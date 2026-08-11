# Journal — decide-ls-resolution

**Agent slug:** `decide-ls-resolution`
**Started:** 2026-08-11
**Goal:** Decide whether the 90 m LS2D level used by the MUSLE engine is defensible, or
whether a reference resolution / correction is required. The decision must be resolved from
source evidence about LS and DEM resolution, and from the internal coherence of the MUSLE
factor set — **never** from what it does to the basin sediment total.

## Overriding discipline (restated so it binds me)

- I will write the DECISION and its justification into this journal **BEFORE** I compute or
  look up its effect on the basin total (144–184 Mt/yr outlet anchor).
- "It makes the number match" is not evidence. If the evidence does not settle it, I write
  UNRESOLVED and state what would settle it.
- Read-only on the frozen artifacts (`sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv,
  q_gauge_H2E.csv, q_gauge_H2E.npz}`). No git. No calibration launches.

## Checklist

- [ ] 0. Journal created; read docs/35, docs/33, docs/36, journal_c31-ls2d, scripts/c3/ls2d.py
- [ ] 1. Establish the resolution/scale-effect phenomenon from literature, with quotable sources:
      published quantifications of LS vs DEM cell size; the resolution at which basin-scale
      MUSLE/RUSLE applications are run; the resolution behind "mountainous LS 2–10"; whether an
      accepted correction or reference resolution exists.
- [ ] 2. Measure OUR scale behaviour: basin LS distribution at ≥3 resolutions (90 m native,
      one intermediate, 740 m) with the existing `scripts/c3/ls2d.py` machinery. Fit the scaling.
      Is it a clean power law in cell size? Report the exponent.
- [ ] 3. Coherence argument: at what scale does the eroding process operate, and at what scale do
      K, C, P, and the model's own computational unit (minibacia, ~25 km², 740 m grid) sit? Is a
      90 m LS coherent with 740 m K/C/P?
- [ ] 4. DECISION written here, with justification, BEFORE any basin-total computation.
- [ ] 5. State the consequence for the C4 anti-compensation alpha guard (docs/35 §6.3).

## Log

### Step 0 — orientation (2026-08-11)

Created journal. Read `scripts/c3/ls2d.py`, `docs/agents/journal_c31-ls2d.md`, `docs/35` §1–§6
and §9.1, and the LS consumption path in `src/mgb_sediment.py`.

Facts fixed before any measurement:

- The engine consumes `urh_ls2d.csv:ls2d_hs` — the **area-weighted mean** of per-cell
  `ls2d_hs` inside each (minibacia, URH), not the median (`src/mgb_sediment.py` L601–681).
- `ls2d_hs` = same equation, upslope **area** capped at `A_CHANNEL_M2 = 1e6` m² (1 km²).
- Registered MUSLE application unit (docs/35 §4): `a_p = 0.0081 km²`, i.e. **the 90 m COP90
  pixel**, with `Sed_URH = (A_URH/a_p)·α·(Qsur·q_peak·a_p)^β·K·C·P·LS2D·FG`.
- The α band (§6.1: 5.9–23.6, hard stop 35.4) is declared valid **only** at `a_p = 0.0081 km²`;
  §6.2 says any other application unit needs the whole band divided by `N^(2β−1)`.

### Step 1 — SOURCE EVIDENCE (2026-08-11). The decisive documents were obtained.

**1a. The source method's own thesis was retrieved and read.**
Buarque, D.C. (2015), *Simulação da geração e do transporte de sedimentos em grandes bacias:
estudo de caso do rio Madeira*, PhD thesis, IPH/UFRGS, 182 pp — the document that defines
MGB-SED, i.e. the method docs/35 §4 registers this project as transposing. Retrieved from
`https://lume.ufrgs.br/bitstream/handle/10183/129875/000977197.pdf`, text extracted with
PyMuPDF. Verbatim quotes with page numbers:

