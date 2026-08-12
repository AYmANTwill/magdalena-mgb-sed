# 43 — The C3/C4 gate: **C3 STAYS OPEN · C4 PROCEEDS CONDITIONALLY**

**Written 2026-08-11** by the `decide-c3-c4` agent (process record:
`docs/agents/journal_decide-c3-c4.md`). This document **decides**; it adds no research and
computes no new science. Everything it weighs was measured by three independent lenses whose
process records are `docs/agents/journal_adj-ratio.md`, `journal_adj-alpha-role.md` and
`journal_adj-c4-feasibility.md`.

> **THE DECISION, in one line.** The C3 residual's **level** component is **reclassified** from
> *defect* to *calibration target* — with primary-source evidence, written as `docs/37`
> **Amendment A2** — but its **structural** components are not, so **C3 remains OPEN** on clauses
> 2, 3 and 4″, and **C4 may proceed** under a named, bounded contract and three blocking
> preconditions.

> **`docs/42` G9 disclosure, carried here because this page draws basin-scale conclusions:** at the
> adopted `C`, **66.53 % of the model's gross erosion — 199.29 of 299.54 Mt/yr — is upstream of no
> usable SSC station**; only **33.47 %** is; and **801.1 km of channel, including the whole
> Depresión Momposina, lies below the outlet-most SSC station** (`21237020` ARRANCAPLUMAS), against
> a basin maximum path of 1,425.9 km. Nothing C4 fits can close that.

---

## 1 — The C3 residual, restated precisely

### 1.1 What the residual is *today* — not what it was this morning

The residual must be quoted in its **A1.9 form**, not its A1.4 form. This is the single most
common way the number is misquoted, including by the brief that commissioned this decision.

| statement | status |
|---|---|
| "the implied SDR 0.579–0.740 is above the plausible 0.05–0.30 band" | **RETIRED** (`docs/40`; `docs/37` A1.2). Not a pass and not a fail — the band is uncited here and measures a different quantity (all-source denominator vs our hillslope-only one). |
| "the model is under-erosive by 1.59 – 2.74× / 1.03 – 2.27×" | **WITHDRAWN AS A DIRECTED RESULT** (`docs/37` **A1.9**). The arithmetic is correct and reproduced; the *interpretation* is not. Leg A compared our MUSLE sum against a **RUSLE gross erosion** while SWAT Ch. 4:1 defines this exact equation's output as a sediment **yield**. |
| **the current form** | **The residual's magnitude is bracketed and its DIRECTION IS UNKNOWN: from 2.27× too low (reading A) to 1.49× too high (reading B).** Clause 4″ — "the quantity the MUSLE sum represents is pinned in writing, and the basin-mean rate is consistent with published levels of *that same quantity*" — is **NOT ESTABLISHED**. |

Alongside it, and independent of it, two clauses fail **in known directions**:

- **Clause 2 — a decision is unresolved.** The **LS formulation** (`docs/37` §4 candidate 0): our
  LS sits **2.37× – 3.00×** above the level α = 11.8 is paired with in the MGB-SED lineage, measured
  on our own 90 m grid over all 30,235,916 basin cells. The pre-registered C3.1 comparison
  (`docs/35` §9.3) has not been made.
- **Clause 3 — the 2026-08-11 decisions are unaudited.** The `docs/41` C-revision default change,
  the `docs/40` SDR retirement and the `docs/42` guard registration had no independent review when
  A1 was written.

### 1.2 What each lens established about it

