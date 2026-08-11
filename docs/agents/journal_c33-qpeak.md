# Journal — c33-qpeak

GOAL: choose and PRE-REGISTER the q_peak proxy for MUSLE, and write the quantified bias
statement BEFORE any sediment parameter is fitted. Deliverables:
- `docs/35_qpeak_preregistration.md` (choice + bias statement + C4 anti-compensation rule)
- `scripts/c3/qpeak.py` (implementation) + unit tests

## Step checklist
- [ ] 0. Journal created
- [ ] 1. Verify topology.npz fields (reach length, slope) exist — do not assume
- [ ] 2. Search repo for Fagundes et al. formulation (recoverable or not — state plainly)
- [ ] 3. Gather constants actually available: minibacia area, Qsur units, existing MUSLE code
- [ ] 4. WRITE docs/35 (choice, justification, bias arithmetic, C4 rule) — BEFORE code
- [ ] 5. Implement scripts/c3/qpeak.py
- [ ] 6. Write + run unit tests (hand case, monotonicity, Qsur=0)
- [ ] 7. Report

## Log

### Step 0 — journal created
docs/agents/ existed; 19 prior journals present. docs/35 is free (docs go 00..34).
No git operations will be performed by me.

### Step 1 — topology.npz fields VERIFIED (do not assume)
`data/processed/model_inputs_v2/topology.npz` keys (all n=8672 unless noted):
minibacia_id, own_area_km2, downstream_id, downstream_idx, topo_order_idx,
upstream_area_km2, n_upstream_links, hops_to_outlet, path_km_to_outlet, reach_km,
centroid_lon, centroid_lat, outlet_idx (scalar).
- `reach_km` EXISTS: 1 zero (the outlet), min>0 = 0.706, p05 3.019, med 5.074, p95 8.601,
  max 19.889 km.
- **SLOPE DOES NOT EXIST** in topology.npz. Confirms docs/31 §C3.3's 2026-08-10 note.
  => option (ii) SCS/Kirpich cannot be evaluated from shipped artifacts today.
- own_area_km2: min 1.63, p05 21.77, med 25.58, mean 29.65, p95 51.70, max 313.45,
  sum 257,097 km² (fleet total matches the documented basin area).

### Step 1b — slope feasibility probe (read-only, no files written)
- `data/processed/cop30_dem.tif` (6120×11160, 30 m) and `dem_coarse.tif` (680×1240) BOTH
  have bounds (-75.400, 8.200) → (-73.700, 11.300) — i.e. the **lower-Magdalena window
  only**, not the basin. `minibacias.tif` spans (-77.000, 1.400) → (-72.300, 11.400).
  Only **1,506 of 8,672 minibacias (17.4 %)** fall inside the processed 30 m DEM, and they
  are the FLAT lowland ones (proxy slope median 0.0056 m/m there).
- Minibacia id spaces match exactly (both n=8672, ids 1174…19256, intersection 8672), so
  the shortfall is DEM extent, not an id mismatch.
- The whole-basin DEM is COP90 inside `data/raw/dem/rasters_COP90_Correcte_Corrdinatzs.tar.gz`
  → single member `output_hh.tif` (260,274,553 B), **not extracted**. The project PDF
  explains why 30 m is a window: "30 m over the whole basin exceeds the tool's cell limit".
- Verdict: a basin-wide slope field is *buildable* but is **not a shipped artifact**;
  option (ii) would need that build first, and the only slope sample available today is
  biased flat (the erosive Andean flanks are outside it).

### Step 2 — Fagundes' own q_peak formulation: RECOVERED via the lineage paper
- Repo search: no Fagundes PDF. The only PDF is `Explanation_script_MGB_SA_Magdalena.pdf`
  (8 pp) — it mentions MUSLE twice and says only "Slope feeds the MUSLE LS factor";
  **no q_peak formulation**, no 0.208, no 11.8. So the *paper itself* is not in the repo.
- The parallel research-method agent recovered the formulation from the MGB-SED source
  paper Fagundes inherits — Buarque (2015, UFRGS, advisor Collischonn), eq. 7:
  **qpico = Dsup · A / 86.4**, preceded by "the peak rate of surface runoff in each pixel k
  is obtained considering a runoff volume uniform through the day" — i.e. the **daily-mean
  surface-runoff rate**, no unit hydrograph, no disaggregation. Applied **per 90 m pixel**
  (eq. 6), with eq. 5 `SED = 11.8 (Qsup·qpico·A)^0.56 · K·C·P·LS·FG`.
