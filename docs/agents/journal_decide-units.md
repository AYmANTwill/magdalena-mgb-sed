# Journal — decide-units

GOAL: determine, from source literature and dimensional analysis ALONE, what units MUSLE's
terms MUST be in for alpha = 11.8, beta = 0.56 to be the correct coefficients.

DISCIPLINE (stated up front): the decision is to be resolved from source evidence /
derivation only. I will write the decision and its justification into this journal BEFORE
computing what any convention does to the basin total. "It makes the number match" is not
evidence. Steps 1-3 (sources, dimensional analysis, hand case) and step 5 (decision) are
recorded before step 4 (checking VOLUME_FACTORS in src/mgb_sediment.py).

## Checklist
- [ ] 1a. READ data/processed/peakgap/method_research.md FIRST (Buarque 2015 eq.7,
      Fagundes 2018 eq.12 review) — note the ha vs km2 apparent mixture.
- [ ] 1b. Williams (1975) original MUSLE: units + coefficients (95 / 0.56 US-customary
      vs 11.8 / 0.56 SI) — verify, do not assume.
- [ ] 1c. SWAT theoretical documentation (Neitsch et al.) MUSLE section — quote the
      explicit units for Qsurf (mm H2O/ha), qpeak (m3/s), area_hru (ha), sed (t).
- [ ] 2.  Full dimensional analysis with arithmetic shown; enumerate all admissible
      unit combos; discriminate with source quotes.
- [ ] 3.  HAND CASE with round numbers, every step shown.
- [ ] 5.  DECISION written here (before step 4).
- [ ] 4.  ONLY THEN: check src/mgb_sediment.py VOLUME_FACTORS against the hand case.

## Log

### Step 0 — journal created
Read-only constraints acknowledged: no git, no calibration, frozen artifacts untouched,
t/km2/yr gauge-referenced yields embargoed. Files I may touch: this journal only.

---

### Step 1a — data/processed/peakgap/method_research.md (READ FIRST, as instructed)

Verbatim, §1.1:

> "Unit check: 1 mm/day over 1 km² = 1000 m³/day = 0.011574 m³/s = 1/86.4, so `Dsup` is
> mm/day and `A` is km² in eq. 7/12 (both texts label the MUSLE area `A` in ha for the
> erosion equation itself — mind the mixed units when porting)."

So the prior review had already flagged the mixture but not resolved it. Resolution below
(step 1e).

### Step 1b — Buarque (2015) PRIMARY, fetched and text-extracted this step

Downloaded `lume.ufrgs.br/bitstream/handle/10183/129875/000977197.pdf` (9,646,521 B,
182 pp) to scratchpad; text extracted with PyMuPDF. §3.3.1, p. 43, VERBATIM:

> `𝑆𝐸𝐷 = 11,8 ∙ (𝑄𝑠𝑢𝑝 ∙ 𝑞𝑝𝑖𝑐𝑜 ∙ 𝐴)^0,56 ∙ 𝐾 ∙ 𝐶 ∙ 𝑃 ∙ 𝐿𝑆 ∙ 𝐹𝐺   ( 5 )
>
> onde SED [t] é a carga de sedimentos resultante da erosão do solo, Qsup [mm.ha-1] é o
> volume de escoamento superficial, qpico [m3.s-1] é a taxa de pico do escoamento
> superficial, A [ha] é a área superficial, K [0,013.t.m2.h.(m3.t.cm)-1] é o fator
> erodibilidade do solo, C [-] … P [-] … LS [-] … FG [-]"

and eq. 6 (per pixel): "`Ap [ha] é a área do pixel`"; eq. 7:
`qpico = Dsup · A / 86,4`.

### Step 1c — Fagundes (2018) PRIMARY, fetched and text-extracted this step

`lume.ufrgs.br/bitstream/handle/10183/175012/001065326.pdf` (9,292,830 B, 201 pp). §5.3,
VERBATIM:

> "`𝑆𝑒𝑑 = 𝛼.(𝑄𝑠𝑢𝑝 ∗ 𝑞𝑝𝑖𝑐𝑜 ∗ 𝐴)^𝛽. 𝐾. 𝐶. 𝑃. 𝐿𝑆` (11)
> em que 𝑆𝑒𝑑[t/dia] é a produção de sedimentos, 𝑄𝑠𝑢𝑝[mm/ha] é o volume de escoamento
> superficial, 𝑞𝑝𝑖𝑐𝑜[m³/s] é a taxa de pico do escoamento superficial, 𝐴[ha] é a área
> superficial, 𝐾[0,013.t.m².h./m³.t.cm] … 𝛼 e 𝛽 são coeficientes de ajuste, ora adotados
> como 11,8 e 0,56, respectivamente, como proposto por Williams (1975), ora calibrados
> automaticamente."

**Observation of fact:** Fagundes eq. 11 is a word-for-word copy of Buarque eq. 5's unit
list — same "mm/ha", same "[ha]", same K unit string "0,013 t m² h (m³ t cm)⁻¹". Neither
thesis derives these units; both transcribe them.

### Step 1d — the text they are both transcribing: SWAT theoretical documentation

SWAT+ theoretical doc, §4 Erosion / Sediment / MUSLE, VERBATIM (fetched):

> "sed = 11.8*(Q_surf*q_peak*area_hru)^0.56*K_USLE*C_USLE*P_USLE*LS_USLE*CFRG"
> - sed: sediment yield on a given day (metric tons)
> - Q_surf: surface runoff volume (mm H2O/ha)
> - q_peak: peak runoff rate (m³/s)
> - area_hru: area of the HRU (ha)
> - K_USLE: USLE soil erodibility factor (0.013 metric ton m² hr/(m³-metric ton cm))

The Buarque/Fagundes unit strings are this table, translated. **The chain of custody for
"ha" is: SWAT manual → Buarque (2015) → Fagundes (2018) → this project.** No independent
derivation exists anywhere in that chain.

**And the SWAT manual's own unit strings are internally incoherent as written:** "mm
H2O/ha" × "ha" = mm, a depth, not a volume; the text calls Q_surf a "volume". So the
manual cannot be read literally. The arbiter is SWAT's source code.

### Step 1e — SWAT SOURCE CODE (the arbiter), fetched this step

`raw.githubusercontent.com/crazyzlj/SWAT/master/src/ysed.f` (4,720 B) and
`.../src/soil_phys.f` (11,016 B), downloaded and read in full. VERBATIM:

`ysed.f` header block:
```
!!    hru_km(:)   |km**2         |area of HRU in square kilometers
!!    peakr       |m^3/s         |peak runoff rate
!!    surfq(:)    |mm H2O        |surface runoff for the day in HRU
!!    usle_mult(:)|none          |product of USLE K,P,LS,exp(rock)
!!    sedyld(:)   |metric tons   |daily soil loss caused by water erosion
```
`ysed.f` body:
```
        cklsp(j) = usle_cfac(j) * usle_mult(j)
        sedyld(j) = (surfq(j) * peakr * 1000. * hru_km(j)) ** .56 * cklsp(j)
```
`soil_phys.f` lines 108-109:
```
      usle_mult(i) = sol_rock(1,i) * usle_k(i) * usle_p(i)
     &     * usle_ls(i) * 11.8
