"""
Download ERA5-Land forcing for the MGB-SA model (lower-Magdalena pilot).

Prerequisites (see docs/08_download_guide.md, section 5):
  1. Free account at https://cds.climate.copernicus.eu  and accept the ERA5-Land licence.
  2. Put your API key in  C:\\Users\\<you>\\.cdsapirc  (Windows) — two lines:
         url: https://cds.climate.copernicus.eu/api
         key: <YOUR-API-KEY>
  3. pip install "cdsapi>=0.7"

Run from the repo root:  python src/download_era5.py
Files land in data/raw/climate/  (one NetCDF per year). CDS queues requests, so it can take a while.
"""
import os
import cdsapi

# --- Study window ---------------------------------------------------------
YEARS = [str(y) for y in range(2009, 2018)]      # 2009-2017 (warm-up + La Nina 2011 + El Nino 2015-2016 + buffer)
AREA = [11.3, -75.4, 8.2, -73.7]                 # North, West, South, East  (lower-Magdalena box)

# --- Variables MGB needs (precip + Penman-Monteith ET) --------------------
VARIABLES = [
    "total_precipitation",
    "2m_temperature",
    "2m_dewpoint_temperature",            # -> relative humidity
    "surface_solar_radiation_downwards",
    "10m_u_component_of_wind",            # -> wind speed (with v)
    "10m_v_component_of_wind",
    "surface_pressure",
]

OUTDIR = os.path.join("data", "raw", "climate")
os.makedirs(OUTDIR, exist_ok=True)

client = cdsapi.Client()

MONTHS = [f"{m:02d}" for m in range(1, 13)]

# One request per (year, month) — a full year of hourly data exceeds CDS cost limits,
# so we split by month. ~108 small files; re-running skips what already downloaded.
for year in YEARS:
    for month in MONTHS:
        out = os.path.join(OUTDIR, f"era5land_{year}_{month}.nc")
        if os.path.exists(out):
            print(f"[skip] {out} already exists")
            continue
        print(f"[request] ERA5-Land {year}-{month} -> {out}")
        client.retrieve(
            "reanalysis-era5-land",
            {
                "variable": VARIABLES,
                "year": year,
                "month": [month],
                "day":   [f"{d:02d}" for d in range(1, 32)],
                "time":  [f"{h:02d}:00" for h in range(24)],
                "area":  AREA,
                "data_format": "netcdf",
                "download_format": "unarchived",
            },
            out,
        )
        print(f"[done] {out}")

print("All requested months downloaded.")
