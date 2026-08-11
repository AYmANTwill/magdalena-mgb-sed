import json
import pathlib

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm

REPO = pathlib.Path(r'c:\dev\magdalena-mgb-sed')
OUT = REPO / 'figures' / 'deck' / 'gen_bfi.png'
OUT.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(REPO / 'data/processed/c2b/bfi_per_gauge.csv')
S = json.load(open(REPO / 'data/processed/c2b/bfi_summary.json'))
inc = df[df.included].copy()
o, s = inc.bfi_obs.values, inc.bfi_sim.values
d = inc['diff'].values
A = inc.area_km2.values
iqr = S['b080']['iqr_obs']
mad = S['b080']['med_abs_diff']

plt.rcParams.update({'font.size': 9, 'axes.labelsize': 9.5, 'axes.titlesize': 10.5,
                     'figure.facecolor': 'white', 'axes.facecolor': 'white'})
fig = plt.figure(figsize=(13.0, 5.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.30], wspace=0.30,
                      left=0.055, right=0.985, top=0.855, bottom=0.145)

# ---------------- panel A : scatter vs 1:1
ax = fig.add_subplot(gs[0, 0])
lo, hi = 0.63, 0.815
ax.fill_between([lo, hi], [lo - iqr, hi - iqr], [lo + iqr, hi + iqr],
                color='#c8d8e8', alpha=0.55, lw=0, zorder=0,
                label=f'± IQR(BFI$_{{obs}}$) = ±{iqr:.3f}\n(the H-BFI yardstick)')
ax.plot([lo, hi], [lo, hi], color='#333333', lw=1.2, zorder=2, label='1:1')
sc = ax.scatter(o, s, c=A, cmap='viridis', norm=LogNorm(vmin=A.min(), vmax=A.max()),
                s=46, edgecolor='white', lw=0.6, zorder=3)
ax.axhline(0.80, color='#b03a2e', lw=1.0, ls=':', zorder=1)
ax.text(lo + 0.004, 0.8015, 'BFI$_{max}$ = 0.80  (the filter ceiling)',
        color='#b03a2e', fontsize=7.8, va='bottom')
ax.set_xlim(lo, hi)
ax.set_ylim(lo, hi)
ax.set_aspect('equal')
ax.set_xlabel('BFI observed  (Eckhardt, BFI$_{max}$ = 0.80, per-gauge $a$)')
ax.set_ylabel('BFI simulated  (identical filter, identical days)')
ax.set_title(f'A.  Flow character, gauge by gauge  (n = {len(inc)})', loc='left')
ax.legend(loc='lower right', fontsize=7.6, framealpha=0.95)
ax.grid(alpha=0.25, lw=0.5)
cb = fig.colorbar(sc, ax=ax, pad=0.02, fraction=0.042)
cb.set_label('upstream area (km²)', fontsize=8, labelpad=2)
cb.ax.tick_params(labelsize=7.5)
ax.text(0.03, 0.965,
        f'median obs {S["b080"]["med_bfi_obs"]:.3f}   median sim '
        f'{S["b080"]["med_bfi_sim"]:.3f}\nr(sim, obs) across gauges = '
        f'{np.corrcoef(o, s)[0, 1]:.2f}',
        transform=ax.transAxes, va='top', fontsize=7.8,
        bbox=dict(boxstyle='round,pad=0.35', fc='white', ec='#bbbbbb', lw=0.6))

# ---------------- panel B : ranked per-gauge difference
ax2 = fig.add_subplot(gs[0, 1])
order = np.argsort(d)
x = np.arange(len(d))
cols = plt.cm.viridis(LogNorm(vmin=A.min(), vmax=A.max())(A[order]))
ax2.axhspan(-iqr, iqr, color='#c8d8e8', alpha=0.55, lw=0, zorder=0)
ax2.bar(x, d[order], color=cols, edgecolor='white', lw=0.35, width=0.86, zorder=2)
ax2.axhline(0, color='#333333', lw=1.0, zorder=3)
for y, lab in ((iqr, f'+IQR {iqr:+.3f}'), (-iqr, f'−IQR {-iqr:.3f}')):
    ax2.axhline(y, color='#4a6f96', lw=0.9, ls='--', zorder=3)
    ax2.text(11.0, y, '  ' + lab, color='#2c4b6b', fontsize=7.4,
             va='bottom' if y > 0 else 'top', ha='left')
ax2.set_xlim(-1, len(d))
ax2.set_xticks(x)
ax2.set_xticklabels(inc.gauge.values[order].astype(str), rotation=90, fontsize=5.2)
ax2.set_xlabel('gauge (ranked by difference; colour = upstream area, as panel A)')
ax2.set_ylabel('BFI$_{sim}$ − BFI$_{obs}$')
ax2.set_title('B.  Per-gauge difference against the pre-registered yardstick', loc='left')
ax2.grid(axis='y', alpha=0.25, lw=0.5)
n_out = int((np.abs(d) > iqr).sum())
ax2.text(0.015, 0.97,
         f'fleet median |Δ| = {mad:.4f}   vs   IQR(BFI$_{{obs}}$) = {iqr:.4f}\n'
         f'{n_out} of {len(d)} gauges individually outside ±IQR;   '
         f'{int((d > 0).sum())} of {len(d)} run too slow (sim > obs)',
         transform=ax2.transAxes, va='top', fontsize=7.8,
         bbox=dict(boxstyle='round,pad=0.35', fc='white', ec='#bbbbbb', lw=0.6))

fig.suptitle(
    'C2b.1  H-BFI — does the model split water the way the rivers do?      '
    f'VERDICT: NOT REFUTED  (median |Δ| {mad:.4f} ≤ IQR {iqr:.4f})',
    x=0.06, ha='left', fontsize=11.5, weight='bold', y=0.965)
fig.text(0.06, 0.917,
         'Eckhardt two-parameter filter, docs/33 §2.1 frozen spec: BFI$_{max}$ = 0.80 '
         'fixed (not fitted), a = exp(−1/k) from the OBSERVED master recession curve, '
         'same a and same days for both series, 2009–2018 scored.',
         ha='left', fontsize=7.9, color='#444444')
fig.savefig(OUT, dpi=170)
print('wrote', OUT, OUT.stat().st_size, 'bytes')
