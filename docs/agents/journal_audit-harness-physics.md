# journal — `audit-harness-physics`

Task: audit the LS variant harness's reported numbers (`scripts/c3/ls2d_variants.py`,
`data/processed/ls2d_variants_summary.json`) for **physical and arithmetic coherence**.
Method required by the brief: form my own expectation FIRST, then read its code, then measure.
Nothing here changes any default, any committed product, or any doc. No git command is run.

---

## 1 — Expectations formed BEFORE reading `ls2d_variants.py` (locked here, 2026-08-11)

Read first: CLAUDE.md, `docs/00_INDEX.md` (skimmed), `docs/46_ls_preregistration_DRAFT.md`
§0–§4, `docs/47_c4_entry_verdict.md` §0–§2.1. Then the reported JSON only.

- **(a)** V1/V2a/V3 must land on 13.985 / 20.005 / 68.234 and 0.351 / 0.502 / 1.714. The
  reported values do. The real test is against the PRIOR ARTIFACT at full precision, not
  against docs/46's 3-dp table — find `scratchpad/ls_formulation.json`.
- **(b)** The published joint row is 16.775 with median 7.262 and Andean 27.109. V4 = 16.7754
  matches; V4′ = 16.7492 does **not** match 16.775 at 5 s.f. So *a priori* the published row
  is V4 (step), not V4′, contradicting docs/46 §3.1 — but this must be settled from the prior
  harness's own source, not from rounding.
- **(c)** Direction: eq. 14 assigns a higher `m` than continuous McCool on every cell below
  tan θ ≈ 0.09, and a_unit_hs ≫ 22.13 m, so `(m+1)(a/22.13)^m` is increasing in m ⇒
  **V2b ≥ V2a pointwise, with equality above 9 %**. Expect a small positive gap.
- **(d)** Order of magnitude, derived before measuring: gap = (LS-mass share of cells below
  the crossover) × (mean uplift − 1). Uplift is 1.2–1.6 (docs/46 §1.1 at the median a_unit).
  A 0.5 % gap therefore implies the sub-crossover cells carry ≈ 1–2 % of the basin LS mass.
  **NOTE — the brief's own premise is wrong**: it says the two "coincide above the 5 %
  breakpoint". They do not. eq. 14 hits 0.5 at Sf ≥ 5 %, but the CONTINUOUS m only reaches
  0.5 at tan θ ≈ 0.09 (docs/46 §1.1 table: at 5 % slope, cont. m = 0.4009 vs step 0.50). The
  difference region is **tan θ < 0.09**, not < 0.05. The magnitude must be checked against the
  area and LS mass below 9 %, and the 5–9 % band is part of the answer, not outside it.
- **(e)** Naive expectation: published 0.790 = [L_dg/L_cont] × [S_McCool87/S_MB86] on the
  UNCAPPED basis. docs/46 §3.4 gives McC/MB < 1 on steep cells (0.95 at tan θ 0.3, 0.87 at
  0.5, 0.78 at 1.0) and ≫ 1 only on near-flat cells. An area-weighted LS mean is dominated by
  steep cells ⇒ the S swap should push the published ratio **DOWN** ⇒ isolating L should give
  **f(V5) > 0.790**. The harness reports f(V5) = 0.770 < 0.790, i.e. the OPPOSITE of the naive
  expectation. That is only reconcilable if the basis change (uncapped vs 1 km²-capped) moves
  the L-form ratio up by more than the S swap moves it down. **This must be decomposed, not
  assumed.** The JSON's three diagnostics do NOT decompose it (`D_ls2d_mb86` is fixed m = 0.4,
  not an S swap), so a new measurement is needed.

## 2 — Progress log

