# Journal: cite-sdr

GOAL: Settle docs/37 residual 3 — cite or retire the sediment delivery ratio (SDR) band.
Our number: gross hillslope erosion 248.73 Mt/yr (MUSLE, hillslope only) vs outlet anchor
144-184 Mt/yr at Calamar => implied SDR 0.579-0.740. Asserted comparison band 0.05-0.30 has
NO citation. Decide: CITED-AND-CONSISTENT / CITED-AND-INCONSISTENT / UNCITABLE, and propose
replacement wording for docs/37's third closure clause.

Write only: docs/40_sdr_evidence.md + this journal.

## Checklist
- [x] 1. Read docs/00_INDEX.md, docs/37, and the parts of docs/34/35 the SDR clause depends on
- [x] 2. Pin definitions (SDR numerator/denominator; what our 248.73 and 144-184 actually are)
- [x] 3. Literature: generic SDR-area relations (Walling 1983, Vanoni/ASCE 1975, modern compilations)
- [x] 4. Literature: Magdalena-specific budget (Restrepo & Syvitski, Restrepo & Kjerfve, Restrepo et al.)
- [x] 5. Classify each citation: hillslope-to-OUTLET vs hillslope-to-CHANNEL (comparability)
- [x] 6. Non-MUSLE source fractions (gully, bank, landslide, mining) with citations
- [x] 7. VERDICT + exact replacement wording for docs/37 clause 3
- [x] 8. Write docs/40_sdr_evidence.md

## Log
- [step 0] Journal created. Starting doc reads.
- [step 1] docs/37 read. Clause 3 is lines 14, 59-80, 164-170. Anchors verified in docs/34 §5.1:
  Restrepo & Kjerfve 2000 = 144 Mt/yr (Calamar, 1975-1995); Restrepo & Escobar 2018 = 184 Mt/yr
  (1980-2010). Basin 257,438 km2 published / 257,097 km2 ours.
- [step 2] Generic relations located and evaluated at A = 257,097 km2 = 99,265 mi2:
  * Vanoni (1975) ASCE Manual 54: SDR = 0.42 A^-0.125 (A mi2, 300 watersheds) -> 0.0997
  * USDA-SCS (1979): SDR = 0.51 A^-0.11 (A mi2) -> 0.1438
  * Renfro (1975): log SDR% = 1.7935 - 0.14191 log A (A km2, 14 Texas Blackland Prairie) -> 10.61 % = 0.106
  * Walling (1983): area exponent range -0.01 to -0.25 (per secondary citation; primary PDF is a
    scan, 0 chars extractable, so quoted as secondary).
  All three land near 0.10-0.14, i.e. INSIDE the asserted 0.05-0.30 band. BUT:
- [step 3] **DEFINITIONAL BREAK FOUND — this is the finding.** USDA NEH Part 632 Ch 6, p.6-4:
  "Gross erosion is the sum of all the water erosion occurring in the drainage area. It includes
  sheet and rill erosion plus channel-type erosion (gullies, valley trenches, streambank erosion,
  etc.)." So published SDR has ALL sources in the denominator. Ours has hillslope only ->
  our ratio is NOT an SDR and is not comparable.
  NEH Table 6-2 (source-texture worked example) quantifies exactly this:
    sheet erosion 900,000 t/yr eroded -> 300,000 t/yr delivered, DR = **33 %**
    gullies 350,000 -> 280,000 (80 %); roadbanks 150,000 -> 120,000 (80 %);
    streambanks 900,000 -> 900,000 (100 %)
    TOTAL gross 2,300,000 -> yield 1,600,000, overall DR = **70 %**
    sheet erosion is only 900,000/2,300,000 = **39 %** of gross erosion
    the MIXED ratio (total outlet yield / sheet-erosion gross) = 1,600,000/900,000 = **1.78**
  Our 0.579-0.740 is the mixed ratio. In USDA's own reference example the same mixed ratio is
  1.78 — so ours is LOW, not high, against the like-for-like quantity. The mixed ratio has no
  upper bound of 1.
  NEH fig 6-2 x-axis spans **0.01 to 100 square miles** (0.026-259 km2) — our basin is ~1,000x
  the largest watershed in the curve. NEH p.6-11: "Using an equation to obtain sediment data
  outside the physiographic area for which the equation was developed is generally not
  recommended."
