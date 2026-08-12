# 53 — The `Δ_shape` pre-test: **COMPUTED**, and the answer is Branch B

**Written 2026-08-11** by the `delta-shape` agent (process record:
`docs/agents/journal_delta-shape.md`). This document does **one** job: it computes `docs/46`
§6.1's `Δ_shape` pre-test — `docs/47` open item **O6**, `docs/51` §7 blocking item **5** — on the
registered configuration, reports it at full precision, judges it against the bar that
`docs/52` decided **before this run started and blind to its result**, and states the resulting
branch.

**Scope.** No default moved. No variant adopted. No fit. No git command. `docs/46`, `docs/47`,
`docs/48`, `docs/49`, `docs/50`, `docs/51` and `docs/52` were read and **not** edited;
`data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv`, `urh_ls2d_variants.csv` and everything in
`sim_calibrated_v2/` are SHA-256 identical before and after. Every new file this run wrote is in
the session scratchpad.

---

> ## THE ANSWER
>
> ### `Δ_shape` = **0.1299456916752905**
>
> Registered reading — variant **V4**, weights normalised over the **18 usable** SSC stations,
> maximum taken over the **CAL 8**. Argmax: **`24037390` CAPITANEJO** (`|ln| = 0.1299456917`).
> **No CAL station is invariant**: the smallest of the eight is `26127010` EL ALAMBRADO AUT at
> **0.0179854753**.
>
> **VERDICT — `Δ_shape` > 0 ⇒ BRANCH B IS MANDATORY (`docs/46` §6.1 as amended, §6.3 **B1**).**
> In the sentence §6.1 requires verbatim: *"the fit is recoverable by rescaling `α̂` if and only
> if `Δ_shape` = 0 exactly; the measured value is **0.1299456916752905**, and the re-run is
> owed."*
>
> **It is not near zero and the margin is not arguable.** A null control — a *uniform* LS factor,
> the exact case Branch A exists for — returns `Δ_shape` = **2.2204460492503136e-16**, one machine
> epsilon. The measured value is **5.9 × 10^14** times that, and **1.3 × 10^7** times
> `report_h2e.py`'s 1e-8 reproduction gate, which `docs/52` §4 names as the tolerance meant.
>
> **The under-specification is real but does not touch the verdict.** §6.1's definition admits
> **three** readings that the text does not settle (§4). All thirty measured combinations of
> variant × normaliser × max-set lie in **[0.0159907, 0.1638779]**; the twenty-four that compose
> an admissible V4 with an admissible normaliser lie in **[0.1282524, 0.1638779]**, and the twelve
> of those that take the maximum over the CAL 8 as §6.1 requires lie in
> **[0.1282524, 0.1451808]**. Every one is > 0 by fourteen orders of magnitude. **The branch is
> the same under every reading.**
>
> **And it must be said plainly, because it is the whole reason the bar was decided blind:
> under the STRUCK 0.1644 bar this measurement would have returned the OPPOSITE verdict.** Every
> V4-family reading is ≤ 0.1644 — the largest, 0.1638779, by a margin of **0.0005221** (0.3 %).
> The struck bar would have said *"Branch A is available"*; the exact discriminator says
> *"Branch B is mandatory"*. `docs/52` §4 predicted its own asymmetry correctly (*"`Δ_shape` = 0
> never opens Branch A where `Δ_shape ≤ 0.1644` would have closed it"*) — this run is the case
> that makes the asymmetry bite, and it bites on a 0.3 % margin.

---

## 1 — The definition, quoted, and the configuration it was computed on

`docs/46` §6.1, verbatim at `:915-920` of the current file (unchanged by today's amendment set,
which rewrote the *branch table* below it and not the statistic):

> Compute, for the 18 usable SSC stations, the per-station upstream **erosion weight**
> `w_s = E_upstream(s) / Σ_s E_upstream(s)` under **V0** and under **V4**, at adopted defaults,
> with no fit. Then
> ```
> Δ_shape = max over the 8 CAL stations of | ln( w_s(V4) / w_s(V0) ) |
> ```

Nothing here was invented. Each term was resolved to a registered object:

| term | resolved to | source |
|---|---|---|
| **the 18 usable SSC stations** | the CAL 8 + the 5 lost tributary + the 5 EVAL, named | `docs/45` §3.4 |
| **the 8 CAL stations** | `22017030`, `26137110`, `24027030`, `21197010`, `23127010`, `26127010`, `22017010`, `24037390` | `docs/45` §3.4, table |
| **`E_upstream(s)`** | decade (2009-01-01…2018-12-31) modelled **gross hillslope erosion** summed over every minibacia upstream of the station's mapped minibacia, inclusive | `docs/46` §3.3's `E_i`; station→minibacia from `data/processed/_c1_geom.csv`; topology from `model_inputs_v2/topology.npz` |
| **adopted defaults, no fit** | `SedParams()` = `volume_convention='williams_m3'`, `k_unit_system='us_customary'`, `cp_revision='cited_central_2026_08_11'`, α = 11.8, β = 0.56, `f_peak` = 1.0, on the frozen `sim_calibrated_v2/h2e_drivers.npz` | `docs/46` §3.3 |
| **V0** | `urh_ls2d_variants.csv:V0_ours_2026_08` | `docs/46` §3.1 |
| **V4** | `urh_ls2d_variants.csv:V4_buarque_2015` | `docs/46` §3.1 — **and see §4.1, this is the live ambiguity** |
| **aggregation** | per-cell LS → (minibacia, URH) by area-weighted mean; MUSLE is linear in LS per cell, so a unit's decade erosion redistributes exactly in proportion to LS·(cell area) | `docs/46` §3.2; `scripts/c3/ls_erosion_weights.py`'s derivation |

**One term the definition leaves implicit, and it resolves cleanly.** §6.1 speaks of *erosion*
weights, while its own derivation two paragraphs down argues about *"every station's simulated
flux"*. Those are different quantities in general — a station's flux is its upstream erosion
after transport. **At the registered configuration they are the same object**: `docs/45` §2.1
fixes the deposition coefficient `k_dep` **at zero** (not fitted, reported as a bound), and
`src/mgb_transport.py` at `k_dep = 0`, `tau_channel_days = 0` asserts *"SDR = 1.0 between
hillslope and station"* with a mass residual that is *"exactly 0.0 for every reach on every day"*.
So delivered decade flux at `s` **equals** `E_upstream(s)` exactly, and the erosion reading and
the flux reading coincide. *(They would not coincide under any non-zero `k_dep`. That is a
condition on the registered configuration, not a general property, and it is recorded here so a
later session that un-fixes `k_dep` knows this pre-test must be recomputed.)*

---

## 2 — The harness, and the six reproduction gates it passed before any new number was read

`scratchpad/delta_shape_full.py` (+ `v4dg_units.py` for §4.1's second variant). It does not
re-implement the model: the erosion field is `src/mgb_sediment.simulate_sediment` on the frozen
H2E drivers opened read-only; the LS variants are the committed
`data/processed/urh_ls2d_variants.csv`; the additional `V4_dg` column is a fresh 90 m cell pass
importing `scripts/c3/ls2d.py` and `scripts/c3/ls2d_defect_b.py:block` unchanged. **A harness
that cannot reproduce known numbers is not trusted with unknown ones**, so:

| # | gate | target | measured | |
|---|---|---|---|---|
| **G1** | basin gross erosion, adopted defaults | 299.5387 Mt/yr (`docs/37` A1.3) | **299.5387088405831** (+8.8e-6) | **PASS** |
| **G2** | `f_ero` V1 / V2a / V3 / V4 | 0.3624 / 0.5175 / 1.6941 / 0.43194 (`docs/47` §4.3) | 0.36243463 / 0.51748003 / 1.69405384 / **0.43194418** | **PASS** |
| **G3** | model upstream area, all 18 stations | `_c1_geom.csv` / `docs/42` §4.1 | 18 of 18 to < 0.02 km² | **PASS** |
| **G4** | per-station erosion-weighted LS-ratio extremes | 0.3687 CARRASPOSO → 0.4745 BANANERA, span 1.287× (`docs/47` §4.4) | 0.368748 → 0.474504, span **1.286798×** | **PASS** |
| **G5** | `sd(ln f_s)` | 0.0769 (all 18) / 0.0868 (CAL 13) (`docs/47` §4.4) | **0.076918** / **0.086777** | **PASS** |
| **G6** | `f_area` and `f_ero` of the source read whole | 0.2446790094097074 area (`ls2d_defect_b.json`) · 0.25146 ero (`docs/51` §2.1) | **0.24467900940970733** · **0.2514648985839397** | **PASS** |
| **NULL** | uniform (pure level) LS factor ⇒ `Δ_shape` = 0 | 0 | **2.2204460492503136e-16** (f = 1: exactly 0.0) | **PASS** |

Two further internal checks: the fresh cell pass reproduces the committed
`urh_ls2d_variants.csv`'s per-unit `V4/V0` ratio to a **max relative difference of 8.0e-8**
(median 1.2e-8 — that is the CSV's own float formatting, not a method difference), and its
independently-aggregated `V4` erosion factor agrees with the committed column's to **9.1e-12**.

> **Incidental, and it discharges an open item.** `docs/46` §3.1 as amended today records that the
> lower bracket end's `f_ero` *"rests on **one** engine re-run; the second reproduction is owed,
> `docs/51` §7 item 7"*. G6 is that second reproduction, by a different aggregation route:
> **`f_ero(V4_dg) = 0.2514648985839397`**. `docs/51` §7 item 7 is discharged.

---

## 3 — The result, at full precision

### 3.1 The registered reading — V4, normaliser = the 18 usable, max over the CAL 8

`Σ_18 E_upstream(V0)` = **1.3373824516 × 10⁹ t** over the decade; pooled factor over that set
`f̄` = **0.432271**. (The `Δ_shape` statistic is scale-free: since `ln(w_s(V4)/w_s(V0))
= ln f_s − ln f̄`, the normaliser enters only as the common centre subtracted from every station.)

| code | name | set | `E_up(V0)` t | `f_s` = `E_up(V4)/E_up(V0)` | **`\|ln(w_s(V4)/w_s(V0))\|`** |
|---|---|---|---:|---:|---:|
| `24037390` | CAPITANEJO | CAL 8 | 6.005512e+07 | 0.379596 | **0.1299456917** ← Δ_shape |
| `23127010` | BORBUR - AUT | CAL 8 | 3.574707e+07 | 0.385461 | 0.1146116846 |
| `26137110` | BANANERA LA 6-909 | CAL 8 | 9.290266e+05 | 0.474504 | 0.0932166557 |
| `21197010` | EL PROFUNDO | CAL 8 | 6.003736e+06 | 0.401363 | 0.0741865822 |
| `22017010` | BOCAS | CAL 8 | 5.077766e+07 | 0.464715 | 0.0723720512 |
| `24027030` | NEMIZAQUE | CAL 8 | 1.276267e+07 | 0.409995 | 0.0529087921 |
| `22017030` | BOCAS | CAL 8 | 9.007728e+05 | 0.444433 | 0.0277454190 |
| `26127010` | EL ALAMBRADO AUT | CAL 8 | 5.536924e+06 | 0.440116 | 0.0179854753 |

**Δ_shape = 0.1299456916752905.** The CAL 8's own `f_s` spread is **×1.250023** (0.379596
CAPITANEJO → 0.474504 BANANERA).

For the record, the other ten stations under the same normaliser — reported, not part of the
statistic (`docs/46` §6.1 takes the maximum over the CAL 8 only):

| code | name | set | `\|ln w ratio\|` |
|---|---|---|---:|
| `21147030` | CARRASPOSO - AUT | trib-lost | **0.1589405011** |
| `22057090` | BOCATOMA TRIANGULO | trib-lost | 0.0846324387 |
| `26017020` | JULUMITO | EVAL | 0.0773663839 |
| `26167060` | PAILA LA | trib-lost | 0.0674510792 |
| `26107130` | MATEGUADUA | trib-lost | 0.0614006214 |
| `26017060` | PUENTE ARAGÓN - AUT | EVAL | 0.0324199744 |
| `26207080` | BOLOMBOLO - AUT | EVAL | 0.0080388244 |
| `23087210` | CANTERAS - AUT | trib-lost | 0.0070242081 |
| `26167070` | IRRA - AUT | EVAL | 0.0058333667 |
| `21237020` | ARRANCAPLUMAS - AUT | EVAL | 0.0017493214 |

The largest single displacement in the whole set, `21147030` CARRASPOSO at **0.1589405011**, is
**not a CAL station** — it is one of the five tributary stations `docs/45` §3.4 names as lost
(zero SSC before 2015). Under §6.1 as written it does not enter the maximum. It is reported
because it is the station `docs/47` §4.4 and `docs/51` §5.4 both quote, and because a reader who
knows only those two documents would expect it to be the answer.

### 3.2 What the prior bounds got right, and what they got wrong

`docs/51` §5.4 (repeated in the amended `docs/46` §6.1) bounded the statistic without computing
it: *"`Δ_shape` ≤ ln 1.287 = 0.2523; normalising the all-18 extremes on the basin joint factor
0.43194 gives ≈ 0.154. It can land on either side of 0.1644 and must be computed, not inferred."*

| statement | status |
|---|---|
| the ceiling `Δ_shape ≤ 0.2523` | **holds** — measured max over all 18 is 0.1589405011, and over the CAL 8, 0.1299456917 |
| the plausible value **≈ 0.154** | **it was an estimate of the wrong statistic.** It approximates the all-18 maximum (measured **0.1589405011**, so the estimate was 3.1 % low on *that*) — but §6.1's statistic maximises over the **CAL 8**, and the measured value there is **0.1299456917**, which the estimate overshoots by **0.0290** = 22 % |
| *"it must be computed, not inferred"* | **vindicated.** Inference would have put the answer 0.0290 from the truth and only 0.0105 from the then-live 0.1644 bar — inside the estimate's own error |

---

## 4 — Where the definition is under-specified, and the value under each reading

**This is itself a finding.** §6.1 is one sentence and an equation, and it does not settle three
choices. None of them changes the branch, but a frozen pre-registration whose statistic has three
admissible values should say so on its own face, so they are enumerated here with the measurement
under each rather than silently resolved.

### 4.1 (U1) Which object is **V4** — and this one is live in the amended document

§6.1 says *"under V0 and under **V4**"*. §3.1 as amended today names **V4** = `buarque_2015`
= V1 + V2b + V3 with **our** `L`, and labels it in the same row *"a documented **hybrid**, not the
source read whole"*; and it adds a **new** row, **V4_dg** = `buarque_2015_dg`, *"the source
formulation **READ WHOLE**"* (`f_ero` 0.25146), which did not exist when §6.1 was drafted. So the
name in §6.1 and the object C3.1 would actually adopt (`docs/51` §2.3: *"the source formulation
read whole is a POINT at ×0.25146"*) are now **different variants**. Both are admissible readings
of §6.1: the **literal** one (the registered name `V4`) and the **purposive** one (the swap whose
consequences the gate exists to anticipate).

Measured under both, and under the cap compositions as well, so the `docs/51` §5.6(b) V4/V4′
label question cannot move it either:

| variant | what it is | `f_ero` | **`Δ_shape`** (norm 18, max CAL 8) | argmax |
|---|---|---:|---:|---|
| **V4** `buarque_2015` | the registered name in §6.1 — hybrid, our `L` | 0.43194418 | **0.1299456917** | CAPITANEJO |
| **V4_dg** `buarque_2015_dg` | the source read whole (eq. 13 `L`) | 0.25146490 | **0.1361987744** | CAPITANEJO |
| **V4′** `buarque_2015_cap` | cap composition | 0.43038143 | 0.1283331586 | CAPITANEJO |
| **V4′_dg** cap + eq. 13 `L` | cap composition, DG `L` | 0.25085872 | 0.1350852579 | CAPITANEJO |
| *(context)* **V5** `L_dg96_fd` | the `L`-form lever alone on V0 | 0.76675960 | *0.0170741517* | BOCAS `22017010` |

The two bracket endpoints' shape fingerprints correlate **r = 0.998040** over the 18 stations —
independently reproducing `docs/47` §4.4's *"the two bracket endpoints correlate r = 0.998"*. **The
choice of endpoint is a level choice, not a shape choice**, which is why U1 cannot flip the
branch: it moves `Δ_shape` by 0.0063, from one un-arguably-nonzero number to another.

### 4.2 (U2) Which set the normaliser `Σ_s` runs over

The sentence defines `w_s` *"for the 18 usable SSC stations"* and writes `Σ_s`, so the **literal**
reading is: normalise over the same 18. But §6.1's branch table and `docs/52` §4 both frame the
question as whether the swap is a pure level change **"for the fit set"**, and a weight vector
whose centre is set by ten stations that the objective never sees is not the fit set's weight
vector. `docs/47` §4.4 additionally reports its LS-shape statistics on a **"CAL 13"** grouping
(the C1-usable tributary set), which §6.1 does not name at all. Three admissible centres:

| normaliser | pooled `f̄` | **`Δ_shape`** (V4, max over CAL 8) | argmax |
|---|---:|---:|---|
| **the 18 usable** (literal) | 0.432271 | **0.1299456917** | CAPITANEJO |
| the CAL 13 | 0.431540 | 0.1282524457 | CAPITANEJO |
| the CAL 8 (the fit set) | 0.411627 | 0.1421522905 | BANANERA LA 6-909 |

Under V4_dg the same three are 0.1361987744 / 0.1330434626 / 0.1450950443.

**A structural criticism that goes with the literal reading**, recorded because it will matter if
this statistic is ever reused: the 18 upstream sets are **nested**, so `Σ_s E_upstream(s)` double
counts. It totals 1.337e9 t against a basin decade erosion of 2.995e9 t, and **42 % of it is one
station** — `21237020` ARRANCAPLUMAS, an **EVAL** station whose catchment contains most of the
others. The literal normaliser therefore centres the fit set's weights on a station the fit never
uses. `Δ_shape` is scale-free so this is a shift, not a scaling — but it is why the literal and
fit-set readings differ by 0.012 and swap the argmax.

### 4.3 (U3) Which set the maximum runs over — **not** ambiguous, but adjacent usage is

§6.1 says *"max over the **8** CAL stations"*, and `docs/45` §3.4 registers exactly 8 and names
them. There is no ambiguity in §6.1. It is flagged only because `docs/47` §4.4 uses **"CAL 13"**
for a different object under the same word, so a reader moving between the two documents can pick
up the wrong set. The maximum over all 18 is **0.1589405011** (CARRASPOSO); over the CAL 8 it is
**0.1299456917**.

### 4.4 The full grid

Thirty readings were measured (5 variants × 3 normalisers × 2 max-sets). Ignoring V5, which is a
single lever and not a candidate for adoption, the **twelve** readings that pair an admissible V4
with an admissible normaliser and take the maximum over the CAL 8 — the combination §6.1 requires
— span **0.1282524457 … 0.1451808423**; relaxing U3 to the all-18 maximum extends the V4-family
range to **0.1282524457 … 0.1638778967**. **Every value in the grid is > 0 by at least fourteen
orders of magnitude relative to the null control.**

| variant \ normaliser | 18 usable | CAL 13 | CAL 8 |
|---|---:|---:|---:|
| **V4** | **0.1299456917** | 0.1282524457 | 0.1421522905 |
| **V4_dg** | 0.1361987744 | 0.1330434626 | 0.1450950443 |
| **V4′** | 0.1283331586 | 0.1283040863 | 0.1422903807 |
| **V4′_dg** | 0.1350852579 | 0.1330715446 | 0.1451808423 |
| *(V5, context)* | *0.0170741517* | *0.0159907232* | *0.0191521145* |

*(maximum over the CAL 8, as §6.1 requires; the registered reading is the bold cell)*

---

## 5 — The judgement, against the bar that was decided blind

`docs/52` struck `docs/46`'s 0.1644 materiality bar and replaced this site's threshold with an
exact discriminator, on principle, **before this measurement existed** (`docs/52` §7:
*"`Δ_shape` is unmeasured and unseen by this pass"*). The amended `docs/46` §6.1 `:924-927` now
reads:

| condition | branch |
|---|---|
| `Δ_shape` = 0 — to the engine's *reproduction* tolerance (`docs/49` gate 2, `report_h2e.py`'s 1e-8), **not** a materiality bar | pure **level** change for the fit set → **Branch A available** |
| any `Δ_shape` > 0 | the swap moves the fit set's stations **relative to each other** → **shape** change → **Branch B MANDATORY (B1)** |

| | |
|---|---|
| measured `Δ_shape` | **0.1299456916752905** |
| the discriminator | 0, at reproduction tolerance |
| the numerical zero, measured on this exact statistic (null control) | 2.2204460492503136e-16 |
| named reproduction tolerance (`report_h2e.py`) | 1e-8 |
| ratio to the numerical zero | **5.85 × 10^14** |
| ratio to the named tolerance | **1.30 × 10^7** |
| smallest CAL-station displacement (i.e. is *any* station invariant?) | 0.0179854753 — **no** |
| smallest value anywhere in the admissible grid | 0.1282524457 |

> ### **VERDICT: `Δ_shape` > 0. BRANCH B IS MANDATORY (`docs/46` §6.3 B1).**
>
> The LS swap is **not** a level change for the fit set. `α̂` may not be rescaled in place of a
> re-run (§6.2 **A6**), and C4.3 may not start under Branch A.

**This does not change what was already going to happen, and that is by design.** `docs/47` and
`docs/51` §5.4 both record that **B2** — a final verdict is unreachable because ADOPT is
unreachable under **A3** — makes Branch B mandatory *regardless* of `Δ_shape`. The branch was
over-determined before this run. What this run supplies is the **record**: B1 is now
independently satisfied, on a measurement, and `docs/47` **O6** closes.

### 5.1 The one thing this measurement says that nothing else did

**Under the struck bar the answer would have been the opposite one.** Every V4-family reading is
**below** 0.1644 — the largest of the thirty, 0.1638778967 (V4_dg, normaliser 18, max over all
18), by **0.0005221033**, a margin of **0.3 %**. Had `docs/46` been frozen as drafted, this
measurement would have returned *"the LS swap is, for the fit set, a level change → Branch A is
available"*, and Branch A is the branch that lets C4.3 start.

Three consequences worth stating in exactly this order:

1. **The blind decision earned its keep.** `docs/52` §7(b) named this site *"the weakest joint,
   and I know why… the one place where a noise-floor threshold could have been argued for"*, and
   named the check a reviewer should run: *"does `Δ_shape` = 0 ever open Branch A where
   `Δ_shape ≤ 0.1644` would have closed it? No — it is strictly tighter in every case."* The
   converse case — the bar opening what the discriminator closes — was the live one, and it is
   the case that occurred.
2. **The margin is smaller than the bar's own uncertainty, by a lot.** `docs/48` §2.4 and
   `docs/52` §3 measure the seven admissible standard-error constructions at 0.3054 – 0.6936, and
   note each carries a ±27 % sampling interval at n = 8. The 0.3 % gap between 0.1638779 and
   0.1644 is not resolvable by any of them. A verdict that turned on it would have been a verdict
   determined by which of seven equally-admissible estimators someone happened to write down.
3. **It is not a retrospective argument for the decision.** `docs/52`'s grounds are §4's four,
   none of which touches the value. This section adds one fact that was unavailable then, and it
   is offered as a *check that the decision behaved as advertised*, not as its justification.

---

## 6 — What this document does NOT establish

Stated as prohibitions, in this project's usual form, because a computed number attracts uses it
cannot bear.

1. **It is not an adoption of V4 or of V4_dg.** No default moved. `ls2d_column` is untouched.
   C3.1's formulation decision is not made here and this document may not be cited as making it.
2. **It is not a measure of how *much* the fit will move.** `Δ_shape` is a maximum of a log
   weight displacement, computed with **no fit**. It says the residual vector changes; it says
   nothing about `F_report`, about `α̂`, or about whether any gate passes. That is `docs/47`
   **O5**, and O5 explicitly may only be run *after* C3.1 lands.
3. **It does not weaken `docs/47`'s BLOCKED verdict, and it does not by itself carry it.**
   `docs/47` §5's three propositions are independent of this statistic.
4. **It is not evidence about detectability.** `docs/47` §4.4 measures the LS shape signal as
   **3.1× below** the power of `docs/42` G4.1 to see it, and this run reproduces the statistics
   that finding rests on (G5). *"Large enough to break the rescaling identity"* and *"large enough
   for a regression to detect"* are different thresholds, and this measurement clears only the
   first. A reader must not read `Δ_shape` = 0.13 as *"the LS shape is now detectable"*.
5. **It is conditional on `k_dep` = 0** (§1). Any later session that fits or imposes a sink must
   recompute it, because the erosion reading and the flux reading then part company.
6. **It is one reading of the erosion field, not a bracket on it.** The field is the frozen H2E
   drivers at adopted defaults; the `docs/43` §5 caveat set travels with it unchanged.

---

## 7 — Incidental, flagged not fixed

Two small things this run measured that belong to other owners. Neither affects anything above.

1. **`f_area(V4)` is quoted inconsistently across today's documents.** `ls2d_variants_summary.json`
   and `ls2d_defect_b.json` both give **0.42136300143291305**, and the amended `docs/46` §3.1
   quotes the level behind it (16.775413430326214) to 17 digits — but the same row's `f_area`
   cell, and `docs/51` §2.2's proxy-bias arithmetic, use **0.42147514**. The difference is 2.7e-4
   relative. It moves `docs/51` §2.2's R7 consistency check from 1.024839 to **1.025112** against
   R7's separately measured 1.0251 — i.e. the on-disk value makes that check *better*, not worse.
   Owner: whoever holds `docs/46` §3.1 and `docs/51` §2.2. **Not corrected here** — this run may
   not edit either file.
2. **`docs/47` §4.4's "CAL 13"** is the C1-usable tributary set, not `docs/45` §3.4's registered
   **CAL 8**. Both are called "CAL" in live documents. This run reproduces the CAL-13 statistic
   (`sd(ln f_s)` = 0.086777 vs the published 0.0868) and confirms the two sets are different
   objects; §4.3 records the risk of confusing them.

---

## 8 — Reproduction

| | |
|---|---|
| harness | `scratchpad/delta_shape_full.py` (statistic) · `scratchpad/v4dg_units.py` (the `V4_dg` per-unit column) |
| inputs, all read-only | `sim_calibrated_v2/h2e_drivers.npz` · `data/processed/` geometry · `urh_ls2d_variants.csv` · `model_inputs_v2/topology.npz` · `_c1_geom.csv` · `cop30_dem.tif` + `minibacias.tif` (cell pass) |
| outputs | `scratchpad/delta_shape_full.json`, `scratchpad/urh_ls2d_v4dg.csv` — **scratchpad only** |
| cell pass | 30,235,916 cells at native 90 m, 65 s; whole run, both scripts, ≈ 12 min |
| protected files, SHA-256 before/after | `urh_ls2d.csv` · `minibacia_ls2d.csv` · `urh_ls2d_variants.csv` — **UNCHANGED** |
| engine defaults touched | **none** (`ls2d_column`, `cp_revision`, unit conventions, H2E parameters all untouched) |

The statistic is one line given the gated inputs:
`Δ_shape = max_{s ∈ CAL8} | ln f_s − ln f̄ |`, where `f_s = E_up(s,V4)/E_up(s,V0)` and `f̄` is the
`E_up(V0)`-weighted mean of `f_s` over the normaliser set. The scale-free form is why the
normaliser is a centre and not a scale (§4.2).

---

## 9 — What this hands to the freezing session

| | |
|---|---|
| `docs/47` **O6** — *"`docs/46` §6.1's `Δ_shape` pre-test has not been run"* | **CLOSED.** Value 0.1299456916752905; Branch B. |
| `docs/51` §7 blocking item **5** — *"run it before item 4 reports, so it cannot be read backwards"* | **DISCHARGED**, and the ordering held: `docs/52` decided the bar blind, on principle, and this run measured afterwards. |
| `docs/51` §7 item **7** — the lower endpoint's `f_ero` second reproduction | **DISCHARGED** incidentally (§2 G6): `f_ero(V4_dg)` = 0.2514648985839397. |
| `docs/46` §6.1's required sentence | *"the fit is recoverable by rescaling `α̂` if and only if `Δ_shape` = 0 exactly; the measured value is **0.1299456916752905**, and the re-run is owed."* |
| the under-specification (§4) | **an amendment the freezing session may wish to make**: §6.1 does not fix which object `V4` is now that §3.1 carries both a hybrid `V4` and a `V4_dg`, nor which set `Σ_s` runs over. It changes no verdict here, and it will change one the next time this statistic is used. |
| `docs/47` **O5** | still open, still may only be run after C3.1 lands. This document does not touch it. |
