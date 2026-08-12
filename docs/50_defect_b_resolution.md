# 50 — Defect B resolved: the ×0.790 decomposed, and the bracket's lower end corrected

**Written 2026-08-11** by the `defect-b` agent (process record:
`docs/agents/journal_defect-b.md`). This document **resolves Defect B of
`docs/46_ls_preregistration_DRAFT.md` §1.1 with numbers**, so that `docs/46` can be frozen with
that defect settled rather than inherited (`docs/46` §9.1 item 1).

**It decides nothing and adopts nothing.** No engine default moved; `ls2d_column` is still
`ls2d_hs`; the committed LS products were SHA-256'd before and after and are unchanged; no
frozen artifact under `sim_calibrated_v2/` was opened; no calibration or simulation was run; no
git command was run. Enactment of any LS choice belongs to the separate dated amendment
`docs/46` §4.2 and §9.1 item 3 name, not here.

---

> ## THE ANSWER, IN FIVE LINES
>
> **(a)** The isolated `L` form, on the column the engine actually reads, is **×0.769833**
> (`V5/V0`, `S` held at Moore–Burch). Published: ×0.790.
> **(b)** The published 0.790 is **0.852262 × 0.926925** — `L` form × `S` swap on its own
> (uncapped) column. **The `S` swap is 32.2 % of it in log units; the `L` form 67.8 %.**
> **(c)** The column choice is worth **×0.9033** (`L` form alone) or **×0.8880** (whole recipe)
> — i.e. it is the **larger** of the two confounds, bigger than the `S` swap.
> **(d)** The corrected lower endpoint is **×0.244679** area-weighted (this run) /
> **×0.25146** erosion-weighted (`docs/47` §4.3), **not ×0.333**. "3.00×" becomes **3.977×**
> erosion-weighted (4.087× on the area proxy).
> **(e)** The corrected bracket is **WIDER, by a factor of 2.30 in log units** (ln width 0.541
> vs 0.236). **It does not narrow, and C4.3's blocking reason is strengthened, not relieved.**
>
> **And the finding that matters most: fixing Defect B does not fix ×0.333.** With the confound
> fully repaired the composition still gives 0.421363 × 0.769833 = **0.324379** against the
> measured **0.244679** — wrong by **×1.326** (|ln| 0.282, above `docs/46`'s 0.1644 bar). The
> ×0.333 endpoint fails because a lever ratio was **composed across two formulations in which
> it takes different values**, not because 0.790 was confounded. The confound itself is
> **immaterial** at basin scale (|ln| 0.0258).

---

## 1 — What was measured, and the gates it had to pass first

`scripts/c3/ls2d_defect_b.py`, native 90 m, all **30,235,916** basin cells, basin area
256,702.36 km². Output: `data/processed/ls2d_defect_b.json` (the only file it writes).

**It is not a second implementation of LS.** `scripts/c3/ls2d.py` is imported. The published
ratio's own numerator and denominator are `ls2d.ls_variants()`'s `ls3` and `ls1`; `V0` is its
`ls4`. The DEM, Horn slope, pit filling, D8, flow accumulation, per-row cell geometry and the
area-weighted accumulation are all `ls2d.py`'s. **Only the four mixed columns are new code**,
and they exist because the intermediates needed to split 0.790 **did not exist on disk**.

> **A trap, recorded because it would have produced a fabricated decomposition.**
> `ls2d.py`'s `ls2` — reported as `D_ls2d_mb86` in `ls2d_variants_summary.json` — is **not**
> "the D&G `L` with Moore–Burch `S`". It is the **fixed `m` = 0.4** Moore & Burch cross-check on
> the **continuous** `L` (`scripts/c3/ls2d.py:281`). Treating it as the missing intermediate
> gives "`L` form ×0.157, `S` swap ×5.04", which multiplies out to 0.790 and is entirely wrong.

**Three reproduction gates ran before any new number was reported. All three PASS:**

| gate | target | measured | result |
|---|---|---|---|
| **G-A** V0 basin area-weighted mean | 39.812260149274394 (`ls2d_variants_summary.json`) | **39.812260149274366** | PASS (2-ulp, the strata-accumulator path) |
| **G-B** the **published** ratio `mean(ls3)/mean(ls1)` | 0.790 (`journal_c31-ls2d` §S4) | **0.7899826861390916** | PASS |
| **G-C** `V5/V0` | 0.7698333815060305 (`ls2d_variants.py`) | **0.7698333815060308** | PASS |

Two further numbers reproduce that no gate demanded, both from independent harnesses:
`S` → McCool-87 on the hs basis **0.907982** against `journal_ls-evidence`'s **0.908**
(36.14880 vs 36.149); and the source method with its own D&G `L` at **9.74122** against
`journal_ls-evidence`'s **9.741** — a **third independent reproduction** of the corrected
endpoint, after `ls-evidence` (×0.2447) and `ls-impact` (×0.2447), the two `docs/47` §3.1 R6
registers.

**Protected:** `urh_ls2d.csv` `8579c128…f3c4` and `minibacia_ls2d.csv` `4c49b07b…1724`,
identical before and after; the script raises if either moves. `scripts/c3/ls2d.py` was **not**
run (`--scale` traps, `journal_decide-ls-resolution` §2).

### 1.1 The levels this run measured

Area-weighted mean LS, basin and the `docs/46` §3.3 elevation strata. `L_cont` = our production
point-rate length term; `L_dg` = the Desmet & Govers (1996) eq. 11 finite difference;
`S_mb` = Moore & Burch (1986) `(sinθ/0.0896)^1.3` (ours); `S_mc` = McCool (1987);
`S_ws` = Wischmeier & Smith (1978) = Buarque eq. 18. "unc" = the uncapped `ls2d` column;
"hs" = the 1 km² channel-capped `ls2d_hs` column **the engine reads**
(`src/mgb_sediment.py`, `ls2d_column="ls2d_hs"`).

| column | what it is | basin | < 200 m | 200–1000 m | > 1000 m | × V0 |
|---|---|---:|---:|---:|---:|---:|
| `U_Lc_Smb` | `ls1` — **published denominator** | 104.90127 | 8.97275 | 221.59705 | 104.57815 | 2.63490 |
| `U_Ldg_Smc` | `ls3` — **published numerator** | 82.87019 | 7.94716 | 180.99248 | 78.97355 | 2.08152 |
| `U_Ldg_Smb` | **new** — `L` form alone, uncapped | 89.40335 | 7.86876 | 195.22856 | 85.66194 | 2.24562 |
| `U_Lc_Smc` | **new** — `S` swap alone, uncapped | 96.99056 | 9.05900 | 205.27752 | 96.00547 | 2.43620 |
| `H_Lc_Smb` | `ls4` = **V0** = `urh_ls2d.csv:ls2d_hs` | **39.81226** | 2.01546 | 36.92706 | 65.19940 | 1.00000 |
| `H_Ldg_Smb` | **V5** — `L` form alone, hs | 30.64881 | 1.53685 | 28.36838 | 50.23294 | 0.76983 |
| `H_Ldg_Smc` | **new** — the published *recipe* on the *engine's* column | 27.92775 | 1.68013 | 26.41503 | 45.30128 | 0.70149 |
| `H_Lc_Smc` | **new** — `S` swap alone, hs | 36.14880 | 2.17648 | 34.25659 | 58.60107 | 0.90798 |
| `V4` | source formulation, continuous `L` | 16.77541 | 1.22216 | 15.80481 | 27.10901 | 0.42136 |
| `V4_dg` | **source formulation, D&G `L`** | **9.74122** | 0.74990 | 9.20023 | 15.70457 | **0.24468** |
| `V4_dg_x1` | same, aspect term `x` = 1 (sensitivity) | 11.19360 | 0.84015 | 10.54347 | 18.07455 | 0.28116 |
| `V4p` / `V4p_dg` | the `min(m,0.5)` cap versions of both | 16.74916 / 9.73134 | | | | 0.42070 / 0.24443 |

---

## 2 — (a) The isolated `L`-form factor

> **`V5 / V0` = 0.769833 (ln −0.26158), against the published ×0.790 (ln −0.23574).**
> **`|ln f(V5) − ln 0.790| = 0.02584 ≤ 0.1644` ⇒ `docs/46` §2.5's H-L refutation clause FIRES:
> H-L is REFUTED. The confound is immaterial at basin scale.**

This confirms `journal_ls-variants-harness` and `journal_ls-evidence` (both ×0.770) on a third
pass, and it is now a like-for-like comparison rather than an inference, because the same run
reproduces the confounded 0.790 to 4 s.f. (0.78998) from `ls2d.py`'s own columns.

**The isolated factor is also the *stable* one.** Across the three elevation strata:

| ratio | < 200 m | 200–1000 m | > 1000 m | spread (ln) |
|---|---:|---:|---:|---:|
| **isolated `L` form, hs (`V5/V0`)** | 0.76253 | 0.76823 | **0.77045** | **0.0103** |
| the published 0.790 (`ls3/ls1`, uncapped) | 0.88570 | 0.81676 | 0.75516 | **0.1594** |

The published number varies by ln 0.159 across strata — nearly the whole materiality bar — while
the isolated `L` form varies by ln 0.010. **The published figure is a composite whose value
depends on where in the basin you evaluate it; the isolated `L` form is very nearly a scalar.**
That is a property of the quantity, not of the arithmetic, and it is the reason the isolation
was worth doing even though the basin-scale difference is immaterial.

---

## 3 — (b) How much of 0.790 was the `S` swap

The published ratio factorises **exactly**, and it does so two ways (it is a ratio of means, so
the decomposition is path-dependent; both paths are reported, and they agree closely):

| path | first factor | second factor | product |
|---|---:|---:|---:|
| **`L` first** | `L` form, `S` held at MB86: **0.852262** | `S` swap on the D&G `L`: **0.926925** | **0.789983** |
| **`S` first** | `S` swap on the continuous `L`: **0.924589** | `L` form on the McCool `S`: **0.854415** | **0.789983** |

Path spread: ln 0.0025 on the `L` term, ln 0.0027 on the `S` term — negligible, so the split is
effectively unique at basin scale.

> **In log units: `ln 0.789983 = −0.23574 = (−0.15986 for the `L` form) + (−0.07588 for the `S`
> swap)`. The `S` swap is 32.2 % of the published number; the `L` form is 67.8 %.**

**Direction:** `S_McCool-87 / S_MB86` is **below 1** on this basin's weighting (0.9269 on the
D&G-`L` weighting, 0.9246 on the continuous-`L` weighting, 0.9080 on the hs column), so the
`S` swap made the published number **7.3 % lower** than a pure `L`-form ratio on the same column.
It is not a uniform factor: it is **above 1 in the lowland** (1.010 uncapped, 1.080 on hs) and
below 1 in the Andes (0.922 / 0.899), exactly as `docs/46` §3.4's pointwise table predicts
(McC/MB 3.578 at tan θ 0.005 → 0.744 at tan θ 1.5). `docs/46` §1.1's characterisation of this
lever as "strongly slope-dependent" is **confirmed**; its basin-scale *size*, which §1.1 does
not state, is **7.3 %**.

