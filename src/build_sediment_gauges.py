"""
Consolidate ALL raw DHIME suspended-sediment downloads into one clean daily table.

The sediment counterpart to `src/build_discharge_gauges.py`. Reads every CSV in
data/raw/observed/sedimento/, every CSV inside every zip there, and the loose
data/raw/observed/concentracion_diaria_santander.csv (all IDEAM "descargaDhime"
exports: CodigoEstacion, NombreEstacion, Variable, Parametro, Fecha, Unidad, Valor,
NivelAprobacion), and produces:

  data/processed/sediment_daily.csv      code, date, ssc_mean_mg_l, ssc_surface_mg_l,
                                         approval, flag_corrupt, flag_zero,
                                         flag_flatline, flatline_run_len
  data/processed/sediment_inventory.csv  one row/station: name, dept, lat, lon,
                                         minibacia, coverage per ENSO phase, stats,
                                         flag counts, value-resolution diagnostic

WHY each step is the way it is (the non-obvious decisions):

1. DATE FORMAT IS DETECTED PER FILE FROM EVIDENCE, NEVER ASSUMED.
   `ssc_cundinamarca.csv` and its zip twin are exported DD/MM/YYYY while the other 14
   sediment files (and all 98 precipitation and 45 discharge files) are ISO yyyy-mm-dd.
   A naive `pd.to_datetime(..., errors='coerce')` silently NaTs the whole department —
   39,815 station-days and 6 stations that exist nowhere else. So the format is proved
   per file: a d/m/y layout is only accepted when at least one row has a component >12
   that can only be a day. Files where both orders are possible, or where the evidence
   is contradictory, ABORT with a message. They are never dropped and never guessed.
   Every detection is cross-checked a second, independent way (`consecutive_day_fraction`,
   below): DHIME exports are per-station consecutive daily series in file order, so the
   correct format yields a high fraction of +1-day steps and the wrong one does not.

2. UNITS ARE CONVERTED EXPLICITLY. Variable CM ("concentracion media diaria") is exported
   in Kg/m3 and Variable CS ("concentracion superficial") in mg/l. Kg/m3 -> mg/L is x1000;
   skipping it is a silent factor-1000 error. Any unit not in UNIT_TO_MGL aborts the run.

3. CM AND CS ARE KEPT AS SEPARATE COLUMNS — they are different physical quantities.
   CM is depth-averaged; CS is a surface grab. At the one station with a real overlap
   (24037360 EL JORDAN, 242 same-day pairs) CS/CM has median 0.715, IQR 0.673-0.768:
   surface concentration runs ~28 % below the depth average with substantial spread,
   exactly as a Rouse profile implies (suspended sand concentrates toward the bed). The
   ratio is a function of grain size and shear velocity, not a constant, so merging the
   two would inject a flow- and station-dependent bias into the very quantity a sediment
   model is calibrated on. REJECTED ALTERNATIVE: rescale CS by 0.715 and merge. It is
   estimable at 1 of 4 CS stations only, and buys ~32 station-days (the CS rows at the two
   stations that have no CM at all) in exchange for an unquantified systematic bias.

4. QC IS FLAGS, NEVER DELETION. The caller decides. See the FLAG constants for the
   thresholds and the reasoning behind each number.

5. MINIBACIA IS INHERITED, NEVER INVENTED. Sediment stations that are also discharge
   stations take the re-snapped mapping from gauge_minibacia.csv (rebuilt by
   src/fix_gauge_minibacia_mapping.py). Sediment-only stations are left unmapped and
   counted: docs/17 showed the naive point-in-cell raster snap that produced the original
   mapping was physically impossible for ~half the discharge network, so manufacturing one
   here would be worse than admitting the gap.

Run:  python src/build_sediment_gauges.py
Requires: pandas, numpy.
"""
import io
import pathlib
import re
import unicodedata
import zipfile

import numpy as np
import pandas as pd

REPO = pathlib.Path(__file__).resolve().parents[1]
SED = REPO / "data" / "raw" / "observed" / "sedimento"
LOOSE = REPO / "data" / "raw" / "observed" / "concentracion_diaria_santander.csv"
MINIB = REPO / "data" / "processed" / "gauge_minibacia.csv"
REMAP = REPO / "data" / "processed" / "gauge_minibacia_remap_report.csv"
COORDS = REPO / "data" / "processed" / "stations_discharge_coords.csv"
QDAILY = REPO / "data" / "processed" / "discharge_daily.csv"
OUTD = REPO / "data" / "processed"

# --- unit -> mg/L. Anything not listed aborts; a silent drop is how factor-1000 errors ship.
UNIT_TO_MGL = {"kg/m3": 1000.0, "g/m3": 1.0, "mg/l": 1.0, "g/l": 1000.0}

# --- approval priority, same ranking as build_discharge_gauges.py
APPROVAL_RANK = {"Definitivo": 0, "En revisión": 1, "En revision": 1, "Preliminar": 2}

