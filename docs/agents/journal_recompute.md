# Journal — agent `recompute`

GOAL: apply the resolved conventions to `src/mgb_sediment.py`, re-run the basin decade, and
state plainly whether C3 is CLOSED or still has an open problem.

## Ground rules I am holding myself to
- Decisions resolved from SOURCE EVIDENCE / DERIVATION only.
- Every decision + justification written into THIS journal BEFORE computing or looking up
  its effect on the basin total.
- "It makes the number match" is not evidence.
- Frozen artifacts (`sim_calibrated_v2/{h2e_drivers.npz,parameters_H2E.csv,q_gauge_H2E.csv,q_gauge_H2E.npz}`)
  are read-only. No calibration launched. No git.
- Files I may touch: `src/mgb_sediment.py`, `tests/test_sediment.py`, `docs/37_c3_closure.md`,
  `docs/35_qpeak_preregistration.md` (dated amendment), this journal.

## Checklist
- [ ] 1. Read module + tests + docs/35 to know the existing option pattern.
- [ ] 2. Classify the three decisions vs the audit: AGREE / DISAGREE. Record.
- [ ] 3. Independently examine the audit's FOURTH claim (K unit system) from source evidence.
- [ ] 4. Record adopted conventions in journal BEFORE running anything.
- [ ] 5. Implement named options + documented default in `src/mgb_sediment.py`.
- [ ] 6. Extend `tests/test_sediment.py` (hand-computed unit-day regression; convention factor
       matrix; keep mass ledger). GATE: full pytest green, report count.
- [ ] 7. Re-run basin decade; report total, implied SDR, spatial gate, seasonal cycle.
- [ ] 8. Write `docs/37_c3_closure.md` with the verdict on line 1.
- [ ] 9. Dated amendment in `docs/35`.

---

## Step 1 — state read (done)
Read: `src/mgb_sediment.py` (1134 lines), `tests/test_sediment.py` (555 lines, 82 tests),
`docs/35` §1, §2, §6, §9 headers, `notebooks/09_soil_parameters.ipynb` §4,
`src/nbgen/make_nb12.py:1443` (the `parameters.npz` unit dictionary).

## Step 2 — DECISION vs AUDIT: agree / disagree table (recorded BEFORE any computation)

| decision | decision agent | independent audit | status |
|---|---|---|---|
| units | `williams_m3` correct; `pixel_km2` wrong by 1000^0.56 = 47.8630x; `swat_mm_ha` wrong by 10^0.56 = 3.6308x | same conclusion, re-derived from Williams' English-unit form by hand (95 -> 11.7826) | **AGREE** |
| LS aggregation | area-weighted arithmetic MEAN of per-cell LS, MUSLE applied per DEM pixel; factor vs current code = 1.000 | "application-scale, LS-aggregation ... already correct (factor 1.000 each)" | **AGREE** |
| LS resolution | keep native 90 m COP90, no correction, no reference-resolution rescaling; retire the uncited "mountainous 2-10" gate | "LS-resolution choices are all already correct (factor 1.000)" | **AGREE** |
| **K unit system** | *not covered by any decision agent* | NEW claim: K is stored in SI USLE units but alpha = 11.8 needs US-customary K numerics -> a further 7.5925x | **audit-only; verified independently below** |

No DISAGREEMENT exists between the two derivations on any of the three decisions, so all
three are implemented. The fourth item is an ADDITION, not a conflict; I do not take it on
the auditor's word — §3 below is my own verification from repository source text.

I verified the units derivation arithmetic myself before accepting it:
1 acre-ft = 1233.4818375 m3, 1 cfs = 0.028316846592 m3/s, product = 34.92823 ;
34.92823^0.56 = 7.31494 ; 1 short ton = 0.90718474 t ;
95 * 0.90718474 / 7.31494 = **11.7818**, i.e. 0.15 % from 11.8. The conversion touches only
Q and q_p (dimensional) and the yield; **K, C, P, LS are carried through untouched**, so the
11.8 pair belongs to the US-customary NUMERIC values of K/C/P/LS. That last clause is what
makes §3 unavoidable.

## Step 3 — the FOURTH error, verified from this repository's own source text

`notebooks/09_soil_parameters.ipynb` §4, verbatim:

> "**K by texture family** — mid-range Wischmeier & Smith (1978) class values **converted to
> SI (x0.1317)**, typical of tropical soils: Coarse 0.020 / Medium 0.045 / Fine 0.028 (SI)"

and `src/nbgen/make_nb12.py:1443` declares the stored units:

> `'K_musle': ('t.ha.h/ha/MJ/mm', 'minibacia_soil_params.csv:K - notebook 09, Wischmeier
> class value x IGAC drainage factor')`

