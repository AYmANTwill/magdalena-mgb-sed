# journal — x59-write (WRITER phase, docs/59)

Agent slug: `x59-write`. Role: WRITER. I own `docs/59_cross_implementation_comparison.md` and this
journal, nothing else. I write no other file, edit no frozen doc, run no fit, quote no alpha-hat of
ours, and run no git command in either repo.

Started 2026-08-12.

## 0. Plan

1. Create this journal (done — first action).
2. Verify the docs/59 filename is free and 54-58 are taken.
3. Read the four measurement journals to confirm the briefs match what the agents recorded, and to
   pick up anything the brief summaries dropped.
4. Verify house style from docs/47 and docs/55 (blockquote verdict, numbered sections, grade
   ladder, disclosure, cross-reference table).
5. Verify the load-bearing OUR-SIDE numbers I am asked to quote: f_LS = 0.25146, C4.3 medians
   -0.118 / +0.139, C5 median rate ratio 3.046755091543662 / 18 stations, 66.53 %, the bar
   [-0.26, 0.44], -0.414, the C revision x1.20427, O10 in docs/41.
6. Write docs/59.
7. Append the verification log as I go.

## 1. Log

### 1.1 docs/59 is free (2026-08-13)

`ls docs/` → 54, 55, 56, 57, 58 present; **no 59**. `ls docs/agents/ | grep x59` → the four
measurement journals exist (`journal_x59-{overlap,bridge,inputs,theirnumbers}.md`, 13,527 /
13,972 / 26,828 / 21,807 bytes) plus my own. Filename claimed:
`docs/59_cross_implementation_comparison.md`.

### 1.2 House style read (docs/47, docs/55)

- `docs/47`: title line `# 47 — <subject>: **VERDICT**`; dated attribution line naming the writing
  agent and its journal, and stating what the doc does NOT edit; `> ## THE VERDICT` blockquote;
  numbered `## N — ` sections; `## 7 — What this run could NOT settle` as a `| # | open item |
  what would settle it |` table with `O`-prefixed numbering; `## 8/9.5 — Disclosure` in bullets,
  ending with the yield embargo and "no git command was run".
- `docs/55`: same shape, shorter; a pre-fit disclosure blockquote; a per-station table; `## 6 —
  Owed and NOT done`; `## 7 — Disclosure`.
- Grade ladder, verbatim from `docs/46` §4.1 (which cites `docs/42` §3.3 / §6 G6 item 5 as amended
  by `docs/37` A1.6 item 3): DERIVED / IDENTIFIED / CITED / ASSUMED / UNVALIDATED. **UNRESOLVED is
  not a row of that table**; `docs/37`:11 and `docs/47` use it for a question left open rather than
  a quantity graded, and I use it that way only.

### 1.3 Our-side numbers verified this session (read-only)

| claim | verified from | value |
|---|---|---|
| C4.3 est (a) in-box `F_report` | `docs/55` §1 | **−0.118** at α = 2.0 (box floor), β 0.60 |
| C4.3 est (b) | `docs/55` §6 | **0.139**, unconstrained optimum α ≈ **5.9** *inside* the box |
| C5 modelled median rate ratio | `data/processed/c5_enso_contrast.json` | `/modelled/median_ratio` = **3.046755091543662**, geomean 3.0563436523427323, `n_stations` 18 |
| C5 observed comparators | same JSON | `est_a_median` **4.620163547568586**, `est_b_median` **2.948674885718534**, `median_rate_ratio_primary` "~3-5" |
| 66.53 % unobserved erosion | `docs/37`:639, `docs/43`:16, `docs/45`:67 & §490 (G9) | **66.53 %** = 199.29 of 299.54 Mt/yr; 33.47 % observed; 801.1 km of channel |
| C revision | `docs/45`:200, `docs/37`:542 | erosion-weighted ×**1.20427** (full precision 1.204272539864846), `cp_revision='cited_central_2026_08_11'` |
| f_LS adopted | `docs/37`:113-114 | **0.25146** erosion-weighted POINT (`ls_formulation = buarque_2015_dg`); 1/f_LS = 3.9767756303× |
| Π condition number | `docs/42`:115, `docs/37`:789/1133 | **inf**, exactly singular |
| bar + no-skill | `docs/45`:84 (Fagundes 2018 §6.3.1), :311, :589 | bar [−0.26, 0.44]; mean predictor KGE = 1 − √2 = **−0.414** |
| pooling prohibition | `docs/34` §1.2 | rates only; unequal-window totals "NEVER divided by each other" |
| Momposina | `docs/45`:460, :499; `docs/47`:360 | "above vs below the Momposina" is **NOT EVALUABLE, measured** |
| O10 | `docs/47` §7 / §9.3 | `docs/41` remains **unaudited**; "no `docs/41` audit exists in `docs/agents/`" |
| O-numbering high-water mark | `docs/47` §7 | O1…O12 (O6, O7 closed) — so docs/59 must NOT reuse O1–O12; I number mine **X1…X12** |

