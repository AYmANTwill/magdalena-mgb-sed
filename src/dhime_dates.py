"""
Evidence-based date-format detection for IDEAM DHIME CSV exports.

WHY THIS MODULE EXISTS
----------------------
DHIME exports the `Fecha` column in at least two mutually incompatible layouts:

    1990-01-01 00:00      ISO, year-first  (15 of 16 sediment files, 98 precip, 45 discharge)
    01/01/1990 00:00      day-first        (ssc_cundinamarca.csv and ssc_cundinamarca.zip only)

Both are 16 characters of digits and separators. Neither carries a locale tag. A parser
that guesses is a parser that will eventually transpose day and month on a file nobody
re-reads, and the transposition is invisible downstream: the dates stay inside the
record's real span, the count stays the same, nothing raises.

THE NAIVE FIX AND WHY IT IS UNSAFE
----------------------------------
The rejected approach was:

    d = pd.to_datetime(s, errors="coerce")                       # pass 1: inference
    d = d.fillna(pd.to_datetime(s, format="%d/%m/%Y %H:%M",      # pass 2: day-first rescue
                                errors="coerce"))

That recovers Cundinamarca only by luck. pandas infers a format from the FIRST element,
gets `%m/%d/%Y`, and then chokes on every row whose day exceeds 12 -- which in a
1990-2018 daily record is roughly 61 % of rows. The mass of NaT is what triggers pass 2.

Now delete every day>12 row, or take a station whose record happens to be 1st-12th only,
or a monthly-sampled campaign series. Pass 1 succeeds on all rows month-first, produces
zero NaT, pass 2 never fires, and 06/08/2004 is silently recorded as 8 June instead of
6 August. Same row count. No warning. See `test_naive_two_pass_transposes()`.

The defect is structural: pass-2-on-failure uses *parse failure* as its evidence, and
parse failure is not evidence of layout. A DD/MM column is only detectably DD/MM if it
contains a day>12 -- and then only by accident.

WHAT THIS MODULE DOES INSTEAD
-----------------------------
Evidence is counted on the FIELD VALUES, before any parsing:

    n_first_gt12  > 0  ->  field 1 cannot be a month  ->  day-first   (positive proof)
    n_second_gt12 > 0  ->  field 2 cannot be a month  ->  month-first (positive proof)
    both > 0           ->  ContradictoryDateFormat, raise. Two layouts in one column.
    neither            ->  AmbiguousDateFormat, raise. There is no evidence. Do not guess.

Then a second, independent check (`_sortedness_hint`) compares sortedness under the two
readings, restricted to the rows that parse under BOTH -- i.e. exactly the rows the >12
test did not decide, which is what makes it independent. DHIME exports arrive date-sorted
within a station block, so on `ssc_cundinamarca.csv` this yields sorted_frac 0.9997 for
d/m/Y vs 0.9036 for m/d/Y over the 15,644-row ambiguous subset. It is circumstantial and
is never allowed to decide: it corroborates the >12 proof (and prints a WARNING if it
contradicts it), and on a raise it is reported as a lead for the caller to chase.

WHAT A CALLER SHOULD DO ON AmbiguousDateFormat
----------------------------------------------
Not guess. In order of preference:

    1. Look for a sibling file from the same export batch that IS decidable (the
       Cundinamarca csv/zip pair is one export duplicated: decide on the larger, apply
       to both -- pass `fmt=` explicitly to `parse_dates_safe` for the undecidable twin).
    2. Cross-check against another variable for the same station: SSC station-days should
       land on days the discharge record also has. Score date-set overlap under DMY vs MDY;
       a real match is lopsided.
    3. Check the station's known operating span from the inventory. A hypothesis that
       places data outside the span is refuted.
    4. If none of the above resolves it, EXCLUDE the file and record the exclusion.
       A dropped department is recoverable. A transposed one corrupts the calibration
       and looks fine.

Deliberately NOT offered: a `default_dayfirst=` argument. An escape hatch with a default
is how a guess gets shipped -- the caller must name the format at the call site, in code
review, with the evidence in the commit message.

USAGE
-----
    from dhime_dates import detect_date_format, parse_dates_safe

    fmt = detect_date_format(df["Fecha"])        # raises rather than guessing
    df["date"] = parse_dates_safe(df["Fecha"], fmt).dt.normalize()

Input schema (DHIME CSV, all sediment/precip/discharge parts):
    CodigoEstacion,NombreEstacion,Variable,Parametro,Fecha,Unidad,Valor,NivelAprobacion
    21237020,ARRANCAPLUMAS - AUT [21237020],CM,Concentracion media diaria en Kg/m3,\
13/08/2004 00:00,Kg/m3,0.353,Preliminar
This module touches `Fecha` only: it takes a Series of strings and returns a Series of
datetime64[ns], or raises.

Run `python src/dhime_dates.py` to execute the smoke tests.
"""

