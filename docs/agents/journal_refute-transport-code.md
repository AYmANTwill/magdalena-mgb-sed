# Journal — adversarial refutation of "state= is validated for shape only" (src/mgb_transport.py:878)

Agent: refute-transport-code. Started 2026-08-11.
Posture: default = the finding is WRONG; try to prove it.

## Target finding
`simulate_transport` checks `st.store_t.shape` and nothing else, so a `TransportState`
carrying negative / NaN / inf tonnes is accepted and propagates, and the mass ledger
cannot see it because the partition still closes.

## Step 1 — read the code (done)
- src/mgb_transport.py:877-879 is literally:
  ```
  st = TransportState.initial(net) if state is None else state.copy()
  if st.store_t.shape != (n,):
      raise ValueError("state does not match the network")
  ```
  No finiteness, no sign, no dtype check. Contrast at 860-864: `local_load_t_day` IS
  screened for non-finite and for negatives. So the *code-shape* half of the claim is
  literally true on inspection.
- `TransportState` (623-644) is a plain `@dataclass` with NO `__post_init__` — so nothing
  validates on construction either. `TransportParams.__post_init__` (533-543) DOES
  validate finiteness + non-negativity of k_dep/tau. State is the odd one out.
- `grep TransportState` in tests/test_transport.py → NO hits. The state path is untested.

## Step 2 — things to actually MEASURE (not assume)
1. Does `store_t=[-1e6,0,0]`, tau=1.0, 3-reach chain really give outlet ≈ -736377.05 t?
2. Does the ledger really report exact=True / node_partition_exact=True / max_node_residual=0?
3. NaN and inf cases — the claim says node_partition_exact stays True. Suspect the
   mechanism is `if m > max_resid` with m=nan → False → max_resid never updated. VERIFY.
4. Adversarial: is there any *reachable* path that produces a bad state, or does it need
   a hand-built one? Engine invariants (rel_coef in (0,1], dep_coef in [0,1), screened
   loads) should make an engine-produced state provably finite and >= 0.

## Step 3 — MEASURED (scripts in scratchpad: repro_state.py, repro2.py; python3.10, numpy 2.2.1)

3-reach chain 10->11->12, reach_km=1, tau_channel_days=1.0, k_dep=0 (default).

| state passed                | accepted? | outlet total (t)        | ledger.exact | node_partition_exact | max_node_residual_t |
|-----------------------------|-----------|-------------------------|--------------|----------------------|---------------------|
| None (cold, control)        | -         | +2650.938…              | False        | True                 | 0.0                 |
| `[-1e6, 0, 0]`              | YES       | **-996018.939…**        | **True**     | **True**             | **0.0**             |
| `[nan, 0, 0]`               | YES       | nan                     | False        | **True**             | **0.0**             |
| `[inf, 0, 0]`               | YES       | nan                     | False        | **True**             | **0.0**             |

Same on `backend='order'`. So the finding's CODE claim reproduces.

**I reproduced the reporter's exact figure.** Grid-searched ndays x load amplitude:
ndays=3, uniform local load 10.0 t/day, tau=1.0, store0=[-1e6,0,0] gives outlet total
= `-736377.0546964137`, bit-for-bit the number they quoted. Their evidence is real and
independently reproducible, not a mis-transcription.

### Attempts to REFUTE, and what each found

1. **"the ledger does see it"** — no. For the negative state all three mass gates report
   clean: `exact=True`, `residual_t=0.0`, `node_partition_exact=True`,
   `max_node_residual_t=0.0`, while the basin exports -996 kt. Refutation failed.
   *Partial hit on the TITLE only:* for nan/inf, `ledger['exact']` is **False**
   (`residual_t=nan`), so "every mass gate reporting PASS" holds for the NEGATIVE case,
   not for the nan/inf case. The finding's body was already careful about this; the title
   is the part that overreaches.

2. **"a RuntimeWarning fires, so it isn't silent"** — partly. nan/inf emit
   `RuntimeWarning: invalid value encountered in multiply` at line 713. The NEGATIVE case
   emits **nothing at all**. And a warning is not a gate: nothing reaches the ledger.

