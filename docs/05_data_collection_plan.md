# Data collection plan (MGB-SA / hydrology)

Living checklist of every dataset needed to build and calibrate MGB-SA on the Magdalena. Sediment-specific data
(IDEAM sediment stations, MUSLE factors) are deferred with the sediment module.

## Study area

- **Target:** the whole Magdalena basin (advisor's brief).
- **Pilot (build first):** upper + middle Magdalena, from the Andean headwaters down to a mid-basin gauge
  (~Puerto Berrío / Barrancabermeja), ~80,000–110,000 km², at full 30 m — under IPH's ~250 M cell limit.
- **Provisional bounding box for the DEM download:** lat **1.8°–7.0° N**, lon **76.7°–73.3° W**
  (generous, must fully contain the pilot watershed; the true boundary comes from delineation).
- Exact outlet is fixed once the calibration gauge is chosen from IDEAM.

## Accounts / API keys to create first (all free)

- **OpenTopography** — API key, for the DEM download.
- **Copernicus Climate Data Store (CDS)** — account + API key, for ERA5 climate.
- **IDEAM / DHIME** — no key; a public portal, data requested/exported online.

## Datasets

| # | Dataset | Used for | Source | Access | Native res | Status |
|---|---------|----------|--------|--------|-----------|--------|
| 1 | DEM | terrain → minibacias, slopes, LS | OpenTopography — Copernicus GLO-30 | API key | 30 m | to download |
| 2 | Soils | URH; erodibility K | IGAC geoportal (Colombia) | web download | vector | to download |
| 3 | Land cover | URH; cover factor C | ESA WorldCover | web / S3 | 10 m | to download |
| 4 | Climate (daily) | forcing: precip, T, radiation, wind, humidity, pressure | Copernicus CDS — ERA5 | account + key | ~31 km | to download |
| 5 | Discharge (observed) | hydrological calibration | IDEAM / DHIME | portal | station series | to identify |

## Ordered steps

1. **DEM** — download GLO-30 for the bounding box → `data/raw/dem/`. Convert to `.asc`, force `NODATA = -9999`.
2. **Discharge stations** — on DHIME, list IDEAM discharge gauges inside the pilot; pick the outlet gauge (this
   finalizes the pilot boundary) and note record length vs candidate years.
3. **Land cover** — download WorldCover tiles covering the box → `data/raw/landcover/`; reclass to hydrological classes.
4. **Soils** — download IGAC soils for the area → `data/raw/soils/`; reclass to hydrological groups.
5. **Align** — reproject/resample soils + land cover to the DEM grid (projection, resolution, extent).
6. **Climate** — download ERA5 daily variables for the box and period → `data/raw/climate/`; plan bias correction
   against IDEAM precipitation (H4).

## Conventions

- Raw data in `data/raw/` (git-ignored). Processed/aligned products in `data/processed/`.
- Record source, download date, resolution, and projection for every dataset added.
- All rasters aligned to the DEM grid before crossing (URH) — the URH analogue of "NODATA = -9999".
