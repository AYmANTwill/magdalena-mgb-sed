"""Engine-grade tests for ``src/mgb_transport.py`` (channel transport, stage C4.1).

The five gates come from the C4.1 brief verbatim:

1. **mass conservation** - at ``k_dep`` = 0 the load leaving the outlet equals the total
   hillslope load delivered, EXACTLY (bitwise wherever the arithmetic is exact; on real float
   drivers the residual is pure cross-reach re-association rounding and is MEASURED, which is
   what the module docstring's MASS LEDGER section says in advance);
2. **deposition accounting** - with ``k_dep`` > 0, ``delivered = exported + deposited``
   exactly;
3. **strict monotonicity** - more deposition, strictly less outlet load;
4. **topological correctness** - a load injected in one headwater reaches the outlet and
   nowhere else upstream of it;
5. **NaN-free over the full basin decade**.

Two things are deliberately NOT tested here.  The *magnitude* of ``k_dep``: nothing in this
module is calibrated, C4.3 fits it under ``docs/42`` G1-G9.  And any per-area yield: t/km²/yr
is EMBARGOED (``docs/23`` §13.2) and no test in this file divides anything by an area.
"""

import math
import pathlib

import numpy as np
import pytest

import mgb_transport as tr

PROCESSED = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"
TOPOLOGY = PROCESSED / "model_inputs_v2" / "topology.npz"
DRIVERS = PROCESSED / "sim_calibrated_v2" / "h2e_drivers.npz"
HAVE_CSVS = all(
    (PROCESSED / f).is_file()
    for f in ("minibacias.csv", "urh_fractions.csv", "minibacia_soil_params.csv",
              "urh_cp_factors.csv", "urh_ls2d.csv")
)
needs_topology = pytest.mark.skipif(
    not TOPOLOGY.is_file(), reason="model_inputs_v2/topology.npz not present (gitignored)"
)
needs_full_basin = pytest.mark.skipif(
    not (TOPOLOGY.is_file() and DRIVERS.is_file() and HAVE_CSVS),
    reason="full-basin inputs not present (topology.npz / h2e_drivers.npz / processed CSVs)",
)


# --------------------------------------------------------------------------------------
# synthetic networks
# --------------------------------------------------------------------------------------


def _chain(n=4, reach_km=None):
    """A straight chain 0 -> 1 -> ... -> n-1, the outlet last."""
    down = list(range(1, n)) + [-1]
    km = [1.0] * n if reach_km is None else list(reach_km)
    return tr.build_network(ids=list(range(100, 100 + n)), downstream_idx=down,
                            reach_km=km, own_area_km2=[10.0] * n)


def _forked():
    """Two headwaters (0, 1) -> junction 2 -> 3 -> outlet 4, plus an independent limb 5 -> 3.

    ids 10..15.  Nothing is symmetric: reach lengths and areas all differ, so a test cannot
    pass by accident through a coincidence of equal numbers.
    """
    return tr.build_network(
        ids=[10, 11, 12, 13, 14, 15],
        downstream_idx=[2, 2, 3, 4, -1, 3],
        reach_km=[3.0, 7.0, 11.0, 13.0, 17.0, 5.0],
        own_area_km2=[12.0, 23.0, 31.0, 44.0, 57.0, 9.0],
    )


def _integer_loads(net, ndays=7, seed=3, hi=64):
    """Loads that are exactly-representable small integers.

    Every partial sum stays far below 2**53, so float addition is EXACT regardless of
    association order.  That is what makes the bitwise global mass test meaningful: any
    difference between the outlet total and the input total would then be a real leak, not
    rounding.
    """
    rng = np.random.default_rng(seed)
    return rng.integers(0, hi, size=(ndays, net.n_reach)).astype(np.float64)


def _float_loads(net, ndays=13, seed=5):
    rng = np.random.default_rng(seed)
    wet = rng.random((ndays, net.n_reach)) < 0.6
    return np.where(wet, rng.gamma(1.4, 30.0, (ndays, net.n_reach)), 0.0)


# --------------------------------------------------------------------------------------
# 0. the network itself
# --------------------------------------------------------------------------------------


def test_network_rejects_a_cycle():
    with pytest.raises(ValueError, match="cycle"):
        tr.build_network([1, 2], [1, 0], [1.0, 1.0], [5.0, 5.0])