from __future__ import annotations

import re
from typing import NamedTuple

import pandas as pd

# ---------------------------------------------------------------------------
# format constants -- every one is an explicit strptime string. There is no
# code path in this module that calls pd.to_datetime without `format=`.
# ---------------------------------------------------------------------------
ISO = "%Y-%m-%d"
ISO_HM = "%Y-%m-%d %H:%M"
ISO_HMS = "%Y-%m-%d %H:%M:%S"
DMY = "%d/%m/%Y"
DMY_HM = "%d/%m/%Y %H:%M"
DMY_HMS = "%d/%m/%Y %H:%M:%S"
MDY = "%m/%d/%Y"
MDY_HM = "%m/%d/%Y %H:%M"
MDY_HMS = "%m/%d/%Y %H:%M:%S"

MAX_MONTH = 12  # a field >12 cannot be a month. The whole detector rests on this.
# Minimum gap in sorted-fraction before the (circumstantial) ordering hint is allowed
# to express a preference at all. 0.02 sits far above the station-reset noise floor
# (~n_stations/n_rows, e.g. 5/39,814 = 0.00013 for ssc_cundinamarca.csv) and far below
# the real separation measured there (0.9997 vs 0.9036, margin 0.096).
SORT_MARGIN = 0.02

# Three numeric fields + optional time. Anchored at both ends: the pattern must
# consume the ENTIRE string, so an unexpected trailing token (seconds, timezone,
# a stray quote) fails detection loudly instead of being ignored.
_YEAR_FIRST = re.compile(
    r"^\s*(?P<a>\d{4})[-/](?P<b>\d{1,2})[-/](?P<c>\d{1,2})"
    r"(?:[ T](?P<H>\d{1,2}):(?P<M>\d{2})(?::(?P<S>\d{2}))?)?\s*$"
)
_YEAR_LAST = re.compile(
    r"^\s*(?P<a>\d{1,2})[-/](?P<b>\d{1,2})[-/](?P<c>\d{4})"
    r"(?:[ T](?P<H>\d{1,2}):(?P<M>\d{2})(?::(?P<S>\d{2}))?)?\s*$"
)
# 2-digit year: a SECOND ambiguity axis on top of day/month. Matched only so it
# can be refused by name rather than falling through as "unrecognised".
_TWO_DIGIT_YEAR = re.compile(r"^\s*\d{1,2}[-/]\d{1,2}[-/]\d{2}(?:[ T]\d{1,2}:\d{2}(?::\d{2})?)?\s*$")


class DateFormatError(ValueError):
    """Base: the format could not be established beyond doubt."""


class AmbiguousDateFormat(DateFormatError):
    """Every field is <=12. No evidence exists. See module docstring for what to do."""


class ContradictoryDateFormat(DateFormatError):
    """Some rows prove day-first, others prove month-first. One column, two layouts."""


class UnrecognisedDateFormat(DateFormatError):
    """Not ISO, not d/m/Y, not m/d/Y -- or the pattern did not consume the whole string."""


