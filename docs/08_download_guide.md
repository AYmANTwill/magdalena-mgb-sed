# Data download guide (step by step)

> **STATUS — recipes LIVE, bounding box SUPERSEDED.** The portal click-paths below are still the way to fetch each dataset, but the pilot box quoted in the next line is obsolete — the locked domain is `Xmin −77.0, Xmax −72.3, Ymin 1.4, Ymax 11.4` ([docs/15](15_domain_correction.md)). Entry point: [docs/00_INDEX.md](00_INDEX.md).

Current pilot region (lower Magdalena, near the sea): **Xmin −75.4, Xmax −73.7, Ymin 8.2, Ymax 11.3** (WGS84, EPSG:4326).
Save each dataset into its `data/raw/<folder>/`.

## 1. DEM — OpenTopography (Copernicus GLO-30, 30 m)

1. Go to **portal.opentopography.org** → create a free account and log in.
2. Data → **Global DEMs → Copernicus GLO-30**.
3. Enter the box (Xmin/Xmax/Ymin/Ymax) or draw it on the map. Type minus signs from the keyboard.
4. Output format **GeoTIFF** → submit → wait for the job.
5. If it is rejected as too large, split into two latitude halves and I will merge them in Python.
6. Save to `data/raw/dem/`.

## 2. Land cover — ESA WorldCover (10 m)

*Pilot:* WorldCover 2021 is fine. *For the study years* use period-matched cover (see note at the end).

1. Go to **esa-worldcover.org** → "View & download" → opens the viewer (**viewer.esa-worldcover.org**).
2. Pan/zoom to the region.
3. Use the download tool and select the 3°×3° tiles overlapping the box (here the tiles covering ~lat 6–12° N,
   lon 75–72° W — e.g. `N09W075`, `N06W075`, plus the `W078` tiles for the small western sliver).
4. Choose the **2021 v200** layer → download the GeoTIFF(s) → accept the licence.
5. Save to `data/raw/landcover/`.
   *Bulk alternative:* the public AWS bucket `s3://esa-worldcover` (tiles by name).

## 3. Soils — SoilGrids (global) or IGAC (Colombia)

**SoilGrids (easier, global 250 m):**
1. Go to **soilgrids.org** (ISRIC) → map viewer.
2. Download the properties needed for MUSLE erodibility K and water storage: **sand, silt, clay, organic carbon (SOC),
   bulk density** for the topsoil (0–5 / 5–15 cm).
3. Export for the box (viewer download, or the WCS/WebDAV at files.isric.org) → GeoTIFF per property.
4. Save to `data/raw/soils/`.

**IGAC (Colombia) — WORKING ROUTE via QGIS + ArcGIS REST (verified 2026-07-27).**
The website download is deprecated (the old open-data page redirects to the view-only Colombia-en-Mapas viewer). But the
data is live on IGAC's ArcGIS REST server as **queryable polygon feature layers**, one soil map per department, which
QGIS can load and export directly.

1. In QGIS → Browser panel → **ArcGIS REST Servers → New Connection**: name `IGAC`, URL
   `https://mapas.igac.gov.co/server/rest/services`.
2. Expand **IGAC → agrologia**. The soil maps are `mapageneraldesuelosdepartamentode<dept>`. For the lower-Magdalena box:
   `...magdalena`, `...atlantico`, `...bolivar`, `...cesar`, `...cordoba`, `...sucre`.
3. Drag each service's layer (layer 0, `esriGeometryPolygon`, capabilities Map/Query/Data) into the map.
4. Right-click → Export → **Save Features As…** → GeoPackage/Shapefile → `data/raw/soils/suelos_<dept>.gpkg`.
5. Source CRS is EPSG:9377 (MAGNA-SIRGAS Origen Nacional) — merge/reproject/clip to the basin in Python.

Each service also exposes WFS/WMS at `.../MapServer/WFSServer` if the REST route is unavailable.
Soil surveys are 1:100,000 (e.g. Magdalena published 2009). SoilGrids remains the global fallback.

## 4. IDEAM discharge & sediment — DHIME portal

1. Go to **dhime.ideam.gov.co** → "Consulta y Descarga de Datos".
2. Filter by parameter: **Caudal** (discharge) and **Transporte de sedimentos / Concentración de sedimentos**.
3. Filter by area (departamento) or search station names (e.g. **Calamar**).
4. Select the station(s) → set the date range (e.g. 2009–2018 to cover both study years) → download CSV/Excel.
5. Record what exists per station and parameter (especially sediment for 2011 and 2015–2016).
6. Save to `data/raw/observed/`.
   Also grab the **Catálogo Nacional de Estaciones** (datos.gov.co) for station coordinates and operating periods.

## 5. Climate — ERA5-Land, Copernicus CDS (via the CDS API — the web form can't handle multi-year requests)

**Years (deduced):** continuous **2009–2017** — warm-up 2009–2010, La Niña 2011, fill 2012–2014, El Niño 2015–2016,
buffer 2017. Warm-up is needed so soil-moisture/groundwater stores are realistic at the start of each event year.
**Area (box):** `[North, West, South, East] = [11.3, -75.4, 8.2, -73.7]`.
**Variables:** total precipitation, 2 m temperature, 2 m dewpoint (humidity), surface solar radiation downwards,
10 m u/v wind, surface pressure.

Steps:
1. **cds.climate.copernicus.eu** → register/log in → open "ERA5-Land hourly" → Download tab → **Accept** the licence.
2. Profile page → copy your **Personal Access Token**.
3. Create `C:\Users\<you>\.cdsapirc`:  `url: https://cds.climate.copernicus.eu/api`  and  `key: <token>`.
4. `pip install "cdsapi>=0.7"`.
5. Run **`python src/download_era5.py`** from the repo root → NetCDF per year into `data/raw/climate/`.

If region/years change (advisor), edit `YEARS`/`AREA` at the top of `src/download_era5.py` and re-run.

---

**Land-cover timing note.** WorldCover only exists for 2020/2021. For the actual study years use period-matched cover:
**IDEAM Corine Land Cover Colombia** (has a ~2010–2012 epoch matching La Niña 2011, and later epochs) or **ESA CCI Land
Cover** (annual, 1992–2020, 300 m). WorldCover is fine for building the pilot workflow.
