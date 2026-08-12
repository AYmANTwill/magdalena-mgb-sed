# journal — `adj-alpha-role`

**Opened** 2026-08-11. Agent slug `adj-alpha-role`.

## GOAL

Settle what MUSLE's `alpha` and `beta` are actually FOR in the method this project
transposes (MGB-SED, Buarque 2015 / Fagundes 2018), because that determines whether
C3's measured under-erosion (1.03–2.27× at the adopted default, docs/40 §8.2 + docs/37 A1.4)
is a **defect** or the **expected input to a calibrated model**.

Two live readings:
- **READING 1 (physical):** α = 11.8 is Williams' fitted coefficient; a calibrated α should
  stay near it; a large departure signals a compensating error. This is what `docs/35` §6.1's
  guard assumed.
- **READING 2 (calibration lever):** in MGB-SED α, β are free coefficients of adjustment
  fitted per application against observed sediment; they legitimately absorb delivery and
  the missing non-hillslope sources; comparability with 11.8 is not expected.

## CHECKLIST

- [x] 1. Read `docs/40`, `docs/agents/journal_research-method.md`, `docs/35`, `docs/42` (repo's
      own prior review of Buarque 2015 / Fagundes 2018) — FIRST, before any web search.
- [x] 2. Read `docs/37` (+ A1) and `docs/agents/journal_alpha-guard.md`, `journal_critic.md`,
      `journal_reverdict.md` for how the α guard came to be and how it went blind.
- [x] 3. Read `src/mgb_sediment.py` for what α/β actually do in OUR implementation and what
      `check_musle_parameters` asserts.
- [x] 4. External evidence: what RANGE of fitted α do Buarque (2015) / Fagundes (2018) (and
      any other MGB-SED application) actually report, and against WHAT were they fitted
      (outlet load? tributary stations? concentration?).
- [x] 5. Decide READING 1 vs READING 2 from source evidence. Enumerate what is physically
      inside a fitted α.
- [x] 6. State the consequence for `docs/35` §6.1 (mis-specified vs merely blind) and the
      correct guard. Verify `docs/42`'s guards sufficient under the winning reading; name gaps.
- [x] 7. `blocks_c4` with reason. Structured output only. No file writes outside this journal.

## PRE-COMMITMENTS (recorded BEFORE computing/reading anything that bears on them)

- P1. I will decide the reading on **what the sources say α/β ARE**, not on which reading is
  more convenient for C3. If the evidence is mixed I will say MIXED, not pick.
- P2. If I cannot find a **reported fitted α value** in the MGB-SED literature I will say
  UNCITED rather than infer a range from our own model. An uncited band may neither pass nor
  fail a gate (task hard rule).
- P3. I will NOT compute any new headline number (no runs, no re-fits). This is an
  adjudication task. If I compute anything at all it will be a re-read of an existing
  artifact, and I will record the intent here first.
- P4. Distinguishing test I commit to in advance: READING 2 is established **iff** the source
  method (a) lists α (and β) among the parameters handed to the automatic optimiser, and
  (b) fits them against **observed sediment at gauges**. If both hold, then a fitted α
  necessarily contains everything that lies between hillslope gross erosion and the gauge —
  and "α near 11.8" cannot be a validity criterion. Failure of (a) or (b) → READING 1 lives.

---

## LOG

### Step 0 — journal opened

Wrote this file before reading any source. Checklist and pre-commitments above are the
registered version.

### Step 1 — repo-internal evidence read (checklist 1–3 partially)

Read `docs/00_INDEX.md`, `docs/40` (§0–§9, 615 of 728 lines), `docs/35` (all, incl. §6.1, §9.1–§9.3),
`docs/42` (all 613 lines), `docs/agents/journal_research-method.md`, `docs/agents/journal_alpha-guard.md`.

What the repo already establishes, with locations:

1. `journal_research-method.md` S1b — **Fagundes (2018) §5.3.1/eq.11 text**: "alpha e beta sao
   coeficientes de ajuste, ora adotados como 11,8 e 0,56 ... ora CALIBRADOS AUTOMATICAMENTE";
   §5.5: the calibrated sediment parameters are **exactly {alpha, beta, TKS}**, optimised with
   **MOCOM-UA multi-objective**; Appendix IV hand-read fitted ranges **alpha 6.93–18.86**,
   **beta 0.44–0.93**, TKS multiplier 0.46–2.05, across "experiments A1–B4, 4 data types".
2. `docs/35` §6.1 states its own premise verbatim: "Reference: **alpha = 11.8** (Williams 1975;
   **adopted unchanged by Buarque 2015** eq. 5 *with the same daily-mean q_peak*, so it is the
   like-for-like reference under §4)". That is READING 1's premise, and it cites **Buarque**, not
   Fagundes — i.e. the guard was built on the branch of the lineage that ADOPTS alpha, while the
   branch this project transposes (Fagundes) **FITS** it.
