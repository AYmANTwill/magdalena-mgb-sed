"""Channel transport of the suspended load (stage C4.1).

WHAT THIS IS
------------
The channel half of the sediment model, and nothing else.  It takes the **hillslope load
delivered to each minibacia's reach**, in tonnes/day, which is exactly what
:func:`mgb_sediment.simulate_sediment` returns, and advects it down the reach network in
``data/processed/model_inputs_v2/topology.npz`` with

* a per-reach **linear storage reservoir** (Muskingum with ``X`` = 0), the same operator
  ``mgb_hydrology._route_numpy`` applies to water, and
* a per-reach **first-order deposition / settling** term, a NAMED parameter
  (:attr:`TransportParams.k_dep`) whose default is exactly **0.0**, so the no-deposition
  case - "every gram eroded on a hillslope reaches the outlet" - is the reproducible
  baseline against which any sink is measured.

It is a SEPARATE module from ``src/mgb_sediment.py`` on purpose, and the reason is written
into that file: its docstring states "It is NOT a channel model.  Advection, deposition and
the Momposina floodplain sink are stage C4 (``docs/31`` §C4.1) and deliberately absent here:
this module's output is the *input* to that step, so anything it produced downstream of the
hillslope would be double-counted later."  Putting channel transport inside it would falsify
that claim and blur the one boundary the double-counting warning depends on.  Keeping the two
apart also keeps the two mass ledgers independent - the hillslope ledger
(``eroded = delivered + stored``) closes inside ``mgb_sediment``, the channel ledger
(``delivered_in = outlet + deposited + in-channel storage``) closes here - so a leak can be
localised to one of them.

It re-runs NOTHING and fits NOTHING.  No parameter in this module has been calibrated; C4.3
does that, held to ``docs/42`` G1-G9.

=====================================================================================
THE LIMITATION, DECLARED BEFORE ANY PARAMETER IS FITTED: THE DEPRESIÓN MOMPOSINA SINK
IS NOT REPRESENTED
=====================================================================================
Written here, at the top, and repeated in :func:`route_day`'s docstring, because ``docs/31``
§C4.1 requires it be committed to the code **before** a search is run, and because a
limitation discovered after a fit is indistinguishable from an excuse.

**What the routing is.**  Implementation A's channel operator - the one this module reuses -
is a cascade of linear reservoirs, i.e. Muskingum with ``X`` = 0.  It has exactly one state
per reach (an in-channel volume), one outflow that is a fixed fraction of that state, and
**no floodplain storage of any kind**: no stage-storage relation, no overbank threshold, no
off-channel ciénaga, no backwater, no bidirectional exchange.  A linear reservoir can delay
mass and, with :attr:`TransportParams.k_dep` > 0, remove it at a rate the user sets.  It
cannot fill a floodplain on the rising limb and give it back on the falling one.

**What that means for the Depresión Momposina.**  The Momposina is the basin's dominant
sediment sink - the vast wetland complex where the Magdalena and the Cauca meet, into which
the river spills and where suspended material settles out.  This model does not contain it.
Two consequences follow and both must travel with any number produced downstream of the
confluence:

1. **Expect systematic OVER-DELIVERY at and below Mompós.**  At the default ``k_dep`` = 0 the
   model asserts, structurally, that the reach network destroys no sediment at all, so a
   simulated load at or below Mompós is an upper bound that omits the single largest known
   loss term in the basin.  The direction is known in advance; only the magnitude is not.
2. **The bias is not a residual to be absorbed by a parameter.**  A basin-uniform ``k_dep``
   fitted to close a below-Mompós gap would spread one localised sink over 46,321 km of
   channel, degrading every upstream station to flatter one downstream one.  That is the
   anti-compensation failure ``docs/35`` §6 RULE 0 forbids for ``alpha``, in a new place.

**The mitigation is structural, and it is a rule about WHERE, not a correction term.**

    **CALIBRATE UPSTREAM OF THE MOMPOSINA ONLY.  EVALUATE BELOW IT - NEVER CALIBRATE
    THERE.**  The below-Mompós failure is then the MEASURED COST of the missing sink, and it
    is reported as such: a number the model was never allowed to fit, whose size is the
    project's own estimate of what the missing floodplain does.

:func:`split_stations_by_momposina` implements the split so a calibration script cannot
forget it, and :class:`TransportResult` carries the station role through to the report.
It is an *enabling* helper, not a permission: passing a below-Mompós station to a fit is
still a violation of this docstring even though nothing in the code can stop it.

**Why the missing sink is not fixed here** (``docs/18`` open item 4, ``docs/21`` §4 item 3).
The fix would be local-inertial / hydrodynamic routing for the Mompós - La Mojana reach, and
the project measured that it is not worth it on current evidence: celerity was swept
0.22 -> 2.0 m/s and El Niño daily ``r`` moved by less than 0.016 (``docs/22`` §4.6), while a
local-inertial scheme costs ~125x more per run (``docs/28``).  It is carried as a **named
limitation** instead - which is what this section is.

**And the surrogate that already exists, which is why a second one would double-count.**
``docs/22`` §4.6, on the twelve-configuration parameter table: the fitted celerity is
**0.221 m/s, 4.5x below its prior and at 33.9 % of its range**, and *"nb14 §4.3 already
identified [it] as a floodplain-storage surrogate for the Mompós reach"*.  The frozen H2E
hydrology has therefore ALREADY smeared water in time to stand in for storage this model
does not have.  That is the direct reason :attr:`TransportParams.tau_channel_days` defaults
to **0.0** here (see ROUTING DEFAULTS below): applying a second lag to the sediment would
double-count a surrogate that has already been fitted once.

**Which stations are affected.**  ``docs/42`` §G9 and ``docs/37`` §4.5: **801.1 km of
channel - the whole Momposina - lies below the outlet-most SSC station** (``21237020``
ARRANCAPLUMAS).  So the observational network cannot see the sink either: there is no station
in it and none below it.  This module can therefore state the limitation and report its cost
at the outlet, but the project has **no observation that could ever falsify a Momposina
retention estimate made here**.  Say that whenever an outlet load is quoted.

ROUTING DEFAULTS, AND WHY EACH IS WHAT IT IS
--------------------------------------------
``tau_channel_days`` = **0.0** (same-step advection: the load traverses the whole network
within the day it is delivered).  Three reasons, in order of weight:

1. It is the zero-storage baseline that makes the no-deposition case exactly reproducible -
   at ``tau`` = 0 the release coefficient is exactly 1.0 and every routing step is bitwise
   (see MASS LEDGER below).
2. The frozen H2E water routing has already applied channel storage, with a celerity that is
   itself a floodplain-storage surrogate (above).  A second lag double-counts it - the same
   argument ``mgb_sediment.SedParams.tau_delivery_days`` = 0 makes for the hillslope
   reservoir.
3. The C4/C5 quantities are window totals (Mt/yr over ENSO windows), and a pure lag leaves a
   window total unchanged except at the window edges.

It is NOT a claim that sediment reaches Calamar the day it is eroded.  A non-zero lag is one
call away - :func:`channel_tau_from_celerity` delegates to
``mgb_hydrology.default_channel_tau`` rather than re-deriving it - and
:class:`TransportParams` accepts a per-reach array, so C4.3 can fit or impose one and the
mass ledger stays closed (the in-channel storage term simply stops being zero).

``k_dep`` = **0.0**, ``dep_mode`` = ``'per_km'``.  Zero because the brief for this stage
requires the no-deposition case to be the reproducible baseline, and because a non-zero
default would be a fitted number smuggled in as a convention.  **At ``k_dep`` = 0 this model
asserts SDR = 1.0 between hillslope and station** - that is a claim, it is stated here in
those words, and ``docs/42`` §G5 requires it be stated in exactly that form by any C4 write-up
that adopts a fit without a named sink.

``dep_mode`` NAMES THE UNITS OF ``k_dep``, and the two are not interchangeable:

``'per_km'`` (DEFAULT), ``k_dep`` in **1/km**
    ``d_i = 1 - exp(-k_dep * reach_km_i)``.  Retention along a flow path is then
    ``exp(-k_dep * path_km)`` - **invariant to how the network is discretised**.  Cutting a
    500 km path into 100 or into 200 minibacias gives the same delivered fraction, which is
    the property a *rate* must have.
``'per_day'``, ``k_dep`` in **1/day**
    ``d_i = 1 - exp(-k_dep * dt)``, the linear-reservoir analogue of the water store.  It is
    meaningful only with ``tau_channel_days`` > 0: at ``tau`` = 0 the load passes through
    every reach on its path within one step, so a per-step coefficient is applied
    ``hops_to_outlet`` times (up to **291** in this basin) in a single day and is not a daily
    rate at all.  Kept because C4.3 may pair it with a fitted ``tau_channel_days``; a run
    that combines ``'per_day'`` with ``tau_channel_days`` = 0 warns.

Both accept a scalar or a per-reach array, so a spatially explicit sink - a Momposina mask,
say - needs no engine change.  **That is the only supported way to represent the Momposina in
this implementation, and it would be an imposed sink, not a fitted one, because no
observation lies inside or below it.**

MASS LEDGER - WHAT IS EXACT, AND WHAT IS ONLY TIGHT
---------------------------------------------------
The daily update per reach is a structural partition, computed in a fixed association order::

    S      = s_ch + inflow                  # inflow = local load + upstream outflows
    dep    = S * d                          # d = 0.0 exactly when k_dep = 0
    S1     = S - dep
    out    = S1 * c                         # c = 1.0 exactly when tau_channel_days = 0
    s_ch'  = S1 - out
    residual = ((S - dep) - out) - s_ch'    # identically 0.0 in IEEE-754, see below

The residual is **exactly 0.0 for every reach on every day, for every parameter value**, not
merely small: writing ``a = fl(S - dep)`` and ``b = fl(a - out)``, the stored state is
``s_ch' = fl(S1 - out) = b``, so the residual evaluates ``fl(b - b)`` = 0.  This is the
strongest mass statement the module makes and :func:`simulate_transport` measures it on every
run (``ledger['max_node_residual_t']``).

The GLOBAL identity ``sum(local) == outlet + deposited + storage`` needs, in addition,
the cross-reach summation to be exact - and float addition is not associative, so re-summing
8,672 reaches in a different order is not bitwise.  Therefore:

* at ``k_dep`` = 0 and ``tau_channel_days`` = 0, ``outlet == sum(local)`` **bitwise** whenever
  the arithmetic itself is exact (integer-valued loads; ``tests/test_transport.py`` asserts
  this on the real 8,672-reach network), and
* on real float drivers the difference is pure re-association rounding.  It is MEASURED and
  reported (``ledger['residual_relative']``), never asserted to be zero.

That distinction is stated here so that a small non-zero residual can never be presented as
though it had been the design.  Totals are accumulated with :func:`math.fsum`, so the
accounting itself contributes no error.

WHAT THIS MODULE DOES NOT DO
----------------------------
* **It does not fit anything.**  C4.2 registers the cells, C4.3 runs the search.
* **It does not produce t/km2/yr.**  Gauge-referenced specific yields are EMBARGOED
  (``docs/23`` §13.2: per-gauge catchment areas disagree by >2x on 36 % of shared gauges).
  Absolute flux only - t/day, Mt/yr.  Nothing here divides by an area.
* **It does not represent bank erosion, gully or valley-trench sources.**  MUSLE upstream is
  sheet-and-rill only, and in USDA NEH Part 632 Ch. 6's reference partition channel-type
  sources are 61 % of gross erosion (``docs/40``).  A load routed by this module is therefore
  hillslope-sourced throughout, and calling its outlet value "the basin sediment load" is a
  category error.
* **It does not resample or re-time the hydrology.**  Local loads come in on the driver
  calendar and leave on it.
"""

