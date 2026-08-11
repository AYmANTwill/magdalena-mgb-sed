"""C2.3 consistency + C2.4 anchor arithmetic + figures. Executes docs/34 §1.7-§1.9."""
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = r"c:\dev\magdalena-mgb-sed"
OUT = os.path.join(R, "data", "processed", "c2")
FIG = os.path.join(R, "figures", "deck")
os.makedirs(FIG, exist_ok=True)

res = pd.read_csv(os.path.join(OUT, "c2_station_window_flux.csv"))
rat = pd.read_csv(os.path.join(OUT, "c2_rate_ratios.csv"))
mon = pd.read_csv(os.path.join(OUT, "c2_monthly_shape.csv"))
res["name"] = res["name"].str.replace("\ufffd", "O", regex=False).str.strip()
rat["name"] = rat["name"].str.replace("\ufffd", "O", regex=False).str.strip()
mon["name"] = mon["name"].str.replace("\ufffd", "O", regex=False).str.strip()

# ---------------- C2.3(1) estimator agreement -------------------------------
ag = []
for _, r in res.iterrows():
    if r.a_status != "ok" or r.b_status not in ("ok", "partial-rating"):
        continue
    if not np.isfinite(r.get("b_lo", np.nan)):
        continue
    ov = (r.a_lo <= r.b_hi) and (r.b_lo <= r.a_hi)
    ag.append(dict(code=r.code, name=r["name"], window=r.window,
                   a=r.a_mean_tday, a_lo=r.a_lo, a_hi=r.a_hi,
                   b=r.b_mean_tday, b_lo=r.b_lo, b_hi=r.b_hi,
                   b_cov=r.b_cov, b_status=r.b_status,
                   ratio_b_over_a=r.b_mean_tday / r.a_mean_tday, agree=ov))
ag = pd.DataFrame(ag)
ag.to_csv(os.path.join(OUT, "c2_estimator_agreement.csv"), index=False)
print("== estimator agreement ==")
print(ag.to_string())
print("testable:", len(ag), " disjoint:", int((~ag.agree).sum()),
      " frac:", round(float((~ag.agree).mean()), 3))
print("median b/a:", round(float(ag.ratio_b_over_a.median()), 3))

# ---------------- C2.3(2) downstream monotonicity ---------------------------
m = pd.read_csv(os.path.join(R, "data/processed/minibacias.csv"))
inv = pd.read_csv(os.path.join(R, "data/processed/sediment_inventory_qc.csv"))
u = inv[inv.ssc_class.isin(["usable", "usable-with-caveat"])]
ds = dict(zip(m.id, m.downstream))


def path(x):
    p = []
    for _ in range(20000):
        p.append(x)
        n = ds.get(x)
        if n is None or (isinstance(n, float) and (np.isnan(n) or n <= 0)):
            break
        x = int(n)
    return p


mb = {int(r.minibacia): int(r.code) for r in u.itertuples() if pd.notna(r.minibacia)}
nested = []
for a in mb:
    down = set(path(a)[1:])
    for b in mb:
        if b != a and b in down:
            nested.append((mb[a], mb[b]))
nm = dict(zip(u.code, u.name.str.replace("\ufffd", "O", regex=False).str.strip()))
ar = dict(zip(u.code, u.up_area_km2))

mono = []
for est in ("a", "b"):
    col, sc = f"{est}_mean_tday", f"{est}_status"
    for up, dn in nested:
        for w in ["P-LN", "P-EN", "S-LN", "S-EN"]:
            ru = res[(res.code == up) & (res.window == w)]
            rd = res[(res.code == dn) & (res.window == w)]
            if len(ru) == 0 or len(rd) == 0:
                continue
            ru, rd = ru.iloc[0], rd.iloc[0]
            if not (np.isfinite(ru.get(col, np.nan)) and np.isfinite(rd.get(col, np.nan))):
                continue
            mono.append(dict(est=est, window=w, up=up, up_name=nm[up], dn=dn,
                             dn_name=nm[dn], up_area=ar[up], dn_area=ar[dn],
                             up_tday=ru[col], dn_tday=rd[col],
                             increases=bool(rd[col] > ru[col]),
                             up_status=ru[sc], dn_status=rd[sc]))
