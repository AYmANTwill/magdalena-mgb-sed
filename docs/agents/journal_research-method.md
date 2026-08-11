# Journal — research-method

GOAL: parallel research track. Establish how daily distributed models (MGB especially) and the
MUSLE literature handle the peak problem, so C3.3's options are grounded in published practice
rather than invented. Write ONLY this journal + a findings file in data/processed/peakgap/.

Constraints honoured: no git, no calibration launch, no other file edits, no yields in t/km2/yr.

## Checklist

- [ ] S1. Fagundes et al. (2026) ISWCR 14, 100599, doi 10.1016/j.iswcr.2025.11.007 — how is
      q_peak obtained for MUSLE from a daily MGB run? Quote or precise paraphrase; if
      inaccessible, say so plainly.
- [ ] S2. MGB-IPH practice on sub-daily peaks and MUSLE q_peak (Collischonn / Paiva / Fan /
      Pontes line; MGB-SED notes).
- [ ] S3. Rainfall disaggregation methods (method-of-fragments, Bartlett-Lewis, Neyman-Scott,
      reanalysis-shape hybrids); realism at 257,000 km2 / ~30 km gauge spacing / daily r 0.57.
- [ ] S4. Hortonian question: adding infiltration-excess to a saturation-excess daily engine —
      established? cost?
- [ ] S5. Per-avenue synthesis: what it is / needs / buys / compatible with frozen daily H2E or
      requires re-opening Phase B a third time.
- [ ] S6. Write data/processed/peakgap/method_research.md; StructuredOutput.

## Log

(appended below, with numbers, after every step)

### S0 — setup (start)
Created docs/agents/ journal and data/processed/peakgap/ (was absent). WebSearch/WebFetch loaded.

### S1a — Fagundes 2026 identified, ScienceDirect blocked, primary formulation found upstream
- CrossRef 10.1016/j.iswcr.2025.11.007 = Fagundes, Maciel, Fassoni-Andrade, Silva, Rossoni,
  Cavalcanti, Buarque, Fan, ISWCR 14, 100599: "Simulating suspended sediment transport during the
  2023-2024 floods in southern Brazil". 50 refs.
- Full text: ScienceDirect returns HTTP 403 to every route tried (article page, /pdfft, jina proxy,
  curl with browser UA -> 403, 1,207,912 bytes of CAPTCHA HTML). OpenAlex says oa_status=diamond,
  any_repository_has_fulltext=False. INPE mirror urlib.net: connection REFUSED (200.160.7.168:443).
  => full text NOT accessible from this box.
- OpenAlex abstract retrieved verbatim: "We used the hydrological model MGB-SED and DAILY
  precipitation to compute sediment erosion, transport and deposition, with calibration focused on
  representing extreme events." (emphasis mine) -> daily forcing, no sub-daily run.
- Got the UPSTREAM primary source instead: Buarque (2015) PhD thesis, UFRGS/IPH, "Simulacao da
  geracao e do transporte de sedimentos em grandes bacias: estudo de caso do rio Madeira" (advisor
  Collischonn) = the MGB-SED formulation paper that Fagundes' MGB-SED inherits. Downloaded
  lume.ufrgs.br/bitstream/handle/10183/129875/000977197.pdf (9,646,521 bytes, 182 pp, 424,028 chars
  of text, 42 'MUSLE' hits) to scratchpad.
- **THE ANSWER (Buarque 2015 eq. 7, p.59):** qpico_{i,j}^k = Dsup_{i,j}^k * A_{i,j}^k / 86.4,
  preceded by: "A taxa de pico do escoamento superficial em cada pixel k e obtida considerando um
  volume de escoamento uniforme ao longo do dia." = peak rate assumed as the DAILY-MEAN surface
  runoff rate. No unit hydrograph, no disaggregation, no regionalised peak relation.
  Unit check: 1 mm/d over 1 km2 = 1000 m3/d = 0.011574 m3/s = 1/86.4 -> A in km2, Dsup in mm/d.
