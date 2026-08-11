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

---

# RUN 2 (2026-08-11): adversarial verification of the C3 dimensional-closure run

GOAL: was anything FITTED TO THE ANSWER? Only write = this journal.

## Checklist (run 2)
- [ ] 1. CENTRAL: did decide-units / decide-ls-aggregation / decide-ls-resolution record
      the DECISION before computing the basin-total effect? (journal ordering + mtimes)
- [ ] 2. Independent recompute of the units hand case, carrying units myself
- [ ] 3. Independent recompute of pixel-vs-URH scale ratio on one real unit
- [ ] 4. Implied SDR reported honestly? outside 0.05-0.3 => verdict must be OPEN
- [ ] 5. docs/37 first line: CLOSED or OPEN, consistent with the rest?
- [ ] 6. pytest green? Does the new regression test assert the AUDIT'S HAND VALUE or
      merely whatever the code emits (test-written-to-pass)?
- [ ] 7. Frozen artifacts untouched (mtimes + git status)
- [ ] 8. Any previously committed number in docs/33/35/36 changed without a dated amendment?

## Log (run 2)
- START. git status shows docs/35_qpeak_preregistration.md MODIFIED (tracked) -> check 8
  target. src/mgb_sediment.py and tests/test_sediment.py modified. docs/37 untracked.
- CHECK 7 PASS. Frozen artifacts in data/processed/sim_calibrated_v2/: h2e_drivers.npz
  2026-08-10 13:54:20, parameters_H2E.csv / q_gauge_H2E.npz 2026-08-10 14:03:22 — ALL
  predate this run's earliest journal write (2026-08-11 07:22:18). git status lists none of
  them (dir is gitignored). q_gauge_H2E.csv does not exist (only .npz) — nothing to touch.
- CHECK 1 PASS (all three). journal_decide-units: DECISION at line 268 "Step 5 — DECISION
  (recorded BEFORE step 4...)", engine numbers only at line 340 Step 4. Decision states
  "adopting this convention does **not** close the gap ... I am not claiming one."
  journal_decide-ls-aggregation: DECISION step 5 line 127, verification step 6 line 167;
  factor delivered = 1.000 (nothing gained) — the strongest possible non-fitting evidence.
  journal_decide-ls-resolution: DECISION line 222, "Step 3 — AFTER the decision" line 337;
  discloses the asymmetry itself (line 348-352) and reports its own finding moves the total
  AWAY from the anchor (0.421x, gap 210-269x -> 500-800x). No "makes the number match"
  anywhere in the three; grep for anchor-first reasoning found none.
- CHECK 2 PASS, my own arithmetic, no numbers copied: ft=0.3048 exact -> acre-ft
  1233.4818375475202 m3, cfs 0.028316846592 m3/s, short ton 0.90718474 t; denominator
  34.9283159678514; alpha(m3) = 95*(1/34.9283...)^0.56*0.90718474 = 11.78256540331627.
  alpha(mm*ha) = 42.77990926837566, alpha(mm*km2) = 563.9490366786792. Hand case: V=10000 m3,
  X^0.56 = 173.78008287493762, sed = 61.51814933772792 t (alpha 11.8) / 61.42725576803022 t
  (Williams exact via 8.107131937899124 ac-ft x 35.314666721488585 cfs = 67.71195883214506
  short ton). Rejected readings 16.943505268221404 / 1.285296313886159. EVERY digit the
  units journal reported reproduces. ONE trivial slip: journal says "if Williams Y had been
  metric tons ... would give 12.983"; I get 12.988055115781895. Not load-bearing (a
  secondary discriminator), but it is a wrong digit in a committed journal.
- CHECK 3 PASS, recomputed from the derived expression WITHOUT the engine: mini 6783 urh 31,
  A=4.761750 km2, n=587.870370, K=0.0302 C=0.003 P=1 LS=0.201784. per-pixel-summed vs lumped
  ratio = 2.149382895959449 at Qsur 1.3461, 0.01 AND 50.0 mm/d (Qsur-independent as derived);
  n^(2beta-1) = 2.149382895959449 — identical to 16 digits. Engine pixel_km2 reproduces the
  journal's 6.6193e-05 / 1.42274e-04 exactly.
- CHECK 6 PASS (with a nuance). `python3.10 -m pytest tests/ -q` -> **96 passed** in 10.36 s,
  0 failed, 0 skipped (test_sediment.py alone = 50). The new regression
  `test_audit_hand_computed_real_unit_day_exact_value` asserts a CONSTANT
  1293.5691626849571 and ALSO re-derives it from literal arithmetic inside the test, so it
  can fail the engine rather than echo it. NUANCE: the audit journal's own hand value is
  1293.4734 (it used the exactly-derived K ratio 0.90718474/0.404686/17.02 = 0.13170977);
  the test uses the repo's stated constant 0.1317 -> 1293.5691626850. I reproduced BOTH from
  scratch: 0.1317 -> 1293.5691626850, 0.13170977 -> 1293.4731818946, i.e. 7.6e-5 relative
  apart. Not fitting, but two different "hand values" for the same unit-day are now in the
  repo without the reason stated.
