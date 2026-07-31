"""
Re-download the 5 SoilGrids rasters on the CORRECTED domain box
(Xmin -77.0, Xmax -72.3, Ymin 1.4, Ymax 11.4) — EPSG:4326, ~250 m, int16,
matching the existing files exactly. Overwrites data/raw/soils/soilgrids_*.tif.

Source: ISRIC SoilGrids WCS (open data).
Requires: pip install owslib
Run:     python src/download_soilgrids.py
"""
import os
from owslib.wcs import WebCoverageService

# --- corrected box (Xmin, Xmax, Ymin, Ymax) ---
XMIN, XMAX, YMIN, YMAX = -77.0, -72.3, 1.4, 11.4
RES = 0.0022457      # ~250 m in degrees (matches the existing tifs)

# short name -> WCS coverage id (topsoil 0-5 cm, mean)
PROPS = {
    "clay": "clay_0-5cm_mean",
    "sand": "sand_0-5cm_mean",
    "silt": "silt_0-5cm_mean",
    "soc":  "soc_0-5cm_mean",
    "bdod": "bdod_0-5cm_mean",
}
OUTDIR = os.path.join("data", "raw", "soils")
os.makedirs(OUTDIR, exist_ok=True)

for short, cov in PROPS.items():
    out = os.path.join(OUTDIR, f"soilgrids_{short}.tif")
    url = f"https://maps.isric.org/mapserv?map=/map/{short}.map"
    print(f"downloading {short} ...", flush=True)
    try:
        wcs = WebCoverageService(url, version="1.0.0")
        resp = wcs.getCoverage(
            identifier=cov,
            crs="EPSG:4326",
            bbox=(XMIN, YMIN, XMAX, YMAX),   # (minx, miny, maxx, maxy)
            resx=RES, resy=RES,
            format="GEOTIFF_INT16",
        )
        with open(out, "wb") as f:
            f.write(resp.read())
        print(f"   wrote {out}")
    except Exception as e:
        print(f"   FAILED {short}: {e}")

print("\nDone. Check the 5 files in data/raw/soils/ (should span lon -77.0..-72.3).")
