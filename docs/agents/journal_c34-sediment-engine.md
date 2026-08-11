# Agent journal: c34-sediment-engine

GOAL: implement `src/mgb_sediment.py` — MUSLE hillslope erosion on the frozen H2E drivers —
to the same engineering standard as `src/mgb_hydrology.py`, plus `tests/test_sediment.py`.

Sed = alpha * (Q_sur * q_peak * A)^beta * K * C * P * LS2D

## Checklist
- [ ] S0 verify inputs on disk (h2e_drivers.npz, minibacia_soil_params.csv, urh_cp_factors.csv,
      minibacia_ls2d.csv, urh_ls2d.csv, scripts/c3/qpeak.py)
- [ ] S1 read src/mgb_hydrology.py, record conventions to match
- [ ] S2 read scripts/c3/qpeak.py + docs/35 (registered q_peak proxy)
- [ ] S3 inspect driver arrays (shapes, dtypes, units) via npz headers only (no wide-CSV reads)
- [ ] S4 implement src/mgb_sediment.py
- [ ] S5 tests/test_sediment.py
- [ ] S6 pytest tests/ -q — report count
- [ ] S7 full basin-decade run: NaN-free + mass ledger closes exactly

HARD RULES honoured: no git ops; no calibration; no edits to src/mgb_hydrology.py or frozen
artifacts; never pd.read_csv the wide forcing CSVs; verify from executed output; yields in
t/km2/yr embargoed (absolute flux only).

## Log
- S0 start.

- S0 DONE. All named inputs exist:
  h2e_drivers.npz 546,366,478 B; minibacia_ls2d.csv 615,882 B (8672 rows);
  urh_ls2d.csv 2,084,696 B (32,782 rows); urh_cp_factors.csv (8 classes);
  minibacia_soil_params.csv (K: n=8672, 0 NaN, 0 non-positive, min 0.019 med 0.03055 max 0.0495);
  scripts/c3/qpeak.py + tests/test_qpeak.py present.
- S1 DONE (read src/mgb_hydrology.py, 1129 lines). Conventions to match: module docstring with
  UNITS / REJECTED-ALTERNATIVES / WARNING sections; frozen dataclass topology + params dataclass
  with per-field default provenance; expand()-style validation that raises rather than coerces;
  time-only loop, numpy over the 32,782 active (minibacia,URH) cells; two independent backends
  cross-checked by tests; structural mass accounting with the guard term RETURNED not swallowed.
- S3 DONE. h2e_drivers.npz keys/shapes: dates (3652,) datetime64[D] 2009-01-01..2018-12-31;
  minibacia_id (8672,) == minibacias.csv order (verified, array_equal True);
  own_area_km2 == minibacias.csv area_km2 (max abs diff 0.0);
  qsur_gen_mm / qsur_rel_mm / q_local_mm / reach_inflow_m3s / q_reach_m3s all (3652, 8672) float32,
  0 NaN. qsur_rel_mm max 74.392 mm/d. meta: cell H2E, et_stress fao56, theta_crit 0.6,
  balance residual_relative 9.66e-17, and an explicit "musle_qsurf_choice: NOT MADE HERE".
- S2 DONE. docs/35 §4 registers, verbatim:
  Sed_URH = (A_URH/a_p) * alpha * (Qsur * Qsur*a_p/86.4 * a_p)^beta * K*C*P*LS2D , a_p=0.0081 km2,
  Qsur = qsur_rel_mm (docs/35 §1 table). Open items it hands to C3.4: (3) FG must be quantified or
  explicitly set to 1 with a reason, (4) C3.4 must state whether it uses Buarque's delivery
  linear reservoir.
- S3b geometry joins verified: urh_fractions nonzero cells == urh_ls2d (mini,urh) rows, 32,782,
  zero-symmetric-difference; ls2d_hs 0 NaN, min 1.465e-4, max 384.58, 0 zeros.
  AREA CROSS-CHECK (recorded, matters): urh_fractions*minibacias.area vs urh_ls2d.area_km2 ->
  ratio median 1.0021, p25 0.9983, p75 1.0097, p99 1.827, max 6.604; 12.89 % of cells differ by
  >5 %; basin totals 257,096.93 vs 251,723.51 km2 (LS2D raster 2.09 % smaller = DEM nodata).
  DECISION: areas come from urh_fractions x minibacias.csv (same area the water balance and the
  frozen drivers use); ls2d_hs is consumed as an INTENSIVE per-cell mean. Recorded as a warning
  in the module, not silently.
- next: S4 write src/mgb_sediment.py.
- S4 DONE. src/mgb_sediment.py written (860 lines). Implements the docs/35 §4 registered form
  verbatim: Sed_URH = (A_URH/a_p)*alpha*(Qsur*q_peak*a_p)^beta*K*C*P*LS2D*FG, q_peak from the
  imported scripts/c3/qpeak.py (loaded by path, NOT re-implemented), a_p = 0.0081 km2.
  Defaults: alpha 11.8, beta 0.56 (Williams 1975, documented as STARTING VALUES for C4),
  FG = 1.0 explicit (docs/35 §8 item 3 answered: no rock-fragment layer exists; FG<=1 so 1.0
  RAISES the load - the only term against the lower-bound direction),
  tau_delivery_days = 0.0 (docs/35 §8 item 4 answered: the registered Qsur is qsur_rel_mm,
  already through the engine's surface reservoir, so Buarque's delivery reservoir is
  implemented but defaults to pass-through to avoid double-counting the lag),
  ls2d_column = 'ls2d_hs' (ls2d.py: "the column MUSLE should use").
  Two backends ('cells' reference / 'collapsed' identity) cross-checked by tests.
