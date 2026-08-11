# Agent journal — prereg-c2b

GOAL: write and FREEZE `docs/33_c2b_preregistration.md` (C2b: validate the MUSLE drivers —
surface runoff partition and peak flow — that total-discharge calibration never tested), and
append a one-line pointer to CLAUDE.md's read-first list.

Constraint: nothing in phase 2 may be measured before this file exists. Thresholds are frozen
on write.

## Step checklist

- [x] 1. Create this journal (mkdir -p docs/agents)
- [ ] 2. Read source docs: 30 (§1 freeze), 31 (stage order), 26 (§5.1 objective/weights), 29
      (prereg pattern), 32 (C1 prereg format)
- [ ] 3. Establish n for the calibration-safe gauge set from
      `data/processed/model_inputs_v2/gauges.csv` (read-only; not a filename count)
- [ ] 4. Recover the exact H2E objective weight vector from code/docs (needed for the
      re-weighting arithmetic in §3)
- [ ] 5. Write docs/33 with all five sections, every threshold justified and FIXED
- [ ] 6. Append one-line pointer to CLAUDE.md read-first list
- [ ] 7. Verify both files on disk (grep the section headings, not exit codes)

## Log

- Step 1 done: journal created.
- Step 2 done: read docs/30 (§1 freeze, §3 stages, §5 background), docs/31 (full workplan,
  C2.1/C4.2/C5.4 doc numbers, B1 CHIRPS gates), docs/26 (§2 objective changes, §5.1 rails,
  addendum A.1–A.6). Key extracted numbers:
  - objective weights on disk `src/calib_v2.py:95` — `W_KGE, W_LOG, W_REC = 0.40, 0.40, 0.20`,
    sum 1; `REC_SCALE = ln 2`; `c2m(k) = k/(2-k)` (Mathevet bounded transform);
    `blend()` renormalises over the terms DEFINED at each gauge.
  - CHIRPS gates (docs/18 §15, docs/31 B1): volume within 1 % of **2,036.4 mm/yr**
    (2009–17 area-weighted areal mean); LOOCV median daily r > **0.429** (287 gauges).
    Rejected merge scored r 0.447 (pass) / +7.5 % volume (fail).
- Step 3 done — gauge set n. NOT a filename count: read
  `data/processed/model_inputs_v2/gauges.csv` (159 rows) and
  `model_inputs_v2/discharge.npz`. `cls == 'calib_safe'` → **63**;
  `discharge.npz['is_calibration_safe'].sum()` → **63**; `calib_v2.py:467` selects exactly
  that mask (`self.JP`). `sim_calibrated_v2/q_gauge_H2E.npz` carries
  `q_obs_m3s`/`q_sim_fit_m3s` of shape **(3652, 63)** on `dates` 2009-01-01…2018-12-31.
  So n = 63, and the C2b comparison can be done gauge-paired on the frozen artifact.
- Step 4 done — H2E incumbent rails, from `sim_calibrated_v2/parameters_H2E.csv`:
  `k_sup@global` pos 0.9911 (YES), `k_int_frac@global` pos 0.0019 (YES),
  `wm_mult@R2` pos 0.9713 (YES) → 2 of 10 global, 3 of 18 dimensions. This is the set the
  "no NEW rails" refit criterion is defined against.
- Step 4b — H2E fit metrics read from `sim_calibrated_v2/metrics_fleet.csv` for the §4
  arithmetic: CAL 2012-14 fit **r = 0.5564**, VAL all r = 0.5912.
- Free DDS seeds confirmed by listing `_calib_cache/`: 20260901–20260906 are consumed for
  H1/H2, 20260901–02 for H2E. **20260907 / 20260908 are unused** → registered for H2E-S.

### ISSUE (journalled, not acted on — thresholds are frozen)

The task brief's §4 quotes "CAL r = 0.518". The on-disk value in
`metrics_fleet.csv` (cell H2E, config fit, period CAL 2012-14) is **r = 0.5564**. Both give
the same verdict (max attainable F = c2m(r) = 0.349 vs 0.386, either way F = 0.5 needs
KGE 0.667 and is out of reach), so the argument is unaffected. docs/33 §4 states the
arithmetic parametrically and reports both numbers rather than silently substituting one.
This is framing prose, not a gate, so no pre-registered threshold moved.

