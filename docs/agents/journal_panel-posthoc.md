# Journal - panel-posthoc (post-hoc-hazard auditor lens)

Opened 2026-08-12. Role: READ-ONLY decision panellist for the C3.1 `ls_formulation` decision
under docs/46 §4.2. I write NOTHING but this file.

## 0. Plan
1. Read CLAUDE.md, docs/00_INDEX.md, docs/47, docs/46 (esp. §1.0, §1.2, §2.0, §2.2, §2.5.2, §3.1,
   §3.3, §4.2, §4.3, §4.4, §5, §6, §7.3, §8.2, §9, §10), docs/51, docs/52, docs/53.
2. Verify the Buarque quotes as transcribed (docs/46 §2.2/§2.5.2, docs/51 §1). Re-hash the PDF.
3. Apply §4.2 rule mechanically. Refuse §4.3 forbidden evidence explicitly.
4. Arithmetic on published factors only, read-only python3.10.

## 1. Reading log

### 1.1 Read (2026-08-12)
- CLAUDE.md, docs/00_INDEX.md (via context), docs/46 (all 1399 lines), docs/47 (all 677 lines).
- Key extractions from docs/46:
  - §4.2 rule: items 1-4 carried from docs/35 §9.3.2 (frozen, binds); item 5 = all four levers CITED.
  - Outcome table: ADOPT-SOURCE conditions = (a) all four levers CITED [MET, §4.2 item 5 amd (d)];
    (b) H-M (R6) not triggered [MET, Sf is percent]; (c) the §3.3 exact re-run completed AND
    reported, INCLUDING THE STRATIFIED REPORT; (d) §4.3 forbidden evidence untouched.
  - §4.2 third note: "Reachable != exercised... §3.3's FULL STRATIFIED REPORT is not discharged --
    elevation strata exist for every variant, SLOPE TERCILES DO NOT, and the per-station
    erosion-weighted LSbar exists only as ratios (docs/47 §4.4) -- and it is required before
    ADOPT-SOURCE is *exercised*, though not before this freeze (docs/51 §7 item 9)."
  - §4.2 second note: "[0.25146, 0.43194] is NOT an ADOPT-BAND band and may not be presented as
    one." ADOPT-BAND trigger = existence of a second admissible READING OF THE SOURCE. All four
    levers have a SINGLE admissible reading => ADOPT-BAND IS NOT TRIGGERED ON ANY LEVER.
  - NEGATIVE-UNRESOLVED condition: ">= 1 lever with no citable ground either way, or (R6) fires,
    or the source text cannot be obtained/verified." NONE of the three obtains.
  - §2.5.2: with eq.13 printed p.47, NO admissible reading of Buarque in which L is our
    point-rate form => the hybrid x0.43194 is NOT a reading of the source.
  - §8.2 item 1 + §9.2: the LEVEL stays UNVALIDATED whatever is adopted. "Cited is not validated."
  - §10 amd 1: Delta_shape = 0.1299456916752905 > 0 => B1 fires => BRANCH B MANDATORY.
  - §7.3 item 5: the enactment amendment is docs/37 §A3, dated, written by the C3.1 owner. That,
    not the freeze, is docs/47's B1 unblocking event.

### 1.2 Read (cont.)
- docs/51 (all 509 lines), docs/52 (THE DECISION block + §1 head), docs/53 (THE ANSWER + §7-§9).
- docs/35 §9.3 IN FULL (lines 678-790) -- because docs/46's own header says "where the two
  disagree, **docs/35 wins** and this file is the bug." THIS MATTERS: see §3 below.

## 2. MEASUREMENTS I MADE MYSELF (read-only)

### 2.1 The source of record, re-hashed
    python3.10 -c "hashlib.sha256(Path('data/raw/refs/buarque2015.pdf').read_bytes())"
    -> 9646521 bytes
    -> 3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037
MATCHES docs/38 §9.1 / docs/51 §1 byte-for-byte and digit-for-digit. The page map therefore holds
(PDF 63 = printed 47). 182 pages, as recorded.

