# Journal — agent `bfi` (C2b.1, H-BFI)

**Goal:** measure C2b.1 per docs/33 §2.1 — Eckhardt-filtered BFI on OBSERVED vs SIMULATED
discharge at the 63 calibration-safe gauges, apply the frozen H-BFI rule, state the verdict.

Frozen inputs I must not change: filter form, `a = exp(-1/k_obs)` from
`calib_v2.recession_k` on the OBSERVED series, `BFImax = 0.80` (0.50 as reported
robustness), 30-day warm-up per segment, gaps ≤3 d interpolated, segments ≥180 valid days,
gauge needs ≥1095 valid scored days, period 2009–2018 scored (2008 warm-up), identical day
mask on sim.

**H-BFI rule (docs/33 §1), quoted:** "Refuted if the fleet-median `|BFI_sim − BFI_obs|`
exceeds the between-gauge spread of `BFI_obs`, where 'spread' is fixed here as the
interquartile range (p75 − p25) of `BFI_obs` across the gauge set of §2.4."

## Checklist

- [ ] 0. Read docs/33 §2 (frozen spec). DONE.
- [ ] 1. Implement `src/baseflow.py` (Eckhardt filter + MRC recession estimator).
- [ ] 2. GATE: synthetic unit tests (pure exponential recession -> BFI ~ 1; spike train ~ 0).
- [ ] 3. Load observed (`model_inputs_v2/discharge.npz`) + simulated
      (`sim_calibrated_v2/q_gauge_H2E.npz`), calib-safe gauges, identical mask.
- [ ] 4. Per-gauge BFI_obs / BFI_sim / diff; fleet median, IQR, p10-p90, median |diff|.
- [ ] 5. By-period breakdown (CAL / La Nina / El Nino / other / 2018).
- [ ] 6. Consistency check vs internal partition 19.5 % (labelled DIFFERENT quantity).
- [ ] 7. Verdict against the quoted rule.
- [ ] 8. Figure `figures/deck/gen_bfi.png`.
- [ ] 9. New section appended to docs/33 (do not touch frozen §1–§3).

## Log

- 2026-08-10 — journal created; docs/33 read in full. Starting step 1.
- 2026-08-10 — step 1 DONE: `src/baseflow.py` written. Eckhardt forward filter, gap fill,
  segmentation, `bfi_series`, `bfi_over` (sub-period ratio without re-filtering),
  `master_recession_k` (delegates to `calib_v2.recession_k` — docs/33 names that estimator
  by name; a second implementation would be a second thing to drift), `recession_a`.
- 2026-08-10 — **step 2 GATE PASSED: 9/9** (`python src/baseflow.py --selftest`).
  1. exponential recession BFI = 1.000000000000 (analytic fixed point, tol 1e-9)
  2. spike train BFI = 0.062014 == analytic (1-a)B/(1-aB) = 0.062014, bar < 0.10
  3. 0 <= b <= y everywhere (max(b-y) = 0.000e+00)
  4. mixed hydrograph strictly interior: BFI(0.50) 0.4573 < BFI(0.80) 0.6295
  5. gap rule: 3-day hole filled exactly, 4-day hole breaks the record
  6. segments [(0,200),(260,500)], n_scored 380 = 440 − 2×30 warm-up
  7. sub-180-day segments dropped entirely (n_scored 0, BFI NaN)
  8. MRC recovers k = 25.000 d from a synthetic 25 d sawtooth over 12 segments
  9. a = exp(-1/k) round trip
  ISSUE (test defect, fixed, recorded): check 8 first returned 27.078 d vs a true 25.0 d.
  Cause was MY synthetic, not the estimator: I had written `300*exp(-t/K) + 1.0`, and an
  additive offset curves the series in log space, so an OLS fit of ln Q must read k high.
  Removing the offset gives 25.000 exactly. No threshold was loosened.
  NOTE: a CONSTANT series gives BFI = BFImax, not 1 — a correct Eckhardt property; no test
  asserts otherwise.
- 2026-08-10 — verified on disk before any filtering: `q_gauge_H2E.npz` gauge_code order
  == `discharge.npz` gauge_code[is_calibration_safe] (63); dates 2009-01-01..2018-12-31
  align with rows 366:4018 of discharge.npz; `isnan(q_obs_m3s)` == `~q_valid` exactly
  (50,464 invalid of 230,076); values equal where valid; q_sim_fit has 0 NaN. Valid days
  per gauge: min 867, median 3145, max 3650.