- CHECK 4/5 PASS. docs/37 line 1 = "# 37 - C3 closure verdict: **OPEN**". SDR reported as
  0.579-0.740, explicitly "above the plausible band", closure table marks that condition
  NOT MET, and §4 refuses to use the uncited SDR band to pass the gate. Consistent.
  Re-ran the basin decade MYSELF (frozen drivers read-only): 2,486,957,417.4342093 t over
  3652 d = 9.998631074606434 yr -> **248.729790996124 Mt/yr**; ledger exact=True,
  residual 0.0; legacy 0.6844056401724942; measured ratio 363.4245196071666 =
  1000**0.56/0.1317 = 363.42451960716664. SDR 144/248.73 = 0.5789, 184/248.73 = 0.7398.
  alpha needed for gross==anchor: 6.8315 / 8.7292, and
  check_musle_parameters(alpha=8.0, beta=0.56) -> {'status': 'ok'}. Every headline number of
  the recompute claim verified independently.
- CHECK 8 PASS for the named docs. docs/33 and docs/36 CLEAN in git (untouched).
  docs/35 diff = ONE changed line (the Amendments summary row, ADDITIVE: appends the §9.2
  pointer) + 107 appended lines (§9.2). No previously committed NUMBER altered; §9.1's
  0.6844/9.0222/32.7577 rows are restated in §9.2 unchanged. scripts/c3/qpeak.py clean.
