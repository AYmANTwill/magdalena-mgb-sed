# Journal — ls-evidence

**Agent slug:** `ls-evidence`
**Started:** 2026-08-11
**Goal:** Establish, from PRIMARY sources, which LS formulation this model should use.
Evidence only — no code changes, no doc rewrites, no git.

## Discipline binding me
- Report only what I can cite to a retrievable primary source. If the literature does not
  settle a lever, write NOT SETTLED. **Do not invent a plausibility band** (this project has
  retired two already: the "mountainous LS 2–10" and the SDR 0.05–0.30).
- Measure before asserting: any claim about what *our* code does must be read out of the code.

## Log

### Step 0 — orientation (2026-08-11)
Read CLAUDE.md, docs/00_INDEX.md, docs/37 §1 + §4 candidate 0, docs/35 §9.3,
docs/agents/journal_decide-ls-resolution.md (the measurement that produced the three levers).

Three levers to adjudicate, as measured by `decide-ls-resolution` on all 30,235,916 basin
cells at 90 m (harness reproduces our own area-wtd `ls2d_hs` = 39.812 bitwise):
  hillslope limiter ×0.351 · m cap ×0.502 · S formulation ×1.714 · joint ×0.421 (→ ×0.333 with
  the literal Desmet–Govers finite-difference L).

### Step 1 — read the implementation before citing anything (2026-08-11)

`scripts/c3/ls2d.py` L24, L177–184, L273–318. The column the engine consumes is **`ls2d_hs`**:

```
LS = (m+1) · (A_unit/22.13)^m · (sinθ/0.0896)^1.3
A_unit = min(A_upslope, A_CHANNEL_M2=1e6 m²) / D
m      = β/(1+β),  β = (sinθ/0.0896)/(3 sinθ^0.8 + 0.56)     [McCool et al. 1989]
```

Findings from the code text itself, before any literature:
- The **production column is NOT the Desmet–Govers finite-difference L.** `ls2d_dg96` (the
  literal D&G eq. 11 × McCool 1987 S) is computed as a *cross-check variant only*; the engine
  reads `ls2d_hs`, which is the **continuous / Moore–Burch–Mitasova** form. So "our
  implementation is Desmet & Govers (1996) LS2D" is imprecise: it is D&G's *unit-contributing-
  area idea* evaluated in the continuous Moore–Burch form.
- The docstring claims McCool m "runs from ~0.0 on flats to ~0.5 on steep Andean slopes".
  That is **false** and is a live docstring defect: β→3.135 as θ→90°, so m→0.758, and the
  measured basin median is 0.584 (journal_decide-ls-resolution Step 2). Verified numerically
  below.
- The S factor actually in production is **Moore & Burch (1986) n=1.3**, while the D&G
  cross-check variant uses **McCool et al. (1987)** S. Two different S factors coexist in one
  script; only the M&B one reaches the engine.

### Step 2 — primary sources retrieved

**S1. Renard, K.G., Yoder, D.C., Lightle, D.T. & Dabney, S.M. (2011)**, "Universal Soil Loss
Equation and Revised Universal Soil Loss Equation", ch. 8 in Morgan & Nearing (eds.),
*Handbook of Erosion Modelling*, Wiley-Blackwell, 137–167. Retrieved
`https://www.tucson.ars.ag.gov/unit/publications/pdffiles/2122.pdf`, 31 pp, text-extracted.
Renard is the lead author of AH-703 and Yoder a co-author, so this is the RUSLE authors'
own statement of the handbook's content. Verbatim, p. 142–144:
- **"on steep slopes, computed soil loss in RUSLE is just over half that predicted by the
  USLE, whose relationship did not include data for steep slopes."** (p. 142)
- **"most attempts to use GIS with USLE/RUSLE recognize this and simply cut off the slope
  lengths at some arbitrary value."** … "slope lengths computed using these data are almost
  always far too long." (p. 143)
