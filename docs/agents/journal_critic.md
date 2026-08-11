# Journal: critic (adversarial verification of the C2b/C1/C2 run)

GOAL: independently verify every claim of this run. ONLY write = this journal.

## Checklist
- [ ] 1. Frozen-doc integrity: git diff docs/32, docs/33 registered sections
- [ ] 2. Pre-registration precedence (mtimes, journals, git)
- [ ] 3. Independent recompute: one BFI_obs, one AMS ratio, CHIRPS volume, one C1 classification
- [ ] 4. C2 comparability: unequal-window totals? both window pairs?
- [ ] 5. Embargo: t/km2/yr anywhere
- [ ] 6. Refit actually running + zero-weight gate <= 1e-10
- [ ] 7. Claimed files exist w/ claimed content (spot-check 3)
- [ ] 8. Journals one per agent, threshold before result

## Log
- CHECK1 docs/32: `git diff HEAD -- docs/32` = ONE hunk at line 120; only 2 lines removed
  (the "## Results (appended...)" heading and the "*(empty until C1.1-C1.7 run...)*"
  placeholder). Registered sections lines 1-119 (§0-§6) BYTE-IDENTICAL. PASS.
- CHECK1 docs/33: untracked (no git baseline). §0-§5 = lines 1-508, §6 starts line 509,
  §7 line 691, EOF 935 -> consistent with append-only. Every threshold in §1/§2.4/§3.2 on
  disk matches the list recorded in journal_prereg-c2b.md Step 5 (mtime 19:04:03) verbatim:
  IQR gate, [0.85,1.15], [2016.0,2056.8], r>0.429, BFImax 0.80, 0.20 BFI scale, ln1.5,
  weights (0.34,0.34,0.17,0.15) / (0.28,0.28,0.14,0.15,0.15), seeds 20260907/08, budget 1000.
- CHECK2 mtimes: prereg journal 19:04:03 < baseflow.py 19:08 < journal_bfi 19:16:48,
  journal_peaks 19:16:25, docs/33 19:17:07. Prereg precedes measurement. PASS so far.
- CHECK3 BFI recomputed INDEPENDENTLY (my own Eckhardt/gapfill/segmentation; only the
  registered recession_k imported). EXACT reproduction: 55/63 included, same 8 excluded,
  median BFI_obs 0.7811, BFI_sim 0.7965, median|diff| 0.01625, IQR 0.02845, SD 0.0307,
  BFImax0.50 0.00308 vs 0.00487, median k 10.444 / a 0.9087, gauge 21237040 obs 0.67325
  sim 0.79053 => +0.1173 (claimed +0.117). Verdict NOT REFUTED confirmed.
- CHECK3 PEAKS recomputed independently: fleet median R_AMS 0.8200 (claimed 0.820),
  R_Q5 0.9744 (0.975), R_Q1 0.8399 -- matches their RAW-mask robustness row (0.840) not
  their headline 0.847 (segmented mask); both < 0.85 so verdict unaffected. Counts
  36/9/18 below/in/above band reproduce exactly. H-PEAK REFUTED confirmed.
- CHECK3 CHIRPS: merge_loocv_report_v2.csv vs merge_loocv_report.csv -> max|diff| 0.0 on
  r_base/r_merged/bias_merged_pct/n_base/n_merged over 291 rows (bit-identical CONFIRMED).
  median r_base 0.42902 (287 finite), median r_merged 0.44748 -> LOOCV PASS confirmed by me.
  Volume ANCHOR recomputed independently from forcing_precip_v2.npy + minibacias areas:
  2036.39 mm/yr 2009-2017 area-weighted (gate anchor 2036.4, band [2016.0,2056.8]) -> correct.
  Basin area sum 257,097 km2. Merged 2188.5 NOT re-derived by me (needs a full field rebuild)
  but is bit-for-bit the value already recorded in COMMITTED docs/18 line 840 from the Aug-3
  run -> corroborated by an independent prior record. v3 files ABSENT on disk (verified).