- **p. 77 (§5.1.1) — the DEM MGB-SED actually used for the Madeira:**
  > "O Modelo Digital de Elevação (MDE) utilizado possui resolução espacial de 15'' (aproximadamente
  > 500 m) e foi obtido a partir dos dados provenientes do HydroSHEDS […]. O MDE com resolução
  > espacial de, aproximadamente, 90 m apresentado na Figura 12 **não foi utilizado devido ao
  > excessivo custo computacional**, tanto para a etapa de pré-processamento como para a etapa de
  > simulação, para sua aplicação em toda a bacia do rio Madeira."

  So the source application ran at **~500 m**, and it rejected 90 m explicitly for *cost*, not
  for any physical or methodological reason. (p. 31 separately introduces SRTM-90m as the
  standard MGB-IPH terrain source: "SRTM-90m […] com resolução de 90 m (ou 0,0008333°)".)

- **p. 94 (§6.2) — the slope-length limiter, which we do NOT have:**
  > "Apenas o fator LS é determinado na etapa de pré-processamento, **para cada pixel do MDE** […].
  > Na determinação do fator comprimento de 'L', **seu valor máximo foi limitado ao tamanho do
  > pixel do MDE**."

- **p. 121 (§7.3) — the author's own verdict on his Andean LS:**
  > "Apesar dos valores de comprimento (L) obtidos para cada pixel do MDE seja **limitado pela
  > resolução de 500 m**, o valor máximo é grande e tende a fazer com que as estimativas da erosão
  > laminar do solo em áreas íngremes, como nos Andes, **seja superestimado** (EPA, 2004)."

- **p. 46–48 (§3.3) — the formulation, eqs. 13/14/15/18:** `L` = Desmet & Govers (1996) finite
  difference (his eq. 13, identical in form to our `ls2d_dg96`); `m` is a **step function capped
  at 0.5** — 0.2 (Sf < 1 %), 0.3 (1–3 %), 0.4 (3–5 %), **0.5 (Sf ≥ 5 %)** (eq. 14); `S` is
  **Wischmeier & Smith (1978)**, `S = 65.41·sin²θ + 4.56·sinθ + 0.065` (eq. 18); slope from
  centred finite differences over the four orthogonal neighbours (Wilson & Gallant 2000).

**1b. What this means, stated before any measurement.** Three separate levers were conflated in
the gate-2 failure and they must be separated:

| lever | ours | Buarque (2015) MGB-SED |
|---|---|---|
| DEM cell size | 90 m | ~500 m (15″ HydroSHEDS) |
| slope-length limiter | upslope **area** ≤ 1 km² ⇒ `a_unit` up to 1e6/92 ≈ **10,870 m** | slope length ≤ **one pixel** (≈ 500 m) |
| `m` | continuous McCool (1989), **can exceed 0.5** on Andean slopes | stepped, **hard-capped at 0.5** |
| `S` | `(sinθ/0.0896)^1.3` (Moore & Burch 1986) | `65.41 sin²θ + 4.56 sinθ + 0.065` (W&S 1978) |

Only the first row is my task. The second and third rows are separate deviations from the
source method and I will report them as findings, not silently fold them into the resolution
decision.

**1c. Literature on the scale effect (task 1), sources named:**

- *Underlying mechanism of the topographic factor scale effect in soil erosion equations*,
  J. Mountain Science (2024), doi 10.1007/s11629-024-9448-4: 20 watersheds, 10 m vs 30 m DEMs.
  Finding quoted: "the **S factor**, heavily influenced by **slope underestimation in
  coarse-resolution DEMs**, makes a difference in the LS factor scale effect" and "the LS factor
  scale effect becomes **less significant with increasing reliefs**, suggesting the possibility of
  using 30-m DEM for LS calculation in rugged terrains."
- Wu, S., Li, J. & Huang, G. (2005), *An evaluation of grid size uncertainty in empirical soil
  loss modeling with digital elevation models*, Environ. Model. Assess. 10, 33–42,
  doi 10.1007/s10666-004-6595-4 — the standard citation that empirical soil-loss estimates are
  grid-size sensitive and that quantitative use of them requires stating the grid size.