from __future__ import annotations

import math
import pathlib
import time
import warnings
from dataclasses import dataclass, field
from typing import Optional, Sequence

import numpy as np

# Resolved from this file, not the caller's cwd - see mgb_sediment.DEFAULT_PROCESSED_DIR.
DEFAULT_TOPOLOGY_PATH = (
    pathlib.Path(__file__).resolve().parent.parent
    / "data" / "processed" / "model_inputs_v2" / "topology.npz"
)

__all__ = [
    "DEFAULT_TOPOLOGY_PATH",
    "DT_DAYS",
    "DEP_MODES",
    "DEFAULT_DEP_MODE",
    "MOMPOSINA_NOTE",
    "ReachNetwork",
    "build_network",
    "load_network",
    "TransportParams",
    "TransportState",
    "TransportResult",
    "channel_tau_from_celerity",
    "route_day",
    "simulate_transport",
    "split_stations_by_momposina",
]

DT_DAYS = 1.0

#: The named deposition parametrisations.  ``per_km`` is the default because retention along
#: a flow path is then ``exp(-k_dep * path_km)``, i.e. invariant to the discretisation of the
#: network; ``per_day`` is the linear-reservoir analogue and is meaningful only when
#: ``tau_channel_days`` > 0.  See the module docstring, ROUTING DEFAULTS.
DEP_MODES = ("per_km", "per_day")
DEFAULT_DEP_MODE = "per_km"

