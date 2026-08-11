"""Engine-grade tests for ``src/mgb_sediment.py`` (MUSLE hillslope erosion, stage C3.4).

The gates come from ``docs/31`` §C3.4 verbatim: zero rain => zero erosion; strict
monotonicity in K, C, LS2D, Q_sur and q_peak; a hand-computed single-cell case to 1e-12; a
units audit; NaN-free over the full basin-decade; and a mass ledger that closes exactly.
Two things are deliberately NOT tested here: the physical magnitude of the load (alpha/beta
are uncalibrated Williams-1975 starting values - fitting them is stage C4) and any per-area
yield (EMBARGOED, docs/23 §13.2 - no test in this file divides anything by an area).

Where a test pins a number that also lives in a document, the document is named. If such a
test fails, either the code changed or the registration did; reconcile them, do not relax
the test.
"""

import math
import pathlib

import numpy as np
import pytest

import mgb_sediment as sed

PROCESSED = pathlib.Path(__file__).resolve().parents[1] / "data" / "processed"
DRIVERS = PROCESSED / "sim_calibrated_v2" / "h2e_drivers.npz"
HAVE_CSVS = all(
    (PROCESSED / f).is_file()
    for f in ("minibacias.csv", "urh_fractions.csv", "minibacia_soil_params.csv",
              "urh_cp_factors.csv", "urh_ls2d.csv")
)
needs_csvs = pytest.mark.skipif(not HAVE_CSVS, reason="processed CSV inputs not present")
needs_drivers = pytest.mark.skipif(
    not DRIVERS.is_file(), reason="frozen H2E driver bundle not present (546 MB, gitignored)"
)

# --------------------------------------------------------------------------------------
# a tiny synthetic geometry: 2 minibacias, 3 URH cells, chosen so nothing is symmetric
# --------------------------------------------------------------------------------------

CLASS_C = {1: 0.003, 3: 0.01, 6: 1.0}
CLASS_P = {1: 1.0, 3: 1.0, 6: 1.0}


def _geom():
    """mini 1 (10 km2): URH 11 forest 4 km2, URH 36 bare 6 km2; mini 2 (20 km2): URH 23 all."""
    return sed.build_geometry(
        mini_ids=[1, 2],
        mini_area_km2=[10.0, 20.0],
        cell_mini=[0, 0, 1],
        cell_urh_code=[11, 36, 23],
        cell_area_km2=[4.0, 6.0, 20.0],
        mini_k=[0.030, 0.040],
        class_c=CLASS_C,
        class_p=CLASS_P,
        cell_ls2d=[5.0, 10.0, 2.0],
    )


def _qsur(ndays=40, seed=11):
    rng = np.random.default_rng(seed)
    wet = rng.random((ndays, 2)) < 0.5
    return np.where(wet, rng.gamma(1.3, 4.0, (ndays, 2)), 0.0)


# --------------------------------------------------------------------------------------
# 1. zero rain => zero erosion, EXACTLY
# --------------------------------------------------------------------------------------


def test_zero_runoff_gives_exactly_zero_erosion_primitive():
    """0**beta is exactly 0.0 for beta > 0, so a dry day must erode 0.0 to the last bit."""
    out = sed.musle_load_tonnes(0.0, 0.0, 0.0081, 0.03, 0.2, 1.0, 5.0)
    assert out == 0.0
    # zero in the runoff factor alone is enough, with every other factor large
    assert sed.musle_load_tonnes(0.0, 1e6, 1e6, 1e6, 1.0, 1.0, 1e6) == 0.0


def test_zero_runoff_gives_exactly_zero_erosion_engine():
    g, p = _geom(), sed.SedParams()
    q = np.zeros((7, 2))
    for backend in ("cells", "collapsed"):
        r = sed.simulate_sediment(g, p, q, backend=backend)
        assert np.all(r.delivered_t_day == 0.0)
        assert np.all(r.series["eroded"] == 0.0)
        assert np.all(r.cell_eroded_t == 0.0)
        assert r.ledger["eroded_t"] == 0.0
        assert r.state.store_t.tolist() == [0.0, 0.0]


def test_dry_days_stay_exactly_zero_inside_a_wet_record():
    """A zero column-day inside a wet record must still be exactly 0, not a rounding smear."""
    g, p = _geom(), sed.SedParams()
    q = _qsur()
    q[5] = 0.0
    r = sed.simulate_sediment(g, p, q, backend="cells")
    assert np.all(r.delivered_t_day[5] == 0.0)


# --------------------------------------------------------------------------------------
# 2. strict monotonicity in each factor, independently
# --------------------------------------------------------------------------------------


BASE = dict(qsur_mm=8.0, qpeak_m3s=7.5e-4, area_km2=0.0081,
            k_usle=0.03, c_usle=0.2, p_usle=1.0, ls2d=5.0)


@pytest.mark.parametrize("factor", ["k_usle", "c_usle", "ls2d", "qsur_mm", "qpeak_m3s",
                                    "p_usle", "area_km2"])
def test_strictly_increasing_in_every_factor(factor):
    """Each factor, varied alone over four decades, must give a strictly increasing load.

    ``qpeak_m3s`` is varied here independently of ``qsur_mm``, which is only possible
    because :func:`musle_load_tonnes` takes q_peak as an argument instead of deriving it
    (the registered proxy makes q_peak a function of Qsur - docs/35 §4).
    """
    values = np.array([0.01, 0.1, 1.0, 3.0, 10.0]) * BASE[factor]
    loads = [sed.musle_load_tonnes(**{**BASE, factor: v}) for v in values]
    assert all(b > a for a, b in zip(loads, loads[1:])), loads


def test_engine_strictly_increasing_in_qsur():
    """Monotone through the whole engine path, not only the primitive."""
    g, p = _geom(), sed.SedParams()
    loads = [float(sed.simulate_sediment(g, p, np.full((1, 2), q)).series["eroded"][0])
             for q in (0.5, 1.0, 2.0, 8.0, 40.0)]
    assert all(b > a for a, b in zip(loads, loads[1:])), loads


