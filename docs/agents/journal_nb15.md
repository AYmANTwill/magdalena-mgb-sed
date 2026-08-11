# journal — agent `nb15`

## Goal

Write `src/nbgen/make_nb15.py` → emit and EXECUTE `notebooks/15_ssc_quality_gate.ipynb`,
documenting stages **C0** (freezing the hydrology at H2E) and **C1** (the SSC quality gate),
for a competent reader with **no prior knowledge of hydrological modelling**.

Gate: notebook executes with 0 errors, every code cell has an `execution_count`, every figure
has its three-part reading (What is plotted / What it shows / What it means), every listed term
defined at first use.

## Checklist

- [ ] 1. Read `src/nbgen/make_nb13.py` and `make_nb14.py` — follow their structure exactly
- [ ] 2. Read sources: docs/26 addendum, docs/32, docs/19, docs/agents/journal_{c0,c1-ssc}.md
- [ ] 3. Inspect artifacts: `sim_calibrated_v2/{parameters_H2E.csv,report_H2E.json,metrics_fleet.csv}`,
       `data/processed/sediment_{daily,inventory}{,_qc}.csv`
- [ ] 4. Write `src/nbgen/make_nb15.py`
- [ ] 5. Run generator → `notebooks/15_ssc_quality_gate.ipynb`
- [ ] 6. Execute with nbconvert, timeout -1
- [ ] 7. Verify from EXECUTED outputs: 0 errors, all cells have execution_count, count figures
- [ ] 8. Report cell count / figure count / undefined terms

## Hard rules acknowledged

- No git add/commit/push. Touch only `src/nbgen/make_nb15.py`, `notebooks/15_ssc_quality_gate.ipynb`,
  this journal.
- Never `pd.read_csv` the wide `forcing_minibacia_*.csv` (silent truncation) — use `src/forcing_npy.py`.
  (Not expected to be needed for this task.)
- Frozen artifacts `sim_calibrated_v2/{h2e_drivers.npz,parameters_H2E.csv,q_gauge_H2E.npz}` are
  READ-ONLY.
- No calibration search. No re-running hydrology.
- Gauge-referenced t/km²/yr yields EMBARGOED.
- Uncited plausibility bands may not pass or fail a gate → label UNCITED.

## Log

### Step 0 — journal created
Date 2026-08-11. Read `docs/00_INDEX.md`. Confirmed: hydrology frozen at H2E
(F = 0.25931, reproduce via `python3.10 src/report_h2e.py`, must match 1e-8); C1 owned by
`docs/32` (79/79 classified, 28 mapped, 6 usable + 12 usable-with-caveat, 46 unmapped);
docs/19 owns the SSC QC audit and §3.9 the honest ceiling; the single Magdalena-trunk SSC
station is `21237020` ARRANCAPLUMAS.

### Step 1 — reads complete
`src/nbgen/make_nb13.py` + `make_nb14.py` (structure: module docstring naming the two run
commands, `OUT` path, `C = []` with `md()` / `code()` helpers, numbered `# ===== N` banners,
closing `cell()` + `nb` dict + `OUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False))`
and a wrote-N-cells print). Followed exactly.

Sources read: `docs/00_INDEX.md`, `docs/32_ssc_qc_audit.md` (full — §0-§6 registration and
R1-R7 results), `docs/26_phase3_refit.md` §A.1-A.6 addendum, `docs/19_sediment_qc_audit.md`
§3.4/§3.7/§3.9, `docs/16_forcing_pipeline_audit.md` §4.1-§4.3,
`docs/18_hydrology_journal.md` §9.1-§9.2 + §10, `docs/agents/journal_c0.md` §0-§3,
`docs/agents/journal_c1-ssc.md` steps 0-2a.

### Step 2 — artifact inventory verified on disk
- `data/processed/sim_calibrated_v2/` (NOT repo-root `sim_calibrated_v2/`):
  `parameters_H2E.csv` 18 rows, `report_H2E.json`, `metrics_fleet.csv` 39 rows
  (H1/H2/ref/H2E x prior/fit x periods), `q_gauge_H2E.npz`
  (dates 3652, gauge_code 63, q_obs/q_sim_prior/q_sim_fit/q_clim (3652,63) float32).