### 2.2 All four levers checked against the printed page (PyMuPDF text extraction)
Printed p. 47 (PDF 63), extracted verbatim:
  - eq. (13): L_k = [(Am_k + Lp_k^2)^(m+1) - Am_k^(m+1)] / [Lp^(m+2) . Xdir_k^m . (22,13)^m]
    and "O fator de direcao Xdir corresponde a distancia entre dois pixels vizinhos, definida
    como igual a 1 quando a direcao entre eles e ortogonal, ou igual a 2^(1/2) quando a direcao
    e diagonal."  => docs/46 §2.5.2 / docs/51 §1.1 transcription CONFIRMED, including the
    denominator position of Xdir^m.
  - eq. (14): the four-branch step 0,2 / 0,3 / 0,4 / 0,5 on Sf<1 / 1<=Sf<3 / 3<=Sf<5 / Sf>=5,
    followed by "onde Sf [%] e a declividade do pixel."  => (R6) CONFIRMED. Sf IS PERCENT.
  - body text: "O fator de declividade S e calculado pela equacao de Wischmeier & Smith (1978)."
  - eq. (15) IS the dimensionless gradient sqrt((dz/dx)^2+(dz/dy)^2) -- docs/46's "the source is
    internally loose" residue is real and I confirm it. It does NOT create a second admissible
    reading: the [%] tag is explicit, and eq. 18's "sendo theta o valor de Sf em graus" excludes
    the degrees reading.
Printed p. 48 (PDF 64): eq. (18) S_k = 65,41.sin^2(theta_k) + 4,56.sin(theta_k) + 0,065,
  preceded by "O fator de declividade S e dado por Wischmeier & Smith (1978):" and followed by
  "sendo theta o valor de Sf em graus."  => CONFIRMED, formula AND attribution.
Printed p. 94 (PDF 110): "Na determinacao do fator comprimento de 'L', seu valor maximo foi
  limitado ao tamanho do pixel do MDE."  => CONFIRMED verbatim.
Printed p. 98 (PDF 114): "por pixel do MDE com resolucao espacial de 500 m, o maior valor
  permitido pelo modelo para o fator L e igual ao limite da dimensao de cada pixel."
  => CONFIRMED verbatim. The second independent sentence is real.
Printed p. 121 (PDF 137): "Apesar dos valores de comprimento (L) obtidos para cada pixel do MDE
  seja limitado pela resolucao de 500m, o valor maximo e grande e tende a fazer com que as
  estimativas da erosao laminar do solo em areas ingremes, como nos Andes, seja superestimado
  (EPA, 2004)."  => CONFIRMED verbatim; p. 98 carries the same sentence with "pode fazer".
  THIS IS docs/35 §9.3.2 ITEM 4's TIE-BREAK GROUND, AND IT IS CITED AND VERIFIED.
  Also p. 121: "os principais processos erosivos existentes sao decorrentes de erosao em massa,
  com desmoronamento de encostas ... o que e incompativel com o uso da MUSLE" -- docs/47 §4.2
  item 7 CONFIRMED.
=> FOUR LEVERS, FOUR PAGES, EVERY QUOTE AS TRANSCRIBED. No second admissible reading found on any
   of the four. ADOPT-BAND's trigger (a second admissible reading) DOES NOT FIRE.

### 2.3 On-disk state of the variants (read-only)
    head -1 data/processed/urh_ls2d_variants.csv
    -> mini,urh,n_cells,area_km2,area_frac,V0_ours_2026_08,V1_lim_pixel,V2a_m_cap05,
       V2b_m_step_eq14,V3_s_ws78,V4_buarque_2015,V4p_buarque_2015_cap,V5_L_dg96_fd
THERE IS NO V4_dg COLUMN. docs/53 §8 confirms it was written to scratchpad only. So the variant I
am about to name as adopted IS NOT REACHABLE BY NAME from a committed products file. That is a
prerequisite of the DEFAULT SWITCH (act 2 below), not of the §4.2 outcome. REPORTED, not fixed.

### 2.4 Stratified levels for V4_dg -- they DO partly exist
From data/processed/ls2d_defect_b.json (read-only), V4_dg / V0 area-weighted, by elevation band:
    basin           9.7412243757 / 39.8122601493 = 0.2446790094   (== the registered f_area)
    lowland <200m   0.7498974751 /  2.0154580158 = 0.3720729826
    mid 200-1000m   9.2002285415 / 36.9270584716 = 0.2491459900
    andean >1000m  15.7045714457 / 65.1993985592 = 0.2408698821
Elevation strata therefore EXIST for the adopted variant. SLOPE TERCILES DO NOT (searched; none),
and the per-station erosion-weighted LSbar exists only as RATIOS (docs/47 §4.4), not as levels.
=> docs/46 §4.2 note 3 and docs/51 §7 item 9 CONFIRMED BY MEASUREMENT: the §3.3 stratified report
   is PARTIAL. This is the one ADOPT-SOURCE condition that is not met today.