def test_network_rejects_a_self_draining_reach():
    with pytest.raises(ValueError, match="self-draining"):
        tr.build_network([1, 2], [0, -1], [1.0, 1.0], [5.0, 5.0])


def test_network_rejects_duplicate_ids_and_bad_shapes():
    with pytest.raises(ValueError, match="duplicate"):
        tr.build_network([1, 1], [1, -1], [1.0, 1.0], [5.0, 5.0])
    with pytest.raises(ValueError, match="reach_km"):
        tr.build_network([1, 2], [1, -1], [1.0], [5.0, 5.0])


def test_network_rejects_a_receiver_past_the_end():
    with pytest.raises(ValueError, match="past the end"):
        tr.build_network([1, 2], [5, -1], [1.0, 1.0], [5.0, 5.0])


def test_levels_are_a_valid_topological_stratification():
    net = _forked()
    for i in range(net.n_reach):
        j = net.down[i]
        if j >= 0:
            assert net.level[j] > net.level[i]


def test_hops_to_outlet_counts_the_path():
    net = _chain(5)
    assert net.hops_to_outlet.tolist() == [4, 3, 2, 1, 0]


def test_negative_parameters_are_rejected_because_they_would_create_sediment():
    with pytest.raises(ValueError, match="CREATE sediment"):
        tr.TransportParams(k_dep=-1e-6)
    with pytest.raises(ValueError, match="CREATE sediment"):
        tr.TransportParams(tau_channel_days=-1.0)
    with pytest.raises(ValueError, match="dep_mode"):
        tr.TransportParams(dep_mode="whatever")


def test_params_are_frozen():
    p = tr.TransportParams()
    with pytest.raises(Exception):
        p.k_dep = 1.0


def test_default_coefficients_are_exactly_zero_and_exactly_one():
    """The whole bitwise story rests on these two being EXACT, not merely tiny/close."""
    net = _forked()
    p = tr.TransportParams()
    assert np.all(p.deposition_coef(net) == 0.0)
    assert np.all(p.release_coef(net) == 1.0)


def test_default_params_declare_the_sdr_1_claim_and_the_missing_momposina():
    """docs/42 G5: a run with no named sink must say SDR = 1.0 in the report, not imply it."""
    s = tr.TransportParams().summary(_forked())
    assert s["asserts_sdr_1"] is True
    assert s["named_sink"] == "none (k_dep = 0)"
    assert s["momposina_represented"] is False
    s2 = tr.TransportParams(k_dep=1e-3).summary(_forked())
    assert s2["asserts_sdr_1"] is False
    assert "k_dep" in s2["named_sink"]


def test_the_momposina_limitation_is_declared_in_the_module_and_in_the_router():
    """The limitation must be IN THE CODE, before any fit - docs/31 §C4.1.

    Asserted on the docstrings themselves so it cannot be quietly deleted: the mitigation
    rule (calibrate upstream, evaluate below) and the docs/22 §4.6 citation are load-bearing.
    """
    for text in (tr.__doc__, tr.route_day.__doc__):
        low = text.lower()
        assert "momposina" in low or "mompós" in low or "mompos" in low
        assert "not represented" in low
        assert "over-deliver" in low
        assert "never calibrate" in low
        assert "22" in text and "4.6" in text
    assert "0.221" in tr.__doc__
    assert "measured cost" in tr.MOMPOSINA_NOTE.lower()


# --------------------------------------------------------------------------------------
# 1. MASS CONSERVATION at deposition = 0
# --------------------------------------------------------------------------------------


def test_mass_conservation_bitwise_on_a_synthetic_network():
    """k_dep = 0, tau = 0: exported == delivered, to the last bit, and nothing is stored."""
    net = _forked()
    load = _integer_loads(net, ndays=9)
    res = tr.simulate_transport(net, tr.TransportParams(), load)
    assert res.ledger["deposited_t"] == 0.0
    assert res.ledger["store_end_t"] == 0.0
    assert res.ledger["exported_t"] == res.ledger["local_in_t"]
    assert res.ledger["residual_t"] == 0.0
    assert res.ledger["exact"] is True


