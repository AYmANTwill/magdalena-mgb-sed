"""C2.2/C2.3 — observed ENSO sediment contrast. Executes docs/34 §1 as frozen.
Writes tables to data/processed/c2/ (gitignored, regenerable)."""
import os, json
import numpy as np, pandas as pd

R = r"c:\dev\magdalena-mgb-sed"
OUT = os.path.join(R, "data", "processed", "c2")
os.makedirs(OUT, exist_ok=True)
SEED = 20260810
NB_A, NB_B, BLOCK = 2000, 1000, 30

WINDOWS = {
    "P-LN": ("2011-01-01", "2011-12-31"),
    "P-EN": ("2015-01-01", "2016-12-31"),
    "S-LN": ("2010-07-01", "2011-06-30"),
    "S-EN": ("2015-10-01", "2016-04-30"),
}
PAIRS = {"primary": ("P-LN", "P-EN"), "sensitivity": ("S-LN", "S-EN")}

inv = pd.read_csv(os.path.join(R, "data/processed/sediment_inventory_qc.csv"))
inv = inv[inv.ssc_class.isin(["usable", "usable-with-caveat"])].copy()
STA = list(inv.code)
sel = pd.read_csv(os.path.join(R, "data/processed/ssc_sampling_selectivity.csv"))
selmap = dict(zip(sel.code, sel.flag_flow_selective))

ssc = pd.read_csv(os.path.join(R, "data/processed/sediment_daily_qc.csv"),
                  usecols=["code", "date", "ssc_mean_mg_l", "c1_deleted"])
ssc = ssc[(ssc.code.isin(STA)) & (~ssc.c1_deleted) & ssc.ssc_mean_mg_l.notna()]
ssc["date"] = pd.to_datetime(ssc.date)

q = pd.read_csv(os.path.join(R, "data/processed/discharge_daily.csv"),
                usecols=["code", "date", "q_m3s"])
q = q[(q.code.isin(STA)) & q.q_m3s.notna() & (q.q_m3s > 0)]
q["date"] = pd.to_datetime(q.date)

fits = pd.read_csv(os.path.join(R, "data/processed/ssc_rating_fits.csv"))
fits = fits[fits.usable & fits.code.isin(STA)].copy()
fits["era_start"] = pd.to_datetime(fits.era_start)
fits["era_end"] = pd.to_datetime(fits.era_end)

pair = ssc.merge(q, on=["code", "date"], how="inner")
pair["qs"] = pair.q_m3s * pair.ssc_mean_mg_l * 0.0864
print("paired same-day rows:", len(pair), "stations:", pair.code.nunique())

qidx = {c: g.set_index("date").q_m3s.sort_index() for c, g in q.groupby("code")}
pidx = {c: g.sort_values("date") for c, g in pair.groupby("code")}

rng_global = np.random.default_rng(SEED)


