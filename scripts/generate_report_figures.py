#!/usr/bin/env python3.10
"""Generate the data figures for the final report PDF and deck, from committed results.
No fit, no engine run — reads the JSON/CSV outputs only.  Writes figures/report/*.png.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

REPO = Path(__file__).resolve().parent.parent
PROC = REPO / "data" / "processed"
FIG = REPO / "figures" / "report"; FIG.mkdir(parents=True, exist_ok=True)
NAVY, STEEL, RUST, GREEN, GREY = "#1a3a5c", "#2e6b8a", "#a8481f", "#2e7d4f", "#777777"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": "#888", "axes.linewidth": 0.8,
                     "figure.dpi": 150})


def save(fig, name):
    fig.savefig(FIG / name, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---- Fig 1: ENSO contrast, modelled vs observed, per station
c5 = json.load(open(PROC / "c5_enso_contrast.json"))
st = c5["per_station"]
items = sorted(st.items(), key=lambda kv: -kv[1]["mod_ratio"])
codes = [f"{k}\n{v['name'][:14]}" for k, v in items]
mod = [v["mod_ratio"] for _, v in items]
oa = [v["obs_a_ratio"] for _, v in items]
ob = [v["obs_b_ratio"] for _, v in items]
x = np.arange(len(codes))
fig, ax = plt.subplots(figsize=(10, 4.3))
ax.axhspan(3, 5, color=GREEN, alpha=0.10, zorder=0, label="observed median band (~3–5×)")
ax.axhline(1, color=GREY, lw=1, ls="--", label="no contrast (ratio = 1)")
ax.bar(x, mod, color=STEEL, width=0.62, label="modelled ratio (this study)", zorder=3)
ax.scatter(x, oa, color=RUST, s=34, zorder=4, label="observed est. (a)", marker="o")
ax.scatter(x, ob, color=NAVY, s=34, zorder=4, label="observed est. (b)", marker="D")
ax.set_xticks(x); ax.set_xticklabels(codes, rotation=90, fontsize=6.3)
ax.set_ylabel("La Niña / El Niño sediment-rate ratio")
ax.set_title("Fig 1 — Modelled ENSO contrast reproduces the observed one (18/18 stations > 1)",
             fontsize=11, color=NAVY, weight="bold")
ax.legend(fontsize=7.5, loc="upper right", framealpha=0.9); ax.set_ylim(0, 11)
save(fig, "fig1_enso_contrast.png")

# ---- Fig 2: KGE vs alpha (the rail)
o5 = json.load(open(PROC / "o5_calibration_profile.json"))
pts = o5["F_report_at_beta056"]
unc = o5["unconstrained_opt_beta0p56"]
xs = sorted([float(k) for k in pts] + [unc["alpha"]])
ys = [unc["F_report"] if abs(a - unc["alpha"]) < 1e-9 else pts[[k for k in pts if abs(float(k) - a) < 1e-6][0]] for a in xs]
fig, ax = plt.subplots(figsize=(7.6, 4.2))
ax.axhspan(-0.26, 0.44, color=GREEN, alpha=0.10, label="Fagundes 'usable' band")
ax.axhline(-0.414, color=GREY, ls="--", lw=1, label="no-skill line (mean predictor)")
ax.plot(xs, ys, "-o", color=STEEL, lw=2, zorder=3, label="median KGE (β = 0.56)")
ax.axvline(2, color=RUST, ls=":", lw=1.4, label="search-box floor (α = 2) — fit rails here")
ax.scatter([unc["alpha"]], [unc["F_report"]], color=RUST, s=60, zorder=5,
           label=f"α the data wants ≈ {unc['alpha']:.2f}")
ax.scatter([11.8], [pts["11.8"]], color=NAVY, s=45, zorder=5, label="Williams α = 11.8")
ax.set_xscale("log"); ax.set_xlabel("α (erosion level knob, log scale)")
ax.set_ylabel("median KGE (F_report)")
ax.set_title("Fig 2 — The calibration rails: it wants α below the plausible floor",
             fontsize=11, color=NAVY, weight="bold")
ax.legend(fontsize=7.3, loc="lower left"); ax.set_xlim(0.3, 33)
save(fig, "fig2_kge_alpha_rail.png")

# ---- Fig 3: per-station KGE tracks r (the ceiling)
ps = o5["per_station"]
rr = [v["r"] for v in ps.values()]; kk = [v["KGE_at_box_opt"] for v in ps.values()]
fig, ax = plt.subplots(figsize=(6.8, 4.2))
ax.axhline(0, color=GREY, lw=0.7)
ax.scatter(rr, kk, color=STEEL, s=48, zorder=3)
ax.axvline(0.57, color=RUST, ls="--", lw=1.3, label="hydrology r ceiling ≈ 0.57")
ax.set_xlabel("station runoff-timing correlation  r")
ax.set_ylabel("station sediment KGE")
ax.set_title("Fig 3 — Sediment skill tracks runoff-timing skill\n(where r is high, KGE is high — the ceiling is the runoff, not the model)",
             fontsize=10, color=NAVY, weight="bold")
ax.legend(fontsize=8, loc="lower right")
save(fig, "fig3_kge_vs_r.png")

# ---- Fig 4: rainfall ceiling bound (isolation bands)
bands = ["< 10 km\n(pure gauge)", "10–30 km\n(blend helps)", "> 30 km\n(CHIRPS hurts)"]
share = [25.8, 57.1, 17.1]; dr = [0.0, +0.023, -0.043]
contrib = [s / 100 * d for s, d in zip(share, dr)]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.8), gridspec_kw={"width_ratios": [1.2, 1]})
cols = [GREY, GREEN, RUST]
a1.bar(bands, share, color=cols)
a1.set_ylabel("% of basin area"); a1.set_title("Where each cell sits vs. the nearest gauge", fontsize=9.5)
for i, (s, d) in enumerate(zip(share, dr)):
    a1.text(i, s + 1, f"Δr={d:+.3f}", ha="center", fontsize=8)
a2.bar(bands, contrib, color=cols)
a2.axhline(sum(contrib), color=NAVY, lw=1.6, ls="--", label=f"net Δr = {sum(contrib):+.4f}")
a2.set_ylabel("contribution to basin-mean Δr"); a2.set_title("Best-case gain from the satellite blend", fontsize=9.5)
a2.legend(fontsize=8)
fig.suptitle("Fig 4 — Even a perfect rainfall repair lifts r by only +0.006: the ceiling is structural",
             fontsize=11, color=NAVY, weight="bold", y=1.03)
save(fig, "fig4_ceiling_bound.png")

# ---- Fig 5: ONI 2009-2018 with the windows
oni = {  # DJF..NDJ per year, 12 overlapping seasons
 2009:[-0.89,-0.84,-0.63,-0.35,0.03,0.34,0.50,0.56,0.66,0.92,1.31,1.50],
 2010:[1.47,1.21,0.88,0.38,-0.16,-0.66,-0.98,-1.24,-1.43,-1.54,-1.57,-1.48],
 2011:[-1.29,-1.06,-0.85,-0.68,-0.50,-0.34,-0.37,-0.50,-0.76,-0.94,-1.02,-0.92],
 2012:[-0.71,-0.56,-0.44,-0.35,-0.18,0.03,0.28,0.39,0.37,0.28,0.13,-0.03],
 2013:[-0.24,-0.28,-0.23,-0.20,-0.30,-0.38,-0.45,-0.34,-0.32,-0.14,-0.12,-0.11],
 2014:[-0.24,-0.21,-0.02,0.25,0.35,0.22,0.07,0.07,0.24,0.51,0.70,0.80],
 2015:[0.73,0.65,0.72,0.86,1.04,1.19,1.44,1.73,2.02,2.28,2.45,2.59],
 2016:[2.50,2.21,1.69,1.11,0.57,0.09,-0.19,-0.34,-0.42,-0.51,-0.49,-0.37],
 2017:[-0.08,0.08,0.27,0.32,0.35,0.32,0.14,-0.07,-0.23,-0.44,-0.61,-0.76],
 2018:[-0.71,-0.67,-0.55,-0.35,-0.07,0.13,0.20,0.30,0.52,0.82,1.04,1.05]}
t = []; v = []
for y in range(2009, 2019):
    for m in range(12):
        t.append(y + (m + 0.5) / 12); v.append(oni[y][m])
t = np.array(t); v = np.array(v)
fig, ax = plt.subplots(figsize=(10, 3.6))
ax.axhspan(0.5, 3, color=RUST, alpha=0.06); ax.axhspan(-3, -0.5, color=STEEL, alpha=0.06)
ax.axhline(0.5, color=RUST, lw=0.8, ls=":"); ax.axhline(-0.5, color=STEEL, lw=0.8, ls=":")
ax.axhline(0, color=GREY, lw=0.6)
ax.fill_between(t, v, 0, where=v >= 0, color=RUST, alpha=0.55, interpolate=True)
ax.fill_between(t, v, 0, where=v < 0, color=STEEL, alpha=0.55, interpolate=True)
ax.plot(t, v, color=NAVY, lw=1.1)
ax.axvspan(2011, 2012, color=STEEL, alpha=0.18); ax.text(2011.5, 2.7, "La Niña 2011\n(wet, P-LN)", ha="center", fontsize=7.5, color=STEEL)
ax.axvspan(2015, 2017, color=RUST, alpha=0.15); ax.text(2016, 2.7, "El Niño 2015–16\n(dry, P-EN)", ha="center", fontsize=7.5, color=RUST)
ax.axvspan(2012, 2015, color=GREY, alpha=0.10); ax.text(2013.5, -2.4, "CAL window 2012–2014", ha="center", fontsize=7.5, color=GREY)
ax.set_ylabel("ONI (°C)"); ax.set_xlim(2009, 2019); ax.set_ylim(-2.9, 3.1)
ax.set_title("Fig 5 — ENSO index (ONI) over the study period: the calibration window vs. the out-of-sample ENSO windows",
             fontsize=10.5, color=NAVY, weight="bold")
save(fig, "fig5_oni_windows.png")

print("wrote figures:", *[p.name for p in sorted(FIG.glob("*.png"))])