- FINDING A (the one that matters). The LS-FORMULATION CRACK measured by
  journal_decide-ls-resolution §3b is in NO document. grep for "2.37", "formulation",
  "limiter" over docs/37, docs/35 and docs/39: zero hits. It exists only in that agent's
  journal. Its size and DIRECTION: our LS is 2.37x-3.00x ABOVE the LS that alpha = 11.8 is
  paired with in the MGB-SED lineage, measured on the SAME 90 m grid (source-faithful LS
  area-wtd mean 16.775 vs ours 39.812 = 0.421x). Consequences I computed:
    248.7298 x 0.421 = 104.72 Mt/yr  -> BELOW both anchors
    248.7298 x 0.333 =  82.83 Mt/yr  -> BELOW both anchors
    implied SDR would be 144/104.72 = 1.375  -> back on the IMPOSSIBLE side
    like-for-like alpha reference for our LS = 11.8/2.37..3.00 = 4.98..3.93, i.e. the
    ADOPTED alpha = 11.8 would itself sit at/above the corrected hard stop (11.8-14.9).
  Therefore docs/37's "moved the model onto the physically possible side ... for the first
  time" and docs/35 §9.2's "it is now a like-for-like comparison, and no threshold changes"
  are both CONTINGENT on a level equivalence this same run measured as 2.4-3x violated, and
  neither doc qualifies it. It also belongs in docs/37 §4 item 4 ("terms known to point the
  wrong way"), where the largest listed term is only 1.125x. The OMITTED term is the
  convenient direction — leaving it out makes the adopted result look better.
- FINDING B. The documentation defect decide-units explicitly reported as needing correction
  SURVIVES in 3 places, uncorrected: src/mgb_sediment.py:132-134 (swat_mm_ha "the convention
  alpha = 11.8 is normally quoted with"), src/mgb_sediment.py:474-477 (same claim on
  SWAT_HA_PER_KM2), docs/35:490-491 (§9.1, committed). docs/35 now asserts both "11.8 is
  normally quoted with mm.ha" (§9.1) and "11.8 belongs to m3" (§9.2) with no retraction.
- FINDING C (minor arithmetic). docs/35 §9.2 and docs/37 §1 both print the conversion as
  "86.1826 / 7.31494 = 11.7818". Correct values: 34.9283159678514**0.56 = 7.314413062858403
  and 95*0.90718474/that = 11.78256540331627. So 7.31494 and 11.7818 are both wrong in the
  last digits, in the run's central derivation table. Also journal_decide-units:196 says the
  metric-ton reading "would give 12.983"; correct is 12.988055115781895. And
  src/mgb_sediment.py:170 prints the adopted row as "1.35x / 1.73x ABOVE" under a
  "vs 144 / 184" header — REVERSED (248.73/144 = 1.727, /184 = 1.352); docs/35 §9.2's table
  has it the right way round.
- VERDICT: NOTHING WAS FITTED TO THE ANSWER. Three decisions all pre-registered their
  reasoning; two delivered factor 1.000; the resolution agent volunteered a finding that
  makes the headline gap WORSE; the units decision is reproducible to 16 digits from primary
  conversion constants alone and I re-derived it without copying. The failure of this run is
  a REPORTING failure (Finding A), not an integrity failure.
- K-CORRECTION SPECIFICALLY STRESS-TESTED for fitting (it is the factor that clears the
  anchor, so it is the prime suspect). Cleared on independent, PRE-EXISTING evidence:
  notebooks/09_soil_parameters.ipynb §4 markdown, read by me directly, says verbatim
  "mid-range Wischmeier & Smith (1978) class values converted to SI (x0.1317)" with the table
  Coarse 0.020 / Medium 0.045 / Fine 0.028; minibacia_soil_params.csv:K measures min 0.019 /
  median 0.03055 / max 0.0495 / mean 0.031824 — that table times the drainage factor. Undoing
  0.1317 gives 0.144-0.376, inside Wischmeier's US-customary 0.02-0.69 AND inside the
  0.1-0.65 range SWAT documents for its own usle_k input, which is the reference
  implementation of the very equation carrying alpha = 11.8. The correction is therefore
  forced by the repo's own documented transform plus the alpha derivation, and its size is a
  consequence, not a target.
- Checklist run 2: [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 [x]8. Wrote nothing outside this
  journal (scratchpad scripts crit2/crit3b/crit4/crit5.py are outside the repo). No git, no
  calibration, frozen artifacts read-only.

================================================================================
RUN 3 — 2026-08-11 — adversarial verification of the SDR retirement / C revision /
C4 guards / re-verdict run (notebooks 15-18, docs/40, docs/41, docs/42, docs/37 amendment)
================================================================================

GOAL: trust nothing not executed here. Verify 10 checks. Only write = this journal.

CHECKLIST (run 3):
[ ] 1 notebooks 15/16/17/18 fully executed, zero error outputs; count cells + figures
[ ] 2 spec followed: 3 figures/nb have What is plotted/shows/means; 5 terms/nb defined at first use
[ ] 3 maths present: 5 computational cells/nb have preceding equation + symbols + units
[ ] 4 five quoted numbers verified against their artifacts
[ ] 5 ANTI-FITTING: journal_cite-cfactor ordering — C chosen BEFORE basin-total effect?
[ ] 6 three citations from docs/40 + three from docs/41 real and as claimed
[ ] 7 docs/37 amendment first line CLOSED/OPEN consistent with its own evidence
[ ] 8 embargo: no gauge-referenced t/km2/yr yields
[ ] 9 frozen artifact mtimes unchanged
[ ] 10 pytest green, report count

--- run 3 findings as executed ---
- CHECK 1 PASS. All four notebooks fully executed in one clean pass, zero error outputs:
  15: 84 cells (27 code / 57 md), exec_count 1-27 monotonic, 22 inline PNG
  16: 99 cells (30 code / 69 md), exec_count 1-30 monotonic, 24 inline PNG
  17: 108 cells (32 code / 76 md), exec_count 1-32 monotonic, 27 inline PNG
  18: 85 cells (38 code / 47 md), exec_count 1-38 monotonic, 16 inline PNG
  Zero unexecuted code cells, zero non-empty stderr streams anywhere.
- CHECK 9 PASS. data/processed/sim_calibrated_v2/: h2e_drivers.npz 2026-08-10 13:54:20
  (546,366,478 B), parameters_H2E.csv + q_gauge_H2E.npz 2026-08-10 14:03:22 — byte-identical
  timestamps to run-1 and run-2 records in this same journal. All notebook work is 2026-08-11
  09:56-10:16, i.e. AFTER, so nothing rewrote them.
- CHECK 10 **FAIL — CRITICAL**. `python3.10 -m pytest tests/ -q` => **2 failed, 94 passed**
  (96 collected). NOT the "82 tests green" of the state summary, nor green at all. Both
  failures are the C revision landing without its tests:
    tests/test_sediment.py:310 test_audit_unit_day_reproduces_from_the_real_files
       assert abs(g.cell_c[j] - 0.003) < 1e-12  ->  got 0.005 (URH 11 = Forest)
    tests/test_sediment.py:683 test_real_geometry_shape_and_ranges
       assert set(unique(cell_c)) <= {0.003,0.005,0.01,0.2,1.0,0.0,0.001}
       -> extra items {0.015, 0.03, 0.5}
  The first is the file's OWN self-described "join guard" for the 0.684 unit-day mass number,
  i.e. the guard protecting the 0.684 -> 248.73 Mt/yr chain is the one that is red.
  Aggravating: commit 8807951 (2026-08-11 08:59) is titled "... as named options, 96 tests".
  Timeline from mtimes: tests/test_sediment.py 08:02:42 < urh_cp_factors.csv 08:42:08 <
  src/mgb_sediment.py 08:54:50 < commit 08:59:38. The CSV+default flip post-dates the tests
  and the suite was never re-run against it. urh_cp_factors.csv is under data/ = gitignored,
  so the red state is invisible to a fresh clone until it regenerates the CSV.
- CHECK 6 (docs/40, citation 1 of 3) **VERIFIED, exactly as claimed**. Fetched USDA NEH Part 632
  Ch. 6 PDF myself (irrigationtoolbox.com mirror, 18 pp., 44,196 chars extracted with pypdf).
  Table 6-2 in the ORIGINAL is split Sand/Fines, which docs/40 merges; the merge is arithmetically
  exact: erosion sand 500,000 + fines 1,800,000 = 2,300,000; yield sand 400,000 + fines
  1,200,000 = 1,600,000; total DR 70 %; sheet 900,000 -> 300,000 = 33 %; gullies 350,000 ->
  280,000 ~80 %; roadbanks 150,000 -> 120,000 80 %; streambanks 900,000 -> 900,000 100 %.
  So 0.6957, 0.3913, 1.7778 all re-derive. Also verified verbatim: "The gross (total) erosion in
  a drainage area is the sum of all the water erosion taking place"; "they vary inversely as the
  0.2 power of the size of the drainage area"; "The figure indicates a wide variation in the
  sediment delivery ratio for any given size of drainage area"; the six-study reference list
  (Gottschalk & Brune 1950, Woodburn & Roehl, Maner & Barnes 1953, Glymph 1954, Maner 1957,
  Roehl 1962) matches docs/40 line 118 exactly; Summary: "Using an equation to obtain sediment
  data outside the physiographic area for which the equation was developed is generally not
  recommended." NOTE: docs/40 renders that as a "prohibition"; the source says "generally not
  recommended" -- softer, but the direction is the source's own.
- CHECK 6 (docs/40, citation 2 of 3) **VERIFIED verbatim via Crossref**: Tan, Liu & Lu (2024),
  ESPL 49:1778-1795, doi 10.1002/esp.5797. Abstract gives 26.5 -> 23.7 t/ha/a, SDR 0.07-0.38 over
  39 subbasins, ~30 % >= 0.35, SSY 1.3-16.9 t/ha/a, 86 % of SDR variation, and Specific Catchment
  Area / Maximum Elevation / Drainage Area "all had a positive correlation with SDR". Every docs/40
  C8 clause is in the abstract.
- CHECK 6 (docs/40, citation 3 of 3) Latrubesse & Restrepo (2014) Geomorphology 216:225-233 and
  Restrepo et al. (2006) J. Hydrol. 316:213-232 -- bibliographic records CONFIRMED via Crossref
  (title, journal, volume, pages, authors all as cited). Abstracts absent from Crossref, so the
  1,485 / ~690 / 2,200 values remain SECONDARY, exactly as docs/40 §9 already labels them. No
  misattribution found.

- **FINDING 1 -- CRITICAL, and it is a science finding, not a bookkeeping one.**
  docs/40 §2.2 asserts "Denominator, 248.730 Mt/yr: hillslope sheet-and-rill erosion only", and
  docs/37 clause 4' compares that rate to Tan's RUSLE gross erosion calling it "like-for-like
  denominator" (docs/40 §7 Leg A, verbatim). But MUSLE's output is a sediment YIELD, with delivery
  already inside it. Primary source, fetched and text-extracted by me: SWAT Theoretical
  Documentation v2009, Ch. 4:1 (the reference implementation of this exact equation, same alpha
  11.8, same beta 0.56, same CFRG):
    "Erosion caused by rainfall and runoff is computed with the Modified Universal Soil Loss
     Equation (MUSLE) (Williams, 1975). ... USLE predicts average annual gross erosion as a
     function of rainfall energy. In MUSLE, the rainfall energy factor is replaced with a runoff
     factor. This improves the sediment yield prediction, ELIMINATES THE NEED FOR DELIVERY RATIOS,
     and allows the equation to be applied to individual storm events. ... Delivery ratios ... are
     required by the USLE because the rainfall factor represents energy used in detachment only.
     Delivery ratios are not needed with MUSLE because the runoff factor represents energy used in
     detaching AND TRANSPORTING sediment."
    and eq. 4:1.1.1 defines "sed is the sediment yield on a given day (metric tons)".
  Consequence, measured here:
    * Leg A INVERTS. Tan's 23.7-26.5 t/ha/a is RUSLE GROSS erosion. Put it on our side of the
      comparison with NEH Table 6-2's own sheet-erosion delivery ratio 0.33 -> 7.821-8.745 t/ha/a
      as hillslope YIELD. Ours is 11.6508 t/ha/a adopted => 1.332x - 1.490x ABOVE, not
      2.034x - 2.275x below. Sign flips.
    * Leg B DISSOLVES. Its whole force was "yield <= gross erosion, so a measured yield above our
      gross erosion is impossible". If our number is a yield, the inequality does not apply, and
      1,445.32 / 1,485 = 0.9733 is a 2.7 % agreement with the published Andean yield.
    * Leg C becomes consistency, not a deficit: 1,165.08 t/km2/yr sits at 1.689x the 32-sub-basin
      MEAN measured yield and 0.530x the MAXIMUM -- i.e. between the mean and the max of measured
      in-basin yields, which is where a basin-mean yield belongs.
    * And the retired ratio 0.579-0.740 becomes an interpretable quantity after all: outlet yield /
      hillslope yield = channel+floodplain throughput, i.e. 26.0-42.1 % lost in transit, against
      docs/40's OWN VERIFIED C11 figure for Momposina retention of 20-45 %. It agrees.
  This is the mirror image of the conflation docs/40 was written to expose, and NOTHING in docs/40,
  docs/37, docs/41, docs/42, src/mgb_sediment.py or journal_cite-sdr addresses it: grep for
  "detach", "runoff factor", "transporting", "SWAT" across all of them returns nothing on point.
  What it does NOT do: it does not close C3. Clause 2 (LS level UNRESOLVED, x0.333-x0.421) and
  clause 3 (three 2026-08-11 decisions unaudited) each forbid closure on their own, and docs/37
  says so. What it does do: clause 4' "NOT MET, under-erosive by 1.03-2.27x" is NOT ESTABLISHED,
  and the direction of the residual is unknown until the yield-vs-gross question is settled.
- CHECK 2 PASS, and stronger than sampled. Instead of 3 figures per notebook I checked ALL of them:
  89/89 figure-producing code cells (15: 22, 16: 24, 17: 27, 18: 16) are IMMEDIATELY followed by a
  markdown cell containing all three of "What is plotted" / "What it shows" / "What it means".
  Zero exceptions in any notebook. Terminology: sampled 26 terms across the four notebooks
  (SSC, rating curve, ENSO, ONI, minibacia, Q_s, flux, bootstrap, BFI, KGE, POT, AMS, Qsur,
  recession, MUSLE, SDR, URH, LS2D, q_peak, FG, ADR, PBIAS, IDW, LOOCV, quantile mapping,
  specific erosion). Every one is defined at or before first use in prose, with units. nb15 and
  nb18 open with an explicit vocabulary map that says which section defines each term. Two
  cosmetic exceptions, both NOTE-level: "LS2D" as a token first surfaces inside a loader warning
  in nb18 code cell 18 (the symbol LS is defined in cell 8's equation table with units, and §3
  defines LS2D properly), and "Qsur"/"recession" first appear in nb17 code comments before their
  markdown definitions. No term is used undefined in narrative text. "Mann-Whitney" is absent from
  nb16 -- it uses bootstrap CIs instead; not a defect.
- CHECK 3 PASS with the same caveat pattern. Notebooks carry 45/57, 41/69, 70/76 and 40/47 markdown
  cells containing LaTeX; of the non-plotting computational cells (5, 6, 5, 22 respectively), all
  but four have an equation-bearing markdown within three cells above, and those four are the
  import/setup/closeout cells (nb15 c1, nb16 c5 and c97, nb18 c2), which legitimately have no
  equation. Symbols are given units in the equation cells (e.g. nb15's $Q_s = Q \cdot C \cdot
  0.0864$ with t/day, m3/s, mg/L and the 1e-6 derivation spelled out; nb18 cell 8's eight-row
  symbol table with a units column and a "class" column marking data/derived/cited/assumed).
- CHECK 4: five+ numbers verified against artifacts by INDEPENDENT recomputation, not by reading.
  I called src/mgb_sediment.load_geometry myself under both revisions:
    (1) area-weighted basin C: central 0.013083, prior 0.010823, ratio 1.208787 -- matches nb18
        cell 18's executed output and docs/41 §7 exactly.
    (2) x1.2043 re-derived from the CSV's own erosion shares as the erosion-weighted mean of the
        per-class C ratio: 1.2042755. 248.730 x 1.2042755 = 299.5394 Mt/yr. Matches.
    (3) geometry: n_mini 8672, n_cells 32782, covered area 257,096.93 km2. Matches.
    (4) 299.5387e6 / 257096.93 = 1165.08 t/km2/yr = 11.6508 t/ha/yr. Matches.
    (5) Leg A 23.7/11.6508 = 2.0342, 26.5/11.6508 = 2.2745; Leg B 1485/1445.32 = 1.0275;
        Leg C 1165.08/690 = 1.6885, 2200/1165.08 = 1.8883; G9 199.29/299.5387 = 66.53 %;
        ADR adopted 144/299.5387 = 0.4807, 184/299.5387 = 0.6143. All match.
    (6) NEH 100 mi2 = 258.9988 km2 and 257096.93/259.0 = 992.7x. Matches.
  ONE DISAGREEMENT FOUND: nb18 cell 67 markdown says "Our apparent ratio is **0.5794** and 0.7397
  at the prior cover factor". The notebook's OWN executed cell 64 two cells earlier prints
  0.5789 and 0.7398, and docs/40 §11's reproduction block also prints 0.5789. The two prose values
  are also mutually inconsistent (144/0.5794 => E = 248.533; 184/0.7397 => E = 248.750), so no
  single run produces both -- it is hand-typed drift, not a stale run. Immaterial numerically
  (0.09 %) but it is prose contradicting the executed cell above it in a notebook whose stated
  contract is that numbers come from executed outputs.
- CHECK 8 PASS. Tightened regex for "number immediately followed by a per-area-per-year sediment
  unit": notebooks 15/16/17 have ZERO such expressions (nb16 states outright "No area-normalised
  quantity appears anywhere in this notebook"); nb18 has 11 and ALL 11 carry a model-internal /
  published / measured-yield label in context. docs/41 and docs/42 have zero. docs/40 has 29 with
  4 in the bare §6/§11 arithmetic ledger; each of those is a model-internal or a published
  literature value, none is an observed load divided by a gauge catchment area. No embargo breach.

- CHECK 5, THE ANTI-FITTING CHECK: **PASS**, and it is the strongest-evidenced part of this run.
  journal_cite-cfactor's own ordering, quoted:
    line 14-15 (the plan, written first): "I will record the CHOSEN central value for grassland
      (and every other class) in this journal **before** computing the effect on the 248.73 Mt/yr
      basin total."
    line 27-28 (checklist): "[ ] 7. RECORD CHOSEN VALUES HERE (before computing effect)" then
      "[ ] 8. Recompute area-weighted basin-mean C ... multiplicative effect on 248.73 Mt/yr"
    line 215-219 (step 6 header): "### Step 6 - CHOSEN VALUES, RECORDED BEFORE ANY EFFECT IS
      COMPUTED ... I am writing them down first, deliberately, so the record shows the choice was
      made from the evidence and not from the answer it produces. **I have not computed the basin
      total for these values yet.**"
    line 251-252: "**I am stating in advance that this is a x1.5 change on the dominant term and
      therefore CANNOT close a 1.93-14.8x residual. The evidence does not support the value that
      would.** Recording that here, before the arithmetic, is the point."
    line 301: "### Step 8 - EFFECT (computed only after step 6 recorded the choice)"
  File order alone is not proof of temporal order, so I tested it four independent ways that a
  fitter could not have passed:
    (a) The single largest available UPWARD lever was REFUSED before any arithmetic: Rengifo's
        *pastos enmalezados* C = 0.6, which on 39.87 % of basin area would have been x40 on the
        dominant class and would have closed the gap outright. I VERIFIED that value exists
        (Cuadro 4, primary PDF, see below) and I verified the stated reason: Cuadro 5 of the same
        paper does file *pastos enmalezados* under "Terreno edificable / Tierra baldia", so the
        argument that its author read "enmalezado" as derelict rather than weed-invaded is real,
        not invented.
    (b) The largest single revision in the adopted table goes DOWN and it is the one that hurts
        most: Bare 1.00 -> 0.50 (x0.822), on the class that supplies 35.60 % of the model's
        erosion from 0.196 % of its area. Nobody fitting to close an under-erosion gap halves that.
    (c) The pre-declared magnitude was honoured: net x1.2043 against a residual of 1.93-14.8x.
        The result is nowhere near the answer, and the journal said in advance it would not be.
    (d) The adopted C makes one of the project's OWN pre-registered guards worse, not better:
        nb18 cell 64's executed output shows the SDR=1 alpha at the 144 Mt/yr anchor falling from
        6.832 (prior C) to 5.673 (adopted C), which check_musle_parameters flags "watch <- alpha
        5.67 is below the expected band low 5.9". A value chosen to look good does not trip its
        own guard.
  NOTE, disclosed not concealed: grassland was set to the TOP of its converging low band (0.015
  rather than ICE 1999's 0.010) and forest to the mid of its band, both upward, i.e. both in the
  gap-closing direction. Each is cited (ICE 1999 0.01-0.015 top; Lianes' measured very-degraded
  potrero 0.016) and the journal argues all three degradation indicators explicitly. This is a
  judgment call in the closing direction, small and fully argued. It is not fitting.

- CHECK 6 (docs/41, 3 of 3) **ALL VERIFIED FROM PRIMARY PDFs I fetched and extracted myself**:
    (1) Benavidez, Jackson, Maxwell & Norton (2018), HESS 22:6059-6086, doi
        10.5194/hess-22-6059-2018, Table 8 "C factors for general types of land cover compiled
        from various sources." Extracted from the publisher PDF, row by row:
          Bare ground 1 / 1 / 1 ; Urban 0.2 / 0.03 / 0 / 0 ; Crop 0.128 / 0.01 / 0.255-0.525 ;
          Forest 0.005 / 0.001-0.006 / 0.001 / 0.001 / 0.001 / 0.003-0.048 ;
          Pasture 0.01 / 0.1 ; Scrub 0.005 / 0.007-0.9 / 0.01 / 0.003 / 0.16 / 0.01-0.1
        and the six source columns are Dymond (2010) NZ, David (1988) PH, Morgan (2005),
        Fernandez et al. (2003) USA, Dumas & Fossey (2009) VU, Land Development Department (2002).
        docs/41's rendering is identical, including the "pasture 0.01-0.1, the same factor of ten
        as Roose" claim and the Forest 0.005 = Dymond attribution.
    (2) Lianes, Marchamalo & Roldan (2009), Agronomia Costarricense 33(2):217-235, ISSN 0377-9424.
        Cuadro 5 extracted verbatim. Every value docs/41 attributes is present and correctly
        column-attributed: Bosque claro subestrato herbaceo denso 0,003-0,010; Bosque degradado
        0,037 (Lianes 2009); Matorral denso 0,003-0,030; Matorral claro subestrato herbaceo
        degradado 0,030-0,100; Pasto FAO 0,009 / ICE 0,01-0,015 / Marchamalo 0,013; Pasto natural
        o mejorado 0,008; Pastizal natural pastoreado 0,040-0,200; Pastizal cultivado (manejado)
        0,003-0,040; Potrero carga normal 0,002 / degradado 0,002 / muy degradado 0,016; Cafe
        0,09 and 0,080; Banano 0,062; Cacao 0,05; Cultivos permanentes asociados densos
        0,010-0,300; no densos 0,100-0,450; Cultivos anuales 0,495. Cuadro 4 also confirms the
        field-measured SLRs (bosque degradado 0,037, potrero muy degradado 0,016) and that SC
        (cubierta en contacto con el suelo) is a subfactor, which is the physics docs/41 s6 leans on.
        docs/41's "this table is internally inconsistent" is also right: the original prints
        "Pastizal natural completo 0,030-0,010", i.e. backwards.
    (3) Rengifo-Rengifo, Munoz-Gomez & Toro-Trochez (2022), Biotecnologia en el Sector Agropecuario
        y Agroindustrial 20(2):29-44, doi 10.18684/rbsaa.v20.n2.2022.1738. Cuadro 4 verbatim:
        Afloramientos rocosos 0,25; Arbustos 0,25; Bosque de galeria/ripario 0,09; Bosque denso
        0,001; Herbazal 0,01; Lagunas/Lagos/cienagas 0,001; three Mosaico-de-pastos rows 0,003;
        Mosaico de cultivos 0,25; **Pastos enmalezados o enrastrojados 0,6**; Pastos limpios 0,01;
        Red vial 0,001; Rios 0,001; Tejido urbano continuo 0,001; Tierras desnudas o degradadas 1;
        Zonas glaciares y nivales 0,25. Cuadro 5 verbatim: Tierra agricola 0,4 / Terreno edificable-
        Tierra baldia 1 / Area arbolada 0,1 / Cuerpos de agua 0,5. Every docs/41 use is exact,
        including the three internal inconsistencies it flags. Municipality list and the Pacheco
        et al. (2019) attribution also confirmed from the article's own abstract and bibliography.
  **A RETRACTION I owe this journal.** Mid-check I believed I had found a CRITICAL misattribution:
  Crossref's record for that DOI lists "Fernando Andres Munoz Gomez" as first author (sequence
  "first") and the page range as "1-13", which would have made "Rengifo-Rengifo et al. (2022),
  20(2): 29-44" wrong twice over. I then fetched the published galley
  (.../article/view/1738/1734, 16 pp.) and the byline on the article itself reads
  "RENGIFO-RENGIFO, INGRIT-YOHANA(1); MUNOZ-GOMEZ, FERNANDO-ANDRES(2); TORO-TROCHEZ, OSCAR-ANDRES(3)",
  and the printed folios run exactly 29, 30, ... 44. docs/41 is RIGHT on both author order and
  pages; CROSSREF's metadata is the thing that is wrong. Finding withdrawn. Recording it because
  a critic who only checked the cheap source would have filed a false CRITICAL against a correct
  citation, and this project's own rule is that the primary source wins.

- CHECK 7 PASS, and it is honest in exactly the way the check asks. docs/37's amendment opens
  "# AMENDMENT A1 (2026-08-11) - C3 is **OPEN** under the revised closure conjunction" / "**C3 is
  OPEN.** Two clauses of the revised conjunction are not met and one is retired." The conjunction
  WAS rewritten around something evaluable: clause 4 (the SDR band) is struck through and marked
  RETIRED with "A retired gate is neither a pass nor a fail", and a new clause 4' -- the gross
  hillslope erosion RATE against published levels -- carries the test. OPEN then rests on clause 2
  (LS formulation level UNRESOLVED, x0.333-x0.421, flagged "This clause alone forbids closure
  today, independently of everything else in this amendment"), clause 3 (the three 2026-08-11
  decisions NOT ESTABLISHED because unaudited) and clause 4'. The doc states explicitly that C3
  "does not stay open on the strength of the retired band". No CLOSED verdict anywhere, no
  reliance on the retired band in either direction, and the doc names the reverdict agent and the
  superseded numbers (248.730 -> 299.539) in the same breath. It also records that clause 1's MET
  quotes the prior-C level and that A1.3 supersedes it.
  Two honesty items I checked and found already self-reported: docs/37 A1.4 concedes "Leg B has
  stopped being a proof" (2.8 % gap), and nb18 cell 71 volunteers its own first-draft defect (a
  combined bracket wrongly computed as min() over raw ratios, reported as 0.59x, corrected to
  1.03x) and a 4th-decimal disagreement with docs/37. That is the behaviour of a record, not a
  brochure.

--- run 3, second pass: what the audit trail ALREADY discloses (severity corrections) ---

I found docs/37 A1.7 "Corrections and consequential edits this amendment requires elsewhere" and
A1.8 "Reproduction" late, and they force me to DOWNGRADE my own CHECK 10 finding. Recording the
downgrade rather than leaving the harsher version standing:

- A1.7 item 2 says, verbatim: "**`tests/test_sediment.py` has two stale hard-coded C assertions and
  the suite is 94 passed / 2 failed.**" It then names line 310 (0.003 -> 0.005, with
  UNIT_DAY_LOAD_T 1293.5691626849571 -> 2155.9486044749287) and lines 683-684 (value set ->
  {0.0, 0.005, 0.015, 0.03, 0.2, 0.5}), states the cause is the CSV rewrite and not a code change,
  warns that the SYNTHETIC class_c={1: 0.003} regression must be LEFT ALONE because it is
  convention arithmetic, and offers cp_revision='prior_2026_08_11' as the alternative pin.
