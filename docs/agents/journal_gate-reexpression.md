# Journal - agent slug `gate-reexpression` (T4 = docs/47 B2)

Task: re-express the C4.3 gate in a unit that survives C3.1.
OWN (write): `docs/45_c4_preregistration.md` §8 (append a FURTHER dated amendment after
the ones already there) AND this journal. Nothing else.

## 00 - 2026-08-12 - opening

Created this journal as first action, before reading anything.

Reading order I will follow: CLAUDE.md, docs/00_INDEX.md, docs/47, docs/46 (§1.0 §1.2 §2.0
§3.1 §3.3 §4.2 §4.3 §4.4 §5 §6 §7.3 §9 §10), docs/51, docs/52, docs/53, then docs/45 (whole,
especially §2.1 §2.3 §2.4 §3 §6.1 §6.3 §7 and the CURRENT §8 in full), docs/35 §6.1 + §9,
docs/37 A1.6 / A3, docs/42 §3.1.

Constraints I am holding in front of me:
- Do NOT widen the box; must DEMONSTRATE the restatement forbids exactly what the original did.
- Do NOT evaluate the objective / run a fit / quote an alpha-hat.
- Do NOT invent a numeric threshold: every number = arithmetic consequence of a registered
  number and the adopted f_LS, arithmetic shown.
- Do NOT reconstruct a materiality bar.
- docs/35 §6.1's 3.9/35.4: PROPOSE ONLY, verbatim text inside my docs/45 §8 amendment.
- Must state plainly whether the re-expression FIXES or merely RELABELS docs/47's
  FAIL-RAILED / FAIL-NUMERIC pre-computability problem.
- Carry docs/47 O5 unchanged.

## 01 - 2026-08-12 - what I read, in order

CLAUDE.md, `docs/00_INDEX.md` (line counts only, to size the corpus), `docs/47` in full,
`docs/46` §6 in full (§6.1 discriminator, §6.2 A1-A6, §6.3 B1-B5, §6.4 cost), `docs/45` in full
(all 1209 lines, including the CURRENT §8 = Amendments 1, 2, 3 and §8.4 disclosure),
`docs/35` §6.1-§6.3 and §9.4.5-§9.4.8, `docs/51` §6.2-§6.3, `docs/52` §7.

Key facts I build on, each read on disk, not carried from the brief:

1. `docs/45` §7.1 registers, among the FIXED not-fitted factors, **`f_LS` 1.000**. §2.3's
   fixed-factor table registers `ls2d_factor` (aggregation x resolution) = 1.000 x 1.000,
   **UNVALIDATED**. So the registered configuration's LS level factor is 1.000 *by registration*.
2. `docs/45` §1 item 4 already registers **Pi = 5,164.42** at the adopted C, unfitted, with the
   decomposition `Pi = alpha * f_vol * f_K * f_LS * C_mult * P * FG` and alpha = 11.8. The Pi
   anchor is ALREADY IN THE DOCUMENT - I introduce no new constant.
3. `docs/45` §2.5 registers the alpha axis as **71 points, log-spaced on [2.0, 30.0], step
   x1.03945**. That grid is a grid on the ENGINE's alpha at the registered configuration.
4. `docs/35` §6.1's caveat (added 2026-08-11, FROZEN) says in registered text: *"every number in
   the table below must be **divided** by that bracket before it is compared with an alpha fitted
   on **our** LS."* So the DIVISION RULE for the docs/35 band is already registered, and dated
   before this run. §9.4.5 prints the rescaled arithmetic, says it re-registers nothing, and
   explicitly awaits a PROPOSAL from the B2 owner - me.
5. `docs/51` §6.3 **P1**, verbatim: *"The box `[2.0, 30.0]` and the stop 3.9 were registered at
   `f_LS = 1`. Any `f_LS != 1` **moves them**."* That is the Pi-invariant convention stated as a
   principle.
6. BUT `docs/51` §6.2, `docs/46` §6.2 **A4** and `docs/47` §5.2 all do the arithmetic the OTHER
   way - they hold the box literal on the post-swap engine alpha and rescale alpha-hat by 1/f.
   A4's own derivation: *"30.0 / 3.9768 = 7.543"*. This convention split is what I must settle.
