# journal — H-C: transfer failure of the quantile map (CHIRPS-gauge merge volume gate)

Agent: `chirps-transfer`. Date: 2026-08-12. Repo `c:\dev\magdalena-mgb-sed`, branch `main`.
Journal file assigned to me: `docs/agents/journal_chirps-transfer.md` (this file, and no other).

## 0. What I was asked

Establish whether the +152.148 mm/yr volume surplus of the merged CHIRPS-gauge field
(2,188.540 vs gauge-only 2,036.393 mm/yr, 2009-2017) is caused by **H-C: transfer failure** —
the quantile map is FITTED at gauge pixels and APPLIED at ungauged cells, so a map that is
nearly mean-preserving on the distribution it was fitted to is not mean-preserving on the
(different) cell distribution. The already-measured fact that makes this the prime suspect:
the same maps lift CHIRPS by +3.1 % at the 291 gauge pixels (4.9626 -> 5.1182 mm/day against
observed G 5.1003) but by +6.6 % over the basin (2,124.721 -> 2,265.757 mm/yr).

Deliverables: (1) stratum table with gauges / area / `pool_level` actually used / contribution;
(2) the gauge-pixel-vs-cell raw-CHIRPS distribution gap and its relation to per-stratum surplus;
(3) a DIRECT held-out transfer test (in-sample vs out-of-sample bias); (4) the tail / low-end
anatomy of the map; (5) whether H-C explains the second channel (CHIRPS-vs-IDW +64.807).

Constraints I am operating under: no `git add/commit/push`; no edits to `docs/33`, `docs/30`,
`docs/18`, `docs/54`; no writes into `data/processed/model_inputs_v2/`, `sim_calibrated_v2/`;
no scripts in the repo (scratch only); `python3.10`, never `python`; ~2 GB free RAM, so the
full merged field must NOT be rebuilt.

## 1. Sources read before measuring anything

* `C:\Users\KNADE~1.MSI\AppData\Local\Temp\claude\c--dev-magdalena-mgb-sed\7fba197a-689b-47d5-9c29-1dc3e3af2581\scratchpad\h2_harvest.py`
  — the generating code for the ledger. Confirmed by reading it:
  - `band` is `np.digitize(elev, (500,1500,2500))` on the cached DEM elevations, cells and
    gauges alike (`elev_cache.npz`, asserted against gauge/minibacia order).
  - the per-cell day-sums are split by subset A (`~Cnan & ~gap`), B (`~Cnan & gap`),
    D (`Cnan`), and the decomposition identity
    `sMerged - sP == w*(sCmapA - sPA) + (sCmapB - sPB)` is asserted in the harvest itself.
  - `stratum_table.csv`'s `pool_level` is the key RETURNED by `pools.fit(band, zone)`, i.e.
    the pool the fallback hierarchy actually used; `own_*` are the `('bz',band,zone)` pool
    whether or not it was used. `qmap_ck_max`/`qmap_gk_max` are `qmap[0][-1]`/`qmap[1][-1]`
    of the pool ACTUALLY used, and `qmap_tail_scale = gk[-1]/ck[-1]`.
  - `gauge_ledger.mean_c_map` uses the basin-field map for that gauge's stratum with **no
    LOOCV holdout** — so it is an IN-SAMPLE number by construction. Important for task 3.
  - `qmap_pools.npz` stores `pairs[code]` concatenated in gauge-index order, which is the
    same order `QmapPools.members[...]` iterates, so the pools are exactly reconstructible.
* `c:\dev\magdalena-mgb-sed\src\merge_chirps_gauges.py` — `fit_qmap` (N_KNOTS=1001 empirical
  quantile knots, tied CHIRPS knots collapsed to the MEAN gauge knot via `np.unique` +
  `np.add.reduceat`), `apply_qmap` (`np.interp` inside the knots, `x*gk[-1]/ck[-1]` strictly
  ABOVE `ck[-1]`), `QmapPools.fit` (hierarchy `('bz',b,z)` -> `('z',z)` -> `('b',b)` ->
  `('all',)`, gated by MIN_GAUGES=3 and MIN_PAIRS=5000), `chirps_weight`
  (clip((d-10)/20,0,1)), `areal_mean` (365.25).

Label discrepancy noticed in passing, flagged for the H-A agent, not used by me:
`bounds_fields.csv` names fields F5/F6 "credited **0.414** x own reporting mean" while my
brief describes them as 0.4527. I do not rely on F5/F6 anywhere.

