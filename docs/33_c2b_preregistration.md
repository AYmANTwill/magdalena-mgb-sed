# 33 — Stage C2b pre-registration: validating the MUSLE drivers

**Status: PRE-REGISTRATION. FROZEN on write, 2026-08-10, by the `prereg-c2b` agent
(`docs/agents/journal_prereg-c2b.md`).**

Nothing in C2b's measurement phase may be computed before this file exists on disk,
because this file fixes the thresholds that would otherwise be chosen after seeing the
answer. Every number in §1–§3 is frozen. If a rule below turns out to be wrong, the
measuring session **journals it as an issue and follows it anyway**; changing a threshold
after seeing data invalidates the result. That rule has already been applied once inside
this document — see the issue note at the end of §4.

---

## 0 — Why C2b exists

MUSLE is

```
Sed = alpha * (Qsur * qpeak * A)^beta * K * C * P * LS2D
```

It consumes **surface runoff** and **peak flow**. Neither has ever been validated.

Phase B calibrated on **total discharge** at the gauge: KGE(Q), KGE(log Q), and a recession
signature (`src/calib_v2.py:95`, weights 0.40 / 0.40 / 0.20). That objective is
structurally blind to *how* the flow was partitioned, and it under-weights peaks —
KGE's alpha term is a ratio of standard deviations over the whole record, not a statement
about the annual maximum. Two parameter sets can produce an identical total-discharge KGE
with very different surface/subsurface/baseflow splits and very different flood peaks.
MUSLE sees that difference immediately: `Qsur * qpeak` is the entire hydrological content
of the sediment equation.

Concretely, the adopted configuration already carries three warnings that point at exactly
this:

- the model's internal partition is **51.3 % surface / 29.2 % subsurface / 19.5 % baseflow**
  and was **never validated against observation** (docs/26 §A.3, RC 0.5127);
- **alpha < 1 in every period** (0.90–0.92; docs/26 §A.4–A.5) — the model's flow variability
  is low, so peaks are low;
- the store-ordering inversion has now **relocated three times** under constraint
  (docs/26 §5.1 and §A.2: H2E fits `k_sup` 19.20 d against `k_int` 0.87 d, surface response
  22x slower than interflow). That is a partition pathology, and the total-discharge
  objective cannot see it.

C2b tests the drivers directly, against observation, before MUSLE is built on top of them.

This re-opens Phase B, which **docs/30 §1 permits only through a new pre-registration**.
This document is that pre-registration. See §5 for exactly what it amends.

---

## 1 — Hypotheses

Each is stated so it can be refuted, with the refuting statistic named and bounded.

### H-BFI — the model's slow/fast flow character matches observation

> The Eckhardt-filtered baseflow index of the simulated hydrograph agrees with the
> Eckhardt-filtered baseflow index of the observed hydrograph, gauge by gauge.

**Refuted if** the fleet-median `|BFI_sim − BFI_obs|` **exceeds the between-gauge spread of
`BFI_obs`**, where "spread" is fixed here as the **interquartile range (p75 − p25) of
`BFI_obs` across the gauge set of §2.4**.

The yardstick is deliberately the data's own spread rather than an invented constant: if
the model's typical BFI error is larger than the difference between one real catchment and
another, the model is not resolving flow character at all — it is producing a
basin-average hydrograph shape. That is a symmetric, self-scaling bar, in the same spirit
as the recession term's "a factor of two either way scores zero".

**Frozen sub-choice:** the IQR is the gate. The standard deviation of `BFI_obs` will be
reported alongside for context and **cannot change the verdict**. Naming both and gating on
one, in advance, is what stops the choice being made after the fact.

### H-PEAK — the model reproduces flood peaks

> The simulated annual maximum flows and high-flow exceedance quantiles match the observed
> ones, gauge by gauge.

**Refuted if** the fleet-median annual-maximum-series ratio `R_AMS` lies outside
**[0.85, 1.15]**, **or** the fleet-median Q1-exceedance ratio `R_Q1` lies outside
**[0.85, 1.15]**.

±15 % is the bound because MUSLE's dependence on peak flow is `qpeak^beta` with
beta ≈ 0.56 (Williams 1975, docs/31 §0): a 15 % peak error propagates to
`1.15^0.56 − 1 ≈ +8 %` on sediment load, which is small against the rating-curve
uncertainty the observed sediment target already carries (median R² 0.54, docs/31 §0).
A peak error larger than that starts to dominate the sediment error budget, which is the
definition of a driver that needs fixing. The bound is symmetric because an over-predicted
peak is exactly as damaging to a sediment claim as an under-predicted one — even though
docs/26 §A.4's alpha < 1 makes the low side the expected failure.

**Only those two statistics can refute H-PEAK.** The Q5-exceedance ratio and the
peaks-over-threshold count (§2.3) are measured and reported for mechanism, and a phase-2
session **may not** substitute them for the gate in either direction.

