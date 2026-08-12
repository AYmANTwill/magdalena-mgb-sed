# journal — lens-freeze-honesty (T6 adversarial lens)

READ-ONLY agent. Writes nothing but this file.

## 00 — mandate (2026-08-12)
Lens: "docs/46 is FROZEN (READ OUT). The freeze presents itself as a pre-registration when its
hypotheses were already answered, and the READ OUT label is decoration." Try to prove it.

Checks assigned:
1. Does docs/46 §9 card + top block ADMIT read-out, or does §2 read prospectively? Count
   clauses carrying the read-out IN PLACE vs not.
2. §4.4's ordering guarantee — does A3 use the corrected sentence §4.4 mandates? Quote A3.
3. H-S (R7)/(R8) field clause + §3.3 stratified report incomplete. §4.2 note 3 says the full
   stratified report is required before ADOPT-SOURCE is EXERCISED. Did A3 exercise anyway?
4. Any doc written this run citing docs/46 §2 as though answers unknown?
5. docs/46 §5 "WHAT IS NOT ALLOWED TO MOVE" — nine rows vs actual file diffs.

## 01 — start

## 02 — docs/46 read (1585 lines). Structure map
§1.0 bracket · §1.1 defects A/B · §1.2 READ-OUT table · §2.0 no-bar · §2.1-§2.5 hypotheses ·
§3.1 variants · §3.3 factors + mandatory stratified report · §3.4 S ratios · §3.5 loads ·
§4.1 ladder · §4.2 rule+outcome table+3 notes · §4.3 forbidden evidence · §4.4 ordering guarantee ·
§5 nine-row immovables · §6 gate · §7 negative pre-commitment · §8 confounding · §9 card ·
§10 amendment slot (Amendment 1 2026-08-11 Delta_shape; Amendment 2 2026-08-12 f_area(V4)).

