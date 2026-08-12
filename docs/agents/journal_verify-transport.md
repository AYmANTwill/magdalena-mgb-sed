# journal — `verify-transport`

Agent task: adversarially verify the correctness of the C4.1 channel-transport implementation
(`src/mgb_transport.py`, `tests/test_transport.py`) **by measurement**, not by reading.

Lens: correctness. Scope of the probes given to me:
(a) mass conservation at zero deposition, (b) topological order invariance,
(c) the `load_network(mini_ids=...)` guard actually firing, (d) zero-deposition default being
*detectably* deposition-free in the audit output, (e) silent failures / swallowed exceptions /
fallbacks that could make a wrong run look right.

Rules I am bound by: no commits, no edits to adopted config, no rewriting docs. Scratch files go
to the system temp dir, not the repo.

---

## Log

### 2026-08-11 — orientation
- Read `CLAUDE.md`, `docs/00_INDEX.md`, `src/mgb_transport.py` (985 lines), `tests/test_transport.py` (605 lines).
- `python` and `python3.10` both resolve to Python 3.10.11 here.
- Next: run the test suite as given.

### Test suite as given
`python -m pytest tests/test_transport.py -q` → **42 passed, 1 warning, 46.50 s**. The warning is
`mgb_sediment.load_geometry`'s known URH-area disagreement (12.9 % of cells >5 %), not a transport
issue.