class DateParseError(ValueError):
    """The chosen explicit format produced NaT on input that was not null."""


class SortHint(NamedTuple):
    """Circumstantial ordering evidence on the rows both hypotheses can parse."""

    sorted_frac_dmy: float
    sorted_frac_mdy: float
    n_subset: int
    prefers_dayfirst: bool | None   # None = margin too small to discriminate


class DateEvidence(NamedTuple):
    """Auditable detection record. Log this, do not just log the format string."""

    fmt: str
    family: str            # 'iso' | 'dmy' | 'mdy'
    n_rows: int            # non-null strings examined
    n_first_gt12: int      # positive proof of day-first
    n_second_gt12: int     # positive proof of month-first
    max_first: int
    max_second: int
    has_time: bool
    sort_hint: SortHint | None      # independent cross-check; None for ISO
    sort_agrees: bool | None        # None = hint could not discriminate


# ---------------------------------------------------------------------------
# internals
# ---------------------------------------------------------------------------
def _clean(series: pd.Series) -> pd.Series:
    """Non-null values as stripped strings. Blank-only cells count as null."""
    s = series.dropna().astype(str).str.strip()
    return s[s != ""]


def _time_suffix(has_time: bool, has_secs: bool) -> str:
    if has_secs:
        return " %H:%M:%S"
    if has_time:
        return " %H:%M"
    return ""


def _sorted_frac(x: pd.Series) -> float:
    x = x.dropna()
    if len(x) < 2:
        return float("nan")
    return float((x.diff().dropna() >= pd.Timedelta(0)).mean())


