# 42 — C4 guard set: pre-registered anti-compensation tests that a scalar cannot absorb

**Stage:** gate on C4 of `docs/31_phase_c_workplan.md`.
**Status: PRE-REGISTRATION. FROZEN on write, 2026-08-11**, by the `alpha-guard` agent
(`docs/agents/journal_alpha-guard.md`). Written **before** any sediment parameter has been
fitted and before any C4 search machinery exists. Every threshold in §5 and §6 is fixed. If a
rule below turns out to be wrong, the measuring session **journals it as an issue and follows
it anyway**; a threshold changed after seeing the number it judges is not a threshold.
**Amendments go in §9, dated, with a reason.**

**Why this document exists.** `docs/35` §6 registered a hard stop on the MUSLE coefficient α, on
the premise that an α absorbing a structural error would show up as an α far from Williams' 11.8.
`docs/35` §9.2 then adopted the `williams_m3` + `us_customary` convention (×363.4245196), and
`docs/37` §5.1 measured the consequence: **a fit that silently omits channel deposition now lands
α at 6.83 – 8.73, inside the registered "expected" band of 5.9 – 23.6, and
`check_musle_parameters` returns `status: ok`.** The guard cannot catch the single error C4 is
most likely to make. It is necessary and no longer sufficient. **C4 must not run until a test
that can catch it is registered. This is that test set.**

`docs/35` §6 is **not edited and not retired** — its bands still do the job they can still do
(§8.1). This document adds the tests it cannot do, and it changes what C4 is allowed to *claim*.

---

## 1 — The design principle, stated once

> **A scalar parameter can absorb a level. It cannot absorb a structure.**

Every guard below is therefore a test on **residual structure** — spatial, flow-magnitude,
seasonal, or land-composition — and not on a parameter value. The sharpest instances are the
statistics that are **algebraically invariant** to the confounded scalars, so no amount of
fitting can move them. §3 identifies exactly which scalars those are, and §4 measures whether
the observing network has enough leverage for each test to have power. **A test whose power was
not measured before registration is not a guard; it is a hope.**

---

## 2 — What C4 will produce anyway (the artifact contract)

Every test in §6 is evaluable on these, and nothing else is required. This list is part of the
registration: if C4's outputs do not include these columns, C4 has not met its own gate.

| artifact | content the guards read |
|---|---|
| `sed_station_daily.npz` (or csv) | simulated delivered load, t/day, at each of the **18** C1-usable, minibacia-mapped SSC stations, 2009-01-01…2018-12-31, day-aligned with `h2e_drivers.npz:dates` |
| the fitted parameter record | α, β, every transport/deposition parameter, and `SedParams.convention_summary()` verbatim |
| `data/processed/c2/c2_station_window_flux.csv` | **already on disk** — observed flux per station-window, both estimators, with bootstrap CIs |
| `data/processed/ssc_rating_fits.csv` | **already on disk** — per-era `log_a`, `b`, `r2`, `resid_sigma`; 30 usable eras |
| `data/processed/model_inputs_v2/topology.npz` | `downstream_idx`, `path_km_to_outlet`, `own_area_km2` — the spatial predictors |
| `SedResult.cell_eroded_t` + `SedGeometry` | per-cell gross erosion, land class, C, P, LS2D, K — the composition predictors |
| `data/processed/sim_calibrated_v2/q_gauge_H2E.npz` | observed and simulated discharge, for the flow-magnitude partition |

Two derived quantities are defined **here**, once, so C4 cannot define them after seeing results:

**`Lw_i` — the erosion-weighted mean channel travel length above station `i`** (km):

```
Lw_i = Σ_{j ∈ U(i)} E_j · (path_km_to_outlet_j − path_km_to_outlet_i) / Σ_{j ∈ U(i)} E_j
```

where `U(i)` is the topological upstream set of station `i`'s minibacia (walk
`downstream_idx`), and `E_j` is the model's own period-total gross erosion in minibacia `j`.
`Lw` is **model-internal**: it uses no gauge-referenced catchment area, so it is outside the
`docs/23` §13.2 area embargo, and it is never used as a divisor.

**`r_i` — the station log-residual**: `r_i = ln(flux_sim_i) − ln(flux_obs_i)`, means taken over
the same day set, per window, per estimator.

Measured values of `Lw` and of the composition predictors are tabulated in §4.1 so that C4
cannot recompute them differently and get a different answer.

---

## 3 — What is NOT separable. The honest answer, first, in full.

This section answers task 3 of the brief plainly, because everything downstream depends on it.

### 3.1 Seven scalars, one identifiable product

MUSLE as implemented is

```
Sed = f_vol · f_K · f_LS · α · (Qsur · q_peak · A)^β · K · C · P · LS2D · FG
```

The following are **spatially and temporally uniform scalars** in the adopted configuration:

| scalar | current value | source |
|---|---|---|
| α | 11.8 unfitted; **to be fitted in C4** | Williams 1975 |
| `volume_factor` (`volume_convention`) | 47.8630 (`williams_m3`) | `docs/35` §9.2 |
| `k_factor` (`k_unit_system`) | 7.593014 (`us_customary`) | `docs/35` §9.2 |
| `ls2d_factor` = aggregation × resolution | 1.000 × 1.000 | `docs/37` decisions 3, 4 |
| a uniform multiplier on the C field | 1.0 implicit | `urh_cp_factors.csv` |
| P | 1.0 basin-wide | `urh_cp_factors.csv` (explicit assumption) |
| FG | 1.0 | `docs/35` §8 item 3 |

> **Each of these enters every minibacia-day identically. Their partial derivatives of
> `ln Sed_i` are therefore the same column of ones, at every station, on every day, in every
> window. They are not "nearly" confounded and it is not a property of our station set: they
> are the same parameter written seven ways.**

Consequently:

> **NO calibration — on a basin total, on 13 stations, on 18, on daily series, on any objective
> function whatsoever — can separate α from the C level, from the LS level, from the K unit
> factor, from the volume convention, from P, or from FG.** Only their **product** is
> identifiable:
>
> ```
> Π = α · f_vol · f_K · f_LS · C_mult · P · FG        (currently Π = 11.8 × 47.8630 × 7.593014 = 4288.4 with C_mult = P = FG = f_LS = 1)
> ```

This was verified algebraically **and** measured: the design matrix `[1 | per-station land-class
erosion shares]` over the 13-station calibration set has **condition number = inf** (exactly
singular), because the shares sum to 1 by construction. A uniform C multiplier *is* the α column.

**This is the Phase B equifinality lesson one level down.** Phase B learned that twelve
parameter configurations moved El Niño `r` by < 0.016 because the ceiling lived in the
*observations*, not the parameters (`docs/22` §4.7). C4's version is stricter: here the
non-identifiability is in the *equations*, so it cannot be relieved by better data at all.

### 3.2 What *is* identifiable

| direction | identifiable? | why | leverage measured in |
|---|---|---|---|
| the product Π | **yes** (that is what a fit determines) | it is the level | — |
| β | **yes** | an exponent, not a scalar multiplier; it reweights days | §4.3 |
| transport/deposition structure | **yes** | it is spatially structured; §6 G1 is invariant to all seven scalars | §4.2 |
| **contrasts** between land-class C values | **yes, 2 of them** | class erosion shares differ between stations | §4.4 |
| a **slope- or steepness-dependent** LS error | **yes** | LS composition differs between stations | §4.4 |
| the C **level** | **no** — it is Π | §3.1 | — |
| the LS **level** (aggregation, resolution) | **no** — it is Π | §3.1 | — |
| C of Shrub, Cropland, Urban, Water, Wetland | **no** — no leverage | those classes carry ≤ 3.1 % of erosion at **every** station | §4.4 |
| the K unit system, the volume convention, P, FG | **no** — they are Π | §3.1 | — |

### 3.3 Therefore: what C4 must do instead of validating

> **REGISTERED.** C4 **cannot validate** α, C, LS, P, FG, the K unit system or the volume
> convention, individually. It must instead:
>
> 1. report the fitted **Π** with its full decomposition, every factor named with its own
>    independent evidence and its own status (derived / cited / assumed / unvalidated);
> 2. report the **family of equifinal solutions** — the set of (α, C_mult, f_LS, …) tuples that
>    give the same Π and therefore the same fit, so a reader can see that the fit does not
>    choose among them;
> 3. report the identifiable structural quantities (β, the transport parameter, the C class
>    contrasts) **separately**, as the only things the fit actually determined;
> 4. name, for each non-identifiable factor, the **independent evidence that pins it** — and
>    where there is none, say **UNVALIDATED** in the same table as the number.

The independent evidence currently available, honestly graded:

| factor | independent evidence | status |
|---|---|---|
| `volume_factor` = 47.8630 | Williams' English-unit form converted to SI, `95 × 0.90718474 / 34.92823^0.56 = 11.7818`, 0.15 % from the published 11.8; derived twice independently | **DERIVED — pinned** |
| `k_factor` = 7.593014 | `notebooks/09_soil_parameters.ipynb` §4 states the stored K was Wischmeier & Smith (1978) class values "converted to SI (×0.1317)"; undoing it returns the textbook numerics (0.020→0.1519 ≈ sand 0.15; 0.045→0.3417 ≈ silt loam 0.34; 0.028→0.2126 ≈ clay 0.21) | **IDENTIFIED — pinned to ≤ 1.3 % rounding residue** |
| α = 11.8 reference | Williams (1975), adopted unchanged by Buarque (2015) eq. 5 with the same daily-mean `q_peak` | **CITED** |
| C, Forest / Grassland | Wischmeier & Smith (1978) Table 10; Roose (1977) | **CITED, but at the low end of its own range** — `docs/37` residual 1 |
| C, **Bare = 1.0** | none; `docs/37` §3 records it as an **input artefact** (bare rock/ash/ice above the treeline), 36.9 % of basin erosion on 6.4 % of area | **UNVALIDATED — and it is the highest-leverage identifiable contrast in the station set (§4.4)** |
| C, Shrub / Cropland / Urban / Wetland | `urh_cp_factors.csv` marks Shrub explicitly ASSUMED | **ASSUMED, and unidentifiable here** |
| `ls2d_factor` = 1.000 | the "published mountainous LS 2–10" comparison was **retired as uncited** (`docs/37` decision 4). Desmet & Govers (1996) pins the *formula*, nothing pins the *level* | **UNVALIDATED** |
| P = 1.0 | no conservation-practice layer exists; P ≤ 1, so it is an explicit upper bound on erosion | **ASSUMED, one-sided** |
| FG = 1.0 | FG ≤ 1 in Buarque eq. 5; omitting it *raises* our load | **ASSUMED, one-sided (`docs/35` §8 item 3)** |

---

## 4 — The measured leverage and the registered yardsticks

