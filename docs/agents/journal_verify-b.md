# journal_verify-b — adversarial verification of H-B (orographic)

Task: try to REFUTE the H-B report (`docs/agents/journal_chirps-orographic.md`), not to agree with
it. Every load-bearing number recomputed independently from the handed ledger, with my own
formulae written from the column semantics documented at the top of `h2_harvest.py` — no reuse of
`hb*.py` helpers. Scripts: `<scratchpad>/verify_d/vb1_core.py`, `vb2_elev.py`,
`vb3_loocv_bounds.py`, `vb4_attack.py`.

## 0. Ledger semantics I relied on (read from `h2_harvest.py`, not from the report)

* `A` = CHIRPS present & k=6 IDW pass succeeded → blended at weight `w`.
* `B` = CHIRPS present & k=6 pass silent → pure mapped CHIRPS (effective weight 1).
* `D` = CHIRPS missing → gauge value kept, contributes 0 to the surplus.
* `s*` columns are **day-sums** per cell over the window, not rates. Any rate needs `/n_days*365.25`.
* `sCraw_all` / `sCmap_all` are `nansum` over **all** days, so they include D-days as zeros — they
  are therefore *not* the same base as `sCrawA+sCrawB`.
* `w_chirps` is not an independent variable: I verified
  `max|w − clip((d_nearest−10)/20, 0, 1)| = 5.7e-08`. **`w` is a deterministic function of
  `d_nearest`.** Distance is therefore in the surplus *formula*, not merely correlated with it.

## 1. Arithmetic: the decomposition closes and every handed number reproduces

Exact identity `sMerged − sP == w*(sCmapA − sPA) + (sCmapB − sPB)` closes to
`max|LHS−RHS| = 1.24e-03 mm` over 3,287 days (1.55e-03 over 4,018) — i.e. float32 accumulation
noise, ≈4e-7 mm/day. `nA+nB+nD == n_days` for all 8,672 cells, both windows.

Gate window 2009–2017, `n_days` 3287, area 257,096.9 km², area-weighted:

| quantity | mine | report / handed |
|---|---|---|
| gauge-only P | **2036.3927** | 2036.3927 ✓ |
| RAW CHIRPS | **2124.7205** | 2124.7205 ✓ |
| MAPPED CHIRPS | **2265.7574** | 2265.7574 ✓ |
| merged | **2188.5404** | 2188.5404 ✓ |
| surplus | **+152.1477** | +152.1477 ✓ |
| channels (map-infl blend / CHIRPS-vs-IDW blend / map-infl fb / CH-IDW fb) | **+87.3022 / +64.8070 / +0.0086 / +0.0298** | identical ✓ |
| w-bands (w=0 / 0<w<1 / w=1) | **+0.0031 / +54.2001 / +97.9445** | identical ✓ |
| full window 2008–2018 merged | **2219.1786** | 2219.1786 ✓ |

No weighting error found. Every table entry is area-weighted where it should be; the "specific
mm/yr" column is correctly the *local* area-weighted mean surplus inside the stratum (I confirmed
`Σ specific_k × area_share_k = 152.148`), and no day-sum is used as a rate anywhere.

## 2. Every reported table reproduced to the printed digit

* **Elevation distributions** (§1): gauge 375.9/1079.0/2393.4/2756.0, basin AREA-wt
  237.5/955.1/2154.5/2741.2, count-wt 213.7/898.6/2100.8/2697.5; means 1248.8 / 1144.6 / 1114.3. ✓
