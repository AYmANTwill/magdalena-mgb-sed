# Journal - agent slug `amend-35-label` (T2b: docs/35 §9.4 amendment)

Started 2026-08-12. Crash journal; appended as I go, never only at the end.

## Ownership
- WRITE: `docs/35_qpeak_preregistration.md`, `docs/agents/journal_amend-35-label.md`.
- Nothing else. Read-only everywhere else. Defects outside ownership get REPORTED, not fixed.

## Task (T2b)
1. JOB 1 - the eq.-14 MISLABEL in docs/35 §9.3.1 (`min(m,0.5)` is a CAP, not Buarque eq. 14).
2. JOB 2 - supersede docs/35's retired LS bracket (x0.333-x0.421 and its dependents).
3. JOB 3 - re-base §9.3.3's expected consequence from prior C 248.730 to adopted 299.5387088405831.
Method: new dated amendment `§9.4 - 2026-08-12` + strike-through/dated-pointer in the body
(house pattern: docs/37 A2.7 / docs/46 inline WARN). NOTHING DELETED.

## Log

### 00 - journal created (first action)

### 01 - reading pass
Read, in the ordered sequence: `CLAUDE.md` (context), `docs/00_INDEX.md`,
`docs/47_c4_entry_verdict.md` (the standing verdict: `C4.3-BLOCKED-UNTIL-LS-LANDS`),
`docs/46_ls_preregistration.md` IN FULL (1400 lines, three reads), then `docs/35` in full (785 lines).
Key bindings I extracted:
- docs/46 §7.3 item 1 = JOB 3 (re-base §9.3.3 to 299.5387 Mt/yr), item 2 = JOB 1 (the eq.-14
  mislabel, UNCONDITIONAL), item 3 = JOB 2 (the ×0.790/×0.333 bracket superseded, UNCONDITIONAL).
- docs/46 §1.0: the source read whole is a **POINT** at f_ero 0.25146; ×0.43194 is a documented
  HYBRID; the span between them is the `L`-form lever exactly.
- docs/46 §4.2 note 2: `[0.25146, 0.43194]` is NOT an ADOPT-BAND band and may not be presented
  as one. This is the structural correction JOB 2 asks me to record.
- docs/46 §5 row "The frozen pre-registrations": docs/35 is amended by ITS OWN owner in ITS OWN
  slot (§9), dated. That is what I am doing.
- docs/46 §3.5: the engine (erosion-weighted) loads are 129.3840 (V4) / 75.3235 (V4_dg) Mt/yr,
  and the proxy loads ≈126.1/≈99.7 are superseded. docs/35's own ≈104.8/≈82.8 are a THIRD,
  earlier pair (prior C level × proxy factor) - see measurement 03 below.

### 02 - SOURCE RE-VERIFIED FIRST-PARTY (not carried)
```
$ sha256sum data/raw/refs/buarque2015.pdf
3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037  (9,646,521 B)
```
MATCHES docs/38 §9.1's card, so the page map holds. Then I extracted the pages myself
(`PYTHONIOENCODING=utf-8 python3.10 -c "import fitz; ... d[62].get_text()"`):

PDF p. 63 = printed **p. 47** returns eq. (13) with `Xdir_k^m` in the denominator, then:
`m = | 0,2 se Sf < 1 | 0,3 se 1 <= Sf < 3 | 0,4 se 3 <= Sf < 5 | 0,5 se Sf >= 5   (14)`
`onde Sf [%] e a declividade do pixel.`
PDF p. 64 = printed **p. 48** returns `S_k = 65,41 sin^2(theta_k) + 4,56 sin(theta_k) + 0,065  (18)`,
`sendo theta o valor de Sf em graus.`
=> eq. 14 is a STEP FUNCTION ON SLOPE PERCENT, verified by me, not carried from docs/46.
`min(m_continuous, 0.5)` is a CAP and is a different object. JOB 1 is confirmed on the source.

