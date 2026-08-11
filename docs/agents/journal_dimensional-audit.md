# Journal — dimensional-audit

## Goal
Independent first-principles audit of the MUSLE dimensional/scale chain in
`src/mgb_sediment.py`. Re-derive the correct evaluation myself, then say whether the
three upstream decisions (units, LS aggregation, LS resolution) agree with me.
Deliverables: (1) hand-computed t/day for one real minibacia-day, (2) comparison with
each VOLUME_FACTORS convention, (3) independent per-pixel-vs-per-URH scale derivation,
(4) the running factor-chain table from 0.684 Mt/yr, (5) the residual and implied SDR.

## Discipline
Every decision is resolved from source evidence or derivation and WRITTEN HERE BEFORE
the basin-total consequence is computed or looked up. "It makes the number match" is
never evidence.

## Checklist
- [ ] 1. Read `src/mgb_sediment.py`, docs/33, 35, 36, and the three decision journals.
- [ ] 2. Independent dimensional derivation of Williams (1975) MUSLE coefficient.
- [ ] 3. Pick a real minibacia + high-runoff day; read Qsur, K, C, P, LS2D, area.
- [ ] 4. Hand-compute t/day carrying units.
- [ ] 5. Run the engine on the same unit-day under each VOLUME_FACTOR; compare.
- [ ] 6. Derive per-pixel vs per-URH ratio as f(n, beta); check numerically.
- [ ] 7. Factor-chain table from 0.684 Mt/yr.
- [ ] 8. Residual + implied SDR against 144-184 Mt/yr.

## Log
(appended below, in order, with numbers)

### Step 0 — journal created
Nothing computed yet. No basin totals looked at beyond what the task statement already
gave me (0.684 / 9.022 / 32.758 Mt/yr for the three conventions).

### Step 1 — sources read
- `src/mgb_sediment.py` (full), `scripts/c3/qpeak.py` (constants + proxy).
- Engine: `Sed_cell = alpha*(Qsur*q_peak*a_p*volume_factor)^beta * K*C*P*LS2D*FG *
  (A_cell/a_p)`, `q_peak = Qsur*a_p/86.4`, `a_p = 0.0081 km2`,
  `VOLUME_FACTORS = {pixel_km2: 1, swat_mm_ha: 100, williams_m3: 1000}`.

### Step 2 — DECISION ON UNITS, written BEFORE any basin total is recomputed
**My independent derivation (pure unit algebra, no data touched):**

Williams (1975) US-customary form: `Y[short ton] = 95*(Q[acre-ft]*q_p[cfs])^0.56*K*C*P*LS`.
Exact conversions: 1 acre-ft = 1233.4818375 m3; 1 cfs = 0.028316846592 m3/s;
1 short ton = 0.90718474 t.

    Y[t] = 0.90718474 * 95 * ( Q[m3]*q_p[m3/s] / (1233.4818375*0.028316846592) )^0.56 *KCPLS
    1233.4818375*0.028316846592 = 34.928312  ->  1/34.928312 = 0.028630066
    0.028630066^0.56 = exp(0.56*ln 0.028630066) = exp(0.56*(-3.553378)) = exp(-1.989892)
                      = 0.1367310
    coefficient = 0.90718474*95*0.1367310 = 86.18255*0.1367310 = 11.7834

11.7834 vs the quoted 11.8: 0.14 % apart. The metric Williams coefficient 11.8 is therefore
**only** the coefficient when the first factor is `runoff VOLUME in m3 times q_peak in
m3/s`, with the yield in metric tonnes.

Same algebra for the two rival readings:
- volume read as mm*ha: 1 mm over 1 ha = 10 m3, so alpha would be 11.7834*10^0.56 = 42.78.
- volume read as mm*km2: 1 mm over 1 km2 = 1000 m3, so alpha would be 11.7834*1000^0.56
  = 563.9.
Neither is 11.8. **DECISION: `williams_m3` is the correct convention.** `pixel_km2` is
wrong by 1000^0.56 = 47.8630x; `swat_mm_ha` (which carries area in ha, i.e. 100x the km2
product = 1/10 of the m3 product) is wrong by 10^0.56 = 3.63078x.
This AGREES with the units decision agent, by an independently reproduced derivation.
Corroboration to verify next: SWAT's `ysed.f` multiplies `surfq[mm]*peakr*1000.*hru_km`,
i.e. it converts to m3 in the source code regardless of the manual's "mm H2O/ha" label.

**A NEW question my derivation raises, which the three decisions do not cover:** the same
conversion that fixes the volume also fixes **K**. Williams' 95 (and hence 11.8) is
paired with K in US-customary USLE numerics, t.ac.h/(100 ac.ft.tonf.in). The engine
docstring labels its K `t.ha.h/(ha.MJ.mm)`, which is the **SI** K, numerically
0.1317x the US one. If `minibacia_soil_params.csv:K` really is SI, the load is low by a
further 1/0.1317 = 7.59x. I will resolve this from how K was derived (nb09 §4), from
evidence, BEFORE looking at what it does to the basin total.

