"""
ERA5-Land EAST STRIP download — extends the basin domain eastward to include the
upper Sogamoso / Chicamocha (clipped by the old -72.9 edge).

The existing 108 files cover lon -77.0..-72.9.  This downloads ONLY the missing
eastern strip  lon -72.8..-72.3  (same latitudes), 108 months, then `mosaic_era5.py`
concatenates each month with its basin file -> full domain -77.0..-72.3.

Same stop/resume design as download_era5.py (atomic .part, multi-key parallel).
Run:  python src/download_era5_strip.py     (resumable)  then  python src/mosaic_era5.py
"""
import os, time, cdsapi
from concurrent.futures import ThreadPoolExecutor

URL = "https://cds.climate.copernicus.eu/api"
with open("cds_keys.txt") as fh:
    KEYS = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]

YEARS  = [str(y) for y in range(2008, 2019)]                 # 2008-2018 (2008 = spin-up, 2018 = validation; obs end 2018-12-31)
CHUNKS = {f"M{m:02d}": [f"{m:02d}"] for m in range(1, 13)}   # one month per request
AREA   = [11.4, -72.8, 1.4, -72.3]                           # N, W, S, E  — EAST STRIP only
VARIABLES = ["total_precipitation", "2m_temperature", "2m_dewpoint_temperature",
             "surface_solar_radiation_downwards", "10m_u_component_of_wind",
             "10m_v_component_of_wind", "surface_pressure"]
PREFIX = "era5land_strip_"
OUTDIR = os.path.join("data", "raw", "climate", "strip")
os.makedirs(OUTDIR, exist_ok=True)

for fn in os.listdir(OUTDIR):
    if fn.startswith(PREFIX) and fn.endswith(".part"):
        os.remove(os.path.join(OUTDIR, fn))

tasks = []
for y in YEARS:
    for q, months in CHUNKS.items():
        out = os.path.join(OUTDIR, f"{PREFIX}{y}_{q}.nc")
        if not os.path.exists(out):
            tasks.append((y, months, out))
total = len(YEARS) * len(CHUNKS)
print(f"{len(KEYS)} key(s) | {total-len(tasks)}/{total} strip files done | {len(tasks)} to download")


def worker(key, my_tasks):
    client = cdsapi.Client(url=URL, key=key, quiet=True)
    tag = key[:8]
    for (y, months, out) in my_tasks:
        if os.path.exists(out):
            continue
        name = os.path.basename(out); tmp = out + ".part"
        for attempt in range(1, 4):
            try:
                print(f"[{tag}..] {name} (try {attempt})", flush=True)
                client.retrieve("reanalysis-era5-land", {
                    "variable": VARIABLES, "year": y, "month": months,
                    "day":  [f"{d:02d}" for d in range(1, 32)],
                    "time": [f"{h:02d}:00" for h in range(24)],
                    "area": AREA, "data_format": "netcdf", "download_format": "unarchived",
                }, tmp)
                os.replace(tmp, out); print(f"[{tag}..] done {name}", flush=True); break
            except (Exception, KeyboardInterrupt) as e:
                if os.path.exists(tmp): os.remove(tmp)
                if isinstance(e, KeyboardInterrupt):
                    print(f"[{tag}..] stopped — {name} resumes next run", flush=True); return
                print(f"[{tag}..] error {name} (try {attempt}): {str(e)[:90]}", flush=True)
                if attempt < 3: time.sleep(30)


buckets = [[] for _ in KEYS]
for i, t in enumerate(tasks):
    buckets[i % len(KEYS)].append(t)
try:
    with ThreadPoolExecutor(max_workers=max(1, len(KEYS))) as ex:
        for f in [ex.submit(worker, k, b) for k, b in zip(KEYS, buckets)]:
            f.result()
    print("East strip complete — now run:  python src/mosaic_era5.py")
except KeyboardInterrupt:
    print("\nStopped. Rerun to resume.")