- slope length "beginning at the top of the hillslope where runoff starts, and extending down
  to where the sheet and rill flow reaches either a concentrated flow channel or a
  depositional area." (p. 143)
- L = (λ/72.6)^m, m = b/(1+b), **b = (sinθ/0.0896)/[3.0(sinθ)^0.8 + 0.56]** (eqs. 8.2–8.3).
  "a constant value of 0.5 should be used" only for **thawing and cultivated soils dominated
  by surface flow** (McCool et al. 1989, 1993) — it is not a general cap.
- S = 10.8 sinθ + 0.03 (S<9 %); S = 16.8 sinθ − 0.50 (S>9 %) (eqs. 8.4–8.5, McCool et al. 1987).

**S2. Renard, K.G., Foster, G.R., Weesies, G.A. & Porter, J.P. (1991)**, "RUSLE — Revised
universal soil loss equation", *J. Soil Water Conserv.* 46(1), 30–33. Retrieved
`https://www.tucson.ars.ag.gov/unit/publications/pdffiles/775.pdf`. Verbatim, p. 3 of the
reprint:
> "The RUSLE has a more nearly linear slope steepness relationship than the USLE. Computed
> soil loss for slopes less than 20 percent are similar in the USLE and RUSLE. However, on
> steep slopes, computed soil loss is reduced almost by half with the RUSLE. **Experimental
> data and field observations, especially on rangeland, do not support the USLE quadratic
> relationship when extended to steep slopes.**"

**S3. Renard, Foster, Weesies, McCool & Yoder (1997), Agriculture Handbook 703 (AH-703)** —
407 pp, full text retrieved from
`https://downloads.regulations.gov/EPA-R08-OW-2019-0512-0226/attachment_464.pdf`. Ch. 4:
- p. 104: "Slope length is defined as the horizontal distance from the origin of overland flow
  to the point where either (1) the slope gradient decreases enough that deposition begins or
  (2) runoff becomes concentrated in a defined channel (Wischmeier and Smith 1978). **Surface
  runoff will usually concentrate in less than 400 ft, which is a practical slope-length limit
  in many situations, although longer slope lengths of up to 1,000 ft are occasionally found.
  … few slope lengths as long as 1,000 ft should be used in RUSLE.**"
- p. 104: "Slope lengths estimated from contour maps are usually **too long** because most maps
  do not have the detail to indicate all concentrated flow areas that end RUSLE slope lengths."
- eqs. [4-1]–[4-3]: L = (λ/72.6)^m; m = β/(1+β); β = (sinθ/0.0896)/[3.0(sinθ)^0.8+0.56].
- eqs. [4-4]/[4-5]: S = 10.8 sinθ+0.03 (s<9 %); S = 16.8 sinθ−0.50 (s≥9 %) (McCool et al. 1987).
- **Table 4-5 (source: McCool et al. 1989) tabulates m to 60 % slope; moderate rill/interrill
  column: 0.52 at 10 %, 0.61 at 20 %, 0.66 at 30 %, 0.70 at 50 %, 0.71 at 60 %** — i.e. the
  RUSLE handbook itself publishes m WELL ABOVE 0.5. The constant 0.5 is reserved for thawing
  soils under surface flow (p. 106).
- Tables 4-1…4-4 tabulate LS over slope **0.2–60 %** and slope length **3–1,000 ft (0.9–305 m)**.
  That is RUSLE's own tabulated domain.

**S4. Buarque (2015) — verified independently from the thesis PDF** (lume.ufrgs.br
`10183/129875`, 182 pp, PyMuPDF). All four items the record depends on reproduce:
- eq. 13 (p. 47) = Desmet & Govers (1996) finite-difference L, `Xdir` = 1 / √2.
- eq. 14 (p. 47) = **step m capped at 0.5** (0.2 / 0.3 / 0.4 / 0.5 by Sf < 1 / 1–3 / 3–5 / ≥5 %)
  — this is the Wischmeier & Smith (1978) USLE table.
