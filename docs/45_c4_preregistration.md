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
| three free parameters {α, β, deposition coefficient} | **two free** {α (as the handle on Π), β} **+ one FIXED at zero and reported as a bound** | lens 3 (`docs/43` §3.2): `k` is **not identifiable** on the achievable fit set (~~`k_min` 0.0209 /km~~ → **0.0838 /km**, §8 Amendment 1, 2026-08-12). Reporting a fitted `k` would be reporting noise with a decimal point. `docs/43` §3.1 **P3**. |
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

- it is the band for the **source LS formulation**; ours is ~~**2.37×–3.00×**~~ that level on the
  same 90 m grid over all 30,235,916 cells (`docs/35` §6.1 caveat; `docs/37` §4 candidate 0);

  > **[WARN] AMENDMENT 3, 2026-08-12 — SUPERSEDED BY MEASUREMENT; `2.37×–3.00×` MAY NOT BE
  > QUOTED AS LIVE.** Measured on the same 90 m grid, engine re-run: `f_LS` ∈ **[0.25146,
  > 0.43194]** erosion-weighted ⇒ **`1/f_LS` = 2.3151× – 3.9768×** (`docs/47` §4.3; `docs/46`
  > §1.0, §2.5.1's register, which names this site). **The source formulation read whole is a
  > POINT at ×0.25146** (`docs/51` §2.3; adopted `ls_formulation` = `buarque_2015_dg`,
  > `docs/37` A3); **×0.43194 is a documented HYBRID** — the source's three levers with **our**
  > `L` — retained only because `docs/35` §9.3.1, `docs/37` §4 candidate 0 and `docs/43` §1.4
  > quote it. The span between them is the **`L`-form lever**, not uncertainty. See §8
  > Amendment 3. **The α box [2.0, 30.0] is NOT amended here** — re-expressing the gate is
  > `docs/47` B2 and belongs to its owner.
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
| SE of the fleet-mean level | ~~**0.1644 ln = ±38 % at 95 %** (0.724×–1.380×)~~ **RETIRED — §8 Amendment 1, 2026-08-12.** Measured per-station residual sd **1.9618 ln** (est. b) / **1.3506 ln** (est. a) ⇒ SE **0.6936** / **0.4775 ln**. The band is now the **station bootstrap** (§8 amd 1) | ~~13 stations would have given ±28.8 %~~ **WITHDRAWN — §8 Amendment 1. No corrected value exists**: a 13-station residual set does not exist, only 8 stations have a paired CAL day at all |
| SE of β (pessimistic, σ_day = 0.809 ln) | **0.0199**; 95 % half-width **0.039** | against a registered band half-width of 0.10 ⇒ β is comfortably determined |
| `k_min` on the fit set | ~~**0.0209 /km** (own span 60.4 km ⇒ no sink weaker than **3.54×** is detectable)~~ **CORRECTED — §8 Amendment 1, 2026-08-12: `k_min` = 0.0838 /km ⇒ no sink weaker than ≈ 173× over 61.5 km is detectable** (0.0883 /km ⇒ ≈ 164× on `docs/42` §4.1's printed `Lw`) | ⇒ **`k` is not fittable** — the corrected figure makes this **more** certain, not less |

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
~~**≈ 2.12× over 348.4 km** at best (all-18 test, `k_min` 0.00216 /km)~~.

> **[WARN] AMENDMENT 1, 2026-08-12 — THE BOUND IS RESTATED AT ITS CORRECTED POWER, AND THE
> SENSE OF THE SENTENCE IS SETTLED.** `k_min` ∝ σ_r, and σ_r's reuse as a residual sd is
> retired. Measured (all 18, G1.2's registered joint form): **`k_min` = 0.0065 – 0.0069 /km
> (joint form 0.00686) ⇒ ≈ 9× – 11×, central ≈ 10× over ~342 km** (`docs/48` §4.2). The
> registered sentence is corrected to read **"no first-order channel sink WEAKER than ≈ 10×
> over ~342 km is detectable on this fit set"** — settling the *stronger*/*weaker* phrasing
> defect `docs/48` §4.2 flagged, in favour of **weaker**, which is the only correct sense of a
> detection floor. See §8 Amendment 1. **`k` is still FIXED at 0.0 /km and the SDR = 1.0 claim
> below is unchanged** — what changes is that the evidence for it is measured to be weaker than
> registered by **×3.18** in `k` and **×4.91** in the survival contrast the sentence prints.

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
   (G1.2) runs on **all 18** with ARRANCAPLUMAS *scored*, and keeps its `k_min` = ~~0.00216 /km~~
   **0.0065 – 0.0069 /km** (§8 Amendment 1, 2026-08-12).

**Cost, stated and not hidden:** fitted area stays **5.4 %** of the basin (13,862 km²) instead
of 25.1 %; the fit set's own `k_min` stays ~~**0.0209 /km** instead of 0.00303 /km~~ — a factor 6.9
in deposition detectability *on the fit set*, which §2.3 declines to use anyway.

> **[WARN] AMENDMENT 1, 2026-08-12.** Both `/km` values are σ_r-scaled and are corrected:
> **0.0838 /km** instead of **0.01210 /km** (the 9-station set's own CAL-window residuals,
> sd 1.8361; `docs/48` §5.2 row 14). **The factor 6.9 SURVIVES UNCHANGED** — it is a ratio of
> two σ_r-scaled numbers and σ_r cancels (0.0838/0.01210 = 6.93). Recorded so this line is not
> over-corrected. The cost of the P2 decision is unchanged; **§2.4's decision is unchanged.**

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
rating residual σ = **0.809 ln**, ~~SE of the fleet level = **0.1644 ln**~~ SE of the fleet level =
**0.4775 ln** (est. a) / **0.6936 ln** (est. b) (§8 Amendment 1, 2026-08-12). *The reason for the
log transform is unaffected — the corrected figures make the case for it stronger.*

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

> **[WARN] AMENDMENT 1, 2026-08-12 — WHAT σ_r MAY AND MAY NOT BE USED FOR.** σ_r = 0.465 ln is
> **valid as it stands** for what it measures: the disagreement between two *observed-flux*
> estimators (`0.658/√2`, `docs/42` §4.2). **Its reuse as the per-station model−observation
> residual sd is RETIRED** — measured **1.9618 ln** (est. b) / **1.3506 ln** (est. a). That
> retirement reaches **exactly two things and nothing else**: (i) the SE of the fleet-mean level
> and the ±38 % band, and (ii) every `k_min` power number. **UNAFFECTED and NOT to be
> "corrected":** G1.1's `D_pair > +0.658`, **G8**'s 0.465 ln and **G11**'s 0.465 ln — these are
> *firing* thresholds, where the error makes the guard **more** trigger-happy and so errs
> **safe** (`docs/47` R4) — the `b_obs` IQR **0.464** (independently measured from
> `ssc_rating_fits.csv`; the near-equality with 0.465 is a coincidence of value) — **SE(β) =
> 0.0199** and its half-width 0.039 (built on σ_day = 0.809 ln, the rating residual) — **G12's
> 0.644 ln full width**, which §8 Amendment 1 re-grounds as a *standalone* fragility threshold —
> and every ratio of two σ_r-scaled numbers (σ_r cancels). *One caution, and it is not a
> correction (`docs/48` §5.4): with a fleet residual sd of 1.35–1.96 ln, a between-month or
> between-region difference of 0.465 ln is well inside ordinary sampling noise at n = 8, so a
> G8 or G11 FAIL must be read for what it is. **G8 and G11 are frozen and are not touched.***

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
| **G1.2** | missing channel deposition — **the registered primary** | `r_i = c + k·Lw_i + ε_i`, OLS over **all 18**, fitted **jointly** with G3.1 and G4.1 as one multiple regression | the 95 % station-bootstrap interval for `k` lies **entirely above 0** | as above | **Do not adopt the fit** — same action as G1.1. If neither G1.1 nor G1.2 fires, **that is NOT A PASS**: report the bound `\|k\| < k_hi` in the registered sentence (§2.3), ~~≈ **2.12×** over 348.4 km at best~~ **≈ 10× over ~342 km** (`k_min` 0.0065–0.0069 /km; §8 Amendment 1, 2026-08-12), in the **"no sink WEAKER than"** sense settled there. Report the Jensen term when `k̂ · sd(L) > 0.3`. **A univariate `Lw` slope reported alone is not an acceptable G1 output.** |
| **G2.1** | the peak deficit folded into β — the α-free test | `ln flux ~ ln Q` per station, OLS on logs per rating era, station value = median over eras, once observed and once simulated (`q_sim_fit_m3s`) | fleet median **\|b_sim − b_obs\| > 0.464** (the between-station IQR of `b_obs`); **or** `b_sim − b_obs > 0` **and** β̂ within 0.02 of its box edge | `sed_station_daily.npz` + `q_gauge_H2E.npz` + `ssc_rating_fits.csv` | Report and **attribute to (β, the runoff partition)** — the test localises the fault there and **explicitly does not license a change to α, C or LS**. |
| **G2.2** | the peak deficit folded into α — residual by flow band | fleet-median relative residual below observed Q50, Q50–Q95, above Q95 | below-Q50 residual **> +25 %** while the above-Q95 residual is **negative** | **estimator (a) only** (`docs/42` G2.2's registered restriction); **EL ALAMBRADO excluded** (§3.4) | **STOP and report.** α has absorbed the peak deficit. Not adopted. |
| **G2.3** | β amplification | β̂ | **β̂ > 0.65 or β̂ < 0.45** (`docs/35` §6.3, re-affirmed) | `c4_parameters.csv` | **HARD STOP.** Not adopted. Report with the `docs/43` §1.3 counter-evidence and a *proposal* for a `docs/35` §9 amendment — never an enactment. |
| **G3.1** | a class-specific C error | `r_i = c + k·Lw_i + c_G·share_Grass_i + c_B·share_Bare_i + ε_i` over all 18 (joint with G1.2, G4.1). Forest is the reference class — its collinearity with `c` **is** the α confounding, correctly quarantined | the 95 % station-bootstrap interval for **`c_G` or `c_B` excludes 0** | `SedResult.cell_eroded_t` + `SedGeometry` + station residuals | Revise **that class's `C`** in `urh_cp_factors.csv`, with the reason and the source in that row's own columns, and refit. **Never α.** `c_B` must be run and reported **whichever way it comes out** — it would be the first independent evidence this project has ever had about the Bare class. |
| **G3.2** | unidentifiable classes | Shrub, Cropland, Urban, Water, Wetland — ≤ 3.1 % of erosion at **every** station | C4 **fits** any of them, or reports one as validated | — | Reporting FAIL. Every table listing them carries **ASSUMED** (or **CITED** per `docs/41`) — **never validated**. |
| **G3.3** | the C **level** | not testable by any fit — it *is* Π | a C4 table quotes a load without the level's evidence grade | — | Reporting FAIL. Grades per `docs/37` A1.6 item 3. **Cited is not validated, and fitted is not validated either** (`docs/43` §3.3 item 1). Registered in advance: G3.1's minimum detectable class-C error is **×4.2** on the CAL 8 (×2.9 on all 18) — *(**[WARN] AMENDMENT 1, 2026-08-12: both figures are σ_r-scaled and are therefore too OPTIMISTIC by roughly the σ_r factor. NO CORRECTED NUMBER EXISTS and none is invented here** — three independent passes have produced three different values (×4.2/×2.9 registered; ×8.2/×3.2 `journal_refute-gate-logic`; ×5.58/×3.53 and ×251.6/×57.9 `docs/48` §6.2). This is carried as `docs/47` **open item O8**. The direction is the safe one: the true detectability is **worse**, so the conclusion that follows is **strengthened**, not weakened.)* — so **G3.1 could not have seen `docs/41`'s ×1.2043 revision** — G3.1 **cannot audit `docs/41`**, and C3 clause 3 stays open however it comes out. |
| **G4.1** | a steepness-dependent LS error | add `ln LS̄_i` (station erosion-weighted LS2D, 38.2–117.1) to the joint regression | the 95 % interval for its coefficient **excludes 0** | as G3.1 | Fix the LS2D field, or adopt a **steepness-dependent** correction with its derivation. **Never α, and never a scalar `ls2d_resolution` multiplier** — a scalar cannot fix a slope-dependent error, only hide it in Π. |
| **G4.2** | the LS **level** | not testable | C4 changes `ls2d_aggregation`/`ls2d_resolution` to move the level, or reports the level as validated | — | Reporting FAIL. The level is **UNVALIDATED** and must be printed that way. A G4.1 non-detection exonerates the field's *shape* and says **nothing** about its level. |
| **G5** | the deposition precondition that replaced the blinded α band | (1) a named non-trivial sink **or** the §2.3 claim in those words; **and** (2) G1.2's `k̂` **with its interval, in the same table as α** | either leg missing | `c4_parameters.csv`, the C4 document itself | **AUTOMATIC FAIL regardless of what `check_musle_parameters` returns.** A fitted α in 5.9–23.6 obtained without both legs is not a result. |
| **G6** | the level-invariant report | five mandatory elements: **(1)** Π with its full decomposition; **(2)** α **with its application unit** (`docs/35` §6.2 — α = 12 is textbook-perfect at `a_p` = 0.0081 km² and a **2.2× over-fit** at minibacia scale) and its registered band beside it; **(3)** `SedParams.convention_summary()` verbatim; **(4)** the **equifinal family** — at minimum the three tuples giving the same Π at `C_mult ∈ {1, 2, 5}`; **(5)** the per-factor evidence grade | **any one missing** | every C4 table | **Reporting FAIL, blocking adoption.** |
| **G7** | cross-phase compensation | fit on one ENSO phase, score on the other | the El Niño 2015–16 residual more positive than the La Niña 2011 residual by **> +10 %** (`docs/35` §5.4; `R_AMS` 0.8875/0.8097 = 1.096) | `sed_station_daily.npz` + the C2 artifacts | Report either way — **the direction is known in advance to flatter the headline contrast**, so silence here is not neutral. |
| **G8** | seasonal structure | median `r_i` by calendar month, fleet-pooled, primary estimator (b) | the **range across months** of the fleet-median monthly residual **> 0.465 ln** (one σ_r) | as above | Report and **attribute** — candidates: the runoff partition, the C field's lack of a seasonal cycle (one annual `C` per class in a basin with two rainy seasons and crop calendars), the antecedent-state effect (`docs/31` §C4.2). **Not α.** |
| **G9** | mandatory disclosure of the unobserved fraction | **66.53 %** of gross erosion (199.29 of 299.54 Mt/yr) upstream of **no** usable SSC station; **33.47 %** is; **801.1 km** of channel including the whole Momposina below the outlet-most station | a **basin-scale** conclusion drawn from station fits **without it in the same paragraph** | — | **Reporting FAIL.** Passing G1–G8 constrains the model over **33.47 %** of its own erosion. **It is not closure of C3.** |
| **G10** *(NEW)* | **the fit determined a level and nothing else** | decompose the CAL improvement in `F_report` from the unfitted default into its `r`, `v`, `m` contributions. On log flux, **α moves only `m`**; `r` and `v` are **invariant to α** exactly | **> 80 %** of the improvement attributable to the **`m` (bias) component** | `c4_grid.csv` | **Not a FAIL — a MANDATORY STATEMENT.** C4 must state, in the abstract and the verdict: *"the calibration determined a level and essentially nothing else."* **Omitting it when the threshold is met is a reporting FAIL.** Registered because a KGE improvement that is all bias term is Π being set, which §1.4 already says is all a fit can do. |
| **G11** *(NEW)* | **the spatial contrast that IS evaluable**, standing where "above vs below Mompós" cannot | fleet median `r_i` by **macro-region** (Magdalena vs Cauca), all 18, and reported for the CAL 8 (2 macro-regions, 6 departments) | the between-region difference in median `r_i` **> 0.465 ln** (one σ_r) | station residuals + `_c1_geom.csv` | **FAIL.** A scalar α cannot be right in two regions at once; report and attribute to the regional axis (forcing field density, land-class composition, rating-era vintage) — **never to α**. Registered as **weak by construction** at n = 8 across 2 groups; the all-18 form is the deciding one. |
| **G12** *(NEW)* | **single-station fragility at n = 8** | refit **8 times**, leaving out one CAL station each time; record `F_report`, α̂, β̂, and the §6 verdict for each | **the §6 verdict flips on any single deletion** | `c4_grid.csv` re-run ×8 (cheap: the surface is precomputed per station) | **INDETERMINATE**, not a pass and not a fail (§6). Also mandatory whether or not it fires: report the **range of ln Π̂ across the 8 LOO refits** against ~~the registered 95 % level band of **±0.322 ln (±38 %)**~~ **the registered STANDALONE FRAGILITY THRESHOLD of ±0.322 ln — 0.644 ln full width — DECOUPLED from the level band by §8 Amendment 1, 2026-08-12, and retained at its registered value**; an LOO range exceeding it means the level is set by one station. *(Pre-fit, on the measured CAL-window residuals, the LOO range is **0.8602 ln** > 0.6445, i.e. **this comparison already exceeds its threshold**: deleting one of the eight CAL stations moves the level by up to **×2.36**. `docs/48` §3.2. A C4.3 that reports it NOT exceeded is itself reportable. The **verdict-flip** condition in the FAIL column is untested pre-fit and is unchanged.)* The `26127010` EL ALAMBRADO deletion is called out by name (§3.4). |

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
> composition form). Lens 3 measured that a class-C error smaller than **×4.2** *(σ_r-scaled and
> too optimistic; **no corrected value exists** — `docs/47` **O8**, §8 Amendment 1, 2026-08-12)*
> is invisible to
> this fit set. **Therefore C4 reports the fitted Π, its ~~±38 %~~ station-bootstrap band (§8
> Amendment 1, 2026-08-12), its equifinal family and a
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
2. ~~**The level's band is ±38 %** (0.724×–1.380×; SE 0.1644 ln at n = 8).~~
   ~~Every Π and every load is quoted **with that band**, never as a point.~~

   > **[WARN] AMENDMENT 1, 2026-08-12 — THIS IS THE SENTENCE THE AMENDMENT REPLACES. The
   > ±38 % band is RETIRED; the obligation to quote a band is NOT.** The replacement, in the
   > same registered form:
   >
   > > **The level's band is the STATION-LEVEL BOOTSTRAP of the fleet-mean per-station log
   > > residual — `docs/45` §4.2's already-registered interval convention, applied to the level.
   > > Every Π and every load is quoted with that band, never as a point, together with the
   > > sentence *"the level is set by 8 stations whose residuals span a factor of 412."***
   >
   > **Pre-fit expectation (a procedure, not a constant):** ×0.418 – ×2.289 (est. a) ·
   > ×0.286 – ×3.730 (est. b) · **quoted union ×0.29 – ×3.73**. Full derivation, the binding
   > estimator decision, and the seed are in §8 Amendment 1. **The band is WIDER, so this is a
   > weaker claim, not a rescue.** And it is a **REPORTING** band: **it is NOT a materiality
   > threshold and may not be used as one, nor may a materiality bar be reconstructed from it**
   > (`docs/52` §7 item 2, binding on every document).
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
| Yardsticks | σ_r **0.465 ln** *(valid as an estimator-disagreement statistic only; its reuse as a residual sd is retired — §8 amd 1)* · pair-σ **0.658 ln** · `b_obs` IQR **0.464** · ~~level SE **0.1644 ln (±38 %)**~~ **level band = the station bootstrap, pre-fit ×0.29–×3.73 (§8 Amendment 1, 2026-08-12)** · β SE **0.0199** *(unaffected)* |
| Preconditions discharged | `docs/43` §3.1 **P1** (§3.4), **P2** (§2.4), **P3** (§2.3). The `docs/42` §9 transcription **remains owed** to that file's owner. |
| Amendments | **THREE, all dated 2026-08-12, all in §8, by the `amend-45-piband-disclosure` agent** (process record `docs/agents/journal_amend-45-piband-disclosure.md`). **Amendment 1** — the ±38 % Π band **REPLACED** by the station bootstrap, and the `k` bound restated at **≈ 10× over ~342 km** (discharges `docs/47` §6.1 **B5**). **Amendment 2** — the **PRE-FIT DISCLOSURE**: the registered objective has already been profiled across the whole registered α box (discharges `docs/47` §5.5; `docs/47` **O9** carried, not decided). **Amendment 3** — §2.1's superseded LS bracket `2.37×–3.00×` struck; `1/f_LS` = **2.3151×–3.9768×**, the source read whole a **POINT** at ×0.25146 (discharges `docs/46` §2.5.1's register for this file). **§2–§6 were not otherwise edited; every superseded number remains readable inside a strike-through with a dated pointer** (`docs/37` A2.7 pattern) |

### 7.2 What this document does **not** do

- It does **not** edit `docs/42` or `docs/35`. Both are frozen; this document imports them,
  records where they are measured to be mis-specified, and **follows them anyway**.
- It does **not** narrow the `docs/35` §5.3 bias bracket, decide the SDR question, resolve the
  LS-formulation decision (C3.1), or close any C3 clause.
- It does **not** launch a search, fit anything, or produce a number that any gate here judges.
  > **[WARN] AMENDMENT 2, 2026-08-12 — STILL TRUE OF THIS PASS, NO LONGER TRUE OF THE PROJECT.**
  > This sentence is **not struck**: it remains an accurate statement about the registering pass.
  > But the registered objective **has since been evaluated by another session**, on this
  > document's own fit set, window, estimator and α box. **A C4.3 session may therefore no longer
  > claim to be a blind pre-registered fit.** The full disclosure — what was profiled, by whom,
  > where the record is, and the measured profile itself — is **§8 Amendment 2**, and it is
  > **mandatory in `report_C4.json` and in the C4 document** (`docs/47` §5.5, §6.2 item 6).
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

**No longer empty. Three amendments, all 2026-08-12, all by the `amend-45-piband-disclosure`
agent (process record `docs/agents/journal_amend-45-piband-disclosure.md`).** §2–§6 were **not
rewritten**: every superseded number stays readable inside a `~~strike-through~~` with a dated
pointer to this section, per the house pattern of `docs/37` A2.7 and `docs/46`'s inline `[WARN]`
blocks. **Nothing here changes a threshold that any gate judges** — see Amendment 2's §8.2.7 for
why that distinction is the whole of the O9 question.

---

## 8.1 — Amendment 1 — 2026-08-12 — **the ±38 % Π band is REPLACED by the station-bootstrap band; the `k` bound is restated at ≈ 10× over ~342 km**

**Discharges `docs/47` §6.1 repair B5.** Reason: `σ_r = 0.465 ln` is the disagreement between two
**observed-flux estimators** (`docs/42` §4.2, `0.658/√2`), and §2.2/§3.1/§5.3/§6.2/§7.1 of this
document used it as the **per-station model−observation residual sd**. Those are different
quantities; the second is measured to be **2.90× – 4.22×** larger. The derivation of §2.2's own
band was therefore **falsified**, not merely imprecise.

### 8.1.1 The measurement this amendment rests on

Carried from `docs/48` §2.3–§2.4, which reproduced it independently behind **two reproduction
gates that both passed exactly** — basin gross hillslope erosion **299.5387088 Mt/yr** against
`docs/37` A1.3.4's **299.5387**, and the CAL-8 paired SSC + observed-Q day count **3,266**,
exactly §3.6's registered denominator. Nothing below is a new measurement by this pass; the
arithmetic tying it together was re-derived and is recorded in this amendment's journal.

| quantity | registered here | **measured** |
|---|---:|---:|
| per-station residual sd, CAL 8, CAL window, estimator **(b)** — `docs/42` §9's primary | 0.465 ln | **1.9618 ln** (**×4.22**) |
| per-station residual sd, CAL 8, CAL window, estimator **(a)** — §7.1's objective estimator | 0.465 ln | **1.3506 ln** (**×2.90**) |
| SE of the fleet-mean level, est. (b) | 0.1644 ln | **0.6936 ln** (95 % factor 3.89×; normal band 0.257× – 3.894×) |
| SE of the fleet-mean level, est. (a) | 0.1644 ln | **0.4775 ln** |
| per-station `r = obs/sim`, CAL window | — | **0.0099 – 4.077**, a factor of **412** (412.1) |
| LOO range of `ln Π̂` across the 8 CAL stations | — | **0.8602 ln** ( = 6.0214/7 exactly) ⇒ **×2.36** |

**The defect is not removable by anything C4 fits, and this is measured, not assumed.** Fitting Π
subtracts a constant from every `r_i`: it moves the mean to ≈ 0 and leaves the sd — hence the SE,
hence the band — untouched. That is what makes a **pre-fit** registration of the band legal.
β moves the scatter the **wrong** way across its whole registered box (CAL-8 est. b: 1.875 at
β = 0.40 → 2.100 at β = 0.75), and adding G3.1's class shares and G4.1's `ln LS̄` to the mandatory
joint regression **raises** the residual sd. Deleting three of the eight CAL stations still leaves
sd = **1.83 × σ_r**. Model up-areas match at all 18 stations, so it is not a mapping artifact.

### 8.1.2 ROUTE CHOSEN: **(b) the station-level bootstrap** — and why route (a) is REJECTED

`docs/47` §2.2 offers two routes and says either is a §8 amendment, not a new registration.
**Route (b) is adopted.** Route (a) — promoting **G12**'s leave-one-out range to a
band-**replacement** rule — is **rejected on two measurements, not on preference**
(`docs/48` §3.2):

1. **It is arithmetically degenerate.** For a mean, the jackknife SE is *identically* `sd/√n` and
   the LOO range is *identically* `range(r_i)/(n−1)`. Measured both ways: jackknife SE **0.6936** =
   `sd/√n` **0.6936**; LOO range **0.8602** = 6.0214/7 **0.8602**. So route (a) delivers either the
   corrected normal band under another name, or a **range** — and a range is not an interval.
   Converting one into a 95 % band needs a conversion constant **this repository cannot cite**.
   That would be **inventing a band**, which is the move `docs/40` retired the SDR band for and
   `docs/52` retired the 0.1644 ln bar for. **Three bands have been retired on that rule
   (an "LS 2–10 mountainous" band, the "SDR 0.05–0.30" band, and `docs/46`'s own 0.1644 ln
   materiality bar). This amendment does not introduce a fourth.**
2. **It destroys G12.** G12's entire content is the comparison *LOO range vs the level band*.
   Defining the band **from** the LOO quantities makes that comparison circular. And measured, the
   direction matters: under the registered ±0.322 ln band the comparison **exceeds** (0.8602 >
   0.6445); under **either** corrected band it does not (2.7190 normal, 2.5667 bootstrap).
   Re-pointing G12 at the new band would convert a firing guard into a silent one **by widening
   the thing it is compared against** — the shape of every gate failure this project has refused.

> **CONSEQUENTLY REGISTERED, and it is the operational heart of this amendment: G12's threshold
> is DECOUPLED from the level band and RETAINED AT ITS REGISTERED VALUE — ±0.322 ln, 0.644 ln
> full width — as a STANDALONE fragility threshold.** Its provenance (originally σ_r/√8) is
> recorded and no longer load-bearing; its diagnostic content survives the correction intact and
> is worth keeping: *an LOO range of 0.8602 ln means deleting one of the eight CAL stations moves
> the fitted level by up to a factor of 2.36.* `docs/52` §7 item 7 independently leaves G12's
> 0.644 ln untouched. **Amendment 1 does not change G12's FAIL condition** (a §6 verdict flip on
> a single deletion), its INDETERMINATE action, or the named `26127010` EL ALAMBRADO deletion.

**Consistency with the parallel repair.** The `docs/43` §3.2 half of this same fix is being
enacted concurrently by another session. This amendment cites **the same route** — `docs/48` §3.3,
which is route 2 of `docs/47` §2.2 — and **the same numbers** (sd 1.9618 / 1.3506 ln; SE 0.6936 /
0.4775 ln; bootstrap half-widths 0.8500 / 1.2833 ln; union ×0.29 – ×3.73). **Stated honestly:
`docs/43` §3.2's Π row was still unamended on disk when this amendment was written** (`docs/43`:191
still prints `0.465/√8 = 0.1644 ln = ±38 %` and the ±28.8 %), so consistency here is guaranteed
**by construction** — same route, same source document, same numbers — and is **not** verified
against a written `docs/43` amendment. **Any disagreement between the two enactments is a defect in
one of them and must be reconciled before C4.3 prints a number, not averaged.**