### 1.4 ONE NEW MEASUREMENT BY THIS WRITER (disclosed, read-only)

M1 concluded *"THEY ARE AHEAD OF US ON COORDINATES"* (8 of their 21 fitted stations excluded by
our C1.0 for absent lat/lon) and no measurement agent checked `docs/57` (B5), which is dated
**2026-08-12** — the day before. I checked it, because publishing M1's sentence unqualified would
have been wrong.

```
python3.10 -c "import pandas as pd; r=pd.read_csv('data/processed/ssc_recovered_coords.csv',dtype=str); ..."
cols ['code','lat','lon','minibacia','in_basin','n_ssc','n_ssc_cal','n_ssc_lanina','n_ssc_elnino','self_paired_q']
rows 46 ; recovered set size 46
21187030 True | 22027010 True | 24017830 True | 24037030 True
24037040 True | 24037130 True | 26177030 True | 28037090 True
```

Detail for exactly those 8 (all 8 of M1's "no coordinates" codes):

```
       c      lat        lon  minibacia  in_basin  n_ssc  self_paired_q
21187030 4.231946 -75.092981      14265      True   5853          False
22027010 3.328278 -75.613111      15927      True   6253          False
24017830 5.618389 -73.612861      11540      True   5829          False
24037030 5.681722 -73.231139      11404      True   5147          False
24037040 6.453972 -72.403056       9910      True   6253          False
24037130 5.748833 -73.189889      11319      True   6253          False
26177030 4.892500 -75.882694      12893      True   6642          False
28037090 9.648193 -73.646367       3909      True   3133          False
in_basin (all 46):  True 43 / False 3
self_paired_q (all 46): False 46   <-- 0 of 46, i.e. 0 of the 43 in-basin
```

**Consequence, and it cuts both ways.** M1's coordinate deficit is REAL as of C1.0 and was
**discharged by `docs/57` on 2026-08-12** — all 8 are geocoded, all 8 are in-basin, all 8 carry
3,133–6,642 SSC records. So docs/59 must not say we lack their coordinates. But `self_paired_q` is
**False for all 46**, which is `docs/57` §2's finding (0 of 43 in-basin recovered sites have
same-code discharge), and that is the exact, measured reason their 21 and our 18 differ: their
objective scores **concentration** and needs no paired Q; ours scores **flux** and cannot exist
without it. Both projects are right on their own terms. This reconciles M1's caveat, M2 §13 and
`docs/57` in one arithmetic statement, and it is the single most useful thing this writer added.

### 1.5 M1/M2 reconciliation check

M2 flagged its "shared = 8" as unreconciled with M1. Both lists are identical — 22017010,
22017030, 22057090, 23127010, 24037390, 26017060, 26127010, 26137110 — M1 §C and M2 §8. The count
is therefore reconciled and docs/59 may quote **8** as settled. Recorded because M2 explicitly
forbade quoting it until reconciled.

### 1.7 SECOND WRITER MEASUREMENT — an M1/M4 numeric disagreement, resolved by recomputation

M1 and M4 disagree on their validation-cell `alpha × c_mult`: M1 says 5.5818822479283315, M4 says
5.581900193275565. Recomputed from the two JSON fields at full precision rather than picking one:

```
python3.10 -c "a=96.58548959666564; c=0.05779232694874972; a0=55.40533705803028; c0=0.04887856036752898; ..."
main   2.7081331120742234
val    5.581900193275565      <-- M4 correct; M1's value is a rounding artifact
ratio  2.0611616793829812
dscore 0.004409952544391804
group main 2.23532271514266 | group val 3.8655776402965714 | group ratio 1.7293152411999122
a0/11.8 4.695367547290701 | 1/c0 20.4588677015193 | (a0*c0)/11.8 0.229502806107985 | inverse 4.357245198690437
```

All of M3's and M4's derived quantities reproduce: ×2.0611616793829812, +0.004409952544391804,
group ratio ×1.7293152411999122, 4.695368, 20.458868, 0.2295028061, 4.357245. **Two sites in
docs/59 were corrected from M1's value to the recomputed one before publication** (the verdict
blockquote and the §4.2 table), and the disagreement is disclosed in docs/59 §9 rather than
silently resolved.

### 1.8 Write (appended last; the 1.7 entry above was made mid-write, hence the out-of-order number)

Wrote `docs/59_cross_implementation_comparison.md` (10 sections, per the commission). Nothing else
written. No git command run in either repo. No engine default moved, no fit run, no alpha-hat of
ours produced, no frozen artifact opened. Their clone read-only throughout; this writer executed
nothing inside it.


---

## Session 2 (2026-08-13, post Phase-1.5 evidence) — REWRITE

Reason for a second pass: the colleague's 23-file data bundle + written answers arrived
AFTER the first draft of docs/59 was written (file mtime 04:44; bundle files 05:00-05:34).
Phase 1.5 evidence OVERRIDES the four measurements M1-M4 where it contradicts them.

Commands run this session (all read-only except my own journal + docs/59):

1. `ls -la docs/59_cross_implementation_comparison.md docs/agents/journal_x59-write.md`
   -> 59: 68741 bytes, 872 lines, mtime Aug 13 04:44. journal: 8496 bytes, 138 lines.
2. `ls -la data/raw/colleague_share/` -> ANSWERS_C1_C2_C3.md (7431), MANIFEST.md (6294),
   input_hashes.txt (2699). All mtime 05:00-05:04.
3. `cat data/raw/colleague_share/MANIFEST.md` -> read in full. Key confirmations:
   - SSC 59 total / 57 plausible / 2 rejected; 25 discharge_validated + 32 nearest_centroid.
   - Discharge 118 total / 114 plausible / 4 rejected; plausible = specific discharge in
     5-150 L/s/km2.
   - 21 = SSC stations with >=30 obs days inside 2013-01-01..2014-12-31.
     90 = discharge gauges with >=180 overlapping in-window days.
   - basin_magdalena.pkl: 7,929 unit catchments, 184 m routing grid, LS2D on the routing
     grid "deliberately", floodplain L-V-A curves, 12 HRU fractions.
   - precip: gauge-CHIRPS merge, 88 gauges >=80% completeness supply the level, CHIRPS the
     pattern, monthly log-ratio IDW-interpolated, multiplicative, ratios clipped 0.25-4.0.
     Basin mean 1,965 mm/yr. 3,287 days x 7,929 catchments.
   - stage1_*/stage2_* WITHHELD: "a recalibration is running right now and those files are
     mid-rewrite".
   - SSC defect: concentration taken from mass left in reach AFTER export, not from flux;
     74% of 7,929 reaches reported exactly 0.00 mg/L at a daily step; 46 of 57 gauged
     reaches biased low. "Any pre-fix SSC comparison against us is invalid."
   - Their warning: median vs area-weighted mean ranked trials in OPPOSITE order.