- Panagos, P. et al. (2015), *A New European Slope Length and Steepness Factor (LS-Factor) for
  Modeling Soil Erosion by Water*, Geosciences 5(2), 117–126 — the continental reference
  application: **25 m** DEM, EU-wide mean LS **1.63**, range 0–99, LS > 25 on only **0.1 %** of
  the EU (Alps, Pyrenees, Apennines, Carpathians, Pindos). A continental application at 25 m,
  i.e. finer than ours, not coarser.
- *Impacts of horizontal resolution and downscaling on the USLE LS factor for different terrains*,
  Int. Soil Water Conserv. Res. (2020), S2095633920300538: in **larger-relief mountainous areas**,
  relative to 5 m, the **30 m** LS is *overestimated by more than 20 %*, and in lower-relief areas
  *underestimated by more than 15 %* — i.e. the sign of the resolution error is itself
  relief-dependent, which matters for a bimodal basin like ours.

**Provenance of the "mountainous 2–10" gate:** it is quoted in `scripts/c3/ls2d.py` and in
`journal_c31-ls2d.md` **without a citation**, and I could not find a source that states a
resolution-free "2–10" for mountainous LS. Panagos et al. (2015) is the closest published
distributional reference and it is EU-wide (mean 1.63 at 25 m, dominated by lowland). A
resolution-free LS band is not a meaningful object given 1c; I will treat gate 2 as a weak,
uncited yardstick and say so.

### Step 2 — plan for the measurement (about to run; risky-op note)

`scripts/c3/ls2d.py` **writes** `data/processed/minibacia_ls2d.csv` and `urh_ls2d.csv`, which are
the committed inputs the sediment engine reads. Running it at any `--scale` other than 1 would
silently clobber the 90 m products. **I will not run it.** Instead
`scratchpad/ls_scale.py` imports its `ls_variants`, `slope_exponent_m`, `locate_dem` and its
constants, recomputes only the per-cell distribution, and appends one JSON line per scale to the
scratchpad. Nothing under `data/` is written.

Scales: 1 (90 m), 2 (180 m), 4 (360 m), 8 (740 m) — `--scale` must divide 8 because the
minibacia grid is 1/8 of the DEM grid. Coarse DEMs are made by `RS.average` aggregation of the
same COP90 source, which is the controlled way to isolate cell size (it is *not* a claim that an
aggregated 740 m DEM equals a native 740 m product).

### Step 2 results — MEASURED SCALE BEHAVIOUR (4 resolutions, 2026-08-11)

Validation first: the `--scale 8` row reproduces `journal_c31-ls2d.md` §S3b exactly
(`ls2d` median 7.508, area-wtd mean 48.669; `ls2d_hs` median 5.524, mean 22.192), and the
`--scale 1` row reproduces §S4 exactly (`ls2d` median 12.774, `ls2d_hs` median 12.486,
`ls2d_hs` area-wtd mean 39.812). The harness is the same code, so the intermediate rows are
comparable.

| D (m) | basin cells | `ls2d` med | `ls2d` awm | `ls2d_hs` med | `ls2d_hs` awm | tanθ med | `a_unit` med (m) | `a_unit_hs` med / p90 | m med | cells with upa < 1 km² |
|---|---|---|---|---|---|---|---|---|---|---|
| 92.2 | 30,235,916 | 12.774 | 104.901 | **12.486** | **39.812** | 0.1581 | 185.2 | 185.2 / 3423.4 | 0.584 | **95.5 %** |
| 184.3 | 7,558,979 | 12.392 | 82.734 | 11.723 | 37.595 | 0.1237 | 370.2 | 370.2 / 5411.7 | 0.550 | 91.5 % |
| 368.7 | 1,889,752 | 10.544 | 69.140 | 9.198 | 32.092 | 0.0932 | 739.8 | 739.8 / 2712.6 | 0.507 | 84.0 % |
| 737.4 | 472,438 | 7.508 | 48.669 | 5.524 | 22.192 | 0.0670 | 1478.5 | **1352.8 / 1359.6** | 0.452 | **57.7 %** |

