"""
Download IDEAM AUTOMATIC precipitation for the Magdalena-Cauca basin, study years
2011 (La Nina) and 2015-2016 (El Nino) — the scriptable, API-based "first pass".

Source: datos.gov.co Socrata dataset s54a-sgyg ("Precipitacion"), 10-minute raw data
from the automatic (telemetry) network. IDEAM flags it as raw/unvalidated, so we apply
basic QC here and treat it as a first-pass forcing; the validated CONVENTIONAL daily
record is pulled separately from DHIME (see Protocolo_descarga_PRECIPITACION.docx).

What it does
------------
1. dump_inventory()  -> data/raw/observed/precip/stations_precip_catalog.csv
   All precipitation stations in the basin from the IDEAM catalog (hp9r-jxuu):
   code, name, category, technology, status, dept, lat, lon, altitude, install date,
   sub-zone. This is the MASTER list the DHIME protocol also refers to.

2. download_automatic() -> data/raw/observed/precip/precip_auto_daily_long.csv
                           data/raw/observed/precip/precip_auto_stations.csv
   Daily precipitation totals per station, aggregated SERVER-SIDE (date_trunc + sum)
   so we move kilobytes, not gigabytes. Each station-day carries the number of 10-min
   intervals that reported (n, full day = 144); we mark a day VALID only if n >= 100
   (~70% completeness) to avoid under-counted daily totals.

Run on a machine with internet access to www.datos.gov.co (the sandbox proxy blocks it):
    python src/download_precip_automatic.py
Optional: set an app token to lift anonymous rate limits:
    setx SOCRATA_APP_TOKEN <your token>     (Windows, then reopen the shell)
Requires: pip install requests pandas
"""
import os, time, csv, requests, pandas as pd

CATALOG = "https://www.datos.gov.co/resource/hp9r-jxuu.json"     # station catalog
PRECIP  = "https://www.datos.gov.co/resource/s54a-sgyg.json"     # automatic 10-min precip
OUTDIR  = os.path.join("data", "raw", "observed", "precip")
os.makedirs(OUTDIR, exist_ok=True)

# codigo 21..29 == Magdalena-Cauca hydrographic area (lexicographic on the 10-digit code)
CODE_LO, CODE_HI = "0021", "0030"
# precipitation-measuring station categories (exclude Limni* = water level)
PRECIP_CATS = ["Pluviométrica", "Pluviográfica", "Climatológica Ordinaria",
               "Climatológica Principal", "Agrometeorológica",
               "Sinóptica Principal", "Sinóptica Secundaria"]
# study-year date windows — small windows keep each server-side aggregation fast (a whole
# month basin-wide overruns Socrata's 180 s limit)
import datetime as _dt
WINDOW_DAYS = 3
SPANS = [(_dt.date(2011, 1, 1), _dt.date(2011, 12, 31)),
         (_dt.date(2015, 1, 1), _dt.date(2016, 12, 31))]
MIN_INTERVALS = 100        # a day is valid only if >=100 of 144 ten-min slots reported

def _windows():
    for a, b in SPANS:
        d = a
        while d <= b:
            e = min(d + _dt.timedelta(days=WINDOW_DAYS - 1), b)
            yield d, e
            d = e + _dt.timedelta(days=1)

HEAD = {}
if os.environ.get("SOCRATA_APP_TOKEN"):
    HEAD["X-App-Token"] = os.environ["SOCRATA_APP_TOKEN"]


def _get(url, params, tries=4):
    for a in range(tries):
        try:
            r = requests.get(url, params=params, headers=HEAD, timeout=180)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if a == tries - 1:
                raise
            time.sleep(5)


def dump_inventory():
    out = os.path.join(OUTDIR, "stations_precip_catalog.csv")
    if os.path.exists(out):
        print(f"catalog: {out} already present — skipping"); return
    print("catalog: pulling basin precipitation stations ...")
    cats = ",".join("'%s'" % c for c in PRECIP_CATS)
    rows, off = [], 0
    while True:
        js = _get(CATALOG, {
            "$select": "codigo,nombre,categoria,tecnologia,estado,departamento,municipio,"
                       "latitud,longitud,altitud,fecha_instalacion,subzona_hidrografica,zona_hidrografica",
            "$where": f"area_hidrografica='Magdalena Cauca' and categoria in({cats})",
            "$order": "codigo", "$limit": 5000, "$offset": off})
        rows += js
        if len(js) < 5000:
            break
        off += 5000
    df = pd.DataFrame(rows)
    out = os.path.join(OUTDIR, "stations_precip_catalog.csv")
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"  wrote {out}  ({len(df)} stations)")
    print("  by category:", df["categoria"].value_counts().to_dict())
    return df


