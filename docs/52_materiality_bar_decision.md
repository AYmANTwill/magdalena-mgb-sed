# 52 — `docs/46`'s materiality bar: **STRUCK, NOT RESCALED**

**Written 2026-08-11** by the `bar-judge` agent (process record:
`docs/agents/journal_bar-judge.md`). This document does **one** job: it decides item **(e)** of
`docs/51` §5.6 — the single non-mechanical item blocking the freeze of
`docs/46_ls_preregistration_DRAFT.md`. It decides it **on principle and before `Δ_shape` is
computed**, so the threshold cannot be reverse-engineered from its verdict.

**Scope.** It **recommends**; it does not enact. `docs/46` was **not edited** (only the agent
told to edit it may). `docs/47`, `docs/48`, `docs/49`, `docs/50`, `docs/51` were read as evidence
and **not edited**. No engine default moved, no fit was run, no LS pass was run, no frozen
artifact was opened for writing, no git command was run (§8).

---

> ## THE DECISION
>
> **1 — There is NO numeric materiality bar.** `0.1644 ln` is **struck**, and it is **not
> replaced by a number** — not by `0.4775`, not by `0.6936`, not by `0.3054`, not by a bootstrap
> half-width, and not by an arbitrary constant declared non-statistical. Every one of `docs/46`'s
> **fifteen** bar sites (five more than the enumeration in `docs/47`/`docs/48`/`docs/51` — §1.3)
> is re-grounded on a **threshold-free rule that already exists inside `docs/46`**: §3.3's
> *"`f_ero` decides; `f_area` can never override it"*, §4.2's four-item rule hierarchy, and
> §6.1's own derivation of what makes a change a level change. Where a number is owed, the
> **exact measured ratio is printed at full precision** and the clause text states what it
> licenses.
>
> **2 — This is not a judgement call relocated to a future session.** Every site's ground is
> fixed in advance and is either a **source reading with a grade**, an **exact discriminator**
> (`= 0`), or a **printed ratio**. A clause that could not name its ground in advance is
> **struck before the freeze**, not left to a later session's discretion.
>
> **3 — The measured fact that makes this a small decision, not a large one.** Every bar
> comparison `docs/46` has **already** made returns the **identical verdict for any bar in
> `(0.0321, 0.2983)` — a factor of 9.29** (§1.2, measured this pass). **The bar adjudicates
> nothing that has been measured.** Its only two live consumers were **(R10)** and the blinded
> **`Δ_shape`**. (R10) is settled by the citation (§3); `Δ_shape`'s site gets the exact
> discriminator its own derivation supplies (§4). After those two, the bar has **no remaining
> decision content at all**.
>
> **4 — (R10) is not a question for a statistical threshold.** The levers are decided as a set
> because they are **one formulation read whole** — eqs. 13/14/18 plus the p. 94 / p. 98 limiter,
> all four **CITED** (`docs/51` §1.2), the source read whole a **POINT** at ×0.25146
> (`docs/51` §2.3) — and `docs/46` §4.2 item 1 registers fidelity to *the transposed method*, not
> to a menu of levers. The arithmetic non-multiplicativity (**joint / product = ×1.34762**,
> reproduced here) is a **reported fact with a standing instruction**, not a gate. Even if the
> levers multiplied out exactly, they would still be adopted whole or not at all.
>
> **5 — Five conclusions must carry an explicit `BAR-DEPENDENT` label** (§5), because their
> verdict reverses under a different bar — including (R10)'s, which reverses on **all seven**
> admissible SE constructions, on a **2.4 % margin** in a quantity known to **±27 %**.

---

## 1 — What was measured this pass, before deciding

Nothing below is transcribed. Every number was recomputed in `python3.10` from the factors
published in `docs/47` §4.3, `docs/48` §2.4/§5.3 and `docs/51` §2.1–§3.

### 1.1 The (R10) statistic, and which construction produces it

| construction | product of single levers | joint | \|ln joint/product\| | joint/product |
|---|---:|---:|---:|---:|
| limiter × **eq. 14 step** `m` × W&S `S` | `0.362435 × 0.52204 × 1.694054` = **0.3205244** | 0.431944 | **0.2983374** | **×1.34762** |
| limiter × **cap** `m` × W&S `S` | `0.362435 × 0.517480 × 1.694054` = **0.3177247** | 0.431944 | 0.3071107 | ×1.35949 |

`docs/51` §5.5's **0.2983** is the **step** construction. Recorded because the two differ by
0.0088 and a later session that reproduces the cap row will get a different number for the same
clause.

### 1.2 The indifference window — the decisive measurement

Sorted, every quantity `docs/46`'s clauses actually compare to the bar, as measured to date:

| clause | statistic | \|ln\| |
|---|---|---:|
| (R4) H-M field clause — step vs cap | `f(V2b)` vs `f(V2a)` | **0.0088** |
| (R12) proxy vs exact, upper endpoint | `f_ero(V4)` vs `f_area(V4)` | **0.0248** *(0.0273 at the DG endpoint)* |
| H-L (§2.5) | `f(V5)` vs published 0.790 | **0.0258** |
| (R2) limiter proxy | `f_ero(V1)` 0.362435 vs area 0.351 | **0.0321** |
| **(R10) joint cell** | product vs joint | **0.2983** |

> **Every one of these verdicts is unchanged for any bar in `(0.0321, 0.2983)` — a factor of
> 9.29.** `0.1644` sits inside that window. **The bar decided none of them**, and it did not
> decide a single evidence grade either: all four levers reached **CITED** from source text
> (`docs/51` §1.2). *(Defect A's two ends, 0.0036 and 0.0010, are further inside still.)*

### 1.3 The bar has FIFTEEN consumers, not ten — new this pass

`docs/47`, `docs/48` §5.3 and `docs/51` §5.5 all enumerate *"ten occurrences:
`:138, :140-142, :189, :217, :240, :265, :490-491, :506, :538`"*. That is the list of lines
carrying the **literal number**. Grepping `docs/46` for `"materiality bar"` as well returns
**five further clause-level consumers that no document has recorded**:

| line | clause | use |
|---|---|---|
| **:163** | **(R1)** H-LIM reading | two admissible readings *"differ by more than the materiality bar"* |
| **:166** | **(R2)** H-LIM proxy | `f_ero(V1)` vs 0.351 |
| **:220** | **(R8)** H-S strata | strata agree with 1.714 *"to within the materiality bar"* |
| **:249** | **(R12)** joint-cell proxy | `f_ero(V4)` vs `f_area(V4)` |
| **:421** | **ADOPT-BAND** | its *trigger condition* — two readings differing by more than the bar |

> **Consequence for the amendment set: `docs/51` §5.6(e) must reach all fifteen sites.** Enacting
> only the ten enumerated ones freezes a document that **retires a bar in §2 and then invokes it
> by name five more times**, including in the **trigger of an entire §4.2 outcome** (ADOPT-BAND).

### 1.4 The three candidate replacement numbers, evaluated

| candidate | value(s) | why it fails |
|---|---|---|
| the corrected SE of the fleet-mean level | 0.3054 – 0.6936 over the seven `docs/48` §2.4 constructions | **wrong error term** (§2.1), **premise false** (§2.2), **flips (R10) on all seven** (§5), **non-composable** (§2.4) |
| the station-bootstrap half-width | 0.8500 (est a) / 1.2833 (est b) | same family, wider; at 1.2833 **all four single levers become immaterial** while their composition stays material (§2.4) |
| the within-fit-set residual sd | 1.2217 – 1.9618 | the one **type-correct** term for a *shape* clause — and it makes the shape test **vacuous for every admissible value** (§2.5) |

---

## 2 — Why no number can serve: five grounds, three of them measured here

### 2.1 Wrong error term — a paired contrast against an unpaired SE

Seven of the ten literal-number sites (`:189` R4, `:240` R10, `:265` H-L, `:490-491`/`:506`/`:538`
the branch, plus `:138`/`:140-142` defining them) apply the bar to `|ln f_A − ln f_B|` between
**two deterministic field computations on the same DEM, the same minibacias, the same stations and
the same days**. There is no sampling in either arm. By `docs/46` §6.1's own derivation, a uniform
LS level multiplies every station's flux by the same `f`, so both arms share their entire residual
vector: **the sampling variance of that paired difference is identically zero.**
`SE = sd/√n` is the error term of an **absolute, unpaired** level. Using it for a within-design
contrast is the textbook wrong-error-term error.

**And it is the same *shape* of category error one level down that `docs/48` retired.** `docs/48`
retired σ_r because an **observation-side** statistic was used for a **model-side** quantity. Here
a **sampling-side** statistic is used for a **specification-side** quantity. Rescaling the number
repairs the size and leaves the type.

*Grade: **DERIVED** from `docs/46` §6.1 + §8.1. No new measurement needed.*

### 2.2 The draft's premise is false, not merely its number

`docs/46`:140-145 justifies the bar as *"a difference in the LS level smaller than the standard
error of the only fit that will ever consume it cannot change any downstream statement."*

**The fit never consumes the LS level.** `docs/46` §8.1: the uniform scalars' design matrix has
**condition number = ∞**; only `Π = α·f_vol·f_K·f_LS·C_mult·P·FG` is identifiable. Swapping the LS
level leaves `Π̂`, the objective value, the residual vector and every residual statistic
**identical**, and moves the implied `α̂` by exactly `1/f`, noiselessly. §4.3 states the same thing
as a prohibition: *"a fit is structurally incapable of preferring one LS level over another."*

**Detectability of an LS level change is therefore exactly zero at every noise level, so no
standard error bounds it.** Rescaling `0.1644` to any corrected SE preserves the false premise.
A level difference's consequence is **bookkeeping** — which number is printed, what `α̂` must be
multiplied by to be quoted against a published α (§8.3) — and bookkeeping has a *reporting
precision*, not a *noise floor*.

*Grade: **CITED** — `docs/46` §8.1, §4.3.*

### 2.3 Measured — (R10) flips on **every** admissible construction, inside the threshold's own error

All seven of `docs/48` §2.4's constructions, recomputed:

| set / window / estimator | n | sd (ln) | **SE** | (R10) 0.2983 refutes? | width 0.5410 material? | 95 % interval on the SE |
|---|---:|---:|---:|:--:|:--:|---|
| CAL 8 / CAL / (b) — `docs/42` §9 primary | 8 | 1.9618 | **0.6936** | **yes** | no | [0.3303, 1.0569] |
| CAL 8 / CAL / (a) — `docs/45` §7.1 objective | 8 | 1.3506 | **0.4775** | **yes** | yes | [0.2274, 0.7276] ∋ 0.2983 |
| CAL 7 / (a), C1.2-compliant | 7 | 1.3539 | **0.5117** | **yes** | yes | [0.2222, 0.8013] ∋ 0.2983 |
| all with CAL-window data / (b) | 10 | 1.8930 | **0.5986** | **yes** | no | [0.3221, 0.8752] |
| all 18 / ENSO medians / (b) | 16 | 1.4175 | **0.3544** | **yes** | yes | [0.2276, 0.4812] ∋ 0.2983 |
| **all 18 / ENSO medians / (a) — smallest** | 16 | 1.2217 | **0.3054** | **yes** | yes | [0.1961, 0.4147] ∋ 0.2983 |
| CAL 8 / ENSO medians / (b) | 8 | 1.7159 | **0.6067** | **yes** | no | [0.2889, 0.9245] ∋ 0.2983 |

Three findings, all measured:

1. **The flip is unanimous, not an estimator-(b) artifact.** The smallest admissible SE is
   **0.3054**; `0.2983 < 0.3054`, so (R10) refutes under **every** honest rescaling.
2. **The margin is 2.4 % in a quantity known to ±27 %.** `sd(s)/s ≈ 1/√(2(n−1))` = **0.267** at
   n = 8 and **0.183** at n = 16, so each threshold carries the 95 % interval in the last column.
   **0.2983 lies inside that interval on 5 of the 7.** A threshold that must resolve 2.4 %
   cannot be built from an estimate of that precision.
3. **The bracket-width verdict is not even construction-stable:** 0.5410 is material on **4** of
   7 and immaterial on **3** — and immaterial at both bootstrap half-widths.

*Side confirmation of `docs/48` by an independent route: **0.1644 lies below the 95 % lower bound
of all seven constructions** (smallest 0.1961), so it is rejected as an SE by its own sampling
distribution, not only by point comparison.*

### 2.4 Measured — non-composability: any aggregate bar loses factors

From `docs/48` §5.3's own table, at the station-bootstrap half-width **1.2833**: the limiter
(1.0150), the `m` cap (0.6588), the `m` step (0.6500), `S` (0.5271) and the `L` form (0.5435) are
**every one of them immaterial** — yet the composition they belong to, the source-DG endpoint,
is **1.3805 = MATERIAL**. Five individually-immaterial specification choices compose to a factor
of **3.977**.

The same failure appears one bar down: at `docs/42` §9's registered primary SE **0.6936**, (R10)
refutes ⇒ `docs/46`'s own text then licenses deciding the levers one at a time ⇒ decided one at a
time, `S`, the `L` form and the `m` step are each immaterial.

**Any single aggregate threshold has this property.** `0.1644` escaped it only by being ~4× too
small — which is not a defence of `0.1644`, it is an accident.

*(Correcting the runner-up brief that raised this: its worked example mixed the `m` **cap** with
the `m` **step** and asserted the three levers compose to exactly 1.3805. They do not — the levers
are non-multiplicative, which is (R10)'s own content. The version above uses only rows measured on
the same construction and is the defensible form of the argument.)*

### 2.5 The one type-correct noise term is vacuous in the other direction

For a **shape** clause the residual vector genuinely moves, so an error term exists — but the
type-correct one is the **within-fit-set residual scatter** (1.2217 – 1.9618 ln), not the SE of
the mean (the SE of the mean is precisely the component a level absorption removes).

`docs/51` §5.4 **already publishes a bound** on the shape statistic: per-station erosion-weighted
LS ratios under the source formulation span 1.287×, so `Δ_shape ≤ ln 1.287 = **0.2523**`. That is
**0.21 of the smallest admissible residual sd**. So on the type-correct term **every admissible
value of `Δ_shape` is immaterial by construction** — the test cannot fail. `docs/48` §5.4 makes
the mirror-image point about G8/G11: **a guard that cannot fire is not a test.**

> **This is a for-all argument from an already-published bound. It is NOT an estimate of, a
> further bound on, or a prediction about `Δ_shape`.** Its conclusion is about the *power* of a
> comparison, and it is the same for every value the blinded quantity can take.

### 2.6 Candidates considered and rejected on principle, without reference to any value

- **the per-station LS-ratio dispersion** (`docs/47` §4.4, `sd(ln)` 0.0769 / 0.0868) — rejected
  because it is the *same quantity* `docs/46` §6.1's pre-test measures; using it as the bar makes
  §6.1 **circular**. This is exactly the defect `docs/48` §3.2 measured when it rejected route 1
  for G12.
- **an analyst-choice (multiverse) yardstick built on σ_r** — attractive because σ_r is an
  estimator *disagreement*, not sampling noise, and the fleet level measurably moves
  `2.5772 − 1.9240 = 0.6532 ln` between the two registered estimators (`docs/48` §3.3), close to
  pair-σ 0.658. Rejected because a **systematic common-mode displacement does not shrink with
  `n`**, so the `/√8` is wrong for that framing too (type-correct value ≈ 0.65, not 0.164) — and
  at ≈ 0.65 it lands squarely in the non-composability regime of §2.4.
- **the deliverable-tolerance route** (set the bar where the ENSO contrast moves by a stated
  amount) — refuted by measurement from `docs/47` §4.4's four pairs: elasticity
  `|d ln contrast| / |d ln f_LS|` = **0.00726 – 0.01154 ln/ln**, so a 1 % tolerance on the
  contrast implies a bar of **0.866 – 1.378 ln** (×2.38 – ×3.97) — the bar would swallow the whole
  bracket. And no tolerance on the contrast is cited anywhere: `docs/34` §2 registers the observed
  contrast as a **range** and tests agreement by CI overlap, so the tolerance would itself be
  uncited (`docs/40`; `docs/46` §4.3). **Structural reason, not bad luck:** the deliverable is a
  *ratio of two runs sharing the same uniform level factor*, so `f_LS` cancels identically and
  survives only through β-nonlinearity and transport. The deliverable is the wrong instrument in
  principle.
- **an α-gate route** (derive the bar from the narrowest registered α verdict cell,
  `[3.40, 3.9]` = 0.1372 ln) — **forbidden by `docs/46` §4.3 bullet 4**, which bars *any α band*
  as evidence in any outcome, and circular besides, since the box is LS-conditional
  (`docs/47` P1). Its numerical proximity to 0.1644 is a reason for suspicion, not comfort.

---

## 3 — (R10): decided by the **citation**, not by a statistic

`docs/46`:239-244 makes (R10) a refutation clause: if the naive product of the three single-lever
factors comes within the bar of the joint, *"the levers are separable after all, and every 'they
interact, so decide them as a set' statement … needs correcting."*

**That clause conflates two different propositions.**

| proposition | what decides it | status |
|---|---|---|
| *the lever factors are **arithmetically** separable* | measurement | **NO** — joint/product = **×1.34762** (§1.1). A naive product understates the joint by **35 %** |
| *the levers may be **methodologically** decided one at a time* | the source and `docs/46` §4.2 | **NO** — and this does not depend on the arithmetic |

The second is settled by the citation and always was. Eqs. 13, 14 and 18 plus the p. 94 / p. 98
limiter are **one formulation**, on two printed pages of one thesis, all four now **CITED**
(`docs/51` §1.2); read whole they are a **POINT** at ×0.25146 (`docs/51` §2.3). `docs/46` §4.2
item 1 registers *"fidelity to **the transposed method**"* — the method, not a menu — and item 2
requires **each deviation** to carry its own written source justification. `docs/47` §5.3 names
lever-picking as the specific post-hoc hazard: *"`f_LS` … can be tuned by choosing among four
levers, each of which has a defensible citation somewhere."*

> ### DECIDED
> **(R10) is retired as a refutation clause.** It is replaced by two statements, neither of which
> reads a threshold:
>
> 1. **A measured fact with a standing instruction.** `f(V4) / [f(V1)·f(V2b)·f(V3)]` = **×1.34762**
>    (**×1.35949** with the `m` cap). *Standing instruction: **never quote a product of
>    single-lever factors as the joint factor**, in any document, table or notebook.*
> 2. **An adoption rule, carried from §4.2 and not new here.** The formulation is **adopted whole
>    or not adopted**; any single-lever deviation requires its own §4.2 item 2 written source
>    justification, dated, before the resulting basin total is computed.
>
> **Even if the levers had multiplied out exactly, the answer would be the same.** Arithmetic
> separability is not methodological separability, and only the second was ever the question.

---

## 4 — The `Δ_shape` site: the exact discriminator, not a threshold

`docs/46` §6.1 derives — correctly — that a **uniform** LS factor leaves the objective surface
identical up to a relabelling of the α axis, so the fit is recoverable by rescaling `α̂`; and that
a change moving stations *relative to each other* changes the residual vector, so it must be
re-run. **That derivation supplies its own discriminator, and the discriminator is exact:**

> ### DECIDED — replaces `:490-491`, `:506`, `:538`
>
> **Branch A is available only if the LS swap is a pure level change for the fit set, i.e.
> `Δ_shape = 0`** (to the engine's numerical tolerance — a *reproduction* tolerance in the sense
> of `docs/49` gate 2 and `report_h2e.py`'s 1e-8, **not** a materiality bar). **Any
> `Δ_shape > 0` ⇒ Branch B is mandatory (B1).**
>
> **`Δ_shape` remains MANDATORY to compute and to record** before C3.1 reports
> (`docs/47` O6, §6.3), and is **reported at full precision as a diagnostic**, with the sentence:
> *"the fit is recoverable by rescaling `α̂` if and only if `Δ_shape = 0` exactly; the measured
> value is X, and the re-run is owed."*

**Four reasons this is the right disposition, none of which touches `Δ_shape`'s value:**

1. **It is the document's own derivation, not an import.** §6.1 already says *"the fit is not
   recoverable by rescaling — it must be re-run"* for any relative movement. The threshold was a
   softening of a statement that is exact.
2. **It can only tighten, never loosen.** `docs/51` §5.4 accepted §6 as *strictly more restrictive
   than `docs/45` §6.1*; this is more restrictive still, so no frozen registration is relaxed.
   *(The freezing session must accept the tightening explicitly — `docs/51` §5.4's "accept it,
   unchanged" is thereby amended in the restrictive direction, and only in that direction.)*
3. **It cannot be tuned, now or later.** A future session that needs the discriminator cannot
   choose a threshold after seeing the number, because there is no threshold to choose. This
   closes the one real hole in a "no bar" decision.
4. **It costs nothing that is live.** `docs/51` §5.4 and `docs/47` record that **B2 makes Branch B
   mandatory regardless of `Δ_shape`**, so the branch is already over-determined. What the site
   was protecting is protected twice over.

It also removes the incentive structure that made the bar dangerous here: under the drafted rule,
a wider bar **opens** Branch A and lets C4.3 start; under this rule no choice of number opens
anything. §6.2 **A6** — *"no rescaling in place of a re-run"* — is the same principle already
registered, and this makes §6.1 consistent with it.

---

## 5 — Conclusions that MUST carry an explicit `BAR-DEPENDENT` label

A reader must be able to see which way each of these would go under a different bar. Labels are
owed wherever the conclusion appears, not only in `docs/46`.

| # | conclusion | at 0.1644 | under the seven admissible SEs (0.3054 – 0.6936) | at the bootstrap half-widths (0.8500 / 1.2833) | label |
|---|---|---|---|---|---|
| **1** | **(R10) "the levers interact, so decide them as a set"** — *as a statistical finding* | survives (0.2983 > bar) | **REVERSES on all seven** (smallest SE 0.3054; margin **2.4 %**; 0.2983 inside the SE's own 95 % interval on **5 of 7**) | reverses | **BAR-DEPENDENT — verdict reverses.** *Superseded: §3 decides it by citation, and that route is bar-independent* |
| **2** | **the bracket WIDTH 0.5410 ln is material** | material | **material on 4 of 7, immaterial on 3** | immaterial on both | **BAR-DEPENDENT *and* CONSTRUCTION-DEPENDENT.** *Superseded: `docs/51` §2.3 — the span is the `L`-form lever (×1.7177) between a POINT and a documented hybrid, not an uncertainty interval* |
| **3** | **the single-lever MATERIAL verdicts** — `S` 0.5271, `L` form 0.5435, `m` step 0.6500, `m` cap 0.6588, and the refuted ×0.790 ratio 0.2357 | all material | ×0.790's 0.2357 goes immaterial at **0.4775**; the other four at **0.6936** | all immaterial | **BAR-DEPENDENT.** This is `docs/48` §5.3's *"three of the levers `docs/46` exists to adjudicate become immaterial"* |
| **4** | **`f_LS` upper endpoint 0.8395 is a material displacement from 1.0** | material | material on all three SE bars | **immaterial at both** | **BAR-DEPENDENT at the widest constructions.** *Only the **DG endpoint 1.3805** is material on every construction ever proposed — that one is **NOT** bar-dependent* |
| **5** | **the `Δ_shape` Branch A/B verdict** | — | — | — | **BAR-DEPENDENT BY CONSTRUCTION** while a threshold exists. *Superseded by §4's exact discriminator; and the branch is over-determined by B2 regardless* |

**Explicitly NOT bar-dependent** — stated so nothing is over-read. Immaterial at 0.1644 **and** at
every construction up to 1.2833: **(R4)** 0.0088 · **(R12)** 0.0248 / 0.0273 · **H-L** 0.0258 ·
**(R2)** 0.0321 · **Defect A** 0.0036 (upper) and 0.0010 (lower).
Also not bar-dependent, and not statistical at all: **all four evidence grades (CITED)**, decided
by source text (`docs/51` §1.2); the **source-read-whole POINT** at ×0.25146; and **`docs/47`'s
`C4.3-BLOCKED-UNTIL-LS-LANDS` verdict**, whose three propositions (P1 unit, P2 rail measured at
`f_LS = 1`, P3 post-hoc) are each width-independent (`docs/51` §6.3).

**Separately owed and NOT fixed by any choice of bar:** `docs/46` §6.2 **A5**'s *"minimum
detectable coefficient given the registered noise floor σ_r = 0.465"* is **σ_r-dependent**, not
bar-dependent, and must move with `docs/48` — but `docs/48` §6.2 records that three passes have
produced three different values for that class of quantity (**O8 open**), so **no corrected number
is supplied here either.**

---

## 6 — Site-by-site disposition: the fifteen clauses, and what each is decided by

Recommended clause grounds for the `docs/46` owner to enact. **No clause is left to a later
session's discretion; each ground is fixed here, in advance, and is a source reading, an exact
discriminator, or a printed ratio.**

| site | clause | decided by, from now on |
|---|---|---|
| **:135-145** | the bar and its derivation | **STRUCK.** Replaced by a short §2.0 *"How difference is adjudicated in this document"* stating the four grounds below and the sentence: *"this document contains no statistical materiality threshold; the reasons are `docs/52`."* |
| **:163** | **(R1)** H-LIM reading | **Source text.** A second admissible reading refutes the reading clause **irrespective of the factor it produces**; both factors are reported; the outcome is **ADOPT-BAND** (§4.2), which carries both. *A reading disagreement is never "inside the bar".* |
| **:166** | **(R2)** limiter proxy | **§3.3, already registered:** *"`f_ero` decides; `f_area` is reported beside it, always, and can never override it."* R2 becomes a **reported diagnostic** — print `f_ero`, `f_area` and their exact ratio (**×1.0326**); the proxy may not be quoted anywhere the exact value exists. |
| **:189** | **(R4)** H-M field clause | **Retired as a refutation clause.** H-M's field content is a **sign** prediction, and the sign test is **(R5)** — exact and threshold-free. The magnitude is **reported**: `f(V2b)/f(V2a)` = **×1.0088**. The **reading** clause (eq. 14 step ≠ `min(m,0.5)` cap) is independent, is **CITED**, and stands. **⚠ This changes a label already written:** `docs/51` §3 records *"(R4) FIRES ⇒ H-M's field clause REFUTED"*; under this disposition the field clause is **confirmed on its sign** and its magnitude is ×1.0088 — while the ×0.502 relabelling that (R4) was standing in for is owed **anyway**, under `docs/51` §5.6(b), because the label is wrong regardless of size. |
| **:216 / :220** | **(R7)/(R8)** *"`S` acts as a scalar"* | **Exact discriminator + report.** A lever is a pure level lever **iff its per-cell factor is constant**; any nonzero dispersion is shape content. Report (i) the per-cell `S_WS78/S_MB86` range over the basin's slope range (§3.4: ≈ **0.975 – 3.81**, non-monotone) and (ii) the quantity that actually enters the fit — the **per-station erosion-weighted factor dispersion**, `sd(ln)`, beside `docs/47` §4.4's measured 0.0769 (all 18) / 0.0868 (CAL 13) for the joint. Restate as measurements — *"the `S` ratio field spans ≈ ×3.9 over the basin's slope range; `S` is not a scalar"* — not as threshold tests. |
| **:240 / :249** | **(R10)** joint cell, **(R12)** joint proxy | **§3** for (R10) — citation, plus the printed ×1.34762 and the standing instruction. **§3.3** for (R12), as for (R2): reported diagnostic, exact ratios **×1.02484** (upper) / **×1.02771** (DG), against `docs/47` R7's separately measured proxy bias 1.0251 / 1.0278. |
| **:265** | **H-L** | **The code reading and the exact factorisation**, both threshold-free: 0.790 = **0.852262** (`L` form) × **0.926925** (`S` swap), measured on the wrong column (`ls2d`, not `ls2d_hs`). H-L is refuted **iff 0.790 is shown to isolate the `L` form** — it is not. The 0.0258 basin-scale agreement is **reported and is not the test**. **And the mandatory re-derivation is re-hung unconditionally** (this discharges `docs/51` §5.6(c)'s logic fix): *the published bracket and every statement derived from it are re-derived because they are superseded by a measurement (`docs/51` §2.1) — not because a hypothesis survived.* |
| **:421** | **ADOPT-BAND** trigger | **Two admissible readings ⇒ ADOPT-BAND, period**, whatever the gap; both factors carried through C4, C5 and every load table. Carrying a band is never the unsafe direction; collapsing one is, and §4.2 already forbids collapsing for convenience. *(Currently not triggered on any lever: all four are CITED with a single admissible reading — `docs/51` §1.2.)* |
| **:490-491, :506, :538** | `Δ_shape` branch, Branch A precondition, **B1** | **§4** — the exact discriminator `Δ_shape = 0`, with `Δ_shape` still mandatory, blinded until computed, and reported at full precision. |

**What keeps its numeric tolerance, unchanged and untouched by this decision:** reproduction and
agreement gates — `docs/49` gate 2, `report_h2e.py`'s `F = 0.25931` to **1e-8**, the basin-erosion
gate at **299.5387088405831 Mt/yr**, the 3,266-day count. Those are **agreement tolerances on
quantities that should be identical**, not materiality bars, and nothing here touches them.

---

## 7 — What this decision must NOT be claimed to be

The draft's failure was a **claim of provenance the number did not have** — a decision threshold
dressed as a measured statistic. The same failure in a new costume is the thing to guard against,
so the prohibitions are explicit.

1. **NOT "the bar is zero", and NOT "everything is material".** Deleting a comparison is not
   setting it to a limit. Nothing may be declared material on the ground that it exceeds zero.
2. **NOT a licence to import a corrected number silently.** No downstream document may quote
   *"bar = 0"*, *"bar = 0.6936"*, *"bar = 0.4775"*, *"bar = 0.3054"*, *"bar = 0.465"*,
   *"bar = 0.1644"*, or **reconstruct a number from this decision**. `docs/48` declined to propose
   a value on purpose; this document declines to supply one on the record.
3. **The `Δ_shape = 0` discriminator is NOT a materiality bar of zero.** It is a **structural**
   condition — *is this change a pure level change?* — used only to decide whether a fit is
   recoverable by rescaling. It never decides whether a difference *matters*.
4. **NOT a finding that "the LS levers are immaterial", that "LS does not matter", or that "the
   LS question is unresolvable".** The opposite: all four levers are **CITED**, the source read
   whole is a **POINT** at ×0.25146, and the endpoints' displacement from 1.0 (**0.8395**,
   **1.3805**) is stated at full precision — the DG endpoint material on **every** construction
   anyone has proposed.
5. **NOT a weakening of `docs/47`.** `C4.3-BLOCKED-UNTIL-LS-LANDS` is untouched; its three
   propositions are bar-independent (`docs/51` §6.3). Retiring the bar removes an instrument, not
   a verdict.
6. **NOT "each session now decides for itself".** Every site's ground is fixed in §6, in advance.
   A clause that cannot name its ground in advance is **struck before the freeze**, not carried.
7. **NOT applicable to anything outside `docs/46`'s bar sites.** Untouched and unaffected:
   `docs/48` §3.3's station-bootstrap **reporting** band on Π; σ_r's valid use as an
   estimator-disagreement statistic (`docs/48` §5.4); G1.1 / G8 / G11's **firing** thresholds;
   G12's 0.644 ln fragility threshold; and every reproduction tolerance in §6's last paragraph.
8. **NOT a statement about `Δ_shape`.** Nothing here estimates it, bounds it further, or predicts
   it. The only `Δ_shape` quantity used is the bound `docs/51` §5.4 already publishes, used in a
   for-all argument about the *power* of a comparison (§2.5).
9. **NOT an enactment.** `docs/46` is unedited. Everything in §6 is a recommendation to its owner,
   and this document adopts no variant, switches no default, and is not `docs/47`'s B1 unblocking
   event (`docs/51` §5.3, §7 item 4 — that is `docs/37` §A3).

---

## 8 — Honest weaknesses, stated so a reviewer can aim

**(a) A fixed number has an anti-gaming virtue that a principled absence does not.** A
pre-registration exists to make verdicts un-gameable before the numbers are seen. "No bar" is
harder to falsify than "0.1644", and a reviewer is entitled to say I removed the one instrument
that could have contradicted a future session. My defence is §6: the replacement is not
*judgement*, it is a set of grounds fixed in advance — source text with a grade, exact
discriminators (`= 0`), and printed ratios — most of which were **already in `docs/46`** (§3.3,
§4.2) and were simply not being used. **But the defence is only as good as the enactment.** If the
freezing session enacts §6 loosely — struck bar, vague clauses — the result is worse than the
falsified number, because it looks decided and is not.

**(b) The `Δ_shape` site is the weakest joint, and I know why.** It is the one place where a noise
comparison is type-correct, and I am recommending it stop carrying a threshold while I am blinded
to the value. My reason never touches the value (§2.5 is a for-all; §4's four reasons are
structural), and "= 0" is the one choice that cannot be tuned to a side of the number — but the
*shape* of the move is the shape the blinding exists to prevent, and it should be read
adversarially. The specific check a reviewer should run: **does `Δ_shape = 0` ever open Branch A
where `Δ_shape ≤ 0.1644` would have closed it?** No — it is strictly tighter in every case. That
asymmetry is the whole defence, and it is checkable without knowing the value.

**(c) Fifteen separately-argued clauses is more document, not less.** The single rule was easier
to freeze and easier to read. If the freezing session is time-boxed, the tempting synthesis is to
keep one explicitly-non-statistical number declared as a decision threshold with no distributional
claim. **I judge that worse**, for a measured reason rather than an aesthetic one: §1.2 shows such
a number would adjudicate nothing over a factor-9.3 range, §2.3 shows the one live comparison it
would touch turns on a 2.4 % margin, and §2.4 shows any single aggregate threshold loses factors
under composition. A number nobody can state the meaning of is the failure `docs/51` §5.5 is
already about. But this is a judgement of honesty over convenience, and it is the judgement a
reviewer should test.

**(d) One label already written changes.** §6's disposition of (R4) reverses `docs/51` §3's
*"H-M's field clause REFUTED"* into *"confirmed on its sign, magnitude ×1.0088"*. That is a
consequence of retiring a threshold that would have refuted a clause on a 0.9 % difference, and it
is flagged rather than buried — but it is a change to a statement in a document I am forbidden to
edit, and it is owed to `docs/51`'s owner as a note, not enacted here.

---

## 9 — Disclosure

- **What this pass measured itself:** the (R10) statistic under both constructions (§1.1); the
  indifference window `(0.0321, 0.2983)` (§1.2); the seven SE constructions, their firing states
  for (R10) and for the bracket width, and their own 95 % sampling intervals via
  `sd(s)/s = 1/√(2(n−1))` (§2.3); the composition check at the bootstrap half-width (§2.4); the
  ENSO-contrast elasticity from `docs/47` §4.4's four pairs (§2.6); the ero/area ratios ×1.0326 /
  ×1.0251 / ×1.0277 and `f(V2b)/f(V2a)` = ×1.0088 (§6); and the **fifteen-site grep** that found
  five unrecorded consumers of the bar (§1.3). All arithmetic, in `python3.10`, from factors
  published in `docs/47` §4.3, `docs/48` §2.4/§5.3 and `docs/51` §2.1–§3. **Nothing transcribed.**
- **What it did not do:** no engine run, no fit, no α̂, no LS pass, no `Δ_shape` computation, no
  variant adopted, no default moved. `data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv` and
  everything in `sim_calibrated_v2/` were **not opened for writing**. `ls2d_column`,
  `cp_revision`, the unit conventions and the H2E parameters are untouched. **No git command was
  run.** Files written: this one and `docs/agents/journal_bar-judge.md`.
- **`docs/46` was NOT edited**, and `docs/47`, `docs/48`, `docs/49`, `docs/50`, `docs/51` were
  read as evidence and not edited. §6 is a set of recommendations to `docs/46`'s owner.
- **`Δ_shape` is unmeasured and unseen by this pass.** This decision is recorded **before** it is
  computed, which is the only condition under which it is worth anything.
- **No plausibility band was invented, and no replacement number is offered.** Where a value could
  not be grounded — a replacement bar, A5's minimum detectable coefficient (O8), α = 11.8's
  like-for-likeness — this document says **NOT SETTLED** and stops.
- **The `docs/23` §13.2 yield embargo is in force.** No t/km²/yr appears here.

### 9.1 Cross-references

| document | relation |
|---|---|
| `docs/51_ls_freeze_decision.md` | **the assignment** — §5.6 item (e), the one non-mechanical item. §5.5 is the finding this decision answers. `docs/51` §3's (R4) label is affected (§8d); `docs/51` §5.4's "accept §6 unchanged" is amended in the restrictive direction only (§4). |
| `docs/48_pi_band_revision.md` | **the measurement that falsified the derivation.** §5.3's P4 (*"what `docs/46`'s materiality bar should be"*) is **closed by this document**: the answer is *no bar*, per-site grounds. §3.3's Π reporting band, §5.4's firing thresholds and G12's 0.644 are **untouched**. |
| `docs/47_c4_entry_verdict.md` | D2 is the origin; §4.3's bracket, §4.4's absorption factor and dispersion, §5.3's post-hoc argument are consumed as evidence. **The BLOCKED verdict is untouched and is not bar-dependent.** |
| `docs/46_ls_preregistration_DRAFT.md` | the document amended. Fifteen sites (§1.3, §6). **Not edited by this pass.** |
| `docs/40_sdr_evidence.md` | the standing rule — *an uncited band cannot pass or fail a gate*. A threshold whose stated derivation is falsified is in that category the moment the falsification is on the record; **striking it is the direction that rule points.** |
| `docs/49`, `docs/50` | Defect A / Defect B resolutions; their reproduction gates are the model for what a **numeric tolerance** legitimately is (§6, last paragraph). |
