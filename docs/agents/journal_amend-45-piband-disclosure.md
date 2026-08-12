# Journal - agent `amend-45-piband-disclosure`

Opened 2026-08-12. Crash journal, appended as I go. Never truncated.

Task: TWO amendments to `docs/45_c4_preregistration.md` §8 (its amendment slot).
 - Amendment 1 (docs/47 B5): replace the +-38 % Pi band (sigma_r = 0.465 ln falsified).
 - Amendment 2 (T5): the pre-fit disclosure (refute-gate-logic-alpha profiled docs/45's objective).
 - Plus: supersede docs/45 §2.1's "2.37x-3.00x" LS bracket; update §7.1's Amendments cell.

I OWN (write): docs/45_c4_preregistration.md + this journal. NOTHING ELSE.

## 00 - opening reads (in the prescribed order)

Read, in the prescribed order: CLAUDE.md (system context), docs/45 in full (615 lines),
docs/48 in full (589), docs/47 in full (677), docs/52 §0 + §7 (the binding prohibitions),
docs/51 §2.3, docs/46 §2.5.1 (the re-derivation register that names docs/45 §2.1),
docs/agents/journal_refute-gate-logic-alpha.md in full (169 lines).

Sites confirmed by grep in docs/45 (my own grep, not carried):
  line 98  - "ours is 2.37x-3.00x that level"        <- docs/46 s2.5.1 register site
  line 124 - "SE of the fleet-mean level | 0.1644 ln = +-38 % at 95 % (0.724x-1.380x)"
             + "13 stations would have given +-28.8 %"
  line 126 - "k_min on the fit set | 0.0209 /km ... no sink weaker than 3.54x"
  line 162 - "~ 2.12x over 348.4 km at best (all-18 test, k_min 0.00216 /km)"
  line 202 - "keeps its k_min = 0.00216 /km"
  line 205 - "the fit set's own k_min stays 0.0209 /km instead of 0.00303 /km - a factor 6.9"
  line 252 - "SE of the fleet level = 0.1644 ln"
  line 429 - G1.2 "~ 2.12x over 348.4 km at best"
  line 445 - G12 "the registered 95 % level band of +-0.322 ln (+-38 %)"
  line 493-494 - "its +-38 % band"
  line 541 - s6.2 item 2 "The level's band is +-38 % ... never as a point."
  line 575 - s7.1 card "level SE 0.1644 ln (+-38 %)"
  line 577 - "| Amendments | none |"
UNTOUCHED by design (docs/47 R4 / docs/48 s5.4 - error errs safe or independent):
  line 125 SE(beta) 0.0199 (sigma_day 0.809) . line 397-398 sigma_r 0.465 as an
  estimator-disagreement statistic + pair-sigma 0.658 + b_obs IQR 0.464 . line 428 G1.1's
  +0.658 . line 441 G8 0.465 . line 444 G11 0.465 . line 435/493 the class-C x4.2/x2.9 (O8).

## 01 - ROUTE DECISION (band replacement)
CHOSE (b), the station-level bootstrap of docs/48 s3.3 (route 2 of docs/47 s2.2).
Reasons are docs/48 s3.2's two MEASUREMENTS, not a preference:
 (i) route (a) is arithmetically degenerate - for a mean, jackknife SE == sd/sqrt(n) exactly
     (0.6936 both ways) and the LOO range == range(r_i)/(n-1) exactly (6.0214/7 = 0.8602);
     converting a RANGE into a 95 % band needs a conversion constant this repo cannot cite,
     i.e. it would be INVENTING A BAND - the exact move docs/40 retired the SDR band for and
     that the standing rule forbids (a fourth retired band).
 (ii) route (a) destroys G12: G12's whole content is "LOO range vs the level band"; defining
     the band FROM the LOO quantities makes the comparison circular.
Consistency with the parallel docs/43 s3.2 agent: I cite the SAME route (docs/48 s3.3 route 2)
and the SAME numbers. Any disagreement to be reported.
G12's 0.644 ln stays as a STANDALONE fragility threshold (docs/48 s3.2 recommendation;
docs/52 s7 item 7 explicitly leaves it untouched) - so G12 keeps FIRING (0.8602 > 0.6445).

