# 55 — C4.3: the sediment calibration VERDICT — RAILED / EXPLORATORY (not adopted)

**Written 2026-08-12. The first run of the registered objective (`docs/45` §3) on the ADOPTED LS
field (`V4_dg`), as a Branch-B first run — every per-station `r, v, m` re-derived on new residuals,
no rescaling of a surface already seen (`docs/46` §6.1; `Δ_shape = 0.1299456916752905 ≠ 0`,
`docs/53`).** Harness: `scripts/c4/o5_calibration_profile.py`; machine record
`data/processed/{o5_calibration_profile.json, report_C4.json}`. This discharges `docs/47` **O5**
("nobody has re-profiled the objective on a corrected LS field") and is the C4.3 deliverable.

> **PRE-FIT DISCLOSURE (mandatory, `docs/45` §8.2.5).** This is **not** a blind pre-registered
> fit. The registered objective was profiled across the whole α box **before** any fit, on the V0
> configuration, in `docs/45` §8 Amendment 2 (2026-08-12). This run re-profiled it on the adopted
> `V4_dg` field. The verdict was predictable and is now **measured**. Recorded in `report_C4.json`
> as `pre_fit_profile_disclosure`, per `docs/47` §5.5 and §6.2 item 6.

## 1 — The verdict

**RAILED / EXPLORATORY. The fit is NOT adopted.** The in-box optimum of `F_report` (the median
KGE_ln over the CAL-8) sits at the **box floor** — α = **2.0**, β 0.60, `F_report` = **−0.118** —
and the *unconstrained* optimum is α ≈ **0.48** (β 0.56, `F_report` −0.025), **below the box floor
and below the `docs/35` §9.5 adopted-level plausibility floor (0.981)**. That fires `docs/35`
§6.1's **lower hard stop**: *a fit that needs α far below Williams means something upstream
(`Qsur`, `K`, `C`, `LS`) is over-producing, and that must be found, not offset.* The low-α pull is
the registered signature of **mild upstream over-production** — a diagnosis, not a value to adopt.

`F_report` = −0.118 is *numerically* inside the Fagundes bar [−0.26, 0.44], but it is read at a
**railed floor**, so it is not an adoption (`docs/45` §5.3, §6.1). α is the handle on the
non-identifiable product **Π** and is **never reported alone** (`docs/45` §5.3, `docs/42` G6).

## 2 — The measured profile (adopted field)

`F_report` is **monotone** in α across the box; the in-box best is the floor. At β 0.56:

| α | meaning | `F_report` |
|--:|---|--:|
| 0.48 | unconstrained optimum | **−0.025** |
| 2.0 | box floor (railed) | −0.120 |
| 2.967 | `docs/35` §9.5 adopted reference | −0.173 |
| 8.902 | §9.5 upper hard stop | −0.365 |
| 11.8 | Williams (1975) | −0.422 |
| 30.0 | box ceiling | −0.627 |

**Consistency check (confirms the machinery, not a coincidence):** the optimal α scales with
`1/f_LS`. The V0 unconstrained optimum was α 0.117 (`docs/45` §8.2.4); 0.117 × (1/0.25146) = 0.465
≈ the measured 0.48, while the achievable KGE at the optimum barely moved (−0.029 → −0.025), as
theory requires (at optimal α the bias term zeroes; KGE then depends on `r, v`, which the shape
change perturbs only slightly). **The adopted `V4_dg` shape improved the in-box KGE materially
over V0 (−0.118 vs −0.350): the shape helps, the level does not.**

## 3 — Per-station, and the guards

At the in-box optimum, per-station KGE tracks per-station `r` almost exactly — proof the ceiling
is the runoff-timing ceiling, not a calibration defect:

| station | n | flow-sel | `r` | KGE |
|---|--:|:--:|--:|--:|
| 21197010 EL PROFUNDO | 112 | | 0.79 | **0.758** |
| 23127010 BORBUR | 845 | | 0.65 | **0.497** |
| 24037390 CAPITANEJO | 477 | | 0.40 | 0.317 |
| 24027030 NEMIZAQUE | 145 | | 0.33 | 0.126 |
| 22017010 BOCAS | 661 | | 0.04 | −0.361 |
| 26127010 EL ALAMBRADO | 176 | **Y** | 0.31 | −1.083 |
| 22017030 BOCAS | 637 | | 0.20 | −1.132 |
| 26137110 BANANERA | 213 | | 0.38 | −4.537 |

**G12 — leave-one-out on the flow-selective station `26127010` (mandatory, `docs/45` §3.4):**
dropping it lifts the median to `F_report` = **+0.197** (β 0.65, α 2), still PASS vs bar — **the
§6 verdict does NOT flip**, so the outcome is not INDETERMINATE. The flow-selective station was
depressing the median; the fit is if anything slightly better without it.

