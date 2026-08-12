# 48 — The ±38 % Π band, replaced: σ_r is not a residual standard deviation

**Written 2026-08-11** by the `debt-b5-piband` agent (process record:
`docs/agents/journal-debt-b5-piband.md`). This document discharges repair **B5** of
`docs/47` §6.1. It does **one** job: retire the ±38 % band on Π, put a defensible band in its
place, restate the `k` bound at its corrected power, and name every published number that moves.

**Scope, stated first.** This document **does not edit `docs/42`, `docs/43` or `docs/45`.** They
are frozen; B5 is owed to them as a `docs/45` §8 amendment, enacted by that document's owner.
What is here is the measurement, the proposed replacement, and the blast radius. It also does not
edit `docs/35`, `docs/37`, `docs/46` or `docs/47`. **No frozen artifact was written; no
calibration was launched; no α̂ was fitted or quoted; no git command was run** (§7).

---

> ## THE FINDING
>
> **`σ_r = 0.465 ln` measures the disagreement between two *observers*. `docs/43` §3.2 and
> `docs/45` §2.2/§5.3/§6.2/§7 use it as the sd of the *model−observation* residual. Those are
> different quantities and the second is measured to be 2.9× – 4.2× larger.**
>
> Reproduced independently this pass, on the registered CAL window, at adopted defaults, behind
> two reproduction gates that both pass exactly:
>
> | | registered | **measured** |
> |---|---:|---:|
> | per-station residual sd, CAL 8, estimator **(b)** | 0.465 ln | **1.9618 ln** (**×4.22**) |
> | per-station residual sd, CAL 8, estimator **(a)** | 0.465 ln | **1.3506 ln** (**×2.90**) |
> | SE of the fleet-mean level, estimator (b) | 0.1644 ln | **0.6936 ln** |
> | SE of the fleet-mean level, estimator (a) | 0.1644 ln | **0.4775 ln** |
> | the 95 % band on Π | ±38 % (×0.724 – ×1.380) | **×0.29 – ×3.73** (est. b) · **×0.42 – ×2.29** (est. a) |
> | `k_min`, all-18 G1.2 joint form | 0.00216 /km ⇒ **2.12×** over 348.4 km | **0.0065 – 0.0069 /km ⇒ ≈ 9× – 11×** |
> | `k_min`, CAL-8 form | 0.0209 /km ⇒ **3.54×** over 60.4 km | **0.0838 /km ⇒ ≈ 173×** over 61.5 km |
>
> **Recommended replacement (route 2 of `docs/47` §2.2):** the **station-level bootstrap**
> that `docs/45` §4.2 already registers verbatim as the meaning of "the 95 % interval" for every
> *other* quantity in the guard set. Route 1 — promoting G12's LOO range to a band — is
> **rejected**, for two measured reasons (§3.2): it is arithmetically degenerate (the jackknife
> of the LOO refits reproduces `sd/√n` *exactly*, 0.6936 both ways), and defining the band from
> the LOO quantities makes **G12's own comparison circular**.
>
> **One consequence must be decided, not absorbed:** the ±38 % band is a *reporting* number in
> `docs/45` but a *decision* number in `docs/46`, where **0.1644 ln is the materiality bar of
> every LS hypothesis and of the Branch A/B discriminator**. Restating that bar at the corrected
> SE would declare **three of the LS levers `docs/46` exists to adjudicate immaterial**, including
> the W&S-1978 `S` lever and the `m`-cap (§5.3). **`docs/46` must decouple its bar, not rescale
> it.** This is the one place where B5 changes a verdict rather than a printed uncertainty.

---

## 1 — The defect, verified by reading before anything was computed

`docs/42` §4.2 registers:

> **REGISTERED NOISE FLOOR: σ_r = 0.465 ln units (a factor of 1.59) per station log-residual.**
> … the two independent observed-flux estimators of `docs/34` disagree by `sd[ln(a/b)] = 0.658`
> over the 32 station-windows where both are admissible, so a single estimator carries
> `0.658/√2 = 0.465`.

That derivation is **correct for what it measures**: the spread between two ways of estimating
the *observed* flux. Neither estimator has seen the model. It is an **observation-noise** figure,
and `docs/42` names it one — "noise **floor**".

`docs/43` §3.2 then writes, in the Π row of its identifiability table:

> SE of the fleet-mean level = 0.465/√8 = **0.1644 ln = ±38 % at 95 %** (0.724× – 1.380×).

