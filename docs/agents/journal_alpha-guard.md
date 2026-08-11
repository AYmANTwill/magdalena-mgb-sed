# Journal — `alpha-guard`

**Goal.** Replace the docs/35 §6 alpha guard, which docs/37 proved is now BLIND: after the C3
convention correction, a fit that silently absorbs the missing channel deposition lands α at
6.83–8.73, i.e. *inside* Williams' expected band around 11.8. Deliverable: `docs/42_c4_guards.md`
— a pre-registered guard set C4 can be held to, built on residual STRUCTURE (spatial, seasonal,
flow-magnitude) rather than parameter values, plus an explicit answer on non-separability of
α, C and LS.

**Constraints acknowledged.** No git. Touch only `docs/42_c4_guards.md` + this journal (docs/35
cross-referenced, NOT edited). No calibration launch. No `pd.read_csv` on wide forcing CSVs.
Frozen artifacts read-only. t/km²/yr gauge-referenced yields embargoed. Uncited plausibility
bands may not pass or fail a gate (docs/37 residual 3).

## Checklist

- [x] 0. Write this journal (first action).
- [x] 1. Read docs/00_INDEX.md.
- [x] 2. Read docs/35 (the blind guard, the q_peak registration, §6 in full).
- [x] 3. Read docs/37 (the C3 closure: the α 6.83–8.73 finding, the four residual candidates).
- [x] 4. Read docs/33 §3 for the registration STYLE to imitate.
- [x] 5. Read docs/34 (the observed target) + docs/32 §R6 (the station set that carries any
      spatial test) — do the tests I want to register actually have the stations to run on?
- [x] 6. Inspect `src/mgb_sediment.py` + the C3 artifacts to confirm each test is evaluable on
      artifacts C4 produces anyway (not on things nobody will compute).
- [x] 7. Enumerate errors (a) missing channel deposition, (b) peak deficit, (c) C-factor level,
      (d) LS2D resolution level — with fingerprints.
- [x] 8. Answer the non-separability question plainly.
- [x] 9. Write `docs/42_c4_guards.md`.
- [x] 10. Structured output.

## Log

### Step 6 — measurements (all read-only; scratchpad scripts, nothing written to the repo)

Ran `src/mgb_sediment.py` at adopted defaults on the frozen H2E drivers: **248.696 Mt/yr**,
ledger `exact = True` (docs/37 §2 says 248.730 — the 0.014 % difference is that I annualise by
dividing by exactly 10.0 rather than 3652/365.25; not a discrepancy in the run). No frozen
artifact touched; no calibration launched.

**(1) Spatial leverage — the deposition axis.** Per usable SSC station, walked the upstream set
over `topology.npz:downstream_idx` and computed the **erosion-weighted mean channel travel
length** `Lw = Σ(E_j · (path_j − path_station)) / ΣE_j` from `path_km_to_outlet`:

| set | n | `Lw` range | model upstream area |
|---|---|---|---|
| C4 calibration (13 tributary) | 13 | **2.6 – 110.4 km** (42×) | 68 – 6,380 km² (94×) |
| all usable | 18 | **2.6 – 348.4 km** (134×) | 68 – 54,035 km² (794×) |

