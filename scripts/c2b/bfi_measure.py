"""C2b.1 measurement driver — docs/33 §2.1. Reads frozen artifacts, writes a per-gauge
table + a JSON summary. Touches nothing under sim_calibrated_v2/."""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

REPO = pathlib.Path(r'c:\dev\magdalena-mgb-sed')
sys.path.insert(0, str(REPO / 'src'))
import baseflow as bf  # noqa: E402

PROC = REPO / 'data' / 'processed'
OUT = PROC / 'c2b'
OUT.mkdir(parents=True, exist_ok=True)

d = np.load(PROC / 'model_inputs_v2' / 'discharge.npz', allow_pickle=True)
s = np.load(PROC / 'sim_calibrated_v2' / 'q_gauge_H2E.npz', allow_pickle=True)

cs = d['is_calibration_safe']
assert int(cs.sum()) == 63
assert np.array_equal(d['gauge_code'][cs], s['gauge_code'])
dates = s['dates'].astype('datetime64[D]')
i0 = int(np.searchsorted(d['dates'], dates[0]))
assert np.array_equal(d['dates'][i0:i0 + dates.size], dates)
QV = d['q_valid'][i0:i0 + dates.size][:, cs]
QO = s['q_obs_m3s'].astype(float)
QS = s['q_sim_fit_m3s'].astype(float)
codes = s['gauge_code']
area = s['gauge_upstream_area_km2'].astype(float)
years = dates.astype('datetime64[Y]').astype(int) + 1970
n, G = QO.shape
print('shape', QO.shape, 'valid', int(QV.sum()))

PERIODS = {
    'CAL 2012-14': np.isin(years, [2012, 2013, 2014]),
    'VAL all': ~np.isin(years, [2012, 2013, 2014]),
    'VAL La Nina 11': years == 2011,
    'VAL El Nino 15-16': np.isin(years, [2015, 2016]),
    'VAL other 09/10/17': np.isin(years, [2009, 2010, 2017]),
    'VAL 2018': years == 2018,
}

rows = []
for j in range(G):
    qo, qs, vv = QO[:, j], QS[:, j], QV[:, j]
    k_obs, nseg = bf.master_recession_k(np.where(vv, qo, np.nan))
    a = bf.recession_a(k_obs)
    rec = dict(gauge=codes[j], area_km2=area[j], n_valid_raw=int(vv.sum()),
               k_obs_d=k_obs, n_rec_seg=nseg, a=a)
    if not np.isfinite(a):
        rec['status'] = 'no_recession_constant'
        rows.append(rec)
        continue

    ro = bf.bfi_series(qo, vv, a, bf.BFIMAX)
    rs = bf.bfi_series(qs, vv, a, bf.BFIMAX)          # identical mask, identical filter
    assert np.array_equal(ro['scored'], rs['scored'])
    ro5 = bf.bfi_series(qo, vv, a, bf.BFIMAX_ROBUST)
    rs5 = bf.bfi_series(qs, vv, a, bf.BFIMAX_ROBUST)

    # sensitivity: sim on its OWN values across the <=3 d holes instead of interpolated
    ysim_true = np.where(ro['scored'], qs, np.nan)
    bfi_sim_true = bf.bfi_over(rs['b'], ysim_true, ro['scored'])

    rec.update(status='ok', seg_days=ro['seg_days'], n_scored=ro['n_scored'],
               bfi_obs=ro['bfi'], bfi_sim=rs['bfi'], diff=rs['bfi'] - ro['bfi'],
               bfi_obs_b50=ro5['bfi'], bfi_sim_b50=rs5['bfi'],
               diff_b50=rs5['bfi'] - ro5['bfi'],
               bfi_sim_nofill=bfi_sim_true,
               n_filled=int((ro['scored'] & ~vv).sum()))
    for pname, pm in PERIODS.items():
        m = pm & ro['scored']
        rec[f'bfi_obs|{pname}'] = bf.bfi_over(ro['b'], ro['y'], m)
        rec[f'bfi_sim|{pname}'] = bf.bfi_over(rs['b'], rs['y'], m)
        rec[f'ndays|{pname}'] = int(m.sum())
    rows.append(rec)

df = pd.DataFrame(rows)
df['included'] = (df['status'] == 'ok') & (df['n_scored'].fillna(0) >= bf.MIN_SCORED_DAYS)
df.to_csv(OUT / 'bfi_per_gauge.csv', index=False)
inc = df[df['included']].copy()
print(f'gauges: {len(df)} total, {int(df["included"].sum())} included, '
      f'{int((~df["included"]).sum())} excluded')
print('excluded:', df.loc[~df['included'], ['gauge', 'status', 'n_valid_raw', 'n_scored']]
      .to_string(index=False))


