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

---

# AMENDMENT A1 (2026-08-11) — C3 is **OPEN** under the revised closure conjunction

**C3 is OPEN.** Two clauses of the revised conjunction are not met and one is retired.

Written by the `reverdict` agent (`docs/agents/journal_reverdict.md`) after
[`docs/40`](40_sdr_evidence.md) settled the SDR band, [`docs/41`](41_cfactor_evidence.md) put the
cover factor `C` on a citable footing, and [`docs/42`](42_c4_guards.md) registered the C4 guard
set. **Nothing above this line is rewritten.** Everything §1–§6 says still stands as the record of
what was believed on the day it was written; where a statement is now wrong, this amendment says
so and says which document overturned it. Two things above are superseded rather than corrected —
the basin total (248.730 → **299.539 Mt/yr**) and the whole of §3 — and the superseding values are
in A1.3.

**Read this first, because it is the honest summary of what changed:** the previous verdict's
deciding clause — the implied sediment delivery ratio against a 0.05–0.30 band — **rested on an
unvalidated level.** The band was never cited in this repository, and worse, it measures a
different quantity from the ratio §2 computed. §1's fourth row was therefore neither a pass nor a
fail; it was not an evaluable test. C3 does **not** close on that discovery, and it does **not**
stay open on the strength of the retired band. It stays open on a **replacement clause that can be
evaluated and is failed**, and on a **decision that was already unresolved** before any of this.

---

## A1.1 The revised closure conjunction

| # | closure condition | status |
|---|---|---|
| 1 | the factor chain is fully explained by evidence-based corrections | **MET**, unchanged — 0.684 → 248.73 Mt/yr is exactly `1000^0.56 × (1/0.1317) = 363.4245196`. The C revision of A1.3 is a **separate, named input change** (×1.2043), not a further unexplained factor. |
| 2 | no decision left unresolved | **NOT MET**, unchanged and unchanged in cause — the **LS formulation level** (§4 candidate 0) is still explicitly UNRESOLVED. Our LS sits **2.37×–3.00×** above the level α = 11.8 is paired with. **This clause alone forbids closure today, independently of everything else in this amendment.** |
| 3 | the independent audit agreed with the decisions | **MET for the decisions it saw** (the three convention decisions of §1) — **NOT ESTABLISHED for the three decisions taken on 2026-08-11**: the C-revision default change (docs/41), the SDR retirement (docs/40) and the guard registration (docs/42). None has been independently audited. Recorded as an open item, not counted as a met condition. |
| 4 | ~~the implied sediment delivery ratio is physically plausible (0.05 – 0.30)~~ **RETIRED — see `docs/40`** | **the ratio 248.730 Mt/yr ↔ 144–184 Mt/yr is not a sediment delivery ratio** (all-source numerator, hillslope-only denominator) and cannot be tested against a published SDR band in either direction. The band was uncited, its supporting relations use an all-source denominator and were fitted 993× below this scale, and no Magdalena SDR exists in the literature. **A retired gate is neither a pass nor a fail.** (A1.2) |
| 4′ | ~~**the basin-mean gross HILLSLOPE erosion rate is consistent with published erosion and yield levels for humid tropical Andean and comparably mountainous large basins**~~ **RE-OPENED — see A1.9**, superseded by clause 4″ | ~~NOT MET — the model is under-erosive by 1.03 – 2.27× at the adopted C~~ → **NOT ESTABLISHED (A1.9).** The clause's decisive leg compares our MUSLE sum (which SWAT's own Ch. 4:1 defines as a sediment **yield**) against a **RUSLE gross erosion**, i.e. the same quantity error the retired SDR gate died of. Converted like-for-like the sign **inverts** (1.33 – 1.49× *high*); Leg B was already conceded not to be evidence (2.8 %); Leg C's max form is arithmetically invalid at basin scale. **Residual direction UNKNOWN: 2.27× low … 1.49× high.** Still not met — a clause that cannot be evaluated is not a pass. |
| 4″ | **the quantity the MUSLE sum represents is pinned in writing, and the basin-mean rate is consistent with published levels of *that same quantity*** | **NOT ESTABLISHED (A1.9)** — the quantity is not pinned (SWAT says yield; a per-pixel sum over 30 M pixels is not a basin yield either), so no level comparison can be evaluated in a known direction. |
| 5 | the `docs/42` guards are in place for C4 | **MET** — `docs/42` registers **G1–G9** with 17 explicit FAIL conditions, frozen on write 2026-08-11 before any C4 machinery existed, with the measured power of each test recorded before its threshold. Note that G9 obliges C4 to disclose the unobserved fraction with every basin-scale claim, and that A1.3 **moves G9's registered numbers** — see A1.7. |

Clause 4′ is the exact wording proposed in `docs/40` §8.2 and it is adopted verbatim. Clauses 2, 3
and 4′ are each sufficient on their own to keep C3 open. **CLOSED would have required every clause
met with citations, no unresolved decision, and the guards in place; two of five fail and one is
retired.**

> **AMENDMENT A1.9 (2026-08-11, later the same day) — clause 4′ is re-opened as clause 4″.** Written
> after this table, and it changes what keeps C3 open without changing that C3 is open. Clause 4′
> reproduced, on the erosion side, the very error clause 4 was retired for: comparing two different
> quantities. **Clauses 2 and 3 are now the only clauses that fail in a *known* direction, and either
> alone still forbids closure.** Read A1.9 before quoting "1.03 – 2.27× under-erosive" from A1.4.

---

## A1.2 The SDR clause: **RETIRED**, and what that costs the previous verdict

`docs/40`'s verdict is **UNCITABLE**, and the reason is a quantity mismatch rather than a missing
reference:

- **Published SDR has all-source gross erosion in the denominator.** USDA NRCS NEH Part 632 Ch. 6
  (fetched and text-extracted, 18 pp.): *"Gross erosion is the sum of all the water erosion
  occurring in the drainage area. It includes sheet and rill erosion plus channel-type erosion
  (gullies, valley trenches, streambank erosion, etc.)"*. Our denominator is hillslope
  sheet-and-rill only, so our ratio is a different, strictly larger quantity — an **apparent
  delivery ratio (ADR)**.
- **The same watershed can carry all three at once.** NEH Table 6-2: hillslope-only delivery ratio
  **0.33**, true SDR **0.6957**, and the mixed ratio we computed — **1.7778**. Our 0.579–0.740 is
  *below* USDA's own reference ADR and almost exactly equal to its *true* SDR. The direction of the
  alleged failure inverts.
- **§2's premise is false as written.** "So `SDR = outlet / gross` must be < 1" is true of a true
  SDR and false of the ADR: Dunne et al. (1998) measure bank-erosion supply of **1,570 Mt/yr against
  a ~1,200 Mt/yr Óbidos flux — 1.3× the outlet load from channel sources alone.** Replace the
  sentence accordingly; the ratio has no upper bound of 1.