## 2. PRE-REGISTRATION of the held-out transfer test (written BEFORE running it)

I state the split rules and the metric now, before seeing any result, and I will report every
design I registered whichever way it comes out.

Metric, in all designs: for a held-out gauge j with paired station-days
`(g_j, c_j)` from `qmap_pools.npz`, the mapped-vs-observed **mean bias**
`bias_j = mean(apply_qmap(c_j, qmap_fit)) - mean(g_j)` in mm/day, and the relative form
`bias_j / mean(g_j)`. Aggregation over a set of gauges is **pair-weighted** (i.e. weighted by
`n_pairs`, equivalent to pooling station-days). "In-sample" means the same gauge's days were
in `qmap_fit`'s pool; "out-of-sample" means they were not.

* **D1 LOGO (leave-one-gauge-out).** For every one of the 291 gauges: out-of-sample map =
  `pools.fit(band_j, zone_j, exclude=code_j)` (the LOOCV protocol's own map); in-sample map =
  `pools.fit(band_j, zone_j)`. Report both biases and their difference. This is the cleanest
  paired in/out contrast and needs no arbitrary split.
* **D2 half-split, alternating (a neutral, non-directional split).** For every pool level
  actually used by >=1 stratum with >=6 gauges: sort member codes ascending as strings,
  fold 0 = even positions, fold 1 = odd positions. Fit on fold 0, apply to fold 1 and to
  fold 0; then swap. Report in-sample and out-of-sample bias per fold.
* **D3 elevation-directional.** Within each such pool, split its gauges at the pool's
  **median gauge elevation**; fit on the LOWER half and apply to the UPPER half, and the
  reverse. Predicted sign if H-C holds: transferring a map fitted low onto high-elevation
  targets should be biased, and the bias should follow the direction of the CHIRPS
  distribution shift between the halves.
* **D4 density-directional — the design that mirrors the basin situation.** Within each such
  pool, split its gauges at the pool's median `d_nearest_gauge_km`; fit on the DENSE half
  (small nearest-gauge distance) and apply to the SPARSE half. The basin analogue: the map is
  fitted where gauges cluster and applied at cells >=30 km from any gauge (the w=1 cells that
  carry 64.4 % of the surplus). I register in advance that D4 is the design I will weight most
  heavily for the verdict, and that a null result in D4 is a REFUTATION of the
  "different-location-same-stratum" form of H-C.
* Minimum sizes, registered now: a fold must have >=3 gauges and >=5,000 pairs (the same
  MIN_GAUGES / MIN_PAIRS the production code uses) or the pool is skipped and reported as
  skipped.

Stated limitation, registered now so it cannot be retrofitted: every one of D1-D4 measures
transfer **to another gauge pixel**. Cells are not gauge pixels, and the ungauged cells are by
construction the far-from-gauge ones. So D1-D4 can only bound the "same stratum, different
location" component of H-C. If they come out small, that does not by itself refute H-C at
cells — it localises H-C's cause to the cell-vs-gauge-pixel distribution difference, which
task 2 and task 4 measure directly.

## 3. Run log

### 3.1 `hc1_strata.py` — task 1 + per-stratum contribution (ledger only, no reload)

Executed output re-derived, from `cell_ledger.csv` alone, every headline number in my brief,
to the printed precision:

```
gauge-only P        2036.393     RAW CHIRPS 2124.720   MAPPED CHIRPS 2265.757   merged 2188.540
surplus merged-P     152.148   via contrib col    152.148
  MAP INFLATION blend  w*(CmapA-CrawA)   87.302
  CHIRPS-vs-IDW blend  w*(CrawA-PA)      64.807
  MAP INFLATION fallb  (CmapB-CrawB)      0.009
  CHIRPS-vs-IDW fallb  (CrawB-PB)         0.030
fallback cell-days 35,716 of 28,504,864 = 0.125 % | CHIRPS-missing cell-days 0
w=0    cells  2213  area  25.8 %  contrib    0.003   map   0.000  cvi   0.000
blend  cells  4963  area  57.1 %  contrib   54.200   map  35.068  cvi  19.115
w=1    cells  1496  area  17.1 %  contrib   97.944   map  52.235  cvi  45.692
```

No disagreement with the brief anywhere. (The +0.003 in the w=0 band is not a rounding
artefact: w=0 kills subset A exactly, so it is entirely the `sCmapB - sPB` fallback term,
which carries w_eff = 1 regardless of w.)

Task-1 result (full table in the return value; `hc_stratum_contrib.csv` written):
* 32 strata are present among the 8,672 cells. **17 use their own `('bz', band, zone)` pool;
  15 fall back to `('z', zone)`. Nothing falls back further** — `('b', band)` and `('all',)`
  are never used.
* fallback burden: 1,169 cells / 35,546.7 km2 = **13.48 % of cells, 13.83 % of area**, but
  **32.533 of the 152.148 mm/yr = 21.4 % of the surplus** (1.55x over-represented).
* five strata have `own_n_gauges == 0` — no gauge at all inside their own band x zone:
  (1,'Bajo Magdalena- Cauca -San Jorge'), (2,'BMCSJ'), (2,'Cesar'), (3,'Cesar'), (3,'Nechí').
  Sized in 3.2 below.

### 3.2 `hc2_transfer.py` — pools rebuilt from `qmap_pools.npz`, then the pre-registered
held-out test. Verification requirement I set for myself first: the rebuilt pools must
reproduce `stratum_table.csv`'s `qmap_ck_max`, `qmap_gk_max`, `pool_level`, `pool_n_gauges`
and `pool_n_pairs` exactly, or the transfer test is measuring a different map than the field.

Executed:
```
VERIFIED: rebuilt pools reproduce all 32 rows of stratum_table.csv (pool_level, n_gauges, n_pairs, ck[-1], gk[-1])
cross-check: max |m_in - gauge_ledger.mean_c_map| = 1.776e-15 mm/day
```
so the maps I test are byte-for-byte the field's maps.

D1 LOGO, 291 gauges / 926,268 pairs, pair-weighted:
```
  pooled observed gauge mean G        5.0550 mm/day
  pooled RAW CHIRPS at gauge pixels   4.9276 mm/day  (-2.52 % vs G)
  IN-SAMPLE  mapped                   5.0567 mm/day  bias +0.0017 (+0.03 %)
  OUT-OF-SAMPLE (LOGO) mapped         5.0709 mm/day  bias +0.0159 (+0.31 %)
  level changed under holdout for 0 gauges
    <5 km     n= 42 pairs=101,400  G 4.150  C_raw 3.812  bias_in -0.2998  bias_out -0.3061
    5-10 km   n= 59 pairs=174,160  G 4.572  C_raw 4.295  bias_in -0.2357  bias_out -0.2542
    10-20 km  n=125 pairs=431,428  G 4.958  C_raw 4.917  bias_in +0.0534  bias_out +0.0667
    >20 km    n= 65 pairs=219,280  G 6.047  C_raw 5.966  bias_in +0.2281  bias_out +0.2794
```
Note on weighting, so nobody thinks I contradict the brief: my 5.0550 / 4.9276 / 5.0567 are
PAIR-weighted (pooled station-days); the brief's 5.1003 / 4.9626 / 5.1182 are the UNWEIGHTED
means over the 291 gauges, which I reproduce too (printed in 3.3). Same data, two weightings.

D2/D3/D4 pool-split summary (pair-weighted over all folds):
```
D2 alt-halves        folds 40  IN  +0.0021 (+0.04 %)   OUT +0.0315 mm/day (+0.63 %)
D3 elev low->high    folds 40  IN  +0.0014 (+0.03 %)   OUT +0.0764 mm/day (+1.53 %)
D4 dense->sparse     folds 39  IN  +0.0018 (+0.04 %)   OUT +0.0451 mm/day (+0.91 %)
```
4 folds skipped for failing the registered minima (3 pools with <6 gauges: ('bz',0,'Cauca'),
('bz',3,'Cauca'), ('z','Saldaña'); plus ('bz',2,'Medio Magdalena') d>med with 2 gauges).
What I will NOT claim: that D2-D4 reproduce the basin's +6.6 % map inflation. They do not —
they are ten times smaller. What they DO establish is the sign and the driver: per-fold
`bias_out` is large (up to ±3.6 mm/day) and carries the SAME SIGN as `dC = C_apply - C_fit`,
antisymmetric under swapping the folds, so it cancels in the pooled average. The systematic
part only appears once the target distribution is systematically wetter than the fit pool's —
which is the basin situation, and is measured in 3.3.

### 3.3 `hc3_chirps.py` — CHIRPS reloaded at points (NOT the merged field)

The 8,672 cell centroids and 291 gauge pixels, via the production `m.load_chirps` (lag -1),
28 MB grid per year. Verification before any inference:
```
VERIFY reload: max |sum(Craw, gate) - ledger sCraw_all| = 7.276e-12 mm   -> 2124.720 mm/yr
VERIFY reload: max |sum(Cmap, gate) - ledger sCmap_all| = 7.276e-12 mm   -> 2265.757 mm/yr
```
The decisive distribution measurement:
```
    gauge pixels, PAIRED station-days only (the fit input) : 4.9276 mm/day
    gauge pixels, ALL 4018 days                            : 4.7024
    gauge pixels, ALL gate-window days                     : 4.6711
    cell centroids, ALL gate-window days (area-weighted)   : 5.8172
    -> day-subset (reporting) component  -0.2565
    -> LOCATION component (cells vs gauge pixels, same days) +1.1461  (+24.5 %)
```
Tail / low-end anatomy of the map channel (87.311 mm/yr by this split; ledger 87.302, the
-0.008 residual is the w_eff=1 uplift on the 0.125 % fallback days which the split charges at w):
```
  above ck[-1] (extrapolated tail):   0.491 mm/yr ( 0.6 %) on 678 cell-days (0.0024 %)
  CHIRPS-ZERO days (map(0) drizzle): 10.140 mm/yr (11.6 %) on 16,266,786 cell-days (57.07 %)
  inside the knots 0 < C <= ck[-1]:  76.688 mm/yr (87.8 %)
```
Ratio-map counterfactual: 87.311 as built vs 26.429 if the map only applied its own pool's
multiplicative lift mean_G/mean_C -> EXCESS 60.882 mm/yr (69.7 % of the map channel, 40.0 %
of the +152.148).

So the tail-extrapolation defect is REFUTED as a material channel (0.6 %), and the drizzle
defect is real but secondary (11.6 %). Next step, 3.4: the arithmetic reason for the 87.8 %
that sits inside the knots.

### 3.4 `hc4_arith.py` — the arithmetic reason. ONE ERROR OF MINE, CORRECTED IN PUBLIC.

My first version of this script asserted `E_pool[delta] = 0` ("empirical quantile mapping
preserves the fit pool's mean"). The run returned an identity residual of **+59.903 mm/yr**,
which is not a rounding error, so I did not paper over it: the assertion was WRONG. The map's
purpose is to move the pool's CHIRPS mean onto the pool's GAUGE mean, so
`E_pool[delta] = mean(G_pool) - mean(C_pool)` — the lift the pool itself calibrates, ranging
-0.712 .. +2.100 mm/day across the 32 strata. hc2's "in-sample bias ~0" is the correct
in-sample statement (`mean(T(C_pool)) - mean(G_pool) = +0.03 %`), and it is consistent.
Re-deriving with the corrected identity, the residual closed to **+0.00000**:

```
mapped-CHIRPS field lift                                +141.037 mm/yr  (= 2265.757-2124.720)
  CALIBRATED  SUM_s share_s * E_pool_s[delta]            +59.903 (42.5 %)
  EXCESS over it                                         +81.134 (57.5 %)
     of which MASS-SHIFT  SUM_b (p_cell-p_pool)*d_pool   +75.335 (92.9 % of the excess)
     of which WITHIN-BAND SUM_b p_cell*(d_cell-d_pool)     +5.799 ( 7.1 %)
```
delta() by raw-CHIRPS band, and the mass shift that meets it:
```
   band  p_cell_%  p_pool_%   dp_%   delta_pool(mm/d)   map_channel_w(mm/yr)
     =0    57.215    58.046  -0.831         +0.165              +10.140
    2-5     6.781     7.657  -0.876         -2.553              -28.728
   5-10    12.514    12.612  -0.097         -3.606              -76.188
  10-20    13.819    12.841  +0.977         -0.804              -14.396
  20-35     6.823     5.830  +0.993         +7.895             +106.021
  35-50     1.518     1.236  +0.282        +20.458              +63.149
  50-75     0.412     0.358  +0.054        +30.429              +24.949
```
(the dp/delta_pool columns are basin-level for legibility; the mass_shift total is summed
per-stratum, so the two are not the same aggregation and dp x delta_pool does not multiply
out band-by-band. The per-stratum sum is the exact one.)

### 3.5 `hc5_close.py` — the same split in the merged field's own w-weighted units

```
  map channel as built                                        87.311 mm/yr (100.0 %)
  A) if the map only added its pool's ADDITIVE lift (G-C)      26.459 (30.3 %) -> excess 60.851
  B) if the map only applied its pool's ratio mean_G/mean_C    26.429 (30.3 %) -> excess 60.882
```
Two independent mean-preserving counterfactuals agree to 0.03 mm/yr, so the H-C excess is
**+60.9 mm/yr = 40.0 % of the +152.148**, not a range I have to hedge.

Mechanism test, per stratum: `r(dC, excess) = +0.747` unweighted, **+0.762 area-weighted**,
slope +0.32 mm/day per mm/day. Every stratum with dC < -1 mm/day has a NEGATIVE excess; every
stratum with dC > +1 mm/day has a positive one. That is the deciding measurement.

Loose ends measured in the same run: the five zero-own-gauge strata (133 cells, 4,188.6 km2 =
1.63 % of basin) carry 11.873 mm/yr = 7.8 % of the surplus, 4.8x over-represented per unit
area. Tail scale spans 0.590..2.607 but only 678 cell-days (0.0024 %) exceed ck[-1].
Both weightings of the gauge-pixel means reproduced (unweighted 5.1003/4.9626/5.1182 = the
brief's; pair-weighted 5.0550/4.9276).

## 4. What I refuse to claim

1. **That the held-out gauge tests reproduce the basin's +6.6 %.** They do not (D2 +0.63 %,
   D3 +1.53 %, D4 +0.91 %). I registered in §2 that D1-D4 can only bound the
   same-stratum-different-gauge-pixel component, and that is what happened. The verdict rests
   on 3.4/3.5, not on D1-D4.
2. **That the drizzle defect (+10.140 mm/yr) causes the gate failure.** It does not: the =0
   band contributes only +0.358 of the +81.134 excess, because the fitting pools have a
   similar dry fraction and so receive the same drizzle in-sample. It is a physical-realism
   defect (up to 1.06 mm/day invented on every CHIRPS-dry day in the Saldaña strata = 272
   mm/yr at those cells) that a rainfall-erosivity or runoff-generation term would feel, but
   it is not the volume mechanism. Reporting it as both would double-count.
3. **That the tail rescale matters.** 0.6 % of the map channel on 0.0024 % of cell-days.
   Refuted as a material channel, though present and up to 2.607x in the Cesar/BMCSJ pools.
4. **That H-C explains the +64.807 CHIRPS-vs-IDW channel.** The map is not in that term.
5. **That the +24.5 % location gap means CHIRPS is right about the ungauged interior.** It is
   not decidable from gauges: there is no observation there. At the 291 places we CAN check,
   raw CHIRPS is -2.52 % against the gauges (pair-weighted).

## 5. Gate-design observation, flagged under the project's uncited-band rule

`src/merge_chirps_gauges.py:95` sets `VOLUME_TOL = 0.01` with no citation anywhere in the
file, and I found no stated basis for the +/-1 % in docs/18 §15.1 or docs/33 §1 (the only
places the band is written down: docs/33 §116 gives the interval [2,016.0, 2,056.8]). The
target 2,036.4 is the v2 gauge-only field's OWN areal mean (docs/18 §14). I am not
relitigating a frozen pre-registration and I take no decision on it; I record only the
measured structural fact, because it bears on how my numbers should be read: the gate asks
the merged field to agree with the gauge-only field it is meant to improve, so any field that
adds information about the 74.2 % of basin area more than 10 km from a gauge fails the gate
unless that information happens to be volume-neutral. Per the docs/40 precedent this is a
matter for the synthesis agent and the advisor, not for me.

## 6. Not settled

* Whether the +1.1461 mm/day (+24.5 %) cell-vs-gauge-pixel CHIRPS gap is real orography or
  CHIRPS error in the ungauged interior. Not identifiable from this basin's gauge network.
* Whether a quantile map fitted on the CELLS' own CHIRPS quantiles (transporting the cell
  distribution onto the pool's gauge distribution) would pass the volume gate. That is a
  different estimator, not a diagnosis, and I did not build it — I only note that by
  construction it would put the mapped cell mean at the pool's gauge mean rather than
  +6.6 % above the cells' raw CHIRPS mean.
* The `bounds_fields.csv` credit-factor label (0.414 in the file vs 0.4527 in my brief).
  Not my hypothesis; flagged for whoever owns H-A.

Files written (all in the scratchpad, none in the repo): `hc1_strata.py`, `hc2_transfer.py`,
`hc3_chirps.py`, `hc4_arith.py`, `hc5_close.py`, `hc_stratum_contrib.csv`, `hc_logo.csv`,
`hc_splits.csv`, `hc_stratum_full.csv`, `hc_bands.csv`, `hc_delta_shape.csv`.
No `git add/commit/push`. No repo file modified except this journal.
