# 35 — The MUSLE `q_peak` proxy: pre-registration, bias statement, and the C4 anti-compensation rule

**Stage:** C3.3 of `docs/31_phase_c_workplan.md`.
**Status:** REGISTERED 2026-08-11, **before** any sediment parameter has been fitted and
before `scripts/c3/qpeak.py` was written. Nothing in §4, §5 or §6 may be revised after the
first α/β fit; a later change is an amendment and must be logged as one, with its date and
reason, in §9.
**Why this document exists.** MUSLE needs an instantaneous peak runoff rate. Our engine is
daily. That gap has to be priced *before* calibration, because a free multiplicative
parameter (α) sitting downstream of a known systematic error will silently absorb it — the
mistake this project already made twice, with the celerity surrogate and with `kc_mult`
railing at its bound. This document fixes the proxy, states the resulting bias with numbers,
and pre-registers the test that stops C4 from hiding it.

---

## 1. What MUSLE needs, and what the engine has

```
Sed = α · (Qsur · q_peak · A)^β · K · C · P · LS2D          (Williams 1975)
```

| symbol | meaning | availability |
|---|---|---|
| `Qsur` | surface runoff depth, mm/day | **have** — `h2e_drivers.npz:qsur_rel_mm` (3652 × 8672, 2009-01-01…2018-12-31, warm-up excluded), frozen |
| `q_peak` | **peak** runoff rate, m³/s | **do not have** — the engine has no sub-daily state. This document. |
| `A` | area of the unit MUSLE is applied to | **have** — `topology.npz:own_area_km2`; URH areas from `parameters.npz:urh_fraction` |
| `K` | erodibility | **have** — `minibacia_soil_params.csv:K` / `parameters.npz:K_musle` |
| `C`, `P` | cover / practice | in progress (C3.2) |
| `LS2D` | topographic factor | in progress (C3.1) |
| `α`, `β` | 11.8, 0.56 (Williams 1975) starting values | to be fitted in C4 — **the thing this document constrains** |

Frozen-driver magnitudes actually on disk (measured 2026-08-11, read-only, from
`data/processed/sim_calibrated_v2/h2e_drivers.npz`):

| `Qsur` (`qsur_rel_mm`) | value |
|---|---|
| per minibacia-day: mean / median / p90 / p99 / p99.9 / max | 1.803 / 0.755 / 5.104 / 11.354 / 18.619 / 74.392 mm |
| per minibacia, annual: p05 / median / p95 | 74 / 509 / 1724 mm/yr |
| **fleet total surface-runoff volume** | **167.4 km³/yr** (= 651 mm/yr over 257,097 km²) |

---

## 2. Input audit — done first, because option (ii) depends on it

`topology.npz` was opened and every key listed (not assumed):

```
minibacia_id, own_area_km2, downstream_id, downstream_idx, topo_order_idx,
upstream_area_km2, n_upstream_links, hops_to_outlet, path_km_to_outlet,
reach_km, centroid_lon, centroid_lat, outlet_idx
```

- **`reach_km` exists.** n = 8672; exactly **1 zero** (the basin outlet); min > 0 = 0.706 km;
  p05 3.019; median 5.074; p95 8.601; max 19.889 km.
- **Slope does not exist.** There is no slope, gradient or elevation-drop key. This confirms
  the note already carried in docs/31 §C3.3 ("verified 2026-08-10") and it is re-verified here.
- **The processed DEM does not cover the basin.** `cop30_dem.tif` (6120 × 11160, 30 m) and
  `dem_coarse.tif` (680 × 1240) both have bounds (−75.400, 8.200) → (−73.700, 11.300): the
  lower-Magdalena window only. `minibacias.tif` spans (−77.000, 1.400) → (−72.300, 11.400).
  Only **1,506 of 8,672 minibacias (17.4 %)** fall inside the processed 30 m DEM — and they are
  the *flat* ones (proxy channel slope median 0.0056 m/m within that window). The id spaces
  match exactly (both n = 8672, ids 1174…19256, intersection 8672), so this is a DEM-extent
  fact, not an id bug.
- **A whole-basin DEM is buildable but unbuilt.** `data/raw/dem/rasters_COP90_Correcte_Corrdinatzs.tar.gz`
  contains one member, `output_hh.tif` (260,274,553 B, Copernicus GLO-90), not extracted.
  `Explanation_script_MGB_SA_Magdalena.pdf` records why 30 m is only a window: *"30 m over
  the whole basin exceeds the tool's cell limit"*, and that *"slope feeds the MUSLE LS factor"* —
  i.e. slope's intended role in this project is LS2D (C3.1), never `q_peak`.