def _sortedness_hint(s: pd.Series, dmy_fmt: str, mdy_fmt: str) -> SortHint:
    """
    Second, INDEPENDENT line of evidence: DHIME exports arrive sorted by date within
    each station block, so the correct reading should be markedly closer to sorted.

    Evaluated on the AMBIGUOUS SUBSET only -- the rows that parse under *both*
    hypotheses. Restricting to that subset is what makes this independent of the >12
    count: it deliberately throws away every row that the >12 test already decided.

    Circumstantial, never decisive, for two reasons:
      * a series sampled only on the 1st-12th is perfectly sorted under BOTH readings
        (06/08,07/08,...,12/08 -> Aug 6..12, or Jun 8/Jul 8/.../Dec 8: both ascending),
        so the margin collapses to 0 exactly where a decision is most wanted;
      * station-block boundaries inside a concatenated export create genuine backward
        steps (~n_stations/n_rows worth), so neither fraction reaches 1.0.
    It corroborates or contradicts; it does not vote.
    """
    d = pd.to_datetime(s, format=dmy_fmt, errors="coerce")
    m = pd.to_datetime(s, format=mdy_fmt, errors="coerce")
    both = d.notna() & m.notna()
    n = int(both.sum())
    if n < 2:
        return SortHint(float("nan"), float("nan"), n, None)
    fd, fm = _sorted_frac(d[both]), _sorted_frac(m[both])
    margin = fd - fm
    prefers = None if abs(margin) < SORT_MARGIN else (fd > fm)
    return SortHint(fd, fm, n, prefers)


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------
def detect_date_format(series: pd.Series, *, return_evidence: bool = False):
    """
    Establish the date layout of `series` from evidence, or raise.

    Never returns a format it cannot prove. Never falls back to pandas inference.

    Returns the strptime format string, or a `DateEvidence` when
    `return_evidence=True` (use this in ingest scripts so the audit trail records
    *why*, not just *what*).

    Raises
    ------
    AmbiguousDateFormat      every field <=12 -- undecidable, caller must resolve
    ContradictoryDateFormat  both day-first and month-first proofs present
    UnrecognisedDateFormat   unparseable shape, mixed shapes, or 2-digit years
    """
    s = _clean(series)
    if s.empty:
        raise UnrecognisedDateFormat("no non-null date strings to inspect")

    n = len(s)
    yf = s.str.extract(_YEAR_FIRST)
    yl = s.str.extract(_YEAR_LAST)
    n_yf = int(yf["a"].notna().sum())
    n_yl = int(yl["a"].notna().sum())

    if n_yf and n_yl:
        raise UnrecognisedDateFormat(
            f"mixed layouts in one column: {n_yf} year-first and {n_yl} year-last rows "
            f"of {n}. Split the file by layout and detect each part separately."
        )
    if not n_yf and not n_yl:
        bad = s[~s.str.match(_YEAR_FIRST) & ~s.str.match(_YEAR_LAST)]
        if bad.str.match(_TWO_DIGIT_YEAR).any():
            raise UnrecognisedDateFormat(
                "2-digit years present (e.g. "
                f"{bad[bad.str.match(_TWO_DIGIT_YEAR)].iloc[0]!r}): year/day/month are all "
                "ambiguous. Re-export with 4-digit years."
            )
        raise UnrecognisedDateFormat(
            f"no row matched ISO or d/m/Y or m/d/Y, e.g. {bad.iloc[0]!r} "
            f"({len(bad)} of {n} unmatched)"
        )
    if n_yf and n_yf < n:
        raise UnrecognisedDateFormat(
            f"{n - n_yf} of {n} rows did not fully match ISO, e.g. "
            f"{s[~s.str.match(_YEAR_FIRST)].iloc[0]!r}"
        )
    if n_yl and n_yl < n:
        raise UnrecognisedDateFormat(
            f"{n - n_yl} of {n} rows did not fully match d/m/Y or m/d/Y, e.g. "
            f"{s[~s.str.match(_YEAR_LAST)].iloc[0]!r}"
        )

    # ---- year-first: unambiguous by construction (yyyy-mm-dd, month before day) ----
    if n_yf:
        g = yf
        has_time = bool(g["H"].notna().all())
        has_secs = bool(g["S"].notna().all())
        if g["H"].notna().any() and not has_time:
            raise UnrecognisedDateFormat(
                f"time component present on only {int(g['H'].notna().sum())} of {n} rows"
            )
        if g["S"].notna().any() and not has_secs:
            raise UnrecognisedDateFormat(
                f"seconds present on only {int(g['S'].notna().sum())} of {n} rows"
            )
        b = g["b"].astype(int)
        c = g["c"].astype(int)
        if (b > MAX_MONTH).any():
            raise UnrecognisedDateFormat(
                f"year-first layout with field 2 > 12 (max {int(b.max())}): "
                "this is yyyy-dd-mm, not ISO. Refusing to guess."
            )
        fmt = ISO + _time_suffix(has_time, has_secs)
        ev = DateEvidence(fmt, "iso", n, 0, 0, int(b.max()), int(c.max()),
                          has_time, None, None)
        return ev if return_evidence else fmt

    # ---- year-last: the ambiguous family. Count evidence. ----
    g = yl
    has_time = bool(g["H"].notna().all())
    has_secs = bool(g["S"].notna().all())
    if g["H"].notna().any() and not has_time:
        raise UnrecognisedDateFormat(
            f"time component present on only {int(g['H'].notna().sum())} of {n} rows"
        )
    if g["S"].notna().any() and not has_secs:
        raise UnrecognisedDateFormat(
            f"seconds present on only {int(g['S'].notna().sum())} of {n} rows"
        )
    first = g["a"].astype(int)
    second = g["b"].astype(int)
    n_first_gt12 = int((first > MAX_MONTH).sum())
    n_second_gt12 = int((second > MAX_MONTH).sum())

    if (first > 31).any() or (second > 31).any():
        raise UnrecognisedDateFormat(
            f"field >31 present (max_first={int(first.max())}, "
            f"max_second={int(second.max())}): neither field is a day-of-month"
        )

    if n_first_gt12 and n_second_gt12:
        ex_d = s[first > MAX_MONTH].iloc[0]
        ex_m = s[second > MAX_MONTH].iloc[0]
        raise ContradictoryDateFormat(
            f"both layouts proven in one column: {n_first_gt12} rows prove day-first "
            f"(e.g. {ex_d!r}) and {n_second_gt12} prove month-first (e.g. {ex_m!r}) "
            f"of {n}. This column is two exports concatenated -- no single format is "
            "correct. Split by source and detect each part."
        )

    ts = _time_suffix(has_time, has_secs)
    dmy_fmt, mdy_fmt = DMY + ts, MDY + ts
    hint = _sortedness_hint(s, dmy_fmt, mdy_fmt)

    if not n_first_gt12 and not n_second_gt12:
        # Report the circumstantial hint so the caller has somewhere to start, but
        # still refuse. A hint is a lead to investigate, not a licence to parse.
        if hint.prefers_dayfirst is None:
            lead = ("The ordering cross-check cannot discriminate either "
                    f"(sorted_frac d/m/Y={hint.sorted_frac_dmy:.4f} vs "
                    f"m/d/Y={hint.sorted_frac_mdy:.4f} on {hint.n_subset} rows).")
        else:
            lead = (f"CIRCUMSTANTIAL ONLY -- not proof: sort order leans "
                    f"{'d/m/Y' if hint.prefers_dayfirst else 'm/d/Y'} "
                    f"(sorted_frac d/m/Y={hint.sorted_frac_dmy:.4f} vs "
                    f"m/d/Y={hint.sorted_frac_mdy:.4f} on {hint.n_subset} rows). "
                    "Corroborate it against a second source before acting.")
        raise AmbiguousDateFormat(
            f"all {n} rows have both leading fields <=12 "
            f"(max_first={int(first.max())}, max_second={int(second.max())}): "
            "d/m/Y and m/d/Y are both consistent with every row, so no proof "
            f"exists. Do NOT default. {lead} "
            "Resolve with a sibling file from the same export, a date-overlap test "
            "against another variable for the same station, or the station's known "
            "span -- then pass fmt= to parse_dates_safe explicitly. If unresolvable, "
            "exclude the file. See module docstring."
        )

    day_first = n_first_gt12 > 0
    fmt = dmy_fmt if day_first else mdy_fmt
    agrees = (None if hint.prefers_dayfirst is None
              else hint.prefers_dayfirst == day_first)
    if agrees is False:
        print(
            f"  WARNING dhime_dates: value-evidence proves "
            f"{'day-first' if day_first else 'month-first'} "
            f"({n_first_gt12} rows first>12, {n_second_gt12} rows second>12) but the "
            f"independent ordering check prefers the opposite "
            f"(sorted_frac d/m/Y={hint.sorted_frac_dmy:.4f} vs "
            f"m/d/Y={hint.sorted_frac_mdy:.4f} on {hint.n_subset} rows). "
            f"Value-evidence stands (a field >12 is proof; sort order is only a DHIME "
            f"convention) -- but this file is not a clean single export. Inspect it."
        )
    ev = DateEvidence(fmt, "dmy" if day_first else "mdy", n,
                      n_first_gt12, n_second_gt12,
                      int(first.max()), int(second.max()), has_time, hint, agrees)
    return ev if return_evidence else fmt


