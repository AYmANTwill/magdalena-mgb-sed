"""Smoke tests for src/mgb_hydrology.py.  Run: python src/test_mgb_hydrology.py

Plain asserts, no pytest required (pytest still collects them: each test is a
zero-argument ``test_*`` function).  Every assertion PRINTS the numbers it rests on, so a
pass is auditable rather than merely green.

Discipline followed throughout: a headline number is computed twice by two independent
routes and the two must agree.
  * mass balance: the engine's own accumulators AND an outside recomputation that
    re-derives the residual from the daily series + the final state object;
  * routing: two separate implementations (NumPy level sweep vs numba topological node
    loop) must agree to machine precision;
  * the vertical balance: against a verbatim scalar transcription of notebook 03 cell 7.
"""

from __future__ import annotations

import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mgb_hydrology import (  # noqa: E402
    MM_KM2_PER_DAY_TO_M3S,
    N_URH,
    MgbParams,
    MgbState,
    _Expanded,
    _get_numba_router,
    _route_numpy,
    _vertical_step,
    build_topology,
    default_channel_tau,
    simulate,
)

_RESULTS: list[tuple[str, bool, str]] = []


def _report(name: str, ok: bool, detail: str) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}\n        {detail}")
    _RESULTS.append((name, bool(ok), detail))
    assert ok, f"{name}: {detail}"


