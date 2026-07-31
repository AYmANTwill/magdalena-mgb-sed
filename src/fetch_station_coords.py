"""
Fetch the (lon, lat) of every discharge station we collected, from the official
IDEAM station catalogue (datos.gov.co Socrata dataset hp9r-jxuu), and save them to
data/processed/stations_discharge_coords.csv  (columns: code, lon, lat).

Used by notebook 07 (Step 6) to check that each gauge falls on a distinct minibacia.
Requires: pip install requests
Run:      python src/fetch_station_coords.py
"""
import csv, glob, os, requests

# 1. collect the station codes from the caudal CSVs
codes = set()
for fp in glob.glob("data/raw/observed/caudal/*.csv"):
    for r in csv.DictReader(open(fp, encoding="utf-8", errors="replace")):
        codes.add(r["CodigoEstacion"])
codes = sorted(codes)
print(f"{len(codes)} discharge stations to locate")

# 2. query the catalogue in small batches (codes are padded to 10 digits: '00'+code)
BASE = "https://www.datos.gov.co/resource/hp9r-jxuu.json"
rows = []
for i in range(0, len(codes), 6):
    batch = codes[i:i+6]
    inlist = ",".join("'00%s'" % c for c in batch)
    params = {"$select": "codigo,latitud,longitud", "$where": f"codigo in({inlist})", "$limit": 50}
    r = requests.get(BASE, params=params, timeout=60); r.raise_for_status()
    for row in r.json():
        code = row["codigo"][2:] if row["codigo"].startswith("00") else row["codigo"]
        rows.append((code, row.get("longitud"), row.get("latitud")))
    print(f"  {min(i+6,len(codes))}/{len(codes)}", end="\r")

# 3. save
os.makedirs("data/processed", exist_ok=True)
out = "data/processed/stations_discharge_coords.csv"
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["code", "lon", "lat"]); w.writerows(rows)
print(f"\nwrote {len(rows)} coordinates -> {out}")
