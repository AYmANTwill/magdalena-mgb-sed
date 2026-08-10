"""Record per-minibacia daily fields from the water-balance engine, without touching it.

WHY THIS MODULE EXISTS
----------------------
`mgb_hydrology.simulate` returns routed discharge at `record_ids` plus basin-TOTAL daily
series.  The sediment model (docs/31 stages C3-C4) needs the per-minibacia daily surface
runoff and reach inflow, and docs/31 C0.5 requires those to be precomputed and frozen so
that sediment evaluation never re-runs hydrology.

Two ways to get them: add a recording hook inside `simulate`, or drive the engine's kernel
from outside.  The second is chosen because `src/mgb_hydrology.py` is the artefact the
whole of Phase B rests on and it stays byte-frozen - its SHA is on record in
`sim_calibrated_v2/calibration_v2.json`, and the H2E search ran against the exact bytes
now on disk (commit 80a7c10; see docs/agents/journal_c0.md P1/P6).

**No arithmetic is duplicated.**  Every calculation below is a call into the engine's own
`_vertical_step`, `_reservoir_step`, router and `_assemble_balance`; this module supplies
only the day loop and the recording.  Reaching into the engine's private names is
deliberate: it is what makes the two runs the SAME run rather than two implementations
that agree today.  `verify_against_engine` asserts bit-identical discharge and basin
series against `simulate`, so if the engine's loop ever changes shape this fails loudly
instead of drifting.

FIELDS RECORDED (all per minibacia, per scored day)
---------------------------------------------------
`qsur_gen_mm`      saturation-excess surface runoff GENERATED on the URH columns,
                   area-weighted to the minibacia (mm/day).  The engine's `i_sup`.
`qsur_rel_mm`      surface runoff RELEASED by the minibacia surface linear reservoir
                   (mm/day).  The engine's `q_sup`.
`q_local_mm`       total local runoff released to the reach, q_sup + q_int + q_bas
                   (mm/day).
`reach_inflow_m3s` total inflow to the reach that day - local plus everything routed in
                   from upstream (m3/s), read off the router's `inflow` accumulator.
`q_reach_m3s`      routed reach outflow (m3/s), i.e. `simulate`'s discharge at EVERY
                   minibacia rather than only at the gauges.

Both surface fields are stored because MUSLE's `Qsurf` could reasonably be either and
docs/31 C3.3 has not registered its choice yet (journal P5).  Storing one would defeat
the purpose of C0.5.
"""
from __future__ import annotations

import time
from typing import Optional, Sequence

import numpy as np

import mgb_hydrology as mgb

#: recorded field name -> unit, in write order
FIELDS: dict[str, str] = {
    'qsur_gen_mm': 'mm/day',
    'qsur_rel_mm': 'mm/day',
    'q_local_mm': 'mm/day',
    'reach_inflow_m3s': 'm3/s',
    'q_reach_m3s': 'm3/s',
}


