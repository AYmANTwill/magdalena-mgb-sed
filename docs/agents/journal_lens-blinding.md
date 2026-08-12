# journal_lens-blinding.md

T6 ADVERSARIAL LENS: Was the blinding held?
Agent slug: lens-blinding. READ-ONLY except this file.
Opened 2026-08-12.

Prior/posture assigned: **the docs/52 bar-strike was reverse-engineered from the
Delta_shape result, and the "blinding" is a story told afterwards.** Try to prove it.

## 00 - plan
1. Timestamps + git inspection of docs/52, docs/53, docs/46 §10 amd 1, and the four journals.
2. Grep every journal/doc for a Delta_shape value/bound/estimate appearing BEFORE docs/52's decision.
3. Judge docs/52's four structural reasons for value-independence.
4. Test docs/52 §4's asymmetry claim as stated.
5. Check this run's writing (docs/37 A3, docs/45 §8, docs/54, amendments) for backwards reading.

## 01 - TIMESTAMP / ORDER EVIDENCE (all read-only)

`ls -la --time-style=full-iso` (local mtimes, 2026-08-11 unless noted):
```
22:54:39  docs/agents/journal_ls-freeze-decision.md   (docs/51's author)
[22:57:36 git commit d60d8d9 -- docs/51 lands in git]
23:09:40  journal_bar-eliminative.md
23:09:57  journal_bar-decision-theoretic.md
23:11:00  journal_bar-statistical.md
23:22:12  docs/52_materiality_bar_decision.md     <-- THE BAR DECISION
23:22:31  journal_bar-judge.md                    (19 s later; final entry)
23:42:59  docs/53_delta_shape_pretest.md          <-- Delta_shape COMPUTED (+20 min)
23:43:13  journal_delta-shape.md                  (14 s later)
23:44:40  journal_amend-46.md                     (docs/46 freeze + §10 amd 1)
[2026-08-12 06:28:10 git commit e5b3c8e -- 52, 53, 46, all 6 journals in ONE commit]
```
=> git gives NO intra-commit ordering (everything landed in e5b3c8e). The order rests on
mtimes + content cross-references. Both agree, and both are corroborated by CONTENT:
docs/53 cites docs/52 as already decided; docs/52 cites no value.

Integrity: `git diff --stat HEAD -- docs/52 docs/53` = EMPTY (neither touched since the
commit, i.e. not retro-edited by this run). docs/46: the committed file is a byte-exact
PREFIX of the disk file (`new.startswith(old)` = True), so §10 Amendment 1 (offset 98270 in
both) was NOT rewritten; T2a's Amendment 2 is a pure append.

## 02 - THE FINDING: bar-judge was NOT fully blind

`journal_bar-judge.md`: "Read: CLAUDE.md, docs/51 (full), docs/48 (full), docs/46 (full)..."
`git show e5b3c8e:docs/51...` lines 305-306 (committed 22:57:36, 25 min BEFORE docs/52):

    `Δ_shape ≤ ln 1.287 = 0.2524`; normalising the all-18 extremes (0.3687, 0.4745) on the
    basin joint factor 0.43194 gives 0.154. **It can land on either side of 0.1644 and must
    be computed, not inferred,**

and docs/51:463: "Bounds without it: `≤ 0.2524`, plausibly ~0.154".

So a PUBLISHED POINT ESTIMATE (0.154), on the BELOW-0.1644 side, naming 0.1644 in the same
sentence, was in the judge's own reading list. docs/52 §2.5 quotes ONLY the ceiling 0.2523
from that same paragraph; §7 item 8 says "The only Δ_shape quantity used is the bound
docs/51 §5.4 already publishes"; §9 says "Δ_shape is unmeasured and unseen by this pass".
All three are LITERALLY TRUE (nothing was computed) but docs/52 alone never discloses that a
pre-decision point estimate on one side of the bar existed. docs/53 §3.2 DOES quote §5.4 in
full including the 0.154. The DRAFT (git show 41919dc:docs/46_..._DRAFT.md) contains NO
0.154 / 1.287 -- the estimate first appears in docs/51.

The bar journals: bar-statistical used only "<= 0.2523 ... in a for-all argument";
bar-eliminative "identical for every value in [0, 0.2524]"; bar-decision-theoretic logged a
near-slip -- "I noticed that docs/51's stated bound on Δ_shape lies inside this window. I did
not use it". NONE of the four records 0.154.

## 03 - MEASUREMENTS (python3.10, pasted verbatim)

