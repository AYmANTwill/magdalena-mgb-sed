# 47 — The C4.3 entry verdict: **BLOCKED UNTIL LS LANDS**

**Written 2026-08-11** by the `c3gate-synthesis` agent (process record:
`docs/agents/journal_c3gate-synthesis.md`). This document **decides one question**: may stage
**C4.3 — the sediment calibration search** — start, and under what contract. It synthesises eight
adversarial lenses plus a three-agent LS track, and it adds one measurement of its own (§5.2).
It does not edit `docs/35`, `docs/37`, `docs/42`, `docs/43` or `docs/45`, all of which are frozen
or closed to this pass.

> ## ⚠ BACK-ANNOTATED 2026-08-12 — READ §9 BEFORE QUOTING ANY STATUS FROM THIS FILE
>
> **This document was written 2026-08-11 and its statuses are as of that date.** By 2026-08-12
> **four of the five repairs of §6.1 and three of the twelve open items of §7 had been discharged
> by other documents**, which back-annotated themselves and not this one. Every such site is now
> struck in place in the house pattern (`~~old~~` → **new**, dated, with the owning doc named) and
> the full item-by-item ledger — including what was checked and found **still open** — is **§9**,
> appended 2026-08-12 by the `backannotate-47` agent
> (process record `docs/agents/journal_backannotate-47.md`).
>
> **THE VERDICT ITSELF DOES NOT MOVE. `C4.3-BLOCKED-UNTIL-LS-LANDS` STILL HOLDS**, re-affirmed on
> 2026-08-12 by every downstream owner: `docs/37` A3.4 (*"Is C4.3 thereby UNBLOCKED? **NO**"*),
> `docs/45` §8.5.10 item 8 (*"It does not unblock C4.3"*), `docs/46` §9, `docs/51` §THE FOUR
> ANSWERS item 4, `docs/53` §8. **What moves is the REASON**, and the title now under-describes it:
> the LS **formulation** landed 2026-08-12 (`docs/37` **A3**, ADOPT-SOURCE), so the block no longer
> rests on B1. See **§9.2** for the corrected blocking condition, which is *narrower in name and
> not weaker in force*.

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
> decision of `docs/35` §9.3, executed under the pre-registration ~~drafted as
> `docs/46_ls_preregistration_DRAFT.md`~~ → **`docs/46_ls_preregistration.md`, FROZEN (READ OUT)
> 2026-08-11; §10 is its amendment slot** (`docs/46`:1, :3 — *"⚠ FROZEN 2026-08-11. §1–§8 ARE IN
> FORCE. §10 IS THE AMENDMENT SLOT."*; no `_DRAFT` file exists on disk), frozen, with a
> `ls_formulation` value and an evidence grade recorded. When it lands, C4.3 starts under the
> six-item contract of §6.2 below.
>
> > **⚠ BACK-ANNOTATION 2026-08-12 — THIS SENTENCE IS NOW WRONG IN ONE DIRECTION ONLY, AND IT IS
> > NOT THE PERMISSIVE ONE. C3.1 HAS LANDED; C4.3 IS STILL BLOCKED.**
> > `docs/37` **A3** (2026-08-12) — the owner of C3.1, named as this event by `docs/46` §9's
> > registration card — reads: *"**THE C3.1 ENACTMENT.** The LS *formulation* is DECIDED on source
> > grounds: **ADOPT-SOURCE**, `ls_formulation = buarque_2015_dg`. **No engine default moves here.
> > C3 stays OPEN. C4.3 stays BLOCKED.**"* So **the single named event was necessary and is now
> > measured NOT to have been sufficient**, and `docs/37` A3.4 says so in its own heading: *"Is
> > C4.3 thereby UNBLOCKED? **NO** — and this amendment is the act that makes the block
> > *dischargeable*, not the act that discharges it."*
> > **The corrected blocking condition is in §9.2.** It is not one event; it is four, none of them
> > B1. This document's title is retained unchanged as the record of what was decided on
> > 2026-08-11.
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

> **⚠ 2026-08-12 — this paragraph runs on the bracket THIS DOCUMENT'S OWN §4.3 retires 280 lines
> later, and it is preserved because that is how the defence was actually mounted.** *"×2.37–3.00"*
> was superseded **as a measurement** by §4.3's **`f_LS` ∈ [0.25146, 0.43194]** ⇒ **2.3151× –
> 3.9768×** — re-affirmed by `docs/51` §THE FOUR ANSWERS item 1 (*"This **supersedes ×0.333 – ×0.421
> and '2.37× – 3.00×'**"*) and enacted in `docs/37` A3.3.1, `docs/43` §7 amd 3, `docs/45` §8 amd 3.
> **Re-derived at the corrected bracket the finding STRENGTHENS**, which is why it is annotated and
> not rewritten: `1.211 × 2.3151 = 2.804` and `1.211 × 3.9768 = 4.816`, so the upper end now crosses
> 3.9 instead of stopping at 3.63. §5.2 already carries that arithmetic; this paragraph does not.
> **The conclusion of this paragraph — that the Π-not-α defence fails — is unchanged.**

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

### 2.3 D3 — the per-node mass audit is blind to NaN and reports PASS on an all-NaN run **BLOCKING (one line)** — ✅ **RESOLVED 2026-08-12**

> **⚠ BACK-ANNOTATION 2026-08-12 — D3 is RESOLVED and B3 is DISCHARGED. Verified on disk by this
> pass, read directly and not taken on trust.** `src/mgb_transport.py`:**908** now reads
> `if not (m <= max_resid):` — the NaN-safe form this section prescribes — with the IEEE-754
> rationale in the comment at :902–907 (*"every IEEE-754 comparison against NaN is False, so a NaN
> residual would leave max_resid at 0.0 and this module would then announce
> `node_partition_exact: True` - its STRONGEST mass claim - on a run carrying no usable mass"*).
> The regression test is `tests/test_transport.py`:**245–277**,
> `test_the_partition_claim_does_not_survive_an_overflowing_run`, whose input is **all finite**
> (`assert np.all(np.isfinite(load))`) and which asserts at :**274**
> `assert math.isnan(res.ledger["max_node_residual_t"])` and at :271 `assert not
> res.ledger["node_partition_exact"]`. A second test at :**232**,
> `test_a_nan_local_load_is_rejected_at_the_door`, pins the door screen so the overflow route is
> the only one left. Independently confirmed by `docs/37` A3.4 item 1 (*"B3 — `src/mgb_transport.py`:908
> reads `if not (m <= max_resid)` … The all-NaN run can no longer publish a false PASS"*) and by
> commit `a0d8afb` *"fix: the per-reach mass claim no longer survives a non-finite run"*.
> **The finding's text below is preserved verbatim — it is the provenance for the fix**, and the
> line numbers it quotes (`:901-903`, `:803`, `tests/test_transport.py:583`) are the PRE-FIX ones.

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

### 2.4 D4 — the `docs/42` §9 transcription is unperformed and C4 has already started **BLOCKING (audit trail)** — ✅ **CLOSED 2026-08-11/12**

> **⚠ BACK-ANNOTATION 2026-08-12 — D4 is CLOSED and B4 is DISCHARGED. The owning document says so
> itself.** `docs/42` §9's amendment log now exists and carries **A-P1** (§9.2 — the fitting set is
> the **CAL 8**), **A-P2** (§9.3 — `21237020` ARRANCAPLUMAS is evaluation-only), **A-P3** (§9.4 —
> deposition `k` FIXED at 0), **A-P1.1** (§9.5 — the power table corrected and the
> 0.0096-vs-0.0104 discrepancy resolved), all dated 2026-08-11, plus **A-P4** (§9.7, 2026-08-12).
> `docs/42`:**648** — the §9 card cell now reads *"⚠ **THREE, all dated 2026-08-11 — A-P1, A-P2,
> A-P3, plus A-P1.1 … Plus A-P4, dated 2026-08-12 (§9.7)** … This cell read `none` until
> 2026-08-11 while C4 was already under way; that gap is the audit-trail defect `docs/47` §2.4
> (D4) recorded, and §9.1 states plainly that the transcription is late."* `docs/42`:**660** heads
> the log *"§9.1 — Amendment log: opened 2026-08-11, and it is late."* `docs/42`:**644** now carries
> *"the fitting set is **SUPERSEDED by amendment A-P1 (§9.2): it is the CAL 8**"*, and the all-18
> clause and the never-fit rule are stated there as **unchanged**. `docs/42` §9.6 **F5** adjudicates
> this item by name: *"**`docs/47` §2.4 D4** (this transcription unperformed) **is discharged** by
> §9.1–§9.5. **D4 may be CLOSED.**"*
> **The "carried defect inside the defect" below is also settled — see open item O7 (§9.3).**
> `docs/42`:**901** F5's companion **F4** reads: *"**`docs/47` open item O7** … is answered by §9.5.
> O7 may be **CLOSED**: 0.00964 is correct, `docs/42` §4.2 was wrong, reason recorded."*
> **The finding's text below is preserved verbatim as the provenance for the repair.**
> *(One residue this pass did not close and does not claim: `docs/42` §9.6 **F1** records that
> §4.2's **body** still prints `0.0104`, so the retired number remains quotable from `docs/42`
> outside its amendment slot. That is `docs/42`'s owner's, not this document's.)*

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
| **C1** | **`docs/43` §3.4's load-bearing "These overlap" mixes the prior and adopted `C` levels.** 6.83–8.73 is `11.8 × {144,184} / 248.730` (prior C); the reading-B band 7.92–8.86 is at the adopted C. At the adopted C the deposition-free band is `11.8 × {144,184} / 299.5387` = **5.67 – 7.25**, which is **disjoint** from 7.92–8.86 (gap 0.67). | medium — **PARTLY ENACTED 2026-08-12; the site list is stale** | ~~**Correct in place at C5 or at the next `docs/42` amendment.** Propagated verbatim into `docs/42:15, :299, :472` and `docs/45:404`.~~ The resulting caution is in the safe direction, so the conclusion is unaffected; the *reasoning* is wrong and `docs/37`'s own rule is "never quote a load without its convention **and** its `cp_revision`". — **⚠ 2026-08-12: (a) ENACTED at its home site.** `docs/43` §7 **Amendment 5** strikes §3.4's *"These overlap"* in place and prints the re-based table: deposition-free `11.8 × 144 / 299.5387088405831` = **5.6727**, `11.8 × 184 / …` = **7.2485**, against reading-B **7.92 – 8.86** ⇒ *"**Gap between 7.2485 and 7.92 = 0.6715 in α. The two bands are DISJOINT.**"* `docs/35` §9.4.4 and `docs/37` A3.3.1 (:355–359) carry the same re-basing. **(b) The propagation list above has DRIFTED and must not be used as line refs**: this pass read `docs/42`:299 (a C-class erosion-share table row) and `docs/42`:472 (G3.3's opening) and **neither carries the band**; `docs/45`:404 is inside §3.5's ONI clause. Quote the *sentence*, not the line. **(c) The remaining live copies are OWED, with a named refusal on the record**: `docs/42` §9.7 **F7** registers `docs/42`'s own copies as owed *"as a further `docs/42` amendment"* and explicitly declines to smuggle them into A-P4's slot — correct process, not an oversight. **(d) O12 — whether the now-disjoint bands change §3.4's "doubly load-bearing" conclusion about G5 — is still OPEN and `docs/43` amd 5 declines to decide it** (*"deciding it needs a judgement about reading B that this pass has no standing to make, and the safe-direction caution is retained regardless"*). |
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
   > **⚠ 2026-08-12 — the bound's *comparative* is inverted wherever this document states it; see
   > §6.2 item 4 as annotated.** The registered form is *"no first-order channel sink **WEAKER**
   > than ≈ 10× over ~342 km is **detectable**"* (`docs/42` §9.7 A-P4:1005–1009 — *"`k_min` is a
   > **detection floor**"*), the ≈ 10× is the **all-18 G1.2** figure, and the **CAL-8 fit-set** floor
   > is **`k_min` = 0.0838 /km ⇒ ≈ 173× over 61.5 km** (`docs/45` §8.1 row 4). **The limitation
   > itself is unchanged and gets STRONGER, not weaker** — `docs/42` §9.7 re-affirms A-P3's decision
   > to fix `k` at 0 on exactly this ground.
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
| **source method, continuous L** | **129.3840** | **0.43194** | 0.42135 ᴬ |
| **source method, Desmet–Govers L** | **75.3235** | **0.25146** | 0.24466 ᴬ |

> **ᴬ ⚠ 2026-08-12 — THE AREA-WEIGHTED COLUMN IS A THIRD AREA SUPPORT. The values are not wrong;
> they are not `docs/46` §3.3's `f_area` either, and they must not be quoted as it.** This is not
> this pass's adjudication — **it is the owning amendment's**, which reached `docs/47`'s cell by
> name before this pass existed. `docs/46` **§10 Amendment 2 (v) item 1**, verbatim:
>
> > *"**`docs/47` §4.3's area-weighted column prints 0.42135** for this cell. That is **not** a
> > rounding of the corrected value — 0.42136300143291305 both rounds *and* truncates to 0.42136 at
> > five decimals. It reconstructs as the **`urh_ls2d_variants.csv` `area_km2` weighting**,
> > 0.4213519856784954 … The same table's DG cell prints **0.24466** where the registered value is
> > 0.2446790094097074 (→ 0.24468). **So `docs/47` §4.3's area column is a third support**, owed to
> > `docs/47`'s owner, and it changes no `docs/47` verdict (all three propositions are
> > erosion-side)."*
>
> **Recomputed independently by this pass, read-only from `data/processed/`, rather than copied:**
> the `area_km2` weighting of `urh_ls2d_variants.csv` (32,782 rows) gives
> `V4/V0` = **0.421351985678496** → **0.42135**, reproducing the printed cell; the `n_cells`
> weighting gives 0.42136472954222043 and the `area_frac` weighting 0.4216185646720824. The
> **registered** `f_area(V4)` — `docs/46` §3.3's per-cell basin quantity over all **30,235,916**
> cells — is `ls2d_variants_summary.json:variants.V4_buarque_2015.ratio_to_V0` =
> **0.42136300143291305**, corroborated at **0.42136300143291344** by
> `ls2d_defect_b.json:decomposition.V4_over_V0`. The registered DG endpoint is
> `ls2d_defect_b.json:decomposition.V4dg_over_V0` = **0.2446790094097074** (→ **0.24468**).
>
> **THE REGISTERED VALUES, which supersede this column for every purpose outside this table:**
> **`f_area` ∈ [0.2446790094097074, 0.42136300143291305]** (`docs/46` §10 amd 2; `docs/51` §9 amd 1;
> `docs/43` §7 amd 8; `docs/37` A3.3.4). **NOTHING THIS DOCUMENT DECIDES MOVES**: `f_ero` is
> untouched at **0.43194417543884817** / **0.25146**, and `docs/46` §3.3 ground **G-ii** governs —
> *"`f_ero` decides; `f_area` is reported beside it, always, and can never override it."*
>
> **Do NOT "correct" §4.1's `×0.4214`** (the harness-validation line above): `16.7754 / 39.8123 =
> 0.42136224…` → **0.4214** at 4 d.p., which is the **corrected** value; the superseded 0.42147514
> would round to 0.4215. Recomputed this pass. It is right as printed.

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
finite-difference character. ~~**A different reading of p. 94 moves both rows.**~~

> **⚠ WITHDRAWN 2026-08-12 — the source was obtained and read verbatim; the interval is not a
> reading ambiguity.** `docs/51` §1 records the primary text on disk (Buarque 2015, `lume.ufrgs.br`
> handle `10183/129875`, 182 pp., sha256 `3047624f…c0037`; PDF p. 63 = printed p. 47). `docs/51`
> §THE FOUR ANSWERS item 1, verbatim: *"**And the interval is not an uncertainty over readings of
> the source**: with Buarque eq. 13 now read verbatim (§1), the source formulation read whole is a
> **POINT at ×0.25146**, and ×0.43194 is a documented **hybrid** that keeps *our* `L`. The span
> between them is the `L`-form lever, not a reading ambiguity."* `docs/46`:119 — *"Every lever is
> **CITED** … there is no admissible reading in which `L` is our point-rate form."*
> **The p. 94 limiter reading specifically is settled by the same two-sentence device this
> paragraph already invokes** (p. 94 + p. 98), and eq. 14's `Sf` units — the last open source
> question — closed **against** the direction that would have narrowed the bracket (`docs/51` §1
> (R6): *"`Sf` is slope PERCENT"*, printed p. 47, corroborated p. 48).
> **Consequence for §6.2 item 2:** what travels with every α̂ under `docs/37` A3 is the **POINT**
> branch — `f_LS` = **0.25146** erosion-weighted (area proxy **0.2446790094097074**), `1/f_LS` =
> **3.976775630318937**, grade *formulation CITED / factor DERIVED / LEVEL UNVALIDATED* — **and not
> the `[0.25146, 0.43194]` bracket** (`docs/37` A3.4, "The contract C4.3 would start under").
> **The bracket survives as a measurement**; it is no longer the thing that travels.

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

> **⚠ BACK-ANNOTATION 2026-08-12 — P2 IS CONVENTION-DEPENDENT AND DOES NOT SURVIVE THE B2 FIX. THE
> VERDICT IS STRENGTHENED, NOT WEAKENED.** This correction was **owed to this document by name**;
> `docs/45` §8.5.12 item 3, verbatim:
>
> > *"**`docs/47` §5.2's *'one corner of the registered parameter space clears both thresholds'* and
> > §5.2's conclusion *'the LS decision is the dominant term in the C4 verdict'* do not survive the
> > fix B2 asks for.** Both are convention-(i) statements; under the enacted convention no corner
> > clears and the LS decision does not move the rail verdict (§8.5.8). **`docs/47`'s VERDICT is
> > strengthened, not weakened** — the rail becomes certain rather than probable. Owed to `docs/47`'s
> > owner, along with a note that its §5's three propositions should be re-ordered: **P1 is
> > discharged by this amendment; P3 and Branch B / `Δ_shape` now carry the block.**"*
>
> **The mechanism, so this is not taken on authority.** This section rescales the α **axis** and
> then reads the rescaled α̂ against a box **held literal** — convention (i). `docs/45` §8 Amendment 4
> enacts convention (ii): the box `[2.0, 30.0]` and the stop 3.9 were registered at `f_LS` = 1, so
> **an `f_LS ≠ 1` moves the thresholds too**, and the gate is re-expressed in the invariant unit Π.
> Under (ii) the LS swap moves the axis **and** the boundary by the same factor, so **it cannot move
> the rail verdict at all**: `docs/45` §8.5.8 measures the rail in **three** of the three G2.3 β
> corners rather than two, with a shortfall of **×1.5516** at the box floor that the maximal
> favourable shape-driven lift `exp(+Δ_shape)` = **1.1387665371423883** still leaves short by
> **×1.3625** (§8.5.9).
>
> **What this changes and what it does not.** ~~*"one corner … clears both thresholds"*~~ and
> ~~*"the LS decision is the dominant term in the C4 verdict"*~~ are **WITHDRAWN as stated**. What
> the LS decision still moves is (a) the **shape** of the residual vector — `Δ_shape` = 0.1299456916752905
> > 0, hence O5 and `docs/46` §6.1's mandatory re-run; (b) the basin load (75.32347104056149 vs
> 299.5387088405831 Mt/yr); (c) the `docs/35` pairing. **§5's three propositions re-ordered, per the
> owing document: P1 is DISCHARGED by `docs/45` §8 amd 4; P3 and Branch B / `Δ_shape` now carry the
> block.** §5's headline answer — *"NO. It is not acceptable, and the reason is arithmetic, not
> caution"* — **is unchanged and is now more certain.**

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

> **⚠ BACK-ANNOTATION 2026-08-12 — FOUR OF THE FIVE REPAIRS HAVE LANDED. C4.3 IS STILL BLOCKED.**
> Status column added below; **no repair's text is altered**. Summary, each verified against the
> document that enacted it:
>
> | repair | status 2026-08-12 | enacted by |
> |---|---|---|
> | **B1** — land C3.1 | **LANDED, in a reduced form** | `docs/37` **A3** (ADOPT-SOURCE, `ls_formulation = buarque_2015_dg`) |
> | **B2** — re-express the gate in Π | **DISCHARGED** | `docs/45` **§8 Amendment 4** (`gate-reexpression`) |
> | **B3** — the NaN-blind mass audit | **DISCHARGED** | `src/mgb_transport.py`:908 + `tests/test_transport.py`:274 (verified on disk, §2.3) |
> | **B4** — the `docs/42` §9 transcription | **DISCHARGED** | `docs/42` §9.1–§9.5 (A-P1, A-P2, A-P3, A-P1.1) + §9.7 (A-P4) |
> | **B5** — replace the ±38 % Π band | **DISCHARGED** | `docs/45` **§8 Amendment 1**, with `docs/42` §9.7 A-P4 and `docs/43` §7 amd 1/4 |
> | the **§5.5** disclosure | **DISCHARGED** | `docs/45` **§8 Amendment 2** |
>
> **Landing B1–B5 was necessary and is now measured not to have been sufficient.** The blockers
> that remain are listed in **§9.2** and none of them is a §6.1 repair. **Nothing here licenses a
> C4.3 start.**

| # | repair | from | cost | why blocking |
|---|---|---|---|---|
| **B1** ✅ **LANDED 2026-08-12** | **Land C3.1** — the LS-formulation decision, under `docs/46` frozen, with `ls_formulation`, its evidence grade, and the negative-result branch (`docs/46` §7) live. | §5 | ≈ 4 min per LS pass; hours for the full variant set | The α box is denominated in the quantity C3.1 decides (§5.1–§5.2). — **`docs/37` A3: ADOPT-SOURCE, `ls_formulation = buarque_2015_dg`, evidence grade recorded. A3.4 item 1: *"B1 lands here, in the reduced form A3.1.6 permits … What B1 does not carry is the default-switch proposal, because ADOPT-SOURCE is not yet exercisable."* `docs/45` §8.5.10 item 8 words the same state as *"B1 is not"* discharged; both describe one fact — the formulation is DECIDED and RECORDED, and NOT EXERCISABLE. §9.2.** |
| **B2** ✅ **DISCHARGED 2026-08-12** | **Re-express the C4.3 gate in Π, or re-register the α box against the adopted `f_LS`.** Whichever C3.1 returns — including *"not resolvable from the available literature"* — `docs/45` §2.1's box and `docs/35` §6.1's 3.9/35.4 must be restated in a unit that survives it. A `docs/35` §9 amendment may only be **proposed** by the session that hits the stop (`docs/45` §6.1), so this is owed to the document owners, not to C4.3. | §5.1 | one amendment | Otherwise C4.3 runs against a floating threshold. — **`docs/45` §8 Amendment 4 (§8.5): *"Discharges `docs/47` §6.1 repair B2"*, taking route (A), the gate re-expressed in Π. Its own one-line verdict: *"the re-expression does NOT fix `docs/47`'s `FAIL — RAILED` / `FAIL — NUMERIC` pre-computability problem. It RELABELS it — and in the Π coordinate the problem is measurably WORSE, not better … `C4.3-BLOCKED-UNTIL-LS-LANDS` is unchanged."* The `docs/35` §6.1 half is PROPOSED, not enacted (§8.5.11 item 2), and `docs/35` §9 carries no α-box re-registration — verified on disk: §9.1–§9.4 only.** |
| **B3** ✅ **DISCHARGED 2026-08-12** | **Fix `src/mgb_transport.py:902`** (`if not (m <= max_resid)`) and add a NaN regression test; `tests/test_transport.py:583` currently passes on an all-NaN run. | §2.3 | one line + one test | C4.3 would publish the false PASS. — **Both landed and both read on disk this pass: `src/mgb_transport.py`:908 is the NaN-safe form; `tests/test_transport.py`:245–277 is the regression test, asserting `math.isnan(...)` at :274 on an input that is all-finite by construction. §2.3.** |
| **B4** ✅ **DISCHARGED 2026-08-11/12** | **Transcribe P1/P2/P3 into `docs/42` §9**, dated, and correct §4.2's CAL-13 power row — resolving the 0.0096-vs-0.0104 discrepancy in writing (§2.4, O7). | §2.4 | one amendment | `docs/43` §3.1 already declares these blocking; they are unperformed. — **`docs/42` §9.1–§9.5 (A-P1, A-P2, A-P3, A-P1.1) + §9.7 (A-P4). §9.6 F5: *"D4 may be CLOSED."* F4: *"O7 may be CLOSED: 0.00964 is correct."* §2.4.** |

**And one repair owed before any C4 number is *printed*, which may be done in parallel:**

| **B5** ✅ **DISCHARGED 2026-08-12** | **Replace the ±38 % Π band.** Either make `docs/45` **G12**'s LOO-range comparison a band-**replacement** rule, or substitute the station-bootstrap band `docs/45` §4.2 already imports for every other interval. Restate the corrected `k` bound as **~10× over 342 km**, not 2.12×. | §2.2 | a `docs/45` §8 amendment | `docs/45` §6.2 item 2 makes the band mandatory on every Π and every load; it is ~4× too narrow in log units, and G12 already fires on it (0.860 ln vs ±0.322 ln). — **`docs/45` §8 Amendment 1: *"the ±38 % Π band REPLACED by the station bootstrap, and the `k` bound restated at ≈ 10× over ~342 km (discharges `docs/47` §6.1 B5)"*. The band is registered as a **procedure, not a constant**; the pre-fit value is ×0.29–×3.73. Enacted in parallel in `docs/42` §9.7 (A-P4) and `docs/43` §7 amd 1 + amd 4. Note `docs/42` §9.6 F5's *"`docs/47` B5… remains open"* was written 2026-08-11 and is superseded by A-P4 the next day.** |

**Plus the disclosure of §5.5**, as a dated `docs/45` §8 amendment.
✅ **DISCHARGED 2026-08-12 — `docs/45` §8 Amendment 2**, the PRE-FIT DISCLOSURE: *"the registered
objective has already been profiled across the whole registered α box (discharges `docs/47` §5.5;
`docs/47` **O9** carried, not decided)"*. `docs/45` §7.2's *"It does not … produce a number that any
gate here judges"* now carries an inline `[WARN]` block saying it is *"STILL TRUE OF THIS PASS, NO
LONGER TRUE OF THE PROJECT."* **O9 — whether this requires a fresh pre-registration rather than a
§8 amendment — is still OPEN and is still undecided** (`docs/45` §8.5.11 item 3: *"`docs/47` O9
remains OPEN and is not decided here"*).

### 6.2 The contract C4.3 starts under, once B1–B4 land

1. **The gate is read in Π, or in α against a named, dated `f_LS`.** No α̂ is compared to 3.9,
   35.4, or a box edge without `f_LS` and its grade in the same table.
2. **The corrected LS bracket travels with every α̂:** `f_LS ∈ [0.25146, 0.43194]` erosion-weighted
   ⇒ `1/f_LS ∈ [2.3151, 3.9768]`, unless C3.1 collapses it to a point, in which case the adopted
   point and its grade travel instead.
3. **The Π band is the corrected one (B5)**, and the sentence *"the level is set by 8 stations
   whose residuals span a factor of 412"* appears beside it.
4. **The `k` bound is stated at its corrected power** — ~~*"no first-order channel sink stronger
   than ~10× over 342 km is detectable on this fit set"*~~ → **the comparative here is INVERTED and
   the set is mis-named; corrected 2026-08-12 to the form the owning documents register:**
   > **"No first-order channel sink WEAKER than ≈ 10× over ~342 km is detectable"** — the **all-18
   > G1.2** joint-regression bound (`k_min` 0.0065–0.0069 /km). **On the CAL-8 fit set the floor is
   > `k_min` = 0.0838 /km ⇒ ≈ 173× over 61.5 km** (0.0883 /km ⇒ ≈ 164× on `docs/42` §4.1's printed
   > `Lw`).
   >
   > **Owners:** `docs/42` §9.7 (A-P4):1005–1009 — *"`k_min` is a **detection floor**. With the verb
   > *detectable* the true comparative is **weaker** (a sink with `|k| < k_min` leaves no visible
   > trace) … §6 G1.2, §9.4 and `docs/45` §2.3 all pair **"stronger"** with **"detectable"**, which
   > asserts the opposite of what the statistic supports. **A-P4 registers the `weaker` /
   > `detectable` pairing.**"* `docs/45` §8.1's site table separates the two sets explicitly: row 5
   > (§2.3) — *"≈ 2.12× over 348.4 km at best, **all-18 test**"* → *"`k_min` 0.0065–0.0069 /km ⇒
   > **≈ 10× over ~342 km**, in the **'weaker than'** sense"*; row 4 (§2.2) — *"`k_min` on the **fit
   > set**"* → *"**0.0838 /km ⇒ ≈ 173× over 61.5 km**"*. `docs/43` §7 amd 4 and `docs/42` §9.7 row 10
   > carry the same pair.
   >
   > **Both figures must travel**, because §2.6 item 1 and G9 make the all-18 span the reporting
   > frame while the fit is CAL 8. *(`docs/45`'s own registered sentence at §8.1:838 still reads
   > "…detectable on this fit set"; that wording is `docs/45`'s to own and is NOT contradicted here
   > — what is corrected here is this document's **comparative** and its silent conflation of the
   > two sets.)*

   — together with the asserted `SDR = 1.0` claim in the words `docs/45` §2.3 registers.
5. **Everything else in `docs/45` §2–§6 is imported unchanged and obeyed**, including the
   asymmetric-bar statement, G9's 66.53 % disclosure, G6's five reporting elements, G10's
   mandatory "the calibration determined a level and essentially nothing else" statement, the
   five not-claims of §5, and the `docs/23` §13.2 embargo.
6. **The §5.5 disclosure appears in `report_C4.json` and in the C4 document**: the registered
   objective was profiled before the fit, by whom, and where the record is.

### 6.3 What may be done **now**, before B1 lands

**Permitted** (LS-invariant, consumes no registered budget, produces no number any `docs/45` gate
judges):

- ~~**`docs/46` §6.1's `Δ_shape` pre-test.** It is the registered Branch A/B discriminator, it has
  **not been run** (O6), and it costs minutes. Run it and record the number **before** C3.1
  reports, so it cannot be read backwards.~~
  > **✅ DONE 2026-08-11 — and the ordering held.** `docs/53_delta_shape_pretest.md`:19 —
  > **`Δ_shape` = 0.1299456916752905** (variant V4, weights normalised over the 18 usable SSC
  > stations, maximum over the CAL 8; argmax `24037390` CAPITANEJO). `docs/53`:24 — *"**VERDICT —
  > `Δ_shape` > 0 ⇒ BRANCH B IS MANDATORY**"*. `docs/53`:397 — *"`docs/47` **O6** … **CLOSED.**
  > Value 0.1299456916752905; Branch B."* Recorded in `docs/46` §10 amendment 1. `docs/52` fixed
  > the bar **before** this run and **blind to its result**, so it could not be read backwards.
  > **This REMOVES Branch A entirely and therefore strengthens §5.4**: `docs/46` §6.2's six Branch-A
  > conditions are available *"only if `Δ_shape` = 0"*, so they are **moot rather than satisfiable**
  > and there is no legal PROVISIONAL C4.3 at all (`docs/37` A3.4 (3) item 1). It also converts
  > `docs/46` §6.1's re-run mandate into a live obligation — see §9.2.
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
| **O1** — **NARROWED 2026-08-12, still open** | **Whether the LS levers can be settled from the literature at all.** Desmet & Govers (1996) primary text not obtained (paywalled); Fagundes et al. (2026) not retrieved (ScienceDirect 403 on every route). | Obtaining either. `docs/46` §7 already pre-commits *"the LS level is not resolvable from the available literature"* as a publishable **result**, which is the right posture. — **⚠ 2026-08-12: the SOURCE lever question is settled, the two named PDFs are still unobtained.** `docs/51` §1: *"**The PDF is obtainable, it was obtained, and it is on disk**"* — Buarque (2015), `lume.ufrgs.br` handle `10183/129875`, 182 pp., sha256 `3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037`; **(R6) RESOLVED — `Sf` is slope PERCENT**, printed p. 47 verbatim, corroborated p. 48. `docs/46`:119 — *"Every lever is **CITED** … there is no admissible reading in which `L` is our point-rate form."* Consequently **C3.1 was decided on source grounds** (`docs/37` A3, ADOPT-SOURCE) rather than under `docs/46` §7's negative branch. **What is still open and unchanged:** D&G (1996) and Fagundes et al. (2026) remain unobtained — `docs/37` A3.7 lists **O1** among the items *"still open and NOT fixed by any outcome of this amendment"*, alongside **O2**, **O3**, **O4** and **O5**. |
| **O2** | **Which S function is valid above tanθ 0.50** — 11.26 % of cells, **35.5 % of the S signal**. | A primary source that validates any S function above 50 % slope. None exists (Schmidt et al. 2019). **No band invented.** |
| **O3** | **The exact slope-length cap.** The literature requires one, rules out 1 km², and calls the value "arbitrary" in print. Defensible span **×0.351 – ×0.585**. | A written source-grounds choice under `docs/46` §4's decision ladder. |
| **O4** | **Moderate vs low rill:interrill `m` column** (worth ×0.508 either way); and whether `α = 11.8` (Williams 1975) is like-for-like with **any** 2-D contributing-area LS. | AH-703 leaves (a) to the user; (b) bounds every ratio in §4.3 from above and may be unresolvable. |
| **O5** | **Whether `F_report` clears the bar anywhere in the box under a corrected LS.** This run rescaled the α **axis**, which is exact for the level, but did not re-profile the objective on a corrected LS **field**, so the per-station residual redistribution (±1.287×) is unmodelled. | Re-running the §5.2 profile on the adopted LS field — **after** C3.1 lands, never before. |
| ~~**O6**~~ ✅ **CLOSED 2026-08-11** | ~~**`docs/46` §6.1's `Δ_shape` pre-test has not been run.** It is the registered Branch A/B discriminator.~~ | ~~Running it (§6.3). Minutes.~~ — **RUN. `docs/53_delta_shape_pretest.md`:19 — `Δ_shape` = **0.1299456916752905** (V4; weights normalised over the 18 usable stations, max over the CAL 8; argmax `24037390` CAPITANEJO; smallest of the eight `26127010` EL ALAMBRADO AUT at 0.0179854753, so **no CAL station is invariant**). :24 — *"**VERDICT — `Δ_shape` > 0 ⇒ BRANCH B IS MANDATORY**"*. :397 — *"`docs/47` **O6** … **CLOSED.** Value 0.1299456916752905; Branch B."* Recorded in `docs/46` §10 amendment 1; the bar was fixed blind beforehand by `docs/52`. Branch-invariance checked: all **thirty** measured readings of the definition lie in [0.0159907, 0.1638779], all > 0 (`docs/37` A3.4 (3)). **Consequence, not a formality: Branch A is CLOSED, so no legal PROVISIONAL C4.3 exists, and `docs/46` §6.1's re-run mandate is live — see §9.2.** |
| ~~**O7**~~ ✅ **CLOSED 2026-08-11** | ~~**The 7 % method difference between the two `k_min` computations** — `docs/42` prints 0.0104 /km, the lens computed 0.0096 /km, and `docs/43` P1 quotes the lens's number as `docs/42`'s.~~ | ~~The B4 transcription must pick one and record why.~~ — **It did. `docs/42` §9.5 (A-P1.1) is headed *"§4.2's power table, corrected — and the **0.0096-vs-0.0104 discrepancy resolved**"*; `docs/42`:803 gives **CAL 13 → 0.009640**, against *"§4.2 prints 0.0104 — **does not reproduce**"*. `docs/42` §9.6 **F4**: *"`docs/47` open item **O7** … is answered by §9.5. O7 may be **CLOSED**: 0.00964 is correct, `docs/42` §4.2 was wrong, reason recorded."* `docs/43` §7 amd 6 enacts the matching P1 attribution fix; `docs/42` §9.6 F3 records that `journal_adj-c4-feasibility.md`:167's *"method rounding"* explanation is **WITHDRAWN**. **Residue, not re-opened: `docs/42` §4.2's body still prints 0.0104 (its own §9.6 F1).** |
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
| `docs/37_c3_closure.md` | C3's verdict and Amendment A1/A2. §4 candidate 0's ×0.333–×0.421 is **superseded as a measurement** by §4.3; A1.9's withdrawn direction is carried unchanged. **Added 2026-08-12: `docs/37` **A3** is this document's §6.1 **B1** event — ADOPT-SOURCE, `ls_formulation = buarque_2015_dg` — and its **A3.4** is the authoritative statement that C4.3 is nonetheless still BLOCKED. A3.3.1/A3.3.2/A3.3.4 enact the bracket, eq.-14 and `f_area` corrections in that file. C3 stays OPEN.** |
| `docs/40_sdr_evidence.md` | the SDR retirement; §3.2 restates it so it is not re-raised. |
| `docs/41_cfactor_evidence.md` | the adopted `C` revision; **unaudited**, open item O10. |
| `docs/42_c4_guards.md` | G1–G9. §2.2 corrects its σ_r-derived power numbers; ~~§2.4 records that its §9 transcription is **unperformed**~~ → **the transcription landed 2026-08-11/12 as §9.1–§9.5 (A-P1, A-P2, A-P3, A-P1.1) and §9.7 (A-P4); its own §9.6 F5 states *"D4 may be CLOSED"* and F4 *"O7 may be CLOSED"*. A-P4 also settles the `weaker`/`detectable` comparative this document had inverted (§6.2 item 4).** |
| `docs/43_c3_c4_gate.md` | the gate decision. Its reclassification **survives** (§3.2); §2.1 and §2.2 attach to its §2.1 and §3.2; §2.5 C1/C2 correct its §3.4 and §5.1. |
| `docs/45_c4_preregistration.md` | C4.2, frozen. This document **blocks its §6 from being exercised** until B1–B4 land, and ~~owes it three §8 amendments (B5, the §5.5 disclosure, the corrected `k` bound)~~ → **all three landed 2026-08-12 as `docs/45` §8 Amendments 1–3, and a fourth (Amendment 4) discharges B2 by re-expressing the gate in Π. §8 is no longer empty.** It does **not** edit §2–§6. **`docs/45` §8.5.12 item 3 owes THIS document a correction, enacted at §5.2 above.** |
| ~~`docs/46_ls_preregistration_DRAFT.md`~~ → **`docs/46_ls_preregistration.md`** *(2026-08-12: the `_DRAFT` file never existed on disk; the file was **FROZEN (READ OUT) 2026-08-11**, §10 is its amendment slot)* | the LS pre-registration. **§6.3 Branch B is selected**, on B2 (ADOPT unreachable under A3) plus the box-boundary argument of §5.4 that A6 already concedes. ~~Its `Δ_shape` pre-test is open item O6.~~ → **`Δ_shape` was COMPUTED 2026-08-11 = `0.1299456916752905` ⇒ Branch B MANDATORY (`docs/53`; recorded in `docs/46` §10 amendment 1). O6 is CLOSED — §9.3.** |
| `docs/31_phase_c_workplan.md` | C4.3's stage definition; its entry is now gated by this document. |
| `docs/18_hydrology_journal.md` §6, `docs/22_dry_phase_diagnosis.md` | the house register of refuted hypotheses; §3 extends it. |
| **Added 2026-08-12** — `docs/46_ls_preregistration.md` §10, `docs/51_ls_freeze_decision.md`, `docs/52_materiality_bar_decision.md`, `docs/53_delta_shape_pretest.md` | the LS track that ran **after** this document and discharged five of its items. `docs/51` obtains the source and settles (R6); `docs/52` fixes the materiality bar blind; `docs/53` computes `Δ_shape` and closes **O6**; `docs/46` §10 amd 1–2 register both plus the `f_area` support correction. See §9. |

---

## 9 — BACK-ANNOTATION, 2026-08-12

**Appended by the `backannotate-47` agent** (process record
`docs/agents/journal_backannotate-47.md`). **§1–§8 above are the record of what was decided and
believed on 2026-08-11 and are NOT rewritten** — every correction in this document is a
strike-through with a dated pointer in the `docs/37` A2.7 / `docs/46` §10 house pattern, and every
superseded sentence remains readable. **This section adds no measurement of its own except two
read-only recomputations disclosed in §9.5, decides nothing, closes no C3 clause, moves no engine
default, and does not unblock C4.3.**

### 9.1 The ledger — what moved, who moved it, and what did not

| item | site | what it claimed on 2026-08-11 | owning doc, and what it says now | status |
|---|---|---|---|---|
| **D3 / B3** | §2.3, §6.1 | *"the per-node mass audit is blind to NaN … **BLOCKING**"*; *"`tests/test_transport.py:583` currently passes on an all-NaN run"* | **`src/mgb_transport.py`:908** = `if not (m <= max_resid):`, IEEE-754 comment at :902–907; **`tests/test_transport.py`:245–277**, `math.isnan(...)` asserted at :274 on an all-finite input; door screen at :232. Confirmed by `docs/37` A3.4 item 1 and commit `a0d8afb`. | **VERIFIED-DISCHARGED** *(read on disk this pass, not taken on trust)* |
| **D4 / B4** | §2.4, §6.1 | *"the `docs/42` §9 transcription is unperformed … **BLOCKING**"*; *"`docs/42` §9 still reads `\| Amendments \| none \|`"* | `docs/42` §9.1–§9.5 (A-P1, A-P2, A-P3, A-P1.1) + §9.7 (A-P4); §9 card at :648. **§9.6 F5**: *"**`docs/47` §2.4 D4** … **is discharged** by §9.1–§9.5. **D4 may be CLOSED.**"* | **VERIFIED-DISCHARGED** |
| **B1** | §6.1, VERDICT | *"the condition for unblocking is a single named event: **C3.1 lands**"* | `docs/37` **A3** (2026-08-12): *"**ADOPT-SOURCE**, `ls_formulation = buarque_2015_dg`. **No engine default moves here. C3 stays OPEN. C4.3 stays BLOCKED.**"*; A3.4 item 1: *"B1 lands here, in the reduced form A3.1.6 permits."* `docs/46` §9's card names A3 as the B1 event. | **VERIFIED-LANDED (reduced form)** — see §9.4 for the one recorded disagreement |
| **B2** | §6.1 | *"Re-express the C4.3 gate in Π … Otherwise C4.3 runs against a floating threshold"* | `docs/45` **§8 Amendment 4** (§8.5): *"**Discharges `docs/47` §6.1 repair B2**"* — route (A), the gate in Π. Its own verdict: *"the re-expression does NOT fix … the pre-computability problem. It RELABELS it — and in the Π coordinate the problem is measurably WORSE."* | **VERIFIED-DISCHARGED** |
| **B5** | §6.1 | *"Replace the ±38 % Π band … a `docs/45` §8 amendment"* | `docs/45` **§8 Amendment 1** — band replaced by the station bootstrap (pre-fit ×0.29–×3.73, registered as a **procedure not a constant**), `k` bound at ≈ 10× over ~342 km. Parallel enactments: `docs/42` §9.7 A-P4, `docs/43` §7 amd 1 + amd 4. | **VERIFIED-DISCHARGED** |
| **§5.5 disclosure** | §5.5, §6.1 | *"`docs/45` §8 must carry a dated amendment disclosing the pre-fit profile … before C4.3 runs"* | `docs/45` **§8 Amendment 2** — the PRE-FIT DISCLOSURE, *"(discharges `docs/47` §5.5; `docs/47` **O9** carried, not decided)"*. | **VERIFIED-DISCHARGED**; **O9 STILL-OPEN** |
| **O6** | §6.3, §7 | *"`docs/46` §6.1's `Δ_shape` pre-test **has not been run**"* | `docs/53`:19 — **`Δ_shape` = 0.1299456916752905**; :24 — *"**BRANCH B IS MANDATORY**"*; :397 — *"`docs/47` **O6** … **CLOSED.**"* Registered in `docs/46` §10 amd 1; bar fixed blind beforehand by `docs/52`. | **VERIFIED-CLOSED** |
| **O7** | §7, §2.4 | *"the 7 % method difference between the two `k_min` computations"* | `docs/42` §9.5 (A-P1.1) — *"the **0.0096-vs-0.0104 discrepancy resolved**"*; :803 CAL 13 = **0.009640**, *"§4.2 prints 0.0104 — does not reproduce"*; §9.6 **F4**: *"O7 may be **CLOSED**."* `docs/43` §7 amd 6 fixes the P1 attribution. | **VERIFIED-CLOSED** |
| **O1** | §7 | *"whether the LS levers can be settled from the literature **at all**"* | `docs/51` §1 — Buarque (2015) **obtained**, sha256 `3047624f…c0037`, (R6) resolved (`Sf` is slope **PERCENT**); `docs/46`:119 — *"Every lever is **CITED**."* But `docs/37` **A3.7** still lists **O1** among items *"still open and NOT fixed"* — D&G (1996) and Fagundes (2026) remain unobtained. | **NARROWED, STILL-OPEN** |
| **`_DRAFT` filename** | §"THE VERDICT", §8.1 | *"`docs/46_ls_preregistration_DRAFT.md`"* | **No such file exists on disk.** `docs/46_ls_preregistration.md`:1/:3 — *"**FROZEN (READ OUT)**… ⚠ FROZEN 2026-08-11. §1–§8 ARE IN FORCE. §10 IS THE AMENDMENT SLOT."* | **CORRECTED** (both sites) |
| **`f_area` 0.42135 / 0.24466** | §4.3 table | area-weighted × **0.42135** / **0.24466** | `docs/46` §10 amd 2 (v) item 1 adjudicates **this exact cell**: *"not a rounding of the corrected value … it reconstructs as the `urh_ls2d_variants.csv` `area_km2` weighting … **a third support** … it changes no `docs/47` verdict."* Registered: **[0.2446790094097074, 0.42136300143291305]**. | **ANNOTATED, NOT REPLACED** — following the owning amendment's own adjudication (§9.5) |
| **§5.2 P2 / "one corner clears"** | §5.2 | *"one corner of the registered parameter space clears both thresholds"*; *"the LS decision is the dominant term in the C4 verdict"* | `docs/45` §8.5.12 item 3 — *"do not survive the fix B2 asks for … **`docs/47`'s VERDICT is strengthened, not weakened** … **P1 is discharged by this amendment; P3 and Branch B / `Δ_shape` now carry the block.**"* | **WITHDRAWN as stated**; verdict strengthened |
| **§6.2 item 4 / §2.6 item 2 `k` bound** | §6.2, §2.6 | *"no first-order channel sink **stronger** than ~10× over 342 km is **detectable on this fit set**"* | `docs/42` §9.7 A-P4:1005–1009 — *"`k_min` is a **detection floor** … the true comparative is **weaker**"*. `docs/45` §8.1 row 5 labels ≈ 10× the **all-18** figure; row 4 gives the **CAL-8 fit set** at `k_min` **0.0838 /km ⇒ ≈ 173× over 61.5 km**. | **CORRECTED** (comparative + set) |
| **§2.1's ×2.37–3.00** | §2.1 | *"the LS level … at its **registered** ×2.37–3.00"* | This document's own §4.3 supersedes it as a measurement; `docs/51` — *"This **supersedes ×0.333 – ×0.421 and '2.37× – 3.00×'**"*. | **ANNOTATED**; finding strengthens at the corrected bracket |
| **§4.3's p. 94 caveat** | §4.3 | *"**A different reading of p. 94 moves both rows.**"* | `docs/51` — *"the interval is **not** an uncertainty over readings of the source … the source formulation read whole is a **POINT at ×0.25146** … The span between them is the `L`-form lever, not a reading ambiguity."* | **WITHDRAWN** |
| **C1's site list** | §2.5 | *"Propagated verbatim into `docs/42:15, :299, :472` and `docs/45:404`"* | Read this pass: `docs/42`:299 is a C-class erosion-share row, :472 is G3.3's opening — **neither carries the band**; `docs/45`:404 is in §3.5's ONI clause. The correction itself is **enacted** in `docs/43` §7 amd 5 (bands **DISJOINT**, gap 0.6715 in α). | **PARTLY ENACTED; line refs stale** |

### 9.2 THE CORRECTED BLOCKING CONDITION — narrower in name, not weaker in force

> ## `C4.3-BLOCKED` STILL HOLDS. **C4.3 may not start.**
>
> **What changed on 2026-08-12 is the NAME of the block, not its existence.** The title
> *"BLOCKED **UNTIL LS LANDS**"* now under-describes the situation: the LS **formulation** landed
> (`docs/37` A3), and C4.3 is still blocked — on grounds that landing B1 **created** rather than
> removed. Re-affirmed the same day by every downstream owner: `docs/37` A3.4 (*"Is C4.3 thereby
> UNBLOCKED? **NO** — and this amendment is the act that makes the block *dischargeable*, not the
> act that discharges it"*), `docs/45` §8.5.10 item 8, `docs/46` §9, `docs/51`, `docs/52`, `docs/53`.
>
> **The block no longer rests on B1, and it does NOT rest on B2 either** — B2 was discharged the
> same day by `docs/45` §8 Amendment 4. It rests on **four** conditions, each verified against its
> owner by this pass:
>
> | # | the surviving blocker | owner, verbatim | verified how |
> |---|---|---|---|
> | **1** | **Branch B is MANDATORY, so the fit must be a FIRST RUN on the ADOPTED LS FIELD** — every guard statistic re-derived on new residuals, and no rescaling of a surface already seen. | `docs/46` §6.1 as amended, §6.3 **B1**; the required sentence, written in `docs/37` A3.4: *"the fit is recoverable by rescaling `α̂` **if and only if** `Δ_shape` = 0 exactly; the measured value is **0.1299456916752905**, and **the re-run is owed**."* Branch A is **CLOSED**, so *"there is no legal PROVISIONAL C4.3 at all"*. | `docs/53`:19/:24; `docs/46` §10 amd 1; `docs/37` A3.4 (3) |
> | **2** | **The adopted variant is NOT A COMMITTED PRODUCT.** C4.3 cannot consume a variant no committed product carries. | `docs/37` A3.4 (4): *"`urh_ls2d_variants.csv` has **no `V4_dg` column** and `urh_ls2d.csv` may not be overwritten … **C4.3 cannot consume a variant that no committed product carries**, and no default can be switched by name."* | **Read on disk this pass.** `urh_ls2d_variants.csv` header = `mini,urh,n_cells,area_km2,area_frac,V0_ours_2026_08,V1_lim_pixel,V2a_m_cap05,V2b_m_step_eq14,V3_s_ws78,V4_buarque_2015,V4p_buarque_2015_cap,V5_L_dg96_fd`; `urh_ls2d.csv` = `…,ls2d,ls2d_hs,ls2d_mb86,ls2d_dg96`. **No `V4_dg` in either.** |
> | **3** | **ACT 2 — the default switch — is NOT DONE and cannot yet be drafted.** ADOPT-SOURCE is *determined and recorded but not exercisable*. | `docs/37` A3.5.1: ACT 2 *"**NOT DONE, and it MAY NOT PRECEDE ACT 1** … **It cannot even be drafted** until the column is materialised."* `src/mgb_sediment.py` defaults still `ls2d_column = "ls2d_hs"`, `urh_ls2d = "urh_ls2d.csv"`. | `docs/37` A3.5.1; `docs/45` §8.5.2 (ii) |
> | **4** | **Deliverables still owed before entry:** `docs/46` §3.3's **stratified report** (slope terciles per variant; per-station erosion-weighted `LS̄` as **levels**, not ratios) · `docs/46` §2.3's H-S field clause **(R7)/(R8)** items 2–3 · the **`docs/35` §9 amendment** A3.1.3 records as owed. | `docs/37` A3.4, *"The remaining blockers, listed plainly so nothing is inferred from silence."* | **`docs/35` §9 verified on disk this pass: §9.1, §9.2, §9.3, §9.4 only — there is no α-box re-registration.** `docs/45` §8.5.11 item 2 confirms the threshold-moving half of B2 is **PROPOSED, not enacted**. |
>
> **§5's three propositions, re-ordered as `docs/45` §8.5.12 item 3 requires:** **P1** (the box is
> written in a unit whose scale is the open question) is **DISCHARGED** by `docs/45` §8 amd 4;
> **P3** (deciding LS after the fit is the forbidden post-hoc move) **stands untouched** and is now
> the second-strongest leg; **Branch B / `Δ_shape`** is the strongest leg (`docs/45` §8.5.8).
> **§5's headline answer is unchanged and is now more certain**, because under the enacted
> convention the rail is measured in **three** of the three G2.3 β corners rather than two.
>
> **The one sentence of the verdict box that survives every correction, and is the reason the block
> holds:** *"a pre-registered search whose verdict is already known is not a test; it is a re-run of
> an answer, and it spends a one-shot registration to produce it."* Quoted back at this document by
> `docs/45` §8.5.8 as *"what is therefore still true after B2 is discharged"*.

### 9.3 Checked and found STILL OPEN — so nobody assumes silence means closed

**O2** (which `S` function above tan θ 0.50) · **O3** (the exact slope-length cap) · **O4**
(rill:interrill `m` column; α = 11.8's like-for-likeness) · **O5** (`F_report` re-profiled on a
corrected LS **field**, not axis) — all four re-affirmed open by `docs/37` **A3.7**: *"Also still
open and NOT fixed by any outcome of this amendment."* `docs/45` §8.5.9 carries **O5** *"verbatim
and unchanged"* and states *"**Nobody has re-profiled the objective on a corrected LS field.**"*
**O8** (class-C detectability) — still open and correctly still refusing a fourth number:
`docs/42` §9.7 row 20 — *"**NO CORRECTED VALUE — `docs/47` open item O8, and it stays open.** Three
passes have now produced three answers … **Do not invent a number.**"*
**O9** (whether the pre-fit profile requires a fresh pre-registration) — `docs/45` §8.5.11 item 3:
*"**`docs/47` O9 remains OPEN and is not decided here.**"*
**O10** (`docs/41` unaudited) — no `docs/41` audit exists in `docs/agents/`; `docs/37` and `docs/43`
§1.5 agree.
**O11** (the provenance record for `docs/37` A2's primary evidence) — **PARTLY discharged**:
`docs/51` §1 supplies retrieval source, sha256 and page map for **`buarque2015.pdf`**, and
`docs/51` §7 item 8 records that a **durable copy** plus *"the same record … for `ah703.pdf`"* and
the parse scripts are **still owed**. **Not closed.**
**O12** (whether the disjoint bands change §3.4's *"doubly load-bearing"* conclusion) — `docs/43`
§7 amd 5 carries it forward by name and declines to decide it.
**§2.5 C2, C3, C4, C5** — carried, not promoted, and none discharged here. **C4**'s registered
remedy (record NOAA CPC ONI v5 in `report_C4.json`, or downgrade *"out-of-phase"* to
*"out-of-window"*) is still unexercised.

### 9.4 One recorded DISAGREEMENT between owners, not reconciled by preference

**Is B1 discharged?** `docs/37` A3.4 item 1 says *"**B1 lands here**, in the reduced form A3.1.6
permits"*; `docs/45` §8.5.10 item 8 says *"**B2 is discharged; B1 is not**"*. **Both were written
2026-08-12 and both are looking at the same fact**: the LS formulation is **DECIDED and RECORDED**
(ADOPT-SOURCE, `ls_formulation = buarque_2015_dg`, grade recorded) and **NOT EXERCISABLE** (no
committed `V4_dg` column, no ACT 2, engine defaults unmoved) — `docs/45` §8.5.2 (ii) states exactly
that and cites `docs/37` A3 while doing it. The disagreement is over **what to call that state**,
not over what the state is.

**This document does not adjudicate it, and does not need to.** Under RULE 0 the owner of C3.1 is
`docs/37`, and `docs/46` §9's registration card pins the B1 event to *"`docs/37` §A3, dated,
written by the C3.1 owner"* — so **the B1 *event* has occurred**. But the annotation above records
**both** wordings verbatim, because **the practical consequence is identical either way: C4.3 does
not start**, and no reading of B1 changes any of §9.2's four surviving blockers. **A reader must
not resolve this by picking the more permissive label.** *(`docs/37` A3.1.6 also names the
governance gap underneath it: `docs/46` §4.2's table *"contains no row for 'determined but not
exercisable'"*. That gap is owed to `docs/46`'s owner, not settled here.)*

### 9.5 Disclosure for this section

- **Files written by this pass:** this section and the dated in-place annotations above in
  `docs/47_c4_entry_verdict.md`, plus `docs/agents/journal_backannotate-47.md`. **Nothing else.**
  `docs/30`, `docs/35`, `docs/37`, `docs/42`, `docs/43`, `docs/45`, `docs/46`, `docs/48`–`docs/53`,
  `docs/00_INDEX.md`, `progress_map.html`, every notebook and every source file were **read and not
  edited**. **No git command was run.**
- **No frozen artifact was opened or written.** `sim_calibrated_v2/{h2e_drivers.npz,
  parameters_H2E.csv, q_gauge_H2E.npz}` untouched. **No engine default moved. No calibration was
  launched. No simulation was run. No headline number was moved. Nothing is backdated.**
- **No original text was deleted.** Every correction is `~~struck~~` in place with a dated pointer,
  in the `docs/37` A2.7 / `docs/46` §10 pattern. **The verdict, its title and its blocking force are
  unchanged**; §9.2 corrects *why* the block holds, never *whether*.
- **Two read-only recomputations were made rather than adjudicated by preference**, from
  `data/processed/`, all files SHA-unchanged and nothing written:
  1. `f_area(V4)` under three weightings of `urh_ls2d_variants.csv` (32,782 rows) —
     `area_km2` **0.421351985678496** (→ **0.42135**, reproducing §4.3's printed cell), `n_cells`
     0.42136472954222043, `area_frac` 0.4216185646720824 — against the registered per-cell value
     `ls2d_variants_summary.json` **0.42136300143291305** and its independent corroboration
     `ls2d_defect_b.json` 0.42136300143291344. **This confirms `docs/46` §10 amendment 2's
     adjudication on its own terms rather than importing it.**
  2. `16.7754 / 39.8123` = **0.42136224232209646** → **0.4214** at 4 d.p., versus the superseded
     0.4214751420286394 → 0.4215. **§4.1's `×0.4214` is therefore CORRECT and was deliberately not
     touched.**
- **Nothing below HIGH was promoted to make the list look decisive**, and everything checked and
  found **still open** is recorded in §9.3 so a later session does not re-litigate it. Where two
  owners disagree the disagreement is printed rather than resolved (§9.4).
