"""Shared machinery for notebook 14's pre-registered calibration cells.

WHY THIS IS A MODULE AND NOT NOTEBOOK CODE
------------------------------------------
Notebook 14 runs two pre-registered cells:

    H1 = v1 forcing + the NEW objective    -> isolates the objective change
    H2 = v2 forcing + the NEW objective    -> isolates the zero-suppression repair

A third pre-registered cell was added after the H1/H2 verdict (docs/26):

    H2E = H2 + FAO-56 threshold ET stress  -> isolates the ET stress function
          (et_stress='fao56', theta_crit FIXED at 0.6 - not searched; hypothesis:
          kc_mult comes off its ~2.0 rail at no material cost in F)

with two DDS seeds each.  Four independent searches, each ~1 core.  They are run
CONCURRENTLY with `concurrent.futures.ProcessPoolExecutor`, and on Windows that means
`spawn`: the worker entry point has to be importable from a module, not defined in a
notebook cell.  Putting the objective here also guarantees the notebook's reporting code
and the workers' search code are literally the same functions - if they drifted, the
reported F would not be the F that was optimised.

The parallelism is spent on BUDGET, not on wall time: four concurrent searches at the
same wall clock as one sequential pair means each seed gets roughly four times the
evaluations the v1 run had.

WHAT CHANGED IN THE OBJECTIVE, AND WHY (docs/18 s5 item 3, docs/22 s4.4 and s4.6)
---------------------------------------------------------------------------------
1. `k_bas` lower bound 15 d -> 5 d.  The observed low-flow recession constant is
   13.9 d at the fleet median (p10 7.7 d), so the v1 search space EXCLUDED the right
   answer.  A bound that excludes the observation is not a prior, it is a mistake.
2. `k_int < k_bas` is imposed by construction, not by rejection.  The v1 fit put
   `k_int` at 117.4 d against `k_bas` 68.6 d - interflow slower than groundwater, which
   is physically inverted.  Rather than reject proposals (which piles probability mass on
   the constraint surface and breaks DDS's reflection), the search variable is the RATIO
   `k_int_frac = k_int / k_bas` on (0.02, 0.90).  Every point in the box satisfies the
   constraint, so the constraint costs nothing and cannot be violated.
   The prior maps exactly: 8 / 60 = 0.13333..., so `RAW_P0` still reproduces nb13.
3. A recession-signature term is added.  Morris put `mu*` for `k_bas` at 0.044, rank 5
   of 10 - the daily-KGE objective barely sees the store time-scales, so the v1 fit for
   them was the prior carried through, and the simulated recession came out 3-4x too slow
   in EVERY period.  The new term scores each gauge on the log-ratio of its simulated to
   its observed recession constant, so the stores are constrained by a signature the data
   actually contains rather than by a metric that cannot see them.

WHAT CHANGED FOR STAGE C2b (docs/33 s3.1 and s3.2)
--------------------------------------------------
4. A PEAK-signature term is added, and it is added because a pre-registered measurement
   refuted H-PEAK: the fleet-median annual-maximum ratio `R_AMS` came out 0.820 and the
   Q1-exceedance ratio 0.847, both below the frozen [0.85, 1.15] bound, on the low side
   exactly as docs/26 s A.4's alpha 0.90-0.92 predicted.  H-BFI was measured at the same
   time and HOLDS (fleet-median |BFI_sim - BFI_obs| 0.01625 <= IQR(BFI_obs) 0.02845), so
   docs/33 s3.1's outcome table resolves on its third row: **the peak term only**, at the
   weight vector (0.34, 0.34, 0.17, 0.15).  The BFI term of docs/33 s3.2 is NOT triggered
   and is deliberately NOT wired into this objective - `src/baseflow.py` stays a
   measurement module.  Adding an untriggered term would be inventing a cell.

   The term is `e_peak = 1 - |ln R_AMS| / ln(1.5)`, symmetric in log space for the same
   reason the recession term is: a peak 1.5x too high must cost exactly what one 1.5x too
   low costs, or the objective quietly encodes a preferred direction.  `R_AMS` per gauge
   is the MEDIAN over calendar years of `Qmax_sim,y / Qmax_obs,y`, over years with
   >= 300 valid days, on the PAIRED day set (the simulation is masked to the observed
   validity mask before its annual maximum is taken - otherwise a simulated peak on a day
   the gauge never reported could enter the ratio).  Both scales, the 300-day rule and the
   weights were frozen in docs/33 before any C2b number existed; none is derived from data.

   Everything about the incumbent objective is left alone.  `W_KGE`, `W_LOG`, `W_REC`
   still read 0.40 / 0.40 / 0.20 and `blend`'s default weight vector is still the
   incumbent 3-tuple, so a cell that does not ask for the peak term computes exactly the
   F it computed before.  That is a gate, not a hope: it was verified by recomputing
   H2E's stored best vector with the peak term PRESENT at weight zero and requiring the
   result to reproduce F = 0.25930593639066796 to <= 1e-10 relative
   (docs/agents/journal_refit-launch.md, step 3; measured relative difference 0.0).

Rejected alternatives for term 3, and why:
  * a hard penalty / constraint on `k_bas` itself.  Rejected: the recession the gauge sees
    is a property of the whole store cascade plus routing, not of one parameter, so
    constraining the parameter would be asserting the mechanism instead of measuring the
    signature.
  * matching the simulated recession on the OBSERVED recession windows.  Rejected: it
    makes the statistic conditional on the observed timing being right, and it is not what
    docs/22 s4.4 measured, so the resulting numbers would not be comparable to the 3-4x
    already on record.
  * a squared-error penalty on (k_sim - k_obs).  Rejected: it is scale-dependent, so a
    slow gauge would dominate; the log-ratio is the scale-free statement of "a factor of
    two out".
"""
from __future__ import annotations

import json
import os
import pathlib

import numpy as np
import pandas as pd

# One thread per worker.  Four concurrent searches x numba's default thread pool would
# oversubscribe a 12-core machine and make every search slower than running them serially.
for _v in ('NUMBA_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
           'OPENBLAS_NUM_THREADS'):
    os.environ.setdefault(_v, '1')

REPO = pathlib.Path(__file__).resolve().parents[1]
PROC = REPO / 'data' / 'processed'
CACHE = PROC / '_calib_cache'

# ============================================================ the parameter space
NAMES = ['adr', 'fint', 'b', 'wm_mult', 'kc_mult', 'lai_mult',
         'k_sup', 'k_int_frac', 'k_bas', 'celerity']
IS_LOG = np.array([True, False, True, True, False, False, True, True, True, True])
#                  adr    fint   b     wm    kc    lai   k_sup k_frac k_bas  cel
RAW_LO = np.array([5e-4, 0.05, 0.05, 0.25, 0.50, 0.0, 0.20, 0.02, 5.0, 0.05])
RAW_HI = np.array([0.30, 0.95, 4.00, 6.00, 2.00, 5.0, 20.0, 0.90, 600.0, 4.00])
RAW_P0 = np.array([0.06, 0.60, 0.60, 1.00, 1.00, 1.0, 1.50, 8.0 / 60.0, 60.0, 1.00])

