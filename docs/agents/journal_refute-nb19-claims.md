# Journal — agent `refute-nb19-claims` (adversarial refutation)

**Task.** Adversarially refute the finding "Cell 32's runoff-ratio numbers contradict the output
of the cell it describes" (`src/nbgen/make_nb19.py:1224`). Default posture: the finding is wrong.

**Started** 2026-08-11.

## Plan
1. Read CLAUDE.md + docs/00_INDEX.md (done).
2. Read the actual generator text at make_nb19.py 1140-1240 (done — prose at 1221-1226 does
   read "2.54-3.92 (primary) or 5.25-7.34 (sensitivity)"; the code at 1150-1151 computes
   `need_P/need_S` from `1/(2*BETA_HI)` and `1/(2*BETA_LO)`).
3. Verify the EXECUTED notebook output in notebooks/19_c3_gate_and_c4_setup.ipynb — do not
   trust the generator source alone.
4. Recompute every number with python3.10.
5. Search the whole notebook + repo for any computation that yields 2.54/3.92/5.25/7.34.
6. Check the "barely touch" sub-claim and the assertion cell.

## Log
- (entries appended below as work proceeds)

## Measurements (all run 2026-08-11)

**1. The generator text (source of truth for the markdown).** `src/nbgen/make_nb19.py:1221-1226`,
the `shows=` argument of the `reading(...)` call that follows the section-2.5 code cell, reads
verbatim: *"...To hit the observed contrast the basin would need a runoff ratio of **2.54-3.92**
(primary) or **5.25-7.34** (sensitivity); the frozen hydrology supplies 1.95 and 3.36."*
The generator is clean in git (last touched by `02e7e95`), so this is the committed text.

**2. The executed notebook.** `notebooks/19_c3_gate_and_c4_setup.ipynb` has 82 cells; **cell 31**
is the code cell of section 2.5 and **cell 32** is its `reading()` markdown — the finding's cell
numbering is right. Cell 31's *stored stdout* (not an exit code) is:

```
            across the WHOLE registered beta band 0.45-0.65: 1.828x - 2.390x   vs observed 2.8-4.6x
            across the WHOLE registered beta band 0.45-0.65: 2.976x - 4.833x   vs observed 6.4-9.3x
to REACH the observed contrast the Qsur ratio would have to be 2.21-5.45 (primary) or 4.17-11.91 (sensitivity)
```

Cell 32's markdown in the *executed* file is byte-identical to the generator text. So the prose
pair (2.54-3.92 / 5.25-7.34) and the printed pair (2.21-5.45 / 4.17-11.91) sit ~15 lines apart in
the same section and disagree. **Finding's core claim: CONFIRMED.**

**3. Recomputation** (`python3.10`, `sys.path.insert(0,'src')`, `sed.WILLIAMS_BETA == 0.56` exactly):

| quantity | value |
|---|---|
| `need_P` = (2.8^(1/1.3), 4.6^(1/0.9)) | 2.2078, 5.4500 |
| `need_S` = (6.4^(1/1.3), 9.3^(1/0.9)) | 4.1704, 11.9149 |
| beta=0.56 inversion, obs^(1/1.12) | 2.5075, 3.9061, 5.2457, 7.3235 |
| `env_P` = (1.9545^0.9, 1.9545^1.3) | 1.8278, 2.3897 |
| `env_S` = (3.3598^0.9, 3.3598^1.3) | 2.9763, 4.8329 |

Matches the finding's recomputation to 4 d.p. Under the charitable (beta=0.56) reading the prose
is wrong at **three of four** endpoints in the third digit: 2.54 vs 2.51, 3.92 vs 3.91, 7.34 vs
7.32; only 5.25 is right.

**4. Is the prose pair computed anywhere in the notebook?** Regex `2\.54|3\.92|5\.25|7\.34|1/1\.12`
over **every cell source AND every stored output** of nb19: the ONLY hit is the markdown line in
cell 32 itself (plus an unrelated `365.25` in cell 6). `need_P`/`need_S` occur only at generator
lines 1150-1151/1163. **CONFIRMED — not reproduced by any computation in the notebook.**

