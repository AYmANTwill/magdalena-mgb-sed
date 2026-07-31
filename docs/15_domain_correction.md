# Domain correction — enlarge east (keep the 4.1 GB ERA5)

## Why
The rasters + ERA5 were on box **N 11.4 · W −77.0 · S 1.4 · E −72.9**. That east edge (−72.9) clips the
**upper Sogamoso / Chicamocha** (e.g. CAPITANEJO −72.69, PAZ DE RIO −72.74), which carries our **key 2011
sediment stations** (EL JORDAN, LA CEIBA, NEMIZAQUE… zona 24). Delineating on a DEM cut there would truncate the
Sogamoso drainage.

## Corrected box (locked)
Only the **east** is extended (−72.9 → −72.3); N/W/S unchanged so the ERA5 mosaic is a simple longitude concatenation.

**For DEM / SoilGrids (Xmin/Xmax/Ymin/Ymax):**
```
Xmin = -77.0   Xmax = -72.3   Ymin = 1.4   Ymax = 11.4
```
**For the ERA5 CDS API** the order is [N, W, S, E]: full box `[11.4, -77.0, 1.4, -72.3]`; the east strip only
`[11.4, -72.8, 1.4, -72.3]` (already set in `download_era5_strip.py`).

## What to (re)acquire

| Dataset | Action | Note |
|---------|--------|------|
| **ERA5-Land** | keep the 108 files; download the **east strip** then mosaic | `src/download_era5_strip.py` → `src/mosaic_era5.py` → `era5land_ext_*.nc` |
| **DEM** (Copernicus GLO-90) | **re-download** on the new bbox | OpenTopography: dataset `COP90`, S=1.4 N=11.4 W=−77.0 E=−72.3 |
| **SoilGrids** (clay/sand/silt/soc/bdod) | **re-fetch** the 5 rasters on the new bbox | small (~80 MB); same fetch, new bbox |
| **Land cover** (ESA WorldCover) | **nothing to do** | tiles W075 already cover lon −75..−72, so −72.3 is included |

## Steps
1. `python src/download_era5_strip.py`  (resumable, uses `cds_keys.txt`; small — only lon −72.8..−72.3).
2. `python src/mosaic_era5.py`  → produces `data/raw/climate/era5land_ext_<y>_M<mm>.nc` (domain −77.0..−72.3).
3. Re-download **DEM** (COP90) and **SoilGrids** on the new bbox; drop them in `data/raw/dem/` and `data/raw/soils/`.
4. Use `era5land_ext_*.nc` as the climate forcing from now on.

Once the eastern extension is in place, the domain is consistent and **preprocessing (minibacias → URH → parameters)**
can start.