Measured 2026-08-11 from `topology.npz`, `_c1_geom.csv`, the C2 artifacts and one read-only run
of `src/mgb_sediment.py` at adopted defaults (basin total **248.696 Mt/yr**, mass ledger
`exact = True`; `docs/37` §2's 248.730 differs only in the days-per-year divisor). No frozen
artifact was modified; no calibration was launched.

### 4.1 The spatial axis — and the Momposina test the brief asked for, which does not exist

> **The test named in the brief — stations above vs below the Depresión Momposina — is NOT
> EVALUABLE, and this is measured, not assumed.** `docs/34` §4.2: **all 18 usable SSC stations
> lie upstream of the Cauca–Magdalena confluence and therefore upstream of the Momposina.** No
> station pair spans the sink. The outlet-most SSC station, `21237020` ARRANCAPLUMAS, still has
> **801.1 km of channel below it** (`path_km_to_outlet`; basin maximum 1,425.9 km).
> **This network cannot observe the Momposina at all.** It is recorded here rather than quietly
> substituted.

What *does* exist is a nested travel-length ladder, and it is long:

| station | `Lw` km | model up-area km² | Forest / Grassland / **Bare** erosion share % | set |
|---|---:|---:|---|---|
| `22017030` BOCAS | 2.6 | 68 | 63.7 / 36.3 / 0.0 | CAL |
| `26167060` PAILA LA | 11.8 | 178 | 40.4 / 59.5 / 0.0 | CAL |
| `26017060` PUENTE ARAGÓN | 14.2 | 152 | 1.5 / 9.8 / **88.7** | EVAL |
| `26137110` BANANERA LA 6-909 | 26.9 | 289 | 11.9 / 12.5 / **75.6** | CAL |
| `24027030` NEMIZAQUE | 27.1 | 611 | 42.9 / 56.9 / 0.0 | CAL |
| `26107130` MATEGUADUA | 30.1 | 748 | 34.1 / 59.6 / 6.3 | CAL |
| `21197010` EL PROFUNDO | 30.4 | 833 | 15.7 / 69.8 / 14.3 | CAL |
| `23127010` BORBUR | 32.7 | 1,645 | 72.3 / 26.7 / 0.0 | CAL |
| `21147030` CARRASPOSO | 39.0 | 1,600 | 35.1 / 46.3 / 18.6 | CAL |
| `26127010` EL ALAMBRADO | 40.4 | 1,711 | 49.7 / 21.0 / 26.1 | CAL |
| `22017010` BOCAS | 42.5 | 2,411 | 26.9 / 10.7 / **62.4** | CAL |
| `26017020` JULUMITO | 46.5 | 723 | 7.4 / 21.7 / **70.7** | EVAL |
| `24037390` CAPITANEJO | 60.4 | 6,362 | 2.4 / 37.9 / **58.4** | CAL |
| `23087210` CANTERAS | 68.0 | 5,487 | 59.4 / 40.5 / 0.0 | CAL |
| `22057090` BOCATOMA TRIANGULO | 110.4 | 6,380 | 27.2 / 20.3 / **52.4** | CAL |
| `26167070` IRRA | 265.2 | 24,665 | 33.8 / 33.8 / 30.6 | EVAL |
| `26207080` BOLOMBOLO | 272.6 | 30,848 | 39.1 / 38.5 / 21.2 | EVAL |
| `21237020` ARRANCAPLUMAS | 348.4 | 54,035 | 19.9 / 24.2 / **54.7** | EVAL |

- CAL set (13, `docs/32` §R6): `Lw` **2.6 – 110.4 km (42×)**, up-area 68 – 6,380 km² (94×).
- All 18: `Lw` **2.6 – 348.4 km (134×)**, up-area 68 – 54,035 km² (794×).
- **22 topologically nested station pairs** (matching `docs/34` §4.2 exactly), ΔLw **7.4 – 345.8
  km**. Only **3 of the 22 are CAL–CAL** (`22017030`→`22057090` 107.8 km,
  `22017010`→`22057090` 67.9 km, `22017030`→`22017010` 39.9 km).

### 4.2 The registered noise floor, and the measured power

> **REGISTERED NOISE FLOOR: σ_r = 0.465 ln units (a factor of 1.59) per station log-residual.**

> **[WARN] AMENDMENT A-P4, 2026-08-12 — the phrase "per station log-residual" is RETIRED; the
> number is not.** `σ_r = 0.465 ln` is **VALID** as what its own next paragraph derives — the
> disagreement between two *observed-flux estimators*, `0.658/√2` — and it stays a registered
> yardstick in that use and as a **firing threshold** (G1.1's `+0.658`, G8, G11). It is
> **INVALID as the per-station model−observation residual sd**, which is what the SE of the
> fitted level and every `k_min` below require: measured on the registered CAL window, CAL 8,
> primary estimator (b), that sd is **1.9618 ln (×4.22)**. **Everything in §4.2 downstream of
> this line that divides or multiplies by `0.465` is restated in §9.7 (A-P4).** No threshold in
> §5 or §6 is changed, and **no materiality bar is created here or anywhere** (`docs/52`).

It is measured, not chosen: the two independent observed-flux estimators of `docs/34` disagree
by `sd[ln(a/b)] = 0.658` over the 32 station-windows where both are admissible, so a single
estimator carries `0.658/√2 = 0.465`. The bootstrap CIs alone would have implied 0.10 (estimator
a) / 0.28 (b) — the estimator disagreement is the honest number and is the one registered, in
the same spirit as `docs/33` H-BFI's use of the data's own spread rather than an invented
constant. (Rating residual σ: median 0.809 ln over 30 usable eras, for context.)

Minimum detectable first-order deposition rate `k` (95 %, two-sided), from the actual `Lw`
values above:

| test form | n | k_min /km | equivalent survival contrast over the 348 km span | usable? |
|---|---:|---:|---:|---|
| slope over the **CAL 13 only** | 13 | ~~0.0104~~ → **0.00964** (§9.5) | ~~3.06× across the CAL span alone~~ → **2.83×** (span) / **2.90×** (max) | **NO — underpowered** |
| **slope over all 18** | 18 | ~~**0.00216**~~ → **0.0066 – 0.0069** (§9.7) | ~~**2.12×**~~ → **≈ 9× – 11×, central ≈ 10× over ~342 km** | **YES — the registered primary** |
| 22 nested pairs (stations shared ⇒ not independent) | 22 | 0.00119 | 1.51× | corroboration only — **σ_r-scaled and NOT correctable; no corrected value (§9.7, open item P2)** |

> **[WARN] AMENDMENT A-P4, 2026-08-12 — every cell in the table above is proportional to
> `σ_r = 0.465`, which §4.2's own opening line above records as retired *for this use*.** The
> struck values are preserved so a reader can identify the superseded statement wherever it is
> still in print; **they may not be quoted from this body.** Two separate corrections are stacked
> in the CAL-13 row and must not be conflated: **0.0104 → 0.00964** is an *arithmetic* correction
> at the **registered** σ_r (A-P1.1, §9.5, unchanged by A-P4), and the CAL-13 row has **no
> σ-corrected value at all** because a CAL-13 residual set does not exist — only 8 of the 13 have
> a single paired CAL-window day (A-P1, §9.2). The all-18 row's correction is the σ one:
> `0.00686 /km` central, measured on the registered joint form, ⇒ `exp(0.00686 × 341.5)` =
> **10.41×**. Full derivation, provenance and the complete list of numbers that move: **§9.7**.

Scale reference **only** — `docs/37` residual 3 records that the 0.05 – 0.30 SDR band is
**UNCITED in this repository**, and per the standing rule an uncited band may not be used to
pass *or* fail a gate: a basin SDR of 0.15 over a 600 km path implies k = 0.0032 /km; SDR 0.30
implies 0.0020 /km. These are printed so a reader can see that ~~the 18-station test's 0.00216 /km
sits *inside* the range that matters and the 13-station test's 0.0104 /km does not~~. **No
threshold in §6 is derived from that band.**

> **[WARN] AMENDMENT A-P4, 2026-08-12 — the struck comparison INVERTS at the measured residual
> sd, and it decides nothing either way.** At the corrected all-18 `k_min` of
> **0.0066 – 0.0069 /km** the 18-station test sits **ABOVE the whole 0.0020 – 0.0032 /km
> reference**, where at the registered σ_r it sat inside it (`docs/48` §6.3). The CAL-13 figure is
> **0.00964 /km** (§9.5), not 0.0104, and is outside the reference on either σ. **This changes no
> verdict, because that band is UNCITED in this repository and, per the standing rule, may pass or
> fail nothing** — the sentence's *conclusion* ("no threshold in §6 is derived from that band")
> is unchanged and is re-affirmed. The inversion is recorded only so that no future reader
> resurrects the struck clause as support for anything.

> **Consequence, registered:** the deposition test **must** include the 5 evaluation stations.
> They are scored, never fitted — which is exactly the posture `docs/31` §C4.1 already requires
> ("evaluate — never calibrate"), and all 18 are upstream of the Momposina anyway, so including
> them imports no sink the model was told to ignore.

### 4.3 The flow-magnitude yardstick

Observed flux–discharge exponent `b` (`ln Qs ~ ln Q`, `ssc_rating_fits.csv`, 30 usable eras):
median 1.409, IQR 0.591, sd 0.393. Per station (median over its eras, 18 stations): median
**1.573**, **IQR 0.464**, range 1.038 – 2.545.

> **REGISTERED YARDSTICK: 0.464** — the between-station IQR of the observed exponent. Symmetric
> and self-scaling: if the model's typical exponent error exceeds the difference between one real
> station and another, the model is not resolving flow-magnitude structure at all.

### 4.4 The composition leverage

Erosion share by land class, across the 13 CAL stations (percentage points):

| class | min | median | max | sd | identifiable? |
|---|---:|---:|---:|---:|---|
| Forest | 2.44 | 35.06 | 72.26 | 20.74 | **yes** |
| Grassland | 10.73 | 37.85 | 69.79 | 19.36 | **yes** |
| **Bare** | 0.00 | 14.31 | **75.62** | **28.05** | **yes — the largest leverage in the set** |
| Shrub | 0.00 | 0.00 | 0.13 | 0.04 | no |
| Cropland | 0.00 | 0.00 | 3.09 | 0.90 | no |
| Urban | 0.00 | 0.00 | 0.16 | 0.05 | no |
| Water / Wetland | 0.00 | 0.00 | 0.00 | 0.00 | no |

Forest + Grassland + Bare ≈ 100 % of erosion at every station, so **exactly 2 C contrasts are
identifiable** (three classes minus the one level that is α). Erosion-weighted LS2D spans
**38.2 – 117.1** (ln range 1.12, sd 0.29 over the CAL 13), so a *steepness-dependent* LS error
has leverage. CAL-13 correlations among the candidate predictors are modest — ln C̄ vs ln LS̄
0.255, ln C̄ vs `Lw` 0.426, ln LS̄ vs `Lw` 0.258, ln K̄ vs ln C̄ −0.362 — so the §6 regressions
are jointly estimable rather than a collinear mush. **`Lw` vs ln C̄ at 0.426 is the one to
watch**: G1 and G3 must be fitted jointly, not one at a time (§6 G1, note 3).

### 4.5 The limit that bounds every guard here

| quantity | upstream of ≥ 1 usable SSC station | fraction |
|---|---:|---:|
| minibacias | 3,282 / 8,672 | 37.8 % |
| area | 98,988 / 257,097 km² | 38.5 % |
| **model gross erosion** | **89.8 / 248.7 Mt/yr** | **36.1 %** |

> **63.9 % of the model's gross erosion — 158.9 Mt/yr — is generated where no usable SSC station
> can see it, and 801.1 km of channel (including the entire Momposina) lies below the outlet-most
> SSC station.** Every guard in §6 constrains the model over the observed 36.1 %. **None of them
> can close `docs/37`'s SDR question**, because the outlet anchors (144 / 184 Mt/yr) are measured
> at the bottom of exactly the reach the network does not sample. This is stated up front so C4
> cannot present a passing guard set as closure of C3.

---

## 5 — The errors C4's parameters could absorb, and their fingerprints

| # | error C4 could absorb | absorbed into | fingerprint that betrays it — what differs between "right" and "compensating" | guard |
|---|---|---|---|---|
| a | **missing channel deposition** (no transport sink) | α (lands at 6.83–8.73, *inside* the old band — `docs/37` §5.1) | The error is spatially structured: with no sink, simulated flux is the undiminished sum of all upstream erosion, so a basin-wide α fitted to the fleet **over-predicts stations with long upstream travel paths and under-predicts short ones**. The residual acquires a **positive slope in `Lw`**, and the **nested-pair double ratio** `(sim_dn/sim_up)/(obs_dn/obs_up)` — which is invariant to α and to all six other confounded scalars — rises above 1. A scalar cannot produce a slope. | **G1** |
| b | **the peak deficit** (`R_AMS` 0.820, `R_Q1` 0.847, `R_Q5` 0.975; 1,829/2,236 observed POT events with no simulated partner at ±2 d) | α (level) and/or β (tail exponent) | The discharge deficit is **tail-only**, so compensation trades body over-prediction for tail under-prediction: (i) the **residual becomes positive at low observed flow and negative at high**; (ii) β rising pushes the **simulated flux–discharge exponent above the observed** one, and that exponent is invariant to all seven scalars. | **G2** |
| c | **the C-factor level wrong** | perfectly confounded with α — **no calibration can separate them** (§3.1, cond = inf) | The **level** leaves no fingerprint, ever. What does leave one is a **class-specific** error: the residual then correlates with that class's **erosion share**, which varies 2.4–72.3 % (Forest), 10.7–69.8 % (Grassland) and 0.0–75.6 % (Bare) across the CAL stations. Only 2 contrasts are identifiable; 5 classes have no leverage at all. | **G3**, and §3.3 |
| d | **the LS2D resolution / aggregation level** | perfectly confounded with α — a scalar (`ls2d_factor` = aggregation × resolution) | Again the **level** leaves no fingerprint. A **steepness-dependent** resolution bias does: the residual then correlates with the station's erosion-weighted LS̄ (38.2 – 117.1, ln range 1.12). If the residual has **no** LS̄ structure, the LS field's *shape* is exonerated and its *level* remains **UNVALIDATED** — not validated. | **G4**, and §3.3 |

---

## 6 — THE GUARD SET (registered; C4 is held to this list)

Each guard states its **quantity**, its **threshold**, and its **action on failure**. Unless a
guard says otherwise, "the 95 % interval" means a **station-level bootstrap**: resample the 18
stations with replacement 10,000 times, recompute the statistic within each resample (including
rebuilding the nested pairs among the resampled stations), take the 2.5/97.5 percentiles. Station
resampling — not day or pair resampling — is what propagates the fact that station residuals
carry systematic, non-averaging error and that pairs share stations.

**Primary estimator, registered once for all guards:** the observed flux is estimator **(b)**,
the per-era rating flux on all days (`c2_station_window_flux.csv`), because the tests need
day-matched pairing and estimator (a) has as few as 91 sample days at a station-window.
Estimator (a) is computed and reported as robustness and **cannot change any verdict** — the
same "gate on one, report both" discipline as `docs/33` §2.1. Exception: **G2.2 runs on (a)
only**, for the reason stated there.

---

### G1 — Missing channel deposition: the spatial transport test *(replaces the blinded job of `docs/35` §6.1)*

**G1.1 — the double-ratio statistic (the α-free test).** For each of the 22 nested station pairs
(up, dn), each window, primary estimator:

```
D_pair = [ ln flux_sim_dn − ln flux_sim_up ] − [ ln flux_obs_dn − ln flux_obs_up ]
```

> **Why this is the right instrument, and it is algebra rather than judgement:** α, a uniform C
> multiplier, `ls2d_factor`, `k_factor`, `volume_factor`, P and FG all cancel **exactly** in
> `sim_dn/sim_up`. `D_pair` is therefore **invariant to all seven confounded scalars of §3.1**
> and cannot be moved by any of them. It responds only to transport structure (and, weakly, to
> β through day reweighting). It is the sharpest available form of "structure cannot be absorbed
> by a scalar".

**G1.2 — the regression (the registered primary).** Over all **18** stations:

```
r_i = c + k · Lw_i + ε_i          (OLS; r_i from §2, Lw_i from §4.1)
```

| threshold | verdict |
|---|---|
| the 95 % station-bootstrap interval for `k` lies **entirely above 0** | **FAIL — the fit is compensating for a missing transport sink** |
| the fleet median of `D_pair` exceeds **+0.658** (one measured pair-σ, = √2 × 0.465) | **FAIL** — magnitude backstop, fires even if the slope interval is wide |
| neither fires | **NOT A PASS. Report the bound**: `|k| < k_hi` (the interval's larger absolute end) ⇒ "no first-order channel sink stronger than a factor `exp(k_hi × 348.4)` over the observed 348 km span". ~~At the registered σ_r that bound is ≈ **2.1×** at best.~~ → **≈ 10× over ~342 km** (§9.7) |

> **[WARN] AMENDMENT A-P4, 2026-08-12 — two corrections to the "neither fires" cell above; NO
> THRESHOLD IN THIS GUARD IS CHANGED.** (1) The **power figure** is restated: the struck
> "≈ 2.1× at best" was computed at `σ_r = 0.465` used as a residual sd; at the measured residual
> sd it is **≈ 9× – 11×, central ≈ 10× over ~342 km** (`k_min` 0.0066 – 0.0069 /km, §9.7).
> (2) The **comparative is inverted as printed.** `k_min` is a *detection floor*: a sink with
> `|k| < k_min` is invisible, so the form that is true with the verb **detectable** is *"no
> first-order channel sink **weaker** than X× … is detectable on this fit set"*. The registered
> wording pairs *"stronger"* with *"detectable"*, which states the opposite of what the statistic
> supports; with the verb *excluded* ("no sink **stronger** than X× is consistent with these
> residuals") the original comparative is correct. **§9.7 settles the reporting form on the
> `weaker`/`detectable` pairing** and records that the same inverted pairing appears in §9.4 and
> in `docs/45` §2.3 / G1.2, whose correction is owed to their own owner.

**ACTION on FAIL:** do **not** adopt the fit. Add an **explicit, named** transport sink
(`SedParams.tau_delivery_days > 0`, or a first-order reach deposition coefficient) and refit.
Report the pre- and post-sink fits side by side, with `k̂` for both. **Never** absorb it into α
(`docs/35` §6 RULE 0).

**Notes, registered.** (1) To first order `ln(sim/obs)_i = k · Lw_i` for a survival law
`exp(−k L)`; the Jensen term is `−k²·Var_E(L)/2` and must be reported when `k̂ · sd(L) > 0.3`,
because beyond that the linearisation is doing work. (2) The pair form of G1.1 is reported for
corroboration only — 22 pairs come from 18 stations (ARRANCAPLUMAS alone appears in 5), so its
apparent k_min of 0.00119 /km overstates the independent information; **the verdict is G1.2's**.
(3) `Lw` correlates with ln C̄ at 0.426 over the CAL 13, so G1.2 and G3.1 must be fitted **as one
multiple regression**, with each coefficient's interval taken from that joint fit. A univariate
`Lw` slope reported alone is not an acceptable G1 output.

---

### G2 — The peak deficit folded into α or β

**G2.1 — the flux–discharge exponent (the α-free test).** Fit `ln flux ~ ln Q` per station by the
**same** estimator as `ssc_rating_fits.csv` (OLS on logs, per rating era, station value = median
over eras), once on the observed pair and once on the **simulated** pair (`flux_sim`,
`q_sim_fit_m3s` from `q_gauge_H2E.npz`). Like `D_pair`, the exponent is invariant to all seven
scalars of §3.1; unlike `D_pair` it is directly sensitive to β.

| threshold | verdict |
|---|---|
| fleet median `\|b_sim − b_obs\|` **> 0.464** (§4.3, the between-station IQR of `b_obs`) | **FAIL — the model's flow-magnitude structure is wrong** |
| `b_sim − b_obs > 0` **and** β is within 0.02 of its upper bound | **FAIL — β is amplifying surviving events to stand in for missing ones** |

**ACTION on FAIL:** report, and attribute to (β, the runoff partition) — **never** to α. `b_sim`
is set jointly by β and by the model's internal `Qsur`↔`Q` scaling, so the test localises the
fault to those two and explicitly does **not** license a change to α, C or LS.

**G2.2 — residual by observed-flow quantile** (`docs/35` §6.4 test T1, carried forward
unchanged in its threshold): fleet-median relative residual below observed Q50 exceeding
**+25 %** while the above-Q95 residual is negative ⇒ **FAIL, STOP and report**.

> **One restriction added here, and it is a restriction, not a threshold change.** T1 must be
> computed on estimator **(a)**, the sample-day fluxes. Under estimator (b) the observed flux is
> a deterministic function of Q, so binning residuals by Q-quantile compares the model against
> the rating's own exponent and the "observation" contributes no independent information about
> flow-magnitude structure. Running T1 on (b) would produce a number that cannot fail for the
> right reason. `docs/35` §6.4 did not specify an estimator; this fixes it before the fact.

**G2.3 — β band** (`docs/35` §6.3, unchanged and re-affirmed): **HARD STOP if β > 0.65 or
β < 0.45.** Still valid because β is dimensionless and no unit factor can move it.

---

### G3 — The C-factor: what can be tested, and what must be pinned from outside

**G3.1 — the class-contrast regression.** Jointly with G1.2, over all 18 stations:

```
r_i = c + k · Lw_i + c_G · share_Grassland_i + c_B · share_Bare_i + ε_i
```

(`c_G`, `c_B` to avoid collision with `b`, which throughout this document means the observed
flux–discharge exponent of G2.1.) Forest is the reference class — its share is `1 − others` and
would be collinear with the intercept `c`; **that collinearity *is* the α confounding of §3.1**,
and dropping one class is how the unidentifiable level is correctly quarantined out of the test.

| threshold | verdict |
|---|---|
| the 95 % station-bootstrap interval for `c_G` or for `c_B` **excludes 0** | **FAIL — that class's C value is wrong** |

**ACTION on FAIL:** revise **that class's C** in `urh_cp_factors.csv`, with the reason and the
source written in its `source`/`note` column, and refit. **Never** α. This is the same
instruction `docs/37` §3 already gave for the >3000 m artefact ("the fix belongs in
`urh_cp_factors.csv`, not in the engine") — G3.1 is the test that decides whether it is needed.

**G3.2 — registered as unidentifiable, and therefore off-limits.** Shrub, Cropland, Urban, Water
and Wetland carry **≤ 3.1 % of erosion at every station** (§4.4). C4 **may not fit** their C
values and **may not report them as validated**. Any C4 table listing them must carry the word
**ASSUMED**.

**G3.3 — the C level, and the independent evidence that must pin it.** The C level is Π (§3.1)
and **no calibration can separate it from α**. It can only be pinned from outside, and the
required evidence is registered here:

1. a **citable** land-condition source for Colombian Andean pasture and cropland, or a published
   Magdalena–Cauca MUSLE/RUSLE C table, applied per URH class with the reason written into
   `urh_cp_factors.csv` (`docs/37` residual 1); **and**
2. for **Bare = 1.0** specifically — the single highest-leverage identifiable contrast in the
   whole station set (share 0.0 – 75.6 %) and simultaneously the least evidenced value in the
   table — either a citation or an explicit reclassification of the above-treeline rock/ash/ice
   cells with a written reason.

Until (1) and (2) exist, every C4 table quoting a load must mark the C level **UNVALIDATED**.
**G3.1 firing on `c_B` would be the first independent evidence this project has ever had about the
Bare class**, so it must be run and reported whichever way it comes out.

---

### G4 — LS2D: shape testable, level not

**G4.1 — the steepness-dependence test.** Add `ln LS̄_i` (station erosion-weighted LS2D, §4.1
range 38.2 – 117.1) to the G1.2/G3.1 joint regression.

| threshold | verdict |
|---|---|
| the 95 % station-bootstrap interval for its coefficient **excludes 0** | **FAIL — the LS2D field carries a steepness-dependent bias** |

**ACTION on FAIL:** fix the LS2D field (`scripts/c3/ls2d.py`, `urh_ls2d.csv`) or adopt a
**steepness-dependent** resolution correction with its derivation. **Never** α, and never a
scalar `ls2d_resolution` multiplier — a scalar cannot fix a slope-dependent error, it can only
hide it in Π.

**G4.2 — registered: the LS level is not identifiable and is currently unevidenced.** C4 **may
not** change `ls2d_aggregation` or `ls2d_resolution` to move the level (that is
`docs/37` §5.4 restated), and **may not** report the LS level as validated. The comparison that
would have pinned it — "published mountainous LS 2–10" — was retired as **uncited**
(`docs/37` decision 4), so the honest status is **UNVALIDATED** and it must be printed that way.
A G4.1 non-detection exonerates the field's *shape* and says nothing about its *level*.

---

### G5 — The precondition guard: what replaces the α band's lost job

`docs/35` §6.1 could once catch a deposition-free fit because it needed α ≈ 2,483. It cannot now
(6.83 – 8.73 is inside the band). The replacement is a **precondition on the run, not a bound on
a number**:

> **REGISTERED.** A C4 fit may be adopted **only if both** hold:
>
> 1. the adopted configuration contains a **named, non-trivial transport sink** — e.g.
>    `tau_delivery_days > 0`, or a reach deposition coefficient that is fitted and reported —
>    **or** the C4 document states **"this model asserts SDR = 1.0 between hillslope and station"**
>    in those words, as a claim, with G1's measured bound as its only evidence; **and**
> 2. **G1.2 has been run and its `k̂` with interval is reported in the same table as α.**
>
> **A fitted α anywhere in 5.9 – 23.6, obtained without (1) and (2), is an automatic FAIL
> regardless of what `check_musle_parameters` returns.** `docs/37` §5.1 states this as a warning;
> here it is a gate with a test attached.

---

### G6 — The level-invariant report (what C4 publishes instead of a validated α)

> **REGISTERED.** Every C4 table that quotes a fitted parameter or a load must carry, in the
> same table:
>
> 1. **Π** = α · `volume_factor` · `k_factor` · `ls2d_factor` · C_mult · P · FG, the only
>    identifiable level (at present, unfitted: 11.8 × 47.8630 × 7.593014 = **4288.4**);
> 2. α **with** the application unit (`docs/35` §6.2 — an α of 12 is textbook-perfect at the
>    registered pixel scale `a_p` = 0.0081 km² and a 2.2× over-fit at minibacia scale) and with
>    the registered band beside it (`docs/35` §6.1, T3);
> 3. `SedParams.convention_summary()` verbatim (`docs/37` §5.3);
> 4. the **equifinal family**: at minimum the three tuples that give the same Π under
>    C_mult ∈ {1, 2, 5}, so a reader sees that the fit did not choose among them;
> 5. the per-factor evidence grade from §3.3 — **DERIVED / IDENTIFIED / CITED / ASSUMED /
>    UNVALIDATED** — for every factor in Π.
>
> **FAIL (as a reporting failure, blocking adoption) if any of the five is missing.**

---

### G7 — Cross-phase compensation (`docs/35` §6.4 T2, carried forward)

Fit on one ENSO phase, score on the other. **FAIL** if the El Niño 2015–16 residual is more
positive than the La Niña 2011 residual by more than the **+10 %** contrast bias already
registered in `docs/35` §5.4 (`R_AMS` 0.808 vs 0.686 ⇒ 0.8875/0.8097 = 1.096). Report either way,
because the direction is known in advance to flatter the headline contrast.

---

### G8 — Seasonal residual structure

Median `r_i` by calendar month, fleet-pooled, primary estimator.

| threshold | verdict |
|---|---|
| the range across months of the fleet-median monthly residual exceeds **0.465 ln** (one σ_r) | **FAIL — a seasonal error is being absorbed by a constant level** |

**ACTION on FAIL:** report, and attribute — candidates are the runoff partition, the C field's
lack of a seasonal cycle (a single annual C per class in a basin with two rainy seasons and
crop calendars), and the antecedent-state effect `docs/31` §C4.2 already flags. Not α.

---

### G9 — Mandatory disclosure of the unobserved fraction

> **REGISTERED.** No C4 statement about a **basin-scale** quantity — the basin total, the implied
> SDR, or the closure of `docs/37` — may be made without stating, in the same paragraph, that
> **63.9 % of the model's gross erosion (158.9 of 248.7 Mt/yr) is upstream of no usable SSC
> station**, that only **36.1 %** is, and that **801.1 km of channel — the whole Momposina —
> lies below the outlet-most SSC station** (§4.5).
>
> **FAIL (reporting) if a basin-scale conclusion is drawn from station fits without it.**
> Passing G1–G8 constrains the model over 36.1 % of its own erosion. It is not closure of C3.

---

## 7 — Coverage check against the brief

| brief item | guard | threshold | evaluable on |
|---|---|---|---|
| a. missing channel deposition — spatial fingerprint | **G1.1, G1.2, G5** | bootstrap interval for `k` above 0; median `D_pair` > +0.658; precondition | station daily load + `topology.npz` + C2 flux |
| b. peak deficit folded into α or β | **G2.1, G2.2, G2.3** | \|b_sim−b_obs\| > 0.464; T1 +25 %/negative; β outside 0.45–0.65 | station daily load + `q_gauge_H2E.npz` + `ssc_rating_fits.csv` |
| c. C-factor level | **G3.1, G3.2, G3.3** | interval for `c_G` or `c_B` excludes 0; unidentifiable classes marked ASSUMED; level UNVALIDATED absent citation | `cell_eroded_t` + `SedGeometry` + station residuals |
| d. LS2D resolution level | **G4.1, G4.2** | interval for the ln LS̄ coefficient excludes 0; level UNVALIDATED | as above |
| non-separability answered explicitly | **§3** | seven scalars, one identifiable product Π; cond = inf measured | — |
| what C4 must report instead | **§3.3, G6** | five mandatory table elements | — |
| the limit on all of it | **§4.5, G9** | 36.1 % observed; 801 km unobserved below | — |

---

## 8 — Relationship to `docs/35`, and what is not changed

### 8.1 `docs/35` §6 is retained, not replaced

Nothing in `docs/35` is edited by this document — its §4, §5 and §6 are frozen and remain so.
What survives and still does useful work:

- **§6.1's α band** (expected 5.9 – 23.6; hard stops α > 35.4, α < 3.9) still catches gross
  mis-scaling and, per `docs/35` §9.2, is a like-for-like comparison for the first time. It is
  **necessary and not sufficient**: it cannot see a deposition-free fit. **G5** supplies the
  missing condition.
- **§6.2's scale trap** (`N^(2β−1)`) is dimensionless and untouched. Re-affirmed as **G6 item 2**.
- **§6.3's β band** is untouched. Re-affirmed as **G2.3**.
- **§6.4 T1** is carried forward as **G2.2** with an estimator restriction added (not a
  threshold change). **T2** is carried forward as **G7**. **T3** is folded into **G6**.
- **§6 RULE 0** — α and β may not compensate the §5 biases — is the premise of this whole
  document and is re-affirmed unchanged.
- **§6.5's permission** to report an explicit, separately named, separately reported `f_peak`
  stands. Note that `f_peak` is itself a scalar and therefore joins Π (§3.1): it may be reported
  as a factor, but it can never be *fitted* separately from α.

### 8.2 What this document deliberately does not do

- It does not narrow the `docs/35` §5.3 bias bracket. That needs sub-daily data.
- It does not decide the SDR question. §4.5 measures why C4 structurally cannot.
- It does not touch the `docs/23` §13.2 embargo: no guard here normalises by a gauge-referenced
  area, and no threshold is expressed in t/km²/yr.
- It does not use the uncited 0.05 – 0.30 SDR band to pass or fail anything (§4.2).
- It launches nothing and fits nothing.

---

## 9 — Registration record

| | |
|---|---|
| Registered | **2026-08-11**, before any C4 search machinery existed and before any α/β fit |
| Registered by | the `alpha-guard` agent; process record `docs/agents/journal_alpha-guard.md` |
| Guards | **G1–G9**, §6; every one with a threshold and a failure action; coverage table §7 |
| Registered yardsticks | σ_r = **0.465 ln** (estimator disagreement, 32 station-windows); `b_obs` between-station IQR = **0.464**; pair-σ = **0.658 ln** — ⚠ **σ_r's parenthetical is the whole of what survives: amendment A-P4 (§9.7) retires its REUSE as the per-station model−observation residual sd (measured **1.9618 ln**), and leaves the number, its derivation, the `b_obs` IQR and the pair-σ untouched** |
| Registered primary estimator | (b) rating flux on all days; (a) reported, non-deciding; **exception G2.2 runs on (a)** |
| Registered station sets | CAL 13 (`docs/32` §R6 tributary set) for fitting; **all 18 for every residual-structure guard**, the 5 evaluation stations scored and never fitted — ⚠ **the fitting set is SUPERSEDED by amendment A-P1 (§9.2): it is the CAL 8.** The all-18 clause and the never-fit rule are **unchanged** and are re-affirmed by A-P2 (§9.3) |
| Measured before registration | `Lw` per station (§4.1); power k_min (§4.2); land-class erosion shares (§4.4); unobserved fraction (§4.5); exponent spread (§4.3) — all from read-only reads of `topology.npz`, `_c1_geom.csv`, `urh_*.csv`, the C2 artifacts, and one scratchpad run of `src/mgb_sediment.py` at adopted defaults (248.696 Mt/yr, ledger `exact = True`) |
| Not evaluable, and why | **above/below the Momposina** — all 18 usable SSC stations lie upstream of the Cauca–Magdalena confluence (`docs/34` §4.2); 801.1 km of channel and 63.9 % of gross erosion lie below the outlet-most station |
| Sources of every number | `docs/32` §R6 (station classification), `docs/33` §7.3–§7.5 (peak ratios), `docs/34` §3.1/§4.2/§5.1 (observed contrast, nesting, anchors), `docs/35` §5–§6 + §9.2 (proxy, bias, conventions), `docs/37` §2–§5 (the re-run, the residuals, the blinded guard), `docs/23` §13.2 (the embargo) |
| Amendments | ⚠ **THREE, all dated 2026-08-11 — A-P1, A-P2, A-P3, plus A-P1.1 (the power-table correction P1 requires). See §9.1–§9.6 below. Plus A-P4, dated 2026-08-12 (§9.7): σ_r's reuse as a residual sd retired, the level band and the `k` power restated, `docs/47` B5's `docs/42` half enacted.** This cell read `none` until 2026-08-11 while C4 was already under way; that gap is the audit-trail defect `docs/47` §2.4 (D4) recorded, and §9.1 states plainly that the transcription is late **Plus A-P5, dated 2026-08-19 (§9.8): the `cp_revision` LABEL on §4's and §9's provenance line — "adopted defaults" there names the **prior** revision.** |

**Disclosure, per the fix protocol.** No frozen artifact was modified:
`sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv, q_gauge_H2E.npz}` were opened
read-only and every computation above ran from a scratchpad script that wrote nothing into the
repository. No calibration was launched. Nothing is backdated. `docs/35` was not edited; this
document cross-references it and states in §8.1 exactly which of its clauses survive. C3 remains
**OPEN** (`docs/37`) and this document does not close it — it registers the conditions under
which C4 may proceed while C3 is open, alongside `docs/37` §5's five prohibitions.

---

## 9.1 — Amendment log: opened 2026-08-11, and it is late

**Written by the `debt-b4-transcription` agent; process record
`docs/agents/journal_debt-b4-transcription.md`.** This block is the amendment slot §9 reserved on
2026-08-11 ("**Amendments go in §9, dated, with a reason**", §0). It is the **only** part of this
document this pass wrote, apart from the two pointer cells in §9's table above, whose original
text is preserved verbatim beside the pointer. **No threshold in §5 or §6 is altered. No number in
§1–§8 is edited or deleted.** §4.2's body still prints the number A-P1.1 corrects; see §9.6 F1.

**The lateness is recorded, not smoothed.** `docs/43` §3.1 declared P1/P2/P3 **blocking
preconditions on C4's start**, to be transcribed here "before C4 begins". They were not. C4 began
anyway: `1e0843c` (C4.1 channel transport), `865f674` (C4.2, `docs/45` frozen), `831bd0a` /
`02e7e95` (nb19 written and executed), `608a39e` ("tracker: C4 is under way"). Until this entry,
§9 read `Amendments | none` and `Registered station sets | CAL 13`.

**What was and was not at risk.** The **substance** was discharged on time: `docs/45` (FROZEN
2026-08-11) registered the same three decisions in its own frozen §2.2, §2.4 and §2.3, and
recorded in its §0 that the `docs/42` §9 transcription "remains owed". So no fit ran under the
superseded rules. What was broken was the **audit trail**: a reader opening this document — the
one `docs/37` A1.6 and `docs/45` §1.1 both say C4 is held to — was given a superseded fit set and
an uncorrected power table with no amendment note. That is `docs/47` §2.4's finding **D4**, and
this block closes it.

---

## 9.2 — AMENDMENT A-P1 · 2026-08-11 · the fitting set is the **CAL 8**, not the CAL 13

**Source:** `docs/43` §3.1 **P1**, measured by lens 3 (`docs/agents/journal_adj-c4-feasibility.md`).
**Discharged in substance by** `docs/45` §0 and §2.2 (frozen 2026-08-11).
**Reason:** 5 of the 13 CAL stations have **no paired SSC + observed-Q day** in the registered CAL
window 2012–14. A station that cannot contribute a single scored day is not a fit point.

**The 8 that survive all four filters** — this is the fit set:
`23127010` BORBUR-AUT · `22017010` BOCAS · `22017030` BOCAS · `24037390` CAPITANEJO ·
`26137110` BANANERA LA 6-909 · `26127010` EL ALAMBRADO AUT · `24027030` NEMIZAQUE ·
`21197010` EL PROFUNDO.

**The 5 lost, each for a hard record-window reason, named so the loss cannot be re-litigated:**

| station | reason |
|---|---|
| `23087210` CANTERAS | zero SSC before 2015 |
| `26167060` PAILA LA | zero SSC before 2015 |
| `21147030` CARRASPOSO | zero SSC before 2015 |
| `22057090` BOCATOMA TRIANGULO | 619 CAL SSC days, but observed Q ends 2009-03-19 |
| `26107130` MATEGUADUA | neither |

**Measured consequences, carried from lens 3 and not recomputed here:** fitted area falls
**10.1 % → 5.4 %** of the basin (13,862 km²); supported free parameters fall **3 → 2**
(`docs/45` §2.2); joint-regression residual df on the fit set = **4**; composition design
condition number **5,682** (basin-total form still **inf**, §3.1 unchanged); only **1** of §4.1's
3 claimed CAL–CAL nested pairs survives (`22017030` → `22017010`, 39.9 km).

> **NOT AMENDED by A-P1, and re-affirmed:** *"**all 18** for every residual-structure guard, the 5
> evaluation stations scored and never fitted."* A-P1 changes **only** the set that is **fitted**.
> **G1.2 still runs on all 18 and keeps `k_min` = ~~0.00216~~ /km.** Every threshold in §6 is untouched.
> ⚠ **A-P4 (§9.7), 2026-08-12:** the *set* is unchanged and re-affirmed a second time; the
> **number** is not — at the measured residual sd it is **0.0066 – 0.0069 /km (≈ 10× over
> ~342 km)**. A-P1's substantive claim (G1.2 runs on all 18) does not depend on it.

---

## 9.3 — AMENDMENT A-P2 · 2026-08-11 · `21237020` ARRANCAPLUMAS is EVALUATION-ONLY

**Source:** `docs/43` §3.1 **P2**, which required the `docs/31` §C4.1 ↔ `docs/42` §4.2/§9 conflict
be decided **in writing, either way, before a fit exists**. **Decided in** `docs/45` §2.4
(process record `docs/agents/journal_c42-prereg.md` D6), **for this document**:

> **`21237020` ARRANCAPLUMAS is an EVALUATION station. It is scored and never fitted.** So are
> `26017060` PUENTE ARAGÓN, `26017020` JULUMITO, `26167070` IRRA and `26207080` BOLOMBOLO.

This **confirms** §9's existing never-fit rule against `docs/31` §C4.1's permission; the conflict is
resolved in favour of this document. Reasons, recorded before the decision entered `docs/45`:
(1) admitting it would relax a frozen registration to gain power **after** the power had been
measured — the post-hoc move this project forbids; (2) it is the **only Magdalena-trunk SSC
station in the network** (`docs/32` §R6) and is worth more as the single independent trunk check;
(3) the entire cost falls on **fitting `k`**, which A-P3 does not do.

**The cost, stated and not hidden:** fitted area stays **5.4 %** instead of 25.1 %; the fit set's
own `k_min` stays **0.02092 /km** instead of **0.00303 /km** — a factor **6.9** in deposition
detectability *on the fit set*. Both figures are recomputed and confirmed in §9.5.

> ⚠ **A-P4 (§9.7), 2026-08-12: both `k_min` values move; the factor 6.9 SURVIVES, and that is the
> load-bearing part of this amendment.** At each set's own measured CAL-window residuals the pair
> becomes **0.0838 /km** (CAL 8) and **0.01210 /km** (CAL 8 + ARRANCAPLUMAS), whose ratio is
> **6.926** — a **ratio of two σ-scaled numbers, in which σ cancels**. A-P2's cost statement is
> therefore unchanged in substance. Do **not** "correct" the 6.9.

---

## 9.4 — AMENDMENT A-P3 · 2026-08-11 · deposition `k` is FIXED at 0, reported as a bound; **2 free + 1 fixed**

**Source:** `docs/43` §3.1 **P3**. **Discharged in substance by** `docs/45` §2.3.
**Reason:** `k` is **not identifiable on the achievable fit set** (`k_min` 0.02092 /km over its own
60.4 km ⇒ only a sink stronger than **3.54×** would be detectable). Reporting a fitted `k` would be
reporting noise with a decimal point.

> ⚠ **A-P4 (§9.7), 2026-08-12: this reason gets STRONGER, not weaker.** At the measured residual
> sd the CAL-8 figure is **0.0838 /km ⇒ ≈ 173× over 61.5 km** (0.0883 ⇒ 164× on §4.1's printed
> `Lw`), so the un-identifiability that justifies fixing `k` at 0 is understated here by ≈ 4×.
> A-P3's decision is re-affirmed. Note also that this sentence pairs *"stronger"* with
> *"detectable"*, the inverted comparative §9.7 settles.

- **`k` = 0.0 /km, FIXED and not fitted** — `TransportParams.k_dep = 0.0`, `dep_mode = 'per_km'`,
  `tau_channel_days = 0.0`, `SedParams.tau_delivery_days = 0` (`docs/45` §2.3, against
  `src/mgb_transport.py` from C4.1).
- **Registered parameter count: 2 free (Π level via α, β) + 1 fixed-and-reported-as-a-bound.**
  `docs/31` §C4.2's "three free" is superseded.
- **`docs/42` G5 is satisfied by option 2, not option 1.** `k_dep` is a *named* parameter, so the
  machinery for option 1 exists, but at `k_dep` = 0 the sink is **trivial** and option 1 requires a
  non-trivial one. `docs/45` §2.3 therefore states the words G5 demands:
  **"This model asserts SDR = 1.0 between hillslope and station."**
- **G5's second leg is unchanged and still binds:** G1.2's `k̂` with its 95 % station-bootstrap
  interval must appear **in the same table as α**, in the registered sentence form *"no first-order
  channel sink stronger than X× over Y km is detectable on this fit set"*, never as a fitted value.

---

## 9.5 — AMENDMENT A-P1.1 · 2026-08-11 · §4.2's power table, corrected — and the **0.0096-vs-0.0104 discrepancy resolved**

`docs/43` §3.1 P1 also instructs: *"Correct §4.2's power table with it."* Doing so exposed a
discrepancy the record carried unresolved (`docs/47` §7 open item **O7**): P1 writes *"the
fitted-set `k_min` is 0.0209 /km, **not 0.0096 /km**"*, attributing **0.0096** to this document,
while §4.2 prints **0.0104**. **This amendment resolves it by recomputation, not by preference.**

### The method, recovered and stated

§4.2 never printed its formula. It is recovered from `src/nbgen/make_nb19.py:1970` (`def k_min`) —
the minimum |slope| whose 95 % two-sided normal interval excludes 0 in the OLS regression
`r_i = c + k · Lw_i` of G1.2:

```
k_min = 1.96 · σ_r / sqrt( Σ_i (Lw_i − L̄)² )          σ_r = 0.465 (§4.2, registered, unchanged)
```

evaluated on **§4.1's own `Lw` column**. That this is *this document's* method, not an imported
one, is established by it reproducing three published numbers of the same lineage:

| set | n | recomputed here | published | source of the published value |
|---|---:|---:|---:|---|
| all 18 | 18 | **0.002158** | 0.00216 | **§4.2 itself** |
| CAL 8 | 8 | **0.020916** | 0.02092 | `docs/43` §3.2, nb19 |
| CAL 8 + ARRANCAPLUMAS | 9 | **0.003031** | 0.00303 | `docs/43` §3.1 P2 |
| **CAL 13** | 13 | **0.009640** | **§4.2 prints 0.0104** | — **does not reproduce** |

`docs/47` §2.2 reached the identical digits independently from a different agent's script (all-18
**0.002157**, CAL-8 **0.02092**).

### Five attempts to reproduce 0.0104, all failed

1. **A different z.** 0.0104 needs z = **2.115**; 1.96 is what the all-18 cell uses, and at 2.115
   that cell would read 0.00233, not 0.00216.
2. **A different σ.** 0.0104 needs σ = **0.5017**, not the registered **0.465**.
3. **A t-critical value.** df = n−2 ⇒ 0.01083; df = n−1 ⇒ 0.01072. Neither is 0.0104, and either
   moves the all-18 cell off 0.00216.
4. **A different 13 of the 18.** Exhaustive search of all C(18,13) = **8,568** subsets of §4.1's
   `Lw`: **zero** subsets give 0.0104 ± 5e-5.
5. **The joint form of G1 note 3** (`Lw` residualised on §4.1's Grassland and Bare shares): CAL 13
   ⇒ 0.01062 — still 2.1 % away — and it fails to reproduce the CAL-8 0.02092 (gives 0.02529), so
   the lineage's numbers are univariate. Hypothesis rejected.

**Sixth check, and it is decisive: `docs/43`'s own arithmetic runs on 0.00964.** P1 states that
losing the 5 stations costs a factor **2.2** and is **9.7×** worse than the all-18 guard.
0.020916 / 0.009640 = **2.170** (→ 2.2) and 0.020916 / 0.002158 = **9.693** (→ 9.7). At 0.0104 the
first factor would be **2.011** (→ 2.0), which is not what P1 prints. Every downstream consequence
already quoted in `docs/43` and `docs/45` was computed from 0.00964.

### RESOLVED

> **`docs/42` §4.2's CAL-13 cell is the wrong number. The correct value, at this document's own
> registered σ_r and its own `Lw` table and its own method, is `k_min` = 0.00964 /km.**
> `docs/43` P1's **number** is right. `docs/43` P1's **attribution** is wrong: it presents 0.0096
> as what `docs/42` printed, and `docs/42` printed 0.0104.
> `docs/agents/journal_adj-c4-feasibility.md:167` explained the gap as *"method rounding"*; **that
> explanation is withdrawn here** — 7 % is far outside 1-dp rounding of any input, and no method
> has been found that yields 0.0104. It is an arithmetic error, isolated to that one cell.

**A second, separate inconsistency inside the same cell, recorded and not repaired here:** the
CAL-13 row's contrast column uses the **max−min span** (exp(0.0104 × 107.8) = 3.068 → "3.06"),
while the all-18 and 22-pair rows use the **max `Lw`** (exp(0.00216 × 348.4) = 2.122 → "2.12";
exp(0.00119 × 348.4) = 1.514 → "1.51"). Corrected, the CAL-13 contrast is **2.83×** on its own
row's stated span convention, **2.90×** on the convention its two neighbours use.

**No verdict moves, and this is stated so the correction cannot be read as a rescue.** 0.00964 is
still **4.47×** the all-18 figure and still sits outside the 0.0020–0.0032 /km reference — which is
**UNCITED** and, per the standing rule, may pass or fail nothing either way (§4.2, unchanged). The
CAL-13-only test remains **underpowered** and remains rejected as the deposition test. The
correction moves the number 7 % in the *more powerful* direction and changes no verdict anywhere in
this document.

### The corrected table, for the station set actually in force

| test form | n | `k_min` /km | survival contrast over its own max `Lw` | status under A-P1 / A-P2 / A-P3 |
|---|---:|---:|---:|---|
| slope over the **CAL 8** — the fit set (A-P1) | 8 | **0.02092** | **3.54×** over 60.4 km | **not used to fit** — `k` is FIXED at 0 (A-P3); the number's job is to justify fixing it |
| **slope over all 18 — G1.2, the registered primary** | 18 | **0.00216** | **2.12×** over 348.4 km | **UNCHANGED and re-affirmed.** Still the deciding test |
| 22 nested pairs (stations shared ⇒ not independent) | 22 | 0.00119 | 1.51× | corroboration only, **unchanged**. Not recomputed here — the pair list is not printed in this document |
| ~~slope over the CAL 13~~ | 13 | ~~0.0104~~ → **0.00964** | ~~3.06×~~ → **2.83×** (span) / **2.90×** (max) | **SUPERSEDED by A-P1** *and* arithmetically corrected above |
| counterfactual: CAL 8 + ARRANCAPLUMAS | 9 | 0.00303 | 2.88× | **REJECTED by A-P2.** Printed so the 6.9× cost of that decision is visible |

> **MANDATORY POINTER, and it is not an amendment.** Every `k_min` above is **proportional to
> σ_r = 0.465**, and `docs/47` §2.2 (**D2**) measures the actual between-station residual sd on the
> CAL 8 at **1.9618 ln (×4.22)**, giving a corrected all-18 `k_min` of **0.0066–0.0069 /km
> (≈ 10× over 342 km)** and a corrected CAL-8 form of ~~**0.0130 /km**~~. **σ_r is a registered
> threshold and this pass does not touch it** — `docs/47` **B5** assigns that repair to a
> `docs/45` §8 amendment, by its owner. The table above is therefore corrected **at the registered
> σ_r**, and a reader must carry D2 alongside it. Re-basing the table on a threshold this pass has
> no standing to change would have been the convenient move and is refused.

> ⚠ **A-P4 (§9.7), 2026-08-12 — the struck `0.0130 /km` is WITHDRAWN, and this pointer's
> all-18 figures are CONFIRMED.** `0.0130` was transcribed from `docs/47` §2.2 and is
> **arithmetically impossible as labelled**: `k_min ∝ σ/√Σ(Lw−L̄)²`, so on a fixed station set a σ
> **4.22× larger** cannot produce a `k_min` **smaller** than the registered 0.02092. `docs/48`
> §4.3 traced it to the **10-station set that happens to have CAL-window observations, which
> includes the EVAL station `21237020` ARRANCAPLUMAS** (measured 0.01230 /km; ARRANCAPLUMAS alone
> supplies 87.6 % of that set's `Σ(Lw−L̄)²`), so a "CAL-8 form" containing it is mislabelled either
> way. **The correct CAL-8 figure is 0.0838 /km (≈ 173× over 61.5 km).** The all-18
> 0.0066–0.0069 /km (≈ 10× over 342 km) is independently reproduced (`docs/48` §4.2) and is what
> A-P4 enacts. B5's `docs/42` half is discharged by §9.7; its `docs/45` half remains owed.

---

## 9.6 — What this amendment does NOT do, and what is flagged to the document owners

**Untouched, explicitly:** every threshold in §5 and §6 (G1–G9); σ_r = **0.465**; the `b_obs` IQR
**0.464**; the pair-σ **0.658**; the β band **0.45–0.65**; G2.2's **+25 %**; G7's **+10 %**; G8's
**0.465 ln**; the primary estimator (b) and the G2.2 exception on (a); §3's non-separability
finding; §4.1's `Lw` table; §4.3–§4.5; §7; §8. **No frozen artifact was opened for writing**
(`sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv, q_gauge_H2E.npz}` untouched); **no
calibration was launched; no simulation was run; nothing is backdated; no git command was run.**
The only computation performed was the `k_min` arithmetic of §9.5, from §4.1's printed `Lw` values
and §4.2's registered σ_r, in a scratchpad script that wrote nothing into the repository.

**Flagged for the document owners / orchestrator — deliberately NOT edited by this pass:**

| # | flag | recommended action |
|---|---|---|
| **F1** | **§4.2's body still prints `0.0104` and `3.06×`** in the CAL-13 row. This pass may write only in the §9 amendment slot, so the wrong number is still quotable from the body. | Apply the **`docs/37` A2.7 precedent**: strike-through + pointer **in place**, nothing deleted, so the retired number cannot be quoted from the body. §4.2's following paragraph (*"the 13-station test's 0.0104 /km does not"*) needs the same treatment — its **conclusion survives** at 0.00964. |
| **F2** | **`docs/43` §3.1 P1 mis-attributes 0.0096 to `docs/42`** (*"is 0.0209 /km, not 0.0096 /km"*). Its number is right; its attribution is wrong. | One-line correction in `docs/43`, e.g. *"not 0.00964 /km (`docs/42` §4.2 mis-printed this as 0.0104; corrected in its §9.5)"*. Not this pass's file. |
| **F3** | **`docs/agents/journal_adj-c4-feasibility.md:167`** explains the 7 % gap as *"method rounding"*. Withdrawn by §9.5. | Record the withdrawal where that journal is next cited. |
| **F4** | **`docs/47` open item O7** (*"the B4 transcription must pick one and record why"*) is answered by §9.5. | O7 may be **CLOSED**: 0.00964 is correct, `docs/42` §4.2 was wrong, reason recorded. |
| **F5** | **`docs/47` §2.4 D4** (this transcription unperformed) is discharged by §9.1–§9.5. | D4 may be **CLOSED**. `docs/47` B5 (the σ_r / Π-band repair) is **NOT** discharged and remains open. |
| **F6** | **`docs/00_INDEX.md`** carries no row for this amendment log, and its status table still describes `docs/42` as unamended. | Add the pointer when the index is next synced. |

---

## 9.7 — AMENDMENT A-P4 · 2026-08-12 · **σ_r's REUSE as a per-station residual sd is RETIRED**; the level band and the `k` power restated

**Written by the `amend-4243-piband` agent; process record
`docs/agents/journal_amend-4243-piband.md`.** **Source:** `docs/47` §2.2 (**D2**), the finding;
`docs/48_pi_band_revision.md`, the measurement and the blast radius. This amendment **enacts the
`docs/42` half of `docs/47` §6.1 repair B5.** Its `docs/45` half — the band replacement, G12's
decoupling and the corrected `k` wording in `docs/45` §2.3 — is a `docs/45` §8 amendment and
remains owed to that document's owner. The `docs/43` half is enacted the same day in `docs/43` §7.

**What this amendment does NOT do, stated before anything else, because the temptation is real:**
it does **not** create, restate, rescale or imply a **materiality bar**. `docs/52` STRUCK
`0.1644 ln` and replaced it with **no number**; the corrected SEs printed below (0.4775 / 0.6936)
and the bootstrap half-widths (0.8500 / 1.2833) are **band widths for reporting an interval**, and
**no session may read any of them as a threshold for deciding whether two numbers differ.** It
also changes **no threshold in §5 or §6**, alters **no** registered station set, moves **no**
engine default, and fits nothing.

### 9.7.1 — The defect, stated in one paragraph

§4.2 registers `σ_r = 0.465 ln` and derives it, correctly, as the disagreement between the **two
independent observed-flux estimators** of `docs/34`: `sd[ln(a/b)] = 0.658` over 32 station-windows,
so one estimator carries `0.658/√2 = 0.465`. **Neither estimator has seen the model.** The
quantity the SE of a fitted level and every `k_min` actually require is the sd of
`r_i = ln(flux_sim_i) − ln(flux_obs_i)` — §2's own residual — whose variance contains observation
error **plus model error plus genuine between-station heterogeneity**. It is bounded **below** by
the observation term and is never equal to it. Substituting one for the other is **not a
conservative approximation**; it is an error in one known direction, and `docs/47` §2.6 item 3 has
already measured the heterogeneity term separately (**I² 96 – 99.2 %, τ 2.03 – 3.40× per
station**).

### 9.7.2 — Which uses survive and which do not, **by name**

| use of `0.465` / `0.658` in this document | status under A-P4 | why |
|---|---|---|
| **σ_r = 0.465 as the estimator-disagreement statistic** (§4.2 derivation; §9's yardstick cell) | **VALID — unchanged, still registered** | `0.658/√2` is correct for what it measures. It is the **reuse**, not the number, that is retired. |
| **pair-σ = 0.658 ln**, and **G1.1's `median D_pair > +0.658` firing threshold** (§6 G1.1) | **VALID — unchanged** | a *firing* threshold: too tight makes the guard **more** trigger-happy, i.e. it errs safe (`docs/47` R4). |
| **G8's `range across months > 0.465 ln`** (§6 G8) | **VALID — unchanged** | same; a firing threshold erring safe. |
| **`b_obs` between-station IQR = 0.464** (§4.3) | **UNAFFECTED** | independently measured from `ssc_rating_fits.csv`; its near-equality with 0.465 is a coincidence of value, not a shared derivation. |
| **σ_day = 0.809 ln** and everything built on it, incl. **SE(β) = 0.0199 / half-width 0.039** | **UNAFFECTED** | built on the rating residual, not on σ_r (`docs/47` §2.2, R4 — which **narrows** the original finding's word *"every"*). |
| **`0.465/√n` as the SE of a fitted level** (`docs/43` §3.2; `docs/45` §2.2/§3.1/§5.3/§6.2/§7.1; `docs/37`:1158) | **RETIRED — INVALID** | wrong error term (§9.7.1). |
| **`k_min = 1.96·σ_r/√Σ(Lw−L̄)²`** — every cell of §4.2's power table, §9.5's recomputation, §6 G1.2's "≈ 2.1× at best", §9.3's and §9.4's CAL-8 figures | **RETIRED as to the NUMBER; the FORMULA is unchanged and re-affirmed** | the formula is right and is what makes the correction exact and linear; only the σ substituted into it was wrong. |
| **ratios between two σ_r-scaled `k_min` values** — §9.3's factor **6.9**, §9.5's **2.2×** and **9.7×** | **SURVIVE UNCHANGED** | σ cancels. Measured: 0.0838/0.01210 = **6.926**. **Do not "correct" these.** |
| **`0.1644 ln` as a materiality bar** (`docs/46`, its bar sites) | **already STRUCK, not rescaled** (`docs/52`) | not this document's number and not re-derived here. A-P4 offers no replacement. |

### 9.7.3 — The measurement, and its reproduction gates

Carried from `docs/48` §2, which reproduced it from scratch behind two gates that both passed
**before** any statistic was computed — basin gross hillslope erosion **299.5387088 Mt/yr** against
`docs/37` A1.3.4's 299.5387, mass ledger `exact = True`; CAL-8 paired SSC + observed-Q day count
**3,266** against `docs/45` §3.6 — and which reproduced §4.1's model up-areas at **all 18**
stations, so the station→minibacia mapping is not in question.

| quantity, registered CAL window 2012-01-01 … 2014-12-31, CAL 8 | registered | **measured** | factor |
|---|---:|---:|---:|
| per-station residual sd, primary estimator **(b)** | 0.465 ln | **1.9618 ln** | **×4.22** |
| per-station residual sd, estimator (a) | 0.465 ln | **1.3506 ln** | ×2.90 |
| SE of the fleet-mean level, est (b) | **0.1644 ln** | **0.6936 ln** | ×4.22 |
| SE of the fleet-mean level, est (a) | 0.1644 ln | **0.4775 ln** | ×2.90 |
| 95 % normal band on the level, est (b) | ±38 % (×0.724 – ×1.380) | **×0.257 – ×3.894** | log width ×4.22 |

**Reproduced independently by this pass** (`python3.10`, scratchpad, nothing written into the
repository): `0.465/√8` = **0.16440232662587229**; `1.9618/√8` = **0.6936010416658844**;
`1.3506/√8` = **0.4775092093352755**; `1.9618/0.465` = **4.2189247311827955**;
`exp(±1.96 × 0.1644)` = **0.7245 – 1.3802**; `exp(±1.96 × 0.6936)` = **0.2568 – 3.8941**. The
mechanism is exact rather than approximate, which is why the correction is a multiplication:
`1.96·σ_r/√Σ(Lw−L̄)²` on §4.1's own printed `Lw` column reproduces this document's registered
`k_min` to the printed digits (all-18 **0.002157** vs 0.00216; CAL-8 **0.02092** vs 0.0209).

**The scale of the underlying heterogeneity, printed because it is the reason the band is wide and
not a defect that a fit can remove:** per-station `obs/sim` on the CAL window spans
**0.0099 – 4.077**, a factor of **412** (`exp(6.0214)` = 412.16, reproduced this pass). **The band
is invariant to the fit and the point is not** — fitting Π removes a constant from every `r_i`,
which moves the mean toward 0 and leaves the sd, hence the SE, hence the band, untouched.

### 9.7.4 — The `k` bound, restated at its corrected power

> ## THE CORRECTED SENTENCE — registered reporting form
>
> ```
> k_min = 0.0066 - 0.0069 /km      (all 18, G1.2's registered joint form, measured residual sd)
> ```
> > **"No first-order channel sink *weaker* than ≈ 10× over ~342 km is *detectable* on this fit
> > set."**  *(equivalently: `|k| < 0.0069 /km` cannot be distinguished from zero)*
>
> **Registered: 0.00216 /km ⇒ 2.12× over 348.4 km. Corrected: ≈ 9× – 11×, central ≈ 10×.**

**Provenance and the exact spread, so the interval is auditable.** `docs/48` §4.2 fits G1.2 in the
**joint** form this document's own G1 note 3 requires (`Lw` + G3.1's class shares + G4.1's
`ln LS̄`, one multiple regression) on all 18, on recomputed predictors: `+ Lw` alone
**0.00666 /km**, `+ shG, shB` **0.00657**, **the registered joint form 0.00686**; and by §4.2's own
univariate formula on **§4.1's printed `Lw` table** **0.00694** (joint-form sd) / **0.00658**
(intercept-only sd). So the constructions span **0.00657 – 0.00694 /km**; `docs/47` §2.2 prints the
interval as **0.0066 – 0.0069** and `docs/48` §4.2's corrected sentence as **0.0065 – 0.0069**.
**Both are the same measurement rounded differently; this amendment registers `0.0066 – 0.0069`
with `0.00686` as the central value and records the construction span above so the two printings
cannot be mistaken for two results.** Survival contrasts reproduced this pass:
`exp(0.00686 × 341.5)` = **10.409**, `exp(0.0066 × 342)` = 9.68, `exp(0.0069 × 342)` = **10.589**,
`exp(0.00694 × 345.8)` = **11.022**, `exp(0.00658 × 345.8)` = **9.731**.

**The comparative, settled.** `k_min` is a **detection floor**. With the verb *detectable* the true
comparative is **weaker** (a sink with `|k| < k_min` leaves no visible trace); with the verb
*excluded* it is *stronger* ("no sink stronger than X× is consistent with these residuals"). §6
G1.2, §9.4 and `docs/45` §2.3 all pair **"stronger"** with **"detectable"**, which asserts the
opposite of what the statistic supports. **A-P4 registers the `weaker` / `detectable` pairing as
the reporting form for this document**; the identical repair in `docs/45` §2.3 and its G1.2 row is
owed to `docs/45`'s owner (`docs/48` §4.2 flags the same defect).

**What the corrected bound means for the SDR = 1.0 claim (A-P3, G5 option 2), stated so it is not
over- or under-read.** The claim is unaffected **in form** and **weakened in evidence**: the guard
that would betray a missing sink cannot see anything weaker than ≈ 10× over the basin's longest
observed path, against ≈ 2.12× as registered. The coefficient moves **×3.18** (0.00216 → 0.00686)
and the survival contrast the registered sentence actually prints moves **×4.90** (2.12 → 10.41).
**The claim stands as a claim. It stands on less.**

### 9.7.5 — EVERY PUBLISHED NUMBER THAT CHANGES

Rows are grouped by disposition. **"ENACTED here"** means this amendment applies it, with the
in-place strike-through or pointer listed in §9.7.7. **"Owed"** means the number lives in a file
this pass does not own; the correction is named, not applied. **"No corrected value"** means the
number is wrong and no replacement is offered — those rows are the honest core of this table.

**(A) The level band and its derivatives**

| # | document · section | old value (as published) | new value |
|---|---|---|---|
| 1 | `docs/43` §3.2, Π row (:191) | SE = `0.465/√8` = **0.1644 ln = ±38 % at 95 %** (0.724× – 1.380×) | SE **0.4775** (est a) / **0.6936** (est b); band = the **station bootstrap**, `Π̂ × [0.29, 3.73]` — **ENACTED 2026-08-12 in `docs/43` §7, amendment 1** |
| 2 | `docs/43` §3.2, Π row (:191) | *"13 stations would have given **±28.8 %**"* | **NO CORRECTED VALUE.** The 13-station residual set does not exist — only 8 of the 13 have a paired CAL-window day at all (A-P1). Struck, not restated — **ENACTED in `docs/43` §7** |
| 3 | `docs/43` §1.2, lens-3 row (:52) | *"a **±38 %** 95 % band"* | as row 1 — **ENACTED in `docs/43` §7** |
| 4 | `docs/45` §2.2 (:124), §3.1 (:252), §5.3 (:494), §7.1 card (:575) | **0.1644 ln = ±38 %** | as row 1 — **OWED to `docs/45` §8** (its owner) |
| 5 | `docs/45` §6.2 item 2 (:541) | *"**The level's band is ±38 %** … Every Π and every load is quoted **with that band**"* | **the mandatory sentence itself changes.** `docs/47` §2.2 notes this is the one site carrying **no hedge** — **OWED to `docs/45` §8** |
| 6 | `docs/45` §4.2, **G12** (:445) | *"the registered 95 % level band of **±0.322 ln (±38 %)**"* | **DECIDE, DO NOT RESCALE.** Recommended (and adopted by `docs/43` §7 amendment 1 for its own purposes): keep **0.644 ln full width as a standalone registered fragility threshold**, decoupled from the level band, recording that it was originally derived from `σ_r/√8`. Rescaling it switches a **firing** guard off — **OWED to `docs/45` §8** |
| 7 | `docs/37`:1158 (A2.4) | SE = `0.465/√8` = **0.1644 ln = ±38 %** | as row 1 — **OWED to `docs/37`'s owner** |
| 8 | `docs/46` (its bar sites) | **0.1644 ln** as a materiality bar and Branch A/B discriminator | **already STRUCK, not rescaled** (`docs/52`). **No number replaces it.** Nothing owed here, and nothing may be reconstructed |

**(B) Every `k_min` and every survival contrast** — all linear in σ_r

| # | document · section | old value | new value |
|---|---|---|---|
| 9 | **`docs/42` §4.2 table and §9.5's corrected table** — all-18 G1.2 | **0.00216 /km ⇒ 2.12×** over 348.4 km | **0.0066 – 0.0069 /km (construction span 0.00657 – 0.00694; central 0.00686) ⇒ ≈ 9× – 11×, central ≈ 10× over ~342 km** — **ENACTED here** |
| 10 | **`docs/42` §4.2 / §9.3 / §9.4 / §9.5** — CAL-8 form | **0.02092 /km ⇒ 3.54×** over 60.4 km | **0.0838 /km ⇒ ≈ 173×** over 61.5 km (**0.0883 ⇒ 164×** on §4.1's printed `Lw`, span 57.8 km) — **ENACTED here** |
| 11 | **`docs/42` §9.5's MANDATORY POINTER** | *"a corrected CAL-8 form of **0.0130 /km**"* | **WITHDRAWN.** Arithmetically impossible as labelled; it is the **10-station** CAL-window set including the EVAL station ARRANCAPLUMAS (measured **0.01230 /km**). Correct CAL-8 value **0.0838 /km** — **ENACTED here** (struck in place) |
| 12 | `docs/42` §4.2 / §9.5 — CAL-13 | ~~0.0104~~ → **0.00964 /km ⇒ 2.83× / 2.90×** (A-P1.1) | **NO σ-CORRECTED VALUE.** A-P1.1's 0.00964 stands **at the registered σ_r** and is *not* contradicted here; a CAL-13 residual set does not exist, so the row cannot be σ-corrected. It is already **SUPERSEDED by A-P1**. **Flag, do not recompute** — the strike-through F1 asked for is **ENACTED here** |
| 13 | `docs/42` §4.2, §9.5 — 22 nested pairs | **0.00119 /km ⇒ 1.51×** | **NO CORRECTED VALUE.** The pair list is printed in no document and `Σ(ΔLw − ΔL̄)²` is not reconstructible from what is published. **Open item P2** — **flagged here** |
| 14 | `docs/42` §9.3 / §9.5 — CAL 8 + ARRANCAPLUMAS | **0.00303 /km ⇒ 2.87× / 2.88×** | **0.01210 /km ⇒ 62.3×** over 341.5 km, on that 9-station set's own CAL-window residuals (sd 1.8361). **The factor 6.9 SURVIVES**: 0.0838/0.01210 = **6.926** — **ENACTED here** |
| 15 | `docs/42` §6 G1.2, "neither fires" cell | *"At the registered σ_r that bound is ≈ **2.1×** at best"* | **≈ 10× over ~342 km**, and the comparative corrected to *weaker/detectable* — **ENACTED here** (power figure only; **the guard's thresholds are untouched**) |
| 16 | `docs/43` §3.2, `k` row (:193) | **0.0209 ⇒ 3.54×**, **0.00303 ⇒ 2.87×**, **0.00216 ⇒ 2.12×** | rows 9, 10, 14 — **ENACTED 2026-08-12 in `docs/43` §7** |
| 17 | `docs/45` §2.2 (:126), §2.3, §4.2 G1.2 (:429), and (:162), (:202), (:205) | the same `k_min` set and the *"no sink stronger than X× … detectable"* wording | rows 9, 10, 14 + the comparative — **OWED to `docs/45` §8** |
| 18 | `docs/42` §4.2's scale-reference sentence | *"the 18-station test's 0.00216 /km sits **inside** the range that matters"* | **INVERTS**: at 0.0066 – 0.0069 /km it sits **above** the whole 0.0020 – 0.0032 /km reference. **The band is UNCITED and passes or fails nothing either way**; the sentence's conclusion is unchanged — **ENACTED here** |
| 19 | `docs/37`:1155 — the **2.2×** and **9.7×** ratios; `docs/42` §9.3's **6.9** | unchanged | **THESE SURVIVE.** They are ratios of two σ-scaled `k_min` values; σ cancels. Recorded so they are not "corrected" by mistake |

**(C) Numbers that are wrong with no replacement offered — the open-item rows**

| # | document · section | number | disposition |
|---|---|---|---|
| 20 | `docs/43` §3.2 (:194); `docs/45` **G3.3** | minimum detectable class-C error **≈ ×4.2** (CAL 8) / **≈ ×2.9** (all 18) | **NO CORRECTED VALUE — `docs/47` open item O8, and it stays open.** Three passes have now produced three answers (×4.2/×2.9 registered; ×8.2/×3.2 `journal_refute-gate-logic`; ×5.58/×3.53 at the registered σ and ×251.6/×57.9 at the measured σ on `docs/48` §6.2's stated design matrix). **The only quotable statement is qualitative: they are σ_r-scaled and the registered figures are too optimistic by roughly the σ_r factor.** Do not invent a number — **flagged in `docs/43` §7** |
| 21 | `docs/42` §4.1's `Lw` column and land-class erosion shares | IRRA 265.2, BANANERA 26.9, CAPITANEJO 60.4, CARRASPOSO 39.0, ARRANCAPLUMAS 348.4; BANANERA 11.9/12.5/75.6 %, CAPITANEJO 2.4/37.9/58.4 % | **DO NOT REPRODUCE** at the adopted `cp_revision` (`docs/48` §2.5: IRRA **289.14**, +9.0 %; BANANERA **24.19**; shares move because `docs/41`'s ×1.2043 `C` revision is not uniform across classes). Probable cause: §4.1 was measured at the **prior** `cp_revision` — §4.5 prints basin total **248.7 Mt/yr**. **Immaterial to every conclusion here** (`k_min` moves ≤ 2 % between the two tables, and §9.7.4 reports both). **A recomputation is OWED** — flag F8. **Not corrected here: this pass has not measured it.** |

### 9.7.6 — What does NOT change, restated in one place

σ_r = **0.465** as an estimator-disagreement statistic · the pair-σ **0.658** · the `b_obs` IQR
**0.464** · σ_day **0.809** and SE(β) **0.0199** · **every threshold in §5 and §6** (G1–G9),
including G1.1's `+0.658`, G8's and G11's `0.465 ln` · the β band **0.45 – 0.65** · G2.2's +25 % ·
G7's +10 % · the registered primary estimator (b) and the G2.2 exception on (a) · §3's
non-separability finding · the registered station sets as amended by A-P1/A-P2 · A-P3's `k` = 0 ·
the `k_min` **formula** · §4.3 – §4.5 · §7 · §8 · G12's **0.644 ln** full width **as a standalone
fragility threshold** · every ratio in row 19.

> **CAUTION, carried from `docs/48` §5.4 and not a correction.** `docs/47` R4 is right that a
> threshold set ~4× too tight makes G8 and G11 **more** likely to fire, which is the safe
> direction for a guard. But the measured residual scale makes firing near-certain: at a
> per-station residual sd of 1.35 – 1.96 ln, a between-month or between-region difference of
> 0.465 ln is well inside ordinary sampling noise at n = 8. **A guard that fires by construction
> is not a test either.** G8 and G11 are frozen thresholds, this amendment has no standing to
> touch them and does not, and **no number is proposed**. It is recorded so that a G8 or G11 FAIL
> is read for what it is.

### 9.7.7 — In-place corrections applied to the body by this pass (§9.6 **F1**'s remedy, discharged)

`docs/42` §9.6 flag **F1** recorded that §4.2's body still printed the retired numbers because
that pass could write only in §9, and prescribed *"the `docs/37` A2.7 precedent: strike-through +
pointer in place, nothing deleted"*. **Applied, at these sites, nothing deleted, every original
string still readable inside its strike-through:**

| site | what was applied |
|---|---|
| §4.2, the REGISTERED NOISE FLOOR blockquote | inline `[WARN] A-P4` block: the phrase *"per station log-residual"* retired, the number kept |
| §4.2, the power table (CAL-13, all-18, 22-pair rows) | strike-through + corrected values in the cells; `[WARN] A-P4` block under the table separating the **arithmetic** correction (0.0104 → 0.00964, A-P1.1) from the **σ** correction (all-18) |
| §4.2, the scale-reference paragraph | *"sits inside the range that matters … 0.0104 /km does not"* struck; `[WARN] A-P4` block recording the inversion **and** that the band is UNCITED and decides nothing |
| §6 **G1.2**, "neither fires" cell | *"≈ 2.1× at best"* struck → ≈ 10×; `[WARN] A-P4` block below the table with the comparative correction. **No threshold cell touched** |
| §9's registration table — *Registered yardsticks* | pointer appended to the σ_r cell (reuse retired, number kept) |
| §9's registration table — *Amendments* | A-P4 added to the list |
| §9.2's *"keeps `k_min` = 0.00216 /km"* re-affirmation | number struck + pointer; A-P1's substantive claim (all 18) untouched |
| §9.3's factor-**6.9** paragraph | pointer: both endpoints move, **the ratio survives**, do not correct the 6.9 |
| §9.4's *"only a sink stronger than 3.54× would be detectable"* | pointer: the reason for fixing `k` at 0 gets **stronger** (≈ 173×), plus the comparative flag |
| §9.5's MANDATORY POINTER | **`0.0130 /km` struck** and withdrawn, with the trace to the 10-station ARRANCAPLUMAS set; the all-18 figures confirmed |

### 9.7.8 — Flags and open items

| # | flag / open item | disposition |
|---|---|---|
| **F1** (§9.6) | §4.2's body still printed 0.0104 / 3.06× | **DISCHARGED** by §9.7.7 |
| **F7** *(new)* | **`docs/42`:15, :299 and :472 print the deposition-free α band `6.83 – 8.73`**, which `docs/47` §2.5 **C1** measures as a **prior-`cp_revision`** number: at the adopted C it is `11.8 × {144,184}/299.5387088405831` = **5.673 – 7.248** (reproduced by this pass), which is **disjoint** from the reading-B band 7.92 – 8.86 (gap **0.672** in α). **NOT corrected here** — it is not a σ_r number and belongs to a different repair; A-P4 will not smuggle an unrelated enactment into its own slot. | **OWED as a further `docs/42` amendment.** The parallel correction to `docs/43` §3.4 **is** enacted 2026-08-12 in `docs/43` §7 (amendment 5), with `docs/47` **O12** recorded as still open |
| **F8** *(new)* | **§4.1's `Lw` table and land-class shares do not reproduce at the adopted `cp_revision`** (row 21; `docs/48` §2.5, its open item P3). G3.1's regressors are read off that table. | **OWED to this document's owner:** one recomputation at the adopted `cp_revision`. Immaterial to A-P4 (`k_min` moves ≤ 2 %; both tables reported) |
| **F9** *(new)* | **`docs/45` §8 read *"Empty at registration"* when this pass read it.** B5's `docs/45` half (rows 4, 5, 6, 17), the corrected `k` wording, G12's decoupling and `docs/47` §5.5's pre-fit-profile disclosure are all owed there. A `docs/43` amendment written the same day **names** that amendment rather than pre-empting it. | **OWED to `docs/45`'s owner.** If the two disagree, `docs/45` §8 wins on its own §2–§6 and `docs/43` §7 records the conflict — see `docs/43` §7 amendment 1 |
| **P1** (`docs/48`) | **Which estimator's band is binding** — §9 registers **(b)** as primary; `docs/45` §7.1 registers the objective on **(a)**. Their bootstrap bands differ by a factor of **1.51** in log width (2.5666 vs 1.7000 ln). | **OPEN.** A `docs/45` §8 decision. `docs/43` §7 adopts the **union** as a reporting convention and says so |
| **P2** (`docs/48`) | The **22-pair `k_min` 0.00119 /km** cannot be corrected (row 13). | **OPEN** |
| **O7** (`docs/47`) | the 0.0096-vs-0.0104 discrepancy | **CLOSED by §9.5** (0.00964). A-P4 does not reopen it and is written to be consistent with it |
| **O8** (`docs/47`) | class-C detectability ×4.2 / ×2.9 (row 20) | **OPEN, and this amendment deliberately adds no fourth number** |
| **O12** (`docs/47`) | whether C1's now-disjoint bands change the "doubly load-bearing" G5 conclusion | **OPEN.** See F7 and `docs/43` §7 amendment 5 |
| **P5** (`docs/48`) | the band is **β-dependent** — CAL-8 est-(b) sd rises monotonically 1.875 → 2.100 across the registered β box | **OPEN, and it is why the replacement is registered as a PROCEDURE, not as a frozen pair of numbers.** C4 recomputes it on its own adopted fit's residuals |

### 9.7.9 — Disclosure

- **Files written by this pass:** `docs/42_c4_guards.md` (this §9.7 plus the §9.7.7 in-place
  pointers), `docs/43_c3_c4_gate.md` (its new §7), and
  `docs/agents/journal_amend-4243-piband.md`. **Nothing else.** `docs/35`, `docs/37`, `docs/45`,
  `docs/46`, `docs/47`, `docs/48`, `docs/51`, `docs/52`, `docs/53` were **read and not edited**.
- **No threshold in §5 or §6 was altered**; the only §6 edit is the strike-through of a **reported
  power figure** in G1.2's "neither fires" cell plus a pointer block beside the table, both named
  in §9.7.7. No registered station set, estimator, box or parameter count moved.
- **No engine default was changed** — `ls2d_column`, `cp_revision`, `volume_convention`,
  `k_unit_system` and every `SedParams`/H2E field untouched. **No frozen artifact was opened for
  writing** (`sim_calibrated_v2/*` was not opened at all by this pass). **No calibration or fit was
  launched, no simulation was run, no `KGE_ln` was evaluated against the `docs/45` α box, and no
  α̂ was quoted, provisional or not.** No git command was run. Nothing is backdated.
- **What this pass measured itself**, in a scratchpad script that wrote nothing into the
  repository: the SE arithmetic, the band factors, the G12 half-width and LOO identity, the
  survival contrasts at every published `k_min`, the 6.926 ratio, the CAL-13 contrasts at 0.00964,
  and `docs/47` C1's α endpoints at the adopted C. Every one is printed with its input above or in
  `docs/agents/journal_amend-4243-piband.md`. **Everything else is carried from `docs/47` or
  `docs/48`, cited in place, and is not re-derived.**
- **One thing this pass checked and it matters for anyone applying the replacement band:** the
  bootstrap **band on the level multiplier is the RECIPROCAL of the bootstrap CI on the residual**.
  `exp(−0.8279), exp(+0.8721)` = 0.4370, 2.3919 does **not** match `docs/48` §3.3's printed band
  ×0.418 – ×2.289; `exp(−hi), exp(−lo)` = **0.41807, 2.28851** does, and est (b)
  `exp(−1.2503), exp(+1.3163)` = **0.28642, 3.72960** matches ×0.286 – ×3.730. `docs/48`'s printed
  bands are therefore **correct**, and the sign flip is **implicit** in them: `r_i = ln(sim/obs)`,
  so a positive residual means the level must come **down**. Applying the CI without the flip
  inverts the band. **Stated here because §9.7.5 row 1 hands that band to two other documents.**
- **Uncited quantities are named and pass or fail nothing:** the 0.05 – 0.30 SDR band and its
  implied `k ≈ 0.0020 – 0.0032 /km` (row 18) and the ENSO-neutrality of CAL 2012–14. **No
  plausibility band was invented, and no materiality bar was created, restated or implied**
  (`docs/52`).
- **The `docs/23` §13.2 yield embargo is in force.** No t/km²/yr appears in this amendment.

---

## 9.8 — AMENDMENT A-P5 · 2026-08-19 · **"at adopted defaults" in §4 and §9 names the PRIOR `cp_revision`, not the adopted one**

**Written 2026-08-19 by the corpus coherence sweep.** **This document is FROZEN; §1–§8 are not
edited and no threshold in §5 or §6 is touched.** This entry is written in the §9 slot the document
reserved for exactly this ("*Amendments go in §9, dated, with a reason*", §0). It corrects a
**label**, not a measurement, and it introduces **no number of its own** — every figure below is
quoted from `docs/37` or read from `src/mgb_sediment.py`.

### 9.8.1 — The reason

§4's provenance line and the §9 registration card's **"Measured before registration"** row both
attribute their inputs to *"one read-only run of `src/mgb_sediment.py` **at adopted defaults**
(basin total **248.696 Mt/yr**, mass ledger `exact = True`)"*.

**That phrase was true of the engine on 2026-08-11 and is not true of the engine now.** Read on
disk 2026-08-19: `src/mgb_sediment.py`:708 — `DEFAULT_CP_REVISION = "cited_central_2026_08_11"`,
and `load_geometry(cp_revision=DEFAULT_CP_REVISION)` at `:923`. At that default the basin total is
**299.5387088405831 Mt/yr** (`docs/37` A1.3 and its table at `docs/37`:518). The level printed in
§4 — **248.696 Mt/yr**, and its `docs/37` §2 sibling **248.730 / 248.7298 Mt/yr**, which §4's own
parenthesis already explains as a days-per-year divisor difference — is the
**`cp_revision='prior_2026_08_11'`** level (`docs/37`:519, :538).

**So the words "at adopted defaults" in §4 and §9 now point at the *prior* revision.** Left
unlabelled, they invite a reader to quote 248.696 Mt/yr as the current adopted basin level. It is
not.

### 9.8.2 — What is registered here

> **READ §4's and §9's provenance line as: `cp_revision='prior_2026_08_11'`,
> `volume_convention='williams_m3'`, `k_unit_system='us_customary'`.**
>
> **The adopted level is 299.5387088405831 Mt/yr at `cp_revision='cited_central_2026_08_11'`**
> (`docs/37` A1.3). **248.696 Mt/yr is NOT retired and NOT struck** — it is the level the §4
> measurements were actually taken at, and a measurement must keep its own provenance. What changes
> is the **label on it**, and this amendment supplies the label the frozen body cannot.
>
> **The house rule, restated because this defect is what it exists to prevent:** *never quote a
> load without its **convention** and its **`cp_revision`***. Both must travel (`docs/37` §prohibition 6).

### 9.8.3 — What this amendment does NOT do

- **It does not recompute anything at the adopted revision.** That recomputation was already owed
  before this entry and is **still owed**: **F8** (§9.7.8) — *"§4.1's `Lw` table and land-class
  shares do not reproduce at the adopted `cp_revision` … **OWED to this document's owner:** one
  recomputation at the adopted `cp_revision`"* — with the measured non-reproduction in **§9.7.5
  row 21** and `docs/48` §2.5 / its open item **P3**. **A-P5 discharges the LABELLING half of F8
  and leaves the ARITHMETIC half open.** F8 stays open.
- **It does not edit §4 or §9's body text.** The freeze forbids it, so the correction lives here and
  is reachable from the §9 card's Amendments row. *(A reader who lands on `:171` or `:645` without
  passing §9 will still read the unlabelled phrase — recorded as a residual exposure rather than
  fixed by a body edit this amendment is not authorised to make.)*
- **It does not touch F7's α band** (`6.83 – 8.73` at `:15`, `:299`, `:472`), which is the *same
  family of defect* — a prior-`cp_revision` number printed unlabelled — and is separately **OWED**
  (§9.7.8 F7, `docs/47` §2.5 C1, `docs/47` **O12**). A-P5 will not smuggle that enactment into its
  own slot, for the reason A-P4 gave when it declined the same thing.
- **It introduces no band, no threshold and no materiality bar**, and reconstructs none (`docs/52`).
- **The `docs/23` §13.2 yield embargo is in force.** No gauge-referenced t/km²/yr appears here.

### 9.8.4 — Status pointer (changes nothing registered)

**The guard set has since been exercised.** Stage **C4.3 has run**: `docs/55_c43_verdict.md`
(2026-08-12) is its deliverable and owns its verdict — **RAILED / EXPLORATORY, not adopted**, the
in-box optimum on the box floor α = 2.0, median `KGE_ln` −0.118 on estimator (a) and +0.139 on
estimator (b), unconstrained optimum α ≈ 0.48 below the floor, design-matrix condition number
**`inf`**. `docs/55` reports in this document's **G6** form — α is the handle on Π and is never
reported alone. Recorded here **only** so a reader of a frozen pre-registration knows the stage it
gates is no longer pending. **No guard, threshold, station set, estimator or parameter count is
altered by this pointer, and no C4.3 number should be quoted from this document — quote `docs/55`.**

### 9.8.5 — Disclosure

- **Files written by this pass:** this §9.8 and the pointer appended to the §9 card's **Amendments**
  row. **Nothing else in this document.** `docs/33`, `docs/35`, `docs/37`, `docs/45`, `docs/46`,
  `docs/48`, `docs/51`–`docs/58` were **read and not edited**.
- **No threshold in §5 or §6 was altered. No §1–§8 text was edited or deleted. No number was
  recomputed, no fit or simulation was run, no notebook was executed, no engine default was moved,
  no frozen artifact was opened, and no git command was run. Nothing is backdated.**
- **Two read-only measurements only:** `DEFAULT_CP_REVISION` and the `load_geometry()` signature in
  `src/mgb_sediment.py`. Every load figure is quoted from `docs/37` with its section named.
