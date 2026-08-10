"""Stage C0 subtask C0.5: freeze the sediment drivers of the adopted H2E run.

    python3.10 src/build_h2e_drivers.py

Writes `data/processed/sim_calibrated_v2/h2e_drivers.npz` - the per-minibacia daily
fields the sediment model (docs/31 C3-C4) consumes, so that sediment evaluation never
re-runs hydrology.  Gitignored and regenerable; this command is the regeneration
command recorded in docs/20.

The run is the SAME run C0.3 reported: same cell, same decoded best-seed parameters, same
2008 warm-up, scored 2009-2018.  `mgb_drivers.simulate_recording` calls the frozen
engine's own kernel functions and its output is asserted bit-identical to
`mgb_hydrology.simulate`'s before anything is written.

Peak RAM is held down by writing each field straight into a memory-mapped `.npy` in a
scratch directory and streaming those into the compressed archive; the scratch files are
removed on success.  Uncompressed the five fields are ~634 MB, which is not something to
hold in RAM next to a 558 MB float64 forcing on a 16 GB box that is often busy.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import sys
import time

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'src'))

import calib_v2 as CV          # noqa: E402
import mgb_drivers as MD       # noqa: E402
import mgb_hydrology as mgb    # noqa: E402

PROC = REPO / 'data' / 'processed'
OUTD = PROC / 'sim_calibrated_v2'
OUT = OUTD / 'h2e_drivers.npz'
SCRATCH = PROC / '_calib_cache' / '_drivers_scratch'

CELL_NAME = 'H2E'
BEST_SEED = 20260901
BALANCE_REL = 1e-6             # C0.5 gate: column sums vs the run's water balance
CHUNK_DAYS = 256               # for the per-reach continuity check


def main() -> int:
    t0 = time.perf_counter()
    print('=' * 78)
    print('C0.5 - precompute and store the sediment drivers   (docs/31 Stage C0)')
    print('=' * 78)

    CV.ensure_cache(CELL_NAME)
    cell = CV.Cell(CELL_NAME, verbose=True)
    assert cell.ET_STRESS == 'fao56' and cell.THETA_CRIT == 0.6, 'H2E cell is not FAO-56'
    run = {k: v for k, v in np.load(
        PROC / '_calib_cache' / f'dds_{CELL_NAME}_{BEST_SEED}.npz', allow_pickle=True).items()}
    x, ro, so = CV.unpack(cell, run['x'])

    topo = cell.TOPO
    n = topo.n_mini
    ndays_sc = len(cell.D_SC)
    print(f'\n  recording {len(MD.FIELDS)} fields x ({ndays_sc}, {n}) float32 = '
          f'{len(MD.FIELDS) * ndays_sc * n * 4 / 1e6:,.0f} MB uncompressed')

    P = np.asarray(cell.P_MM, dtype=np.float64)
    E = np.asarray(cell.E_MM, dtype=np.float64)
    pr = cell.build_params(x, ro, so)
    st, eq_resid, _ = cell.eq_state(pr, P.mean(0), E.mean(0))
    print(f'  equilibrium start re-solved for these parameters, residual {eq_resid:.3e} mm/day')

    # --- the engine's own run, as the reference -------------------------------------
    eng = mgb.simulate(topo, pr, P, E, state=st, warmup_days=cell.NWU,
                       record_ids=cell.REC_IDS, routing_backend='auto')
    print(f'  engine    run: {eng.wall_time_s:6.1f} s  backend {eng.routing_backend}  '
          f'resid_rel {eng.balance["residual_relative"]:.3e}')

    # --- the recording run, into memory-mapped scratch ------------------------------
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True)
    sink = {k: np.lib.format.open_memmap(SCRATCH / f'{k}.npy', mode='w+',
                                        dtype=np.float32, shape=(ndays_sc, n))
            for k in MD.FIELDS}
    rec, sink = MD.simulate_recording(topo, pr, P, E, state=st, warmup_days=cell.NWU,
                                      record_ids=cell.REC_IDS, routing_backend='auto',
                                      sink=sink)
    print(f'  recording run: {rec.wall_time_s:6.1f} s  backend {rec.routing_backend}  '
          f'resid_rel {rec.balance["residual_relative"]:.3e}')
    for v in sink.values():
        v.flush()
    del P, E

    # --- it must BE the engine's run, not merely close to it ------------------------
    v = MD.verify_against_engine(rec, eng)
    print(f'\n  IDENTITY vs mgb_hydrology.simulate: discharge max |diff| '
          f'{v["q_m3s_max_abs_diff"]:.3e} m3/s over {eng.q_m3s.shape}, '
          f'all {len(eng.series)} basin series identical, balance identical')
    assert v['q_m3s_max_abs_diff'] == 0.0

    # --- C0.5 gate part 1: column sums vs the run's water balance --------------------
    print('\n  C0.5 GATE (a): area-weighted column sums vs the run\'s own basin series')
    area = topo.area_km2.astype(np.float64)
    sl = slice(cell.NWU, None)                      # scored days of the full-period series
    to_m3s = mgb.MM_KM2_PER_DAY_TO_M3S
    checks = {
        'qsur_gen_mm': (rec.series['d_sup'][sl], 'd_sup (URH surface generation)'),
        'qsur_rel_mm': (rec.series['q_sup'][sl], 'q_sup (surface reservoir release)'),
        'q_local_mm': (rec.series['q_sup'][sl] + rec.series['q_int'][sl]
                       + rec.series['q_bas'][sl], 'q_sup + q_int + q_bas'),
    }
    worst = 0.0
    for k, (want, what) in checks.items():
        got = (np.asarray(sink[k], dtype=np.float64) * area).sum(axis=1)
        den = np.maximum(np.abs(want), np.abs(want).mean())
        rel = float(np.max(np.abs(got - want) / den))
        tot = float(abs(got.sum() - want.sum()) / abs(want.sum()))
        worst = max(worst, rel, tot)
        print(f'    {k:<17s} vs {what:<34s} daily max rel {rel:.3e}  period total rel {tot:.3e}')
    outl = (np.asarray(sink['q_reach_m3s'][:, topo.outlets], dtype=np.float64).sum(axis=1))
    want = rec.series['q_outlet'][sl] * to_m3s
    rel = float(np.max(np.abs(outl - want) / np.maximum(np.abs(want), np.abs(want).mean())))
    tot = float(abs(outl.sum() - want.sum()) / abs(want.sum()))
    worst = max(worst, rel, tot)
    print(f'    {"q_reach_m3s":<17s} vs {"q_outlet at the basin outlets":<34s} '
          f'daily max rel {rel:.3e}  period total rel {tot:.3e}')
    assert worst < BALANCE_REL, f'C0.5 gate: worst relative mismatch {worst:.3e} >= {BALANCE_REL:.0e}'
    print(f'    worst {worst:.3e} < {BALANCE_REL:.0e} - PASS (the residual is float32 '
          f'storage, not lost mass)')

    # --- C0.5 gate part 2: per-reach continuity of the two routed fields -------------
    # inflow_i = local_i + sum of the outflows of everything draining into i.  This is
    # the only check that ties reach_inflow_m3s and q_reach_m3s together, and it uses
    # ONLY the stored fields - so it also proves the stored pair is self-consistent.
    down = topo.down
    has = np.flatnonzero(down >= 0)
    tgt = down[has]
    worst_c = 0.0
    for a in range(0, ndays_sc, CHUNK_DAYS):
        b = min(a + CHUNK_DAYS, ndays_sc)
        loc = (np.asarray(sink['q_local_mm'][a:b], dtype=np.float64) * area * to_m3s).T
        qr = np.asarray(sink['q_reach_m3s'][a:b], dtype=np.float64).T
        up = np.zeros_like(loc)
        np.add.at(up, tgt, qr[has])
        want_i = loc + up
        got_i = np.asarray(sink['reach_inflow_m3s'][a:b], dtype=np.float64).T
        den = np.maximum(np.abs(want_i), 1e-6)
        worst_c = max(worst_c, float(np.max(np.abs(got_i - want_i) / den)))
    print(f'\n  C0.5 GATE (b): per-reach continuity  inflow = local + sum(upstream outflow)')
    print(f'    worst relative residual over all {ndays_sc} days x {n} reaches: {worst_c:.3e}')
    assert worst_c < BALANCE_REL, f'per-reach continuity broken: {worst_c:.3e}'
    print(f'    PASS (< {BALANCE_REL:.0e})')

    # --- write ----------------------------------------------------------------------
    meta = dict(
        stage='C0.5', cell=CELL_NAME, best_seed=BEST_SEED,
        generated_by='src/build_h2e_drivers.py',
        engine_sha256=hashlib.sha256((REPO / 'src' / 'mgb_hydrology.py').read_bytes()).hexdigest(),
        drivers_sha256=hashlib.sha256((REPO / 'src' / 'mgb_drivers.py').read_bytes()).hexdigest(),
        calib_v2_sha256=hashlib.sha256((REPO / 'src' / 'calib_v2.py').read_bytes()).hexdigest(),
        bundle=cell.bundle, et_stress=cell.ET_STRESS, theta_crit=cell.THETA_CRIT,
        warmup=['2008-01-01', '2008-12-31'],
        scored=[str(cell.D_SC[0].date()), str(cell.D_SC[-1].date())],
        fields={k: u for k, u in MD.FIELDS.items()},
        field_notes={
            'qsur_gen_mm': 'saturation-excess surface runoff GENERATED on the URH columns, '
                           'area-weighted to the minibacia (engine i_sup)',
            'qsur_rel_mm': 'surface runoff RELEASED by the minibacia surface linear '
                           'reservoir (engine q_sup)',
            'q_local_mm': 'total local runoff released to the reach, q_sup+q_int+q_bas',
            'reach_inflow_m3s': 'total daily inflow to the reach: local plus everything '
                                'routed in from upstream',
            'q_reach_m3s': 'routed reach outflow at EVERY minibacia (the engine records '
                           'this only at gauges)'},
        musle_qsurf_choice='NOT MADE HERE - docs/31 C3.3 registers whether MUSLE Qsurf is '
                           'qsur_gen_mm or qsur_rel_mm; both are stored so that choice '
                           'never requires re-running hydrology (journal_c0.md P5)',
        identity_check=v,
        balance_gate={'worst_relative': worst, 'bar': BALANCE_REL},
        continuity_gate={'worst_relative': worst_c, 'bar': BALANCE_REL},
        balance=dict(rec.balance),
        area_embargo='per-area yields (t/km2/yr) are EMBARGOED until docs/31 B3 delivers an '
                     'external catchment-area arbiter (docs/23 s13.2); own_area_km2 and '
                     'upstream_area_km2 are stored for routing geometry, not for yields',
    )
    print(f'\n  writing {OUT.name} (compressing ~'
          f'{len(MD.FIELDS) * ndays_sc * n * 4 / 1e6:,.0f} MB) ...', flush=True)
    tw = time.perf_counter()
    np.savez_compressed(
        OUT,
        dates=cell.D_SC.to_numpy().astype('datetime64[D]'),
        minibacia_id=topo.ids.astype(np.int64),
        own_area_km2=topo.area_km2.astype(np.float64),
        upstream_area_km2=cell.TOP['upstream_area_km2'].astype(np.float64),
        downstream_id=cell.TOP['downstream_id'].astype(np.int64),
        reach_km=cell.REACH_KM.astype(np.float64),
        gauge_code=cell.GC, gauge_minibacia_idx=cell.GMIDX[cell.JP].astype(np.int64),
        meta=np.array([json.dumps(meta, default=str)]),
        **{k: sink[k] for k in MD.FIELDS})
    print(f'  written in {time.perf_counter()-tw:.0f} s, '
          f'{OUT.stat().st_size/1e6:,.1f} MB on disk')

    # --- C0.5 gate part 3: np.load round trip ---------------------------------------
    for vv in sink.values():
        del vv
    sink.clear()
    z = np.load(OUT, allow_pickle=False)
    print(f'\n  C0.5 GATE (c): np.load round trip')
    print(f'    keys: {sorted(z.files)}')
    mm = {k: np.load(SCRATCH / f'{k}.npy', mmap_mode='r') for k in MD.FIELDS}
    for k in MD.FIELDS:
        a = z[k]
        assert a.shape == (ndays_sc, n) and a.dtype == np.float32, f'{k}: {a.shape} {a.dtype}'
        d = float(np.abs(a.astype(np.float64) - np.asarray(mm[k], np.float64)).max())
        nn = int(np.isnan(a).sum())
        print(f'    {k:<17s} {a.shape} {str(a.dtype):<8s} max |reload - written| {d:.3e}  '
              f'NaN {nn}  min {float(a.min()):.4g}  max {float(a.max()):.4g}')
        assert d == 0.0, f'{k} did not survive the round trip'
        assert nn == 0, f'{k} contains {nn} NaNs'
        assert float(a.min()) >= 0.0, f'{k} contains negative values'
    m2 = json.loads(str(z['meta'][0]))
    assert m2['cell'] == CELL_NAME and m2['best_seed'] == BEST_SEED
    assert np.array_equal(z['dates'], cell.D_SC.to_numpy().astype('datetime64[D]'))
    print(f'    meta round trip OK: cell {m2["cell"]}, seed {m2["best_seed"]}, '
          f'{len(m2["fields"])} fields, scored {m2["scored"][0]}..{m2["scored"][1]}')
    print('    PASS')

    # a physical sanity line, reported not asserted: basin-mean annual depths
    yrs = ndays_sc / 365.25
    print(f'\n  SANITY (reported, not gated): basin-mean over {yrs:.2f} yr, '
          f'area-weighted')
    for k in ('qsur_gen_mm', 'qsur_rel_mm', 'q_local_mm'):
        tot = float((np.asarray(mm[k], np.float64) * area).sum() / area.sum() / yrs)
        print(f'    {k:<17s} {tot:8.1f} mm/yr')
    print(f'    {"outlet":<17s} {rec.balance["runoff_mm"] / (rec.balance["ndays"]/365.25):8.1f}'
          f' mm/yr (full period incl. warm-up)   RC '
          f'{rec.balance["runoff_coefficient"]:.4f}')
    for k in list(mm):
        del mm[k]
    z.close()
    shutil.rmtree(SCRATCH, ignore_errors=True)
    print(f'\nC0.5 COMPLETE in {(time.perf_counter()-t0)/60:.1f} min  -> {OUT}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