| lens | question | answer | what it establishes about the residual |
|---|---|---|---|
| **1** — `adj-ratio` | does the bias cancel in the ENSO ratio? | **PARTIALLY** | The residual's **period-differential is centred on 1** — four fleet cells, every 95 % CI containing 1 (RE-pooled `expD` 0.848 [0.310, 2.318], 0.801 [0.472, 1.360], 1.791 [0.720, 4.459], 0.815 [0.351, 1.891]); 0.959 with the registered EL PROFUNDO precedence. **But it is not a constant**: I² 96 – 99.2 %, τ 2.03 – 3.40× per station, 18 of 24 station-cells with CIs excluding 1, and the pooled band is as wide as the residual it would certify. |
| **2** — `adj-alpha-role` | what is α for? | **NO — does not block C4** | α and β in the transposed method are **fitted coefficients of adjustment**, not physical constants. Therefore the residual's **level** is not a defect: it is the quantity C4's α exists to supply. |
| **3** — `adj-c4-feasibility` | is C4 feasible? | **PARTIALLY** | C4 is feasible as a **2-free-parameter** fit (Π level, β) plus **1 bounded** (deposition `k`), on **8** stations, not the 13 `docs/42` registered — so whatever C4 supplies to the level, it supplies with a ±38 % 95 % band and no ability to decompose it. |

### 1.3 The reclassification, and its evidence

**The level component of the C3 residual is reclassified from *defect* to *calibration target*.**
Two independent legs, either sufficient:

1. **The method defines it as free.** Fagundes (2018) eq. 11 calls α and β *"coeficientes de ajuste
   … ora adotados como 11,8 e 0,56 … ora **calibrados automaticamente**"*; §6.3.1 puts them in the
   MOCOM-UA parameter vector; they are fitted **per sub-basin** (1, 5 or 17) and **separately against
   each of four observed sediment datasets**, over 1997–2010, with a search prior α ∈ [2.0, 25.0].
   The decisive measurement, from the source's own Appendix IV: **for the same sub-basin in the same
   experiment, fitted α changes by median 1.28× and up to 7.78× depending only on which observed
   dataset was the calibration target** (101 complete rows; 30.7 % spread > 1.5×, 13.9 % > 2×). A
   physical constant cannot do that. An unfitted α is therefore an *unset lever*, not a *wrong value*.
2. **The level has no separate existence to be defective.** `docs/42` §3.1: α, the C level, the LS
   level, the K unit system, the volume convention, P and FG are **seven ways of writing one
   identifiable product Π**, design-matrix condition number measured as **inf**, exactly singular.
   The "level residual" *is* Π. Π is precisely what a C4 fit sets.

**Consequence for `docs/35` §6.1's α band.** Lens 2 falsified it against its own source: running this
repository's unmodified `check_musle_parameters` over all **426** published, adopted (α, β) pairs of
the transposed method returns **STOP on 185 (43.4 %)**, watch on 59, ok on 182 — and **42.7 points of
that STOP rate is the β hard stop 0.45–0.65**, which is dimensionless and therefore cannot be rescued
by any unit or convention argument. Additionally, 97.7 % of the 426 fits land inside the "expected"
5.9–23.6 band **because the source's search prior [2.0, 25.0] contains it** — the statistic measures
the prior, not the physics. *(`docs/35` is a frozen pre-registration; this document does not edit it.
It records that §6.1 is **necessary-and-not-sufficient at best, and mis-specified at worst**, and that
`docs/42`'s structural guards, not §6.1, decide C4. That is already `docs/42` §8.1's position; lens 2
supplies the measured reason.)*

### 1.4 What the reclassification does **not** cover — and this is why C3 stays open

`docs/42` §1's design principle, restated: **a scalar can absorb a level; it cannot absorb a
structure.** Three structures survive the reclassification, all measured:

1. **The LS formulation is level *plus slope-dependent shape*.** Its three levers (slope-length
   limiter ×0.351, `m` cap ×0.502, `S` function ×1.714) act **per cell as a function of slope**, and
   they do not multiply out (0.502 × 1.714 × 0.351 = 0.302 ≠ the joint 0.421). Only the joint
   *level* joins Π. The residual shape is what `docs/42` **G4.1** tests — and G4.1 can **detect** it,
   never fix it. Clause 2 therefore still fails in a known direction, and the fix is a written
   source-grounds decision (C3.1, `docs/35` §9.3), not a fit.
