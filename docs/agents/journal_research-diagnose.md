# Journal: research-diagnose

GOAL: diagnose empirically WHAT KIND of flood events the model misses (43 % of observed
POT absent). Parallel research track; does not block C3.

Hard constraints honoured: no git ops; write only this journal + data/processed/peakgap/
+ figures/deck/gen_peakgap.png; no calibration launch; no pd.read_csv on wide forcing;
no t/km2/yr yields.

## Step checklist
- [ ] S0 read scripts/c2b/peaks_measure.py, reuse POT definition verbatim
- [ ] S1 load discharge.npz + q_gauge_H2E.npz, align gauges/dates
- [ ] S2 build missed-event table (obs POT, no sim POT within +/-2 d)
- [ ] S3 covariates: area, month, mag/Q5, antecedent P7/P30, duration
- [ ] S4 answer 3a-3e each with a number
- [ ] S5 absent vs present-but-sub-threshold split
- [ ] S6 figure figures/deck/gen_peakgap.png
- [ ] S7 mechanism verdict + falsifier

## Log
- S0 DONE. Read scripts/c2b/peaks_measure.py; copied build_mask / local_maxima_above /
  pot_peaks VERBATIM (MIN_SEG 180, MAX_GAP 3, POT_SEP 10, POT_FRAC 0.6, threshold =
  observed Q5 for both obs and sim). Target reconciliation: 2,236 obs / 1,285 sim.
- S1 DONE. q_gauge_H2E.npz = 63 gauges x 3652 d (2009-2018). Gauge->minibacia from
  discharge.npz (all 63 present). topology upstream_area matches stored gauge area to
  5.7e-16 rel. Areas used ONLY as a covariate; no t/km2/yr anywhere.
- S2 running: catchment-mean forcing built as P @ W with W = own_area weights over the
  DFS upstream set of each gauge minibacia; antecedent windows read from forcing.npz
  (2008 available, so P30 is complete for Jan-2009 events).
- S2-S6 DONE. POT reconciliation EXACT: obs 2,236 / sim 1,285 / R_POT 0.5747 -> matches
  docs/33 s7. Events table 2,236 rows, data/processed/peakgap/events.csv.
  MATCHING SURPRISE (must be reported): +/-2 d 1-to-1 matching leaves 1,829 / 2,236 =
  81.8 % unmatched, NOT 43 %. The 43 % is a COUNT deficit; 81.8 % is an EVENT-identity
  deficit. Timing sensitivity (greedy 1-to-1): +/-0 d 5.1 %, 1 d 14.2 %, 2 d 18.2 %,
  3 d 20.8 %, 5 d 24.3 %, 7 d 26.4 %, 10 d 28.8 %, 15 d 31.2 %, 30 d 33.8 % matched
  (ceiling 57.5 %). So the deficit is NOT a lag; a month of slack recovers only 16 pts.
- 3a AREA: NO. Spearman(log A, per-gauge miss frac) rho=+0.018 p=0.89 n=62; terciles
  small 79.2 % (68-288 km2, n=853), mid 82.9 %, large 84.1 % (to 54,035 km2). Event-level
  MWU p=0.22. If anything LARGER catchments are worse.
- 3b ANTECEDENT: missed are DRIER but the storm rain is a stronger separator.
  P30 within-gauge pctile 0.459 vs 0.714 (rb -0.388); P7 0.448 vs 0.800 (rb -0.553);
  P3 (3-day storm) 0.441 vs 0.810 (rb -0.578); Pmax3 rb -0.512.
  Intensity ratio P3/P30 is LOWER for missed (0.146 vs 0.194, rb -0.339) -> ANTI-Hortonian.
  Within-gauge paired (33 gauges): med diff P30 -62.5 mm (0/33 ... 4/33 positive).
  Dry tail: lowest P30 tercile 93.9 % missed vs highest 70.2 %.
  Storm-confirmed subset (P3_pct >= 0.9, n=257): miss 51.8 % overall, dry 65.4 % (n=26),
  wet 48.3 % (n=145); rho(P30_pct, missed) = -0.127 p=0.041 -> real but SMALL residual.
