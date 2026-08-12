# 46 — Resolving the LS **level**: pre-registration **DRAFT**

> # ⚠ THIS IS A DRAFT. IT IS NOT IN FORCE.
>
> **Status: DRAFT, 2026-08-11, written by the `ls-prereg` agent**
> (process record: `docs/agents/journal_ls-prereg.md`).
>
> **Nothing in this file is frozen, registered, adopted, or binding on anyone.** It
> authorises no measurement, licenses no change to any default, and may not be cited as a
> registration by any session. It exists so that the orchestrator and the user can decide
> whether to freeze it. Until a freezing session adds the registration card in §9 with a
> date and a name, every threshold below is a **proposal**.
>
> **If it is frozen**, §1–§8 become frozen on that date and **§10 becomes the amendment
> slot** — the `docs/33` / `docs/35` / `docs/42` / `docs/45` pattern. A session that then
> believes a rule here is wrong **journals the objection and follows the rule anyway**.
>
> **It does not supersede `docs/35` §9.3**, which is a frozen pre-registration of the same
> comparison. This document is *subordinate* to it: where the two disagree, **`docs/35`
> wins** and this file is the bug. What this draft adds is what §9.3 does not contain —
> per-lever refutable hypotheses, an evidence-grade decision rule, the C4.3 ordering gate,
> a pre-commitment on the negative result, and the non-identifiability declaration.

---

## 0 — Why this document exists, and what it inherits

The C3.1 **LS-formulation** decision is the largest single unmade decision in Phase C and it
is named as unmade in four live documents:

| document | what it says about LS |
|---|---|
| `docs/35` §9.3 | pre-registers the comparison: the **source formulation is the registered default outcome**; a deviation needs its own written source justification; a deviation requires the α band rescaled by the measured level ratio; ties break toward the **lower** LS |
| `docs/37` §4 candidate 0 | the levers, measured, "the largest term in this list, and it points the WRONG WAY" |
| `docs/37` A2.2 / `docs/43` §2.1 | the LS **level** is reclassified into Π (C4's calibration target); the LS **shape** is **STILL A DEFECT**, owner **C3.1** — and clause 2 of C3's closure conjunction **alone forbids closure** because of it |
| `docs/42` **G4** | shape is testable (G4.1), **level is not** (G4.2); the level is **UNVALIDATED** and must be printed that way; C4 may not move `ls2d_aggregation` / `ls2d_resolution` |

`docs/45` (C4.2, frozen) registers the fit that will consume whatever LS is in force, fixes
`f_LS = 1.000` in its parameter card, and states in §7.2 that it does **not** resolve C3.1.

**C4.3 — the search itself — has not started** (`progress_map.html`: *"C4.3, the search
itself, has not started"*; there is no `scripts/c4/`, no `data/processed/c4/` and no
`c4_grid.csv` on disk — the recent commits deliver C4.1 transport, the C4.2 freeze and
notebook 19, and stop there). So the
ordering question in §6 is live rather than retrospective, which is the only condition under
which a pre-registration of it is worth anything.

---

## 1 — The ordering disclosure: what is ALREADY measured, and therefore cannot be a hypothesis

**This document is written after the lever factors were measured.** Pretending otherwise
would be exactly the failure this project's pre-registration discipline exists to prevent, so
the known numbers are listed first and are explicitly **out of scope as hypotheses**.

Measured 2026-08-11 by `docs/agents/journal_decide-ls-resolution.md` §3b, on all
**30,235,916** basin cells at 90 m, with a harness that reproduces our own `ls2d_hs`
area-weighted mean **39.812** bitwise. Quoted since in `docs/35` §9.3.1, `docs/37` §4
candidate 0, `docs/43` §1.4, and `src/nbgen/make_nb18.py` / `make_nb19.py`:

| variant (one lever swapped, others held at ours) | area-wtd mean | Andean >1000 m | median | × ours |
|---|---|---|---|---|
| **ours** — `ls2d_hs`: upslope area ≤ 1 km², continuous McCool-89 `m`, `(sinθ/0.0896)^1.3` | **39.812** | 65.199 | 12.486 | 1.000 |
| `m` hard-capped at 0.5 | 20.005 | 31.820 | 9.911 | **0.502** |
| `S` = Wischmeier & Smith (1978) | 68.234 | 114.202 | 15.072 | **1.714** |
| slope length ≤ 1 pixel (Buarque p. 94) | 13.985 | 22.308 | 7.511 | **0.351** |
| **all three together** | **16.775** | 27.109 | **7.262** | **0.421** |

Also already known: the levers **do not multiply out** (0.502 × 1.714 × 0.351 = 0.302 ≠
0.421); a further ×0.790 for "the literal Desmet–Govers finite-difference `L`" gives the
bracket **×0.333 – ×0.421**, i.e. our LS is **2.37× – 3.00×** the level α = 11.8 is paired
with; and the consequent α reference for **our** LS is ≈ **3.9 – 5.0**, band ≈ **2.0 – 9.9**,
hard stop ≈ **11.8 – 14.9** (`docs/37` §4 candidate 0).

> **Therefore no hypothesis in §2 may "predict" any number in this section.** The
> hypotheses below are about quantities that are **not** measured today, and each names
> which one.

### 1.1 Two defects in the existing evidence, found by this draft and measurable

Both were found by reading the code and the source description, and both are stated with the
arithmetic that supports them. **Neither is acted on here** — they are what §2 and §3 are
built to settle.

**Defect A — the ×0.502 row is a *cap*, and Buarque's eq. 14 is a *step function*. They are
different objects.**
`journal_decide-ls-resolution` labels that row *"+ m hard-capped at 0.5 (his eq. 14)"*, and
its own §1a records eq. 14 as the step function `m` = 0.2 (`Sf` < 1 %), 0.3 (1–3 %), 0.4
(3–5 %), **0.5** (`Sf` ≥ 5 %). `min(m_continuous, 0.5)` equals that step function **only
where the continuous `m` already exceeds each step**, which our own `slope_exponent_m()`
(`scripts/c3/ls2d.py:273`) puts at tan θ ≈ 0.09:

| tan θ | slope % | our continuous `m` | `min(m, 0.5)` (what was measured) | eq. 14 step |
|---|---|---|---|---|
| 0.005 | 0.5 | 0.0847 | 0.0847 | **0.20** |
| 0.010 | 1.0 | 0.1494 | 0.1494 | **0.30** |
| 0.020 | 2.0 | 0.2441 | 0.2441 | **0.30** |
| 0.030 | 3.0 | 0.3110 | 0.3110 | **0.40** |
| 0.050 | 5.0 | 0.4009 | 0.4009 | **0.50** |
| 0.090 | 9.0 | 0.5012 | 0.5000 | 0.50 |
| 0.158 (basin median) | 15.8 | 0.5845 | 0.5000 | 0.50 |
| 0.500 | 50.0 | 0.7003 | 0.5000 | 0.50 |

At the basin-median `a_unit_hs` of 185.2 m (measured, same journal §2), the length term
`(m+1)(a_unit/22.13)^m` under eq. 14 is **×1.41 / ×1.18 / ×1.32** that of the cap at
tan θ = 0.005 / 0.02 / 0.05, and **×1.000** at tan θ ≥ 0.09. Reproduce:
`python3.10 -c "..."` with `m_cont` and the step, as recorded in
`docs/agents/journal_ls-prereg.md`.

**Consequence, stated as a direction and not as a result:** eq. 14 is **less reducing** than
the cap on every cell below ~9 % slope, so the joint **×0.421** is a plausible *over*-statement
of how far the source formulation sits below ours — i.e. the true gap may be **smaller than
2.37×**. The size of that correction at basin scale is **not measured** and is H-M's job.

**Defect B — the ×0.790 "literal Desmet–Govers `L`" ratio is confounded with an `S` swap.**
`scripts/c3/ls2d.py:289` builds the variants; `ls3` (the `ls2d_dg96` column) is
`l_dg × s_factor_mccool(...)`, while the primary `ls1` uses `(sinθ/0.0896)^1.3`. So the
0.790 measured in `journal_c31-ls2d.md` §S4 is
`[L_dg / L_continuous] × [S_McCool-87 / S_Moore&Burch-86]` — **two levers, not one** — and
the second factor is strongly slope-dependent (§3.4 table: 3.58 at tan θ 0.005 → 0.744 at
tan θ 1.5). It was also measured on the **uncapped** `ls2d` column, not on `ls2d_hs`, which
is the column the engine reads (`src/mgb_sediment.py:864`, `ls2d_column="ls2d_hs"`).
**Neither transfer is verified.** The lower end of the published bracket (×0.333, ⇒ "3.00×")
therefore rests on an unisolated lever applied to a different column. H-L (§2.5) is the test.

---

## 2 — HYPOTHESES

Four hypotheses: one per lever, plus a joint cell. Each is stated so a measurement can refute
it, with the refuting statistic named and bounded, and each names the **grade** at stake
(§4.1). Each has a **reading clause** (what the source says — refutable by document evidence)
and a **field clause** (what the swap does to our field — refutable by recomputation).

**The materiality bar, fixed once and used by every clause below:** two factors are
"different" if
```
| ln f_A  −  ln f_B |  >  0.1644          (= ±38 % at 95 %, the 0.724×–1.380× band)
```
**0.1644 ln is not invented here.** It is the registered standard error of the fleet-mean
level on the achievable fit set — `docs/45` §2.2 / §6.2 item 2, measured by `docs/43` §3.2
lens 3 (σ_r 0.465 ln over n = 8). The justification for reusing it is a derivation, not a
preference: **a difference in the LS level smaller than the standard error of the only fit
that will ever consume it cannot change any downstream statement**, and one larger than it
can. It is symmetric in log space for the same reason `docs/33` §3.2's peak term is.

### 2.1 H-LIM — the slope-length limiter (the lever measured at ×0.351)

> **Reading clause.** Buarque (2015) p. 94 — *"Na determinação do fator comprimento de 'L',
> seu valor máximo foi limitado ao **tamanho do pixel do MDE**"* — read together with p. 121
> — *"os valores de comprimento (L) […] limitado pela resolução de 500 m"* — means **the
> slope length is capped at one DEM pixel**, and that is the only reading consistent with
> both sentences.
>
> **Field clause.** Recomputed at 90 m on the engine's own column with **only** this lever
> swapped, the limiter is the **dominant** lever, and the erosion-weighted factor it produces
> agrees with the already-published area-weighted proxy 0.351.

**Refuted if any of:**
- **(R1)** a second admissible reading of pp. 94 / 121 is established from the source text,
  from Buarque's equations 13/15, or from another primary MGB-SED document (Fagundes 2018;
  the MGB-SED code, if obtained), and the two readings give factors that differ by more than
  the materiality bar. *(A reading disagreement inside the bar is recorded and does not
  refute.)*
