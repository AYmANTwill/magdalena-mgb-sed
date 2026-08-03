# 25 — Plan to close the hydrological phase

**Scope decision: this plan ENDS at a defensible calibrated hydrological model.**
Sediment (Phase C) is explicitly out of scope. Everything below exists to answer one
question — *is the discharge model good enough to stand as a result on its own, and do we
know precisely where it fails?*

Written 2026-08-03, after the 4,000-evaluation DDS search completed at 04:54.

---

## 1 — Where the stop line is

**In scope:** rainfall/PET forcing, the water balance, discharge calibration and validation,
the ENSO discharge contrast, and the documented limits of all of it.

**Out of scope — do not start these:**

| excluded | why, in one line |
|---|---|
| MUSLE / sediment module | blocked on mainstem SSC quality; a separate phase |
| local-inertial / hydrodynamic routing | celerity swept 0.22→2.0 m/s moved El Niño r by <0.016 (docs/22 §4.7); it cannot buy discharge skill |
| per-gauge specific yield (t/km²/yr) | 36 % of 85 shared gauges disagree beyond 2× on catchment area in **both** networks (docs/23 §13.2) |
| resolving catchment areas against an external source | required before *sediment*, not before *discharge* calibration. Carry it as a stated limitation |
| remote sensing / ML SSC retrieval | colleague's branch of the work |

The area question (open item 14) is the sharpest scope boundary here. It is **fatal to
sediment yield** and only **second-order for discharge calibration**, because the fitted
parameters are conditioned on the same areas used to score them. Say so explicitly rather
than resolving it now.

---

## 2 — Definition of done

The phase closes when every row below is either **met** or **documented as unreachable with
the measurement that shows why**. A row closed by measurement counts as closed.

### Physical plausibility — fully within our control, no excuses available

| criterion | adopted Config B | target |
|---|---|---|
| parameters railed at a bound | **3 of 10** (`kc_mult` 100 %, `k_int` 99.5 %, `lai_mult` 88 %) | **0** |
| store ordering `k_int < k_bas` | **inverted** (117 d vs 69 d) | holds |
| simulated / observed recession constant | **3.5×** | ≤ 1.5× |
| `kc_mult` (crop coefficient) | **2.00**, railed, beyond any FAO-56 value | ≤ 1.2 |

**A skill gain bought by railing a parameter counts as a failure, not a pass.**

### Skill

| criterion | current | target |
|---|---|---|
| **PRIMARY** — El Niño skill over climatology ≥ half of La Niña's | **+0.024 vs +0.236 (10× apart)** | El Niño ≥ +0.12 |
| validation median KGE | 0.450 | ≥ 0.50 |
| El Niño KGE | 0.193 | ≥ 0.35 (hard ceiling 0.57) |
| El Niño α | 0.793 | ≥ 0.90 |

### Reproducibility

| criterion | status |
|---|---|
| mass-balance residual < 1e-15 | **met** (1.67e-17) |
| numpy vs numba routers identical | **met** (max \|ΔQ\| = 0) |
| both ENSO phases out of calibration (Klemeš) | **met** |
| environment pinned, `pyproject.toml`, `tests/` | **not met** |
| docs/20, docs/21 written; docs/19 FLAWED items fixed | **not met** |

---

## 3 — Stages

### Stage 0 — read the search that already finished · *today, minutes*

The 4,000 evaluations are on disk and **unread**. Nothing else can be decided first.

```
python -m nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=-1 notebooks/14_calibration.ipynb
```

If it starts a *new* search instead of reading the four checkpoints, kill it — that means it
did not recognise them, and the fix belongs in `src/calib_v2.py`, not in a re-run.

**Exit:** per-period metrics for H1 and H2, and every parameter's position within its bounds.
That table is what decides Stages 1 and 2.

### Stage 1 — make H1 vs H2 separable · *1 session*

**The problem the raw numbers already show:**

| cell | seed 20260901 | seed 20260902 | mean | seed spread |
|---|---|---|---|---|
| H1 (v1 forcing) | 0.23023 | 0.23677 | 0.2335 | 0.0065 |
| H2 (v2 forcing) | 0.25337 | 0.23479 | 0.2441 | **0.0186** |

H2 leads by **+0.0106**, but its own seed spread is **0.0186** — larger than the gap. With
two seeds per cell, **the repair's effect on the objective is not established.**

Note for the journal in its own right: the v1 search reported a seed spread of **0.0043** on
~193 evaluations per run. This one produced **0.0186** on 1,000 — five times the budget, four
times the spread. That is evidence about the *revised objective's* surface (most likely the
added recession term), not about the forcing.

**Work:** add seeds — 4 to 6 per cell, not a longer single search, since the problem is
between-seed variance rather than under-convergence. Report the mean and spread per cell and
state plainly whether the cells separate.

**Exit:** either "H2 > H1 with seed spread smaller than the gap" or "not separable at N
seeds" — both are publishable; guessing is not.

### Stage 2 — physical plausibility · *1 session, gated on Stage 0*

The revised objective was built for exactly this (lower `k_bas` bound to 5 d, `k_int`
searched as a *ratio* of `k_bas` so the ordering holds by construction, recession-signature
term at weight 0.20). Stage 0's parameter-position table says whether it worked.

