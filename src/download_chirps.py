"""
CHIRPS-2.0 daily rainfall download, clipped to the Magdalena-Cauca basin.

CHIRPS is the satellite + gauge blended product proposed as the spatial backbone for the
MGB-SA rainfall forcing (notebook 11). This script fetches the yearly global p05 (0.05 deg)
netCDF, subsets it to the basin box, and writes a compact per-year file. The ~1.1 GB global
download is deleted once the subset is written, so only a few MB/year is kept.

Three large files are fetched rather than ~1100 daily GeoTIFFs: fewer requests, each
independently restartable, and the same underlying data.

Outputs:
    data/raw/climate/chirps_basin_<year>.nc   dims (time, latitude, longitude), precip mm/day

Run:
    python src/download_chirps.py                # default study years 2011, 2015, 2016
    python src/download_chirps.py 2011 2012      # explicit years
"""
from __future__ import annotations

import shutil
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "data" / "raw" / "climate"
TMP_DIR = OUT_DIR / "_chirps_tmp"

URL = ("https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/"
       "chirps-v2.0.{year}.days_p05.nc")

# Basin box from data/processed/minibacias.tif, padded by one 0.05 deg cell.
LON_MIN, LON_MAX = -77.05, -72.25
LAT_MIN, LAT_MAX = 1.35, 11.45

STUDY_YEARS = (2011, 2015, 2016)
CHUNK = 1 << 22  # 4 MB reads — large buffers keep Defender scanning off the hot path
PROGRESS_EVERY = 1 << 28  # log roughly every 256 MB


def download(year: int, dest: Path) -> None:
    """Stream the global yearly netCDF to `dest` via a .part temporary file."""
    url = URL.format(year=year)
    tmp = dest.with_suffix(".part")
    with urllib.request.urlopen(url, timeout=120) as resp:
        total = int(resp.headers.get("Content-Length", 0))
        done = 0
        next_log = PROGRESS_EVERY
        with tmp.open("wb") as fh:
            while True:
                block = resp.read(CHUNK)
                if not block:
                    break
                fh.write(block)
                done += len(block)
                if done >= next_log:
                    print(f"    {year}: {done / 1e9:.2f}/{total / 1e9:.2f} GB", flush=True)
                    next_log += PROGRESS_EVERY
    tmp.replace(dest)


def subset(src: Path, dest: Path) -> None:
    """Clip the global file to the basin box and write a compact netCDF."""
    import xarray as xr

    with xr.open_dataset(src) as ds:
        lat_ascending = bool(ds.latitude[0] < ds.latitude[-1])
        lat_slice = slice(LAT_MIN, LAT_MAX) if lat_ascending else slice(LAT_MAX, LAT_MIN)
        clipped = ds.sel(latitude=lat_slice, longitude=slice(LON_MIN, LON_MAX))
        encoding = {"precip": {"zlib": True, "complevel": 4, "dtype": "float32"}}
        clipped.to_netcdf(dest, encoding=encoding)
        print(f"    subset -> {dest.name}  {dict(clipped.sizes)}  "
              f"{dest.stat().st_size / 1e6:.1f} MB", flush=True)


def main() -> None:
    years = [int(a) for a in sys.argv[1:]] or list(STUDY_YEARS)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(exist_ok=True)

    for year in years:
        dest = OUT_DIR / f"chirps_basin_{year}.nc"
        if dest.exists():
            print(f"  {year}: already have {dest.name} — skipping", flush=True)
            continue
        raw = TMP_DIR / f"chirps-v2.0.{year}.days_p05.nc"
        if not raw.exists():
            print(f"  {year}: downloading global p05 …", flush=True)
            download(year, raw)
        print(f"  {year}: subsetting to basin …", flush=True)
        subset(raw, dest)
        raw.unlink()

    if TMP_DIR.exists() and not any(TMP_DIR.iterdir()):
        shutil.rmtree(TMP_DIR)
    print("done:", ", ".join(str(y) for y in years))


if __name__ == "__main__":
    main()
