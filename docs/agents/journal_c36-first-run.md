# Journal — c36-first-run

GOAL: first UNCALIBRATED basin erosion run with MUSLE alpha=11.8, beta=0.56 over the full
frozen H2E driver record. Order-of-magnitude + spatial-pattern gate ONLY. Magnitude is
expected to be wrong; that is not the test.

## Checklist
- [ ] 1. Read src/mgb_sediment.py API (entry points, driver loading, outputs)
- [ ] 2. Read journal_c34-sediment-engine.md for conventions already established
- [ ] 3. Run full-record erosion with alpha=11.8, beta=0.56
- [ ] 4. Basin total Mt/yr; spatial distribution; per-minibacia specific erosion
      (t/km2/yr, INTERNAL model-area diagnostic only — NOT a station/sub-basin yield;
      docs/23 embargo covers the latter)
- [ ] 5. Gate a: Andean flanks >> lowland floodplain (map)
- [ ] 6. Gate b: within an order of magnitude of ~145-169 Mt/yr anchor (over-estimate
      expected: no channel deposition yet)
- [ ] 7. Gate c: zero erosion where no runoff
- [ ] 8. Gate d: no NaN, no negatives
- [ ] 9. Two known biases, quantified + signed
- [ ] 10. Figures -> figures/deck/: erosion map; seasonal cycle w/ ENSO windows
- [ ] 11. Report ENSO signal (NOT C5)

## Log
### Step 0 — start
Confirmed present: src/mgb_sediment.py (53,308 bytes),
data/processed/sim_calibrated_v2/h2e_drivers.npz (546,366,478 bytes).
ENGINE handoff reports done=true, 82 pytest passed, ledger exact.

### Step 1 — engine API read (no edits)
`simulate_sediment(geom, params, qsur_mm, dates=, record_ids=, backend=, store_daily=)`.
`SedParams(alpha=11.8, beta=0.56, fg=1.0, pixel_area_km2=0.0081, tau_delivery_days=0.0,
volume_convention='pixel_km2')` — the requested alpha/beta ARE the module defaults, so this
run is the registered configuration with nothing overridden.
Per-minibacia period totals recoverable as `bincount(geom.cell_mini, cell_eroded_t)`.
Basin daily series in `result.series['delivered']`.
KNOWN before running (docs in module + journal_c34): registered `pixel_km2` gives
0.6844 Mt/yr; `williams_m3` is exactly 1000**0.56 = 47.8630x that = 32.76 Mt/yr. Gate (b)
will therefore be reported for BOTH conventions, since the choice of convention is the
order-of-magnitude question.
Terrain classifier for gate (a) must be INDEPENDENT of LS2D (LS2D is itself a MUSLE
multiplier — using it would make the gate circular). Using mean elevation per minibacia from
the corrected COP90 DEM (`%TEMP%/output_hh.tif`, 260 MB, present) block-aggregated 8x onto
`data/processed/minibacias.tif` (705x1500, EPSG:4326, 0.01 deg).

### Step 2 — RUN A DONE (registered configuration, alpha 11.8, beta 0.56)
Full record 2009-01-01..2018-12-31, 3,652 d x 8,672 minibacias, 32,782 URH cells,
covered area 257,096.93 km2, ls2d_hs, qsur_rel_mm, tau 0, FG 1.0, pixel_km2. 1.46 s.
`params.check()` -> status 'ok' (alpha band 5.9-23.6, hard stops 3.93 / 35.4; beta band
0.50-0.62; scale_factor 1.0) — i.e. the STARTING values sit inside the pre-registered band.
- LEDGER EXACT: eroded == delivered == 6,843,119.50146461 t, store_end 0.0, residual **0.0**
  (bitwise), exact=True. Reproduces journal_c34 S7 to the last digit.
- GATE d PASS: 31,713,882 elements checked (3652x8672 delivered + 32,782 cell totals +
  3x3652 series) -> 0 non-finite, 0 negative. min 0.0, max 1,096.59 t/d.
- FLEET: 6.8431 Mt over 9.999 yr = **0.6844 Mt/yr** (pixel_km2) / **32.758 Mt/yr**
  (williams_m3, factor exactly 1000^0.56 = 47.8630, re-run and confirmed).
  Daily basin mean 1,873.8 t/d, median 1,504.7, p99 6,674.4, max 9,000.7.
