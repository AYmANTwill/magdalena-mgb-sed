# 47 — The C4.3 entry verdict: **BLOCKED UNTIL LS LANDS**

**Written 2026-08-11** by the `c3gate-synthesis` agent (process record:
`docs/agents/journal_c3gate-synthesis.md`). This document **decides one question**: may stage
**C4.3 — the sediment calibration search** — start, and under what contract. It synthesises eight
adversarial lenses plus a three-agent LS track, and it adds one measurement of its own (§5.2).
It does not edit `docs/35`, `docs/37`, `docs/42`, `docs/43` or `docs/45`, all of which are frozen
or closed to this pass.

---

> ## THE VERDICT
>
> **`C4.3-BLOCKED-UNTIL-LS-LANDS`.**
>
> **C4.3 may not start.** The blocking reason is not a doubt and not a preference; it is an
> arithmetic incompatibility that was measured this run. `docs/45` §2.1 registers the search as a
> box on **α ∈ [2.0, 30.0]**, and `docs/35` §6.1 registers a hard stop at **α̂ < 3.9**. But α is
> only a *handle* on Π (`docs/45` §2.1, `docs/42` §3.1), and its numerical value is proportional
> to `1/f_LS`, where `f_LS` is graded **UNVALIDATED** (`docs/45` §2.3) and is measured to be
> uncertain by a factor of **2.3151 – 3.9768** (§4.3). **A box registered in α is therefore a box
> whose position is unknown to within a factor of four on an unresolved source-reading question.**
> Measured on the registered fit set, the registered window, the registered estimator and the
> registered objective, the level the objective drives toward at the adopted LS is **α ≈ 0.05 –
> 1.29** across the whole G2.3 β gate, so `F_search` and `F_report` are **monotone decreasing
> across the entire registered box** and the search **rails at the box floor α = 2.0** — a
> `docs/45` §6.1 **FAIL — RAILED / HARD STOP**, with `F_report` there measured at **−0.305 …
> −0.350**, also below the bar's lower edge **−0.26**, i.e. **FAIL — NUMERIC** as well. Both
> outcomes are computable in advance and have now been computed. **A pre-registered search whose
> verdict is already known is not a test; it is a re-run of an answer, and it spends a one-shot
> registration to produce it.**
>
> **The condition for unblocking is a single named event: C3.1 lands** — the LS-formulation
> decision of `docs/35` §9.3, executed under the pre-registration drafted as
> `docs/46_ls_preregistration_DRAFT.md`, frozen, with a `ls_formulation` value and an evidence
> grade recorded. When it lands, C4.3 starts under the six-item contract of §6.2 below.
>
> **One bounded exception is granted** (§6.3): the **LS-invariant** preparation — the C4.3
> machinery, the artifact contract, `Δ_shape` (`docs/46` §6.1), the four blocking repairs of §2 —
> may be done now. **No objective evaluation against the α box, and no consumption of the
> registered 5,482-evaluation budget, is authorised by this document.**

**What this verdict is not.** It is not a judgement that C4 is a bad idea, that the model is
wrong, or that the level residual is a defect — `docs/43` §1.3's reclassification of the level to
a calibration target survives every attack mounted at it this run (§3.1). It is a judgement about
**ordering**: the gate C4.3 must pass is denominated in a unit whose scale is the thing C3.1 has
not yet decided.

---

## 1 — How this run was conducted, and what it is allowed to claim

| | |
|---|---|
| Lenses synthesised | 8 (gate-logic, adj-ratio, prereg-integrity, transport-code, nb19-claims, and their refutation counterparts) + 3 LS-track agents (`ls-evidence`, `ls-impact`, `ls-prereg`) |
| Findings that survived adversarial refutation | **3** (§2.1–§2.4), two of them re-measured *and strengthened* by their own refuters |
| Findings refuted | **2** (§3.2) — registered so they are not re-raised |
| Findings never sent to refutation (medium/low) | 5 (§2.5) — carried at their stated grade, **not** promoted |
| New measurement made by this pass | **one** (§5.2): the LS-corrected α optimum. It is exact arithmetic on two prior measurements, not a new simulation. |
| Frozen artifacts touched | **none.** `sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv, q_gauge_H2E.npz}` not opened. No calibration launched, no simulation run, no git command. |

**Evidence grades used below** are `docs/37` A1.6 item 3's ladder: **DERIVED · IDENTIFIED ·
CITED · ASSUMED · UNVALIDATED**, plus `docs/46` §4's addition, **UNRESOLVED** (two admissible
readings survive).

---

## 2 — Confirmed defects

Each is stated with the measurement that confirms it, then classified: **BLOCKING** (must be
fixed before C4.3 runs) or **CARRIED** (a declared limitation that travels with the result).

### 2.1 D1 — the α box is LS-conditional, and at the adopted LS the search rails **BLOCKING**

**Claim.** `docs/43` §2.1 assigns the multiplicative level to Π with "C4, as a fitted Π" as its
owner; `docs/45` §2.3 then fixes `f_LS`, `C`, `P`, `FG`, `f_K` and `f_vol`, leaving α as Π's only
surviving handle. The level the objective is driven toward is an order of magnitude below the
registered box floor, so the search cannot supply the level it was handed.