3. **"the engine can't produce a bad state, so it's unreachable"** — this is the one real
   dent, and it is in the *severity story*, not the code claim. Measured: 200 randomised
   runs (n 3-25, random k_dep/dep_mode/tau, 40 d of random loads) gave **min store over
   every run/reach = exactly 0.0, all finite**. Analytically it must: loads are screened
   finite and >=0 (860-864), `dep_coef` in [0,1), `rel_coef` in (0,1], so
   `store' = (s - dep)(1 - rel) >= 0`. An engine-produced state is therefore provably
   clean, so the corruption has to arrive from outside (hand-built, deserialised, or a
   future code path).
   Also: `grep simulate_transport` over the whole repo -> **only tests/test_transport.py**
   calls it, and **none of them passes `state=`**. C4.2/C4.3 are not written yet. And
   docs/31 §C4.2 describes ONE continuous 2009-2018 run scored on windows, not two chained
   calls, so the "spin-up hands its corruption to the scored window" narrative needs a
   handoff nothing currently performs.
   => the defect is a latent hazard on an untested path, not an active wrong number.

### Two things I found that the finding UNDERSTATES

4. **The shape-only check also admits the wrong DTYPE**, and that one is an ordinary
   mistake, not a contrived one. Same chain, 6 d, `TransportState(np.zeros(3, dtype=...))`:
   - float64 (ref): outlet 1454.5313896428243
   - float32: ACCEPTED, outlet 1454.5313878787736, final store [58.053413 115.55969 171.8555]
   - int64:  ACCEPTED, outlet 1450.5244582780676, final store **[57 115 171]** — the store
     is truncated to whole tonnes every single day
   (both do trip `node_partition_exact=False`, so the ledger catches dtype corruption even
   though it cannot catch sign/nan corruption.)

5. **`max_node_residual_t` is NaN-blind independently of the state.** With a perfectly
   valid zero state and loads that pass both screens (finite, non-negative), overflow to
   inf -> nan gives outlet nan with `node_partition_exact=True, max_node_residual_t=0.0`.
   Mechanism at 901-903: `m = float(np.abs(resid).max())` is nan, and `if m > max_resid`
   is False for nan, so `max_resid` is never updated from its 0.0 initialiser. The module
   docstring calls this "the strongest mass statement the module makes" — it has a nan
   blind spot regardless of `state=`. Fix is `if not (m <= max_resid): max_resid = m`, or
   screen `resid` for non-finiteness.

## Verdict
NOT REFUTED. refuted=false, confidence high. Corrections: title overreaches on the nan/inf
case; severity should be latent-hazard (unreachable from inside the engine, no caller today)
rather than an active corruption; and the check should screen dtype as well as sign and
finiteness, with the separate nan-blind `max_resid` comparison fixed alongside.


---

# APPENDED 2026-08-11 by a SECOND agent sharing this filename (see MEMORY: filename collision)

Agent: refute-transport-code (wave 2). Different target finding. Nothing above was edited.
**Target: "The per-node mass audit is blind to NaN and reports PASS on an all-NaN run"**
(src/mgb_transport.py:902, severity high). Posture: default = WRONG, try to prove it.

Note on independence: §5 of the section above was written by a different agent working a
*different* target, and it reports this same mechanism as a side observation. I did not read
it until after my own runs had completed (my scripts were already written and executed). Two
agents, two entry points, same measured behaviour.

## What I ran
- `scratchpad/repro_nan_audit.py` — 5-reach toy net (3 headwaters -> junction -> outlet),
  **DEFAULT `TransportParams()`**, python3.10 / numpy 2.2.1, `np.geterr()` all 'warn'.
- `scratchpad/repro_real_topology.py` — the real 8,672-reach `model_inputs_v2/topology.npz`.

## Measured (executed output, not exit code)

