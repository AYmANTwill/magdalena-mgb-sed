# 49 — Defect A resolved: the label is wrong, the number is not

**Written 2026-08-11** by the `defect-a` agent (process record:
`docs/agents/journal_defect-a.md`). This document does **one** job: settle **Defect A** of
`docs/46_ls_preregistration_DRAFT.md` §1.1 — *the row published as ×0.502 and labelled "`m`
hard-capped at 0.5 (his eq. 14)" is a **cap**, while eq. 14 is a **step function*** — with
measurements, so that `docs/46` can be frozen or amended on evidence instead of inherited.

**Scope, stated first.** It edits nothing frozen. `docs/35`, `docs/37`, `docs/42`, `docs/43`,
`docs/45`, `docs/46` and `docs/47` were read and **not** edited; §6 records what is *owed* to
their owners and enacts none of it. No default moved: every variant is reached **by name**
through `ls2d_column=` / the variant CSV, exactly as `docs/46` §3.1 requires. No calibration was
launched, no α̂ fitted or quoted, no git command run (§7).

---

> ## THE VERDICT
>
> **Defect A is REAL as a *reading* defect and IMMATERIAL as a *level* correction, and the
> joint ×0.421 row never carried it at all.**
>
> | | published | **corrected, this run** | |
> |---|---:|---:|---|
> | **(a)** eq. 14's `m` lever | ×0.502 — *which is the cap* | **×0.5051** area-wtd · **×0.5220 erosion-wtd** | `\|ln f(V2b) − ln f(V2a)\| = 0.0052` area / **0.0088** erosion, against the 0.1644 bar |
> | **(b)** the joint source formulation | ×0.421 | **×0.42136** area-wtd · **×0.43194 erosion-wtd** | the published ×0.421 **already used the step** — it is V4, not V4′ |
> | **(c)** how far our LS sits above the source | 2.37× – 3.00× | **2.3151× – 3.9768×** (`docs/47` §4.3) | Defect A's own share of the move at the ×0.421 end is **−0.36 %** (2.3235× → 2.3151×) |
> | **(d)** below the 5 % breakpoint | — | **30.51 % of basin AREA · 0.729 % of basin EROSION** | below the true cap/step crossover (8.9333 %): **37.86 % of area · 2.14 % of erosion** |
>
> **(e) One-line verdict.** The published **×0.421 is not wrong** — it is the step function, and
> exactly it is ×0.43194 erosion-weighted (the ×0.421 is the area-weighted proxy, 2.5 % low);
> the published **bracket 2.37×–3.00× is wrong, corrected to 2.3151×–3.9768×**, but **none of
> that correction is Defect A's** — Defect A is worth **0.36 %** at that end, i.e. **+0.018 on
> the α reference (5.079 → 5.097)**, which is **45× inside** the materiality bar `docs/46` §2
> registers. **This defect turned out not to matter to the level. It matters to the label:**
> the ×0.502 row is `min(m, 0.5)`, which — as `docs/46` §2.2 says — is nobody's published
> formulation and may never be graded CITED.

**And the thing that does matter, found while measuring the thing that does not:** eq. 14's
`Sf` **units** — `docs/46` (R6), still unverified against Buarque pp. 46–48 — are worth
**×0.329** on this lever if the reading is m/m (§5.3). The open question about `m` is the
units, not the cap.

---

## 1 — What was measured, and the two gates it passed first

`scripts/c3/ls_erosion_weights.py` (new; read-only on everything it touches). It does three
things and nothing else:

1. runs `src/mgb_sediment.simulate_sediment` at **adopted defaults** (`SedParams()` =
   α 11.8, β 0.56, FG 1.0, `williams_m3`, `us_customary`, `cp_revision='cited_central_2026_08_11'`)
   on the frozen H2E drivers, and keeps the **per-(minibacia, URH) decade gross erosion** `E_u`;
2. converts the `f_area` **proxy** of `data/processed/urh_ls2d_variants.csv` into the **exact**
   `f_ero` that `docs/46` §3.3 says decides;