### Step 3 — K UNIT RESOLVED FROM SOURCE, decision written before any total is computed
`notebooks/09_soil_parameters.ipynb` sec.4, verbatim: *"K by texture family — mid-range
Wischmeier & Smith (1978) class values **converted to SI (x0.1317)**"*, table Coarse 0.020 /
Medium 0.045 / Fine 0.028, units stated as `t.ha.h.ha^-1.MJ^-1.mm^-1` (the SI USLE K unit).
Measured: `minibacia_soil_params.csv:K` n=8672, min 0.019, median 0.03055, max 0.0495,
mean 0.031824 — that table times the drainage factor (0.95/1.00/1.10). So **K IS SI.**

Independent check of the 0.1317: A_SI[t/ha] = A_US[ton/ac]*0.90718474/0.404686 = 2.2417x;
R_SI[MJ.mm/(ha.h)] = 17.02*R_US. K = A/(R*LSCP), so K_SI = K_US*2.2417/17.02
= K_US*0.13171 (Foster et al. 1981). Inverse = 7.5926.

**DECISION (FOURTH ERROR, not among the three I was asked to check): the K scale is wrong
for alpha = 11.8.** The 11.8 derivation above converted ONLY V, q_p and Y; K, C, P and LS
keep their US-customary USLE numerics. Feeding an SI K into a formula whose coefficient was
derived for a US-numeric K understates the load by 1/0.13171 = **7.5926x**.
Corroboration: SWAT, the reference implementation of this exact equation, documents
`USLE_K` in units of `0.013 t.m2.hr/(m3.t.cm)`, i.e. the US-customary NUMBER, typical values
0.1-0.65; this project's 0.019-0.0495 is an order of magnitude below that range and is
exactly 0.1317x nb09's own pre-conversion Wischmeier numbers (0.152/0.342/0.213 US).
The justification is a dimensional identity plus the notebook's own stated conversion, and
it was written here before I computed any basin total.

### Step 4 — A CONCEPTUAL FINDING that changes the yardstick, recorded before computing
MUSLE is **not** USLE. Williams (1975) regressed against sediment yield MEASURED AT THE
OUTLET of his calibration watersheds; the runoff-energy factor `(V*q_p)^0.56` replaces
USLE's rainfall factor precisely because runoff already carries the delivery information.
So MUSLE output is *sediment delivered from the application unit to its channel*, not gross
detachment. Consequence: the brief's "gross erosion must be 1/SDR x outlet load, so
500-3,000 Mt/yr" yardstick is not the right one. What remains to explain between this
module's output and the outlet anchor is the CHANNEL/floodplain delivery (the Momposina
sink, stage C4), not a hillslope SDR of 0.05-0.3. I will still report the implied ratio
exactly as asked, and label which quantity it actually is.

### Step 5 — the unit-day, chosen by a rule fixed before any sediment number was seen
Rule: unit = the minibacia at the basin MEDIAN of decadal total Qsur; day = that
minibacia's own maximum-Qsur day. Executed output:
- minibacia **id 16115** (index 7718), decadal Qsur total 5084.43 mm
- day **2009-04-11** (index 100), **Qsur = 26.677167892456055 mm/d**
- own area 24.49 km2 (urh_fractions x minibacias; driver own_area_km2 identical)
- ONE URH cell: urh 11 = Forest, area 24.49 km2, **K = 0.019** (SI), **C = 0.003**,
  **P = 1.0**, **LS2D(ls2d_hs) = 118.245**, FG = 1.0
- pixels n = 24.49/0.0081 = 3023.4568

### Step 6 — DECISIONS on the other three questions, written before their basin effect
- **LS aggregation.** Verified independently in `scripts/c3/ls2d.py` line 606:
  `"ls2d_hs": L4[:, 1:][mi_idx, ui_slot] / urh_area`, i.e. sum(area_i*LS_i)/sum(area_i) —
  the area-weighted arithmetic mean, already. And it is the *only* admissible aggregate:
  with MUSLE applied per pixel and every other per-pixel factor identical inside a cell,
  Sed = f*sum_i LS_i = f*n*mean(LS); a median is a different functional. **Factor 1.000.**
  I agree with the LS-aggregation agent.
- **LS resolution.** Desmet & Govers unit contributing area is a_unit = (A_in + D^2)/D, so
  D is the equation's own plot size; the engine's application unit is a_p = 0.0081 km2 and
  sqrt(a_p) = 90 m = the COP90 D. The two are already consistent. **Factor 1.000.**
  I agree with the LS-resolution agent.
- **Application scale (per pixel vs per URH).** Derivation below gives ratio n^(2b-1). The
  choice is not free: Buarque (2015) — the source method this project ports — applies MUSLE
  per DEM pixel, and docs/35 sec.4 registered a_p before any number was produced. Per pixel
  is also the SMALLER of the two, so keeping it cannot be motivated by the gap.
  **Factor 1.000** in the chain; the lumped alternative is reported as a sensitivity only.