**Is it a clean power law in cell size? NO — and that is a result, not a nuisance.**
Log–log fits of `y = c·D^p`:

| quantity | p | R²(log) | 737/92 ratio |
|---|---|---|---|
| tanθ median | **−0.4127** | **0.9956** | 0.424 |
| tanθ mean | −0.3756 | 0.9931 | 0.458 |
| `ls2d` area-wtd mean | −0.3583 | 0.9813 | 0.464 |
| `ls2d_hs` area-wtd mean | −0.2758 | 0.8802 | 0.557 |
| `ls2d` median | −0.2533 | 0.8652 | 0.588 |
| `ls2d_hs` median | −0.3879 | 0.8779 | 0.442 |

The *slope* field is a near-perfect power law (R² 0.993–0.996, p ≈ −0.38…−0.41). **LS is not**
(R² 0.87–0.88 for the medians). The residual structure is systematic, not noise: the
sensitivity **decays monotonically toward fine resolution**. Cost of halving the cell size, in
`ls2d_hs` median: 737→369 m **+66.5 %**, 369→184 m **+27.5 %**, 184→92 m **+6.5 %**. For the
uncapped `ls2d` median: **+40.4 %, +17.5 %, +3.1 %**. So a single "resolution correction
exponent" is not a well-posed object, and the 90 m value sits on a flattening curve rather than
on a divergence.

**Mechanism, decomposed on our own data (and it matches the published one).** Going 92 → 737 m
the slope term `(sinθ/0.0896)^1.3` falls ×0.33 while the length term `(m+1)(a_unit/22.13)^m`
rises ×1.70; net ×0.56 (measured `ls2d_hs` median ratio 0.442). The **S term dominates**, which
is exactly the mechanism reported by J. Mountain Science (2024) doi 10.1007/s11629-024-9448-4
("the S factor, heavily influenced by slope underestimation in coarse-resolution DEMs, makes a
difference in the LS factor scale effect"). `a_unit` median tracks D exactly (185.2 / 370.2 /
739.8 ≈ 2.00·D — the median cell has ~2 cells of upslope area).

**The `ls2d_hs` cap becomes unrepresentable at coarse resolution — measured.** At 737 m one cell
is 0.544 km², so the 1 km² channel-initiation cap binds on **42.3 %** of basin cells and the unit
contributing length collapses to a near-constant (median 1352.8 m, p90 1359.6 m — both equal
1e6/D to three figures). The hillslope/channel distinction that the column exists to draw is not
representable on that grid. At 92 m the cap binds on **4.5 %** of cells and `a_unit_hs` spans
185 m (median) to 3423 m (p90).

### Step 2b — does the law continue BELOW 90 m? (the only finer DEM in the repo)

`data/processed/cop30_dem.tif` covers the lower-Magdalena window only (docs/35 §2: 1,506 of
8,672 minibacias) but it does contain the Sierra Nevada de Santa Marta — 3.02 M cells above
1000 m at 30 m. Slope needs no flow routing, and slope is the dominant term, so the sub-90 m
question can be answered on the slope field alone. COP30 aggregated to 30/90/180/360 m:

| D (m) | tanθ med (all) | tanθ med, <200 m | tanθ med, >1000 m |
|---|---|---|---|
| 30 | 0.0277 | 0.0199 | **0.5562** |
| 90 | 0.0137 | 0.0098 | **0.4831** |
| 180 | 0.0088 | 0.0063 | 0.4138 |
| 360 | 0.0060 | 0.0042 | 0.3287 |

| band | p | R² | 30→90 ratio | 90→180 |
|---|---|---|---|---|
| lowland < 200 m | −0.6274 | 0.9995 | **2.032** | 1.555 |
| **Andean > 1000 m** | **−0.2072** | 0.9499 | **1.151** | 1.167 |

