"""Unit tests for the registered MUSLE ``q_peak`` proxy (``scripts/c3/qpeak.py``).

The pre-registration is ``docs/35_qpeak_preregistration.md``. These tests pin the two
things that must not drift silently: (a) the proxy's arithmetic, against a case computed
by hand, and (b) the numbers docs/35 quotes -- the bias column (§5.2), the scale-factor
table (§6.2) and the C4 hard stops (§6.1, §6.3). If a test here fails, either the code
changed or docs/35 did; reconcile them, do not relax the test.
"""

import pathlib
import sys

import numpy as np
import pytest

C3 = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "c3"
if str(C3) not in sys.path:
    sys.path.insert(0, str(C3))

import qpeak as qp  # noqa: E402


# ---------------------------------------------------------------------------
# The registered proxy: hand-computed case, zero, monotonicity, arrays
# ---------------------------------------------------------------------------

def test_hand_computed_single_cell():
    """10 mm over 25 km2 in one day.

    By hand: 0.010 m * 25e6 m2 = 250,000 m3 of water; 250,000 / 86,400 s
    = 2.893518518518... m3/s. Equivalently 10 * 25 / 86.4.
    """
    got = qp.qpeak_daily_mean(10.0, 25.0)
    assert got == pytest.approx(250_000.0 / 86_400.0, rel=0, abs=1e-12)
    assert got == pytest.approx(2.8935185185185186, abs=1e-12)


def test_hand_computed_unit_case_is_the_86_4_constant():
    """1 mm/day over 1 km2 is exactly 1/86.4 m3/s -- Buarque (2015) eq. 7's constant."""
    assert qp.qpeak_daily_mean(1.0, 1.0) == pytest.approx(1.0 / 86.4, abs=1e-15)


def test_hand_computed_at_the_registered_pixel_scale():
    """The registered application unit: one COP90 pixel, 90 m x 90 m = 0.0081 km2."""
    got = qp.qpeak_daily_mean(10.0, qp.COP90_PIXEL_AREA_KM2)
    # 0.010 m * 8100 m2 = 81 m3 per day / 86400 s
    assert got == pytest.approx(81.0 / 86_400.0, abs=1e-15)


def test_zero_runoff_gives_zero_peak():
    assert qp.qpeak_daily_mean(0.0, 25.0) == 0.0
    assert qp.qpeak_daily_mean(0.0, qp.COP90_PIXEL_AREA_KM2) == 0.0
    assert np.all(qp.qpeak_daily_mean(np.zeros(7), 25.0) == 0.0)


def test_zero_area_gives_zero_peak():
    assert qp.qpeak_daily_mean(10.0, 0.0) == 0.0


def test_strictly_monotonic_in_qsur():
    q = np.array([0.0, 0.755, 1.803, 5.104, 11.354, 18.619, 74.392])  # docs/35 §1 quantiles
    peaks = qp.qpeak_daily_mean(q, 25.58)
    assert np.all(np.diff(peaks) > 0.0)
    # and doubling the runoff exactly doubles the peak (it is linear, by construction)
    assert qp.qpeak_daily_mean(2.0, 25.0) == pytest.approx(
        2.0 * qp.qpeak_daily_mean(1.0, 25.0), abs=1e-15
    )


def test_strictly_monotonic_in_area():
    a = np.array([0.0081, 0.544, 4.762, 24.485, 25.58, 313.45])
    peaks = qp.qpeak_daily_mean(5.0, a)
    assert np.all(np.diff(peaks) > 0.0)


def test_array_path_matches_scalar_path_and_broadcasts():
    q = np.array([0.0, 1.0, 10.0, 74.392])
    a = np.array([0.0081, 4.762, 25.58, 313.45])
    vec = qp.qpeak_daily_mean(q, a)
    scal = np.array([qp.qpeak_daily_mean(float(qi), float(ai)) for qi, ai in zip(q, a)])
    assert np.allclose(vec, scal, rtol=0, atol=1e-15)
    grid = qp.qpeak_daily_mean(q[:, None], a[None, :])
    assert grid.shape == (4, 4)
    assert grid[2, 3] == pytest.approx(qp.qpeak_daily_mean(10.0, 313.45), abs=1e-15)


def test_negative_inputs_are_rejected_not_silently_used():
    with pytest.raises(ValueError):
        qp.qpeak_daily_mean(-1.0, 25.0)
    with pytest.raises(ValueError):
        qp.qpeak_daily_mean(10.0, -25.0)
    with pytest.raises(ValueError):
        qp.qpeak_daily_mean(np.array([1.0, -0.001]), 25.0)