- **Scale and region.** The band's supporting relations (Vanoni 0.0997, Renfro 0.1061,
  USDA-SCS 0.1439 at our area) were fitted on US agricultural watersheds of
  **0.0259 – 259.0 km²** — our basin is **992.7×** the largest — and NEH's own summary says
  *"Using an equation to obtain sediment data outside the physiographic area for which the equation
  was developed is generally not recommended."*
- **No Magdalena SDR exists or can be assembled.** Every published Magdalena "erosion rate" (550,
  690, 710, 1,485, 128–2,200 t km⁻² yr⁻¹) is a sediment **yield** — the numerator. `USLE` and
  `RUSLE` appear **zero times** in the fullest published treatment (Restrepo A. 2015).
- **The area trend's sign does not even survive.** In the one large, data-sparse, mountainous basin
  where SDR was refitted (Tan et al. 2024), **SDR increases with drainage area**; de Vente et al.
  (2007) state the decay holds above 10⁴ km² only *"when drainage density decreases or channel banks
  are stabilized"* — the one condition the Magdalena–Cauca does not meet.

**Consequences, stated plainly.**

1. **The previous verdict rested on an unvalidated level.** §1's fourth row and §2's "why this
   document says OPEN" section judged the model against a number this repository could not cite and
   that does not measure what we computed. The *conclusion* (OPEN) survives, but not for that
   reason. Anyone who quoted "implied SDR 0.579–0.740, above the plausible band" quoted an
   unevaluable test.
2. **§2's requirement table loses two rows.** The SDR = 0.15 and SDR = 0.05 rows demanded
   960 – 1,227 and 2,880 – 3,680 Mt/yr of gross erosion and tripped the `docs/35` §6.1 hard stop.
   They rest entirely on the retired band and on the ADR/SDR conflation, and they **overstated the
   problem by 4 – 8×**. **Struck.**
3. **§4 residual 3 is RESOLVED AND RETIRED** (see A1.5).
4. **§5.1's trap is unchanged in kind and gets worse in degree.** With the Depresión Momposina's
   20–45 % retention (36–80 Mt/yr, labelled *preliminar* by its own author) added back, the flux
   entering the channel network above the sink is 180 – 264 Mt/yr, so the hillslope-to-channel ratio
   at the prior C was already **0.72 – 1.06** — within ~40 % of encoding zero hillslope deposition
   *before* any fitting. At the adopted C it is **0.60 – 0.88**. The `docs/35` §6.1 α band cannot
   see this; `docs/42` G5 is what now catches it.

**What the retirement does not license.** It does not close C3; it does not authorise moving α or
any convention to close a gap (`docs/35` §6 RULE 0); and per this project's standing rule — *an
uncited plausibility band may not be used to pass **or** fail a gate* — the band is retired in
**both** directions.

---

## A1.3 The C-factor revision is citable, so it is applied — as a named option, and re-run

`docs/41` is **CITABLE**: all 8 rows of `data/processed/urh_cp_factors.csv` now carry a source, a
stated land condition and a low/central/high range, with the Colombian anchor inside this basin
(Rengifo-Rengifo et al. 2022, seven Cauca municipalities) and the only field-measured
tropical-highland cattle-pasture C values found (Lianes et al. 2009). The largest available upward
lever — a published Colombian C = 0.6 for *pastos enmalezados* — was **rejected on physics, in
writing, before its effect was computed**. So the revision is adopted.

### A1.3.1 How it is applied

`src/mgb_sediment.py` now carries **`load_geometry(cp_revision=...)`** — the same named-option
pattern as `volume_convention` / `k_unit_system` / `ls2d_*`, so a level change is reversible by name
and cannot be a silent edit:

| `cp_revision` | reads columns | basin total | status |
|---|---|---|---|
| **`cited_central_2026_08_11`** (DEFAULT) | `C`, `P` | **299.5387 Mt/yr** | adopted (`docs/41`) |
| `prior_2026_08_11` | `value_prior_2026_08_11`, `P_prior_2026_08_11` | **248.7298 Mt/yr** | reproduces §2–§3 of this document as first published |
| `cited_low_2026_08_11` | `C_low`, `P_central` | 107.3201 Mt/yr | DIAGNOSTIC — **refuted by mass balance** (ADR 1.34 – 1.71 > 1) |
| `cited_high_2026_08_11` | `C_high`, `P_central` | 1,896.2641 Mt/yr | DIAGNOSTIC — not adopted; picking a C to hit a residual is the failure mode `docs/35` §6 RULE 0 forbids for α |
| `pacheco_practice_2026_08_11` | `C`, `P_low` | — | DIAGNOSTIC — the land-use-keyed P is **rejected as a category error**; it costs ×0.542, i.e. any P < 1 widens the residual |

The chosen name and both column names are recorded in `SedGeometry.audit` (`cp_revision`,
`cp_c_column`, `cp_p_column`, plus the resolved `class_c` / `class_p`), so a load cannot be quoted
without its C provenance — the same discipline §5.3 imposes on the unit conventions. A drift guard
warns if the loader-facing `C` column stops equalling `C_central` while the default name is in use.
**The default reads exactly the columns the pre-edit loader hardcoded, so the option changes no
behaviour by itself** — verified per land class against a raw read of the CSV.

### A1.3.2 The basin decade, re-run

Frozen H2E hydrology (`h2e_drivers.npz:qsur_rel_mm`, read-only), 3,652 days × 8,672 minibacias,
32,782 URH cells, α = 11.8 and β = 0.56 **unfitted**.

| quantity | prior C | **adopted C** |
|---|---|---|
| basin total, gross hillslope erosion | 248.7298 Mt/yr | **299.5387 Mt/yr** |
| over the record | 2,486.957417 Mt / 3,652 d | **2,994.977042 Mt / 3,652 d** |
| area-weighted basin-mean C | 0.010823 | **0.013083** |
| mass ledger `eroded − delivered − Δstore` | exactly 0.0, `exact = True` | **exactly 0.0, `exact = True`** |
| measured adopted/prior ratio | — | **1.2042736** (`docs/41` predicted ×1.2043 from a linear decomposition — confirmed by simulation, not assumed) |

**This revision is NOT a pure level shift, and that is why both pattern gates had to be re-run.**
Unlike the two unit conventions — whose adopted/legacy ratio was constant to 12 significant figures
across every minibacia and every day — the per-minibacia adopted/prior ratio spans **0.500 – 5.000**
(median 1.577) and the per-**day** basin ratio spans **0.7258 – 1.4889**, because Bare moves down
(×0.5) while Forest moves up (×1.667). The spatial and land-class attribution genuinely changes.

Land-class attribution of gross erosion (**attribution, not yield**): Forest **36.48 % → 50.49 %**,
Grassland 27.33 % → 34.04 %, **Bare 35.60 % → 14.78 %**, Cropland 0.47 % → 0.39 %, Urban 0.06 % →
0.15 %, Shrub 0.06 % → 0.14 %, Wetland 0.0015 % → 0.006 %, Water exactly 0 in both.

### A1.3.3 Gate (a) — Andean flanks ≫ lowland floodplain: **PASS, and stronger, 18.67×**

