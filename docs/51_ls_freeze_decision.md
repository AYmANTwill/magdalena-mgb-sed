# 51 — The LS freeze decision: **DO NOT FREEZE AS DRAFTED**, and the corrected bracket

**Written 2026-08-11** by the `ls-freeze-decision` agent (process record:
`docs/agents/journal_ls-freeze-decision.md`). This document does **four** jobs and nothing else:
it restates the LS bracket on the measurements that landed today, verdicts `docs/46` §1.1's two
defects, answers `docs/46` §9.1's four freezing conditions one by one, and states what the result
does to `docs/47`'s `C4.3-BLOCKED-UNTIL-LS-LANDS` verdict.

**Scope.** It **does not edit `docs/46`** — it recommends; the orchestrator enacts. `docs/35`,
`docs/37`, `docs/42`, `docs/43`, `docs/45`, `docs/46` and `docs/47` were read and **not** edited.
No default moved, no variant adopted, no engine run, no fit, no git command. The one new
*measurement* this pass makes is a **reading** of the primary source (§1), and it is decisive.

---

> ## THE FOUR ANSWERS
>
> **1 — The corrected bracket.** `f_LS ∈ [0.25146, 0.43194]` **erosion-weighted**
> (`[0.24468, 0.42148]` area-weighted proxy) ⇒ **our LS is 2.3151× – 3.9768× the source level**.
> This **supersedes ×0.333 – ×0.421 and "2.37× – 3.00×"** and it is *identical* to what
> `docs/47` §4.3 already registered — today's work **confirms it, it does not move it**. Both
> ends are corrected; neither is uncorrectable. **And the interval is not an uncertainty over
> readings of the source**: with Buarque eq. 13 now read verbatim (§1), the source formulation
> read whole is a **POINT at ×0.25146**, and ×0.43194 is a documented **hybrid** that keeps *our*
> `L`. The span between them is the `L`-form lever, not a reading ambiguity.
>
> **2 — Defect A: RESOLVED, IMMATERIAL.** `|ln V4/V4′|` = **0.0036** at the upper end and
> **0.0010** at the lower end, against the 0.1644 bar. Real as a **label** (the ×0.502 row is the
> cap, which is nobody's formulation), worth nothing as a **level**. *And the joint ×0.421 never
> carried it at all* — the published row was already the step.
> **Defect B: RESOLVED, MATERIAL.** The endpoint it was raised against moves by
> `|ln|` **0.307** (×0.333 → ×0.2447 area) and the bracket gets **2.31× wider in log units**.
> Its stated *mechanism* (the `S` confound) accounts for only **0.026** of that; the rest is that
> the `L`-form ratio is **formulation-dependent** (0.852 uncapped / 0.770 `hs` / 0.581 inside the
> source) and was carried across formulations as a scalar.
>
> **3 — Freeze recommendation: DO NOT FREEZE the draft as it stands. Freeze it after the
> five-item amendment set of §5.6** — four mechanical restatements of measurements already in
> hand, plus one real decision (the materiality bar). Freezing today would freeze a headline
> bracket that is falsified, a variant table that mislabels its own reproducibility anchor, an
> open (R6) that is now **settled from the primary source**, and a decision threshold whose stated
> derivation `docs/47` §2.2 measures **4.2× wrong**. This is hours of work, not a research
> programme. **`docs/46` §9.1 items 1, 2 and 4 are answerable YES today; item 3 needs one naming
> decision** (§5).
>
> **4 — `docs/47`: the BLOCKED verdict HOLDS, and is strengthened, not weakened.** The bracket
> did not narrow — it is unchanged, now with the last open source question closed *against* the
> direction that would have narrowed it. Even **collapsing the bracket to its point** leaves the
> registered search railing in two of the three G2.3 β corners. And `docs/47`'s three decisive
> propositions (§5.1 unit, §5.2 pre-computed rail at `f_LS = 1`, §5.3 post-hoc) are each
> **independent of the bracket's width**. §6 states the one measured point that cuts against
> `docs/47`'s *phrasing*, and why it does not cut against its verdict.

---

## 1 — The new evidence: the source **was** obtainable, and it settles (R6)

`docs/46` §9.1 item 2 makes the freeze conditional on whether eq. 14's `Sf` units can be verified
from Buarque (2015) **pp. 46–48**, and pre-commits **NEGATIVE — UNRESOLVED** for the `m` lever if
the PDF cannot be obtained. **The PDF is obtainable, it was obtained, and it is on disk.**

| | |
|---|---|
| document | Buarque, D. C. (2015), doctoral thesis, IPH/UFRGS, **182 pp.** |
| retrieval | `lume.ufrgs.br` handle **`10183/129875`**, by the `ls-evidence` agent (`docs/agents/journal_ls-evidence.md` S4) |
| file | `…/scratchpad/buarque2015.pdf`, **9,646,521 bytes** |
| **sha256** | **`3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037`** |
| page map | PDF page **63** = printed page **47** (eqs. 13–17); PDF page **64** = printed page **48** (eq. 18) |

**(R6) — RESOLVED. `Sf` is slope PERCENT.** Printed p. 47, immediately under eq. (14), verbatim:

> `m = 0,2 se Sf < 1` | `0,3 se 1 ≤ Sf < 3` | `0,4 se 3 ≤ Sf < 5` | `0,5 se Sf ≥ 5`  **(14)**
> **onde Sf [%] é a declividade do pixel.**

Corroborated by a **second, independent sentence** on printed p. 48, under eq. (18):

> `S_k = 65,41·sin²(θ_k) + 4,56·sin(θ_k) + 0,065`  **(18)**, **sendo θ o valor de `Sf` em graus.**

A conversion note that is only meaningful if `Sf` is **not** already in degrees. This is the same
two-sentence device that settled the limiter (p. 94 + p. 98).

**Honesty about the residue:** eq. (15) writes `Sf = √((∂z/∂x)² + (∂z/∂y)²)`, a **dimensionless**
gradient — the ×100 is not written. The source is internally loose. But the unit tag is explicit,
the degrees reading is excluded by eq. 18's conversion note, and the m/m reading is excluded twice
over (by the tag, and because breakpoints at 1, 3 and 5 **m/m** are 100 %, 300 % and 500 % slopes).
**Single admissible reading.** Consequently `docs/49` §5.3's live risk — *"×0.329, `|ln|` 1.1117,
6.8× the bar, basin 51.4 Mt/yr, if `Sf` is m/m"* — is **RETIRED**, and
`scripts/c3/ls2d_variants.py:148`'s `sf = 100·tanθ` with half-open 1/3/5 breakpoints is the
source's own unit and its own boundaries, verified line by line against the quote above.

### 1.1 A second lever closed by the same page, not previously on the record

Eq. (13), printed p. 47, is the Desmet & Govers finite-difference `L` **with its aspect factor
written into the source we transpose**:

> `L_k = [(Am_k + Lp_k²)^(m+1) − Am_k^(m+1)] / [Lp^(m+2) · Xdir_k^m · (22,13)^m]`  **(13)**
> …*"O fator de direção `Xdir` … igual a 1 quando a direção entre eles é ortogonal, ou igual a
> 2^(1/2) quando a direção é diagonal."*

`scripts/c3/ls2d_defect_b.py:146` and `ls2d_variants.py:186-190` both carry `x_aspect ** m` in
exactly that denominator position. **So `docs/50`'s flag — *"the D&G aspect term `x^m` is worth
×1.149 on the lower endpoint on a convention that is UNVERIFIED while D&G (1996) is unobtained"* —
is now closed at grade CITED against the transposed source itself.** D&G (1996) remains unobtained
(`docs/47` O1) and does not need to be: `docs/46` §4.2 item 1 registers fidelity to **the
transposed method**, and the transposed method states the convention on p. 47.

### 1.2 What this does to the evidence grades

| lever | source sentence | grade |
|---|---|---|
| slope-length limiter (1 pixel) | p. 94 + **p. 98**, two independent sentences | **CITED** |
| `m` — eq. 14 step | p. 47, verbatim, **with `Sf` [%] verified** | **CITED** — (R6) closed |
| `S` — eq. 18 W&S 1978 | p. 48, verbatim, *"dado por Wischmeier & Smith (1978)"* | **CITED** |
| `L` — eq. 13 D&G FD, `Xdir^m` | p. 47, verbatim | **CITED** |

`docs/46` §4.2 item 5 requires CITED on every lever before any default is switched. **That
evidentiary condition is now met** — which makes **ADOPT-SOURCE reachable**, where before today
the honest outcome for the `m` lever was NEGATIVE — UNRESOLVED. *(Reachable is not adopted: §4.2's
other conditions, including §3.3's full stratified report, are not all discharged — §7 item 6.)*

> **Provenance debt, and it is real:** the PDF lives in a **session scratchpad**, which
> `docs/00` §6 and `docs/47` §2.5 C3 both name as a known loss mode. The hash and handle above are
> the record; **copying the file somewhere durable is §7 item 2.**

---

## 2 — The corrected LS bracket

### 2.1 The replacement statement

> **`f_LS` ∈ [0.25146, 0.43194] erosion-weighted ⇒ `1/f_LS` ∈ [2.3151, 3.9768].**
> Area-weighted proxy: **[0.24468, 0.42148]**, measured **2.5 % low** (`docs/47` §3.1 R7).
> This **replaces ×0.333 – ×0.421** and **"our LS is 2.37× – 3.00×"** everywhere they appear.

| | published (`docs/37` §4 cand. 0, `docs/46` §1) | **corrected** | what moved it |
|---|---|---|---|
| upper end (`f` nearest 1) | ×0.421 | **×0.43194** ero · ×0.42148 area | proxy→exact only (`|ln|` 0.0248). **Defect A: 0.0036** |
| lower end | ×0.333 | **×0.25146** ero · ×0.24468 area | Defect B's resolution (`|ln|` 0.307) |
| gap `1/f` | 2.37× – 3.00× | **2.3151× – 3.9768×** | |
| ln width | 0.2345 | **0.5410** — **2.31× wider** | |
| α reference `11.8·f` | ≈ 3.9 – 5.0 | **2.967 – 5.097** | |
| `docs/35` §6.1 band `5.9–23.6 · f` | ≈ 2.0 – 9.9 | **1.484 – 2.548** … **5.935 – 10.194** | |
| hard stop `35.4 · f` | ≈ 11.8 – 14.9 | **8.902 – 15.291** | |
| basin load at the endpoint | ≈ 126.1 / ≈ 99.7 Mt/yr (proxy) | **129.3840 / 75.3235 Mt/yr** (engine) | |

### 2.2 The measurement behind each end

**Upper end — ×0.43194 (erosion-weighted).** `V4` = 1-pixel limiter + eq. 14 step `m` + eq. 18
W&S `S`, **our continuous `L`**. Engine re-run, `docs/47` §4.3 (129.3840 of 299.5387 Mt/yr).
Independently reproduced by `docs/49` gate 2 through the exact-linearity route (0.431944 vs
0.43194) after passing a basin-erosion gate at **299.5387088405831 Mt/yr**. The area-weighted
counterpart 16.775413430326214 reproduces the published ×0.421 row **to 15 significant figures**,
which is what proved the published row was already the step, not the cap.

**Lower end — ×0.25146 (erosion-weighted).** `V4_dg` = the **same three levers with eq. 13's
`L`** — the source formulation read whole. Engine re-run, `docs/47` §4.3 (75.3235 Mt/yr). Its
area-weighted counterpart has **three independent reproductions**: `ls-evidence` 9.741 (×0.245),
`ls-impact` ×0.24466, and `docs/50` **0.2446790094097074** behind three gates. Under the p. 94 /
p. 98 cap `a_in → 0`, so eq. 13 degenerates to `L = (D/(22,13·Xdir))^m` — that is the source's own
two statements composed, not a choice made here (`docs/47` §4.3's caveat, carried).

**Cross-check I ran myself:** the two erosion/area pairs must be consistent with `docs/47` R7's
separately measured proxy bias. `0.43194418/0.42147514 = 1.024839` (R7: 1.0251) and
`0.25146/0.24467901 = 1.027714` (R7: 1.0278). **Consistent to 4 s.f.**

### 2.3 What the interval **is**, and what it is not

It is **not** an uncertainty band over admissible readings of the source. Every lever is now CITED
(§1.2), and there is no admissible reading of Buarque in which `L` is our point-rate form: eq. 13
is on p. 47 in print. Therefore:

- **the source formulation read whole is a POINT: `f_LS` = 0.25146 (ero) / 0.24468 (area);**
- **×0.43194 is a hybrid** — the source's three levers with **our** `L` — retained because
  `docs/35` §9.3.1, `docs/37` §4 candidate 0 and `docs/43` §1.4 all quote it and it must stay
  reproducible;
- **the span between them is the `L`-form lever**, exactly: `ln(0.43194/0.25146) = 0.5410` =
  `−ln 0.5807`, the `L`-form ratio *inside* the source formulation.

**This is a statement about what the source says, not an adoption.** `docs/46` §4 owns the
adoption and this document may not make it. But the freezing session must know that the object it
is registering as a "bracket" is a point plus a documented hybrid, because `docs/47` §6.2 item 2
already provides for that case (*"unless C3.1 collapses it to a point, in which case the adopted
point and its grade travel instead"*).

### 2.4 Can either end **not** be corrected? — No, but three residues travel with both

Both ends are corrected. Neither is uncorrectable. What cannot be removed, stated so nothing is
over-read:

1. **Both rows are the source's *formulation* on OUR terrain data** — our 90 m COP90 DEM (his
   500 m), our Horn 3×3 slope (his eq. 15 centred differences over four orthogonal neighbours,
   Wilson & Gallant 2000), our D8 routing, our URH mask. `docs/46` §3.1 fixes this deliberately
   (everything not named is held at V0), but it means neither number is "his LS".
2. **The lower end has ONE erosion-weighted measurement** (`docs/47` §4.3's engine re-run) against
   **three** area-weighted ones. `urh_ls2d_variants.csv` carries no `V4_dg` column, so no second
   `f_ero` reproduction exists on disk. **I did not re-measure it.** §7 item 7 is the cheap fix.
3. **`α = 11.8` (Williams 1975) predates every 2-D contributing-area LS by two decades**
   (`docs/47` §4.2 item 6). This bounds every ratio above and is **NOT SETTLED**. No band offered.

---

## 3 — Defect A — **RESOLVED, IMMATERIAL** *(and it never touched the joint)*

| test | measured | bar | verdict |
|---|---:|---:|---|
| (R4) `|ln f(V2b) − ln f(V2a)|` | **0.0088** ero (0.0052 area) | 0.1644 | **FIRES** ⇒ H-M's **field clause REFUTED**, 19× inside |
| (R5) sign `f(V2b) > f(V2a)` | 0.52204 > 0.51748 | — | **does not fire** — the predicted sign held |
| Defect A on the **upper** endpoint | `|ln V4/V4′|` = **0.00362** | 0.1644 | immaterial (45× inside) |
| Defect A on the **lower** endpoint | `|ln V4_dg/V4′_dg|` = **0.00101** | 0.1644 | immaterial (163× inside) — *measured here, not previously stated* |
| Defect A on the α reference | +0.018 (5.079 → **5.097**) | — | nothing |

**The reading clause stands and matters:** `min(m, 0.5)` is nobody's published formulation and
**may never be graded CITED** (`docs/46` §2.2). The ×0.502 row's label *"his eq. 14"* is wrong in
`docs/35` §9.3.1, `docs/37` §4 cand. 0, `docs/43` §1.4, `src/nbgen/make_nb18.py`, `make_nb19.py`.

**The finding that reverses the draft's own bookkeeping:** the published **×0.421 was already the
step** — it is **V4**, not V4′. `docs/46` §3.1's table says the opposite. V4′ (×0.42070 area /
0.43038 ero) had **never been measured** before this run. So Defect A contaminated **the
single-lever label only**, never the joint. **`docs/46` §3.1 must be fixed before freezing**, or
the frozen table mislabels its own reproducibility anchor.

*(Deciding statistic, from `docs/49` §4: below the true cap/step crossover — `tanθ = 0.0893325`,
solved not guessed — lies **37.86 % of basin AREA** but **2.14 % of basin EROSION**, a 17.7-fold
mismatch. Defect A could only have reached the bar if that terrain carried **83.8 %** of the
source field's erosion. It carries 4.1 %.)*

---

## 4 — Defect B — **RESOLVED, MATERIAL** *(right conclusion, wrong diagnosis)*

| test | measured | bar | verdict |
|---|---:|---:|---|
| H-L, as `docs/46` §2.5 states it: `|ln f(V5) − ln 0.790|` | **0.0258** | 0.1644 | **REFUTED** — the confound is immaterial at basin scale |
| the endpoint the defect was raised against: ×0.333 vs ×0.2447 | `|ln|` **0.307** | 0.1644 | **MATERIAL** — the endpoint is wrong |
| bracket ln width, published → corrected | 0.2345 → **0.5410** | — | **2.31× WIDER**; the widening (+0.305) is itself ~2× the bar |
| the published 0.790, factorised exactly | **0.852262 (`L` form) × 0.926925 (`S` swap)** | — | the split is effectively unique |
| the **column** confound (`ls2d` → `ls2d_hs`) | **0.887977** (`|ln|` 0.1188) | — | **the larger of the two confounds** — `docs/46` §1.1 presents it as the afterthought |

**The two errors nearly cancel** (`S` made 0.790 7.3 % too low, the column 10.7 % too high, net
+2.6 %) — arithmetic luck, not a defence. **×0.333 fails for a different reason than the draft
gives:** the `L`-form ratio is **formulation-dependent** — 0.852 uncapped / 0.770 `hs` /
**0.580685 inside the source formulation** (span ln 0.384) — and was composed across formulations
as a scalar. Repairing the confound *completely* still gives `0.421363 × 0.769833 = 0.324379`
against the measured **0.244679**, wrong by ×1.326.

> **Consequence for the freeze, and it is not cosmetic:** `docs/46` §2.5 attaches the mandatory
> re-derivation of the bracket to the clause *"if H-L is **not** refuted"*. **H-L IS refuted** —
> and the bracket still must be re-derived. **§2.5 hangs its only mandatory action on a trigger
> that cannot fire.** Freezing that sentence freezes a rule that does the opposite of what it
> says. This is §5.6 item (c).

---

## 5 — The freeze decision

### 5.1 `docs/46` §9.1 item 1 — Defects A and B resolved or explicitly inherited?

**RESOLVED — both, by measurement, not inherited.** §3 and §4 above; primary records `docs/49`,
`docs/50`, `data/processed/{ls_defect_a.json, ls2d_defect_b.json, ls2d_variants_summary.json}`,
each behind reproduction gates, with `urh_ls2d.csv` / `minibacia_ls2d.csv` SHA-256 checked
unchanged before and after by the scripts themselves.

**"Explicitly inherited" is no longer an available option** and must not be taken: the draft's
Defect A text predicts a direction that is now measured as immaterial, and its Defect B text gives
a diagnosis that is now measured as wrong. Freezing them as "inherited" would freeze two
falsified paragraphs.

### 5.2 §9.1 item 2 — can eq. 14's `Sf` units be verified?

**YES — verified, verbatim, page-numbered, single admissible reading (§1).** The pre-committed
NEGATIVE — UNRESOLVED branch for the `m` lever **does not fire**. The PDF is obtainable (it is on
disk, hashed, with its `lume` handle). This is the single largest change today: it converts the
`m` lever from *unfalsifiable* to **CITED**, and it retires the ×0.329 m/m risk.

### 5.3 §9.1 item 3 — who owns enactment?

**A naming decision only I can recommend, and it must be made before the freeze.** The facts:
`scripts/c3/ls2d.py` and `data/processed/urh_ls2d.csv` were delivered by commit `5eaabf5`
(*"c3: LS2D topographic factor from the COP90 DEM"*) under stage **C3.1**; `docs/37` A2.2's owner
table assigns the LS-shape decision to **C3.1** by name; `docs/46` §4.2 requires enactment to be
"a separate dated amendment owned by whoever owns `scripts/c3/ls2d.py` and `docs/37`".

> **Recommendation: the enactment amendment is `docs/37` §A3**, dated, written by the C3.1 owner —
> because `docs/37` is the document that carries the closure conjunction whose **clause 2** the
> adoption discharges, and it is the document whose §1 table and §4 candidate 0 still print
> "2.37× – 3.00×". One amendment then does both jobs. `docs/51` (this file) is **not** that
> amendment and does not switch any default.

### 5.4 §9.1 item 4 — is §6's gate accepted as more restrictive than `docs/45` §6.1?

**YES — accept it, unchanged.** It removes ADOPT from a provisional C4.3 (A3) and is strictly
more restrictive; every `docs/45` condition continues to apply, so no frozen registration is
relaxed. `docs/47` reached **Branch B** independently, on B2 (ADOPT unreachable) plus the
box-boundary argument, and rejected Branch A on three measured grounds — so accepting §6 is
consistent with the standing verdict and creates no conflict.

**Two repairs to §6 to make at the same time, both from `docs/47`:**
- **A4's α̂ ≥ 10.0 stop is moot in the direction written.** The measured optimum sits at the
  **bottom** of the box (0.26 – 1.29 across the β gate), not the top. The symmetric stop it should
  carry is **α̂ ≤ 2.0 × 1.05**, which the measurement says will fire (`docs/47` §5.4).
- **§6.1's `Δ_shape` pre-test has still not been run** (`docs/47` O6) and it is now nearly out of
  time — `docs/47` §6.3 requires it recorded *before* C3.1 reports so it cannot be read backwards.
  **What is knowable without running it, stated as bounds rather than a guess:** per-station
  erosion-weighted LS ratios under the source formulation span **1.287×** (`docs/47` §4.4), so
  `Δ_shape ≤ ln 1.287 = 0.2524`; normalising the all-18 extremes (0.3687, 0.4745) on the basin
  joint factor 0.43194 gives 0.154. **It can land on either side of 0.1644 and must be computed,
  not inferred.** The *branch* does not depend on it (B2 makes Branch B mandatory regardless);
  the *record* does.

### 5.5 The item §9.1 does not list, and it is the one real blocker

**`docs/46`'s materiality bar (0.1644 ln) is the document's single decision rule — it appears at
ten decision points (`:138, 140-142, 189, 217, 240, 265, 490-491, 506, 538`) — and its stated
justification is falsified.** The draft derives it as *"the registered standard error of the
fleet-mean level"* from σ_r = 0.465. `docs/47` §2.2 (**D2, BLOCKING**) measures the actual
per-station residual sd at **1.9618 ln** and the SE at **0.6936 ln** — ×4.22 and ×3.89 — and
`docs/48` (B5) confirms it on three constructions and finds **no admissible construction** on
which 0.465 is the residual sd.

**This is not a rounding problem; it flips a registered verdict.** At the corrected SE:

| clause | statistic | at 0.1644 | at 0.6936 |
|---|---:|---|---|
| (R4) H-M field clause | 0.0088 | refuted | refuted — **robust** |
| H-L (§2.5) | 0.0258 | refuted | refuted — **robust** |
| (R12) proxy vs exact | 0.0248 | refuted | refuted — **robust** |
| **(R10) "decide the levers as a set"** | **0.2983** | **survives** (levers interact) | **FIRES** (levers separable) — **verdict flips** |
| bracket **width** | 0.5410 | material | **immaterial** |
| bracket **endpoints** vs 1.0 | 0.8395 / 1.3805 | material | **material — robust** |

`docs/48` §5 states the requirement and declines to propose a number: **`docs/46` must DECOUPLE
its bar from σ_r, not rescale it** — a decision threshold does not have to be a standard error,
but it may not claim to be one that it is not. This project's own rule (`docs/46` §4.3, `docs/40`)
is that **an uncited band cannot pass or fail a gate**; two have already been retired here. A bar
whose derivation is falsified is in that category the moment the falsification is on the record.

### 5.6 What must land before the freeze — the amendment set

Four mechanical restatements of measurements already in hand, and one decision.

| # | edit to `docs/46` | source | kind |
|---|---|---|---|
| **(a)** | **§1 lines 71–73, §2.5 line 269, §3.5 lines 370–371, §6.2 A2 lines 511–512**: replace ×0.333 – ×0.421 / "2.37×–3.00×" / the α reference, band and hard stop / the proxy load table with **§2.1 of this document** | `docs/47` §4.3, confirmed here | mechanical |
| **(b)** | **§3.1 line 294**: **V4 and V4′ are swapped.** V4 (step) is "the ×0.421 row as published"; V4′ (cap) had never been measured | harness + `docs/49` | mechanical |
| **(c)** | **§1.1 and §2.5**: restate Defect A as RESOLVED-IMMATERIAL and Defect B as RESOLVED-MATERIAL-with-a-different-mechanism, and **re-hang §2.5's mandatory re-derivation on a trigger that can fire** (it currently fires only if H-L survives; H-L is refuted and the re-derivation is still owed) | §3, §4 above | mechanical + one logic fix |
| **(d)** | **§2.2 (R6)**: close it **CITED** with the p. 47 quote, the p. 48 corroboration and the provenance card of §1; strike the m/m sensitivity as retired; and add §1.1's eq. 13 `Xdir` finding to §2.5 | §1 above | mechanical |
| **(e)** | **§2's materiality bar**: **decouple it from σ_r** and re-derive or re-justify it, recording that (R10)'s verdict is bar-dependent | §5.5 | **decision — the only non-mechanical item** |

**And one structural note the freezing session must write into the card, because it is true and
uncomfortable:** every hypothesis in §2 has now been **measured** — H-LIM (R2/R3), H-M (R4/R5/R6),
H-JOINT (R10/R12), H-L — by the variants harness, `docs/49` and `docs/50`, *before* the freeze.
§1's ordering disclosure therefore has to be extended: **`docs/46` freezes as a pre-registration
that has been read out, not as an open one.** What remains genuinely prospective is §4's decision
rule, §6's gate and §7's negative-result branch — nothing has been adopted, no default has moved,
and the enactment amendment (§5.3) is unwritten. Written that way, the freeze is honest; written
as though §2 were still open, it is not.

---

## 6 — The consequence for `docs/47`

`docs/47`'s verdict box rests the blocking argument on *"`f_LS` … measured to be uncertain by a
factor of **2.3151 – 3.9768** … a box whose position is unknown to within a factor of four."*
The question this document owes: **is the corrected bracket materially narrower?**

### 6.1 It is not narrower. It is the same bracket, better founded.

**Measured, not asserted.** Today's work reproduces `docs/47` §4.3 exactly — the four `f_ero` rows
behind `docs/49`'s gate 2 (0.362435/0.517480/1.694054/0.431944 against 0.3624/0.5175/1.6941/
0.43194), the DG endpoint for a **third** independent time (0.2446790 area), and the two
ero/area pairs mutually consistent with R7's separately measured proxy bias. **Nothing in the
bracket moved.** Defect A, the one open item that could plausibly have narrowed it, is worth
**0.0036 at one end and 0.0010 at the other** — 45× and 163× inside the bar.

Moreover the **one live route by which the bracket could still have moved is now closed in the
direction that would have widened it, not narrowed it**: had `Sf` been m/m, the `m` lever would
have gone to ×0.329 and pushed the source level further down (`docs/49` §5.3). It is percent
(§1). And Defect B's resolution made the bracket **2.31× wider in log units** than the published
one that `docs/47` superseded.

### 6.2 The one thing that changes: it may be a **point**, not an interval

§2.3: with eq. 13 verified verbatim, the source read whole is a point at **×0.25146**. If C3.1
adopts it, `docs/47` §6.2 item 2's own escape clause applies — *"unless C3.1 collapses it to a
point, in which case the adopted point and its grade travel instead"* — and the verdict box's
phrase *"unknown to within a factor of four"* becomes **"known to be 3.977× away, pending an
enactment that has not been written."**

**Does that dissolve the block? No — measured, at the point:** applying `1/f_LS = 3.9768` to
`docs/47` §5.2's measured optima gives α̂-equivalents **1.026** (β = 0.45, G2.3 floor), **2.485**
(β = 0.56), **5.126** (β = 0.65, G2.3 ceiling), against the box floor **2.0**, the 5 %-rail band
**< 3.40** and the `docs/35` hard stop **3.9**. **Two of the three G2.3 corners still return
`FAIL — RAILED / HARD STOP`; only the top corner clears.** Collapsing the bracket removes a
*range* from C4's contract; it does not make the search's outcome determinate. (Independently
reached by `docs/50` (e), reproduced here to the last printed digit.)

### 6.3 The blocking argument survives because it never depended on the width

Each of `docs/47` §5's three propositions is **independent of the bracket's width**:

- **P1 (the unit).** The box `[2.0, 30.0]` and the stop 3.9 were registered at `f_LS = 1`. Any
  `f_LS ≠ 1` moves them — a point moves them just as surely as an interval. **Unaffected.**
- **P2 (the pre-computed rail).** The rail is measured **at the adopted LS**, `f_LS = 1`
  (α optima 0.26 – 1.29 across the β gate, `F_report` −0.305 … −0.350 against the bar's −0.26).
  No property of the bracket enters it. **Unaffected**, and §6.2 shows the corrected level does
  not rescue it in two of three corners.
- **P3 (post-hoc).** *Deciding LS after the fit is made by a session that knows which `f_LS` puts
  α̂ inside its box.* If anything today **sharpens** this: with all four levers now CITED and the
  source formulation a single point, the temptation to pick among levers is replaced by a
  temptation to pick between "the source read whole" and "the hybrid" — a **binary** choice worth
  ×1.718, which is easier to make post-hoc, not harder. **Strengthened.**

### 6.4 The one measured point that cuts against `docs/47`'s phrasing — stated, not buried

`docs/47` §2.2 (its own finding) and `docs/48` measure the SE of the fleet-mean level at
**0.6936 ln**. The corrected bracket's **width is 0.5410 ln — smaller than one SE.** So the
sentence *"uncertain by a factor of four"*, read as a **statistical** claim about a quantity the
fit could resolve, is weaker than it sounds: the bracket's width is inside the fit's own noise on
the level.

**Why that does not touch the verdict, and this is arithmetic:** the gate C4.3 must pass is a
**hard interval in α** (`[2.0, 30.0]`, `α̂ < 3.9`), not a confidence statement. A hard boundary is
crossed or not crossed by a level factor **regardless of the noise on the level** — `docs/47`
§5.4 point 1 makes exactly this argument and `docs/46` §6.2 A6 concedes it. And the endpoints'
own distance from 1.0 — `|ln|` **0.8395** and **1.3805** — **exceeds even the corrected SE**, so
the LS level is a material displacement on the corrected noise floor too. `docs/48` reached the
same conclusion by its own route: *"Both `f_LS` bracket endpoints stay material either way, so
`docs/47` §4.3 and its BLOCKED verdict are **not** weakened."*

### 6.5 Verdict on `docs/47`

> **`C4.3-BLOCKED-UNTIL-LS-LANDS` HOLDS. It does not weaken and it does not fall.**
> The bracket is confirmed, not narrowed; the last open source question closed against the
> narrowing direction; the blocking propositions are width-independent; and at the *most*
> favourable end of the corrected bracket the registered search still rails in two of three
> admissible β corners. **The only edit `docs/47` needs is to its §4.3 caveat and its §6.2 item 2
> — to record that the source formulation is a point at ×0.25146 whose four levers are now CITED,
> and that its B1 unblocking event is one amendment set away, not a research programme.** Those
> are additions to a standing verdict, not a revision of it.

---

## 7 — What remains blocking, numbered

An orchestrator can execute this list top to bottom. Items 1–3 unblock the freeze; 4–6 unblock
C4.3; 7–9 are cheap verifications that are **not** blockers and are labelled as such.

1. **Enact the `docs/46` amendment set** — §5.6 (a)–(d), four mechanical restatements. Owner:
   `docs/46`'s owner / orchestrator. **Do not edit §1–§8 after freezing** — enact first, then
   freeze.
2. **Decide `docs/46`'s materiality bar** — §5.6 (e), the one real decision. Decouple it from
   σ_r; record that (R10)'s verdict is bar-dependent (survives at 0.1644, flips at 0.6936).
   `docs/48` deliberately proposes no replacement value; **do not rescale it silently**, and do
   not import 0.6936 by default — the bar is a decision threshold, not a standard error.
3. **Freeze `docs/46`** with the §9 card filled (date + name), §10 opened, and the structural
   note of §5.6 written in: *frozen as a pre-registration that has been read out*. Name the
   enactment owner per §5.3 (**recommended: `docs/37` §A3**).
4. **Write the enactment amendment** — `docs/37` §A3, dated: `ls_formulation`, its grade, the
   §4.2 decision-rule outcome, the α band rescaled per item 3, every variant still reachable by
   name, and `docs/37` §1's table + §4 candidate 0 corrected off "2.37× – 3.00×". **This, not
   `docs/46`'s freeze, is `docs/47`'s B1 unblocking event.**
5. **Run `docs/46` §6.1's `Δ_shape` pre-test** (`docs/47` O6) **before item 4 reports**, so it
   cannot be read backwards. Minutes. Bounds without it: `≤ 0.2524`, plausibly ~0.154 — **it must
   be computed, not inferred** (§5.4).
6. **`docs/47`'s remaining repairs, unchanged:** **B2** (re-express the C4.3 gate in Π, or
   re-register the α box against the adopted `f_LS`); **B3** (`src/mgb_transport.py:902`,
   `if not (m <= max_resid)`, plus the NaN regression test); **B5** (replace the ±38 % Π band and
   restate the `k` bound at ~10× over 342 km); and the **§5.5 disclosure** of the pre-fit profile
   as a `docs/45` §8 amendment. **B4 is discharged** (`docs/42` §9 written) — its three flags
   (`docs/42:230` body value, `docs/43` §3.1's mis-attribution, the withdrawn "method rounding"
   label) are one-line fixes owed to their own files.
7. *(verification, not a blocker)* **Second erosion-weighted reproduction of the lower endpoint.**
   `f_ero(V4_dg)` currently rests on one engine re-run; `urh_ls2d_variants.csv` has no `V4_dg`
   column. `scripts/c3/ls_erosion_weights.py` already has the exact-linearity machinery. §2.4.
8. *(verification, not a blocker)* **Durable copy + provenance record for `buarque2015.pdf`** —
   handle `10183/129875`, sha256 `3047624f…c0037`, pp. 47–48, 94, 98, 121. It is in a session
   scratchpad, a known loss mode (`docs/00` §6, `docs/47` O11). Same record owed for `ah703.pdf`,
   `md1988/89`, `fagundes2018.pdf`.
9. *(not a blocker, and not resolvable)* **`docs/46` §3.3's full stratified report** — elevation
   strata exist for every variant; **slope terciles do not**, and the per-station erosion-weighted
   `LS̄` exists only as ratios (`docs/47` §4.4). Needed before ADOPT-SOURCE is *exercised*, not
   before the freeze. And **`α = 11.8`'s like-for-likeness with any 2-D LS remains NOT SETTLED**
   (`docs/47` §4.2 item 6, O4) — it bounds every ratio in §2.1 from above and no band is offered
   for it here.

---

## 8 — Disclosure

- **What this pass measured itself:** the Buarque (2015) pp. 47–48 reading (§1, the decisive new
  evidence, made from the PDF on disk with its hash recorded); the two-ended Defect A arithmetic
  (`|ln|` 0.00362 upper / 0.00101 lower); the ero/area consistency cross-check against `docs/47`
  R7; the bracket restatement arithmetic of §2.1; the α̂-equivalents of §6.2; and a line-by-line
  read of `scripts/c3/ls2d_variants.py:148,186-190` and `ls2d_defect_b.py:146` against eqs. 13–14.
  **Everything else is carried from a named source and cited in place.**
- **What it did not do:** no engine run, no fit, no α̂, no LS pass, no variant adopted, no default
  moved. `data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv` and
  `sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv, q_gauge_H2E.npz}` were **not opened for
  writing**. `scripts/c3/ls2d.py` was **not run**. No git command was run. Files written: this one
  and `docs/agents/journal_ls-freeze-decision.md`.
- **`docs/46` was NOT edited.** Every change named in §5.6 is a **recommendation** to its owner.
- **`docs/47` was NOT edited**, and §6 is an argument about it, not a revision of it.
- **The `docs/23` §13.2 yield embargo is in force**; §2.1's basin loads are absolute flux,
  model-internal.
- **No plausibility band was invented.** Where a quantity is unresolved — `α = 11.8`'s
  like-for-likeness, `Δ_shape`, `docs/46`'s replacement bar — this document says **NOT SETTLED**
  and stops.
- **The LS level remains UNVALIDATED** (`docs/42` G4.2). Nothing here validates it; §1 raises the
  *provenance* grade of four levers to CITED, and **cited is not validated** (`docs/37` A1.6).