- A1.8 says: "python3.10 -m pytest tests/ -q   # 94 passed, 2 failed (A1.7 item 2), 2026-08-11".
- commit 8807951's BODY says: "IMPORTANT, and disclosed rather than patched: as of this commit 2 of
  the 96 FAIL ... Proof it is the data: reloading the old table through the engine's own option
  (cp_revision='prior_2026_08_11') gives exactly the C set the tests whitelist."
  That is the exact experiment I ran independently, with the exact result I got.
  So the commit title's "96 tests" is a case COUNT, not a green claim, and the body is explicit.
- A1.7 item 4 likewise pre-discloses my docs/40-staleness observation: "The 248.730 Mt/yr headline
  is superseded by 299.539 Mt/yr wherever it is quoted - docs/35, docs/36, this document's
  §2-§4, `docs/40` §1 and §7, `docs/42` §4, docs/PROGRESS.md, progress_map.html ... `docs/40`'s
  three legs are re-evaluated at the new level in A1.4; its §1 table and §11 reproduction block are
  correct for the prior C and should be read as such."
- A1.7 item 1 pre-discloses that docs/42 G9's registered 36.10 %/63.90 % split moves to
  33.47 %/66.53 %, and item 5 that §2's "SDR must be < 1" is false for the computed quantity.
