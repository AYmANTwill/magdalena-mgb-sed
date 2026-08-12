# 46 — Resolving the LS **level**: pre-registration — **FROZEN (READ OUT)**

> # ⚠ FROZEN 2026-08-11. §1–§8 ARE IN FORCE. §10 IS THE AMENDMENT SLOT.
>
> **Status: FROZEN (READ OUT), 2026-08-11**, by the **`amend-46`** session
> (process record: `docs/agents/journal_amend-46.md`). Drafted 2026-08-11 by the `ls-prereg`
> agent (`docs/agents/journal_ls-prereg.md`); amended before freezing per `docs/51` §5.6
> items (a)–(e) and `docs/52` §6. The registration card is **§9**.
>
> ## READ OUT — read this before anything else in the file
>
> **Four of §2's five hypotheses had ALREADY been measured before this freeze** — H-LIM
> (R1/R2/R3), H-M (R4/R5/R6), H-JOINT (R10/R11/R12) and H-L — by the variants harness,
> `docs/49` and `docs/50`, and the read-out is printed in full in **§1.2**. *(The exception is
> **H-S's field clause** (R7)/(R8), whose measurement on our own slope field and strata does not
> exist.)* **This document therefore freezes as a pre-registration that has been READ OUT, not as
> an open one**, and it may not be cited as though §2 were prospective. Saying so is `docs/51`
> §5.6's own condition for the freeze being honest.
>
> **What remains genuinely prospective**, and is what the freeze is actually worth: **§4**'s
> decision rule and grade requirement, **§6**'s C4.3 ordering gate, and **§7**'s negative-result
> pre-commitment. *(`Δ_shape` was blinded when §6.1's discriminator and §2.0's striking of the
> bar were decided; it landed the same day and is recorded in **§10, amendment 1**.)*
> **Nothing has been adopted, no
> engine default has moved, and the enactment amendment is unwritten** — enactment is
> `docs/37` §A3 (`docs/51` §5.3), and *that*, not this freeze, is `docs/47`'s **B1** unblocking
> event.
>
> **What frozen means here:** §1–§8 are binding as written on 2026-08-11 and are changed only
> through **§10**, dated, by this document's owner — the `docs/33` / `docs/35` / `docs/42` /
> `docs/45` pattern. A session that believes a rule here is wrong **journals the objection and
> follows the rule anyway**.
>
> **This document contains NO statistical materiality threshold.** The draft's `0.1644 ln`
> materiality bar was **STRUCK, not rescaled**, at all **fifteen** of its sites; what replaces
> it is fixed in **§2.0** and the reasons are `docs/52`. No number may be reconstructed from
> this file to serve as one.
>
> **It does not supersede `docs/35` §9.3**, which is a frozen pre-registration of the same
> comparison. This document is *subordinate* to it: where the two disagree, **`docs/35`
> wins** and this file is the bug. What this document adds is what §9.3 does not contain —
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

Also already known: the levers **do not multiply out** — on the **exact erosion-weighted**
re-run, `0.362435 × 0.52204 × 1.694054 = 0.3205244` against a joint **0.431944**, i.e.
**joint / product = ×1.34762** (`docs/52` §1.1); the area-weighted proxies show the same thing
(0.5051 × 1.7139 × 0.3513 = 0.3042 ≠ 0.4214, `docs/49` §6 item 2).

### 1.0 THE BRACKET — corrected before freezing (amendment (a), `docs/51` §5.6)

> **SUPERSEDED AND NOT QUOTABLE FROM THIS DOCUMENT:** the bracket **×0.333 – ×0.421**, the
> phrase *"our LS is 2.37× – 3.00×"*, and the derived α reference ≈ 3.9 – 5.0, band ≈ 2.0 – 9.9
> and hard stop ≈ 11.8 – 14.9 (`docs/37` §4 candidate 0). They are printed here **only** so the
> superseded statement is identifiable wherever it is still in print.

> ## The registered statement
> **`f_LS` ∈ [0.25146, 0.43194] erosion-weighted ⇒ `1/f_LS` ∈ [2.3151, 3.9768]** — our LS is
> **2.3151× – 3.9768×** the level α = 11.8 is paired with.
> Area-weighted proxy **[0.24468, 0.42148]**, measured **2.5 % low** (`docs/47` §3.1 R7).

| quantity | published (superseded) | **registered here** |
|---|---|---|
| upper end (`f` nearest 1) | ×0.421 | **×0.43194** ero · ×0.42148 area |
| lower end | ×0.333 | **×0.25146** ero · ×0.24468 area |
| `1/f_LS` | 2.37× – 3.00× | **2.3151× – 3.9768×** |
| ln width | 0.2345 | **0.5410** — 2.31× wider |
| α reference `11.8 · f` | ≈ 3.9 – 5.0 | **2.967 – 5.097** |
| `docs/35` §6.1 band `5.9 – 23.6 · f` | ≈ 2.0 – 9.9 | **1.484 – 2.548 … 5.935 – 10.194** |
| hard stop `35.4 · f` | ≈ 11.8 – 14.9 | **8.902 – 15.291** |
| basin load at the endpoint | ≈ 126.1 / ≈ 99.7 Mt/yr (proxy) | **129.3840 / 75.3235 Mt/yr** (engine) |

**The interval is NOT an uncertainty over admissible readings of the source** (`docs/51` §2.3).
Every lever is **CITED** (§1.2), and with Buarque eq. 13 read verbatim (§2.2, §2.5) there is no
admissible reading in which `L` is our point-rate form. Therefore:

- **the source formulation read whole is a POINT: `f_LS` = 0.25146 (ero) / 0.24468 (area);**
- **×0.43194 is a documented HYBRID** — the source's three levers with **our** `L` — retained
  only because `docs/35` §9.3.1, `docs/37` §4 candidate 0 and `docs/43` §1.4 quote it and it
  must stay reproducible;
- **the span between them is the `L`-form lever, exactly:**
  `ln(0.43194 / 0.25146) = 0.5410 = −ln 0.580685`.

Source: `docs/47` §4.3 engine re-runs, confirmed and cross-checked in `docs/51` §2.1–§2.2 (the
upper endpoint's area-weighted counterpart reproduces the published ×0.421 row to **15
significant figures**; the lower endpoint's has **three** independent reproductions; both
ero/area pairs are consistent with `docs/47` R7's separately measured proxy bias to 4 s.f.).

**Three residues travel with both ends** (`docs/51` §2.4, carried so nothing is over-read):
1. both rows are the source's **formulation on OUR terrain data** — 90 m COP90 (his 500 m),
   Horn 3×3 slope (his eq. 15 centred differences), our D8 routing, our URH mask. §3.1 fixes
   this deliberately, but it means **neither number is "his LS"**;
2. the **lower end rests on ONE erosion-weighted measurement** against three area-weighted ones
   (`urh_ls2d_variants.csv` carries no `V4_dg` column) — the second reproduction is owed, and is
   a verification, not a blocker (`docs/51` §7 item 7);
3. **`α = 11.8` (Williams 1975) predates every 2-D contributing-area LS by two decades** — its
   like-for-likeness with any of these numbers is **NOT SETTLED** (`docs/47` §4.2 item 6). It
   bounds every ratio above and **no band is offered for it**.

> **Therefore no hypothesis in §2 may "predict" any number in this section.** The
> hypotheses below are about quantities that were **not** measured when they were written, and
> each names which one. **⚠ As of the freeze this condition no longer holds for any of them —
> see §1.2.**

### 1.1 Two defects in the existing evidence — **BOTH RESOLVED BY MEASUREMENT BEFORE THE FREEZE**

Both were found by reading the code and the source description, and both are stated below with
the arithmetic that supports them. They were written as *open* defects for §2 and §3 to settle.

> **Amendment (c), 2026-08-11 (`docs/51` §5.6c; primary records `docs/49`, `docs/50`,
> `docs/51` §3–§4).** Both have since been measured, and the verdicts are **not** the ones the
> paragraphs below predict. `docs/46` §9.1 item 1's *"explicitly inherited"* option was
> therefore **not available and was not taken** — inheriting them would have frozen two
> falsified paragraphs.
>
> | defect | verdict | the deciding number |
> |---|---|---|
> | **A** — the ×0.502 row is a cap, eq. 14 is a step | **RESOLVED — IMMATERIAL as a level, REAL as a label** | `f(V2b)/f(V2a)` = **×1.005212** area-wtd (0.52 %) · **×1.008878** ero-wtd; on the *endpoints* `\|ln V4/V4′\|` = **0.00362** upper, **0.00101** lower; α reference +0.018 (5.079 → 5.097) |
> | **B** — the ×0.790 `L` ratio is confounded | **RESOLVED — MATERIAL, but by a DIFFERENT MECHANISM than the one stated** | the endpoint moves `\|ln\|` **0.307** (×0.333 → ×0.24468 area) and the bracket becomes **2.31× wider in log units**; the stated `S` confound accounts for only **0.026** of that |
>
> **The direction of the correction is the opposite of the one Defect A predicts.** The text
> below reasons that eq. 14, being less reducing than the cap, makes the true gap *smaller than
> 2.37×*. Measured, the gap **widened** to 2.3151× – 3.9768× — and **none of that widening is
> Defect A's** (its share at the ×0.421 end is **−0.36 %**, 2.3235× → 2.3151×, `docs/49` (c)).
> Defect B's resolution is what moved it.
>
> **And the bookkeeping reverses:** the published **×0.421 was already the step** — it is
> **V4**, not V4′ — so Defect A contaminated the **single-lever label only** and **never touched
> the joint**. §3.1's variant table is corrected accordingly (amendment (b)).

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

> **MEASURED, 2026-08-11 (`docs/49`) — the reasoning is right and the consequence is nil.** The
> *sign* holds: `f(V2b)` **0.522043** > `f(V2a)` **0.517480** erosion-weighted (0.505092 >
> 0.502472 area-weighted). The *size* is **×1.005212 area / ×1.008878 erosion** — because the
> terrain below the true cap/step crossover (`tan θ = 0.0893325`, solved, not guessed) carries
> **37.86 % of basin AREA but only 2.14 % of basin EROSION**, a 17.7-fold mismatch. For Defect A
> to have mattered at the level, that terrain would have had to carry **83.8 %** of the source
> field's erosion; it carries **4.1 %**. **And the joint ×0.421 never carried the cap at all**
> (§3.1). The reading defect stands and is not nil: `min(m, 0.5)` is nobody's published
> formulation and **may never be graded CITED** (§2.2) — the mislabel is owed to `docs/35`
> §9.3.1, `docs/37` §4 candidate 0, `docs/43` §1.4, `src/nbgen/make_nb18.py`, `make_nb19.py`
> (§7.3 item 2, now unconditional).

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

> **MEASURED, 2026-08-11 (`docs/50`, `docs/51` §4) — RIGHT CONCLUSION, WRONG DIAGNOSIS.** The
> endpoint is wrong, by `|ln|` **0.307** (×0.333 → ×0.24468 area), and the bracket is **2.31×
> wider in log units** than published. But **the mechanism named above is not what does it.**
> Exact factorisation of the published number: **0.790 = 0.852262 (`L` form) × 0.926925 (`S`
> swap)** — so the stated `S` confound is worth `|ln| ≈ 0.026`, i.e. **8 %** of the move — while
> the **column** confound (`ls2d` → `ls2d_hs`), presented above as the afterthought, is
> **0.887977** (`|ln|` 0.1188) and is **the larger of the two**. The two errors nearly cancel
> (`S` 7.3 % low, column 10.7 % high, net +2.6 %): **arithmetic luck, not a defence.**
>
> **What actually breaks ×0.333 is that the `L`-form ratio is FORMULATION-DEPENDENT** —
> **0.852262** uncapped / **0.769833** on `ls2d_hs` / **0.580685** *inside the source
> formulation* (span `ln` 0.384) — **and was composed across formulations as a scalar.**
> Repairing the stated confound *completely* still gives `0.421363 × 0.769833 = 0.324379`
> against the measured **0.244679**: wrong by **×1.326**. A scalar `L`-form ratio is not a
> transferable object, and no repair of the `S` confound alone recovers the endpoint.
>
> **Consequence for H-L:** its refutation statistic (`|ln f(V5) − ln 0.790|` = **0.0258**) is
> **not** the test — see §2.5, re-hung by amendment (c). The bracket's re-derivation is owed
> **unconditionally**, because it is superseded by measurement (§1.0), not because a hypothesis
> survived.

### 1.2 THE READ-OUT — what §2 already returned, printed before the freeze

**This is the uncomfortable part of the freeze and it is stated first rather than buried.**
`docs/46` was drafted as a pre-registration of §2's five hypotheses. Between the drafting and
the freeze — the same day — **four of the five were measured**, by the variants harness,
`docs/49` and `docs/50`. A pre-registration whose hypotheses have been read out is still worth
freezing (§4's rule, §6's gate and §7's pre-commitment are untouched by the read-out, and they
are what the freeze protects), but it **may not be presented as an open one**, and no session
may cite §2 as though its answers were still unknown.

| clause | statistic, at full precision | read-out | source |
|---|---|---|---|
| **(R1)** second admissible reading of pp. 94 / 121 | — | **does not fire.** Two independent sentences (p. 94 + p. 98); single admissible reading ⇒ limiter **CITED** | `docs/51` §1.2 |
| **(R2)** `f_ero(V1)` vs area 0.351 | `f_ero(V1)` = **0.362435**, ratio **×1.0326**, `\|ln\|` 0.0321 | proxy and exact agree; **reported diagnostic**, not a gate (§2.0) | `docs/47` §4.3, `docs/49` |
| **(R3)** another lever beats the limiter | `\|ln f\|`: limiter **1.0150** · `m` step 0.6500 · `m` cap 0.6588 · `L` form 0.5435 · `S` 0.5271 | **does not fire** — the limiter is the dominant lever on the exact re-run | `docs/48` §5.3 |
| **(R4)** step vs cap magnitude | `f(V2b)/f(V2a)` = **×1.008878** ero (**×1.005212** area) | **retired as a refutation clause** (§2.0); H-M's field content is the **sign**, and the sign held | `docs/49`, `docs/52` §6 |
| **(R5)** predicted sign | 0.522043 > 0.517480 ero; 0.505092 > 0.502472 area | **does not fire — H-M's field clause is CONFIRMED on its sign** | `docs/49` |
| **(R6)** `Sf` units | p. 47, verbatim: *"onde Sf [%] é a declividade do pixel"*, corroborated on p. 48 | **does not fire.** `Sf` is slope **percent**; the `m` lever reaches **CITED** (§2.2) | `docs/51` §1, `docs/38` §9.1 |
| **(R7)/(R8)** `S` acts as a scalar | per-cell `S_WS78/S_MB86` ≈ **0.975 – 3.81**, non-monotone (§3.4, **DERIVED-here**) | **NOT READ OUT.** The field measurement on *our* slope field, and the three strata, **do not exist**; the shape conclusion rests on the derivation alone | §3.4; `docs/51` §7 item 9 |
| **(R10)** naive product vs joint | product **0.3205244** vs joint **0.431944**; **joint/product = ×1.34762**; `\|ln\|` **0.2983374** | **retired as a refutation clause** — decided by the citation (§2.0; `docs/52` §3) | `docs/52` §1.1 |
| **(R11)** exact load vs `299.5387 × f_ero` | reproduced through the exact-linearity route (**0.431944** vs 0.43194), behind a basin-erosion gate at **299.5387088405831 Mt/yr** | **does not fire** — linearity holds | `docs/49` gate 2 |
| **(R12)** `f_ero(V4)` vs `f_area(V4)` | **×1.02484** (upper) / **×1.02771** (DG), against `docs/47` R7's 1.0251 / 1.0278 | proxy bias confirmed at ≈ 2.5 %; **reported diagnostic**, not a gate | `docs/47` §3.1, §4.3 |
| **H-L** `f(V5)` vs 0.790 | `\|ln\|` **0.0258** — *and it is not the test* (§2.5) | the published 0.790 **does not isolate the `L` form** (0.852262 × 0.926925, measured on the wrong column) ⇒ the confound is real, and the bracket is re-derived unconditionally | `docs/50`, `docs/51` §4 |

**What the read-out did NOT do, stated so the freeze is not over-read:** it adopted nothing,
switched no default, ran no fit and produced no α̂. §4.2's outcome (ADOPT-SOURCE / ADOPT-BAND /
NEGATIVE — UNRESOLVED) is **unexercised**; `Δ_shape` was **unmeasured and blinded** when §2.0 and
§6.1 were written, and landed the same day (**§10, amendment 1**); §6's branch
is unresolved on its own terms (though over-determined by B2); and the LS level remains
**UNVALIDATED** (§8.2 item 1, `docs/42` G4.2). The one evidentiary condition that *has* changed
is §4.2 item 5's: **all four levers now reach CITED**, which makes ADOPT-SOURCE **reachable** —
and reachable is not adopted.