- Read `docs/46` §0–§4, `docs/47` head, `journal_decide-ls-resolution.md` §3b (the published
  table's origin), `scripts/c3/ls2d.py` docstring + `ls_variants()`, then
  `scripts/c3/ls2d_variants.py` §registry/`variant_block`.
- **Found the prior harness**: `…/Temp/claude/c--dev-magdalena-mgb-sed/3d81998f-…/scratchpad/
  ls_formulation.py` and `.json` (this session's own scratchpad — it survives).
- Next: an INDEPENDENT full-basin pass of my own (my own LS expressions, my own accumulator)
  adding the slope-class decomposition (d) and the 0.790 decomposition (e).

### 2.1 Settled from artifacts, before my own pass

1. **(a) and (b) settled against the PRIOR ARTIFACT, not the rounded table.**
   `scratchpad/ls_formulation.json` (the prior harness's own output) gives
   ours_hs 39.812260149274366 · cap_m05 20.00456156037736 · s_ws78 68.23366459596707 ·
   Lcap_pixel 13.984559495556091 · **buarque_exact 16.775413430326218**. The new harness's
   V0/V2a/V3/V1/V4 agree with those to 15–16 s.f. `scratchpad/ls_formulation.py:116` builds
   `buarque_exact` from `m_step_buarque` (its line 33–36, the STEP function) — so **the
   published ×0.421 joint row IS V4, the step composition; V4′ (16.7492) has never been
   published.** docs/46 §3.1's label on V4′ ("the ×0.421 row as published") is wrong, and
   docs/46 §1's own ×0.502 row IS the cap (`min(m_ours,0.5)`, line 112–113), so Defect A is
   real for the single-lever row only. The harness's finding (1) is CONFIRMED from source.
2. **JSON internal arithmetic: clean.** For all 11 columns the three elevation strata
   recombine to the basin level to ≤ 3.6e-16 relative; `ratio_to_V0` and `ln_ratio_to_V0`
   are exact; strata areas sum to the basin area to 3e-11 km². Naive-product |ln| 0.3262
   (step) / 0.3298 (cap); |ln f(V2b) − ln f(V2a)| 0.0051992 (bar/gap = 31.6, the report's
   "32×"); |ln f(V5) − ln 0.790| 0.0258588. All as reported.
3. **The URH-table offset ×1.0185 is arithmetic, not error.** Non-URH cells (4,978.85 km²,
   1.94 % of the basin) carry a mean V0 LS of **2.53** against the basin's 39.81; that
   deficit alone reproduces the offset, and the offset is variant-stable (1.0181–1.0187), so
   ratios are unaffected at the 0.06 % level.
4. **V2b and V5 are independently corroborated by a DIFFERENT harness.**
   `journal_ls-evidence.md` (its own table, line ~205–215): step-m row **20.109 (×0.505)**,
   D&G-L-isolated row **30.649 (×0.770)**, uncapped `ls2d` **104.901**. These match V2b, V5
   and D_ls2d_uncapped to 6 s.f. That journal also has the number this audit needs for (e):
   **S → McCool-87 alone, on V0's capped basis, = 36.149 (×0.908)** — i.e. the S swap on its
   own pushes the level DOWN 9.2 %, which is what makes f(V5)=0.770 < published 0.790 look
   wrong until the basis change is accounted for.
5. **Reported-vs-artifact mismatch (immaterial, but real).** Six fields in the harness's
   returned blob do not match `ls2d_variants_summary.json`: V2b mean 20.108816546932 (JSON
   20.108840138033035, −1.2e-6 rel) and median 10.066267013549805 (JSON 10.066278457641602 —
   a *different float32*, so not a rounding artifact); V5 mean 30.648845 (JSON
   30.648806856, +1.2e-6) and median 7.490357875823975 (JSON 7.490399360656738); Andean
   V2b 31.89528 (JSON 31.895333), V4 27.108995 (JSON 27.109007), V4p 27.098859 (JSON
   27.098938). Neither CSV reproduces them either (mini-CSV re-aggregation matches the JSON
   to 1e-9; URH-CSV gives the ×1.0185 level). Magnitude ≤ 3e-6 relative = 5 orders below the
   0.1644 ln bar, so no verdict moves; but the blob is not a faithful transcript of the
   executed output for those six fields, and the report's "2-ulp" explanation covers 1e-15,
   not 1e-6.

## 3 — My own independent pass (the measurement this audit rests on)

`…/scratchpad/audit_pass.py` + `audit_pass.json`. Same inputs as the committed pipeline (same
DEM, Horn slope, pyflwdir pit-fill/D8/upstream area, minibacia mask, per-row cell geometry —
otherwise it is not like-for-like); **every LS expression written from the published
definitions, importing neither `ls2d.py`'s `ls_variants()` nor the harness.** 30,235,916 cells,
256,702.3554 km², ~8 min. Nothing written into the repo.

**It reproduces all eight variants and all three diagnostics:** V0 39.812260149 · V1
13.984559496 · V2a 20.004561560 · V2b 20.108840138 · V3 68.233664596 · V4 16.775413430 · V4p
16.749164372 · V5 30.648806856 · uncapped 104.901268761 · mb86 16.435489282 · dg96
82.870186075. **Max per-cell relative deviation from the harness's own stored per-cell field:
5.96e-08 on all 11 columns = 2^-24, i.e. float32 storage epsilon — the two implementations are
bit-identical before storage.** The harness's artifact values (not its returned blob) are the
correct ones for V2b and V5.

### 3.1 (d) — the V2b−V2a gap, fully accounted

| slope class (Sf = 100 tan θ) | area km² | area % | V2a level | V2b level | V2b/V2a | share of V2a LS mass | contribution to the basin gap |
|---|---:|---:|---:|---:|---:|---:|---:|
| < 1 % | 33,613.3 | 13.09 | 0.0339 | 0.0497 | 1.469 | 0.022 % | +0.0104 pts |
| 1–3 % | 31,632.9 | 12.32 | 0.3499 | 0.4332 | 1.238 | 0.216 % | +0.0513 pts |
| 3–5 % | 16,018.6 | 6.24 | 1.4041 | 1.6614 | 1.183 | 0.438 % | +0.0803 pts |
| 5–9 % | 18,946.8 | 7.38 | 5.0525 | 6.0805 | 1.204 | 1.864 % | **+0.3793 pts** |
| ≥ 9 % | 156,490.7 | 60.96 | 31.9814 | 31.9814 | **1.0000** | **97.460 %** | 0.0000 |
| basin | 256,702.4 | 100 | 20.00456 | 20.10884 | 1.005213 | 100 % | **+0.5213 %** |

Area-weighted median tan θ **0.1588** (the quoted 0.158 ✓). Area below the true crossover
(tan θ 0.0893) = **39.04 %** of the basin but only **2.5398 %** of the LS mass; mean uplift over
that mass **1.2052**; `0.025398 × 0.2052 = 0.005213` — the identity closes exactly. **The
brief's "below 5 %" premise is wrong: the 5–9 % band alone supplies 72.8 % of the gap.**

### 3.2 (c) — a pointwise exception docs/46 §1.1 does not state

262,088 cells (0.87 %) have **V2b < V2a**, exactly on tan θ ∈ (0.028132, 0.03) ∪ (0.049741,
0.05): the continuous m reaches 0.3 at 2.8132 % and 0.4 at 4.9741 %, *before* eq. 14's next
step. So "eq. 14 is less reducing on every cell below ~9 %" is false in two narrow bands. The
basin direction is unaffected (every class ratio ≥ 1; ≥ 9 % is exactly 1.0000 because
m_cont ≥ 0.5 from tan θ 0.089333).

### 3.3 (e) — the 0.790 decomposed (new measurement)

| basis | L_cont × S_MB86 | L_fd × S_MB86 | L_cont × S_McC87 | L_fd × S_McC87 |
|---|---:|---:|---:|---:|
| uncapped (`ls2d`) | 104.9013 | 89.4033 | 96.9906 | 82.8702 |
| hs, 1 km² cap (`ls2d_hs`) | 39.8123 (V0) | **30.6488 (V5)** | — | 27.9277 |

- L-form factor: **0.85226 uncapped** vs **0.76983 capped** ⇒ the basis confound is **+10.71 %**.
- S swap (McCool-87 / Moore&Burch-86) given L_fd: **0.92693 uncapped**, 0.91122 capped ⇒ **−7.31 %**.
- Product on the uncapped basis: 0.85226 × 0.92693 = **0.78998 = the published 0.790** ✓.
- Net: 0.790 / 0.76983 = **1.0262** = 1.1071 × 0.92693. "Two errors nearly cancel" is confirmed
  **and quantified**; each component is *also* inside the 0.1644 bar (|ln| 0.1017 and 0.0759).
- Direction: the S component alone points the way docs/46 §3.4 implies (McCool < M&B on a
  steep-weighted mean ⇒ isolating L should raise the ratio to 0.852); the **basis** component is
  larger and flips the net sign, which is why f(V5) = 0.770 lands *below* 0.790.
- Cross-check: capped L_fd × S_McC = 27.9277 = `journal_ls-evidence`'s RUSLE-faithful **27.928**.

### 3.4 Verdict

The harness's numbers are physically and arithmetically coherent and independently reproduced.
The defects found are: the six mis-transcribed fields in the returned blob (≤ 3e-6, immaterial),
"reproduces EXACTLY as 0.7900" (it is 0.789983 — exact to 4 dp), and the per-cell ratio list
being cell-specific rather than a slope profile. Nothing changes a gate outcome.