CONCLUSION on those: red suite = real debt, correctly diagnosed, disclosed in three places, fix
written down. WARN, not CRITICAL. docs/40 staleness = WARN downgraded to NOTE, with the single
residual point that the disclosure lives in docs/37 and NOT in docs/40, so a reader who opens
docs/40 alone still meets 248.730 / 9.675 t-ha-yr / "1.59-2.74x" with no in-document flag.

- **FINDING 2 -- the one thing A1.7's consequential-edit list does NOT cover: the engine's own
  docstring still states the retired gate as live fact.** src/mgb_sediment.py lines 191-197,
  read by me today (file mtime 08:54:50, i.e. AFTER docs/40 retired the band at 08:38 and AFTER
  docs/41 changed the default level at 08:47 - the CP_REVISIONS block was added in that same edit):
    "The adopted row is on the right side of the outlet anchor at last - but only barely: it implies
     a basin sediment delivery ratio of 0.58 - 0.74, where the published range for a basin of
     257,097 km2 is roughly 0.05 - 0.3.  **This module does not resolve that residual, and does not
     let ``alpha`` resolve it either** - see ``docs/37_c3_closure.md``, which records C3 as OPEN for
     exactly this reason."
  Three problems in one paragraph: (i) it presents the RETIRED, uncited 0.05-0.3 band as "the
  published range", which is precisely the thing docs/37 A1.2 struck and precisely what this run's
  own hard rule forbids ("an uncited plausibility band may not be used to pass OR fail a gate");
  (ii) it tells the reader C3 is OPEN "for exactly this reason", which is now false - C3 is open on
  clauses 2, 3 and 4'; (iii) the convention table 12 lines above still labels
  "williams_m3 + us_customary (DEFAULT) 248.72 Mt/yr" as the default output, but the default also
  carries cited_central C, so the default output is 299.54 Mt/yr - the docstring understates its own
  default by 20.4 %. grep confirms the file contains no reference to docs/40 at all and no
  retirement note on that band, and src/mgb_sediment.py is absent from A1.7 item 4's list of files
  where 248.730 is superseded. This matters more than a doc typo because the engine docstring is
  what C4 will read, and it outlives the amendment.

