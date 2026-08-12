# 45 — C4.2: the sediment calibration PRE-REGISTRATION

**Stage:** C4.2 of `docs/31_phase_c_workplan.md`.
**Status: PRE-REGISTRATION. FROZEN ON WRITE, 2026-08-11**, by the `c42-prereg` agent
(process record: `docs/agents/journal_c42-prereg.md`).

> **Written before any C4 search machinery exists, before any α or β has been fitted, and
> before any sediment objective has been evaluated once.** Every threshold, bound, station
> list, window, seed and decision rule below is fixed. **Nothing may be searched until this
> document exists**, and nothing in §2–§6 may be edited after a number it judges has been
> computed. **Amendments go in §8, dated, with a reason.** If a rule here turns out to be
> wrong, the measuring session **journals it as an issue and follows it anyway**: a threshold
> changed after seeing the number it judges is not a threshold.

**This document contains no fitted number and no new measurement.** Every quantity in it is
carried from a prior document or from the three adjudication lenses of `docs/43`, cited in
place. The two things this pass read from disk are station properties, not results, and are
disclosed in §7.3.

---

## 0 — What C4 is, in one paragraph, and what changed since `docs/31` registered it

C4 fits the MUSLE level and its event exponent to observed suspended-sediment flux at
tributary stations, over neutral years, with both ENSO windows held strictly out of sample,
and then submits the fit to a battery of residual-**structure** tests that a scalar parameter
cannot pass by absorbing anything. Three things have changed since `docs/31` §C4.2 sketched
it, and all three make C4 **smaller** than it was registered to be:

| `docs/31` §C4.2 registered | this document registers | why |
|---|---|---|
| three free parameters {α, β, deposition coefficient} | **two free** {α (as the handle on Π), β} **+ one FIXED at zero and reported as a bound** | lens 3 (`docs/43` §3.2): `k` is **not identifiable** on the achievable fit set (`k_min` 0.0209 /km). Reporting a fitted `k` would be reporting noise with a decimal point. `docs/43` §3.1 **P3**. |
| "the C1-usable tributary set" (13 stations) | the **CAL 8** — 5 of the 13 have **no paired SSC + observed-Q day** in the CAL window | `docs/43` §3.1 **P1**, measured by lens 3. |
| upper-mainstem stations upstream of the Momposina permitted in the fit (`docs/31` §C4.1) | **`21237020` ARRANCAPLUMAS stays OUT of the fit** — EVAL only | `docs/43` §3.1 **P2**, decided here, §2.4. |

`docs/43` §3.1 makes P1, P2 and P3 **blocking preconditions on C4's start** and says they are
owed to `docs/42` §9. **This document is not scoped to edit `docs/42` either** — a frozen
pre-registration is amended by its own owner. It discharges the preconditions by registering
the same three decisions in its own frozen sections (§2.2, §2.4, §2.3), and records that the
`docs/42` §9 transcription **remains owed**.

---

## 1 — The state C4 inherits, stated once so no section has to re-argue it

1. **C3 is OPEN** (`docs/37` A1, `docs/43` §2) on clauses 2, 3 and 4″. C4 runs while it is
   open, held to `docs/42` G1–G9, **never to `docs/35` §6 alone** (`docs/37` A1.6).
2. **The C3 residual's DIRECTION is UNKNOWN** — from 2.27× too low (reading A) to 1.49× too
   high (reading B) (`docs/37` A1.9). *"The model is ~2× under-erosive"* is **WITHDRAWN** and
   may not justify, motivate or excuse anything in C4 (`docs/43` §3.3 item 5).
3. **The level is a calibration target, not a defect** (`docs/43` §1.3): Fagundes (2018)
   eq. 11 calls α and β *coeficientes de ajuste* and fits them; in that source's own
   Appendix IV, fitted α moves by **median 1.28× and up to 7.78×** for the same sub-basin
   depending only on which observed dataset was the target. **This is not a licence to fit α
   to close a level gap** — there is no gap of known size (item 2). `docs/35` §6 RULE 0 stands.
4. **Seven scalars, one identifiable product.** α, the C level, the LS level, the K unit
   system, the volume convention, P and FG enter every minibacia-day identically; the
   design-matrix condition number is **inf**, exactly singular (`docs/42` §3.1). Only
   **Π = α · f_vol · f_K · f_LS · C_mult · P · FG** is identifiable. At the adopted `C`,
   unfitted, **Π = 5,164.42** (`docs/37` A1.6 item 2; erosion-weighted 1.20427, not the
   area-weighted 1.20881).
5. **The hydrology is frozen at H2E** and is not touched by C4. Its inherited defects are
   carried, not fixed: the r-ceiling (El Niño r 0.556–0.572), the structural peak deficit
   (`R_AMS` 0.820; **81.8 %** of observed POT events with no simulated partner at ±2 d), and
   the peak deficit's **period-dependence** (`R_AMS` 0.808 La Niña vs 0.686 El Niño ⇒
   **×1.096**, which *flatters* every simulated contrast).
6. **33.47 %** of the model's gross erosion is upstream of a usable SSC station; **66.53 %
   (199.29 of 299.54 Mt/yr) is not**, and **801.1 km of channel — the whole Depresión
   Momposina — lies below the outlet-most SSC station**, against a basin maximum path of
   1,425.9 km (`docs/43` header; `docs/42` G9 as re-numbered by `docs/37` A1.6 item 5).
   *(`docs/42` §4.5's 36.1 % is the same quantity at the **prior** `C`; the adopted-`C`
   figure supersedes it.)*
7. **The yield embargo is in force** (`docs/23` §13.2): per-gauge catchment areas disagree by
   >2× on 31 of 85 shared gauges. **Absolute flux only.**

---

## 2 — THE CELLS (registered exactly)

### 2.1 The two free parameters, their bounds, and the source of every bound

| | parameter | role | **search box** | source of the box | reference value | source of the reference |
|---|---|---|---|---|---|---|
| **P1** | **α** | the multiplicative level; the *handle* on Π, **never reported alone** (§5.3) | **[2.0, 30.0]**, log-spaced | union of `docs/31` §C4.2's registered `α ∈ [2, 30]` and Fagundes (2018) §6.3.1's own MOCOM-UA search prior **[2.0, 25.0]** (`docs/43` §1.3 leg 1) | **11.8** | **Williams (1975)**; adopted unchanged by Buarque (2015) eq. 5 with the **same daily-mean `q_peak`**, so it is like-for-like under `docs/35` §4 |
| **P2** | **β** | the event exponent on `(Qsur · q_peak · A)` | **[0.40, 0.75]**, linear | `docs/31` §C4.2, registered | **0.56** | **Williams (1975)** |