---

## 2 — HYPOTHESES

**Five** hypotheses: one per lever (H-LIM, H-M, H-S), a joint cell (H-JOINT), and the `L` form
(H-L, §2.5). Each is stated so a measurement can refute it, with the refuting statistic named,
and each names the **grade** at stake (§4.1). Each has a **reading clause** (what the source
says — refutable by document evidence) and a **field clause** (what the swap does to our field —
refutable by recomputation).

> *Amendment (e), 2026-08-11: the draft added "and bounded" to "the refuting statistic named".
> **The bounds are gone** — see §2.0. Several clauses below are consequently **retired as
> refutation clauses** and restated as reported diagnostics or exact discriminators; each says so
> at its own site, and none is left to a later session's discretion. **§1.2 records what each
> already returned.***

### 2.0 How difference is adjudicated in this document — **there is no materiality bar**

> ### STRUCK, NOT RESCALED
> **The draft's materiality bar — `| ln f_A − ln f_B | > 0.1644 ln`, justified as *"the
> registered standard error of the fleet-mean level"* (σ_r 0.465 over n = 8) — is STRUCK at all
> fifteen of its sites, and is replaced by NO NUMBER.** Not by 0.6936, not by 0.4775, not by
> 0.3054, not by a bootstrap half-width, and not by a constant declared "explicitly
> non-statistical". **This document contains no statistical materiality threshold.** The
> decision and its full reasoning are `docs/52`; the falsification that forced it is
> `docs/47` §2.2 (D2) and `docs/48`.

**Why, in four lines** (`docs/52` §2, each ground measured or derived there, not asserted):

1. **Wrong error term.** Seven of the sites compare two **deterministic** field computations on
   the same DEM, minibacias, stations and days. By §6.1's own derivation both arms share their
   entire residual vector, so the sampling variance of the paired difference is **identically
   zero**. `SE = sd/√n` is the error term of an absolute, *unpaired* level.
2. **The premise was false, not just the number.** *"A difference smaller than the SE of the
   only fit that will ever consume it cannot change any downstream statement"* — but **the fit
   never consumes the LS level**: §8.1's design matrix has condition number = ∞, only Π is
   identifiable, and §4.3 states that a fit is *structurally incapable* of preferring one LS
   level over another. Detectability is exactly zero **at every noise level**, so no standard
   error bounds it. A level difference's consequence is **bookkeeping**, which has a *reporting
   precision*, not a noise floor.
3. **It adjudicated nothing.** Every comparison this document has actually made returns the
   identical verdict for any bar in **(0.0321, 0.2983)** — a factor of **9.29** — and 0.1644
   sits inside it (`docs/52` §1.2). It decided no evidence grade either: all four levers reached
   **CITED** from source text.
4. **No aggregate threshold composes.** At the station-bootstrap half-width 1.2833 every single
   lever is immaterial while the composition they belong to is material — five
   individually-immaterial choices composing to ×3.977 (`docs/52` §2.4). 0.1644 escaped this
   only by being ≈ 4× too small, which is an accident, not a defence.

**What adjudicates instead — four grounds, fixed here in advance, none of them tunable.** Each
clause below names the one it uses; **no clause is left to a later session's discretion.**

| # | ground | where it already lived | used by |
|---|---|---|---|
| **G-i** | **Source text with a grade.** A second admissible reading refutes a reading clause **irrespective of the factor it produces**; a single admissible reading with a page number is **CITED** | §4.1's ladder, §4.2 item 5 | (R1), (R6), (R9), the ADOPT-BAND trigger |
| **G-ii** | **The registered precedence rule:** *"`f_ero` decides; `f_area` is reported beside it, always, and can never override it"* | §3.3, unchanged | (R2), (R12) |
| **G-iii** | **Exact discriminators.** A lever is a pure *level* lever **iff its per-cell factor is constant**; an LS swap is a pure level change for the fit set **iff `Δ_shape` = 0** (to *reproduction* tolerance — §6.1) | §6.1's own derivation | (R7)/(R8), §6.1's branch |
| **G-iv** | **The exact measured ratio, printed at full precision, with a stated licence** — and never compared to a threshold | new; the honest form of what the bar was pretending to do | (R4), (R10), (R12), H-L |

**Prohibitions that travel with the striking** (`docs/52` §7, binding here):

- **"No bar" does NOT mean "the bar is zero" and does NOT mean "everything is material."**
  Deleting a comparison is not setting it to a limit. **Nothing may be declared material on the
  ground that it exceeds zero.**
- **No document downstream may quote a bar for this file** — not 0.1644, not 0.465, not 0.3054,
  not 0.4775, not 0.6936, not 0 — **or reconstruct one from this decision.** `docs/48` declined
  to propose a value on purpose; `docs/52` declines on the record.
- **§6.1's `Δ_shape` = 0 is NOT a materiality bar of zero.** It is a *structural* condition —
  *is this change a pure level change?* — and it never decides whether a difference matters.
- **Numeric tolerances that are NOT materiality bars are untouched**: `docs/49` gate 2,
  `report_h2e.py`'s `F = 0.25931` to 1e-8, the basin-erosion gate at 299.5387088405831 Mt/yr,
  the 3,266-day count. Those are **agreement tolerances on quantities that should be
  identical**. Also untouched, because they are outside this document: `docs/48` §3.3's Π
  reporting band, σ_r's valid use as an estimator-disagreement statistic, and G1.1 / G8 / G11 /
  G12's firing thresholds.

#### 2.0.1 BAR-DEPENDENT register — conclusions whose verdict turns on the struck bar

Registered under amendment (e) so a reader can see which way each would go under a different
threshold. **Wherever these conclusions appear — in this file or any other — they carry the
label.**

| # | conclusion | at the struck 0.1644 | under the seven admissible SEs (0.3054 – 0.6936) | at the bootstrap half-widths (0.8500 / 1.2833) | label |
|---|---|---|---|---|---|
| **1** | **(R10)** *"the levers interact, so decide them as a set"*, **as a statistical finding** | survives (0.2983 > bar) | **REVERSES on all seven** — smallest SE 0.3054, margin **2.4 %**, and 0.2983 lies inside the SE's own 95 % sampling interval on **5 of 7** | reverses | **BAR-DEPENDENT — verdict reverses.** *Superseded: §2.4 decides it by citation, which is bar-independent* |
| **2** | the bracket **WIDTH** 0.5410 ln is material | material | **material on 4 of 7, immaterial on 3** | immaterial on both | **BAR- AND CONSTRUCTION-DEPENDENT.** *Superseded: §1.0 — the span is the `L`-form lever (×1.7177) between a POINT and a documented hybrid, not an uncertainty interval* |
| **3** | the **single-lever MATERIAL verdicts** (`S` 0.5271, `L` form 0.5435, `m` step 0.6500, `m` cap 0.6588, and the refuted ×0.790 ratio 0.2357) | all material | ×0.790's 0.2357 goes immaterial at 0.4775; the other four at 0.6936 | all immaterial | **BAR-DEPENDENT** (`docs/48` §5.3) |
| **4** | `f_LS`'s **upper** endpoint (`\|ln\|` **0.8395**) is a material displacement from 1.0 | material | material on all | **immaterial at both** | **BAR-DEPENDENT at the widest constructions.** *The **DG endpoint 1.3805** is material on every construction ever proposed and is **NOT** bar-dependent* |
| **5** | §6.1's **Branch A/B** verdict | — | — | — | **BAR-DEPENDENT BY CONSTRUCTION while a threshold exists.** *Superseded by §6.1's exact discriminator; and the branch is over-determined by B2 regardless* |

