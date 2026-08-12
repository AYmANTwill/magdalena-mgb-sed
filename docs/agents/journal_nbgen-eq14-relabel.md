# Journal - agent `nbgen-eq14-relabel` (T2b: code + notebooks share)

Opened 2026-08-12. Crash journal: appended as I go, never only at the end.

## Ownership (write)
- `src/nbgen/make_nb18.py`
- `src/nbgen/make_nb19.py`
- `notebooks/18_musle_construction.ipynb`
- `notebooks/19_c3_gate_and_c4_setup.ipynb`
- DOCSTRING-ONLY edits to `src/mgb_sediment.py`
- this journal

Nothing else. Four other agents run in parallel on disjoint files.

## Task
- JOB 1: eq.-14 mislabel (`min(m,0.5)` cap mislabelled as Buarque eq. 14) in both generators.
- JOB 2: superseded LS bracket (`x0.333 - x0.421`, `2.37x - 3.00x`, `x0.790`) in both generators.
- JOB 3: `src/mgb_sediment.py`:213 docstring factor 2.37x-3.00x -> 2.3151x-3.9768x.
- JOB 4: regenerate, re-execute, verify 299.5387 (nb18) and 248.7298 (nb19) FROM EXECUTED OUTPUT.

## Log

### 0. Start

Read, in the ordered brief's order: `CLAUDE.md`, `docs/00_INDEX.md` (via CLAUDE.md pointers),
`docs/47_c4_entry_verdict.md` in full, `docs/46_ls_preregistration.md` §0-§2.2 / §3.1-§3.3 / §7.3,
`docs/37_c3_closure.md` A3 header + A3.1 (the DECISION card) + A3.2 (the rescaled alpha) + A3.3 head.

### 1. BASELINE TEST SUITE (JOB 4 step 1) - measured, not assumed

```
cd C:\dev\magdalena-mgb-sed; python3.10 -m pytest -q
```
tail of executed output:
```
........................................................................ [ 47%]
........................................................................ [ 94%]
.........                                                                [100%]
============================== warnings summary ===============================
tests/test_transport.py::test_full_basin_decade_is_nan_free
  ...UserWarning: URH cell areas ... differ by more than 5% on 12.9% of cells ...
153 passed, 1 warning in 70.37s (0:01:10)
```
**BEFORE = 153 passed, 1 warning.** The brief's "140" is stale; 153 is the real number and it
matches the brief's own MEASURED STATE table.

(First attempt piped through `Select-Object -Last 25` into a background task and produced an
EMPTY output file with exit code 0 - a reminder that an exit code is not an observation. Re-run
redirecting to a file, then read the file. Recorded because the brief demands verification from
executed output.)

### 2. SITE INVENTORY - grepped myself, NOT taken from the brief

`grep -n "0\.502|eq\. 14|0\.790|2\.37|3\.00|0\.333|0\.421|1\.714|0\.351|hard-capped|multiply out|0\.302"`

**`src/nbgen/make_nb18.py`** - 14 live sites (brief named 4):
| line | what |
|---|---|
| 931 | print: *"the same ratio measured 0.790 at 90 m and 0.794 at 740 m"* - a TRUE statement of what `journal_c31-ls2d` §S4 measured, but with no disclosure that 0.790 does not isolate the `L` form |
| 984 | reading `shows=`: *"0.789 of the primary - matching the 0.790"* - same |
| 1225-1228 | the four-row lever table (`m` row mislabelled "his eq. 14 ... hard-capped at 0.5", factor 0.502) |
| 1231 | *"a further x0.790, giving the bracket x0.333 - x0.421 ... our LS is 2.37x - 3.00x"* |
| 1234 | **product-as-joint**: `0.502 x 1.714 x 0.351 = 0.302 != 0.421` |
| 1239-1245 | consequence on the level: 99.8-126.1 Mt/yr + the proxy caveat |
| 1246-1250 | consequence on the guards: alpha ref 3.9-5.0, band 2.0-9.9, hard stop 11.8-14.9 |
| 1262-1288 | the CODE cell: `LEVERS` label "capped 0.5" + 0.502, `DG_EXTRA = 0.790`, product print, rescaled-band print |
| 1304 | plot title *"product of the three = 0.302, joint = 0.421"* |
| 1332-1340 | reading `shows=`: x0.502, product 0.302, 2.37x-3.00x, band 2.0-9.9 / stop 11.8-14.9 |
| 2443 | clause-2 row: *"ours is 2.37x-3.00x the level alpha = 11.8 belongs to"* |
| 2776 | §7.4 wrong-beliefs table: *"2.37x-3.00x the source formulation's level"* |
| 2808 | §7.6 item 3: *"measured at 2.37x-3.00x"* |
| 2812 | §7.6 item 5: *"2.4-3.0x too high"* |
| 2981 | §8 what-is-not-established item 2: *"Ours is 2.37x-3.00x"* |

