"""MGB-SA daily water-balance engine for the Magdalena basin.

WHAT THIS IS
------------
A vectorised, importable implementation of the daily rainfall-runoff formulation
*derived by this project itself* in ``notebooks/03_hydrology.ipynb`` (sections 1-5),
extended with the canopy-interception store that notebook 03 names but does not code
("P - precipitation reaching the soil (after canopy interception)").

It is NOT a generic HBV/GR4J/Sacramento. Every equation below is traceable either to
notebook 03 or to Collischonn (2001) / Collischonn et al. (2007), the MGB-IPH papers
notebook 03 paraphrases.

STATE AND FLUXES (per day, dt = 1 day)
--------------------------------------
Two nested resolutions, exactly as notebook 03 section 5 prescribes:

  * **URH level** (soil x land-cover unit, 24 types): canopy store ``Sc`` and soil
    store ``W``.  One balance per (minibacia, URH) pair that actually has area.
  * **Minibacia level**: the three linear reservoirs (surface / subsurface /
    groundwater) and the channel store.  Notebook 03 s.5: "runoff from all URHs of a
    minibacia is aggregated (area-weighted), passed through these reservoirs into the
    minibacia's river reach, then routed reach by reach downstream".

1. Canopy interception (MGB-IPH; alpha * LAI bucket)::

       Sc      += P                                   # gross rainfall
       Pthr     = max(Sc - Simax, 0);  Sc -= Pthr     # throughfall reaches the soil
       Ecan     = min(PET, Sc);        Sc -= Ecan     # evaporates at the POTENTIAL rate
       PETsoil  = PET - Ecan                          # what is left for the soil

   with ``Simax = alpha_int * LAI``.  LAI = 0 (bare, urban, open water) => Simax = 0 =>
   the store is inert and Pthr == P, so the engine degrades exactly to notebook 03.

2. Saturation-excess runoff with variable contributing area (nb03 s.2, verbatim)::

       Asat = 1 - (1 - W/Wm)**b
       Dsup = Pthr * Asat
       W   += Pthr - Dsup
       if W > Wm:  Dsup += W - Wm;  W = Wm      # nb03's second, "bucket-full" term

3. Evapotranspiration, limited by BOTH demand and supply (nb03 s.1)::

       ET = min(kc * PETsoil * (W/Wm), W)
       W -= ET

4. Percolation out of the soil column.  Two modes:

   ``percolation='linear'`` (**default**, nb03 s.4 cell 7)::

       drain = adr * W;  W -= drain
       Dint  = fint * drain
       Dbas  = (1 - fint) * drain

   ``percolation='mgb'`` (Collischonn 2001, the published nonlinear form)::

       Dint = Kint * ((W - Wz)/(Wm - Wz)) ** (3 + 2/lam)     for W > Wz, else 0
       Dbas = Kbas * (W/Wm)
       (jointly rescaled if Dint + Dbas > W, so W can never go negative)

5. Three linear reservoirs at the minibacia (nb03 s.3, ``Q = Q0 exp(-t/K)``).
   ``reservoir='exact'`` (**default**) uses the analytic one-day solution::

       S += inflow;  Q = S * (1 - exp(-dt/K));  S -= Q

   ``reservoir='euler'`` reproduces notebook 03 cell 7 literally (``Q = S/K``); it is
   kept only so the notebook can be regression-tested and is unstable for K < 1.

6. Channel routing down ``minibacias.csv`` (see ROUTING below).

UNITS
-----
* ``W``, ``Sc``, ``Wm`` .............. mm of the URH's own area
* ``Dsup/Dint/Dbas``, ``P``, ``PET`` . mm/day
* reservoir stores ``Ssup/Sint/Sbas``  mm of the minibacia's own area
* channel store, all routed flow ..... ``mm.km2`` and ``mm.km2/day`` (= 1000 m3),
  because water crossing a reach boundary changes reference area.  Convert with
  ``MM_KM2_PER_DAY_TO_M3S``.

ROUTING - the choice, and what was rejected
-------------------------------------------
Implemented: **one linear reservoir per reach**, i.e. Muskingum with X = 0, solved with
a within-day topological sweep so water can cross many reaches in a single day::

    S_i += local_i + sum(Q_j for j draining into i)
    Q_i  = S_i * (1 - exp(-dt/tau_i));   S_i -= Q_i

* Why: mass conservation is structural (every drop is either released or still in
  ``S``), it needs exactly one parameter per reach (``tau_i``, travel time in days),
  and it degrades continuously to instantaneous accumulation as ``tau -> 0``.  With
  ~6 km reaches the physical travel time is ~0.1 d, i.e. FAR below the daily step;
  a scheme that could not represent sub-daily lags would be useless here.
* Rejected - **Muskingum-Cunge** (notebook 03 s.5's "simpler" option): its coefficients
  need channel width, depth, slope and celerity.  ``minibacias.csv`` carries only
  ``id, area_km2, downstream``; inventing hydraulic geometry would be fabricating data.
  When geometry exists, Muskingum with X > 0 is a drop-in generalisation of the very
  same storage equation, so this is not a dead end.
* Rejected - **integer-day translation** (pure lag, no attenuation): also conserves
  mass, but the true per-reach lag (~0.1 d) would have to be rounded to 0 or 1 day,
  i.e. either no lag at all or a 292-day traverse of the mainstem.  Unusable.
* Rejected - **instantaneous accumulation** (sum all upstream, no storage): the
  mainstem is ~1500 km, so real travel time to Calamar is weeks.  Zero lag would
  destroy every peak-timing metric the calibration is judged on.
* Rejected - **local-inertial / hydrodynamic** (notebook 03 s.5's recommendation for
  the lower Magdalena): needs cross-sections, a floodplain DEM, a sub-daily step and an
  implicit solver.  Out of scope for a NumPy daily engine and properly the plugin's job.
  DOCUMENTED CONSEQUENCE: backwater and floodplain storage in the Mompos / Mojana
  cienagas are NOT represented; gauges there will show timing error this engine cannot
  remove by calibration.

WARNING - ``K`` in ``minibacia_soil_params.csv`` IS NOT A HYDROLOGICAL PARAMETER
--------------------------------------------------------------------------------
``data/processed/minibacia_soil_params.csv`` has columns ``Wm_mm`` and ``K``.  Only
``Wm_mm`` belongs here.  Notebook 09 section 4 defines ``K`` as the **MUSLE soil
erodibility** (t.ha.h/(ha.MJ.mm)), a SEDIMENT parameter.  Its basin values (~0.02-0.05)
are numerically close to notebook 03's drainage fraction ``adr = 0.06``, so wiring
``K`` into ``MgbParams.adr`` would run without error and be silently wrong.
``load_soil_params()`` therefore returns ``Wm_mm`` only, and ``MgbParams`` has no field
named ``K``.

PERFORMANCE
-----------
Loops over TIME ONLY.  Everything else is NumPy over the 32,782 (minibacia, URH) pairs
that actually have area - 15.8 % of the dense 8,672 x 24 grid, so a dense formulation
would waste 6x the work.

MEASURED on the real basin (8,672 minibacias, 32,782 URH cells, 3,287 days, 4 repeats,
recording 67 gauge minibacias): NumPy backend 29.9-36.5 s (median 33.8 s), numba backend
13.8-18.1 s (median 17.2 s), i.e. a 2.2x speedup.  ``src/test_mgb_hydrology.py`` re-times
a 200-day slice and asserts the projected full run stays under 300 s.

Two routing backends exist *on purpose*: the NumPy level sweep is the reference and needs
no optional dependency, the numba topological node loop is the fast path, and the test
suite asserts the two agree.  That is a second independent implementation of the routing,
not merely a speedup - see test 5b / 5b2.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Optional, Sequence

import numpy as np

__all__ = [
    "DT_DAYS",
    "MM_KM2_PER_DAY_TO_M3S",
    "URH_CODES",
    "MgbTopology",
    "MgbParams",
    "MgbState",
    "MgbResult",
    "build_topology",
    "load_topology",
    "load_soil_params",
    "load_forcing",
    "intersect_forcing",
    "default_channel_tau",
    "urh_soil_family",
    "urh_land_class",
    "simulate",
]

DT_DAYS = 1.0
#: (mm.km2)/day -> m3/s.  1 mm over 1 km2 = 1e-3 m * 1e6 m2 = 1000 m3.
MM_KM2_PER_DAY_TO_M3S = 1000.0 / 86400.0

#: URH id = soil_family*10 + land_class (notebook 08 step 4).
#: soil family 1=Coarse 2=Medium 3=Fine; land 1=Forest 2=Shrub 3=Grassland
#: 4=Cropland 5=Urban 6=Bare 7=Water 8=Wetland.
URH_CODES: tuple[int, ...] = tuple(
    s * 10 + l for s in (1, 2, 3) for l in (1, 2, 3, 4, 5, 6, 7, 8)
)
N_URH = len(URH_CODES)

_EPS = 1e-300


def urh_soil_family(code: int) -> int:
    """1=Coarse, 2=Medium, 3=Fine (notebook 08)."""
    return int(code) // 10


def urh_land_class(code: int) -> int:
    """1=Forest .. 8=Wetland (notebook 08)."""
    return int(code) % 10


# ---------------------------------------------------------------------------
# topology
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MgbTopology:
    """Immutable spatial structure: minibacia network + active (minibacia, URH) cells.

    Built once, reused for every parameter set - the whole point of separating it from
    :class:`MgbParams` is that calibration re-runs must not re-derive the topology.
    """

    ids: np.ndarray            # (n,) int64  minibacia ids, in internal order
    area_km2: np.ndarray       # (n,) float64
    down: np.ndarray           # (n,) int64  internal index of receiver, -1 at an outlet
    outlets: np.ndarray        # (n_out,) int64
    order: np.ndarray          # (n,) int64  topological order, upstream -> downstream
    level: np.ndarray          # (n,) int64  0 = headwater, level = 1 + max(upstream)
    cell_mini: np.ndarray      # (N,) int64  internal minibacia index per active cell
    cell_urh: np.ndarray       # (N,) int64  URH column 0..23
    cell_frac: np.ndarray      # (N,) float64 area fraction of its minibacia
    cell_area_km2: np.ndarray  # (N,) float64 = cell_frac * area_km2[cell_mini]
    urh_codes: np.ndarray      # (24,) int64
    frac_sum: np.ndarray       # (n,) float64  sum of fractions (~1.0)
    sorted_ids: np.ndarray = field(repr=False, default=None)   # (n,) ids ascending
    sorted_pos: np.ndarray = field(repr=False, default=None)   # (n,) internal index
    levels: tuple = field(repr=False, default=())

    @property
    def n_mini(self) -> int:
        return int(self.ids.size)

    @property
    def n_cells(self) -> int:
        return int(self.cell_mini.size)

    @property
    def covered_area_km2(self) -> float:
        """Area that actually receives forcing: sum(frac_sum * area).

        Differs from ``sum(area_km2)`` only if some minibacia has URH fractions that do
        not sum to 1.  Rainfall depths and runoff depths are both referenced to THIS
        area so they are directly comparable.
        """
        return float(np.dot(self.frac_sum, self.area_km2))

    def index_of(self, ids: Sequence[int]) -> np.ndarray:
        """Internal indices of the given minibacia ids (raises if any is unknown)."""
        want = np.asarray(ids, dtype=np.int64)
        loc = np.clip(np.searchsorted(self.sorted_ids, want), 0, self.sorted_ids.size - 1)
        ok = self.sorted_ids[loc] == want
        if not ok.all():
            raise KeyError(f"unknown minibacia ids: {want[~ok][:10].tolist()}")
        return self.sorted_pos[loc]


def build_topology(
    ids: Sequence[int],
    area_km2: Sequence[float],
    downstream: Sequence[int],
    urh_matrix: np.ndarray,
    urh_codes: Sequence[int] = URH_CODES,
    *,
    frac_tol: float = 1e-6,
) -> MgbTopology:
    """Validate and pack the network + URH composition.

    ``urh_matrix`` is (n, n_urh) area fractions, rows aligned with ``ids``.
    ``downstream`` uses minibacia *ids*, with -1 (or an id not in ``ids``) marking an
    outlet.  Cycles, self-loops and unknown receivers raise.

    Only cells with fraction > 0 are kept; the model never evaluates a URH that has no
    area in a minibacia.
    """
    ids = np.asarray(ids, dtype=np.int64)
    area = np.asarray(area_km2, dtype=np.float64)
    dsid = np.asarray(downstream, dtype=np.int64)
    urh_matrix = np.asarray(urh_matrix, dtype=np.float64)
    n = ids.size
    if np.unique(ids).size != n:
        raise ValueError("duplicate minibacia ids")
    if area.shape != (n,) or dsid.shape != (n,):
        raise ValueError("ids / area_km2 / downstream length mismatch")
    if np.any(area <= 0):
        raise ValueError("non-positive minibacia area")
    if urh_matrix.shape != (n, len(urh_codes)):
        raise ValueError(f"urh_matrix must be {(n, len(urh_codes))}, got {urh_matrix.shape}")
    if np.any(urh_matrix < 0) or not np.all(np.isfinite(urh_matrix)):
        raise ValueError("urh_matrix has negative or non-finite entries")

    srt = np.argsort(ids, kind="stable")
    sids = ids[srt]
    loc = np.searchsorted(sids, dsid)
    loc_c = np.clip(loc, 0, n - 1)
    known = (dsid >= 0) & (sids[loc_c] == dsid)
    down = np.where(known, srt[loc_c], -1).astype(np.int64)
    if np.any(down == np.arange(n)):
        bad = ids[down == np.arange(n)][:5]
        raise ValueError(f"self-draining minibacia(s): {bad.tolist()}")
    outlets = np.flatnonzero(down < 0).astype(np.int64)
    if outlets.size == 0:
        raise ValueError("no outlet: every minibacia drains somewhere (cycle)")

    order, level = _topological_order(down)
    frac_sum = urh_matrix.sum(axis=1)
    if np.any(np.abs(frac_sum - 1.0) > frac_tol):
        worst = float(np.max(np.abs(frac_sum - 1.0)))
        warnings.warn(
            f"URH fractions do not sum to 1 (max deviation {worst:.3e}). The engine "
            "stays mass-conservative because minibacia volumes use cell_area_km2 = "
            "frac * area, but the uncovered fraction of the minibacia produces no "
            "runoff.",
            stacklevel=2,
        )
    mi, ui = np.nonzero(urh_matrix > 0.0)
    return MgbTopology(
        ids=ids,
        area_km2=area,
        down=down,
        outlets=outlets,
        order=order,
        level=level,
        cell_mini=mi.astype(np.int64),
        cell_urh=ui.astype(np.int64),
        cell_frac=urh_matrix[mi, ui],
        cell_area_km2=urh_matrix[mi, ui] * area[mi],
        urh_codes=np.asarray(urh_codes, dtype=np.int64),
        frac_sum=frac_sum,
        sorted_ids=sids,
        sorted_pos=srt.astype(np.int64),
        levels=_pack_levels(level, down),
    )


def _topological_order(down: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Kahn sweep. ``level[i] = 1 + max(level of inflowing nodes)``; headwaters are 0."""
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
        raise ValueError(f"network contains a cycle: only {k}/{n} nodes are orderable")
    return order, level


