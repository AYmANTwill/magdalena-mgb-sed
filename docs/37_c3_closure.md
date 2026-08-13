# 37 — C3 closure verdict: **OPEN**

**Stage:** C3.6 of `docs/31_phase_c_workplan.md`. **Written 2026-08-11**, after the convention
amendment of `docs/35` §9.2 was applied to `src/mgb_sediment.py` and the basin decade was re-run.

C3 is **OPEN**, not closed. Precisely:

| closure condition | status |
|---|---|
| the factor chain is fully explained by evidence-based corrections | **MET** — 0.684 → 248.73 Mt/yr is exactly `1000^0.56 × (1/0.1317) = 363.4245196`, measured to the last stored digit |
| no decision left unresolved | **NOT MET** (amended 2026-08-11) — the four *convention* questions below are resolved from source derivations, but a fifth question was measured and left explicitly UNRESOLVED: the **LS formulation level**. Our LS sits ~~**2.37× – 3.00×**~~ above the LS that α = 11.8 is paired with in the MGB-SED lineage, measured on our own 90 m grid. See §4 candidate **0**. → **A3.3.1 (2026-08-12): the bracket is superseded by measurement. Read `1/f_LS` = 2.3151× – 3.9768×, from `f_LS` ∈ [0.25146, 0.43194] erosion-weighted (`docs/47` §4.3, registered `docs/46` §1.0); and per A3.1 the source formulation read whole is a POINT at `f_ero` = 0.25146 ⇒ 3.9767756303×. The clause stays NOT MET — A3 records the decision, it does not exercise it (A3.1.6).** |
| the independent audit agreed with the decisions | **MET** — agreement on all three decisions; the audit's fourth finding was verified here from this repository's own source text, not taken on trust |
| ~~**the implied sediment delivery ratio is physically plausible (0.05 – 0.30)**~~ **RETIRED — see `docs/40`** | ~~**NOT MET — implied SDR is 0.579 – 0.740**, and under §4 candidate 0 it becomes 1.37 – 2.22, i.e. impossible~~ → **the ratio 248.730 Mt/yr ↔ 144–184 Mt/yr is not a sediment delivery ratio** (all-source numerator, hillslope-only denominator) and cannot be tested against a published SDR band in either direction. The band was uncited, its supporting relations use an all-source denominator and were fitted 993× below this scale, and no Magdalena SDR exists in the literature. **A retired gate is neither a pass nor a fail.** The clause that replaced it — 4′ — was itself **re-opened as 4″, NOT ESTABLISHED**: see **A1.1** and **A1.9**, not this row. *(Struck in place 2026-08-11 per `docs/40` §8.2 as amended by its §0; applied by **A2.7**. Original text preserved above.)* |

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

### ~~The implied delivery ratio, which is why this document says OPEN~~ — **RETIRED, `docs/40`**

> **STRUCK IN PLACE 2026-08-11 (applied by A2.7, wording from `docs/40` §8.2 as amended by its §0).**
> The whole of this sub-section is retired and is preserved only as the record of what was believed.
> **This is no longer why this document says OPEN** — see **A1.1** (clauses 2, 3, 4″) and **A1.9**.
> Two specific sentences below are false as written and are struck rather than deleted.

MUSLE computes **gross hillslope erosion**; the outlet load is what survives channel transport
and floodplain deposition. ~~So `SDR = outlet / gross` must be < 1~~ — **FALSE for the quantity
computed:** the ratio of outlet load to *hillslope-only* gross erosion has **no upper bound of 1**;
channel-bank supply alone averages **1.3×** the outlet flux in the Brazilian Amazon (Dunne et al.
1998), and USDA NEH Table 6-2's own mixed ratio is **1.7778** — and ~~for a basin of
257,097 km² the published expectation is roughly 0.05 – 0.30~~ — **UNCITED in this repository and
retired in both directions** (`docs/40` §8.1).

| against outlet anchor | ~~implied SDR~~ **apparent delivery ratio (ADR), not an SDR** | ~~verdict~~ **no verdict — the gate is retired** |
|---|---|---|
| 144 Mt/yr | **0.579** | ~~above the plausible band~~ — *below* USDA's own reference ADR of 1.7778 and ≈ its true SDR of 0.6957 |
| 184 Mt/yr | **0.740** | ~~above the plausible band~~ — as above |

Read as the gross erosion that the anchor plus a plausible SDR would require:

| required SDR | required gross erosion | shortfall of the model | α that would be needed at the adopted convention |
|---|---|---|---|
| ~~0.30~~ | ~~480 – 613 Mt/yr~~ | ~~**1.93 – 2.47×**~~ | ~~22.8 – 29.1 (1.93× – 2.47× Williams)~~ |
| ~~0.15~~ | ~~960 – 1,227 Mt/yr~~ | ~~3.86 – 4.93×~~ | ~~45.5 – 58.2 — **past the `docs/35` §6.1 hard stop**~~ |
| ~~0.05~~ | ~~2,880 – 3,680 Mt/yr~~ | ~~11.6 – 14.8×~~ | ~~136.6 – 174.6 — far past the hard stop~~ |

> **ALL THREE ROWS STRUCK 2026-08-11** (A1.2 consequence 2, applied in place by A2.7). They rest
> entirely on the retired band and on the ADR/SDR conflation; the 0.15 and 0.05 rows **overstated the
> problem by 4 – 8×**. Nothing in this table may be quoted as a requirement on the model.

The amendment moved the model onto the physically *possible* side of the outlet anchor for the
first time (gross 248.7 > outlet 144–184, where all three pre-amendment conventions had gross
*below* the outlet load, which is impossible). That is real progress. It is not closure.

> **CONDITIONAL — read with §4 candidate 0 (added 2026-08-11).** "Physically possible side" holds
> **only if** our LS is at the level that α = 11.8 belongs to. That equivalence was asserted, not
> demonstrated, when this sentence was written — and it has since been *measured*, on our own
> 90 m grid, as violated by ~~**2.37× – 3.00×**~~ (`docs/agents/journal_decide-ls-resolution.md` §3b).
> ~~Applying the measured bracket takes 248.730 → **104.8 Mt/yr** (×0.421) or **82.8 Mt/yr**
> (×0.333), i.e. **below both anchors**, implied SDR **1.37 – 2.22** — back on the impossible
> side.~~ So the sign of gate (b) is *not* yet secured; it is secured only at our LS level, and our
> LS level is the one thing in the chain that is known to be off and not yet corrected. Treat the
> "possible side" claim as provisional until C3.1 (`docs/35` §9.3) settles the formulation.
>
> > **⚠ AMENDMENT A3.3.1, 2026-08-12 — the two struck numbers above are superseded by
> > measurement, and the base is superseded too.** The bracket is `1/f_LS` = **2.3151× – 3.9768×**
> > (`f_LS` ∈ [0.25146, 0.43194] erosion-weighted, `docs/47` §4.3, registered `docs/46` §1.0), and
> > per **A3.1** the source formulation read whole is a **POINT** at `f_ero` = **0.25146** ⇒
> > **3.9767756303×**. The 248.730 Mt/yr base is itself superseded by A1.3's **299.5387088405831
> > Mt/yr**, so the correct engine figures are **129.3840 Mt/yr** (the documented hybrid `V4`,
> > ×0.43194) and **75.3235 Mt/yr** (the adopted `V4_dg`, ×0.25146) — engine re-runs, not
> > proxies. The struck ADR arithmetic is *not* re-derived here: the SDR band is retired
> > (`docs/40`, A1.2) and `docs/46` §4.3 forbids the anchors and the distance between them as
> > evidence in the LS decision. C3.1 **has now settled the formulation on source grounds**
> > (A3.1); it has **not** switched the engine default (A3.5.1), so the provisionality of this
> > paragraph's "possible side" claim stands unchanged.

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

~~The unexplained residual is **1.93 – 14.8×** of gross erosion, depending on which end of the
0.05 – 0.30 SDR band is taken~~ — **STRUCK 2026-08-11 (A2.7): this sizing is derived entirely from
the retired band. The residual's current form is A1.9's — magnitude bracketed, DIRECTION UNKNOWN,
2.27× too low … 1.49× too high** — and **candidate 0 below makes that residual larger, not smaller,
by a further ~~2.37× – 3.00×~~** → **A3.3.1 (2026-08-12): read 2.3151× – 3.9768×, and at the
adopted POINT 3.9767756303×.** Five candidates, with what would settle each. None of them may be
absorbed into α (`docs/35` §6 RULE 0). **Amended by A2:** candidates 0 and 2 decompose into a
*level* part, which A2 reclassifies as C4's calibration target, and a *shape* part, which it does
not — read A2.1–A2.2 before treating any candidate as a single quantity.

