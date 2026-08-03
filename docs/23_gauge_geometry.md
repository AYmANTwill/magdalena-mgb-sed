# 23 — Gauge and interpolation geometry

Split out of [doc 18](18_hydrology_journal.md) §11–§13 when that document passed 65 KB.
One coherent topic: **where the gauges are, which minibacia each drains, and how their
values reach the model** — as distinct from doc 18 §9–§10, which is about how much water
the gauges report.

Section numbers are kept as §11–§13 so every cross-reference written before the split still
resolves.

Headline findings:

| | |
|---|---|
| §11 | The IDW was **order-dependent** — shuffling gauge columns moved up to 83 minibacias by 20.5 mm/day. Fixed with a lexsort tie-break, proven by a shuffle test. Four co-located pairs classified by evidence: 2 duplicates and 1 sequential replacement merged, 1 refused as a **coordinate error** |
| §12 | The 14 residual energy-floor gauges triaged: **2 exclude, 2 keep, 10 down-weight**. Only 2 of 14 are our forcing's fault; 8 of 14 have no rating curve at all |
| §13 | The rc-reference **circularity charge is refuted** (Levene p = 0.76), cancelling a pre-authorised re-snap. But catchment areas are **unreliable per gauge in both implementations** — 31 of 85 shared gauges differ by more than 2× |

---

## 11 — Phase 0: the IDW blocker (open item 11 closed)

New module `src/idw_forcing.py`, extracted from nb11 §3 so that the notebook, the
diagnostics and any re-run share **one** interpolator instead of three copies. It fixes the
two defects §10.7 found, which turned out to need different fixes.

### 11.1 Order-invariance: the defect is larger than first reported

