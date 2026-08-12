# Run journal — H-B (OROGRAPHIC) test of the CHIRPS-merge volume surplus

Agent: `chirps-orographic`. One agent of a multi-agent diagnosis of why the CHIRPS-gauge merged
rainfall field fails its pre-registered VOLUME gate (+7.5 %) while passing its LOOCV gate.
Started 2026-08-12.

## What I was asked

Test **H-B: OROGRAPHIC** — "the gauge-only field is too DRY in the headwaters and the merge is
(partly) RIGHT." `notebooks/11_rainfall_pet_forcing.ipynb` records as a known limitation that
plain IDW ignores elevation, so headwater rainfall is interpolated from valley stations with no
lapse adjustment. If CHIRPS carries orographic enhancement the gauge field structurally cannot,
the +7.5 % is partly real signal rather than bias.

Five required measurements: (1) is the gauge network elevation-biased, against the AREA-weighted
basin elevation distribution; (2) where is the +152.148 mm/yr surplus in elevation, mm/yr and
specific, cross-tabbed against `d_nearest_km`; (3) does CHIRPS actually show orographic
enhancement in THIS basin — at cells and at gauges; (4) characterise the w→1 area (high, or
merely remote?); (5) state the honest limit.

Return value: the distributions, the surplus decomposition, the gradients, the observed-gauge
profile, the w=1 characterisation, and a verdict.

## Constraints I am operating under

* No rebuild of the 4018 x 8672 field (RAM ~2 GB). All work on the harvested ledger in the
  scratchpad `.../7fba197a-689b-47d5-9c29-1dc3e3af2581/scratchpad`.
* No `git add/commit/push`; no edits to docs/18, docs/30, docs/33, docs/54; no engine defaults.
* Scratch scripts live in the scratchpad, not the repo.
* MEASURE BEFORE ASSERTING. An uncited band cannot pass or fail a gate. A negative result is
  publishable. Verify from executed output, never an exit code.

## Sources read before measuring

* `C:\Users\...\scratchpad\h1_elev.py` — confirms `elev_mb` is DEM-derived per minibacia
  (`m.minibacia_elevation(cent, demc)` on the coarsened DEM), `elev_g` is the DEM sampled at the
  gauge lat/lon with a fallback to the inventory `alt` column where the DEM sample is non-finite
  ("gauge elevation: N filled from inventory alt" is printed). **Consequence for me:** gauge
  elevation and cell elevation come from the SAME DEM, so a gauge-vs-cell elevation comparison is
  not confounded by two different elevation sources — except for the inventory-alt fallbacks. I
  must count those.
* `h2_harvest.py` — confirms the ledger column definitions I rely on: `band =
  np.digitize(elev, m.ELEV_BANDS)`; `w = m.chirps_weight(d_near)`; subsets A/B/D; the
  per-cell identity `sMerged - sP == w*(sCmapA - sPA) + (sCmapB - sPB)`; `sCraw_all` is
  `np.nansum` of RAW CHIRPS over the window and `sP` the full-window gauge-IDW sum, so both are
  all-days sums and directly comparable per cell. Gauge-side `mean_g / mean_c_raw / mean_c_map`
  are means over that gauge's own paired station-days (so each gauge has its OWN day sample —
  cross-gauge comparison of these means is NOT a common-day comparison; noted as a caveat).
* `docs/18` §15.1–§15.5 (read-only) — the two gates, the LOOCV isolation-band table
  (>30 km: gauge-only r 0.343 vs merged 0.300), and §15.5's correction of §15.3.
* `notebooks/11_rainfall_pet_forcing.ipynb` cell 23 — the actual wording of the "No orographic
  correction" limitation, and its 2026-08-12 STALE annotation which already records that the
  ">30 km CHIRPS gap-fill" case was tested and did not hold.

## Discrepancy noticed in the material handed to me (not my hypothesis, recorded for the synthesis agent)

`bounds_fields.csv` labels F5/F6 as "credited **0.414** x own reporting mean"; my brief describes
the same rows as "credited **0.4527** x own REPORTING-day mean". The mm/yr values match the brief
exactly (F5 2267.409 / 2290.932, F6 2527.237 / 2541.149), so only the LABEL differs, but the two
numbers cannot both describe the same run. I do not use F5/F6 in any H-B claim. Flagging it
because H-A owns those rows.

## Log

### L1 — self-checks (`hb1_checks_and_elev.py`, executed)

I re-derived every handed number before using the ledger. Executed output:

```
gauge-only P     2036.3927   handed   2036.393
RAW CHIRPS       2124.7205   handed   2124.721
MAPPED CHIRPS    2265.7574   handed   2265.757
merged           2188.5404   handed   2188.540
total surplus (identity)    152.1477   handed  152.148
max |contrib - (sM-sP)|   1.2378e-03 mm
channel MAP INFL blend  w*(Cmap-Craw):  +87.3022
channel CHIRPS-IDW blend w*(Craw-P) :  +64.8070
channel MAP INFL fallback (Cmap-Craw):   +0.0086
channel CHIRPS-IDW fallb  (Craw-P)  :   +0.0298
wband w=0         n= 2213 area%= 25.8  surplus   +0.0031  specific   +0.0119
wband blend 0<w<1 n= 4963 area%= 57.1  surplus  +54.2001  specific  +94.9739
wband w=1         n= 1496 area%= 17.1  surplus  +97.9445  specific +573.1761
fallback cell-days 35,716 of 28,504,864 = 0.125 %   CHIRPS-missing cell-days 0
```

All reproduce to <=5e-4 mm/yr. **One handed number needed a definition check** and I ran the
four candidate definitions (`hb2_surplus_elev.py` part (a)):

```
d1 = (Cmap-P) over A+B days, ALL cells   mean_d  +229.365  mw*md  +92.598  cov  +59.549
d2 = same but zeroed where w==0          mean_d  +204.704  mw*md  +82.642  cov  +69.505
d3 = (Cmap-P) on A days only, ALL cells  mean_d  +229.326  mw*md  +92.583  cov  +59.565
handed: mean_d +229.381, mw*md +92.605, cov +59.528
```

So the handed `cov_area(w,d) = +59.528` uses **d over ALL 8,672 cells** (d1/d4), not d restricted
to blend cells, and my d1 agrees to **+0.021 mm/yr (0.04 % of the covariance term)** — within
float32/ordering noise, not a disagreement. Recording it because my first (natural) reading, d2,
gives +69.505 and would have looked like a contradiction. **Definition matters here: state it.**

### L2 — M1 gauge vs basin elevation (`hb1_checks_and_elev.py`, executed)

`elev_m` for gauges and for cells both come from the same COP90 DEM (`h1_elev.py`), so the
comparison is not confounded by two elevation sources. 0 NaN on both sides.

```
decile |  gauge elev (count-wt) | basin elev (AREA-wt) | basin elev (count-wt, the TRAP)
    0% |            0.4 m |            6.2 m |            6.2 m
   30% |          375.9 m |          237.5 m |          213.7 m
   50% |         1079.0 m |          955.1 m |          898.6 m
   80% |         2393.4 m |         2154.5 m |         2100.8 m
   90% |         2756.0 m |         2741.2 m |         2697.5 m
  100% |         3980.9 m |         4491.1 m |         4491.1 m
  MEAN |         1248.8 m |         1144.6 m |         1114.3 m

band          n_gauge   gauge%   n_cell    area_km2   area%  gauges/1000km2
<500 m             98    33.7%     3427      98,992   38.5%           0.990
500-1500 m         84    28.9%     2442      72,123   28.1%           1.165
1500-2500 m        55    18.9%     1628      49,243   19.2%           1.117
>2500 m            54    18.6%     1175      36,738   14.3%           1.470
```

**The network is elevation-biased UPWARD, not downward.** Mean gauge elevation 1,248.8 m exceeds
the area-weighted basin mean 1,144.6 m; the gauge deciles sit above the area-weighted basin
deciles from the 30th to the 80th percentile; and gauge density per 1,000 km² is *highest* in the
`>2500 m` band (1.470) and *lowest* in the `<500 m` band (0.990). H-B's premise — headwaters
interpolated from valley gauges — is not true basin-wide. Only the very top is unsampled: the
highest gauge is 3,980.9 m and only **0.25 % of basin area** lies above it.

The one place the premise survives is **zone-local**: area above the highest gauge *in its own
hydrographic zone* is 18,413 km² = **7.16 %** of the basin, concentrated in the LOWLAND-gauged
zones — Cesar 30.3 % (17 gauges, highest 505.9 m, cells to 4,491.1 m — Sierra Nevada / Perijá),
Saldaña 29.3 %, Bajo Magdalena 20.3 %, Bajo Mag-Cauca-San Jorge 16.0 %. I test that pocket
separately below rather than asserting it either way.

### L3 — M2 surplus by elevation (`hb2_surplus_elev.py`, executed)

