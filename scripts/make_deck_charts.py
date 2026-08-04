"""Regenerate the four gen_*.png deck charts from data/processed/sim_calibrated_v2/*.csv.

Outputs to figures/deck/: gen_attempts.png, gen_skill_clim.png,
gen_recession.png, gen_h2_h1.png. Run from anywhere (paths anchored to the
repo root). These CSVs are small — the wide-forcing pd.read_csv ban does not
apply here.
"""
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO = pathlib.Path(__file__).resolve().parent.parent
SIM = REPO / "data" / "processed" / "sim_calibrated_v2"
OUT = REPO / "figures" / "deck"

NAVY = "#1F3564"
RED = "#B03A2E"
GREEN = "#1B7F4B"
GREY = "#9AA5AE"
TEAL = "#0B6E99"
DPI = 150

# (cell, config, display label) for the three calibration attempts, in order.
ATTEMPTS = [
    ("ref", "ConfigB", "1 — Config B\n(original forcing)"),
    ("H1", "fit", "2 — H1\n(+ recession term)"),
    ("H2", "fit", "3 — H2\n(repaired forcing)"),
]


def attempt_rows(fleet: pd.DataFrame, period: str) -> pd.DataFrame:
    """One row per attempt, in ATTEMPTS order, for the given period."""
    rows = []
    for cell, config, label in ATTEMPTS:
        sel = fleet[(fleet.cell == cell) & (fleet.config == config)
                    & (fleet.period == period)]
        if len(sel) != 1:
            raise ValueError(f"expected 1 row for {cell}/{config}/{period}, got {len(sel)}")
        rows.append(sel.iloc[0].to_dict() | {"label": label})
    return pd.DataFrame(rows)


def make_attempts(fleet: pd.DataFrame) -> None:
    df = attempt_rows(fleet, "VAL all")
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    x = range(len(df))
    ax1.bar([i - 0.19 for i in x], df.kge, width=0.36, color=NAVY,
            label="VAL KGE (median)")
    ax2.bar([i + 0.19 for i in x], df.rec_ratio, width=0.36, color=RED,
            label="recession ratio (sim/obs)")
    for i, r in df.iterrows():
        ax1.annotate(f"{r.kge:.3f}", (i - 0.19, r.kge), ha="center",
                     va="bottom", fontweight="bold", color=NAVY)
        ax2.annotate(f"{r.rec_ratio:.2f}×", (i + 0.19, r.rec_ratio),
                     ha="center", va="bottom", fontweight="bold", color=RED)
    ax2.axhline(1.0, color=GREEN, ls="--", lw=1.6)
    ax2.axhspan(0.0, 1.5, color=GREEN, alpha=0.07)
    ax2.annotate("ratio = 1\n(correct)", (len(df) - 0.52, 1.02), color=GREEN,
                 fontsize=9, va="bottom")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(df.label)
    ax1.set_ylabel("VAL KGE", color=NAVY)
    ax1.set_ylim(0, 0.62)
    ax2.set_ylabel("recession ratio  (sim / obs)", color=RED)
    ax2.set_ylim(0, 4.4)
    ax1.tick_params(axis="y", colors=NAVY)
    ax2.tick_params(axis="y", colors=RED)
    kge_drop = df.kge.iloc[0] - df.kge.iloc[1]
    ax1.set_title(f"Three calibration attempts: we traded {kge_drop:.3f} KGE "
                  "for a correct recession", fontweight="bold")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper center", ncol=2)
    save(fig, "gen_attempts.png")