- PER-UNIT: per-minibacia 0.0675 t/d median (p25 0.0122, p75 0.1993, p95 0.5579,
  max 142.74). Specific erosion INTERNAL t/km2/yr: median 0.875, p25 0.166, p75 2.588,
  p95 6.646, p99 13.855, max 1,395.8, area-weighted mean 2.662. LABEL: model-area
  diagnostic of the model's own spatial pattern, NOT a station/sub-basin yield (docs/23).
- CONCENTRATION: 415 minibacias (4.79 % of count, **6.31 % of area**) carry 50 % of erosion;
  3,225 carry 90 %; top 1 % of minibacias carry 36.4 %, top 10 % carry 61.4 %.
- LAND CLASS (share of erosion vs share of area): Forest 36.48 / 55.77, Bare 35.60 / **0.196**,
  Grassland 27.33 / 39.87, Cropland 0.47 / 1.57, Urban 0.059 / 0.297, Shrub 0.058 / 0.119,
  Wetland 0.0015 / 1.52, Water 0.000 / 0.649. Bare = 182x over-represented (C3.2 bare-rock
  caveat is live and dominant).
- GATE c PASS, measured on the real record: qsur_gen_mm has 11,389,623 exact-zero
  minibacia-days (35.96 % of the record; every day and every minibacia has at least one).
  Erosion on those = **0 of 11,389,623 non-zero**, max |erosion| exactly 0.0. Converse also
  holds: 0 of 20,280,521 non-zero-runoff cells produced zero erosion. The registered
  qsur_rel_mm has NO exact zeros (linear-reservoir output, floor ~2e-43 mm/d), so the gate is
  necessarily exercised on qsur_gen_mm — stated, not hidden. qsur_gen run = 0.7699 Mt/yr
  (1.1249x the registered field).
- ENSO (uncalibrated; alpha cancels in a ratio, beta does not): La Nina 2011 2,976.77 t/d vs
  El Nino 2015-07..2016-06 1,052.48 t/d = **2.828x**. Annual Mt: 2009 0.497, 2010 1.053,
  2011 1.086, 2012 0.646, 2013 0.709, 2014 0.528, 2015 0.364, 2016 0.586, 2017 0.737,
  2018 0.639. Monthly climatology (t/d): J 815, F 697, M 1163, A 2268, M 3089, J 1997,
  J 1322, A 1238, S 1609, O 2754, N 3397, D 2088 — bimodal, Apr-May and Oct-Nov.
NEXT: gate (a) needs an LS2D-INDEPENDENT terrain classifier -> mean elevation per minibacia.

### Step 3 — GATE (a): Andean flanks >> lowland floodplain — PASS
Terrain classifier: mean elevation per minibacia from the corrected COP90 DEM
(`%TEMP%/output_hh.tif`, 12,000 x 5,640 @ 0.000833 deg) block-averaged 8x onto
`minibacias.tif`. 8,672 of 8,672 minibacias got a value (elev p0/p5/p50/p95/p100 =
6.2 / 27.2 / 898.6 / 3,090.7 / 4,491.1 m). Elevation is NEVER a MUSLE input, so the gate is
not circular — classifying by LS2D would have been.

band (mean elev)        n     area%  erosion%  spec_aw   spec_median   [t/km2/yr INTERNAL]
Lowland floodplain <100 1,736  19.2     1.6      0.221      0.031
Piedmont 100-500        1,691  19.3     8.5      1.168      0.467
Lower Andean 500-1500   2,442  28.1    30.0      2.843      2.258
Upper Andean 1500-3000  2,286  27.0    23.1      2.275      1.389
High Andes >3000          517   6.4    36.9     15.304      1.633

- **Andean flanks (500-3000 m) 2.559 vs lowland floodplain (<100 m) 0.221 t/km2/yr =
  11.6x.** Spearman(specific erosion, mean elevation) = **+0.554** over 8,672 minibacias.
  Lowland floodplain: 19.2 % of area, **1.6 %** of erosion. GATE (a) PASS.
- CAVEAT recorded on the figure, not buried: the >3000 m band's 36.9 % of erosion on 6.4 %
  of area is an INPUT artefact (bare rock/ice given C = 1.0, C3.2), not a terrain gradient —
  its per-minibacia MEDIAN (1.633) is BELOW the 500-1500 m band's (2.258), so the band mean
  is carried by a few extreme cells. Consistent with Bare = 0.196 % of area / 35.6 % of
  erosion in the land-class attribution.

