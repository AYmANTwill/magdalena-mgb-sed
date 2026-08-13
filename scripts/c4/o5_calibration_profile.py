#!/usr/bin/env python3.10
"""C4.3 / docs/47 O5 — the sediment calibration profile, on the ADOPTED LS field (Branch B).

The registered objective (docs/45 §3) is KGE on log flux over the CAL-8 stations.  Two free
parameters: alpha in [2,30] (a pure multiplicative scale -> CLOSED FORM), beta in [0.40,0.75]
(the event exponent -> one engine run per value).  k_dep = 0 / SDR = 1 (docs/45 §2.3), so the
simulated flux at a station is the hillslope load summed over its catchment — no routing.

This is the first run of the objective on the adopted field V4_dg (ACT 2 made it load_geometry's
default), with per-station r, v, m re-derived on new residuals — the Branch-B requirement that
Delta_shape != 0 forces (docs/46 §6.1; docs/53).  It is NOT a rescale of the V0 profile.

Objective, per station s over its CAL paired days D_s (docs/45 §3.1):
    x = ln(flux_obs)   [estimator (a): q_m3s * ssc_mean_mg_l * 0.0864, c1_deleted==False]
    y = ln(flux_sim)   [alpha * hillslope load summed over catchment, same days]
    r = corr(x,y)   v = sd(y)/sd(x)   m = mean(y)/mean(x)
    KGE_ln = 1 - sqrt((r-1)^2 + (v-1)^2 + (m-1)^2)
    F_search = mean over CAL-8 ;  F_report = median over CAL-8 ;  bar F_report in [-0.26, 0.44]

alpha closes analytically: scaling flux_sim by alpha adds ln(alpha) to mean(y), leaves sd(y), r.
So one engine run per beta at alpha=1 gives every alpha.

Writes: data/processed/o5_calibration_profile.json  (+ .md fragment).  Reads only; no default moved.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts" / "c3"))
import mgb_sediment as sed        # noqa: E402
import ls_stratified_report as SR  # noqa: E402  (reuse station_catchments)

PROC = REPO / "data" / "processed"
FROZEN = PROC / "sim_calibrated_v2"

CAL8 = ["22017030", "26137110", "24027030", "21197010",
        "23127010", "26127010", "22017010", "24037390"]
EVAL5 = ["26017060", "26017020", "26167070", "26207080", "21237020"]  # scored, never fitted (§2.4)
ALLSTA = CAL8 + EVAL5
FLOW_SELECTIVE = {"26127010"}                       # docs/45 §3.4, kept but flagged (G12)
CAL_START, CAL_END = np.datetime64("2012-01-01"), np.datetime64("2014-12-31")
BETAS = [0.40, 0.45, 0.50, 0.56, 0.60, 0.65, 0.70, 0.75]
ALPHAS = np.geomspace(2.0, 30.0, 57)                # registered box [2,30], log-spaced
BAR = (-0.26, 0.44)                                 # docs/45 §3.2 Fagundes median-KGE band
ALPHA_HARD_STOP = (3.9, 35.4)                       # docs/35 §6.1 (source-LS); adopted-level §9.5


def observed_flux() -> dict[str, pd.DataFrame]:
    """Estimator (a): paired sample-day flux per CAL station over the CAL window."""
    ssc = pd.read_csv(PROC / "sediment_daily_qc.csv", dtype={"code": str},
                      parse_dates=["date"])
    ssc = ssc[(~ssc["c1_deleted"].astype(bool)) & ssc["ssc_mean_mg_l"].notna()]
    q = pd.read_csv(PROC / "discharge_daily.csv", dtype={"code": str}, parse_dates=["date"])
    qcol = "q_m3s" if "q_m3s" in q.columns else [c for c in q.columns
                                                 if c not in ("code", "date")][0]
    obs = ssc.merge(q[["code", "date", qcol]], on=["code", "date"], how="inner")
    obs["flux"] = obs[qcol] * obs["ssc_mean_mg_l"] * 0.0864
    obs = obs[(obs["flux"] > 0) & (obs["date"] >= CAL_START) & (obs["date"] <= CAL_END)]
    out = {}
    for code in ALLSTA:
        d = obs[obs["code"] == code][["date", "flux"]].dropna()
        out[code] = d.set_index("date")["flux"]
    return out


def sim_base_series(betas, mini_col, cats) -> dict:
    """Per station, per beta: the daily hillslope flux summed over its catchment at alpha=1."""
    drv = sed.load_drivers(FROZEN / "h2e_drivers.npz")
    geom = sed.load_geometry(PROC, mini_ids=drv.mini_ids)     # adopted default = V4_dg (ACT 2)
    print(f"engine geometry: ls2d_column={geom.ls2d_column!r}  (must be V4_dg)")
    assert geom.ls2d_column == "V4_dg", "engine is not on the adopted field — abort"
    dates = np.asarray(drv.dates, dtype="datetime64[D]")
    # catchment -> delivered_t_day column indices (columns are geom.mini_ids order)
    mid_to_col = {int(m): j for j, m in enumerate(geom.mini_ids)}
    cat_cols = {c: [mid_to_col[m] for m in cats[c] if m in mid_to_col] for c in ALLSTA}

    series = {c: {} for c in ALLSTA}
    for b in betas:
        t0 = time.time()
        p = sed.SedParams(alpha=1.0, beta=float(b))
        run = sed.simulate_sediment(geom, p, drv.qsur_mm, dates=drv.dates,
                                    store_daily=True, dtype_out=np.float64)
        D = run.delivered_t_day                     # (ndays, n_mini) tonnes/day at alpha=1
        for c in ALLSTA:
            series[c][b] = D[:, cat_cols[c]].sum(axis=1)
        print(f"  beta={b:.2f}: engine {time.time()-t0:.0f}s "
              f"(basin day-mean {D.sum(axis=1).mean():.3g} t/d at alpha=1)")
    return {"dates": dates, "series": series}


def kge_profile(obs, sim) -> dict:
    dates = sim["dates"]
    date_idx = {d: i for i, d in enumerate(dates)}
    # per station, per beta: the log-flux moments needed to close alpha analytically
    MIN_N = 15                                    # need enough paired days for a KGE at all
    moments = {}
    for c in ALLSTA:
        od = obs[c]
        keep_mask = [np.datetime64(d, "D") in date_idx for d in od.index]
        di = np.array([date_idx[np.datetime64(d, "D")] for d, k in zip(od.index, keep_mask) if k],
                      dtype=int)
        x = np.log(od.values[keep_mask])
        moments[c] = {"n": int(x.size)}
        if x.size < MIN_N:
            moments[c]["insufficient"] = True
            continue
        moments[c].update(meanx=float(x.mean()), sdx=float(x.std(ddof=1)), by_beta={})
        for b in BETAS:
            lb = np.log(sim["series"][c][b][di])
            moments[c]["by_beta"][b] = {"mean_lnbase": float(lb.mean()),
                                        "sd_lnbase": float(lb.std(ddof=1)),
                                        "r": float(np.corrcoef(x, lb)[0, 1])}

    def kge(c, b, alpha):
        mo = moments[c]
        mm = mo["by_beta"][b]
        r = mm["r"]
        v = mm["sd_lnbase"] / mo["sdx"]
        m = (np.log(alpha) + mm["mean_lnbase"]) / mo["meanx"]
        return 1.0 - np.sqrt((r - 1) ** 2 + (v - 1) ** 2 + (m - 1) ** 2)

    # profile over the registered box
    grid = []
    for b in BETAS:
        for a in ALPHAS:
            ks = np.array([kge(c, b, a) for c in CAL8])
            grid.append({"beta": b, "alpha": float(a),
                         "F_search": float(np.mean(ks)), "F_report": float(np.median(ks))})
    gdf = pd.DataFrame(grid)

    # in-box optimum of F_report (what §6 judges), within the beta GATE [0.45,0.65]
    ingate = gdf[(gdf.beta >= 0.45) & (gdf.beta <= 0.65)]
    best = ingate.loc[ingate.F_report.idxmax()]
    best_search = ingate.loc[ingate.F_search.idxmax()]

    # unconstrained (alpha allowed below the box) argmax of F_report, per gate-central beta 0.56
    fine_a = np.geomspace(0.02, 30.0, 400)
    unc = []
    for a in fine_a:
        ks = np.array([kge(c, 0.56, a) for c in CAL8])
        unc.append((a, float(np.median(ks))))
    ua, uf = max(unc, key=lambda t: t[1])

    # per-station KGE at the in-box optimum (for the report)
    per_station = {c: {"n": moments[c]["n"],
                       "flow_selective": c in FLOW_SELECTIVE,
                       "KGE_at_box_opt": float(kge(c, best.beta, best.alpha)),
                       "r": moments[c]["by_beta"][best.beta]["r"]}
                   for c in CAL8}

    verdict_railed = bool(best.alpha <= ALPHAS[0] * 1.001 or best.alpha >= ALPHAS[-1] * 0.999)
    verdict_bar = "PASS" if best.F_report >= BAR[0] else "FAIL"

    # G12 — mandatory leave-one-out on the flow-selective station (docs/45 §3.4)
    keep = [c for c in CAL8 if c not in FLOW_SELECTIVE]
    g12 = []
    for b in BETAS:
        for a in ALPHAS:
            ks = np.array([kge(c, b, a) for c in keep])
            g12.append({"beta": b, "alpha": float(a), "F_report": float(np.median(ks))})
    g12df = pd.DataFrame(g12)
    g12df = g12df[(g12df.beta >= 0.45) & (g12df.beta <= 0.65)]
    g12best = g12df.loc[g12df.F_report.idxmax()]
    g12_bar = "PASS" if g12best.F_report >= BAR[0] else "FAIL"
    g12_flips = bool((g12_bar != verdict_bar))

    # EVAL — 5 stations scored at the CAL optimum, never fitted (§2.4)
    eval_scores = {}
    for c in EVAL5:
        if "by_beta" not in moments[c]:
            eval_scores[c] = {"n": moments[c]["n"], "scored": False,
                              "reason": "fewer than 15 paired CAL days"}
        else:
            eval_scores[c] = {"n": moments[c]["n"], "scored": True,
                              "r": moments[c]["by_beta"][best.beta]["r"],
                              "KGE_at_cal_opt": float(kge(c, best.beta, best.alpha))}

    return {
        "betas": BETAS, "alpha_box": [float(ALPHAS[0]), float(ALPHAS[-1])], "bar": list(BAR),
        "in_box_optimum": {"beta": float(best.beta), "alpha": float(best.alpha),
                           "F_report": float(best.F_report), "F_search": float(best.F_search),
                           "railed": verdict_railed, "vs_bar": verdict_bar},
        "in_box_F_search_opt": {"beta": float(best_search.beta), "alpha": float(best_search.alpha),
                                "F_search": float(best_search.F_search),
                                "F_report": float(best_search.F_report)},
        "unconstrained_opt_beta0p56": {"alpha": float(ua), "F_report": float(uf)},
        "F_report_at_beta056": {f"{a:.3g}": float(np.median([kge(c, 0.56, a) for c in CAL8]))
                                for a in [2.0, 2.967, 8.902, 11.8, 30.0]},
        "per_station": per_station,
        "g12_leave_out_flowsel": {"dropped": list(FLOW_SELECTIVE), "beta": float(g12best.beta),
                                  "alpha": float(g12best.alpha), "F_report": float(g12best.F_report),
                                  "vs_bar": g12_bar, "verdict_flips": g12_flips},
        "eval_stations_at_cal_opt": eval_scores,
        "n_stations": len(CAL8),
    }


def render_md(rep) -> list[str]:
    o = rep["in_box_optimum"]
    L = ["### C4.3 / O5 — sediment KGE profile on the ADOPTED field (V4_dg), Branch-B first run", "",
         f"CAL-8, estimator (a), CAL window 2012–2014. Bar `F_report` ∈ [{rep['bar'][0]}, "
         f"{rep['bar'][1]}] (Fagundes median). α box [2, 30]; β gate [0.45, 0.65].", "",
         f"**In-box optimum (F_report):** β **{o['beta']:.2f}**, α **{o['alpha']:.3g}**, "
         f"F_report **{o['F_report']:.3f}**, F_search **{o['F_search']:.3f}** — "
         f"{'RAILED at the box edge' if o['railed'] else 'interior'}, **{o['vs_bar']}** vs bar.",
         f"**Unconstrained (β 0.56):** α **{rep['unconstrained_opt_beta0p56']['alpha']:.3g}**, "
         f"F_report **{rep['unconstrained_opt_beta0p56']['F_report']:.3f}** "
         f"(α below the box floor — not a physical value).", "",
         "**F_report at reference α (β 0.56):**", "",
         "| α | meaning | F_report |", "|--:|---|--:|"]
    lab = {"2": "box floor", "2.967": "docs/35 §9.5 adopted ref", "8.902": "§9.5 hard stop",
           "11.8": "Williams", "30": "box ceiling"}
    for a, f in rep["F_report_at_beta056"].items():
        L.append(f"| {a} | {lab.get(a,'')} | {f:.3f} |")
    L += ["", "**Per-station KGE at the in-box optimum:**", "",
          "| station | n | flow-sel | r | KGE |", "|---|--:|:--:|--:|--:|"]
    for c, s in rep["per_station"].items():
        L.append(f"| {c} | {s['n']} | {'Y' if s['flow_selective'] else ''} | "
                 f"{s['r']:.2f} | {s['KGE_at_box_opt']:.3f} |")
    g = rep["g12_leave_out_flowsel"]
    L += ["", f"**G12 (leave out flow-selective {g['dropped']}):** F_report **{g['F_report']:.3f}** "
          f"(β {g['beta']:.2f}, α {g['alpha']:.3g}), {g['vs_bar']} vs bar — "
          f"verdict {'FLIPS ⇒ INDETERMINATE' if g['verdict_flips'] else 'holds'}."]
    L += ["", "**EVAL stations (scored at CAL optimum, never fitted):**", "",
          "| station | n | r | KGE |", "|---|--:|--:|--:|"]
    for c, s in rep["eval_stations_at_cal_opt"].items():
        if s.get("scored"):
            L.append(f"| {c} | {s['n']} | {s['r']:.2f} | {s['KGE_at_cal_opt']:.3f} |")
        else:
            L.append(f"| {c} | {s['n']} | — | not scored ({s['reason']}) |")
    return L


def main() -> int:
    cats, _ = SR.station_catchments()
    obs = observed_flux()
    for c in CAL8:
        print(f"  obs {c}: {len(obs[c])} paired CAL days")
    sim = sim_base_series(BETAS, None, cats)
    rep = kge_profile(obs, sim)
    (PROC / "o5_calibration_profile.json").write_text(json.dumps(rep, indent=1))
    md = "\n".join(render_md(rep))
    (PROC / "o5_calibration_profile.md").write_text(md)
    print("\n" + md)
    print("\nwrote data/processed/o5_calibration_profile.{json,md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
