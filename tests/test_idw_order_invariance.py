"""Order-invariance of the gauge->minibacia IDW on a synthetic network.

Six gauges, two of which share EXACT coordinates -- the distance tie that made the
production IDW order-dependent (docs/23 s11). Values are random and the co-located
pair disagrees day by day, so a column-order-dependent tie-break would change the
field. k=3 (< number of gauges) so the neighbour SET, not just the summation order,
depends on the tie-break.
"""
import numpy as np
import pandas as pd

from idw_forcing import assert_order_invariant, idw_field

N_DAYS = 40
K = 3
K_FALLBACK = 6


def _synthetic():
    rng = np.random.default_rng(42)
    codes = ["21205791", "21206570", "24010140", "24030590", "27015070", "35010500"]
    glat = np.array([5.0, 5.0, 4.6, 5.4, 4.8, 5.2])      # gauges 0 and 1 co-located
    glon = np.array([-74.0, -74.0, -74.3, -73.7, -73.9, -74.2])
    vals = rng.gamma(0.8, 6.0, size=(N_DAYS, len(codes))).astype("float32")
    vals[rng.random(vals.shape) < 0.25] = np.nan          # silent-gauge days
    W = pd.DataFrame(vals, columns=codes)
    lat = np.linspace(4.5, 5.5, 5)
    lon = np.linspace(-74.4, -73.6, 5)
    grid_lat, grid_lon = np.meshgrid(lat, lon)
    return W, glat, glon, grid_lat.ravel(), grid_lon.ravel()


def test_assert_order_invariant_passes_with_colocated_gauges():
    W, glat, glon, clat, clon = _synthetic()
    # raises AssertionError if any shuffled column order changes a single cell
    assert_order_invariant(W, glat, glon, clat, clon, n_shuffle=8, seed=1,
                           k=K, k_fallback=K_FALLBACK)


def test_shuffled_columns_give_byte_identical_field():
    W, glat, glon, clat, clon = _synthetic()
    ref, ref_gap = idw_field(W, glat, glon, clat, clon, k=K, k_fallback=K_FALLBACK)
    lat = pd.Series(glat, index=W.columns)
    lon = pd.Series(glon, index=W.columns)
    rng = np.random.default_rng(7)
    for _ in range(5):
        perm = list(rng.permutation(list(W.columns)))
        got, gap = idw_field(
            W.reindex(columns=perm),
            lat.reindex(perm).to_numpy(), lon.reindex(perm).to_numpy(),
            clat, clon, k=K, k_fallback=K_FALLBACK,
        )
        assert gap == ref_gap
        assert np.array_equal(got, ref, equal_nan=True), \
            "shuffled gauge columns changed the interpolated field"