- `data/processed/`: `sediment_daily_qc.csv` (269,337 rows, 22 cols),
  `sediment_inventory_qc.csv` (79 rows, 34 cols), `sediment_coverage_census.csv` (1,107 rows),
  `ssc_sampling_selectivity.csv` (79 rows), `ssc_rating_fits.csv` (30 eras),
  `ssc_station_eras.csv`.
- Gate numbers confirmed from `report_H2E.json` (EXECUTED artifact, not prose):
  archived F = recomputed F = 0.25930593639066796, relative difference 0.000e+00, bar 1e-8,
  `pass` true, `per_gauge_terms_bit_identical` true. kc_mult 1.6624690504559212,
  k_sup 19.199 d, k_int 0.8656 d, k_bas 42.974 d, railed_global 2, railed_all 3.
  Mass residual 9.6578e-17 relative, RC 0.51269.

### Step 3 — DISAGREEMENT FOUND between doc prose and the data on disk (to be reported in the nb)
`docs/18` §9.1's reporting-density gradient reads 4.38 / 6.75 / 11.69 mm/day over
92 / 119 / 83 stations. Recomputed from `precip_gauges_daily_qc_v2.csv` (926,910 rows,
294 stations, 240,158 `Inferido_seco` rows on 153 stations) with pre-repair = drop
`Inferido_seco`, density = reported days / own span:
**station counts reproduce EXACTLY (92 / 119 / 83)**; pooled means are
**4.859 / 6.994 / 12.052 mm/day** and %zeros 60.2 / 32.9 / 26.9 against the doc's
60.4 / 26.9 / 23.7. Same gradient, same sign, same order; the level differs. The doc does
not state whether its mean is pooled or a station-mean-of-means, and neither definition
reproduces its level (station-mean-of-means gives 4.75 / 7.27 / 12.48). REPORTED as a
disagreement in the notebook per the honesty clause, not silently smoothed.
Note also `precip_gauges_daily_qc.csv` (no `_v2`) is the **v1** repair (70 stations,
109,129 inferred days) — the v2 repair the notebook must quote is the `_v2` file.

### Step 4-5 — generator written and notebook emitted
`src/nbgen/make_nb15.py` (3,192 lines) follows make_nb13/14 exactly: module docstring with both
run commands, `OUT`, `C = []`, `md()` / `code()`, `# ===== N` banners, closing `cell()`/`nb`
emit. Emitted `notebooks/15_ssc_quality_gate.ipynb`: **84 cells (27 code, 57 markdown)**.
Structure: 0 how to read + inputs; 1 what freezing means (+F1); 2 H2E (2.1 FAO-56, 2.2 KGE +
independent recompute + F2, 2.3 NSE/climatology + F3 + F4, 2.4 recession + F5, 2.5
railed/equifinality + F6, 2.6 peaks POT/AMS + F7, 2.7 r-ceiling IDW/LOOCV/quantile mapping +
F8); 3 reproduction gate + F9; 4 SSC + rating curve + F10; 5 THE TRANSPOSED LESSON (5.1
rainfall F11+F12, 5.2 SSC selectivity F13, +F14 decomposition, 5.3 absent-record F15, 5.4 the
honest null failure F16, 5.5 low-end truncation NEGATIVE F17); 6 classification (6.1 N knee +
coverage heatmap F18, 6.2 classes/reach F19, 6.3 rating R2 F20); 7 window membership F21;
8 PROBLEMS (8.1 trunk gap F22 ... 8.8 what NOT to conclude); 9 handoff + MUSLE/SDR/specific
erosion; 10 choices with rejected alternatives; 11 summary.
22 figures planned. Now executing.

### Step 6-7 — executed and verified from the EXECUTED outputs
`python3.10 -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1`.
Three execution failures found and fixed before the clean run (each recorded, none papered over):
1. `assert CHK.absdiff.max() < 1e-9` failed at 3.506e-09. Root cause: the flows are stored
   float32 and re-widened to float64, and the largest residual lands on `skill_over_clim`, a
   DIFFERENCE of two near-equal KGE values. Fixed by making the bar 1e-8 ABSOLUTE and printing
   why a relative bar is meaningless on a near-cancelling difference (a relative error of 6.6e-6
   on a quantity of -0.000533 means nothing).