| gate | result | |
|---|---|---|
| **G1** control — nb11 verbatim (`argsort` + inventory column order) vs the stored field | **0 of 34,844,096 cells differ**, 124,097 fallback cells (nb11's printed figure) | **PASS** |
| **G2** the defect, reproduced on demand — same `argsort`, gauge columns shuffled | 145,531 / 179,458 / 248,528 cells differ; **52 / 61 / 83 minibacias**; max \|ΔP\| **19.5 / 20.5 / 17.8 mm** | **PASS** (defect confirmed) |
| **G3** the fix — deterministic `lexsort` on (distance, gauge code), 5 shuffles | byte-identical field every time | **PASS** |

§10.7 reported 44 minibacias and 13.1 mm from *one* alternative ordering (sorted by code).
Random orderings are worse: up to **83 minibacias and 20.5 mm/day**. The earlier figure was
a lower bound on an arbitrary choice, not the size of the defect.

G2 matters as much as G3. A fix for a defect you cannot reproduce on demand is untestable,
so the shuffle test is written to *first* show the old code path failing and only then show
the new one holding. `assert_order_invariant()` in the module is the standing guarantee —
the `lexsort` is only the mechanism, and without the assertion nothing stops a later edit
reintroducing an order-dependent field.

**Cost of adopting determinism (G4):** against the stored field the deterministic
interpolator moves 194,081 cells across **69 minibacias**, max \|ΔP\| 20.47 mm — because the
stored field embodies one arbitrary tie-break and this one embodies a reproducible rule.
The **areal mean is unchanged: 2,174.3 mm/yr either way.** Anything that re-runs nb11
inherits the new local values, which is the correct outcome but must not be mistaken for a
data change.

### 11.2 Co-located gauges: a blanket rule would have destroyed data

Swept to 500 m as instructed and found a **fourth** pair the exact-tie search had missed.
Then classified each pair by what the two records do on the days they **both** report —
because that, not distance, is the evidence for whether they are one instrument or two:

| pair | dist | n both | mean \|diff\| | corr | verdict |
|---|---|---|---|---|---|
| AEROPUERTO OLAYA HERRERA `27015070` / `27015330` | 0.000 m | 276 | 0.000 mm | 1.000 | **duplicate** → merge |
| CUCUNUBA `24010140` / CUCUNUBA-AUT `2401500040` | 0.000 m | 366 | 0.003 mm | 1.000 | **duplicate** → merge |
| CERINZA `24030590` / `24035420` | 0.000 m | **0** | — | — | **sequential** → merge |
| EL DORADO CATAM `21205791` / AEROPUERTO CATAM `21206570` | 0.052 m | 1,470 | **1.915 mm** | **0.756** | **coordinate error** → **do NOT merge** |

Three distinct situations, and only two of them are duplicates:

* **duplicate** — one measurement filed under two codes. Merging is pure de-duplication.
* **sequential** — CERINZA has *zero* overlap: `24030590` runs 2008-01→2009-06 and
  `24035420` picks up 2009-07→2018-12. An instrument replacement, not a duplicate. Merging
  reconstructs one continuous record from two fragments, which is strictly better than
  interpolating across the join.
* **coordinate error** — Catam's two records overlap on 1,470 days and *disagree*: only 470
  identical, mean \|difference\| 1.9 mm, correlation **0.756**. At a nominal separation of
  5 cm that is not physical — the true duplicates above read 1.000, and the basin-wide
  inter-gauge correlation at 0–25 km is only 0.33 ([doc 22 §4.7](22_dry_phase_diagnosis.md)), so 0.756 is neither. **These are
  two real gauges and one of them has the wrong catalogue coordinates.** Merging them would
  have averaged away a genuine second observation, silently. Left unmerged and flagged.

**A distance-only rule would have destroyed that station.** The rule adopted is
evidence-based per cluster; `data/processed/precip_colocated_gauges.csv` carries the
classification with its numbers so the judgement is auditable rather than asserted.

Merge mechanics: highest approval level wins the day (`Definitivo > En revisión >
Preliminar`, the precedence `build_precip_gauges.py` already uses); the surviving code is
the member with the most records, so provenance stays traceable.

### 11.3 What the merge costs — negligible globally, material locally

Gauges **294 → 291**; station-days 926,910 → 926,268; k=6 fallback cells **41,504 →
41,180** (the merge *improves* coverage, because a reconstructed record fills days on which
neither fragment alone reported).

| area-weighted basin mean | v2 unmerged | v2 merged | change |
|---|---|---|---|
| 2009–2017 | 2,035.6 | 2,036.4 | **+0.8 mm/yr (+0.04 %)** |
| 2008–2018 | 2,072.2 | 2,073.1 | +0.8 mm/yr (+0.04 %) |

| local effect | |
|---|---|
| minibacias changed | **542** of 8,672 |
| median mean \|ΔP\| among them | 0.225 mm/day |
| **median relative change** | **+5.03 %** |
| max relative change | **+33.48 %** |
| largest single-day \|ΔP\| anywhere | 29.18 mm |

**The basin mean is untouched and 542 minibacias move by a median 5 % — so this matters, and
it would have been invisible in any basin-level check.** Gauges are scored locally, so a
5–33 % change in catchment rainfall is a change in the calibration objective. 542 is also
far more than the 69 minibacias affected by the tie-break alone: removing a gauge frees a
`k=6` slot, so a *different* sixth gauge enters for every minibacia near a merged cluster.

Both numbers had to be reported. Had only the basin mean been checked, the correct
conclusion would have been "negligible" and it would have been wrong.

---

### 11.4 nb11 now imports the shared interpolator (open items 12 and 13 closed)

`make_nb11.py` §3 no longer carries its own copy of the IDW. It imports
`src/idw_forcing.py`, so the notebook, the diagnostics and any re-run share one
implementation. `idw_field(..., return_detail=True)` returns the fallback mask and the
neighbour distances as well as the field, which is what nb11 needed for its
`fallback_days` and `d_nearest_km` columns — the reason it had a private copy.

`assert_order_invariant()` is called **inside the notebook**, before the field is built,
rather than sitting in a test file. A notebook that regenerates its own forcing should not
be able to regress silently.

| gate | result | |
|---|---|---|
| **G-A** `return_detail` API — mask matches `n_gap`, distances shaped (8672, 6) | 41,504 fallback cells both ways; nearest gauge median 16.3 km, max 71.5 km | PASS |
| **G-B** `NEVER_MERGE` guard under deliberately absurd thresholds (`IDENTICAL_MM = 999`, `IDENTICAL_CORR = 0`) | CATAM still `coord_error`, `do_merge=False`, while every other pair flipped to merge | PASS |
| **G-C** generator produces a valid notebook | 23 cells, 2 `idwf` references | PASS |

G-B is open item 12. Refusing the CATAM merge on *evidence* is not enough on its own,
because a later edit loosening `IDENTICAL_MM` or `IDENTICAL_CORR` would resurrect it. The
named `NEVER_MERGE` set makes that impossible, and G-B is the proof: with thresholds set so
loose that all three genuine duplicates merge, CATAM still does not.

**Not yet done: the notebook has not been re-executed.** Only the generator was run
(trap 10 — verify from executed outputs, never from the fact that a generator succeeded).
Executing it is Phase 2, and when it runs it will produce the deterministic field, which
differs from the stored one at 69 minibacias (§11.1) before the v2 gauge file and the merge
are even applied.

---

## 12 — Phase 1: triage of the 14 residual energy-floor gauges (open item 10)

14 of 61 is 23 % of the calibration objective, and both failure modes are real — leaving an
impossible target in pulls parameters toward nonsense, while excluding a gauge whose problem
is *our* local forcing hides our own defect. So the decision rule was declared **before the
numbers were looked at**:

| rule | condition | verdict |
|---|---|---|
| D1 | one precip gauge carries ≥40 % of the catchment's IDW weight **and** is rain-selective (> 1.2885) | **KEEP** — our forcing defect; fix the forcing, don't hide it |
| D2 | flagged intake / distributary / nested inversion | **EXCLUDE** — hydrology the model does not represent |
| D3 | needs P to fall > 25 % with no dominant selective gauge | **EXCLUDE** — impossible target |
| D4 | rating curve R² < 0.90 or < 30 stage–discharge pairs | **DOWN-WEIGHT** |
| D5 | anything else | **DOWN-WEIGHT** — unresolvable |

Result: **2 EXCLUDE, 2 KEEP, 10 DOWN-WEIGHT** → 59 full-weight gauges, 10 down-weighted.
Full table in `data/processed/energy_floor_triage.csv`.

| code | area km² | P mm/d | Q mm/d | rc | floor | P cut needed | dominant precip gauge (share, selectivity) | rating R² (n) | verdict |
|---|---|---|---|---|---|---|---|---|---|
| 22017010 | 2,411 | 5.645 | 0.947 | 0.168 | 0.480 | **31.2 %** | 22010010 (0.39, —) | **0.359** (6,966) | EXCLUDE D3 |
| 23087200 | 524 | 11.464 | 4.930 | 0.430 | 0.705 | **27.5 %** | 23080750 (0.61, **0.997**) | — (0) | EXCLUDE D3 |
| 26107130 | 748 | 5.453 | 1.869 | 0.343 | 0.498 | 15.5 % | 26100670 (0.34, 1.258) | 0.536 (3,075) | DOWN-WEIGHT D4 |
| **22077060** | 731 | 4.841 | 1.040 | 0.215 | 0.368 | 15.4 % | 22070030 (**0.49, 1.445**) | — (0) | **KEEP D1** |
| 26027240 | 188 | 4.750 | 1.460 | 0.307 | 0.447 | 13.9 % | 26020460 (0.47, 1.001) | — (0) | DOWN-WEIGHT D5 |
| 26197020 | 255 | 6.546 | 2.867 | 0.438 | 0.563 | 12.5 % | 26195020 (0.55, 1.020) | — (0) | DOWN-WEIGHT D5 |
| 26237020 | 210 | 5.513 | 1.681 | 0.305 | 0.410 | 10.5 % | 27011110 (0.29, 1.311) | 0.455 (305) | DOWN-WEIGHT D4 |
| 26127100 | 101 | 6.377 | 2.908 | 0.456 | 0.555 | 9.9 % | 26135040 (0.44, 1.000) | — (0) | DOWN-WEIGHT D5 |
| 26167060 | 179 | 5.393 | 2.188 | 0.406 | 0.448 | 4.2 % | 26155110 (0.31, 1.000) | 0.685 (551) | DOWN-WEIGHT D4 |
| **21107030** | 288 | 4.730 | 1.528 | 0.323 | 0.360 | 3.7 % | 21100070 (**0.69, 1.575**) | — (0) | **KEEP D1** |
| 23087160 | 344 | 8.712 | 4.834 | 0.555 | 0.591 | 3.6 % | 27011230 (0.29, 1.285) | — (0) | DOWN-WEIGHT D5 |
| 26027200 | 320 | 4.537 | 1.708 | 0.376 | 0.395 | 1.9 % | 26020460 (0.58, 1.001) | — (0) | DOWN-WEIGHT D5 |
| 21237040 | 243 | 4.118 | 0.935 | 0.227 | 0.237 | 1.0 % | 21205670 (0.22, 1.664) | — (0) | DOWN-WEIGHT D5 |
| 26207080 | 30,848 | 5.131 | 2.217 | 0.432 | 0.436 | 0.4 % | 26195020 (0.05, 1.020) | 0.644 (385) | DOWN-WEIGHT D4 |

### 12.1 Only 2 of 14 are ours, and 8 of 14 cannot be checked at all

Two gauges (22077060, 21107030) fail with a *selective* precip gauge carrying half to
two-thirds of their catchment weight — 1.445 and 1.575 selectivity, and both were repaired,
so what remains is residual local inflation from a gauge that was already treated. **These
stay in the objective.** Excluding them would delete the evidence of our own forcing defect,
and both need only a 4–15 % local P correction, which is within reach.

Eight of the 14 have **no rating curve at all** (`n_pairs = 0`), so their discharge cannot be
independently verified. That is not "unresolvable" in the sense of being fine — it is a
measurement gap, and D5 down-weights rather than excludes precisely because we cannot tell
the difference between a bad gauge and a bad catchment there.

Where a rating curve *does* exist it is mostly poor: **R² 0.359 on 6,966 stage–discharge
pairs** at 22017010, 0.455, 0.536, 0.644, 0.685 elsewhere. An R² of 0.36 over nearly seven
thousand pairs is not noise, it is a rating relationship that does not hold — which is
independent support for excluding that gauge.

### 12.2 The two exclusions look like water leaving the catchment, not error

23087200 is the interesting one, and the collaborator's independent run corroborates it: his
second-worst station, PBIAS **+417 %**, KGE **−4.59**. Two implementations, two different
forcing pipelines, the same station broken in the same direction — the model produces far
more water than the river carries.

But its dominant precip gauge is *healthy*: 23080750 carries 61 % of the catchment weight
with selectivity **0.997** and was never repaired. So the rainfall is well supported, and
11.46 mm/day (4,187 mm/yr) is high but entirely plausible on the Antioquia–Chocó flank. The
observed runoff coefficient of 0.430 is what does not fit: that flank should run at 0.7+.

**Hypothesis to check, not a conclusion: upstream hydropower diversion.** Both exclusions sit
in Antioquia, where EPM and ISAGEN operate major reservoirs and inter-basin transfers. Water
routed out of a catchment for generation makes observed Q genuinely far below P − ET, with no
error anywhere in the data. If that is what these are, they are D2 (unrepresented hydrology)
rather than D3 (bad data), and the verdict is the same — exclude — but the *reason* recorded
in the paper would be different, and defensible. `is_intake` in `gauges.csv` does not flag
them, so the flag list is incomplete rather than the gauges being clean.

### 12.3 A 2.5× catchment-area disagreement between the two implementations

For 23087200 we compute an upstream area of **524 km²**; the collaborator reports
**1,324 km²**. That is not a rounding difference, and it cannot be reconciled by the ENSO
window or the forcing — it is the drainage network. One of the two delineations is wrong, or
the two are snapping the gauge to different reaches.

It does not change this gauge's verdict (both implementations find it broken, and in the same
direction) but it is a direct check on the doc-17 gauge re-snap that nobody has run, and it
should be settled before any published area-normalised sediment yield. New open item 14.