3. makes one per-cell pass over all **30,235,916** basin cells at 90 m — reusing
   `scripts/c3/ls2d.py`'s own DEM, slope, pit filling, D8, flow accumulation, URH grid and cell
   geometry **by import** — accumulating area and `Σ LS·w` per (minibacia, URH) **per eq.-14
   slope class**.

**Gate 1 — basin gross erosion at adopted defaults.** Measured **299.5387088405831 Mt/yr**
against `docs/37` A1.3's **299.5387** (difference 8.8 × 10⁻⁶). **PASS.**

**Gate 2 — the erosion-weighted factors must reproduce the four already published in
`docs/47` §4.3**, which were obtained by an independent agent through an actual engine re-run on
a rebuilt LS field:

| variant | this run `f_ero` | `docs/47` §4.3 | gate |
|---|---:|---:|---|
| V1 `lim_pixel` | 0.362435 | 0.3624 | **PASS** |
| V2a `m_cap05` | 0.517480 | 0.5175 | **PASS** |
| V3 `s_ws78` | 1.694054 | 1.6941 | **PASS** |
| V4 `buarque_2015` | 0.431944 | 0.43194 | **PASS** |

**Why `f_ero` computed this way *is* the re-run and not an approximation.** MUSLE is linear in
LS per cell (`src/mgb_sediment.cell_static_factor`) and the daily runoff-energy term is
identical for every cell of a minibacia (`mini_static_factor`), so `E_u(V)/E_u(V0) =
LS_V(u)/LS_V0(u)` exactly and `f_ero = Σ_u E_u · (LS_V/LS_V0)_u / Σ_u E_u`. Gate 2 is the
empirical check on that algebra: it reproduces four independently re-run numbers to 5 × 10⁻⁴.
The same linearity distributes a unit's erosion over its 90 m cells in proportion to `LS_j w_j`,
which is what makes §4's erosion split exact rather than modelled.

`data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv`, `sim_calibrated_v2/h2e_drivers.npz` and
`parameters_H2E.csv` were SHA-256'd before and after by the script itself: **UNCHANGED**.

---

## 2 — (a) The corrected lever factor for Buarque eq. 14

| id | what it is | `f_area` | `f_ero` | basin Mt/yr |
|---|---|---:|---:|---:|
| **V2a** `m_cap05` | `m → min(m_cont, 0.5)` — **the row published as ×0.502** | 0.502472 | **0.517480** | 155.005 |
| **V2b** `m_step_eq14` | eq. 14's step 0.2 / 0.3 / 0.4 / 0.5 on `Sf` < 1 / 1–3 / 3–5 / ≥ 5 % | **0.505092** | **0.522043** | 156.372 |

**The corrected factor for "Buarque eq. 14" is ×0.5051 area-weighted, ×0.5220
erosion-weighted.** Against the published ×0.502:

| comparison | \|ln ratio\| | vs the 0.1644 bar |
|---|---:|---|
| V2b vs V2a, area-weighted | 0.00520 | **32× inside** |
| V2b vs V2a, erosion-weighted (the deciding statistic) | **0.00878** | **19× inside** |
| V2b (`f_ero`) vs the number as printed, 0.502 | 0.03915 | 4× inside |

**Clause outcomes, now on `f_ero` and not on the proxy** (`docs/46` §2.2):

- **(R4) FIRES.** `|ln f(V2b) − ln f(V2a)| = 0.0088 ≤ 0.1644`. **H-M's field clause is
  REFUTED**: at basin scale the cap and the step are the same object, and the published ×0.502
  stands as eq. 14's factor to within four times the bar's own resolution.
- **(R5) does not fire.** The predicted **sign is right**: `f(V2b) > f(V2a)` on both weightings.
- **The reading clause survives untouched.** `min(m, 0.5)` is still nobody's formulation; the
  *label* is the defect, and §6 lists the five places that carry it.
- **(R3) survives.** Erosion-weighted, the limiter is still the largest single lever:
  `|ln f_ero|` = limiter **1.0149** > `m` cap 0.6588 ≈ `m` step 0.6500 > `S` 0.5271 >
  `L` form 0.2656. Correcting Defect A does not reorder the levers.

---

## 3 — (b) The corrected joint factor — and a swap that must be fixed before `docs/46` freezes