3. `docs/42` §3.1 already proves the confounding algebraically: seven uniform scalars
   (alpha, f_vol 47.8630, f_K 7.593014, f_LS, C_mult, P, FG) are one identifiable product
   Pi = 4288.4; design matrix cond = inf.
4. `docs/35` §9.2 point 2 is the blindness: a deposition-free fit lands alpha at **6.83–8.73**,
   inside the expected band 5.9–23.6.
5. `docs/40` §0.3: under the yield reading the alpha reproducing Tan's converted level is
   **7.92–8.86**, which **overlaps** the deposition-free band 6.83–8.73.

Decision recorded BEFORE computing/looking up anything further (per the hard rule): I will treat
pre-commitment P4 as the deciding test, and I will look for (a) whether alpha is in the optimiser's
parameter vector and (b) what observed quantity the objective is computed on. Both PDFs are still
in this session's scratchpad (`buarque2015.pdf` 9.6 MB, `fagundes2018.pdf` 9.3 MB) so this is a
primary-source read, not a secondary one.

### Step 2 — PRIMARY SOURCES READ (checklist 4). Both PDFs re-extracted in this session.

`buarque2015.pdf` 182 pp / 424,028 chars; `fagundes2018.pdf` 201 pp / 343,216 chars
(PyMuPDF text extraction, scratchpad only, nothing written to the repo).

**B — Buarque (2015), the FORMULATION source.** Verbatim eq. 5, p. 43:
`SED = 11,8 . (Qsup . qpico . A)^0,56 . K . C . P . LS . FG` — **alpha and beta do not exist as
symbols**; 11.8 and 0.56 are literals. Eq. 6 applies it per DEM pixel. His MOCOM-UA calibration
is of the **hydrological** model only — verbatim, the calibrated set is "Wm; ... Kint, e
subterraneo, Kbas; ... CS, ... CI, ... CB", fitted to **discharge** at 25 fluviometric stations.
For the sediment module, verbatim: "Os parametros do modelo de sedimentos **relacionados a MUSLE
foram ajustados de acordo com faixas de valores obtidas da literatura** para os usos e tipos de
solo simplificados conforme as URHs" — i.e. K/C/P/LS/FG set from literature ranges, **alpha
never fitted**. He then RECOMMENDS what Fagundes did next, verbatim: "Uma **espacializacao dos
parametros da MUSLE por sub-bacia**, assim como realizado para a calibracao do modelo
hidrologico, ... pode melhorar as estimativas da geracao de sedimentos nesses locais."
=> **READING 1 is a true description of Buarque.**

**F — Fagundes (2018), the APPLICATION source (the one docs/00 H3 names as the transposed
method).** eq. 11 with **alpha and beta as symbols**, text verbatim: "alpha e beta sao
**coeficientes de ajuste**, ora adotados como 11,8 e 0,56 ... ora **calibrados automaticamente**".
s6.3.1 verbatim: "Os parametros que foram adotados como calibraveis foram os parametros **de
ajuste** da equacao da MUSLE, alpha e beta e o parametro de retardo ... TKS."
s5.5.1: MOCOM-UA multi-objective, Pareto region, "adotou-se sempre o valor que apresentou a melhor
media das funcoes objetivos para o conjunto de dados que estava sendo calibrado".
**Against WHAT:** Quadro 5-2, 14 experiments, 1997-2010, four observed data types —
**in-situ CSS (21-26 stations), red-band surface reflectance RefVer (21), turbidity (61-63),
SST (61-63)**; objectives Rtemp/Resp/Rtudo (correlations) in 11 of 14 experiments,
**BIAS/RMSE/KGE in B2**, **Nash/KGE/Rtemp in D1**. alpha is fitted **PER SUB-BASIN**
(1, 5 or 17 sub-basins) and **separately per data type**.
**Search intervals, verbatim:** "para a maioria dos experimentos, utilizou-se um intervalo de
busca para alpha entre **2,0 e 25,0**, para beta entre **0,2 e 1,7** e TKS entre 0,1 e 3,0";
C2 narrowed alpha to **10,0-13,0**; C3 to **0,00001-3,0**; **C4 widened alpha to 0,0001-500,0**
and beta to 0,01-5,0.
=> **READING 2 is a true description of Fagundes.**

Two further primary quotes that bear on C3's under-erosion verdict (docs/40):
- F, s3 on MUSLE: "a MUSLE se constitui de uma equacao de base empirica, **ajustada a partir de
  experimentos de campo com medicoes de descargas solidas, que leva em conta, portanto, os
  sedimentos NO CANAL e nao apenas nas encostas**."
