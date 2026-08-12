# Journal: adversarial refutation of "deposition axis pre-satisfied" finding

Agent: refute-prereg-integrity. Started 2026-08-11.
Posture: default is that the finding is WRONG; trying to prove it.

## Finding under test
Title: "The deposition axis is registered so that it cannot block adoption, and docs/35's
countervailing rule is not imported."
Anchor: docs/45_c4_preregistration.md:155.

## Plan
1. Read docs/45 lines 120-170, 400-450 (k=0.0 fix, G1.2 2.12x floor).
2. Read docs/42:460-500 (G5 definition).
3. Read docs/35:600-650 (the "low teens = failure" registered rule).
4. Read docs/37:900-920 (alpha 6.83-8.73 / 7.921 back-solve).
5. Check whether docs/35 §9.2 rule appears in any §6 outcome anywhere.
6. Check file birth/commit times for pre-registration ordering claims.

## Log

## What I actually checked (all in docs/45_c4_preregistration.md unless noted)

1. **Citations are accurate.** :531 (FAIL—STRUCTURE), :428 (G1.1), :429 (G1.2), :433 (G3.1),
   :436 (G4.1), :221 (§2.5 budget row), :553-555 (§6.3) all say what the finding quotes.
   Doc is committed and clean (`865f674 c4.2: freeze the sediment-calibration pre-registration`);
   no working-tree modification.

2. **Count check — "four of the nine ACTION cells prescribe a refit" is 3, not 4.**
   Grep for `refit` over the nine adoption-blocking structure guards (G1.1 G1.2 G2.1 G2.2
   G3.1 G4.1 G7 G8 G11): hits only at :428 (G1.1 "and refit") and :433 (G3.1 "and refit");
   G1.2 (:429) inherits by "same action as G1.1". **G4.1 (:436) never says refit** — its text is
   "Fix the LS2D field, or adopt a steepness-dependent correction with its derivation", which is
   what the finding itself quoted. The other six ACTIONs are report/attribute/STOP only.

3. **The decisive internal gloss is the adjacent FAIL—NUMERIC row (:532).** It licenses
   "**one named remedial route from the failing guard's ACTION column**" and in the SAME cell
   denies "**NOT** a widened box, **NOT** an added parameter, **NOT** a second search."
   So the document itself already fixes the operative meaning of invoking the ACTION column at
   verdict time: naming a route, not executing one. `grep` shows no other gloss anywhere
   (docs/42, docs/43, docs/31 contain no "remedial route"/"ACTION column"/"second search" text).

4. **Every refit-bearing ACTION is independently blocked twice, so the alleged licence cannot be
   exercised at all.** §6.3 (:553-555) forbids both "a second search" AND "an edit to ... this
   document's §2–§6". Each ACTION requires a §2.3 edit:
   - G1.1/G1.2 "add a named transport sink" vs §2.3 :130-132 **"REGISTERED. ... FIXED AT
     k = 0.0 /km ... and it is NOT FITTED", `SedParams.tau_delivery_days = 0`**.
   - G3.1 "revise that class's C in urh_cp_factors.csv" vs §2.3 :178 fixed factor table,
     `C` at `cp_revision` docs/41 central ×1.20427.
   - G4.1 "fix the LS2D field" vs §2.3 :177 `ls2d_factor` 1.000 × 1.000 — and G4.2 (:437) makes
     "C4 changes `ls2d_aggregation`/`ls2d_resolution` to move the level" an explicit FAIL.
   Header :10 repeats it: "nothing in §2–§6 may be edited after a number it judges has been
   computed."

5. **The harm chain is cut in the very row the finding cites.** :531's "does not license" column:
   "**The fit is NOT adopted and C5 does not run on it.**" And ADOPT (:530) condition (4) requires
   "**every structure guard passes**". So no Π, load or ENSO contrast can reach C5 through a
   FAIL—STRUCTURE verdict, refit or no refit.

6. **The doc pre-authorised the one k>0 move it will allow, and labelled it not-a-search**
   (§2.3 :164-168): Π re-solved once at `k_hi`, "It adds **no free parameter** ... a
   one-dimensional level solve, not a search." The document anticipated the deposition direction
   and gave it a bounded non-search form; the full G1 remedy stays outside.

7. **"The most likely failure mode" is uncited and points the other way.** `grep -i "most likely"`
   returns exactly one hit, :407: "**The α-magnitude guard is blind to the single error C4 is most
   likely to make**" — context :403-406 is a **level** error (silent deposition omission landing
   α at 6.83–8.73, overlapping the flattering reading-B α 7.92–8.86). §5.3 :493 and docs/42 :301
   both state the level "leaves no fingerprint, ever". The doc's registered power numbers make
   guard-firing marginal, not likely: :126 fit-set `k_min` 0.0209 /km ⇒ no sink weaker than
   **3.54×** detectable; :162 all-18 bound ≈ **2.12×** over 348.4 km "at best" (k_min 0.00216 /km)
   against the UNCITED SDR-implied k ≈ 0.0020–0.0032 /km — i.e. right AT the detection floor;
   :435/:493 G3.1's minimum detectable class-C error **×4.2** on CAL 8; :444 G11 "**weak by
   construction**". G1.2 (:429) registers non-firing as "**NOT A PASS**" precisely because of this.

8. **Lexical check:** "refit" in this document does not mean "second search" — :445 G12 mandates
   8 LOO **refits** and budgets them as "cheap: the surface is precomputed per station".

## Verdict
REFUTED. The narrow surviving point is a drafting asymmetry, not a licence: FAIL—NUMERIC repeats
the "NOT a second search" denial in its own row and says "one **named** remedial route", while
FAIL—STRUCTURE says "with that guard's registered ACTION **taken**" and its does-not-license cell
omits the denial. A one-clause cross-reference to §6.3 in :531 would close it. Recommend as an §8
amendment note at most; not a finding about the registration's integrity.