---

## 13 — Phase 1: the catchment-area disagreement, and the circularity that wasn't

Open items 14 and 15, plus a pre-authorised re-snap (1c) that this section argues **should not
be run**.

### 13.1 The circularity test — REFUTED, and it saves the re-snap

`src/fix_gauge_minibacia_mapping.py:161` scores candidate minibacias by
`abs(log(rc) − log(RC_REFERENCE))` with `RC_REFERENCE = 0.435`, a single basin-wide median.
The energy floor says the Antioquia–Chocó flank should run 0.7+, so the concern was that the
mapping optimised toward a regionally wrong target and the energy-floor test is therefore not
independent of the mapping it evaluates. That is a serious charge, and it is testable:
`kept` stations (129) were never moved, so their rc spread is the natural one.

| group | n | median rc | SD of log rc | IQR of log rc | median \|log(rc/0.435)\| | within ±10 % of 0.435 |
|---|---|---|---|---|---|---|
| kept | 129 | 0.378 | **0.886** | 1.252 | **0.402** | 14.7 % |
| remapped | 20 | 0.463 | **0.895** | 0.748 | **0.435** | 25.0 % |

* SD of log rc is **the same**: ratio 1.009. Levene's equal-variance test on log rc gives
  **W = 0.095, p = 0.76** — no evidence the remapped group is tighter.
