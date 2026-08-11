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

---

# Journal: critic — RUN 2 (adversarial verification of the C3 / peak-deficit run)

GOAL: verify by execution the nine checks handed to me. ONLY write = this journal.
NOTE: I initially overwrote this file's RUN-1 content; restored via `git checkout --`
before any further work. RUN-1 section above is intact (83 lines, matches HEAD).

## Checklist
- [ ] 0. Inventory: files, mtimes, git status
- [ ] 1. pytest green? count? are the new sediment tests falsifiable?
- [ ] 2. order of writing: docs/35 CHOICE+BIAS before scripts/c3/qpeak.py?
- [ ] 3. invented constants: urh_cp_factors.csv per-row source; ls2d.py m/n citation
- [ ] 4. independent recompute: one minibacia LS2D, basin-mean C, basin-total erosion
- [ ] 5. embargo: any gauge-referenced t/km2/yr yield?
- [ ] 6. first-run report states both biases with directions?
- [ ] 7. synthesis honest about the null option?
- [ ] 8. frozen artifacts untouched?
- [ ] 9. journals: one per agent, numbers before conclusions

## Log
- CHECK0 git status --porcelain: 15 untracked (docs/35, docs/36, 8 agent journals,
  scripts/c3/, src/mgb_sediment.py, tests/test_qpeak.py, tests/test_sediment.py) + my
  journal. NO tracked file modified except my own journal. No data/ paths appear
  (gitignored, so status alone does not clear them — mtimes checked separately in CHECK8).
- CHECK1 pytest: `python3.10 -m pytest tests/ -q` -> **82 passed in 6.71s**, 0 failed,
  0 skipped. Per-file collect: dhime 7 / mass_balance 3 / forcing_npy 4 / idw 2 /
  qpeak 30 / sediment 36 (36 = 27 functions, parametrize expanding 2 of them to 7+4).
  Falsifiability audit: 0 of the 57 new test functions lack an `assert`/`pytest.raises`
  (scripted scan). The hand cases use an INDEPENDENT arithmetic path (250,000/86,400 and
  0.010 m x 8,100 m2, not the function under test); the extensivity test (3a/3b) would
  fail a per-area or per-second formulation; the two backends are cross-checked at
  rtol 1e-12; the ledger residual is asserted == 0.0 bitwise; check_musle_parameters
  STOP/watch/ok boundaries are each pinned. Verdict: real tests.
- CHECK2 ORDER OF WRITING - PASS, strongly. Windows birth times (both `stat -c %w` and
  Get-ChildItem CreationTime): docs/35 birth 04:08:37.2025 == mtime 04:08:37.2120 (ONE
  write, never edited afterwards); scripts/c3/qpeak.py birth 04:10:22.99; tests/test_qpeak.py
  04:11:26.71. The pre-registration was complete and frozen ~105 s before the implementation
  file existed. journal_c33-qpeak Step 4 "WRITE docs/35 ... BEFORE code" precedes Step 5.
- CHECK3 SOURCES. urh_cp_factors.csv: 8 rows, cols class_id,class_name,C,P,source,note;
  every `source` is either a named citation (W&S 1978 AH-537 Tab.10; Roose 1977/1996 FAO
  SB 70) or begins "C: ASSUMED"; all 8 end "| P: ASSUMED = 1.0 basin-wide". 4 rows ASSUMED
  on C (Shrub, Cropland, Urban) plus Water "definitional". ls2d.py cites m = McCool et al.
  (1989) = D&G (1996) eqs 5-6, n = 1.3 Moore & Burch (1986)/Mitasova (1996), 22.13 and
  0.0896 = W&S (1978), 1 km2 cap = Montgomery & Dietrich (1988,1992), full reference block
  lines 135-150, constants annotated lines 177-195. No unsourced number presented as
  published. PASS.
- CHECK4a LS2D RECOMPUTED INDEPENDENTLY (my own script: rasterio -> pyflwdir.dem.slope ->
  from_dem -> upstream_area -> MY OWN eq.(1)/(2) and MY OWN area-weighted aggregation;
  D8 diagonals (2,8,32,128); flow routing uses the same library, stated not hidden).
  DEM 12000x5640, ratio 8 over minibacias.tif 1500x705, outlet upstream area 356,066 km2.
    mini 1174 (2,688 cells, 22.5734 km2): ls2d 82.5760 / hs 62.9248 / mb86 24.8604 /
      dg96 60.5134 / per-cell median 40.8187   vs SHIPPED 82.576 / 62.9248 / 24.8604 /
      60.5134 / 40.8187 -> EXACT on all five. p90 150.0368 vs 149.781 (0.17 %, percentile
      interpolation only).
    mini 1183 (2,944 cells, 24.7230 km2): 78.8265 / 71.1290 / 25.0442 / 56.6870 / 44.0603
      vs SHIPPED 78.8265 / 71.129 / 25.0442 / 56.687 / 44.0603 -> EXACT. p90 165.6149 vs
      165.607.
    m ranges 0.2356-0.7282 and 0.2612-0.7381 (ls2d.py docstring says "~0.0 to ~0.5"; the
    analytic limit is 0.758 -> docstring understates, not an error).