**`src/nbgen/make_nb19.py`** - 5 live sites (brief named 3):
| line | what |
|---|---|
| 437 | *"section 6.4's unresolved LS question points the other way by 2.37x-3.00x"* |
| 2093 | reclassification table: *"ours is 2.37-3.00x high in level"* |
| 2385-2392 | §6.4 lead-in: *"differs ... in **three** ways"* (it is four levers) |
| 2396-2411 | the `LSLEV` DataFrame (step mislabel, 0.333/0.421), the product-as-joint print, the 1/0.421-1/0.333 print, the 99.8-126.1 print, the "PROXY not a re-run ... has NOT been done" print |
| 2418-2435 | plot: naive-product line, x0.333-x0.421 bar, annotation |
| 2447-2461 | reading `shows=` / `means=`: x0.302 vs 0.421, 2.37x-3.00x, 99.8-126.1, *"The comparison has NOT been made"* |

`false positives` deliberately NOT changed: nb18:1078 (`1,053.00`/`808.62` water LS), nb18:2310-2312
(bar-plot offsets), nb19:590/659/710 (NEH sheet DR 0.3333 - a different quantity), nb19:919
(`re_lo` random-effects CI list).

**No assertion in either generator's integrity block depends on the bracket.** nb18 `chks`
(:3031-3050) gates 39.812 / 299.5387 / 248.7298; nb19 `checks` (:2731+) gates 299.5387 / 248.7298 /
1.2043 / 363.4245196 / 0.684406 and 25 others, none of them an LS-bracket number. So the relabel
cannot move the two headline numbers **by construction** - which I will still verify from output.

### 3. EVERY NUMBER I AM ABOUT TO WRITE, MEASURED FIRST

Standing rule: MEASURE BEFORE ASSERTING. I did not copy the brief's numbers on trust.

```
python3.10 -c "... math on the registered factors ..."
```
executed output:
```
ero product step : 0.3205262902296241
ero product cap  : 0.3177246791318452
joint/product ero: 1.347608646050708          <- x1.34762, matches docs/52 §1.1 and the brief
area product step: 0.30411239291243997
area joint/prod  : 1.3859185282243696
step/cap ero     : 1.0088177320862641   area: 1.0052142208919104
1/f upper        : 2.315114922304743    1/f lower: 3.976775630318937
ln ratio         : 0.541012019046799
-ln 0.580685     : 0.543546837831505
exp(-0.541012...): 0.5821587983627508
gap ln           : 0.002534818784706072
alpha ref        : 2.9672280000000004  5.0969392000000004
band low         : 1.4836140000000002  2.5484696000000002
band high        : 5.934456000000001   10.193878400000001
hard stop        : 8.901684            15.290817599999999
loads            : 75.32200372505304   129.38394805143685
proxy bias ero/area upper: 1.0248389584198352   lower: 1.0277138223121463
hybrid/source    : 1.717744372862483
0.852262*0.926925: 0.78998295435       <- the x0.790 factorisation confirmed to 5 s.f.
```

