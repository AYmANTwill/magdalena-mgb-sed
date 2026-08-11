# Report outline — MGB-SED / Magdalena (UMNG internship · EMINES)

> **STATUS — STALE.** Every `[done]/[in progress]/[pending]` tag below predates docs/16 and everything after it; the report itself has not been written. For what the project now claims, read [docs/00_INDEX.md](00_INDEX.md) §4. The *presentation* deliverables that were produced are [docs/24](24_presentation_outline.md), [docs/27](27_presentation_script.md) and [docs/28](28_presentation_explained.md).

Structure for the internship report. EMINES evaluates two components: a **research component** (this modelling study,
assessed by UMNG via the report) and a **human-experience component** (a focused Colombia/Morocco comparison). Both are
covered below. Status tags: **[done]**, **[in progress]**, **[pending]**.

---

## Front matter
- Title, author, advisor (Prof. Briceño Zuluaga), UMNG / EMINES, date.
- **Abstract** — 200–250 words: question, method (MGB-SED), key result (La Niña vs El Niño sediment flux), significance. **[pending — write last]**

## 1. Introduction
- 1.1 Context — suspended sediment in tropical Andean rivers; the Magdalena's role and sediment yield. **[done — see docs/01]**
- 1.2 ENSO and sediment — why La Niña/El Niño should change fluxes. **[done — docs/00, 07]**
- 1.3 Problem statement & research question. **[done — docs/00]**
- 1.4 Objectives and **hypotheses** (H1–H4). **[done — docs/00]**
- 1.5 The approach transposed (Fagundes et al., southern Brazil). **[done — docs/01]**

## 2. Study area
- 2.1 The Magdalena basin — geography, relief (Andes → Caribbean), the source/sink contrast. **[done — terrain map, notebook 04]**
- 2.2 Study years — La Niña 2011 vs El Niño 2015–2016 (ONI justification; 2017 excluded). **[done — docs/07]**
- 2.3 Domain / outlet decision (whole basin vs pilot; mainstem vs tributary calibration). **[pending — advisor]**

## 3. The MGB-SED model
- 3.1 Overview — MGB-SA (hydrology/hydrodynamics) + MGB-SED (sediment); coupling order. **[done — docs/04, notebooks 01–03]**
- 3.2 Hydrology — water balance per URH, saturation-excess runoff, routing. **[done — notebook 03]**
- 3.3 Sediment — MUSLE hillslope erosion, Exner channel routing. **[pending — notebook 06]**

## 4. Data
- 4.1 DEM (Copernicus GLO-30) and preprocessing. **[done — notebook 04]**
- 4.2 Soils (IGAC) and land cover (WorldCover) → URH. **[done — notebook 05]**
- 4.3 Climate forcing (ERA5-Land) and bias correction plan. **[in progress — download]**
- 4.4 Observed data (IDEAM) — discharge (Calamar) and the **sediment-data situation** (mainstem gap; tributary
  stations covering 2011 & 2015–2016). **[done — docs/06; a genuine finding worth a subsection]**

## 5. Methodology
- 5.1 Physical structure — DEM → minibacias (IPH-HydroTools); stream-threshold choice. **[pending — after domain]**
- 5.2 URH generation — reclassification schemes; per-minibacia composition. **[reclassification done — notebook 05; composition pending]**
- 5.3 Hydrological calibration — parameters (Wm, b, Kint, Kbas); metrics (NSE/KGE/PBIAS); calibration/validation split. **[pending]**
- 5.4 Sediment calibration — MUSLE α, β; **multi-gauge calibration on tributary stations**; Fagundes rain/slope thresholds. **[pending]**
- 5.5 Scenario protocol — run calibrated model for the two ENSO years; comparison metrics. **[pending]**

## 6. Results
- 6.1 Basin structure (minibacias, URH maps). **[partial — URH map done]**
- 6.2 Hydrological calibration performance. **[pending]**
- 6.3 Sediment calibration performance. **[pending]**
- 6.4 **La Niña 2011 vs El Niño 2015–2016** — sediment fluxes, spatial patterns, hydrographs/sedigraphs. **[pending — core result]**

## 7. Discussion
- 7.1 Interpretation — drivers of the difference; where sediment is produced vs deposited. **[pending]**
- 7.2 Uncertainties & limitations — ERA5 bias over the Andes; no mainstem sediment validation; land-cover vintage;
  first-pass soil grouping. **[framework done — see journal/open_questions]**
- 7.3 Comparison with the literature (Restrepo, Higgins, Fagundes). **[pending]**

## 8. Conclusion & perspectives. **[pending]**

## 9. References. **[in progress — docs/01]**

## Appendices
- A. Data sources & download procedures. **[done — docs/05, 08]**
- B. Reproducible workflow (notebooks 01–05, repository). **[done]**
- C. Open decisions log. **[done — docs/open_questions]**

---

## Human-experience component (EMINES) — separate section or annex
- Framing: a focused **Colombia vs Morocco** comparison on one well-defined dimension (to fix with the advisor).
  Candidate axes: research-data accessibility (IDEAM/DHIME vs Moroccan agencies), water/sediment management institutions,
  or the working/academic environment. **[pending — pick the axis]**
- Keep it concrete and evidence-based, mirroring the rigor of the technical part.