def parse_dates_safe(series: pd.Series, fmt: str) -> pd.Series:
    """
    Parse with an explicit format and assert nothing was silently lost.

    `fmt` must be given -- there is no inference path. Nulls in the input stay NaT
    (that is not a parse failure); any non-null value that fails to match `fmt`
    raises `DateParseError` with offending examples.
    """
    if not fmt or "%" not in fmt:
        raise ValueError(f"fmt must be an explicit strptime format, got {fmt!r}")
    was_null = series.isna() | (series.astype(str).str.strip() == "")
    out = pd.to_datetime(series, format=fmt, errors="coerce")
    bad = out.isna() & ~was_null
    n_bad = int(bad.sum())
    if n_bad:
        ex = series[bad].astype(str).head(5).tolist()
        raise DateParseError(
            f"{n_bad} of {int((~was_null).sum())} non-null values did not match "
            f"format {fmt!r}: {ex}"
        )
    return out


def parse_dhime_dates(series: pd.Series) -> tuple[pd.Series, DateEvidence]:
    """Detect then parse in one call. Returns (dates, evidence) or raises."""
    ev = detect_date_format(series, return_evidence=True)
    return parse_dates_safe(series, ev.fmt), ev


# ===========================================================================
# SMOKE TESTS -- synthetic series with known answers, run before real data
# ===========================================================================
def _iso(dates: list[str]) -> pd.Series:
    return pd.Series([f"{d} 00:00" for d in dates])


