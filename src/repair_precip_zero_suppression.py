"""
Repair zero-suppressed rain-gauge series in the QC'd DHIME dataset.

THE BUG
-------
Some DHIME station series contain only *rain* days - the dry days were never exported.
Annual totals then reach 9,000-12,000 mm/yr in regions that receive ~2,000-2,500.

Why `build_precip_gauges.py` could not catch it: that step screens outlier *values*
(0-400 mm/day). Every individual reading in a zero-suppressed series is plausible. The
defect is in the *absent* records, which no value-based filter can see.

Why it corrupts the forcing: in IDW interpolation a gauge contributes only on days it
reported. A zero-suppressed gauge therefore joins the weighted average exactly when it
is raining there and is masked out when it is dry, so it can only ever pull the estimate
up - producing persistent wet "bullseyes" centred on those stations.

DETECTION - two complementary tests, either of which flags a station
-------------------------------------------------------------------
1. **Dry-day fraction.** Healthy gauges here are dry (<= 0.1 mm) on ~45 % of their
   records. Below 15 % means rain days only.

2. **Neighbour ratio.** Station annual total divided by the median annual total of its
   6 nearest neighbours. The healthy population sits at 1.01; offenders reach 2.5-3.2.

Neither test alone is sufficient, which is why both are used:

- The dry-fraction test misses stations that keep *some* zeros. SAN LUIS 21130040 has a
  perfectly normal dry fraction of 0.40 yet is 2.5x wetter than every neighbour.
- The neighbour test would fail if a whole *region* were suppressed together, since every
  ratio in that neighbourhood would be ~1. The dry-fraction test still catches that case.

Both are additionally gated on `span_frac < 0.85` (the station must actually be missing
days inside its own active period), so a dense, genuinely wet gauge is never touched.

THE REPAIR
----------
For flagged stations every missing calendar day inside the station's own active span is
inserted as 0.0 mm and marked `Inferido_seco` — with one exception (see below). Nothing
is invented outside the span, and healthy stations are untouched.

**Station outages must not be infilled as dry.** A gap of a single missed day is
consistent with "reports rain, omits dry" — the pattern this repair targets. A gap of
many *months* is not: it means the station reported nothing at all, wet or dry, and
treating that as "dry" fabricates a drought. ALGECIRAS 21105030 is the clean example:
raw records show three genuine outages (2012-05..2013-12, 2015-07..2017-12,
2018-01..2018-08 — 20, 30 and 8 months of zero raw reports), and the first version of
this repair filled all of them with 0.0, injecting an artificial multi-year drought into
exactly the years the model calibrates on. `SILENCE_GAP_DAYS` draws the line: raw-missing
runs at or above it are left absent (not infilled); shorter runs are infilled as before.

Validation is built in: the repair must move a flagged station's annual total into a
plausible range *and* bring its neighbour ratio down. Stations that stay anomalous are
reported rather than silently accepted - for those the gaps are genuinely missing data,
not dry days.

Outputs (data/processed/):
    precip_gauges_daily_qc.csv          repaired daily series
    precip_gauges_inventory_qc.csv      inventory + diagnostics
    precip_zero_suppression_report.csv  per-station before/after

Run:  python src/repair_precip_zero_suppression.py
"""
from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

REPO = pathlib.Path(__file__).resolve().parents[1]
PROC = REPO / "data" / "processed"

DRY_MM = 0.1           # at or below this counts as a dry day
DRY_FRAC_MIN = 0.15    # healthy gauges are dry on ~45 % of days
RATIO_MAX = 1.8        # healthy population sits at ~1.0; offenders reach 2.5-3.2
SPAN_FRAC_MAX = 0.85   # a suppressed series is also missing days inside its own span
N_NEIGHBOURS = 6
PLAUSIBLE_MM = (400.0, 7000.0)
SILENCE_GAP_DAYS = 60  # raw-missing runs this long or longer are a station outage, not
                       # an omitted dry day; those days are left absent, never infilled


def haversine_km(la1, lo1, la2, lo2):
    return np.sqrt(((la1-la2)*111.0)**2
                   + ((lo1-lo2)*111.0*np.cos(np.radians((la1+la2)/2)))**2)