**Explicitly NOT bar-dependent**, stated so nothing is over-read — immaterial at 0.1644 *and*
at every construction up to 1.2833: **(R4)** 0.0088 · **(R12)** 0.0248 / 0.0273 · **H-L** 0.0258
· **(R2)** 0.0321 · **Defect A** 0.00362 (upper) and 0.00101 (lower). Also not bar-dependent and
not statistical at all: **all four evidence grades (CITED)**; the **source-read-whole POINT** at
×0.25146; and **`docs/47`'s `C4.3-BLOCKED-UNTIL-LS-LANDS` verdict**, whose three propositions
are each width-independent (`docs/51` §6.3).

**Separately owed and NOT fixed by any choice of bar:** §6.2 **A5**'s *"minimum detectable
coefficient given the registered noise floor σ_r = 0.465 ln"* is **σ_r-dependent**, not
bar-dependent. σ_r = 0.465 is falsified as the per-station residual sd (`docs/47` §2.2 measures
1.9618; `docs/48` finds no admissible construction giving 0.465), and **no replacement number is
registered here** — `docs/48` §6.2 records three passes producing three different values for
that class of quantity (**O8 open**). A5 is amended accordingly at its own site.

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
- **(R1)** *(ground **G-i**, amendment (e))* a second admissible reading of pp. 94 / 121 is
  established from the source text, from Buarque's equations 13/15, or from another primary
  MGB-SED document (Fagundes 2018; the MGB-SED code, if obtained). **A second admissible
  reading refutes the reading clause irrespective of the factor it produces**, both factors are
  reported, and the outcome is **ADOPT-BAND** (§4.2), which carries both. **A reading
  disagreement is never "inside the bar" — there is no bar** (§2.0).
  *(Read out: does not fire. p. 94 + p. 98 are two independent sentences; single admissible
  reading ⇒ **CITED**, `docs/51` §1.2.)*
- **(R2)** *(ground **G-ii**, amendment (e))* — **retired as a refutation clause.** §3.3 already
  registers the precedence: **`f_ero` decides; `f_area` is reported beside it, always, and can
  never override it.** R2 becomes a **reported diagnostic**: print `f_ero(V1)`, `f_area(V1)` and
  their exact ratio, and **do not quote the proxy anywhere the exact value exists**. Any
  ×0.421-based load arithmetic published against the proxy is superseded by the exact re-run,
  not adjudicated against a threshold (`docs/35` §9.3.3 asks for exactly that re-run).
  *(Read out: `f_ero(V1)` = **0.362435** vs `f_area` 0.351, ratio **×1.0326**.)*