- 2026-08-10 — steps 3-5 DONE. Driver: scratchpad `run_bfi.py`; outputs
  `data/processed/c2b/bfi_per_gauge.csv` (63 rows) + `bfi_summary.json`.
  **55 of 63 gauges included**; 8 excluded for `n_scored < 1095` after segmentation
  (23087300, 23127050, 26127150, 26157080, 26187170, 26197020, 26217050, 28047010).
  0 gauges failed to yield a recession constant. k_obs median 10.44 d (p10 5.34, p90
  17.24) -> median a = 0.9087.
  **BFImax 0.80 (the gate):** median BFI_obs **0.7811**, median BFI_sim **0.7965**,
  IQR(BFI_obs) **0.02845** (p25 0.7593, p75 0.7878), p10-p90 **0.0673**, SD 0.0307
  (context only, per §1). Fleet **median |BFI_sim − BFI_obs| = 0.01625**.
  0.01625 <= 0.02845 -> **H-BFI NOT REFUTED**.
  **Robustness BFImax 0.50 (cannot change the verdict):** med|diff| 0.00308 vs IQR
  0.00487 -> same verdict; no flip.
  Per gauge: 48/55 sim > obs, 7/55 sim < obs; median signed +0.0128; max |diff| 0.1173
  (21237040); 23/55 gauges individually exceed the fleet IQR; 0 exceed 0.20.
  Sub-periods (reported, NOT gates — §2.4 evaluates every gate on 2009-2018):
  CAL 0.0186 vs 0.0281; VAL all 0.0154 vs 0.0286; La Nina 11 0.0183 vs 0.0358;
  **El Nino 15-16 0.0295 vs 0.0290 — would refute on that window alone, by 0.0005**;
  other 09/10/17 0.0191 vs 0.0262; 2018 0.0157 vs 0.0336.
  Consistency check (DIFFERENT quantity, no threshold): internal baseflow 19.5 % vs
  filter-derived median BFI_sim 0.7965 -> gap **+0.602**; 0/55 gauges below 0.195.
  Sensitivity (gap-fill symmetry): filtering sim on its own values across the <=3 d holes
  instead of the interpolated ones moves BFI_sim by a median 6.2e-05, max 1.8e-03.
  ISSUE journalled, not acted on: both distributions are compressed against the BFImax
  ceiling (BFI_obs range 0.658-0.799; 12/55 above 0.79), so the yardstick IQR is only
  0.028 and r(BFI_sim, BFI_obs) = **0.094** — the model carries almost no between-gauge
  information about flow character even though it passes. r(diff, BFI_obs) = -0.825.
  The rule is frozen; the verdict stands as computed and the caveat goes in the write-up.
- 2026-08-10 — step 6 DONE: `figures/deck/gen_bfi.png` (233,710 bytes, 2210x951).
  Panel A: BFI_obs vs BFI_sim scatter, 1:1 line, ±IQR band, colour = upstream area (log
  viridis), BFImax ceiling marked. Panel B: per-gauge difference ranked, same colour scale,
  ±IQR guides. Verified by opening the rendered PNG (twice: first render had a colorbar
  label / y-label collision and an IQR label clipped by the tall bars; both fixed).
- 2026-08-10 — step 7 DONE: appended **§6** to `docs/33_c2b_preregistration.md`.
  §1–§5 untouched (verified: file still opens with the identical first 6,000 chars).
  CONCURRENCY NOTE: the `peaks` agent (C2b.2) appended **§7** to the same file while I was
  measuring, and deliberately left §6 free. My first append landed after §7; the file was
  then reordered so §5 → §6 → §7 and both sections verified intact
  (headings 0,1,2,3,4,5,6.0-6.6,7.1-7.8 all present, 921+ lines).
  Their result: **H-PEAK REFUTED** (R_AMS 0.820, R_Q1 0.847, band [0.85, 1.15]).
  I therefore resolved my §6.6 to §3.1's third row: refit with the PEAK term only,
  (0.34, 0.34, 0.17, —, 0.15). `e_bfi` is NOT triggered.

## VERDICT

**H-BFI is NOT REFUTED.** Rule quoted: "Refuted if the fleet-median |BFI_sim − BFI_obs|
exceeds the between-gauge spread of BFI_obs, where 'spread' is fixed here as the
interquartile range (p75 − p25) of BFI_obs across the gauge set of §2.4."
Measured: **0.01625 ≤ 0.02845**. Robustness BFImax 0.50: 0.00308 ≤ 0.00487, same verdict,
no flip. n = 55 of 63 (8 excluded on the ≥1,095-scored-day rule, named in §6.1).

All checklist items complete.
