"""MUSLE hillslope-erosion engine for the Magdalena basin (stage C3.4).

WHAT THIS IS
------------
A vectorised, importable implementation of **hillslope** (sheet + rill) soil loss with the
Modified Universal Soil Loss Equation, driven by the FROZEN H2E hydrology of Phase B.
It computes, per minibacia per day, the suspended-sediment load delivered from the
hillslopes to that minibacia's river reach, in **tonnes/day**.

It is NOT a channel model.  Advection, deposition and the Momposina floodplain sink are
stage C4 (``docs/31`` §C4.1) and deliberately absent here: this module's output is the
*input* to that step, so anything it produced downstream of the hillslope would be
double-counted later.

It re-runs NOTHING.  The hydrology is read from
``data/processed/sim_calibrated_v2/h2e_drivers.npz`` (546 MB, adopted cell H2E, FAO-56 ET,
``theta_crit`` 0.6, F 0.25931).  ``src/mgb_hydrology.py`` and that file are frozen twice
over (Phase B closed twice, docs/33 §8) and are opened read-only here.

THE EQUATION, EXACTLY AS PRE-REGISTERED (docs/35 §4, registered 2026-08-11)
--------------------------------------------------------------------------
::

    Sed_URH = (A_URH / a_p) * alpha * (Qsur * q_peak * a_p)^beta * K * C * P * LS2D * FG
    q_peak  = Qsur * a_p / 86.4                        (Buarque 2015 eq. 7)
    a_p     = 0.0081 km2                               (COP90 pixel, the registered scale)

i.e. MUSLE is evaluated **per DEM pixel** and multiplied by the number of pixels in the
URH cell, which is what keeps a fitted ``alpha`` comparable to Williams' 11.8 with no
scale correction (docs/35 §6.2: lumping ``N`` pixels inflates the load by ``N**(2*beta-1)``,
2.63x at the median minibacia).  ``q_peak`` is the registered proxy and is **not** a knob:
it comes from :mod:`scripts.c3.qpeak`, which this module imports rather than re-derives.

Every symbol, and where its number comes from:

===========  ===============================================  ==================================
symbol       meaning                                          source
===========  ===============================================  ==================================
``Qsur``     surface-runoff depth, mm/day                     ``h2e_drivers.npz:qsur_rel_mm``
``q_peak``   peak runoff rate, m3/s                           ``qpeak.qpeak_daily_mean`` (docs/35)
``a_p``      MUSLE application area, km2                      ``qpeak.COP90_PIXEL_AREA_KM2``
``A_URH``    URH cell area, km2                               ``urh_fractions.csv`` x ``minibacias.csv``
``K``        soil erodibility, per minibacia                  ``minibacia_soil_params.csv:K`` (nb09 §4)
``C``,``P``  cover / practice, per land class                 ``urh_cp_factors.csv`` (C3.2)
``LS2D``     2-D topographic factor, per URH cell             ``urh_ls2d.csv:ls2d_hs`` (C3.1)
``FG``       coarse-fragment factor                           1.0, see FG below
``alpha``    11.8                                             Williams (1975) - STARTING VALUE
``beta``     0.56                                             Williams (1975) - STARTING VALUE
===========  ===============================================  ==================================

``alpha`` and ``beta`` ARE NOT TUNED VALUES.  They are the published Williams (1975) pair,
adopted unchanged by Buarque (2015) eq. 5 *with this same daily-mean* ``q_peak``, and they
are here only so the module runs before stage C4 fits them.  C4's registered bands and hard
stops live in ``qpeak.check_musle_parameters`` - call it, do not retype the numbers.

UNITS - AND THE ONE OPEN UNIT QUESTION, STATED NOT HIDDEN
---------------------------------------------------------
* ``Qsur`` mm/day, ``q_peak`` m3/s, areas km2, ``K`` t.ha.h/(ha.MJ.mm), ``C``/``P``/``LS2D``
  dimensionless, output **tonnes/day**.
* MUSLE is an empirical, dimensionally inhomogeneous regression: the tonne scale is set
  entirely by ``alpha`` *at one particular unit convention*.  **THREE** conventions exist in
  the literature for the ``(Qsur * q_peak * A)`` product; they differ only by a constant
  factor, and no reading of the sources rules any of them out on its own:

  ``volume_convention='pixel_km2'`` (**default - the registered one, docs/35 §4**)
      the product is ``Qsur[mm] * q_peak[m3/s] * a_p[km2]``, i.e. the area is carried in
      **km2**, the unit Buarque (2015) eq. 7 needs for ``q_pico = Dsup*A/86.4``.
      CORRECTED 2026-08-11 (this module previously asserted that Buarque's MUSLE ``A`` "is
      the same km2 area his eq. 7 uses" - that assertion is DELETED, because this project's
      own source review says the opposite).  Verbatim, from
      ``data/processed/peakgap/method_research.md`` §1.1, written 62 min before this module:

          "Unit check: 1 mm/day over 1 km² = 1000 m³/day = 0.011574 m³/s = 1/86.4, so
          ``Dsup`` is mm/day and ``A`` is km² in eq. 7/12 (both texts label the MUSLE area
          ``A`` in ha for the erosion equation itself - mind the mixed units when porting)."

      So the km2 area is established for the ``q_peak`` equation ONLY.  For the erosion
      equation the sources say **ha**, which is the next convention.

  ``volume_convention='swat_mm_ha'`` (non-default; the convention ``alpha`` = 11.8 is
  normally quoted with)
      SWAT's standard MUSLE form, and the reading the sentence above points to:
      ``Q_surf[mm] * q_peak[m3/s] * area[ha]``.  ``area[ha] = 100 * area[km2]``, so the
      product is exactly ``100`` times the registered one and the load exactly
      ``100**beta = 13.18x`` larger (at ``beta`` = 0.56).

  ``volume_convention='williams_m3'`` (non-default, diagnostic only)
      Williams (1975) writes ``Y = 11.8 (V * q_p)^0.56 K C P LS`` with ``V`` the runoff
      **volume in m3**.  ``V = 1000 * Qsur[mm] * A[km2]``, so this convention's product is
      exactly ``1000`` times the registered one and its load is exactly
      ``1000**beta = 47.86x`` larger (at ``beta`` = 0.56).

  MEASURED on this basin with the uncalibrated defaults, 2009-2018, executed 2026-08-11
  (all three numbers are gross HILLSLOPE erosion, before any channel deposition, which is
  C4).  This is docs/35 §9.1's restated gate (b) - three rows, so the convention is CHOSEN,
  not inherited by taking the smallest:

  =========================  =============  =====================  ===================
  convention                 basin total    vs 144 / 184 Mt/yr     orders of magnitude
  =========================  =============  =====================  ===================
  ``pixel_km2`` (registered) 0.684 Mt/yr    210x / 269x below      2.32 - 2.43
  ``swat_mm_ha`` (x13.18)    9.02 Mt/yr     16.0x / 20.4x below    1.20 - 1.31
  ``williams_m3`` (x47.86)   32.76 Mt/yr    4.4x / 5.6x below      0.64 - 0.75
  =========================  =============  =====================  ===================

  Gross hillslope erosion should EXCEED the load measured at the outlet (a delivery ratio is
  < 1), so all three conventions are low - the registered one by two orders of magnitude,
  the SWAT/hectare one by ~1.2 orders.  **This module does not resolve that, and does not
  let ``alpha`` resolve it either.**  MEASURED (same run): reaching the 144 Mt/yr anchor with
  ``alpha`` alone would need ``alpha`` = 2483 (``pixel_km2``), 188 (``swat_mm_ha``) or 52
  (``williams_m3``) - respectively 70.1x, 5.3x and 1.5x past the pre-registered
  ``alpha`` > 35.4 hard stop.  Every convention still fails the hard stop, so the stop's
  verdict does not depend on which is chosen - but the SIZE of the residual gap does, by
  13.18x, which is why the enumeration had to be completed before C4 reads it.  (Separately,
  and not the same quantity: an ``alpha`` of ~565 in ``pixel_km2`` units merely reproduces
  the ``williams_m3`` LEVEL, 11.8 x 47.86.)  That is the
  hard stop doing exactly the job docs/35 §6.1 defines for it: "a fit that needs alpha far
  below Williams means something upstream is over-producing, and that must be found, not
  offset" - here in the opposite direction.  It is C3.6's gate and C4's problem, not a
  default to change quietly: switching the default convention is an AMENDMENT to
  docs/35 §9, with a date and a reason.
* No quantity in ``t/km2/yr`` is produced anywhere in this module, by design: per-area
  sediment yields are EMBARGOED (catchment areas disagree by >2x on 36 % of shared gauges,
  docs/23 §13.2).  Area enters only as the MUSLE application unit, and only as each
  minibacia's OWN area, which is the same number the frozen water balance used.

WHY THE DAILY TERM FACTORISES (an identity, not an approximation)
-----------------------------------------------------------------
``a_p`` is a constant and the frozen drivers carry ``Qsur`` per MINIBACIA, so within one
minibacia-day the runoff-energy term ``(Qsur * q_peak * a_p)^beta`` is the same number for
every URH cell.  Therefore::

    Sed_mini(t) = term(t, mini) * sum_over_cells[ (A_cell/a_p) * alpha * K*C*P*LS2D*FG ]
                = term(t, mini) * mini_factor(mini)

exactly, with the second factor static.  Two backends exploit this differently and the test
suite asserts they agree, the same two-implementation discipline the routing uses in
``mgb_hydrology.py``:

* ``backend='cells'``  - the reference: evaluate MUSLE on all 32,782 (minibacia, URH) cells
  every day through :func:`musle_load_tonnes` and ``bincount`` to the minibacia.  Obvious,
  and it gives per-cell output for free.
* ``backend='collapsed'`` - pre-sum the static per-cell factor once, then one multiply per
  minibacia-day.  Agrees with ``cells`` to float rounding only (different summation order, so
  agreement is asserted to 1e-12 relative, not bitwise).

MEASURED, and it changes why the second backend exists: the full basin-decade takes 2.0 s
with ``cells`` and 1.3 s with ``collapsed`` - only **1.5x**, because 32,782 cells x 3,652 days
is small.  So ``collapsed`` is NOT justified as an optimisation; it is justified as a second
independent implementation of the same identity, which is what the routing backends do in
``mgb_hydrology.py`` (test 5b there).  If the two ever disagree beyond rounding, one of them
has a bug and the test says so.

DOCUMENTED CONSEQUENCE - URH-level ``Qsur`` IS NOT RECOVERABLE.  The engine generated
surface runoff on the URH columns and area-weighted it to the minibacia before storing
(``h2e_drivers.npz`` field note for ``qsur_gen_mm``).  So all URHs of a minibacia share
their minibacia's ``Qsur`` here, and URH identity enters only through ``K``, ``C``, ``P``,
``LS2D`` and area.  A forest and a bare cell in the same minibacia therefore differ in
erodibility but not in runoff depth - which understates the contrast, because the bare cell
really does generate more runoff.  Un-mixing it would require re-running the frozen
hydrology with per-URH output, which is out of scope and forbidden here.

DELIVERY, AND THE MASS LEDGER (docs/35 §8 open item 4, answered)
---------------------------------------------------------------
Buarque (2015) delays each minibacia's sediment to the channel through a linear reservoir.
This module implements the same reservoir but **defaults its residence time to 0 days**::

    store += eroded
    delivered = store * (1 - exp(-dt/tau))     # tau = 0  =>  coefficient 1, pass-through
    store    -= delivered

Why ``tau_delivery_days = 0.0`` is the default: the registered ``Qsur`` is
``qsur_rel_mm``, the runoff **released by the minibacia's surface linear reservoir**
(engine ``q_sup``), not the runoff generated on the columns.  The lag Buarque applies to the
sediment has therefore already been applied to the water that drives it; adding a second
reservoir would double-count it.  The store is kept in the code and in the ledger anyway so
that (a) a non-zero ``tau`` is a one-line change if C4 wants one, and (b) the accounting is
structural rather than a lucky consequence of a default.

DOCUMENTED CONSEQUENCE of driving MUSLE with the *released* rather than the *generated*
runoff: the term is convex in ``Qsur`` (exponent ``2*beta`` = 1.12 > 1), so smoothing the
runoff before MUSLE yields less sediment than MUSLE-then-smooth.  Measured on the frozen
drivers, ``qsur_gen_mm`` gives 0.770 Mt/yr against ``qsur_rel_mm``'s 0.684, i.e. **1.125x**
- small, because the surface reservoir's residence time is short.  It is one more term in
the SAME direction as the registered
lower bound of docs/35 §5.3, and it is switchable via ``qsur_field`` for anyone who wants to
report the alternative - not silently averaged with it.

**Ledger.** ``eroded = delivered + stored`` exactly.  With the default pass-through the
identity is bitwise: ``tau = 0`` gives a release coefficient of exactly 1.0, so
``delivered`` is the same float as ``eroded`` and the store stays at exactly 0.0 for every
minibacia-day of the record; the reported residual is exactly ``0.0``, not a small number.
With ``tau > 0`` the daily arithmetic is still a structural partition (``store`` is defined
as ``S - delivered``, so no gram is created or dropped), and the cumulative totals are
accumulated with :func:`math.fsum` so the accounting adds no error of its own - the residual
then reflects only per-day float rounding (measured < 1e-15 relative).

INPUTS AND THE CAVEATS THEY BRING WITH THEM
-------------------------------------------
* ``K`` (``minibacia_soil_params.csv:K``) is per MINIBACIA, not per URH: 8,672 values,
  texture-derived (nb09 §4), 0 NaN, range 0.019-0.0495.  The same file's ``Wm_mm`` is a
  hydrological parameter and is NOT read here, mirroring the reverse warning in
  ``mgb_hydrology.py``: the two columns are numerically similar and confusing them runs
  without error and is silently wrong.
* ``C`` (C3.2) is per land class, and its dominant term is a low-end choice: grassland
  ``C`` = 0.01 (Roose's "good condition"), which carries 36.8 % of the area-weighted basin
  ``C`` while Roose's own table spans a factor of 10 up to overgrazed/burnt.  Basin-mean
  ``C`` is nearly linear in it.  ``P`` = 1.0 basin-wide is an EXPLICIT assumption (no
  conservation-practice layer exists), which makes the practice term an upper bound on
  erosion.  Bare ``C`` = 1.0 is applied above the treeline where the surface is rock, ash
  and ice: with ``K`` non-zero everywhere, the model erodes bare rock.  See
  ``urh_cp_factors.csv``'s own ``note`` column - it is loaded, not paraphrased.
* ``LS2D``: the default column is ``ls2d_hs``, the hillslope-limited variant (upslope area
  capped at a 1 km2 channel-initiation threshold).  ``scripts/c3/ls2d.py`` states in its own
  docstring that this is "the column MUSLE should use": the uncapped ``ls2d`` lets channel
  cells carry the entire upstream catchment into a *hillslope* equation, which is a
  domain-of-validity failure (area-weighted mean 104.9 uncapped vs 39.8 capped).  Measured
  through this engine: the uncapped column multiplies basin-total erosion by **2.225x** at a
  uniform ``Qsur``, so this is not a cosmetic choice.
* ``FG`` = 1.0, explicitly, because no coarse-fragment / rock-fragment layer exists for the
  basin (IGAC gives texture classes, not stone content).  ``FG <= 1`` always, so omitting it
  RAISES the simulated load - it is the only term found so far that points against the
  lower-bound direction of docs/35 §5.3, and docs/35 §8 item 3 requires it be said out loud
  rather than left silent.  It is a parameter, not a hardcoded 1.
* AREA CROSS-CHECK, recorded because it is a >2x disagreement on some cells: URH areas from
  ``urh_fractions.csv`` x ``minibacias.csv`` (used here) and from ``urh_ls2d.csv:area_km2``
  (the LS2D raster's own cell count) agree at the median (ratio 1.0021) but differ by >5 % on
  12.9 % of cells, up to 6.6x, and the LS2D raster totals 2.09 % less basin area (251,724 vs
  257,097 km2 - DEM nodata).  This module takes area from ``urh_fractions``, i.e. the same
  area the frozen water balance and ``h2e_drivers.npz:own_area_km2`` use, and treats
  ``ls2d_hs`` as an intensive per-cell mean.  :func:`load_geometry` re-measures the
  disagreement and warns; it does not silently pick the smaller number.

BIAS THIS MODULE INHERITS (measured, docs/33 §7 and docs/35 §5 - do not re-derive)
---------------------------------------------------------------------------------
The peak deficit is STRUCTURAL (docs/33 §8: the H2E-S refit that fixed peaks was rejected
on 2 of 3 pre-registered conditions).  Fleet-median ``R_AMS`` 0.820 (El Nino 0.686),
``R_POT`` 0.567 - the model produces 1,285 independent peaks-over-threshold against 2,236
observed, i.e. ~43 % of flood events are missing.  Through ``beta``, the magnitude channel
alone puts simulated flood-driven sediment at least 10.5 % low fleet-wide and 19.0 % low in
El Nino; with the missing events the bracket is -10 % to -45 %; adding the ``q_peak`` proxy's
own sub-daily assumption the total suppression is ~2.1x (bracket 1.4-4.8), and that last term
is method-consistent with Buarque/Fagundes and must be reported separately, never merged.
**Simulated sediment from this module is a LOWER BOUND**, and the simulated
La Nina : El Nino contrast is overstated by ~+10 % because the dry phase is suppressed
harder.  Nothing in this module corrects any of that.

REJECTED ALTERNATIVES
---------------------
* **Rejected - deriving ``q_peak`` from a unit hydrograph** (SCS triangular, docs/35 §3(ii)):
  needs a rainfall-excess duration ``D``, which does not exist in a model with no sub-daily
  rainfall, and a basin-wide slope field, which does not exist at all (the only processed DEM
  covers 17.4 % of minibacias and they are the flat ones).  Implemented in
  ``scripts/c3/qpeak.py`` as a sensitivity generator only.  Choosing it would be a tuned
  decision dressed as a physical one.
* **Rejected - applying MUSLE lumped at the minibacia (or URH) scale.**  It is cheaper and it
  is what a naive port does, but MUSLE is scale-dependent: lumping inflates the load by
  ``N**(2*beta-1)``, 2.63x at the median minibacia, and it silently invalidates the
  pre-registered ``alpha`` band (docs/35 §6.2 - the hard stop would point the wrong way).
  The pixel-scale form is one extra multiplication.  If C4 ever needs the lumped form, use
  ``qpeak.rescale_alpha_reference`` and say so in the same table as ``alpha``.
* **Rejected - a per-URH sediment delivery ratio (SDR) or a Renard-style routing factor.**
  Any SDR is another free multiplicative parameter sitting upstream of ``alpha``, i.e. a
  second knob for the same degree of freedom, and nothing measured in this project can
  identify it separately from ``alpha``.  Delivery is one named linear reservoir (above) and
  the channel step is C4.
* **Rejected - making ``K`` per URH by soil family.**  ``K`` in
  ``minibacia_soil_params.csv`` is already texture-derived per minibacia; splitting it by the
  URH's soil-family digit would re-derive the same texture information from the URH code and
  could disagree with the file.  One source of truth per factor.
* **Rejected - clipping or smoothing extreme cells** (the eight highest-``C`` minibacias are
  bare rock/ice above the treeline).  A clip would hide a known input problem inside the
  engine.  The engine reports where its load concentrates; the fix, if any, belongs in
  ``urh_cp_factors.csv`` with a written reason.
* **Rejected - defaulting ``qsur_field`` to ``qsur_gen_mm``** even though Buarque's eq. 7 uses
  generated runoff: docs/35 §1 registers ``qsur_rel_mm`` as ``Qsur``, and the registration
  predates this module.  Switching the default after the fact is exactly the ordering
  violation docs/35 exists to prevent.  Both fields are available and the difference is
  measured (~1.6x), not hidden.

PERFORMANCE
-----------
Loops over TIME ONLY, like ``mgb_hydrology.py``.  Full basin-decade (3,652 days x 8,672
minibacias, 32,782 URH cells), measured 2026-08-11: ``collapsed`` 1.3 s without the daily
output array and 1.5 s with it (126 MB, float32), ``cells`` 2.0 s.  Peak memory is dominated
by the inputs, not the loop: the ``Qsur`` field alone is 121 MB.
"""

