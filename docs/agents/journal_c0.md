# Journal — Stage C0: freeze and report H2E

Session opened 2026-08-10. Plan: `docs/31_phase_c_workplan.md` Stage C0, subtasks C0.1–C0.6,
executed exactly. **C0.2 (the reproduction gate) blocks everything else.**

Reading order actually followed: `CLAUDE.md` → `docs/21_project_state_and_handoff.md` →
`docs/20_reproduction_guide.md` → `docs/31` §0 + Stage C0. Also read for the numbers this stage
must reproduce: `docs/29_seed_expansion.md` (the H2E read-out), `src/calib_v2.py` in full,
`src/nbgen/make_nb14.py` §7/§8/§13 (the artifact schemas C0.1/C0.3 must match).

---

## 0 — Pre-registration: choices made BEFORE any number was computed

Recorded here first, because each of them could otherwise be tuned to the answer.

**P1 — the environment/provenance check.** `calibration_v2.json` records
`engine.sha256 = cdea026a…` and `search_code.sha256 = 3342728f…`. The files on disk are
`93b180a9…` and `3aa4f8b6…`. This is **expected, not drift**: commit `80a7c10`
("FAO-56 threshold ET stress (opt-in) + pre-registered cell H2E", 2026-08-03 20:34) changed both
files *after* nb14 ran (2026-08-03 05:22) and *before* the H2E search ran (2026-08-04 23:04 →
2026-08-05 02:26). The check that matters is therefore not "matches nb14's recorded SHA" but
**"matches the blob the H2E search itself ran"**: `git show 80a7c10:src/mgb_hydrology.py` hashes
to `93b180a9…`, identical to the working tree, and `git log --follow` shows no commit has touched
either file since. The line-ending normalisation commit `73cbc24` did not include them.

