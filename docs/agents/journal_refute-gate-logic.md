# Journal — adversarial refutation of "σ_r = 0.465 is an observation-noise floor 3.1–3.9× below the residual scatter"

Agent: refute-gate-logic. 2026-08-11. Posture: assume the finding is WRONG; try to prove it.

Target finding: docs/42 §4.2 registers σ_r = 0.465 ln (estimator disagreement); docs/43 §3.2
(line 191) / docs/45 §2.2 reuse it as the per-station residual sd for the SE of the fitted level
(0.465/√8 = 0.1644 ln = ±38 %) and for every k_min. Claimed true between-station scatter:
1.716 ln (CAL 8, est b) / 1.456 ln (all-18 G1.2 form).

## VERDICT: NOT REFUTED. Every attack failed; the finding is if anything conservative.

## What I read
docs/42 §1–§6 (incl. §2 r_i definition, §4.1 Lw table, §4.2 σ_r derivation, §4.3, §4.4, G1–G2),
docs/43 §2.2–§3.4 (line 191 is the Π row), docs/45 §2.2–§2.5, §3.1–§3.2, §4.2 guard table,
§5.3, §6.1–§6.2, §7 summary. docs/agents/journal_verify-gate-logic.md (the finding's origin).

## Attack 1 — "the k_min numbers are not actually σ_r-derived". FAILED.
`1.96 · 0.465 / sqrt(Σ(Lw−L̄)²)` on docs/42 §4.1's Lw values reproduces the registered numbers
exactly: all-18 → **0.002157 → 0.00216 /km** (2.109× over 345.8 km, doc says 2.12×);
CAL 8 → **0.02092 → 0.0209 /km** (docs/43 §3.2). σ_r IS the regression residual sd in every
power number. (CAL 13 gives 0.00964, not docs/42's 0.0104 — a separate ~8 % method difference
already flagged by docs/43 P1's "0.0096"; not part of this finding.)

## Attack 2 — "measured on the wrong window". FAILED, and it back-fires.
The verify agent measured on `adj_ratio_station_window.csv`, whose windows are the four **ENSO**
windows (2011, 2015–16, …). docs/45 §7 registers **CAL = 2012-01-01…2014-12-31** and puts both
ENSO pairs strictly out of sample. `data/processed/c2/c2_station_window_flux.csv` has only the
four ENSO windows — no CAL-window observed flux exists on disk, so nobody had measured the
residual scatter on the fitted window.
I measured it: `scratchpad/refute_sigma.py` (read-only; `ms.load_drivers` on `h2e_drivers.npz`,
`ms.load_geometry` at `cp_revision = cited_central_2026_08_11`, `SedParams()`, ledger exact=True,
basin 299.5387 Mt/yr — matches the verify agent's own figure). Estimator (b) = per-era Duan-smeared
rating flux, exactly `scripts/c2_compute.py`'s construction; estimator (a) = sample days.

| set / window | est | n | sd(ln r) | SE(mean) | ×σ_r |
|---|---|---:|---:|---:|---:|
| **CAL 8, CAL window 2012–14** | **b** | 8 | **1.9618** | **0.6936** | **4.22** |
| CAL 8, CAL window | a | 7 | 1.3539 | 0.5117 | 2.91 |
| all avail, CAL window | b | 10 | 1.8930 | 0.5986 | 4.07 |
| CAL 8, ENSO-window medians (their construction) | b | 8 | 1.7118 | 0.6052 | 3.68 |
| all, ENSO-window medians | b | 16 | 1.4202 | 0.3551 | 3.05 |

The last two rows reproduce the verify agent's 1.7159 / 1.4175 to 0.3 %. On the **correct**
window the gap is **larger**, not smaller.

Per-station, CAL window, est (b), r = obs/sim: 22017010 BOCAS 0.0099 · 24027030 NEMIZAQUE 0.0150 ·
21197010 EL PROFUNDO 0.0686 · 26137110 BANANERA 0.1435 · 22017030 BOCAS 0.187 · 24037390
CAPITANEJO 0.269 · 23127010 BORBUR 0.691 · 26127010 EL ALAMBRADO 4.077. Range = a factor **412**.
Model up-areas match IDEAM up-areas to 5 significant figures at every station, so this is not a
station-mapping artefact.

## Attack 3 — "the fit will remove the scatter". FAILED.
C4 has exactly two free parameters (docs/45 §2.2: `free_params_supported = 2`, Π and β).
- Π is a constant ⇒ removes the mean, not the spread (as the finding says).
- β: I re-simulated at β ∈ {0.40,0.45,0.50,0.56,0.60,0.65,0.75}. CAL-8 est(b) sd(ln r) runs
  1.875 → 2.100 **monotonically upward**; est(a) is flat at 1.354–1.385. β cannot absorb it.
- The joint regression docs/42 G1 note 3 *requires* (G1.2 + G3.1 + G4.1 in one fit) does not help
  either. Predictors recomputed from artifacts, not transcribed (`scratchpad/refute_joint2.py`):
  Lw by docs/42 §2's formula, class erosion shares, erosion-weighted LS̄.

| residual set | c | +Lw | +shG,shB | +lnLS̄ |
|---|---:|---:|---:|---:|
| all-18 form, ENSO medians, est b | 1.420 | 1.460 | 1.438 | 1.497 |
| CAL 8, ENSO medians, est b | 1.712 | 1.825 | 2.035 | 2.088 |
| CAL 8, CAL window, est b | 1.962 | 2.110 | 2.352 | 2.110 |

Every cell is 2.7×–5.3× σ_r. Adding the guard predictors *raises* the residual sd (dof loss).
Resulting k_min: all-18 **0.0067–0.0069 /km ⇒ 9.5–10.4×** over 342 km (registered 2.12×);
CAL 8 **0.078–0.122 /km ⇒ 121×–1,800×** over 61 km (registered 3.54×).

## Attack 4 — "one or two rogue stations". FAILED.
Deleting the extreme stations one at a time (nothing licenses this): 8 → sd 1.962; drop EL
ALAMBRADO (only 287 rating days) → 1.542; drop BOCAS-22017010 too → 1.307; drop NEMIZAQUE too
→ 0.849. Even after deleting **three of eight**, sd is 1.83× σ_r and SE(mean) is 0.380 ln
(±107 %), still 2.3× the registered 0.1644.

## Attack 5 — "the docs already disclose it". PARTIAL, and only for the k bound.
docs/42 §4.2 does head the number "REGISTERED NOISE **FLOOR**", and docs/42 G1 + docs/45 §2.3
both attach "**at best**" to the 2.12× bound — so the direction (not the size) is disclosed for k.
No such hedge exists on the level band. docs/45 registers it flatly, three times:
§5.3 "C4 reports the fitted Π, **its ±38 % band**"; §6.2 item 2 "**The level's band is ±38 %**
(0.724×–1.380×; SE 0.1644 ln at n = 8). Every Π and every load is quoted **with that band**,
never as a point"; §7 summary row. So the finding's "will be published as C4's headline
uncertainty" is the document's own text.
Constructive: docs/45 **G12** does contain a self-check that fires. It mandates reporting the
range of ln Π̂ across the 8 leave-one-out refits against ±0.322 ln. On the measured CAL-window
residuals the LOO range of the fleet-mean level is **0.860 ln > 0.644** ⇒ **G12's check fires**.

## Attack 6 — "the blast radius is overstated". PARTIAL SUCCESS (the only one).
"Every guard power number" is too broad:
- **SE(β) = 0.0199** is built on σ_day = 0.809 ln (the rating residual), **not** σ_r. Unaffected.
- The **b_obs IQR yardstick 0.464** (docs/42 §4.3) is an independently measured between-station
  IQR. Unaffected (and it is a coincidence of value, not the same number as σ_r).
- Where 0.465 / 0.658 is used as a **firing threshold** (G1.1's pair backstop, G8's seasonal
  range, G11's regional difference) the error makes those guards **more** trigger-happy — an
  error in the safe direction, not an optimistic one.
- The class-C detectability (docs/43 §3.2's "≈4.2× on the CAL 8, ≈2.9× on all 18") **is** σ_r-
  scaled, but I could not reproduce those exact figures with my design matrix (I get 8.2× / 3.2×
  at σ_r = 0.465), so I put no corrected number on it — only the note that it scales with σ_r.

## Artifacts (scratchpad, read-only on the repo)
`refute_sigma.py` · `refute_sigma_station_window.csv` (630 rows: 18 stations × 5 windows × 7 β) ·
`refute_joint2.py` · `refute_predictors.csv` (recomputed Lw / LS̄ / shares, all 18) ·
`refute_joint_regression.csv`.

Side observation, not part of the finding: my recomputed Lw differs from docs/42 §4.1 by a few
percent at most stations but by **9 %** at IRRA (289.1 vs 265.2 km), which flips the IRRA /
BOLOMBOLO ordering. Immaterial to k_min (Sxx changes ~1 %), but someone should reconcile it.
