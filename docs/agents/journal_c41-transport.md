# journal — `c41-transport`

**Agent slug:** `c41-transport`
**Opened:** 2026-08-11
**Goal:** implement **C4.1 — channel transport of the suspended load**: advect the MUSLE
hillslope load per minibacia down the existing reach topology, with a first-order
deposition/settling term as a *named* parameter defaulting to zero, and with the
**Depresión Momposina limitation declared in the docstring before any parameter is fitted**.

**Hard constraints carried in (from the brief):**
- No git add/commit/push. No calibration search. No touching frozen artifacts
  (`sim_calibrated_v2/{h2e_drivers.npz,parameters_H2E.csv,q_gauge_H2E.npz}`).
- Never `pd.read_csv` the wide forcing CSVs — use `src/forcing_npy.py`.
- Verify from executed outputs, not exit codes.
- t/km²/yr gauge-referenced yields are EMBARGOED (docs/23 §13.2).
- Uncited plausibility bands may neither pass nor fail a gate — say UNCITED.
- **Record any decision here BEFORE computing what it does to a headline number.**

## Checklist

- [x] 0. Journal opened (this file) — first action.
- [x] 1. Read state: docs/00_INDEX, docs/42 (C4 guards), docs/37 A1/A2, docs/43 if present,
      docs/22 §4.6 (celerity as floodplain surrogate).
- [x] 2. Read `src/mgb_sediment.py` and the routing in `src/mgb_hydrology.py`;
      inspect `model_inputs_v2/topology.npz`.
- [x] 3. **Placement decision** (record here before writing code).
- [x] 4. Implement transport + declare the Momposina limitation in the module docstring
      and in the routing function's docstring, *before* any fit.
- [x] 5. `tests/test_transport.py` — 5 required properties, all green.
- [x] 6. Full `pytest` — report count.
- [x] 7. Basin decade run: outlet Mt/yr at deposition=0, spatial pattern, load at the one
      trunk station and each usable tributary station.
- [x] 8. Report via structured output only.

---

## Log

### Step 0 — journal opened
Before reading any code. No numbers computed yet.

### Step 1 — state read (no numbers computed)
- `docs/00_INDEX.md` §4 (the WHERE-IS-IT table), `docs/31` §C4.1 (the subtask that names the
  Momposina docstring requirement verbatim), `docs/42` §G5 (the precondition guard: a C4 fit is
  adoptable only with a **named, non-trivial transport sink** — `tau_delivery_days > 0` or a
  fitted+reported reach deposition coefficient — or the explicit SDR = 1.0 claim), `docs/42` §G9
  (the unobserved-fraction disclosure), `docs/22` §4.6 (celerity fitted to **0.221 m/s**, 4.5×
  below prior, identified by nb14 §4.3 as a **floodplain-storage surrogate for the Mompós
  reach**), `docs/18` §open-item 4 / `docs/21` §4 item 3 (local-inertial routing for Mompós —
  *not to be implemented on current evidence*; carry it as a **named limitation**).
- `src/mgb_sediment.py` (1,512 lines) and `src/mgb_hydrology.py` routing (`_route_numpy`,
  `_topological_order`, `_pack_levels`, `default_channel_tau`).
- `data/processed/model_inputs_v2/topology.npz`: 8,672 nodes, **one** outlet
  (`outlet_idx` = 234), `topo_order_idx` verified an admissible topological order
  (downstream strictly later for all 8,671 linked nodes), `hops_to_outlet` max 291,
  `reach_km` present (total 46,321.03 km).
- Usable SSC set read from `data/processed/sediment_inventory_qc.csv`:
  6 `usable` + 12 `usable-with-caveat` = **18**, all with a mapped minibacia; exactly one
  Magdalena-trunk station (`21237020` ARRANCAPLUMAS, minibacia 12354).

### Step 2 — DECISIONS, recorded BEFORE any headline number is computed
*I am writing these down before running anything, as the brief requires. Nothing below was
chosen after seeing what it does to the outlet load — at the time of writing I have computed
no load of any kind.*