| id | what it is | `f_area` | `f_ero` | basin Mt/yr |
|---|---|---:|---:|---:|
| **V4** `buarque_2015` | limiter + **eq. 14 step** + W&S 78 — the source formulation **as read** | **0.421363** | **0.431944** | **129.384** |
| **V4′** `buarque_2015_cap` | limiter + **cap** + W&S 78 | 0.420704 | 0.430381 | 128.916 |

**The corrected joint source-formulation factor is ×0.42136 area-weighted, ×0.43194
erosion-weighted.**

> **The published ×0.421 was already the step.** `journal_decide-ls-resolution` §3b's joint row
> prints **16.775**, and 16.775413 is V4 — the step. V4′, the cap joint, is 16.749164 and had
> **never been measured** until now. The same journal's *single-lever* row (20.005) **is** the
> cap. **That table mixes the two objects: its `m` row is `min(m, 0.5)`, its joint row is
> eq. 14.** Only the single-lever row was ever contaminated by Defect A.

**Consequence for `docs/46`, and it is a freezing-blocker.** `docs/46` §3.1 labels **V4′** *"the
×0.421 row as published, kept so the prior number stays reproducible"*, and §1.1 infers from
that labelling that *"the joint ×0.421 is a plausible over-statement"*. Both are wrong in the
same way: **V4 is the reproducibility anchor, V4′ is the object that had never been measured.**
A freezing session that does not fix §3.1 freezes a table that mislabels its own anchor.
(Independently reached by the `ls-variants-harness` agent from the same measurement.)

Defect A's counterfactual worth at the joint — i.e. what would have changed had the joint
*really* used the cap:

| | area-weighted | erosion-weighted |
|---|---:|---:|
| V4 (step) ÷ V4′ (cap) | ×1.001567 | ×1.003631 |
| `\|ln\|` | 0.001566 | **0.003625** — **45× inside the bar** |

**(R10) does not fire, on either weighting and with the corrected step.** Naive product vs
joint: area 0.30421 vs 0.42136 (`|ln|` **0.3262**); erosion 0.32053 vs 0.43194 (`|ln|`
**0.2983**). Both about twice the bar. *"The levers interact and must be decided as a set"*
(`docs/35` §9.3.1, `docs/37` §4, `docs/43` §1.4) **survives the correction of eq. 14** — it was
a losable prediction and it held.

**(R12) does not fire either.** `f_ero(V4)` 0.43194 vs `f_area(V4)` 0.42136: `|ln| = 0.0248`,
6.6× inside the bar. The proxy `docs/35` §9.3.3 and `docs/37` §4 published is **2.5 % low**
(`docs/47` §3.1 R7, reproduced here) but it is **not refuted as a proxy**. Same for **(R2)**:
`f_ero(V1)` 0.362435 vs the published 0.351, `|ln| = 0.0313`.

---

## 4 — (d) The measurement that decides it: area is not erosion

**A lever that acts only on low-slope cells is worth what those cells erode, not what they
cover.** This is `docs/37` line 206's distinction, and it is the reason Defect A collapses.

Measured on all 30,235,916 basin cells; the erosion column is exact by the linearity of §1, at
adopted defaults, over 2009-01-01…2018-12-31:

| slope class (`Sf` = 100 tan θ) | cells | area km² | **% of area** | Mt/yr | **% of erosion** | LS̄ (V0) |
|---|---:|---:|---:|---:|---:|---:|
| < 1 % | 3,972,161 | 30,188.4 | 11.993 | 0.123 | **0.041** | 0.034 |
| 1 – 3 % | 3,736,147 | 30,797.7 | 12.235 | 0.779 | **0.260** | 0.350 |
| 3 – 5 % | 1,889,825 | 15,808.1 | 6.280 | 1.282 | **0.428** | 1.404 |
| 5 % – 8.9333 % | 2,198,820 | 18,502.3 | 7.350 | 4.228 | **1.411** | 4.998 |
| ≥ 8.9333 % | 18,438,963 | 156,427.0 | 62.142 | 293.128 | **97.860** | 64.374 |
| **below 5 %** | 9,598,133 | **76,794.3** | **30.507** | **2.183** | **0.729** | |
| **below the crossover** | 11,796,953 | **95,296.6** | **37.858** | **6.411** | **2.140** | |

