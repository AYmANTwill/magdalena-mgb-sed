# Journal — ls-variants-harness

**Agent slug:** `ls-variants-harness`
**Started:** 2026-08-11
**Goal:** build `scripts/c3/ls2d_variants.py`, a harness that computes the eight LS variants
named in `docs/46` §3.1 (V0, V1, V2a, V2b, V3, V4, V4′, V5), gate it on reproducing the
published `ls2d_hs` area-weighted mean **39.812**, and write the per-(minibacia, URH) table to
a **new** file `data/processed/urh_ls2d_variants.csv`.

## Binding constraints I restated to myself before touching anything

- **V0 gate first.** No new variant is reported unless the harness reproduces 39.812. If it
  does not reproduce, I STOP and report the number I actually got.
- `data/processed/urh_ls2d.csv` and `minibacia_ls2d.csv` are **byte-identical** before and
  after. Verified by SHA-256, recorded below.
- `scripts/c3/ls2d.py` is **not modified and not executed**. It is *imported*, and V0 is
  computed by calling **its own** `ls_variants()` — so V0 cannot drift from the committed
  definition, because it *is* the committed definition.
- No git. No engine default moved. Nothing under `sim_calibrated_v2/` opened.
- The **median is diagnostic only** (`docs/46` §3.2); the headline aggregate is the
  area-weighted mean with weights = true cell area.

## Step 0 — orientation (2026-08-11)

Read `CLAUDE.md`, `docs/00_INDEX.md`, `docs/46` §0–§3.5, `docs/47`, `scripts/c3/ls2d.py` in
full, and `docs/agents/journal_decide-ls-resolution.md`.

**Find that de-risks the whole job:** the harness that produced the already-published rows
(39.812 / 0.502 / 1.714 / 0.351 / 0.421) is still on disk in this session's scratchpad —
`scratchpad/ls_formulation.py` + `ls_formulation.json`. So I am not reconstructing those
definitions from prose; I can read the exact code that produced the numbers docs/46 §1 quotes,
and my new variants sit beside it rather than re-deriving it. The json holds

```
ours_hs   39.812260149274366   andean 65.1993985592483   median 12.485774040222168
cap_m05   20.00456156037736    ratio 0.5024723913028578
s_ws78    68.23366459596707    ratio 1.7138857311825018
Lcap_pixel 13.984559495556091  ratio 0.3512626372660478
buarque_exact 16.775413430326218 ratio 0.42136300143291344
n_cells 30,235,916   basin 256,702.36 km2   andean 119,176.76 km2
```

**Decision recorded before running:** the four already-published rows are recomputed by *my*
harness too (V0, V2a, V3, V1, V4′-equivalent), not copied. If any of them fails to reproduce
its published value, that is a finding and it goes in this journal regardless of what it does
to the new rows.

### Definitions I had to fix, and the ground for each

1. **The pixel limiter (V1).** `ls_formulation.py` implements it as
   `a_unit = min(upslope_area, cell_area) / D`. Since a cell's own upslope area always
   includes itself, `upslope_area >= cell_area`, so this is **exactly `a_unit = D`** — slope
   length is one pixel on every cell, which is the literal reading of Buarque p. 94. I keep
   that implementation verbatim so V1 is comparable with the published 0.351.
2. **V5 `L_dg96_fd` — which area basis.** docs/46 §3.1 says V0 + literal D&G finite-difference
   L with S held at V0's, and the task says compute it on the **`ls2d_hs` (1 km²) basis**, not
   the uncapped `ls2d` column. V0's basis is `A_tot = min(upa, 1 km²)`, so the finite-difference
   L's `A_in` must be `max(min(upa, 1e6) - cell_area, 0)`. That is the only choice that makes
   V5 differ from V0 in the **L form alone**.
3. **V2b eq. 14** is taken from `ls_formulation.py:m_step_buarque` — `Sf = tanθ × 100`
   (slope percent), steps 0.2 / 0.3 / 0.4 / 0.5. *(docs/46 (R6) notes the `Sf` units are not
   yet verified against Buarque pp. 46–48; that verification is not my task and I do not
   claim it. I implement the units the existing record uses and say so.)*

### Memory plan (this box has ~2 GB free)