def simulate_recording(
    topo: mgb.MgbTopology,
    params: mgb.MgbParams,
    precip: np.ndarray,
    pet: np.ndarray,
    *,
    state: Optional[mgb.MgbState] = None,
    warmup_days: int = 0,
    record_ids: Optional[Sequence[int]] = None,
    routing_backend: str = 'auto',
    dtype_out: type = np.float32,
    sink: Optional[dict] = None,
) -> tuple[mgb.MgbResult, dict]:
    """`mgb_hydrology.simulate`, plus the per-minibacia fields in :data:`FIELDS`.

    `sink` maps each field name to a writable `(ndays - warmup_days, n_mini)` array -
    pass memory-mapped `.npy` arrays to keep peak RAM at the forcing's size instead of
    the forcing plus half a gigabyte of output.  Allocated in RAM when omitted.

    Warm-up days are simulated but NOT recorded, exactly as `simulate` does not record
    them in `q_m3s`; `balance` still covers the full simulated period, because that is
    the only window over which both initial and final storage are known.
    """
    t_start = time.perf_counter()
    n = topo.n_mini
    precip, pet, ndays = mgb._validate_forcing(precip, pet, n, warmup_days, None)
    ex = params.expand(topo)
    st = mgb.MgbState.initial(topo, params) if state is None else state.copy()
    if st.w.shape != (topo.n_cells,) or st.s_sup.shape != (n,):
        raise ValueError('state does not match topology')
    v_start = st.storage_volume(topo)

    if record_ids is None:
        rec_idx = np.arange(n, dtype=np.int64)
        rec_ids = topo.ids.copy()
    else:
        rec_idx = topo.index_of(record_ids)
        rec_ids = topo.ids[rec_idx]
    n_rec = ndays - warmup_days
    q_out_rec = np.empty((n_rec, rec_idx.size), dtype=dtype_out)

    router = mgb._get_numba_router() if routing_backend in ('auto', 'numba') else None
    if routing_backend == 'numba' and router is None:
        raise RuntimeError("routing_backend='numba' requested but numba is unavailable")
    backend = 'numba' if router is not None else 'numpy'

    if sink is None:
        sink = {k: np.empty((n_rec, n), dtype=dtype_out) for k in FIELDS}
    missing = set(FIELDS) - set(sink)
    if missing:
        raise ValueError(f'sink is missing fields: {sorted(missing)}')
    for k in FIELDS:
        if tuple(sink[k].shape) != (n_rec, n):
            raise ValueError(f'sink[{k!r}] is {sink[k].shape}, need {(n_rec, n)}')

    cell_mini = topo.cell_mini
    cell_frac = topo.cell_frac
    a_cell = topo.cell_area_km2
    a_mini = topo.area_km2
    keys = ('p', 'et', 'd_sup', 'd_int', 'd_bas', 'q_sup', 'q_int', 'q_bas',
            'q_outlet', 'clip')
    ser = {k: np.zeros(ndays) for k in keys}
    inflow = np.zeros(n)
    q_node = np.zeros(n)
    to_m3s = mgb.MM_KM2_PER_DAY_TO_M3S

    for t in range(ndays):
        p_cell = precip[t][cell_mini]
        pet_cell = pet[t][cell_mini]
        d_sup, d_int, d_bas, et, clip = mgb._vertical_step(ex, st, p_cell, pet_cell)
        i_sup = np.bincount(cell_mini, weights=d_sup * cell_frac, minlength=n)
        i_int = np.bincount(cell_mini, weights=d_int * cell_frac, minlength=n)
        i_bas = np.bincount(cell_mini, weights=d_bas * cell_frac, minlength=n)
        q_sup, q_int, q_bas = mgb._reservoir_step(ex, st, i_sup, i_int, i_bas)
        q_loc = q_sup + q_int + q_bas
        local_vol = q_loc * a_mini
        if router is None:
            mgb._route_numpy(topo, ex.c_ch, st.s_ch, local_vol, inflow, q_node)
        else:
            router(topo.order, topo.down, ex.c_ch, st.s_ch, local_vol, inflow, q_node)

        ser['p'][t] = np.dot(p_cell, a_cell)
        ser['et'][t] = np.dot(et, a_cell)
        ser['clip'][t] = np.dot(clip, a_cell)
        ser['d_sup'][t] = np.dot(d_sup, a_cell)
        ser['d_int'][t] = np.dot(d_int, a_cell)
        ser['d_bas'][t] = np.dot(d_bas, a_cell)
        ser['q_sup'][t] = np.dot(q_sup, a_mini)
        ser['q_int'][t] = np.dot(q_int, a_mini)
        ser['q_bas'][t] = np.dot(q_bas, a_mini)
        ser['q_outlet'][t] = q_node[topo.outlets].sum()
        if t >= warmup_days:
            r = t - warmup_days
            q_out_rec[r] = q_node[rec_idx] * to_m3s
            # `inflow` is the router's accumulator: it starts at local_vol and every
            # upstream node adds its outflow before its receiver is processed (the sweep
            # runs upstream -> downstream), so after the sweep it IS total reach inflow.
            sink['qsur_gen_mm'][r] = i_sup
            sink['qsur_rel_mm'][r] = q_sup
            sink['q_local_mm'][r] = q_loc
            sink['reach_inflow_m3s'][r] = inflow * to_m3s
            sink['q_reach_m3s'][r] = q_node * to_m3s

    bal = mgb._assemble_balance(ser, topo, v_start, st.storage_volume(topo), ndays)
    res = mgb.MgbResult(dates=None, record_ids=rec_ids, q_m3s=q_out_rec, series=ser,
                        balance=bal, state=st,
                        wall_time_s=time.perf_counter() - t_start,
                        routing_backend=backend)
    return res, sink


def verify_against_engine(rec: mgb.MgbResult, eng: mgb.MgbResult) -> dict:
    """Prove the recording run IS the engine's run, not merely close to it.

    Returns the measured differences; raises on any of them being non-zero.  Bit
    equality is the right bar here, not a tolerance: both runs execute the same engine
    functions on the same inputs in the same order, so anything other than 0 means the
    day loop above has drifted from `simulate`'s and every recorded field is suspect.
    """
    out = {}
    if rec.q_m3s.shape != eng.q_m3s.shape:
        raise AssertionError(f'recorded q {rec.q_m3s.shape} vs engine {eng.q_m3s.shape}')
    if not np.array_equal(rec.record_ids, eng.record_ids):
        raise AssertionError('recorded column ids differ from the engine run')
    d = float(np.abs(rec.q_m3s.astype(np.float64)
                     - eng.q_m3s.astype(np.float64)).max())
    out['q_m3s_max_abs_diff'] = d
    if d != 0.0:
        raise AssertionError(f'recorded discharge differs from the engine by {d:.3e} m3/s')
    for k, v in eng.series.items():
        dk = float(np.abs(rec.series[k] - v).max())
        out[f'series_{k}_max_abs_diff'] = dk
        if dk != 0.0:
            raise AssertionError(f'basin series {k!r} differs by {dk:.3e}')
    for k, v in eng.balance.items():
        if isinstance(v, (int, float)) and rec.balance[k] != v:
            raise AssertionError(f'balance {k!r}: {rec.balance[k]!r} vs {v!r}')
    out['backend'] = f'{rec.routing_backend}/{eng.routing_backend}'
    return out