# inherited from the v1 Morris screening (sim_calibrated/calibration.json), NOT re-derived:
# re-running Morris for both cells would cost ~15 % of the search budget to reproduce a
# ranking that is already on record, and the screening is a property of the model and the
# gauge network, not of the objective being changed here.
REG_PARAMS = ['k_sup', 'wm_mult', 'celerity']
SOIL_PARAMS = ['adr']

# objective weights.  They sum to 1, so F(perfect) = 1 exactly, as in v1.
W_KGE, W_LOG, W_REC = 0.40, 0.40, 0.20
REC_SCALE = float(np.log(2.0))      # a factor of two out scores exactly zero

# --- the C2b peak signature (docs/33 s3.2), FROZEN there before any C2b number existed --
PEAK_SCALE = float(np.log(1.5))     # a peak 1.5x out EITHER way scores exactly zero
AMS_MIN_DAYS = 300                  # docs/33 s2.3a: a year needs >= 300 valid days
W_PEAK = 0.15                       # a new term takes 0.15, drawn proportionally
# docs/33 s3.2, row "H-PEAK refuted only": each incumbent weight x (1 - 0.15), i.e.
# 0.40 x 0.85 = 0.34 and 0.20 x 0.85 = 0.17.  Written as the literals the table quotes,
# not as the products, so the numbers in the code are the numbers in the frozen document.
W_SET_PEAK = (0.34, 0.34, 0.17, W_PEAK)
W_SET_INCUMBENT = (W_KGE, W_LOG, W_REC)
assert abs(sum(W_SET_PEAK) - 1.0) < 1e-12, 'the refit weights must still sum to 1'

CAL_YEARS = [2012, 2013, 2014]
SEARCH_WU_YEAR = 2011
ANCHOR_EXCLUDE = '29037020'         # the outlet: it cannot be a region anchor

CELLS = {
    'H1': dict(bundle='model_inputs', label='H1  v1 forcing + new objective',
               scored=('2009-01-01', '2017-12-31')),
    'H2': dict(bundle='model_inputs_v2', label='H2  v2 forcing + new objective',
               scored=('2009-01-01', '2018-12-31')),
    # H2E = H2 + the FAO-56 threshold ET stress (mgb_hydrology et_stress='fao56'),
    # theta_crit FIXED at 0.6, not searched - one change at a time, so any movement in
    # kc_mult is attributable to the functional form alone.  Pre-registered hypothesis
    # (docs/22 s4.6, docs/26 s5.1): with the threshold form, kc_mult comes off its rail
    # (< 90 % of range; H1 hit 1.98, H2 1.90 of [0.5, 2.0]) at no material cost in F.
    # `cache='H2'`: bundle and period are identical to H2, so the cell READS H2's
    # forcing cache instead of writing a duplicate ~100 MB copy into _calib_cache.
    'H2E': dict(bundle='model_inputs_v2', label='H2E v2 forcing + new objective + FAO-56 ET',
                scored=('2009-01-01', '2018-12-31'), cache='H2',
                et_stress='fao56', theta_crit=0.6),
    # H2E-S = H2E + the C2b PEAK signature term, and NOTHING else (docs/33 s3.3: forcing,
    # ET, parameter box, gauges, split, algorithm and budget all identical to H2E; only
    # the objective gains a term).  Registered here so a phase-3 session cannot invent a
    # cell: docs/33 s3.3 authorises this cell and no other, at seeds 20260907/20260908 and
    # budget 1000.  `use_peak` is separate from the weight on purpose - it lets the peak
    # term be COMPUTED at weight zero, which is what makes the "did I extend the objective
    # or change it?" gate a real test rather than a tautology.
    'H2E-S': dict(bundle='model_inputs_v2',
                  label='H2E-S v2 + FAO-56 ET + C2b peak signature term',
                  scored=('2009-01-01', '2018-12-31'), cache='H2',
                  et_stress='fao56', theta_crit=0.6,
                  use_peak=True, weights=W_SET_PEAK),
}
WU_SPAN = ('2008-01-01', '2008-12-31')


def fwd(v, lg):
    return np.where(lg, np.log(np.maximum(v, 1e-300)), v)


def inv(x, lg):
    return np.where(lg, np.exp(x), x)


LO, HI, X0 = fwd(RAW_LO, IS_LOG), fwd(RAW_HI, IS_LOG), fwd(RAW_P0, IS_LOG)
assert np.all(LO < X0) and np.all(X0 < HI), 'a prior sits on or outside its own range'


# ============================================================ metrics
def kge_terms(sim, obs):
    """KGE = 1 - sqrt((r-1)^2+(alpha-1)^2+(beta-1)^2), plus NSE and PBIAS.

    Identical to notebook 14 v1's `kge_terms`, deliberately: the whole point of H1 is
    that only the OBJECTIVE changed, so the metric underneath it must not.
    """
    sim = np.asarray(sim, dtype=float)
    obs = np.asarray(obs, dtype=float)
    m = np.isfinite(sim) & np.isfinite(obs)
    s, o = sim[m], obs[m]
    out = dict(n=int(s.size), r=np.nan, alpha=np.nan, beta=np.nan, kge=np.nan,
               nse=np.nan, pbias=np.nan)
    if s.size < 30:
        return out
    ss, so, mo = s.std(ddof=1), o.std(ddof=1), o.mean()
    if so > 0:
        out['alpha'] = float(ss / so)
        if ss > 1e-12 * so:          # relative guard: a flat-to-roundoff sim has no r
            out['r'] = float(np.corrcoef(s, o)[0, 1])
    if mo > 0:
        out['beta'] = float(s.mean() / mo)
        out['pbias'] = float(100.0 * (s.sum() - o.sum()) / o.sum())
    if np.all(np.isfinite([out['r'], out['alpha'], out['beta']])):
        out['kge'] = float(1 - np.sqrt((out['r'] - 1) ** 2 + (out['alpha'] - 1) ** 2
                                       + (out['beta'] - 1) ** 2))
    den = float(((o - mo) ** 2).sum())
    if den > 0:
        out['nse'] = float(1 - ((s - o) ** 2).sum() / den)
    return out


def c2m(k):
    """Mathevet et al. (2006) bounded transform: strictly increasing, B(1)=1, B(0)=0,
    B(-inf)=-1.  Keeps one hopeless gauge from dominating a fleet mean without
    discarding it."""
    k = np.asarray(k, dtype=float)
    return k / (2.0 - k)


