"""Deterministic gauge->minibacia IDW, and the co-located-gauge handling it needs.

Extracted from notebook 11 section 3 so that nb11, the diagnostics and any re-run share
ONE interpolator instead of three copies. Two defects found in docs/18 s10.7 are fixed
here; both were invisible until a rebuild was compared cell by cell against the stored
field.

DEFECT 1 - THE IDW WAS NOT ORDER-INVARIANT
------------------------------------------
nb11 selected the k nearest gauges with `np.argsort(D, axis=1)`. Four gauge pairs sit at
the same coordinates to within 0.1 m, so their distances to every minibacia TIE, and
argsort then resolves the neighbour set by column index. nb11 happens to feed columns in
the QC inventory's row order; sorting them by code instead - a change no reviewer would
flag - moves 44 of 8,672 minibacias by up to 13.1 mm/day.

`neighbour_order()` breaks ties on the gauge CODE via `np.lexsort`, so the neighbour set
is a property of the data and not of the column order. `assert_order_invariant()` proves
it by shuffling the columns and demanding a byte-identical field; that assertion, not the
lexsort, is the actual guarantee.

DEFECT 2 - CO-LOCATED GAUGES WERE DOUBLE-WEIGHTED
-------------------------------------------------
A deterministic tie-break does NOT fix this: two gauges at one point still receive two
weights of `1/max(d,1)**2`, so that location carries twice the influence of a single
gauge on the days both report.

But a blanket "merge everything within 500 m" rule would destroy real data. Measuring the
four pairs on the days they BOTH report splits them into three different situations:

  identical on overlap (corr 1.000, mean |diff| 0.00 mm)
      27015070 / 27015330    AEROPUERTO OLAYA HERRERA   233 overlap days, 233 identical
      24010140 / 2401500040  CUCUNUBA / CUCUNUBA-AUT    366 overlap days, 364 identical
      -> ONE measurement filed under two codes. Merging is pure de-duplication.

  no overlap at all, adjacent spans
      24030590 / 24035420    CERINZA   0 overlap; 2008-01..2009-06 then 2009-07..2018-12
      -> a sequential instrument REPLACEMENT. Merging reconstructs one continuous record
         from two fragments, which is strictly better than interpolating between them.

  overlap with genuine disagreement
      21205791 / 21206570    EL DORADO CATAM / AEROPUERTO CATAM
                             1,470 overlap days, only 470 identical, mean |diff| 1.91 mm,
                             corr 0.756
      -> these are TWO REAL GAUGES and the catalogue coordinates are wrong for one of
         them. A correlation of 0.756 at a nominal separation of 0.1 m is not physical:
         true duplicates here read 1.000. NOT merged. Flagged instead, because merging
         would average away a real second observation, and silently.

So the rule is evidence-based per cluster rather than distance-based, and the evidence is
the agreement on overlap days. `classify_colocated()` returns that classification with the numbers
attached in a `do_merge` column - not `merge`, which would shadow `DataFrame.merge` and
silently return a bound method on attribute access. `merge_colocated()` acts only on the
first two categories.

Merge mechanics: on a day where several members report, the value from the highest
approval level wins (`Definitivo > En revision > Preliminar`, the same precedence
`build_precip_gauges.py` uses for duplicate station-days). Where levels tie the first is
taken, which is immaterial here: `duplicate` members agree to 0.00 mm on their overlap
days and `sequential` members never share one. The surviving code is the member with the
most records, so provenance stays traceable.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

APPROVAL_RANK = {"Definitivo": 0, "En revisión": 1, "En revision": 1, "Preliminar": 2,
                 "Inferido_seco": 3}
COLOCATED_M = 500.0        # sweep radius; exact ties were only how the defect announced itself
IDENTICAL_MM = 0.05        # mean |difference| below this on overlap days = one instrument
IDENTICAL_CORR = 0.99


def km(la1, lo1, la2, lo2):
    """nb11's local flat-earth distance, kept identical so fields stay comparable."""
    return np.sqrt(((la1 - la2) * 111.0) ** 2
                   + ((lo1 - lo2) * 111.0 * np.cos(np.radians((la1 + la2) / 2))) ** 2)