```

**Decisive.** In the code `surfq` is in **mm** (not mm/ha) and `hru_km` in **km²** (not
ha), and the product carries an explicit `* 1000.` — and `surfq[mm] · hru_km[km²] · 1000`
is *numerically the runoff volume in m³* (1 mm over 1 km² = 1000 m³, exactly). So the
operative first factor of MUSLE in the reference implementation is the **surface runoff
volume in cubic metres**, multiplied by `peakr` in m³/s, with 11.8 in front and metric
tons out. The "(mm H2O/ha)" and "(ha)" in the manual are a documentation artefact; the
implementation is the m³ form.

### Step 1f — the independent authority: HEC-HMS (US Army Corps of Engineers)

Two pages of the same manual, fetched separately, give the two unit systems explicitly:

- Technical Reference, *Modified USLE*, VERBATIM:
  > "Sed = 11.8(Q_surf × q_peak)^0.56 × K × LS × C × P"
  > "Sed = Sediment Yield per Event (metric tons); Q_surf = Surface Runoff Volume (m³);
  > q_peak = Peak Runoff Rate (m³/s)"
  (note: **no area term at all** — because Q_surf is already the volume)
- Applications Guide, UNBRW case study, Equation 11, VERBATIM:
  > "Sed = 95 · (Q_surf × q_peak)^0.56 × K × LS × C × P"
  > "Sed = sediment yield for a given event (tons); Q_surf = surface runoff volume
  > (acre feet); q_peak = peak runoff rate (cubic feet per second)"

So: **95 / 0.56 is the US-customary form (acre-ft, cfs, short tons); 11.8 / 0.56 is the
metric form (m³, m³/s, metric tons).** Confirmed independently by Sadeghi et al. (2014)
review: "Sv is sediment yield (in t) …, Q is volume of runoff (in m³), and qp is peak flow
rate (in m³ s⁻¹) … for the areas where the equation was developed, a and b were 11.8 and
0.56, respectively, for metric system units."

---

### Step 2 — DIMENSIONAL ANALYSIS, in full

**First, the honest statement about what dimensional analysis can and cannot do here.**
MUSLE is an empirical power law; α is *not* dimensionless — it carries whatever dimensions
make the equation balance. Consequently **dimensional homogeneity alone cannot select the
units**: for ANY choice of units for (Q, q_peak, A) there exists some α that works.
(APSIM's erosion documentation says this outright of the same equation family: it "is not
dimensionally correct (the units of E (t/ha) do not match those on the right hand side of
the equation)".) Therefore the question "what units MUST the terms be in for α = 11.8" is
answered not by dimensional homogeneity but by **exact unit conversion of Williams' fitted
US-customary coefficient**. That conversion has one answer and is reproduced below.

**The conversion.** Williams (1975), US-customary: `Y[short ton] = 95 (Q[acre-ft] ·
qp[cfs])^0.56 · K C P LS`. Hold K, C, P, LS fixed (they are the same USLE factors in both
forms — Williams changed only the runoff variables and the mass unit). Let V = runoff
volume in m³ and q = peak rate in m³/s.

- 1 acre-ft = 43,560 ft³ = 43,560 × 0.3048³ m³ = **1233.4818375475 m³**
- 1 cfs = 0.3048³ m³/s = **0.028316846592 m³/s**
- 1 short ton = **0.90718474** metric ton

```
Q[acre-ft] · qp[cfs] = (V / 1233.4818375475) · (q / 0.028316846592)
                     = V·q × 0.0286300662454
Y[short ton] = 95 · (0.0286300662454)^0.56 · (V·q)^0.56 · KCPLS
0.0286300662454^0.56 = exp(0.56 · ln 0.0286300662454)
                     = exp(0.56 · (−3.5534126))  = exp(−1.9899111) = 0.13665858