### Step 7 — EXECUTED: hand computation vs engine (task 1 & 2)
Williams coefficient reproduced by the code as well:
`95*(1/(1233.4818375*0.028316846592))^0.56*0.90718474 = 11.782565403570468`
(0.148 % from 11.8); mm*ha reading 42.7799, mm*km2 reading 563.9490.

HAND, minibacia 16115, 2009-04-11, per pixel then x n:
```
n pixels  = 24.49/0.0081                = 3023.456790123457
q_peak    = 26.677167892456055*0.0081/86.4 = 0.0025009844899177547 m3/s
V         = 1000*26.677167892456055*0.0081 = 216.08505992889403 m3
X = V*q_p                               = 0.5404253833851125
X^0.56                                  = 0.7084872091666863
K_US = 0.019/0.131710                   = 0.14425659098005977
Sed/pixel = 11.8*0.7084872*0.14425659*0.003*1.0*118.245*1.0 = 0.4278127529036679 t/d
Sed(minibacia 16115, 2009-04-11)        = 1293.4733726680033 t/d   <-- DEFENDED
```
ENGINE (`musle_load_tonnes`, stored SI K, same day), and the miss factor vs my hand number:

| convention | volume_factor | engine t/d | hand/engine |
|---|---|---|---|
| `pixel_km2` (registered) | 1 | 3.559389 | **363.398x low** |
| `swat_mm_ha` | 100 | 46.921883 | **27.567x low** |
| `williams_m3` | 1000 | 170.363059 | **7.5925x low** |

`williams_m3` reproduces my hand number **bitwise** when I substitute the stored SI K
(170.36305872560888 both ways, ratio exactly 1.0). So the engine's volume algebra is right
in `williams_m3` and the ONLY remaining discrepancy is the K unit — which is the cleanest
possible separation of the two errors.

### Step 8 — EXECUTED: the scale question (task 3), CLAIM VERIFIED
Derivation: with q_peak = c*Qsur*a and V = 1000*Qsur*a, the argument X(a) = V*q_p is
proportional to a^2, so Sed(a) ~ a^(2b). Splitting A into n pixels of a = A/n:
`Sed_lumped / Sed_persum = A^(2b) / (n*(A/n)^(2b)) = n^(2b-1)`.
Measured on minibacia 16115: lumped 3383.9033062538188 t/d, per-pixel-summed
1293.4733726680033 t/d, ratio **2.6161368125220523**; predicted
n^(2*0.56-1) = n^0.12 = **2.6161368125220523**; difference **exactly 0.0**.
The claim that the two differ is CONFIRMED, and the ratio is n^(2b-1) exactly.
Basin-wide, erosion-weighted: lumping per URH cell x2.372, per minibacia x2.700.
NOT applied — per-pixel is the source method (Buarque 2015) and the registered choice.

### Step 9 — EXECUTED: the factor chain (task 4)
Base reproduced from the frozen drivers: 3652 days = 9.9986 yr, ledger exact=True,
**0.6844 Mt/yr** (matches the reported 0.684). Units factor confirmed by running the
engine, not just asserted: `williams_m3 / pixel_km2 = 47.86300923226385` = 1000^0.56 to
the last bit.

| # | correction | factor | running total Mt/yr |
|---|---|---|---|
| 0 | as reported (`pixel_km2`, SI K, per pixel, area-wtd LS, 90 m) | 1.0000 | 0.684 |
| 1 | UNITS -> runoff volume in m3 (`williams_m3`) | 47.8630 | 32.758 |
| 2 | APPLICATION SCALE -> per DEM pixel (already correct) | 1.0000 | 32.758 |
| 3 | LS AGGREGATION -> area-weighted mean (already correct) | 1.0000 | 32.758 |
| 4 | LS RESOLUTION -> native 90 m (already correct) | 1.0000 | 32.758 |
| 5 | **K UNIT -> US-customary numerics (K/0.131710)** | 7.5925 | **248.711** |

### Step 10 — RESIDUAL (task 5)
248.71 Mt/yr against the 144-184 Mt/yr outlet anchor:
implied ratio outlet/model = **0.579** (at 144) to **0.740** (at 184).
- Read as the brief intends (model = gross erosion): SDR 0.58-0.74 is ABOVE the 0.05-0.3
  band but BELOW 1 — no longer impossible, and in the physically required direction for the
  first time. Under-corrected relative to that band.
- Read as I argue in Step 4 (MUSLE = sediment delivered from the application unit): 0.58-0.74
  is a CHANNEL/floodplain delivery ratio, and that is a normal value for a large basin with
  a floodplain sink. On this reading the order-of-magnitude gap is CLOSED.
Not tuned: nothing below step 5 was applied, and the two remaining pre-registered biases
(docs/35 sec.5: q_peak proxy + peak deficit, combined ~2.1x, bracket 1.4-4.8) would push the
model UP to ~522 Mt/yr and the ratio DOWN to ~0.28-0.35 — reported, deliberately not applied.

Context measured this run: basin area 257,096.93 km2, mean Qsur 658.54 mm/yr,
area-wtd C 0.0108232, area-wtd K(SI) 0.0317648, area-wtd LS2D(ls2d_hs) 39.859.

CHECKLIST: all 8 items done.