- Eq. 5: SED = 11.8 (Qsup*qpico*A)^0.56 * K*C*P*LS*FG, with FG a coarse-fragment factor.
  MUSLE applied PER PIXEL inside each URH of each minibacia (eq. 6), then a simple linear reservoir
  delays delivery of minibacia sediment to the channel.

### S1b — Fagundes' OWN thesis confirms the same qpeak, and names the calibration lever
Downloaded Fagundes (2018) MSc dissertation, UFRGS/IPH, "Modelagem hidrossedimentologica de
grandes bacias com o apoio de dados in situ e sensoriamento remoto" (rio Doce, 86,715 km2),
lume.ufrgs.br/bitstream/handle/10183/175012/001065326.pdf, 9,292,830 bytes, 201 pp.
- s5.3.1 "Taxa de pico do escoamento superficial": "A taxa de pico do escoamento superficial
  (qpico) foi calculada a partir do volume de escoamento superficial (Dsup [mm]) UNIFORME AO LONGO
  DO DIA, fornecido pelo MGB-IPH" -> eq.12 qpico = Dsup*A/86.4. IDENTICAL to Buarque 2015 eq.7.
- eq.11 text: "alpha e beta sao coeficientes de ajuste, ora adotados como 11,8 e 0,56 ... ora
  CALIBRADOS AUTOMATICAMENTE" -> alpha/beta are calibration parameters in MGB-SED practice.
- s5.5: the calibrated sediment parameters are exactly {alpha, beta, TKS} (TKS = surface/sediment
  linear-reservoir delay), optimised with MOCOM-UA multi-objective.
- Appendix IV calibrated values read directly off the tables (experiments A1-B4, 4 data types):
  alpha 6.93-18.86 (Williams default 11.8), beta 0.44-0.93 (default 0.56), TKS multiplier
  0.46-2.05. (An automated parse of the whole appendix gave alpha median 11.66, beta median 0.613,
  TKS median 1.110 over 404/376/469 parsed cells, but column collapse in the PDF text makes the
  extremes unreliable - hence quoting the hand-read ranges.)
- s6.3.1 sensitivity: alpha scales the sedimentogram proportionally; beta amplifies peaks/valleys
  as it DECREASES (exponent on a quantity <1); TKS -50% sharpens peaks and shifts CSS peak timing
  by ~2 days.
- s6.4.1, verbatim: "Na equacao MUSLE, os fatores de intensidade de chuva sao substituidos pelo
  escoamento superficial e uma vazao de pico, que estaria relacionada com a energia maxima do
  escoamento sobre o solo, E QUE NO MGB-SED E DESCONSIDERADA PELA DIFICULDADE DE SE OBTER TAL
  INFORMACAO (Kinnell e Risse, 1998)."
- s6.4.2, verbatim: "o modelo tambem nao representou de forma adequada grandes picos de
  concentracao." => the peak deficit is a NAMED, PUBLISHED limitation of MGB-SED itself.
No occurrence of 'sub-diario', 'subdiario' or 'horaria' anywhere in either document (0 hits).

### S2 — MGB practice + the SWAT contrast (quantified)
- Official MGB-IPH application manual (ufrgs.br/hge, 6,468,314 bytes, 90 pp): 0 hits for
  'passo de tempo', 0 for 'horario', 0 for 'sub-diario', 0 for 'sedimento'. MGB is a daily model and
  the sediment module is a separate add-on.
- MGB-SED computes minibacia time of concentration but spends it on the DELAY (TKS linear
  reservoir), never on the peak - the exact opposite of SWAT's choice.
- SWAT Theoretical Doc v2009 (swat.tamu.edu/media/99192/swat2009-theory.pdf, 7,690,470 bytes,
  647 pp), s2:1.3.3-2:1.3.4 verbatim: alpha_tc = 1 - exp[2*t_conc*ln(1-alpha_0.5)] (2:1.3.19);
  q_peak = alpha_tc*Q_surf*Area/(3.6*t_conc) (2:1.3.20); "alpha_tc falls in the range
  t_conc/24 <= alpha_tc <= 1.0" (2:1.3.18), the lower bound being storms "of uniform intensity".
  => MGB-SED's q_peak IS SWAT's lower bound with t_conc = 24 h: the minimum admissible peak.
