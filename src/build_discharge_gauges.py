"""
Consolidate ALL raw DHIME discharge downloads into one clean daily table.

Reads every CSV in data/raw/observed/caudal/, every CSV inside every zip there,
and every CSV inside every zip in OMAR_CAUDAL/ (all IDEAM "descargaDhime" exports:
CodigoEstacion, NombreEstacion, Variable, Parametro, Fecha, Unidad, Valor,
NivelAprobacion), and produces two clean products:

  data/processed/discharge_daily.csv      long: code, date, q_m3s, approval
  data/processed/discharge_inventory.csv  one row/station: name, dept, lat, lon,
                                          minibacia, coverage + value stats

Steps (all explicit and logged):
  1. ingest every source file; encodings vary (utf-8 or latin-1 — try utf-8 first);
     filenames contain accents/spaces; zips may nest further zips.
  2. keep only Parametro == 'Caudal medio diario'; every other Parametro value seen
     is counted and reported, never silently dropped.
     NOTE: 'Caudal medio diario' is assumed to be a midnight->midnight calendar-day
     mean (unlike precip's 07:00->07:00 dia pluviometrico); all Fecha timestamps in
     the raw exports are 00:00, consistent with that assumption.
  3. de-duplicate station-days across sources (the same dept was downloaded both as
     .csv and .zip, and valle appears 3x): keep the highest approval level
     (Definitivo > En revisión > Preliminar > anything else), then deterministic
     tie-break (lowest value, then source filename).
  4. drop negative q_m3s (counted); zeros and extremes are KEPT — downstream QC
     decides what to do with them.
  5. left-join lon/lat from stations_discharge_coords.csv and minibacia from
     gauge_minibacia.csv; unmatched stations are counted, not dropped.

Coverage columns: cov_2011 = n valid days in 2011; cov_2015_16 = n valid days in
2015-2016 (prior inventory stations_discharge.csv stored booleans; counts are
strictly more informative and threshold-free).

Run:  python src/build_discharge_gauges.py
Requires: pandas, numpy.
"""
import io
import pathlib
import unicodedata
import zipfile

import numpy as np
import pandas as pd

from dhime_dates import parse_dhime_dates

REPO = pathlib.Path(__file__).resolve().parents[1]
CAUDAL = REPO / "data" / "raw" / "observed" / "caudal"
COORDS = REPO / "data" / "processed" / "stations_discharge_coords.csv"
MINIB = REPO / "data" / "processed" / "gauge_minibacia.csv"
OUTD = REPO / "data" / "processed"

PARAM_KEEP = "Caudal medio diario"
# task-specified ranking: Definitivo > En revisión/En revision > Preliminar > other
APPROVAL_RANK = {"Definitivo": 0, "En revisión": 1, "En revision": 1, "Preliminar": 2}
# dept aliases: normalize filename typos/variants to one canonical dept name
DEPT_ALIAS = {
    "rizaralda": "risaralda",
    "boliviar": "bolivar",
    "valle": "valle_de_cauca",
    "valledecauca": "valle_de_cauca",
    "valle_de_cauca": "valle_de_cauca",
    "nsantander": "norte_de_santander",
}


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def dept_from_filename(path_like: str) -> str:
    """caudal_Boyacá  -1.zip -> boyaca; Santander_caudal_2.zip -> santander.

    Zip members are tagged 'outer.zip::member.csv' — dept comes from the outer name.
    """
    stem = pathlib.Path(path_like.split("::", 1)[0]).stem
    s = strip_accents(stem).lower()
    s = s.replace("caudal", "")
    s = "".join(ch if (ch.isalpha() or ch == "_") else "_" for ch in s)
    parts = [p for p in s.split("_") if p]
    key = "_".join(parts)
    return DEPT_ALIAS.get(key, key)


DATE_EVIDENCE: list = []   # (source, DateEvidence) per part, printed by load_all


def read_dhime_csv(raw: bytes, source: str) -> pd.DataFrame:
    """Parse one descargaDhime CSV; utf-8 first, latin-1 fallback.

    The date is established here, PER PART, from that part's own field values.
    `Fecha` layout is a property of the export (ISO in most DHIME parts, d/m/Y in
    others - see src/dhime_dates.py), so it cannot be decided on the concatenated
    frame without letting one part's layout speak for another's. `parse_dhime_dates`
    raises on an undecidable part rather than coercing, which is the whole point:
    a transposed day/month leaves the record's min/max span identical and is
    invisible to every downstream range check.
    """
    for enc in ("utf-8", "latin-1"):
        try:
            d = pd.read_csv(io.BytesIO(raw), dtype=str, encoding=enc)
            break
        except UnicodeDecodeError:
            continue
    else:  # pragma: no cover - latin-1 never raises UnicodeDecodeError
        raise ValueError(f"undecodable file: {source}")
    d["source"] = source
    if "Fecha" in d.columns and len(d):
        dates, ev = parse_dhime_dates(d["Fecha"])
        d["date"] = dates.dt.normalize()
        DATE_EVIDENCE.append((source, ev))
    return d


