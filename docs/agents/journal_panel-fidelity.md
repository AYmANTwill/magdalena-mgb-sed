# Journal - panel-fidelity (read-only decision panellist)

Started 2026-08-12. Role: decide the C3.1 `ls_formulation` outcome from docs/46 §4.2's
decision rule ALONE, through the FIDELITY lens (item 1 default, item 2 deviation burden,
item 4 tie-break, item 5 levers CITED).

I write NO project file except this journal.

## Log

### 00 - setup
Created this journal as first action.

### 01 - reading pass
Read in order: CLAUDE.md (context), docs/47 (full), docs/46 (full, 1400 lines, three reads),
docs/51 §0-§2.1. Key load-bearing text captured:

- docs/46 §4.2 items 1-5 and the outcome table (lines 841-891).
- ADOPT-SOURCE's condition list has FOUR conjuncts: (i) all four levers CITED [MET, amd (d)];
  (ii) (R6) not triggered [MET, Sf is percent]; (iii) "the §3.3 exact re-run completed **and
  reported, including the stratified report**"; (iv) §4.3 forbidden evidence untouched.
- §4.2 note 3 "Reachable != exercised": the §3.3 full stratified report is NOT discharged --
  elevation strata exist for every variant, **slope terciles do not**, and the per-station
  erosion-weighted LSbar exists only as ratios (docs/47 §4.4). "required before ADOPT-SOURCE is
  *exercised*, though not before this freeze".
- §10's closing note: "H-S's field clause (R7)/(R8) and §3.3's slope-tercile stratified report are
  owed before ADOPT-SOURCE is exercised".
- ADOPT-BAND trigger is a SECOND ADMISSIBLE READING OF THE SOURCE TEXT, period. Not "external
  literature disagrees with the source's formula". Note in §4.2: "ADOPT-BAND is not currently
  triggered on any lever."
- NEGATIVE condition: ">= 1 lever with no citable ground either way, or (R6) fires, or the source
  text cannot be obtained/verified." All three fail.
- §2.5.2 (CITED, eq.13 p.47): "there is NO admissible reading of Buarque in which L is our
  point-rate form" => V4 (x0.43194) is a documented HYBRID, not a reading of the source; the
  source read whole is a POINT at f_ero 0.25146 / f_area 0.2446790094097074.
- §4.4's honest state: every basin total is ALREADY published; no session may claim to have written
  its justification before the total was computed. What survives: justification must be a SOURCE
  READING WITH A GRADE, and §4.3 binds absolutely.

### 02 - disk verification (read-only)
`head -1 data/processed/urh_ls2d_variants.csv` ->
  mini,urh,n_cells,area_km2,area_frac,V0_ours_2026_08,V1_lim_pixel,V2a_m_cap05,V2b_m_step_eq14,
  V3_s_ws78,V4_buarque_2015,V4p_buarque_2015_cap,V5_L_dg96_fd
  => **NO V4_dg COLUMN.** The adopted variant's column DOES NOT EXIST ON DISK.