- Step 5 DONE: `docs/33_c2b_preregistration.md` written, 507 lines, sections §0–§5 with all
  five required blocks (hypotheses / exact definitions / decision rules / what this does not
  do / amendment note). Frozen-on-write banner at the top.
  Thresholds fixed in it, all justified in place:
  - H-BFI gate: fleet-median |BFI_sim − BFI_obs| vs **IQR(BFI_obs)** over n=63 (SD reported,
    cannot change the verdict).
  - H-PEAK gate: fleet-median R_AMS in **[0.85, 1.15]** OR fleet-median R_Q1 outside it →
    refuted. Justification: qpeak^0.56 ⇒ 15 % peak error ⇒ ~8 % sediment, small against the
    rating-curve R² 0.54. R_Q5 and POT counts are diagnostic and explicitly cannot substitute.
  - H-CHIRPS gates carried over unchanged: volume **[2,016.0, 2,056.8] mm/yr** (±1 % of
    2,036.4, 2009–17) and LOOCV median daily **r > 0.429** (287 gauges).
  - Eckhardt: single forward pass, `a = exp(-1/k_obs)` from `calib_v2.recession_k` on the
    OBSERVED series and reused for both series, **BFImax FIXED 0.80** (Eckhardt 2005,
    perennial/porous) declared as a fixed not fitted choice; 0.50 as a reported robustness
    column only. 30-day filter warm-up, gaps ≤3 d interpolated, segments ≥180 d, gauge needs
    ≥1095 valid scored days, identical mask applied to sim.
  - Model internal partition **51.3 / 29.2 / 19.5** recorded alongside, labelled a different
    (generation-side, pre-routing) quantity; no threshold attaches to it.
  - Weight vectors, exact and summing to 1.00: incumbent (0.40, 0.40, 0.20); one term refuted
    → (0.34, 0.34, 0.17, 0.15); both → (0.28, 0.28, 0.14, 0.15, 0.15). Derivation: incumbents
    × 0.85 / × 0.70.
  - Term forms frozen: `e_bfi = 1 − |ΔBFI|/0.20`, `e_peak = 1 − |ln R_AMS|/ln 1.5`, both via
    `c2m`, both renormalised by the existing `blend()` rule.
  - Refit cell H2E-S: 2 seeds **20260907 / 20260908**, budget **1000**, all else identical.
  - Refit success: signature inside bound AND mean F within **0.02 of 0.25931** *evaluated on
    the incumbent (0.40,0.40,0.20) scale* — registered explicitly because the refit's own F is
    a different quantity — AND railed set ⊆ {k_sup@global, k_int_frac@global, wm_mult@R2}.
  - §4 ceiling arithmetic: F_max = c2m(r) = 0.349 at r 0.518, 0.386 at the on-disk 0.5564;
    F = 0.5 needs KGE 0.667, out of reach. Reframed goal stated.
  - §5 amendments: docs/30 §1 freeze extended to objective re-openings (this is the first);
    docs/31 DAG becomes C0 → C2b → C3 → C4 → C5 with C1 → C2 → C4 in parallel; doc renumbering
    33=C2b, 34=C2 contrast, 35=C4.2, 36=C5.4; C1/C2 provably unaffected (model-free).
- Step 6 DONE: one-line pointer appended to CLAUDE.md's read-first list (line 42), between the
  docs/31 entry and `docs/progress_journal.md`. No other CLAUDE.md content touched.
- Step 7 DONE — verified from disk, not exit codes: `wc -l docs/33_c2b_preregistration.md` →
  507; `grep '^#\{1,3\} '` lists §0–§5 with all subsections; `grep -n 33_c2b_preregistration
  CLAUDE.md` → line 42 hit.

## Files touched

- `docs/33_c2b_preregistration.md` (new)
- `CLAUDE.md` (one entry added to the read-first list)
- `docs/agents/journal_prereg-c2b.md` (this journal)

No git commands run (hard rule). No measurement computed — C2b's measurement phase is
deliberately untouched, which is the point of writing this first.
