# journal_adj-ratio

**Agent slug:** `adj-ratio`
**Started:** 2026-08-11
**Goal:** Settle whether the C3 gross-erosion-rate residual (model under-erosive by
1.03–2.27×) is **constant in time** — in which case it cancels in C5's wet/dry ENSO
*ratio* and is irrelevant to the deliverable — or **period-dependent**, in which case it
distorts the contrast and blocks C4/C5. Answer by measurement, not argument.

**Hard constraints I am operating under (restated so violations are auditable):**
- No git add/commit/push.
- Touch only: this journal (and read-only reads of everything else). No calibration launch.
- Frozen READ-ONLY: `sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv, q_gauge_H2E.npz}`.
- Never `pd.read_csv` the wide forcing CSVs — use `src/forcing_npy.py`.
- Verify from executed outputs, never exit codes.
- Gauge-referenced t/km²/yr yields EMBARGOED (docs/23 §13.2). Model-internal specific
  erosion allowed only if labelled as such.
- An uncited plausibility band may neither pass nor fail a gate — say UNCITED.
- **Any decision gets recorded here BEFORE I compute what it does to a headline number.**

## Checklist

- [ ] 0. Journal created (this file).
- [ ] 1. Read state: docs/00_INDEX (done), 34 (observed contrast), 37 + A1 (C3 verdict),
      40 (rate test), 33 §7 (R_AMS by period), 35 (q_peak), 42 (C4 guards), 23 §13.2.
- [ ] 2. Task 1 — enumerate mechanisms for non-constant bias, each with a SIGN.
- [ ] 3. Task 1c — derive the β=0.56 compression exactly; invert it.
- [ ] 4. Task 2 — measure simulated ENSO sediment ratio on frozen artifacts
      (h2e_drivers.npz + src/mgb_sediment.py, read-only), primary + sensitivity windows.
- [ ] 5. Task 3 — THE DECISIVE TEST: per-station observed/simulated flux ratio computed
      SEPARATELY for the La Niña and El Niño windows; compare the two distributions.
- [ ] 6. Task 4 — blocks_c4 verdict with condition.

## Log

### Step 0 — journal opened
Nothing computed yet. Reading order fixed above before any number is produced.

### Step 1 — state read (numbers I am inheriting, not producing)
- `docs/34` §3.1 — OBSERVED rate ratios: PRIMARY median 4.62 (a) / 2.84 (b, headline);
  SENSITIVITY 9.32 (a) / 6.40 (b, headline). 22/22 station-ratios > 1.
- `docs/34` §4.1 — **8 of 38 station-windows have disjoint estimator CIs, and five of those
  eight are DRY-window station-windows sampled at flow percentiles 0.163–0.438.** This is the
  single biggest confound for my task-3 test: a dry-window observed mean biased LOW by
  low-flow-selective sampling would look exactly like "the model under-erodes the wet phase
  more". It must be neutralised by day-matching, not argued away.
- `docs/37` A1.3.4 — SIMULATED basin ratio **2.2915× primary, 3.9725× sensitivity**
  (α=11.8, β=0.56 unfitted, `cp_revision='cited_central_2026_08_11'`, 299.5387 Mt/yr).
- `docs/33` §7.4 — `R_AMS` by period: **VAL La Niña 2011 = 0.808 (n=48), VAL El Niño 2015-16
  = 0.686 (n=39)**; no gate reads these. `R_POT` 0.500 vs 0.464.
- `docs/35`/`scripts/c3/qpeak.py` §5.4 — the +10 % over-statement of a SIMULATED contrast was
  **already registered** from exactly those two `R_AMS` numbers. Task 1b is therefore a
  re-derivation of a pre-registered quantity, not a new claim.
- `docs/00_INDEX` §7.3 — **`R_POT^0.56` is forbidden arithmetic**: β acts on magnitude, not on
  event counts. I will not raise any count ratio to β.
- **The registered `q_peak` proxy is `q_peak = Qsur · a_p / 86.4`, i.e. LINEAR in `Qsur`**
  (`src/mgb_sediment.py:runoff_energy_term`). So the MUSLE product ∝ `Qsur²` and the load
  ∝ `Qsur^(2β) = Qsur^1.12`. This inverts the premise of task 1c — see decision D7.

