# journal_x59-lens-numbers

Adversarial lens: do the numbers and citations in docs/59 hold?
READ-ONLY except this file. Slug: x59-lens-numbers. Started 2026-08-13.

## Plan
1. Read docs/59 in full, extract every quoted figure and every docs/NN section citation.
2. Re-verify their numbers from their clone (params jsons, metric csvs, rs summary, code).
3. Re-verify our numbers from our repo (docs/55, docs/56, docs/34, docs/45, docs/46, docs/37).
4. Check each cross-reference resolves to a section that CONTAINS the claim.
5. Count checked / clean / wrong.

## Log

### 1. Read docs/59 in full (1,206 lines) + the Tier-B bundle text

    $ wc -l docs/59_cross_implementation_comparison.md            -> 1206
    $ ls -la data/raw/colleague_share/  -> ANSWERS_C1_C2_C3.md 7431, MANIFEST.md 6294,
                                           input_hashes.txt 2699   (three files, as doc 59 s1.2 says)
    $ cat data/raw/colleague_share/{MANIFEST.md,ANSWERS_C1_C2_C3.md,input_hashes.txt}  -> read in full

### 2. THE BUNDLE HASH LIST HAS 20 ENTRIES, NOT 23  (doc 59 s0 says 23)

    $ grep -c "^[0-9a-f]\{64\}  " data/raw/colleague_share/input_hashes.txt   -> 20