4. `cat data/raw/colleague_share/ANSWERS_C1_C2_C3.md` -> read in full.
   - C1: stage-3 skipped-vs-ran unanswerable from git (both paths emit byte-identical
     JSON: 21_calibrate_sediment.py:256-258, :300, :316-318, :328-345). Re-run tonight:
     stage 3 DOES fire, 3 rules, +0.068 -> +0.087. TriggerSet last-match-wins bug
     (musle.py:204-208) killed one of the three rules while still reporting it.
   - C2: row-random split (ssc.py:448), docstring defence at :427-430 "empirically wrong
     for the subset actually used". 787 samples, 82 sites, 58 with >1 sample, 97% of
     samples in repeat-visit sites, Taihu 113 = 14%. Site-grouped: S2 0.918->0.801
     (+0.118), L8 0.905->0.781 (+0.124), grouped spread 0.73-0.88. 41 South American
     samples from 3 Brazilian sites, 0 Colombian.
   - C3: no precip_gauges_daily_qc.csv exists anywhere in their repo -> nothing bypassed.
     In-script QC at 15_build_forcing_v2.py:52-108 (<80% reporting dropped :80-93,
     no-coordinate records dropped :74-79, abort under 20 gauges :95-99). They intend to
     ADOPT our selectivity statistic; their 80% cutoff discards 199 of 287 gauges.

### 2.1 NEW MEASUREMENTS MADE BY THIS WRITER THIS SESSION (read-only)

**(a) THE FIRST HASH-LEVEL PROOF OF A SHARED INPUT.** `input_hashes.txt` lists
`02_basin_and_soils/minibacia_soil_params.csv` = sha256
`6e5940ecdbd06c8b89b09e9134cbe6586933ff9c6971e896feb9e85b19ae38b1`.

    $ ls -la data/processed/minibacia_soil_params.csv && sha256sum data/processed/minibacia_soil_params.csv
    -rw-r--r-- 1 knade 197609 398698 Jul 30 22:28 data/processed/minibacia_soil_params.csv
    6e5940ecdbd06c8b89b09e9134cbe6586933ff9c6971e896feb9e85b19ae38b1 *data/processed/minibacia_soil_params.csv

=> **BYTE-IDENTICAL.** Our soil/K product IS their soil/K product. This CLOSES the soils row of
M3's shared-inputs table in the opposite direction from M3's code read (which found
`build_k_factor` -> SoilGrids + EPIC). Phase-1.5 rule applies: the author's own account (MANIFEST
A9, "soil/K source as used") WINS, and it is now corroborated by a hash rather than taken on trust.
It also partially closes X12 (byte-identity of shared inputs) for exactly one row.

**(b) The git bundle hash matches the brief.**

    $ sha256sum data/raw/refs/yben409_sediment_repo.bundle
    adf7a1d1bf21d62057257de14bc8adf0584facfa1e37cfe1f5b7afafb551ca9e *data/raw/refs/yben409_sediment_repo.bundle

**(c) WHAT IS AND IS NOT ON OUR DISK from the bundle.** `ls -la data/raw/colleague_share/` returns
exactly THREE files: MANIFEST.md, ANSWERS_C1_C2_C3.md, input_hashes.txt. The 20 data files listed
in input_hashes.txt (Tiers 1-5) are NOT extracted into our repo, and `ls data/raw/*.zip` ->
"No such file or directory". `data/raw/refs/` holds `yben409_sediment_repo.bundle` (82,047,044 B)
and `buarque2015.pdf`. So every bundle DATA file remains unread by me; only the hash list, the
manifest and the answers are readable. Recorded as a limit on what docs/59 may claim.

**(d) OUR ENGINE HAS NO TRIGGER / RULE MECHANISM** (the check their C1 asked us to make).

    $ grep -ric "trigger" src/mgb_sediment.py src/mgb_transport.py
    src/mgb_sediment.py:0
    src/mgb_transport.py:0
    $ grep -ril "trigger" src/            -> src/calib_v2.py, src/dhime_dates.py,
                                             src/nbgen/make_nb16.py, src/nbgen/make_nb17.py
    $ grep -in "trigger" <those four>     -> all hits are PROSE about pre-registered TEST triggers
                                             (docs/33 BFI term "NOT triggered"; the 25 % single-point
                                             leverage trigger at EL PROFUNDO; H-PEAK refit triggers).
                                             No rule set, no overlap resolution, no per-domain
                                             strength multiplier anywhere.
    src/mgb_transport.py:521  k_dep: object = 0.0    (deposition default exactly zero, unfitted)