### PROBE (a) — mass conservation, measured independently of the module's own ledger
Script: scratchpad `probe_a_mass.py`. Builds its own random DAGs (not the test file's networks),
computes the reference input total with `math.fsum` on the **raw load array**, and the export with
`fsum` on `outlet_t_day` + `deposited_t` + `state.store_t`. Residual = in − out − dep − store.

| network | loads | residual (t) | rel | ULP |
|---|---|---|---|---|
| synthetic n=37, 5 outlets, levels backend | integer | **0.0** | 0 | 0 |
| synthetic n=37, **order** backend | integer | **0.0** | 0 | 0 |
| synthetic n=37 | lognormal σ=4 | **0.0** | 0 | 0 |
| synthetic n=4000, 321 outlets, 15 levels | integer | **0.0** | 0 | 0 |
| synthetic n=4000 | lognormal σ=3 | **0.0** | 0 | 0 |
| synthetic n=37, 1e18 + 1e−12 (cancellation bait) | mixed | **0.0** | 0 | 0 |
| **REAL basin n=8672, 291 levels** | integer | **0.0** | 0 | 0 |
| **REAL basin n=8672**, levels backend | lognormal σ=3 | **−1.1920928955078125e-07** | 2.656e-16 | **2** |
| **REAL basin n=8672**, order backend | lognormal σ=3 | **−5.960464477539063e-08** | 1.328e-16 | **1** |

Verdict: mass conserves. On real-valued loads the residual is 1–2 ULP of the input total, i.e.
exactly the cross-reach re-association rounding the module docstring predicts in advance and
reports as `ledger['residual_relative']`. `max_node_residual_t` was **0.0** in every single case.

### PROBE (b) — topological order
Script: `probe_b_order.py`.
- **B1** real basin: of **8,671** linked edges, **0** have the receiver before a contributor in
  `net.order`; **0** have `level[receiver] <= level[contributor]`; the levels packing covers all
  8,672 nodes exactly once; **0** level-packings target a receiver that is not strictly deeper.
  Sweep depth 291 (292 distinct levels).
- **B2 order invariance**: relabelled the internal indices with 200 random permutations (loads
  permuted identically) at three parameter sets. `max |Δ accum_load_t| = 0.0` and
  `max |Δ outlet total| = 0.0` — **bitwise**, not approximate. Repeated on a 600-node random DAG
  with 25 permutations: 0.0.
- **B3 stored `topo_order_idx`**: the stored order differs from the module's Kahn order in
  **8,644 of 8,672** positions and both are valid (0 partial-order violations each). Wrote a
  third, deliberately unusual valid order (differs from stored in 8,490 positions) into a scratch
  npz — `load_network` accepted it and the routing result was **bitwise identical**, confirming the
  module routes on its own Kahn order and never on the stored one. An invalid stored order (one
  contributor/receiver swap) **raises**; a non-permutation **raises**. A bundle with
  `topo_order_idx` **absent** loads with no warning and the cross-check is silently skipped.

### PROBE (c) — the `mini_ids` guard, fired six ways
Script: `probe_cd_guard.py`. Every one of these **raised `ValueError`**, with a correct first-
mismatch index: adjacent transposition at 4335/4336 (reported index 4335), swap first/last,
full random permutation, `ids[::-1]`, `np.roll(ids, 1)`, truncation to n−1, a `(n,1)` reshape.
No false positives: `np.sort(ids)` and a correct Python list were accepted.

**Whether the guard matters in production:** `h2e_drivers.npz:minibacia_id` **equals**
`topology.npz:minibacia_id` elementwise (0 of 8,672 positions differ), so the guard has never
fired on real data. It is defensive, and it works.

**But it is opt-in, and nothing downstream can substitute for it.** Measured: with the adopted
`k_dep = 0`, routing a **column-reversed** load array gives a *bitwise identical* outlet total
(862,758.948603 both ways) and an identical ledger; only per-reach series differ (max 4,028.8 t).
Mass conservation is invariant to a spatial scramble, so no ledger check can see one.

### PROBE (d) — is a zero-deposition run *declaratively* deposition-free?
**Yes, via `params.summary()`; no, via `ledger`.** The default run's summary reports
`asserts_sdr_1: true`, `named_sink: "none (k_dep = 0)"`, `momposina_represented: false`,
`dep_coef_max: 0.0`. On the real basin `deposition_coef` is exactly 0.0 everywhere and
`release_coef` exactly 1.0 everywhere.

Counter-construction: a `k_dep = 0.5` run on a network whose `reach_km` are all 0 produces a
ledger **identical on all 11 keys** to the `k_dep = 0` run. Only `summary()` separates them.
Not a live risk (1 of 8,672 real reaches has `reach_km == 0` — the outlet; total channel
46,321 km), but `ledger` is the dict a report would serialise and it carries no declaration.

### PROBE (e) — silent failure
`src/mgb_transport.py` has **0** `try:`, **0** `contextlib.suppress`, **0** `errstate`,
**0** `nan_to_num`, **0** `filterwarnings`. No swallowed exceptions. The problems are elsewhere:

1. **The per-node mass audit is NaN-blind.** `simulate_transport` line 902 does
   `m = float(np.abs(resid).max()); if m > max_resid:` — and `nan > 0.0` is False. Measured
   with **default params** and loads that pass every declared screen (3 headwaters × 1e308 t,
   finite and positive): every output is NaN, yet `max_node_residual_t = 0.0` and
   `node_partition_exact = True`. Control: monkeypatched a deliberate 1 t/reach leak → the
   audit reports 1.0 and `False`, so it is live, not dead. The global `exact`/`residual_relative`
   *do* flag it (False / nan) — but `max_node_residual_t` is what the module calls "the
   strongest mass statement the module makes" and what `tests/test_transport.py:583` asserts.
2. **`state=` is screened for shape only** (line 878). A `TransportState` with a **negative**
   store was accepted and produced an outlet export of **−736,377.05 t** while
   `exact = True`, `node_partition_exact = True`, `max_node_residual_t = 0.0` — every mass gate
   PASSES on a run exporting negative sediment. NaN and inf stores likewise accepted.
   `TransportState.initial`'s docstring names docs/31 §C4.2's spin-up→calibration state handoff,
   so this is on the C4.2/C4.3 path.
3. **`frozen=True` does not freeze an array parameter.** Built `TransportParams(k_dep=<array>)`
   (validated ≥ 0), then mutated the caller's array to −5. `deposition_coef` → −7.20e10; the
   run turned 40 t of input into `exported_t = 2.0565e12`; ledger `exact=True`,
   `residual_t=0.0`, `max_node_residual_t=0.0`; `summary()['k_dep_max'] = 0.01` hides it.
   Directly falsifies the class docstring's stated purpose.
4. **`downstream_idx < -1` is silently normalised to "outlet"** (line 388) while `>= n` raises.
   Set index 2082 (id 6513, 132,025 km² upstream, 60 hops from the outlet) to −9999: accepted,
   2 outlets instead of 1, and at `k_dep = 1e-3` the outlet load inflates **1.192×**
   (4,067,514.8 vs 3,412,321.2 t) with the corrupt run reporting `exact = True`.
   Real data is clean (min −1, 0 entries < −1).
5. **`hops_to_outlet` from the npz is trusted verbatim** (line 411): an all-zero array and an
   array of the **wrong length** (8,669 vs n=8,672) were both accepted into the frozen network.
   Real stored hops == recomputed (max |diff| 0).
6. **`per_day` warning misses a partially-zero tau array**: `tau = [0,0,0,2.0]` with
   `dep_mode='per_day', k_dep=0.1` emitted **0** warnings (scalar 0.0 emits 1). It is also only
   a warning — no trace in `ledger` or `summary`.
7. **`audit_mass=False` reports `node_partition_exact: False`** with `max_node_residual_t: nan`
   — a not-measured rendered as a boolean failure.
8. Minor: duplicate `record_ids` accepted; `load_at(unknown)` raises `IndexError` not `KeyError`;
   `ndays=0` accepted. Correctly handled: `state` is copied not mutated; `k_dep` array of wrong
   length raises; `k_dep=1e300` → dep_coef 1.0 (no nan); `tau=1e300` → rel_coef 1e-300 (never
   exactly 0, so mass is never trapped); subnormal tau → 1.0.

### `split_stations_by_momposina` — the 801.1 km, checked against its source
`channel_km_below_reference` = **801.0880261366544** km = `net.reach_km[path].sum()` over the
**147**-reach path *including* the reference's own 5.8139 km, and equals
`topology.npz:path_km_to_outlet[12354]` **exactly** — so docs/42's 801.1 km reproduces.
But `n_reaches_below_reference` = **146** counts `path[1:]`. The two returned fields describe
different sets of reaches. Number right, field pair inconsistent.

### `dtype_out` float32 default
`load_t_day` is float32 unless set. Measured on the real basin with lognormal loads: max
relative error **5.953e-08**, median **2.066e-08**, max absolute **0.4999 t/day**;
`accum_load_t` is float64 so the two disagree at 5.741e-08 relative. The test file documents
this in a comment; the module docstring does not.

### Confirmations worth keeping
- **End-to-end coupling reproduces the published level.** `mgb_sediment` at adopted defaults →
  `simulate_transport` at `k_dep = 0` over 2009-2018: decade export **2,994.977 Mt** =
  **299.54 Mt/yr**, matching `docs/37` Amendment A1's 299.539 Mt/yr. `residual_relative = 0.0`,
  `store_end = 0.0`, `max_node_residual_t = 0.0`.
- **The module's stated reason #3 for `tau_channel_days = 0` survives measurement.** With
  per-reach tau from the frozen H2E celerity 0.221 m/s (median 0.266 d/reach; **cumulative**
  lag to the outlet median 35.7 d, max 74.7 d), window totals move by **+0.03 %** (La Niña
  2011), **−0.43 %** (El Niño 2015-16 Jul–Jun), **−0.03 %** (decade), and the simulated ENSO
  ratio moves **2.8806 → 2.8939**. A pure lag really does leave the C5 quantity alone.



---

## Verdict

The C4.1 transport engine is **correct on every property it was asked to have**: mass conserves
to 0–2 ULP, the sweep is topologically sound and bitwise order-invariant, both backends agree,
the `mini_ids` guard fires on every permutation form, and the zero-deposition default is exactly
zero and declared. No swallowed exceptions anywhere.

What it does **not** have is an audit that can tell a physical run from an unphysical one. The
ledger measures a *partition* (`S − dep − out − store'`), which closes identically for negative
coefficients, negative stores and corrupt topology, and its per-node maximum is skipped entirely
by NaN. Three separate constructions produced runs the ledger certifies as `exact = True` /
`node_partition_exact = True`:

| construction | what the run did | what the ledger said |
|---|---|---|
| `state=` with a negative store | exported **−736,377 t** | `exact=True`, `node_partition_exact=True` |
| mutated `k_dep` array (frozen dataclass) | 40 t in → **2.06e12 t** out | `exact=True`, `residual_t=0.0` |
| `downstream_idx = −9999` on a trunk reach | outlet inflated **1.192×** at k_dep=1e-3 | `exact=True` |
| loads overflowing to inf at a confluence | every output NaN | `node_partition_exact=True` |

None of these is a live defect on today's data (drivers and topology are both clean, and the
adopted run is `k_dep = 0` with `state=None`). All four become live the moment C4.3 starts
fitting a `k_dep` field or chaining a spin-up state — which `docs/31` §C4.2 says it will.

