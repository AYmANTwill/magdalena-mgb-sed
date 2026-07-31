"""
Automated download of IGAC department soil surveys (UCS polygons + texture text)
straight from the IGAC ArcGIS REST query API — no QGIS needed.

For each department it pages through .../MapServer/0/query (f=geojson, outSR=4326)
and writes data/raw/soils/suelos_<dept>.gpkg with ALL attributes (the texture lives
in the free-text field CARACTERÍSTICAS_SUELOS).

Requires:  pip install requests geopandas
Run:       python src/download_igac_soils.py
Resumable: already-downloaded departments are skipped.
"""
import os, time, requests, geopandas as gpd

BASE = "https://mapas.igac.gov.co/server/rest/services/agrologia/{svc}/MapServer/0/query"

# department -> exact IGAC service name (verified against the live server)
DEPTS = {
    "huila":            "mapageneraldesuelosdepartamentodehuila",
    "tolima":           "mapageneraldesuelosdepartamentodetolima",
    "cauca":            "mapageneraldesuelosdepartamentodecauca",
    "cundinamarca":     "mapageneraldesuelosdepartamentodecundinamarca",
    "boyaca":           "mapageneraldesuelosdepartamentodeboyaca",
    "caldas":           "mapageneraldesuelosdepartamentodecaldas",
    "risaralda":        "mapageneraldesuelosdepartamentoderisaralda",
    "quindio":          "mapageneraldesuelosdepartamentodequindio",
    "valledelcauca":    "mapageneraldesuelosdepartamentodevalledelcauca",
    "nortedesantander": "mapageneraldesuelosdepartamentodenortedesantander",
    "santander":        "mapageneraldesuelosdepartamentodeSantander",   # note: capital S on the server
}

OUTDIR = os.path.join("data", "raw", "soils")
os.makedirs(OUTDIR, exist_ok=True)
STEP = 2000   # = the service maxRecordCount


def fetch_department(svc):
    url = BASE.format(svc=svc)
    feats, offset = [], 0
    while True:
        params = {"where": "1=1", "outFields": "*", "returnGeometry": "true",
                  "outSR": "4326", "f": "geojson",
                  "resultOffset": offset, "resultRecordCount": STEP}
        for attempt in range(3):
            try:
                r = requests.get(url, params=params, timeout=180); r.raise_for_status()
                js = r.json(); break
            except Exception as e:
                if attempt == 2: raise
                time.sleep(5)
        batch = js.get("features", [])
        feats += batch
        print(f"    {len(feats)} features", end="\r")
        if len(batch) < STEP:          # last page
            break
        offset += STEP; time.sleep(0.4)
    return feats


for dep, svc in DEPTS.items():
    out = os.path.join(OUTDIR, f"suelos_{dep}.gpkg")
    if os.path.exists(out):
        print(f"skip {dep} (already present)"); continue
    print(f"downloading {dep} ...")
    try:
        feats = fetch_department(svc)
        if not feats:
            print(f"   {dep}: NO FEATURES (check the service name)"); continue
        gdf = gpd.GeoDataFrame.from_features(feats, crs="EPSG:4326")
        gdf.to_file(out, driver="GPKG")
        has_tex = any("CARACTER" in c.upper() for c in gdf.columns)   # texture field = CARACTERISTICAS
        print(f"   wrote {out}  ({len(gdf)} polygons, {len(gdf.columns)-1} fields, texture field present: {has_tex})")
    except Exception as e:
        print(f"   FAILED {dep}: {e}")

print("\nDone. GeoPackages are in data/raw/soils/. Tell TWILL — the notebook will merge them basin-wide.")