0. **The LS *formulation* level — the largest term in this list, and it points the WRONG WAY.**
   Listed first because it is the biggest and because it was missing from every numbered document
   until 2026-08-11. Our LS2D differs from the MGB-SED reference LS in three ways, all measured on
   the **same** 90 m grid, i.e. this is a *formulation* difference and not the resolution question
   that decision 4 in §1 resolved:

   | lever | ours | Buarque (2015), the method this project transposes | measured × on basin area-wtd LS |
   |---|---|---|---|
   | slope-length limiter | upslope **area** ≤ 1 km² ⇒ unit contributing length up to 1e6/92 ≈ **10,870 m** ≈ 118 pixels | p. 94: "seu valor máximo foi limitado ao **tamanho do pixel do MDE**" — slope length ≤ **one pixel** | **0.351** (dominant) |
   | `m` | continuous McCool (1989), basin median **0.584** | ~~his eq. 14, step function **hard-capped at 0.5**~~ → **A3.3.2**: **two different objects, both named below** | ~~0.502~~ → **A3.3.2** |
   | `S` | Moore & Burch (1986) `(sinθ/0.0896)^1.3` | his eq. 18, Wischmeier & Smith (1978) `65.41 sin²θ + 4.56 sinθ + 0.065` | 1.714 |
   | **all three together (source-method LS)** | area-wtd mean **39.812** | area-wtd mean **16.775** | ~~**0.421**~~ → **A3.3.1**: `f_ero` **0.431944** · `f_area` ~~**0.421475**~~ → **0.42136300143291305** (**A3.3.4**, 2026-08-12; owning records `docs/46` §10 amd 2 / `docs/51` §9 amd 1) (`V4`, the documented **hybrid**) |

   The three levers interact (0.502 × 1.714 × 0.351 = 0.302 ≠ the joint 0.421 — → **A3.3.2**: the
   ×0.502 here is the **CAP**, `min(m, 0.5)`, not eq. 14; and → **A3.3.1**: exactly, on the
   erosion-weighted basis and with the eq.-14 **step**, 0.362435 × 0.522043 × 1.694054 =
   0.3205262902296241 ≠ the joint 0.431944, measured **joint / product = ×1.347608646050708**; with
   the **cap** instead, 0.362435 × 0.517480 × 1.694054 = 0.3177246791318452), so no single one is
   "the" cause. Using the literal Desmet–Govers finite-difference `L` in place of our continuous
   form lowers the source row a further ~~×0.790~~, giving the bracket ~~**×0.333 – ×0.421**~~, i.e. our LS
   is ~~**2.37× – 3.00×**~~ the level α = 11.8 is paired with. Source and measurement:
   `docs/agents/journal_decide-ls-resolution.md` §1a and §3b (all 30,235,916 basin cells; the
   harness reproduces our own 39.812 bitwise).

   > **⚠ AMENDMENT A3.3.1 + A3.3.2, 2026-08-12 — this candidate is now DECIDED, and four of its
   > numbers are superseded. Nothing above is deleted.**
   >
   > 1. **The `m` row's label was wrong.** The object measured as ×0.502 is `min(m_continuous, 0.5)`
   >    — **a cap**, which is **nobody's published formulation and may NEVER be graded CITED**
   >    (`docs/46` §2.2). **Buarque eq. 14 is a STEP function**, printed p. 47 verbatim: `m` = 0.2
   >    (`Sf` < 1 %) / 0.3 (1 ≤ `Sf` < 3) / 0.4 (3 ≤ `Sf` < 5) / 0.5 (`Sf` ≥ 5), *"onde `Sf` [%] é a
   >    declividade do pixel"* — `Sf` is slope **PERCENT** (corroborated p. 48). Both objects,
   >    kept named and distinct, with both factors printed: **eq. 14 step (`V2b`) = ×0.505092
   >    area-weighted / ×0.522043 erosion-weighted**; **the cap (`V2a`) = ×0.502472 area-weighted /
   >    ×0.517480 erosion-weighted** (`docs/49`). ×0.502 is the **CAP**, not eq. 14. See **A3.3.2**.
   > 2. **The joint and the bracket are superseded by exact erosion-weighted engine re-runs**
   >    (`docs/47` §4.3, registered `docs/46` §1.0, §3.1): `f_LS` ∈ **[0.25146, 0.43194]**
   >    erosion-weighted ⇒ `1/f_LS` ∈ **[2.3151×, 3.9768×]**. ×0.333 is **REFUTED** (`docs/47`
   >    §3.1 R6: it is 0.421 × 0.790, and 0.790 is two levers measured on the wrong column).
   > 3. **The interval is not an uncertainty band.** With eq. 13 read verbatim on p. 47 there is
   >    **no admissible reading of Buarque in which `L` is our point-rate form** (`docs/46`
   >    §2.5.2), so **the source formulation read whole is a POINT** — `V4_dg`, `f_ero` =
   >    **0.25146**, `f_area` = **0.2446790094097074** — and ×0.43194 is a **documented HYBRID**
   >    (the source's three levers with *our* `L`), retained only for reproducibility. The
   >    0.5410027585442313 ln span between them **is the `L`-form lever** (×1.7177284657599616).
   > 4. **`docs/46` §4.2's outcome is now exercised as ADOPT-SOURCE at `ls_formulation = **[⚠ A3.9, 2026-08-13: "exercised" was PREMATURE as written here — `docs/46` §4.2 note 3 reserves *exercised* for the step gated on §3.3's full stratified report, and A3.1.6 of this amendment correctly said **determined and recorded, NOT YET EXERCISABLE**. It has since become TRUE: see A3.9.]**
   >    buarque_2015_dg`** — see **A3.1**. The RESOLVER named below has therefore been executed on
   >    source grounds; what remains owed before the engine default may move is **A3.1.6**'s three
   >    deliverables. **STANDING INSTRUCTION** (`docs/46` §2.4): never quote a product of
   >    single-lever factors as the joint factor — measured **joint / product = ×1.34762**.

   **Two consequences, both unfavourable, both stated in full:**
   - **On the level.** MUSLE is linear in LS, so ~~248.730 × 0.421 = **104.8 Mt/yr** and × 0.333 =
     **82.8 Mt/yr**~~ → **A3.3.1 (2026-08-12): superseded on BOTH the base and the factors. At the
     adopted C level 299.5387088405831 Mt/yr the exact engine re-runs are 299.5387088405831 ×
     0.43194 = **129.3840 Mt/yr** (the hybrid `V4`) and × 0.2514648985839397 =
     **75.32347104056149 Mt/yr** (the adopted `V4_dg`) — `docs/47` §4.3. The implied-SDR
     arithmetic is NOT re-derived: the band is retired (A1.2, `docs/40`) and the anchors may not be
     used as evidence in the LS decision (`docs/46` §4.3).** ~~— *below* both anchors, implied SDR
     **1.374 – 2.222**, i.e. back on the
     physically impossible side that §2 claims was left behind.~~ **Caveat on that arithmetic:**
     0.421 is a ratio of **area-weighted** per-cell LS means, whereas the basin total weights LS by
     each cell's `Qsur·q_peak·K·C`, so 104.8 is a **proxy, not a re-run**. It is a defensible proxy
     because the swap has nearly the same effect on the erosive terrain as on the whole basin
     (Andean >1000 m: 27.109/65.199 = 0.416 vs basin 0.421) and erosion is concentrated there
     (§3 gate (a)). The exact figure requires the C3.1 re-run. → **A3.3.1: the C3.1 re-run has
     landed, so the proxy caveat is discharged as MEASURED — and the proxy errs in the model's
     favour, not against it: `f_ero`/`f_area` = 0.25146 / 0.2446790094097074 =
     **1.0277138223121463**, i.e. the proxy is 2.51 % low (`docs/47` §3.1 R7, independently
     1.0278). `f_ero` decides and `f_area` is reported beside it and can never override it
     (`docs/46` §3.3).**
   - **On the α guard.** Because MUSLE is linear in LS, a fit on our LS returns an α that is
     ~~1/2.37 – 1/3.00~~ of what the same observations would return on the source's LS. The like-for-like
     α reference for **our** LS is therefore ~~**≈ 3.9 – 5.0, not 11.8**~~; the `docs/35` §6.1 expected
     band 5.9 – 23.6 becomes ~~≈ **2.0 – 9.9**~~ and the hard stop α > 35.4 becomes ~~≈ **11.8 – 14.9**~~.
     ~~The **adopted, unfitted α = 11.8 then sits at or above its own corrected hard stop** at the
     3.00× end of the bracket.~~ This tightens the guard; it does not loosen it.
     > **⚠ AMENDMENT A3.3.1 + A3.2, 2026-08-12 — all four struck α numbers are superseded. The
     > registered rescaling is `1/f_LS` = 2.3151× – 3.9768×, and at the ADOPTED POINT
     > `f_LS` = 0.25146 it collapses to single numbers: α reference `11.8·f` = **2.9672280000000004**;
     > `docs/35` §6.1 expected band `5.9–23.6 · f` = **1.4836140000000002 – 5.934456000000001**;
     > hard stop `35.4·f` = **8.901684**; lower hard stop `3.9·f` = **0.9806940000000001**;
     > `1/f` = **3.976775630318937**. Full arithmetic, the area-proxy column and the coordinate the
     > column lives in: **A3.2**. The old *"α = 11.8 sits at or above its own corrected hard stop"*
     > sentence does not survive as written — at the adopted point the rescaled hard stop is 8.9017
     > and 11.8 is **above** it, which is a sharper statement, but it is a statement about the
     > PAIRING of α with an LS and not about α (`docs/46` §8.2 item 2), and α = 11.8's
     > like-for-likeness with any 2-D contributing-area LS is **NOT SETTLED, with no band offered**
     > (`docs/47` §4.2 item 6). That ceiling bounds every number in this bullet.**

   **RESOLVER:** the pre-registered C3.1 LS-formulation comparison — choose the limiter, the `m`
   cap and the `S` function **on source grounds, in writing, before any basin total is looked at**
   (`docs/35` §9.3). Note also that the source's own verdict on his Andean LS (p. 121) is that even
   his *pixel-capped* L "tende a fazer com que as estimativas da erosão laminar do solo em áreas
   íngremes, como nos Andes, seja **superestimado**", and ours uses a looser limiter than his.

   **DO NOT** stack the upward candidates below (1: C revision ×2–5; 2: `f_peak` ×2.1) on top of an
   LS that is ~~2.4 – 3.0×~~ → **A3.3.1 (2026-08-12): 2.3151 – 3.9768×, and 3.9767756303× at the
   adopted POINT** too high for its own α, and then read the sum as agreement with the
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
3. ~~**The 0.05 – 0.30 SDR expectation itself is uncited in this repository.** It arrived as a
   brief-level assertion, exactly like the "mountainous LS 2–10" comparison that decision 4
   retired. The Magdalena is an unusually high-yield system, and a large basin SDR near 0.5 is
   not self-evidently absurd for it.
   **RESOLVER:** a citation for basin-scale SDR in humid tropical Andean catchments, or a
   Magdalena-specific sediment-budget paper. **This is a reason C3 is OPEN, not a reason to call
   it closed:** an uncited plausibility band cannot be used to *pass* a gate any more than it
   could be used to fail one, and until it is cited the level remains unvalidated.~~
   → **RESOLVED AND RETIRED (`docs/40`).** *(Replacement wording from `docs/40` §8.2, applied in
   place 2026-08-11 by A2.7; the same text already stands as A1.5 residual 3.)* The band is retired
   as a gate: the tested quantity is an **apparent** delivery ratio (all-source outlet load ÷
   hillslope-only gross erosion), not an SDR, and the same mixed ratio is **1.7778** in USDA NEH
   Ch. 6's own reference example (true SDR 0.6957, hillslope-only ratio 0.33). No Magdalena SDR
   exists, because every published Magdalena "erosion rate" is a sediment *yield*. §2's SDR = 0.15
   and SDR = 0.05 requirement rows are **struck**. The residual survives, relocated to the erosion
   side — **and per A1.9 its direction is now UNKNOWN** (2.27× low … 1.49× high), so `docs/40`
   §8.2's own "1.59 – 2.74×" figure in this slot is **not** re-adopted here.
4. **Terms known to point the wrong way, listed so they are not proposed later as fixes.**
   P = 1.0 and FG = 1.0 are both upper bounds on erosion (P ≤ 1, FG ≤ 1), so any real value
   *lowers* the model and widens the residual. Driving MUSLE with released rather than generated
   runoff costs a further 1.125×. **The largest wrong-way term is candidate 0 above
   (~~×0.333 – ×0.421 = 2.37 – 3.00× of residual~~ → **A3.3.1: `f_LS` ∈ [0.25146, 0.43194] ero
   = 2.3151 – 3.9768×, and 3.9767756303× at the adopted POINT**), not the 1.125× recorded here** — when this list
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
   not yet level-equivalent, and at the corrected band (expected ~~≈ 2.0 – 9.9~~ → **A3.2: at the
   adopted POINT the rescaled expected band is 1.4836140000000002 – 5.934456000000001**) an
   SDR = 1.0 fit at α = 6.83 – 8.73 ~~still lands inside it~~ → **A3.3.1: as arithmetic, 6.83 – 8.73
   lies ABOVE the rescaled band's upper edge 5.9345 and BELOW the rescaled hard stop 8.9017 — i.e.
   in `docs/35` §6.1's "watch" register rather than "expected". That is NOT re-stated here as a
   finding, for a reason `docs/47` §2.5 C1 records: 6.83 – 8.73 is `11.8 × {144,184} / 248.730`,
   i.e. at the PRIOR `C`; at the adopted `C` the deposition-free band is 5.67 – 7.25, and C1's
   correction to `docs/43` §3.4 is owed to that file. What survives unqualified is the trap itself:
   the α band is not a sufficient guard, `docs/42` G5 is, and the numbers to quote the trap with are
   now A3.2's. None of them passes or fails anything here.**
   The trap is unchanged in kind and the numbers to quote
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
| 2 | no decision left unresolved | **NOT MET**, unchanged and unchanged in cause — the **LS formulation level** (§4 candidate 0) is still explicitly UNRESOLVED. Our LS sits ~~**2.37×–3.00×**~~ above the level α = 11.8 is paired with. **This clause alone forbids closure today, independently of everything else in this amendment.** → **A3.3.1 + A3.5.2 (2026-08-12): read 2.3151× – 3.9768×, and 3.9767756303× at the adopted POINT. The FORMULATION decision is now taken (A3.1, ADOPT-SOURCE at `buarque_2015_dg`) — but clause 2 is still NOT MET: ADOPT-SOURCE is recorded and not yet *exercised* (A3.1.6), the engine default has not moved (A3.5.1), and `docs/46` §8.2 item 6 holds that clause 2 needs the *shape* decision — settling LS is NECESSARY AND NOT SUFFICIENT.** |
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
adopted C, applying the measured LS bracket (~~×0.333 – ×0.421~~, §4 candidate 0) gives
~~**99.8 – 126.1 Mt/yr**~~ — still *below* both outlet anchors, ~~ADR **1.14 – 1.84**~~, and Leg A worsens
to ~~**4.8 – 6.8×**~~.
→ **A3.3.1 (2026-08-12): the factors and therefore the loads are superseded by exact
erosion-weighted engine re-runs — `f_LS` ∈ [0.25146, 0.43194] gives **75.3235 – 129.3840 Mt/yr**
(`docs/47` §4.3), and at the adopted POINT it is the single figure **75.32347104056149 Mt/yr**. The
ADR and Leg-A numbers are NOT re-derived: A1.9 withdrew the residual's direction and `docs/46` §4.3
forbids the anchors as evidence in the LS decision. The sentence that survives is the one this
paragraph is actually for — the C revision does not rescue the LS question, and the two must not be
netted against each other.** The C revision does **not** rescue the LS question, and the two must not be
netted against each other: candidate 0 is a formulation error to be resolved on source grounds, not
a factor to be cancelled by another factor.

---

## A1.5 What remains OPEN, and what would resolve it

§4's five candidates, restated with their status after `docs/40`–`docs/42`. The unexplained residual
is now **1.03 – 2.27×** on the **erosion side** (not 1.93 – 14.8× of an SDR), and candidate 0 still
makes it larger by a further ~~2.37 – 3.00×~~ → **A3.3.1: 2.3151 – 3.9768×, 3.9767756303× at the
adopted POINT**. None may be absorbed into α (`docs/35` §6 RULE 0).

0. **The LS *formulation* level — ~~STILL OPEN~~, still the largest term, still pointing the wrong way.**
   Unchanged by everything in this amendment: ~~×0.333 – ×0.421~~ on the level, and the like-for-like α
   reference for *our* LS is ~~≈ 3.9 – 5.0~~ rather than 11.8. **RESOLVER: unchanged** — the
   pre-registered C3.1 LS-formulation comparison (`docs/35` §9.3), decided on source grounds, in
   writing, before any basin total is looked at. **This is now the single highest-value open item in
   Phase C**, a position `docs/40` §8.3 assigned to the C factor before the C factor was measured and
   found to be worth only ×1.20.
   > **⚠ AMENDMENT A3, 2026-08-12 — THE RESOLVER HAS BEEN EXECUTED.** The `docs/35` §9.3
   > comparison, run under the frozen pre-registration `docs/46`, returns **ADOPT-SOURCE**:
   > `ls_formulation = buarque_2015_dg`, the source formulation **read whole**, `f_ero` =
   > **0.25146** (second independent reproduction 0.2514648985839397) / `f_area` =
   > **0.2446790094097074**, ⇒ `1/f_LS` = **3.976775630318937**. Grade: the FORMULATION CHOICE is
   > **CITED** on all four levers; the LS **LEVEL** stays **UNVALIDATED** (`docs/42` G4.2). The
   > like-for-like α reference at the adopted point is **2.9672280000000004** (A3.2). **The item is
   > DECIDED but NOT CLOSED**: three named deliverables stand between the decision and the engine
   > default (A3.1.6), the default has not moved (A3.5.1), and clause 2 of A1.1 is still NOT MET
   > (A3.5.2). Full record: **A3.1**.
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
correction lowers the model by ~~2.4 – 3.0×~~ → **A3.3.1 (2026-08-12): 2.3151 – 3.9768×, and
3.9767756303× at the adopted POINT — so the opposition is *wider*, not narrower** while clause 4′
asks for 1.03 – 2.27× more. Resolving
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
   formulation, ~~×0.333 – ×0.421~~ → **A3.3.1: [0.25146, 0.43194] erosion-weighted, and a POINT at
   0.25146 as adopted by A3.1**) still points down and is still the largest single term; candidate 2
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

---

# AMENDMENT A2 (2026-08-11, after A1.9) — the residual's **level** is RECLASSIFIED from defect to calibration target. **C3 stays OPEN.**

Written by the `decide-c3-c4` agent (`docs/agents/journal_decide-c3-c4.md`) after three independent
lenses reported: `journal_adj-ratio.md` (does the bias cancel in the ENSO ratio — **PARTIALLY**),
`journal_adj-alpha-role.md` (what α is for — **does not block C4**), `journal_adj-c4-feasibility.md`
(is C4 feasible — **PARTIALLY**). The adjudication that combines them is **`docs/43_c3_c4_gate.md`**;
this amendment records only what it does to *this* document.

**Nothing above this line is rewritten**, with one exception that is itself an amendment: **A2.7**
applies `docs/40` §8.2's paste-ready corrections *in place* to §1, §2 and §4, as **strike-through
with a dated pointer**, so that no sentence is deleted and the retired gate can no longer be quoted
out of the body. A1 and A1.9 are untouched.

> **THE VERDICT DOES NOT MOVE. C3 was OPEN and stays OPEN**, on clauses **2**, **3** and **4″**.
> What moves is the *name* of one component of the residual, and it moves on evidence.

> **`docs/42` G9 disclosure, required in the same paragraph as any basin-scale statement:** at the
> adopted `C`, **66.53 % of the model's gross erosion — 199.29 of 299.54 Mt/yr — is upstream of no
> usable SSC station**; only **33.47 %** is; and **801.1 km of channel, including the whole
> Depresión Momposina, lies below the outlet-most SSC station** (`21237020` ARRANCAPLUMAS).

---

## A2.1 The reclassification, and the evidence for it

**The multiplicative LEVEL component of the C3 residual is reclassified from *defect* to
*calibration target*.** Two independent legs, either sufficient on its own:

1. **The transposed method defines α and β as free.** Re-extracted from the primary sources in this
   run, not from secondary notes. Fagundes (2018) eq. 11 calls them *"coeficientes de ajuste … ora
   adotados como 11,8 e 0,56 … ora **calibrados automaticamente**"*; §6.3.1 places them in the
   MOCOM-UA parameter vector alongside TKS; they are fitted **per sub-basin** (1, 5 or 17) and
   **separately against each of four observed sediment datasets** (in-situ CSS at 21–26 stations,
   red-band surface reflectance at 21, turbidity at 61–63, SST at 61–63) over 1997–2010, under a
   search prior α ∈ [2.0, 25.0], β ∈ [0.2, 1.7] (widened to α ∈ [0.0001, 500.0] in experiment C4).
   **The decisive measurement, from the source's own Appendix IV (426 published fitted pairs): for
   the same sub-basin in the same experiment, fitted α changes by median 1.28× and up to 7.78×
   depending only on which observed dataset was the calibration target** (101 complete rows; 30.7 %
   spread > 1.5×, 13.9 % > 2×; β likewise, median 1.33×, max 3.25×). A physical constant cannot do
   that. **An unfitted α is an unset lever, not a wrong value.**
2. **The level has no separate existence to be defective.** `docs/42` §3.1: α, the C level, the LS
   level, the K unit system, the volume convention, P and FG are seven ways of writing **one
   identifiable product Π**, design-matrix condition number measured as **inf** (exactly singular).
   The "level residual" *is* Π; Π is what a C4 fit sets.

**This is a reclassification, not a tolerance.** The claim is not that the level is right, nor that
the residual is small. The claim is that the level belongs to a parameter the method leaves free, so
"the unfitted model is off by a factor" is a statement about C4's starting point, not a defect of the
C3 build.

**What A1 and this document said about that level, which is now labelled rather than repaired.**
`docs/35` §6.1's α band was imported from the wrong branch of the lineage: it cites **Buarque (2015)**,
who writes 11.8 and 0.56 as *literals*, runs MOCOM-UA on the **hydrology only**, sets the MUSLE
factors "de acordo com faixas de valores obtidas da literatura" — and then **recommends** the
per-sub-basin spatialisation of the MUSLE parameters that Fagundes went on to do. `docs/00`'s H3
declares the transposition to be of **Fagundes**, the branch that fits them.

**Empirical falsification of the band, run on this repository's own unmodified code.**
`check_musle_parameters` (`docs/35` §6.1 + §6.3 thresholds) over all **426** published, **adopted**
(α, β) pairs of the source method returns:

| verdict | count | share |
|---|---:|---:|
| `STOP` | **185** | **43.4 %** |
| `watch` | 59 | 13.8 % |
| `ok` | 182 | 42.7 % |

**42.7 points of that STOP rate is the β hard stop 0.45 – 0.65** — and β is **dimensionless**, so no
unit or convention argument can rescue it (the very property `docs/35` §9.2 and `docs/42` §8.1 rely
on). The α hard stop trips on only 5/426 = 1.2 %, because our stops are *wider than the source's own
search prior* — which is also why 97.7 % of the fits land inside the "expected" 5.9 – 23.6 band: the
statistic measures the prior, not the physics.

> **What this amendment does NOT do with that finding.** It does **not** edit `docs/35` (a frozen
> pre-registration, not this pass's file) and it does **not** relax the β band for C4. `docs/42` G2.3
> re-affirms the β hard stop and it stands until whoever owns `docs/35`/`docs/42` re-derives or demotes
> it, with a date and a reason. This amendment records only that **an α band is a test on Π with six
> of seven factors assumed, and could never have been a test on α** — which is `docs/42` §3.1's
> position, now with a measured reason and a source-side falsification behind it.

---

## A2.2 What is NOT reclassified — and this is why C3 stays OPEN

`docs/42` §1's principle: **a scalar absorbs a level; it cannot absorb a structure.** Three structural
components of the residual survive the reclassification, each measured, each with an owner that is not
α:

| residual component | classification | measurement | owner |
|---|---|---|---|
| the multiplicative **level** (Π) | **CALIBRATION TARGET** — status **UNVALIDATED and unfittable-apart** | A2.1 | **C4**, as a fitted Π reported with its equifinal family |
| the **LS slope-dependent shape** | **STILL A DEFECT**, direction known | §4 candidate 0: the three levers (limiter ×0.351, `m` cap ×0.502, `S` ×1.714) act per cell as a function of slope and do **not** multiply out (0.502 × 1.714 × 0.351 = 0.302 ≠ the joint 0.421). Only the joint *level* joins Π. → **A3.3.1 (2026-08-12): the exact erosion-weighted factors are limiter 0.362435 · `m` CAP 0.517480 · `m` eq.-14 STEP 0.522043 · `S` 1.694054, joint (`V4`) 0.431944, and the source read whole (`V4_dg`) 0.25146; measured joint / product = ×1.34762 — never quote a product of single-lever factors as the joint factor (`docs/46` §2.4). There are FOUR levers, not three: the `L` form is the fourth and is worth the whole 0.5410027585442313 ln span (`docs/46` §4.2 item 5 as amended).** | **C3.1** — a written source-grounds decision (`docs/35` §9.3). → **A3.1 (2026-08-12): that decision is TAKEN — ADOPT-SOURCE at `buarque_2015_dg`. The SHAPE defect is not thereby repaired: the adopted field is not in the engine (A3.5.1), `docs/46` §2.3's H-S field clause (R7)/(R8) items 2–3 have never been read out, and G4.1 is measured 3.1× underpowered to see the shape at all (`docs/47` §4.4).** `docs/42` **G4.1** can detect the shape, never fix it |
| **station-to-station heterogeneity** of the residual | **STILL A DEFECT**, unresolvable at this fleet size | I² **96.0 – 99.2 %**, Cochran Q p ≤ 3.2e-16, τ **2.03× – 3.40×** per station, station `expD` 0.203 – 4.550, **18 of 24** station-cells with CIs excluding 1 | not resolvable by C4; needs n ≈ 19 stations for ±50 %, n ≈ 94 for ±20 % |
| **period-dependent peak deficit** | **STILL A DEFECT**, direction known, magnitude registered | `R_AMS` 0.808 (LN) vs 0.686 (EN) ⇒ **×1.096** (`docs/35` §5.4) | not resolvable — propagate as a caveat (`docs/43` §5.2) |
| **which quantity the MUSLE sum is** | **UNRESOLVED LABEL** — neither defect nor target | A1.9.1 (SWAT Ch. 4:1 calls this equation's output a sediment **yield**) | a written, cited answer — A1.9.3 resolver (1) |

**Clause-by-clause effect on A1.1's conjunction:**

- **Clause 2 — still NOT MET, and now split.** The LS *level* reclassifies into Π; the LS *shape*
  does not, and the C3.1 decision remains unmade. **This clause alone still forbids closure.**
- **Clause 3 — still NOT MET, upgraded to PARTIAL.** The three lenses of this adjudication did
  constitute an adversarial pass over `docs/35` §6.1 (falsified against its own source), `docs/42`
  §4.1–§4.2 (fit set CAL 13 → **CAL 8**; `k_min` 0.0096 → **0.0209 /km**) and this document's A1.3.4
  (comparison-basis artifact — A2.3). **`docs/41`'s C rows remain unaudited**, and `docs/42` G3.1 is
  measured incapable of auditing them: its minimum detectable class-C error is **≈ 4.2×** on the
  achievable fit set, against a revision of **×1.2043**.
- **Clause 4″ — still NOT ESTABLISHED**, unchanged. A1.9's resolver step (1) has not been done.
  **This pass deliberately declines to do it** (A2.6): it is research rather than adjudication, and
  the reading that would settle it favourably — reading B — is the one A1.9 refused *because* it
  flatters the result. It is not adopted here by the side door.

**Why CLOSED was available and was refused.** Closing today would require retiring a **third**
successive level clause (SDR → 4′ → 4″) and reading the accumulated retirements as a pass. `docs/40`
§8.1, A1.2 and A1.9.6 all say the same thing: **a retired gate is neither a pass nor a fail.**

---

## A2.3 Correction owed to **A1.3.4**: "short by 1.22 – 2.01×" is largely a comparison-basis artifact

A1.3.4 reported the simulated contrast **short of observation by 1.22 – 2.01×** (primary pair) and
**1.61 – 2.34×** (sensitivity pair). **The arithmetic is right and the comparison is not.** It sets a
**basin-total** simulated ratio against a **fleet-median tributary-station** observed ratio computed on
a **different day set** — three mismatches at once.

**Reproduction gates passed before the correction was accepted:** the lens reproduced this document's
own simulated basin ratios to 4 d.p. (**2.2915** primary, **3.9725** sensitivity, mass ledger
`exact = True`) and `docs/34` §3.1's observed estimator-(a) fleet median (**4.62**), so both sides are
the quantities the project already published.

**Repaired to like-for-like — same stations, same days, same estimator:**

| pair | est | n | OBS median | SIM median | obs / sim |
|---|---|---:|---:|---:|---:|
| primary | (a) | 6 | 4.620 | **4.903** | **0.9423** |
| primary | (b) all | 7 | 2.949 | **2.904** | **1.0154** |
| primary | (b) ok-only | 4 | 2.845 | 3.081 | 0.9232 |
| sensitivity | (a) | 4 | 9.320 | **4.212** | **2.2129** |
| sensitivity | (b) all | 7 | 4.650 | **4.998** | 0.9304 |
| sensitivity | (b) ok-only | 5 | 6.404 | 4.970 | 1.2887 |

**In three of six cells the model reproduces the observed ENSO contrast to within 8 %, and in five of
six to within 1.29×.** Repairing the basis moves the simulated number 2.2915 → 4.903 (est. a) or
2.904 (est. b) — **×2.14 / ×1.27**, of which the day set alone is **×1.69** — and that is essentially
the whole of the primary-pair gap.

**What this corrects, and what it does not.** It corrects the *comparison*, not the model: A1.3.4's
"the magnitude is short" must now be quoted as **"the basin-total-vs-station-median comparison was
short; like-for-like it is not"**. It does **not** license calling the contrast reproduced — the
period-differential is centred on 1 but is **not constant** (A2.2), and `docs/35` §5.4's **+9.6 %**
over-statement still applies to every simulated contrast (peak-corrected: **2.0908×** primary,
**3.6245×** sensitivity). A1.3.4 keeps its numbers and gains this pointer; nothing in it is deleted.

---

## A2.4 What this changes for C4 — added to A1.6, which otherwise stands unchanged

`docs/43` §3 is the full contract. The three items that belong in *this* document, because they modify
what A1.6 permits:

1. **A1.6's permission to "fit α and β on the 13-station calibration set" is superseded on the set,
   not on the permission.** The achievable set is **8** stations: `23127010` BORBUR-AUT, `22017010`
   BOCAS, `22017030` BOCAS, `24037390` CAPITANEJO, `26137110` BANANERA LA 6-909, `26127010` EL
   ALAMBRADO AUT, `24027030` NEMIZAQUE, `21197010` EL PROFUNDO. Five of the registered 13 have **no
   paired SSC + observed-Q day** in CAL 2012–14. Consequences, measured: fitted area **10.1 % → 5.4 %**
   of the basin; `k_min` **0.0096 → 0.0209 /km** (2.2× worse than `docs/42` assumed, **9.7×** worse
   than the all-18 guard that will judge the fit); surviving CAL-CAL nested pairs **3 → 1**.
2. **The parameter count is 2 free + 1 bounded, not 3 free.** Π (the level) is identifiable with
   SE = 0.465/√8 = **0.1644 ln = ±38 % at 95 %**; **β is identifiable** (SE 0.020, 95 % half-width
   0.039 against a band half-width of 0.10) **but physically confounded with the surface-runoff
   partition**; the **deposition coefficient is NOT identifiable** on this set and must be reported as
   a **bound**, never a value.
3. **A1.6 item 1 / `docs/42` G5 gains a second reason to be load-bearing.** A1.9.4 already showed the
   deposition-free α band (**6.83 – 8.73**) overlaps the reading-B α (**7.92 – 8.86**). A2 adds: since
   `k̂` will be a *weak* bound on the achievable set, **the named claim — an explicit transport sink,
   or the words "this model asserts SDR = 1.0 between hillslope and station" — is what carries the
   weight, not the number beside it.**

**Nothing in A1.6's eight prohibitions is relaxed by this amendment.** In particular: the
reclassification is **not** a licence to fit α to close a level gap (`docs/35` §6 RULE 0 unchanged) —
the level is a target because the method leaves it free, **not** because there is a gap of known size
to close. Per A1.9, **there is no gap of known size**.

---

## A2.5 Consequential corrections applied and owed

| item | status |
|---|---|
| `docs/40` §8.2's paste-ready corrections to §1 row 4, §2's `< 1` premise, §2's SDR = 0.15 / 0.05 requirement rows, §4's opening residual sizing, and §4 residual 3 | **APPLIED IN PLACE 2026-08-11** as strike-through + dated pointer — **A2.7** |
| A1.3.4's "short by 1.22 – 2.01× / 1.61 – 2.34×" | **CORRECTED by A2.3** (pointer added; A1.3.4 not rewritten) |
| `docs/42` §9 — three amendments (fit set CAL 8 + `k_min` 0.0209; the ARRANCAPLUMAS conflict decided explicitly; deposition reported as a bound, 2 free + 1 bounded) | **OWED — blocking on C4's start.** `docs/43` §3.1. Not this pass's file |
| A1.7 items 2 and 7 (`tests/test_sediment.py`; `notebooks/18` §6.4/§7 + `src/nbgen/make_nb18.py`) | **OWED**, unchanged |
| `docs/00_INDEX.md` — a row for `docs/43`, and its "Is stage C3 closed?" answer to point there | **OWED** — not this pass's file |

---

## A2.6 Direction disclosure, and what was NOT done

- **The change that would most flatter the project is again the one refused.** Adopting A1.9's reading
  B would convert the residual from "2.03 – 2.27× low" to "1.33 – 1.49× high" and make clause 4″
  evaluable. This amendment **declines to adopt it**, for A1.9's stated reason: it is unestablished,
  and it is the reading that helps.
- **The reclassification does not move a single number.** No level, no parameter, no convention, no
  `cp_revision`, no threshold, no gate. What changes is one **label** on one component of a residual,
  and the **owner** it is assigned to.
- **No gate was passed.** Clause 2 still fails, clause 3 still fails, clause 4″ is still not
  established. C3 is **OPEN**.
- **No frozen artifact was opened or written**: `sim_calibrated_v2/{h2e_drivers.npz,
  parameters_H2E.csv, q_gauge_H2E.npz}` untouched. **No simulation was run, no calibration launched,
  no headline number recomputed, nothing backdated, no git command issued.**
- **Files written by this pass:** `docs/43_c3_c4_gate.md`, this amendment plus the A2.7 in-place
  corrections in §1/§2/§4 of this document, and `docs/agents/journal_decide-c3-c4.md`. Nothing else —
  `docs/35`, `docs/40`, `docs/41`, `docs/42` and all code were **not** edited.
- **Gauge-referenced t/km²/yr yields remain embargoed** (`docs/23` §13.2).

---

## A2.7 The `docs/40` §8.2 corrections, applied in place

`docs/40` §8.2 flagged that this document would otherwise **keep asserting a retired gate from its
body**, where a reader who never reaches A1 would find it. A1.7 item 5 recorded the corrections rather
than applying them, under the "nothing above the line is rewritten" rule. Both concerns are satisfiable
at once, and this is how it was done:

**Method: strike-through with a dated pointer. Nothing is deleted.** Every original sentence remains
readable, marked `~~struck~~`, with the replacement text and the reason beside it. The record of what
was believed survives intact; the retired claim can no longer be quoted as live.

**Applied, five places:**

1. **§1's closure table, row 4** — the SDR clause struck and marked **RETIRED — see `docs/40`**, with
   `docs/40` §8.2's replacement text and a pointer that its successor clause 4′ was itself re-opened
   as **4″** (A1.1, A1.9). **`docs/40` §8.2's own replacement row 4′ is deliberately NOT pasted**, per
   that document's own §0.
2. **§2's "The implied delivery ratio, which is why this document says OPEN"** — the whole
   sub-section marked retired; *"So `SDR = outlet / gross` must be < 1"* struck and replaced with
   `docs/40` §8.2's wording (no upper bound of 1; Dunne et al. 1998's 1.3×; NEH's 1.7778); the
   "published expectation is roughly 0.05 – 0.30" struck as **uncited and retired in both
   directions**; the two-row ADR table relabelled and its verdicts struck.
3. **§2's requirement table** — the SDR = 0.30 / 0.15 / 0.05 rows struck, with a note that the 0.15
   and 0.05 rows **overstated the problem by 4 – 8×** (A1.2 consequence 2).
4. **§4's opening sizing** — *"the unexplained residual is 1.93 – 14.8×"* struck as derived entirely
   from the retired band, and pointed at A1.9's current form (**direction UNKNOWN**).
5. **§4 residual 3** — replaced with `docs/40` §8.2's wording, **except** its "1.59 – 2.74×" figure,
   which is **not** re-adopted because A1.9 withdrew the direction of exactly that quantity.

**§3, §5, §6, A1 and A1.9 are untouched.** The document's headline verdict line is untouched: it says
**OPEN** and that is still correct.

---

# AMENDMENT A3 (2026-08-12, after A2.7) — **THE C3.1 ENACTMENT.** The LS *formulation* is DECIDED on source grounds: **ADOPT-SOURCE**, `ls_formulation = buarque_2015_dg`. **No engine default moves here. C3 stays OPEN. C4.3 stays BLOCKED.**

Written by the `a3-enactment` agent (`docs/agents/journal_a3-enactment.md`) under the frozen
pre-registration **`docs/46_ls_preregistration.md`**, whose §4.2 decision rule is in force and
whose §7.3 item 5, §9's registration card and §9.1 item 3 all name **this amendment** — *"`docs/37`
§A3, dated, written by the C3.1 owner"* — as the single act that enacts the decision. This is
therefore **`docs/47` §6.1's B1 unblocking event**, and **not** the freeze of `docs/46`, **not**
`docs/51`, `docs/52` or `docs/53`, and **not** any read-only panel verdict.

**Nothing above this line is rewritten**, with the one exception that is itself part of this
amendment: **A3.3** applies the corrections `docs/46` §2.5.1 and §7.3 items 2–3 make *unconditional*
to §1, §2, §4, §5, A1.1, A1.4, A1.5 and A2.2 **in place**, in **A2.7's own pattern — strike-through
with a dated pointer, nothing deleted**. Every superseded sentence remains readable.

> **THE HEADLINE VERDICT DOES NOT MOVE. C3 was OPEN and stays OPEN.** What moves is that clause 2's
> *formulation* question — open since 2026-08-11 and named in A1.5 as *"the single highest-value open
> item in Phase C"* — now has a written, source-grounded answer. Clause 2 is still **NOT MET**,
> because the answer is **recorded** and not yet **exercised**, because the engine default has not
> moved, and because `docs/46` §8.2 item 6 holds that clause 2 also needs the *shape* decision:
> **settling LS is necessary and not sufficient.**

> **`docs/42` G9 disclosure, required in the same paragraph as any basin-scale statement:** at the
> adopted `C`, **66.53 % of the model's gross erosion — 199.29 of 299.54 Mt/yr — is upstream of no
> usable SSC station**; only **33.47 %** is; and **801.1 km of channel, including the whole
> Depresión Momposina, lies below the outlet-most SSC station** (`21237020` ARRANCAPLUMAS).

> **`docs/42` G4.2, required beside every `f_LS` in this amendment:** the LS **LEVEL** is
> **UNVALIDATED**, and adopting a *cited* formulation does not change that. See A3.1.4.

**An ordering record, cited because it belongs in the file and not only in a journal.**
`docs/agents/journal_c31-enactment.md` (2026-08-11) records that a **still earlier session took this
same task, reached this same decision, and did not write §A3**; a second attempt on 2026-08-12 was
interrupted mid-edit and left §1, §2, §4, §5 and A1 pointing at A3 subsections that did not exist.
This amendment is the one that lands. The decision has therefore now been reached **three times
independently** before being written — which is a fact about persistence, **not** a third
reproduction of any measurement, and it is recorded so that no reader mistakes it for one.

---

## A3.1 `ls_formulation` — the decision, and the `docs/46` §4.2 row it exercises

> ### THE DECISION
>
> | field | value |
> |---|---|
> | `ls_formulation` | **`buarque_2015_dg`** — `docs/46` §3.1's **`V4_dg`**: `V1` limiter at one DEM pixel + `V2b` eq.-14 **step** `m` + `V3` eq.-18 W&S-78 `S` + eq. 13's Desmet–Govers **finite-difference `L`** with `Xdir^m`. *"The source formulation read whole."* |
> | `f_LS`, **erosion-weighted — this is the one that decides** (`docs/46` §3.3) | **0.25146**; second independent erosion-weighted reproduction, by a different aggregation route, **0.2514648985839397** (`docs/46` §10 amendment 1 item 2, `docs/53` §2 gate G6) |
> | `f_LS`, area-weighted **PROXY** — reported beside it and **never** able to override it | **0.2446790094097074** (three independent reproductions; `docs/50`, and the `docs/46` §10 route 0.24467900940970733) |
> | `1/f_LS` | **3.976775630318937** (on the exact value, **3.9766981619750683**) |
> | `ln f_LS` | **−1.3804713478171018** |
> | measured proxy bias `f_ero`/`f_area` | **1.0277138223121463** — the proxy is **2.51 % low**, i.e. *in the model's favour* (`docs/47` §3.1 R7, independently 1.0278) |
> | basin gross hillslope erosion at the adopted point | **75.32347104056149 Mt/yr** of `V0`'s 299.5387088405831 (`docs/47` §4.3 engine re-run; absolute flux only — `docs/23` §13.2 embargo) |
> | `docs/46` §4.2 outcome row exercised | **ADOPT-SOURCE** |
> | grade of the **FORMULATION CHOICE** | **CITED** on all four levers |
> | grade of the **LS LEVEL** | **UNVALIDATED**, unchanged and unchangeable by this amendment |
> | status | **DETERMINED and RECORDED — not yet EXERCISABLE.** A3 does **not** propose the engine-default switch (A3.1.6, A3.5.1) |

**The sentence `docs/46` §4.4 item 1 requires, in the true form it gives, and not in the form the
original guarantee asked for:**

> **"This decision is recorded before any default was switched, and after the basin totals under
> every variant were already published in `docs/47` §4.3, `docs/49`, `docs/50` and `docs/51`."**

The original guarantee — *"recorded before any basin total under it was computed"* — is
**permanently unavailable to any session** and **is not claimed here**: 299.5387 (`V0`), 129.3840
(`V4`) and 75.3235 (`V4_dg`) Mt/yr were all on the record before this amendment opened. `docs/46`
§4.4 item 3 further warns that the collapse to a **binary** — the source read whole *versus* the
hybrid, worth **×1.7177284657599616** — makes the choice **easier** to make post-hoc, not harder.
That is exactly why the justification below is **a source reading with a grade, checkable against
four printed pages**, and cites no total.

### A3.1.1 The rule applied row by row — three of the four rows fail their own conditions

`docs/46` §4.2's outcome table is a **conjunction per row**. Taken in order, and each condition
checked against the artifact rather than a summary:

| row | its condition | verdict |
|---|---|---|
| **ADOPT-BAND** | *"≥ 1 lever CITED but ambiguous — i.e. **two admissible readings survive on the source text** … the existence of a second admissible reading, period, whatever the gap"* | **CONDITION ABSENT.** Every lever has a **single** admissible reading: the limiter on **two** independent sentences (printed pp. 94 and 98), `m` on eq. 14 p. 47 with *"onde `Sf` [%] é a declividade do pixel"* (corroborated p. 48's degrees-conversion note, which would be meaningless if `Sf` were already degrees), `S` on eq. 18 p. 48 attributed to Wischmeier & Smith 1978 (and a **third**, independent attribution on p. 47), `L` on eq. 13 p. 47 with `Xdir_k^m` in the denominator and the orthogonal/diagonal convention printed. §4.2's own first note says so: *"ADOPT-BAND is not currently triggered on any lever."* |
| **NEGATIVE — UNRESOLVED** | *"≥ 1 lever with no citable ground either way, **or** (R6) fires, **or** the source text cannot be obtained/verified"* | **ALL THREE DISJUNCTS FALSE.** No lever lacks citable ground (above). **(R6) does not fire** — `Sf` is slope **percent**, single admissible reading (`docs/46` §2.2 amendment (d), §9.1 item 2); the pre-committed NEGATIVE branch for the `m` lever **did not fire**. The source text is on disk at `data/raw/refs/buarque2015.pdf`, **9,646,521 bytes**, sha256 `3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037` — **MATCHING** `docs/38` §9.1's provenance card, LUME handle 10183/129875. §7.1's four triggers all fail. **A negative result is publishable in this project; a fabricated one is not.** |
| **RETAIN-OURS, discrepancy declared** | *— no §4.2 row grants it* | **INADMISSIBLE AS AN OUTCOME.** The licence it wants — keep `V0` *"because it is incumbent, not because it won"*, carrying the bracket — is precisely **NEGATIVE's** licence column, and NEGATIVE's condition is unmet. Its only other route is an item-2 deviation, and A3.1.2 finds none. `docs/46` §7.3 independently forbids *"treating the incumbent `V0` as **validated** because it survived by default"*. **"Ours keeps running for now" is a fact about the engine default (A3.5.1), not a §4.2 outcome.** |
| **ADOPT-SOURCE** | all four levers CITED (**met**, §4.2 item 5 as amended (d)); H-M's (R6) not triggered (**met**); the §3.3 exact re-run completed **and reported, including the stratified report** (**HALF met** — A3.1.6); §4.3's forbidden evidence untouched (**met**, A3.1.5) | **EXERCISED**, by **item 1 and by elimination**, and **not by preference**. Three of its four conjuncts are discharged; the fourth is discharged only in its *re-run* half, which is what makes the outcome **determined but not yet exercisable** (A3.1.6). |

**Which point, and why the hybrid is not a candidate.** `docs/46` §2.5.2 is frozen and in force:
with eq. 13 printed on p. 47 there is *"no admissible reading of Buarque in which `L` is our
point-rate form"*. So **×0.43194 is not a reading of the source at all** — it is the source's three
levers with **our** `L`, a **documented HYBRID** retained only because `docs/35` §9.3.1, this
document's §4 candidate 0 and `docs/43` §1.4 quote it and it must stay reproducible.
**Reproducibility is not candidacy.** §2.4's adoption rule is that *"the formulation is adopted
whole or not adopted"*, and `buarque_2015_dg` is the whole four-lever formulation with no lever
picked. `[0.25146, 0.43194]` is therefore **a POINT beside a documented hybrid** and **may not be
presented as an ADOPT-BAND band** (§4.2 note 2).

**§4.2 item 4 — *"ties break toward the lower LS level … a tie may not be broken by the basin
total"* — is satisfied vacuously and its ground is verified first-hand.** There is no tie on the
source text. But the ground is stronger than `docs/46` states: the source's own verdict appears on
**p. 98 as well as p. 121** — of his *already-capped* `L`, *"o valor máximo é grande e … pode fazer
com que as estimativas da erosão laminar do solo em áreas íngremes, como nos Andes, seja
**superestimado** (EPA, 2004)"*, with p. 121 adding *"erosão em massa … o que é incompatível com o
uso da MUSLE"*. **The source's author says his capped LS over-estimates Andean sheet erosion, and
our limiter is looser than his** — upslope area ≤ 1 km², i.e. unit contributing length to ≈ 10,870 m,
against his one pixel. Every direction the source itself points is **down**. A fidelity nuance that
also favours item 1: transposing the *method* (*"`L` ≤ one DEM pixel"*) at our 90 m gives a **302 ft**
cap, **inside** AH-703's tabulated range, whereas his literal 500 m = 1,640 ft would be outside it.

**And item 4 is not a licence to hunt the lowest published LS.** The independent RUSLE-handbook path
at ×0.206 (`docs/47` §4.1 finding 6) is **a different method**, not a reading of the source, and is
published area-weighted only. It is cited here **only** as the convergence result it is: two paths
sharing no formulation choice but the `L` form land within 19 % of each other and both sit ~4–5×
below production.

### A3.1.2 Item 2 — the deviation burden is the whole question, and **no candidate clears it**

`docs/46` §4.2 item 2 admits a deviation from the source *"only with its own written source
justification, naming a citable reason why the source's choice is wrong **for this basin**, dated,
**written before the resulting basin total is computed**"*, and rules out *"our terrain is steeper"*
*"unless a citation says the source's choice fails on steep terrain"*. Two things must be true of any
such candidate, and the second is now unsatisfiable in principle:

1. it must argue **against the source's choice and for ours**, in *our* direction; and
2. it must have been **written before the total** — which `docs/46` §4.4 records as permanently
   impossible now, since 129.3840 and 75.3235 Mt/yr are published. **The deviation route is
   therefore closed to every future session as well as to this one.** The default route needs no
   such justification; that asymmetry is item 1's, and it is registered, not invented here.

The only CITED/DERIVED material that could serve is `docs/47` §4.1's six findings. Walked in full:

| `docs/47` §4.1 finding | grade | direction |
|---|---|---|
| 1. *"A cap on slope length is REQUIRED"* (AH-703 p. 104) | CITED | **against ours** — 59.5 % of cells already exceed 400 ft and our `A_unit` reaches **35.6×** AH-703's outer tabulated bound |
| 2. *"Our specific cap value 1 km² is a citation defect"* — Montgomery & Dietrich measure channel-head source areas **2,700–12,000 m²** against our 1e6 (**150×** at Andean slopes, **24×** at the basin median), and *wetter* regions have **smaller** source areas while our basin is wetter than their wettest site | CITED, **contradicted** | **against ours** — `docs/47` §4.2 item 2 states flatly that *"×1.000 is not defensible"* |
| 3. *"The W&S-1978 `S` function was withdrawn by its own authors for steep slopes"* (Renard et al. 1991 p. 32; 2011 ch. 8 p. 142) | **CITED** | **the only item-2-shaped candidate on the record** — see below |
| 4. *"Our `m` is McCool-89 / AH-703 exactly, and AH-703 publishes `m` up to 0.71"* | CITED | **fails item 2** — see below |
| 5. *"The `L` form our production column uses is a point rate, not a cell average"* | DERIVED | **against ours** — the cell-average (D&G) form is the coherent one and our point form **over-states**; predicted head-cell ratio 0.58 against a measured **0.5807** |
| 6. The convergence result (Buarque path ×0.245 vs the independent RUSLE-handbook path ×0.206, within 19 %) | DERIVED + CITED | **against ours** |

**Finding 3 has exactly the shape item 2's worked example demands, and it still does not license
RETAIN-OURS**, for three separate reasons, each sufficient: it argues against **the source's** `S`,
not **for ours** — and ours (Moore & Burch, `n` = 1.3) is *equally* unvalidated above tan θ 0.50,
where 35.5 % of the basin's `S` signal sits (Schmidt et al. 2019; `docs/47` §4.2 item 1, O2); its
direction is **down**, because `V3` is the ×1.694054 **amplifier**, so it would put `f_LS` **below**
0.25146; and the variant it implies is **not registered in `docs/46` §3.1 and has no measured
`f_ero`**, so adopting it today would be adopting an **unmeasured** formulation. The standing
instruction forbids assembling it as a product of single-lever factors — **joint / product =
×1.347608646050708**; the levers do not multiply out.

**Finding 4 is the strongest-looking pro-ours row and it fails item 2 on the row's own citation.**
It cites **our** formula; it does not say the source's eq. 14 is wrong for this basin. It is
undercut twice: AH-703 pp. 105–106 makes `m` a **land-condition** parameter, and its rangeland /
low rill:interrill column returns **×0.5082** on this basin — essentially the source's own
**×0.5051** — so *the same citation read for THIS basin returns the SOURCE's level*; and the
"moderate" column we use is **our own unstated user choice** (`docs/47` §4.2 item 3, O4).

**Five of six findings point against ours; the sixth is a symmetric citation that item 2 does not
admit. There is no admissible item-2 justification on the record for keeping ours, so item 1's
default stands unrebutted.**

> **A NAMED RISK ON THE ADOPTED VALUE, recorded because it is real and because it is the kind of
> thing this project has reversed itself on before.** `docs/47` §4.2 item 5 — verified on disk at
> `docs/47`:369–371 — records that the shipping MGB-SED plugin (`github.com/LabHig-Ufes/MGB-SED` →
> `bin/formPRESED.exe`, 2025-09-10) contains a **run-time user choice of `S` factor**, the literal
> strings *"(0) standard method / (1) slope scaling method"*, plus a source→target DEM resolution
> rescaling our implementation does not have — so `docs/47` concludes that *"in the tool this
> project transposes, `S` is a user choice, **not a fixed part of the method**"*. If that were
> admitted as a **second admissible reading of the transposed method**, the `S` lever would trigger
> **ADOPT-BAND** and a band would be owed where this amendment records a point.
>
> **Why it does not change this outcome, and what it does change.** `docs/46` §1.2's read-out that
> **(R1) does not fire** is **frozen and in force**, and a session that believes a frozen rule is
> wrong *"journals the objection and follows the rule anyway"* (§10) — which is what is happening
> here. On the merits: the source of record is unambiguous **three times over** on printed pages 47
> and 48; the plugin is a **2025 artifact of a successor tool**, not the transposed source whose
> provenance card `docs/38` §9.1 carries; and H-S's own refutation clauses are (R7)/(R8) (field) and
> (R9) (a reading test on *our* side), none of which admits the code as a reading of Buarque.
> **But every branch of the objection points DOWN**: whether `S` stays at W&S (`f_LS` = 0.25146) or
> is treated as selectable (`f_LS` **lower still**), and whether the row is ADOPT-SOURCE or
> ADOPT-BAND, **nothing in it licenses RETAIN-OURS or NEGATIVE**, because neither requires nor
> produces a citable reason the source's choice is wrong for this basin **in the direction of ours**.
> So it is a live risk to the adopted **number** and to the **shape of the record** — it may mean a
> band is owed where a point is recorded — and **no risk at all to the elimination of `V0`**. A
> future session may raise it **only with the new variant measured first**, and never as a reason to
> keep the incumbent.

### A3.1.3 The supremacy objection — `docs/35` §9.3.2 item 1 names **three** levers, not four — adjudicated, and a `docs/35` §9 amendment is **OWED**

This is the strongest objection to the adopted **value** on the whole record, and it must not be
glided past. `docs/46` §0 says without qualification that it *"does not supersede `docs/35` §9.3 …
this document is **subordinate** to it: where the two disagree, **`docs/35` wins** and this file is
the bug."* Read on disk at `docs/35`:710–715, §9.3.2 item 1 defines the registered default outcome as

> *"the **source formulation is the registered default outcome** of C3.1: slope length limited to one
> DEM pixel, `m` stepped and capped at 0.5 (his eq. 14), `S` = Wischmeier & Smith 1978 (his eq.
> 18)."*

**Three levers. `L` is not named.** Read literally, frozen `docs/35`'s registered default is
therefore **`V4` = the hybrid**, `f_ero` **0.43194**, α reference 11.8 × 0.43194 = **5.096892** and
hard stop 35.4 × 0.43194 = **15.290676** — **not** the point this amendment adopts. And `docs/46`
§2.4's relabelling of `V4` as *"a documented hybrid, not the source formulation"*, with `V4_dg`
installed as *"the source formulation read whole"*, is precisely the species of disagreement §0
hands to `docs/35`. **Two of the three panellists raised this; the third missed it entirely.**

**Adjudicated as follows, on four grounds read on disk, and the adjudication is recorded as an
interpretation rather than a rewriting:**

1. **Item 1's own stated rationale is LEVEL fidelity, and the literal reading defeats it.** The
   clause's reason, in its own words, is that *"because MUSLE is **linear** in LS, an LS level that
   differs from the source's passes one-for-one into α and silently invalidates the §6.1 guard."*
   Keeping our point-rate `L` leaves exactly that discrepancy against the printed source —
   **×1.7177284657599616**, ln **0.5410027585442313** — so the literal enumeration defeats the
   clause's own purpose.
2. **The enumeration is an inventory of levers *then measured*, not a definition of the method.**
   `docs/35` §9.3.1, in the same frozen amendment at :700–702, **already records the `L` lever
   separately** — *"with the literal Desmet–Govers finite-difference `L` instead of our continuous
   form, a further ×0.790"* — so §9.3.2 item 1 cannot be read as an exhaustive definition that
   excludes a lever its own preceding subsection prices.
3. **The enumeration is already known defective on its face.** *"`m` **stepped and capped at 0.5**
   (his eq. 14)"* conflates **two different objects** — eq. 14's step function and `min(m, 0.5)` —
   and `docs/46` §7.3 item 2 records that this very label is **WRONG** and owed correction in five
   places, `docs/35` §9.3.1 among them. A sentence that mis-describes one lever cannot outrank the
   printed page it purports to summarise (A3.3.2).
4. **If a reader genuinely cannot tell which composition item 1 names, that is a TIE** — and §4.2
   item 4, *"ties break toward the lower LS level … a tie may not be broken by the basin total"*,
   returns `V4_dg` at 0.25146 anyway, on the source's own pp. 98/121 verdict and never on a total.

> **THE HONEST LIMIT OF THIS ADJUDICATION, and the branch it leaves open.** Grounds 1–4 are all
> arguments about what a frozen clause **meant**; §0's supremacy rule is about what it **says**.
> **A `docs/35` §9 amendment is therefore OWED** — dated, by `docs/35`'s own owner, and neither by
> `docs/46` nor by this amendment — recording that §9.3.2 item 1's three-lever enumeration is
> superseded by eq. 13's reading. **If `docs/35`'s owner declines it**, then `docs/35` wins on its
> literal text, this amendment's ADOPT-SOURCE at `V4_dg` is the bug, and the surviving outcome is
> **NEGATIVE — UNRESOLVED on a *documentary* rather than an evidentiary ground**, with `V0` retained
> **as incumbent and never as validated**, the bracket carried, and C4.3 still blocked. That branch
> is written here so that no downstream session can present A3.1's ADOPT-SOURCE as unconditional.
>
> **[⚠ A3.9, 2026-08-13 — THIS BRANCH IS CORRECTED AND CLOSED. Nothing above is deleted.]** The branch as written names an outcome **no governing document admits**: `docs/46` §4.2's NEGATIVE — UNRESOLVED row is a **closed disjunction** (≥ 1 lever with no citable ground either way · (R6) fires · the source text cannot be obtained/verified), and **A3.1.1 of this same amendment measures all three disjuncts FALSE**. A *documentary* ground is not in that disjunction, and a frozen row's entry conditions may not be extended by an amendment in another file. Separately, *"`V0` retained"* is an **engine-state fact (A3.5.1), not a §4.2 outcome** — the conflation A3.1.1's own RETAIN-OURS row expressly rejects. The correct characterisation is a **supremacy conflict between two frozen documents**, for their owners, not a third §4.2 outcome; and the gap between the two *fallbacks* (`V0` vs `docs/35` §9.3.2's registered three-lever default `V4`) is **×2.3151**, **not** the ×1.7177 POINT-vs-hybrid `L`-form lever. **AND THE TRIGGER DID NOT FIRE:** the owed `docs/35` §9 amendment (A3.7 row (a)) **arrived** — `docs/35` **§9.5, 2026-08-12**, written by `docs/35`'s own owner, re-registers the §6.1 α band at the adopted LS level and records *"ACT 1 and ACT 2 have now been executed"*. `docs/35`'s owner **did not decline**. See A3.9.
>
> **A second, related exposure, recorded rather than argued away.** `docs/46` §4.2 item 5's fourth
> lever came in by **amendment (d), dated 2026-08-11 — the same day as the freeze and after the
> ×0.25146 total was on the record** (`docs/47` §4.3). A hostile auditor can say the `L` lever was
> added to the CITED requirement by a session that already knew what adopting it costs, in the
> direction of the number now adopted. The answers available are that amendment (d) moves in the
> **restrictive** direction (requiring *more* to be CITED, not less) and that its stated ground is a
> printed page, not a total. Neither answer removes the exposure, and `docs/46` §4.4's own warning —
> that a binary is *easier* to make post-hoc — applies to this amendment with full force.

### A3.1.4 The grade — **four distinct propositions, four different grades**

Conflating these is the error `docs/46` §8.2 item 1 and §9.2 exist to prevent, and A1.6 item 3
already supplies half of it. Each is stated with the exact proposition it attaches to.

| # | proposition | grade |
|---|---|---|
| **(A)** | *"The adopted formulation is what Buarque (2015) prints, on all four levers"* | **CITED** — verbatim, page-numbered, single admissible reading, `Sf` units verified: limiter printed **pp. 94 + 98**, `m` eq. 14 printed **p. 47**, `S` eq. 18 printed **p. 48**, `L` eq. 13 printed **p. 47**. Excluded from this grade **by name**: `min(m, 0.5)`, which *"may NEVER be graded CITED — it is nobody's published formulation"* (`docs/46` §2.2). |
| **(B)** | *"`f_LS(buarque_2015_dg)` = 0.25146 erosion-weighted / 0.2446790094097074 area-weighted **on OUR terrain, OUR engine, at adopted defaults**"* | **DERIVED** on §4.1's own definition — *reproduced by arithmetic from a published definition, twice, independently.* Two erosion-weighted measurements and three area-weighted, each behind reproduction gates including the basin-erosion gate at **299.5387088405831 Mt/yr**. |
| **(C)** | *"The LS **LEVEL** is correct / validated / confirmed"* | **UNVALIDATED, AT ANY GRADE, AND UNCHANGED BY THIS ADOPTION.** `docs/42` **G4.2** stands. ***Cited is not validated*** (A1.6 item 3) and ***fitted is not validated either*** (`docs/43` §3.3 item 1). `docs/46` §9.2: *"Raising four levers to CITED raises their **provenance** grade and nothing else."* The mechanism is §8.1's: the design matrix has condition number **∞**, only **Π = α · f_vol · f_K · f_LS · C_mult · P · FG** is identifiable, so **no** calibration on **any** objective can separate the LS level — which is also why §4.3 rules a fit out as **zero** evidence, not weak evidence. |
| **(D)** | *"α = 11.8 (Williams 1975) is like-for-like with this 2-D contributing-area LS"* | **UNRESOLVED / NOT SETTLED, and no band is offered** (`docs/46` §1.0 residue 3, §9.2; `docs/47` §4.2 item 6, O4). Williams 1975 predates every 2-D contributing-area LS by two decades. **This bounds every number in A3.2 from above.** |

**`docs/46` §1.0 residue 1 stands unremoved and is not repaired by adoption:** both rows are the
source's **FORMULATION on OUR terrain data** — 90 m COP90 against his 500 m, Horn 3×3 slope against
his eq. 15 centred differences, our D8 routing, our URH mask. **Neither number is "his LS", and
adopting the formulation does not make it so.**

What (A) + (B) buy is exactly `docs/46` §8.3's one conclusion: *which formulation the engine uses,
on written source grounds, with a grade — and therefore what the decomposition of Π is, and what α̂
has to be multiplied by to be quoted against a published α.* **Bookkeeping and provenance.**

### A3.1.5 What `docs/46` §4.3 forbids, and what was refused

Each of the following was available and **was not used as evidence** for this decision:

- **the basin total, the outlet anchors (144–184 Mt/yr), and the distance between them.** The
  75.32347104056149 Mt/yr figure appears in A3.1 and A3.3.1 **only as the reproduction of an already
  published engine re-run** (`docs/47` §4.3), and it entered no step of the reasoning. The fact that
  the adopted point lands **furthest** from the anchors is **not** counted as evidence in either
  direction — `docs/35` §9.3.5's *"an unattractive total is not evidence against the source
  formulation"* binds **symmetrically**;
- **the retired "mountainous LS 2–10" band**, and its coincidence with the source formulation's
  7.262 median, which `docs/35` §9.3.5 already forbids as evidence and which is a *fingerprint*;
- **the retired SDR band 0.05–0.30** and every implied-SDR arithmetic built on it. This is why A3.3.1
  declines to re-derive §2's and A1.4's struck ADR numbers rather than correcting them;
- **any α band.** A3.2's numbers were computed **after** the choice was fixed, as §4.2 item 3's
  reporting obligation, and **passed and failed nothing**. `docs/47` §3.2 independently falsifies
  `docs/35` §6.1's band as a sufficient guard: **185 of 426** published pairs STOP, and 97.7 % land
  inside 5.9–23.6 *because the source's own search prior contains it*;
- **any C4 fit, at any stage.** No fit was run, no `KGE_ln` was evaluated against `docs/45` §2.1's
  box, and **no α̂ — provisional or otherwise — was produced or quoted**;
- **`check_musle_parameters`'s verdict.**

**No new band was introduced anywhere in this amendment, and no materiality bar was reconstructed
from anything.** `docs/52`'s striking of `docs/46`'s 0.1644 ln bar is respected: nothing here
compares a difference to a threshold. **An uncited band cannot pass a gate any more than it can fail
one** — three have been retired on that rule and this amendment does not add a fourth.

### A3.1.6 **Reachable ≠ exercised** — the three deliverables between this decision and the engine

`docs/46` §4.2's third note is explicit, and this amendment is bound by it:

> *"**Reachable ≠ exercised.** No outcome in this table has been taken. §3.3's **full stratified
> report** is not discharged — elevation strata exist for every variant, **slope terciles do not**,
> and the per-station erosion-weighted `LS̄` exists only as ratios (`docs/47` §4.4) — and it is
> required before ADOPT-SOURCE is **exercised**, though not before this freeze."*

ADOPT-SOURCE's third conjunct is *"the §3.3 exact re-run completed **AND REPORTED, INCLUDING THE
STRATIFIED REPORT**"*. **The re-run half is discharged** — twice reproduced erosion-weighted, three
times area-weighted. **The reporting half is not.** Three named deliverables stand between this
decision and any engine-default proposal:

1. **§3.3's missing stratified report.** Measured this run: **slope terciles do not exist** for any
   variant — a grep across `docs/`, `scripts/` and `src/` returns **only documents saying they are
   owed** (`docs/46`, `docs/49`, `docs/50`, `docs/51` and agent journals), and **no artifact**. The
   **elevation** strata *do* exist for `V4_dg` (`f_area` 0.3720729826 lowland < 200 m ·
   0.2491459900 mid 200–1000 m · 0.2408698821 Andean > 1000 m — **no stratum reverses**, which is a
   §3.3 *reporting* fact and **not** a ground for the choice). And the **per-station erosion-weighted
   `LS̄` exists only as RATIOS** (`docs/47` §4.4), not as the **levels** `docs/42` G4.1 reads.
2. **`docs/46` §2.3's H-S field clause, (R7)/(R8) items 2 and 3** — the per-station erosion-weighted
   factor dispersion reported beside `docs/47` §4.4's 0.0769 / 0.0868, and the stratified `S`
   factors printed beside the basin **1.714** with the spread shown. This is **the one hypothesis in
   `docs/46` §2 that was never read out** (§1.2, §9's card, §10's closing note). Item 1 of the clause
   is DERIVED from the two published formulas alone — the `S` ratio field spans ≈ 0.975–3.81 and is
   **non-monotone**, so `S` is not a scalar — but items 2 and 3 do not exist on our slope field.
3. **A committed, gated `V4_dg` column — the adopted formulation is not engine-readable anywhere.**
   Measured on disk this run: `data/processed/urh_ls2d_variants.csv`'s header is
   `mini,urh,n_cells,area_km2,area_frac,V0_ours_2026_08,V1_lim_pixel,V2a_m_cap05,V2b_m_step_eq14,V3_s_ws78,V4_buarque_2015,V4p_buarque_2015_cap,V5_L_dg96_fd`
   — **there is no `V4_dg` column**; `docs/53` §8 built it in a **scratchpad** only, the loss mode
   `docs/00` §6 names. And `data/processed/urh_ls2d.csv` carries only `ls2d`, `ls2d_hs`,
   `ls2d_mb86`, `ls2d_dg96` — the last being **Defect B's confounded column**, not `V4_dg` — and
   **may not be overwritten** (`docs/46` §3.1's registered hard requirement, §5's immovables).
   So `docs/46` §3.1's requirement that *"every variant is reachable **by name**"* currently
   **fails for exactly the variant ADOPT-SOURCE adopts**, the §3.3 re-run cannot be *reported* in
   the registered form, and **no default can be switched by name**. Materialising the column in a
   **new** committed product is also what would give the lower endpoint a **third** erosion-weighted
   reproduction (`docs/51` §7 item 7).

> **Therefore, stated so it cannot be over-read: the §4.2 outcome is DETERMINED and RECORDED, and it
> is NOT YET EXERCISABLE. This amendment does NOT propose the engine-default switch** — which is
> consistent with what ADOPT-SOURCE licenses in its own words, *"**proposing** the adopted variant as
> the engine default in a **separate**, dated amendment"*. **A3 records; it proposes nothing and
> flips nothing** (A3.5.1).
>
> **A governance gap, named rather than papered over.** Strictly, **no §4.2 row's condition set is
> fully satisfied today**, so a purist can say the rule returns nothing and that
> *"ADOPT-SOURCE, determined but not exercisable"* is a **fifth outcome** the table does not
> contain. The answer this amendment gives is that §4.2's own third note draws exactly the
> reachable/exercised distinction relied on here and puts the stratified report on the **exercise**
> step; that the only other candidate row, NEGATIVE, fails **affirmatively** on its own evidentiary
> condition; and that §7.3 forbids treating `V0` as validated by default. **A reader who thinks an
> unexercisable outcome is no outcome is not being unreasonable, and `docs/46` does not close this
> gap.** Recorded as an open item (A3.7).

---

## A3.2 The α band **RESCALED** at the adopted `f_LS` (`docs/46` §4.2 item 3)

**The source of the un-rescaled numbers, read directly from `docs/35` §6.1 rather than from a
summary:** reference **α = 11.8** (Williams 1975); *"expected"* band **5.9 – 23.6** (0.5× – 2×
Williams); *"watch"* **23.6 – 35.4**; **HARD STOP α > 35.4** (3×); **HARD STOP α < 3.9** (⅓ ×
Williams, i.e. 11.8/3 = 3.9333 — and this **3.9 is not itself a rescaled LS number**, a check worth
making because 3.9 coincides numerically with the superseded 11.8 × 0.333).

**Arithmetic, computed with `python3.10` this run at full precision, on the published factors. The
erosion-weighted column decides (`docs/46` §3.3); the area-weighted proxy is printed beside it and
can never override it.**

| quantity | `f_ero` = **0.25146** (registered) | on the exact reproduction **0.2514648985839397** | area proxy **0.2446790094097074** |
|---|---|---|---|
| lower hard stop `3.9 · f` | **0.9806940000000001** | 0.9807131044773649 | 0.9542481366978589 |
| expected band, low edge `5.9 · f` | **1.4836140000000002** | 1.4836429016452444 | 1.443606155517274 |
| **α reference `11.8 · f`** | **2.9672280000000004** | 2.9672858032904887 | 2.887212311034548 |
| expected band, high edge `23.6 · f` | **5.934456000000001** | 5.9345716065809775 | 5.774424622069096 |
| **upper hard stop `35.4 · f`** | **8.901684** | 8.901857409871466 | 8.661636933103642 |
| `docs/45` §2.1 box floor `2.0 · f` | **0.50292** | 0.5029297971678794 | 0.4893580188194148 |
| `docs/45` §2.1 box ceiling `30.0 · f` | **7.543800000000001** | 7.543946957518192 | 7.3403702822912225 |
| `1/f` | **3.976775630318937** | 3.9766981619750683 | 4.08698728351287 |
| `ln f` | **−1.3804713478171018** | | |

These reproduce `docs/46` §1.0's lower-end column **exactly** (α reference 2.967; band 1.484 … 5.935;
hard stop 8.902). Two further checks: `docs/45`'s 5 %-of-box rail band **3.40 · f = 0.8549640000000001**;
and the area-basis rescaler `docs/46` §4.2 item 3 literally names,
`mean(LS_ours)/mean(LS_source)` = 39.812 / 9.741 = **4.087054717174828**, agrees with `1/f_area` =
4.08698728351287 to 5 s.f. — but **`f_ero` decides**, so the operative rescaler is **3.976775630318937**.

**WHAT THE COLLAPSE DOES.** The published *interval* collapses to a **point**: the α reference was
registered as **2.967 – 5.097** (11.8 × [0.25146, 0.43194]) and the hard stop as **8.902 – 15.291**;
at the adopted point they are the single numbers **2.9672280000000004** and **8.901684**. **The ln
width 0.5410027585442313 does not disappear as uncertainty — it is re-labelled as what it is, the
`L`-form lever** between the source read whole and the retained hybrid (`docs/46` §1.0, §2.5.2). For
contrast, the hybrid's column, retained only for reproducibility: 11.8 × 0.43194 = **5.096892**,
35.4 × 0.43194 = **15.290676**, `1/f` = **2.315136361531694**.

**DIRECTION, STATED SO IT CANNOT BE MIS-READ** (`docs/47` §6.2 item 1: no α̂ is compared to 3.9, 35.4
or a box edge without `f_LS` and its grade in the same table):

- **Today**, the engine column is `ls2d_column = 'ls2d_hs'` and `f_LS` = 1.000 as `docs/45`'s
  parameter card fixes it. **Any α fitted on TODAY's LS field must be read against 2.9672 /
  1.4836 – 5.9345 / 8.9017**, not against 11.8 / 5.9 – 23.6 / 35.4. Equivalently, any α̂ obtained at
  the `V0` level must be **multiplied by 3.976775630318937** to be quotable against a published α.
- **Once the default is switched** (a separate act — A3.5.1), the engine's LS *is* the source's, the
  factor between the engine LS and the LS the published α was paired with becomes **1.000 by
  construction**, and the published numbers apply **un-rescaled**.
- **Both statements are the same arithmetic in two coordinates.** What may never happen is quoting
  an α without naming **which LS column it was fitted on**.

> **AN ADJUDICATION ON WHETHER ITEM 3 EVEN ATTACHES, because the panel split on it.** Read narrowly,
> §4.2 item 3's antecedent is *"a deviation adopted under (2)"*, and ADOPT-SOURCE is **item 1's
> default, not a deviation** — so on that reading the engine's LS after adoption sits *at* the level
> α = 11.8 was paired with and `docs/35` §6.1's numbers would stand unrescaled. **The narrow reading
> is textually right about item 3's antecedent and is overridden anyway**, by two frozen sites that
> name the obligation unconditionally for this outcome: §4.2's **ADOPT-SOURCE licence cell** (*"α
> band rescaled per item 3"*) and §7.3 item 5's content list for **this amendment**. The obligation
> attaches, and both coordinates are printed above. **The narrow reading may not be used as
> reassurance** in any case, for two measured reasons: proposition (D) — α = 11.8's like-for-likeness
> with any 2-D contributing-area LS is **NOT SETTLED, no band offered** — and `docs/47` §3.2's
> falsification of the band as a sufficient guard.

> **THE CEILING ON ALL OF IT, carried and not softened.** Every number in this subsection is
> **BOOKKEEPING**. Per `docs/46` §8.2 item 2, a rescaled α reference is *"a statement about the
> **pairing** of α with an LS, not about α"*. **None of it passes or fails anything.** §4.3 forbids
> using any α band as evidence in the LS decision and this amendment used none. And
> `docs/46` §1.0 residue 3 / `docs/47` §4.2 item 6 bound it all from above: **α = 11.8 predates
> every 2-D contributing-area LS by two decades and its like-for-likeness is NOT SETTLED, with no
> band offered.**

**A precision note, recorded so a later reader does not read a defect into it.** The registered
hybrid load **129.3840 Mt/yr** divided by the basin total 299.5387088405831 gives
**0.43194417342854735**, so *"0.43194"* is the 5 s.f. rounding of the engine's `f_ero(V4)` and
299.5387088405831 × 0.43194 = 129.38274989660147. The two are consistent to the precision each is
printed at; **129.3840 is the engine re-run and 0.43194 is its rounded factor**, and neither is
superseded by the other.

---

## A3.3 Corrections to **this document's own text**, applied in place

`docs/46` §2.5.1 and §7.3 items **2 and 3** make these **unconditional** — the ground is *"a landed
measurement, **not** the survival of a hypothesis"* — and §9.1 item 3 names this document by name,
because it *"carries the closure conjunction whose clause 2 the adoption discharges, and whose §1
table and §4 candidate 0 still print '2.37× – 3.00×' — one amendment does both jobs."*

**Method: A2.7's, unchanged. Strike-through with a dated pointer. NOTHING IS DELETED.** Every
original sentence remains readable, marked `~~struck~~`, with the replacement beside it and a
pointer to the subsection that carries the reasoning. The record of what was believed survives
intact; the superseded number can no longer be quoted as live.

### A3.3.1 The bracket — *"2.37× – 3.00×"* and *"×0.333 – ×0.421"* are SUPERSEDED BY MEASUREMENT

**What replaces them, registered at `docs/46` §1.0 from `docs/47` §4.3's engine re-runs:**

| superseded | registered |
|---|---|
| lower end ×0.333 | **×0.25146** ero · ×0.2446790094097074 area — and ×0.333 is **REFUTED**, not merely superseded (`docs/47` §3.1 R6: it is 0.421 × 0.790, and ×0.790 is **two levers measured on the wrong column**) |
| upper end ×0.421 | **×0.43194** ero · ~~×0.421475~~ → **×0.42136300143291305** area (**A3.3.4**, 2026-08-12 — `0.421475` was the *engine URH-fraction* area support, not §3.3's) (`V4`, the documented **hybrid**) |
| `1/f_LS` = 2.37× – 3.00× | **2.3151× – 3.9768×**, and at the adopted POINT the single figure **3.976775630318937×** |
| ln width 0.2345 | **0.5410027585442313** — 2.31× wider, and it is the **`L`-form lever**, not an uncertainty |
| the isolated `L`-form factor ×0.790 | **×0.76983** on the `ls2d_hs` basis; the published ×0.790 was **two levers**, not one (`docs/50`, `docs/46` §1.1) |

**Applied, twelve places in this document.** Nine were applied in the pass of 2026-08-12 that this
amendment completes; **three further live sites were found by grep in this pass and are corrected
here**, and they are named separately because a reader auditing whether the enactment travelled
needs to know the list was not complete on the first attempt:

1. **§1's closure table, row 2** — the *"2.37× – 3.00×"* struck, with the registered bracket, the
   adopted point, and the note that **the clause stays NOT MET**.
2. **§2's gate-(b) CONDITIONAL blockquote** — the bracket struck **and its base too**: the 248.730
   Mt/yr base is itself superseded by A1.3's **299.5387088405831 Mt/yr**, so the correct engine
   figures are **129.3840 Mt/yr** (`V4`) and **75.3235 Mt/yr** (`V4_dg`), **engine re-runs, not
   proxies**. The struck ADR arithmetic is **not** re-derived — the SDR band is retired (`docs/40`,
   A1.2) and `docs/46` §4.3 forbids the anchors as evidence in the LS decision.
3. **§4's opening sizing** — *"a further 2.37× – 3.00×"* struck.
4. **§4 candidate 0's lever table** — the joint row's ×0.421 struck; the `m` row's factor and label
   struck (A3.3.2).
5. **§4 candidate 0's *"two consequences"* bullets** — the level bullet's 104.8 / 82.8 Mt/yr struck
   on **both** the base and the factors; the **proxy caveat discharged as MEASURED**, and it errs
   **in the model's favour**: `f_ero`/`f_area` = **1.0277138223121463**, 2.51 % low. The α bullet's
   four numbers struck and pointed at A3.2.
6. **§4 candidate 0's RESOLVER paragraph** — recorded as **EXECUTED**, with what remains owed
   (A3.1.6).
7. **§4 residual 3, the wrong-way-terms paragraph** — the bracket struck.
8. **§5's α-band trap, item 1** — the corrected expected band substituted, with the reason the
   *"6.83 – 8.73 lands inside it"* claim is **not** re-stated as a finding: `docs/47` §2.5 C1 records
   that 6.83 – 8.73 is `11.8 × {144,184} / 248.730`, i.e. at the **prior** `C`; at the adopted `C`
   the deposition-free band is 5.67 – 7.25, and C1's correction is owed to `docs/43` §3.4. **The
   trap itself survives unqualified**: the α band is not a sufficient guard, `docs/42` **G5** is.
9. **A1.1's revised conjunction, clause 2** — the bracket struck; clause 2 restated as **still NOT
   MET** for the three reasons of A3.5.2.
10. **A1.4's *"candidate 0 still points the other way"* paragraph** — the 99.8 – 126.1 Mt/yr range
    superseded by the exact re-runs; the ADR and Leg-A numbers **not** re-derived (A1.9 withdrew the
    direction; §4.3 forbids the anchors).
11. **A1.5's candidate-0 restatement** — marked **DECIDED but NOT CLOSED**, with the ADOPT-SOURCE
    record and the three deliverables.
12. **A2.2's LS-shape row** — the exact erosion-weighted factors substituted (limiter 0.362435 ·
    `m` **cap** 0.517480 · `m` **eq.-14 step** 0.522043 · `S` 1.694054, joint `V4` 0.431944, source
    read whole `V4_dg` 0.25146), with **joint / product = ×1.347608646050708** and the note that
    **there are FOUR levers, not three**.

> **THREE LIVE SITES THE EARLIER PASS MISSED, found by grep in this pass and corrected here.** They
> are listed openly because *"treat the list as a starting point, not as complete"* is the only safe
> way to do this kind of correction, and because the miss is itself evidence for that rule:
>
> - **§4 candidate 0's *"DO NOT stack"* paragraph** — *"an LS that is ~~2.4 – 3.0×~~ too high for its
>   own α"*, the **rounded** form of the same superseded bracket, still live. Corrected.
> - **A1.5's *"What would close C3"* paragraph** — *"the LS correction lowers the model by
>   ~~2.4 – 3.0×~~ while clause 4′ asks for 1.03 – 2.27× more"*, still live. Corrected — and the
>   correction **widens** the opposition between clauses 2 and 4′ rather than narrowing it.
> - **§4 candidate 0's interaction identity** — *"(0.502 × 1.714 × 0.351 = 0.302 ≠ the joint
>   0.421)"*, a live use of ×0.502 with no label pointer. Corrected with pointers to A3.3.1/A3.3.2
>   and with the exact erosion-weighted arithmetic printed: **0.362435 × 0.522043 × 1.694054 =
>   0.3205262902296241 ≠ the joint 0.431944** (with the **cap** instead, 0.362435 × 0.517480 ×
>   1.694054 = **0.3177246791318452**). **The claim the sentence makes — that the levers interact
>   and no single one is "the" cause — is unchanged and correct.**
>
> **STANDING INSTRUCTION, obeyed throughout** (`docs/46` §2.4): **never quote a product of
> single-lever factors as the joint factor.** Measured **joint / product = ×1.347608646050708**.

### A3.3.2 The `m` row's label — *"his eq. 14, step function hard-capped at 0.5"* is **WRONG**, and there are **two objects**

`docs/46` §7.3 item 2 makes this correction **unconditional** — *"the label is wrong regardless of
the size of the difference"* — and names §4 candidate 0 of this document as one of its five sites.
**Corrected here, with both objects kept named and distinct and both factors printed:**

| object | what it is | factor, area-weighted | factor, **erosion-weighted** | may it be graded CITED? |
|---|---|---|---|---|
| **Buarque eq. 14** — `V2b`, `m_step_eq14` | a **STEP function**, printed p. 47 verbatim: `m` = **0.2** (`Sf` < 1 %) / **0.3** (1 ≤ `Sf` < 3) / **0.4** (3 ≤ `Sf` < 5) / **0.5** (`Sf` ≥ 5), *"onde `Sf` [%] é a declividade do pixel"* — `Sf` is slope **PERCENT**, corroborated p. 48's *"sendo θ o valor de `Sf` em graus"* | **×0.505092** | **×0.522043** | **YES — CITED.** It is the adopted lever. |
| **the cap** — `V2a`, `m_cap05` | `min(m_continuous, 0.5)` | **×0.502472** | **×0.517480** | **NEVER.** *"It is nobody's published formulation"* (`docs/46` §2.2). |

**So the ×0.502 that this document printed for years is the CAP, not eq. 14** — and the difference
between the two objects is **Defect A**, measured **×1.005212 area-weighted / ×1.008878
erosion-weighted** and therefore **IMMATERIAL in magnitude** (`docs/49`, `docs/46` §1.1). **The
label correction does not depend on that**: `min(m, 0.5)` is a cap on a continuous McCool-89 `m` and
eq. 14 is a four-branch step on slope percent; they are different objects, one is citable and one is
not, and conflating them is what let `min(m, 0.5)` be described as *"his eq. 14"* in five documents.
**H-M's (R6) does not fire**: `Sf` has a single admissible reading, so the pre-committed NEGATIVE
branch for the `m` lever **did not fire** (`docs/46` §9.1 item 2).

### A3.3.3 The other four mislabel sites belong to other owners and were **NOT touched**

`docs/46` §7.3 item 2's five sites are `docs/35` §9.3.1, **`docs/37` §4 candidate 0** (corrected in
A3.3.2), `docs/43` §1.4, `src/nbgen/make_nb18.py` and `src/nbgen/make_nb19.py`; item 3's list adds
`docs/45` §2.1 and this document's §1 table. **Only this document was edited.** The remaining four
mislabel sites and the `docs/45` §2.1 re-derivation are **owed and are being enacted in parallel by
other agents in this same run** — see A3.7. They are recorded here as **owed, dated, and never as
silent edits**, which is the form `docs/46` §7.3 requires.

### A3.3.4 `f_area(V4)` — this document printed **0.421475**, which is a *different area support*. Corrected to **0.42136300143291305**

**Owning records:** `docs/46` **§10 amendment 2** (2026-08-12) and `docs/51` **§9 amendment 1**
(2026-08-12). This subsection **imports no number from a document that does not own it** — the two
values below were **independently recomputed** by the `defect-45-residual` session
(`docs/agents/journal_defect-45-residual.md`) from `data/processed/urh_ls2d_variants.csv`,
`urh_fractions.csv`, `minibacias.csv` and the three LS JSON artifacts, read-only, all SHA-256'd
unchanged after. **`f_ero` is untouched, so nothing this document decides moves** (`docs/46` §3.3
ground **G-ii**: *"`f_ero` decides; `f_area` is reported beside it, always, and can never override
it"*).

**Sites corrected in place:** §4 candidate 0's lever table, joint row (:207); A3.3.1's replacement
table, upper-end row (:1790). **Nothing is deleted** — both originals stay readable inside
`~~…~~`.

**Why 0.42136300143291305 and not 0.421475 — the definition selects the support.** `docs/46` §3.3
(frozen) defines the proxy as *"basin **area-weighted mean** of LS(V) / basin area-weighted mean of
LS(V0)"*, and `docs/46` §1 fixes what "basin" means there: *"on all **30,235,916** basin cells at
90 m, with a harness that reproduces our own `ls2d_hs` area-weighted mean **39.812** bitwise."* That
is the **per-cell DEM pass**, 256,702.3554292511 km². Hence
`f_area(V4)` = 16.775413430326214 / 39.812260149274394 = **0.42136300143291305**;
`1/f_area(V4)` = **2.3732506095678505**.

**Every plausible support, recomputed here, with `docs/47` §3.1 **R7**'s independently measured
proxy bias 1.0251 as the discriminator** (`f_ero(V4)` = **0.43194417543884817**, unchanged):

| support / weighting | `f_area(V4)` | `f_ero/f_area` | \|d\| vs R7 1.0251 | inside R7's own 4-d.p. rounding interval [1.02505, 1.02515]? |
|---|---:|---:|---:|---|
| **per-cell basin, 30,235,916 cells — §3.3's quantity** | **0.42136300143291305** | **1.025111777659529** | **1.178e-05** | **YES** |
| same, `ls2d_defect_b.json:decomposition.V4_over_V0` (independent script) | 0.42136300143291344 | 1.0251117777 | 1.178e-05 | YES |
| same, recomposed from the three elevation strata | 0.4213630014329133 | 1.0251117777 | 1.178e-05 | YES |
| `urh_ls2d_variants.csv` weighted by `n_cells` | 0.42136472954221804 | 1.0251075735 | 7.573e-06 | YES |
| `urh_ls2d_variants.csv` weighted by `area_km2` | 0.4213519856784954 | 1.0251385780 | 3.858e-05 | YES |
| `urh_ls2d_variants.csv` weighted by `area_frac` | 0.42161856467208547 | 1.0244904082 | 6.096e-04 | **NO** |
| **engine `urh_fractions.csv`×`minibacias.csv` areas, 32,782 units, 257,096.93 km²** — *what this document printed* | **0.4214751420286394** | **1.0248390293193077** | **2.610e-04** | **NO** |

**The arithmetic, printed rather than asserted** (`docs/46` §2.0 ground **G-iv** — the exact ratio at
full precision with a stated licence, never compared to a threshold):
`0.43194417543884817 / 0.42136300143291305` = **1.025111777659529**, |d| = **1.1777659529199624e-05**;
`0.43194417543884817 / 0.4214751420286394` = **1.0248390293193077**, |d| = **2.609706806921963e-04**.
**The corrected value is 22.158110450144004× closer to R7**, and the value this document printed is
the only *area* support that R7's own rounding interval **excludes**. The gap between the two is
**2.661377371648382e-04** relative / **2.661023287994224e-04 ln**.

**What R7 can and cannot decide, stated rather than glossed.** Printed to four decimals, R7 cannot
separate the three reconstructions of the per-cell support from the two URH-table area weightings —
all five agree with it to ≤ 3.9e-05 — but it **rejects the engine support outright**, at 5.2× the
half-width of its own rounding. *(It also rejects `area_frac`, which is not an area weight at all:
that column sums to 8,672, weighting every minibacia equally regardless of size. It is listed only
so the search is auditable.)* **So the definition selects, and R7 confirms:** `docs/46` §3.3 plus
§1's cell-pass disclosure pick 0.42136300143291305 out of the near-neighbours, and R7 independently
rules out the number this document had been printing.

**What 0.421475 actually is — and it is not an arithmetic error.** It is the engine's own
URH-fraction area support (`ls_defect_a.json:variants.V4_buarque_2015.f_area_urhfrac_areas`),
**rebuilt independently here from `urh_fractions.csv` × `minibacias.csv` and reproduced to all 16
digits, with the same 257,096.93 km² basin total** — against the DEM cell pass's 256,702.36 km².
`load_geometry` itself warns that its two candidate area sources *"differ by more than 5 % on 12.9 %
of cells."* So **0.421475 is a correctly computed quantity on a different support, correctly named
in its own JSON key — it is simply not §3.3's `f_area`**, and no artifact needs editing.

**Not corrected, because they are already right** — stated so nothing is over-corrected:
- the **DG / lower endpoint** `f_area(V4_dg)` = **0.2446790094097074** and A3.3.1's `×0.2446790094097074 area`
  are already on the registered support. Control, recomputed here:
  `0.2514648985839397 / 0.2446790094097074` = **1.0277338427624152** against R7's DG figure 1.0278,
  |d| = **6.615723758485181e-05**. **Only the upper end was on the wrong support.**
- **every erosion-weighted number in this document**, including A3.2's whole α rescaling table,
  A3.3.1's `1/f_LS` = 2.3151× – 3.9768×, 3.976775630318937× at the adopted POINT, the ln width
  0.5410027585442313, the loads 129.3840 / 75.32347104056149 Mt/yr, the 299.5387088405831 Mt/yr
  gate, joint/product ×1.347608646050708, and A3.8's reproduction block — `f_ero` does not move.
- the proxy-bias figure **1.0277138223121463** at :264, :1392, :1812 and A3.8:2244 is the **DG**
  endpoint (`0.25146 / 0.2446790094097074`) and is on the registered support already.
- the rounded **×0.421** strings elsewhere in this document are the historic published proxy, already
  struck or pointered by A3.3.1; **0.42136300143291305 rounds to 0.421 at three significant figures**,
  so they are not additionally wrong and are left exactly as they stand.

**Reproduce:**

```
python3.10 -c "
import json
s=json.load(open('data/processed/ls2d_variants_summary.json'))
a=json.load(open('data/processed/ls_defect_a.json'))
v0=s['variants']['V0_ours_2026_08']['area_wtd_mean']; v4=s['variants']['V4_buarque_2015']['area_wtd_mean']
fe=a['variants']['V4_buarque_2015']['f_ero']; fu=a['variants']['V4_buarque_2015']['f_area_urhfrac_areas']
print(repr(v4/v0), repr(v0/v4)); print(repr(fe/(v4/v0)), repr(fe/fu))
print(repr(abs(fe/(v4/v0)-1.0251)), repr(abs(fe/fu-1.0251)))
"
0.42136300143291305  2.3732506095678505
1.025111777659529    1.0248390293193077
1.1777659529199624e-05   2.609706806921963e-04
```

**Disclosure for A3.3.4.** No engine default was changed; no data product was regenerated or
hand-edited; no fit, calibration or simulation was run; no α̂ is quoted; no materiality bar is
invoked, rescaled or reconstructed (`docs/46` §2.0's striking stands); no git command was run. The
`docs/23` §13.2 yield embargo is in force — no t/km²/yr appears here. `urh_ls2d_variants.csv`
(sha256 `81d2376a…1ddc0`), `urh_ls2d.csv`, `minibacia_ls2d.csv`, `urh_fractions.csv`,
`minibacias.csv` and the three LS JSONs were hashed before and after and are **UNCHANGED**.

**Residual owed elsewhere and NOT fixed here** (this session owns only `docs/37`, `docs/43` and its
own journal): `docs/47` §4.3's area column prints **0.42135** for this cell — a **third** support
(the `urh_ls2d_variants.csv` `area_km2` weighting, 0.4213519856784954), owed to `docs/47`'s owner;
`docs/52` §6:371's **×1.02484**, owed to `docs/52`'s owner; `docs/35` §9's :850 and :1021 **×1.02484**,
owed to `docs/35`'s amendment slot; `src/mgb_sediment.py`:223's docstring bracket `[0.24468, 0.42148]`;
`src/nbgen/make_nb18.py`:1244,1269,1353 / `make_nb19.py`:2435's **0.421475** and the notebooks they
generate; and `scripts/c3/ls_erosion_weights.py`:174's untagged `f_area` column header, which is the
channel by which the engine-support number entered the corpus. Full register:
`docs/agents/journal_defect-45-residual.md`.

---

## A3.4 Is C4.3 thereby UNBLOCKED? **NO** — and this amendment is the act that makes the block *dischargeable*, not the act that discharges it

**`docs/47`'s `C4.3-BLOCKED-UNTIL-LS-LANDS` holds.** Four independent grounds, none of which a
*decision* can discharge, and the honest answer keeps it blocked.

### (1) B1 is landed by **this amendment** — and B1 alone was never sufficient

`docs/47` §6.1 **B1** is *"Land C3.1 — the LS-formulation decision, under `docs/46` frozen, with
`ls_formulation`, its evidence grade, and the negative-result branch live"*, and §6.2 is explicitly
*"the contract C4.3 starts under, **once B1–B4 land**"*. **B1 lands here, in the reduced form A3.1.6
permits**: `ls_formulation`, its grade, the §4.2 outcome, the rescaled α column and the negative
branch are all live and written. **What B1 does not carry is the default-switch proposal**, because
ADOPT-SOURCE is not yet exercisable. **B3 and B4 are DISCHARGED**, verified on disk in this pass and
not taken on trust:

- **B3** — `src/mgb_transport.py`:**908** reads `if not (m <= max_resid)`, the NaN-safe form, with
  the IEEE-754 comment at :902–907; the NaN regression test is at `tests/test_transport.py`:274,
  `assert math.isnan(res.ledger["max_node_residual_t"])`. The all-NaN run can no longer publish a
  false PASS.
- **B4** — `docs/42` §9's amendment log exists from :616, carrying **A-P1** (§9.2, the fitting set is
  the **CAL 8**), **A-P2** (§9.3, `21237020` ARRANCAPLUMAS is evaluation-only), **A-P3** (§9.4,
  deposition `k` FIXED at 0), and **A-P1.1** (§9.5, the power table corrected and the
  0.0096-vs-0.0104 discrepancy resolved); the §9 card cell at :604 now reads *"THREE, all dated
  2026-08-11 — A-P1, A-P2, A-P3, plus A-P1.1"*. Neither is re-litigated here.

### (2) **B2, B5 and the §5.5 disclosure have NOT landed**, and none of them is C4.3's to discharge

**Measured on disk in this pass:** `docs/45` §8 at :610–612 still reads ***"Empty at registration"***,
and `docs/35` §9 carries **§9.1, §9.2 and §9.3 only** — there is no α-box re-registration anywhere.

- **B2** requires the C4.3 gate *"re-express[ed] in Π, or the α box re-register[ed] against the
  adopted `f_LS` … **Whichever C3.1 returns**"*, and notes that a `docs/35` §9 amendment *"may only
  be **proposed** by the session that hits the stop"* — so it is **owed to the document owners, not
  to C4.3**. **Adopting a point does not repair it**: `docs/45` §2.1's box **[2.0, 30.0]** and
  `docs/35` §6.1's **3.9 / 35.4** are still denominated at `f_LS` = 1, and a **point** moves them
  just as surely as an interval does (A3.2). That is `docs/47` §5.1's P1 and it is untouched.
- **B5** (replace the ±38 % Π band — measured ~4× too narrow in log units, with **G12 already
  firing**, 0.860 ln against ±0.322 ln — and restate the `k` bound as **~10× over 342 km**, not
  2.12×) is owed **before any C4 number is PRINTED**.
- **The `docs/47` §5.5 disclosure** — that `docs/45`'s registered objective was already profiled
  before any fit — is owed as a dated `docs/45` §8 amendment **before C4.3 RUNS**.

**Parallel agents are enacting B2, B5 and the §5.5 disclosure in the same run as this amendment.
Their landing is stated here as a CONDITION and is NOT claimed as a fact.** A later reader must
check `docs/45` §8 and `docs/35` §9 themselves; if this amendment and those land in the same commit,
the condition is satisfied by them and not by this sentence.

### (3) **BRANCH B IS MANDATORY** — and what that means for C4.3's *entry* is substantive, not a formality

`docs/46` §6.3 fires **three times over**, and its §6.1 discriminator is **exact, not a threshold**:

- **B1 fires on `Δ_shape` = 0.1299456916752905 > 0.** §6.1: *"any `Δ_shape` > 0 … Branch B is
  **MANDATORY**."* The null control for the uniform case Branch A exists for is
  **2.2204460492503136e-16**, so the measured value is ≈ **5.9e14 ×** one machine epsilon and
  ≈ **1.3e7 ×** `report_h2e.py`'s named 1e-8 reproduction tolerance; every one of the **thirty**
  measured readings of the definition lies in **[0.0159907, 0.1638779]**, all > 0, so **the branch
  is reading-invariant** (`docs/53`, `docs/46` §10 amendment 1).
- **B2 fires independently**, because ADOPT is unreachable under §6.2 **A3** while the α̂ thresholds
  are LS-conditional. This is why `docs/47` reached Branch B on its own grounds and why the branch
  is **over-determined**.
- **B5 fires** because the freezing of `docs/46` was scheduled, and its read-out states that B5
  *"continues to hold until"* this enactment amendment exists.

**What "Branch B mandatory" actually implies, worked out rather than glided past:**

1. **It CLOSES Branch A; it does not merely make a provisional C4.3 stricter.** §6.2's six
   conditions are available *"**only** if `Δ_shape` = 0"*. So **A1**'s PROVISIONAL labelling, **A2**'s
   run card at `ls_formulation = ours_2026_08`, **A3**'s ADOPT-PENDING ceiling, **A4**'s two α̂ stops
   (7.54 upper / 2.10 lower), **A5**'s named noise floor and **A6**'s no-rescaling rule are all
   Branch-A machinery and are **unavailable**. **There is no legal PROVISIONAL C4.3 at all** — the
   six conditions are **moot rather than satisfiable**.
2. **No rescaling substitutes for a re-run.** §6.1 mandates the sentence, and it is written here in
   the required form: ***"the fit is recoverable by rescaling `α̂` if and only if `Δ_shape` = 0
   exactly; the measured value is 0.1299456916752905, and the re-run is owed."*** Every existing
   profile of the registered objective — `docs/47` §5.2's rescaled optima and §5.5's whole-box,
   nine-β profile — is a **LEVEL-only** rescaling of the α axis and is **not** the answer at the
   adopted LS.
3. **The residual vector itself changes, so the search must run on the ADOPTED LS FIELD.** Measured
   (`docs/53` §2, verified on disk this pass at :134, :141, :143): **no CAL station is invariant**;
   the argmax is **`24037390` CAPITANEJO at |ln| = 0.1299456917** and the smallest of the eight is
   **`26127010` EL ALAMBRADO AUT at 0.0179854753**; the CAL 8's own `f_s` spread is **×1.250023**.
   So **every guard statistic must be re-derived on the new residuals** — G4.1's ln `LS̄`
   coefficient, the per-station residual sd, `k_min`, G12's LOO range and the Π band — and under
   **A5 as amended** the C4.3 session must **NAME its noise-floor construction**, because *"a
   minimum detectable coefficient computed against 0.465 is void"*.
4. **`docs/47` O5 is not merely open but known to be non-trivially open**, and it becomes runnable
   **only after C3.1 lands, never before**: re-profiling `F_report` on a corrected LS **field**
   (not axis) is the owed measurement, and the per-station redistribution the rescaling could not
   model is **real and measured** (±1.287× per-station, `docs/47` §4.4, §6.2 O5).
5. **`Δ_shape` says nothing about whether any gate passes** (`docs/53` §6 item 2) and **must not be
   read as detectability** — the LS shape signal remains measured **3.1× below G4.1's power**
   (`docs/47` §4.4). It is a *sequencing* discriminator, not a finding about shape.

**Branch B is a sequencing mandate, not a permanent veto.** Once the enactment is *exercised* there
is nothing left to wait for, and the post-enactment C4.3 is a **first run** rather than a **re-run** —
which is the economy `docs/46` §6.4 measured and offered as information, explicitly **not** as a gate.

### (4) A physical block: **the adopted variant is not a committed product**

`urh_ls2d_variants.csv` has **no `V4_dg` column** and `urh_ls2d.csv` may not be overwritten
(A3.1.6 item 3). **C4.3 cannot consume a variant that no committed product carries**, and no default
can be switched by name.

### The contract C4.3 would start under — stated CONDITIONALLY, in order

**Prerequisites, in sequence:** (i) §3.3's missing **stratified report** — slope terciles for every
variant, and the per-station erosion-weighted `LS̄` as **levels**, not ratios — plus `docs/46` §2.3's
H-S field clause **(R7)/(R8) items 2–3**; (ii) a durable, **gated `V4_dg` column** in a **new**
committed product, `urh_ls2d.csv` and `minibacia_ls2d.csv` left untouched; (iii) the `docs/35` §9
amendment A3.1.3 records as owed; (iv) **B2**, **B5** and the **§5.5 disclosure** as dated `docs/45`
§8 amendments (B5 before any C4 number is *printed*; §5.5 before C4.3 *runs*); (v) the separate,
dated **default-switch** act (A3.5.1).

**Then C4.3 enters under `docs/47` §6.2's six items, with item 2 in its POINT branch** — *"unless
C3.1 collapses it to a point, in which case the adopted point and its grade travel instead"* — so
what travels with **every** α̂ is `f_LS` = **0.25146** erosion-weighted (area proxy
**0.2446790094097074**), `1/f_LS` = **3.976775630318937**, **formulation CITED / factor DERIVED /
LEVEL UNVALIDATED**, and **not** the `[0.25146, 0.43194]` bracket. Item 1: the gate read in Π, or in
α against a **named, dated `f_LS` in the same table**. Item 3: the corrected Π band, beside *"the
level is set by 8 stations whose residuals span a factor of 412"*. Item 4: the corrected `k` bound
with the asserted `SDR = 1.0` claim in `docs/45` §2.3's words. Item 5: all of `docs/45` §2–§6
imported unchanged, including G9's **66.53 %** disclosure, G6's five reporting elements, G10's
mandatory *"the calibration determined a level and essentially nothing else"* statement, the five
not-claims of §5, and the **`docs/23` §13.2 embargo**. Item 6: the §5.5 disclosure in
`report_C4.json` and in the C4 document. **And the search runs on the ADOPTED LS FIELD — never on a
rescaling of a surface already seen.**

> **The remaining blockers, listed plainly so nothing is inferred from silence:** §3.3's stratified
> report (slope terciles absent; per-station `LS̄` only as ratios) · H-S's (R7)/(R8) items 2–3 · the
> missing committed `V4_dg` column · the `docs/35` §9 amendment of A3.1.3 · **B2** · **B5** · the
> **§5.5** disclosure · and Branch B's own consequence, that the fit must be a **first run on the
> adopted field** with every guard statistic re-derived.

---

## A3.5 What this enactment does **NOT** do

### A3.5.1 **No engine default moves here.** The owner, and the trigger, named

**OWNER: the C3.1 owner** — in `docs/46` §4.2's ADOPT-SOURCE licence column, *"whoever owns
`scripts/c3/ls2d.py` and `docs/37`"*. `docs/46` §9's registration card pins it and grounds it:
*"Enactment owner — `docs/37` §A3, dated, written by the C3.1 owner (`docs/51` §5.3; `docs/37` A2.2
assigns the LS-shape decision to C3.1 by name, and `scripts/c3/ls2d.py` + `data/processed/urh_ls2d.csv`
were delivered under C3.1 by commit `5eaabf5`)."* **Not** `docs/45`'s owner, **not** `docs/46`'s,
**not** C4 — `docs/42` **G4.2** keeps `ls2d_*` out of C4's hands and `docs/46` §5 lists the committed
LS products and `ls2d.py`'s defaults as immovable — and **not** any read-only panel.

**TRIGGER: two separately dated acts, and the distinction is the whole point.**

| act | what it is | status |
|---|---|---|
| **ACT 1 — the enactment** | **THIS AMENDMENT.** A **WRITTEN** amendment carrying `ls_formulation` and its grade, the §4.2 outcome, the α band rescaled per item 3, every prior variant reachable by name, §1's table and §4 candidate 0 corrected off *"2.37× – 3.00×"*, and §4.4 item 1's true ordering sentence. **What ADOPT-SOURCE licenses is only *"proposing* the adopted variant as the engine default in a **separate**, dated amendment"** — **so act 1 proposes; it flips nothing.** | **DONE, 2026-08-12** — and, because A3.1.6's three deliverables are outstanding, **this act does not even make the proposal**. It records the outcome. |
| **ACT 2 — the default switch** | `ls2d_column` moved from `"ls2d_hs"` to the adopted `V4_dg` column, **and** `urh_ls2d` re-pointed at the **new** committed product — a **TWO-PARAMETER** change, as its own dated act by the same owner. `docs/46` §5's committed-LS-products row is explicit: *"the default switches only through §4.2's separate dated amendment."* | **NOT DONE, and it MAY NOT PRECEDE ACT 1.** Its preconditions, verified read-only on disk this pass: `src/mgb_sediment.py`'s `load_geometry` defaults are `urh_ls2d = "urh_ls2d.csv"` (:863) and `ls2d_column = "ls2d_hs"` (:757, :801, :864); **`V4_dg` exists in NEITHER committed file**; `urh_ls2d.csv` and `minibacia_ls2d.csv` **may not be overwritten** (§3.1). **It cannot even be drafted** until the column is materialised. |

**ENACTMENT IS A WRITTEN AMENDMENT, NOT A CODE EDIT.** A code change to a default that is not
preceded by act 1 and separately dated as act 2 is **not** enactment — it is an **unrecorded default
switch**, which is exactly what `docs/46` §5 and §9's *"no engine default moved"* card exist to make
detectable.

**What the switch may NOT drag with it, when it eventually happens:** `ls2d_aggregation` and
`ls2d_resolution` stay at factor **1.000** (`area_weighted_mean`, `native_90m`) — `docs/42` **G4.2**
forbids using them to move the level, and `docs/46` §3.2 forbids `per_cell_median` for any variant
in any table. `cp_revision`, `volume_convention`, `k_unit_system`, the **H2E** parameters, α, β, `P`
and `FG` do **not** move (`docs/46` §5). `data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv`,
`urh_ls2d_variants.csv` and everything in `sim_calibrated_v2/` stay **read-only**. **And the switch
changes NO grade:** after it, the LS level is **still UNVALIDATED** and must be printed that way
(`docs/42` G4.2, `docs/46` §9.2).

**Until act 2, the engine keeps running `V0` with the discrepancy DECLARED.** That is **the interim
engine state, not an outcome**, and `V0` is emphatically **not validated by having survived**
(`docs/46` §7.3).

**Every prior variant stays reachable BY NAME** (`docs/46` §3.1): `V0` `ours_2026_08` · `V1`
`lim_pixel` · `V2a` `m_cap05` · `V2b` `m_step_eq14` · `V3` `s_ws78` · `V4` `buarque_2015` (the
hybrid) · `V4'` `buarque_2015_cap` (whose `min(m, 0.5)` may never be graded CITED) · **`V4_dg`
`buarque_2015_dg` (adopted)** · `V5` `L_dg96_fd`. **Nothing is retired by this adoption**, and
`V4`'s ×0.43194 row stays reproducible precisely because `docs/35` §9.3.1, §4 candidate 0 and
`docs/43` §1.4 quote it.