#: One-paragraph form of the limitation, so a report cannot quote a below-Mompós number
#: without it.  :meth:`TransportResult.momposina_note` returns it.
MOMPOSINA_NOTE = (
    "LIMITATION (declared in src/mgb_transport.py before any parameter was fitted): the "
    "channel operator is a linear reservoir per reach (Muskingum X = 0) with NO floodplain "
    "storage, so the Depresion Momposina sink is NOT represented. Expect systematic "
    "OVER-DELIVERY at and below Mompos. Mitigation is structural - calibrate upstream of the "
    "Momposina only and EVALUATE below it, never calibrate there - so that the below-Mompos "
    "failure is the MEASURED cost of the missing sink. The frozen H2E celerity (0.221 m/s) is "
    "already a floodplain-storage surrogate for the Mompos reach (docs/22 s4.6), which is why "
    "tau_channel_days defaults to 0 here: a second lag would double-count it. 801.1 km of "
    "channel - the whole Momposina - lies BELOW the outlet-most SSC station 21237020 "
    "ARRANCAPLUMAS (docs/42 G9), so no observation can falsify a retention estimate made "
    "inside it."
)


# ---------------------------------------------------------------------------
# network
# ---------------------------------------------------------------------------


def _finite(name: str, arr, *, nonneg: bool = False, positive: bool = False) -> np.ndarray:
    a = np.asarray(arr, dtype=np.float64)
    if not np.all(np.isfinite(a)):
        raise ValueError(f"{name} has {int((~np.isfinite(a)).sum())} non-finite entries")
    if positive and np.any(a <= 0.0):
        raise ValueError(f"{name} must be > 0; min is {float(a.min())!r}")
    if nonneg and np.any(a < 0.0):
        raise ValueError(f"{name} must be >= 0; min is {float(a.min())!r}")
    return a


def _topological_order(down: np.ndarray) -> tuple:
    """Kahn sweep -> (order, level).  ``level[i] = 1 + max(level of inflowing nodes)``.

    Deliberately the same algorithm as ``mgb_hydrology._topological_order``.  It is
    re-derived here rather than imported so that this module has no import-time dependency
    on the frozen Phase B engine, and :func:`build_network` cross-checks the result against
    the ``topo_order_idx`` column stored in ``topology.npz`` - two independent orderings
    that must agree on the partial order, which is the property that matters.
    """
    n = down.size
    indeg = np.bincount(down[down >= 0], minlength=n).astype(np.int64)
    level = np.zeros(n, dtype=np.int64)
    order = np.empty(n, dtype=np.int64)
    stack = np.flatnonzero(indeg == 0).astype(np.int64).tolist()
    rem = indeg.copy()
    k = 0
    while stack:
        i = stack.pop()
        order[k] = i
        k += 1
        j = down[i]
        if j >= 0:
            if level[i] + 1 > level[j]:
                level[j] = level[i] + 1
            rem[j] -= 1
            if rem[j] == 0:
                stack.append(int(j))
    if k != n:
        raise ValueError(f"the reach network contains a cycle: only {k}/{n} nodes orderable")
    return order, level


def _pack_levels(level: np.ndarray, down: np.ndarray) -> tuple:
    """Pre-slice reaches by level so the daily sweep does no fancy indexing of ``down``."""
    out = []
    for lv in range(int(level.max()) + 1):
        idx = np.flatnonzero(level == lv).astype(np.int64)
        tgt = down[idx]
        has = tgt >= 0
        out.append((idx, has, tgt[has]))
    return tuple(out)


@dataclass(frozen=True)
class ReachNetwork:
    """Immutable reach topology: who drains into whom, and how long each reach is.

    Built once and reused for every parameter set, exactly like ``MgbTopology`` and
    ``SedGeometry``: a C4.3 search must not re-read the network per evaluation.
    """

    ids: np.ndarray             # (n,) int64   minibacia ids, in internal order
    down: np.ndarray            # (n,) int64   internal index of receiver, -1 at an outlet
    outlets: np.ndarray         # (n_out,) int64
    order: np.ndarray           # (n,) int64   topological order, upstream -> downstream
    level: np.ndarray           # (n,) int64   0 = headwater
    reach_km: np.ndarray        # (n,) float64 own reach length
    own_area_km2: np.ndarray    # (n,) float64
    upstream_area_km2: np.ndarray   # (n,) float64
    hops_to_outlet: np.ndarray  # (n,) int64
    levels: tuple = field(repr=False, default=())
    sorted_ids: np.ndarray = field(repr=False, default=None)
    sorted_pos: np.ndarray = field(repr=False, default=None)
    audit: dict = field(default_factory=dict, repr=False)

    @property
    def n_reach(self) -> int:
        return int(self.ids.size)

    def index_of(self, ids: Sequence[int]) -> np.ndarray:
        """Internal indices of the given minibacia ids (raises on an unknown id)."""
        want = np.asarray(ids, dtype=np.int64)
        loc = np.clip(np.searchsorted(self.sorted_ids, want), 0, self.sorted_ids.size - 1)
        ok = self.sorted_ids[loc] == want
        if not ok.all():
            raise KeyError(f"unknown minibacia ids: {want[~ok][:10].tolist()}")
        return self.sorted_pos[loc]

    def downstream_path(self, start: int) -> np.ndarray:
        """Internal indices from ``start`` to its outlet, inclusive of both."""
        path = [int(start)]
        j = int(self.down[start])
        while j >= 0:
            path.append(j)
            j = int(self.down[j])
        return np.asarray(path, dtype=np.int64)

    def upstream_mask(self, node: int) -> np.ndarray:
        """Boolean mask of every reach that drains through ``node`` (``node`` included).

        A reverse sweep in reverse topological order: a reach is upstream of ``node`` if its
        receiver is.  Used by the station reports (what erosion a station can see) and by
        the topological-correctness test.
        """
        mask = np.zeros(self.n_reach, dtype=bool)
        mask[int(node)] = True
        for i in self.order[::-1]:
            j = self.down[i]
            if j >= 0 and mask[j]:
                mask[i] = True
        return mask


