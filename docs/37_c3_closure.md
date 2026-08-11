# 37 — C3 closure verdict: **OPEN**

**Stage:** C3.6 of `docs/31_phase_c_workplan.md`. **Written 2026-08-11**, after the convention
amendment of `docs/35` §9.2 was applied to `src/mgb_sediment.py` and the basin decade was re-run.

C3 is **OPEN**, not closed. Precisely:

| closure condition | status |
|---|---|
| the factor chain is fully explained by evidence-based corrections | **MET** — 0.684 → 248.73 Mt/yr is exactly `1000^0.56 × (1/0.1317) = 363.4245196`, measured to the last stored digit |
| no decision left unresolved | **NOT MET** (amended 2026-08-11) — the four *convention* questions below are resolved from source derivations, but a fifth question was measured and left explicitly UNRESOLVED: the **LS formulation level**. Our LS sits **2.37× – 3.00×** above the LS that α = 11.8 is paired with in the MGB-SED lineage, measured on our own 90 m grid. See §4 candidate **0**. |
| the independent audit agreed with the decisions | **MET** — agreement on all three decisions; the audit's fourth finding was verified here from this repository's own source text, not taken on trust |
| **the implied sediment delivery ratio is physically plausible (0.05 – 0.30)** | **NOT MET — implied SDR is 0.579 – 0.740**, and under §4 candidate 0 it becomes 1.37 – 2.22, i.e. impossible |

Do not read the METs as "closed with caveats". The purpose of C3 was to make the
basin-scale sediment level defensible, and it is not yet defensible.

**Amendment note (2026-08-11).** As first written, this document reported three METs and one
NOT MET, and omitted the LS-formulation term entirely. That omission pointed in the flattering
direction — it is the largest wrong-way term the C3 runs produced, and leaving it out made the
adopted result look better than the evidence supports. It is now §4 candidate 0, the row above
is corrected, and the two sentences that depended on it (in §2 here and in `docs/35` §9.2) are
qualified. Nothing else in this document changed; no number was moved toward the outlet anchor.

---

## 1. What was adopted, and on what evidence

Four convention questions, each resolved from a derivation or a source quotation and each now an
explicit named option on `SedParams` (`src/mgb_sediment.py`; every prior convention is still
reachable by name, so the choices stay reversible):

| # | question | adopted | factor vs the first run | evidence |
|---|---|---|---|---|
| 1 | unit convention of the `(Qsur · q_peak · A)` product | `volume_convention='williams_m3'` | **×47.8630** (`1000^0.56`) | Converting Williams' English form `Y[short ton] = 95 (Q[ac-ft]·q_p[cfs])^0.56 K C P LS` — 1 ac-ft = 1233.4818375 m³, 1 cfs = 0.028316846592 m³/s, 1 short ton = 0.90718474 t — gives `95 × 0.90718474 / 34.92823^0.56 = 11.7818`, i.e. **11.8 belongs to runoff volume in m³**. The mm·ha reading gives 42.78, the mm·km² reading 563.95. Derived independently twice, same answer. |
| 2 | numeric unit system of `K` | `k_unit_system='us_customary'` | **×7.593014** (`1/0.1317`) | The conversion in (1) leaves K/C/P/LS untouched, so 11.8 goes with **US-customary K numerics**. `notebooks/09_soil_parameters.ipynb` §4 states the stored K was made from "mid-range Wischmeier & Smith (1978) class values **converted to SI (×0.1317)**"; undoing it returns the textbook numbers (0.020→0.1519 ≈ sand 0.15; 0.045→0.3417 ≈ silt loam 0.34; 0.028→0.2126 ≈ clay 0.21), which identifies the transform rather than inferring it. `src/nbgen/make_nb12.py` labels the array `t.ha.h/ha/MJ/mm`. |
| 3 | LS2D aggregation | `ls2d_aggregation='area_weighted_mean'` | **×1.000** | `urh_ls2d.csv:ls2d_hs` already is the area-weighted arithmetic mean, and MUSLE is applied per DEM pixel and summed, which is what a factor entering linearly requires. A median (×0.5410) is not an admissible aggregate for a linear factor and is retained only as a reproducible diagnostic. |
| 4 | LS2D resolution | `ls2d_resolution='native_90m'` | **×1.000** | Keep native COP90 90 m; no correction, no reference-resolution rescaling. The "published mountainous LS 2–10" comparison that would have motivated a rescale is **uncited** and is retired rather than acted on. |