### A3.5.2 What A3 does **NOT** conclude — from `docs/46` §8.2 and §9.2

1. **It does NOT validate the LS level.** `docs/42` **G4.2** stands: the level is **UNVALIDATED** and
   must be printed that way. **CITED is not validated** (A1.6 item 3); **fitted is not validated
   either** (`docs/43` §3.3 item 1). Raising four levers to CITED raises their **provenance** grade
   and nothing else.
2. **It does NOT close C3, and the verdict line of this document is unchanged: OPEN.** Clause 2 of
   A1.1's conjunction needs the ***shape*** decision, and clauses **3** and **4″** are untouched by
   anything here (`docs/43` §2). **Settling LS is NECESSARY AND NOT SUFFICIENT** (`docs/46` §8.2
   item 6). Concretely, clause 2 remains NOT MET on three separate counts: the outcome is recorded
   and not **exercised** (A3.1.6); the engine default has not **moved** (A3.5.1); and the **shape**
   defect A2.2 classifies is not repaired — the adopted field is not in the engine, H-S's field
   clause (R7)/(R8) items 2–3 have never been read out, and G4.1 is measured **3.1× underpowered**
   to see the shape at all.
3. **It does NOT say the LS *shape* is right**, on any non-detection: a G4.1 non-detection exonerates
   the field's shape and **says nothing about its level**, and a non-detection at unreported power
   says nothing at all (`docs/46` §8.2 item 5).