### 2026-08-11 — what I actually checked

**Citations verified in place**
- `docs/45`:128-132 — k FIXED at 0.0 /km, NOT FITTED, `SedParams.tau_delivery_days = 0`. TRUE.
- `docs/45`:**154** (finding says 155, off by one) — "This model asserts SDR = 1.0 between
  hillslope and station." TRUE, it is in the frozen registration.
- `docs/45`:429 — G1.2 row. TRUE. **But**: the "≈ 2.12× over 348.4 km at best" text is in the
  **ACTION ON FAILURE** column, not the **threshold ⇒ FAIL** column. The FAIL threshold is
  *"the 95 % station-bootstrap interval for `k` lies entirely above 0"* — a significance test,
  not a magnitude bar. The same cell registers **"If neither G1.1 nor G1.2 fires, that is NOT
  A PASS"**. The finding calls 2.12× "G1.2's own registered detection floor" and treats it as
  the bar k must clear to fire. That is a misread of which column it is in.
- `docs/42`:475-485 — G5 as quoted. TRUE.
- `docs/35`:627-631 — inside **§9.2** (starts :551). Rule quoted correctly.
- `docs/37`:907 — TRUE, but it says the deposition-free band (6.83–8.73) and the reading-B α
  (7.92–8.86, :984) **overlap**; they are two different back-solves. The finding merges them
  ("6.83–8.73 ... back-solved 11.8/1.4897 = 7.921"). 11.8/1.4897 is the reading-B number.

**Arithmetic I ran** (reproduces the doc's own floors, so the doc's numbers are sound):
```
exp(0.00216*348.4) = 2.1224   (docs/45 says 2.12x)   all-18
exp(0.0209 *60.4 ) = 3.5338   (docs/45 says 3.54x)   CAL-8
k_min 0.00216/km as whole-basin delivery over the registered 1425.9 km max path = 0.0460
SDR 0.30 -> k 0.000844/km -> signal over 348.4 km = 1.342x   (< 2.12x floor)
SDR 0.05 -> k 0.002101/km -> signal over 348.4 km = 2.079x   (< 2.12x floor)
deposition-free alpha at ADOPTED cp_revision 299.5387: 5.67-7.25  (NOT 6.83-8.73, which is
  the SUPERSEDED 248.730 level -- docs/37:748 says 248.730 is superseded wherever quoted)
```

**Ordering check (pre-registration discipline)** — no C4 fit artifact exists anywhere:
`c4_parameters.csv` and `c4_grid.csv` are absent; `git log docs/45` = one commit,
865f674 2026-08-11 20:13:22. So the SDR=1.0 sentence was written **before** any α existed.
That is the *required* order for G5 leg 1 option 2, not evasion. Writing it after seeing
α̂ ≈ 8 is what would have been the violation.

**The supersession chain the finding says is missing** — it is not missing, it is explicit:
- `docs/42` §8.1 "docs/35 §6 is retained, not replaced": §6.1's band "is **necessary and not
  sufficient**: it cannot see a deposition-free fit. **G5** supplies the missing condition."
- `docs/42` G1 header: "*(replaces the blinded job of `docs/35` §6.1)*".
- `docs/37` **A1.6 item 1** (dated 2026-08-11) restates §5.1's warning **as G5's precondition**,
  and A1.6's preamble says "C4 is no longer blocked: `docs/42` supplies the test §5.1 could
  only warn about." `docs/37` A1.9.4 item 2: "**G5 is not softened by A1.9.**"
- `docs/45` §1 item 1 imports exactly that: held to `docs/42` G1–G9, "never to `docs/35` §6
  alone (`docs/37` A1.6)". §7.2: docs/45 does **not** edit docs/35 or docs/42.
So the "must be treated as a failure" wording was converted to a precondition by two frozen
prior documents; docs/45 followed the chain rather than dropping a rule.

**G1.1 exists and the finding never mentions it.** `docs/42` G1 note (2): the pair form's
k_min is **0.00119 /km** (= 1.51x over 348.4 km, whole-basin DR 0.183), with an independent
magnitude threshold `D_pair > +0.658` that is invariant to all seven confounded scalars.
It is separately listed in `docs/45` §6.1 ADOPT condition (4).

**Implementation check** — `src/mgb_transport.py`: `TransportParams.k_dep`, `dep_mode='per_km'`,
`d_i = 1 - exp(-k_dep*reach_km)`, retention `exp(-k_dep*path_km)`, `_broadcast` allows per-reach
k. So §2.3's registered "re-solve Π once at k_hi and report the two levels as a pair" is an
executable run, as the doc claims.

**Blocking check** — `docs/45` §6.1:
- ADOPT condition (4) names **G1.1 and G1.2** among the guards that must pass.
- FAIL — STRUCTURE names G1.1/G1.2 and says "**The fit is NOT adopted and C5 does not run on it.**"
- FAIL — RAILED/HARD STOP lists "**a G5/G6/G9 reporting leg missing**", so leg 2 does block,
  and leg 2 requires G1.2 to have been **run**.
⇒ "cannot block adoption" is false as written.

**Internal wrinkle I found (not the finding's claim, but adjacent):** G1.2's ACTION cell says a
non-firing is "**NOT A PASS**", while §6.1 ADOPT condition (4) requires "every structure guard
**passes** — ... G1.2 ...". Read literally the two cannot both be satisfied. Worth flagging to
the owner as an ambiguity, but it cuts *against* the finding, not for it.

**VERDICT: refuted.** The narrow surviving part is in `corrected_claim` of the structured output.