and `docs/45` imports it six times (§2.2 table, §3.1, §4.2 G12's ±0.322 ln, §5.3, §6.2 item 2,
§7.1's yardstick card), `docs/37` line 1158 repeats it, and `docs/46` §2 promotes it to a
**materiality bar**.

**Those are two different quantities.** The residual whose sd the level's SE requires is
`r_i = ln(flux_sim_i) − ln(flux_obs_i)` (`docs/42` §2's own definition). Its variance contains
observation error **plus** model error **plus** genuine between-station heterogeneity. It is
bounded **below** by the observation term, never equal to it. Substituting the observation term
for the total is not a conservative approximation — it is an error in one known direction, and
`docs/47` §2.5 C-list item 3 (`docs/47` §2.6 item 3) already measured the heterogeneity term
independently: **I² 96 – 99.2 %, τ 2.03 – 3.40× per station.**

**No measurement was needed to see the category error. Every number below is needed to size it.**

---

## 2 — (a) Independent reproduction

### 2.1 Method, stated so it can be re-run

Nothing below is transcribed from a prior pass. The chain is:

1. `mgb_sediment.load_drivers('sim_calibrated_v2/h2e_drivers.npz')` (read-only) →
   `load_geometry(..., mini_ids=DRV.mini_ids)` at the adopted `cp_revision` and `ls2d_column`
   → `simulate_sediment(GEOM, SedParams(), ...)`. **No default changed. No parameter fitted.**
2. Station flux = the topological upstream sum of `delivered_t_day`, walked over
   `topology.npz:downstream_idx` in `topo_order_idx`. At the registered `k = 0.0 /km` and
   `tau_channel_days = 0` this *is* the model's station flux.
3. Observed flux rebuilt from `sediment_daily_qc.csv` + `discharge_daily.csv` +
   `ssc_rating_fits.csv` by re-implementing `scripts/c2_compute.py`'s two estimators —
   **(a)** sample-day flux mean, **(b)** per-era Duan-smeared rating flux — on the **registered
   CAL window 2012-01-01 … 2014-12-31** instead of on the four ENSO windows.
4. `r_i = ln(mean sim) − ln(mean obs)`, **means over the same day set**, per `docs/42` §2.

> **A trap, recorded because it silently produces a plausible wrong number.**
> `topology.npz:topo_order_idx` is **the ordered list of indices** (headwater-first), *not* the
> rank of each index. Accumulating over `np.argsort(topo_order_idx)` gives a partial sum that
> looks sane per station and is wrong. The control that catches it in one line is
> `acc[:, outlet_idx] == Σ_j E_j` — **rel err 1.000 before the fix, 0.000 after.** Keep it.

### 2.2 The two reproduction gates

| gate | required | **measured** |
|---|---|---|
| basin gross hillslope erosion, adopted convention | `docs/37` A1.3.4: **299.5387 Mt/yr** | **299.5387088 Mt/yr**, mass ledger `exact = True` |
| CAL-8 paired SSC + observed-Q day count | `docs/45` §3.6 / `docs/47` §2.1: **3,266** | **3,266** |

Model up-areas reproduce `docs/42` §4.1's printed column at **all 18** stations (54,035 /
30,848 / 24,665 / 6,380 / 6,362 / 5,487 / 2,411 / 1,711 / 1,645 / 1,600 / 833 / 748 / 723 / 611 /
289 / 178 / 152 / 68 km²), so the station→minibacia mapping is not in question.

### 2.3 The per-station residuals

CAL window 2012–14, estimator (b), at `α = 11.8`, `β = 0.56` (unfitted defaults):

| station | | `n` days | obs t/day | sim t/day | `r_i` = ln(sim/obs) | obs/sim |
|---|---|---:|---:|---:|---:|---:|
| `26127010` | EL ALAMBRADO AUT | 287 | 3,053.15 | 748.95 | **−1.4053** | 4.0766 |
| `23127010` | BORBUR - AUT | 1,096 | 7,121.30 | 10,305.28 | +0.3696 | 0.6910 |
| `24037390` | CAPITANEJO | 727 | 3,260.64 | 12,110.41 | +1.3121 | 0.2692 |
| `22017030` | BOCAS | 963 | 34.36 | 183.73 | +1.6765 | 0.1870 |
| `26137110` | BANANERA LA 6-909 | 1,004 | 32.49 | 226.50 | +1.9418 | 0.1435 |
| `21197010` | EL PROFUNDO | 1,093 | 81.23 | 1,184.10 | +2.6795 | 0.0686 |
| `24027030` | NEMIZAQUE | 771 | 43.99 | 2,937.95 | +4.2016 | 0.0150 |
| `22017010` | BOCAS | 1,095 | 107.36 | 10,853.27 | **+4.6161** | 0.0099 |

**Range 6.0214 ln — a factor of 412.1 in obs/sim across eight stations.**
(`21237020` ARRANCAPLUMAS +1.7495 and `26017060` PUENTE ARAGÓN +4.3273 also have CAL-window
observations but are EVAL stations, `docs/45` §2.4.)

### 2.4 The result, on every admissible construction

| set / window / estimator | `n` | **sd(r) ln** | ×σ_r | **SE = sd/√n** | ×0.1644 |
|---|---:|---:|---:|---:|---:|
| **CAL 8 / CAL window / (b)** — `docs/42` §9's registered primary | 8 | **1.9618** | **4.22** | **0.6936** | 4.22 |
| **CAL 8 / CAL window / (a)** — `docs/45` §7.1's objective estimator | 8 | **1.3506** | 2.90 | **0.4775** | 2.90 |
| CAL 8 / CAL window / (a), C1.2-compliant (EL ALAMBRADO dropped) | 7 | 1.3539 | 2.91 | 0.5117 | 3.11 |
| all with CAL-window data / (b) | 10 | 1.8930 | 4.07 | 0.5986 | 3.64 |
| all 18 / ENSO-window medians / (b) — the G1.2 basis | 16 | 1.4175 | 3.05 | 0.3544 | 2.16 |
| all 18 / ENSO-window medians / (a) | 16 | 1.2217 | 2.63 | 0.3054 | 1.86 |
| CAL 8 / ENSO-window medians / (b) | 8 | 1.7159 | 3.69 | 0.6067 | 3.69 |

**The two headline numbers `docs/47` §2.2 reports — 1.9618 ln and 0.6936 ln — reproduce
exactly.** So do the earlier passes' ENSO-window figures (1.7159 / 1.4175 against their reported
1.7118 / 1.4202, 0.2 %) and the factor-412 spread.

**And one number that was not asked for reproduces exactly too, which matters because it is a
*different* finding:** the geometric mean of the per-station obs/sim ratios under estimator (a)
over the CAL 8 is **0.07603 ⇒ implied α = 11.8 × 0.07603 = 0.8971**, against `docs/47` §2.1's
**0.0760 ⇒ α 0.897**. **`docs/47` D1's level measurement is independently confirmed by this
pass.** (Under estimator (b) the same statistic is 0.1460 ⇒ α **1.723**.)

> **Verdict on (a): the defect is real, it is larger than 3.9–4.2× under estimator (b) and
> 2.9× under estimator (a), and it is present on every station set, every window construction
> and both estimators. There is no admissible construction on which σ_r = 0.465 is the residual
> sd.**

