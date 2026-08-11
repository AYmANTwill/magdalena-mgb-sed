"""Eckhardt two-parameter baseflow separation, as frozen by docs/33 §2.1.

WHY THIS IS A MODULE AND NOT NOTEBOOK CODE
------------------------------------------
Stage C2b.1 asks one question: *does the model split water the way the rivers do?*  The
only defensible way to ask it is to apply the **identical** filter, with the **identical**
recession constant, to the observed and the simulated hydrograph at the same gauge on the
same days.  If the filter lived in a notebook cell there would be nothing stopping the two
series being filtered by two subtly different code paths - and a difference produced that
way would be an artefact, not a finding.  One function, called twice, makes that class of
error impossible.

WHAT IS FROZEN (docs/33 §2.1 - do NOT change any of it here)
------------------------------------------------------------
    b_k = ( (1 - BFImax) * a * b_{k-1} + (1 - a) * BFImax * y_k ) / ( 1 - a * BFImax )
    b_k = min(b_k, y_k)
    BFI = sum(b_k) / sum(y_k)   over the scored days

  * single FORWARD pass; `b_0 = y_0` at the start of every segment;
  * the first **30 days** of every segment are discarded from both sums (filter warm-up);
  * gaps of **<= 3 days** are linearly interpolated, longer gaps break the record;
  * a **segment** is a contiguous run of **>= 180** valid days;
  * `BFImax` is FIXED at **0.80** (Eckhardt 2005, perennial streams / porous aquifers).
    It is a CHOICE, not a fit: it is never estimated, never tuned per gauge, never
    selected after seeing a result.  A free BFImax can produce almost any BFI you want,
    which is why the literature's BFI "validations" are so often worthless.  0.50 is
    computed alongside as a robustness column and CANNOT change a verdict.
  * `a = exp(-1 / k_obs)` with `k_obs` the master-recession-curve constant of the
    **OBSERVED** series at that gauge.  The SAME `a` filters both series: `a` is a
    property of the catchment, not of the model, and letting the simulation supply its
    own `a` would let the model define its own yardstick.

THE RECESSION ESTIMATOR
-----------------------
`master_recession_k` delegates to `calib_v2.recession_k` rather than reimplementing it.
That is deliberate and load-bearing: docs/33 §2.1 names *"the estimator already on disk
and already validated against docs/22 §4.4"*.  A second implementation, however faithful,
would be a second thing to keep in sync, and the first time it drifted the BFI comparison
would silently stop being the pre-registered one.  The wrapper exists only to give the
quantity its own name and to convert k -> a.

SELF-TEST
---------
    python src/baseflow.py --selftest

is the docs/33 gate: no real series may be filtered until the synthetic cases pass.  The
two anchors are analytic, not empirical:

  * a **pure exponential recession** sampled at the filter's own `a` is a fixed point of
    the recursion with b_k = y_k exactly, so BFI must be 1.0 to machine precision.  (Proof:
    substitute b_k = c*y_k and y_{k-1} = y_k / a; the recursion collapses to c = 1.)
  * a **spike train on a dry bed** has b_k = min(., y_k) = 0 between spikes, so BFI
    collapses to the filter's fast-response coefficient (1-a)B / (1-a B), which is 0.062
    at a = exp(-1/60), B = 0.8.  "~0", and analytically so.

Note what is deliberately NOT asserted: a CONSTANT series does not give BFI = 1, it gives
BFI = BFImax.  That is a known and correct property of the Eckhardt filter, and writing a
test that expected 1.0 there would be a test of a misunderstanding.
"""
from __future__ import annotations

import numpy as np

from calib_v2 import recession_k as _recession_k

# ---- frozen constants (docs/33 §2.1).  Changing any of these invalidates the result.
BFIMAX = 0.80              # the gate value
BFIMAX_ROBUST = 0.50       # reported alongside; cannot change a verdict
WARMUP_DAYS = 30
MAX_GAP_DAYS = 3
MIN_SEGMENT_DAYS = 180
MIN_SCORED_DAYS = 1095     # 3 years; gauges below this are excluded and counted