# --- QC thresholds -----------------------------------------------------------------
# flag_corrupt: SSC above a physical ceiling. 50,000 mg/L = 5 % sediment by mass.
#   WHY 50,000 and not 40,000: hyperconcentrated flow conventionally begins at ~40,000
#   mg/L and genuinely occurs in steep Andean rivers, so a 40,000 ceiling would flag real
#   physics as corrupt. 50,000 sits just above that transition, so the flag means "cannot
#   be a river SSC measurement" rather than "rare".
#   WHY the exact number does not matter: the run log prints the sensitivity table. In this
#   dataset the 2nd largest value is 32,000 mg/L and the largest is 1.97e8 mg/L, so ANY
#   ceiling in [32,001 , 1.97e8] flags exactly the same single row (station 24037040,
#   2018-05-19, a 1e6 scaling slip). The choice is therefore demonstrably insensitive.
#   REJECTED ALTERNATIVE: a station-relative ceiling (e.g. > 20x the station's own p99).
#   It would (a) mislabel the 1996 delta-station year-scale defect (see the run log) as
#   per-value corruption, when the correct remedy is excluding a period, not a value, and
#   (b) be blind to a slip that affects a station's whole record.
SSC_CEILING_MG_L = 50_000.0

# flag_flatline: member of a run of >= N identical values on CONSECUTIVE CALENDAR DAYS.
#   WHY N=5 and not the 10 that docs/17 used for discharge: Q integrates catchment storage
#   and has strong day-to-day memory (recession), so identical consecutive Q is physically
#   plausible; SSC responds to individual rainfall/erosion events with almost no memory, so
#   identical consecutive SSC is not. Empirically N=10 is nearly vacuous here (143 days at
#   4 stations, 0.05 %) and would let the real artefacts through, while a within-station
#   value shuffle — which preserves each station's exact value multiset and therefore its
#   quantisation coarseness — puts the chance expectation at N>=5 at 0.00037 % against
#   0.354 % observed, a 952x excess (at N>=7 the null is 0 in 20 replicates).
#   REJECTED ALTERNATIVE: N=3. At the coarsely quantised stations (26017060 has 27 distinct
#   values in 2,591 rows) a 3-day repeat is expected by chance, and 1.57 % of all days
#   would be flagged.
#   CONSECUTIVE CALENDAR DAYS, not consecutive rows: sediment records are gappy (~250 d/yr
#   typical). Row-adjacency merges identical values across multi-day gaps and manufactures
#   runs that never happened — that is precisely how an earlier audit arrived at "23
#   stations with runs >=10" from data that has 4 (see the run log).
#   The per-day run length is exported as `flatline_run_len` so a caller who prefers N=10
#   can filter on it without re-deriving anything, and the per-station value resolution
#   (n_distinct / n_days) is exported so a stuck sensor can be told from a coarse rating
#   table — the docs/17 section 3.3 trap.
FLATLINE_MIN_RUN = 5

# --- ENSO phase windows ------------------------------------------------------------
# These are EVENT BRACKETS, not a recomputation of the ONI index (no ONI series is in the
# repo). `lanina_2011` and `elnino_2015_16` deliberately use the calendar spans that
# build_discharge_gauges.py, nb11 and nb12 already key on — redefining them here would
# silently desynchronise this inventory from the rest of the project. The three historical
# events use the Jun/Jul->May/Jun bracket in which ENSO events are conventionally stated,
# because they peak in NDJ and a calendar year would split them.
ENSO_PHASES = {
    "elnino_1997_98": ("1997-05-01", "1998-05-31"),
    "lanina_1999_2000": ("1999-07-01", "2000-06-30"),
    "elnino_2009_10": ("2009-06-01", "2010-05-31"),
    "lanina_2011": ("2011-01-01", "2011-12-31"),
    "elnino_2015_16": ("2015-01-01", "2016-12-31"),
}
MODEL_WINDOW = ("2009-01-01", "2017-12-31")
# candidate calibrate/target pairings to report joint coverage for
PHASE_PAIRINGS = [
    ("lanina_2011", "elnino_2015_16"),
    ("elnino_2009_10", "lanina_2011"),
    ("elnino_1997_98", "lanina_1999_2000"),
    ("elnino_2009_10", "elnino_2015_16"),
]
MIN_PAIRED_DAYS = 30

DEPT_ALIAS = {"valledelcauca": "valle_de_cauca", "nsantander": "norte_de_santander"}


# =========================== date-format detection ==================================
# src/dhime_dates.py is being written by a parallel agent. If it is importable its
# detector is used AND cross-checked against the local one; a disagreement aborts.
# If it is absent, the local implementation below is used and the run log says so.

_LAYOUT = re.compile(
    r"^\s*(\d{1,4})([-/])(\d{1,2})\2(\d{2,4})(?:[ T](\d{1,2}):(\d{2})(?::(\d{2}))?)?\s*$")


class DateFormatUndecidable(RuntimeError):
    """Raised when a file's date format cannot be PROVEN. Never fall back to guessing."""


