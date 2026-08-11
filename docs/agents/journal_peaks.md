# Journal - agent SLUG=peaks

## Goal
C2b.2: measure whether simulated flood peaks are biased, and by how much.
Follow docs/33 s2 EXACTLY (frozen). Propagate bias to sediment via MUSLE beta~0.56.

## Step checklist
- [ ] 1. Read docs/33 s2 (frozen pre-registration) + locate artifacts
- [ ] 2. Identify calibration-safe gauges + obs/sim series
- [ ] 3. (a) AMS per water year, sim/obs ratio, per-gauge median
- [ ] 4. (b) Q1 / Q5 exceedance flows + ratios
- [ ] 5. (c) POT count above observed Q5, sim vs obs
- [ ] 6. (d) timing lag, top-10 observed events, median abs lag
- [ ] 7. Fleet medians + by-period breakdown + vs catchment area
- [ ] 8. Apply H-PEAK rule, state verdict quoting the rule
- [ ] 9. Sediment propagation R^0.56
- [ ] 10. Figure figures/deck/gen_peaks.png
- [ ] 11. Write new section into docs/33

## Log
- (start) journal created.
- Step 1 DONE: read docs/33 (frozen). Key: s2.3 defines AMS/Q1/Q5/POT exactly; H-PEAK gate = fleet-median R_AMS in [0.85,1.15] OR fleet-median R_Q1 in [0.85,1.15] -> refuted if either outside. R_Q5 and POT diagnostic only.
  ISSUE (journalled, followed anyway): task brief item 1d (timing lag) is NOT in the frozen s2.3. It will be computed and reported as an EXTRA diagnostic, clearly labelled non-preregistered, and cannot touch the verdict.
- Step 2 DONE: artifacts confirmed on disk. q_gauge_H2E.npz: dates(3652) 2009-01-01..2018-12-31,
  gauge_code(63), gauge_upstream_area_km2(63), q_obs_m3s(3652,63) with NaN = invalid (21.93% NaN),
  q_sim_fit_m3s(3652,63) no NaN. Valid-day count per gauge: min 867, p25 2197, median 3145, max 3650.
  Period masks read from src/calib_v2.py:484-493 (CAL 2012-14; LaNina 2011; ElNino 2015-16; other 09/10/17; 2018).
  ISSUES journalled (rules followed as frozen):
   * brief says "water year"; frozen s2.3(a) says CALENDAR year 2009-2018 with >=300 valid days -> CALENDAR used.
   * s2.3 says "same masked, paired day set as s2.1" -> s2.1 day handling (<=3d gap interp, >=180d segments)
     applied as PRIMARY; raw-mask variant reported as robustness, cannot change the gate.
   * s2.1's >=1095-day gauge-exclusion is written for the BFI statistic only; not applied to peaks, but counted.
   * POT independence needs a candidate rule (not frozen): all local maxima above threshold, then iterative
     merge while (separation <10 d) OR (min valid flow between >= 0.6 x lower peak). Identical for obs and sim.
   * timing lag (brief 1d) not pre-registered: window +/-15 d chosen by this session, +/-10/+/-20 sensitivity.
- NEXT: write scratch script and run.
- Steps 3-7 DONE. Script: scratchpad/peaks.py -> peaks_per_gauge.csv (63 rows) + peaks_fleet.json.
  FLEET MEDIANS (full 2009-2018 scored record, n=63 gauges):
    R_AMS 0.820 (IQR 0.529-1.186; geomean 0.810) ; R_Q1 0.847 (IQR 0.633-1.234)
    R_Q5 0.975 (IQR 0.740-1.279) ; R_POT 0.567 ; POT totals sim 1285 vs obs 2236 = 0.575
    median abs lag 4 d (signed 0 d) ; per-gauge Pearson r median 0.599
  Per-gauge spread R_AMS: 36/63 below 0.85, 9 in band, 18 above 1.15 (range 0.247-3.169).
  Robustness (raw unsegmented mask): R_AMS 0.820, R_Q1 0.840, R_Q5 0.974 -> verdict unchanged.
  BY PERIOD (R_AMS / R_Q1 / R_Q5 / R_POT medians):
    CAL 2012-14        0.648 0.863 0.957 0.423
    VAL all            0.854 0.879 0.954 0.667
    VAL La Nina 11     0.808 0.894 0.977 0.500
    VAL El Nino 15-16  0.686 0.744 0.858 0.464
    VAL other 09/10/17 0.794 0.927 0.958 0.571
    VAL 2018           0.589 0.744 0.863 0.375
  AREA: spearman(log10 area, R_AMS) = +0.088 (p 0.49, n 63) -> NOT significant.
    terciles small/mid/large R_AMS 0.769 / 0.725 / 0.981; R_Q1 1.001 / 0.839 / 0.847;
    R_Q5 1.257 / 0.965 / 0.888; r_pearson 0.530 / 0.589 / 0.739.
    spearman(log10 area, r_pearson) = +0.580 (p 6.3e-7) -> correlation DOES improve with area
    (reproduces the docs/26 pattern); peak bias does NOT follow it in rank terms.
  EVENT-MATCHED (addendum, scratchpad/lagcheck.py, 599 events): sim/obs peak magnitude at the 10
    largest observed events = 0.552 median (IQR 0.305-0.887); 36.4% of events matched within +/-1 d,
    44.9% +/-2 d, 56.9% +/-5 d, 15.2% at the +/-15 d window edge (so median |lag| is partly
    window-driven: 2/4/6 d at +/-10/15/20). Signed median 0 d -> no early/late bias.
- Step 8 VERDICT: H-PEAK REFUTED. docs/33 s1 rule: "Refuted if the fleet-median AMS ratio R_AMS
  lies outside [0.85, 1.15], OR the fleet-median Q1-exceedance ratio R_Q1 lies outside [0.85, 1.15]."
  BOTH are outside, low: R_AMS 0.820 < 0.85 and R_Q1 0.847 < 0.85. Either alone refutes.
- Step 9 SEDIMENT: R^0.56 with R = R_AMS 0.820 -> 0.895, i.e. -10.5 % sediment.
  From R_Q1 0.847 -> 0.911 (-8.9 %). El Nino R_AMS 0.686 -> 0.810 (-19.0 %).
- NEXT: figure + docs/33 new section.
- Step 10 DONE: figures/deck/gen_peaks.png written (155,570 bytes, verified by rendering the PNG,
  not by exit code). Panel A ranked R_AMS bars with [0.85,1.15] band; panel B R_AMS vs area (log-log)
  with tercile medians.
- Step 11 DONE: docs/33 new section "## 7 - C2b.2 RESULTS: flood-peak bias (H-PEAK)" appended
  (7.1 verdict .. 7.8 issues). s1-s5 untouched, verified by grep of the heading list.
  NOTE: the concurrent `bfi` agent appended its "## 6" AFTER my "## 7" while I was writing, leaving
  7 before 6 in the file. Fixed by a programmatic move of the s7 block (14,318 chars, byte-identical)
  to the end; heading order is now 0,1,2,3,4,5,6,7 and both sections are intact.
  s6 records H-BFI HOLDS (median |dBFI| 0.01625 vs IQR gate 0.02845), so the docs/33 s3.1 outcome
  is "holds / refuted" -> refit H2E-S with the PEAK term only at (0.34, 0.34, 0.17, -, 0.15).
  s7.1 updated to state that definitively.
- Persistent artifacts: data/processed/c2b/peaks_per_gauge.csv (63 rows + header = 64 lines),
  peaks_summary.json, peaks_measure.py.
- DONE. No git commands run. No frozen artifact modified.