def test_nan_propagates_and_is_not_turned_into_zero():
    got = qp.qpeak_daily_mean(np.array([np.nan, 10.0]), 25.0)
    assert np.isnan(got[0])
    assert got[1] == pytest.approx(2.8935185185185186, abs=1e-12)


# ---------------------------------------------------------------------------
# The rejected alternative -- kept so the docs/35 §5.1 bound is reproducible
# ---------------------------------------------------------------------------

def test_scs_triangular_reduces_to_the_textbook_0_208_coefficient():
    """2V/T_b with T_b = 2.67 T_p is the familiar 0.208 * A * Q / T_p."""
    coefficient = 2.0 * 1000.0 / (qp.SCS_TIME_BASE_RATIO * 3600.0)
    assert coefficient == pytest.approx(0.2081, abs=5e-5)
    assert qp.qpeak_scs_triangular(1.0, 1.0, 1.0) == pytest.approx(coefficient, abs=1e-12)


def test_peak_amplification_is_exactly_the_ratio_of_the_two_proxies():
    for tp in (3.0, 4.0, 6.0, 9.0, 12.0, 18.0):
        ratio = qp.qpeak_scs_triangular(7.3, 4.762, tp) / qp.qpeak_daily_mean(7.3, 4.762)
        assert ratio == pytest.approx(qp.peak_amplification(tp), rel=1e-12)


def test_peak_amplification_reproduces_the_docs35_table():
    # docs/35 §3 / §5.1: 17.978 / T_p
    expected = {3.0: 5.99, 4.0: 4.49, 6.0: 2.99, 9.0: 2.00, 12.0: 1.50, 18.0: 1.00}
    for tp, want in expected.items():
        assert qp.peak_amplification(tp) == pytest.approx(want, abs=0.01)


def test_scs_exceeds_the_daily_mean_for_any_storm_shorter_than_a_day():
    """The registered proxy is a FLOOR: any concentrated hydrograph peaks above it."""
    for tp in (1.0, 3.0, 6.0, 12.0, 17.9):
        assert qp.qpeak_scs_triangular(5.0, 25.0, tp) > qp.qpeak_daily_mean(5.0, 25.0)


def test_kirpich_time_of_concentration_hand_case_and_monotonicity():
    # t_c = 0.0195 * L[m]^0.77 * S^-0.385 minutes, converted to hours
    tc = qp.time_of_concentration_kirpich(5.074, 0.01)  # median reach_km, 1 % slope
    expected_min = 0.0195 * (5074.0 ** 0.77) * (0.01 ** -0.385)
    assert tc == pytest.approx(expected_min / 60.0, rel=1e-12)
    # longer reach -> slower; steeper -> faster
    assert qp.time_of_concentration_kirpich(19.889, 0.01) > tc
    assert qp.time_of_concentration_kirpich(5.074, 0.10) < tc


def test_kirpich_rejects_the_outlet_zero_reach_and_zero_slope():
    """topology.npz:reach_km has exactly one zero (the outlet); it must not pass silently."""
    with pytest.raises(ValueError):
        qp.time_of_concentration_kirpich(0.0, 0.01)
    with pytest.raises(ValueError):
        qp.time_of_concentration_kirpich(5.074, 0.0)


# ---------------------------------------------------------------------------
# The scale trap (docs/35 §6.2)
# ---------------------------------------------------------------------------

def test_scale_factor_is_one_at_the_registered_pixel_scale():
    assert qp.musle_scale_factor(qp.COP90_PIXEL_AREA_KM2) == pytest.approx(1.0, abs=1e-12)
    assert qp.rescale_alpha_reference(qp.COP90_PIXEL_AREA_KM2) == pytest.approx(
        qp.WILLIAMS_ALPHA, abs=1e-12
    )


def test_scale_factor_reproduces_the_docs35_table():
    # docs/35 §6.2, measured on this basin's own geometry
    for area, want in ((0.544, 1.657), (4.762, 2.149), (25.58, 2.630), (313.45, 3.552)):
        assert qp.musle_scale_factor(area) == pytest.approx(want, abs=0.002)
    for area, want in ((4.762, 5.49), (25.58, 4.49), (313.45, 3.32)):
        assert qp.rescale_alpha_reference(area) == pytest.approx(want, abs=0.01)