2. `NameError: jt` in the section 8.1 cell — `jt` had been defined in the figure-4 cell, which I
   rewrote to use a different gauge. Fixed by defining it locally.
3. `SyntaxError` from an escaped apostrophe inside a raw-string code cell; rephrased.

**FINAL: 84 cells (27 code, 57 markdown), 0 errors, all 27 code cells carry an
`execution_count` (1..27), 22 rendered PNG figures, and all 22 figure-producing cells are
immediately followed by a markdown cell containing all three of "What is plotted" / "What it
shows" / "What it means".** Every one of the 29 required terms appears and is defined at first
use.

### Step 7b — readings corrected against the executed outputs (honesty clause)
Eight numbers I had pre-computed into the reading cells disagreed with the executed run and were
corrected in the generator, not left standing:
- KGE > 0 at **54** of 63 gauges (I had written 44); r p10 **0.4388** (not ~0.36); r>0.7 at 21/63.
- corr(NSE, observed CV) over the six windows is **-0.386** — weak. The reading now quotes it and
  explicitly says six points cannot establish the mechanism, and that the climatology yardstick
  does not depend on that correlation.
- absent-record median **28.3 %** (not 28.4), PENALTA 74.1 %, BOLOMBOLO 73.4 %.
- median gap between sorted non-empty window counts is **8**, not ~20.
- eras with r2_conc < 0.05: **9** of 30, not 6.
- **outlet skill-over-climatology on VAL all is +0.0375, NOT negative.** I had written -0.640 in
  three places. Corrected everywhere, and the notebook now names the aggregation trap: the outlet
  is far worse than climatology in BOTH ENSO windows (-0.891 La Nina, -0.333 El Nino) yet
  marginally positive on the combined VAL all window because the four VAL sub-windows cancel.

### DISAGREEMENTS between doc prose and executed artifacts, reported in the notebook
1. `docs/18` §9.1 reporting-density gradient 4.38/6.75/11.69 mm/day: station counts reproduce
   EXACTLY (92/119/83) but levels measured are **4.859/6.994/12.052**; neither pooled nor
   station-mean-of-means reproduces the doc level. Reported in section 5.1.
2. `R_AMS = 0.820` (docs/33 §7, docs/36 §1): measured **0.7337** median-of-ratios and **0.5508**
   ratio-of-medians on the frozen archive, 70.0 % of 404 gauge-years under-predicted. A definition
   gap of the same kind docs/26 A.3 already found in `rec_ratio`. Reported in section 2.6.
Both are stated in the notebook as disagreements with the sign/order agreeing and the level not.

### Independent reproductions the notebook performs (not re-runs)
- All 48 (period x metric) H2E fleet scores recomputed from `q_gauge_H2E.npz` with an
  independently written KGE function: max |absolute difference| **3.506e-09** vs
  `metrics_fleet.csv`, gauge counts identical.
- The C1.2 selectivity statistic recomputed from `discharge_daily.csv` + `sediment_daily_qc.csv`:
  max |diff| **1.45e-02**, median **2.27e-04**, paired-day counts identical, **flag decisions
  identical**.
- `ssc_rating_fits.csv` R2/b/n for `21237020` reproduced to **0.00e+00**.
- `report_H2E.json` C0.2 gate re-derived: archived F == recomputed F as float64 bit patterns,
  relative difference 0.000e+00 against a 1e-8 bar.

### Files touched
- `src/nbgen/make_nb15.py` (new, 3,207 lines)
- `notebooks/15_ssc_quality_gate.ipynb` (new, generated + executed, 2.87 MB)
- `docs/agents/journal_nb15.md` (this file)
No git operations run. No frozen artifact written. No calibration launched. No t/km2/yr yield
appears anywhere in the notebook (verified: nothing is divided by `AREA`, and the cell that loads
it says so).