- CHECK3 C1: recomputed window counts from sediment_daily_qc.csv (269,337 rows, 79 stations,
  c1_deleted sum 0): 26017060 = 207/34, 21197010 = 192/202, 21237020 = 91/195,
  26237020 = 0/179 -> all match docs/32 R6.1 exactly. Classification of 26017060 as
  usable-with-caveat (single-window at N=91) reproduces.
  NOTE: 21237020 (the ONLY Magdalena-trunk station) has La Nina n = 91 = N exactly.
- CHECK6 GATE reproduced INDEPENDENTLY in my own process (registered temp cell, no file
  written): H2E stored best F 0.25930593639066796; current modified calib_v2 recomputes
  0.25930593639066796 (rel 0.0); peak term COMPUTED at weight 0 with (0.40,0.40,0.20,0.0)
  gives 0.25930593639066796, abs 0.000e+00, rel 0.000e+00 <= 1e-10 -> GATE PASS CONFIRMED.
  H2E-S weights on the same vector: F 0.22057354584714875, r_ams finite 51, median 0.6482
  (matches the launch agent's informational numbers exactly).
- CHECK5 embargo grep over docs/32,33,34, all agent journals, docs/18 and data/processed/c2/*:
  every "t/km2/yr" hit is an embargo STATEMENT; no computed yield. c2 CSVs carry only
  *_tday rate columns. PASS.
- CHECK4 C2: c2_rate_ratios has pair in {primary(18), sensitivity(18)}; flux table has all
  four windows P-LN 365 d / P-EN 731 d / S-LN 365 d / S-EN 213 d, but every ratio is
  t/day over t/day: max |a_ln_tday/a_en_tday - a_ratio| = 1.8e-15. NO totals ratio. PASS.
  Reproduced medians: primary a 4.620, primary b(all) 2.949, sens a 9.320, sens b(all) 4.650.
  DISCREPANCY: 24 finite station x estimator x pair ratios exist and 24/24 exceed 1; docs/34
  line 204/473 says "22 of 22". Direction claim holds a fortiori; the count does not tie out.
- CHECK6 RUN ALIVE: PIDs 23840 (queue, 25.8 MB), 29064 + 28648 (workers 455.5/455.8 MB,
  > 300 MB bar). Worker logs advance 26 -> 51 -> 76 / 1000; checkpoints read back as cell
  H2E-S, budget 1000, arch_ra (76,63) with 51 finite per eval. queue_runner.log has the
  19:44:12 QUEUE START + 2 START lines. No .err files.
- CHECK7 files: src/baseflow.py --selftest re-run by me = 9/9 PASS (BFI 1.000000000000,
  spike 0.062014, MRC k_hat 25.000). figures/deck/gen_bfi.png, gen_peaks.png,
  gen_ssc_coverage.png all present. sediment_inventory_qc.csv = 79 rows, classes
  6/12/61 (matches). c2_monotonicity 40 rows, 40 increases. 21237020 discharge really
  ends 2014-12-31 (n 9073). EL PROFUNDO leverage 156.66 % reproduced.
  peaks_per_gauge medians: R_AMS 0.8200, R_Q1 0.8470, R_Q5 0.9746, POT 1285/2236 = 0.575,
  4 zero-POT gauges -- all as claimed.
- CHECK8 journals: 7 journals present and non-empty (bfi 108, peaks 79, c1-ssc 359,
  c2-contrast 107, chirps-refit 154, refit-launch 180, prereg-c2b 105 lines); each quotes
  its gate/threshold at the head before any result.
- FINDINGS (see structured output): no CRITICAL. WARN: nothing committed (docs/33+34 are
  untracked and hold prereg + results in one file; docs/34 has no external corroboration
  of precedence); docs/31 still points C2 at "docs/33" and C4 at "docs/34" so the
  renumbering is unresolved outside docs/33 §5.2; H-BFI gate has near-zero power
  (r(sim,obs)=0.094, BFI_obs range 0.658-0.799 under the 0.80 cap); refit peak term scored
  on CAL 2012-14 (R_AMS 0.6482) while §2.3/§3.5 define it on 2009-2018 (0.820);
  docs/34's "22 of 22" does not tie out (artifact holds 24 finite ratios, 24/24 > 1).