**The 5 % breakpoint is not actually the boundary of Defect A, and the true boundary is
computed, not guessed.** The cap `min(m_cont, 0.5)` binds only where the continuous `m` exceeds
0.5, which is the root of `sin θ / 0.0896 = 3 sin θ^0.8 + 0.56`: **tan θ = 0.08933250413265519
(8.9333 %)**, solved to 1e-15. Two facts fall out of the pass and are stated because they are
measured, not assumed:

- **below the crossover the cap does literally nothing** — `Σ LS_V2a·w` equals `Σ LS_V0·w` to
  the last digit in all four sub-crossover classes;
- **above the crossover the step does literally nothing** — eq. 14's `m` is 0.5 there and so is
  the cap, so `Σ LS_V2b·w = Σ LS_V2a·w` exactly.

**The two objects act on disjoint terrain, and the terrain the step acts on carries 2.14 % of
the basin's erosion while covering 37.86 % of its area — a 17.7-fold mismatch (41.8-fold for
the ≤ 5 % band).** On that sub-crossover erosion the step raises the LS-weighted total by
**×1.2132**; carried to the basin that is

```
f_ero(V2b) = f_ero(V2a) + 0.021403 × (1.2132 − 1) = 0.517480 + 0.004563 = 0.522043
```

i.e. **+0.88 %**, all of it from 2.14 % of the erosion. (Under the source field itself that
terrain carries 4.14 %, because the cap knocks the steep cells down.)

**The counterfactual, so the smallness is bounded and not merely asserted.** Holding the
measured per-class ratios (×1.2132 below the crossover, ×1.0000 above), eq. 14-vs-cap would
have reached the 0.1644 materiality bar only if the sub-crossover terrain carried **83.8 %** of
the source field's erosion. It carries **4.1 %**. **Defect A had no route to mattering on this
basin's slope distribution.**

---

## 5 — (c) How far our LS sits above the source level, corrected

### 5.1 The number

| basis | source-formulation factor | our LS ÷ source |
|---|---:|---:|
| published (`docs/37` §4 candidate 0, area-weighted proxy) | ×0.421 – ×0.333 | **2.37× – 3.00×** |
| **corrected, erosion-weighted, exact** (`docs/47` §4.3, reproduced here) | **×0.43194 – ×0.25146** | **2.3151× – 3.9768×** |

**The corrected statement is: our LS is 2.3151× – 3.9768× the source level** — the lower end
with the source's continuous `L`, the upper with its literal Desmet–Govers `L`. `docs/47` §4.3
already registers this bracket; this run reproduces its ×0.43194 endpoint independently, behind
both gates of §1, and adds the V4′ endpoint it did not contain.

### 5.2 Did Defect A's prediction hold?

`docs/46` §1.1 predicted: *eq. 14 is less reducing than the cap below ~9 % slope, so the true
gap may be **smaller than 2.37×***.

**The direction held. The magnitude is 0.36 %, and as applied to the published number it is
zero.**

| | ×0.421-end of the gap |
|---|---:|
| cap joint V4′, erosion-weighted | 2.3235× |
| **step joint V4, erosion-weighted** | **2.3151×** |
| Defect A's own contribution | **−0.36 %** |
| (same on the area basis: 2.3770× → 2.3733×) | −0.16 % |

And because the published joint already **was** the step (§3), **the published 2.37× owed no
Defect-A correction at all.** The move it *did* need — 2.375× → 2.315× — is the proxy→exact
correction of `docs/47` §3.1 R7 (−2.5 %), and the move at the other end — 3.00× → 3.98× — is
Defect **B**'s, in the opposite direction. In log units the three terms are **0.0036** (Defect
A), **0.0257** (the proxy) and **0.2809** (Defect B): **Defect A is the smallest term in the
correction of this bracket by factors of 7× and 78×.**

### 5.3 What this does not settle about `m` — and it is bigger than Defect A