**Measurement** (refutation agent `refute-gate-logic-alpha`, on the **registered** configuration
— CAL 8, CAL `2012-01-01 … 2014-12-31`, estimator (a), `KGE_ln`, `F_search` = mean /
`F_report` = median; two reproduction gates passed first: basin gross erosion
**299.5387088 Mt/yr** against `docs/37` A1.3.4's **299.5387**, exact to 7 s.f.; CAL-8 paired-day
count **3,266**, exactly `docs/45` §3.6's registered denominator):

| quantity, at β = 0.56 | measured |
|---|---:|
| implied level, geometric mean of station arithmetic ratios | 0.0760 ⇒ **α 0.897** |
| implied level, geometric mean of station **log-mean** ratios (what KGE's `m` zeroes) | 0.1026 ⇒ **α 1.211** |
| unconstrained argmax α, `F_search` | **0.625** |
| unconstrained argmax α, `F_report` | **0.117** |
| `F_report` at α = 2.0 (box floor) | **−0.349** |
| `F_report` at α = 3.9 (the `docs/35` hard stop) | −0.486 |
| `F_report` at α = 11.8 (Williams) | −0.737 |
| `F_report` at α = 30 (box ceiling) | −0.849 |

β sweep, argmax α (`F_search` / `F_report`): 0.40 → 0.171/0.050 · **0.45 → 0.258/0.050** ·
0.56 → 0.625/0.117 · **0.65 → 1.289/0.325** · 0.70 → 1.969/0.629 · 0.75 → 3.062/1.168. Best
attainable in-box `F_report`: **−0.350** (β 0.45), **−0.350** (β 0.56), **−0.305** (β 0.65) —
every one below the bar's lower edge **−0.26**.

**Four attacks on this finding were mounted and all four failed.** (i) *Wrong window* — the
original evidence used four ENSO windows that `docs/45` §3.5 declares strictly out of sample;
re-measured on CAL 2012–14 the answer is the same. (ii) *Wrong estimand* — the objective is KGE
on **log** flux, whose level optimum is a log-mean ratio, not an arithmetic window-mean ratio;
correcting this moves the answer **×1.35**, not the **×10** needed. (iii) *β is free* — β does
move the level enormously (implied α 0.23 – 8.22 across its box), but the direction is unhelpful:
inside the **G2.3 hard gate β ∈ [0.45, 0.65]** the free optimum is α **0.26 – 1.29**, i.e. *below*
the geometric-mean estimate; α only reaches the box floor at β ≥ 0.70, which is itself a
registered hard stop. (iv) *Aggregation* — the one aggregation that would rescue the level,
flux-pooled `Σobs/Σsim` → α 3.3–3.6, is precisely the untransformed weighting `docs/45` §3.1
rejects by name ("would fit the level of BORBUR and CAPITANEJO and nothing else").

**The Π-not-α defence fails quantitatively too.** Crediting C4 with the largest re-partition this
project has measured — the LS level, `docs/37` §4 candidate 0 at its **registered** ×2.37–3.00 —
lifts implied α only to **2.87 – 3.63**: over the box floor, still under the 3.9 hard stop, and
2.87 is inside the 5 %-of-box-edge rail band (α̂ must be ≥ 3.40).

**Two clauses of the original finding are NOT established and are dropped here, not carried:**
(a) *"the gap is dominated by hillslope→station delivery"* — an attribution with no measurement
behind it; nothing separates delivery from the LS level, the C level, the K unit system, the
volume convention, SSC event-undersampling or rating bias, and the per-station implied α spans
**0.10 – 8.37 (84×)**, which is heterogeneity, not one delivery ratio. (b) the ENSO-window
arithmetic-mean ratios as evidence — out-of-sample windows and the wrong statistic; they happened
to land on the right answer.

**Why BLOCKING.** The outcome is `FAIL — RAILED / HARD STOP` **and** `FAIL — NUMERIC`, both
predictable in advance, both now computed. `docs/45` §6.3 says no outcome licenses a widened box;
so running C4.3 today produces a registered failure that cannot be acted on inside its own
registration. **The fix is not to widen the box. The fix is to fix the unit the box is written
in** — see §5.

### 2.2 D2 — the ±38 % Π band and the k power numbers sit on a noise floor 3.9–4.2× too low **BLOCKING (on reporting)**

**Claim.** `docs/42` §4.2 registers **σ_r = 0.465 ln** — derived from disagreement between two
*observed-flux estimators* — and `docs/43` §3.2, `docs/45` §2.2/§5.3/§6.2/§7 then use it as the
**per-station residual sd**, for the SE of the fitted level (`0.465/√8 = 0.1644 ln = ±38 %`) and
for every `k_min`. The actual between-station scatter of the level residual is several times
larger.

**Measurement** (refutation agent `refute-gate-logic`, five attacks, all failed):

| quantity | registered | **measured** |
|---|---:|---:|
| per-station residual sd, CAL 8, registered CAL window, primary estimator (b) | 0.465 ln | **1.9618 ln** (×4.22) |
| SE of the fleet-mean level | 0.1644 ln (±38 %, 0.725×–1.380×) | **0.6936 ln** (95 % factor **3.89×**, 0.257×–3.894×) |
| `k_min`, all-18 G1.2 form (joint regression per `docs/42` G1 note 3) | 0.00216 /km ⇒ 2.12× over 348.4 km | **0.0066 – 0.0069 /km ⇒ ~10× over 342 km** |
| `k_min`, CAL-8 form | 0.0209 /km ⇒ 3.54× | **0.0130 /km** on the CAL window form |

The mechanism is exact, not approximate: `1.96·σ_r/√Σ(Lw−L̄)²` on `docs/42` §4.1's own `Lw` table
reproduces the registered `k_min` to the printed digits (all-18 **0.002157** vs 0.00216; CAL-8
**0.02092** vs 0.0209). Per-station `r = obs/sim` on the CAL window spans **0.0099 – 4.077**, a
factor of **412**; no estimator of a fleet level over 8 such stations carries a ±38 % band.

**It is not removable by anything C4 fits.** Π is a constant (fitting it removes a constant and
cannot change SE(k)); β moves the scatter the **wrong** way across its whole registered box (CAL-8
est (b): 1.875 at β = 0.40 → 2.100 at β = 0.75); and adding G3.1's class shares and G4.1's
`ln LS̄` to the mandatory joint regression **raises** the residual sd (1.420→1.497 all-18 form;
1.712→2.088 CAL 8). Deleting three of the eight CAL stations still leaves sd = **1.83 × σ_r**.
Model up-areas match IDEAM up-areas to 5 significant figures at all 18 stations, so it is not a
station-mapping artifact.

**Scope narrowed — the original finding's word "every" is wrong and is corrected here.** σ_r
propagates into (i) the level SE / ±38 % band and (ii) the `k_min` power numbers, and **nothing
else**. It does **not** affect `SE(β) = 0.0199` (built on σ_day = 0.809, the rating residual) or
the `b_obs` IQR yardstick **0.464** (independently measured). And where 0.465 / 0.658 is used as a
**firing threshold** — G1.1's pair backstop, G8, G11 — the error makes those guards **more**
trigger-happy, i.e. it errs safe. The class-C detectability figures (×4.2 CAL 8, ×2.9 all 18) are
σ_r-scaled too, but did not reproduce on the refuter's design matrix (they obtained ×8.2 / ×3.2),
so **no corrected number is offered for them** — see §7 open item O8.

**Partial defence, on the record.** `docs/42` §4.2 heads the number "**REGISTERED NOISE FLOOR**",
and both `docs/42` G1 and `docs/45` §2.3 attach "at best" to the 2.12×. So the *direction* (not
the size) of the error is disclosed for the `k` bound. **The level band carries no such hedge**:
`docs/45` §6.2 item 2 registers it flatly — *"Every Π and every load is quoted with that band,
never as a point."*

**Why BLOCKING, and the cheapest fix.** `docs/43` §3.2 makes "Π with its band" the one quantity
C4 may report; the band is a headline number and it is ~4× too narrow in log units. `docs/45`
**G12 already contains the check that catches this**: on the measured CAL-window residuals the
leave-one-out range of `ln Π̂` is **0.860 ln** against G12's registered ±0.322 ln band (full width
0.644) — **G12 fires**. The fix is to make G12's LOO-range comparison a **band-replacement rule**
rather than a descriptive note, or to replace the fixed ±38 % with the station-bootstrap band
`docs/45` §4.2 already imports for every other interval. Either is an amendment to `docs/45` §8,
not a new registration.

### 2.3 D3 — the per-node mass audit is blind to NaN and reports PASS on an all-NaN run **BLOCKING (one line)**

**File:** `src/mgb_transport.py:901-903`.

```python
resid = (((prev + inflow) - dep_t) - out_t) - st.store_t
m = float(np.abs(resid).max())
if m > max_resid:          # nan > 0.0 is False in IEEE-754 — never fires
    max_resid = m
```

and `:803`, `"node_partition_exact": float(max_node_residual) == 0.0`.

**Measured, this pass, directly:** `np.abs(np.array([nan, 0.0, 0.0])).max()` → `nan`;
`nan > 0.0` → `False`; `max_resid` stays `0.0`; `node_partition_exact` → `True`. `inf * 0.0` →
`nan` confirmed as the production route. The `transport-code` lens reached the same result through
a full run: a 5-reach network with three headwaters at 1e308 t — an input that passes **both**
declared input screens (all finite, all ≥ 0) — overflows to `inf` at the junction, returns
`outlet_t_day = [nan]`, and reports `max_node_residual_t = 0.0`, `node_partition_exact = True`.
Control: monkeypatching `route_day` to steal 1 t/reach gives `1.0` / `False`, so the audit is live
and this is specifically NaN blindness. `tests/test_transport.py:583` asserts
`led["max_node_residual_t"] == 0.0`, which the NaN run satisfies.

**Why it matters here.** The module docstring (`:159`, `:785`, `:835`) calls this "the strongest
mass statement the module makes", and C4.3 is the first stage that would quote it as proof the
routing did not leak. The global `exact` / `residual_relative` keys **do** flag the same run
(`False` / `nan`), so the failure is recoverable — but only by a reader who ignores the statement
the docstring points them to.

**Fix:** `if not (m <= max_resid): max_resid = m`, or raise on `np.isnan(m)`. **BLOCKING because
it is one line and because C4.3 would publish the false PASS.**

### 2.4 D4 — the `docs/42` §9 transcription is unperformed and C4 has already started **BLOCKING (audit trail)**

`docs/43` §3.1 declares P1/P2/P3 **blocking preconditions on C4's start**, to be transcribed into
`docs/42` §9, dated, "before C4 begins". **Read directly this pass:** `docs/42` §9 still reads
`| Amendments | none |` and `| Registered station sets | CAL 13 … |`, and §4.2's power table still
prints the CAL-13 `k_min` as **0.0104 /km**. Meanwhile `git log` shows `1e0843c` c4.1 (transport),
`865f674` c4.2 (`docs/45`), `02e7e95` nb19 executed, and `608a39e` "tracker: C4 is under way".

`docs/45` §0 discharges the *substance* of P1/P2/P3 in its own frozen sections (§3.4, §2.4, §2.3)
and records that the §9 transcription "remains owed". **The substance is therefore safe; the audit
trail is not.** A reader who opens `docs/42` — the document `docs/37` A1.6 and `docs/45` §1.1 both
say C4 is held to — gets a superseded fit set and a power table that overstates the fit's power on
`k` by ~2× against its own successor, with no amendment note.

**Carried defect inside the defect (low, fix at transcription):** P1 instructs *"the fitted-set
`k_min` is 0.0209 /km, **not 0.0096 /km**"*, but `docs/42` prints **0.0104**; 0.0096 is the lens's
own recomputation. `docs/agents/journal_adj-c4-feasibility.md:167` discloses the 7 % method
difference; `docs/43` and `docs/37` A2.4 both drop the disclosure. Whoever transcribes must pick
one and record why — see §7 open item **O7**.

### 2.5 Findings carried at their stated grade, **not** promoted

These were never sent to adversarial refutation. They are recorded so they are neither lost nor
over-weighted. **None is blocking.**

| # | finding | grade | disposition |
|---|---|---|---|
| **C1** | **`docs/43` §3.4's load-bearing "These overlap" mixes the prior and adopted `C` levels.** 6.83–8.73 is `11.8 × {144,184} / 248.730` (prior C); the reading-B band 7.92–8.86 is at the adopted C. At the adopted C the deposition-free band is `11.8 × {144,184} / 299.5387` = **5.67 – 7.25**, which is **disjoint** from 7.92–8.86 (gap 0.67). | medium | **Correct in place at C5 or at the next `docs/42` amendment.** Propagated verbatim into `docs/42:15, :299, :472` and `docs/45:404`. The resulting caution is in the safe direction, so the conclusion is unaffected; the *reasoning* is wrong and `docs/37`'s own rule is "never quote a load without its convention **and** its `cp_revision`". |
| **C2** | **`docs/43` §5.1's mandatory registered C5 statement embeds the comparison-basis artifact §5.3 of the same document forbids** — a basin-total simulated ratio against a fleet median of tributary-**station** observed ratios, the three-way mismatch measured at ×2.14 (est a) / ×1.27 (b). Repaired to like-for-like the simulated median is **4.903** against observed **4.620** (obs/sim 0.9423) — the simulated contrast *exceeds* the observed in the only admissible frame. | medium | **Carry as a correction to `docs/43` §5.1, to be applied before C5 quotes it.** The qualifier sits after the blockquote, and registered statements are quoted verbatim by design. It could be used to reject a legitimate C4 result. |
| **C3** | **`docs/37` A2's evidentiary base is primary and verifies, but is unreproducible from the repository.** Four citations followed to origin and verbatim-confirmed (`fagundes2018` L3773 / L4907 / L4189; `swat2009` L24759/24765/24804). But none of `fagundes2018.pdf`, `buarque2015.pdf`, `swat2009.pdf`, `parse_appIV.py`, `guard_vs_source.py` is in the repository. And "two independent legs" is **one primary leg plus one self-citation** (leg 2 cites `docs/42` §3.1). | low | **A one-line provenance record is owed** (retrieval source, file hash, page numbers) for the evidence behind C3's central reclassification. `docs/00` §6 already records scratchpad-only analysis code as a known loss mode. |
| **C4** | The **ENSO-neutrality of CAL 2012–14** is **UNCITED** — no ONI table exists in this repository. It is the premise of the fit/evaluation split. | UNCITED | **Already has a registered remedy** (`docs/45` §3.5: record NOAA CPC ONI v5 with retrieval date in `report_C4.json`, or downgrade "out-of-phase" to "out-of-window" everywhere). Carry. |
| **C5** | **`docs/41` remains unaudited** (C3 clause 3), and G3.1's minimum detectable class-C error means **G3.1 could not have seen `docs/41`'s ×1.2043 revision**. | — | Carry. C3 clause 3 stays open however C4 comes out (`docs/45` G3.3, registered in advance). |

### 2.6 What is CARRIED as a declared limitation, in full

Not defects of this run's making, but limitations that must travel with every C4 number:

1. **66.53 % of the model's gross erosion (199.29 of 299.54 Mt/yr) is upstream of no usable SSC
   station**; 801.1 km of channel, including the whole Depresión Momposina, lies below the
   outlet-most SSC station (`docs/42` G9). Passing G1–G12 constrains the model over **33.47 %** of
   its own erosion, and is **not** closure of C3.
2. **`k = 0.0 /km` and the asserted `SDR = 1.0`** (`docs/45` §2.3, G5 option 2). This is a claim,
   not a measurement, and the guard that would betray it now has a corrected power of **~10× over
   342 km**, not 2.12× (§2.2). State the corrected bound.
3. **Station heterogeneity is irreducible at this fleet size** — I² 96 – 99.2 %, τ 2.03 – 3.40×
   per station, 18 of 24 station-cells with CIs excluding 1. Certifying the residual's constancy
   to ±50 % needs n ≈ 19 stations; to ±20 %, n ≈ 94. We have 8 in the fit and 18 in the guards.
4. **The bar is asymmetric.** The mean predictor scores `KGE = 1 − √2 = −0.414`; the bar's lower
   edge **−0.26** sits 0.15 KGE units above no-skill; a median over 8 stations carries very little
   information. **Passing is not evidence of a good model; failing is evidence of a bad one.**
5. **"Above vs below the Momposina" is NOT EVALUABLE** — measured, not assumed: the
   Cauca–Magdalena confluence is minibacia 4430, 146.1 km above the outlet, and the closest SSC
   station is 684.4 km above it. No station pair spans the sink.
6. **The residual's direction is UNKNOWN** (`docs/37` A1.9). *"The model is ~2× under-erosive"* is
   **WITHDRAWN** and may not motivate, justify or excuse anything.
7. **The yield embargo is in force** (`docs/23` §13.2). Absolute flux only.

---

## 3 — The register of refuted claims

This project keeps a standing register of refuted hypotheses on purpose (`docs/18` §6, `docs/22`).
**Do not re-raise any of the following without new evidence.**

### 3.1 Refuted this run

| # | claim | why it fell |
|---|---|---|
| **R1** | *"`FAIL — STRUCTURE` licenses exactly the refit that `docs/45` §2.5 and §6.3 forbid."* | **REFUTED.** The `FAIL — STRUCTURE` row's licence is to report the fit **as a measured negative** and take the failing guard's registered ACTION; §6.1 states in the same row that the fit is **not adopted and C5 does not run on it**, and §6.3 independently forbids a second search, a widened box and an added parameter. No refit is licensed. |
| **R2** | *"The deposition axis is registered so that it cannot block adoption, and `docs/35`'s countervailing rule is not imported."* | **REFUTED.** G1.1 and G1.2 are both in `docs/45` §6.1's ADOPT condition (4); G5 is condition (5) and is an **AUTOMATIC FAIL regardless of what `check_musle_parameters` returns**; and `docs/35` §6 RULE 0 is imported by name in `docs/45` §1 item 3 and §5.2. The deposition axis blocks adoption three separate ways. |
| **R3** | *"The α-level gap is dominated by hillslope→station delivery."* | **NOT ESTABLISHED — dropped from the surviving finding by its own refuter.** No measurement separates delivery from the LS level, the C level, the K unit system, the volume convention, SSC event-undersampling or rating bias; and the per-station implied α spans **0.10 – 8.37 (84×)**, which is heterogeneity, not one delivery ratio. |
| **R4** | *"**Every** guard power number is computed at the wrong noise floor."* (the original scope of D2) | **REFUTED IN SCOPE, confirmed in substance.** `SE(β) = 0.0199` rests on σ_day = 0.809, not σ_r; `b_obs` IQR 0.464 is independently measured; and where σ_r is a *firing threshold* (G1.1, G8, G11) the error errs **safe**. D2 is confined to the level band and the `k_min` power numbers. |
| **R5** | *"The ENSO-window `obs/sim` ratios establish the level gap."* | **REFUTED as evidence** (though the conclusion survives on better evidence). Those four windows are **strictly out of sample** per `docs/45` §3.5, and the arithmetic window-mean ratio is the wrong statistic for a log-space objective. The finding was re-established on the registered CAL window with the registered estimator (§2.1). |
| **R6** | *"docs/37's LS bracket lower endpoint ×0.333 is the source level."* | **REFUTED by two independent agents.** ×0.333 = 0.421 × 0.790, where 0.790 is `journal_c31-ls2d`'s `ls2d_dg96/ls2d` measured on the **uncapped** column and confounded with an S swap (`ls2d_dg96` uses McCool-87 S while the production `ls2d` uses Moore–Burch). Measured **inside** the source formulation the DG/continuous ratio is **0.5807** area-weighted / **0.5822** erosion-weighted. Corrected endpoint: **×0.2447** (area-wtd, `ls-evidence`) / **×0.24466** (area-wtd, `ls-impact`) — two independent reproductions agreeing to 4 s.f. |
| **R7** | *"docs/37 §4 candidate 0's scalar proxy is a conservative approximation of the LS effect."* | **REFUTED, and it errs the other way.** Erosion-weighted / area-weighted = **1.0251** (continuous L) / **1.0278** (DG L): the proxy is **2.51 % low**, i.e. in the model's favour. The precision caveat at `docs/37` line 206 can be struck as **measured**. |
| **R8** | *"The ×1.714 S lever is a correction toward the standard."* | **REFUTED.** W&S-1978's quadratic is the lone outlier and its own authors withdrew it for steep slopes — Renard, Foster, Weesies & Porter (1991) *JSWC* 46(1) p. 32, verbatim: *"Experimental data and field observations, especially on rangeland, do not support the USLE quadratic relationship when extended to steep slopes"*; repeated in Renard et al. (2011) ch. 8 p. 142. The three modern S functions agree within ±10 % on this basin (McCool-87 **×0.908**, Nearing-97 **×1.047**). The real S lever is **−9.2 % … +4.7 %**. |
| **R9** | *"The ×0.502 `m` lever is a correction toward the standard."* | **REFUTED as stated, re-founded at the same magnitude on a better citation.** Our code implements McCool et al. (1989) / AH-703 eqs. [4-2],[4-3] **exactly** — verified against AH-703 Table 4-5's moderate column to ±0.005 at six slopes (0.518/0.614/0.658/0.684/0.698/0.712 vs 0.52/0.61/0.66/0.68/0.70/0.71) — and **AH-703 itself publishes m up to 0.71**. The 0.5 constant is reserved by AH-703 p. 106 for thawing cultivated soils. But AH-703 p. 105-106 makes m a **land-condition** parameter, and its **rangeland / low rill:interrill** column gives **×0.5082** on this basin, essentially identical to the USLE cap's ×0.5051. The lever survives at ×0.51 on a different ground. |

### 3.2 Standing refutations this run does **not** reopen

Restated because they are the claims most likely to be re-raised in a C4 discussion:

- **"The implied SDR 0.579–0.740 is above the plausible 0.05–0.30 band."** **RETIRED**
  (`docs/40`; `docs/37` A1.2). The band is uncited here and measures a different quantity
  (all-source numerator vs our hillslope-only denominator). **A retired gate is neither a pass nor
  a fail.**
- **"The model is under-erosive by 1.59–2.74× / 1.03–2.27×."** **WITHDRAWN as a directed result**
  (`docs/37` A1.9). The arithmetic reproduces; the interpretation does not.
- **`docs/35` §6.1's α band as a sufficient guard.** Falsified against its own source: this
  repository's unmodified `check_musle_parameters` **STOPs 185 of the 426 published, adopted
  (α, β) pairs of the transposed method (43.4 %)**, of which **42.7 points is the dimensionless β
  hard stop**; and 97.7 % land inside "expected" 5.9–23.6 **because the source's own search prior
  [2.0, 25.0] contains it** — the statistic measures the prior, not the physics. Necessary and not
  sufficient at best.
- **The C3 residual's level as a *defect*.** **RECLASSIFIED** to a calibration target with primary
  evidence (`docs/43` §1.3, `docs/37` A2). **This run attacked that reclassification and it
  survived**: the method defines α and β as *coeficientes de ajuste* and fits them, with fitted α
  moving **×7.78** for the same sub-basin depending only on which observed dataset was the target;
  and Π's design matrix is exactly singular (condition number **inf**), so "the level residual"
  *is* Π and Π is what a fit sets. What this run adds is not a reversal — it is that **the
  reclassified level has nowhere legal to go inside the registered box** (§2.1).

---

## 4 — The LS position

### 4.1 What the literature settles

| lever | settled finding | grade |
|---|---|---|
| **A cap on slope length is REQUIRED** | AH-703 ch. 4 p. 104, verbatim: *"Slope length is defined as the horizontal distance from the origin of overland flow to the point where either (1) the slope gradient decreases enough that deposition begins or (2) runoff becomes concentrated in a defined channel."* An uncapped 2-D LS is not "USLE with long slopes"; it is USLE evaluated **outside its own definition**. AH-703's LS tables 4-1…4-4 stop at **1,000 ft (305 m)**; our `A_unit` reaches `1e6/92.2 ≈ 10,846 m = 35,585 ft`, **35.6×** that outer bound, and **59.5 % of cells already exceed 400 ft**. | **CITED** |
| **Our specific cap value 1 km² is a citation defect** | `scripts/c3/ls2d.py:183-185` justifies `A_CHANNEL_M2 = 1e6` as "the upper end of the humid/steep field range in Montgomery & Dietrich (1988, 1992)". Both papers retrieved and read: M&D (1989) *WRR* 25(8) Table 1 measures channel-head source areas **2,700 – 12,000 m²**, and its eq. (10) `A = 1978·tanθ^(−1.65)` gives **≈ 6.6×10³ m²** at our Andean median tanθ 0.483 and **≈ 4.2×10⁴ m²** at the basin median 0.158. M&D (1988) *Nature* 336 adds that **wetter** regions have **smaller** source areas, and our basin is wetter than their wettest site. **Our cap is 150× its own citation at Andean slopes and 24× at the basin median.** This is a defect, not a modelling opinion. | **CITED, contradicted** |
| **The W&S-1978 S function was withdrawn by its own authors for steep slopes** | Renard et al. (1991) p. 32 and (2011) ch. 8 p. 142, both verbatim (§3.1 R8). ×1.714 is **not** a correction. | **CITED** |
| **Our `m` is McCool-89 / AH-703 exactly, and AH-703 publishes m up to 0.71** | Reproduced against AH-703 Table 4-5 to ±0.005 at six slopes. The "0.5 cap" is superseded USLE, reserved by AH-703 p. 106 for thawing cultivated soils. *(Code defect found alongside: the `ls2d.py` docstring claims m "runs … to ~0.5 on steep Andean slopes"; **measured median 0.5844, p90 0.7028, max 0.7501**.)* | **CITED** |
| **The `L` form our production column uses is a point rate, not a cell average** | Derived, not cited: USLE's `A(λ) ∝ (λ/22.13)^m` is a length-**average**, so cumulative loss `T(λ) ∝ λ^(m+1)`; the cell average `[λ_out^(m+1) − λ_in^(m+1)]/(D·22.13^m)` is **exactly D&G eq. 11 = Buarque eq. 13**, while `dT/dλ = (m+1)(λ/22.13)^m` is **exactly our production form**, a *point* rate. Because MUSLE here is applied per pixel and summed, **the cell-average (D&G) form is the coherent one and our point form over-states**. Predicted head-cell ratio ≈ 0.58; **measured 0.5807**. | **DERIVED** |
| **The convergence result** — the strongest single LS finding | Rebuilt on **our** grid, everything else identical: production `ls2d_hs` **39.812** (×1.000) · Buarque / MGB-SED source method (D&G L + step m + W&S S + 1 px) **9.741** (**×0.245**) · RUSLE handbook (D&G L + McCool m + McCool S + AH-703's own 400 ft) **8.187** (**×0.206**) · RUSLE handbook with the rangeland m column **6.421** (×0.161). **Two paths that share no formulation choice except the L form land within 19 % of each other, and both sit ≈ 4–5× below production.** | **DERIVED + CITED** |

Harness validation before any of it: the LS harness reproduces every published lever number on all
**30,235,916** basin cells at 90 m — `ls2d_hs` awm **39.8123** (pub. 39.812) · S→W&S **1.7139**
(1.714) · m→step **0.5051** (0.502) · limiter→1 px **0.3513** (0.351) · joint **16.7754 / ×0.4214**
(16.775 / 0.421); and the per-(mini,URH) aggregation matches committed `urh_ls2d.csv:ls2d_hs` to
max rel diff **4.97e-6**. The engine re-run on the re-derived column returns **299.53867** vs the
adopted **299.538709 Mt/yr** — the adopted gate `|total − 299.5387| < 1e-3` **PASSES**.

### 4.2 What the literature does **not** settle

Stated plainly, with no band invented for any of them.

1. **Which S function is right above tanθ 0.50.** **11.26 % of our cells exceed tanθ 0.50 and they
   carry 35.5 % of the basin's area-weighted S total; 5.71 % exceed 0.60**, AH-703 Table 4-5's
   highest tabulated slope. Schmidt, Tresch & Meusburger (2019) *MethodsX* 6, 219-229: *"all
   S-factors have in common that empirical evidence and thus validity is limited to slope
   gradients less than 50 %"*, and the nine published regressions "differ largely with increasing
   slope steepness". JRC/ESDAC (Panagos et al. 2015) therefore **caps at 50 % (26.6°)**; we do not
   cap at all. **No primary source validates any S function there. No band is offered.**
2. **The exact cap value.** The literature *requires* a cap, *rules out* 1 km², and gives a
   **range** — 400 ft / 1,000 ft / channel-initiation source area — not a number. Renard et al.
   (2011) p. 143 in print: attempts to use GIS with USLE/RUSLE *"simply cut off the slope lengths
   at some **arbitrary** value"*. Defensible span measured: **×0.351** (1 px = 302 ft) · ×0.379
   (A ≤ 1e4 m²) · **×0.401** (400 ft) · ×0.585 (1,000 ft) · ×0.672 (A ≤ 5e4 m²). **×1.000 is not
   defensible.**
3. **Moderate vs low rill:interrill `m` column** — AH-703 leaves it to the user; worth **×0.508**
   either way on this basin.
4. **Desmet & Govers (1996) primary text not obtained** (JSWC, paywalled on every route).
   `ls2d.py`'s claim that McCool-89 `m` is "adopted verbatim as eqs. 5-6 of D&G 1996" is
   **UNVERIFIED**.
5. **Fagundes et al. (2026) NOT RETRIEVED.** doi `10.1016/j.iswcr.2025.11.007` is diamond open
   access but hosted only on ScienceDirect, which 403'd on every route (WebFetch, requests with
   browser headers, doi.org, linkinghub, `/pdfft`, DOAJ, OpenAlex). **No verdict rests on it.**
   What was established first-party instead: the shipping MGB-SED plugin
   (`github.com/LabHig-Ufes/MGB-SED` → `bin/formPRESED.exe`, 2025-09-10) contains the literal
   strings `LS-2D CALCULATION (Desmet and Govers, 1996) CLOSED!!!` and a **run-time user choice**
   of S factor (`(0) standard method / (1) slope scaling method`), plus a source→target DEM
   resolution rescaling our implementation does not have. **So in the tool this project transposes,
   S is a user choice, not a fixed part of the method.**
6. **α = 11.8 (Williams 1975) predates every 2-D contributing-area LS by two decades.** Buarque's
   is the closer comparator and is what `docs/35` §6.1 registers, but **no 2-D LS is strictly
   like-for-like with the LS α = 11.8 was fitted against.** This bounds every ratio in §4.3 from
   above and could not be resolved from the sources obtained.
7. **Buarque's own verdict, carried because it is load-bearing and uncomfortable:** thesis p. 121
   calls Andean erosion *"erosão em massa… **incompatível com o uso da MUSLE**"*.

### 4.3 The measured erosion-weighted bracket

All rows below: 90 m, same grid, same aggregation, engine re-run (**not** a scalar proxy).

| LS field | basin Mt/yr | **erosion-weighted ×** | area-weighted × |
|---|---:|---:|---:|
| adopted `ls2d_hs` | **299.5387** | **1.0000** | 1.0000 |
| + `m` capped at 0.5 | 155.0053 | 0.5175 | 0.5023 |
| + S = W&S 1978 | 507.4346 | 1.6941 | 1.7143 |
| + slope length ≤ 1 pixel | 108.5632 | 0.3624 | 0.3512 |
| **source method, continuous L** | **129.3840** | **0.43194** | 0.42135 |
| **source method, Desmet–Govers L** | **75.3235** | **0.25146** | 0.24466 |

> **REGISTERED HERE AS THE MEASURED BRACKET, superseding `docs/37` §4 candidate 0's
> ×0.333 – ×0.421 as a *measurement* (not as a decision):**
> **`f_LS` ∈ [0.25146, 0.43194] erosion-weighted — our LS is 2.315× – 3.977× the source level.**
> `docs/37`'s ×0.333 endpoint is refuted (§3.1 R6); its scalar proxy is measured **2.51 % low**
> (§3.1 R7). Basin gross erosion at the endpoints: **129.3840 Mt/yr** (503.25 t/km²/yr,
> *model-internal*) and **75.3235 Mt/yr** (292.98, *model-internal*), against the adopted
> **299.5387** (1,165.08). Both endpoints put gross hillslope erosion **below** both all-source
> outlet anchors (144 Mt/yr Restrepo & Kjerfve 2000; 184 Mt/yr Restrepo & Escobar 2018) —
> anchor/model **1.113 / 1.422** (continuous L) and **1.912 / 2.443** (DG L). *(That ratio is an
> ADR, not an SDR, is not bounded by 1, and is **not** a gate — the anchors are all-source and
> net-of-deposition past a gauge 801 km below our outlet-most SSC station.)*

**Caveat travelling with both source-method rows:** they rest on `journal_decide-ls-resolution`
§3b's reading of Buarque (2015) p. 94 (*"seu valor máximo foi limitado ao tamanho do pixel do
MDE"*). That reading is now **corroborated by a second, independent sentence** on p. 98
(*"o maior valor permitido pelo modelo para o fator L é igual ao limite da dimensão de cada
pixel"*), which resolves the interpretation risk `docs/35` §9.3.4 item 4 flagged. But under that
cap `a_in → 0`, so the D&G finite difference degenerates to `L = (D/(22.13·x))^m` and loses its
finite-difference character. **A different reading of p. 94 moves both rows.**

### 4.4 The α-absorption factor

> **`α_corrected = α_fit / f_LS`, exactly.** α and `f_LS` are both pure multiplicative level
> factors entering MUSLE linearly (`docs/42` §3.1: seven ways of writing one Π), and the transport
> step is linear in cell load, so the objective depends only on the **product** `α · f_LS`.
> Verified by control: a uniform scalar moves the basin total by exactly that scalar
> (`|ratio − f| < 1e-12`).
>
> **`1/f_LS` = 2.3151 – 3.9768. An α fitted today at the adopted LS is low by ×2.32 – ×3.98.**

**And it is not resolvable by calibration — ever, by any objective.** Two measurements:

- **Level: exactly confounded.** `ln f = −0.8395 … −1.3805` *is* the α column of the design
  matrix. Not separable, by construction.
- **Shape: 3.1× below detection.** The per-station erosion-weighted LS ratio spans only **1.287×**
  (0.3687 CARRASPOSO → 0.4745 BANANERA); `sd(ln)` **0.0769** (all 18) / **0.0868** (CAL 13), i.e.
  **0.165 / 0.187 × σ_r**. Minimum detectable regression slope at 95 %: **3.108** (all 18) /
  **3.405** (CAL 13) against a true slope of exactly **1.0** if the LS is wrong. **Underpowered by
  3.1×. `docs/42` G4.1 cannot see it.** *(For contrast, the C revision's shape is 3.9× larger —
  `sd(ln)` 0.299, min |b| **0.799 < 1.0** — marginally detectable at 18 stations, not at 13.)*
  The two bracket endpoints correlate **r = 0.998**: the bracket's *width* is a pure level
  uncertainty with **no fingerprint at all**.

**The one number the bracket does not move: the deliverable.** Primary wet:dry flux ratio
**2.2915** (adopted) → 2.2694 (continuous L, **−0.96 %**) → 2.2665 (DG L, **−1.09 %**);
sensitivity pair 3.9725 → 3.9364 → 3.9329 (−0.91 % / −1.00 %). **The level moves 2.3–4.0×; the
ENSO contrast moves ≤ 1.1 %.** Waiting for LS therefore costs C5's headline nothing.

---

## 5 — THE DECISIVE ARGUMENT: is fitting α before LS lands acceptable?

> ## **NO. It is not acceptable, and the reason is arithmetic, not caution.**

Three propositions, each measured, and a conclusion that follows from them without a judgement
call.

### 5.1 P1 — the box is written in a unit whose scale is the open question

`docs/45` §2.1 registers a **search box on α: [2.0, 30.0]**, and `docs/45` §6.1 makes two of the
eight ADOPT conditions — (2) "no free parameter railed" and (3) the `FAIL — RAILED / HARD STOP`
row's `α̂ < 3.9` — read α̂ against fixed numbers. `docs/45` §2.1 also states, correctly, that **α
is only the handle by which the search moves Π** and that "what C4 has determined is Π". Both
cannot be true of a *gate*: **Π is invariant to `f_LS`; α is not.** The registered gate is
therefore denominated in the one quantity in the whole registration whose scale is unresolved,
and `docs/45` §2.3 grades that scale **UNVALIDATED** in its own fixed-factor table.

`docs/46` §6.2 **A3** reaches the same conclusion from the other side and states it as a Branch A
condition: *"the ADOPT outcome of `docs/45` §6.1 is not reachable… α̂ is read against 3.9 / 35.4,
which is an LS-conditional band."* **This document agrees with A3 and goes one step further: if
ADOPT is unreachable, the thing that would run is not C4.3.**

### 5.2 P2 — the LS decision moves α across the gate, and this run measured by how much

This is the one new measurement of this pass. Because the objective depends only on `α · f_LS`
(§4.4), the argmax α scales **exactly** as `1/f_LS`. Applying the measured bracket
`1/f_LS ∈ [2.3151, 3.9768]` to the measured optima on the registered configuration (§2.1):

| quantity, registered CAL window / estimator (a) / `KGE_ln` | at adopted LS | **at the source LS level** |
|---|---:|---:|
| implied level (geometric mean of station log-mean ratios), β = 0.56 | 1.211 | **2.804 – 4.816** |
| argmax α for `F_search`, β = 0.45 (G2.3 floor) | 0.258 | 0.597 – 1.026 |
| argmax α for `F_search`, β = 0.56 | 0.625 | 1.447 – **2.485** |
| argmax α for `F_search`, β = 0.65 (G2.3 ceiling) | 1.289 | 2.984 – **5.126** |
| argmax α for `F_report`, β = 0.56 | 0.117 | 0.271 – 0.465 |

Against the registered thresholds — box floor **2.0**, the 5 %-of-box-range rail band
**α̂ < 3.40**, and the `docs/35` hard stop **α̂ < 3.9**:

- **At the adopted LS the search rails at the box floor in every G2.3-admissible β**, and
  `F_report` at that floor is **−0.305 … −0.350**, below the bar's lower edge −0.26. The outcome
  is `FAIL — RAILED` **and** `FAIL — NUMERIC`. **Certain, and now pre-computed.**
- **At the source LS level, one corner of the registered parameter space clears both thresholds**
  — β at the top of the G2.3 gate combined with the Desmet–Govers endpoint of the LS bracket gives
  **α ≈ 5.13**, above 3.9 and outside the rail band. The geometric-mean implied level, **2.80 –
  4.82**, straddles the 3.9 hard stop.

**Therefore the LS decision is not a downstream refinement of the C4 result. It is the dominant
term in the C4 verdict.** It is worth the difference between *a guaranteed rail* and *a possible
clean fit*, and no other registered quantity in C4.3 has that leverage.

*(Honesty about the limits of this measurement: rescaling the α axis is **exact** for the level
but does not hand me `F_report` values at the new box endpoints, because the LS swap also moves
each station's residual by up to ±1.287× relative to the fleet. So "may clear" is the strongest
statement available; "will clear" is not measured. See §7 open item **O5**.)*

### 5.3 P3 — deciding LS after the fit is the exact post-hoc move this project forbids

If C4.3 runs first, the LS decision that follows is made by a session that **knows which value of
`f_LS` puts α̂ inside its box**. `docs/45` §2.4 rejected admitting ARRANCAPLUMAS on precisely this
ground — *"admitting it would relax a frozen registration in order to gain statistical power,
**after the power had been measured** — the exact post-hoc move this project forbids"* — and the
LS case is worse, because `f_LS` is not a station list but a continuous multiplier that can be
tuned by choosing among four levers, each of which has a defensible citation somewhere in
§4.1–§4.2. `docs/46` §4.3 already lists the basin total and the outlet anchors as **evidence that
may not be used** in the LS decision; the fitted α̂ would have to be added to that list, and the
cleanest way to keep it off the list is not to have measured it yet.

### 5.4 The counter-argument, taken seriously, and why it fails

**The strongest case for going ahead** is `docs/46` §6.2's Branch A: if the LS swap is a pure
**level** change for the fit set, the objective surface is the same surface with a relabelled α
axis, so running now and running later are the same run, and a provisional negative is cheap
information. That argument is sound as far as it goes, and its discriminator — `Δ_shape` — is
correctly derived.

**It fails on three measured points.**

1. **The relabelling is blocked by the box.** The equivalence "same surface, relabelled axis"
   holds for Π and for the objective *value*, but **not for a gate expressed as a hard interval in
   α**. `[2.0, 30.0]` and `α̂ < 3.9` are boundaries in the relabelled coordinate. One labelling
   rails; the other may not. The two runs are therefore **not** the same run *for the purpose the
   run exists to serve*. `docs/46` §6.2 **A6** already forbids rescaling in place of a re-run,
   which concedes the point.
2. **The information Branch A would buy has already been obtained without spending the
   registration.** The refutation pass profiled `F_search` and `F_report` across the whole
   registered box at nine β values on the registered fit set, window, estimator and objective
   (§2.1). The headline outcome of the registered search is therefore **already known**. A 5,482-
   evaluation grid plus 4×1,000 DDS would confirm a rail we can already state. `docs/46` §6.4
   measures the rest of the cost asymmetry: one 90 m LS pass is **≈ 4 minutes**; the eight LS
   variants are **hours, not days**; a C4.3 **re-run** after a later LS adoption costs the full
   5,482 + 4,000 **plus** the re-derivation of every guard statistic on new residuals.
   **LS-first is cheaper on every measured number.**
3. **Branch A's own ceiling makes the product not-C4.3.** A3 caps a provisional fit at
   **ADOPT-PENDING at most**; A1 requires every artifact stamped *PROVISIONAL — LS FORMULATION
   UNRESOLVED*. A run that cannot reach ADOPT, cannot be rescaled, and must be re-run is
   preparation, not the stage. Calling it C4.3 consumes a one-shot pre-registration to produce a
   labelled placeholder.

*(A4 — Branch A's `α̂ ≥ 10.0` stop — is now moot in the direction it was written for: the measured
optimum is at the **bottom** of the box, not the top. The symmetric stop it should have carried is
`α̂ ≤ 2.0 × 1.05`, which the measurement says will fire.)*

### 5.5 One more reason, which arrived from outside the LS question

**The registered objective has already been evaluated.** `docs/45` §7.3 states truthfully of its
own pass that it "does not launch a search, fit anything, or produce a number that any gate here
judges". That is no longer true **of the project**: the `refute-gate-logic-alpha` pass evaluated
`docs/45`'s registered objective, on its registered fit set, in its registered window, with its
registered estimator, across its whole registered α box and nine β values. Nothing was written to
the repository and no frozen artifact was touched — but the surface has been seen.

**Consequence, and it is not optional:** a C4.3 session can no longer claim to be a blind
pre-registered fit. **`docs/45` §8 must carry a dated amendment disclosing the pre-fit profile,
naming `docs/agents/journal_refute-gate-logic-alpha.md`, before C4.3 runs.** This is an argument
for pausing and re-registering the α axis, not for hurrying to run before anyone notices.

---

## 6 — The contract

### 6.1 The four repairs that must land before C4.3 starts

| # | repair | from | cost | why blocking |
|---|---|---|---|---|
| **B1** | **Land C3.1** — the LS-formulation decision, under `docs/46` frozen, with `ls_formulation`, its evidence grade, and the negative-result branch (`docs/46` §7) live. | §5 | ≈ 4 min per LS pass; hours for the full variant set | The α box is denominated in the quantity C3.1 decides (§5.1–§5.2). |
| **B2** | **Re-express the C4.3 gate in Π, or re-register the α box against the adopted `f_LS`.** Whichever C3.1 returns — including *"not resolvable from the available literature"* — `docs/45` §2.1's box and `docs/35` §6.1's 3.9/35.4 must be restated in a unit that survives it. A `docs/35` §9 amendment may only be **proposed** by the session that hits the stop (`docs/45` §6.1), so this is owed to the document owners, not to C4.3. | §5.1 | one amendment | Otherwise C4.3 runs against a floating threshold. |
| **B3** | **Fix `src/mgb_transport.py:902`** (`if not (m <= max_resid)`) and add a NaN regression test; `tests/test_transport.py:583` currently passes on an all-NaN run. | §2.3 | one line + one test | C4.3 would publish the false PASS. |
| **B4** | **Transcribe P1/P2/P3 into `docs/42` §9**, dated, and correct §4.2's CAL-13 power row — resolving the 0.0096-vs-0.0104 discrepancy in writing (§2.4, O7). | §2.4 | one amendment | `docs/43` §3.1 already declares these blocking; they are unperformed. |

**And one repair owed before any C4 number is *printed*, which may be done in parallel:**

| **B5** | **Replace the ±38 % Π band.** Either make `docs/45` **G12**'s LOO-range comparison a band-**replacement** rule, or substitute the station-bootstrap band `docs/45` §4.2 already imports for every other interval. Restate the corrected `k` bound as **~10× over 342 km**, not 2.12×. | §2.2 | a `docs/45` §8 amendment | `docs/45` §6.2 item 2 makes the band mandatory on every Π and every load; it is ~4× too narrow in log units, and G12 already fires on it (0.860 ln vs ±0.322 ln). |

**Plus the disclosure of §5.5**, as a dated `docs/45` §8 amendment.

### 6.2 The contract C4.3 starts under, once B1–B4 land

1. **The gate is read in Π, or in α against a named, dated `f_LS`.** No α̂ is compared to 3.9,
   35.4, or a box edge without `f_LS` and its grade in the same table.
2. **The corrected LS bracket travels with every α̂:** `f_LS ∈ [0.25146, 0.43194]` erosion-weighted
   ⇒ `1/f_LS ∈ [2.3151, 3.9768]`, unless C3.1 collapses it to a point, in which case the adopted
   point and its grade travel instead.
3. **The Π band is the corrected one (B5)**, and the sentence *"the level is set by 8 stations
   whose residuals span a factor of 412"* appears beside it.
4. **The `k` bound is stated at its corrected power** — *"no first-order channel sink stronger
   than ~10× over 342 km is detectable on this fit set"* — together with the asserted `SDR = 1.0`
   claim in the words `docs/45` §2.3 registers.
5. **Everything else in `docs/45` §2–§6 is imported unchanged and obeyed**, including the
   asymmetric-bar statement, G9's 66.53 % disclosure, G6's five reporting elements, G10's
   mandatory "the calibration determined a level and essentially nothing else" statement, the
   five not-claims of §5, and the `docs/23` §13.2 embargo.
6. **The §5.5 disclosure appears in `report_C4.json` and in the C4 document**: the registered
   objective was profiled before the fit, by whom, and where the record is.

### 6.3 What may be done **now**, before B1 lands

**Permitted** (LS-invariant, consumes no registered budget, produces no number any `docs/45` gate
judges):

- **`docs/46` §6.1's `Δ_shape` pre-test.** It is the registered Branch A/B discriminator, it has
  **not been run** (O6), and it costs minutes. Run it and record the number **before** C3.1
  reports, so it cannot be read backwards.
- B3 and B4 in full; B5 and the §5.5 disclosure as amendments.
- Building the C4.3 machinery and the `docs/42` §2 artifact contract — `sed_station_daily.npz`,
  the `c4_grid.csv` writer, the guard evaluators — and testing them on synthetic input.
- The C3.1 / `docs/46` work itself, which is the unblocking event.

**Not permitted:** any evaluation of `KGE_ln` against the α box; any consumption of the registered
5,482-evaluation budget or the four DDS seeds (20260921–24); any α̂ quoted anywhere, provisional
or not; any edit to `docs/35`, `docs/42` §1–§8, or `docs/45` §2–§6.

---

## 7 — What this run could NOT settle

Named as open items, with what would settle each. **None of these is a finding.**

| # | open item | what would settle it |
|---|---|---|
| **O1** | **Whether the LS levers can be settled from the literature at all.** Desmet & Govers (1996) primary text not obtained (paywalled); Fagundes et al. (2026) not retrieved (ScienceDirect 403 on every route). | Obtaining either. `docs/46` §7 already pre-commits *"the LS level is not resolvable from the available literature"* as a publishable **result**, which is the right posture. |
| **O2** | **Which S function is valid above tanθ 0.50** — 11.26 % of cells, **35.5 % of the S signal**. | A primary source that validates any S function above 50 % slope. None exists (Schmidt et al. 2019). **No band invented.** |
| **O3** | **The exact slope-length cap.** The literature requires one, rules out 1 km², and calls the value "arbitrary" in print. Defensible span **×0.351 – ×0.585**. | A written source-grounds choice under `docs/46` §4's decision ladder. |
| **O4** | **Moderate vs low rill:interrill `m` column** (worth ×0.508 either way); and whether `α = 11.8` (Williams 1975) is like-for-like with **any** 2-D contributing-area LS. | AH-703 leaves (a) to the user; (b) bounds every ratio in §4.3 from above and may be unresolvable. |
| **O5** | **Whether `F_report` clears the bar anywhere in the box under a corrected LS.** This run rescaled the α **axis**, which is exact for the level, but did not re-profile the objective on a corrected LS **field**, so the per-station residual redistribution (±1.287×) is unmodelled. | Re-running the §5.2 profile on the adopted LS field — **after** C3.1 lands, never before. |
| **O6** | **`docs/46` §6.1's `Δ_shape` pre-test has not been run.** It is the registered Branch A/B discriminator. | Running it (§6.3). Minutes. |
| **O7** | **The 7 % method difference between the two `k_min` computations** — `docs/42` prints 0.0104 /km, the lens computed 0.0096 /km, and `docs/43` P1 quotes the lens's number as `docs/42`'s. | The B4 transcription must pick one and record why. |
| **O8** | **The class-C detectability figures ×4.2 (CAL 8) / ×2.9 (all 18)** did not reproduce on the refuter's design matrix (obtained ×8.2 / ×3.2). They are σ_r-scaled and therefore also affected by D2. | An independent recomputation with the design matrix stated. |
| **O9** | **Whether the pre-fit profile (§5.5) compromises `docs/45`'s freeze enough to require a fresh pre-registration** rather than a §8 amendment. | A governance decision by the document owner. This pass registers the disclosure requirement and declines to decide the governance question. |
| **O10** | **`docs/41` remains unaudited** (C3 clause 3), and G3.1 is measured blind to its ×1.2043 revision, so C4 cannot audit it however it comes out. | An independent adversarial pass on `docs/41`. Not C4's job. |
| **O11** | **The provenance record for `docs/37` A2's primary evidence** (§2.5 C3) — the PDFs and parse scripts exist only in a session scratchpad. | A one-line retrieval source + hash + page-number record. |
| **O12** | **Whether `docs/43` §3.4's corrected, now-disjoint bands (5.67–7.25 vs 7.92–8.86, §2.5 C1) change the "doubly load-bearing" conclusion about G5.** The corrected reasoning says the two *are* distinguishable. | A correction pass on `docs/43` §3.4 and its three downstream copies. The safe-direction caution should be retained regardless. |

---

## 8 — Disclosure

- **The verdict was reached and recorded before this document was written**:
  `docs/agents/journal_c3gate-synthesis.md`, section "Measurements I made myself", carries the
  §5.2 arithmetic and the `BLOCKED_UNTIL_LS_LANDS` conclusion before either entered a numbered
  document.
- **Files written by this pass:** `docs/47_c4_entry_verdict.md` (this file) and
  `docs/agents/journal_c3gate-synthesis.md`. **Nothing else.** `docs/35`, `docs/37`, `docs/42`,
  `docs/43`, `docs/45` and `docs/46` were read and **not edited**. No git command was run.
- **No frozen artifact was opened or written.** `sim_calibrated_v2/{h2e_drivers.npz,
  parameters_H2E.csv, q_gauge_H2E.npz}` untouched. **No calibration was launched. No simulation
  was run. No headline number was moved. Nothing is backdated.**
- **The only measurement this pass made itself** is §5.2's rescaling (exact arithmetic on two
  prior measurements, stated as such) and §2.3's IEEE-754 demonstration
  (`np.abs([nan,0,0]).max() > 0.0` → `False`). Both are flagged in place. **Everything else is
  carried from a named lens, a refutation verdict, or a prior document, cited in place.**
- **Uncited quantities are named and pass or fail nothing:** the 0.05–0.30 SDR band and its
  implied `k ≈ 0.0020–0.0032 /km`; the ENSO-neutrality of CAL 2012–14; the `m'` KGE bias variant.
  **No plausibility band was invented for any LS lever** — where the literature does not settle a
  lever, §4.2 says so and stops.
- **The `docs/23` §13.2 yield embargo is in force.** Every specific-erosion figure in §4.3 is
  labelled *model-internal*.
- **C3 remains OPEN** (`docs/37` A1, `docs/43` §2) on clauses 2, 3 and 4″. This document closes no
  C3 clause and does not weaken `docs/43`'s reclassification of the level — §3.2 records that the
  reclassification **survived** this run's attack on it.

### 8.1 Cross-references

| document | relation to this one |
|---|---|
| `docs/37_c3_closure.md` | C3's verdict and Amendment A1/A2. §4 candidate 0's ×0.333–×0.421 is **superseded as a measurement** by §4.3; A1.9's withdrawn direction is carried unchanged. |
| `docs/40_sdr_evidence.md` | the SDR retirement; §3.2 restates it so it is not re-raised. |
| `docs/41_cfactor_evidence.md` | the adopted `C` revision; **unaudited**, open item O10. |
| `docs/42_c4_guards.md` | G1–G9. §2.2 corrects its σ_r-derived power numbers; §2.4 records that its §9 transcription is **unperformed**. |
| `docs/43_c3_c4_gate.md` | the gate decision. Its reclassification **survives** (§3.2); §2.1 and §2.2 attach to its §2.1 and §3.2; §2.5 C1/C2 correct its §3.4 and §5.1. |
| `docs/45_c4_preregistration.md` | C4.2, frozen. This document **blocks its §6 from being exercised** until B1–B4 land, and owes it three §8 amendments (B5, the §5.5 disclosure, the corrected `k` bound). It does **not** edit §2–§6. |
| `docs/46_ls_preregistration_DRAFT.md` | the LS pre-registration. **§6.3 Branch B is selected**, on B2 (ADOPT unreachable under A3) plus the box-boundary argument of §5.4 that A6 already concedes. Its `Δ_shape` pre-test is open item O6. |
| `docs/31_phase_c_workplan.md` | C4.3's stage definition; its entry is now gated by this document. |
| `docs/18_hydrology_journal.md` §6, `docs/22_dry_phase_diagnosis.md` | the house register of refuted hypotheses; §3 extends it. |