95 × 0.13665858 = 12.982565            [short tons]
× 0.90718474    = 11.782565            [metric tons]
```

**α = 11.7826 ≈ 11.8, with V in m³ and q in m³/s and the yield in metric tons.**
Agreement to 0.15 % — i.e. 11.8 is the rounded value of this exact conversion.

**Enumerate the alternatives, same arithmetic, same 95:**

| first factor expressed as | numeric relation to V[m³] | metric coefficient that Williams' fit implies |
|---|---|---|
| **runoff volume, m³** | V | **11.7826  → quoted as 11.8 ✔** |
| Q[mm] × A[ha] ("mm·ha") | V/10 | 11.7826 × 10^0.56 = **42.780** |
| Q[mm] × A[km²] ("mm·km²") | V/1000 | 11.7826 × 1000^0.56 = **563.949** |

Only one of the three lands on 11.8. The mm·ha reading requires α = 42.8 and the mm·km²
reading requires α = 564 to be *the same physical equation Williams fitted*. Neither is
11.8, and neither appears anywhere in the literature.

**Secondary discriminator (confirms the short-ton reading).** If Williams' Y had been
metric tons rather than short tons, the conversion would give 12.983, which is 10.0 % from
11.8 — versus 0.15 % for the short-ton reading. The short-ton/m³ combination is the one
that reproduces the quoted metric coefficient.

**So the answer to "if more than one combination is dimensionally admissible":** infinitely
many are *dimensionally* admissible (α absorbs any of them) — which is exactly why the
discrimination has to come from the source conversion, and it does, uniquely.

### Step 1e-bis — RECONCILING THE ha/km² MIXTURE PRECISELY (the task's specific ask)

The mixture is not a mixture of two different physical areas. Both eq. 6 (`Ap`, pixel area)
and eq. 7 (`A`) are the *same* pixel. What differs is which numeric unit each equation's
embedded constant presupposes:

1. **eq. 7 (`q_pico = Dsup·A/86.4`) presupposes A in km²** — provably, because the constant
   86.4 is exactly the km² conversion: 1 mm/d over 1 km² = 1000 m³/d = 1000/86400 m³/s =
   1/86.4 m³/s. In ha the constant would be 8640. So km² is *forced* here by the constant.
2. **eq. 5/6 (`SED = 11.8·(Qsup·q_pico·A)^0.56·…`) presupposes that `Qsup · A` is the
   runoff volume in m³** — provably, because 11.8 is exactly Williams' 95 converted on that
   basis (step 2). The `[ha]` label on `A` and the `[mm.ha⁻¹]` label on `Qsup` are copied
   from the SWAT manual, whose own code (step 1e) computes `surfq[mm]·hru_km[km²]·1000`,
   i.e. m³. The labels are transcription, not derivation, and taken literally they are
   dimensionally incoherent (mm/ha × ha = mm).
3. Therefore the two equations are consistent once stated correctly:
   `q_peak = Dsup[mm/d]·A[km²]/86.4` and `V = Dsup[mm/d]·A[km²]·1000` (or equivalently
   `A[ha]·10`), and MUSLE's first factor is `V` **in m³**. Nothing in eq. 7 contradicts
   anything in eq. 5; the "ha" is a label on a variable, not an instruction to feed the
   product in mm·ha.

### Step 3 — HAND CASE (the number the implementation must reproduce)

Inputs, exactly as specified in the task: Qsurf = 10 mm, q_peak = 1 m³/s, A = 100 ha,
K = 0.3, C = 0.1, P = 1, LS = 1 (FG = 1).

```
1. Runoff volume:
   A = 100 ha = 100 × 10,000 m² = 1.0 × 10^6 m²
   depth = 10 mm = 0.010 m
   V = 1.0e6 × 0.010 = 1.0000e4 m³        = 10,000 m³
2. Energy argument:
   V · q_peak = 10,000 m³ × 1 m³/s = 1.0000e4
3. Raise to β:
   (1.0e4)^0.56 = 10^(4 × 0.56) = 10^2.24 = 173.78008287
4. Multiply by α:
   11.8 × 173.78008287 = 2050.6049779
5. Multiply by K·C·P·LS:
   × 0.3 = 615.18149338
   × 0.1 =  61.51814934
   × 1.0 × 1.0 (P, LS)
6. RESULT:  sed = 61.518 metric tons
```

**Independent cross-check through Williams' own US-customary equation** (no use of 11.8):
```
V = 10,000 m³ = 10,000 / 1233.4818375 = 8.10713194 acre-ft
q = 1 m³/s    = 1 / 0.028316846592    = 35.31466672 cfs
product = 8.10713194 × 35.31466672 = 286.30066245
286.30066245^0.56 = 23.75858205
Y = 95 × 23.75858205 × 0.3 × 0.1 × 1 × 1 = 67.71195883 short tons
  = 67.71195883 × 0.90718474 = 61.42725577 metric tons