Same terrain classifier as §3, reproduced rather than approximated: mean elevation per minibacia
from the corrected COP90 DEM block-averaged 8× onto `minibacias.tif`, 8,672/8,672 covered,
elevation p0/p5/p50/p95/p100 = 6.2 / 27.2 / 898.6 / 3,090.7 / 4,491.1 m — identical to §3, so the
band memberships (1,736 / 1,691 / 2,442 / 2,286 / 517) are identical too and only the erosion moves.
Elevation is never a MUSLE input, so the gate is not circular.

All specific-erosion figures are **MODEL-INTERNAL specific erosion in t/km²/yr** — the model's own
erosion over the model's own minibacia area. They are **not** gauge-referenced sediment yields,
which remain embargoed (`docs/23` §13.2).

| band (mean elevation) | n | area % | erosion % (prior → **adopted**) | spec. area-wtd (prior → **adopted**) | spec. median (prior → **adopted**) |
|---|---|---|---|---|---|
| Lowland floodplain <100 m | 1,736 | 19.2 | 1.60 → **1.28** | 80.2 → **77.4** | 11.4 → **17.4** |
| Piedmont 100–500 m | 1,691 | 19.3 | 8.46 → **10.86** | 424.6 → **656.5** | 169.6 → **263.1** |
| Lower Andean 500–1500 m | 2,442 | 28.1 | 29.96 → **39.31** | 1,033.2 → **1,632.4** | 820.5 → **1,309.6** |
| Upper Andean 1500–3000 m | 2,286 | 27.0 | 23.10 → **29.02** | 826.9 → **1,251.1** | 504.9 → **799.8** |
| High Andes >3000 m | 517 | 6.4 | **36.89 → 19.54** | 5,561.7 → **3,547.2** | 593.4 → **893.9** |

- **Andean flanks (500–3000 m) 1,445.32 vs lowland floodplain (<100 m) 77.41 = 18.67×** (was 11.61×).
- Spearman(specific erosion, mean elevation) = **+0.5518** over 8,672 minibacias (was +0.5544).
- Lowland floodplain holds 19.2 % of the area and produces **1.28 %** of the erosion.
- **§3's carried-forward input artefact is now half-fixed, in the file §3 said the fix belonged in.**
  The >3000 m band's share of erosion falls from 36.89 % to **19.54 %** because Bare C went
  1.00 → 0.50 with a written reason and cited endpoints (`docs/41` §4). It is not *gone*: 19.54 % of
  erosion on 6.4 % of area, and the band's per-minibacia *median* (893.9) is still below the
  500–1500 m band's (1,309.6), which is still the signature of a few extreme cells rather than a
  band-wide effect. Bare's central 0.50 is an explicit **interpolation** (√(0.25 × 1.00)) between
  cited endpoints, not a table value.

### A1.3.4 Gate (b) — seasonal cycle and the ENSO windows: **PASS in shape**

