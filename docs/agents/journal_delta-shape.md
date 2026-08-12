# journal — `delta-shape` agent

Task: compute `docs/46` §6.1's `Δ_shape` pre-test (docs/47 O6, docs/51 blocking item 5).
Output: `docs/53_delta_shape_pretest.md`. Started 2026-08-11.

## Orientation (step 1)

- `docs/46` §6.1 definition read verbatim (lines 479-503):
  `w_s = E_upstream(s) / Σ_s E_upstream(s)` for the **18 usable SSC stations**, under **V0** and
  **V4**, at adopted defaults, no fit; `Δ_shape = max over the 8 CAL stations of |ln(w_s(V4)/w_s(V0))|`.
- Bar: STRUCK by `docs/52`. Replacement discriminator at the `Δ_shape` site: Branch A available
  only if `Δ_shape = 0` to engine numerical tolerance; any `Δ_shape > 0` ⇒ Branch B mandatory.
- Prior bounds (`docs/51` §5.4): `≤ 0.2524`, plausibly ~0.154. Must be computed.
- Assets on disk: `data/processed/urh_ls2d_variants.csv` (V0,V1,V2a,V2b,V3,V4,V4p,V5 columns),
  `scripts/c3/ls_erosion_weights.py` (writes `urh_erosion_weights.csv`, gated on 299.5387 Mt/yr),
  `data/processed/ls2d_defect_b.json` (DG endpoint).
- NOTE: no `V4_dg` column in the variants CSV — the source-read-whole point (×0.25146) lives in
  the defect-B artifact. Candidate ambiguity #1 (which object is "V4" after `docs/51` §2.3).
- NOTE: `docs/47` §4.4 says "CAL 13"; `docs/47` §2.2 says "CAL 8"; `docs/46` §6.1 says "the 8 CAL
  stations". Candidate ambiguity #2 — need the registered CAL set from `docs/45`.

## Step 2 — the registered-V4 measurement (2026-08-11). MEASURED.

Harness `scratchpad/delta_shape.py`. Four reproduction gates, all run before any new number
was read, all **PASS**:

| gate | target | got |
|---|---|---|
| G1 basin gross erosion, adopted defaults (docs/37 A1.3) | 299.5387 Mt/yr | **299.5387088405831** (+8.8e-6) |
| G2 f_ero V1/V2a/V3/V4 (docs/47 §4.3) | 0.3624/0.5175/1.6941/0.43194 | 0.362435/0.517480/1.694054/0.431944 |
| G3 model upstream area, all 18 (`_c1_geom.csv`) | 18/18 | 18/18 exact |
| G4 per-station LS ratio extremes (docs/47 §4.4) | 0.3687 CARRASPOSO / 0.4745 BANANERA | 0.368748 / 0.474504, span 1.286798× |

**Δ_shape (registered reading: V4, normaliser = the 18 usable, max over the CAL 8)
= 0.1299456916752905**, argmax `24037390` CAPITANEJO.

Full admissible-reading grid measured (variant × normaliser × max-set): **0.12825 … 0.15894**.
Every reading > 0 by ~10^6 × any engine reproduction tolerance ⇒ **Branch B mandatory** under
docs/52's discriminator. Note for the write-up: under the STRUCK 0.1644 bar every reading would
have said "Branch A available" — the struck bar and its replacement give OPPOSITE verdicts, and
the replacement was decided blind. That must be said plainly.

Ambiguities found so far: (A) which object is "V4" after docs/51 §2.3 (registered V4 = our
continuous L, ×0.43194, vs the source-read-whole V4_dg, ×0.25146 — the latter has NO per-unit
column on disk); (B) normaliser set (18 vs the fit set); (C) Σ_s double-counts nested stations.

Next: build a per-(mini,urh) V4_dg column by a cell pass so reading (A) is measured, not inferred.

## Step 3 — the V4_dg (source-read-whole) column, built and gated (2026-08-11 23:31–23:35)