### 8.1.3 THE REPLACEMENT, registered

> ## REGISTERED PROCEDURE — the 95 % band on Π̂
>
> **The band on Π̂ is the station-level bootstrap of the fleet-mean per-station log residual:
> resample the CAL stations with replacement, recompute the fleet mean inside each resample, take
> the 2.5 / 97.5 percentiles.** This is **§4.2's already-registered interval convention**,
> imported unchanged from `docs/42` §6 — *"a station-level bootstrap … station resampling, not day
> or pair resampling"* — now applied to the level, which was the only quantity in the guard set
> still on a bespoke normal-theory formula. **No new statistic is introduced.**
>
> **Registered mechanics:** **10,000** station resamples, seed **20260810** (the seed `docs/48`
> §3.3 used, so the pre-fit expectation below is exactly reproducible). **This consumes none of
> the four registered DDS seeds 20260921–24 and none of the 5,482-evaluation budget.**
>
> **THE BAND IS A PROCEDURE, NOT A CONSTANT.** C4.3 recomputes it on its own adopted fit's
> residuals and reports what it gets. The numbers below are the **pre-fit expectation**, registered
> here so that a materially different C4.3 number is itself reportable. Registering the procedure
> rather than a frozen pair of numbers also discharges `docs/48` §6.1 **P5** (the sd is measured to
> rise monotonically 1.875 → 2.100 across the registered β box, so a frozen pair would be wrong at
> the adopted β).