`docs/46` (R6) asks whether eq. 14's `Sf` is slope **percent**, **degrees**, or **m/m**, and
records that if the answer is not percent the hypothesis is **withdrawn, not adjusted**. That
question is **still untested against the source text** — Buarque (2015) pp. 46–48 were not
obtained by this run. What can be measured without the source is the *size* of the question, and
it was measured (erosion-weighted, single lever, same pass):

| reading of `Sf` | `f_ero` | vs percent | basin Mt/yr |
|---|---:|---:|---:|
| **percent** (what the record assumes, and what V2b implements) | 0.52204 | — | 156.37 |
| degrees | 0.51369 | `\|ln\| = 0.0161` — inside the bar | 153.87 |
| **m/m** | **0.17175** | `\|ln\| = **1.1117**` — **6.8× the bar** | **51.44** |

**No verdict is offered on which reading is right — that is a document question and this run
did not obtain the document.** The finding is only this: **the live risk in the `m` lever is the
units, not the cap-vs-step.** One reading is worth 1.6 %, another is worth ×0.329, and Defect A
is worth 0.9 %.

---

## 6 — Corrections owed (recorded, not enacted)

This document may not edit the files below; each is owed to its own owner's amendment slot,
dated, as `docs/46` §7.3 requires.

| # | where | what is wrong | what it should say |
|---|---|---|---|
| **1** | `docs/46` §3.1 (V4/V4′ rows) and §1.1's consequence paragraph | **V4 and V4′ are swapped.** §3.1 calls V4′ *"the ×0.421 row as published"*; the published ×0.421 is **V4**, the step | V4 is the reproducibility anchor; V4′ is newly measured at ×0.420704 area / ×0.430381 ero. §1.1's inference that the joint over-states the gap does not apply to the joint |
| **2** | `docs/35` §9.3.1 · `docs/37` §4 candidate 0 and line 1082 · `docs/43` §1.4 (line 89) · `src/nbgen/make_nb18.py` (~1226, 1264, 1334) · `make_nb19.py` (~2399–2447) | the ×0.502 factor is printed beside a description of **eq. 14** | the measured object is `min(m, 0.5)`. eq. 14 is **×0.5051** area-weighted / **×0.5220** erosion-weighted. The naive-product sentence survives with the corrected number (0.5051 × 1.7139 × 0.3513 = 0.3042 ≠ 0.4214) |
| **3** | everywhere the bracket *"2.37×–3.00×"*, *"α reference ≈ 3.9–5.0"*, *"×0.333–×0.421"* appears | superseded as a **measurement** by `docs/47` §4.3 | **2.3151×–3.9768×**; α reference 11.8 × f = **2.967 – 5.097**. Defect A's share of that: +0.018 on the upper α endpoint |
| **4** | `docs/46` §9.1 item 1 | asks a freezing session to resolve or explicitly inherit Defects A and B | **Defect A is resolved here**: real as a label, immaterial as a level (§2–§5). Defect B is resolved in `docs/47` §3.1 R6 |

---

## 7 — What this run does **not** conclude, and what it does not license

1. **It does not validate the LS level.** `docs/42` **G4.2** is untouched: the level stays
   **UNVALIDATED**. Measuring a lever exactly is not evidence that the field is right.
2. **It does not choose a formulation.** `docs/46` §4.2's rule needs grade **CITED** on all
   three levers; this run obtained no source document and verifies no citation. It removes one
   *arithmetic* obstacle to freezing `docs/46`, nothing else.
3. **It does not settle (R6).** §5.3 is a **sensitivity**, explicitly unverified. If `Sf` is not
   percent, V2b is **void, not adjustable** (`docs/46` §2.2).
4. **It does not touch (R11).** No transport re-run was performed; `f_ero` here is gross
   hillslope erosion, which is what `docs/46` §3.3 defines it to be.
5. **It supplies no per-station LS̄ and no slope terciles.** `docs/46` §3.3 requires both of a
   measuring session; `docs/47` §4.4 already carries the per-station numbers (span 1.287×,
   3.1× below detection) and this run does not revisit them.
6. **It says nothing about α, Π, C, the K unit system, the volume convention, P or FG.** They
   are one product (`docs/42` §3.1). An LS factor is a statement about the *pairing*, not about
   α.
