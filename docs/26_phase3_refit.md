# 26 — Phase 3: the refit on the v2 forcing, and what H2 − H1 settled

Executed 2026-08-03. Notebooks 13 and 14 re-run on `model_inputs_v2/` with a revised
objective and two pre-registered forcing cells. Commits `74eb324` (nb13), `328f5e8`
(nb14 rebuild), `9fc227a` (nb14 execution). Closes [doc 18](18_hydrology_journal.md)
§8 items 1 and 18.

Read [doc 22](22_dry_phase_diagnosis.md) §4.4 and §4.6 first — this document is the
answer to the two defects recorded there.

---

## 1 — The design

Three configurations, differing in exactly one thing at a time:

| cell | forcing | objective | scored | gauges |
|---|---|---|---|---|
| reference | v1 | old | 2009–2017 | 61 — Config B as adopted, **not re-run**, its stored flows re-scored |
| **H1** | v1 | **new** | 2009–2017 | 61 |
| **H2** | **v2** | **new** | 2009–2018 | 63 |

H3 (v2 + CHIRPS-gauge merge) was **dropped, not faked**: the merge was never implemented
in nb11 — the areal mean is exactly the gauge-only figure and no quantile-mapping output
exists anywhere in the pipeline. It stays as item 20.

Search: DDS, 1,000 evaluations × 2 seeds × 2 cells = **4,000 model runs**, four concurrent
OS processes, 330 min wall, 19.7 s/eval. That is **5.2×** the v1 run's 774. Seed-to-seed
spread of the final objective 0.0065 (H1) and 0.0186 (H2) — 7 % and 19 % of the gain over
the prior.

## 2 — The three objective changes, and the two validations run before optimising anything

1. `k_bas` lower bound **15 d → 5 d**. The observed recession constant is 13.9 d (p10
   7.7 d), so the v1 box excluded the answer.
2. `k_int < k_bas` **by reparameterisation**: the search variable is the ratio
   `k_int/k_bas ∈ (0.02, 0.90)`, so every point in the box satisfies the ordering. A
   penalty or rejection was rejected — both pile probability mass on the constraint
   surface and break DDS's reflection at the bounds, which is what stops a boundary
   optimum from looking real. The prior maps exactly (8/60), so nb13 is still reproduced.
3. A **recession-signature term** at weight 0.20 on `1 − |ln(k_sim/k_obs)|/ln 2`,
   symmetric in log space so a recession twice too fast costs exactly what one twice too
   slow costs.

**Validation A — the two objective scales are comparable.** `calib_v2.blend_v1` reproduces
the v1 run's own recorded `F(prior) = 0.1276369667` to nine decimals, so old-scale and
new-scale values sit on one axis and the ladder below means something.

**Validation B — the recession estimator measures what doc 22 measured.** Written from doc
22 §4.4's prose and applied to the *stored* Config B flows:

| period | obs k | Config B sim k | ratio | doc 22 ratio |
|---|---|---|---|---|
| CAL 2012–14 | 10.40 d | 40.10 d | 3.86× | 3.9× |
| La Niña 2011 | 9.49 d | 27.30 d | 2.88× | 2.5× |
| El Niño 2015–16 | 11.93 d | 44.77 d | 3.75× | 4.2× |
| other 09/10/17 | 9.76 d | 31.43 d | 3.22× | 3.4× |