* Distance from the reference is **larger** for the remapped group, not smaller: median
  \|log(rc/0.435)\| is 0.435 against the kept group's 0.402.
* Only the IQR narrows (ratio 0.598), and with n = 20 that is one or two stations; the SD and
  Levene both contradict it.

**The reference was not injected into the data.** The mechanism explains why: the candidate
set is a 3×3 window of minibacias around the gauge, so the rc target only breaks ties among a
handful of geometrically plausible options — it cannot manufacture an rc that no nearby
minibacia produces. The tie-break is weak by construction.

**Consequence: step 1c is not justified and was not run.** Re-snapping with regional rc
references would have been a large, invalidating change to the gauge mapping, and the evidence
for needing it is absent. Recorded here so the decision is auditable rather than silent — and
so that anyone reviving the idea has to beat p = 0.76 first.

### 13.2 Scope of the area disagreement — worse than "one bad station"

Joined our upstream areas to the collaborator's 91-gauge table on station code: **85 gauges**
in common.

| ratio his/ours | |
|---|---|
| median | **0.991** |
| p05 / p25 / p75 / p95 | 0.15 / 0.50 / 1.37 / 8.68 |
| within 10 % | 22 of 85 (26 %) |
| within 25 % | 28 of 85 (33 %) |
| within 2× | 54 of 85 (64 %) |
| **beyond 2×** | **31 of 85 (36 %)** |