Monthly climatology of basin-total erosion, Mt/day (bimodal, the Magdalena's two rainy seasons):

| J | F | M | A | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.367 | **0.293** | 0.513 | 1.011 | 1.332 | 0.879 | 0.589 | 0.561 | 0.710 | 1.151 | **1.477** | 0.935 |

Annual totals, Mt: 2009 225.8 · 2010 457.1 · **2011 476.5 (max)** · 2012 279.8 · 2013 287.1 ·
2014 238.6 · **2015 167.3 (min)** · 2016 249.1 · 2017 322.0 · 2018 291.9.

ENSO windows exactly as pre-registered in `docs/34` §1.1. Windows are of unequal length, so
**rates only** are compared and window totals are never divided by each other:

| window | days | mean flux (Mt/day) | window total (Mt, context only) |
|---|---|---|---|
| **P-LN** La Niña 2011-01-01…2011-12-31 | 365 | **1.3054** | 476.5 |
| **P-EN** El Niño 2015-01-01…2016-12-31 | 731 | **0.5696** | 416.4 |
| **S-LN** 2010-07-01…2011-06-30 | 365 | 1.5513 | 566.2 |
| **S-EN** 2015-10-01…2016-04-30 | 213 | 0.3905 | 83.2 |

**Simulated wet : dry flux ratio 2.2915× (primary pair) and 3.9725× (sensitivity pair)**, against
`docs/34`'s **observed 2.8 – 4.6× (primary) and 6.4 – 9.3× (sensitivity)**. So the simulated
contrast is **below the observed range at both window definitions** — short by 1.22 – 2.01× on the
primary pair and 1.61 – 2.34× on the sensitivity pair — and the gap **widens** once `docs/35` §5.4's
registered +10 % over-statement is removed (corrected 2.09× and 3.62×). The sign is right, the order
of magnitude is right, and the magnitude is short, in the same direction as everything in A1.4.
Nothing more is claimed here: this is a report, not C5.

> **Correction to `docs/41` §8.3 claim 3, which said the ENSO contrast is "unchanged" because
> "every scenario rescales all windows identically".** Measured here: the primary ratio moves
> 2.2908 → 2.2915 (**+0.03 %**) and the sensitivity ratio 3.9281 → 3.9725 (**+1.13 %**). The claim
> is right in substance and wrong in mechanism — a *row-wise* C revision is not a uniform multiplier
> on the erosion field, because the land-class mix of erosion varies through the season and between
> years (per-day ratio 0.7258 – 1.4889). Only a single uniform C multiplier would leave the ratios
> exactly invariant. The effect is far below any threshold that matters, and it is recorded because
> "identically" is the kind of claim that later gets relied on.

---

## A1.4 Clause 4′ evaluated: **NOT MET**, and the residual is now 1.03 – 2.27×

> **SUPERSEDED IN PART BY A1.9 (same day, later).** Every number in this section is arithmetically
> correct and is reproduced unchanged in A1.9. What A1.9 withdraws is the *interpretation*: Leg A is
> not like-for-like (yield vs gross erosion), Leg C's max form is invalid at basin scale, and Leg B is
> conceded below to be no longer evidence — so **"the residual is 1.03 – 2.27×" must not be quoted as
> a directed result.** The residual's direction is UNKNOWN. This section stands as the record of what
> was concluded before the quantity question was asked.

`docs/40` §8.2's replacement clause tests the **gross hillslope erosion RATE** against published
erosion and yield levels. At the adopted C the basin-mean gross hillslope erosion is
**1,165.08 t km⁻² yr⁻¹ = 11.6508 t ha⁻¹ yr⁻¹** (model-internal; 299.5387 Mt/yr over 257,097 km²).

> **`docs/42` G9 disclosure, required in the same paragraph as any basin-scale claim:** at the
> adopted C, **66.53 % of the model's gross erosion — 199.29 of 299.54 Mt/yr — is upstream of no
> usable SSC station**; only **33.47 %** is; and **801.1 km of channel, including the whole
> Depresión Momposina, lies below the outlet-most SSC station** (`21237020` ARRANCAPLUMAS), against
> a basin maximum path of 1,425.9 km. No station fit can close this clause.

| leg | source | prior C | **adopted C** |
|---|---|---|---|
| **A** — like-for-like denominator: our hillslope rate vs a published mountainous-basin **RUSLE hillslope** rate of 23.7 – 26.5 t ha⁻¹ a⁻¹ | Tan, Liu & Lu (2024), *ESPL* 49:1778–1795 | 9.675 t/ha/yr ⇒ **2.450 – 2.739×** low | 11.6508 t/ha/yr ⇒ **2.034 – 2.275× low** |
| **B** — hard inequality: our Andean-flank model-internal specific erosion vs the Colombian Andes measured mean **yield** 1,485 t km⁻² y⁻¹ (yield ≤ gross erosion wherever net deposition is ≥ 0) | Latrubesse & Restrepo (2014), 119 Andean gauges | 931.95 ⇒ **≥ 1.593×** low | 1,445.32 ⇒ **1.028× low** |
| **C** — our basin-mean gross erosion vs in-basin measured yields: 32-sub-basin mean ~690, maximum 2,200 t km⁻² yr⁻¹ | Restrepo et al. (2006), *J. Hydrol.* 316:213–232 | 1.402× the mean, 0.440× the max ⇒ **up to 2.274×** | **1.689×** the mean, **0.530×** the max ⇒ **up to 1.888×** |
| **combined** | | **1.59 – 2.74×** | **1.03 – 2.27×** |

**Verdict: NOT MET.** The clause asks for consistency, and Leg A — the only leg whose denominator is
like-for-like — still reports the model **2.03 – 2.27× under-erosive**. Two honest qualifications
that cut in opposite directions, both recorded:

- **Leg B has stopped being a proof.** At the prior C it was a *proof by impossibility*: modelled
  Andean gross erosion sat 1.593× **below** a published Andean *yield*, implying a local delivery
  ratio > 1. At the adopted C the gap is **2.8 %** (1.028×), which is inside the noise of a
  comparison `docs/40` itself labelled an order-of-magnitude statement (the spatial supports differ:
  our 500–3,000 m elevation bands against a 119-station Andean compilation). The inequality is still
  formally violated; it is no longer *evidence*.
- **Leg C moved the wrong way on one of its two forms, and that is not a defect.** Our basin-mean
  gross erosion is now **1.689×** the 32-sub-basin mean measured yield (was 1.402×) — a *rise* is
  what should happen, since gross erosion must exceed yield. Read as a bound the finding is the
  same: a basin-mean gross erosion of 1,165 t km⁻² yr⁻¹ is still only **0.53×** the maximum measured
  in-basin yield of 2,200, and a gross-erosion field that cannot reach its own basin's measured
  yields is under-erosive.

**Closing the remaining Leg A gap with α is forbidden and would be visible.** It needs
α ≈ **24.0 – 26.8**, i.e. outside the `docs/35` §6.1 expected band (5.9 – 23.6) at both ends though
inside the hard stop of 35.4 — and `docs/35` §6 RULE 0 forbids it regardless.

**The C revision accounts for roughly a quarter of the residual in log terms, and no more.**
`docs/37` §4 candidate 1 estimated 2–5× for `C` on its own; the *evidence*, once conditioned and
ranged, supports **×1.2043**, because the largest single revision in the table (Bare 1.00 → 0.50,
×0.822) **lowers** the model. That is the measurement candidate 1 asked for, and it did not deliver
what candidate 1 hoped for.

**And candidate 0 still points the other way, harder than the C revision points this way.** At the
adopted C, applying the measured LS bracket (×0.333 – ×0.421, §4 candidate 0) gives
**99.8 – 126.1 Mt/yr** — still *below* both outlet anchors, ADR **1.14 – 1.84**, and Leg A worsens
to **4.8 – 6.8×**. The C revision does **not** rescue the LS question, and the two must not be
netted against each other: candidate 0 is a formulation error to be resolved on source grounds, not
a factor to be cancelled by another factor.

---

## A1.5 What remains OPEN, and what would resolve it

§4's five candidates, restated with their status after `docs/40`–`docs/42`. The unexplained residual
is now **1.03 – 2.27×** on the **erosion side** (not 1.93 – 14.8× of an SDR), and candidate 0 still
makes it larger by a further 2.37 – 3.00×. None may be absorbed into α (`docs/35` §6 RULE 0).

0. **The LS *formulation* level — STILL OPEN, still the largest term, still pointing the wrong way.**
   Unchanged by everything in this amendment: ×0.333 – ×0.421 on the level, and the like-for-like α
   reference for *our* LS is ≈ 3.9 – 5.0 rather than 11.8. **RESOLVER: unchanged** — the
   pre-registered C3.1 LS-formulation comparison (`docs/35` §9.3), decided on source grounds, in
   writing, before any basin total is looked at. **This is now the single highest-value open item in
   Phase C**, a position `docs/40` §8.3 assigned to the C factor before the C factor was measured and
   found to be worth only ×1.20.
1. **The cover factor `C` — CLOSED as a residual** (`docs/41`). All 8 rows are cited, conditioned and
   ranged; P stays 1.0 on AH-537 definitional grounds plus a quantified check that adopted
   conservation practice covers ~0.02–0.24 % of Colombian pasture. Two things this does **not** do:
   it does not close the *level* question, because the C level is confounded with α and no
   calibration can separate them (`docs/42` §3.1); and Bare's central value remains an explicit
   interpolation between cited endpoints (`docs/41` residual E).
2. **The peak deficit — STILL OPEN, unchanged.** `docs/35` §5's ~2.1× suppression (bracket
   1.4 – 4.8×) still spans the whole of the remaining residual on its own. **RESOLVER: nothing inside
   C3** — only an explicit, separately named, separately reported `f_peak` with its own derivation
   (`docs/35` §6.5), never a fold-in to α. Reporting the result as a lower bound remains the
   registered default. Note `docs/42` §8.1: `f_peak` is itself a scalar and therefore joins Π, so it
   may be *reported* as a factor but can never be *fitted* separately from α.
3. ~~The 0.05 – 0.30 SDR expectation itself is uncited in this repository.~~ **RESOLVED AND RETIRED
   (`docs/40`).** The tested quantity is an *apparent* delivery ratio (all-source outlet load ÷
   hillslope-only gross erosion), not an SDR, and the same mixed ratio is **1.7778** in USDA NEH
   Ch. 6's own reference example (true SDR 0.6957, hillslope-only ratio 0.33). No Magdalena SDR
   exists, because every published Magdalena "erosion rate" is a sediment *yield*. §2's SDR = 0.15
   and SDR = 0.05 requirement rows are **struck**. The residual survives, relocated to the erosion
   side and 4 – 8× smaller.
4. **Terms known to point the wrong way — unchanged, and one is now quantified.** P = 1.0 and
   FG = 1.0 are upper bounds on erosion (P ≤ 1, FG ≤ 1), so any real value *lowers* the model and
   widens the residual: `docs/41` §5 measures the only citable sub-1 P scheme at **×0.542** and
   rejects it as a category error rather than adopting the flattering direction. Driving MUSLE with
   released rather than generated runoff costs a further 1.125×. The largest wrong-way term is still
   candidate 0.