def build_network(ids, downstream_idx, reach_km, own_area_km2, upstream_area_km2=None,
                  *, hops_to_outlet=None, audit: Optional[dict] = None) -> ReachNetwork:
    """Validate and pack the reach network.  ``downstream_idx`` is INTERNAL indices, -1 = outlet.

    Everything that could make a run silently wrong is rejected here rather than at use
    time: duplicate ids, a self-draining reach, an out-of-range receiver, a cycle, a
    negative reach length.
    """
    ids = np.asarray(ids, dtype=np.int64)
    n = ids.size
    if np.unique(ids).size != n:
        raise ValueError("duplicate minibacia ids")
    down = np.asarray(downstream_idx, dtype=np.int64).copy()
    if down.shape != (n,):
        raise ValueError(f"downstream_idx must be ({n},), got {down.shape}")
    if np.any(down >= n):
        raise ValueError("downstream_idx points past the end of the network")
    down[down < 0] = -1
    if np.any(down == np.arange(n)):
        bad = ids[down == np.arange(n)][:5]
        raise ValueError(f"self-draining reach(es): {bad.tolist()}")
    outlets = np.flatnonzero(down < 0).astype(np.int64)
    if outlets.size == 0:
        raise ValueError("no outlet: every reach drains somewhere (cycle)")
    rk = _finite("reach_km", reach_km, nonneg=True)
    if rk.shape != (n,):
        raise ValueError(f"reach_km must be ({n},), got {rk.shape}")
    area = _finite("own_area_km2", own_area_km2, positive=True)
    if area.shape != (n,):
        raise ValueError(f"own_area_km2 must be ({n},), got {area.shape}")
    up_area = area if upstream_area_km2 is None else _finite(
        "upstream_area_km2", upstream_area_km2, positive=True)
    order, level = _topological_order(down)
    if hops_to_outlet is None:
        hops = np.zeros(n, dtype=np.int64)
        for i in order[::-1]:
            j = down[i]
            if j >= 0:
                hops[i] = hops[j] + 1
    else:
        hops = np.asarray(hops_to_outlet, dtype=np.int64)
    srt = np.argsort(ids, kind="stable")
    return ReachNetwork(
        ids=ids, down=down, outlets=outlets, order=order, level=level,
        reach_km=rk, own_area_km2=area, upstream_area_km2=up_area, hops_to_outlet=hops,
        levels=_pack_levels(level, down),
        sorted_ids=ids[srt], sorted_pos=srt.astype(np.int64),
        audit=dict(audit or {}),
    )


def load_network(path=DEFAULT_TOPOLOGY_PATH,
                 *, mini_ids: Optional[Sequence[int]] = None) -> ReachNetwork:
    """Read the reach network from the model-inputs bundle.

    ``mini_ids`` (pass ``h2e_drivers.npz:minibacia_id``) asserts that the network's column
    order is the order the local-load array uses.  A mismatch there is a silent spatial
    scramble - every reach would receive some other reach's sediment - so it raises rather
    than reorders.

    The stored ``topo_order_idx`` is CROSS-CHECKED against an independent Kahn sweep: not for
    equality (many topological orders are valid) but for the property that matters, that
    every receiver is processed after its contributors.
    """
    p = pathlib.Path(path)
    if not p.is_file():
        raise FileNotFoundError(
            f"{p} not found. It is the model-inputs topology bundle; rebuild it with the "
            "Phase A chain (docs/20 §2) - do not hand-edit it."
        )
    with np.load(p, allow_pickle=False) as z:
        need = ("minibacia_id", "downstream_idx", "reach_km", "own_area_km2")
        missing = [k for k in need if k not in z.files]
        if missing:
            raise ValueError(f"{p} is missing field(s) {missing}; it holds {sorted(z.files)}")
        ids = z["minibacia_id"].astype(np.int64)
        down = z["downstream_idx"].astype(np.int64)
        reach_km = z["reach_km"].astype(np.float64)
        own_area = z["own_area_km2"].astype(np.float64)
        up_area = (z["upstream_area_km2"].astype(np.float64)
                   if "upstream_area_km2" in z.files else None)
        hops = z["hops_to_outlet"].astype(np.int64) if "hops_to_outlet" in z.files else None
        stored_order = z["topo_order_idx"].astype(np.int64) if "topo_order_idx" in z.files else None
    if mini_ids is not None:
        want = np.asarray(mini_ids, dtype=np.int64)
        if want.shape != ids.shape or not np.array_equal(want, ids):
            raise ValueError(
                f"{p}'s minibacia_id order differs from the local-load column order "
                "(first mismatch at index "
                f"{int(np.flatnonzero(want != ids)[0]) if want.shape == ids.shape else 0}). "
                "Routing on a mismatched order silently scrambles the basin; align the "
                "arrays instead of reordering here."
            )
    net = build_network(ids, down, reach_km, own_area, up_area, hops_to_outlet=hops,
                        audit={"source": str(p)})
    if stored_order is not None:
        if stored_order.shape != ids.shape or np.unique(stored_order).size != ids.size:
            raise ValueError(f"{p}:topo_order_idx is not a permutation of the reaches")
        pos = np.empty(ids.size, dtype=np.int64)
        pos[stored_order] = np.arange(ids.size, dtype=np.int64)
        linked = net.down >= 0
        if not np.all(pos[net.down[linked]] > pos[linked]):
            bad = int(np.flatnonzero(pos[net.down[linked]] <= pos[linked])[0])
            raise ValueError(
                f"{p}:topo_order_idx is not a topological order (reach at position {bad} is "
                "processed after its own receiver); the stored order and the network "
                "disagree, so one of them is wrong - do not route on either."
            )
    return net