**Consequence for option (ii):** a basin-wide `t_c` is not computable from any shipped
artifact today, and the only slope sample that *is* available is systematically flat — it
excludes the Andean flanks, which are exactly the erosive part. A `t_c` field built from that
sample would be wrong in the worst possible direction.

---

## 3. The candidate proxies

### (i) Daily-mean surface-runoff rate — the floor estimate

```
q_peak = Qsur[mm/d] · A[km²] / 86.4                                (m³/s)
```

Derivation (unit audit, no fudge factor): a depth `Qsur` mm over `A` km² is
`Qsur/1000 · A·10⁶ = 1000·Qsur·A` m³ per day; divided by 86,400 s this is `Qsur·A/86.4` m³/s.

**Assumes:** the day's surface-runoff volume leaves the unit at a *constant* rate for 24 h —
i.e. there is no storm within the day. Since the true instantaneous peak of any non-constant
hydrograph exceeds its mean, this is a **provable floor**: `q_peak,true ≥ q_peak,proxy`
always, with equality only for a perfectly flat day.
**Needs:** `Qsur`, `A`. Both frozen and verified. No slope, no `t_c`, no unit-hydrograph
shape, no storm duration.

### (ii) SCS triangular unit hydrograph

```
q_peak = 2V / T_b,   V = 1000·Qsur·A m³,   T_b = 2.67·T_p,   T_p = D/2 + 0.6·t_c
     ⇒ q_peak = Qsur·A / (4.806 · T_p[h])   ≈ 0.208·A·Qsur/T_p        (m³/s)
t_c (Kirpich) = 0.0195 · L[m]^0.77 · S^−0.385   minutes
```

**Assumes:** (a) a triangular UH with the US-derived shape constant `T_b = 2.67·T_p`
(peak-rate factor 484 in imperial units), known to overestimate peaks in flat, humid basins;
(b) a rainfall-excess duration `D` — **an unconstrained free parameter, because the model has
no sub-daily rainfall at all**; (c) a `t_c` from channel length and slope, extrapolating
Kirpich (fitted on 0.4–45 ha Tennessee farm plots) to 1.6–313 km² units; (d) that a
basin-wide slope field exists.
**Needs:** `reach_km` (have) **and slope (do not have — §2)**.

Its only effect relative to (i) is a multiplier, exactly:

```
amplification = q_peak,(ii) / q_peak,(i) = 86.4 / (4.806 · T_p[h]) = 17.978 / T_p[h]
```

| `T_p` | 3 h | 4 h | 6 h | 9 h | 12 h | 18 h |
|---|---|---|---|---|---|---|
| amplification | 5.99 | 4.49 | 2.99 | 2.00 | 1.50 | 1.00 |

So (ii) is (i) times a number between roughly 1.5 and 6 whose *spatial* variation comes only
through `t_c`, i.e. only through the slope field we do not have.

### (iii) The source paper's own formulation — RECOVERABLE, and it equals (i)

Fagundes et al. (2026) itself is **not in this repo** (no PDF; the only PDF,
`Explanation_script_MGB_SA_Magdalena.pdf`, mentions MUSLE twice and gives no `q_peak`).
The formulation was recovered from the MGB-SED source that Fagundes' sediment module
inherits — **Buarque (2015), UFRGS doctoral thesis (advisor Collischonn), on sediment
generation and transport in large basins (Madeira)**:

> **eq. 7:**  `qpico_{i,j}^k = Dsup_{i,j}^k · A_{i,j}^k / 86.4`
> preceded by: *"the peak rate of surface runoff in each pixel k is obtained considering a
> runoff volume uniform through the day."*

with **eq. 5** `SED = 11.8·(Qsup·qpico·A)^0.56 · K·C·P·LS·FG` applied **per DEM pixel** inside
each URH of each minibacia (eq. 6), and a linear reservoir delaying delivery to the channel.
`FG` is a coarse-fragment factor. No unit hydrograph, no rainfall disaggregation, no
regionalised peak relation anywhere in the lineage.

**Therefore (iii) ≡ (i).** The floor estimate is not an expedient; it is the published method.

---

## 4. THE CHOICE (registered)