5. **NEW — the 2026-08-11 decisions are unaudited** (clause 3). The C-revision default change, the
   SDR retirement and the guard registration have had no independent review.
   **RESOLVER:** an adversarial pass over `docs/40`, `docs/41`, `docs/42` and this amendment, in the
   style of `docs/agents/review_2026-08-10_docs31.md`.
6. **NEW — the C4 station-side evidence does not exist yet.** `docs/42` G3.1 would give this project
   its **first independent evidence about the Bare class** (erosion share 0.0 – 75.6 % across the
   13 calibration stations — the largest identifiable contrast in the set), and G1.2 its first
   measured bound on channel deposition. Both are *pending C4*, and C4 may run while C3 is open
   (A1.6).

**What would close C3.** Clause 2 needs the C3.1 LS-formulation decision. Clause 4′ needs either an
LS/erosion resolution that raises the gross-erosion rate, **on evidence**, into the neighbourhood of
Leg A's 609 – 681 Mt/yr, or a documented argument — with citations — that a large tropical Andean
basin's hillslope sheet-and-rill rate legitimately sits ~2× below Tan et al.'s. Clause 3 needs an
audit. **Note that clauses 2 and 4′ are the same lever pointing in opposite directions**: the LS
correction lowers the model by 2.4 – 3.0× while clause 4′ asks for 1.03 – 2.27× more. Resolving
candidate 0 in the direction its own source argues for would take the model *further* from clause 4′,
and that must be reported rather than quietly averaged away.

---

## A1.6 What C4 may now do, and what it still may not

C3 is **OPEN**, so §5's five prohibitions all stand. What has changed is that C4 is no longer
blocked: `docs/42` supplies the test §5.1 could only warn about.

**C4 MAY now start** — and only when held to `docs/42` G1–G9, never on `docs/35` §6 alone.
Specifically it may: fit α and β on the 13-station calibration set; score the 5 evaluation stations
without ever fitting them; run and report G1–G9 whichever way each comes out; add an **explicit,
named** transport sink and report the pre- and post-sink fits side by side with `k̂` for both; and
revise a *class-specific* C in `urh_cp_factors.csv` — with the reason and the source in that row's
own columns — if G3.1 fires.

**C4 STILL MAY NOT:**

1. **Adopt a fit without `docs/42` G5's precondition.** A fitted α anywhere in 5.9 – 23.6 obtained
   without (1) a named non-trivial transport sink **or** the words *"this model asserts SDR = 1.0
   between hillslope and station"* stated as a claim, **and** (2) G1.2's `k̂` with its interval in the
   same table as α, is an **automatic FAIL regardless of what `check_musle_parameters` returns.** At
   the adopted convention a deposition-free fit lands α at 6.83 – 8.73, comfortably inside the old
   "expected" band; and at the adopted C the hillslope-to-channel ratio is already 0.60 – 0.88, so
   the model is within ~40 % of encoding zero hillslope deposition before any fitting.
2. **Claim that any of α, the C level, the LS level, the K unit system, the volume convention, P or
   FG is validated.** They are seven ways of writing one identifiable product Π (`docs/42` §3.1;
   design-matrix condition number measured as **inf**, exactly singular). Π = 4,288.408 at the prior
   C becomes **5,164.42** under the adopted C — using the **erosion-weighted** factor 1.20427, not
   the area-weighted 1.20881, because the erosion-weighted one is what a fit sees. C4 must report Π
   with its full decomposition, the **equifinal family**, and a per-factor evidence grade.
3. **Print a stale evidence grade.** The grades move with `docs/41`: `C` for Forest, Shrub,
   Grassland, Cropland, Urban and Wetland → **CITED (conditioned and ranged)**; `C` for **Bare** →
   **CITED ENDPOINTS, INTERPOLATED CENTRAL** (0.50 = √(0.25 × 1.00)), which satisfies `docs/42`
   G3.3(2)'s "explicit reclassification with a written reason" but is still not a table value; the
   **LS level → UNVALIDATED**, unchanged and unchangeable by any fit; P and FG → **ASSUMED,
   one-sided**; `volume_factor` → **DERIVED**; `k_factor` → **IDENTIFIED**. `docs/42` G3.3's blanket
   requirement to stamp the C *level* UNVALIDATED is superseded by `docs/41` **only** to the extent
   of the citation: **cited is not validated**, and the level is still Π.
4. **Fit or validate the C of Shrub, Cropland, Urban, Water or Wetland** — ≤ 3.1 % of erosion at
   every station (`docs/42` G3.2). Any table listing them carries the word ASSUMED, or now CITED, but
   never *validated*.
5. **Present a passing guard set as closure of C3.** `docs/42` G9: 66.53 % of the model's gross
   erosion (199.29 of 299.54 Mt/yr) is upstream of no usable SSC station, and 801.1 km of channel
   including the whole Momposina lies below the outlet-most one. The guards constrain the model over
   **33.47 %** of its own erosion.
6. **Treat 299.5387 Mt/yr as calibrated, or quote it without its convention *and* its C revision.**
   α and β are unfitted Williams values and the number remains a **lower bound** (`docs/35` §5.3).
   `SedParams.convention_summary()` **plus** `SedGeometry.audit['cp_revision']` must travel in the
   same table as any load — after this amendment a load is 363× ambiguous in convention **and** 1.2×
   (at the band endpoints 0.43× – 7.62×) ambiguous in C.
7. **Publish t/km²/yr as a yield.** Every specific-erosion figure in A1.3.3 and A1.4 is
   **model-internal**; gauge-referenced yields stay embargoed (`docs/23` §13.2).
8. **Change a convention or a `cp_revision` default to move the level.** Every prior value stays
   reachable by name precisely so that a level change must be argued as a dated amendment with a
   derivation.

---

## A1.7 Corrections and consequential edits this amendment requires elsewhere

Recorded rather than silently applied, because several touch committed numbers and two are in files
this pass was not scoped to edit.

1. **`docs/42` §4.5 and G9's registered numbers move with the C revision** and need an amendment in
   that document's own §9 (it is a frozen pre-registration; §9 is its amendment slot). Measured here,
   with the upstream walk validated by reproducing the prior-C figures exactly: observed
   **3,282 / 8,672** minibacias and **98,987.61 km² (38.50 %)** are unchanged — they are geometry —
   but the erosion split moves from **36.10 % / 63.90 %** (89.78 / 158.95 Mt/yr) to
   **33.47 % / 66.53 % (100.25 / 199.29 Mt/yr)**. The registered *fact* is unchanged and in fact
   sharper: the majority of the model's erosion is unobservable. The `Lw`, power, exponent and
   composition-leverage numbers of §4.1–§4.4 are not affected in kind, but the per-station land-class
   **erosion shares** in §4.1/§4.4 were computed at the prior C and will shift (Bare's share halves
   basin-wide), so G3.1's leverage table should be recomputed before G3.1 is run.
