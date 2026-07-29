# Presentation plan — MGB-SED / Magdalena (methodology-focused)

**Audience:** Prof. Briceño Zuluaga (UMNG, EMINES).
**Framing (critical):** the advisor's reply to our proposed solutions was *"how do you plan to do all this?"* — so the **spine of the deck is the methodology and the work plan**, not the context. Every slide should visibly answer *how*. Context/motivation is kept to a minimum; the middle third (model + preprocessing + calibration) and the work plan are the heart.
**Scope of THIS talk (important):** the focus is the **hydrological modelling (MGB-SA)** — water balance, runoff generation, discharge calibration/validation, and the ENSO signal in discharge. The **sediment module / final MGB-SED implementation is NOT the centrepiece**; it appears only briefly as the **next phase (outlook)**. Rationale: hydrology must be calibrated first, and it is where our data is already collected and validated — so it is the defensible, concrete story for the advisor.

**Integration:** slots marked **[+colleague]** are where the classmate's work will be inserted once their git arrives (likely in Data, Team, and possibly a dedicated method component).

---

## Section A — Framing (keep short: ~3 slides, ~15% of time)

**1. Title.** Project title; authors (TWILL + colleague); advisor; program; date. One basin image.

**2. Problem & motivation (1 slide max).** Magdalena = one of the world's largest specific sediment yields; strong **ENSO**-driven interannual variability; consequences (reservoir siltation, delta, water quality). One sentence on the gap: the ENSO–sediment *link* is known observationally, but never reproduced with a **process-based, distributed** model over the whole basin.

**3. Question, objectives, hypothesis, novelty.**
- Main objective: quantify & **explain** the sediment-flux difference between La Niña 2011 and El Niño 2015-16 with a calibrated MGB-SED.
- Hypothesis: contrasting ENSO phases produce a detectable, physically interpretable difference the model can reproduce.
- **Novelty** (from our literature check): first **MGB-SED** application to the Magdalena; process + spatial attribution beyond existing statistical correlations (Restrepo).

## Section B — Methodology (the core: ~8 slides, ~50% of time)

**4. Methodological overview — the roadmap.** One master flowchart: *inputs → preprocessing → MGB-SA (hydrology) → MGB-SED (sediment) → ENSO comparison*, dashed arrows = calibration data. This slide is the map the rest of the talk walks through. (Reuse the README/notebook-04 diagram.)

**5. Why MGB-SED (model choice = a methodological decision).** Semi-distributed, physically-based; **transposition of Fagundes et al.** (southern Brazil) to Colombia; couples hydrology + hydrodynamics + sediment; spatial units = **minibacias**, sub-divided into **URH** (soil × land-cover). Justify why a process model (vs a rating curve) is needed: spatial attribution + prediction.

**6. Model structure & equations (high-level).** Vertical water balance per URH; saturation-excess runoff (parameter *b*); MUSLE hillslope erosion (K, LS, C, P, α, β); channel transport (Exner). Show the **parameter → data-source map** (DEM→geometry, soils→Wm/K, land cover→vegetation, ERA5→forcing, IDEAM→calibration). *(Backup slide holds full equations.)*