> **REGISTERED: `q_peak = Qsur[mm/d] · a[km²] / 86.4`, the daily-mean surface-runoff rate
> (Buarque 2015 eq. 7 ≡ candidate (i) ≡ candidate (iii)), evaluated at the COP90 pixel
> scale `a_p = 0.0081 km²` and summed analytically to the URH:**
>
> ```
> Sed_URH = (A_URH / a_p) · α · (Qsur · Qsur·a_p/86.4 · a_p)^β · K · C · P · LS2D
> ```
>
> **Option (ii) is REJECTED for production. It is implemented only as a sensitivity
> generator, to bound the bias in §5.1.**

Justification, in order of weight:

1. **It is the source formulation, so the transposition claim is exact.** H3 (docs/00) is
   *method transfer* from Fagundes et al. Using their own `q_peak` makes our loads comparable
   to the published South-American MGB-SED numbers **bias for bias** — the same daily-mean
   assumption, the same α reference. Any other proxy silently breaks that comparability while
   the paper is still cited as the method source. This alone outranks physical elegance.
2. **Option (ii) is not computable today and its inputs are biased flat.** §2: no slope field
   exists; the only DEM on disk covers 17.4 % of minibacias and is the lowland 17.4 %.
   Building `t_c` from it would manufacture spatial structure from the least representative
   sample available.
3. **Option (ii) would add a free parameter the model cannot constrain.** `D`, the
   rainfall-excess duration, is unknowable in a model with no sub-daily rainfall. Setting
   `D = 24 h` collapses (ii) back onto (i) (`T_p ≈ 14–18 h` ⇒ amplification ≈ 1.0–1.3);
   setting `D = 6 h` triples the peak. There is no measurement in this project that can
   choose between those, so (ii) would be a *tuned* choice dressed as a physical one.
4. **Its bias has one provable direction.** `q_peak,true ≥ q_peak,mean` identically, so with
   `β > 0` the simulated load is a strict lower bound *given `Qsur`*. A proxy with a
   one-sided, provable error is worth more here than one with a smaller but sign-ambiguous
   error, because the whole point of §5 is to state a direction the reader can trust.
5. **Evaluating at the pixel scale removes the α scale-ambiguity.** MUSLE is scale-dependent:
   under uniform `Qsur`, lumping `N` pixels into one unit multiplies the load by `N^(2β−1)`
   (= `N^0.12`). Measured on our own geometry: **2.149** at the median URH (4.762 km²),
   **2.630** at the median minibacia (25.58 km²), 3.552 at the largest (313 km²). Keeping
   Buarque's pixel scale means our fitted α is directly comparable to 11.8 with **no**
   correction factor — which is what makes the §6 threshold enforceable rather than notional.
   (URH geometry as measured: 32,782 non-empty URH cells, 15.8 % of 8672 × 24; 3.78 URH per
   minibacia; URH area p05 0.544, median 4.762, p95 24.485, max 169.98 km².)

**What the chosen proxy produces, at both scales** (frozen `Qsur`, 2009–2018):

| scale | statistic | value |
|---|---|---|
| per minibacia-day | median `q_peak` | 0.243 m³/s |
| per minibacia-day | p99 / max | 4.285 / 108.03 m³/s |
| per minibacia | annual-max `q_peak`, fleet median (p05–p95) | **2.178** (0.317 – 6.947) m³/s |
| fleet | total surface-runoff volume driving it | 167.4 km³/yr |

---

## 5. THE BIAS STATEMENT (registered, quantified)

Two independent errors sit under the sediment estimate. **They point the same way — both
suppress simulated load — so they compound; there is no cancellation to hope for.**

### 5.1 The proxy's own bias (this document's choice)

The daily mean understates the true instantaneous peak by the amplification factor of §3(ii):
**1.5×–6.0× for `T_p` = 12 h down to 3 h**, central estimate ≈ 3× at `T_p` = 6 h. Through
MUSLE this is `amplification^β`:

| `T_p` assumed | amplification | sediment factor `amp^0.56` |
|---|---|---|
| 12 h | 1.50 | 1.26 |
| 6 h (central) | 2.99 | **1.86** |
| 3 h | 5.99 | 2.75 |

> **Statement:** relative to a model that resolved sub-daily peaks, this proxy suppresses
> flood-driven sediment by a factor of **1.26 – 2.75 (central ≈ 1.9)**, i.e. **−21 % to −64 %
> (central ≈ −46 %)**.

