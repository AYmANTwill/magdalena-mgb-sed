"""Phase B - finish the zero-suppression repair, using SELECTIVITY as the detector.

WHY A SECOND DETECTOR
---------------------
`repair_precip_zero_suppression.py` gates on

    anomalous = (dry_frac < 0.15) | (ratio > 1.8);  flag = anomalous & (span_frac < 0.85)

and it works on what it catches: docs/18 s9.3 measured the 70 stations it repaired as
behaving like fair reporters afterwards (dense-band selectivity held at ~1.00 while that
band grew from 92 to 151 stations). But it is incomplete in COVERAGE - 139 of 294 stations
still report rain-selectively and still feed the IDW.

Both existing tests are uncontrolled statistics of the station's OWN series:

  * `dry_frac` confounds suppression with climate. A genuinely wet station in the Chocó
    flank has a low dry fraction because it rains there, not because zeros were dropped.
  * `ratio` (station annual total / neighbour median annual total) confounds suppression
    with orography. A ridge station legitimately reports 2x its valley neighbours.

Both therefore need a loose threshold to avoid firing on healthy wet stations, and a loose
threshold is what left 139 stations unrepaired.

THE STATISTIC USED HERE
-----------------------
    selectivity(S) = mean(D | days S reports) / mean(D | all days)

for D = the nearest dense, unflagged neighbours of S. It is computed ENTIRELY FROM THE
NEIGHBOUR'S DATA. S's own values never enter, so how wet S is cannot influence it.

If S reports on a fair sample of days, those days are a random draw and the neighbour's
mean over them equals its mean over all days: selectivity = 1. If S reports preferentially
when it rains, then D - a different instrument, in a different place - is also wetter on
those days, because daily rainfall is regionally correlated. Values above 1 are positive
evidence of rain-day-selective reporting that no siting or climate argument explains.

That is what makes it usable as a DETECTOR rather than only a validator, and it is why the
threshold can be set from data instead of chosen: the statistic has a known null. On the
dense, unflagged population it must read 1.00, and it does (docs/18 s9.2 measured 1.001
over 89 stations). The threshold here is the upper tail of that measured null, so the
false-positive rate is calibrated rather than assumed.

WHAT IT CANNOT DO
-----------------
Selectivity says a station reports selectively; it does not create days to fill. Inserting
dry days needs absent days inside the active span, so the flag is still gated on
`span_frac < 0.85`. Stations that are selective AND essentially complete cannot be repaired
by infilling and are reported separately as candidates for exclusion or down-weighting -
they are a different defect (values wrong on days that ARE reported).

Outputs, written ALONGSIDE the v1 products so both remain available for attribution:

    precip_gauges_daily_qc_v2.csv        long: code, date, precip_mm, approval
    precip_selectivity_report.csv        per station: selectivity before/after, flags, why

Run:  python src/repair_precip_selectivity.py
"""
from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

from repair_precip_zero_suppression import (
    SPAN_FRAC_MAX,
    diagnose,
    haversine_km,
    repair,
)

REPO = pathlib.Path(__file__).resolve().parents[1]
PROC = REPO / "data" / "processed"

DENSE_MIN = 0.90        # a station reporting >=90 % of its span is a usable reference
MAX_NB_KM = 60.0        # beyond this, daily rainfall is too decorrelated to be a reference
N_NB = 5
MIN_DAYS_S = 200        # days S must report for its selectivity to mean anything
MIN_DAYS_D = 150        # overlap days needed from a neighbour
NULL_QUANTILE = 0.99    # threshold = this quantile of the dense-unflagged null
MIN_OVERLAP_ALL = 300


