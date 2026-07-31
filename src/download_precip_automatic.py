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
# study-year months
MONTHS = [(2011, m) for m in range(1, 13)] + \
         [(2015, m) for m in range(1, 13)] + [(2016, m) for m in range(1, 13)]
MIN_INTERVALS = 100        # a day is valid only if >=100 of 144 ten-min slots reported

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
    print("automatic precip: server-side daily aggregation, 2011 + 2015-16 ...")
    frames = []
    for (y, m) in MONTHS:
        d0 = f"{y}-{m:02d}-01"
        d1 = f"{y+(m//12)}-{(m%12)+1:02d}-01"          # first day of next month
        off, got = 0, 0
        while True:
            js = _get(PRECIP, {
                "$select": "codigoestacion,date_trunc_ymd(fechaobservacion) AS dia,"
                           "sum(valorobservado) AS p_mm,count(1) AS n",
                "$where": f"codigoestacion between '{CODE_LO}' and '{CODE_HI}' "
                          f"and fechaobservacion >= '{d0}' and fechaobservacion < '{d1}' "
                          f"and valorobservado >= 0 and valorobservado < 250",
                "$group": "codigoestacion,date_trunc_ymd(fechaobservacion)",
                "$order": "codigoestacion,dia", "$limit": 50000, "$offset": off})
            frames += js
            got += len(js)
            if len(js) < 50000:
                break
            off += 50000
        print(f"  {y}-{m:02d}: {got} station-days", flush=True)
        time.sleep(0.3)
    df = pd.DataFrame(frames)
    if df.empty:
        print("  no data returned"); return
    df["p_mm"] = pd.to_numeric(df["p_mm"], errors="coerce")
    df["n"] = pd.to_numeric(df["n"], errors="coerce")
    df["date"] = pd.to_datetime(df["dia"]).dt.date
    df["code"] = df["codigoestacion"]
    df["valid"] = df["n"] >= MIN_INTERVALS
    df = df[["code", "date", "p_mm", "n", "valid"]].sort_values(["code", "date"])
    long_out = os.path.join(OUTDIR, "precip_auto_daily_long.csv")
    df.to_csv(long_out, index=False)
    print(f"  wrote {long_out}  ({len(df)} station-days, {df['code'].nunique()} stations)")

    # station metadata + per-year valid-day coverage
    meta = _get(PRECIP, {
        "$select": "codigoestacion AS code,max(nombreestacion) AS name,max(latitud) AS lat,"
                   "max(longitud) AS lon,max(departamento) AS dept,max(zonahidrografica) AS zona",
        "$where": f"codigoestacion between '{CODE_LO}' and '{CODE_HI}' "
                  f"and fechaobservacion >= '2011-01-01' and fechaobservacion < '2017-01-01'",
        "$group": "codigoestacion", "$limit": 50000})
    mt = pd.DataFrame(meta)
    v = df[df["valid"]].copy(); v["yr"] = pd.to_datetime(v["date"]).dt.year
    cov = v.groupby("code").agg(
        n_valid_2011=("yr", lambda s: int((s == 2011).sum())),
        n_valid_2015_16=("yr", lambda s: int(s.isin([2015, 2016]).sum()))).reset_index()
    st = mt.merge(cov, on="code", how="left").fillna({"n_valid_2011": 0, "n_valid_2015_16": 0})
    st_out = os.path.join(OUTDIR, "precip_auto_stations.csv")
    st.to_csv(st_out, index=False, encoding="utf-8")
    print(f"  wrote {st_out}  ({len(st)} stations)")
    print(f"  stations with >=300 valid days in 2011:        {int((st['n_valid_2011']>=300).sum())}")
    print(f"  stations with >=600 valid days in 2015-16:     {int((st['n_valid_2015_16']>=600).sum())}")


if __name__ == "__main__":
    dump_inventory()
    download_automatic()
    print("\nDone. Automatic first-pass precip is in data/raw/observed/precip/.")
    print("For the validated CONVENTIONAL daily record, follow Protocolo_descarga_PRECIPITACION.docx (DHIME).")