### H-CHIRPS — refitting the quantile maps on the repaired series fixes the volume failure

> Refitting the CHIRPS-gauge quantile maps on the **repaired** precipitation series —
> `precip_gauges_daily_qc.csv` with `approval == 'Inferido_seco'` days included, so the
> maps are no longer conditioned on reporting days only — brings the areal volume inside
> its pre-registered gate while retaining the LOOCV correlation gain.

**Refuted if either** frozen gate fails (both are carried over unchanged from docs/18 §15 /
docs/31 B1, and are **not** re-derived here):

| gate | bar |
|---|---|
| volume | area-weighted basin areal mean, **2009–2017**, within **±1 %** of the gauge-only **2,036.4 mm/yr** → the interval **[2,016.0, 2,056.8] mm/yr** |
| LOOCV | median daily r over the 287-gauge LOOCV set **> 0.429** |

The rejected merge scored r 0.447 (passed) and 2,188.5 mm/yr, +7.5 % (failed). The
diagnosed cause is that quantile maps fitted on reporting-day pairs re-inherit the
rain-selective bias of the 139 residual rain-selective stations (docs/18 §15.3).

H-CHIRPS is included in this document — even though it is a *forcing* question, not a
*driver-partition* question — for one reason: it is the only intervention that could still
change the drivers C3 will consume, so its gates must be frozen on the same page and at
the same moment as the driver gates. It remains **background and non-gating** on C1 and C2
(docs/31 B1). **A pass does not authorise adopting v3**: docs/30 §1 requires a further
pre-registration for that, and this document does not grant it.

---

## 2 — Exact definitions

No ambiguity is left for the measuring session. Where a choice existed, it is made here.

### 2.1 Baseflow separation — Eckhardt two-parameter filter

Applied **identically to the observed and the simulated series at each gauge**. This is the
apples-to-apples comparison and it is the whole point of the design.

> **Do NOT compare a filtered observation against the model's internal partition.** The
> model's internal surface/subsurface/baseflow split is a *generation-side* quantity: it is
> measured before routing, and the three components are routed through different linear
> stores (`k_sup`, `k_int`, `k_bas`) and then through the reach network. What arrives at
> the gauge has been redistributed in time. A filter applied to the gauge hydrograph
> measures the *routed* signature. These are different quantities and forcing them into
> one comparison would produce a difference that means nothing.

**The filter.** With `y_k` the discharge on day k and `b_k` the baseflow:

```
b_k = ( (1 - BFImax) * a * b_{k-1}  +  (1 - a) * BFImax * y_k ) / ( 1 - a * BFImax )
b_k = min(b_k, y_k)
BFI = sum(b_k) / sum(y_k)   over the scored days of that gauge
```

Single forward pass. Initialised `b_0 = y_0`; the **first 30 days of every continuous
segment are discarded** from both sums as filter warm-up.