@needs_topology
def test_mass_conservation_bitwise_on_the_real_8672_reach_basin():
    """The same claim on the real network, with exactly-representable loads.

    8,672 reaches x integer tonnes keeps every partial sum well below 2**53, so float
    addition is exact and the equality is BITWISE. Any difference here would be a real leak.
    """
    net = tr.load_network(TOPOLOGY)
    load = _integer_loads(net, ndays=5, seed=17)
    res = tr.simulate_transport(net, tr.TransportParams(), load, store_daily=False)
    assert res.ledger["exported_t"] == res.ledger["local_in_t"]
    assert res.ledger["residual_t"] == 0.0
    assert res.ledger["deposited_t"] == 0.0
    assert res.ledger["store_end_t"] == 0.0


def test_the_per_reach_partition_residual_is_exactly_zero_for_every_parameter_value():
    """The module's strongest mass statement: structural, not tolerance-based.

    ((S - dep) - out) - store' is identically 0.0 in IEEE-754 whatever k_dep and tau are.
    """
    net = _forked()
    load = _float_loads(net, ndays=11)
    for params in (tr.TransportParams(),
                   tr.TransportParams(k_dep=0.02),
                   tr.TransportParams(k_dep=0.3, tau_channel_days=2.5),
                   tr.TransportParams(k_dep=0.05, dep_mode="per_day",
                                      tau_channel_days=1.7)):
        res = tr.simulate_transport(net, params, load)
        assert res.ledger["max_node_residual_t"] == 0.0
        assert res.ledger["node_partition_exact"] is True


def test_a_nan_local_load_is_rejected_at_the_door():
    """The cheap screen: a non-finite load never reaches the router at all.

    Documented as a test because it is what makes the NaN residual below reachable ONLY by
    overflow - without this screen there would be a much easier path to the same failure.
    """
    net = _forked()
    load = _float_loads(net, ndays=6)
    load[2, 1] = np.nan
    with pytest.raises(ValueError, match="non-finite"):
        tr.simulate_transport(net, tr.TransportParams(), load)


def test_the_partition_claim_does_not_survive_an_overflowing_run():
    """`node_partition_exact` must not be True on a run whose mass is NaN.

    The residual tracker compared `m > max_resid`, and in IEEE-754 every comparison against
    NaN is False - so a NaN residual left max_resid at its 0.0 initial value and the ledger
    then announced `node_partition_exact: True`, the module's STRONGEST mass statement, on a
    run carrying no usable mass.

    This is reachable WITHOUT passing a NaN in: the loads below are all finite, so they pass
    the screen above, but they are large enough that accumulation overflows to inf, and
    inf - inf = NaN inside the residual.  A finite-input screen structurally cannot see a
    defect that is manufactured during the arithmetic - the same lesson as the precipitation
    zero-suppression (a value screen cannot see absent records).

    The fix tests the negation (`not (m <= max_resid)`), which IS True for NaN.
    """
    net = _forked()
    load = np.full((6, net.ids.size), 1e308, dtype=np.float64)
    assert np.all(np.isfinite(load)), "the point of this test is that the INPUT is finite"

    with np.errstate(over="ignore", invalid="ignore"):
        res = tr.simulate_transport(net, tr.TransportParams(), load)

    assert not math.isfinite(res.ledger["exported_t"]), (
        "test premise broken: this run was supposed to overflow"
    )
    assert not res.ledger["node_partition_exact"], (
        "a run with non-finite mass reported an exact per-reach partition"
    )
    assert math.isnan(res.ledger["max_node_residual_t"]), (
        "the NaN residual was swallowed instead of being reported"
    )


def test_mass_conservation_on_real_valued_loads_is_rounding_only():
    """Float loads: the global identity is re-association rounding, and it is tiny."""
    net = _forked()
    res = tr.simulate_transport(net, tr.TransportParams(), _float_loads(net))
    assert res.ledger["residual_relative"] < 1e-14


def test_a_channel_store_delays_mass_without_destroying_it():
    """With tau > 0 and no deposition the ledger closes through the storage term."""
    net = _chain(6)
    load = _float_loads(net, ndays=25, seed=9)
    res = tr.simulate_transport(net, tr.TransportParams(tau_channel_days=3.0), load)
    assert res.ledger["deposited_t"] == 0.0
    assert res.ledger["store_end_t"] > 0.0
    assert res.ledger["residual_relative"] < 1e-14
    assert res.ledger["exported_t"] < res.ledger["local_in_t"]