NOTE, and I decline to use it as evidence: no stratum reverses direction (0.372 / 0.249 / 0.241).
That is a §3.3 REPORTING fact, not a ground for the choice. The choice is the source reading.

### 2.5 Arithmetic, all reproducing published values
    1/0.25146 = 3.976776            (registered 3.9768)
    0.43194/0.25146 = 1.717728      (docs/46 §4.4's x1.7177 -- the BINARY)
    ln(0.43194/0.25146) = 0.541003  (registered 0.5410)
    |ln 0.43194| = 0.8395 ; |ln 0.25146| = 1.3805   (both registered)
    f_ero/f_area = 0.25146 / 0.2446790094097074 = 1.027714 (docs/47 R7: 1.0278) CONSISTENT
    299.5387088405831 x 0.25146 = 75.322 Mt/yr (registered 75.3235; embargo: absolute flux only)
  alpha band rescaled at the ADOPTED f_ero = 0.25146:
    11.8 x f = 2.967228 ; 5.9 x f = 1.483614 ; 23.6 x f = 5.934456 ; 35.4 x f = 8.901684
  at the area proxy f_area = 0.2446790094097074:
    11.8 x f = 2.887212 ; 5.9 x f = 1.443606 ; 23.6 x f = 5.774425 ; 35.4 x f = 8.661637
  docs/51 §6.2's alpha-hat-equivalents at the point reproduce to the last printed digit (run only
  as a check on docs/51; I do NOT quote them -- my brief forbids quoting any alpha-hat).

### 2.6 DEFECT FOUND IN A FILE I DO NOT OWN -- reported, not fixed
docs/46 §1.0 and docs/51 §2.3 both assert ln(0.43194/0.25146) = 0.5410 = -ln 0.580685.
Measured: -ln(0.580685) = 0.543547, but ln(0.43194/0.25146) = 0.541003. Gap 0.002544 ln (0.25 %).
0.5410 corresponds to a ratio of 0.582164, not 0.580685; and docs/46 §1.2 (R3) separately lists the
L-form |ln f| as 0.5435, which IS -ln 0.580685. Both numbers are individually right (0.580685 is
docs/50's directly measured in-formulation L ratio; 0.582164 is the ratio of the 5-s.f. rounded
endpoints) -- the IDENTITY as written is not exact. Owner: docs/46 §10 / docs/51. Immaterial to
every verdict here. NOT FIXED BY ME.

## 3. THE ONE REAL TENSION I HAD TO ADJUDICATE
docs/35 §9.3.2 item 1 -- FROZEN, and docs/46's own header concedes docs/35 WINS on conflict --
enumerates the registered default outcome as THREE levers: "slope length limited to one DEM pixel,
m stepped and capped at 0.5 (his eq. 14), S = Wischmeier & Smith 1978 (his eq. 18)". It does NOT
name L. Read literally, docs/35's registered default is V4 = the HYBRID at x0.43194, and adopting
V4_dg would be a DEVIATION under item 2 -- whose ordering condition ("written before the resulting
basin total is computed") is now PERMANENTLY UNSATISFIABLE (docs/46 §4.4: 75.3235 and 129.3840 are
both published). On that reading ADOPT-SOURCE at V4_dg is barred outright.