4. **It says NOTHING about the `C` level, the `K` unit system, the volume convention, `P` or `FG`.**
   They are the same parameter written differently; an LS result that appeared to speak about one of
   them would be speaking about **Π** (`docs/46` §8.2 item 4, §8.1).
5. **It says NOTHING about whether the model is under- or over-erosive.** **A1.9 WITHDREW the
   direction**: the C3 residual's direction is **UNKNOWN** (2.27× low … 1.49× high), and the
   *"~2× under-erosive"* claim is **withdrawn**. No LS variant may be argued for or against by which
   way it moves the load (`docs/46` §8.2 item 3) — which is exactly why A3.3.1 declines to re-derive
   the struck ADR and Leg-A numbers rather than correcting them.
6. **It settles NOTHING about α = 11.8's like-for-likeness with any 2-D contributing-area LS.**
   **NOT SETTLED, and no band is offered** (`docs/46` §1.0 residue 3, §9.2; `docs/47` §4.2 item 6,
   O4). It bounds every number in A3.2 from above.
7. **It says NOTHING about the 66.53 % of the model's erosion upstream of no usable SSC station**, or
   about the **801.1 km** of channel below the outlet-most one (`docs/46` §8.2 item 7).
8. **It does NOT unblock C4.3** (A3.4), and **it does not license re-fitting anything to the new
   level without `docs/46` §6** (§4.2's ADOPT-SOURCE row, final column).

---

## A3.6 Direction disclosure, and what was NOT done

**Measured by me in this pass, read-only, and not carried from any summary or panel:**

- the three live superseded-number sites this document still carried at §4 candidate 0's *"DO NOT
  stack"* paragraph, A1.5's *"What would close C3"* paragraph, and §4 candidate 0's interaction
  identity (A3.3.1's closing block) — found by grep, corrected here;
- the whole of A3.2's arithmetic, recomputed at full precision with `python3.10` (A3.8), including
  the erosion-weighted lever product, where **I first wrote the wrong number and caught it by
  measuring**: `0.362435 × 0.517480 × 1.694054 = 0.3177246791318452` is **the cap**, while the
  product that pairs with the registered joint/product ×1.347608646050708 uses the **eq.-14 step**,
  `0.362435 × 0.522043 × 1.694054 = 0.3205262902296241`. Recorded because the standing rule in this
  project is *measure before asserting*, and this is a live instance of it;
- **B3** at `src/mgb_transport.py`:908 and `tests/test_transport.py`:274, and **B4** at `docs/42`
  §9.1–§9.6 with the §9 card cell at :604 — both **DISCHARGED**;
- `docs/45` §8 at :610–612 still **"Empty at registration"**, and `docs/35` §9 carrying §9.1/§9.2/§9.3
  only — so **B2, B5 and the §5.5 disclosure had NOT landed at the time of my read**;
- `docs/35` §9.3.2 item 1 at :710–715 read verbatim — the **three-lever** enumeration that grounds
  A3.1.3's supremacy objection;
- `src/mgb_sediment.py`'s `ls2d_column = "ls2d_hs"` (:757, :801, :864) and `urh_ls2d =
  "urh_ls2d.csv"` (:863); `urh_ls2d_variants.csv`'s header (**no `V4_dg`**) and `urh_ls2d.csv`'s
  four columns;
- `data/raw/refs/buarque2015.pdf` at **9,646,521 bytes**, sha256
  `3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037` — **MATCHES** `docs/38` §9.1;
- **slope terciles CONFIRMED ABSENT** — a grep across `docs/`, `scripts/` and `src/` returns only
  documents saying they are owed;
- `docs/47`:369–371's `formPRESED.exe` `S`-user-choice finding, and `docs/53`:23–24/:134/:141/:143's
  `Δ_shape`, argmax and CAL-8 spread.

**Carried and cited, not re-derived here:** the engine re-runs of `docs/47` §4.3 (0.25146, 0.43194,
75.3235, 129.3840); the lever factors of `docs/49` and `docs/50`; `docs/46` §10 amendment 1's second
erosion-weighted reproduction; the transcriptions of Buarque pp. 47, 48, 94, 98, 121, which three
independent panellists each re-read from the hash-matching PDF this run; the `docs/47` §4.1 findings
and §4.4 power numbers; the 153-passed test-suite state; and `Δ_shape`'s thirty-reading range.

**What was NOT done:**

- **No frozen artifact was opened for writing.** `docs/33`, `docs/35`, `docs/42`, `docs/45`,
  `docs/46` and `docs/51` were **read only**. `data/processed/urh_ls2d.csv`,
  `minibacia_ls2d.csv`, `urh_ls2d_variants.csv` and everything in
  `data/processed/sim_calibrated_v2/` were **read only**.
- **No engine default moved.** `ls2d_column`, `urh_ls2d`, `ls2d_aggregation`, `ls2d_resolution`,
  `cp_revision`, `volume_convention`, `k_unit_system`, α, β and the H2E parameters are all
  **untouched**. No file under `src/` or `scripts/` was edited.
- **No fit, no calibration, no LS pass was run. No α̂ was produced or quoted, provisional or
  otherwise. `KGE_ln` was not evaluated against the `docs/45` §2.1 box.**
- **No git command was run.** The orchestrating session commits.
- **No new band was introduced and no materiality bar was reconstructed.** `docs/52`'s striking
  stands; nothing here compares a difference to a threshold.
- **Gauge-referenced t/km²/yr yields remain embargoed** (`docs/23` §13.2). Every load in this
  amendment is **absolute flux**.

**Files written by this amendment:** `docs/37_c3_closure.md` (this section, plus A3.3's in-place
corrections) and `docs/agents/journal_a3-enactment.md`. **Nothing else.**

**A panel was used and is disclosed as what it is.** Three independent **read-only** panellists each
derived the §4.2 outcome from the frozen rule before this amendment was written
(`docs/agents/journal_panel-fidelity.md`, `journal_panel-negative.md`,
`journal_panel-posthoc.md`). **All three returned ADOPT-SOURCE at `buarque_2015_dg`, determined but
not exercisable, and C4.3 NOT unblocked.** They are **evidence, not instructions**, and two
adjudications were needed. **First**, they split on whether §4.2 item 3's rescaling obligation
attaches at all to a *default* rather than a *deviation*; resolved in A3.2's blockquote, against the
narrow reading, on §4.2's own licence cell and §7.3 item 5. **Second, one of the three omitted the
`docs/35` supremacy objection entirely** — the strongest objection to the adopted **value** on the
record — and it is adjudicated in **A3.1.3** with the branch under which this amendment would be the
bug written out in full. **Where all three were wrong:** none named the three live superseded-number
sites of A3.3.1's closing block, which were found by grep in this pass. Convergence of three
panellists and two prior sessions on one outcome is **persistence, not reproduction**, and is not
counted as evidence for the outcome.

---

## A3.7 Cross-references — what is owed, to which owner, so a reader can audit whether the enactment travelled

**This amendment enacts NONE of these. Each is recorded as owed, dated, and to be applied by its own
owner as a dated correction — never as a silent edit** (`docs/46` §7.3).

| owed to | what | source of the obligation |
|---|---|---|
| **`docs/35` §9** (amendment slot) | **(a)** the ruling A3.1.3 asks for: that §9.3.2 item 1's **three-lever** enumeration is superseded by eq. 13's reading — **without it, `docs/35` wins on its literal text and this amendment's outcome becomes NEGATIVE — UNRESOLVED**; **(b)** §9.3.3's expected consequence **re-based** from the prior `C` to 299.5387088405831 Mt/yr; **(c)** §9.3.1's *"his eq. 14"* mislabel on the ×0.502 row (A3.3.2); **(d)** §9.3.2 item 3's *"expected ≈ 2.0 – 9.9, hard stop ≈ 11.8 – 14.9"* re-derived to A3.2's numbers; **(e)** B2's α-box re-registration, which may only be **PROPOSED** by the session that hits the stop (`docs/45` §6.1) | A3.1.3; `docs/46` §7.3 items 1–3; `docs/47` §6.1 B2 |
| **`docs/45` §8** (amendment slot, **"Empty at registration"** at the time of my read) | **B2** (the gate re-expressed in Π, or the α box re-registered against the adopted `f_LS`); **B5** (the ±38 % Π band replaced; the `k` bound restated as ~10× over 342 km); the **§5.5 pre-fit-profile disclosure**; and §2.1's superseded *"2.37× – 3.00×"* derivation re-derived | `docs/47` §6.1 B2/B5, §5.5; `docs/46` §7.3 item 3 |
| **`docs/46` §10** (amendment slot; §1–§9 frozen) | the **identity defect** below; and the closing note's own list — H-S's (R7)/(R8) items 2–3 and §3.3's stratified report — before ADOPT-SOURCE is **exercised** | A3.1.6; below |
| **`docs/51`** | the same identity defect at §2.3 | below |
| **`docs/42` §9** | **nothing further from this amendment.** B4 is **DISCHARGED** (A3.4), verified on disk. `docs/42` **G4.1/G4.2** are unchanged by anything here | `docs/46` §7.3 item 4, read out |
| **`docs/43`** | §1.4's *"his eq. 14"* mislabel (A3.3.2); and `docs/47` §2.5 C1's correction to §3.4 — 6.83 – 8.73 is at the **prior** `C`, and at the adopted `C` the deposition-free band is 5.67 – 7.25 | `docs/46` §7.3 item 2; `docs/47` §2.5 |
| **`src/nbgen/make_nb18.py`, `make_nb19.py`** | the same *"his eq. 14"* mislabel, and the superseded bracket wherever it is printed into a notebook | `docs/46` §7.3 items 2–3 |
| **whoever materialises the adopted field** | a durable, **gated `V4_dg` column** in a **NEW** committed product — `urh_ls2d.csv` and `minibacia_ls2d.csv` **not** overwritten (`docs/46` §3.1, §5) — which is simultaneously the fix for §3.1's *"reachable by name"* failure, the precondition of act 2, and the route to a **third** erosion-weighted reproduction of the endpoint (`docs/51` §7 item 7) | A3.1.6 item 3 |
| **C4.3's session** | `docs/47` §6.2's six items, **item 2 in its POINT branch**, on the **adopted LS field** and never on a rescaling; A5's **named** noise-floor construction | A3.4 |

> **A DEFECT IN FILES THIS AMENDMENT DOES NOT OWN — REPORTED, NOT FIXED.** `docs/46` §1.0 (at
> `docs/46`:127) and `docs/51` §2.3 both print the identity
> `ln(0.43194 / 0.25146) = 0.5410 = −ln 0.580685`. **Measured:**
> `−ln(0.580685) = 0.543546837831505` against `ln(0.43194/0.25146) = 0.5410027585442313` — a gap of
> **0.0025440792872737372 ln** — and `exp(−0.5410027585442313) = 0.5821641894707599`, so **0.5410
> pairs with 0.58216, not 0.580685**. **Both constituents are separately correct** — 0.580685 is
> `docs/50`'s measured in-formulation `L`-form ratio, and 0.5410 is the ln ratio of the two 5-s.f.
> endpoints — but **the IDENTITY as written does not hold**. It is **immaterial to every verdict in
> this amendment and to every verdict in either source document**; the two quantities are simply
> not the same number and should not be joined by an `=`. Owed to `docs/46` §10 and to `docs/51`.

**Also still open and NOT fixed by any outcome of this amendment:** `docs/47` **O4** — α = 11.8's
like-for-likeness with any 2-D contributing-area LS is **NOT SETTLED, no band offered**, and it
bounds every rescaled number from above; **O2** — which `S` function is valid above tan θ 0.50,
where 11.26 % of cells carry **35.5 %** of the basin's area-weighted `S` signal and **no** primary
source validates **any** `S` function; **O3** — the exact cap value, which the literature calls
*"arbitrary"* in print; **O1** — Desmet & Govers (1996) and Fagundes et al. (2026) **unobtained**;
**O5** — `F_report` re-profiled on a corrected LS **field**, runnable only after C3.1 lands; and the
**governance gap** A3.1.6 names, that §4.2's table contains no row for *"determined but not
exercisable"*.

---

## A3.8 Reproduction

Every number this amendment prints, recomputed read-only. Nothing below writes, fits, or runs the
engine.

```
python3.10 -c "
import math
f = 0.25146                 # registered f_ero(V4_dg), docs/47 §4.3 / docs/46 §1.0, §3.1
fe = 0.2514648985839397     # 2nd independent erosion-weighted reproduction, docs/46 §10 amd 1
fa = 0.2446790094097074     # area-weighted PROXY, docs/50 (never overrides f_ero, docs/46 §3.3)
fh = 0.43194                # the documented HYBRID V4 (source's 3 levers + our L)
for x in (3.9, 5.9, 11.8, 23.6, 35.4, 2.0, 30.0, 3.40):
    print(x, repr(x*f), repr(x*fe), repr(x*fa))
print(repr(1/f), repr(1/fe), repr(1/fa), repr(math.log(f)))
print(repr(11.8*fh), repr(35.4*fh), repr(1/fh))
print(repr(f/fa), repr(math.log(fh/f)), repr(fh/f))
print(repr(299.5387088405831*fe), repr(129.3840/299.5387088405831))
print(repr(0.431944/(0.362435*0.522043*1.694054)))
print(repr(0.362435*0.522043*1.694054), repr(0.362435*0.517480*1.694054))
print(repr(39.812/9.741), repr(-math.log(0.580685)), repr(math.exp(-0.5410027585442313)))
"

3.9  f 0.9806940000000001  exact 0.9807131044773649  area 0.9542481366978589   <- lower hard stop
5.9  f 1.4836140000000002  exact 1.4836429016452444  area 1.443606155517274    <- band, low edge
11.8 f 2.9672280000000004  exact 2.9672858032904887  area 2.887212311034548    <- ALPHA REFERENCE
23.6 f 5.934456000000001   exact 5.9345716065809775  area 5.774424622069096    <- band, high edge
35.4 f 8.901684            exact 8.901857409871466   area 8.661636933103642    <- UPPER HARD STOP
2.0  f 0.50292             exact 0.5029297971678794  area 0.4893580188194148   <- docs/45 box floor
30.0 f 7.543800000000001   exact 7.543946957518192   area 7.3403702822912225   <- docs/45 box ceil
3.40 f 0.8549640000000001                                                      <- 5%-of-box rail
1/f  3.976775630318937   1/fe 3.9766981619750683   1/fa 4.08698728351287
ln f -1.3804713478171018
hybrid V4:  11.8f 5.096892   35.4f 15.290676   1/f 2.315136361531694
proxy bias f_ero/f_area          1.0277138223121463      (docs/47 §3.1 R7 independently 1.0278)
L-form lever ln(0.43194/0.25146) 0.5410027585442313   ratio 1.7177284657599616
basin load 299.5387088405831*fe  75.32347104056149 Mt/yr   (absolute flux; docs/23 §13.2 embargo)
implied f_ero of the 129.3840 re-run  0.43194417342854735   ("0.43194" is its 5 s.f. rounding)
joint / product of single levers 1.347608646050708   <- NEVER quote the product as the joint
  eq.-14 STEP product 0.362435*0.522043*1.694054 = 0.3205262902296241   (pairs with x1.34762)
  CAP product         0.362435*0.517480*1.694054 = 0.3177246791318452
docs/46 §4.2 item 3's literal area rescaler 39.812/9.741 = 4.087054717174828 (= 1/fa to 5 s.f.)
REPORTED DEFECT, not fixed:  -ln(0.580685) = 0.543546837831505
                             exp(-0.5410027585442313) = 0.5821641894707599

# provenance and state checks, read-only
sha256sum data/raw/refs/buarque2015.pdf
  3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037   9,646,521 bytes  -> MATCHES docs/38 §9.1
head -1 data/processed/urh_ls2d_variants.csv     -> no V4_dg column (A3.1.6 item 3)
head -1 data/processed/urh_ls2d.csv              -> ls2d, ls2d_hs, ls2d_mb86, ls2d_dg96 only
grep -n "if not (m <= max_resid)" src/mgb_transport.py       -> :908       B3 DISCHARGED
grep -n "isnan" tests/test_transport.py                     -> :274       B3 test present
grep -n "A-P1\|A-P2\|A-P3" docs/42_*.md                      -> §9.1-§9.6 B4 DISCHARGED
grep -n "Empty at registration" docs/45_*.md                -> :612       B2/B5/§5.5 NOT landed
grep -rn "tercile" docs/ scripts/ src/   -> only documents saying they are OWED; NO artifact

Delta_shape = 0.1299456916752905 (docs/53; argmax 24037390 CAPITANEJO; smallest CAL station
  26127010 EL ALAMBRADO AUT 0.0179854753; no CAL station invariant; CAL 8 f_s spread x1.250023)
  => Branch B MANDATORY (docs/46 §6.3 B1), and B2 makes it mandatory regardless.

Test suite: 153 passed, 1 warning (measured 2026-08-12; unchanged by this amendment, which
  edits no code). No fit was run; no alpha-hat exists.
```


---

## A3.9 Closure of the three surviving T6 findings — 2026-08-13

`docs/54` §6 recorded **four** adversarial findings that survived independent refutation and
were left OPEN when the run that raised them was cut short. One was CRITICAL and belonged to
the notebook track (`refute-t6-2`, the retired ±38 % band live in `src/nbgen/make_nb19.py`);
it is **fixed and verified from executed output** — 14 sites, nb19 re-executed, all 33
integrity assertions passed, 299.5387 / 248.7298 reproduced, `pytest` 154 passed. The two
that belong to **this** document are closed here, and the third is closed in `docs/51` §9
Amendment 3. **None of the four touched a canonical result number**, and none does now.

### A3.9.1 `refute-t6-1` (HIGH, freeze-honesty) — *"exercised"* was premature. It is now TRUE.

**The finding, confirmed by its refuter** (`docs/agents/journal_refute-t6-1.md`: *"I could not
kill it"*): §A3.3's item 4 at line **241** said `docs/46` §4.2's outcome *"is now exercised as
ADOPT-SOURCE"*, while `docs/46` §4.2 note 3 reserves **exercised** for the step gated on §3.3's
**full stratified report**, and **A3.1.6 of this very amendment** said *"determined and
recorded, NOT YET EXERCISABLE"*. The refuter found the one substantive site to be :241;
:1394 and :1423 use the same verb in a *defensible-but-colliding* sense, and
`src/mgb_sediment.py`:242 is mitigated in place two lines later.

**What discharged it — measured on disk, not asserted.** The gating condition has since been
met, by other owners, after A3 was written:

| what was owed | discharged by | evidence on disk |
|---|---|---|
| `docs/46` §3.3's **full stratified LS report** (slope terciles were *confirmed absent* when A3 was written) | **`docs/46` §10 Amendment 3, 2026-08-12** — *"the last owed item of `docs/47` §9.2 blocker 4"* | `scripts/c3/ls_stratified_report.py`, `data/processed/ls_stratified_report.{json,md}` |
| §2.3's **H-S field clause (R7)/(R8) items 2–3** — the one part of `docs/46` §2 never read out | **`docs/46` §10 Amendment 4, 2026-08-12** | `docs/46`:1642 |
| the **engine default** itself (A3.5.1 named this as a separate dated act) | **ACT 1 + ACT 2, 2026-08-12** | `V4_dg` materialised, then made the default; `V0` pinned explicitly |

> **RESOLUTION.** *"Exercised"* was **wrong when written** and is **right now**. The wording at
> :241 is corrected in place with a dated pointer rather than silently repaired, because the
> record of what was claimed prematurely is itself the audit trail. **A3.1.6's
> *determined-but-not-yet-exercisable* status is therefore SUPERSEDED BY EVENT, not by
> argument** — and the sequence is checkable: the report landed *after* the claim.

### A3.9.2 `refute-t6-6` (HIGH, a3-overreach) — the fallback branch named an inadmissible outcome

**The finding, confirmed on three independent legs** (`journal_refute-t6-6.md`), against A3.1.3's
*"THE HONEST LIMIT OF THIS ADJUDICATION"* blockquote:

1. it asserts **NEGATIVE — UNRESOLVED on a *documentary* ground**, which is **absent from**
   `docs/46` §4.2's frozen disjunction — and **A3.1.1 measures all three disjuncts FALSE**. A
   frozen row's entry conditions cannot be extended by an amendment in another file;
2. it contradicts **`docs/35` §9.4.3's** own stated consequence for the same premise, **and
   contradicts this document's own :1536–1538**;
3. *"`V0` retained"* as part of a §4.2 outcome is exactly the **engine-state / outcome
   conflation** that A3.1.1's RETAIN-OURS row expressly rejects.

**Two corrections to the finding as raised**, from its own refuter, so the record is right in
both directions: the *fallback-vs-fallback* gap is **×2.3151** (`V0` vs `docs/35` §9.3.2's
registered three-lever default `V4`), **not ×1.7177** (which is the POINT-vs-hybrid `L`-form
lever, correct in its own place at :240 and :1409); and the locator must include **A3.7's
`docs/35` row (a)**, which is where the owed amendment was registered.

> **RESOLUTION — and the branch's trigger DID NOT FIRE.** The branch was conditional on
> *"if `docs/35`'s owner declines"* the owed §9 amendment. **The owner did not decline.**
> **`docs/35` §9.5, dated 2026-08-12**, re-registers the §6.1 α band at the adopted LS level and
> records in its own words that *"ACT 1 and ACT 2 have now been executed"*. So the supremacy
> conflict this branch was insurance against **was resolved by the document that would have
> lost**, in its own amendment slot, by its own owner — which is the correct route and the one
> A3.7 row (a) asked for. The branch is **corrected in place and closed**; it is not deleted,
> so a future reader can see what it protected against and why it lapsed.

### A3.9.3 What A3.9 does NOT do

It moves **no engine default** (ACT 2 did that, separately and earlier, and A3.9 is a written
record only); it **runs no fit** and quotes **no α̂**; it opens no frozen artifact for writing;
it introduces **no materiality bar** and reconstructs none (`docs/52` §7 item 2); it does not
re-open `docs/46` §1–§9, `docs/35` §1–§8, `docs/42` §1–§8 or `docs/45` §2–§6; and it does **not**
close C3 — clauses 3 and 4″ of A1.1's conjunction are untouched, and A3.4's **C4.3 verdict is
unchanged by this section** (C4.3's own outcome is `docs/55`, RAILED / EXPLORATORY). The
`docs/23` §13.2 yield embargo is in force: no t/km²/yr appears here.