**P2 — the forcing cache is absent and will be regenerated.** `_calib_cache/H2_precip.npy`,
`H2_pet.npy`, `H2_dates.npy` (H2E reads H2's cache, `CELLS['H2E']['cache'] = 'H2'`) are not on
disk; they were cleaned up after the queue finished. `calib_v2.ensure_cache('H2E')` rebuilds them
from `model_inputs_v2/forcing.npz` deterministically, and `Cell.__init__` asserts the date axis
against the declared period. If the rebuild were not faithful the C0.2 gate would fail — which is
exactly what the gate is for, so no separate check is invented for it.

**P3 — `rec_ratio` has two inequivalent definitions in this repo, so both are reported.**
`make_nb14.py` §7 writes `rec_ratio = nanmedian(k_sim) / nanmedian(k_obs)` (a **ratio of
medians**). `docs/29` rule (b)2 used `median_j(k_sim_j / k_obs_j)` (a **median of ratios**) and is
where the 1.08/1.11 seed-level figures come from. C0.3's gate cites those 1.08/1.11 figures but
also requires the "identical column set" as `metrics_fleet.csv`. Resolution, fixed here in
advance: `metrics_fleet.csv` gets the **ratio of medians**, unchanged, so the column keeps one
meaning across all cells; the **median of ratios** is computed and reported alongside in this
journal and in the docs/26 addendum; the ≤ 1.5× gate is applied to **both** and passes only if
both pass. No post-hoc selection of the kinder statistic.

**P4 — H2E gets both a `prior` and a `fit` row in `metrics_fleet.csv`.** C0.3 says "append H2E
rows … with the identical column set". H1 and H2 each contribute prior+fit rows; H2E's prior is
*not* H2's prior (the ET functional form differs at the prior point too), so a prior row is a real
measurement rather than a duplicate, and omitting it would make the H2E block the only one that
cannot be read as before/after. Cost is one extra full-period run.

**P5 — "Qsur" is ambiguous in C0.5, so both candidates are stored.** The engine produces two
distinct per-day surface quantities: `d_sup` (saturation-excess surface runoff *generated* on the
URH column, area-weighted to the minibacia) and `q_sup` (the *release* from the minibacia surface
linear reservoir). MUSLE's `Qsurf` could reasonably be either, and C3.3 has not yet registered its
choice. C0.5 exists precisely so that sediment work never re-runs hydrology, so storing only one
would defeat it. Both are stored, named unambiguously, and the choice is left to C3.3.

**P6 — the recording driver must not modify the engine.** C0.5 needs per-minibacia daily fields
that `mgb_hydrology.simulate` does not return (it records only `q_m3s` at `record_ids` plus
basin-total series). Two options: add a recording hook inside `simulate`, or write a separate
driver that calls the engine's own kernel functions. The second is chosen: `mgb_hydrology.py` is
the artefact the whole of Phase B is built on and it stays byte-frozen (P1). The new module
`src/mgb_drivers.py` imports and calls the engine's own `_vertical_step`, `_reservoir_step`,
router and `_assemble_balance`, so **no arithmetic is duplicated**, and it is verified by asserting
its gauge discharge and basin-total series against `simulate`'s on the same inputs. If the engine
loop ever changes, that assertion fails loudly instead of drifting.

---

## 1 — What was built

| file | role |
|---|---|
| `src/report_h2e.py` | C0.1–C0.4. Gate first, then artefacts. Idempotent. |
| `src/mgb_drivers.py` | recording driver over the **frozen** engine (P6) |
| `src/build_h2e_drivers.py` | C0.5. Memmap sinks → `h2e_drivers.npz`. Idempotent. |

A notebook was deliberately not used: nb14 is generated by `src/nbgen/make_nb14.py` and is
pre-registered around H1/H2, so adding H2E there would force a re-execution that rewrites
artefacts H2E does not touch, for no gain. Every schema written here is nb14 section 13's,
and the parameter decoder is **regression-checked** rather than assumed: `check_decoder`
re-derives the committed `parameters_H1.csv` and `parameters_H2.csv` from their own
`dds_*.npz` archives and requires every column to agree to < 1e-12 and every `railed` flag
to match, before the same function is used on H2E. It does. So "identical schema" is a
measurement here, not a claim.

## 2 — C0.1 — the adopted parameter set

`sim_calibrated_v2/parameters_H2E.csv`, 18 rows, decoded from `dds_H2E_20260901.npz`.

**Gate: PASS.** `kc_mult` reads **1.6625** (docs/31 asks for 1.662). `k_int_frac` is at its
0.02 floor — value 0.020142, position **0.185 %** of its log range — and is flagged
`railed=YES`, as docs/31 says it should be.

Railed: **2 of 10 global** (`k_sup` at 99.11 %, `k_int_frac` at 0.19 %), **3 of 18
dimensions** (adding `wm_mult@R2` at 97.13 %). Both denominators are reported everywhere in
this stage's outputs, because reporting one is the origin of docs/31 known-open #1.

**A finding, not a formality — the store-ordering inversion relocated a third time.**
`k_sup` 19.199 d, `k_int` 0.866 d, `k_bas` 42.974 d. `k_int < k_bas` holds by construction.
Unlike H2 (`k_sup` 19.8 d > `k_bas` 13.7 d), H2E no longer puts the surface store above
groundwater — but it puts **surface response 22× slower than interflow**, which is inverted
in the one pair the constraint does not cover. docs/21 open item 12 predicted exactly this
("a constrained ordering *relocates* compensation rather than removing it") and it now holds
for the configuration the project has **adopted**, not only for the ones it rejected. Anyone
reading H2E's stores as physical is reading them wrong; the docs/26 §5.1 warning transfers
verbatim.

## 3 — C0.2 — the reproduction gate: **PASS, exactly**

| | |
|---|---|
| archived F | `0.25930593639066796` |
| recomputed F | `0.25930593639066796` |
| absolute / relative difference | `0.000e+00` / `0.000e+00` (bar ≤ 1e-8) |
| best evaluation index in the archive | 947 of 1000 |
| stored per-gauge terms | `k1` (57 finite), `k2` (54), `k_sim` (63): **max abs diff 0.000e+00**, NaN patterns identical |

Checked before the comparison, so the gate could not pass on a technicality: the archive's
`f` equals its own `arch_f.max()`; the stored `x` is the `arch_f` argmax; the stored
18-name search-vector layout equals `pack_bounds(cell)`'s; the cell really is FAO-56 with
θ_crit 0.6. The per-gauge check matters — F is one scalar and a scalar can coincide, whereas
174 finite per-gauge terms reproducing bit-for-bit cannot.

The forcing cache had to be regenerated (P2); the gate passing to the last bit *is* the
evidence that regeneration was faithful, which is why no separate check was invented for it.

## 4 — C0.3 — full run and per-period metrics

Full period 2008–2018 (4,018 d), 2008 warm-up, **3,652 scored days**, 63 gauges, numba
router. Prior and fit both run (P4).

- **Gate (a) PASS:** mass-balance residual **9.66e-17** relative at the fit (8.39e-17 at the
  prior), bar < 1e-15. Negative-W guard never fired at either set. RC 0.5127.
- **Gate (b) PASS:** every period's recession ratio inside [1/1.5, 1.5] on **both**
  definitions (P3). Worst value across all 12 combinations: **1.170**. CAL reads 1.0780
  (ratio of medians) / 1.0821 (median of ratios) — the second reproduces docs/29's 1.082 for
  this seed, which cross-validates the decode against the pre-registration read-out.
- A cross-check not asked for but cheap: the day-of-year climatology benchmark computed here
  reproduces H2's **stored** `clim_kge` on all six periods to < 1e-12 (same bundle, same
  gauges), so `skill_over_clim` is on the same yardstick as the H1/H2 rows it will be read
  against.