# ---------------------------------------------------------------------------
# parameters
# ---------------------------------------------------------------------------


def channel_tau_from_celerity(net: ReachNetwork, celerity_m_s: float) -> np.ndarray:
    """Per-reach travel time in days from the network's OWN reach lengths.

    ``tau = reach_km * 1000 / (celerity * 86400)``.  Unlike
    ``mgb_hydrology.default_channel_tau`` - which approximates the reach length by a
    minibacia's equivalent-circle diameter because ``MgbTopology`` carries no length - the
    C4 topology bundle stores the real D8 ``reach_km``, so this uses it.  The two are
    reconciled deliberately: ``default_channel_tau`` remains the Phase B prior and is not
    re-derived here.

    This is a PRIOR, not a measurement, and it is not the default: see the module docstring
    on why ``tau_channel_days`` is 0.0 unless a caller sets it.  Note also that the celerity
    fitted in Phase B (0.221 m/s) is a floodplain-storage surrogate, so feeding it here
    applies that surrogate a SECOND time - if you do it, say so.
    """
    c = float(celerity_m_s)
    if not math.isfinite(c) or c <= 0.0:
        raise ValueError("celerity_m_s must be finite and > 0")
    return net.reach_km * 1000.0 / (c * 86400.0)


@dataclass(frozen=True)
class TransportParams:
    """Every channel parameter, with the origin of its default stated.  NOTHING here is fitted.

    Frozen on purpose: a C4.3 search must build a new instance per evaluation rather than
    mutate a shared one, so a half-updated parameter set cannot leak between evaluations.
    """

    #: First-order deposition/settling rate.  **DEFAULT EXACTLY 0.0** - the no-deposition
    #: case is the reproducible baseline (and at 0.0 this model asserts SDR = 1.0 between
    #: hillslope and station, which docs/42 G5 requires be stated as a claim).  Scalar or a
    #: per-reach array, so a spatially explicit sink needs no engine change.  Units are set
    #: by :attr:`dep_mode`: 1/km for ``'per_km'``, 1/day for ``'per_day'``.
    k_dep: object = 0.0
    #: Which first-order law ``k_dep`` obeys.  ``'per_km'`` (default) is discretisation
    #: invariant - retention along a path is ``exp(-k_dep * path_km)``.  ``'per_day'`` is the
    #: linear-reservoir analogue and is meaningful only with ``tau_channel_days`` > 0.
    dep_mode: str = DEFAULT_DEP_MODE
    #: Channel residence time, days.  **DEFAULT 0.0** = same-step advection, i.e. exactly
    #: 1.0 release coefficient and a bitwise routing step.  Not a claim about travel time:
    #: the frozen H2E hydrology already applied channel storage with a celerity that is
    #: itself a floodplain-storage surrogate (docs/22 §4.6), so a second lag on the sediment
    #: double-counts it.  Scalar or per-reach array; see :func:`channel_tau_from_celerity`.
    tau_channel_days: object = 0.0

    def __post_init__(self) -> None:
        if self.dep_mode not in DEP_MODES:
            raise ValueError(f"dep_mode must be one of {DEP_MODES}, got {self.dep_mode!r}")
        for name in ("k_dep", "tau_channel_days"):
            a = np.asarray(getattr(self, name), dtype=np.float64)
            if not np.all(np.isfinite(a)):
                raise ValueError(f"{name} must be finite")
            if np.any(a < 0.0):
                raise ValueError(f"{name} must be >= 0 (a negative one would CREATE sediment)")
            if a.ndim > 1:
                raise ValueError(f"{name} must be a scalar or a 1-D per-reach array")

    # -- derived per-reach coefficients ------------------------------------------------

    def _broadcast(self, value, n: int, name: str) -> np.ndarray:
        a = np.asarray(value, dtype=np.float64)
        if a.ndim == 0:
            return np.full(n, float(a))
        if a.shape != (n,):
            raise ValueError(f"{name} must be scalar or length {n}, got {a.shape}")
        return a.astype(np.float64, copy=True)

    def deposition_coef(self, net: ReachNetwork) -> np.ndarray:
        """Fraction of a reach's sediment mass that settles out per step, ``(n,)`` in [0, 1).

        ``per_km``: ``1 - exp(-k_dep * reach_km)``.  ``per_day``: ``1 - exp(-k_dep * dt)``.
        Exactly 0.0 wherever ``k_dep`` is 0.0 (``-expm1(-0.0)`` is exactly 0.0), which is
        what makes the default run bitwise.
        """
        k = self._broadcast(self.k_dep, net.n_reach, "k_dep")
        span = net.reach_km if self.dep_mode == "per_km" else np.full(net.n_reach, DT_DAYS)
        if self.dep_mode == "per_day" and np.any(k > 0.0):
            tau = self._broadcast(self.tau_channel_days, net.n_reach, "tau_channel_days")
            if np.all(tau == 0.0):
                warnings.warn(
                    "dep_mode='per_day' with tau_channel_days = 0: the load traverses every "
                    "reach on its path within one step, so the coefficient is applied "
                    f"hops_to_outlet times (up to {int(net.hops_to_outlet.max())} here) per "
                    "day and is NOT a daily rate. Use dep_mode='per_km' for a "
                    "discretisation-invariant sink, or set tau_channel_days > 0.",
                    stacklevel=2,
                )
        return -np.expm1(-k * span)

    def release_coef(self, net: ReachNetwork) -> np.ndarray:
        """Fraction of a reach's store released downstream per day, ``(n,)`` in (0, 1].

        ``1 - exp(-dt/tau)``, the analytic one-day solution of ``dS/dt = -S/tau`` - the same
        form ``mgb_hydrology._release_coef`` uses for water, and for the same reason (bounded
        in (0, 1] for every ``tau`` >= 0, so a store can never go negative).  ``tau`` = 0
        gives exactly 1.0, i.e. bitwise pass-through.
        """
        tau = self._broadcast(self.tau_channel_days, net.n_reach, "tau_channel_days")
        out = np.ones(net.n_reach, dtype=np.float64)
        pos = tau > 0.0
        out[pos] = -np.expm1(-DT_DAYS / tau[pos])
        return out

    def summary(self, net: Optional[ReachNetwork] = None) -> dict:
        """Every named choice this parameter set carries - meant to be printed with the load.

        ``docs/42`` G6 requires a fitted parameter never be quoted without its conventions;
        this is the transport half of that table.  ``asserts_sdr_1`` is the G5 sentence in
        machine-readable form.
        """
        k = np.asarray(self.k_dep, dtype=np.float64)
        tau = np.asarray(self.tau_channel_days, dtype=np.float64)
        out = {
            "dep_mode": self.dep_mode,
            "k_dep_scalar": float(k) if k.ndim == 0 else None,
            "k_dep_is_field": bool(k.ndim > 0),
            "k_dep_max": float(k.max()) if k.size else 0.0,
            "tau_channel_days_scalar": float(tau) if tau.ndim == 0 else None,
            "tau_channel_is_field": bool(tau.ndim > 0),
            "asserts_sdr_1": bool(np.all(k == 0.0)),
            "named_sink": "none (k_dep = 0)" if np.all(k == 0.0) else f"k_dep ({self.dep_mode})",
            "momposina_represented": False,
        }
        if net is not None:
            d = self.deposition_coef(net)
            out["dep_coef_median"] = float(np.median(d))
            out["dep_coef_max"] = float(d.max())
        return out