Why I do not take that reading, and why it does not change the answer either way:
 (a) docs/35 §9.3.1, in the SAME amendment, ALREADY records the L lever ("With the literal
     Desmet-Govers finite-difference L instead of our continuous form, a further x0.790"). Item 1's
     parenthetical is an enumeration of the levers then measured, not a definition of the method.
 (b) Item 1's OPERATIVE principle is "Fidelity to the transposed method wins by default." Eq. 13 is
     printed on p. 47 OF THE TRANSPOSED METHOD -- I read it myself this pass. Our point-rate L is
     the deviation from the method; the finite-difference L is the method.
 (c) docs/35 §9.3.4 item 4 provides for exactly this: "If a different reading is adopted, the
     x0.351 row and the whole bracket must be recomputed and this section amended -- not quietly
     re-quoted." docs/35 pre-authorised its own bracket being superseded by a better reading.
 (d) AND THE DECISIVE ONE, which is contamination-proof: if a reader genuinely cannot tell which of
     V4 / V4_dg item 1's enumeration names, THAT IS A TIE. docs/35 §9.3.2 item 4 -- frozen -- breaks
     ties TOWARD THE LOWER LS, on the p.121/p.98 citation I verified verbatim, and adds "A tie must
     not be broken by the basin total." The lower LS is V4_dg. The tension therefore resolves to the
     SAME point by a rule that explicitly forbids the total from entering.

STILL OWED, and I say so rather than paper over it: a docs/35 §9 amendment recording that item 1's
three-lever enumeration is superseded by eq. 13's reading. Owner: docs/35's owner. Until it lands, a
later session can argue the hybrid is "the default" -- which is precisely the x1.7177 binary docs/46
§4.4 warns about, and it is the strongest objection to my verdict.

## 4. THE docs/46 §4.3 FORBIDDEN EVIDENCE I REFUSED (enumerated, so it is checkable)
1. The basin total (299.5387 / 129.3840 / 75.3235 Mt/yr). I computed 299.5387 x 0.25146 ONLY as a
   reproduction check of a published figure, and it entered NO step of the decision. For the record:
   my outcome lands the total FURTHEST from the anchors -- I decline to count even that as evidence
   in either direction, because docs/46 §3.5 pre-registers that an unattractive total is not
   evidence against the source formulation, and the symmetric statement binds me too.
2. The outlet anchors 144-184 Mt/yr and the distance between them. Not read, not used.
3. The retired "mountainous LS 2-10" band. NOT USED; docs/35 §9.3.5 trap 1 forbids the fingerprint
   (the source formulation's per-cell median 7.262 sitting inside 2-10).
4. The retired SDR 0.05-0.30 band and any implied-SDR arithmetic. Not used.
5. ANY alpha band. I computed 11.8 / 5.9 / 23.6 / 35.4 x f ONLY as §4.2 item 3's REPORTING
   obligation, AFTER the choice was fixed by the source reading. No band passed or failed anything.
   I also record that docs/47 §3.2 falsifies docs/35 §6.1's band as a sufficient guard anyway
   (check_musle_parameters STOPs 185 of 426 published pairs; 97.7 % land inside because the source's
   own search prior contains it).
6. ANY C4 fit at any stage. No fit run, no KGE_ln evaluated, no alpha-hat quoted.
7. check_musle_parameters' verdict (ok/watch/STOP). Not run, not read, not used.

## 5. VERDICT (recorded here before it entered the structured return)
OUTCOME = **ADOPT-SOURCE**. ls_formulation = **buarque_2015_dg** (V4_dg).
f_LS = 0.25146 erosion-weighted (2nd repro 0.2514648985839397); 0.2446790094097074 area proxy.
GRADES, by proposition: the FOUR-LEVER READING OF THE SOURCE = CITED; the FACTOR on our terrain =
DERIVED (2 erosion-weighted + 3 area-weighted reproductions), carrying docs/46 §1.0 residue 1 (it is
not "his LS"); the LS LEVEL ITSELF = UNVALIDATED, unchanged, forever inside this decision;
alpha = 11.8's like-for-likeness = NOT SETTLED / UNRESOLVED, no band.
NOT YET EXERCISABLE: §3.3's stratified report is partial (slope terciles absent, per-station LSbar
only as ratios) and H-S's (R7)/(R8) items 2-3 do not exist. Both are named ADOPT-SOURCE conditions.
Cheap, prospective, and they must land BEFORE docs/37 §A3 is written.
C4.3 UNBLOCKED? **NO.** docs/47 B1's unblocking event is the ENACTMENT AMENDMENT (docs/37 §A3),
unwritten; B2 unmet; B5 + the §5.5 disclosure unmet; docs/46 §6.3 B5 still holds because §A3 is
unwritten; and Branch B is MANDATORY on B1 (Delta_shape = 0.1299456916752905 > 0) and on B2
independently -- which is the BLOCKING direction: it closes the Branch A provisional-run escape
entirely, so there is no version of C4.3 that may run before LS lands.
ENGINE DEFAULT: owner = the C3.1 owner (whoever owns scripts/c3/ls2d.py + docs/37; commit 5eaabf5
delivered both under C3.1). TWO SEPARATE DATED ACTS: (1) docs/37 §A3, the written enactment
amendment, which only LICENSES proposing the switch; (2) the ls2d_column switch itself, which
additionally requires a durable gated V4_dg column in urh_ls2d_variants.csv (measured absent, §2.3)
because docs/46 §3.1 forbids overwriting urh_ls2d.csv / minibacia_ls2d.csv. Never C4's act
(docs/42 G4.2). No code edit substitutes for either.

## 6. Files written by me: this journal ONLY. No doc, script, notebook or data product touched.
No git command run. No engine default moved. No fit, no LS pass, no calibration, no simulation.