def q(x, p):
    return float(np.nanpercentile(np.asarray(x, float), p))


summ = {}
for tag, co, csm, cd in [('b080', 'bfi_obs', 'bfi_sim', 'diff'),
                         ('b050', 'bfi_obs_b50', 'bfi_sim_b50', 'diff_b50')]:
    o, sm, dd = inc[co].values, inc[csm].values, inc[cd].values
    iqr = q(o, 75) - q(o, 25)
    p1090 = q(o, 90) - q(o, 10)
    med_abs = float(np.nanmedian(np.abs(dd)))
    summ[tag] = dict(
        n=int(len(inc)),
        med_bfi_obs=float(np.nanmedian(o)), med_bfi_sim=float(np.nanmedian(sm)),
        iqr_obs=iqr, p25_obs=q(o, 25), p75_obs=q(o, 75),
        p10_obs=q(o, 10), p90_obs=q(o, 90), p10_90_obs=p1090,
        sd_obs=float(np.nanstd(o, ddof=1)),
        iqr_sim=q(sm, 75) - q(sm, 25), p10_90_sim=q(sm, 90) - q(sm, 10),
        sd_sim=float(np.nanstd(sm, ddof=1)),
        med_abs_diff=med_abs, med_signed_diff=float(np.nanmedian(dd)),
        iqr_diff=q(dd, 75) - q(dd, 25),
        n_sim_gt_obs=int((dd > 0).sum()), n_sim_lt_obs=int((dd < 0).sum()),
        max_abs_diff=float(np.nanmax(np.abs(dd))),
        gauge_max_abs=str(inc['gauge'].values[int(np.nanargmax(np.abs(dd)))]),
        n_gauge_abs_gt_iqr=int((np.abs(dd) > iqr).sum()),
        n_gauge_abs_gt_020=int((np.abs(dd) > 0.20).sum()),
        verdict_refuted=bool(med_abs > iqr),
    )

# by period
per = {}
for pname in PERIODS:
    o = inc[f'bfi_obs|{pname}'].values
    sm = inc[f'bfi_sim|{pname}'].values
    dd = sm - o
    per[pname] = dict(
        n_gauges=int(np.isfinite(dd).sum()),
        med_days=float(np.nanmedian(inc[f'ndays|{pname}'].values)),
        med_bfi_obs=float(np.nanmedian(o)), med_bfi_sim=float(np.nanmedian(sm)),
        iqr_obs=q(o, 75) - q(o, 25), p10_90_obs=q(o, 90) - q(o, 10),
        med_abs_diff=float(np.nanmedian(np.abs(dd))),
        med_signed_diff=float(np.nanmedian(dd)),
        would_refute=bool(float(np.nanmedian(np.abs(dd))) > (q(o, 75) - q(o, 25))),
    )
summ['by_period'] = per
summ['k_obs'] = dict(med=float(np.nanmedian(inc['k_obs_d'])),
                     p10=q(inc['k_obs_d'], 10), p90=q(inc['k_obs_d'], 90),
                     med_a=float(np.nanmedian(inc['a'])))
summ['sensitivity_nofill'] = dict(
    med_abs_delta=float(np.nanmedian(np.abs(inc['bfi_sim_nofill'] - inc['bfi_sim']))),
    max_abs_delta=float(np.nanmax(np.abs(inc['bfi_sim_nofill'] - inc['bfi_sim']))),
    med_filled_days=float(np.nanmedian(inc['n_filled'])))
summ['internal_partition'] = dict(
    surface=0.513, subsurface=0.292, baseflow=0.195,
    med_bfi_sim=summ['b080']['med_bfi_sim'],
    gap=summ['b080']['med_bfi_sim'] - 0.195,
    n_gauges_bfi_sim_below_0195=int((inc['bfi_sim'] < 0.195).sum()))
# area correlation of the difference
fa = np.log10(inc['area_km2'].values)
summ['area'] = dict(
    r_diff_logarea=float(np.corrcoef(fa, inc['diff'].values)[0, 1]),
    r_bfiobs_logarea=float(np.corrcoef(fa, inc['bfi_obs'].values)[0, 1]),
    r_bfisim_logarea=float(np.corrcoef(fa, inc['bfi_sim'].values)[0, 1]),
    med_abs_diff_small=float(np.nanmedian(np.abs(
        inc['diff'].values[inc['area_km2'].values < np.median(inc['area_km2'])]))),
    med_abs_diff_large=float(np.nanmedian(np.abs(
        inc['diff'].values[inc['area_km2'].values >= np.median(inc['area_km2'])]))))

(OUT / 'bfi_summary.json').write_text(json.dumps(summ, indent=2), encoding='utf-8')
print(json.dumps(summ, indent=2))