```
$ python3.10 -c "import math; print(math.log(1.287))"
0.25231392861398955        -> 4dp = 0.2523. docs/51 §5.4 prints 0.2524 (WRONG 4dp);
                              docs/52 §2.5 and docs/46 §6.1:1008 print 0.2523 (RIGHT).

$ reconstruct docs/51 §5.4's own inference:
joint 0.43194    -> |ln(0.3687/jf)|=0.1583033845  |ln(0.4745/jf)|=0.0939749283  max=0.1583033845
joint 0.43194418 -> 0.1583130617 / 0.0939652511                                 max=0.1583130617
joint 0.432271   -> 0.1590694011 / 0.0932089117                                 max=0.1590694011  (f_bar, docs/53 §3.1)
=> the stated method gives 0.15830, NOT 0.154. docs/51's printed 0.154 is an ARITHMETIC ERROR,
   separate from docs/53 §3.2's (correct) "estimate of the wrong statistic" diagnosis.
   Corrected inference vs docs/53's measured all-18 max 0.1589405011: rel err 0.00081 (0.08%).

$ distance below the 0.1644 bar:
docs/51 printed 0.154                      0.1540000000   below by 0.010400  =  6.326 %
corrected arith, centre 0.43194            0.1583033845   below by 0.006097  =  3.708 %
corrected arith, centre f_bar 0.432271     0.1590694011   below by 0.005331  =  3.242 %
measured all-18 max                        0.1589405011   below by 0.005459  =  3.321 %
measured REGISTERED CAL-8 statistic        0.1299456917   below by 0.034454  = 20.958 %
largest of the 30 readings (V4_dg/18/all18)0.1638778967   below by 0.000522  =  0.318 %
```
JUDGEMENT on "could a session have anticipated the SIDE?": **YES.** Every correct form of
docs/51's own published inference (0.15830 / 0.15907) lands BELOW 0.1644, by 3.2-3.7 %, and the
registered statistic landed 20.96 % below. Foreknowledge of the **side** was available from the
record; foreknowledge of the **value** was not (the estimate is 18.5 % high on the CAL-8 statistic).

## 04 - DIRECTION OF INCENTIVE - the hypothesis I was told to prove FAILS here
Under the DRAFTED bar, Δ_shape ~0.154 <= 0.1644 => §6.1's table says **Branch A is available**
(C4.3 may start provisionally, α̂ rescaled). Striking the bar and imposing Δ_shape = 0 =>
**Branch B mandatory**, C4.3 blocked, a full re-run owed with every guard statistic re-derived.
So an agent that HAD anticipated the side and wanted the permissive outcome would have KEPT the
bar. The strike is the self-denying direction. There is no motive to reverse-engineer.

## 05 - docs/52 §4's four reasons: value-independence, checked one at a time
1 "the document's own derivation" - reads §6.1's text only. VALUE-FREE.
2 "can only tighten, never loosen" - {Δ_shape = 0} is a SUBSET of {Δ_shape <= 0.1644}; a subset
  acceptance region can only close Branch A. Set inclusion. VALUE-FREE.
3 "cannot be tuned" - there is no threshold to choose. VALUE-FREE.
4 "costs nothing that is live" - rests on B2, which is in the PRE-docs/52 DRAFT at :540
  ("intends to issue a final verdict ... because ADOPT is unreachable under A3") and on B5
  (:546, "the freezing of this document is already scheduled"). Both fire independently of
  Δ_shape. VALUE-FREE.
=> none of the four works only if the value is below 0.1644. Clean.

ASYMMETRY CLAIM, tested as stated: *"Δ_shape = 0 never opens Branch A where Δ_shape <= 0.1644
would have closed it."* The bar rule CLOSES A only when Δ_shape > 0.1644; there the exact rule
(needs = 0) also closes. So no counterexample exists. **TRUE** - and it is the tautological
(safe) half; the informative half (the exact rule closes what the bar opened) is what occurred.

## 06 - DEFECT: docs/46 §10 amd 1's headline is false
":1355-1372" ⚠ box: *"The struck bar would have said 'Branch A is available; C4.3 may start'"* /
*"had the bar survived, C4.3 would have been licensed to start on a 0.3 % margin"*.
§6.3 (docs/46:1084+) makes Branch B mandatory if **ANY** of B1-B5. On 2026-08-11 **B2** fired
(final verdict / ADOPT unreachable under A3) and **B5** fired (:1101-1103, read out: "continues
to hold until" docs/37 §A3 exists). So C4.3 could NOT have started under the drafted bar.
The same box concedes it 3 lines later ("The branch was over-determined anyway - B2 ..."), and
docs/53 §5 makes the point BEFORE its §5.1, and docs/37 A3 §(3) gets it right (B1+B2+B5).
The clause "Branch A is available" is correct; "C4.3 may start" is not.

## 07 - the "0.3 %" framing
0.1638778967 is V4_dg / normaliser-18 / max-over-ALL-18: two of the three choices are NOT what
§6.1 requires. On the REGISTERED statistic the drafted bar would have opened Branch A by
**20.96 %**, not 0.3 %. docs/53 §5.1 labels the reading honestly; docs/46 §10 and docs/37 A3
repeat "0.3 %" without printing the registered reading's own margin. The 0.3 % figure supports
"the bar's verdict was READING-fragile", not "the asymmetry bit narrowly".

## 08 - forward-only use in THIS RUN (checked, clean)
docs/37 A3 §(3) :2043-2087 - forward; names B1/B2/B5 as three independent firings; item 5
  forbids reading Δ_shape as detectability.
docs/45 §8.5.9 :1684-1700 - uses exp(±Δ_shape) as a bound on the LEVEL term and registers, in
  the same block, that it does NOT bound the argmax and that O5 stays OPEN. §8.5.10 item 7
  forbids reading anything in it as a materiality bar.
docs/35 §9.4 :1181 - one forward citation. docs/42, docs/43 - no Δ_shape at all.
docs/00_INDEX :138-139 - claims only "decided *before* Δ_shape was computed" = true.
docs/54 DOES NOT EXIST (the brief names it); nothing to check there.

## 09 - VERDICT
The reverse-engineering hypothesis is REFUTED on the artifact. Order holds on mtimes AND on
content; no journal carries a value or a side-selecting estimate; all four grounds are
value-free; and the strike moved the outcome in the direction that COST the deciding session.
What is真 real is narrower: docs/52's disclosure omits that a side-indicating point estimate was
in its own reading list, and docs/46 §10's flagship sentence overstates what the bar was
holding back.