On the **erosive** terrain the resolution sensitivity of slope is weak: refining 90 → 30 m raises
median tanθ by only **15.1 %**, i.e. LS by ≈ 1.151^1.3 = **1.20**. On near-flat lowland it is
strong (2.03×) but lowland LS is ~0.2 and contributes almost nothing. **So refining below 90 m
would raise, not lower, the erosive-terrain LS, and only by ~20 %.**

---

## DECISION (recorded 2026-08-11, BEFORE computing any effect on the basin total)

> **I confirm: this decision and its full justification are written here before I compute or look
> up what it does to the basin sediment total. Nothing below was chosen to move a number toward
> the 144–184 Mt/yr outlet anchor.**

> ### DECISION: **Keep LS2D at the native 90 m COP90 resolution. No reference resolution is
> adopted and NO resolution correction is applied. Gate 2's "mountainous 2–10" comparison is
> retired as an uncited, resolution-free yardstick rather than acted on.**

Justification, in order of weight — every item is a derivation or a source, none is an appeal to
the total:

**D1 — the cell size is not a free choice; it is fixed by the registered application unit.**
In the Desmet & Govers formulation D is not a display resolution, it *is* the plot whose length
factor is being computed: `a_unit = (A_in + D²)/D`, so the smallest possible contributing length
is D itself, and the finite-difference L (their eq. 11 = Buarque eq. 13) is an explicit function
of D. LS(D) is therefore "the topographic factor **of a D × D plot**". docs/35 §4 registers the
MUSLE application unit as `a_p = 0.0081 km²`, and `src/mgb_sediment.py` literally multiplies by
`A_URH/a_p`, the count of 90 m pixels. `√a_p = 90 m`. Evaluating LS at 740 m while keeping
`a_p = 0.0081 km²` would put a 0.547 km² plot's length factor and a 0.0081 km² plot's erosivity
term in the same product — two different plots in one equation. **90 m is forced, not preferred.**

**D2 — it is the source method's own principle, and the source's coarser instance is an
obsolete cost constraint, not a physical one.** Buarque (2015) computes LS "para cada pixel do
MDE" — LS at the MUSLE pixel, which is D1. He ran it at ~500 m and says why, verbatim (p. 77):
the 90 m DEM "**não foi utilizado devido ao excessivo custo computacional**" for a 1.4 × 10⁶ km²
basin. Our basin is 257,097 km², 5.4× smaller, and the 90 m LS pass completes in ≈ 4 minutes.
Copying his 500 m would be inheriting a 2015 hardware limit as if it were method.

**D3 — the column the engine actually consumes is only defined at fine resolution.** The engine
reads `ls2d_hs`, whose whole content is the 1 km² channel-initiation cap. Step 2 measured that at
740 m the cap binds on 42.3 % of cells and `a_unit_hs` degenerates to a constant (median = p90 =
1e6/D). A coarse `ls2d_hs` is not a coarser estimate of the same quantity; it is a different,
degenerate quantity.

**D4 — the measured scaling forbids a "correction" and shows 90 m is near the plateau.** LS is
not a power law in D (R² 0.87 vs 0.99 for slope alone), so there is no principled exponent to
correct with; and the sensitivity decays 40.4 % → 17.5 % → 3.1 % per halving toward the fine end.
The 90 m level is not an artefact of over-resolution.

**D5 — the only sub-90 m evidence says 90 m under-states, not over-states, the erosive LS.**
Step 2b: on terrain above 1000 m, 90 → 30 m raises median tanθ by 15.1 % (LS by ≈ 1.20). If 90 m
is biased at all against a finer DEM, it is biased **low** on exactly the terrain that produces
the sediment. Gate 2's "fails high" reading is therefore not supported by refinement either.

**D6 — the yardstick that failed is weak.** "mountainous 2–10" appears in `scripts/c3/ls2d.py`
and `journal_c31-ls2d.md` with **no citation**, and per D4 a resolution-free LS band is not a
well-defined object. The nearest published distributional reference, Panagos et al. (2015)
Geosciences 5(2) 117–126, is a **25 m** continental product (finer than ours) with EU mean 1.63
and LS > 25 on 0.1 % of the EU — a lowland-dominated continent evaluated with the McCool S
factor, not our `(sinθ/0.0896)^1.3`. It is not like-for-like with an Andean basin and cannot
adjudicate our level.