def detect_date_format(fecha: pd.Series, label: str = "?") -> tuple[str, dict]:
    """Return (strptime_format, evidence) for one DHIME export's Fecha column.

    Evidence-based: a d/m/y ordering is only accepted when some row carries a component
    >12 that can only be a day. No such row => UNDECIDABLE => abort.
    """
    tok = fecha.astype(str).str.extract(_LAYOUT)
    tok.columns = ["t1", "sep", "t2", "t3", "hh", "mm", "ss"]
    n = len(tok)
    n_bad = int(tok["t1"].isna().sum())
    if n_bad:
        ex = fecha[tok["t1"].isna()].head(3).tolist()
        raise DateFormatUndecidable(
            f"{label}: {n_bad}/{n} Fecha values match no d/m/y layout; examples={ex}")
    seps = set(tok["sep"])
    if len(seps) != 1:
        raise DateFormatUndecidable(f"{label}: mixed date separators {seps}")
    sep = seps.pop()
    w1, w3 = set(tok["t1"].str.len()), set(tok["t3"].str.len())
    if len(w1) > 1 and 4 in w1:
        raise DateFormatUndecidable(f"{label}: mixed first-token widths {w1}")
    t1, t2 = tok["t1"].astype(int), tok["t2"].astype(int)
    n_time = int(tok["hh"].notna().sum())
    if n_time not in (0, n):
        raise DateFormatUndecidable(
            f"{label}: {n_time}/{n} rows carry a time-of-day — inconsistent Fecha column")
    tail = " %H:%M" if n_time == n else ""
    n_sec = int(tok["ss"].notna().sum())
    if n_sec:
        if n_sec != n:
            raise DateFormatUndecidable(f"{label}: {n_sec}/{n} rows carry a seconds field")
        tail = " %H:%M:%S"

    ev = {"n": n, "sep": sep, "has_time": n_time == n}
    if w1 == {4}:
        n_t2_gt12 = int((t2 > 12).sum())
        if n_t2_gt12:
            raise DateFormatUndecidable(
                f"{label}: year-first layout but token 2 exceeds 12 in {n_t2_gt12} rows "
                f"(YYYY-DD-MM?) — refusing to guess")
        ev.update(kind="year_first", proof_rows=int((tok['t3'].astype(int) > 12).sum()))
        return f"%Y{sep}%m{sep}%d{tail}", ev
    if w3 not in ({4}, {2}):
        raise DateFormatUndecidable(f"{label}: ambiguous trailing-year widths {w3}")
    ypat = "%Y" if w3 == {4} else "%y"
    n_day_first = int((t1 > 12).sum())    # proves token 1 is a day
    n_month_first = int((t2 > 12).sum())  # proves token 2 is a day
    ev.update(kind="year_last", n_t1_gt12=n_day_first, n_t2_gt12=n_month_first)
    if n_day_first and n_month_first:
        raise DateFormatUndecidable(
            f"{label}: CONTRADICTORY evidence — {n_day_first} rows require day-first and "
            f"{n_month_first} require month-first. The file mixes two formats.")
    if not n_day_first and not n_month_first:
        raise DateFormatUndecidable(
            f"{label}: UNDECIDABLE — no date has a component >12, so DD/MM and MM/DD are "
            f"indistinguishable from this file alone ({n} rows). Refusing to guess.")
    ev["proof_rows"] = n_day_first or n_month_first
    order = f"%d{sep}%m{sep}{ypat}" if n_day_first else f"%m{sep}%d{sep}{ypat}"
    return order + tail, ev


def consecutive_day_fraction(fecha: pd.Series, fmt: str, code: pd.Series) -> float:
    """Independent recheck of a detected format.

    DHIME exports are per-station consecutive daily series in file order, so under the
    correct format most adjacent same-station rows differ by exactly +1 day. Under the
    wrong ordering the series either fails to parse or scrambles. Returns NaN if the
    format cannot parse every row (which is itself decisive).
    """
    d = pd.to_datetime(fecha, format=fmt, errors="coerce")
    if d.isna().any():
        return float("nan")
    df = pd.DataFrame({"c": code.values, "d": d.values})
    same = df["c"] == df["c"].shift(1)
    ok = same & ((df["d"] - df["d"].shift(1)).dt.days == 1)
    return float(ok.sum()) / max(1, int(same.sum()))


def _flip_day_month(fmt: str) -> str:
    return fmt.replace("%d", "\0").replace("%m", "%d").replace("\0", "%m")


try:  # pragma: no cover - src/dhime_dates.py is a separately owned deliverable
    from dhime_dates import detect_date_format as _external_detect
    DETECTOR_NOTE = ("local detector, cross-checked row-for-row against "
                     "src/dhime_dates.detect_date_format — a disagreement aborts the run")
except ImportError:
    _external_detect = None
    DETECTOR_NOTE = ("local detector ONLY — src/dhime_dates.py absent, so the "
                     "second opinion is unavailable")


def detect_and_verify(fecha: pd.Series, code: pd.Series, label: str) -> tuple[str, dict]:
    """Detect the format, then verify it two independent ways before returning it.

    Verification 1: the shared src/dhime_dates.py detector (a separately written
    implementation) must return the identical format string. Verification 2: the
    consecutive-day fraction must be finite under the chosen format.
    """
    fmt, ev = detect_date_format(fecha, label)
    if _external_detect is not None:
        ext_fmt = _external_detect(fecha)  # returns the format string
        if str(ext_fmt) != fmt:
            raise DateFormatUndecidable(
                f"{label}: dhime_dates.py says {ext_fmt!r} but the local detector says "
                f"{fmt!r} — resolve the disagreement, do not pick one")
        ev["confirmed_by"] = "dhime_dates"
    ev["frac_consecutive"] = consecutive_day_fraction(fecha, fmt, code)
    if ev["kind"] == "year_last":
        ev["frac_consecutive_alt"] = consecutive_day_fraction(fecha, _flip_day_month(fmt), code)
    if not (ev["frac_consecutive"] == ev["frac_consecutive"]):  # NaN => cannot parse
        raise DateFormatUndecidable(f"{label}: detected {fmt!r} but it fails to parse every row")
    return fmt, ev


