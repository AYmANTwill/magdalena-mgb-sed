#!/usr/bin/env python3.10
"""C5 sensitivity — is the modelled ENSO sediment contrast robust to β and to the window
definition?  (docs/56 owed robustness; docs/34 §1.2 primary vs secondary window pairs.)

Sweeps β in {0.45, 0.56, 0.65} (the G2.3 gate span) and evaluates BOTH window pairs from the
same daily series:
    PRIMARY    P-LN 2011           vs  P-EN 2015-01..2016-12
    SECONDARY  S-LN 2010-07..2011-06  vs  S-EN 2015-10..2016-04   (ONI-peak centred)
Ratio is mean t/day(LN)/mean t/day(EN) per station; α- and LS-invariant.  Adopted V4_dg field.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts" / "c3"))
import mgb_sediment as sed          # noqa: E402
import ls_stratified_report as SR   # noqa: E402

PROC = REPO / "data" / "processed"
FROZEN = PROC / "sim_calibrated_v2"
BETAS = [0.45, 0.56, 0.65]
PAIRS = {
    "primary":   ((np.datetime64("2011-01-01"), np.datetime64("2011-12-31")),
                  (np.datetime64("2015-01-01"), np.datetime64("2016-12-31"))),
    "secondary": ((np.datetime64("2010-07-01"), np.datetime64("2011-06-30")),
                  (np.datetime64("2015-10-01"), np.datetime64("2016-04-30"))),
}


def main() -> int:
    cats, usable = SR.station_catchments()
    codes = [str(int(c)) for c in usable["code"]]
    drv = sed.load_drivers(FROZEN / "h2e_drivers.npz")
    geom = sed.load_geometry(PROC, mini_ids=drv.mini_ids)
    assert geom.ls2d_column == "V4_dg"
    dates = np.asarray(drv.dates, dtype="datetime64[D]")
    mid_to_col = {int(m): j for j, m in enumerate(geom.mini_ids)}
    cat_cols = {c: [mid_to_col[m] for m in cats[c] if m in mid_to_col] for c in codes}

    print(f"{'beta':>5} {'window':>10} {'n>1':>7} {'median':>8} {'geomean':>8} {'range':>14}")
    rows = []
    for b in BETAS:
        run = sed.simulate_sediment(geom, sed.SedParams(alpha=1.0, beta=b), drv.qsur_mm,
                                    dates=drv.dates, store_daily=True, dtype_out=np.float64)
        D = run.delivered_t_day
        series = {c: D[:, cat_cols[c]].sum(axis=1) for c in codes}
        for pair, ((l0, l1), (e0, e1)) in PAIRS.items():
            lnm = (dates >= l0) & (dates <= l1)
            enm = (dates >= e0) & (dates <= e1)
            r = np.array([series[c][lnm].mean() / series[c][enm].mean() for c in codes])
            r = r[np.isfinite(r) & (r > 0)]
            print(f"{b:>5.2f} {pair:>10} {int((r>1).sum()):>4}/{r.size:<2} "
                  f"{np.median(r):>8.2f} {np.exp(np.log(r).mean()):>8.2f} "
                  f"{r.min():>6.2f}-{r.max():<6.2f}")
            rows.append(dict(beta=b, window=pair, n_gt1=int((r > 1).sum()), n=int(r.size),
                             median=float(np.median(r)), geomean=float(np.exp(np.log(r).mean()))))
    pd.DataFrame(rows).to_csv(PROC / "c5_sensitivity.csv", index=False)
    allpos = all(x["n_gt1"] == x["n"] for x in rows)
    print(f"\nDirection La Nina > El Nino holds in EVERY (beta, window) cell: {allpos}")
    print("Observed (docs/34): 22/22 > 1, median ~3-5 primary.  wrote c5_sensitivity.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