- **(R3)** some other single lever produces a larger |ln f| than the limiter on the exact
  re-run. *(This is a genuine possibility given Defect A: eq. 14 may move `m`'s factor toward
  1, but it cannot move the limiter's.)*
  *(Read out: does not fire. `|ln f|` on the exact re-run — limiter **1.0150**, `m` cap 0.6588,
  `m` step 0.6500, `L` form 0.5435, `S` 0.5271 (`docs/48` §5.3). **The limiter is the dominant
  lever**, and this clause is exact and threshold-free: it is an ordering, not a comparison to a
  bar.)*

**Grade at stake:** the limiter reaches **CITED** only if (R1) fails with a verbatim,
page-numbered quote and a single admissible reading. Otherwise **ASSUMED**.
**Read out ⇒ CITED**: p. 94 states the cap, and it is corroborated by a **second, independent
sentence on p. 98** (the same two-sentence device that settled `Sf`'s units on pp. 47–48), with
p. 121's *"limitado pela resolução de 500 m"* consistent with both. Single admissible reading
(`docs/51` §1.2; provenance `docs/38` §9.1). **Its consequence inside the source formulation is
load-bearing and is registered here:** under the cap, `a_in → 0`, so eq. 13 degenerates to
`L = (D / (22,13 · Xdir))^m` — **the source's own two statements composed** (§2.5.2).

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
- **(R4)** *(ground **G-iv**, amendment (e))* — **retired as a refutation clause.** H-M's field
  content is a **sign** prediction, and the sign test is **(R5)**, which is exact and
  threshold-free. The magnitude is **reported at full precision and compared to nothing**:
  `f(V2b)/f(V2a)` = **×1.008878** erosion-weighted (**×1.005212** area-weighted). The **reading**
  clause — eq. 14's step is not `min(m, 0.5)` — is independent of the magnitude, is **CITED**,
  and **stands**.
  > **⚠ This changes a label already written elsewhere** (`docs/52` §6, §8d). `docs/51` §3
  > records *"(R4) FIRES ⇒ H-M's field clause REFUTED"*, which was correct against the bar it
  > was measured against. **Under the struck bar, H-M's field clause is CONFIRMED on its sign**
  > and its magnitude is ×1.008878. Nothing downstream changes: the ×0.502 relabelling is owed
  > **anyway** (§7.3 item 2, `docs/51` §5.6b), because the label is wrong regardless of size.
- **(R5)** `f(V2b) < f(V2a)` on the basin area-weighted mean — the predicted **sign** is
  wrong. *(Sign is the load-bearing content here; the magnitude is not pre-registered because
  it depends on the basin's slope distribution below 9 %, which is not measured per-lever.)*
  *(Read out: does not fire — 0.522043 > 0.517480 ero, 0.505092 > 0.502472 area.)*
- **(R6)** `Sf` in eq. 14 is established from p. 46–48 to be slope in **degrees** or in
  **m/m**, not percent, in which case the step boundaries move and the whole clause is
  recomputed and this hypothesis is **withdrawn, not adjusted**.

> ### (R6) — **CLOSED, CITED. `Sf` IS SLOPE PERCENT.** *(amendment (d), `docs/51` §1)*
>
> The freezing condition of §9.1 item 2 — *"if the source PDF cannot be re-obtained, (R6) is
> unfalsifiable and the honest outcome is already NEGATIVE — UNRESOLVED for that lever"* —
> **did not fire. The PDF was obtained, it is on disk, it is hashed, and it was read.**
>
> Buarque (2015), printed **p. 47**, immediately under eq. (14), verbatim:
>
> > `m = 0,2 se Sf < 1` | `0,3 se 1 ≤ Sf < 3` | `0,4 se 3 ≤ Sf < 5` | `0,5 se Sf ≥ 5` **(14)**
> > — **onde `Sf` [%] é a declividade do pixel.**
>
> Corroborated by a **second, independent sentence** on printed **p. 48**, under eq. (18):
> `S_k = 65,41·sin²(θ_k) + 4,56·sin(θ_k) + 0,065` **(18)**, ***sendo θ o valor de `Sf` em
> graus*** — a conversion note that is only meaningful if `Sf` is **not** already in degrees.
> This is the same two-sentence device that settled the limiter (p. 94 + p. 98).
>
> **Honesty about the residue:** eq. (15) writes `Sf = √((∂z/∂x)² + (∂z/∂y)²)`, a
> **dimensionless** gradient — the ×100 is not written, and the source is internally loose. But
> the unit tag is explicit; the *degrees* reading is excluded by eq. 18's conversion note; and
> the *m/m* reading is excluded twice over, by the tag and because breakpoints at 1, 3 and 5
> **m/m** would be 100 %, 300 % and 500 % slopes. **Single admissible reading.**
>
> **Provenance card** (`docs/38` §9.1, which is the durable record):
>
> | | |
> |---|---|
> | reference | Buarque, D. C. (2015), doctoral thesis, IPH/UFRGS, 182 pp. |
> | repository | LUME/UFRGS, handle **`10183/129875`** |
> | local copy | **`data/raw/refs/buarque2015.pdf`** (gitignored), 9,646,521 bytes |
> | `sha256` | **`3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037`** |
> | page map | PDF p. 63 = printed p. 47 (eqs. 13–17); PDF p. 64 = printed p. 48 (eq. 18) |
>
> **Verify before quoting it:** re-hash and compare. A different hash is a different scan and
> the page numbers are then not guaranteed to point at the same equations.
>
> **Two consequences, both registered here:**
> 1. **The `m/m` sensitivity is STRUCK as retired.** `docs/49` §5.3's live risk — *"×0.329,
>    `|ln|` 1.1117, basin 51.4 Mt/yr, if `Sf` is m/m"* — **cannot occur** and may not be carried
>    as an open branch by any session. `scripts/c3/ls2d_variants.py:148`'s `sf = 100·tanθ` with
>    half-open 1/3/5 breakpoints is **the source's own unit and its own boundaries**, verified
>    line by line against the quote above.
> 2. **Every lever is now CITED** — limiter (p. 94 + p. 98), `m` (p. 47), `S` (p. 48), `L`
>    (p. 47, §2.5) — so **§4.2 item 5's evidentiary condition is met and ADOPT-SOURCE is
>    reachable.** *Reachable is not adopted*: §4.2's other conditions, including §3.3's full
>    stratified report, are **not** all discharged (§9.1 item 5).

**Grade at stake:** `m` reaches **CITED** only with eq. 14 transcribed verbatim, its `Sf`
units verified against the source text, and the step boundaries reproduced. **All three are
discharged above ⇒ `m` is CITED.** The **cap** — `min(m, 0.5)` — may **never** be graded CITED:
it is nobody's published formulation, and its mislabel is owed correction in five places
(§7.3 item 2).

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
- **(R7)/(R8)** *(ground **G-iii** + **G-iv**, amendment (e))* — **restated as an exact
  discriminator plus a report, not as threshold tests.** A lever is a **pure level lever if and
  only if its per-cell factor is constant**; any nonzero dispersion is shape content, at any
  size. What must be measured and printed, on our own slope field and on the §3.3 strata:
  1. the per-cell `S_WS78 / S_MB86` **range and monotonicity** over the basin's slope range —
     §3.4 derives ≈ **0.975 – 3.81**, non-monotone, which already answers the *iff*: **`S` is
     not a scalar**;
  2. the quantity that actually reaches the fit — the **per-station erosion-weighted factor
     dispersion**, `sd(ln)`, reported beside `docs/47` §4.4's measured **0.0769** (all 18) /
     **0.0868** (CAL 13) for the joint formulation;
  3. the stratified factors (lowland < 200 m / 200–1000 m / Andean > 1000 m) **beside** the
     basin factor 1.714, as numbers, with the spread printed.

  The conclusion is written as a measurement — *"the `S` ratio field spans ≈ ×3.9 over the
  basin's slope range and is non-monotone; `S` is not a scalar"* — never as a pass or a fail.
  *(**Not read out.** Items 1 is DERIVED-here from the two published formulas (§3.4); items 2–3
  on **our** slope field and strata **do not exist** — §1.2, `docs/51` §7 item 9. H-S is the one
  hypothesis in §2 that is still open on its field clause.)*
- **(R9)** `n = 1.3` in our own form is established from Moore & Burch (1986) or Mitasova
  et al. (1996) to be inadmissible for this terrain, or `scripts/c3/ls2d.py`'s stated
  justification (module docstring, "rill-dominated overland flow") is contradicted by a
  cited source. *(This is a reading test on **our** side, deliberately symmetric with R1.)*

**Grade at stake:** whichever `S` is adopted reaches **CITED** (both candidates are published
and page-citable). The *choice between them* is graded by rule §4.2, not by evidence about
`S` itself.
**Read out ⇒ the source's `S` is CITED**: Buarque eq. 18, printed p. 48, verbatim,
`S_k = 65,41·sin²(θ_k) + 4,56·sin(θ_k) + 0,065`, attributed in the source itself to
*"Wischmeier & Smith (1978)"* (`docs/51` §1.2). **This settles the *reading*, not the *choice***
— and it settles nothing about H-S's **field** clause, which remains the one part of §2 that is
**not read out** ((R7)/(R8) above).

### 2.4 H-JOINT — the joint cell (the three-lever composition, measured at ×0.421)

> The three levers must be decided **as a set**, because they interact: the naive product
> 0.302 is not the joint 0.421. The joint cell `V4 = buarque_2015` (limiter + **eq. 14 step**
> + W&S 78) is the registered-default outcome of `docs/35` §9.3.2 item 1, and its exact
> erosion-weighted re-run — not the area-weighted proxy — is what C4 and C5 would consume.

> **⚠ Corrected at the freeze (amendments (a), (d)):** `V4` is **not** "the source formulation".
> It is the source's **three** levers with **our** `L` — a documented **hybrid**. With eq. 13
> read verbatim (§2.5.2), the source formulation **read whole** is **`V4_dg`**, `f_ero` =
> **0.25146**, and it is a **POINT** (§1.0, §3.1). `V4` is retained as the registered upper end
> because `docs/35` §9.3.1, `docs/37` §4 candidate 0 and `docs/43` §1.4 all quote it and it must
> stay reproducible. Everything (R10)–(R12) says about deciding levers as a set applies to the
> **four**-lever formulation, not the three.

**Refuted if any of:**
- **(R10)** *(ground **G-i** + **G-iv**, amendment (e))* — **RETIRED as a refutation clause.**
  The clause conflated two different propositions, and only one of them was ever the question:

  | proposition | what decides it | status |
  |---|---|---|
  | the lever factors are **arithmetically** separable | measurement | **NO** — joint/product = **×1.34762**; a naive product understates the joint by 35 % |
  | the levers may be **methodologically** decided one at a time | the source, and §4.2 | **NO** — and this does not depend on the arithmetic |

  The second is settled **by the citation** and always was: eqs. 13, 14 and 18 plus the
  p. 94 / p. 98 limiter are **one formulation**, on two printed pages of one thesis, all four
  now **CITED**; read whole they are a **POINT** at ×0.25146 (§1.0). §4.2 item 1 registers
  fidelity to *the transposed **method***, not to a menu of levers, and item 2 requires **each**
  deviation to carry its own written source justification. `docs/47` §5.3 names lever-picking
  as the specific post-hoc hazard.

  > **What replaces (R10) — two statements, neither of which reads a threshold:**
  > 1. **A measured fact with a standing instruction.**
  >    `f(V4) / [f(V1)·f(V2b)·f(V3)]` = **×1.34762** (**×1.35949** with the `m` cap).
  >    ***Standing instruction: never quote a product of single-lever factors as the joint
  >    factor, in any document, table or notebook.***
  > 2. **An adoption rule, carried from §4.2 and not new here.** The formulation is **adopted
  >    whole or not adopted**; any single-lever deviation requires its own §4.2 item 2 written
  >    source justification, dated, before the resulting basin total is computed.
  >
  > **Even if the levers had multiplied out exactly, the answer would be the same.** Arithmetic
  > separability is not methodological separability. *(`docs/52` §3. This conclusion is
  > **BAR-INDEPENDENT**; the statistical version of it is register entry 1 in §2.0.1 and it
  > **reverses** under every admissible SE.)*
- **(R11)** the **exact** basin load under `V4` differs from `299.5387 × f_ero(V4)` — i.e.
  the linearity assumption itself fails. MUSLE is linear in LS **per cell**, so this can only
  fail through the aggregation path; if it fails, the failure is a defect in
  `load_geometry`/`SedGeometry`, and it must be reported as such rather than absorbed.
  *(Read out: does not fire — the exact-linearity route reproduces `f_ero(V4)` = **0.431944**
  against 0.43194, behind a basin-erosion gate at 299.5387088405831 Mt/yr, `docs/49` gate 2.)*
- **(R12)** *(ground **G-ii**, amendment (e))* — **retired as a refutation clause**, on the same
  ground as (R2): §3.3 already registers that **`f_ero` decides and `f_area` can never override
  it**. R12 becomes a **reported diagnostic** — print `f_ero(V4)`, `f_area(V4)` and their exact
  ratio, and never quote the proxy where the exact value exists. The *"≈ 104.8 Mt/yr"* published
  by `docs/35` §9.3.3 and `docs/37` §4 against the proxy is superseded by the exact re-run
  (§1.0, §3.5), not adjudicated.
  *(Read out: **×1.02484** at the upper endpoint, **×1.02771** at the DG endpoint, against
  `docs/47` R7's separately measured proxy bias 1.0251 / 1.0278 — consistent to 4 s.f.)*

### 2.5 H-L — the `L` form (the ×0.790 that produces the lower end of the bracket)

Registered as a **fifth** clause even though it is not one of the three levers named in the
task, because the published bracket's lower end (×0.333, "3.00×") depends on it and §1.1
Defect B shows it is currently confounded.

> Isolating the literal Desmet & Govers (1996) finite-difference `L` (their eq. 11 =
> Buarque's eq. 13) **with `S` held at ours** (`V5`) gives a factor that differs from the
> published 0.790, because 0.790 also swaps `S` from Moore & Burch to McCool (1987) and was
> measured on the uncapped `ls2d` rather than on `ls2d_hs`.

**Refuted if** *(ground **G-i** + **G-iv**, amendment (e))* **the published 0.790 is shown to
isolate the `L` form.** That is the whole content of the clause and it is threshold-free: the
question was never *how big* the discrepancy is, but *whether 0.790 is the object it is labelled
as*. It is not. The exact factorisation is
**0.790 = 0.852262 (`L` form) × 0.926925 (`S` swap)**, measured on the wrong column (`ls2d`, not
the engine's `ls2d_hs`), and the split is effectively unique. **H-L is therefore NOT refuted.**

The basin-scale agreement `| ln f(V5) − ln 0.790 | =` **0.0258** is **reported and is not the
test**. It measures only that the *stated* `S` confound is small at basin scale — 8 % of the
move — while the **column** confound, **0.887977** (`|ln|` 0.1188), is the larger of the two,
and neither is the reason ×0.333 fails (§1.1 Defect B: the `L`-form ratio is
**formulation-dependent**, 0.852262 / 0.769833 / **0.580685**, and was composed across
formulations as a scalar).

#### 2.5.1 The mandatory re-derivation — **re-hung on a trigger that can fire** *(amendment (c))*

> **The draft attached this obligation to the clause *"if H-L is not refuted"*. That trigger
> could not do the job it was written for**, and freezing it would have frozen a rule that does
> the opposite of what it says. It is replaced, unconditionally:
>
> **The published bracket ×0.333 – ×0.421 and every statement derived from it — *"our LS is
> 2.37× – 3.00×"*, *"α reference ≈ 3.9 – 5.0"*, *"band ≈ 2.0 – 9.9"*, *"hard stop ≈ 11.8 –
> 14.9"*, and the *"≈ 104.8 Mt/yr"* / *"≈ 126.1 / ≈ 99.7 Mt/yr"* proxy loads — ARE
> SUPERSEDED BY MEASUREMENT (§1.0) AND MUST BE RE-DERIVED AND RE-QUOTED WHEREVER THEY APPEAR,
> as dated corrections, never as silent edits.** The obligation is unconditional because its
> ground is a measurement that has already landed, **not** the survival or refutation of any
> hypothesis.
>
> **Where they appear** (the list is the register, not a suggestion): `docs/35` §9.3.1;
> `docs/37` §1 table, §4 candidate 0 and A2.2; `docs/43` §1.4 and §3.x; `docs/45` §2.1;
> `src/nbgen/make_nb18.py`; `src/nbgen/make_nb19.py`. **This document enacts none of them** —
> each is owed to its own owner's amendment slot (§7.3), and the `docs/37` corrections travel
> with the enactment amendment `docs/37` §A3 (`docs/51` §5.3, §7 item 4).

#### 2.5.2 Eq. 13 read verbatim — the `L` lever and its `Xdir` factor, **CITED** *(amendment (d))*

`docs/50` flagged an open convention risk: *"the D&G aspect term `x^m` is worth ×1.149 on the
lower endpoint on a convention that is UNVERIFIED while D&G (1996) is unobtained."* **That flag
is CLOSED — against the transposed source itself**, not against D&G. Buarque (2015), printed
**p. 47**:

> `L_k = [(Am_k + Lp_k²)^(m+1) − Am_k^(m+1)] / [Lp^(m+2) · Xdir_k^m · (22,13)^m]` **(13)**
> …*"O fator de direção `Xdir` … igual a 1 quando a direção entre eles é ortogonal, ou igual a
> 2^(1/2) quando a direção é diagonal."*

`scripts/c3/ls2d_defect_b.py:146` and `scripts/c3/ls2d_variants.py:186-190` both carry
`x_aspect ** m` in **exactly that denominator position**, verified line by line. **Grade: CITED.**
D&G (1996) remains unobtained (`docs/47` O1) **and does not need to be**: §4.2 item 1 registers
fidelity to *the transposed method*, and the transposed method states the convention on its own
printed page.

**Consequence, and it is the one that matters most in this file:** with eq. 13 on p. 47 in print
there is **no admissible reading of Buarque in which `L` is our point-rate form**. That is what
collapses the source formulation, read whole, to a **POINT at ×0.25146** (§1.0), makes ×0.43194 a
**documented hybrid** rather than a bracket end, and makes the 0.5410 ln span **the `L`-form
lever** rather than an uncertainty interval. Under the p. 94 / p. 98 one-pixel cap `a_in → 0`, so
eq. 13 degenerates to `L = (D / (22,13 · Xdir))^m` — **the source's own two statements composed**,
not a choice made here (`docs/47` §4.3's caveat, carried).

---

## 3 — EXACT DEFINITIONS (no choice left to the measuring session)

### 3.1 The variants, named — and nothing is overwritten

`src/mgb_sediment.py:load_geometry` already takes `urh_ls2d=` and `ls2d_column=` as
parameters (verified at `src/mgb_sediment.py:863–864`), so every variant is reachable **by
name** without touching a default — the same discipline as `volume_convention`,
`k_unit_system` and `cp_revision`.

> **⚠ AMENDMENT (b), 2026-08-11 — V4 AND V4′ WERE SWAPPED IN THE DRAFT, AND THE TABLE BELOW IS
> THE CORRECTED ONE.** The draft's row labelled the **cap** composition (V4′) as *"the ×0.421 row
> as published"*. It is the other way round: **the published ×0.421 row is V4 — the eq. 14
> STEP** — proved by its area-weighted counterpart reproducing the published number to **15
> significant figures** (16.775413430326214, `docs/51` §2.2). **V4′ (the cap composition) had
> NEVER been measured** before 2026-08-11. This is the correction that keeps the frozen table
> from mislabelling its own reproducibility anchor, and it is why Defect A contaminated the
> **single-lever label only** and never the joint (§1.1).

| id | name | definition (all at native 90 m, `ls2d_hs`'s own 1 km² channel cap unless stated) | measured |
|---|---|---|---|
| **V0** | `ours_2026_08` | as built: upslope area ≤ 1 km², continuous McCool-89 `m`, `(sinθ/0.0896)^1.3`, `n = 1.3` — **the current engine input**, `urh_ls2d.csv:ls2d_hs` | 1.000 by definition |
| **V1** | `lim_pixel` | V0 with **slope length ≤ one DEM pixel** | `f_ero` **0.362435** · `f_area` 0.3513 |
| **V2a** | `m_cap05` | V0 with `m → min(m, 0.5)` — **the variant actually measured as the published ×0.502**, and **nobody's published formulation** (§2.2) | `f_ero` **0.517480** · `f_area` 0.502472 |
| **V2b** | `m_step_eq14` | V0 with `m →` Buarque **eq. 14 step function** — *this is the source's `m`* | `f_ero` **0.522043** · `f_area` 0.505092 |
| **V3** | `s_ws78` | V0 with `S → 65.41 sin²θ + 4.56 sinθ + 0.065` | `f_ero` **1.694054** · `f_area` 1.7139 |
| **V4** | `buarque_2015` | V1 + **V2b** + V3 — the source's three levers with **our** `L`. **THIS is the ×0.421 row as published** (area-weighted proxy), and the **upper end of the registered bracket** — a documented **hybrid**, not the source read whole | `f_ero` **0.431944** · `f_area` **0.421475** |
| **V4′** | `buarque_2015_cap` | V1 + **V2a** + V3 — the **cap** composition. **Never measured before 2026-08-11**; kept only so the cap stays reachable by name. It is **not** the published row | `f_ero` 0.43038 · `f_area` 0.42070 |
| **V4_dg** | `buarque_2015_dg` | V1 + V2b + V3 + **eq. 13's finite-difference `L`** — **the source formulation READ WHOLE**, and the **lower end of the registered bracket** (§1.0's POINT) | `f_ero` **0.25146** · `f_area` **0.2446790094097074** |
| **V5** | `L_dg96_fd` | V0 with the literal D&G finite-difference `L`, **`S` held at V0's** (isolates the `L` form; see Defect B) | `L`-form ratio **0.769833** on `ls2d_hs` (0.852262 uncapped, **0.580685** inside the source formulation) |

*(The `measured` column is the **read-out** (§1.2), added at the freeze. It records what has been
measured; it adopts nothing. `f_ero` decides and `f_area` is the proxy — §3.3. The lower end's
`f_ero` rests on **one** engine re-run; the second reproduction is owed, `docs/51` §7 item 7.)*

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

### 3.5 Re-based expected consequence — stated before the re-run, **and now superseded by it**

`docs/35` §9.3.3 registered the expected consequence against the **prior** C level
(248.730 Mt/yr, `cp_revision='prior_2026_08_11'`). The adopted level is now **299.5387
Mt/yr** (`docs/37` A1.3, ×1.20427 erosion-weighted). Re-based, using the published proxy
factors and the same arithmetic:

| adopted variant | proxy factor | basin load (proxy) | against the 144–184 Mt/yr outlet anchors |
|---|---|---|---|
| V0 (today) | 1.000 | **299.5387 Mt/yr** | above both |
| **V4′ / V4** | 0.421 | **≈ 126.1 Mt/yr** | **below both** |
| V4 + literal `L` | 0.333 | **≈ 99.7 Mt/yr** | **further below both** |

> **⚠ SUPERSEDED BY THE EXACT RE-RUN — amendment (a), 2026-08-11.** The table above was written
> *before* the re-run, on the **area-weighted proxy** factors, and is retained only so the
> superseded numbers are identifiable. The registered figures are the **erosion-weighted engine**
> ones (`docs/47` §4.3, `docs/51` §2.1), and **`f_ero` decides** (§3.3):
>
> | adopted variant | `f_ero` | basin load (engine) | against the 144–184 Mt/yr outlet anchors |
> |---|---|---|---|
> | **V0** (today) | 1.000 | **299.5387 Mt/yr** | above both |
> | **V4** — the hybrid, upper end | **0.43194** | **129.3840 Mt/yr** | **below both** |
> | **V4_dg** — the source read whole, the POINT | **0.25146** | **75.3235 Mt/yr** | **further below both** |
>
> The proxy is **2.5 % low** on both ends (`docs/47` §3.1 R7), which is why the proxy loads read
> ≈ 126.1 / ≈ 99.7 against the exact 129.3840 / 75.3235 — the upper end moves little, the lower
> end moves a great deal, and **the lower end's move is Defect B's, not the proxy's** (§1.1).
> The `docs/23` §13.2 **yield embargo** is in force: these are absolute flux, model-internal.

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

5. **The adopted formulation must reach grade CITED on ALL FOUR levers** — the limiter, `m`,
   `S` **and the `L` form** — verbatim, page-numbered, single admissible reading, `Sf` units
   verified, before any default is switched.
   > *Amendment (d), 2026-08-11: the draft said "all three levers", written before eq. 13 was
   > read. `L` is a lever — it is worth the entire 0.5410 ln span of §1.0 — so requiring it is
   > the restrictive direction and the honest one. **All four are now CITED*** (limiter p. 94 +
   > p. 98 · `m` p. 47 · `S` p. 48 · `L` p. 47), ***so this condition is MET and ADOPT-SOURCE is
   > REACHABLE — which is not the same as adopted*** (§1.2, §9.1 item 5).

| outcome | condition | what it licenses | what it does NOT license |
|---|---|---|---|
| **ADOPT-SOURCE** | **all four levers CITED** (met, §4.2 item 5); H-M's **(R6) not triggered** (met — `Sf` is percent, §2.2); the §3.3 exact re-run completed **and reported, including the stratified report**; the §4.3 forbidden evidence untouched | proposing the adopted variant as the engine default in a *separate*, dated amendment owned by whoever owns `scripts/c3/ls2d.py` and `docs/37` — **`docs/37` §A3** (`docs/51` §5.3); α band rescaled per item 3; every prior variant still reachable by name | it does **not** validate the LS level (still **UNVALIDATED**), does not close C3 clause 2 on its own, does not change Π's *status*, and does not license re-fitting anything to the new level without §6 |
| **ADOPT-BAND** | *(amendment (e), ground **G-i**)* **≥ 1 lever CITED but ambiguous — i.e. two admissible readings survive on the source text.** The trigger is **the existence of a second admissible reading, period, whatever the gap between the factors it produces.** There is no threshold on that gap and none may be introduced | adopting the **lower-LS** reading under item 4, **and** carrying `f_LS` as an explicit **band** (both readings) through C4, C5 and every load table | it does **not** license choosing the reading that lands the load nearer an anchor, and does not collapse the band for convenience anywhere downstream |
| **NEGATIVE — UNRESOLVED** | ≥ 1 lever with **no citable ground either way**, or (R6) fires, or the source text cannot be obtained/verified | **§7**: publish the negative result; keep V0 as the default *because it is incumbent, not because it won*; carry the full bracket as a declared uncertainty on Π's decomposition | it does **not** license silence, does not license quoting a single `f_LS` anywhere, and does not license C4/C5 proceeding as if the level were settled |

**Three notes on this table, registered at the freeze:**

- **ADOPT-BAND is not currently triggered on any lever.** All four are CITED with a **single**
  admissible reading (§1.2). **Carrying a band is never the unsafe direction; collapsing one is**
  — and item 2 above already forbids collapsing for convenience.
- **`[0.25146, 0.43194]` is NOT an ADOPT-BAND band and may not be presented as one.** It is a
  **POINT** (the source read whole, ×0.25146) beside a **documented hybrid** (×0.43194, the
  source's three levers with *our* `L`), and the span between them is the `L`-form lever (§1.0,
  §2.5.2). An ADOPT-BAND band would be two admissible *readings of the source*; this is one
  reading plus a retained legacy composition. `docs/47` §6.2 item 2 already provides for the
  point case — *"unless C3.1 collapses it to a point, in which case the adopted point and its
  grade travel instead."*
- **Reachable ≠ exercised.** No outcome in this table has been taken. §3.3's **full stratified
  report** is not discharged — elevation strata exist for every variant, **slope terciles do
  not**, and the per-station erosion-weighted `LS̄` exists only as ratios (`docs/47` §4.4) — and
  it is required before ADOPT-SOURCE is *exercised*, though not before this freeze
  (`docs/51` §7 item 9).

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

> **⚠ THE HONEST STATE OF THIS GUARANTEE AT THE FREEZE, and it is the sharpest cost of the
> read-out (§1.2).** The re-runs **have already been made** and the basin totals under every
> variant **are already on the record** — 299.5387 (V0), 129.3840 (V4), 75.3235 (V4_dg) Mt/yr,
> §3.5. **No session can now write a §4.2 justification "before the total was computed"**, and
> **no session may claim to have done so.** What survives, and what the enacting session is
> bound by instead:
> 1. **The variant and its §4.2 justification are still written first — before ADOPTION**, in
>    `docs/37` §A3, dated, with the journal sentence changed to the one that is true: *"this
>    decision is recorded before any default was switched, and after the basin totals under
>    every variant were already published in `docs/47` §4.3, `docs/49`, `docs/50` and
>    `docs/51`."*
> 2. **§4.3 still binds absolutely.** The totals being known is exactly why *"the basin total,
>    the outlet anchors, or the distance between them"* may not be used — and why the
>    justification must be a **source reading with a grade**, checkable against the printed page,
>    which is the one kind of evidence that a known total cannot contaminate.
> 3. **`docs/47` §5.3's post-hoc hazard is SHARPENED, not relieved, by everything settled here.**
>    With all four levers CITED and the source read whole a single point, the temptation to pick
>    among levers is replaced by a **binary** choice — "the source read whole" (×0.25146) versus
>    "the hybrid" (×0.43194), worth ×1.7177 — which is *easier* to make post-hoc, not harder.
>    The enacting session must state which it adopted **and why, from the source**, and must
>    state it knowing that both totals are already published.

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

> ### THE DISCRIMINATOR IS EXACT, NOT A THRESHOLD *(amendment (e), ground **G-iii**)*
>
> | condition | branch |
> |---|---|
> | **`Δ_shape` = 0** — to the engine's *reproduction* tolerance, in the sense of `docs/49` gate 2 and `report_h2e.py`'s 1e-8, **not** a materiality bar | the LS swap is a **pure level** change for the fit set → **Branch A is available** |
> | **any `Δ_shape` > 0** | the swap moves the fit set's stations **relative to each other** → it is a **shape** change → **Branch B is MANDATORY (B1)** |
>
> **`Δ_shape` remains MANDATORY to compute and to record** before C3.1 reports (`docs/47` O6,
> §6.3), **blinded until computed**, and **reported at full precision as a diagnostic**, with
> the sentence: *"the fit is recoverable by rescaling `α̂` if and only if `Δ_shape` = 0 exactly;
> the measured value is X, and the re-run is owed."*
>
> **Why the exact form and not a number** (`docs/52` §4; none of these reasons touches
> `Δ_shape`'s value, which was unseen when this was decided):
> 1. **It is this section's own derivation, not an import.** The paragraph below already says
>    *"the fit is not recoverable by rescaling — it must be re-run"* for **any** relative
>    movement. The threshold was a softening of a statement that is exact.
> 2. **It can only tighten, never loosen.** §6 was accepted as strictly more restrictive than
>    `docs/45` §6.1 (`docs/51` §5.4); this is more restrictive still, so **no frozen
>    registration is relaxed.** *(The freezing session accepts the tightening explicitly — §9.1
>    item 4.)* The checkable asymmetry: **`Δ_shape` = 0 never opens Branch A where
>    `Δ_shape ≤ 0.1644` would have closed it.**
> 3. **It cannot be tuned, now or later.** A future session cannot choose a threshold after
>    seeing the number, because there is no threshold to choose.
> 4. **It costs nothing that is live.** **B2 makes Branch B mandatory regardless of `Δ_shape`**
>    (`docs/47`, `docs/51` §5.4), so the branch is already over-determined and what this site was
>    protecting is protected twice over.
>
> **Bounds that are already published, and they are NOT a substitute for computing it:**
> per-station erosion-weighted LS ratios under the source formulation span **1.287×**
> (`docs/47` §4.4), so `Δ_shape ≤ ln 1.287 = 0.2523`; normalising the all-18 extremes (0.3687,
> 0.4745) on the basin joint factor 0.43194 gives ≈ 0.154. **It must be computed, not inferred**
> (`docs/51` §5.4). Under the exact discriminator the *branch* no longer depends on where it
> lands — the **record** does.
>
> *(Under the struck bar this site was the most dangerous one in the file: a **wider** bar
> **opened** Branch A and let C4.3 start. Under the exact discriminator **no choice of number
> opens anything**, which is what makes §6.1 consistent with **A6** — "no rescaling in place of
> a re-run".)*

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

Available **only** if **`Δ_shape` = 0** (§6.1, amendment (e)), and **only** with all six of:

- **A1.** Every C4.3 artifact is labelled **PROVISIONAL — LS FORMULATION UNRESOLVED**, in the
  file, in the table, and in the notebook cell. It is not C4's verdict.
- **A2.** *(corrected by amendment (a))* The run card declares `ls_formulation = ours_2026_08`,
  grade **UNVALIDATED**, with the registered bracket **×0.25146 – ×0.43194** (erosion-weighted;
  area proxy ×0.24468 – ×0.42148) printed beside it, together with the sentence *"a later LS
  adoption multiplies α̂ by **2.3151× – 3.9768×** and leaves Π unchanged"* **and** the sentence
  *"the source formulation read whole is a **point** at ×0.25146; ×0.43194 is a documented
  hybrid that keeps our `L`"* (§1.0). **The superseded ×0.333 – ×0.421 / "2.37× – 3.00×" may not
  be printed on a run card.**
- **A3.** **The ADOPT outcome of `docs/45` §6.1 is not reachable.** Its conditions (2) and
  (3) and its `FAIL — RAILED / HARD STOP` row read α̂ against **3.9 / 35.4**, which is an
  LS-conditional band (`docs/37` §4 candidate 0). A provisional fit may return **ADOPT-PENDING
  at most**. *(This does not amend `docs/45`; it is strictly more restrictive, and every
  `docs/45` condition continues to apply.)*
- **A4.** **The α̂ stops — BOTH ENDS.** *(arithmetic corrected by amendment (a); the lower stop
  added on `docs/51` §5.4)*
  - **Upper stop.** If the provisional fit returns **α̂ ≥ 7.54**, the verdict is **blocked**
    until LS lands. Derivation, not a guess: the registered α box is **[2.0, 30.0]**
    (`docs/45` §2.1); a later adoption multiplies α̂ by `1/f ∈ [2.3151, 3.9768]`;
    `30.0 / 3.9768 = 7.543`, so any α̂ above 7.54 **may** put the equivalent source-LS optimum
    outside the registered box, and above `30.0 / 2.3151 = 12.958` it **certainly** does.
    *(The draft's 10.0 / 12.63 were computed on the superseded `1/f ∈ [2.375, 3.00]` and are
    void. The corrected upper stop is **lower**, i.e. **more** restrictive.)*
  - **Lower stop.** If the provisional fit returns **α̂ ≤ 2.10** (= `2.0 × 1.05`), the verdict is
    **blocked** until LS lands — the symmetric statement, and the one the measurement says will
    actually fire: `docs/47` §5.4 measures the optimum at the **bottom** of the box
    (α̂ 0.26 – 1.29 across the β gate), not the top, so the upper stop is moot **in the direction
    written** and the box's *floor* is the live boundary. `2.0 / 2.3151 = 0.864` and
    `2.0 / 3.9768 = 0.503`, so an α̂ at or below ≈ 2.1 is already at or under the box floor once
    the level factor is applied in either direction of the bracket.
  - A fit whose equivalent lies outside its own registered box is not a fit that can be
    re-expressed — it needs a **new pre-registration**, not a re-run.
- **A5.** **G4.1 runs and is reported** (the `ln LS̄_i` coefficient in the joint regression,
  with its 95 % station-bootstrap interval, and the **minimum detectable coefficient** given the
  noise floor and the ln `LS̄` range 1.12). If **G4.1 fires**, the verdict is blocked —
  `docs/42` G4.1's ACTION on FAIL is to fix the field, never α.
  > **⚠ σ_r = 0.465 IS FALSIFIED AND IS STRUCK FROM THIS CLAUSE** *(amendment (e); this is
  > **σ_r-dependent**, not bar-dependent)*. `docs/47` §2.2 (D2) measures the per-station residual
  > sd at **1.9618 ln**, and `docs/48` finds **no admissible construction** on which 0.465 is
  > that quantity. **No replacement number is registered here**: `docs/48` §6.2 records three
  > passes producing three different values for this class of quantity (**O8, open**). The
  > requirement therefore becomes procedural and is **strictly more onerous**: the C4.3 session
  > **names the noise-floor construction it uses**, prints it beside the minimum detectable
  > coefficient, and cites the document that registers it. **A minimum detectable coefficient
  > computed against 0.465 is void** and may not be reported.
- **A6.** **No rescaling in place of a re-run.** No C4.3 statement may convert its result to
  another LS by multiplying α̂ by `1/f`. Rescaling is arithmetic on the *level*; the adoption
  changes the *shape* too, and A1's provisional label exists precisely because the re-run is
  owed.

### 6.3 Branch B — C4.3 must wait until LS lands

**Mandatory** if **any** of:

- **B1.** *(amendment (e))* **`Δ_shape` > 0** — any relative movement at all (§6.1).
- **B2.** The C4.3 session intends to issue a **final** verdict — i.e. anything other than
  PROVISIONAL — because ADOPT is unreachable under A3.
- **B3.** G4.1 has fired in any prior run on the V0 field.
- **B4.** The LS decision is expected to change the **`m` step-vs-cap** answer (H-M) or the
  **`L` form** answer (H-L), both of which are shape levers and both of which are currently
  *unmeasured*: a fit run under an LS whose own definition is in flux is a fit to an unnamed
  object.
  > *Read out, 2026-08-11: both answers have since landed — `m` is the **step** (×1.008878 off
  > the cap, `docs/49`) and the `L` form is **formulation-dependent** and worth the whole 0.5410
  > ln span (`docs/50`, §1.1). B4 is therefore **discharged on its stated ground** and is no
  > longer the reason to wait; **B2 is** (`docs/47` reached Branch B independently on B2 plus
  > the box-boundary argument). Recorded rather than deleted, because a frozen clause is amended
  > in the open, not quietly.*
- **B5.** The freezing of this document is already scheduled — in which case waiting costs
  what §6.4 measures and nothing else. *(Read out: this document froze on 2026-08-11, and the
  enactment amendment `docs/37` §A3 is still unwritten, so B5 continues to hold until it is.)*

> **Standing verdict at the freeze, carried and not created here:** `docs/47`'s
> **`C4.3-BLOCKED-UNTIL-LS-LANDS`** holds, on **B2** plus the box-boundary argument, and it is
> **independent of the bracket's width** — `docs/51` §6.3's three propositions (the unit; the
> rail measured at `f_LS` = 1; the post-hoc hazard) each survive the corrected bracket, and even
> **collapsing the bracket to its point** leaves the registered search railing in **two of the
> three** G2.3 β corners (α̂-equivalents 1.026 / 2.485 / 5.126 against a box floor of 2.0 and a
> hard stop of 3.9, `docs/51` §6.2). **Freezing this document is not that verdict's unblocking
> event; the enactment amendment `docs/37` §A3 is** (`docs/51` §7 item 4).

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
2. *(re-hung UNCONDITIONAL by amendment (c) — the draft read "if H-M is not refuted")* **The
   ×0.502 row's label *"his eq. 14"* is WRONG and must be corrected** in `docs/35` §9.3.1,
   `docs/37` §4 candidate 0, `docs/43` §1.4, `src/nbgen/make_nb18.py` and `make_nb19.py`. The
   measured object is `min(m, 0.5)`; **eq. 14 is ×0.505092 area-weighted / ×0.522043
   erosion-weighted** (`docs/49`). The obligation does **not** depend on H-M's fate: the label
   is wrong regardless of the size of the difference, and `min(m, 0.5)` may never be graded
   CITED (§2.2).
3. *(re-hung UNCONDITIONAL by amendment (c) — the draft read "if H-L is not refuted")* **The
   ×0.790 / ×0.333 bracket and everything derived from it are SUPERSEDED BY MEASUREMENT (§1.0,
   §2.5.1) and must be re-derived** in the same five places plus `docs/45` §2.1 and `docs/37` §1's
   table. The ground is a landed measurement, **not** the survival of a hypothesis.
4. `docs/42` §9 still owes the transcription of `docs/43` §3.1's P1/P2/P3 (recorded in
   `docs/45` §0 as outstanding; unrelated to LS but in the same amendment slot).
5. *(added at the freeze)* **The enactment amendment — `docs/37` §A3, dated**, written by the
   C3.1 owner: `ls_formulation` and its grade, the §4.2 outcome, the α band rescaled per §4.2
   item 3, every variant still reachable by name, and `docs/37` §1's table and §4 candidate 0
   corrected off *"2.37× – 3.00×"*. **This, not this document's freeze, is `docs/47`'s B1
   unblocking event** (`docs/51` §5.3, §7 item 4).
6. *(added at the freeze)* **`Δ_shape` must be computed and recorded BEFORE C3.1 reports**, so
   it cannot be read backwards (`docs/47` O6, §6.3; `docs/51` §7 item 5). Minutes of work.
7. *(added at the freeze, verifications and explicitly NOT blockers)* a **second
   erosion-weighted reproduction of the lower endpoint** `f_ero(V4_dg)`, which currently rests
   on one engine re-run (`docs/51` §7 item 7); and durable provenance records for `ah703.pdf`,
   `md1988/89` and `fagundes2018.pdf`, on the model of `docs/38` §9.1's Buarque card
   (`docs/51` §7 item 8).

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
precisely because the alternative is that a **2.3151×–3.9768×** factor stays hidden inside a product
nobody can decompose.

---

## 9 — REGISTRATION CARD — **FROZEN (READ OUT)**

| | |
|---|---|
| **Status** | **FROZEN (READ OUT) — IN FORCE** |
| **Frozen** | **2026-08-11**, by the **`amend-46`** session (`docs/agents/journal_amend-46.md`) |
| Drafted | 2026-08-11, by the `ls-prereg` agent (`docs/agents/journal_ls-prereg.md`) |
| Amended before freezing | `docs/51` §5.6 items **(a)–(e)**, enacted in full; item (e) per the bar decision `docs/52` §6, at **all fifteen** sites |
| Sections frozen on that date | **§1–§8** |
| Amendment slot | **§10 — OPEN** |
| **Why "READ OUT"** | **four of §2's five hypotheses had already been measured before the freeze** — H-LIM (R1/R2/R3), H-M (R4/R5/R6), H-JOINT (R10/R11/R12), H-L — by the variants harness, `docs/49` and `docs/50`. The read-out is printed in **§1.2**. **H-S's field clause (R7/R8) is the one that is NOT read out.** This document may not be cited as an open pre-registration of §2 |
| **What is still prospective** | **§4**'s decision rule and grade requirement · **§6**'s C4.3 gate · **§7**'s negative-result pre-commitment. **§4.2's outcome is unexercised** and the LS level remains **UNVALIDATED**. `Δ_shape` was blinded when §2.0 and §6.1 were decided and landed the same day — **§10, amendment 1** |
| **Materiality bar** | **STRUCK, NOT RESCALED, and replaced by no number** (§2.0; decision `docs/52`; falsification `docs/47` §2.2 D2 + `docs/48`). Bar-dependent conclusions are registered in **§2.0.1** |
| **Enactment owner** | **`docs/37` §A3**, dated, written by the **C3.1** owner (`docs/51` §5.3; `docs/37` A2.2 assigns the LS-shape decision to C3.1 by name, and `scripts/c3/ls2d.py` + `data/processed/urh_ls2d.csv` were delivered under C3.1 by commit `5eaabf5`). **That amendment, not this freeze, is `docs/47`'s B1 unblocking event.** This document is **not** that amendment and switches no default |
| **Frozen artifacts touched** | **none.** `data/processed/sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv, q_gauge_H2E.npz, q_gauge_H2E.csv, report_H2E.json, metrics_fleet.csv}`, `data/processed/urh_ls2d.csv` and `minibacia_ls2d.csv` were **not opened for writing**. No engine default moved (`ls2d_column`, `cp_revision`, the unit conventions, the H2E parameters are untouched); no calibration launched, no fit performed, no simulation run, no LS pass run, no `data/` product written |
| Numbers computed by the draft itself | **two derivations only**, both from published formulas with no project data: the `S`-factor pointwise ratios (§3.4) and the `m` step-vs-cap divergence (§1.1) |
| Numbers added at the freeze | **none computed here.** Every figure in §1.0, §1.2, §2.0.1, §2.2, §2.5, §3.1, §3.5 and §6 is **carried and cited in place** from `docs/47` §3.1/§4.3/§4.4, `docs/48` §2.4/§5.3, `docs/49`, `docs/50`, `docs/51` §1–§6 and `docs/52` §1–§6. The only arithmetic performed at the freeze was **re-verification** of `11.8·f`, `35.4·f`, `5.9–23.6·f`, `1/f`, `299.5387·f`, `ln(0.43194/0.25146)`, `30.0/3.9768` and `30.0/2.3151` against the values those documents publish |
| Everything else | carried from `docs/33`, `docs/35`, `docs/37`, `docs/38` §9.1, `docs/40`, `docs/41`, `docs/42`, `docs/43`, `docs/45`, `journal_decide-ls-resolution`, `journal_c31-ls2d`, and read-only inspection of `scripts/c3/ls2d.py` and `src/mgb_sediment.py` — cited in place |
| Embargo | `docs/23` §13.2 in force — absolute flux only (t/day, Mt/yr); **no t/km²/yr** may be produced by any LS variant table |

### 9.1 What the freezing session settled — the four conditions, answered

The draft required these to be settled *before* freezing rather than rubber-stamped. Each is
answered here, with the document that answers it.

1. **Defect A and Defect B — RESOLVED BY MEASUREMENT, not inherited.** *"Explicitly inherited"*
   was **not an available option**: the draft's Defect A text predicts a direction now measured
   as immaterial, and its Defect B text gives a diagnosis now measured as **wrong** (the stated
   `S` confound is 8 % of the move; the column confound is larger; and the real mechanism is
   that the `L`-form ratio is formulation-dependent). Inheriting them would have frozen two
   falsified paragraphs. **§1.1**, primary records `docs/49`, `docs/50`, `docs/51` §3–§4, each
   behind reproduction gates with `urh_ls2d.csv` / `minibacia_ls2d.csv` SHA-256-checked
   unchanged before and after by the measuring scripts themselves.
2. **`Sf` units — VERIFIED, verbatim, page-numbered, single admissible reading.** `Sf` is slope
   **percent** (p. 47, corroborated p. 48). The pre-committed **NEGATIVE — UNRESOLVED** branch
   for the `m` lever **did not fire**; the PDF is on disk, hashed, with its LUME handle, and
   durably recorded in `docs/38` §9.1. **§2.2**, `docs/51` §1. This is the single largest change
   between draft and freeze: it converts the `m` lever from unfalsifiable to **CITED** and
   retires the ×0.329 m/m risk.
3. **Enactment owner — `docs/37` §A3**, dated, written by the C3.1 owner. See the card above.
   `docs/37` is the file that carries the closure conjunction whose clause 2 the adoption
   discharges, and whose §1 table and §4 candidate 0 still print *"2.37× – 3.00×"* — one
   amendment does both jobs.
4. **§6's gate — ACCEPTED as more restrictive than `docs/45` §6.1, and TIGHTENED FURTHER.** It
   removes ADOPT from a provisional C4.3 (A3) and every `docs/45` condition continues to apply,
   so no frozen registration is relaxed. `docs/47` reached **Branch B** independently on B2 plus
   the box-boundary argument, so accepting §6 creates no conflict. **The freezing session
   additionally and explicitly accepts three tightenings**, each strictly restrictive:
   §6.1's `Δ_shape` = 0 exact discriminator (replacing `≤ 0.1644`); A4's corrected upper stop
   **7.54** (was 10.0) plus the added symmetric lower stop **2.10**; and A5's striking of
   σ_r = 0.465 in favour of a **named** noise-floor construction. *(`docs/51` §5.4's "accept it,
   unchanged" is thereby amended **in the restrictive direction only** — `docs/52` §4.)*

### 9.2 What this freeze does NOT do — stated so nothing is over-read

- It **adopts no variant**, switches **no engine default**, and exercises **no §4.2 outcome**.
- It does **not** validate the LS level. **`docs/42` G4.2 stands: the level is UNVALIDATED and
  must be printed that way.** *Cited is not validated* (`docs/37` A1.6 item 3), and *fitted is
  not validated either* (`docs/43` §3.3 item 1). Raising four levers to **CITED** raises their
  **provenance** grade and nothing else.
- It does **not** unblock C4.3. `docs/47`'s **`C4.3-BLOCKED-UNTIL-LS-LANDS`** holds, is
  bar-independent, and is unblocked by the **enactment amendment**, not by this freeze.
- It does **not** close C3. Clause 2 of `docs/37` A1.1's conjunction needs the *shape* decision;
  settling LS is **necessary and not sufficient** (§8.2 item 6).
- It settles **nothing** about `α = 11.8`'s like-for-likeness with a 2-D contributing-area LS —
  **NOT SETTLED**, no band offered (§1.0, `docs/47` §4.2 item 6).

## 10 — Amendment slot — **OPEN from 2026-08-11**

§1–§8 are frozen. Changes to them are made **here**, dated, by this document's owner, and never
by silent edit. A session that believes a rule in §1–§8 is wrong **journals the objection and
follows the rule anyway** until an amendment is written.

### Amendment 1 — 2026-08-11 — **`Δ_shape` is COMPUTED. The branch is B.**

**Record only. No rule in §1–§8 is changed by this amendment**; §6.1's discriminator and §6.3's
B1 are applied exactly as frozen, and the result is entered here because §9's card, written
minutes earlier, says `Δ_shape` was blinded — which was true when §2.0 and §6.1 were decided and
stopped being true the same day. **Source: `docs/53_delta_shape_pretest.md`** (`delta-shape`
agent, process record `docs/agents/journal_delta-shape.md`), which computed it on the registered
configuration behind six reproduction gates plus a null control, and did not edit this file.

> ### `Δ_shape` = **0.1299456916752905**
>
> Registered reading — variant **V4**, weights normalised over the **18 usable** SSC stations,
> maximum over the **CAL 8**. Argmax **`24037390` CAPITANEJO**; smallest CAL station
> `26127010` EL ALAMBRADO AUT at **0.0179854753**. **No CAL station is invariant.**
>
> **VERDICT — `Δ_shape` > 0 ⇒ BRANCH B IS MANDATORY (§6.1 as frozen, §6.3 B1.)** In §6.1's own
> required words: *"the fit is recoverable by rescaling `α̂` if and only if `Δ_shape` = 0
> exactly; the measured value is **0.1299456916752905**, and the re-run is owed."*
>
> **It is not near zero.** The null control — a *uniform* LS factor, the exact case Branch A
> exists for — returns **2.2204460492503136e-16**, one machine epsilon. The measured value is
> **5.9 × 10¹⁴** times that and **1.3 × 10⁷** times `report_h2e.py`'s 1e-8 reproduction gate,
> which §6.1 names as the tolerance meant. Under all thirty measured readings of §6.1's
> under-specified definition the statistic lies in **[0.0159907, 0.1638779]** — **every one > 0
> by fourteen orders of magnitude, and the branch is the same under every reading.**

> ### ⚠ THE ORDERING FACT THIS AMENDMENT EXISTS TO PUT ON THE RECORD
> **Under the STRUCK 0.1644 bar this measurement would have returned the OPPOSITE verdict.**
> Every V4-family reading is **≤ 0.1644** — the largest, 0.1638779, by a margin of **0.0005221**
> (**0.3 %**). The struck bar would have said *"Branch A is available; C4.3 may start"*; the
> exact discriminator says *"Branch B is mandatory."*
>
> §2.0's striking of the bar and §6.1's discriminator were decided **before this number existed
> and blind to it** (`docs/52` §9: *"`Δ_shape` is unmeasured and unseen by this pass"*), and
> `docs/52` §4 stated its own asymmetry in advance — *"`Δ_shape` = 0 never opens Branch A where
> `Δ_shape ≤ 0.1644` would have closed it."* **This is the case that makes the asymmetry bite,
> and it bites on a 0.3 % margin.** Recorded here so that the ordering is checkable by anyone,
> and so that no later reader has to take it on trust: had the bar survived, C4.3 would have been
> licensed to start on a 0.3 % margin in a threshold whose own derivation was falsified.
>
> *(The branch was over-determined anyway — **B2** makes Branch B mandatory regardless, and
> `docs/47` reached Branch B independently. This changes no verdict. It changes what the record
> shows about how close the struck bar came to changing one.)*

**Two open items discharged by the same run, recorded here rather than left dangling:**

1. **`docs/47` O6 / `docs/51` §7 item 5** — *"run §6.1's `Δ_shape` pre-test before C3.1 reports,
   so it cannot be read backwards"*. **Discharged**, and the ordering holds: it was computed
   after this document froze and after `docs/52` decided the discriminator, and before C3.1
   reports or any enactment amendment exists.
2. **`docs/51` §7 item 7 / §1.0 residue 2 / §3.1's note** — the **second, independent
   erosion-weighted reproduction of the lower bracket endpoint**. **Discharged**: by a different
   aggregation route, `f_ero(V4_dg)` = **0.2514648985839397** (against the registered 0.25146),
   with `f_area(V4_dg)` = **0.24467900940970733**. §1.0's residue 2 and §3.1's *"rests on one
   engine re-run"* note are **satisfied** — the lower endpoint now has two erosion-weighted
   measurements and three area-weighted ones. *(The residue is struck by this amendment; residues
   1 and 3 of §1.0 — our terrain data, and `α = 11.8`'s like-for-likeness — **stand
   unchanged**.)*

**What this amendment does NOT do:** it adopts nothing, moves no default, exercises no §4.2
outcome, and does not unblock C4.3 — Branch B is *mandatory*, which is the blocking direction.
The enactment amendment (`docs/37` §A3) remains unwritten and remains `docs/47`'s B1 event.

---

*(Further amendments go below this line, dated, most recent last. Where obligations are owed to
**other** owners rather than to this slot: the enactment is **`docs/37` §A3**; H-S's field clause
(R7)/(R8) and §3.3's slope-tercile stratified report are owed before ADOPT-SOURCE is exercised;
and §7.3 is the standing register of everything else.)*

### Amendment 2 — 2026-08-12 — **`f_area(V4)` is 0.42136300143291305, not ×0.42148 / 0.421475; and §1.0's `= −ln 0.580685` identity does not hold**

**Record and correction. No rule in §1–§8 is changed by this amendment, and no hypothesis, grade,
outcome or gate moves.** Written by the `defect-farea-amend` session (process record
`docs/agents/journal_defect-farea-amend.md`), which owns `docs/51` and this slot and nothing else.
The companion record, with the full weighting table and the reproduction commands, is **`docs/51`
§9 amendments 1 and 2 (2026-08-12)**. `docs/46` §1–§9 were **not** opened for writing.

---

#### (i) The two body cells that are corrected

| site in §1–§8 (unchanged there; corrected here) | as printed | **corrected** |
|---|---|---|
| **§1.0** — the registered statement, *"Area-weighted proxy **[0.24468, 0.42148]**"* | ×0.42148 | **0.42136300143291305** |
| **§1.0** — the table row *"upper end (`f` nearest 1) … ×0.42148 area"* | ×0.42148 | **0.42136300143291305** |
| **§3.1** — the **V4** row's `measured` cell, *"`f_ero` 0.431944 · `f_area` **0.421475**"* | 0.421475 | **0.42136300143291305** |
| **§6.2** (:1037) — *"area proxy ×0.24468 – ×0.42148"* | ×0.42148 | **0.42136300143291305** |
| **§2.2** (:271, the (R12) read-out row) and **§2.5** (:617) — *"×1.02484 (upper)"* | ×1.02484 | **×1.025111777659529** |

**Not corrected, because they are already right** — stated so nothing is over-corrected:

- **the DG / lower endpoint** `f_area(V4_dg)` = **0.2446790094097074** (`ls2d_defect_b.json`,
  `decomposition.V4dg_over_V0`) and its (R12) ratio **×1.02771** are on the registered support
  already. *(§10 amendment 1 prints 0.24467900940970733 from its own aggregation route; that is the
  same value to 16 significant figures — the two differ by **one unit in the last place**, 2.8e-17.
  Both stand.)*
- **§2.0.1's and `docs/52` §5's abs-ln register "(R12) 0.0248 / 0.0273"** — measured on the
  registered support: **0.024801658019852884** → 0.0248, and **0.027336745312405174** → 0.0273. On
  the wrong support the upper figure would be 0.0245. **§2.0.1 needs no change**, and that is a
  third independent internal vote for the corrected value.
- **every erosion-weighted number in this document.** `f_ero(V4)` = 0.43194417543884817 and
  `f_ero(V4_dg)` = 0.2514648985839397 are untouched, so §1.0's **registered statement
  `f_LS ∈ [0.25146, 0.43194]` erosion-weighted, `1/f_LS ∈ [2.3151, 3.9768]`, the α reference
  11.8·f = 2.967–5.097, the `docs/35` §6.1 band, the 35.4·f = 8.902–15.291 hard stop, the
  `docs/45` box ·f, and the basin loads 129.3840 / 75.3235 Mt/yr ALL STAND EXACTLY AS FROZEN.**

---

#### (ii) The measurement behind it

**§3.3's registered definition is the deciding text**, and it names a support:

> `f_area(V) = basin area-weighted mean of LS(V) / basin area-weighted mean of LS(V0)   [the PROXY]`

read with §1's own read-out — *"Measured 2026-08-11 … on all **30,235,916** basin cells at 90 m,
with a harness that reproduces our own `ls2d_hs` area-weighted mean **39.812** bitwise"*. **The
"basin area-weighted mean" is the per-cell basin mean, over 30,235,916 cells and
256,702.3554292511 km².** Hence

> ## `f_area(V4)` = 16.775413430326214 / 39.812260149274394 = **0.42136300143291305**
> `1/f_area(V4)` = **2.3732506095678505**. Area-weighted proxy bracket:
> **[0.2446790094097074, 0.42136300143291305]**.

Recomputed 2026-08-12 from `data/processed/urh_ls2d_variants.csv` (read-only; sha256
`81d2376ac11978391612bfe39483113b321c327752392fba10e5d3e91471ddc0` re-checked unchanged after,
together with `urh_ls2d.csv`, `minibacia_ls2d.csv` and `sim_calibrated_v2/h2e_drivers.npz`) under
**every** defensible weighting, plus the two published per-cell means and an elevation-strata
recomposition — the full six-row table is `docs/51` §9 amendment 1. The three decisive rows:

| support | `f_area(V4)` | note |
|---|---|---|
| **per-cell basin, 30,235,916 cells** (`ls2d_variants_summary.json:ratio_to_V0`, and independently `ls2d_defect_b.json:decomposition.V4_over_V0` = 0.42136300143291344, and independently the strata recomposition = 0.4213630014329133) | **0.42136300143291305** | **§3.3's quantity** |
| `urh_ls2d_variants.csv` weighted by its own `area_km2` | 0.4213519856784954 | −2.61e-05 |
| engine `urh_fractions.csv`×`minibacias.csv` areas, 32,782 units, 257,096.93 km² (`ls_defect_a.json:f_area_urhfrac_areas`) | 0.4214751420286394 | **+2.661377371648382e-04** |

**Where ×0.42148 came from — reconstructed bitwise, and it is NOT an arithmetic error.** It is
`scripts/c3/ls_erosion_weights.py`:166 with `a = geom.cell_area_km2` from
`src/mgb_sediment.load_geometry`: the **engine's own URH-fraction areas**, a different area source
that `load_geometry` itself warns *"differ[s] by more than 5 % on 12.9 % of cells … basin totals
257097 vs 251724 km²"*. A 2026-08-12 re-run reproduced all eight of that JSON's
`f_area_urhfrac_areas` values exactly. **So ×0.42148 is a correctly computed quantity on a
different support, correctly named in its own JSON key — it is simply not §3.3's `f_area`.** The
two artifacts are consistent with each other and **neither needs editing; no regeneration was
run.**

**The deciding independent check — `docs/47` §3.1 R7's separately measured proxy bias 1.0251:**

| `f_area` used | `f_ero(V4)/f_area(V4)` | abs-diff vs R7's 1.0251 |
|---|---:|---:|
| **per-cell basin 0.42136300143291305** | **1.025111777659529** | **1.1777659529199624e-05** |
| engine 0.4214751420286394 | 1.0248390293193077 | 2.609706806921963e-04 |

**R7 confirms the corrected value 22× more closely.** The DG pair gives
0.2514648985839397 / 0.2446790094097074 = **1.0277338427624152** (×1.0277138223121467 with the
rounded 0.25146) against R7's 1.0278. **The bracket's two ends had been printed on two different
supports; only the upper one was off.** `docs/49`:154 and `docs/50`:244,274 were already right.

---

#### (iii) §1.0's `L`-form identity — false as written, and why

§1.0's third bullet reads: *"the span between them is the `L`-form lever, exactly:*
`ln(0.43194 / 0.25146) = 0.5410 = −ln 0.580685`*"*. Re-verified 2026-08-12:

| quantity | value |
|---|---:|
| `ln(0.43194 / 0.25146)` | **0.5410027585442313** |
| `−ln(0.580685)` | **0.543546837831505** |
| **gap** | **0.0025440792872737372 ln** (a factor 1.0025473) |
| `exp(−0.5410027585442313)` | **0.5821641894707599** — so 0.5410 pairs with **0.58216** |

**Both constituents are separately true; the identity mixes two supports.**

| span | value | its `L`-form ratio inside the source formulation |
|---|---:|---:|
| **erosion-weighted** `ln(f_ero(V4)/f_ero(V4_dg))` | **0.5410027585442313** (rounded inputs) · 0.540992944828321 (exact) | **0.5821641894707599** · 0.5821699026927624 (exact) — independently measured at **0.5822 erosion-wtd** by `docs/agents/journal_ls-impact.md`:105 |
| **area-weighted** `ln(f_area(V4)/f_area(V4_dg))` | **0.5435475125003637** | **0.580684608230046** = `ls2d_defect_b.json:decomposition.L_form_inside_source` (0.5806846082300454, ln −0.5435475125003647); `docs/50`:275 prints this row's ln width as 0.54355, correctly |

> **The corrected identity, as §1.0's bullet must be read:** *the span between the POINT and the
> hybrid is the `L`-form lever, exactly, on each support —* **erosion-weighted**
> `ln(0.43194/0.25146) = 0.5410027585442313 = −ln 0.5821641894707599`; **area-weighted**
> `ln(0.42136300143291305/0.2446790094097074) = 0.5435475125003637 = −ln 0.580684608230046`.
> **0.580685 is the AREA-weighted ratio and belongs with 0.54355, not with 0.5410.**

§1.0's **conclusion is unaffected**: the span is the `L`-form lever between a POINT and a
documented hybrid, and **not** an uncertainty over readings of the source. So is §2.0.1 row 2's
label, whose *"Superseded"* clause rests on exactly that conclusion. The **registered ln width
0.5410** in §1.0's table is the erosion-weighted span and **stays as frozen.**

---

#### (iv) Does anything move? — No, and the licence is named, not a threshold

**`docs/46` §2.0 ground G-iv** (*the exact measured ratio, printed at full precision, with a stated
licence — and never compared to a threshold*). The corrections are
**2.661377371648382e-04 relative / 2.661023287994224e-04 ln** on `f_area(V4)`, and
**0.0025440792872737372 ln** on the identity. **Neither number is the reason nothing moves**, and
**no materiality bar is invoked, rescaled, imported or reconstructed** — §2.0's striking stands and
this amendment introduces no fourth uncited band.

What licenses "no verdict moves" is that **no rule in force reads either quantity**:

1. **Ground G-ii, §3.3's registered precedence** — *"`f_ero` decides; `f_area` is reported beside
   it, always, and can never override it."* `f_ero` does not change, so nothing that `f_ero`
   decides can change. §1.0's registered erosion-weighted bracket, `1/f_LS`, and every α rescaling
   are erosion-weighted throughout.
2. **Ground G-i, §4.2's decision rule and §4.1's grade ladder** — decided by source text with a
   page number. All four levers stay **CITED**; the ADOPT-SOURCE outcome recorded in `docs/37` A3
   is unaffected, as is the `ls_formulation` = `buarque_2015_dg` naming.
3. **Ground G-iii, §6.1's discriminator** — `Δ_shape` is per-station and erosion-based and reads
   neither `f_area` nor either span. **`Δ_shape` = 0.1299456916752905 and BRANCH B (amendment 1)
   are untouched**, as are §6.3's B1 obligations and the mandatory re-run.
4. **(R12) is a reported diagnostic, not a gate** — §2.4 and `docs/52` §6 both say so. Its
   restatement from ×1.02484 to ×1.025111777659529 changes a printed diagnostic and nothing else,
   and it moves it **toward** `docs/47` R7's independent measurement.
5. **§7's negative-result pre-commitment, §8's non-identifiability declaration and §5's
   immovables** read none of these numbers.

Unchanged for the same reasons: the basin gross-erosion gate **299.5387088405831 Mt/yr**; the two
endpoint loads **129.3840 / 75.3235 Mt/yr**; the joint/product **×1.34762** and the
erosion-weighted lever product; §1.1's Defect A figures (0.00362 / 0.00101) and Defect B's 0.307
and ×1.326; and `docs/47`'s **`C4.3-BLOCKED-UNTIL-LS-LANDS`** verdict, whose three propositions are
width-independent. **The LS level remains UNVALIDATED** (`docs/42` G4.2) — this amendment corrects
a proxy's arithmetic and validates nothing.

---

#### (v) Owed to other owners, reported not fixed

1. **`docs/47` §4.3's area-weighted column prints 0.42135** for this cell. That is **not** a
   rounding of the corrected value — 0.42136300143291305 both rounds *and* truncates to 0.42136 at
   five decimals. It reconstructs as the **`urh_ls2d_variants.csv` `area_km2` weighting**,
   0.4213519856784954 → 0.42135 (equal to `urh_table_check`'s V4/V0 level ratio
   0.42135198571912497). The same table's DG cell prints **0.24466** where the registered value is
   0.2446790094097074 (→ 0.24468). **So `docs/47` §4.3's area column is a third support**, owed to
   `docs/47`'s owner, and it changes no `docs/47` verdict (all three propositions are erosion-side).
2. **`docs/52` §6:371's ×1.02484 (upper)** — same restatement as §(i) above; owed to `docs/52`'s
   owner. **`docs/52` §5:78 and §5:343's 0.0248 / 0.0273 are already correct and must not be
   touched.**
3. **The JSON artifacts are correct and were not edited; no producing script was run.** The one
   code-level defect found is documentary: `scripts/c3/ls_erosion_weights.py`:174 prints its GATE-2
   column header as a bare `f_area` with no support tag beside `f_ero`, which is the plausible
   channel by which the engine-support number reached `docs/51` §2.2 as *"`f_area(V4)`"*. A
   one-word header fix (`f_area_urhfrac`), or printing §3.3's per-cell value alongside. Owed to
   `scripts/c3/`'s owner.

**Disclosure.** No engine default was changed (`ls2d_column`, `urh_ls2d`, `cp_revision`,
`volume_convention`, `k_unit_system`, α, β and every H2E parameter untouched); no fit, no
calibration, no `KGE_ln` evaluation, no α̂ quoted; no committed data product regenerated or
hand-edited; no git command run. `urh_ls2d.csv`, `minibacia_ls2d.csv`, `urh_ls2d_variants.csv` and
`sim_calibrated_v2/h2e_drivers.npz` were SHA-256'd before and after and are **UNCHANGED**. Files
written by this session: **`docs/51`** (four strike-through pointers plus a new §9 amendment slot),
**this §10 amendment**, and its journal. **§1–§9 of this document were not touched.** The `docs/23`
§13.2 yield embargo is in force; no t/km²/yr appears here.