Four of his areas are unambiguous **mainstem-snapping failures** — he assigns 15–62 % of the
entire 257,097 km² basin to gauges we place at 137–2,550 km²:

| code | ours | his | ratio |
|---|---|---|---|
| 25027360 | 137 km² | 158,251 km² | **1,154×** |
| 23187280 | 249 km² | 116,326 km² | 468× |
| 23217030 | 1,006 km² | 119,627 km² | 119× |
| 25027530 | 2,550 km² | 73,871 km² | 29× |

But removing those four does **not** rescue the comparison: of the remaining 81 gauges only
**28 agree within 25 %**, and the median is 0.988. So this is not "his network is broken and
ours is fine". **The median agrees to ~1 % while individual gauges disagree wildly, which
means neither derivation is trustworthy per gauge.** Two independent D8 delineations on
different DEMs disagree by more than 2× on a third of a shared 85-gauge sample.

That is the finding, and it is more uncomfortable than the one we set out to check. It bears
directly on Phase C: **a sediment yield in t/km²/yr inherits this error one-for-one**, so no
specific yield should be published per gauge until the area is verified against something
external to both networks.

### 13.3 23087200 specifically — brackets, does not resolve

Inverting the water balance, holding the measured discharge (29.9 m³/s) and upstream
P (11.464 mm/day) fixed and solving for the area that would give a target rc:

| target rc | implied area |
|---|---|
| 0.435 (the mapping's reference) | 518 km² |
| 0.600 | 376 km² |
| 0.700 | 322 km² |
| 0.800 | 282 km² |

Our 524 km² sits almost exactly on the rc = 0.435 line — **but that is circular**, because the
mapping chose this minibacia to bring rc near 0.435. It cannot be used to validate our area.

Can it reject his 1,324 km²? That implies rc = 0.430 × 524/1324 = **0.17**. Against the
never-remapped `kept` distribution (§13.1) — 10th percentile 0.067, 25th percentile 0.151,
median 0.378 — an rc of 0.17 sits near the **27th percentile**. Low, but squarely inside the
observed range. **So this test cannot reject his area either.** It brackets and stops there.

`stations_discharge.csv` and `discharge_inventory.csv` carry **no published drainage area**, so
the external arbiter 1d wanted is not available locally. Open item 14 stays open, narrowed:
what is needed is IDEAM's catalogue area for this station, or a manual delineation check, not
another derivation from either of our DEMs.

### 13.4 `is_intake` is a name regex, not a regulation inventory (open item 15)

`make_nb12.py:983`:

```python
G['is_intake'] = nm.str.contains(re.compile('BOCATOMA|CANAL', re.I)) | G.index.isin(DOC_INTAKE)
```

So the flag fires on gauges whose **name** contains *bocatoma* or *canal*, plus a manual list
carried over from doc 17. It cannot see a gauge sitting downstream of a reservoir or an
inter-basin transfer whose name is simply a place — which is exactly the situation of the two
gauges §12.2 excluded. PAILANIA is not called a canal.

**The flag list is a naming heuristic and was never a regulation inventory.** It is not wrong,
it is narrower than its name suggests, and the EPM/ISAGEN diversion hypothesis cannot be tested
against it. Testing that needs an external register of reservoirs and transfers in the
Antioquia headwaters. Open item 15 restated accordingly — it is a data-acquisition task, not a
code fix.