2. **`tests/test_sediment.py` has two stale hard-coded C assertions and the suite is 94 passed /
   2 failed.** Both are the one-line provenance updates enumerated in `docs/41` §8.1, both are caused
   by the CSV rewrite rather than by any code change here, and `tests/` is not a file this pass was
   scoped to touch: line 310 `0.003` → `0.005` with `UNIT_DAY_LOAD_T` 1293.5691626849571 →
   **2155.9486044749287** for the *file-based* join guard only, and lines 683–684's value set →
   `{0.0, 0.005, 0.015, 0.03, 0.2, 0.5}`. The **synthetic** §3b regression that passes
   `class_c={1: 0.003}` explicitly **must be left alone** — it is convention arithmetic, not a
   statement about the CSV. Either test can alternatively be pinned by passing
   `cp_revision='prior_2026_08_11'`, which is now the honest way to assert the old numbers.
3. **`docs/41` §8.3 claim 3 is corrected in A1.3.4** (the ENSO ratios move by +0.03 % and +1.13 %,
   not by exactly zero).
4. **The 248.730 Mt/yr headline is superseded by 299.539 Mt/yr** wherever it is quoted — `docs/35`,
   `docs/36`, this document's §2–§4, `docs/40` §1 and §7, `docs/42` §4, **`src/mgb_sediment.py`'s
   module docstring (its UNITS convention table)**, `docs/PROGRESS.md`,
   `progress_map.html` and any figure or deck built from them. `docs/40`'s three legs are
   re-evaluated at the new level in A1.4; its §1 table and §11 reproduction block are correct for the
   prior C and should be read as such.
   **ADDED 2026-08-11 (A1.9's pass), because this list omitted the one file C4 will actually read.**
   `src/mgb_sediment.py` was missing from the enumeration above, and its docstring carried **three**
   stale claims past the amendment: a convention table whose "DEFAULT" row printed **248.72 Mt/yr**
   (the default now also carries `cp_revision='cited_central_2026_08_11'`, so the true default output
   is **299.539 Mt/yr** — the docstring understated its own default by 20.4 %); the **retired**
   0.05 – 0.3 SDR band presented as *"the published range"*, which A1.2 struck and which this
   project's standing rule forbids using in either direction; and *"C3 is OPEN for exactly this
   reason"*, which is false — C3 is open on clauses 2, 3 and (as NOT ESTABLISHED) 4″. All three are
   **fixed in that file** by the same pass that wrote A1.9; the omission is recorded here rather than
   silently repaired. The engine docstring is what C4 reads and what outlives this amendment, so a
   retired gate left standing there is the version that propagates.
5. **§2's "So `SDR = outlet / gross` must be < 1" is false for the quantity computed** (A1.2), and
   §2's SDR = 0.15 / 0.05 requirement rows are **struck**.
6. **`docs/00_INDEX.md`'s where-is-it table** gains rows for 40, 41, 42 and this amendment — done by
   this pass.
7. **ADDED by A1.9 — `notebooks/18_musle_construction.ipynb` §6.4 and §7 still present clause 4′ as a
   like-for-like, directed result, and they are generated.** The claim appears in
   `src/nbgen/make_nb18.py` at **line 2366–2368** (*"Leg A — the only like-for-like denominator …
   Hillslope against hillslope, so this is the leg that counts"*), in the **printed strings of the
   §6.4 code cell** at lines **2397, 2417, 2430, 2449** (*"THE leg that counts"*, *"under-erosive"*,
   *"closing Leg A with alpha would need alpha ="*), and in the narrative at lines **2512–2517** and
   **2980**. Its §1 (line ~ the "class column" cell) already states the opposite — that MUSLE's output
   is *"closer to 'sediment delivered from this patch to its stream' than to 'soil detached on this
   patch'"* — so the notebook contradicts itself, which is how A1.9 was found.
   **NOT FIXED by A1.9's pass, deliberately:** the wrong text is partly inside *executed* cells, so a
   correct fix is a generator edit **plus** a full nb18 re-execution, and neither the notebook nor its
   generator is a file the finding that prompted A1.9 scoped for editing. Recorded here so the next
   pass can do it in one go, with the qualification text taken from A1.9.2–A1.9.3: the legs must be
   printed under **both** readings and the summary line must say **direction unknown**, not
   *"under-erosive"*.

---

## A1.8 Reproduction

```
python3.10 -m pytest tests/ -q          # 94 passed, 2 failed (A1.7 item 2), 2026-08-11
```

The basin decade is
`sed.simulate_sediment(sed.load_geometry(mini_ids=..., cp_revision=...), sed.SedParams(), qsur_rel_mm)`.
`cp_revision='cited_central_2026_08_11'` (the default) gives **2,994.977042 Mt over 3,652 d =
299.5387 Mt/yr**; `cp_revision='prior_2026_08_11'` gives **2,486.957417 Mt = 248.7298 Mt/yr**, i.e.
§2–§3 of this document reproduce exactly, and the ledger is `residual_t == 0.0`, `exact = True` in
both. Gate (a) uses the same classifier as §3 — the corrected COP90 DEM (0.000833°, 5,640 × 12,000,
identical bounds to `minibacias.tif`) block-averaged 8× — which reproduces §3's elevation percentiles
and band counts, so the gate was validated against the published numbers before being used on new
ones. Every number in A1.3–A1.4 comes from two scratchpad scripts that read
`sim_calibrated_v2/h2e_drivers.npz`, `model_inputs_v2/topology.npz`, `_c1_geom.csv` and the four
`urh_*` / `minibacia_*` CSVs **read-only** and wrote nothing into the repository. No calibration was
launched. No frozen artifact was modified. Nothing is backdated.

---

# AMENDMENT A1.9 (2026-08-11, after A1) — **which quantity is the MUSLE sum?** Clause 4′ is re-opened as 4″: **NOT ESTABLISHED**

Written by `docs/agents/journal_fixer.md` run 3. **Nothing above this line is rewritten**; A1.4 keeps
its numbers and gains a pointer. **The verdict does not move: C3 was OPEN and stays OPEN.** What
moves is *why*: the replacement clause A1.1 adopted verbatim from `docs/40` §8.2 reproduced, on the
erosion side, the exact error the retired SDR gate died of — **it compares two different
quantities** — so the residual's *direction* is no longer a measured result. Clauses 2 (LS
formulation level, UNRESOLVED) and 3 (the 2026-08-11 decisions unaudited) are now the only clauses
failing in a known direction, and each alone still forbids closure.

## A1.9.1 The evidence: the reference implementation calls this equation's output a **yield**

**SWAT Theoretical Documentation, Version 2009** (Neitsch, Arnold, Kiniry & Williams; TR-406, 2011),
Section 4 Chapter 1 *"Equations: Sediment"*, printed **p. 252** — the reference implementation of the
same MUSLE with the same α = 11.8, β = 0.56 and `CFRG`, and the text from which Buarque (2015) and
Fagundes (2018) transcribe their unit strings (`docs/agents/journal_decide-units.md` §1d). PDF
fetched and text-extracted for this amendment (7,690,470 B, 647 pp). **Verbatim:**

> "USLE predicts average annual **gross erosion** as a function of rainfall energy. In MUSLE, the
> rainfall energy factor is replaced with a runoff factor. This improves the **sediment yield**
> prediction, **eliminates the need for delivery ratios**, and allows the equation to be applied to
> individual storm events. … Delivery ratios (the sediment yield at any point along the channel
> divided by the source erosion above that point) are required by the USLE because the rainfall
> factor represents energy used in **detachment only**. **Delivery ratios are not needed with MUSLE
> because the runoff factor represents energy used in detaching *and transporting* sediment.**"

and, defining eq. 4:1.1.1's left-hand side on the same page:

> "where **`sed` is the sediment yield on a given day** (metric tons)"

Full citation and retrieval record: `docs/40` §9 **C18** (independently reconfirmed for the
`sed` definition against the SWAT+ theoretical documentation, which does not carry the delivery-ratio
passage).

**This project already knew.** `notebooks/18_musle_construction.ipynb` §1: *"Because runoff already
encodes how much water was available to carry the soil away, MUSLE's output is closer to 'sediment
delivered from this patch to its stream' than to 'soil detached on this patch'. Section 6 shows this
distinction is not pedantic — a whole closure gate was retired over it."* The same notebook's §6.4
then writes: *"Leg A — the only like-for-like denominator. Tan, Liu & Lu (2024) report **RUSLE**
hillslope erosion of 23.7–26.5 t/ha/a … Hillslope against hillslope, so this is the leg that
counts."* RUSLE is USLE's descendant and therefore a **detachment**-side quantity. The two sentences
are in the same notebook, three sections apart.

## A1.9.2 The three legs, re-derived under both readings, at the adopted `C`

Basin total 299.5387 Mt/yr over 257,097 km² = **1,165.0805 t km⁻² yr⁻¹ = 11.6508 t ha⁻¹ yr⁻¹**
(model-internal specific erosion; `docs/23` §13.2's gauge-referenced-yield embargo unaffected).

*`docs/42` G9 disclosure, required in the same paragraph: **66.53 %** of the model's gross erosion —
199.29 of 299.54 Mt/yr — is upstream of no usable SSC station, and 801.1 km of channel including the
whole Depresión Momposina lies below the outlet-most one (`21237020` ARRANCAPLUMAS).*

| leg | reading A — **our sum is gross erosion** (as A1.4 assumed) | reading B — **our sum is a hillslope→stream yield** (SWAT Ch. 4:1) |
|---|---|---|
| **A** vs Tan, Liu & Lu (2024) RUSLE 23.7 – 26.5 t ha⁻¹ a⁻¹ | erosion vs erosion: ours 11.6508 ⇒ **2.034 – 2.275× LOW** | their erosion → yield with NEH Table 6-2's own sheet-erosion DR **0.33** (300,000/900,000) = **7.821 – 8.745 t ha⁻¹ a⁻¹**; ours 11.6508 ⇒ **1.332 – 1.490× HIGH** (with DR = ⅓ exactly: 1.319 – 1.475×). **Conversion-free cross-check:** Tan et al.'s own specific sediment **yield** is 1.3 – 16.9 t ha⁻¹ a⁻¹ and ours sits **inside** it |
| **B** vs Latrubesse & Restrepo (2014) Colombian Andes mean **yield** 1,485 t km⁻² y⁻¹ | Andean-flank 1,445.32 ⇒ 1.027× low — **A1.4 already concedes this "has stopped being a proof … it is no longer evidence"** (2.8 %, differing spatial supports) | identical arithmetic, same concession: a hillslope yield must still exceed a downstream gauge yield, and 2.8 % is inside the comparison's own stated noise |
| **C** vs Restrepo et al. (2006), 32 sub-basins: mean **~690**, max **2,200** t km⁻² yr⁻¹ | mean form: ours 1.689× **above**; max form: 0.530×, quoted as "up to 1.888× low" | mean form is **yield vs yield**: 1.689× above, the *expected* direction. **Max form WITHDRAWN as invalid at basin scale under either reading** |
| **combined** | 1.03 – 2.27× low | **1.33 – 1.49× high** |

**Why Leg C's max form is withdrawn.** It compares a **mean** over 257,097 km² against the
**maximum** of 32 catchments of 320 – 59,600 km². A spatially variable field's mean is
*arithmetically required* to lie below its own maximum, and this model's internal range is **18.671×**
(A1.3.3: Andean flanks 1,445.32 vs lowland floodplain 77.41). "0.530× the maximum measured yield"
measures spatial variability, not under-erosion. It cannot be evidence for or against any level.

## A1.9.3 Verdict on the clause

**Clause 4′ → NOT ESTABLISHED, superseded by clause 4″** (A1.1). The clause asked for consistency
with published levels; it can only be evaluated once both sides name the same quantity, and they do
not. **The residual's direction is UNKNOWN across a bracket of 2.27× too low to 1.49× too high.**

**And the yield reading is NOT adopted here.** It makes the adopted result look better, which is the
reason to hold it at arm's length rather than the reason to take it. Its own counter-argument,
recorded so that it travels with it: MUSLE was fitted to sediment yields measured at the **outlets of
18 small watersheds**, while this project evaluates it **per 90 m DEM pixel and sums ~30 million
pixels**. A per-pixel sum over 257,097 km² is therefore not a basin sediment yield either — every
pixel is credited with delivering to a stream it may be 100 km from. **Our sum is neither exactly
gross erosion nor exactly a basin yield**, and saying so is the finding, not a hedge.

**RESOLVER for clause 4″**, in priority order and all decidable on source grounds before any level is
looked at: (1) state in writing, with citations, which quantity the per-pixel MUSLE sum is under the
MGB-SED lineage — Buarque (2015) applies MUSLE per pixel and then routes the sediment through a linear
reservoir (`src/mgb_sediment.py` implements it with `tau = 0`, a lag and not a loss), which is
consistent with reading B; (2) if reading B holds, the comparator set must be **yields** (Restrepo
et al. 2006's 32-sub-basin mean; Tan et al.'s 1.3 – 16.9 t ha⁻¹ a⁻¹), never (R)USLE erosion rates, and
the per-pixel-sum caveat above must be stated with the comparison; (3) if reading A holds, Leg A's
denominator needs a *hillslope-yield-to-gross-erosion* conversion that is cited for terrain like this
one — NEH Table 6-2's 0.33 is a US agricultural sheet-erosion figure, used here to establish the
*direction* and explicitly **not** a validated conversion for a tropical Andean basin. **Until (1) is
answered, no level comparison may be reported with a direction.**

## A1.9.4 What this does to C4 — G5 keeps its force and gains a number

1. **C4 must not fit α against clause 4′ or 4″.** `docs/35` §6 RULE 0 already forbade fitting to close
   a gap; A1.9 removes even the gap's sign. A fit justified by "the model is 2× under-erosive" would
   be justified by a withdrawn interpretation.
2. **Measured, and it is the reason `docs/42` G5 exists.** The α that reproduces Tan's *converted*
   level under reading B is **7.92 – 8.86** (11.8 ÷ 1.4897 and 11.8 ÷ 1.3323, α being linear in the
   load). `docs/42` G5 / A1.6 item 1 record that a **deposition-free** fit — one silently asserting
   SDR = 1.0 between hillslope and station — lands α at **6.83 – 8.73**. **These overlap.** So a fit
   that "works" under the yield reading is nearly indistinguishable from one that has simply deleted
   channel deposition, and G5's precondition (a **named** transport sink, or the words *"this model
   asserts SDR = 1.0 between hillslope and station"* stated as a claim, **plus** G1.2's `k̂` with its
   interval in the same table as α) is the only thing that can tell them apart. **G5 is not softened
   by A1.9; it is exactly what A1.9 predicts C4 will need.**
3. **The unexplained-residual arithmetic in A1.5 loses its sign, not its terms.** Candidate 0 (the LS
   formulation, ×0.333 – ×0.421) still points down and is still the largest single term; candidate 2
   (the peak deficit, 1.4 – 4.8×) still points up; P = 1.0 and FG = 1.0 are still one-sided upper
   bounds. What may no longer be said is that they are collectively required to close a 1.03 – 2.27×
   shortfall.

## A1.9.5 The reading under which the retired ratio was telling us something true

If the MUSLE sum is a hillslope→stream **yield**, then `outlet load ÷ MUSLE sum` was never a delivery
ratio — it is a **channel-and-floodplain throughput**, and its complement is transit loss:

| | ratio at 144 Mt/yr | ratio at 184 Mt/yr | implied transit loss |
|---|---:|---:|---|
| prior `C` (248.7298 Mt/yr) — the number A1.2 retired | 0.5789 | 0.7398 | **26.0 – 42.1 %** |
| adopted `C` (299.5387 Mt/yr) | 0.4807 | 0.6143 | **38.6 – 51.9 %** |

The **prior-`C`** loss of 26.0 – 42.1 % lies inside `docs/40` C11's primary-verified Depresión
Momposina retention of **20 – 45 %** (36 – 80 Mt/yr, labelled *"una cifra preliminar"* by its own
author). **That agreement is real and it is worth putting to the advisor**: the quantity this project
retired as an implausible SDR may have been an ordinary transit loss all along, and 0.579 – 0.740 is
close to what a Momposina-dominated floodplain system would produce.

**It must not be quoted as a current result, for two reasons.** First, it is a **prior-`C`**
agreement: at the adopted `C` the required loss is 38.6 – 51.9 %, *above* the Momposina band, so the
Momposina alone no longer accounts for it — total transit loss is 155.54 Mt/yr at the low anchor and
115.54 at the high one, of which M9's 36 – 80 Mt/yr is 12.0 – 26.7 % of the hillslope yield, leaving
**75.5 – 119.5 Mt/yr (25.2 – 39.9 %)** resp. **35.5 – 79.5 Mt/yr (11.9 – 26.6 %)** for every other
sink. Second, reading B is not established (A1.9.3). This is a **hypothesis with a measured bracket
and a named test** — `docs/42` G1.2's `k̂` — not a closure argument. And it licenses no loosening: an
*interpretable* throughput is still an unvalidated one.

## A1.9.6 Direction disclosure, and what was NOT done

- **The one change that makes the adopted result look better is the one this amendment refuses to
  adopt.** Reading B moves the model from 2.03 – 2.27× low to 1.33 – 1.49× high on the decisive leg;
  A1.9 records it as *unestablished* and reports the residual as **sign-unknown**, which is in one
  sense worse for the project than a clean shortfall, because a shortfall at least has a direction to
  work in.
- **No number in the repository was moved.** No parameter, no convention, no `cp_revision`, no
  threshold. A1.4's arithmetic is reproduced digit-for-digit. What changed is one **label** (which
  quantity a sum is) and the status of one **clause**.