mono = pd.DataFrame(mono)
mono.to_csv(os.path.join(OUT, "c2_monotonicity.csv"), index=False)
print("\n== monotonicity ==")
print(mono.to_string())
if len(mono):
    print("pairs tested:", len(mono), "violations:", int((~mono.increases).sum()))

# ---------------- C2.4 anchor arithmetic ------------------------------------
print("\n== C2.4 anchor: outlet-most usable station ==")
om = res[(res.code == 21237020)]
for _, r in om.iterrows():
    for est in ("a", "b"):
        v = r.get(f"{est}_mean_tday")
        if np.isfinite(v):
            print(f"  {r.window} est({est}) {v:,.0f} t/day -> {v*365.25/1e6:,.2f} Mt/yr "
                  f"(cov={r.b_cov:.2f})" if est == "b" else
                  f"  {r.window} est({est}) {v:,.0f} t/day -> {v*365.25/1e6:,.2f} Mt/yr "
                  f"(n={int(r.n_sample_days)})")

# ================= FIGURES ==================================================
C_LN, C_EN = "#1f6fb4", "#c0392b"
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": .25,
                     "axes.spines.top": False, "axes.spines.right": False})

# --- FIG 1: per-station wet:dry RATE ratio, stations ordered downstream ------
fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.4), sharey=True)
for axi, pname in zip(axes, ["primary", "sensitivity"]):
    d = rat[rat.pair == pname].copy()
    d = d[d[["a_ratio", "b_ratio"]].notna().any(axis=1)]
    d = d.sort_values("up_area_km2")
    y = np.arange(len(d))
    axi.axvline(1.0, color="0.35", lw=1, ls="--", zorder=1)
    for i, (_, r) in enumerate(d.iterrows()):
        if np.isfinite(r.a_ratio):
            if np.isfinite(r.get("a_ratio_lo", np.nan)):
                axi.plot([r.a_ratio_lo, r.a_ratio_hi], [i + .16] * 2, color=C_LN, lw=1.4, alpha=.55)
            axi.plot(r.a_ratio, i + .16, "o", ms=6.5, color=C_LN, zorder=3)
        if np.isfinite(r.b_ratio):
            part = "partial-rating" in (str(r.b_ln_status) + str(r.b_en_status))
            if np.isfinite(r.get("b_ratio_lo", np.nan)):
                axi.plot([r.b_ratio_lo, r.b_ratio_hi], [i - .16] * 2, color=C_EN, lw=1.4, alpha=.55)
            axi.plot(r.b_ratio, i - .16, "s", ms=6, color="white" if part else C_EN,
                     mec=C_EN, mew=1.6, zorder=3)
    axi.set_yticks(y)
    axi.set_yticklabels([f"{r['name'][:20]}  ({r.up_area_km2:,.0f} km²)" for _, r in d.iterrows()])
    axi.set_xscale("log")
    axi.set_xlabel("La Niña : El Niño  RATE ratio  (mean t/day ÷ mean t/day)")
    ttl = ("PRIMARY  2011 vs 2015-01…2016-12" if pname == "primary"
           else "SENSITIVITY  2010-07…2011-06 vs 2015-10…2016-04")
    axi.set_title(ttl, fontsize=9.5)
axes[0].invert_yaxis()
h = [plt.Line2D([], [], marker="o", ls="", color=C_LN, label="(a) sample-day flux mean"),
     plt.Line2D([], [], marker="s", ls="", mfc=C_EN, mec=C_EN, color=C_EN,
                label="(b) rating-curve flux (Duan)"),
     plt.Line2D([], [], marker="s", ls="", mfc="white", mec=C_EN, mew=1.6, color="none",
                label="(b) partial-rating (cov < 0.50)")]
fig.legend(handles=h, loc="lower center", ncol=3, frameon=False, fontsize=8.5)
fig.suptitle("Observed ENSO suspended-sediment contrast — per-station RATE ratio\n"
             "stations ordered downstream by upstream area (display only; areas unreliable, docs/23 §13.2)",
             fontsize=10.5)
