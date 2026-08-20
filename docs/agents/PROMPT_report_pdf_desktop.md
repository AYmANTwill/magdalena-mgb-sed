# MGB-SED / Magdalena — FINISH THE EXPLANATORY REPORT PDF (Claude Desktop hand-off)

> **How to use this file.** Open a fresh **Claude Desktop** chat, attach the files listed in §1,
> paste this whole document as the first message, and say: *"Execute this."*
> Written 2026-08-13 from the repo at `c:\dev\magdalena-mgb-sed`, checked against the owning docs.
>
> **This is the report track. It is NOT the notebook-coherence track** — that one
> (`docs/agents/PROMPT_notebook_coherence.md`) stays in Claude Code and resumes separately.
> Do not attempt notebook or generator work here.

---

## 0 — What this is

The study has a complete result and no written report. `scripts/build_report_pdf.py` (450 lines,
reportlab + matplotlib mathtext) builds **one self-contained explanatory PDF** that tells the whole
study **twice**: Part I in plain language for a non-modeller, Part II with the full mathematics, plus
a glossary defining every technical term. Its structure already exists end to end:

```
Title · Executive summary · Part I §1–3 (plain language)
Part II §4 MUSLE · §5 hydrology ceiling · §6 LS · §7 calibration KGE · §8 the result
        · §9 why not 1 · §10 gauges · §11 ENSO contrast · §12 ceiling bound
Part III Conclusions · Glossary (25 terms) · page footer
```

Equations render to `_eq/*.png` (7 exist: `musle`, `kge`, `kgec`, `kgemax`, `fls`, `ratio`, `bound`).

**Your job is to finish and harden it — the prose, the numbers, and the honesty — not to rebuild it.**

> ⚠ `OUT` and `EQD` at the top of the script are absolute paths from a previous sandbox
> (`/sessions/epic-sleepy-mendel/mnt/magdalena-mgb-sed/`). **Fix them for wherever you are running**
> before anything else, or the build writes into nowhere.

---

## 1 — Attach these to the chat

Required:
- `scripts/build_report_pdf.py` — the builder you are finishing
- `docs/00_INDEX.md` — the map and the WHERE-IS-IT table
- `docs/34_observed_enso_contrast.md` — the observed contrast (the target)
- `docs/55_c43_verdict.md` — the calibration verdict
- `docs/56_c5_enso_application.md` — the modelled contrast (the positive result)
- `docs/58_rainfall_ceiling_bound.md` — the closed rainfall lever

Attach if the section needs it:
- `docs/22_dry_phase_diagnosis.md` (§4.7, the r-ceiling) · `docs/37_c3_closure.md` + its four
  amendments (the erosion level, the G9 disclosure) · `docs/42_c4_guards.md` (non-identifiability)
- `docs/48_pi_band_revision.md` (the Π band) · `docs/59_cross_implementation_comparison.md`
- `docs/23_gauge_geometry.md` §13.2 (why the yield embargo exists) · `docs/57_b5_gauge_expansion.md`

**Desktop has no repo access.** Every number you need is in §4 below, with its owner. If a number you
want is not there and not in an attached doc, **do not invent it — leave a marked `[TK]` and list it
in the report-back.** A plausible fabricated number is the single worst outcome available here.

---

## 2 — House rules that bind every sentence you write

These are the project's own rules, paid for with measured failures. They bind the report exactly as
they bind the code.

- **MEASURE BEFORE ASSERTING.** This project has reversed several confident verdicts by measuring
  them. A claim with no measurement behind it is worse than silence.
- **A NEGATIVE RESULT IS PUBLISHABLE HERE.** The failures are the spine of the story, not
  embarrassments to be smoothed. Do not sand them down — and do not dramatise them either.
- **YIELD EMBARGO.** Absolute flux only — t/day, Mt/yr, mg/L, m³/s. **No t/km²/yr anywhere**, in any
  sentence, table, axis label or figure caption. Per-gauge catchment areas disagree by **more than 2×
  on 31 of 85 shared gauges (36 %)** in *both* independent implementations, so every area-normalised
  number inherits that error one-for-one (`docs/23` §13.2). The current Part III states the embargo
  and its reason — keep that.
- **Never quote a load without its convention AND its `cp_revision`.** The safest course: the report
  currently quotes **no** absolute load. If you add one, it must carry both, plus the G9 disclosure
  (§4).
- **AN UNCITED BAND CANNOT PASS OR FAIL A GATE.** Four have been retired on this rule. Introduce no
  fifth, and reconstruct no materiality bar — `docs/46`'s own `0.1644 ln` bar was **struck and
  replaced by no number** (`docs/52`), after the project applied its own rule to itself.
- **"CITED is not validated" and "fitted is not validated."** Never write that any factor, level or
  parameter is "validated".