**A DEFECT I FOUND IN THE BRIEF'S OWN WORDING, and did NOT propagate.** The brief's JOB 2 tells me
to write *"ln(0.43194/0.25146) = 0.5410 = -ln 0.580685"*. **That identity does not hold.**
`ln(0.43194/0.25146)` = 0.541012 (0.5410027585442313 on the exactly-rounded factors) but
`-ln(0.580685)` = **0.543546837831505** - a gap of **0.00253 ln**; and
`exp(-0.541012) = 0.582159`, so 0.5410 pairs with **0.58216**, not 0.580685. Both constituents are
separately correct; the **equation between them is not**. I therefore wrote
`ln(0.43194/0.25146) = 0.5410` and stated the 0.580685 in-formulation `L`-form ratio **separately**,
never as an identity. Immaterial to every verdict. (Independently reported by the `a3-enactment`
agent for `docs/46`:127 and `docs/51` §2.3 - files I do not own, so I report and do not fix.)

Also noted: `1/0.431944` = 2.3151149 while `docs/37` A3.2 prints 2.315136361531694 (from 0.43194
exactly). Both round to the registered **2.3151x**; I quote 2.3151x and print the full value from
the factor the cell actually holds, so the two can never silently disagree.

### 4. EDITS - `src/nbgen/make_nb18.py`

All 14 sites addressed. Method: correct the claim, **keep the pedagogy**, and where a superseded
number is still needed for identifiability, keep it **inside an explicit "this was wrong" frame**
(the house pattern) rather than deleting it.

1. **§3.6 lever table + prose** (was 1219-1260): three levers -> **four**; two columns,
   `f_ero` (DECIDES) and `f_area` (proxy, per `docs/46` §3.3); the `m` row relabelled to the
   **eq.-14 STEP** (printed p. 47, `Sf` in slope PERCENT) at **x0.522043 ero / x0.505092 area**;
   an `L` row added at **x0.580685** in-formulation; the two joints separated into `V4` HYBRID
   (0.431944 / 0.421475) and `V4_dg` SOURCE READ WHOLE (0.25146 / 0.2446790094097074). Added a
   boxed, dated **label correction** naming `min(m,0.5)` as the CAP (x0.517480 / x0.502472),
   NOBODY'S published formulation, never gradable CITED, and recording that the published joint
   x0.421 **was already the step** (16.775413430326214 to 15 s.f.), so the mislabel touched the
   single-lever label only. Replaced the product-as-joint sentence with the measured **ratio**
   joint/product = **x1.34762**. Replaced the bracket with **[0.25146, 0.43194]** ero,
   `1/f_LS` = **2.3151x-3.9768x**, engine loads **129.3840 / 75.3235 Mt/yr**. Added the structural
   correction (POINT vs HYBRID; the span IS the `L`-form lever) and the x0.790 factorisation
   (0.852262 x 0.926925, wrong column, formulation-dependent 0.852262 / 0.769833 / 0.580685,
   and the residual x1.326 after a complete `S` repair). Rescaled alpha: reference **2.967-5.097**,
   band **1.484-10.194**, stop **8.902-15.291**, collapsing to **2.9672 / 8.9017**. Added the A3
   ceiling block: DETERMINED and RECORDED, **NOT YET EXERCISABLE**, no default moved, LEVEL still
   UNVALIDATED, C3 OPEN, C4.3 BLOCKED.