2. **The residual is not constant across stations.** Lens 1: I² 96 – 99.2 %, Cochran Q p ≤ 3.2e-16,
   τ 2.03 – 3.40×, station `expD` spanning 0.203 – 4.550. A single fitted scalar cannot be right at
   more than one station at a time.
3. **The peak deficit is period-dependent** — `R_AMS` 0.808 (La Niña) vs 0.686 (El Niño) ⇒ ×1.096 —
   i.e. structured in the exact dimension C5's headline lives in.

### 1.5 Why "CLOSED" was available and was refused

Closing C3 today would require retiring a **third** successive level clause — SDR (retired) →
4′ (re-opened) → 4″ (not established) — and reading the accumulated retirements as a pass. This
project's standing rule, stated in `docs/40` §8.1 and re-stated in `docs/37` A1.2 and A1.9.6, is that
**a retired gate is neither a pass nor a fail**. A closure assembled from three retirements is
tolerance wearing a verdict's clothes. Separately, clause 2 fails in a known direction and is cheap to
resolve, and clause 3 fails because a level-moving change (`docs/41`, ×1.2043) has had no adversarial
pass while the guard that would catch it (G3.1) is measured blind to anything below a ~4.2× class-C
error on the real fit set.

---

## 2 — THE DECISION

> ## `C3-STAYS-OPEN-C4-PROCEEDS-CONDITIONALLY`

**C3's verdict is unchanged: OPEN.** What changes is *what keeps it open* and *what its residual is
called*.

| # | closure clause | status after this decision | why |
|---|---|---|---|
| 1 | factor chain fully explained | **MET**, unchanged | `docs/37` A1.1 |
| 2 | no decision left unresolved | **NOT MET**, and now **split**: the LS **level** reclassifies into Π (A2); the LS **shape** does not | C3.1 (`docs/35` §9.3) unmade; G4.1 detects but cannot fix |
| 3 | the decisions were independently audited | **NOT MET — upgraded to PARTIAL** | three lenses adversarially audited `docs/35` §6.1, `docs/42` §4, `docs/37` A1.3.4 and found errors in each; **`docs/41` remains unaudited** |
| 4 | ~~implied SDR plausible~~ | **RETIRED** | `docs/40`; `docs/37` A1.2 |
| 4′ | ~~gross hillslope erosion rate consistent~~ | **RE-OPENED** | `docs/37` A1.9 |
| 4″ | the quantity is pinned in writing, and the rate is consistent with published levels **of that quantity** | **NOT ESTABLISHED**, unchanged | A1.9's resolver step (1) not done; this pass declines to do it (§5.3) |
| **5** | the `docs/42` guards are in place for C4 | **MET, with three amendments now required before C4 starts** | §3.1 |

**Each of clauses 2, 3 and 4″ alone forbids closure.**

### 2.1 The problem is RECLASSIFIED, not tolerated — and here is the boundary

| component of the C3 residual | classification after this decision | evidence | who resolves it |
|---|---|---|---|
| **the multiplicative LEVEL** (α, C level, LS level, K units, volume convention, P, FG — i.e. Π) | **CALIBRATION TARGET.** Not a defect. Status: **UNVALIDATED and unfittable-apart** | Fagundes (2018) eq. 11 / §6.3.1 / Appendix IV (α moves ×7.78 with the calibration target); `docs/42` §3.1 (cond = inf) | **C4**, as a fitted Π reported with its equifinal family |
| **the LS slope-dependent SHAPE** | **STILL A DEFECT**, direction known (our LS is 2.37–3.00× high in level and formulation-different in shape) | `docs/37` §4 candidate 0, all 30,235,916 cells | **C3.1** — a written source-grounds decision, *before* any basin total is looked at |
| **station-to-station heterogeneity of the residual** | **STILL A DEFECT**, unresolvable at this fleet size | lens 1: I² 96–99.2 %, τ 2.03–3.40×, 18/24 CIs excluding 1 | not resolvable by C4; needs more both-window stations (n ≈ 19 for ±50 %, n ≈ 94 for ±20 %) |
| **period-dependent peak deficit** | **STILL A DEFECT**, direction known, magnitude registered (×1.096) | `docs/35` §5.4; `docs/33` §7.4 | not resolvable — propagate as a caveat (§5) |
| **which quantity the sum is (yield vs gross erosion)** | **UNRESOLVED LABEL**, not a defect and not a target | `docs/37` A1.9.1 (SWAT Ch. 4:1) | a written, cited answer — A1.9.3 resolver (1) |