- **Never quote a product of single-lever factors as a joint factor.** Measured joint = **×1.34762**.
- **Say which window.** Every ENSO ratio is window-dependent. A ratio without its window is unusable.

---

## 3 — The narrative the report must carry

It is one honest investigation that repeatedly tested its own assumptions, repeatedly found them
wrong, and arrived at a robust result on the one quantity that survived. The report already has the
right two-level shape (weak absolute prediction · strong contrast). What it must not lose:

1. **Inputs are not innocent.** Rain gauges were **zero-suppressed** — missing dry days recorded as
   absent rather than zero — and value screens structurally *cannot* see missing data; neighbour-ratio
   tests caught what per-station statistics missed. The interpolation was **order-dependent** until
   fixed. Catchment areas proved unreliable per gauge in **both** implementations.
2. **The water model hit a data ceiling, not a parameter ceiling.** All three standing hypotheses for
   the El Niño failure were measured and **refuted** — one was **backwards**.
3. **The last rainfall lever was spent and the diagnosis was wrong.** The satellite (CHIRPS) merge was
   built, passed its skill gate (LOOCV r 0.447) and **failed its volume gate twice** (+7.47 %); the
   registered repair was a **no-op** and the diagnosed cause was **wrong**. The final residual route
   was then **bounded at ≤ +0.006 r** — closed-negative, with a number.
4. **Pre-registration earned its keep.** Thresholds were frozen in numbered documents *before* the
   numbers judged against them were computed. One hypothesis (H-PEAK) was **refuted**; a refit fixed
   the peaks but failed 2 of its 3 registered conditions, and the hydrology closed on that **measured
   conflict**, not on preference.
5. **The level is not identifiable, and that is a result — not a gap.** Seven scalars are seven ways
   of writing one product Π; the design matrix has condition number **inf**. So the calibration
   reports Π and evidence grades, never "validated".
6. **Better physics beat tuning.** The slope-length formulation was settled **from the printed
   source, not from a fit**, and improved the sediment score from **−0.350 to −0.118 with no fitting
   at all**.
7. **And the deliverable survives all of it.** The contrast is a **ratio**, so every unidentifiable
   multiplier cancels **exactly**.

---

## 4 — The verified number sheet

Every number below was read from its owning doc on 2026-08-13. **Where a doc disagrees with the
index, the doc wins.** Use these and no others.

### The result (the positive one — Part I §3, Part II §11, Part III)
| quantity | value | owner |
|---|---|---|
| modelled contrast, direction | **18/18** stations, La Niña > El Niño | `docs/56` |
| modelled median rate ratio | **3.05** (geo-mean 3.06, range 1.62 – 4.85) | `docs/56` |
| modelled robustness | direction **18/18 in every one of 6 cells**, β ∈ {0.45, 0.56, 0.65} × {primary, secondary} windows; primary median rises **2.59 → 3.05 → 3.50** with β | `docs/56` |
| observed contrast, direction | **22 of 22** station-ratios exceed 1.0, **no counter-examples**, both estimators, both windows | `docs/34` |
| observed, PRIMARY window | median **2.84** (headline, partial-rating excluded) to **4.62** (sample-day) | `docs/34` |
| observed, SENSITIVITY (ONI-peak) window | median **6.40** (headline) to **9.32** (sample-day) | `docs/34` |
| the honest all-window statement | **~3–9×** | `docs/00_INDEX` §4, from `docs/34` |
| the like-for-like statement | modelled **3.05** sits at the lower edge of the observed **~3–5** *primary-window* band | `docs/56` |
| independent agreement | consistent with Restrepo & Kjerfve (2000) | `docs/34` |
| **no mainstem contrast exists in the observations** | only one Magdalena-trunk SSC station exists in the whole network (`21237020`) | `docs/32` §R6 |

> **Read the last two rows of that table together before writing a word of §11.** "~3–5×" and
> "~3–9×" are **both correct** and mean different things: 3–5 is the *primary-window* band the
> modelled 3.05 is legitimately compared against; 3–9 is the *all-window* honest statement. The
> current draft says "~3–5×" in the Executive summary **without naming the window** — that is the
> single most likely place for this report to be read as overstating agreement. Name the window.