**But this term must NOT be corrected for, and must not be absorbed by α.** Buarque and
Fagundes fit/adopt α = 11.8 *with this same daily-mean proxy*, so the term is already inside
the reference α. Correcting it here while still comparing to their α, or letting α swallow it,
double-counts. It is stated so that the *absolute* loads are read as method-consistent with
the published MGB-SED family, not as physically unbiased.

### 5.2 The peak deficit this proxy sits on top of (measured, docs/33 §7.3–§7.5)

These are measurements, not assumptions. From C2b, on the adopted H2E hydrology:

| measured | value | 25–75 % across gauges | sediment factor `R^0.56` | sediment deficit |
|---|---|---|---|---|
| `R_AMS` fleet median | **0.820** | 0.529 – 1.186 | 0.8948 | **−10.5 %** |
| `R_AMS` geometric mean | 0.810 | — | 0.8887 | −11.1 % |
| `R_Q1` (1 % exceedance) | 0.847 | 0.633 – 1.234 | 0.9112 | −8.9 % |
| `R_Q5` (5 % exceedance) | 0.975 | 0.740 – 1.279 | 0.9859 | −1.4 % |
| `R_POT` (independent events > obs Q5) | **0.567** | 0.155 – 1.141 | see below | see below |

`R_POT` is a **count**, not a magnitude: the model produces **1,285 independent
peaks-over-threshold against 2,236 observed (57.5 % of them)**, i.e. **~43 % of flood events
are missing entirely**. `β` acts on magnitude and therefore **cannot** convert a count deficit
into a load deficit — writing `0.567^0.56 = 0.728` would be wrong and is recorded here as
wrong so that no one does it later. The correct bracket:

- **Lower bound on the event-count channel:** if the 951 missing events were the smallest ones
  (threshold-adjacent), their omitted load is small and the count channel adds only a few
  percent.
- **Upper bound:** if the missing events were of average above-threshold size, the
  flood-driven load deficit from this channel alone approaches **−42.5 %**.
- Nothing measured in this project resolves where in that bracket the truth sits. It stays a
  bracket.

**Shape of the error (docs/33 §7.3):** the deficit switches on between the 95th and 99th flow
percentile — `R_Q5` = 0.975 (essentially unbiased) while `R_Q1` = 0.847 and `R_AMS` = 0.820.
It is a tail effect, not a level shift. This matters for §6: a *constant* α cannot repair a
tail-only deficit without over-predicting sediment on the 95 % of days that are already right.

**Correction to docs/31 §C3.3 and docs/22.** docs/31 §C3.3 states the peak bias is "worst at
the largest" gauges. C2b measured **ρ(`R_AMS`, area) = +0.088, p = 0.49 — indistinguishable
from zero** (docs/33 §7.5). The peak deficit does **not** scale with catchment area (unlike the
correlation deficit, which does). Any C3/C4 reasoning that leans on an area-dependent peak
bias is leaning on a refuted claim.

### 5.3 The combined statement

Compounding §5.1 and §5.2 (magnitude channel only, fleet median, `β` = 0.56):

```
0.895 (measured peak magnitude)  ×  1/1.86 (proxy, central)   ⇒  0.481
```

> **REGISTERED BIAS STATEMENT.** Simulated flood-driven suspended-sediment transport from this
> model is a **LOWER BOUND**.
> - From the **measured** peak-magnitude deficit alone (`R_AMS` = 0.820, β = 0.56), it is low
>   by **at least 10.5 %** fleet-wide, and by **at least 19.0 %** in the El Niño 2015–16 phase
>   (`R_AMS` = 0.686).
> - Adding the **missing 43 % of flood events**, the flood-driven load deficit is plausibly
>   **−10 % to −45 %**; the project cannot narrow that bracket with what it has measured.
> - Adding the **`q_peak` proxy's own** sub-daily assumption (central 1.86×), the total
>   suppression relative to a sub-daily-resolved model is a factor of ≈ **2.1 (bracket
>   1.4 – 4.8)** — but this last term is *method-consistent with Buarque/Fagundes* and must be
>   reported separately, never merged into the previous two and never absorbed by α (§5.1, §6).
> - No channel pushes the other way. There is no term in this accounting that would make the
>   simulated load an over-estimate.

### 5.4 Direction of the error on the study's headline result (ENSO contrast)

