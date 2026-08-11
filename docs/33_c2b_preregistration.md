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

> **[resolved 2026-08-10 — see §7]** H-CHIRPS is **REFUTED by its own volume gate**
> (2,188.5 mm/yr against the required [2,016.0, 2,056.8]). The registered intervention
> turned out to be a **no-op**: the quantile maps already included the inferred-dry days,
> so the diagnosed cause in docs/18 §15.3 was wrong. This paragraph is a pointer, not an
> edit to the frozen hypothesis — the original wording above is unchanged.

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

---

## 7 — C2b.2 RESULTS: flood-peak bias (H-PEAK)

**Measured 2026-08-10 by the `peaks` agent (`docs/agents/journal_peaks.md`), following §2.3
and §2.4 as frozen. §1–§5 above are unaltered.** Artifacts on disk:
`data/processed/c2b/peaks_per_gauge.csv` (63 rows, §2.5's required per-gauge table),
`data/processed/c2b/peaks_summary.json`, `data/processed/c2b/peaks_measure.py`,
`figures/deck/gen_peaks.png`.

*(§6 is deliberately left free for the C2b.1 / H-BFI results, which were being measured
concurrently by a separate agent; this section took §7 so the two appends could not collide.)*

Source: `data/processed/sim_calibrated_v2/q_gauge_H2E.npz`, `q_obs_m3s` vs `q_sim_fit_m3s`,
shape (3652, 63), 2009-01-01 → 2018-12-31. No frozen artifact was modified.

### 7.1 The verdict

> **H-PEAK is REFUTED.**

The rule, quoted from §1: *"Refuted if the fleet-median annual-maximum-series ratio `R_AMS`
lies outside [0.85, 1.15], **or** the fleet-median Q1-exceedance ratio `R_Q1` lies outside
[0.85, 1.15]."*

| gate statistic | fleet median | IQR over gauges | band | in band? |
|---|---|---|---|---|
| `R_AMS` | **0.820** | 0.529 – 1.186 | [0.85, 1.15] | **NO — below** |
| `R_Q1` | **0.847** | 0.633 – 1.234 | [0.85, 1.15] | **NO — below** |

Both gate statistics fail, and each fails on its own; the disjunction is not doing any work.
The failure is **on the low side**, which is the direction docs/26 §A.4's `alpha` 0.90–0.92
predicted. The prediction is confirmed but the magnitude is larger than `alpha` implied:
`alpha` is a whole-record standard-deviation ratio, and the peak deficit at the annual
maximum (−18.0 %) is roughly twice the whole-record dispersion deficit (−8 to −10 %).

`R_Q1` at 0.847 sits 0.003 below its bound and would be called marginal on its own. It is
recorded as marginal and it is **not** the load-bearing number: `R_AMS` at 0.820 is 0.030
clear of the bound, the two are rank-correlated at Spearman 0.928, and both point the same
way. Per §1 the two diagnostics below could not have rescued either gate in any case.

Consequence, from §3.1, now that §6 has recorded **H-BFI holds**: the outcome table's
**"holds / refuted"** row applies — **refit with the peak term only**, at weights
`W_KGE` 0.34 / `W_LOG` 0.34 / `W_REC` 0.17 / `W_BFI` — / `W_PEAK` 0.15, using
`e_peak = 1 − |ln R_AMS| / ln(1.5)` through `c2m`, in cell `H2E-S` (§3.3: v2 forcing, FAO-56
ET with `theta_crit` 0.6, 63 gauges, DDS, 1000 evaluations, seeds 20260907 and 20260908).
**The `e_bfi` term is NOT triggered** — §6.6 says so from the BFI side and this section
confirms it from the peak side. This section **triggers** the refit; it does not run it, and
§3.5's three success criteria (signature inside its bound; `F` on the **incumbent** (0.40,
0.40, 0.20) scale within 0.02 of 0.25931; no new rails beyond `k_sup@global`,
`k_int_frac@global`, `wm_mult@R2`) are the bar it will be judged against.

The frozen artifacts stay frozen (§5.1): this measurement read
`q_gauge_H2E.npz` and wrote nothing into `sim_calibrated_v2/`.

### 7.2 Fleet statistics, full 2009–2018 scored record, n = 63

