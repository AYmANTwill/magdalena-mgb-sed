"""Pytest port of the load-bearing smoke tests in src/dhime_dates.py.

The module ships 14 smoke tests runnable via `python src/dhime_dates.py`; these are
the CI-facing subset: unambiguous parses, day>12 disambiguation, and the refusals
(ambiguous / contradictory input must RAISE, never guess).
"""
import pandas as pd
import pytest

from dhime_dates import (
    DMY_HM,
    ISO_HM,
    MDY_HM,
    AmbiguousDateFormat,
    ContradictoryDateFormat,
    DateParseError,
    detect_date_format,
    parse_dates_safe,
)


def test_iso_unambiguous_parse():
    s = pd.Series(["1990-01-01 00:00", "1990-06-15 00:00", "2018-12-31 00:00"])
    ev = detect_date_format(s, return_evidence=True)
    assert ev.fmt == ISO_HM
    assert ev.family == "iso"
    out = parse_dates_safe(s, ev.fmt)
    assert out.iloc[1] == pd.Timestamp("1990-06-15")
    assert out.notna().all()


def test_day_gt12_proves_dayfirst():
    """The load-bearing case: 06/08/2004 must become 6 August, NOT 8 June."""
    s = pd.Series(["06/08/2004 00:00", "13/08/2004 00:00", "31/12/2004 00:00"])
    ev = detect_date_format(s, return_evidence=True)
    assert ev.fmt == DMY_HM
    assert ev.family == "dmy"
    assert ev.n_first_gt12 == 2 and ev.n_second_gt12 == 0
    got = parse_dates_safe(s, ev.fmt).iloc[0]
    assert got == pd.Timestamp("2004-08-06")
    assert (got.day, got.month) == (6, 8)


def test_second_gt12_proves_monthfirst():
    s = pd.Series(["08/06/2004 00:00", "08/13/2004 00:00", "12/31/2004 00:00"])
    ev = detect_date_format(s, return_evidence=True)
    assert ev.fmt == MDY_HM
    assert ev.family == "mdy"
    assert parse_dates_safe(s, ev.fmt).iloc[0] == pd.Timestamp("2004-08-06")


def test_ambiguous_raises_instead_of_guessing():
    """Every field <=12: no evidence exists, so the detector must refuse."""
    s = pd.Series(["01/02/2004 00:00", "03/04/2004 00:00", "05/06/2004 00:00"])
    with pytest.raises(AmbiguousDateFormat, match="no proof"):
        detect_date_format(s)


def test_contradictory_raises():
    """Day-first AND month-first proofs in one column: two exports concatenated."""
    s = pd.Series(["13/01/2004 00:00", "01/13/2004 00:00", "05/06/2004 00:00"])
    with pytest.raises(ContradictoryDateFormat, match="both layouts proven"):
        detect_date_format(s)


def test_parse_dates_safe_rejects_unmatched_value():
    s = pd.Series(["1990-01-01 00:00", "not a date"])
    with pytest.raises(DateParseError, match="not a date"):
        parse_dates_safe(s, ISO_HM)


def test_parse_dates_safe_keeps_genuine_nulls():
    s = pd.Series(["1990-01-01 00:00", None, ""])
    out = parse_dates_safe(s, ISO_HM)
    assert out.isna().sum() == 2
    assert out.iloc[0] == pd.Timestamp("1990-01-01")