### 2.5 Two honest disagreements found on the way, neither of which changes the verdict

1. **`Lw` does not reproduce `docs/42` §4.1's printed table.** Recomputed from
   `topology.npz:path_km_to_outlet` weighted by the model's own per-minibacia erosion (docs/42
   §2's formula, at the **adopted** `cp_revision`): IRRA **289.14** vs 265.2 (+9.0 %), BANANERA
   **24.19** vs 26.9, CAPITANEJO **64.15** vs 60.4, CARRASPOSO **36.18** vs 39.0, ARRANCAPLUMAS
   **344.21** vs 348.4. This independently reproduces `journal_refute-gate-logic`'s IRRA 289.1 to
   4 s.f. **Immaterial to every conclusion here** — `k_min` moves ≤ 2 % between the two `Lw`
   tables, and every result below is reported on **both**. Reconciliation is owed to whoever owns
   §4.1; the most likely cause is that §4.1 was measured at the **prior** `cp_revision`
   (its own §4 header records basin total 248.696 Mt/yr).
2. **The land-class erosion shares also differ from `docs/42` §4.1** for the same reason —
   e.g. BANANERA Forest/Grass/Bare measured **26.0 / 24.5 / 49.5 %** against the printed
   11.9 / 12.5 / 75.6 %, CAPITANEJO **4.4 / 62.0 / 31.9** against 2.4 / 37.9 / 58.4. `docs/41`'s
   ×1.2043 `C` revision is not uniform across classes, so it moves shares. Recorded here because
   G3.1's regressors are read off that table; **not a B5 finding and not corrected here.**

---

## 3 — (b) The replacement band

### 3.1 What the band is a band *on*, stated exactly

The registered construction is one formula:

```
SE(level) = sd(per-station log residual) / sqrt(n)          band = ± 1.96 · SE
```

**This document changes the `sd` and nothing else.** Same estimator of the level (the fleet mean
of per-station log residuals over window means), same `n`, same 95 %. That is the strongest form
the correction can take: it is not a new statistic, it is the registered statistic evaluated on
the quantity its own name says it is.

**The band is invariant to the fit; the point is not.** Fitting Π removes a constant from every
`r_i`, which moves the mean to ≈ 0 and leaves the sd — hence the SE, hence the band — untouched.
So the band measured here at `α = 11.8` is the band that will travel with whatever Π̂ C4 returns.
(`docs/47` §2.2 states the same thing; it is what makes a pre-fit registration of the band legal.)

### 3.2 Why route 1 — G12's LOO range as a band-replacement rule — is REJECTED

`docs/47` §2.2 names two routes. Route 1 fails on two measurements.

**(i) It is arithmetically degenerate.** For a mean, the jackknife standard error is *identically*
`s/√n`, and the LOO range is *identically* `range(r_i)/(n−1)`. Measured, to confirm the algebra
rather than assume it: jackknife SE **0.6936** = `sd/√n` **0.6936**; LOO range **0.8602** =
6.0214/7 **0.8602**. So route 1 delivers either (a) exactly the corrected-σ normal band, in which
case it is that band under another name, or (b) a *range*, which is not an interval — and turning a
range into a 95 % band requires a conversion constant that this repository cannot cite.
**`docs/40` retired one uncited band and `docs/47` §8 refuses to invent another; this one would be
invented.**

**(ii) It destroys G12.** G12's entire content is the comparison *LOO range vs the level band*. If
the band is defined from the LOO quantities the comparison is circular. Measured:

| band | full width | vs LOO range 0.8602 | G12 |
|---|---:|---|---|
| registered ±0.322 ln (σ_r/√8) | 0.6445 | 0.8602 > 0.6445 | **FIRES** |
| ±1.96·SE at the measured sd | 2.7190 | 0.8602 < 2.7190 | does **not** fire |
| station bootstrap (route 2) | 2.5667 | 0.8602 < 2.5667 | does **not** fire |

