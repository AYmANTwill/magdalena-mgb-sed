# 19 — Sediment QC audit: the date trap, the unit trap, and what the SSC network can and cannot support

The sediment sibling of [doc 16](16_forcing_pipeline_audit.md) (forcing) and
[doc 17](17_discharge_qc_audit.md) (discharge). Complete record of the sediment consolidation + QC
campaign: what was built, what was found wrong in the raw data, what was found wrong in **our own
prior claims**, and what the resulting dataset can and cannot be asked to do.

Read §3.1 and §3.9 first if you are picking this up cold. **§3.1 is a general rule for every future
DHIME ingest, not a sediment fact.** **§3.9 is the honest ceiling on the sediment phase** — the data
constrain the answerable question more tightly than the model does.

Every headline number in this document was recomputed in-session by at least two independent code
paths (pandas and a pure-`csv`/`str.split` recount that shares no library heuristic with the first).
Where the two agree but an *established project figure* does not, the disagreement is reported, not
reconciled by choosing — see §4.1 and §4.6.

---

## 1 — Current state

| Component | State |
|---|---|
| Sediment daily (IDEAM DHIME) | **79 stations, 269,337 station-days, 1979-01-01…2018-12-31**, consolidated, structurally clean |
| Sediment inventory | 79 stations with name/dept/coords/minibacia/ENSO coverage/QC counts — **46 lack coordinates, 51 lack a minibacia** |
| Date parsing | ✅ **Fixed and guarded.** `src/dhime_dates.py` proves the format per file from field values; **39,815 station-days recovered** (§3.1) |
| Unit handling | ✅ CM converted `Kg/m3 → mg/L` (×1000); CS already `mg/l`. **Silent factor-1000 hazard, now explicit** (§3.2) |
| Gauge→minibacia mapping | ❗ **28 of 79 mappable** (inherited from the doc-17 re-snap); 46 have no coordinates at all, so no snap of any kind is possible |
| Calibration-safe SSC stations | **24** (28 mapped − 4 BOCATOMA intakes, per doc 17 §5.1) — **73,264 clean paired SSC+Q days** |
| ENSO contrast as designed (2011 vs 2015-16) | ⚠️ **Only 6 bridging stations**, and the one mainstem anchor sees **0 days** of the El Niño side (§3.8) |
| Mainstem SSC | ❗ One upper-Magdalena anchor (21.0 % of basin area), **nothing below it, nothing at the outlet** (§3.9) |
| **Phase C (sediment)** | **Unblocked as a data problem, bounded as a science problem.** The data exist; §3.9 states what they cannot answer |

No raw data was modified. Two new products were written
(`data/processed/sediment_daily.csv`, `sediment_inventory.csv`) and one new module
(`src/dhime_dates.py`). All QC is carried as **flag columns**, not deletions — every figure in §6 is
re-derivable from the shipped table.

---

## 2 — What was built

### 2.1 `src/dhime_dates.py` — the date-format guard *(new, 652 lines, 14 inline smoke tests)*

`detect_date_format(series)` / `parse_dates_safe(series, fmt)` / `parse_dhime_dates(series)`, plus
`DateEvidence` / `SortHint` audit records and four typed exceptions (`AmbiguousDateFormat`,
`ContradictoryDateFormat`, `UnrecognisedDateFormat`, `DateParseError`). **No code path in the module
ever calls `pd.to_datetime` without an explicit `format=`.** Runnable as
`python src/dhime_dates.py`.

The design decision that matters: **the format is decided by counting raw field values > 12 before
any parsing** — a field > 12 cannot be a month, so this is positive proof, independent of any
parser's behaviour. The rejected alternative was counting *parse failures* under each hypothesis
(the naive two-pass fix), which §3.1 proves unsafe on real project data. When every leading field is
≤ 12 the module **raises rather than guessing**, and there is deliberately **no `dayfirst=` default
parameter anywhere in the API** — an escape hatch with a default is precisely how a guess gets
shipped.

### 2.2 `src/build_sediment_gauges.py` — consolidation *(new)*

Mirrors `build_discharge_gauges.py` conventions. Ingests **25 DHIME parts** (16 loose CSVs + 8 zips
+ the loose `concentracion_diaria_santander.csv`) = **450,015 raw rows** → proves the date format per
file → converts units → de-duplicates → flags QC as columns → inherits the doc-17 re-snapped
minibacia mapping → writes:

- `data/processed/sediment_daily.csv` — `code,date,ssc_mean_mg_l,ssc_surface_mg_l,approval,flag_corrupt,flag_zero,flag_flatline,flatline_run_len`; **269,337 station-days**, 15.9 MB
- `data/processed/sediment_inventory.csv` — 79 stations with per-ENSO-window coverage, `calibration_safe`, and `n_distinct`/`resolution` quantisation diagnostics

Threshold choices, each with the rejected alternative:

| Choice | Value | Why, and what was rejected |
|---|---|---|
| Corrupt ceiling | **50,000 mg/L** | Hyperconcentrated flow conventionally begins ~40,000 mg/L and genuinely occurs in steep Andean rivers, so a 40,000 ceiling would flag real physics. **Demonstrably insensitive:** 2nd largest value is 32,000 mg/L, largest is 1.9687 × 10⁸, so *any* ceiling in [32,001, 1.9687 × 10⁸] flags the same single row. Rejected a station-relative ceiling (>20× own p99) — it would mislabel the 1996 delta *period* defect (§3.3) as per-value corruption and be blind to a whole-record slip. |
| Flatline run | **N = 5 consecutive calendar days** | Q integrates catchment storage and has recession memory, so identical consecutive Q is plausible; **SSC responds to individual erosion events with almost no memory, so the discharge N=10 threshold does not transfer.** Empirically N=10 is near-vacuous for sediment (143 days, 4 stations). Rejected N=10 (physically unjustified here, and toothless) and N=3 (at coarsely quantised stations a 3-day repeat is expected by chance). |
| Run adjacency | **consecutive calendar days** | Sediment records are gappy (~250 d/yr). Row-adjacency merges identical values across multi-day gaps and manufactures runs that never happened — **and provably did: it is what produced the wrong published 23-station figure** (§3.4). |
| CM vs CS | **two separate columns** | At the only station with real overlap, CS/CM median is 0.715 (IQR 0.673–0.768) — surface runs ~28 % below the depth average with substantial spread, as a Rouse profile implies. The ratio depends on grain size and shear velocity, not a constant. Rejected rescaling CS by 0.715 and merging: the factor is estimable at 1 of 4 CS stations and buys ~32 station-days in exchange for an unquantified flow-dependent bias in the exact quantity being calibrated. |
| Unmapped stations | **left unmapped, no snap invented** | 46 of 51 have no coordinates at all. Rejected sampling `minibacias.tif` at the coordinate — doc 17 §3.1 showed that method was physically impossible for 79 of 159 discharge gauges. |

