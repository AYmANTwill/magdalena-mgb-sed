# Data sources (model inputs)

Inputs are grouped by role: data that build the **physical structure**, **climate forcing**, **parameters**, and
**observed data** used for calibration/validation. See `04_model_structure.md` for the flow diagram.

## 1. Spatial data — physical structure

| Data | Source (Colombia) | Role | Feeds | Status |
|------|-------------------|------|-------|--------|
| DEM | ALOS World 3D 30 m, or Copernicus GLO-30 (OpenTopography) | minibacias, network, slopes, drainage areas | MGB-SA + MGB-SED | GLO-30 tested on 3000 km² test zone |
| Soil map | IGAC | erodibility (K) + water storage | URH | to obtain |
| Land cover | ESA WorldCover, or IDEAM | cover factor (C) | URH | to obtain |

Crossing **soil × land cover** produces the **URH**; each minibacia is described by a vector of URH area fractions.

## 2. Climate forcing (daily, over the simulated period)

- **Precipitation** — main forcing (Copernicus ERA5, or IDEAM gauges interpolated).
- For **evapotranspiration** (Penman-Monteith): temperature, solar radiation, wind speed, relative humidity, pressure.
- ⚠️ **Bias correction** of precipitation against IDEAM stations is required over mountainous terrain (H4).

## 3. Parameters (calibrated, in order)

- **Hydrological (MGB-SA), per URH**: max soil storage `Wm`, shape parameter `b`, baseflow `Kbas`, interflow `Kint`, etc.
  → calibrated on **discharge**.
- **Sediment (MGB-SED)**: MUSLE factors — erodibility `K` (soils), topographic `LS` (from DEM), cover `C` (land use),
  practice `P` — and the calibration coefficient/exponent **α, β**. Channel: grain size / settling velocity for Exner routing.
  → calibrated on **suspended sediment**.

> MUSLE uses **runoff volume × peak flow**, not raw rainfall → hydrology must be calibrated before sediments.

## 4. Observed data for calibration/validation (critical)

| Data | Source | Purpose | Status |
|------|--------|---------|--------|
| Discharge time series | IDEAM hydrological stations | hydrological calibration | to identify |
| Suspended sediment concentration / load | IDEAM **sediment** stations (DHIME portal) | sediment calibration | **BLOCKING — to secure first** |

## 5. MGB configuration files (produced from the above)

- `mini.gtb` — minibacia table + topology (from preprocessing).
- URH table — per-minibacia URH fractions.
- Climate/rainfall forcing files in MGB format.
- Parameter file.

## Data handling conventions

- All rasters must be **aligned** to the DEM grid (same projection, resolution, extent) before crossing.
- DEM `NODATA_value` must be forced to **-9999** for IPH-HydroTools.
- Raw data live in `data/raw/` (not versioned); processed products in `data/processed/`. See `../data/README.md`.