def test_iso() -> None:
    s = _iso(["1990-01-01", "1990-06-15", "2018-12-31"])
    ev = detect_date_format(s, return_evidence=True)
    assert ev.fmt == ISO_HM, ev.fmt
    assert ev.family == "iso"
    out = parse_dates_safe(s, ev.fmt)
    assert out.iloc[1] == pd.Timestamp("1990-06-15"), out.iloc[1]
    assert out.notna().all()
    print(f"  PASS iso            fmt={ev.fmt!r} n={ev.n_rows} -> {out.iloc[1].date()}")


def test_iso_no_time() -> None:
    s = pd.Series(["1990-01-01", "2004-08-06"])
    assert detect_date_format(s) == ISO
    assert parse_dates_safe(s, ISO).iloc[1] == pd.Timestamp("2004-08-06")
    print("  PASS iso_no_time    fmt='%Y-%m-%d'")


def test_dmy_with_day_gt12() -> None:
    """The load-bearing case: 06/08/2004 must become 6 August, NOT 8 June."""
    s = pd.Series(["06/08/2004 00:00", "13/08/2004 00:00", "31/12/2004 00:00"])
    ev = detect_date_format(s, return_evidence=True)
    assert ev.fmt == DMY_HM, ev.fmt
    assert ev.family == "dmy"
    assert ev.n_first_gt12 == 2 and ev.n_second_gt12 == 0, ev
    out = parse_dates_safe(s, ev.fmt)
    got = out.iloc[0]
    assert got == pd.Timestamp("2004-08-06"), f"expected 6 Aug, got {got}"
    assert got.month == 8 and got.day == 6
    print(f"  PASS dmy_day_gt12   fmt={ev.fmt!r} first>12={ev.n_first_gt12} "
          f"06/08/2004 -> {got.date()} (6 August)")


def test_mdy_with_second_gt12() -> None:
    s = pd.Series(["08/06/2004 00:00", "08/13/2004 00:00", "12/31/2004 00:00"])
    ev = detect_date_format(s, return_evidence=True)
    assert ev.fmt == MDY_HM, ev.fmt
    assert ev.family == "mdy"
    assert ev.n_second_gt12 == 2 and ev.n_first_gt12 == 0, ev
    out = parse_dates_safe(s, ev.fmt)
    assert out.iloc[0] == pd.Timestamp("2004-08-06"), out.iloc[0]
    print(f"  PASS mdy_2nd_gt12   fmt={ev.fmt!r} second>12={ev.n_second_gt12} "
          f"08/06/2004 -> {out.iloc[0].date()}")


def test_ambiguous_raises() -> None:
    s = pd.Series(["01/02/2004 00:00", "03/04/2004 00:00", "05/06/2004 00:00"])
    try:
        detect_date_format(s)
    except AmbiguousDateFormat as e:
        assert "no proof" in str(e)
        print(f"  PASS ambiguous      raised AmbiguousDateFormat ({len(s)} rows, "
              f"max_first=5 max_second=6)")
        return
    raise AssertionError("all-ambiguous series did NOT raise -- detector guessed")