```
band             n  area%  surplus mm/yr  % of tot  SPECIFIC mm/yr  aw mean w  aw d_near km
<500 m        3427  38.5%        +67.452     44.3%        +175.183      0.476         20.94
500-1500 m    2442  28.1%        +54.629     35.9%        +194.733      0.410         20.04
1500-2500 m   1628  19.2%        +26.374     17.3%        +137.699      0.319         15.82
>2500 m       1175  14.3%         +3.693      2.4%         +25.842      0.310         15.42
```

Equal-area elevation deciles: specific surplus peaks at **D4 (238-554 m, +395.4)** and falls to
**D9 +53.6 / D10 (2,741-4,491 m) +45.6**; D1 (6-51 m) is **negative, -23.9**. So the surplus is a
LOWLAND/foothill phenomenon, not a headwater one — the opposite sign to H-B's prediction.

Confounding, measured: **area-weighted corr(elev_m, d_nearest_km) = -0.1757** (and
corr(elev_m, w_chirps) = -0.1688) — high ground is *slightly closer* to gauges, so the confound
runs AGAINST H-B rather than hiding it. The 2-D specific table separates them: across a row
(fixed band, rising distance) the specific surplus spans +0.1 -> +542 (three orders of magnitude);
down a column (fixed distance, rising elevation) it spans about 2x and is **non-monotonic**,
collapsing at `>2500 m` (10-20 km: +36.8/+47.0/+58.8/+2.5; 20-30 km: +190.3/+285.6/+260.8/-0.9).
Distance explains the surplus; elevation does not.

### L4 — M3 the load-bearing test (`hb3_gradients.py`, executed)

```
gauge-IDW  P    slope   -224.18  aw r -0.324  basin aw mean   2036.4
RAW CHIRPS      slope   -209.35  aw r -0.274  basin aw mean   2124.7
MAPPED CHIRPS   slope   -269.24  aw r -0.253  basin aw mean   2265.8
difference: raw +14.83, mapped -45.07 mm/yr per 1,000 m
```

Rainfall in this basin **decreases** with elevation in every field. RAW CHIRPS's gradient is only
+14.8 mm/yr/1,000 m more positive than the IDW's, and the field that is actually merged
(**MAPPED** CHIRPS) is **-45.1 STEEPER downward** than the gauge field it displaces.

At the gauges — the only place with truth — observed rainfall regressed on elevation is
**-223.5 mm/yr per 1,000 m (r -0.265, n=291)**; band means 2021.1 / 1966.3 / 2057.7 / 1216.4 mm/yr
for `<500 / 500-1500 / 1500-2500 / >2500 m`: flat to 2,500 m, then a collapse at the crest. The
"Andes wetter at mid-elevation and drier at the crest" caution in my brief is **confirmed by
measurement**, so there is no monotonic enhancement for IDW to be missing.

Like-for-like (same paired days within each gauge): `C_raw - g` slope on elevation
**+16.9 mm/yr/1,000 m, r +0.036**; `C_map - g` slope **-25.1, r -0.049** — i.e. CHIRPS's bias
against the gauges has **no elevation dependence at all**. At 1,500-2,500 m CHIRPS is *drier*
than the gauges by -163.7 mm/yr mean.

Quantile-map tail scale (gk[-1]/ck[-1]) area-weighted by band: `<500 m` **1.913**,
`500-1500 m` 1.317, `1500-2500 m` 1.640, `>2500 m` **1.053**. The map's stretch — which carries
57.4 % of the whole surplus — is **weakest exactly where H-B needs it strongest**.

Within-zone gradients: only **3 of 9** zones have slope(Craw) > slope(P) — Alto Magdalena +17.5,
Saldaña +97.4, and **Cesar +349.1** (the zone whose 17 gauges all sit below 506 m). Cesar is the
one H-B-consistent signature in the data and I size it in L5 rather than dismissing it.

### L5 — M4 the w=1 area, and the size of the one H-B-consistent pocket (`hb4_w1_and_pocket.py`, executed)

```
w=1 AREA: 1496 cells, 43,933 km2 = 17.1 % of basin, surplus +97.944 mm/yr (64.4 % of 152.148)
  AREA-weighted mean elevation   816.3 m   vs whole basin 1,144.6 m   (-328.4 m)
band          w=1 area km2  w=1 area%  basin area%  surplus mm/yr  % of w=1 surp  SPECIFIC
<500 m              21,241      48.3%        38.5%        +44.861          45.8%    +543.0
500-1500 m          15,309      34.8%        28.1%        +37.248          38.0%    +625.5
1500-2500 m          4,518      10.3%        19.2%        +12.271          12.5%    +698.2
>2500 m              2,865       6.5%        14.3%         +3.565           3.6%    +319.9
  area-weighted mean d_nearest in w=1: 40.47 km (basin 18.92 km); min 30.02, max 71.48
```