- eqs. 15–17 (p. 47) slope by **centred finite differences over the four orthogonal neighbours**
  (Wilson & Gallant 2000) — ours is Horn 3×3, a further small difference.
- eq. 18 (p. 48): S = 65,41 sin²θ + 4,56 sinθ + 0,065, "**dado por Wischmeier & Smith (1978)**".
- p. 94: "Na determinação do fator comprimento de 'L', seu valor máximo foi limitado ao tamanho
  do pixel do MDE."
- **p. 98 — the second, independent sentence that RESOLVES the interpretation risk docs/35
  §9.3.4 item 4 flagged:** "por pixel do MDE com resolução espacial de 500 m, **o maior valor
  permitido pelo modelo para o fator L é igual ao limite da dimensão de cada pixel**." Two
  separate passages say the same thing, so the "slope length ≤ one pixel" reading is confirmed,
  not inferred. The ×0.351 row's *definition* is safe.
- p. 98 and p. 121 also record the author's own verdict that MUSLE is the wrong equation for the
  Andes: "os principais processos erosivos existentes são decorrentes de **erosão em massa**,
  com desmoronamento de encostas … o que é **incompatível com o uso da MUSLE**" (p. 121).

**S5. Montgomery & Dietrich — the source the `A_CHANNEL = 1 km²` constant cites.**
- (1988) *Nature* 336, 232–234, retrieved from geomorphology.sese.asu.edu. Source area above the
  channel head **decreases** with local valley gradient over 5°–45°, and — measured across three
  sites — **wetter regions have SMALLER source areas** (Coos Bay 1,500 mm/yr lowest; S. Sierra
  260 mm/yr highest).
- (1989) *WRR* 25(8), 1907–1918, same source. **Table 1** (Tennessee Valley, CA): measured source
  areas **2,700 – 12,000 m²**. **Eq. (10): A = 1978 · tanθ^(−1.65), R² = 0.75.**
  At our Andean median tanθ ≈ 0.483 that is **≈ 6.6 × 10³ m²**; at the basin median tanθ 0.1581,
  **≈ 4.2 × 10⁴ m²**. Our cap is **1 × 10⁶ m²** — 150× and 24× those values respectively.
  → **The code's stated justification for 1 km² ("upper end of the humid/steep field range in
  Montgomery & Dietrich 1988, 1992") is contradicted by the cited source by ~2 orders of
  magnitude.** This is a citation defect, not a modelling opinion.

**S6. Schmidt, S., Tresch, S. & Meusburger, K. (2019)**, "Modification of the RUSLE slope
length and steepness factor (LS-factor) based on rainfall experiments at steep alpine
grasslands", *MethodsX* 6, 219–229, doi 10.1016/j.mex.2019.01.004 (open access, PMC6360611).
Collects the published S functions verbatim (W&S-78 65.4 sin²θ+4.56 sinθ+0.0654; McCool-87
10.8 s+0.03 / 16.8 s−0.50; **Nearing-97 S = −1.5 + 17/(1+e^(2.3−6.1 sinθ))**; Liu 21.91 sinθ−0.96)
and states: **"all S-factors have in common that empirical evidence and thus validity is limited
to slope gradients less than 50 %"**, and that the regression lines "differ largely with
increasing slope steepness" (R² 0.18–0.70).

**S7. Benavidez, Jackson, Maxwell & Norton (2018)**, HESSD `hess-2018-68` (published as HESS 22,
6059–6086). Its Table 5 row 5 records the form our engine uses:
`LS = (m+1)(U/L0)^m (sinβ/S0)^n`, "Moore & Burch (1986) **as cited in** Mitasova et al. (1996);
Desmet & Govers (1996)", with **m = 0.4–0.6 and n = 1.0–1.3**. Our n = 1.3 is the top of the
published range; our m is not a constant from that range but the McCool-89 continuous function.
Row 1 records the W&S-78 step m (0.5 > 5 %, 0.4 3.5–4.5 %, 0.3 1–3 %, 0.2 < 1 %) = Buarque eq. 14.