def _pack_levels(level: np.ndarray, down: np.ndarray) -> tuple:
    """Pre-slice nodes by level so the daily sweep does no fancy indexing of ``down``."""
    out = []
    for L in range(int(level.max()) + 1):
        idx = np.flatnonzero(level == L).astype(np.int64)
        tgt = down[idx]
        has = tgt >= 0
        out.append((idx, has, tgt[has]))
    return tuple(out)


# ---------------------------------------------------------------------------
# parameters
# ---------------------------------------------------------------------------


def _as_urh(value, name: str) -> np.ndarray:
    a = np.asarray(value, dtype=np.float64)
    if a.ndim == 0:
        return np.full(N_URH, float(a))
    if a.shape != (N_URH,):
        raise ValueError(f"{name} must be scalar or length {N_URH}, got {a.shape}")
    return a.astype(np.float64, copy=True)


def _as_mini(value, n: int, name: str) -> np.ndarray:
    a = np.asarray(value, dtype=np.float64)
    if a.ndim == 0:
        return np.full(n, float(a))
    if a.shape != (n,):
        raise ValueError(f"{name} must be scalar or length {n}, got {a.shape}")
    return a.astype(np.float64, copy=True)


@dataclass
class MgbParams:
    """Every tunable number, with the default's origin stated.

    Per-URH fields accept a scalar or a length-24 array ordered like :data:`URH_CODES`.
    Per-minibacia fields accept a scalar or a length-n array ordered like
    ``topology.ids``.  Nothing here is fitted - these are documented priors for the
    calibration step to move.
    """

    # ---- soil store -------------------------------------------------------
    #: per-minibacia soil storage capacity (mm).  Prior = IGAC ``Wm_mm`` from nb09.
    wm_mini: object = 120.0
    #: per-URH multiplier on ``wm_mini``.  nb09 s.7: "calibration will scale Wm per URH".
    wm_scale: object = 1.0
    #: variable-contributing-area shape (nb03 s.2 uses 0.6 in its worked example).
    b: object = 0.6
    #: crop/vegetation coefficient on PET.  1.0 = nb03 exactly (ET = ETp * W/Wm).
    kc: object = 1.0

    # ---- canopy -----------------------------------------------------------
    #: leaf area index per URH.  0.0 = interception switched off => literal nb03.
    lai: object = 0.0
    #: canopy storage per unit LAI (mm).  0.2 mm is the MGB-IPH value.
    alpha_int: object = 0.2

    # ---- percolation ------------------------------------------------------
    percolation: str = "linear"     # 'linear' (nb03 cell 7) | 'mgb' (Collischonn 2001)
    #: 'linear': daily drainage fraction of W.  nb03 cell 7 uses adr = 0.06.
    adr: object = 0.06
    #: 'linear': share of drainage going to interflow.  nb03 cell 7 uses fint = 0.6.
    fint: object = 0.6
    #: 'mgb': maximum interflow drainage (mm/day).
    kint_mm: object = 4.0
    #: 'mgb': maximum groundwater drainage (mm/day).
    kbas_mm: object = 0.6
    #: 'mgb': residual-moisture threshold, as a fraction of Wm, below which Dint stops.
    wz_frac: object = 0.1
    #: 'mgb': Brooks-Corey pore-size index; exponent is 3 + 2/lam.
    lam: object = 0.4

    # ---- linear reservoirs (nb03 s.3).  MGB-IPH calls these CS / CI / CB. ----
    reservoir: str = "exact"        # 'exact' (analytic) | 'euler' (nb03 cell 7, Q=S/K)
    k_sup: object = 1.5             # surface residence time, days  (CS)
    k_int: object = 8.0             # subsurface residence time, days (CI)
    k_bas: object = 60.0            # groundwater residence time, days (CB / Kbas)

    # ---- channel ----------------------------------------------------------
    #: reach travel time, days.  0 => the reach has no storage (pass-through).
    tau_channel: object = 0.1

    def __post_init__(self) -> None:
        if self.percolation not in ("linear", "mgb"):
            raise ValueError("percolation must be 'linear' or 'mgb'")
        if self.reservoir not in ("exact", "euler"):
            raise ValueError("reservoir must be 'exact' or 'euler'")

    # -- expansion ---------------------------------------------------------

    def expand(self, topo: MgbTopology) -> "_Expanded":
        """Broadcast to flat per-cell / per-minibacia arrays and validate ranges."""
        n = topo.n_mini
        u = topo.cell_urh
        wm_mini = _as_mini(self.wm_mini, n, "wm_mini")
        if np.any(wm_mini < 0) or not np.all(np.isfinite(wm_mini)):
            raise ValueError("wm_mini must be finite and >= 0")
        wm = wm_mini[topo.cell_mini] * _as_urh(self.wm_scale, "wm_scale")[u]
        b = _as_urh(self.b, "b")[u]
        if np.any(b < 0):
            raise ValueError("b must be >= 0")
        kc = _as_urh(self.kc, "kc")[u]
        simax = (_as_urh(self.alpha_int, "alpha_int") * _as_urh(self.lai, "lai"))[u]
        if np.any(simax < 0):
            raise ValueError("alpha_int * lai must be >= 0")

        adr = _as_urh(self.adr, "adr")[u]
        fint = _as_urh(self.fint, "fint")[u]
        if self.percolation == "linear":
            if np.any((adr < 0) | (adr > 1)):
                raise ValueError("adr must lie in [0, 1] so drainage <= W")
            if np.any((fint < 0) | (fint > 1)):
                raise ValueError("fint must lie in [0, 1]")
        kint = _as_urh(self.kint_mm, "kint_mm")[u]
        kbas = _as_urh(self.kbas_mm, "kbas_mm")[u]
        wzf = _as_urh(self.wz_frac, "wz_frac")[u]
        lam = _as_urh(self.lam, "lam")[u]
        if self.percolation == "mgb":
            if np.any(kint < 0) or np.any(kbas < 0):
                raise ValueError("kint_mm / kbas_mm must be >= 0")
            if np.any((wzf < 0) | (wzf >= 1)):
                raise ValueError("wz_frac must lie in [0, 1)")
            if np.any(lam <= 0):
                raise ValueError("lam must be > 0")

        ks = _as_mini(self.k_sup, n, "k_sup")
        ki = _as_mini(self.k_int, n, "k_int")
        kb = _as_mini(self.k_bas, n, "k_bas")
        tau = _as_mini(self.tau_channel, n, "tau_channel")
        for nm, arr in (("k_sup", ks), ("k_int", ki), ("k_bas", kb), ("tau_channel", tau)):
            if np.any(arr < 0) or not np.all(np.isfinite(arr)):
                raise ValueError(f"{nm} must be finite and >= 0")
            if self.reservoir == "euler" and nm != "tau_channel" and np.any((arr > 0) & (arr < 1)):
                raise ValueError(
                    f"{nm} < 1 day is unstable with reservoir='euler' (Q = S/K would "
                    "exceed S). Use reservoir='exact'."
                )
        return _Expanded(
            wm=wm,
            wm_pos=wm > 0.0,
            wm_safe=np.where(wm > 0.0, wm, 1.0),
            b=b,
            kc=kc,
            simax=simax,
            adr=adr,
            fint=fint,
            kint=kint,
            kbas=kbas,
            wz=wzf * wm,
            expo=3.0 + 2.0 / np.where(lam > 0, lam, 1.0),
            c_sup=_release_coef(ks, self.reservoir),
            c_int=_release_coef(ki, self.reservoir),
            c_bas=_release_coef(kb, self.reservoir),
            c_ch=_release_coef(tau, "exact"),
            percolation=self.percolation,
        )