7. **No basin total was used as evidence for anything** (`docs/46` §4.3). The Mt/yr columns are
   consequences, printed after the factors, and no formulation is preferred here on any of them.
8. **The `docs/23` §13.2 yield embargo is in force.** Absolute flux only; no t/km²/yr appears.

**Robustness note on the bar.** Every "inside the bar" statement above uses `docs/46` §2's
registered **0.1644 ln**. `docs/48` argues that number is 2.9× – 4.2× too small as a level SE
and proposes replacing it with 0.4775 – 0.6936 ln. **Defect A's 0.0036 – 0.0088 is immaterial
against either**, and a wider bar can only make it more so — so this verdict does not depend on
which band `docs/45` ends up carrying.

---

## 8 — Reproduction and disclosure

```
python3.10 scripts/c3/ls_erosion_weights.py           # ~5 min: 4 min DEM/D8, 35 s cell pass
  -> data/processed/urh_erosion_weights.csv           # 32,782 rows, decade E_u at adopted defaults
  -> data/processed/ls_defect_a.json                  # f_ero for all 8 variants + the class table
```
Both gates print before any new number is reported and the script exits non-zero on either
failure. It SHA-256s `urh_ls2d.csv`, `minibacia_ls2d.csv`, `h2e_drivers.npz` and
`parameters_H2E.csv` before and after and raises if any changed.

- **Files written by this run:** `scripts/c3/ls_erosion_weights.py`,
  `data/processed/urh_erosion_weights.csv`, `data/processed/ls_defect_a.json`,
  `docs/49_defect_a_resolution.md`, `docs/agents/journal_defect-a.md`. **Nothing else.** The
  analysis code is in the repository and not in a scratchpad on purpose: `docs/00` §6 and
  `docs/47` §2.5 C3 record scratchpad-only analysis code as a known loss mode, and
  `journal_ls-impact` lost its harness that way.
- **`data/processed/urh_ls2d.csv` and `minibacia_ls2d.csv` were not opened for writing**;
  `scripts/c3/ls2d.py` was **imported**, never run, and never with `--scale ≠ 1`.
- **No engine default moved.** `ls2d_column` is still `ls2d_hs`; `cp_revision`, the volume and K
  conventions and the H2E parameters are untouched. Every variant is reached by name.
- **No frozen artifact was opened for writing.** `sim_calibrated_v2/{h2e_drivers.npz,
  parameters_H2E.csv}` were read and hash-checked; `q_gauge_H2E.npz` was not opened.
- **No calibration was launched, no simulation of the hydrology re-run, no α̂ produced, no git
  command run.**
- **One honest process note.** The first execution of the cell pass completed the measurement
  and then died in `print()` on a `θ` under cp1252 — and the shell wrapper still reported exit
  code 0. The run was verified from its **executed output**, the traceback was found, the
  character removed, and the pass re-run in full. This is the trap `CLAUDE.md` and the task
  brief both name; it fired, and it was caught by reading the log rather than the status.

### 8.1 Cross-references

| document | relation |
|---|---|
| `docs/46_ls_preregistration_DRAFT.md` | **§1.1 Defect A is this document's subject.** §2.2's (R4) **fires** and (R5) does not; the V4/V4′ swap in §3.1 must be fixed before freezing (§6 item 1) |
| `docs/47_c4_entry_verdict.md` | §4.3's erosion-weighted bracket is reproduced here behind two gates; §3.1 R7's "proxy 2.51 % low" is reproduced (`|ln| = 0.0248`, inside the bar) |
| `docs/37_c3_closure.md` | §4 candidate 0's ×0.502 label and line 206's proxy caveat — both addressed (§6 item 2, §3) |
| `docs/35_qpeak_preregistration.md` §9.3 | the registered comparison this feeds; **not edited**, and the source formulation remains its registered default outcome |
| `docs/48_pi_band_revision.md` | the materiality bar's own revision; §7 shows this verdict is invariant to it |
| `docs/agents/journal_ls-variants-harness.md` | measured V2a/V2b/V4/V4′ on the area basis and reached the V4/V4′ swap independently |
| `docs/agents/journal_ls-impact.md` | the engine re-runs Gate 2 checks against |