def test_engine_strictly_increasing_in_k_c_ls2d():
    """Perturb one static factor of one cell at a time; the basin load must rise strictly."""
    p = sed.SedParams()
    q = np.full((1, 2), 6.0)
    base = _geom()
    b0 = float(sed.simulate_sediment(base, p, q).series["eroded"][0])
    for kwargs in ({"mini_k": [0.031, 0.040]},
                   {"class_c": {**CLASS_C, 1: 0.004}},
                   {"cell_ls2d": [5.1, 10.0, 2.0]}):
        args = dict(mini_ids=[1, 2], mini_area_km2=[10.0, 20.0], cell_mini=[0, 0, 1],
                    cell_urh_code=[11, 36, 23], cell_area_km2=[4.0, 6.0, 20.0],
                    mini_k=[0.030, 0.040], class_c=CLASS_C, class_p=CLASS_P,
                    cell_ls2d=[5.0, 10.0, 2.0])
        args.update(kwargs)
        b1 = float(sed.simulate_sediment(sed.build_geometry(**args), p, q).series["eroded"][0])
        assert b1 > b0, (kwargs, b0, b1)


# --------------------------------------------------------------------------------------
# 3. hand-computed single-cell case, to 1e-12
# --------------------------------------------------------------------------------------

# One COP90 pixel, 0.0081 km2, one day, Qsur = 10 mm, K = 0.03, C = 0.2, P = 1, LS2D = 5,
# at the PRE-AMENDMENT convention (volume_convention='pixel_km2', k_unit_system='si_stored').
# Kept as-is so the pre-2026-08-11 arithmetic stays pinned and the amendment's factor is
# measurable against something fixed.
#
#   q_peak = 10 mm * 0.0081 km2 / 86.4        = 0.0009375        m3/s
#   product = 10 * 0.0009375 * 0.0081         = 7.59375e-05
#   Sed    = 11.8 * 7.59375e-05**0.56 * 0.03 * 0.2 * 1.0 * 5.0
#          = 1.7439...e-03 tonnes/day
HAND_QSUR_MM = 10.0
HAND_QPEAK_M3S = 10.0 * 0.0081 / 86.4
HAND_PRODUCT = 10.0 * HAND_QPEAK_M3S * 0.0081
HAND_LOAD_T = 11.8 * math.pow(HAND_PRODUCT, 0.56) * 0.03 * 0.2 * 1.0 * 5.0

#: The pre-amendment parameter set, by name.  Every test that compares against HAND_LOAD_T
#: must pass this explicitly - after 2026-08-11 the DEFAULTS are a different convention.
LEGACY = dict(volume_convention="pixel_km2", k_unit_system="si_stored")

#: The same pixel-day under the ADOPTED convention.  The two unit corrections are
#: 1000**beta (inside the power) and 1/0.1317 (linear on K), i.e. 47.8630 x 7.593014.
ADOPTED_UNIT_FACTOR = math.pow(1000.0, 0.56) / 0.1317
HAND_LOAD_T_ADOPTED = HAND_LOAD_T * ADOPTED_UNIT_FACTOR


def test_hand_computed_single_pixel_primitive():
    got = sed.musle_load_tonnes(HAND_QSUR_MM, HAND_QPEAK_M3S, 0.0081, 0.03, 0.2, 1.0, 5.0)
    # 10 * 0.0081 / 86.4 and 81 / 86400 are the same real number, 9.375e-4 m3/s, and differ
    # by one ULP as doubles - which is why this comparison has a tolerance and the decimal
    # 0.0009375 is not asserted bitwise.
    assert abs(HAND_QPEAK_M3S - 81.0 / 86400.0) <= 1e-15 * 9.375e-4
    assert abs(float(got) - HAND_LOAD_T) <= 1e-12 * HAND_LOAD_T


def test_hand_computed_single_pixel_through_the_engine():
    """The engine on a one-pixel URH must reproduce the same number to 1e-12 relative.

    This is the end-to-end unit check: it goes through the registered q_peak proxy, the
    pixel-count scaling, the delivery reservoir and the ledger.  Run twice: at the
    pre-amendment convention (against HAND_LOAD_T) and at the adopted default (against
    HAND_LOAD_T_ADOPTED), so the amendment is pinned from both sides.
    """
    g = sed.build_geometry(
        mini_ids=[7], mini_area_km2=[0.0081], cell_mini=[0], cell_urh_code=[14],
        cell_area_km2=[0.0081], mini_k=[0.03], class_c={4: 0.2}, class_p={4: 1.0},
        cell_ls2d=[5.0],
    )
    for params, expect in ((sed.SedParams(**LEGACY), HAND_LOAD_T),
                           (sed.SedParams(), HAND_LOAD_T_ADOPTED)):
        r = sed.simulate_sediment(g, params, np.array([[HAND_QSUR_MM]]),
                                  backend="cells", dtype_out=np.float64)
        assert abs(float(r.delivered_t_day[0, 0]) - expect) <= 1e-12 * expect
        assert abs(r.ledger["eroded_t"] - expect) <= 1e-12 * expect


# --------------------------------------------------------------------------------------
# 3b. the audit's hand-computed REAL unit-day (regression, exact value)
# --------------------------------------------------------------------------------------