def _release_coef(k: np.ndarray, mode: str) -> np.ndarray:
    """Fraction of a linear reservoir released in one day.

    ``exact``  : 1 - exp(-dt/K), the analytic solution of dS/dt = -S/K, i.e. exactly the
                 ``Q = Q0 exp(-t/K)`` recession notebook 03 s.3 writes down.  Bounded in
                 (0, 1] for every K >= 0, so storage can never go negative.
    ``euler``  : dt/K, which is what notebook 03 cell 7 codes (``Q = S/K``).  Kept for
                 bit-level regression against the notebook; rejected as the default
                 because it releases more than the store holds whenever K < dt.
    """
    k = np.asarray(k, dtype=np.float64)
    if mode == "euler":
        return np.where(k > 0.0, DT_DAYS / np.where(k > 0.0, k, 1.0), 1.0)
    return np.where(k > 0.0, -np.expm1(-DT_DAYS / np.where(k > 0.0, k, 1.0)), 1.0)


@dataclass
class _Expanded:
    wm: np.ndarray
    wm_pos: np.ndarray
    wm_safe: np.ndarray
    b: np.ndarray
    kc: np.ndarray
    simax: np.ndarray
    adr: np.ndarray
    fint: np.ndarray
    kint: np.ndarray
    kbas: np.ndarray
    wz: np.ndarray
    expo: np.ndarray
    c_sup: np.ndarray
    c_int: np.ndarray
    c_bas: np.ndarray
    c_ch: np.ndarray
    percolation: str


