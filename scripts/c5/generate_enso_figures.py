#!/usr/bin/env python3.10
"""Detailed ENSO-contrast figures for the paper-depth deck section. Reads committed results only."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]           # scripts/c5/ -> scripts/ -> repo root
PROC = REPO / "data" / "processed"
FIG = REPO / "figures" / "deck"; FIG.mkdir(parents=True, exist_ok=True)
NAVY, STEEL, RUST, GREEN, GREY = "#1a3a5c", "#2e6b8a", "#a8481f", "#2e7d4f", "#777"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": "#888", "figure.dpi": 150})


def save(fig, n):
    fig.savefig(FIG / n, dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)


# ---- OBSERVED contrast per station (primary pair), estimators (a) and (b), with CIs
o = pd.read_csv(PROC / "c2" / "c2_rate_ratios.csv", dtype={"code": str})
o = o[o["pair"] == "primary"].copy()
o = o[o["a_ratio"].notna() | o["b_ratio"].notna()].copy()
o["srt"] = o[["a_ratio", "b_ratio"]].max(axis=1)
o = o.sort_values("srt", ascending=False)
y = np.arange(len(o))[::-1]
fig, ax = plt.subplots(figsize=(9.6, 5.0))
ax.axvspan(3, 9, color=GREEN, alpha=0.08, zorder=0, label="honest observed range ~3–9×")
ax.axvline(1, color=GREY, ls="--", lw=1, label="no contrast (=1)")
for yi, (_, r) in zip(y, o.iterrows()):
    if pd.notna(r["a_ratio"]):
        lo, hi = r.get("a_ratio_lo", np.nan), r.get("a_ratio_hi", np.nan)
        if pd.notna(lo) and pd.notna(hi):
            ax.plot([lo, hi], [yi + 0.12, yi + 0.12], color=RUST, lw=1.3, alpha=0.5)
        ax.scatter(r["a_ratio"], yi + 0.12, color=RUST, s=42, zorder=4)
    if pd.notna(r["b_ratio"]):
        lo, hi = r.get("b_ratio_lo", np.nan), r.get("b_ratio_hi", np.nan)
        if pd.notna(lo) and pd.notna(hi):
            ax.plot([lo, hi], [yi - 0.12, yi - 0.12], color=NAVY, lw=1.3, alpha=0.5)
        ax.scatter(r["b_ratio"], yi - 0.12, color=NAVY, s=42, marker="D", zorder=4)
ax.set_yticks(y); ax.set_yticklabels([f"{c}  {n[:16]}" for c, n in zip(o["code"], o["name"])], fontsize=8)
ax.scatter([], [], color=RUST, s=42, label="estimator (a) — paired sample-day flux")
ax.scatter([], [], color=NAVY, s=42, marker="D", label="estimator (b) — rating-curve flux")
ax.set_xscale("log"); ax.set_xlim(0.9, 40)
ax.set_xticks([1, 2, 3, 5, 9, 20]); ax.set_xticklabels(["1", "2", "3", "5", "9", "20"])
ax.set_xlabel("observed wet:dry sediment-RATE ratio  (La Niña ÷ El Niño, t/day),  log scale")
ax.set_title("Observed ENSO sediment contrast — every station La Niña > El Niño (22/22 ratios)",
             fontsize=12, color=NAVY, weight="bold")
ax.legend(fontsize=8.5, loc="lower right", framealpha=0.95)
save(fig, "gen_obs_contrast_detail.png")

# ---- SENSITIVITY: modelled median ratio across beta x window (direction invariant)
s = pd.read_csv(PROC / "c5_sensitivity.csv")
betas = sorted(s["beta"].unique())
fig, ax = plt.subplots(figsize=(8.4, 4.4))
w = 0.36
xp = np.arange(len(betas))
pri = [s[(s.beta == b) & (s.window == "primary")]["median"].iloc[0] for b in betas]
sec = [s[(s.beta == b) & (s.window == "secondary")]["median"].iloc[0] for b in betas]
ax.axhspan(3, 5, color=GREEN, alpha=0.08, label="observed primary median (~3–5×)")
ax.axhline(1, color=GREY, ls="--", lw=1)
ax.bar(xp - w / 2, pri, w, color=STEEL, label="primary windows (2011 vs 2015–16)")
ax.bar(xp + w / 2, sec, w, color=RUST, label="secondary (ONI-peak) windows")
for i, (p, q) in enumerate(zip(pri, sec)):
    ax.text(i - w / 2, p + 0.1, f"{p:.2f}", ha="center", fontsize=8)
    ax.text(i + w / 2, q + 0.1, f"{q:.2f}", ha="center", fontsize=8)
ax.set_xticks(xp); ax.set_xticklabels([f"β = {b}" for b in betas])
ax.set_ylabel("modelled median wet:dry ratio")
ax.set_title("Robustness — the contrast direction (18/18) never reverses across β or window choice",
             fontsize=11.5, color=NAVY, weight="bold")
ax.legend(fontsize=8.5, loc="upper left"); ax.set_ylim(0, 7)
save(fig, "gen_sensitivity_detail.png")

print("wrote gen_obs_contrast_detail.png, gen_sensitivity_detail.png")
