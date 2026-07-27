# Methodology (workflow)

The project follows the MGB-SED workflow, phased. Hydrology is always calibrated **before** sediments.

## Phase 0 — Environment (DONE)

- QGIS 3.44 LTR (French UI), system decimal separator set to **point** (else IPH-HydroTools fails).
- Plugins installed and working: **IPH-HydroTools** (2025), **MGB** (Dec 2025), **MGB-SED**.
- End-to-end preprocessing tested on a **~3000 km² test zone** (upper Magdalena, Copernicus GLO-30 from OpenTopography):
  DEM → `.asc` (NODATA forced to -9999) → Sink and Destroy → Flow Direction → Flow Accumulation →
  Stream Definition (threshold 1000 cells) → Stream Segmentation → Watershed Delineation → Catchment Delineation
  → **198 minibacias**. Files kept in `D:\test\`.

## Phase 1 — Data preparation (IN PROGRESS)

### 1a. DEM → hydrological structure (understood; see notebook 01)
IPH-HydroTools turns a DEM into flow directions, network and minibacias by repeating one rule — water follows the
steepest descent, cell by cell. Minibacias are the MGB computation units, linked by upstream→downstream topology.
The maths of each transformation are worked out by hand in `notebooks/01_dem_preprocessing.ipynb`.

### 1b. URH generation (understood; see notebook 02)
Cross soil (IGAC) × land cover (WorldCover/IDEAM), cell by cell, on the aligned DEM grid → URH grid → per-minibacia
URH fractions. Worked out in `notebooks/02_urh_soil_landuse.ipynb`.

### 1c. Convert minibacias to MGB format (`mini.gtb`) — TODO.

## Phase 2 — Hydrological calibration (NOT STARTED)

- Force MGB-SA with bias-corrected climate (ERA5 vs IDEAM).
- Calibrate hydrological parameters against IDEAM **discharge** at selected stations.
- Evaluate with NSE / KGE / PBIAS.

## Phase 3 — Sediment calibration (NOT STARTED)

- Compute MUSLE factors (K, LS, C, P) from soils / DEM / land use.
- Calibrate **α, β** using the **rain/slope threshold** technique of Fagundes et al. to isolate erosive events.
- Validate against IDEAM **sediment** records.

## Phase 4 — Scenario comparison (NOT STARTED)

- Run the calibrated model for the **La Niña (2011)** and **El Niño (2015–2016 / 2017)** years.
- Compare suspended sediment fluxes; attribute differences to hydro-climatic drivers.

## Phase 5 — Analysis and reporting (NOT STARTED)

- Uncertainty-aware interpretation, figures, final report (UMNG) and EMINES defense material.

## Cross-cutting decisions (see open_questions.md)

- Sediment stations (feasibility) · confirm years · whole basin vs sub-basin (cell-count limit).