# ---------------------------------------------------------------------------
# state
# ---------------------------------------------------------------------------


@dataclass
class MgbState:
    """Mutable state.  ``sc``/``w`` are per active cell; the rest per minibacia."""

    sc: np.ndarray       # (N,) canopy store, mm
    w: np.ndarray        # (N,) soil store, mm
    s_sup: np.ndarray    # (n,) surface reservoir, mm
    s_int: np.ndarray    # (n,) subsurface reservoir, mm
    s_bas: np.ndarray    # (n,) groundwater reservoir, mm
    s_ch: np.ndarray     # (n,) channel store, mm.km2

    @classmethod
    def initial(
        cls,
        topo: MgbTopology,
        params: MgbParams,
        *,
        w_frac: float = 0.4,
        s_bas_mm: float = 0.0,
    ) -> "MgbState":
        """Cold start: soil at ``w_frac * Wm``, all reservoirs at ``s_bas_mm`` / zero.

        ``w_frac = 0.4`` is a deliberately mid-range, non-informative guess: any start
        is wrong, so the run must be given a warm-up long enough that the answer stops
        depending on it (``simulate(..., warmup_days=...)``).  ``s_bas_mm > 0`` shortens
        the groundwater warm-up, which is the slowest state (K_bas ~ 60 d).
        """
        ex = params.expand(topo)
        return cls(
            sc=np.zeros(topo.n_cells),
            w=np.clip(float(w_frac), 0.0, 1.0) * ex.wm,
            s_sup=np.zeros(topo.n_mini),
            s_int=np.zeros(topo.n_mini),
            s_bas=np.full(topo.n_mini, float(s_bas_mm)),
            s_ch=np.zeros(topo.n_mini),
        )

    def copy(self) -> "MgbState":
        return MgbState(
            self.sc.copy(), self.w.copy(), self.s_sup.copy(),
            self.s_int.copy(), self.s_bas.copy(), self.s_ch.copy(),
        )

    def storage_volume(self, topo: MgbTopology) -> float:
        """Total water held, in mm.km2 - the quantity the mass-balance test tracks.

        Reference areas matter and are easy to get wrong: ``sc``/``w`` are depths over
        the URH's OWN area (``cell_area_km2 = frac * area``), whereas the three
        reservoirs are fed by ``sum_u frac_u * D_u``, i.e. depths over the minibacia's
        FULL area, so their volume uses ``area_km2`` and NOT ``frac_sum * area_km2``.
        With this project's fractions summing to exactly 1.0 the two are identical, so a
        mistake here would be invisible on the real data - test 1c forces frac_sum != 1.
        """
        return float(
            np.dot(self.sc + self.w, topo.cell_area_km2)
            + np.dot(self.s_sup + self.s_int + self.s_bas, topo.area_km2)
            + self.s_ch.sum()
        )