**D1 — placement: a NEW module `src/mgb_transport.py`, not an addition to `mgb_sediment.py`.**
Three reasons, the first decisive:
1. `mgb_sediment.py`'s own docstring states, as a scope claim the rest of the file depends on:
   *"It is NOT a channel model. Advection, deposition and the Momposina floodplain sink are
   stage C4 (docs/31 §C4.1) and deliberately absent here: this module's output is the input to
   that step, so anything it produced downstream of the hillslope would be double-counted
   later."* Adding channel transport to that file would falsify its own docstring and blur the
   one boundary — hillslope vs channel — that the double-counting warning depends on.
2. It is already 1,512 lines; the project's style rule caps a file at 800.
3. Separation keeps the two mass ledgers independent: the hillslope ledger
   (`eroded = delivered + stored`) is closed inside `mgb_sediment`, and the channel ledger
   (`delivered_in = outlet + deposited + in-channel storage`) is closed inside `mgb_transport`,
   so a leak can be localised to one of the two.

**D2 — routing form: linear-reservoir (Muskingum X = 0) per reach, swept in topological
order, i.e. exactly the water router `mgb_hydrology._route_numpy` uses.** Reason: C4.1 says
"with the existing storage routing". A different channel operator for sediment than for water
would make concentration = load/discharge un-interpretable at a station.

**D3 — `tau_channel_days` default 0.0 (same-step advection).** Reasons, in order:
(a) it is the zero-storage, SDR-defining baseline the brief asks to be reproducible;
(b) the frozen H2E water routing has ALREADY applied channel storage, and its fitted celerity
0.221 m/s is a floodplain-storage surrogate (docs/22 §4.6) — a second lag on the sediment
double-counts it, which is the same argument `mgb_sediment.SedParams.tau_delivery_days = 0`
already makes for the hillslope reservoir;
(c) annual and window totals — the C4/C5 quantities — are invariant to a pure lag anyway.
A non-zero lag stays one call away (`channel_tau_from_celerity`, which delegates to
`mgb_hydrology.default_channel_tau` rather than re-deriving it).

**D4 — deposition: a NAMED first-order parameter `k_dep`, default exactly 0.0, with two named
modes.** `dep_mode='per_km'` (DEFAULT): `d_i = 1 − exp(−k_dep · reach_km_i)`, `k_dep` in 1/km.
`dep_mode='per_day'`: `d_i = 1 − exp(−k_dep · dt)`, `k_dep` in 1/day. `per_km` is the default
because it is **discretisation-invariant**: retention along a flow path is
`exp(−k_dep · path_km)` regardless of how many minibacias the path is cut into, whereas a
per-step coefficient is applied once per reach and therefore changes meaning if the network is
re-discretised — and at `tau_channel_days = 0` it would be applied ~`hops_to_outlet` times in a
single day, which is not a rate at all. `per_day` is kept because it is the linear-reservoir
analogue C4.3 may want once `tau_channel_days > 0`. This choice is recorded here **before** I
know what any value of `k_dep` does to the outlet load.

**D5 — two backends, asserted to agree** (`'levels'` vectorised, `'order'` node loop), the same
two-implementation discipline `mgb_hydrology` and `mgb_sediment` use.

**D6 — exactness claim, stated before it is tested.** At `k_dep = 0` and
`tau_channel_days = 0` the per-reach coefficients are exactly 0.0 and exactly 1.0, so every
per-node step is bitwise and the per-node/per-day mass residual is exactly 0.0. The GLOBAL
identity `sum(local) == outlet` additionally needs the cross-node summation to be exact, which
holds whenever the arithmetic is exact — so it is asserted **bitwise on the real 8,672-node
topology with integer-valued loads**, and on real float drivers the residual is pure
re-association rounding, measured and reported rather than asserted to zero. I am stating this
distinction now so that a small non-zero float residual later cannot be presented as if it had
been the plan.