**Advancing is justified because the level residual is reclassified with evidence, and because the
components that are *not* reclassified are (i) each named, (ii) each assigned an owner that is not
C4's α, and (iii) two of them are things only C4's own outputs can supply evidence about.** It is not
justified by any of them being small.

### 2.2 Why C4 is not BLOCKED

- **No lens supports blocking**: lens 2 `NO`, lenses 1 and 3 `PARTIALLY` with conditions, and lens 3's
  own verdict is *"PROCEED WITH C4"*.
- **`docs/37` A1.6 already grants it** — C4 may run while C3 is open, held to `docs/42` G1–G9.
- **C4 is the cheapest route to closing part of C3.** G3.1's `c_B` would be *the first independent
  evidence this project has ever had about the Bare class* (station erosion share 0.0 – 75.6 %, the
  largest identifiable contrast in the set); G1.2's `k̂` would be its first measured bound on channel
  deposition. Both are inputs to clauses 3 and 4″. Blocking C4 blocks them.

---

## 3 — The C4 contract: preconditions, bound, and mandatory reporting

### 3.1 THREE BLOCKING PRECONDITIONS — register in `docs/42` §9 **before any search machinery is written**

`docs/42` is a frozen pre-registration whose §9 is its amendment slot, and **this document is not
scoped to edit it**. These are registered here as **blocking conditions on C4's start**; whoever owns
`docs/42` must transcribe them into its §9, dated, before C4 begins. Lens 3 measured all three.

| # | amendment required | measured cost of not doing it |
|---|---|---|
| **P1** | **Correct the fit set from CAL 13 to the CAL 8.** 5 of the 13 have **no paired SSC + observed-Q day** in the registered CAL window 2012–14. Survivors: `23127010` BORBUR-AUT, `22017010` BOCAS, `22017030` BOCAS, `24037390` CAPITANEJO, `26137110` BANANERA LA 6-909, `26127010` EL ALAMBRADO AUT, `24027030` NEMIZAQUE, `21197010` EL PROFUNDO. Lost for hard record-window reasons: CANTERAS, PAILA LA, CARRASPOSO (zero SSC before 2015), BOCATOMA TRIANGULO (619 CAL SSC days but observed Q ends 2009-03-19), MATEGUADUA (neither). **Correct §4.2's power table with it: the fitted-set `k_min` is 0.0209 /km, not 0.0096 /km.** | every §4.2 power number attributed to "the CAL 13" **overstates the fit's power on `k` by 2.2×**, and by **9.7×** against the all-18 guard that will judge it. Fitted area falls 10.1 % → **5.4 %** of the basin. Only **1** of the 3 claimed CAL-CAL nested pairs survives (`22017030` → `22017010`, 39.9 km). |
| **P2** | **Decide the `docs/31` C4.1 ↔ `docs/42` §9 conflict on `21237020` ARRANCAPLUMAS explicitly**, in writing, either way. `docs/31` C4.1 permits upper-mainstem stations upstream of the Momposina in the fit; `docs/42` §9 forbids them. | worth a factor **6.9** on deposition detectability (`k_min` 0.0209 → 0.00303 /km) and takes the fitted area from **5.4 % → 25.1 %** of the basin. Deciding it after seeing a fit is not a decision. |
| **P3** | **Register the deposition coefficient as REPORTED-AS-A-BOUND, not fitted** — or invoke `docs/42` G5 option 2 and state *"this model asserts SDR = 1.0 between hillslope and station"* as a claim. **Register the parameter count as 2 free (Π level, β) + 1 bounded, not 3 free.** | `k` is **not identifiable on the achievable fit set**. Reporting a fitted `k` value would be reporting noise with a decimal point. |