# The 2026-08-11 independent audit hand-computed one real minibacia-day entirely from the
# frozen inputs, with the unit chosen by a rule fixed BEFORE any sediment number was looked
# at: the minibacia at the basin median of decadal Qsur, on its own maximum-Qsur day.
#
#   minibacia 16115, 2009-04-11 (its own max-Qsur day, verified below against the frozen npz)
#   Qsur   = 26.677167892456055 mm/day     h2e_drivers.npz:qsur_rel_mm[100, col(16115)]
#   area   = 24.49 km2                     minibacias.csv x urh_fractions.csv (fraction 1.0)
#   ONE URH cell, code 11 = Forest         urh_fractions.csv: '11' is the only non-zero column
#   K      = 0.019   (SI, as stored)       minibacia_soil_params.csv
#   C      = 0.003, P = 1.0                urh_cp_factors.csv class_id 1
#   LS2D   = 118.245                       urh_ls2d.csv:ls2d_hs (mini 16115, urh 11)
#
# The arithmetic, at the ADOPTED convention (f_vol = 1000, f_K = 1/0.1317):
#   n_pix   = 24.49 / 0.0081                   = 3023.456790123457
#   q_peak  = 26.677167892456055*0.0081/86.4   = 2.5009844899177547e-03  m3/s
#   product = Qsur * q_peak * a_p * 1000       = 0.54042538338511248
#   ^0.56                                      = 0.70848720916668628
#   K_us    = 0.019 / 0.1317                   = 0.14426727410782078
#   per pixel = 11.8 * 0.70848...  * K_us * 0.003 * 1.0 * 118.245 = 0.42784443518775633 t
#   x n_pix                                    = 1293.5691626849571 tonnes/day
UNIT_DAY_QSUR_MM = 26.677167892456055
UNIT_DAY_MINI_ID = 16115
UNIT_DAY_DATE = "2009-04-11"
UNIT_DAY_ROW = 100
UNIT_DAY_LOAD_T = 1293.5691626849571
# The SYNTHETIC tests above pass class_c={1: 0.003} explicitly and assert convention
# arithmetic, so they are unaffected by the CSV.  The FILE-BASED join guard reads
# urh_cp_factors.csv, whose cited-central revision (docs/41, 2026-08-11) moved Forest
# C from 0.003 to 0.005.  MUSLE is linear in C, so the same unit-day load scales by
# 0.005/0.003 exactly:
UNIT_DAY_C_FROM_CSV = 0.005
UNIT_DAY_LOAD_T_FROM_CSV = UNIT_DAY_LOAD_T * UNIT_DAY_C_FROM_CSV / 0.003   # 2155.9486044749287


def _unit_day_geometry():
    return sed.build_geometry(
        mini_ids=[UNIT_DAY_MINI_ID], mini_area_km2=[24.49], cell_mini=[0],
        cell_urh_code=[11], cell_area_km2=[24.49], mini_k=[0.019],
        class_c={1: 0.003}, class_p={1: 1.0}, cell_ls2d=[118.245],
    )


def test_audit_hand_computed_real_unit_day_exact_value():
    """REGRESSION: the audit's real unit-day must give 1293.5691626849571 t/day.

    The expected value is a hand computation (the comment block above walks every
    intermediate), NOT a recorded engine output, so this test can fail the engine rather than
    merely echo it.  It pins the whole adopted chain at once: the registered q_peak proxy, the
    pixel count, ``volume_convention='williams_m3'`` and ``k_unit_system='us_customary'``.
    """
    g = _unit_day_geometry()
    r = sed.simulate_sediment(g, sed.SedParams(), np.array([[UNIT_DAY_QSUR_MM]]),
                              backend="cells", dtype_out=np.float64)
    got = float(r.delivered_t_day[0, 0])
    assert abs(got - UNIT_DAY_LOAD_T) <= 1e-12 * UNIT_DAY_LOAD_T, got
    # the collapsed backend must reach the same number by its own route
    r2 = sed.simulate_sediment(g, sed.SedParams(), np.array([[UNIT_DAY_QSUR_MM]]),
                               backend="collapsed", dtype_out=np.float64)
    assert abs(float(r2.delivered_t_day[0, 0]) - UNIT_DAY_LOAD_T) <= 1e-12 * UNIT_DAY_LOAD_T
    # and re-derive it from the literal arithmetic, independently of the module's internals
    n_pix = 24.49 / 0.0081
    q_peak = UNIT_DAY_QSUR_MM * 0.0081 / 86.4
    product = UNIT_DAY_QSUR_MM * q_peak * 0.0081 * 1000.0
    expect = (n_pix * 11.8 * math.pow(product, 0.56) * (0.019 / 0.1317) * 0.003 * 1.0
              * 118.245)
    assert abs(expect - UNIT_DAY_LOAD_T) <= 1e-12 * UNIT_DAY_LOAD_T


def test_audit_unit_day_at_the_pre_amendment_convention():
    """The same day at the pre-amendment convention, and the ratio between them.

    3.559388794358739 t/day was what this engine produced before 2026-08-11 for that cell-day;
    the amendment multiplies it by exactly ``1000**0.56 / 0.1317 = 363.4245196``.  Pinning
    both ends means the amendment cannot be silently widened or narrowed later.
    """
    g = _unit_day_geometry()
    q = np.array([[UNIT_DAY_QSUR_MM]])
    legacy = float(sed.simulate_sediment(g, sed.SedParams(**LEGACY), q, backend="cells",
                                        dtype_out=np.float64).delivered_t_day[0, 0])
    assert abs(legacy - 3.559388794358739) <= 1e-12 * 3.559388794358739
    assert abs(UNIT_DAY_LOAD_T / legacy - 363.424519607167) <= 1e-9 * 363.424519607167
    assert abs(ADOPTED_UNIT_FACTOR - 363.424519607167) <= 1e-9 * 363.424519607167


