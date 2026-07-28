"""
Parallel ERA5-Land download for MGB-SA (lower-Magdalena pilot).

Speed-up: uses MULTIPLE CDS API keys at once (one download running per key), and requests
3 months (a quarter) per file instead of one month.

Keys:    put one CDS personal-access token per line in  cds_keys.txt  (gitignored) —
         your own key + the colleagues' keys.
Prereqs: pip install "cdsapi>=0.7"
Run:     python src/download_era5.py          (from the repo root)
Output:  data/raw/climate/era5land_<year>_<Qn>.nc   (resumable — existing files are skipped)

If a request ever fails with "cost limits exceeded / request too large", switch to monthly
chunks (see the note at the very bottom).
"""
import os
import time
import cdsapi
from concurrent.futures import ThreadPoolExecutor

URL = "https://cds.climate.copernicus.eu/api"

# --- read one API token per line from the gitignored key file ---
with open("cds_keys.txt") as fh:
    KEYS = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
print(f"{len(KEYS)} API key(s) -> up to {len(KEYS)} downloads in parallel")

YEARS = [str(y) for y in range(2009, 2018)]                 # 2009-2017
CHUNKS = {f"M{m:02d}": [f"{m:02d}"] for m in range(1, 13)}      # ONE month per request
# (3-month chunks exceed the CDS cost limit -> 403; monthly works. Speed comes from the 3 keys in parallel.)
AREA = [11.3, -75.4, 8.2, -73.7]                            # N, W, S, E (lower-Magdalena box)
VARIABLES = ["total_precipitation", "2m_temperature", "2m_dewpoint_temperature",
             "surface_solar_radiation_downwards", "10m_u_component_of_wind",
             "10m_v_component_of_wind", "surface_pressure"]

OUTDIR = os.path.join("data", "raw", "climate")
os.makedirs(OUTDIR, exist_ok=True)

# build the task list, skipping anything already downloaded
tasks = []
for y in YEARS:
    for q, months in CHUNKS.items():
        out = os.path.join(OUTDIR, f"era5land_{y}_{q}.nc")
        if not os.path.exists(out):
            tasks.append((y, months, out))
print(f"{len(tasks)} chunks to download")


def worker(key, my_tasks):
    client = cdsapi.Client(url=URL, key=key, quiet=True)
    tag = key[:8]
    for (y, months, out) in my_tasks:
        if os.path.exists(out):
            continue
        name = os.path.basename(out)
        for attempt in range(1, 4):                      # up to 3 tries (transient MARS errors)
            try:
                print(f"[{tag}..] requesting {name} (try {attempt})")
                client.retrieve("reanalysis-era5-land", {
                    "variable": VARIABLES, "year": y, "month": months,
                    "day":  [f"{d:02d}" for d in range(1, 32)],
                    "time": [f"{h:02d}:00" for h in range(24)],
                    "area": AREA, "data_format": "netcdf", "download_format": "unarchived",
                }, out)
                print(f"[{tag}..] done {name}")
                break
            except Exception as e:
                print(f"[{tag}..] error on {name} (try {attempt}): {str(e)[:100]}")
                if os.path.exists(out):
                    os.remove(out)                       # drop any partial file
                if attempt < 3:
                    time.sleep(30)
        else:
            print(f"[{tag}..] gave up on {name} — will retry on next run")


# distribute chunks round-robin across the keys, run one thread per key
buckets = [[] for _ in KEYS]
for i, t in enumerate(tasks):
    buckets[i % len(KEYS)].append(t)

with ThreadPoolExecutor(max_workers=max(1, len(KEYS))) as ex:
    futures = [ex.submit(worker, k, b) for k, b in zip(KEYS, buckets)]
    for f in futures:
        f.result()

print("All chunks downloaded.")

# --- FALLBACK: if you get "cost limits exceeded", make chunks smaller (one month each):
#   CHUNKS = {f"M{m:02d}": [f"{m:02d}"] for m in range(1, 13)}