Total: `47.8630 × 7.593014 × 1.000 × 1.000 = 363.4245196`. The application scale stays at
`a_p = 0.0081 km²` (per-pixel, factor 1.000).

**The corrections are a pure level shift, and this is measured rather than assumed.** Both are
spatially and temporally uniform, so the adopted/legacy ratio was checked per unit and per day:
it spans 363.42451960716335 – 363.42451960717045 across all 8,672 minibacias and
363.4245196071665 – 363.4245196071668 across all 3,652 days. Every spatial and seasonal ratio
in §3 is therefore numerically identical to the first run's.

---

## 2. The re-run — basin decade, 2009-01-01 … 2018-12-31, adopted defaults

Frozen H2E hydrology (`h2e_drivers.npz:qsur_rel_mm`), 3,652 days × 8,672 minibacias,
32,782 URH cells, α = 11.8 and β = 0.56 **unfitted** (Williams 1975 starting values).

| quantity | value |
|---|---|
| **basin total, gross hillslope erosion** | **248.730 Mt/yr** (2,486,957,417 t over 3,652 d) |
| same run, pre-amendment convention | 0.684406 Mt/yr |
| measured amendment ratio | 363.4245196071666 (derived: 363.4245196071666) |
| mass ledger `eroded − delivered − Δstore` | **exactly 0.0**, `exact = True` |
| `cells` vs `collapsed` backend | relative difference **exactly 0.0** |
| wall time | 1.44 s |

### The implied delivery ratio, which is why this document says OPEN

MUSLE computes **gross hillslope erosion**; the outlet load is what survives channel transport
and floodplain deposition. So `SDR = outlet / gross` must be < 1, and for a basin of
257,097 km² the published expectation is roughly 0.05 – 0.30.

| against outlet anchor | implied SDR | verdict |
|---|---|---|
| 144 Mt/yr | **0.579** | above the plausible band |
| 184 Mt/yr | **0.740** | above the plausible band |

Read as the gross erosion that the anchor plus a plausible SDR would require:

| required SDR | required gross erosion | shortfall of the model | α that would be needed at the adopted convention |
|---|---|---|---|
| 0.30 | 480 – 613 Mt/yr | **1.93 – 2.47×** | 22.8 – 29.1 (1.93× – 2.47× Williams) |
| 0.15 | 960 – 1,227 Mt/yr | 3.86 – 4.93× | 45.5 – 58.2 — **past the `docs/35` §6.1 hard stop** |
| 0.05 | 2,880 – 3,680 Mt/yr | 11.6 – 14.8× | 136.6 – 174.6 — far past the hard stop |

The amendment moved the model onto the physically *possible* side of the outlet anchor for the
first time (gross 248.7 > outlet 144–184, where all three pre-amendment conventions had gross
*below* the outlet load, which is impossible). That is real progress. It is not closure.

> **CONDITIONAL — read with §4 candidate 0 (added 2026-08-11).** "Physically possible side" holds
> **only if** our LS is at the level that α = 11.8 belongs to. That equivalence was asserted, not
> demonstrated, when this sentence was written — and it has since been *measured*, on our own
> 90 m grid, as violated by **2.37× – 3.00×** (`docs/agents/journal_decide-ls-resolution.md` §3b).
> Applying the measured bracket takes 248.730 → **104.8 Mt/yr** (×0.421) or **82.8 Mt/yr**
> (×0.333), i.e. **below both anchors**, implied SDR **1.37 – 2.22** — back on the impossible
> side. So the sign of gate (b) is *not* yet secured; it is secured only at our LS level, and our
> LS level is the one thing in the chain that is known to be off and not yet corrected. Treat the
> "possible side" claim as provisional until C3.1 (`docs/35` §9.3) settles the formulation.

---

## 3. The two pre-registered pattern gates — both PASS, and both unchanged by the amendment

### Gate (a) — Andean flanks ≫ lowland floodplain: **PASS, 11.61×**

Terrain classifier is mean elevation per minibacia from the corrected COP90 DEM, block-averaged
onto `minibacias.tif` (8,672/8,672 covered; elevation p0/p5/p50/p95/p100 =
6.2 / 27.2 / 898.6 / 3,090.7 / 4,491.1 m). Elevation is never a MUSLE input, so the gate is not
circular — classifying by LS2D would have been.