> **This is the single most important operational consequence of B5 and it must not be absorbed
> silently: correcting the band switches G12 off.** Under the registered band G12 fires (that is
> `docs/47` §2.2's "G12 already fires on it"); under **either** corrected band it does not.
>
> **Recommendation, for the `docs/45` §8 amendment:** keep G12's **0.644 ln full width as a
> standalone registered fragility threshold**, decoupled from the level band, and record that it
> was originally derived from σ_r/√8. Its diagnostic content survives the correction and is
> worth keeping: **an LOO range of 0.8602 ln means that deleting one of the eight CAL stations
> moves the fitted level by up to a factor of `exp(0.8602)` = 2.36×.** That statement is true,
> measured, and is exactly what G12 was written to surface. Re-pointing G12 at the new band would
> convert a firing guard into a silent one **by widening the thing it is compared against**,
> which is the shape of every gate failure this project has already refused.

### 3.3 The recommended replacement — route 2, the station bootstrap

> ## REGISTERED PROCEDURE (proposed for `docs/45` §8)
>
> **The 95 % band on Π̂ is the station-level bootstrap of the fleet-mean per-station log
> residual: resample the CAL stations with replacement 10,000 times, recompute the fleet mean
> inside each resample, take the 2.5 / 97.5 percentiles.** This is `docs/45` §4.2's **already
> registered** interval convention — *"a station-level bootstrap … station resampling, not day or
> pair resampling"* — imported unchanged from `docs/42` §6 and applied to the level, which is
> currently the only quantity in the guard set on a bespoke normal-theory formula.
>
> **The band is a procedure, not a constant.** C4 recomputes it on its own adopted fit's
> residuals and reports what it gets. The numbers below are what the procedure evaluates to at
> the unfitted defaults on the registered CAL window, and are registered here as the pre-fit
> expectation so that a materially different C4 number is itself reportable.

Measured (seed 20260810, 10,000 station resamples):

| estimator | point (ln) | bootstrap CI about the point | **band on the level** | normal ±1.96·SE, for comparison |
|---|---:|---|---|---|
| **(a)** — `docs/45` §7.1's objective estimator | +2.5772 | [−0.8279, +0.8721] ln | **×0.418 – ×2.289** | ±0.9359 ln ⇒ ×0.392 – ×2.550 |
| **(b)** — `docs/42` §9's registered primary | +1.9240 | [−1.3163, +1.2503] ln | **×0.286 – ×3.730** | ±1.3595 ln ⇒ ×0.257 – ×3.894 |

*(`docs/47` §2.2's "0.257× – 3.894×" is the normal band under estimator (b); it reproduces
exactly. The bootstrap is marginally narrower and, unlike the normal band, **asymmetric**, which
is the honest shape for a log-space level at n = 8.)*

**Which one travels with a number.** The two registered estimators do not agree on the *width*,
and `docs/45` §6.1 already makes estimator disagreement an **INDETERMINATE** trigger for
*verdicts*. For a *band* the conservative reading is the union:

> **RECOMMENDED, as a reporting convention and explicitly not a statistical claim:
> the band quoted with every Π and every load is the UNION over the two registered estimators,**
> ```
> Pi_hat  x  [0.29, 3.73]        (95 %, station bootstrap, union of estimators (a) and (b))
> ```
> **and the sentence `docs/47` §6.2 item 3 requires appears beside it, now with its measured
> value: *"the level is set by 8 stations whose residuals span a factor of 412."*** (Measured:
> 412.1.)

Two further numbers, reported so the choice is auditable and not adopted here:

- **If the level is read off `F_report` (a median over 8 stations, `docs/45` §3.2) rather than a
  mean**, the bootstrap band is wider still: point median +1.8092 ln, CI about the point
  [−1.4396, +2.3925] ⇒ **×0.091 – ×4.219**. It is jagged by construction at n = 8 and is
  **reported, not recommended**.
- **The band is β-dependent.** `journal_refute-gate-logic` measured CAL-8 est-(b) sd rising
  monotonically 1.875 → 2.100 across the registered β box [0.40, 0.75]. This is a second reason
  the amendment must register the **procedure** and not a frozen pair of numbers.

### 3.4 What the replacement does and does not change

- **It changes no `docs/45` §6.1 outcome.** ADOPT / FAIL-STRUCTURE / FAIL-NUMERIC / FAIL-RAILED
  are defined on `F_report`, on the guards and on the boxes. **None of the eight ADOPT conditions
  reads the level band.** The band is a reporting number in `docs/45`.
- **It changes G12's firing state** (§3.2) — handle explicitly.
- **It changes ten occurrences in `docs/46`, where the same number is a decision threshold and
  not a report** (§5.3) — that is the only place a *verdict* moves.
- **It does not rescue anything.** A wider band is a weaker claim. The corrected band spans a
  factor of **13.0** (est. b) where the registered one spanned **1.91**. Nothing that failed
  passes because of it.

---

## 4 — (c) The `k` bound, restated at its corrected power

### 4.1 The registered bound and where it comes from

`docs/45` §2.3 and G1.2 register the sentence C4 must print:

> *"no first-order channel sink stronger than X× over Y km is detectable on this fit set"* …
> **≈ 2.12× over 348.4 km at best** (all-18 test, `k_min` 0.00216 /km).

`docs/42` §9.5 (amendment A-P1.1, 2026-08-11) re-affirms 0.00216 /km unchanged and states the
mechanism explicitly: `k_min = 1.96 · σ_r / sqrt(Σ_i (Lw_i − L̄)²)`. **Every `k_min` in the
corpus is linear in σ_r.** That is why B5 moves them all.

### 4.2 The corrected bound, measured

G1.2 is registered as a **joint** regression (`docs/42` G1 note 3; `docs/45` §4.2 G1.2 —
"fitted **jointly** with G3.1 and G4.1 as one multiple regression"), on **all 18**, whose only
available all-station residual set is the ENSO-window construction. Fitted here on recomputed
predictors (`Lw`, class erosion shares, erosion-weighted `ln LS̄` — all rebuilt from
`SedResult.cell_eroded_t` and `topology.npz`, none transcribed):

| model | resid sd (ln) | df | SE(k̂) /km | **`k_min` = 1.96·SE** | **contrast over 341.5 km** |
|---|---:|---:|---:|---:|---:|
| intercept only | 1.4175 | 15 | — | — | — |
| `+ Lw` (G1.2 alone) | 1.4568 | 14 | 0.00340 | 0.00666 | **9.74×** |
| `+ shG, shB` (G3.1) | 1.4347 | 12 | 0.00335 | 0.00657 | 9.42× |
| **`+ ln LS̄` (G4.1) — the registered joint form** | **1.4955** | 11 | **0.00350** | **0.00686** | **10.41×** |

By `docs/42` §4.2's own univariate formula, on **its own printed `Lw` table** (span 345.8 km), at
the same joint-form residual sd: `k_min` **0.00694 /km ⇒ 11.02×**; at the intercept-only sd,
**0.00658 /km ⇒ 9.72×**.

> ## THE CORRECTED SENTENCE
>
> ```
> k_min  =  0.0065 - 0.0069 /km        (all 18, G1.2 joint form, measured residual sd)
> ```
> > **"No first-order channel sink weaker than ≈ 10× over ~342 km is detectable on this fit
> > set."**  *(equivalently: `|k| < 0.0069 /km` cannot be distinguished from zero)*
>
> **Registered: 2.12× over 348.4 km. Corrected: ≈ 9× – 11×, central ≈ 10×.**
> `docs/47` §2.6 item 2 and §6.2 item 4 already state "~10× over 342 km"; **this pass confirms it
> from an independent recomputation** and supplies the interval and the design matrix.
>
> **A phrasing defect, flagged not fixed:** `docs/42` G1.2 and `docs/45` §2.3 write *"no sink
> **stronger** than X× … is detectable"* while `docs/45` §2.2 writes *"no sink **weaker** than
> 3.54× is detectable"*. Only the second is the correct sense of a detection floor. Whoever
> enacts the amendment should settle on one.

### 4.3 The CAL-8 form, and a number in `docs/47` that does not reproduce

| form | registered | **measured at the corrected σ** |
|---|---:|---:|
| CAL 8, recomputed `Lw` (span 61.5 km) | 0.02092 /km ⇒ 3.54× | **0.0838 /km ⇒ 173×** |
| CAL 8, `docs/42` printed `Lw` (span 57.8 km) | 0.02092 /km ⇒ 3.54× | **0.0883 /km ⇒ 164×** |

The ratio 0.0838 / 0.02092 = **4.006** against the sd ratio 1.9618 / 0.465 = **4.219** — the
small difference is entirely the recomputed-vs-printed `Lw` (§2.5), confirming the bound is
linear in σ as `docs/42` §9.5 states.

> **NEGATIVE RESULT, reported plainly.** `docs/47` §2.2's table row *"`k_min`, CAL-8 form …
> **0.0130 /km** on the CAL window form"* **does not reproduce, and it is arithmetically
> impossible as labelled.** `k_min ∝ σ/√Sxx`; on a fixed station set a σ **4.22× larger** cannot
> yield a `k_min` **smaller** than the registered 0.0209. Traced: **0.0130 is the 10-station set
> that happens to have CAL-window observations, which includes `21237020` ARRANCAPLUMAS** —
> measured **0.01230 /km**, and ARRANCAPLUMAS alone supplies **87.6 %** of that set's `Σ(Lw−L̄)²`.
> Removing it: **0.0799 /km**. **ARRANCAPLUMAS is an EVAL station that `docs/45` §2.4 registers
> out of the fit**, so a "CAL-8 form" containing it is mislabelled either way.
>
> **This matters beyond `docs/47`, because `docs/42` §9.5's MANDATORY POINTER has already copied
> the number** (`docs/42`:804, "*a corrected CAL-8 form of **0.0130 /km***"). The corrected CAL-8 figure is
> **0.0838 /km (≈ 173× over 61.5 km)**. `docs/42` §9.5's all-18 figures (0.0066–0.0069 /km,
> ≈ 10× over 342 km) are **confirmed**.

