# journal — bar-eliminative (materiality bar option, ELIMINATIVE angle)

Task: propose ONE option for docs/46's materiality bar. My assigned angle: argue that docs/46
should carry NO numeric bar, and test that against every site.

BLINDING ACKNOWLEDGED: Delta_shape must not be computed, estimated, or reasoned toward. I record
here, up front, the test I will hold myself to: **my proposal must give the same answer at every
one of the four Delta_shape sites whatever Delta_shape turns out to be.** If at any point my
argument needs to know which side of a line Delta_shape lands on, the argument has failed and I
will say so rather than guess.

## S1 — orientation done
Read: CLAUDE.md, docs/00_INDEX (via CLAUDE.md summary), docs/51 in full, docs/46 in full,
docs/48 sec 5 in full, docs/47 sec 2.2 + 5.3/5.4, docs/50 head.

## S2 — FIRST MEASUREMENT: the site inventory is WRONG in docs/51 and docs/48.
`grep -n "0.1644\|materiality bar" docs/46` returns **15 sites, not 10**.
docs/51 sec 5.5 and docs/48 sec 5.3 both list ten (`:138, 140-142, 189, 217, 240, 265, 490-491,
506, 538`). They both omit **:163 (R1), :166 (R2), :220 (R8), :249 (R12), :421 (ADOPT-BAND)** —
these say "the materiality bar" in words rather than printing 0.1644, which is presumably how the
inventory was built (numeral search). :249 is (R12), which docs/51's own bar-dependence table
scores — so docs/51 scores a site its own inventory does not list.
CONSEQUENCE: an amendment that edits only the ten listed sites leaves five live references to a
deleted/relabelled bar. This is a blocker for enactment regardless of which option is chosen.

## S3 — direction audit (each clause refutes in a different direction; noted so the
   restatement does not silently flip one)
  refutes when the gap is SMALL (<= bar): R4, R10, H-L(:265), R7(:216 "narrower than"), R8(:220)
  refutes when the gap is LARGE (> bar): R1(:163), R2(:166), R12(:249), ADOPT-BAND trigger(:421)
  branch gate, both directions: :490-491, :506, :538

## S4 — MEASURED THIS RUN (read-only, from data/processed/ls2d_variants_summary.json,
   whose own gate published_v0_mean 39.812 vs measured 39.812260149274394 PASSes)

NEW FINDING — **(R8) at :220 is bar-dependent too, and it is not on anyone's record.**
H-S's stratified clause: "the stratified factors agree with the basin factor 1.714 to within the
materiality bar in all three strata" -> S is a pure level lever with no shape content.
  lowland  <200 m : f = 1.268457   |ln(f/f_basin)| = **0.3010**
  mid  200-1000 m : f = 1.615845   |ln(f/f_basin)| = 0.0589
  andean >1000 m  : f = 1.751579   |ln(f/f_basin)| = 0.0218
  basin           : f = 1.713886
At 0.1644 the lowland stratum misses -> (R8) does NOT fire -> S keeps shape content.
At 0.6936 all three are inside -> (R8) FIRES -> S declared a pure level lever.
**VERDICT FLIPS**, at 0.3010, in the same window as (R10)'s 0.2983. docs/51 sec 5.5's
bar-dependence table lists (R10) as the only flip; it scores five clauses and misses this one,
because its site inventory omits :220. So the bar-dependence blast radius is TWO clause verdicts,
and the second one classifies LS *shape* -- the open defect docs/37 A2.2 / docs/42 G4 assign to
C3.1. This is an argument against ANY bar in [0.30, 0.70], not only against 0.6936.

VERIFICATIONS (measure before asserting):
  (R10) ero: 0.362435 * 0.522040 * 1.694054 = 0.320524 vs joint 0.431944 -> |ln| 0.2983.
        docs/51's figure REPRODUCES exactly. Area-weighted counterpart from the JSON: 0.3262.
  (R2)  f_ero(V1) 0.362435 vs f_area 0.3512626 -> 0.0313 (not 0.0248; docs/51 does not print it)
  (R12) f_ero(V4) 0.431944 vs f_area 0.4213630 -> 0.0248  (matches docs/51)
  (R4)  V2b/V2a area 0.005199 (ero 0.0088 per docs/51)
  (H-L) 0.7698333815060305 vs 0.790 -> 0.0259 (matches docs/50 (a) and docs/51 sec 4)
  bracket width ln(0.43194/0.25146) = 0.5410; endpoints 0.8395 / 1.3805. All match.

## S5 — the floor nobody has stated: the statistics are not defined to better than ~0.03
The SAME clause statistic computed under the two admissible weightings differs by
0.0248 (R12) / 0.0313 (R2) / (0.0052 vs 0.0088) (R4). So no bar below ~0.031 can decide anything
-- the quantity is not defined that finely. That gives a MEASURED lower edge for the
verdict-invariance intervals below, without inventing a threshold.

## S6 — the eliminative frame, site by site (see final answer). Grounds used, in priority order:
   G-SOURCE (a reading is decided by the source at CITED or it is NOT DECIDED)
   G-QUANTITY (the exact quantity is now measured; report it + the interval of bars over which
               the verdict is invariant, instead of a threshold)
   G-CONSEQUENCE (a practice that has demonstrably produced a wrong published number is rejected
               without a threshold -- the naive product produced the retired x0.333)
   LABEL "BAR-DEPENDENT -- NOT DECIDED" where none of the three reaches.

## S7 — BLINDING SELF-TEST, run explicitly
My verdict at the four Delta_shape sites (:490-491, :506, :538) is: drop the threshold, keep the
computation as a reported diagnostic, decide the branch on B2 + B5 + A6.
  B5 fires by construction the moment docs/46 is frozen ("the freezing of this document is
     already scheduled") -- this run IS the freeze run.
  B2 is established fired by docs/47 sec 5.4 (ADOPT unreachable under A3).
  A6 forbids rescaling in place of a re-run REGARDLESS of Delta_shape -- and rescaling-equivalence
     is the entire content Branch A buys. Branch A's premise is denied by Branch A's own condition.
**This answer is identical for every value of Delta_shape in [0, 0.2524].** I did not compute it,
did not estimate it, and at no point did my argument need to know which side of a line it lands
on. Test set in S1: PASSED. I record that I was told a plausible value in the task brief and
deliberately did not use it; nothing above changes if that value is wrong.

## S8 — dead end I went down and abandoned
I considered proposing the ~0.03 convention-floor as a replacement bar ("the quantity's own
definitional precision"). REJECTED as a proposal: it is a precision floor, not a materiality
threshold -- it would declare 3.2 % differences "material", which is not what any of the ten
sites means by material, and it would be the same category error (a measurement statistic worn as
a decision rule) that docs/47 sec 2.2 just falsified. Kept only as the LOWER EDGE of the
invariance intervals, where it is honest.

## S9 — enactment blocker, independent of which option wins
The bar has **15** sites in docs/46, not 10. docs/51 sec 5.5 and docs/48 sec 5.3 both list ten and
both omit :163 (R1), :166 (R2), :220 (R8), :249 (R12), :421 (ADOPT-BAND). An amendment that edits
only the listed ten leaves five live references to a retired bar inside a frozen document.
Also: **R-number collision.** docs/46's (R1)-(R12) and docs/47's R1-R9 are different sequences.
docs/48 sec 5.3's table labels rows "(R7)"/"(R6)" with docs/47's meanings inside a section about
docs/46's clauses. Whoever enacts must not conflate them.