### The ceiling (the honest catch — Part I §3, Part II §5 and §12)
| quantity | value | owner |
|---|---|---|
| dry-phase daily r ceiling | **0.556 – 0.572** across twelve parameter configurations ⇒ **r ≈ 0.57** | `docs/22` §4.7 |
| what it is inherited from | the rainfall field — gauge-only LOOCV daily r **0.429**; inter-gauge daily correlation **0.33** at 0–25 km against ~30 km spacing | `docs/22`, `docs/18` |
| **the caveat that must travel with the hydrology** | **El Niño skill-over-climatology = −0.0005** — the dry phase sits **AT** climatology, not above it | `docs/26` addendum A.5 |
| the satellite merge | LOOCV r **0.447** (gate PASSED); volume **2,188.5 mm/yr, +7.47 %** against [2,016.0, 2,056.8] (gate FAILED, twice) | `docs/18` §15 |
| the final bound on the last route | **r 0.57 → ~0.576, i.e. ≤ +0.006** — "the ceiling is structural" | `docs/58` |
| adopted hydrology | **H2E**, objective **F = 0.25931** | `docs/26` addendum |

### The calibration verdict (Part II §7–§9)
| quantity | value | owner |
|---|---|---|
| verdict | **RAILED / EXPLORATORY — the fit is NOT adopted** | `docs/55` |
| in-box optimum | at the **box floor**: α = **2.0**, β 0.60, `F_report` = **−0.118** (median KGE_ln over CAL-8) | `docs/55` |
| unconstrained optimum | α ≈ **0.48**, β 0.56, `F_report` **−0.025** — *below* the box floor | `docs/55` |
| what α ≈ 0.48 means | a **symptom of upstream over-production**, to be found and not offset — **not** a tuning success | `docs/55` |
| the shape result | adopted `V4_dg` improved in-box KGE **−0.350 → −0.118**; *"the shape helps, the level does not"* | `docs/55` |
| the bar | **[−0.26, 0.44]**, Fagundes (2018) §6.3.1 — and **weak by construction**: a mean-flow predictor scores KGE = 1 − √2 = **−0.414** | `docs/55`, `docs/59` |
| the out-of-sample check | EVAL station `21237020` (Magdalena trunk), scored but **never fitted**: KGE **+0.462** | `docs/55` |
| without the one flow-selective station | median lifts to `F_report` **+0.197** | `docs/55` |
| non-identifiability | α, C, LS, K units, volume convention, P and FG are **seven ways of writing one product Π**; design-matrix **condition number = inf** | `docs/42` §3 |
| the Π interval | **Π̂ × [0.29, 3.73]** (95 %, station bootstrap) | `docs/48` |
| measured per-station residual sd | **1.9618 ln** — **×4.22** the old 0.465 ln figure, which measured *observer-vs-observer disagreement*, not model−observation residual | `docs/48` |
| Williams' published α reference | **11.8** (legitimate to cite as the physical reference) | `docs/45` |
| slope-length factor | `f_LS` = **0.25146** adopted; bracket **[0.25146, 0.43194]** erosion-weighted ⇒ **2.3151× – 3.9768×** | `docs/51`, `docs/37` A3.3.1 |

### The gauge network (Part II §10)
| quantity | value | owner |
|---|---|---|
| SSC stations classified | **79/79**, every one with a deciding measurement | `docs/32` §R6 |
| usable | **18** (6 usable + 12 usable-with-caveat); 28 mapped, 46 had no coordinates | `docs/32` §R6 |
| the fit sets — **never conflate** | **CAL 8** is what is fitted · **EVAL 5** scored never fitted · **all 18** run the structure guards | `docs/45` §3.4 |
| the expansion attempt | 46 geocoded, **43 in-basin**, and **0 of 43 have any discharge record** — sediment-only sampling points; a **physical limit of the monitoring network**, not a processing gap | `docs/57` |
| **the G9 disclosure** | **66.53 %** of the model's gross erosion (**199.29 of 299.54 Mt/yr**) is upstream of **no** usable SSC station; only **33.47 %** is observable | `docs/37`, `docs/42` G9 |
| basin | **8,672** minibacias, **257,097 km²** | `docs/00_INDEX` §1 |

> **`docs/37` requires the 66.53 % disclosure in the same paragraph as any basin erosion figure.**
> If you quote 299.54 Mt/yr you owe: the **convention** (gross **hillslope** erosion, α and β
> **unfitted** — a **lower bound**), the **`cp_revision`** (`cited_central_2026_08_11`), *and* this
> disclosure. If that is too heavy for a plain-language report, **quote no load at all** — which is
> what the current draft does, and it is a defensible choice.

### If — and only if — you mention the second implementation (`docs/59`)
It must be stated **in these words**: **"an independent implementation, not independent data."** The
algebraic non-identifiability leg is bug-independent and survives: *"MUSLE is linear in both alpha
and the C multiplier; only their product is identifiable from these data."* It is admissible as
**methodological replication only** — **never** as "independent confirmation". If that nuance cannot
be carried in a plain-language report, **omit the comparison entirely.** An overclaim here is worse
than an omission.

---

## 5 — Issues already found in the current draft

Verified against the owning docs. Fix each, or record why not.

