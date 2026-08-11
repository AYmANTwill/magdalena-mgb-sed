# Journal: nb16 — observed ENSO sediment contrast notebook

## Goal
Write `src/nbgen/make_nb16.py` -> `notebooks/16_observed_enso_contrast.ipynb`, documenting stage C2
(the OBSERVED, model-free sediment contrast). Generator convention per make_nb13/14. Notebook must
execute with 0 errors; every code cell an execution_count; every figure a three-part reading;
every listed term defined at first use; rates-only rule DEMONSTRATED with a figure.

## Checklist
- [ ] Read src/nbgen/make_nb13.py + make_nb14.py (structure, md()/code() helpers)
- [ ] Read docs/34, docs/33, docs/32, docs/agents/journal_c2-contrast.md
- [ ] Locate C2 outputs in data/processed/c2 (+ c2b)
- [ ] Inspect column schemas of every source before writing code
- [ ] Write generator
- [ ] Emit notebook, execute, verify from executed outputs
- [ ] Report cell/figure counts

## Log
- (start) journal created.

### Step 1 — sources read, schemas inspected, numbers verified BEFORE writing the generator
Read: src/nbgen/make_nb13.py + make_nb14.py (md()/code() helpers, `## N - ` headings, cell()
writer emitting nbformat 4.5 with execution_count None), docs/34 (all 501 lines),
docs/agents/journal_c2-contrast.md, docs/00_INDEX.md head.
C2 outputs located at `data/processed/c2/`: c2_station_window_flux.csv (72 rows),
c2_rate_ratios.csv (36 rows), c2_estimator_agreement.csv (38 rows), c2_monotonicity.csv (40 rows),
c2_monthly_shape.csv (758 rows). NOT `c2_rate_ratios.csv` alone as the brief guessed.

INDEPENDENT VERIFICATION (raw -> frozen table), all cheap, no re-run of anything expensive:
- Station set: sediment_inventory_qc ssc_class = 6 usable + 12 usable-with-caveat = 18. OK.
- Paired same-day SSC/Q rows: **71,529** (journal_c2-contrast says 71,528; +1). 0 duplicate keys.
- Estimator (a) sample means: reproduced for all 38 admissible station-windows, max |rel dev|
  2.2e-16 (float round-off). n_sample_days identical for all 38.
- Rating fit convention verified: polyfit(ln Q, ln Qs) at 23127010 reproduces stored
  log_a 0.157925, b 1.854866, sigma 1.040870 exactly.
- Duan smearing S: recomputed per era from raw residuals. Over the **20 eras of the 18-station
  usable set**: min 1.0800, max 1.8321, median **1.4778** -> docs/34's "1.080-1.832, median 1.478"
  reproduced EXACTLY. exp(sigma^2/2) over the same 20: 1.0835-1.8258 -> docs' "1.083-1.826" exact.
  (My first attempt used the 46 station-windows and got median 1.560 - wrong population, corrected.)
- Bootstrap: default_rng(20260810) 2000-rep day bootstrap at 23127010 P-LN gives
  [15729.9, 22496.1] vs frozen [15724.1, 22436.5] = 0.04 % / 0.27 % - reproduction within MC noise,
  not bitwise (RNG call order differs across stations).
- Selectivity percentiles reproduced to <=0.02 (tie handling): 0.160/0.270/0.588/0.324/0.4375/
  0.420/0.496/0.558 vs docs' 0.163/0.288/0.589/0.326/0.438/0.422/0.497/0.570.
  corr(ln b/a, ln Qsamp/Qwin) = -0.6483 (docs -0.649); agree median pctile 0.4859 (docs 0.488).
- Monotonicity 40/40 increases over 11 distinct nested pairs. Monthly spans BORBUR 66.4 / 91.5
  (docs 66 / 92), peaks April in both. ARRANCAPLUMAS annualised 15.07/23.41/13.33/23.88 Mt/yr
  (docs 15.1/23.4/13.3/23.9).
- model_inputs_v2/discharge.npz: 115 gauges; 21237020 present, **last valid day 2014-12-31** -
  independent confirmation of the trunk blocker from a second artifact. All 7 ratio-supporting
  stations are in the 115-gauge set; 6 calibration-safe; 4 enso_pair_ok.

DISAGREEMENTS FOUND (doc prose vs executed output) - to be reported in the notebook's problems
section, per honesty clause 8:
1. docs/34 s3.1/s7 "22 of 22 station-ratios exceed 1.0" and "16 of 22 exclude 1.0". MEASURED:
   **24** ratios exist (primary a 6, primary b 7, sens a 4, sens b 7); 24/24 > 1; **18/24** CIs
   exclude 1; with partial-rating dropped, 19 ratios and **16/19** exclude 1. The 16 is right, the
   denominator 22 matches neither 24 nor 19. Direction of the finding is unaffected.
2. docs/34 s4.1 mechanism 3: "22017030 ... b = 1.49/1.79 across eras". MEASURED b = **1.794 /
   2.163** (sigma 0.9195/1.0557, which the doc quotes correctly). Steeper than stated, so the
   mechanism argument is strengthened, not weakened.
3. Paired-row count 71,529 vs 71,528 in the C2 journal.
Everything else in docs/34 that I could recompute, reproduced.