**S8. Panagos et al. (2015) / JRC ESDAC LS-factor page** — the continental reference
application: Desmet & Govers algorithm in SAGA GIS with multiple-flow accumulation, **25 m**
EU-DEM, EU mean LS **1.63**, range 0–99, LS > 25 on **0.1 %** of the EU, and — the item that
matters here — the methodology **"limits the estimation of LS to a maximum slope angle of 50 %
(26.6 degrees)"**. (Retrieved from `esdac.jrc.ec.europa.eu/themes/slope-length-and-steepness-factor-ls-factor`.)

**S9. Global 30 m LS dataset built on SRTM** (*Scientific Data*, 2024, PMC10799908) — an
independent large-scale D&G implementation. It applies an explicit **cut-off**: "when the
catchment area was greater than the threshold, the point was marked as a cut-off point", with a
slope-dependent cut-off factor (0.7 below 5 % slope, 0.5 at/above). Confirms that capping
contributing area is standard practice in large-scale LS products — the *practice* is standard,
the *value* is not standardised.

**S10. The MGB-SED plugin binary — first-party, current, retrievable.**
`https://github.com/LabHig-Ufes/MGB-SED` ships one artefact, `MGB-SED.zip` (3.69 MB). Extracted;
`MGB-SED/bin/formPRESED.exe` (2025-09-10) contains these literal strings:
- `LS-2D CALCULATION (Desmet and Govers, 1996) CLOSED!!!`
- `1.3 LS-2D TOPOGRAPHIC FACTOR FILE...:` / `PLEASE CHOOSE...:` /
  `(0) Use the standard method to calculate the S factor` /
  `(1) Use the slope scaling method to calculate the S factor`
- `PLEASE ENTER THE SPATIAL RESOLUTION OF THE DEM/DTM IN METERS` /
  `NOW PLEASE ENTER THE SPATIAL RESOLUTION OF THE TARGET DEM/DTM`
So in the tool this project transposes, **the S factor is a run-time user choice, not a fixed
part of the method**, and the tool carries a *source→target resolution rescaling* our
implementation does not have. I could NOT recover the numeric constants: an exhaustive
float32/float64 scan of `formPRESED.exe` found no 22.13, 0.0896, 65.41, 0.065, 10.8 or 16.8
(it does contain 4.56 once and 0.2/0.3/0.4/0.5). **So the binary settles the L reference and the
existence of the S choice, and settles nothing about which S is "standard".**

**NOT RETRIEVED — stated so it is not mistaken for evidence.** Fagundes et al. (2026),
*Int. Soil Water Conserv. Res.*, doi 10.1016/j.iswcr.2025.11.007 (article
`S2095633925001388`) is **diamond open access but hosted only on ScienceDirect, which returned
403 to every route tried** (WebFetch, requests with browser headers, doi.org redirect,
linkinghub, /pdfft, DOAJ API, OpenAlex `best_oa_location`). Same for Fagundes et al. (2021)
*WRR* 57 e2020WR027884 and its ESSOAr preprint. **I did not read either paper. Nothing in my
verdicts rests on them.** A search-index snippet for a sibling ISWCR paper
(doi 10.1016/j.iswcr.2025.10.004, "Comparison of approaches using MUSLE, USLE-M and RUSLE2…")
states that MGB-SED's LS uses "Desmet and Govers (1996) for the L factor and Wischmeier and
Smith (1978) for the S factor" — **that is a snippet, not a read**, it merely corroborates
Buarque (2015), and I flag it as second-hand.

### Step 3 — MEASUREMENT (read-only harness, 2026-08-11)