from __future__ import annotations

import importlib.util
import math
import pathlib
import sys
import time
import warnings
from dataclasses import dataclass, field
from typing import Optional, Sequence

import numpy as np

__all__ = [
    "DT_DAYS",
    "COP90_PIXEL_AREA_KM2",
    "WILLIAMS_ALPHA",
    "WILLIAMS_BETA",
    "WILLIAMS_M3_PER_MM_KM2",
    "VOLUME_CONVENTIONS",
    "QSUR_FIELDS",
    "LAND_CLASS_NAMES",
    "SedGeometry",
    "SedParams",
    "SedState",
    "SedDrivers",
    "SedResult",
    "qpeak_daily_mean",
    "musle_load_tonnes",
    "build_geometry",
    "load_geometry",
    "load_drivers",
    "cell_static_factor",
    "mini_static_factor",
    "runoff_energy_term",
    "erode_day",
    "simulate_sediment",
    "check_musle_parameters",
]

DT_DAYS = 1.0


# ---------------------------------------------------------------------------
# the registered q_peak proxy, imported (never re-derived)
# ---------------------------------------------------------------------------


def _import_qpeak():
    """Import ``scripts/c3/qpeak.py`` by path.

    It lives in ``scripts/c3/`` and not ``src/`` on purpose (docs/35 §7): Phase B's engine
    directory is frozen and C3 code must not be mistakable for part of it.  ``src/`` is not
    a package, so a relative import is impossible; loading by path keeps the registered
    proxy a single source of truth instead of copying its constants in here, which is how
    a "registered" number quietly drifts.
    """
    if "qpeak" in sys.modules:
        return sys.modules["qpeak"]
    path = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "c3" / "qpeak.py"
    if not path.is_file():
        raise ImportError(
            f"the registered q_peak proxy is missing: {path}. It is pre-registered in "
            "docs/35 §4 and must not be re-implemented here."
        )
    spec = importlib.util.spec_from_file_location("qpeak", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["qpeak"] = module
    spec.loader.exec_module(module)
    return module


_QP = _import_qpeak()

#: The registered MUSLE application scale, 0.0081 km2 (docs/35 §4).  Re-exported, not copied.
COP90_PIXEL_AREA_KM2 = _QP.COP90_PIXEL_AREA_KM2
WILLIAMS_ALPHA = _QP.WILLIAMS_ALPHA        # 11.8  - starting value, NOT a fitted value
WILLIAMS_BETA = _QP.WILLIAMS_BETA          # 0.56  - starting value, NOT a fitted value
qpeak_daily_mean = _QP.qpeak_daily_mean
check_musle_parameters = _QP.check_musle_parameters

#: 1 mm of depth over 1 km2 is 1000 m3 - the whole difference between the two unit
#: conventions of the module docstring (``williams_m3`` = ``pixel_km2`` x 1000).
WILLIAMS_M3_PER_MM_KM2 = 1000.0

#: 1 km2 = 100 ha.  SWAT's standard MUSLE form carries the area in HECTARES
#: (``Q_surf[mm] * q_peak[m3/s] * area[ha]``), which is the form ``alpha`` = 11.8 is normally
#: quoted with, and the form ``method_research.md`` §1.1 says both source texts label
#: (see the module docstring's UNITS section).  ``swat_mm_ha`` = ``pixel_km2`` x 100.
SWAT_HA_PER_KM2 = 100.0

#: The product multiplier for each convention, in ascending order of magnitude.
VOLUME_FACTORS = {
    "pixel_km2": 1.0,
    "swat_mm_ha": SWAT_HA_PER_KM2,
    "williams_m3": WILLIAMS_M3_PER_MM_KM2,
}
VOLUME_CONVENTIONS = tuple(VOLUME_FACTORS)
#: Frozen-driver fields that can play ``Qsur``.  ``qsur_rel_mm`` is the registered one.
QSUR_FIELDS = ("qsur_rel_mm", "qsur_gen_mm")

#: URH id = soil_family*10 + land_class (nb08 step 4); the land digit indexes C/P.
LAND_CLASS_NAMES = {
    1: "Forest", 2: "Shrub", 3: "Grassland", 4: "Cropland",
    5: "Urban", 6: "Bare", 7: "Water", 8: "Wetland",
}


def _finite_nonneg(name: str, arr: np.ndarray, *, positive: bool = False) -> np.ndarray:
    """Reject NaN/inf/negative (or non-positive) inputs loudly instead of coercing them."""
    a = np.asarray(arr, dtype=np.float64)
    if not np.all(np.isfinite(a)):
        n = int((~np.isfinite(a)).sum())
        raise ValueError(f"{name} has {n} non-finite entries")
    if positive:
        if np.any(a <= 0.0):
            raise ValueError(f"{name} must be > 0; min is {float(a.min())!r}")
    elif np.any(a < 0.0):
        raise ValueError(f"{name} must be >= 0; min is {float(a.min())!r}")
    return a


# ---------------------------------------------------------------------------
# the MUSLE primitive
# ---------------------------------------------------------------------------


def musle_load_tonnes(
    qsur_mm,
    qpeak_m3s,
    area_km2,
    k_usle,
    c_usle,
    p_usle,
    ls2d,
    *,
    alpha: float = WILLIAMS_ALPHA,
    beta: float = WILLIAMS_BETA,
    fg: float = 1.0,
    volume_factor: float = 1.0,
    validate: bool = True,
):
    """MUSLE soil loss for ONE application unit and one day, in tonnes.

    ``Sed = alpha * (Qsur * q_peak * A * volume_factor)^beta * K * C * P * LS2D * FG``

    This is the primitive every other function in the module goes through, and it takes
    ``q_peak`` **explicitly** rather than deriving it: the registered proxy makes ``q_peak``
    a function of ``Qsur`` (docs/35 §4), so a function that derived it internally could not
    be tested for monotonicity in ``q_peak`` alone.  Keeping the argument separate is what
    lets ``tests/test_sediment.py`` vary each of the seven factors independently.

    ``volume_factor`` is the unit convention of the module docstring: 1.0 for the registered
    ``pixel_km2`` form, :data:`SWAT_HA_PER_KM2` for SWAT's hectare form,
    :data:`WILLIAMS_M3_PER_MM_KM2` for the Williams-m3 form (see :data:`VOLUME_FACTORS`).
    It is a documented convention, not a calibration knob - see the docstring's UNITS
    section.

    All arguments broadcast.  Exact zero anywhere in the first three factors gives exactly
    0.0 tonnes (``0.0**beta`` is exactly 0.0 for ``beta`` > 0), so a dry day erodes nothing
    to the last bit rather than to within a tolerance.
    """
    if validate:
        qsur = _finite_nonneg("qsur_mm", qsur_mm)
        qpeak = _finite_nonneg("qpeak_m3s", qpeak_m3s)
        area = _finite_nonneg("area_km2", area_km2)
        k = _finite_nonneg("k_usle", k_usle)
        c = _finite_nonneg("c_usle", c_usle)
        p = _finite_nonneg("p_usle", p_usle)
        ls = _finite_nonneg("ls2d", ls2d)
        if not np.all(np.isfinite([alpha, beta, fg, volume_factor])):
            raise ValueError("alpha, beta, fg, volume_factor must be finite")
        if alpha < 0.0 or beta <= 0.0 or fg < 0.0 or volume_factor <= 0.0:
            raise ValueError(
                "need alpha >= 0, beta > 0 (beta <= 0 would make a dry day erode "
                "infinitely), fg >= 0, volume_factor > 0"
            )
    else:
        qsur, qpeak, area = qsur_mm, qpeak_m3s, area_km2
        k, c, p, ls = k_usle, c_usle, p_usle, ls2d
    product = qsur * qpeak * area * volume_factor
    return alpha * product ** beta * k * c * p * ls * fg


# ---------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SedGeometry:
    """Immutable static erosion geometry: one row per active (minibacia, URH) cell.

    Built once and reused for every parameter set, exactly like ``MgbTopology``: a C4
    calibration re-run must not re-read four CSVs per evaluation.  Nothing here depends on
    ``alpha``, ``beta``, ``FG`` or the pixel scale - those live in :class:`SedParams`.
    """

    mini_ids: np.ndarray         # (n,) int64   minibacia ids, in driver order
    mini_area_km2: np.ndarray    # (n,) float64 own area (== h2e_drivers own_area_km2)
    cell_mini: np.ndarray        # (N,) int64   internal minibacia index per cell
    cell_urh_code: np.ndarray    # (N,) int64   URH code 11..38
    cell_area_km2: np.ndarray    # (N,) float64
    cell_k: np.ndarray           # (N,) float64 erodibility (per minibacia, broadcast)
    cell_c: np.ndarray           # (N,) float64 cover factor (per land class)
    cell_p: np.ndarray           # (N,) float64 practice factor (1.0 basin-wide)
    cell_ls2d: np.ndarray        # (N,) float64
    ls2d_column: str = "ls2d_hs"
    area_source: str = "urh_fractions"
    audit: dict = field(default_factory=dict, repr=False)

    @property
    def n_mini(self) -> int:
        return int(self.mini_ids.size)

    @property
    def n_cells(self) -> int:
        return int(self.cell_mini.size)

    @property
    def covered_area_km2(self) -> float:
        """Area MUSLE is actually applied to = sum of cell areas."""
        return float(self.cell_area_km2.sum())

    def cell_land_class(self) -> np.ndarray:
        """Land digit of each cell's URH code (1 Forest .. 8 Wetland)."""
        return self.cell_urh_code % 10

    def index_of(self, ids: Sequence[int]) -> np.ndarray:
        """Internal indices of the given minibacia ids (raises on an unknown id)."""
        want = np.asarray(ids, dtype=np.int64)
        srt = np.argsort(self.mini_ids, kind="stable")
        sorted_ids = self.mini_ids[srt]
        loc = np.clip(np.searchsorted(sorted_ids, want), 0, sorted_ids.size - 1)
        ok = sorted_ids[loc] == want
        if not ok.all():
            raise KeyError(f"unknown minibacia ids: {want[~ok][:10].tolist()}")
        return srt[loc].astype(np.int64)


def build_geometry(
    mini_ids,
    mini_area_km2,
    cell_mini,
    cell_urh_code,
    cell_area_km2,
    mini_k,
    class_c,
    class_p,
    cell_ls2d,
    *,
    ls2d_column: str = "ls2d_hs",
    area_source: str = "urh_fractions",
    audit: Optional[dict] = None,
) -> SedGeometry:
    """Validate and pack the static factors.  ``class_c`` / ``class_p`` are dicts keyed 1..8.

    Every input is range-checked here rather than at use time, because a negative ``K`` or a
    NaN ``LS2D`` would otherwise surface 3,652 days later as a NaN in the output and cost a
    bisection to find.
    """
    ids = np.asarray(mini_ids, dtype=np.int64)
    n = ids.size
    if np.unique(ids).size != n:
        raise ValueError("duplicate minibacia ids")
    area_mini = _finite_nonneg("mini_area_km2", mini_area_km2, positive=True)
    if area_mini.shape != (n,):
        raise ValueError(f"mini_area_km2 must be ({n},), got {area_mini.shape}")
    cm = np.asarray(cell_mini, dtype=np.int64)
    cu = np.asarray(cell_urh_code, dtype=np.int64)
    ca = _finite_nonneg("cell_area_km2", cell_area_km2, positive=True)
    ls = _finite_nonneg("cell_ls2d", cell_ls2d, positive=True)
    if not (cm.shape == cu.shape == ca.shape == ls.shape) or cm.ndim != 1:
        raise ValueError("cell_* arrays must be 1-D and the same length")
    if cm.size and (cm.min() < 0 or cm.max() >= n):
        raise ValueError("cell_mini out of range for the given minibacia ids")
    k_mini = _finite_nonneg("mini_k", mini_k, positive=True)
    if k_mini.shape != (n,):
        raise ValueError(f"mini_k must be ({n},), got {k_mini.shape}")

    land = cu % 10
    unknown = sorted(set(land.tolist()) - set(class_c))
    if unknown:
        raise ValueError(f"no C factor for land class(es) {unknown}")
    unknown = sorted(set(land.tolist()) - set(class_p))
    if unknown:
        raise ValueError(f"no P factor for land class(es) {unknown}")
    c = _finite_nonneg("class_c", np.array([class_c[int(x)] for x in land]))
    p = _finite_nonneg("class_p", np.array([class_p[int(x)] for x in land]))
    return SedGeometry(
        mini_ids=ids,
        mini_area_km2=area_mini,
        cell_mini=cm,
        cell_urh_code=cu,
        cell_area_km2=ca,
        cell_k=k_mini[cm],
        cell_c=c,
        cell_p=p,
        cell_ls2d=ls,
        ls2d_column=str(ls2d_column),
        area_source=str(area_source),
        audit=dict(audit or {}),
    )


def load_geometry(
    processed_dir="data/processed",
    *,
    minibacias: str = "minibacias.csv",
    urh_fractions: str = "urh_fractions.csv",
    soil_params: str = "minibacia_soil_params.csv",
    cp_factors: str = "urh_cp_factors.csv",
    urh_ls2d: str = "urh_ls2d.csv",
    ls2d_column: str = "ls2d_hs",
    mini_ids: Optional[Sequence[int]] = None,
    area_tol_frac: float = 0.05,
) -> SedGeometry:
    """Assemble :class:`SedGeometry` from the four project CSVs.

    ``mini_ids`` orders the output (pass ``h2e_drivers.npz:minibacia_id`` so the geometry and
    the drivers share one column order - a mismatch there is a silent spatial scramble).

    ``ls2d_column`` defaults to ``ls2d_hs``, the hillslope-limited LS2D, because that is the
    column ``scripts/c3/ls2d.py`` states MUSLE should use; ``ls2d`` (uncapped) is available
    but lets channel cells carry the whole upstream catchment into a hillslope equation.

    Cell areas come from ``urh_fractions`` x ``minibacias``, NOT from ``urh_ls2d:area_km2``.
    The two disagree (see the module docstring); this function re-measures the disagreement
    on the spot and warns above ``area_tol_frac`` so the choice cannot rot silently.
    """
    import pandas as pd

    d = pathlib.Path(processed_dir)
    mb = pd.read_csv(d / minibacias)
    uf = pd.read_csv(d / urh_fractions)
    sp = pd.read_csv(d / soil_params)
    cp = pd.read_csv(d / cp_factors)
    ul = pd.read_csv(d / urh_ls2d)

    for name, df, cols in (
        (minibacias, mb, ("id", "area_km2")),
        (urh_fractions, uf, ("mini",)),
        (soil_params, sp, ("id", "K")),
        (cp_factors, cp, ("class_id", "C", "P")),
        (urh_ls2d, ul, ("mini", "urh", "area_km2", ls2d_column)),
    ):
        missing = [c for c in cols if c not in df.columns]
        if missing:
            raise ValueError(f"{name} is missing column(s) {missing}")

    ids = mb.id.to_numpy(dtype=np.int64) if mini_ids is None else np.asarray(mini_ids, np.int64)
    mb = mb.set_index("id")
    unknown = set(ids.tolist()) - set(mb.index)
    if unknown:
        raise ValueError(f"{len(unknown)} requested minibacia ids are absent from "
                         f"{minibacias}, e.g. {sorted(unknown)[:5]}")
    area_mini = mb.loc[ids, "area_km2"].to_numpy(dtype=np.float64)

    codes = [c for c in uf.columns if c != "mini"]
    uf = uf.set_index("mini")
    missing_rows = set(ids.tolist()) - set(uf.index)
    if missing_rows:
        raise ValueError(f"{urh_fractions} has no row for {len(missing_rows)} minibacias, "
                         f"e.g. {sorted(missing_rows)[:5]}")
    frac = uf.loc[ids, codes].to_numpy(dtype=np.float64)
    if np.any(frac < 0) or not np.all(np.isfinite(frac)):
        raise ValueError(f"{urh_fractions} has negative or non-finite fractions")
    mi, ci = np.nonzero(frac > 0.0)
    cell_mini = mi.astype(np.int64)
    cell_code = np.asarray([int(codes[j]) for j in ci], dtype=np.int64)
    cell_area = frac[mi, ci] * area_mini[mi]

    sp = sp.set_index("id")
    missing_rows = set(ids.tolist()) - set(sp.index)
    if missing_rows:
        raise ValueError(f"{soil_params} has no row for {len(missing_rows)} minibacias")
    k_mini = sp.loc[ids, "K"].to_numpy(dtype=np.float64)

    cp = cp.set_index("class_id")
    class_c = {int(i): float(v) for i, v in cp["C"].items()}
    class_p = {int(i): float(v) for i, v in cp["P"].items()}

    ul_idx = ul.set_index(["mini", "urh"])
    want = list(zip(ids[cell_mini].tolist(), cell_code.tolist()))
    missing_cells = [key for key in want if key not in ul_idx.index]
    if missing_cells:
        raise ValueError(
            f"{urh_ls2d} has no LS2D for {len(missing_cells)} active (minibacia, URH) cells, "
            f"e.g. {missing_cells[:5]}. A missing LS2D must not become an implicit 0 - that "
            "would silently switch erosion off for those cells."
        )
    sub = ul_idx.loc[want]
    cell_ls2d = sub[ls2d_column].to_numpy(dtype=np.float64)
    ls_area = sub["area_km2"].to_numpy(dtype=np.float64)

    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(ls_area > 0, cell_area / ls_area, np.nan)
    frac_off = float(np.mean(np.abs(ratio - 1.0) > area_tol_frac))
    audit = {
        "n_cells": int(cell_mini.size),
        "area_ratio_median": float(np.nanmedian(ratio)),
        "area_ratio_p99": float(np.nanpercentile(ratio, 99)),
        "area_ratio_max": float(np.nanmax(ratio)),
        "frac_cells_area_off": frac_off,
        "area_total_urh_fractions_km2": float(cell_area.sum()),
        "area_total_urh_ls2d_km2": float(ls_area.sum()),
        "ls2d_column": ls2d_column,
    }
    if frac_off > 0.0:
        warnings.warn(
            f"URH cell areas from {urh_fractions} x {minibacias} and from "
            f"{urh_ls2d}:area_km2 differ by more than {area_tol_frac:.0%} on "
            f"{frac_off:.1%} of cells (median ratio {audit['area_ratio_median']:.4f}, max "
            f"{audit['area_ratio_max']:.2f}; basin totals "
            f"{audit['area_total_urh_fractions_km2']:.0f} vs "
            f"{audit['area_total_urh_ls2d_km2']:.0f} km2). This module uses the "
            f"{urh_fractions} area, i.e. the same area the frozen water balance used, and "
            "treats LS2D as an intensive per-cell mean.",
            stacklevel=2,
        )
    return build_geometry(
        ids, area_mini, cell_mini, cell_code, cell_area, k_mini,
        class_c, class_p, cell_ls2d,
        ls2d_column=ls2d_column, area_source=urh_fractions, audit=audit,
    )


# ---------------------------------------------------------------------------
# parameters
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SedParams:
    """Every tunable number, with the origin of its default stated.

    Frozen on purpose: a C4 search must construct a new instance per evaluation rather than
    mutate a shared one, so a half-updated parameter set cannot leak between evaluations.
    Nothing here is fitted.
    """

    #: MUSLE coefficient.  Williams (1975), adopted unchanged by Buarque (2015) eq. 5 with
    #: this same daily-mean q_peak.  A STARTING VALUE to be fitted in C4, not a tuned value;
    #: C4's registered band and hard stops are in ``qpeak.check_musle_parameters``.
    alpha: float = WILLIAMS_ALPHA
    #: MUSLE exponent.  Williams (1975).  STARTING VALUE; C4 hard stop outside [0.45, 0.65].
    beta: float = WILLIAMS_BETA
    #: Coarse-fragment factor.  EXPLICITLY 1.0: no rock-fragment layer exists for the basin
    #: (docs/35 §8 item 3).  FG <= 1 always, so 1.0 RAISES the load - the one term pointing
    #: against the docs/35 §5.3 lower-bound direction.  Stated, not silent.
    fg: float = 1.0
    #: MUSLE application area, km2.  The registered COP90 pixel (docs/35 §4).  Changing it
    #: invalidates the pre-registered alpha band unless the band is rescaled by
    #: ``qpeak.musle_scale_factor`` - see docs/35 §6.2.
    pixel_area_km2: float = COP90_PIXEL_AREA_KM2
    #: Delivery linear-reservoir residence time, days.  0.0 = pass-through, the default,
    #: because the registered Qsur (``qsur_rel_mm``) has ALREADY been through the engine's
    #: surface linear reservoir; a second one would double-count the lag (docs/35 §8 item 4).
    tau_delivery_days: float = 0.0
    #: Unit convention for the (Qsur * q_peak * A) product: 'pixel_km2' is the registered
    #: form (docs/35 §4); 'swat_mm_ha' is SWAT's standard hectare form (x100 product,
    #: 100**beta = 13.18x load) which is the form alpha = 11.8 is normally quoted with;
    #: 'williams_m3' is Williams' literal m3-volume form, exactly 1000**beta = 47.86x larger.
    #: The two non-default forms are for the C3.6 order-of-magnitude diagnostic ONLY.
    #: Switching the default is an amendment to docs/35 §9, not a code change.
    volume_convention: str = "pixel_km2"

    def __post_init__(self) -> None:
        if self.volume_convention not in VOLUME_CONVENTIONS:
            raise ValueError(f"volume_convention must be one of {VOLUME_CONVENTIONS}")
        for name in ("alpha", "beta", "fg", "pixel_area_km2", "tau_delivery_days"):
            v = float(getattr(self, name))
            if not math.isfinite(v):
                raise ValueError(f"{name} must be finite")
        if self.alpha < 0.0:
            raise ValueError("alpha must be >= 0")
        if self.beta <= 0.0:
            raise ValueError(
                "beta must be > 0: with beta <= 0 a zero-runoff day would erode infinitely"
            )
        if self.fg < 0.0 or self.fg > 1.0:
            raise ValueError("fg is a fraction of erodible surface and must lie in [0, 1]")
        if self.pixel_area_km2 <= 0.0:
            raise ValueError("pixel_area_km2 must be > 0")
        if self.tau_delivery_days < 0.0:
            raise ValueError("tau_delivery_days must be >= 0")

    @property
    def volume_factor(self) -> float:
        """Multiplier on the ``(Qsur * q_peak * A)`` product for the chosen convention."""
        return VOLUME_FACTORS[self.volume_convention]

    @property
    def delivery_release_coef(self) -> float:
        """Fraction of the sediment store delivered in one day.

        ``1 - exp(-dt/tau)``, the analytic one-day solution of ``dS/dt = -S/tau`` - the same
        form ``mgb_hydrology._release_coef`` uses for water, for the same reason (bounded in
        (0, 1] for every tau >= 0, so the store can never go negative).  ``tau = 0`` gives
        exactly 1.0, i.e. bitwise pass-through.
        """
        tau = float(self.tau_delivery_days)
        return 1.0 if tau == 0.0 else float(-math.expm1(-DT_DAYS / tau))

    def check(self, area_km2: Optional[float] = None) -> dict:
        """Apply the pre-registered docs/35 §6 anti-compensation rule to (alpha, beta).

        Thin wrapper over ``qpeak.check_musle_parameters`` so C4 cannot forget it exists.
        ``area_km2`` is only needed if MUSLE was applied lumped rather than at the
        registered pixel scale.
        """
        return check_musle_parameters(float(self.alpha), float(self.beta), area_km2=area_km2)


# ---------------------------------------------------------------------------
# static factor and the daily runoff-energy term
# ---------------------------------------------------------------------------


def cell_static_factor(geom: SedGeometry, params: SedParams) -> np.ndarray:
    """Per-cell part of MUSLE that does not depend on the day, ``(N,)``.

    ``(A_cell / a_p) * alpha * K * C * P * LS2D * FG`` - the pixel count times every static
    factor.  Multiply by :func:`runoff_energy_term` to get tonnes/day.
    """
    n_pix = geom.cell_area_km2 / float(params.pixel_area_km2)
    return (n_pix * float(params.alpha) * geom.cell_k * geom.cell_c * geom.cell_p
            * geom.cell_ls2d * float(params.fg))


def mini_static_factor(geom: SedGeometry, params: SedParams) -> np.ndarray:
    """:func:`cell_static_factor` summed to the minibacia, ``(n,)`` - the collapsed backend.

    Valid because the runoff-energy term is identical for every cell of a minibacia (the
    frozen drivers carry ``Qsur`` per minibacia and ``a_p`` is a constant), so the sum
    factorises exactly.  See the module docstring, WHY THE DAILY TERM FACTORISES.
    """
    return np.bincount(geom.cell_mini, weights=cell_static_factor(geom, params),
                       minlength=geom.n_mini)


def runoff_energy_term(qsur_mm, params: SedParams, *, validate: bool = True):
    """``(Qsur * q_peak * a_p * volume_factor)^beta`` at the registered pixel scale.

    ``q_peak`` comes from the registered proxy :func:`qpeak_daily_mean` evaluated on the
    pixel, i.e. ``Qsur * a_p / 86.4``; nothing here is free.  Exactly 0.0 where ``Qsur`` is
    0.0.
    """
    q = _finite_nonneg("qsur_mm", qsur_mm) if validate else qsur_mm
    a_p = float(params.pixel_area_km2)
    qpeak = q * a_p * _QP.MM_KM2_PER_DAY_TO_M3S
    return (q * qpeak * a_p * params.volume_factor) ** float(params.beta)


def erode_day(geom: SedGeometry, params: SedParams, qsur_mini_mm) -> np.ndarray:
    """Gross hillslope erosion for one day, per URH cell, in tonnes/day, ``(N,)``.

    ``qsur_mini_mm`` is ``(n_mini,)``: the minibacia's surface-runoff depth for the day.
    This is the reference path - it evaluates MUSLE cell by cell through
    :func:`musle_load_tonnes`, so what the tests check is what the run uses.
    """
    q = _finite_nonneg("qsur_mini_mm", qsur_mini_mm)
    if q.shape != (geom.n_mini,):
        raise ValueError(f"qsur_mini_mm must be ({geom.n_mini},), got {q.shape}")
    q_cell = q[geom.cell_mini]
    a_p = float(params.pixel_area_km2)
    qpeak_cell = qpeak_daily_mean(q_cell, a_p)
    per_pixel = musle_load_tonnes(
        q_cell, qpeak_cell, a_p,
        geom.cell_k, geom.cell_c, geom.cell_p, geom.cell_ls2d,
        alpha=float(params.alpha), beta=float(params.beta), fg=float(params.fg),
        volume_factor=params.volume_factor, validate=False,
    )
    return per_pixel * (geom.cell_area_km2 / a_p)


# ---------------------------------------------------------------------------
# state, drivers, result
# ---------------------------------------------------------------------------


@dataclass
class SedState:
    """Mutable state: tonnes held in each minibacia's delivery reservoir."""

    store_t: np.ndarray          # (n,) tonnes

    @classmethod
    def initial(cls, geom: SedGeometry) -> "SedState":
        """Cold start with an empty store.

        Unlike the water balance there is nothing to warm up: the store's only input is the
        day's erosion and, at the default ``tau`` = 0, it is empty at the end of every day.
        A non-zero ``tau`` fills it within a few ``tau``, which is why C4's spin-up note
        (docs/31 §C4.2) is about antecedent CHANNEL state, not about this store.
        """
        return cls(store_t=np.zeros(geom.n_mini, dtype=np.float64))

    def copy(self) -> "SedState":
        return SedState(store_t=self.store_t.copy())

    def stored_tonnes(self) -> float:
        return float(math.fsum(self.store_t.tolist()))


@dataclass(frozen=True)
class SedDrivers:
    """The frozen hydrology this module consumes, and nothing else."""

    qsur_mm: np.ndarray          # (ndays, n_mini) float32, mm/day
    dates: np.ndarray            # (ndays,) datetime64[D]
    mini_ids: np.ndarray         # (n_mini,) int64
    own_area_km2: np.ndarray     # (n_mini,) float64
    qsur_field: str
    meta: dict = field(default_factory=dict, repr=False)

    @property
    def ndays(self) -> int:
        return int(self.qsur_mm.shape[0])


def load_drivers(
    path="data/processed/sim_calibrated_v2/h2e_drivers.npz",
    *,
    qsur_field: str = "qsur_rel_mm",
) -> SedDrivers:
    """Read ``Qsur`` (and geometry keys) out of the frozen H2E driver bundle, read-only.

    ``qsur_field`` defaults to the REGISTERED ``qsur_rel_mm`` (docs/35 §1).  ``qsur_gen_mm``
    (runoff generated on the URH columns, before the surface reservoir) is the field
    Buarque's eq. 7 uses and is available for the comparison the module docstring quantifies
    - but it is not the default, because the registration predates this module.

    Only the one requested field is materialised: each is 3652 x 8672 float32 = 121 MB and
    the file holds five of them.
    """
    if qsur_field not in QSUR_FIELDS:
        raise ValueError(f"qsur_field must be one of {QSUR_FIELDS}")
    p = pathlib.Path(path)
    if not p.is_file():
        raise FileNotFoundError(
            f"{p} not found. It is the frozen H2E driver bundle (546 MB, gitignored); "
            "rebuild it with src/build_h2e_drivers.py - do NOT re-run the hydrology by hand."
        )
    import json

    with np.load(p, allow_pickle=False) as z:
        if qsur_field not in z.files:
            raise KeyError(f"{p} has no field '{qsur_field}'; it holds {sorted(z.files)}")
        qsur = z[qsur_field]
        dates = z["dates"]
        ids = z["minibacia_id"].astype(np.int64)
        own_area = z["own_area_km2"].astype(np.float64)
        meta_raw = str(z["meta"][0]) if "meta" in z.files else "{}"
    try:
        meta = json.loads(meta_raw)
    except ValueError:
        meta = {"raw": meta_raw}
    if qsur.ndim != 2 or qsur.shape[1] != ids.size or qsur.shape[0] != dates.size:
        raise ValueError(
            f"{qsur_field} is {qsur.shape} but dates is {dates.shape} and minibacia_id is "
            f"{ids.shape} - the driver bundle is inconsistent; do not proceed"
        )
    return SedDrivers(qsur_mm=qsur, dates=dates, mini_ids=ids, own_area_km2=own_area,
                      qsur_field=qsur_field, meta=meta)


@dataclass
class SedResult:
    """Delivered load plus everything needed to audit the run."""

    dates: Optional[np.ndarray]
    record_ids: np.ndarray             # (m,) minibacia ids of the recorded columns
    delivered_t_day: Optional[np.ndarray]   # (ndays_rec, m) tonnes/day, or None
    series: dict                       # basin-total daily series, tonnes/day
    cell_eroded_t: np.ndarray          # (N,) period-total gross erosion per URH cell
    ledger: dict
    state: SedState
    params: SedParams
    backend: str
    wall_time_s: float

    def load_at(self, mini_id: int) -> np.ndarray:
        if self.delivered_t_day is None:
            raise ValueError("this run was made with store_daily=False")
        j = int(np.flatnonzero(self.record_ids == int(mini_id))[0])
        return self.delivered_t_day[:, j]

    def eroded_by_land_class(self, geom: SedGeometry) -> dict:
        """Period-total gross erosion (tonnes) grouped by land class - attribution, not yield."""
        land = geom.cell_land_class()
        return {LAND_CLASS_NAMES[int(k)]: float(self.cell_eroded_t[land == k].sum())
                for k in np.unique(land)}


# ---------------------------------------------------------------------------
# the driver loop
# ---------------------------------------------------------------------------


def _assemble_ledger(eroded_daily, delivered_daily, store_start: float,
                     store_end: float) -> dict:
    """Close the sediment budget: ``eroded = delivered + (store_end - store_start)``.

    Totals are summed with :func:`math.fsum` so the ACCOUNTING contributes no error of its
    own; whatever residual remains is the per-day float rounding of the reservoir update,
    and at the default ``tau`` = 0 it is exactly 0.0 because ``delivered`` is bitwise
    ``eroded``.  ``exact`` records which of those two situations the run was in, instead of
    letting a tolerance hide the difference.
    """
    eroded = math.fsum(eroded_daily)
    delivered = math.fsum(delivered_daily)
    residual = eroded - delivered - (store_end - store_start)
    scale = max(abs(eroded), 1.0)
    return {
        "eroded_t": eroded,
        "delivered_t": delivered,
        "store_start_t": store_start,
        "store_end_t": store_end,
        "residual_t": residual,
        "residual_relative": abs(residual) / scale,
        "exact": residual == 0.0,
        "ndays": len(eroded_daily),
    }


def simulate_sediment(
    geom: SedGeometry,
    params: SedParams,
    qsur_mm: np.ndarray,
    *,
    dates: Optional[Sequence] = None,
    record_ids: Optional[Sequence[int]] = None,
    state: Optional[SedState] = None,
    backend: str = "auto",
    store_daily: bool = True,
    dtype_out: type = np.float32,
) -> SedResult:
    """Run the hillslope-erosion model over ``qsur_mm`` ``(ndays, n_mini)``, mm/day.

    Parameters
    ----------
    qsur_mm
        Surface-runoff depth per minibacia-day, columns ordered like ``geom.mini_ids``.
        Get it from :func:`load_drivers`; NEVER from the wide forcing CSVs (pandas returns a
        silent truncated prefix on those - see ``src/forcing_npy.py``).
    record_ids
        Minibacia ids to write out; ``None`` records all (float32, 126 MB for the full
        basin-decade).  ``store_daily=False`` skips the array entirely and keeps only the
        basin series, the per-cell period totals and the ledger.
    backend
        ``'cells'`` = evaluate MUSLE on all 32,782 cells daily (reference);
        ``'collapsed'`` = pre-summed static factor, one multiply per minibacia-day - the
        same identity computed a different way, only 1.5x faster, kept as an independent
        second implementation; ``'auto'`` = collapsed.  ``tests/test_sediment.py`` asserts
        the two agree to 1e-12 relative on the synthetic case and on a real year.

    Returns
    -------
    SedResult
        ``delivered_t_day`` is the hillslope load delivered to each reach, in TONNES/DAY.
        It is a lower bound (module docstring, BIAS THIS MODULE INHERITS) and it is not a
        yield: nothing is divided by an area anywhere.
    """
    if backend == "auto":
        backend = "collapsed"
    if backend not in ("cells", "collapsed"):
        raise ValueError("backend must be 'cells', 'collapsed' or 'auto'")
    t0 = time.perf_counter()
    n = geom.n_mini
    q = np.asarray(qsur_mm)
    if q.ndim != 2 or q.shape[1] != n:
        raise ValueError(f"qsur_mm must be (ndays, {n}), got {q.shape}")
    ndays = int(q.shape[0])
    if dates is not None and len(dates) != ndays:
        raise ValueError(
            f"dates has {len(dates)} entries but qsur_mm has {ndays} days - a mismatch "
            "here silently mislabels the output time axis"
        )
    # One full-array screen up front: a NaN or a negative Qsur anywhere would otherwise
    # propagate into the load as a NaN and be found only by bisection.
    if not np.all(np.isfinite(q)):
        raise ValueError(f"qsur_mm has {int((~np.isfinite(q)).sum())} non-finite entries")
    if np.any(q < 0.0):
        raise ValueError("qsur_mm has negative entries - surface runoff cannot be negative")

    if record_ids is None:
        rec_idx = np.arange(n, dtype=np.int64)
        rec_ids = geom.mini_ids.copy()
    else:
        rec_idx = geom.index_of(record_ids)
        rec_ids = geom.mini_ids[rec_idx]
    out = (np.empty((ndays, rec_idx.size), dtype=dtype_out) if store_daily else None)

    st = SedState.initial(geom) if state is None else state.copy()
    if st.store_t.shape != (n,):
        raise ValueError("state does not match geometry")
    store_start = st.stored_tonnes()
    coef = params.delivery_release_coef

    static_cell = cell_static_factor(geom, params)
    static_mini = mini_static_factor(geom, params)
    cell_mini = geom.cell_mini
    ser = {k: np.zeros(ndays) for k in ("eroded", "delivered", "store_end")}
    eroded_daily = ser["eroded"]
    delivered_daily = ser["delivered"]
    cell_acc = np.zeros(geom.n_cells)
    term_sum_mini = np.zeros(n)

    for t in range(ndays):
        q_day = q[t].astype(np.float64, copy=False)
        term = runoff_energy_term(q_day, params, validate=False)
        if backend == "cells":
            cell_day = static_cell * term[cell_mini]
            cell_acc += cell_day
            eroded = np.bincount(cell_mini, weights=cell_day, minlength=n)
        else:
            term_sum_mini += term
            eroded = static_mini * term
        # delivery reservoir: a structural partition of the store, so no tonne is created
        # or dropped.  coef == 1.0 (tau = 0) makes this bitwise pass-through.
        s = st.store_t + eroded
        delivered = s * coef
        st.store_t = s - delivered
        eroded_daily[t] = eroded.sum()
        delivered_daily[t] = delivered.sum()
        ser["store_end"][t] = st.store_t.sum()
        if out is not None:
            out[t] = delivered[rec_idx]

    if backend != "cells":
        cell_acc = static_cell * term_sum_mini[cell_mini]
    ledger = _assemble_ledger(eroded_daily.tolist(), delivered_daily.tolist(),
                              store_start, st.stored_tonnes())
    return SedResult(
        dates=None if dates is None else np.asarray(dates),
        record_ids=rec_ids,
        delivered_t_day=out,
        series=ser,
        cell_eroded_t=cell_acc,
        ledger=ledger,
        state=st,
        params=params,
        backend=backend,
        wall_time_s=time.perf_counter() - t0,
    )