**Also registered, and it is a restriction, not a threshold change:** do **not** relax the Fagundes
success bar (median KGE −0.26 … 0.44). Record alongside it that **the mean predictor scores
KGE = 1 − √2 = −0.414**, so the bar's lower edge sits **0.15 KGE units above no-skill**, and a median
over **8** stations passing it carries very little information. Passing that bar is not evidence of a
good model; failing it is evidence of a bad one.

### 3.2 THE BOUND on C4's output

> **C4 may fit and report a LEVEL (Π) and a SHAPE PARAMETER (β), and may report a BOUND on channel
> deposition. It may not report a validated α, a validated C level, a validated LS level, or a
> validated basin sediment load. Every C4 number is a member of an equifinal family, and the family
> must be printed beside it (`docs/42` G6 item 4).**

Quantitatively, measured by lens 3 on the achievable CAL 8:

| quantity | identifiable? | what C4 may report | the number |
|---|---|---|---|
| **α alone** | **NO** — not partially, not weakly, not at all | never α as a validated value | `cond([1\|f_F\|f_G\|f_B])` = 5.7e3 on the CAL 8; = **inf** in the basin-total form (`docs/42` §3.1) |
| **Π (the level)** | **YES**, as a level only | Π with its band **and** its equifinal family | SE of the fleet-mean level = 0.465/√8 = **0.1644 ln = ±38 % at 95 %** (0.724× – 1.380×). 13 stations would have given ±28.8 % |
| **β** | **YES**, comfortably | β with its CI **and** the confounding note | SE **0.020** at the pessimistic σ_day = 0.809 ln; 95 % half-width **0.039**, against a registered band half-width of 0.10. **Confounded with the surface-runoff partition** — the leverage is entirely the model's own ln `Qsur` spread (`docs/42` G2's warning) |
| **channel deposition `k`** | **NO** on the achievable set | a **BOUND**, never a value | `k_min` **0.0209 /km** on the CAL 8 (its own 60.4 km span ⇒ no sink stronger than **3.54×** detectable); **0.00303 /km** if P2 admits ARRANCAPLUMAS (⇒ **2.87×**); the all-18 **G1.2** residual test stays at **0.00216 /km** ⇒ **2.12×** over its 348.4 km span. **UNCITED and therefore may neither pass nor fail anything:** the retired 0.05–0.30 SDR band would imply k ≈ 0.0020–0.0032 /km over a 600 km path — printed only so a reader can see where 0.0209 sits |
| **a class C value** | only as a **contrast**, and coarsely | G3.1's `c_G`, `c_B` with intervals | minimum detectable class-C error ≈ **4.2×** on the CAL 8 (≈ 2.9× on all 18). **G3.1 could not have seen the ×1.2043 revision `docs/41` made** — so it cannot audit `docs/41`, and clause 3 stays open regardless of how G3.1 comes out |

### 3.3 What C4 must report alongside **every** number

All of `docs/42` G6's five elements, plus `docs/37` A1.6's eight prohibitions, plus these five, which
this decision adds:

1. **The word UNVALIDATED on the level**, in the same table as Π — *cited is not validated*
   (`docs/37` A1.6 item 3), and *fitted is not validated either* (§1.3 leg 2: a fit sets Π, it does
   not test it).
2. **The parameter count as 2 free + 1 bounded**, with the CAL **8** named and the 5 lost stations
   named with their reasons (P1).
3. **`k` as a bound with its span**, in the form *"no first-order channel sink stronger than X× over
   Y km is detectable on this fit set"* — never as a fitted value (P3).
