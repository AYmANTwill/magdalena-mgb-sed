"""
QC + merge the DHIME conventional daily precipitation downloads into a clean gauge dataset.

Reads every zip in data/raw/observed/precip/dhime/ (each an IDEAM "descargaDhime.csv":
CodigoEstacion, NombreEstacion, Variable, Parametro, Fecha, Unidad, Valor, NivelAprobacion),
and produces two clean products the bias-correction (notebook 10) consumes:

  data/processed/precip_gauges_daily.csv      long: code, date, precip_mm, approval
  data/processed/precip_gauges_inventory.csv  one row/station: coords + coverage + flags

QC steps (all explicit and logged):
  1. concatenate all zips/parts.
  2. de-duplicate (code, date) — the multi-part downloads overlap; keep the highest
     approval level (Definitivo > Preliminar > En revisión).
  3. value screen: keep 0 <= Valor <= 400 mm/day (basin max seen = 294; >400 is a sensor
     error, none present). Negatives -> missing.
  4. drop broken/unusable stations: all-constant series (nunique <= 1, e.g. stuck at 0) or
     < 90 valid days over 2008-2018 (too sparse to correct anything).
  5. attach lon/lat/elevation/zone from the IDEAM catalogue (stations_precip_catalog.csv).

Run:  python src/build_precip_gauges.py
Requires: pandas, geopandas not needed.
"""
import glob, os, re, zipfile, io, pathlib
import numpy as np, pandas as pd

from dhime_dates import parse_dhime_dates

REPO = pathlib.Path(__file__).resolve().parents[1]
DHIME = REPO / "data" / "raw" / "observed" / "precip" / "dhime"
CATALOG = REPO / "data" / "raw" / "observed" / "precip" / "stations_precip_catalog.csv"
OUTD = REPO / "data" / "processed"
OUTD.mkdir(parents=True, exist_ok=True)
APPROVAL = {"Definitivo": 0, "Preliminar": 1, "En revisión": 2, "En revision": 2}
VMAX = 400.0
MIN_DAYS = 90


def _read_one(src, label, frames, evidence):
    """Read one DHIME csv and date it FROM ITS OWN EVIDENCE, before concatenation.

    Per-file is not a stylistic choice. `Fecha` layout is a property of the export,
    not of the corpus: DHIME ships ISO in most parts and d/m/Y in others (docs/17,
    src/dhime_dates.py). Detecting on the concatenated frame would either raise
    `UnrecognisedDateFormat('mixed layouts')` on a corpus that is individually
    well-formed, or - worse, with pandas inference - let one file's layout decide
    another's. `parse_dhime_dates` raises rather than coercing, so an undecidable
    file stops the build here instead of silently transposing day and month.
    """
    df = pd.read_csv(src, dtype={"CodigoEstacion": str})
    dates, ev = parse_dhime_dates(df["Fecha"])
    df["date"] = dates.dt.normalize()
    frames.append(df)
    evidence.append((label, ev))
    return df


def load_all():
    frames, evidence = [], []
    regions = DHIME / "regions"
    if regions.exists():
        # preferred: the organized region folders (your zips + Youssef, via organize_precip_regions.py)
        for c in glob.glob(str(regions / "**" / "*.csv"), recursive=True):
            _read_one(c, os.path.relpath(c, regions), frames, evidence)
        print(f"reading organized regions/  ({len(frames)} csv files)")
    else:
        # fallback: raw zips + any Youssef csvs
        for z in sorted(glob.glob(str(DHIME / "*.zip"))):
            with zipfile.ZipFile(z) as zf:
                for nm in zf.namelist():
                    if nm.lower().endswith(".csv"):
                        _read_one(io.BytesIO(zf.read(nm)), f"{os.path.basename(z)}:{nm}",
                                  frames, evidence)
        for c in glob.glob(str(DHIME / "**" / "*.csv"), recursive=True):
            if "__MACOSX" not in c:
                _read_one(c, os.path.relpath(c, DHIME), frames, evidence)
    a = pd.concat(frames, ignore_index=True)
    print(f"loaded {len(frames)} files, {len(a):,} raw rows")

    fams = pd.Series([ev.family for _, ev in evidence]).value_counts().to_dict()
    print(f"date formats detected per file: {fams}")
    nondmy = [(lb, ev) for lb, ev in evidence if ev.family != "iso"]
    for lb, ev in nondmy:
        print(f"  NON-ISO  {lb}: fmt={ev.fmt!r} family={ev.family} "
              f"n={ev.n_rows:,} first>12={ev.n_first_gt12:,} second>12={ev.n_second_gt12:,}")
    if not nondmy:
        print("  every file proved ISO year-first; no day/month ambiguity existed to resolve")
    return a