Fitted VAL-all: KGE 0.3563, r 0.5912, α 0.9048, β 1.0351, PBIAS **+3.51 %**, rec 0.98×.

## 5 — C0.4 — the two tables (full versions in docs/26 addendum A.4/A.5)

**(a)** H2E's improvement over H2 is **volume, not skill**: β 1.073 → 1.035, PBIAS
+7.34 → +3.51 % (best of the four attempts), while VAL KGE +0.011 and r +0.008 both sit
inside docs/29's 0.051 between-seed spread — so neither is a separation, and the docs/22
§4.7 r-ceiling is untouched. Applying docs/26 §5's nine criteria unchanged, **H2E scores
3/9**, the same three as H1 and H2. Adoption rested on docs/29's rules, which H2E passed; it
was never a claim that the adequacy criteria were met, and this stage does not upgrade it
into one.

Also recorded because it is awkward rather than in spite of it: H2E's **prior** scores
VAL-all KGE 0.3576, marginally above the fitted 0.3563. The fit remains right — the prior
buys that KGE with PBIAS +24.4 % and a recession 1.49× too slow — but the number is on
record rather than omitted.

**(b) The inherited caveat, and the most consequential number this stage produced.**
El Niño skill-over-climatology for the adopted fit is **−0.0005**: the dry phase sits *at*
climatology, not above it. Across attempts 2 → 3 → 4 it reads **+0.026 → +0.006 → −0.0005**,
while La Niña holds at **+0.106**. docs/24 slide 9's "the dry phase turns from
worse-than-climatology to better" is true of attempt 1 → attempt 2 and **not** of the
adopted configuration; both docs/24 slide 9 and docs/26 now say so in place. This is what
docs/31 C5.2 must propagate, and it is the caveat attached to every El Niño sediment claim.

## 6 — C0.5 — frozen sediment drivers

`sim_calibrated_v2/h2e_drivers.npz`, **546.4 MB** on disk (633 MB uncompressed: five fields
× (3652, 8672) float32) — larger than docs/31's "~250 MB", which assumed three fields.

- **Identity, not similarity:** the recording run's discharge matches
  `mgb_hydrology.simulate`'s at **0.000e+00** over (3652, 63), all ten basin-total series are
  identical, and the balance dict matches entry for entry. The engine is untouched (P6).
- **Gate — column sums vs the run's water balance: PASS.** Worst relative mismatch
  **5.76e-8** (bar 1e-6), across `qsur_gen_mm` vs `d_sup`, `qsur_rel_mm` vs `q_sup`,
  `q_local_mm` vs `q_sup+q_int+q_bas`, and `q_reach_m3s` at the outlets vs `q_outlet`. Period
  totals agree to 1e-10…1e-13. The residual is float32 storage, not lost mass.
- **Extra gate not asked for:** per-reach continuity, `inflow = local + Σ upstream outflow`,
  evaluated from the **stored fields alone** over all 3,652 days × 8,672 reaches — worst
  relative residual **1.18e-7**. This is the only check that ties `reach_inflow_m3s` and
  `q_reach_m3s` together and proves the stored pair is self-consistent, and it is why the
  (strictly redundant) inflow field is kept.
- **Gate — `np.load` round trip: PASS.** All five fields exact on reload, correct shape and
  dtype, zero NaNs, no negatives.
- Sanity, reported not gated: 650.2 mm/yr generated surface runoff, 651.1 mm/yr released
  (agreeing to 0.14 %, as a quasi-steady surface store should), 1,038.3 mm/yr total local
  runoff, RC 0.5127.