1. **Executive summary — "matching independent measurements (~3–5×)".** Correct band, **missing its
   window**, and "matching" is doing heavy lifting: the modelled 3.05 sits at the *lower edge* of
   that band, and the all-window observed statement is ~3–9×. Rewrite to name the window and state
   the position honestly (`docs/37`'s own phrasing for the earlier comparison was *"right sign and
   order, short in magnitude"*). **This is the report's highest overclaim risk.**
2. **"reconstruct the day-to-day river flow to about 57% accuracy (a correlation of r ≈ 0.57)".**
   A correlation is **not** a percentage accuracy, and r ≈ 0.57 is specifically the **dry-phase /
   El Niño** daily ceiling (0.556–0.572), not an all-period figure. Keep a plain-language gloss if you
   want one, but make it a *simile*, not an equation, and state the precise claim in Part II §5.
3. **The −0.0005 caveat is absent.** El Niño skill-over-climatology = **−0.0005** — the dry phase sits
   *at* climatology. The project's standing instruction is that this travels with the hydrology,
   **stated not buried**. It belongs in Part II §5, and arguably in Part I §3.
4. **Part III "the sediment model is weak (KGE near zero)"** — checked, and this is **fair**
   (−0.118 in-box). Do not weaken it further, and do not strengthen it either. But add what makes it
   interpretable: the bar is **weak by construction** (mean-flow predictor = −0.414), so "beats the
   no-skill line but sits at the bottom of the range" is the honest form.
5. **"rails under calibration"** is used before "rails" is defined. The glossary defines it — move a
   one-clause gloss to first use.
6. **Zero-suppression, the order-dependent interpolation, and the refuted hypotheses do not appear
   anywhere.** These are narrative beats 1, 2 and 4 (§3 above) and they are what make the report an
   *investigation* rather than a results dump. Part I currently jumps from "what we built" to "what
   we found". **This is the largest substantive gap.**
7. **Glossary.** "α — the level knob for erosion; physical reference value 11.8" is correct. Consider
   adding: **Π** (the one identifiable product), **pre-registration**, **zero-suppression**,
   **LOOCV**, **PBIAS**. The glossary is the report's best feature — extend it.
8. **`OUT` / `EQD` sandbox paths** (§0 warning). Fix before building.

---

## 6 — What "finish" means

In this order:

1. **Repair the paths, build the PDF once, and read it as a document** — page count, orphaned
   headings, equation images that render at the wrong size, table overflow, footer on every page.
   Report the page count.
2. **Fix the eight issues in §5.**
3. **Close the narrative gap (§5 item 6):** add the investigation beats to Part I — inputs were not
   innocent, hypotheses were measured and refuted, pre-registration caught a failure. Keep Part I
   readable by a non-modeller; the mathematics stays in Part II.
4. **Audit every number in the PDF against §4.** Any number not in §4 and not in an attached doc
   becomes a `[TK]` and goes in the report-back. **Do not fill a gap by inference.**
5. **Run the honesty pass yourself, adversarially** — assume the draft is overclaiming, and check:
   is any failure softened? is any negative result dressed as a success? is any ratio quoted without
   its window? is the yield embargo intact (grep the whole script for `km²`, `km2`, `t/km`, `ton/ha`)?
   is anything called "validated"? has any retired band or bar been reconstructed?
6. **Deliver the finished PDF**, plus a short change-log of what you altered and why.

Optional, only if the above is done and solid: a one-page **executive brief** for the advisor
(Prof. F. J. Briceño-Zuluaga) — the question, the two-level answer, the three convergent lines
(observed flux 22/22 · observed concentration, weaker but same direction · modelled 18/18), and the
named limitations.

---

## 7 — Do NOT

- **Do not** invent, interpolate, or "reasonably estimate" any number. `[TK]` it and say so.
- **Do not** report any t/km²/yr, anywhere, in any form.
- **Do not** write that anything is "validated", or that the calibration was adopted — it was
  **RAILED / EXPLORATORY and explicitly not adopted**.
- **Do not** present the second implementation as independent *data*, or as confirmation.
- **Do not** claim the rainfall ceiling has a known fix. It is **closed-negative, bounded at
  ≤ +0.006 r**. There is **no v3 forcing** and none is coming.
- **Do not** soften a failure to make the report read better. The failures are the argument.
- **Do not** touch notebooks, generators, `src/`, or `data/` — none of that is in this track, and the
  notebook-coherence pass owns those files.

---

## 8 — Report back

1. The finished PDF, and its page count.
2. A change-log: every edit, and the reason.
3. Every `[TK]` — the number you needed, the sentence it belongs in, and which doc should own it.
4. The honesty-pass result: what you found overclaimed, softened, or embargo-breaching, and what you
   did about it — **including anything you decided to leave as-is, and why**.
5. Anything you could not settle, named as an open item rather than resolved by assumption.