=> The `TriggerSet` last-match-wins class of defect (their musle.py:204-208) is **NOT APPLICABLE**
to this engine. C4.3 fits alpha and beta only, with k_dep FIXED at 0.0 /km. Checked-and-clean.

**(e) Our rainfall comparator, taken from the RIGHT place.** `grep -n "2,036\|2073.1" docs/16` ->
line 452: "| Basin-mean rainfall **2,206 mm/yr** | **2,073.1 mm/yr** (2008-2018) - **2,036.4 mm/yr**
(2009-2017) | s14.2 / s14.1 |". So 2,206 is the STALE headline and must not be used. Their forcing
spans 2009-2017 (3,287 days, verified: (2017-12-31 - 2009-01-01).days + 1 = 3287), so the
like-for-like comparator is **2,036.4**.
Arithmetic (python3.10): 1965/2036.4 = 0.9649381261048909; gap = 3.5061873895109055 %.
Against 2,073.1 (2008-2018): 0.9478558680237326, gap 5.2144131976267385 %.

**(f) Satellite arithmetic:** 0.918 - 0.801 = 0.11699999999999999 (S2); 0.905 - 0.781 = 0.124 (L8);
Taihu 113/787 = 14.358322744599747 %; South American 41/787 = 5.209656925031767 %.

### 2.2 docs/59 REWRITTEN (session 2)

`docs/59_cross_implementation_comparison.md` rewritten in full, 1,206 lines. Structure:

    0  THE PIN (snapshot; d055561; bundle sha256; counterpart numbers mid-rewrite)
       THE VERDICT (blockquote)
    1  What was compared, on what evidence (Tier A = M1-M4, Tier B = author's answers; B overrides A)
       1.3 SIX corrected framings (4 of R1's wrong premises + 2 of the brief's)
    2  The two configurations side by side
    3  The score comparison: VOID
    4  THE CENTRAL RESULT: algebraic leg SURVIVES, empirical leg SUSPENDED
    5  What the comparison narrows (soils hash; 184 m terrain; K narrowed, Qsur/C/LS not;
       precip accusation WITHDRAWN; C factor + O10; 5.8 the CHIRPS candidate, proposes nothing)
    6  The ENSO contrast (station counts corrected; bars compared; B3 in progress)
    7  The satellite retrieval (leakage +0.118/+0.124 measured by them; regional transfer binding)
    8  Open items X1-X4, X6-X8, X11-X14; 8.2 CLOSED (X5, X9, X10, stage-3, M1's coordinates);
       8.3 the trigger check, negative; 8.4 what we owe them; 8.5 the docs/57 reconciliation
    9  Disclosure (four own measurements named; embargo; nothing reasoned backwards)
   10  Cross-references + 10 OWED rows

Verification of the written file:
    $ grep -n "t/km" docs/59_...md   -> ONE hit, line 1160, which is the embargo DECLARATION itself.
                                        No t/km2/yr quantity anywhere. R2's 5-150 L/s/km2 screen is
                                        quoted as a specific-discharge criterion and flagged as not
                                        engaging the embargo.
    $ grep -c "" -> 1206 lines.

What I did NOT do, deliberately:
  - did not print any ranking of the two projects' scores (score comparison is VOID);
  - did not present the x2.061 / +0.0044 result as a measured demonstration (SUSPENDED, owed);
  - did not quote 2,206 mm/yr (stale) as our rainfall comparator;
  - did not open, extract or read any of the 20 bundle DATA files;
  - did not run git in either repo; did not run a fit; did not move an engine default;
  - did not pre-register anything, and did not propose re-opening Phase B (docs/33 s5.1 cited);
  - introduced no threshold, band, tolerance or materiality bar anywhere;
  - edited no other document; every consequence for docs/16, 26, 32, 34, 41, 45, 47, 56, 57, 58,
    00_INDEX and progress_map.html is recorded as OWED in s10, not enacted.