@needs_csvs
@needs_drivers
def test_audit_unit_day_reproduces_from_the_real_files(basin_geometry):
    """The same number, but with every input read from the real CSVs and the frozen npz.

    This is the join guard for the regression above: the synthetic version could pass while
    ``load_geometry`` handed minibacia 16115 the wrong LS2D or the driver column order was
    scrambled.  Here the id, the date and all five factors come from disk.
    """
    drivers = sed.load_drivers(DRIVERS)
    col = int(np.flatnonzero(drivers.mini_ids == UNIT_DAY_MINI_ID)[0])
    row = int(np.flatnonzero(
        drivers.dates.astype("datetime64[D]") == np.datetime64(UNIT_DAY_DATE))[0])
    assert row == UNIT_DAY_ROW
    q = float(drivers.qsur_mm[row, col])
    assert q == UNIT_DAY_QSUR_MM
    # the rule that selected the day: it is that minibacia's own maximum-Qsur day
    assert int(np.argmax(drivers.qsur_mm[:, col])) == row

    g = basin_geometry
    j = int(np.flatnonzero(g.cell_mini == int(g.index_of([UNIT_DAY_MINI_ID])[0]))[0])
    assert int(g.cell_urh_code[j]) == 11
    assert abs(g.cell_ls2d[j] - 118.245) < 1e-9
    assert abs(g.cell_k[j] - 0.019) < 1e-12
    assert abs(g.cell_c[j] - UNIT_DAY_C_FROM_CSV) < 1e-12
    assert abs(g.cell_area_km2[j] - 24.49) < 1e-9

    r = sed.simulate_sediment(g, sed.SedParams(), drivers.qsur_mm[row:row + 1],
                              backend="collapsed", dtype_out=np.float64,
                              record_ids=[UNIT_DAY_MINI_ID])
    got = float(r.delivered_t_day[0, 0])
    assert abs(got - UNIT_DAY_LOAD_T_FROM_CSV) <= 1e-9 * UNIT_DAY_LOAD_T_FROM_CSV, got


# --------------------------------------------------------------------------------------
# 4. units audit
# --------------------------------------------------------------------------------------


def test_units_audit_tonnes_per_day():
    """Assert the output really is TONNES PER DAY, by checking every stage's arithmetic.

    Stage 1 - the water, in SI: a depth of 10 mm over one COP90 pixel is
    0.010 m * 8100 m2 = 81 m3 of water in the day; 81 m3 / 86,400 s = 9.375e-4 m3/s. That is
    exactly what the registered proxy returns, so the m3/s stage is dimensionally checked
    against first principles and not against itself.

    Stage 2 - the load, from Williams' regression: MUSLE is an empirical, dimensionally
    inhomogeneous relation, so the tonne scale is carried entirely by alpha at one unit
    convention. At the registered convention (docs/35 §4) one pixel-day with Qsur = 10 mm,
    K = 0.03, C = 0.2, P = 1, LS2D = 5 gives 11.8 * (7.59375e-5)**0.56 * 0.03 = 1.7439e-3
    tonnes/day - the hand arithmetic above.

    Stage 3 - extensivity, which is what makes "tonnes" (a mass) rather than a rate density:
    the load must be exactly linear in the number of pixels (double the area, double the
    tonnes) and exactly additive over days (three identical days give three times the mass).
    Both are asserted here to 1e-12; a formulation that was secretly per-area or per-second
    would fail one of them.
    """
    # stage 1: SI water volume -> m3/s, from first principles
    water_m3 = 0.010 * 8100.0
    assert water_m3 == 81.0
    assert abs(float(sed.qpeak_daily_mean(10.0, 0.0081)) - water_m3 / 86400.0) < 1e-18

    # stage 2: tonnes for one pixel-day
    one_pixel = sed.musle_load_tonnes(10.0, water_m3 / 86400.0, 0.0081, 0.03, 0.2, 1.0, 5.0)
    assert abs(float(one_pixel) - HAND_LOAD_T) <= 1e-12 * HAND_LOAD_T

    # stage 3a: exactly linear in area (100 pixels = 0.81 km2), at the pre-amendment
    # convention so the comparison is against the hand arithmetic above
    g100 = sed.build_geometry(
        mini_ids=[1], mini_area_km2=[0.81], cell_mini=[0], cell_urh_code=[14],
        cell_area_km2=[0.81], mini_k=[0.03], class_c={4: 0.2}, class_p={4: 1.0},
        cell_ls2d=[5.0],
    )
    r1 = sed.simulate_sediment(g100, sed.SedParams(**LEGACY), np.array([[10.0]]),
                               dtype_out=np.float64)
    assert abs(r1.ledger["eroded_t"] - 100.0 * HAND_LOAD_T) <= 1e-12 * 100.0 * HAND_LOAD_T

    # stage 3b: exactly additive over days
    r3 = sed.simulate_sediment(g100, sed.SedParams(**LEGACY), np.full((3, 1), 10.0),
                               dtype_out=np.float64)
    assert abs(r3.ledger["eroded_t"] - 3.0 * r1.ledger["eroded_t"]) <= 1e-12 * r3.ledger["eroded_t"]


def test_volume_convention_factor_is_exactly_1000_to_the_beta():
    """The unit conventions of the docstring differ by exactly 1000**beta = 47.8630x.

    A documented constant; pinning it here is what stops it from being quietly folded into
    alpha (which would need alpha ~ 565, 16x past the docs/35 §6.1 hard stop of 35.4).
    """
    g = _geom()
    q = np.full((4, 2), 7.0)
    a = sed.simulate_sediment(g, sed.SedParams(volume_convention="pixel_km2"),
                              q).ledger["eroded_t"]
    b = sed.simulate_sediment(g, sed.SedParams(volume_convention="williams_m3"),
                              q).ledger["eroded_t"]
    factor = math.pow(1000.0, sed.WILLIAMS_BETA)
    assert abs(b / a - factor) <= 1e-12 * factor
    assert abs(factor - 47.863009232263856) < 1e-9
    # and the compensation it would require is past the registered hard stop
    assert sed.SedParams(alpha=sed.WILLIAMS_ALPHA * factor).check()["status"] == "STOP"


