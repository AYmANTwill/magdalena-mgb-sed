# Journal: adj-c4-feasibility

GOAL: establish whether C4 (sediment calibration) is FEASIBLE with the data we have, before
anyone writes its code. Deliver: (1) actual calibration station set after every filter with
names, (2) observations-to-parameters ratio and verdict, (3) confounding/equifinality answer
extending docs/42, (4) what C4 can/cannot deliver, (5) blocks_c4 = "is C4 infeasible".

CHECKLIST
- [ ] 1. Read docs/00_INDEX.md, docs/31 (C4 registration), docs/32 (SSC QC), docs/42 (guards),
      docs/13 (rating pairs), docs/37/40 as needed.
- [ ] 2. Load sediment_inventory_qc.csv + sediment_daily_qc.csv (chunked; never wide-CSV rules
      apply to forcing only, but still read carefully).
- [ ] 3. Filter chain: 18 usable -> tributary (not trunk) -> upstream of Momposina -> CAL
      window 2012-14 -> paired SSC+Q days sufficient for a rating curve. Count at each step.
- [ ] 4. Effective observations count (independent monthly/decorrelated, not raw days).
- [ ] 5. Parameter identifiability: alpha, beta, deposition coeff.
- [ ] 6. Confounding: alpha vs C vs LS on a single macro-region.
- [ ] 7. Verdict + structured output.

NOTES / STEPS (append-only, with numbers)

## S1 — docs read (2026-08-11)

- docs/00 INDEX read. docs/42 read IN FULL (it is the decisive input for task 3).
- docs/31 C4.1/C4.2/C4.3 read verbatim. Registered: calibrate tributary + upper-mainstem
  UPSTREAM of the Momposina, evaluate never calibrate below; params {alpha, beta, deposition
  coeff}; objective = KGE on log flux at the C1-usable tributary set; CAL = neutral 2012-14;
  both ENSO windows out-of-sample (Klemes); success = median log-flux KGE inside Fagundes'
  -0.26...0.44 AND params off bounds.
- docs/32 R6 read. Tributary set for C4 = 13 named codes. 8 mainstem / 20 tributary of the 28
  mapped. Only Magdalena-trunk SSC station = 21237020 ARRANCAPLUMAS.
- docs/42 §4.1 ALREADY MEASURED the Momposina filter and found it VACUOUS: all 18 usable
  stations lie upstream of the Cauca-Magdalena confluence, hence upstream of the Momposina.
  So filter (b) removes ZERO stations. I will re-verify this independently from topology.

## S2 — DECISIONS RECORDED BEFORE COMPUTING (this is the pre-commitment note the brief requires)

Recorded here BEFORE running any of the counting code below, and before I know any of the
resulting numbers:

- D1. "Tributary rather than trunk" = docs/32 R6's own topological trunk membership column
  (`reach`), not my own re-derivation. I take their 13-station tributary set as filter (a)'s
  output by definition; I will report the 5 mainstem stations separately.
- D2. Filter (b) "upstream of the Momposina" is evaluated as: does the station's minibacia lie
  strictly upstream of the Cauca-Magdalena confluence in `topology.npz`? I predict, from
  docs/42 §4.1, that it removes 0 stations. If my own computation disagrees with docs/42 I
  will report the disagreement, not pick the convenient one.