4. **G9's unobserved fraction** — 66.53 % of the model's erosion upstream of no usable SSC station —
   in the same paragraph as any basin-scale statement (`docs/42` G9; reporting FAIL if omitted).
5. **The residual's direction is UNKNOWN** (`docs/37` A1.9). No C4 output may be justified by, or
   compared against, "the model is 2× under-erosive". A fit argued from a withdrawn direction is a
   fit argued from nothing.

### 3.4 What C4 still may NOT do

`docs/37` §5's five prohibitions and A1.6's eight stand unchanged and are not restated here. Three
are re-emphasised because this decision creates the temptation:

- **The reclassification is NOT a licence to fit α to close a level gap.** `docs/35` §6 RULE 0 is
  unchanged. The level is a target because the method defines it as free — *not* because there is a
  gap of known size to be closed. There is no gap of known size (A1.9).
- **`docs/42` G5's precondition is unchanged and is now doubly load-bearing.** A deposition-free fit
  lands α at **6.83 – 8.73**; the α that reproduces Tan's converted level under reading B is
  **7.92 – 8.86**. **These overlap.** A fit that "works" under the flattering reading is nearly
  indistinguishable from one that has silently deleted channel deposition. Only G5's named sink (or
  the stated SDR = 1.0 claim) plus G1.2's `k̂` in the same table can tell them apart — and §3.2 shows
  `k̂` will be a weak bound, which makes the **named claim**, not the number, the thing that carries
  the weight.
- **Passing G1–G8 is not closure of C3.** It constrains the model over 33.47 % of its own erosion.

---

## 4 — Consequential documents

| document | what this decision requires | status |
|---|---|---|
| `docs/37` | **Amendment A2**, appended (this pass). A1 and the original verdict are **not** rewritten. | **DONE** |
| `docs/37` §1 row 4, §2's premise and requirement rows, §4 residual 3 | `docs/40` §8.2's paste-ready corrections, applied **in place** as strike-through + pointer so the retired gate can no longer be quoted from the body, and nothing is deleted | **DONE** — `docs/37` A2.7 |
| `docs/42` §9 | preconditions **P1, P2, P3** of §3.1, transcribed and dated | **OWED — blocking on C4's start.** Not this pass's file. |
| `notebooks/18_musle_construction.ipynb` §6.4/§7 + `src/nbgen/make_nb18.py` | still present clause 4′ as a directed like-for-like result, in *executed* cells (`docs/37` A1.7 item 7). Needs a generator edit **plus** a full re-execution. | **OWED**, unchanged |
| `tests/test_sediment.py` | two stale hard-coded C assertions; suite is 94 passed / 2 failed (`docs/37` A1.7 item 2) | **OWED**, unchanged |
| `docs/00_INDEX.md` | gains a row for this document, and its "Is stage C3 closed?" answer should point here | **OWED** — not this pass's file |

---

## 5 — What C5 must carry as a caveat, regardless of how C4 comes out

Registered here so that it is fixed **before** C5 produces a headline. All three are measured, none is
optional, and each must appear **with** the number it qualifies — not in a footnote.

### 5.1 The β-compression of variability — and that β is not a lever on the contrast

Because `q_peak = Qsur · a_p / 86.4` in this implementation, the MUSLE product is `∝ Qsur²`, so the
simulated flux scales as **`Qsur^{2β}` — effective exponent 1.12 at β = 0.56, not 0.56.** (Lens 1
derived and inverted this; quoting `β = 0.56` as the exponent is an error the record has now made
once.) The consequence is stark and must be stated:

| | basin `Qsur` ratio | simulated flux ratio at β = 0.56 | across the **whole** registered β band 0.45 – 0.65 (exponent 0.90 – 1.30) | observed (`docs/34`) |
|---|---:|---:|---|---:|
| primary pair | 1.9545 | **2.1182** (run: 2.2915) | **1.83× – 2.39×** | 2.8× – 4.6× |
| sensitivity pair | 3.3598 | **3.8857** (run: 3.9725) | **2.98× – 4.83×** | 6.4× – 9.3× |