# ---------------------------------------------------------------------------
# the daily kernel
# ---------------------------------------------------------------------------


def _vertical_step(ex: _Expanded, st: MgbState, p_cell: np.ndarray, pet_cell: np.ndarray):
    """One day of the URH column balance.  Returns (Dsup, Dint, Dbas, ET) in mm/day.

    Mutates ``st.sc`` and ``st.w``.  ``Wm == 0`` cells (impervious / open water, if the
    caller sets them so) are handled without dividing by zero: ``Asat = 1`` so all
    throughfall becomes surface runoff, and ET / percolation are 0 because there is no
    store to draw from.
    """
    # --- 1. canopy -----------------------------------------------------
    sc = st.sc + p_cell
    thr = np.maximum(sc - ex.simax, 0.0)
    sc -= thr
    e_can = np.minimum(pet_cell, sc)
    sc -= e_can
    st.sc = sc
    pet_soil = pet_cell - e_can

    # --- 2. saturation excess, variable contributing area --------------
    w = st.w
    rel = np.clip(w / ex.wm_safe, 0.0, 1.0)
    a_sat = np.where(ex.wm_pos, 1.0 - (1.0 - rel) ** ex.b, 1.0)
    d_sup = thr * a_sat
    w = w + thr - d_sup
    exc = np.maximum(w - ex.wm, 0.0)
    d_sup = d_sup + exc
    w = w - exc

    # --- 3. evapotranspiration: min(demand, supply) --------------------
    et_soil = np.where(ex.wm_pos, np.minimum(ex.kc * pet_soil * (w / ex.wm_safe), w), 0.0)
    w = w - et_soil

    # --- 4. percolation ------------------------------------------------
    if ex.percolation == "linear":
        drain = ex.adr * w
        d_int = ex.fint * drain
        d_bas = drain - d_int
    else:
        over = np.maximum(w - ex.wz, 0.0)
        span = np.maximum(ex.wm - ex.wz, _EPS)
        d_int = ex.kint * np.where(ex.wm_pos, (over / span) ** ex.expo, 0.0)
        d_bas = ex.kbas * np.where(ex.wm_pos, np.clip(w / ex.wm_safe, 0.0, 1.0), 0.0)
        tot = d_int + d_bas
        scale = np.where(tot > w, w / np.maximum(tot, _EPS), 1.0)
        d_int = d_int * scale
        d_bas = d_bas * scale
        drain = d_int + d_bas
    w = w - drain
    # Both modes are constructed so that w >= 0 exactly (adr <= 1 in 'linear';
    # proportional rescaling in 'mgb'), so this clip should only ever absorb float
    # rounding.  Its magnitude is RETURNED rather than swallowed, so the mass balance
    # stays exact and any real clipping shows up as a non-zero 'clip' term.
    clip = np.maximum(-w, 0.0)
    st.w = w + clip
    return d_sup, d_int, d_bas, et_soil + e_can, clip