def iter_zip_csvs(raw: bytes, source: str, frames: list, failures: list) -> None:
    """Collect every CSV member of a zip (recursing into nested zips)."""
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            for nm in zf.namelist():
                if "__MACOSX" in nm:
                    continue
                low = nm.lower()
                member_src = f"{source}::{nm}"
                if low.endswith(".csv"):
                    frames.append(read_dhime_csv(zf.read(nm), member_src))
                elif low.endswith(".zip"):
                    iter_zip_csvs(zf.read(nm), member_src, frames, failures)
    except (zipfile.BadZipFile, ValueError, KeyError) as e:
        failures.append((source, repr(e)))


def load_all() -> tuple:
    frames, failures = [], []
    csvs = sorted(CAUDAL.rglob("*.csv"))
    zips = sorted(CAUDAL.rglob("*.zip"))
    for p in csvs:
        frames.append(read_dhime_csv(p.read_bytes(), p.name))
    for p in zips:
        iter_zip_csvs(p.read_bytes(), p.name, frames, failures)
    expected = {"CodigoEstacion", "Parametro", "Fecha", "Valor", "NivelAprobacion"}
    bad_schema = [f["source"].iloc[0] for f in frames if not expected.issubset(f.columns)]
    frames = [f for f in frames if expected.issubset(f.columns)]
    a = pd.concat(frames, ignore_index=True)
    print(f"loaded {len(frames)} csv parts from {len(csvs)} csv files + {len(zips)} zips "
          f"-> {len(a):,} raw rows")
    fams = pd.Series([ev.family for _, ev in DATE_EVIDENCE]).value_counts().to_dict()
    print(f"date formats detected per part: {fams}")
    noniso = [(s, ev) for s, ev in DATE_EVIDENCE if ev.family != "iso"]
    for s, ev in noniso:
        print(f"  NON-ISO  {s}: fmt={ev.fmt!r} family={ev.family} n={ev.n_rows:,} "
              f"first>12={ev.n_first_gt12:,} second>12={ev.n_second_gt12:,}")
    if not noniso:
        print("  every part proved ISO year-first; no day/month ambiguity existed to resolve")
    if bad_schema:
        print(f"  WARNING: {len(bad_schema)} parts skipped for unexpected schema: {bad_schema}")
    if failures:
        print(f"  WARNING: {len(failures)} zip failures: {failures}")
    return a, failures, bad_schema