def make_skill_clim(fleet: pd.DataFrame) -> None:
    periods = [
        ("VAL La Nina 11", "La Niña 2011\n(WET)"),
        ("VAL El Nino 15-16", "El Niño 2015-16\n(DRY)"),
        ("VAL other 09/10/17", "other 09/10/17"),
        ("CAL 2012-14", "CAL 2012-14"),
    ]
    series = [("attempt 1 (Config B)", GREY), ("attempt 2 (H1)", NAVY),
              ("attempt 3 (H2)", TEAL)]
    values = [attempt_rows(fleet, p).skill_over_clim.tolist() for p, _ in periods]
    fig, ax = plt.subplots(figsize=(10, 5))
    width = 0.26
    for k, (name, colour) in enumerate(series):
        xs = [i + (k - 1) * width for i in range(len(periods))]
        ys = [values[i][k] for i in range(len(periods))]
        ax.bar(xs, ys, width=width * 0.94, color=colour, label=name)
        for xv, yv in zip(xs, ys):
            ax.annotate(f"{yv:+.3f}", (xv, yv),
                        ha="center", va="bottom" if yv >= 0 else "top",
                        fontsize=9, fontweight="bold",
                        color=GREEN if yv >= 0 else RED)
    ax.axhline(0, color="black", lw=1.2)
    ax.set_xticks(range(len(periods)))
    ax.set_xticklabels([lbl for _, lbl in periods])
    ax.set_ylabel("KGE gain over a day-of-year climatology")
    ax.set_title("Skill above climatology — the dry phase turns POSITIVE "
                 "in attempt 2", fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    save(fig, "gen_skill_clim.png")


def make_recession(fleet: pd.DataFrame) -> None:
    rec = pd.read_csv(SIM / "recession_validation.csv")
    h1 = fleet[(fleet.cell == "H1") & (fleet.config == "fit")]
    h1_ratio = dict(zip(h1.period, h1.rec_ratio))
    labels = {"CAL 2012-14": "CAL 2012-14", "VAL all": "all",
              "VAL La Nina 11": "La Nina 11",
              "VAL El Nino 15-16": "El Nino\n15-16",
              "VAL other 09/10/17": "other 09/10/17"}
    fig, ax = plt.subplots(figsize=(10, 5))
    width = 0.27
    for i, row in rec.iterrows():
        r1 = h1_ratio[row.period]
        bars = [(-width, row.obs_k_d, GREEN, None),
                (0.0, row.simB_k_d, RED, f"{row.ratio:.1f}×"),
                (width, row.obs_k_d * r1, NAVY, f"{r1:.2f}×")]
        for dx, val, colour, tag in bars:
            ax.bar(i + dx, val, width=width * 0.94, color=colour)
            if tag:
                ax.annotate(tag, (i + dx, val), ha="center", va="bottom",
                            fontsize=10, fontweight="bold", color=colour)
    sim_lo, sim_hi = rec.ratio.min(), rec.ratio.max()
    h1_vals = [h1_ratio[p] for p in rec.period]
    ax.set_title(f"Baseflow recession: attempt 1 was {sim_lo:.1f}–"
                 f"{sim_hi:.1f}× too slow; the refit lands within "
                 f"{min(h1_vals):.2f}–{max(h1_vals):.2f}×",
                 fontweight="bold")
    ax.set_xticks(range(len(rec)))
    ax.set_xticklabels([labels[p] for p in rec.period])
    ax.set_ylabel("recession constant  k  (days)")
    ax.grid(axis="y", alpha=0.3)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c)
               for c in (GREEN, RED, NAVY)]
    ax.legend(handles, ["observed", "attempt 1 (Config B)",
                        "attempt 2 (H1, refitted)"])
    save(fig, "gen_recession.png")


def make_h2_h1() -> None:
    diff = pd.read_csv(SIM / "h2_minus_h1.csv")
    diff = diff[diff.period == "matched all 2009-17"].set_index("metric")
    # Top-to-bottom display order; (target, display label) per metric.
    metrics = [("nse", 1.0, "NSE"), ("kge", 1.0, "KGE"),
               ("r", 1.0, "r  correlation"),
               ("alpha", 1.0, "α  variability"),
               ("beta", 1.0, "β  bias ratio"),
               ("pbias", 0.0, "PBIAS (points)")]
    fig, ax = plt.subplots(figsize=(10, 5))
    ys = range(len(metrics), 0, -1)
    for y, (m, target, label) in zip(ys, metrics):
        row = diff.loc[m]
        improved = abs(row.H2 - target) < abs(row.H1 - target)
        val = row["diff"]
        ax.barh(y, val, height=0.6, color=GREEN if improved else RED)
        txt = f"{val:+.2f}" if m == "pbias" else f"{val:+.4f}"
        ax.annotate(txt, (val, y), ha="right" if val < 0 else "left",
                    va="center", fontweight="bold",
                    xytext=(-6 if val < 0 else 6, 0),
                    textcoords="offset points")
    ax.axvline(0, color="black", lw=1.2)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([label for _, _, label in metrics])
    ax.set_xlim(-5.6, 2.0)
    ax.set_xlabel("attempt 3 (H2, repaired forcing)  −  "
                  "attempt 2 (H1, original)")
    pb, dr = diff.loc["pbias", "diff"], diff.loc["r", "diff"]
    ax.set_title(f"Repairing the rainfall: PBIAS {pb:+.2f} points, "
                 f"correlation {dr:+.3f} (unchanged)", fontweight="bold")
    ax.grid(axis="x", alpha=0.3)
    save(fig, "gen_h2_h1.png")


def save(fig, name: str) -> None:
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=DPI)
    plt.close(fig)
    print(f"wrote {OUT / name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fleet = pd.read_csv(SIM / "metrics_fleet.csv")
    make_attempts(fleet)
    make_skill_clim(fleet)
    make_recession(fleet)
    make_h2_h1()


if __name__ == "__main__":
    main()