def test_scale_factor_is_the_aggregation_identity_it_claims_to_be():
    """Summing MUSLE over N pixels vs applying it once to the lumped area, uniform Qsur."""
    beta, qsur, area = qp.WILLIAMS_BETA, 8.0, 4.762
    ap = qp.COP90_PIXEL_AREA_KM2
    n = area / ap
    pixelwise = n * (qsur * qp.qpeak_daily_mean(qsur, ap) * ap) ** beta
    lumped = (qsur * qp.qpeak_daily_mean(qsur, area) * area) ** beta
    assert lumped / pixelwise == pytest.approx(qp.musle_scale_factor(area), rel=1e-10)


# ---------------------------------------------------------------------------
# The bias arithmetic (docs/35 §5.2)
# ---------------------------------------------------------------------------

def test_sediment_bias_ratio_reproduces_the_docs35_column():
    cases = {
        0.820: 0.8948,   # R_AMS fleet median
        0.810: 0.8887,   # R_AMS geometric mean
        0.847: 0.9112,   # R_Q1
        0.975: 0.9859,   # R_Q5
        0.808: 0.8875,   # La Nina 2011
        0.686: 0.8097,   # El Nino 2015-16
    }
    for r, want in cases.items():
        assert qp.sediment_bias_ratio(r) == pytest.approx(want, abs=5e-5)


def test_enso_contrast_inflation_is_the_registered_ten_percent():
    inflation = qp.sediment_bias_ratio(0.808) / qp.sediment_bias_ratio(0.686)
    assert inflation == pytest.approx(1.096, abs=0.001)


def test_bias_ratio_is_one_at_no_bias_and_monotonic():
    assert qp.sediment_bias_ratio(1.0) == pytest.approx(1.0, abs=1e-15)
    r = np.array([0.25, 0.5, 0.686, 0.82, 1.0, 1.2])
    assert np.all(np.diff(qp.sediment_bias_ratio(r)) > 0.0)


# ---------------------------------------------------------------------------
# The C4 anti-compensation rule (docs/35 §6)
# ---------------------------------------------------------------------------

def test_williams_starting_values_pass():
    out = qp.check_musle_parameters(qp.WILLIAMS_ALPHA, qp.WILLIAMS_BETA)
    assert out["status"] == "ok"
    assert out["reasons"] == []


def test_alpha_far_above_williams_hard_stops():
    out = qp.check_musle_parameters(40.0, 0.56)
    assert out["status"] == "STOP"
    assert any("hard stop" in r for r in out["reasons"])


def test_alpha_in_the_watch_band_is_flagged_not_stopped():
    out = qp.check_musle_parameters(28.0, 0.56)
    assert out["status"] == "watch"
    assert out["reasons"]


def test_alpha_far_below_williams_hard_stops():
    assert qp.check_musle_parameters(2.0, 0.56)["status"] == "STOP"


def test_beta_above_the_registered_ceiling_hard_stops():
    out = qp.check_musle_parameters(11.8, 0.70)
    assert out["status"] == "STOP"
    assert any("missing flood events" in r for r in out["reasons"])


def test_beta_below_the_registered_floor_hard_stops():
    assert qp.check_musle_parameters(11.8, 0.40)["status"] == "STOP"


def test_the_scale_trap_fires_on_a_lumped_fit_that_looks_textbook():
    """alpha = 12 is perfect at pixel scale and an over-fit at minibacia scale."""
    assert qp.check_musle_parameters(12.0, 0.56)["status"] == "ok"
    lumped = qp.check_musle_parameters(12.0, 0.56, area_km2=25.58)
    assert lumped["status"] == "watch"
    assert lumped["alpha_band"]["reference"] == pytest.approx(4.49, abs=0.01)
    # and a genuinely large lumped alpha stops
    assert qp.check_musle_parameters(20.0, 0.56, area_km2=25.58)["status"] == "STOP"


def test_registered_constants_match_docs35():
    assert qp.WILLIAMS_ALPHA == 11.8
    assert qp.WILLIAMS_BETA == 0.56
    assert qp.ALPHA_EXPECTED_LOW == pytest.approx(5.9)
    assert qp.ALPHA_EXPECTED_HIGH == pytest.approx(23.6)
    assert qp.ALPHA_HARD_STOP_HIGH == pytest.approx(35.4)
    assert qp.ALPHA_HARD_STOP_LOW == pytest.approx(3.9333, abs=1e-3)
    assert (qp.BETA_HARD_STOP_LOW, qp.BETA_HARD_STOP_HIGH) == (0.45, 0.65)
