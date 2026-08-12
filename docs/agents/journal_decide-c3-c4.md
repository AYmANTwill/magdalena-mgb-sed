# Journal — decide-c3-c4

GOAL: adjudicate three lenses (ratio-cancellation, alpha-role, C4-feasibility) into ONE
decision; write it as `docs/43_c3_c4_gate.md`; append a dated amendment A2 to `docs/37`
if the decision reclassifies the residual; apply `docs/40 §8.2`'s paste-ready corrections
to `docs/37` if still unapplied; register C5 caveats.

I am deciding, not researching. Keeping C3 open is an allowed outcome.

## Checklist
- [x] 1. Read docs/00_INDEX, 37 (+A1, +A1.9), 40 (esp §8.2 + §0), 42 (G1–G9, §8, §9), 35 §5.4, three lens journals
- [x] 2. Restate the C3 residual precisely; map what each lens established about it — docs/43 §1
- [x] 3. Check whether docs/40 §8.2 corrections are already applied to docs/37 — they were NOT (§1 row 4, §2, §4 all still asserted the retired gate from the body; A1.7 item 5 had recorded them as "recorded rather than silently applied")
- [x] 4. Record the DECISION in this journal BEFORE writing it into any doc — Step 2 above
- [x] 5. Write docs/43_c3_c4_gate.md
- [x] 6. Append dated amendment A2 to docs/37
- [x] 7. Apply docs/40 §8.2 corrections to docs/37 — five places, strike-through + pointer
- [x] 8. Register C5 caveats — docs/43 §5.1–§5.4

## Log

### Step 0 — journal created
Files I am permitted to touch: `docs/43_c3_c4_gate.md` (new), `docs/37_c3_closure.md`
(A2 + docs/40 §8.2 corrections), this journal. Nothing else.
Explicitly NOT touched, though lens 3 asks for it: `docs/42` §9 (the amendment slot). Its three
amendments are recorded in docs/43 as a **blocking precondition on C4's start**, to be registered
by whoever owns that file.

### Step 1 — state read (checklist 1 DONE)
- `docs/00_INDEX.md` (whole), `docs/37_c3_closure.md` (whole, 962 lines incl. A1 and **A1.9**),
  `docs/40` §8 + §9 citation table, `docs/42` §6 (G1–G9) + §8 + §9, `docs/35` §5.4.
- The three lens journals in full: `journal_adj-ratio.md`, `journal_adj-alpha-role.md`,
  `journal_adj-c4-feasibility.md`.

**Load-bearing thing the task brief did not carry:** `docs/37` **A1.9** (written later the same
day than A1) already **withdrew the direction** of the "1.03 – 2.27× under-erosive" residual. The
brief states the replacement test "FAILS: the model is UNDER-EROSIVE by 1.03-2.27x". A1.9 supersedes
that: clause 4′ → 4″, status **NOT ESTABLISHED**, residual direction **UNKNOWN** across
2.27× low … 1.49× high, because Leg A compared a MUSLE sum (SWAT Ch. 4:1 calls it a sediment
*yield*) against a RUSLE *gross erosion*. I decide on A1.9's state of the record, not the brief's.

### Step 2 — THE DECISION, recorded BEFORE writing it into any document
**I am recording this decision here first, and I am stating so explicitly, per the run rule. No
headline number was moved to reach it and none is moved by it.**

> **DECISION: `C3-STAYS-OPEN-C4-PROCEEDS-CONDITIONALLY`.**

Reasoning, compressed (the full form goes into `docs/43`):

1. **What reclassifies, with evidence.** The **LEVEL** component of the C3 residual is reclassified
   from *defect* to *calibration target*. Evidence: lens 2's primary-source re-extraction —
   Fagundes (2018) eq. 11 defines α, β as *"coeficientes de ajuste … calibrados automaticamente"*,
   in the MOCOM-UA vector, fitted per sub-basin **and per calibration dataset**, and the same
   sub-basin in the same experiment returns α values differing by median 1.28× and up to **7.78×**
   according only to which observed dataset was the target. A quantity the transposed method
   defines as free is not a defect of the model when it is left unfitted. `docs/42` §3.1 closes the
   argument from the other side: α, C level, LS level, K unit system, volume convention, P, FG are
   one identifiable product Π (cond = inf), so the level residual has **no separate existence** —
   it *is* Π, and Π is exactly what C4 fits. This is a reclassification, not a tolerance.