2. **the §3.6 code cell** (was 1262-1288): deleted `JOINT` and `DG_EXTRA` (both derived from the
   superseded 0.790 / 16.775-over-39.812 route). Now holds the registered factors as named
   constants with `f_ero`/`f_area` pairs, prints the step/cap ratio, prints non-multiplicativity as
   a **ratio in both weightings**, prints the bracket, the `L`-form formulation-dependence, the
   x0.790 factorisation, the engine endpoint loads, the proxy bias, the rescaled alpha with its
   "passes and fails NOTHING" ceiling, and the A3 decision card including
   `ls2d_column={GEO.ls2d_column!r}` read live from the loaded geometry so the notebook can never
   claim a default that is not in force.
   *Caught before execution:* my first draft printed `{ADOPT:.4f}` here. **`ADOPT` is not defined
   until line 1877, well after §3.6** - it would have raised `NameError` and killed the run.
   Replaced with the literal 299.5387 + a `docs/47` §4.3 citation.
3. **the §3.6 figure**: left panel now 4 levers + 2 joints on `f_ero`; the naive product is drawn
   as a single purple **x** labelled *"NOT a candidate for the joint: joint/product = x1.34762"* -
   the pedagogy of "they interact" survives, the false claim does not. Right panel now three
   **engine** loads (299.5387 / 129.3840 / 75.3235) with the `L`-form lever annotated between the
   last two, replacing the old area-weighted-mean-LS bars.
4. **the §3.6 reading** (what/shows/means): rewritten on the four levers, the ratio, the
   POINT-vs-HYBRID structure, the superseded bracket named as superseded, and **four** things the
   figure does not license (was two) - the two new ones being "the rescaled alpha is not a test"
   and "A3 changed nothing in this notebook".
5. **:931 (print) and :984 (reading)**: the `ls2d_dg96/ls2d` = 0.790/0.789 cross-check is retained
   as a **coding** cross-check, with an added CAUTION that it is **not** the `L`-form lever, its
   exact factorisation, the wrong-column problem, and the formulation-dependence.
6. **the CLAUSES table**: clause 2 stays **NOT MET**; reason text corrected to 2.3151x-3.9768x and
   extended with A3's recorded-not-exercised status and the outstanding SHAPE decision.
7. **§6's "clauses 2 and 4' point opposite ways"**: 2.4-3.0x -> **2.3151x-3.9768x**, and 3.9768x at
   the adopted point.
8. **§7.4 wrong-beliefs table**: corrected the alpha row and **added two new rows** - the
   2.37x-3.00x/eq.-14 belief and the multiply-out belief. This is the right home for them: §7.4
   exists to list beliefs that were written down, acted on, and then measured.
