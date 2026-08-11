"""MUSLE peak-runoff-rate (``q_peak``) proxy for a daily model.

**Read ``docs/35_qpeak_preregistration.md`` before changing anything in this file.**
The choice implemented here, its quantified bias, and the rule that forbids C4 from
absorbing that bias into ``alpha``/``beta`` were all registered in docs/35 *before* this
module was written and *before* any sediment parameter was fitted. That ordering is the
point of the module; do not invert it by tuning the proxy to make a later fit look better.

THE REGISTERED CHOICE (docs/35 §4)
----------------------------------
``q_peak = Qsur[mm/d] * a[km2] / 86.4``  (m3/s) -- the daily-mean surface-runoff rate.

This is Buarque (2015, UFRGS, advisor Collischonn) eq. 7, the MGB-SED formulation that
Fagundes et al.'s sediment module inherits: *"the peak rate of surface runoff in each
pixel k is obtained considering a runoff volume uniform through the day."*  It is applied
per DEM pixel (``COP90_PIXEL_AREA_KM2``), which is what keeps a fitted ``alpha``
comparable to Williams' 11.8 with no scale correction (docs/35 §6.2).

THE BIAS IT CARRIES (docs/35 §5) -- all in the same direction, so they compound
------------------------------------------------------------------------------
1. The proxy itself: the true instantaneous peak always exceeds the daily mean, so
   simulated flood-driven sediment is a strict LOWER BOUND given ``Qsur``. Magnitude
   1.26x-2.75x (central ~1.86x at T_p = 6 h), i.e. -21 % to -64 %. This term is
   method-consistent with Buarque/Fagundes -- report it, never correct it into alpha.
2. The measured peak deficit it sits on top of (docs/33 §7.3-§7.5, C2b): fleet-median
   ``R_AMS`` = 0.820 -> ``R^0.56`` = 0.895, i.e. sediment low by at least 10.5 %;
   El Nino 2015-16 ``R_AMS`` = 0.686 -> low by 19.0 %.
3. Missing events: ``R_POT`` = 0.567 -- 1,285 simulated independent peaks-over-threshold
   against 2,236 observed, ~43 % of flood events absent. ``R_POT`` is a COUNT: do NOT
   raise it to ``beta``. The load deficit from this channel is a bracket, 0 % to -42.5 %.
4. Direction on the headline result: the dry phase is suppressed harder than the wet
   phase (0.686 vs 0.808), so a SIMULATED La Nina : El Nino sediment ratio is overstated
   by ~+10 % (docs/35 §5.4). Quote that whenever a simulated contrast is quoted.

THE C4 RULE (docs/35 §6), exported here as constants so C4 imports rather than retypes
--------------------------------------------------------------------------------------
``alpha`` and ``beta`` may NOT compensate any of the above. Hard stops:
``alpha > ALPHA_HARD_STOP_HIGH`` (3x Williams) or ``alpha < ALPHA_HARD_STOP_LOW``, and
``beta`` outside ``[BETA_HARD_STOP_LOW, BETA_HARD_STOP_HIGH]``. The alpha thresholds are
valid ONLY at the registered pixel scale -- see :func:`musle_scale_factor` and
:func:`rescale_alpha_reference` before comparing a lumped fit to them.

Placement: ``scripts/c3/`` and not ``src/`` because Phase B's engine is frozen twice over
and nothing here is engine state -- these are pure functions with no I/O and no globals,
which ``src/mgb_sediment.py`` (C3.4) will import.  (docs/35 §7)
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "SECONDS_PER_DAY",
    "MM_KM2_PER_DAY_TO_M3S",
    "COP90_PIXEL_AREA_KM2",
    "SCS_TIME_BASE_RATIO",
    "WILLIAMS_ALPHA",
    "WILLIAMS_BETA",
    "ALPHA_EXPECTED_LOW",
    "ALPHA_EXPECTED_HIGH",
    "ALPHA_WATCH_HIGH",
    "ALPHA_HARD_STOP_HIGH",
    "ALPHA_HARD_STOP_LOW",
    "BETA_EXPECTED_LOW",
    "BETA_EXPECTED_HIGH",
    "BETA_HARD_STOP_LOW",
    "BETA_HARD_STOP_HIGH",
    "qpeak_daily_mean",
    "qpeak_scs_triangular",
    "time_of_concentration_kirpich",
    "peak_amplification",
    "musle_scale_factor",
    "rescale_alpha_reference",
    "sediment_bias_ratio",
    "check_musle_parameters",
]

# --------------------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------------------

SECONDS_PER_DAY = 86_400.0

#: 1 mm/day spread over 1 km2 is 1000 m3/day = 1/86.4 m3/s. This is the whole of
#: Buarque (2015) eq. 7; the 86.4 is a unit conversion, not a calibrated coefficient.
MM_KM2_PER_DAY_TO_M3S = 1.0 / 86.4

#: Registered application scale (docs/35 §4): the Copernicus GLO-90 pixel the basin
#: geometry was delineated from. 90 m x 90 m = 8100 m2 = 0.0081 km2.
COP90_PIXEL_AREA_KM2 = 0.0081

#: SCS triangular unit hydrograph: time base = 2.67 x time to peak. Kept symbolic so the
#: familiar 0.208 coefficient is *derived* in :func:`qpeak_scs_triangular` and can be
#: checked by a test, rather than pasted in.
SCS_TIME_BASE_RATIO = 2.67

# MUSLE reference parameters (Williams 1975; adopted unchanged by Buarque 2015 eq. 5
# *with this same daily-mean q_peak*, which is what makes 11.8 the like-for-like anchor).
WILLIAMS_ALPHA = 11.8
WILLIAMS_BETA = 0.56

# Registered C4 bands at the COP90 pixel scale (docs/35 §6.1, §6.3).
ALPHA_EXPECTED_LOW = 0.5 * WILLIAMS_ALPHA       # 5.9
ALPHA_EXPECTED_HIGH = 2.0 * WILLIAMS_ALPHA      # 23.6
ALPHA_WATCH_HIGH = 3.0 * WILLIAMS_ALPHA         # 35.4 -- also the hard stop
ALPHA_HARD_STOP_HIGH = 3.0 * WILLIAMS_ALPHA     # 35.4
ALPHA_HARD_STOP_LOW = WILLIAMS_ALPHA / 3.0      # 3.933...
BETA_EXPECTED_LOW = 0.50
BETA_EXPECTED_HIGH = 0.62
BETA_HARD_STOP_LOW = 0.45
BETA_HARD_STOP_HIGH = 0.65


def _as_array(name: str, value, allow_zero: bool = True):
    """Return ``value`` as a float array, rejecting negatives (NaN passes through)."""
    arr = np.asarray(value, dtype=float)
    with np.errstate(invalid="ignore"):
        bad = arr < 0.0
        if not allow_zero:
            bad = bad | (arr == 0.0)
    if np.any(bad):
        limit = "negative" if allow_zero else "non-positive"
        raise ValueError(f"{name} must not be {limit}; got min {np.nanmin(arr)!r}")
    return arr


# --------------------------------------------------------------------------------------
# The registered proxy
# --------------------------------------------------------------------------------------

def qpeak_daily_mean(qsur_mm, area_km2):
    """THE REGISTERED ``q_peak`` PROXY (docs/35 §4): daily-mean surface-runoff rate.

    ``q_peak = qsur_mm * area_km2 / 86.4``  (m3/s)

    Unit audit: a depth ``qsur_mm`` mm over ``area_km2`` km2 is
    ``qsur_mm/1000 * area_km2*1e6 = 1000 * qsur_mm * area_km2`` m3 of water in the day;
    divided by 86,400 s this is ``qsur_mm * area_km2 / 86.4`` m3/s.

    Assumes the day's runoff volume leaves the unit at a constant rate for 24 h, i.e. no
    storm within the day. The true instantaneous peak of any non-constant hydrograph
    exceeds its mean, so this is a provable FLOOR and the sediment it drives is a LOWER
    BOUND (docs/35 §5.1). Do not "fix" that here and do not let alpha fix it (docs/35 §6).

    Parameters
    ----------
    qsur_mm : float or array_like
        Surface runoff depth for the day, mm. Must be >= 0.
    area_km2 : float or array_like
        Area of the unit MUSLE is applied to, km2. Must be >= 0. Pass
        :data:`COP90_PIXEL_AREA_KM2` for the registered pixel-scale application.

    Returns
    -------
    numpy.ndarray or numpy.float64
        Peak runoff rate, m3/s. Zero wherever ``qsur_mm`` or ``area_km2`` is zero.
    """
    q = _as_array("qsur_mm", qsur_mm)
    a = _as_array("area_km2", area_km2)
    return q * a * MM_KM2_PER_DAY_TO_M3S


# --------------------------------------------------------------------------------------
# The rejected alternative -- kept only to reproduce the bias bound of docs/35 §5.1
# --------------------------------------------------------------------------------------

def qpeak_scs_triangular(qsur_mm, area_km2, tp_hours):
    """REJECTED option (ii) (docs/35 §3, §4): SCS triangular unit hydrograph peak.

    Not for production. It exists so that the sensitivity bound quoted in docs/35 §5.1 is
    reproducible, and so that the rejection can be re-checked rather than believed.

    ``q_peak = 2 V / T_b``, with ``V = 1000 * qsur_mm * area_km2`` m3 and
    ``T_b = SCS_TIME_BASE_RATIO * tp_hours``; this reduces to the familiar
    ``0.208 * area_km2 * qsur_mm / tp_hours`` (see the unit test).

    It is rejected because ``tp_hours = D/2 + 0.6 t_c`` needs (a) a rainfall-excess
    duration ``D``, unknowable in a model with no sub-daily rainfall, and (b) a
    basin-wide slope field for ``t_c``, which does not exist (docs/35 §2: no slope key in
    ``topology.npz``; the processed 30 m DEM covers 17.4 % of minibacias and they are the
    flat ones).

    Parameters
    ----------
    qsur_mm, area_km2 : float or array_like
        As in :func:`qpeak_daily_mean`.
    tp_hours : float or array_like
        Time to peak, hours. Must be > 0.
    """
    q = _as_array("qsur_mm", qsur_mm)
    a = _as_array("area_km2", area_km2)
    tp = _as_array("tp_hours", tp_hours, allow_zero=False)
    volume_m3 = 1000.0 * q * a
    time_base_s = SCS_TIME_BASE_RATIO * tp * 3600.0
    return 2.0 * volume_m3 / time_base_s


def time_of_concentration_kirpich(reach_km, slope):
    """Kirpich (1940) time of concentration, hours. Part of the REJECTED option (ii).

    ``t_c = 0.0195 * L[m]**0.77 * S**-0.385`` minutes, converted to hours here.

    **Unusable in production in this project**: there is no basin-wide slope field
    (docs/35 §2). Retained so the rejection in docs/35 §4 is reproducible if a slope
    field is ever built from the unextracted COP90 DEM (docs/35 §8 item 1) -- computable
    is not the same as chosen; re-opening the choice is an amendment under docs/35 §9.

    Parameters
    ----------
    reach_km : float or array_like
        Flow path / reach length, km. Must be > 0 (``topology.npz:reach_km`` has exactly
        one zero, the basin outlet -- floor it before calling).
    slope : float or array_like
        Dimensionless channel slope, m/m. Must be > 0.
    """
    length_m = _as_array("reach_km", reach_km, allow_zero=False) * 1000.0
    s = _as_array("slope", slope, allow_zero=False)
    minutes = 0.0195 * length_m ** 0.77 * s ** -0.385
    return minutes / 60.0


def peak_amplification(tp_hours):
    """Ratio ``qpeak_scs_triangular / qpeak_daily_mean`` -- the docs/35 §5.1 multiplier.

    ``= 86.4 / (SCS_TIME_BASE_RATIO/2 * 3600/1000 * tp_hours) = 17.978 / tp_hours``.

    This is the size of the bias the registered proxy accepts: ~1.50 at ``T_p`` = 12 h,
    ~2.99 at 6 h, ~5.99 at 3 h. It is NOT to be applied to simulated loads, and NOT to be
    absorbed by alpha -- Buarque/Fagundes' alpha = 11.8 already carries it (docs/35 §5.1).
    """
    tp = _as_array("tp_hours", tp_hours, allow_zero=False)
    return SECONDS_PER_DAY / (SCS_TIME_BASE_RATIO / 2.0 * 3600.0 * tp)


# --------------------------------------------------------------------------------------
# The scale trap (docs/35 §6.2) and the bias arithmetic (docs/35 §5.2)
# --------------------------------------------------------------------------------------

def musle_scale_factor(area_km2, pixel_area_km2=COP90_PIXEL_AREA_KM2, beta=WILLIAMS_BETA):
    """How much MUSLE inflates when lumped from pixels to a unit of ``area_km2``.

    Under uniform ``Qsur``, applying MUSLE once to ``N`` pixels' worth of area instead of
    ``N`` times per pixel multiplies the load by ``N**(2*beta - 1)`` (= ``N**0.12`` at
    beta = 0.56), because ``q_peak`` and ``A`` both scale with area inside the
    ``(Qsur * q_peak * A)**beta`` term.

    Measured on this basin's geometry (docs/35 §6.2): 2.149 at the median URH
    (4.762 km2), 2.630 at the median minibacia (25.58 km2), 3.552 at the largest
    (313.45 km2). So an alpha of 12 is textbook at pixel scale and a 2.2x over-fit at
    minibacia scale -- which is why C4 must report the application unit next to alpha.
    """
    a = _as_array("area_km2", area_km2, allow_zero=False)
    ap = _as_array("pixel_area_km2", pixel_area_km2, allow_zero=False)
    b = np.asarray(beta, dtype=float)
    return (a / ap) ** (2.0 * b - 1.0)


def rescale_alpha_reference(area_km2, alpha_reference=WILLIAMS_ALPHA,
                            pixel_area_km2=COP90_PIXEL_AREA_KM2, beta=WILLIAMS_BETA):
    """The alpha reference a LUMPED application must be compared against (docs/35 §6.2).

    ``alpha_ref(area) = alpha_reference / musle_scale_factor(area)``.

    Use it only if C4 departs from the registered pixel-scale application. The whole
    band (``ALPHA_EXPECTED_*``, ``ALPHA_HARD_STOP_*``) must be divided by the same
    factor; comparing a lumped alpha against the un-rescaled 11.8 makes the hard stop
    point the wrong way.
    """
    return np.asarray(alpha_reference, dtype=float) / musle_scale_factor(
        area_km2, pixel_area_km2=pixel_area_km2, beta=beta
    )


def sediment_bias_ratio(discharge_ratio, beta=WILLIAMS_BETA):
    """Sediment ratio implied by a peak-MAGNITUDE ratio: ``R**beta`` (docs/35 §5.2).

    Reproduces the docs/35 §5.2 column: ``R_AMS`` 0.820 -> 0.8948 (-10.5 %);
    ``R_Q1`` 0.847 -> 0.9112; ``R_Q5`` 0.975 -> 0.9859; El Nino ``R_AMS`` 0.686 -> 0.8097
    (-19.0 %); La Nina 0.808 -> 0.8875 (-11.3 %).

    **Only for magnitude ratios.** ``R_POT`` = 0.567 is a COUNT of independent events
    (1,285 simulated vs 2,236 observed). beta acts on magnitude, not on frequency, so
    passing ``R_POT`` here is a category error and gives a meaningless 0.728; docs/35
    §5.2 records that explicitly so nobody does it. The event-count channel stays a
    bracket (0 % to -42.5 %).
    """
    r = _as_array("discharge_ratio", discharge_ratio)
    return r ** np.asarray(beta, dtype=float)


def check_musle_parameters(alpha, beta, area_km2=None):
    """Apply the registered C4 anti-compensation rule (docs/35 §6) to a fitted pair.

    Parameters
    ----------
    alpha, beta : float
        The fitted MUSLE parameters.
    area_km2 : float, optional
        The application unit's area, if MUSLE was NOT applied at the registered pixel
        scale. When given, the alpha band is rescaled by :func:`musle_scale_factor`
        (docs/35 §6.2). When omitted, the pixel-scale band is used.

    Returns
    -------
    dict
        ``status`` is ``"ok"``, ``"watch"`` or ``"STOP"``; ``reasons`` lists every rule
        that fired; ``alpha_band`` / ``beta_band`` are the bands actually applied.
        ``"STOP"`` means C4 must report the fit and the docs/35 §5.3 bias statement and
        NOT adopt the parameters.
    """
    scale = 1.0 if area_km2 is None else float(musle_scale_factor(area_km2, beta=beta))
    band = {
        "expected": (ALPHA_EXPECTED_LOW / scale, ALPHA_EXPECTED_HIGH / scale),
        "watch_high": ALPHA_WATCH_HIGH / scale,
        "stop_high": ALPHA_HARD_STOP_HIGH / scale,
        "stop_low": ALPHA_HARD_STOP_LOW / scale,
        "reference": WILLIAMS_ALPHA / scale,
    }
    reasons = []
    status = "ok"
    if alpha > band["stop_high"]:
        status = "STOP"
        reasons.append(
            f"alpha {alpha:.3g} exceeds the hard stop {band['stop_high']:.3g} "
            f"(3x the {band['reference']:.3g} reference): fingerprint of alpha absorbing "
            "the peak deficit (docs/35 §6.1)"
        )
    elif alpha < band["stop_low"]:
        status = "STOP"
        reasons.append(
            f"alpha {alpha:.3g} is below the hard stop {band['stop_low']:.3g}: something "
            "upstream is over-producing and must be found, not offset (docs/35 §6.1)"
        )
    elif alpha > band["expected"][1]:
        status = "watch"
        reasons.append(
            f"alpha {alpha:.3g} is in the watch band "
            f"({band['expected'][1]:.3g}-{band['watch_high']:.3g}): adopt only with a "
            "written non-peak justification (docs/35 §6.1)"
        )
    elif alpha < band["expected"][0]:
        status = "watch"
        reasons.append(
            f"alpha {alpha:.3g} is below the expected band low {band['expected'][0]:.3g} "
            "(docs/35 §6.1)"
        )
    if beta > BETA_HARD_STOP_HIGH or beta < BETA_HARD_STOP_LOW:
        status = "STOP"
        reasons.append(
            f"beta {beta:.3g} is outside [{BETA_HARD_STOP_LOW}, {BETA_HARD_STOP_HIGH}]: "
            "event-amplification standing in for the ~43 % missing flood events "
            "(docs/35 §6.3)"
        )
    elif not (BETA_EXPECTED_LOW <= beta <= BETA_EXPECTED_HIGH):
        if status == "ok":
            status = "watch"
        reasons.append(
            f"beta {beta:.3g} is outside the expected "
            f"[{BETA_EXPECTED_LOW}, {BETA_EXPECTED_HIGH}] (docs/35 §6.3)"
        )
    return {
        "status": status,
        "reasons": reasons,
        "alpha_band": band,
        "beta_band": (BETA_EXPECTED_LOW, BETA_EXPECTED_HIGH),
        "scale_factor": scale,
    }