- 3c DURATION: median 1 d missed vs 2 d captured; miss frac 84.9 % (1-2 d, n=1682),
  76.0 % (3-5 d), 68.7 % (6-10 d), 61.0 % (>10 d).
- 3d SEASON: chi2 63.1, p 2.5e-9, dof 11. Worst Jun-Sep (91.5 %, dry season), best
  Oct-Nov (75.9 %) and Mar-May (77.8 %) - the two rainy peaks.
- 3e SPLIT of the 1,829: absent (no rise) 737 = 40.3 % (33.0 % of all POT);
  present-but-sub-extreme 631 = 34.5 %; present and above the model's OWN Q5 461 = 25.2 %.
  Median sim/Q5obs at the missed events 0.616; 37.1 % below half the threshold;
  31.7 % within 20 % of it.
- KEY DISCRIMINATOR: obs peak per mm of forcing rain, ranked WITHIN gauge (area cancels)
  = 0.568 missed vs 0.286 captured (rb +0.397, p 4.6e-36). The catchment responded; the
  input rainfall did not.
- S6 figure figures/deck/gen_peakgap.png written (6 panels, 334 kB).
- Outputs: data/processed/peakgap/{events.csv,per_gauge.csv,match_sensitivity.csv,summary.json}
- S7 VERDICT.
  MIRROR STATISTIC: 68.3 % of the 1,285 SIMULATED POT have no observed counterpart within
  +/-2 d. The model does not just make too few peaks - it makes them on the wrong days.
  HORTONIAN-CANDIDATE SET (missed AND storm in the top within-gauge P3 tercile AND
  antecedent in the bottom P30 tercile) = 99 events = 5.4 % of the 1,829 missed / 4.4 % of
  all 2,236 POT. Even at 100 % attribution the missing infiltration-excess mechanism
  explains at most ~5 % of the gap. In the 'absent' class only 74/737 (10.0 %) have the
  storm present in the forcing at all; 408/737 (55.4 %) have P3 below the gauge's own
  33rd percentile.
  DATA-ARTIFACT BOUND: 224/737 'absent' events (30.4 %) are single-day spikes with
  obs_rise > 3x. Upper bound on the discharge-observation contribution = 224/2236 = 10.0 %.
  BEST SINGLE MECHANISM: the RAINFALL FIELD, not the runoff engine. The IDW gauge-
  interpolated daily rainfall does not contain the storms that produced the observed
  peaks (P3 rank-biserial -0.578, the largest of any covariate; obs peak per mm of
  forcing rain 0.568 vs 0.286 within gauge). This is the same r ~ 0.57 ceiling docs/22
  and docs/26 already identified, now expressed at event scale.
  FALSIFIERS (pre-stated): (1) rebuild the POT diagnosis on CHIRPS or a CHIRPS-gauge
  merge - if miss frac falls materially (say from 81.8 % toward the 57.5 % count ceiling)
  and the P3 separation collapses, rainfall is confirmed; if the miss frac barely moves,
  the explanation is WRONG and the engine is implicated. (2) If a Hortonian module were
  added and it recovered more than ~5 % of the missed events, my 99-event bound is wrong.
  (3) If sub-daily disaggregation of the SAME rainfall recovered the 1-2 d events, the
  daily time step - not the field - is the binding constraint.
  NOT DISTINGUISHED: within the 99-event Hortonian-candidate cell I cannot separate a
  missing infiltration-excess mechanism from residual rainfall-field error, because both
  are diagnosed against the same suspect rainfall field. The dry-antecedent gradient
  inside the storm-confirmed subset (65.4 % dry vs 48.3 % wet, rho -0.127 p 0.041) is
  also exactly what CORRECT ARNO saturation-excess behaviour would produce, so it is not
  evidence of a missing mechanism on its own.
  C3.5 remains BLOCKED (implementation B's musle.py is not in this repo) - not attempted.
- All checklist items closed. Files written: docs/agents/journal_research-diagnose.md,
  data/processed/peakgap/{events.csv,per_gauge.csv,match_sensitivity.csv,summary.json},
  figures/deck/gen_peakgap.png. No git operations performed.