7. `docs/45` §8.2.7 item 2 RECOMMENDS a fresh pre-registration for exactly my job, and item 4
   registers a route rule: changing §6.1's eight ADOPT conditions, §3.2's bar, §2.1's boxes,
   §3.4's fit set, §3.5's windows or §2.5's budget/seeds CLOSES the §8 route. I must engage with
   this head on, not around it.

## 02 - 2026-08-12 - the arithmetic, measured

Scripts `<scratchpad>/t4_gate.py`, `t4b.py`, `t4c.py`, run with `python3.10`. Verbatim output
below, trimmed to the lines I use.

```
k0  = f_vol*f_K*f_LS(=1.000)*C_mult*P*FG = 437.66113721058014      (C_mult 1.20427 as printed)
Pi(alpha=11.8) = 5164.401419084846   vs registered 5164.42   rel err 3.5978706523513363e-06
k0 with C_mult 1.204272539864846      = 437.66206025951175  -> Pi(11.8) 5164.412311062239
k0 back-solved from the registered Pi  = 437.6627118644068
max relative spread across the three k0 = 3.597883597084349e-06

Pi_lo = 2.0*k0  = 875.3222744211603
Pi_hi = 30.0*k0 = 13129.834116317405        Pi_hi/Pi_lo = 15.0 exactly (True)
alpha rail band = [3.4000000000000004 , 28.6]      (5 % of range = 1.4000000000000001)
Pi    rail band = [1488.0478665159726 , 12517.108524222593]
  -> back to alpha: 3.4000000000000004  28.6      EXACT: True True
grid step alpha (71 log pts) = 1.0394444954338562 ; grid step Pi = 1.0394444954338562 identical: True

the SAME Pi box in engine-alpha units:
  f_LS=1.0                  alpha in [2.0 , 30.0]                 rail [3.4 , 28.6]
  f_LS=0.2514648985839397   alpha in [7.953396323950136 , 119.30094485925204]
                            rail  [13.520773750715232 , 113.73356743248695]
  f_LS=0.43194417543884817  alpha in [4.630227963991024 , 69.45341945986537]
                            rail  [7.8713875387847425 , 66.21225988507166]

docs/35 §6.1 in Pi, the two readings:
  5.9   Pi(literal)=2582.200709542423    Pi(divided)=649.3328395484625   alpha_ours 1.4836429016452444
  11.8  Pi(literal)=5164.401419084846    Pi(divided)=1298.665679096925   alpha_ours 2.9672858032904887
  23.6  Pi(literal)=10328.802838169691   Pi(divided)=2597.33135819385    alpha_ours 5.9345716065809775
  35.4  Pi(literal)=15493.204257254536   Pi(divided)=3895.997037290775   alpha_ours 8.901857409871466
  3.9   Pi(literal)=1706.8784351212626   Pi(divided)=429.220012582882    alpha_ours 0.9807131044773649
  docs/35 lower stop divided 429.220012582882 < Pi floor 875.3222744211603  -> INOPERATIVE
  docs/35 upper stop divided 3895.997037290775 is INSIDE the box
  window if BOTH applied: Pi [1488.0478665159726 , 3895.997037290775] == alpha_ours [3.4 , 8.901857409871466]
  today's literal window : alpha_ours (3.9 , 28.6]  -> Pi (1706.8784351212626 , 12517.108524222593]

direction cross-checks:
  2.0*f = 0.5029297971678794    30.0*f = 7.543946957518192
  2.0/f = 7.953396323950137     30.0/f = 119.30094485925204
  docs/46 A4: 30.0/3.9768 = 7.543753771876887 ; 30.0/2.3151 = 12.958403524685759
              30.0/(1/f)  = 7.543946957518191 ; 30.0/(1/fh) = 12.958325263165444
  A4 lower  : 2.0/2.3151 = 0.8638935683123838 ; 2.0/3.9768 = 0.5029169181251257
  ratio form: 5.9/11.8=0.5  23.6/11.8=2.0  35.4/11.8=2.9999999999999996  3.9/11.8=0.33050847457627114

the pre-computed profile in Pi (f_LS = 1.000):
  beta 0.45  F_search argmax alpha 0.258 -> Pi 112.91657340032968   F_report 0.050 -> Pi 21.88305686052901
  beta 0.56  F_search argmax alpha 0.625 -> Pi 273.53821075661256   F_report 0.117 -> Pi 51.206353053637876
  beta 0.65  F_search argmax alpha 1.289 -> Pi 564.1452058644378    F_report 0.325 -> Pi 142.23986959343856
  best Pi_hat 564.1452058644378 ; shortfall to Pi floor 1.5515903801396431x ;
                                   to rail-trimmed floor 2.6377036462373935x
  F_report argmax beta 0.65 : shortfall to floor 6.153846153846153x
  implied level (geo-mean of station LOG-MEAN ratios, beta 0.56) alpha 1.211 -> Pi 530.0076371620125
        shortfall to floor 1.6515276630883566x
  implied level (geo-mean of station ARITHMETIC ratios, beta 0.56) alpha 0.897 -> Pi 392.5820400778904
        shortfall to floor 2.229654403567447x

Delta_shape = 0.1299456916752905 ; exp(+D) = 1.1387665371423883 ; exp(-D) = 0.8781431201072979
  after the maximal favourable shape lift the Pi floor is STILL short by 1.3625184175442946x
  and the rail-trimmed floor by 2.316281309825301x
  on the log-mean implied level: still short by 1.450277655007924x

post-swap, the two conventions:
  alpha_dg = 0.258/f = 1.0259881257895676 ; 0.625/f = 2.4854363512344175 ; 1.289/f = 5.125963930785862
  (i) box held literal on engine alpha: railed True / True / False ; >3.9 False / False / True
      -> TWO of three rail, top corner clears     == docs/46 §6.3, docs/51 §6.2, docs/47 §5.2
  (ii) Pi-invariant, Pi box [875.3222744211603 , 13129.834116317405]:
      railed True / True / True                   -> THREE of three rail, NO corner clears
  (i)'s Pi content of the box AFTER the swap = [220.11282696558052 , 3301.692404483708]
      = the anchored box x 0.2514648985839397   <-- the box's Pi floor drops x3.977 on a swap
```

