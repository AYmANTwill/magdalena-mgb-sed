# Journal — bar-judge (materiality bar decision, docs/52)

## 2026-08-11 — start
Task: decide docs/46's materiality bar on principle, BEFORE Delta_shape is computed.
Three proposals received (statistical / decision-theoretic / eliminative — third truncated in brief).
Plan: read docs/51 §5.5–5.6, docs/48 §5, docs/46 (bar sites), docs/47, then decide and write docs/52.
Constraint: no git ops, no edits to 46–51, only docs/52 + this journal.

## 2026-08-11 — orientation complete
Read: CLAUDE.md, docs/51 (full), docs/48 (full), docs/46 (full), docs/47 §2.2/§4.2-4.4/§5.3-5.5.
Not edited: 46,47,48,49,50,51. No git command.

## Measurements made this pass (python3.10, arithmetic only, nothing transcribed)
- R10 statistic reproduced BOTH ways: step 0.362435*0.52204*1.694054 = 0.32052445 ->
  |ln(0.431944/.)| = 0.2983374 ; cap 0.51748 -> 0.31772468 -> 0.3071107.
  joint/product = x1.3476164 (step) / x1.3595... (cap). Confirms docs/51 5.5's 0.2983.
- Seven docs/48 §2.4 SE constructions recomputed sd/sqrt(n): 0.6936 0.4775 0.5117 0.5986
  0.3544 0.3054 0.6067. SMALLEST = 0.3054. R10 = 0.2983 < 0.3054 => R10 refutes on ALL SEVEN.
  Margin on the tightest: 0.3054/0.2983 = 1.0238 (2.4%).
- Threshold's own sampling error: sd(s)/s = 1/sqrt(2(n-1)) = 0.267 (n=8), 0.183 (n=16).
  95% interval on the smallest SE = [0.1961, 0.4147]; R10 lies inside on 5 of 7.
- Bracket width 0.5410 vs the seven SEs: material on 4, immaterial on 3. Construction-dependent.
- INDIFFERENCE WINDOW (my own, decisive): every ALREADY-MEASURED bar comparison returns the
  identical verdict for any bar in (0.0321, 0.2983) -- a factor of 9.29. Sorted measured values:
  R4 0.0088, R12 0.0248(ero/area 0.0273), H-L 0.0258, R2 0.0321, then R10 0.2983.
  => the bar adjudicates NOTHING measured. Its only live consumers are R10 and the blinded
  Delta_shape.
- Non-composability, measured cleanly from docs/48 §5.3's own table: at the bootstrap-(b)
  half-width 1.2833 ALL FOUR single levers are immaterial (1.0150, 0.6588, 0.6500, 0.5271,
  L-form 0.5435) yet the composed DG endpoint 1.3805 is material. (Proposal 2's version of this
  mixed m-cap with m-step and overstated it; corrected here.)
- Elasticity of the ENSO deliverable to f_LS from docs/47 §4.4's four pairs: 0.00726-0.01154
  ln/ln => a 1% tolerance implies a bar of 0.866-1.378 ln. Confirms proposal 2's kill.
- NEW FINDING: the bar has FIVE consumers that docs/47/48/51 never enumerated. Their list
  (:138,:140-142,:189,:217,:240,:265,:490-491,:506,:538) is the LITERAL-NUMBER sites only.
  By-name uses at :163 (R1), :166 (R2), :220 (R8), :249 (R12), :421 (ADOPT-BAND) are missing.
  15 clause-level sites, not 10. Amendment (e) must reach all fifteen or the frozen document
  keeps by-name references to a retired bar.

## Decision (taken before Delta_shape is computed)
NO NUMERIC BAR. Struck, not rescaled. Each of the 15 sites gets a threshold-free rule that
already exists in docs/46 (§3.3 f_ero-decides, §4.2's hierarchy, §6.1's own derivation) plus
mandatory full-precision reporting. Delta_shape's site gets the EXACT discriminator its own
derivation supplies (pure level change <=> Delta_shape = 0), which is strictly tightening and
cannot be tuned. (R10) is settled by the citation, not by a statistic.
Writing docs/52 now.

## 2026-08-11 — docs/52 written
docs/52_materiality_bar_decision.md written (9 sections). Decision: NO NUMERIC BAR, struck not
rescaled; 15 sites re-grounded on threshold-free rules already inside docs/46; (R10) decided by
the citation; Delta_shape's site gets the exact discriminator Delta_shape = 0 (strictly
tightening, un-tunable); 5 conclusions labelled BAR-DEPENDENT.

Ratios re-verified to full precision before writing the final table:
  f_ero(V1)/0.351      = 1.0325783
  f_ero(V4)/f_area(V4) = 1.0248386   (R7 proxy bias 1.0251)
  DG ero/area          = 1.0277138   (R7 1.0278)
  f(V2b)/f(V2a)        = 1.0088119
  joint/product step   = 1.3476164 ; cap = 1.3594914
Corrected two digits in the draft after this check (had written 1.0251 and 1.35950).

## Dead ends / rejected en route (recorded so they are not re-tried)
- Deriving the bar from the narrowest registered alpha verdict cell [3.40,3.9] = 0.1372 ln:
  FORBIDDEN by docs/46 §4.3 bullet 4 (no alpha band as evidence) and circular (box is
  LS-conditional, docs/47 P1). Its closeness to 0.1644 is suspicious, not reassuring.
- Deriving it from a tolerance on the ENSO deliverable: elasticity 0.00726-0.01154 ln/ln, so a
  1% tolerance implies a bar of 0.87-1.38 ln. Structural reason it can never work: the
  deliverable is a RATIO of two runs sharing the same uniform level factor, so f_LS cancels.
- Using the per-station LS-ratio dispersion (docs/47 §4.4): circular with §6.1's own pre-test,
  the same defect docs/48 §3.2 measured for G12/route 1.
- Keeping one "explicitly non-statistical" constant: rejected on the measured ground that any
  such number adjudicates nothing over (0.0321, 0.2983) and the one live comparison turns on
  2.4%.

## Owed to others (not enacted here; I may not edit those files)
- docs/51 §3's "(R4) FIRES => H-M field clause REFUTED" label changes under §6's disposition
  (field clause confirmed on its SIGN; magnitude x1.0088). Owed to docs/51's owner as a note.
- docs/51 §5.4's "accept §6 unchanged" is amended by §4 in the RESTRICTIVE direction only.
- The amendment set (e) must reach FIFTEEN sites, not the ten enumerated in docs/47/48/51.