8 variants × 30.24 M cells × float32 = 968 MB if held in RAM, on top of ~610 MB of rasters.
Too tight. Per-cell values therefore go to a **memmap** in the scratchpad, and the medians are
taken one variant at a time after the rasters are freed. Means / Andean means / strata / the
(mini, URH) table are all streaming accumulators and need no storage. (11 columns are stored,
not 8: `ls2d.py`'s own `ls2d`, `ls2d_mb86` and `ls2d_dg96` come out of the same call for free
and are kept as **diagnostics** — `ls2d_dg96` is the column the published ×0.790 was measured
on, so keeping it lets Defect B be shown rather than asserted. 1.33 GB of scratch disk; 74 GB
free.)

## Step 1 — pre-flight algebra check (2026-08-11), before spending a 30 M-cell pass

`scripts/c3/ls2d_variants.py` written. Nine synthetic cells covering the slope range, checked
against docs/46's own tables:

- **V1 is exactly `a_unit = D`.** `max|V1 − (m+1)(D/22.13)^m·S| = 0.0` over all test cells,
  i.e. the `min(upa, cell_area)` form really is a one-pixel slope length everywhere, because
  `upa >= cell_area` always. The limiter is therefore a *deterministic* variant with no
  dependence on the flow accumulation at all — worth knowing, and it means V1 cannot be
  sensitive to any routing detail.
- **continuous `m` reproduces docs/46 §1.1 row for row**: tanθ 0.005 → 0.0847, 0.010 → 0.1494,
  0.020 → 0.2441, 0.030 → 0.3110, 0.050 → 0.4009, 0.090 → 0.5012, 0.1581 → 0.5845,
  0.500 → 0.7003. So the harness's `m` is the same `m` the draft's Defect A argument used.
- **V2b / V2a per cell**: 1.329 / 2.033 / 1.478 / 1.854 / 1.233 at tanθ 0.005…0.05, then
  **exactly 1.000** at tanθ >= 0.09. That is Defect A's predicted *direction* confirmed
  pointwise: eq. 14 is less reducing than the cap below ~9 % and identical above it. Whether
  it survives area weighting is the basin question and is what the pass measures.

Launched the full 90 m pass.

## Step 2 — a correction to my own task brief, found while the pass ran

The task says V2b (`m_step_eq14`) *"has never been measured"* and that V5 isolates a form the
published ×0.790 confounded. Reading `docs/47` §4.1/§4.3 and `docs/agents/journal_ls-evidence.md`
§3 while the pass ran, **both statements are out of date by one day**, and a successor should
not be told otherwise:

- `journal_ls-evidence.md` line 213 already reports a step-`m` row: *"m → W&S-78 step, capped
  0.5"* awm **20.109, ×0.505**, beside the cap's ×0.502. Its step boundaries, though, are
  written at line 146 as **0.2 / 0.3 (1–3 %) / 0.4 (3.5–4.5 %) / 0.5 (> 5 %)** — a *different*
  step set from the one `docs/46` §3.1 registers (0.4 on **3–5 %**). And `docs/47` §4.1's
  harness-validation table then quotes that row as reproducing *the published 0.502*, i.e. it
  compares a **step** number against a **cap** number and calls it a reproduction. So Defect A
  is still live in the record even though a step row exists.
- `journal_ls-evidence.md` line 216 already reports *"L → Desmet–Govers finite difference (S and
  limiter held)"* awm **30.649, ×0.770** — that is V5's definition. So V5 has been measured
  once, by one implementation.

This does not make my run redundant; it changes what it is worth. **It is now a second,
independent implementation of V5 and the first measurement of eq. 14 with `docs/46` §3.1's own
step boundaries.** I record my expectations before reading my own output, so the agreement (or
not) is a real check and not a rationalisation:

> **Pre-stated expectations, written before the pass finished.**
> V0 = 39.812 (the gate). V2a ≈ 0.502. V3 ≈ 1.714. V1 ≈ 0.351. V4′ ≈ 0.421.
> **V5 ≈ 0.770** if my hs-basis reading of "V0 with the D&G L" matches `ls-evidence`'s
> "S and limiter held". **V2b ≈ 0.505** — near the cap, *not* near ×1.4, because the
> area-weighted mean is dominated by steep cells where the step and the cap are both 0.5, and
> Defect A's ×1.18–1.41 divergence lives only on sub-9 % cells whose LS is ~0.03–2.
> If V2b lands near 0.505 then `docs/46`'s **(R4) fires and H-M is refuted on the field
> clause** while its *reading* clause (cap ≠ eq. 14) stands: the two are different objects
> that happen to agree at basin scale. That is the honest reading and I will report it whether
> or not it is the interesting one.