| estimator | point (ln) | bootstrap CI about the point | **band on the level** | half-width (ln) | normal ±1.96·SE, for comparison |
|---|---:|---|---|---:|---|
| **(a)** — §7.1's objective estimator | +2.5772 | [−0.8279, +0.8721] | **×0.418 – ×2.289** | **0.8500** | ±0.9359 ⇒ ×0.392 – ×2.550 |
| **(b)** — `docs/42` §9's registered primary | +1.9240 | [−1.3163, +1.2503] | **×0.286 – ×3.730** | **1.2833** | ±1.3595 ⇒ ×0.257 – ×3.894 |

*(The band on the LEVEL is the reciprocal of the residual CI, because `r_i = ln(sim/obs)` and the
level correction is `exp(−r)`. Verified arithmetically this pass, not assumed: `exp(−0.8721)` =
0.4181 and `exp(+0.8279)` = 2.2885. The bootstrap is marginally narrower than the normal band and,
unlike it, **asymmetric** — the honest shape for a log-space level at n = 8.)*

**DECIDED HERE, discharging `docs/48` §6.1 P1, which that document referred explicitly to this
document's owner.** `docs/42` §9 registers estimator **(b)** as primary; §7.1 of this document
registers the objective on **(a)**; they give bands differing by a factor of **1.51** in log
width (2.5667 vs 1.7000 ln). Neither frozen document may be edited, and §6.1 already makes
estimator disagreement an **INDETERMINATE** trigger for *verdicts* — so it cannot be resolved for
a *band* by picking a winner. Therefore:

> **REGISTERED, as a reporting convention and explicitly NOT a statistical claim:**
> ```
> Pi_hat  x  [0.29, 3.73]     (95 %, station bootstrap, UNION over estimators (a) and (b))
> ```
> **The per-estimator bands are printed beside the union, always.** The union spans a factor of
> **13.0** in the pre-fit expectation, where the retired band spanned **1.91**.

**The mandatory sentence of §6.2 item 2, in its replaced form** (`docs/47` §6.2 item 3 fixes the
words; the measured value is supplied here):

> **The level's band is the station-level bootstrap of the fleet-mean per-station log residual.
> Every Π and every load is quoted with that band, never as a point, together with the sentence
> *"the level is set by 8 stations whose residuals span a factor of 412."***

### 8.1.4 The `k` bound, restated at its corrected power, and the sense of the sentence SETTLED

`k_min = 1.96 · σ_r / √Σ(Lw_i − L̄)²` (`docs/42` §9.5), so **every `k_min` in the corpus is linear
in σ_r** — which is why one falsified σ moves them all. Measured on the **registered joint form**
(G1.2 fitted jointly with G3.1 and G4.1, all 18):

> ## THE CORRECTED SENTENCE
> ```
> k_min = 0.0065 - 0.0069 /km      (all 18, G1.2's registered joint form, measured residual sd)
> ```
> > **"No first-order channel sink WEAKER than ≈ 10× over ~342 km is detectable on this fit
> > set."**  *(equivalently: `|k| < 0.0069 /km` cannot be distinguished from zero)*
>
> **Registered: 2.12× over 348.4 km. Corrected: ≈ 9× – 11×, central ≈ 10×** (joint form
> `k_min` 0.00686 /km ⇒ 10.41× over 341.5 km; 0.00694 ⇒ 11.02× on `docs/42` §4.1's printed `Lw`
> span 345.8 km). `docs/47` §2.6 item 2 and §6.2 item 4 already require this wording; `docs/48`
> §4.2 supplies the interval and the design matrix.
>
> **THE PHRASING DEFECT IS SETTLED, and settling it is this owner's job** (`docs/48` §4.2 flagged
> it and left it to whoever enacts): §2.3 and G1.2 wrote *"no sink **stronger** than X×"* while
> §2.2 wrote *"no sink **weaker** than 3.54×"*. **Only "weaker" is the correct sense of a
> detection floor**, and **"weaker" is the registered wording from this amendment forward.**

**What this does and does not do to §2.3's registered claim.** `k` stays **FIXED at 0.0 /km**,
`TransportParams.dep_mode = 'per_km'`, `tau_channel_days = 0`, and the claim *"this model asserts
SDR = 1.0 between hillslope and station"* stands **in the words §2.3 registers**. G5's two legs are
unchanged in form. **What changes is the strength of the evidence for the claim, and it is
measured: the guard that would betray SDR = 1.0 is weaker than registered by ×3.18 in `k`
(0.00216 → 0.00686 /km) and ×4.91 in the survival contrast the sentence prints (2.12× → 10.41×).**
The corrected bound **must travel with the SDR = 1.0 claim wherever it appears** — §2.3, G5 and
G1.2 — per `docs/47` §6.2 item 4. **The one-shot `k_hi` sensitivity re-solve of §2.3 is unchanged
in form and is now a wider excursion**, `k_hi` being read off G1.2's corrected interval.

*(Also recorded, from `docs/48` §6.3: the corrected `k_min` of 0.0065–0.0069 /km now sits **above**
the whole uncited 0.05–0.30 SDR band's implied `k ≈ 0.0020–0.0032 /km`, where the registered
0.00216 sat inside it. **That band is UNCITED and passes and fails nothing** (`docs/40`); the
observation is scale reference only and no gate reads it.)*

### 8.1.5 EVERY PUBLISHED NUMBER THAT CHANGES

Line numbers are as of this document **before** this amendment's strikes. Every "old" string
below survives in the body inside a strike-through — **nothing was deleted.**

| # | § / line | old | **new**, or open item |
|---|---|---|---|
| 1 | §0 table, :32 | `k_min` on the achievable fit set **0.0209 /km** | **0.0838 /km** |
| 2 | §2.2, :124 | SE of the fleet-mean level **0.1644 ln = ±38 % at 95 %** (0.724×–1.380×) | residual sd **1.9618** (b) / **1.3506 ln** (a) ⇒ SE **0.6936** / **0.4775 ln**; **band = the station bootstrap**, ×0.286–×3.730 (b) / ×0.418–×2.289 (a), **union ×0.29–×3.73** |
| 3 | §2.2, :124 | *"13 stations would have given **±28.8 %**"* | **WITHDRAWN. No corrected value exists** — a 13-station residual set does not exist; only 8 of the 13 have a paired CAL day at all (`docs/48` §5.1 row 9) |
| 4 | §2.2, :126 | `k_min` on the fit set **0.0209 /km**, *"no sink weaker than **3.54×**"* over 60.4 km | **0.0838 /km ⇒ ≈ 173× over 61.5 km** (0.0883 /km ⇒ ≈ 164× on `docs/42`'s printed `Lw`) |
| 5 | §2.3, :162 | **≈ 2.12× over 348.4 km** at best, all-18 test, `k_min` **0.00216 /km** | **`k_min` 0.0065–0.0069 /km ⇒ ≈ 10× over ~342 km**, in the **"weaker than"** sense |
| 6 | §2.4, :202 | the all-18 test *"keeps its `k_min` = **0.00216 /km**"* | **0.0065–0.0069 /km** |
| 7 | §2.4, :205 | the fit set's own `k_min` stays **0.0209 /km** instead of **0.00303 /km** | **0.0838 /km** instead of **0.01210 /km** (that 9-station set's own CAL-window residuals, sd 1.8361). **The factor 6.9 SURVIVES** — σ_r cancels in a ratio (0.0838/0.01210 = 6.93) |
| 8 | §3.1, :252 | SE of the fleet level = **0.1644 ln** | **0.4775 ln** (a) / **0.6936 ln** (b). The case for the log transform is *strengthened* |
| 9 | §4.2 preamble, :397–398 | σ_r **0.465 ln** listed as a registered yardstick | **kept, with its use restricted**: valid as an estimator-disagreement statistic; **its reuse as a residual sd is retired**. pair-σ 0.658, `b_obs` IQR 0.464, SE(β) 0.0199 **unchanged** |
| 10 | §4.2 **G1.2**, :429 | the reported bound ≈ **2.12×** over 348.4 km at best | **≈ 10× over ~342 km** |
| 11 | §4.2 **G3.3**, :435 | G3.1's minimum detectable class-C error **×4.2** (CAL 8) / **×2.9** (all 18) | **OPEN ITEM O8. No corrected number exists and none is invented** — three passes, three answers (×4.2/×2.9 · ×8.2/×3.2 · ×5.58/×3.53 and ×251.6/×57.9). The error is in the **safe** direction: true detectability is worse, so G3.3's conclusion is **strengthened** |
| 12 | §4.2 **G12**, :445 | *"the registered 95 % level band of **±0.322 ln (±38 %)**"* | **DECOUPLED, value RETAINED**: a **standalone** fragility threshold, ±0.322 ln / **0.644 ln full width**. Pre-fit LOO range **0.8602 ln > 0.6445** ⇒ **the comparison already exceeds** (×2.36 per deletion). G12's FAIL condition and action are unchanged |
| 13 | §5.3, :493 | class-C error smaller than **×4.2** invisible to this fit set | **OPEN ITEM O8**, as row 11 |
| 14 | §5.3, :494 | *"C4 reports the fitted Π, **its ±38 % band**, …"* | *"… its **station-bootstrap band**, …"* |
| 15 | **§6.2 item 2**, :541 | *"**The level's band is ±38 %** (0.724×–1.380×; SE 0.1644 ln at n = 8). Every Π and every load is quoted **with that band**, never as a point."* | **THE MANDATORY SENTENCE ITSELF IS REPLACED**, in the form quoted in §8.1.3. This is the headline, and the one place `docs/47` §2.2 notes carried **no hedge** |
| 16 | §7.1 card, :575 | level SE **0.1644 ln (±38 %)** | **level band = the station bootstrap**, pre-fit ×0.29–×3.73, **a procedure not a constant** |
| 17 | §7.1 card, :577 | Amendments **none** | **Amendments 1, 2, 3**, all 2026-08-12 (Amendment 3 = §8.3) |
| 18 | §2.1, :98 | *"ours is **2.37×–3.00×** that level"* | **§8.3 Amendment 3**: `1/f_LS` = **2.3151×–3.9768×** |

**DOES NOT CHANGE — stated so nothing is over-corrected.** σ_r = 0.465 ln itself as an
estimator-disagreement statistic (§4.2 preamble, `docs/42` §4.2) · pair-σ **0.658 ln** and
**G1.1**'s `D_pair > +0.658` firing threshold · **G8**'s 0.465 ln and **G11**'s 0.465 ln (firing
thresholds; the error errs **safe**, `docs/47` R4) · `b_obs` between-station IQR **0.464**
(independently measured; the near-equality with 0.465 is a coincidence of value) · **SE(β) =
0.0199** and its half-width 0.039 (built on σ_day = 0.809 ln, the rating residual) · **G12's
0.644 ln** (retained, re-grounded) · **every ratio of two σ_r-scaled numbers**, including the
factor **6.9** at :205 and `docs/37`:1155's 2.2×/9.7× · **all five §6.1 outcomes and all eight
ADOPT conditions** — *measured: none of the eight reads the level band* (`docs/48` §3.4) · the
bar **[−0.26, 0.44]** · the boxes · the search budget · the four DDS seeds · the CAL 8 · the
windows · every not-claim of §5.

### 8.1.6 What this amendment is NOT, and one carried disagreement

1. **A reporting band on Π is NOT a materiality threshold, and no materiality bar may be
   reconstructed from anything in this amendment** — not from 0.4775, not from 0.6936, not from
   0.8500 or 1.2833, not from the union ×0.29–×3.73, and not from G12's 0.644 ln. `docs/52` §7
   item 2 is **binding on every document**, and `docs/46`'s 0.1644 ln bar is **STRUCK, not
   rescaled** (`docs/52`). There is no numeric materiality bar anywhere, and this amendment
   creates none.
2. **Not a rescue.** A wider band is a **weaker** claim. Nothing that failed passes because of
   it, and the corrected `k` bound makes the SDR = 1.0 evidence **worse**, not better.
3. **Not a re-registration of anything a gate judges.** No threshold, no box, no bar, no station
   list, no window, no seed, no budget moves. See Amendment 2 §8.2.7.
4. **Not an edit to `docs/42`, `docs/43`, `docs/35`, `docs/37`, `docs/46`, `docs/47` or
   `docs/48`.** Two sites were **checked on disk at the time of writing rather than assumed**:
   `docs/42`'s §9.5 pointer **has already been repaired by its own owner** — `docs/42`:863 now
   reads `~~**0.0130 /km**~~` with amendment **A-P4 (§9.7, 2026-08-12)** withdrawing it and
   confirming the all-18 figures, so **no correction is owed there any longer**. `docs/43` §3.2's
   Π row (`docs/43`:191) **does still carry `0.465/√8 = 0.1644 ln = ±38 %` and the ±28.8 %**; that
   is owed to its owner and is **reported, not fixed, here**.