- CHECK4b BASIN-MEAN C recomputed from parameters.npz:urh_fraction x topology:own_area_km2
  x urh_cp_factors: area 257,096.9 km2, **C = 0.010823** (claim 0.01082). Class shares
  15.46/0.05/36.83/29.10/0.27/18.13/0.00/0.14 % and areas 55.774/0.119/39.867/1.575/
  0.297/0.196/0.649/1.523 % all reproduce. Per-minibacia median 0.00575, p25 0.00389,
  p75 0.00840, p95 0.02927, min 0.00081, max 0.83800, mean 0.01025; 264 units >0.05,
  100 >0.10 -> every figure matches. Area-wtd K 0.03176 (claim 0.0318).
  DISCREPANCY: area-weighted K*C*P is **3.2554e-4**, not the claimed 3.44e-4 - 3.44e-4 is
  0.0318 x 0.01082, i.e. the product of two means, not the mean of the product (-5.4 %).
- CHECK4c BASIN-TOTAL EROSION recomputed with my own MUSLE loop (no import of
  src/mgb_sediment.py): Sed = 11.8*(a_p^2/86.4)^0.56 * sum_cells[(a/a_p)*K*C*P*LS_hs] *
  Qsur^1.12, cell areas from urh_fractions.csv x minibacias.csv:
  **6,843,119.50146 t** vs claim 6,843,119.50146461 t -> ratio 1.00000000.
  Daily basin mean 1,873.8 / median 1,504.7 / p99 6,674.4 / max 9,000.7 t/d (all match);
  ENSO 2,976.77 vs 1,052.48 t/d = 2.8283 (claim 2.828); williams_m3 32.758 Mt/yr (claim
  32.758). Variant with urh_ls2d.csv:area_km2 (sum 251,723.5 km2) gives 6.771 Mt, -1.05 % -
  the module documents and audits that choice (load_geometry area_tol_frac).
- CHECK5 EMBARGO - PASS. Only journal_c36 carries t/km2/yr and every instance is labelled
  "INTERNAL model-area diagnostic ... NOT a station or sub-basin yield (docs/23)". I opened
  figures/deck/gen_c36_erosion_map.png: the caption is printed in panel (a) and the gate-(a)
  note in panel (c). Nothing in src/mgb_sediment.py divides by an area. No gauge-referenced
  yield anywhere.
- CHECK6 BOTH BIASES - PASS. journal_c36 Step 4 states the peak deficit (direction NEGATIVE,
  R_AMS 0.820 / R_POT 0.567 / -10.5 % to -45 % / ~2.1x) and absent channel deposition
  (direction POSITIVE on the model number relative to the outlet anchor, i.e. the hillslope
  figure ought to sit ABOVE 144-184 Mt/yr). It also records that gate (b) came out the
  OPPOSITE way to the task's expectation and that nothing was tuned in response.
- CHECK7 NULL OPTION - PASS. docs/36 section 3.0 is rank 0 "accept + propagate", with its own
  NOT-WORTH-DOING condition; 7 such conditions exist (lines 295/347/406/451/501/535/583);
  section 4 states in the strong form that rank 0 is the operating decision and that six of
  the seven options fail their own condition today.