def download_automatic():
    print(f"automatic precip: daily totals in {WINDOW_DAYS}-day server-side windows (resumable) ...")
    long_out = os.path.join(OUTDIR, "precip_auto_daily_long.csv")
    done_path = os.path.join(OUTDIR, "_auto_done.txt")
    done = set(open(done_path).read().split()) if os.path.exists(done_path) else set()
    new_file = not os.path.exists(long_out)
    fout = open(long_out, "a", newline="", encoding="utf-8"); w = csv.writer(fout)
    if new_file:
        w.writerow(["code", "date", "p_mm", "n", "valid"])
    wins = list(_windows()); total = len(wins)
    for i, (d0, d1) in enumerate(wins):
        key = d0.isoformat()
        if key in done:
            continue
        e_excl = (d1 + _dt.timedelta(days=1)).isoformat()
        off, got = 0, 0
        while True:
            js = _get(PRECIP, {
                "$select": "codigoestacion,date_trunc_ymd(fechaobservacion) AS dia,"
                           "sum(valorobservado) AS p_mm,count(1) AS n",
                "$where": f"codigoestacion between '{CODE_LO}' and '{CODE_HI}' "
                          f"and fechaobservacion >= '{d0.isoformat()}' and fechaobservacion < '{e_excl}' "
                          f"and valorobservado >= 0 and valorobservado < 250",
                "$group": "codigoestacion,date_trunc_ymd(fechaobservacion)",
                "$order": "codigoestacion,dia", "$limit": 50000, "$offset": off})
            for rr in js:
                n = int(float(rr.get("n", 0))); dd = str(rr["dia"])[:10]
                w.writerow([rr["codigoestacion"], dd, rr.get("p_mm", ""), n, int(n >= MIN_INTERVALS)])
            got += len(js)
            if len(js) < 50000:
                break
            off += 50000
        fout.flush(); done.add(key); open(done_path, "a").write(key + "\n")
        if i % 10 == 0 or i == total - 1:
            print(f"  {key}  ({i+1}/{total})  +{got} station-days", flush=True)
        time.sleep(0.2)
    fout.close()
    _summarise(long_out)


def _summarise(long_out):
    df = pd.read_csv(long_out, dtype={"code": str})
    if df.empty:
        print("  no data"); return
    df["yr"] = pd.to_datetime(df["date"]).dt.year
    v = df[df["valid"] == 1]
    cov = v.groupby("code").agg(
        n_valid_2011=("yr", lambda s: int((s == 2011).sum())),
        n_valid_2015_16=("yr", lambda s: int(s.isin([2015, 2016]).sum()))).reset_index()
    cov["code"] = cov["code"].astype(str)
    cat = os.path.join(OUTDIR, "stations_precip_catalog.csv")
    if os.path.exists(cat):
        meta = pd.read_csv(cat, dtype=str).rename(columns={
            "codigo": "code", "nombre": "name", "latitud": "lat", "longitud": "lon",
            "departamento": "dept", "zona_hidrografica": "zona"})
        keep = [c for c in ["code", "name", "lat", "lon", "dept", "zona"] if c in meta.columns]
        st = cov.merge(meta[keep], on="code", how="left")
    else:
        st = cov
    st_out = os.path.join(OUTDIR, "precip_auto_stations.csv")
    st.to_csv(st_out, index=False, encoding="utf-8")
    print(f"  wrote {long_out}  ({len(df)} station-days, {df['code'].nunique()} stations)")
    print(f"  wrote {st_out}  ({len(st)} stations)")
    print(f"  stations >=300 valid days in 2011:    {int((cov['n_valid_2011']>=300).sum())}")
    print(f"  stations >=600 valid days in 2015-16: {int((cov['n_valid_2015_16']>=600).sum())}")


if __name__ == "__main__":
    dump_inventory()
    download_automatic()
    print("\nDone. Automatic first-pass precip is in data/raw/observed/precip/.")
    print("For the validated CONVENTIONAL daily record, follow Protocolo_descarga_PRECIPITACION.docx (DHIME).")