def _reservoir_step(ex: _Expanded, st: MgbState, i_sup, i_int, i_bas):
    """Three linear reservoirs at the minibacia.  Returns local runoff in mm/day."""
    st.s_sup += i_sup
    q_sup = st.s_sup * ex.c_sup
    st.s_sup -= q_sup
    st.s_int += i_int
    q_int = st.s_int * ex.c_int
    st.s_int -= q_int
    st.s_bas += i_bas
    q_bas = st.s_bas * ex.c_bas
    st.s_bas -= q_bas
    return q_sup, q_int, q_bas


def _route_numpy(topo: MgbTopology, c_ch: np.ndarray, s_ch: np.ndarray,
                 local_vol: np.ndarray, inflow: np.ndarray, q_out: np.ndarray) -> None:
    """Within-day topological sweep, vectorised level by level.

    Reference implementation - always available, no optional dependency.  Nodes in the
    same level have no upstream/downstream relation to each other, so a whole level
    updates at once; 292 levels for this basin.  ``np.add.at`` (not ``inflow[tgt] += q``)
    is required because two nodes in one level may share the same receiver.
    """
    np.copyto(inflow, local_vol)
    for idx, has, tgt in topo.levels:
        s = s_ch[idx] + inflow[idx]
        q = s * c_ch[idx]
        s_ch[idx] = s - q
        q_out[idx] = q
        if tgt.size:
            np.add.at(inflow, tgt, q[has])


_NUMBA_ROUTE = [None]            # lazily compiled


def _get_numba_router():
    """Compile the topological node loop once.  Returns None if numba is unavailable."""
    if _NUMBA_ROUTE[0] is not None:
        return _NUMBA_ROUTE[0] or None
    try:
        from numba import njit
    except Exception:                                   # pragma: no cover
        _NUMBA_ROUTE[0] = False
        return None

    @njit(cache=True, fastmath=False)
    def _route(order, down, c_ch, s_ch, local_vol, inflow, q_out):
        n = order.shape[0]
        for i in range(n):
            inflow[i] = local_vol[i]
        for k in range(n):
            i = order[k]
            s = s_ch[i] + inflow[i]
            q = s * c_ch[i]
            s_ch[i] = s - q
            q_out[i] = q
            j = down[i]
            if j >= 0:
                inflow[j] += q

    _NUMBA_ROUTE[0] = _route
    return _route


# ---------------------------------------------------------------------------
# results
# ---------------------------------------------------------------------------


@dataclass
class MgbResult:
    """Routed discharge plus everything needed to audit the run."""

    dates: Optional[np.ndarray]
    record_ids: np.ndarray            # (m,) minibacia ids of the recorded columns
    q_m3s: np.ndarray                 # (ndays_rec, m) routed discharge
    #: basin-total daily series in mm.km2/day (all length = full simulated ndays)
    series: dict
    balance: dict
    state: MgbState
    wall_time_s: float
    routing_backend: str

    def q_at(self, mini_id: int) -> np.ndarray:
        j = int(np.flatnonzero(self.record_ids == int(mini_id))[0])
        return self.q_m3s[:, j]


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------


def _validate_forcing(precip, pet, n: int, warmup_days: int, dates):
    """Reject anything that would make the run silently wrong.  Returns (P, E, ndays)."""
    precip = np.ascontiguousarray(precip, dtype=np.float64)
    pet = np.ascontiguousarray(pet, dtype=np.float64)
    if precip.ndim != 2 or precip.shape[1] != n:
        raise ValueError(f"precip must be (ndays, {n}), got {precip.shape}")
    if pet.shape != precip.shape:
        raise ValueError(
            f"pet {pet.shape} must match precip {precip.shape}. The project's two "
            "forcing files cover DIFFERENT periods (precip 4018 d, pet 3287 d) - use "
            "intersect_forcing() to align them on dates, never by slicing to length."
        )
    if not np.all(np.isfinite(precip)) or not np.all(np.isfinite(pet)):
        raise ValueError("precip/pet contain NaN or inf - fill them before simulating")
    if np.any(precip < 0) or np.any(pet < 0):
        raise ValueError("precip/pet contain negative values")
    ndays = precip.shape[0]
    if not 0 <= warmup_days < ndays:
        raise ValueError(f"warmup_days must be in [0, {ndays})")
    if dates is not None and len(dates) != ndays:
        raise ValueError(
            f"dates has {len(dates)} entries but the forcing has {ndays} days - a "
            "mismatch here silently mislabels the output time axis"
        )
    return precip, pet, ndays


def _assemble_balance(ser: dict, topo: MgbTopology, v_start: float, v_end: float,
                      ndays: int) -> dict:
    """Close the water budget over the FULL simulated period, warm-up included.

    ``clip`` enters as an INPUT: it is water the negative-W guard created, so counting
    it makes the residual an exact identity and leaves any real clipping visible instead
    of hidden inside the residual.
    """
    p_tot = float(ser["p"].sum())
    et_tot = float(ser["et"].sum())
    q_tot = float(ser["q_outlet"].sum())
    clip_tot = float(ser["clip"].sum())
    resid = (p_tot + clip_tot) - et_tot - q_tot - (v_end - v_start)
    area = topo.covered_area_km2
    return {
        "p_volume_mm_km2": p_tot,
        "et_volume_mm_km2": et_tot,
        "outlet_volume_mm_km2": q_tot,
        "clip_volume_mm_km2": clip_tot,
        "storage_start_mm_km2": v_start,
        "storage_end_mm_km2": v_end,
        "residual_mm_km2": float(resid),
        "residual_relative": float(abs(resid) / max(p_tot, abs(v_start), 1.0)),
        "covered_area_km2": area,
        "total_area_km2": float(topo.area_km2.sum()),
        "p_mm": p_tot / area,
        "et_mm": et_tot / area,
        "runoff_mm": q_tot / area,
        "runoff_coefficient": (q_tot / p_tot) if p_tot > 0 else float("nan"),
        "ndays": ndays,
    }