- S5 DONE. tests/test_sediment.py, 35 tests.
- S6 GATE MET: python3.10 -m pytest tests/ -q -> **81 passed** in 6.59 s (35 new + 46 pre-existing),
  0 failed, 0 skipped. tests/test_sediment.py alone: 35 passed.
- S7 DONE, full basin-decade (3652 d x 8672 minibacias, 32,782 URH cells), registered defaults:
  * MASS LEDGER CLOSES EXACTLY: residual_t == 0.0 (bitwise, not a tolerance), exact=True,
    delivered_t == eroded_t == 6,843,119.50146461 t, store_end == 0.0.
  * NaN-free: 0 non-finite in the (3652, 8672) delivered array, in cell_eroded_t, and in the
    daily basin series; all values >= 0.
  * runtime 1.50 s (collapsed, with the 126 MB output array); cells backend 2.0 s projected
    -> the second backend is a CROSS-CHECK, not an optimisation (docstring corrected: my
    "~30x faster" guess was wrong by 20x, measured 1.5x).
  FLEET scale: 6.843 Mt over 9.999 yr = 0.6844 Mt/yr; daily basin total median 1,504.7 t/d,
    p99 6,674.4, max 9,000.7.
  PER-UNIT scale: per-minibacia 0.0675 t/day median (p25 0.0122, p75 0.1993, p95 0.5579,
    max 142.74, min 3.09e-06); per-URH-cell 0.00615 t/day median, p95 0.198, max 112.9,
    1,131 of 32,782 cells exactly 0 (open water, C=0). Concentration: 415 minibacias (4.79 %)
    carry 50 % of basin erosion, 3,225 carry 90 %.
  Attribution by land class (share of total): Forest 36.5 %, Bare 35.6 %, Grassland 27.3 %,
    Cropland 0.47 %, Urban 0.06 %, Shrub 0.06 %, Wetland 0.001 %, Water 0.000 %.
    NB Bare is 0.196 % of area and 35.6 % of the erosion - the C3.2 bare-rock caveat is live.
  ENSO diagnostic (uncalibrated, alpha cancels in a ratio, beta does not): La Nina 2011
    2,976.8 t/d vs El Nino 2015-07..2016-06 1,052.5 t/d = **2.83x**, against the OBSERVED
    2.8x-4.6x primary (docs/34) - and docs/35 §5.4 says a simulated ratio is overstated by
    ~+10 %, so read it as ~2.6x corrected. Same sign, same order; nothing is claimed beyond that.
- UNIT-CONVENTION FINDING (recorded, NOT acted on): the registered pixel_km2 convention gives
  0.6844 Mt/yr of GROSS HILLSLOPE erosion, i.e. 210x-269x BELOW the docs/34 §1.8 outlet
  anchors (144 / 184 Mt/yr) - and gross hillslope erosion must EXCEED the outlet load.
  Williams' literal m3-volume convention is exactly 1000^0.56 = 47.8630x larger = 32.76 Mt/yr,
  4.4x-5.6x below the anchors. Closing the registered gap with alpha needs alpha ~ 2480 (70x
  past the docs/35 §6.1 hard stop of 35.4); absorbing just the convention factor needs
  alpha ~ 565 (16x past). Implemented as SedParams.volume_convention with 'pixel_km2' as the
  default and 'williams_m3' available for the C3.6 diagnostic only; a default change is an
  AMENDMENT to docs/35 §9, not a code edit. The pre-registered hard stop is doing its job.
- Other measured sensitivities (diagnostics, not adopted): qsur_gen_mm instead of the
  registered qsur_rel_mm = 1.1249x (0.7699 vs 0.6844 Mt/yr) - docstring corrected, my guessed
  "~1.6x" was wrong; uncapped ls2d instead of ls2d_hs = 2.225x at uniform Qsur.
- MEASURED FACT worth carrying forward: qsur_rel_mm has NO exact zeros anywhere (fleet min
  2.0e-43 mm/d) because it is the output of an exponential linear reservoir. The
  zero-runoff-zero-erosion gate is therefore exercised on qsur_gen_mm, which does contain
  exact zeros. Pinned in a test so nobody assumes dry days exist in the released field.
- C3.5 (cross-check vs implementation B's musle.py): STILL BLOCKED - that file is not in this
  repo. Not attempted, per instruction.
- NOT DONE, deliberately: no calibration, no search, no edit to src/mgb_hydrology.py or to any
  frozen artifact, no t/km2/yr yield anywhere (nothing in the module divides by an area).
- FINAL GATE RE-RUN after docstring corrections: python3.10 -m pytest tests/ -q -> 82 passed
  (36 in tests/test_sediment.py), 0 failed, 0 skipped, 6.8 s.
- Added test_real_geometry_join_is_not_scrambled: 300 random cells re-looked-up straight from
  the four CSVs (LS2D, K, C, P, area) - 0 mismatches; cell areas tile the basin exactly
  (257,096.93 km2 both ways). A mis-join changes no total and is invisible to distributional
  tests, so it is pinned element-wise.
- File sizes: src/mgb_sediment.py 1,090 lines of which lines 1-260 are the module docstring
  (equation provenance, units + the open unit question, rejected alternatives, inherited
  bias) - ~830 lines of code+API docstrings. tests/test_sediment.py 555 lines, 36 tests.
- STATUS: C3.4 COMPLETE. Files touched: src/mgb_sediment.py (new), tests/test_sediment.py
  (new), docs/agents/journal_c34-sediment-engine.md (this file). Nothing else; no git ops.