def _pivot(daily: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
    W = daily.pivot_table(index="date", columns="code", values="precip_mm", aggfunc="first")
    W = W.reindex(pd.date_range(daily.date.min(), daily.date.max(), freq="D"))
    return W, W.to_numpy(float)


def selectivity(daily: pd.DataFrame, inv: pd.DataFrame, ref_codes: list[str]) -> pd.Series:
    """selectivity(S) for every station, referenced to `ref_codes` only.

    `ref_codes` is passed in rather than derived so that the reference pool can be held
    FIXED across a before/after comparison. Recomputing it on the repaired file would let
    repaired stations enter the pool and change the yardstick mid-measurement.
    """
    W, V = _pivot(daily)
    codes = list(W.columns)
    pos = {c: i for i, c in enumerate(codes)}
    rep = np.isfinite(V)
    meta = inv.set_index("code")
    lat = meta.lat.reindex(codes).to_numpy(float)
    lon = meta.lon.reindex(codes).to_numpy(float)
    D = haversine_km(lat[:, None], lon[None, :], lat[None, :], lon[:, None])
    np.fill_diagonal(D, np.inf)
    ref_idx = np.array([pos[c] for c in ref_codes if c in pos], dtype=int)

    out = {}
    for i, c in enumerate(codes):
        if not np.isfinite(lat[i]):
            continue
        sel = rep[:, i]
        if sel.sum() < MIN_DAYS_S:
            continue
        cand = ref_idx[(ref_idx != i) & (D[i, ref_idx] <= MAX_NB_KM)]
        if cand.size == 0:
            continue
        cand = cand[np.argsort(D[i, cand])][:N_NB]
        num, den = [], []
        for j in cand:
            vj = V[:, j]
            fin = np.isfinite(vj)
            on = vj[sel & fin]
            allv = vj[fin]
            if len(on) < MIN_DAYS_D or len(allv) < MIN_OVERLAP_ALL or allv.mean() <= 0:
                continue
            num.append(on.mean())
            den.append(allv.mean())
        if num:
            out[c] = float(np.mean(num) / np.mean(den))
    return pd.Series(out, name="selectivity")


def band_table(sel: pd.Series, dens: pd.Series, label: str) -> pd.DataFrame:
    rows = []
    for lo, hi, nm in [(DENSE_MIN, 1.01, "reports >90%"), (0.50, DENSE_MIN, "reports 50-90%"),
                       (0.00, 0.50, "reports <50%")]:
        k = dens[(dens >= lo) & (dens < hi)].index.intersection(sel.index)
        rows.append(dict(band=nm, n=len(k),
                         selectivity=sel.reindex(k).median() if len(k) else np.nan))
    T = pd.DataFrame(rows).set_index("band")
    print(f"\n  {label}")
    print("    " + T.round(3).to_string().replace("\n", "\n    "))
    return T


def main() -> None:
    daily = pd.read_csv(PROC / "precip_gauges_daily.csv", dtype={"code": str})
    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.dropna(subset=["precip_mm"])
    inv = pd.read_csv(PROC / "precip_gauges_inventory.csv", dtype={"code": str})

    diag = diagnose(daily, inv)
    dens_pre = (diag.span_frac).clip(upper=1.0)
    v1_flag = diag.zero_suppressed.copy()
    print(f"stations {len(diag)} | v1 detector flags {int(v1_flag.sum())}")

    # Reference pool: dense AND not flagged by v1. Held FIXED for every measurement below.
    ref = sorted(diag.index[(dens_pre >= DENSE_MIN) & ~v1_flag])
    print(f"reference pool (dense >={DENSE_MIN:.2f} and unflagged): {len(ref)} stations")

    print("\n" + "=" * 78)
    print("B1  CALIBRATE THE THRESHOLD FROM THE NULL")
    print("=" * 78)
    sel_pre = selectivity(daily, inv, ref)
    print(f"selectivity computed for {len(sel_pre)} of {len(diag)} stations")
    null = sel_pre.reindex(ref).dropna()
    mad = float(np.median(np.abs(null - null.median())))
    robust3 = float(null.median() + 3 * 1.4826 * mad)
    q = float(null.quantile(NULL_QUANTILE))
    THRESH = max(q, robust3)
    print(f"\nnull on the {len(null)} reference stations (must read ~1.00):")
    print(f"  median {null.median():.4f} | p90 {null.quantile(.90):.4f} | "
          f"p95 {null.quantile(.95):.4f} | p99 {q:.4f} | max {null.max():.4f}")
    print(f"  robust 3-sigma (median + 3*1.4826*MAD) = {robust3:.4f}")
    print(f"  THRESHOLD = max(p{NULL_QUANTILE*100:.0f}, robust3) = {THRESH:.4f}")
    print("  (set from the measured null, not chosen; the false-positive rate on healthy")
    print("   dense stations is therefore calibrated rather than assumed)")

    print("\n" + "=" * 78)
    print("B2  FLAG AND REPAIR")
    print("=" * 78)
    is_sel = sel_pre.reindex(diag.index) > THRESH
    repairable = dens_pre < SPAN_FRAC_MAX
    new_flag = is_sel & repairable & ~v1_flag
    stuck = is_sel & ~repairable
    print(f"selective (> {THRESH:.3f})            : {int(is_sel.sum())}")
    print(f"  already caught by v1              : {int((is_sel & v1_flag).sum())}")
    print(f"  NEW, repairable (span_frac<{SPAN_FRAC_MAX}) : {int(new_flag.sum())}")
    print(f"  selective but ~complete           : {int(stuck.sum())}  <- cannot be fixed by")
    print("                                         infilling; exclude or down-weight")

    diag2 = diag.copy()
    diag2["zero_suppressed"] = v1_flag | new_flag
    print(f"\nv1 flags {int(v1_flag.sum())} -> v2 flags {int(diag2.zero_suppressed.sum())}")

    fixed, added, excluded = repair(daily, diag2)
    n_ins = int(added.sum())
    print(f"inserted {n_ins:,} inferred-dry station-days across "
          f"{int((added > 0).sum())} stations")
    print(f"  left absent as station outages (>=60 d runs): {int(excluded.sum()):,} days")
    print(f"corpus {len(daily):,} -> {len(fixed):,} station-days")

    print("\n" + "=" * 78)
    print("B3  DID IT WORK?  selectivity re-measured against the SAME reference pool")
    print("=" * 78)
    sel_post = selectivity(fixed, inv, ref)
    print("\nFIXED bands (density from the PRE-repair file) - the apples-to-apples view:")
    band_table(sel_pre, dens_pre, "before")
    band_table(sel_post, dens_pre, "after")

    d2 = diagnose(fixed, inv)
    dens_post = d2.span_frac.clip(upper=1.0)
    print("\nRECOMPUTED bands (density from the POST-repair file) - comparable to "
          "docs/18 s9.2,\nbut confounded by stations changing band:")
    band_table(sel_post, dens_post, "after, recomputed bands")

    out = pd.DataFrame({
        "selectivity_pre": sel_pre, "selectivity_post": sel_post,
        "span_frac_pre": dens_pre, "span_frac_post": dens_post,
        "dry_frac_pre": diag.dry_frac, "ratio_pre": diag.ratio,
        "flag_v1": v1_flag, "flag_new_selectivity": new_flag.fillna(False),
        "selective_but_complete": stuck.fillna(False),
        "days_inserted": added.reindex(diag.index).fillna(0).astype(int),
        "outage_days_left_absent": excluded.reindex(diag.index).fillna(0).astype(int),
    })
    out.index.name = "code"
    out.to_csv(PROC / "precip_selectivity_report.csv")
    fixed.to_csv(PROC / "precip_gauges_daily_qc_v2.csv", index=False)
    print(f"\nwrote {PROC / 'precip_gauges_daily_qc_v2.csv'}")
    print(f"wrote {PROC / 'precip_selectivity_report.csv'}")

    print("\n" + "=" * 78)
    print("SUCCESS CRITERIA")
    print("=" * 78)
    sp = band_table(sel_post, dens_pre, "final, fixed bands").selectivity
    sparse = sp.loc["reports <50%"]
    dense = sp.loc["reports >90%"]
    ok1 = sparse < 1.15
    ok2 = abs(dense - 1.0) < 0.05
    print(f"\n  sparse-band selectivity < 1.15   : {sparse:.3f}  "
          f"{'PASS' if ok1 else 'FAIL'}   (was 1.734 in s9.3)")
    print(f"  dense-band selectivity ~ 1.00    : {dense:.3f}  "
          f"{'PASS' if ok2 else 'FAIL'}   (over-repair guard)")
    print(f"  station-days inserted            : {n_ins:,} on {int((added > 0).sum())} stations")


if __name__ == "__main__":
    main()