### Step 2 — DECISIONS, recorded BEFORE computing what they do to any headline number
*(This section is written and saved before the measurement script is run. I state explicitly
that I have not yet computed the task-2 or task-3 numbers at the time of writing it.)*

- **D1 — simulated station flux.** `Sim(station, day)` = **sum of `delivered_t_day` over the
  station's complete upstream minibacia set**, walked on the single-downstream (D8)
  `data/processed/minibacias.csv` topology from the station's `minibacia`
  (`sediment_inventory_qc.csv`). At `tau_delivery_days = 0` delivery is bitwise pass-through,
  so this equals upstream-summed gross hillslope erosion. **This asserts SDR = 1.0 between
  hillslope and station, with no channel deposition and no channel/bank/gully source** —
  stated as a claim, as `docs/42` G5 requires, not smuggled in.
- **D2 — day matching (the load-bearing decision).** The simulated window mean is taken over
  **exactly the same days** as the observed window mean, per station and per window:
  estimator (a) → the paired sample days; estimator (b) → all window days carrying a valid
  `q_m3s` (the rating's day set), with coverage reported. Reason recorded in advance: without
  day matching, `docs/34` §4.1's one-sided sampling selectivity would enter the test as a
  spurious period effect. Day matching cannot remove selectivity from the *observed level*,
  but it removes it from the *comparison*, because both sides then average the same days.
- **D3 — the test statistic.** Per station, `r_w = Obs_mean(w) / Sim_mean(w)` for
  `w ∈ {LN, EN}`, and `D = ln r_LN − ln r_EN = ln(observed contrast) − ln(simulated contrast)`.
  **`D = 0` ⇔ the multiplicative bias is identical in both phases ⇔ the C3 residual cancels
  exactly in C5's ratio.** `D` is invariant to every station-constant multiplicative factor —
  α, β's prefactor, LS level, C, P, K unit system, volume convention, FG, and any constant
  SDR — which is precisely why it can decide the question while the absolute level is unsettled.
- **D4 — uncertainty.** Nonparametric bootstrap, resampling **sample days i.i.d. with
  replacement within each window**, 2,000 reps, **seed 20260811**, percentile 2.5/97.5 on `D`.
  Registered limitation, same as `docs/34` §1.4: daily flux is autocorrelated and sample days
  are not random, so this interval is a LOWER bound on the true uncertainty. Also reported:
  the across-station distribution of `D` and a two-sided sign test on `D`.
- **D5 — configuration.** `load_geometry(cp_revision='cited_central_2026_08_11')`,
  `SedParams()` defaults (`williams_m3`, `us_customary`, `native_90m`,
  `ls2d_aggregation='area_weighted_mean'`, α = 11.8, β = 0.56, FG = 1.0, τ = 0) — the adopted
  C3 configuration of `docs/37` A1.3. Nothing is fitted; no calibration is launched.
- **D6 — station admissibility.** Estimator (a) only where `flag_flow_selective == False` and
  ≥ 12 paired sample days in BOTH windows (the C1.1/C1.2 rules, unchanged). `21197010` P-EN is
  `single-point dominated` (`docs/34` §1.6/§3.4) so `D` is reported for it **both with and
  without** the 2016-06-04 point, and the with-point value is the primary.
- **D7 — the β arithmetic, fixed before use.** Because the registered proxy makes `q_peak`
  linear in `Qsur`, the model's load scales as `Qsur^(2β) = Qsur^1.12`, i.e. it **AMPLIFIES** a
  surface-runoff ratio, it does not compress it. The `R^0.56` form applies only to a ratio of
  the **product** `(Qsur·q_peak·A)`. I will report both exponents explicitly and will not use
  `^0.56` on a `Qsur` ratio. Counts are never raised to β (`docs/00_INDEX` §7.3).
- **D8 — windows.** Exactly `docs/34` §1.1: P-LN 2011, P-EN 2015-01-01…2016-12-31,
  S-LN 2010-07-01…2011-06-30, S-EN 2015-10-01…2016-04-30. Rates only; no window total is ever
  divided by another (`docs/34` §1.2).
- **D9 — embargo.** No t/km²/yr anywhere. All fluxes absolute t/day. Any model-internal
  specific erosion, if quoted, is labelled model-internal.

**Confirmation of ordering:** D1–D9 above were written to this file before the measurement
script existed and before any task-2 or task-3 number was computed. The next log entry is the
first one that contains a number I produced.

### Step 3 — first measurement run. TWO REPRODUCTION GATES PASS EXACTLY
Script (scratchpad, not in repo): `adj_ratio.py`. Read-only throughout; no calibration.

- **Gate 1 — simulated basin ENSO ratio reproduces `docs/37` A1.3.4 to 4 d.p.:**
  primary **2.2915** (doc: 2.2915), sensitivity **3.9725** (doc: 3.9725). Window means
  1.3054 / 0.5696 / 1.5513 / 0.3905 Mt/day. Mass ledger `exact = True`.
- **Gate 2 — my day-matched observed estimator (a) reproduces `docs/34` §3.1's median:**
  the six primary (a) `obs_ratio`s are 1.212, 1.702, 9.679, 11.68, 2.451, 6.789 → median
  **4.62**, identical to docs/34's published 4.62. So the observed side is the same quantity
  docs/34 published, and the day matching did not silently change it.

**Task 3 raw result (the decisive numbers).** `expD = r_LN/r_EN = obs contrast ÷ sim contrast`
per station. Fleet cells:

| pair | est | n | geo-mean expD | median | range | >1 | sign-test p | CIs excluding 1 |
|---|---|---:|---:|---:|---|---:|---:|---:|
| primary | (a) | 6 | 0.8197 | 0.8712 | 0.2951 – 4.3531 | 3/6 | 1.000 | 4/6 |
| primary | (b) all | 7 | 0.8000 | 0.7828 | 0.3930 – 2.2791 | 2/7 | 0.453 | 5/7 |
| primary | (b) ok-only | 4 | 0.8283 | 0.7316 | 0.3930 – 2.2791 | 1/4 | 0.625 | 3/4 |
| sensitivity | (a) | 4 | 1.7833 | 1.9180 | 0.6215 – 4.5498 | 3/4 | 0.625 | 3/4 |
| sensitivity | (b) all | 7 | 0.8109 | 0.8809 | 0.2034 – 2.6223 | 3/7 | 1.000 | 6/7 |
| sensitivity | (b) ok-only | 5 | 1.1859 | 1.2887 | 0.3613 – 2.6223 | 3/5 | 1.000 | 4/5 |

Reading it before deciding anything: the **central** tendency sits near 1 (0.80 – 1.78), so
there is no established systematic direction; the **per-station spread is enormous**
(0.20 – 4.55) and **18 of 24 station-cells have bootstrap CIs excluding 1**. Those two facts
together are the answer, and they are not the same answer.

### Step 4 — SECOND SET OF DECISIONS, again recorded before the numbers they move
*(Written before the follow-up script was run. I have NOT yet computed D10–D13's outputs.)*

- **D10 — the like-for-like fleet comparison.** `docs/37` A1.3.4 compared a **basin-total**
  simulated ratio (2.2915) against a **fleet median of tributary station** observed ratio
  (2.8 – 4.6) on **different day sets**. That is three mismatches at once. I will therefore
  also report the **fleet median of the per-station SIMULATED contrast**, on the same stations,
  same days, same estimator, beside the observed median — because that is the only comparison
  that can be read as a bias.
- **D11 — fleet uncertainty.** Bootstrap over **stations** (resample the station set with
  replacement, 10,000 reps, seed 20260811) for a CI on the geometric mean of `expD`, so the
  n = 4–7 fleet size is priced in rather than asserted. Report the sign test's **power**: at
  n = 6 the minimum attainable two-sided p is 2/2⁶ = 0.03125, so a unanimous direction *would*
  have been detectable; at n = 4 it is 0.125 and the test is underpowered by construction.
- **D12 — heterogeneity is reported, never averaged away** (`docs/34` §1.1's rule): the
  primary and sensitivity cells disagree by a factor of ~2.2 on estimator (a) (0.82 vs 1.78)
  and that disagreement is stated as a finding.
- **D14 — heterogeneity test (added at Step 5, before its numbers were computed).** The
  question "is the bias constant?" is formally a homogeneity question, so it gets the standard
  homogeneity statistic: **Cochran's Q on `ln expD`** with per-station variance taken from the
  D4 bootstrap (`σ̂ = (ln hi − ln lo)/3.9199`), plus **I²**. Registered interpretation, written
  before the numbers: `Q ≫ df` / high I² ⇒ the bias is **not** a single constant; `Q ≈ df` ⇒ a
  single constant bias is consistent with the data. Registered caveat: the D4 bootstrap is a
  LOWER bound on within-station uncertainty, so Q is biased **upward** and I² **overstates**
  heterogeneity — i.e. this test is conservative against the "bias is constant" conclusion,
  which is the direction that protects C5 from a false clean bill of health.
- **D13 — sensitivity variants to be reported:** (i) `21197010` EL PROFUNDO with the
  2016-06-04 point removed; (ii) `expD` against upstream area (Spearman) to test whether the
  spread is a scale effect; (iii) the smallest-`n_EN` cells (`26017060` has n_EN = 33 and 16)
  flagged, since a 16-day dry window cannot carry a contrast.

### Step 5 — results of D10–D14

**D10 — the like-for-like fleet contrast (same stations, same days, same estimator).**

| pair | est | n | OBS median | SIM median | obs/sim of the medians |
|---|---|---:|---:|---:|---:|
| primary | (a) | 6 | 4.620 | **4.903** | **0.9423** |
| primary | (b) all | 7 | 2.949 | **2.904** | **1.0154** |
| primary | (b) ok-only | 4 | 2.845 | 3.081 | 0.9232 |
| sensitivity | (a) | 4 | 9.320 | **4.212** | **2.2129** |
| sensitivity | (b) all | 7 | 4.650 | **4.998** | 0.9304 |
| sensitivity | (b) ok-only | 5 | 6.404 | 4.970 | 1.2887 |

**In 5 of 6 cells the model reproduces the observed ENSO contrast to within 1.29×, and in
three of them to within 8 %.** `docs/37` A1.3.4's "short by 1.22 – 2.01×" compared a
**basin-total** simulated ratio (2.2915) against a **fleet-median tributary-station** observed
ratio on a **different day set** — three mismatches at once. Repairing the basis moves the
simulated number 2.2915 → 4.903 (est. a) or 2.904 (est. b), i.e. **×2.14 / ×1.27**, which is
the whole of the primary-pair gap. The day set alone is worth ×1.69 (4.903 vs 2.904).

**D11 — fleet pooling, bootstrap over stations (10,000 reps, seed 20260811).** All four cells'
CIs contain 1: geo-mean `expD` 0.8197 [0.404, 1.951], 0.8000 [0.523, 1.269],
1.7833 [0.856, 3.503], 0.8109 [0.416, 1.529]. Sign tests p = 0.45 – 1.00 against a **minimum
attainable** two-sided p of 0.031 (n=6) / 0.016 (n=7) — the test could have detected a
unanimous direction and did not.

**D12 — window-pair disagreement, same stations.** `expD` moves by ×0.51 – ×7.58 between the
primary and sensitivity definitions of the same station. Stated as a finding per `docs/34`
§1.1, not averaged.

**D13 — sensitivities.** (i) The registered EL PROFUNDO precedence moves its primary (a)
`expD` 0.2951 → 0.7584, and the cell to **geo-mean 0.9593, median 1.0786** — within 4–8 % of
exactly constant. (ii) `expD` vs upstream area: ρ = −0.20 … −0.68, **p = 0.094 – 0.800, none
significant** — the scatter is not a scale effect. (iii) `26017060` carries n_EN = 33 / 16 / 25
and its cells are correspondingly wide; flagged, not deleted.

**D14 — homogeneity. This is the number that decides the question.**

| pair | est | n | Cochran Q | df | p | I² | τ (log) | RE pooled expD [95 %] |
|---|---|---:|---:|---:|---:|---:|---:|---|
| primary | (a) | 6 | 255.7 | 5 | 3.3e-53 | **98.0 %** | 1.225 (=3.40×) | 0.848 [0.310, 2.318] |
| primary | (b) | 7 | 310.1 | 6 | 5.6e-64 | **98.1 %** | 0.707 (=2.03×) | 0.801 [0.472, 1.360] |
| sensitivity | (a) | 4 | 75.3 | 3 | 3.2e-16 | **96.0 %** | 0.902 (=2.47×) | 1.791 [0.720, 4.459] |
| sensitivity | (b) | 7 | 783.6 | 6 | 5.4e-166 | **99.2 %** | 1.127 (=3.09×) | 0.815 [0.351, 1.891] |

**Side finding (spatial, not temporal, and it does not touch `expD`).** The apparent delivery
ratio `r = obs/sim` spans **0.0039 – 1.239 across 46 station-windows, a factor of 322**.
**Only one station of eighteen — `23127010` BORBUR — has `r > 1`**, i.e. observed flux above
the model's entire upstream hillslope erosion; that is a local, like-for-like instance of
`docs/40`'s Leg-B impossibility argument, at 1 station rather than basin-wide.

**Honesty note on areas.** The 18 stations' `up_area_km2` in `sediment_inventory_qc.csv` equals
my D8 upstream sum to 3 d.p. for all 18 (ratio 1.000). That is **not** independent
corroboration — it is the same model-derived number. `expD` is area-invariant regardless.

### Step 6 — VERDICT

**The C3 residual's period-differential is centred on 1 and has no established direction, but
it is emphatically NOT a single constant across stations.**

- **Not systematically period-dependent:** four independent fleet cells, all CIs containing 1
  (RE pooled 0.80 – 1.79), sign tests non-significant with adequate minimum power, and the
  like-for-like contrast matching observation to within 8 % in three of six cells.
- **Not constant either:** I² = 96 – 99 %, Q p ≤ 3e-16, τ = 2.0× – 3.4× per station, observed
  `expD` range 0.20 – 4.55, and 18 of 24 station-cells with CIs excluding 1.
- **The uncertainty band is as wide as the thing being tested.** Primary (a) pools to
  [0.310, 2.318] — a factor of 7.5 — against a C3 residual of 1.03 – 2.27×. So constancy is
  **not refuted and not established**; it is unresolvable at n = 4 – 7 stations.

**`blocks_c4 = PARTIALLY`**, on the conditions written into the summary. What would tell:
more both-window stations. At τ ≈ 0.9, certifying the period-differential to ±50 % needs
n ≈ 19 stations and to ±20 % needs n ≈ 94; the network currently supplies 4 – 7. The two named
routes to more are `docs/34` §7 item 2 (recover post-2014 discharge at `21237020`
ARRANCAPLUMAS) and item 1 (two-sided C1.2 selectivity rule, which would readmit
low-flow-sampled dry windows).

**Files written:** this journal only, inside the repo. Tables live in the session scratchpad
(`adj_ratio_station_window.csv`, `adj_ratio_decisive.csv`, `adj_ratio_summary.json`) and are
regenerable from `adj_ratio.py` / `adj_ratio2.py` / `adj_ratio3.py`. No repo artifact was
modified; no frozen artifact was written; no calibration was launched.

## Checklist — final

- [x] 0. Journal created.
- [x] 1. State read (00_INDEX, 34, 37+A1, 40 via 37, 33 §7.4, 35 via qpeak.py, 42 via 37).
- [x] 2. Task 1 — mechanisms enumerated with signs (in the summary; 7 of them).
- [x] 3. Task 1c — exponent derived (2β = 1.12, not β = 0.56) and inverted.
- [x] 4. Task 2 — simulated ratio measured, 2.2915 / 3.9725, reproduces docs/37 exactly.
- [x] 5. Task 3 — per-window bias ratio computed per station, with CIs, Q, I², τ.
- [x] 6. Task 4 — `blocks_c4 = PARTIALLY` with conditions and with what would tell.