## 03 - 2026-08-12 - the decision, and why

**ROUTE A: re-express the gate in Pi.** Route B (re-register the alpha box against the adopted
`f_LS`) is rejected as the PRIMARY unit because it does not survive C3.1: every alpha number
would have to be re-derived at every future `f_LS`, and A3 records the adopted `f_LS` as
DETERMINED and RECORDED but **NOT YET EXERCISABLE** (`ls2d_column` is still `"ls2d_hs"`, no
`V4_dg` column is committed), so route B would register numbers against a value the engine cannot
yet produce. Route B's *reporting* requirement (`f_LS` and its grade in the same table as any
alpha-hat, `docs/47` §6.2 item 1) is adopted IN ADDITION - complementary, not alternative.

**CONVENTION: (ii), Pi-invariant, anchored at the registered configuration `f_LS` = 1.000.**
Four grounds, in order of strength:
1. It is what `docs/45` itself registered: §2.5's grid is a grid on the engine's alpha, and §7.1
   registers `f_LS` = 1.000. The box's Pi content is `[2.0*k0, 30.0*k0]` **as registered**.
2. It is the only convention under which the box is a GATE. §6.1 ADOPT condition (2) makes
   railing at a box edge a FAIL, so the edges are thresholds, and a threshold whose content
   multiplies by 1/f_LS when someone swaps an LS field is not a threshold. Reductio: under (i) an
   LS field 100x smaller would drop the box's Pi floor 100x and let any fit in.
3. It relaxes nothing. At `f_LS` = 1.000 - the only configuration the engine can run today - the
   restatement is the IDENTITY, verified: same interval, same 71 log points, same x1.0394444954
   step, same rail band recovered to the last bit (3.4000000000000004 and 28.6).
4. Convention (i) relaxes the live edge by x3.9767 on a swap (Pi floor 875.32 -> 220.11) and is
   measured to be exactly the mechanism that produces the corpus's only "one corner clears".
   Adopting (i) would be relaxing a frozen gate, post-profile, in the direction that lets the fit
   pass - `docs/45` §2.4's forbidden move.

