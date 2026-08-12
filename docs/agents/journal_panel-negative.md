# Journal - panel-negative (C3.1 ls_formulation decision panellist, NEGATIVE-prior lens)

Opened 2026-08-12. Read-only panellist. I own ONLY this file.

## Lens
Default posture: docs/46 §7's NEGATIVE - UNRESOLVED branch is the honest outcome; ADOPT-SOURCE
is what a session reaches because it wants C4.3 unblocked. Test that hard.

## Log

### Step 0 - journal created

### Step 1 - read the standing corpus (2026-08-12)
Read in order: CLAUDE.md (given in context), docs/47_c4_entry_verdict.md (full),
docs/46_ls_preregistration.md (full, 1400 lines, in three passes), docs/51_ls_freeze_decision.md
(full). Next: docs/52, docs/53.

Notes carried forward that are load-bearing for my lens:

- docs/46 §4.2 outcome table has THREE rows only. Their conditions:
  * ADOPT-SOURCE: (i) all four levers CITED; (ii) H-M's (R6) not triggered; (iii) "the §3.3 exact
    re-run completed AND REPORTED, INCLUDING THE STRATIFIED REPORT"; (iv) "the §4.3 forbidden
    evidence untouched".
  * ADOPT-BAND: ">= 1 lever CITED but ambiguous - i.e. two admissible readings survive on the
    source text". Trigger = EXISTENCE of a second admissible reading, whatever the gap.
  * NEGATIVE - UNRESOLVED: ">= 1 lever with NO CITABLE GROUND EITHER WAY, or (R6) fires, or the
    source text cannot be obtained/verified".
- docs/46 §4.2 third note: "Reachable != exercised ... §3.3's full stratified report is NOT
  discharged - elevation strata exist for every variant, SLOPE TERCILES DO NOT, and the
  per-station erosion-weighted LS-bar exists only as ratios (docs/47 §4.4) - and it is required
  before ADOPT-SOURCE is *exercised*, though not before this freeze (docs/51 §7 item 9)."
- docs/46 §1.2 last para: "The one evidentiary condition that HAS changed is §4.2 item 5's: all
  four levers now reach CITED, which makes ADOPT-SOURCE REACHABLE - and reachable is not adopted."
- docs/51 §1.2: all four levers CITED (limiter p.94+p.98; m p.47 with Sf[%] verified; S p.48;
  L p.47 eq.13 with Xdir^m). docs/51 §5.2: the pre-committed NEGATIVE branch for the m lever
  DOES NOT FIRE - the PDF was obtained.
- docs/51 §7 item 9: the stratified report is "Needed before ADOPT-SOURCE is *exercised*, not
  before the freeze"; labelled "not a blocker".
- docs/46 §7.3 "Does not oblige, and explicitly does not license": ... "treating the incumbent V0
  as *validated* because it survived by default".
- docs/46 §4.2 item 1 (carried from docs/35 §9.3.2, FROZEN AND BINDS): "Fidelity to the transposed
  method wins BY DEFAULT - the source formulation ... is the registered default outcome."
  item 2: a deviation needs its own written source justification, dated, naming a citable reason
  why the source's choice is WRONG FOR THIS BASIN, written before the resulting basin total is
  computed. item 3: deviation requires the alpha band rescaled. item 4: ties break toward the
  LOWER LS; a tie may not be broken by the basin total.

### Step 2 - read docs/52, docs/53
- docs/52: bar STRUCK not rescaled, no number anywhere; (R10) retired, decided by citation;
  Delta_shape site gets the EXACT discriminator (=0). §7 item 4: "NOT a finding that ... the LS
  question is unresolvable. The opposite: all four levers are CITED, the source read whole is a
  POINT at x0.25146".
- docs/53: Delta_shape = 0.1299456916752905 (V4, norm 18, max CAL 8; argmax CAPITANEJO). Null
  control 2.22e-16. => BRANCH B MANDATORY. Also G6 discharged the SECOND erosion-weighted
  reproduction of the lower endpoint: f_ero(V4_dg) = 0.2514648985839397,
  f_area(V4_dg) = 0.24467900940970733. Under V4_dg the statistic is 0.1361987744 (also > 0).
  §6 item 1: "It is not an adoption of V4 or of V4_dg. ls2d_column is untouched."

