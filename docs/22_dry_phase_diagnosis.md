# 22 — The dry-phase diagnosis

Split out of [doc 18](18_hydrology_journal.md) §4 when that document passed 65 KB. This is
the measured diagnosis of why the El Niño 2015–16 half of the ENSO contrast fails, and it is
the document to read before touching calibration.

**All three standing hypotheses were tested against 30 full model runs and all three failed;
one was backwards.** The binding constraint is the daily correlation `r ≈ 0.57`, which no
parameter in the model can move.

Subsection numbers are kept as §4.x so every cross-reference written before the split
still resolves.

Context and everything downstream of this diagnosis stays in doc 18: §5 verdict, §6 refuted
claims, §7 traps, §8 open items, §9–§12 the forcing follow-up (surplus, repair, IDW
determinism, gauge triage).

---

## 4 — The dry-phase diagnosis

The study is a wet-vs-dry ENSO contrast and only the wet half worked. Three hypotheses were
standing when this diagnosis began. All three are now refuted, and one is backwards.

Everything below was produced by rebuilding the adopted Config B parameters in memory from
`sim_calibrated/minibacia_params.npz` and re-running the engine one factor at a time. The harness
reproduces the stored `q_sim_B_m3s` to a **median relative error of 9.1×10⁻⁹** — it was not allowed
to interpret anything until it did.

### 1 First: the yardstick is not symmetric

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

### 2 Which term collapses: α, not β

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

### 3 Hypothesis (b) is backwards — CONFIRMED

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

### 4 Hypothesis (a): the recession defect is real, and it is not the cause — CONFIRMED

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

### 5 Hypothesis (c): the inflation is real and period-invariant — CONFIRMED

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

### 6 What the calibration actually did: compensating errors

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

### 7 The binding constraint: r ≈ 0.57, and nothing moves it

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