9. **§7.6**: item 3 rewritten (UNVALIDATED level, CITED-but-unexercised formulation, "a cited
   formulation is not a validated level"); item 5's 2.4-3.0x corrected; **new item 6** on
   non-multiplicativity.
10. **§8 "what is not established" item 2**: retitled to *the topographic LEVEL*, corrected factor,
    A3 status, level still UNVALIDATED.

### 5. EDITS - `src/nbgen/make_nb19.py`

All 5 sites addressed.

1. **:437** direction-of-travel line: 2.37x-3.00x -> **2.3151x-3.9768x**, + 3.9768x at the adopted
   point, citing `docs/37` A3.
2. **:2093** reclassification table, LS SHAPE row: corrected factor; added that the **level**
   question is now decided (CITED, `f_LS` = 0.25146) but RECORDED-not-EXERCISED while the **shape**
   question is untouched by that. Row stays **STILL A DEFECT**.
3. **§6.4 lead-in**: three ways -> **four**; the `f_ero`-decides / `f_area`-proxy rule stated; and a
   boxed block carrying **all three corrections** (the eq.-14 mislabel with both factors and the
   x1.008878 immateriality; the superseded bracket with the POINT/HYBRID structure and the x0.790
   factorisation; and the product-is-never-the-joint rule with joint/product = x1.34762).
4. **the §6.4 code cell**: `LSLEV` rebuilt with 6 rows (4 levers + 2 joints) and **two factor
   columns**; the cap printed separately as not-eq.-14 and never-CITED; non-multiplicativity printed
   as a ratio in both weightings; the bracket, the `L`-form formulation-dependence and the x0.790
   factorisation printed; the endpoint loads switched from `ADOPT*0.333`/`ADOPT*0.421` **proxy
   arithmetic** to the **engine re-runs 129.3840 / 75.3235** with the proxy bias stated; and an A3
   decision card. The old *"the exact figure needs the pre-registered C3.1 re-run, which has NOT
   been done"* is now false and is replaced by *"the comparison HAS now been made"* with the
   not-exercised / UNVALIDATED / C3-OPEN / C4.3-BLOCKED qualifiers.
5. **the §6.4 figure**: left panel 4 levers + 2 joints on `f_ero`, product as a labelled purple **x**
   marked NOT a candidate; right panel three engine loads instead of a x0.333-x0.421 floating bar,
   with the `L`-form lever annotated. **the §6.4 reading**: rewritten; the *means=* paragraph now
   states that the comparison **has** been made and gives **three separate reasons clause 2 still
   fails**.

### 6. EDIT - `src/mgb_sediment.py` DOCSTRING ONLY

Site: the module docstring's clause-2 bullet (was :212-215). **No executable line touched.**
Verified `ast.parse` succeeds and that `ls2d_column: str = "ls2d_hs"` (:796, :840, :903),
`urh_ls2d: str = "urh_ls2d.csv"` (:902), `cp_revision: str = DEFAULT_CP_REVISION` (:901),
`volume_convention` and `k_unit_system` defaults are all **byte-identical** to before.

Content: factor corrected to **2.3151x-3.9768x**; the old sentence quoted inside the correction so
it stays identifiable; the **status word changed** - and it changed because A3 changed it. Under
`docs/46` §4's ladder, UNRESOLVED means *two admissible readings survive*; A3 records that **no**
lever has a second admissible reading and all four are **CITED**, outcome **ADOPT-SOURCE**. So the
FORMULATION is no longer UNRESOLVED. What replaced it is not a promotion: the docstring now says
the formulation is DECIDED and **RECORDED, NOT YET EXERCISABLE**, that nothing in the module changes
and that this is deliberate, and that the **LEVEL remains UNVALIDATED** (`docs/42` G4.2) - *a CITED
formulation is not a validated level, and a fitted one is not either*. Clause 2 stays **NOT MET**.
Added the eq.-14 step/cap correction and the never-quote-the-product rule.

### 7. REGENERATION

```
python3.10 src/nbgen/make_nb18.py  ->  wrote notebooks/18_musle_construction.ipynb
                                        85 cells: 47 markdown, 38 code, 16 with figures
python3.10 src/nbgen/make_nb19.py  ->  wrote notebooks/19_c3_gate_and_c4_setup.ipynb
                                        82 cells: 53 markdown, 29 code, 19 with figures
```
Both generators take **no arguments**; `OUT` is hardcoded (nb18 :22, nb19 equivalent).

### 8. FIRST EXECUTION OF nb18, AND A PRECISION DEFECT THE OUTPUT CAUGHT

nb18 executed: `EXIT=0`, `[NbConvertApp] Writing 1859921 bytes`. **But an exit code is not an
observation**, so I parsed the executed JSON:

```
cells 85 | code cells 38 executed 38 | ERROR outputs: 0
'299.5387'  in executed OUTPUT of code cells [15, 20, 24, 28, 30, 32]
'248.7298'  in executed OUTPUT of code cells [28, 32, 37]
'0.522043'  in executed OUTPUT of code cells [15]
'2.3151'    in executed OUTPUT of code cells [15, 30]
'3.9768'    in executed OUTPUT of code cells [15, 30]
'0.25146'   in executed OUTPUT of code cells [15]
'all integrity assertions passed'  in executed OUTPUT of code cells [37]
'1.34762'   in executed OUTPUT of code cells []          <-- ABSENT.  INVESTIGATED.
```

**The registered `x1.34762` was NOT in my output.** Rather than adjust the text to match my code, I
measured which input produces the registered value:

```
python3.10 -c "J=0.431944
for m in (0.52204, 0.522043):
    p=0.362435*m*1.694054; print(m, p, J/p, f'{J/p:.5f}')"
m=0.52204   product=0.3205244482762396  joint/product=1.3476163903345526  ->  1.34762
m=0.522043  product=0.3205262902296241  joint/product=1.347608646050708   ->  1.34761
```

**Diagnosis: the registered `x1.34762` is computed from the `m` step at FIVE decimals, 0.52204** -
which is what `docs/46` §1 and `docs/52` §1.1 print - while `docs/46` §3.1's variant table prints
the same lever at SIX decimals, **0.522043**, which gives **x1.347609**. **One measurement, two
printed precisions - not two numbers.** My draft had paired the 6-d.p. product (0.3205263) with the
5-d.p. ratio (x1.34762), which is the kind of mismatch a later reader correctly reads as a defect.

**Repair, applied in all four places** (nb18 markdown, nb18 code cell + figure label, nb19 markdown,
nb19 code cell + figure label, `mgb_sediment.py` docstring): the **registered** product 0.3205244
and ratio **x1.34762** are stated as the primary pair, the 6-d.p. pair 0.3205263 / x1.347609 is
printed beside it with an explicit note that it is the same measurement at a different precision,
and both are printed **in the same output block so they can never appear to disagree**. This is the
same discipline I applied to `1/0.431944` = 2.3151149 vs `docs/37` A3.2's 2.315136361531694.

This is a **defect I introduced and caught by measuring** - recorded per the project's standing
rule, not smoothed over.

### 9. SECOND REGENERATION + EXECUTION OF BOTH NOTEBOOKS

```
python3.10 src/nbgen/make_nb18.py  ->  85 cells: 47 markdown, 38 code, 16 with figures
python3.10 src/nbgen/make_nb19.py  ->  82 cells: 53 markdown, 29 code, 19 with figures
python3.10 -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 \
    notebooks/18_musle_construction.ipynb
python3.10 -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 \
    notebooks/19_c3_gate_and_c4_setup.ipynb
```
Result: `NB18_EXIT=0`, `NB19_EXIT=0`; `Writing 1861324 bytes to notebooks\18_...ipynb`,
`Writing 1840740 bytes to notebooks\19_...ipynb`.

**VERIFIED FROM THE EXECUTED JSON, not from the exit codes.**

nb18: `code cells 38 executed 38 | ERROR outputs: 0`
| literal | present in the executed OUTPUT of code cells |
|---|---|
| `299.5387` | 15, 20, 24, 28, 30, 32 |
| `248.7298` | 28, 32, 37 |
| `x1.34762` | 15 |
| `0.3205244` | 15 |
| `0.522043` / `0.517480` | 15 |
| `2.3151` / `3.9768` / `0.25146` | 15, 30 / 15, 30 / 15 |
| `all integrity assertions passed` | 37 |

nb19: `code cells 29 executed 29 | ERROR outputs: 0`
| literal | present in the executed OUTPUT of code cells |
|---|---|
| `248.7298` | 1, 28 |
| `299.5387` | 1, 24, 28 |
| `x1.34762` / `0.3205244` / `0.522043` | 24 |
| `2.3151` / `3.9768` / `0.25146` | 24 |
| `integrity assertions passed` | 28 |

Both LS cells' full stdout was read and is quoted in §11 below. **Neither headline number moved.**

### 10. A DISCREPANCY IN A FILE I DO NOT OWN - `docs/46`'s x1.008878

The executed output printed the eq.-14-step / cap ratio as **x1.008818** erosion-weighted. Frozen
`docs/46` prints **x1.008878** at six sites (:163, :208, :265, :448, :454, :1095), all sourced to
`docs/49`. That is not a rounding difference at the digit that matters, so I measured it:

```
0.522043 / 0.517480 = 1.0088177320862641      -> x1.008818
0.505092 / 0.502472 = 1.0052142208919104      -> x1.005214
back-solve: 0.517480 x 1.008878 = 0.5220742    (registered step is 0.522043 - does NOT match)
back-solve: 0.502472 x 1.005212 = 0.5050909    (registered step is 0.505092 - matches to 6 s.f.)
```

**Finding.** Recomputed from **`docs/46` §3.1's own registered pair** - `f_ero(V2b)` = 0.522043 and
`f_ero(V2a)` = 0.517480 - the erosion-weighted ratio is **x1.008818**, not the **x1.008878** the same
document prints in six other places. Back-solving confirms the two cannot both be right:
0.517480 x 1.008878 = 0.5220742, which is not 0.522043. The shape of the difference
(**1.008818 -> 1.008878**) is a **digit transposition**. The **area-weighted** figure has no such
problem: x1.005214 vs the printed x1.005212, agreeing to 6 significant figures.

**Materiality: NIL.** Both readings are ~0.9 %, both are far inside `docs/49`'s conclusion, and
`docs/46`'s verdict on Defect A - *"REAL as a label, IMMATERIAL as a level"* - is unchanged either
way. It also cannot touch the joint, because `docs/46` §3.1 amendment (b) establishes that the
published x0.421 joint **was already the step**.

**Disposition: REPORTED, NOT FIXED.** `docs/46` is FROZEN and is not in my ownership block, and
`docs/49` (the primary) is not either. What I *did* do, because a notebook that silently prints a
different number from a frozen document looks like the notebook's error: both generators now print
the recomputation, the back-solve, the transposition diagnosis, the immateriality and the words
*"REPORTED, not fixed - docs/46 is FROZEN and is not ours"* **in the executed output itself**.

Cosmetic fix made in the same pass: nb18's plain-text lever print was leaking LaTeX (`$m$`,
`km$^2$`) because the label strings are shared with the matplotlib axis; the print now strips `$`
and renders `^2` as `2`. No number affected.

