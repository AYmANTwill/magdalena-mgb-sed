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
  LS sits ~~**2.37× – 3.00×**~~ above the level α = 11.8 is paired with in the MGB-SED lineage, measured
  on our own 90 m grid over all 30,235,916 basin cells. The pre-registered C3.1 comparison
  (`docs/35` §9.3) has not been made.
  ⚠ **AMENDMENT 3, 2026-08-12 (§7): read `1/f_LS` = 2.3151× – 3.9768×**, `f_LS` ∈
  **[0.25146, 0.43194]** erosion-weighted — and the source formulation **read whole is a POINT at
  ×0.25146** (`1/f_LS` = 3.9768×), while ×0.43194 is a documented **HYBRID** that keeps **our** `L`.
  The C3.1 comparison **has since been made**: `docs/37` §A3 (2026-08-12) records **ADOPT-SOURCE**
  at `ls_formulation = buarque_2015_dg`, *determined and recorded but not yet exercisable*, with
  **C3 still OPEN and C4.3 still BLOCKED** — `docs/37` is that amendment's owner and its text wins
  over this pointer.
- **Clause 3 — the 2026-08-11 decisions are unaudited.** The `docs/41` C-revision default change,
  the `docs/40` SDR retirement and the `docs/42` guard registration had no independent review when
  A1 was written.

### 1.2 What each lens established about it

| lens | question | answer | what it establishes about the residual |
|---|---|---|---|
| **1** — `adj-ratio` | does the bias cancel in the ENSO ratio? | **PARTIALLY** | The residual's **period-differential is centred on 1** — four fleet cells, every 95 % CI containing 1 (RE-pooled `expD` 0.848 [0.310, 2.318], 0.801 [0.472, 1.360], 1.791 [0.720, 4.459], 0.815 [0.351, 1.891]); 0.959 with the registered EL PROFUNDO precedence. **But it is not a constant**: I² 96 – 99.2 %, τ 2.03 – 3.40× per station, 18 of 24 station-cells with CIs excluding 1, and the pooled band is as wide as the residual it would certify. |
| **2** — `adj-alpha-role` | what is α for? | **NO — does not block C4** | α and β in the transposed method are **fitted coefficients of adjustment**, not physical constants. Therefore the residual's **level** is not a defect: it is the quantity C4's α exists to supply. |
| **3** — `adj-c4-feasibility` | is C4 feasible? | **PARTIALLY** | C4 is feasible as a **2-free-parameter** fit (Π level, β) plus **1 bounded** (deposition `k`), on **8** stations, not the 13 `docs/42` registered — so whatever C4 supplies to the level, it supplies with a ~~±38 %~~ 95 % band and no ability to decompose it. ⚠ **AMENDMENT 1, 2026-08-12 (§7): the band is the station bootstrap, `Π̂ × [0.29, 3.73]`** — ~4× wider in log units than ±38 %. The clause's point (*"no ability to decompose it"*) is unchanged and strengthened. |

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
   limiter ×0.351, ~~`m` cap ×0.502~~, `S` function ×1.714) act **per cell as a function of slope**, and
   they do not multiply out ~~(0.502 × 1.714 × 0.351 = 0.302 ≠ the joint 0.421)~~. Only the joint
   *level* joins Π.
   ⚠ **AMENDMENT 2, 2026-08-12 (§7) — two corrections, and one standing instruction.** (a) The
   ×0.502 object is **`min(m, 0.5)`, which is NOBODY's published formulation and may never be graded
   CITED**; **Buarque eq. 14 is a STEP FUNCTION** on slope **percent**, worth **×0.505092**
   area-weighted / **×0.522043** erosion-weighted. (b) The struck product-vs-joint arithmetic is
   restated on the erosion-weighted re-run as **joint / product = ×1.34762**, and **a product of
   single-lever factors may NEVER be quoted as the joint factor.** (c) There are **FOUR** levers,
   not three — the `L` form is the fourth. Full restatement in §7. The residual shape is what `docs/42` **G4.1** tests — and G4.1 can **detect** it,
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
pass while the guard that would catch it (G3.1) is measured blind to anything below a ~~~4.2×~~ class-C
error on the real fit set.
⚠ **AMENDMENT 4, 2026-08-12 (§7): `~4.2×` is σ_r-scaled and therefore wrong, and NO corrected value
is offered** — three passes have produced three answers (`docs/47` open item **O8**). G3.1's
blindness is **worse**, not better, than printed, so the clause-3 conclusion is unchanged; the
*number* may not be quoted.

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
| **the LS slope-dependent SHAPE** | **STILL A DEFECT**, direction known (our LS is ~~2.37–3.00×~~ high in level and formulation-different in shape) → ⚠ **AMENDMENT 3, 2026-08-12 (§7): 2.3151× – 3.9768×**, and **3.9768×** at the adopted POINT | `docs/37` §4 candidate 0, all 30,235,916 cells | **C3.1** — a written source-grounds decision, *before* any basin total is looked at. ⚠ **Taken 2026-08-12: `docs/37` §A3, ADOPT-SOURCE at `buarque_2015_dg`, not yet exercisable; the SHAPE defect is NOT thereby repaired** |
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
| **P1** | **Correct the fit set from CAL 13 to the CAL 8.** 5 of the 13 have **no paired SSC + observed-Q day** in the registered CAL window 2012–14. Survivors: `23127010` BORBUR-AUT, `22017010` BOCAS, `22017030` BOCAS, `24037390` CAPITANEJO, `26137110` BANANERA LA 6-909, `26127010` EL ALAMBRADO AUT, `24027030` NEMIZAQUE, `21197010` EL PROFUNDO. Lost for hard record-window reasons: CANTERAS, PAILA LA, CARRASPOSO (zero SSC before 2015), BOCATOMA TRIANGULO (619 CAL SSC days but observed Q ends 2009-03-19), MATEGUADUA (neither). **Correct §4.2's power table with it: the fitted-set `k_min` is 0.0209 /km, not ~~0.0096 /km~~.** ⚠ **AMENDMENT 6, 2026-08-12 (§7): the NUMBER is right and the ATTRIBUTION is wrong** — read *"not 0.00964 /km"*; `docs/42` §4.2 mis-printed that cell as **0.0104**, and its own §9.5 (A-P1.1) recomputed it to **0.00964** and closed `docs/47` **O7**. Both figures are at the **registered** σ_r; see amendment 4 for the σ correction. | every §4.2 power number attributed to "the CAL 13" **overstates the fit's power on `k` by 2.2×**, and by **9.7×** against the all-18 guard that will judge it. Fitted area falls 10.1 % → **5.4 %** of the basin. Only **1** of the 3 claimed CAL-CAL nested pairs survives (`22017030` → `22017010`, 39.9 km). |
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
| **Π (the level)** | **YES**, as a level only | Π with its band **and** its equifinal family | ~~SE of the fleet-mean level = 0.465/√8 = **0.1644 ln = ±38 % at 95 %** (0.724× – 1.380×). 13 stations would have given ±28.8 %~~ → ⚠ **AMENDMENT 1, 2026-08-12 (§7): SE 0.4775 ln (est a) / 0.6936 ln (est b); the band is the STATION BOOTSTRAP, `Π̂ × [0.29, 3.73]`**, and it is quoted with the sentence *"the level is set by 8 stations whose residuals span a factor of 412"*. The **±28.8 %** 13-station figure is **struck with NO replacement** — a 13-station residual set does not exist |
| **β** | **YES**, comfortably | β with its CI **and** the confounding note | SE **0.020** at the pessimistic σ_day = 0.809 ln; 95 % half-width **0.039**, against a registered band half-width of 0.10. **Confounded with the surface-runoff partition** — the leverage is entirely the model's own ln `Qsur` spread (`docs/42` G2's warning) |
| **channel deposition `k`** | **NO** on the achievable set | a **BOUND**, never a value | ~~`k_min` **0.0209 /km** on the CAL 8 (its own 60.4 km span ⇒ no sink stronger than **3.54×** detectable); **0.00303 /km** if P2 admits ARRANCAPLUMAS (⇒ **2.87×**); the all-18 **G1.2** residual test stays at **0.00216 /km** ⇒ **2.12×** over its 348.4 km span.~~ → ⚠ **AMENDMENT 4, 2026-08-12 (§7): CAL 8 → 0.0838 /km (≈ 173× over 61.5 km); +ARRANCAPLUMAS → 0.01210 /km (≈ 62.3×); all-18 G1.2 → 0.0066 – 0.0069 /km, central 0.00686 ⇒ ≈ 10× over ~342 km. The factor 6.9 between the first two SURVIVES (0.0838/0.01210 = 6.926). And the comparative is inverted: with the verb *detectable* it is "no sink WEAKER than X× is detectable"** (`docs/42` §9.7). **UNCITED and therefore may neither pass nor fail anything:** the retired 0.05–0.30 SDR band would imply k ≈ 0.0020–0.0032 /km over a 600 km path — printed only so a reader can see where 0.0209 sits |
| **a class C value** | only as a **contrast**, and coarsely | G3.1's `c_G`, `c_B` with intervals | ~~minimum detectable class-C error ≈ **4.2×** on the CAL 8 (≈ 2.9× on all 18)~~ → ⚠ **AMENDMENT 4, 2026-08-12 (§7): σ_r-scaled, therefore wrong; NO CORRECTED VALUE — `docs/47` open item O8.** Three passes, three answers. Only the qualitative statement is quotable: **the registered figures are too optimistic by roughly the σ_r factor, so G3.1 is blinder than printed.** **G3.1 could not have seen the ×1.2043 revision `docs/41` made** — so it cannot audit `docs/41`, and clause 3 stays open regardless of how G3.1 comes out |

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
  lands α at ~~**6.83 – 8.73**~~; the α that reproduces Tan's converted level under reading B is
  **7.92 – 8.86**. ~~**These overlap.**~~ ~~A fit that "works" under the flattering reading is nearly
  indistinguishable from one that has silently deleted channel deposition.~~
  ⚠ **AMENDMENT 5, 2026-08-12 (§7): the two bands are at DIFFERENT `cp_revision`s, and at the
  adopted one they are DISJOINT.** `6.83 – 8.73` is `11.8 × {144, 184} / 248.730` — the **prior** C
  level. At the **adopted** C it is `11.8 × {144, 184} / 299.5387088405831` = **5.673 – 7.248**,
  against reading B's **7.92 – 8.86**: a **gap of 0.672 in α**, no overlap. **The reasoning above is
  wrong; the caution it supports survives on other grounds** (§7 amendment 5). Whether the
  *conclusion* about G5 changes is `docs/47` open item **O12**, still open. Only G5's named sink (or
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