| statistic | fleet median | IQR | role |
|---|---|---|---|
| `R_AMS` — annual-maximum ratio | **0.820** | 0.529 – 1.186 | **gate** |
| `R_Q1` — 1 %-exceedance ratio | **0.847** | 0.633 – 1.234 | **gate** |
| `R_Q5` — 5 %-exceedance ratio | 0.975 | 0.740 – 1.279 | diagnostic (§1) |
| `R_POT` — independent events above observed Q5 | 0.567 | 0.155 – 1.141 | diagnostic (§1) |
| median absolute timing lag, top-10 observed events | 4 d | 2 – 7 d | not pre-registered (§7.6) |

Geometric mean of `R_AMS` (log-symmetric, matching the §3.2 peak term's own form): **0.810**.

**The shape of the error is a tail effect, not a level shift.** `R_Q5` is 0.975 — the model
reproduces the flow exceeded 5 % of days almost exactly — while `R_Q1` is 0.847 and `R_AMS`
is 0.820. The bias switches on somewhere between the 95th and the 99th percentile and
deepens all the way to the annual maximum. A uniform multiplicative correction on discharge
would therefore be the wrong repair; the deficit lives in the extreme tail only.

**Event count is worse than event size.** Applying the *observed* Q5 as the threshold to both
series (§2.3(c)), the model produces **1,285 independent peaks against 2,236 observed
(0.575 fleet-wide, 0.567 as a median over gauges)** — it misses **43 %** of the events that
cross the observed high-flow threshold at all, and it under-produces events at **42 of 63**
gauges. Four gauges produce **zero** simulated exceedances of their observed Q5 over ten
years. This is diagnostic only under §1 and cannot move the verdict, but it is the more
alarming number for MUSLE: sediment is delivered in events, and a model that generates
little more than half of them will under-deliver load even where the surviving peaks are the
right size.

### 7.3 Per-gauge scale — the median is not hiding a uniform bias

| `R_AMS` | gauges |
|---|---|
| below 0.85 | **36** |
| inside [0.85, 1.15] | 9 |
| above 1.15 | **18** |

Range 0.247 – 3.169. The fleet is **bimodal, not uniformly low**: a majority under-predicts
badly and a substantial minority over-predicts badly, and the median lands at 0.820 because
the low group is bigger, not because the typical gauge is 18 % low. Nine gauges out of
sixty-three have a peak ratio a sediment modeller would accept.

Worst under-prediction: `21257090` (486 km², `R_AMS` 0.247, 20 observed POT events, **0**
simulated), `26017060` (152 km², 0.273, 48 obs / 1 sim), `23147040` (1,569 km², 0.280,
40 obs / 0 sim). Worst over-prediction: `21107030` (288 km², 3.169), `22077060` (731 km²,
3.075), `26237020` (210 km², 2.293, 20 obs POT / 94 sim).

Seven gauges have fewer than the 1,095 valid scored days that §2.1 requires *for the BFI
statistic*; §2.3 does not repeat that rule and it was therefore **not** applied to the peak
statistics. They are `23087300`, `26127150`, `26157080`, `26187170`, `26197020`, `26217050`,
`28047010`, and they are flagged in the `lt_1095_days` column of the per-gauge table.
Excluding them moves nothing material — they are 7 of 63 and split both ways.

**Robustness (reported, not a gate).** Recomputing on the raw validity mask, with no ≤3-day
gap interpolation and no ≥180-day segmentation, gives `R_AMS` **0.820**, `R_Q1` **0.840**,
`R_Q5` **0.974**. The verdict is identical under both day sets.

### 7.4 By period (§2.4: reported, but no gate reads these)

Fleet medians over gauges; `n` varies because §2.3(a) needs ≥ 300 valid days in a year and
the sub-period Q1/Q5 need ≥ 90 valid days.

| period | `R_AMS` | `R_Q1` | `R_Q5` | `R_POT` | n (AMS) |
|---|---|---|---|---|---|
| CAL 2012-14 | 0.648 | 0.863 | 0.957 | 0.423 | 46 |
| VAL all | 0.854 | 0.879 | 0.954 | 0.667 | 63 |
| VAL La Niña 11 | 0.808 | 0.894 | 0.977 | 0.500 | 48 |
| **VAL El Niño 15-16** | **0.686** | **0.744** | 0.858 | 0.464 | 39 |
| VAL other 09/10/17 | 0.794 | 0.927 | 0.958 | 0.571 | 60 |
| VAL 2018 | 0.589 | 0.744 | 0.863 | 0.375 | 34 |

Every period is below 1. **El Niño 2015-16 is the second-worst period on `R_AMS` (0.686) and
the equal-worst on `R_Q1` (0.744)**, which is consistent with everything already established
about the dry phase: skill-over-climatology −0.0005, r pinned at 0.556–0.572. 2018 is worst
of all (0.589 / 0.744), matching its VAL-2018 skill-over-climatology of −0.110.

The sub-period ordering is **not** an argument about calibration transfer: CAL 2012-14 scores
0.648 against VAL-all's 0.854, i.e. the calibration years are *worse* on peaks than the
held-out years. That is not overfitting reversed — it is a reminder that the incumbent
objective never contained a peak term, so the CAL years carry no peak advantage to lose. It
is precisely the gap §3.2's peak term exists to close.

### 7.5 Relationship to catchment area — the opposite of the correlation pattern

Areas are the model-topology `gauge_upstream_area_km2` carried in `q_gauge_H2E.npz`, not the
IDEAM catalogue areas that docs/23 §13.2 shows disagree by more than 2× on 36 % of shared
gauges. No t/km²/yr quantity is computed here, so the embargo is untouched.

| statistic | Spearman ρ vs log₁₀ area | p | n |
|---|---|---|---|
| `R_AMS` | **+0.088** | 0.49 | 63 |
| `R_Q1` | +0.027 | 0.84 | 63 |
| `R_Q5` | −0.139 | 0.28 | 63 |
| `R_POT` | −0.102 | 0.43 | 63 |
| per-gauge Pearson r (obs vs sim) | **+0.580** | **6.3 × 10⁻⁷** | 63 |
| median absolute lag | −0.224 | 0.078 | 63 |

| area tercile | n | area range (km²) | `R_AMS` | `R_Q1` | `R_Q5` | Pearson r | lag (d) |
|---|---|---|---|---|---|---|---|
| small | 21 | 68 – 288 | 0.769 | 1.001 | 1.257 | 0.530 | 4.0 |
| mid | 21 | 298 – 1,563 | 0.725 | 0.839 | 0.965 | 0.589 | 4.5 |
| large | 21 | 1,569 – 257,097 | 0.981 | 0.847 | 0.888 | 0.739 | 2.0 |

**The answer to the question as posed: peaks do NOT follow the correlation pattern.**
Correlation reproduces it emphatically — per-gauge Pearson r rises with area, ρ = +0.580 at
p = 6 × 10⁻⁷ (median r 0.530 → 0.589 → 0.739 across terciles), so the "largest catchments
correlate best" behaviour is confirmed on this data set with the same gauges and the same day
mask. Peak bias does not: ρ(`R_AMS`, area) = +0.088 at p = 0.49, indistinguishable from zero.

The tercile table hints that the largest catchments have the *least biased* peaks
(0.981 vs 0.769 and 0.725), which would make peaks weakly agree with the correlation pattern
— but the rank correlation says that is not a monotone relationship and is not significant at
n = 63, and the two largest gauges in the fleet (`29037020`, 257,097 km², `R_AMS` 1.690, and
`21237020`, 54,035 km², 1.523) over-predict badly. **Reported as measured: correlation
improves with area, peak bias does not vary with area, and the tercile medians are not
evidence to the contrary.** The honest reading is that aggregation cancels peak errors of both
signs in the median without removing them at any individual large gauge.

### 7.6 Event timing — measured, NOT pre-registered, cannot touch the verdict

Timing was not part of §2.3 and is therefore an addition made by the measuring session, with
its own choices declared: the ten largest **observed** POT events per gauge, and the lag of
the simulated maximum inside a ±15-day window (the window is this session's choice; ±10 and
±20 are reported for sensitivity). **No pre-registered gate reads any of this.**

- Median absolute lag **4 d**, fleet IQR 2–7 d; **median signed lag 0 d**, IQR −1 to +1 d —
  there is **no systematic early or late bias**, only scatter.
- Pooled over 599 events: **36.4 %** matched within ±1 d, **44.9 %** within ±2 d, **56.9 %**
  within ±5 d, and **15.2 %** land on the ±15-day window edge.
- The window-edge fraction is why the median absolute lag scales with the window (2 d / 4 d /
  6 d at ±10 / ±15 / ±20). **The absolute-lag median is therefore partly a property of the
  search window and should not be quoted as "the model is 4 days off".** The
  window-independent statements are the ones above: no signed bias, and roughly 45 % of large
  observed events have a simulated peak within two days.
- Event-matched magnitude, the strictest form of the peak question: the simulated maximum
  within ±15 d of each of the ten largest observed events is **0.552 × observed** (median over
  599 events, IQR 0.305 – 0.887). This is far worse than `R_AMS` 0.820, and the difference is
  informative rather than contradictory: `R_AMS` compares each series' *own* annual maximum,
  so the model is credited for producing a big flood at the right scale in the wrong week,
  whereas 0.552 asks whether it produced *this* flood. **For MUSLE, which multiplies event
  runoff by event peak, 0.552 is the more relevant number and the more damaging one.** It is
  recorded here as a diagnostic and is explicitly **not** substituted for the gate.

### 7.7 Propagation into sediment — the number C3 and C4 inherit

MUSLE carries peak flow as `qpeak^beta` with `beta ≈ 0.56` (Williams 1975; docs/31 §0), so a
peak ratio `R` becomes a sediment ratio `R^0.56`:

| source | `R` | `R^0.56` | implied sediment bias |
|---|---|---|---|
| **fleet-median `R_AMS` (the gate statistic)** | **0.820** | **0.895** | **−10.5 %** |
| fleet-median `R_Q1` | 0.847 | 0.911 | −8.9 % |
| El Niño 2015-16 `R_AMS` | 0.686 | 0.810 | −19.0 % |
| event-matched peak ratio (§7.6, diagnostic) | 0.552 | 0.723 | −27.7 % |

> **The one sentence C3 and C4 inherit: the measured fleet-median annual-maximum peak deficit
> of 18.0 % propagates through MUSLE's `qpeak^0.56` to an expected sediment under-prediction
> of about 10.5 %, rising to about 19 % in the El Niño 2015-16 dry phase where the peak
> deficit is deepest.**

Three qualifications that must travel with that number:

1. **It is a floor, not a total.** It counts the peak term only. `Qsur` is the other MUSLE
   driver and is tested by H-BFI, and the event-count deficit (§7.2: 43 % of events above the
   observed Q5 never occur in the simulation) is not in the `R^0.56` arithmetic at all. An
   event that does not happen contributes zero load, not `0.895 ×` its load.
2. **The direction is asymmetric across the fleet.** 18 gauges over-predict peaks by more
   than 15 %, so at those gauges the sediment bias runs the other way. A basin-total sediment
   number inherits the −10.5 %; a per-gauge sediment number inherits that gauge's own ratio,
   which the per-gauge table supplies.
3. **It bites hardest exactly where the ENSO contrast is measured.** The dry phase is both
   the phase with the deepest peak deficit (0.686) and the phase where the hydrology has no
   skill over climatology. A Niña-minus-Niño sediment contrast computed from these drivers
   will be biased *toward* a larger contrast, because the dry phase is under-predicted by
   19 % against the wet phase's 11.5 % (La Niña `R_AMS` 0.808 → 0.885).

### 7.8 Issues journalled under the §5.4 freeze rule

Each was journalled and then the frozen rule was followed unchanged.

1. The commissioning brief asked for annual maxima per **water year**; §2.3(a) specifies
   **calendar** years 2009–2018 with ≥ 300 valid days. **The calendar year was used.**
2. §2.3 says its statistics use "the same masked, paired day set as §2.1", and §2.1's data
   handling includes ≤3-day gap interpolation and ≥180-day segmentation. That reading was
   taken as primary; the raw-mask variant is in §7.3 as robustness and changes no verdict.
3. §2.1's ≥1,095-valid-day gauge exclusion is written for "the BFI statistic". It was **not**
   applied to peaks; the 7 affected gauges are named in §7.3 and flagged in the table.
4. §2.3(c) fixes the POT *independence* rule but not the *candidate* rule. Candidates were
   taken as all local maxima above the threshold, then merged pairwise while either
   independence condition failed — applied **identically to both series**, which is what
   §2.3(c)'s "applied unchanged to both series" requires.
5. Timing (§7.6) is not in the pre-registration at all and is fenced off accordingly.

---


---

## §8 — H2E-S verdict: the signature and the objective are in conflict

Read out 2026-08-11. Both seeds completed (exit 0, 156 min each, 1000 evaluations).
Reproduction check first: the recomputed peak-scale F reproduces each archived F exactly
(0.21669, 0.22689), so the evaluation below is sound before it is interpreted.

### The three pre-registered conditions (§3.3)

| condition | required | seed 20260907 | seed 20260908 | verdict |
|---|---|---|---|---|
| 1 — signature inside bound | R_AMS ∈ [0.85, 1.15] | **0.9364** | **0.9970** | **PASS** |
| 2 — no material cost in F | mean incumbent-scale F within 0.02 of 0.25931 | 0.22489 | 0.22984 | **FAIL** — mean 0.22737, Δ −0.0319 (1.6× the budget) |
| 3 — no new rails | railed ⊆ {k_sup@global, k_int_frac@global, wm_mult@R2} | kc_mult 0.975, k_int_frac 0.008 | lai_mult 0.006, k_int_frac 0.014 | **FAIL** — two new rails |

§3.3's rule, quoted: *"Anything else = signature and objective in conflict, itself
reportable, and licenses no further refit."* That is the outcome. **No further refit.**

### What the peak term actually did, and what it cost

It worked on its own terms: **R_AMS 0.820 → 0.94–1.00**, comfortably inside the band. The
annual-maximum deficit is fixable by parameters. The problem is the price.

**How it paid.** Both seeds abandoned the canopy: `lai_mult` at its floor (0.006) on one
seed, and `kc_mult` railed high again (0.975 of range ≈ 1.95) on the other. Removing
interception delivers rainfall to the soil undelayed and unbuffered — which is exactly how
you manufacture a bigger peak — and the high crop coefficient then evaporates the surplus
back out over the following days to keep the volume defensible.

**This re-breaks what H2E had just fixed.** H2E's whole purpose (docs/29) was releasing
`kc_mult` from its 2.00 rail; the FAO-56 threshold form achieved it (1.662/1.836). Adding
the peak term puts it straight back on the rail. The two objectives want opposite things
from the same parameter.

### The conclusion this forces

**The peak deficit is structural, not a calibration oversight.** A daily model cannot
represent a sub-daily flood peak; the only lever it has is to remove physical buffers, and
in a heavily forested basin setting canopy interception to zero is not a defensible way to
be right about peaks. This is the same compensating-error signature the project has caught
three times before (celerity absorbing floodplain storage; `kc` absorbing the linear ET
form; `k_int` absorbing the store ordering) — recognised here *before* it was adopted,
which is what the pre-registration was for.

### What C3 and C4 inherit

H2E remains the adopted configuration. The peak bias becomes a **named, quantified caveat**
rather than a hidden one:

- fleet-median **R_AMS 0.820** (annual maxima ~18 % low), **R_Q1 0.847**, El Niño 0.686
- **R_POT 0.567** — the model produces 1,285 independent events against 2,236 observed,
  i.e. it misses ~43 % of the flood events entirely
- propagated through MUSLE's β ≈ 0.56, the magnitude bias alone implies roughly a
  **10 % sediment under-prediction**, before the event-count deficit is considered
- therefore **C3/C4 must treat simulated sediment as a lower bound on flood-driven
  transport**, and C4's α/β must not be allowed to silently absorb it (docs/31 C3.3)

### Phase B closes for the second time

Not on exhausted headroom, and not on a clean validation either — on a **measured
conflict**. H-BFI held (with its power caveat, §6), H-PEAK is refutable and was refuted,
and the refit that would have fixed it costs more than the registered budget and undoes an
earlier gain. That is a complete answer to the question C2b asked, and it is the honest
basis on which the sediment phase proceeds.