# --------------------------------------------------------------------------------------
# 4b. the convention matrix: every named option returns its DOCUMENTED factor
# --------------------------------------------------------------------------------------

#: name -> (documented load multiplier relative to the option's own reference member)
DOCUMENTED_VOLUME_LOAD_FACTORS = {
    "pixel_km2": 1.0,
    "swat_mm_ha": math.pow(100.0, 0.56),      # 13.1826
    "williams_m3": math.pow(1000.0, 0.56),    # 47.8630
}
DOCUMENTED_K_FACTORS = {"si_stored": 1.0, "us_customary": 1.0 / 0.1317}
DOCUMENTED_LS_AGG_FACTORS = {"area_weighted_mean": 1.0, "per_cell_median": 16.555 / 30.605}
DOCUMENTED_LS_RES_FACTORS = {"native_90m": 1.0, "rescale_740m_ref": 7.51 / 12.5}


@pytest.mark.parametrize("name,expect", sorted(DOCUMENTED_VOLUME_LOAD_FACTORS.items()))
def test_each_volume_convention_returns_its_documented_load_factor(name, expect):
    """Measured on the engine, relative to ``pixel_km2``: 1 / 13.1826 / 47.8630.

    The volume factor sits inside ``^beta``, so the LOAD factor is ``F**beta`` and not ``F``.
    Getting that wrong is a 1000-vs-47.9 error, which is why it is asserted and not commented.
    """
    g, q = _geom(), np.full((3, 2), 6.5)
    ref = sed.simulate_sediment(g, sed.SedParams(volume_convention="pixel_km2", **{
        "k_unit_system": "si_stored"}), q).ledger["eroded_t"]
    got = sed.simulate_sediment(g, sed.SedParams(volume_convention=name,
                                                k_unit_system="si_stored"),
                                q).ledger["eroded_t"]
    assert abs(got / ref - expect) <= 1e-12 * expect
    p = sed.SedParams(volume_convention=name)
    assert p.volume_factor == sed.VOLUME_FACTORS[name]
    assert abs(p.convention_summary()["volume_load_multiplier"] - expect) <= 1e-12 * expect


@pytest.mark.parametrize("name,expect", sorted(DOCUMENTED_K_FACTORS.items()))
def test_each_k_unit_system_returns_its_documented_load_factor(name, expect):
    """K multiplies the load LINEARLY (it is outside ``^beta``): 1.0 or 7.593014.

    7.593014 = 1/0.1317, the exact inverse of the SI conversion
    ``notebooks/09_soil_parameters.ipynb`` §4 documents applying to Wischmeier & Smith's
    US-customary class values.  ``alpha`` = 11.8 belongs to the US-customary numerics.
    """
    g, q = _geom(), np.full((3, 2), 6.5)
    ref = sed.simulate_sediment(g, sed.SedParams(k_unit_system="si_stored"),
                                q).ledger["eroded_t"]
    got = sed.simulate_sediment(g, sed.SedParams(k_unit_system=name), q).ledger["eroded_t"]
    assert abs(got / ref - expect) <= 1e-12 * expect
    assert abs(sed.SedParams(k_unit_system=name).k_factor - expect) <= 1e-12 * expect
    assert abs(sed.K_US_PER_K_SI - 7.593014426727411) < 1e-9


@pytest.mark.parametrize("name,expect", sorted(DOCUMENTED_LS_AGG_FACTORS.items()))
def test_each_ls2d_aggregation_returns_its_documented_load_factor(name, expect):
    """LS2D multiplies linearly too.  ADOPTED ``area_weighted_mean`` is EXACTLY 1.000.

    The 1.000 is the point: the LS aggregation choice contributes nothing to the C3.6
    order-of-magnitude gap, and this test is what keeps that claim honest.
    """
    g, q = _geom(), np.full((3, 2), 6.5)
    ref = sed.simulate_sediment(g, sed.SedParams(), q).ledger["eroded_t"]
    got = sed.simulate_sediment(g, sed.SedParams(ls2d_aggregation=name), q).ledger["eroded_t"]
    assert abs(got / ref - expect) <= 1e-12 * expect
    if name == sed.DEFAULT_LS2D_AGGREGATION:
        assert expect == 1.0
        assert got == ref                      # x1.0 is bitwise identity, not near-identity


@pytest.mark.parametrize("name,expect", sorted(DOCUMENTED_LS_RES_FACTORS.items()))
def test_each_ls2d_resolution_returns_its_documented_load_factor(name, expect):
    """ADOPTED ``native_90m`` is EXACTLY 1.000 - no resolution rescaling is applied."""
    g, q = _geom(), np.full((3, 2), 6.5)
    ref = sed.simulate_sediment(g, sed.SedParams(), q).ledger["eroded_t"]
    got = sed.simulate_sediment(g, sed.SedParams(ls2d_resolution=name), q).ledger["eroded_t"]
    assert abs(got / ref - expect) <= 1e-12 * expect
    if name == sed.DEFAULT_LS2D_RESOLUTION:
        assert expect == 1.0
        assert got == ref


def test_the_adopted_default_is_exactly_363_424x_the_pre_amendment_default():
    """The whole 2026-08-11 amendment, as one number, on the engine.

    ``1000**0.56 * (1/0.1317) = 363.4245196``.  Any future edit that changes a default without
    an amendment moves this ratio and fails here.
    """
    g, q = _geom(), np.full((5, 2), 4.25)
    legacy = sed.simulate_sediment(g, sed.SedParams(**LEGACY), q).ledger["eroded_t"]
    adopted = sed.simulate_sediment(g, sed.SedParams(), q).ledger["eroded_t"]
    assert abs(adopted / legacy - 363.424519607167) <= 1e-10 * 363.424519607167


