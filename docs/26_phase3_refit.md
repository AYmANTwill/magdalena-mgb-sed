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