def test_sort_hint_cannot_discriminate() -> None:
    """
    The hint must report NO PREFERENCE on the crafted 6th-12th-of-August series:
    both readings are perfectly ascending (Aug 6..12, or Jun 8/Jul 8/.../Dec 8).
    If it expressed a preference here it would be inventing evidence.
    """
    s = pd.Series([f"{d:02d}/08/2004 00:00" for d in range(6, 13)])
    h = _sortedness_hint(s, DMY_HM, MDY_HM)
    assert h.n_subset == 7, h
    assert h.sorted_frac_dmy == 1.0 and h.sorted_frac_mdy == 1.0, h
    assert h.prefers_dayfirst is None, h
    print(f"  PASS hint_no_disc   both readings sorted_frac=1.0 on n={h.n_subset} "
          f"-> prefers=None (refuses to invent evidence)")


def test_sort_hint_discriminates() -> None:
    """A day-first block whose ambiguous subset is out of order read month-first."""
    s = pd.Series([f"{d:02d}/{m:02d}/2004 00:00"
                   for m in (1, 2, 3) for d in (3, 7, 11)])   # all fields <=12
    h = _sortedness_hint(s, DMY_HM, MDY_HM)
    assert h.n_subset == 9, h
    assert h.prefers_dayfirst is True, h
    assert h.sorted_frac_dmy > h.sorted_frac_mdy + SORT_MARGIN, h
    # still raises: the hint informs, it does not decide
    try:
        detect_date_format(s)
        raise AssertionError("hint was allowed to decide -- it must not be")
    except AmbiguousDateFormat as e:
        assert "CIRCUMSTANTIAL ONLY" in str(e) and "d/m/Y" in str(e)
    print(f"  PASS hint_discrim   sorted_frac d/m/Y={h.sorted_frac_dmy:.4f} > "
          f"m/d/Y={h.sorted_frac_mdy:.4f} -> leans day-first, but STILL RAISED")


def test_contradictory_raises() -> None:
    s = pd.Series(["13/01/2004 00:00", "01/13/2004 00:00", "05/06/2004 00:00"])
    try:
        detect_date_format(s)
    except ContradictoryDateFormat as e:
        assert "both layouts proven" in str(e)
        print("  PASS contradictory  raised ContradictoryDateFormat (1 first>12, 1 second>12)")
        return
    raise AssertionError("contradictory series did NOT raise -- detector guessed")


def test_two_digit_year_raises() -> None:
    s = pd.Series(["01/02/04 00:00", "03/04/04 00:00"])
    try:
        detect_date_format(s)
    except UnrecognisedDateFormat as e:
        assert "2-digit years" in str(e)
        print("  PASS two_digit_year raised UnrecognisedDateFormat")
        return
    raise AssertionError("2-digit-year series did NOT raise")


def test_mixed_layout_raises() -> None:
    s = pd.Series(["1990-01-01 00:00", "01/01/1990 00:00"])
    try:
        detect_date_format(s)
    except UnrecognisedDateFormat as e:
        assert "mixed layouts" in str(e)
        print("  PASS mixed_layout   raised UnrecognisedDateFormat (1 year-first, 1 year-last)")
        return
    raise AssertionError("mixed-layout series did NOT raise")


def test_parse_dates_safe_rejects_mismatch() -> None:
    s = pd.Series(["1990-01-01 00:00", "not a date"])
    try:
        parse_dates_safe(s, ISO_HM)
    except DateParseError as e:
        assert "not a date" in str(e)
        print("  PASS safe_rejects   parse_dates_safe raised on 1 unmatched value")
        return
    raise AssertionError("parse_dates_safe silently coerced a bad value to NaT")


def test_parse_dates_safe_allows_nulls() -> None:
    s = pd.Series(["1990-01-01 00:00", None, ""])
    out = parse_dates_safe(s, ISO_HM)
    assert out.isna().sum() == 2 and out.iloc[0] == pd.Timestamp("1990-01-01")
    print("  PASS safe_nulls     2 genuine nulls -> NaT, no raise")