**Idempotency, measured not asserted.** Both scripts were run twice.
`report_h2e.py`: 39 rows → 39 rows, "12 stale H2E rows replaced", pre-existing prefix
unchanged at 5,658 bytes / md5 `33e389a9…` — which is also the byte size the pristine
`metrics_fleet.csv` had before this stage touched it, so the prefix is the original.
`build_h2e_drivers.py` clears and recreates its scratch directory and overwrites the npz.

## 7 — Three things fixed that were nobody's stated task

1. **`metrics_fleet.csv` precision.** The first implementation appended via
   `pd.read_csv(...) → to_csv(...)`. Measured: that re-emits pre-existing floats one digit
   short (`0.08329265113146145` → `0.0832926511314614`), and the two strings **do not parse
   to the same float64** — 3 ULP apart. Those rows are quoted in docs/21 and docs/26. The
   file was restored and the writer replaced with a text-level append that keeps every
   pre-existing line byte-for-byte and asserts so after writing. Worth generalising: *a
   round trip through a dataframe is not a read-only operation.*
2. **The provenance check that would have mis-fired.** `calibration_v2.json`'s recorded
   engine SHA does not match the file on disk, which looks exactly like the drift C0.2
   exists to catch. It is not: commit `80a7c10` added the FAO-56 option after nb14 ran and
   before the H2E search ran. The correct comparison is against the blob the H2E search ran
   (`git show 80a7c10:src/mgb_hydrology.py` → `93b180a9…`, identical to disk, and no commit
   has touched it since). Recorded as P1 so the next session does not raise a false alarm —
   or, worse, dismiss a real one by analogy.
3. **`src/test_mgb_hydrology.py` has been broken since 2026-08-03 and nobody noticed.**
   docs/20 §4 lists it as the first verification bar a rebuild must pass. Running it:
   `TypeError: _Expanded.__init__() missing 2 required positional arguments: 'et_stress'
   and 'theta_crit'` — aborting tests 4 and 6. Cause: commit `80a7c10` added those two
   **required** fields to `_Expanded` when it added the FAO-56 option and did not update
   the test's `_random_cells` constructor; the test file's last commit (`c014623`) predates
   it. So the engine's smoke/regression suite did not run at any point during the
   seed-expansion queue, the H2E search, or the adoption decision. Fixed test-side only —
   two keyword arguments, `et_stress='linear'` (the value that preserves what those tests
   were written to sweep; they predate the option) and `theta_crit=0.6` (inert on the
   linear path). **The engine was not touched**, so nothing frozen by this stage can have
   moved. Result: **59/59 assertions pass, 0 aborted, 33 s.**

   Out of scope but handed forward: the suite still has **no coverage of the `fao56`
   branch** of `_vertical_step` — the branch the adopted configuration runs on. Its only
   end-to-end check is C0.2's reproduction gate, which does exercise it (bit-identically,
   1,000-evaluation search reproduced), but that is a regression test against one stored
   result, not a property test. A test of the FAO-56 stress term's own properties
   (potential ET above θ_crit, linear to zero below, continuity at θ_crit, mass closure)
   belongs with the other engine tests.

**Not fixed, and named rather than silently left:** the C0.5 archive is 546 MB against
docs/31's "~250 MB" estimate. The estimate assumed three fields; five are stored, for the
reasons in P5 and A.6. If space becomes a problem, `reach_inflow_m3s` is recoverable from
`q_local_mm` + `q_reach_m3s` + `downstream_id` by the continuity identity in §6 and is the
one field that can be dropped without losing information.

## 8 — Handed to C1, and what C0 did not do

- Phase B is closed on H2E; `CLAUDE.md`, docs/20, docs/24 and docs/26 all say so in place.
- **Not done, deliberately, because C0 does not ask for it:** no `feasibility_H2E.csv` (the
  energy-floor test is a property of the bundle and gauge set, both identical to H2, so
  `feasibility_H2.csv` applies verbatim); no `h2e_minus_h2.csv` (docs/29 already settled the
  comparison on the objective, and a second matched-window table would invite reading a
  0.011 KGE move as a result when it is inside seed noise); no re-execution of nb14; no new
  figures — docs/31 C0.4 asks for tables, and `scripts/make_deck_charts.py` reads
  `metrics_fleet.csv`, so the deck picks H2E up on its next rebuild without new code.
- Next stage is **C1** (the SSC-quality gate) on the 28 mapped stations per the C1.0
  decision; it does not depend on anything C0 produced except the frozen hydrology, which is
  now on disk and re-verifiable in ~1 minute.