- **Therefore option (iii) ≡ option (i).** The floor estimate IS the source formulation.

### Step 3 — magnitudes from the frozen drivers (read-only)
`data/processed/sim_calibrated_v2/h2e_drivers.npz`, `qsur_rel_mm` (3652×8672, 2009-01-01…
2018-12-31, warm-up already excluded):
- per-day-per-minibacia: mean 1.803 mm, median 0.755, p90 5.104, p99 11.354, p99.9 18.619,
  max 74.392 mm; zero-fraction 0.000.
- per-minibacia annual: p05 74, med 509, p95 1724 mm/yr. Fleet total surface-runoff volume
  **167.4 km³/yr** (= 651 mm/yr over 257,097 km²).
- chosen proxy q_peak = Qsur·A/86.4 at minibacia scale: median 0.243 m³/s, p99 4.285,
  max 108.03; per-minibacia annual-max q_peak fleet median **2.178** m³/s (p05 0.317,
  p95 6.947).
- URH units (`parameters.npz:urh_fraction` × own_area): 32,782 non-empty URH cells
  (15.8 % of 8672×24), 3.78 URH per minibacia; URH area p05 0.544, med 4.762, p95 24.485,
  max 169.98 km².
- MUSLE scale factor N^(2β−1), N = A/0.0081 km² (COP90 pixel): 1.657 at 0.544 km²,
  **2.149 at the median URH 4.762 km²**, 2.630 at 25.58 km², 3.552 at 313 km².

### Step 4 — bias arithmetic (β = 0.56), computed
R^0.56: R_AMS 0.820→0.8948 (−10.5 %); geo-mean 0.810→0.8887 (−11.1 %); R_Q1 0.847→0.9112
(−8.9 %); R_Q5 0.975→0.9859 (−1.4 %); La Niña-11 R_AMS 0.808→0.8875 (−11.3 %);
El Niño-15/16 R_AMS 0.686→0.8097 (−19.0 %); 2018 0.589→0.7435 (−25.7 %);
CAL 12-14 0.648→0.7843 (−21.6 %). R_POT 0.567→0.7278 if (wrongly) exponentiated.
Contrast inflation (La Niña/El Niño) = 0.8875/0.8097 = **1.096**.
POT counts 1285/2236 = 0.5747 (fleet-median R_POT 0.567).
SCS/daily-mean amplification = 86.4/(4.806·T_p[h]) = 17.978/T_p: 5.99 at 3 h, 2.99 at 6 h,
1.50 at 12 h, 1.00 at 18 h.
All period peak ratios read from docs/33 §7.3–§7.4 (executed output), not re-derived.

Next: write docs/35 (choice + bias + C4 rule) BEFORE any code.

### Step 5 — docs/35 WRITTEN (before any code)
`docs/35_qpeak_preregistration.md` created 2026-08-11. Contains, in this order:
§1 what MUSLE needs vs what the engine has; §2 input audit (reach_km yes, slope NO,
DEM covers 17.4 % of minibacias, COP90 archive unextracted); §3 the three candidates with
formulas and assumptions, incl. the Buarque (2015) eq. 7 recovery showing (iii) ≡ (i);
**§4 THE CHOICE** (Qsur·a/86.4 at a_p = 0.0081 km², 5 numbered justifications);
**§5 THE BIAS STATEMENT** (5.1 proxy 1.26–2.75× i.e. −21…−64 %; 5.2 measured deficits
with R^0.56 column and the explicit warning that R_POT is a COUNT and must NOT be
exponentiated; 5.3 the registered lower-bound statement −10.5 % minimum, −19.0 % El Niño,
−10…−45 % with missing events, ≈2.1× total vs a sub-daily model; 5.4 ENSO contrast
overstated by +10 %; 5.5 what is not claimed);
**§6 THE C4 ANTI-COMPENSATION RULE** (α expected 5.9–23.6, watch 23.6–35.4, HARD STOP
α > 35.4 = 3× Williams or α < 3.9; §6.2 the scale trap with the rescaled thresholds per
application unit; §6.3 β hard stop outside 0.45–0.65; §6.4 tests T1 residual-by-quantile
(+25 % below-Q50 trigger), T2 ENSO-split (+10 %), T3 reporting; §6.5 what IS permitted);
§7 implementation spec; §8 open items (incl. C3.5 still BLOCKED, FG omission points the
other way); §9 registration record.
Also recorded a CORRECTION: docs/31 §C3.3 says the peak bias is "worst at the largest" —
C2b measured ρ(R_AMS, area) = +0.088, p = 0.49, i.e. no area dependence (docs/33 §7.5).