def main():
    a = load_all()
    a["precip_mm"] = pd.to_numeric(a["Valor"], errors="coerce")
    a["code"] = a["CodigoEstacion"].str.lstrip("0")
    a["apr"] = a["NivelAprobacion"].map(APPROVAL).fillna(3).astype(int)

    # 2. de-duplicate (code, date), keep best approval
    n0 = len(a)
    a = a.sort_values("apr").drop_duplicates(["code", "date"], keep="first")
    print(f"de-dup (code,date): {n0:,} -> {len(a):,}  ({n0-len(a):,} duplicate station-days removed)")

    # 3. value screen
    bad = (a["precip_mm"] < 0) | (a["precip_mm"] > VMAX)
    a.loc[bad, "precip_mm"] = np.nan
    print(f"value screen: {int(bad.sum())} readings set to missing (outside 0..{VMAX:.0f} mm)")

    # 4a. keep only Magdalena-Cauca stations (zone code 21-29); departments spill into the
    #     Pacific (52-54) and Caribbean (11) basins — those are out of our domain.
    a["zone2"] = a["code"].str[:2]
    BASIN = {"21", "22", "23", "24", "25", "26", "27", "28", "29"}
    n_out = a.loc[~a["zone2"].isin(BASIN), "code"].nunique()
    a = a[a["zone2"].isin(BASIN)].copy()
    print(f"in-basin filter: dropped {n_out} out-of-basin stations (Pacific/Caribbean spillover)")

    # 4b. drop broken / ultra-sparse stations
    valid = a.dropna(subset=["precip_mm"])
    g = valid.groupby("code")["precip_mm"]
    ndays = g.size(); nuniq = g.nunique()
    drop_flat = set(nuniq[nuniq <= 1].index)
    drop_sparse = set(ndays[ndays < MIN_DAYS].index)
    drop = drop_flat | drop_sparse
    print(f"drop {len(drop_flat)} flatline + {len(drop_sparse)} ultra-sparse (<{MIN_DAYS}d) -> {len(drop)} stations removed")
    a = a[~a["code"].isin(drop)].copy()

    # daily product
    daily = a[["code", "date", "precip_mm", "NivelAprobacion"]].rename(columns={"NivelAprobacion": "approval"})
    daily = daily.sort_values(["code", "date"])
    daily.to_csv(OUTD / "precip_gauges_daily.csv", index=False)

    # 5. inventory + coverage, join catalogue coords
    cat = pd.read_csv(CATALOG, dtype=str)
    cat["code"] = cat["codigo"].str.lstrip("0")
    cat = cat.rename(columns={"nombre": "name", "latitud": "lat", "longitud": "lon",
                              "altitud": "alt", "departamento": "dept",
                              "zona_hidrografica": "zona", "categoria": "categoria"})
    v = daily.dropna(subset=["precip_mm"]).copy(); v["yr"] = v.date.dt.year
    inv = v.groupby("code").agg(
        n_valid=("precip_mm", "size"),
        first=("date", "min"), last=("date", "max"),
        ann_mean_mm=("precip_mm", lambda s: round(s.sum() / max(1, v.loc[s.index, "yr"].nunique()), 0)),
        cov_2011=("yr", lambda s: int((s == 2011).sum())),
        cov_2015=("yr", lambda s: int((s == 2015).sum())),
        cov_2016=("yr", lambda s: int((s == 2016).sum())),
    ).reset_index()
    keep = [c for c in ["code", "name", "lat", "lon", "alt", "dept", "zona", "categoria"] if c in cat.columns]
    inv = inv.merge(cat[keep].drop_duplicates("code"), on="code", how="left")
    for c in ("lat", "lon", "alt"):
        if c in inv: inv[c] = pd.to_numeric(inv[c], errors="coerce")
    # backfill coords for in-basin stations absent from the category-filtered catalogue
    # (e.g. "Meteorológica Especial" gauges) from the supplement fetched from the IDEAM catalogue
    sup_path = REPO / "data" / "raw" / "observed" / "precip" / "precip_coords_supplement.csv"
    if sup_path.exists():
        sup = pd.read_csv(sup_path, dtype={"code": str})
        inv = inv.merge(sup, on="code", how="left", suffixes=("", "_sup"))
        inv["lat"] = inv["lat"].fillna(inv["lat_sup"]); inv["lon"] = inv["lon"].fillna(inv["lon_sup"])
        inv = inv.drop(columns=[c for c in ("lat_sup", "lon_sup") if c in inv])
    inv = inv.sort_values(["zona", "dept", "code"])
    inv.to_csv(OUTD / "precip_gauges_inventory.csv", index=False)

    print(f"\nCLEAN: {inv.code.nunique()} stations | {len(daily):,} station-days")
    print(f"  with coords: {inv.lat.notna().sum()} | missing coords: {inv.lat.isna().sum()}")
    print("  by zona:", inv.zona.value_counts().to_dict())
    print(f"  usable in study years (>=200 valid d): 2011 {int((inv.cov_2011>=200).sum())} | "
          f"2015 {int((inv.cov_2015>=200).sum())} | 2016 {int((inv.cov_2016>=200).sum())}")
    print("wrote", OUTD / "precip_gauges_daily.csv")
    print("wrote", OUTD / "precip_gauges_inventory.csv")


if __name__ == "__main__":
    main()