`scratchpad/v4dg_units.py`: a fresh 30,235,916-cell pass importing `scripts/c3/ls2d.py` and
`scripts/c3/ls2d_defect_b.py:block`, accumulating area-weighted LS per (mini, URH) for
`H_Lc_Smb` (=V0), `V4`, `V4_dg`, `V4p_dg`. Gates:

- basin area-weighted V0 = **39.812260149274394** (target to 1e-8) PASS
- V4/V0 area = **0.42136300143291305** vs `ls2d_defect_b.json` 0.42136300143291344 PASS
- V4_dg/V0 area = **0.24467900940970733** vs 0.2446790094097074 PASS
- per-unit V4/V0 vs the committed `urh_ls2d_variants.csv`: max rel diff **8.0e-8** (the CSV's own
  `%.6g`-class rounding), median 1.2e-8
- protected files SHA-256 UNCHANGED (`urh_ls2d.csv`, `minibacia_ls2d.csv`, `urh_ls2d_variants.csv`)

Erosion-weighted: **f_ero(V4_dg) = 0.2514648985839397**, reproducing `docs/51` §2.1's 0.25146 by
an independent aggregation route. `docs/46` §3.1 (as amended today) says the lower end's `f_ero`
"rests on ONE engine re-run; the second reproduction is owed, `docs/51` §7 item 7" — **that item
is now discharged.**

## Step 4 — NULL CONTROL

A uniform (pure level) LS factor must give Δ_shape exactly 0. Measured: **2.2204460492503136e-16**
(one machine epsilon) for f = 0.431944, 0.25146 and 1e-9; exactly 0.0 for f = 1. So the
statistic's numerical zero is ~2.2e-16 and the measured 0.1299 is **5.9e14 ×** it.

## Step 5 — CONCURRENCY NOTE

`docs/46` changed under me mid-run (704 → 1232 lines): another agent is enacting the `docs/51`
§5.6 amendment set. Re-read §6.1 at its new location (`:908-971`): **the Δ_shape definition at
`:915-920` is UNCHANGED**, and amendment (e) is now in force there as the exact discriminator.
§3.1 (`:660`) now carries a NEW `V4_dg` row named "the source formulation READ WHOLE" while V4 is
labelled "a documented hybrid, not the source read whole" — which makes ambiguity (A) live and
citable rather than speculative. I did not edit docs/46.

## Step 6 — RESULT

Δ_shape (registered reading) = **0.1299456916752905**, argmax `24037390` CAPITANEJO.
All 30 measured readings ∈ [0.0159907, 0.1638779]; the V4-family ones ∈ [0.1282524, 0.1638779].
Verdict: **BRANCH B MANDATORY** on every reading. Under the struck 0.1644 bar every V4-family
reading would have said Branch A available — opposite verdicts. Written to `docs/53`.

## Step 7 — written out

`docs/53_delta_shape_pretest.md` written (9 sections). Contains: the definition resolved term by
term against registered objects; six reproduction gates + the null control; the full-precision
per-station table for all 18; the 3-way under-specification register (U1 which object is V4 — now
LIVE because §3.1 gained a V4_dg row today; U2 the normaliser set; U3 CAL-8 vs the adjacent
"CAL 13" usage) with the value under each; the 4x3 grid; the verdict; six prohibitions; two
incidental flags (the f_area(V4) 0.421363 vs 0.421475 inconsistency between the on-disk artifacts
and docs/51 §2.2 / the amended docs/46 §3.1 cell; and the CAL-8 / CAL-13 naming collision).

Self-check on the arithmetic quoted in the doc: V4-family readings = 4 variants x 3 normalisers x
2 max-sets = 24, of which 12 take the max over the CAL 8 (range 0.1282524457-0.1451808423); the
all-30 range is 0.0159907232-0.1638778967. Two count/range errors caught and corrected before
finishing. No docs other than 53 and this journal were written; no git command run.