MANIFEST.md's own line says "sha256 + mtime for all 23 files in this bundle" -- so the 23 is
THEIR error, but doc 59 s0 states it as a fact about the file ("whose 23 member hashes are
listed in ..."). s1.2 says 20; X12 says "remaining 19". 20 is right; s0 is wrong.

### 3. THE BUNDLE ARCHIVE IS ON THIS DISK (doc 59 s1.2 / s9 imply otherwise)

    $ find ... -iname "*magdalena_share*"
      /c/dev/magdalena-mgb-sed/magdalena_share_for_colleague.zip                306200202 B
      /c/Users/knade.MSI_TWILL/Downloads/Mobile Devices/magdalena_share_...zip  306200202 B
    $ grep -n "zip" .gitignore -> line 52 "*.zip"  (gitignored, hence invisible to git status)
    $ python3.10 zipfile listing -> 60 members; ALL 20 data files present, incl.
      02_basin_and_soils/basin_magdalena.pkl              8,169,760 B
      01_essential_small/observed_ssc_stations.csv            7,146 B
      01_essential_small/observed_ssc_daily.parquet         284,663 B
      03_large_forcing/precip_mm_day.parquet            92,465,380 B
      03_large_forcing/etp_mm_day.parquet              252,035,867 B

doc 59 s1.2: "no bundle archive is present under `data/raw/`" -- literally true (it is at the
REPO ROOT), but the inference drawn from it ("every claim ... rests on the manifest text or on
a hash, never on a read of the file") is not supported, and X3/X4/X11 are settleable from disk
today. journal_x59-write.md line 209 records only `ls data/raw/*.zip` -> not found.
Note s0 quotes the zip's exact size 306,200,202 B, which is obtainable only from that file.

### 4. THEIR PARAMETERS AND PRODUCTS -- ALL EXACT

    $ python3.10 (json.load on outputs/{calibration,calibration_val}/stage2_sediment_params.json)
      main  alpha 55.40533705803028 beta 0.3980082263356884 alpha_tc 0.6174944111935904
            c_mult 0.04887856036752898  score 0.05461202762457862  n 21  window 2013-01-01..2014-12-31
            final == stage2, stage3_trigger_rules []
      val   alpha 96.58548959666564 beta 0.3493190336411669 alpha_tc 0.34930405763655487
            c_mult 0.05779232694874972  score 0.05902198016897042  n 13  same window
      prod1 2.7081331120742234   prod2 5.581900193275565   ratio 2.0611616793829812
      alpha ratio 1.7432524504905407   c_mult ratio 1.1823655712074193
      score delta 0.004409952544391804

doc 59 s4.3's table reproduces to the last digit. M4 (not M1) is correct, as s9 says.

### 5. THEIR SEDIMENT / HYDROLOGY MEDIANS + THE DEGENERATE ROW

stage2_best_station_metrics.csv (21 rows): median kge_log 0.0546120276245786 (== reported),
median kge -0.6116615042541171, median peak_kge -0.707685835442408 (n 20),
median r 0.08705689420035126 (n 20), ratio median 1.4894761031788255, range 0.0-22.64216150017258.
12/21 inside [-0.26, 0.44]; 14/21 above -0.414; 11/21 above 0.

DEGENERATE: station 21217250 sim_mean 0.0, ratio 0.0, pbias -100.0, r NaN, kge_log -2.281251,
n 472 -> excluding it the median moves to 0.05783141598210405, shift +0.0032193883575254503
(doc 59 s3.1 item 2 says "+0.0032" -- correct).

stage1_best_station_metrics.csv (90 rows): median kge_log 0.32933947922532514 == the JSON's
score_kge_log, while the JSON note says "area-sqrt-weighted mean" -> stale note, doc 59 s3.2 right.
The table carries an `area_km2` column; it IS discharge.

calibration_fast 0.36820537350137134 / calibration_fast_b 0.37235713475898685, both
"routing": "linear_reservoir (NOT hydrodynamic)", n_gauges 90 -> doc 59's 0.368 / 0.372 right.

### 6. THEIR SEARCH GEOMETRY

stage2_search_history.csv 500 / 300 rows; trial 0 = (11.8, 0.56, 0.5, 1.0),
score -0.304786553973932 (main) / -0.3397805706657051 (val) -> s2.1 right.
300 common i: max|diff| = 0.0 on alpha, beta, alpha_tc, c_mult; score corr 0.9965067408833312;
133/300 identical scores; best i 263 (main) / 67 (val) -> s4.3's "one seeded sample re-scored" right.
Box positions: 0.86063040139613 / 0.24668037722614733 / 0.6678491588479862 / 0.12936280345827444
and val 0.9209704724874501 / 0.16553172273527816 / 0.28472008233793555 / 0.1536133951920586
-> s2.1's 0.861/0.247/0.668/0.129 and 0.921/0.166/0.285/0.154 all right; no rail.

### 7. THEIR RS TABLE, SPLIT CODE, ENSO EDA, CODE QUOTES

outputs/tables/rs_retrieval_summary.csv -- all 4 rows x 8 columns match doc 59 s7.1 verbatim.

    ssc.py:448  Xtr,Xte,ytr,yte = train_test_split(X, y, test_size=test_size, random_state=seed)

plain row split, no groups; X/y built at :440-441 with site identity dropped; the defending
docstring is at :427-430 -> s7.2's characterisation is exactly right.

outputs/eda/enso_summary.csv -- all 16 cells match s6.4 verbatim (column is `stations`).
viz/observations.py: ENSO_EVENTS at L43-46 (L41-42 are the ONI comment); dates as quoted.
doc 59 s6.3 cites "L41-46" -- two lines early, content correct.
metrics.py L7 "(-0.26 to 0.44)" and L53 "KGE = -0.41, not 0" -> both cited correctly.
musle.py:164/177  qpeak = alpha_tc * qsur * area / (3.6 * tc_h) -> s4.2 right.
musle.py TriggerSet docstring "the **last** matching rule wins" -> s8.3's quote right.
config/magdalena.yaml: alpha 11.8, beta 0.56, p_factor 1.0, gamma clay/silt 1.0 -> right.
scripts/15_build_forcing_v2.py:313  chunk = got if chunk is None else chunk -> s8.4 item 3 right.

### 8. CONTAINMENT, RE-MEASURED INDEPENDENTLY OF M1

    their 21 in our sediment_inventory (79): inter 21, containment 1.000, onlyA []
    their 13 in our 79:                      inter 13, containment 1.000, onlyA []; 13 subset of 21 True
    their 90 in our discharge_daily (192):   inter 90, containment 1.000, onlyA []
    their 21 in our usable-18:               inter 8 (containment 0.381)

The 13 not in our usable-18 are exactly the codes doc 59 s8.5 lists. The headline
21/21, 13/13, 90/90 is CONFIRMED.

### 9. OUR SIDE

docs/55: -0.118 (a) / +0.139 (b), box floor alpha 2.0 beta 0.60, unconstrained 0.48,
est (b) unconstrained ~5.9 inside the box, RAILED/EXPLORATORY -> s2/s3 right.

c5_enso_contrast.json: median_ratio 3.046755091543662, geomean 3.0563436523427323, 18/18,
est_a_median 4.620163547568586, est_b_median 2.948674885718534 -> s6.7's values right,
BUT docs/34's table marks 2.84 (n=4, partial-rating excluded) as the HEADLINE (b);
2.95 is the "(b) rating, all" row (n=7). doc 59 says only "est. (b)".

docs/45: line 84 = the alpha box [2.0, 30.0]; line 302 = F_report median; line 311 = 1-sqrt(2)
= -0.414; s3.2 (line 307) = THE BAR [-0.26, 0.44]; s3.4 = CAL-8 (18 -> 13 -> 13 -> 9 -> 8);
s3.5 = CAL 2012-01-01..2014-12-31; s2.1 = the TWO free parameters; s2.3 = k_dep 0.0 /km FIXED
plus the SDR = 1.0 claim; s4.1 = Momposina NOT EVALUABLE; line 490 = G9 with
66.53 % / 199.29 of 299.54 / 33.47 % / 801.1 km.

    $ grep -n "0.26" docs/45_c4_preregistration.md   -> the bar is NOT at line 84

docs/42: s3.1 at line 78, cond = inf at line 115 (13-station set); line 710 amendment records
composition cond 5,682 with "basin-total form still inf, s3.1 unchanged" -> doc 59 s4.1 faithful.
G9 (lines 576-584) registers 63.9 % / 158.9 of 248.7 Mt/yr / 36.1 % -- NOT 66.53 %.

docs/37: line 542 = adopted/prior ratio 1.2042736; 789 and 1133 = cond inf; 1596 = "(C) LS LEVEL
UNVALIDATED / cited is not validated / fitted is not validated either"; 405 and 847 = 299.539 Mt/yr
-> every one of doc 59's line citations to docs/37 checks out.
docs/43:76 and docs/31:633 = cond inf -> right.

docs/35 s6.1 (line 334 onward) = the alpha band; its HARD STOP row names the upstream suspects as
"(`Qsur`, `K`, `C`, `LS2D`, or the delivery step)" -- FIVE items. doc 59 says "four".

docs/33 s5.1 = the Phase B freeze plus "adopting it needs a further pre-registration" -> right.
docs/26 s7 = "One lever ... the CHIRPS-gauge merge ... is the only untried one" (doc 59 quotes
"the CHIRPS merge is the only remaining lever" -- that exact phrasing is docs/18 line 357,
not docs/26 s7).
docs/18 s15.5 (line 950; quote at 1012) -> right. docs/52 s7 (line 413) forbids reconstructing
a number -> right. docs/23 s13.2 (line 270; embargo sentence at line 301) -> right.
docs/47 O10 at line 862 (inside s7 "What this run could NOT settle") and line 988 (inside s9.3)
-> both citations right, and the O10 text matches doc 59's quotation verbatim.
docs/34: s1.1 windows (365/731/365/213 d), s1.2 RATES-ONLY rule, s1.3 Qs = Q*C*0.0864 plus embargo,
s1.4 estimator (a) plus C1.2 gate, s1.5 estimator (b) plus Duan, s3.4 EL PROFUNDO 15,180 mg/L
2016-06-04 leverage +156.7 % -> every citation right.

docs/15 L24 = "OpenTopography: dataset COP90, S=1.4 N=11.4 W=-77.0 E=-72.3"; L31 = "Re-download
DEM (COP90) and SoilGrids". NEITHER contains the tarball name or `output_hh.tif`.

    $ grep -rn "Corrdinatzs|output_hh" docs/ src/ notebooks/  -> docs/35 lines 65-66 ONLY

Their side: config/data_sources.yaml L11 archive rasters_COP90_Correcte_Corrdinatzs.tar.gz,
L12 member output_hh.tif. So the CLAIM is true; the CITATION in s5.1 is wrong.

docs/57: 46 geocoded / 43 in basin / 44 carry SSC / 0 of 43 with same-code Q (192 stations);
ssc_recovered_coords.csv: 46 rows, in_basin True 43 / False 3, self_paired_q False 46/46;
the 8-row table in s8.5 matches lat/lon/minibacia/n_ssc exactly for all 8 codes.

docs/16 line 452: 2,206 stale vs 2,073.1 (2008-2018) / 2,036.4 (2009-2017) -> right.
manifest.json: basin_mean_P 2073.1, basin_mean_PET 1251.6, areas 257096.93 -> right.
report_h2e.py:223 kc gate 1.662 -> right.

minibacia_soil_params.csv: sha256 6e5940ecdbd06c8b89b09e9134cbe6586933ff9c6971e896feb9e85b19ae38b1,
398,698 B == the input_hashes.txt entry -> BYTE-IDENTICAL CONFIRMED.
yben409_sediment_repo.bundle sha256 adf7a1d1bf21d62057257de14bc8adf0584facfa1e37cfe1f5b7afafb551ca9e,
82,047,044 B -> CONFIRMED.

minibacia_soil_params K: median 0.03055, mean 0.03182408902214022, min 0.019, max 0.0495,
CV 0.22894948854967634 -> s5.3 right.
urh_cp_factors.csv: area-weighted C = 0.013082958380829582; Bare C 0.500 at area_pct 0.196257
-> right. urh_ls2d_variants.csv (32,782 rows): V4_dg area-wt 9.920900112295154,
median 5.09004955 -> right.

precip files:

    686752 / 294 / 0.44179267 / 0      / 6.821824719840642
    795881 / 294 / 0.51833251 / 109129 / 5.886434994678853
    926910 / 294 / 0.58642155 / 240158 / 5.054322177989231

s5.5's table is right. BUT

    6.821824719840642 / 5.054322177989231 = 1.3497012021807004
    6.821825         / 5.054322          = 1.3497013051404323

doc 59 says x1.3496976 -- WRONG in the 6th decimal.
6.821824719840642 * 365.25 = 2491.6714789217945 -> "2,491.67" right.

Arithmetic: 1965/2036.4 gap 3.5061873895109064 %; vs 2073.1 gap 5.214413197626744 %;
0.0101226238 vs their 0.0104 = 2.667 %; 0.0130829583/0.0101226238 = 1.2924473;
0.0080549035/0.0040460557 = 1.9908039; effective C 0.0004947792784860855;
ratio 26.442009334002304; 1/c_mult 20.4588677; alpha/11.8 4.695367547;
(alpha*c_mult)/11.8 0.229502806 -> inverse 4.357245199. All of s5.6 right.

### 10. INDEPENDENT RECOMPUTATION OF THE BRIDGE (s6.4-s6.6), our data, our definitions

18 usable stations; paired = c1_deleted False and ssc_mean_mg_l notna and same-day q_m3s;
Qs = Q*C*0.0864; means over sample days.

P (2011 vs 2015-16), 6 stations: C med 1.86479249436355, Q med 2.1903590454348567,
F med 4.620163547568586 (== docs/34's est_a_median exactly), B med 0.9615895840179741,
F/C med 2.222674091953934, F/C range 1.2800698747089452-2.8431322644507566.

T (2010-06-01..2012-04-30 vs 2015-03-01..2016-05-31), 6 stations: C med 1.9319870850024972,
Q med 2.0826721076653323, F med 4.4858271690743745, B med 1.002192273471404,
F/C med 2.1038576640449866, range 1.1619547508041534-2.4435233268918632.

Per station: 21197010 P C 0.432980 B 1.315351; 24037390 T C 0.998722; 26017060 33 (P) / 16 (T).

POOLED, our data, their T windows: SSC wet n 17,384 / 41 st med 61.0 mean 210.1764841233318;
SSC dry n 4,862 / 32 st med 40.0 mean 109.3377911178082; Q wet n 72,833 / 124 st med 20.0
mean 534.7697354198896; Q dry n 38,083 / 108 st med 9.628 mean 261.63900815618456
-> SSC mean ratio 1.9222675158753932, SSC med 1.525, Q mean 2.0439220404805254,
Q med 2.077274615704196; product of means 3.928965.

POOLED PAIRED: T B 1.4260623620179824; P B 1.9171228120119566, pooled P Q ratio 0.8108790697181472.

EVERY number in doc 59 s6.4, s6.5 and s6.6 reproduces. Agreement vs theirs: 4.33 % / 3.54 % /
3.57 % / 0.95 % / 14.38 % -> "4.3 / 3.5 / 3.6 / 1.0 / 14 %" right.

### 11. THE CHECKED-AND-CLEAN OF s8.3, RE-RUN

    $ grep -ric "trigger" src/mgb_sediment.py src/mgb_transport.py -> 0 and 0
    $ grep -ril "trigger" src/ -> calib_v2.py, dhime_dates.py, nbgen/make_nb16.py, nbgen/make_nb17.py
                                  (plus two .pyc, which doc 59 omits)
    $ sed -n 521p src/mgb_transport.py -> "    k_dep: object = 0.0"

s8.3 is accurate as printed.

### 12. TALLY

About 218 distinct figures / verbatim quotations / cross-references checked. 211 clean.
7 wrong or mis-located (see the structured findings). No fabricated number was found and no
number was quoted from a file that does not contain it. The defects are (i) one arithmetic slip
in the 6th decimal, (ii) four wrong or stale locators, (iii) one internal 20-vs-23 contradiction,
(iv) one overstated claim about what is unreadable on this disk.

Nothing was written outside this journal. No git command in either repo. No fit, no engine
default touched, no alpha-hat produced. No t/km2/yr anywhere.