## 02 - MEASUREMENTS I MADE MYSELF (python3.10, arithmetic on docs/48's published CIs)
Command: python3.10 -c "<see below>"   Output verbatim:
  half a 0.85 half b 1.2833            <- (0.8279+0.8721)/2 ; (1.3163+1.2503)/2  BRIEF CONFIRMED
  full a 1.7 full b 2.5666             <- docs/48 s3.2's "2.5667" reproduces
  band a 0.4180726741360727 2.2885078241395704   <- docs/48 s3.3's x0.418-x2.289 CONFIRMED
  band b 0.28641885831255876 3.7295963103109484  <- x0.286-x3.730 CONFIRMED
  union log width 2.5665999999999998
  registered band 0.7246981903299029 1.3798847759572466 full 0.644   <- +-38 % / +-0.322 ln
  LOO range 0.8602 exp 2.363633373110901          <- 6.0214/7 ; deleting one station = x2.36
  kmin all18 342km 9.556294047770173 10.5888334739482 central 10.409199682619848
  registered 2.12x 2.122392521012205              <- exp(0.00216*348.4) CONFIRMED
  CAL8 corrected 173.0706685816207                <- exp(0.0838*61.5) CONFIRMED
  1/f 2.315136361531694 3.976775630318937  ln ratio 0.5410027585442313
  11.8f 2.9672280000000004 5.096892
  sd ratios 4.2189 4.2190 4.0057 3.1759 4.9104
  412 411.77777777777777                          <- 4.0766/0.0099
DECISION: the band on the LEVEL is the RECIPROCAL of the residual CI (r_i = ln(sim/obs), so the
level correction is exp(-r)). That is why docs/48's [-0.8279,+0.8721] maps to x0.418-x2.289 and
not to x0.437-x2.392. Verified, not assumed.

## 03 - DEFECTS I FOUND IN THE BRIEF ITSELF (report, do not propagate)
 (i) The brief says "docs/45 s2.3 and s6.2 item 4 carry the asserted SDR = 1.0 ... claim".
     MEASURED: docs/45 s6.2 has THREE items (lines 538-549), no item 4. The "item 4" is
     docs/47 s6.2 item 4. docs/45's SDR=1.0 sites are s2.3 (the claim in registered words),
     s4.2 G5 (the two legs) and s4.2 G1.2 (the sentence). Citing those.
 (ii) The brief says "the CAL-8 form measures 0.0130 /km against a registered 0.0209".
     docs/48 s4.3 WITHDREW 0.0130 as arithmetically impossible as labelled (k_min prop sigma;
     a sigma 4.22x larger cannot give a SMALLER k_min) and traced it to the 10-STATION
     CAL-window set that includes 21237020 ARRANCAPLUMAS, an EVAL station docs/45 s2.4
     registers OUT of the fit (measured 0.01230 /km there; ARRANCAPLUMAS alone supplies 87.6 %
     of that set's Sum(Lw-Lbar)^2). The corrected CAL-8 figure is 0.0838 /km. THE DOC WINS.

## 04 - TWO THINGS docs/48 REFERRED TO ME AS docs/45's OWNER, WHICH I THEREFORE DECIDE
 (P1, docs/48 s6.1) WHICH ESTIMATOR'S BAND IS BINDING -> the UNION over (a) and (b), as a
     reporting convention and explicitly not a statistical claim. Ground: docs/45 s6.1 already
     makes estimator disagreement an INDETERMINATE trigger for VERDICTS, so it cannot be
     resolved by picking a winner for a BAND; docs/42 s9 registers (b) primary and docs/45 s7.1
     registers the objective on (a); neither doc may be edited. Per-estimator bands print beside.
 (docs/48 s4.2) THE STRONGER/WEAKER PHRASING DEFECT -> settled on **WEAKER**. A detection floor
     says nothing weaker than X is visible. docs/45 s2.3 and G1.2 wrote "stronger"; s2.2 wrote
     "weaker". Only "weaker" is the correct sense. Registered in the corrected sentence.

## 05 - BODY STRIKES (docs/37 A2.7 pattern: ~~struck~~ + dated pointer, NOTHING DELETED)
Applying now, then s8.

## 06 - APPLIED. Verification of the written file (executed output, not exit codes)
Body strike sites applied (line numbers AFTER the edits):
  :32  s0 table       k_min 0.0209 -> 0.0838                        strike + inline pointer
  :98  s2.1           "2.37x-3.00x" struck + [WARN] AMENDMENT 3 block at :101-:110
  :135 s2.2           0.1644 / +-38 % / 0.724x-1.380x struck; +-28.8 % WITHDRAWN (same row)
  :137 s2.2           k_min 0.0209 / 3.54x struck -> 0.0838 /km, ~173x over 61.5 km
  :173 s2.3           "2.12x over 348.4 km ... 0.00216 /km" struck + [WARN] AMENDMENT 1 block
  :224 s2.4           "keeps its k_min = 0.00216 /km" struck -> 0.0065-0.0069
  :228 s2.4           "0.0209 /km instead of 0.00303 /km" struck; FACTOR 6.9 KEPT (sigma cancels)
  :281 s3.1           "SE of the fleet level = 0.1644 ln" struck -> 0.4775 / 0.6936
  :430 s4.2 preamble  [WARN] AMENDMENT 1 block: sigma_r's permitted vs retired uses, and the
                      explicit UNAFFECTED list (G1.1 0.658, G8 0.465, G11 0.465, b_obs 0.464,
                      SE(beta) 0.0199, G12 0.644, all sigma-cancelling ratios)
  :477 G1.2           "~2.12x over 348.4 km at best" struck -> ~10x over ~342 km, "WEAKER" sense
  :483 G3.3           x4.2 / x2.9 annotated -> OPEN ITEM O8, no corrected number, safe direction
  :493 G12            "the registered 95 % level band of +-0.322 ln (+-38 %)" struck -> STANDALONE
                      fragility threshold, value RETAINED at 0.644 ln full width; pre-fit LOO
                      0.8602 > 0.6445 => the comparison ALREADY EXCEEDS (x2.36 per deletion)
  :544 s5.3           x4.2 annotated (O8) + "its +-38 % band" -> station-bootstrap band
  :592 s6.2 item 2    THE MANDATORY SENTENCE struck (two closed strikes, one per line) and
                      REPLACED inside a [WARN] AMENDMENT 1 block, with the materiality-bar
                      prohibition (docs/52 s7 item 2) stated in the same block
  :642 s7.1 card      "level SE 0.1644 ln (+-38 %)" struck -> the station bootstrap, a PROCEDURE
  :644 s7.1 card      Amendments: none -> THREE, named, dated
  :670 s7.2           the "does not ... produce a number that any gate here judges" bullet
                      ANNOTATED, NOT STRUCK - it stays true of its own pass
s8 written: 8.1 Amendment 1 (:700) . 8.2 Amendment 2 (:945) . 8.3 Amendment 3 (:1103) .
8.4 Disclosure (:1157). File 615 -> 1201 lines.
MECHANICAL CHECKS, executed:
  tables checked: 20   mismatched: 0        (all markdown tables column-consistent)
  ~~ occurrences: 34, even; per-line parity odd lines: []   (no strike spans a line break)
  [WARN] AMENDMENT blocks: 7
  docs/46 s2.5.1's OTHER derived strings ("3.9 - 5.0", "2.0 - 9.9", "11.8 - 14.9", "104.8",
  "126.1", "99.7"): grep finds them ONLY inside my own s8.3 clause quoting them => docs/45
  prints none of them => nothing further owed here. Claim verified, not assumed.
