"""
Repair zero-suppressed rain-gauge series in the QC'd DHIME dataset.

THE BUG
-------
Some DHIME station series contain only *rain* days - the dry days were never
exported. Their median daily value is ~20 mm where a healthy gauge sits at ~0.8 mm,
and their naive annual totals reach 9,000-12,000 mm/yr in regions that receive
~2,000-2,500 mm/yr.

Why `build_precip_gauges.py` could not catch it: that step screens outlier *values*
(0-400 mm/day). Every individual value in a zero-suppressed series is perfectly
plausible. The defect is in the *absent* records, which no value-based filter sees.

Why it corrupts the forcing: in the IDW interpolation a gauge contributes only on days
it reported. A zero-suppressed gauge therefore joins the weighted average exactly when
it is raining there and is masked out when it is dry, so it can only ever pull the
estimate up. The result is a persistent wet bias centred on that station - the circular
"bullseyes" visible in the notebook 11 mean-annual rainfall map.

THE TEST
--------
Fraction of a station's *recorded* days that are dry (<= 0.1 mm). In this basin a healthy
gauge is dry on roughly 40-70 % of days. A station dry on <15 % of its records is
reporting rain days only.

THE REPAIR
----------
For flagged stations, every missing calendar day inside the station's own active span
(first..last observation) is inserted as 0.0 mm and marked `Inferido_seco`. Nothing is
invented outside that span, and healthy stations are untouched.

Validation built in: the repair must move a flagged station's annual total into a
plausible range. Stations that remain implausible afterwards are reported, not silently
accepted - for those the gaps are genuinely missing data rather than dry days.

Outputs (data/processed/):
    precip_gauges_daily_qc.csv          repaired daily series
    precip_gauges_inventory_qc.csv      inventory + dry_frac, zero_suppressed, n_infilled
    precip_zero_suppression_report.csv  per-station before/after

Run:  python src/repair_precip_zero_suppression.py
"""
from __future__ import annotations

import pathlib

import pandas as pd

REPO = pathlib.Path(__file__).resolve().parents[1]
PROC = REPO / "data" / "processed"

DRY_MM = 0.1          # at or below this counts as a dry day
DRY_FRAC_MIN = 0.15   # healthy gauges are dry on 40-70 % of days; <15 % means suppressed
SPAN_FRAC_MAX = 0.85  # a suppressed series also has many absent days
PLAUSIBLE_MM = (400.0, 7000.0)   # annual totals expected anywhere in the basin


def diagnose(daily: pd.DataFrame) -> pd.DataFrame:
    """Per-station diagnostics used to decide which series are zero-suppressed."""
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
    out["zero_suppressed"] = (out.dry_frac < DRY_FRAC_MIN) & (out.span_frac < SPAN_FRAC_MAX)
    # what the annual total becomes if the absent days inside the span are dry
    out["ann_after"] = out.mean_mm * out.span_frac * 365.25
    return out


def repair(daily: pd.DataFrame, diag: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Insert dry days inside the active span of every flagged station."""
    added: dict[str, int] = {}
    new_rows = []
    for code in diag.index[diag.zero_suppressed]:
        row = diag.loc[code]
        have = set(daily.loc[daily.code == code, "date"])
        missing = [d for d in pd.date_range(row["first"], row["last"], freq="D")
                   if d not in have]
        added[code] = len(missing)
        if missing:
            new_rows.append(pd.DataFrame({"code": code, "date": missing,
                                          "precip_mm": 0.0, "approval": "Inferido_seco"}))
    if new_rows:
        daily = pd.concat([daily] + new_rows, ignore_index=True)
    daily = daily.sort_values(["code", "date"]).reset_index(drop=True)
    return daily, pd.Series(added, dtype="int64")


def main() -> None:
    daily = pd.read_csv(PROC / "precip_gauges_daily.csv", dtype={"code": str})
    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.dropna(subset=["precip_mm"])
    inv = pd.read_csv(PROC / "precip_gauges_inventory.csv", dtype={"code": str})

    diag = diagnose(daily)
    flagged = diag.zero_suppressed
    print(f"stations                 : {len(diag)}")
    print(f"zero-suppressed (flagged): {int(flagged.sum())} "
          f"({100*flagged.mean():.0f} % of network, "
          f"{int(diag.loc[flagged, 'n_rec'].sum()):,} station-days)")
    print(f"  dry-day fraction : flagged median {diag.loc[flagged,'dry_frac'].median():.2f}"
          f"  vs healthy {diag.loc[~flagged,'dry_frac'].median():.2f}")
    print(f"  annual total     : flagged median {diag.loc[flagged,'ann_before'].median():.0f}"
          f" -> {diag.loc[flagged,'ann_after'].median():.0f} mm/yr"
          f"   (healthy {diag.loc[~flagged,'ann_before'].median():.0f})")

    fixed, added = repair(daily, diag)

    post = fixed.groupby("code").precip_mm.mean()*365.25
    bad = [c for c in diag.index[flagged]
           if not (PLAUSIBLE_MM[0] <= post[c] <= PLAUSIBLE_MM[1])]
    if bad:
        print(f"\n  WARNING {len(bad)} flagged stations still implausible after repair "
              f"-> their gaps are missing data, not dry days:")
        for c in bad:
            print(f"    {c}  {post[c]:.0f} mm/yr")
    else:
        print("\n  all flagged stations land in a plausible range after repair")

    inv2 = inv.merge(diag[["dry_frac", "span_frac", "zero_suppressed",
                           "ann_before", "ann_after"]],
                     left_on="code", right_index=True, how="left")
    inv2["n_infilled"] = inv2.code.map(added).fillna(0).astype(int)
    inv2["ann_mean_mm"] = inv2.code.map(post)
    inv2["n_valid"] = inv2.code.map(fixed.groupby("code").size())

    fixed.to_csv(PROC / "precip_gauges_daily_qc.csv", index=False,
                 date_format="%Y-%m-%d", float_format="%.2f")
    inv2.to_csv(PROC / "precip_gauges_inventory_qc.csv", index=False)
    diag.to_csv(PROC / "precip_zero_suppression_report.csv")

    print(f"\nwrote precip_gauges_daily_qc.csv        {len(fixed):,} rows "
          f"(+{int(added.sum()):,} inferred dry days)")
    print(f"wrote precip_gauges_inventory_qc.csv   {len(inv2)} stations")
    print("wrote precip_zero_suppression_report.csv")
    print(f"\nbasin gauge-mean annual: {inv['ann_mean_mm'].mean():.0f} -> "
          f"{inv2['ann_mean_mm'].mean():.0f} mm/yr")


if __name__ == "__main__":
    main()