**Direction, stated once so I cannot lose it:** `Pi = alpha * k0 * f_LS`. A SMALLER LS field needs
a LARGER alpha for the same Pi, so `alpha` scales as `1/f_LS`. Therefore:
- the same Pi box, in engine-alpha units on a field with factor `f`, is `[2.0/f, 30.0/f]`;
- `docs/35`'s SOURCE-LS numbers, expressed in OUR engine-alpha units, are `x f` (11.8*f = 2.967) -
  which is exactly `docs/35` §6.1's own registered instruction to **divide by the bracket**
  (dividing by 1/f == multiplying by f). Both directions cross-check against `docs/46` A4's
  `30.0/3.9768 = 7.543` (mine: `30.0*f = 7.543946957518192`).

**What I do NOT enact:** anything about `docs/35` §6.1's 3.9 / 35.4. PROPOSED only. Reason
recorded before I wrote a word of the proposal: applying `docs/35`'s own division rule moves BOTH
stops down by x3.9767, which LOOSENS the floor (3.9 -> 0.9807 in our alpha units) and TIGHTENS
the ceiling (35.4 -> 8.9019). The loosened floor is the LIVE edge (the profile puts the optimum
at the bottom), so enacting it myself would be relaxing a hard stop after seeing the surface.
`docs/45` §6.1 forbids it anyway - a session that hits a stop may only PROPOSE.

**Net effect on the admissible window, measured (this is why the proposal is not a relaxation
overall):** today's literal reading admits alpha_ours in (3.9, 28.6]; with `docs/35`'s division
rule applied the window is [3.4, 8.901857409871466] and the lower stop becomes INOPERATIVE
because the box floor binds first (Pi 429.22 < 875.32). The admissible set SHRINKS.

## 04 - 2026-08-12 - the sentence I was told to get right

**The re-expression does NOT fix the FAIL-RAILED / FAIL-NUMERIC pre-computability problem. It
RELABELS it, and in the Pi coordinate it gets WORSE, not better.** Measured: Pi_hat at the most
favourable G2.3 corner is 564.1452058644378 against a Pi floor of 875.3222744211603 - short by
x1.5515903801396431, and short of the rail-trimmed floor by x2.6377036462373935 - in EVERY
G2.3-admissible beta, at EVERY `f_LS`, because both Pi_hat and the Pi box are `f_LS`-invariant.
F_report's -0.305...-0.350 against the bar's -0.26 is an objective value and no re-expression of
the alpha axis touches it. And the corpus's only "may clear" corner (`docs/47` §5.2, `docs/51`
§6.2, `docs/46` §6.3) is measured to be an artifact of convention (i): it exists only because the
box's Pi floor drops x3.9767 on the swap. Under the invariant reading, **three of three corners
rail and no corner clears.**

O5 carried unchanged. New, and it is a bound not a resolution: for a fleet log-mean level,
`|ln(Pi_hat shift)| <= Delta_shape` = 0.1299456916752905, so the maximal favourable shape-driven
lift is x1.1387665371423883 - smaller than the x1.5515903801396431 gap it would have to close
(and smaller than the x1.6515276630883566 gap on the log-mean implied level itself). Derivation:
station s's simulated flux under the new field is `Pi * (h_s / f) * base_s` with
`h_s = E_s(V4)/E_s(V0)` and `f` the basin factor, so `Pi_s*(V4) = Pi_s*(V0) * exp(-ln(w_s ratio))`
and `|mean_CAL ln(w_s ratio)| <= max_CAL |ln(w_s ratio)| = Delta_shape`. Labelled as a bound on
the LEVEL term: F_search / F_report argmaxes are not exactly a fleet log-mean level, so **O5
stays OPEN and "may clear" remains the strongest statement about the objective**.

## 05 - 2026-08-12 - what I wrote, and the mechanical verification

Appended **`## 8.5 - Amendment 4 - 2026-08-12`** to `docs/45_c4_preregistration.md`, after §8.4,
subsections 8.5.1 - 8.5.14. File **1209 -> 1850 lines**.