def test_unknown_convention_names_are_rejected_not_silently_ignored():
    for kwargs, match in (
        ({"volume_convention": "m3"}, "volume_convention"),
        ({"k_unit_system": "metric"}, "k_unit_system"),
        ({"ls2d_aggregation": "median"}, "ls2d_aggregation"),
        ({"ls2d_resolution": "90m"}, "ls2d_resolution"),
    ):
        with pytest.raises(ValueError, match=match):
            sed.SedParams(**kwargs)


def test_pixel_scale_matters_by_the_registered_factor():
    """Lumping N pixels into one application unit inflates the load by N**(2*beta-1).

    docs/35 §6.2's scale trap, asserted on the engine itself: applying MUSLE at a 1 km2
    unit instead of the 0.0081 km2 pixel multiplies the same cell's load by
    ``musle_scale_factor``, so an alpha fitted at the wrong unit is wrong by that factor.
    """
    import qpeak

    g = _geom()
    q = np.full((3, 2), 9.0)
    fine = sed.simulate_sediment(g, sed.SedParams(), q).ledger["eroded_t"]
    coarse = sed.simulate_sediment(g, sed.SedParams(pixel_area_km2=1.0), q).ledger["eroded_t"]
    expect = float(qpeak.musle_scale_factor(1.0, beta=sed.WILLIAMS_BETA))
    assert abs(coarse / fine - expect) <= 1e-12 * expect


# --------------------------------------------------------------------------------------
# 5. the mass ledger
# --------------------------------------------------------------------------------------


def test_ledger_closes_exactly_pass_through():
    """Default tau = 0: delivery is bitwise pass-through, so the residual is exactly 0.0."""
    g, p = _geom(), sed.SedParams()
    assert p.delivery_release_coef == 1.0
    r = sed.simulate_sediment(g, p, _qsur(), backend="cells")
    assert r.ledger["residual_t"] == 0.0
    assert r.ledger["exact"] is True
    assert r.ledger["delivered_t"] == r.ledger["eroded_t"]
    assert r.ledger["store_end_t"] == 0.0
    assert np.array_equal(r.series["delivered"], r.series["eroded"])


@pytest.mark.parametrize("tau", [0.5, 1.0, 3.0, 30.0])
def test_ledger_closes_with_a_delivery_reservoir(tau):
    """eroded = delivered + stored, with a non-zero delivery lag, and nothing goes negative."""
    g = _geom()
    p = sed.SedParams(tau_delivery_days=tau)
    r = sed.simulate_sediment(g, p, _qsur(), backend="cells")
    assert r.ledger["residual_relative"] < 1e-14
    assert r.ledger["store_end_t"] > 0.0
    assert r.ledger["delivered_t"] < r.ledger["eroded_t"]
    assert np.all(r.state.store_t >= 0.0)
    assert np.all(r.delivered_t_day >= 0.0)
    # the store only ever holds what has been eroded and not yet delivered
    assert abs((r.ledger["eroded_t"] - r.ledger["delivered_t"]) - r.ledger["store_end_t"]) \
        <= 1e-12 * r.ledger["eroded_t"]


def test_delivery_reservoir_is_a_pure_delay_not_a_sink():
    """Run long enough past the last erosion event and everything eventually arrives."""
    g = _geom()
    p = sed.SedParams(tau_delivery_days=2.0)
    q = np.zeros((600, 2))
    q[0] = 25.0
    r = sed.simulate_sediment(g, p, q, backend="cells")
    assert r.ledger["store_end_t"] / r.ledger["eroded_t"] < 1e-9
    assert abs(r.ledger["delivered_t"] / r.ledger["eroded_t"] - 1.0) < 1e-9


# --------------------------------------------------------------------------------------
# 6. the two backends are independent implementations and must agree
# --------------------------------------------------------------------------------------


def test_backends_agree():
    g, p = _geom(), sed.SedParams(tau_delivery_days=1.5)
    q = _qsur(60, seed=5)
    a = sed.simulate_sediment(g, p, q, backend="cells", dtype_out=np.float64)
    b = sed.simulate_sediment(g, p, q, backend="collapsed", dtype_out=np.float64)
    assert np.allclose(a.delivered_t_day, b.delivered_t_day, rtol=1e-12, atol=0.0)
    assert np.allclose(a.cell_eroded_t, b.cell_eroded_t, rtol=1e-12, atol=0.0)
    assert abs(a.ledger["eroded_t"] - b.ledger["eroded_t"]) <= 1e-12 * a.ledger["eroded_t"]
    assert sed.simulate_sediment(g, p, q, backend="auto").backend == "collapsed"


def test_cell_totals_sum_to_the_basin_total():
    g, p = _geom(), sed.SedParams()
    r = sed.simulate_sediment(g, p, _qsur(), backend="cells")
    assert abs(float(r.cell_eroded_t.sum()) - r.ledger["eroded_t"]) \
        <= 1e-12 * r.ledger["eroded_t"]
    by_class = r.eroded_by_land_class(g)
    assert abs(sum(by_class.values()) - r.ledger["eroded_t"]) <= 1e-12 * r.ledger["eroded_t"]


# --------------------------------------------------------------------------------------
# 7. validation: wrong input must raise, never be coerced
# --------------------------------------------------------------------------------------


def test_negative_and_nonfinite_qsur_rejected():
    g, p = _geom(), sed.SedParams()
    with pytest.raises(ValueError, match="negative"):
        sed.simulate_sediment(g, p, np.array([[-1.0, 1.0]]))
    with pytest.raises(ValueError, match="non-finite"):
        sed.simulate_sediment(g, p, np.array([[np.nan, 1.0]]))
    with pytest.raises(ValueError, match="must be"):
        sed.simulate_sediment(g, p, np.zeros((3, 5)))
    with pytest.raises(ValueError, match="dates"):
        sed.simulate_sediment(g, p, np.zeros((3, 2)), dates=[1, 2])