### 4.4 What the corrected bound means for `docs/45` §2.3's registered claim

`docs/45` §2.3 fixes `k = 0.0 /km` and discharges `docs/42` G5 by stating, as a claim,
*"this model asserts SDR = 1.0 between hillslope and station."* G5's second leg is `k̂` with its
interval in the same table as α. **That leg is unaffected in form and gutted in content:** the
guard that would betray the SDR = 1.0 claim cannot see any sink weaker than ~10× over the basin's
longest observed path. **The claim stands as a claim; the evidence for it is measured to be
weaker than registered by 3.18× in `k` (0.00216 → 0.00686 /km) and 4.91× in the survival contrast
the registered sentence actually prints (2.12× → 10.41×).** `docs/47` §2.6 item 2 already requires the corrected bound travel with it; §6.2 item 4 fixes the words.

---

## 5 — (d) The blast radius: every number that becomes wrong

Grouped by what has to happen to it. **File:line references are as of 2026-08-11**; `docs/42` was
amended earlier the same day by the `debt-b4-transcription` pass, so its §9 numbering is current.

### 5.1 MUST CHANGE — the level band and its derivatives

| # | number | where | replacement |
|---|---|---|---|
| 1 | `SE of the fleet-mean level = 0.465/√8 = **0.1644 ln = ±38 % at 95 %** (0.724×–1.380×)` | `docs/43`:191 (§3.2 Π row) | SE **0.4775** (est. a) / **0.6936** (est. b); band **×0.29 – ×3.73** |
| 2 | `SE of the fleet-mean level | **0.1644 ln = ±38 % at 95 %** (0.724×–1.380×)` | `docs/45`:124 (§2.2) | as above |
| 3 | `SE of the fleet level = **0.1644 ln**` | `docs/45`:252 (§3.1) | as above |
| 4 | `C4 reports the fitted Π, **its ±38 % band**` | `docs/45`:494 (§5.3) | the station-bootstrap band (§3.3) |
| 5 | `**The level's band is ±38 %** (0.724×–1.380×; SE 0.1644 ln at n = 8). Every Π and every load is quoted **with that band**` | `docs/45`:541 (§6.2 item 2) | **the mandatory sentence itself changes.** This is the headline; it is the one place `docs/47` §2.2 notes carries **no hedge** |
| 6 | `level SE **0.1644 ln (±38 %)**` | `docs/45`:575 (§7.1 card) | as above |
| 7 | `the registered 95 % level band of **±0.322 ln (±38 %)**` | `docs/45`:445 (G12) | **decide, do not rescale** (§3.2): recommend retaining 0.644 ln full width as a standalone fragility threshold |
| 8 | `SE = 0.465/√8 = **0.1644 ln = ±38 % at 95 %**` | `docs/37`:1158 (A2.4) | as above; `docs/37` is closed to this pass, so this is a pointer, not an edit |
| 9 | `13 stations would have given **±28.8 %**` | `docs/43`:191, `docs/45`:124 | derived from the same σ_r ⇒ also wrong. **No corrected value is offered** — the 13-station residual set does not exist (only 8 have CAL-window paired days at all) |

### 5.2 MUST CHANGE — every `k_min` and every survival contrast

All are `∝ σ_r`. `docs/42` §9.5 already carries a pointer for the first two rows; the rest do not.

