# Journal — agent `chirps-blend-arith` (H-D: blend arithmetic)

Process record. Findings go in the return value; this file records what I was asked, what I ran,
which executed output grounds each claim, and what I refused to claim.

Date: 2026-08-12. Repo `c:\dev\magdalena-mgb-sed`, branch `main`. No commits, no adds, no pushes.

## 1. What I was asked

Test **H-D: blend arithmetic**. The claim under test: matching marginals does not preserve an
area-weighted mean when the blend weight `w` correlates with rainfall magnitude. The merge is
`merged = w*Cmap + (1-w)*P`; writing `d = Cmap - P`, the surplus is
`E_area[w*d] = E_area[w]*E_area[d] + cov_area(w, d)`. If `cov_area(w,d) > 0` the merge adds water
that neither field's own mean predicts.

Deliverables demanded: (1) correlation table w vs several readings of "rainfall"; (2) the exact
`E[w]E[d] + cov` decomposition closing to +152.148 mm/yr; (3) the correlation-alone attribution via
a constant-w counterfactual; (4) per-weight-band and per-decile `w` vs `d` trend; (5) three
counterfactual areal means (constant w / de-inflated map / both); (6) an explicit statement of the
VALUE-vs-ERROR distinction and what it would take to measure correlation with the error.

Constraints I am operating under: measure before asserting; an uncited band cannot pass or fail a
gate; a negative result is publishable; verify from executed output not exit codes; no writes to
`docs/33`, `docs/30`, `docs/18`, `docs/54`; no scripts in the repo (scratchpad only); do not touch
`model_inputs_v2/` or `sim_calibrated_v2/`.

## 2. Inputs I read before measuring

* `.../scratchpad/h2_harvest.py` — read in full to check the ledger column definitions before
  trusting a single column. Confirmed from the source:
  - subsets are built as `A = (~Cnan) & (~gap)`, `B = (~Cnan) & gap`, `D = Cnan`;
  - the sums `sPA/sCrawA/sCmapA` etc. are `np.where(mask, X, 0).sum(0)` — i.e. day-sums in mm
    over that subset, per cell, so they are additive and the blend identity is exact;
  - `w = m.chirps_weight(d_near)` where `d_near = dk6[:,0]`, the k=6 IDW nearest-gauge distance;
  - the merged field is `np.where(Cnan, P, np.where(gap, C_map, w*C_map + (1-w)*P))` — identical
    to `build_merged_field()`;
  - `areal_mean` uses 365.25 and area weights; `nD` is 0 everywhere (CHIRPS never missing).
* `src/merge_chirps_gauges.py` lines 99-102 and 408-412 — confirmed
  `chirps_weight = clip((d - D_FULL_GAUGE_KM)/(D_FULL_CHIRPS_KM - D_FULL_GAUGE_KM), 0, 1)` and
  the mm/yr areal-mean formula, so `w` is the blend weight and not a proxy for it.
* `bounds_fields.csv` — read for context (H-A bracket, not my hypothesis).

## 3. Discrepancy noticed on the way in (recorded, not swept)

The brief describes F5/F6 as crediting the insertions at **0.4527 x own reporting-day mean**.
The `bounds_fields.csv` field labels written by `h3_bounds.py` say **0.414**. The mm/yr values in
the file match the brief exactly (2267.409 / 2527.237 and 2290.932 / 2541.149), so only the
*stated multiplier* differs between the brief text and the file's own label. I do not use F5/F6 in
any H-D claim, so this does not propagate into my findings — but whoever owns the H-A bracket
should reconcile the label, because a coefficient that appears as two different numbers in two
places is exactly the sort of uncited constant docs/40 retired bands for.

## 4. What I ran

Three scratchpad scripts, all reading `cell_ledger.csv` / `gauge_ledger.csv` only — no CHIRPS
reload, no DEM, no field rebuild (RAM constraint respected; peak use is one 8,672-row dataframe):

1. `.../scratchpad/hd_blend_arith.py` -> `hd_out.txt` — the six required blocks.
2. `.../scratchpad/hd_followup.py` -> `hd_followup_out.txt` — chases the E[d] mismatch,
   decomposes cov itself by decile, and asks whether any constant w passes the gate.
