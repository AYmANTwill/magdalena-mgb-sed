"""
Build the basin-wide soil-texture-family layer used by notebook 08 (the URH).

Primary source = IGAC field survey (the 18 in-basin department soil maps in
data/raw/soils/suelos_<dept>.gpkg, downloaded via src/download_igac_soils.py).
For each UCS polygon we parse the free-text soil description and assign a texture
family (1=Coarse, 2=Medium, 3=Fine). SoilGrids (same USDA triangle, collapsed to
3 families) fills the ~14 % of the basin IGAC does not cover.

Why IGAC over SoilGrids: SoilGrids collapses ~95 % of the basin to "Fine" (a global
250 m ML artefact); IGAC shows the real Coarse/Medium volcanic-Andean soils. The two
agree on only ~39-47 % of cells, so the choice materially changes runoff & MUSLE-K.

Output: data/processed/soil_family_igac.tif  (uint8, on the minibacias.tif grid,
        1=Coarse 2=Medium 3=Fine, 0=nodata).

Requires: geopandas, rasterio, pandas, numpy
Run:      python src/build_soil_layer.py
"""
import glob, os, re, shutil, tempfile, pathlib
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from rasterio.features import rasterize
from rasterio.warp import reproject, Resampling

REPO = pathlib.Path(__file__).resolve().parents[1]
SOILS = REPO / "data" / "raw" / "soils"
MINIB = REPO / "data" / "processed" / "minibacias.tif"
OUT   = REPO / "data" / "processed" / "soil_family_igac.tif"

FAM = {"Coarse": 1, "Medium": 2, "Fine": 3}

# IGAC gpkgs to skip (outside the Magdalena-Cauca drainage)
SKIP = {"laguajira"}


def texfam(t):
    """First texture keyword in the IGAC free-text description -> family code (0 = none)."""
    t = str(t).lower()
    best, bestpos = None, 1e9
    for pat, fam in [
        (r"muy\s+fina", "Fine"), (r"franco\s*arcillos", "Fine"), (r"arcillos", "Fine"), (r"\bfina", "Fine"),
        (r"franco\s*arenos", "Medium"), (r"franco\s*limos", "Medium"), (r"\bmedia", "Medium"),
        (r"\bfranc", "Medium"), (r"limos", "Medium"),
        (r"gruesa", "Coarse"), (r"arenos", "Coarse"),
    ]:
        m = re.search(pat, t)
        if m and m.start() < bestpos:
            bestpos, best = m.start(), fam
    return FAM.get(best, 0)


def pick_texcol(cols):
    """Name-guided selection of the soil-characteristics column.

    IGAC services are inconsistent: CARACTERISTICAS, CARACTERISTICAS_SUELOS,
    CARACTERÍSTICAS_RELIEVE_Y_SUELOS, ... We ONLY accept columns that name the SOIL
    (never RELIEVE-only, never COMPONENTES_TAXONOMICOS, which would falsely match keywords).
    """
    up = {c: c.upper() for c in cols}
    return [c for c in cols
            if "CARACTER" in up[c]
            and ("SUELO" in up[c] or up[c] == "CARACTERISTICAS" or "RELIEVE_Y_SUELOS" in up[c])
            and not up[c].endswith("RELIEVE")]