def neighbour_order(D: np.ndarray, codes: list[str]) -> np.ndarray:
    """Row-wise neighbour ranking of the (minibacia, gauge) distance matrix `D`.

    Primary key distance, secondary key gauge code. The secondary key is what makes the
    result independent of the column order when distances tie.
    """
    rank = np.empty(len(codes), dtype=np.int64)
    rank[np.argsort(np.asarray(codes, dtype=object), kind="stable")] = np.arange(len(codes))
    sec = np.broadcast_to(rank, D.shape)
    return np.lexsort(np.stack([sec, D]), axis=-1)


def idw_field(W: pd.DataFrame, glat, glon, clat, clon, k: int = 6,
              k_fallback: int = 20) -> tuple[np.ndarray, int]:
    """Masked inverse-distance-squared interpolation, nb11's scheme with a stable tie-break.

    `W` is (days x gauges); NaN means the gauge did not report, and only reporting gauges
    contribute on a given day, so a silent gauge neither propagates NaN nor implies zero.
    Cells where all `k` nearest gauges were silent are refilled from a `k_fallback` pass.
    Returns (field, n_fallback_cells).
    """
    codes = list(W.columns)
    Gv = W.to_numpy("float32")
    obs = ~np.isnan(Gv)
    Gf = np.where(obs, Gv, 0.0).astype("float32")
    D = km(np.asarray(clat)[:, None], np.asarray(clon)[:, None],
           np.asarray(glat)[None, :], np.asarray(glon)[None, :])
    srt = neighbour_order(D, codes)
    n_mb = D.shape[0]

    def pass_k(kk):
        nb = srt[:, :kk]
        wt = (1.0 / np.maximum(np.take_along_axis(D, nb, 1), 1.0) ** 2).astype("float32")
        out = np.full((len(W), n_mb), np.nan, dtype="float32")
        for a in range(0, n_mb, 500):
            b = min(a + 500, n_mb)
            i2, w2 = nb[a:b], wt[a:b]
            num = (Gf[:, i2] * w2).sum(2)
            den = (obs[:, i2] * w2).sum(2)
            with np.errstate(invalid="ignore", divide="ignore"):
                out[:, a:b] = np.where(den > 0, num / den, np.nan)
        return out

    P = pass_k(k)
    gap = np.isnan(P)
    n_gap = int(gap.sum())
    if n_gap:
        P = np.where(gap, pass_k(k_fallback), P)
    return P, n_gap


def assert_order_invariant(W, glat, glon, clat, clon, n_shuffle: int = 5, seed: int = 0,
                           **kw) -> None:
    """Shuffle the gauge columns and require a byte-identical field.

    This is the real guarantee. The lexsort is only the mechanism; without this assertion
    nothing stops a future edit reintroducing an order-dependent field.
    """
    ref, ref_gap = idw_field(W, glat, glon, clat, clon, **kw)
    rng = np.random.default_rng(seed)
    lat = pd.Series(np.asarray(glat), index=W.columns)
    lon = pd.Series(np.asarray(glon), index=W.columns)
    for i in range(n_shuffle):
        perm = list(rng.permutation(list(W.columns)))
        Ws = W.reindex(columns=perm)
        got, gap = idw_field(Ws, lat.reindex(perm).to_numpy(), lon.reindex(perm).to_numpy(),
                             clat, clon, **kw)
        if gap != ref_gap or not np.array_equal(got, ref, equal_nan=True):
            n_bad = int((~np.isclose(got, ref, equal_nan=True)).sum())
            raise AssertionError(
                f"IDW is order-dependent: shuffle {i+1} changed {n_bad:,} cells "
                f"(fallback cells {gap} vs {ref_gap})")


