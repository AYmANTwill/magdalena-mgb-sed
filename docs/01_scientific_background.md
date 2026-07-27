# Scientific background and references

## The MGB / MGB-SED model family

**MGB** (Modelo de Grandes Bacias, IPH-UFRGS, Brazil) is a large-scale, semi-distributed hydrological–hydrodynamic
model. The catchment is discretized into **minibacias** (unit-catchments) connected by an upstream→downstream
topology; within each minibacia the land is split into **HRUs / URH** (Hydrological Response Units) obtained by
crossing soil and land-use maps. Vertical water balance is computed per URH; lateral routing uses a
**local inertial** (hydrodynamic) method coupled to floodplain storage.

**MGB-SED** adds a sediment module on top of MGB:
- **Hillslope erosion** per minibacia via **MUSLE** (Modified Universal Soil Loss Equation), which uses the
  **runoff volume × peak flow** produced by the hydrology (hence hydrology must be calibrated first).
- **Channel routing** of sediment via **Exner** and 1-D transport equations, with channel erosion/deposition and
  floodplain exchanges.

## The Fagundes et al. approach (what we transpose)

Fagundes and co-authors applied MGB-SED across South America and to specific flood events, developing a workflow
for **event-based sediment analysis** and a **rain/slope threshold** technique to isolate erosive events. The core
transposition of this internship is to apply that workflow to the **Magdalena** for two contrasting ENSO years.

## Reference list (advisor-provided + core)

> Links are to ResearchGate / official portals as provided. Full citations to be completed as PDFs are read.

- **MGB-SED plugin (QGIS)** — source and documentation:
  `https://github.com/LabHig-Ufes/MGB-SED`
- **Fagundes et al.** — *Sediment Flows in South America Supported by Daily Hydrologic-Hydrodynamic Modeling*
  (ResearchGate publication 347968751). Foundational for the method.
- **Fagundes et al.** — *Human-induced changes in South American sediment fluxes from 1984 to 2019*
  (ResearchGate publication 367392618). Context on anthropogenic sediment change.
- **MGB-SED graphic interface & automatic calibration module** — *Development of a graphic interface and an
  automatic calibration module for MGB-SED model* (ResearchGate publication 328290560). Relevant to α/β calibration.
- **Briceño Zuluaga et al.** — advisor's work noting **ERA5/reanalysis bias over mountainous terrain**
  (motivates bias correction, H4).
- **Climate forcing** — Copernicus ERA5 single levels:
  `https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels`
- **In-situ measurements (Colombia)** — IDEAM citizen-service / DHIME portal:
  `https://atencionciudadano.ideam.gov.co/`

## Notes on documentation language

MGB / IPH-HydroTools documentation is largely in **Portuguese**; terminology is mapped to English/French in the
progress journal as encountered.