### 2.3 Verification apparatus

- **22 synthetic smoke tests passed before any real data was touched** (date detector including the
  undecidable / contradictory / US-order traps; unit factors; flatline runs; approval dedup).
- **24 independent output checks** re-derived every headline from raw bytes via a separate code path
  (pure `csv` module, hand-rolled date swap, hand-rolled run scan). **That pass caught a real defect
  in our own inventory before it shipped** — see §3.10.
- The two date detectors (`dhime_dates.py` and the build script's own) were cross-checked against
  each other on all 25 files: **agreement on 25/25**, and disagreement is coded to abort.
- This document's author re-ran the ENSO design, mainstem, flatline, 1996, CS/CM, distribution and
  duplicate-census computations from the shipped products with fresh code (§6).

---

## 3 — Discoveries (verified)

Verdicts: **CONFIRMED** = independently recomputed by a second code path or mechanism directly
reproduced; **UNCERTAIN** = evidence points one way but a benign explanation survives. REFUTED
findings are in [§4](#4--checked-and-cleared).

### 3.1 The DD/MM/YYYY date trap ❗ *the significant one* — **CONFIRMED, CRITICAL. This is a rule, not a sediment fact.**

**`ssc_cundinamarca.csv` and its byte-identical zip twin use `DD/MM/YYYY`. Every other DHIME export
in this project uses ISO `yyyy-mm-dd`. A naive parse either drops the entire Cundinamarca department
— 39,815 station-days, 6 stations — or silently transposes day and month on 91.6 % of the rows it
keeps, with an identical date span either way.**

Proof, computed in-session by a pure-string test that never invokes a date parser:

| Measure | `ssc_cundinamarca.csv` |
|---|---|
| Rows | 39,815 |
| Rows whose **first** field > 12 (∴ cannot be a month ∴ day-first) | **24,171 (60.7 %)** |
| Rows whose **second** field > 12 | **0** |
| max(field 1), max(field 2) | **31, 12** |

The prior audit's premise — that "only one Cundinamarca value has day > 12" — is **wrong by four
orders of magnitude**. This matters: at 60.7 % the naive fix looks robust under *any* spot-check of
this file. All 6 stations remain individually decidable if exported one at a time (3,597–4,588
proving rows each).

**Why the naive two-pass fix is unsafe — proven on real project data, not just synthetically.** Take
the file and keep only the 15,644 rows that happen to parse month-first (i.e. delete every day > 12
row — exactly what a station sampled early-month, or a re-export, would look like):

| | Result |
|---|---|
| Naive pass 1, `pd.to_datetime(s, errors='coerce')` | **0 NaT** → the `fillna(format='%d/%m/%Y')` rescue **never fires** |
| Dates differing from truth | **14,327 of 15,644 = 91.6 %** |
| Date span, naive | 1990-01-01 … 2018-12-12 |
| Date span, truth | 1990-01-01 … 2018-12-12 — **IDENTICAL** |
| `detect_date_format` on the same input | raises `AmbiguousDateFormat` |

**Every range, span and plausibility gate passes on the corrupted column.** Synthetically: a 7-day
August window `06/08…12/08/2004` becomes **seven different months on the 8th**. Six of seven rows
transpose; `08/08` survives correct by self-symmetry — so **the corruption is *partial*, and a
day-of-month histogram of the corrupted column still shows 1–12 populated.** A daily record retains
a correct fraction equal to the share of day == month dates (~12/365 ≈ 3.3 %).

**Precipitation and discharge are NOT contaminated — measured, not assumed.** The detector was run
over every DHIME corpus in the repo:

| Corpus | Parts | Rows | Non-ISO parts | Detector raises |
|---|---|---|---|---|
| Sediment | 25 | 450,015 | **2** (`ssc_cundinamarca.csv` + `.zip`) | 0 |
| Discharge | 45 | 2,443,316 | **0** | 0 |
| Precipitation | 295 (from 236 top-level files; the organised working set is **98/98 CSVs**) | 2,678,351 | **0** | 0 |

This independently reproduces the known answer (day-first set == exactly the two Cundinamarca files,
**MATCH = True**), with 0 NaT after explicit-format parsing, and confirms the anomaly is isolated —
the two files are one duplicated export, not a portal-wide behaviour.

**The date fix is validated physically, not merely structurally.** The two paired Cundinamarca
stations reach SSC–Q Spearman ρ = 0.457 (21237020, n = 6,400) and 0.345 (21197010, n = 5,817),
inside and above the ISO-file fleet distribution (median 0.340). Deliberately swapping day↔month
wherever legal degrades them to 0.285 and 0.204. Recovered dates carry real signal.

> #### RULE for every future DHIME ingest — adopt verbatim
>
> 1. **Never call `pd.to_datetime` without `format=`.** Bare inference is a silent layout guess.
> 2. **Never use inference-then-`fillna` as a "robust" fallback.** Parse failure is not evidence of
>    layout: a `DD/MM` column is only *detectably* `DD/MM` if it happens to contain a day > 12. When
>    it does not, the rescue pass never fires and the transposition is total and invisible.
> 3. **Decide the layout from raw field values > 12, before parsing.** Positive proof, no parser in
>    the loop.
> 4. **When no field exceeds 12, raise.** There is no evidence, so any return value is a
>    fabrication. Resolve externally (sibling file from the same export; date-overlap against another
>    variable at the same station; the station's known operating span) or **exclude and record the
>    exclusion**.
> 5. **Assert zero NaT on non-null input after parsing.** A row count that shrinks without complaint
>    is how a department disappears.
> 6. **Never trust these as detection:** "dates look plausible", "the span is right", "the row count
>    is unchanged", or a day-of-month histogram. All four pass on a transposed column. One assertion
>    that *is* worth adding to any multi-year daily ingest: **max(day-of-month) > 12**.
> 7. **Do not disambiguate by separator.** `13-01-2004` is a plausible DHIME variant; the position of
>    the 4-digit year is the signal, not `/` vs `-`. And a `yyyy-dd-mm` series must be refused, not
>    accepted as ISO.
>
> Two live call sites still violate rules 1–2 — see §5.4 items 9 and 10. Neither is corrupting
> anything **today**, because the sweep above proves both corpora are currently 100 % ISO. Neither
> has a guard.

### 3.2 The kg/m³ unit trap — factor 1000, silent — **CONFIRMED**

**DHIME serves variable CM (`Concentración media diaria`, depth-averaged) in `Kg/m3` and variable CS
(`Concentración superficial`) in `mg/l`. Reading `Valor` without checking `Unidad` understates CM by
exactly 1000×.**

449,740 raw CM rows carry `Unidad = Kg/m3`; 275 CS rows carry `mg/l`. The trap is nastier than a
normal unit error because **both readings look like a concentration**: unconverted CM has median
0.059 kg/m³, and "0.06" is a perfectly plausible-looking number that no range check on a column
labelled *concentration* would reject. Converted, the median is **59 mg/L** — squarely in the
published Magdalena range. A MUSLE α/β calibrated against unconverted CM would absorb the factor
1000 into the erosion coefficients and report an excellent fit.

`build_sediment_gauges.py` keys the ×1000 off the `Unidad` string per row, not off the variable code,
so a future export that changes units on either variable converts correctly or fails loudly.

### 3.3 A 1996 year-scale defect at **all six** zone-29 delta stations — **CONFIRMED, never previously reported**

Leave-one-year-out station medians (recomputed in-session, stations with ≥ 60 days in 1996):

| Station | 1996 median | Other-years median | Ratio | n(1996) |
|---|---|---|---|---|
| `29067150` GANADERIA CARIBE | **7,000 mg/L** | 23 | **304×** | 139 |
| `29067040` SANTA ROSALIA | 800 | 15 | 53× | 99 |
| `29067010` EL TREBOL | 1,000 | 21 | 48× | 201 |
| `29067060` PUERTO RICO HACIENDA | 1,000 | 28.5 | 35× | 94 |
| `29067130` PUENTE FERROCARRIL | 550 | 22 | 25× | 157 |
| `29067050` CANAL FLORIDA | 200 | 16 | 12.5× | 191 |

**This is not a basin-wide 1996 signal.** The basin-wide median 1996/other-years ratio is **1.32**
over the 35 testable stations — indistinguishable from ordinary interannual variation. Six stations,
one hydrographic zone, one source file (`ssc_magdalena.csv`), ratios 12.5–304×: a rating or units
change in the Ciénaga Grande network, not hydrology. Also caught: `28037090` 1996 = 101 days of
median **0.0 mg/L**; `26127010` 1999 at 10.0×; `24017820` 1993 and `21217250` 2004 at 0.06×.

**Exclude 1996 at all six zone-29 stations and at `28037090` before any sediment use.** Note four of
these six are also the unmapped zone-29 discharge gauges of doc 17 §5.3 — the same delta network is
failing two independent audits.

### 3.4 The established "23 stations flatline ≥ 10 days, worst 24037040 at 4.2 %" is a de-duplication artefact — **CONFIRMED as an artefact; true figure is 4 stations**

The claim was **reproduced exactly** — but only by scanning raw rows *without* de-duplication, using
row-adjacency: 2,474 flat days, **23 stations**, `24037040` at **4.2058 %**. The 8 zips duplicate 8
departments byte-for-byte, so every station-day appears twice and **every apparent run length
doubles**.

Recomputed in-session off the shipped table, calendar-day adjacency, de-duplicated:

| Threshold | Flat days | Stations |
|---|---|---|
| N ≥ 5 (the shipped `flag_flatline`) | **952 (0.354 %)** | **28** |
| N ≥ 7 | 373 | 13 |
| N ≥ 10 | **143 (0.05 %)** | **4** |
| N ≥ 20 | 22 | 1 |

Longest run anywhere is **22 days** (`24037040`) — yet the original claim implies runs ≥ 10 at 23
stations. Worst share of record at N ≥ 10: `24037040` **1.04 %** (not 4.2 %), then `24017820` 0.53 %,
`29067150` 0.50 %, `21217250` 0.48 %.

**Consequence: `24037040` does *not* "fail two independent tests".** It fails only the corrupt-value
test (§6). The "fails two tests" framing was an artefact of counting duplicated rows.

That N = 5 is the right threshold was established against a null, not asserted: a **within-station
value shuffle** (preserving each station's exact value multiset, hence its quantisation coarseness)
puts the chance expectation at N ≥ 5 at 0.00037 % against 0.354 % observed — a **952× excess**; at
N ≥ 7 the null is 0 in 20 replicates.

### 3.5 A 06:00-timestamp provenance splice at 4 stations — **CONFIRMED, unreported until now**

2,788 raw rows (1,394 unique station-days) carry a `06:00` stamp rather than `00:00`. All are in
`ssc_cundinamarca.csv` and its twin, at 4 stations (`21197010`, `21207960`, `21237010` NARIÑO-AUT,
`23067040` PUERTO LIBRE-AUT), 2016–2018. **Median 16 decimal places vs 3 for the `00:00` rows** — the
signature of a sensor-derived computation, not a manual lab value. 0 station-days carry both stamps,
and every 06:00 segment begins strictly *after* that station's 00:00 record ends (`21197010`: 00:00
spans 1990–2012, 06:00 is 2016 only).

So it **extends** the record rather than duplicating it — but by a different method. **Do not fit one
SSC–Q rating across the splice**, and allow ±1 day slack when pairing 06:00 rows against discharge,
whose averaging window doc 17 §3.12 already flags as *assumed* midnight-to-midnight.

### 3.6 Three "calibration-safe" stations have no SSC–Q relationship at all — **CONFIRMED**

Spearman ρ(Q, SSC) on clean paired days, recomputed in-session over the 33 stations with ≥ 100 clean
paired days (**fleet median 0.340**, range −0.019 … 0.715):

| Station | ρ | n (clean paired d) | Note |
|---|---|---|---|
| `21217250` BOCATOMA | **−0.019** | 7,049 | intake; already excluded by the safe-set rule |
| `26107070` LA VICTORIA-AUT | **−0.003** | 1,703 | **in the safe-24 set** |
| `22017010` BOCAS | **+0.032** | **6,966** | **in the safe-24 set**; also a doc-17 §3.8 bifurcation twin (mirrored −35 %/+41 % break pair) |
| `29067150` GANADERIA CARIBE | +0.045 | 2,348 | also the worst 1996 station (§3.3) — **fails two independent tests** |
| `26247030` APAVI | **+0.055** | **274** | **the largest-area Cauca SSC station** (37,808 km²) — see §3.9 |
| — strongest, for contrast — | | | `26127010` EL ALAMBRADO **+0.715** · `21147030` CARRASPOSO +0.680 · `26167060` PAILA LA +0.618 |

A river with zero SSC–Q dependence over 6,966 clean paired days is not physically credible. A flat
SSC–Q relation
usually means SSC was infilled from a constant or a non-local rating. **Do not use `26107070` or
`22017010` for sediment-rating calibration without inspecting their rating history first.** `26247030`
APAVI is the more consequential one because it is the only near-mouth Cauca gauge (§3.9) — but at
n = 274 its ρ is weakly determined, so this is the one entry here rated **UNCERTAIN**.

### 3.7 Only 28 of 79 sediment stations can be mapped; 46 have no coordinates at all — **CONFIRMED**

- **28** inherit the doc-17 re-snapped mapping from `gauge_minibacia.csv`.
- **33** are also discharge stations — so **5 discharge stations still have no mapping**, all zone 29
  (`29067010, 29067050, 29067120, 29067130, 29067150`): the doc 17 §5.3 delta-gauge open item,
  reappearing.
- The other **46** are sediment-only **and** have no lat/lon in `stations_discharge_coords.csv`. Even
  a bad snap is impossible.
- Of the mapped 28, **4 are literally named BOCATOMA** (`21217230, 21217250, 22057090, 24017820`) —
  intake gauges doc 17 §3.6/§5.1 says to exclude permanently. Hence **24**, not 28,
  calibration-safe.

Both figures are shipped with their definitions, because *matching* the established 28-station number
is not the same as being *right*: reporting only 28 would silently carry four diversion works into a
river-sediment calibration set.

### 3.8 ENSO calibration design: the 2011-vs-2015-16 contrast is the **weakest** of the four candidate pairings — **CONFIRMED, and it is the reason a second ENSO cycle matters**

All figures recomputed in-session from `sediment_daily.csv` × `discharge_daily.csv`, restricted to
the 24 calibration-safe stations, clean = not zero/corrupt SSC and Q > 0, and a station counts toward
a window only with **≥ 30 clean paired days** in it.

Per-window availability:

| Window | Span | SSC stations (all 79) | Safe paired stations | Clean paired days | Stations ≥ 30 d |
|---|---|---|---|---|---|
| `elnino_1997_98` | 1997-05 … 1998-05 | 43 | 11 | 2,900 | **11** |
| `lanina_1999_2000` | 1999-07 … 2000-06 | 43 | 10 | 2,146 | **10** |
| `elnino_2009_10` | 2009-06 … 2010-05 | 35 | 11 | 2,818 | **10** |
| `lanina_2011` | 2011 | 37 | 10 | 2,144 | **10** |
| `elnino_2015_16` | 2015–2016 | 32 | 13 | 2,773 | **13** |
| model window | 2009-01 … 2017-12 | 59 | 18 | 15,036 | **18** |
| full record | 1979 … 2018 | 77 | 24 | 73,264 | **24** |

**Bridging stations — the number that actually decides the design.** A ratio-based ENSO contrast only
cancels model bias if *the same station* is observed in **both** phases. Stations meeting ≥ 30 clean
paired days in both:

| Calibration / target pairing | Phase 1 | Phase 2 | **Bridging** | Bridging stations |
|---|---|---|---|---|
| `lanina_2011` vs `elnino_2015_16` *(the locked design)* | 10 st / 2,144 d | 13 st / 2,773 d | **6** | 21197010 · 22017010 · 22017030 · 23127010 · 24037390 · 26017060 |
| `elnino_2009_10` vs `lanina_2011` | 10 st / 2,818 d | 10 st / 2,144 d | **10** | the 6 above **+ 21237020 · 24027030 · 26107130 · 26137110** |
| `elnino_1997_98` vs `lanina_1999_2000` | 11 st / 2,900 d | 10 st / 2,146 d | **10** | 21197010 · **21237020** · 22017010 · 22017030 · 23127010 · **24027030** · 24037390 · **26107070** · **26127010** · **26137110** — a *different* set: it gains 21237020 and 26127010 but **loses 26017060** |
| `elnino_2009_10` vs `elnino_2015_16` *(same-phase control)* | 10 st / 2,818 d | 13 st / 2,773 d | **6** | identical to row 1 |

The row-3 set is not a superset of row 1, so the pairings are not simply nested: **only 5 stations
(21197010, 22017010, 22017030, 23127010, 24037390) bridge every candidate pairing.** Those 5 are the
irreducible core of any ENSO sediment contrast, whichever cycle is chosen.

**The locked 2011-vs-2015-16 design has the fewest bridging stations of any pairing tested — 6 — and
it loses the single most valuable station in the dataset.** `21237020` ARRANCAPLUMAS is the only
Magdalena **mainstem** SSC gauge (54,035 km² upstream = **21.0 %** of the basin, Q median
1,103 m³/s, ρ = 0.457 over 6,400 clean paired days). Its clean paired days per window:

| Window | `elnino_1997_98` | `lanina_1999_2000` | `elnino_2009_10` | `lanina_2011` | `elnino_2015_16` |
|---|---|---|---|---|---|
| ARRANCAPLUMAS `21237020` | **293 d** | **261 d** | **279 d** | 91 d | **0 d** |

Its SSC record ends **2015-08-31**. So under the locked design **the only mainstem anchor is
one-sided** — present for La Niña, absent for El Niño — which is exactly the failure mode a
ratio-based contrast cannot absorb. Under either earlier cycle it contributes ~260–293 days to *both*
phases.

**This is the quantitative case for a second ENSO cycle.** 1997-98 vs 1999-2000 pairs the El Niño
that `docs/07` already classes as top-3 all-time (with 1982-83 and 2015-16) against the La Niña that
followed it, delivers **10 bridging stations instead of 6**, and is the *only* pairing in which the
mainstem anchor is present on both sides. Two costs must be stated honestly: (a) it lies **outside
the 2009–2017 forcing window**, so using it requires extending ERA5-Land and the rainfall forcing
back to 1997 — a data-acquisition task, not a modelling one; and (b) **the 1999-2000 La Niña's ONI
strength has not been established anywhere in this repo** (`docs/07` classifies only the 1997-98,
2010-11, 2015-16 and 2016-18 events), so it must be confirmed against the NOAA CPC ONI table before
the pairing is adopted — a weak cold phase would blunt the contrast even with 10 bridging stations.

Secondary observations from the same computation:

- **The terminal years are the weak point, worse than the raw station count suggests.** Within the
  safe paired set: 2015 = 11 st / 2,001 d, **2016 = 4 st / 772 d**, **2017 = 2 st / 376 d**
  (`26167070` 324 d, `26127010` 52 d), 2018 = 11 st / 2,420 d. The El Niño target window is carried
  overwhelmingly by its 2015 half.
- **2018 is a wasted harvest.** 45 SSC stations and 11 safe paired stations / 2,420 clean paired days
  exist in 2018 — entirely **outside** the 2009-2017 forcing window (doc 16 §1, ERA5-bounded).
  Extending the forcing forward by one year is a cheaper way to gain calibration stations than any
  new download.

### 3.9 What the sediment data **cannot** support — state this before anyone promises it

**(a) The mainstem gap is real, but the usual phrasing is wrong and the correction matters.** It is
not true that there is "no mainstem SSC". Recomputed upstream areas by post-order accumulation over
`minibacias.csv` (outlet check: 257,097 km², matching doc 17):

| Station | River | Upstream area | % of basin | Q median | SSC days | Clean paired | ρ |
|---|---|---|---|---|---|---|---|
| `21237020` ARRANCAPLUMAS | **Magdalena mainstem** | **54,035 km²** | **21.0 %** | 1,103 m³/s | 6,596 | 6,400 | 0.457 |
| `26247030` APAVI | **Cauca, near mouth** | 37,808 km² | 14.7 % | 1,031 m³/s | **304** | **274** | **0.055** |
| `26207080` BOLOMBOLO-AUT | Cauca, middle | 30,848 km² | 12.0 % | 725 m³/s | **387** | 385 | 0.377 |
| `26167070` IRRA-AUT | Cauca, upper | 24,665 km² | 9.6 % | 586 m³/s | 993 | — | — |
| — | *Magdalena below Arrancaplumas* | — | — | — | **none** | — | — |
| `29037020` CALAMAR (outlet) | Magdalena at the sea | 257,097 km² | 100 % | 6,954 m³/s | **no SSC** | — | — |

The precise statement: **there is one well-observed mainstem anchor covering a fifth of the basin,
and below it nothing.** The Magdalena–Cauca confluence, the Mojana/Mompós floodplain, the Brazo de
Loba/Mompós distributaries and the outlet at Calamar have **zero SSC**. The Cauca *is* gauged near its
mouth (APAVI) but with **274 clean paired days and ρ = 0.055** — that is not a calibration target,
it is a spot check. The zone-29 stations that look coastal are Ciénaga Grande de Santa Marta
tributaries (Fundación, Río Frío), **not** the Magdalena, and six of them carry the 1996 defect
(§3.3). Consequence: **the basin's sediment *export* — the quantity the project is ultimately about
— is not observed anywhere.** It can only be inferred by routing a model calibrated on the upper
21 %, and the "Cauca vs Magdalena share" question rests on a 274-day sample at the Cauca end.

**(b) The 2016-17 collapse.** Per-calendar-year SSC station counts (all 79 stations, ≥ 1 day):
2013 **16**, 2014 25, 2015 28, **2016 12**, **2017 14**, 2018 45. At ≥ 60 days: 2016 **12**,
2017 **9**. At ≥ 200 days: 2016 **6**, 2017 **4**. And within the calibration-safe paired set,
**2016 = 4 stations, 2017 = 2 stations** (§3.8). *(The established "11-13 stations" figure for
2016-17 is close to but not exactly reproducible — I measure 12 and 14 at ≥ 1 day; see §4.6.)*
Anything framed as a 2016-17 result rests on 2–4 usable stations.

**(c) The realistic performance bar, stated from the project's own benchmark.** `docs/14` §"Honest
scope" already records it: **Fagundes et al. (2026) report SSC KGE from −0.26 to 0.44** — with
in-situ data and **25 years of calibration**. That is the method's own published range, and a
negative KGE means *worse than predicting the mean*. This project has **6 bridging stations across
the locked ENSO pairing** (§3.8), no mainstem SSC below 21 % of the basin, and a 9-year forcing
window. **It is not reasonable to expect to beat −0.26…0.44, and a reported SSC KGE above ~0.5
should be treated as a bug until proven otherwise** — most likely a unit slip (§3.2), a date
transposition (§3.1), or calibration and validation sharing days.

The defensible output is therefore the **relative** comparison (2011 vs 2015-16; Cauca vs Magdalena
share), where multiplicative model bias partly cancels — which is what `docs/14` already argues. §3.8
adds the constraint that a ratio only cancels bias across **bridging** stations, so the relative
result is quantitatively supported by **6 stations**, not by all 24.

### 3.10 Our own verification caught a defect in our own inventory before it shipped — **recorded, not buried**

The independent output check found `sum(inventory.n_mean_days) = 269,304` against **269,305** CM
station-days in `sediment_daily.csv`. Cause: `n_mean_days` was computed on the `flag_corrupt`-excluded
frame, so the single corrupt station-day was **silently missing from a count column while the flags
elsewhere claimed nothing had been deleted**. Fixed: `n_mean_days` now counts every CM day, while
`p50/p99/max/n_distinct` still exclude `flag_corrupt` (otherwise `max` would read 1.9687 × 10⁸).
All 24 checks re-pass. Recorded because it is exactly the class of silent inconsistency the recheck
rule exists to catch, and **it survived a code review.**

A second self-inflicted defect, in `dhime_dates.py`: the original `_corroborate_monotonic`
cross-check was **vacuous dead code**. It returned early whenever either hypothesis produced any
NaT — but the only path that called it is the path where value-evidence already decided, and there a
> 12 field makes the rejected hypothesis unparseable *by construction*. Probed directly: it returned
`None` on **100 % of its only calling path**. Redesigned as `_sortedness_hint`, computed on the
**ambiguous subset** (rows parseable under both), which makes it genuinely independent: sorted
fraction **0.9997 (d/m/Y) vs 0.9036 (m/d/Y)** on Cundinamarca's 15,644 ambiguous rows, margin 0.096
against a 0.02 threshold and a 0.00013 station-reset noise floor. **It remains advisory and is never
allowed to decide** — because on the crafted 6th-to-12th series both readings are perfectly ascending
(1.0 vs 1.0), so the margin collapses to zero exactly where a decision is most wanted. A smoke test
pins that.

"The check that never fires" is the same class of defect as the doc-16 dry-fraction test that missed
the worst stations.

### 3.11 Traps for whoever picks this up

- **DHIME date layout is per-file, not per-portal.** §3.1. The rule box is the deliverable of this
  document.
- **DHIME units are per-variable and per-row.** CM is `Kg/m3`, CS is `mg/l` (§3.2). Key the
  conversion off the `Unidad` column, never off the variable code or the filename.
- **Raw sediment rows are ~1.67× the truth.** 450,015 raw rows → 269,580 unique
  `(code,date,Variable)` keys, because 8 departments were downloaded as both `.csv` and `.zip`.
  **Any statistic computed pre-dedup is wrong by a station-dependent factor**, and run-length
  statistics are wrong by ~2× (§3.4). Always state the base.
- **Row adjacency ≠ calendar adjacency in a gappy record.** Sediment averages ~250 d/yr. Scanning
  runs by row index merges values across multi-month gaps and manufactures runs (§3.4).
- **Rating-table quantisation mimics flatlining**, as for discharge: `26017060` has **27 distinct
  values in 2,591 rows**. Check `n_distinct`/`resolution` in the inventory before condemning a
  station. This is why `flatline_run_len` ships as a column — a caller preferring N = 10 filters
  `flatline_run_len >= 10` without re-deriving anything.
- **A flat SSC–Q relation is a data smell, not a hydrological finding** (§3.6). ρ ≈ 0 over thousands
  of days means infilling, not a river.
- **CS and CM are not interchangeable.** CS/CM median 0.715, IQR 0.673–0.768 (§2.2). Merging them
  injects a flow- and grain-size-dependent bias into the calibration target.
- **Approval level carries no screening power here either** — as for discharge (doc 17 §3.12). The
  0 approval conflicts among 180,435 duplicate rows (§4.1) mean it is consistent, not that it is
  informative.
- **Zone 29 is the delta, not the mainstem.** A zone-29 code near the coast is a Ciénaga Grande
  tributary (§3.9), and six of the eight carry the 1996 defect (§3.3).
- **`n_days` ≠ `n_mean_days` + `n_surface_days`** where a station has both variables on one date
  (§2.2) — the table is one row per `(code, date)`.

---

## 4 — Checked and cleared

Findings that did not survive verification, plus reconciliations recorded so nobody re-chases them.

### 4.1 The 180,435 duplicate rows are benign — **REFUTED as a data conflict**

Pure-`csv` census in-session: 450,015 raw rows → **269,580** unique `(code,date,Variable)` keys →
**180,435 duplicate rows**, with **0 groups holding more than one distinct `Valor`** and 0 holding
more than one `NivelAprobacion`. Byte-identical re-exports; the approval-priority rule never had to
arbitrate — the same result doc 17 §4.1 found for discharge.

### 4.2 The 140,620 vs 180,435 duplicate discrepancy — **reconciled exactly, both figures are right for their base**

**180,435 − 39,815 = 140,620**, computed in-session. The established figure is a **pre-date-fix**
count: before the fix, both Cundinamarca files NaT'd out entirely, so neither their rows nor their
mutual duplication entered the census. Likewise "CM = 71 stations" becomes 77 once the 6
Cundinamarca-only stations are recovered (79 total including CS-only, which matches the established
79). **State which corpus each figure describes, or the two read as a conflict.**

### 4.3 The 269,194 usable-rows figure — **reconciled exactly**

269,580 unique `(code,date,Variable)` keys − **385** zero-SSC keys − **1** corrupt key =
**269,194**, exactly the established figure. An earlier pass reported this as an unresolved 386-row
gap; it is not a gap, it is the QC drop. Quote with the base attached: **269,337 station-days /
269,580 `(code,date,Variable)` records / 269,194 after dropping zeros and the corrupt value**. The
shipped table keeps all 269,337 with flags, so all three are derivable.

### 4.4 Zero-SSC (756) and corrupt (2) counts — **raw-row figures; de-duplicated they are 385 and 1**

Pure-`csv` raw scan reproduces 756 and 2. On the de-duplicated table: **385 zeros at the same 17
stations**, and **1** corrupt station-day (`24037040`, 2018-05-19, 1.9687 × 10⁸ mg/L = 196,867
Kg/m³, a clean 10⁶ slip). The differences are the zip re-exports. Quote 385 / 1 for anything
per-station-day.

### 4.5 Paired SSC+Q agrees with the established figures to 6 days in 103,283 — **cleared**

Recomputed in-session: raw pairing **103,283 days / 33 stations**; mapped-28 set **92,190 / 28**;
safe-24 set **73,265 / 24**. Station counts match the established 33 and 28 **exactly**. Applying the
exclusion rule the prior audit used (drop SSC = 0, SSC > ceiling, Q = 0) gives **102,895** and
**91,981** against the established 102,901 and 91,987 — **the same −6 in both**. The six are the
zero-SSC paired days at `29067050`, which the prior audit retained. 0.006 % discrepancy, localised to
one station. Do not tune.

### 4.6 The published SSC distribution is **not** reproducible on any base I could construct — **reported, not resolved**

The established figure is "median 47, p99 2,000, p99.9 5,362 mg/L". Two fully independent methods
(pandas, and a pure-`csv` recount sharing no code) agree with **each other** to rounding on all three
candidate bases, and **none** matches:

| Base | n | p50 | p99 | p99.9 | max |
|---|---|---|---|---|---|
| Raw, un-deduplicated (CM ≤ ceiling) | 449,738 | 58 | 1,850 | 5,000 | 32,000 |
| **De-duplicated, date-fixed (shipped)** | **269,304** | **59** | **1,895** | **4,870** | **32,000** |
| De-duplicated, Cundinamarca excluded (≈ pre-date-fix) | 229,489 | 50 | **2,000** | 5,084 | 32,000 |

p99 reproduces **exactly** (2,000) on the pre-date-fix base, which identifies the era of the
established figure — but p50 (50 vs 47) and p99.9 (5,084 vs 5,362) do not, on that or any other base.
Per the recheck rule this is reported rather than reconciled by choosing. **Quote the shipped
de-duplicated figures — p50 59, p99 1,895, p99.9 4,870, max 32,000 mg/L — and note the physical
verdict is unchanged either way: the distribution is sound** (median tens of mg/L, p99 ~2 g/L, p99.9
~5 g/L, max 32 g/L just below the hyperconcentration transition).

### 4.7 No out-of-basin sediment stations — **cleared, unlike discharge**

All 79 codes fall in zones 21–29: `{21:18, 22:5, 23:9, 24:15, 25:3, 26:18, 28:3, 29:8}` (sums to 79,
verified). Contrast doc 17 §3.12, where the discharge downloads spilled 14 stations into the Orinoco
(35), Catatumbo (37) and Pacific (53/54). Also verified clean: 0 duplicate `(code,date)` rows, 0
negative SSC, 0 rows with both SSC columns null, 0 null approvals, 0 ingest failures, 0 schema
anomalies, 0 value conflicts, 0 approval conflicts. **Keep the check anyway — it is one line and the
discharge network proved it can fail.**

### 4.8 "1996 was a basin-wide sediment anomaly" — **REFUTED**

Basin-wide median 1996/other-years ratio = **1.32** across 35 testable stations, indistinguishable
from ordinary variation (§3.3). The 12.5–304× excursions are confined to six stations in one zone
from one source file. No basin-wide 1996 adjustment is warranted; the six stations are excluded
instead.

### 4.9 The zip re-exports are not a second data source — **cleared**

The 8 zips duplicate 8 departments byte-for-byte (§4.1: 0 value conflicts). They add **no**
information; they only inflate raw counts (§3.11) and doubled the flatline statistic (§3.4). The one
genuine extra part is the loose `concentracion_diaria_santander.csv`.

---

## 5 — Open items, ranked by whether they block the sediment phase

### 5.1 Station disposition before sediment calibration *(the plain-language answer)*

**Usable now — 24 calibration-safe stations, 73,264 clean paired SSC+Q days**, with `flag_corrupt`,
`flag_zero` and `flag_flatline` (N ≥ 5) masked as missing. Best-constrained: `26127010` EL ALAMBRADO
(ρ = 0.715), `21147030` CARRASPOSO (0.680), `26167060` PAILA LA (0.618). Primary mainstem anchor:
`21237020` ARRANCAPLUMAS (54,035 km², ρ = 0.457) — **but only for periods ending before
2015-08-31** (§3.8).

**Exclude segments, keep the station:** 1996 at `29067010, 29067040, 29067050, 29067060, 29067130,
29067150` and `28037090` (§3.3); `24037040` 2018-05-19 (the corrupt row, already flagged); the 06:00
segments at `21197010, 21207960, 21237010, 23067040` treated as a separate provenance class, not
spliced into one rating (§3.5).

**Do not use for rating calibration without a rating-history check:** `26107070` (ρ = −0.003) and
`22017010` (ρ = +0.032) (§3.6).

**Exclude permanently:** the 4 BOCATOMA intakes inside the mapped set (`21217230, 21217250,
22057090, 24017820`) — doc 17 §3.6/§5.1.

**Blocked on coordinates:** the 46 sediment-only stations with no lat/lon, and the 5 zone-29
discharge stations with no minibacia.

### 5.2 Blocking the sediment phase

1. **Decide the ENSO pairing, on the §3.8 numbers.** The locked 2011-vs-2015-16 contrast has **6
   bridging stations** and **no mainstem anchor on the El Niño side**. 1997-98 vs 1999-2000 has
   **10 bridging stations** and ~260–293 mainstem days on *both* sides. This is a design decision
   with a data cost either way and it must be taken explicitly, not inherited: choosing the earlier
   cycle requires extending ERA5-Land and the rainfall forcing back to 1997 (item 3); keeping the
   locked cycle means accepting a one-sided mainstem and a 2-to-4-station 2016-17 (§3.9b).
2. **Coordinates + drainage areas for the 46 unmapped sediment stations** — extend
   `src/fetch_station_coords.py` to pull the IDEAM catalogue coordinate **and catalogue drainage
   area**, then re-snap by **drainage-area matching**. Note `fix_gauge_minibacia_mapping.py` scores
   candidates by runoff coefficient, which needs a Q series these stations lack, so it must fall back
   to the catalogue area. **The point-in-cell raster snap is not an option** (doc 17 §3.1). Until
   this is done the sediment network is 24 stations, not 79.
3. **Extend the forcing window** in whichever direction the item-1 decision requires: **back to 1997**
   for the earlier ENSO cycle, and/or **forward through 2018** to capture the 45-station / 11-safe-paired
   / 2,420-day 2018 harvest that currently falls outside 2009-2017 (§3.8). Forward by one year is the
   cheapest calibration-station gain available.
4. **Apply the §5.1 masks as a scripted, reproducible step** — a `sediment_daily_qc.csv` or mask
   file, not ad-hoc notebook filtering. The flags are already columns; the exclusion *periods* (1996
   zone-29, the 06:00 segments) are not yet encoded anywhere machine-readable.
5. **Write down the expected-performance bar before calibrating** (§3.9c: KGE −0.26…0.44 from the
   method's own paper, with 25 years of data against our 9). Pre-registering it is what stops a
   suspiciously good KGE from being celebrated instead of debugged.

### 5.3 Not blocking, worth doing

6. **IDEAM metadata check for a 1996 rating or units change in the Ciénaga Grande network** (§3.3) —
   would convert six excluded stations into six correctable ones, and the same six overlap the
   doc 17 §5.3 delta open item.
7. **Rating-history check for `26107070` and `22017010`** (§3.6), and for `26247030` APAVI, whose
   ρ = 0.055 on 274 days is the only evidence at the Cauca mouth (§3.9a).
8. **Fit and publish the CS→CM relation** if any further CS station is delivered. At present it is
   estimable at 1 of 4 CS stations (0.715, IQR 0.673–0.768) and merging is not justified (§2.2).

### 5.4 Housekeeping — the two unguarded date call sites

9. **`src/build_precip_gauges.py:62`** — `pd.to_datetime(a['Fecha'], errors='coerce')` with **no
   `format=`, no fallback, no NaT assertion**. The weakest of the three ingests: a day-first precip
   export would be transposed with **no NaT and no warning**. Currently harmless (295/295 parts ISO,
   §3.1) but unguarded, and the precip corpus is **re-downloaded** by
   `src/download_precip_automatic.py`, so a future re-export could introduce a day-first part at any
   time. Replace with `detect_date_format` + `parse_dates_safe`.
10. **`src/build_discharge_gauges.py:149-152`** — the mirror-image hazard: ISO-format-first, then
    **bare pandas inference as the `fillna` fallback**. On a day-first part the ISO pass yields
    all-NaT and the fallback hands the layout choice to inference. Smoke-tested: for `06/08/2004`,
    `07/08/2004` the ISO pass gives 2/2 NaT and the fallback returns **8 June / 8 July** —
    transposed. Currently harmless (45/45 parts ISO) and **one non-ISO IDEAM re-export away from
    silent corruption**. ⚠️ **This file is inside the concurrently-running hydrology workflow's
    scope — hand over, do not edit.**
11. **Consider splitting `dhime_dates.py`'s 14 inline smoke tests** into `src/test_dhime_dates.py` to
    match the repo precedent (`src/test_mgb_hydrology.py`). They were kept inline so the module
    self-verifies with no test infrastructure and the naive-fix proof sits beside the docstring that
    rejects it; the tests import nothing beyond the public API plus `_sortedness_hint`/`SORT_MARGIN`,
    so the split is a one-move change.
12. **Consider an explicit exclusion register** — analogous to `gauge_minibacia_remap_report.csv`'s
    `action` column — so `AmbiguousDateFormat`-driven and QC-driven exclusions are **auditable
    rather than merely absent**. A department that vanishes silently is the defect this whole audit
    exists to prevent.
13. **`_sortedness_hint` treats the Series as one block**, so station-boundary resets count as
    genuine backward steps — negligible for Cundinamarca (5 of 39,814 = 0.013 %) but material for a
    file with many short station records. Add an optional grouping key if it is ever promoted above
    advisory status.

---

## 6 — Key numbers

Every value recomputed in-session; those marked † were reproduced by two independent code paths
(pandas and a pure-`csv`/`str.split` recount).

| Quantity | Value |
|---|---|
| Raw parts / rows ingested | 25 parts (16 CSV + 8 zip + 1 loose) / **450,015 rows** † |
| Unique keys / duplicates | 269,580 `(code,date,Variable)` † / **180,435 duplicate rows, 0 value + 0 approval conflicts** † |
| Duplicate reconciliation | 180,435 − 39,815 = **140,620** = the pre-date-fix established figure † |
| Consolidated | **79 stations, 269,337 station-days, 1979-01-01…2018-12-31** |
| Usable-rows reconciliation | 269,580 − 385 zeros − 1 corrupt = **269,194** = established figure, exactly |
| **Date fix** | 2 of 25 sediment parts are `%d/%m/%Y %H:%M`; **39,815 station-days / 6 stations recovered** |
| Day-first proof | `ssc_cundinamarca.csv`: **24,171 / 39,815 rows (60.7 %) have field 1 > 12**; 0 have field 2 > 12; max 31 / 12 † |
| Naive-fix failure rate | **91.6 % of dates wrong** (14,327 / 15,644) with **0 NaT** and an **identical date span** |
| Format sweep | sediment 2/25 non-ISO · **discharge 0/45** (2,443,316 rows) · **precip 0/295** (2,678,351 rows; 98/98 organised CSVs) · 0 detector raises |
| NaT after explicit parse | **0** across all 450,015 rows |
| Unit conversion | 449,740 CM rows `Kg/m3` **×1000** → mg/L; 275 CS rows already `mg/l` |
| CM distribution (shipped base) | **p50 59 · p99 1,895 · p99.9 4,870 · max 32,000 mg/L** † *(see §4.6)* |
| Corrupt | **1** station-day: `24037040` 2018-05-19, 1.9687 × 10⁸ mg/L (a 10⁶ slip); ceiling insensitive over [32,001, 1.9687 × 10⁸] |
| Zeros | **385** station-days at **17** stations (756 raw rows) † |
| Flatlines | N ≥ 5: **952 d / 28 st (0.354 %)** · N ≥ 7: 373 / 13 · N ≥ 10: **143 / 4** · longest run **22 d** (`24037040`, 1.04 % of its record) |
| Flatline null | within-station shuffle: 0.00037 % expected vs 0.354 % observed at N ≥ 5 = **952× excess** |
| Established flatline claim | 23 st / 4.2058 % — **reproduced only pre-dedup with row-adjacency**; it is an artefact (§3.4) |
| Zones | 21:18 · 22:5 · 23:9 · 24:15 · 25:3 · 26:18 · 28:3 · 29:8 = **79, all in-basin** |
| Mapping | **28 of 79 mapped** · 4 are BOCATOMA intakes → **24 calibration-safe** · 46 have **no coordinates** · 5 zone-29 discharge stations still unmapped |
| Paired SSC+Q | all: **103,283 d / 33 st** (clean 102,895) · mapped-28: 92,190 / 28 (91,981) · **safe-24: 73,265 / 24 (73,264)** |
| SSC–Q Spearman ρ | 33 stations ≥ 100 clean paired days: **median 0.340**, range **−0.019 … 0.715**; 3 stations at ρ ≈ 0 (§3.6) |
| **ENSO bridging stations** | 2011 vs 2015-16 **6** · 2009-10 vs 2011 **10** · **1997-98 vs 1999-2000 10** · 2009-10 vs 2015-16 6 |
| ENSO clean paired days | 1997-98 2,900 · 1999-2000 2,146 · 2009-10 2,818 · 2011 2,144 · 2015-16 2,773 · model window 15,036 |
| Mainstem anchor `21237020` | 54,035 km² = **21.0 % of basin** · Q med 1,103 m³/s · ρ 0.457 / 6,400 d · **293 / 261 / 279 / 91 / 0 d** across the five windows |
| Largest Cauca SSC station | `26247030` APAVI 37,808 km² — but **274 clean paired days, ρ 0.055** |
| Below Arrancaplumas | **no SSC anywhere**; outlet CALAMAR `29037020` (257,097 km², 6,954 m³/s) has **none** |
| 1996 zone-29 defect | 6 stations at **12.5×–304×** own other-year medians; basin-wide 1996 ratio **1.32** over 35 st |
| 06:00 splice | 2,788 raw rows / 1,394 station-days / **4 stations** / 16 vs 3 median decimal places |
| CS coverage | 275 station-days / 4 stations; **243 same-day CM overlaps** (242 at `24037360`): **CS/CM median 0.715, IQR 0.673–0.768** |
| Terminal-year collapse | SSC stations ≥ 1 d: 2015 **28** → 2016 **12** → 2017 **14** → 2018 45; **safe paired: 2016 = 4 st / 772 d, 2017 = 2 st / 376 d** |
| 2018 outside the forcing window | 45 SSC stations · 11 safe paired · **2,420 clean paired days** unusable until the forcing is extended |
| Verification | 22 pre-data smoke tests + 24 independent output checks + 14 date-module smoke tests, **all passing**; 25/25 file agreement between the two date detectors |
| Defects found in our own work | **3**: the vacuous `_corroborate_monotonic` cross-check, the `n_mean_days` corrupt-row omission, and 4 established figures corrected (§3.1, §3.4, §4.2, §4.6) |
| **Realistic performance bar** | **SSC KGE −0.26 … 0.44** (Fagundes et al. 2026, in-situ data, **25 years** of calibration) — we have 6 bridging stations and 9 forcing years |

**The two sentences to carry forward.** *First:* **prove the date format from the data before parsing
any DHIME export, and key the unit conversion off the `Unidad` column — one file in 365 was
day-first and one variable in two was kg/m³, and both failures are invisible to every plausibility
check the project owns.** *Second:* **the sediment data are good enough to calibrate 24 tributary
stations and to support a relative ENSO comparison across 6 bridging stations — they are not good
enough to state a basin sediment export, and the locked 2011-vs-2015-16 pairing is the weakest of
the four candidates on the network's own numbers.**
