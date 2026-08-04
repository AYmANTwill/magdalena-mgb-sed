"""Mass balance of the daily water-balance engine on a tiny synthetic topology.

Three minibacias in a chain (1 -> 2 -> 3 -> outlet), two URH types with area,
100 days of synthetic forcing. The budget identity
P + clip = ET + Q_outlet + (storage_end - storage_start)
must close to float precision (residual_relative < 1e-10) with no NaNs anywhere.
"""
import numpy as np
import pytest

import mgb_hydrology as mgb

N_DAYS = 100


def _chain_topology():
    ids = [1, 2, 3]
    area_km2 = [10.0, 20.0, 30.0]
    downstream = [2, 3, -1]                       # 1 -> 2 -> 3 -> outlet
    urh = np.zeros((3, mgb.N_URH))
    urh[:, 0] = 0.6                               # URH 11 (coarse forest)
    urh[:, 12] = 0.4                              # URH 25 (medium urban)
    return mgb.build_topology(ids, area_km2, downstream, urh)


def _forcing(seed=3):
    rng = np.random.default_rng(seed)
    wet = rng.random((N_DAYS, 3)) < 0.45
    precip = np.where(wet, rng.gamma(1.2, 9.0, (N_DAYS, 3)), 0.0)
    pet = np.full((N_DAYS, 3), 4.0)
    return precip, pet


@pytest.mark.parametrize("percolation", ["linear", "mgb"])
def test_mass_balance_closes(percolation):
    topo = _chain_topology()
    params = mgb.MgbParams(percolation=percolation)
    precip, pet = _forcing()
    res = mgb.simulate(topo, params, precip, pet, routing_backend="numpy")
    bal = res.balance
    assert bal["residual_relative"] < 1e-10, bal
    assert not np.isnan(res.q_m3s).any()
    assert np.isfinite(res.q_m3s).all()
    assert (res.q_m3s >= 0).all()
    assert bal["clip_volume_mm_km2"] < 1e-9 * max(bal["p_volume_mm_km2"], 1.0)


def test_series_finite_and_chain_accumulates():
    topo = _chain_topology()
    precip, pet = _forcing()
    res = mgb.simulate(topo, mgb.MgbParams(), precip, pet, routing_backend="numpy")
    for name, series in res.series.items():
        assert np.isfinite(series).all(), f"series {name!r} has non-finite values"
    # water is only added downstream, so the outlet node carries the most flow
    assert res.q_at(3).mean() > res.q_at(1).mean()