- **FINDING 1 stands and is NOT covered anywhere.** Re-checked after reading A1.7: docs/37 mentions
  "sediment yield" only twice, both about the gauge-referenced embargo (lines 111, 451), never about
  what MUSLE's own output is. A1.7's six items do not include it. And the sharpest version of the
  finding is an internal contradiction inside ONE notebook:
    nb18 cell 8 (§1): "Because runoff already encodes how much water was available to *carry* the
      soil away, MUSLE's output is closer to 'sediment delivered from this patch to its stream' than
      to 'soil detached on this patch'. Section 6 shows this distinction is not pedantic - a whole
      closure gate was retired over it."
    nb18 cell 68 (§6.4): "**Leg A - the only like-for-like denominator.** Tan, Liu & Lu (2024) ...
      report **RUSLE hillslope** erosion of 23.7-26.5 t/ha/a ... Hillslope against hillslope, so
      this is the leg that counts."
  RUSLE is USLE's descendant, and the same notebook's §1 says USLE "predicts long-term average soil
  loss from rainfall energy", i.e. detachment. So §6.4 labels a delivered-quantity-vs-detached-
  quantity comparison "like-for-like", using the distinction §1 had just drawn to retire the
  previous gate. The verdict turns entirely on that leg (docs/37 A1.4: "Leg A - the only leg whose
  denominator is like-for-like - still reports the model 2.03-2.27x under-erosive").
  And the other two shortfall legs do not carry it either:
    Leg B is conceded by docs/37 itself - "Leg B has stopped being a proof ... it is no longer
      *evidence*" (2.8 % gap at the adopted C).
    Leg C's shortfall form compares our BASIN MEAN (257,097 km2) against the MAXIMUM of 32
      sub-basins of 320-59,600 km2 (2,200 t/km2/yr). A spatially variable field's mean is
      arithmetically required to sit below its own maximum, so 0.530x cannot be evidence of
      under-erosion. The valid like-scale comparison in that source is the 32-sub-basin MEAN
      (~690), where the model is 1.689x ABOVE - which the notebook itself flags as the required
      direction. The model's own field is not flat either: docs/37 line 462 gives Andean flanks
      1,445.32 vs lowland floodplain 77.41, an 18.67x internal range.
  So all three shortfall legs are individually unsound and clause 4' "NOT MET, under-erosive by
  1.03-2.27x" is NOT ESTABLISHED. It does not close C3 - clause 2 (LS level UNRESOLVED, x0.333-
  x0.421) and clause 3 (three unaudited decisions) each forbid closure independently, and docs/37
  says so in those words. What it does is remove the residual's measured direction.
  Bonus consequence worth putting in front of the advisor: under the yield reading the retired ratio
  0.579-0.740 becomes an interpretable quantity - outlet yield / hillslope yield = 26.0-42.1 % lost
  in channel and floodplain transit - against docs/40's OWN primary-verified C11 figure for
  Depresion Momposina retention of 20-45 %. Those agree. The number the project spent this run
  retiring may have been telling it something true.