Absolute constants differ (10.4 d observed here against doc 22's ~13 d) because the
segment rule is reconstructed from a description. The **ratio** is what the objective and
the criterion use, and it reproduces to a mean 0.26×.

## 3 — What the objective change bought, and what it cost

Config B → H1: same forcing, same 61 gauges, same split, same algorithm. Only the
objective differs.

| | Config B | H1 |
|---|---|---|
| worst-period recession ratio | 3.86× | **1.27×** |
| El Niño α | 0.793 | **0.911** |
| store ordering | k_int 117.4 d > k_bas 68.6 d — **inverted** | k_sup 1.92 < k_int 13.02 < k_bas 53.73 d |
| El Niño KGE (59 common gauges) | 0.193 | **0.245** |
| VAL 2009–17 median KGE (59 common) | **0.454** | 0.423 |
| F on the OLD scale | **0.2429** | 0.2137 |
| F on the NEW scale | 0.1262 | **0.2368** |

The recession repair **holds on the held-out years** (La Niña 0.92×, El Niño 1.19×), which
is the non-circular part of the test — the ratio is both an objective term and criterion
F3, so only the validation periods count.

The cost is real and is the designed trade: 20 % of the objective now buys store realism,
so both new fits score below Config B on the old objective and give up ≈0.03 of validation
median KGE.

## 4 — H2 − H1: the deliverable

59 common gauges, matched 2009–2017 window, so neither the fleet nor the period is a
confound.

| metric | H1 (v1 forcing) | H2 (v2 forcing) | H2 − H1 |
|---|---|---|---|
| KGE | 0.3886 | 0.3668 | **−0.0218** |
| r | 0.5802 | 0.5836 | **+0.0033** |
| α | 0.9343 | 0.9168 | −0.0175 |
| β | 1.0885 | 1.0441 | **−0.0444** |
| PBIAS % | +8.85 | +4.41 | **−4.44** |
| recession ratio | 1.084× | 1.038× | −0.046× |

**The prediction registered before the run is CONFIRMED.** β moved 0.044 toward 1 and
PBIAS improved 4.4 points, while **r moved +0.0033 — nothing**.

> **Volume and correlation are independent problems in this basin.** Doc 22 §4.7 showed
> r pinned inside 0.556–0.572 across twelve *parameter* configurations. This adds that it
> does not move for a *rainfall-volume* change either. No further work on rainfall totals
> will move the ENSO contrast.

Stated without inflation: H2 also **loses** 0.022 KGE overall and 0.038 El Niño KGE
against H1. The repair is a volume improvement that costs a little daily fit, not a net
skill gain. Outside the matched comparison H2 gains 2018 as a validation year (KGE 0.235),
four gauges the co-located merge recovered, and two fewer gauges below their energy floor
(18 → 16).

## 5 — Criteria: 3/9 for both cells, against 0/9 for Config B

| | Config B | H1 | H2 |
|---|---|---|---|
| **P** El Niño skill-over-clim ≥ +0.12 and La Niña ≥ +0.24 | FAIL (−0.026 / +0.157) | FAIL (+0.026 / +0.126) | FAIL (+0.006 / +0.128) |
| **P′** El Niño ≥ ½ La Niña | FAIL | FAIL | FAIL |
| S1 El Niño KGE ≥ 0.35 | FAIL 0.193 | FAIL 0.245 | FAIL 0.207 |
| S2 validation KGE ≥ 0.50 | FAIL 0.450 | FAIL 0.421 | FAIL 0.346 |
| S3 El Niño α ≥ 0.90 | FAIL 0.793 | **PASS 0.911** | **PASS 0.910** |
| F1 0 of 10 railed | FAIL 3 | FAIL 2 | FAIL 2 |
| F2 k_int < k_bas | FAIL | **PASS** | **PASS** |
| F3 recession ≤ 1.5× | FAIL 3.86× | **PASS 1.27×** | **PASS 1.15×** |
| F4 kc_mult ≤ 1.2 | FAIL 1.999 | FAIL 1.982 | FAIL 1.896 |

The three that flipped are exactly the three the objective change targeted. Nothing else
moved, and the primary criterion fails in both its absolute and its ratio form.

### 5.1 The railing rule bites both cells — called as a failure

* **H1** rails `kc_mult` at 98.8 % of its range and drives `lai_mult` to 0.5 %, i.e.
  interception switched *off* so the canopy coefficient can evaporate more. That is the
  same compensating structure doc 22 §4.6 named, one knob over.
* **H2** rails `k_sup` at 99.8 % and `k_int_frac` at its 0.9 % floor, giving
  **k_sup 19.8 d > k_bas 13.7 d > k_int 0.28 d**. The ordering constraint is satisfied by
  construction and the search simply **relocated the inversion into the pair that was not
  constrained**. Constraining one ordering did not remove the compensation; it moved it.

Whatever skill H2 shows is partly bought by railing, and by the rule stated before the run
that is a failure. Anyone reading H2's numbers as a clean result is reading them wrong.

## 6 — A trap, and a measurement correction

**The day-of-year climatology benchmark here is not doc 22 §4.1's.** Built as the
(month, day) **mean** over the whole scored record, it scores CAL 0.344 / La Niña 0.242 /
El Niño 0.219 / other 0.259, against doc 22's 0.227 / 0.162 / 0.168 / 0.173 — **harder by
+0.051 to +0.117 KGE**. Doc 22 does not state its construction beyond "day-of-year … from
the whole record"; a median, or one built from a sub-window, is a weaker predictor.

Consequence, and it is not cosmetic: the primary criterion's absolute targets (+0.12,
+0.24) were set against the *easier* benchmark, so passing or failing them on this one is
not a like-for-like test of the pre-registered number. What *is* like-for-like is the
comparison between the three configurations, all scored against the same benchmark — and
on that comparison El Niño skill-over-climatology goes **−0.026 → +0.026 → +0.006**.