**5. Provenance the finding did not report (new, and it strengthens the finding).** The prose pair
is quoted from **`docs/43_c3_c4_gate.md:268`**: *"...would need a ratio of 6.4 – 15.4 (primary) or
27.5 – 53.8 (sensitivity), i.e. a `Qsur` ratio of 2.54 – 3.92 or 5.25 – 7.34"*. docs/43 derives it
as sqrt of a needed **product** ratio at beta = 0.56 (product ∝ Qsur^2). But docs/43's own product
numbers are themselves off: obs^(1/0.56) = **6.2872 / 15.2568 / 27.5099 / 53.6210** against the
doc's 6.4 / 15.4 / 27.5 / 53.8 (up to +1.8 %). Solving for the implied beta endpoint-by-endpoint
gives 0.5547 / 0.5580 / 0.5601 / 0.5596 — i.e. **no single exponent reproduces all four**; they are
hand/LLM arithmetic with ~1 % noise, not an alternative well-defined quantity. So the notebook
prose is a faithful quote of a document whose numbers do not reproduce, layered on top of a cell
that computes a *different* quantity (band-wide, not at beta = 0.56).

**6. The "barely touch" sub-claim.** `env_P` = [1.828, 2.390] and `OBS_P` = [2.8, 4.6] are
**disjoint**, gap 0.41 (2.8 / 2.390 = 1.172). The notebook's own integrity cell (**cell 81**)
asserts `env_P[1] < OBS_P[0]` under the label *"beta cannot reach the observed primary contrast
anywhere in [0.45, 0.65]"* and its stored output shows **PASS** (31/31 assertions pass). So the
prose's "barely touch" contradicts a passing assertion in the same notebook. **CONFIRMED.**

**7. The "why it matters" arithmetic.** 2.54/1.9545 = 1.30x and 3.92/1.9545 = 2.01x versus
2.2078/1.9545 = 1.13x and 5.4500/1.9545 = 2.79x. Materially different, and in *both* directions:
the prose overstates the minimum required hydrology change (1.30x vs 1.13x) and understates the
maximum (2.01x vs 2.79x). CONFIRMED.

## Attempts to refute that FAILED
- Looked for an alternative legitimate formula behind 2.54/3.92/5.25/7.34 (peak-corrected observed,
  scaling by the run value SIM_BASIN_P, a different WILLIAMS_BETA): none reproduces the pair;
  `WILLIAMS_BETA` is exactly 0.56 (`src/mgb_sediment.py:537`).
- Checked whether the prose could be a *labelled* beta=0.56 statement (which would make it a second
  legitimate quantity rather than a contradiction): it is not labelled, and the two sentences
  before it are explicitly "across the *entire* registered beta band".
- Checked whether "barely touch" could refer to some other pair (the run value 2.2915, the
  peak-corrected 2.0908, the like-for-like cells of section 2.4): all still fall short of 2.8.

## VERDICT: finding NOT refuted. Confirmed in full, with one addition (provenance = docs/43 §268,
whose own numbers also fail to reproduce — so the fix touches docs/43 too, not only nb19).

- [t1] Confirmed the target text. `src/nbgen/make_nb19.py:2186` (= executed notebook **cell 61**,
  §5.4) reads: "...and **$\beta$ cannot reach the observed contrast** anywhere inside its
  registered band (section 2.5)." Unscoped, with a bare citation to §2.5.

- [t2] §2.5 (make_nb19.py:1100-1236, cells 30-32). The bound is derived from `RQ_P = 1.9545`,
  the **basin** surface-runoff ratio (journal_adj-ratio Step 1/D1). `env_P = (1.828, 2.390)`.
  Cell 31 executed output verbatim:
    `across the WHOLE registered beta band 0.45-0.65: 1.828x - 2.390x   vs observed 2.8-4.6x`
  So the envelope is a BASIN-TOTAL bound. The evidence offered is accurate.

- [t3] Cell 28 executed output verbatim (like-for-like, same stations/days/estimator, beta=0.56):
    primary (a)         n=6  obs 4.6200  sim 4.9030  obs/sim 0.9423
    primary (b) all     n=7  obs 2.9490  sim 2.9040  obs/sim 1.0155
    primary (b) ok-only n=4  obs 2.8450  sim 3.0810  obs/sim 0.9234
    sensitivity (a)     n=4  obs 9.3200  sim 4.2120  obs/sim 2.2127
    sensitivity (b) all n=7  obs 4.6500  sim 4.9980  obs/sim 0.9304
    sensitivity (b) ok  n=5  obs 6.4040  sim 4.9700  obs/sim 1.2885
  2.904 and 3.081 lie INSIDE the observed primary band [2.8, 4.6]. 4.903 lies 2.0515x beyond the
  top of env_P. beta=0.56 IS inside [0.45,0.65]. -> the unscoped statement is false for the
  station-aggregate quantity, at the band centre, with no extrapolation.
  On the SENSITIVITY pair it still holds (4.212/4.998/4.970 all < 6.4).