# ================================== ingest =========================================
def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def dept_from_filename(path_like: str) -> str:
    """ssc_valledelcauca_hist.csv -> valle_de_cauca; ssc_boyaca.zip::x.csv -> boyaca.

    Zip members are tagged 'outer.zip::member.csv'; the dept comes from the outer name.
    """
    stem = pathlib.Path(path_like.split("::", 1)[0]).stem
    s = strip_accents(stem).lower()
    for junk in ("concentracion", "diaria", "ssc", "hist"):
        s = s.replace(junk, "")
    s = "".join(ch if ch.isalpha() else "_" for ch in s)
    key = "_".join(p for p in s.split("_") if p)
    return DEPT_ALIAS.get(key, key)


def read_dhime_csv(raw: bytes, source: str) -> pd.DataFrame:
    """Parse one descargaDhime CSV; utf-8 first, latin-1 fallback.

    utf-8 first matters: these files ARE utf-8, and latin-1 would decode them without
    error into mojibake station names (NARINO -> NARIÃ‘O), so the order is not arbitrary.
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
    return d


def iter_zip_csvs(raw: bytes, source: str, frames: list, failures: list) -> None:
    """Collect every CSV member of a zip (recursing into nested zips)."""
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            for nm in zf.namelist():
                if "__MACOSX" in nm:
                    continue
                low, member = nm.lower(), f"{source}::{nm}"
                if low.endswith(".csv"):
                    frames.append(read_dhime_csv(zf.read(nm), member))
                elif low.endswith(".zip"):
                    iter_zip_csvs(zf.read(nm), member, frames, failures)
    except (zipfile.BadZipFile, ValueError, KeyError) as e:
        failures.append((source, repr(e)))


EXPECTED = {"CodigoEstacion", "Variable", "Parametro", "Fecha", "Unidad", "Valor",
            "NivelAprobacion"}


def load_all() -> tuple[list, list, list]:
    frames, failures = [], []
    csvs = sorted(SED.rglob("*.csv"))
    zips = sorted(SED.rglob("*.zip"))
    for p in csvs:
        frames.append(read_dhime_csv(p.read_bytes(), p.name))
    for p in zips:
        iter_zip_csvs(p.read_bytes(), p.name, frames, failures)
    if LOOSE.exists():
        frames.append(read_dhime_csv(LOOSE.read_bytes(), LOOSE.name))
    else:
        failures.append((LOOSE.name, "missing"))
    bad_schema = [f["source"].iloc[0] for f in frames if not EXPECTED.issubset(f.columns)]
    frames = [f for f in frames if EXPECTED.issubset(f.columns)]
    print(f"loaded {len(frames)} csv parts from {len(csvs)} csv files + {len(zips)} zips "
          f"+ {'1 loose file' if LOOSE.exists() else 'no loose file'} "
          f"-> {sum(len(f) for f in frames):,} raw rows")
    if bad_schema:
        print(f"  WARNING: {len(bad_schema)} parts skipped for unexpected schema: {bad_schema}")
    if failures:
        print(f"  WARNING: {len(failures)} ingest failures: {failures}")
    return frames, failures, bad_schema


# ================================ QC helpers =======================================
def flatline_runs(df: pd.DataFrame, value_col: str) -> pd.Series:
    """Length of the identical-value run on CONSECUTIVE CALENDAR DAYS each row belongs to.

    1 where the value is unique-in-place or missing. df must have code/date columns.
    """
    out = pd.Series(1, index=df.index, dtype=int)
    for _, g in df.groupby("code", sort=False):
        g = g.sort_values("date")
        v = g[value_col]
        new = v.ne(v.shift(1)) | g["date"].diff().dt.days.ne(1) | v.isna()
        rid = new.cumsum()
        out.loc[g.index] = rid.map(rid.value_counts()).values
    out[df[value_col].isna()] = 1
    return out


def n_in_window(dates: pd.Series, lo: str, hi: str) -> int:
    return int(dates.between(pd.Timestamp(lo), pd.Timestamp(hi)).sum())


# ==================================== main =========================================
def main() -> None:
    OUTD.mkdir(parents=True, exist_ok=True)
    frames, failures, bad_schema = load_all()

    # ---- 2. detect the date format PER FILE, parse explicitly, assert nothing is lost
    print(f"\ndate-format detection — detector: {DETECTOR_NOTE}")
    print(f"  {'file':<48s} {'format':<20s} {'proof':>6s} {'consec':>7s} {'alt':>7s}")
    fmt_seen: dict[str, list] = {}
    for d in frames:
        src = d["source"].iloc[0]
        fmt, ev = detect_and_verify(d["Fecha"], d["CodigoEstacion"], src)
        d["date"] = pd.to_datetime(d["Fecha"], format=fmt).dt.normalize()
        n_nat = int(d["date"].isna().sum())
        if n_nat:
            raise AssertionError(f"{src}: {n_nat} rows unparsed with proven format {fmt}")
        alt = ev.get("frac_consecutive_alt", float("nan"))
        print(f"  {src:<48s} {fmt:<20s} {ev['proof_rows']:>6,d} "
              f"{ev['frac_consecutive']:>7.3f} {(f'{alt:.3f}' if alt == alt else 'no-parse'):>7s}")
        fmt_seen.setdefault(fmt, []).append(src)
    print(f"  formats found: " + " | ".join(f"{k} x{len(v)}" for k, v in fmt_seen.items()))
    for k, v in fmt_seen.items():
        if len(v) <= 3:
            print(f"    MINORITY FORMAT {k}: {v}")

    a = pd.concat(frames, ignore_index=True)
    assert a["date"].notna().all(), "unparsed dates survived concat"
    print(f"  ALL {len(a):,} rows parsed, 0 unparsed. "
          f"range {a['date'].min():%Y-%m-%d} .. {a['date'].max():%Y-%m-%d}")

    # time-of-day audit — the day-window assumption docs/17 section 3.12 warns about
    tod = a["Fecha"].str.extract(r"(\d{1,2}:\d{2})$")[0].fillna("(none)")
    print(f"  time-of-day stamps: {tod.value_counts().to_dict()}")
    if tod.nunique() > 1:
        odd = a[tod != tod.value_counts().idxmax()]
        print(f"    ATTENTION: {len(odd):,} rows carry a minority stamp — "
              f"{odd['CodigoEstacion'].nunique()} stations, "
              f"{odd['date'].dt.year.min()}-{odd['date'].dt.year.max()}, "
              f"sources {sorted(set(odd['source']))}")

    # ---- 3. units -> mg/L
    a["code"] = a["CodigoEstacion"].str.strip().str.lstrip("0")
    a["unit"] = a["Unidad"].astype(str).str.strip().str.lower()
    unknown = sorted(set(a["unit"]) - set(UNIT_TO_MGL))
    if unknown:
        raise AssertionError(f"unknown Unidad values {unknown} — add them to UNIT_TO_MGL "
                            f"with a conversion factor; refusing to drop them silently")
    print(f"\nunit mix (raw rows): {a['unit'].value_counts().to_dict()}")
    print(f"  Variable x Unidad: "
          f"{a.groupby(['Variable', 'unit']).size().to_dict()}")
    print(f"  Parametro: {a['Parametro'].value_counts().to_dict()}")
    val = pd.to_numeric(a["Valor"], errors="coerce")
    n_badval = int(val.isna().sum())
    if n_badval:
        print(f"  WARNING: {n_badval} non-numeric Valor rows dropped")
        a, val = a[val.notna()].copy(), val[val.notna()]
    a["ssc_mg_l"] = val.values * a["unit"].map(UNIT_TO_MGL).values
    print(f"  converted to mg/L: {len(a):,} rows, 0 non-numeric remaining")

    var_unexpected = sorted(set(a["Variable"]) - {"CM", "CS"})
    if var_unexpected:
        raise AssertionError(f"unexpected Variable codes {var_unexpected} — CM is "
                            f"depth-averaged and CS is surface; a third quantity needs "
                            f"its own column, not silent merging into one of these")

    # ---- 4. de-duplicate (code, date, Variable), highest approval wins
    a["name"] = (a["NombreEstacion"].astype(str)
                 .str.replace(r"\s*\[\d+\]\s*$", "", regex=True).str.strip())
    a["dept"] = a["source"].map(dept_from_filename)
    a["apr"] = a["NivelAprobacion"].map(APPROVAL_RANK).fillna(3).astype(int)
    key = ["code", "date", "Variable"]
    g = a.groupby(key)["ssc_mg_l"]
    n_groups = g.ngroups
    nun = g.nunique()
    n_conflict = int((nun > 1).sum())
    n_apr_conflict = int((a.groupby(key)["NivelAprobacion"].nunique() > 1).sum())
    print(f"\nde-dup on (code,date,Variable): {len(a):,} rows -> {n_groups:,} groups "
          f"({len(a) - n_groups:,} duplicate rows removed)")
    print(f"  value-CONFLICTING groups: {n_conflict}   approval-conflicting groups: "
          f"{n_apr_conflict}")
    if n_conflict:
        c = nun[nun > 1].index[:5].tolist()
        spread = g.max() - g.min()
        print(f"    examples {c}; max absolute spread {spread.max():,.1f} mg/L — "
              f"the approval rule is arbitrating real disagreements, inspect them")
    a = a.sort_values(key + ["apr", "ssc_mg_l", "source"], kind="mergesort")
    a = a.drop_duplicates(key, keep="first")
    print(f"  approval mix after dedup: {a['NivelAprobacion'].value_counts().to_dict()}")

    # ---- 5. wide: CM and CS as SEPARATE columns, one row per (code, date)
    piv = a.pivot_table(index=["code", "date"], columns="Variable", values="ssc_mg_l",
                        aggfunc="first")
    for c in ("CM", "CS"):
        if c not in piv:
            piv[c] = np.nan
    daily = (piv.rename(columns={"CM": "ssc_mean_mg_l", "CS": "ssc_surface_mg_l"})
             .reset_index()[["code", "date", "ssc_mean_mg_l", "ssc_surface_mg_l"]])
    apr = (a.sort_values(["code", "date", "Variable"])  # CM sorts before CS
           .drop_duplicates(["code", "date"], keep="first")[["code", "date", "NivelAprobacion"]]
           .rename(columns={"NivelAprobacion": "approval"}))
    daily = daily.merge(apr, on=["code", "date"], how="left")
    n_mean = int(daily["ssc_mean_mg_l"].notna().sum())
    n_surf = int(daily["ssc_surface_mg_l"].notna().sum())
    n_both = int((daily["ssc_mean_mg_l"].notna() & daily["ssc_surface_mg_l"].notna()).sum())
    print(f"\nCM/CS kept separate: {len(daily):,} station-days | "
          f"CM (depth-averaged) {n_mean:,} at {daily.loc[daily.ssc_mean_mg_l.notna(),'code'].nunique()} st "
          f"| CS (surface) {n_surf:,} at {daily.loc[daily.ssc_surface_mg_l.notna(),'code'].nunique()} st "
          f"| same-day both {n_both:,}")
    if n_both:
        r = (daily["ssc_surface_mg_l"] / daily["ssc_mean_mg_l"]).replace([np.inf, -np.inf], np.nan).dropna()
        print(f"  CS/CM ratio on the {len(r):,} overlapping days: median {r.median():.3f}, "
              f"IQR {r.quantile(.25):.3f}-{r.quantile(.75):.3f} — NOT 1.0 and NOT constant, "
              f"which is why they are not merged")
    surf_only = daily.loc[daily.ssc_mean_mg_l.isna() & daily.ssc_surface_mg_l.notna(), "code"]
    print(f"  CS-only station-days (would be LOST by a CM-only pipeline): {len(surf_only):,} "
          f"at stations {sorted(surf_only.unique())}")

    # ---- 6. QC flags as COLUMNS
    daily = daily.sort_values(["code", "date"]).reset_index(drop=True)
    daily["flag_corrupt"] = ((daily["ssc_mean_mg_l"] > SSC_CEILING_MG_L)
                            | (daily["ssc_surface_mg_l"] > SSC_CEILING_MG_L))
    daily["flag_zero"] = ((daily["ssc_mean_mg_l"] == 0) | (daily["ssc_surface_mg_l"] == 0))
    run_m = flatline_runs(daily, "ssc_mean_mg_l")
    run_s = flatline_runs(daily, "ssc_surface_mg_l")
    daily["flatline_run_len"] = np.maximum(run_m, run_s)
    daily["flag_flatline"] = daily["flatline_run_len"] >= FLATLINE_MIN_RUN

    print(f"\nQC flags (columns, nothing deleted):")
    print(f"  ceiling sensitivity — rows above each candidate ceiling:")
    for t in (10_000, 20_000, 30_000, 40_000, 50_000, 100_000, 1e6):
        s = daily[(daily["ssc_mean_mg_l"] > t) | (daily["ssc_surface_mg_l"] > t)]
        print(f"    > {t:>12,.0f} mg/L : {len(s):5d} rows  {s['code'].nunique():3d} stations")
    print(f"  flag_corrupt (> {SSC_CEILING_MG_L:,.0f} mg/L): {int(daily.flag_corrupt.sum())} rows, "
          f"{daily.loc[daily.flag_corrupt,'code'].nunique()} stations "
          f"{daily.loc[daily.flag_corrupt, ['code','date','ssc_mean_mg_l']].to_dict('records')}")
    print(f"  flag_zero: {int(daily.flag_zero.sum())} rows, "
          f"{daily.loc[daily.flag_zero,'code'].nunique()} stations")
    print(f"  flatline run-length sensitivity (calendar-adjacent):")
    for nn in (3, 5, 7, 10, 15, 20, 30):
        m = daily["flatline_run_len"] >= nn
        print(f"    N>={nn:3d}: {int(m.sum()):6,d} days ({m.mean() * 100:5.2f}%)  "
              f"{daily.loc[m, 'code'].nunique():3d} stations")
    print(f"  flag_flatline (N>={FLATLINE_MIN_RUN}): {int(daily.flag_flatline.sum())} rows, "
          f"{daily.loc[daily.flag_flatline,'code'].nunique()} stations, "
          f"longest run {int(daily.flatline_run_len.max())} d")
    n_any = int((daily.flag_corrupt | daily.flag_zero | daily.flag_flatline).sum())
    print(f"  any flag: {n_any:,} of {len(daily):,} station-days ({n_any/len(daily)*100:.2f}%)")

    # ---- diagnostic: year-scale defects (docs/17 section 3.4 analogue). Reported, not flagged:
    #      the remedy for these is excluding a PERIOD, which is the caller's decision.
    cmv = daily[daily["ssc_mean_mg_l"].notna() & ~daily["flag_corrupt"]].copy()
    cmv["yr"] = cmv["date"].dt.year
    rows = []
    for c, gg in cmv.groupby("code"):
        for y, gy in gg.groupby("yr"):
            if len(gy) < 60:
                continue
            other = gg.loc[gg.yr != y, "ssc_mean_mg_l"]
            if len(other) < 60:
                continue
            rows.append((c, y, len(gy), gy["ssc_mean_mg_l"].median(), other.median()))
    ys = pd.DataFrame(rows, columns=["code", "yr", "n", "med_yr", "med_other"])
    ys["ratio"] = ys["med_yr"] / ys["med_other"].replace(0, np.nan)
    flagged = ys[(ys.ratio > 10) | (ys.ratio < 0.1)].sort_values("ratio", ascending=False)
    print(f"\nyear-scale audit ({len(ys)} station-years with >=60 d): "
          f"ratio p50 {ys.ratio.median():.2f} p95 {ys.ratio.quantile(.95):.2f} "
          f"max {ys.ratio.max():,.0f}")
    print(f"  {len(flagged)} station-years shifted >=10x vs the station's other years "
          f"(NOT flagged per-row — the remedy is excluding a period):")
    for _, r in flagged.iterrows():
        print(f"    {r.code} {int(r.yr)}  n={int(r.n):4d}  median {r.med_yr:>10,.1f} vs "
              f"{r.med_other:>8,.1f} mg/L  ratio {r.ratio:>8.2f}x")

    # ---- 7. attach lon/lat + minibacia (inherited only, never invented)
    mb = pd.read_csv(MINIB, dtype={"code": str})
    mb["code"] = mb["code"].str.lstrip("0")
    co = pd.read_csv(COORDS, dtype={"code": str})
    co["code"] = co["code"].str.lstrip("0")
    rr = pd.read_csv(REMAP, dtype={"code": str})
    rr["code"] = rr["code"].str.lstrip("0")

    ok = daily[~daily.flag_corrupt]
    inv = daily.groupby("code").agg(n_days=("date", "size"), first=("date", "min"),
                                    last=("date", "max")).reset_index()
    meta = a.groupby("code").agg(name=("name", "first"),
                                 dept=("dept", lambda s: s.mode().iloc[0])).reset_index()
    inv = inv.merge(meta, on="code", how="left")
    # n_mean_days counts EVERY CM station-day (flagged included — flags are not deletions);
    # the value statistics exclude flag_corrupt only, or the 1.97e8 mg/L slip would set `max`.
    inv = inv.merge(daily.groupby("code")["ssc_mean_mg_l"].count()
                    .rename("n_mean_days").reset_index(), on="code", how="left")
    stat = ok.groupby("code")["ssc_mean_mg_l"].agg(
        p50="median", p99=lambda s: s.quantile(0.99), max="max",
        n_distinct="nunique").reset_index()
    inv = inv.merge(stat, on="code", how="left")
    inv["resolution"] = inv["n_distinct"] / inv["n_mean_days"]
    inv = inv.merge(daily.groupby("code")["ssc_surface_mg_l"].count()
                    .rename("n_surface_days").reset_index(), on="code", how="left")
    for nm, (lo, hi) in ENSO_PHASES.items():
        inv = inv.merge(daily[daily.ssc_mean_mg_l.notna()].groupby("code")["date"]
                        .apply(lambda s, lo=lo, hi=hi: n_in_window(s, lo, hi))
                        .rename(f"cov_{nm}").reset_index(), on="code", how="left")
    inv = inv.merge(daily[daily.ssc_mean_mg_l.notna()].groupby("code")["date"]
                    .apply(lambda s: n_in_window(s, *MODEL_WINDOW))
                    .rename("cov_2009_2017").reset_index(), on="code", how="left")
    for f in ("flag_corrupt", "flag_zero", "flag_flatline"):
        inv = inv.merge(daily.groupby("code")[f].sum().rename(f"n_{f[5:]}").reset_index(),
                        on="code", how="left")
    inv = inv.merge(co[["code", "lon", "lat"]].drop_duplicates("code"), on="code", how="left")
    inv = inv.merge(mb[["code", "minibacia"]].drop_duplicates("code"), on="code", how="left")
    inv = inv.merge(rr[["code", "action"]].drop_duplicates("code")
                    .rename(columns={"action": "mapping_action"}), on="code", how="left")

    n_st = len(inv)
    n_map = int(inv["minibacia"].notna().sum())
    n_coord = int(inv["lat"].notna().sum())
    q = pd.read_csv(QDAILY, dtype={"code": str}, parse_dates=["date"])
    q["code"] = q["code"].str.lstrip("0")
    qcodes = set(q["code"])
    inv["is_discharge_station"] = inv["code"].isin(qcodes)
    print(f"\nmapping: {n_st} sediment stations | {n_map} inherit a minibacia from "
          f"gauge_minibacia.csv | {n_coord} have coordinates | "
          f"{int(inv.is_discharge_station.sum())} are also discharge stations")
    gap = inv[inv.minibacia.isna() & inv.is_discharge_station]
    print(f"  UNMAPPED: {n_st - n_map} stations. Of these {len(gap)} ARE discharge stations "
          f"but were never mapped: {sorted(gap.code)} — all zone "
          f"{sorted(set(c[:2] for c in gap.code))} (the docs/17 section 5.3 delta-gauge item).")
    sed_only = inv[inv.minibacia.isna() & ~inv.is_discharge_station]
    print(f"  {len(sed_only)} are sediment-only, of which "
          f"{int(sed_only.lat.isna().sum())} have no coordinates at all.")
    print("  NO SNAP IS INVENTED. To map them: (1) pull coordinates for the "
          f"{int(sed_only.lat.isna().sum())} coordinate-less stations "
          "(extend src/fetch_station_coords.py); (2) re-snap by drainage-area matching as "
          "src/fix_gauge_minibacia_mapping.py does — but that scores candidates by runoff "
          "coefficient, which needs a Q series these stations do not have, so it must fall "
          "back to the IDEAM catalogue drainage area. The point-in-cell raster snap is NOT "
          "an option: docs/17 section 3.1 showed it was physically impossible for 79 of 159 "
          "discharge gauges.")

    # ---- 8. paired SSC + Q availability
    pair = (daily[daily.ssc_mean_mg_l.notna()][["code", "date", "flag_corrupt", "flag_zero"]]
            .merge(q[["code", "date", "q_m3s"]], on=["code", "date"]))
    mapped = set(mb["code"])
    distrib = set(rr.loc[rr.action == "excluded_distributary", "code"])
    nm_by_code = inv.set_index("code")["name"].to_dict()
    intake = {c for c in mapped if any(k in str(nm_by_code.get(c, "")).upper()
                                       for k in ("BOCATOMA", "CANAL"))}
    # docs/17 section 5.1 "exclude structurally / permanently"
    safe = mapped - distrib - intake - {"28037020", "2319700100"}
    safe = {c for c in safe if c[:2] in {f"2{i}" for i in range(1, 10)}}
    clean = ~(pair.flag_corrupt | pair.flag_zero) & (pair.q_m3s > 0)

    print(f"\npaired SSC(CM) + Q availability against discharge_daily.csv:")
    print(f"  {'set':<44s} {'days':>9s} {'stations':>9s} {'clean days':>11s}")
    for lbl, sub in [("all sediment stations", pair),
                     ("has a minibacia (28-station definition)", pair[pair.code.isin(mapped)]),
                     ("docs/17 calibration-safe", pair[pair.code.isin(safe)])]:
        cl = sub[clean.reindex(sub.index, fill_value=False)]
        print(f"  {lbl:<44s} {len(sub):>9,d} {sub.code.nunique():>9d} {len(cl):>11,d}")
    print(f"  intake/canal gauges inside the mapped set (docs/17 section 3.6 says exclude): "
          f"{sorted(mapped & intake & set(pair.code))}")

    psafe = pair[pair.code.isin(safe)]
    print(f"\n  by period, restricted to the {psafe.code.nunique()} calibration-safe "
          f"sediment+Q stations (clean = not zero/corrupt SSC and Q>0):")
    periods = [("full record", str(daily.date.min().date()), str(daily.date.max().date())),
               ("model window 2009-2017", *MODEL_WINDOW)] + \
              [(k, *v) for k, v in ENSO_PHASES.items()]
    for lbl, lo, hi in periods:
        s = psafe[psafe.date.between(pd.Timestamp(lo), pd.Timestamp(hi))]
        cl = s[~(s.flag_corrupt | s.flag_zero) & (s.q_m3s > 0)]
        ge30 = int((cl.groupby("code").size() >= MIN_PAIRED_DAYS).sum())
        print(f"    {lbl:<24s} {lo}..{hi}  {len(s):>7,d} days  "
              f"{s.code.nunique():>3d} st  clean {len(cl):>7,d}  "
              f">={MIN_PAIRED_DAYS}d: {ge30:>3d} st")

    print(f"\n  stations with >={MIN_PAIRED_DAYS} clean paired days in BOTH phases of each "
          f"candidate calibrate/target pairing:")
    cl_all = psafe[~(psafe.flag_corrupt | psafe.flag_zero) & (psafe.q_m3s > 0)]
    for p1, p2 in PHASE_PAIRINGS:
        s1 = set(cl_all[cl_all.date.between(*map(pd.Timestamp, ENSO_PHASES[p1]))]
                 .groupby("code").filter(lambda x: len(x) >= MIN_PAIRED_DAYS)["code"])
        s2 = set(cl_all[cl_all.date.between(*map(pd.Timestamp, ENSO_PHASES[p2]))]
                 .groupby("code").filter(lambda x: len(x) >= MIN_PAIRED_DAYS)["code"])
        both = sorted(s1 & s2)
        print(f"    {p1:<17s} vs {p2:<17s} : {len(s1):>3d} / {len(s2):>3d} -> BOTH "
              f"{len(both):>3d}  {both}")

    # ---- 9. write
    cols_d = ["code", "date", "ssc_mean_mg_l", "ssc_surface_mg_l", "approval",
              "flag_corrupt", "flag_zero", "flag_flatline", "flatline_run_len"]
    out = daily[cols_d].copy()
    out["date"] = out["date"].dt.strftime("%Y-%m-%d")
    out.to_csv(OUTD / "sediment_daily.csv", index=False)

    inv["first"] = inv["first"].dt.strftime("%Y-%m-%d")
    inv["last"] = inv["last"].dt.strftime("%Y-%m-%d")
    inv["calibration_safe"] = inv["code"].isin(safe)
    cols_i = (["code", "name", "dept", "lat", "lon", "minibacia", "mapping_action",
               "is_discharge_station", "calibration_safe", "n_days", "n_mean_days",
               "n_surface_days", "first", "last"]
              + [f"cov_{k}" for k in ENSO_PHASES] + ["cov_2009_2017"]
              + ["p50", "p99", "max", "n_distinct", "resolution",
                 "n_corrupt", "n_zero", "n_flatline"])
    inv[cols_i].sort_values(["dept", "code"]).to_csv(OUTD / "sediment_inventory.csv", index=False)

    print(f"\nCLEAN: {n_st} stations | {len(daily):,} station-days | "
          f"{daily.date.min():%Y-%m-%d} .. {daily.date.max():%Y-%m-%d}")
    print(f"  CM mg/L distribution (flag_corrupt excluded): "
          f"p50 {ok.ssc_mean_mg_l.median():,.0f}  p99 {ok.ssc_mean_mg_l.quantile(.99):,.0f}  "
          f"p99.9 {ok.ssc_mean_mg_l.quantile(.999):,.0f}  max {ok.ssc_mean_mg_l.max():,.0f}")
    print(f"  ingest failures: {len(failures)} | schema-skipped parts: {len(bad_schema)}")
    print("wrote", OUTD / "sediment_daily.csv")
    print("wrote", OUTD / "sediment_inventory.csv")


if __name__ == "__main__":
    main()