def simulate(
    topo: MgbTopology,
    params: MgbParams,
    precip: np.ndarray,
    pet: np.ndarray,
    *,
    state: Optional[MgbState] = None,
    warmup_days: int = 0,
    record_ids: Optional[Sequence[int]] = None,
    dates: Optional[Sequence] = None,
    routing_backend: str = "auto",
    dtype_out: type = np.float32,
) -> MgbResult:
    """Run the daily water balance + routing.

    Parameters
    ----------
    precip, pet
        ``(ndays, n_mini)`` mm/day, columns ordered like ``topo.ids``.  Use
        :func:`load_forcing` to get that ordering from the wide project CSVs.
    warmup_days
        Leading days simulated but NOT written to ``q_m3s``.  The mass balance in
        ``balance`` always covers the FULL simulated period (warm-up included), because
        that is the only window over which initial and final storage are both known.
    record_ids
        Minibacia ids to write out.  ``None`` records all 8,672 (float32 => ~114 MB for
        3,287 days); pass the gauge list to keep it small.
    routing_backend
        ``'numpy'`` = level sweep (reference), ``'numba'`` = topological node loop,
        ``'auto'`` = numba if importable else numpy.  The two are asserted identical in
        ``src/test_mgb_hydrology.py``.
    """
    import time

    t_start = time.perf_counter()
    n = topo.n_mini
    precip, pet, ndays = _validate_forcing(precip, pet, n, warmup_days, dates)
    ex = params.expand(topo)
    st = MgbState.initial(topo, params) if state is None else state.copy()
    if st.w.shape != (topo.n_cells,) or st.s_sup.shape != (n,):
        raise ValueError("state does not match topology")
    v_start = st.storage_volume(topo)

    if record_ids is None:
        rec_idx = np.arange(n, dtype=np.int64)
        rec_ids = topo.ids.copy()
    else:
        rec_idx = topo.index_of(record_ids)
        rec_ids = topo.ids[rec_idx]
    n_rec_days = ndays - warmup_days
    q_out_rec = np.empty((n_rec_days, rec_idx.size), dtype=dtype_out)

    router = _get_numba_router() if routing_backend in ("auto", "numba") else None
    if routing_backend == "numba" and router is None:
        raise RuntimeError("routing_backend='numba' requested but numba is unavailable")
    backend = "numba" if router is not None else "numpy"

    cell_mini = topo.cell_mini
    cell_frac = topo.cell_frac
    a_cell = topo.cell_area_km2          # URH depth (mm) -> volume
    a_mini = topo.area_km2               # minibacia-reservoir depth (mm) -> volume
    keys = ("p", "et", "d_sup", "d_int", "d_bas", "q_sup", "q_int", "q_bas",
            "q_outlet", "clip")
    ser = {k: np.zeros(ndays) for k in keys}
    inflow = np.zeros(n)
    q_node = np.zeros(n)

    for t in range(ndays):
        p_cell = precip[t][cell_mini]
        pet_cell = pet[t][cell_mini]
        d_sup, d_int, d_bas, et, clip = _vertical_step(ex, st, p_cell, pet_cell)
        i_sup = np.bincount(cell_mini, weights=d_sup * cell_frac, minlength=n)
        i_int = np.bincount(cell_mini, weights=d_int * cell_frac, minlength=n)
        i_bas = np.bincount(cell_mini, weights=d_bas * cell_frac, minlength=n)
        q_sup, q_int, q_bas = _reservoir_step(ex, st, i_sup, i_int, i_bas)
        local_vol = (q_sup + q_int + q_bas) * a_mini
        if router is None:
            _route_numpy(topo, ex.c_ch, st.s_ch, local_vol, inflow, q_node)
        else:
            router(topo.order, topo.down, ex.c_ch, st.s_ch, local_vol, inflow, q_node)

        ser["p"][t] = np.dot(p_cell, a_cell)
        ser["et"][t] = np.dot(et, a_cell)
        ser["clip"][t] = np.dot(clip, a_cell)
        ser["d_sup"][t] = np.dot(d_sup, a_cell)
        ser["d_int"][t] = np.dot(d_int, a_cell)
        ser["d_bas"][t] = np.dot(d_bas, a_cell)
        ser["q_sup"][t] = np.dot(q_sup, a_mini)
        ser["q_int"][t] = np.dot(q_int, a_mini)
        ser["q_bas"][t] = np.dot(q_bas, a_mini)
        ser["q_outlet"][t] = q_node[topo.outlets].sum()
        if t >= warmup_days:
            q_out_rec[t - warmup_days] = q_node[rec_idx] * MM_KM2_PER_DAY_TO_M3S

    bal = _assemble_balance(ser, topo, v_start, st.storage_volume(topo), ndays)
    return MgbResult(
        dates=None if dates is None else np.asarray(dates)[warmup_days:],
        record_ids=rec_ids,
        q_m3s=q_out_rec,
        series=ser,
        balance=bal,
        state=st,
        wall_time_s=time.perf_counter() - t_start,
        routing_backend=backend,
    )


# ---------------------------------------------------------------------------
# loaders / helpers
# ---------------------------------------------------------------------------


def load_topology(processed_dir="data/processed", *, minibacias="minibacias.csv",
                  urh="urh_fractions.csv") -> MgbTopology:
    """Build the topology from ``minibacias.csv`` + ``urh_fractions.csv``.

    ``urh_fractions.csv`` has the minibacia id in column ``mini`` and one column per URH
    code ('11'...'38'); rows are reindexed onto ``minibacias.csv`` order, and a missing
    row is an error rather than an implicit zero-area minibacia.
    """
    import pandas as pd
    from pathlib import Path

    d = Path(processed_dir)
    mb = pd.read_csv(d / minibacias)
    uf = pd.read_csv(d / urh)
    for col in ("id", "area_km2", "downstream"):
        if col not in mb.columns:
            raise ValueError(f"{minibacias} is missing column '{col}'")
    if "mini" not in uf.columns:
        raise ValueError(f"{urh} is missing column 'mini'")
    codes = [c for c in uf.columns if c != "mini"]
    want = [str(c) for c in URH_CODES]
    if [str(c) for c in codes] != want:
        missing = set(want) - {str(c) for c in codes}
        raise ValueError(f"{urh} URH columns differ from URH_CODES; missing {sorted(missing)}")
    uf = uf.set_index("mini")
    missing_rows = set(mb.id) - set(uf.index)
    if missing_rows:
        raise ValueError(f"{urh} has no row for {len(missing_rows)} minibacias, e.g. "
                         f"{sorted(missing_rows)[:5]}")
    mat = uf.loc[mb.id.to_numpy(), codes].to_numpy(dtype=np.float64)
    return build_topology(mb.id.to_numpy(), mb.area_km2.to_numpy(),
                          mb.downstream.to_numpy(), mat)