# ---------------------------------------------------------------------------
# state
# ---------------------------------------------------------------------------


@dataclass
class TransportState:
    """Mutable state: tonnes of suspended load held in each reach's channel store."""

    store_t: np.ndarray          # (n,) tonnes

    @classmethod
    def initial(cls, net: ReachNetwork) -> "TransportState":
        """Cold start with empty channels.

        At the default ``tau_channel_days`` = 0 the store is empty at the end of every day,
        so there is nothing to warm up.  With ``tau`` > 0 it fills within a few ``tau``;
        ``docs/31`` §C4.2's spin-up clarification (2009-2011 feeds antecedent state into the
        2012-14 calibration window) is about THIS store.
        """
        return cls(store_t=np.zeros(net.n_reach, dtype=np.float64))

    def copy(self) -> "TransportState":
        return TransportState(store_t=self.store_t.copy())

    def stored_tonnes(self) -> float:
        return float(math.fsum(self.store_t.tolist()))


# ---------------------------------------------------------------------------
# the daily sweep
# ---------------------------------------------------------------------------


def route_day(net: ReachNetwork, dep_coef: np.ndarray, rel_coef: np.ndarray,
              store_t: np.ndarray, local_t: np.ndarray, *,
              backend: str = "levels",
              work: Optional[dict] = None) -> tuple:
    """Advect one day's load through the network.  Returns ``(out_t, dep_t, inflow_t)``.

    ``local_t`` is the hillslope load delivered to each reach that day (tonnes), i.e. exactly
    ``mgb_sediment.simulate_sediment(...).delivered_t_day[t]``.  ``store_t`` is updated IN
    PLACE.  ``out_t[i]`` is what reach ``i`` passes to its receiver; the basin's export is
    ``out_t[net.outlets].sum()``.

    Per reach, in this fixed association order::

        S     = store + inflow
        dep   = S * dep_coef
        S1    = S - dep
        out   = S1 * rel_coef
        store = S1 - out

    which is a structural partition: no tonne is created or dropped, and the per-reach
    residual ``((S - dep) - out) - store`` is exactly 0.0 in IEEE-754 (module docstring,
    MASS LEDGER).

    LIMITATION, RESTATED HERE BECAUSE THIS IS THE FUNCTION THAT WOULD HAVE TO CHANGE.  This
    is Muskingum with ``X`` = 0 - one linear store per reach, one outflow proportional to it,
    **no floodplain storage**.  The **Depresión Momposina sink is therefore NOT represented**,
    and the model will systematically **over-deliver at and below Mompós**.  The mitigation is
    structural, not a correction term: **calibrate on stations upstream of the Momposina only
    and EVALUATE below it - never calibrate there** - so that the below-Mompós failure is the
    MEASURED cost of the missing sink.  The Phase B celerity (0.221 m/s) already acts as a
    floodplain-storage surrogate for the Mompós reach (``docs/22`` §4.6), which is why
    ``tau_channel_days`` defaults to 0 rather than inheriting it.

    Two backends, the project's standing two-implementation discipline:
    ``'levels'`` updates a whole topological level at once (``np.add.at``, required because
    two reaches in one level may share a receiver); ``'order'`` is a plain node loop in
    topological order.  They differ only in summation order and
    ``tests/test_transport.py`` asserts they agree.
    """
    n = net.n_reach
    if backend not in ("levels", "order"):
        raise ValueError("backend must be 'levels' or 'order'")
    if work is None:
        work = {}
    inflow = work.get("inflow")
    if inflow is None or inflow.shape != (n,):
        inflow = np.empty(n, dtype=np.float64)
        work["inflow"] = inflow
    out_t = work.get("out")
    if out_t is None or out_t.shape != (n,):
        out_t = np.empty(n, dtype=np.float64)
        work["out"] = out_t
    dep_t = work.get("dep")
    if dep_t is None or dep_t.shape != (n,):
        dep_t = np.empty(n, dtype=np.float64)
        work["dep"] = dep_t

    np.copyto(inflow, local_t)
    if backend == "levels":
        for idx, has, tgt in net.levels:
            s = store_t[idx] + inflow[idx]
            d = s * dep_coef[idx]
            s1 = s - d
            q = s1 * rel_coef[idx]
            store_t[idx] = s1 - q
            dep_t[idx] = d
            out_t[idx] = q
            if tgt.size:
                np.add.at(inflow, tgt, q[has])
    else:
        down = net.down
        for i in net.order:
            s = store_t[i] + inflow[i]
            d = s * dep_coef[i]
            s1 = s - d
            q = s1 * rel_coef[i]
            store_t[i] = s1 - q
            dep_t[i] = d
            out_t[i] = q
            j = down[i]
            if j >= 0:
                inflow[j] += q
    return out_t, dep_t, inflow


