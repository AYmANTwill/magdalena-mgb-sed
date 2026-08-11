"""C2b.2 peak-bias measurement. Follows docs/33 s2.3 exactly.

Primary day set: docs/33 s2.1 data handling (<=3 d gap interpolation, >=180 d segments),
applied identically to obs and sim. Raw-mask variant reported as robustness only.
"""
import json
import numpy as np
import pandas as pd

NPZ = 'data/processed/sim_calibrated_v2/q_gauge_H2E.npz'
OUT = 'C:/Users/KNADE~1.MSI/AppData/Local/Temp/claude/c--dev-magdalena-mgb-sed/3d81998f-30ab-4e88-ba3e-09f1f28fae62/scratchpad'

MIN_SEG = 180          # docs/33 s2.1
MAX_GAP = 3            # docs/33 s2.1
MIN_YEAR_DAYS = 300    # docs/33 s2.3(a)
POT_SEP = 10           # docs/33 s2.3(c)
POT_FRAC = 0.6         # docs/33 s2.3(c)
LAG_WIN = 15           # NOT pre-registered - this session's choice, diagnostic only
BETA_MUSLE = 0.56      # docs/31 s0 / docs/33 s1

d = np.load(NPZ, allow_pickle=True)
dates = pd.DatetimeIndex(d['dates'])
gc = d['gauge_code']
area = d['gauge_upstream_area_km2'].astype(float)
QO = d['q_obs_m3s'].astype(np.float64)
QS = d['q_sim_fit_m3s'].astype(np.float64)
yr = dates.year.to_numpy()
NT, NG = QO.shape

PERIODS = [
    ('CAL 2012-14', np.isin(yr, [2012, 2013, 2014])),
    ('VAL all', ~np.isin(yr, [2012, 2013, 2014])),
    ('VAL La Nina 11', yr == 2011),
    ('VAL El Nino 15-16', np.isin(yr, [2015, 2016])),
    ('VAL other 09/10/17', np.isin(yr, [2009, 2010, 2017])),
    ('VAL 2018', yr == 2018),
]


def build_mask(qo, segmented=True):
    """Return (mask, qo_filled) after <=3 d gap interpolation and >=180 d segmentation."""
    v = np.isfinite(qo)
    q = qo.copy()
    if not segmented:
        return v, q
    # linear interpolation of gaps <= MAX_GAP
    idx = np.flatnonzero(v)
    if idx.size < 2:
        return np.zeros(NT, bool), q
    filled = v.copy()
    for a, b in zip(idx[:-1], idx[1:]):
        gap = b - a - 1
        if 0 < gap <= MAX_GAP:
            q[a + 1:b] = np.interp(np.arange(a + 1, b), [a, b], [qo[a], qo[b]])
            filled[a + 1:b] = True
    # segments of >= MIN_SEG contiguous valid days
    out = np.zeros(NT, bool)
    i = 0
    while i < NT:
        if filled[i]:
            j = i
            while j < NT and filled[j]:
                j += 1
            if j - i >= MIN_SEG:
                out[i:j] = True
            i = j
        else:
            i += 1
    return out, q


def local_maxima_above(q, m, thr):
    """Indices of days that are valid, above thr, and >= their valid neighbours."""
    idx = np.flatnonzero(m & (q > thr))
    if idx.size == 0:
        return idx
    keep = []
    vidx = np.flatnonzero(m)
    pos = {t: k for k, t in enumerate(vidx)}
    qv = q[vidx]
    for t in idx:
        k = pos[t]
        left = qv[k - 1] if k > 0 else -np.inf
        right = qv[k + 1] if k + 1 < qv.size else -np.inf
        if qv[k] >= left and qv[k] >= right:
            keep.append(t)
    return np.array(keep, dtype=int)


def pot_peaks(q, m, thr):
    """Independent peaks-over-threshold, docs/33 s2.3(c) independence rule."""
    cand = list(local_maxima_above(q, m, thr))
    if not cand:
        return []
    changed = True
    while changed and len(cand) > 1:
        changed = False
        i = 0
        while i < len(cand) - 1:
            a, b = cand[i], cand[i + 1]
            between = np.flatnonzero(m[a + 1:b]) + a + 1
            mn = q[between].min() if between.size else 0.0
            indep = (b - a >= POT_SEP) and (mn < POT_FRAC * min(q[a], q[b]))
            if not indep:
                cand[i] = a if q[a] >= q[b] else b
                del cand[i + 1]
                changed = True
            else:
                i += 1
    return cand