RISKY-OP NOTE: none of this touched data, git, or any calibration. Read-only measurements
only. Next: write scripts/c3/qpeak.py + tests/test_qpeak.py, then run pytest.

### Step 6 — implementation + tests (written AFTER docs/35, as required)
`scripts/c3/qpeak.py` (pure functions, no I/O, no globals; placement justified in
docs/35 §7 — Phase B's src/ is frozen twice, and src/mgb_sediment.py will import this):
  qpeak_daily_mean (THE registered proxy), COP90_PIXEL_AREA_KM2 = 0.0081,
  qpeak_scs_triangular + time_of_concentration_kirpich (REJECTED option (ii), retained so
  the §5.1 bound is reproducible), peak_amplification, musle_scale_factor,
  rescale_alpha_reference, sediment_bias_ratio, check_musle_parameters, and the §6 bands
  as importable constants (ALPHA_EXPECTED_LOW 5.9 / HIGH 23.6, ALPHA_HARD_STOP_HIGH 35.4,
  ALPHA_HARD_STOP_LOW 3.933, BETA_HARD_STOP 0.45/0.65).

`tests/test_qpeak.py` — 30 tests, all green:
  - hand case 10 mm over 25 km² = 250,000 m³ / 86,400 s = 2.8935185185185186 m³/s
    (abs 1e-12); unit case 1 mm/1 km² = 1/86.4; pixel case 81/86400.
  - Qsur = 0 → 0; area = 0 → 0; strict monotonicity in Qsur and in area; exact linearity;
    array == scalar path (atol 1e-15) + broadcasting; negatives raise ValueError;
    NaN propagates (not silently zeroed).
  - SCS reduces to 0.2081; peak_amplification == the exact ratio of the two proxies at
    T_p = 3/4/6/9/12/18 h and reproduces 5.99/4.49/2.99/2.00/1.50/1.00; SCS > daily mean
    for every T_p < 18 h (the FLOOR claim, tested); Kirpich hand case + monotonicity +
    rejects reach 0 (the outlet) and slope 0.
  - musle_scale_factor == 1 at the pixel scale, reproduces 1.657/2.149/2.630/3.552, and
    is verified to BE the aggregation identity (pixelwise sum vs lumped, rel 1e-10);
    rescale_alpha_reference gives 5.49 / 4.49 / 3.32.
  - sediment_bias_ratio reproduces the whole docs/35 §5.2 column (abs 5e-5) and the
    contrast inflation 1.096.
  - C4 rule: (11.8, 0.56) ok; alpha 40 STOP; alpha 28 watch; alpha 2 STOP; beta 0.70 STOP;
    beta 0.40 STOP; **the scale trap** — alpha 12 is "ok" at pixel scale and "watch"
    against a rescaled reference of 4.49 at minibacia scale, alpha 20 lumped STOPs.

VERIFIED FROM EXECUTED OUTPUT (not exit codes):
  `python3.10 -m pytest tests/test_qpeak.py -q` -> "30 passed in 0.30s"
  `python3.10 -m pytest tests/ -q`             -> "46 passed in 1.36s" (no regressions)

### Step 7 — done
Ordering requirement met: docs/35 §4 (choice), §5 (quantified bias), §6 (C4 rule) were all
written and saved before scripts/c3/qpeak.py was created. Files touched: docs/35_qpeak_
preregistration.md, scripts/c3/qpeak.py, tests/test_qpeak.py, this journal. No git, no
calibration launched, no yields in t/km²/yr, no forcing CSV read with pandas.