`scratchpad/ls_levers.py` imports `scripts/c3/ls2d.py`'s own constants and helpers and
recomputes 17 LS variants over the same 30,235,916 basin cells at 90 m. **Nothing under
`data/` was written; `scripts/c3/ls2d.py` was not run and not edited.**

**Validation — the harness reproduces every published lever number:**

| published | source | mine |
|---|---|---|
| `ls2d_hs` area-wtd mean 39.812 | journal_c31-ls2d §S4 | **39.8123** |
| S → W&S-78 ×1.714 | docs/37 §4 cand. 0 | **1.7139** |
| m → step-capped ×0.502 | docs/37 §4 cand. 0 | **0.5051** |
| limiter → 1 pixel ×0.351 | docs/37 §4 cand. 0 | **0.3513** |
| "all three" awm 16.775 (×0.421) | docs/37 §4 cand. 0 | **16.7754 (×0.4214)** |

**Results (area-weighted mean LS over the basin; "steep" = tanθ > 0.2):**

| variant | awm | × ours | × ours (steep) |
|---|---|---|---|
| `ours_hs` — production (cont. L, McCool-89 m, M&B-86 S n=1.3, A≤1 km²) | 39.812 | 1.000 | 1.000 |
| **S → McCool et al. 1987 (the RUSLE prescription)** | 36.149 | **0.908** | 0.891 |
| **S → Nearing 1997** | 41.663 | **1.047** | 1.052 |
| S → Wischmeier & Smith 1978 | 68.234 | 1.714 | 1.786 |
| m → W&S-78 step, capped 0.5 | 20.109 | 0.505 | 0.476 |
| **L → Desmet–Govers finite difference (S and limiter held)** | 30.649 | **0.770** | 0.763 |
| limiter → slope length ≤ 1 pixel | 13.985 | 0.351 | 0.356 |
| limiter → none (the `ls2d` column) | 104.901 | 2.635 | 2.542 |
| **limiter → length ≤ 400 ft (AH-703 practical limit)** | 15.973 | **0.401** | 0.409 |
| **limiter → length ≤ 1,000 ft (AH-703 outer bound)** | 23.303 | **0.585** | 0.601 |
| cap → A ≤ 1e5 m² | 30.145 | 0.757 | 0.774 |
| cap → A ≤ 5e4 m² | 26.752 | 0.672 | 0.690 |
| cap → A ≤ 1e4 m² | 15.099 | 0.379 | 0.385 |
| **Buarque source method, continuous L** (= docs/37's "all three") | 16.775 | 0.421 | 0.435 |
| **Buarque source method, literal D&G L** | **9.741** | **0.245** | 0.252 |
| RUSLE-faithful (D&G L + McCool m + McCool S + 1 km² cap) | 27.928 | 0.702 | 0.681 |
| RUSLE-faithful with the 1-pixel limiter | 6.300 | 0.158 | 0.154 |

Also measured: McCool-89 `m` median **0.5844**, p90 **0.7028**, max **0.7501**; basin median
tanθ **0.1581**; **1,769,622 cells (5.85 %) have upslope area > 1 km²**; **18,004,898 cells
(59.5 %) already have a unit contributing length > 400 ft**.

`scratchpad/slope_dist.py`, same 30,235,916 cells: tanθ p25/50/75/90/95/99 =
0.0290 / 0.1580 / 0.3450 / 0.5187 / 0.6164 / 0.7964. **11.26 % of cells exceed tanθ 0.50 and
they carry 35.5 % of the basin's area-weighted S-factor total. 5.71 % exceed 0.60**, AH-703
Table 4-5's highest tabulated slope.

### Step 4 — derivation: the L form is a *point* rate vs a *cell average* (not a citation, a proof)

USLE's `A(λ) ∝ (λ/22.13)^m` is the loss **averaged over** 0→λ. So cumulative loss per unit
width is `T(λ) = λ·A(λ) ∝ λ^(m+1)/22.13^m`, and:

- loss from the segment [λ_in, λ_out] **averaged over the cell**:
  `L_seg = (λ_out^(m+1) − λ_in^(m+1)) / (D · 22.13^m)` → **exactly Desmet & Govers eq. 11 =
  Buarque eq. 13** once λ = A/D.
- the **point** rate at λ: `dT/dλ = (m+1)(λ/22.13)^m` → **exactly our production continuous
  form** (Mitasova et al. 1996 / Moore & Burch as cited there).

They converge when λ_in ≫ D (derivative approximation) — measured ×0.770 at our 1 km² cap.
They diverge maximally when λ_in = 0, i.e. on a head cell, which under a one-pixel limiter is
**every** cell: then `L_seg/L_point = 1/[(m+1)·x^m]` = 0.71/0.59 (x=1, m=0.4/0.7) or
0.62/0.46 (x=√2). Measured composite **0.2447/0.4214 = 0.5807**. Derivation and measurement
agree, so the L-form gap is understood, not just observed.

**Consequence — a defect in docs/37 §4 candidate 0 and docs/35 §9.3.1.** Both quote a
"further ×0.790" for "the literal Desmet–Govers finite-difference L". That 0.790 is
`ls2d_dg96/ls2d` from `journal_c31-ls2d.md` §S4 — and reading `scripts/c3/ls2d.py` L308–313,
`ls2d_dg96 = L_dg × S_McCool87` while `ls2d = L_cont × S_MooreBurch`. **The 0.790 therefore
bundles an L-form change AND an S-formulation change**, and it was then multiplied onto a row
(`all three`, ×0.4214) whose S had already been swapped to W&S-78 — the S change is counted
twice, in opposite directions. Measured directly instead: the Buarque method with his own
D&G L is **×0.2447**, not ×0.333. **The corrected source-faithful bracket is ×0.245 – ×0.421,
i.e. our LS is 2.37× – 4.09× the level α = 11.8 is paired with, not 2.37× – 3.00×.** The
correction widens the bracket downward; it does not flatter us.

### Step 5 — second harness pass: AH-703's own rill/interrill provision on `m`

AH-703 p. 105–106 makes `m` a *land-condition* parameter, not only a slope function: **double β**
where the soil is highly rill-susceptible (construction), **halve β** where the rill:interrill
ratio is low — and, verbatim, "Values for m and LS for **rangelands** are usually taken from
tables for the **low** ratio of rill to interrill erosion". Measured on the same 30,235,916 cells:

| variant | awm | × ours |
|---|---|---|
| `ours_m_low` — AH-703 low column, β halved (median m 0.4129) | 20.233 | **0.508** |
| `ours_m_high` — AH-703 high column, β doubled | 72.138 | 1.812 |
| `rusle_mod_dg_400ft` — D&G L + McCool-89 m + McCool-87 S + length ≤ 400 ft | 8.187 | **0.206** |
| `rusle_low_dg_400ft` — same with the AH-703 low column | 6.421 | **0.161** |
| `rusle_low_dg_pixel` — same with the 1-pixel limiter | 5.215 | 0.131 |

**Two things follow, and both are measurements, not opinions.**
1. The `m` lever's magnitude (×0.505 for Buarque's USLE 0.5 cap) is reproduced almost exactly by
   a **cited, RUSLE-internal** provision (×0.508 for AH-703's rangeland column). So the lever does
   not disappear when the USLE cap is retired — it is **re-founded on a better citation** with the
   same magnitude, on a basin whose dominant classes are forest/shrub/grassland (docs/41: grassland
   alone carries 36.8 % of the area-weighted basin C).
2. **Two independent reconstructions converge.** The transposed source method rebuilt on our grid
   (Buarque: D&G L, step m, W&S S, 1-pixel) gives **9.741**; the RUSLE handbook rebuilt on our grid
   (D&G L, McCool m, McCool S, AH-703's own 400 ft) gives **8.187** — **within 19 % of each other**,
   and both **≈ 4–5× below our production 39.812**. The convergence is the strongest single piece
   of evidence in this journal, because the two paths share no formulation choice except the L form.

Consequences for the `docs/35` §6.1 α guard, recomputed:

| LS reference | ratio ours/ref | like-for-like α for 11.8 | §6.1 band 5.9–23.6 → | hard stop 35.4 → |
|---|---|---|---|---|
| Buarque, continuous L (docs/37's "all three") | 2.373 | 4.97 | 2.49 – 9.95 | 14.92 |
| **Buarque, his own D&G L** | **4.087** | **2.89** | 1.44 – 5.77 | 8.66 |
| RUSLE-faithful, moderate m, 400 ft | 4.863 | 2.43 | 1.21 – 4.85 | 7.28 |
| RUSLE-faithful, low m, 400 ft | 6.201 | 1.90 | 0.95 – 3.81 | 5.71 |

docs/37 §4 candidate 0 quotes α ref ≈ 3.9–5.0, band ≈ 2.0–9.9, stop ≈ 11.8–14.9. **Every one of
those is too generous.** The guard tightens further; nothing here loosens it.

**A caveat that bounds ALL of the above and that I cannot resolve from the sources I obtained:**
α = 11.8 is Williams' (1975) MUSLE coefficient and predates every 2-D contributing-area LS by two
decades. Buarque's LS is *closer* in formulation to it (USLE m, USLE S) than ours, which is why
docs/35 §6.1 registers his as the comparator — but **no 2-D LS is strictly like-for-like with the
LS α = 11.8 was fitted against.** NOT SETTLED.

### Dead ends / what a successor should not repeat
- **ScienceDirect is closed to this environment.** Fagundes et al. (2026) ISWCR is *diamond open
  access* and still 403s on WebFetch, `requests` with browser headers, doi.org, linkinghub,
  `/pdfft`, DOAJ API and OpenAlex `best_oa_location`. Same for AGU/Wiley (Fagundes 2021 WRR),
  Taylor & Francis (Desmet & Govers 1996; Mitasova et al. 1996) and MDPI (Panagos et al. 2015 PDF).
  What DID work: USDA-ARS `tucson.ars.ag.gov/unit/publications/PDFfiles/*.pdf`, `regulations.gov`
  attachment mirrors, Copernicus preprints, `lume.ufrgs.br`, `geomorphology.sese.asu.edu`,
  `pmc.ncbi.nlm.nih.gov` (via WebFetch, not requests), `esdac.jrc.ec.europa.eu`, and the GitHub API.
- **Decompiling the MGB-SED binary for LS constants failed.** Exhaustive float32/float64 scans of
  `formPRESED.exe` find no 22.13 / 0.0896 / 65.41 / 0.065 / 10.8 / 16.8. The *strings* are the
  usable evidence; the numbers are not there. Do not spend more time on it.
- **`gh` is not on PATH on this box** — use the GitHub REST API via `requests`.
- Running `scripts/c3/ls2d.py` at any `--scale` **overwrites** `data/processed/urh_ls2d.csv` and
  `minibacia_ls2d.csv`. I did not run it. `scratchpad/ls_levers.py` imports its helpers instead and
  writes only to the scratchpad; it reproduces `ls2d_hs` awm 39.8123 as its validation gate.

### Files this run produced (all outside the repo except this journal)
`scratchpad/{getpdf.py, ls_levers.py, ls_levers.json, ls_levers2.json, slope_dist.py,
slope_dist.json}` and the retrieved sources `{ah703, usle_ch8, mccool_rusle775, buarque2015,
md1988, md1989, rusle_review, dg_ext, rdsm_amazon}.{pdf,txt}`. **No repository data, code or
numbered doc was modified.**
