"""Round-trip and truncation defence of src/forcing_npy.py.

The converter exists because pd.read_csv silently returned a plausible PREFIX of a
complete 180 MB forcing CSV. Its checks compare the parsed frame against the file's
own raw bytes, so (a) a genuinely truncated file must raise, and (b) a parser that
lies about the row count must be caught by the row-count-vs-raw-bytes assertion.
"""
import numpy as np
import pandas as pd
import pytest

import forcing_npy

IDS = (101, 102, 103)
N_DAYS = 10


def _write_frame(path):
    dates = pd.date_range("2020-01-01", periods=N_DAYS, freq="D")
    rng = np.random.default_rng(11)
    df = pd.DataFrame(
        rng.gamma(1.0, 5.0, (N_DAYS, len(IDS))).round(3),
        index=dates.strftime("%Y-%m-%d"),
        columns=[str(i) for i in IDS],
    )
    df.to_csv(path)
    return df


def test_line_and_field_count(tmp_path):
    src = tmp_path / "forcing_minibacia_precip_test.csv"
    _write_frame(src)
    assert forcing_npy.line_and_field_count(src) == (N_DAYS, len(IDS))


def test_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(forcing_npy, "PROC", tmp_path)
    src = tmp_path / "forcing_minibacia_precip_test.csv"
    df = _write_frame(src)
    forcing_npy.convert("precip", "test")
    V = np.load(tmp_path / "forcing_precip_test.npy")
    D = np.load(tmp_path / "forcing_precip_test_dates.npy")
    ids = np.load(tmp_path / "forcing_precip_test_ids.npy")
    assert V.shape == (N_DAYS, len(IDS)) and V.dtype == np.float32
    np.testing.assert_array_equal(V, df.to_numpy(dtype="float32"))
    assert ids.tolist() == list(IDS)
    assert str(D[0]) == "2020-01-01" and str(D[-1]) == "2020-01-10"


def test_truncated_file_raises(tmp_path, monkeypatch):
    """A copy cut mid-row must RAISE, never convert to a plausible subset."""
    monkeypatch.setattr(forcing_npy, "PROC", tmp_path)
    src = tmp_path / "forcing_minibacia_precip_trunc.csv"
    _write_frame(src)
    raw = src.read_bytes()
    # cut right after the last row's date field: the row loses its value fields
    cut = raw.rfind(b"2020-01-10,") + len(b"2020-01-10,")
    src.write_bytes(raw[:cut])
    with pytest.raises(AssertionError):
        forcing_npy.convert("precip", "trunc")


def test_parser_truncation_is_caught(tmp_path, monkeypatch):
    """Simulate the original defect: the parser returns a silent PREFIX of a
    complete file. The row-count-vs-raw-bytes check must catch it."""
    monkeypatch.setattr(forcing_npy, "PROC", tmp_path)
    monkeypatch.setattr(forcing_npy, "CHUNK", 4)          # 10 rows -> 3 chunks
    src = tmp_path / "forcing_minibacia_precip_lie.csv"
    _write_frame(src)

    real_read_csv = pd.read_csv

    def lying_read_csv(path, **kw):
        chunks = list(real_read_csv(path, **kw))
        return iter(chunks[:-1])                          # drop the last chunk

    monkeypatch.setattr(forcing_npy.pd, "read_csv", lying_read_csv)
    with pytest.raises(AssertionError, match="truncated"):
        forcing_npy.convert("precip", "lie")