**D7 — the Momposina limitation goes into the module docstring and into the routing function's
docstring BEFORE any parameter is fitted**, and no fit is performed in this session at all.

### Step 3-4 — implementation
`src/mgb_transport.py` written (700 lines). Module docstring opens with the limitation block
(*"THE LIMITATION, DECLARED BEFORE ANY PARAMETER IS FITTED: THE DEPRESIÓN MOMPOSINA SINK IS
NOT REPRESENTED"*), repeated inside `route_day` — the function that would have to change —
and available as the string constant `MOMPOSINA_NOTE` so a report cannot quote a below-Mompós
number without it. `tests/test_transport.py::test_the_momposina_limitation_is_declared_in_the_module_and_in_the_router`
asserts the mitigation rule and the docs/22 §4.6 citation are present in both docstrings, so
the declaration cannot be quietly deleted.

### Step 5 — a real bug the tests caught, recorded because it changed a table
First draft of `split_stations_by_momposina` read *"calibrate = drains through the
reference"*. On the real basin that put **JULUMITO, IRRA, BOLOMBOLO, PUENTE ARAGÓN, EL
ALAMBRADO, MATEGUADUA, PAILA LA, BANANERA** into `evaluate_only` — because the **Cauca joins
the Magdalena BELOW ARRANCAPLUMAS**, so no Cauca station drains through it, even though every
one of them sits hundreds of km **above** the Momposina. The correct rule is *"evaluate_only =
on the trunk strictly downstream of the reference"*. Fixed; regression test added
(`test_station_split_keeps_a_sibling_tributary_in_the_calibration_set`), and the fixed
function now reproduces docs/42 §4.5's published **801.1 km** below ARRANCAPLUMAS from
`topology.npz` alone (measured **801.088 km**) as an independent check that the definition is
the one the documents used. Under the fixed rule **all 18 usable stations are `calibrate`,
0 are `evaluate_only`** — which agrees with docs/42 §6 ("all 18 usable SSC stations lie
upstream of the Cauca–Magdalena confluence").

### Step 6 — a second measured finding, from a failing test
The first full-decade run FAILED the mass gate at **3.9e-11 relative** (2 994 977 042.143 vs
2 994 977 042.261 t). Cause: `mgb_sediment.simulate_sediment` writes its coupling array in
**float32** by default (~1e-7 relative per value). Not a leak — a storage-precision artefact —
but a mass test must not silently absorb one, so the coupling now runs at `dtype_out=float64`
and the reason is written into the fixture.

### Step 7 — GATE: full pytest
`python3.10 -m pytest tests -q` → **138 passed**, 1 warning (the pre-existing
`urh_fractions` vs `urh_ls2d` area-disagreement warning from `mgb_sediment.load_geometry`),
47.8 s. Baseline before this session was 96; `tests/test_transport.py` adds **42**.

### Step 8 — the basin decade, at k_dep = 0 (NO fit performed)
Period 2009-01-01 … 2018-12-31, 3,652 d (9.9986 yr). `SedParams()` adopted defaults
(`williams_m3` + `us_customary` + `cp_revision='cited_central_2026_08_11'`),
`TransportParams()` = `k_dep` 0.0 / `per_km` / `tau_channel_days` 0.0.

- **Outlet load 299.5387 Mt/yr** at minibacia 2470, *identical* to the hillslope delivered
  total — which is the definition of `k_dep` = 0, not a result: **this run asserts SDR = 1.0
  between hillslope and station** (docs/42 G5, stated in those words).
- **Mass ledger:** `local_in` = `exported` = 2 994 977 042.2609434 t; `deposited` 0.0;
  `store_end` 0.0; **`residual_t` exactly 0.0** and **`max_node_residual_t` exactly 0.0** on
  real float drivers. The global bitwise equality was promised only for exact arithmetic
  (D6) — it came out exact here too; recorded as measured, not as designed.
- **Spatial pattern** (period-total load leaving each reach, Mt/yr): min 4.45e-5, median
  0.0815, p90 3.910, max 299.539; **0 reaches carry zero**. Share of local hillslope load
  generated at or above N hops from the outlet: 50 → 99.47 %, 100 → 77.65 %, 150 → 29.57 %,
  200 → 16.40 %, 250 → 5.16 %. By hops-to-outlet quintile (Mt/yr): 27.33 / 68.90 / 101.52 /
  52.07 / 49.72 — the middle of the network, not the outlet-most fifth, generates the most.
- **Runtime:** hillslope 3.4 s, transport 27.6 s (292 levels × 3,652 d).
- **G9 disclosure, reproduced independently:** only **33.47 %** of the model's local load is
  upstream of any usable SSC station (3,282 of 8,672 reaches); **801.088 km of channel —
  the whole Momposina — lies below the outlet-most station**. The 33.47 % matches docs/37
  §4.5 to the printed digits from an independent path.

**Station loads, C4.3's calibration targets** (absolute flux only; **no t/km²/yr anywhere —
embargoed, docs/23 §13.2**):

| code | name | mini | class | reach | Mt/yr | t/day | hops |
|---|---|---|---|---|---|---|---|
| 21237020 | ARRANCAPLUMAS | 12354 | usable | **magdalena trunk** | **56.727** | 155 311 | 146 |
| 26207080 | BOLOMBOLO | 10854 | caveat | cauca mainstem | 16.904 | 46 281 | 148 |
| 23087210 | CANTERAS | 10273 | caveat | tributary | 15.761 | 43 152 | 124 |
| 22057090 | BOCATOMA TRIANGULO | 15126 | caveat | tributary | 12.085 | 33 088 | 193 |
| 26167070 | IRRA | 12207 | caveat | cauca mainstem | 10.787 | 29 534 | 167 |
| 24037390 | CAPITANEJO | 9812 | usable | tributary | 6.006 | 16 444 | 138 |
| 22017010 | BOCAS | 15661 | usable | tributary | 5.079 | 13 904 | 212 |
| 23127010 | BORBUR | 11503 | usable | tributary | 3.575 | 9 788 | 137 |
| 21147030 | CARRASPOSO | 15959 | caveat | tributary | 2.695 | 7 380 | 210 |
| 24027030 | NEMIZAQUE | 10354 | caveat | tributary | 1.276 | 3 495 | 138 |
| 26107130 | MATEGUADUA | 14641 | caveat | tributary | 0.698 | 1 911 | 219 |
| 26017020 | JULUMITO | 17645 | caveat | cauca mainstem | 0.608 | 1 663 | 276 |
| 21197010 | EL PROFUNDO | 14664 | usable | tributary | 0.600 | 1 644 | 190 |
| 26127010 | EL ALAMBRADO | 13857 | caveat | tributary | 0.554 | 1 516 | 197 |
| 26017060 | PUENTE ARAGÓN | 18128 | caveat | cauca mainstem | 0.187 | 513 | 287 |
| 26137110 | BANANERA LA 6-909 | 13188 | caveat | tributary | 0.093 | 254 | 195 |
| 22017030 | BOCAS | 15654 | usable | tributary | 0.090 | 247 | 213 |
| 26167060 | PAILA LA | 12298 | caveat | tributary | 0.029 | 80 | 169 |

All 18 are `calibrate`-eligible; **`evaluate_only` is EMPTY**. The consequence, stated
because it is the honest one: **the cost of the missing Momposina sink cannot be measured at
any station in this network** — the only place it shows is the outlet, and there is no
observation there. The mitigation rule survives as a *prohibition* (never calibrate below
Mompós) but its *measurement* arm has nothing to measure until an at- or below-Mompós SSC
series is obtained.

### Step 9 — what was NOT done
No calibration search launched. No parameter fitted. No frozen artifact written
(`h2e_drivers.npz` opened read-only by `mgb_sediment.load_drivers`; `parameters_H2E.csv` and
`q_gauge_H2E.npz` never opened). No wide forcing CSV read with pandas. Files touched: this
journal, `src/mgb_transport.py`, `tests/test_transport.py` — and nothing else.