Verification from executed output, not from an exit code:
```
CRLF 0  CR 0  LF 1850                      (docs/45 was pure LF before; preserved)
prefix byte-identical: True                (bytes 0..1209-lines unchanged - §1-§7 and §8.1-§8.4 untouched)
markdown tables: 30  column mismatches: 0
odd ~~ parity lines: []                    (no strike-through spans a line break; I struck nothing)
all §8.5.x cross-references defined; MISSING: []
headings 1213 / 1227 / 1238 / 1259 / 1297 / 1333 / 1376 / 1424 / 1600 / 1674 / 1708 / 1737 / 1768 / 1804 / 1816
PROPOSED block delimited at :1457 ("PROPOSED AMENDMENT TO docs/35 §9 - NOT ENACTED HERE")
                        and :1596 ("END OF PROPOSED docs/35 §9.5 TEXT. NOT ENACTED.")
```
A byte copy of the pre-edit file is in `<scratchpad>/45_before.bak`.

**I struck NOTHING in §2-§6, deliberately.** The restatement is the identity at the registered
configuration, so no body number is superseded: §2.1's `[2.0, 30.0]` and §6.1's alpha-hat-against
-3.9/35.4 remain correct as written. Striking correct text would have been the error.

**Ownership honoured:** I wrote §8 only, plus this journal. §7.1's card cell still says "THREE"
amendments and there are now four - **reported in §8.5.12 item 4, not fixed**, because §7 is not
mine. `docs/35` was read and NOT edited; the amendment text for it is a labelled PROPOSAL inside my
own §8.5.7.

## 06 - 2026-08-12 - things I rejected, recorded so they are not re-attempted

1. **Route B as the gate's unit** - rejected on measurement, not taste (journal §03): the adopted
   `f_LS` is NOT YET EXERCISABLE, and route B does not survive a future `cp_revision`,
   `k_unit_system` or `volume_convention` change either, whereas Pi survives all seven factors.
   Route B's *reporting* half is adopted as a companion.
2. **Provenance-correcting the docs/45 BOX** (i.e. treating `[2.0, 30.0]` as source-LS numbers
   because docs/31 and Fagundes' MOCOM-UA prior `[2.0, 25.0]` are source-formulation values, and so
   moving the Pi floor to 2.0*k0*f = 220.11282696558052). **REJECTED on three grounds:** it is
   incoherent with §2.5's registered grid (which is a grid on the engine's alpha at `f_LS` = 1.000);
   §2.1 registers the box as *"a SEARCH BOX, not a plausibility band"* and a search box has no
   external scale to be corrected to; and it drops the live edge by x3.9767 post-profile, which is
   §2.4's forbidden move and closes §8.2.7 item 4's route. **This is the single most tempting wrong
   turn in the task and it is the one that manufactures a pass.**
3. **Enacting the docs/35 division inside docs/45.** Refused: `docs/45` §6.1 permits only a
   PROPOSAL, and the change loosens the live edge.
4. **Inventing a "materiality" statement about the 3.6e-06 `k0` reproduction residue.** Refused
   (`docs/52` §7 item 2). I printed all three `k0` evaluations, registered the conversion as a
   FORMULA, and stated the residue is four orders below the smallest quantity anything turns on -
   without calling that a bar.
5. **Numbering my open items into `docs/47`'s O-register.** Refused - not my document. They are
   Q1-Q5 in §8.5.13, offered for numbering by that owner.
6. **Claiming O5 closed by the `Delta_shape` bound.** Refused. The bound is exact for a fleet
   log-mean level and `F_search`/`F_report` argmaxes are not that statistic. O5 stays OPEN and
   "may clear" remains the strongest statement.

## 07 - 2026-08-12 - final state

- **B2 is DISCHARGED.** The gate is registered in Pi, `f_LS`-invariant, identity at the registered
  configuration, with the exact conversion both ways and the demonstration that it forbids exactly
  what the original forbade.
- **C4.3 is STILL BLOCKED.** B1 has not landed (no committed `V4_dg` column; `docs/37` A3's ACT 2
  is not draftable), Branch B is MANDATORY (`Delta_shape` = 0.1299456916752905 > 0), and the
  pre-computed FAIL stands.
- **The pre-computability problem is RELABELLED, NOT FIXED**, and in Pi it is worse: three of three
  G2.3 corners rail, and the corpus's only optimistic corner is measured to be an artifact of the
  retired convention.