def recession_k(q, min_pts=3, low_pct=40.0):
    """Linear-reservoir constant from monotone declines below the low_pct-th flow
    percentile, as docs/22 s4.4 defines it.

    A decline DAY is a day t whose flow is finite, strictly below its predecessor, and
    below the series' own low_pct-th percentile.  A SEGMENT is a maximal run of
    consecutive decline days together with the day before it (the peak the recession
    starts from), and is used only if it holds >= min_pts points.  On each segment
    ln Q is fitted against day number by ordinary least squares in closed form and
    k = -1/slope.  The gauge's constant is the MEDIAN over its segments: recession
    lengths are heavy-tailed and one long dry spell would otherwise set the answer.

    Returns (k_days, n_segments); k is NaN when nothing qualifies.
    """
    q = np.asarray(q, dtype=float)
    n = q.size
    fin = np.isfinite(q) & (q > 0)
    if int(fin.sum()) < 60:
        return np.nan, 0
    thr = float(np.percentile(q[fin], low_pct))
    lq = np.where(fin, np.log(np.maximum(q, 1e-300)), np.nan)
    dec = np.zeros(n, dtype=bool)
    dec[1:] = fin[1:] & fin[:-1] & (q[1:] < q[:-1]) & (q[1:] < thr)
    ks = []
    i = 1
    while i < n:
        if not dec[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and dec[j + 1]:
            j += 1
        npts = j - i + 2                     # + the pre-decline point at i-1
        if npts >= min_pts:
            y = lq[i - 1: j + 1]
            if np.all(np.isfinite(y)):
                t = np.arange(npts, dtype=float)
                tb = t.mean()
                sl = float(((t - tb) * (y - y.mean())).sum() / ((t - tb) ** 2).sum())
                if sl < 0:
                    ks.append(-1.0 / sl)
        i = j + 1
    if not ks:
        return np.nan, 0
    return float(np.median(ks)), len(ks)


def recession_fleet(Q, cols=None):
    """recession_k over the columns of a (time, gauge) matrix."""
    Q = np.asarray(Q)
    out = np.full(Q.shape[1], np.nan)
    nseg = np.zeros(Q.shape[1], dtype=int)
    rng = range(Q.shape[1]) if cols is None else cols
    for j in rng:
        out[j], nseg[j] = recession_k(Q[:, j])
    return out, nseg


def rec_efficiency(k_sim, k_obs):
    """1 at a perfect match, 0 at a factor of two either way, negative beyond.

    Symmetric in log space on purpose: a recession twice too fast is exactly as wrong as
    one twice too slow, and the v1 defect (3-4x too SLOW) must not be scored on a
    yardstick that only punishes one direction.
    """
    k_sim = np.asarray(k_sim, dtype=float)
    k_obs = np.asarray(k_obs, dtype=float)
    with np.errstate(divide='ignore', invalid='ignore'):
        rat = np.where((k_sim > 0) & (k_obs > 0), k_sim / k_obs, np.nan)
        return 1.0 - np.abs(np.log(rat)) / REC_SCALE


def ams_fleet(Q, years, min_days=AMS_MIN_DAYS):
    """Annual maximum series of every column of a (time, gauge) matrix, docs/33 s2.3a.

    A calendar year contributes its maximum only if that gauge has at least `min_days`
    FINITE days in it; otherwise the year is NaN and drops out of the ratio.  The rule is
    on the number of valid days, not on the number of calendar days, because a gauge that
    reported for two months of a year has not observed that year's flood and its
    "annual maximum" would be a within-year maximum masquerading as one.

    Returns (ams, years_used) with `ams` of shape (n_year, n_gauge).
    """
    Q = np.asarray(Q, dtype=float)
    years = np.asarray(years)
    uy = np.unique(years)
    out = np.full((uy.size, Q.shape[1]), np.nan)
    for i, y in enumerate(uy):
        blk = Q[years == y]
        fin = np.isfinite(blk)
        cnt = fin.sum(axis=0)
        # max over the finite entries only; -inf is never selected where cnt > 0, and
        # the cnt >= min_days test discards the column before the -inf could escape.
        mx = np.max(np.where(fin, blk, -np.inf), axis=0)
        out[i] = np.where(cnt >= min_days, mx, np.nan)
    return out, uy


def ams_ratio(ams_sim, ams_obs):
    """R_AMS per gauge = MEDIAN over years of Qmax_sim,y / Qmax_obs,y (docs/33 s2.3a).

    The median, not the mean, for the same reason `recession_k` takes one over segments:
    a single year in which the gauge's own maximum is suspect would otherwise set the
    gauge's answer.  A gauge with no usable year is NaN and `blend` renormalises it away
    rather than crediting it a zero.
    """
    ams_sim = np.asarray(ams_sim, dtype=float)
    ams_obs = np.asarray(ams_obs, dtype=float)
    with np.errstate(divide='ignore', invalid='ignore'):
        rat = np.where((ams_sim > 0) & (ams_obs > 0), ams_sim / ams_obs, np.nan)
    out = np.full(rat.shape[1], np.nan)
    for j in range(rat.shape[1]):
        col = rat[:, j]
        ok = np.isfinite(col)
        if ok.any():
            out[j] = float(np.median(col[ok]))
    return out


def peak_efficiency(r_ams):
    """1 at a perfect annual-maximum match, 0 at 1.5x either way, negative beyond.

    docs/33 s3.2: e_peak = 1 - |ln R_AMS| / ln(1.5).  Symmetric in log space on purpose -
    an over-predicted peak is exactly as damaging to a sediment claim as an under-predicted
    one, even though docs/26 s A.4's alpha 0.90-0.92 makes the low side the expected
    failure and the C2b measurement found it there (R_AMS 0.820).
    """
    r = np.asarray(r_ams, dtype=float)
    with np.errstate(divide='ignore', invalid='ignore'):
        rr = np.where(r > 0, r, np.nan)
        return 1.0 - np.abs(np.log(rr)) / PEAK_SCALE


def blend(k1, k2, e_rec=None, sel=None,
          w=(W_KGE, W_LOG, W_REC), use_rec=True, e_peak=None, use_peak=False):
    """The fleet objective.

        F = mean over gauges of  sum_t w_t * C2M(score_t)  /  sum_t w_t

    where t runs over {KGE(Q), KGE(log Q), recession, peak} and the sum is taken over the
    terms that are DEFINED at that gauge, with the weights renormalised.  A gauge with no
    usable recession is therefore scored on its two KGE terms alone rather than being
    dropped or silently credited with a zero.

    `use_rec=False` reproduces the v1 objective exactly at w=(0.5, 0.5, 0), which is what
    makes the old and new numbers comparable in the report.

    THE PEAK TERM IS OPT-IN AND OFF BY DEFAULT.  `use_peak=False` and the default
    3-element `w` mean every existing caller - notebook 14's identity checks, the H1/H2/H2E
    cells, the report - computes exactly the number it computed before docs/33 existed.
    The peak weight is `w[3]`, and a 3-element `w` gives it weight 0.0, so the incumbent
    weight vector cannot accidentally acquire a fourth term.  This is the same "keep the
    old function on one axis" discipline as `blend_v1` below, applied to the new term.
    """
    k1 = np.asarray(k1, dtype=float)
    k2 = np.asarray(k2, dtype=float)
    terms = [c2m(k1), c2m(k2)]
    ws = [w[0], w[1]]
    if use_rec and e_rec is not None:
        terms.append(c2m(np.asarray(e_rec, dtype=float)))
        ws.append(w[2])
    if use_peak and e_peak is not None:
        terms.append(c2m(np.asarray(e_peak, dtype=float)))
        ws.append(w[3] if len(w) > 3 else 0.0)
    V = np.stack(terms, 0)
    W = np.array(ws, dtype=float)[:, None] * np.ones_like(V)
    ok = np.isfinite(V)
    W = np.where(ok, W, 0.0)
    num = np.nansum(np.where(ok, V, 0.0) * W, axis=0)
    den = W.sum(axis=0)
    per_gauge = np.where(den > 0, num / np.maximum(den, 1e-30), np.nan)
    if sel is not None:
        per_gauge = per_gauge[sel]
    good = np.isfinite(per_gauge)
    return float(per_gauge[good].mean()) if good.any() else np.nan


def blend_v1(k1, k2, w=0.5, sel=None):
    """The v1 objective, reproduced EXACTLY, including its NaN handling.

    v1 formed v = (1-w)*C2M(k1) + w*C2M(k2) per gauge - which is NaN if EITHER term is -
    and averaged the finite entries.  The new `blend` instead renormalises over the terms
    that exist, so a gauge with a usable log-KGE but no plain KGE still contributes.  That
    is a better rule, but it is a DIFFERENT rule, so the old function is kept verbatim: it
    is the only way to put the new cells on the same axis as the F = 0.2429 already on
    record for Config B, and a re-derived "old" number that did not reproduce
    F(prior) = 0.1276369667 would mean the comparison was never like-for-like.
    """
    v = (1 - w) * c2m(np.asarray(k1, float)) + w * c2m(np.asarray(k2, float))
    if sel is not None:
        v = v[sel]
    ok = np.isfinite(v)
    return float(v[ok].mean()) if ok.any() else np.nan


def doy_climatology(Q, dates):
    """Day-of-year climatology of each column, built from the WHOLE record.

    Keyed on (month, day), not day-of-year: doy 60 is 29-Feb in a leap year and 1-Mar
    otherwise, so a doy key shifts most of every leap year by one calendar day.  The
    29-Feb bin is fed by the leap years present and nothing else.
    Mean, not median: this is the benchmark a hydrologist would actually have to beat,
    and the conventional seasonal-climatology benchmark is the mean.
    """
    d = pd.DatetimeIndex(dates)
    key = np.asarray(d.month) * 100 + np.asarray(d.day)
    uk = np.unique(key)
    Q = np.asarray(Q, dtype=float)
    clim = np.empty((uk.size, Q.shape[1]))
    import warnings as _w
    with _w.catch_warnings():
        # a (gauge, month-day) bin with no observation in any year yields NaN, which is
        # the right answer - the benchmark simply has nothing to say on that day. numpy
        # warns about the empty slice; the NaN is intended, so the warning is suppressed
        # rather than the NaN being filled with something invented.
        _w.simplefilter('ignore', RuntimeWarning)
        for i, k in enumerate(uk):
            clim[i] = np.nanmean(Q[key == k], axis=0)
    return clim[np.searchsorted(uk, key)]


# ============================================================ DDS
def dds(fun, x0, lo, hi, budget, seed, r_pert=0.2, log=None,
        replay=None, checkpoint=None, every=25):
    """Dynamically Dimensioned Search with exact, verified resumption.

    RESUMPTION, and why it is exact rather than approximate.  These searches are long
    enough that a killed process must not cost the work already done, but a naive restart
    would draw a different random stream and stop being the same search.  Instead the RNG
    is re-created from the same seed and the first `len(replay)` iterations are replayed
    with their STORED objective values in place of calling `fun`, so every draw, every
    acceptance and every best-so-far is reproduced exactly.  The replay is not trusted:
    each replayed proposal is compared with the stored parameter vector and a mismatch
    raises, so a resume from a checkpoint written by different code, a different seed or a
    different budget fails loudly instead of silently continuing a different search.
    (`budget` enters the perturbation probability p = 1 - ln i / ln M, so resuming with a
    different budget really would be a different search.)
    """
    """Dynamically Dimensioned Search (Tolson & Shoemaker 2007), MAXIMISING.

    Unchanged from notebook 14 v1 so the search algorithm is not a confound in H1.
    Out-of-range proposals are reflected, not clipped: clipping piles probability mass on
    the bound and would make a boundary optimum look like a real one.
    """
    rng = np.random.default_rng(seed)
    x0 = np.asarray(x0, float).copy()
    lo = np.asarray(lo, float)
    hi = np.asarray(hi, float)
    d = x0.size
    rx, rf, rex = (replay if replay is not None else (None, None, None))
    n_replay = 0 if rx is None else len(rf)
    if n_replay:
        print(f'    resuming: replaying {n_replay} stored evaluations', flush=True)

    xb = x0.copy()
    if n_replay:
        assert np.allclose(rx[0], xb, rtol=0, atol=1e-12), 'checkpoint start point differs'
        fb, extra = float(rf[0]), rex[0]
    else:
        fb, extra = fun(xb)
    arch = [(xb.copy(), fb, extra)]
    hist = [fb]
    for i in range(1, budget):
        p = 1.0 - np.log(i) / np.log(budget)
        J = np.flatnonzero(rng.random(d) < p)
        if J.size == 0:
            J = np.array([rng.integers(d)])
        xn = xb.copy()
        for j in J:
            xn[j] = xb[j] + r_pert * (hi[j] - lo[j]) * rng.standard_normal()
            if xn[j] < lo[j]:
                xn[j] = lo[j] + (lo[j] - xn[j])
                if xn[j] > hi[j]:
                    xn[j] = lo[j]
            elif xn[j] > hi[j]:
                xn[j] = hi[j] - (xn[j] - hi[j])
                if xn[j] < lo[j]:
                    xn[j] = hi[j]
        if i < n_replay:
            assert np.allclose(rx[i], xn, rtol=0, atol=1e-10), (
                f'replay diverged at evaluation {i} - the checkpoint was written by a '
                f'different seed, budget or code path; refusing to continue a different '
                f'search')
            fn, extra = float(rf[i]), rex[i]
        else:
            fn, extra = fun(xn)
        arch.append((xn.copy(), fn, extra))
        if fn > fb:
            xb, fb = xn, fn
        hist.append(fb)
        if i >= n_replay and checkpoint is not None and (i % every == 0
                                                         or i == budget - 1):
            checkpoint(arch)
        if log and (i % log == 0 or i == budget - 1):
            print(f'    eval {i+1:5d}/{budget}  best {fb:.5f}  p_pert {p:.3f}', flush=True)
    return dict(x=xb, f=fb, hist=np.array(hist), archive=arch)


# ============================================================ the cell context
class Cell:
    """Everything one pre-registered cell needs, loaded once per process.

    The forcing arrives as a memory-mapped .npy (see `ensure_cache`), so four concurrent
    workers share one copy of each field through the OS page cache instead of holding four.
    Only the days a given run needs are ever materialised as float64.
    """

    def __init__(self, name, verbose=True):
        import mgb_hydrology as mgb
        self.mgb = mgb
        self.name = name
        spec = CELLS[name]
        self.label = spec['label']
        MI = PROC / spec['bundle']
        self.bundle = spec['bundle']
        self.TOP = dict(np.load(MI / 'topology.npz'))
        self.PAR = dict(np.load(MI / 'parameters.npz', allow_pickle=True))
        self.DIS = dict(np.load(MI / 'discharge.npz', allow_pickle=True))
        self.MAN = json.loads((MI / 'manifest.json').read_text())

        # --- the period, declared here and checked against the cache ------------------
        self.D_FULL = pd.date_range(WU_SPAN[0], spec['scored'][1], freq='D')
        self.D_SC = pd.date_range(spec['scored'][0], spec['scored'][1], freq='D')
        self.NWU = len(self.D_FULL) - len(self.D_SC)
        # cast the unit: the cache stores datetime64[D] and date_range yields [ns];
        # DatetimeIndex.equals compares resolution, so without this the two are unequal
        # while printing identically.
        ckey = spec.get('cache', name)      # H2E reads H2's cache (same bundle + period)
        cdates = pd.DatetimeIndex(np.load(CACHE / f'{ckey}_dates.npy')
                                  .astype('datetime64[ns]'))
        assert cdates.equals(self.D_FULL), (
            f'{name}: cache date axis {cdates[0].date()}..{cdates[-1].date()} '
            f'({len(cdates)}) != declared {self.D_FULL[0].date()}..'
            f'{self.D_FULL[-1].date()} ({len(self.D_FULL)})')
        self.P_MM = np.load(CACHE / f'{ckey}_precip.npy', mmap_mode='r')
        self.E_MM = np.load(CACHE / f'{ckey}_pet.npy', mmap_mode='r')
        assert self.P_MM.shape[0] == len(self.D_FULL)

        # --- ET stress mode of this cell (H2E; everything else stays 'linear') --------
        self.ET_STRESS = spec.get('et_stress', 'linear')
        self.THETA_CRIT = float(spec.get('theta_crit', 0.6))

        # --- objective weights of this cell (H2E-S; everything else stays incumbent) --
        # A cell that does not declare weights gets the incumbent 3-tuple, so H1, H2 and
        # H2E keep the objective they were searched with.
        self.W = tuple(float(v) for v in spec.get('weights', W_SET_INCUMBENT))
        self.USE_PEAK = bool(spec.get('use_peak', False))
        assert abs(sum(self.W) - 1.0) < 1e-9, (
            f'{name}: objective weights {self.W} do not sum to 1, so F(perfect) != 1')

        ids = self.TOP['minibacia_id'].astype(np.int64)
        self.ids = ids
        self.A_MB = self.TOP['own_area_km2'].astype(np.float64)
        self.A_TOT = float(self.A_MB.sum())
        self.REACH_KM = self.TOP['reach_km'].astype(np.float64)
        self.TOPO = mgb.build_topology(ids, self.A_MB,
                                       self.TOP['downstream_id'].astype(np.int64),
                                       self.PAR['urh_fraction'].astype(np.float64),
                                       urh_codes=self.PAR['urh_id'].astype(np.int64))
        self.WM0 = self.PAR['Wm_mm'].astype(np.float64)
        self.U24 = self.PAR['urh_id'].astype(int)
        self.SOIL_OF_URH = np.array([c // 10 for c in self.U24])
        KC_LAND = [1.0, 0.9, 0.9, 1.0, 0.35, 0.25, 1.05, 1.05]
        LAI_LAND = [5.0, 2.0, 1.5, 2.5, 0.5, 0.0, 0.0, 2.0]
        self.KC0 = np.array([KC_LAND[(c % 10) - 1] for c in self.U24])
        self.LAI0 = np.array([LAI_LAND[(c % 10) - 1] for c in self.U24])
        self.ALPHA_INT = 0.2

        # --- gauges: the primary calibration set of this bundle -----------------------
        dis_dates = pd.DatetimeIndex(np.asarray(self.DIS['dates'], dtype='datetime64[ns]'))
        keep = np.isin(dis_dates, self.D_SC)
        assert int(keep.sum()) == len(self.D_SC), (
            f'{name}: discharge covers {int(keep.sum())} of the {len(self.D_SC)} scored days')
        self.JP = np.flatnonzero(self.DIS['is_calibration_safe'])
        self.GC = self.DIS['gauge_code'].astype(str)[self.JP]
        self.GMIDX = self.DIS['gauge_minibacia_idx'].astype(np.int64)
        self.GUP = self.TOP['upstream_area_km2'].astype(np.float64)[self.GMIDX[self.JP]]
        self.NG = int(self.JP.size)
        self.REC_IDS = ids[self.GMIDX[self.JP]].tolist()
        self.GW = (self.DIS['gauge_weight'].astype(float)[self.JP]
                   if 'gauge_weight' in self.DIS else np.ones(self.NG))
        self.QOBS = np.where(self.DIS['q_valid'][keep][:, self.JP],
                             self.DIS['q_m3s'][keep][:, self.JP].astype(np.float64), np.nan)
        self.QLOG0 = np.nanmean(self.QOBS, axis=0) * 0.01

        # --- period masks on the SCORED axis ------------------------------------------
        yr = self.D_SC.year.to_numpy()
        self.yr = yr
        self.M_CAL = np.isin(yr, CAL_YEARS)
        self.M_VAL = ~self.M_CAL
        self.M_LANINA = yr == 2011
        self.M_ELNINO = np.isin(yr, [2015, 2016])
        self.M_VOTHER = np.isin(yr, [2009, 2010, 2017])
        self.M_2018 = yr == 2018
        self.PERIODS = [('CAL 2012-14', self.M_CAL), ('VAL all', self.M_VAL),
                        ('VAL La Nina 11', self.M_LANINA),
                        ('VAL El Nino 15-16', self.M_ELNINO),
                        ('VAL other 09/10/17', self.M_VOTHER)]
        if self.M_2018.any():
            self.PERIODS.append(('VAL 2018', self.M_2018))

        # --- macro-regions, read off the model's own topology -------------------------
        order = [str(c) for c in self.GC[np.argsort(-self.GUP)]]
        self.ANCHOR_CODES = [c for c in order if c != ANCHOR_EXCLUDE][:2]
        anch = {int(self.GMIDX[self.JP[list(self.GC).index(c)]]): k
                for k, c in enumerate(self.ANCHOR_CODES, start=1)}
        down = self.TOPO.down
        REG = np.zeros(self.TOPO.n_mini, dtype=np.int64)
        for i in range(self.TOPO.n_mini):
            cur = i
            while cur >= 0:
                if cur in anch:
                    REG[i] = anch[cur]
                    break
                cur = down[cur]
        self.REG = REG
        self.NREG = int(REG.max()) + 1

        # --- the calibration segment: warm-up 2011 + CAL 2012-14 ----------------------
        m_seg = np.isin(yr, [SEARCH_WU_YEAR] + CAL_YEARS)
        seg_pos_sc = np.flatnonzero(m_seg)
        self.N_WU_SEG = int((yr == SEARCH_WU_YEAR).sum())
        self.POS_CAL = seg_pos_sc[self.N_WU_SEG:]
        assert np.array_equal(self.POS_CAL, np.flatnonzero(self.M_CAL))
        off = self.NWU                       # scored days start here in the FULL axis
        self.P_SEG = np.asarray(self.P_MM[off + seg_pos_sc], dtype=np.float64)
        self.E_SEG = np.asarray(self.E_MM[off + seg_pos_sc], dtype=np.float64)
        self.PM_SEG, self.EM_SEG = self.P_SEG.mean(0), self.E_SEG.mean(0)

        # --- observed recession constants, computed ONCE ------------------------------
        self.K_OBS_CAL, self.NSEG_OBS_CAL = recession_fleet(self.QOBS[self.M_CAL])
        self.K_OBS = {}
        for pn, pm in self.PERIODS:
            self.K_OBS[pn] = recession_fleet(self.QOBS[pm])[0]

        # --- observed annual maxima on the CAL window, computed ONCE -----------------
        # Same pattern as K_OBS_CAL: the observed side of the signature is a property of
        # the gauges and never changes during a search, so it is computed once here and
        # only the simulated side is recomputed per evaluation.
        self.AMS_OBS_CAL, self.AMS_YEARS_CAL = ams_fleet(self.QOBS[self.M_CAL],
                                                         yr[self.M_CAL])
        self.N_AMS_OBS = int(np.isfinite(self.AMS_OBS_CAL).sum())

        # --- day-of-year climatology benchmark, from the whole scored record ----------
        self.QCLIM = doy_climatology(self.QOBS, self.D_SC)

        self.CELL_MINI = self.TOPO.cell_mini
        self.CELL_URH = self.TOPO.cell_urh
        self.CELL_FRAC = self.TOPO.cell_frac
        if verbose:
            print(f'{name}: bundle {spec["bundle"]}, full {self.D_FULL[0].date()}..'
                  f'{self.D_FULL[-1].date()} ({len(self.D_FULL)} d), '
                  f'scored {len(self.D_SC)} d, {self.NG} primary gauges, '
                  f'{self.NREG} regions', flush=True)
            print(f'{name}: weights {self.W}  peak term '
                  f'{"ON" if self.USE_PEAK else "off"}'
                  + (f', {self.N_AMS_OBS} of {self.AMS_OBS_CAL.size} observed CAL '
                     f'gauge-years usable' if self.USE_PEAK else ''), flush=True)

    # ---------------------------------------------------------------- parameters
    def build_params(self, x, reg_over=None, soil_over=None):
        v = dict(zip(NAMES, inv(np.asarray(x, float), IS_LOG)))
        n = self.TOPO.n_mini
        wm = self.WM0 * v['wm_mult']
        ks = np.full(n, v['k_sup'])
        kb = np.full(n, v['k_bas'])
        kfrac = np.full(n, v['k_int_frac'])
        cel = np.full(n, v['celerity'])
        if reg_over:
            arrs = {'k_sup': ks, 'k_bas': kb, 'k_int_frac': kfrac, 'celerity': cel}
            for nm, vals in reg_over.items():
                rv = inv(np.asarray(vals, float), IS_LOG[NAMES.index(nm)])
                for k in range(self.NREG):
                    sel = self.REG == k
                    if nm == 'wm_mult':
                        wm[sel] = self.WM0[sel] * rv[k]
                    else:
                        arrs[nm][sel] = rv[k]
        ki = kfrac * kb                    # k_int < k_bas holds by construction
        adr = np.full(len(self.U24), v['adr'])
        fint = np.full(len(self.U24), v['fint'])
        bsh = np.full(len(self.U24), v['b'])
        if soil_over:
            tgt = {'adr': adr, 'fint': fint, 'b': bsh}
            for nm, vals in soil_over.items():
                sv = inv(np.asarray(vals, float), IS_LOG[NAMES.index(nm)])
                for si in (1, 2, 3):
                    tgt[nm][self.SOIL_OF_URH == si] = sv[si - 1]
        tau = self.REACH_KM * 1000.0 / (cel * 86400.0)
        return self.mgb.MgbParams(
            wm_mini=wm, b=bsh, kc=self.KC0 * v['kc_mult'],
            lai=self.LAI0 * v['lai_mult'], alpha_int=self.ALPHA_INT,
            adr=adr, fint=fint, percolation='linear', reservoir='exact',
            k_sup=ks, k_int=ki, k_bas=kb, tau_channel=tau,
            et_stress=self.ET_STRESS, theta_crit=self.THETA_CRIT)

    def eq_state(self, params, p_mean, e_mean, n_bis=60):
        """Mean-field equilibrium start, re-solved for the candidate parameters.

        This is what makes a one-year warm-up enough: a slow-groundwater candidate begins
        from ITS OWN groundwater equilibrium, not from a 60-day one.
        """
        ex = params.expand(self.TOPO)
        cm = self.CELL_MINI
        pc, ec = p_mean[cm], e_mean[cm]

        # The equilibrium must use the SAME ET stress function as the engine, or a
        # fao56 candidate would start from the linear model's equilibrium and burn
        # warm-up correcting an inconsistency this solver exists to remove.
        if ex.et_stress == 'fao56':
            def _et(m):
                return ex.kc * ec * np.minimum(m / ex.theta_crit, 1.0)
        else:
            def _et(m):
                return ex.kc * ec * m          # the original linear term, verbatim

        lo = np.zeros_like(pc)
        hi = np.ones_like(pc)
        for _ in range(n_bis):
            mid = .5 * (lo + hi)
            pos = (pc * np.power(np.maximum(1 - mid, 0), ex.b) - _et(mid)
                   - ex.adr * ex.wm * mid) > 0
            lo = np.where(pos, mid, lo)
            hi = np.where(pos, hi, mid)
        x = .5 * (lo + hi)
        resid = float(np.abs(pc * np.power(np.maximum(1 - x, 0), ex.b) - _et(x)
                             - ex.adr * ex.wm * x).max())
        drain = ex.adr * x * ex.wm
        fr = self.CELL_FRAC
        nmb = self.TOPO.n_mini
        d_sup = np.bincount(cm, weights=pc * (1 - np.power(np.maximum(1 - x, 0), ex.b)) * fr,
                            minlength=nmb)
        d_int = np.bincount(cm, weights=ex.fint * drain * fr, minlength=nmb)
        d_bas = np.bincount(cm, weights=(1 - ex.fint) * drain * fr, minlength=nmb)
        st = self.mgb.MgbState(sc=np.zeros(self.TOPO.n_cells), w=x * ex.wm,
                               s_sup=d_sup / ex.c_sup, s_int=d_int / ex.c_int,
                               s_bas=d_bas / ex.c_bas, s_ch=np.zeros(nmb))
        return st, resid, x

    # ---------------------------------------------------------------- runners
    def run_seg(self, x, reg_over=None, soil_over=None):
        pr = self.build_params(x, reg_over, soil_over)
        st, _, _ = self.eq_state(pr, self.PM_SEG, self.EM_SEG)
        return self.mgb.simulate(self.TOPO, pr, self.P_SEG, self.E_SEG, state=st,
                                 warmup_days=self.N_WU_SEG, record_ids=self.REC_IDS,
                                 routing_backend='auto')

    def run_full(self, x, reg_over=None, soil_over=None):
        P = np.asarray(self.P_MM, dtype=np.float64)
        E = np.asarray(self.E_MM, dtype=np.float64)
        pr = self.build_params(x, reg_over, soil_over)
        st, _, _ = self.eq_state(pr, P.mean(0), E.mean(0))
        res = self.mgb.simulate(self.TOPO, pr, P, E, state=st, warmup_days=self.NWU,
                                record_ids=self.REC_IDS, routing_backend='auto')
        return res, pr

    # ---------------------------------------------------------------- objective
    def score_cal(self, qsim):
        """The per-gauge terms on the CAL window.  `qsim` rows align with POS_CAL.

        Returns (k1, k2, k_sim, r_ams).  `r_ams` is all-NaN unless this cell asked for the
        peak term, so a cell without it pays nothing for its existence.
        """
        obs = self.QOBS[self.M_CAL]
        k1 = np.full(self.NG, np.nan)
        k2 = np.full(self.NG, np.nan)
        for j in range(self.NG):
            s = qsim[:, j].astype(np.float64)
            o = obs[:, j]
            k1[j] = kge_terms(s, o)['kge']
            k2[j] = kge_terms(np.log(np.maximum(s, 0) + self.QLOG0[j]),
                              np.log(np.maximum(o, 0) + self.QLOG0[j]))['kge']
        k_sim, _ = recession_fleet(qsim)
        r_ams = np.full(self.NG, np.nan)
        if self.USE_PEAK:
            # PAIRED day set (docs/33 s2.3): the simulation is masked to the observed
            # validity mask BEFORE its annual maximum is taken, so a simulated peak on a
            # day the gauge did not report can never enter the ratio.  The min-days test
            # then reads the same count on both sides by construction.
            sim_paired = np.where(np.isfinite(obs), np.asarray(qsim, dtype=np.float64),
                                  np.nan)
            ams_sim, _ = ams_fleet(sim_paired, self.yr[self.M_CAL])
            r_ams = ams_ratio(ams_sim, self.AMS_OBS_CAL)
        return k1, k2, k_sim, r_ams

    def F_of(self, x, reg_over=None, soil_over=None):
        res = self.run_seg(x, reg_over, soil_over)
        k1, k2, k_sim, r_ams = self.score_cal(res.q_m3s)
        e_rec = rec_efficiency(k_sim, self.K_OBS_CAL)
        e_peak = peak_efficiency(r_ams)
        f = blend(k1, k2, e_rec, w=self.W, e_peak=e_peak, use_peak=self.USE_PEAK)
        return f, dict(k1=k1.astype(np.float32), k2=k2.astype(np.float32),
                       k_sim=k_sim.astype(np.float32),
                       r_ams=r_ams.astype(np.float32),
                       rc=float(res.balance['runoff_coefficient']),
                       resid=float(res.balance['residual_relative']))


# ============================================================ the search vector
def pack_bounds(cell):
    """Config-B-shaped search vector: the 10 global parameters plus the regional and
    soil-family extras the v1 screening selected.  Region 0 and soil family 1 ARE the
    global entries, so the extras number (NREG-1) and 2 respectively and the prior maps to
    a vector in which every extra equals its global parent - i.e. the search starts from
    an exactly global configuration and can only depart from it if that pays."""
    names = [f'{n}@global' for n in NAMES]
    lo, hi, x0 = list(LO), list(HI), list(X0)
    for nm in REG_PARAMS:
        i = NAMES.index(nm)
        for k in range(1, cell.NREG):
            names.append(f'{nm}@R{k}')
            lo.append(LO[i]); hi.append(HI[i]); x0.append(X0[i])
    for nm in SOIL_PARAMS:
        i = NAMES.index(nm)
        for s in (2, 3):
            names.append(f'{nm}@soil{s}')
            lo.append(LO[i]); hi.append(HI[i]); x0.append(X0[i])
    return names, np.array(lo), np.array(hi), np.array(x0)


def unpack(cell, z):
    x = np.asarray(z, float)[:len(NAMES)].copy()
    k = len(NAMES)
    reg_over, soil_over = {}, {}
    for nm in REG_PARAMS:
        reg_over[nm] = np.concatenate([[x[NAMES.index(nm)]], z[k:k + cell.NREG - 1]])
        k += cell.NREG - 1
    for nm in SOIL_PARAMS:
        soil_over[nm] = np.concatenate([[x[NAMES.index(nm)]], z[k:k + 2]])
        k += 2
    return x, reg_over, soil_over


# ============================================================ cache + worker
def ensure_cache(cell_name, build_h1_warmup=None, verbose=True):
    """Materialise the cell's full (warm-up + scored) forcing as plain .npy.

    Why .npy and not the bundle npz: four concurrent workers memory-map one shared copy
    instead of each decompressing its own, and a raw buffer with a shape header cannot be
    half-read without an error - which the CSVs demonstrably can (see src/forcing_npy.py).
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    spec = CELLS[cell_name]
    ckey = spec.get('cache', cell_name)     # H2E resolves to H2's files (same forcing)
    dfull = pd.date_range(WU_SPAN[0], spec['scored'][1], freq='D')
    fp = CACHE / f'{ckey}_precip.npy'
    fe = CACHE / f'{ckey}_pet.npy'
    fd = CACHE / f'{ckey}_dates.npy'
    if fp.exists() and fe.exists() and fd.exists():
        # cast the unit exactly as Cell.__init__ does: the cache stores datetime64[D],
        # date_range yields [ns], and DatetimeIndex.equals compares resolution - without
        # the cast this check is always False and the cache is silently REWRITTEN on
        # every call (observed 2026-08-03: an ensure_cache('H2E') rewrote the H2 files
        # with identical content; harmless only because the write is deterministic).
        got = pd.DatetimeIndex(np.load(fd).astype('datetime64[ns]'))
        if got.equals(dfull):
            if verbose:
                print(f'{cell_name}: cache present ({ckey}), {len(got)} d')
            return
    MI = PROC / spec['bundle']
    frc = np.load(MI / 'forcing.npz')
    bd = pd.DatetimeIndex(np.asarray(frc['dates'], dtype='datetime64[ns]'))
    P, E = frc['precip_mm'], frc['pet_mm']
    if bd.equals(dfull):
        Pf, Ef = np.asarray(P), np.asarray(E)
    else:
        # the v1 bundle starts at 2009 and carries no 2008 at all, so the warm-up block
        # has to be supplied.  It is supplied by the caller, exactly as notebook 13 v1 and
        # notebook 14 v1 built it, so that H1 differs from the Config B already in hand in
        # the OBJECTIVE and nothing else.
        if build_h1_warmup is None:
            raise SystemExit(f'{cell_name}: bundle spans {bd[0].date()}..{bd[-1].date()} '
                             f'but the cell needs {dfull[0].date()}..{dfull[-1].date()} '
                             f'and no warm-up builder was given')
        d_wu = pd.date_range(WU_SPAN[0], WU_SPAN[1], freq='D')
        P_wu, E_wu = build_h1_warmup(bd, P, E, d_wu)
        assert P_wu.shape == (len(d_wu), P.shape[1]) and E_wu.shape == P_wu.shape
        assert d_wu.append(bd).equals(dfull), 'warm-up block does not abut the bundle'
        Pf = np.vstack([P_wu, np.asarray(P)]).astype(np.float32)
        Ef = np.vstack([E_wu, np.asarray(E)]).astype(np.float32)
    assert Pf.shape[0] == len(dfull) and Ef.shape[0] == len(dfull)
    assert not np.isnan(Pf).any() and not np.isnan(Ef).any()
    np.save(fp, Pf.astype(np.float32))
    np.save(fe, Ef.astype(np.float32))
    np.save(fd, dfull.to_numpy().astype('datetime64[D]'))
    if verbose:
        print(f'{cell_name}: cache written, {Pf.shape} '
              f'P {Pf.mean()*365.25:,.0f} mm/yr, PET {Ef.mean()*365.25:,.0f} mm/yr')


_CELL_CACHE = {}


def get_cell(name):
    if name not in _CELL_CACHE:
        import sys
        if str(REPO / 'src') not in sys.path:
            sys.path.insert(0, str(REPO / 'src'))
        _CELL_CACHE[name] = Cell(name, verbose=False)
    return _CELL_CACHE[name]


def _arch_arrays(arch):
    # `r_ams` is appended LAST so the tuple's existing positions are untouched; it is
    # written for every cell (all-NaN where the peak term is off) rather than
    # conditionally, because a checkpoint whose contents depend on a cell flag is a
    # checkpoint that eventually gets read by the wrong reader.
    return (np.array([a[0] for a in arch], dtype=np.float64),
            np.array([a[1] for a in arch], dtype=np.float64),
            np.array([a[2]['k1'] for a in arch], dtype=np.float32),
            np.array([a[2]['k2'] for a in arch], dtype=np.float32),
            np.array([a[2]['k_sim'] for a in arch], dtype=np.float32),
            np.array([a[2]['rc'] for a in arch], dtype=np.float64),
            np.array([a[2]['resid'] for a in arch], dtype=np.float64),
            np.array([a[2]['r_ams'] for a in arch], dtype=np.float32))


def run_dds_cell(job):
    """Worker entry point.  One (cell, seed) search.  Must stay module level: Windows
    spawns a fresh interpreter per worker and pickles this by qualified name."""
    name, seed, budget = job['cell'], job['seed'], job['budget']
    cell = get_cell(name)
    pnames, lo, hi, z0 = pack_bounds(cell)

    def F(z):
        x, ro, so = unpack(cell, z)
        return cell.F_of(x, ro, so)

    # --- checkpoint / resume -----------------------------------------------------------
    part = job.get('part')
    replay = None
    if part is not None:
        part = pathlib.Path(part)
        if part.exists():
            try:
                z = np.load(part, allow_pickle=True)
                if int(z['budget'][0]) == budget and int(z['seed'][0]) == seed \
                        and str(z['cell'][0]) == name:
                    # a checkpoint written before the C2b peak term existed carries no
                    # arch_ra; it is replayed with NaN there, which is exactly what a
                    # peak-less cell produces anyway.  The replay's RNG assertion is the
                    # thing that guarantees the search is the same search, not this array.
                    has_ra = 'arch_ra' in z.files
                    nan_ra = np.full(z['arch_k1'].shape[1], np.nan, dtype=np.float32)
                    ex = [dict(k1=z['arch_k1'][i], k2=z['arch_k2'][i],
                               k_sim=z['arch_ks'][i],
                               r_ams=z['arch_ra'][i] if has_ra else nan_ra,
                               rc=float(z['arch_rc'][i]),
                               resid=float(z['arch_resid'][i]))
                          for i in range(z['arch_f'].size)]
                    replay = (z['arch_x'], z['arch_f'], ex)
                else:
                    print(f'    checkpoint present but for a different '
                          f'(cell, seed, budget) - ignoring it', flush=True)
            except Exception as e:                       # a truncated npz is not fatal
                print(f'    checkpoint unreadable ({e}) - starting from scratch', flush=True)

    def _save(arch):
        ax, af, k1, k2, ks, rc, rs, ra = _arch_arrays(arch)
        tmp = part.with_suffix('.tmp.npz')
        np.savez_compressed(tmp, cell=np.array([name]), seed=np.array([seed]),
                            budget=np.array([budget]), arch_x=ax, arch_f=af,
                            arch_k1=k1, arch_k2=k2, arch_ks=ks, arch_rc=rc,
                            arch_resid=rs, arch_ra=ra)
        tmp.replace(part)          # atomic: a kill mid-write cannot leave a torn file

    import time
    t0 = time.perf_counter()
    r = dds(F, z0, lo, hi, budget, seed=seed, log=job.get('log', 25),
            replay=replay, checkpoint=None if part is None else _save,
            every=job.get('every', 25))
    wall = time.perf_counter() - t0
    return dict(cell=name, seed=seed, budget=budget, wall_s=wall,
                names=pnames, x=r['x'], f=float(r['f']), hist=r['hist'],
                arch_x=np.array([a[0] for a in r['archive']], dtype=np.float64),
                arch_f=np.array([a[1] for a in r['archive']], dtype=np.float64),
                arch_k1=np.array([a[2]['k1'] for a in r['archive']], dtype=np.float32),
                arch_k2=np.array([a[2]['k2'] for a in r['archive']], dtype=np.float32),
                arch_ks=np.array([a[2]['k_sim'] for a in r['archive']], dtype=np.float32),
                arch_ra=np.array([a[2]['r_ams'] for a in r['archive']], dtype=np.float32))


# ============================================================ CLI worker
def _main():
    """One (cell, seed) search as its own OS process.

    Run as a subprocess rather than through ProcessPoolExecutor inside the notebook.
    Reason: on Windows multiprocessing uses `spawn`, and spawning from a Jupyter kernel
    has to reconstruct a `__main__` that does not exist as a file - it usually works and
    occasionally hangs, and a hang two hours into a four-way search is not a failure mode
    worth accepting. Separate processes also give one log file each, so progress is
    visible while they run, and a crashed worker cannot take the kernel with it.
    """
    import argparse
    import time
    ap = argparse.ArgumentParser()
    ap.add_argument('--cell', required=True, choices=sorted(CELLS))
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--budget', type=int, required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    part = out.with_name(out.stem + '.part.npz')
    print(f'{a.cell} seed {a.seed} budget {a.budget}  checkpoint {part.name}', flush=True)
    r = run_dds_cell(dict(cell=a.cell, seed=a.seed, budget=a.budget, part=str(part)))
    np.savez_compressed(
        out, cell=np.array([r['cell']]), seed=np.array([r['seed']]),
        budget=np.array([r['budget']]), wall_s=np.array([r['wall_s']]),
        names=np.array(r['names']), x=r['x'], f=np.array([r['f']]), hist=r['hist'],
        arch_x=r['arch_x'], arch_f=r['arch_f'], arch_k1=r['arch_k1'],
        arch_k2=r['arch_k2'], arch_ks=r['arch_ks'], arch_ra=r['arch_ra'])
    if part.exists():
        part.unlink()
    print(f'DONE {a.cell} seed {a.seed}: F {r["f"]:.6f} in {r["wall_s"]/60:.1f} min '
          f'({r["wall_s"]/a.budget:.2f} s/eval) -> {out}', flush=True)


if __name__ == '__main__':
    _main()