def test_naive_two_pass_transposes() -> None:
    """
    PROOF the rejected fix is unsafe. A real DD/MM series in which every day
    happens to be <=12 -- station sampled on the 6th-12th of each month, which is
    exactly what a manual sediment campaign looks like.
    """
    truth = [(6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8)]  # (day, month)
    s = pd.Series([f"{d:02d}/{m:02d}/2004 00:00" for d, m in truth])

    # --- the naive two-pass fix, verbatim ---
    naive = pd.to_datetime(s, errors="coerce")
    n_nat_pass1 = int(naive.isna().sum())
    naive = naive.fillna(pd.to_datetime(s, format=DMY_HM, errors="coerce"))

    assert n_nat_pass1 == 0, "pass 1 must succeed for the demo to be the dangerous case"
    wrong = [(t.day, t.month) for t in naive]
    assert wrong == [(m, d) for d, m in truth], wrong          # day and month swapped
    n_transposed = sum(1 for (d, m), t in zip(truth, naive) if (t.day, t.month) != (d, m))
    # 08/08 is self-symmetric under transposition, so it is silently CORRECT -- which
    # makes the corruption partial and therefore even harder to spot in a date histogram.
    n_symmetric = sum(1 for d, m in truth if d == m)
    assert n_transposed == len(truth) - n_symmetric == 6, (n_transposed, n_symmetric)

    # --- this module, same input ---
    try:
        detect_date_format(s)
        raise AssertionError("detector guessed on the crafted ambiguous series")
    except AmbiguousDateFormat:
        pass

    print(f"  PASS naive_unsafe   naive pass-1 NaT={n_nat_pass1} (rescue never fires), "
          f"{n_transposed}/{len(truth)} dates transposed "
          f"({n_symmetric} self-symmetric row stayed correct by chance):")
    print(f"      raw {s.iloc[0]} -> naive {naive.iloc[0].date()} "
          f"(8 June) but truth is 2004-08-06 (6 August)")
    print(f"      raw {s.iloc[6]} -> naive {naive.iloc[6].date()} "
          f"(8 December) but truth is 2004-08-12 (12 August)")
    print(f"      naive dates: {[str(t.date()) for t in naive]}")
    print(f"      truth      : {[f'2004-{m:02d}-{d:02d}' for d, m in truth]}")
    print("      -> detect_date_format raised AmbiguousDateFormat on the same input")
    return naive, truth


def test_naive_two_pass_month_gt12_case() -> None:
    """
    The mirror hazard, and why src/build_discharge_gauges.py:149-152 is also exposed:
    ISO-format-first-then-infer. On a DD/MM file the ISO pass yields all-NaT and the
    inference fallback decides the layout by luck, exactly as above.
    """
    s = pd.Series(["06/08/2004 00:00", "07/08/2004 00:00"])
    iso_pass = pd.to_datetime(s, format=ISO_HM, errors="coerce")
    assert iso_pass.isna().all()
    fallback = pd.to_datetime(s, errors="coerce")
    got = [(t.day, t.month) for t in fallback]
    assert got == [(8, 6), (8, 7)], got
    print("  PASS naive_mirror   ISO-first pass gives 2/2 NaT; inference fallback "
          "returns 8 June / 8 July for 06/08 & 07/08 (transposed)")


def run_smoke_tests() -> None:
    print("SMOKE TESTS (synthetic, known answers)")
    test_iso()
    test_iso_no_time()
    test_dmy_with_day_gt12()
    test_mdy_with_second_gt12()
    test_ambiguous_raises()
    test_sort_hint_cannot_discriminate()
    test_sort_hint_discriminates()
    test_contradictory_raises()
    test_two_digit_year_raises()
    test_mixed_layout_raises()
    test_parse_dates_safe_rejects_mismatch()
    test_parse_dates_safe_allows_nulls()
    test_naive_two_pass_transposes()
    test_naive_two_pass_month_gt12_case()
    print("all smoke tests passed")


if __name__ == "__main__":
    run_smoke_tests()