### Coherence with K, C, P — the argument the task asked for, answered explicitly

K, C and P are **intensive** factors: a 90 m pixel and a 740 m pixel of the same soil and the
same cover have the **same** K and the same C. Their definitions contain no cell size. That they
are supplied at URH/minibacia granularity is a *spatial-detail* limitation (sub-URH heterogeneity
is unresolved), not a scale-convention mismatch — the URH-mean K is simply the best available
estimate *of the 90 m pixel's* K. LS is different in kind: its definition contains D, so it is
not "K at a different resolution", it is the geometry of the modelled plot. Therefore the
coherence requirement is **not** "evaluate every factor on the same grid"; it is "evaluate every
factor **for the same plot**", and the plot is fixed at `a_p` by docs/35 §4. Degrading LS to
740 m would not buy coherence with K/C/P — it would break coherence with `a_p` while restoring
nothing, because coarsening LS destroys information and does not recover the lost within-URH
covariance between steepness and cover. That residual covariance loss (steep cells are more
likely bare) is a real and separate bias; it is not fixed by a resolution choice.

### CONSEQUENCE FOR THE C4 ANTI-COMPENSATION α GUARD (docs/35 §6.1–§6.3) — stated, not hidden

1. **This decision preserves the guard, and that is the point of D1.** §6.2 rescales the α band
   by `N^(2β−1)` when the **application unit** changes. There is **no registered rescaling for a
   change in the LS evaluation scale** — because none is possible: MUSLE is *linear* in LS, so an
   LS level change of factor f moves the fitted α by exactly 1/f with no compensating rule. Had
   we coarsened LS to 740 m while keeping `a_p = 0.0081 km²`, the `ls2d_hs` area-weighted mean
   would have fallen 39.812 → 22.192 (×0.557) and every fitted α would have risen ×1.79 against
   an unchanged band — the guard would have fired for a reason that was pure bookkeeping. Keeping
   90 m keeps α comparable to 11.8 and keeps the §6.1 hard stops enforceable.

2. **BUT the guard has a crack that this decision does not open and cannot close, and it is
   larger than the resolution lever.** Step 1a found that our LS *formulation* differs from the
   MGB-SED reference's in three ways that all bear on the level:
   - **slope-length limiter:** Buarque (2015) p. 94, "seu valor máximo foi limitado ao tamanho do
     pixel do MDE" — the slope length is capped at **one pixel**. Ours (`ls2d_hs`) caps the
     upslope **area** at 1 km², allowing `a_unit` up to 1e6/92 ≈ **10,870 m** ≈ 118 pixels.
   - **m:** his eq. 14 is a step function **hard-capped at 0.5**; ours is continuous McCool (1989)
     and exceeds 0.5 on Andean slopes (measured basin median **0.584** at 90 m).
   - **S:** his eq. 18 is Wischmeier & Smith (1978) `65.41 sin²θ + 4.56 sinθ + 0.065`; ours is
     `(sinθ/0.0896)^1.3` (Moore & Burch 1986).

   α = 11.8 in this lineage is paired with **that** LS. Because MUSLE is linear in LS, any level
   difference between our LS and the reference LS passes one-for-one into the fitted α. **The
   §6.1 band is therefore only as enforceable as our LS is the reference LS**, and right now that
   equivalence is asserted, not measured. This is a real, currently unquantified weakening of the
   C4 guard. It is a C3.1 formulation question, **not** a resolution question, and it is not mine
   to change — I flag it as the next pre-registered item.

