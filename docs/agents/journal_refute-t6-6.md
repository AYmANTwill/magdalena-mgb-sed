# Journal - refute-t6-6

ROLE: REFUTER. Default posture: the T6 finding (lens-a3-overreach, HIGH) is WRONG.
READ-ONLY except this file.

Finding under test: docs/37_c3_closure.md A3.1.3 lines 1570-1573, the blockquote
"THE HONEST LIMIT OF THIS ADJUDICATION" -- claims the fallback branch names
"NEGATIVE -- UNRESOLVED on a documentary rather than an evidentiary ground" with V0
retained, an outcome no governing doc admits, and which disagrees with docs/35 §9.4.3
by the whole L-form lever (x0.43194 vs x0.25146 -> 1.7177x).

## Plan
1. Verify the quoted string exists verbatim at docs/37:1570-1573.
2. Check surrounding context (supersession block? strike-through? historical?).
3. Verify docs/46 §4.2 row at line 872 verbatim, and §7.1 at 1132-1136.
4. Verify docs/37:1421-1422 (A3.1.1 verdict cells).
5. Verify docs/35:1074-1081.
6. Recompute 0.43194/0.25146.
7. Check docs/47 §3 for prior refutation / retirement.
8. Category-error check.

## Log

### 1. Quote fidelity — CHECKED, quote is VERBATIM
`sed -n '1566,1584p' docs/37_c3_closure.md` returns, at 1570-1573:
  "**If `docs/35`'s owner declines it**, then `docs/35` wins on its literal text, this
   amendment's ADOPT-SOURCE at `V4_dg` is the bug, and the surviving outcome is
   **NEGATIVE - UNRESOLVED on a *documentary* rather than an evidentiary ground**, with `V0`
   retained **as incumbent and never as validated**, the bracket carried, and C4.3 still blocked."
=> the lens's quote is exact. No misquote refutation available.

### 2. Context — NOT a supersession / historical block
A3.1.3 is a LIVE adjudication inside the A3 amendment written this run (git diff --stat shows
docs/37 +1212 lines uncommitted). No strike-through, no "superseded", no historical label.
It is the operative escape branch of the adoption. Refutation route 2 fails.

### 3. Cross-document locators — ALL EXACT
- docs/46:872 = the frozen NEGATIVE - UNRESOLVED row; condition verbatim as quoted:
  ">= 1 lever with **no citable ground either way**, or (R6) fires, or the source text cannot be
  obtained/verified".  Licence column: "keep V0 as the default *because it is incumbent, not
  because it won*; carry the full bracket".
- docs/46:1132 = §7.1 commitment, all four triggers literature-facing.
- docs/37:1421 = A3.1.1's NEGATIVE row: "**ALL THREE DISJUNCTS FALSE.**"
- docs/37:1422 = RETAIN-OURS row: "'Ours keeps running for now' is a fact about the engine
  default (A3.5.1), **not a §4.2 outcome**."
- docs/35:1079-1081 = "**If §9.3.2 item 1's three-lever list is held to be supreme, the hybrid is
  the registered default and the POINT is a deviation requiring item 2's written source
  justification.** Both branches are live as of this date; neither is exercised here."
- docs/35:1074 = "**This amendment does not resolve that**".
- docs/35:764-790 = §9.3.2 item 1 as amended 2026-08-12: the eq.-14 phrase is struck and the WARN
  block says the fourth-lever supremacy question is "**left open, not decided here**".
=> mutual deferral confirmed on disk. Neither owner rules. The branch IS live.

### 4. Does the counterfactual make any NEGATIVE disjunct true? NO.
If docs/35's owner declines: (a) all four levers still have citable ground (pp. 47/48/94/98
printed); (b) (R6) still does not fire (Sf percent); (c) buarque2015.pdf is still on disk with a
matching sha256. All three disjuncts stay FALSE. §7.1's four triggers stay FALSE (the dispute is
between two PROJECT documents, not in the literature). So NEGATIVE - UNRESOLVED is NOT reachable
on the frozen condition set under the branch's own premise. I could not construct any reading
that makes it reachable.

### 5. Arithmetic
python3.10 -c "import math; print(1/0.43194, math.log(1/0.43194)); print(0.43194/0.25146,
math.log(0.43194/0.25146)); print(1/0.25146); print(299.5387088405831*0.43194)"
  V0/V4    = 2.315136361531694   (ln 0.8394685892728705)
  V4/V4dg  = 1.7177284657599616  (ln 0.5410027585442313)
  V0/V4dg  = 3.976775630318937
  load(V4) = 129.38274989660147 Mt/yr   (vs V0's 299.5387088405831)
=> the lens's 1.7177 is arithmetically right BUT it is the V4-vs-adopted-POINT gap. The gap
between the TWO FALLBACKS it is actually contrasting (docs/37's V0 = 1.000 vs docs/35 §9.4.3's
V4 = 0.43194) is **x2.3151**, ln 0.8395. So "by the whole L-form lever" mislabels the gap; the
substance (V4 not V0) is unaffected. Recorded as an overclaim to correct, not a refutation.

### 6. Retired / already-refuted check — CLEAN
docs/47 §3.1 R1-R9 and §3.2's standing refutations contain nothing about §4.2 outcome-row entry
conditions or the docs/35 supremacy branch. No retired band, no materiality bar, no (R10), no
SDR band, no mountainous LS band is invoked by the finding. Not a re-raise.

### 7. Category-error check — CLEAN
Not tolerance-vs-bar; not f_ero-vs-f_area (0.43194 and 0.25146 are both erosion-weighted, 1.000
is V0); not level-vs-shape; not CITED-vs-validated. The finding is about an OUTCOME LABEL and its
frozen entry conditions.

### 8. NEW: the defect has a SECOND site the finding does not name
docs/37 A3.7 (line ~2286), the docs/35 row, item (a): "**without it, `docs/35` wins on its literal
text and this amendment's outcome becomes NEGATIVE - UNRESOLVED**". Same wrong label, restated.
Any fix must cover A3.7 as well as A3.1.3.

### 9. Partial defence of docs/37 that DOES hold
"`V0` retained ... the bracket carried" is docs/46:872's own NEGATIVE licence wording, so that
PAIRING is not docs/37's invention. What docs/37 invents is the ENTRY CONDITION ("documentary
ground") and the application of the label. Also docs/37 :1536-1538 already states the literal
reading yields V4 at 0.43194, and A3.1.6 already names a §4.2 governance gap - so the material to
catch this is on disk. But A3.7 reinforces the error rather than correcting it.

## VERDICT: refuted = false. CONFIRMED. Severity HIGH stands.
Three independent legs, each verified from disk:
 (i) NEGATIVE - UNRESOLVED is asserted on a ground absent from docs/46:872's frozen disjunction,
     and A3.1.1 (same document, :1421) measures all three disjuncts FALSE - a frozen row's entry
     conditions extended by an amendment in another file;
 (ii) it contradicts docs/35 §9.4.3's own stated consequence for the same premise (V4 0.43194 as
      registered default, POINT as an item-2 deviation) - and contradicts docs/37's OWN :1536-1538;
 (iii) "V0 retained" as part of a §4.2 outcome is the engine-state/outcome conflation A3.1.1's
       RETAIN-OURS row (:1422) expressly rejects.
Corrections to the finding as written: the fallback-vs-fallback gap is x2.3151 not x1.7177; the
locator must include A3.7's docs/35 row (a); the V0+bracket pairing is docs/46's wording.