```
61.427 (Williams exact) vs 61.518 (α = 11.8 rounded) — **0.15 % apart, the rounding of
11.7826 → 11.8.** The two independent routes agree. **HAND CASE = 61.5 t (61.518 t with
α = 11.8; 61.427 t with Williams' exact 95-form).**

For completeness, the same inputs under the two rejected readings:
- `Q[mm]·A[ha]·q` = 10 × 100 × 1 = 1000 → 1000^0.56 = 47.8630 → 11.8 × 47.8630 × 0.03 =
  **16.944 t**  (= 61.518 / 10^0.56)
- `Q[mm]·A[km²]·q` = 10 × 1 × 1 = 10 → 10^0.56 = 3.63078 → 11.8 × 3.63078 × 0.03 =
  **1.2853 t** (= 61.518 / 1000^0.56)

---

### Step 5 — DECISION (recorded BEFORE step 4, and before looking at any basin total)

**I am writing this decision now, before opening `src/mgb_sediment.py` and before
computing or looking up what it does to the basin total. I have not run the model in this
task and will not, per the constraints.**

> **DECISION: the correct convention is the CUBIC-METRE one. For α = 11.8 and β = 0.56 to
> be the coefficients Williams (1975) fitted, MUSLE's first factor must be the surface
> runoff VOLUME in m³, the peak rate in m³/s, and the output is metric tons; K, C, P, LS
> stay in their USLE (US-customary-numeric) definitions.**
>
> Operationally, at the project's pixel scale a_p = 0.0081 km²:
> `V = Qsur[mm/d] · a_p[km²] · 1000` m³  (equivalently `Qsur[mm/d] · a_p[ha] · 10`),
> `q_peak = Qsur[mm/d] · a_p[km²] / 86.4` m³/s, and
> `Sed[t] = 11.8 · (V · q_peak)^0.56 · K·C·P·LS·FG`.
>
> In the repository's existing vocabulary this is the row named `williams_m3`; the
> registered default `pixel_km2` and the diagnostic `swat_mm_ha` are **both wrong**, by
> 1000^0.56 = 47.863× and 10^0.56 = 3.6308× respectively.

**Justification, in order of weight — all of it derivation or source quotation:**
1. Exact unit conversion of Williams' own fitted coefficient: 95 (acre-ft, cfs, short tons)
   → 11.7826 (m³, m³/s, metric tons). The mm·ha reading demands α = 42.78 and the mm·km²
   reading demands α = 563.95. Only m³ reproduces 11.8 (step 2).
2. The reference implementation says so in code: SWAT `ysed.f` computes
   `(surfq[mm] · peakr · 1000. · hru_km[km²])^0.56 · (11.8·K·P·LS·C·rock)`, and
   `surfq·hru_km·1000` **is** m³ (step 1e).
3. An authority independent of both SWAT and Williams' original — HEC-HMS — states the
   metric form with **Q_surf in m³ and no area term at all**, and the US form with 95 and
   acre-feet, on two pages of the same manual (step 1f).
4. The "[ha]" in Buarque eq. 5/6 and Fagundes eq. 11 is a verbatim transcription of the
   SWAT manual's unit table — the same table whose "mm H2O/ha" is dimensionally
   incoherent and whose own code uses m³. A transcribed label does not outrank the
   conversion that defines the coefficient (step 1e-bis).
5. eq. 7's km² and eq. 5's ha are not in conflict: 86.4 forces km² in the q_peak formula,
   11.8 forces m³ in the erosion formula, and both are satisfied simultaneously by the
   single physical pixel area (step 1e-bis).

**What this decision is NOT based on:** I have not consulted, computed, or reasoned from
any basin total, and no part of the argument above references the 144–184 Mt/yr outlet
anchor. I note explicitly, and it is worth stating as an integrity check, that adopting
this convention does **not** close the gap the run is chasing — it is a 47.863× change
from the current default, which by the repo's own docs/35 §9.1 table still leaves the
result several-fold below the anchor, i.e. the derivation does not deliver a match and I
am not claiming one.

**Residual uncertainty, stated honestly:** what I have established is what units make
α = 11.8 *the coefficient Williams fitted*. I have NOT established what units
Buarque/Fagundes' compiled Fortran actually fed the equation — their source is not
available, only their theses' transcribed labels. If their code used mm·ha, then their
published α = 11.8 was applied in a convention 3.63× below Williams'. That is a statement
about *their* fidelity, not about the right answer, and it does not change the decision:
the question asked is what the units MUST be for 11.8/0.56 to be correct, and that has one
answer. What would settle the secondary question is the MGB-SED source (the `musle.py` /
Fortran of implementation B), which docs/35 §8 records as **not in this repository** —
still blocked.

**Flagged, out of scope, NOT part of this decision — a second unit chain that may be
wrong.** Buarque and Fagundes both give K's unit as "0.013 t m² h (m³ t cm)⁻¹", copied
from SWAT. In SWAT that string denotes the metric equivalent of the US-customary USLE K,
and SWAT's `usle_k` input is entered in **US-customary numeric values** (~0.02–0.69) —
which is consistent with my conversion above, where K was held fixed while only Q, qp and
the mass unit were converted. If this project's `minibacia_soil_params.csv:K` were
populated in SI units (t·ha·h/(ha·MJ·mm), numerically ≈ 0.1317 × the US value), the load
would be low by a further ≈ 7.6×. I flag this for whoever owns the K factor; it is not
part of the volume-convention decision and I did not act on it.

**Checklist status at this point:** 1a ✔ 1b ✔ 1c ✔ 2 ✔ 3 ✔ 5 ✔ (decision recorded).
Proceeding to step 4.

---

### Step 4 — ONLY NOW: the three VOLUME_FACTORS against the hand case

`src/mgb_sediment.py` read (read-only; nothing modified). The primitive is
```
product = qsur * qpeak * area * volume_factor
return alpha * product ** beta * k * c * p * ls * fg
```
with `VOLUME_FACTORS = {'pixel_km2': 1.0, 'swat_mm_ha': 100.0, 'williams_m3': 1000.0}`
applied to `(Qsur[mm] · q_peak[m³/s] · area[km²])`.

Hand case fed through the actual function — `musle_load_tonnes(10.0, 1.0, 1.0, 0.3, 0.1,
1.0, 1.0, volume_factor=f)` (area 100 ha = 1.0 km²), executed output:

| convention | factor | sed (t) | ratio to hand case 61.518149 t |
|---|---|---|---|
| `pixel_km2` (registered default) | 1.0 | 1.285296 | 0.020893 (= 1/1000^0.56) |
| `swat_mm_ha` | 100.0 | 16.943505 | 0.275423 (= 1/10^0.56) |
| **`williams_m3`** | **1000.0** | **61.518149** | **1.000000 — exact** |

**`williams_m3` reproduces the hand case exactly.** The other two do not, by the two
factors derived in step 2 before this was run.

**Documentation defect found in `src/mgb_sediment.py` (NOT fixed — outside my file scope,
reported to the parent).** Lines 374-378, the comment introducing `SWAT_HA_PER_KM2`, state:

> "SWAT's standard MUSLE form carries the area in HECTARES (`Q_surf[mm] * q_peak[m3/s] *
> area[ha]`), which is the form `alpha` = 11.8 is normally quoted with"

The second clause is **false**. SWAT's *manual* prints "ha"; SWAT's *code* (`ysed.f`)
computes `surfq[mm] · peakr · 1000. · hru_km[km²]` = m³, and α = 11.8 is quoted in the
literature (HEC-HMS, Sadeghi et al. 2014) with **Q in m³**. The comment should say that the
hectare label is the manual's, that the implementation is m³, and that 11.8 belongs to m³.
Same correction is due in the module docstring's UNITS section and in docs/35 §9.1, which
says the ha form "is also SWAT's standard MUSLE form … and the form α = 11.8 is normally
quoted with" — same error, same source.

**Checklist: 1a ✔ 1b ✔ 1c ✔ 1d ✔ 1e ✔ 1f ✔ 2 ✔ 3 ✔ 4 ✔ 5 ✔. Task complete.**
Nothing was written outside this journal. No model run, no calibration, no frozen artifact
touched, no basin total computed or consulted in reaching the decision.