---

## 4 — (c) How much of it was the column choice

The published ratio was measured on the **uncapped** `ls2d` column; the engine reads `ls2d_hs`.
Moving the **identical recipe** to the engine's column:

| quantity | uncapped column | **hs column (the engine's)** | column factor |
|---|---:|---:|---:|
| the whole published recipe (`L_dg·S_mc / L_cont·S_mb`) | **0.789983** | **0.701486** | **0.887977** (ln −0.11881) |
| the `L` form alone (`S` held at MB86) | 0.852262 | **0.769833** | **0.903283** (ln −0.10172) |

> **The column choice is worth ×0.888 on the whole recipe and ×0.903 on the `L` form alone —
> i.e. |ln| 0.102–0.119, which is LARGER than the `S` swap's 0.076–0.093.** `docs/46` §1.1
> presents the column as the secondary half of Defect B ("It was **also** measured on the
> uncapped `ls2d` column"). **Measured, it is the bigger of the two errors.**

The mechanism is derivable and was predicted before the run (journal, Step 2): per cell,
`L_dg/L_cont = [λ_out^(m+1) − λ_in^(m+1)] / [(m+1)·λ_out^m·D·x^m]`, which equals
`1/[(m+1)x^m]` on a head cell (`λ_in` = 0) and tends to `1/x^m` as `λ_in ≫ D`. Capping the
upslope area at 1 km² **shortens** slope lengths, moves cells toward the head-cell limit, and so
drives the `L`-form ratio **further below 1** — 0.770 on the capped column against 0.852 on the
uncapped one. The measurement matched the prediction in sign and in size.

---

## 5 — The error budget: the two confounds nearly cancel, and that is a coincidence

From the published 0.790 to the isolated, correct-column ×0.7698:

| term | factor | ln | effect on the published number |
|---|---:|---:|---|
| the `S` swap (McCool-87 instead of holding ours) | 0.926925 | −0.07588 | made it **7.3 % too low** |
| the column choice (uncapped instead of `ls2d_hs`) | 1.107068 | +0.10172 | made it **10.7 % too high** |
| **net** | **1.026174** | **+0.02584** | **2.6 % too high** |

**Both individual errors are also inside `docs/46`'s 0.1644 materiality bar**, so no single
clause of §2.5 would have caught either. The near-cancellation is arithmetic luck: the two
levers have no common cause, they act on different variables, and their strata behaviour is
opposite in sign (the `S` swap is worst in the lowland, the column choice worst in the mid
belt). **Defect B is real as a description of the published number and immaterial as a
correction to it.** Reporting only one of those two facts would misrepresent the evidence.

---

## 6 — (d) The corrected lower endpoint, and why repairing Defect B does not produce it

### 6.1 The measurement

> **Source formulation with its own `L` (one-pixel limiter + eq. 14 step `m` + W&S-78 `S` +
> Desmet–Govers finite-difference `L`): area-weighted mean LS = 9.74122 = ×0.244679 of V0.**
> Erosion-weighted, from the engine re-run registered in `docs/47` §4.3: **×0.25146**.
> **Not ×0.333.**

Three independent harnesses now agree: `ls-evidence` 9.741 / ×0.245 and `ls-impact` ×0.2447
(the two reproductions `docs/47` §3.1 R6 registers, carried into its §4.3 as ×0.24466 area /
×0.25146 erosion), and this run ×0.244679. The cap variant
lands at ×0.244431, so the Defect-A cap-vs-step question moves this endpoint by 0.1 %.

### 6.2 The composition error — the actual defect in ×0.333

`docs/37` §4 candidate 0 built ×0.333 as `0.421 × 0.790`. This run reproduces that arithmetic
exactly (0.421363 × 0.789983 = **0.332869**) and then measures what it was meant to approximate:

| composition | value | vs the measured 0.244679 |
|---|---:|---:|
| `0.421363 × 0.789983` (as published) | 0.332869 | **×1.360** too high (ln 0.308) |
| `0.421363 × 0.769833` (**Defect B fully repaired**) | 0.324379 | **×1.326** too high (ln 0.282) |
| **measured directly, `V4_dg / V0`** | **0.244679** | — |

> **Repairing Defect B moves ×0.333 to ×0.324. The measured value is ×0.245. The confound was
> never the reason ×0.333 is wrong.**

The reason is that the `L`-form ratio is **formulation-dependent** and was multiplied across
formulations. Measured, on the same cells, the same lever takes three different values:

| where the `L` form is evaluated | `L_dg / L_cont` |
|---|---:|
| uncapped column (long slopes, `λ_in ≫ D`) | **0.852262** |
| `ls2d_hs` column (1 km² cap) — the isolated V5 | **0.769833** |
| **inside the source formulation** (one-pixel limiter ⇒ `λ_in` = 0 on every cell) | **0.580685** |

with the third value equal to the head-cell limit `1/[(m+1)x^m]` — derived independently in
`journal_ls-evidence` Step 4 and measured there at 0.5807, reproduced here at **0.580685**, and
measured erosion-weighted at 0.5822 by `ls-impact` (a 0.26 % difference from the area proxy, so
this particular ratio is close to weight-invariant). **A lever that spans ln 0.384 across the
formulations it might be applied to cannot be carried between them as a scalar.**

### 6.3 The corrected "how far our LS sits above source"

| basis | bracket | our LS above source |
|---|---|---|
| published (`docs/37` §4 cand. 0, `docs/35` §9.3.1, `docs/43` §1.4, nb18/nb19) | ×0.333 – ×0.421 | **2.37× – 3.00×** |
| **corrected, area-weighted proxy (this run)** | **×0.244679 – ×0.421363** | **2.373× – 4.087×** |
| **corrected, erosion-weighted — the registered measurement** (`docs/47` §4.3) | **×0.25146 – ×0.43194** | **2.315× – 3.977×** |

> **The "3.00×" upper claim is wrong. It is 3.977× erosion-weighted (4.087× on the area proxy).
> The lower claim, 2.37×, is unchanged — Defect B never touched the upper endpoint.**

This run's area-weighted correction and `docs/47` §4.3's erosion-weighted one are the **same**
finding measured two ways; where they differ (×0.2447 vs ×0.25146) the difference is the proxy's
known 2.51 % bias (`docs/47` §3.1 R7), and **`docs/47` §4.3's erosion-weighted bracket is the
registered one**. Nothing here supersedes it.

### 6.4 One uncertainty on the lower endpoint that nobody has stated

The D&G finite difference carries an aspect term `x^m` (`x` = √2 on diagonal D8 directions).
Dropping it moves the endpoint from **×0.244679 to ×0.281160** — a factor of **1.149**
(ln 0.139), below `docs/46`'s bar but not negligible against the 2.51 % proxy bias that
`docs/47` bothered to measure. **Desmet & Govers (1996) primary text has not been obtained**
(`docs/47` §4.2 item 4), so the `x^m` convention in `scripts/c3/ls2d.py` is **UNVERIFIED**, and
so is the endpoint's dependence on it. Both prior agents used the aspect term; this run adopts
the same convention and states the sensitivity rather than hiding it. **No band is invented for
it** — it is a two-point sensitivity, and which point is right is a reading question.

---

## 7 — (e) Is the corrected bracket NARROWER or WIDER, and what that does to C4.3

### 7.1 It is wider, by a factor of 2.30 in log units

| bracket | endpoints | width | ln width | `1/f_LS` |
|---|---|---:|---:|---|
| published | ×0.332869 – ×0.421363 | ×1.2659 | **0.23575** | 2.373 – 3.004 |
| **corrected, area proxy** | ×0.244679 – ×0.421363 | ×1.7221 | **0.54355** | 2.373 – 4.087 |
| **corrected, erosion-weighted** (`docs/47` §4.3) | ×0.25146 – ×0.43194 | ×1.7177 | **0.54100** | **2.3151 – 3.9768** |

> **The corrected bracket is WIDER: ln 0.541 against 0.236 — ×2.29 wider in log units on the
> erosion-weighted basis (+0.30525 ln), ×2.31 on the area proxy (+0.30780 ln). The widening
> alone is nearly twice `docs/46`'s materiality bar.**
>
> **It does not narrow. The factor-of-four uncertainty `docs/47` gives as the reason C4.3 is
> blocked is not relieved by resolving Defect B — it is where the factor of four came from.**

The identity behind this is worth stating because it makes the result checkable rather than
merely reported: **the bracket's width IS the `L`-form lever**, evaluated inside whichever
formulation is being bracketed. Published width = ln(1/0.790) = 0.2357, exactly. Corrected width
= ln(1/0.580685) = 0.5436, exactly. The bracket widened by precisely the amount the `L`-form
lever was mis-transferred by (§6.2), and by nothing else.

### 7.2 What the bracket's width actually is — and what would collapse it

The corrected bracket is **not** a band over admissible readings of the source. It has one
lever in it, and its two ends are:

- **×0.2447 / ×0.25146** — the source formulation **taken whole**, including Buarque's eq. 13,
  recorded in this project (`docs/46` §2.5, `journal_decide-ls-resolution` §1a) as
  Desmet & Govers (1996) eq. 11;
- **×0.4214 / ×0.43194** — the source's limiter, its `m` and its `S`, with **our** production
  point-rate `L` substituted in. **That is a hybrid, and nobody publishes it.** It is the same
  category of object as the `min(m, 0.5)` cap that `docs/46` §2.2 rules may never be graded
  CITED.

So the honest statement of the level is: **the source formulation, read as a whole, is a POINT
at ×0.2447 (area) / ×0.25146 (erosion)**, and the bracket exists only because the `L` form has
not been decided. `docs/47` §4.1 grades the direction of that decision **DERIVED** (the
cell-average form is the coherent one for a per-pixel MUSLE; predicted head-cell ratio ≈ 0.58,
measured 0.5807/0.580685). **This document does not make that decision** — grade CITED needs the
primary text, which is not obtained (`docs/47` §4.2 item 4), and the decision belongs to the
freezing session under `docs/46` §4.2.

### 7.3 If it did collapse, would C4.3 unblock? Measured: no

Arithmetic on `docs/47` §5.2's measured optima (α scales **exactly** as `1/f_LS`; this run
reproduces every entry of §5.2's table to within one unit in its last printed digit, which is
the check that this is the same arithmetic and not a second one):

| registered configuration | α̂ at adopted LS | at ×2.3151 | at **×3.9768** (the DG point) | (published ×3.004) |
|---|---:|---:|---:|---:|
| argmax `F_search`, β = 0.45 (G2.3 floor) | 0.258 | 0.597 | **1.026** | 0.775 |
| argmax `F_search`, β = 0.56 | 0.625 | 1.447 | **2.486** | 1.877 |
| argmax `F_search`, β = 0.65 (G2.3 ceiling) | 1.289 | 2.984 | **5.126** | 3.872 |
| implied level (geometric mean of station log-mean ratios), β = 0.56 | 1.211 | 2.804 | **4.816** | 3.638 |

Against the registered thresholds — box floor **2.0**, rail band **α̂ < 3.40**, `docs/35` hard
stop **α̂ < 3.9**: at the collapsed DG point the search **still rails at β = 0.45 and β = 0.56**
and clears only at the **top** of the G2.3 β gate. **Collapsing the bracket to a point removes
the level *range* from C4's contract item 2; it does not make the search's outcome
determinate.** `docs/47`'s verdict `C4.3-BLOCKED-UNTIL-LS-LANDS` is untouched by everything in
this document, and its §6.2 item 2 should now read as a point-or-bracket depending on H-L,
never as ×0.333 – ×0.421.

---

## 8 — What `docs/46` must do with this before it freezes (owed, not enacted)

This document edits nothing. `docs/46` is a DRAFT and is the file that inherits these.

1. **§1.1 Defect B's arithmetic is right and its emphasis is wrong.** The two confounds are
   ×0.9269 (`S`) and ×1.1071 (column); **the column is the larger**, and §1.1 presents it as the
   afterthought. Both are individually inside the materiality bar, and they nearly cancel.
2. **§2.5's H-L is REFUTED** (|ln| 0.0258 ≤ 0.1644), so §2.5's *"Consequence either way"* clause
   — which fires only if H-L is **not** refuted — **does not fire**. But the bracket still has
   to be re-derived everywhere. **§2.5 attaches the re-derivation to the wrong condition.** The
   condition that should trigger it is the one measured in §6.2 here: the composition
   `0.421 × f_L` is invalid because `f_L` is formulation-dependent (0.8523 / 0.7698 / 0.5807),
   and that is true whether or not the confound is material. A freezing session that leaves
   §2.5 as written freezes a correct conclusion with a refuted explanation attached to a clause
   that cannot fire.
3. **§1's summary line** — *"a further ×0.790 for the literal Desmet–Govers `L` gives the
   bracket ×0.333 – ×0.421"* — is wrong in both the factor and the method, and §3.5's
   `V4 + literal L` row (proxy 0.333, ≈ 99.7 Mt/yr) is wrong with it. The measured row is
   ×0.2447 area / ×0.25146 erosion; `docs/47` §4.3 gives the corresponding basin total as
   **75.3235 Mt/yr** (erosion-weighted engine re-run, not a proxy).
4. **§6.2 A2** requires the bracket ×0.333 – ×0.421 to be printed on every provisional C4.3
   artifact together with *"multiplies α̂ by 2.37× – 3.00×"*. Both must become
   **×0.25146 – ×0.43194** and **2.315× – 3.977×**. **§6.2 A4's derivation changes with it**:
   `30.0 / 3.00 = 10.0` becomes `30.0 / 3.9768 = 7.54`, and the "certainly outside" bound
   `30.0 / 2.375 = 12.63` becomes `30.0 / 2.3151 = 12.96`. (`docs/47` §5.4 already records that
   A4 is moot in the direction it was written for — the measured optimum is at the box **floor**
   — but if A4 is kept, its numbers move.)
5. **The same correction is owed** to `docs/35` §9.3.1 / :339 / :614-615 / :656 / :701 / :725 /
   :733, `docs/37` §4 candidate 0 and A2.2 (:104, :106, :177, :197-216, :265, :344, :600, :612,
   :615, :914), `docs/39` :192, `docs/43` §1.4 (:39, :137), `docs/45` §2.1 (:98),
   `src/nbgen/make_nb18.py` (:931, :984, :1231, `DG_EXTRA = 0.790` at :1267, :1338, :2443,
   :2776) and `make_nb19.py` — **as dated corrections, never as silent edits**
   (`docs/46` §2.5, §7.3 item 3). Each of those is a frozen or owned file and none is touched
   here.

---

## 9 — What this document does NOT settle

1. **Everything measured here is `f_area`, the PROXY.** `docs/46` §3.3 says `f_ero` decides.
   This harness runs no engine. The erosion-weighted values quoted in §6–§7 are `docs/47`
   §4.3's, not this run's. The one erosion-weighted check available for a quantity this run
   measures — the `L` form inside the source formulation — differs from the area proxy by
   **0.26 %** (0.5822 vs 0.5807), which is evidence that these particular ratios transfer, and
   is **not** a general licence: `docs/47` §3.1 R7 measures the proxy 2.51 % low on the V4 row.
2. **No per-station erosion-weighted `LS̄` and no slope terciles** (`docs/46` §3.3 requires both
   for the decision). `docs/47` §4.4 measures the per-station spread at 1.287×, sd(ln) 0.0769,
   **3.1× below detection** — that number is carried, not re-measured.
3. **The `x^m` aspect convention is UNVERIFIED** (§6.4) and worth ×1.149 on the lower endpoint.
4. **Nothing about which formulation should be adopted.** No lever is graded here. `docs/42`
   G4.2 is unchanged: the LS **level** is **UNVALIDATED** and stays so whatever `docs/46`
   decides (`docs/46` §8.2 item 1).
5. **Nothing about α, about the C level, the K unit system, the volume convention, P or FG.**
   They are one product, Π (`docs/42` §3.1). §7.3's α arithmetic is a **relabelling of the α
   axis**, exact for the level and silent about `F_report`, exactly as `docs/47` §5.2 states of
   itself (open item O5).
6. **`docs/23` §13.2's yield embargo is in force.** No t/km²/yr figure appears anywhere above.
7. **No uncited band was used or invented.** The only threshold applied is `docs/46`'s 0.1644,
   quoted as that document's, and `docs/48` §5.3 separately argues that bar is too narrow by
   2.9×–4.2×. **Every verdict in this document that leans on the bar (§2, §5) would survive its
   widening — an immaterial confound stays immaterial when the bar grows.** The verdicts that
   matter (§6.2's ×1.326 composition error, §7.1's widening) are stated as measurements with
   their ln values printed, so they can be re-adjudicated against any bar.

---

## 10 — Reproduction

```
python3.10 scripts/c3/ls2d_defect_b.py          # ~15 min (pit filling dominates); native 90 m
```
Gates G-A/G-B/G-C must all print PASS or the script stops before reporting anything and writes
nothing. Output: `data/processed/ls2d_defect_b.json` (levels, strata, gates, the decomposition
and its ln values). Inputs: the same DEM, minibacia grid and `scripts/c3/ls2d.py` the committed
products were built from; `data/processed/ls2d_variants_summary.json` for the V0 and V5 targets.
Process record and the pre-run prediction: `docs/agents/journal_defect-b.md`.