# --------------------------------------------------------------------------------------
# 2. DEPOSITION ACCOUNTING: eroded = delivered + deposited, exactly
# --------------------------------------------------------------------------------------


def test_deposition_accounting_is_bitwise_on_a_hand_checkable_chain():
    """A 3-reach chain, local 1 t each, deposition coefficient exactly 1/2.

    Every quantity is a dyadic rational at low precision, so the identity is BITWISE:
        A: S=1     dep=0.5    out=0.5
        B: S=1.5   dep=0.75   out=0.75
        C: S=1.75  dep=0.875  out=0.875   <- outlet
        3.0 = 0.875 + (0.5 + 0.75 + 0.875)
    """
    net = _chain(3, reach_km=[1.0, 1.0, 1.0])
    # k_dep such that 1 - exp(-k_dep * 1 km) == 0.5 exactly-representable target
    k = -math.log(0.5)
    params = tr.TransportParams(k_dep=k)
    assert np.allclose(params.deposition_coef(net), 0.5, rtol=0, atol=1e-16)
    load = np.ones((1, 3), dtype=np.float64)
    res = tr.simulate_transport(net, params, load)
    assert res.outlet_t_day[0] == 0.875
    assert res.ledger["deposited_t"] == 2.125
    assert res.ledger["local_in_t"] == 3.0
    assert res.ledger["exported_t"] + res.ledger["deposited_t"] == res.ledger["local_in_t"]
    assert res.ledger["residual_t"] == 0.0


def test_deposition_accounting_closes_on_the_forked_network_with_integer_loads():
    net = _forked()
    load = _integer_loads(net, ndays=6, seed=23)
    res = tr.simulate_transport(net, tr.TransportParams(k_dep=-math.log(0.5)), load)
    assert res.ledger["store_end_t"] == 0.0
    assert res.ledger["deposited_t"] > 0.0
    assert res.ledger["residual_relative"] < 1e-15


@needs_topology
def test_deposition_accounting_closes_on_the_real_basin():
    net = tr.load_network(TOPOLOGY)
    load = _float_loads(net, ndays=4, seed=31)
    res = tr.simulate_transport(net, tr.TransportParams(k_dep=2e-3), load, store_daily=False)
    led = res.ledger
    assert led["deposited_t"] > 0.0
    assert led["max_node_residual_t"] == 0.0
    assert led["residual_relative"] < 1e-13
    assert led["exported_t"] < led["local_in_t"]


# --------------------------------------------------------------------------------------
# 3. MONOTONICITY: more deposition -> strictly less outlet load
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize("mode,taus", [("per_km", 0.0), ("per_day", 2.0)])
def test_outlet_load_strictly_decreases_with_deposition(mode, taus):
    net = _forked()
    load = _float_loads(net, ndays=30, seed=41)
    totals = []
    for k in (0.0, 1e-4, 1e-3, 1e-2, 5e-2, 0.2):
        res = tr.simulate_transport(
            net, tr.TransportParams(k_dep=k, dep_mode=mode, tau_channel_days=taus),
            load, store_daily=False)
        totals.append(math.fsum(res.outlet_t_day.tolist()))
    assert all(a > b for a, b in zip(totals, totals[1:])), totals


def test_deposition_is_strictly_monotone_reach_by_reach_too():
    """Not only the outlet: every reach's period load must be non-increasing, and the ones
    with upstream area strictly decreasing."""
    net = _forked()
    load = _float_loads(net, ndays=20, seed=43)
    a = tr.simulate_transport(net, tr.TransportParams(), load).accum_load_t
    b = tr.simulate_transport(net, tr.TransportParams(k_dep=1e-2), load).accum_load_t
    assert np.all(b <= a)
    assert np.all(b < a)          # every reach deposits something, since every reach_km > 0


@needs_topology
def test_outlet_load_strictly_decreases_with_deposition_on_the_real_basin():
    net = tr.load_network(TOPOLOGY)
    load = _float_loads(net, ndays=3, seed=47)
    prev = None
    for k in (0.0, 1e-5, 1e-4, 1e-3):
        res = tr.simulate_transport(net, tr.TransportParams(k_dep=k), load,
                                    store_daily=False)
        total = math.fsum(res.outlet_t_day.tolist())
        if prev is not None:
            assert total < prev
        prev = total