## Step 3 — RESULTS (2026-08-11). Gate first.

Run: `python3.10 scripts/c3/ls2d_variants.py`, 30,235,916 basin cells at 90 m, 61 s for the
per-cell pass, exit 0. Log kept at `scratchpad/ls_variants_run.log`.

### 3.1 THE V0 REPRODUCTION GATE — **PASS**

```
cells scored                    : 30,235,916   (published 30,235,916)
basin area from cell weights    : 256,702.3554 km2
V0 area-weighted mean, MEASURED : 39.812260149274394
same via the strata accumulator : 39.812260149274366
published                       : 39.812        difference +2.601e-04   GATE: PASS
```

The strata accumulator's value is **bit-identical** to the prior harness's
`ls_formulation.json` (39.812260149274366); the (mini, URH) accumulator differs in the last
2 ulp only because it sums 216,800 bins before the total. Cell count and basin area match to
the digit. The gate is not a tolerance pass, it is a reproduction.

### 3.2 The levels

Headline = **area-weighted mean**; the median column is diagnostic and is not an aggregate.

| id | area-wtd mean | Andean >1000 m | median (diag) | × V0 | ln × V0 |
|---|---|---|---|---|---|
| `V0_ours_2026_08` | **39.8123** | 65.1994 | 12.4858 | 1.00000 | 0.0000 |
| `V1_lim_pixel` | 13.9846 | 22.3079 | 7.5113 | **0.35126** | −1.0462 |
| `V2a_m_cap05` | 20.0046 | 31.8202 | 9.9106 | **0.50247** | −0.6882 |
| `V2b_m_step_eq14` | **20.1088** | **31.8953** | **10.0663** | **0.50509** | −0.6830 |
| `V3_s_ws78` | 68.2337 | 114.2019 | 15.0717 | **1.71389** | +0.5388 |
| `V4_buarque_2015` | 16.7754 | 27.1090 | 7.2625 | **0.42136** | −0.8643 |
| `V4p_buarque_2015_cap` | **16.7492** | **27.0989** | **7.2625** | **0.42070** | −0.8658 |
| `V5_L_dg96_fd` | **30.6488** | **50.2329** | 7.4904 | **0.76983** | −0.2616 |
| *diag* `D_ls2d_uncapped` | 104.9013 | 104.5781 | 12.7740 | 2.63490 | |
| *diag* `D_ls2d_mb86` | 16.4355 | 24.1195 | 7.9728 | 0.41282 | |
| *diag* `D_ls2d_dg96_published` | 82.8702 | 78.9735 | 7.6666 | 2.08152 | |

Zero non-finite cells in any of the eleven columns. Lowland (<200 m) and mid (200–1000 m)
strata are in `data/processed/ls2d_variants_summary.json`.

**Every previously published row reproduces:** ×0.351 → 0.35126, ×0.502 → 0.50247,
×1.714 → 1.71389, ×0.421 → 0.42136, and the confounded ×0.790 → **0.7900** exactly
(`D_ls2d_dg96_published / D_ls2d_uncapped` = 82.8702/104.9013).

### 3.3 Aggregation validated against the committed product

`urh_ls2d_variants.csv` has the same 32,782 (mini, urh) rows as `urh_ls2d.csv`, identical
`n_cells` on every row, and its `V0_ours_2026_08` column matches the committed
`ls2d_hs` to **max relative difference 4.988e−06, median 6.05e−07** — which is the `%.6g`
rounding of the committed file, not a numerical disagreement. (`ls-evidence` reports 4.97e−06
for the same comparison; same rounding floor, reached independently.)

The URH table's own area-weighted level sits **×1.0185** above the basin level for *every*
variant (1.0181–1.0187). That is coverage, not error: the URH-valid area is 251,723.5 km² of
256,702.4 km² (×1.0198), and the excluded cells are the URH-invalid low-LS floodplain/water
ones. A per-variant discrepancy would have been a bug; a constant one is the mask.