nb14 first printed "the benchmark is the same benchmark". It was wrong, it was corrected
before the notebook was committed, and the correction is in the executed record.

**Two engineering traps worth the next reader's time:**

* `pd.DatetimeIndex(frc['dates'])` is `datetime64[D]` while `pd.date_range` is
  `datetime64[ns]`, and `DatetimeIndex.equals` compares resolution. nb13's first run
  failed an assertion whose two sides **printed identically**. Cast the unit; never weaken
  the comparison to make it pass.
* The interpreter on this box is **`python3.10.exe`**, so `Get-Process python` reports
  nothing while four searches are running — which is how three duplicate worker batches
  ended up racing on the same output files. Shell-backgrounded children (`nohup … &`) die
  with the tool call; `Start-Process` and `schtasks` detach properly. DDS now
  checkpoints and resumes with a **verified replay** (each replayed proposal is asserted
  against the checkpoint), so a wrong liveness verdict costs nothing.

## 7 — What this leaves

**One lever.** Every measurement in this document says the deficit is in daily
**correlation**, not in volume, and correlation did not move for either the objective
change or the forcing repair. The CHIRPS-gauge merge is a correlation intervention and it
is the only untried one. Its gate is unchanged and pre-registered: **leave-one-out daily
r must beat the gauge-only 0.429** before it is worth re-running nb14 as H3.

Everything else on the table is either measured-and-refuted (doc 22 §4.4–§4.7), a named
limitation (celerity as a floodplain-storage surrogate, doc 18 §8 item 4), or a data
acquisition problem (IDEAM catalogue areas, doc 23 §13.2 — which is why **no per-gauge
sediment yield in t/km²/yr appears anywhere in nb14**).

Outputs: `data/processed/sim_baseline_v2/` and `data/processed/sim_calibrated_v2/`
(`calibration_v2.json`, `metrics_fleet.csv`, `h2_minus_h1.csv`, per-cell parameter and
feasibility tables, gauge flows including the climatology benchmark, and the full search
archives).

---

## Addendum (2026-08-10) — attempt 4: H2E adopted, reported, and frozen

Written by the **Stage C0** session (`docs/agents/journal_c0.md`), executing
[docs/31](31_phase_c_workplan.md) subtasks C0.1–C0.6. H2E was pre-registered in
[docs/29](29_seed_expansion.md) §3(b), passed all three of its decision rules, and was
adopted as Phase B's closing configuration by the team decision in
[docs/30](30_phase_c_plan.md) §1. This addendum is the report §5's table stops one attempt
short of. Nothing above this line was edited.

**Provenance.** `_calib_cache/dds_H2E_20260901.npz` (best of two seeds, F 0.25931 vs
0.24671). `src/mgb_hydrology.py` and `src/calib_v2.py` on disk are bit-identical to their
blobs at commit `80a7c10` (2026-08-03 20:34), which is the last commit touching either and
predates the H2E search (2026-08-04 23:04 → 2026-08-05 02:26). The SHAs recorded in
`calibration_v2.json` are nb14's, i.e. *before* `80a7c10` added the FAO-56 option — a
difference that is expected rather than drift, and is why the check that matters is
against the blob the search actually ran.

### A.1 The reproduction gate (C0.2) — passed exactly

Rebuilding `Cell('H2E')` and re-evaluating the archived best `x`:

| | value |
|---|---|
| archived F | `0.25930593639066796` |
| recomputed F | `0.25930593639066796` |
| relative difference | **0.000e+00** (bar: ≤ 1e-8, the docs/22 9.1e-9 harness bar) |
| stored per-gauge terms | all 3 × 63 (`k1`, `k2`, `k_sim`) reproduce **bit-for-bit**, NaN patterns identical |

The forcing cache had been cleaned up after the queue finished and was regenerated from
`model_inputs_v2/forcing.npz`; that the gate then reproduces the objective to the last bit
is also the evidence the regeneration is faithful, so no separate check was invented for it.

### A.2 The fitted set (C0.1) — `sim_calibrated_v2/parameters_H2E.csv`

`kc_mult` **1.6625** (77.5 % of its (0.5, 2.0) range) — the docs/29 result, confirmed off
the rail that held H1 at 98.8 % and H2 at 93.3 %. Railed: **2 of 10 global**
(`k_sup` 99.1 %, `k_int_frac` at its 0.02 floor, position 0.19 %), **3 of 18 dimensions**
(adding `wm_mult@R2` at 97.1 %) — both denominators stated, because reporting only one is
what produced the docs/24-vs-docs/26 "3 vs 2" discrepancy.

**The store-ordering inversion relocated a third time.** `k_sup` 19.20 d, `k_int` 0.87 d,
`k_bas` 42.97 d. `k_int < k_bas` holds by construction, and unlike H2 the fit no longer puts
`k_sup` above `k_bas` — but surface response is now **22× slower than interflow**, which is
inverted in the pair the constraint still does not cover. This is the third instance of the
precedent in §5.1 and in docs/21 open item 12: **a constrained ordering relocates
compensation, it does not remove it.** It holds for the configuration the project has
adopted, not only for the ones it rejected.

### A.3 Full-period metrics (C0.3) — `metrics_fleet.csv`, 12 new rows

Engine run over 2008–2018, 2008 warm-up, 2009–2018 scored, 63 gauges. Mass-balance residual
**9.66e-17** relative (bar < 1e-15); the negative-W guard never fired; RC 0.5127. Both a
`prior` and a `fit` block were written, as for H1 and H2 — the FAO-56 prior is not H2's
prior, so it is a measurement rather than a duplicate.

Recession is reported on **both** definitions in circulation, because they are not
equivalent and picking one after the fact would be a choice: `metrics_fleet.rec_ratio` is
nb14's **ratio of medians**; docs/29 rule (b)2's 1.08/1.11 figures are the **median of
ratios**. Every period passes ≤ 1.5× on both (worst 1.17).

### A.4 (a) The four-attempt history, VAL-all row

| attempt | VAL KGE | NSE | r | α | β | PBIAS % | rec ratio | skill over clim | railed (global / all 18) |
|---|---|---|---|---|---|---|---|---|---|
| 1 — Config B (v1, old objective) | **0.450** | 0.256 | 0.646 | 0.866 | 1.068 | +6.83 | **2.98×** | +0.199 | 3 / — |
| 2 — H1 (v1 + new objective) | 0.421 | 0.179 | 0.607 | 0.941 | 1.064 | +6.36 | 0.96× | +0.170 | 2 / 2 |
| 3 — H2 (v2 + new objective) | 0.346 | 0.161 | 0.583 | 0.911 | 1.073 | +7.34 | 1.01× | +0.079 | 2 / 3 |
| **4 — H2E (v2 + new objective + FAO-56 ET)** | **0.356** | 0.130 | 0.591 | 0.905 | **1.035** | **+3.51** | 0.98× | +0.089 | 2 / 3 |

Read honestly, H2E's gain over H2 is **in volume, not in skill**: β 1.073 → 1.035 and PBIAS
+7.34 → **+3.51 %**, the best of the four attempts, while VAL KGE moves +0.011 and r +0.008
— both inside the 0.051 seed spread docs/29 measured, so neither is a separation. The r
ceiling (docs/22 §4.7) is untouched, exactly as predicted.

Two further honest readings, stated here so nobody has to find them:

* H2E's own **prior** scores VAL-all KGE 0.3576, marginally *above* the fitted 0.3563. The
  fit is still the right set: the prior buys that KGE with PBIAS **+24.4 %** and a recession
  1.49× too slow, against the fit's +3.5 % and 0.98×. It is the Config B story one level
  down, and it is why this project reports the ratio next to the skill.
