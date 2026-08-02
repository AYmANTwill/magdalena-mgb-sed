# 18 — Hydrology journal: water balance, calibration, and the dry-phase diagnosis

The Phase B record. What was built (`src/mgb_hydrology.py`, notebooks 13–14), what the calibration
actually achieved, and — the reason this document exists — **why the El Niño 2015–16 half of the
ENSO contrast fails, measured rather than argued**.

Companion to [doc 16](16_forcing_pipeline_audit.md) (forcing) and
[doc 17](17_discharge_qc_audit.md) (discharge). Same rule as those two: findings that did not
survive measurement are in [§6 Checked and refuted](#6--checked-and-refuted), not deleted.

Read §4 first if you are picking this up cold: **all three standing hypotheses for the dry-phase
failure are wrong, and one of them is backwards.** The binding constraint is the daily correlation
`r ≈ 0.57`, which no parameter in the model can move.

---

## 1 — Current state

| Component | State |
|---|---|
| Engine `src/mgb_hydrology.py` | **Verified.** Mass closes to 1.4×10⁻¹⁷ relative; numpy and numba routers agree exactly; 16 s for a 3,653-day × 8,672-minibacia run |
| Calibration (nb14) | **Complete.** Klemeš differential split, fitted on neutral 2012–14 only; both ENSO phases are out-of-sample |
| Validation skill | median KGE **+0.450**, NSE +0.256, PBIAS +6.8 % (unfitted prior: +0.253 / −0.279 / +45.2 %) |
| Overfitting | excess degradation vs the unfitted reference **+0.011** median KGE — negligible |
| La Niña 2011 | KGE **+0.399**, α 0.981, β 0.980 — works |
| El Niño 2015–16 | KGE **+0.193**, α 0.793, β 1.084 — ❗ the blocker |
| Dry-phase diagnosis | **Complete** (§4–§6). Cause is *not* recession, *not* gauge error, *not* seasonal forcing inflation |
| Recession realism | ❗ **Newly found defect.** Simulated low-flow recession 48.6 d against 14 d observed, in *every* period |
| Parameter bounds | ❗ `kc_mult` railed at its 2.00 ceiling, `k_int` at 117.4/120, `lai_mult` 4.40/5.0 |
| Store ordering | ❗ `k_int` (117.4 d) **slower than** `k_bas` (68.6 d) — physically inverted |
| Phase C (sediment) | Still blocked — on mainstem SSC data and on the doc 19 `calibration_safe` gate |

Nothing in `data/processed/` was modified by the diagnostic work in §4–§6: every experiment
rebuilt parameters in memory from `sim_calibrated/minibacia_params.npz` and discarded the result.

---

## 2 — What was built

### 2.1 `src/mgb_hydrology.py` — the water-balance engine

A daily MGB-SA water balance over 8,672 minibacias × 24 URH, with Muskingum-Cunge (X=0) routing on
the D8 network from notebook 07. Structure, per URH cell per day:

1. **canopy** — interception store `Simax = alpha_int × LAI`, evaporated at PET before anything else;
2. **saturation excess** — variable contributing area `Asat = 1 − (1 − W/Wm)^b`, plus any overflow
   above `Wm`;
3. **evapotranspiration** — `min(kc · PET_soil · W/Wm, W)`, so ET is supply-limited as the soil dries;
4. **percolation** — `linear` mode: `drain = adr · W`, split `fint` to interflow and the rest to
   groundwater;
5. **three linear reservoirs** at the minibacia (`k_sup`, `k_int`, `k_bas`), exact release
   coefficient `1 − e^{−Δt/K}`;
6. **routing** — within-day topological sweep, 292 levels, vectorised level by level.

The negative-`W` guard returns its own magnitude rather than swallowing it, so any real clipping
appears as a non-zero term in the mass balance instead of hiding inside it. It has never fired.

**The engine is the one part of Phase B that is not in doubt.** `src/test_mgb_hydrology.py` checks
the recession constant analytically, not just its shape; mass closes to 1.4×10⁻¹⁷ relative on the
calibrated parameter set, which is a fresh test of the guards rather than of the algebra.

### 2.2 Notebook 13 — baseline run

The unfitted prior: `adr` 0.06, `fint` 0.60, `b` 0.60, `k_sup/int/bas` 1.5/8/60 d, celerity
1.0 m/s, FAO-56 `kc` and per-class LAI. Fleet median KGE 0.253 on validation, β 1.452 —
**bias is one-signed at 53 of 61 gauges**, so the first thing calibration had to move was the water
partition, not the timing.

### 2.3 Notebook 14 — calibration

| | |
|---|---|
| split | fit on **2012, 2013, 2014 only** (1,096 d), warm-up 2011 |
| validation | 2009, 2010, **2011 (La Niña)**, **2015–16 (El Niño)**, 2017 (2,191 d) |
| why | Klemeš (1986) differential split-sample: the ENSO extremes the project studies are never seen by the objective, so the contrast is a *prediction* |
| objective | mean over gauges of `(1−w)·C2M(KGE(Q)) + w·C2M(KGE(log(Q+q0)))`, `w=0.5`, `q0 = 0.01·mean Q` |
| bounded transform | `C2M(k) = k/(2−k)` (Mathevet et al. 2006) — stops one hopeless gauge dominating |
| algorithm | DDS (Tolson & Shoemaker 2007), `r=0.2`, 2 seeds × 178/209 evaluations = **774 model runs**, 63 min |
| screening | Morris elementary effects, 6 trajectories, 8 levels; 10/10 parameters survived, none frozen |
| adopted | **Configuration B** — 18 free parameters: global set + 3 macro-regions on `k_sup`, `wm_mult`, `celerity` + IGAC-soil-family split on `adr` |

Effective sample size is the honest number here: 53,499 gauge-days of calibration data, but a
lag-1 daily autocorrelation of 0.80 reduces that to **5,916 effective observations** for 18
parameters.

### 2.4 Skill, as measured

Median over the 61 calibration-safe gauges:

| period | KGE | NSE | r | α | β | PBIAS % |
|---|---|---|---|---|---|---|
| unfitted prior, VAL | +0.253 | −0.279 | 0.584 | 1.186 | 1.452 | +45.2 |
| calibrated, CAL 2012–14 | +0.291 | +0.045 | 0.522 | 0.866 | 1.001 | +0.1 |
| calibrated, VAL all | **+0.450** | +0.256 | 0.646 | 0.866 | 1.068 | +6.8 |
| calibrated, La Niña 2011 | +0.399 | +0.225 | 0.653 | 0.981 | 0.980 | −2.0 |
| calibrated, El Niño 2015–16 | **+0.193** | −0.078 | 0.569 | 0.793 | 1.084 | +8.4 |
| calibrated, other 09/10/17 | +0.446 | +0.170 | 0.650 | 0.878 | 1.079 | +7.9 |

Validation scores *higher* than calibration (−0.159 change), which means the calibration years are
intrinsically the harder ones. The control for that is the unfitted prior, which changes −0.170
over the same two periods with no fitting at all; the overfitting statistic is the **excess** over
that reference, **+0.011**.

---

## 3 — The hard limit found before any fitting

The engine cannot evaporate more than `max(1, kc) · PET`. Closing the observed water balance at
CALAMAR needs 1,300 mm/yr of ET against an ERA5-Land PET of 1,251 mm/yr — a deficit of
**49 mm/yr**. Consequences, all measured in nb14 §1:

* **18 of 61** gauges have an observed runoff coefficient below their own energy floor;
* outlet PBIAS can never fall below **+5.6 %** with this forcing;
* the fitted `kc_mult` of 1.9994 is partly absorbing that inconsistency, not only representing
  forest transpiration.

§4.3 shows this floor is real but is **not** what breaks the dry phase.

---

## 4 — The dry-phase diagnosis

The study is a wet-vs-dry ENSO contrast and only the wet half worked. Three hypotheses were
standing when this diagnosis began. All three are now refuted, and one is backwards.

Everything below was produced by rebuilding the adopted Config B parameters in memory from
`sim_calibrated/minibacia_params.npz` and re-running the engine one factor at a time. The harness
reproduces the stored `q_sim_B_m3s` to a **median relative error of 9.1×10⁻⁹** — it was not allowed
to interpret anything until it did.

### 4.1 First: the yardstick is not symmetric

`NSE = −0.078` was being read as "worse than predicting the mean". Before accepting that, the same
window was scored for a **day-of-year climatology** benchmark built from the whole record — the
thing a hydrologist would actually have to beat:

| period | model KGE | model NSE | climatology KGE | climatology NSE | obs CV | model − clim (KGE) |
|---|---|---|---|---|---|---|
| CAL 2012–14 | 0.291 | +0.045 | 0.227 | +0.141 | 0.657 | +0.064 |
| La Niña 2011 | 0.399 | +0.225 | 0.162 | +0.021 | 0.617 | **+0.236** |
| El Niño 2015–16 | 0.193 | −0.078 | 0.168 | **−0.062** | **0.799** | **+0.024** |
| other 09/10/17 | 0.446 | +0.170 | 0.173 | +0.135 | 0.709 | +0.274 |

A perfect seasonal climatology *also* scores NSE −0.062 in the El Niño window, because that window
has the highest observed CV (0.799) and NSE's benchmark variance changes with it. **NSE is not
comparable across these windows.** About a third of the headline gap is the metric.

The honest statement of the deficit is the last column: the model adds **+0.024** KGE over
climatology in El Niño against **+0.236** in La Niña. That is still a real and large failure — it
is just not "worse than the mean".

### 4.2 Which term collapses: α, not β

Repairing each KGE term in turn, median over gauges:

| period | KGE as-is | + bias removed | + variance matched (= r) |
|---|---|---|---|
| CAL 2012–14 | 0.291 | 0.381 | 0.522 |
| La Niña 2011 | 0.399 | 0.496 | 0.653 |
| **El Niño 2015–16** | **0.193** | 0.294 | **0.569** |
| other 09/10/17 | 0.446 | 0.480 | 0.650 |

Bias is worth +0.101; **variance is worth +0.275**. And the error is concentrated at low flow —
bias by observed-flow quantile bin, as % of observed:

| bin | CAL | La Niña | **El Niño** | other |
|---|---|---|---|---|
| Q0–10 | +152 | +127 | **+244** | +164 |
| Q10–30 | +89 | +76 | +115 | +79 |
| Q30–50 | +59 | +47 | +80 | +56 |
| Q50–70 | +36 | +31 | +49 | +37 |
| Q70–90 | +11 | +15 | +14 | +16 |
| Q90–100 | −25 | −12 | −27 | −12 |

The model triples the lowest flows in the dry phase, and undershoots the highest ones. That single
pattern produces both α < 1 and β > 1.

### 4.3 Hypothesis (b) is backwards — CONFIRMED

The brief recorded the 18 energy-floor gauges as *"observed dry-season Q exceeds what P − PET can
supply, which points at gauge/rating error"*. `feasibility_gauge.csv` says the opposite:

```
18 of 61 gauges fail the energy test.
  observed rc BELOW its floor (model forced too WET) : 18
  observed rc ABOVE its floor                        :  0
  mass_ok False (obs Q exceeds P)                    :  1
```

All 18 fail because the observed runoff coefficient is **below** the minimum the forcing permits —
the forcing supplies more water than the rivers carry. Worst case is 22017010: rc 0.161 against a
floor of 0.500, a +210 % PBIAS floor. This is the signature of **too much precipitation or too
little PET**, not of gauges under-reporting. Exactly one gauge in 61 has observed Q exceeding P.

That surplus is real, and those 18 gauges are genuinely worse in the dry phase (median β 1.756
against 0.922 for the feasible ones). But it does not explain the ENSO contrast — see §4.5.

### 4.4 Hypothesis (a): the recession defect is real, and it is not the cause — CONFIRMED

Fitting a linear-reservoir constant to ≥3-day monotone declines below the 40th flow percentile:

| period | observed k | simulated k | ratio |
|---|---|---|---|
| CAL 2012–14 | 13.2 d | 51.7 d | 3.9× |
| La Niña 2011 | 13.6 d | 33.9 d | 2.5× |
| El Niño 2015–16 | 15.0 d | 63.3 d | 4.2× |
| other 09/10/17 | 13.2 d | 44.8 d | 3.4× |

**The simulated recession is 3–4× too slow in every period** — a defect not previously recorded.
Observed spread across gauges is p10 7.7 d / median 13.9 d / p90 26.8 d; by region 13.5 / 9.0 /
15.9 d. So there *is* regional structure, but it spans 1.8×, while the global level is wrong by
3.5×. **The problem is the level, not the missing regionalisation.**

Then the direct test — sweep `k_bas`, everything else frozen at Config B, 10 full runs:

| configuration | CAL | La Niña | **El Niño** | other | sim k |
|---|---|---|---|---|---|
| Config B as adopted (68.6 d) | 0.291 | 0.399 | **0.193** | 0.446 | 48.6 d |
| k_bas = 12 d | 0.283 | 0.386 | 0.217 | 0.437 | 25.5 d |
| k_bas = 25 d | 0.305 | 0.400 | **0.227** | 0.461 | 33.5 d |
| k_bas = 45 d | 0.314 | 0.385 | 0.208 | 0.455 | 43.1 d |
| k_bas = 100 d | 0.286 | 0.397 | 0.184 | 0.427 | 52.7 d |
| k_bas regionalised to **observed** recession | 0.281 | 0.387 | 0.214 | 0.444 | 24.9 d |

Correcting `k_bas` to the value the observations imply buys **+0.021** KGE in El Niño. The best
value found anywhere in the sweep buys **+0.034**. The gap to La Niña is 0.206. **Hypothesis (a)
closes at most 16 % of it.**

Why the objective never found this: Morris `mu*` for `k_bas` is **0.044**, rank 5 of 10 and five
times below `k_sup` (0.228) and `adr` (0.225). The daily-KGE objective barely sees the parameter,
so the fitted 68.6 d is essentially the 60 d prior default carried through.

Note also that `k_bas`'s **lower bound is 15 d while the observations imply 13.9 d** — the search
space excludes the right answer.

### 4.5 Hypothesis (c): the inflation is real and period-invariant — CONFIRMED

Doc 16 §11 measured +18.3 pts of IDW wet-day inflation and the brief expected it to *"bite hardest
in the dry season"*. Leave-one-out IDW (k=6, inverse distance squared) at the 294 QC'd precip
gauges — observations only, so this cannot inherit an error from the forcing pipeline:

| window | gauges | LOO r | LOO bias % | wet-day obs % | wet-day IDW % | **inflation pts** |
|---|---|---|---|---|---|---|
| La Niña 2011 | 207 | 0.45 | +4.9 | 49.1 | 68.0 | **+18.9** |
| El Niño 2015–16 | 217 | 0.40 | +3.6 | 36.7 | 54.4 | **+17.7** |
| neutral 2012–14 | 240 | 0.38 | +0.7 | 41.3 | 60.2 | **+18.9** |

The inflation is **+17.7 to +18.9 pts in every window** and is, if anything, marginally *smaller*
in the El Niño window. It cannot explain an ENSO contrast.

The volume story fails the same way. Mean `sim − obs` per gauge, converted to mm/yr of catchment:

| period | observed mm/yr | excess mm/yr | excess % |
|---|---|---|---|
| CAL 2012–14 | 925 | +0.6 | +0.1 |
| La Niña 2011 | 1,474 | −30 | −2.0 |
| El Niño 2015–16 | 630 | +38 | **+8.4** |
| other 09/10/17 | 1,037 | +62 | **+7.9** |

**"other 09/10/17" carries the same relative excess as El Niño (+7.9 % vs +8.4 %) and scores KGE
0.446 against 0.193.** Volume bias is not the discriminator.

And every knob that removes water fixes β at α's expense — 11 more full runs:

| configuration | CAL | La Niña | **El Niño** | other | EN α | EN β |
|---|---|---|---|---|---|---|
| Config B as adopted | 0.291 | 0.399 | **0.193** | 0.446 | 0.793 | 1.084 |
| P × 0.90 | 0.277 | 0.365 | 0.212 | 0.347 | 0.649 | 0.915 |
| P × 0.85 | 0.299 | 0.315 | 0.257 | 0.324 | 0.583 | 0.833 |
| P zeroed below 2.0 mm/d | 0.280 | 0.380 | 0.179 | 0.423 | 0.774 | 1.024 |
| kc × 1.20 (`kc_mult` → 2.40) | 0.286 | 0.383 | 0.177 | 0.427 | 0.766 | 1.015 |

Drizzle removal below 2 mm/d strips only 3.0 % of total precipitation and moves nothing. P × 0.85
does raise El Niño to 0.257 — by destroying La Niña (0.399 → 0.315) and the other years
(0.446 → 0.324). There is no water-volume setting that improves the contrast.

### 4.6 What the calibration actually did: compensating errors

Where the search left each parameter inside its own range:

| parameter | prior | fitted B | range | position |
|---|---|---|---|---|
| `kc_mult` | 1.00 | **1.9994** | 0.50 – 2.00 | **100.0 % — railed** |
| `k_int` | 8.0 | **117.39** | 1.5 – 120 | **99.5 % — railed** |
| `lai_mult` | 1.00 | 4.400 | 0.0 – 5.0 | 88.0 % |
| `adr` | 0.060 | 0.0689 | 5e-4 – 0.30 | 77.0 % |
| `k_sup` | 1.50 | 6.634 | 0.20 – 20.0 | 76.0 % |
| `k_bas` | 60.0 | 68.64 | 15 – 600 | 41.2 % |
| `celerity` | 1.00 | **0.221** | 0.05 – 4.00 | 33.9 % |
| `fint` | 0.60 | **0.0868** | 0.05 – 0.95 | **4.1 % — near floor** |

Read together: **every water-disposal knob is at its ceiling and every damping knob is pushed
toward maximum damping.** `kc_mult` and `lai_mult` are the two ways the model can evaporate more,
and both are pinned. `k_int` is railed at 120 d — *slower than* `k_bas` at 68.6 d, which is
physically inverted, interflow being by definition the faster path. `fint` then sits near its floor,
starving that inverted store and partly undoing the rail. Celerity is 4.5× below its prior, which
nb14 §4.3 already identified as a floodplain-storage surrogate for the Mompós reach.

This is a compensating-error structure: the forcing supplies more water than the rivers carry
(§4.3), the search evaporated as much as its bounds allowed, and smeared the residue out in time so
the peaks would not overshoot. Smearing costs variance. In neutral years α lands at 0.866, which is
tolerable. In the dry phase, when true flow is low and spiky, the same smearing is fatal.

De-damping directly, 8 more runs:

| configuration | CAL | La Niña | **El Niño** | other | EN r | EN α | sim k |
|---|---|---|---|---|---|---|---|
| Config B as adopted | 0.291 | 0.399 | **0.193** | 0.446 | 0.569 | 0.793 | 48.6 d |
| k_int = 15 d | 0.294 | 0.395 | 0.201 | 0.450 | 0.570 | 0.806 | 45.8 d |
| celerity = 1.0 m/s | 0.282 | 0.399 | 0.195 | 0.451 | 0.569 | 0.802 | 45.4 d |
| **k_int 15 + k_bas 25** | **0.307** | 0.399 | **0.216** | **0.462** | 0.564 | **0.890** | 31.0 d |
| k_int 15 + k_bas 25 + celerity 1.0 | 0.310 | 0.391 | 0.217 | 0.434 | 0.564 | 0.895 | 28.7 d |

De-damping the stores recovers most of the α gap (0.793 → 0.890) and improves **three of four
periods at once** — CAL +0.016, El Niño +0.023, other +0.016, La Niña unchanged. It is free skill.
It is also small.

### 4.7 The binding constraint: r ≈ 0.57, and nothing moves it

Across **all 12 parameter configurations** tested in §4.4–§4.6 — `k_bas` from 8 to 100 d, `k_int`
from 5 to 117 d, celerity from 0.22 to 2.0 m/s, `fint`, `kc`, and P scaled from 0.80 to 1.00 — the
El Niño correlation stayed inside **0.556 – 0.572**.

Once α and β are repaired, KGE *is* r (§4.2). So r = 0.57 is the ceiling on the dry phase, and it
is not a parameter property.

Two measurements locate it in the forcing:

* **Anomaly correlation.** Removing the day-of-year climatology from both observed and simulated
  flow leaves r = 0.476 in El Niño against 0.541 in La Niña. Only 16 % of r is seasonality, so this
  is genuine daily skill — and it is genuinely lower in the dry phase.
* **The rainfall field's own ceiling.** LOO IDW skill at the gauges is r = 0.40 in the El Niño
  window against 0.45 in La Niña (§4.5). Inter-gauge correlation of daily rainfall is 0.33 even at
  0–25 km separation, and 0.25 at 25–50 km — against a mean gauge spacing of roughly 30 km.

The model's catchment-scale anomaly correlation (0.476) sits just above the point-scale skill of
the rainfall field driving it (0.40). **The model is at its input's ceiling.** No parameter set can
exceed it, and the 0.05 drop in field skill from La Niña to El Niño is the same order as the 0.065
drop in the model's anomaly correlation.

---

## 5 — Verdict and what to do next

**The dry-phase failure is not one cause.** It decomposes as:

| share | cause | evidence | fixable by |
|---|---|---|---|
| ~⅓ of the headline | the NSE yardstick is not symmetric across windows | climatology also scores NSE −0.062 there (§4.1) | reporting against a benchmark, not raw NSE |
| the recoverable part | α collapse from a compensating-error calibration | α 0.793; de-damping recovers 0.890 (§4.6) | constraining the stores — worth ≈ +0.023 |
| the hard floor | r = 0.57, inherited from the rainfall field | invariant over 12 configurations; LOO IDW r = 0.40 (§4.7) | **only a better rainfall field** |

Ranked by measured payoff:

1. **Stop tuning parameters for the dry phase.** §4.7 puts a hard ceiling on what they can buy. The
   remaining parameter gain is ≈ +0.02, already located.
2. **Adopt the de-damped store set** (`k_int` 15, `k_bas` 25) — it improves three of four periods
   simultaneously and costs nothing. It should be *re-fitted*, not hand-set, under item 3.
3. **Add a recession-signature term to the objective.** `k_bas` and `k_int` are invisible to
   daily KGE (Morris `mu*` 0.044 and 0.032, ranks 5 and 8 of 10) and are therefore set by the prior,
   not the data. Constrain them against the observed 13.9 d recession instead. Also **lower the
   `k_bas` bound below 15 d** — it currently excludes the observed value — and **impose
   `k_int < k_bas`** so the search cannot invert the stores again.
4. **Fix the rainfall field.** This is the only lever measured to be capable of moving r, and it
   was already the top item on nb14's carried-forward list. The CHIRPS–gauge merge plus the four
   SNHT segment exclusions from doc 17, then re-run notebook 11 → 12 → 13 → 14.
5. **Raise the `kc_mult` ceiling only together with a PET review.** It is railed at 2.00, meaning
   the search wanted more ET than allowed; but §4.5 shows more ET alone makes El Niño *worse*
   (0.193 → 0.177 at kc × 1.20). The energy deficit is an input problem, not a bound problem.
6. **Report the ENSO contrast against a climatology benchmark.** "NSE < 0" overstates the failure;
   "+0.024 vs +0.236 KGE over climatology" is the defensible statement.

---

## 6 — Checked and refuted

Recorded because each looked right before it was measured.

| claim | status | what the measurement said |
|---|---|---|
| "18 gauges have observed Q above what P − PET can supply → gauge/rating error" | ❌ **backwards** | All 18 fail in the opposite direction: observed rc is *below* its floor. Only 1 of 61 has obs Q > P (§4.3) |
| "`k_bas` is global but should be regional; that is the dry-phase cause" | ❌ refuted | Regionalising to the observed recessions buys +0.021 KGE. The *level* is wrong by 3.5×, not the regionalisation, and even fixing the level buys ≤ +0.034 (§4.4) |
| "IDW wet-day inflation bites hardest in the dry season" | ❌ refuted | +18.9 / +17.7 / +18.9 pts in La Niña / El Niño / neutral — period-invariant, marginally smaller in El Niño (§4.5) |
| "The dry phase fails because of a constant water surplus divided by a smaller flow" | ❌ refuted | "other 09/10/17" carries the same +7.9 % excess and scores 0.446 against 0.193 (§4.5) |
| "The model is worse than predicting the mean in El Niño" | ⚠️ **misleading** | True of NSE, but a day-of-year climatology also scores −0.062 there. The window's obs CV is the highest of the record (§4.1) |
| "Most of the model's r is basin-wide seasonality" (nb14 §10.4 framing) | ⚠️ **overstated** | Removing the day-of-year climatology leaves r = 0.476 of 0.569 in El Niño. Seasonality is 13–17 % of r, not most of it |
| "`identifiability.csv` shows all 10 parameters identified" | ⚠️ **confounded** | `iqr_frac_of_range` is exactly 0.0 for 7 of 10 parameters. The top 5 % of a **DDS** archive is a neighbourhood of the optimum by construction, so this measures search concentration, not information in the data. Morris `mu*` is the trustworthy screen, and it says `k_bas`, `k_int`, `kc_mult` and `fint` are weak |

---

## 7 — Traps for whoever picks this up

1. **Never compare NSE across windows with different observed variance.** NSE's benchmark is the
   within-window mean, so the metric changes when the window does. Score a fixed benchmark
   (day-of-year climatology) in every window and report the difference.
2. **A parameter surviving Morris screening is not a parameter the data constrained.** `k_bas`
   survived with `mu*` = 0.044 against `k_sup`'s 0.228 — a factor of five. Surviving means
   "detectable", not "identified".
3. **Do not read a DDS archive as a posterior.** DDS is greedy; its top 5 % is a ball around the
   optimum. Any IQR-based identifiability statistic computed from it will report near-zero width
   regardless of what the data actually say.
4. **Check parameter positions against their bounds before interpreting any fitted value.** Three of
   ten are railed here, and a railed parameter is reporting the bound, not the basin.
5. **A calibrated model can be right for the wrong reasons in one regime and visibly wrong in
   another.** The α/β trade in §4.5 is the diagnostic: if fixing bias breaks variance, the fit was
   compensating for an input error, not representing a process.
6. **Before blaming a process, check whether the metric's ceiling is set by the input.** Twelve
   parameter configurations left r inside 0.016 of each other. That flatness *is* the finding.
7. The harness in any re-run must reproduce the stored `q_sim_B_m3s` before its output is
   interpreted — 9.1×10⁻⁹ median relative error was the bar used here.

---

## 8 — Open items

| # | item | blocks |
|---|---|---|
| 1 | Re-fit with a recession-signature objective term, `k_int < k_bas` constraint, and a `k_bas` lower bound below 15 d | the ≈ +0.02 parameter gain, and store realism |
| 2 | CHIRPS–gauge merged rainfall (nb11 → 12 → 13 → 14) | **r, and therefore the dry phase** |
| 3 | Extend the model period to 2008–2018 — precipitation already spans it, ERA5 `era5land_ext_*` is 132/132 on disk, but `forcing_minibacia_pet.csv` still stops at 2017-12-31, so nb11 must be re-run first | 2008 spin-up + a 2018 validation year |
| 4 | Local-inertial routing for the Mompós / La Mojana reach | celerity being used as a floodplain-storage surrogate |
| 5 | PET review against the 49 mm/yr basin ET deficit | the +5.6 % outlet PBIAS floor and the 18 infeasible gauges |
| 6 | `build_discharge_gauges.py:149-152` and `build_precip_gauges.py:62` rely on pandas date inference; use `src/dhime_dates.py` | latent day/month transposition on any non-ISO export |