### 11. FINAL REGENERATION + EXECUTION (the run of record)

```
python3.10 src/nbgen/make_nb18.py   -> 85 cells: 47 markdown, 38 code, 16 with figures
python3.10 src/nbgen/make_nb19.py   -> 82 cells: 53 markdown, 29 code, 19 with figures
python3.10 -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 <each>
NB18_EXIT=0
NB19_EXIT=0
```

**VERIFIED FROM THE EXECUTED JSON.** Both notebooks: **every** code cell executed, **zero** error
outputs.

```
18_musle_construction.ipynb   code cells 38  executed 38  ERROR outputs 0
   basin gross HILLSLOPE erosion   299.5387 Mt/yr  (2,994,977,042.2609 t over 3652 d)
   PASS  adopted basin total matches the documented 299.5387 to 1e-3
   PASS  prior basin total matches the documented 248.7298 to 1e-3
   all integrity assertions passed.

19_c3_gate_and_c4_setup.ipynb  code cells 29  executed 29  ERROR outputs 0
   PASS  the adopted basin total reproduces the documented 299.5387 Mt/yr
   PASS  the prior-C basin total reproduces the documented 248.7298 Mt/yr
   all 31 integrity assertions passed.
```

**BOTH HEADLINE NUMBERS REPRODUCED. NEITHER MOVED.** `299.5387` in nb18 code cells
[15, 20, 24, 28, 30, 32] and nb19 [1, 24, 28]; `248.7298` in nb18 [28, 32, 37] and nb19 [1, 28].
Corrected literals present in the executed output of both: `x1.34762`, `x1.008818`, `1.008878`
(the disclosure), `REPORTED, not fixed`, `2.3151`, `3.9768`, `0.25146`.