* Applying §5's nine criteria unchanged, **H2E scores 3/9** — the same three as H1 and H2
  (S3 El Niño α 0.911, F2 `k_int < k_bas`, F3 recession 1.08× on CAL), and it still fails F4
  (`kc_mult` 1.662 > 1.2) and F1 (2 railed). Adoption was on the docs/29 rules, which H2E
  passed; it was never a claim that the pre-registered adequacy criteria were met.

### A.5 (b) ENSO asymmetry for H2E — the number Phase C inherits

| | La Niña 2011 | El Niño 2015–16 | La Niña − El Niño |
|---|---|---|---|
| median KGE | 0.344 | 0.200 | +0.144 |
| day-of-year climatology KGE | 0.238 | 0.201 | +0.037 |
| **skill over climatology** | **+0.106** | **−0.0005** | **+0.107** |
| r | 0.652 | 0.585 | +0.067 |
| α | 0.996 | 0.911 | +0.085 |
| β | 0.946 | 1.075 | −0.129 |
| PBIAS % | −5.42 | +7.48 | −12.89 |
| gauges | 59 | 54 | |

**The dry phase in the adopted configuration is at climatology, not above it: −0.0005.**
Across attempts 2 → 3 → 4 the El Niño skill-over-climatology reads +0.026 → +0.006 →
−0.0005. The deck's slide-9 argument ("the dry phase turns from worse-than-climatology to
better") was measured on attempt 1 → attempt 2 and remains true *of that comparison*; it is
**not** true of the configuration the project adopted, and docs/24 must not be read as
claiming it is. This is the hydrology caveat every Phase C sediment claim inside the El Niño
window inherits, and docs/31 C5.2 is where it gets propagated quantitatively.

The asymmetry itself — La Niña beating its climatology by +0.106 while El Niño merely matches
it — is the honest statement of the ENSO contrast at the hydrological level: **the wet phase
is predictable, the dry phase is not**, and the cause is the input ceiling (docs/22 §4.7),
not a parameter.

### A.6 Frozen sediment drivers (C0.5)

`sim_calibrated_v2/h2e_drivers.npz` (546 MB, gitignored; regenerate with
`python3.10 src/build_h2e_drivers.py`). Five per-minibacia daily fields on the scored axis,
(3652, 8672) float32 each — `qsur_gen_mm`, `qsur_rel_mm`, `q_local_mm`, `reach_inflow_m3s`,
`q_reach_m3s` — plus topology, gauge indices and a JSON `meta` block. Two surface fields
because MUSLE's `Qsurf` is ambiguous between *generated* and *reservoir-released* surface
runoff and docs/31 C3.3 has not registered its choice yet; storing one would defeat the
point of precomputing. `reach_inflow_m3s` is redundant with
`q_local_mm` + `q_reach_m3s` + `downstream_id` by the continuity identity below, and is kept
because C0.5 names it and because the redundancy is what makes that check possible.

Produced by `src/mgb_drivers.py`, which drives the **frozen** engine's own
`_vertical_step` / `_reservoir_step` / router rather than modifying it, and whose discharge
and all ten basin series are asserted **bit-identical** to `mgb_hydrology.simulate`'s on the
same inputs. Gates: identity 0.000e+00; area-weighted column sums against the run's own
basin series, worst relative 5.8e-8; per-reach continuity
(`inflow = local + Σ upstream outflow`, computed from the stored fields alone) worst 1.2e-7;
`np.load` round trip exact, no NaNs, no negatives. Basin-mean 650 mm/yr generated surface
runoff against 1,038 mm/yr total local runoff. The file is larger than docs/31 C0.5's
"~250 MB" estimate because that estimate assumed three fields, not five.

Outputs added by this addendum: `parameters_H2E.csv`, `q_gauge_H2E.npz`, `report_H2E.json`,
`h2e_drivers.npz`, and 12 rows in `metrics_fleet.csv` — where the 27 pre-existing rows are
byte-for-byte unchanged, a pandas read/write round trip having been measured to re-emit them
3 ULP different and replaced with a text-level append.