fig.tight_layout(rect=[0, .06, 1, .93])
fig.savefig(os.path.join(FIG, "gen_c2_ratio_dotplot.png"), dpi=160)
plt.close(fig)

# --- FIG 2: flux time series at the best stations ---------------------------
best = [23127010, 24037390, 22017010, 21197010, 21237020]
ssc = pd.read_csv(os.path.join(R, "data/processed/sediment_daily_qc.csv"),
                  usecols=["code", "date", "ssc_mean_mg_l", "c1_deleted"])
ssc = ssc[ssc.code.isin(best) & (~ssc.c1_deleted) & ssc.ssc_mean_mg_l.notna()]
q = pd.read_csv(os.path.join(R, "data/processed/discharge_daily.csv"),
                usecols=["code", "date", "q_m3s"])
q = q[q.code.isin(best) & q.q_m3s.notna()]
p = ssc.merge(q, on=["code", "date"])
p["date"] = pd.to_datetime(p.date)
p["qs"] = p.q_m3s * p.ssc_mean_mg_l * 0.0864

fig, axes = plt.subplots(len(best), 1, figsize=(11.5, 10), sharex=True)
for axi, c in zip(axes, best):
    d = p[(p.code == c) & (p.date >= "2010-01-01") & (p.date <= "2017-06-30")]
    axi.axvspan(pd.Timestamp("2011-01-01"), pd.Timestamp("2011-12-31"), color=C_LN, alpha=.13)
    axi.axvspan(pd.Timestamp("2015-01-01"), pd.Timestamp("2016-12-31"), color=C_EN, alpha=.13)
    axi.plot(d.date, d.qs, lw=.55, color="0.25")
    axi.set_yscale("log")
    axi.set_ylabel("t/day", fontsize=8)
    axi.set_title(f"{nm.get(c,c)}  ({c})  —  {len(d):,} paired days plotted", fontsize=9, loc="left")
axes[-1].set_xlabel("La Niña window (blue) · El Niño window (red) · sample-day flux Q·C·0.0864")
fig.suptitle("Observed sample-day suspended-sediment flux, 2010–2017 (absolute t/day, log scale)",
             fontsize=11)
fig.tight_layout(rect=[0, 0, 1, .965])
fig.savefig(os.path.join(FIG, "gen_c2_flux_timeseries.png"), dpi=160)
plt.close(fig)

# --- FIG 3: monthly shape ---------------------------------------------------
sel = [23127010, 24037390, 22017010, 21197010, 26017060, 22017030]
fig, axes = plt.subplots(2, len(sel), figsize=(14, 6.2), sharex=True)
for j, c in enumerate(sel):
    for i, (pn, wl, we) in enumerate([("PRIMARY", "P-LN", "P-EN"),
                                      ("SENSITIVITY", "S-LN", "S-EN")]):
        axi = axes[i, j]
        for w, col, lab in [(wl, C_LN, "La Niña"), (we, C_EN, "El Niño")]:
            d = mon[(mon.code == c) & (mon.window == w) & (mon.est == "a")].sort_values("month")
            if len(d):
                axi.plot(d.month, d.mean_tday, "-o", ms=3, color=col, label=lab)
        axi.set_yscale("log")
        axi.set_xticks([1, 4, 7, 10])
        if i == 0:
            axi.set_title(f"{nm.get(c,c)[:16]}", fontsize=8.5)
        if j == 0:
            axi.set_ylabel(f"{pn}\nmean t/day", fontsize=8)
axes[0, 0].legend(fontsize=7, frameon=False)
fig.suptitle("Monthly shape of observed sediment flux — estimator (a), sample-day mean t/day "
             "(rates only; windows are 12 vs 24 / 12 vs 7 months)", fontsize=10.5)
fig.tight_layout(rect=[0, 0, 1, .94])
fig.savefig(os.path.join(FIG, "gen_c2_monthly_shape.png"), dpi=160)
plt.close(fig)
print("\nFIGURES WRITTEN to", FIG)