5. **CARRIED DISAGREEMENT, reported not resolved.** `docs/47` §2.2's table row *"`k_min`, CAL-8
   form … **0.0130 /km**"* **does not reproduce and is arithmetically impossible as labelled** —
   `k_min ∝ σ/√Sxx`, so on a fixed station set a σ **4.22×** larger cannot yield a `k_min`
   *smaller* than the registered 0.0209. `docs/48` §4.3 traced it: **0.0130 is the 10-station set
   that happens to have CAL-window observations, which includes `21237020` ARRANCAPLUMAS** — an
   **EVAL** station §2.4 registers **out of the fit** — measured **0.01230 /km** there, with
   ARRANCAPLUMAS alone supplying **87.6 %** of that set's `Σ(Lw−L̄)²`. **This amendment adopts
   0.0838 /km as the CAL-8 figure and records 0.0130 /km as WITHDRAWN.** A correction to
   `docs/47`:148 and to `docs/42`:805 is owed to those files' owners.
6. **Not a correction of `docs/42` §4.1's `Lw` table or land-class shares**, which `docs/48` §2.5
   measured as not reproducing at the adopted `cp_revision` (IRRA 289.14 vs 265.2, CAPITANEJO
   64.15 vs 60.4; BANANERA Forest/Grass/Bare 26.0/24.5/49.5 vs 11.9/12.5/75.6). Immaterial here
   (≤ 2 % on `k_min`, and both `Lw` tables are reported above) but **G3.1's regressors and §3.4's
   station table are read off it**. `docs/48` §6.1 **P3**, owed to `docs/42`'s owner.

### 8.1.7 Open items this amendment carries and does not close

**O8** (class-C detectability, §8.1.5 row 11) · **`docs/48` P2** — the 22-pair `k_min`
**0.00119 /km ⇒ 1.51×** is σ_r-scaled and therefore wrong, and **cannot be corrected**: the 22
pairs are printed in no document and `Σ(ΔLw − ΔL̄)²` is not reconstructible from what is
published. **No corrected value is offered.** G1.1 is corroboration-only (the verdict is G1.2's),
so this does not block · **`docs/48` P3** (the `docs/42` §4.1 `Lw` table) · **`docs/48` P5**
(β-dependence — discharged in form by registering the band as a procedure) · and the CAL-13
`k_min` **0.00964 /km** at `docs/42`:744/:798, already SUPERSEDED by that document's own A-P1;
**flagged, not recomputed** — a CAL-13 residual set does not exist.

---

## 8.2 — Amendment 2 — 2026-08-12 — **PRE-FIT DISCLOSURE: the registered objective has already been evaluated across the whole registered α box**

**Discharges `docs/47` §5.5, whose consequence that document registers as NOT OPTIONAL.**
§7.2 states, of this document's own registering pass, that it *"does not launch a search, fit
anything, or produce a number that any gate here judges."* **That remains true of that pass and is
no longer true of the project.** §7.2 is annotated in place and **not struck**.

### 8.2.1 WHAT was profiled, on WHOSE configuration

**This document's own registered configuration, in every particular** — which is exactly why the
disclosure is owed rather than merely interesting:

| element | registered here | what the profile used |
|---|---|---|
| objective | §3.1 `KGE_ln` = `1 − √((r−1)² + (v−1)² + (m−1)²)`, on ln flux in t/day | the same |
| fit set | §3.4 the **CAL 8** | the same eight codes |
| window | §3.5 **`2012-01-01 … 2014-12-31`** | the same |
| estimator | §3.3 **(a)**, `Qs = Q × C × 0.0864`, `c1_deleted == False`, same-day `q_m3s` | the same |
| statistics | §3.2 `F_search` = **mean**, `F_report` = **median** | the same |
| α coverage | §2.1's box **[2.0, 30.0]** | **the whole box**, and beyond it in both directions |
| β coverage | §2.1's box **[0.40, 0.75]** | **nine β values** — `0.40 · 0.45 · 0.50 · 0.56 · 0.60 · 0.65 · 0.70 · 0.75` are tabulated in the record, which also states *"9 full re-simulations"*; **the tabulated count is eight and the stated count is nine, and this discrepancy is disclosed rather than reconciled** |

### 8.2.2 BY WHOM, and WHERE the record is

- **By the `refute-gate-logic` agent working the α-level finding**, on 2026-08-11, as an
  **adversarial refutation** pass whose posture was *"assume the finding is WRONG; try to prove
  it."* It mounted five attacks and all five failed.
- **The record is `docs/agents/journal_refute-gate-logic-alpha.md`.** That filename is itself part
  of the disclosure: the orchestrator assigned the agent `journal_refute-gate-logic.md`, a
  **different** refutation agent (target: the σ_r finding) had already written that file, the first
  write **clobbered** it, and the α-level agent moved to the uniquely-named file so neither
  agent's evidence was lost. **The σ_r refutation lives in `journal_refute-gate-logic.md`; the
  α-level profile lives in `journal_refute-gate-logic-alpha.md`.**
- The agent **flagged the disclosure itself**, under the heading *"DISCLOSURE OWED (important —
  flag to the orchestrator)"*: *"Whoever runs C4 must disclose that this profile existed
  beforehand."* **This amendment is that disclosure.**
- **Two reproduction gates passed BEFORE any statistic was computed**, so neither side of the
  comparison is that pass's own invention: basin gross erosion **299.5387088 Mt/yr** against
  `docs/37` A1.3.4's **299.5387** (exact to 7 s.f.), and the CAL-8 paired-day count **3,266**,
  **exactly §3.6's registered denominator**.
- **Nothing was written to the repository and no frozen artifact was touched.** The numeric
  artifacts (`refute_alpha_cal_beta*.csv`, `refute_alpha_summary.json`, `refute_alpha_out.txt`,
  `refute_gate_check.txt`) and the generating script (`refute_alpha_level.py`) live **only in that
  session's scratchpad** and are therefore **not reproducible from this repository** — the same
  loss mode `docs/00` §6 and `docs/47` O11 already record. **The journal is the record.**

### 8.2.3 Two of this document's own registered pre-checks were incidentally discharged

Recorded because they are §2–§6 obligations and a C4.3 session would otherwise re-do them:

- **§3.4's admissibility floor:** per-station paired-day counts **637 / 213 / 145 / 112 / 845 /
  176 / 661 / 477**, all ≥ **91**. §3.4's claim that all 8 clear the stricter C1.1 floor is
  **independently corroborated**, and the *"if fewer than 6 of the 8 remain"* EXPLORATORY branch
  is not triggered.
- **§3.1's numerical-stability pre-check:** `mean(ln obs)` = **2.16 – 7.11** per station, all
  > 1.0, and no simulated zero days. **The `m'` bias-term fallback is NOT triggered**, so the
  INDETERMINATE branch that a `m`/`m'` disagreement would open does not arise.

### 8.2.4 THE MEASURED PROFILE, disclosed because concealing it now would be the worse error

Carried verbatim from `docs/47` §2.1 and the named journal, cited in place. **These are profile
argmaxes and objective values of the registered objective at the unfitted default configuration.
They are NOT an α̂: no search was run, no fit was performed, no parameter was estimated by any
C4 stage, and this pass evaluated nothing.** Scaling sim by `f` shifts `mean(y)` by `ln f` and
leaves `r` and `v` untouched, so `KGE_ln(α)` is **exact** from the per-station moments — the
profile is arithmetic on eight stations' moments, not a search.

**At β = 0.56:**

| α | `F_search` (mean) | `F_report` (median) |
|---:|---:|---:|
| 0.117 — unconstrained argmax of `F_report` | −0.583 | **−0.029** |
| 0.625 — unconstrained argmax of `F_search` | −0.579 | −0.163 |
| **2.0 — the registered box floor** | **−0.621** | **−0.349** |
| 3.9 — the `docs/35` §6.1 hard stop | −0.675 | **−0.486** |
| 11.8 — Williams (1975), §2.1's reference value | −0.805 | **−0.737** |
| 30.0 — the registered box ceiling | −0.947 | **−0.849** |

**Both statistics are monotone decreasing across the whole registered box.** The in-box optimum
is the box **floor** for `F_search` at every β ∈ [0.40, 0.70] and for `F_report` at every
β ∈ [0.40, 0.75].