# ============================================================ the filter
def eckhardt(y: np.ndarray, a: float, bfimax: float = BFIMAX) -> np.ndarray:
    """One forward Eckhardt pass over a CONTIGUOUS, gap-free, positive series.

    `y` must already be a single segment: this function does not know about gaps and will
    happily filter across one if you hand it a series with holes.  Use `bfi_series`.
    """
    y = np.asarray(y, dtype=float)
    if y.ndim != 1:
        raise ValueError('eckhardt expects a 1-D series')
    if not (0.0 < a < 1.0):
        raise ValueError(f'recession parameter a must lie in (0, 1); got {a!r}')
    if not (0.0 < bfimax < 1.0):
        raise ValueError(f'BFImax must lie in (0, 1); got {bfimax!r}')
    denom = 1.0 - a * bfimax
    c_prev = (1.0 - bfimax) * a / denom          # coefficient on b_{k-1}
    c_now = (1.0 - a) * bfimax / denom           # coefficient on y_k
    b = np.empty_like(y)
    prev = y[0]                                  # b_0 = y_0
    b[0] = prev
    for k in range(1, y.size):
        cur = c_prev * prev + c_now * y[k]
        if cur > y[k]:
            cur = y[k]
        b[k] = cur
        prev = cur
    return b


# ============================================================ gaps and segments
def fill_short_gaps(q: np.ndarray, valid: np.ndarray,
                    max_gap: int = MAX_GAP_DAYS) -> tuple[np.ndarray, np.ndarray]:
    """Linearly interpolate runs of <= `max_gap` invalid days that sit BETWEEN valid days.

    Returns (filled_series, filled_valid_mask).  Longer runs, and any run touching either
    end of the record, are left invalid - docs/33: "longer gaps break the record".
    """
    q = np.asarray(q, dtype=float).copy()
    valid = np.asarray(valid, dtype=bool).copy()
    n = q.size
    i = 0
    while i < n:
        if valid[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and not valid[j + 1]:
            j += 1
        run = j - i + 1
        if run <= max_gap and i - 1 >= 0 and j + 1 < n and valid[i - 1] and valid[j + 1]:
            lo, hi = q[i - 1], q[j + 1]
            for m in range(run):
                q[i + m] = lo + (hi - lo) * (m + 1) / (run + 1)
            valid[i:j + 1] = True
        i = j + 1
    return q, valid


def find_segments(valid: np.ndarray,
                  min_len: int = MIN_SEGMENT_DAYS) -> list[tuple[int, int]]:
    """Half-open [start, stop) index pairs of contiguous valid runs of >= `min_len` days."""
    valid = np.asarray(valid, dtype=bool)
    out: list[tuple[int, int]] = []
    n = valid.size
    i = 0
    while i < n:
        if not valid[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and valid[j + 1]:
            j += 1
        if (j + 1 - i) >= min_len:
            out.append((i, j + 1))
        i = j + 1
    return out


# ============================================================ the per-gauge entry point
def bfi_series(q: np.ndarray, valid: np.ndarray, a: float,
               bfimax: float = BFIMAX,
               max_gap: int = MAX_GAP_DAYS,
               min_seg: int = MIN_SEGMENT_DAYS,
               warmup: int = WARMUP_DAYS) -> dict:
    """Segment, filter and score one gauge.

    Returns a dict with
        b        : (n,) baseflow, NaN outside the scored days
        y        : (n,) the gap-filled series, NaN outside the scored days
        scored   : (n,) bool, the days that enter the sums (post-warm-up segment days)
        seg_days : int, days inside qualifying segments (warm-up included)
        n_scored : int, `scored.sum()`
        bfi      : float, sum(b) / sum(y) over `scored`; NaN if nothing is scored
    """
    q = np.asarray(q, dtype=float)
    valid = np.asarray(valid, dtype=bool) & np.isfinite(q) & (q >= 0.0)
    qf, vf = fill_short_gaps(q, valid, max_gap)
    segs = find_segments(vf, min_seg)

    n = q.size
    b = np.full(n, np.nan)
    yy = np.full(n, np.nan)
    scored = np.zeros(n, dtype=bool)
    seg_days = 0
    for s, e in segs:
        seg_days += e - s
        bb = eckhardt(qf[s:e], a, bfimax)
        b[s:e] = bb
        yy[s:e] = qf[s:e]
        scored[s + warmup:e] = True

    if not scored.any():
        return dict(b=b, y=yy, scored=scored, seg_days=seg_days, n_scored=0, bfi=np.nan)
    sy = float(np.nansum(yy[scored]))
    sb = float(np.nansum(b[scored]))
    return dict(b=b, y=yy, scored=scored, seg_days=seg_days,
                n_scored=int(scored.sum()),
                bfi=(sb / sy if sy > 0 else np.nan))


def bfi_over(b: np.ndarray, y: np.ndarray, mask: np.ndarray) -> float:
    """sum(b)/sum(y) restricted to `mask` - used for the sub-period breakdown.

    The filter is NOT re-run per period: re-running it would need a fresh 30-day warm-up
    inside each window and would therefore be a different estimator from the one docs/33
    freezes.  The pre-registered quantity is a ratio of sums, so a sub-period figure is
    that same ratio over fewer days.
    """
    m = np.asarray(mask, dtype=bool) & np.isfinite(b) & np.isfinite(y)
    if not m.any():
        return np.nan
    sy = float(y[m].sum())
    return float(b[m].sum()) / sy if sy > 0 else np.nan


# ============================================================ recession constant
def master_recession_k(q: np.ndarray, min_pts: int = 3,
                       low_pct: float = 40.0) -> tuple[float, int]:
    """Master-recession-curve constant `k` (days) of a series, and its segment count.

    Thin delegation to `calib_v2.recession_k`, which docs/33 §2.1 names by module and
    function.  Monotone declines below the `low_pct`-th flow percentile, segments of
    >= `min_pts` points, ln Q regressed on day number, gauge constant = MEDIAN over
    segments (recession lengths are heavy-tailed; one long dry spell must not set the
    answer).  NaN when nothing qualifies.
    """
    return _recession_k(q, min_pts=min_pts, low_pct=low_pct)


def recession_a(k_days: float) -> float:
    """a = exp(-1/k), the daily recession ratio of a linear reservoir with constant k."""
    k = float(k_days)
    if not np.isfinite(k) or k <= 0:
        return np.nan
    return float(np.exp(-1.0 / k))


# ============================================================ the docs/33 GATE
def _selftest(verbose: bool = True) -> None:
    ok = []

    def check(name, cond, detail):
        ok.append(bool(cond))
        if verbose:
            print(f'{"PASS" if cond else "FAIL"}  {name}: {detail}')

    # -- 1. pure exponential recession -> BFI = 1 (analytic fixed point)
    K = 45.0
    a = recession_a(K)
    t = np.arange(400)
    y = 500.0 * np.exp(-t / K)
    v = np.ones_like(t, dtype=bool)
    r = bfi_series(y, v, a)
    check('exponential recession BFI ~ 1', abs(r['bfi'] - 1.0) < 1e-9,
          f"BFI = {r['bfi']:.12f} (n_scored={r['n_scored']})")

    # -- 2. spike train on a dry bed -> BFI ~ 0 (analytic: (1-a)B/(1-aB))
    Ks = 60.0
    a_s = recession_a(Ks)
    n = 600
    y2 = np.zeros(n)
    y2[::30] = 100.0
    expect = (1.0 - a_s) * BFIMAX / (1.0 - a_s * BFIMAX)
    r2 = bfi_series(y2, np.ones(n, dtype=bool), a_s)
    check('spike train BFI ~ 0', (r2['bfi'] < 0.10) and abs(r2['bfi'] - expect) < 1e-9,
          f"BFI = {r2['bfi']:.6f}, analytic {expect:.6f}, bar < 0.10")

    # -- 3. the filter never exceeds the hydrograph, and never goes negative
    rng = np.random.default_rng(0)
    y3 = np.abs(rng.gamma(1.5, 40.0, 1000)) + 1.0
    b3 = eckhardt(y3, recession_a(30.0))
    check('0 <= b <= y everywhere', bool(np.all(b3 <= y3 + 1e-12) and np.all(b3 >= 0)),
          f'max(b - y) = {float((b3 - y3).max()):.3e}, min(b) = {float(b3.min()):.3e}')

    # -- 4. a mixed hydrograph sits strictly between the two anchors, and a higher
    #       BFImax gives a higher BFI (monotonicity of the knob we froze)
    base = 20.0 * np.exp(-((np.arange(1000) % 200) / 80.0)) + 5.0
    storm = np.zeros(1000)
    storm[np.arange(20, 1000, 60)] = 300.0
    y4 = base + storm
    m80 = bfi_series(y4, np.ones(1000, dtype=bool), recession_a(30.0), BFIMAX)['bfi']
    m50 = bfi_series(y4, np.ones(1000, dtype=bool), recession_a(30.0), BFIMAX_ROBUST)['bfi']
    check('mixed hydrograph strictly interior', 0.0 < m50 < m80 < 1.0,
          f'BFI(0.50) = {m50:.4f} < BFI(0.80) = {m80:.4f}')

    # -- 5. gap handling: a 3-day hole is filled, a 4-day hole breaks the record
    y5 = np.linspace(100.0, 200.0, 50)
    v5 = np.ones(50, dtype=bool)
    v5[10:13] = False
    qf, vf = fill_short_gaps(y5, v5)
    filled3 = bool(vf.all() and np.allclose(qf, y5))
    v6 = np.ones(50, dtype=bool)
    v6[10:14] = False
    _, vf6 = fill_short_gaps(y5, v6)
    check('gap rule (<=3 filled, 4 breaks)', filled3 and (not vf6[10:14].any()),
          f'3-day filled = {filled3}, 4-day still invalid = {not vf6[10:14].any()}')

    # -- 6. segmentation and the 30-day warm-up are actually applied
    v7 = np.ones(500, dtype=bool)
    v7[200:260] = False                      # 60-day hole: two segments, 200 and 240 days
    segs = find_segments(v7, MIN_SEGMENT_DAYS)
    r7 = bfi_series(np.full(500, 10.0), v7, recession_a(30.0))
    check('segments + warm-up', segs == [(0, 200), (260, 500)] and r7['n_scored'] == 380,
          f'segments = {segs}, n_scored = {r7["n_scored"]} (expected 440 - 2*30 = 380)')

    # -- 7. a segment shorter than 180 days is dropped entirely
    v8 = np.ones(300, dtype=bool)
    v8[150:250] = False                      # leaves 150 and 50: neither qualifies
    r8 = bfi_series(np.full(300, 10.0), v8, recession_a(30.0))
    check('short segments dropped', r8['n_scored'] == 0 and not np.isfinite(r8['bfi']),
          f'n_scored = {r8["n_scored"]}, bfi = {r8["bfi"]}')

    # -- 8. the recession estimator recovers a known k from a synthetic hydrograph
    Kr = 25.0
    tt = np.arange(1200)
    # A PURE exponential sawtooth, with no additive offset: `recession_k` fits ln Q on a
    # straight line, so (A e^{-t/K} + c) with c > 0 is curved in log space and MUST bias k
    # high.  A first draft of this test carried "+ 1.0" and returned 27.08 d against a true
    # 25 d - a defect in the test, not in the estimator, and worth recording rather than
    # loosening the tolerance to hide.
    yr = 300.0 * np.exp(-(tt % 100) / Kr)           # sawtooth of clean recessions
    k_hat, nseg = master_recession_k(yr)
    check('MRC recovers a known k', abs(k_hat - Kr) / Kr < 0.05,
          f'k_hat = {k_hat:.3f} d vs true {Kr:.1f} d over {nseg} segments')

    # -- 9. a -> the filter: round trip
    check('a = exp(-1/k) round trip', abs(-1.0 / np.log(recession_a(13.9)) - 13.9) < 1e-9,
          f'a(13.9 d) = {recession_a(13.9):.9f}')

    n_ok = sum(ok)
    print(f'\n{n_ok}/{len(ok)} checks passed')
    if n_ok != len(ok):
        raise SystemExit(1)


if __name__ == '__main__':
    import sys
    if '--selftest' in sys.argv:
        _selftest()
    else:
        print(__doc__)
