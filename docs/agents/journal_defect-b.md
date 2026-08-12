# journal — `defect-b` (resolve Defect B of docs/46 §1.1, with numbers)

Started 2026-08-11. Task: isolate the `L`-form lever from the published ×0.790, decompose that
0.790 into its `S` swap and its column choice, correct the bracket's lower endpoint (×0.333),
and say whether the corrected bracket is narrower or wider than ×0.333–×0.421.
Deliverable: `docs/50_defect_b_resolution.md`. Nothing adopted, no default moved, no git.

## Step 0 — orientation (done)

Read `CLAUDE.md`, `docs/00_INDEX.md` (via CLAUDE.md's summary), `docs/46 DRAFT`, `docs/47`,
`scripts/c3/ls2d.py:ls_variants()`, `scripts/c3/ls2d_variants.py`,
`data/processed/ls2d_variants_summary.json`, `docs/agents/journal_ls-variants-harness.md`.

**Inherited, verified on disk in `ls2d_variants_summary.json`:**
- V0 (`ls2d_hs`) = 39.812260149274394; V5 (`L_dg96_fd`, hs basis, S held at Moore–Burch)
  = 30.64880685611369 → **V5/V0 = 0.7698333815060305**, ln = −0.26158.
- diagnostics: `D_ls2d_uncapped` (= `ls1`) 104.90126876086376; `D_ls2d_dg96_published`
  (= `ls3`) 82.87018607510596 → ratio **0.79000...**, i.e. the published 0.790 reproduces.

**A trap I nearly walked into.** `D_ls2d_mb86` is *not* "the D&G L with Moore–Burch S". It is
`ls2d.py`'s `ls2` = the **fixed m = 0.4** Moore & Burch cross-check variant on the *continuous*
L, uncapped (`scripts/c3/ls2d.py:281`). Using it as the missing intermediate would have
produced a fabricated decomposition (it would have said the L form is worth ×0.157 and the S
swap ×5.04 on the uncapped column — both wrong). **The intermediates needed to decompose 0.790
do not exist on disk and must be measured.** That is Step 1.

## Step 1 — what has to be measured, and why each column is needed

Published ratio, on the UNCAPPED column:  `R_unc = mean(L_dg·S_McCool) / mean(L_cont·S_MB86)` = 0.7900
Isolated ratio, on the hs column:         `V5/V0 = mean(L_dg·S_MB86) / mean(L_cont·S_MB86)` = 0.7698

Neither decomposes without the mixed cells. New columns (all native 90 m, same grid, same
area-weighted aggregation, `ls2d.py` imported not copied):

| id | expression | what it isolates |
|---|---|---|
| `U_Lc_Smb` | `ls1` — L continuous, S Moore–Burch, uncapped | published denominator |
| `U_Ldg_Smc` | `ls3` — L D&G, S McCool-87, uncapped | published numerator |
| `U_Ldg_Smb` | L D&G × S Moore–Burch, uncapped | **L form alone, uncapped basis** |
| `U_Lc_Smc` | L continuous × S McCool-87, uncapped | **S swap alone, uncapped basis** |
| `H_Lc_Smb` | = V0 | hs denominator |
| `H_Ldg_Smb` | = V5 | **L form alone, hs basis** |
| `H_Ldg_Smc` | L D&G × S McCool, hs basis | the published *recipe* on the *engine's* column |
| `H_Lc_Smc` | L continuous × S McCool, hs basis | S swap alone, hs basis |
| `V4`, `V4_dg` | source formulation as read, and the same with D&G L | the corrected bracket endpoint |
| `V4p`, `V4p_dg` | the cap versions of both | keeps the published row reproducible |

The decomposition is a ratio of means, so it is **path-dependent**; I will report both paths
and the spread between them rather than pick one.

(Progress appended below as it happens.)

## Step 2 — harness written and launched (22:20)

`scripts/c3/ls2d_defect_b.py`, ~4 min of LS pass after ~10 min of pit filling / D8. Design
notes worth keeping:

- **No re-implementation.** `U_Lc_Smb` and `U_Ldg_Smc` ARE `ls2d.ls_variants()`'s `ls1` and
  `ls3` — the published denominator and numerator themselves — and `H_Lc_Smb` is `ls4` = V0.
  Only the four mixed columns and the source-formulation rows are new expressions.
- **Three gates before anything is reported:** V0 = 39.812260149274394 (1e-6),
  `mean(ls3)/mean(ls1)` = 0.7900 (5e-4, the published number), `V5/V0` = 0.7698333815060305
  (1e-6). A harness that cannot reproduce those cannot be trusted with the mixed cells.
- **No memmap, no medians, no URH table.** Only area-weighted sums over basin + 3 elevation
  strata are accumulated, so the run is light and nothing new is written except one JSON.
- The committed products are SHA-256'd before and after and the script raises if either moves.

**Prediction recorded BEFORE the numbers land** (so the decomposition cannot be tuned):
the per-cell L-form ratio is `[λ_out^(m+1) − λ_in^(m+1)] / [(m+1) λ_out^m D x^m]`, which is
`1/[(m+1)x^m]` on a head cell (λ_in = 0) and `→ 1/x^m` as λ_in ≫ D. So the L-form lever must be
**closer to 1 on the uncapped column than on the hs column**, because uncapped slopes are longer.
Given `ls-evidence`'s independently measured S→McCool-87 factor of **0.908** on the hs basis, I
expect the hs-basis full recipe near 0.770 × 0.908 ≈ 0.70 and therefore a column factor near
0.70/0.790 ≈ 0.89. If the measurement contradicts this, the arithmetic above is wrong and the
prediction is what gets thrown away, not the measurement.

## Step 3 — the measurement (22:25). All three gates PASS.

```
G-A  V0        target 39.812260149274394   got 39.812260149274366   PASS (2 ulp)
G-B  published target 0.7900               got 0.7899826861390916   PASS
G-C  V5/V0     target 0.7698333815060305   got 0.7698333815060308   PASS
```
Unasked-for reproductions that also landed: S->McCool-87 on the hs basis **0.907982** vs
`ls-evidence`'s 0.908 (36.14880 vs 36.149); source method with D&G L **9.74122** vs its 9.741;
L-form inside the source formulation **0.580685** vs 0.5807 (`ls-evidence`, `ls-impact`).
`urh_ls2d.csv` / `minibacia_ls2d.csv` SHA-256 unchanged.

**The Step-2 prediction held.** L form uncapped 0.852262 > hs 0.769833 (predicted: uncapped is
closer to 1 because slopes are longer); full recipe on hs 0.701486 ≈ predicted 0.70; column
factor 0.887977 ≈ predicted 0.89. The prediction was recorded before the run and is not being
retro-fitted.

### The decomposition (basin, area-weighted; exact — both paths multiply back to 0.789983)

| | factor | ln | share of ln 0.790 |
|---|---:|---:|---:|
| L form (S held at MB86, uncapped) | 0.852262 | −0.15986 | **67.8 %** |
| S swap (McCool-87 / MB86, on L_dg, uncapped) | 0.926925 | −0.07588 | **32.2 %** |
| (S-first path) S 0.924589 then L 0.854415 | | −0.07841 / −0.15734 | 33.3 / 66.7 % |
| column choice, whole recipe (unc → hs) | 0.887977 | −0.11881 | — |
| column choice, L form only | 0.903283 | −0.10172 | — |

**Error budget, published 0.790 → isolated 0.7698:** S swap made it 7.3 % too LOW
(ln −0.0759); the wrong column made it 10.7 % too HIGH (ln +0.1017); net +2.6 % (ln +0.0258).
Both individually inside the 0.1644 bar. **The column error is the larger of the two** — the
opposite of the emphasis in `docs/46` §1.1.

### The bracket

```
published        0.332869 - 0.421363   ln width 0.23575   = ln(1/0.789983) exactly
corrected AREA   0.244679 - 0.421363   ln width 0.54355   = ln(1/0.580685) exactly
corrected ERO    0.25146  - 0.43194    ln width 0.54100   (docs/47 §4.3, engine re-run)
WIDENS by ln +0.30525 (ero) / +0.30780 (area) = x2.29 / x2.31 in log width.
```
Multiply-through error: 0.421363 x 0.789983 = 0.332869 (reproduces docs/37's 0.333 exactly);
with Defect B fully repaired 0.421363 x 0.769833 = 0.324379; **measured 0.244679**. So the
repair moves 0.333 to 0.324 and the truth is 0.245 — **fixing Defect B does not fix x0.333**.
The L-form lever takes three different values (0.852 uncapped / 0.770 hs / 0.581 inside the
source formulation, span ln 0.384) and was carried across formulations as if it were a scalar.

### Dead ends / things that did not go to plan

1. **`D_ls2d_mb86` is a decoy.** It is `ls2` = fixed m = 0.4 on the *continuous* L, not
   `L_dg x S_MB86`. Using it would have "decomposed" 0.790 into 0.157 x 5.04 — which multiplies
   out correctly and is entirely fabricated. Recorded in `docs/50` §1 so nobody repeats it.
2. **The aspect term is unverified and it matters.** `V4_dg_x1` (x = 1) gives x0.28116 against
   x0.244679 with `x^m` — a factor 1.149 on the *lower bracket endpoint*, on a convention taken
   from `ls2d.py` while D&G (1996) primary text is **not obtained** (`docs/47` §4.2 item 4).
   Stated as a two-point sensitivity in `docs/50` §6.4; no band invented.
3. **`docs/46` §2.5's consequence clause is attached to the wrong condition.** H-L is refuted,
   so the clause that orders the bracket re-derived cannot fire — yet the bracket does need
   re-deriving, for the composition reason instead. `docs/50` §8 item 2.
4. **f_ero not measured here** (no engine run). The one available check says the L-form ratio
   inside the source formulation is 0.5807 area vs 0.5822 erosion (0.26 % apart), so these
   particular ratios transfer; that is not a general licence and `docs/50` §9 says so.

## Step 4 — files

Written: `docs/50_defect_b_resolution.md`, `scripts/c3/ls2d_defect_b.py`,
`data/processed/ls2d_defect_b.json`, this journal. Nothing else. No default moved, no frozen
artifact opened, no git command run. `docs/35/37/42/43/45/46/47` read and **not edited** — the
corrections they are owed are listed in `docs/50` §8 and enacted nowhere.
