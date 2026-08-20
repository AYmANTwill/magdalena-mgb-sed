# journal_x59-bridge — M2: can their concentration contrast bridge to our flux contrast?

Agent slug: x59-bridge. READ-ONLY except this file. No git, ever.
Task: establish what is arithmetically valid in bridging their pooled SSC/Q marginal ratios
to our modelled/observed flux contrast, and measure the concentration->flux bridge factor
in OUR basin on OUR paired data.

## 00 — start
Journal created as first action. Appending as I go.

## 01 — THEIR windows: the label "2010-12" resolved, no guessing needed
Found the generator, so the ambiguity the task flagged is settled by code, not by reading.

`friend_repo/src/mgbsed/viz/observations.py:41-46`
```
# ENSO phases. Oceanic Nino Index thresholds sustained over 5 overlapping
# seasons; dates are the conventional event windows for these two events.
ENSO_EVENTS = {
    "La Nina 2010-12": ("2010-06-01", "2012-04-30"),
    "El Nino 2015-16": ("2015-03-01", "2016-05-31"),
}
```
`friend_repo/scripts/11_plot_observations.py:135-147` selects `date >= a & date <= b` (inclusive
both ends), then reports n / median / mean / p90 / nunique(station) over the POOLED station-days.
=> La Nina = 2010-06-01..2012-04-30 (699 d inclusive); El Nino = 2015-03-01..2016-05-31 (458 d).
NOT calendar 2010-2012. My earlier reading (and the orchestrator's) would have been wrong.

## 02 — their raw data is absent: CONFIRMED by listing
`ls -a` in their clone: .git .gitignore README.md config environment.yml outputs pyproject.toml
scripts src tests. Tested each gitignored data root explicitly:
  ABSENT: data / data_Final / data_chirps / "data precip"
Their .gitignore documents 15 GB in data/ + 7.5 GB in data_Final/ obtained from a shared drive.
=> A paired per-station recomputation ON THEIR DATA IS IMPOSSIBLE from this clone. Full stop.

## 03 — their enso_summary.csv verbatim (re-verified, full precision)
variable,phase,n,median,mean,p90,stations
SSC (mg/L),La Nina 2010-12,14722,48.0,213.35545442195354,607.0,35
SSC (mg/L),El Nino 2015-16,4139,36.0,106.1816597825161,204.0,27
Q (m3/s),La Nina 2010-12,65065,21.2,589.2964713876403,1582.0,108
Q (m3/s),El Nino 2015-16,32666,10.57,298.51300188766006? -> 298.51300188766403 (see file), 93
(exact string from file: 298.51300188766403 -- transcribe from file, not from memory)

## 04 — my reimplementation of docs/34 estimator (a) REPRODUCES the registered numbers
Script: scratchpad/x59/bridge.py (read-only on data/processed; writes only to scratchpad).
Definitions used, taken from docs/34 §1.3-§1.4: paired sample days = c1_deleted==False AND
ssc_mean_mg_l notna AND same-day q_m3s at the same code; Qs = Q*C*0.0864; statistic = arithmetic
mean over sample days (a RATE, t/day, per §1.2).
Station set = the 18 with ssc_class in {usable, usable-with-caveat} (verified from
sediment_inventory_qc.csv: 6 usable + 12 usable-with-caveat + 61 excluded = 79).
flag_flow_selective within the 18: only 26127010 (matches docs/34 §2 note).

P-pair (2011 vs 2015-2016) mean flux ratio, mine vs docs/34 §3.2 PRIMARY (a):
  21197010  1.211804  vs 1.21  OK
  22017010  1.701723  vs 1.70  OK
  22017030  9.678658  vs 9.68  OK
  23127010 11.680023  vs 11.68 OK
  24037390  2.451295  vs 2.45  OK
  26017060  6.789032  vs 6.79  OK
6/6 exact to the printed precision => the pipeline under this measurement is the registered one.

## 05 — the exact algebra (this is the answer to task item 1)
E[CQ] = E[C]E[Q] + Cov(C,Q).  Define rho = Cov(C,Q)/(E[C]E[Q]) = corr(C,Q)*CV_C*CV_Q.
Then  E[CQ] = E[C]E[Q]*(1+rho), so

  F_ratio = mean(CQ)_wet / mean(CQ)_dry
          = [C_ratio * Q_ratio] * (1+rho_wet)/(1+rho_dry)

=> BRIDGE FACTOR B = (1+rho_wet)/(1+rho_dry). The product of marginals equals the flux ratio
iff rho_wet == rho_dry. C and Q being positively correlated in BOTH windows makes both
numerator and denominator > 1, so THE SIGN OF THE BIAS IS NOT DETERMINABLE from marginals:
it depends on which window has the larger normalised covariance, which pooled marginals do not
contain. I therefore assert NO bound; I measure B instead.

## 06 - MEASURED bridge factor B, our basin, our paired data (task item 3)
per-station table: scratchpad/x59/per_station.csv. Stations = the 18 usable/usable-with-caveat.
Only stations with >=1 paired day in BOTH windows can carry a ratio.

PRIMARY pair P (2011 vs 2015-2016), 6 stations:
 code      n_w/n_d  C_ratio   Q_ratio   product   F_ratio    B=F/product  rho_wet   rho_dry
 21197010  192/202  0.432980  2.127763   0.921278  1.211804  1.315351     0.249350 -0.051419
 22017010  184/174  1.329398  1.117509   1.485614  1.701723  1.145467     0.096678 -0.043301
 22017030  236/210  5.772965  1.702623   9.829182  9.678658  0.984686     0.074718  0.091546
 23127010  301/316  4.460815  2.895105  12.914527 11.680023  0.904410     0.444463  0.597392
 24037390  319/309  1.341714  2.252955   3.022821  2.451295  0.810929     0.326485  0.636557
 26017060  201/33   2.387871  3.029465   7.233971  6.789032  0.938493    -0.011652  0.054846
 MEDIANS   C 1.864792 | Q 2.190359 | product 5.128396 | F 4.620164 | B 0.961590 (geomean 1.003499)
 (F median 4.620164 == docs/34 registered 4.62; B range 0.810929-1.315351)
 excl 21197010 (single-point dominated, docs/34 sec 1.6): C 2.387871, Q 2.252955,
 product 7.233971, F 6.789032 (== docs/34's 6.79), B median 0.938493.

THEIR windows T (2010-06-01..2012-04-30 vs 2015-03-01..2016-05-31), 6 stations:
 MEDIANS   C 1.931987 | Q 2.082672 | product 4.486182 | F 4.485827 | B 1.002192 (geomean 0.998922)
 B range 0.846851-1.205462.
SENSITIVITY pair S: MEDIANS C 2.557716 Q 2.507720 product 7.596180 F 9.320415 B 1.165177
 (B range 0.959011-1.511812); F median 9.320415 == docs/34's 9.32.
The ALTERNATIVE reading T2 (calendar 2010-2012 vs 2015-2016): MEDIANS C 1.771662 Q 1.655937
 product 3.981752 F 3.766024 B 1.082514. Reported because the task asked both readings tested;
 T is the one their code actually uses.

=> THE COVARIANCE TERM IS SMALL. Within a station, on paired days, C_ratio x Q_ratio recovers the
flux ratio to a median of 4 % (P), 0.2 % (T), and never worse than a factor 1.51 at any station in
any pair. Its SIGN IS NOT FIXED: B < 1 at 4 of 6 stations in P, > 1 at 4 of 6 in T. So the
orchestrator's multiplication step is not where the error bites, and I say so.

## 07 - SHARED station subset (my own computation; M1's journal was still empty)
Their 21 sediment-calibration codes (outputs/calibration/stage2_best_station_metrics.csv,
"station" column, zero-padded to 10 digits, int-normalised) vs our docs/34 18:
 SHARED (8): 22017010 22017030 22057090 23127010 24037390 26017060 26127010 26137110
 theirs-only (13): 21187030 21217250 22027010 24017830 24037030 24037040 24037130 26177030
                   28037090 29067010 29067050 29067120 29067130
 ours-only (10): 21147030 21197010 21237020 23087210 24027030 26017020 26107130 26167060
                 26167070 26207080
Of the 8 shared, 5 carry a paired both-window ratio (22057090 discharge ends 2009-03-19;
26127010 has 0 paired 2011 days and is C1.2 flow-selective; 26137110 has no El Nino SSC).
SHARED-SUBSET medians, P: C 2.387871 Q 2.252955 product 7.233971 F 6.789032 B 0.938493 (n=5)
SHARED-SUBSET medians, T: C 2.139147 Q 1.886731 product 4.874287 F 4.756998 B 0.975937 (n=5)
Note: their enso_summary pools 35/27 SSC stations and 108/93 Q stations, i.e. NOT this subset,
so the shared subset does not make the two numbers commensurate on its own.

## 08 - where the error actually bites: THE POOLING, not the covariance
Applied THEIR estimator (pool all station-days, SSC and Q independently) to OUR data.
On THEIR windows T: SSC n 17,384/41 st (wet) vs 4,862/32 st (dry), median 61.0/40.0,
mean 210.176484/109.337791; Q n 72,833/124 st vs 38,083/108 st, median 20.00/9.628,
mean 534.769735/261.639008.
  ours pooled: SSC mean ratio 1.922268, SSC median ratio 1.525000,
               Q mean ratio 2.043922, Q median ratio 2.077275,
               product of means 3.928965, product of medians 3.167844
  theirs:      SSC mean ratio 2.009344, SSC median ratio 1.333333,
               Q mean ratio 1.974107, Q median ratio 2.005676,
               product of means 3.966659, product of medians 2.674235
=> their pooled marginals REPRODUCE on our independently QC'd copy of the same IDEAM network:
   SSC mean ratio agrees to 4.3 %, Q mean ratio to 3.5 %, Q median ratio to 3.6 %.
   (SSC median ratio is the outlier: 1.333 vs 1.525, 14 %.)
   THIS IS A POINT IN THEIR FAVOUR AND I RECORD IT AS SUCH.

But the pooled *flux* ratio on our data is NOT the product of those pooled marginals:
  pooled paired, all stations, P:  C 1.899602  Q 0.810879  product 1.540347  F 2.953035  B 1.917123
  pooled paired, all stations, T:  C 1.480113  Q 1.074398  product 1.590231  F 2.267768  B 1.426062
  pooled paired, fixed both-window station set (6 st), P: product 4.445022 F 4.126660 B 0.928378
  pooled paired, fixed both-window station set (6 st), T: product 2.436769 F 2.329697 B 0.956060
Pooling moves B from ~0.96 (composition held fixed) to 1.43-1.92 (composition free) - an effect
5-20x larger than the within-station covariance term. Note also Q_ratio flips BELOW 1 (0.811 in P)
once the pooled sample is allowed to change composition: the dry window simply contains more
station-days at the big gauges. That is the real defect in the product-of-marginals argument.

## 09 - the paired restriction is NOT a confound (control)
Per-station C_ratio computed on ALL QC'd SSC days vs on paired days only: identical at 4 of 6
stations in P and 4 of 6 in T; largest deviation 24037390 on T (0.944448 all vs 0.998722 paired,
5.7 %) and 26017060 P (2.345308 vs 2.387871, 1.8 %). So restricting to paired days does not
manufacture the bridge factor.

## 10 - the only defensible transfer
F/C measured per station (this IS the concentration->flux bridge, and it is essentially the Q ratio):
  P: median 2.222674, range 1.280070-2.843132 (n 6)
  T: median 2.103858, range 1.161955-2.443523 (n 6)
Their pooled SSC MEAN ratio 2.009343749748812 x our F/C(T) median 2.103858 = 4.227373
   (range across our stations 2.334767 - 4.909878)
Their pooled SSC MEDIAN ratio 1.3333333333333333 x our F/C(T) median 2.103858 = 2.805144
   (range 1.549273 - 3.258031)
On our P windows instead: 2.009344 x 2.222674 = 4.466116 ; 1.333333 x 2.222674 = 2.963565.
This is legitimate arithmetic but it is THEIR C times OUR Q: it is not independent corroboration.

## 11 - what their repo does and does not contain on ENSO
outputs/calibration/stage2_sediment_params.json + calibration_val: window ["2013-01-01",
"2014-12-31"], notes.held_out = "2011 (La Nina) and 2015-2017 (El Nino) were not used."
grep -ril for nino/nina/enso over outputs -> only the two params json, eda/enso_summary.csv, and
two rs_retrieval files. THERE IS NO MODELLED ENSO CONTRAST IN THEIR OUTPUTS. Their ENSO material
is observational EDA. So the correct pairing is their enso_summary vs our docs/34 (observation vs
observation), NOT their model vs our docs/56. Also: their held-out dry span is 2015-2017, wider
than both their own EDA window (2015-03..2016-05) and ours (2015-2016).

## 12 - our C5 anchor re-verified
data/processed/c5_enso_contrast.json: modelled median_ratio = 3.046755091543662, n_stations 18,
windows P-LN 2011 / P-EN 2015-2016; observed_docs34 est_a_median 4.620163547568586,
est_b_median 2.948674885718534. Per-station obs_a matches my recomputation exactly
(23127010 11.68002291274528; 24037390 2.451294657881718).

## 13 - VERDICT
- Task item 1 (the error): stated and derived. B = (1+rho_wet)/(1+rho_dry); sign NOT determinable
  from marginals; measured B ~ 1 within a station, 1.43-1.92 once pooling is allowed to move.
- Task item 2: their raw data absent - confirmed by listing. Paired recomputation on their data
  is impossible.
- Task items 3-4: their pooled marginals are individually REPRODUCIBLE on our data; their PRODUCT
  is NOT COMPARABLE to our flux contrast, because the two marginals come from different station
  sets (35/27 vs 108/93) and pooled composition change dominates. Grade: CONSISTENT (marginals,
  separately, to 3.5-4.3 % on the means) / NOT COMPARABLE (the product, as a flux contrast).
- No tolerance invented. No band introduced. No pass/fail asserted.

## 14 - why their station set is larger, and it is NOT a quality failure on their part
Checked all 13 theirs-only sediment-calibration codes against our files:
all 13 EXIST in our sediment_daily_qc.csv; 6 of 13 also exist in our discharge_daily.csv
(21217250, 29067010, 29067050, 29067120, 29067130 - and 21217250; the other 7 have no discharge
record in our copy at all). All 13 are ssc_class == "excluded" in our C1 gate. Reasons:
  - 9 of 13 "no coordinates: lat/lon absent in sediment_inventory.csv" (21187030, 22027010,
    24017830, 24037030, 24037040, 24037130, 26177030, 28037090 ... ) -> an OUR-SIDE metadata gap,
    not a data-quality finding about the station.
  - 4 of 13 "outside the modelled domain" - 29067010 EL TREBOL (10.636, -74.146),
    29067050 CANAL FLORIDA (10.756, -74.086), 29067120 FUNDACION (10.525, -74.183),
    29067130 PUENTE FERROCARRIL (10.586, -74.192): lower-Magdalena / Cienaga Grande gauges that
    fall on no minibacia of our delineation.
  - only 1 of 13 excluded on data grounds: 21217250 BOCATOMA, "single-window coverage
    (La Nina 344, El Nino 0 vs N=91) ; flow-selective".
=> the 18-vs-21 difference is overwhelmingly a DOMAIN + GEOLOCATION difference, not them being
laxer than us. Their set is not contaminated; it is a different (partly wider) domain. Say so.