### Step 3 - MEASUREMENT: the source PDF hash (does the NEGATIVE row's third disjunct fire?)
  $ python3.10 -c "<sha256 of data/raw/refs/buarque2015.pdf>"
  True 9646521
  3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037
  MATCH True
=> the source text IS obtained and IS verified, at a DURABLE path (data/raw/refs/, not a
   scratchpad; docs/51 §7 item 8's provenance debt is paid). NEGATIVE disjunct 3 DOES NOT FIRE.

### Step 4 - MEASUREMENT: I read the four sentences myself out of the PDF (pymupdf), not out of
a summary. PDF p.63 = printed 47; p.64 = printed 48; p.110 = printed 94; p.114 = printed 98.
  * printed p.47, eq. (13): L_k = [(Am_k + Lp_k^2)^(m+1) - Am_k^(m+1)] / [Lp^(m+2) . Xdir_k^m .
    (22,13)^m]  -- and "O fator de direcao Xdir ... igual a 1 quando a direcao entre eles e
    ortogonal, ou igual a 2^(1/2) quando a direcao e diagonal."  MATCHES docs/46 §2.5.2 verbatim.
  * printed p.47, eq. (14): 0,2 / 0,3 / 0,4 / 0,5 on Sf < 1 / 1<=Sf<3 / 3<=Sf<5 / Sf>=5,
    "onde Sf [%] e a declividade do pixel."  MATCHES docs/46 §2.2 verbatim. (R6) is closed.
  * printed p.48, eq. (18): "O fator de declividade S e dado por Wischmeier & Smith (1978):
    S_k = 65,41 . sin2(theta_k) + 4,56 . sin(theta_k) + 0,065 , sendo theta o valor de Sf em
    graus."  MATCHES docs/46 §2.3 / docs/51 §1 verbatim, INCLUDING the degrees conversion note
    that excludes the degrees reading of Sf.
  * printed p.94: "Na determinacao do fator comprimento de 'L', seu valor maximo foi limitado ao
    tamanho do pixel do MDE."  MATCHES.
  * printed p.98: "...por pixel do MDE com resolucao espacial de 500 m, o maior valor permitido
    pelo modelo para o fator L e igual ao limite da dimensao de cada pixel."  MATCHES - a second,
    independent sentence, exactly as docs/46 §2.1 claims. p.98 continues: "o valor maximo e grande
    e pode fazer com que as estimativas da erosao laminar do solo em areas ingremes, como nos
    Andes, seja superestimado (EPA, 2004)" - which is the source's own verdict underwriting §4.2
    item 4's tie-break toward the LOWER LS.
=> all four levers' READING clauses are verified by me at first hand. NEGATIVE disjunct 1 (">=1
   lever with no citable ground either way") cannot be made to fire on the ADOPTED formulation.

### Step 5 - arithmetic (read-only, python3.10). Output:
  f_ero=0.25146  1/f_ero=3.976775630318937   (at full precision 0.2514648985839397 -> 3.976698)
  f_area=0.2446790094097074  1/f_area=4.086987283512870 ; ero/area = 1.0277138 (docs/47 R7 1.0278)
  11.8*f_ero = 2.967228     (docs/46 §1.0 prints 2.967 at this end)
  5.9*f_ero  = 1.483614  23.6*f_ero = 5.934456   (docs/46 §1.0: 1.484 ... 5.935)
  35.4*f_ero = 8.901684     (docs/46 §1.0: 8.902)
  3.9*f_ero  = 0.980694 ; 2.0*f_ero = 0.502920 ; 30.0*f_ero = 7.543800 ; 3.40*f_ero = 0.854964
  ln(0.43194/0.25146) = 0.5410027585442313 (registered 0.5410)
  |ln 0.25146| = 1.3804713 (registered 1.3805) ; |ln 0.43194| = 0.8394686 (0.8395)
  299.5387088405831 * 0.25146 = 75.32200 (75.3235 with the full-precision f_ero)
  docs/47 §5.2 optima / f_ero: 0.258->1.0260 ; 0.625->2.4855 ; 1.289->5.1261  (docs/51 §6.2's
  1.026 / 2.485 / 5.126 reproduced to the last printed digit)

### Step 6 - MEASUREMENTS on repo state (each one checked, not assumed)
  $ grep -n "A3" docs/37_c3_closure.md   -> NO MATCHES. docs/37's last amendment is A2.7.
    mtime docs/37_c3_closure.md = 2026-08-11 12:14:42. The ENACTMENT AMENDMENT IS UNWRITTEN.
    => docs/47 B1 has NOT landed. (docs/agents/journal_c31-enactment.md, 2026-08-11 23:54, is a
    prior session that reached the same decision and stopped before writing A3. I did not copy
    its reasoning; I record that it converged independently.)
  $ grep -n ls2d_column src/mgb_sediment.py -> :757 / :801 / :864 all `= "ls2d_hs"`. Default
    UNMOVED, as every document says.
  $ header of data/processed/urh_ls2d_variants.csv:
    ['mini','urh','n_cells','area_km2','area_frac','V0_ours_2026_08','V1_lim_pixel','V2a_m_cap05',
     'V2b_m_step_eq14','V3_s_ws78','V4_buarque_2015','V4p_buarque_2015_cap','V5_L_dg96_fd']
    => THERE IS NO V4_dg COLUMN. The variant docs/46 §3.1 calls "the source formulation READ
    WHOLE" is NOT a committed product; docs/53 built it in scratchpad only
    (scratchpad/urh_ls2d_v4dg.csv), a loss mode docs/00 §6 names. docs/46 §3.1's "every variant is
    reachable BY NAME" is therefore FALSE for the one variant ADOPT-SOURCE would adopt. This is a
    defect in a file I do not own: REPORTED, not fixed.
  $ docs/45 §8 amendment slot: "Empty at registration." => docs/47 B2 (re-express the C4.3 gate in
    Pi / re-register the alpha box), B5 (replace the +-38% Pi band) and the §5.5 pre-fit-profile
    disclosure are ALL UNDISCHARGED. docs/35 §9 has 9.1/9.2/9.3 only - no alpha-box re-registration.
  $ grep -i tercile across docs/ scripts/ src/ -> only docs/33 & docs/36 (discharge/peak work) and
    the docs/46/49/50/51 statements that LS slope terciles DO NOT EXIST. Confirmed undischarged.

### Step 7 - THE TEST OF MY OWN PRIOR (NEGATIVE - UNRESOLVED). It FAILS, on all three disjuncts.
§4.2's NEGATIVE row: ">= 1 lever with NO CITABLE GROUND EITHER WAY, or (R6) fires, or the source
text cannot be obtained/verified."
  (a) no lever without citable ground: refuted by Step 4 - I read all four sentences myself.
  (b) (R6): CLOSED CITED (docs/46 §2.2 amendment (d), verified at Step 4).
  (c) source obtainable/verified: refuted by Step 3 (hash match, durable path).
=> the honest answer from the rule ALONE is that NEGATIVE is NOT LICENSED. My prior loses.

I then tested each item docs/47 §4.2 says the literature does NOT settle, against §4.2 item 5:
  1. S above tan-theta 0.50 (35.5% of the S signal; no primary source; no band) - does NOT unground
     the S lever, because docs/46 §2.3's grade note is explicit: "whichever S is adopted reaches
     CITED (both candidates are published and page-citable). The CHOICE between them is graded by
     rule §4.2, not by evidence about S itself."
  2. the "arbitrary" cap value (Renard et al. 2011 p.143) - the SOURCE states its own cap (p.94 +
     p.98); docs/47 O3 says what would settle it is "a written source-grounds choice under docs/46
     §4's decision ladder", i.e. the rule, which is what is being applied.
  3. moderate-vs-low rill:interrill m column - a question about OUR McCool-89 m (V0), not about the
     adopted eq.14 step. Irrelevant to the adopted formulation's grade.
  4. D&G 1996 unobtained - expressly answered by docs/46 §2.5.2: "does not need to be: §4.2 item 1
     registers fidelity to the transposed method, and the transposed method states the convention
     on its own printed page" (eq.13 + Xdir, printed p.47, which I read).
  5. alpha=11.8's like-for-likeness NOT SETTLED - not a lever; it is a property of the COMPARATOR.
     §4.3 forbids using ANY alpha band as evidence in ANY outcome, so it structurally cannot fire a
     §4.2 row. It bounds every ratio and must travel as a declared residue (§1.0 residue 3, §9.2).
=> READING OF ITEM 5 I TAKE: the NARROW/literal one. Item 5 asks whether the ADOPTED FORMULATION's
   four levers are CITED - a PROVENANCE test - not whether every open question in the neighbourhood
   is closed. Grounds: (i) every criterion item 5 lists is a provenance criterion ("verbatim,
   page-numbered, single admissible reading, Sf units verified"); (ii) §4.1's ladder defines CITED
   as "a page-numbered published source states the choice, with its conditioning; a single
   admissible reading"; (iii) §2.3 routes the S CHOICE to the rule and not to the grade; (iv) §8.2
   item 1 / §9.2 insist the LEVEL stays UNVALIDATED whatever is adopted, which only coheres if
   CITED never speaks to validity ("CITED is not validated"); (v) the BROAD reading makes item 5
   unsatisfiable in principle - O2 has no primary source and "no band is offered" - so NEGATIVE
   would be the only reachable row FOREVER, converting a decision rule into a permanent stall in
   which an admittedly-unvalidated incumbent runs by default, which §7.3 expressly forbids
   ("does not license ... treating the incumbent V0 as VALIDATED because it survived by default").

WHERE THE BROAD READING DOES HAVE FORCE, recorded because it is the honest residue: docs/47 §4.1
grades CITED the fact that W&S-78's own authors withdrew it for steep slopes (Renard et al. 1991
JSWC 46(1) p.32; 2011 ch.8 p.142), and Schmidt et al. 2019 limits every S factor to <50% slope.
That is exactly the material a §4.2 ITEM 2 DEVIATION justification would need - "a citable reason
why the source's choice is wrong FOR THIS BASIN". No such justification is written or dated
anywhere in the repo, so item 1's default stands. And I may NOT quote a number for such a
composition: V1+V2b+McCool-S+eq.13-L has never been measured, and the STANDING INSTRUCTION forbids
forming it as a product of single-lever factors (joint/product = x1.34762 is why).

### Step 8 - the two objections I could NOT dismiss cheaply, both recorded
(A) THE SUPREMACY OBJECTION - the strongest thing against my own verdict's NUMBER.
    docs/46 §0 says: "It does not supersede docs/35 §9.3 ... where the two disagree, docs/35 WINS
    and this file is the bug." I read docs/35 §9.3.2 item 1 in the frozen original
    (docs/35:704-760): it defines the registered default outcome as "slope length limited to one
    DEM pixel, m stepped AND CAPPED AT 0.5 (his eq. 14), S = Wischmeier & Smith 1978 (his eq. 18)"
    - THREE levers, and it does NOT name the L form. Read literally, docs/35's registered default
    is V4 (f_ero 0.43194, alpha reference 5.097), NOT V4_dg (0.25146, 2.967). docs/46 §2.4's
    amendment relabelling V4 "a documented hybrid, not the source formulation" is precisely the
    kind of disagreement §0 hands to docs/35.
    Why I still land on V4_dg, twice over:
      (i) purposive: item 1's OWN stated rationale is level fidelity - "Because MUSLE is linear in
          LS, an LS level that differs from the source's passes one-for-one into alpha and silently
          invalidates the §6.1 guard." Keeping OUR point-rate L leaves a x1.7177 level discrepancy
          against the source (ln 0.5410), which is the exact failure item 1 exists to prevent.
      (ii) item 1's enumeration is ALREADY KNOWN DEFECTIVE in the same sentence: "m stepped and
          capped at 0.5" conflates the step with min(m,0.5) - Defect A - and docs/46 §7.3 item 2
          records that this very label in docs/35 §9.3.1 is WRONG and owed correction. An
          enumeration with a known-false element cannot outrank the printed source page.
      (iii) and if one insists the two registrations genuinely conflict and both compositions are
          live candidates, §4.2 ITEM 4 breaks it: "Ties break toward the LOWER LS level" -
          0.25146 < 0.43194. Same answer.
    I keep (A) as my strongest self-objection because it is the objection that would change the
    NUMBER downstream consumers use, and because §0's supremacy clause is unqualified.

(B) THE (R1) SECOND-READING RESIDUE - the one place ADOPT-BAND could still be argued.
    docs/46 §1.2 reads (R1) out as "does not fire ... single admissible reading". Reading p.94/p.98
    myself, the sentences cap the L FACTOR "ao tamanho do pixel"/"ao limite da dimensao de cada
    pixel" - dimensionally loose (L is dimensionless), so an adversary can propose a second
    construction of the SAME cap: not a_in -> 0 (the head-cell degeneration docs/46 §2.5.2
    registers) but Am capped AT one pixel area, Am = Lp^2. Measured consequence on eq.13's
    numerator, [(Am+Lp^2)^(m+1) - Am^(m+1)]:
        m=0.2 -> x1.2974 ; m=0.3 -> x1.4623 ; m=0.4 -> x1.6390 ; m=0.5 -> x1.8284
    i.e. the alternative reading gives a HIGHER L, hence a HIGHER f_LS. So even if it were admitted
    and (R1) fired, §4.2's ADOPT-BAND row directs "adopting the LOWER-LS reading under item 4, AND
    carrying f_LS as an explicit band" - and the lower-LS reading is the registered one, f_ero
    0.25146. THE ADOPTED VALUE IS THE SAME UNDER ADOPT-SOURCE AND UNDER ADOPT-BAND; only an extra
    band-carrying obligation would attach. docs/46 §1.2's read-out is frozen and in force, so I
    follow it (ADOPT-SOURCE) and journal the objection, per the freeze's own instruction. I also
    note the residue is on the SAME side as the yield-safe direction and cannot be used to raise
    the LS.
    Cross-check on the area basis: 39.812 / 9.741 = 4.087055 vs 1/f_area = 4.086987 - the
    "mean(LS_ours)/mean(LS_source)" of §4.2 item 3 is literally the AREA-weighted 4.0870, while
    §3.3's precedence rule ("f_ero decides; f_area is reported beside it, always, and can never
    override it") makes the DECIDING rescaler the erosion-weighted 1/f_ero = 3.9768.

### Step 9 - VERDICT (recorded before I wrote the structured object)
OUTCOME = ADOPT-SOURCE. ls_formulation = buarque_2015_dg (V4_dg). f_LS(ero) = 0.25146
(0.2514648985839397 at full precision; two independent erosion-weighted reproductions), area proxy
0.2446790094097074 (three). GRADE: CITED attaches ONLY to "each of the four levers of the adopted
formulation is stated by a page-numbered sentence of the transposed source on a single admissible
reading"; the LS LEVEL is and stays UNVALIDATED (docs/42 G4.2, docs/46 §8.2 item 1, §9.2); the
number 0.25146 itself is DERIVED (twice, behind gates) but it is the source's formulation ON OUR
TERRAIN (§1.0 residue 1) - it is not "his LS"; alpha=11.8's like-for-likeness is UNRESOLVED / NOT
SETTLED, no band.
NOT EXERCISABLE TODAY: §3.3's stratified report (slope terciles absent; per-station erosion-weighted
LS-bar only as RATIOS) is the third limb of the ADOPT-SOURCE condition, and §4.2's third note plus
docs/51 §7 item 9 and docs/46 §9's closing note all say it is required BEFORE ADOPT-SOURCE is
EXERCISED. So C3.1 records the outcome and does NOT propose the default switch.
C4.3: NO, not unblocked. B1 (docs/37 §A3) unwritten; B2 + B5 + the §5.5 disclosure undischarged
(docs/45 §8 empty, docs/35 §9 has no alpha-box re-registration); §6.2 says C4.3 starts "once B1-B4
land". Branch B is mandatory twice (§6.3 B1 on Delta_shape 0.1299456916752905 > 0; §6.3 B2 because
ADOPT is unreachable under A3), and §6.3 B5 holds until the enactment amendment exists.
RETAIN-OURS-WITH-DISCREPANCY-DECLARED is NOT a §4.2 row: only the NEGATIVE row's licence column
mentions keeping V0 ("because it is incumbent, not because it won"), and NEGATIVE's condition does
not fire. It is an accurate description of the INTERIM ENGINE STATE under ADOPT-SOURCE (which
licenses only PROPOSING the default switch), not an outcome.
DEFECT REPORTED, NOT FIXED: urh_ls2d_variants.csv has no V4_dg column, so the adopted variant is
not reachable by name in any committed product - docs/46 §3.1's own requirement fails for exactly
the variant ADOPT-SOURCE adopts. Owner: whoever owns scripts/c3/ and data/processed/.