All specific-erosion figures below are **MODEL-INTERNAL specific erosion in t/km²/yr**: the
model's own erosion divided by the model's own minibacia area. They are **not** gauge-referenced
sediment yields, which remain embargoed (`docs/23` §13.2 — catchment areas disagree by >2× on
36 % of shared gauges).

| band (mean elevation) | n | area % | erosion % | spec., area-wtd | spec., median |
|---|---|---|---|---|---|
| Lowland floodplain <100 m | 1,736 | 19.2 | **1.60** | 80.2 | 11.4 |
| Piedmont 100–500 m | 1,691 | 19.3 | 8.46 | 424.6 | 169.6 |
| Lower Andean 500–1500 m | 2,442 | 28.1 | 29.96 | 1,033.2 | 820.5 |
| Upper Andean 1500–3000 m | 2,286 | 27.0 | 23.10 | 826.9 | 504.9 |
| High Andes >3000 m | 517 | 6.4 | 36.89 | 5,561.7 | 593.4 |

- **Andean flanks (500–3000 m) 931.95 vs lowland floodplain (<100 m) 80.25 = 11.61×.**
- Spearman(specific erosion, mean elevation) = **+0.554** over 8,672 minibacias.
- Lowland floodplain holds 19.2 % of the area and produces 1.60 % of the erosion.
- CARRIED FORWARD, not fixed: the >3000 m band's 36.9 % of erosion on 6.4 % of area is an
  **input artefact** — bare rock/ash/ice above the treeline carries C = 1.0 (C3.2) — and not a
  terrain gradient. Its per-minibacia *median* (593.4) is below the 500–1500 m band's (820.5),
  which is the signature of a few extreme cells rather than a band-wide effect. The fix belongs
  in `urh_cp_factors.csv` with a written reason, not in the engine.

### Gate (b) — seasonal cycle and the ENSO windows: **PASS in shape**