### Read-out attachment audit (grep -n "Read out\|NOT READ OUT")
In place at the clause site: (R1):406 · (R2):414 · (R3):418 · (R4) magnitude printed in place
:445-450 · (R5):459 · (R6) whole blockquote :464-508 · (R7)/(R8) "**Not read out.**":544 ·
(R10) retired w/ replacement in place :577-604 · (R11):609 · (R12):617 · H-L :636 "H-L is
therefore NOT refuted". => 11 of 12 clauses carry the read-out AT THE SITE.
**(R9) at :547 carries NOTHING.** grep "R9" docs/46 -> only :337 (G-i "used by" list) and :547.
grep "(R9)" docs/*.md -> only docs/37:1515. §1.2's read-out TABLE has no (R9) row.
BUT top block :14-16 and §9 card :1268 both say the exception is *only* H-S's field clause
(R7/R8); §2.3:558-559 says (R7)/(R8) is "the one part of §2 that is not read out".
=> candidate finding: the not-read-out set is understated by one clause.

## 03 — CHECK 2: §4.4's ordering guarantee — does A3 use the corrected sentence?
`grep -n "recorded before any default was switched" docs/37_c3_closure.md` -> :1402.
Quoted from docs/37:1400-1404 (A3.1, immediately under the DECISION table):

  **The sentence `docs/46` §4.4 item 1 requires, in the true form it gives, and not in the form the
  original guarantee asked for:**
  > **"This decision is recorded before any default was switched, and after the basin totals under
  > every variant were already published in `docs/47` §4.3, `docs/49`, `docs/50` and `docs/51`."**
  The original guarantee — *"recorded before any basin total under it was computed"* — is
  **permanently unavailable to any session** and **is not claimed here**

=> VERBATIM MATCH with docs/46 §4.4 item 1. CLEAN on the document side.

BUT §4.4 says: "**The journal must contain the sentence** ..., and the file birth times must
support it." Measured:

    grep -niE "recorded before|before any default|before any basin total|ordering" \
      docs/agents/journal_a3-enactment.md
    :25   - §4.4: honest ordering sentence prescribed verbatim.
    :69   ... I do not write to that journal. I cite it as the ordering record.

The SENTENCE ITSELF IS ABSENT FROM THE JOURNAL (175 lines). => FINDING (MEDIUM).

## 04 — CHECK 3: was ADOPT-SOURCE "EXERCISED"? (the most likely overreach)

docs/46's gate, three frozen sites:
 - §4.2 note 3 (:886-890): "Reachable != exercised. ... §3.3's full stratified report is not
   discharged — elevation strata exist for every variant, slope terciles do not, and the
   per-station erosion-weighted LS-bar exists only as ratios — and it is REQUIRED BEFORE
   ADOPT-SOURCE IS *EXERCISED*"
 - §9.2 (:1313): "It ... exercises no §4.2 outcome."
 - §10 closing note (:1397-1399): "(R7)/(R8) and §3.3's slope-tercile stratified report are owed
   before ADOPT-SOURCE is exercised"

Measured in docs/37 (21 lines contain "exercis"):
 SAY NOT EXERCISED / NOT EXERCISABLE: :11 :423 :1359 :1397 :1633 :1637 :1640 :1674 :1681 :1683
   :1686 :2006 :2183 :2267 :2289 :2316   (16 sites)
 SAY EXERCISED:
   :241  "> 4. **`docs/46` §4.2's outcome is now exercised as ADOPT-SOURCE at `ls_formulation =
          buarque_2015_dg`** — see A3.1. The RESOLVER named below has therefore been executed on
          source grounds; what remains owed BEFORE THE ENGINE DEFAULT MAY MOVE is A3.1.6's three
          deliverables."                              <-- LIVE BODY, §4 candidate 0
   :1394 "> | `docs/46` §4.2 outcome row exercised | **ADOPT-SOURCE** |"
   :1423 "| ADOPT-SOURCE | ... the stratified report (HALF met — A3.1.6) ... | EXERCISED, by item 1
          and by elimination ... which makes the outcome determined but not yet exercisable |"
 and src/mgb_sediment.py docstring (from git diff): "`docs/46` §4.2's outcome exercised is
   **ADOPT-SOURCE**."

A3.1.6 (:1633-1690) NAMES the condition, quotes note 3 verbatim, does NOT discharge it ("The
reporting half is not"), and concludes "the §4.2 outcome is DETERMINED and RECORDED, and it is NOT
YET EXERCISABLE". So the SUBSTANCE is honest and no default moved. The LABEL at 4 sites uses the
frozen document's own gated verb. => FINDING (HIGH), not CRITICAL.
Note :241 also RELOCATES the gate: note 3 puts the stratified report before *exercise*; :241 puts
it before "the engine default may move".

## 05 — CHECK 1 continued: (R9), and the "one clause not read out" claim

`ls data/raw/refs/` -> buarque2015.pdf ONLY. docs/47 O1 (:624): "Desmet & Govers (1996) primary
text not obtained (paywalled)". No Moore & Burch 1986, no Mitasova 1996 on disk. (R9) requires
exactly one of those two. => (R9) is not read out and is not readable from the current sources.
Yet docs/46:14-16 (top block) "(The exception is H-S's field clause (R7)/(R8) ...)", :1268 (§9
card) "H-S's field clause (R7/R8) is the one that is NOT read out.", and :558-559 "(R7)/(R8) ...
remains the one part of §2 that is not read out". Propagated into docs/37:1230 "This is the one
hypothesis in docs/46 §2 that was never read out". => FINDING (MEDIUM).
Direction: (R9) firing would refute OUR n=1.3, i.e. it argues FOR ADOPT-SOURCE — the correction
cannot help the adopted outcome.

## 06 — measurement: the (R3) ladder mixes weighting supports

python3.10 output:
    limiter_ero 0.362435          abs ln = 1.014910131110257
    m_step_ero 0.522043           abs ln = 0.6500053190132445
    m_cap_ero 0.51748             abs ln = 0.6587844019324358
    S_ero 1.694054                abs ln = 0.5271244729354905
    L_form_inside_source 0.580685 abs ln = 0.543546837831505
    ln(0.43194/0.25146) = 0.5410027585442313

docs/46 §1.2 (R3) row is labelled "on the exact re-run" (= erosion-weighted, §3.3) and four of its
five entries ARE erosion-weighted. The L entry 0.5435 is the AREA-weighted L-form ratio's |ln|;
the erosion-weighted span is 0.5410. Same in §2.0.1 row 3. Verdict unaffected (limiter dominates
either way). 1.0150 vs measured 1.0149 traced to docs/48:441 using 4 s.f. 0.3624 (-> 1.0150067),
so docs/46 carries its cited source faithfully. => FINDING (LOW), distinct sites from the
already-reported §1.0 / docs/51 §2.3 identity defect.

## 07 — CHECK 5: §5's nine rows vs the actual diffs

Hashes/mtimes taken 2026-08-12 (files ARE being edited concurrently: docs/37 read 2373 lines,
then 2382 minutes later).

| §5 row | verdict | evidence |
|---|---|---|
| cp_revision cited_central | CLEAN | src/mgb_sediment.py:688 DEFAULT_CP_REVISION unchanged; diff is docstring-only |
| volume_convention / k_unit_system | CLEAN | no executable line in the diff |
| H2E hydrology | CLEAN | parameters_H2E.csv sha256[:16] cfe68790db22bdf1, mtime 2026-08-10 14:03 |
| frozen driver bundle | CLEAN | h2e_drivers 6bbb15c7db5eeaa7 · q_gauge_H2E.npz d545d98a8b6e0741 · report_H2E 60df921d7fb4c9fa · metrics_fleet c8052df034a44170 — all mtime 2026-08-10 |
| ls2d_aggregation / ls2d_resolution | CLEAN | no added line changes them; docs/37:1726 reaffirms 1.000 |
| committed LS products | CLEAN | urh_ls2d.csv 8579c1281c1a992d (2026-08-11 04:15) · minibacia_ls2d.csv 4c49b07bb92d54cb · scripts/c3/ls2d.py 103a31c4a50f2c0a — none in git status |
| frozen pre-registrations 33/35/42/45 | CLEAN | docs/33 untouched (314076992ddf8fbe); 35 -> own §9.4; 42 -> own §9.7; 45 -> own §8; docs/45:635 still prints f_LS 1.000 |
| P, FG = 1.0 | CLEAN | no added line changes either |
| yield embargo | CLEAN | all 12 t/km2/yr hits in added docs lines are affirmations of the embargo |

docs/46 itself: `git diff -U0` -> single hunk `@@ -1399,0 +1400,186 @@`; python check
`new.startswith(old) == True` and the prefix through "## 10" byte-identical. PURELY ADDITIVE.
`head -1 data/processed/urh_ls2d_variants.csv` -> no V4_dg column, so A3.1.6 item 3 is verified
independently by me.

## 08 — CHECK 4: does anything written this run cite docs/46 §2 as OPEN?

grep of all added lines in docs/, src/nbgen, src/mgb_sediment.py for "docs/46 §2" and the five
hypothesis names: ~45 hits, EVERY one cites §2 as settled ("(R6) CLOSED", "may never be graded
CITED", "settled by the citation", "(R7)/(R8) never read out"). ZERO prospective citations. CLEAN.

## 09 — out-of-lens defect found while diffing

.claude/settings.json is MODIFIED and no agent claims it (the T3+T5 return says "none by me").
`git diff .claude/settings.json` adds two permission entries, one a Read() glob into
//c/Users/knade.MSI_TWILL/.claude/projects/.../subagents/workflows/wf_2cc018e6-a22/** — outside
the repo. Reported, not touched.

## 10 — VERDICT

The lens hypothesis largely FAILS. docs/46's freeze is unusually honest: the read-out is in the
title, the top block, §1.2's table, §9's card, §9.2, and at 11 of 12 clause sites; §4.4 admits the
ordering guarantee is permanently unavailable and prescribes the true replacement sentence; §10
amendment 1 volunteers that the struck bar would have reversed the branch on a 0.3 % margin, which
is self-incriminating and was not required of it. Three real defects survive: the "exercised"
label at 4 sites, the missing journal sentence, and (R9) / "the one clause not read out".