- My arithmetic from those two equations, ratio vs 1/86.4, sediment ratio = q ratio^0.56:
  t_conc 2 h: q x2.23-9.12, sed x1.57-3.45 for alpha_0.5 0.05-0.30
  t_conc 4 h: q x2.02-5.65, sed x1.48-2.64
  t_conc 6 h: q x1.84-3.94, sed x1.41-2.16
  t_conc 12 h: q x1.42-2.00, sed x1.22-1.47 ; t_conc 24 h: x1.00 (identity, as expected).
  Our minibacias: 257,000/8,672 = 29.6 km2 mean; Kirpich gives t_conc 0.73 h (L 5 km, S 0.05) to
  6.42 h (L 12 km, S 0.001) -> we sit in the top three rows.
- KEY LIMIT: q_peak stays a monotone function of daily Q_surf under ANY of these formulas, so it
  cannot manufacture events. R_POT 0.567 (1,285 sim vs 2,236 obs POT) is untouched by q_peak choice.
  The gain is (a) a scale factor alpha already absorbs and (b) spatial re-weighting t_conc^-0.56.

### S3 — the erosion-equation alternative, found in the 2026 paper's own reference #1
Almeida et al. (2025), ISWCR, doi 10.1016/j.iswcr.2025.10.004, "Comparison of approaches using
MUSLE, USLE-M and RUSLE2 for large-scale hydrosedimentological modelling" - USLE-M and RUSLE2
implemented IN THE MGB-SED SOURCE CODE, Doce basin. Abstract verbatim (OpenAlex): "MUSLE achieved
KGE > 0.5 at most stations. USLE-M best represented the SOLID DISCHARGE PEAKS, while MUSLE best
represented the minimum suspended sediment concentrations (SSC) ... The greater applicability of
MUSLE is especially in conditions of unavailability or scarcity of data for an estimate of daily
rainfall erosivity, which is necessary for the use of USLE-M and RUSLE2."
=> a published, in-model route to better peaks, priced in daily EI30 which our r=0.57 field cannot
supply credibly.

### S4 — disaggregation and Hortonian
- Families + citations recorded in the findings file (method of fragments / Bartlett-Lewis /
  Neyman-Scott / multiplicative cascades / reanalysis-shape hybrids / LSTM). Pui et al. 2012
  (doi 10.1016/j.jhydrol.2012.08.041) compared three families: method of fragments generally best,
  i.e. the winner is the one that copies a REAL observed profile.
- Blunt verdict recorded: stochastic disaggregation reproduces STATISTICS, not sequences; for a
  day-matched ENSO contrast it adds structure without information; and in our daily architecture it
  can only reach sediment through q_peak, where the SWAT formula gets the same effect
  deterministically. It earns its keep only with a sub-daily engine = Phase B reopened.
- Hortonian: established (Liang & Xie 2001, doi 10.1016/S0309-1708(01)00032-X, 246 cites, adds
  infiltration-excess to VIC's saturation-excess). But at daily step 50 mm/day = 2.1 mm/h mean
  intensity < Ks for most soils -> inert unless a within-day intensity distribution is assumed,
  i.e. disaggregation smuggled into runoff generation. SWAT's Green-Ampt option requires sub-daily
  rain for the same reason. Cost: changes Q_sur -> voids H2E / F 0.25931 -> Phase B a third time.

### S5/S6 — findings file written
data/processed/peakgap/method_research.md (single file; nothing else in the repo touched besides
this journal). Contains: the two verbatim q_peak quotes, the alpha/beta/TKS calibration ranges, the
SWAT ratio table, the six-avenue comparison, the source list, and an explicit "not done / blocked"
section (Fagundes 2026 full text; C3.5 still blocked - musle.py absent from this repo).
DONE.