- If **0 railed and recession ≤ 1.5×** → this row of the definition of done is met, and it
  is the most defensible improvement in the whole phase.
- If `kc_mult` is **still railed** → do not simply raise the ceiling. docs/22 §4.5 measured
  that more ET alone makes El Niño *worse* (0.193 → 0.177 at kc × 1.20). The remaining
  candidate is the ET stress function: `ET = ETp·W/Wm` throttles evaporation even in wet
  soil, and with `W/Wm ≈ 0.5` a doubled `kc` is exactly the compensation required. Replacing
  it with the FAO-56 threshold form is a **one-function change** and it belongs in scope.

### Stage 3 — the decision point: CHIRPS merge · *1–2 sessions*

**The PRIMARY criterion is probably unreachable without this.** docs/22 §4.7 fixed El Niño r
inside 0.556–0.572 across twelve parameter configurations; the field's own leave-one-out
skill is 0.429. Parameters have ≈ +0.02 of headroom left, already located. Only a better
rainfall field can move r, and therefore the dry phase.

Design, already settled by the volume result: **quantile-map CHIRPS *to* the gauge
distribution**, stratified by elevation band and hydrographic zone. Volume stays
gauge-controlled — v2 IDW is now ~4 % *below* CHIRPS, so a naive merge would add water and
undo the repair. CHIRPS supplies spatial structure and fills the ungauged 17 % (41,180
fallback cells; nearest gauge median 16.3 km, max 71.5 km).

**Gate:** the notebook-11 LOOCV must beat gauge-only. If it does not, **do not adopt it**,
and record the negative result — it would mean satellite rainfall cannot improve the field
at this density, which is itself a finding.

**Two honest exits, and this is the choice to make consciously:**

- **(a) Merge succeeds** → El Niño moves, PRIMARY may be met, phase closes on a positive.
- **(b) Merge fails or is not enough** → close on the **input-ceiling result** instead:
  *"at ~30 km gauge spacing in a tropical mountain basin, daily rainfall–runoff correlation
  is capped near 0.57, because inter-gauge daily rainfall correlation is 0.33 at 0–25 km."*

**Recommendation: time-box (a) to two sessions, then take (b).** Exit (b) is publishable and
transferable on its own, so the phase is not hostage to the merge working.

### Stage 4 — close the gauge-quality items · *1 session*

- Open item 10: the **14 residual energy-floor gauges**. Triage exists (2 exclude, 2 keep,
  10 down-weight). Confirm the decisions survive the v2 forcing and record each reason.
- Open item 15: `is_intake` is a name regex (`BOCATOMA|CANAL`) and structurally cannot flag a
  place-named gauge below a reservoir. Either obtain a reservoir/transfer register or
  document the flag's true coverage — **do not leave its name implying more than it does.**
- Open item 12: flag the CATAM coordinate error in the inventory.

### Stage 5 — make it citable · *1 session*

- `environment.yml`, `pyproject.toml`, `Makefile`, `CITATION.cff`, `CONTRIBUTING.md`.
  `requirements.txt` currently omits 11 real dependencies (pandas, scipy, rasterio,
  geopandas, cdsapi, requests, pyflwdir, pysheds, affine, numba, OWSLib) and pins nothing.
- `tests/` — the smoke assertions currently live inside notebooks and cannot run in CI.
- **docs/20 and docs/21** — never written; generate from artefacts already on disk.
- **docs/19** — fix the two items flagged FLAWED: `calibration_safe` is geometry-only with no
  SSC-quality gate, and the flatline-threshold justification is wrong by ~600×.
- One results document for the advisor: the calibrated model, its skill, and its limits.

---

## 4 — Order, and why

```
Stage 0  read the finished search          <- today, blocks everything
Stage 1  seeds, until H1/H2 separate       <- else the repair's value is unknown
Stage 2  physical plausibility             <- fully in our control; do before chasing skill
Stage 3  CHIRPS merge, time-boxed          <- the only lever on the dry phase
Stage 4  gauge-quality items
Stage 5  packaging + docs
```

Stages 1 and 2 come before 3 deliberately. They are cheap, entirely within our control, and
they decide whether the model is *defensible*; Stage 3 decides whether it is *good*. A model
with interpretable parameters at KGE 0.45 is a better result than one at KGE 0.55 with a crop
coefficient of 2.0 and inverted reservoirs.

Realistic total: **5–7 sessions.**

---

## 5 — The one decision that needs the advisor

Everything else on this plan is ours to execute. This is not:

**Is the input-ceiling result an acceptable closing statement for the hydrological phase?**

If yes, the phase can close whether or not the CHIRPS merge succeeds, and Stage 3 becomes an
attempt rather than a requirement. If no — if he expects conventional adequacy (Moriasi
NSE > 0.50) — then Stage 3 must succeed, and if it does not, the phase needs either denser
rainfall input than IDEAM provides or a reduced spatial/temporal target (monthly instead of
daily; sub-basins instead of the whole network).

Put the ceiling slide in front of him and ask directly. It changes what "done" means.