**The w=1 terrain is REMOTE, not HIGH.** It is 328 m *lower* than the basin on area-weighted mean;
48.3 % of it lies below 500 m and only 6.5 % above 2,500 m (against 14.3 % basin-wide). Zones, by
share of the w=1 area: **Medio Magdalena 40.0 %** (area-weighted elevation 462.8 m — valley floor),
Cauca 16.8 % (1,462 m), Nechí 10.1 % (864 m), Bajo Magdalena 8.8 % (62.1 m — Mompós floodplain,
and its w=1 surplus is **negative, -6.11 mm/yr**), Cesar 8.6 % (1,100 m), Bajo Mag-Cauca-San Jorge
5.9 % (624 m). Surplus by zone over the whole basin: Medio Magdalena +69.96 (46.0 %), Cauca +46.98
(30.9 %), Cesar +16.95 (11.1 %), Bajo Magdalena **-7.41**.

It IS wet: area-weighted gauge-only P inside w=1 is **2,483.2 mm/yr** against the basin 2,036.4,
and the surplus there is **+573.2 mm/yr = +23.08 % of the local gauge-only mean**. So the surviving
half of `docs/18` §15.3 — "concentrated in the sparsely gauged (wet, high) terrain where w -> 1" —
is **half right and half wrong**: *sparsely gauged* and *wet* check out; **HIGH does not.**

The H-B pocket, sized: cells above their own zone's highest gauge = 589 cells, 18,413 km²,
**7.16 %** of basin, surplus **+25.376 mm/yr = 16.68 %** of the total, at area-weighted elevation
1,511 m. By zone it is **Cesar +16.769** (7,381 km², aw elev 1,364 m) and **Bajo Mag-Cauca-San
Jorge +9.049** (3,108 km², aw elev **604 m**) — lowland-gauged zones flanking a massif, not
headwaters. The genuinely high pockets give almost nothing: Saldaña +2.270 (3,106 m), Sogamoso
+0.185 (3,802 m), Alto Magdalena +0.304 (3,884 m), Cauca **-0.003** (4,115 m), Nechí **-1.181**.

Upper bounds on any orographic reading:

| definition | area | surplus creditable | % of +152.148 |
|---|---|---|---|
| above own-zone highest gauge AND RAW CHIRPS wetter than IDW | 10,708 km² (4.16 %) | **+28.208** | 18.54 % |
| — of which the RAW-CHIRPS channel only (not map-created) | " | +16.018 | 10.53 % |
| generous: any cell >1,500 m AND RAW CHIRPS wetter than IDW | 51,511 km² (20.04 %) | **+37.729** | 24.80 % |

The gate needs the surplus down to **<= +20.4 mm/yr** (ceiling 2,056.8 on 2,036.4). Crediting the
generous bound in full leaves +114.4 (2,150.8 = +5.62 %) — **still fails by 5.6x**.

### L6 — M5 the honest limit, tested rather than asserted (`hb5_honest_limit.py`, `hb6_robust.py`, executed)

No gauge lies inside a w=1 cell **by construction** (w=1 requires >=30 km to the nearest gauge;
`min d_nearest over w=1 cells = 30.02 km`). But 20 of the 291 gauges sit >=30 km from their nearest
neighbour, so the LOOCV rebuilds a w=1 estimate AT those 20 points. That is the only observational
test of the w=1 field that exists, and it is not silent.

First I validated my read of `data/processed/merge_loocv_report_v2.csv` (read-only) against
`docs/18` §15.2/§15.5 — it reproduces them exactly:

```
band                n  med r_base  med r_merged  med d_bias pts  med bias_base%  med bias_merged%
<10 km  w=0        98       0.481         0.475           +0.00           +3.62             +2.98
10-30 km blend    169       0.426         0.449           +0.24           +0.29             +1.29
>=30 km w=1        20       0.343         0.300           +0.89           +3.86             +6.56
fleet median r_base 0.429, r_merged 0.447; improved 149 worsened 51 unchanged 87
```

(docs/18 quotes 0.481/0.475, 0.426/0.449, 0.343/0.300, +0.00/+0.24/+0.89, 0.429->0.447, 149/51/87.)