NOT TOUCHED, verified by grep: s2.1's alpha box [2.0, 30.0] (T4/B2 owns it) . the bar
[-0.26, 0.44] . beta box . G2.3 . the 5,482 budget . DDS seeds 20260921-24 . CAL 8 . windows .
every s6.1 outcome condition. No engine default, no frozen artifact, no git command.

## 07 - TWO ON-DISK CHECKS THAT CHANGED WHAT I WROTE (measured, not assumed)
 (a) I had drafted "docs/42 s9.5's mandatory pointer still carries the withdrawn 0.0130 /km
     (docs/42:805)". GREPPED docs/42 on disk: a PARALLEL AGENT HAS ALREADY REPAIRED IT -
     docs/42:863 now reads "~~**0.0130 /km**~~" and :869-870 carry amendment A-P4 (s9.7,
     2026-08-12) withdrawing it and CONFIRMING the all-18 figures. Corrected my s8.1.6 item 4:
     nothing is owed to docs/42 there any longer.
 (b) GREPPED docs/43: :191 STILL prints "0.465/sqrt(8) = 0.1644 ln = +-38 % (0.724x-1.380x).
     13 stations would have given +-28.8 %", and docs/43 has NO amendment slot entry for it.
     So the parallel docs/43 s3.2 enactment had NOT landed at my write. I therefore label my
     consistency claim honestly in s8.1.2: consistency is BY CONSTRUCTION (same route docs/48
     s3.3 = route 2 of docs/47 s2.2, same source document, same numbers), NOT verified against a
     written docs/43 amendment. Reported to the orchestrator.
Final mechanical re-check after these two edits: tables 20 / mismatched 0; ~~ even, no odd line.