### 03 - THE ARITHMETIC (python3.10, exact)
f_hi = 0.43194 (V4, the HYBRID), f_lo = 0.25146 (V4_dg, the POINT); C = 299.5387088405831.
```
1/f            : 2.315136361531694      3.976775630318937
                 (exact: 2.315114922304743 at 0.431944 / 3.9766981619750683 at 0.2514648985839397)
11.8*f         : 5.096892               2.9672280000000004
5.9*f          : 2.548446               1.4836140000000002
23.6*f         : 10.193784              5.934456000000001
35.4*f         : 15.290676              8.901684
3.9*f          : 1.684566               0.9806940000000001
C*f            : 129.38274989660147     75.32200372505304
C*f exact      : 129.38394805143685     75.32347104056149
144/L, 184/L   : 1.1129660545353368 / 1.4221232919062636   (V4, L=129.3840)
                 1.9117539678851887 / 2.4427967367421854   (V4_dg, L=75.3235)
ln(f_hi/f_lo)  : 0.5410027585442313      exp(-that) = 0.5821641894707599
-ln(0.580685)  : 0.543546837831505       <-- NOT equal to 0.5410 (see defect report)
C_adopted/prior: 299.5387088405831/248.730 = 1.204272539864846
248.730*0.421  : 104.71533   248.730*0.333 : 82.82709   <-- provenance of docs/35's 104.8 / 82.8 CONFIRMED
step/cap ratio from the 6-d.p. printed factors: 0.505092/0.502472 = 1.0052142208919104 area;
                 0.522043/0.517480 = 1.0088177320862641 ero. docs/49 registers x1.005212 / x1.008878;
                 the difference is rounding in the 6-d.p. inputs, so I QUOTE docs/49's registered
                 pair and do not present my own recomputation as authoritative.
```
DECISION: §9.4 prints the ENGINE (erosion-weighted) factors and loads, with the area proxy
carried BY REFERENCE to docs/46 §1.0/§3.1 "as corrected 2026-08-12" (a parallel agent owns the
upper area value; I may not hard-code a number I cannot verify).