# ---------------------------------------------------------------------------
# result
# ---------------------------------------------------------------------------


@dataclass
class TransportResult:
    """Routed load plus everything needed to audit the run."""

    dates: Optional[np.ndarray]
    record_ids: np.ndarray                 # (m,) minibacia ids of the recorded columns
    load_t_day: Optional[np.ndarray]       # (ndays, m) tonnes/day leaving each recorded reach
    outlet_ids: np.ndarray                 # (n_out,) minibacia ids of the outlet reach(es)
    outlet_t_day: np.ndarray               # (ndays,) tonnes/day exported by the basin
    accum_load_t: np.ndarray               # (n,) period-total load leaving each reach
    deposited_t: np.ndarray                # (n,) period-total deposition per reach
    series: dict                           # basin-total daily series, tonnes/day
    ledger: dict
    state: TransportState
    params: TransportParams
    backend: str
    wall_time_s: float

    def load_at(self, mini_id: int) -> np.ndarray:
        if self.load_t_day is None:
            raise ValueError("this run was made with store_daily=False")
        j = int(np.flatnonzero(self.record_ids == int(mini_id))[0])
        return self.load_t_day[:, j]

    def outlet_mt_per_year(self, ndays: Optional[int] = None) -> float:
        """Basin export in Mt/yr.  ABSOLUTE flux only - never divided by an area (docs/23)."""
        nd = int(self.outlet_t_day.size if ndays is None else ndays)
        total = math.fsum(self.outlet_t_day.tolist())
        return total / 1e6 / (nd / 365.25)

    def momposina_note(self) -> str:
        """The declared limitation, for pasting beside any at-or-below-Mompós number."""
        return MOMPOSINA_NOTE


def _assemble_ledger(local_daily, out_daily, dep_daily, store_start: float, store_end: float,
                     max_node_residual: float) -> dict:
    """Close the channel budget: ``local_in = exported + deposited + (store_end - store_start)``.

    Totals use :func:`math.fsum`, so the accounting adds no error of its own.  ``exact``
    records whether the GLOBAL residual is literally 0.0 - which it is when the arithmetic is
    exact (integer loads) and at the default parameters, and which it is not on real float
    drivers, where the remainder is pure cross-reach re-association rounding.  The stronger
    and always-exact statement is ``max_node_residual_t``: the per-reach, per-day partition
    residual, which is 0.0 by construction for every parameter value.
    """
    local = math.fsum(local_daily)
    exported = math.fsum(out_daily)
    deposited = math.fsum(dep_daily)
    residual = local - exported - deposited - (store_end - store_start)
    scale = max(abs(local), 1.0)
    return {
        "local_in_t": local,
        "exported_t": exported,
        "deposited_t": deposited,
        "store_start_t": store_start,
        "store_end_t": store_end,
        "residual_t": residual,
        "residual_relative": abs(residual) / scale,
        "exact": residual == 0.0,
        "max_node_residual_t": float(max_node_residual),
        "node_partition_exact": float(max_node_residual) == 0.0,
        "ndays": len(local_daily),
    }