def load_soil_params(topo: MgbTopology, path="data/processed/minibacia_soil_params.csv",
                     *, default_wm: Optional[float] = None) -> np.ndarray:
    """Return ``Wm_mm`` per minibacia, ordered like ``topo.ids``.

    Deliberately returns ONLY ``Wm_mm``.  The file's other numeric column, ``K``, is the
    MUSLE soil erodibility from notebook 09 section 4 - a sediment parameter.  It must
    never reach the water balance; see the module docstring.
    """
    import pandas as pd

    df = pd.read_csv(path)
    if "id" not in df.columns or "Wm_mm" not in df.columns:
        raise ValueError("minibacia_soil_params.csv needs columns 'id' and 'Wm_mm'")
    s = df.set_index("id")["Wm_mm"]
    out = s.reindex(topo.ids).to_numpy(dtype=np.float64)
    bad = ~np.isfinite(out) | (out <= 0)
    if bad.any():
        if default_wm is None:
            raise ValueError(
                f"{int(bad.sum())} minibacias have missing/non-positive Wm_mm "
                f"(e.g. ids {topo.ids[bad][:5].tolist()}). Pass default_wm to fill them "
                "explicitly rather than letting a silent 0 kill the soil store."
            )
        out = np.where(bad, float(default_wm), out)
    return out


def load_forcing(path: str, topo: MgbTopology, *, date_col: str = "date",
                 start=None, end=None):
    """Read a wide forcing CSV (date + one column per minibacia id) -> (array, dates).

    Columns are reordered to ``topo.ids``; a missing minibacia column is an error, not a
    zero-filled column, because silent zero rainfall is indistinguishable from drought.
    """
    import pandas as pd

    df = pd.read_csv(path)
    if date_col not in df.columns:
        raise ValueError(f"{path} has no '{date_col}' column")
    dates = pd.to_datetime(df[date_col])
    if start is not None or end is not None:
        m = np.ones(len(df), bool)
        if start is not None:
            m &= (dates >= pd.Timestamp(start)).to_numpy()
        if end is not None:
            m &= (dates <= pd.Timestamp(end)).to_numpy()
        df = df.loc[m]
        dates = dates.loc[m]
    have = {str(c) for c in df.columns}
    want = [str(i) for i in topo.ids]
    missing = [c for c in want if c not in have]
    if missing:
        raise ValueError(f"{path} lacks columns for {len(missing)} minibacias, e.g. "
                         f"{missing[:5]}")
    arr = df[want].to_numpy(dtype=np.float64)
    return arr, dates.to_numpy()


def intersect_forcing(p_arr, p_dates, e_arr, e_dates):
    """Restrict two forcing arrays to their common dates -> (p, e, dates).

    THIS EXISTS BECAUSE THE TWO PROJECT FORCING FILES DO NOT COVER THE SAME PERIOD:
    ``forcing_minibacia_precip.csv`` has 4018 days (2008-01-01..2018-12-31) while
    ``forcing_minibacia_pet.csv`` has 3287 (2009-01-01..2017-12-31, ERA5-bounded).
    ``simulate`` rejects a length mismatch, but a caller who "fixes" it by slicing the
    longer array from the wrong end gets a silent one-year offset between rainfall and
    evaporative demand - a bias no calibration could diagnose.  Align on dates, never on
    length.

    Returns rows in ascending date order and raises if the intersection is empty or if
    either input has duplicate dates.
    """
    import pandas as pd

    pd_dates = pd.DatetimeIndex(pd.to_datetime(p_dates))
    ed = pd.DatetimeIndex(pd.to_datetime(e_dates))
    if pd_dates.has_duplicates or ed.has_duplicates:
        raise ValueError("duplicate dates in a forcing file - deduplicate first")
    common = pd_dates.intersection(ed).sort_values()
    if len(common) == 0:
        raise ValueError(
            f"precip ({pd_dates.min().date()}..{pd_dates.max().date()}) and pet "
            f"({ed.min().date()}..{ed.max().date()}) do not overlap"
        )
    return (np.asarray(p_arr)[pd_dates.get_indexer(common)],
            np.asarray(e_arr)[ed.get_indexer(common)],
            common.to_numpy())


def default_channel_tau(area_km2: np.ndarray, celerity_m_s: float = 1.0) -> np.ndarray:
    """Crude first-guess reach travel time (days) from minibacia area.

    Reach length is approximated by the equivalent-circle diameter
    ``L = 2 sqrt(A/pi)`` and ``tau = L / celerity``.  For this basin's mean 29.7 km2
    that is L ~ 6.1 km and, at 1 m/s, tau ~ 0.07 d.

    This is a PRIOR, not a measurement: real reach lengths come from the D8 flow paths,
    and celerity varies from steep Andean headwaters to the near-flat lower Magdalena.
    Rejected alternative - deriving tau from Hack's law on upstream area: it gives the
    length of the whole flow path, not of one reach, so it would double-count lag once
    the reaches are chained.  Calibrate ``tau_channel`` against gauge peak timing.
    """
    a = np.asarray(area_km2, dtype=np.float64)
    length_km = 2.0 * np.sqrt(a / np.pi)
    return length_km * 1000.0 / (float(celerity_m_s) * 86400.0)