`head -1 data/processed/urh_ls2d.csv` -> mini,urh,n_cells,area_km2,area_frac,ls2d,ls2d_hs,
  ls2d_mb86,ls2d_dg96  (ls2d_dg96 is Defect B's confounded column, NOT V4_dg)
`sed -n '855,875p' src/mgb_sediment.py` -> load_geometry(..., urh_ls2d: str = "urh_ls2d.csv",
  ls2d_column: str = "ls2d_hs", ...)  => the default switch is a TWO-parameter act
  (file + column), because V4_dg lives in neither file today.

### 03 - FIRST-HAND SOURCE VERIFICATION (the decisive step for a fidelity lens)
The brief says I may re-hash the PDF and must check the quotes as transcribed. I did both.

    python3.10 -c "import hashlib; print(hashlib.sha256(open('data/raw/refs/buarque2015.pdf','rb').read()).hexdigest())"
    -> 3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037   **MATCH** (docs/38 §9.1)
    ls -l -> 9,646,521 bytes  **MATCH**.  The CITED levers are no longer scratchpad-dependent.

The `Read` tool failed on the PDF (pdftoppm absent). Used PyMuPDF (`fitz`), read-only text
extraction, page map PDF p63 = printed p47 (offset +16):

    python3.10 -c "import fitz,io,sys; ...; d=fitz.open('data/raw/refs/buarque2015.pdf'); print(d[62].get_text())"   # printed 47
    ... d[63] ...   # printed 48        ... d[109], d[113], d[136] ...   # printed 94, 98, 121

**All four levers verified verbatim, first-hand. Every transcription in docs/46 §2.2, §2.5.2 and
docs/51 §1 is EXACT. Nothing is mis-quoted.**

1. **L (eq. 13), printed p.47** - `L_k = [(Am_k + Lp_k^2)^(m+1) - Am_k^(m+1)] / [Lp^(m+2) *
   Xdir_k^m * (22,13)^m]` (13), with *"O fator de direcao Xdir corresponde a distancia entre dois
   pixels vizinhos, definida como igual a 1 quando a direcao entre eles e ortogonal, ou igual a
   2^(1/2) quando a direcao e diagonal."* -> `Xdir^m` IS in the denominator. CITED confirmed.
2. **m (eq. 14), printed p.47** - `m = 0,2 se Sf<1 | 0,3 se 1<=Sf<3 | 0,4 se 3<=Sf<5 | 0,5 se
   Sf>=5` (14) **"onde Sf [%] e a declividade do pixel."** CITED confirmed; `Sf` is PERCENT.
3. **S (eq. 18), printed p.48** - `S_k = 65,41*sin^2(theta_k) + 4,56*sin(theta_k) + 0,065` (18),
   *"sendo theta o valor de Sf em graus"*, introduced by *"O fator de declividade S e dado por
   Wischmeier & Smith (1978)"*. **PLUS a THIRD independent attribution I found myself on p.47:**
   *"O fator de declividade S e calculado pela equacao de Wischmeier & Smith (1978)."* So the S
   reading rests on THREE sentences across two printed pages, not two. CITED confirmed, hardened.
4. **limiter, printed p.94** - *"Na determinacao do fator comprimento de 'L', seu valor maximo foi
   limitado ao tamanho do pixel do MDE."*  **printed p.98** - *"por pixel do MDE com resolucao
   espacial de 500 m, o maior valor permitido pelo modelo para o fator L e igual ao limite da
   dimensao de cada pixel."* Two independent sentences. CITED confirmed.
   Residue confirmed honest: **eq. 15** does write `Sf = sqrt((dz/dx)^2+(dz/dy)^2)` (dimensionless),
   with eqs. 16/17 as **centred differences over the FOUR ORTHOGONAL neighbours (Wilson & Gallant
   2000)**. docs/46 discloses the unit looseness; the *orthogonal-4* specificity is sharper than
   "his eq. 15 centred differences" and is a lever nobody has measured (we use Horn 3x3, which
   feeds BOTH m via Sf and S via theta). Reported, not fixed - it afflicts V0 and V4_dg alike and
   docs/46 §3.1 holds everything unnamed at V0.

### 03b - THE FIND THAT DECIDES THE FIDELITY LENS (item 4's ground, verified first-hand)
printed **p.98**, continuing the limiter sentence:
> *"Apesar de limitado pela resolucao do dado de topografia utilizado, **o valor maximo e grande e
> pode fazer com que as estimativas da erosao laminar do solo em areas ingremes, como nos Andes,
> seja superestimado** (EPA, 2004)."*

printed **p.121**: *"...os principais processos erosivos existentes sao decorrentes de erosao em
massa ... **o que e incompativel com o uso da MUSLE**"* and *"o elevado aporte de sedimentos ...
pode ainda estar relacionado com os valores do fator topografico LS, o qual possuem grande
sensibilidade ... Apesar dos valores de comprimento (L) ... seja limitado pela resolucao de 500m,
**o valor maximo e grande e tende a fazer com que as estimativas ... nos Andes, seja
superestimado**."*

**=> The source's own author states that his ALREADY-CAPPED L still OVER-estimates Andean sheet
erosion.** docs/46 §4.2 item 4's stated ground ("Buarque p.121's own verdict that his Andean LS is
already an over-estimate, and our limiter is looser than his") is therefore VERIFIED FIRST-HAND and
is stronger than docs/46 states (p.98 says it too, independently). Every direction the source itself
points is DOWN. There is no sentence anywhere in the source that could support raising the level.

### 04 - ARITHMETIC (read-only, published factors only)
    python3.10 -c "f_ero=0.25146; f_area=0.2446790094097074; ... c*f for c in (3.9,5.9,11.8,23.6,35.4)"
docs/35 §6.1 read first to get the band right (`grep -n '35\.4|5\.9|23\.6' docs/35`): line 346
expected **5.9-23.6** (0.5x-2x Williams); 347 watch 23.6-35.4; 348 HARD STOP alpha>35.4;
349 HARD STOP **alpha<3.9** (1/3 x Williams). NOTE 3.9 = 11.8/3, NOT a rescaled LS number - I
checked that before assuming it, because 3.9 coincides with the superseded 11.8x0.333.

| c | c * f_ero(0.25146) | c * f_area(0.2446790094097074) |
|---|---|---|
| 3.9  lower hard stop | **0.98069400** | 0.95424814 |
| 5.9  band lo         | **1.48361400** | 1.44360616 |
| 11.8 reference       | **2.96722800** | 2.88721231 |
| 23.6 band hi         | **5.93445600** | 5.77442462 |
| 35.4 upper hard stop | **8.90168400** | 8.66163693 |

1/f_ero = **3.9767756303**, ln f_ero = -1.3804713478; 1/f_area = 4.0869872835.
Reproduces docs/46 §1.0's published lower-end column (2.967 / 1.484 / 5.935 / 8.902) EXACTLY.
On the exact second reproduction f=0.2514648985839397: 11.8f=2.96728580, 35.4f=8.90185741,
5.9f=1.48364290, 23.6f=5.93457161, 1/f=3.9766981620, load=299.5387088405831*f=75.32347 Mt/yr
(published 75.3235). Hybrid V4 0.43194 for contrast: 11.8f=5.096892, 35.4f=15.290676, 1/f=2.315136.
span ln(0.43194/0.25146) = 0.5410027585 = the L-form lever. NO product-of-levers quoted anywhere.

### 05 - THE FIDELITY ANALYSIS: does any admissible §4.2 item 2 justification exist for OURS?
Walked docs/47 §4.1's six CITED/DERIVED rows one at a time. Item 2 demands *a citable reason why
the SOURCE'S choice is wrong FOR THIS BASIN*.

1. "a cap is REQUIRED" (AH-703 p.104, CITED) - AGAINST ours (59.5% of cells > 400 ft; A_unit 35.6x
   AH-703's outer bound). Cannot justify ours.
2. "our 1 km2 cap is a citation defect" - **CITED, CONTRADICTED**: M&D source areas 2,700-12,000
   m2 vs our 1e6; 150x at Andean slopes, 24x at basin median; wetter => smaller, and we are wetter
   than their wettest site. docs/47 §4.2 item 2: **"x1.000 is not defensible."** AGAINST ours.
3. "W&S-78 was withdrawn by its own authors for steep slopes" (Renard 1991 p.32; 2011 p.142) -
   **THE ONLY ITEM-2-SHAPED CANDIDATE ON THE RECORD**, and it has exactly the form item 2's worked
   example demands. But (a) it argues against the SOURCE's S, not for ours; (b) ours (Moore&Burch
   n=1.3) is equally unvalidated above tan0.50 where 35.5% of the S signal lives (Schmidt 2019;
   docs/47 §4.2 item 1); (c) its direction is DOWN (V3 is the x1.694 amplifier), so it would put
   f_LS BELOW 0.25146 - it cannot license RETAIN-OURS; (d) the resulting variant is NOT in §3.1 and
   has NO measured f_ero. Not available today, and not available for us in any case.
4. "our m is McCool-89/AH-703 exactly, m up to 0.71" (CITED) - the strongest-looking pro-ours row
   and it FAILS item 2: it cites OUR formula; it does not say the SOURCE's eq.14 is wrong for this
   basin. Undercut twice: AH-703 p.105-106 makes m a LAND-CONDITION parameter and its rangeland/low
   rill:interrill column gives **x0.5082** on this basin (~= the source's x0.5051) - the same
   citation read for THIS basin returns the SOURCE's level; and the "moderate" column is our own
   unstated user choice (docs/47 §4.2 item 3, O4). A symmetric citation, not a refutation => item 1
   decides, and item 4 reinforces (the source's m is the lower).
5. "our L is a point rate, not a cell average" (DERIVED) - AGAINST ours; the D&G/eq.13 cell average
   is "the coherent one and our point form over-states"; predicted head-cell ratio 0.58, measured
   0.5807.
6. the convergence result (DERIVED+CITED) - AGAINST ours, decisively: the Buarque path x0.245 and
   the INDEPENDENT RUSLE-handbook path (D&G L + McCool m + McCool S + AH-703's own 400 ft) x0.206
   land within 19% of each other sharing no formulation choice but the L form, both ~4-5x below
   production.

**VERDICT: NO admissible §4.2 item 2 justification exists on the record for retaining ours. Five of
six rows point against ours; the sixth is a symmetric citation that item 2 does not admit and whose
own land-condition reading returns the source's level.**

Fidelity nuance worth recording, and it FAVOURS item 1: transposing the METHOD ("L <= one DEM
pixel") at 90 m gives a 90 m cap = 302 ft, INSIDE AH-703's tabulated range (its tables stop at
1,000 ft), whereas the source's literal 500 m = 1,640 ft would be OUTSIDE it. Item 1's object is
the transposed *method*, and the transposition lands the cap inside the defensible span
(docs/47 §4.2 item 2: x0.351 / x0.379 / x0.401 / x0.585 / x0.672). And item 4 is NOT a licence to
hunt the lowest published LS (x0.206 is a *different method*, not a reading of the source, and is
published area-weighted only) - it breaks ties among admissible READINGS OF THE SOURCE.

### 06 - OUTCOME ELIMINATION
- **ADOPT-BAND**: trigger = "two admissible readings survive **on the source text**", whatever the
  gap. I verified the S attribution on THREE sentences and the limiter on TWO; eq.13 and eq.14 are
  single-reading. docs/46 §4.2's own note: "ADOPT-BAND is not currently triggered on any lever."
  NOT TRIGGERED. Also: [0.25146, 0.43194] "is NOT an ADOPT-BAND band and may not be presented as
  one" - it is a POINT beside a documented hybrid.
- **NEGATIVE - UNRESOLVED**: condition = ">=1 lever with no citable ground either way, or (R6)
  fires, or the source text cannot be obtained/verified". All four levers CITED; (R6) closed
  (percent); the PDF is obtained, on disk, hash re-verified BY ME today. §7.1's four triggers all
  fail. NOT LICENSED.
- **RETAIN-OURS-WITH-DISCREPANCY-DECLARED**: no §4.2 row licenses it. The licence it wants ("keep
  V0 as the default because it is incumbent, not because it won" + carry the bracket) is
  **NEGATIVE's licence**, and NEGATIVE's condition is unmet. The only other route is an item-2
  deviation, and §05 shows none exists. => INADMISSIBLE. (docs/46 §7.3 also forbids "treating the
  incumbent V0 as *validated* because it survived by default".)
- **ADOPT-SOURCE**: conditions - (i) all four levers CITED **MET** (verified first-hand today);
  (ii) (R6) not triggered **MET**; (iii) §3.3 exact re-run completed AND reported **INCLUDING THE
  STRATIFIED REPORT** -> the re-run is DONE and now twice-reproduced erosion-weighted (docs/46 §10
  amd 1 item 2), but the **stratified report is NOT discharged** (slope terciles absent;
  per-station ero-wtd LSbar exists only as ratios) - docs/46 §4.2 note 3, §10 closing note,
  docs/51 §7 item 9; (iv) §4.3 forbidden evidence untouched - I used NO basin total, NO anchor, NO
  alpha band, NO fit as evidence; my §05 walk is source readings only.
  => **ADOPT-SOURCE is the outcome the rule returns, and it is NOT YET EXERCISABLE.** Three named
  deliverables stand between the decision and the enactment: the §3.3 stratified report (slope
  terciles + per-station ero-wtd LSbar over the 18); H-S (R7)/(R8) items 2-3 on OUR slope field;
  and the **V4_dg column does not exist on disk** (verified §02), so the adopted formulation is not
  engine-readable and the re-run is not reportable in the registered form.

### 07 - C4.3
`grep -n 'A3|## A' docs/37` returns A1.* and A2.* sections only - **NO §A3**. So B1's unblocking
event (the dated enactment amendment: docs/46 §9 card / §7.3 item 5 / docs/51 §5.3 + §7 item 4) HAS
NOT LANDED, and a panel verdict is not it. docs/47 §6.1 **B2** (re-express the gate in Pi or
re-register the alpha box against the adopted f_LS) is undischarged and is owed to the docs/35 §9 /
docs/45 §8 owners, not to C4.3. B5 + the §5.5 pre-fit-profile disclosure are owed before any number
is printed. Branch B is MANDATORY three times over: docs/46 §6.3 B1 (Delta_shape =
0.1299456916752905 > 0; null control 2.22e-16), §6.3 B2 (a final verdict is unreachable under A3),
§6.3 B5 (the enactment amendment is unwritten). NOTE: docs/46 §6.3 B2 and docs/47 §6.1 B2 are
DIFFERENT objects and I keep them apart.

Implication worked out: Branch A is permanently unavailable for this swap; there is no provisional
C4.3 at all; **A6 bites** - Delta_shape > 0 means the swap is a SHAPE change, so every existing
profile of the objective (docs/47 §5.2's rescaled optima, §5.5's whole-box profile) is a LEVEL-only
rescaling and is NOT the answer at the adopted LS. docs/47 O5 is therefore not merely open but known
to be non-trivially open: no CAL station is invariant and CAPITANEJO moves 0.1299 in ln erosion
weight. Every guard statistic must be re-derived on the new residuals with a NAMED noise-floor
construction (A5: a minimum detectable coefficient computed against 0.465 is VOID).
=> **c43_unblocked = NO.**

### 08 - engine default
docs/46 §4.2 ADOPT-SOURCE licenses only *PROPOSING* the default; §5's "committed LS products" row:
"the default switches only through §4.2's separate dated amendment"; §9 card names **docs/37 §A3,
dated, written by the C3.1 owner** (owner of `scripts/c3/ls2d.py` + `docs/37`; C3.1 delivered both
by commit 5eaabf5). Two-act structure and the code act is act 2. Verified preconditions:
`ls2d_column="ls2d_hs"` and `urh_ls2d="urh_ls2d.csv"` are BOTH `load_geometry` defaults, V4_dg is in
NEITHER file, and `urh_ls2d.csv` may not be overwritten (§3.1) - so the switch is a two-parameter
act that cannot even be written until the column is materialised in a new file. G4.2 keeps
`ls2d_aggregation` / `ls2d_resolution` at 1.000: a column swap only, never an aggregation or
resolution change.

### 09 - the objection I could not dismiss
docs/47 §4.2 item 5 (first-party, the shipping MGB-SED plugin `bin/formPRESED.exe`, 2025-09-10)
found a **run-time user choice of S factor** - "(0) standard method / (1) slope scaling method" -
and concludes *"in the tool this project transposes, S is a user choice, not a fixed part of the
method."* If that is admitted as a second reading of the transposed METHOD (and docs/46 (R1)
explicitly admits "the MGB-SED code, if obtained" as a source of a second reading for the limiter
lever), then the S lever is ambiguous and the honest outcome is **ADOPT-BAND**, whose item-4
tie-break lands on an UNMEASURED variant BELOW 0.25146 - i.e. my adopted point would be the wrong
end of a band I declared not to exist. What blunts it: Buarque's own text is unambiguous three times
over (p.47 sentence, p.47 introduction of eq.13's context, p.48 eq.18 + attribution), all verified
by me today; docs/46 §4.2's note says ADOPT-BAND is not triggered on any lever; H-S has no clause
admitting the code as a second reading (only H-LIM's (R1) does); and the plugin is a 2025 artifact
of a successor tool, not the transposed source of record. **Decisive for the outcome field: it
points DOWN, not at ours, so it cannot rescue RETAIN-OURS either way.** Recorded as the objection,
and as a named risk to the VALUE (not to the outcome).

Secondary objection: strictly, no §4.2 row's condition is fully satisfied today (ADOPT-SOURCE fails
its stratified-report conjunct), so a purist reading says the rule returns nothing and my
"ADOPT-SOURCE, not yet exercisable" is a fifth outcome. Answer: §4.2 note 3 itself separates
"reachable" from "exercised" and puts the stratified report on the *exercise* step; and the only
alternative (NEGATIVE) is affirmatively unlicensed and would license keeping V0, which no evidence
on the record supports. ADOPT-SOURCE-conditional is the least-wrong of the four.

### 10 - defects found in files I do NOT own (REPORTED, NOT FIXED)
1. `data/processed/urh_ls2d_variants.csv` has **no V4_dg column** - the adopted formulation is not
   materialised anywhere on disk. docs/51 §7 item 7 calls this a verification; it is in fact a
   **precondition of the default switch** and of "the §3.3 re-run reported".
2. docs/46 §3.1's V5 row and docs/51 §2.4 residue 1 do not name the **slope-operator lever**:
   the source specifies eqs. 15-17, centred differences over the FOUR ORTHOGONAL neighbours
   (Wilson & Gallant 2000); we use Horn 3x3, which feeds both `m` (via Sf) and `S` (via theta).
   Unmeasured, un-named, and it is a lever, not a residue.
3. docs/47 §4.1 row 4's parenthetical code defect stands: `scripts/c3/ls2d.py`'s docstring claims
   `m` runs "to ~0.5 on steep Andean slopes"; measured median 0.5844, p90 0.7028, max 0.7501.

**Files written by me: `docs/agents/journal_panel-fidelity.md` only. No default moved, no fit, no
alpha-hat, no git command, no edit to any doc/script/notebook.**
