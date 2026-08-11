# Journal — agent `c2-contrast`

GOAL: Phase C stage C2 — the OBSERVED ENSO sediment contrast, model-free. Deliverable
`docs/34_observed_enso_contrast.md` + figures in `figures/deck/`.

Hard constraints carried in:
- Pre-registration block written BEFORE any computation (C2.1). Order is auditable in this journal.
- Cross-window comparison by RATES ONLY (12-month vs 24-month windows).
- Every result reported for PRIMARY and SENSITIVITY windows.
- Absolute flux only (t/day, t). No t/km²/yr anywhere (area embargo, docs/23 §13.2).
- No git add/commit/push. Touch only docs/34, figures/deck/*, scratch scripts, this journal.

## Step checklist
- [ ] 0. Journal created; read C1 artifacts (docs/32, sediment_daily_qc, rating_curves, C1 screens).
- [ ] 1. C2.1 pre-registration written to docs/34 §1 BEFORE computing.
- [ ] 2. C2.2 per-station flux, both estimators, both window pairs, bootstrap CIs.
- [ ] 3. C2.3 consistency: estimator (a) vs (b); downstream monotonicity.
- [ ] 4. C2.4 literature anchor, exact figure fetched and cited.
- [ ] 5. Figures to figures/deck/.
- [ ] 6. docs/34 finalized; structured output.

## Log

### Step 0 — start
Journal created. C1 inherited: 79/79 classified, 6 usable + 12 usable_with_caveat,
13 usable in La Niña 2011, 12 in El Niño 2015-16, 7 in both. 30 rating eras, 0 unusable
(all n>=15), fleet median R² (Qs~Q) 0.546, median b 1.409, median residual sigma_ln 0.809.

### Step 1 — C2.1 pre-registration WRITTEN AND FROZEN (before any computation)
`docs/34_observed_enso_contrast.md` §1 written at this point. Nothing in §2+ existed yet; no
flux, ratio, or CI had been computed. Registered content:
- Windows P-LN 2011 / P-EN 2015-01..2016-12 (primary); S-LN 2010-07..2011-06 /
  S-EN 2015-10..2016-04 (sensitivity). Every result reported for BOTH pairs.
- Comparability rule: RATES ONLY (t/day). Totals may be context, never a ratio.
- Estimator (a) sample-day mean, ONLY where flag_flow_selective is False, n>=12,
  2000-rep day bootstrap, seed 20260810.
- Estimator (b) rating flux, per-era fit, Duan smearing primary + naive reported,
  cov<0.50 => `partial-rating` excluded from headline ratio table,
  1000-rep CI combining pair-refit (parameter) + 30-day moving-block residual bootstrap.
- EL PROFUNDO 15180 mg/L 2016-06-04: included in primary, sensitivity without it, >25%
  leverage => `single-point dominated`.
- C2.3 rules: disjoint CIs = missed C1 flag, must name mechanism; monotonicity on
  topologically nested pairs only; Momposina annotated as a sink.
- C2.4 pass = within factor 10 of the verified published load.
- C2 FAIL conditions registered in §1.10.
Station set: 18 mapped usable/usable-with-caveat; all 28 mapped are discharge stations too,
so Q pairs on the same `code`. 1 station is flow-selective (26127010 EL ALAMBRADO) => (b) only.

NEXT (risky/long): write scratch script and compute C2.2.

### Step 2 — C2.2 computed (scratch script; tables to data/processed/c2/, gitignored)
Script: scratchpad/c2_compute.py. Outputs: c2_station_window_flux.csv (72 station-windows),
c2_rate_ratios.csv (36 rows), c2_monthly_shape.csv. 71,528 same-day SSC/Q pairs, 18 stations.
KEY NUMBERS / PROBLEMS FOUND:
- **Paired-Q availability, not SSC, is the binding constraint.** 21237020 ARRANCAPLUMAS (the ONLY
  Magdalena-trunk SSC station) has 195 El Nino SSC samples but its DISCHARGE record ends
  2014-12-31 -> 0 paired days in P-EN/S-EN. No trunk ENSO contrast is computable, either estimator.
- 22057090 (Q ends 2009-03-19) and 26017020 JULUMITO (Q ends 2006-12-31): no flux in ANY window.
- 26127010 EL ALAMBRADO: 321 SSC in 2011 but 0 Q days in 2011.
- Primary pair both-window ratios: estimator (a) 6 stations, estimator (b) 7 (4 without
  partial-rating). >=3 => the §1.10 fail condition does NOT fire.
- EL PROFUNDO registered extreme test FIRED: removing 2016-06-04 (15,180 mg/L) moves the P-EN
  sample mean 112.47 -> 43.82 t/day = **+156.7 %** > 25 % => `single-point dominated`,
  rating estimate takes precedence for that station-window (as registered in §1.6).
- Primary (a) ratios: BORBUR 11.68, BOCAS-22017030 9.68, PUENTE ARAGON 6.79, CAPITANEJO 2.45,
  BOCAS-22017010 1.70, EL PROFUNDO 1.21 (single-point dominated).
- Primary (b) ratios: BORBUR 6.19, EL PROFUNDO 2.99, BOCAS-22017030 2.70, BOCAS-22017010 1.14
  (+ partial-rating: CAPITANEJO 2.95, NEMIZAQUE 3.15, PUENTE ARAGON 1.94).
NEXT: C2.3 nesting/monotonicity, C2.4 literature fetch, figures.

### Step 3 — C2.3 consistency (script 2)
- Estimator agreement: 38 testable station-windows, median b/a = 1.068, **8 disjoint (21 %)**
  -> under the registered 50 % fail line. Mechanisms NAMED with measurements:
  (1) C1.2 one-sided rule misses LOW-flow-biased sampling — 5 of 8 are dry-window with
      within-window sampled-day flow percentile 0.163/0.288/0.326/0.438; corr(ln b/a,
      ln Qsamp/Qwin) = -0.649; CARRASPOSO and PAILA LA are two of the three counter-direction
      stations C1 R2 named in prose;
  (2) ARRANCAPLUMAS: sampling UNBIASED (0.497/0.422) so it is era mis-specification — one era
      1990-01-01..2015-08-31, 6400 pairs, over-predicts 2011 by 1.6x;
  (3) PAILA LA / BOCAS-68: steep b (1.86 / 1.49-1.79) + sigma 0.91-1.06 => flow-tail driven.
      Duan S measured 1.080-1.832 (median 1.478) vs lognormal 1.083-1.826 -> smearing is NOT
      the culprit.
- Monotonicity: 22 topologically nested station pairs; 40 pair x window x estimator combos with
  both ends; **40/40 increase downstream, 0 violations.** No pair spans the Depresion Momposina —
  ALL 18 stations sit upstream of the Cauca confluence, so the sink is unobservable here.

### Step 4 — C2.4 literature anchor FETCHED AND VERIFIED
- Restrepo & Kjerfve (2000) J. Hydrology **235(1-2): 137-149**, doi 10.1016/S0022-1694(00)00269-9
  (Crossref-verified bibliographic record): **144e6 t/yr** at Calamar, 1975-1995, 55 paired
  measurements. Also states La Nina => marked increases, El Nino => moderate reductions.
- Restrepo & Escobar (2018) Geomorphology **302: 76-91**: **184 Mt/yr** (1980-2010).
- Basin 257,438 km2, ~7,100 m3/s at Calamar. Project domain sums to 257,097 km2 = 0.13 % off.
- ARRANCAPLUMAS annualised La Nina rate: (a) 15.1 / 13.3 Mt/yr, (b) 23.4 / 23.9 Mt/yr.
  vs 144 -> 6.0-10.8x ; vs 184 -> 7.7-13.8x. PASS on (b) both anchors; (a) misses factor-10 vs
  the 2018 anchor and the cause is identified: 21 % of basin area, above the Cauca and above the
  Momposina; it carries 24.6 % of outlet WATER but 10-16 % of outlet SEDIMENT.
- docs/31 open item 5 (unverified Restrepo anchor) is CLOSED by these two citations.

### Step 5 — figures written (verified by opening the PNGs, not by filename)
figures/deck/gen_c2_ratio_dotplot.png, gen_c2_flux_timeseries.png, gen_c2_monthly_shape.png.

### Step 6 — docs/34 finalised (§2-§7 appended AFTER §1 was frozen)
HEADLINE: 22/22 station-ratios > 1, both estimators, both window pairs, zero counter-examples.
Median RATE ratio: primary (a) 4.62 / (b) 2.84-2.95 ; sensitivity (a) 9.32 / (b) 6.40.
=> quote "~3x to ~9x", never a single number. C2 PASSES all three §1.10 conditions.
Files touched: docs/34_observed_enso_contrast.md, figures/deck/gen_c2_*.png, this journal,
data/processed/c2/*.csv (gitignored, regenerable). NO git commands run.