Cross-check that the x0.1317 really was applied (undo it and see whether textbook
US-customary numbers come back):
0.020/0.1317 = 0.1519 ; 0.045/0.1317 = 0.3417 ; 0.028/0.1317 = 0.2126 — i.e. the classic
Wischmeier & Smith US-customary K for sand 0.15, silt loam 0.34, clay 0.21. Forward check:
0.15*0.1317 = 0.01976 -> 0.020 ; 0.34*0.1317 = 0.04478 -> 0.045 ; 0.21*0.1317 = 0.02766 ->
0.028. All three round to the stored table. **The transform is identified, not inferred.**

DECISION 4 (mine, from the two quotations above + the Williams derivation in §2):
`minibacia_soil_params.csv:K` is in SI USLE units and MUSLE with alpha = 11.8 requires the
US-customary numerics, so the engine must multiply the stored K by
`1 / 0.1317 = 7.593014` before it enters MUSLE. Equivalently one may keep SI K and use
alpha = 11.8 * 7.593014 = 89.60; the product is identical and I implement the K-side form so
that alpha stays comparable to Williams' published 11.8 (that comparability is the entire
point of the docs/35 §6.1 guard).
Residual imprecision I accept and state: the stored SI table is rounded to 3 decimals, so the
recovered US values differ from the originals by <= 1.3 % (0.1519 vs 0.15). That is a known
+-1.3 % on K, not a free parameter.

### Why this is not fitting to the answer
- Nothing in §2/§3 references the basin total, the 144-184 Mt/yr anchor, or an SDR.
- The evidence is a *forward-verifiable arithmetic identity* on three published numbers.
- Refusing to correct a demonstrated dimensional error because the correction happens to move
  the total upward would itself be a bias, in the opposite direction.
- The number I am about to compute is 47.863 * 7.593 = **363.42x** the first-run
  `pixel_km2` figure. HONESTY NOTE, stated so it cannot be discovered later: the task brief I
  was given already quoted the auditor's post-correction total (248.71 Mt/yr), so I cannot
  claim to have been blind to it. What I can and do claim is that the justification above was
  written down before I ran anything, contains no reference to that number, and would be
  unchanged if the corrected total had come out at 3 Mt/yr or 3,000 Mt/yr.
- Sanity check that this is NOT a convenient answer: 248 Mt/yr gross hillslope erosion against
  a 144-184 Mt/yr outlet load implies a delivery ratio of ~0.6-0.74, which is ABOVE the
  0.05-0.3 band the task calls physically plausible for a 257,097 km2 basin. So the corrected
  chain still fails the physical expectation, by 2-15x in gross erosion. The corrections do
  not rescue the result; they relocate the residual.

## Step 4 — conventions I am adopting (recorded BEFORE running)
- `volume_convention` default CHANGES `pixel_km2` -> `williams_m3` (x1000 product, x47.8630 load).
- NEW `k_unit_system` default `us_customary` (stored SI K x 7.593014); `si_stored` (x1.0) kept
  reachable so the previous behaviour is reproducible.
- NEW `ls2d_aggregation` default `area_weighted_mean` (factor 1.000, what the code already does).
- NEW `ls2d_resolution` default `native_90m` (factor 1.000, no rescaling).
- `pixel_area_km2` unchanged at 0.0081 km2 (per-pixel application, factor 1.000).
- Every prior convention stays reachable by name; the default change is documented with date
  and reason in the module docstring and amended into docs/35 §9.

## Step 5 — implementation (done)
`src/mgb_sediment.py`: new module-docstring section CONVENTION AMENDMENT - 2026-08-11 (both
default changes with their derivations) and LS2D AGGREGATION AND RESOLUTION; new constants
`DEFAULT_VOLUME_CONVENTION`, `K_SI_PER_K_US` = 0.1317, `K_US_PER_K_SI` = 7.593014,
`K_UNIT_FACTORS`, `LS2D_AGGREGATION_FACTORS`, `LS2D_RESOLUTION_FACTORS`; new `SedParams`
fields `k_unit_system`, `ls2d_aggregation`, `ls2d_resolution` with `k_factor` / `ls2d_factor`
properties and a `convention_summary()` reporter; new `effective_k` / `effective_ls2d` used by
BOTH the collapsed and the cells path (one conversion site, so a mismatch would surface as a
backend disagreement). `volume_convention` default `pixel_km2` -> `williams_m3`.