**EVAL (scored, never fitted):** `21237020` ARRANCAPLUMAS (Magdalena trunk) scores KGE **+0.462**
(`r` 0.61) **out of sample**; `26017060` PUENTE ARAGÓN −1.46 (`r` 0.35). The other three EVAL
stations have **0 paired SSC×Q days inside 2012–2014** and are not scored.

## 4 — The three accompanying statements (`docs/45` §6.2, mandatory)

1. **α is the handle on Π.** The design matrix condition number is `inf`; α is not separable from
   `C/LS/K/vol/P/FG`. What C4 determined is **Π**; α̂ printed without Π and its equifinal family is
   a reporting FAIL (`docs/42` G6).
2. **The bar is weak by construction.** The mean-flow predictor scores KGE = 1 − √2 = **−0.414**;
   the bar's lower edge −0.26 sits only 0.15 above no-skill, over **8** stations. **Passing it is
   not evidence of a good model; failing it is evidence of a bad one** (`docs/45` §3.2). Our median
   (−0.118, or +0.197 without the flow-selective station) beats the no-skill line but is at the
   *edge of usable*.
3. **The LS level is UNVALIDATED and O4 is open.** `docs/42` G4.2 stands. O4 (α = 11.8's
   like-for-likeness with a 2-D contributing-area LS, no band offered) is UNRESOLVED and **bounds
   this verdict from above**.

## 5 — Why a high KGE was never attainable (the input ceiling, stated plainly)

Sediment timing is driven by runoff timing, and the runoff field is capped at **r ≈ 0.57** — the
Phase B rainfall ceiling, with the dry ENSO phase sitting at climatology (skill-over-climatology
**−0.0005**, `docs/26` addendum A.5). With `r_max ≈ 0.57`, the absolute KGE ceiling is
`1 − √((0.57−1)²) ≈ 0.57` even with perfect variability and bias; the campaign-sampled SSC and its
rating noise (σ ≈ 0.8 ln) lower the realistic figure further. **A high sediment KGE was not
physically on the table, and better rainfall is a known dead-end** — the CHIRPS merge failed its
volume gate twice (`docs/18` §15.5: *"no route to a passing volume gate exists inside the merge
code"*), and there is no v3 forcing. This is why a rigorously-measured railed/exploratory result
is the pre-registered publishable finding (`docs/46` §7, `docs/45` §6), and why the **model-free**
observed ENSO contrast (~3–9×, `docs/34`) carries the study's scientific claim independently.

## 6 — Owed and NOT done

- **ONI 2012–2014 record.** NOAA CPC ONI v5 could not be retrieved this session (page
  JS-rendered). Per `docs/45` §3.5's registered fallback the CAL window is labelled
  **OUT-OF-WINDOW** (by date), **not out-of-phase**, until the ONI values, retrieval date and
  threshold are recorded in `report_C4.json`. **Owed.**
- **Estimator (b) robustness — DONE (2026-08-12).** Refit on rating-curve flux
  (`ssc_rating_fits.csv`, usable eras) gives in-box `F_report` = **0.139** (PASS), **same sign** as
  estimator (a) (−0.118): **no sign disagreement, so the verdict is NOT INDETERMINATE.** Estimator
  (b) rails less — its unconstrained optimum α ≈ **5.9** sits *inside* the box — because it compares
  two Q-driven quantities (sim and a rating that is itself a function of Q), the exact reason
  `docs/45` §3.3 fits on (a), not (b). The EXPLORATORY verdict holds under both.
- **`k_hi` deposition re-solve** (`docs/45` §2.3) — **owed.** It reports a *level* pair (α at
  k = 0 vs k = k_hi) and needs the per-minibacia→station flow-path lengths; it **cannot change the
  verdict** (deposition raises the fitted α but does not move the bar comparison's sign). Deferred
  with that scope stated.
- **C5** (the ENSO out-of-sample application, 2011 / 2015–16) — not started; the strictly
  out-of-sample windows are untouched by this fit.

## 7 — Disclosure

Reads only. New files: `scripts/c4/o5_calibration_profile.py`,
`data/processed/{o5_calibration_profile.json, o5_calibration_profile.md, report_C4.json}`. No
engine default moved here (ACT 2 moved it earlier); no frozen artifact opened; `urh_ls2d.csv`,
`minibacia_ls2d.csv`, `urh_ls2d_variants.csv` and the frozen bundle untouched. The `docs/23` §13.2
yield embargo is in force — flux is absolute t/day, model-internal; **no t/km²/yr**.