### 12. TEST SUITE AFTER THE EDITS

```
cd C:\dev\magdalena-mgb-sed; python3.10 -m pytest -q
...
153 passed, 1 warning in 62.80s (0:01:02)     EXIT=0
```

**BEFORE 153 passed / 1 warning -> AFTER 153 passed / 1 warning. No change**, as expected: the
`mgb_sediment.py` edit is docstring-only and the generator edits touch no tested code path.

### 13. WHAT I DID NOT DO, AND WHAT I COULD NOT VERIFY

- **No git command of any kind.** No commit, add, stash, checkout, mv.
- **No frozen artifact opened for writing.** Nothing under `data/processed/sim_calibrated_v2/`;
  `urh_ls2d.csv`, `minibacia_ls2d.csv`, `urh_ls2d_variants.csv` untouched.
- **No engine default changed.** Verified after my edit that `ls2d_column: str = "ls2d_hs"`
  (:796, :840, :903), `urh_ls2d: str = "urh_ls2d.csv"` (:902) and
  `cp_revision: str = DEFAULT_CP_REVISION` (:901) are unchanged, and that `ast.parse` succeeds.
  **No executable line of `src/mgb_sediment.py` was modified** - the edit is entirely inside the
  module docstring (which `ast.parse` confirms is still well-formed and still the module docstring).
