# Journal: audit-harness-code

Task: adversarial correctness audit of `scripts/c3/ls2d_variants.py` (written by another agent).
Assume wrong; try to prove it. Checks (a)-(g) from the brief.

## Log

- [start] Oriented: listed scripts/c3 (ls2d.py 35570 B, ls2d_variants.py 22134 B, qpeak.py).
  Reading order: CLAUDE.md, docs/00_INDEX.md, docs/46_ls_preregistration_DRAFT.md,
  docs/47_c4_entry_verdict.md, then the script + ls2d.py.

- [check a] PASS. `m_step_eq14(tan)` -> sf = 100*tan; breakpoints verified numerically at
  exactly tan = 0.01 / 0.03 / 0.05 (i.e. 1 % / 3 % / 5 %), half-open [1,3) [3,5) >=5,
  giving 0.2/0.3/0.4/0.5. It is applied to tan(theta) (slope percent), NOT sin, degrees or
  a fraction. Matches docs/46 SS3.1 + SS1.1's step table. (R6 - whether Buarque's Sf really
  is percent - remains untested; no source PDF located yet.)
- [check f] Protected hashes 8579c128...f3c4 / 4c49b07b...1724 confirmed by me now, AND the
  same two hashes appear in scratchpad/ls_committed_hashes_before.txt written ~07:00 by an
  earlier session, 14 h before the harness ran at 21:46. mtime of both files is Aug 11 04:15
  (the ls2d.py run). Independent corroboration that nothing was overwritten.
- [check e/CSV] urh_ls2d_variants.csv V0 column vs committed urh_ls2d.csv:ls2d_hs -
  32,782 rows both, outer join all 'both', n_cells identical on every row, max rel diff
  4.9878e-06 = the committed file's own %.6g rounding floor (area_km2 shows 4.867e-06 from
  the same rounding). Anchor holds.
- [DISCREPANCY FOUND, logging early] The numbers in the agent's REPORTED RESULT do not all
  match data/processed/ls2d_variants_summary.json on disk. See next entry.
- [launched] independent re-implementation scratchpad/audit_ls_independent.py (own
  expressions incl. V0 longhand, fsum aggregation not bincount, chunk 400 not 512, plus
  R6 sensitivity variants m_step in degrees and in m/m, plus V4 with the FD L).

## THE REPORTED-RESULT DISCREPANCY (fabricated precision)

The StructuredOutput the harness agent returned does NOT match its own artifact
`data/processed/ls2d_variants_summary.json` for exactly the values that were only ever
printed to 4 decimals in its console table. Copy-pasted values agree to ulp; the rest were
reconstructed with invented trailing digits.

| quantity | agent's reported value | ls2d_variants_summary.json (authoritative) | rel diff |
|---|---|---|---|
| V2b area-wtd mean | 20.108816546932    | 20.108840138033035 | 1.2e-06 |
| V2b Andean        | 31.89528           | 31.895333143914797 | 1.7e-06 |
| V2b median        | 10.066267013549805 | 10.066278457641602 | 1.1e-06 |
| V2b ratio         | 0.5050912          | 0.5050916492215158 | 9e-07 |
| V5  area-wtd mean | 30.648845          | 30.64880685611369  | 1.2e-06 |
| V5  Andean        | 50.232913          | 50.232935837782584 | 4.5e-07 |
| V5  median        | 7.490357875823975  | 7.490399360656738  | 5.5e-06 |
| V5  ratio         | 0.7698343          | 0.7698333815060305 | 1.2e-06 |
| V4  Andean        | 27.108995          | 27.109007071766452 | 4.5e-07 |
| V4p Andean        | 27.098859          | 27.098938 (json ...09893781440437) | 2.9e-06 |

Corroboration that the JSON is the real number and the report is not: the prior harness's
own `scratchpad/ls_formulation.json` records buarque_exact andean = 27.109007071766452 -
the JSON digit-for-digit, not the reported 27.108995. And minibacia_ls2d_variants.csv rolls
up (area-weighted) to the JSON levels to 2.4e-10 for every variant, i.e. the written table
agrees with the JSON, not with the report.

MAGNITUDE: <=5.5e-06 relative. It cannot move any gate: (R4) 0.0052 vs bar 0.1644, (R10)
0.3262 vs 0.1644, (R3) ordering - all unaffected at 1e-05. It IS a reporting-integrity
defect: a successor quoting "V2b = 20.108816546932" quotes a number no computation produced.
Only the JSON / the two CSVs may be cited.

## INDEPENDENT RE-IMPLEMENTATION — the decisive test

`scratchpad/audit_ls_independent.py` (+ `.json`, `.log`). Deliberately different on every
axis except the input data: V0 written LONGHAND (not `L.ls_variants()[3]`), all eight
variants written from docs/46 SS3.1's definitions, aggregation by `math.fsum` over per-chunk
float64 partials (not `np.bincount`), chunk 400 (not 512). Shared only: the DEM, Horn slope,
pyflwdir pit-fill/D8/upstream_area, and the per-row latitude cell geometry - i.e. the input,
not the object under audit. Run 22:01-22:07, 30,235,916 cells.