Recommended (NOT applied — I do not edit adopted config):
1. `simulate_transport` line 902: `if not (m <= max_resid): max_resid = m` — or `np.isnan(m)`
   raises. One character of intent, and the NaN hole closes.
2. Screen `state.store_t` for finiteness and non-negativity next to the shape check at line 878.
3. Re-validate `k_dep` / `tau_channel_days` inside `deposition_coef` / `release_coef`, or
   `np.array(..., copy=True); arr.flags.writeable = False` in `__post_init__`.
4. `build_network`: raise on `down < -1` instead of normalising; validate `hops_to_outlet`'s
   shape (and ideally recompute-and-compare, as `topo_order_idx` already is).
5. Fold `dep_mode` / `asserts_sdr_1` / `named_sink` into `ledger` so a serialised report carries
   the docs/42 G5 claim; and make `node_partition_exact` tri-state (`None` when not audited).
6. `split_stations_by_momposina`: name the km field `channel_km_reference_to_outlet`, or count
   147 reaches, so the two agree.

Nothing in the repo was modified except this journal. Scratch scripts live in the session
scratchpad (`probe_a_mass.py`, `probe_b_order.py`, `probe_cd_guard.py`, `probe_e_silent.py`,
`probe_f_nanblind.py`, `probe_g_state_tau.py`) and are not versioned — the numbers above are
the record.
