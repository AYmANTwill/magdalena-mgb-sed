# journal x59-refute-2 (REFUTER)

Target finding: HIGH / x59-lens-overclaim
"§2's comparison table sets the two scores side by side in one row — precisely what §3.1
forbids 'not in a table ... not with a caveat'"
Locator: docs/59_cross_implementation_comparison.md:216 vs :250-254

Default posture: WRONG. Read-only except this journal.

## Step 1: verify the quoted strings exist verbatim

### 1a. Quoted strings — BOTH VERBATIM (no misquote)
`grep -n "median score reported" docs/59_cross_implementation_comparison.md`
-> 216: | **median score reported** | `F_report` **-0.118** (est. a) / **+0.139** (est. b) | `stage2_median_kge_log` **0.05461202762457862** (21 st) / **0.05902198016897042** (13 st) - **both computed on defective simulated SSC; see 3.1. Superseded and mid-rewrite (0)** |
`sed -n '250,254p'` -> the prohibition, verbatim as quoted, incl. "Not in a table, not
in a sentence, not in a figure, not with a caveat." and "...any statement that either
project scores better is unsupported."
VERDICT on quoting: the finding quotes accurately. No refutation on that route.

### 1b. The finding's own negative claim - CONFIRMED
`grep -n -i -E "outperform|scores better|higher score|beats|superior|worse score|better than"`
-> only :146 ("beats", unrelated: an author reading their own source) and :254 (the
prohibition itself). NO ranking sentence exists anywhere in docs/59. Confirmed.

### 2. Numerals at :216 recomputed from the PRIMARY artifact (their repo, read-only)
outputs/calibration/stage2_sediment_params.json     -> stage2_median_kge_log 0.05461202762457862, n_stations 21
outputs/calibration_val/stage2_sediment_params.json -> stage2_median_kge_log 0.05902198016897042, n_stations 13
docs/55:19 -> `F_report` = -0.118 (box floor, alpha=2.0, beta 0.60); docs/55:109 -> in-box `F_report` = 0.139 est (b)
=> every numeral in row 216 is correct to full precision. Row is factually accurate.

### 3. The finding's supporting evidence (their defect) - CONFIRMED REAL
friend_repo/src/mgbsed/model/sediment.py, advection block:
  L404  state.channel[c.name] = np.maximum(new_mass, 0.0)
  L409  qss_t_s = outflow / dt_s
  L410  ssc = self.concentration_mg_l(new_mass, v_ch)
`new_mass` is the POST-export residual; `outflow` is the flux. So SSC was read from the
residual, not the flux, exactly as their MANIFEST states. data/raw/colleague_share/MANIFEST.md
:109-110 -> "Any pre-fix SSC comparison against us is invalid." The prohibition in 3.1 is
well founded. Not disputed.

### 4. THE KILL: the finding's literal reading makes 3.1 violate ITSELF, three times
`grep -n -E "0\.05461|0\.0546|\+0\.139|-0\.118"` over docs/59 -> the SAME two quantities
sit together in PROSE at:
  :99-100  (THE VERDICT block) "Their committed median KGE_log `0.05461202762457862` was
           therefore computed on defective simulated SSC, and it must not be set beside our
           **-0.118** (est. a) / **+0.139** (est. b) in any table, sentence or figure."
           <- a SENTENCE that sets them beside each other while forbidding it
  :250     the prohibition's own sentence prints both
  :266-267 "`+0.0546` and `-0.118` / `+0.139` differ in at least five ways at once"
Under the finding's reading ("numerals must not co-occur"), 3.1 is violated by 3.1, by the
VERDICT, and by 3.1's next paragraph - and the fix would require gutting the disclosure.
A reading that makes the rule self-violating is the WRONG READING. The rule's own final
clause states its object: "any statement that either project scores better is unsupported."
The prohibited object is a COMPARATIVE CLAIM / A GRADE, not co-location of two numerals.
Row 216 makes no claim and carries no grade.

### 5. Context test (disclosure vs comparison) - it is a disclosure, and 2 says so IN 2
2 is titled "The two configurations, side by side": a SPEC table (variable scored,
estimator, transform, station universe, window, free-parameter count, search box, fitted
values). Row label is "median score reported" - a field of the record.
- In-cell: R2's number carries TWO disqualifiers ("defective simulated SSC; see 3.1",
  "Superseded and mid-rewrite (0)").
- Row 215, immediately above: R1's own fit is flagged "NOT ADOPTED - RAILED."
- Paragraph :221-224, immediately BELOW the table, of the *bar* row: "It is also the only
  row of this table on which a comparison of numbers would have been admissible if the
  numbers had been sound." => an explicit, in-section statement that NO OTHER ROW of this
  table - the score row included - admits a comparison of numbers.
- 3.5:326 "This section is about design, not scores, so it survives 3.1 intact."
- 9:1150-1156 records that VOID describes validity, not a gate outcome.
The document discloses this weakness at the point of the table.

### 6. The proposed fix is a NET LOSS OF DISCLOSURE and internally inconsistent
The numeral 0.05461202762457862 appears at :49 (the PIN), :99 (VERDICT), :216, :250, :407
(a TABLE, 4.3's alpha x c_mult table). Withholding it from ONE table while it stays in
another table and three prose places is cosmetic. 0's pin rule ("Anyone quoting a number
from this document must quote the commit and the date with it") requires the committed
number to be on the record. No figure or summary reproduces 2's table:
`grep -rn "0.0546" --include=*.html --include=*.py .` -> no hit outside docs/59.

### 7. Category error in the finding
It equates "table row" with "comparison". But 2's table is the instrument that ESTABLISHES
incomparability: row 203 (FLUX t/day vs CONCENTRATION mg/L), 205 (different epsilon), 208
(21/13 vs 8), 209 (730 d vs 1,096 d), 211 (4 vs 2 free params). A reader reading across
row 216 has already read five rows telling them the two columns are different measurements.

### 8. What survives - and it is small
A real WORDING overreach exists: "not in a table ... not with a caveat" is written more
absolutely than the document itself obeys. One of the two needs a word for literal
self-consistency - but the repair belongs in 3.1's phrasing (narrow it to "no comparative
statement, no grade, no ranking"), NOT in withholding a verified artifact value from the
spec table. Editorial. LOW.
One remnant worth passing up separately (NOT what was filed): in-cell asymmetry. R2's cell
is caveated in-cell; R1's is not (its RAILED/EXPLORATORY flag sits in row 215). A row
quoted alone reads "theirs is broken, ours stands." Fairness-of-tone item, LOW.

## CONCLUSION: REFUTED as filed. Corrected severity LOW (editorial, in 3.1's wording).