def test_per_km_deposition_is_discretisation_invariant():
    """The reason ``per_km`` is the default: splitting a reach must not change delivery.

    One 12 km reach vs four 3 km reaches carrying the same total load at the head: the
    surviving fraction at the outlet must agree to rounding, because retention along a path
    is ``exp(-k_dep * path_km)`` either way.  A per-STEP coefficient fails this test, which
    is exactly why it is not the default.
    """
    k = 0.05
    coarse = tr.build_network([1, 2], [1, -1], [12.0, 1e-12], [10.0, 10.0])
    fine = tr.build_network([1, 2, 3, 4, 5], [1, 2, 3, 4, -1],
                            [3.0, 3.0, 3.0, 3.0, 1e-12], [10.0] * 5)
    lc = np.zeros((1, 2)); lc[0, 0] = 1000.0
    lf = np.zeros((1, 5)); lf[0, 0] = 1000.0
    rc = tr.simulate_transport(coarse, tr.TransportParams(k_dep=k), lc)
    rf = tr.simulate_transport(fine, tr.TransportParams(k_dep=k), lf)
    assert rc.outlet_t_day[0] == pytest.approx(rf.outlet_t_day[0], rel=1e-12)
    assert rc.outlet_t_day[0] == pytest.approx(1000.0 * math.exp(-k * 12.0), rel=1e-9)


def test_per_day_mode_warns_when_it_is_meaningless():
    net = _forked()
    with pytest.warns(UserWarning, match="NOT a daily rate"):
        tr.TransportParams(k_dep=0.1, dep_mode="per_day").deposition_coef(net)


# --------------------------------------------------------------------------------------
# 4. TOPOLOGICAL CORRECTNESS
# --------------------------------------------------------------------------------------


def test_a_headwater_injection_reaches_the_outlet_and_nowhere_off_its_path():
    net = _forked()
    load = np.zeros((1, net.n_reach))
    load[0, 0] = 500.0                      # headwater id 10
    res = tr.simulate_transport(net, tr.TransportParams(), load)
    path = net.downstream_path(0)           # 0 -> 2 -> 3 -> 4
    assert path.tolist() == [0, 2, 3, 4]
    assert res.outlet_t_day[0] == 500.0
    assert np.all(res.accum_load_t[path] == 500.0)
    off = np.setdiff1d(np.arange(net.n_reach), path)
    assert np.all(res.accum_load_t[off] == 0.0)


def test_nothing_travels_upstream_even_when_the_receiver_is_loaded():
    """A load placed downstream must leave every upstream reach at exactly zero."""
    net = _forked()
    load = np.zeros((1, net.n_reach))
    load[0, 3] = 90.0                       # reach 13, one hop above the outlet
    res = tr.simulate_transport(net, tr.TransportParams(), load)
    assert res.accum_load_t[3] == 90.0
    assert res.accum_load_t[4] == 90.0
    assert np.all(res.accum_load_t[[0, 1, 2, 5]] == 0.0)


@needs_topology
def test_headwater_injection_on_the_real_basin_hits_exactly_its_own_path():
    """Real 8,672-reach network: one unit dropped in a headwater lights up its flow path and
    nothing else, and the outlet receives all of it."""
    net = tr.load_network(TOPOLOGY)
    head = int(np.flatnonzero(net.level == 0)[7])
    load = np.zeros((1, net.n_reach))
    load[0, head] = 1024.0
    res = tr.simulate_transport(net, tr.TransportParams(), load)
    path = net.downstream_path(head)
    assert path.size == net.hops_to_outlet[head] + 1
    assert np.all(res.accum_load_t[path] == 1024.0)
    on = np.zeros(net.n_reach, dtype=bool)
    on[path] = True
    assert np.all(res.accum_load_t[~on] == 0.0)
    assert res.outlet_t_day[0] == 1024.0


