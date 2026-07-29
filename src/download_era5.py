"""
ERA5-Land download for MGB-SA — WHOLE Magdalena-Cauca basin (90 m study).

Parallel over multiple CDS keys, one month per request, fully STOP/RESUME safe:
- Each month downloads to a temporary <file>.part, then is renamed to the final name ONLY when complete.
  => pressing Ctrl+C at any time never leaves a half-written file that resume would skip.
- On restart, completed files are skipped and any leftover .part files are cleaned and re-downloaded.
- Transient CDS/MARS errors are retried (3x); anything still failing is skipped and retried next run.

Keys:    one CDS personal-access token per line in  cds_keys.txt  (gitignored).
Prereqs: pip install "cdsapi>=0.7"
Run:     python src/download_era5.py        (from the repo root)  -- run again anytime to resume.
Output:  data/raw/climate/era5land_basin_<year>_M<mm>.nc   (108 files: 2009-2017 x 12)
"""
import os
import time
import cdsapi
from concurrent.futures import ThreadPoolExecutor

URL = "https://cds.climate.copernicus.eu/api"

with open("cds_keys.txt") as fh:
    KEYS = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]

YEARS = [str(y) for y in range(2009, 2018)]                 # 2009-2017
CHUNKS = {f"M{m:02d}": [f"{m:02d}"] for m in range(1, 13)}  # one month per request
AREA = [11.4, -77.0, 1.4, -72.9]                            # N, W, S, E — whole Magdalena-Cauca basin
VARIABLES = ["total_precipitation", "2m_temperature", "2m_dewpoint_temperature",
             "surface_solar_radiation_downwards", "10m_u_component_of_wind",
             "10m_v_component_of_wind", "surface_pressure"]
PREFIX = "era5land_basin_"

OUTDIR = os.path.join("data", "raw", "climate")
os.makedirs(OUTDIR, exist_ok=True)

# --- clean up leftover .part files from a previous interruption ---
for fn in os.listdir(OUTDIR):
    if fn.startswith(PREFIX) and fn.endswith(".part"):
        os.remove(os.path.join(OUTDIR, fn))

# --- build the task list; skip months already fully downloaded (this is the resume) ---
tasks = []
for y in YEARS:
    for q, months in CHUNKS.items():
        out = os.path.join(OUTDIR, f"{PREFIX}{y}_{q}.nc")
        if not os.path.exists(out):
            tasks.append((y, months, out))
total = len(YEARS) * len(CHUNKS)
print(f"{len(KEYS)} API key(s) | {total-len(tasks)}/{total} already done | {len(tasks)} to download")


def worker(key, my_tasks):
    client = cdsapi.Client(url=URL, key=key, quiet=True)
    tag = key[:8]
    for (y, months, out) in my_tasks:
        if os.path.exists(out):            # became available since the list was built
            continue
        name = os.path.basename(out)
        tmp = out + ".part"
        for attempt in range(1, 4):        # retry transient MARS/network errors
            try:
                print(f"[{tag}..] requesting {name} (try {attempt})", flush=True)
                client.retrieve("reanalysis-era5-land", {
                    "variable": VARIABLES, "year": y, "month": months,
                    "day":  [f"{d:02d}" for d in range(1, 32)],
                    "time": [f"{h:02d}:00" for h in range(24)],
                    "area": AREA, "data_format": "netcdf", "download_format": "unarchived",
                }, tmp)
                os.replace(tmp, out)        # atomic: final file appears only when complete
                print(f"[{tag}..] done {name}", flush=True)
                break
            except (Exception, KeyboardInterrupt) as e:
                if os.path.exists(tmp):
                    os.remove(tmp)          # never leave a partial behind
                if isinstance(e, KeyboardInterrupt):
                    print(f"[{tag}..] stopped — {name} will resume next run", flush=True)
                    return
                print(f"[{tag}..] error on {name} (try {attempt}): {str(e)[:100]}", flush=True)
                if attempt < 3:
                    time.sleep(30)
        else:
            print(f"[{tag}..] gave up on {name} — will retry on next run", flush=True)


# distribute months round-robin across keys, one thread per key
buckets = [[] for _ in KEYS]
for i, t in enumerate(tasks):
    buckets[i % len(KEYS)].append(t)

try:
    with ThreadPoolExecutor(max_workers=max(1, len(KEYS))) as ex:
        futures = [ex.submit(worker, k, b) for k, b in zip(KEYS, buckets)]
        for f in futures:
            f.result()
    print("All 108 months present — ERA5 download complete.")
except KeyboardInterrupt:
    print("\nStopped. Run the script again to resume from where it left off.")