rows = []
excl = []
for g in range(NG):
    m, qo = build_mask(QO[:, g], segmented=True)
    qs = QS[:, g]
    nval = int(m.sum())
    if nval < 30:
        excl.append((str(gc[g]), nval, 'no qualifying segment'))
        continue
    rec = {'gauge': str(gc[g]), 'area_km2': area[g], 'n_valid': nval,
           'lt_1095_days': nval < 1095}

    # ---- (a) AMS, calendar years with >= 300 valid days -------------------------
    ratios, yrs = [], []
    for y in range(2009, 2019):
        my = m & (yr == y)
        if my.sum() < MIN_YEAR_DAYS:
            continue
        mo, ms = qo[my].max(), qs[my].max()
        if mo <= 0:
            continue
        ratios.append(ms / mo)
        yrs.append(y)
    rec['n_years'] = len(ratios)
    rec['R_AMS'] = float(np.median(ratios)) if ratios else np.nan
    for y, r in zip(yrs, ratios):
        rec[f'ams_{y}'] = r

    # ---- (b) Q1 / Q5 exceedance ------------------------------------------------
    o, s = qo[m], qs[m]
    q1o, q1s = np.quantile(o, 0.99), np.quantile(s, 0.99)
    q5o, q5s = np.quantile(o, 0.95), np.quantile(s, 0.95)
    rec.update(Q1_obs=q1o, Q1_sim=q1s, R_Q1=q1s / q1o if q1o > 0 else np.nan,
               Q5_obs=q5o, Q5_sim=q5s, R_Q5=q5s / q5o if q5o > 0 else np.nan)

    # ---- (c) POT above OBSERVED Q5 --------------------------------------------
    po = pot_peaks(qo, m, q5o)
    ps = pot_peaks(qs, m, q5o)
    rec.update(n_POT_obs=len(po), n_POT_sim=len(ps),
               R_POT=(len(ps) / len(po)) if len(po) else np.nan)

    # ---- (d) timing lag, top-10 observed events (NOT pre-registered) -----------
    top = sorted(po, key=lambda t: -qo[t])[:10]
    lags = {}
    for w in (10, 15, 20):
        L = []
        for t in top:
            lo, hi = max(0, t - w), min(NT, t + w + 1)
            win = np.flatnonzero(m[lo:hi]) + lo
            if win.size == 0:
                continue
            L.append(int(win[np.argmax(qs[win])] - t))
        lags[w] = L
    rec['n_top_events'] = len(top)
    rec['lag_med_abs_d'] = float(np.median(np.abs(lags[LAG_WIN]))) if lags[LAG_WIN] else np.nan
    rec['lag_med_signed_d'] = float(np.median(lags[LAG_WIN])) if lags[LAG_WIN] else np.nan
    rec['lag_med_abs_d_w10'] = float(np.median(np.abs(lags[10]))) if lags[10] else np.nan
    rec['lag_med_abs_d_w20'] = float(np.median(np.abs(lags[20]))) if lags[20] else np.nan

    # ---- per-gauge Pearson r (for the area relationship) -----------------------
    rec['r_pearson'] = float(np.corrcoef(o, s)[0, 1])

    # ---- by-period Q1/Q5/POT/AMS ----------------------------------------------
    for pname, pm in PERIODS:
        mp = m & pm
        if mp.sum() < 90:
            continue
        op, sp = qo[mp], qs[mp]
        p1o, p5o = np.quantile(op, 0.99), np.quantile(op, 0.95)
        rec[f'R_Q1[{pname}]'] = np.quantile(sp, 0.99) / p1o if p1o > 0 else np.nan
        rec[f'R_Q5[{pname}]'] = np.quantile(sp, 0.95) / p5o if p5o > 0 else np.nan
        pyrs = [y for y in yrs if pm[yr == y].any()]
        rr = [rec[f'ams_{y}'] for y in pyrs if f'ams_{y}' in rec]
        rec[f'R_AMS[{pname}]'] = float(np.median(rr)) if rr else np.nan
        npo = pot_peaks(np.where(mp, qo, np.nan), mp, p5o)
        nps = pot_peaks(np.where(mp, qs, np.nan), mp, p5o)
        rec[f'R_POT[{pname}]'] = (len(nps) / len(npo)) if npo else np.nan
    rows.append(rec)

df = pd.DataFrame(rows)
df.to_csv(f'{OUT}/peaks_per_gauge.csv', index=False)

# ---- robustness: raw mask (no gap-fill, no segmentation) -----------------------
raw = []
for g in range(NG):
    m = np.isfinite(QO[:, g])
    qo, qs = QO[:, g], QS[:, g]
    if m.sum() < 300:
        continue
    rr = []
    for y in range(2009, 2019):
        my = m & (yr == y)
        if my.sum() < MIN_YEAR_DAYS:
            continue
        mo = qo[my].max()
        if mo > 0:
            rr.append(qs[my].max() / mo)
    o, s = qo[m], qs[m]
    raw.append({'gauge': str(gc[g]),
                'R_AMS': np.median(rr) if rr else np.nan,
                'R_Q1': np.quantile(s, 0.99) / np.quantile(o, 0.99),
                'R_Q5': np.quantile(s, 0.95) / np.quantile(o, 0.95)})