@needs_topology
def test_upstream_mask_and_downstream_path_are_consistent():
    net = tr.load_network(TOPOLOGY)
    node = int(np.flatnonzero(net.hops_to_outlet == 40)[0])
    mask = net.upstream_mask(node)
    # every masked reach must have `node` on its downstream path
    picks = np.flatnonzero(mask)[:: max(1, mask.sum() // 25)]
    for i in picks:
        assert node in net.downstream_path(int(i)).tolist()
    assert not mask[net.down[node]]


def test_backends_agree():
    """Two independent implementations of the same sweep - the project's standing discipline."""
    net = _forked()
    load = _float_loads(net, ndays=40, seed=53)
    p = tr.TransportParams(k_dep=3e-3, tau_channel_days=1.5)
    a = tr.simulate_transport(net, p, load, backend="levels")
    b = tr.simulate_transport(net, p, load, backend="order")
    assert np.allclose(a.accum_load_t, b.accum_load_t, rtol=1e-12, atol=0.0)
    assert np.allclose(a.outlet_t_day, b.outlet_t_day, rtol=1e-12, atol=0.0)


@needs_topology
def test_backends_agree_on_the_real_network():
    net = tr.load_network(TOPOLOGY)
    load = _float_loads(net, ndays=3, seed=59)
    p = tr.TransportParams(k_dep=1e-3)
    a = tr.simulate_transport(net, p, load, store_daily=False, backend="levels")
    b = tr.simulate_transport(net, p, load, store_daily=False, backend="order")
    assert np.allclose(a.accum_load_t, b.accum_load_t, rtol=1e-11, atol=0.0)
    assert a.ledger["exported_t"] == pytest.approx(b.ledger["exported_t"], rel=1e-12)


# --------------------------------------------------------------------------------------
# input screens
# --------------------------------------------------------------------------------------


def test_nonfinite_and_negative_local_loads_are_rejected_not_propagated():
    net = _forked()
    load = _float_loads(net, ndays=4)
    bad = load.copy(); bad[1, 2] = np.nan
    with pytest.raises(ValueError, match="non-finite"):
        tr.simulate_transport(net, tr.TransportParams(), bad)
    bad = load.copy(); bad[0, 0] = -1.0
    with pytest.raises(ValueError, match="negative"):
        tr.simulate_transport(net, tr.TransportParams(), bad)


def test_wrong_shape_and_mislabelled_dates_are_rejected():
    net = _forked()
    with pytest.raises(ValueError, match="local_load_t_day must be"):
        tr.simulate_transport(net, tr.TransportParams(), np.zeros((3, 2)))
    with pytest.raises(ValueError, match="mislabels the output time axis"):
        tr.simulate_transport(net, tr.TransportParams(), np.zeros((3, net.n_reach)),
                              dates=["a", "b"])


@needs_topology
def test_a_scrambled_column_order_raises_instead_of_routing_the_wrong_basin():
    with np.load(TOPOLOGY, allow_pickle=False) as z:
        ids = z["minibacia_id"].astype(np.int64)
    with pytest.raises(ValueError, match="silently scrambles"):
        tr.load_network(TOPOLOGY, mini_ids=ids[::-1])
    net = tr.load_network(TOPOLOGY, mini_ids=ids)      # the aligned case must pass
    assert net.n_reach == ids.size


def test_channel_tau_from_celerity_is_length_over_speed():
    net = _chain(3, reach_km=[8.64, 17.28, 4.32])
    tau = tr.channel_tau_from_celerity(net, 1.0)
    assert tau == pytest.approx([0.1, 0.2, 0.05], rel=1e-12)
    with pytest.raises(ValueError):
        tr.channel_tau_from_celerity(net, 0.0)


# --------------------------------------------------------------------------------------
# the calibrate-upstream / evaluate-below split
# --------------------------------------------------------------------------------------


def test_station_split_puts_below_reference_stations_in_evaluate_only():
    net = _forked()
    out = tr.split_stations_by_momposina(net, [10, 12, 13, 15, 14],
                                         momposina_ref_minibacia=13)
    assert set(out["calibrate"]) == {10, 12, 13, 15}
    assert out["evaluate_only"] == [14]
    assert "never calibrate" in out["rule"]
    assert "OVER-DELIVERY" in out["note"]


def test_station_split_keeps_a_sibling_tributary_in_the_calibration_set():
    """The bug this test exists for: reach 15 joins reach 3 (the reference) from the side.

    Under a 'drains through the reference' reading it would be excluded; it must not be,
    because it sits ABOVE the reference's confluence, not below it. On the real basin this
    is the difference between keeping and losing every Cauca station.
    """
    net = _forked()
    out = tr.split_stations_by_momposina(net, [15], momposina_ref_minibacia=13)
    assert out["calibrate"] == [15]
    assert out["evaluate_only"] == []


@needs_topology
def test_the_real_momposina_split_reproduces_the_published_801_1_km():
    """docs/42 §4.5 / G9: 801.1 km of channel - the whole Momposina - lies below 21237020.

    Computed here from topology.npz alone. If this drifts, either the network changed or the
    reference station did; reconcile with docs/42, do not relax the test.
    """
    net = tr.load_network(TOPOLOGY)
    out = tr.split_stations_by_momposina(net, [12354], momposina_ref_minibacia=12354)
    assert out["channel_km_below_reference"] == pytest.approx(801.1, abs=0.1)
    assert out["calibrate"] == [12354]        # the reference itself is ABOVE the sink


# --------------------------------------------------------------------------------------
# 5. THE FULL BASIN DECADE
# --------------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def basin_decade():
    """Hillslope load (mgb_sediment, adopted defaults) routed at k_dep = 0 over 2009-2018."""
    import mgb_sediment as sed

    net = tr.load_network(TOPOLOGY)
    drivers = sed.load_drivers(DRIVERS)
    geom = sed.load_geometry(PROCESSED, mini_ids=drivers.mini_ids)
    # dtype_out=float64 for the COUPLING array, deliberately: mgb_sediment's default float32
    # output rounds each daily minibacia load at ~1e-7 relative, which shows up as a 3.9e-11
    # relative gap between the two modules' ledgers - measured, and large enough to swamp the
    # 1e-13 mass gate below. The gap is a storage precision artefact, not a leak, but a mass
    # test must not be silently absorbing one.
    hill = sed.simulate_sediment(geom, sed.SedParams(), drivers.qsur_mm,
                                 dates=drivers.dates, store_daily=True,
                                 dtype_out=np.float64)
    net = tr.load_network(TOPOLOGY, mini_ids=drivers.mini_ids)
    res = tr.simulate_transport(net, tr.TransportParams(), hill.delivered_t_day,
                                dates=drivers.dates, store_daily=False)
    return net, hill, res


@needs_full_basin
def test_full_basin_decade_is_nan_free(basin_decade):
    _, _, res = basin_decade
    assert np.all(np.isfinite(res.outlet_t_day))
    assert np.all(np.isfinite(res.accum_load_t))
    assert np.all(np.isfinite(res.deposited_t))
    for k, v in res.series.items():
        assert np.all(np.isfinite(v)), k
    assert np.all(res.accum_load_t >= 0.0)
    assert res.outlet_t_day.size == 3652


@needs_full_basin
def test_full_basin_decade_conserves_mass_at_zero_deposition(basin_decade):
    """The C4.1 gate on real drivers: nothing deposited, nothing stored, outlet == hillslope.

    The residual here is cross-reach re-association rounding only - the per-reach partition
    residual (the exact statement) is asserted to be literally 0.0 alongside it.
    """
    _, hill, res = basin_decade
    led = res.ledger
    assert led["deposited_t"] == 0.0
    assert led["store_end_t"] == 0.0
    assert led["max_node_residual_t"] == 0.0
    assert led["residual_relative"] < 1e-13
    assert led["local_in_t"] == pytest.approx(hill.ledger["delivered_t"], rel=1e-12)


@needs_full_basin
def test_full_basin_decade_load_increases_downstream_at_zero_deposition(basin_decade):
    """With no sink the routed load can only accumulate: a reach must carry at least what
    each of its contributors carries."""
    net, _, res = basin_decade
    a = res.accum_load_t
    linked = net.down >= 0
    assert np.all(a[net.down[linked]] >= a[linked] - 1e-6 * np.maximum(a[linked], 1.0))


@needs_full_basin
def test_full_basin_decade_outlet_equals_the_hillslope_total(basin_decade):
    """Restated as the headline: at k_dep = 0 the model asserts SDR = 1.0 (docs/42 G5)."""
    _, hill, res = basin_decade
    assert math.fsum(res.outlet_t_day.tolist()) == pytest.approx(
        hill.ledger["delivered_t"], rel=1e-12)
    assert res.params.summary()["asserts_sdr_1"] is True