The peak deficit is **phase-asymmetric** (docs/33 §7.4), and this bends the central claim:

| period | `R_AMS` | `R^0.56` | sediment deficit | `R_POT` |
|---|---|---|---|---|
| VAL La Niña 2011 | 0.808 | 0.8875 | −11.3 % | 0.500 |
| **VAL El Niño 2015–16** | **0.686** | 0.8097 | **−19.0 %** | 0.464 |
| VAL 2018 (worst) | 0.589 | 0.7435 | −25.7 % | 0.375 |
| CAL 2012–14 | 0.648 | 0.7843 | −21.6 % | 0.423 |

```
contrast inflation = 0.8875 / 0.8097 = 1.096
```

> **The dry phase is suppressed harder than the wet phase.** The *simulated* La Niña : El Niño
> sediment-flux ratio is therefore **overstated by ≈ +10 %** relative to truth, from the peak
> magnitude channel alone (the count channel, `R_POT` 0.500 vs 0.464, points the same way,
> ≈ +8 % in event counts). This is the opposite of a conservative error for H1/H2: it flatters
> the headline contrast. It must be quoted whenever a *simulated* contrast ratio is quoted, and
> compared against the **observed** contrast (docs/34: 2.8×–4.6× primary, 6.4×–9.3×
> sensitivity, 22/22 stations same sign), which carries no such bias because it is measured.

### 5.5 What is NOT claimed

- Not claimed: that the deficit bracket can be narrowed. It cannot, without sub-daily data.
- Not claimed: that the bias is uniform in space. It is not measurably area-dependent
  (§5.2), but per-gauge `R_AMS` spans 0.529–1.186 at the quartiles and a substantial minority
  of gauges *over*-predicts peaks; the worst is gauge 21257090 (486 km², `R_AMS` 0.247, 20
  observed POT events, **0** simulated).
- Not claimed: any sediment **yield** in t/km²/yr. Embargoed — catchment areas disagree by
  more than 2× on 36 % of shared gauges (docs/23 §13.2). Absolute flux only.
- Not claimed: that `LS2D`, `C`, `P` are settled. They are C3.1/C3.2 and carry their own
  errors, independent of this one.

---

## 6. THE C4 ANTI-COMPENSATION RULE (registered, hard)

> **RULE 0 — the prohibition.** α and β may **not** be used to compensate the biases of §5.
> `q_peak` is fixed by §4 and is not a calibration knob, directly or by proxy. The §5 bias is
> to be *reported* with the result, not fitted away.

The bias is a *multiplicative, tail-concentrated* suppression. α is a multiplicative constant
and β a tail exponent — so both are exactly the shape a fitter would reach for. The available
compensation product is bounded and known in advance: `2.75` (proxy, worst case) × `1.12`
(peak magnitude) × `1.74` (missing events) ≈ **5.4×**. Thresholds are therefore set at a
fraction of that, so the alarm fires long before full compensation is reached.

### 6.1 Registered α band — the primary fingerprint

Reference: **α = 11.8** (Williams 1975; adopted unchanged by Buarque 2015 eq. 5 *with the
same daily-mean `q_peak`*, so it is the like-for-like reference under §4).

| band | α (at the §4 pixel scale) | C4 action |
|---|---|---|
| expected | **5.9 – 23.6** (0.5× – 2× Williams) | adopt; report α with this band beside it |
| watch | 23.6 – 35.4 (2× – 3×) | adopt **only** with a written, non-peak physical justification in the C4 doc; state explicitly that compensation was considered and why it is rejected |
| **HARD STOP** | **α > 35.4** (3× Williams) | **STOP. Do not adopt. Report the fit, the bias of §5, and the fact that the threshold fired.** A fitted α at ≥ 3× Williams is the fingerprint of α absorbing the peak deficit, because ~5.4× is precisely the size of the compensation available. |
| **HARD STOP** | **α < 3.9** (⅓× Williams) | **STOP.** The proxy is a floor (§3(i)); a fit that needs α far *below* Williams means something upstream (`Qsur`, `K`, `C`, `LS2D`, or the delivery step) is over-producing, and that must be found, not offset. |

### 6.2 The scale trap — the threshold points the wrong way if this is skipped

α is scale-dependent (§4 point 5). The band in §6.1 is valid **only** if MUSLE is evaluated at
`a_p = 0.0081 km²` as §4 registers. If C4 instead applies MUSLE lumped, the comparable
reference and the whole band must be divided by `N^(2β−1)`, `N = A/a_p`:

| application unit | `N^(2β−1)` | comparable α reference | rescaled hard-stop |
|---|---|---|---|
| COP90 pixel, 0.0081 km² (**registered**) | 1.000 | **11.8** | 35.4 |
| median URH, 4.762 km² | 2.149 | 5.49 | 16.5 |
| median minibacia, 25.58 km² | 2.630 | 4.49 | 13.5 |
| largest minibacia, 313.45 km² | 3.552 | 3.32 | 10.0 |

> **C4 must state which unit it applied MUSLE to, in the same table as α.** An α of 12 looks
> textbook-perfect at pixel scale and is a **2.2× over-fit** at minibacia scale. Reporting α
> without its unit is how this error survives review.

### 6.3 Registered β rule — the second compensation channel

β weights large events against small ones. Raising β is the natural way to make the surviving
1,285 peaks stand in for 2,236.

| band | β | C4 action |
|---|---|---|
| expected | 0.50 – 0.62 (Williams 0.56 ± literature spread) | adopt |
| **HARD STOP** | **β > 0.65 or β < 0.45** | **STOP and report.** β above 0.65 is event-amplification standing in for missing events. |

### 6.4 Registered residual test — detects compensation even inside the bands

α can be inside its band and still be compensating, if the fit trades tail under-prediction
for body over-prediction. Because the discharge deficit is **tail-only** (`R_Q5` = 0.975,
`R_Q1` = 0.847, `R_AMS` = 0.820 — §5.2), compensation has a signature:

> **Test T1 (mandatory in C4).** Partition simulated-vs-observed sediment residuals by the
> station's *observed discharge* quantile. Report the median relative residual for
> (a) days below observed Q50, (b) Q50–Q95, (c) above Q95, per station and as a fleet median.
> **Trigger:** if the fleet-median relative residual below Q50 exceeds **+25 %** while the
> above-Q95 residual is negative, α has absorbed the peak deficit. **STOP and report.**

> **Test T2 (mandatory in C4).** Fit on one phase, score on the other. If the El Niño 2015–16
> residual is systematically more positive than the La Niña 2011 residual by more than the
> **+10 %** contrast bias already registered in §5.4, the fit is phase-compensating. Report.

> **Test T3 (reporting, not a trigger).** Every table that reports a fitted α or β must carry,
> in the same table, the registered reference (§6.1/§6.3), the application unit (§6.2), and a
> one-line pointer to the §5.3 bias statement. A fitted parameter published without its
> registered band is not an acceptable C4 output.

### 6.5 What C4 *is* permitted to do

- Report the result as a **lower bound**, quoting §5.3. This is the default and needs no
  special justification.
- Apply an **explicit, separately named, separately reported** peak-correction factor
  (e.g. `f_peak`) with its own stated derivation — *outside* α, visible in every table, and
  with the uncorrected number reported alongside. Folding the same factor into α is forbidden;
  naming it is not.
- Calibrate on tributary stations first (docs/30 §C3), which is unrelated to this rule.

---

## 7. Implementation

`scripts/c3/qpeak.py`, written **after** §4–§6 were fixed.

**Placement (justified).** `scripts/c3/`, not `src/`:
1. Phase B is closed twice and `src/mgb_hydrology.py` / `h2e_drivers.npz` are frozen; C3 code
   must not land inside the frozen engine's directory where it could be mistaken for part of it.
2. These are pure functions of scalars/arrays with no engine state, no I/O and no globals;
   `src/mgb_sediment.py` (C3.4) will `import` them rather than re-derive them.
3. It keeps the C3 static-input builders together (`scripts/c3/ls2d.py`, the C/P mapping).

**Exposed:**

| name | role |
|---|---|
| `qpeak_daily_mean(qsur_mm, area_km2)` | **the registered proxy** (§4), `Qsur·A/86.4` |
| `COP90_PIXEL_AREA_KM2 = 0.0081` | the registered application scale (§4) |
| `musle_scale_factor(area_km2, pixel_area_km2, beta)` | `N^(2β−1)` — the §6.2 scale trap, in code |
| `qpeak_scs_triangular(qsur_mm, area_km2, tp_hours)` | **rejected** option (ii), retained only as the §5.1 sensitivity generator |
| `time_of_concentration_kirpich(reach_km, slope)` | option (ii)'s `t_c`; unusable in production (no slope field, §2) — kept so the rejection is reproducible |
| `peak_amplification(tp_hours)` | `86.4/(4.806·T_p)`, the §3/§5.1 multiplier |
| `sediment_bias_ratio(discharge_ratio, beta)` | `R^β` — the §5.2 arithmetic |
| `ALPHA_*`, `BETA_*` constants | the §6 registered bands and hard stops, so C4 imports them instead of re-typing them |