- FINDING 3 (warn, small): nb18 cell 67 prose says "Our apparent ratio is **0.5794** and 0.7397 at
  the prior cover factor", against its own executed cell 64 which prints 0.5789 / 0.7398 and
  docs/40 §11 which also prints 0.5789, 0.7397. The two prose values cannot come from one E
  (144/0.5794 => 248.533; 184/0.7397 => 248.750), so it is typing drift. 0.09 % - immaterial to
  every conclusion - but it is narrative contradicting the executed cell two cells above it.
- FINDING 4 (note): the run's own one-line summary of the C work says "Grassland C moved 0.010 ->
  0.015 ... a label correction more than a value one". SIX of eight rows moved: Forest 0.003->0.005
  (55.77 % of area, 36.48 % of prior erosion), Shrub 0.005->0.015, Grassland 0.010->0.015,
  Urban 0.010->0.030, Bare 1.000->0.500 (35.60 % of prior erosion, HALVED), Wetland 0.001->0.005.
  docs/41, the CSV, src/mgb_sediment.py's docstring and nb18 cell 20 all report all six correctly
  and nb18 names Bare as "the largest single change in the table and it goes *down*". The
  understatement is in the summary only, but Bare-halved and Forest-up-67 % are the two biggest
  levers and a one-line summary that omits both misdescribes the revision.
- FINDING 5 (note): the run's summary also states the residual is "1.59-2.74x" and that "it sits
  inside the 2-5x that docs/37 §4 candidate 1 (the C factor) already estimated for itself".
  Both halves are contradicted by docs/37 A1.4, which I read: the residual at the adopted default
  is **1.03-2.27x** (1.59-2.74x is the prior-C column), and candidate 1 was MEASURED at x1.2043 with
  the verdict "docs/37 §4 candidate 1 estimated 2-5x for C on its own; the *evidence* ... supports
  x1.2043 ... it did not deliver what candidate 1 hoped for" and "The C revision accounts for
  roughly a quarter of the residual in log terms, and no more." The C revision is also ALREADY
  SPENT inside the 1.03-2.27x, so it cannot additionally explain it. The documents are right; the
  summary is not, and it is wrong in the reassuring direction.

Checklist run 3: [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 [x]8 [x]9 [x]10.
Wrote nothing outside this journal. Scratchpad scripts (nbscan/spec/spec2/terms/emb/emb2/nbdump.py)
and all fetched PDFs live outside the repo. No git, no calibration launched, frozen artifacts
read-only and mtime-verified unchanged.