### 3.4 Committed products untouched

```
urh_ls2d.csv        UNCHANGED  8579c1281c1a992d2e76b3c8278ef3eba59e3bb8543fd38a9c01a0bd3c93f3c4
minibacia_ls2d.csv  UNCHANGED  4c49b07bb92d54cbb3cb93ac1817373a182434c65cf47e535e5ebdd66dcd1724
```
SHA-256 taken before the run and after it, by the script itself, which raises if they differ.

---

## Step 4 — what the numbers do to `docs/46`'s clauses

I state these as **measurements against the draft's own registered thresholds**. I am not the
freezing session and I adopt nothing.

### 4.1 A THIRD MISLABEL, and it is in `docs/46` §3.1 itself — V4′ is NOT the published ×0.421

`docs/46` §3.1 defines **V4′** as *"V1 + V2a + V3 — the ×0.421 row as published, kept so the
prior number stays reproducible"*, and **V4** (with eq. 14) as *"not yet measured"* in effect.
**Both halves are wrong**, and the evidence is the prior harness's own source:
`scratchpad/ls_formulation.py:116` builds `buarque_exact` with `m_bua = m_step_buarque(tan)` —
**the step function** — not with the cap.

| | area-wtd mean | ratio |
|---|---|---|
| prior harness `buarque_exact` (published as ×0.421) | 16.775413430326218 | 0.42136300143291344 |
| **my V4** (limiter + **step** + W&S) | **16.775413430326214** | **0.42136300143291305** |
| my V4′ (limiter + **cap** + W&S) | 16.749164372472990 | 0.42070368046608514 |

V4 reproduces the published joint row to **15 significant figures**. So:

- **The published ×0.421 joint row already IS the source formulation as read** (V4). It never
  used the cap. Defect A does **not** contaminate it.
- **V4′ is the one that had never been measured.** It is ×0.42070.
- `docs/46` §7.3 item 2's owed correction is therefore **half right**: the ×0.502 *single-lever*
  row is indeed mislabelled *"his eq. 14"* when it is `min(m, 0.5)`; but the joint row needs no
  correction at all, and §3.1's V4/V4′ definitions have the two swapped. A freezing session must
  fix §3.1 before freezing, or it freezes a table that mislabels its own reproducibility anchor.

### 4.2 H-M (§2.2) — the sign survives, the **materiality fails**: (R4) FIRES

```
f(V2b) = 0.50509   f(V2a) = 0.50247
|ln f(V2b) − ln f(V2a)| = 0.0052   vs the materiality bar 0.1644   →  (R4) FIRES
f(V2b) > f(V2a)?  TRUE                                             →  (R5) does NOT fire
```

**H-M's field clause is refuted at basin scale.** The predicted *direction* is right — eq. 14 is
less reducing than the cap, exactly as Defect A's pointwise arithmetic said (measured per-cell
ratios 1.33 / 2.03 / 1.48 / 1.85 / 1.23 at tanθ 0.005…0.05, and exactly 1.000 at tanθ ≥ 0.09).
It is worth **0.5 % of the basin level**, 32× inside the bar, because the area-weighted mean of
a linear factor is carried by the steep cells where the step and the cap are the same number,
and the cells where they differ have LS ≈ 0.03–2.

**What survives:** the *reading* clause. `min(m, 0.5)` and eq. 14 are still different objects,
and the ×0.502 row is still mislabelled. They just happen to agree at basin scale. That is a
weaker, truer statement than the draft's, and it is the one the record should carry.

**Independent corroboration:** `journal_ls-evidence.md` line 213 reports ×0.505 for its own step
row, computed by a different harness with step boundaries its §1 text writes as 3.5–4.5 % rather
than 3–5 %. Two implementations, one boundary disagreement, same answer to 4 s.f. — which also
says the 3–5 % vs 3.5–4.5 % ambiguity is immaterial here.

### 4.3 H-L (§2.5) — (the refutation clause) FIRES on the area-weighted proxy

