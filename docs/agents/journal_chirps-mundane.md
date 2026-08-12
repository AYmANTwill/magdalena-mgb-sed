# Journal — agent H-E ("the mundane ones"), CHIRPS-gauge volume-gate failure

**Date:** 2026-08-12. **Branch:** main. **Role:** one agent of a multi-agent diagnosis of
why the CHIRPS-gauge merged rainfall field failed its pre-registered VOLUME gate
(2,188.5 mm/yr vs target 2,036.4 ±1 % = [2,016.0, 2,056.8]).

## What I was asked

Rule out — or find LIVE — the *boring* explanations, each with its own measurement:
1 unit mismatch (mm/day vs mm/yr; the 365.25 convention; CHIRPS's own units),
2 window mismatch (gate 2009–2017 vs LOOCV 2008–2018),
3 double-counting of overlapping strata (a cell mapped twice),
4 area weights inconsistent between gauge-only and merged,
5 different cell mask / order / date index,
6 the gap-fill/fallback story (41,180 vs 35,716 k=6-silent cell-days),
7 the CHIRPS `LAG = -1` edge handling,
8 anything else — incl. (a) the docs/18 §10.5 2,035.6/2,174.3 vs measured 2036.393/2175.167
  +0.8 offset, and (b) `VOLUME_TARGET = 2036.4` being a hard-coded constant.

Constraints honoured: no `git add/commit/push`; no writes to `data/processed/model_inputs_v2/`,
`sim_calibrated_v2/`, docs/33, docs/30, docs/18, or docs/54; all scratch scripts live in the
session scratchpad, none in the repo.

## Log

### 1. Read the code before trusting any column
Read in full: `src/merge_chirps_gauges.py`, `<scratchpad>/h2_harvest.py`,
`<scratchpad>/h3_bounds.py`. Next: `src/idw_forcing.py`.

First reading note (recorded before any measurement, defect candidate for item 8):
`h3_bounds.py` sets `RATIO_104 = 1.836 / 4.056` = 0.45266, but its docstring and BOTH F5/F6
row labels written into `bounds_fields.csv` say "0.414". The **code** is 0.4527 (matching the
task brief); the **label in the artefact** says 0.414. Label defect, not a number defect —
verified below.

### 2. Grep for the docs/18 §10.5 numbers (item 8a) — found the documented answer, will measure it
`grep -rn "2035.6|2174.3"` over docs/src/notebooks returns, among others:
* `docs/18_hydrology_journal.md:598` — the §10.5 table: 2009-2017 v1 **2,174.3**, v2 **2,035.6**.
* `docs/23_gauge_geometry.md:95` — §11.3 "What the merge costs": 2009-2017 v2 **unmerged 2,035.6**
  vs v2 **merged 2,036.4**, "+0.8 mm/yr (+0.04 %)"; 2008-2018 2,072.2 -> 2,073.1, +0.8.
* `docs/39_contradiction_audit.md:167` — "**2,035.6** unmerged / **2,036.4** merged … (merge worth +0.8)".
So the offset is ALREADY attributed to the co-located-gauge merge (`idw_forcing.merge_colocated`,
294 -> 291 gauges). docs/18 §10.5 predates the merge; `h3_bounds` F1/F2 call `merge_colocated`.
That is an attribution in prose, not a measurement I have made -> I will MEASURE it by building
the same two fields with the merge suppressed. (Done in `he3_idw.py`, entry 5 below — I had
planned a separate `he5_merge_offset.py` and folded it in to avoid a second IDW rebuild.)

### 3. `he1_ledger.py` — ledger-only re-derivation (items 1 part, 2 part, 3, 4, 6)
Ran `python3.10 he1_ledger.py` (scratchpad `he/`, output saved to `he/he1_out.txt`). Executed
output, not exit code. Highlights I based claims on:
* ids/areas identical to `forcing_minibacia_provenance_v2.csv`, `sum(area)=257096.930000 km2`,
  min area 1.63, 0 zero/NaN/duplicate. `lat` differs on 30 rows by <=8.9e-16 (CSV float64
  round-trip, 1 ulp) — recorded, immaterial.
* (band,zone) groupby of the 8,672 cells = 32 keys = `stratum_table.csv`'s 32 keys, counts and
  areas equal to 0, `sum(n_minibacia)=8672`, `sum(area)=257096.930000`. No zone NaN/empty; no
  `str()` collision. Partition proven.
* 365.25 vs real days/yr: gate +0.00761 %, full -0.00622 %; ratio merged/target identical to
  8 dp on either convention (1.07471432). Cancels.
* fallback: gate nB 35,716 (0.1253 % of cell-days) contributing **+0.0384 mm/yr**; full nB
  41,180 -> +0.0500. nA+nB+nD == n_cells*n_days on every row, nD == 0.
* surplus re-derived +152.1477 (identity residual 1.24e-3 mm/cell), channels
  +87.3022 / +64.8070 / +0.0086 / +0.0298 — matches the brief to 4 dp.
* cross-window matrix: every merged/target pairing is +5.571 % to +8.976 %. No pairing passes.
* NEW defect (label only): `bounds_fields.csv` F5/F6 row strings say "0.414" while the code
  ratio is 1.836/4.056 = 0.452663. The numbers in the CSV are the 0.4527 ones.

### 4. `he2_units.py` — units from attributes, the window mask, and the hard-coded target
Ran; output `he/he2_out.txt`.
* `chirps_basin_2011.nc` `precip.attrs['units'] = 'mm/day'`, `time_step='day'`, CF-1.6,
  CHIRPS v2.0. Payload min 0.000 max 381.921 mean 7.8189 (bounding box — trap 8, never averaged).
* `precip_gauges_daily_qc_v2.csv`: 926,910 rows, `precip_mm` mean 5.0543, max 270, 0 NaN,
  2008-01-01..2018-12-31; `Inferido_seco` 240,158. mm/day.
* masks: 2009-2017 -> 3,287 contiguous days 2009-01-01..2017-12-31; 2008-2018 -> 4,018.
* **stored `forcing_precip_v2.npy` (4018, 8672) float32, areal mean 2009-2017 =
  2036.392327 mm/yr**, 0 non-finite, 0 negative. `VOLUME_TARGET = 2036.4` is off by
  **-0.007673 mm/yr (-3.8e-4 %)**. Tolerance half-width is 20.364 mm/yr; the miss is 7.47x it.

### 5. `he3_idw.py` — item 5 re-verified myself + item 8a MEASURED
Ran (4 IDW rebuilds, ~7 min); output `he/he3_out.txt`, table `he/he3_fields.csv`.
* item 5: rebuilt v2 field is (4018, 8672) on the exact daily index 2008-01-01..2018-12-31;
  `d_nearest_km` matches provenance_v2 to 1.99e-13; `fallback_days` identical (max|diff| 0);
  `max |P_rebuilt - stored forcing_precip_v2.npy| = 0.005001 mm`, and only **147 of
  34,844,096** cells sit above the 0.005 half-width (all at 0.005001 = the float32 image of
  the half-width). The harvest's claim is confirmed independently.
* item 8a: co-located merge OFF vs ON, one interpolator:
  v2 2035.5998 -> 2036.3927 (+0.7929); v1 2174.2958 -> 2175.1666 (+0.8708);
  2008-2018: v2 2072.2219 -> 2073.0546, v1 2205.9991 -> 2206.9298.
  **docs/18 §10.5's 2,035.6 / 2,174.3 / 2,206.0 are the merge-OFF fields to 4 dp.** The offset
  is `idw_forcing.merge_colocated` (294->291 gauges; 3 codes folded; station-days 926,910 ->
  926,268; k=6-silent cells 41,504 -> 41,180). Not quantisation, not a units or window artefact.
  (docs/18 prints v2 2008-2018 as 2,072.3; measured merge-OFF is 2072.2219, so docs/23's
  "2,072.2" is the correct rounding and docs/18's "2,072.3" is 0.1 out. Cosmetic.)

### 6. `he4_lag_tail.py` — item 7 (the lag) and a new item-8 check (map extrapolation)
Ran; output `he/he4_out.txt`, table `he/he4_tail.csv`. Loaded raw CHIRPS at the 8,672 centroids
once with a loader that mirrors `load_chirps` minus the lag, and additionally asserted the
CHIRPS lat/lon grid is byte-identical across all 11 year files (it is).
Quantile maps were refit from `qmap_pools.npz` using `stratum_table.csv`'s recorded
`pool_level`; the refit reproduces every stratum's `ck[-1]`, `gk[-1]` and `pool_n_pairs`
(asserted before any tail number was computed), and the 32 strata partition 0..8671.

* `aligned[t] == raw[t+1]` for all t<4017 : True. `aligned[4017] == raw[4017]` (2018-12-31
  duplicated) : True. Raw 2008-01-01 is dropped.
* Gate window = aligned indices 366..3652, consuming RAW 367..3653 = **2009-01-02..2018-01-01,
  3,287 contiguous distinct raw days, no repeat**. Index 4017 is NOT in the gate window.
  **The duplicate-last-day edge handling costs the gate window exactly 0.**
* The lag's own one-day shift (raw 2009-01-01 out, raw 2018-01-01 in): basin day-means
  0.1387 -> 8.4523 mm raw, 0.2854 -> 8.7975 mm mapped; areal-mean effect on the MERGED field
  **+0.3893 mm/yr** w-weighted (+0.9459 at w=1, upper bound) = **0.26 %** of the surplus.
* Duplicated last day, 2008-2018 only: magnitude bounded by that one day's whole contribution,
  +0.0057 mm/yr w-weighted. Signed error unmeasurable (no 2019 CHIRPS on disk) — I refuse to
  put a sign on it. Irrelevant to the gate.
* NEW (item 8c): `apply_qmap`'s above-max branch replaces the interpolation with
  `x * gk[-1]/ck[-1]`, i.e. it EXTRAPOLATES off the support the map was fitted on (ck is
  quantiles of CHIRPS at GAUGE PIXELS; x is CHIRPS at MINIBACIA cells, a different sample).
  30 of 32 strata have tail_scale > 1 (up to 2.607). Measured: **678 of 28,504,864 cell-days
  (0.00238 %)** exceed ck[-1]; mapped areal mean 2265.7574 with the branch on vs 2265.4769
  with it clipped at gk[-1] -> the rescale is worth **+0.2805 mm/yr** of the mapped field and
  **+0.1508 mm/yr (0.10 %)** of the merged surplus. RULED OUT as a cause; recorded so no one
  else has to test it, and so the map inflation is known to live in the BULK, not the tail.

### 7. Two more mundane candidates, both measured, both ruled out
* Per-station unit slip in the gauge file: 294 stations, per-station mean mm/day min 1.727 /
  median 4.620 / max 15.295; **0 stations above 20 mm/day** (a monthly-total slip would sit
  near 150); 0 duplicate (code,date) rows.
* The flat-earth distance that sets `w`: `idw_forcing.km` uses 111.0 km/deg where the true
  figure is 111.19508, so it UNDERSTATES distance by 0.176 %. Recomputed `d_nearest` with a
  haversine (R = 6371.0088): mean 18.9673 -> 19.0007 km, max |diff| 0.126 km, area-weighted
  mean w 0.403717 -> 0.404628, and re-evaluating the exact ledger identity gives surplus
  +152.1477 -> **+152.3365 mm/yr (+0.1888)**. Ruled out, and the sign is the wrong way to help.
  (The flat-earth d reproduces the ledger's `d_nearest_km` to 9.6e-14, so the ledger column
  and `km()` agree — that was the control.)

### 8. Gate provenance, read not measured
`docs/agents/journal_chirps-merge.md` L65-66 and `docs/33` §1 both state the volume bar as
"within ±1 % of the gauge-only 2,036.4 mm/yr → [2,016.0, 2,056.8]". The **target** is internal
and reproducible (stored v2 forcing gives 2036.392327, so the constant is right to 3.8e-4 %) —
it is not an uncited literature band, so the docs/40 retirement rule does not bite it. The
**±1 % tolerance** has no derivation anywhere I could find: it is declared, not cited. I do not
call the gate void on that, because the miss is 7.47x the tolerance — no defensible tolerance
choice rescues it short of pre-registering ±7.5 %. Stated so the synthesis agent can decide.

## What I refused to claim
* A signed size for the duplicated-2018-12-31 error on the 2008-2018 window — 2019 CHIRPS is
  not on disk. Magnitude only.
* That the ±1 % tolerance is justified. It is pre-registered, not cited. Different thing.
* Anything about whether the gauge-only TARGET field is itself correct (the H-A bracket agent
  owns that). I re-print `bounds_fields.csv` unchanged and repeat h3's own warning that F5/F6
  double-count the selectivity the repair removes, so they are loose upper sensitivities.
* I did not re-run the LOOCV gate or `assert_order_invariant` — both are outside the volume
  gate and both were deliberately skipped by the harvest too. So I cannot speak to r = 0.447.

## Could not settle
* Nothing on the mundane list is unsettled. Every one of the eight items has a number.
* Open, and NOT mine (measured, so the synthesis agent has the number): the quantile map is
  **volume-neutral where it was fitted and not where it is applied**. Pair-weighted over the
  926,268 paired station-days at the 291 gauge pixels: G 5.0550, C_raw 4.9276, C_map 5.0567
  mm/day, so **C_map/G = +0.034 %** — the map does exactly what it says. Over the 8,672
  minibacia cells, gate window: P 2036.3927, C_raw 2124.7205 (+4.337 % on P), C_map 2265.7574
  (**+11.263 % on P**, +6.638 % on C_raw). The map lifts CHIRPS by +2.619 % at the gauge pixels
  and by +6.638 % over the basin. **That gap is the whole finding**, and it is not a unit,
  window, mask, area-weight, stratum, fallback, lag or tail-extrapolation artefact — every one
  of those is measured and dead above. It is a transfer/representativeness question about where
  the gauges are versus where the field is evaluated, which is the interesting hypotheses' turf.

## Residual arithmetic (the number I hand on)
Total surplus, gate window: **+152.1477 mm/yr**. To PASS the merged field must fall to
<= 2056.7640, i.e. shed **131.7764 mm/yr**.
Every mundane channel measured above, summed with the sign that HELPS the gate:
fallback days +0.0384, lag one-day shift +0.3893, above-max tail rescale +0.1508,
365.25-vs-365.222 net on the surplus +0.0115  =>  **+0.590 mm/yr, 0.39 % of the surplus and
0.45 % of what the gate needs**. (The flat-earth `km()` moves it the wrong way, +0.19.)
Residual for the interesting hypotheses: **>= 151.56 mm/yr**, all of it in the two blend-day
channels — map inflation +87.3022 (57.4 %) and CHIRPS-vs-IDW +64.8070 (42.6 %) — on the 74.2 %
of basin area with w > 0, with 64.4 % of the whole surplus inside the 17.1 % of area at w = 1.

Scratch scripts (not in the repo):
`<scratchpad>/he/he1_ledger.py`, `he2_units.py`, `he3_idw.py`, `he4_lag_tail.py`
with saved executed output `he1_out.txt`, `he2_out.txt`, `he3_out.txt`, `he4_out.txt`
and tables `he3_fields.csv`, `he4_tail.csv`.