> **Registered statement for C5: the basin-total simulated ENSO contrast is the surface-runoff
> contrast raised to 2β and essentially nothing else. β cannot reach the observed basin-total
> contrast anywhere inside its registered band. Therefore a C4 fit that appears to improve the
> contrast has either moved outside the β band (a `docs/42` G2.3 hard stop) or is not doing what it
> appears to be doing.** To hit the observed contrast on the product would need a ratio of 6.4 – 15.4
> (primary) or 27.5 – 53.8 (sensitivity), i.e. a `Qsur` ratio of 2.54 – 3.92 or 5.25 – 7.34 — a
> hydrology change, not a sediment one. *(The 0.90/1.30 endpoints are this pass's arithmetic on lens
> 1's registered `Qsur` ratios and `docs/35` §6.3's band; the run values 2.2915 / 3.9725 are
> `docs/37` A1.3.4's, reproduced by lens 1 to 4 d.p.)*

**This must be reported together with §5.3's comparison-basis correction and never alone**, because
alone it reads as a model failure and §5.3 shows most of the apparent shortfall is a comparison
artifact.

### 5.2 The peak deficit's period-dependence

`R_AMS` **0.808** (La Niña 2011) vs **0.686** (El Niño 2015–16) ⇒ `0.8875 / 0.8097` = **×1.096**: the
dry phase is suppressed harder than the wet one, so **every simulated contrast is overstated by
≈ +9.6 %** from the peak-magnitude channel alone, and the count channel (`R_POT` 0.500 vs 0.464)
points the same way. Peak-corrected: primary **2.0908×**, sensitivity **3.6245×**.

> **Registered statement for C5: this is not a conservative error — it flatters the headline. It must
> be quoted with every simulated contrast (`docs/35` §5.4, `docs/42` G7), and the observed contrast
> carries no counterpart because it is measured.** Related and separately mandatory: the peak deficit
> is **structural** — 81.8 % of observed POT events have no simulated partner at ±2 d (`docs/36`) —
> so the simulated sediment level is an explicit **lower bound**, and "43 % of flood events missed" is
> a *count* statement that may never be quoted without the 81.8 % event-identity figure beside it.

### 5.3 Ratio stability — what lens 1 measured, in both directions

**The good half.** The C3 residual's period-differential is **centred on 1**: RE-pooled `expD` =
0.848 [0.310, 2.318] (primary, est. a, n = 6), 0.801 [0.472, 1.360] (primary, b, n = 7),
1.791 [0.720, 4.459] (sensitivity, a, n = 4), 0.815 [0.351, 1.891] (sensitivity, b, n = 7) — **every
CI contains 1**; 0.959 (geo-mean) / 1.079 (median) under the registered EL PROFUNDO precedence. Sign
tests p = 0.45 – 1.00 against a **minimum attainable** two-sided p of 0.031 (n = 6) / 0.016 (n = 7),
so the test had the power to detect a unanimous direction and did not. `expD` is invariant to α, β's
prefactor, LS, C, P, K units, the volume convention, FG and any constant SDR — which is why it is
decidable when the level is not.

**The bad half.** The differential is **not a constant**: Cochran Q = 75.3 – 783.6 (p ≤ 3.2e-16),
**I² 96.0 – 99.2 %**, τ = 0.707 – 1.225 ln (**2.03× – 3.40× per station**), station `expD` spanning
**0.203 – 4.550**, and **18 of 24 station-cells with CIs excluding 1**. The pooled band [0.310, 2.318]
is as wide as the residual it is meant to certify. Constancy is **neither refuted nor established**;
it is unresolvable at n = 4 – 7 stations. Certifying it to ±50 % needs **n ≈ 19**; to ±20 %, **n ≈ 94**.

**The correction this owes `docs/37` A1.3.4** (carried into A2 §A2.3): its *"simulated contrast short
by 1.22 – 2.01× (primary) / 1.61 – 2.34× (sensitivity)"* is largely a **comparison-basis artifact** —
a **basin-total** simulated ratio against a **fleet-median tributary-station** observed ratio on a
**different day set**, three mismatches at once, worth **×2.14** (est. a) and **×1.27** (est. b), of
which the day set alone is ×1.69. Repaired to like-for-like (same stations, same days, same
estimator), **the model reproduces the observed contrast to within 8 % in three of six cells and
within 1.29× in five of six**: obs/sim of the medians = 0.942, 1.015, 0.923, 2.213, 0.930, 1.289.

> **Registered statements for C5, all mandatory:**
> 1. **Fleet-aggregate only.** No per-station simulated contrast may be attributed to the model.
> 2. **Quote the envelope, not the central value** — [0.310, 2.318] on the primary (a) cell.
> 3. **Report both window pairs, unaveraged** (`docs/34` §1.1). They disagree by ~2.2× on estimator
>    (a) and that disagreement is a finding.
> 4. **Score any comparison day-matched and station-matched**, or say in the same sentence that it is
>    not. The basin-total-vs-station-median comparison is the error this project already made once.
> 5. **Quote §5.2's +9.6 % with every simulated contrast**, and §5.1's exponent statement with any
>    claim about what drives the contrast.
> 6. **Rates only.** Windows are 12 vs 24 months; window totals are never divided by each other
>    (`docs/34` §1.1; `docs/37` A1.3.4).

### 5.4 One spatial finding that is not a C5 caveat but must not be lost

The apparent delivery ratio `r = obs/sim` spans **0.0039 – 1.239 across 46 station-windows — a factor
of 322** — and **exactly one station of eighteen (`23127010` BORBUR) has `r > 1`**, i.e. observed flux
exceeding the model's entire upstream hillslope erosion. That is a **local, like-for-like instance of
`docs/40`'s Leg-B impossibility argument, at one station rather than basin-wide**, and it is evidence
about the level that does not depend on any published comparator. It belongs in C4's G1 discussion.

---

## 6 — Disclosure

- **Decision recorded before it was written.** `docs/agents/journal_decide-c3-c4.md` Step 2 carries
  the decision and its reasoning, written before any of it entered a numbered document, and it
  discloses the one piece of arithmetic (§5.1's β-band endpoints) done during deliberation.
- **Files written by this pass:** `docs/43_c3_c4_gate.md` (this file), `docs/37_c3_closure.md`
  (Amendment **A2** appended + the `docs/40` §8.2 corrections applied in place as strike-through with
  pointers, nothing deleted), `docs/agents/journal_decide-c3-c4.md`. Nothing else.
- **`docs/42` was NOT edited**, though lens 3 requires three amendments in its §9. They are recorded
  in §3.1 as blocking preconditions for whoever owns that file. Editing a frozen pre-registration was
  outside this pass's scope.
- **No research was added.** No new measurement was made; every number here is a lens's or a prior
  document's, cited to it. The only arithmetic performed is §5.1's β-band endpoints and §3.2's
  `exp(k_min × span)` bounds, both flagged in place.
- **No frozen artifact was opened or written**: `sim_calibrated_v2/{h2e_drivers.npz,
  parameters_H2E.csv, q_gauge_H2E.npz}` untouched. **No calibration was launched. No simulation was
  run. No headline number was moved. Nothing is backdated. No git command was run.**
- **Gauge-referenced t/km²/yr yields remain embargoed** (`docs/23` §13.2). Every specific-erosion
  figure referenced here is model-internal and is labelled so in its source document.
- **Uncited quantities are named as such** and used to pass or fail nothing: the 0.05 – 0.30 SDR band
  and its implied `k` ≈ 0.0020 – 0.0032 /km (§3.2); the ENSO-neutrality of the CAL window 2012–14,
  which `docs/31` asserts with no in-repo ONI table behind it (lens 3 issue 5) — **UNCITED**, and it
  matters because it is the premise of the fit/evaluation split.