**Tests** (`tests/test_qpeak.py`, run with the repo's existing pytest suite):
hand-computed single-cell case (`Qsur` = 10 mm, `A` = 25 km² ⇒ 2.8935185185… m³/s, exact to
1e-12); strict monotonicity in `Qsur`; `q_peak` = 0 at `Qsur` = 0; array/broadcast equivalence
with the scalar path; negative inputs rejected; NaN propagation not silently zeroed;
`peak_amplification` consistent with `qpeak_scs_triangular / qpeak_daily_mean`;
`musle_scale_factor` = 1 at the pixel scale and reproduces the §6.2 table;
`sediment_bias_ratio` reproduces the §5.2 column.

---

## 8. Open items this document creates

1. **`t_c` remains unbuildable basin-wide.** If a full-basin slope field is ever produced from
   `output_hh.tif` (COP90) for LS2D (C3.1), option (ii) becomes *computable* — it does not
   thereby become chosen. Re-opening §4 would be an amendment under §9, and would need a
   defensible `D` first.
2. **C3.5 (cross-check against implementation B's `musle.py`) stays BLOCKED.** That file is not
   in this repo and no path or URL is recorded (docs/20:43, docs/31 §C3.5). Recorded as still
   blocked; not attempted.
3. **`FG` (coarse-fragment factor)** appears in Buarque eq. 5 and is absent from our
   formulation. `FG ≤ 1`, so omitting it *raises* our load — the only term found so far that
   points against §5.3's lower-bound direction. It must be quantified or explicitly set to 1
   with a stated reason in C3.4, not left silent.
4. **Delivery.** Buarque delays minibacia sediment to the channel through a linear reservoir.
   Our C3.4 must state whether it does the same; without it, timing (not mass) differs.

---

## 9. Registration record

| | |
|---|---|
| Registered | 2026-08-11, before `scripts/c3/qpeak.py` existed and before any α/β fit |
| Choice | §4 — `q_peak = Qsur·a/86.4`, Buarque (2015) eq. 7, at `a_p` = 0.0081 km² |
| Bias statement | §5.3 (magnitude) + §5.4 (ENSO direction) |
| C4 rule | §6 — α band 5.9–23.6, hard stop α > 35.4 or α < 3.9; β hard stop outside 0.45–0.65; tests T1, T2, T3 mandatory |
| Sources of every measured number | docs/33 §7.3–§7.5 (peak ratios, executed output), docs/34 (observed contrast), `topology.npz` / `parameters.npz` / `h2e_drivers.npz` (read-only, 2026-08-11) |
| Amendments | **§9.1 (2026-08-11)** — MUSLE area-unit enumeration completed; registered choice UNCHANGED |

---

### 9.1 Amendment — 2026-08-11 — the MUSLE area unit is a THIRD convention, and it was missing

**What changed:** nothing registered. `q_peak` (§4), `a_p` = 0.0081 km², the α band and hard
stops (§6), and the model default (`volume_convention = 'pixel_km2'`) are all **unchanged**.
What changed is the *enumeration of unit conventions* the C3.6 gate-(b) verdict is read
against, and one factual assertion in `src/mgb_sediment.py` that is now deleted.

**Why.** `src/mgb_sediment.py` documented **two** conventions for the `(Qsur · q_peak · A)`
product — `pixel_km2` (×1) and `williams_m3` (×1000, load ×1000^0.56 = 47.863) — and
justified the default by asserting that Buarque (2015)'s MUSLE `A` "is the same km² area his
eq. 7 uses". **This project's own source review says the opposite.** Verbatim, from
`data/processed/peakgap/method_research.md` §1.1 (written 2026-08-11 04:13, i.e. 62 minutes
*before* `src/mgb_sediment.py`):

> "Unit check: 1 mm/day over 1 km² = 1000 m³/day = 0.011574 m³/s = 1/86.4, so `Dsup` is
> mm/day and `A` is km² in eq. 7/12 (**both texts label the MUSLE area `A` in ha for the
> erosion equation itself** — mind the mixed units when porting)."

So km² is established for the **`q_peak` equation only** (eq. 7 / eq. 12). For the **erosion
equation** the sources say **hectares** — which is also SWAT's standard MUSLE form,
`Q_surf[mm] · q_peak[m³/s] · area[ha]`, and the form α = 11.8 is normally quoted with. That
convention appeared **nowhere** in this document, in `src/mgb_sediment.py`, in docs/36, or in
the C3.4/C3.6 journals. It is worth exactly **100^0.56 = 13.1826×** on the load.

**Third convention now implemented** as `volume_convention='swat_mm_ha'`
(`src/mgb_sediment.py`, `VOLUME_FACTORS`), non-default, diagnostic only — the same status
`williams_m3` has.

**Gate (b) restated as three rows.** Measured on the frozen H2E drivers, 2009–2018,
uncalibrated α = 11.8 / β = 0.56, τ = 0, FG = 1.0, `qsur_rel_mm`, all three re-run
2026-08-11 (mass ledger residual exactly 0.0 in each; `pixel_km2` reproduces C3.6's
6,843,119.50146461 t bit for bit). Gross **hillslope** erosion, before any channel
deposition. Anchors: 144 Mt/yr (Restrepo & Kjerfve 2000) / 184 Mt/yr (Restrepo & Escobar
2018), docs/34 §5.1.

| convention | product factor | load factor | basin total | vs 144 | vs 184 | orders of magnitude | α needed for 144 | × past the α > 35.4 stop |
|---|---|---|---|---|---|---|---|---|
| `pixel_km2` (**registered default**) | ×1 | ×1 | **0.6844 Mt/yr** | 210.4× low | 268.8× low | 2.323 – 2.430 | 2,483 | 70.1× |
| `swat_mm_ha` (SWAT / hectare form) | ×100 | ×13.1826 | **9.0222 Mt/yr** | 15.96× low | 20.39× low | **1.203 – 1.310** | 188 | 5.3× |
| `williams_m3` (Williams' m³ volume) | ×1000 | ×47.8630 | **32.7577 Mt/yr** | 4.40× low | 5.62× low | 0.643 – 0.750 | 52 | 1.5× |

Per-unit, for the same reason the factor is a scalar on every minibacia-day: the
per-minibacia median moves 0.0675 → 0.8899 → 3.231 t/d across the three rows. (No t/km²/yr
yield is quoted — docs/23 §13.2 embargo.)

**What this does and does not change about the verdict.**

1. Gate (b) still **FAILS in the same direction** under every convention: all three are
   *below* the outlet anchors, which is the physically forbidden direction (delivery
   ratio < 1 ⇒ gross hillslope erosion must *exceed* the outlet load).
2. The §6.1 α hard stop still **binds under every convention** (70.1× / 5.3× / 1.5× past
   it), so the stop's verdict is convention-independent.
3. But the *size* of the gap C4 must explain is convention-dependent by **13.1826×**, and the
   previously documented pair made the registered reading look like the only km²-defensible
   one. **C4 must therefore CHOOSE a convention explicitly, citing this table**, and must not
   inherit the smallest by default. Adopting `swat_mm_ha` (or any other row) as the default
   remains an amendment under this §9, with its own date and reason — this amendment does
   **not** make it.
4. Corrected in `src/mgb_sediment.py` at the same time: the claim that Buarque's MUSLE `A` is
   in km² is **deleted** (the quote above replaces it), and "Two conventions exist in the
   literature" becomes three. A previously stated figure of "α ≈ 565 to absorb the 47.86×
   convention factor" is retained but relabelled — 565 = 11.8 × 47.863 is the `pixel_km2`-unit
   α that *reproduces the `williams_m3` level*, not the α that closes the gap to 144 Mt/yr
   (that is 52). Both numbers now appear with their distinct meanings.

**Disclosure, per the fix protocol:** no frozen artifact was modified. `h2e_drivers.npz` and
every `sim_*_v2/` output were read read-only; the erosion run above was executed in a
scratchpad script and wrote nothing to the repository. Nothing was backdated: this amendment
carries the date it was written (2026-08-11), *after* the C3.6 gate-(b) result it revises,
and it revises that result rather than replacing the record of it. C3.5 (cross-check against
implementation B's `musle.py`) remains **BLOCKED** — that file is not in this repo (§8 item 2,
unchanged).