### 04 - A DIAGNOSIS I DID NOT EXPECT: the `= -ln 0.580685` identity is a WEIGHTING MIX
`docs/46`:127 (§1.0) and `docs/51` §2.3 both print
`ln(0.43194 / 0.25146) = 0.5410 = -ln 0.580685`. Measured:
```
0.25146/0.43194                  = 0.5821641894707599   (EROSION-weighted L-form ratio)
ln(0.43194/0.25146)              = 0.5410027585442313 = -ln(0.5821641894707599)   OK
-ln(0.580685)                    = 0.543546837831505                              NOT 0.5410
0.2446790094097074/0.421475      = 0.5805303028879706   (AREA-weighted L-form ratio)
ln(0.421475/0.2446790094097074)  = 0.5438132778492345
```
So the two constituents are each correct but belong to DIFFERENT weightings: 0.5410 is the
**erosion**-weighted span and pairs with 0.58216 (= `docs/47` §3.1 R6's "0.5822 erosion-weighted");
**0.580685 is the AREA-weighted L-form ratio** (R6's "0.5807 area-weighted") and pairs with the
area-weighted span 0.5438. Gap 0.0025440792872737372 ln. IMMATERIAL to every verdict; the
identity as written does not hold. `docs/46` and `docs/51` are NOT MINE -> REPORTED, not fixed.
docs/35 §9.4 will print the erosion-weighted identity correctly and will not reproduce the bad one.
(The `a3-enactment` agent reported the same non-identity; my measurement adds the *cause*.)

### 05 - BODY EDITS APPLIED (strike-through + dated pointer, house pattern; NOTHING DELETED)
All at 2026-08-12, each pointing at the new §9.4:
1. §6.1 caveat (was line 339) - struck `2.37x-3.00x`; added an inline WARN reaffirming that the
   REGISTERED 5.9-23.6 / 35.4 / 3.9 are UNCHANGED.
2. §9 registration record, the Amendments cell (was line 472) - struck the inner `2.37x-3.00x`
   and appended the `§9.4 (2026-08-12)` entry.
3. §9.2 CONDITIONAL box (was 614-632) - WARN header with the whole old->new map, then each of
   2.37x-3.00x / x0.421 / x0.333 / 3.9-5.0 / 2.0-9.9 / 11.8-14.9 / 1.3-1.6 / 3.00x struck inline.
   Added the asymmetry note: the upper end barely moved (proxy bias 2.5 %), the lower end moved a
   lot (Defect B), so the tightening the box warns of is STRONGER than the box states.
4. §9.2 gate-(b) sentence (was 656) - struck `x0.421 ... x0.333 gives 104.8 ... 82.8 Mt/yr` and
   `implied SDR 1.37-2.22`; WARN gives the re-based 129.3840 / 75.3235 and reaffirms the
   conclusion (still below both anchors, direction failure would return) + ADR-not-SDR.
5. §9.3.1 lever table (was 696) - the `m` row RELABELLED (JOB 1) with both objects and all four
   factors; the joint row annotated "already used the STEP: it is V4, not V4'"; the `x0.790` /
   `x0.333-x0.421` / `2.37x-3.00x` paragraph struck; WARN carries the standing instruction on
   never quoting a product of single levers as the joint.
6. §9.3.2 item 1 (was 715-716) - struck "`m` stepped and capped at 0.5 (his eq. 14)"; WARN
   explains the phrase FUSES the two objects, states item 1's default outcome was always the
   STEP, and flags the fourth-lever exposure WITHOUT deciding the supremacy question.
7. §9.3.2 item 3 (was 725) - struck `2.37-3.00 / 2.0-9.9 / 11.8-14.9`; WARN gives the rescaled
   set and states item 3's RULE is unchanged.
8. §9.3.3 (was 733-744) - JOB 3: struck the whole prior-C proxy arithmetic; WARN re-bases to
   299.5387088405831 -> 129.3840 / 75.3235 and carries §9.3.3's own rule verbatim in intent.
   Also annotated the "Precision note" - discharged, proxy bias measured at ~2.5 %.
9. TWO SITES NOT IN MY BRIEF'S LIST, found by grep and corrected (both mine, both LS-conditional):
   §9.3.4 item 4 (the p. 94 interpretation risk - CLOSED by the p. 98 corroboration, limiter
   CITED) and §9.3.5 trap 2 (`2.4 - 3.0x` -> 2.3151x-3.9768x, and the trap binds HARDER because
   the C revision has since landed).

### 06 - §9.4 WRITTEN (785 -> 1243 lines)
Appended as a new final dated amendment `### 9.4 Amendment - 2026-08-12`, with subsections
9.4.1 (JOB 1, the mislabel) · 9.4.2 (JOB 2, the register of struck numbers) · 9.4.3 (the
structural POINT-vs-HYBRID correction) · 9.4.4 (JOB 3, the re-basing) · 9.4.5 (§6.1 is
LS-conditional - CONSEQUENTIAL RESTATEMENT, explicitly NOT a change to the registered band) ·
9.4.6 (what it does NOT do) · 9.4.7 (defects in files I do not own, REPORTED not fixed) ·
9.4.8 (disclosure + reproduction).

Two things I deliberately did NOT do:
- I did NOT touch §6.1's registered table (5.9-23.6 / 23.6-35.4 / >35.4 / <3.9). Verified
  byte-identical after all edits by reading lines 352-357. T4 owns the GATE re-expression and may
  only reach §9 as a PROPOSAL; §9.4.5 says so.
- I did NOT resolve the docs/35 §9.3.2-item-1 three-lever supremacy question (docs/35 enumerates
  three levers and does not name `L`, so read literally its registered default is the x0.43194
  HYBRID, not the x0.25146 POINT). That is an ADOPTION and adoption is docs/37 §A3's. §9.4.3
  states BOTH branches and exercises neither. Reasoning backwards from "the source read whole
  should win" would have been exactly the post-hoc move docs/47 §5.3 names.

### 07 - INTEGRITY CHECKS ON THE EDITED FILE (measured, not assumed)
```
line endings : CRLF 0 / bare LF 1243  -> pure LF, unchanged, no mixing introduced
table blocks : 21 parsed, 0 column-count mismatches (checker handles blockquoted + indented rows)
§9.4.x refs  : defined {9.4, .1-.8}; referenced {9.4, .1-.7}; DANGLING = [] (9.4.8 defined,
               never referenced - fine, it is the disclosure)
naked superseded numbers (occurrence outside any ~~strike~~): audited line by line. Every
  remaining live occurrence is one of (a) an explicit old->new correction arrow inside a dated
  WARN, (b) provenance arithmetic (248.730 x 0.421 = 104.715 etc., measured by me to prove where
  the struck numbers came from), or (c) a number that is NOT superseded - specifically x0.421 as
  the AREA-WEIGHTED PROXY OF THE JOINT, which docs/46 §3.1 registers live as f_area(V4)=0.421475
  and which reproduces the published row to 15 s.f. Nothing superseded is quotable as live.
originals preserved: "eq. 14, step function capped at **0.5**", "2.37x-3.00x", "x0.333 - x0.421",
  "x0.790", "104.8"/"82.8", "implied SDR 1.37 - 2.22", "m stepped and capped at 0.5 (his eq. 14)",
  "2.37 - 3.00, giving expected ~ 2.0 - 9.9 and hard stop ~ 11.8 - 14.9", "~ 3.9 - 5.0",
  "~ 1.3 - 1.6", "2.4 - 3.0x" - all still present and readable inside strike-throughs.
```
NO git command was run (prohibited), so the §6.1-unchanged claim is verified by re-reading the
table, not by a diff.

### 08 - FILES I WROTE, AND ONLY THESE
- `C:\dev\magdalena-mgb-sed\docs\35_qpeak_preregistration.md`
- `C:\dev\magdalena-mgb-sed\docs\agents\journal_amend-35-label.md`
Nothing else. No `data/` product, no frozen artifact opened (urh_ls2d.csv, minibacia_ls2d.csv,
urh_ls2d_variants.csv and everything under sim_calibrated_v2/ were never touched - this amendment
needs none of them). No engine default changed. No calibration, no fit, no alpha-hat, no LS pass,
no notebook execution, no KGE_ln against the docs/45 box.