> **REGISTERED, and it is the whole point of this row:** the α box is a **SEARCH BOX, not a
> plausibility band**. `docs/43` §1.3 measured that **97.7 %** of the transposed method's 426
> published (α, β) pairs land inside `docs/35` §6.1's "expected" 5.9–23.6 **because the
> source's own search prior [2.0, 25.0] contains it** — that statistic measures the prior, not
> the physics. **No C4 verdict may be argued from where α̂ sits inside its box.**

**The plausibility judgement on α is `docs/35` §6.1's band, and it is applied with its measured
defect stated.** `docs/35` is frozen, so C4 **follows it anyway**: expected 5.9–23.6, *watch*
23.6–35.4 (adopt only with a written non-peak physical justification), **HARD STOP α > 35.4 or
α < 3.9**. Two defects must be printed beside it every time it is quoted:

- it is the band for the **source LS formulation**; ours is **2.37×–3.00×** that level on the
  same 90 m grid over all 30,235,916 cells (`docs/35` §6.1 caveat; `docs/37` §4 candidate 0);
- this repository's own unmodified `check_musle_parameters` **STOPs 185 of the 426 published,
  adopted pairs (43.4 %)** (`docs/43` §1.3). It is **necessary-and-not-sufficient at best**.

**β's adoption gate is `docs/35` §6.3, unchanged and re-affirmed as `docs/42` G2.3: HARD STOP
if β̂ > 0.65 or β̂ < 0.45.** The box is wider than the gate **on purpose** — a search that walks
out of [0.45, 0.65] is diagnostic information the gate would otherwise hide. **42.7 points of
that 43.4 % STOP rate is this β stop firing on published fits** (`docs/43` §1.3): the gate is
frozen, C4 obeys it, and a β̂ outside it is a registered **FAILURE** (§6), reported with the
Fagundes counter-evidence and with a *proposal* — never an enactment — of a `docs/35` §9 amendment.

**Registered precision on α's identity, so the doc cannot be misread:** α is fitted as the
numerical handle by which the search moves Π. **What C4 has determined is Π.** Any α̂ printed
without Π, its equifinal family and its application unit is a reporting FAIL (`docs/42` G6).

### 2.2 Why TWO free parameters and not the three `docs/31` registered

Lens 3's measurement (`docs/43` §1.2, §3.2), carried and not recomputed:

| quantity | value | consequence |
|---|---:|---|
| stations that survive all four filters | **8** | `free_params_supported` = **2**; `free_params_registered` was 3 |
| stations : 3 params · stations : 2 params | 2.7 · **4.0** | 2.7 is not a fit, it is a fitted curve through a rumour |
| joint-regression residual df on the CAL 8 | **4** | |
| condition number, composition design, CAL 8 | **5,682** (basin-total form: **inf**) | α is not separable from C/LS/K/vol/P/FG **at all** |
| SE of the fleet-mean level | **0.1644 ln = ±38 % at 95 %** (0.724×–1.380×) | 13 stations would have given ±28.8 % |
| SE of β (pessimistic, σ_day = 0.809 ln) | **0.0199**; 95 % half-width **0.039** | against a registered band half-width of 0.10 ⇒ β is comfortably determined |
| `k_min` on the fit set | **0.0209 /km** (own span 60.4 km ⇒ no sink weaker than **3.54×** is detectable) | ⇒ **`k` is not fittable** |

### 2.3 The FIXED parameter, its value, and the claim that fixing it obliges (`docs/42` G5)

> **REGISTERED. The first-order channel/reach deposition coefficient is FIXED AT
> `k = 0.0 /km` — i.e. no transport sink is applied between hillslope and station — and it is
> NOT FITTED.** `SedParams.tau_delivery_days = 0`.

**Named against the implementation, so this is executable and not an abstraction.** C4.1 built
the transport step concurrently with this registration (`src/mgb_transport.py`, process record
`docs/agents/journal_c41-transport.md`). The registered mapping is:

| this document | C4.1's implementation | registered value |
|---|---|---|
| `k` (the /km deposition coefficient of G1.2) | **`TransportParams.k_dep`** with **`dep_mode = 'per_km'`** — retention along a flow path is `exp(−k_dep · path_km)`, invariant to how the network is discretised | **0.0** |
| channel storage lag | `TransportParams.tau_channel_days` | **0.0** (same-step advection; at 0 the release coefficient is exactly 1.0 and the run is the bitwise-reproducible baseline) |

`k_dep` is a **named** parameter whose default is exactly zero, so the machinery for G5 option 1
exists — but **at `k_dep` = 0 the sink is trivial**, and G5 option 1 requires a *non-trivial*
one. Option 2 is therefore what applies, below. The §2.3 sensitivity re-solve at `k_hi` is
consequently an executable run, not a hypothetical.

`docs/42` **G5** permits a fit to be adopted only if the configuration contains a **named,
non-trivial transport sink**, **or** the C4 document states the following in these words, as a
claim. There is no citable value for `k` in this repository — the 0.05–0.30 SDR band that would
imply `k ≈ 0.0020–0.0032 /km` is **UNCITED** (`docs/40`; `docs/42` §4.2) and **may neither pass
nor fail anything** — so the second option is taken, explicitly:

> ## **This model asserts SDR = 1.0 between hillslope and station.**

G5's second leg is discharged by §4.2 **G1.2**: `k̂` **with its 95 % station-bootstrap interval
must appear in the same table as α**, in the registered sentence form

> *"no first-order channel sink stronger than X× over Y km is detectable on this fit set"*

and never as a fitted value (`docs/43` §3.3 item 3). At the registered σ_r that bound is
**≈ 2.12× over 348.4 km** at best (all-18 test, `k_min` 0.00216 /km).