def classify_colocated(inv: pd.DataFrame, daily: pd.DataFrame,
                       max_m: float = COLOCATED_M) -> pd.DataFrame:
    """Find gauge clusters within `max_m` and classify each pair from its overlap days."""
    g = inv.dropna(subset=["lat", "lon"]).reset_index(drop=True)
    lat, lon = g.lat.to_numpy(float), g.lon.to_numpy(float)
    D = km(lat[:, None], lon[None, :], lat[None, :], lon[:, None])
    np.fill_diagonal(D, np.inf)
    ser = {c: s.set_index("date")["precip_mm"] for c, s in daily.groupby("code")}
    rows = []
    for i, j in zip(*np.where(np.triu(D < max_m / 1000.0, 1))):
        a, b = g.code[i], g.code[j]
        sa, sb = ser.get(a), ser.get(b)
        if sa is None or sb is None:
            continue
        both = sa.index.intersection(sb.index)
        n_both = len(both)
        if n_both == 0:
            kind, mad, corr = "sequential", np.nan, np.nan
        else:
            d = (sa.reindex(both) - sb.reindex(both)).abs()
            mad = float(d.mean())
            corr = float(sa.reindex(both).corr(sb.reindex(both))) if n_both > 2 else np.nan
            kind = ("duplicate" if mad <= IDENTICAL_MM
                    and (np.isnan(corr) or corr >= IDENTICAL_CORR) else "coord_error")
        rows.append(dict(a=a, b=b, dist_m=float(D[i, j] * 1000), n_a=len(sa), n_b=len(sb),
                         n_both=n_both, mean_abs_diff_mm=mad, corr=corr, kind=kind,
                         do_merge=kind in ("duplicate", "sequential")))
    return pd.DataFrame(rows).sort_values("dist_m").reset_index(drop=True)


def merge_colocated(daily: pd.DataFrame, inv: pd.DataFrame,
                    cls: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Collapse every mergeable cluster into its highest-coverage code.

    Returns (daily, inventory, log). Pairs classified `coord_error` are left untouched -
    they are two real gauges with one bad coordinate, and averaging them would erase an
    observation. They stay in the log so the defect is visible.
    """
    parent: dict[str, str] = {}

    def find(x):
        while parent.get(x, x) != x:
            x = parent[x]
        return x

    n_rec = daily.groupby("code").size()
    for _, r in cls[cls["do_merge"]].iterrows():
        ra, rb = find(r.a), find(r.b)
        if ra == rb:
            continue
        keep, drop = (ra, rb) if n_rec.get(ra, 0) >= n_rec.get(rb, 0) else (rb, ra)
        parent[drop] = keep
    groups = {c: find(c) for c in daily.code.unique() if find(c) != c}
    if not groups:
        return daily, inv, pd.DataFrame()

    cluster = set(groups) | set(groups.values())
    d = daily.copy()
    d["_target"] = d.code.map(lambda c: groups.get(c, c))
    d["_rank"] = d.approval.map(APPROVAL_RANK).fillna(9).astype(int)
    in_cl = d.code.isin(cluster)
    # highest approval level wins the day; the members classified `duplicate` are identical
    # on their overlap days anyway (mean |diff| 0.00 mm), so first-vs-mean is immaterial
    # there, and `sequential` members never share a day at all.
    coll = (d.loc[in_cl, ["_target", "date", "_rank", "precip_mm", "approval"]]
            .sort_values(["_target", "date", "_rank"])
            .groupby(["_target", "date"], as_index=False)
            .first()
            .rename(columns={"_target": "code"})[["code", "date", "precip_mm", "approval"]])
    out = (pd.concat([d.loc[~in_cl, ["code", "date", "precip_mm", "approval"]], coll],
                     ignore_index=True)
           .sort_values(["code", "date"]).reset_index(drop=True))

    log = pd.DataFrame([dict(dropped=k, merged_into=v) for k, v in groups.items()])
    inv2 = inv[~inv.code.isin(groups)].copy()
    return out, inv2, log