**H-B predicts the gauge-only field is biased LOW at these isolated points. It is biased HIGH.**
Median `bias_base_pct` = **+3.86 %**, mean +6.46 %, negative at only **8 of 20** (binomial p=0.25
against 50/50 — i.e. no evidence of a dry bias at all). And at the **5** w=1 gauges above 1,500 m
the gauge-only bias is `+73.4, +17.2, +108.5, +15.5, +33.8 %` — **positive at 5 of 5**
(p = 1/32 = 0.031) — and the merge **dries 4 of those 5** (median delta -28.6 pts).

What I will NOT claim from these 20: `bias_base_pct` regressed on elevation gives Pearson
r +0.522 (p=0.018) but Spearman rho +0.371 (**p=0.107**), and `dbias` gives Pearson -0.403
(p=0.078) / Spearman -0.268 (p=0.254). So "the gauge-only field is *increasingly* wet-biased with
elevation" is **outlier-driven and not robust at n=20** — I report the level (5/5 positive) and
refuse the slope.

### L7 — the confound separated properly (`hb6_robust.py`, executed)

```
gate window: slope of per-cell surplus on ELEVATION -38.31 mm/yr per 1,000 m (aw r -0.072)
             slope of per-cell surplus on DISTANCE  +15.71 mm/yr per km      (aw r +0.351)
d bin km      n  area%  mean surplus  slope on elev    aw r       elev rng
0-10       2213  25.8%          +0.0           +0.1  +0.028        13-4267
10-20      3223  36.9%         +38.8           -6.0  -0.038        12-4355
20-30      1740  20.2%        +197.9          -29.2  -0.051         6-3903
30-50      1281  14.6%        +580.8           +8.7  +0.009        17-4491
>=50        215   2.5%        +529.1         +263.4  +0.087        57-1958
```

At FIXED distance the elevation slope is **~0 or negative** in the three bins holding 83 % of the
basin area; only the `>=50 km` bin (2.5 % of area, n=215, elevation range only 57-1,958 m, aw
r +0.087) shows a positive slope, and it is too small and too weakly correlated to carry a verdict.
ACROSS bins the mean surplus runs +0.0 -> +38.8 -> +197.9 -> +580.8: **distance is the variable
that explains the surplus.** Same on the 2008-2018 window (elevation -37.07, distance +15.35), and
the band decomposition repeats there too (`<500 m` 43.9 % / `>2500 m` 1.9 % of +146.124), with
merged reproducing the handed 2219.1786 to 2219.179.

## What I refused to claim, and why

1. **That the Cesar / Bajo Mag-Cauca-San Jorge pocket is a real orographic correction.** It is the
   one H-B-shaped signal in the data (Cesar within-zone slope(Craw) - slope(P) = +349.1 mm/yr per
   1,000 m; 7,381 km² above its highest gauge at 505.9 m). But there is **no gauge above 506 m in
   Cesar to test it**, and `docs/18` §15.2 measured pure mapped CHIRPS *worse* than long-range IDW
   even beyond 30 km (r 0.300 vs 0.343, n=20) — so CHIRPS's own point skill is not a warrant. I
   **bound** the pocket (<=+28.2 mm/yr defensible, <=+37.7 generous) and decline to credit it.
2. **The elevation slope of gauge-only bias at the 20 w=1 gauges** — Pearson significant, Spearman
   not (L6). I report the level, not the slope.
3. **F5/F6 of `bounds_fields.csv`** — my brief itself says they double-count the selectivity the
   repair removes, and their label disagrees with the brief on the credit factor (0.414 vs 0.4527).
   Unused here.
4. **Any statement that the merged field in the w=1 area is WRONG.** It is untestable there. My
   finding is only that H-B supplies no support for it being right, and that the one place it can
   be tested contradicts H-B.
5. **A t/km²-style specific-yield framing of "specific surplus".** I report mm/yr per unit area
   inside a subset, which is a rainfall rate; catchment areas are known unreliable per gauge
   (`docs/23` §13.2) but the minibacia `area_km2` used here is the same weight the gate itself
   uses, so the comparison is internally consistent with the gate.

## Could not settle

* Whether the **Cesar high-terrain field** (Sierra Nevada de Santa Marta / Serranía del Perijá,
  7,381 km², up to 4,491 m, highest gauge 505.9 m) is genuinely wetter than the IDW says. No
  observation exists inside it. Settling it needs a gauge, a different satellite product with
  measured point skill in this basin, or a discharge-side constraint on that sub-basin — none of
  which is in the ledger I was given.
* Whether the **`>=50 km` distance bin's** positive within-bin elevation slope (+263.4) is signal.
  n=215 cells, 2.5 % of area, elevation range 57-1,958 m, aw r +0.087. Underpowered.