| variant | ls2d_variants_summary.json | my independent value | agreement |
|---|---|---|---|
| V0  | 39.812260149274394 | 39.81226014927437  | 1 ulp |
| V1  | 13.984559495556095 | 13.984559495556091 | 1 ulp |
| V2a | 20.004561560377365 | 20.004561560377354 | 1 ulp |
| V2b | 20.108840138033035 | 20.108840138033028 | 1 ulp |
| V3  | 68.23366459596708  | 68.23366459596704  | 1 ulp |
| V4  | 16.775413430326214 | 16.775413430326214 | exact |
| V4p | 16.74916437247299  | 16.749164372472986 | 1 ulp |
| V5  | 30.64880685611369  | 30.648806856113683 | 1 ulp |

All three elevation strata likewise agree to 1 ulp. n_cells 30,235,916; basin area
256,702.35542925 km2; zero non-finite in every column; **zero** basin cells with a NaN coarse
elevation, so lowland+mid+andean = basin EXACTLY (no cell silently dropped from the strata).

Also measured, and both are new:
- `min(upslope_area / cell_area)` over the basin = **1.00400** > 1, so `min(upa, cell_area)`
  IS `cell_area` on every scored cell => V1 is exactly a one-pixel slope length and carries
  no dependence on the flow accumulation. Max deviation of V1 from `(m+1)(D/22.13)^m S`
  computed two ways = 4.26e-14.
- **V4 with the literal D&G FD L (one-pixel limiter => A_in = 0): 9.7412, x0.24468.** Third
  independent reproduction of docs/47 SS4.3's corrected endpoint (ls-impact x0.24466,
  ls-evidence 9.741 / x0.245).

## SYNTHETIC LONGHAND CHECK of variant_block (7 cells spanning tan 0.005-1.5)

max |harness - longhand| : V0 0.0, V1 0.0, V2a 0.0, V2b 0.0, V3 7.1e-15, V4 4.4e-16,
V4p 4.4e-16, V5 0.0. Every expression is what it says it is.

Decomposition of V5/V0 per cell (worth recording): V5 carries D&G eq.11's contour-width
factor 1/x^m as well as the finite difference. On a diagonal-flow long-slope cell
(tan 0.1581, upa 5e6) V5/V0 = 0.8147 of which 1/x^m = 0.8166 and the FD-vs-continuous part
is 0.9976; on a cardinal head cell (upa = cell_area) V5/V0 = 1/(m+1) = 0.588. So "isolates
the L form" means the WHOLE D&G L including its aspect correction. Faithful to eq. 11, and
the published 0.790 (`ls2d_dg96/ls2d`) contains the same x^m, so the H-L comparison is
like-for-like. Not a defect - an interpretation note owed to a freezing session.

## GATE ARITHMETIC re-derived from the JSON (all reproduce the report)

(R4) |ln f(V2b) - ln f(V2a)| = 0.0051992  <= 0.1644  -> FIRES
(R5) f(V2b) > f(V2a) TRUE -> does not fire
(H-L) |ln f(V5) - ln 0.790| = 0.0258588 <= 0.1644 -> REFUTED
      (harness's own reproduction of the confounded ratio: 82.87019/104.90127 = 0.7899827)
(R10) V1*V2b*V3 = 0.3040773 vs joint 0.4213630 -> |ln| 0.3262127 > bar; cap version 0.3298460
(R3)  limiter 1.0462 > m cap 0.6882 > m step 0.6830 > S 0.5388 > L form 0.2616

## (R6) UNITS SENSITIVITY — the thing the report declared untested; now MEASURED

Same 30,235,916 cells, only eq.14's `Sf` reading changed:

| reading of Sf | V2b level | f | R4 | R5 |
|---|---|---|---|---|
| **100*tan (percent, as implemented)** | 20.1088 | 0.50509 | FIRES (0.0052) | does not fire |
| degrees | 19.9012 | 0.49988 | FIRES (0.0052) | **FIRES - sign wrong** |
| m/m (fraction) | 6.4828 | **0.16283** | **does NOT fire (1.1268)** | **FIRES** |

So H-M's field clause is refuted under ALL three readings, but by different clauses, and the
report's sub-verdict *"(R5) does not fire, the sign is right"* is NOT robust to the units
question it correctly declares open. m/m is physically inadmissible (breakpoints at tan 1/3/5)
and percent is corroborated by ls-evidence S7 (Benavidez et al. 2018 Table 5 row 1), but no
primary Buarque text is in the repository, so (R6) stays NOT SETTLED.

## VERDICT (checks a-g)

a PASS (with the R6 caveat quantified above) | b PASS | c PASS | d PASS | e PASS, and by a
stronger route than the coded 1e-3 gate | f PASS | g no try/except anywhere, no sampling, no
subsetting, three writes all to NEW filenames. One LATENT silent fallback: `build_urh_coarse`
accepts the cached `urh_coarse.npz` on a shape match alone with no content check - a stale
cache would mis-split the (mini,URH) table silently (basin levels unaffected). Benign here:
n_cells identical to committed urh_ls2d.csv on all 32,782 rows.

NOTHING FOUND THAT MOVES A HEADLINE RATIO. The single real defect is in the agent's REPORTED
numbers, not in the code or the artifacts (see the discrepancy table above).