3. Buarque's own verdict on his Andean LS (p. 121) is that even with the 500 m pixel-capped L,
   "o valor máximo é grande e tende a fazer com que as estimativas da erosão laminar do solo em
   áreas íngremes, como nos Andes, **seja superestimado**". The source method reports its Andean
   LS as an over-estimate. Ours is built with a *looser* length limiter than his. That points the
   same way as gate 2 — but it points at the **limiter**, not at the resolution.

### What is RESOLVED and what is UNRESOLVED

- **RESOLVED:** the *resolution* question. 90 m, by D1–D6. No correction.
- **UNRESOLVED (and explicitly named as such):** the *level* question that gate 2 was really
  probing. Resolution does not settle it and cannot: the residual level uncertainty lives in the
  slope-length limiter, the m cap and the S function (item 2 above). What would resolve it: run
  the identical grid through Buarque's exact eqs. 13/14/18 with L capped at one pixel and compare
  the level, pre-registering the comparison before looking at any basin total.

---

### Step 3 — AFTER the decision: the formulation diagnostic, and the effect on the basin total

The decision above is locked. What follows was computed afterwards, in the order stated.

**3a. Effect of the decision on the basin sediment total: exactly none.** 90 m is what
`data/processed/urh_ls2d.csv` already holds and what `src/mgb_sediment.py` already reads. The
decision is *keep*, so the multiplier on the docs/35 §9.1 gate-(b) table is **1.000** and all three
convention rows (0.6844 / 9.0222 / 32.7577 Mt/yr) stand unchanged.

For completeness, what the rejected alternative would have done — MUSLE is linear in LS, so the
factor is the ratio of area-weighted `ls2d_hs`: adopting 740 m would multiply the basin load by
22.192/39.812 = **0.557**, i.e. `pixel_km2` 0.6844 → 0.381 Mt/yr. **The rejected option moves the
model further from the outlet anchor, and the option I adopted is the one that keeps the load
higher.** That asymmetry is disclosed deliberately: D1 is a derivation from the registered
application unit, it was written before this paragraph, and item 3b below shows that the net of
this run's findings moves the total *away* from the anchor, not toward it.

**3b. The guard-crack, now with numbers (DIAGNOSTIC ONLY — nothing was changed).**
`scratchpad/ls_formulation.py`, 90 m, all 30,235,916 basin cells, same harness (it reproduces
`ours_hs` = 39.812 / median 12.486 / p90 99.204 bit-for-bit, so the comparison is like-for-like).
Each row swaps in **one** of Buarque's three choices, holding the other two at ours:

| LS variant at 90 m | area-wtd mean | Andean (>1000 m) awm | median | p90 | ×  ours |
|---|---|---|---|---|---|
| **ours** (`ls2d_hs`: A≤1 km², McCool-89 m, `(sinθ/0.0896)^1.3`) | **39.812** | 65.199 | 12.486 | 99.204 | 1.000 |
| + m hard-capped at 0.5 (his eq. 14) | 20.005 | 31.820 | 9.911 | 51.490 | **0.502** |
| + S = Wischmeier & Smith 1978 (his eq. 18) | 68.234 | 114.202 | 15.072 | 180.394 | **1.714** |
| + slope length ≤ 1 pixel (his p. 94 limiter) | 13.985 | 22.308 | 7.511 | 39.014 | **0.351** |
| **all three (source-method LS)** | **16.775** | 27.109 | **7.262** | 49.136 | **0.421** |

Reading, stated carefully:

- **Our LS level is ≈ 2.37× the level the α = 11.8 reference is paired with**, evaluated on the
  *same* 90 m grid — so this is a formulation difference, not a resolution difference. Using the
  literal Desmet & Govers finite-difference L (his eq. 13) instead of the continuous form would
  lower the source row a further ×0.790 (the ratio `journal_c31-ls2d.md` measured, stable at both
  90 m and 740 m), giving **2.37× – 3.00×**. Quote it as a bracket.
- The three levers partly cancel (0.502 × 1.714 × 0.351 = 0.302 vs the joint 0.421 — m and L
  interact), so no single one of them is "the" cause.