```
f(V5) = 0.76983      |ln f(V5) − ln 0.790| = 0.0259   ≤ 0.1644   →  H-L REFUTED
```
So **Defect B's confound is immaterial at basin scale on the V0 basis**: isolating the L form
(hs basis, S held at Moore & Burch) gives 0.770 where the confounded published figure — which
also swapped S to McCool-87 and used the *uncapped* column — gives 0.790. My diagnostics
reproduce that confounded 0.790 exactly, so this is a like-for-like comparison of the two, not
an inference. Two errors nearly cancel. `ls-evidence` measured the same isolation
independently at ×0.770.

**But this does NOT rescue the ×0.333 bracket endpoint, and the reason matters.** The L-form
ratio is **formulation-dependent**, so it may not be multiplied across formulations:

- on the **V0** basis (1 km² cap, long slopes): L_dg/L_point = **0.770** (V5, this run);
- inside the **source** formulation (one-pixel length ⇒ `A_in = 0`, so the ratio collapses to
  the head-cell value `1/(m+1)`): **0.5807** (`docs/47` §4.1, derived and measured).

`0.42136 × 0.770 = 0.324` is therefore **not** the source-with-D&G level; the measured one is
**×0.245** (`ls-evidence` 9.741; `docs/47` §4.3 ×0.24466 area-weighted). So `docs/46` §2.5's
framing — that ×0.333 fails because the 0.790 was *confounded* — is the wrong diagnosis. The
0.790 was confounded, but immaterially; **×0.333 fails because a lever ratio was composed across
two formulations in which it takes different values.** `docs/47` §3.1 R6 already reached the
corrected endpoint by a different route, and this run's V5 is consistent with it. The draft's
§2.5, if frozen as written, would freeze the wrong explanation of a correct conclusion.

### 4.4 H-JOINT (R10) — does NOT fire; the levers still do not separate

```
V1 × V2b × V3 = 0.3041   joint V4  = 0.42136   |ln diff| = 0.3262  > 0.1644
V1 × V2a × V3 = 0.3025   joint V4′ = 0.42070   |ln diff| = 0.3298  > 0.1644
```
Twice the bar, on both the step and the cap composition. **"Decide them as a set" survives**,
and it survives against the corrected eq. 14 rather than only against the cap.

### 4.5 H-LIM (R3) — does NOT fire; the limiter is still the largest single lever

|ln f| by lever: **limiter 1.0462** > m cap 0.6882 ≈ m step 0.6830 > S 0.5388 > L form 0.2616.
`docs/46` (R3) anticipated that eq. 14 might overtake it. It does not — it moves `m`'s factor
toward 1 by 0.5 %, and the limiter is unmoved by construction (V1 is exactly `a_unit = D`).

### 4.6 What this run does NOT settle — stated so nobody over-reads it

1. **Everything above is `f_area`, the PROXY.** `docs/46` §3.3 says **`f_ero` decides** and this
   harness runs no engine, so it measures none of (R2), (R11), (R12). `docs/47` §4.3 has
   erosion-weighted values for four of the rows and measures the proxy **2.51 % low**; that
   correction is not applied here and my ratios should not be quoted as `f_ero`.
2. **(R6) — the `Sf` units of eq. 14 — is untested.** I implement `Sf = 100·tanθ` because that
   is what the existing record uses. If eq. 14's `Sf` turns out to be degrees or m/m, V2b is
   void and must be recomputed, not adjusted.
3. **No stratified per-station `LS̄` and no slope terciles** (`docs/46` §3.3 also requires
   those for the decision). Elevation strata only.
4. **Nothing is adopted.** No engine default moved; `ls2d_column` is untouched; the variants are
   reachable only by name from the new file.

## Step 5 — files, and closing state

Written by this run:
- `scripts/c3/ls2d_variants.py` — the harness (imports `ls2d.py`; V0 is `ls2d.ls_variants()[3]`)
- `data/processed/urh_ls2d_variants.csv` — 32,782 rows, key (mini, urh), 8 variant columns
- `data/processed/minibacia_ls2d_variants.csv` — 8,672 rows
- `data/processed/ls2d_variants_summary.json` — levels, strata, ratios, ln-ratios, gate record
- this journal

Not touched: `urh_ls2d.csv`, `minibacia_ls2d.csv` (SHA-256 verified before and after),
`scripts/c3/ls2d.py`, any engine default, anything under `sim_calibrated_v2/`. No git command
was run. The scratchpad memmap `ls2d_variants_percell.f32` (1.33 GB) can be deleted; it is
regenerable in ~4 minutes.