### Step 4 — GATE (b): order of magnitude vs the published load — SPLIT, and the direction
is the finding
Anchors (docs/34 §5.1, both citations verified there): **144 Mt/yr** (Restrepo & Kjerfve
2000, 1975-1995) and **184 Mt/yr** (Restrepo & Escobar 2018, 1980-2010); docs/06's
~145-169 Mt/yr confirmed as a plausible range, not a single figure.

| convention | basin total | vs 144 | vs 184 | vs 145-169 | orders of magnitude |
|---|---|---|---|---|---|
| `pixel_km2` (REGISTERED, docs/35 §4) | **0.684 Mt/yr** | 210.4x low | 268.8x low | 211.9-246.9x low | **2.32-2.43 — FAIL** |
| `williams_m3` (Williams' literal m3 volume, = 1000^0.56 = 47.863x) | **32.758 Mt/yr** | 4.40x low | 5.62x low | 4.43-5.16x low | 0.64-0.75 — **PASS** |

**The direction is the informative part.** The task framing anticipated an OVER-estimate
(no channel deposition yet). Both conventions came out UNDER, which is the physically
forbidden direction: gross hillslope erosion must EXCEED the outlet load, because the
delivery ratio is < 1 and the Momposina sink lies above Calamar. So the shortfall against
the physically-required value is worse than the table by the factor 1/SDR.
Closing the registered gap with alpha needs alpha ~ 2,480 (70x past the pre-registered
hard stop of 35.4); merely absorbing the convention factor needs alpha ~ 565 (16x past).
`params.check()` on (11.8, 0.56) returns status 'ok', so the STARTING values are inside the
band and the band is not the thing that broke — the convention/level is.
Applying the docs/33+35 peak-deficit correction (central 2.1x, bracket 1.4-4.8x) to the
Williams number: 68.8 Mt/yr central (2.09x below 144, 2.67x below 184), bracket
45.9-157.2 Mt/yr — the top of the bracket is the first value that reaches the anchor, and
only under the most generous of three stacked assumptions. Recorded, not adopted:
**changing the default convention is an AMENDMENT to docs/35 §9, not a code edit, and this
agent did not make it.**

### Step 5 — GATES (c) and (d): PASS (numbers in Step 2 above)
(c) 11,389,623 exact-zero-runoff minibacia-days (35.96 % of the record) -> 0 with non-zero
erosion, max |erosion| exactly 0.0; converse holds on all 20,280,521 non-zero cells.
(d) 31,713,882 elements: 0 non-finite, 0 negative.

### Step 6 — ENSO signal, at BOTH scales (report only; NOT C5)
FLEET: La Nina 2011 2,976.77 t/d vs El Nino 2015-07..2016-06 1,052.48 t/d = **2.828x**
(observed 2.8x-4.6x primary, docs/34; docs/35 §5.4 says a simulated ratio is overstated by
~+10 %, so read ~2.6x corrected — same sign, same order, nothing more claimed).
PER-UNIT: per-minibacia ratio median **3.114** (p25 2.186, p75 4.613, p05 1.423, p95 8.745);
**8,579 of 8,672 minibacias (98.93 %)** have wet > dry. Per-minibacia rates: La Nina median
0.1142 t/d vs El Nino 0.0295 t/d. Monthly: wet month > dry month in **12 of 12** months.

### Step 7 — figures written (regenerable, gitignored per CLAUDE.md)
- `figures/deck/gen_c36_erosion_map.png` — (a) specific-erosion map, (b) COP90 elevation as
  the independent terrain reference, (c) the gate-(a) elevation-band panel with the
  bare-rock caveat printed on it. Sequential one-hue ramp for magnitude (never a rainbow);
  the t/km2/yr label carries the "INTERNAL model diagnostic / NOT a station or sub-basin
  yield (docs/23)" note in the panel itself.
- `figures/deck/gen_c36_seasonal_cycle.png` — daily basin erosion 2009-2018 with both ENSO
  windows shaded, plus the monthly climatology with La Nina 2011 and El Nino overlaid.
Both rendered and visually inspected for label collisions/overflow, then re-laid out twice.

### Step 8 — NOT DONE, deliberately
No calibration, no search, no edit to src/mgb_sediment.py or any frozen artifact, no git
operation, no convention change, no t/km2/yr presented as a station or sub-basin YIELD.
C3.5 (cross-check vs implementation B's musle.py) remains BLOCKED — that file is not in
this repo; not attempted.
STATUS: C3.6 COMPLETE. All four gates reported with numbers; gate (b) reported as a split
verdict with the failing direction named.