22 topologically nested station pairs (matches docs/34 §4.2's count exactly), ΔLw 7.4 – 345.8 km.
Only **3** of the 22 are CAL–CAL.

**(2) The measured noise floor.** Two independent observed-flux estimators disagree by
`sd[ln(a/b)] = 0.658` over 32 station-windows ⇒ per-station 1σ on a single estimator
= **0.465 ln (1.59×)**. Bootstrap CIs alone would have said 0.10 (a) / 0.28 (b) — too
optimistic, so 0.465 is the yardstick I will register. Rating residual σ median 0.809 ln.

**(3) Power, at σ = 0.465.** Minimum detectable first-order deposition rate `k`:

| test | n | k_min (95 %) | = survival contrast over the 348 km span |
|---|---|---|---|
| slope on CAL13 only | 13 | 0.0104 /km | 3.06× over the CAL span — **underpowered** |
| slope on all 18 | 18 | **0.00216 /km** | 2.12× |
| 22 nested pairs (non-independent) | 22 | 0.00119 /km | 1.51× |

Reference (NOT a gate — the 0.05–0.30 SDR band is UNCITED, docs/37 residual 3): SDR 0.15 over
600 km ⇒ k = 0.0032 /km; SDR 0.30 over 600 km ⇒ 0.0020 /km. So the 18-station test has power
against realistic deposition and the CAL-13-only test does not. **The evaluation stations must
be in the diagnostic** (they are already evaluate-not-calibrate under docs/31 §C4.1).

**(4) Separability — measured, not asserted.** Per-station erosion share by land class:
Forest 2.4–72.3 %, Grassland 10.7–69.8 %, **Bare 0.0–75.6 %** across the 13 CAL stations;
Shrub / Cropland / Urban / Water / Wetland ≤ 3.1 % **everywhere** (sd 0.04 / 0.90 / 0.05 / 0 / 0
pp). Shares sum to 1 by construction ⇒ the design matrix `[1 | shares]` is **exactly singular,
cond = inf**. That is the algebraic proof: a uniform C multiplier *is* the α column. Only
class *contrasts* are identifiable, and only 2 of them (Forest/Grassland/Bare − 1 level).
Erosion-weighted LS spans 38.2 – 117.1 (ln range 1.12), so a *slope-dependent* LS error has
leverage while a scalar LS multiplier has none, ever.

**(5) The hard limit on all of it.** Only **3,282/8,672 minibacias (37.8 %), 98,988 km² (38.5 %),
89.8 of 248.7 Mt/yr (36.1 %)** lie upstream of any usable SSC station. **63.9 % of the model's
gross erosion (158.9 Mt/yr) is observed by no station**, and there are **801.1 km of channel
below the outlet-most SSC station** (ARRANCAPLUMAS `path_km_to_outlet`), including the whole
Momposina (basin max path 1,425.9 km).

**(6) Yardstick for the β/peak channel.** Observed flux–discharge exponent `b` (ln Qs ~ ln Q,
30 usable eras): median 1.409, IQR 0.591, sd 0.393; per-station median `b` over the 18:
median **1.573, IQR 0.464**, range 1.038 – 2.545. That IQR is the self-scaling bar.

**Consequence for the task as briefed:** the "above vs below the Momposina" test named in
task 1a is **NOT EVALUABLE** — docs/34 §4.2 measured that all 18 usable SSC stations lie
upstream of the Cauca–Magdalena confluence and therefore upstream of the Momposina, so no
station pair spans the sink. Replaced with a nested-pair travel-length test, which *is*
evaluable and whose power I measured above. Recorded here rather than quietly substituted.

**The key design insight** (this is what makes the replacement guard work): for a nested
station pair the **double ratio** `(sim_dn/sim_up)/(obs_dn/obs_up)` is **exactly invariant** to
α, to a uniform C multiplier, to a uniform LS multiplier, to `k_unit_system` and to
`volume_convention` — every scalar that is mutually confounded — because each cancels in the
numerator. It is not invariant to β or to the routing. So it tests transport structure alone
and *cannot* be absorbed by the parameter the old guard was watching.

### Step 9 — `docs/42_c4_guards.md` written (612 lines)

Guard set **G1–G9**, each with a threshold and a failure action, §7 coverage table mapping every
brief item to its guard. Arithmetic re-verified numerically after writing: Π = 11.8 × 47.8630 ×
7.593014 = **4288.408** (= 363.4245196 × 11.8 = 4288.409, the 0.001 being the rounding of
47.8630); √2 × 0.465 = **0.6576** → registered 0.658; exp(0.00216 × 348.4) = **2.122** →
registered "≈ 2.1×".

Two naming collisions caught and fixed on review: the Bare-class regression coefficient was
called `b`, which already means the observed flux–discharge exponent in G2.1 — renamed `c_G` /
`c_B` in G3.1, in §7's coverage row, and in the Bare-class sentence. `docs/35` §6.2's
cross-reference "G6.2" was ambiguous → "G6 item 2".

**`docs/35` was NOT edited.** §8.1 of the new doc states clause by clause which of its §6
survives (α band necessary-not-sufficient, scale trap, β band, T1 with an estimator restriction
added, T2, T3, RULE 0, §6.5's `f_peak` permission — with the note that `f_peak` is itself a
scalar and therefore joins Π and can never be fitted separately from α). No pointer was appended
to docs/35, because its §9 amendment log is the only place a pointer would belong and writing
there would be an amendment I have no result to justify.

**Honest limits recorded in the doc rather than smoothed over:** the Momposina test named in the
brief does not exist on this network; the CAL-13-only version of the deposition test is
underpowered by a factor ~5 and the 5 evaluation stations are therefore mandatory in the
diagnostic; a G1 non-detection is a *bound* (no sink stronger than ~2.1× over 348 km), never a
pass; and no guard here can close docs/37's SDR question because 63.9 % of gross erosion and
801 km of channel sit below the last station.

**Nothing launched, nothing frozen touched, no git.** Files written: `docs/42_c4_guards.md`,
this journal. Everything else was read-only; all computation ran from the scratchpad.

### Step 0 — journal opened (2026-08-11)

Task received. Nothing computed yet. Recording the premise I must not lose: the guard being
replaced failed not because α was mis-bounded but because the *quantity being bounded* is
insensitive to the error of interest. Any replacement I write must be checked against exactly
that failure mode — "would this test have caught the missing-deposition fit?" If a proposed
test cannot distinguish α=8 (compensating) from α=8 (correct), it is not a guard.