rawdf = pd.DataFrame(raw)

def q(v):
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    return dict(n=int(v.size), med=float(np.median(v)),
                p25=float(np.percentile(v, 25)), p75=float(np.percentile(v, 75)),
                mean=float(v.mean()))

fleet = {k: q(df[k]) for k in ['R_AMS', 'R_Q1', 'R_Q5', 'R_POT', 'lag_med_abs_d',
                               'lag_med_signed_d', 'n_POT_obs', 'n_POT_sim', 'r_pearson']}
fleet['raw_mask_robustness'] = {k: q(rawdf[k]) for k in ['R_AMS', 'R_Q1', 'R_Q5']}
fleet['POT_totals'] = dict(obs=int(df['n_POT_obs'].sum()), sim=int(df['n_POT_sim'].sum()),
                           ratio=float(df['n_POT_sim'].sum() / df['n_POT_obs'].sum()))
fleet['by_period'] = {}
for pname, _ in PERIODS:
    e = {}
    for stat in ['R_AMS', 'R_Q1', 'R_Q5', 'R_POT']:
        c = f'{stat}[{pname}]'
        if c in df:
            e[stat] = q(df[c])
    fleet['by_period'][pname] = e

# ---- area relationship ---------------------------------------------------------
from scipy import stats
sub = df[np.isfinite(df['R_AMS'])]
la = np.log10(sub['area_km2'].to_numpy())
areastat = {}
for stat in ['R_AMS', 'R_Q1', 'R_Q5', 'R_POT', 'r_pearson', 'lag_med_abs_d']:
    v = sub[stat].to_numpy(float)
    ok = np.isfinite(v)
    rho, p = stats.spearmanr(la[ok], v[ok])
    areastat[stat] = dict(spearman_rho=float(rho), p=float(p), n=int(ok.sum()))
ter = pd.qcut(sub['area_km2'], 3, labels=['small', 'mid', 'large'])
areastat['terciles'] = {}
for lab in ['small', 'mid', 'large']:
    s = sub[ter == lab]
    areastat['terciles'][lab] = dict(
        n=int(len(s)),
        area_min=float(s['area_km2'].min()), area_max=float(s['area_km2'].max()),
        R_AMS=float(np.nanmedian(s['R_AMS'])), R_Q1=float(np.nanmedian(s['R_Q1'])),
        R_Q5=float(np.nanmedian(s['R_Q5'])), R_POT=float(np.nanmedian(s['R_POT'])),
        r_pearson=float(np.nanmedian(s['r_pearson'])),
        lag=float(np.nanmedian(s['lag_med_abs_d'])))
fleet['area'] = areastat
fleet['excluded_gauges'] = excl
fleet['n_gauges_lt_1095_valid_days'] = int(df['lt_1095_days'].sum())
fleet['gauges_lt_1095'] = df.loc[df['lt_1095_days'], 'gauge'].tolist()

# ---- H-PEAK verdict + MUSLE propagation ---------------------------------------
R_AMS = fleet['R_AMS']['med']; R_Q1 = fleet['R_Q1']['med']
ok_ams = 0.85 <= R_AMS <= 1.15
ok_q1 = 0.85 <= R_Q1 <= 1.15
fleet['H_PEAK'] = dict(R_AMS_fleet=R_AMS, R_Q1_fleet=R_Q1,
                       R_AMS_in_band=bool(ok_ams), R_Q1_in_band=bool(ok_q1),
                       verdict='HOLDS' if (ok_ams and ok_q1) else 'REFUTED')
fleet['sediment'] = {
    'beta': BETA_MUSLE,
    'from_R_AMS': dict(R=R_AMS, sed_ratio=float(R_AMS ** BETA_MUSLE),
                       pct=float((R_AMS ** BETA_MUSLE - 1) * 100)),
    'from_R_Q1': dict(R=R_Q1, sed_ratio=float(R_Q1 ** BETA_MUSLE),
                      pct=float((R_Q1 ** BETA_MUSLE - 1) * 100)),
    'ElNino_from_R_AMS': None,
}
en = fleet['by_period'].get('VAL El Nino 15-16', {}).get('R_AMS')
if en:
    fleet['sediment']['ElNino_from_R_AMS'] = dict(
        R=en['med'], sed_ratio=float(en['med'] ** BETA_MUSLE),
        pct=float((en['med'] ** BETA_MUSLE - 1) * 100))

with open(f'{OUT}/peaks_fleet.json', 'w') as f:
    json.dump(fleet, f, indent=2)
print(json.dumps(fleet, indent=2))