def test_bad_parameters_rejected():
    with pytest.raises(ValueError, match="volume_convention"):
        sed.SedParams(volume_convention="m3")
    with pytest.raises(ValueError, match="beta"):
        sed.SedParams(beta=0.0)
    with pytest.raises(ValueError, match="fg"):
        sed.SedParams(fg=1.5)
    with pytest.raises(ValueError, match="tau_delivery_days"):
        sed.SedParams(tau_delivery_days=-1.0)
    with pytest.raises(ValueError, match="pixel_area_km2"):
        sed.SedParams(pixel_area_km2=0.0)


def test_bad_geometry_rejected():
    args = dict(mini_ids=[1, 2], mini_area_km2=[10.0, 20.0], cell_mini=[0, 0, 1],
                cell_urh_code=[11, 36, 23], cell_area_km2=[4.0, 6.0, 20.0],
                mini_k=[0.030, 0.040], class_c=CLASS_C, class_p=CLASS_P,
                cell_ls2d=[5.0, 10.0, 2.0])
    with pytest.raises(ValueError, match="no C factor"):
        sed.build_geometry(**{**args, "class_c": {1: 0.003, 3: 0.01}})
    with pytest.raises(ValueError, match="cell_ls2d"):
        sed.build_geometry(**{**args, "cell_ls2d": [5.0, np.nan, 2.0]})
    with pytest.raises(ValueError, match="cell_area_km2"):
        sed.build_geometry(**{**args, "cell_area_km2": [4.0, 0.0, 20.0]})
    with pytest.raises(ValueError, match="mini_k"):
        sed.build_geometry(**{**args, "mini_k": [0.03, -0.04]})
    with pytest.raises(ValueError, match="out of range"):
        sed.build_geometry(**{**args, "cell_mini": [0, 0, 2]})
    with pytest.raises(ValueError, match="duplicate"):
        sed.build_geometry(**{**args, "mini_ids": [1, 1]})


def test_params_are_frozen():
    """A C4 search must build a new SedParams per evaluation, not mutate a shared one."""
    p = sed.SedParams()
    with pytest.raises(Exception):
        p.alpha = 20.0


def test_registered_defaults_are_the_williams_starting_values():
    """Pin the documented defaults, INCLUDING the 2026-08-11 convention amendment.

    ``volume_convention`` and ``k_unit_system`` changed on 2026-08-11 (module docstring,
    CONVENTION AMENDMENT; docs/35 §9.2).  If this test fails, a default moved - reconcile the
    docstring, docs/35 §9 and docs/37 before touching the assertion.
    """
    p = sed.SedParams()
    assert (p.alpha, p.beta) == (11.8, 0.56)
    assert p.fg == 1.0
    assert p.pixel_area_km2 == 0.0081
    assert p.tau_delivery_days == 0.0
    assert p.volume_convention == "williams_m3" == sed.DEFAULT_VOLUME_CONVENTION
    assert p.k_unit_system == "us_customary" == sed.DEFAULT_K_UNIT_SYSTEM
    assert p.ls2d_aggregation == "area_weighted_mean" == sed.DEFAULT_LS2D_AGGREGATION
    assert p.ls2d_resolution == "native_90m" == sed.DEFAULT_LS2D_RESOLUTION
    assert p.ls2d_factor == 1.0
    assert p.check()["status"] == "ok"
    # every prior convention is still reachable by name (the choice stays reversible)
    assert set(sed.VOLUME_CONVENTIONS) == {"pixel_km2", "swat_mm_ha", "williams_m3"}
    assert set(sed.K_UNIT_SYSTEMS) == {"si_stored", "us_customary"}


# --------------------------------------------------------------------------------------
# 8. the real basin: geometry, then the full decade
# --------------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def basin_geometry():
    if not HAVE_CSVS:
        pytest.skip("processed CSV inputs not present")
    with pytest.warns(UserWarning, match="differ by more than"):
        g = sed.load_geometry(PROCESSED)
    return g


@needs_csvs
def test_real_geometry_shape_and_ranges(basin_geometry):
    g = basin_geometry
    assert g.n_mini == 8672
    assert g.n_cells == 32782                      # C3.1 / nb08: active (minibacia, URH) cells
    assert abs(g.covered_area_km2 - 257096.93) < 1.0
    assert g.ls2d_column == "ls2d_hs"              # the column ls2d.py says MUSLE must use
    for name, arr in (("K", g.cell_k), ("C", g.cell_c), ("P", g.cell_p),
                      ("LS2D", g.cell_ls2d), ("area", g.cell_area_km2)):
        assert np.all(np.isfinite(arr)), name
        assert np.all(arr >= 0.0), name
    assert 0.019 <= g.cell_k.min() and g.cell_k.max() <= 0.0495
    # urh_cp_factors.csv, cited-central revision (docs/41 2026-08-11):
    # Forest .005 Shrub .015 Grassland .015 Cropland .2 Urban .03 Bare .5
    # Water 0 Wetland .005  -> six distinct values
    assert set(np.unique(g.cell_c).tolist()) <= set(
        [0.0, 0.005, 0.015, 0.03, 0.2, 0.5])
    assert np.all(g.cell_p == 1.0)                 # P = 1.0 basin-wide (C3.2, stated)
    assert g.audit["frac_cells_area_off"] > 0.0    # the area disagreement is real, not hidden