NEXT: write src/nbgen/make_nb16.py (read-only notebook: reads artifacts, writes NO files).

### Step 2 — generator written and notebook emitted
`src/nbgen/make_nb16.py` (2,717 lines) follows make_nb13/14 exactly: module docstring, `md()`/`code()`
helpers appending to `C`, `## N - ` section headings, and the same `cell()` + nbformat 4.5 writer.
Emitted `notebooks/16_observed_enso_contrast.ipynb`: **99 cells (30 code, 69 markdown)**.
Notebook is READ-ONLY by design: it writes no CSV, no PNG, no file at all (avoids colliding with the
C2 session's figures/deck/gen_c2_*.png).
NEXT (long): execute with nbconvert, verify from executed outputs.

### Step 3 — executed, verified from outputs, readings corrected against them
First execution: 0 errors, 99 cells, 30/30 execution_count, 24 figures. Then I read EVERY stdout
stream and corrected eight drafted readings that did not match the executed numbers (this is the
point of the exercise — the readings must quote the run, not my expectation):
1. BORBUR daily-flux span: drafted "four orders of magnitude, 5e5 vs 30 t/day" -> measured
   **1,443x** (193,988 t/day on 2011-05-14 vs 134 t/day).
2. Reproduction deviation: 4.441e-16 not 2.2e-16 -> figure band widened to +/-2 ulp, text fixed.
3. n<12 CELLS are **32** of 72 (the a_status counter says 30; 2 more belong to the flow-selective
   station, blocked by the other gate first). cov<0.50 dry share **16 of 33**, not 20.
4. Literature anchor: (a) PASSES vs 144 in the primary window (9.56x) and MISSES in the
   sensitivity window (10.81x); misses 184 in both (12.21x, 13.82x). Sediment share 10.5-16.6 %
   (made figure and print use the same per-estimator maxima).
5. ARRANCAPLUMAS single-era bias measured on sampled days = **1.738x / 1.601x**, which is NOT the
   same statistic as s7.1's b/a = 1.553/1.792 (all-day rating mean vs sampled-day mean). Both now
   reported with the distinction stated.
6. docs/34 disagreements: **5 of 10** recomputed quantities disagree, not 4.
7. s9.6 was WRONG as drafted: (b) is admissible slightly MORE often in the dry phase (20 vs 19) and
   the wet windows have MORE all-missing rating coverage (16 vs 10). The real asymmetry is depth:
   median paired days **125 wet vs 31.5 dry**, median cov **0.789 wet vs 0.561 dry**, 6 of 7
   partial-rating dry. Reading and figure title rewritten.
8. EL PROFUNDO extreme = **61.2 %** of the window sampled flux, not 68 %.
Also fixed a genuine clarity trap: the inventory `reach` column calls Cauca-trunk stations
`mainstem`, so PUENTE ARAGON would have appeared as a "mainstem" station WITH a ratio while the
notebook claims no mainstem contrast. Added a derived `branch` column (Magdalena trunk / Cauca trunk
/ tributary) used in all labels, with an explanatory paragraph. And removed a pandas
DeprecationWarning (groupby.apply -> groupby.agg) so the run is warning-free.

FINAL VERIFIED STATE (from the executed .ipynb, not from exit codes):
- 99 cells = 30 code + 69 markdown; **0 error outputs, 0 stderr streams**; 30/30 code cells carry an
  execution_count; **24 figures**, and all 24 are immediately followed by a markdown cell containing
  all three of "What is plotted / What it shows / What it means".
- Rates-only rule DEMONSTRATED with figures, not stated: window-length bars, a per-station
  rate-vs-total dot plot in which **4 of 13 primary comparisons reverse sign** as totals
  (PUENTE ARAGON b 1.938->0.968, EL PROFUNDO a 1.212->0.605, BOCAS-2411 a 1.702->0.850 and
  b 1.141->0.570), and the pure-arithmetic multiplier figure (0.4993 vs 1.7136, spread 3.432;
  any rate ratio below 2.003 reports as <1).
- Headline as executed: 24 ratios, 24/24 > 1, 18/24 CIs exclude 1 (16/19 headline subset); medians
  primary (a) 4.62 / (b) 2.845, sensitivity (a) 9.32 / (b) 6.404.
- Terms from the mandated list that DO NOT appear (so need no definition): URH/HRU, water balance,
  saturation-excess runoff, baseflow / baseflow index / Eckhardt, recession constant, PET vs actual
  ET, POT / annual maximum series, LOOCV, quantile mapping. Every term that DOES appear is defined
  at first use (checked by locating each first occurrence): minibacia, KGE+r/alpha/beta, NSE (with
  its window dependence), PBIAS, climatology benchmark, DDS, objective function, railed,
  equifinality, Klemes differential split-sample, IDW, pre-registration, SSC, rating curve, era,
  sampling selectivity, Duan smearing, bootstrap CI, geometric mean, MUSLE + alpha/beta/K/C/P/LS,
  surface runoff, sediment delivery ratio, specific erosion (with the t/km2/yr embargo).
- Notebook writes NO files. No git commands run. No calibration launched. No wide forcing CSV read.

Files touched: src/nbgen/make_nb16.py, notebooks/16_observed_enso_contrast.ipynb, this journal.