Monthly climatology of basin-total erosion, Mt/day (bimodal, the Magdalena's two rainy seasons):

| J | F | M | A | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.296 | **0.253** | 0.423 | 0.824 | 1.123 | 0.726 | 0.481 | 0.450 | 0.585 | 1.001 | **1.235** | 0.759 |

Annual totals, Mt: 2009 180.5 · 2010 382.5 · **2011 394.9 (max)** · 2012 234.6 · 2013 257.7 ·
2014 191.9 · **2015 132.3 (min)** · 2016 212.9 · 2017 267.7 · 2018 232.0.

ENSO windows exactly as pre-registered in `docs/34` §1.1. Windows are of unequal length, so
**rates only** are compared and window totals are never divided by each other:

| window | days | mean flux (Mt/day) | window total (Mt, context only) |
|---|---|---|---|
| **P-LN** La Niña 2011-01-01…2011-12-31 | 365 | **1.0818** | 394.9 |
| **P-EN** El Niño 2015-01-01…2016-12-31 | 731 | **0.4722** | 345.2 |
| **S-LN** 2010-07-01…2011-06-30 | 365 | 1.2897 | 470.7 |
| **S-EN** 2015-10-01…2016-04-30 | 213 | 0.3283 | 69.9 |

Wet : dry flux ratio **2.29×** (primary pair) and **3.93×** (sensitivity pair). Both carry the
registered bias of `docs/35` §5.4 unchanged: the dry phase is suppressed harder than the wet one,
so the simulated contrast is overstated by ~+10 %, and the whole level is a **lower bound**.

---

## 4. What remains OPEN, and what would resolve it

The unexplained residual is **1.93 – 14.8×** of gross erosion, depending on which end of the
0.05 – 0.30 SDR band is taken — and **candidate 0 below makes that residual larger, not smaller,
by a further 2.37× – 3.00×**. Five candidates, with what would settle each. None of them may be
absorbed into α (`docs/35` §6 RULE 0).

0. **The LS *formulation* level — the largest term in this list, and it points the WRONG WAY.**
   Listed first because it is the biggest and because it was missing from every numbered document
   until 2026-08-11. Our LS2D differs from the MGB-SED reference LS in three ways, all measured on
   the **same** 90 m grid, i.e. this is a *formulation* difference and not the resolution question
   that decision 4 in §1 resolved:

   | lever | ours | Buarque (2015), the method this project transposes | measured × on basin area-wtd LS |
   |---|---|---|---|
   | slope-length limiter | upslope **area** ≤ 1 km² ⇒ unit contributing length up to 1e6/92 ≈ **10,870 m** ≈ 118 pixels | p. 94: "seu valor máximo foi limitado ao **tamanho do pixel do MDE**" — slope length ≤ **one pixel** | **0.351** (dominant) |
   | `m` | continuous McCool (1989), basin median **0.584** | his eq. 14, step function **hard-capped at 0.5** | 0.502 |
   | `S` | Moore & Burch (1986) `(sinθ/0.0896)^1.3` | his eq. 18, Wischmeier & Smith (1978) `65.41 sin²θ + 4.56 sinθ + 0.065` | 1.714 |
   | **all three together (source-method LS)** | area-wtd mean **39.812** | area-wtd mean **16.775** | **0.421** |

   The three levers interact (0.502 × 1.714 × 0.351 = 0.302 ≠ the joint 0.421), so no single one is
   "the" cause. Using the literal Desmet–Govers finite-difference `L` in place of our continuous
   form lowers the source row a further ×0.790, giving the bracket **×0.333 – ×0.421**, i.e. our LS
   is **2.37× – 3.00×** the level α = 11.8 is paired with. Source and measurement:
   `docs/agents/journal_decide-ls-resolution.md` §1a and §3b (all 30,235,916 basin cells; the
   harness reproduces our own 39.812 bitwise).

   **Two consequences, both unfavourable, both stated in full:**
   - **On the level.** MUSLE is linear in LS, so 248.730 × 0.421 = **104.8 Mt/yr** and × 0.333 =
     **82.8 Mt/yr** — *below* both anchors, implied SDR **1.374 – 2.222**, i.e. back on the
     physically impossible side that §2 claims was left behind. **Caveat on that arithmetic:**
     0.421 is a ratio of **area-weighted** per-cell LS means, whereas the basin total weights LS by
     each cell's `Qsur·q_peak·K·C`, so 104.8 is a **proxy, not a re-run**. It is a defensible proxy
     because the swap has nearly the same effect on the erosive terrain as on the whole basin
     (Andean >1000 m: 27.109/65.199 = 0.416 vs basin 0.421) and erosion is concentrated there
     (§3 gate (a)). The exact figure requires the C3.1 re-run.
   - **On the α guard.** Because MUSLE is linear in LS, a fit on our LS returns an α that is
     1/2.37 – 1/3.00 of what the same observations would return on the source's LS. The like-for-like
     α reference for **our** LS is therefore **≈ 3.9 – 5.0, not 11.8**; the `docs/35` §6.1 expected
     band 5.9 – 23.6 becomes ≈ **2.0 – 9.9** and the hard stop α > 35.4 becomes ≈ **11.8 – 14.9**.
     The **adopted, unfitted α = 11.8 then sits at or above its own corrected hard stop** at the
     3.00× end of the bracket. This tightens the guard; it does not loosen it.

   **RESOLVER:** the pre-registered C3.1 LS-formulation comparison — choose the limiter, the `m`
   cap and the `S` function **on source grounds, in writing, before any basin total is looked at**
   (`docs/35` §9.3). Note also that the source's own verdict on his Andean LS (p. 121) is that even
   his *pixel-capped* L "tende a fazer com que as estimativas da erosão laminar do solo em áreas
   íngremes, como nos Andes, seja **superestimado**", and ours uses a looser limiter than his.

   **DO NOT** stack the upward candidates below (1: C revision ×2–5; 2: `f_peak` ×2.1) on top of an
   LS that is 2.4 – 3.0× too high for its own α, and then read the sum as agreement with the
   anchor. Candidate 0 must be settled *first*, or every upward correction is being applied to an
   inflated base.

1. **The cover factor `C`.** Basin area-weighted C = 0.01082 and its dominant term is
   grassland C = 0.01, Roose's "good condition", carrying 36.8 % of the area-weighted basin C —
   while Roose's own table spans a factor of 10 up to overgrazed/burnt pasture. Basin-mean C is
   very nearly linear in it, so a defensible upward revision could account for a factor of
   ~2–5 on its own, which covers the SDR = 0.30 end of the residual.
   **RESOLVER:** a citable land-condition source for Colombian Andean pasture and cropland, or a
   published C table from a Magdalena–Cauca MUSLE/RUSLE study, applied per URH class with the
   reason written into `urh_cp_factors.csv`. Until then C is a *choice*, and it is at the low end
   of its own range.
2. **The peak deficit already registered in `docs/35` §5.** The `q_peak` proxy plus the missing
   43 % of flood events suppress simulated flood-driven sediment by ~2.1× (bracket 1.4 – 4.8×).
   That bracket alone spans the SDR = 0.30 end of the residual.
   **RESOLVER:** nothing inside C3 — `docs/35` §6.5 permits only an explicit, separately named,
   separately reported `f_peak` with its own derivation, never a fold-in to α. Reporting the
   result as a lower bound is the registered default and needs no justification.
3. **The 0.05 – 0.30 SDR expectation itself is uncited in this repository.** It arrived as a
   brief-level assertion, exactly like the "mountainous LS 2–10" comparison that decision 4
   retired. The Magdalena is an unusually high-yield system, and a large basin SDR near 0.5 is
   not self-evidently absurd for it.
   **RESOLVER:** a citation for basin-scale SDR in humid tropical Andean catchments, or a
   Magdalena-specific sediment-budget paper. **This is a reason C3 is OPEN, not a reason to call
   it closed:** an uncited plausibility band cannot be used to *pass* a gate any more than it
   could be used to fail one, and until it is cited the level remains unvalidated.
4. **Terms known to point the wrong way, listed so they are not proposed later as fixes.**
   P = 1.0 and FG = 1.0 are both upper bounds on erosion (P ≤ 1, FG ≤ 1), so any real value
   *lowers* the model and widens the residual. Driving MUSLE with released rather than generated
   runoff costs a further 1.125×. **The largest wrong-way term is candidate 0 above
   (×0.333 – ×0.421 = 2.37 – 3.00× of residual), not the 1.125× recorded here** — when this list
   was first written it stopped at 1.125× and that understated the wrong-way side by more than a
   factor of two.

---

## 5. What C4 must NOT do while C3 is open

1. **Do not fit α against outlet or station sediment without an explicit channel-deposition
   step.** This is a NEW trap created by the amendment and it is the most important line in this
   document. At the adopted convention, making gross erosion equal the outlet load needs
   **α = 6.83 – 8.73**, which sits comfortably **inside** the `docs/35` §6.1 "expected" band of
   5.9 – 23.6. Before the amendment the same mistake needed α ≈ 2,483 and tripped the hard stop
   immediately. So the §6.1 guard, which has only now become a like-for-like comparison at all,
   **can no longer catch a fit that omits deposition** — it will report `status: ok`. A fitted
   α in the low teens or below, obtained without a routing/deposition step, silently encodes
   SDR = 1.0 and must be treated as a failure regardless of what the guard says.
   **"Like-for-like" here means like-for-like in *units* only** — per §4 candidate 0 the guard is
   not yet level-equivalent, and at the corrected band (expected ≈ 2.0 – 9.9) an SDR = 1.0 fit at
   α = 6.83 – 8.73 still lands inside it. The trap is unchanged in kind and the numbers to quote
   it with depend on C3.1.
2. **Do not treat 248.7 Mt/yr as calibrated.** α and β are unfitted Williams values and the
   number is a lower bound (`docs/35` §5.3).
3. **Do not report any load without its convention.** After this amendment a load is 363×
   ambiguous. `SedParams.convention_summary()` exists so the convention, the K unit system, the
   LS choices and the application unit travel in the same table as the number
   (`docs/35` §6.4 test T3).
4. **Do not change a convention default to move the level.** Every prior convention stays
   reachable by name precisely so that a level change must be argued as an amendment with a date
   and a derivation, in `docs/35` §9.
5. **Do not publish t/km²/yr as a yield.** The specific-erosion figures in §3 are model-internal
   and are labelled as such; gauge-referenced yields stay embargoed (`docs/23` §13.2).

---

## 6. Reproduction

```
python3.10 -m pytest tests/ -q          # 96 passed, 0 failed, 0 skipped (2026-08-11)
```

The basin decade is `sed.simulate_sediment(load_geometry(...), SedParams(), drivers.qsur_mm)`
with the defaults as amended; `SedParams(volume_convention='pixel_km2',
k_unit_system='si_stored')` reproduces the pre-amendment first-run numbers exactly
(0.684406 Mt/yr). The audit's hand-computed unit-day — minibacia 16115 on 2009-04-11,
**1293.5691626849571 t/day** — is pinned as a regression test in `tests/test_sediment.py`
(§3b), on both backends, and re-derived there from literal arithmetic rather than from a
recorded engine output.