- F, same section: "a inclusao de um fator que considera o escoamento superficial ... **elimina a
  necessidade de inclusao de uma taxa de transferencia de sedimentos (Sediment Delivery Rate -
  SDR)**" (attributed to Williams 1975 and Neitsch et al. 2005).
- F, B8 rationale: bank erosion is named as a process the model does NOT represent, and it was
  handled by an **additive** base concentration `CSSbase`, NOT by inflating alpha.

**DECISION RECORDED BEFORE THE NEXT COMPUTATION** (per the hard rule). I am about to parse
Fagundes Appendix IV in full and compute (i) the distribution of fitted alpha/beta, (ii) the
spread of fitted alpha ACROSS DATA TYPES for the SAME sub-basin, and (iii) the fraction of
fitted beta outside docs/35 s6.3's hard stop. I am recording in advance what I will conclude
from each outcome so the conclusion cannot be selected:
- If the same sub-basin's fitted alpha changes materially depending on whether CSS, reflectance,
  turbidity or SST was the calibration target, then alpha cannot be a physical constant in this
  method, and READING 2 is established regardless of where the values happen to sit.
- If fitted alpha nevertheless clusters near 11.8, I will NOT read that as support for READING 1,
  because the search interval [2,0 - 25,0] is itself centred near 11.8 (mid-point 13.5) and caps
  the range; a clustered posterior inside a narrow prior is not evidence about physics. I will
  say that explicitly.
- beta outside 0.45-0.65 in the SOURCE's own fits would mean docs/35 s6.3's beta hard stop is
  also tighter than the transposed method's own practice. I will report it either way.

### Step 3 — Appendix IV parsed in full, and the guard turned on its own source (checklist 4–6)