- **(R2)** the **erosion-weighted** factor `f_ero(V1)` (§3.3) differs from the area-weighted
  0.351 by more than the materiality bar — which would refute the *proxy*, not the reading,
  and would invalidate every ×0.421-based load arithmetic published to date (`docs/35`
  §9.3.3's own precision note anticipates this and asks for the exact re-run).
- **(R3)** some other single lever produces a larger |ln f| than the limiter on the exact
  re-run. *(This is a genuine possibility given Defect A: eq. 14 may move `m`'s factor toward
  1, but it cannot move the limiter's.)*

**Grade at stake:** the limiter reaches **CITED** only if (R1) fails with a verbatim,
page-numbered quote and a single admissible reading. Otherwise **ASSUMED**.

### 2.2 H-M — the `m` exponent (the lever measured at ×0.502)

> **Reading clause.** Buarque's eq. 14 is the **step function** 0.2 / 0.3 / 0.4 / 0.5 on
> slope classes < 1 % / 1–3 % / 3–5 % / ≥ 5 %, with `Sf` in **slope percent** — not a cap on
> a continuous `m`.
>
> **Field clause (the refutable prediction, and it contradicts the published number).**
> Implementing eq. 14 verbatim (`V2b`) gives a **different** basin factor from the cap
> (`V2a`, the published 0.502), and specifically **`f(V2b) > f(V2a)`**, because eq. 14
> assigns a *higher* `m` than our continuous form on every cell below ~9 % slope (§1.1
> Defect A).

**Refuted if any of:**
- **(R4)** `| ln f(V2b) − ln f(V2a) | ≤ 0.1644` — the two are the same object at basin scale
  after all, and the published 0.502 stands as eq. 14's factor.
- **(R5)** `f(V2b) < f(V2a)` on the basin area-weighted mean — the predicted **sign** is
  wrong. *(Sign is the load-bearing content here; the magnitude is not pre-registered because
  it depends on the basin's slope distribution below 9 %, which is not measured per-lever.)*
- **(R6)** `Sf` in eq. 14 is established from p. 46–48 to be slope in **degrees** or in
  **m/m**, not percent, in which case the step boundaries move and the whole clause is
  recomputed and this hypothesis is **withdrawn, not adjusted**.

**Grade at stake:** `m` reaches **CITED** only with eq. 14 transcribed verbatim, its `Sf`
units verified against the source text, and the step boundaries reproduced. The **cap** —
`min(m, 0.5)` — may **never** be graded CITED: it is nobody's published formulation.

### 2.3 H-S — the `S` slope factor (the lever measured at ×1.714)

> **Reading clause.** Buarque eq. 18 is Wischmeier & Smith (1978)
> `S = 65.41 sin²θ + 4.56 sinθ + 0.065`; ours is Moore & Burch (1986) `(sinθ/0.0896)^1.3`.
> Both are published; the question is which one belongs in *this* transposition, and the
> registered default answer is the source's (`docs/35` §9.3.2 item 1).
>
> **Field clause.** The `S` lever is **not a level change**: the per-cell ratio
> `S_WS78 / S_MB86` is a strongly varying, **non-monotone** function of slope, so the
> published ×1.714 is a basin-weighted summary of a per-cell factor that spans roughly
> **0.97 – 3.8** over the basin's slope range (§3.4).

**Refuted if any of:**
- **(R7)** the per-cell ratio is measured, on our own slope field, to lie inside a factor
  interval narrower than the materiality bar in **both** directions (i.e. `S` acts as a
  scalar to within ±38 %) — in which case `S` is a pure level lever and joins Π with no shape
  content.
- **(R8)** the stratified factors (lowland < 200 m / 200–1000 m / Andean > 1000 m, §3.3)
  agree with the basin factor 1.714 to within the materiality bar in all three strata —
  same conclusion as (R7), reached on the strata the erosion actually lives in.
- **(R9)** `n = 1.3` in our own form is established from Moore & Burch (1986) or Mitasova
  et al. (1996) to be inadmissible for this terrain, or `scripts/c3/ls2d.py`'s stated
  justification (module docstring, "rill-dominated overland flow") is contradicted by a
  cited source. *(This is a reading test on **our** side, deliberately symmetric with R1.)*

**Grade at stake:** whichever `S` is adopted reaches **CITED** (both candidates are published
and page-citable). The *choice between them* is graded by rule §4.2, not by evidence about
`S` itself.

### 2.4 H-JOINT — the joint cell (the source formulation, measured at ×0.421)

> The three levers must be decided **as a set**, because they interact: the naive product
> 0.302 is not the joint 0.421. The joint cell `V4 = buarque_2015` (limiter + **eq. 14 step**
> + W&S 78) is the registered-default outcome of `docs/35` §9.3.2 item 1, and its exact
> erosion-weighted re-run — not the area-weighted proxy — is what C4 and C5 would consume.

**Refuted if any of:**
- **(R10)** the naive product of the three single-lever factors comes within the materiality
  bar of the joint factor (`| ln(f1·f2·f3) − ln f_joint | ≤ 0.1644`) — the levers are
  separable after all, and every "they interact, so decide them as a set" statement in
  `docs/35` §9.3.1, `docs/37` §4, `docs/43` §1.4 and notebooks 18/19 needs correcting.
  *(Today's numbers say 0.302 vs 0.421 ⇒ |ln| = 0.332, twice the bar — so this is a real,
  losable prediction on the exact re-run, not a formality.)*
- **(R11)** the **exact** basin load under `V4` differs from `299.5387 × f_ero(V4)` — i.e.
  the linearity assumption itself fails. MUSLE is linear in LS **per cell**, so this can only
  fail through the aggregation path; if it fails, the failure is a defect in
  `load_geometry`/`SedGeometry`, and it must be reported as such rather than absorbed.
- **(R12)** `f_ero(V4)` and `f_area(V4) = 0.421` differ by more than the materiality bar —
  refuting the proxy that `docs/35` §9.3.3 and `docs/37` §4 both used to publish "≈ 104.8
  Mt/yr". *(`docs/35` §9.3.3 already flags this as a proxy and demands the exact re-run; this
  clause is the test it did not state a bound for.)*

### 2.5 H-L — the `L` form (the ×0.790 that produces the lower end of the bracket)

Registered as a **fifth** clause even though it is not one of the three levers named in the
task, because the published bracket's lower end (×0.333, "3.00×") depends on it and §1.1
Defect B shows it is currently confounded.

> Isolating the literal Desmet & Govers (1996) finite-difference `L` (their eq. 11 =
> Buarque's eq. 13) **with `S` held at ours** (`V5`) gives a factor that differs from the
> published 0.790, because 0.790 also swaps `S` from Moore & Burch to McCool (1987) and was
> measured on the uncapped `ls2d` rather than on `ls2d_hs`.

**Refuted if** `| ln f(V5) − ln 0.790 | ≤ 0.1644` — the confound is immaterial at basin scale
and the published bracket's lower end survives unchanged.

**Consequence either way, registered now:** if H-L is **not** refuted, the bracket
**×0.333 – ×0.421** and the derived statements *"our LS is 2.37×–3.00× the reference"*,
*"α reference ≈ 3.9–5.0"*, *"band ≈ 2.0–9.9"*, *"hard stop ≈ 11.8–14.9"* must be **re-derived
and re-quoted everywhere they appear** (`docs/35` §9.3.1, `docs/37` §4 candidate 0 and A2.2,
`docs/43` §1.4/§3.x, `docs/45` §2.1, `src/nbgen/make_nb18.py`, `make_nb19.py`) — as dated
corrections, never as silent edits.

---

## 3 — EXACT DEFINITIONS (no choice left to the measuring session)

### 3.1 The variants, named — and nothing is overwritten

`src/mgb_sediment.py:load_geometry` already takes `urh_ls2d=` and `ls2d_column=` as
parameters (verified at `src/mgb_sediment.py:863–864`), so every variant is reachable **by
name** without touching a default — the same discipline as `volume_convention`,
`k_unit_system` and `cp_revision`.

| id | name | definition (all at native 90 m, `ls2d_hs`'s own 1 km² channel cap unless stated) |
|---|---|---|
| **V0** | `ours_2026_08` | as built: upslope area ≤ 1 km², continuous McCool-89 `m`, `(sinθ/0.0896)^1.3`, `n = 1.3` — **the current engine input**, `urh_ls2d.csv:ls2d_hs` |
| **V1** | `lim_pixel` | V0 with **slope length ≤ one DEM pixel** |
| **V2a** | `m_cap05` | V0 with `m → min(m, 0.5)` — **the variant actually measured as ×0.502** |
| **V2b** | `m_step_eq14` | V0 with `m →` Buarque eq. 14 step function — **not yet measured** |
| **V3** | `s_ws78` | V0 with `S → 65.41 sin²θ + 4.56 sinθ + 0.065` |
| **V4** | `buarque_2015` | V1 + **V2b** + V3 — the source formulation **as read** |
| **V4′** | `buarque_2015_cap` | V1 + **V2a** + V3 — the ×0.421 row as published, kept so the prior number stays reproducible |
| **V5** | `L_dg96_fd` | V0 with the literal D&G finite-difference `L`, **`S` held at V0's** (isolates the `L` form; see Defect B) |

**Registered hard requirement:** `data/processed/urh_ls2d.csv` and
`data/processed/minibacia_ls2d.csv` are **not overwritten**. Variants go to a new file
(proposed: `data/processed/urh_ls2d_variants.csv`, one column per variant id, same
`mini,urh` key), and `scripts/c3/ls2d.py` is **not** run with a `--scale` other than 1 in the
repository tree — it writes the committed products
(`docs/agents/journal_decide-ls-resolution.md` §2 records that trap).

### 3.2 The aggregation — fixed, and it is the registered one

Per-cell LS → (minibacia, URH) by **`area_weighted_mean`**, the adopted aggregation
(`docs/37` §1 decision 3; `src/mgb_sediment.py:LS2D_AGGREGATION_FACTORS`). **The median is
not an admissible aggregate for a linear factor** and may not be used for any variant, in any
table, including diagnostics — the `per_cell_median` option exists only to keep the rejected
alternative reproducible.

### 3.3 The two factors, and which one decides

For a variant `V`:
```
f_area(V) = basin area-weighted mean of LS(V) / basin area-weighted mean of LS(V0)      [the PROXY]
f_ero(V)  = Σ_i E_i(V) / Σ_i E_i(V0)                                                    [the EXACT re-run]
```
where `E_i` is the modelled gross hillslope erosion of engine cell `i` over the full scored
decade 2009-01-01…2018-12-31 at **adopted defaults** (`volume_convention='williams_m3'`,
`k_unit_system='us_customary'`, `cp_revision='cited_central_2026_08_11'`, α = 11.8, β = 0.56,
`f_peak` 1.0), i.e. the configuration that produces **299.5387 Mt/yr** (`docs/37` A1.3).

**`f_ero` decides. `f_area` is reported beside it, always, and can never override it.**
Naming both and gating on one, in advance, is what stops the choice being made after the
fact (`docs/33` §1's device).

**Stratified reporting is mandatory** for every variant, on the strata
`journal_decide-ls-resolution` §2b already used, so the numbers are comparable:
elevation **< 200 m**, **200–1000 m**, **> 1000 m**; plus slope terciles; plus the
**per-station erosion-weighted `LS̄`** for all 18 usable SSC stations (`docs/42` §4.1 records
the V0 range as **38.2 – 117.1**, ln range **1.12** — that is the quantity G4.1 reads).

### 3.4 The `S`-factor pointwise ratios — a derivation, not a measurement

Computed here from the two published formulas alone (no data, reproducible in three lines;
recorded in `docs/agents/journal_ls-prereg.md`). It is offered as the *basis of H-S's field
clause*, and it is labelled **DERIVED-here**, not measured on our slope field:

| tan θ | θ° | MB86 `(sinθ/0.0896)^1.3` | W&S 78 | **W&S/MB** | McCool 87 | **McC/MB** |
|---|---|---|---|---|---|---|
| 0.005 | 0.29 | 0.0235 | 0.0894 | **3.809** | 0.0840 | 3.578 |
| 0.010 | 0.57 | 0.0578 | 0.1171 | 2.026 | 0.1380 | 2.387 |
| 0.020 | 1.15 | 0.1423 | 0.1823 | 1.281 | 0.2460 | 1.728 |
| 0.050 | 2.86 | 0.4677 | 0.4558 | **0.975** | 0.5693 | 1.217 |
| 0.090 | 5.14 | 1.0005 | 0.9993 | 0.999 | 1.0059 | 1.005 |
| **0.1581** (basin median) | 8.98 | 2.0589 | 2.3722 | **1.152** | 2.1235 | 1.031 |
| 0.300 | 16.70 | 4.5491 | 6.7761 | 1.490 | 4.3274 | 0.951 |
| 0.500 | 26.57 | 8.0848 | 15.1863 | 1.878 | 7.0132 | 0.867 |
| 1.000 | 45.00 | 14.6666 | 35.9944 | **2.454** | 11.3794 | **0.776** |
| 1.500 | 56.31 | 18.1215 | 49.1430 | 2.712 | 13.4784 | 0.744 |

Two things this table is allowed to be used for, and one it is not:
- it establishes that **the `S` swap is slope-dependent and non-monotone** (H-S field clause,
  and (R7)/(R8) are its refutation);
- it establishes that **`ls2d_dg96`'s S is neither ours nor Buarque's** (Defect B, H-L);
- it **may not** be used to compute a basin factor. The basin factor requires our own slope
  distribution and the erosion weights, i.e. §3.3.

### 3.5 Re-based expected consequence — stated NOW, before the re-run

`docs/35` §9.3.3 registered the expected consequence against the **prior** C level
(248.730 Mt/yr, `cp_revision='prior_2026_08_11'`). The adopted level is now **299.5387
Mt/yr** (`docs/37` A1.3, ×1.20427 erosion-weighted). Re-based, using the published proxy
factors and the same arithmetic:

| adopted variant | proxy factor | basin load (proxy) | against the 144–184 Mt/yr outlet anchors |
|---|---|---|---|
| V0 (today) | 1.000 | **299.5387 Mt/yr** | above both |
| **V4′ / V4** | 0.421 | **≈ 126.1 Mt/yr** | **below both** |
| V4 + literal `L` | 0.333 | **≈ 99.7 Mt/yr** | **further below both** |

> **Registered in advance, following `docs/35` §9.3.3 verbatim in intent: an unattractive
> total is not evidence against the source formulation.** If the adopted variant lands the
> basin load below the anchors, the correct report is that the residual widened — *not* a
> re-opening of the formulation choice. **This restatement is not an amendment to `docs/35`**
> (which this document may not edit); it is a consequential re-basing owed to that file's
> owner, recorded here and in §7.3.

---

## 4 — THE DECISION RULE, and the evidence grade required

### 4.1 The grade ladder (this project's, not a new one)

`docs/42` §3.3 and §6 G6 item 5, as amended by `docs/37` A1.6 item 3:

| grade | meaning in this project | LS example |
|---|---|---|
| **DERIVED** | reproduced by arithmetic from a published definition, twice, independently | `volume_factor` 47.8630 |
| **IDENTIFIED** | the stored artifact's provenance is recovered and reproduced to a stated residue | `k_factor` 7.593014, ≤ 1.3 % |
| **CITED** | a page-numbered published source states the choice, with its conditioning; a single admissible reading | Desmet & Govers (1996) pins the LS **formula** |
| **ASSUMED** | a choice made without a source, declared as such, one-sided where possible | P = 1.0, FG = 1.0 |
| **UNVALIDATED** | no independent evidence pins the quantity, and none is obtainable from a fit | **the LS *level* — `docs/42` G4.2, and it stays UNVALIDATED after this document whatever it decides** |

### 4.2 The rule (priority order; every criterion is a source or a derivation)

Items 1–4 are **carried unchanged from `docs/35` §9.3.2**, which is frozen and binds:

1. **Fidelity to the transposed method wins by default** — the source formulation (limiter at
   one pixel, eq. 14, W&S 78) is the registered default outcome.
2. **A deviation is admissible only with its own written source justification**, naming a
   citable reason why the source's choice is wrong *for this basin*, dated, **written before
   the resulting basin total is computed**. *"Our terrain is steeper"* is not such a reason
   unless a citation says the source's choice fails on steep terrain.
3. **A deviation adopted under (2) requires the α band rescaled** by the measured level ratio
   `mean(LS_ours)/mean(LS_source)`, reported in the same table as any fitted α.
4. **Ties break toward the lower LS level** (Buarque p. 121's own verdict that his Andean LS
   is already an over-estimate, and our limiter is looser than his). **A tie may not be broken
   by the basin total.**

This document adds the grade requirement and the three-outcome table:

5. **The adopted formulation must reach grade CITED on all three levers** — verbatim,
   page-numbered, single admissible reading, `Sf` units verified — before any default is
   switched.

| outcome | condition | what it licenses | what it does NOT license |
|---|---|---|---|
| **ADOPT-SOURCE** | all three levers **CITED**; H-M's (R6) not triggered; the §3.3 exact re-run completed and reported; the §4.3 forbidden evidence untouched | proposing `V4` as the engine default in a *separate*, dated amendment owned by whoever owns `scripts/c3/ls2d.py` and `docs/37`; α band rescaled per item 3; every prior variant still reachable by name | it does **not** validate the LS level (still **UNVALIDATED**), does not close C3 clause 2 on its own, does not change Π's *status*, and does not license re-fitting anything to the new level without §6 |
| **ADOPT-BAND** | ≥ 1 lever **CITED but ambiguous** (two admissible readings, differing by more than the materiality bar) | adopting the **lower-LS** reading under item 4, **and** carrying `f_LS` as an explicit **band** (both readings) through C4, C5 and every load table | it does **not** license choosing the reading that lands the load nearer an anchor, and does not collapse the band for convenience anywhere downstream |
| **NEGATIVE — UNRESOLVED** | ≥ 1 lever with **no citable ground either way**, or (R6) fires, or the source text cannot be obtained/verified | **§7**: publish the negative result; keep V0 as the default *because it is incumbent, not because it won*; carry the full bracket as a declared uncertainty on Π's decomposition | it does **not** license silence, does not license quoting a single `f_LS` anywhere, and does not license C4/C5 proceeding as if the level were settled |

### 4.3 Evidence that may NOT be used — in any outcome

Registered explicitly because each of these has already misled this project once:

- **the basin total, the outlet anchors (144–184 Mt/yr), or the distance between them**
  (`docs/35` §9.3.3; `docs/40` §8);
- **the retired "mountainous LS 2–10" band** — uncited, retired (`docs/37` §1 decision 4).
  Its coincidence with the source formulation's median 7.262 is a *fingerprint*, and
  `docs/35` §9.3.5 already forbids using it as evidence. **An uncited band cannot pass a
  choice any more than it could fail one;**
- **the retired SDR band 0.05–0.30** (`docs/40`) and any implied-SDR arithmetic built on it;
- **any α band** — `docs/35` §6.1's is itself LS-conditional, and `docs/43` §1.3 measured that
  97.7 % of the source method's 426 published pairs land inside it *because the source's own
  search prior contains it*;
- **any C4 fit, at any stage.** §8 gives the derivation: at fixed LS *shape*, a change in the
  LS level is exactly absorbed by α̂ and the objective surface is unchanged up to a relabelling
  of the α axis. **A fit is structurally incapable of preferring one LS level over another**,
  so quoting fit quality as evidence for an LS choice is not weak evidence — it is zero
  evidence;
- **`check_musle_parameters`'s verdict** (`ok`/`watch`/`STOP`), which reads the same
  LS-conditional band and **STOPs 185 of 426 published, adopted pairs** (`docs/37` A2.1).

### 4.4 Ordering guarantee (the thing that makes this a pre-registration at all)

The measuring session **writes the chosen variant and its §4.2 justification into the record
first**, then runs the re-run, then looks at the total — `docs/35` §9.3.4 item 2, restated so
it is unmissable. The journal must contain the sentence *"this decision is recorded before any
basin total under it was computed"*, and the file birth times must support it.

---

## 5 — WHAT IS NOT ALLOWED TO MOVE

None of the following may be changed, re-fitted, re-defaulted or "improved" by any work under
this pre-registration. Each is a frozen or adopted object with its own owner.

| object | value / location | why it is immovable here |
|---|---|---|
| **The adopted C revision** | `cp_revision='cited_central_2026_08_11'` (`docs/41`; erosion-weighted ×1.20427) | it is a *different* factor of Π with its own document; touching it while deciding LS makes both undecidable. The prior revision stays reachable by name and is **not** to be reinstated |
| **The unit conventions** | `volume_convention='williams_m3'` → `volume_factor` **47.8630** (**DERIVED**); `k_unit_system='us_customary'` → `k_factor` **7.593014** (**IDENTIFIED**) | `docs/35` §9.2; a load is already 363× ambiguous in convention (`docs/37` A1.6 item 6) — LS work may not add to that |
| **The H2E hydrology** | `parameters_H2E.csv`; reproduce with `python3.10 src/report_h2e.py`, **F must match 0.25931 to 1e-8** | Phase B is closed (`docs/30` §1); re-opening needs its own pre-registration |
| **The frozen driver bundle** | `data/processed/sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv, q_gauge_H2E.npz, q_gauge_H2E.csv, report_H2E.json, metrics_fleet.csv}` | **read-only, always.** Every LS variant is a static-input change; no driver is regenerated |
| **`ls2d_aggregation`, `ls2d_resolution`** | both at factor **1.000** (`area_weighted_mean`, `native_90m`) | `docs/42` **G4.2**: they may not be used to move the level. The **resolution** question is separately **RESOLVED** at 90 m (`journal_decide-ls-resolution` D1–D6) and this document does **not** re-open it |
| **The committed LS products** | `data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv`, and `scripts/c3/ls2d.py`'s defaults | variants are written to a **new** file (§3.1); the default switches only through §4.2's separate dated amendment |
| **The frozen pre-registrations** | `docs/33`, `docs/35`, `docs/42`, `docs/45` — including `docs/45`'s `f_LS = 1.000` parameter card | a frozen pre-registration is amended by **its own owner**, in **its own** amendment slot, dated. This document records what is **owed** (§7.3) and enacts none of it |
| **P, FG** | 1.0, 1.0 — **ASSUMED, one-sided** | they are Π; moving them under cover of an LS decision is the compensation this whole guard set exists to prevent |
| **The yield embargo** | absolute flux only (t/day, Mt/yr) | `docs/23` §13.2; no t/km²/yr may be produced by any LS variant table |

---

## 6 — THE C4.3 GATE: may the search start before LS lands?

**Both branches are stated with their conditions, and the branch is decided by one cheap
measurement made before either job runs.**

### 6.1 The deciding pre-test (registered, and it costs minutes)

Compute, for the 18 usable SSC stations, the per-station upstream **erosion weight**
`w_s = E_upstream(s) / Σ_s E_upstream(s)` under **V0** and under **V4**, at adopted defaults,
with no fit. Then
```
Δ_shape = max over the 8 CAL stations of | ln( w_s(V4) / w_s(V0) ) |
```

| condition | branch |
|---|---|
| **Δ_shape ≤ 0.1644** | the LS swap is, for the fit set, a **level** change → **Branch A** is available |
| **Δ_shape > 0.1644** | the LS swap moves the fit set's own weights by more than the level's standard error → it is a **shape** change → **Branch B is mandatory** |

**Why this is the right discriminator, derived not asserted:** LS enters MUSLE linearly per
cell and the transport step is linear in cell load, so a *uniform* LS factor `f` multiplies
every station's simulated flux by the same `f`. The search optimum then moves to `α̂/f` and
**at that optimum** the fitted **Π**, the objective value, the residual vector and every
residual-structure statistic are **identical** — the objective surface is the same surface
with a relabelled α axis. A change that moves
stations *relative to each other* changes the residual vector itself, so the fit is not
recoverable by rescaling — it must be re-run. `docs/37` A2.2 already classifies the LS shape
as a defect distinct from the level for this reason; §6.1 is that classification made
operational for one specific decision.

### 6.2 Branch A — C4.3 MAY start before LS lands

Available **only** if `Δ_shape ≤ 0.1644`, and **only** with all six of:

- **A1.** Every C4.3 artifact is labelled **PROVISIONAL — LS FORMULATION UNRESOLVED**, in the
  file, in the table, and in the notebook cell. It is not C4's verdict.
- **A2.** The run card declares `ls_formulation = ours_2026_08`, grade **UNVALIDATED**, with
  the bracket **×0.333 – ×0.421** printed beside it and the sentence *"a later LS adoption
  multiplies α̂ by 2.37× – 3.00× and leaves Π unchanged"*.
- **A3.** **The ADOPT outcome of `docs/45` §6.1 is not reachable.** Its conditions (2) and
  (3) and its `FAIL — RAILED / HARD STOP` row read α̂ against **3.9 / 35.4**, which is an
  LS-conditional band (`docs/37` §4 candidate 0). A provisional fit may return **ADOPT-PENDING
  at most**. *(This does not amend `docs/45`; it is strictly more restrictive, and every
  `docs/45` condition continues to apply.)*
- **A4.** **The α̂ stop.** If the provisional fit returns **α̂ ≥ 10.0**, the verdict is
  **blocked** until LS lands. Derivation, not a guess: the registered α box is **[2.0, 30.0]**
  (`docs/45` §2.1); a later adoption of the source formulation multiplies α̂ by
  `1/f ∈ [2.375, 3.00]`; `30.0 / 3.00 = 10.0`, so any α̂ above 10.0 **may** put the
  equivalent source-LS optimum outside the registered box, and above `30.0 / 2.375 = 12.63`
  it **certainly** does. A fit whose equivalent lies outside its own registered box is not a
  fit that can be re-expressed — it needs a **new pre-registration**, not a re-run.
- **A5.** **G4.1 runs and is reported** (the `ln LS̄_i` coefficient in the joint regression,
  with its 95 % station-bootstrap interval, and the **minimum detectable coefficient** given
  the registered noise floor σ_r = 0.465 ln and the ln `LS̄` range 1.12). If **G4.1 fires**,
  the verdict is blocked — `docs/42` G4.1's ACTION on FAIL is to fix the field, never α.
- **A6.** **No rescaling in place of a re-run.** No C4.3 statement may convert its result to
  another LS by multiplying α̂ by `1/f`. Rescaling is arithmetic on the *level*; the adoption
  changes the *shape* too, and A1's provisional label exists precisely because the re-run is
  owed.

### 6.3 Branch B — C4.3 must wait until LS lands

**Mandatory** if **any** of:

- **B1.** `Δ_shape > 0.1644` (§6.1).
- **B2.** The C4.3 session intends to issue a **final** verdict — i.e. anything other than
  PROVISIONAL — because ADOPT is unreachable under A3.
- **B3.** G4.1 has fired in any prior run on the V0 field.
- **B4.** The LS decision is expected to change the **`m` step-vs-cap** answer (H-M) or the
  **`L` form** answer (H-L), both of which are shape levers and both of which are currently
  *unmeasured*: a fit run under an LS whose own definition is in flux is a fit to an unnamed
  object.
- **B5.** The freezing of this document is already scheduled — in which case waiting costs
  what §6.4 measures and nothing else.

### 6.4 The cost comparison, measured, offered as information and NOT as the rule

| job | measured / registered cost | source |
|---|---|---|
| one 90 m LS pass over 30.2 M cells | **≈ 4 minutes** | `journal_decide-ls-resolution` D2 |
| the eight variants of §3.1 + the exact decade re-runs | **hours, not days** | above + `docs/37` A1.8 reproduction |
| C4.3's registered search | **5,482 grid evaluations + 4 × 1,000 DDS**, timing probe with a **6 h** ceiling | `docs/45` §2.5 |
| a C4.3 **re-run** after a later LS adoption | the same 5,482 + 4,000, **plus** the re-derivation of every guard statistic on the new residuals | `docs/45` §2.5, §4.2 |

**LS-first is cheaper on every one of these numbers.** That fact is recorded so the decision
is made with it in view, and it is **explicitly not** a gate condition: the gate is §6.1–§6.3.

---

## 7 — PRE-COMMITMENT: the negative result is a publishable finding

### 7.1 The commitment

> **If the levers cannot be settled from the literature — if the source text is ambiguous,
> if `Sf`'s units cannot be verified, if two admissible readings survive, or if the primary
> documents cannot be obtained — then "the LS level is not resolvable from the available
> literature" is the RESULT, it is written up in full, and it is reported as a finding rather
> than as a stalled task.**

The write-up must contain, at minimum: the levers with their exact re-run factors; the
readings that survive and the sentences that generate them; the bracket carried as a band; the
per-factor grades; and the sentence *"the LS level enters Π and cannot be validated by any
fit"* (§8).

### 7.2 Why this project treats a negative result that way

The precedent is explicit and is not being invented here:

- **`docs/30` §1** closed Phase B **on the input-ceiling result**, by decision, at a measured
  ceiling rather than at a target, and called that ceiling *"a quantified, transferable
  closing statement — publishable as-is"*.
- **`docs/33` §3.4** pre-committed that "both hypotheses hold, no refit" would be **a RESULT,
  not a failure and not an anticlimax**.
- **`docs/40`** retired the SDR gate as **UNCITABLE** and published the retirement, holding
  the line that *"a retired gate is neither a pass nor a fail"*.
- **`docs/29`** published H1-vs-H2 as **not separated**.

### 7.3 What the negative result obliges, and what it does not

**Obliges:** `f_LS` quoted as a **band** wherever it appears; both variants reachable by name;
the C5 caveat list extended by one line; and these consequential corrections **recorded as
owed** to their own owners (this document enacts none of them):

1. `docs/35` §9.3.3's expected consequence is stated against the **prior** C level and needs
   re-basing to 299.5387 Mt/yr (§3.5) — owed to `docs/35`'s amendment slot §9.
2. If H-M is not refuted, the ×0.502 row's label *"his eq. 14"* is wrong in `docs/35` §9.3.1,
   `docs/37` §4 candidate 0, `docs/43` §1.4, `src/nbgen/make_nb18.py` and `make_nb19.py`.
3. If H-L is not refuted, the ×0.790 / ×0.333 bracket and everything derived from it
   (§2.5) needs re-deriving in the same five places plus `docs/45` §2.1.
4. `docs/42` §9 still owes the transcription of `docs/43` §3.1's P1/P2/P3 (recorded in
   `docs/45` §0 as outstanding; unrelated to LS but in the same amendment slot).

**Does not oblige, and explicitly does not license:** picking the variant that lands the load
nearer an anchor; collapsing the band anywhere downstream; treating the incumbent V0 as
*validated* because it survived by default; or a second, differently-worded attempt at the
same question without a new pre-registration.

---

## 8 — THE CONFOUNDING DECLARATION, and what this pre-registration therefore CANNOT conclude

### 8.1 One identifiable product

`docs/42` §3.1, carried verbatim in substance:

```
Sed = f_vol · f_K · f_LS · α · (Qsur · q_peak · A)^β · K · C · P · LS2D · FG
```

α, the C level, **the LS level**, the K unit system, the volume convention, P and FG are
**spatially and temporally uniform scalars**. Their partial derivatives of `ln Sed_i` are the
same column of ones at every station, on every day, in every window. The design matrix
`[1 | per-station land-class erosion shares]` has **condition number = inf** — exactly
singular. Only the product is identifiable:

```
Π = α · f_vol · f_K · f_LS · C_mult · P · FG   =  5,164.42 today
                                                  (docs/37 A1.6 item 2, adopted C)
```

> **NO calibration — on a basin total, on 8 stations, on 13, on 18, on daily series, on any
> objective function whatsoever — can separate the LS level from α, from the C level, from the
> K unit factor, from the volume convention, from P, or from FG.**

### 8.2 The consequence for THIS document, stated as prohibitions

This pre-registration, however it comes out, **cannot conclude**:

1. **that the LS level is correct, validated, or confirmed** — at any grade. `docs/42` **G4.2**
   is unchanged by anything here: the level is **UNVALIDATED** and must be printed that way.
   *Cited is not validated* (`docs/37` A1.6 item 3), and **fitted is not validated either**
   (`docs/43` §3.3 item 1);
2. **that α is right or wrong** — an α reference rescaled by `1/f` is a statement about the
   *pairing* of α with an LS, not about α;
3. **that the model is under- or over-erosive.** The C3 residual's **DIRECTION is UNKNOWN**
   (`docs/37` A1.9; the *"~2× under-erosive"* claim is **WITHDRAWN**), so no LS variant may be
   argued for or against by which way it moves the load;
4. **anything about the C level, the K unit system, the volume convention, P or FG.** They are
   the same parameter written differently; an LS result that appeared to say something about
   one of them would be saying something about Π;
5. **that the LS *shape* is right**, on any non-detection. `docs/42` G4.2: a G4.1
   non-detection exonerates the field's shape **and says nothing about its level**; and a
   non-detection at unreported power says nothing at all, which is why A5 requires the
   minimum detectable coefficient to be printed beside the interval;
6. **that C3 closes.** Clause 2 of `docs/37` A1.1's conjunction needs the *shape* decision;
   clauses 3 and 4″ are untouched by anything here (`docs/43` §2). Settling LS is **necessary
   and not sufficient**;
7. **anything about 66.53 % of the model's erosion**, which lies upstream of no usable SSC
   station (`docs/45` §1 item 6), or about the 801.1 km of channel below the outlet-most one.

### 8.3 The one thing it CAN conclude

**Which formulation the engine uses, on written source grounds, with a grade — and therefore
what the decomposition of Π is, and what α̂ has to be multiplied by to be quoted against a
published α.** That is a statement about *bookkeeping and provenance*, and it is worth making
precisely because the alternative is that a 2.4×–3.0× factor stays hidden inside a product
nobody can decompose.

---

## 9 — REGISTRATION CARD — **BLANK. This document is a DRAFT.**

| | |
|---|---|
| Status | **DRAFT — NOT IN FORCE** |
| Drafted | 2026-08-11, by the `ls-prereg` agent (`docs/agents/journal_ls-prereg.md`) |
| Frozen | *(blank — to be filled by the freezing session, with a date and a name)* |
| Sections that freeze on that date | §1–§8 |
| Amendment slot | §10, once frozen |
| Frozen artifacts touched by this draft | **none.** `sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv, q_gauge_H2E.npz, q_gauge_H2E.csv}` were **not opened**. No calibration launched, no fit performed, no simulation run, no `data/` product written, no git command run |
| Numbers computed by this draft | **two derivations only**, both from published formulas with no project data: the `S`-factor pointwise ratios (§3.4) and the `m` step-vs-cap divergence (§1.1). Both are reproducible in three lines and are recorded in the journal |
| Everything else | carried from `docs/33`, `docs/35`, `docs/37`, `docs/40`, `docs/41`, `docs/42`, `docs/43`, `docs/45`, `journal_decide-ls-resolution`, `journal_c31-ls2d`, and read-only inspection of `scripts/c3/ls2d.py` and `src/mgb_sediment.py` — cited in place |

### 9.1 What a freezing session must settle FIRST

Recorded so that freezing is a decision and not a rubber stamp:

1. **Defect A and Defect B (§1.1) are either resolved or explicitly inherited.** If inherited,
   say so in the card — a frozen document that quotes ×0.502 as "eq. 14" and ×0.790 as "the
   `L` form" inherits two mislabels.
2. **Whether the `Sf` units of eq. 14 can be verified** from Buarque (2015) pp. 46–48. If the
   source PDF cannot be re-obtained, H-M's (R6) is unfalsifiable and the honest outcome is
   already **NEGATIVE — UNRESOLVED** for that lever.
3. **Who owns the enactment.** This document decides *what* is adopted; switching the engine
   default is a separate dated amendment in the file that owns `scripts/c3/ls2d.py` and
   `urh_ls2d.csv` (§4.2, §5).
4. **Whether §6's gate is accepted as more restrictive than `docs/45` §6.1**, since it removes
   the ADOPT outcome from a provisional C4.3. If it is not accepted, §6 must be rewritten
   before freezing — not overridden afterwards.

## 10 — Amendment slot *(inactive until this document is frozen)*
