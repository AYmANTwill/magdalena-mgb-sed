# data

Inputs are **not versioned** (large / external). This folder documents what belongs here and how to get it.

## data/raw/  (external, gitignored)
- `dem/` — ALOS World 3D 30 m or Copernicus GLO-30 (OpenTopography). Force `NODATA_value` to -9999.
- `soils/` — IGAC soil map.
- `landcover/` — ESA WorldCover or IDEAM.
- `climate/` — Copernicus ERA5 (precip, temperature, radiation, wind, humidity, pressure).
- `observed/` — IDEAM discharge and sediment series (DHIME portal).

## data/processed/  (gitignored)
- Aligned rasters (reprojected/resampled to the DEM grid).
- `mini.gtb`, URH table, MGB-format forcing files.

## Conventions
- All rasters aligned to the DEM grid (projection, resolution, extent) before crossing.
- Keep a note of source, date, and resolution for every dataset added.