def main() -> None:
    OUTD.mkdir(parents=True, exist_ok=True)
    a, zip_failures, bad_schema = load_all()

    # 2. keep only the daily-mean parameter; report everything else seen
    par = a["Parametro"].value_counts(dropna=False)
    others = par[par.index != PARAM_KEEP]
    print(f"Parametro values seen: {par.to_dict()}")
    if len(others):
        print(f"  dropping {int(others.sum()):,} rows of other Parametro: {others.to_dict()}")
    a = a[a["Parametro"] == PARAM_KEEP].copy()

    # parse
    a["code"] = a["CodigoEstacion"].str.strip().str.lstrip("0")
    # `date` was set per part in read_dhime_csv() from that part's own evidence.
    # The old ISO-format-then-infer pair here was the hazard dhime_dates
    # test_naive_two_pass_month_gt12_case() demonstrates: on a d/m/Y part the ISO
    # pass yields all-NaT and the inference fallback then picks the layout by luck.
    n_baddate = int(a["date"].isna().sum())
    if n_baddate:
        print(f"  {n_baddate} rows with null Fecha dropped")
        a = a.dropna(subset=["date"])
    a["q_m3s"] = pd.to_numeric(a["Valor"], errors="coerce")
    n_badval = int(a["q_m3s"].isna().sum())
    if n_badval:
        print(f"  {n_badval} rows with non-numeric Valor dropped")
        a = a.dropna(subset=["q_m3s"])
    a["name"] = (a["NombreEstacion"].astype(str)
                 .str.replace(r"\s*\[\d+\]\s*$", "", regex=True).str.strip())
    a["dept"] = a["source"].map(dept_from_filename)
    a["apr"] = a["NivelAprobacion"].map(APPROVAL_RANK).fillna(3).astype(int)

    # 3. de-duplicate (code, date) across sources; quantify disagreements first
    dup_mask = a.duplicated(["code", "date"], keep=False)
    dups = a[dup_mask]
    if len(dups):
        g = dups.groupby(["code", "date"])["q_m3s"]
        vmin, vmax = g.min(), g.max()
        disagree = vmax > vmin
        n_disagree = int(disagree.sum())
        rel = ((vmax - vmin) / vmax.where(vmax != 0, np.nan))[disagree]
        print(f"duplicate (code,date) groups: {g.ngroups:,}; value disagreements: {n_disagree:,} "
              f"({100 * n_disagree / max(1, g.ngroups):.2f}% of dup groups)")
        if n_disagree:
            print(f"  relative spread of disagreeing dups: median {rel.median():.3f}, "
                  f"p95 {rel.quantile(0.95):.3f}, max {rel.max():.3f}")
    n0 = len(a)
    a = a.sort_values(["code", "date", "apr", "q_m3s", "source"], kind="mergesort")
    a = a.drop_duplicates(["code", "date"], keep="first")
    n_dupdrop = n0 - len(a)
    print(f"de-dup (code,date): {n0:,} -> {len(a):,}  ({n_dupdrop:,} duplicate station-days removed)")

    # 4. drop negatives; KEEP zeros and extremes (downstream QC decides)
    neg = a["q_m3s"] < 0
    n_neg = int(neg.sum())
    a = a[~neg].copy()
    print(f"negative q_m3s dropped: {n_neg}")

    # daily product
    daily = a.rename(columns={"NivelAprobacion": "approval"})[["code", "date", "q_m3s", "approval"]]
    daily = daily.sort_values(["code", "date"])
    out_daily = daily.copy()
    out_daily["date"] = out_daily["date"].dt.strftime("%Y-%m-%d")
    out_daily.to_csv(OUTD / "discharge_daily.csv", index=False)

    # 5. inventory: per-station stats + coords + minibacia (left joins)
    a["yr"] = a["date"].dt.year
    inv = a.groupby("code").agg(
        name=("name", "first"),
        dept=("dept", lambda s: s.mode().iloc[0]),
        n_days=("q_m3s", "size"),
        first=("date", "min"),
        last=("date", "max"),
        cov_2011=("yr", lambda s: int((s == 2011).sum())),
        cov_2015_16=("yr", lambda s: int(s.isin([2015, 2016]).sum())),
        zero_days=("q_m3s", lambda s: int((s == 0).sum())),
        p50=("q_m3s", "median"),
        p99=("q_m3s", lambda s: s.quantile(0.99)),
        max=("q_m3s", "max"),
    ).reset_index()
    inv["first"] = inv["first"].dt.strftime("%Y-%m-%d")
    inv["last"] = inv["last"].dt.strftime("%Y-%m-%d")

    coords = pd.read_csv(COORDS, dtype={"code": str})
    coords["code"] = coords["code"].str.lstrip("0")
    inv = inv.merge(coords[["code", "lon", "lat"]].drop_duplicates("code"), on="code", how="left")
    mb = pd.read_csv(MINIB, dtype={"code": str})
    mb["code"] = mb["code"].str.lstrip("0")
    inv = inv.merge(mb[["code", "minibacia"]].drop_duplicates("code"), on="code", how="left")
    n_nocoord = int(inv["lat"].isna().sum())
    n_nomini = int(inv["minibacia"].isna().sum())

    cols = ["code", "name", "dept", "lat", "lon", "minibacia", "n_days", "first", "last",
            "cov_2011", "cov_2015_16", "zero_days", "p50", "p99", "max"]
    inv = inv[cols].sort_values(["dept", "code"])
    inv.to_csv(OUTD / "discharge_inventory.csv", index=False)

    print(f"\nCLEAN: {inv['code'].nunique()} stations | {len(daily):,} station-days | "
          f"{daily['date'].min():%Y-%m-%d} .. {daily['date'].max():%Y-%m-%d}")
    print(f"  stations without coords: {n_nocoord} | without minibacia link: {n_nomini}")
    print(f"  approval mix: {daily['approval'].value_counts().to_dict()}")
    print(f"  zip failures: {len(zip_failures)} | schema-skipped parts: {len(bad_schema)}")
    print("wrote", OUTD / "discharge_daily.csv")
    print("wrote", OUTD / "discharge_inventory.csv")


if __name__ == "__main__":
    main()