> ⚠ **AMENDMENT 7, 2026-08-12 (§7) — a MANDATORY RIDER on the registered statement above, because
> registered statements are quoted verbatim by design and this one embeds the artifact §5.3 of this
> same document forbids.** The comparison it makes is a **basin-total simulated** ratio against a
> **fleet median of tributary-station observed** ratios on a **different day set** — three
> mismatches at once, which §5.3 measures at **×2.14** (est a) / **×1.27** (est b), of which the day
> set alone is ×1.69. **The registered statement may not be quoted without this rider in the same
> paragraph.** `docs/47` §2.5 **C2** reports that, repaired to like-for-like, the *simulated*
> contrast **exceeds** the observed (simulated median 4.903 vs observed 4.620, obs/sim 0.9423);
> **those two numbers are carried from `docs/47` and were NOT verified by this pass**, so they are
> recorded as owed, not adopted (§7 amendment 7).

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

---

## 7 — Amendment slot — **OPEN from 2026-08-12**

**This document had no amendment slot; it ends at §6. This section creates one**, on the model of
`docs/42` §9 and `docs/46` §10. **Rules, fixed here so the slot cannot be abused:** amendments are
**appended**, dated, each naming its source and the session that wrote it; **nothing in §1–§6 is
deleted, renumbered or silently rewritten** — where a superseded number must stop being quotable
from the body it is struck in place (`~~…~~`) with a dated pointer to the amendment that replaces
it, the `docs/37` A2.7 precedent, and the original string stays readable; and **no threshold, no
registered statement and no decision of §2 is changed by an amendment that only corrects a
number.**