- [step 4] Magdalena-specific sweep. NO published study reports GROSS EROSION for this basin.
  Every "erosion rate" in the Magdalena literature is a specific sediment YIELD back-calculated
  from measured load or from BQART, i.e. the SDR NUMERATOR, never the denominator:
  * Restrepo (2015) RACCEFYN 39(151):250, doi 10.18257/raccefyn.141 — 550 -> 710 t/km2/yr
    (+34 %), 690 t/km2/yr at Calamar in 2000, +44 Mt/yr load, 78 % of catchment in critical
    erosion state, 9 % of load from deforestation, ~160 Mt 2000-2010. Verified verbatim from the
    article HTML (curl, latin-1). 710 x 257,097 km2 = 182.54 Mt/yr — independently corroborates
    the 184 Mt anchor.
  * Restrepo, Kettner & Syvitski (2015) Anthropocene 10:13-28 — +33 % erosion 1972-2010,
    +44 Mt/yr, 482 Mt from forest clearance over three decades, 79 % under severe erosion.
  * Restrepo et al. (2006) J. Hydrol. 316:213-232 — yields 128-2,200 t/km2/yr for catchments
    320-59,600 km2; mean 690 t/km2/yr over 32 sub-basins.
  * Latrubesse & Restrepo (2014) Geomorphology 216:225-233 — Colombian Andes mean SSY
    **1,485 t/km2/yr** (119 Andean gauging stations); N+C Andes weighted mean 2,045, total
    2.25 Gt/yr. Confirmed by two independent searches.
- [step 5] MOMPOSINA (task 3). Restrepo (2015), verbatim: "entre el 20 y 45 % de los sedimentos
  del sistema de los rios Magdalena-Cauca-Cesar quedan retenidos en la Depresion cada ano, una
  cifra que fluctua entre 36 y 80 millones de toneladas anualmente" — author labels it a
  PRELIMINARY figure (EAFIT + U. Colorado). So channel input above the Momposina =
  144+36 = 180 to 184+80 = 264 Mt/yr; /248.73 = **0.724 to 1.061**. Hillslope-to-channel
  delivery of ~1.0 means essentially zero hillslope deposition — the implausible end — which
  points at the erosion side, not the anchor.
- [step 6] Closest genuine modern analogue: Tan, Liu & Lu (2024) ESPL 49:1778-1795,
  doi 10.1002/esp.5797 — large, data-sparse, MOUNTAINOUS basin, RUSLE (hillslope) denominator.
  SDR 0.07-0.38 across 39 subbasins, ~30 % >= 0.35, model explains 86 % of SDR variance, and
  SDR is POSITIVELY correlated with drainage area (opposite sign to the classic decay).
  Basin-average gross erosion 23.7-26.5 t/ha/yr vs OURS 9.675 t/ha/yr -> ours low by
  **2.450-2.739x**. Applying their rate over 257,097 km2 gives 609.32-681.31 Mt/yr, and
  609.32 lands INSIDE docs/37's own "SDR 0.30 requires 480-613 Mt/yr" row.
- [step 7] Non-MUSLE sources: Dunne et al. (1998) GSA Bull 110(4):450-467 — Amazon bank-erosion
  supply 1,570 Mt/yr = 1.3x the Obidos flux ~1,200 Mt/yr (channel sources alone can exceed the
  outlet load); Dethier et al. (2023) Nature 620:787-793 — 396 mining districts / 49 countries,
  80 % of 173 mining-affected rivers have SSC >2x pre-mining; de Vente et al. (2007)
  Prog. Phys. Geog. 31(2):155-178 and Parsons et al. (2006) ESPL 31(10):1325-1328 retire the
  generality of the area-decay relation. A Magdalena-SPECIFIC non-hillslope fraction is
  **UNCITED** — no such partition is published.
- [step 8] VERDICT = **UNCITABLE**. The 0.05-0.30 number is approximately reproducible from
  three published relations (0.0997 / 0.1061 / 0.1439) but all three measure a DIFFERENT
  quantity (total-gross denominator), were fitted ~10^3x below our scale on US agricultural
  land, and their own source forbids out-of-domain use. No Magdalena SDR exists. Our ratio is
  a mixed total-outlet / hillslope-gross quantity that is 1.78 in USDA's own reference example,
  so it is not bounded by 1 and cannot pass or fail against any published SDR.
  Replacement test proposed: a gross-erosion-RATE test with three citable legs, all failed in
  the same direction, quantifying the residual at **1.59-2.74x** on the erosion side (which is
  much tighter than docs/37's 1.93-14.8x, and lands inside docs/37 §4 candidate 1's own 2-5x).
- [step 9] docs/40_sdr_evidence.md written (11 sections, 17 numbered citations each with retrieval
  status, plus 6 explicitly-UNCITED items). Final arithmetic re-verified:
  967.46/690 = 1.4021; 2200/967.46 = 2.2740; 967.46/2200 = 0.4398; channel share of gross erosion
  in NEH table 6-2 = 0.6087 and of yield = 0.8125; true SDR / hillslope-only DR = 2.108;
  710 t/km2/yr x 257,097 km2 = 182.54 Mt/yr, 0.79 % from the 184 Mt anchor.
- [step 10] DONE. Files touched: docs/40_sdr_evidence.md, docs/agents/journal_cite-sdr.md.
  Nothing else read-modified; no code, notebook or frozen artifact executed or changed;
  no calibration launched; no git commands run.
  NOT done (correctly out of scope, flagged for the docs agent): the edits to docs/37 itself.
  docs/40 §8.2 carries the paste-ready replacement wording for the closure-table row, for
  residual 3, and for the two consequential fixes in docs/37 §2 and §5.1.