def diagnose(daily: pd.DataFrame, inv: pd.DataFrame) -> pd.DataFrame:
    """Per-station diagnostics deciding which series are zero-suppressed."""
    out = daily.groupby("code").agg(
        n_rec=("precip_mm", "size"),
        dry_frac=("precip_mm", lambda s: (s <= DRY_MM).mean()),
        median_mm=("precip_mm", "median"),
        mean_mm=("precip_mm", "mean"),
        first=("date", "min"),
        last=("date", "max"))
    out["span_days"] = (out["last"] - out["first"]).dt.days + 1
    out["span_frac"] = out.n_rec / out.span_days
    out["ann_before"] = out.mean_mm * 365.25
    # annual total if the absent days inside the span are dry
    out["ann_after"] = out.mean_mm * out.span_frac * 365.25

    coords = inv.dropna(subset=["lat", "lon"]).set_index("code")[["lat", "lon"]]
    out = out.join(coords, how="left")
    known = out.dropna(subset=["lat", "lon"])
    dist = haversine_km(known.lat.values[:, None], known.lon.values[:, None],
                        known.lat.values[None, :], known.lon.values[None, :])
    np.fill_diagonal(dist, np.inf)
    nb = np.argsort(dist, axis=1)[:, :N_NEIGHBOURS]
    out["nbr_ann"] = np.nan
    out.loc[known.index, "nbr_ann"] = np.median(known.ann_before.values[nb], axis=1)
    out["ratio"] = out.ann_before / out.nbr_ann
    out.loc[known.index, "nbr_ann_after"] = np.median(known.ann_after.values[nb], axis=1)
    out["ratio_after"] = out.ann_after / out.nbr_ann_after

    anomalous = (out.dry_frac < DRY_FRAC_MIN) | (out.ratio.fillna(0) > RATIO_MAX)
    out["zero_suppressed"] = anomalous & (out.span_frac < SPAN_FRAC_MAX)
    out["why"] = np.where(out.dry_frac < DRY_FRAC_MIN,
                          np.where(out.ratio.fillna(0) > RATIO_MAX, "both", "dry_frac"),
                          np.where(out.ratio.fillna(0) > RATIO_MAX, "neighbour", ""))
    out.loc[~out.zero_suppressed, "why"] = ""
    return out


def _missing_runs(all_days: pd.DatetimeIndex, have: set) -> list[np.ndarray]:
    """Contiguous runs of days in `all_days` absent from `have`."""
    missing_mask = np.array([d not in have for d in all_days])
    runs, start = [], None
    for i, is_missing in enumerate(missing_mask):
        if is_missing and start is None:
            start = i
        elif not is_missing and start is not None:
            runs.append(all_days[start:i])
            start = None
    if start is not None:
        runs.append(all_days[start:])
    return runs