RUN 1, one day, three headwaters at 1e308 (input screens: all finite=True, any negative=False):
```
outlet_t_day        : [nan]
local_in_t = inf   exported_t = nan   deposited_t = nan   store_end_t = nan
residual_t = nan   residual_relative = nan   exact = False
max_node_residual_t = 0.0        node_partition_exact = True
```
RUN 2 (5 days, only day 2 overflows): `outlet [500. 500. nan nan nan]`, still
`max_node_residual_t=0.0 / node_partition_exact=True`.
RUN 3 CONTROL (monkeypatched route_day stealing 1 t/reach): `1.0 / False` — the audit is live,
so this is specifically NaN blindness, not a dead audit.
RUN 5 (`backend='order'`): identical, `nan` outlet, `0.0 / True`.
Primitives: `np.abs([nan,0,0]).max()` = nan; `float(nan) > 0.0` -> False; `inf*0.0` = nan;
proposed fix `not (m <= max_resid)` on nan -> True.

The reporter's cited test line is right: `tests/test_transport.py:583` is
`assert led["max_node_residual_t"] == 0.0`, which RUN 1 satisfies.

## Refutation attempts, and what each found

1. **"an np.seterr/errstate somewhere turns the overflow into a raise, so the run never
   returns"** — no. `grep -rn "seterr\|errstate"` over the repo: 17 hits, none in
   `src/mgb_transport.py` or `tests/test_transport.py`, and all are local
   `with np.errstate(...)` suppressors elsewhere. Defaults are 'warn'. The run returns.
2. **"only the 'levels' backend does this"** — no, RUN 5, `order` backend is identical.
3. **"the docstring doesn't actually advertise this as the primary gate"** — it does,
   verbatim: line 159 "This is the strongest mass statement the module makes"; line 785
   "The stronger and always-exact statement is ``max_node_residual_t``"; line 835
   "it is the module's strongest mass statement and it is cheap."
4. **"1e308 is absurd, so this is unreachable"** — the only dent, and it lands on the
   *load* path only. MEASURED on the real 8,672-reach network, uniform load per reach:
   1e300 -> outlet 8.672e303 finite; 1e304 -> 8.672e307 finite; **1e305 -> nan with
   `max_node_residual_t=0.0 / node_partition_exact=True`**. So the threshold is between
   1e304 and 1e305 t/reach/day. The project's own cited load (docs/37 §line 58: 248.730
   Mt/yr = 2,486,957,417 t over 3,652 d over 8,672 reaches) is **78.5 t/reach/day** — about
   3e302x below the trigger. No conceivable driver reaches it.
   BUT the refutation still fails, because there is a second trigger that needs no overflow
   at all: **RUN 4** — a caller-supplied `TransportState` with one NaN in `store_t`, ordinary
   250 t/day loads -> `outlet [nan nan nan nan]`, `max_node_residual_t=0.0`,
   `node_partition_exact=True`. `simulate_transport` validates only `st.store_t.shape`
   (line 878). That is the same hole the wave-1 finding above is about, reached from the
   other side.
5. **"the test suite catches it anyway"** — partly, and only for the real-basin fixture:
   `tests/test_transport.py:560 test_full_basin_decade_is_nan_free` asserts
   `np.all(np.isfinite(res.outlet_t_day))` as a SEPARATE test. That protects the suite; it
   does nothing for a report that quotes the ledger, which is the finding's actual scenario.
6. **"the ledger as a whole still fails, so nothing is certified"** — the finding already
   concedes this (`exact=False`, `residual_relative=nan`) and I confirm it. It narrows the
   consequence; it does not touch the claim.

## Verdict
NOT REFUTED. refuted=false, confidence high — every element reproduced verbatim, on two
backends, on the toy net and on the real topology, with a live-audit control.
Narrowing that should travel with it: the load-side trigger is measured at >1e304 t/reach/day
(~3e302x the project's own load, i.e. unreachable), so the reachable trigger is the unscreened
`state=` path, which makes this and the wave-1 finding **one defect surface with two gates
missing**: (a) `if not (m <= max_resid)` at 902, and (b) a finiteness screen on `state`.

Consumers of the key, for whoever fixes it: `tests/test_transport.py:228,229,294,583`.
Nothing in `src/` or `scripts/` consumes it yet — C4.3 is not written, so this is a latent
hazard, not a wrong number already published.