- [t4] Cell 34 figure rendered from the executed PNG and inspected. Teal circle 4.903 and purple
  circle 2.904 both plot clearly to the right of the blue "reachable by beta, primary" axvspan
  (1.828-2.390). Purple 2.904 sits inside the amber observed-primary bar 2.8-4.6. Cell 35's
  reading discusses position relative to the OBSERVED bands only; it does not remark that a
  beta=0.56 value sits outside its own "reachable by beta" span. Finding accurate on this too.

- [t5] REFUTATION ATTEMPTS AND WHAT THEY FOUND.
  (a) "the (section 2.5) citation is the scope qualifier" - partly true; §2.5's title, its
      derivation and its `means` (:1227) all say "basin-total", and §2.4's `means` at :1097
      already carries the correctly-scoped form: "the model's **basin-total** contrast is
      constrained to be smaller than the observed one however good the fit looks at stations."
      But the mandatory one-liner itself is unscoped, and unscoped is how it will be quoted.
  (b) "the pre-registration of record is broken" - **NO, and this is the real narrowing.**
      docs/43:264-265 registered statement: "beta cannot reach the observed **basin-total**
      contrast anywhere inside its registered band." docs/45 §6.2.3 body: "the simulated
      **basin** contrast is 1.83x-2.39x". Both documents of record ARE scoped. nb19 §5.4 is a
      restatement that drops the word. So the defect is a transcription scope-drop, not a broken
      registration.
  (c) "a genuine C4 improvement gets mis-adjudicated as a registration breach" - **overstated.**
      docs/45 §6.1's five outcomes (ADOPT / FAIL-STRUCTURE / FAIL-NUMERIC / FAIL-RAILED /
      INDETERMINATE) are decided on F_report, rails, beta in [0.45,0.65] and G1-G12. **None reads
      the ENSO contrast** - C5 runs the contrast. Harm is a mis-quotable sentence, not a verdict.
  (d) "the L4L sim medians were not run at beta=0.56" - **refuted.** journal_adj-ratio Step 1:
      "SIMULATED basin ratio 2.2915x primary ... (alpha=11.8, beta=0.56 unfitted)"; D1 defines
      the station sim as the upstream sum of the same engine's `delivered_t_day`.
      `src/mgb_sediment.py:537  WILLIAMS_BETA = _QP.WILLIAMS_BETA  # 0.56`.
  (e) "§5.4 registers the like-for-like as the headline" - **wrong attribution in the finding.**
      §2.6 (:1313, cell 35) does: "The registered headline comparison is the like-for-like one".
      §5.4 says nothing about the headline comparison.

- [t6] FIX SURFACE IS LARGER THAN THE FINDING NAMED. A third unscoped instance:
  `make_nb19.py:2762` - the label of a machine-checked assertion in cell 81:
    ('beta cannot reach the observed primary contrast anywhere in [0.45, 0.65]', env_P[1] < OBS_P[0])
  It PASSES (2.390 < 2.8) on a basin-only test, printed two rows above
    PASS  the like-for-like comparison agrees within 1.29x in 5 of 6 cells
  i.e. the notebook's own integrity list prints the unscoped claim and its counterexample together.

- [t7] INCIDENTAL, not part of this adjudication, but measured so it is not lost: cell 32's
  markdown says "the basin would need a runoff ratio of **2.54-3.92** (primary) or **5.25-7.34**
  (sensitivity)" - those are docs/43:268's numbers (the beta=0.56 inversion). Cell 31's own
  executed output prints "2.21-5.45 (primary) or 4.17-11.91 (sensitivity)" - the band-edge
  inversion (need_P/need_S). Both are internally correct for their own definition, but the
  figure-reading quotes numbers its own cell did not print. Separate defect; flagged only.

## VERDICT
NOT REFUTED. Factual core independently confirmed from executed outputs. Narrowed on three
points (primary pair only; documents of record are scoped; no C4 gate reads the contrast).
Severity medium, not high. Confidence high.