- CHECK8 FROZEN ARTIFACTS - PASS. h2e_drivers.npz 2026-08-10 13:54:20 (546,366,478 B),
  parameters_H2E.csv and q_gauge_H2E.npz 2026-08-10 14:03:22, model_inputs_v2/*.npz
  2026-08-02. All predate the C3 run's first write (2026-08-11 04:06). `git status
  --porcelain` shows NO tracked file modified. New files under data/ since 03:00 are only
  minibacia_ls2d.csv, urh_ls2d.csv, urh_cp_factors.csv and peakgap/*.
- CHECK9 JOURNALS - PASS. 9 new journals, 93-183 lines / 6.6-12.5 kB, one per agent, all
  non-empty, all with the goal + checklist header and numbers recorded before verdicts
  (c31's four gates carry counts and percentiles before "PASS/FAILS HIGH"; c33 records the
  topology.npz key list and the DEM-extent measurement before choosing option (i)).
  Cross-check of the synthesis' NEW per-gauge finding against per_gauge.csv, computed by me:
  miss_frac median 0.7895, p25 0.6545, p75 0.9303, min 0.2500; 8 gauges at 1.0; 4 with
  n_sim == 0; totals 2236 obs / 1285 sim / 1829 missed / 407 captured; R_POT 0.5746869.
  All reproduce. C3.5 blocked confirmed: `find . -iname "musle*.py"` returns nothing.

## FINDINGS (severity)

**CRITICAL - MUSLE AREA-UNIT CONTRADICTION, INSIDE THIS RUN'S OWN EVIDENCE.**
data/processed/peakgap/method_research.md (written 04:13:37, i.e. 62 min BEFORE
src/mgb_sediment.py at 05:15:48) says of Buarque eq. 7 / Fagundes eq. 12: "so `Dsup` is
mm/day and `A` is km2 in eq. 7/12 (**both texts label the MUSLE area `A` in ha for the
erosion equation itself - mind the mixed units when porting**)". src/mgb_sediment.py's
UNITS section asserts the opposite - "read literally off Buarque (2015) eq. 5/eq. 7,
whose `A` is the same km2 area his eq. 7 uses" - and states "Two conventions exist in the
literature", enumerating only `pixel_km2` and `williams_m3` (x1000^0.56 = 47.863).
The hectare convention - SWAT's standard MUSLE, Q_surf[mm] x q_peak[m3/s] x area[ha],
the form alpha = 11.8 is usually quoted with - appears NOWHERE: not in docs/35, not in
mgb_sediment.py, not in journal_c34, journal_c36 or docs/36 (grep for ha/hectare returns
nothing in any of them). It is worth exactly 100^0.56 = 13.1826x: 0.6844 Mt/yr ->
**9.022 Mt/yr**, i.e. 16.0x / 20.4x below the 144 / 184 Mt/yr anchors instead of
210x / 269x. That turns gate (b) from "2.32-2.43 orders of magnitude" into ~1.2 orders,
and the alpha needed to close it from ~2,480 into ~188. C4 inherits a two-item convention
menu that this run's own primary-source research says is wrong and incomplete.

**WARN - the registered beta hard stop is narrower than the source method's published range.**
docs/35 s6.3 registers HARD STOP outside beta in [0.45, 0.65]. method_research.md
(04:13:37, 5 min AFTER docs/35 was frozen at 04:08:37) records Fagundes (2018) App. IV
calibrated **beta 0.44-0.93** and alpha 6.93-18.86 for the very method being transposed.
The alpha band is compatible; the beta ceiling is not. Nobody reconciled it, and docs/35
s9's amendment procedure was not used. C4 will hard-stop on beta values the source
literature publishes.

**WARN - ls2d.py's docstring justifies the `ls2d_hs` cap with 740 m numbers**
(Medium x Water 240.6 -> 2.89, Coarse x Bare 76.8 -> 62.3) while the SHIPPED default output
is 90 m. Recomputed by me from urh_ls2d.csv: Medium x Water 1837 -> 13.72, Coarse x Bare
91.43 -> 85.21 (the agent's report is right, the code comment is 7.6x off). The resolution
IS labelled, but the 90 m equivalents are never given.

**WARN - C3.6 has no runnable artifact.** src/mgb_sediment.py has no `__main__`/CLI,
scripts/c3 holds only ls2d.py and qpeak.py, and no sediment output was written under
data/processed. The 6,843,119.50 t total, the four gates, the elevation-band table and the
ENSO split exist only in journal_c36 and two PNGs. (I reproduced the total in ~40 lines, so
it is verifiable - but nothing in the repo re-runs C3.6.)

**WARN - journal_c32's "area-weighted K*C*P = 3.44e-4"** is a product of means; the
area-weighted mean of the product is 3.2554e-4 (-5.4 %).

**NOTE - R_POT** is quoted as 0.567 in docs/33, docs/35 s5.2 and docs/36 s1; the measured
value in peakgap/summary.json is 0.5746869 (1285/2236). Cosmetic, but it is a headline
number carried into three documents.

**NOTE - ls2d.py docstring** says m runs "~0.0 to ~0.5"; measured 0.728/0.738 (analytic
limit 0.758). ls2d_p90 differs from mine by 0.17 % on mini 1174 (percentile interpolation).

## Housekeeping
My only write was this file. I overwrote the RUN-1 content once by mistake and restored it
with `git checkout --` before doing anything else; RUN-1 (83 lines) is byte-identical to
HEAD. No git add/commit/push. No calibration launched. No frozen artifact opened for write.
Scratch work lives in the session scratchpad, not the repo.