def simulate_transport(
    net: ReachNetwork,
    params: TransportParams,
    local_load_t_day: np.ndarray,
    *,
    dates: Optional[Sequence] = None,
    record_ids: Optional[Sequence[int]] = None,
    state: Optional[TransportState] = None,
    backend: str = "levels",
    store_daily: bool = True,
    dtype_out: type = np.float32,
    audit_mass: bool = True,
) -> TransportResult:
    """Route ``local_load_t_day`` ``(ndays, n_reach)``, tonnes/day, down the network.

    Parameters
    ----------
    local_load_t_day
        Hillslope load delivered to each reach per day - ``SedResult.delivered_t_day`` with
        ``record_ids=None``, columns ordered like ``net.ids``.  A column-order mismatch is a
        silent spatial scramble, so pass ``mini_ids`` to :func:`load_network` and let it
        raise.
    record_ids
        Minibacia ids whose outgoing load is written out; ``None`` records all.
        ``store_daily=False`` keeps only the outlet series, the period totals and the ledger.
    audit_mass
        Measure the per-reach per-day partition residual (a few array ops per day).  Leave it
        on: it is the module's strongest mass statement and it is cheap.

    Returns
    -------
    TransportResult
        ``load_t_day`` is the load LEAVING each recorded reach, tonnes/day.  It is a lower
        bound in the hillslope-source sense (``mgb_sediment``'s inherited biases) and an
        UPPER bound at and below Mompós (no floodplain sink - see the module docstring).
        Nothing is divided by an area anywhere: t/km²/yr is embargoed (``docs/23`` §13.2).
    """
    if backend not in ("levels", "order"):
        raise ValueError("backend must be 'levels' or 'order'")
    t0 = time.perf_counter()
    n = net.n_reach
    load = np.asarray(local_load_t_day)
    if load.ndim != 2 or load.shape[1] != n:
        raise ValueError(f"local_load_t_day must be (ndays, {n}), got {load.shape}")
    ndays = int(load.shape[0])
    if dates is not None and len(dates) != ndays:
        raise ValueError(
            f"dates has {len(dates)} entries but the load has {ndays} days - a mismatch here "
            "silently mislabels the output time axis"
        )
    # One screen up front: a NaN or a negative local load would otherwise propagate through
    # the whole network and be found only by bisection.
    if not np.all(np.isfinite(load)):
        raise ValueError(f"local_load_t_day has {int((~np.isfinite(load)).sum())} non-finite "
                         "entries")
    if np.any(load < 0.0):
        raise ValueError("local_load_t_day has negative entries - erosion cannot be negative")

    dep_coef = params.deposition_coef(net)
    rel_coef = params.release_coef(net)

    if record_ids is None:
        rec_idx = np.arange(n, dtype=np.int64)
        rec_ids = net.ids.copy()
    else:
        rec_idx = net.index_of(record_ids)
        rec_ids = net.ids[rec_idx]
    out_arr = np.empty((ndays, rec_idx.size), dtype=dtype_out) if store_daily else None

    st = TransportState.initial(net) if state is None else state.copy()
    if st.store_t.shape != (n,):
        raise ValueError("state does not match the network")
    store_start = st.stored_tonnes()

    outlets = net.outlets
    series = {k: np.zeros(ndays) for k in ("local", "exported", "deposited", "store_end")}
    accum = np.zeros(n)
    dep_accum = np.zeros(n)
    outlet_daily = np.zeros(ndays)
    work: dict = {}
    max_resid = 0.0
    prev = np.empty(n, dtype=np.float64) if audit_mass else None

    for t in range(ndays):
        local = load[t].astype(np.float64, copy=False)
        if audit_mass:
            np.copyto(prev, st.store_t)
        out_t, dep_t, inflow = route_day(net, dep_coef, rel_coef, st.store_t, local,
                                         backend=backend, work=work)
        if audit_mass:
            # ((S - dep) - out) - store'  with S = prev + inflow.  Identically 0.0 in
            # IEEE-754 for every parameter value; see the module docstring, MASS LEDGER.
            resid = (((prev + inflow) - dep_t) - out_t) - st.store_t
            m = float(np.abs(resid).max())
            if m > max_resid:
                max_resid = m
        accum += out_t
        dep_accum += dep_t
        series["local"][t] = local.sum()
        series["exported"][t] = out_t[outlets].sum()
        series["deposited"][t] = dep_t.sum()
        series["store_end"][t] = st.store_t.sum()
        outlet_daily[t] = series["exported"][t]
        if out_arr is not None:
            out_arr[t] = out_t[rec_idx]

    ledger = _assemble_ledger(series["local"].tolist(), series["exported"].tolist(),
                              series["deposited"].tolist(), store_start, st.stored_tonnes(),
                              max_resid if audit_mass else float("nan"))
    return TransportResult(
        dates=None if dates is None else np.asarray(dates),
        record_ids=rec_ids,
        load_t_day=out_arr,
        outlet_ids=net.ids[outlets],
        outlet_t_day=outlet_daily,
        accum_load_t=accum,
        deposited_t=dep_accum,
        series=series,
        ledger=ledger,
        state=st,
        params=params,
        backend=backend,
        wall_time_s=time.perf_counter() - t0,
    )


# ---------------------------------------------------------------------------
# the calibrate-upstream / evaluate-below split
# ---------------------------------------------------------------------------


def split_stations_by_momposina(net: ReachNetwork, station_minibacias: Sequence[int],
                                *, momposina_ref_minibacia: int) -> dict:
    """Partition stations into ``calibrate`` and ``evaluate_only`` about the Momposina.

    ``momposina_ref_minibacia`` is the **outlet-most reach still ABOVE the Momposina** - for
    this project ``21237020`` ARRANCAPLUMAS's minibacia (12354), because ``docs/42`` G9
    records that the whole Momposina lies below it.  ``evaluate_only`` is then the set of
    stations sitting on the trunk **strictly downstream of that reach**, i.e. on
    ``downstream_path(ref)[1:]``; every other station is ``calibrate``.

    **The rule is "not on the trunk below the reference", NOT "drains through the
    reference".**  The distinction is not cosmetic and getting it wrong was a real bug in the
    first draft of this function: the Cauca joins the Magdalena *below* ARRANCAPLUMAS, so the
    "drains through" reading throws every Cauca station - JULUMITO, IRRA, BOLOMBOLO, PUENTE
    ARAGÓN, EL ALAMBRADO - out of the calibration set even though all of them sit hundreds of
    kilometres **above** the Momposina.  ``docs/42`` §6 states the ground truth this must
    reproduce: *all 18 usable SSC stations lie upstream of the Cauca-Magdalena confluence*.

    ``channel_km_below_reference`` is returned so the split can be checked against a
    published number rather than trusted: it must come out at **801.1 km**
    (``docs/42`` §4.5 / G9, the whole Momposina).

    This helper exists so that a C4.3 script cannot silently include a below-Mompós station
    in an objective.  **It grants no permission**: a below-Mompós station in a fit violates
    this module's declared limitation whether or not the code notices.  Nothing here is a
    substitute for reading the docstring.
    """
    ref = int(net.index_of([momposina_ref_minibacia])[0])
    trunk_below = net.downstream_path(ref)
    below = np.zeros(net.n_reach, dtype=bool)
    below[trunk_below[1:]] = True
    idx = net.index_of(list(station_minibacias))
    cal = [int(net.ids[i]) for i in idx if not below[i]]
    ev = [int(net.ids[i]) for i in idx if below[i]]
    return {
        "reference_minibacia": int(net.ids[ref]),
        "calibrate": cal,
        "evaluate_only": ev,
        "n_calibrate": len(cal),
        "n_evaluate_only": len(ev),
        "n_reaches_below_reference": int(below.sum()),
        "channel_km_below_reference": float(net.reach_km[trunk_below].sum()),
        "rule": ("calibrate upstream of the Momposina only; evaluate below it, never "
                 "calibrate there (docs/31 §C4.1)"),
        "note": MOMPOSINA_NOTE,
    }