**Opened by the `amend-4243-piband` agent, 2026-08-12; process record
`docs/agents/journal_amend-4243-piband.md`.** Seven amendments, all dated 2026-08-12. Sources:
`docs/47` §2.2 (**D2**), §2.5 (**C1**, **C2**), §6.2 items 3–4; `docs/48` §3–§5; `docs/46` §2.5.1
and §7.3 items 2–3; `docs/42` §9.6 flags **F1**/**F2** and its new §9.7 (**A-P4**), enacted the
same day. **Nothing here creates a materiality bar** — `docs/52` struck the only one this project
had and replaced it with **no number**, and no band width below may be read as a threshold for
deciding whether two numbers differ.

> **Slot addendum, 2026-08-12 (`defect-45-residual`).** The *"Seven amendments"* above is the
> `amend-4243-piband` pass's own count and is left as written. **An eighth was appended the same
> day** by a different session, correcting amendment 3's area-weighted **proxy** upper end
> (×0.42148 → 0.42136300143291305) on the authority of `docs/46` §10 amendment 2 / `docs/51` §9
> amendment 1. **It changes no registered statement, no threshold and no decision** — see
> amendment 8. §7.2 remains the `amend-4243-piband` pass's disclosure; amendment 8 carries its own.

---

### Amendment 1 — 2026-08-12 — **§3.2's Π band is REPLACED by the station bootstrap**

**Source:** `docs/47` §2.2 (**D2**) and §6.2 item 3; measured and blast-radiused in `docs/48`
§2–§3. **Sites:** §3.2's Π row (struck in place), §1.2's lens-3 row (struck in place).

**The defect.** §3.2 wrote `SE of the fleet-mean level = 0.465/√8 = 0.1644 ln = ±38 % at 95 %`.
`0.465 ln` is `docs/42` §4.2's **σ_r**, and `docs/42` derives it — correctly — as the disagreement
between two **observed-flux estimators** (`0.658/√2`). **Neither estimator has seen the model.**
The quantity this SE requires is the sd of `r_i = ln(flux_sim_i) − ln(flux_obs_i)`, whose variance
is observation error **plus** model error **plus** between-station heterogeneity, and which is
bounded **below** by the observation term. Measured on the registered CAL window, CAL 8, primary
estimator (b): **1.9618 ln (×4.22)**, so the SE is **0.6936 ln**, not 0.1644 (est (a): 1.3506 ⇒
**0.4775**). **The ±38 % band is ~4× too narrow in log units.** `docs/42` §9.7 (A-P4) enacts the
same retirement in the document that registered σ_r.

> ## THE REPLACEMENT — REGISTERED HERE FOR §3.2
>
> **The 95 % band on Π̂ is the STATION-LEVEL BOOTSTRAP of the fleet-mean per-station log residual:
> resample the CAL stations with replacement 10,000 times, recompute the fleet mean inside each
> resample, take the 2.5 / 97.5 percentiles.**
>
> ```
> Pi_hat  x  [0.29, 3.73]     (95 %, station bootstrap, union over registered estimators (a), (b))
> ```
> **and the sentence *"the level is set by 8 stations whose residuals span a factor of 412"*
> appears beside it, every time** (`docs/47` §6.2 item 3; measured 412.1, `exp(6.0214)` = 412.16).
>
> **The band is a PROCEDURE, not a constant.** C4 recomputes it on its own adopted fit's residuals
> and reports what it gets. The numbers above are what the procedure evaluates to at the unfitted
> defaults on the registered CAL window, registered as the **pre-fit expectation** so that a
> materially different C4 number is itself reportable. Two reasons this must be a procedure:
> the sd is **β-dependent** (CAL-8 est (b) rises monotonically 1.875 → 2.100 across the registered
> β box, `docs/48` §6.1 P5), and the two registered estimators disagree on the width by a factor
> of **1.51** in log units (`docs/48` §6.1 P1, still open).

**The per-estimator numbers, so the union is auditable** (`docs/48` §3.3, seed 20260810, 10,000
station resamples): est **(a)** point +2.5772 ln, CI about the point [−0.8279, +0.8721] ⇒ band
**×0.418 – ×2.289**; est **(b)** point +1.9240 ln, CI [−1.3163, +1.2503] ⇒ band **×0.286 –
×3.730**. Mean half-widths **0.8500** (a) / **1.2833** (b); full widths 1.7000 / 2.5666 ln. The
union is (b)'s band, rounded to `[0.29, 3.73]`.

> **A trap this pass verified by arithmetic, recorded because applying the band wrongly INVERTS
> it.** The band on the **level multiplier** is the **reciprocal** of the bootstrap CI on the
> residual: `r_i = ln(sim/obs)`, so a positive residual means the level must come **down**.
> `exp(−0.8279), exp(+0.8721)` = 0.4370, 2.3919 — which is **not** the band; `exp(−hi), exp(−lo)` =
> **0.4181, 2.2885** is, and est (b) gives **0.2864, 3.7296**. `docs/48`'s printed bands are
> correct; the flip is implicit in them. **Do not re-derive the band from the CI without it.**

#### Why route 2 (the bootstrap) and NOT route 1 (G12's LOO range promoted to a band)

`docs/47` §2.2 names two routes and requires one be chosen. **Route 1 is rejected**, on two
measurements rather than a preference (`docs/48` §3.2, both reproduced by this pass):

1. **It is arithmetically degenerate.** For a mean, the jackknife SE is *identically* `s/√n` and
   the LOO range is *identically* `range(r_i)/(n−1)`. Measured: jackknife SE **0.6936** =
   `sd/√n` **0.6936**; LOO range **0.8602** = `6.0214/7` **0.8602**. So route 1 delivers either the
   corrected normal band under another name, or a **range** — and a range is not an interval;
   converting one into a 95 % band needs a constant this repository cannot cite. **`docs/40`
   retired one uncited band and `docs/47` §8 refuses to invent another. This one would be
   invented.**
2. **It destroys G12.** G12's entire content is the comparison *LOO range vs the level band*.
   Define the band from the LOO quantities and the comparison is circular. And the arithmetic is
   worse than circular — it is **self-cancelling**: at the registered ±0.322 ln (full width 0.6445)
   the measured LOO range 0.8602 **exceeds** it and **G12 FIRES**; at the corrected normal band
   (full width 2.7190) or the bootstrap band (2.5666) it does **not**. **Correcting the band
   switches a firing guard off by widening the thing it is compared against** — the shape of every
   gate failure this project has already refused.

**Consequently, and it is part of this amendment:** **G12's `0.644 ln` full width is retained as a
STANDALONE registered fragility threshold**, decoupled from the level band, with its origin
recorded (it was `1.96 × σ_r/√8`, and it keeps that value as a threshold, not as an SE). Its
diagnostic content survives the correction intact and is worth keeping: **an LOO range of
0.8602 ln means that deleting one of the eight CAL stations moves the fitted level by up to
`exp(0.8602)` = 2.36×.** That is exactly what G12 was written to surface, it is measured, and it
fires.

#### The relationship to `docs/45` §8 — named, not pre-empted

**G12 and the mandatory "quote Π with its band" sentence live in `docs/45`, not here.** `docs/47`
§6.1 **B5** assigns that half of this repair to a **`docs/45` §8 amendment by `docs/45`'s owner**;
at this pass's read, `docs/45` §8 still read *"Empty at registration"*. **This amendment therefore
binds §3.2 of THIS document only, and names the `docs/45` §8 amendment as the instrument that must
carry the same replacement into `docs/45` §2.2, §3.1, §5.3, §6.2 item 2, §7.1 and G12.** It does
not write, quote or presume the content of that amendment.

> **If the two disagree: `docs/45` §8 WINS**, on three grounds — `docs/45` is the C4
> pre-registration C4.3 is actually held to (`docs/45` §1.1); §3.2 of this document is a *bound on
> what C4 may report*, which `docs/45` §6 operationalises; and the band is a **reporting** number
> in `docs/45`, whose §6.1 ADOPT conditions do **not** read it (`docs/48` §3.4), so a disagreement
> cannot flip an outcome. **What must not happen is silence:** if `docs/45` §8 registers a
> different band, this amendment is superseded **in writing**, dated, at this site — and if
> `docs/45` §8 registers **no** band at all, then the ±38 % band **remains struck and unreplaced**,
> and C4 may not quote a band on Π at all until one is registered. **A struck band does not revert
> to ±38 % by default.**

**What this amendment does NOT change.** It does not touch `SE(β) = 0.020` / half-width 0.039 in
the same table (built on σ_day = 0.809, the rating residual, not σ_r — `docs/47` R4); the `b_obs`
IQR **0.464** yardstick (independently measured; the near-equality with 0.465 is coincidence); the
`cond` figures 5.7e3 / inf in the α row; §3.2's **BOUND** itself; or any of §3.3's five mandatory
reporting elements. **A wider band rescues nothing** — it spans a factor of **13.0** where the
registered one spanned **1.91**, and nothing that failed passes because of it.

---

### Amendment 2 — 2026-08-12 — **§1.4's ×0.502 is NOT Buarque eq. 14, and the product is NOT the joint**

**Source:** `docs/46` §7.3 item 2 (re-hung **UNCONDITIONAL** by its amendment (c)) and §2.2;
`docs/49`; the standing instruction on products of single-lever factors. **Site:** §1.4 item 1
(struck in place). **Enacted in parallel at `docs/37` A3.3.1 by that document's owner.**

**(a) The label is wrong, and the object it labels may never be graded CITED.** §1.4 calls the
×0.502 lever *"the `m` cap"* and the corpus has repeatedly called it *"his eq. 14"*. **Buarque
(2015) eq. 14 is a STEP FUNCTION**, printed on p. 47 and corroborated on p. 48:

> `m = 0.2` for `Sf < 1 %` · `0.3` for `1 % ≤ Sf < 3 %` · `0.4` for `3 % ≤ Sf < 5 %` · `0.5` for
> `Sf ≥ 5 %`, where **`Sf` is the pixel slope in PERCENT** (*"onde Sf [%] é a declividade do
> pixel"*).

Measured on our field, the **step** is worth **×0.505092** area-weighted / **×0.522043**
erosion-weighted. The ×0.502 object actually implemented and measured is **`min(m, 0.5)`** — a cap
on the McCool-89 continuous `m`. **`min(m, 0.5)` is nobody's published formulation and MAY NEVER
BE GRADED `CITED`** (`docs/46` §2.2). Its erosion-weighted value is **×0.517480**. The two differ
by **×1.008878** erosion-weighted / ×1.005212 area-weighted — *immaterial in size, and the label is
wrong regardless of the size*, which is why `docs/46` §7.3 item 2 made the correction
unconditional.

**(b) The product-vs-joint arithmetic, restated to comply with the standing instruction.** §1.4
printed `0.502 × 1.714 × 0.351 = 0.302 ≠ the joint 0.421`. That is arithmetically true
(0.302010228) and it is written in a form the project has since forbidden. **The compliant
statement, erosion-weighted, on the exact re-run:**

| quantity | value |
|---|---|
| slope-length limiter, one DEM pixel | **×0.362435** |
| `m` → **Buarque eq. 14 STEP** (the CITED object) | **×0.522043** |
| `m` → `min(m, 0.5)` **CAP** (never CITED) | ×0.517480 |
| `S` → Wischmeier & Smith 1978 (eq. 18) | **×1.694054** |
| **the JOINT of the three, measured by engine re-run** | **×0.431944** |
| the product of the three single-lever factors | 0.362435 × 0.522043 × 1.694054 = **0.3205262902296241** |
| **joint / product** | **×1.347608646050708 (×1.34762)** |

> **STANDING INSTRUCTION, restated at the site it was violated: a product of single-lever factors
> may NEVER be quoted as the joint factor.** The joint is **×0.431944**, measured. **×0.3205 is
> not the joint and is not an approximation to it** — it is 34.76 % low, and the only legitimate use
> of it is to report the non-multiplicativity itself, as `joint / product = ×1.34762`.
> *(The same product computed with the **cap** instead of the step is **0.3177246791318452**, a
> different number; it does **not** pair with the registered ×1.34762, which is the eq.-14 step's.)*

**(c) There are FOUR levers, not three.** §1.4's *"Its three levers"* is superseded: the **`L`
form** is the fourth, and it is worth the **whole 0.5410027585442313 ln** span between ×0.43194 and
×0.25146 (`docs/46` §4.2 item 5 as amended (d), §2.5.2). **§1.4's structural conclusion is
unchanged and strengthened** — the levers act per cell as a function of slope, only the joint
*level* joins Π, and G4.1 can detect the residual shape but never fix it.

---

### Amendment 3 — 2026-08-12 — **the superseded LS bracket: 2.37×–3.00× → 2.3151×–3.9768×, and the source read whole is a POINT**

**Source:** `docs/46` §1.0 and §2.5.1 (which names *"`docs/43` §1.4 and §3.x"* in its register) and
§7.3 item 3, both **UNCONDITIONAL**; measured in `docs/47` §4.3 by engine re-run and cross-checked
in `docs/51` §2.1–§2.2. **Sites:** §1.1 clause 2 (struck in place), §2.1's LS-shape row (struck in
place).

> ## REGISTERED HERE, replacing every *"2.37× – 3.00×"* in this document
> **`f_LS` ∈ [0.25146, 0.43194] erosion-weighted ⇒ `1/f_LS` ∈ [2.3151, 3.9768]** — our LS is
> **2.3151× – 3.9768×** the level α = 11.8 is paired with. Area-weighted **proxy**
> ~~[0.24468, 0.42148]~~ → **[0.2446790094097074, 0.42136300143291305]** (**amendment 8**,
> 2026-08-12 — the upper end had been quoted on the *engine URH-fraction* area support, not
> `docs/46` §3.3's per-cell basin one; owning records `docs/46` §10 amd 2 / `docs/51` §9 amd 1),
> measured **2.51 % low** and never overriding (`docs/46` §3.3).
> Basin gross erosion at the endpoints: **129.3840** and **75.3235 Mt/yr**, against the adopted
> **299.5387088405831**.

**And the shape of that interval is not an uncertainty.** `docs/46` §1.0, §2.5.2 and `docs/51` §2.3
record, with all four levers **CITED** and Buarque eq. 13 read verbatim on p. 47:

- **the source formulation READ WHOLE is a POINT at `f_LS` = ×0.25146** (`1/f_LS` = **3.9768×**;
  exact **3.976775630318937**), which `docs/37` §A3 (2026-08-12) has since **ADOPTED** as
  `ls_formulation = buarque_2015_dg` — *determined and recorded, not yet exercisable*;
- **×0.43194 is a documented HYBRID** — the source's three levers with **OUR** `L` — retained only
  because `docs/35` §9.3.1, `docs/37` §4 candidate 0 and **this document's §1.4** quote it and it
  must stay reproducible;
- **the span between them is the `L`-form lever, exactly**, not an interval of admissible readings:
  `ln(0.43194/0.25146)` = **0.5410027585442313**.

**Everything this document derived from the old bracket goes with it**, and none of it is restated
here as a number: the α reference, band and hard stop rescalings are `docs/37` §A3.2's and
`docs/35` §9's to publish, not §7's. **This document quotes no rescaled α anywhere**, and this
amendment introduces none.

> **Defect found and NOT fixed, because the file is not this pass's** (reported per the standing
> rule): `docs/46`:127 (§1.0) and `docs/51` §2.3 both print
> `ln(0.43194/0.25146) = 0.5410 = −ln 0.580685`. Measured: `−ln(0.580685)` =
> **0.543546837831505** against `ln(0.43194/0.25146)` = **0.5410027585442313** — a gap of
> **0.0025440792872737** ln; `exp(−0.5410027585442313)` = **0.5821641894707599**, so 0.5410 pairs
> with **0.58216**, not 0.580685. **Both constituents are separately correct; the identity as
> written does not hold.** Immaterial to every verdict, and owed to those documents' owners.

---

### Amendment 4 — 2026-08-12 — **the remaining σ_r-derived numbers in §1.5 and §3.2**

**Source:** `docs/47` §2.2 (**D2**), §2.6 item 2, §6.2 item 4; `docs/48` §4; `docs/42` §9.7
(**A-P4**), which enacts the same corrections in the document that registered them. **Sites:** §1.5
(struck in place), §3.2's `k` row and class-C row (struck in place).

| # | §3.2 / §1.5 as published | corrected |
|---|---|---|
| 1 | all-18 **G1.2** `k_min` **0.00216 /km ⇒ 2.12×** over 348.4 km | **0.0066 – 0.0069 /km** (construction span 0.00657 – 0.00694; central **0.00686**, the registered joint form) **⇒ ≈ 9× – 11×, central ≈ 10× over ~342 km**. Reproduced: `exp(0.00686 × 341.5)` = **10.409** |
| 2 | CAL-8 `k_min` **0.0209 /km ⇒ 3.54×** over 60.4 km | **0.0838 /km ⇒ ≈ 173×** over 61.5 km (0.0883 ⇒ 164× on `docs/42` §4.1's printed `Lw`) |
| 3 | CAL 8 + ARRANCAPLUMAS **0.00303 /km ⇒ 2.87×** | **0.01210 /km ⇒ ≈ 62.3×** over 341.5 km |
| 4 | the **factor 6.9** between rows 2 and 3 (§3.1 P2) | **SURVIVES UNCHANGED.** It is a ratio of two σ-scaled numbers: 0.0838/0.01210 = **6.926**. **Do not "correct" it** |
| 5 | *"the fitted-set `k_min` is 0.0209 /km, not **0.0096** /km"* (§3.1 P1) | see **amendment 6** — the number is right, the attribution is wrong |
| 6 | minimum detectable class-C error **≈ 4.2×** (CAL 8) / **≈ 2.9×** (all 18) — §3.2 **and** §1.5 | **NO CORRECTED VALUE. `docs/47` open item O8, and it stays open.** Three passes, three answers: registered ×4.2/×2.9; `journal_refute-gate-logic` ×8.2/×3.2; `docs/48` §6.2 ×5.58/×3.53 at the registered σ and ×251.6/×57.9 at the measured σ on its own stated design matrix. **Only the qualitative statement is quotable: the figures are σ_r-scaled and too optimistic by roughly the σ_r factor, so G3.1 is BLINDER than printed** — which makes §1.5's clause-3 conclusion **stronger**, not weaker |
| 7 | *"no first-order channel sink **stronger** than X× over Y km is **detectable**"* (§3.3 item 3, §3.2's `k` row) | **the comparative is inverted.** `k_min` is a **detection floor**: a sink with `\|k\| < k_min` leaves no visible trace, so with the verb **detectable** the true comparative is **weaker**. With the verb *excluded* (*"no sink stronger than X× is consistent with these residuals"*) the original is correct. **`docs/42` §9.7 registers the `weaker`/`detectable` pairing**; §3.3 item 3's sentence form is corrected to it, and the identical repair in `docs/45` §2.3 is owed to that document |

**§3.2's structural verdicts are unchanged by all of this**, and that is the point: `k` remains
**NOT identifiable** and reportable only as a **BOUND** — the corrected numbers make that
conclusion **stronger by ≈ 4×** — a class C value remains reportable only as a coarse contrast, α
remains **not identifiable at all**, and Π remains identifiable **as a level only**. **No row of
§3.2 changes its "identifiable?" column.** Nothing that failed passes because of this amendment.

---

### Amendment 5 — 2026-08-12 — **§3.4's "These overlap" mixes two `cp_revision`s; at the adopted C the bands are DISJOINT**

**Source:** `docs/47` §2.5 **C1** (graded *medium*, *"to be applied before C5 quotes it"*).
**Site:** §3.4 bullet 2 (struck in place). **Measured by this pass, not transcribed.**

`6.83 – 8.73` is `11.8 × {144, 184} / 248.730` — the **prior** `cp_revision`'s basin total. The
reading-B band `7.92 – 8.86` is at the **adopted** C. Recomputed at the adopted C
(**299.5387088405831 Mt/yr**):

| band | at the prior C (248.730) | **at the adopted C (299.5387088405831)** |
|---|---:|---:|
| deposition-free fit, `11.8 × 144 / total` | 6.8315 | **5.6727** |
| deposition-free fit, `11.8 × 184 / total` | 8.7291 | **7.2485** |
| reading-B band (unchanged, already at the adopted C) | — | **7.92 – 8.86** |

**Gap between 7.2485 and 7.92 = 0.6715 in α. The two bands are DISJOINT.** The struck reasoning —
*"these overlap … a fit that works under the flattering reading is nearly indistinguishable from
one that has silently deleted channel deposition"* — **is wrong**, and it is wrong for the reason
`docs/37` states as a house rule: **never quote a load without its convention AND its
`cp_revision`.**

**What survives, and it must not be over-read in either direction.** The **caution** §3.4 draws is
retained, on different grounds: G5's **named claim** still carries the weight rather than `k̂`,
because amendment 4 measures `k̂`'s bound as **≈ 4× weaker than registered** (≈ 10× over ~342 km).
The **corrected** arithmetic says the two cases *are* distinguishable in α, which points the other
way. **Whether that changes §3.4's "doubly load-bearing" conclusion about G5 is `docs/47` open item
O12 and is NOT decided here** — deciding it needs a judgement about reading B that this pass has no
standing to make, and the safe-direction caution is retained regardless. **The same 6.83 – 8.73
figure is propagated into `docs/42`:15, :299, :472 and `docs/45`:404**; those are recorded as owed —
`docs/42` §9.7 flag **F7** carries it for `docs/42`, and `docs/45`'s copy is owed to its owner.

---

### Amendment 6 — 2026-08-12 — **§3.1 P1's `0.0096 /km` is mis-attributed (the `docs/42` §9.6 F2 correction)**

**Source:** `docs/42` §9.6 flag **F2**, and §9.5 (A-P1.1) which resolved the discrepancy by
recomputation. **Site:** §3.1 P1 (struck in place).

P1 instructs *"the fitted-set `k_min` is 0.0209 /km, **not 0.0096 /km**"*, presenting 0.0096 as what
`docs/42` printed. **`docs/42` §4.2 printed 0.0104.** `docs/42` §9.5 recomputed the CAL-13 cell from
that document's own formula, σ_r and `Lw` table and landed on **0.00964 /km**, failed five separate
attempts to reproduce 0.0104, and showed decisively that **P1's own downstream arithmetic runs on
0.00964** (0.020916/0.009640 = 2.170 → P1's *"factor 2.2"*; 0.020916/0.002158 = 9.693 → P1's
*"9.7×"*; at 0.0104 the first factor would be 2.011, which is not what P1 prints).

> **Read P1 as: *"… is 0.0209 /km, not 0.00964 /km (`docs/42` §4.2 mis-printed this cell as 0.0104;
> corrected by recomputation in its §9.5)."*** P1's **number** is right; only its **attribution**
> was wrong. `docs/47` open item **O7** is thereby **CLOSED**, and
> `docs/agents/journal_adj-c4-feasibility.md:167`'s explanation of the 7 % gap as *"method
> rounding"* is **WITHDRAWN** (`docs/42` §9.5).

**Both figures are at the registered σ_r.** The CAL-13 row cannot be σ-corrected at all — a CAL-13
residual set does not exist, because only 8 of the 13 have a single paired CAL-window day, which is
what P1 itself established. **Two corrections are stacked here and must never be conflated:**
0.0104 → 0.00964 is *arithmetic at the registered σ*; the σ correction of amendment 4 applies to the
CAL-8 and all-18 rows and **not** to this one.

---

### Amendment 7 — 2026-08-12 — **§5.1's registered C5 statement carries a MANDATORY comparison-basis rider**

**Source:** `docs/47` §2.5 **C2** (graded *medium*, *"to be applied before C5 quotes it"*).
**Site:** §5.1, immediately after the registered blockquote (rider added in place; **the registered
statement itself is not altered, not struck and not rewritten**).

**The defect is real and it is documentary, not statistical:** §5.1's registered statement compares
a **basin-total simulated** ENSO contrast against a **fleet median of tributary-station observed**
contrasts on a **different day set** — the three-way comparison-basis mismatch that **§5.3 of this
same document** measures at **×2.14** (est a) / **×1.27** (est b), of which the day set alone is
×1.69, and that §5.3's own registered statement 4 forbids (*"score any comparison day-matched and
station-matched, or say in the same sentence that it is not"*). §5.1's following paragraph already
says the two must be reported together — **but registered statements are quoted verbatim by
design**, and this one could be used to reject a legitimate C4 result.

> **ENACTED: the rider is now attached at the site, and the registered statement of §5.1 may not be
> quoted without it in the same paragraph.** What is enacted is the **scoping** requirement, whose
> whole evidentiary basis is already inside this document (§5.3).

**What is NOT enacted, and why.** `docs/47` §2.5 C2 reports that, repaired to like-for-like, the
**simulated** median contrast is **4.903** against observed **4.620** (obs/sim **0.9423**), i.e. the
simulated contrast *exceeds* the observed in the only admissible frame. **This pass did not measure
those numbers and does not adopt them.** They are recorded as **carried from `docs/47`** and
**owed** — the like-for-like repair of §5.1 needs the day-matched, station-matched recomputation,
which is a measurement, not a paragraph. **Per the standing rule, a correction that cannot be
verified is not applied**, so §5.1's registered statement keeps its numbers and gains only the
rider. **Named as an open item below.**

---

### Amendment 8 — 2026-08-12 — **amendment 3's area-weighted proxy upper end was on the wrong support: ×0.42148 → 0.42136300143291305**

**Written by the `defect-45-residual` session** (process record
`docs/agents/journal_defect-45-residual.md`), which owns `docs/37`, this file and its own journal
and nothing else. **Owning records for the fact:** `docs/46` **§10 amendment 2** and `docs/51` **§9
amendment 1**, both 2026-08-12. **Site:** amendment 3's registered blockquote (:586, struck in
place). **Enacted in parallel at `docs/37` A3.3.4 by the same session, which owns that file too.**

**No number this document registers, bounds or decides moves.** The corrected quantity is the
**PROXY**, and `docs/46` §3.3 ground **G-ii** registers that *"`f_ero` decides; `f_area` is reported
beside it, always, and can never override it."* `f_ero` is untouched, so amendment 3's
`f_LS ∈ [0.25146, 0.43194]`, `1/f_LS ∈ [2.3151, 3.9768]`, the POINT at ×0.25146 / 3.976775630318937×,
the ln span 0.5410027585442313, the loads 129.3840 / 75.3235 Mt/yr and the 299.5387088405831 Mt/yr
base **all stand exactly as registered**. §3.2's Π bound, §2's decision, §5's C5 caveats and every
guard reference are untouched. **No materiality bar is invoked, created, rescaled or implied**
(`docs/52` struck the only one this project had and replaced it with **no number**).

**Recomputed, not adopted.** This session did not take either circulating value on trust. Both were
recomputed read-only from `data/processed/urh_ls2d_variants.csv`, `urh_fractions.csv`,
`minibacias.csv` and the three LS JSON artifacts, all SHA-256'd unchanged after.

**The definition selects the support.** `docs/46` §3.3 (frozen): *"`f_area(V)` = basin **area-weighted
mean** of LS(V) / basin area-weighted mean of LS(V0)"*, and `docs/46` §1 fixes "basin" as the pass
*"on all **30,235,916** basin cells at 90 m … reproduc[ing] our own `ls2d_hs` area-weighted mean
**39.812** bitwise"* — 256,702.3554292511 km². Hence **16.775413430326214 / 39.812260149274394 =
0.42136300143291305**, `1/f_area` = **2.3732506095678505**.

**The discriminator, with the arithmetic shown** — `docs/47` §3.1 **R7**'s separately measured proxy
bias **1.0251**, against `f_ero(V4)` = **0.43194417543884817**:

| support | `f_area(V4)` | `f_ero/f_area` | \|d\| vs 1.0251 | inside R7's own 4-d.p. interval [1.02505, 1.02515]? |
|---|---:|---:|---:|---|
| **per-cell basin, 30,235,916 cells — §3.3's quantity** | **0.42136300143291305** | **1.025111777659529** | **1.1777659529199624e-05** | **YES** |
| `ls2d_defect_b.json:decomposition.V4_over_V0` (independent script, same support) | 0.42136300143291344 | 1.0251117777 | 1.178e-05 | YES |
| three-elevation-strata recomposition (same support) | 0.4213630014329133 | 1.0251117777 | 1.178e-05 | YES |
| `urh_ls2d_variants.csv` × `n_cells` | 0.42136472954221804 | 1.0251075735 | 7.573e-06 | YES |
| `urh_ls2d_variants.csv` × `area_km2` | 0.4213519856784954 | 1.0251385780 | 3.858e-05 | YES |
| `urh_ls2d_variants.csv` × `area_frac` | 0.42161856467208547 | 1.0244904082 | 6.096e-04 | **NO** |
| **engine `urh_fractions.csv`×`minibacias.csv` areas, 32,782 units, 257,096.93 km²** — *what :586 printed* | **0.4214751420286394** | **1.0248390293193077** | **2.609706806921963e-04** | **NO** |

**R7 confirms the corrected value 22.158110450144004× more closely, and the only *area* support it
excludes is the one :586 printed.** R7 is a genuine discriminator here, and its limits are stated
rather than glossed: printed to four decimals, it **cannot** separate the three near-identical
reconstructions of the per-cell support and the two URH-table area weightings (all agree with it to
≤ 3.9e-05), but it **rejects the engine support outright**, at 5.2× the half-width of its own
rounding. *(It also rejects the `area_frac` weighting, which is not an area weight at all — the
column sums to 8,672, weighting every minibacia equally regardless of size, and is listed only so
the search is auditable.)* **So R7 does not by itself pick 0.42136300143291305 out of its three
near-neighbours; `docs/46` §3.3's definition does that, and R7 independently rules out the value
that was printed.** Read as a *report*, per ground **G-iv** — an exact ratio at full precision with
a stated licence, **never compared to a threshold**.

**0.42148 is not an arithmetic error.** It is the engine's own URH-fraction area support
(`ls_defect_a.json:…f_area_urhfrac_areas`), rebuilt independently here from `urh_fractions.csv` ×
`minibacias.csv` and reproduced to all 16 digits with the same 257,096.93 km² basin total, against
the DEM pass's 256,702.36 km². `load_geometry` warns its two candidate area sources *"differ by more
than 5 % on 12.9 % of cells."* **A correct quantity on a different support, correctly named in its
own JSON key — just not §3.3's `f_area`.** No artifact was edited; none needs editing.

**The lower end needed no correction** — `f_area(V4_dg)` = **0.2446790094097074** is already the
registered support; control recomputed here: `0.2514648985839397 / 0.2446790094097074` =
**1.0277338427624152** against R7's DG figure 1.0278, |d| = **6.615723758485181e-05**. **Only the
upper end was off, and the bracket's two ends had been printed on two different supports.**

**Also checked in this document and found already correct, so nothing was over-corrected:** §1.4's
and amendment 2's factors are area- or erosion-weighted **single-lever** values from `docs/49`
(×0.505092 / ×0.502472 / ×0.522043 / ×0.517480 / ×0.362435 / ×1.694054), none of which reads
`f_area(V4)`; amendment 2's joint ×0.431944 and joint/product ×1.347608646050708 are
erosion-weighted; amendment 3's *"2.51 % low"* is R7's own shorthand for ×1.0251 and remains right
at ×1.025112. **This document quotes no rescaled α, and this amendment introduces none.**

**Disclosure.** Files written by this session: `docs/37_c3_closure.md` (A3.3.4 plus two in-place
strike-throughs), this amendment plus the :586 strike-through, and
`docs/agents/journal_defect-45-residual.md`. **Nothing else.** `docs/30`, `docs/33`, `docs/35`,
`docs/42`, `docs/45`, `docs/46`, `docs/47`, `docs/49`, `docs/50`, `docs/51`, `docs/52`, `docs/53`,
both notebooks, both nbgen generators, `src/mgb_sediment.py` and `scripts/c3/` were **read and not
edited**. Nothing in §1–§6 was deleted, renumbered or rewritten; the superseded string stays
readable inside `~~…~~`. No engine default was changed (`ls2d_column`, `urh_ls2d`, `cp_revision`,
`volume_convention`, `k_unit_system`, α, β, every H2E parameter); no data product was regenerated or
hand-edited; no fit, search, calibration or simulation was run; no α̂ exists; no git command was run.
The `docs/23` §13.2 yield embargo is in force — no t/km²/yr appears here.

**Residuals this amendment reports and does NOT fix**, added to §7.1 below: `docs/47` §4.3's area
column (a **third** support, 0.42135); `docs/52` §6:371 and `docs/35` §9:850,:1021's ×1.02484;
`src/mgb_sediment.py`:223's docstring bracket; `src/nbgen/make_nb18.py` / `make_nb19.py` and the two
notebooks they generate; and `scripts/c3/ls_erosion_weights.py`:174's untagged `f_area` header.

---

### §7.1 — Open items this slot leaves open, named

| # | open item | what would settle it |
|---|---|---|
| **O8** (`docs/47`) | **the class-C detectability figures ×4.2 / ×2.9** are σ_r-scaled and wrong, and **three passes have produced three different corrected values**. Amendment 4 row 6 offers **no fourth number**. | One recomputation with its design matrix, station set, σ and df printed together, checked against `docs/48` §6.2's matrix. Until then only the qualitative statement is quotable. |
| **O12** (`docs/47`) | whether amendment 5's now-**disjoint** α bands change §3.4's *"doubly load-bearing"* conclusion about G5. | A judgement about reading B, with the corrected `k̂` bound (≈ 10× over ~342 km) in the same table. Not this pass's to make. |
| **C2's repair** (`docs/47` §2.5) | the **like-for-like** simulated-vs-observed contrast behind amendment 7 (`docs/47` reports 4.903 vs 4.620, obs/sim 0.9423) is **unverified here**. | A day-matched, station-matched recomputation on the registered estimator, before C5 quotes §5.1. |
| **P1** (`docs/48` §6.1) | **which estimator's band is binding** — `docs/42` §9 registers **(b)** as primary, `docs/45` §7.1 registers the objective on **(a)**; their bootstrap widths differ by ×1.51 in log units. Amendment 1 adopts the **union** as a reporting convention and explicitly declines the registration question. | A decision in the `docs/45` §8 amendment. |
| **P5** (`docs/48` §6.1) | the band is **β-dependent** (CAL-8 est (b) sd 1.875 → 2.100 across the registered β box). | Nothing — this is why amendment 1 registers a **procedure**; C4 recomputes on its adopted fit. |
| **the `docs/45` §8 half of B5** | at this pass's read `docs/45` §8 was **empty**. `docs/45` §2.2/§3.1/§5.3/§6.2 item 2/§7.1, its G12 row and its §2.3 `k` wording all still carry the retired numbers. | The `docs/45` §8 amendment, by its owner. Amendment 1 states the precedence rule if the two disagree, and states that **a struck band does not revert to ±38 % by default**. |
| **§4's consequential-documents table** | it lists `docs/42` §9's P1/P2/P3 transcription as *"OWED — blocking"*; that is now **DONE** (`docs/42` §9.1–§9.5, 2026-08-11), and `docs/42` §9.7 (2026-08-12) discharges B5's `docs/42` half. **§4 is not amended here** — no number in it is wrong, only a status is stale. | A one-line status refresh whenever §4 is next touched. |
| **the `docs/46`:127 / `docs/51` §2.3 identity** | `0.5410 = −ln 0.580685` **does not hold** (measured gap 0.0025440792872737 ln; 0.5410 pairs with 0.58216). Reported in amendment 3, **not fixed** — those files are not this pass's. | A dated correction by each document's owner. **SETTLED 2026-08-12 by `docs/46` §10 amendment 2 (iii) and `docs/51` §9 amendment 2**: both constituents are true, the identity **mixed the erosion and area supports** — erosion-weighted `0.5410027585442313 = −ln 0.5821641894707599`, area-weighted `0.5435475125003637 = −ln 0.580684608230046`. |
| **`f_area(V4)`'s remaining stale prints, repo-wide** *(added 2026-08-12, amendment 8)* | **RESIDUAL, not this session's to fix.** `docs/47` §4.3's area column prints **0.42135** — a **third** support (`urh_ls2d_variants.csv` `area_km2` weighting, 0.4213519856784954), and its DG cell prints 0.24466 where the registered value is 0.2446790094097074. `docs/52` §6:371 and `docs/35` §9:850,:1021 print **×1.02484**. `src/mgb_sediment.py`:223's docstring prints the bracket `[0.24468, 0.42148]`. `src/nbgen/make_nb18.py`:1244,1269,1353 and `make_nb19.py`:2435 print **0.421475**, and `notebooks/18`,`notebooks/19` carry it in generated markdown, code and executed output. | A dated correction by each owner: `docs/47`'s owner; `docs/52`'s owner; `docs/35` §9's amendment slot (§9.4 is already open); the notebook/verification track for both generators, followed by a regeneration and re-execution so the notebooks stop printing it. **`docs/46` §1–§9 and `docs/51` §1–§8 stay struck-and-pointered only** — their amendment slots are the sole remedy and both have already been used. |
| **`scripts/c3/ls_erosion_weights.py`:174's untagged `f_area` header** *(added 2026-08-12, amendment 8)* | the GATE-2 console table prints a bare `f_area` beside `f_ero` with **no support tag**, while the value it prints is `geom.cell_area_km2`-weighted (the engine URH-fraction support). That console line is the plausible channel by which 0.42147514 entered the corpus as *"`f_area(V4)`"*. **Reported, not fixed** — `scripts/c3/` is not this session's. | One word in a header string (`f_area_urhfrac`), or printing `docs/46` §3.3's per-cell value alongside. Owed to `scripts/c3/`'s owner. |

### §7.2 — Disclosure for this slot

- **Files written by the `amend-4243-piband` pass:** `docs/43_c3_c4_gate.md` (this §7 and the
  in-place strike-throughs and pointers named in each amendment), `docs/42_c4_guards.md` (its new
  §9.7, **A-P4**), and `docs/agents/journal_amend-4243-piband.md`. **Nothing else.** `docs/35`,
  `docs/37`, `docs/45`, `docs/46`, `docs/47`, `docs/48`, `docs/51`, `docs/52` and `docs/53` were
  **read and not edited**.
- **Nothing in §1–§6 was deleted, renumbered or rewritten.** Every superseded string is preserved
  inside a `~~strike-through~~` with a dated pointer, and every original sentence remains readable.
  **No registered statement was altered** — §5.1's gained a rider beside it; §5.2's, §5.3's and
  §3.2's registered forms are unchanged in substance.
- **No threshold anywhere was changed**, no station set moved, no parameter count moved, **no
  materiality bar was created, restated, rescaled or implied** (`docs/52`: the only one this
  project had is **STRUCK** and replaced by **no number**), and **no rescaled α is quoted here, in
  any form, provisional or not**.
- **No engine default was changed** (`ls2d_column`, `cp_revision`, `volume_convention`,
  `k_unit_system`, every H2E parameter, α, β — all untouched); **no frozen artifact was opened for
  writing**; **no calibration, fit, search or simulation was run**; **no `KGE_ln` was evaluated
  against the `docs/45` §2.1 α box**; **no α̂ was quoted**. No git command was run. Nothing is
  backdated.
- **Measured by this pass**, in a scratchpad script that wrote nothing into the repository: the SE
  and band arithmetic of amendment 1 including the reciprocal-orientation check, the jackknife /
  LOO identities, every survival contrast in amendment 4, the 6.926 ratio, the lever product and
  `joint/product` = 1.347608646050708 of amendment 2, the bracket and its `ln` width in amendment
  3, and amendment 5's α endpoints at both `cp_revision`s. Everything else is carried from
  `docs/46`, `docs/47`, `docs/48`, `docs/51`, `docs/52` or `docs/42` §9.5, cited in place.
- **Uncited quantities are named and pass or fail nothing:** the 0.05 – 0.30 SDR band and its
  implied `k ≈ 0.0020 – 0.0032 /km` (§3.2, unchanged — and at the corrected all-18 `k_min` the
  18-station test now sits **above** that whole range instead of inside it, which decides nothing
  either way, `docs/42` §9.7 row 18); and the ENSO-neutrality of CAL 2012–14.
- **The `docs/23` §13.2 yield embargo is in force.** No t/km²/yr appears in this slot.