- The dominant one is the **slope-length limiter**, ×0.351. Ours lets the unit contributing length
  reach 1e6/92 ≈ 10,870 m ≈ 118 pixels; his stops at one pixel. Interpretation note: I read
  p. 94 ("seu valor máximo foi limitado ao tamanho do pixel do MDE") together with p. 121 ("os
  valores de comprimento (L) […] limitado pela resolução de 500 m, o valor máximo é grande") as
  *slope length ≤ one pixel*, which is the only reading consistent with both sentences. If some
  other reading is intended, this row changes and the bracket must be redone.
- **Consequence for the C4 α guard, in the guard's own units:** because MUSLE is linear in LS,
  a fit on our LS returns an α that is 1/2.37 (to 1/3.00) of what the same observations would
  return on the source's LS. So the like-for-like α reference for **our** LS is not 11.8 but
  **≈ 3.9 – 5.0**, the §6.1 expected band 5.9–23.6 becomes ≈ **2.0 – 10.0**, and the hard stop
  α > 35.4 becomes ≈ **11.8 – 14.9**. **This makes the guard TIGHTER, not looser** — the gate-(b)
  α values needed to reach 144 Mt/yr (2,483 / 188 / 52) go from 70.1× / 5.3× / 1.5× past the stop
  to roughly **167× / 12.6× / 3.5×** past it. The §6.1 verdict is unchanged in direction and
  strengthened in size.
- **And the net effect of this run's findings on the basin total is DOWNWARD.** A source-faithful
  LS would multiply the load by 0.421 (to 0.33), taking `pixel_km2` 0.6844 → **0.288 Mt/yr**
  (0.228 at 0.33) and widening the gap from 210–269× to roughly **500–800×**. I am recording that
  because it is the plainest available evidence that this run was not steering toward the anchor:
  the thing I found makes the headline problem worse.
- **I did not change it.** `scripts/c3/ls2d.py`, `data/processed/urh_ls2d.csv`,
  `src/mgb_sediment.py` and docs/35 are untouched. The formulation question belongs to C3.1 and
  needs its own pre-registration (choose the limiter, the m cap and the S function on source
  grounds *before* looking at the total), because it is worth 2.4–3.0× and is therefore exactly
  the kind of lever that could be used to fit the answer.

### Recommendation on gate 2 (not applied — for whoever owns the C3.1 record)

Gate 2 as written compares a resolution-free "mountainous 2–10" of unknown provenance against a
90 m per-cell median. Per D4 that comparison is not well posed. If a gate is wanted, make it
like-for-like: the source-method LS on our own grid (row 5 above) has basin per-cell median
**7.262**, which *does* sit inside 2–10 — i.e. the "2–10" band is plausibly a band for
*pixel-length-limited* LS, and our failure of it is a fingerprint of the **limiter**, not of the
**resolution**. That reframing is a hypothesis worth pre-registering, not a result.

### Checklist — closing state

- [x] 0. Journal created; docs/35, docs/33 §, journal_c31-ls2d, ls2d.py, mgb_sediment.py read
- [x] 1. Phenomenon established with sources (J. Mtn Sci 2024; Wu et al. 2005; Panagos et al.
      2015; ISWCR 2020) **and** the source method's own resolution recovered from Buarque (2015)
- [x] 2. Own scale behaviour measured at 4 resolutions (92 / 184 / 369 / 737 m) + a sub-90 m
      slope check on COP30; power law fitted and **rejected** for LS (R² 0.87 vs 0.99 for slope)
- [x] 3. Coherence argument made from `a_p` and from the intensive/extensive distinction
- [x] 4. DECISION recorded before any basin-total computation (stated explicitly above)
- [x] 5. Consequence for the C4 α guard stated: preserved by this decision, but independently
      cracked by the formulation mismatch, with the corrected band quantified

Files written by this run: this journal, and (outside the repo) `scratchpad/ls_scale.py`,
`scratchpad/ls_scale.jsonl`, `scratchpad/ls_formulation.py`, `scratchpad/ls_formulation.json`.
No repository data, code or doc was modified.