**The recession constant `a`, per gauge.** Estimated from the **master recession curve of
the OBSERVED series** using the estimator already on disk and already validated against
docs/22 §4.4 — `calib_v2.recession_k` (monotone declines below the 40th flow percentile,
segments of ≥ 3 points, gauge constant = median over segments; validated in docs/26 §2
"Validation B" to a mean 0.26x of docs/22's ratios). Then

```
a = exp(-1 / k_obs)     with k_obs in days
```

**The same `a` is used to filter both the observed and the simulated series at that
gauge.** `a` is a property of the catchment, not of the model; letting the simulation
supply its own `a` would let the model define its own yardstick, and the comparison would
no longer be apples-to-apples.

**`BFImax` is FIXED at 0.80.** This is Eckhardt (2005)'s value for **perennial streams with
porous aquifers**, which is the correct class for the Magdalena–Cauca mainstem and its
perennial tributaries. It is **a fixed choice, not a fitted one** — it is not estimated
from the data, not tuned per gauge, and not selected after seeing any C2b number. Recording
this explicitly matters because BFImax is the single most abused knob in the baseflow-index
literature: a free BFImax can produce almost any BFI you want, and a "validation" done with
a free BFImax validates nothing.

**Robustness, reported but not a gate.** The whole BFI computation is repeated at
`BFImax = 0.50` (Eckhardt's perennial hard-rock value) and reported as a second column. If
the H-BFI verdict flips between 0.80 and 0.50, that instability is itself reported as a
finding — and **the 0.80 verdict still stands as the pre-registered one**.

**Data handling, frozen.**

- Period: **2009-01-01 → 2018-12-31 scored** (3,652 days); **2008 is warm-up and is
  excluded**, matching docs/26.
- Validity mask: the observed `q_valid` mask from `model_inputs_v2/discharge.npz`, as
  carried in `sim_calibrated_v2/q_gauge_H2E.npz`.
- Gaps of **≤ 3 days** are linearly interpolated; longer gaps break the record.
- A **segment** is a contiguous run of **≥ 180 valid days**; only segments qualify.
- A gauge enters the BFI statistic only if it has **≥ 1,095 valid scored days** (3 years)
  after segmentation. Gauges that do not are **excluded and counted**, with the count
  reported next to the verdict.
- The **identical day mask** is applied to the simulated series, so every comparison is
  paired day-for-day.

### 2.2 The model's internal partition — recorded, clearly labelled, NOT the test

Alongside the BFI table, record the model's internal generation-side partition for the H2E
run: **51.3 % surface / 29.2 % subsurface / 19.5 % baseflow** (docs/26 §A.3).

Label it in the output as a **different quantity** from BFI. It is a **consistency check,
not the test**: routing and channel storage move water from the fast components into the
slow tail of the gauge hydrograph, so `BFI_sim` is expected to exceed 0.195, and by how
much is a property of the router, not evidence about the partition. **No threshold attaches
to this number**, and no C2b verdict may be drawn from it.

### 2.3 Peak signatures

All computed on the **same masked, paired day set** as §2.1, from
`sim_calibrated_v2/q_gauge_H2E.npz` (`q_obs_m3s` vs `q_sim_fit_m3s`).

**(a) Annual maximum series ratio — the primary peak signature.**
For each calendar year 2009–2018 with **≥ 300 valid days** at that gauge, take the maximum
daily mean flow in each series (they need not fall on the same day — this is a magnitude
comparison). Then

```
R_AMS(gauge) = median over included years of ( Qmax_sim,y / Qmax_obs,y )
R_AMS(fleet) = median over gauges of R_AMS(gauge)
```

**(b) Q1 and Q5 exceedance-flow ratios.**
`Q1` is the flow exceeded on **1 %** of that gauge's valid scored days, `Q5` the flow
exceeded on **5 %**. Per gauge, `R_Q1 = Q1_sim / Q1_obs` and `R_Q5 = Q5_sim / Q5_obs`;
fleet statistic is the median over gauges. **`R_Q1` is a gate (§1); `R_Q5` is diagnostic.**

**(c) Independent peaks-over-threshold above Q5 — diagnostic count.**
Threshold = the **observed** `Q5` at that gauge, applied unchanged to **both** series (a
per-series threshold would make the two counts incomparable by construction). Two
exceedance peaks are **independent** if and only if:

- they are separated by **≥ 10 days**, **and**
- the minimum flow between them falls below **0.6 x** the lower of the two peaks.

Report `n_POT_sim`, `n_POT_obs`, and the ratio, per gauge and as a fleet median.
**Diagnostic only — no gate.**

### 2.4 Gauge set and period

**The calibration-safe set used by H2E: n = 63.** Verified from disk, not from a filename
count: `model_inputs_v2/gauges.csv` has 159 rows of which `cls == 'calib_safe'` is 63;
`model_inputs_v2/discharge.npz['is_calibration_safe'].sum()` is 63; `calib_v2.py:467`
selects exactly that mask; and `sim_calibrated_v2/q_gauge_H2E.npz` carries `q_obs_m3s` and
`q_sim_fit_m3s` at shape **(3652, 63)**.

**Period: 2009–2018 scored, 2008 warm-up.** Sub-period breakdowns (CAL 2012-14, VAL all,
VAL La Niña 11, VAL El Niño 15-16, VAL other 09/10/17, VAL 2018) are **reported** with the
same column set as `metrics_fleet.csv`, but **every gate in §1 is evaluated on the full
2009–2018 scored record**, so no verdict can be extracted from a favourable sub-window.

### 2.5 Reporting scale — both, always

Every statistic in §2.1–§2.3 is reported at **both** scales, as this project requires:

- **fleet**: the median over gauges (and the IQR), which is what the gates read;
- **per gauge**: a full 63-row table, written to disk, so the fleet median can be audited
  and so a gauge-level pathology cannot hide inside a healthy median.

A fleet number quoted without its per-gauge table is not a C2b result.

---

## 3 — Decision rules, fixed now

### 3.1 The four outcomes

| H-BFI | H-PEAK | consequence |
|---|---|---|
| holds | holds | **NO REFIT.** §3.4. |
| refuted | holds | refit with the BFI term (§3.2) |
| holds | refuted | refit with the peak term (§3.2) |
| refuted | refuted | refit with both terms (§3.2) |

H-CHIRPS is decided independently and changes nothing in this table: it can only produce a
v3 forcing proposal, which requires its own pre-registration (§1, §5).

### 3.2 The new objective terms and the exact weight vector

The incumbent objective, on disk at `src/calib_v2.py:95`, is

```
(W_KGE, W_LOG, W_REC) = (0.40, 0.40, 0.20)        sum = 1
F = mean over gauges of  sum_t w_t * c2m(score_t) / sum_t w_t
c2m(k) = k / (2 - k)      (Mathevet bounded transform)
```

`blend()` renormalises over the terms **defined** at each gauge, so a gauge missing one
signature is scored on the rest rather than dropped or credited zero. The new terms inherit
that behaviour unchanged.

**New term forms, frozen.**

```
BFI  term:  e_bfi(gauge)  = 1 - |BFI_sim - BFI_obs| / 0.20
PEAK term:  e_peak(gauge) = 1 - |ln R_AMS(gauge)| / ln(1.5)
```

Both are passed through `c2m` like every existing term. The `0.20` BFI scale means a BFI
error of 0.20 — one fifth of BFI's full [0, 1] range — scores exactly zero, mirroring
`REC_SCALE = ln 2`'s "a factor of two out scores zero". The peak term is **symmetric in log
space** for the same reason the recession term is: a peak 1.5x too high must cost exactly
what one 1.5x too low costs, or the objective quietly encodes a preferred direction. Both
scales are fixed here, before any C2b number exists; neither is derived from data.

**The exact new weight vectors.** A new term takes weight **0.15**, drawn **proportionally
from all three incumbent terms** (the recession term's 0.20 and the two KGE terms alike),
so the incumbent balance between skill and store realism is preserved rather than
re-litigated. Each incumbent weight is multiplied by `(1 - 0.15)` or `(1 - 0.30)`:

| case | W_KGE | W_LOG | W_REC | W_BFI | W_PEAK | sum |
|---|---|---|---|---|---|---|
| incumbent H2E | 0.40 | 0.40 | 0.20 | — | — | 1.00 |
| H-BFI refuted only | **0.34** | **0.34** | **0.17** | **0.15** | — | 1.00 |
| H-PEAK refuted only | **0.34** | **0.34** | **0.17** | — | **0.15** | 1.00 |
| both refuted | **0.28** | **0.28** | **0.14** | **0.15** | **0.15** | 1.00 |

(0.40 x 0.85 = 0.34, 0.20 x 0.85 = 0.17; 0.40 x 0.70 = 0.28, 0.20 x 0.70 = 0.14. Each row
sums to exactly 1.00, so `F(perfect) = 1` still holds, as in v1 and v2.)

This is the same pattern that took the recession ratio from **2.98x to 0.98x** (docs/26
§3 and §A.4): a signature the objective could not see was added to the objective, at a
stated cost in the terms it displaced, and the repair held on the held-out years.

### 3.3 The refit cell — registered here so phase 3 cannot invent cells

**`H2E-S`** = H2E + the new signature term(s) selected by §3.1. Everything else
**identical to H2E**:

| item | value |
|---|---|
| forcing | `model_inputs_v2/` (v2) |
| ET | FAO-56 threshold, `et_stress='fao56'`, `theta_crit` FIXED 0.6 (not searched) |
| parameter box | unchanged, including the `k_int/k_bas` ratio reparameterisation and `k_bas` lower bound 5 d |
| gauges | the 63 calibration-safe gauges (§2.4) |
| split | CAL 2012–14, VAL 2009–2018 minus CAL; 2008 warm-up |
| algorithm | DDS |
| budget | **1000** evaluations per seed |
| seeds | **2**: `20260907`, `20260908` (verified unused — `_calib_cache/` holds 20260901–06 for H1/H2 and 20260901–02 for H2E) |

No other cell is authorised by this document. No third seed, no budget increase, no
`theta_crit` search, no bound change — any of those needs a new pre-registration.

### 3.4 If BOTH hypotheses hold — no refit, and that is a RESULT

If H-BFI and H-PEAK both hold, **there is no refit**. Record that **the MUSLE drivers are
validated as-is** and that **Phase B closes for the second time — on evidence rather than
on exhaustion.**

Say this plainly in the write-up: the first close (docs/30 §1) rested on parameter headroom
being spent; this one would rest on a positive measurement that the two quantities MUSLE
actually consumes are right. **That outcome is a RESULT, not a failure, and not an
anticlimax.** A pre-registration whose hypotheses survive has produced the strongest
statement this project can make about its own drivers, and C3 then proceeds on validated
inputs instead of on hope. Any session tempted to search for a refit anyway, having read a
"both hold" verdict, is fabricating a problem — and the record will show it.

### 3.5 Success criteria for a refit (only if triggered)

A refit **succeeds** if and only if **all three** hold:

1. **The refuted signature comes inside its bound.** BFI: fleet-median
   `|BFI_sim − BFI_obs| ≤ IQR(BFI_obs)`. PEAK: fleet-median `R_AMS` in [0.85, 1.15]
   **and** fleet-median `R_Q1` in [0.85, 1.15]. If both were refuted, both must come in.
2. **Mean F stays within 0.02 of H2E's 0.25931**, i.e. **F ∈ [0.23931, 0.27931]**, where the
   mean is over the two registered seeds.
   > **The comparison is on the H2E scale, not the refit's own scale.** Adding a term
   > changes the objective, so the refit's own `F` is a different quantity and comparing it
   > to 0.25931 would not be like-for-like. Therefore: evaluate `calib_v2.blend` at the
   > **incumbent weights (0.40, 0.40, 0.20)** on the refit's fitted parameter set, and apply
   > the ±0.02 criterion to *that* number. The refit's native `F` is reported alongside and
   > is explicitly labelled incomparable. This is the docs/26 §2 "Validation A" pattern
   > (`blend_v1` kept verbatim so old and new numbers sit on one axis) applied one level up;
   > registering it now is what stops a phase-3 session from picking whichever scale flatters.
3. **No NEW parameter rails.** "Railed" keeps the pre-registered 5 %-of-range definition.
   H2E's incumbent railed set, from `sim_calibrated_v2/parameters_H2E.csv`, is
   **`k_sup@global` (pos 0.9911), `k_int_frac@global` (pos 0.0019), `wm_mult@R2`
   (pos 0.9713)** — **2 of 10 global, 3 of 18 dimensions**, both denominators stated as
   docs/26 §A.2 requires. The refit's railed set must be a **subset** of those three.
   `adr@soil-medium` at pos 0.9105 is inside the band by the rule and is **not** counted;
   it is recorded because it is the closest unflagged dimension and a reader quoting the
   parameters should see it.

**Anything else is a failure of the refit**, and it means **the signature and the objective
are in conflict** — the model cannot reproduce the driver signature without giving up
discharge skill or hitting a bound. **That is itself reportable**, and it is a real finding
about model structure, not a null. It does **not** license another refit: further work
needs a new pre-registration.

---

## 4 — What this does not do

**C2b does not chase F.** The arithmetic forbids it, and stating that now stops a phase-3
session from quietly reframing a driver-validation stage as a skill hunt.

`F` is a weighted mean of `c2m(score)` terms with `c2m(k) = k/(2−k)`. For `F = 0.5` with
terms of comparable quality, each term needs `c2m(k) = 0.5`, i.e. **KGE = 0.667**. But KGE
is bounded above by r:

```
KGE = 1 - sqrt( (r-1)^2 + (alpha-1)^2 + (beta-1)^2 )  <=  1 - |r - 1|  =  r     (r <= 1)
```

so the attainable ceiling is `F_max = c2m(r)`:

| r used | c2m(r) = F_max |
|---|---|
| 0.518 | **0.349** |
| 0.5564 (H2E fit, CAL 2012-14, `metrics_fleet.csv`) | **0.386** |

Either way **F ≈ 0.35 is the ceiling and F = 0.5 is arithmetically out of reach**, because
r is pinned by the rainfall field, not by any parameter: El Niño r sits at 0.556–0.572
across twelve configurations and the field's own LOOCV skill is 0.429 (docs/22 §4.7,
docs/26 §7).

> **The reframed goal, stated once and plainly: C2b exists to produce the most trustworthy
> surface-runoff and peak field for sediment — even if F falls.**

A refit that trades objective value for a correct partition or correct peaks is a **success**
by §3.5, not a regression, provided F stays inside the ±0.02 band. The band exists to catch
a *collapse*, not to defend a number. Phase C's deliverable is a sediment contrast; a
sediment model driven by a right-for-the-wrong-reasons runoff field is worth less than one
driven by a slightly-lower-scoring field that partitions water correctly.

> **Issue journalled, per the freeze rule.** The task brief that commissioned this document
> quotes "CAL r = 0.518"; the on-disk value in `sim_calibrated_v2/metrics_fleet.csv`
> (cell H2E, config fit, period CAL 2012-14) is **0.5564**. Both are reported above because
> both give the same verdict, and because silently substituting one for the other is exactly
> the kind of undocumented adjustment this project refuses. No pre-registered threshold is
> affected — this is §4 framing prose, not a gate.

---

## 5 — Amendment note: what this changes, and what it does not

### 5.1 docs/30 §1 — the Phase B freeze

docs/30 §1 froze the hydrology at H2E and stated: *"Any future forcing change (CHIRPS v3)
re-opens it only through a new pre-registration."*

**Amended to:** the hydrology is frozen except through a pre-registered re-opening, of
which **this document is the first**. The re-opening C2b claims is on the **objective**
(a signature term), not on the **forcing** — a case docs/30 §1 named only by its forcing
example. The forcing route stays exactly as written: H-CHIRPS passing both gates produces a
v3 *proposal*, and adopting it needs a further pre-registration that this document does not
grant.

**The frozen artifacts stay frozen until a refit succeeds.**
`sim_calibrated_v2/q_gauge_H2E.npz`, `parameters_H2E.csv`, `report_H2E.json` and
`h2e_drivers.npz` (521 MB) remain the Phase C drivers throughout C2b's measurement phase.
C2b *reads* them; it does not modify them.

**The cost of a successful refit, named now so it is not discovered later.** If H2E-S is
triggered **and** succeeds, then C0 must be re-run for H2E-S — new `parameters_H2E-S.csv`,
new `q_gauge_H2E-S.npz`, new `metrics_fleet.csv` rows, and a **regenerated
`h2e_drivers.npz`** — and **everything downstream of C0 that has already run must be
re-run against the new drivers**. C1 and C2 are unaffected (§5.3). Budget that cost into
the decision before triggering, not after.

### 5.2 docs/31 — stage order and document numbering

**Stage order.** C2b is inserted as a driver-validation stage that consumes C0's frozen
artifacts and gates C3, because C3 is where `Qsur` and `qpeak` are first used:

```
C0 ──► C2b ──► C3 ──► C4 ──► C5
       C1 ──► C2 ─────────► C4
B1 (= H-CHIRPS here), B2, B3, B4, B5: independent, non-gating
```

C2b **does not gate C1 or C2** — both are model-free observational stages (§5.3).

**Document numbering — a collision to avoid.** docs/31 C2.1 currently directs the C2
registration block to *"the top of `docs/33_observed_enso_contrast.md`"*. That is
**superseded**: number **33 is this document**. The renumbering, recorded here so two
sessions do not claim one number:

| content | docs/31 said | now |
|---|---|---|
| C2b pre-registration (this file) | — | **33** |
| C2 observed ENSO contrast | 33 | **34** |
| C4.2 sediment calibration pre-registration | 34 | **35** |
| C5.4 ENSO contrast results | 35 | **36** |

docs/31 is not edited by this session (it is outside this task's file scope); this table is
the authority until a session that owns docs/31 folds it in.

### 5.3 C1 and C2 are unaffected and run in parallel

**C1** (the SSC-quality gate) and **C2** (the observed, model-free ENSO flux contrast) touch
no model output whatsoever. C1 classifies SSC stations from `sediment_daily.csv` and paired
observed discharge; C2 computes observed flux as concentration x same-day **observed**
discharge. Neither consumes `Qsur`, `qpeak`, `h2e_drivers.npz`, or any fitted parameter.

**Therefore a C2b refit — triggered, succeeded, or failed — cannot invalidate a single C1 or
C2 number**, and the two tracks run in parallel with no coordination beyond this sentence.
The C1 decision (C1.0: 28 mapped / 24 calibration-safe stations, docs/32) and the C2.1
window registration stand unchanged.

### 5.4 What is frozen by this document

§1's three hypotheses and their bounds; §2's every definition (filter form, `a` estimator,
`BFImax` 0.80, warm-up, gap and segment rules, AMS/Q1/Q5/POT definitions, n = 63,
2009–2018); §3's weight vectors, term forms, cell specification, seeds, budget, and all
three refit success criteria. **None of it may be changed once any C2b number has been
computed.** A session that believes a rule is wrong journals the objection and follows the
rule.

## 6 — C2b.1 RESULT: H-BFI measured

**Added 2026-08-10 by the `bfi` agent (`docs/agents/journal_bfi.md`). §1–§5 above are
frozen and are NOT edited by this section.** Artifacts on disk: `src/baseflow.py` (the
filter, the MRC estimator, and the self-test), `data/processed/c2b/bfi_per_gauge.csv`
(63 rows — §2.5's required per-gauge table), `data/processed/c2b/bfi_summary.json`,
`data/processed/c2b/bfi_measure.py`, `data/processed/c2b/bfi_figure.py`,
`figures/deck/gen_bfi.png`. No frozen artifact was modified: `q_gauge_H2E.npz` and
`discharge.npz` were read only.

### 6.0 The gate came first

`python src/baseflow.py --selftest` — **9/9 pass**, run before any real series was
filtered, as the task's gate requires. The two anchors are analytic rather than empirical:

| check | result |
|---|---|
| pure exponential recession sampled at the filter's own `a` | BFI = **1.000000000000** (tol 1e-9) |
| spike train on a dry bed, `a = exp(-1/60)` | BFI = **0.062014**, identical to the analytic `(1-a)B/(1-aB)`; bar was < 0.10 |
| `0 <= b <= y` on a random gamma hydrograph | max(b − y) = 0.000e+00 |
| mixed hydrograph, monotone in the knob | BFI(0.50) 0.4573 < BFI(0.80) 0.6295 |
| gap rule | 3-day hole filled exactly; 4-day hole breaks the record |
| segments + warm-up | segments [(0,200),(260,500)], n_scored 380 = 440 − 2×30 |
| sub-180-day segments | dropped entirely (BFI NaN) |
| MRC recovers a known constant | **k = 25.000 d** from a synthetic 25 d sawtooth, 12 segments |
| `a = exp(-1/k)` round trip | exact |

Two things are worth recording because they are the kind of error that would have produced
a confident wrong answer:

- The MRC check first returned **27.078 d against a true 25.0 d**. The defect was in the
  *test*, not the estimator: the synthetic carried an additive `+1.0` offset, and
  `A e^{-t/k} + c` is curved in log space, so an OLS fit of `ln Q` must read `k` high.
  Removing the offset gives 25.000 exactly. No tolerance was loosened to make it pass.
- A **constant** series does **not** give BFI = 1; it gives BFI = `BFImax`. That is a
  correct Eckhardt property, and no test asserts otherwise. A "BFI = 1 for constant flow"
  test would have been a test of a misunderstanding.

### 6.1 What was filtered

Verified from the arrays, not from filenames: `q_gauge_H2E.npz['gauge_code']` is
element-wise equal to `discharge.npz['gauge_code'][is_calibration_safe]` (63); its dates
2009-01-01…2018-12-31 align with rows 366:4018 of `discharge.npz`;
`isnan(q_obs_m3s)` equals `~q_valid` exactly (50,464 invalid of 230,076) and the values
agree where valid; `q_sim_fit_m3s` has zero NaN.

**55 of 63 gauges are included.** Eight are excluded by the pre-registered
`>= 1,095` scored-day rule and are counted here as §2.1 requires:
`23087300, 23127050, 26127150, 26157080, 26187170, 26197020, 26217050, 28047010`
(scored days 703–1,032). None failed for want of a recession constant. Included gauges
carry 1,351–3,650 scored days (median 2,862).

Recession constants from the **observed** master recession curve: median
`k_obs = 10.44 d` (p10 5.34, p90 17.24) → median `a = 0.9087`. The same `a` filtered both
series at each gauge, on the same days.

One implementation choice, journalled: the simulated series is passed through the
*identical* code path, so the ≤3-day interpolated gaps are interpolated in the simulation
too rather than taking the simulation's own values there. Symmetric treatment was
preferred over using more information on one side. It is immaterial — forcing the
simulation to use its own values on those days moves `BFI_sim` by a median **6.2e-05**
(max 1.8e-03), against a median of 10 filled days per gauge.

### 6.2 The verdict, against the rule as written

> **§1, H-BFI, quoted:** *"Refuted if the fleet-median `|BFI_sim − BFI_obs|` **exceeds the
> between-gauge spread of `BFI_obs`**, where 'spread' is fixed here as the **interquartile
> range (p75 − p25) of `BFI_obs` across the gauge set of §2.4**."*

| quantity | value |
|---|---|
| fleet-median `BFI_obs` | **0.7811** |
| fleet-median `BFI_sim` | **0.7965** |
| **fleet-median abs difference** | **0.01625** |
| **IQR(`BFI_obs`) — the gate** | **0.02845** (p25 0.7593, p75 0.7878) |
| p10–p90 of `BFI_obs` (also requested) | **0.0673** (p10 0.7267, p90 0.7939) |
| SD of `BFI_obs` (§1: context only, cannot change the verdict) | 0.0307 |
| fleet-median signed difference | **+0.0128** (simulation slower) |

**0.01625 ≤ 0.02845, so H-BFI is NOT REFUTED.**

**Robustness at `BFImax = 0.50` (§2.1: reported, cannot change a verdict):** median
absolute difference **0.00308** against IQR **0.00487** → the same verdict. **The verdict
does not flip between 0.80 and 0.50**, so the instability clause of §2.1 is not triggered.

Per gauge, as §2.5 requires: **48 of 55** gauges have `BFI_sim > BFI_obs` (the simulation
is the slower hydrograph almost everywhere), 7 the other way; **23 of 55** individually
exceed the fleet IQR; **0 of 55** exceed 0.20, the scale at which §3.2's `e_bfi` term would
score zero. Largest errors: `21237040` +0.117 (243 km²), `21167090` +0.113 (345 km²),
`24017610` +0.103 (298 km²); largest negative `26237110` −0.073 (171 km²).

### 6.3 By period (reported; §2.4 evaluates every gate on the full record)

| period | median days | median `BFI_obs` | median `BFI_sim` | median abs diff | IQR(`BFI_obs`) | would refute on this window alone |
|---|---|---|---|---|---|---|
| CAL 2012–14 | 974 | 0.7803 | 0.7981 | 0.0186 | 0.0281 | no |
| VAL all | 2,040 | 0.7807 | 0.7960 | 0.0154 | 0.0286 | no |
| VAL La Niña 2011 | 365 | 0.7807 | 0.7962 | 0.0183 | 0.0358 | no |
| **VAL El Niño 2015–16** | 606 | 0.7698 | 0.7918 | **0.0295** | **0.0290** | **yes, by 0.0005** |
| VAL other 09/10/17 | 904 | 0.7792 | 0.7965 | 0.0191 | 0.0262 | no |
| VAL 2018 | 331 | 0.7800 | 0.7990 | 0.0157 | 0.0336 | no |

The El Niño window is the one place the statistic crosses its own bar, and by a hair
(0.0295 vs 0.0290). **It does not change the verdict**, and it must not: §2.4 fixes every
gate on the full 2009–2018 record precisely so that a verdict cannot be extracted from a
favourable — or an unfavourable — sub-window. It is recorded because it points the same
way as everything else in this project's dry phase (docs/22, docs/26 §7): the model's
worst flow-character error, like its worst skill, falls in the El Niño years, where the
simulated hydrograph is **+0.0255** too slow at the median.

### 6.4 Consistency check — a DIFFERENT quantity, no threshold (§2.2)

The H2E model's **internal, generation-side** partition is
**51.3 % surface / 29.2 % subsurface / 19.5 % baseflow**. The filter-derived
`BFI_sim` at the gauge has a fleet median of **0.7965**.

**Gap: +0.602.** Not one of the 55 gauges has `BFI_sim` below 0.195.

§2.2 anticipated the sign — routing and channel storage move water out of the fast
components into the slow tail — but the magnitude is worth stating plainly: **roughly three
quarters of what the model generates as "fast" arrives at the gauge carrying the temporal
signature of baseflow.** The routing cascade, not the runoff-generation split, is what sets
the character of the simulated hydrograph. Two consequences follow, and neither is a C2b
verdict:

- **The filter cannot see the partition.** A BFI comparison is not evidence about
  51.3/29.2/19.5 in either direction, and this result must not be quoted as validating it.
  The internal partition remains **never validated against observation**.
- **MUSLE consumes the un-routed `Qsur`**, which is precisely the quantity this check shows
  the gauge hydrograph cannot constrain. That is an argument for C2b.2's peak signatures
  carrying the weight, not the BFI.

Note the same gap applies to the observation: `BFI_obs` medians 0.781, so the real rivers
are equally "slow" under this filter. The two are compared with each other, as designed —
never against 0.195.

### 6.5 The caveat that has to travel with the verdict

H-BFI passes, and the pass is real by the rule that was frozen. But **the filter has very
little discriminating power on this fleet**, and a reader who takes "BFI validated" to mean
"flow character validated" would be over-reading it.

- `BFI_obs` spans only **0.658–0.799** and 12 of 55 gauges sit above 0.79 — both
  distributions are compressed against the `BFImax = 0.80` ceiling. That is why the
  yardstick IQR is 0.028 rather than something like 0.2.
- **`r(BFI_sim, BFI_obs)` across gauges is 0.094.** The model carries essentially **no
  between-gauge information** about flow character. It passes because both it and the
  observation sit near the ceiling, not because it tracks which catchment is flashy.
- `r(difference, BFI_obs) = −0.825`: the difference is almost entirely "the observation
  departs from the ceiling and the simulation does not follow".
- The error is systematically a **small-catchment** error: median absolute difference is
  **0.0317** in the smallest area quartile (68–236 km²) and **0.0081** in the largest
  (2,868–257,097 km²); `r(difference, log area) = −0.21`. Big rivers agree trivially; small
  flashy ones are where the model is too smooth.

This is journalled as an issue rather than acted on. **The rule is frozen and the verdict
stands as computed.** Anyone proposing a sharper flow-character test (a lower `BFImax`, a
flow-duration-curve slope, an event-scale runoff ratio) needs a new pre-registration —
§5.4 — and should note that the `BFImax = 0.50` robustness column showed the *same* pass,
so a simple ceiling change is not obviously the fix.

### 6.6 Where this leaves §3.1

H-BFI **holds**. C2b.2 was measured concurrently by a separate agent and **H-PEAK is
refuted** (§7.1). The §3.1 table therefore resolves on its third row — *"holds / refuted →
refit with the peak term"* — and the weight vector that applies is

| case | W_KGE | W_LOG | W_REC | W_BFI | W_PEAK |
|---|---|---|---|---|---|
| **H-PEAK refuted only** (the row this result selects) | 0.34 | 0.34 | 0.17 | — | 0.15 |

**The BFI term `e_bfi` is NOT triggered.** It must not be added to the objective on the
strength of §6.5's caveat, and the both-refuted row (0.28 / 0.28 / 0.14 / 0.15 / 0.15) must
not be used: H-BFI passed its pre-registered gate at 0.01625 against 0.02845, and passed
again on the `BFImax = 0.50` robustness column. Adding a term for a hypothesis that held
would be exactly the fabricated problem §3.4 warns about.

For the record, §6.5's own numbers do not argue for the BFI term either: `e_bfi` scores
zero at an error of 0.20, and **no gauge in the fleet reaches 0.12**.

