"""
Mosaic each basin ERA5 file (-77.0..-72.9) with its east strip (-72.8..-72.3)
along longitude -> full corrected domain -77.0..-72.3.

Reads : data/raw/climate/era5land_basin_<y>_M<mm>.nc   (existing, kept)
        data/raw/climate/strip/era5land_strip_<y>_M<mm>.nc
Writes: data/raw/climate/era5land_ext_<y>_M<mm>.nc      (the domain to use for MGB)

Run after download_era5_strip.py finishes:  python src/mosaic_era5.py
Requires: xarray, netcdf4  (pip install xarray netcdf4)
"""
import os, glob
import xarray as xr

CLIM = os.path.join("data", "raw", "climate")
STRIP = os.path.join(CLIM, "strip")
LONNAME = "longitude"

done = missing = 0
for basin in sorted(glob.glob(os.path.join(CLIM, "era5land_basin_*.nc"))):
    tag = os.path.basename(basin).replace("era5land_basin_", "").replace(".nc", "")   # e.g. 2011_M03
    strip = os.path.join(STRIP, f"era5land_strip_{tag}.nc")
    out = os.path.join(CLIM, f"era5land_ext_{tag}.nc")
    if os.path.exists(out):
        done += 1; continue
    if not os.path.exists(strip):
        print("MISSING strip for", tag, "-> run download_era5_strip.py"); missing += 1; continue
    db = xr.open_dataset(basin); ds = xr.open_dataset(strip)
    lon = LONNAME if LONNAME in db.dims else "lon"
    merged = xr.concat([db, ds], dim=lon).sortby(lon)
    # drop any duplicate longitudes at the seam, keep first
    _, idx = __import__("numpy").unique(merged[lon].values, return_index=True)
    merged = merged.isel({lon: sorted(idx)})
    merged.to_netcdf(out)
    db.close(); ds.close(); merged.close()
    done += 1
    print("wrote", os.path.basename(out))

print(f"\n{done} extended files ready in data/raw/climate/ (era5land_ext_*.nc); {missing} missing strips.")
print("Use era5land_ext_*.nc as the climate forcing (domain -77.0..-72.3).")
