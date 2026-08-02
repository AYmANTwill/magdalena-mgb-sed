# 17 — Discharge QC audit: consolidation, defects, adversarial verdicts and open items

The discharge counterpart to [doc 16](16_forcing_pipeline_audit.md): complete record of the
discharge consolidation + QC campaign, plus the closure of several doc-16 open items
(precipitation SNHT screening, the dry-fraction band, the 7 residual stations, and two
housekeeping fixes). Every major finding was either **adversarially re-verified from raw data by an
independent agent** (marked CONFIRMED) or cross-checked by multiple independent tests; findings that
did not survive scrutiny are in [§4 Checked and cleared](#4--checked-and-cleared), not hidden.

Read §3.1 first if you are picking this up cold: **the discharge data are largely fine — the
gauge→minibacia mapping is not**, and calibrating against it as-is would be worse than not
calibrating at all.

---

## 1 — Current state

| Component | State |
|---|---|
| Discharge daily (IDEAM DHIME) | **192 stations, 1,296,324 station-days, 1990–2018**, consolidated, structurally clean |
| Discharge inventory | 192 stations with name/dept/coords/minibacia/coverage — 26 lack coords, 33 lack a minibacia |
| Gauge→minibacia mapping | ❗ **Broken for ~half the network** — 79/159 testable gauges fail plausibility, 33 unmapped |
| Usable calibration gauges today | **80** (pass both plausibility tests); 5 mainstem anchors strictly monotonic |
| Discharge QC | 4 test batteries run (structure/value, specific discharge, network mass balance, SNHT) — diagnosis only |
| Precip SNHT screening (doc 16 §7.2 analogue) | 159/294 stations testable; **4 genuine breaks**, all inside 2009–2017 |
| Precip dry-band + residual-7 (doc 16 items 5–6) | **Closed** with per-station verdicts: repair 9–29 more, exclude 1 |
| Housekeeping (doc 16 items 7 + §9 note) | `regions.zip` guard added; nb11 radiation band widened to 15–22 (generator only, notebook not re-run) |
| **Phase B** | **Still blocked** — now by the gauge re-snap and the forcing fixes, no longer by "discharge never audited" |

No processed data file was modified by the QC work: all four discharge test batteries and both
precipitation screenings were diagnosis-only. The only edits were the two housekeeping code fixes
(§2.5).

---

## 2 — What was built

### 2.1 `src/build_discharge_gauges.py` — consolidation *(new)*

Consolidates all **45 DHIME discharge parts** (17 loose CSVs + 16 top-level zips + 12
`OMAR_CAUDAL/` zips; utf-8 with latin-1 fallback; accented/spaced filenames; recursive zip handling)
into:

- `data/processed/discharge_daily.csv` — `code,date,q_m3s,approval`; 1,296,324 station-days,
  1990-01-01…2018-12-31, 49.9 MB
- `data/processed/discharge_inventory.csv` — 192 stations with name, dept-from-filename, lat/lon,
  minibacia, coverage and value stats

Headline numbers: 2,443,316 raw rows → 1,296,324 after dedup; every raw row is
`Caudal medio diario` (no other `Parametro` existed to drop); 0 negative values; 0 zip failures;
0 schema anomalies; all 167 prior-inventory stations retained, +25 new from zip-only sources.
Station coverage for the ENSO contrast years: 104 stations with ≥200 days in 2011, 82 with
≥400 days in 2015–16.

The approval-priority rule (`Definitivo > En revisión > Preliminar`) is implemented but **never had
to arbitrate** — see §4.1.

### 2.2 Discharge QC test battery *(diagnosis only)*

| Test | Method | Headline result |
|---|---|---|
| Structure + value QC | NaN/negative/duplicate scan, timestamp scan, flatline runs, zero runs, year-median jumps, dry-season completeness, approval mix | Dataset structurally clean; defects are flatlines (§3.3), one splice (§3.4), fabricated zeros (§3.5) |
| Specific-discharge plausibility | Upstream area by reverse-BFS over `minibacias.csv`; runoff coefficient vs per-minibacia forcing precip; neighbour q_spec ratio | **79/159 testable gauges fail** — mapping defect, not data defect (§3.1) |
| Network mass balance | 159 direct nested gauge pairs on the 8,672-minibacia topology; Q_down < 0.95·Q_up violation fractions; mainstem monotonicity | Clean pairs near-perfect (median violation frac 0.0016); all gross violations trace to mapping, intakes, or distributaries |
| SNHT homogeneity | Monthly log-Q, climatol-style 6-neighbour 1/d² reference, Alexandersson 1986 | 24 strong break candidates (Tmax>50), 12 inside 2009–2017 (§3.8) |

Sanity anchor used throughout: outlet gauge CALAMAR `29037020` accumulates to **257,097 km² = the
full basin**, and its mean flow gives ~880 mm/yr specific runoff — the accepted value for the
Magdalena at Calamar. The area-accumulation method is sound; the per-gauge assignments are not.

### 2.3 Precipitation SNHT screening *(closes the doc 16 §7 "apply the same scrutiny" mandate for precip homogeneity)*

Climatol methodology on the 294 repaired gauges: monthly totals (≥25 days/month, `Inferido_seco`
counts as present), ratio-normalised, 6-nearest-neighbour 1/d² reference, flag Tmax>25. 159 stations
had ≥60 valid months; 135 short records untestable. Monte-Carlo null (n=130, 20k sims): T95=7.8,
T99=11.2, P(T>25)≈0 — **expected false flags 0.00 of 159, so every flag is a real signal.**

Result: 5 raw flags → **4 genuine breaks** after climatol-style iteration (one was reference
contamination, §4.6). All 4 fall inside 2009–2017. Two are incomplete repairs of zero-suppressed
stations, two are raw DHIME inhomogeneities the zero-suppression QC structurally could not see
(§3.9).

### 2.4 Dry-band sensitivity + residual-7 verification *(closes doc 16 open items 5 and 6)*

CHIRPS-based per-station adjudication of (a) the 49 unflagged stations with dry_frac in
[0.15, 0.30), and (b) the 7 stations still >1.8× neighbours after repair. Calibration set: 44
healthy stations give station/CHIRPS median 1.076, IQR 0.93–1.18, q95 1.49 — so the ">1.5× own
CHIRPS pixel" gate has a 4.5 % false-positive rate. Verdicts in §3.10.

### 2.5 Housekeeping *(the only code edits)*

- **`regions.zip` glob bug (doc 16 §3.1 / item 7) — fixed.** `src/organize_precip_regions.py` now
  skips any zip whose normalised department name is empty or `regions`, so a re-run can no longer
  ingest its own output archive as a phantom `regionszip` department with 98 duplicate CSVs.
  Verified by re-read + `py_compile`. If a `regions/regionszip/` directory already exists from a
  past run, it must be deleted manually — nothing was deleted.
- **nb11 radiation sanity band (doc 16 §9 warning) — fixed in the generator.** The printed band and
  the markdown prose now read **15–22 MJ/m²/day** with a note that cloudy tropical basins sit at the
  low end (clear-sky tropics 18–22), so the corrected 17.2 no longer reads as a failure. The
  notebook itself was **not regenerated or executed** — that regeneration is an open item (§5).

---

## 3 — Discoveries (verified)

Each major finding carries a verdict: **CONFIRMED** = independently recomputed from raw data by an
adversarial verification agent, or mechanism directly reproduced; **UNCERTAIN** = evidence points
one way but a benign explanation survives. REFUTED findings are in §4.

### 3.1 The gauge→minibacia mapping is physically impossible for ~half the network ❗ *the significant one* — **CONFIRMED, CRITICAL**

**37 mapped stations have impossible specific runoff (4 to 652,196 mm/yr); 54 fail the water
balance (RC≥1 or RC≤0.1); 79 of 159 testable stations fail at least one plausibility test; 33 more
have no mapping at all. 34 of the 37 impossible-runoff stations are flagged `representative=True`
in `gauge_minibacia.csv`.**

Adversarial verification independently re-parsed all 45 raw files, rebuilt upstream areas by
post-order accumulation over `minibacias.csv` (exactly one outlet, id 2470, total 257,097 km²) and
reproduced the finding exactly.

Flagship cases, all three tests agreeing:

| Station | Q | Mapped area | Implied runoff | Reality |
|---|---|---|---|---|
| `25027360` ARMENIA | 2,836 m³/s | **137 km²** | 652,196 mm/yr | Magdalena mainstem (Brazo de Loba) |
| `23187280` SITIO NUEVO | 3,501 m³/s | 249 km² | RC = 163 | mainstem |
| `25027270` LAS FLORES | 2,356 m³/s | 14,774 km² | — | true area ≈ 257,000 km² |
| `26217040` CANGREJO | 4.1 m³/s | 31,842 km² | **4 mm/yr** | creek on a mainstem minibacia |
| `25027420` LA VICTORIA | 368 m³/s | 161,792 km² | 72 mm/yr | minor Brazo de Mompós arm |
| `23177060` ALTAMIRA | 264 m³/s | 85,990 km² | — | upper-Magdalena gauge, true ≈ 10,000 km² |

**Mechanism confirmed:** sampling `data/processed/minibacias.tif` at each gauge's stored lon/lat
reproduces the assigned minibacia for **133/159 stations** — the mapping is a point-in-cell raster
snap with **no drainage-area consistency check**. One cell (~0.05°) of coordinate error moves a
mainstem gauge into a small lateral minibacia (RC explodes) or a tributary gauge onto the mainstem
cell (RC collapses) — exactly the observed bidirectional failure. The 26 stations that do not even
match the cell at their own coordinate indicate a second, inconsistent assignment step.

The errors are **bidirectional and 3×–500×**, which pins the defect on the *area assignment*, not
the discharge: mainstem flows in tiny minibacias and creek flows in mainstem minibacias. Flags
scatter across all 40 raw source files and all 16 departments — no ingest cluster.

**Why it corrupts calibration outright:** MGB would tune runoff generation and routing of a 137 km²
catchment to reproduce 2,836 m³/s. It also propagates: the network mass-balance test shows the
mis-mappings contaminate **81 of 159 nested gauge-pair tests**, and 2 concrete tributary→mainstem
mislabels were localised — CARTAGO AUT `26127040` carries Río La Vieja flow (73.6 m³/s) but sits on
a Cauca mainstem minibacia (17,319 km²), and PTO TEJADA-AUT `26027010` carries Río Palo flow
(23.7 m³/s) on a 7,400 km² Cauca minibacia; the next pair downstream jumps ratio 9.63, confirming
the diagnosis.

**Where the mapping is sound, the data are excellent** — see §4.2. The fix is re-snapping by
drainage-area matching (search minibacias within a few km of the coordinate, pick the one whose
accumulated area best matches the IDEAM catalogue area or the Q-implied area at ~27 l/s/km²), then
rebuilding `gauge_minibacia.csv` and re-running all three network tests.

### 3.2 Lower-Magdalena distributaries (brazos) are structurally unrepresentable — **CONFIRMED (structural, not a data error)**

6/7 bolívar and 3/3 magdalena stations fail plausibility — the only geographic cluster. These sit
on Brazo de Loba / Brazo de Mompós distributaries where the river bifurcates; `minibacias.csv` is
single-downstream (D8), so upstream-area accumulation *cannot* allocate split flow: EL BANCO
`25027020` (mainstem) accumulates only 22,585 km² because the BFS follows one arm; LA VICTORIA
`25027420` carries partial brazo flow but is assigned the near-full basin. **No re-snapping fixes
these — the topology itself cannot represent bifurcating flow.** The COYONGAL→BARBOSA pair shows a
persistent ~8 % loss (median ratio 0.924 over 8,559 common days), plausible Momposina ciénaga
exchange on top of the splits.

Affected: `25027360, 25027400, 25027530, 25027620, 25027930, 25027020, 25027270, 25027420,
23187280, 23217030`. Exclude from area-normalised calibration, or treat as fractional-flow
observations with externally specified split ratios. Calibrate the reach against full-river
stations only (CALAMAR `29037020`: median 6,954 m³/s, 27 l/s/km² — plausible).

### 3.3 Flatline (stuck/infilled) runs at 113 stations — **CONFIRMED**

Adversarial recomputation reproduced **every claimed number exactly**: 113/192 stations have ≥1 run
of ≥10 identical consecutive daily values; 21,064 flat days (1.6 % of all rows); 68 runs ≥30 d at
35 stations, of which **30 runs at q > 1 m³/s across 17 stations — physically impossible for a
natural river**: `24037510` frozen 89 d at 26.48 m³/s (2007) and 42 d at 122.6 m³/s (1997);
`21107030` 76 d at 3.10; `25017010` 34 d at 44.66. Worst by share of record: `26087100` 32.8 %,
`21217230` 24.6 % (one 148-d run of 0.0, §3.5), `21047040` 20.0 %, `26017040` 14.5 %, `24037300`
14.1 %.

Caveat (verified): for low-flow stations `26087100`/`21047040` (medians 0.45/0.28 m³/s, 107/285
distinct values) part of the effect is coarse rating-table quantisation — but ≥30-d runs at q>1
cannot be. **Mask flatline runs ≥10 d as missing before computing calibration statistics**;
flatlined segments deflate variance and corrupt low-flow signatures exactly like infilled data.

### 3.4 Station `23017020` (BOCATOMA): a 2003–2004 block ~35× above baseline — **CONFIRMED**

Yearly medians: 1990–2002 range 0.23–0.64 m³/s; **2003 = 15.62 (n=332), 2004 = 17.06 (n=364)**;
2005–2018 back to 0.22–0.66. Adversarial verification recomputed from `caudal_tolima.csv` (the zip
copy is byte-identical, so no join artefact) and rejected the benign explanations: across 115
stations the median 2003-04/surrounding-years ratio is **0.89** (slightly dry — the target's 35.4×
is the dataset maximum), and full-year coverage rules out seasonal sampling. Not a 1000× l/s slip
(35×). It looks like two years of another station's record — or a differently scaled rating —
spliced in. **Exclude 23017020's 2003–2004 (697 days) from any use.**

### 3.5 Fabricated zero-flow records — **CONFIRMED**

658 zero days at 18 stations, individually adjudicated:

- `21217230` (BOCATOMA, 131.7 km²): 297 zero days, **all in 1998**, including one unbroken
  **148-day run from 1998-06-06 spanning the wet season of a strong La Niña year**; its other years
  have medians 0.82–1.39 m³/s and zero q=0 days. Instrument/diversion outage recorded as 0, not
  drought. Adversarially reproduced to the day.
- `24017670` (AMARILLO EL): 213/1004 days = **21.2 % zeros**.
- The 3 zero-reporting stations with nominal area >5,000 km² (`26077060`, `28037020`, `24057080`)
  all have impossible specific runoff (17/15/41 mm/yr) — their areas are snap errors (§3.1), so
  "mainstem zero" cannot be confirmed. Remaining zero stations are 100–3,210 km² where intermittency
  or intake diversion (several literally named BOCATOMA) is plausible.

**Treat 21217230's 1998 zeros and 24017670's zeros as missing, not as zero flow.**

### 3.6 Intake and canal stations are in the gauge set as if they were rivers — **CONFIRMED (by name + mass balance)**

12+ stations are literally named BOCATOMA or CANAL — they gauge diversion works. They produce
exactly the persistent mass-balance violations expected: BOCATOMA RIO PALO → CANAL PALO violation
frac 0.715 at area ratio 1.009; BOCATOMA-FLORIDA → PUENTE CARRETERA frac 0.984, ratio 0.204; and
several also fail specific runoff (`24017900` BOCATOMA ARRIBA: 0.26 m³/s on 2,973 km²). **Tag
station type from name/metadata and exclude intake/canal stations from the calibration set** (or
use them only as evidence for abstraction terms).

### 3.7 Chicamocha canyon mass-balance deficits — **UNCERTAIN**

CAPITANEJO `24037390` → CEPITA `24037500`: median ratio 0.757 while area grows 1.42× (violation
frac 0.663, 623 common days). PAZ DE RIO `24037510` → PLAYA LA `24037280`: ratio 0.601, frac 0.586,
1,291 days. Irrigation and the Acerías Paz del Río intake exist in this semi-arid canyon, but a
persistent 24–40 % median loss while drainage area grows 42 % exceeds plausible abstraction — yet
cannot be ruled out from this data. `24037300` PUENTE COLONIAL (0.20 l/s/km²) sits between pairs
with ratios 0.078 and 42.1 — station-level data or mapping fault. **Inspect rating curves and
periods before using any Chicamocha gauge; if the deficits are real, represent abstraction
explicitly or exclude the reach.**

### 3.8 SNHT: 24 strong discharge break candidates, 12 inside 2009–2017 — signal robust, attribution **UNCERTAIN** pending metadata

146/192 stations screenable (22 qualifying stations lack coordinates). 82 exceed Tmax>25, but the
neighbour-difference series have median lag-1 autocorrelation **0.58**, inflating T by roughly
2–4× — so the **Tmax>50 tier (24 stations) is the action list**, and 12 of those break inside the
calibration window, with neighbour-relative shifts of −65 % to +88 %. Most damaging if used
uncorrected: PALMARIGUANI `28047050` (−65 % at 2013-06), SAN PEDRO-AUT `25017020` (+72 % at
2009-04), MAJADAS-AUT `23197700` (+88 % at 2016-11).

Two verified physical (not instrumental) cases: **mirrored opposite-sign break pairs at channel
bifurcations** — COYONGAL `25027930` (+14 %) and ARMENIA `25027360` (−12 %), 10.7 km apart, both
break 2010-03 at the onset of the 2010 La Niña floods (flow redistribution between arms conserving
total flow); same signature at the BOCAS twins `22017010`/`22017030` (2005-02, −35 %/+41 %). Do not
"correct" these records — model the combined flow of both arms or calibrate post-2010 only.

### 3.9 Precipitation: two zero-suppression repairs manufactured fake droughts; two raw breaks passed all QC — **CONFIRMED**

The SNHT screening (§2.3) found the doc-16 repair broadly sound (§4.7) but exposed 4 stations, all
breaking inside 2009–2017:

| Station | Break | Shift vs neighbours | Diagnosis |
|---|---|---|---|
| `21105030` ALGECIRAS-AUT | 2012-06 | **−84 %** | ❗ **Repair-manufactured drought.** After 2012-06 the raw record stopped reporting rain days almost entirely; the repair infilled the dead period as `Inferido_seco` (fraction 0.41 → **0.89**) instead of leaving it missing. 5.5 yr at ~200 mm/yr (neighbours ~1,433) — an artificial **87 % rainfall deficit** injected into the forcing around Algeciras for most of the calibration window. |
| `24050110` ALBANIA | 2011-02 | +194 % | Same mechanism, mirrored: the 2008…2011-01 segment lost rain days too; dry-day infill halved apparent rainfall (832 vs neighbours' 2,407 mm/yr). Post-break record is consistent with neighbours — keep it. |
| `26210070` CAICEDO | 2010-01 (at search bound — true break anywhere 2008…2010-01) | −68 % | Raw DHIME inhomogeneity: never suppressed, zero infill — 3,234 → 819 mm/yr while neighbours barely move. Invisible to the zero-suppression QC by construction. 96 suspect months inside the window. |
| `29030040` ARJONA | 2011-04 | +191 % | Raw inhomogeneity: pre-2011-04 under-catches ~half vs flat neighbours — exactly through the 2010-11 La Niña peak that flood calibration needs. |

The 2010–2012 clustering is **not** a climate regime (§4.5): the shifts are station-specific,
opposite-signed and huge — plausibly network disruption during the *ola invernal* emergency.
Repair-guard lesson: **never infill dry days in months where most neighbours report rain, and flag
any segment with infill fraction > ~0.6.**

### 3.10 Precipitation dry band and residuals: the 0.15 threshold missed 9–29 stations; one station is defective — **CONFIRMED (per-station), magnitudes bracketed**

Verdicts for the 49-station dry-frac [0.15, 0.30) band (doc 16 item 6):

| Verdict | n | Basis |
|---|---|---|
| **Repair** (full rubric: >1.4× neighbours before, 0.7–1.4× after, >1.5× own CHIRPS pixel) | **9** | e.g. `22050070`: 5,587 mm/yr = 1.67× neighbours, 2.68× CHIRPS; repaired 2,820 = 0.84×/1.35× |
| Repair-lean (CHIRPS-corroborated; neighbour test blinded by already-suppressed neighbourhoods, mean 33 % suppressed members) | 20 | ch_before 1.60–3.79, repaired lands at CHIRPS median 1.04 |
| **Leave alone** — repair would wrongly dry them to ~0.83× CHIRPS | 13 | validates keeping a confirmation test rather than raising the threshold unconditionally |
| Uncertain — span_frac ~0.39, global span-correction overshoots patchy records | 7 | inspect monthly gap structure; repair only months with the wet-day-only signature |

Aggregate effect of acting: station-population mean −1.96 % (~−43 mm, conservative 9 repairs + 1
exclusion) to −6.88 % (~−152 mm, CHIRPS-lean 29 repairs) on the 2,206 mm/yr basin mean.

Residual-7 verdicts are in §4.4 (six cleared). The seventh, **`26100670` GITANA LA, is defective —
exclude or cap**: no CHIRPS maximum at its location (pixel 1.12× neighbours' pixels), yet the
already-repaired gauge is **2.18× its own pixel** (healthy q95 = 1.49, max 1.97) and 1.71×
neighbours as-delivered. At 2,783 m in the Cauca headwaters it would locally inflate IDW rainfall
by ~70–120 %.

Side discovery: recomputing the neighbour ratio on **effective** (as-delivered) values exposes
**24 stations >1.8×, 23 of them >1.5× their own CHIRPS pixel — 11 outside both audit items**
(worst `29060170`: 6,120 mm/yr = 4.13× neighbours, 5.07× CHIRPS). The one-pass neighbour test
compared pre-repair vs pre-repair; lowering 70 stations exposed this tier. Iterate the neighbour
test once on post-repair values.

### 3.11 The repair report's `ratio_after` metric overstates residuals — **CONFIRMED (reproduced to the mm)**

`nbr_ann_after` was computed from *hypothetical* span-corrected annuals of **all** stations,
including the 224 never-repaired ones whose delivered data remain at `ann_before`. On the
as-delivered basis the residual ratios drop from 1.81–2.66 to 1.21–2.14 — 3 of the "7 residual
>1.8× stations" were never actually >1.8× in the dataset the model ingests (§4.4). Fix
`src/repair_precip_zero_suppression.py` to benchmark against effective neighbour values.

### 3.12 Traps for whoever picks this up

- **Approval level carries no screening power for discharge.** 90.6 % of all rows are *Preliminar*;
  182/192 stations are >80 % Preliminar, 93 are 100 %. Using it as an exclusion criterion would
  discard ~91 % of the data. The one full *En revisión* year (365 rows at `26017040`) coincides
  with that station's 14.5 % flatline share — treat with caution. (Contrast doc 16 §6.2, which
  describes precip as mostly *Definitivo*.)
- **The day-window is still an assumption.** All 2,443,316 raw `Fecha` stamps are `00:00` and
  `Parametro` is uniformly `Caudal medio diario` — consistent with a midnight→midnight calendar-day
  mean, but the averaging window cannot be proven from the export. Precip runs 07:00→07:00
  (*día pluviométrico*), so daily rain–runoff pairing carries an inherent ~7 h (effectively up to
  1-day) phase offset no processing step can remove. Allow ±1 day slack in event-scale lag
  analysis; immaterial at monthly aggregation.
- **Rating-table quantisation mimics flatlining at low-flow stations** (§3.3 caveat) — check the
  distinct-value count before condemning a station.
- **Departmental DHIME downloads spill across the basin divide**: 14 out-of-basin stations
  (Orinoco zone 35 ×8, Catatumbo 37 ×1, Pacific 53/54 ×5) are in the consolidated table. Filter
  `code[:2]` in 21…29 before basin-wide statistics, mirroring `build_precip_gauges.py`.
- **One 10-digit code**: `2319700100` (PIEDECUESTANA, new-format DHIME id), 214 days in 2018 only —
  fails any coverage threshold; no ingest action needed.
- **SNHT on autocorrelated difference series over-flags** (lag-1 r = 0.58 → T inflated 2–4×): use
  the Tmax>50 tier, never auto-homogenise at Tmax>25. And a dominant nearest neighbour can mirror
  its own break into a healthy station's flag (§4.6) — iterate climatol-style before trusting a
  flag.

---

## 4 — Checked and cleared

Findings that did not survive verification, plus deliberate non-issues — recorded so nobody
re-chases them.

### 4.1 The 1.1 M duplicate rows are benign — **REFUTED as a data conflict**

1,130,236 duplicate `(code,date)` groups among 2,443,316 raw rows (same departments downloaded as
both .csv and .zip; valle three times). Groupby on raw strings: **0 groups with more than one
distinct `Valor` and 0 with more than one `NivelAprobacion`** — byte-identical re-exports. The
priority rule never had to arbitrate.

### 4.2 The discharge values themselves are sound — no unit slips, near-perfect internal consistency

- **No l/s-as-m³/s slips**: 0 days fall 500–2000× their 31-day local median (max anywhere = 151×);
  basin max 14,909 m³/s at CALAMAR is plausible.
- The 80 stations passing both plausibility tests are textbook-healthy: q_spec median
  **26.8 l/s/km²** (IQR 15.8–33.8, p5–p95 7.0–57.1, max 74.9 — the physics band with a wet-Andean
  tail), RC median 0.435, max **0.908 < 1**, consistent with P ≈ 2,206 mm/yr minus PET.
- The 76 mass-balance pairs whose gauges both have plausible runoff: median violation fraction
  **0.0016**, log-log correlation of Q-ratio vs area-ratio **0.894** (vs 0.402 over all pairs).
- After excluding mis-mapped gauges, the mainstem chain is **strictly monotonic**:
  60.7 → 558.7 → 1,103 → 2,589 → 6,954 m³/s (raw chain had 3 gross inversions, −95.8 % to −98.7 %,
  all at mis-mapped gauges). The 5 anchors: `21017030, 21137050, 21237020, 23157080, 29037020`.

Violations elsewhere are mapping/station-type artefacts, not systematic data corruption.

### 4.3 The precip-style dry-season selective-reporting defect has no discharge analogue — **cleared**

Month-of-year completeness (dry-3 vs wet-3 months) flags only **2 of 192** stations with a >25-pt
gap: `23177060` ALTAMIRA (42.6 pts, short span) and `28037020` HACIENDA CONVENCIÓN (40.5 pts). The
systematic suppression that hit 70 precip stations is nearly absent from discharge. Down-weight
those 2 for mean-flow/low-flow signatures; no dataset-wide correction.

### 4.4 Six of the seven residual precip stations — **cleared** (doc 16 item 5 closed for 6/7)

- **3 genuine orographic hotspots**: `24015280` GÁMBITA (own CHIRPS pixel 2.19× neighbours'
  pixels), `24025030` LA SIERRA (1.99×), `24011070` SANTUARIO (1.38×) — and their gauge/own-pixel
  ratios sit inside the healthy envelope. Keep; candidates for the v2 orographic correction.
- **3 metric artefacts**: `2125500032` MARIQUITA, `23015040`, `23060370` — as-delivered ratios are
  only 1.21–1.35 (the reported 1.81–1.97 came from the hypothetical benchmark, §3.11). They were
  never actually >1.8× in the forcing dataset. Keep, no action.
- The seventh (`26100670`) is *not* cleared — §3.10.

### 4.5 "The 2010–11 La Niña explains the breaks" — **REFUTED, twice**

- Discharge SNHT: max basin-wide break co-occurrence 5 % of stations within ±6 months (2005); max
  department-level 18 %; the 2010-01…2011-12 window holds only 7 % — all far below the
  pre-registered 30 % regime threshold. Breaks are gauge-level (ratings, moves, diversions).
- Precip SNHT: the 4 genuine breaks cluster in 2010–2012 but are opposite-signed and 68–194 %
  neighbour-relative — no regional climate shift produces that, and the neighbour-difference method
  cancels common-mode signals by construction. No basin-wide regime adjustment is warranted.

### 4.6 SANTA BÁRBARA FINCA `21100070` is homogeneous — **REFUTED as a break**

Its Tmax=36.7 flag at exactly 2012-06 is contamination from ALGECIRAS `21105030` (10.5 km away,
carrying **76 %** of its 1/d² reference weight). Own record stable (−4 %). Removing the 4 confirmed
bad stations from all neighbour pools drops it to Tmax=11.0; `23155030` and `24050060` deflate the
same way. The repair *worked* at this station.

### 4.7 The zero-suppression repair itself is sound — **cleared, with two exceptions**

55/57 tested repaired stations are homogeneous (median Tmax 5.5 vs 4.5 for never-suppressed) — no
systematic residual inhomogeneity from the repair. The 2 failures (§3.9) share one mechanism the
repair cannot fix: segments where rain days were lost too. 13 repaired stations were too short to
test — untested is not certified clean.

### 4.8 The 2.5 % precip break rate vs Jupin et al.'s 17 % — **not a contradiction**

Constant break-hazard scaling of 17 % per ~60-yr record to our 11-yr window predicts 3.1 % —
matching the 3.1 % raw / 2.5 % genuine observation. SNHT power scales with n: with 132 months a
break needs ~2.3× the shift to reach the same T, so 60-yr studies catch 5–15 % relocation breaks
that are invisible here. Do not read the low rate as a cleaner network.

---

## 5 — Open items, ranked by whether they block Phase B

### 5.1 Station disposition before calibration *(the plain-language answer)*

**Discharge — usable now:** the **80 stations** passing both plausibility tests, with flatline runs
≥10 d masked as missing. Primary anchors: the 5 monotonic mainstem gauges `21017030, 21137050,
21237020, 23157080, 29037020` (CALAMAR).

**Discharge — exclude until the re-snap (mapping, not data):** the 79 plausibility-flagged
stations and the 33 unmapped ones. Most return to service once `gauge_minibacia.csv` is rebuilt.

**Discharge — exclude structurally / permanently:**

| Stations | Why |
|---|---|
| Brazo/distributary gauges `25027360, 25027400, 25027530, 25027620, 25027930, 25027020, 25027270, 25027420, 23187280, 23217030` | D8 single-thread topology cannot represent bifurcating flow (§3.2) — no re-snap fixes them |
| BOCATOMA/CANAL intake stations (12+, e.g. `26047100, 26017110, 26017030, 21217230, 21217250, 24017900, 26137110, 26137170`) | They gauge diversion works, not rivers (§3.6) |
| `28037020` HACIENDA CONVENCIÓN | Fails four independent tests: median steps, seasonal gap, zeros on mis-assigned area, 9 % flatline |
| `2319700100` | 214 days in 2018 only; fails any coverage threshold |
| 14 out-of-basin stations (zones 35/37/53/54) | Outside the Magdalena–Cauca divide (§3.12) |

**Discharge — repair (mask segments, keep the station):** `23017020` drop 2003–2004 (697 days,
§3.4); `21217230` 1998 zeros → missing; `24017670` zeros → missing (§3.5); all stations: flatline
runs ≥10 d → missing (§3.3); the 12 strong in-window SNHT breaks — restrict to the homogeneous
sub-period or exclude after a metadata check (§3.8); COYONGAL/ARMENIA — calibrate post-2010 or as
combined-arm flow.

**Precipitation — before rebuilding the forcing grid:** revert the `Inferido_seco` infill at
`21105030` from 2012-06 (leave missing); mark `24050110` 2008-01…2011-01 missing; distrust/drop
`26210070` from 2010-01 (CHIRPS cross-check first); mark `29030040` 2008-01…2011-03 missing;
**exclude `26100670` GITANA LA** (or cap to the neighbour envelope ~1,390–2,150 mm/yr); repair the
9 rubric band stations (and decide the 20 CHIRPS-lean ones); repair-or-exclude the 11 new >1.8×
effective stations; leave the 13 "leave-alone" band stations untouched.

### 5.2 Blocking Phase B

1. **Re-snap every gauge to its minibacia by drainage-area matching** (§3.1) and rebuild
   `gauge_minibacia.csv`; then re-run the specific-discharge, mass-balance and neighbour tests.
   Expect >90 % of pairs below violation frac 0.05. Nothing downstream of the mapping can be
   trusted until this is done. Classify the distributary gauges out (§3.2) rather than re-snapping
   them.
2. **Apply the precipitation fixes and re-export the forcing** (§5.1): 4 SNHT segment exclusions,
   GITANA LA, the 9(–29) band repairs, then re-run notebook 11 (IDW + LOOCV) and re-export
   `forcing_minibacia_precip.csv`. The ALGECIRAS fake drought alone injects an 87 % local deficit
   across most of the calibration window.
3. **Apply the discharge masks/exclusions** (§5.1) as a scripted, reproducible step (a
   `discharge_daily_qc.csv` or a mask file) — not ad-hoc notebook filtering.
4. **Day-convention offset** (carried from doc 16 §4.2): rainfall 07:00→07:00 vs discharge
   (assumed) midnight→midnight. Resolve or explicitly absorb with ±1 day slack before calibrating
   hydrograph timing, or routing/recession parameters will eat a ~7 h error and look well-calibrated
   for the wrong reason.

### 5.3 Not blocking, worth doing

5. **Coordinates for the 11 new in-basin zip-gained stations** (extend
   `src/fetch_station_coords.py`), then include them in the re-snap. Currently 0 of the 25
   zip-gained stations are usable.
6. **Decide the 7 zone-29 delta gauges** (Canal del Dique / Fundación area): snap if the model
   covers the delta, or document exclusion — do not leave them silently unlinked.
7. **Metadata check for the SNHT Tmax>50 discharge stations** (rating-curve history around each
   break date) and for the Chicamocha reach (§3.7).
8. **Iterate the precip neighbour test once on post-repair effective values** with CHIRPS
   corroboration (§3.10), and fix the `ratio_after` benchmark in
   `src/repair_precip_zero_suppression.py` (§3.11). Add the repair guard (infill fraction > 0.6 ⇒
   flag; never infill against raining neighbours).
9. **Inspect the 7 uncertain band stations' monthly gap structure** before repairing or excluding
   (§3.10).
10. **Resolve multi-gauge minibacias** (6 minibacias hold 2–3 gauges each — up/down order undefined)
    and the 2 nested pairs with zero common days.
11. **Regenerate and execute notebook 11** from the updated generator so the 15–22 radiation band
    ships in the actual notebook (§2.5).
12. **Re-screen the 13 short repaired precip stations against CHIRPS** (too short for SNHT), and
    CHIRPS-check the two near-misses `21170040` / `23120240`.

---

## 6 — Key numbers

Consolidation and QC, as of this audit. Diagnosis-only: none of these numbers changed any processed
file yet.

| Quantity | Value |
|---|---|
| Raw parts / rows ingested | 45 files (17 CSV + 16 zip + 12 OMAR zip) / 2,443,316 rows |
| Consolidated | **192 stations, 1,296,324 station-days, 1990–2018** (322,644 in 2009–2017) |
| Dedup | 1,146,992 rows removed, **0 value / 0 approval disagreements** |
| Structure | 0 NaN, 0 negative, 0 duplicate `(code,date)`; inventory recomputation: 0 mismatches |
| Timestamps | 2,443,316/2,443,316 at `00:00`; `Parametro` uniformly `Caudal medio diario` |
| Approval mix | Preliminar **90.6 %** · Definitivo 9.3 % · En revisión 367 rows |
| Coverage (ENSO years) | 104 stations ≥200 d in 2011 · 82 stations ≥400 d in 2015–16 |
| No coords / no minibacia / out-of-basin | 26 / 33 / 14 stations |
| Mapping test | 159 testable → **79 flagged** (72 neighbour, 54 RC, 47 both) → **80 pass** |
| Impossible runoff | 11 stations >4,000 mm/yr (max **652,196**) · 26 stations <100 mm/yr (min **4**) |
| Snap mechanism | raster cell at gauge coordinate reproduces mapping for **133/159** |
| Healthy subset | q_spec median **26.8 l/s/km²** (p5–p95 7.0–57.1) · RC median 0.435, max 0.908 |
| Mass balance | 76 clean pairs: median violation frac **0.0016**, log-log r **0.894** (all pairs: 0.402) |
| Mainstem chain | raw 3 inversions → **0 after exclusions**: 60.7 → 558.7 → 1,103 → 2,589 → 6,954 m³/s |
| Outlet sanity | CALAMAR `29037020`: 257,097 km², ~880 mm/yr specific runoff — the accepted value |
| Flatlines | 113 stations · 21,064 days (1.6 %) · 68 runs ≥30 d · **30 runs ≥30 d at q>1 m³/s** |
| Zeros | 658 days at 18 stations; worst: 148-d run in La Niña 1998 (`21217230`) |
| Splice | `23017020` 2003–04 at 33.1× baseline (n=696; dataset max; neighbours at 0.89×) |
| Discharge SNHT | 146 screened · 82 Tmax>25 (inflated, lag-1 r=0.58) · **24 Tmax>50** · 12 in-window |
| Break clustering | max 5 % basin-wide / 18 % department — vs 30 % regime threshold: **no regime** |
| Precip SNHT | 159/294 tested · 4 genuine breaks (2.5 %) · MC null: T99=11.2, expected false flags **0.00** |
| Worst precip artefact | ALGECIRAS `21105030`: 5.5 yr at ~200 mm/yr vs neighbours ~1,433 (**−87 %**, infill frac 0.89) |
| Dry band (49 stations) | repair 9 · repair-lean 20 · leave 13 · uncertain 7 |
| Healthy gauge/CHIRPS envelope | median 1.076 · IQR 0.93–1.18 · q95 1.49 (44 stations, 3,287/3,287 valid days each) |
| New >1.8× effective tier | 24 stations (23 CHIRPS-corroborated), **11 outside both audit items** |
| Basin-mean effect of precip fixes | **−1.96 %** (~−43 mm, conservative) to **−6.88 %** (~−152 mm, CHIRPS-lean) on 2,206 mm/yr |
| Calibration-ready discharge gauges | **80 of 192** today; most flagged ones recoverable by the re-snap |

The single sentence to carry forward: **the IDEAM discharge series are internally consistent almost
everywhere the plumbing is right — fix the gauge→minibacia plumbing and the forcing artefacts before
letting MGB see any of it.**

## Update: the gauge→minibacia plumbing is fixed

`src/fix_gauge_minibacia_mapping.py` re-snaps every gauge whose current mapping gives an implausible
runoff coefficient (RC = annual Q volume ÷ annual rainfall volume over the assigned upstream area) by
searching minibacias within an expanding radius (3→20 km) of the gauge coordinate and picking the one
whose RC is closest to the fleet's healthy median (0.435). The ten Brazo de Loba / Mompós
distributary stations are excluded, not remapped — no re-snap can fix a topology that cannot
represent a forking channel.

| | Before | **After** |
|---|---|---|
| Stations with RC outside [0.03, 1.2] (severe) | 20 | **0** |
| RC inside [0.1, 1.0] (QC clean-station band) | 105/149 | **120/149** |
| RC inside [0.137, 0.724] (5–95% healthy band) | 87/149 | **99/149** |
| Median RC (non-distributary) | 0.364 | 0.397 |

20 stations remapped (median move 4.9 km — consistent with the "one raster cell off" mechanism the QC
identified), 129 already plausible and left untouched, 10 excluded as distributaries. Examples:
CANGREJO EL `26217040` RC 0.002 → 0.426; BUCHITOLO `26077060` RC 0.008 → 0.896; BOCAS `22017030`
RC 0.022 → 0.629.

`data/processed/gauge_minibacia.csv` is updated in place (backup at
`gauge_minibacia_ORIG_backup.csv`); `gauge_minibacia_remap_report.csv` records every station's
before/after RC and the action taken (kept / remapped / excluded_distributary), so any downstream
user can audit exactly which mapping changed and why.
