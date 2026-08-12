# Journal - refute-t6-4 (REFUTER, read-only)

Task: try to kill T6 finding "docs/51 §7 item 2 orders a materiality-bar decision; §3/§4 adjudicate
verdicts in a `bar` column at 0.1644; no pointer to docs/52 at those sites". severity HIGH.
Posture: default = the finding is WRONG.

Start 2026-08-12. Read-only. Only file I write is this journal.

## Step 1 - open docs/51 at the named locators

### 1a. Quotes verified verbatim (all of them)
- `sed -n '228,233p' docs/51_ls_freeze_decision.md` -> ":228 `| test | measured | bar | verdict |`",
  ":230 `| (R4) ... | **0.0088** ero (0.0052 area) | 0.1644 | **FIRES** => H-M's **field clause
  REFUTED**, 19x inside |`", :232 and :233 as quoted. VERBATIM.
- `:257` H-L row `| **0.0258** | 0.1644 | **REFUTED** ...` VERBATIM.
- `:352` = §5.5 table bracket-width row; `:371` = §5.6 item (e); `:474-477` = §7 item 2. VERBATIM.
- Preface: "An orchestrator can execute this list top to bottom" is at **:469**, not :468
  (off-by-one in the finding; substance unaffected).
- `grep -n "0.1644"` -> 31, 230, 232, 233, 257, 258, 330, 336, 346, 476. The finding UNDER-lists:
  it misses **:31** (THE FOUR ANSWERS box, "against the 0.1644 bar") and :258/:330.
- `grep -n "docs/52"` -> 657, 676, 678, 730 ONLY, all inside the new §9. CONFIRMED: no pointer at
  any §3/§4/§5.5/§5.6/§7 site.

### 1b. Is the surrounding context a supersession block / historical record?
NO. docs/51 header (:1-12) says "Written 2026-08-11 ... does four jobs"; no superseded banner.
`docs/00_INDEX.md:137` -> "| 51 | ls_freeze_decision | ... | **LIVE** - owns the corrected LS
bracket; **§7 is the numbered blocking list an orchestrator can execute** |". The index itself
advertises §7 as executable. The §3/§4 tables are operative verdict tables, not a register of
superseded values (contrast docs/39, docs/46 §1.0/§3.5, docs/47 §3).

### 1c. Was docs/51 amended THIS run?
`git status --porcelain` -> ` M docs/51_ls_freeze_decision.md` (uncommitted). Last commit touching
it: d60d8d9. §9 "Amendment slot - OPEN from 2026-08-12" exists with Amendment 1 (f_area support)
and Amendment 2 (the -ln 0.5807 identity), plus 5 body strike-throughs at :19/:135/:141/:167/:190.
So the slot was open and being written in the same run, and neither amendment touches the bar
column, §5.6(e) or §7 item 2. CONFIRMED.

### 2. Numbers recomputed from the primary artifact (not transcribed)
python3.10 from data/processed/ls2d_variants_summary.json:
  V2a_m_cap05 ln_ratio -0.688214583239191 ; V2b_m_step_eq14 ln_ratio -0.6830153825659728
  area |dln| = 0.005199200673218218            -> docs/51's "0.0052 area" OK
  ero 0.52204/0.517480 = 1.0088119347607636 ; |ln| = 0.00877333624962563
                                              -> docs/51's "0.0088" OK and docs/52's "x1.0088" OK
  joint/product step = 1.3476163903345526      -> x1.34762 OK
So the arithmetic on both sides is right; the dispute is purely the LABEL, exactly as claimed.

### 3. docs/52 side verified
- `docs/52:369` (§6, :189 row) prints, verbatim: "**[WARN] This changes a label already written:**
  `docs/51` §3 records *"(R4) FIRES => H-M's field clause REFUTED"*; under this disposition the
  field clause is **confirmed on its sign** and its magnitude is x1.0088".
- `docs/52:452-456` (§8d): "... it is owed to `docs/51`'s owner as a note, not enacted here."
- `docs/52` §5 binding line, verbatim: "Labels are owed wherever the conclusion appears, not only
  in `docs/46`." And §5's "Explicitly NOT bar-dependent" list names (R4) 0.0088, (R12) 0.0248,
  H-L 0.0258, Defect A 0.0036/0.0010 - precisely the fix content the finding proposes.
- INDEX:138 -> docs/52 LIVE, "0.1644 ln ... is **superseded**".
So the debt is explicitly owed AT docs/51 by the document that struck the bar. Not killable.

### 4. Retired-claim / category-error checks
- Not a re-raise of anything retired: the finding flags CONTINUED USE of the retired instrument,
  the opposite of re-raising it.
- Not a category error: `0.1644` at :230/:232/:233/:257 sits under a column literally headed `bar`
  and drives words "FIRES"/"immaterial"/"REFUTED". It is used as a materiality bar, not as an
  agreement tolerance. f_ero vs f_area is stated correctly at :230.
- (R4) is nowhere marked retired in docs/51: `grep -n "(R4)"` -> 230, 348 only, both "refuted".

### 5. Where the finding OVERCLAIMS (severity/scope trims)
(i) Consequence overreach: §7 item 2's own text says "`docs/48` deliberately proposes no
    replacement value; **do not rescale it silently**, and do not import 0.6936 by default". So it
    FORBIDS the import and the silent rescale; "Decide the bar" is satisfiable by "strike it",
    which is what docs/52 did. It is a DISCHARGED-BUT-UNMARKED instruction, not an instruction to
    manufacture a fourth band.
(ii) Not unique to item 2: §7 items 1 (enact docs/46 (a)-(d)), 3 (freeze docs/46 - now
     "FROZEN (READ OUT)") and 5 (run the Delta_shape pre-test - computed, 0.1299456916752905,
     docs/53) are ALSO discharged and unmarked. `grep -ni "discharg"` in docs/51 -> only :122,
     :309, :493 (B4). So §7 is stale as a list; item 2 is one entry in it.
(iii) Locator :352 is the weakest: docs/51 §9 amd 2 at :730 already says "docs/46 §2.0.1 row 2 and
     `docs/52` §5 row 2 already label the bracket **width** as BAR-DEPENDENT *and superseded*".
     That substance is already pointed at docs/52, just not at :352.
(iv) Site list should ADD :31 (the FOUR ANSWERS box) and :258/:330.

### 6. VERDICT
Could not kill it. refuted = false, CONFIRMED. Severity stays HIGH, but on the load-bearing half:
a LIVE doc the INDEX advertises as executable still prints "(R4) FIRES => field clause REFUTED"
as a verdict reached through a struck instrument, and docs/52 §8(d) explicitly says that label is
owed to docs/51's owner. The "fourth retired band" consequence is the overclaim and must be
dropped from the wording.