@needs_csvs
def test_real_geometry_join_is_not_scrambled(basin_geometry):
    """Every static factor of 300 random cells, re-looked-up straight from the CSVs.

    ``load_geometry`` joins four files on (minibacia, URH). A mis-join would not raise and
    would not change any total - it would silently give a forest cell the bare cell's LS2D,
    which is a spatial scramble no distributional test can see. So the join is checked
    element-wise against independent ``pandas`` lookups.
    """
    import pandas as pd

    g = basin_geometry
    ul = pd.read_csv(PROCESSED / "urh_ls2d.csv").set_index(["mini", "urh"])
    sp = pd.read_csv(PROCESSED / "minibacia_soil_params.csv").set_index("id")
    cp = pd.read_csv(PROCESSED / "urh_cp_factors.csv").set_index("class_id")
    uf = pd.read_csv(PROCESSED / "urh_fractions.csv").set_index("mini")
    mb = pd.read_csv(PROCESSED / "minibacias.csv").set_index("id")
    rng = np.random.default_rng(0)
    for i in rng.integers(0, g.n_cells, 300):
        mid = int(g.mini_ids[g.cell_mini[i]])
        code = int(g.cell_urh_code[i])
        assert abs(g.cell_ls2d[i] - ul.loc[(mid, code), "ls2d_hs"]) < 1e-9, (mid, code)
        assert abs(g.cell_k[i] - sp.loc[mid, "K"]) < 1e-12, (mid, code)
        assert abs(g.cell_c[i] - cp.loc[code % 10, "C"]) < 1e-12, (mid, code)
        assert abs(g.cell_p[i] - cp.loc[code % 10, "P"]) < 1e-12, (mid, code)
        expect_area = uf.loc[mid, str(code)] * mb.loc[mid, "area_km2"]
        assert abs(g.cell_area_km2[i] - expect_area) < 1e-9, (mid, code)
    # and the cell areas must tile the basin exactly, not approximately
    assert abs(g.cell_area_km2.sum() - float(mb.area_km2.sum())) < 1e-6


@pytest.fixture(scope="module")
def basin_run(basin_geometry):
    if not DRIVERS.is_file():
        pytest.skip("frozen H2E driver bundle not present")
    drivers = sed.load_drivers(DRIVERS)
    assert np.array_equal(drivers.mini_ids, basin_geometry.mini_ids)
    res = sed.simulate_sediment(basin_geometry, sed.SedParams(), drivers.qsur_mm,
                                dates=drivers.dates, backend="collapsed")
    return drivers, res


@needs_csvs
@needs_drivers
def test_full_basin_decade_is_nan_free(basin_run):
    """NaN-free and non-negative over 3,652 days x 8,672 minibacias, plus per-cell totals."""
    drivers, res = basin_run
    assert res.delivered_t_day.shape == (3652, 8672)
    assert np.all(np.isfinite(res.delivered_t_day))
    assert np.all(res.delivered_t_day >= 0.0)
    assert np.all(np.isfinite(res.cell_eroded_t))
    assert np.all(np.isfinite(res.series["eroded"]))
    assert float(res.cell_eroded_t.min()) >= 0.0
    assert res.ledger["eroded_t"] > 0.0


@needs_csvs
@needs_drivers
def test_full_basin_decade_ledger_closes_exactly(basin_run):
    """The gate: eroded = delivered + stored, EXACTLY, over the whole record."""
    _, res = basin_run
    assert res.ledger["residual_t"] == 0.0
    assert res.ledger["exact"] is True
    assert res.ledger["delivered_t"] == res.ledger["eroded_t"]
    assert res.ledger["store_end_t"] == 0.0
    assert abs(float(res.cell_eroded_t.sum()) - res.ledger["eroded_t"]) \
        <= 1e-10 * res.ledger["eroded_t"]


@needs_csvs
@needs_drivers
def test_dry_and_inert_cells_are_exactly_zero_on_real_data(basin_geometry, basin_run):
    """Exactly-zero cases on the real basin: dry minibacia-days, and open-water URHs.

    Open water carries C = 0 by construction (``urh_cp_factors.csv``: "open water has no
    soil surface to detach"), so those cells must contribute exactly 0 tonnes over the whole
    decade - a tolerance would let a stray epsilon of erosion off a lake go unnoticed.

    MEASURED FACT this test pins: the registered driver ``qsur_rel_mm`` contains **no exact
    zeros at all** (fleet minimum 2.0e-43 mm/day), because it is the output of an
    exponential linear reservoir, which decays towards zero without ever arriving. So the
    exactly-zero-erosion gate cannot be exercised on the registered field; it is exercised
    on ``qsur_gen_mm``, the runoff GENERATED on the URH columns, which does contain exact
    zeros. Anyone who expects `Qsur == 0` days in ``qsur_rel_mm`` is wrong about the driver.
    """
    drivers, res = basin_run
    assert not np.any(drivers.qsur_mm == 0.0)
    assert float(drivers.qsur_mm.min()) > 0.0

    water = basin_geometry.cell_land_class() == 7
    assert water.any()
    assert np.all(res.cell_eroded_t[water] == 0.0)

    gen = sed.load_drivers(DRIVERS, qsur_field="qsur_gen_mm")
    q = gen.qsur_mm[:200]
    dry = q == 0.0
    assert dry.any(), "expected exact zeros in qsur_gen_mm"
    r = sed.simulate_sediment(basin_geometry, sed.SedParams(), q, dtype_out=np.float64)
    assert np.all(r.delivered_t_day[dry] == 0.0)


@needs_csvs
@needs_drivers
def test_backends_agree_on_one_real_year(basin_geometry):
    """Cross-check the fast path against the reference on 365 real days, all 8,672 units."""
    drivers = sed.load_drivers(DRIVERS)
    q = np.asarray(drivers.qsur_mm[:365], dtype=np.float64)
    p = sed.SedParams()
    a = sed.simulate_sediment(basin_geometry, p, q, backend="cells", dtype_out=np.float64)
    b = sed.simulate_sediment(basin_geometry, p, q, backend="collapsed", dtype_out=np.float64)
    assert abs(a.ledger["eroded_t"] - b.ledger["eroded_t"]) <= 1e-12 * a.ledger["eroded_t"]
    ok = np.isclose(a.delivered_t_day, b.delivered_t_day, rtol=1e-11, atol=0.0)
    assert ok.all(), f"{int((~ok).sum())} of {ok.size} cells disagree beyond 1e-11"