def repair(daily: pd.DataFrame, diag: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Insert dry days inside the active span of every flagged station.

    Raw-missing runs shorter than SILENCE_GAP_DAYS are infilled as dry (the pattern this
    repair targets). Runs at or above it are a station outage and are left absent.
    """
    added: dict[str, int] = {}
    excluded: dict[str, int] = {}
    new_rows = []
    for code in diag.index[diag.zero_suppressed]:
        row = diag.loc[code]
        have = set(daily.loc[daily.code == code, "date"])
        all_days = pd.date_range(row["first"], row["last"], freq="D")
        runs = _missing_runs(all_days, have)

        fill_days, outage_days = [], 0
        for run in runs:
            if len(run) >= SILENCE_GAP_DAYS:
                outage_days += len(run)
            else:
                fill_days.extend(run)

        added[code] = len(fill_days)
        excluded[code] = outage_days
        if fill_days:
            new_rows.append(pd.DataFrame({"code": code, "date": fill_days,
                                          "precip_mm": 0.0, "approval": "Inferido_seco"}))
    if new_rows:
        daily = pd.concat([daily] + new_rows, ignore_index=True)
    fixed = daily.sort_values(["code", "date"]).reset_index(drop=True)
    return fixed, pd.Series(added, dtype="int64"), pd.Series(excluded, dtype="int64")


def main() -> None:
    daily = pd.read_csv(PROC / "precip_gauges_daily.csv", dtype={"code": str})
    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.dropna(subset=["precip_mm"])
    inv = pd.read_csv(PROC / "precip_gauges_inventory.csv", dtype={"code": str})

    diag = diagnose(daily, inv)
    f = diag.zero_suppressed
    print(f"stations                 : {len(diag)}")
    print(f"zero-suppressed (flagged): {int(f.sum())} ({100*f.mean():.0f} % of network, "
          f"{int(diag.loc[f, 'n_rec'].sum()):,} station-days)")
    print("  caught by: " + ", ".join(f"{k} {v}" for k, v in
                                      diag.loc[f, "why"].value_counts().items()))
    print(f"  dry-day fraction : flagged {diag.loc[f,'dry_frac'].median():.2f} "
          f"vs healthy {diag.loc[~f,'dry_frac'].median():.2f}")
    print(f"  neighbour ratio  : flagged {diag.loc[f,'ratio'].median():.2f} "
          f"vs healthy {diag.loc[~f,'ratio'].median():.2f}")
    print(f"  annual mm/yr     : flagged {diag.loc[f,'ann_before'].median():.0f} -> "
          f"{diag.loc[f,'ann_after'].median():.0f}  (healthy {diag.loc[~f,'ann_before'].median():.0f})")

    fixed, added, excluded = repair(daily, diag)
    n_outage_stations = int((excluded > 0).sum())
    if n_outage_stations:
        print(f"\n  station outages found (>= {SILENCE_GAP_DAYS} d raw-missing, left absent, "
              f"not infilled): {n_outage_stations} stations, {int(excluded.sum()):,} days total")
        for c, d in excluded[excluded > 0].sort_values(ascending=False).items():
            print(f"    {c}  {d:,} days excluded from infill")

    post = fixed.groupby("code").precip_mm.mean()*365.25
    bad = [c for c in diag.index[f]
           if not (PLAUSIBLE_MM[0] <= post[c] <= PLAUSIBLE_MM[1])]
    still = diag.index[f & (diag.ratio_after > RATIO_MAX)].tolist()
    print(f"\n  after repair: neighbour ratio {diag.loc[f,'ratio_after'].median():.2f} "
          f"(was {diag.loc[f,'ratio'].median():.2f})")
    if bad:
        print(f"  WARNING {len(bad)} stations still outside a plausible annual range: {bad}")
    if still:
        print(f"  NOTE {len(still)} stations remain >{RATIO_MAX}x their neighbours after repair "
              f"- their gaps may be missing data rather than dry days:")
        for c in still:
            print(f"    {c}  {post[c]:.0f} mm/yr  ratio {diag.loc[c,'ratio_after']:.1f}")
    if not bad and not still:
        print("  all flagged stations are plausible and consistent with neighbours after repair")

    keep = ["dry_frac", "span_frac", "ratio", "ratio_after", "zero_suppressed",
            "ann_before", "ann_after", "why"]
    inv2 = inv.merge(diag[keep], left_on="code", right_index=True, how="left")
    inv2["n_infilled"] = inv2.code.map(added).fillna(0).astype(int)
    inv2["n_outage_days"] = inv2.code.map(excluded).fillna(0).astype(int)
    inv2["ann_mean_mm"] = inv2.code.map(post)
    inv2["n_valid"] = inv2.code.map(fixed.groupby("code").size())

    fixed.to_csv(PROC / "precip_gauges_daily_qc.csv", index=False,
                 date_format="%Y-%m-%d", float_format="%.2f")
    inv2.to_csv(PROC / "precip_gauges_inventory_qc.csv", index=False)
    diag.to_csv(PROC / "precip_zero_suppression_report.csv")

    print(f"\nwrote precip_gauges_daily_qc.csv       {len(fixed):,} rows "
          f"(+{int(added.sum()):,} inferred dry days)")
    print(f"wrote precip_gauges_inventory_qc.csv  {len(inv2)} stations")
    print("wrote precip_zero_suppression_report.csv")
    before = daily.groupby("code").precip_mm.mean().mean()*365.25
    print(f"\ngauge-mean annual total: {before:.0f} -> {post.mean():.0f} mm/yr")


if __name__ == "__main__":
    main()