**One sensitivity is registered here, and it is not a fit.** After the primary fit, Π is
**re-solved once** with `k` held at `k_hi` (the larger-magnitude end of G1.2's interval), and
the two levels are reported **as a pair**. This makes the deposition axis of the equifinal
family concrete. It adds **no free parameter**: `k_hi` is measured by G1.2 before the re-solve,
and the re-solve is a one-dimensional level solve, not a search.

**Everything else is FIXED and named** — and every one of these is a way of writing Π (§1.4),
so *fixing* them is a convention choice, not a validation:

| fixed factor | value | evidence grade (`docs/37` A1.6 item 3) |
|---|---|---|
| `volume_factor` (`volume_convention = williams_m3`) | 47.8630 | **DERIVED** |
| `k_factor` (`k_unit_system = us_customary`) | 7.593014 | **IDENTIFIED** (≤ 1.3 % rounding residue) |
| `ls2d_factor` (aggregation × resolution) | 1.000 × 1.000 | **UNVALIDATED** — and unchangeable by any fit (`docs/42` G4.2) |
| `C` field, `cp_revision` = `docs/41` central | erosion-weighted ×**1.20427** | **CITED, conditioned and ranged**; **Bare** = CITED ENDPOINTS, INTERPOLATED CENTRAL (0.50 = √(0.25×1.00)) |
| `P` | 1.0 | **ASSUMED, one-sided** (P ≤ 1 ⇒ an upper bound on erosion) |
| `FG` | 1.0 | **ASSUMED, one-sided** (FG ≤ 1 ⇒ omitting it *raises* our load) |
| `f_peak` | **1.0 — not applied** | see §5.2: if ever applied it is separately named, separately reported, and it **joins Π** |

### 2.4 P2 DECIDED: `21237020` ARRANCAPLUMAS stays OUT of the fit

`docs/31` §C4.1 permits upper-mainstem stations upstream of the Momposina in the fit;
`docs/42` §4.2/§9 forbids fitting the five evaluation stations. `docs/43` §3.1 **P2** requires
the conflict be decided **in writing, either way, before a fit exists**. It is decided **for
`docs/42`**:

> **REGISTERED. `21237020` ARRANCAPLUMAS is an EVALUATION station. It is scored and never
> fitted.** So are `26017060` PUENTE ARAGÓN, `26017020` JULUMITO, `26167070` IRRA and
> `26207080` BOLOMBOLO.

Three reasons, and the cost, all recorded before the decision entered this document
(`docs/agents/journal_c42-prereg.md` D6):

1. Admitting it would **relax a frozen registration in order to gain statistical power, after
   the power had been measured** — the exact post-hoc move this project forbids.
2. It is the **only Magdalena-trunk SSC station in the entire network** (`docs/32` §R6). It is
   worth more as the single independent trunk check than as an extra fit point.
3. The cost falls **entirely on fitting `k`**, which §2.3 does not do. The deposition **test**
   (G1.2) runs on **all 18** with ARRANCAPLUMAS *scored*, and keeps its `k_min` = 0.00216 /km.

**Cost, stated and not hidden:** fitted area stays **5.4 %** of the basin (13,862 km²) instead
of 25.1 %; the fit set's own `k_min` stays **0.0209 /km** instead of 0.00303 /km — a factor 6.9
in deposition detectability *on the fit set*, which §2.3 declines to use anyway.

### 2.5 The search: a deterministic grid, and the DDS corroboration

With two free parameters, a grid is exhaustive, seed-free, bitwise reproducible, and — the
deciding reason — **the registered deliverable is an equifinal FAMILY and a ridge (§5.3), which
a grid yields whole and a single DDS optimum does not.**

| item | registered value |
|---|---|
| **primary search** | **deterministic 2-D grid**, full enumeration |
| α axis | **71 points, log-spaced** on [2.0, 30.0] (step ×1.03945, ≤ 4 % resolution) |
| β axis | **71 points, linear** on [0.40, 0.75] (**Δβ = 0.005**) |
| coarse budget | **5,041 evaluations** |
| refinement | one pass: **21 × 21 = 441** evaluations on the ±1-coarse-step box around the coarse argmax |
| **total registered budget** | **5,482 evaluations. No second search is authorised by this document.** |
| **corroboration (non-deciding)** | **DDS** (Tolson & Shoemaker 2007), `r = 0.2`, **4 seeds × 1,000 evaluations**, seeds **20260921, 20260922, 20260923, 20260924** (verified unused: `_calib_cache/` holds 20260901–06 and 20260901–02; `docs/33` §3.3 claimed 20260907–08). Over-meets `docs/31`'s "2 seeds minimum". |
| DDS's status | **it cannot change any verdict.** If DDS finds a point better than the grid argmax by more than **0.005** in `F_search`, that is a **reportable grid-resolution defect**, and the refinement pass is re-run once around the DDS point — the *rule* being registered here, not invented then. |
| **timing probe (registered contingency)** | run **25** evaluations first. If the projected coarse-grid wall clock exceeds **6 h**, coarsen to **36 × 36** (Δβ = 0.01, α step ×8.0 %) and **state the coarsening in the report**. Nothing else may be cut. |
| reproducibility gate | the full objective surface is written to `c4_grid.csv` (α, β, `F_search`, `F_report`, and the three KGE components per station). A C4 that cannot hand over the surface has not met this registration. |

---

## 3 — THE OBJECTIVE

### 3.1 KGE on **log** flux — and the symbol collision, disarmed first

> **Notation, fixed here because it is a real hazard:** KGE's own components are conventionally
> written α and β, which are the MUSLE parameters. **In this document and in every C4 output
> they are named `r` (correlation), `v` (variability ratio), `m` (mean ratio). The letters α and
> β mean MUSLE's α and β, always.**

For station `s`, over its admissible CAL paired-day set `D_s`, with
`x_t = ln(flux_obs)`, `y_t = ln(flux_sim)` in **t/day**:

```
r = Pearson(x, y)        v = sd(y)/sd(x)        m = mean(y)/mean(x)
KGE_ln(s) = 1 − sqrt( (r − 1)² + (v − 1)² + (m − 1)² )        (Gupta et al. 2009)
```

**Why the log transform, registered:** flux spans **decades** — window-mean flux across the
CAL 8 alone runs **3.31 to 22,050 t/day** (§7.3), a factor of 6,650, and daily values span more.
An untransformed KGE is dominated by a handful of station-days at the two largest stations, and
would fit the level of BORBUR and CAPITANEJO and nothing else. `docs/31` §C4.2 registered "KGE
on **log flux** (flux spans decades)"; this is that, made exact. It is also the space every
uncertainty in this project is already expressed in: σ_r = **0.465 ln**, pair-σ = **0.658 ln**,
rating residual σ = **0.809 ln**, SE of the fleet level = **0.1644 ln**.

**Numerical-stability pre-check, registered with its fallback.** `m` is a ratio of means of
logs and misbehaves if `mean(x)` approaches 0. Measured (§7.3): CAL-8 window-mean fluxes give
ln 1.20–10.00, all positive, so the denominator is safe at station scale — but a *daily*
geometric mean at a small station could still approach 1 t/day.

> **Registered:** compute `mean(x)` per CAL station before the search. **If any station has
> `|mean(x)| < 1.0`**, that station's KGE is *additionally* computed with the bias term
> replaced by `m' = (mean(y) − mean(x)) / sd(x)`, **both variants are reported**, the station is
> flagged in every table, and **if the §6 verdict differs between the two variants the outcome
> is INDETERMINATE, not a pass.** The `m'` variant is **UNCITED in this repository** and is used
> only as a numerical-stability fallback — never as the deciding statistic on its own.

### 3.2 Search statistic, report statistic, and the bar

| | definition | why |
|---|---|---|
| **`F_search`** (what the grid maximises) | **mean** of `KGE_ln(s)` over the admissible CAL stations | smooth: every station moves it, so the surface has a well-defined ridge |
| **`F_report`** (what §6 judges) | **median** of `KGE_ln(s)` over the admissible CAL stations | **Fagundes' bar is a median**; `docs/31` §C4.2 registered the median |

Both are reported for every cell, always, together with the three components (`r`, `v`, `m`)
**per station**.

> **THE SEDIMENT KGE BAR, registered: `F_report` ∈ [−0.26, 0.44]** — Fagundes' median log-flux
> KGE band, as `docs/31` §C4.2 registered and `docs/43` §3.1 forbids relaxing.

**And registered with it, in the same breath, so the bar cannot be oversold** (`docs/43` §3.1):
the **mean predictor** scores **KGE = 1 − √2 = −0.414**, so the bar's lower edge sits only
**0.15 KGE units above no-skill**, and a median over **8** stations carries very little
information. **Passing this bar is not evidence of a good model; failing it is evidence of a
bad one.** That asymmetry must be printed with the verdict.

### 3.3 The observation the objective is fitted to — and why it is estimator (a)

> **REGISTERED. The objective is fitted on estimator (a) — the paired sample-day flux,
> `Qs = Q × C × 0.0864` on days carrying a QC'd `ssc_mean_mg_l` (`c1_deleted == False`) and a
> same-day observed `q_m3s` at the same code** (`docs/34` §1.3–§1.4).

Reason, registered before the fit: under estimator **(b)** the observed flux is a **deterministic
function of Q**, so fitting on it fits the model to a rating curve and the SSC measurements
contribute nothing independent about flux. That is `docs/42` **G2.2**'s own argument, applied
one level up to the objective. **The guards are unaffected: `docs/42` §6's registered primary
estimator for G1–G9 remains (b), with G2.2 on (a). Nothing in `docs/42` is edited.**

The fit is **also** re-run on estimator (b) and reported as robustness. **It cannot change the
verdict** — same "gate on one, report both" discipline as `docs/33` §2.1 — **except** that a
sign disagreement between (a) and (b) on the §6 verdict makes the outcome **INDETERMINATE**.

### 3.4 The stations

**CAL — fitted (8).** Lens 3's filter chain, carried (`docs/43` §3.1 P1): 18 mapped-usable →
(a) tributary **13** → (b) upstream of the Momposina **13, removes ZERO** → (c) ≥ 1 SSC obs in
CAL 2012–14 → **9** → (d) ≥ 1 **paired** SSC + observed-Q day → **8**. The same 8 survive the
`docs/32` rating floor (n ≥ 15) **and** the stricter C1.1 floor (n ≥ 91), and all 8 have a
usable rating era covering CAL.

| code | name | `Lw` km | model up-area km² | Forest/Grass/**Bare** erosion share % | `flow_selective` |
|---|---|---:|---:|---|---|
| `22017030` | BOCAS | 2.6 | 68 | 63.7 / 36.3 / 0.0 | False |
| `26137110` | BANANERA LA 6-909 | 26.9 | 289 | 11.9 / 12.5 / **75.6** | False |
| `24027030` | NEMIZAQUE | 27.1 | 611 | 42.9 / 56.9 / 0.0 | False |
| `21197010` | EL PROFUNDO | 30.4 | 833 | 15.7 / 69.8 / 14.3 | False |
| `23127010` | BORBUR - AUT | 32.7 | 1,645 | 72.3 / 26.7 / 0.0 | False |
| `26127010` | EL ALAMBRADO AUT | 40.4 | 1,711 | 49.7 / 21.0 / 26.1 | **True** |
| `22017010` | BOCAS | 42.5 | 2,411 | 26.9 / 10.7 / **62.4** | False |
| `24037390` | CAPITANEJO | 60.4 | 6,362 | 2.4 / 37.9 / **58.4** | False |

Total fitted area **13,862 km² = 5.4 %** of the basin. `Lw` span **2.6–60.4 km**. 2 macro-regions,
6 departments. **Exactly 1** CAL–CAL nested pair survives (`22017030` → `22017010`, 39.9 km) of
the 3 `docs/42` §4.1 claimed.

**The 5 lost tributary stations, named with their reasons** (`docs/43` §3.1 P1), because a fit
set that shrank silently is a fit set nobody can audit: `23087210` CANTERAS, `26167060` PAILA LA,
`21147030` CARRASPOSO — **zero SSC before 2015**; `22057090` BOCATOMA TRIANGULO — 619 CAL SSC
days but **observed Q ends 2009-03-19**; `26107130` MATEGUADUA — **neither**.

**`26127010` EL ALAMBRADO AUT is `flow_selective == True`** (measured, §7.3). It is **kept** in
the objective — a *day-matched* KGE over the sampled days is internally consistent, and the
C1.2 gate forbids its use as a **window-mean** estimator, which the objective does not use — but:
(i) it is flagged in every table; (ii) a **leave-it-out refit is mandatory** (G12); (iii) **if
the §6 verdict flips with and without it, the outcome is INDETERMINATE, not a pass**; and
(iv) it is **excluded from G2.2**, whose observed-flow-quantile bins a flow-selective sample
directly distorts.

**EVAL — scored, never fitted (5):** `26017060` PUENTE ARAGÓN, `26017020` JULUMITO,
`26167070` IRRA, `26207080` BOLOMBOLO, `21237020` ARRANCAPLUMAS (§2.4).

**All 18 are used by every residual-structure guard** (`docs/42` §4.2's registered consequence:
the deposition test *must* include the evaluation stations, or it has no power).

**Station admissibility rule, registered:** a CAL station enters the objective only with
**≥ 91 paired CAL days** (the stricter C1.1 floor; lens 3 measured all 8 clear it). If the actual
paired construction drops a station below 91, it is **dropped and named** in the report. **If
fewer than 6 of the 8 remain, C4 is reported as EXPLORATORY and is NOT adopted** (§6).

### 3.5 The windows — CAL, warm-up, and what is strictly out of sample

| set | dates | role |
|---|---|---|
| **warm-up** | `2009-01-01 … 2011-12-31` | sediment state spin-up. **Not scored. No parameter is adjusted against it.** |
| **CAL (fitted)** | **`2012-01-01 … 2014-12-31`** — neutral years | the only data the objective sees |
| **VAL-neutral** | 2017–2018 (and 2009–2010 as warm-up-contaminated, reported separately) | out-of-sample, scored |
| **P-LN / P-EN** | 2011 · 2015–2016 | **STRICTLY OUT OF SAMPLE.** C5's target. |
| **S-LN / S-EN** | 2010-07-01…2011-06-30 · 2015-10-01…2016-04-30 | **STRICTLY OUT OF SAMPLE.** |

**Klemeš (1986) differential split-sample, as Phase B used it:** fit on one climatic regime,
score on another. `docs/31` §C4.2's spin-up clarification is re-registered verbatim in effect —
the sediment model runs the full 2009–2018 driver record and is *scored* only on the registered
sets; the 2009–2011 span, La Niña 2011 included, feeds antecedent state into CAL. **That is
physics, not fitting: no 2011 observation enters the objective, no parameter is adjusted against
2011 data, and the ENSO windows remain strictly out of sample.** "Warm-up ≠ scored" is the same
distinction Phase B used for 2008 (`docs/26`).

> **UNCITED, and it is the premise of this split.** `docs/31` asserts that **2012–14 is ENSO-
> neutral** with **no ONI table in this repository** behind it (lens 3 issue 5; `docs/43` §6).
> **Registered action:** C4.3 must record the ONI values for 2012–2014 from the NOAA CPC ONI
> v5 series, with the retrieval date and the threshold used, in `report_C4.json`. **If it
> cannot, the split is labelled UNCITED and the claim is downgraded from "out-of-phase" to
> "out-of-window"** everywhere it appears. An uncited premise may not certify an out-of-sample
> claim.

### 3.6 The honest denominator — registered so it cannot be inflated later

| quantity | value | use |
|---|---:|---|
| raw paired CAL days, all 8 stations | 3,266 | **MAY NOT be quoted as an `n`** |
| autocorrelation-effective days (median lag-1 ρ **0.771**) | **474.2** | the honest temporal `n` |
| station-months with data / possible | 126 / 288 | coverage |
| **effective observational units for every spatial claim** | **8 stations** | the honest `n` for Π, for the fleet median, for every guard interval |

---

## 4 — THE GUARDS, made evaluable

All of `docs/42` G1–G9 are imported **unchanged in threshold**. What this section adds is, for
each, the **artifact it is computed from** and the **action on failure**, plus three **new**
guards (**G10, G11, G12**) that `docs/42` could not have written because it was drafted for
n = 13 and did not know n = 8.

**Bootstrap convention, imported verbatim (`docs/42` §6):** "the 95 % interval" means a
**station-level bootstrap** — resample the 18 stations with replacement 10,000 times, recompute
the statistic inside each resample (rebuilding the nested pairs among the resampled stations),
take the 2.5/97.5 percentiles. **Station resampling, not day or pair resampling.**

**Registered yardsticks, imported (`docs/42` §4.2–§4.3, §9):** σ_r = **0.465 ln** (a factor
1.59) · pair-σ = **0.658 ln** · `b_obs` between-station IQR = **0.464**.

### 4.1 The residual-STRUCTURE battery — the only thing that can betray compensation now

> **The design principle, imported from `docs/42` §1:** *a scalar parameter can absorb a level;
> it cannot absorb a structure.* This is now doubly load-bearing: `docs/37` §5.1 measured that a
> fit which **silently omits channel deposition lands α at 6.83–8.73, INSIDE `docs/35` §6.1's
> "expected" band**, with `check_musle_parameters` returning `ok`; and `docs/43` §3.4 measured
> that the α reproducing the flattering reading-B level is **7.92–8.86** — **these overlap**.
> **The α-magnitude guard is blind to the single error C4 is most likely to make. The structure
> tests are what is left.**

#### The spatial axis the brief asks for — and the honest answer about half of it

> **NOT EVALUABLE, and this is MEASURED, not assumed. "Above vs below the Depresión Momposina"
> cannot be tested at all.** All 18 usable SSC stations lie upstream of the Cauca–Magdalena
> confluence (`docs/34` §4.2; `docs/42` §4.1). Lens 3 measured the geometry: the confluence is
> **minibacia 4430, 146.1 km above the outlet**, and **the closest SSC station is 684.4 km
> above it** — which is why filter (b) removed **zero** stations. **No station pair spans the
> sink.** `21237020` ARRANCAPLUMAS still has **801.1 km** of channel below it. It is recorded
> here rather than quietly substituted.

What *is* evaluable on this network are **three** spatial axes, and all three are registered:
the **longitudinal ladder** (G1.2, `Lw` 2.6–348.4 km, 134×), the **nested upstream/downstream
pairs** (G1.1, 22 pairs, ΔLw 7.4–345.8 km), and the **macro-region contrast** (G11, NEW).

### 4.2 The guard table

| id | what it tests | quantity | **threshold ⇒ FAIL** | computed from | **ACTION ON FAILURE** |
|---|---|---|---|---|---|
| **G1.1** | missing channel deposition — the α-free pair test | `D_pair = [ln flux_sim_dn − ln flux_sim_up] − [ln flux_obs_dn − ln flux_obs_up]` over the **22** nested pairs; α, C_mult, `f_LS`, `k_factor`, `f_vol`, P, FG **cancel exactly** | fleet median `D_pair` **> +0.658** (one measured pair-σ) | `sed_station_daily.npz` + `topology.npz` + `c2_station_window_flux.csv` | **Do not adopt.** Add an **explicit, named** transport sink and refit; report pre- and post-sink fits side by side with `k̂` for both. **Never absorb into α** (`docs/35` §6 RULE 0). Corroboration only — the verdict is G1.2's (22 pairs come from 18 stations; ARRANCAPLUMAS appears in 5). |
| **G1.2** | missing channel deposition — **the registered primary** | `r_i = c + k·Lw_i + ε_i`, OLS over **all 18**, fitted **jointly** with G3.1 and G4.1 as one multiple regression | the 95 % station-bootstrap interval for `k` lies **entirely above 0** | as above | **Do not adopt the fit** — same action as G1.1. If neither G1.1 nor G1.2 fires, **that is NOT A PASS**: report the bound `\|k\| < k_hi` in the registered sentence (§2.3), ≈ **2.12×** over 348.4 km at best. Report the Jensen term when `k̂ · sd(L) > 0.3`. **A univariate `Lw` slope reported alone is not an acceptable G1 output.** |
| **G2.1** | the peak deficit folded into β — the α-free test | `ln flux ~ ln Q` per station, OLS on logs per rating era, station value = median over eras, once observed and once simulated (`q_sim_fit_m3s`) | fleet median **\|b_sim − b_obs\| > 0.464** (the between-station IQR of `b_obs`); **or** `b_sim − b_obs > 0` **and** β̂ within 0.02 of its box edge | `sed_station_daily.npz` + `q_gauge_H2E.npz` + `ssc_rating_fits.csv` | Report and **attribute to (β, the runoff partition)** — the test localises the fault there and **explicitly does not license a change to α, C or LS**. |
| **G2.2** | the peak deficit folded into α — residual by flow band | fleet-median relative residual below observed Q50, Q50–Q95, above Q95 | below-Q50 residual **> +25 %** while the above-Q95 residual is **negative** | **estimator (a) only** (`docs/42` G2.2's registered restriction); **EL ALAMBRADO excluded** (§3.4) | **STOP and report.** α has absorbed the peak deficit. Not adopted. |
| **G2.3** | β amplification | β̂ | **β̂ > 0.65 or β̂ < 0.45** (`docs/35` §6.3, re-affirmed) | `c4_parameters.csv` | **HARD STOP.** Not adopted. Report with the `docs/43` §1.3 counter-evidence and a *proposal* for a `docs/35` §9 amendment — never an enactment. |
| **G3.1** | a class-specific C error | `r_i = c + k·Lw_i + c_G·share_Grass_i + c_B·share_Bare_i + ε_i` over all 18 (joint with G1.2, G4.1). Forest is the reference class — its collinearity with `c` **is** the α confounding, correctly quarantined | the 95 % station-bootstrap interval for **`c_G` or `c_B` excludes 0** | `SedResult.cell_eroded_t` + `SedGeometry` + station residuals | Revise **that class's `C`** in `urh_cp_factors.csv`, with the reason and the source in that row's own columns, and refit. **Never α.** `c_B` must be run and reported **whichever way it comes out** — it would be the first independent evidence this project has ever had about the Bare class. |
| **G3.2** | unidentifiable classes | Shrub, Cropland, Urban, Water, Wetland — ≤ 3.1 % of erosion at **every** station | C4 **fits** any of them, or reports one as validated | — | Reporting FAIL. Every table listing them carries **ASSUMED** (or **CITED** per `docs/41`) — **never validated**. |
| **G3.3** | the C **level** | not testable by any fit — it *is* Π | a C4 table quotes a load without the level's evidence grade | — | Reporting FAIL. Grades per `docs/37` A1.6 item 3. **Cited is not validated, and fitted is not validated either** (`docs/43` §3.3 item 1). Registered in advance: G3.1's minimum detectable class-C error is **×4.2** on the CAL 8 (×2.9 on all 18), so **G3.1 could not have seen `docs/41`'s ×1.2043 revision** — G3.1 **cannot audit `docs/41`**, and C3 clause 3 stays open however it comes out. |
| **G4.1** | a steepness-dependent LS error | add `ln LS̄_i` (station erosion-weighted LS2D, 38.2–117.1) to the joint regression | the 95 % interval for its coefficient **excludes 0** | as G3.1 | Fix the LS2D field, or adopt a **steepness-dependent** correction with its derivation. **Never α, and never a scalar `ls2d_resolution` multiplier** — a scalar cannot fix a slope-dependent error, only hide it in Π. |
| **G4.2** | the LS **level** | not testable | C4 changes `ls2d_aggregation`/`ls2d_resolution` to move the level, or reports the level as validated | — | Reporting FAIL. The level is **UNVALIDATED** and must be printed that way. A G4.1 non-detection exonerates the field's *shape* and says **nothing** about its level. |
| **G5** | the deposition precondition that replaced the blinded α band | (1) a named non-trivial sink **or** the §2.3 claim in those words; **and** (2) G1.2's `k̂` **with its interval, in the same table as α** | either leg missing | `c4_parameters.csv`, the C4 document itself | **AUTOMATIC FAIL regardless of what `check_musle_parameters` returns.** A fitted α in 5.9–23.6 obtained without both legs is not a result. |
| **G6** | the level-invariant report | five mandatory elements: **(1)** Π with its full decomposition; **(2)** α **with its application unit** (`docs/35` §6.2 — α = 12 is textbook-perfect at `a_p` = 0.0081 km² and a **2.2× over-fit** at minibacia scale) and its registered band beside it; **(3)** `SedParams.convention_summary()` verbatim; **(4)** the **equifinal family** — at minimum the three tuples giving the same Π at `C_mult ∈ {1, 2, 5}`; **(5)** the per-factor evidence grade | **any one missing** | every C4 table | **Reporting FAIL, blocking adoption.** |
| **G7** | cross-phase compensation | fit on one ENSO phase, score on the other | the El Niño 2015–16 residual more positive than the La Niña 2011 residual by **> +10 %** (`docs/35` §5.4; `R_AMS` 0.8875/0.8097 = 1.096) | `sed_station_daily.npz` + the C2 artifacts | Report either way — **the direction is known in advance to flatter the headline contrast**, so silence here is not neutral. |
| **G8** | seasonal structure | median `r_i` by calendar month, fleet-pooled, primary estimator (b) | the **range across months** of the fleet-median monthly residual **> 0.465 ln** (one σ_r) | as above | Report and **attribute** — candidates: the runoff partition, the C field's lack of a seasonal cycle (one annual `C` per class in a basin with two rainy seasons and crop calendars), the antecedent-state effect (`docs/31` §C4.2). **Not α.** |
| **G9** | mandatory disclosure of the unobserved fraction | **66.53 %** of gross erosion (199.29 of 299.54 Mt/yr) upstream of **no** usable SSC station; **33.47 %** is; **801.1 km** of channel including the whole Momposina below the outlet-most station | a **basin-scale** conclusion drawn from station fits **without it in the same paragraph** | — | **Reporting FAIL.** Passing G1–G8 constrains the model over **33.47 %** of its own erosion. **It is not closure of C3.** |
| **G10** *(NEW)* | **the fit determined a level and nothing else** | decompose the CAL improvement in `F_report` from the unfitted default into its `r`, `v`, `m` contributions. On log flux, **α moves only `m`**; `r` and `v` are **invariant to α** exactly | **> 80 %** of the improvement attributable to the **`m` (bias) component** | `c4_grid.csv` | **Not a FAIL — a MANDATORY STATEMENT.** C4 must state, in the abstract and the verdict: *"the calibration determined a level and essentially nothing else."* **Omitting it when the threshold is met is a reporting FAIL.** Registered because a KGE improvement that is all bias term is Π being set, which §1.4 already says is all a fit can do. |
| **G11** *(NEW)* | **the spatial contrast that IS evaluable**, standing where "above vs below Mompós" cannot | fleet median `r_i` by **macro-region** (Magdalena vs Cauca), all 18, and reported for the CAL 8 (2 macro-regions, 6 departments) | the between-region difference in median `r_i` **> 0.465 ln** (one σ_r) | station residuals + `_c1_geom.csv` | **FAIL.** A scalar α cannot be right in two regions at once; report and attribute to the regional axis (forcing field density, land-class composition, rating-era vintage) — **never to α**. Registered as **weak by construction** at n = 8 across 2 groups; the all-18 form is the deciding one. |
| **G12** *(NEW)* | **single-station fragility at n = 8** | refit **8 times**, leaving out one CAL station each time; record `F_report`, α̂, β̂, and the §6 verdict for each | **the §6 verdict flips on any single deletion** | `c4_grid.csv` re-run ×8 (cheap: the surface is precomputed per station) | **INDETERMINATE**, not a pass and not a fail (§6). Also mandatory whether or not it fires: report the **range of ln Π̂ across the 8 LOO refits** against the registered 95 % level band of **±0.322 ln (±38 %)**; an LOO range exceeding it means the level is set by one station. The `26127010` EL ALAMBRADO deletion is called out by name (§3.4). |

### 4.3 What the guard battery covers, against the brief

| axis the brief requires | guard | status |
|---|---|---|
| spatial — above vs below Mompós | — | **NOT EVALUABLE, measured** (§4.1). Substituted, not skipped. |
| spatial — upstream vs downstream | **G1.1, G1.2** | evaluable; the registered primary deposition test |
| spatial — regional | **G11** *(NEW)* | evaluable, weak at n = 8, deciding form is all-18 |
| seasonal | **G8** | evaluable |
| flow magnitude | **G2.1, G2.2** | evaluable |
| land composition | **G3.1, G4.1** | evaluable, 2 C contrasts only |
| cross-phase | **G7** | evaluable |
| identifiability / reporting | **G5, G6, G3.2, G3.3, G4.2, G9, G10** | evaluable as reporting gates |
| fragility | **G12** *(NEW)* | evaluable |

---

## 5 — WHAT C4 WILL NOT CLAIM (registered in advance, so it is not discovered later)

### 5.1 No gauge-referenced yield, in any units, anywhere

> **No t/km²/yr, no t/ha/yr, no area-normalised sediment yield referenced to a gauge.** The
> `docs/23` §13.2 embargo is in force: per-gauge catchment areas disagree by more than 2× on
> **31 of 85** shared gauges (36 %) in **both** implementations, so every area-normalised number
> inherits that error one-for-one. **Absolute flux only — t/day, Mt/yr.** Model-internal specific
> erosion is permitted **only** if labelled *model-internal* in the same sentence. `Lw` is
> model-internal by construction and is **never used as a divisor** (`docs/42` §2).

### 5.2 No absorption of the peak deficit into α or β

> `docs/35` §6 **RULE 0** stands unchanged: α and β may **not** compensate the §5 biases, and
> `q_peak` is not a calibration knob, directly or by proxy. The available compensation product is
> known in advance — 2.75 (proxy) × 1.12 (peak magnitude) × 1.74 (missing events) ≈ **5.4×**.
> The **only** permitted correction is an **explicit, separately named, separately reported
> `f_peak`** with its own stated derivation, **outside α**, visible in every table, with the
> uncorrected number alongside (`docs/35` §6.5). **This registration sets `f_peak = 1.0`, not
> applied.** And note the trap `docs/42` §8.1 recorded: **`f_peak` is itself a scalar and
> therefore joins Π — it may be *reported* as a factor but can never be *fitted* separately from
> α.** The simulated level is reported as an explicit **lower bound**, because the peak deficit
> is structural (81.8 % event-identity deficit); "43 % of flood events missed" is a **count**
> statement and may never be quoted without the 81.8 % figure beside it.

### 5.3 No unique fit — C4 reports a FAMILY

> **REGISTERED NOW, so it is not presented later as a discovery.** α, the C level, the LS level,
> the K unit system, the volume convention, P and FG are **seven ways of writing one product Π**;
> the design matrix is **exactly singular** (condition number **inf**; **5,682** in the CAL-8
> composition form). Lens 3 measured that a class-C error smaller than **×4.2** is invisible to
> this fit set. **Therefore C4 reports the fitted Π, its ±38 % band, its equifinal family and a
> per-factor evidence grade — never a unique fit, never a validated α, never a validated C or LS
> level, never a validated basin sediment load** (`docs/42` G6, `docs/43` §3.2, `docs/37`
> A1.6 item 2). The word **UNVALIDATED** appears in the same table as Π.

### 5.4 The remaining five, listed so the not-claim set is complete

1. **No fitted deposition coefficient.** `k` is reported as a **bound**, in the registered
   sentence form, never as a value (§2.3; `docs/43` §3.1 P3, §3.3 item 3).
2. **No argument from a withdrawn direction.** *"The model is 2× under-erosive"* is **WITHDRAWN**
   (`docs/37` A1.9). No C4 output may be motivated by, justified by, or compared against it.
   A fit argued from a withdrawn direction is a fit argued from nothing.
3. **No closure of C3, and no basin-scale statement without G9's disclosure.** Passing G1–G12
   constrains the model over **33.47 %** of its own erosion.
4. **No claim about the Momposina, about below-Mompós delivery, or about the mainstem below
   `21237020`.** The network **cannot see it** (§4.1). Any such statement is unsupported by
   construction, not merely uncertain.
5. **No per-station simulated ENSO contrast** attributed to the model, and **no window-total
   ratios** — rates only, both window pairs, unaveraged (`docs/34` §1.2, `docs/43` §5.3).
   Registered here because C4's outputs are what C5 will reach for.

**And one claim that must be *made*, not withheld:** `docs/43` §5.4's finding that the apparent
delivery ratio `obs/sim` spans **0.0039–1.239 across 46 station-windows (a factor of 322)** and
that **exactly one station of eighteen (`23127010` BORBUR) has `r > 1`** — observed flux
exceeding the model's entire upstream hillslope erosion — **belongs in C4's G1 discussion**. It is
a local, like-for-like instance of `docs/40`'s impossibility argument and it does not depend on
any published comparator.

---

## 6 — DECISION RULES, fixed now

### 6.1 The outcomes, and there are five

| outcome | conditions | what it licenses | what it does **not** license |
|---|---|---|---|
| **ADOPT** | **all eight**: (1) `F_report` ∈ **[−0.26, 0.44]** on the CAL 8; (2) **no free parameter railed** — α̂ and β̂ each ≥ **5 % of the box range** from either edge (Phase B's rail definition, `docs/33` §3.5); (3) **β̂ ∈ [0.45, 0.65]** (G2.3); (4) **every structure guard passes** — G1.1, G1.2, G2.1, G2.2, G3.1, G4.1, G7, G8, G11; (5) **G5's two legs both discharged**; (6) **G6's five reporting elements all present**; (7) **G9's disclosure present**; (8) **G12 shows no verdict flip** | C5 may run the contrast, carrying `docs/43` §5's caveat set in full; the fitted **Π** may be reported with its band, its family and its grades | **NOT** closure of C3. **NOT** a validated α, C, LS, P, FG, K-unit or volume convention. **NOT** a yield. **NOT** a statement about the Momposina or the lower mainstem. |
| **FAIL — STRUCTURE** *(the case the brief demands be named)* | **the fit succeeds numerically — `F_report` inside the bar, parameters off their bounds — AND any one of G1.1, G1.2, G2.1, G2.2, G3.1, G4.1, G7, G8, G11 fails** | reporting the fit as a **measured negative**, with that guard's registered ACTION taken | **This is a FAILURE. It is NOT a pass with a caveat, not a "pass, noting…", and not an adoption pending future work.** A scalar cannot absorb a structure, so a structured residual means the number that fits is fitting the wrong thing. **The fit is NOT adopted and C5 does not run on it.** |
| **FAIL — NUMERIC** | `F_report` **< −0.26** (or > 0.44, which at n = 8 would itself demand explanation) | reporting the measured negative; one named remedial route from the failing guard's ACTION column | **NOT** a widened box, **NOT** an added parameter, **NOT** a second search. Any of those needs a **new** pre-registration. |
| **FAIL — RAILED / HARD STOP** | any of: α̂ or β̂ within 5 % of a box edge; **α̂ > 35.4 or α̂ < 3.9** (`docs/35` §6.1); **β̂ outside [0.45, 0.65]** (G2.3); a G5/G6/G9 reporting leg missing | reporting the fit **and the fact that the threshold fired** | **The box may not be widened and the frozen band may not be amended by the session that hit it.** A `docs/35` §9 amendment may be **proposed**, with the `docs/43` §1.3 evidence, and enacted by someone else. |
| **INDETERMINATE** | any of: **G12** verdict flip on a single-station deletion; the estimator **(a)/(b)** verdicts disagree in sign; the **KGE `m`/`m'`** variants disagree (§3.1); fewer than **6** of the 8 CAL stations admissible (§3.4) | reporting exactly that, with the flipping station or estimator named | **Not a pass.** C5 does **not** run on an indeterminate fit. Resolving it needs more both-window stations, not more search. |

### 6.2 The three statements that must accompany the verdict, whatever it is

1. **The bar is asymmetric.** The mean predictor scores **KGE = −0.414**; the bar's lower edge
   sits **0.15 units above no-skill**; a median over **8** stations carries very little
   information. **Passing is not evidence of a good model; failing is evidence of a bad one.**
2. **The level's band is ±38 %** (0.724×–1.380×; SE 0.1644 ln at n = 8). Every Π and every load
   is quoted **with that band**, never as a point.
3. **β cannot reach the observed contrast.** Because `q_peak = Qsur · a_p / 86.4` here, the
   MUSLE product is ∝ `Qsur²` and simulated flux scales as **`Qsur^{2β}`** — effective exponent
   **1.12** at β = 0.56, **not** 0.56. Across the **whole** registered β band the simulated
   basin contrast is **1.83×–2.39×** (primary) and **2.98×–4.83×** (sensitivity) against observed
   **2.8×–4.6×** and **6.4×–9.3×** (`docs/43` §5.1). **Therefore a C4 fit that appears to improve
   the ENSO contrast has either left the β band — a G2.3 hard stop — or is not doing what it
   appears to be doing.** Registered *now* so that outcome cannot be read as success later.

### 6.3 What no outcome licenses

No outcome of C4 licenses: a second search, a widened box, an added free parameter, an edit to
`docs/35`, `docs/42` or this document's §2–§6, a re-run of the hydrology, or a change to any
frozen artifact. **Every one of those requires a new, dated pre-registration.**

---

## 7 — Registration record

### 7.1 The card

| | |
|---|---|
| Registered | **2026-08-11**, before any C4 search machinery existed and before any α/β fit |
| Registered by | the `c42-prereg` agent; process record `docs/agents/journal_c42-prereg.md` |
| Free parameters | **2** — α (handle on Π) ∈ [2.0, 30.0]; β ∈ [0.40, 0.75] |
| Fixed, not fitted | `k = 0.0 /km` + the stated SDR = 1.0 claim; `f_vol` 47.8630; `f_K` 7.593014; `f_LS` 1.000; `C` at `cp_revision` docs/41 central (×1.20427); P 1.0; FG 1.0; `f_peak` 1.0 |
| Objective | `KGE_ln` (Gupta et al. 2009) on ln flux, t/day, estimator **(a)**; `F_search` = mean, `F_report` = median, over the CAL 8 |
| Bar | **Fagundes' median KGE −0.26 … 0.44**, not relaxable (`docs/43` §3.1) |
| Fit set | **CAL 8**; EVAL 5 scored never fitted; **all 18** for every structure guard |
| Windows | warm-up 2009–2011 · **CAL 2012-01-01…2014-12-31** · both ENSO pairs **strictly out of sample** (Klemeš 1986) |
| Search | deterministic **71 × 71 grid** + 21 × 21 refinement = **5,482** evaluations; DDS ×4 seeds (20260921–24) corroboration, **non-deciding** |
| Guards | **G1–G9 imported unchanged from `docs/42`**; **G10, G11, G12 NEW** (§4.2), with reasons |
| Yardsticks | σ_r **0.465 ln** · pair-σ **0.658 ln** · `b_obs` IQR **0.464** · level SE **0.1644 ln (±38 %)** · β SE **0.0199** |
| Preconditions discharged | `docs/43` §3.1 **P1** (§3.4), **P2** (§2.4), **P3** (§2.3). The `docs/42` §9 transcription **remains owed** to that file's owner. |
| Amendments | none |

### 7.2 What this document does **not** do

- It does **not** edit `docs/42` or `docs/35`. Both are frozen; this document imports them,
  records where they are measured to be mis-specified, and **follows them anyway**.
- It does **not** narrow the `docs/35` §5.3 bias bracket, decide the SDR question, resolve the
  LS-formulation decision (C3.1), or close any C3 clause.
- It does **not** launch a search, fit anything, or produce a number that any gate here judges.
- It does **not** claim the number **44**; only **45** is claimed by this pass.

### 7.3 Disclosure

- **No frozen artifact was opened or written.**
  `sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv, q_gauge_H2E.npz}` were not touched.
  **No calibration was launched. No simulation was run. No headline number was moved. Nothing is
  backdated. No git command was run.** No wide forcing CSV was read.
- **Two read-only reads of `data/processed/c2/c2_station_window_flux.csv`** were made, both
  **station properties, not results**, and both **journalled as decisions before they entered
  this document**: (i) `flow_selective` is `False` for 7 of the CAL 8 and **`True` for
  `26127010` EL ALAMBRADO AUT**; (ii) CAL-8 window-mean fluxes span **3.31–22,050 t/day**
  (ln **1.20–10.00**, all positive), which is what makes §3.1's KGE `m` denominator safe.
- **Every other number here is carried from a prior document or from `docs/43`'s three lenses**,
  cited in place. Nothing was recomputed.
- **UNCITED quantities are named as such and pass or fail nothing:** the 0.05–0.30 SDR band and
  its implied `k ≈ 0.0020–0.0032 /km`; the **ENSO-neutrality of CAL 2012–14** (§3.5), which is
  the premise of the out-of-sample split and carries a registered remedy; the `m'` KGE bias
  variant (§3.1). The α box and the β box are **search boxes, not plausibility bands**, and §2.1
  says so.
- **The `docs/23` §13.2 yield embargo is in force** and §5.1 registers it as a not-claim.

---

## 8 — Amendment slot

*Empty at registration. Amendments are appended here, dated, each with the reason and the name
of the session making it. A threshold changed after seeing the number it judges is not a
threshold; a section of §2–§6 may be amended but never rewritten, and the original text stays
visible.*