* **Gauge density** 98/33.7/38.5/**0.990**, 84/28.9/28.1/1.165, 55/18.9/19.2/1.117,
  54/18.6/14.3/**1.470**. ✓
* **Area above the highest gauge** 632 km² = **0.25 %**; own-zone version **18,413 km² = 7.16 %**,
  Cesar 30.3 % (17 gauges, highest 505.9 m, cells to 4,491.1 m), Saldaña 29.3 %, Bajo Magdalena
  20.3 %, Bajo Mag-Cauca-San Jorge 16.0 %. ✓
* **Surplus by band** +67.452 / +54.629 / +26.374 / +3.693 (44.33 / 35.90 / 17.33 / **2.43** %),
  local +175.2 / +194.7 / +137.7 / +25.8. ✓
* **Equal-area deciles** D1 (6–51 m) −23.848 → report −23.9 ✓; D4 (238–554 m) **+395.380** ✓;
  D9 +53.6 ✓; D10 (2741–4491 m) +45.6 ✓.
* **Map-inflation channel** +87.302 total, **+51.233 below 500 m**. ✓
* **qmap tail scale by band** 1.913 / 1.317 / 1.640 / 1.053 — these are **area-weighted over
  strata**; the report does not say so. Unweighted they are 1.694 / 1.606 / 1.711 / 1.302. The
  claim "weakest exactly where H-B needs it strongest" survives *both* weightings (band 3 is the
  minimum either way), so the conclusion is robust but the weighting must be stated.
* **Confound** aw corr(elev, d) = **−0.1757**, aw corr(elev, w) = **−0.1688**. ✓
* **Basin slopes** surplus on d **+15.706** mm/yr/km (aw r +0.3507); on elev **−38.313**
  mm/yr/1000 m (aw r −0.0722). ✓
* **Distance-bin table** 25.8/+0.0/+0.1/+0.028 · 36.9/+38.8/−6.0/−0.038 · 20.2/+197.9/−29.2/−0.051
  · 14.6/+580.8/+8.7/+0.009 · 2.5/+529.1/+263.4/+0.087. ✓
* **Field gradients at cells** P −224.18, Craw −209.35, Cmap −269.24; differences +14.83 and
  −45.07. I confirmed the algebraic identity `slope(Cmap) − slope(P) == slope(Cmap − P) = −45.07`
  exactly, so that comparison is arithmetically legitimate and not a two-population artefact.
  Zones with slope(Craw) > slope(P): **3 of 9** (Alto Magdalena +17.5, Saldaña +97.4, Cesar
  +349.1). ✓
* **At gauges** g on elev −223.5 mm/yr/1000 m, r −0.265, n=291; band means
  2021.1 / 1966.3 / 2057.7 / 1216.4; (Craw−g) on elev +16.9 (r +0.036); (Cmap−g) −25.1 (r −0.049);
  1500–2500 m Craw−g = **−163.7**. ✓ (0 gauges used the inventory-`alt` fallback — the elevation
  source is uniformly the DEM; corr(DEM, inventory alt) 0.980.)
* **w=1 anatomy** 1,496 cells, 43,933 km² (17.1 %), surplus +97.944 (64.4 %), aw elev 816.3 m vs
  1144.6 m (−328.4), 48.3 % below 500 m, 6.5 % above 2500 m, d 40.47 km (30.02–71.48); zone shares
  40.0 / 16.8 / 10.1 / 8.8 / 8.6 / 5.9 %; Bajo Magdalena aw elev 62.1 m, surplus −6.110; local P
  2483.2 vs 2036.4, local surplus +573.2 = **+23.08 %**. ✓
* **LOOCV** 0.481/0.475 (n=98), 0.426/0.449 (n=169), 0.343/0.300 (n=20); d_bias
  +0.00/+0.24/+0.89; fleet 0.429→0.447; 149/51/87. ✓ — matches docs/18 §15.2 table and §15.5 text
  verbatim.
* **20 w=1 gauges** median bias_base **+3.86 %**, mean +6.46 %, negative **8/20**; the 5 above
  1,500 m are +15.5/+17.2/+108.5/+73.4/+33.8, positive 5/5, `dbias`
  +0.6/−8.8/−28.6/−30.4/−32.2 → merge dries 4/5, median −28.6 pts. Refused slope: Pearson
  r +0.522 p=0.018, Spearman rho +0.371 p=0.107. ✓
* **Bounds** 10,708 km² (4.16 %) → **+28.208** = 18.54 %, raw-channel-only **+16.018** = 10.53 %;
  generous >1500 m ∧ Craw>P 51,511 km² (20.04 %) → **+37.729** = 24.80 %. Gate ceiling
  2036.4×1.01 = 2056.764 ⇒ surplus must fall to **≤ +20.371**; residues +123.940 → 2160.3 and
  +114.419 → 2150.8, both FAIL; miss factor 114.419/20.371 = **5.62×**. ✓
* **Robustness** full window +146.1241, <500 m 43.89 %, >2500 m 1.94 %. ✓

## 3. Citations checked against the docs

* docs/18 §15.3, line 928, verbatim: *"concentrated in the sparsely gauged (wet, high) terrain
  where w -> 1"*. The report quotes this correctly and its "half wrong" correction is well founded:
  *sparsely gauged* ✓ (aw d 40.47 km), *wet* ✓ (local P 2483.2 vs 2036.4), *high* ✗ (aw elev
  816.3 m vs 1144.6 m).
* docs/18 §15.2 (lines 904–908) and §15.5 (lines 990–992) — all six quoted LOOCV figures present
  and correct.
* **The gate band is cited, not invented.** docs/18 §15.1 (line 892) and §15.5 (line 984):
  *"within 1 % of the v2 gauge-only 2,036.4 mm/yr"*, band **[2,016.0, 2,056.8]** quoted verbatim
  in §15.5's gate table and in the §15.1 docstring of `src/merge_chirps_gauges.py` (VOLUME_TARGET
  2036.4, VOLUME_TOL 0.01), pre-registered in `docs/agents/journal_chirps-merge.md`. **No uncited
  band is doing work anywhere in the report.** No CRITICAL citation flaw.
* The report's flag on `bounds_fields.csv` is **correct**: `h3_bounds.py` line 109 sets
  `RATIO_104 = 1.836/4.056 = 0.4527` but labels F5/F6 *"credited 0.414 × own reporting mean"*. The
  mm/yr values are the 0.4527 ones. Label defect only; H-A's rows.

## 4. Reproduction failures / description defects I found

1. **The pocket table and the credit table use DIFFERENT masks and the report does not say so.**
   The §"What survives" table row is `above own-zone highest gauge ∧ Craw>P` (10,708 km²,
   +28.208). The pocket sentence's numbers (Cesar +16.769 @ 1,364 m; BMCSJ +9.049 @ 604 m;
   Saldaña +2.270 @ 3,106 m; Sogamoso +0.185 @ 3,802 m; Cauca −0.003 @ 4,115 m; Nechí −1.181)
   come from the `above`-only mask (18,413 km², **net +25.376 = 16.68 %**). I reproduced both
   exactly. Under the *credit* mask the same zones read Cesar +17.029 @ 1,404 m and BMCSJ +9.180
   @ **412 m** — so quoting "604 m" next to a table built on the other mask is a mismatch. Both
   sets are individually right; the section must name which mask each belongs to.
2. **"d restricted to blend cells gives +69.505"** does not reproduce under the natural reading. A
   *local* mean over `w>0` cells gives cov **+40.704**. +69.505 reproduces only if `d` is *zeroed*
   at `w=0` and still averaged over the whole basin area (my recompute: +69.47). Wording defect in
   a note that belongs to H-A/H-D, not H-B.
3. **`0.25 % of basin area lies above the highest gauge` is a claim about minibacia AREAL-MEAN
   elevation, not about terrain.** `minibacia_elevation()` is a label-mean of an 8×-block-averaged
   COP90 DEM, so peaks are smoothed away; gauge elevations are point samples of the same coarse
   grid. The figure is right for the field (which is defined per minibacia) and wrong as a terrain
   statement. Must be reworded.

## 5. The measurements the report did NOT run — and one of them cuts against it

### 5.1 Partial (multivariate) area-weighted slope on elevation, controlling for distance

The report stratified into 5 distance bins and read them by area. The direct test is a joint fit.
Area-weighted OLS of the per-cell surplus rate:

| model | elev coef (mm/yr per 1,000 m) | d coef (mm/yr per km) |
|---|---|---|
| surplus ~ elev | **−38.31** | — |
| surplus ~ elev + d | **−5.77** | +15.62 |
| surplus ~ elev + w | **−7.55** | (w: +497.58 per unit) |
| surplus ~ elev + d + d² | **−5.68** | +16.80 (d² −0.0228) |

**The −38.31 headline is almost entirely the elevation–distance confound.** Held at fixed
distance the elevation coefficient is −5.8, i.e. *nil*, not "running against H-B". The report's
"elevation contributes ~0 or negative" is the correct reading; its rhetorical "rainfall gradient
runs the other way, so H-B is backwards" is not supported once distance is controlled.

### 5.2 Within-stratum slopes aggregated by SURPLUS instead of by AREA — the sign flips

| d bin | area % | surplus share | % of total surplus | within-bin elev slope |
|---|---|---|---|---|
| 0–10 | 25.8 | +0.003 | 0.0 | +0.1 |
| 10–20 | 36.9 | +14.316 | 9.4 | −6.0 |
| 20–30 | 20.2 | +39.884 | 26.2 | −29.2 |
| 30–50 | 14.6 | +84.550 | **55.6** | **+8.7** |
| ≥50 | 2.5 | +13.395 | **8.8** | **+263.4** (aw r only +0.087) |

Area-weighted mean of the within-bin slopes **−0.2**; **surplus-weighted mean +19.8**. The report
wrote *"within bins elevation contributes ~0 or negative over 83 % of the area"* — true, but those
83 % of the area carry only **35.6 %** of the surplus. **64.4 % of the surplus sits in the two bins
whose within-bin elevation slope is positive.** This is a real weighting asymmetry: area for the
"no elevation effect" claim, volume for the "surplus is lowland" claim.

### 5.3 The elevation structure *inside* the w=1 area — the report's §4 stopped at composition

w=1 carries 64.4 % of the surplus. Within it the slope of surplus on elevation is **+18.1 mm/yr
per 1,000 m (positive)**, and the *local* surplus **rises** with elevation to 2,500 m:

| band inside w=1 | area km² | % of w=1 | share mm/yr | LOCAL surplus | local P |
|---|---|---|---|---|---|
| <500 m | 21,241 | 48.3 | +44.861 | +543.0 | 2446.9 |
| 500–1500 | 15,309 | 34.8 | +37.248 | +625.5 | 2797.6 |
| 1500–2500 | 4,518 | 10.3 | +12.271 | **+698.2** | 2111.1 |
| >2500 m | 2,865 | 6.5 | +3.565 | +319.9 | 1659.4 |

Equal-area elevation quartiles inside w=1 (local surplus): Q1 17–143 m **+77.5**, Q2 144–525 m
**+1020.9**, Q3 525–1145 m +657.2, Q4 1153–4491 m +539.0 — so it is a **maximum at 144–525 m**,
non-monotonic, not a clean orographic rise. But the report's flat claim that the surplus is a
"lowland/foothill phenomenon" is a statement about *where the remote area is*, not about
*intensity*: per unit area the surplus is **strongest at 1,500–2,500 m inside the region that
generates it**. This is the single measurement most favourable to H-B and the report omits it.
It does not rescue the gate — the whole >1,500 m part of w=1 is +15.8 mm/yr against a required
cut of 131.8.

### 5.4 Support-mismatch robustness for "gauge density is highest in the top band"

The numerator bands gauges by their own point DEM sample; the denominator bands *area* by
minibacia mean elevation. 31 of 291 gauges fall in a different band on the two supports.
Re-banding every gauge by the band of the minibacia it sits in (nearest centroid):

| band | n (own DEM) | n (cell band) | area % | per 1,000 km² own | per 1,000 km² cell |
|---|---|---|---|---|---|
| <500 m | 98 | 89 | 38.5 | 0.990 | **0.899** |
| 500–1500 | 84 | 87 | 28.1 | 1.165 | 1.206 |
| 1500–2500 | 55 | 57 | 19.2 | 1.117 | 1.158 |
| >2500 m | 54 | 58 | 14.3 | **1.470** | **1.579** |

The ranking is unchanged and the contrast widens. Mean gauge elevation on cell support 1,321.9 m
vs basin count-mean 1,114.3 m. **The "network is biased up, not down" claim survives its own
worst confound.** CONFIRMED and now robust.

### 5.5 A definition-free bound that is stronger than either bound the report offered

Both of the report's bounds depend on a definition of "creditable-as-orographic" that a critic can
argue with. The following needs none — credit **100 %** of the surplus above an elevation cut, no
`Craw>P` filter, no zone logic:

| cut | area % | credited mm/yr | % of surplus | residue | merged | gate |
|---|---|---|---|---|---|---|
| >250 m | 69.7 | +118.432 | 77.8 | +33.715 | 2070.1 | FAIL |
| >500 m | 61.5 | +84.696 | 55.7 | +67.452 | 2103.8 | FAIL |
| >1000 m | 48.0 | +48.682 | 32.0 | +103.465 | 2139.9 | FAIL |
| >1500 m | 33.4 | +30.067 | 19.8 | +122.081 | 2158.5 | FAIL |
| >2500 m | 14.3 | +3.693 | 2.4 | +148.455 | 2184.8 | FAIL |

To pass, any account must own **≥ 86.6 %** of the surplus (≥ 131.8 of +152.148 mm/yr). Everything
above 1,500 m owns **19.8 %**; above 500 m, **55.7 %**. **H-B cannot reach the gate even if every
millimetre above 500 m is conceded in full.** This is the claim I would publish, because it is
immune to the definition of "creditable".

Framing note (offered, not as a refutation): an area-weighted linear-in-elevation fit reproduces
the basin mean surplus **by construction** — a *gradient* hypothesis has no purchase on a *level*
offset, it can only relocate it. What H-B actually needs is a level offset localised to high
ground, and that is exactly what the band table (§5.5 above) prices at ≤19.8 %.

## 6. Inference defects in the verdict as written

1. **"three independent measurements, any one of which is sufficient" — they are not independent.**
   (a) is the elevation slope of observed gauge rainfall (−223.5); the P-limb of (b) is the
   elevation slope of the gauge IDW at cells (−224.18). `P` **is** the interpolated gauges, so
   those are the same fact measured twice; the independent content of (b) is
   `slope(Cmap) − slope(P) = −45.07`.
2. **(a) does not license "there is no enhancement to miss."** The −223.5 slope is produced
   entirely by the >2,500 m band. Gauge band means are 2021.1 / 1966.3 / **2057.7** / 1216.4 —
   *flat to 2,500 m with the 1,500–2,500 m band the wettest*, then a crest collapse. A
   mid-elevation orographic maximum is not excluded by a linear slope; it is what the gauges show.
   What *does* refute the mid-elevation variant is the like-for-like per-gauge measurement the
   report buried: at 1,500–2,500 m raw CHIRPS is **−163.7 mm/yr drier** than the gauges, and at
   500–1,500 m only +11.5 different — CHIRPS carries **no** mid-slope signal the gauges lack.
   That, not the slope, is the load-bearing sentence.
3. **(c) is a null result at n=20, not a positive finding.** median bias_base +3.86 %, 8/20
   negative. My tests: two-sided binomial **p = 0.503**; Wilcoxon signed-rank **p = 0.596**;
   one-sample t **p = 0.456**. The report's "p = 0.25" is the one-sided P(X≤8) and is not a test
   of wet bias. The defensible statement is *"not detectably dry-biased"*, i.e. H-B's prediction
   (`bias_base ≪ 0`) is **not observed** — not *"already wet-biased"*. The >1,500 m subgroup
   (5/5 positive) is n=5, **two-sided p = 0.0625** (one-sided 0.0312, which is what the report
   quoted without saying so), and only 1 of the 5 is above 2,500 m. Suggestive, not sufficient.
4. **"Distance explains it"** overstates aw r = +0.351 (r² = 0.12) if read as variance explained.
   The strong form of that claim is structural, not correlational, and the report never states it:
   `w ≡ clip((d−10)/20, 0, 1)` to 6e-08, so distance is *in the formula*. Say that instead.
5. **"Gauge density is highest in the top band"** is basin-wide and coexists with the report's own
   7.16 % own-zone blind spot. Both are true; the headline needs the qualifier.

## 7. Verdicts

* **H-B REFUTED as a rescue of the volume gate — CONFIRMED**, and on a stronger footing than the
  report used (§5.5: ≥86.6 % needed, ≤19.8 % available above 1,500 m, ≤55.7 % above 500 m).
* **H-B REFUTED as a mechanism — PLAUSIBLE, not CONFIRMED.** Refutation limb (a) is
  over-interpreted, (c) is a null at n=20, and §5.2/§5.3 show a positive elevation dependence of
  the surplus inside the strata that actually carry it. The surviving decisive facts are: the
  network is not elevation-deficient (§5.4, robust); the mapped field that enters the merge is
  −45.07 steeper *downward* than the field it displaces; and CHIRPS carries no mid-slope excess
  over the gauges (−163.7 at 1,500–2,500 m).
* **Individual measurement verdicts** are in §2 (all CONFIRMED) and §4/§6 (defects).
