# Presentation plan — MGB-SED / Magdalena (methodology-focused)

**Audience:** Prof. Briceño Zuluaga (UMNG, EMINES).
**Framing (critical):** the advisor's reply to our proposed solutions was *"how do you plan to do all this?"* — so the **spine of the deck is the methodology and the work plan**, not the context. Every slide should visibly answer *how*. Context/motivation is kept to a minimum; the middle third (model + preprocessing + calibration) and the work plan are the heart.
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

## Decisions locked
- **Language: English.**
- **Format: long (~30 min, ~22 slides).** Equations and extended EDA are promoted **into the body** (not backup).

## Long-format expansion (~22 slides, ~30 min)
Keep slides 1–17 above, with these additions/splits so the body carries the depth:
- **6 → 6a / 6b.** Split the model equations across two slides: **6a Hydrology** (water balance, Penman ET, saturation-excess runoff with *b*, interflow, baseflow) and **6b Sediment** (MUSLE hillslope erosion K·LS·C·P·α·β, Exner channel transport). Full equations in the body.
- **+ Study area slide** (after 2): basin map, sub-basins, key stations (Calamar, Sogamoso), relief — grounds the audience geographically.
- **10 → 10a / 10b.** Extended EDA in the body: **10a** ENSO validation (anomaly + hydrograph contrast) and **10b** sediment/rating-curve evidence (log-normal concentration + fitted Qs=a·Q^b + coverage). Use notebook-06 figures directly.
- **8 expanded** with a dedicated **pedotransfer** mini-slide (raw texture → K, Wm) since the advisor cares about *how* each input is derived.
- Keep **14 (work plan/timeline)** as a full slide — the centrepiece answer.

Time weighting (~30 min): Framing (A) ~5 min · **Methodology (B) ~15 min** · Execution/plan (C) ~7 min · Close (D) ~3 min.

## Still to confirm
1. Live **demo** (QGIS/notebook) or slides only?
2. **Colleague's git** → to slot their contribution into slides 7 (data), 8 (preprocessing, if applicable) and 12 (team).
3. Visual theme / any UMNG or EMINES template to match.