Scripts: `scratchpad/parse_appIV.py`, `scratchpad/guard_vs_source.py` (scratchpad only; the second
imports the repo's own `scripts/c3/qpeak.py` read-only and calls `check_musle_parameters`).
Parse validated by design: recovered sub-basin row counts per experiment are
A1 5, B1 1, B2 5, B3 5, B4 17, B5 17, B8 17, C1 5, C2 17, C3 17, D1 17 — exactly the sub-basin
counts Quadro 5-2 declares. **123 sub-basin rows x 4 calibration data types = 426 fitted
(alpha, beta) pairs.** Tables for B6, B7 and **C4** are ABSENT from Appendix IV, so the fit made
under the widest prior (alpha 0.0001–500.0) is **not recoverable** — recorded as a gap, not
guessed at. Also recorded as a **source inconsistency**: Quadro 5-2 gives C3's alpha prior as
0,00001–3,0 while Tabela IV-9 (labelled C3) reports alpha 10.011–12.805; and C2's beta prior is
printed "entre 4,0 e 7,0" against fitted beta 0.460–0.693. Neither affects anything below.

**Fitted values, 426 pairs:**
- alpha: min 2.221, p05 8.520, **median 11.765**, mean 12.202, p95 16.738, max 23.179 (10.4x span)
- beta: min 0.207, p05 0.487, **median 0.618**, mean 0.656, p95 0.939, max 1.659

**The decisive measurement (P4's distinguishing test, and it is unambiguous).** For the SAME
sub-basin in the SAME experiment, the only thing that changes between the four columns is
*which observed dataset was the calibration target*. Fitted alpha changes with it:
**median 1.28x, p95 3.99x, max 7.78x** (101 complete rows); 30.7 % of rows spread > 1.5x,
13.9 % > 2x. Fitted beta likewise, median 1.33x, max 3.25x. A physical coefficient cannot
change by 7.78x according to whether you calibrated against in-situ CSS or Landsat red-band
reflectance in the same sub-basin over the same 1997–2010 period. **alpha in MGB-SED is a
fitted coefficient of adjustment. READING 2 is established.**

Across sub-basins within one experiment and one data type, alpha spans 1.11x (C2, prior narrowed
to 10–13) to 4.94x (B5); i.e. alpha is also **spatially distributed** — Buarque's own written
recommendation ("uma espacializacao dos parametros da MUSLE por sub-bacia ... pode melhorar as
estimativas") carried out.

**Why "alpha near 11.8" in that table is not evidence of anything.** (i) 97.7 % of the 426 fits
land inside docs/35 s6.1's "expected" 5.9–23.6 — but the source's search prior is [2.0, 25.0],
which *contains* that band, so the statistic measures the prior, not the physics. (ii) 11 of the
14 experiments optimise **correlation only** (Rtemp/Resp/Rtudo). A Pearson correlation is
invariant to any exact positive rescaling of the simulated series, and MGB-SED's fine-sediment
routing (Fagundes eq. 15) is **linear in concentration**, so in those 11 experiments alpha is
identified only through the nonlinear sand/transport-capacity path — it is close to unconstrained.
*(This inference is mine, labelled as such; the linearity of eq. 15 is the source's.)*
Split measured: correlation-only experiments n=336, alpha 2.221–23.179, median 11.909;
level-constrained experiments (B2 BIAS/RMSE/KGE, C2 …/ENS, D1 Nash/KGE/Rtemp) n=90,
alpha 8.556–14.850, median 11.617.

**The guard turned on its own source — this is the falsification.** Running the repo's OWN
`check_musle_parameters` (docs/35 s6.1 + s6.3 thresholds, unmodified) over all 426 published,
*adopted* fits of the method this project transposes:

| verdict | count | share |
|---|---:|---:|
| `STOP` | 185 | 43.4 % |
| `watch` | 59 | 13.8 % |
| `ok` | 182 | 42.7 % |

- **beta hard-stop (0.45–0.65) trips on 182/426 = 42.7 %.** Per experiment: D1 94.1 %,
  B8 80.9 %, B2 80.0 %, B3 70.0 %, B4 55.9 %, A1 55.0 %, C1 45.0 %, B5 32.4 %, B1 25.0 %,
  C2/C3 8.8 %. The source's own beta prior was **[0.2, 1.7]**, and [0.01, 5.0] in C4.
- alpha hard-stop (3.93 / 35.4) trips on only 5/426 = 1.2 % — because our stops are *wider* than
  the source's prior. That is the point: the alpha band is a prior-range check, not a physics test.

**beta is dimensionless, so this result is convention-proof.** docs/35 s9.2 and docs/42 s8.1 both
argue the beta band survives every unit/convention argument because no unit factor can move beta.
That is correct and it is exactly why the finding bites: no convention correction can rescue
docs/35 s6.3. **The guard hard-stops 43.4 % of the published fits of the method it guards.**

DECISION RECORDED BEFORE WRITING THE VERDICT: I will not soften this by noting that our basin
differs from the Doce. A threshold that rejects the source method's own accepted practice is
mis-specified *as a threshold*, whatever basin it is applied in; the correct response is to
re-derive or demote it, not to keep it and hope it does not fire.

### Step 4 — verdict, and what it does to docs/35 s6.1 (checklist 5–6)

READING 2 governs the transposed method. READING 1 is a true description of **Buarque (2015)**
only, and docs/35 s6.1 cites exactly that branch ("adopted unchanged by Buarque 2015 eq. 5").
The project's own H3 (docs/00) is method transfer from **Fagundes**, where alpha/beta are the
calibration levers. So docs/35 s6.1 imported its reference from the wrong branch of its own
lineage.

**docs/35 s6.1 was MIS-SPECIFIED from the start, not merely blinded by the s9.2 convention
change.** Three independent reasons, any one sufficient:
1. It bounds a quantity that the transposed method **defines as free** — "coeficientes de
   ajuste ... calibrados automaticamente", fitted per sub-basin AND per data type, moving up to
   7.78x with the choice of calibration target.
2. Even granting the reference, the comparison needs unit **and** level equivalence in all six
   other confounded scalars. docs/35 s9.2 conceded the unit half and s9.3 conceded the level half
   (LS 2.37–3.00x, UNRESOLVED), and docs/42 s3.1 then proved the seven scalars are one product
   Pi with condition number inf. **An alpha band is therefore a test on Pi with six factors
   assumed** — it could never have been a test on alpha.
3. Empirically, its companion beta clause rejects 42.7 % of the source method's own fits.

s9.2 point 2 (the 6.83–8.73 blindness) is a *symptom*, not the disease. The disease is that a
parameter value cannot be a validity criterion for a parameter the method fits.

**The correct guard** is what docs/42 already asserts in its s1: *a scalar can absorb a level, it
cannot absorb a structure*. If alpha legitimately absorbs a multiplicative constant, the only
thing that can betray a compensating error is STRUCTURE in the residuals — spatial (G1), flow
magnitude (G2.1), land-composition (G3.1), steepness (G4.1), seasonal (G8), cross-phase (G7) —
plus the reporting preconditions G5, G6, G9. docs/42 is the right instrument. Four gaps are named
in the structured output; the sharpest is that docs/42 G2.3 re-affirms the docs/35 beta hard stop
unchanged, and that band is the one clause of docs/35 s6 that this run has now falsified against
the source.

Files written by this run: `docs/agents/journal_adj-alpha-role.md` (this file) only. No frozen
artifact opened. No calibration launched. No git. No headline number recomputed.