def boot_a(v, nb=NB_A, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(v)
    idx = rng.integers(0, n, size=(nb, n))
    return v[idx].mean(axis=1)


def era_pairs(code, e):
    d = pidx.get(code)
    if d is None:
        return None
    m = (d.date >= e.era_start) & (d.date <= e.era_end)
    d = d[m]
    if len(d) < 15:
        return None
    return np.log(d.q_m3s.values), np.log(d.qs.values)


def rating_window(code, w0, w1):
    """Return (dates, qvals, era_id) for window days with Q inside a usable era."""
    s = qidx.get(code)
    if s is None:
        return None
    s = s[(s.index >= w0) & (s.index <= w1)]
    if len(s) == 0:
        return None
    f = fits[fits.code == code]
    era_id = np.full(len(s), -1)
    for _, e in f.iterrows():
        m = (s.index >= e.era_start) & (s.index <= e.era_end)
        era_id[np.asarray(m)] = int(e.era)
    keep = era_id >= 0
    return s.index[keep], s.values[keep], era_id[keep]


rows = []
monthly_rows = []
for code in STA:
    name = inv.loc[inv.code == code, "name"].iloc[0]
    area = inv.loc[inv.code == code, "up_area_km2"].iloc[0]
    reach = inv.loc[inv.code == code, "reach"].iloc[0]
    flagsel = bool(selmap.get(code, False))
    for wid, (a, b) in WINDOWS.items():
        w0, w1 = pd.Timestamp(a), pd.Timestamp(b)
        ndays = (w1 - w0).days + 1
        r = dict(code=code, name=name, reach=reach, up_area_km2=area, window=wid,
                 window_days=ndays, flow_selective=flagsel)
        # ---- estimator (a)
        d = pidx.get(code)
        if d is not None:
            dw = d[(d.date >= w0) & (d.date <= w1)]
        else:
            dw = pair.iloc[0:0]
        r["n_sample_days"] = len(dw)
        if flagsel:
            r["a_status"] = "flow-selective"
        elif len(dw) < 12:
            r["a_status"] = "n<12"
        else:
            v = dw.qs.values
            r["a_status"] = "ok"
            r["a_mean_tday"] = v.mean()
            r["a_median_tday"] = float(np.median(v))
            bs = boot_a(v, seed=SEED + int(code) % 100000)
            r["a_lo"], r["a_hi"] = np.percentile(bs, [2.5, 97.5])
            # EL PROFUNDO registered sensitivity
            if code == 21197010:
                mm = ~((dw.date == pd.Timestamp("2016-06-04")) & (dw.ssc_mean_mg_l > 15000))
                if (~mm).any():
                    v2 = dw[mm].qs.values
                    r["a_mean_tday_no_extreme"] = v2.mean()
                    r["a_extreme_leverage_pct"] = 100 * (v.mean() - v2.mean()) / v2.mean()
        # ---- estimator (b)
        rw = rating_window(code, w0, w1)
        if rw is None or len(rw[0]) == 0:
            r["b_status"] = "no rating days"
            r["b_cov"] = 0.0
        else:
            dts, qv, eid = rw
            r["b_cov"] = len(qv) / ndays
            lq = np.log(qv)
            pred_naive = np.zeros(len(qv))
            pred_duan = np.zeros(len(qv))
            for e_id in np.unique(eid):
                e = fits[(fits.code == code) & (fits.era == e_id)].iloc[0]
                m = eid == e_id
                ep = era_pairs(code, e)
                if ep is None:
                    S = float(np.exp(e.resid_sigma ** 2 / 2))
                else:
                    lqf, lqsf = ep
                    res = lqsf - (e.log_a + e.b * lqf)
                    S = float(np.mean(np.exp(res)))
                pn = np.exp(e.log_a + e.b * lq[m])
                pred_naive[m] = pn
                pred_duan[m] = pn * S
            r["b_status"] = "partial-rating" if r["b_cov"] < 0.50 else "ok"
            r["b_mean_tday"] = pred_duan.mean()
            r["b_mean_tday_naive"] = pred_naive.mean()
            r["b_days"] = len(qv)
            # CI: parameter refit + 30d moving-block residual bootstrap
            rng = np.random.default_rng(SEED + int(code) % 100000 + 7)
            reps = np.zeros(NB_B)
            era_cache = {}
            for e_id in np.unique(eid):
                e = fits[(fits.code == code) & (fits.era == e_id)].iloc[0]
                ep = era_pairs(code, e)
                if ep is None:
                    continue
                lqf, lqsf = ep
                res = lqsf - (e.log_a + e.b * lqf)
                era_cache[e_id] = (lqf, lqsf, res)
            ok_ci = len(era_cache) == len(np.unique(eid))
            if ok_ci:
                for k in range(NB_B):
                    tot = np.zeros(len(qv))
                    for e_id in np.unique(eid):
                        lqf, lqsf, res = era_cache[e_id]
                        n = len(lqf)
                        bi = rng.integers(0, n, size=n)
                        X = np.vstack([np.ones(n), lqf[bi]]).T
                        coef, *_ = np.linalg.lstsq(X, lqsf[bi], rcond=None)
                        m = eid == e_id
                        nd = m.sum()
                        # moving-block residual draw
                        nblk = int(np.ceil(nd / BLOCK))
                        starts = rng.integers(0, max(1, len(res) - BLOCK + 1), size=nblk)
                        rr = np.concatenate([res[s:s + BLOCK] for s in starts])[:nd]
                        if len(rr) < nd:
                            rr = np.resize(rr, nd)
                        # exp(pred + resid draw): E[exp(res)] = S, so the rep mean is
                        # consistent with the Duan-smeared point estimate by construction
                        tot[m] = np.exp(coef[0] + coef[1] * lq[m] + rr)
                    reps[k] = tot.mean()
                r["b_lo"], r["b_hi"] = np.percentile(reps, [2.5, 97.5])
        # ---- monthly shape (rates)
        if r.get("b_status") in ("ok", "partial-rating"):
            dfm = pd.DataFrame({"date": dts, "qs": pred_duan})
            for mth, gg in dfm.groupby(dfm.date.dt.month):
                monthly_rows.append(dict(code=code, name=name, window=wid, month=int(mth),
                                         est="b", mean_tday=gg.qs.mean(), n=len(gg)))
        if r.get("a_status") == "ok":
            for mth, gg in dw.groupby(dw.date.dt.month):
                monthly_rows.append(dict(code=code, name=name, window=wid, month=int(mth),
                                         est="a", mean_tday=gg.qs.mean(), n=len(gg)))
        rows.append(r)

res = pd.DataFrame(rows)
res.to_csv(os.path.join(OUT, "c2_station_window_flux.csv"), index=False)
pd.DataFrame(monthly_rows).to_csv(os.path.join(OUT, "c2_monthly_shape.csv"), index=False)
print(res.to_string())

# ---- ratios (RATE ratios only)
rat = []
for pname, (wln, wen) in PAIRS.items():
    for code in STA:
        ln = res[(res.code == code) & (res.window == wln)]
        en = res[(res.code == code) & (res.window == wen)]
        if len(ln) == 0 or len(en) == 0:
            continue
        ln, en = ln.iloc[0], en.iloc[0]
        row = dict(pair=pname, code=code, name=ln["name"], reach=ln.reach,
                   up_area_km2=ln.up_area_km2)
        for est in ("a", "b"):
            mn, md = ln.get(f"{est}_mean_tday"), en.get(f"{est}_mean_tday")
            if pd.notna(mn) and pd.notna(md) and md > 0:
                row[f"{est}_ratio"] = mn / md
                lo1, hi1 = ln.get(f"{est}_lo"), ln.get(f"{est}_hi")
                lo2, hi2 = en.get(f"{est}_lo"), en.get(f"{est}_hi")
                if pd.notna(lo1) and pd.notna(lo2):
                    row[f"{est}_ratio_lo"] = lo1 / hi2
                    row[f"{est}_ratio_hi"] = hi1 / lo2
            row[f"{est}_ln_status"] = ln.get(f"{est}_status")
            row[f"{est}_en_status"] = en.get(f"{est}_status")
            row[f"{est}_ln_tday"] = mn
            row[f"{est}_en_tday"] = md
        row["b_cov_ln"] = ln.get("b_cov")
        row["b_cov_en"] = en.get("b_cov")
        rat.append(row)
rr = pd.DataFrame(rat)
rr.to_csv(os.path.join(OUT, "c2_rate_ratios.csv"), index=False)
print(rr.to_string())
print("WROTE", OUT)