**Best attainable in-box `F_report` across the G2.3 β gate:** **−0.350** (β 0.45) · **−0.350**
(β 0.56) · **−0.305** (β 0.65). **Every one is below the bar's lower edge −0.26.** The implied
level at β = 0.56 is 0.0760 ⇒ α 0.897 (arithmetic station ratios) / 0.1026 ⇒ α 1.211 (log-mean
ratios, the quantity KGE's `m` term zeroes); inside the G2.3 gate the free optimum is α
**0.26 – 1.29** (`F_search`) / **0.05 – 0.33** (`F_report`).

> **The consequence, stated plainly and not softened:** the headline outcome of the registered
> search is **already known** — `FAIL — RAILED / HARD STOP` **and** `FAIL — NUMERIC`, both §6.1
> outcomes, both predictable in advance and now computed. **A pre-registered search whose verdict
> is already known is not a test.** This is `docs/47`'s reason for
> **`C4.3-BLOCKED-UNTIL-LS-LANDS`**, which this amendment does not weaken.

### 8.2.5 THE REGISTERED CONSEQUENCE — not optional

> **A C4.3 session may no longer claim to be a blind pre-registered fit.**
>
> **This disclosure is MANDATORY in two places** (`docs/47` §5.5 and §6.2 item 6):
> **(1) `report_C4.json`** — a named field recording that the registered objective was profiled
> before the fit, **by whom**, **on what configuration**, and **where the record is**; and
> **(2) the C4 document itself**, in the verdict's own section, not a footnote.
> **A C4.3 output missing either is a reporting FAIL on the same footing as G5, G6 and G9.**

### 8.2.6 What this amendment does NOT do

1. **It quotes no α̂**, provisional or otherwise — §8.2.4's values are profile argmaxes at fixed
   β on an unfitted default configuration, and are labelled as such.
2. **It evaluates nothing.** This pass ran no simulation, launched no calibration, evaluated no
   `KGE_ln`, and consumed neither the 5,482-evaluation budget nor the DDS seeds 20260921–24.
3. **It does not amend §2.1's α box, §3.2's bar, §6.1's outcomes, or `docs/35` §6.1's 3.9/35.4
   stops.** Re-expressing the gate in a unit that survives the LS decision is `docs/47` **B2**
   and belongs to its owners; a concurrent session holds that job.
4. **It does not lift the block.** `C4.3-BLOCKED-UNTIL-LS-LANDS` stands (`docs/47` §5; B1's
   status is `docs/37` A3's to report).

### 8.2.7 `docs/47` **O9** — CARRIED, and a RECOMMENDATION that is explicitly not a decision

> **O9, verbatim:** *whether the pre-fit profile compromises `docs/45`'s freeze enough to require
> a FRESH PRE-REGISTRATION rather than a §8 amendment.* `docs/47` §7 **declined to decide** it and
> called it *"a governance decision by the document owner."*

**O9 remains OPEN and is carried unresolved. What follows is a RECOMMENDATION. I am
recommending, not deciding** — and the reason I decline to decide is not modesty: the same
argument that makes a §8 amendment legal for *some* changes makes it **illegal** for others, so a
single yes/no would be wrong either way. The recommendation is therefore **split**, on one
criterion that is already registered in §0: ***does the change touch a number the profile has
seen judged?***

1. **For everything in Amendments 1–3, a §8 amendment SUFFICES.** Measured, not asserted: **none
   of §6.1's eight ADOPT conditions reads the level band** (`docs/48` §3.4), and no threshold, bar,
   box, station list, window, seed or budget is moved by any of the three. A **reporting** band, a
   **bound's power**, a **phrasing sense**, a **superseded LS bracket** and a **disclosure** are
   not thresholds. Amending them post-profile cannot buy a pass, because none of them can turn a
   FAIL into an ADOPT.
2. **For `docs/47` B2 — re-expressing the α box, or restating `docs/35` §6.1's 3.9 / 35.4 — a §8
   amendment does NOT suffice, and I recommend a fresh, dated pre-registration.** §0's own rule is
   that *"nothing in §2–§6 may be edited after a number it judges has been computed"*, and the
   profile computed **exactly** the numbers §6.1 judges α̂ and `F_report` against, across the whole
   box. Restating those thresholds now would be done by a project that **knows which values put
   α̂ inside its box** — the same post-hoc move §2.4 refused for ARRANCAPLUMAS, in its own words,
   *"relax a frozen registration in order to gain statistical power, after the power had been
   measured."* **This is B2's owner's decision, not mine, and I do not make it here.**
3. **One asymmetry that argues for the §8 route and should be weighed, not ignored.** The lost
   blinding produced a **predicted FAILURE**, not a favourable result. The risk a blind
   registration exists to prevent — a threshold tuned to pass — is not the risk realised. And a
   *fresh* pre-registration of the whole document would re-open **every** threshold to a project
   that has now seen the surface, which is strictly more dangerous than amending a document whose
   thresholds were fixed blind. **A wholesale re-registration could make the governance problem
   worse.**
4. **The condition that would close the §8 route entirely, registered here so it cannot be
   discovered later:** if any session proposes to change **any of §6.1's eight ADOPT conditions,
   §3.2's bar `[−0.26, 0.44]`, §2.1's boxes, §3.4's fit set, §3.5's windows, or §2.5's search
   budget or seeds**, the §8 amendment route is **closed** and a fresh pre-registration is
   required. **That is a rule about the route, not a decision on O9.**

---

## 8.3 — Amendment 3 — 2026-08-12 — **§2.1's LS bracket `2.37×–3.00×` is SUPERSEDED BY MEASUREMENT**

**Discharges `docs/46` §2.5.1's re-derivation register for this file**, which names `docs/45` §2.1
by section as a site still printing the superseded bracket. That obligation is **unconditional** —
its ground is a measurement that has already landed, not the survival of any hypothesis.

| | superseded | **measured** |
|---|---|---|
| `f_LS`, erosion-weighted (decides) | ×0.333 – ×0.421 | **[0.25146, 0.43194]** (exact second reproduction 0.2514648985839397) |
| `f_LS`, area-weighted **PROXY** (beside it, never overriding) | — | **0.2446790094097074** – 0.42135; the proxy is measured **2.51 %** low, i.e. in the model's favour |
| `1/f_LS` — *"our LS is …"* | ~~**2.37× – 3.00×**~~ | **2.3151× – 3.9768×** (3.976775630318937 exact at the DG endpoint) |
| the shape of the interval | a bracket | **the source formulation read whole is a POINT at ×0.25146**; **×0.43194 is a documented HYBRID** keeping **our** `L`. The 0.5410027585442313 ln span between them is **the `L`-form lever**, not uncertainty |
| basin gross erosion at the endpoints | — | **75.32347104056149 Mt/yr** (DG `L`) · **129.3840 Mt/yr** (continuous `L`), against the adopted **299.5387088405831** |

**Provenance.** `docs/47` §4.3 (the measured bracket, engine re-run on all 30,235,916 cells at
90 m, **not** a scalar proxy) · `docs/46` §1.0 and §2.5.1 (the register) · `docs/51` §2.3 (point
vs hybrid) · `docs/37` A3 (the enactment: adopted `ls_formulation` = **`buarque_2015_dg`**, all
four levers **CITED** against Buarque (2015), LUME 10183/129875, sha256 `3047624f…c0037`, printed
pp. 47–48, 94, 98, 121). `docs/37` §4 candidate 0's ×0.333 endpoint is **refuted** (`docs/47`
§3.1 **R6**: it was 0.421 × 0.790, and 0.790 was two levers measured on the uncapped column and
confounded with an S swap).

**Its evidence grade is unchanged and must travel with it:** the LS **level** is **UNVALIDATED**
(§2.3's fixed-factor table, `docs/42` **G4.2**) — *cited is not validated, and fitted is not
validated either*. The bracket being CITED at both ends changes the **shape** of the uncertainty,
not the grade.

**What Amendment 3 does NOT do.**

1. **It does not touch §2.1's α box `[2.0, 30.0]`, and it does not touch `docs/35` §6.1's
   5.9–23.6 / 23.6–35.4 / 3.9 / 35.4.** Those are registered numbers, re-expressing the gate is
   `docs/47` **B2**, and a concurrent session owns it. **No rescaled α is registered here.** The
   arithmetic pairing of α with an LS is recorded in `docs/37` A3.2 and is bookkeeping about the
   pairing, not about α.
2. **It does not adopt or switch anything.** `ls2d_column` remains `"ls2d_hs"` and `urh_ls2d`
   remains `"urh_ls2d.csv"` (`src/mgb_sediment.py`). **Enactment is a written amendment, not a
   code edit**, and the engine-default switch is `docs/37`'s C3.1 owner's second, separately dated
   act, **not draftable until a gated `V4_dg` column exists**.
3. **It does not unblock C4.3** and does not close any C3 clause.
4. **It does not restate the derived quantities `docs/46` §2.5.1 also lists** — *"α reference ≈
   3.9 – 5.0"*, *"band ≈ 2.0 – 9.9"*, *"hard stop ≈ 11.8 – 14.9"*, the *"≈ 104.8 Mt/yr"* /
   *"≈ 126.1 / ≈ 99.7 Mt/yr"* proxy loads — **because this document prints none of them.**
   Verified by grep over the whole file: the only occurrences of those strings anywhere in
   `docs/45` are **this clause's own quotation of them**. Each is owed to the file that prints it.
5. **A defect in a file this pass does not own, reported and NOT fixed** (`docs/37` A3 reports the
   same one): `docs/46`:127 (§1.0) and `docs/51` §2.3 both print the identity
   `ln(0.43194/0.25146) = 0.5410 = −ln 0.580685`. Measured: `−ln(0.580685) = 0.543546837831505`
   against `ln(0.43194/0.25146) = 0.5410027585442313`, a gap of **0.0025440792872737372 ln**;
   `exp(−0.5410027585442313) = 0.5821641894707599`, so 0.5410 pairs with **0.58216**, not
   0.580685. Both constituents are separately correct; **the identity as written does not hold.**
   Immaterial to every verdict, including this amendment's.

---

## 8.4 — Disclosure for this amendment set

- **Files written:** `docs/45_c4_preregistration.md` (this file — §8 appended, plus
  strike-through-and-pointer annotations at **seventeen** body sites: the eighteen rows of
  §8.1.5 less its own §7.1-card row, plus the §4.2 σ_r-preamble `[WARN]` block, the §7.2
  annotation and the §7.1 Amendments cell. Counted, and every one is listed with its line in
  this amendment's journal) and
  `docs/agents/journal_amend-45-piband-disclosure.md`. **Nothing else in the repository.**
  `docs/33`, `docs/35`, `docs/37`, `docs/42`, `docs/43`, `docs/46`, `docs/47`, `docs/48`,
  `docs/51`, `docs/52`, `docs/53` were **read and not edited**.
- **§2–§6 were not rewritten and nothing was deleted, renumbered or silently changed.** Every
  superseded string survives inside a `~~strike-through~~` with a dated pointer to §8, per the
  `docs/37` A2.7 house pattern; the longer corrections use the `docs/46` inline `> **[WARN]
  AMENDMENT n, 2026-08-12 — …**` form. **Every original sentence remains readable.**
- **No frozen artifact was opened, read or written.** `sim_calibrated_v2/{h2e_drivers.npz,
  parameters_H2E.csv, q_gauge_H2E.npz, q_gauge_H2E.csv, report_H2E.json, metrics_fleet.csv}`,
  `data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv` and `urh_ls2d_variants.csv` were **not
  touched at all** by this pass.
- **No engine default was changed.** `ls2d_column`, `cp_revision`, `volume_convention`,
  `k_unit_system`, every `SedParams` field, every H2E parameter, α and β are untouched.
  **Enactment is a written amendment, not a code edit.**
- **No calibration was launched, no simulation was run, no LS pass was run, no search was
  started, no α̂ or β̂ was fitted, and no `KGE_ln` was evaluated against §2.1's α box by this
  pass.** The 5,482-evaluation budget and the four DDS seeds 20260921–24 are untouched.
  `docs/47` §6.3's permitted / not-permitted list was read before anything was written and obeyed.
- **What this pass measured itself:** only the arithmetic tying the carried figures together —
  the bootstrap half-widths from `docs/48` §3.3's published CIs (0.8500 / 1.2833 ln), their
  exponentials (×0.418–×2.289, ×0.286–×3.730, union log width 2.5666), the registered band's
  factors (exp ±0.322 = 0.7247 / 1.3799), `6.0214/7 = 0.8602` and `exp(0.8602) = 2.3636`,
  `exp(0.00216 × 348.4) = 2.1224` and `exp(0.00686 × 341.5) = 10.409`,
  `exp(0.0838 × 61.5) = 173.07`, `1/0.43194 = 2.315136`, `1/0.25146 = 3.976776`,
  `4.0766/0.0099 = 411.8`, and the σ-ratios 4.219 / 4.006 / 3.176 / 4.910. **Every one reproduces
  the published figure it was checked against.** Commands and verbatim output are in the journal.
  **Every other number is carried from a named prior document and cited in place.**
- **UNCITED quantities are named and pass or fail nothing:** the 0.05–0.30 SDR band and its
  implied `k ≈ 0.0020–0.0032 /km`; the **ENSO-neutrality of CAL 2012–14** (§3.5's premise, whose
  registered remedy is unchanged); the `m'` KGE bias variant. **No plausibility band was
  invented.** Where a corrected value does not exist — the ±28.8 % 13-station figure, the 22-pair
  `k_min`, the CAL-13 `k_min`, the class-C detectability (**O8**) — this amendment **says so and
  stops.**
- **NO MATERIALITY BAR IS CREATED, RESCALED OR RECONSTRUCTED** anywhere in this amendment set.
  `docs/52` is binding: 0.1644 ln is **struck**, not rescaled, and a **reporting** band on Π is
  **not** a materiality threshold.
- **The `docs/23` §13.2 yield embargo is in force.** No t/km²/yr, t/ha/yr or area-normalised
  sediment yield appears in this amendment set; §8.3's loads are absolute (Mt/yr).
- **Nothing is backdated. No git command was run.** `C4.3-BLOCKED-UNTIL-LS-LANDS` is unchanged by
  this amendment set, and no C3 clause is closed.

---

## 8.5 — Amendment 4 — 2026-08-12 — **the C4.3 gate is RE-EXPRESSED IN Π, the `f_LS`-invariant unit. The α box's CONTENT is unchanged; only the coordinate it is written in changes**

**Discharges `docs/47` §6.1 repair B2**, by the `gate-reexpression` agent (process record
`docs/agents/journal_gate-reexpression.md`). **It enacts one thing — the re-expression — and
proposes one thing — a `docs/35` §9 amendment — and the two are kept rigidly apart**, because
`docs/45` §6.1 lets a session that hits a registered stop *propose* a `docs/35` §9 amendment and
never enact it.

> **THE ONE-LINE VERDICT, put first because getting it wrong in the optimistic direction is the
> failure this amendment exists to avoid: the re-expression does NOT fix `docs/47`'s
> `FAIL — RAILED` / `FAIL — NUMERIC` pre-computability problem. It RELABELS it — and in the Π
> coordinate the problem is measurably WORSE, not better.** §8.5.8 states this with the
> arithmetic. **`C4.3-BLOCKED-UNTIL-LS-LANDS` is unchanged.**

### 8.5.1 The defect, in one paragraph

`docs/47` §2.1 **D1** and §5.1 **P1**: §2.1 of this document registers the search as a box on
**α ∈ [2.0, 30.0]** and §6.1's `FAIL — RAILED / HARD STOP` row reads α̂ against `docs/35` §6.1's
**3.9 / 35.4**. But α is only the *handle* on Π (§2.1 of this document, in its own words: *"what
C4 has determined is Π"*; `docs/42` §3.1: seven ways of writing one Π), and α's numerical value is
proportional to **1/`f_LS`**, while **Π is invariant to `f_LS`**. §2.3's own fixed-factor table
grades that scale **UNVALIDATED**, and `docs/47` §4.3 measures it uncertain by
**2.3151× – 3.9768×**. **The registered gate was therefore denominated in the one quantity whose
scale C3.1 decides.** That is what is repaired here.

### 8.5.2 ROUTE CHOSEN: **(A) re-express the gate in Π** — and why (B) is adopted only as a companion

`docs/47` §6.1 **B2** offers two acceptable routes. **(A) is taken as the unit of the gate.**

**Why not (B) — re-register the α box against the adopted `f_LS` — as the primary unit.** It does
not survive C3.1, which is the requirement B2 states. (i) Every α threshold would have to be
re-derived at every future `f_LS`, so the gate remains a *function* of an unresolved decision
rather than independent of it. (ii) The adopted `f_LS` is **DETERMINED and RECORDED but NOT YET
EXERCISABLE** (`docs/37` A3): `ls2d_column` is still `"ls2d_hs"` and `urh_ls2d` still
`"urh_ls2d.csv"` (`src/mgb_sediment.py`), and **no committed `V4_dg` column exists anywhere**, so
route (B) would register gate numbers against a level the engine cannot yet produce. (iii) Π is
invariant not only to `f_LS` but to **all seven** of §1 item 4's factors — `f_vol`, `f_K`,
`f_LS`, `C_mult`, `P`, `FG` and α — so route (A) also survives a future `cp_revision`, a change of
`k_unit_system`, or a change of `volume_convention`, none of which route (B) survives.

**Route (B)'s reporting requirement IS adopted, as a companion and not an alternative**
(`docs/47` §6.2 item 1, imported here): **no α̂ may be compared to a box edge, to 3.9, or to 35.4
without `f_LS` and its evidence grade in the same table.** This strictly *adds* a reporting
obligation to G6 element (2); it can only turn an ADOPT into a reporting FAIL and can never turn a
FAIL into an ADOPT, which is the test §8.2.7 registers for whether a §8 amendment is legal.

### 8.5.3 The conversion, exact, both ways — and its anchor

> ## REGISTERED — THE CONVERSION IS A FORMULA, NOT A CONSTANT
>
> ```
> Pi    =  alpha * k0 * f_LS                 (forward)
> alpha =  Pi / ( k0 * f_LS )                (inverse)
>
> k0    =  f_vol * f_K * C_mult * P * FG     (the product of §2.3's registered fixed factors,
>                                             f_LS factored out)
> f_LS  =  the LS field's level factor RELATIVE TO the adopted `ls2d_hs` field.
>          Registered value: **1.000** (§2.3's `ls2d_factor` 1.000 x 1.000; §7.1's card).
> ```
>
> Registering the conversion as a formula rather than a frozen constant is deliberate and follows
> Amendment 1's precedent (*"the band is a procedure, not a constant"*): `k0` is rebuilt from
> whatever §2.3 registers at the time it is evaluated, so it cannot go stale, and **no new constant
> is introduced by this amendment** — every input is already registered in §1 item 4 and §2.3.

**The anchor is registered, not chosen.** §7.1 registers `f_LS` = **1.000** among the fixed,
not-fitted factors, and §1 item 4 registers **Π = 5,164.42** at α = 11.8 on that configuration.
`docs/51` §6.3 **P1** states the same thing in one sentence: *"The box `[2.0, 30.0]` and the stop
3.9 were registered at `f_LS = 1`."*

**`k0`, evaluated three ways, all printed so no session has to choose:**

| construction | `k0` | Π at α = 11.8 | vs §1 item 4's registered **5,164.42** |
|---|---:|---:|---:|
| §2.3's printed factors, `C_mult` = **1.20427** | **437.66113721058014** | 5164.401419084846 | rel. **3.5978706523513363e-06** |
| §2.3's factors with `C_mult` at full precision **1.204272539864846** | 437.66206025951175 | 5164.412311062239 | rel. **1.4888289026620914e-06** |
| back-solved from the registered Π: 5164.42 / 11.8 | 437.6627118644068 | 5164.42 (by construction) | 0 |

The three agree to **3.597883597084349e-06** relative — printed rounding in the inputs, **not** a
substantive disagreement, and **explicitly not a materiality claim of any kind** (`docs/52` §7
item 2). Every number below uses the **first** row (§2.3's printed factors), because those are the
factors this document registers; the residue is four orders of magnitude below the smallest
quantity any statement here turns on (§8.5.8's ×1.5516).

### 8.5.4 THE RESTATED GATE, registered

> ## REGISTERED — the C4.3 gate, in Π
>
> | registered condition, as written in α | **the same condition, in Π** | Π value | α value at `f_LS` = 1.000 |
> |---|---|---:|---:|
> | §2.1 box, lower edge — α ≥ **2.0** | Π ≥ **2.0 · k0** | **875.3222744211603** | 2.0 |
> | §2.1 box, upper edge — α ≤ **30.0** | Π ≤ **30.0 · k0** | **13129.834116317405** | 30.0 |
> | §6.1 ADOPT (2) rail band, lower — α̂ ≥ 2.0 + 5 % of the box range | Π̂ ≥ Π_lo + 5 % of the Π range | **1488.0478665159726** | **3.4000000000000004** |
> | §6.1 ADOPT (2) rail band, upper — α̂ ≤ 30.0 − 5 % of the box range | Π̂ ≤ Π_hi − 5 % of the Π range | **12517.108524222593** | **28.6** |
> | §2.5 α axis — 71 points, log-spaced, step ×1.03945 | 71 points, log-spaced on the Π box | step **1.0394444954338562** | step **1.0394444954338562** — *identical* |
> | §2.5 refinement — ±1 coarse step about the argmax | ±1 coarse step (a multiplicative step) | unchanged | unchanged |
> | §2.5 budget — 5,041 + 441 = **5,482** | unchanged | unchanged | unchanged |
> | §3.2 bar — `F_report` ∈ **[−0.26, 0.44]** | unchanged — an objective value, **coordinate-free** | unchanged | unchanged |
> | §2.1 / G2.3 β box and gate | unchanged, and *structurally* so | unchanged | unchanged |
> | `docs/35` §6.1's **3.9 / 35.4** | **CARRIED UNCHANGED — not restated here.** §8.5.7 records both Π readings and PROPOSES the amendment | see §8.5.7 | see §8.5.7 |
>
> **Π_hi / Π_lo = 15.0 exactly**, as 30.0 / 2.0 = 15.0 — the ratio the box actually encodes.
>
> **β is untouched, and for a structural reason rather than by choice** (`docs/35` §9.4.5's own
> argument, imported): a constant multiplicative factor on the load moves α by that factor and
> **cannot move β at all**, because `f_LS` multiplies the load and sits **outside** the `β` power
> entirely. §6.2's `N^(2β−1)` scale table is dimensionless and is likewise untouched.

**The same Π box, expressed in engine-α units on other LS fields** — printed so a C4.3 session
that runs after `docs/37` A3's ACT 2 knows where to put its grid, and so nobody re-derives it:

| LS field | `f_LS` | box in engine α | rail band in engine α |
|---|---:|---|---|
| **`ls2d_hs`, the registered configuration** | **1.000** | **[2.0, 30.0]** — *the identity* | **[3.4, 28.6]** |
| `buarque_2015_dg` (`V4_dg`), the source read whole — the POINT | **0.2514648985839397** | [**7.953396323950136**, **119.30094485925204**] | [13.520773750715232, 113.73356743248695] |
| `V4`, the documented HYBRID (our `L`) | 0.43194417543884817 | [4.630227963991024, 69.45341945986537] | [7.8713875387847425, 66.21225988507166] |

*(The two non-registered rows are **consequential arithmetic**, not adoptions. `ls2d_column`
remains `"ls2d_hs"`. Enactment is a written amendment, not a code edit.)*

### 8.5.5 THE DEMONSTRATION — it forbids **exactly** what the original forbade, neither more nor less

`docs/45` §6.3 forbids a widened box; §8.2.7 item 4 closes the §8 route to any change of §2.1's
boxes. **This is therefore the load-bearing section of the amendment, and it is a proof, not an
assurance.**

**The structure of the argument.** `α ↦ Π = k0 · α` with `k0 > 0` is a strictly increasing
bijection of `(0, ∞)`. Every condition in §2.1, §2.5 and §6.1 that reads α is one of exactly three
forms, and a positive linear map preserves all three:

1. **membership in a closed interval** — preserved, because a strictly increasing bijection maps
   `[a, b]` onto `[k0·a, k0·b]` and preserves order;
2. **distance from an edge as a FRACTION of the interval's range** (the rail definition, `docs/33`
   §3.5) — preserved, because the distance and the range are multiplied by the same `k0`;
3. **a multiplicative grid step** — preserved, because a geometric progression stays geometric
   with the same ratio under multiplication by a constant.

**Verified numerically, not asserted** (`python3.10`, output in this amendment's journal §02):
the Π rail band **1488.0478665159726 … 12517.108524222593** maps back to α
**3.4000000000000004** and **28.6** — the *same* floating-point values the α form produces from
`2.0 + 0.05·28.0` and `30.0 − 0.05·28.0`; and the 71-point log grid step is
**1.0394444954338562** in **both** coordinates, bit for bit.

**The one form that would NOT survive, and the search for it.** An *absolute* distance in α (as
opposed to a fraction of the range) would not transform without changing what it forbids. The
whole document was searched for one. **There is exactly one absolute-distance condition anywhere
in §2–§6 and it is on β, not α**: G2.1's *"β̂ within 0.02 of its box edge"*. β is not rescaled by
anything here, so it is untouched. **No α condition in this document is stated as an absolute
distance.**

**Two secondary invariances, recorded so they are not discovered at run time.** (i) The DDS
corroboration's `r = 0.2` is a perturbation size on the **normalised** box coordinate
(Tolson & Shoemaker 2007), which is invariant under a positive affine rescaling of the box; an
implementation that perturbs in raw units must re-normalise, which is an implementation note and
not a change to this registration. (ii) The DDS-vs-grid discrepancy trigger — *"better than the
grid argmax by more than 0.005 in `F_search`"* — is in objective units and is coordinate-free.

> **CONCLUSION, registered:** at the registered configuration the restatement is the **IDENTITY**.
> The admissible set, the forbidden set, the grid, the step, the refinement, the budget, the seeds
> and the bar are unchanged. **Nothing is widened and nothing is narrowed.** What changes is that
> the boundary is now written in a quantity that does not move when C3.1 lands — which is B2's
> entire requirement.

### 8.5.6 THE DIRECTION — and the two conventions the corpus contains, one of which is retired here

**The direction, stated once, in the form least likely to be inverted by a reader:**

```
Pi = alpha * k0 * f_LS.      A SMALLER LS field needs a LARGER alpha for the SAME Pi.
                             Therefore alpha scales as 1 / f_LS.
  the same Pi box, in engine-alpha units on a field with factor f  ->  [ 2.0 / f , 30.0 / f ]
  docs/35's SOURCE-LS alpha numbers, in OUR engine-alpha units     ->  x f      (11.8 * f = 2.967)
```

The second line is **exactly what `docs/35` §6.1's own frozen caveat instructs** — *"every number
in the table below must be **divided** by that bracket before it is compared with an α fitted on
**our** LS"* — because dividing by `1/f` is multiplying by `f`. **Both directions cross-check
against `docs/46` §6.2 A4's own derivation:** A4 prints `30.0 / 3.9768 = 7.543`; measured here
`30.0 · f = 7.543946957518192`, and `30.0 / 2.3151 = 12.958403524685759` against
`30.0 · f_hybrid = 12.958325263165444`. A4's lower-stop arithmetic `2.0 / 3.9768 = 0.5029169…`
against `2.0 · f = 0.5029297971678794`. **Every printed digit agrees.**

**The corpus contains two incompatible conventions, and B2's job is to choose one.** They are:

| | convention | what happens to the box's **Π content** when the LS field is swapped | corpus sites |
|---|---|---|---|
| **(i)** | the box is held **literal on the engine's α parameter**; α̂ is rescaled by `1/f` | it **multiplies by `f`** — measured: [875.3222744211603, 13129.834116317405] → [**220.11282696558052**, **3301.692404483708**], a **×3.9767 drop in the floor** | `docs/46` §6.2 **A4**; `docs/47` §5.2's rescaling table; `docs/51` §6.2 |
| **(ii)** | the box is a constraint on **Π**, anchored at the registered configuration; the engine-α *edges* move | it is **invariant** | `docs/51` §6.3 **P1** states this as the principle; **this amendment enacts it** |

> **REGISTERED: convention (ii) is the gate. Convention (i) is RETIRED for gate purposes.** Four
> grounds, in order of strength:
>
> 1. **(ii) is what this document registered.** §2.5's grid is a grid on the engine's α *at the
>    registered configuration*, and §7.1 registers `f_LS` = 1.000 there. So the box's Π content is
>    `[2.0·k0, 30.0·k0]` **as registered**, and `docs/51` §6.3 P1 says so in one sentence.
> 2. **Only (ii) makes the box a GATE.** §6.1 ADOPT condition (2) makes railing at a box edge a
>    FAIL, so the edges are thresholds. A threshold whose content multiplies by `1/f_LS` whenever
>    someone swaps an LS field is not a threshold. **Reductio, and it is not rhetorical:** under
>    (i), an LS field 100× smaller would drop the box's Π floor 100× and admit almost any fit —
>    the gate would be defeated by a choice the gate is not supposed to be able to see.
> 3. **(ii) relaxes nothing** (§8.5.5, proved and verified bitwise), while **(i) relaxes the live
>    edge by ×3.9767 on a swap**. Adopting (i) would be relaxing a frozen gate **after** the
>    surface had been profiled (§8.2), in the direction that lets the fit pass — §2.4's forbidden
>    move, in §2.4's own words.
> 4. **(i) is measured to be the mechanism that produces the corpus's only optimistic corner.**
>    §8.5.8 shows this arithmetically. A convention that manufactures a pass is not a convention.

**This retirement edits nothing.** `docs/46`, `docs/47` and `docs/51` are not touched. Their
convention-(i) arithmetic was correct *as a diagnosis of the unfixed reading* — that diagnosis is
what motivated B2 — and their **verdicts are unaffected or strengthened** (§8.5.12).

### 8.5.7 `docs/35` §6.1's **3.9 / 35.4** — CARRIED UNCHANGED here, and the PROPOSED §9 amendment in full

**What this amendment does with them: nothing.** `docs/45` §6.1's `FAIL — RAILED / HARD STOP` row
continues to read *"α̂ > 35.4 or α̂ < 3.9 (`docs/35` §6.1)"*, unamended, with the two defects §2.1
already requires be printed beside it. **`docs/45` §6.1 permits a session that hits a registered
stop only to PROPOSE a `docs/35` §9 amendment**, and `docs/35` §9.4.5 explicitly reserves the
question for a §9 amendment *"written after such a proposal arrives."* This is that proposal.

**Both Π readings of `docs/35` §6.1, recorded here so no session has to reconstruct them and so
the direction cannot be lost** (`k0` = 437.66113721058014; `f` = 0.2514648985839397):

| `docs/35` §6.1 quantity | Π, **literal** reading (read against the engine α at `f_LS` = 1.000) | Π, **divided** reading (§6.1's own caveat, at the POINT) | α in **our** engine's units (= × `f`) |
|---|---:|---:|---:|
| expected band, lower **5.9** | 2582.200709542423 | 649.3328395484625 | 1.4836429016452444 |
| reference **11.8** (Williams 1975) | 5164.401419084846 | 1298.665679096925 | **2.9672858032904887** |
| expected band, upper **23.6** | 10328.802838169691 | 2597.33135819385 | 5.9345716065809775 |
| **HARD STOP, upper 35.4** | 15493.204257254536 | **3895.997037290775** | **8.901857409871466** |
| **HARD STOP, lower 3.9** | 1706.8784351212626 | **429.220012582882** | **0.9807131044773649** |

**Two measured consequences of the divided reading, both registered because they are not obvious:**

1. **The lower hard stop becomes INOPERATIVE.** Π = **429.220012582882** lies **below** this
   document's own box floor Π = **875.3222744211603**, so any fit inside the registered box
   automatically satisfies it. The box floor binds first, at every `f_LS`, because both are Π
   statements and both are invariant.
2. **The admissible window SHRINKS, it does not widen.** Today's literal reading admits
   α_ours ∈ (3.9, 28.6] ⇒ Π ∈ (1706.8784351212626, 12517.108524222593]. With the division applied
   the window is **Π ∈ [1488.0478665159726, 3895.997037290775]** ⇒ **α_ours ∈ [3.4,
   8.901857409871466]** — the ceiling tightens by ×3.9767 and the floor loosens only to the box's
   own rail edge. **The set of admissible fits gets smaller.**

---

> # PROPOSED AMENDMENT TO `docs/35` §9 — **NOT ENACTED HERE**
>
> **Addressed to `docs/35`'s owner.** Written by the `gate-reexpression` agent, 2026-08-12, as
> `docs/47` §6.1 **B2**'s deliverable and under `docs/45` §6.1's propose-never-enact rule. It is
> **ready to adopt verbatim**; it is **not** adopted by writing it here, and `docs/35` is not
> edited by this pass. `docs/35` §9.4.5 already anticipates it by name. **A parallel pass amended
> `docs/35` §9 on 2026-08-12 for other reasons (§9.4); this proposal is additional and does not
> assume §9.4 was made.**
>
> ---
>
> ### 9.5 Amendment — 2026-08-12 — **§6.1's α band is RE-EXPRESSED as a RATIO TO THE REFERENCE LEVEL, which is `f_LS`-invariant**
>
> **Reason.** §6.1's caveat (2026-08-11) requires every number in its table to be *divided by the
> LS level ratio* before it is compared with an α fitted on our LS. That instruction is correct and
> is the source of a hazard: it is a human step, performed in a direction that the corpus has
> already written **two incompatible ways** (`docs/45` §8.5.6), on a bracket whose value has since
> been re-measured twice. **A gate that requires a division to be performed by hand, in a direction
> that has been inverted in print, is not a gate.** This amendment removes the division by writing
> §6.1's band in a unit in which the ratio cancels identically.
>
> #### 9.5.1 The observation that makes this exact, not approximate
>
> §6.1's four registered numbers are already **multiples of its own reference value**, and three of
> the four are exact:
>
> | §6.1 edge | value | ÷ 11.8 |
> |---|---:|---:|
> | expected, lower | 5.9 | **0.5** exactly |
> | expected, upper | 23.6 | **2.0** exactly |
> | HARD STOP, upper | 35.4 | **3.0** exactly (`2.9999999999999996` in IEEE-754 double) |
> | HARD STOP, lower | 3.9 | **0.33050847457627114** |
>
> *(§6.1 labels the lower stop "⅓× Williams". **The registered number is 3.9, not 11.8/3 =
> 3.9333…**, so the ratio is taken from **3.9** and is 0.33050847457627114, not 1/3. Recorded so
> the re-expression cannot silently move the stop by 0.85 %.)*
>
> #### 9.5.2 THE RESTATED BAND, registered
>
> > **Registered form.** Let
> > ```
> > R_hat  =  Pi_hat / Pi_ref
> > Pi_ref =  11.8 * f_vol * f_K * C_mult * P * FG * f_LS(ref)
> > ```
> > where `f_LS(ref)` is the LS level factor of the LS field the reference α = 11.8 is paired with,
> > and `Pi_hat` is the fitted level of the SAME configuration in every other factor.
> >
> > | band | **registered condition, in `R_hat`** | C4 action — unchanged from §6.1 |
> > |---|---|---|
> > | expected | `R_hat` ∈ **[0.5, 2.0]** | adopt; report `R_hat` with this band beside it |
> > | watch | `R_hat` ∈ **(2.0, 3.0]** | adopt **only** with a written, non-peak physical justification; state that compensation was considered and why it is rejected |
> > | **HARD STOP** | **`R_hat` > 3.0** | **STOP. Do not adopt.** Report the fit, §5's bias, and that the threshold fired |
> > | **HARD STOP** | **`R_hat` < 0.33050847457627114** | **STOP.** The proxy is a floor (§3(i)); a level far below the reference means something upstream is over-producing, and that must be found, not offset |
> >
> > §6.3's β band **0.45 – 0.65** and §6.2's `N^(2β−1)` scale table are **unchanged**, and
> > structurally so: `f_LS` multiplies the load and sits outside the β power, so a level factor
> > cannot move β; `N^(2β−1)` is dimensionless.
>
> #### 9.5.3 Why this forbids **exactly** what §6.1 forbids
>
> `R_hat = Pi_hat / Pi_ref`, and both numerator and denominator carry the **same** `k0` and the
> **same** `f_LS` **provided the fit and the reference are evaluated on the same LS field**.
> Therefore `R_hat = alpha_hat / 11.8` **identically**, on every LS field, and the four conditions
> above are the four conditions of §6.1 with the mandated division already performed and impossible
> to invert, forget, or apply twice. **`f_LS` cancels; it does not have to be known.**
>
> #### 9.5.4 The one input this form needs, and its grade
>
> `Pi_ref` requires `f_LS(ref)` — the LS field Williams (1975)'s α = 11.8 was fitted against.
> **Its grade is NOT SETTLED and no band is offered** (`docs/37` A3 evidence proposition D;
> `docs/47` §4.2 item 6: *"α = 11.8 predates every 2-D contributing-area LS by two decades … no
> 2-D LS is strictly like-for-like"*; `docs/46` §1.0 residue 3; `docs/46` §1.0 residue 1: **neither
> bracket end is "his LS"** — both are the source's *formulation on our terrain*). **This amendment
> does not settle it and offers no band.**
>
> **What §6.1 already registers about it, and which therefore travels with `R_hat`:** §6.1's own
> text pairs the reference with Buarque's LS (*"α = 11.8 is paired with Buarque's LS"*, and
> *"adopted unchanged by Buarque 2015 eq. 5 with the same daily-mean `q_peak`, so it is the
> like-for-like reference under §4"*). Under that registered pairing and `docs/37` A3's adopted
> `ls_formulation = buarque_2015_dg`, `f_LS(ref)` = **0.2514648985839397** on our terrain, and the
> engine-α equivalents of the four edges are exactly §9.4.5's already-published column:
> **1.4836429016452444 · 5.9345716065809775 · 8.901857409871466 · 0.9807131044773649**, reference
> **2.9672858032904887**.
>
> **Registered with it, unchanged:** the LS **level** is **UNVALIDATED** (`docs/42` **G4.2**) —
> *cited is not validated, and fitted is not validated either*. Raising four levers to CITED raises
> their **provenance** grade only.
>
> #### 9.5.5 The direction of the change, stated against this proposal's own interest
>
> **Adopting this form moves BOTH stops down by ×3.9767** in our engine's α units: the lower stop
> from 3.9 to **0.9807131044773649** (a **loosening**) and the upper from 35.4 to
> **8.901857409871466** (a **tightening**). And **the loosened edge is the LIVE one**: `docs/45`
> §8.2 discloses that the registered objective has already been profiled across the whole α box and
> that the optimum sits at the **bottom**. So a session adopting this proposal is loosening the
> binding edge of a hard stop **after** the surface has been seen. **That must be weighed, not
> waved past.** Three measurements are offered, and they are offered as evidence, not persuasion:
>
> 1. **The loosening is not new and is not this proposal's.** §6.1's caveat mandating the division
>    is dated **2026-08-11** and was written against `docs/37` §4 candidate 0's much older bracket.
>    Only the bracket's numeric value has since been corrected by measurement, and that correction
>    belongs to `docs/47` §4.3 and `docs/46`, not here.
> 2. **Net, the admissible set SHRINKS.** In combination with `docs/45` §2.1's box the window
>    narrows from α_ours ∈ (3.9, 28.6] to **[3.4, 8.901857409871466]**, and the lower stop becomes
>    **inoperative** because `docs/45`'s box floor (Π **875.3222744211603**) binds above it
>    (Π **429.220012582882**).
> 3. **It is measured NOT to convert the pre-computed FAIL into a pass.** The profiled `F_search`
>    argmax at the most favourable G2.3 corner is Π̂ = **564.1452058644378**, still **×1.5515903801396431**
>    below `docs/45`'s box floor — which binds whichever stop applies. And `F_report` there is
>    **−0.305**, below the bar's lower edge **−0.26**, which no restatement of an α axis touches.
>
> #### 9.5.6 The weaker alternative, named so this is not presented as the only option
>
> `docs/35`'s owner may prefer to **leave §6.1 in α** and register only the *pairing print*: **no
> α̂ may be compared to 5.9 / 23.6 / 35.4 / 3.9 without `f_LS`, its evidence grade, and the division
> performed in the same table** (`docs/47` §6.2 item 1). That changes **no registered number at
> all**. It is weaker for one measured reason: it leaves the division a human step, and the corpus
> already contains that step written two incompatible ways (`docs/45` §8.5.6's table).
>
> #### 9.5.7 What this proposed amendment does **NOT** do
>
> 1. It does **not** change **5.9 / 23.6 / 35.4 / 3.9** as registered numbers. They stay, in α, for
>    the **source** LS, exactly as §9.4.5 insists.
> 2. It does **not** touch §6.3's β band, §6.2's scale table, §6.4's residual test, §6.5, RULE 0,
>    or any of §1–§5.
> 3. It does **not** adopt an LS variant, exercise a `docs/46` §4.2 outcome, or switch an engine
>    default. `ls2d_column` = `"ls2d_hs"`, `urh_ls2d` = `"urh_ls2d.csv"`. **Enactment is a written
>    amendment, not a code edit.**
> 4. It does **not** validate the LS level, close any C3 clause, or **unblock C4.3**.
>    `C4.3-BLOCKED-UNTIL-LS-LANDS` stands; **Branch B is MANDATORY** (`Δ_shape` =
>    **0.1299456916752905** > 0, `docs/46` §6.1, §6.3 B1, §10 amendment 1, `docs/53`).
> 5. It **quotes no α̂**, runs no fit, and evaluates nothing against `docs/45`'s box.
> 6. It **introduces no band and no threshold**, and in particular **no materiality bar**:
>    `docs/46`'s 0.1644 ln bar is **STRUCK, not rescaled** (`docs/52`), and nothing here may be
>    reconstructed as one. **An uncited band cannot pass or fail a gate.** Every number above is an
>    arithmetic consequence of a registered number.
> 7. It settles **nothing** about α = 11.8's like-for-likeness with a 2-D contributing-area LS
>    (§9.5.4). **NOT SETTLED; no band offered.**
>
> **— END OF PROPOSED `docs/35` §9.5 TEXT. NOT ENACTED. `docs/35` IS NOT EDITED BY THIS PASS. —**

---

### 8.5.8 Does this fix `docs/47`'s pre-computability problem? **NO. It relabels it, and in Π it is WORSE**

> ## THE ANSWER, PLAINLY
>
> **The re-expression removes the FLOATING-THRESHOLD problem. It does NOT remove the
> PRE-COMPUTABILITY problem.** `docs/47` §2.1's `FAIL — RAILED / HARD STOP` **and**
> `FAIL — NUMERIC` are both still computable in advance, and both are still computed. **In the Π
> coordinate the rail is worse: it holds in *three* of the three G2.3 β corners instead of two,
> and the corpus's only "one corner clears" is measured to be an artifact of the convention this
> amendment retires.**

**The rail, in Π** — §8.2.4's own profile, converted with `k0` and nothing else added:

| G2.3 corner | argmax α (`F_search`) | **Π̂** | argmax α (`F_report`) | **Π̂** |
|---|---:|---:|---:|---:|
| β = 0.45, the G2.3 floor | 0.258 | **112.91657340032968** | 0.050 | 21.88305686052901 |
| β = 0.56 | 0.625 | **273.53821075661256** | 0.117 | 51.206353053637876 |
| β = 0.65, the G2.3 ceiling | 1.289 | **564.1452058644378** | 0.325 | 142.23986959343856 |

Against the **Π box floor 875.3222744211603** and the **rail-trimmed floor 1488.0478665159726**:

- **every cell in that table is below the box floor**, so `FAIL — RAILED` in **every**
  G2.3-admissible β;
- the **most favourable** cell, `F_search` at β = 0.65, is short of the box floor by
  **×1.5515903801396431** and of the rail-trimmed floor by **×2.6377036462373935**;
- `F_report` at β = 0.65 is short of the box floor by **×6.153846153846153**;
- the implied levels §8.2.4 prints are also short: log-mean ratios at β = 0.56 give Π̂ =
  **530.0076371620125** (short by **×1.6515276630883566**), arithmetic ratios Π̂ =
  **392.5820400778904** (short by **×2.229654403567447**).

**And this holds at EVERY `f_LS`, which is the whole point of the unit:** Π̂ is `f_LS`-invariant
(`docs/47` §4.4, verified there by control to `|ratio − f| < 1e-12`) and the Π box is
`f_LS`-invariant by §8.5.4. **So the LS decision does not move the rail verdict at all.**

**`FAIL — NUMERIC` is untouched by construction.** `F_report` is an objective value, the bar
**[−0.26, 0.44]** is in objective units, and the best attainable in-box `F_report` across the G2.3
gate is **−0.350 / −0.350 / −0.305** (§8.2.4) — every one below **−0.26**. **No re-expression of
the α axis can reach a bar that is not written in α.**

**The optimistic corner, traced to its cause.** `docs/47` §5.2, `docs/51` §6.2 and `docs/46` §6.3
report that at the source LS level **one** G2.3 corner clears both thresholds (α̂-equivalents
**1.0259881257895676 / 2.4854363512344175 / 5.125963930785862** against a box floor of 2.0, a
5 %-rail band of 3.4 and the `docs/35` stop 3.9). **Measured: that corner exists only because
convention (i) drops the box's Π floor from 875.3222744211603 to 220.11282696558052 — a factor of
exactly `f` = 0.2514648985839397 — when the LS field is swapped.** Under convention (ii) the floor
does not move, and:

| corner | convention (i): box literal on engine α | **convention (ii): Π-invariant** |
|---|---|---|
| β = 0.45 | railed | **railed** |
| β = 0.56 | railed | **railed** |
| β = 0.65 | **clears** (α̂ 5.126 > 3.9, outside the rail band) | **railed** |

> **Consequently registered:** *"collapsing the bracket to its point leaves the registered search
> railing in **two of the three** G2.3 β corners"* becomes, in the gate's own unit, **three of the
> three, with no corner clearing.** `docs/46` §6.3's and `docs/51` §6.2's conclusions are
> **strengthened**, not contradicted; `docs/47` §5.2's *"one corner … clears both thresholds"* is
> **convention-dependent and does not survive the fix** (§8.5.12 item 3, reported not fixed).

**One further consequence, stated because it re-orders `docs/47` §5's own argument and a reader is
entitled to know.** `docs/47` §5.2 **P2** — *"the LS decision is the dominant term in the C4
verdict"* — is a convention-(i) statement. Under (ii), the LS decision **does not move the rail
verdict at all**. What it still moves is (a) the **shape** of the residual vector
(`Δ_shape` = 0.1299456916752905 > 0, hence O5 and `docs/46` §6.1's mandatory re-run), (b) the basin
load (**75.32347104056149** vs **299.5387088405831** Mt/yr), and (c) the `docs/35` **pairing**
(§8.5.7). **So the strongest remaining leg of the block is Branch B / `Δ_shape`, not P2** —
`docs/47` §5.1's **P1** is discharged by *this amendment*, and **P3** (deciding LS after the fit is
the forbidden post-hoc move) stands untouched and is now the second-strongest leg.

**What is therefore still true after B2 is discharged, in the words that matter:** *a
pre-registered search whose verdict is already known is not a test; it is a re-run of an answer,
and it spends a one-shot registration to produce it* (`docs/47`'s verdict box). **B2 removes the
unit defect. It does not make the search a test.**

### 8.5.9 `docs/47` **O5** — CARRIED UNCHANGED, and one bound that is explicitly not a resolution

> **O5, verbatim and unchanged:** *"whether `F_report` clears the bar anywhere in the box under a
> corrected LS. This run rescaled the α **axis**, which is exact for the level, but did not
> re-profile the objective on a corrected LS **field**, so the per-station residual redistribution
> (±1.287×) is unmodelled."* **Nobody has re-profiled the objective on a corrected LS field.
> "May clear" remains the strongest available statement, and this amendment does not weaken O5's
> status, close it, or substitute for it.**

**One bound is added, and it is a bound on the LEVEL term only.** Derivation, not assertion: under
the new field station `s`'s simulated flux is `Π · (h_s / f) · base_s` with
`h_s = E_s(V4)/E_s(V0)` and `f` the basin factor, so the station-optimal level is
`Π_s*(V4) = Π_s*(V0) · exp(−ln(w_s(V4)/w_s(V0)))` in `docs/46` §6.1's own `w_s` notation; hence for
a **fleet log-mean** level the shift factor obeys
`|ln shift| ≤ max_CAL |ln(w_s ratio)| = Δ_shape`. With the measured
**`Δ_shape` = 0.1299456916752905** (`docs/46` §10 amendment 1; `docs/53`):

```
maximal favourable shape-driven lift   = exp(+0.1299456916752905) = 1.1387665371423883
maximal unfavourable                   = exp(-0.1299456916752905) = 0.8781431201072979
gap it would have to close (box floor)                            = 1.5515903801396431
gap it would have to close (rail-trimmed floor)                   = 2.6377036462373935
after the maximal favourable lift, still short by  1.3625184175442946x  (box floor)
                                                   2.316281309825301x   (rail-trimmed floor)
on the log-mean implied level itself, still short by 1.450277655007924x
```

> **Registered with its limitation, which is the point of registering it:** `F_search` and
> `F_report` argmaxes are **not** a fleet log-mean level, so this bounds the **level** term and
> **does not** bound the argmax of either statistic. **O5 stays OPEN**, and it is the *only* route
> by which C4.3 could produce a verdict that is not pre-computed. **The honest statement is
> unchanged: "may clear", not "will clear" — and now also "the unmodelled term is measured to be
> smaller than the gap it would have to close."**

### 8.5.10 What this amendment does **NOT** do

1. **It does not widen the box, narrow it, add a parameter, or authorise a second search.**
   §8.5.5 proves the restatement is the identity at the registered configuration and verifies it
   bitwise. §6.3 is unchanged and unchallenged.
2. **It does not change a single threshold, bar, box, station list, window, seed or budget.** The
   bar **[−0.26, 0.44]**, the CAL 8, the windows, the **5,482**-evaluation budget, the DDS seeds
   **20260921–24**, G2.3's **[0.45, 0.65]**, and all five §6.1 outcomes stand as written.
3. **It does not amend `docs/35`.** §8.5.7's text is a **PROPOSAL**, labelled as such, addressed to
   that document's owner. `docs/35` was read and not edited.
4. **It quotes no α̂**, provisional or not. §8.5.8's figures are §8.2.4's already-disclosed profile
   argmaxes on an **unfitted default configuration**, converted to Π by multiplication — they are
   not a fit, not an estimate, and not an α̂.
5. **It evaluates nothing.** No `KGE_ln` was evaluated against §2.1's α box by this pass, no
   simulation, no calibration, no LS pass, no fit. The budget and the seeds are untouched.
6. **It does not adopt or switch anything.** `ls2d_column` remains `"ls2d_hs"`, `urh_ls2d` remains
   `"urh_ls2d.csv"`, `cp_revision`, `volume_convention`, `k_unit_system`, every `SedParams` field,
   every H2E parameter, α and β are untouched. **Enactment is a written amendment, not a code
   edit**, and the engine-default switch is `docs/37`'s C3.1 owner's separately dated ACT 2, **not
   draftable until a gated `V4_dg` column exists**.
7. **It creates, rescales and reconstructs NO materiality bar.** Nothing here — not `k0`, not its
   3.6e-06 reproduction residue, not Π_lo, not the ×1.5516 shortfall, not `exp(±Δ_shape)` — is a
   materiality threshold or may be read as one. `docs/52` §7 item 2 is binding.
8. **It does not unblock C4.3, and does not close any C3 clause.** **B2 is discharged; B1 is
   not**, Branch B is mandatory, and the pre-computed FAIL stands (§8.5.8).
9. **It strikes nothing in §2–§6, and that is deliberate**: a restatement that changes no
   admissible set supersedes no body number, so there is nothing to strike. §2.1's box still reads
   **[2.0, 30.0]** because **[2.0, 30.0]** is still correct.

### 8.5.11 The route question — why §8, and exactly where §8.2.7 item 4 binds

§8.2.7 item 2 **recommends a fresh, dated pre-registration** for `docs/47` B2, and item 4
registers that a proposal to change *"§2.1's boxes"* **closes the §8 route**. That recommendation
is taken seriously and is answered on its own registered criterion — ***does the change touch a
number the profile has seen judged?***

1. **The re-expression does not.** Measured, not asserted: the admissible set, the forbidden set,
   the rail band, the grid, the step, the refinement, the budget and the bar are **identical** at
   the registered configuration (§8.5.5, verified bitwise). The profiled verdict is therefore
   **identical** — `FAIL — RAILED` **and** `FAIL — NUMERIC` — and under the enacted convention it
   is **more** certain, not less (§8.5.8: three corners rather than two). **A restatement that is
   measured to make the pre-computed outcome worse cannot have been chosen to buy a pass**, which
   is the only hazard §8.2.7's criterion exists to catch.
2. **The part that WOULD touch such a number is not enacted here.** Restating `docs/35` §6.1's
   3.9 / 35.4 loosens the live edge by ×3.9767 (§8.5.7). That is exactly the change §8.2.7 item 4
   closes the §8 route to — and it is also, independently, a change `docs/45` §6.1 forbids this
   session from enacting at all. **It is therefore PROPOSED, to a different owner, in a document
   that must adopt it in its own dated act with this profile disclosure in front of it.** §8.2.7
   item 2's recommendation is thereby honoured in substance: the threshold-moving half of B2 gets a
   fresh, dated registration by its own owner; the coordinate-changing half, which moves no
   admissible set, goes in §8.
3. **`docs/47` O9 remains OPEN and is not decided here.** A reader may hold that any B2 work
   requires a fresh pre-registration of the whole of `docs/45`. §8.2.7 item 3's counter-argument —
   that a wholesale re-registration re-opens **every** threshold to a project that has seen the
   surface, which is strictly more dangerous — is carried unchanged and unresolved.
4. **§8.2.7 item 4's route rule is re-affirmed, not softened.** If any future session proposes to
   change §6.1's eight ADOPT conditions, §3.2's bar, §2.1's boxes **as sets of admissible model
   levels**, §3.4's fit set, §3.5's windows, or §2.5's budget or seeds, the §8 route is **closed**.
   **This amendment changes none of them**, which is why it is here.

### 8.5.12 Defects and disagreements in files this amendment does **not** own — REPORTED, NOT FIXED

1. **`docs/51` is internally inconsistent about the convention.** §6.3 **P1** states the principle
   of convention (ii) — *"The box `[2.0, 30.0]` and the stop 3.9 were registered at `f_LS = 1`. Any
   `f_LS != 1` **moves them**"* — while §6.2's arithmetic holds the box literal on the post-swap
   engine α (convention (i)). **Immaterial to `docs/51`'s verdict**, and in the safe direction:
   under (ii) §6.2's *"two of the three"* becomes **three of three**, strengthening its own
   conclusion that collapsing the bracket does not dissolve the block. Owed to `docs/51`'s owner.
2. **`docs/46` §6.2 A4's stops (α̂ ≥ 7.54 upper, ≤ 2.10 lower) are convention-(i) quantities.**
   Under (ii) the corresponding Branch-A stops would be different numbers. **MOOT, and therefore
   not owed as a correction:** Branch A is closed entirely — `Δ_shape` = 0.1299456916752905 > 0
   ⇒ **B1** ⇒ Branch B MANDATORY (`docs/46` §6.1, §6.3, §10 amendment 1) — and `docs/47` §5.4
   already records A4 as moot in the direction it was written for. `docs/46` is **FROZEN** and its
   §10 slot is not this pass's; **not touched**.
3. **`docs/47` §5.2's *"one corner of the registered parameter space clears both thresholds"* and
   §5.2's conclusion *"the LS decision is the dominant term in the C4 verdict"* do not survive the
   fix B2 asks for.** Both are convention-(i) statements; under the enacted convention no corner
   clears and the LS decision does not move the rail verdict (§8.5.8). **`docs/47`'s VERDICT is
   strengthened, not weakened** — the rail becomes certain rather than probable. Owed to
   `docs/47`'s owner, along with a note that its §5's three propositions should be re-ordered:
   **P1 is discharged by this amendment; P3 and Branch B / `Δ_shape` now carry the block.**
4. **§7.1's card cell now under-counts the amendments** — it reads *"Amendments | **THREE**, all
   dated 2026-08-12"*; there are **four**. §7 is outside this amendment's ownership (§8 only) and
   is **not edited**; the correction is owed to that section's owner.
5. **§1 item 4's Π = 5,164.42 does not reproduce exactly from §2.3's printed factors** —
   5164.401419084846 at `C_mult` 1.20427, 5164.412311062239 at 1.204272539864846; relative gaps
   3.5978706523513363e-06 and 1.4888289026620914e-06. Both constituents are correct at their
   printed precision; the residue is **printed rounding**, is disclosed rather than reconciled, and
   is **not** a materiality claim. §8.5.3 prints all three `k0` evaluations and registers the
   conversion as a **formula** precisely so that no session has to choose.
6. **`docs/46`:127 (§1.0) and `docs/51` §2.3's `ln(0.43194/0.25146) = 0.5410 = −ln 0.580685`
   identity** has now been independently measured not to hold by three separate passes
   (`docs/37` A3, `docs/35` §9.4.7 item 1, `docs/45` §8.3 item 5). **Not re-raised in detail here**;
   recorded only so a fourth pass does not spend time re-discovering it. Immaterial to every
   verdict, including this one.

### 8.5.13 What this amendment leaves OPEN — named, not numbered into another document's register

Offered to `docs/47`'s owner for numbering into its §7 register if wanted; **none is a finding.**

| | open question | what would settle it |
|---|---|---|
| **Q1** | Whether `docs/46` §6.2 A4, `docs/47` §5.2 and `docs/51` §6.2 should be restated in the enacted convention. | Their owners' amendments. **Not this pass's**, and A4 is moot anyway (§8.5.12 item 2). |
| **Q2** | **`f_LS(ref)` — the LS field α = 11.8 was fitted against — is NOT SETTLED and no band is offered.** It is the one input the Π form of `docs/35` §6.1 needs and does not have; §8.5.7's proposal supplies it only from `docs/35` §6.1's **own registered pairing**, not from a measurement. | `docs/47` **O4**'s second half and `docs/46` §1.0 residue 3, carried unchanged. Williams (1975)'s own LS treatment, obtained and read. |
| **Q3** | **`docs/47` O9** — whether the pre-fit profile requires a fresh pre-registration rather than a §8 amendment. | A governance decision by this document's owner. §8.5.11 gives a measured argument for the §8 route **for this amendment only** and decides nothing wider. |
| **Q4** | **The search GRID must be re-placed if and when `ls2d_column` switches** — to α ∈ [7.953396323950136, 119.30094485925204] on `buarque_2015_dg`, with the same 71 log points and the same ×1.0394444954338562 step. | Nothing: it is a consequence, registered in §8.5.4 so it is not discovered at run time. It is **not** a widening — it is the same Π box. |
| **Q5** | **`docs/47` O5** — the objective has never been re-profiled on a corrected LS **field**. | Re-running §5.2's profile on the adopted LS field, **after** C3.1's ACT 2, never before (§8.5.9). |

### 8.5.14 Disclosure for Amendment 4

- **Files written by this pass:** `docs/45_c4_preregistration.md` (**§8 only** — this section
  appended after §8.4; **§1–§7 and §8.1–§8.4 were not edited, not renumbered, and nothing was
  deleted**) and `docs/agents/journal_gate-reexpression.md`. **Nothing else in the repository.**
  `docs/00`, `docs/33`, `docs/35`, `docs/37`, `docs/42`, `docs/43`, `docs/46`, `docs/47`,
  `docs/48`, `docs/51`, `docs/52`, `docs/53` were **read and not edited**.
- **No body site is struck**, because no body number is superseded: the restatement is the
  identity at the registered configuration (§8.5.5). §2.1's `[2.0, 30.0]` and §6.1's α̂-against-3.9
  /35.4 remain readable and remain **correct as written**.
- **No frozen artifact was opened, read or written.** `sim_calibrated_v2/{h2e_drivers.npz,
  parameters_H2E.csv, q_gauge_H2E.npz, q_gauge_H2E.csv, report_H2E.json, metrics_fleet.csv}`,
  `data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv` and `urh_ls2d_variants.csv` were **not
  touched at all**.
- **No engine default was changed. No calibration, simulation, LS pass, fit or search was run. No
  `KGE_ln` was evaluated against §2.1's α box. No α̂ — provisional or otherwise — is quoted.** The
  5,482-evaluation budget and the DDS seeds 20260921–24 are untouched. `docs/47` §6.3's
  permitted / not-permitted list was read before anything was written and obeyed.
- **What this pass measured itself, all of it arithmetic on registered numbers** (`python3.10`;
  scripts and verbatim output in the journal §02): `k0` three ways and its 3.6e-06 spread; the Π
  box and rail band and their bitwise inversion back to α (3.4000000000000004, 28.6); the 71-point
  log-grid step in both coordinates (1.0394444954338562, identical); the Π box in engine-α units at
  three `f_LS` values; `docs/35` §6.1's five numbers in both readings; the four ÷11.8 ratios; the
  §8.2.4 profile converted to Π and its five shortfall factors; `exp(±Δ_shape)`; and the
  direction cross-checks against `docs/46` A4 (`30.0/3.9768 = 7.543753771876887` vs
  `30.0·f = 7.543946957518192`). **Every cross-check reproduces the published figure to every
  printed digit.** Every other number is carried from a named prior document and cited in place.
- **UNCITED quantities are named and pass or fail nothing:** the 0.05–0.30 SDR band and its implied
  `k ≈ 0.0020–0.0032 /km`; the ENSO-neutrality of CAL 2012–14; the `m'` KGE bias variant; and
  **`f_LS(ref)`, which is NOT SETTLED with no band offered** (Q2). **No plausibility band was
  invented, and no fourth band was created.**
- **The `docs/23` §13.2 yield embargo is in force.** No `t/km²/yr`, `t/ha/yr` or area-normalised
  yield appears; §8.5.8's loads are absolute (Mt/yr).
- **Nothing is backdated. No git command was run.** `C4.3-BLOCKED-UNTIL-LS-LANDS` is unchanged.
  **B2 is discharged. B1 is not. Branch B is mandatory. The pre-computed FAIL stands.**