## Step 6 — tests (GATE)
`tests/test_sediment.py`: `LEGACY` parameter alias so every pre-amendment expected value is
now pinned explicitly; the audit's real unit-day as an exact regression
(`UNIT_DAY_LOAD_T = 1293.5691626849571` t/day, mini 16115, 2009-04-11, hand-derived in a
comment block, re-derived from literals inside the test, and checked on BOTH backends);
a files-gated twin that reads the id/date/five factors off disk (join guard); a convention
factor matrix (4 parametrized tests x each named option); the whole-amendment ratio
363.424519607167; rejection of unknown convention names; updated defaults test.
Inputs read from disk for the unit day: area 24.49 km2 (fraction 1.0 on URH 11),
K 0.019 SI, C 0.003, P 1.0, `ls2d_hs` 118.245, Qsur 26.677167892456055 mm/d at row 100,
which IS that minibacia's own max-Qsur day (asserted).
**RESULT: `python3.10 -m pytest tests/ -q` -> 96 passed, 0 failed, 0 skipped**
(`tests/test_sediment.py` alone: 50 passed; was 82 total / ~36 in this file before).

## Step 7 — the re-run (executed 2026-08-11, adopted defaults, 3,652 days x 8,672 minibacias)
Runner: scratchpad `run_c3_recompute.py` (not repo code; no repo file added).
- basin total **248.7298 Mt/yr** gross hillslope erosion (2,486,957,417 t over 3,652 d).
- legacy convention on the same run: 0.6844056 Mt/yr. Measured ratio **363.4245196071666**
  vs derived 363.4245196071666 — agreement to the last stored digit.
- ledger: `residual_t` **exactly 0.0**, `exact` True; `cells` vs `collapsed` relative
  difference **exactly 0.0**; 1.44 s.
- **The amendment is a pure LEVEL shift, proved not assumed:** per-minibacia adopted/legacy
  ratio spans 363.42451960716335-363.42451960717045 over all 8,672 units and per-day
  363.4245196071665-363.4245196071668 over all 3,652 days. So every spatial and seasonal
  ratio is numerically identical to the first run.
- implied SDR vs the 144-184 Mt/yr outlet anchor: **0.579-0.740**. Plausible band 0.05-0.30
  ⇒ gross erosion is still **1.93-2.47x** short of the SDR = 0.30 end and **11.6-14.8x**
  short of the SDR = 0.05 end.
- spatial gate: Andean 500-3000 m 931.95 vs lowland <100 m 80.25 (model-internal specific
  erosion, t/km2/yr, NOT a gauge-referenced yield) = **11.61x**; Spearman(spec, elevation)
  **+0.554**; lowland floodplain 19.2 % of area carries 1.60 % of erosion. PASS.
- seasonal: bimodal, Nov 1.2345 and May 1.1228 Mt/d against Feb 0.2532 Mt/d.
  P-LN 2011 1.0818 Mt/d vs P-EN 2015-16 0.4722 Mt/d = 2.291x; S-LN 1.2897 vs S-EN 0.3283 =
  3.928x. Annual max 2011 394.9 Mt, min 2015 132.3 Mt.

## Step 8 — VERDICT: **OPEN** (docs/37_c3_closure.md line 1)
The factor chain 0.684 -> 248.73 is fully explained (47.8630 x 7.593014, measured exact) and
no decision was left unresolved and the audit agreed — but the implied SDR 0.579-0.740 is
OUTSIDE 0.05-0.30, so the CLOSED conjunction fails on its third clause. Named residual and the
new C4 trap (a no-deposition fit now lands alpha at 6.83-8.73, INSIDE the docs/35 §6.1
expected band, so the guard can no longer catch that error) are written into docs/37.

## Step 9 — docs written, final gate re-run
- `docs/37_c3_closure.md` created; line 1 is `# 37 — C3 closure verdict: **OPEN**`.
- `docs/35_qpeak_preregistration.md`: §9.2 amendment appended (542 -> 649 lines) and the
  Amendments row of the §9 registration table updated. §9.2 answers the guard question in two
  parts: §6.1's α band is unchanged in value and meaningful for the FIRST time (it was a
  cross-unit-system comparison, 363.4245x apart, before), but it has LOST the ability to catch
  a no-deposition fit (α 6.83-8.73 now sits inside the expected band). §6.3's β band and
  §6.2's `N^(2β-1)` are structurally unaffected: a constant unit factor F moves α by F^β and
  cannot move β, and the K factor is outside the power.
- FINAL GATE re-run after all edits: `python3.10 -m pytest tests/ -q` -> **96 passed**.
- Files touched (all named by the task, plus this journal): `src/mgb_sediment.py`,
  `tests/test_sediment.py`, `docs/35_qpeak_preregistration.md`, `docs/37_c3_closure.md`,
  `docs/agents/journal_recompute.md`. No git commands run. No frozen artifact written (the
  runner lives in the scratchpad and opened the npz read-only). No calibration launched.

## Checklist — final
- [x] 1 read state  - [x] 2 agree/disagree table  - [x] 3 fourth error verified from source
- [x] 4 decisions recorded before computing  - [x] 5 implemented as named options
- [x] 6 tests extended, 96 green  - [x] 7 basin decade re-run and reported
- [x] 8 docs/37 verdict OPEN on line 1  - [x] 9 docs/35 §9.2 dated amendment