| # | number | where | corrected |
|---|---|---|---|
| 10 | all-18 `k_min` **0.00216 /km ⇒ 2.12×** over 348.4 km | `docs/42`:231, :671, :796; `docs/43`:193; `docs/45`:162, :202, :429 | **0.0065–0.0069 /km ⇒ ≈ 9×–11×**, central **≈ 10× over ~342 km** |
| 11 | CAL-8 `k_min` **0.02092 /km ⇒ 3.54×** over 60.4 km | `docs/42`:692, :700-701, :742, :795; `docs/43`:193; `docs/45`:126, :205 | **0.0838 /km ⇒ ≈ 173×** over 61.5 km (0.0883 ⇒ 164× on `docs/42`'s `Lw`) |
| 12 | CAL-13 `k_min` **0.00964 /km** (was 0.0104) ⇒ 2.83× / 2.90× | `docs/42`:744, :798 (A-P1.1) | σ_r-scaled ⇒ wrong. **No corrected value offered**: a CAL-13 residual set does not exist (only 8 of the 13 have a CAL-window paired day at all — that is what A-P1 records). The row is already SUPERSEDED by A-P1; **flag, do not recompute** |
| 13 | 22-pair `k_min` **0.00119 /km ⇒ 1.51×** | `docs/42`:232, :797 | σ_r-scaled ⇒ wrong. **No corrected value offered** — the pair list is not printed anywhere and `Σ(ΔLw−ΔL̄)²` cannot be rebuilt from the documents. **Open item.** |
| 14 | CAL 8 + ARRANCAPLUMAS `k_min` **0.00303 /km ⇒ 2.87×/2.88×**, and the **factor 6.9** cost of the P2 decision | `docs/42`:692, :799; `docs/43`:193; `docs/45`:205 | **measured on that 9-station set's own CAL-window residuals (sd 1.8361): `k_min` = 0.01210 /km ⇒ 62.4× over 341.5 km.** The **factor 6.9** becomes **6.9 (0.0838/0.01210)** — it is a *ratio* of two σ-scaled numbers and **survives**; stated so it is not over-corrected |
| 15 | `k_min` **0.0130 /km** attributed to the "CAL-8 form" | `docs/47`:148; **copied into `docs/42`:805 (§9.5 pointer)** | **withdrawn** — it is the 10-station CAL-window set including ARRANCAPLUMAS (measured 0.01230). Correct CAL-8 value **0.0838 /km** (§4.3) |
| 16 | `k_min` 0.0209 → *"2.2× worse than `docs/42` assumed, **9.7×** worse"* | `docs/37`:1155 | both are **ratios of σ_r-scaled numbers** and **survive unchanged**. Recorded so this line is not "corrected" by mistake |

### 5.3 MUST BE DECIDED — `docs/46`, where 0.1644 is a decision threshold, not a report

`docs/46` §2 adopts `|ln f_A − ln f_B| > 0.1644` as **the materiality bar used by every LS
hypothesis**, and §6.1 uses the same number as the **Branch A / Branch B discriminator**
(`Δ_shape ≤ 0.1644` ⇒ C4.3 may start provisionally). **Ten occurrences:** `docs/46`:138 (the bar),
:140-142 (its derivation), :189 (H-M's **R4**), :217 (the `S`-lever level clause), :240 (the joint
cell's consistency bar), :265 (H-L's refutation condition), :490-491 (the `Δ_shape` branch table),
:506 (Branch A's precondition), :538 (**B1**).

**`docs/46`'s derivation is sound and its value is not:** *"a difference in the LS level smaller
than the standard error of the only fit that will ever consume it cannot change any downstream
statement."* Correct. But the standard error is 2.9×–4.2× larger than the number substituted into
it. Measured consequence, on the LS levers `docs/46` and `docs/47` §4.3 have already quantified:

| LS lever | factor | \|ln f\| | bar 0.1644 | 0.4775 (SE, est a) | 0.6936 (SE, est b) | 0.8500 (boot, a) | 1.2833 (boot, b) |
|---|---:|---:|:--:|:--:|:--:|:--:|:--:|
| erosion- vs area-weighting of the scalar proxy (R7) | 1.0251 | 0.0248 | — | — | — | — | — |
| the refuted ×0.790 DG/continuous ratio (R6) | 0.790 | 0.2357 | **MATERIAL** | — | — | — | — |
| `S` → Wischmeier & Smith 1978 | 1.6941 | 0.5272 | **MATERIAL** | **MATERIAL** | — | — | — |
| DG `L` / continuous `L` inside the source formulation | 0.5807 | 0.5435 | **MATERIAL** | **MATERIAL** | — | — | — |
| `m` capped at 0.5 | 0.5175 | 0.6587 | **MATERIAL** | **MATERIAL** | — | — | — |
| source method, continuous `L` (`f_LS` upper endpoint) | 0.43194 | 0.8395 | **MATERIAL** | **MATERIAL** | **MATERIAL** | — | — |
| slope length ≤ 1 pixel | 0.3624 | 1.0150 | **MATERIAL** | **MATERIAL** | **MATERIAL** | **MATERIAL** | — |
| source method, Desmet–Govers `L` (`f_LS` lower endpoint) | 0.25146 | 1.3805 | **MATERIAL** | **MATERIAL** | **MATERIAL** | **MATERIAL** | **MATERIAL** |

> **RECOMMENDATION — and it is the one place where B5 changes an outcome rather than a printed
> uncertainty. `docs/46` must DECOUPLE its materiality bar from the fit's standard error, not
> restate it at the corrected value.**
>
> At the corrected estimator-(b) SE (0.6936 ln = a factor of **2.001**) the bar declares a
> **factor-two** LS lever "immaterial" — including three of the levers `docs/46` was written to
> adjudicate. At the corrected bootstrap half-width it declares **all but one endpoint of the
> whole `f_LS` bracket** immaterial. A pre-registration whose materiality bar is wide enough to
> swallow its own subject cannot decide anything.
>
> **What survives either way, so the negative is bounded:** the measured `f_LS` bracket endpoints
> (|ln| 0.8395 and 1.3805) remain material at both corrected **SE** bars. **`docs/47` §4.3's
> bracket `f_LS ∈ [0.25146, 0.43194]` and §5's BLOCKED-UNTIL-LS-LANDS verdict are not weakened by
> B5.** What is weakened is `docs/46`'s ability to adjudicate the *individual levers* and its
> Branch A/B discriminator.
>
> This document does **not** propose a replacement bar. Inventing one would be exactly the move
> `docs/40` retired the SDR band for. **`docs/46` §6.1's `Δ_shape` pre-test has still not been
> run (`docs/47` O6); it should be run and its number recorded before the bar is re-chosen, so
> the bar cannot be picked to produce a branch.**

### 5.4 DOES **NOT** CHANGE — stated so nothing is over-corrected

| number | where | why it survives |
|---|---|---|
| **σ_r = 0.465 ln itself, as an estimator-disagreement statistic** | `docs/42`:216-220, :598 | The derivation `0.658/√2` is correct for what it measures. **It is the *reuse* that is retired, not the number.** |
| **pair-σ = 0.658 ln** and G1.1's `D_pair > +0.658` firing threshold | `docs/42`:349, :549; `docs/45`:398, :428 | a firing threshold; the error makes it **more** trigger-happy (`docs/47` R4) |
| **G8's 0.465 ln** seasonal range; **G11's 0.465 ln** regional difference | `docs/42`:524; `docs/45`:441, :444 | same — thresholds, erring in the safe direction. **But see the caution below.** |
| **`b_obs` between-station IQR = 0.464** | `docs/42`:598; `docs/45`:398 | independently measured from `ssc_rating_fits.csv`; the near-equality with 0.465 is a coincidence of value |
| **SE(β) = 0.0199**, half-width 0.039 | `docs/43`:191; `docs/45`:124, :575 | built on σ_day = 0.809 ln (the rating residual), not σ_r |
| **the ratios** 2.2× / 9.7× / 6.9× between two σ_r-scaled `k_min` values | `docs/37`:1155; `docs/42`:692; `docs/45`:205 | σ_r cancels |
| every `docs/45` §6.1 outcome condition | `docs/45`:530-534 | none of the eight ADOPT conditions reads the level band (§3.4) |

> **CAUTION on the "errs safe" row, and it is not a correction.** `docs/47` R4 is right that a
> threshold set 4× too tight makes G8 and G11 *more* likely to fire. The measured residual scale
> makes that near-certain: the fleet's per-station residual sd is 1.35–1.96 ln, so a
> between-month or between-region difference of 0.465 ln is well inside ordinary sampling noise
> at n = 8. **A guard that fires by construction is not a test either.** No number is offered and
> nothing is proposed — G8 and G11 are frozen thresholds and this pass has no standing to touch
> them. It is recorded so that a G8 or G11 FAIL is read for what it is.

### 5.5 Also owed

- **`docs/00_INDEX.md` §3** has no row for `docs/42`'s §9 amendment log, none for `docs/47`, and
  none for this document. Its `docs/42` row should gain "*σ_r's reuse as a residual sd retired by
  `docs/48`*". (`docs/42` §9.6 F6 already raises the first half.)
- **`docs/47` open item O8** — the class-C detectability figures ×4.2 (CAL 8) / ×2.9 (all 18) at
  `docs/43`:193 and `docs/45` G3.3 are σ_r-scaled and therefore also wrong. §6.2 below contributes
  a measurement but **does not close O8**.

---

## 6 — What this document could NOT settle

### 6.1 Named open items

| # | open item | what would settle it |
|---|---|---|
| **P1** | **Which estimator's band is binding.** `docs/42` §9 registers **(b)** as the primary; `docs/45` §7.1 registers the objective on **(a)**. They give bands differing by a factor of **1.51** in log width (2.5667 vs 1.7001 ln). §3.3 recommends the union as a convention and declines to decide the registration question. | A decision by `docs/45`'s owner, in the §8 amendment. |
| **P2** | **The 22-pair `k_min` 0.00119 /km** cannot be corrected — the pair list is printed in no document and `Σ(ΔLw − ΔL̄)²` is not reconstructible from what is published (§5.2 row 13). | Publishing the 22 pairs with their ΔLw, or recomputing G1.1's design from `topology.npz`. |
| **P3** | **`docs/42` §4.1's `Lw` table and land-class shares do not reproduce** (§2.5). Probable cause: measured at the prior `cp_revision`. Immaterial here (≤ 2 % on `k_min`) but G3.1's regressors are read off it. | A recomputation at the adopted `cp_revision`, by `docs/42`'s owner. |
| **P4** | **What `docs/46`'s materiality bar should be** (§5.3). This document establishes that the current value is wrong and that the corrected value is unusable. It offers **no** replacement, on purpose. | Running `docs/46` §6.1's `Δ_shape` pre-test first (`docs/47` O6), then a source-grounded choice. |
| **P5** | **Whether the band should be computed on the fitted residuals of the adopted β** rather than at β = 0.56. The sd is measured to rise monotonically 1.875 → 2.100 across the registered β box. §3.3 registers the procedure so C4 recomputes it; the pre-fit numbers here are an expectation, not the deliverable. | C4.3, once it is unblocked. |

### 6.2 An O8 contribution, clearly labelled as such

`docs/43` §3.2 and `docs/45` G3.3 register "minimum detectable class-C error ≈ **×4.2** on the
CAL 8 (≈ **×2.9** on all 18)". `journal_refute-gate-logic` could not reproduce those on its own
design matrix (it obtained ×8.2 / ×3.2) and therefore offered no correction. **Nor can this
pass** — a third design matrix gives a third answer. Reported with the matrix stated, so the next
attempt has something to compare against:

Design matrix `[1 | Lw | share_Grassland | share_Bare | ln LS̄]`, Forest the reference class,
"minimum detectable" = `exp(1.96 · SE(coef))` across the full 0 → 1 share range:

| set | σ used | resid sd | df | min. detectable `c_G` | min. detectable `c_B` |
|---|---|---:|---:|---:|---:|
| all 18, ENSO medians, est (b) | registered 0.465 | 1.4955 | 11 | ×5.58 | ×3.53 |
| all 18, ENSO medians, est (b) | **measured** | 1.4955 | 11 | **×251.6** | **×57.9** |
| CAL 8, CAL window, est (b) | registered 0.465 | 2.1103 | 3 | ×21.6 | ×8.3 |
| CAL 8, CAL window, est (b) | **measured** | 2.1103 | 3 | *(degenerate, df = 3)* | *(degenerate)* |

**Three different passes have now produced three different numbers for this quantity. O8 stays
open.** What all three agree on, and what is the only thing that should be quoted: **the class-C
contrasts are σ_r-scaled, the registered ×4.2 / ×2.9 are too optimistic by roughly the σ_r
factor, and G3.1 could not have seen `docs/41`'s ×1.2043 revision** — which `docs/45` G3.3 already
registers in advance, and which no correction here changes.

### 6.3 Explicitly not settled, and not attempted

- **The level itself.** This document measures the *width* of the band, not where its centre
  belongs. `docs/47` §2.1's D1 is confirmed as a by-product (§2.4) and is otherwise untouched.
- **Whether C4.3 may start.** `docs/47`'s verdict `C4.3-BLOCKED-UNTIL-LS-LANDS` is unchanged.
  B5 is listed there as "*owed before any C4 number is printed*", in parallel with B1–B4, and
  §5.3 above adds one reason the ordering matters.
- **Anything about `docs/40`'s retired SDR band.** The uncited 0.05–0.30 band and its implied
  `k ≈ 0.0020–0.0032 /km` are named in `docs/42` §4.2 as scale reference only. **The corrected
  `k_min` of 0.0065–0.0069 /km now sits *above* that whole range**, where the registered 0.00216
  sat inside it. Recorded because `docs/42` §4.2's sentence *"the 18-station test's 0.00216 /km
  sits inside the range that matters"* is a consequence of the wrong σ. **It passes and fails
  nothing** — the band is uncited and remains so.

---

## 7 — Disclosure

- **Files written by this pass:** `docs/48_pi_band_revision.md` (this file) and
  `docs/agents/journal-debt-b5-piband.md`. **Nothing else in the repository.**
  `docs/35`, `docs/37`, `docs/42`, `docs/43`, `docs/45`, `docs/46` and `docs/47` were read and
  **not edited**.
- **No frozen artifact was opened for writing.** `sim_calibrated_v2/{h2e_drivers.npz,
  parameters_H2E.csv, q_gauge_H2E.npz}` were read read-only. `data/processed/urh_ls2d.csv` and
  `minibacia_ls2d.csv` were read, never written. `scripts/c3/ls2d.py` was **not run**.
  **No engine default was changed** — `ls2d_column`, `cp_revision`, `volume_convention`,
  `k_unit_system` and every `SedParams` field were at their adopted values.
- **No calibration was launched, no search was run, no α̂ or β̂ was fitted, and no objective was
  evaluated against the `docs/45` §2.1 α box.** `docs/47` §6.3's permitted/not-permitted list was
  read before any code ran and obeyed. The registered 5,482-evaluation budget and the four DDS
  seeds are untouched.
- **Every number in this document was measured by this pass** from scratchpad scripts
  (`b5_run.py`, `b5_stats.py`, `b5_predictors.py`, `b5_final.py`, `b5_extra.py`) that wrote
  nothing into the repository, **except** where a number is explicitly attributed to a prior
  document, in which case it is cited in place. Two reproduction gates were passed **before** any
  statistic was computed (§2.2).
- **Uncited quantities are named and pass or fail nothing:** the 0.05–0.30 SDR band and its
  implied `k` (§6.3); the ENSO-neutrality of CAL 2012–14, which is the premise of the CAL/ENSO
  split (`docs/45` §3.5, `docs/47` C4). **No plausibility band was invented.** Where a corrected
  value could not be computed — the 22-pair `k_min`, the ±28.8 % 13-station figure, `docs/46`'s
  replacement bar, the class-C detectability — this document says so and stops.
- **The `docs/23` §13.2 yield embargo is in force.** No t/km²/yr appears here.
- **Nothing is backdated. No git command was run.**

### 7.1 Cross-references

| document | relation |
|---|---|
| `docs/47_c4_entry_verdict.md` | **the source.** §2.2 (D2) is the finding; §6.1 B5 is the assignment. D2 is **confirmed**; its `k_min` "CAL-8 form 0.0130 /km" row is **withdrawn** (§4.3); its D1 level 0.0760 ⇒ α 0.897 is **independently reproduced** (§2.4). |
| `docs/42_c4_guards.md` | owns σ_r's registration (§4.2) and its §9.5 power table. **Not edited.** §4.2's derivation stands; its *reuse* elsewhere is what §5.1 retires. §9.5's mandatory pointer needs the 0.0130 correction (§5.2 row 15). |
| `docs/43_c3_c4_gate.md` | §3.2's Π row is the first reuse of σ_r as a residual sd. **Not edited.** |
| `docs/45_c4_preregistration.md` | frozen; owes **three** §8 amendments — the band (§3.3), the `k` bound wording (§4.2), and G12's decoupling (§3.2). **Not edited.** |
| `docs/46_ls_preregistration_DRAFT.md` | **the document B5 most affects.** Its materiality bar and Branch A/B discriminator are 0.1644 ln. §5.3 measures the consequence and recommends decoupling. **Not edited.** |
| `docs/37_c3_closure.md` | A2.4 line 1158 repeats the ±38 %; its 2.2×/9.7× ratios survive (§5.4). **Not edited.** |
| `docs/40_sdr_evidence.md` | the standing rule that an uncited band may neither pass nor fail a gate — the rule this document follows in declining to invent a replacement for `docs/46`'s bar. |