- D3. Filter (c) CAL window = 2012-01-01..2014-12-31 inclusive (docs/31 C4.2 "neutral years
  2012-14"). A station is "in the CAL window" if it has >= 1 non-deleted SSC observation
  inside it. That is the loosest possible reading and is deliberately generous.
- D4. Filter (d) "enough paired SSC-discharge days for a rating-based flux series": TWO
  thresholds, both reported, neither invented now for convenience:
    (i) the docs/32-registered rating-fit floor n >= 15 pairs (C1.5's own unusable rule), and
    (ii) the docs/32 C1.1 registered per-window sample floor N >= 91 (the flat-usable-mode
         threshold that decided the 18), applied to the 3-year CAL window.
  I commit NOW to reporting both counts even if (ii) collapses the set, and to treating (i) as
  the permissive bound and (ii) as the strict bound.
- D5. "Effective observations" for the obs:param ratio = independent STATION-WINDOW residual
  units, not raw days, because docs/42 §4.2 registered sigma_r = 0.465 ln as a per-STATION
  residual noise floor derived from estimator disagreement, i.e. the error does not average
  down within a station. I commit to reporting BOTH the raw paired-day count (the flattering
  number) and the station-count (the honest one), and to basing the verdict on the latter.
- D6. If beta turns out to be identifiable in principle (docs/42 §3.2 says yes, an exponent
  reweights days) I will still test whether the CAL data has the flow-range leverage to do it,
  and report a bound rather than asserting identifiability from theory alone.
- D7. I will NOT relax the Fagundes -0.26..0.44 KGE bar and will note that a NEGATIVE lower
  edge means the registered bar can be met by a fit with no skill over the mean.

## S3 — RESULTS (computed after S2, in the order S2 fixed)

Scripts (scratchpad, disposable): c4feas.py, c4feas2.py, c4feas3.py, c4beta.py, c4design.py.
Nothing in the repo was modified except this journal. No search was launched. h2e_drivers.npz
opened READ-ONLY.

### 3.1 The filter chain (task 1) — counts at every step

| step | tributary track | all-18 track |
|---|---:|---:|
| mapped + (usable or usable-with-caveat) | 13 | 18 |
| (a) tributary (docs/32 `reach`) | **13** | 18 |
| (b) & upstream of the Cauca-Magdalena confluence (= upstream of the Momposina) | **13** | **18** |
| (c) & >= 1 non-deleted SSC obs in CAL 2012-01-01..2014-12-31 | **9** | 11 |
| (d1) & >= 1 paired SSC+observed-Q day in CAL | **8** | 10 |
| (d2) & >= 15 paired days (docs/32 C1.5 rating floor) | **8** | 10 |
| (d3) & >= 91 paired days (docs/32 C1.1 registered floor) | **8** | 9 |
| (d4) & a usable rating era overlapping CAL | **8** | 10 |

**Filter (b) removes ZERO stations, and this is measured, not assumed.** Confluence node =
minibacia 4430 (UA 246,098 km2, 146.1 km above the outlet; parents 165,425 km2 Magdalena +
80,364 km2 Cauca). Every one of the 18 is upstream of it; the closest station to the outlet is
`23087210` CANTERAS at 684.4 km. Independently reproduces docs/42 §4.1.

**THE C4 CALIBRATION SET IS 8 STATIONS** (tributary, upstream of the Momposina, with paired
SSC-Q days inside the registered CAL window and a rating era covering it):

| code | name | dept | paired CAL days | CAL months w/ data (of 36) | obs-Q days in CAL | Lw km |
|---|---|---|---:|---:|---:|---:|
| `23127010` | BORBUR - AUT | boyaca | 845 | 33 | 1096 | 32.7 |
| `22017010` | BOCAS | tolima | 661 | 24 | 1095 | 42.5 |
| `22017030` | BOCAS | tolima | 637 | 23 | 963 | 2.6 |
| `24037390` | CAPITANEJO | boyaca | 477 | 18 | 727 | 60.4 |
| `26137110` | BANANERA LA 6-909 | risaralda | 213 | 9 | 1096 | 26.9 |
| `26127010` | EL ALAMBRADO AUT | quindio | 176 | 8 | **287** | 40.4 |
| `24027030` | NEMIZAQUE | santander | 145 | 7 | 771 | 27.1 |
| `21197010` | EL PROFUNDO | cundinamarca | 112 | 4 | 1093 | 30.4 |

Total 3,266 paired CAL days; 126 of 288 station-months (43.8 %) carry data.

**The 5 tributary stations lost, each for a hard record-window reason (not a method artefact):**
- `23087210` CANTERAS (SSC starts 2015-01-01), `26167060` PAILA LA (2015-01-03),
  `21147030` CARRASPOSO (2015-01-01) — the three El Nino-only stations: **zero** SSC in CAL.
- `22057090` BOCATOMA TRIANGULO — 619 SSC days in CAL but its **observed discharge ends
  2009-03-19**, so zero paired days. This is the costly one: Lw 110.4 km, the longest lever arm
  in the CAL 13.
- `26107130` MATEGUADUA — SSC ends 2011-05-30 AND zero observed Q in 2012-14.

**One mainstem station has CAL data: `21237020` ARRANCAPLUMAS, 501 paired CAL days, Lw 348.4 km.**
docs/31 C4.1 permits "tributary **and upper-mainstem** stations upstream of the Momposina" in
the fit; docs/42 §9 registered the fit set as the CAL 13 tributary set only. That is a live
tension and §3.3 below measures what it costs.

Area drained by the fitting set (union of upstream minibacias, topology.npz):
| set | minibacias | area km2 | % of basin |
|---|---:|---:|---:|
| all 18 | 3,282 | 98,988 | **38.5 %** (reproduces docs/42 §4.5 exactly) |
| CAL 13 | 884 | 25,844 | 10.1 % |
| **CAL 8 (actual)** | **476** | **13,862** | **5.4 %** |
| CAL 8 + ARRANCAPLUMAS | 2,161 | 64,653 | 25.1 % |

### 3.2 Observations to parameters (task 2)

Effective observation counts on the CAL 8 (D5 pre-commitment: report both):

| unit | count | : 3 params | : 2 params |
|---|---:|---:|---:|
| raw paired SSC-Q days (the flattering number) | 3,266 | 1089 : 1 | 1633 : 1 |
| lag-1-autocorrelation-effective days (median rho 0.771) | 474.2 | 158 : 1 | 237 : 1 |
| station-months with data | 126 | 42 : 1 | 63 : 1 |
| **stations = station-CAL-window residual units (the honest one)** | **8** | **2.7 : 1** | **4.0 : 1** |

The last row is the binding one because docs/42 §4.2 registered sigma_r = 0.465 ln as a
**per-station** floor: it does not average down within a station.

Parameter by parameter:
- **alpha** — NOT identifiable at all, individually (docs/42 §3.1: seven scalars, one product
  Pi, cond = inf). Reproduced here on the CAL 8: cond([1|fF|fG|fB]) = 5.7e3, singular up to
  docs/42's table rounding. What is identifiable is the LEVEL Pi. SE of the fleet-mean level =
  0.465/sqrt(8) = **0.1644 ln = +-38 % at 95 %** (13 stations would have given +-28.8 %).
- **beta** — **identifiable, and comfortably.** Measured, not assumed: because
  q_peak = Qsur*a_p/86.4, the station flux is sum_j W_j Qsur_j^(2 beta) with W_j static, so
  d ln F/d beta = 2 x (erosion-weighted mean ln Qsur). Computed on the real H2E driver field
  over the CAL-8 upstream sets and their paired CAL days: per-station sd of that derivative
  1.15-4.84 (median 2.88) ln per unit beta; pooled autocorrelation-deflated Sxx = 1,644.9.
  SE(beta) = **0.020** at the pessimistic sigma_day = 0.809 ln (the median rating residual over
  the 30 usable eras), 0.015 at 0.60, 0.012 at 0.465. 95 % CI half-width **0.039**, versus the
  registered band 0.45-0.65 whose half-width is 0.10. **Caveat that must travel with it:** the
  leverage is entirely the model's own ln Qsur spread, so beta is statistically identifiable but
  physically confounded with the surface-runoff partition -- exactly docs/42 G2's warning.
  (A crude first pass using observed ln Q as the driver proxy gave SE 0.075 and would have said
  "not identifiable". Recorded because it is the measurement that changed the verdict.)
- **deposition/settling coefficient k** — **NOT identifiable on the registered fit set.**
  Minimum detectable k (95 %, sigma_r 0.465, from the docs/42 §4.1 Lw values):

  | set | n | Lw span km | k_min /km | contrast over its own span |
  |---|---:|---|---:|---:|
  | all 18 (docs/42 guard set) | 18 | 2.6-348.4 | **0.00216** (reproduces docs/42 exactly) | 2.11x |
  | CAL 13 (docs/42 fit set) | 13 | 2.6-110.4 | 0.00964 (docs/42 prints 0.0104; 7 % apart, method rounding) | 2.83x |
  | **CAL 8 (actual fit set)** | **8** | **2.6-60.4** | **0.02092** | 3.35x |
  | CAL 8 + ARRANCAPLUMAS | 9 | 2.6-348.4 | **0.00303** | 2.85x |

  Losing BOCATOMA TRIANGULO (110.4 km, no CAL discharge) and 4 others takes k_min from 0.0096
  to 0.0209 /km -- **2.2x worse than docs/42 assumed, 9.7x worse than the guard that will judge
  the fit.** Adding the one trunk station recovers a factor 6.9.
  **UNCITED, and therefore may neither pass nor fail anything:** the 0.05-0.30 SDR band that
  docs/40 retired implies k ~ 0.0020-0.0032 /km over a 600 km path. It is printed only so the
  reader can see where 0.0209 sits. There is no citable expected k in this repository, so the
  correct C4 output for k is a BOUND, not a value.
- Also measured, joint G1.2+G3.1 regression r_i = c + k Lw + c_G fG + c_B fB:
  cond(scaled X) 2.56 on the CAL 8 (no collinearity problem -- the limit is n and sigma_r),
  residual df **4**. Minimum detectable class-C error, converting the coefficient bound through
  ln(1 - s + s f): **factor ~2.9 on all 18, ~4.2 on the CAL 8.** The C-factor guard can only
  catch order-of-magnitude C errors; it could not have seen the x1.2043 revision docs/41 made.
- **Fagundes bar.** For the mean predictor r = 0, alpha = 0, beta = 1 gives
  KGE = 1 - sqrt(2) = -0.414 (algebra, not a citation). The registered success band's lower edge
  is -0.26, i.e. **0.15 KGE units above no-skill-over-the-mean**, and the statistic is a median
  over 8 stations (the 4th/5th value). A "success" against that bar carries very little
  information.

### 3.3 Confounding (task 3)

docs/42 §3.1 answers the basin-total form: alpha, volume_factor, k_factor, ls2d_factor, a uniform
C multiplier, P and FG "are the same parameter written seven ways", partial derivatives = the
same column of ones, cond = inf. The extension asked for:

- **The premise "only tributary stations in ONE macro-region" is FALSE for this set, and it does
  not help.** The CAL 8 is 6 Magdalena-side + 2 Cauca-side, across 6 departments (tolima 2,
  boyaca 2, risaralda, santander, cundinamarca, quindio). Composition spread survives the cut:
  Bare share 0.0-75.6 pp, Grassland 10.7-69.8 pp, Forest 2.4-72.3 pp; Lw 2.6-60.4 km.
- **Region diversity buys nothing on the level.** The confounding is in the equations, not the
  sampling design, so no station set of any size or geographic spread separates a uniform alpha
  from a uniform C or LS level. More regions buy only CONTRASTS, and the contrasts are detectable
  only at a factor ~4.2 error (CAL 8).
- **Therefore: on this data a spatially uniform alpha CANNOT be distinguished from a wrong C
  level or a wrong LS level -- not partially, not weakly, not at all.** C4 can report only a
  FAMILY of equifinal solutions on Pi. That is docs/42 §3.3's registered requirement, and this
  pass adds the measured reason it is not merely conservative.

### 3.4 Issues raised

1. docs/42's registered fit set (CAL 13) is not achievable: 5 of the 13 have no paired SSC-Q day
   in the registered CAL window. Every §4.2 power number attributed to "the CAL 13" overstates
   the fit's power by 2.2x on k.
2. docs/42 §4.1 lists 3 CAL-CAL nested pairs; only **1** survives with CAL-window data on both
   ends (`22017030` -> `22017010`, 39.9 km).
3. docs/31 C4.1 permits upper-mainstem stations in the fit; docs/42 §9 excludes them. Resolving
   this in docs/42 §9 BEFORE the search is worth a factor 6.9 on k_min and takes the fitted area
   from 5.4 % to 25.1 % of the basin.
4. `26127010` EL ALAMBRADO has observed Q on only 287 of 1,096 CAL days (26 %), so its
   estimator-(b) flux series is a quarter-length series.
5. docs/07 does not classify 2012-14; the CAL window's ENSO-neutrality is asserted in docs/31
   with no in-repo ONI table behind it. UNCITED here.
6. Not computed: the CAL 8's share of the model's GROSS EROSION (docs/42 §4.5 gives 36.1 % for
   all 18). Only the area share (5.4 %) is measured here; do not interpolate between them.

Checklist: items 1-7 all done.