- **No gate was passed.** Clause 4′ did not become MET; it became NOT ESTABLISHED, which is not a
  pass. C3 is OPEN on clauses 2, 3 and 4″.
- **No frozen artifact was read into or written.** `sim_calibrated_v2/{h2e_drivers.npz,
  parameters_H2E.csv, q_gauge_H2E.npz}` untouched; no simulation was re-run for A1.9 (the erosion
  levels are A1.3 – A1.4's, quoted); no calibration was launched; nothing is backdated.
- **Files written by this pass:** `docs/40_sdr_evidence.md` (§0 and its consequential notes), this
  amendment plus A1.1/A1.4/A1.7 pointers, `src/mgb_sediment.py`'s module docstring (A1.7 item 4), and
  `docs/agents/journal_fixer.md`.
- **Known gap, disclosed rather than fixed:** `notebooks/18_musle_construction.ipynb` §6.4/§7 still
  present clause 4′ as a directed result, in *executed* cells as well as markdown. Enumerated with
  generator line numbers as **A1.7 item 7**, because fixing it needs a `src/nbgen/make_nb18.py` edit
  plus a full notebook re-execution.

## A1.9.7 Reproduction

```
A = 257097 km2 ; adopted-C basin total = 299.5387 Mt/yr
rate                     299.5387e6/257097 = 1165.0805 t/km2/yr = 11.6508 t/ha/yr
Leg A reading A          23.7/11.6508 = 2.0342 ; 26.5/11.6508 = 2.2745        (low)
Leg A reading B          DR 0.33 -> 7.8210 / 8.7450 ; 11.6508/7.8210 = 1.4897 ;
                         11.6508/8.7450 = 1.3323                              (HIGH)
                         DR 1/3 -> 1.4748 ; 1.3190 . Tan SSY 1.3-16.9 contains 11.6508
Leg B                    1485/1445.32 = 1.0275
Leg C                    1165.0805/690 = 1.6885 ; 1165.0805/2200 = 0.5296 (withdrawn)
internal range           1445.32/77.41 = 18.671
throughput               144/248.7298 = 0.5789 ; 184/248.7298 = 0.7398 -> 26.02-42.11 %
                         144/299.5387 = 0.4807 ; 184/299.5387 = 0.6143 -> 38.57-51.93 %
Momposina 36-80 Mt/yr    = 12.02-26.71 % of 299.5387
residual sinks           (299.5387-144)-[36,80] = 75.54-119.54 = 25.2-39.9 %
                         (299.5387-184)-[36,80] = 35.54-79.54 = 11.9-26.6 %
alpha reading B          11.8/1.4897 = 7.921 ; 11.8/1.3323 = 8.857   (G5 band 6.83-8.73)
alpha reading A          11.8*2.034 = 24.00 ; 11.8*2.275 = 26.84
python3.10 -m pytest tests/ -q     # unchanged by this amendment: 94 passed, 2 failed (A1.7 item 2)
```