def _banner(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------------------
# synthetic fixtures
# ---------------------------------------------------------------------------


def _single_cell_topology(area_km2: float = 10.0, urh_col: int = 0, frac: float = 1.0):
    """One minibacia, one URH - the analytically checkable base case."""
    mat = np.zeros((1, N_URH))
    mat[0, urh_col] = frac
    return build_topology([100], [area_km2], [-1], mat, frac_tol=1.0)


def _chain_topology(n: int = 6, area_km2: float = 25.0):
    """Straight chain 0 -> 1 -> ... -> n-1, three URHs per minibacia summing to 1."""
    ids = np.arange(1000, 1000 + n)
    down = np.append(ids[1:], -1)
    mat = np.zeros((n, N_URH))
    mat[:, 0] = 0.5
    mat[:, 10] = 0.3
    mat[:, 20] = 0.2
    return build_topology(ids, np.full(n, area_km2), down, mat)


def _tree_topology(n: int = 400, seed: int = 7, max_urh: int = 5):
    """Random dendritic network, one outlet, random URH mixes summing to 1."""
    rng = np.random.default_rng(seed)
    ids = np.arange(5000, 5000 + n)
    down = np.empty(n, dtype=np.int64)
    for i in range(n - 1):                      # receiver index > own index => acyclic
        down[i] = ids[rng.integers(i + 1, n)]
    down[n - 1] = -1
    mat = np.zeros((n, N_URH))
    for i in range(n):
        k = int(rng.integers(1, max_urh + 1))
        cols = rng.choice(N_URH, size=k, replace=False)
        w = rng.random(k) + 0.05
        mat[i, cols] = w / w.sum()
    return build_topology(ids, rng.uniform(5.0, 80.0, n), down, mat)


def _full_params(seed: int = 0, percolation: str = "linear", n_mini: int = 1) -> MgbParams:
    """Randomised but valid parameters - exercises the per-URH broadcasting."""
    rng = np.random.default_rng(seed)
    return MgbParams(
        wm_mini=rng.uniform(40.0, 400.0, n_mini),
        wm_scale=rng.uniform(0.6, 1.6, N_URH),
        b=rng.uniform(0.2, 2.5, N_URH),
        kc=rng.uniform(0.7, 1.2, N_URH),
        lai=rng.uniform(0.0, 6.0, N_URH),
        percolation=percolation,
        adr=rng.uniform(0.005, 0.25, N_URH),
        fint=rng.uniform(0.1, 0.9, N_URH),
        kint_mm=rng.uniform(0.5, 8.0, N_URH),
        kbas_mm=rng.uniform(0.05, 1.5, N_URH),
        wz_frac=rng.uniform(0.0, 0.4, N_URH),
        lam=rng.uniform(0.15, 0.9, N_URH),
        k_sup=rng.uniform(0.3, 3.0, n_mini),
        k_int=rng.uniform(2.0, 20.0, n_mini),
        k_bas=rng.uniform(20.0, 150.0, n_mini),
        tau_channel=rng.uniform(0.0, 0.6, n_mini),
    )


def _forcing(ndays: int, n_mini: int, seed: int = 1, wet: float = 8.0, pet: float = 4.0):
    rng = np.random.default_rng(seed)
    p = rng.gamma(0.7, wet / 0.7, size=(ndays, n_mini)) * (rng.random((ndays, n_mini)) < 0.45)
    e = np.clip(rng.normal(pet, 1.2, size=(ndays, n_mini)), 0.0, None)
    return p, e


def _random_cells(n: int, rng, percolation: str, *, allow_zero_wm: bool = True):
    """Build a real ``_Expanded`` over n independent pseudo-cells spanning the domain.

    Lets tests 4 and 6 sweep (W, P, Wm, b, ...) far wider than any calibration would,
    including Wm = 0 (open water / fully paved), b < 1 and b > 1, adr = 0 and adr = 1.
    """
    wm = rng.uniform(0.0, 600.0, n)
    if allow_zero_wm:
        wm[rng.random(n) < 0.02] = 0.0
    else:
        wm = np.maximum(wm, 1.0)
    lam = rng.uniform(0.15, 0.95, n)
    dummy = np.ones(1)
    return _Expanded(
        wm=wm,
        wm_pos=wm > 0.0,
        wm_safe=np.where(wm > 0.0, wm, 1.0),
        b=rng.uniform(0.05, 4.0, n),
        kc=rng.uniform(0.5, 1.5, n),
        simax=rng.uniform(0.0, 2.0, n),
        adr=rng.uniform(0.0, 1.0, n),
        fint=rng.uniform(0.0, 1.0, n),
        kint=rng.uniform(0.0, 30.0, n),
        kbas=rng.uniform(0.0, 10.0, n),
        wz=rng.uniform(0.0, 0.9, n) * wm,
        expo=3.0 + 2.0 / lam,
        c_sup=dummy, c_int=dummy, c_bas=dummy, c_ch=dummy,
        percolation=percolation,
    )


def _cell_state(sc, w) -> MgbState:
    z = np.zeros(1)
    return MgbState(sc=sc.copy(), w=w.copy(), s_sup=z.copy(), s_int=z.copy(),
                    s_bas=z.copy(), s_ch=z.copy())


def _independent_balance(res, topo) -> tuple[float, float]:
    """Recompute the residual WITHOUT using ``res.balance`` except for the start value."""
    inflow = float(res.series["p"].sum() + res.series["clip"].sum())
    outflow = float(res.series["et"].sum() + res.series["q_outlet"].sum())
    d_store = res.state.storage_volume(topo) - res.balance["storage_start_mm_km2"]
    resid = inflow - outflow - d_store
    return float(resid), float(abs(resid) / max(inflow, 1.0))


# ---------------------------------------------------------------------------
# 1. mass balance
# ---------------------------------------------------------------------------


def test_01_mass_balance() -> None:
    _banner("TEST 1 - mass balance closes to <= 1e-9 relative on random forcing")
    tol = 1e-9

    topo = _single_cell_topology()
    for perc in ("linear", "mgb"):
        par = _full_params(seed=3, percolation=perc, n_mini=1)
        p, e = _forcing(500, 1, seed=11)
        res = simulate(topo, par, p, e, routing_backend="numpy")
        r_eng = res.balance["residual_relative"]
        r_abs, r_ind = _independent_balance(res, topo)
        _report(
            f"1a single URH, 500 d, percolation='{perc}'",
            r_eng <= tol and r_ind <= tol,
            f"engine rel={r_eng:.3e} | independent rel={r_ind:.3e} "
            f"(abs {r_abs:+.3e} mm.km2 on P={res.balance['p_volume_mm_km2']:.6g}) | "
            f"the two routes agree to {abs(r_eng - r_ind):.3e}",
        )

    topo = _tree_topology(n=400)
    for perc in ("linear", "mgb"):
        par = _full_params(seed=5, percolation=perc, n_mini=topo.n_mini)
        p, e = _forcing(400, topo.n_mini, seed=13)
        res = simulate(topo, par, p, e, routing_backend="numpy")
        r_eng = res.balance["residual_relative"]
        _, r_ind = _independent_balance(res, topo)
        b = res.balance
        _report(
            f"1b full coupled system, percolation='{perc}'",
            r_eng <= tol and r_ind <= tol,
            f"{topo.n_mini} minibacias / {topo.n_cells} URH cells / 400 d: "
            f"engine rel={r_eng:.3e}, independent rel={r_ind:.3e}; "
            f"P={b['p_mm']:.1f} mm, ET={b['et_mm']:.1f} mm, Q={b['runoff_mm']:.1f} mm, "
            f"dS={b['storage_end_mm_km2'] - b['storage_start_mm_km2']:+.6g} mm.km2, "
            f"RC={b['runoff_coefficient']:.3f}",
        )

    # frac_sum != 1 - catches a wrong reference area, which is INVISIBLE on the real
    # data because urh_fractions.csv rows sum to exactly 1.0.
    mat = np.zeros((3, N_URH))
    mat[0, 0] = 0.4          # 60 % of minibacia 1 carries no URH at all
    mat[1, 3] = 0.5
    mat[1, 7] = 0.2
    mat[2, 12] = 1.0
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        topo3 = build_topology([1, 2, 3], [10.0, 20.0, 30.0], [2, 3, -1], mat)
    par = _full_params(seed=9, n_mini=3)
    p, e = _forcing(300, 3, seed=17)
    res = simulate(topo3, par, p, e, routing_backend="numpy")
    _, r_ind = _independent_balance(res, topo3)
    _report(
        "1c mass balance holds when URH fractions do NOT sum to 1",
        res.balance["residual_relative"] <= tol and r_ind <= tol,
        f"frac_sum={np.round(topo3.frac_sum, 3).tolist()}, covered="
        f"{res.balance['covered_area_km2']:.1f} of {res.balance['total_area_km2']:.1f} "
        f"km2; engine rel={res.balance['residual_relative']:.3e}, independent rel="
        f"{r_ind:.3e}",
    )
    _report(
        "1d the negative-W guard never fires (clip term is exactly zero)",
        res.balance["clip_volume_mm_km2"] == 0.0,
        f"clip volume = {res.balance['clip_volume_mm_km2']:.3e} mm.km2, must be 0.0 - "
        "any non-zero value means the formulation, not rounding, drove W below 0",
    )


# ---------------------------------------------------------------------------
# 2. recession from a wet start with zero rainfall
# ---------------------------------------------------------------------------


def test_02_zero_rain_recession() -> None:
    _banner("TEST 2 - zero rainfall from a wet start: decay to zero, W >= 0, no NaN")
    topo = _chain_topology(n=6)
    par = MgbParams(wm_mini=200.0, b=0.6, lai=3.0, adr=0.06, fint=0.6,
                    k_sup=1.5, k_int=8.0, k_bas=60.0, tau_channel=0.15)
    st = MgbState.initial(topo, par, w_frac=1.0)     # soil FULL
    st.sc[:] = 0.6
    st.s_sup[:] = 20.0
    st.s_int[:] = 30.0
    st.s_bas[:] = 50.0
    st.s_ch[:] = 100.0

    ndays = 1200
    p = np.zeros((1, topo.n_mini))
    e = np.full((1, topo.n_mini), 3.0)
    names = ["W", "S_canopy", "S_sup", "S_int", "S_bas", "S_ch", "TOTAL_vol"]
    traj = np.zeros((ndays, 7))
    qout = np.zeros(ndays)
    state = st.copy()
    for t in range(ndays):
        r = simulate(topo, par, p, e, state=state, routing_backend="numpy")
        state = r.state
        traj[t] = [state.w.sum(), state.sc.sum(), state.s_sup.sum(), state.s_int.sum(),
                   state.s_bas.sum(), state.s_ch.sum(), state.storage_volume(topo)]
        qout[t] = r.series["q_outlet"][0]

    d = np.diff(traj, axis=0)
    # Total storage and the two stores with NO possible inflow must fall every single day.
    _report(
        "2a total storage and the inflow-free stores (W, canopy) fall every day",
        bool(d[:, 6].max() <= 1e-9 and d[:, 0].max() <= 1e-12 and d[:, 1].max() <= 1e-12),
        f"max day-to-day increase: TOTAL={d[:, 6].max():+.3e} mm.km2, "
        f"W={d[:, 0].max():+.3e} mm, canopy={d[:, 1].max():+.3e} mm",
    )
    # The three runoff reservoirs and the channel legitimately FILL first: a saturated
    # soil keeps percolating for weeks. Physics says unimodal (one peak), then monotone.
    peaks, sign_changes = [], []
    for j in range(2, 6):
        s = np.sign(np.round(d[:, j], 12))
        s = s[s != 0]
        sign_changes.append(int((np.diff(s) != 0).sum()))
        peaks.append(int(traj[:, j].argmax()))
    _report(
        "2b each runoff reservoir is unimodal, then decays monotonically",
        max(sign_changes) <= 1,
        "sign changes in the daily increment (<=1 means rise-then-fall, no oscillation): "
        + ", ".join(f"{n}={c} (peak day {pk})"
                    for n, c, pk in zip(names[2:6], sign_changes, peaks)),
    )
    _report(
        "2c every store converges to ~zero",
        bool(np.all(traj[-1, :6] <= traj[:, :6].max(axis=0) * 1e-3 + 1e-9)),
        "peak -> final: " + ", ".join(
            f"{n} {traj[:, j].max():.4g}->{traj[-1, j]:.3g}"
            for j, n in enumerate(names[:6])),
    )
    _report(
        "2d W never negative, never above Wm, no NaN or inf in any state",
        bool(traj[:, 0].min() >= 0.0 and state.w.max() <= 200.0 + 1e-12
             and all(np.all(np.isfinite(getattr(state, a)))
                     for a in ("sc", "w", "s_sup", "s_int", "s_bas", "s_ch"))),
        f"min sum(W) over {ndays} d = {traj[:, 0].min():.6e} mm; final max cell W = "
        f"{state.w.max():.6e} mm (Wm=200); all six state arrays finite",
    )
    _report(
        "2e outlet discharge decays monotonically after its peak",
        bool(np.all(np.diff(qout[int(qout.argmax()):]) <= 1e-9)),
        f"peak Q on day {int(qout.argmax())} = "
        f"{qout.max() * MM_KM2_PER_DAY_TO_M3S:.4f} m3/s, final day "
        f"{qout[-1] * MM_KM2_PER_DAY_TO_M3S:.3e} m3/s, max post-peak rise="
        f"{np.diff(qout[int(qout.argmax()):]).max():+.3e}",
    )
    # Independent analytic recheck of the recession CONSTANT, not just its shape.
    tail = traj[-300:, 4]
    ratio = float(np.mean(tail[1:] / tail[:-1]))
    expected = float(np.exp(-1.0 / 60.0))
    _report(
        "2f groundwater tail decays at exactly exp(-1/K_bas) - analytic check",
        abs(ratio - expected) < 1e-6,
        f"measured mean daily ratio={ratio:.12f}, analytic exp(-1/60)={expected:.12f}, "
        f"diff={ratio - expected:+.3e} (this is what would catch a wrong K -> c mapping)",
    )


# ---------------------------------------------------------------------------
# 3. constant rainfall -> steady state with outflow == input
# ---------------------------------------------------------------------------


def test_03_steady_state() -> None:
    _banner("TEST 3 - constant rainfall: steady state with total outflow == rainfall")
    topo = _chain_topology(n=8, area_km2=25.0)
    # PET = 0 so the steady-state target is EXACTLY known (all input must leave as Q),
    # instead of merely 'balanced' against an unknown ET.
    par = MgbParams(wm_mini=150.0, b=0.6, lai=0.0, adr=0.10, fint=0.6,
                    k_sup=1.0, k_int=5.0, k_bas=30.0, tau_channel=0.2)
    ndays, rain = 12000, 7.0
    p = np.full((ndays, topo.n_mini), rain)
    e = np.zeros((ndays, topo.n_mini))
    res = simulate(topo, par, p, e, routing_backend="numpy")

    area = topo.covered_area_km2
    target = rain * area
    q_last = float(res.series["q_outlet"][-1])
    rel = abs(q_last - target) / target
    _report(
        "3a outlet outflow equals rainfall input at steady state",
        rel <= 1e-6,
        f"input={target:.6f} mm.km2/d, outlet={q_last:.6f}, rel err={rel:.3e} "
        f"(= {q_last * MM_KM2_PER_DAY_TO_M3S:.4f} m3/s from {area:.0f} km2)",
    )
    q_mean = float(res.series["q_outlet"][-1000:].mean())
    rel2 = abs(q_mean - target) / target
    _report(
        "3b same answer from the mean of the last 1000 days (independent route)",
        rel2 <= 1e-6,
        f"mean outlet={q_mean:.6f} vs input={target:.6f}, rel err={rel2:.3e}, "
        f"agrees with 3a to {abs(rel - rel2):.3e}",
    )
    drift = float(np.abs(np.diff(res.series["q_outlet"][-50:])).max())
    _report(
        "3c the state is genuinely stationary, not still drifting",
        drift / target < 1e-9,
        f"max |day-to-day change| in outlet over the last 50 d = {drift:.3e} "
        f"({drift / target:.3e} of the input)",
    )
    # With PET = 0 every drop must leave or still be in storage - tight, not approximate.
    b = res.balance
    ds = b["storage_end_mm_km2"] - b["storage_start_mm_km2"]
    closure = abs(b["p_volume_mm_km2"] - b["outlet_volume_mm_km2"] - ds) / b["p_volume_mm_km2"]
    _report(
        "3d with PET=0, cumulative Q == cumulative P minus the storage filled",
        closure <= 1e-9 and b["et_volume_mm_km2"] == 0.0,
        f"RC={b['runoff_coefficient']:.9f}; the {1 - b['runoff_coefficient']:.3e} "
        f"shortfall is exactly the water still stored ({ds:.6g} mm.km2 = "
        f"{ds / area:.2f} mm); closure rel={closure:.3e}; ET={b['et_volume_mm_km2']:.1f}",
    )


# ---------------------------------------------------------------------------
# 4. runoff bounded by available water; W in [0, Wm]
# ---------------------------------------------------------------------------


def test_04_bounds() -> None:
    _banner("TEST 4 - runoff <= P + W and W in [0, Wm] over a random sweep of (W, P)")
    n = 200_000
    for perc in ("linear", "mgb"):
        rng = np.random.default_rng(21)
        ex = _random_cells(n, rng, perc)
        w0 = rng.uniform(0.0, 1.0, n) * ex.wm
        sc0 = rng.uniform(0.0, 1.0, n) * ex.simax
        p = rng.gamma(0.6, 40.0, n) * (rng.random(n) < 0.7)
        pet = rng.uniform(0.0, 12.0, n)
        st = _cell_state(sc0, w0)
        d_sup, d_int, d_bas, et, clip = _vertical_step(ex, st, p, pet)

        avail = p + w0 + sc0
        v1 = float(np.max(d_sup - avail))
        _report(
            f"4a surface runoff <= P + W + canopy store  [{perc}]",
            v1 <= 1e-9,
            f"n={n:,} random states, Wm in [0,600], b in [0.05,4]: "
            f"max(Dsup - (P+W+Sc)) = {v1:+.3e} mm; max Dsup={d_sup.max():.2f}, "
            f"max avail={avail.max():.2f}",
        )
        v2 = float(np.max(d_sup + d_int + d_bas + et - avail))
        _report(
            f"4b total outgoing flux <= available water  [{perc}]",
            v2 <= 1e-9,
            f"max(Dsup+Dint+Dbas+ET - (P+W+Sc)) = {v2:+.3e} mm",
        )
        lo = float(st.w.min())
        hi = float(np.max(st.w - ex.wm))
        _report(
            f"4c W stays inside [0, Wm]  [{perc}]",
            lo >= 0.0 and hi <= 1e-12,
            f"min W={lo:.3e} (>= 0), max (W - Wm)={hi:+.3e} (<= 0); "
            f"{int((ex.wm == 0).sum()):,} cells had Wm=0 and all stayed at W=0 with "
            f"Asat=1",
        )
        resid = (sc0 + w0 + p) - (st.sc + st.w) - d_sup - d_int - d_bas - et - clip
        v4 = float(np.max(np.abs(resid)))
        _report(
            f"4d per-cell balance is exact, cell by cell  [{perc}]",
            v4 <= 1e-11,
            f"max |(Sc0+W0+P) - (Sc1+W1) - Dsup - Dint - Dbas - ET - clip| = "
            f"{v4:.3e} mm over n={n:,}; clip total={clip.sum():.3e}",
        )
        allfin = all(np.all(np.isfinite(a))
                     for a in (st.w, st.sc, d_sup, d_int, d_bas, et))
        _report(
            f"4e no NaN or inf produced  [{perc}]",
            allfin,
            "all outputs finite - this is the assertion that catches "
            "(1 - W/Wm)**b going complex when float error puts W just above Wm",
        )


# ---------------------------------------------------------------------------
# 5. routing conserves mass
# ---------------------------------------------------------------------------


def test_05_routing_conserves_mass() -> None:
    _banner("TEST 5 - routing: volume in == volume out at the outlet + volume stored")
    rng = np.random.default_rng(31)
    topo = _tree_topology(n=1200, seed=19)
    n = topo.n_mini
    tau = rng.uniform(0.0, 1.5, n)
    tau[rng.random(n) < 0.05] = 0.0                      # include pass-through reaches
    c_ch = np.where(tau > 0, -np.expm1(-1.0 / np.where(tau > 0, tau, 1.0)), 1.0)

    ndays = 500
    local = rng.gamma(1.0, 500.0, size=(ndays, n)) * (rng.random((ndays, n)) < 0.5)
    s_ch = np.zeros(n)
    inflow = np.zeros(n)
    q = np.zeros(n)
    out_total = 0.0
    for t in range(ndays):
        _route_numpy(topo, c_ch, s_ch, local[t], inflow, q)
        out_total += float(q[topo.outlets].sum())
    entered = float(local.sum())
    stored = float(s_ch.sum())
    resid = entered - out_total - stored
    rel = abs(resid) / entered
    _report(
        "5a network mass conservation, NumPy level sweep",
        rel <= 1e-9,
        f"entered={entered:.6f}, left at outlet={out_total:.6f}, still stored="
        f"{stored:.6f} mm.km2 -> residual={resid:+.3e} (rel {rel:.3e}); "
        f"{n} reaches x {ndays} d, {len(topo.levels)} topological levels, "
        f"{int((tau == 0).sum())} pass-through reaches",
    )

    router = _get_numba_router()
    if router is None:
        _report("5b numba router agrees with the NumPy sweep", True,
                "SKIPPED - numba unavailable; the NumPy level sweep is the reference")
    else:
        # The two backends are NOT expected to be bit-identical in general: at a
        # confluence the level sweep sums the tributaries via np.add.at in node-index
        # order while the numba loop sums them in topological order, and float addition
        # is not associative.  The bound must therefore be RELATIVE to the flow
        # magnitude.  5b2 below pins the exact-equality claim to the case where it does
        # hold - a chain with no confluences - which is what proves the residual
        # difference is summation order and not a logic difference.
        s2, i2, q2 = np.zeros(n), np.zeros(n), np.zeros(n)
        s3, i3, q3 = np.zeros(n), np.zeros(n), np.zeros(n)
        out2, maxdiff, maxrel = 0.0, 0.0, 0.0
        for t in range(ndays):
            router(topo.order, topo.down, c_ch, s2, local[t], i2, q2)
            _route_numpy(topo, c_ch, s3, local[t], i3, q3)
            a = np.abs(q2 - q3)
            maxdiff = max(maxdiff, float(a.max()))
            maxrel = max(maxrel, float((a / np.maximum(np.abs(q3), 1e-300)).max()))
            out2 += float(q2[topo.outlets].sum())
        rel2 = abs(entered - out2 - float(s2.sum())) / entered
        eps = float(np.finfo(float).eps)
        _report(
            "5b numba topological loop == NumPy level sweep (two implementations)",
            maxrel <= 1e-12 and rel2 <= 1e-9,
            f"max relative |Q_numba - Q_numpy| over {ndays} d x {n} nodes = "
            f"{maxrel:.3e} ({maxrel / eps:.0f} x machine eps); max absolute "
            f"{maxdiff:.3e} on peak Q {q2.max():.4g}; max in-degree "
            f"{int(np.bincount(topo.down[topo.down >= 0]).max())}; numba mass residual "
            f"rel={rel2:.3e}",
        )
        chain = _chain_topology(n=50)
        cc = np.full(50, 0.5)
        s4, i4, q4 = np.zeros(50), np.zeros(50), np.zeros(50)
        s5, i5, q5 = np.zeros(50), np.zeros(50), np.zeros(50)
        loc = rng.gamma(1.0, 500.0, size=(200, 50))
        worst = 0.0
        for t in range(200):
            router(chain.order, chain.down, cc, s4, loc[t], i4, q4)
            _route_numpy(chain, cc, s5, loc[t], i5, q5)
            worst = max(worst, float(np.abs(q4 - q5).max()))
        _report(
            "5b2 on a confluence-free chain the two backends are bit-identical",
            worst == 0.0,
            f"50-reach chain, 200 d: max |Q_numba - Q_numpy| = {worst:.3e} exactly - "
            "so the tree-case difference above is float summation order at confluences, "
            "not a difference in the routing logic",
        )

    one = _single_cell_topology()
    s, i, qq = np.zeros(1), np.zeros(1), np.zeros(1)
    _route_numpy(one, np.array([1.0]), s, np.array([123.456]), i, qq)
    _report(
        "5c tau = 0 is exact pass-through, no phantom storage",
        abs(qq[0] - 123.456) < 1e-12 and abs(s[0]) < 1e-15,
        f"in=123.456 -> out={qq[0]:.12f}, stored={s[0]:.3e}",
    )

    par = _full_params(seed=23, n_mini=topo.n_mini)
    p, e = _forcing(300, topo.n_mini, seed=29)
    res = simulate(topo, par, p, e, routing_backend="numpy")
    _, rel_ind = _independent_balance(res, topo)
    _report(
        "5d full coupled run (balance + reservoirs + routing) conserves mass",
        res.balance["residual_relative"] <= 1e-9 and rel_ind <= 1e-9,
        f"{topo.n_mini} minibacias / {topo.n_cells} URH cells / 300 d: engine rel="
        f"{res.balance['residual_relative']:.3e}, independent rel={rel_ind:.3e}, "
        f"outlet volume={res.balance['outlet_volume_mm_km2']:.6g} mm.km2",
    )


# ---------------------------------------------------------------------------
# 6. monotonicity
# ---------------------------------------------------------------------------


def test_06_monotonicity() -> None:
    _banner("TEST 6 - more rain never produces less runoff")
    n = 100_000
    for perc in ("linear", "mgb"):
        rng = np.random.default_rng(41)
        ex = _random_cells(n, rng, perc, allow_zero_wm=False)
        w0 = rng.uniform(0.0, 1.0, n) * ex.wm
        sc0 = rng.uniform(0.0, 1.0, n) * ex.simax
        pet = rng.uniform(0.0, 10.0, n)
        p = rng.gamma(0.8, 20.0, n)
        outs = []
        for d_p in (0.0, 0.5, 5.0):
            st = _cell_state(sc0, w0)
            ds, di, db, _et, _c = _vertical_step(ex, st, p + d_p, pet)
            outs.append((ds, ds + di + db))
        w_sup = min(float((outs[k + 1][0] - outs[k][0]).min()) for k in range(2))
        w_tot = min(float((outs[k + 1][1] - outs[k][1]).min()) for k in range(2))
        _report(
            f"6a single step: d(Dsup)/dP >= 0 and d(total runoff)/dP >= 0  [{perc}]",
            w_sup >= -1e-12 and w_tot >= -1e-12,
            f"n={n:,} random states, dP in (+0.5, +5.0) mm: smallest increment in "
            f"Dsup={w_sup:+.3e}, in Dsup+Dint+Dbas={w_tot:+.3e} mm",
        )

    topo = _tree_topology(n=200, seed=43)
    par = _full_params(seed=47, n_mini=topo.n_mini)
    p, e = _forcing(600, topo.n_mini, seed=53)
    factors = (1.0, 1.05, 1.25, 2.0, 5.0)
    totals = [float(simulate(topo, par, p * k, e, routing_backend="numpy")
                    .series["q_outlet"].sum()) for k in factors]
    diffs = np.diff(totals)
    _report(
        "6b scaling the whole rainfall series up never lowers outlet volume",
        bool(np.all(diffs > 0)),
        "outlet volume (mm.km2) for P x "
        + "/".join(f"{k:g}" for k in factors) + " = "
        + ", ".join(f"{v:.5g}" for v in totals)
        + f"; every increment positive, smallest={diffs.min():+.5g}",
    )

    p2 = p.copy()
    p2[100, :] += 25.0
    base = simulate(topo, par, p, e, routing_backend="numpy")
    bump = simulate(topo, par, p2, e, routing_backend="numpy")
    cb = np.cumsum(base.series["q_outlet"])
    cu = np.cumsum(bump.series["q_outlet"])
    worst = float((cu - cb).min())
    added = 25.0 * topo.covered_area_km2
    _report(
        "6c one extra rainy day never lowers cumulative outlet volume",
        worst >= -1e-9,
        f"+25 mm on day 100 across all {topo.n_mini} minibacias: "
        f"min(cumQ_bumped - cumQ_base)={worst:+.3e}; by day 600 the extra outlet volume "
        f"is {cu[-1] - cb[-1]:.5g} of the {added:.5g} mm.km2 added "
        f"({100 * (cu[-1] - cb[-1]) / added:.1f} % - the rest is ET and storage)",
    )


# ---------------------------------------------------------------------------
# 7. regression against notebook 03 cell 7 - the project's own derivation
# ---------------------------------------------------------------------------


def test_07_notebook03_regression() -> None:
    _banner("TEST 7 - engine reproduces notebook 03 cell 7 exactly")
    # notebook 03 cell 7, transcribed verbatim as a scalar reference
    Wm, b, ETp = 100.0, 0.6, 3.0
    adr, fint = 0.06, 0.6
    Ksup, Kint, Kbas = 1.0, 6.0, 45.0
    ndays = 130
    P = np.zeros(ndays)
    rng = np.random.default_rng(0)
    for t in range(5, 36):
        if rng.random() < 0.5:
            P[t] = rng.uniform(5, 30)
    W = 20.0
    Ssup = Sint = Sbas = 0.0
    ref = np.zeros(ndays)
    ref_bas = np.zeros(ndays)
    for t in range(ndays):
        Asat = 1 - (1 - W / Wm) ** b
        Dsup = P[t] * Asat
        W += P[t] - Dsup
        if W > Wm:
            Dsup += W - Wm
            W = Wm
        W -= ETp * (W / Wm)
        drain = adr * W
        W -= drain
        if W < 0:
            W = 0
        Ssup += Dsup
        Qsup = Ssup / Ksup
        Ssup -= Qsup
        Sint += fint * drain
        Qint = Sint / Kint
        Sint -= Qint
        Sbas += (1 - fint) * drain
        Qbas = Sbas / Kbas
        Sbas -= Qbas
        ref[t] = Qsup + Qint + Qbas
        ref_bas[t] = Qbas

    topo = _single_cell_topology(area_km2=1.0)
    par = MgbParams(wm_mini=Wm, b=b, lai=0.0, kc=1.0, percolation="linear",
                    adr=adr, fint=fint, reservoir="euler",
                    k_sup=Ksup, k_int=Kint, k_bas=Kbas, tau_channel=0.0)
    st = MgbState.initial(topo, par, w_frac=20.0 / Wm)
    res = simulate(topo, par, P.reshape(-1, 1), np.full((ndays, 1), ETp),
                   state=st, routing_backend="numpy")
    area = topo.covered_area_km2
    eng = res.series["q_outlet"] / area                    # mm.km2/d -> mm/d
    eng_bas = res.series["q_bas"] / area
    dq = float(np.abs(eng - ref).max())
    _report(
        "7a discharge series identical to notebook 03 cell 7",
        dq <= 1e-12,
        f"max |Q_engine - Q_notebook| = {dq:.3e} mm/day over {ndays} d; peak Q "
        f"notebook={ref.max():.6f} vs engine={eng.max():.6f} mm/day "
        f"(the notebook prints {ref.max():.2f})",
    )
    db = float(np.abs(eng_bas - ref_bas).max())
    share = 100.0 * ref_bas[120] / ref[120]
    _report(
        "7b the baseflow COMPONENT also matches, not just the total",
        db <= 1e-12,
        f"max |Qbas_engine - Qbas_notebook| = {db:.3e} mm/day; day-120 baseflow share = "
        f"{share:.1f} % (the notebook prints this number)",
    )
    # And the default 'exact' reservoir must differ, else 'euler' is dead code.
    par_ex = MgbParams(wm_mini=Wm, b=b, lai=0.0, percolation="linear", adr=adr,
                       fint=fint, reservoir="exact", k_sup=Ksup, k_int=Kint,
                       k_bas=Kbas, tau_channel=0.0)
    res_ex = simulate(topo, par_ex, P.reshape(-1, 1), np.full((ndays, 1), ETp),
                      state=MgbState.initial(topo, par_ex, w_frac=20.0 / Wm),
                      routing_backend="numpy")
    eng_ex = res_ex.series["q_outlet"] / area
    _report(
        "7c the default 'exact' reservoir differs from the notebook's Euler form",
        float(np.abs(eng_ex - ref).max()) > 1e-3
        and res_ex.balance["residual_relative"] <= 1e-9,
        f"peak Q exact={eng_ex.max():.4f} vs euler={eng.max():.4f} mm/day "
        f"(exact is lower because 1-exp(-1/K) < 1/K); both conserve mass "
        f"(exact rel={res_ex.balance['residual_relative']:.3e}) - so 'euler' is a real "
        "alternative that was rejected, not dead code",
    )


# ---------------------------------------------------------------------------
# 8. real basin: loads, fast enough, still conservative
# ---------------------------------------------------------------------------


def test_08_real_topology_performance() -> None:
    _banner("TEST 8 - real basin topology: load, speed, conservation (synthetic forcing)")
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proc = os.path.join(root, "data", "processed")
    if not os.path.exists(os.path.join(proc, "minibacias.csv")):
        _report("8 real topology", True, "SKIPPED - data/processed not found")
        return
    from mgb_hydrology import load_soil_params, load_topology

    t0 = time.perf_counter()
    topo = load_topology(proc)
    t_load = time.perf_counter() - t0
    wm = load_soil_params(topo, os.path.join(proc, "minibacia_soil_params.csv"))
    _report(
        "8a topology loads as a single acyclic network",
        topo.n_mini == 8672 and topo.outlets.size == 1,
        f"{topo.n_mini} minibacias, {topo.n_cells:,} active URH cells "
        f"({100 * topo.n_cells / (topo.n_mini * N_URH):.1f} % of the dense "
        f"{topo.n_mini}x{N_URH} grid), {len(topo.levels)} topological levels, "
        f"1 outlet (id {topo.ids[topo.outlets][0]}), area "
        f"{topo.covered_area_km2:,.0f} km2, loaded in {t_load:.2f}s",
    )
    _report(
        "8b IGAC Wm loads for every minibacia and is positive",
        bool(np.all(np.isfinite(wm)) and np.all(wm > 0)),
        f"Wm_mm over {wm.size} minibacias: min={wm.min():.1f} mean={wm.mean():.1f} "
        f"max={wm.max():.1f} mm",
    )

    ndays = 200
    p, e = _forcing(ndays, topo.n_mini, seed=61, wet=7.0, pet=4.0)
    par = MgbParams(wm_mini=wm, b=0.6, lai=2.0, adr=0.05, fint=0.6,
                    k_sup=1.5, k_int=8.0, k_bas=60.0,
                    tau_channel=default_channel_tau(topo.area_km2, 1.0))
    timings, outs = {}, {}
    for backend in ("numpy", "numba"):
        try:
            r = simulate(topo, par, p, e, routing_backend=backend,
                         record_ids=topo.ids[topo.outlets])
        except RuntimeError as exc:
            print(f"        (backend '{backend}' unavailable: {exc})")
            continue
        timings[backend] = r.wall_time_s
        outs[backend] = r
    ref = outs["numpy"]
    _report(
        "8c full-basin run is mass conservative",
        ref.balance["residual_relative"] <= 1e-9,
        f"residual rel={ref.balance['residual_relative']:.3e} (abs "
        f"{ref.balance['residual_mm_km2']:+.4g} mm.km2 on P="
        f"{ref.balance['p_volume_mm_km2']:.6g}); clip="
        f"{ref.balance['clip_volume_mm_km2']:.3e}; P={ref.balance['p_mm']:.0f} mm, "
        f"ET={ref.balance['et_mm']:.0f} mm, Q={ref.balance['runoff_mm']:.0f} mm over "
        f"{ndays} d",
    )
    proj = {k: v / ndays * 3287 for k, v in timings.items()}
    _report(
        "8d a full 3287-day basin run completes in minutes, not hours",
        min(proj.values()) < 300.0,
        "; ".join(f"{k}={timings[k]:.2f}s for {ndays} d -> {proj[k]:.1f}s projected for "
                  f"3287 d" for k in timings),
    )
    if "numba" in outs:
        d = float(np.abs(outs["numba"].q_m3s.astype(np.float64)
                         - ref.q_m3s.astype(np.float64)).max())
        _report(
            "8e numba and NumPy backends agree on the real basin",
            d <= 1e-9,
            f"max |Q_numba - Q_numpy| at the outlet = {d:.3e} m3/s over {ndays} d "
            f"(peak {ref.q_m3s.max():.1f} m3/s); speedup "
            f"{timings['numpy'] / timings['numba']:.2f}x",
        )
    tau = default_channel_tau(topo.area_km2, 1.0)
    _report(
        "8f default channel tau is physically sane for ~6 km reaches",
        0.01 < float(np.median(tau)) < 0.5,
        f"tau (days): min={tau.min():.4f} median={np.median(tau):.4f} "
        f"max={tau.max():.4f}; a {len(topo.levels)}-reach mainstem traverse is "
        f"~{np.median(tau) * len(topo.levels):.0f} d at 1 m/s (Magdalena is ~1500 km, "
        f"so ~17 d at 1 m/s - same order)",
    )


# ---------------------------------------------------------------------------
# 8b. the real forcing files load with the right column ordering
# ---------------------------------------------------------------------------


def test_08b_real_forcing_loaders() -> None:
    _banner("TEST 8b - real forcing CSVs load with correct column ordering")
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proc = os.path.join(root, "data", "processed")
    pf = os.path.join(proc, "forcing_minibacia_precip.csv")
    if not os.path.exists(pf):
        _report("8b real forcing", True, "SKIPPED - forcing CSVs not found")
        return
    import pandas as pd
    from mgb_hydrology import intersect_forcing, load_forcing, load_topology

    topo = load_topology(proc)
    p, pdates = load_forcing(pf, topo)
    e, edates = load_forcing(os.path.join(proc, "forcing_minibacia_pet.csv"), topo)
    _report(
        "8b1 both forcing files load, no NaN, non-negative",
        bool(np.all(np.isfinite(p)) and np.all(np.isfinite(e))
             and p.min() >= 0 and e.min() >= 0),
        f"precip {p.shape} {str(pdates[0])[:10]}..{str(pdates[-1])[:10]} "
        f"max={p.max():.2f} mm/d; pet {e.shape} {str(edates[0])[:10]}.."
        f"{str(edates[-1])[:10]} max={e.max():.2f} mm/d; 0 NaN in both",
    )

    # Column ordering is the failure mode that no shape check can catch. Validate it
    # against a number computed elsewhere in this project: the area-weighted basin mean
    # annual rainfall (docs/foundation audit: 2206 mm/yr for 2008-2018, 2174.3 for
    # 2009-2017). An unweighted mean would NOT move under a column shuffle; an
    # area-weighted one does.
    a = topo.area_km2
    tot = a.sum()
    m1 = float(((p @ a) / tot).mean() * 365.25)
    yrs = len(pdates) / 365.25
    m2 = float((p @ a).sum() / tot / yrs)
    _report(
        "8b2 area-weighted basin rainfall reproduces the audited 2206 mm/yr",
        abs(m1 - 2206.0) < 1.0 and abs(m1 - m2) < 1.0,
        f"2008-2018: mean-of-daily route={m1:.1f} mm/yr, volume-integration route="
        f"{m2:.1f} mm/yr, published audit=2206 -> both agree to {abs(m1 - m2):.2f}",
    )
    mask = ((pd.to_datetime(pdates) >= pd.Timestamp("2009-01-01"))
            & (pd.to_datetime(pdates) <= pd.Timestamp("2017-12-31")))
    pw = p[mask]
    m3 = float(((pw @ a) / tot).mean() * 365.25)
    rng = np.random.default_rng(0)
    shuf = float(((p[:, rng.permutation(p.shape[1])] @ a) / tot).mean() * 365.25)
    _report(
        "8b3 the ordering check has teeth (a column shuffle changes the answer)",
        abs(m3 - 2174.3) < 1.0 and abs(shuf - m1) > 0.5,
        f"2009-2017 window ({int(mask.sum())} days): {m3:.1f} mm/yr vs audited 2174.3; "
        f"shuffling the columns gives {shuf:.1f} mm/yr, i.e. {abs(shuf - m1):.1f} mm/yr "
        f"away - so 8b2 would have failed on a mis-ordered load",
    )

    pi, ei, di = intersect_forcing(p, pdates, e, edates)
    _report(
        "8b4 intersect_forcing aligns the mismatched windows on DATES, not length",
        pi.shape == ei.shape == (3287, topo.n_mini)
        and str(di[0])[:10] == "2009-01-01" and str(di[-1])[:10] == "2017-12-31",
        f"precip {p.shape[0]} d and pet {e.shape[0]} d -> {pi.shape[0]} common days "
        f"{str(di[0])[:10]}..{str(di[-1])[:10]}; this is the documented model window",
    )
    # prove it actually realigned rather than just truncating from the front
    off = float(np.abs(pi[0] - p[0]).max())
    _report(
        "8b5 the aligned precip is NOT simply the first 3287 rows",
        off > 0.0,
        f"max |aligned_row0 - raw_row0| = {off:.3f} mm - precip starts 2008-01-01 but "
        f"the overlap starts 2009-01-01, so a naive length-based slice would have "
        f"offset rainfall from PET by 366 days",
    )


# ---------------------------------------------------------------------------
# 9. guardrails
# ---------------------------------------------------------------------------


def test_09_guardrails() -> None:
    _banner("TEST 9 - the engine refuses inputs that would be silently wrong")
    topo = _chain_topology(n=4)
    par = MgbParams(wm_mini=100.0)
    p, e = _forcing(10, 4, seed=71)
    p = p + 1.0                     # guarantee something strictly positive to negate
    checks = []

    def expect(label, fn, exc=Exception):
        try:
            fn()
        except exc as ex:
            checks.append((label, True, type(ex).__name__))
        except Exception as ex:                                  # wrong exception type
            checks.append((label, False, f"WRONG EXC {type(ex).__name__}"))
        else:
            checks.append((label, False, "NO ERROR RAISED"))

    nanp = p.copy()
    nanp[3, 1] = np.nan
    expect("NaN in precip", lambda: simulate(topo, par, nanp, e), ValueError)
    expect("negative precip", lambda: simulate(topo, par, -p, e), ValueError)
    expect("precip/pet shape mismatch", lambda: simulate(topo, par, p, e[:, :2]), ValueError)
    expect("adr > 1 (drainage would exceed W)",
           lambda: MgbParams(adr=1.4).expand(topo), ValueError)
    expect("k_sup < 1 with reservoir='euler'",
           lambda: MgbParams(reservoir="euler", k_sup=0.5).expand(topo), ValueError)
    expect("unknown percolation mode", lambda: MgbParams(percolation="hbv"), ValueError)
    expect("cycle in the network",
           lambda: build_topology([1, 2], [1.0, 1.0], [2, 1], np.eye(2, N_URH)), ValueError)
    expect("self-draining minibacia",
           lambda: build_topology([1, 2], [1.0, 1.0], [1, -1], np.eye(2, N_URH)), ValueError)
    expect("unknown record id",
           lambda: simulate(topo, par, p, e, record_ids=[999999]), KeyError)
    expect("no field named K - MUSLE erodibility must not reach the water balance",
           lambda: MgbParams(K=0.0266), TypeError)
    expect("warmup_days >= ndays",
           lambda: simulate(topo, par, p, e, warmup_days=10), ValueError)
    ok = all(c[1] for c in checks)
    _report(
        "9a every guardrail fires",
        ok,
        f"{sum(c[1] for c in checks)}/{len(checks)}: "
        + "; ".join(f"{lab} -> {r}" for lab, _, r in checks),
    )


# ---------------------------------------------------------------------------
# 10. restart continuity and warm-up plumbing
# ---------------------------------------------------------------------------


def test_10_restart_and_warmup() -> None:
    _banner("TEST 10 - state handover and warm-up are exact, not approximate")
    topo = _tree_topology(n=150, seed=67)
    par = _full_params(seed=71, n_mini=topo.n_mini)
    p, e = _forcing(400, topo.n_mini, seed=73)
    ids = topo.ids[:20]

    whole = simulate(topo, par, p, e, record_ids=ids, routing_backend="numpy")
    first = simulate(topo, par, p[:150], e[:150], record_ids=ids, routing_backend="numpy")
    second = simulate(topo, par, p[150:], e[150:], state=first.state, record_ids=ids,
                      routing_backend="numpy")
    stitched = np.vstack([first.q_m3s, second.q_m3s])
    d = float(np.abs(stitched.astype(np.float64)
                     - whole.q_m3s.astype(np.float64)).max())
    _report(
        "10a splitting a run in two and handing over the state is exact",
        d == 0.0,
        f"400 d in one call vs 150 + 250 with state handover: max |diff| = {d:.3e} m3/s "
        f"over 20 recorded minibacias (peak {whole.q_m3s.max():.3f} m3/s)",
    )
    warm = simulate(topo, par, p, e, record_ids=ids, warmup_days=150,
                    routing_backend="numpy")
    d2 = float(np.abs(warm.q_m3s.astype(np.float64)
                      - second.q_m3s.astype(np.float64)).max())
    _report(
        "10b warmup_days=150 returns exactly the post-warm-up part of the full run",
        d2 == 0.0 and warm.q_m3s.shape[0] == 250,
        f"shape {warm.q_m3s.shape} (expected (250, 20)); max |diff| vs the handover "
        f"run = {d2:.3e} m3/s",
    )
    _report(
        "10c the mass balance still covers the FULL simulated period, warm-up included",
        abs(warm.balance["p_volume_mm_km2"] - whole.balance["p_volume_mm_km2"]) < 1e-9
        and warm.balance["ndays"] == 400,
        f"warm-up run reports ndays={warm.balance['ndays']} and P="
        f"{warm.balance['p_volume_mm_km2']:.6g} mm.km2, identical to the full run's "
        f"{whole.balance['p_volume_mm_km2']:.6g} - so a short warm-up cannot hide a leak",
    )
    # simulate() must COPY the state it is given, or a calibration loop that reuses one
    # warm-start object would silently drift from iteration to iteration.
    snap = (first.state.w.copy(), first.state.s_bas.copy(), first.state.s_ch.copy())
    again = simulate(topo, par, p[150:], e[150:], state=first.state, record_ids=ids,
                     routing_backend="numpy")
    unchanged = (np.array_equal(snap[0], first.state.w)
                 and np.array_equal(snap[1], first.state.s_bas)
                 and np.array_equal(snap[2], first.state.s_ch))
    repeatable = float(np.abs(again.q_m3s.astype(np.float64)
                              - second.q_m3s.astype(np.float64)).max())
    _report(
        "10d simulate() copies the caller's state, so re-runs are repeatable",
        unchanged and repeatable == 0.0,
        f"caller's w/s_bas/s_ch byte-identical after a second run: {unchanged}; "
        f"re-running the same window from the same state object reproduced it to "
        f"{repeatable:.3e} m3/s",
    )


# ---------------------------------------------------------------------------
# 11. the whole coupled engine vs a naive scalar re-implementation
# ---------------------------------------------------------------------------


def _naive_reference(topo, par, p, e, w_frac=0.4):
    """Deliberately slow, deliberately independent: scalar Python, no NumPy tricks.

    No bincount, no level sweep, no broadcasting - so it shares nothing with the engine
    except the equations themselves.  This is what actually validates the area-weighted
    URH -> minibacia aggregation and the routing sweep together; tests 1-10 could all
    pass with a consistently wrong ``frac`` weighting.
    """
    ex = par.expand(topo)
    n, N = topo.n_mini, topo.n_cells
    mi = topo.cell_mini.tolist()
    frac = topo.cell_frac.tolist()
    area = topo.area_km2.tolist()
    order = topo.order.tolist()
    down = topo.down.tolist()
    wm = ex.wm.tolist()
    b = ex.b.tolist()
    kc = ex.kc.tolist()
    simax = ex.simax.tolist()
    adr = ex.adr.tolist()
    fint = ex.fint.tolist()
    c_sup, c_int, c_bas = ex.c_sup.tolist(), ex.c_int.tolist(), ex.c_bas.tolist()
    c_ch = ex.c_ch.tolist()

    sc = [0.0] * N
    w = [w_frac * wm[c] for c in range(N)]
    s_sup = [0.0] * n
    s_int = [0.0] * n
    s_bas = [0.0] * n
    s_ch = [0.0] * n
    out = []
    for t in range(p.shape[0]):
        i_sup = [0.0] * n
        i_int = [0.0] * n
        i_bas = [0.0] * n
        for c in range(N):
            m = mi[c]
            pp, pe = float(p[t, m]), float(e[t, m])
            s = sc[c] + pp
            thr = s - simax[c] if s > simax[c] else 0.0
            s -= thr
            ec = pe if pe < s else s
            sc[c] = s - ec
            pet_soil = pe - ec
            wm_c = wm[c]
            if wm_c > 0.0:
                rel = w[c] / wm_c
                rel = 0.0 if rel < 0.0 else (1.0 if rel > 1.0 else rel)
                a_sat = 1.0 - (1.0 - rel) ** b[c]
            else:
                a_sat = 1.0
            d_sup = thr * a_sat
            ww = w[c] + thr - d_sup
            if ww > wm_c:
                d_sup += ww - wm_c
                ww = wm_c
            if wm_c > 0.0:
                et = kc[c] * pet_soil * (ww / wm_c)
                if et > ww:
                    et = ww
            else:
                et = 0.0
            ww -= et
            dr = adr[c] * ww
            d_i = fint[c] * dr
            d_b = dr - d_i
            ww -= dr
            w[c] = ww if ww > 0.0 else 0.0
            f = frac[c]
            i_sup[m] += d_sup * f
            i_int[m] += d_i * f
            i_bas[m] += d_b * f
        local = [0.0] * n
        for i in range(n):
            s_sup[i] += i_sup[i]
            qs = s_sup[i] * c_sup[i]
            s_sup[i] -= qs
            s_int[i] += i_int[i]
            qi = s_int[i] * c_int[i]
            s_int[i] -= qi
            s_bas[i] += i_bas[i]
            qb = s_bas[i] * c_bas[i]
            s_bas[i] -= qb
            local[i] = (qs + qi + qb) * area[i]
        inflow = list(local)
        q = [0.0] * n
        for i in order:
            s_ch[i] += inflow[i]
            qq = s_ch[i] * c_ch[i]
            s_ch[i] -= qq
            q[i] = qq
            j = down[i]
            if j >= 0:
                inflow[j] += qq
        out.append([q[i] for i in topo.outlets.tolist()])
    return np.array(out).sum(axis=1)


def test_11_vs_naive_scalar_reference() -> None:
    _banner("TEST 11 - full engine vs an independent scalar re-implementation")
    topo = _tree_topology(n=60, seed=83, max_urh=6)
    par = _full_params(seed=89, n_mini=topo.n_mini)
    p, e = _forcing(120, topo.n_mini, seed=97)
    ref = _naive_reference(topo, par, p, e, w_frac=0.4)
    res = simulate(topo, par, p, e, routing_backend="numpy")
    eng = res.series["q_outlet"]
    rel = float(np.max(np.abs(eng - ref) / np.maximum(np.abs(ref), 1e-300)))
    _report(
        "11a outlet series matches the naive scalar model",
        rel <= 1e-12,
        f"{topo.n_mini} minibacias / {topo.n_cells} URH cells / 120 d: max relative "
        f"|Q_engine - Q_naive| = {rel:.3e}; peak {eng.max():.6f} vs {ref.max():.6f} "
        f"mm.km2/d; totals {eng.sum():.6f} vs {ref.sum():.6f}",
    )
    # Same check with the fractions deliberately unequal AND several URHs per minibacia,
    # because a frac/area mix-up cancels out when all fractions are equal.
    mat = np.zeros((5, N_URH))
    mat[0, [0, 5, 17]] = [0.7, 0.2, 0.1]
    mat[1, [2, 9]] = [0.95, 0.05]
    mat[2, [23]] = [1.0]
    mat[3, [1, 4, 11, 20]] = [0.4, 0.3, 0.2, 0.1]
    mat[4, [7, 8]] = [0.5, 0.5]
    topo5 = build_topology([10, 20, 30, 40, 50], [3.0, 300.0, 17.0, 88.0, 5.0],
                           [30, 30, 40, 50, -1], mat)
    par5 = _full_params(seed=101, n_mini=5)
    p5, e5 = _forcing(90, 5, seed=103)
    ref5 = _naive_reference(topo5, par5, p5, e5)
    res5 = simulate(topo5, par5, p5, e5, routing_backend="numpy")
    rel5 = float(np.max(np.abs(res5.series["q_outlet"] - ref5)
                        / np.maximum(np.abs(ref5), 1e-300)))
    _report(
        "11b matches with unequal URH fractions and areas spanning 100x",
        rel5 <= 1e-12,
        f"areas 3-300 km2, fractions 0.05-1.0: max relative diff = {rel5:.3e}; "
        f"engine total={res5.series['q_outlet'].sum():.9f}, "
        f"naive total={ref5.sum():.9f} mm.km2",
    )


# ---------------------------------------------------------------------------
# 12. adversarial: try to break it
# ---------------------------------------------------------------------------


def test_12_adversarial() -> None:
    _banner("TEST 12 - adversarial parameter and forcing extremes")
    topo = _chain_topology(n=5)
    cases = {
        "b = 100 (near step-function saturation)": dict(b=100.0),
        "b = 0.001 (almost no contributing area)": dict(b=0.001),
        "Wm = 1e-6 mm (degenerate soil)": dict(wm_mini=1e-6),
        "Wm = 0 (open water / fully paved)": dict(wm_mini=0.0),
        "adr = 1.0 (soil empties completely every day)": dict(adr=1.0),
        "adr = 0.0 (no percolation at all)": dict(adr=0.0),
        "fint = 0 (all drainage to groundwater)": dict(fint=0.0),
        "fint = 1 (all drainage to interflow)": dict(fint=1.0),
        "k_bas = 1e6 d (groundwater never releases)": dict(k_bas=1e6),
        "tau = 1000 d (channel never releases)": dict(tau_channel=1000.0),
        "tau = 0 everywhere (instant routing)": dict(tau_channel=0.0),
        "LAI = 20 (huge canopy)": dict(lai=20.0, alpha_int=0.5),
        "percolation='mgb', lam=0.15 (exponent 16.3)": dict(percolation="mgb", lam=0.15),
        "percolation='mgb', wz_frac=0.99": dict(percolation="mgb", wz_frac=0.99),
    }
    rng = np.random.default_rng(107)
    ndays = 400
    # brutal forcing: a 300-day drought then a 500 mm/day deluge, plus noise
    p = rng.gamma(0.4, 5.0, size=(ndays, topo.n_mini))
    p[50:350] = 0.0
    p[351] = 500.0
    p[352] = 0.0
    e = np.full((ndays, topo.n_mini), 6.0)
    e[50:350] = 12.0

    worst_bal, worst_case = 0.0, ""
    lines = []
    for label, kw in cases.items():
        base = dict(wm_mini=150.0, b=0.6, lai=1.0, adr=0.06, fint=0.6,
                    k_sup=1.5, k_int=8.0, k_bas=60.0, tau_channel=0.1)
        base.update(kw)
        par = MgbParams(**base)
        res = simulate(topo, par, p, e, routing_backend="numpy")
        r = res.balance["residual_relative"]
        fin = (np.all(np.isfinite(res.q_m3s)) and np.all(np.isfinite(res.state.w))
               and np.all(np.isfinite(res.state.s_ch)))
        nonneg = (res.state.w.min() >= 0.0 and res.state.s_ch.min() >= -1e-12
                  and res.state.s_bas.min() >= -1e-12
                  and float(res.q_m3s.min()) >= -1e-12)
        clip0 = res.balance["clip_volume_mm_km2"] == 0.0
        ok = r <= 1e-9 and fin and nonneg and clip0
        if r > worst_bal:
            worst_bal, worst_case = r, label
        lines.append(f"{label}: rel={r:.2e} finite={fin} nonneg={nonneg} clip0={clip0}")
        if not ok:
            _report(f"12 {label}", False, lines[-1])
    _report(
        "12a all 14 extreme configurations stay finite, non-negative and conservative",
        True,
        f"worst mass-balance residual {worst_bal:.3e} on '{worst_case}'; "
        f"forcing was a 300-day drought then a single 500 mm/day day. Details -- "
        + " | ".join(lines),
    )

    # A deluge far beyond Wm.  Starting from an EMPTY basin makes the bound exact:
    # with PET=0, cumulative outflow can then only ever be <= cumulative rainfall.
    # (Starting from the default w_frac=0.4 the bound is in + initial storage, and the
    # first version of this test wrongly asserted the tighter form - the 0.4 % 'excess'
    # it flagged was the initial 8 mm of soil water draining out, with mass balance
    # still exact at 2.9e-17.)
    par = MgbParams(wm_mini=20.0, b=2.0, lai=0.0, adr=0.5, fint=0.5, k_sup=0.5,
                    k_int=2.0, k_bas=10.0, tau_channel=0.0)
    p2 = np.zeros((60, topo.n_mini))
    p2[10] = 2000.0
    empty = MgbState.initial(topo, par, w_frac=0.0)
    res = simulate(topo, par, p2, np.zeros((60, topo.n_mini)), state=empty,
                   routing_backend="numpy")
    total_out = float(res.series["q_outlet"].sum())
    total_in = 2000.0 * topo.covered_area_km2
    _report(
        "12b a 2000 mm/day deluge on Wm=20 mm produces no more runoff than fell",
        total_out <= total_in * (1 + 1e-12)
        and res.balance["storage_start_mm_km2"] == 0.0
        and res.balance["residual_relative"] <= 1e-9,
        f"empty start: in={total_in:.6g} mm.km2, out over 60 d={total_out:.6g} "
        f"({100 * total_out / total_in:.4f} %), still stored="
        f"{res.balance['storage_end_mm_km2']:.6g} (that is the {20.0:.0f} mm Wm x "
        f"{topo.covered_area_km2:.0f} km2 the soil retained); mass rel="
        f"{res.balance['residual_relative']:.3e}",
    )

    # Zero everything: the model must do nothing at all, not drift.
    st = MgbState.initial(topo, par, w_frac=0.0)
    res = simulate(topo, par, np.zeros((30, topo.n_mini)), np.zeros((30, topo.n_mini)),
                   state=st, routing_backend="numpy")
    _report(
        "12c zero precip + zero PET + empty state produces exactly zero discharge",
        float(np.abs(res.q_m3s).max()) == 0.0
        and float(np.abs(res.series["q_outlet"]).max()) == 0.0,
        f"max |Q| = {float(np.abs(res.q_m3s).max()):.3e} m3/s over 30 d; "
        f"storage stayed {res.balance['storage_end_mm_km2']:.3e} mm.km2",
    )


# ---------------------------------------------------------------------------


def main() -> int:
    t0 = time.perf_counter()
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    aborted = 0
    for fn in tests:
        try:
            fn()
        except AssertionError as exc:
            aborted += 1
            print(f"  !! ABORTED: {exc}")
    n_ok = sum(1 for _, ok, _ in _RESULTS if ok)
    print("\n" + "=" * 78)
    print(f"{n_ok}/{len(_RESULTS)} assertions PASSED    "
          f"{aborted} test function(s) aborted    "
          f"wall time {time.perf_counter() - t0:.1f}s")
    print("=" * 78)
    return 1 if (aborted or n_ok != len(_RESULTS)) else 0


if __name__ == "__main__":
    raise SystemExit(main())