- **No `docs/*.md` file was edited** except my own journal. The other four mislabel sites
  (`docs/35` §9.3.1, `docs/37` §4 candidate 0, `docs/43` §1.4) belong to parallel agents and I did
  not open them for writing.
- **No calibration, no fit, no `KGE_ln` evaluation, no alpha-hat.** The only alpha arithmetic is the
  `docs/46` §4.2 item 3 rescaling *bookkeeping*, printed with its "passes and fails NOTHING" ceiling.
- **No `t/km2/yr`** introduced anywhere - the `docs/23` §13.2 yield embargo is respected; all loads
  are absolute flux (Mt/yr).
- **NOT VERIFIED / OUT OF SCOPE, named honestly:**
  1. I did not re-derive any `f_ero` / `f_area` value. Every factor in both notebooks is a
     **cited constant** from `docs/47` §4.3 / `docs/49` / `docs/50` / `docs/51`; the notebooks now
     say so in a comment at the top of each cell. No `V4_dg` column exists to re-derive from
     (`urh_ls2d_variants.csv` has no such column, and `urh_ls2d.csv` may not be overwritten), which
     is exactly `docs/37` A3.1.6's outstanding deliverable.
  2. **`docs/46`'s x1.008878 vs the recomputed x1.008818** (§10 above): I established the
     inconsistency and its immateriality, but **not which of the two `docs/49` actually measured** -
     I did not open `docs/49`, which is not mine. That is a one-line check for `docs/46`/`docs/49`'s
     owner.
  3. nb19's integrity check *"the level band at n=8 is +/-38 % at 95 %"* still encodes the +/-38 %
     Pi band that `docs/47` §2.2 (D2) measures as ~4x too narrow (measured SE 0.6936 ln, not
     0.1644). That is **B5**, owed as a `docs/45` §8 amendment, and it is **not** in my four JOBs -
     I left the assertion alone rather than silently move a registered number. Reported.
  4. The figures render without error but I did not inspect the rendered PNGs visually; I verified
     the plotting cells produce `display_data` outputs and raise no exception.

### 14. FILES I WROTE

| file | what |
|---|---|
| `C:\dev\magdalena-mgb-sed\src\nbgen\make_nb18.py` | JOBs 1-2, 14 sites |
| `C:\dev\magdalena-mgb-sed\src\nbgen\make_nb19.py` | JOBs 1-2, 5 sites |
| `C:\dev\magdalena-mgb-sed\notebooks\18_musle_construction.ipynb` | regenerated + executed |
| `C:\dev\magdalena-mgb-sed\notebooks\19_c3_gate_and_c4_setup.ipynb` | regenerated + executed |
| `C:\dev\magdalena-mgb-sed\src\mgb_sediment.py` | JOB 3, **module docstring only** |
| `C:\dev\magdalena-mgb-sed\docs\agents\journal_nbgen-eq14-relabel.md` | this journal |

Nothing else.