def main():
    assert MINIB.exists(), "Run notebook 07 first (needs data/processed/minibacias.tif)."
    with rasterio.open(MINIB) as ds:
        subs = ds.read(1); tr = ds.transform; H, W = ds.height, ds.width
        prof = ds.profile
    bas = subs > 0

    # ---- 1. merge every in-basin IGAC department, correct CRS + correct texture column ----
    frames = []
    for fp in sorted(glob.glob(str(SOILS / "suelos_*.gpkg"))):
        dep = os.path.basename(fp)[7:-5]
        if dep in SKIP:
            continue
        g = gpd.read_file(fp)
        if g.crs is None:                       # older QGIS exports are MAGNA-SIRGAS Origen-Nacional
            g = g.set_crs(9377, allow_override=True)
        g = g.to_crs(4326)
        cand = pick_texcol(g.columns)
        if not cand:
            print(f"  {dep}: no soil-characteristics column -> skipped"); continue
        col = max(cand, key=lambda c: (g[c].apply(texfam) > 0).mean())
        g["fam"] = g[col].apply(texfam)
        cov = (g["fam"] > 0).mean()
        print(f"  {dep:18} col={col:34} texture coverage {100*cov:4.0f}%")
        frames.append(g[["fam", "geometry"]][g["fam"] > 0])
    ig = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=4326)
    igr = rasterize(((geom, int(f)) for geom, f in zip(ig.geometry, ig.fam)),
                    out_shape=(H, W), transform=tr, fill=0, dtype="uint8")

    # ---- 2. SoilGrids fallback (USDA triangle -> 3 families) ----
    def load(n):
        with rasterio.open(SOILS / f"soilgrids_{n}.tif") as s:
            o = np.zeros((H, W), "float32")
            reproject(rasterio.band(s, 1), o, dst_transform=tr, dst_crs="EPSG:4326",
                      resampling=Resampling.bilinear)
        return o
    clay, sand, silt = load("clay"), load("sand"), load("silt")
    v = (clay > 0) & (sand > 0) & (silt > 0)
    C = np.where(v, clay/10., np.nan); S = np.where(v, sand/10., np.nan); Si = np.where(v, silt/10., np.nan)
    tot = C + S + Si; C, S, Si = C/tot*100, S/tot*100, Si/tot*100
    conds = [(Si+1.5*C) < 15, ((Si+1.5*C) >= 15) & ((Si+2*C) < 30),
             (((C >= 7) & (C < 20) & (S > 52) & ((Si+2*C) >= 30)) | ((C < 7) & (Si < 50) & ((Si+2*C) >= 30))),
             (C >= 7) & (C < 27) & (Si >= 28) & (Si < 50) & (S <= 52),
             ((Si >= 50) & (C >= 12) & (C < 27)) | ((Si >= 50) & (Si < 80) & (C < 12)),
             (Si >= 80) & (C < 12), (C >= 20) & (C < 35) & (Si < 28) & (S > 45),
             (C >= 27) & (C < 40) & (S > 20) & (S <= 45), (C >= 27) & (C < 40) & (S <= 20),
             (C >= 35) & (S > 45), (C >= 40) & (Si >= 40), (C >= 40) & (S <= 45) & (Si < 40)]
    usda = np.select(conds, list(range(1, 13)), default=0)
    U2F = {1:1,2:1,3:1,4:2,5:2,6:2,7:2,8:3,9:3,10:3,11:3,12:3}
    sgf = np.zeros((H, W), "uint8")
    for u, f in U2F.items():
        sgf[usda == u] = f

    # ---- 3. combine: IGAC where present, SoilGrids elsewhere; mask to basin ----
    final = np.where(igr > 0, igr, sgf)
    final = np.where(bas, final, 0).astype("uint8")

    m = (igr > 0) & (sgf > 0) & bas
    print(f"\nIGAC covers {100*np.mean(igr[bas] > 0):.1f}% of basin; IGAC vs SoilGrids agreement {100*np.mean(igr[m]==sgf[m]):.0f}%")
    inv = {1: "Coarse", 2: "Medium", 3: "Fine"}
    print("final basin family %:", {inv[k]: round(100*float(np.mean(final[bas]==k)), 1) for k in (1, 2, 3)})

    # ---- 4. write (temp then copy: the mount forbids unlink-overwrite) ----
    prof.update(count=1, dtype="uint8", nodata=0, compress="lzw")
    tmp = str(pathlib.Path(tempfile.gettempdir()) / "soil_family_igac.tif")
    with rasterio.open(tmp, "w", **prof) as d:
        d.write(final, 1)
    shutil.copyfile(tmp, OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