**7. Data & sources — inventory. [+colleague]** The 6 dataset families table (source, resolution, role) with status **collected & verified**. Cite the data-inventory notebook (06). Emphasise: DEM (Copernicus 90 m), WorldCover, SoilGrids, ERA5-Land, IDEAM discharge (167 stations), IDEAM sediment (77 stations, variable CM). *(Colleague's collected datasets slot in here.)*

**8. Preprocessing methodology.** The chain, step by step: DEM → fill → D8 → accumulation → **minibacias** (IPH-HydroTools); **URH** = soil-group × land-class crossing; SoilGrids **raw texture → pedotransfer → K, Wm, soil groups**; WorldCover **reclass → 8 hydro classes + C factor**; ERA5 hourly→daily + **bias correction vs IDEAM gauges**. This is the most "how" slide — spend time here.

**9. Calibration & validation strategy.** **Hydrology first**, then sediment (always). Split-sample calibration/validation; objective functions **KGE / NSE / PBIAS**. Sediment: **tributary calibration + rating curves** (Qs = a·Q^b); note the sediment-data gap on the mainstem and the three mitigations (tributaries; direct concentration comparison since MGB-SED outputs concentration; Restrepo published rating parameters as backup).

**10. Data-driven validation of our choices (shows rigor).** Selected EDA figures from notebook 06: (a) **ENSO anomaly** — 2011 = +1.7σ (wet) vs 2015-16 = −1σ (dry), proving the year choice from our own data; (b) rating-curve fits (median R² ≈ 0.5); (c) station coverage of the study years. Message: the methodology is already being checked against evidence.

**11. ENSO scenario comparison — the experiment.** Run the calibrated model for **2011** and **2015-16**; compare sediment fluxes in time and **space** (which sub-basins drive the difference); attribute the signal (rainfall amount vs spatial pattern vs antecedent moisture). This is what the process model adds over correlations.

## Section C — Execution & plan (answers "how will you do all this": ~4 slides, ~25%)

**12. Team & work organization. [+colleague]** Who does what (TWILL, colleague, Omar): data collection (discharge/sediment by department + catalogue verification), preprocessing, calibration, analysis. Show it is a coordinated, division-of-labour effort.

**13. Progress to date.** Done: data collected & catalogue-verified (167 discharge / 77 sediment stations), full inventory + EDA notebook, download protocols. In progress: ERA5 (resumable), domain-box fix. This proves momentum.

**14. Work plan / timeline (the direct answer to the advisor).** A phased Gantt: (1) finish acquisition + domain box → (2) preprocessing (minibacias, URH, params) → (3) **hydrological** calibration/validation → (4) **sediment** calibration → (5) ENSO scenario runs → (6) analysis & report. Rough durations per phase. This slide *is* "comment comptez-vous faire tout cela."

**15. Risks & mitigations.** Sediment-data gap → tributary rating curves + direct concentration; ERA5 orographic bias → gauge bias-correction; whole-basin at 30 m infeasible → 90 m (justified); eastern domain clip → enlarge box. Showing you anticipate problems reassures the advisor.

## Section D — Close (~2 slides)

**16. Expected results & contribution.** First calibrated MGB-SED for the Magdalena; a process-based, spatial explanation of the ENSO sediment signal; a reusable, validated tool; deliverables (report, calibrated model, figures).

**17. References.** Fagundes et al.; Collischonn et al. (MGB); Restrepo et al. (Magdalena sediment/ENSO); Briceño et al. (ERA5 bias); MGB-SED plugin.

**Backup slides:** full model equations; extra EDA; station maps; pedotransfer formulas; rating-curve table.

---

## Colleague's work (yben409) — integration

Repo: `github.com/yben409/simulating-suspended-sediment-transport`. This is **the model engine**: a
**from-scratch, tested Python implementation of the full MGB-SED** (Fagundes et al. 2026 method), for the Magdalena.

**What it contains**
- Complete coupled model: MGB-IPH water balance, Penman–Monteith ET, three linear reservoirs, **local-inertial routing** (Bates 2010) + floodplain storage, **MUSLE** erosion with 2D LS factor, suspended-load advection (clay+silt), floodplain deposition.
- Preprocessing: DEM → unit catchments + reach geometry + LS2D; **12 HRUsed** (soil texture × land cover); IDW gauge forcing.
- Calibration: 3-stage + automated erosion-trigger fitting; **KGE** metrics; **ML** layer (RF/GBM/MLP with blocked CV) and a **rating-curve baseline** `SSC=aQ^b`; remote-sensing SSC retrieval (GLORIA → Landsat-8/Sentinel-2).
- **64 tests**, water/sediment/mass balance closure verified; runs end-to-end on synthetic data.

**The key synthesis (the story for the advisor).** yben409's README lists its #1 blocker as *"IDEAM does not publish SSC or discharge — the method collapses to an uncalibrated run."* **That blocker is now resolved by our team's data:** we downloaded **Caudal medio diario** (167 stations) and **Concentración media diaria** (77 stations) from the **DHIME portal** — a different access route than the open `datos.gov.co` API he checked. So: **he built the model that was waiting for data; we collected the data the model was waiting for.** The two halves meet.

**Reconciliation points to state honestly**
1. **Period.** His repo is currently set for **2016–2017**; our project is **2011 (La Niña) vs 2015–16 (El Niño)** — locked. Fix = re-point the run period (the model is data-driven, calibrated on the long record, so the run years are just a config change).
2. **Data-availability claim** in his README (SSC/Q "do not exist") must be updated — DHIME provides both; the open Socrata API does not. Both statements are true for their respective routes.
3. **Honest scope (use it — it *helps* us).** Even with full data, the paper's SSC KGE was −0.26 to 0.44; absolute tonnages are uncertain. **Defensible outputs are RELATIVE comparisons** (2011 vs 2015–16, Cauca vs Magdalena share) because model bias cancels in a ratio — which is *exactly* our ENSO comparison design. Frame the contribution as the relative signal, with explicit uncertainty on absolute loads. Suspended load only (no bedload), as in the paper.

**Where it slots into the deck (hydrology-focused)**
- **Slides 5–6 (model = hydrology):** use the **hydrological core** of his implementation — MGB-IPH water balance, linear reservoirs, local-inertial routing — to show "a **tested** hydrological engine already exists (mass/water balance closes; 64 conservation tests pass)". Do **not** feature the sediment/MUSLE/ML/remote-sensing modules here.
- **Slide 7 (data):** our DHIME collection resolves his data blocker → the **discharge** calibration can start now.
- **Slide 8 (preprocessing):** his `preprocess/` modules (terrain → unit catchments/minibacias, HRU, IDW forcing) = the concrete hydrology pipeline.
- **Slide 9 (calibration = hydrology):** discharge calibration with **KGE/NSE/PBIAS**, split-sample / **blocked CV** (no autocorrelation leakage). (His 3-stage optimiser is the tool; keep sediment-trigger fitting out.)
- **New synthesis slide** ("Two halves meet: model + data"): the narrative above, framed around enabling **hydrology** now.
- **Outlook slide (Section D):** the sediment side — data collected, rating-curve-ready, tested MGB-SED engine available — as the **next phase**, plus the honest relative-comparison / uncertainty framing (pre-empts the hardest question) kept brief.
- **Slide 12 (team):** yben409 = model engine; TWILL/Omar/3rd colleague = data acquisition & validation.

## Decisions locked
- **Language: English.**
- **Format: long (~30 min, ~22 slides).** Equations and extended EDA are promoted **into the body** (not backup).

## Long-format expansion (~22 slides, ~30 min)
Keep slides 1–17 above, with these additions/splits so the body carries the depth:
- **Model = hydrology, expanded across two slides (6a/6b, both hydrology).** **6a Water balance & runoff** (per-URH storage Wm, Penman–Monteith ET, saturation-excess runoff with the *b* parameter, interflow, baseflow). **6b Routing** (three linear reservoirs → channel; local-inertial river routing + floodplain storage). Full equations in the body. The **sediment equations are NOT here** — they move to a single outlook slide (see below).
- **+ Study area slide** (after 2): basin map, sub-basins, key stations (Calamar, Sogamoso), relief — grounds the audience geographically.
- **10 → 10a / 10b (hydrology EDA in the body).** **10a** ENSO validation (discharge anomaly +1.7σ / −1σ + hydrograph contrast 2011 vs 2015). **10b** discharge network & coverage (availability heatmap, seasonal bimodal cycle, stations/year). Use notebook-06 figures directly.
- **Sediment → one OUTLOOK slide only** (in Section D, near the end): "Next phase — sediment". States that the sediment data is already collected (77 CM stations) and rating-curve-ready, and that a tested MGB-SED engine exists to run it — but keeps it short and forward-looking, not a results section.
- **8 expanded** with a dedicated **pedotransfer** mini-slide (raw texture → K, Wm) since the advisor cares about *how* each input is derived.
- Keep **14 (work plan/timeline)** as a full slide — the centrepiece answer.

Time weighting (~30 min): Framing (A) ~5 min · **Methodology (B) ~15 min** · Execution/plan (C) ~7 min · Close (D) ~3 min.

## Still to confirm
1. Live **demo** (QGIS/notebook) or slides only?
2. **Colleague's git** → to slot their contribution into slides 7 (data), 8 (preprocessing, if applicable) and 12 (team).
3. Visual theme / any UMNG or EMINES template to match.