3. an inline `python3.10 -c` over `gauge_ledger.csv` -> `hd_gauge_out.txt` — the map's bias
   where it is verifiable at all.

### 4.1 Re-derivation control (executed output, hd_out.txt block 0)

```
gauge-only P  2036.3927 (pub 2036.393) | RAW CHIRPS 2124.7205 (pub 2124.721)
MAPPED CHIRPS 2265.7574 (pub 2265.757) | merged     2188.5404 (pub 2188.540)
surplus 152.147692 (pub 152.148)
per-cell blend identity max|LHS-RHS| = 1.3754e-04 mm/yr
nB.sum() = 35,716 of 28,504,864 = 0.1253 %;  nD.sum() = 0; max|nA+nB+nD-ND| = 0
```
Everything I claim below rests on this ledger reproducing the rejected numbers, which it does.
I also reproduced the headline 4-way exactly: map-infl blend +87.302 / chirps-vs-idw blend
+64.807 / map-infl fallback +0.0086 / chirps-vs-idw fallback +0.0298.

### 4.2 The decomposition closes to 2.25e-08 (hd_out.txt block 2)

```
E_area[w] = 0.403717 ; E_area[dA] = +229.326272 ; product = +92.582966
cov_area(w, dA) = +59.526290 ; blend term E_area[w*dA] = +152.109256
fallback E_area[dB] = +0.038436 ; TOTAL +152.147692 ; residual vs surplus +2.252e-08
```

### 4.3 DISAGREEMENT WITH A PRE-MEASURED NUMBER — stated loudly, as instructed

The brief gives `E[d] = +229.381` and `product = +92.605`. I get **+229.3263** and **+92.5830**.
I chased the definition (`hd_followup.py` block (i)) and found the cause exactly:

```
A  E_area[(sCmapA-sPA)] normalised by ND  (mine)   = 229.3263   diff -0.0547
B  E_area[(sCmapA-sPA)] normalised by own nA       = 229.3812   diff +0.0002  <-- the brief
C  E_area[sCmap_all] - E_area[sP]                  = 229.3647
```
The brief's `E[d]` divides each cell's blend-day sum by **that cell's own blend-day count nA**,
not by the window length ND. That is a defensible "mean over blend days" but it is **not the d
that enters the product-plus-covariance identity**, which requires the same ND normalisation the
blend term uses. Consequence, measured:
`92.605 + 59.528 = 152.1330` against the exact blend term `152.109256` — the brief's trio is
internally inconsistent by **+0.0237 mm/yr**. My trio closes to 2.25e-08. The `cov` value itself
is unaffected in practice (mine +59.5263 vs the brief's +59.528, agreeing to 4 significant
figures), so no conclusion changes; but I will not quote a decomposition that does not close, so
all my numbers use definition A. Magnitude 0.024 mm/yr on a 152 mm/yr surplus = 0.016 %:
immaterial to every verdict, recorded so nobody re-derives it and thinks they erred.

### 4.4 Correlation-alone attribution (hd_out.txt block 3)

```
actual merged 2188.5404 ; constant w = 0.403717 everywhere 2129.0141
difference +59.526290 ; cov_area(w,dA) +59.526290 ; agreement -2.252e-08
```
The counterfactual and the covariance agree to 2e-08. They must, and they do — the constant-w
field only changes subset A (fallback days take Cmap regardless of w), so the difference is
algebraically `E[w*dA] - E[w]E[dA]`. I report the agreement rather than assuming it.

Sensitivity: using the UNWEIGHTED mean w (0.405512) instead gives 2129.4257, difference +59.115.
The choice of which mean to hold constant moves the attribution by 0.4 mm/yr.

### 4.5 Order-dependence of the 3-way split — the caveat that constrains my verdict

The three-way attribution (cov / map inflation / raw-CHIRPS-vs-IDW) is a **sequential**
decomposition and its shares depend on the order the interventions are applied. Both orders were
computed from the counterfactual ladder in hd_out.txt block 5:

* de-correlate first: cov +59.526, then map inflation +56.997, then raw-vs-IDW +35.624
* de-inflate first:   map inflation +65.912, then cov +50.611, then raw-vs-IDW +35.624

Both sum to +152.148. So cov's share is **33.3 %-39.1 %** depending on order, Shapley-average
36.2 %. I refuse to quote a single-point "39.1 %" without this bracket, and my verdict uses the
bracket.

### 4.6 What I refused to claim

* I did **not** claim the surplus is "wrong because of the blend". cov(w,d) > 0 says how the water
  arrives, not that it should not. See 4.7.
* I did **not** claim corr(w, ERROR) — it is not identifiable. `w = 1` is *defined* as "no gauge
  within 30 km" (measured: 1,496 cells, 17.09 % of area, d_nearest 30.0-71.5 km, median 38.2 km),
  so no gauge-independent truth exists anywhere in the region that carries 64.4 % of the surplus.
  The map's bias is measurable only where gauges are, i.e. where w is smallest: at the 291 gauge
  pixels, pair-weighted C_map/G - 1 = **+0.034 %** (simple mean +0.350 %) while raw C/G - 1 =
  **-2.519 %**. The map is verified near-unbiased exactly where it is least used and extrapolated
  where it is used most. That is a structural limit of the design, not a gap in this analysis.
* I did **not** treat counterfactual (b) as a recommendation, and I flag explicitly that a uniform
  rescale of Cmap to raw CHIRPS's basin mean is a **different intervention** from H-C's (H-C is
  about why the map inflates at all; (b) just removes the basin-level consequence by fiat and
  would destroy the quantile match the map exists to achieve).
* I did **not** use F5/F6 from `bounds_fields.csv` for anything (loose upper sensitivities, and
  their stated multiplier disagrees between the brief and the file — see s3).
* The counterfactual areal means are stated as **predictions of arithmetic** on fixed fields.
  They are not model runs and they do not account for any re-fit of the quantile maps.

### 4.7 The VALUE-vs-ERROR distinction (the thing I most want on the record)

`merged = w*Cmap + (1-w)*P` is a per-cell convex combination. Its area-weighted mean is a
legitimate estimate of the basin mean whenever each cell's estimate is unbiased, i.e. whenever
`w` is uncorrelated with the *error* (`Cmap - truth` relative to `P - truth`). Correlation of `w`
with the field **VALUE** (measured: area-weighted Pearson +0.371 against raw CHIRPS) is not by
itself a defect — if the remote terrain really is wetter, a weighting scheme that puts more CHIRPS
there is doing its job and the higher basin mean is the *correct* answer. cov(w,d) > 0 is
therefore a **mechanism**, not a verdict. What would make it a defect is `cov(w, error) > 0`, and
that is the quantity nobody here can measure. Anyone who reads my +59.5 mm/yr as "59.5 mm/yr of
spurious water" has over-read it.

### 4.8 Could not settle

* Whether the +7.5 % is an error at all. That needs an independent areal-rainfall truth over the
  ungauged 17 % (satellite-independent: basin water-balance closure against discharge, or a
  reanalysis cross-check). Not in scope and not in this ledger.
* Whether the gate's own target 2,036.4 mm/yr is the right reference. It is the gauge-only IDW
  field's own areal mean, so the gate as written asks the merge to reproduce the field it is
  meant to improve. That is a gate-design question, not an H-D question, but it is the reason my
  verdict cannot be "the merge is wrong": measured, no constant w >= 0.089 can pass with the map
  as-is, and the constant w that hits 2,036.393 exactly is **-0.0002**. A gate that no positive
  amount of CHIRPS influence can satisfy is a gate about the target, not about the blend. I flag
  it for the synthesis agent and claim nothing further.

## 5. Executed-output files backing this journal

* `.../scratchpad/hd_out.txt` (blocks 0-6), `.../scratchpad/hd_followup_out.txt`,
  `.../scratchpad/hd_gauge_out.txt` — all three are the verbatim stdout of the scripts named
  in section 4.
* Scripts: `.../scratchpad/hd_blend_arith.py`, `.../scratchpad/hd_followup.py`.
* Nothing was committed, added, staged or pushed. No repo file was modified except this journal.