2. **What does NOT reclassify, and is why C3 stays open.** A scalar absorbs a level; it cannot
   absorb a structure (`docs/42` §1). Three structural residues survive the reclassification:
   (i) the LS *formulation* difference is level **+ slope-dependent shape** — G4.1 can only detect
   it, never fix it, and the C3.1 decision (`docs/35` §9.3) is still unmade, so clause 2 ("no
   decision left unresolved") still fails **in a known direction**;
   (ii) lens 1 measured the residual's per-station heterogeneity at I² 96 – 99.2 %, τ 2.03 – 3.40×,
   18/24 station-cells with CIs excluding 1 — not a constant, therefore not fully absorbable;
   (iii) the peak deficit is period-dependent (`R_AMS` 0.808 vs 0.686 ⇒ ×1.096), a structure in the
   one dimension C5's headline lives in.
3. **Clause 3 (audit) is now PARTIAL, not met.** The three lenses did adversarially audit
   `docs/35` §6.1 (falsified), `docs/42` §4.1/§4.2 (CAL 13 → CAL 8; k_min 0.0096 → 0.0209/km) and
   `docs/37` A1.3.4 (comparison-basis artifact). **`docs/41`'s C rows remain unaudited**, and lens 3
   measured that G3.1 cannot self-check them (min detectable class-C error ~4.2× on the CAL 8,
   against a revision of ×1.2043). So the clause is not met.
4. **Clause 4″ is still NOT ESTABLISHED.** A1.9's resolver step (1) — pin in writing, with
   citations, which quantity the per-pixel MUSLE sum is — has not been done. I decline to do it
   here: it is research, it is outside my remit, and the reading that would settle it favourably
   (reading B) is the one A1.9 refused **because** it flatters the result. I will not adopt it by
   the side door.
5. **Therefore CLOSED is unavailable.** Closing would require retiring a **third** successive
   level clause (SDR → 4′ → 4″) and calling the retirements a pass. `docs/40` §8.1 and A1.2 both
   forbid exactly that. Retiring is neither a pass nor a fail.
6. **BLOCKED is also wrong.** No lens supports it (NO / PARTIALLY / PARTIALLY), `docs/37` A1.6
   already grants C4 permission to run while C3 is open, and C4's own outputs — G1.2's `k̂` and
   G3.1's `c_B` — are the *only* named routes to the first independent evidence this project would
   ever have about channel deposition and the Bare class, i.e. two of the things keeping C3 open.
   Blocking C4 blocks the cheapest route to closing C3.

**Disclosure of arithmetic done during deliberation, before this decision was written:** I computed
the β-band consequence for the C5 caveat — `1.9545^0.90 = 1.828`, `1.9545^1.30 = 2.390` from lens
1's registered `basin_Qsur_ratio_primary` and the `docs/35` §6.3 β band 0.45–0.65 (exponent 2β).
It is a caveat input, not a headline move, and it did not select the decision. Recorded here rather
than presented as if it came after.

### Step 3 — docs/40 §8.2 corrections: status checked, then applied (checklist 3, 7 DONE)
**They were UNAPPLIED in the body.** `docs/37` A1.7 item 5 had recorded them ("Recorded rather than
silently applied"), and A1's "nothing above this line is rewritten" rule was why. So a reader who
never reached A1 would still have found, in the body: §1 row 4 asserting the SDR gate as NOT MET;
§2's "So `SDR = outlet / gross` must be < 1" (false for the quantity computed); §2's three
requirement rows; §4's "residual is 1.93 – 14.8×"; §4 residual 3. That is exactly what docs/40
warned about.

**Method chosen, recorded before applying it:** strike-through + dated pointer, nothing deleted.
This satisfies docs/40's concern and A1's no-rewrite rule at once — every original sentence stays
readable and marked, so the record of what was believed survives while the retired claim cannot be
quoted as live. Five places, enumerated in the new `docs/37` A2.7.

**One deliberate non-application:** `docs/40` §8.2's own replacement row (clause 4′, "under-erosive
by 1.59 – 2.74×") is **NOT** pasted, because docs/40's own §0 and `docs/37` A1.9 re-opened it. I
pasted the *retirement* half and pointed at A1.1/A1.9 for the replacement. Same for §8.2's residual-3
wording: adopted, minus its "1.59 – 2.74×" figure.

### Step 4 — numbers verified before quoting (arithmetic, not new science)
```
1.9545^0.90 = 1.8278   1.9545^1.12 = 2.1182   1.9545^1.30 = 2.3897   (primary, exponent 2*beta)
3.3598^0.90 = 2.9763   3.3598^1.12 = 3.8857   3.3598^1.30 = 4.8329   (sensitivity)
exp(0.02092*60.4)  = 3.538   CAL 8 deposition bound over its own span
exp(0.00303*348.4) = 2.874   CAL 8 + ARRANCAPLUMAS
exp(0.00216*348.4) = 2.122   all 18 (G1.2 residual test), reproduces docs/42's 2.11x
0.465/sqrt(8)  = 0.1644 ln -> x0.7245 .. x1.3802  = +-38 % at 95 % on the Pi level
0.465/sqrt(13) = 0.1290 ln  (what docs/42 assumed)
2.2915/1.096 = 2.0908 ; 3.9725/1.096 = 3.6245   (peak-corrected simulated contrast)
```
Everything else in `docs/43` and `docs/37` A2 is quoted from a lens journal or a prior numbered doc.

### Step 5 — files written (final)
- `docs/43_c3_c4_gate.md` — NEW. The adjudication: decision, evidence, C4 contract, C5 caveats.
- `docs/37_c3_closure.md` — **Amendment A2** appended (A2.1–A2.7) **plus** the docs/40 §8.2
  corrections applied in place in §1/§2/§4 as strike-through + pointer. A1, A1.9, §3, §5, §6 and the
  headline verdict line untouched. 987 -> 1,238 lines.
- `docs/agents/journal_decide-c3-c4.md` — this file.

**NOT written, and why:** `docs/42` §9 (lens 3's three amendments) — a frozen pre-registration and
not a file this task names; recorded as a **blocking precondition on C4's start** in `docs/43` §3.1.
`docs/00_INDEX.md`, `docs/35`, `docs/40`, `docs/41`, `notebooks/`, `src/`, `tests/` — untouched.

### Disclosure
No frozen artifact opened or written (`sim_calibrated_v2/{h2e_drivers.npz, parameters_H2E.csv,
q_gauge_H2E.npz}`). No simulation run. No calibration launched. No wide forcing CSV read. No git
command issued. No headline number moved. Nothing backdated. No gauge-referenced t/km2/yr quoted.
Uncited quantities named as such and used to pass or fail nothing: the retired 0.05-0.30 SDR band
and its implied k ~ 0.0020-0.0032 /km; the ENSO-neutrality of CAL 2012-14.
