# 41 — The MUSLE cover factor C, on a citable footing

**Scope.** `docs/37` §4 residual 1: *"Basin area-weighted C = 0.01082 and its dominant term is
grassland C = 0.01, Roose's 'good condition' … Until then C is a choice, and it is at the low end
of its own range."* This document closes that gap: every row of
`data/processed/urh_cp_factors.csv` now carries a **source**, a stated **land condition**, and a
**low/central/high range**. It also answers residual 1's sibling question for P, and it corrects a
measurement error in how this table's sensitivity was ranked.

**Verdict in one line.** The evidence supports a **×1.20 central revision** of the basin total
(248.73 → **299.54 Mt/yr**), with a defensible range of **×0.43 to ×7.62 (107.3 – 1,896.3 Mt/yr)**.
The central case **does not close the SDR residual**, and the evidence does not support the value
that would. The single largest available upward lever — a published Colombian C = 0.6 for weedy
pasture — is **rejected on physics**, and it is rejected in writing before its effect was computed
(`docs/agents/journal_cite-cfactor.md` §5–§6).

---

## 1. What changed

| id | class | area % | C prior | **C central** | C low | C high | direction |
|----|-------|-------:|--------:|--------------:|------:|-------:|-----------|
| 1 | Forest | 55.774 | 0.003 | **0.005** | 0.001 | 0.037 | ↑ ×1.67 |
| 2 | Shrub | 0.119 | 0.005 *(ASSUMED)* | **0.015** | 0.003 | 0.100 | ↑, now cited |
| 3 | Grassland | 39.867 | 0.010 | **0.015** | 0.008 | 0.100 | ↑ ×1.5 |
| 4 | Cropland | 1.575 | 0.200 *(ASSUMED)* | **0.200** | 0.080 | 0.495 | unchanged, now cited |
| 5 | Urban | 0.297 | 0.010 *(ASSUMED)* | **0.030** | 0.000 | 0.200 | ↑, now cited |
| 6 | Bare | 0.196 | 1.000 | **0.500** | 0.250 | 1.000 | **↓ ×0.5** |
| 7 | Water | 0.649 | 0.000 | **0.000** | 0.000 | 0.001 | unchanged |
| 8 | Wetland | 1.523 | 0.001 | **0.005** | 0.001 | 0.010 | ↑ |

P is **1.0 for every class, unchanged** (§5). The prior values, prior sources and prior notes are
preserved verbatim in the CSV's `value_prior_2026_08_11`, `P_prior_2026_08_11`,
`source_prior_2026_08_11` and `note_prior_2026_08_11` columns, so the change is auditable without
this document. `C` in the loader-facing column equals `C_central`; `src/mgb_sediment.load_geometry`
reads only `class_id`, `C`, `P`, so the extra columns are inert to the engine.

---

## 2. The measurement that reorders everything: area weights are the wrong yardstick

`docs/agents/journal_c32-cp.md` §5 ranked this table's sensitivity by **area × C**. That ranking is
wrong, and the error is large. MUSLE weights a cell by `(Qsur·q_peak·A)^β · K·C·P·LS2D·FG`, and the
engine is **exactly linear in C** (`Sed_mini(t) = term(t,mini) × Σ_cells (A/a_p)·α·K·C·P·LS2D·FG`).
So the basin total decomposes as `Σ_c W_c · C_c`, where `W_c` is the class's *unit-C weight*.
`W_c` was computed on the frozen H2E drivers (`qsur_rel_mm`, the registered `Qsur`) and checked
against a full engine run: **relative difference 1.9 × 10⁻¹⁶**, and the decomposition reproduces
the published headline exactly — 2,486.957417 Mt over 3,652 days = **248.7298 Mt/yr**.

| class | area % | share of **area-weighted C** | share of **actual erosion** | ratio |
|---|---:|---:|---:|---:|
| Forest | 55.774 | 15.46 % | **36.48 %** | ×2.36 |
| Bare | 0.196 | 18.13 % | **35.60 %** | ×1.96 |
| Grassland | 39.867 | 36.83 % | 27.33 % | ×0.74 |
| Cropland | 1.575 | **29.10 %** | **0.47 %** | **×0.016** |
| Urban | 0.297 | 0.27 % | 0.06 % | ×0.22 |
| Shrub | 0.119 | 0.05 % | 0.06 % | ×1.06 |
| Wetland | 1.523 | 0.14 % | 0.0015 % | ×0.01 |
| Water | 0.649 | 0 | 0 | — |

Two consequences that matter more than the C revision itself:

- **Cropland is not the second-biggest lever; it is a rounding error.** It carries 29.1 % of the
  area-weighted C but **0.47 %** of the erosion, because cropland sits in the flat inter-Andean and
  lower valleys where LS2D and Qsur are small. Its whole defensible range, 0.08 → 0.495, moves the
  basin total by **less than ×1.01**. Any future effort spent refining the crop mosaic is wasted.
- **Forest is the largest single term at 36.5 %**, not the fourth at 15.5 %, because 55.8 % of the
  basin is forest *on the steep Andean flanks*. Bare is second at 35.6 % from 0.196 % of the area.

Per-class unit-C weights (Mt of decadal erosion per unit of C) are stored in the CSV's
`unit_C_weight_Mt_decade` column so this cannot be re-derived wrongly: Forest 302,443 · Grassland
67,959 · Bare 885 · Water 450 · Urban 148 · Shrub 289 · Cropland 58.8 · Wetland 36.5.

---

## 3. The evidence, by source

Sources are ordered as `docs/37` residual 1 asked: (a) a Magdalena–Cauca or Colombian Andean study,
(b) Latin American tropical, (c) FAO/Roose tables with the condition stated.

### (a) Colombian Andean, inside the basin

**Rengifo-Rengifo et al. (2022)**, "Modelo USLE para estimar la erosión hídrica en siete municipios
de la zona andina colombiana", *Biotecnología en el Sector Agropecuario y Agroindustrial* 20(2):
29–44, DOI 10.18684/rbsaa.v20.n2.2022.1738. Seven Cauca municipalities (Almaguer, Bolívar, Cajibío,
Mercaderes, Popayán, Puracé, Santander de Quilichao) spanning inter-Andean valley, sub-Andean and
high-Andean belts — all inside the Magdalena–Cauca. Their **Cuadro 4**, keyed on the Colombian
Corine legend, after Pacheco et al. (2019):

| class | C | | class | C |
|---|---:|---|---|---:|
| Bosque denso | 0.001 | | Mosaico de cultivos | 0.25 |
| Bosque de galería/ripario | 0.09 | | **Pastos limpios** | **0.01** |
| Arbustos | 0.25 | | **Pastos enmalezados o enrastrojados** | **0.6** |
| Herbazal | 0.01 | | Tejido urbano continuo | 0.001 |
| Mosaico de pastos y cultivos | 0.003 | | **Tierras desnudas o degradadas** | **1.0** |
| Mosaico de pastos c/ espacios naturales | 0.003 | | **Afloramientos rocosos** | **0.25** |
| Lagunas/lagos/ciénagas, Ríos, Red vial | 0.001 | | **Zonas glaciares y nivales** | **0.25** |

Two rows of this table are adopted here and one is refused. Adopted: *Pastos limpios* 0.01 (it
anchors the low end of the grassland row) and *Afloramientos rocosos* / *Zonas glaciares y nivales*
0.25 (they are what the Bare class physically *is* — see §4). Refused: *Pastos enmalezados* 0.6, for
the reason given in §6. The table is also internally inconsistent in places — crop mosaics at 0.003
sit *below* clean pasture at 0.01, continuous urban fabric is 0.001, and bare rock is 0.25 while
"tierras desnudas" is 1.0 — so it is used row by row with a stated reason, not wholesale.

### (b) Latin American tropical, with the condition stated and measured

**Lianes, Marchamalo & Roldán (2009)**, "Evaluación del factor C de la RUSLE para el manejo de
coberturas vegetales en el control de la erosión en la cuenca del río Birrís, Costa Rica",
*Agronomía Costarricense* 33(2): 217–235, ISSN 0377-9424. A 4,802 ha andisol catchment, 1,245–3,432 m
on the flank of Irazú volcano, dairy pasture plus highland horticulture — the closest available
analogue to Andean cattle country. Two distinct contributions:

**Cuadro 4 — C subfactors and soil-loss ratios MEASURED IN THE FIELD** by the original RUSLE
formulation (Renard et al. 1996): bosque natural 0.003 · **bosque degradado 0.037** · pasto de corta
0.012 · **potrero carga normal 0.002 · potrero degradado 0.002 · potrero muy degradado 0.016** ·
papa 0.122–0.731 across four crop stages · zanahoria 0.051–0.990 · brócoli 0.015–0.735.

The authors explain the pasture result (p. 229), and the explanation is the load-bearing part:
*potrero carga normal* and *potrero degradado* come out equal because both keep ~100 % ground-contact
cover, and the extra compaction of the heavier stocking rate *"está compensado por la alta rugosidad
del escalonamiento característico"* — the terracettes cut by cattle, whose figure caption is
literally *"Potrero con escalonamiento por sobrepastoreo"* — *"y la baja densidad de los andisoles"*.
The ground-contact subfactor SC, not canopy, dominates C.

**Cuadro 5 — a cross-source compilation.** Column attributions were resolved from the PDF's word
coordinates rather than guessed (x ≈ 222 Mora 1987 · 258 FAO 1989 · 288 ICE 1999 · 334 a single
column shared by Saborío 2002 / Gómez 2002 / CATIE 2003 · 394 Marchamalo 2004, 2007 · 438 Lianes
2009). The Saborío/Gómez/CATIE column is the one that states **condition** and gives **ranges**:

| cover, with condition | C |
|---|---|
| Bosque denso | 0.003–0.010 |
| Bosque claro, subestrato herbáceo denso | 0.003–0.010 |
| Bosque claro, subestrato herbáceo **degradado** | 0.010–0.100 |
| Matorral denso | 0.003–0.030 |
| Matorral claro, subestrato herbáceo **degradado** | 0.030–0.100 |
| Páramo | 0.003–0.040 |
| Pastizal natural completo | 0.003–0.010 *(printed "0,030-0,010"; the ordering of the three pastizal rows fixes the transposition)* |
| **Pastizal natural pastoreado** | **0.040–0.200** |
| **Pastizal cultivado (manejado)** | **0.003–0.040** |
| Cultivos permanentes asociados (densos) | 0.010–0.300 |
| Cultivos permanentes no densos | 0.100–0.450 |
| Cultivos anuales de ciclo corto / largo | 0.300–0.800 / 0.400–0.900 |

Same table, other columns — FAO 1989: Pasto 0.009 · Pasto (natural o mejorado) 0.008 · Café 0.09 ·
Banano 0.062 · Cacao 0.05 · Caña 0.263 · Cultivos anuales 0.495 · Maíz 0.519. ICE 1999: Bosque
natural 0.001–0.003 · **Pasto 0.01–0.015** · Cultivos perennes 0.086. Marchamalo 2004/2007: Bosque
0.003 · Charral 0.012 · **Pasto 0.013** · Café 0.080 · Caña 0.050.

### (c) MGB-SED's own upstream C source

`Fagundes et al. (2021)`, *WRR* 57, e2020WR027884, states that MGB-SED assigns C per URH from
**Benavidez et al. (2018)**, Buarque (2015) and Fagundes et al. (2019). The Wiley full text is
paywalled to this session, so Fagundes' own per-class table remains un-ingested (§7, residual A);
the cited review was read: **Benavidez, Jackson, Maxwell & Norton (2018)**, "A review of the
(Revised) Universal Soil Loss Equation ((R)USLE)…", *HESS* 22: 6059–6086,
doi:10.5194/hess-22-6059-2018, **Table 8** (columns again resolved by x-coordinate):

| cover | Dymond 2010 (NZ) | David 1988 (PH) | Morgan 2005 | Fernandez 2003 (US) | Dumas & Fossey 2009 (VU) | LDD 2002 (TH) |
|---|---|---|---|---|---|---|
| Bare ground | 1 | 1 | 1 | | | |
| Urban | | 0.2 | | 0.03 | 0 | 0 |
| Crop | | | | 0.128 | 0.01 | 0.255–0.525 |
| Forest | 0.005 | 0.001–0.006 | 0.001 | 0.001 | 0.001 | 0.003–0.048 |
| **Pasture** | **0.01** | | **0.1** | | | |
| Scrub | 0.005 | 0.007–0.9 | 0.01 | 0.003 | 0.16 | 0.01–0.1 |

Note that MGB-SED's own C authority puts pasture at **0.01–0.1** — the same factor of ten as Roose.
The range in `docs/37` residual 1 is therefore not an artefact of one old African table; it is the
state of the literature.

### Land-condition evidence for the basin

1. **IDEAM, MADS & U.D.C.A. (2015)**, *Estudio Nacional de la Degradación de Suelos por Erosión en
   Colombia*, Bogotá, 188 pp. Reached only through a **secondary** summary (IECA Iberoamérica) —
   flagged as such. **40 % of continental Colombia is eroded: 20 % ligera, 17 % moderada, 3 %
   severa, 0.2 % muy severa.** Water erosion 39.16 % (laminar 19.33 %, laminar + gullies 9.31 %,
   terracettes + laminar 7.30 %), wind 0.61 %. 29.9 % of the surface is under livestock and **77 %
   of that shows some degree of erosion**; **74 % of the Magdalena–Cauca is affected**; "territorios
   ganaderos" = 36.59 % of the causal factors. Reading: erosion under pasture is *widespread* but
   overwhelmingly *light-to-moderate* — severe plus very severe is 3.2 % of the country.
2. **MADS/IDEAM/UNCCD (2018)**, *República de Colombia: Neutralidad en la Degradación de las
   Tierras — informe país (LDN TSP)*, 54 pp, **Tabla 12**: JRC Land Productivity Dynamics on the
   Corine class *Pastos y herbazales* (383,732 km² in 2002 → 414,505 km² in 2012) —
   declining 5,774.2 km² (**1.7 %**) · early deterioration 7,281.3 km² (**2.2 %**) ·
   stable-but-stressed 35,170.4 km² (**10.5 %**) · stable-not-stressed 172,508.7 km² (**51.6 %**) ·
   **increasing 112,269.1 km² (33.6 %)**. So **~14.4 % of Colombian pasture is stressed or worse and
   ~85 % is not.** *Sobrepastoreo* appears in the same report's list of direct causes but is not
   quantified. Caveat: LPD is an NDVI-productivity indicator, not a ground-cover measurement, and a
   productivity rise can come from fertiliser or improved grasses.
3. **Consorcio POMCAS Oriente Antioqueño (2016)**, *POMCA río Nare, Fase Diagnóstico §4.11* for
   CORNARE — Corine Land Cover Colombia over 94,353.7 ha of a **direct Magdalena tributary**. This
   is the only *in-basin, measured* pasture-condition split found. 2011: Pastos limpios 38,039.83 ha
   (40.24 % of basin) · Pastos enmalezados 5,338.43 ha (5.65 %) · Pastos arbolados 75.94 ha (0.08 %)
   · Áreas erosionadas 76.42 ha (0.08 %). **Within the pasture classes: 87.5 % limpios (managed),
   12.3 % enmalezados, 0.2 % arbolados.** For contrast, 1986: 21.57 % / 9.64 % → 69 % / 31 %.
   Same table, forest: bosque denso alto 5.91 % against bosque abierto alto 10.73 % + vegetación
   secundaria alta 10.58 % + veg. secundaria baja 7.54 % + bosque fragmentado c/ veg. secundaria
   1.90 % — **open and secondary stands outweigh dense forest about 5 : 1.** This is the measured
   basis for raising Forest from the closed-canopy end.
4. **CIAT (1999, 2005)**, as cited in the *Rehabilitación de praderas degradadas en el trópico de
   México* review (*Rev. Mex. Cienc. Pecu.*): ~60 % of tropical America's ~400 Mha of pasture is
   degraded. Flagged **SECONDARY** — CIAT was not read directly, and "degraded" there is an
   agronomic-productivity term, not a ground-cover term.

---

## 4. Why each central value is what it is

- **Forest 0.003 → 0.005.** The condition call is *secondary/open forest with a dense herbaceous
  understorey*, measured from the Nare CLC split above. 0.005 is the mid of Saborío/Gómez/CATIE's
  *bosque claro, subestrato herbáceo denso* 0.003–0.010 and is independently Dymond (2010)'s forest
  value in Benavidez Table 8. Low 0.001 = closed canopy (Roose, Morgan, Fernandez, and Rengifo's
  *bosque denso*). High 0.037 = Lianes' **field-measured** *bosque degradado*.
- **Grassland 0.010 → 0.015.** See §6.
- **Bare 1.000 → 0.500.** `docs/37` §3 gate (a) asked for exactly this: *"bare rock/ash/ice above
  the treeline carries C = 1.0 … The fix belongs in `urh_cp_factors.csv` with a written reason."*
  The class is measured to be above-treeline rock, ash and ice — WorldCover 60 at 0.191 % and 70 at
  0.013 % of the URH grid, and every bare-dominated minibacia is above the treeline (the eight
  highest sit at ~10.8 N/73.6 W and ~9.7 N/73.5 W in the Sierra Nevada/Perijá, ~4.9 N/75.4 W in Los
  Nevados and ~2.9 N/76.1 W in Puracé–Huila). Rengifo gives 0.25 for *afloramientos rocosos* **and**
  for *zonas glaciares y nivales*; W&S 1978 / Roose / Benavidez give 1.00 for bare soil. Central
  0.50 = √(0.25 × 1.00), an **explicit interpolation**, labelled as one, because the class mixes
  bare rock and ice (0.25) with the loose, genuinely detachable volcanic ash of the Los Nevados and
  Puracé cells (1.00). This change **lowers** the model by ×0.822 on its own.
- **Shrub, Urban, Wetland** were uncited ASSUMED values; they are now cited (§3) with conditions and
  ranges. Together their full low-to-high spans move the basin total by ~×1.01, so they are recorded
  for completeness rather than for effect.
- **Cropland unchanged at 0.200**, now with cited endpoints (all-perennial 0.08 → annual-dominated
  0.495) instead of an ASSUMED label. §2 explains why refining it further is pointless.

---

## 5. P: is there a citable basis for a basin-wide P < 1?

**Answer: no defensible one, and P stays 1.0 for every class.**

1. **Definitional.** Wischmeier & Smith (1978) AH-537 define P for **support practices** —
   contouring, strip-cropping, terracing — and set P = 1.0 for up-and-down-slope tillage or no
   practice. No conservation-practice layer exists for the Magdalena–Cauca, so 1.0 is the
   definitional value, not a default reached for lack of thought.
2. **The one citable sub-1 scheme is a category error.** Rengifo-Rengifo et al. (2022) Cuadro 5,
   after Pacheco et al. (2019), assigns P by **land use**: Área arbolada 0.1 · Tierra agrícola 0.4 ·
   Cuerpos de agua 0.5 · Terreno edificable/baldío 1.0. P keyed on land use double-counts the cover
   effect that C already carries — a forest does not have a *support practice*. Note also that even
   in that scheme **both pasture classes keep P = 1.0**, so it would not touch 39.9 % of this basin.
3. **Empirical check that P ≈ 1 is also the right answer.** MADS/IDEAM/UNCCD (2018) sets national
   2030 targets of **9,000 ha** of pasture converted to silvopastoral systems and **100,000 ha** of
   degraded land restored nationally, against **414,505 km² (41.45 Mha)** of national pasture —
   adopted practice of order **0.02–0.24 %** of the pasture area. FEDEGÁN's *Ganadería Colombiana
   Sostenible* reports 50,500 ha converted. At basin scale P = 1.0 is not merely conservative; it is
   approximately correct.
4. **Direction, stated as `docs/37` residual 4 requires.** Any **P < 1 LOWERS modelled erosion and
   WIDENS the residual.** Measured here: applying the Rengifo/Pacheco P column to the revised C
   gives **299.54 → 162.44 Mt/yr, ×0.542** (with the prior C it is 248.73 → 166.26, ×0.669). It
   moves the model **away** from the asserted SDR band, not towards it. P = 1.0 happens to be the
   erosion-maximising choice, which is a reason to hold it to the definitional justification in (1)
   — which it meets — and to keep reporting the practice term as an **upper bound**.

The `P_low` column in the CSV records the Rengifo/Pacheco values so the sensitivity is auditable
without re-deriving it; `P` and `P_central` are 1.0 and `P_high` is 1.0.

---

## 6. Grassland: the decisive row, and one value refused

### The refusal, recorded before any arithmetic

Rengifo-Rengifo et al. (2022) give **Pastos enmalezados o enrastrojados C = 0.6**. Combined with the
Nare split (87.5 % limpios @ 0.01 + 12.3 % enmalezados @ 0.6) that puts the grassland row at
**≈ 0.083**, i.e. **×8.3** on the row and — computed afterwards, for the record — **742.2 Mt/yr,
×2.98** on the basin total. That single move would close most of the `docs/37` residual.

**It is rejected, on physics, and the rejection was written down before the effect was computed**
(`docs/agents/journal_cite-cfactor.md` §5, which precedes §8's arithmetic in the file and in time):

- IDEAM's own national legend defines class 2.3.3 *Pastos enmalezados o enrastrojados* as pasture
  **invaded by weeds and secondary vegetation** through scarce management or abandonment. In (R)USLE
  the dominant subfactor is **ground-contact cover** — Lianes et al. (2009) p. 229 measure exactly
  that and say so. Weed and *rastrojo* invasion **increases** ground cover, so C for *enmalezado*
  pasture must be **lower** than for clean pasture, not sixty times higher.
- Rengifo's own P table files *pastos enmalezados* under *"Terreno edificable / Tierra baldía"*
  (wasteland), which shows the authors read "enmalezado" as bare or derelict — a misreading of the
  class they were keying on.
- The same table is inconsistent elsewhere (§3a).

### The choice

**Central 0.015, range 0.008 – 0.100.** The condition is *grazed, humid-tropical **sown** cattle
pasture in fair condition* — CLC *pastos limpios*, Brachiaria/kikuyu. Roose's label "savanna and
prairie in **good condition**" was the wrong description even though his number was close: this is
grazed land. But the evidence does not put it at the degraded end either, and four independent lines
converge low:

| source | value | what it is |
|---|---|---|
| Rengifo-Rengifo et al. (2022) | **0.01** | *Pastos limpios*, Cauca, **Colombia** |
| FAO (1989) | 0.008 / 0.009 | *Pasto (natural o mejorado)* / *Pasto*, tropical |
| ICE (1999) | **0.01–0.015** | *Pasto*, Costa Rica |
| Marchamalo (2004, 2007) | 0.013 | *Pasto*, same catchment |
| Lianes et al. (2009) | 0.002 / 0.002 / **0.016** | **field-measured** potrero at normal stocking / degraded / very degraded |

The high tabulated band — *Pastizal natural pastoreado* 0.040–0.200, Roose's overgrazed-or-burnt
0.1, Morgan (2005) 0.1 — is for **natural rangeland under grazing** with incomplete ground cover, a
semi-arid situation. The Magdalena's grassland is the *Pastizal cultivado (manejado)* row,
**0.003–0.040**.

0.015 is chosen as the **top** of the converging band rather than its middle, for three cited
reasons: 77 % of Colombia's livestock land carries some erosion and 74 % of the Magdalena–Cauca is
affected (IDEAM 2015); ~14.4 % of Colombian pasture is stressed or declining (LDN 2018 Tabla 12);
and Lianes' *measured* value for very degraded tropical pasture is 0.016. It is simultaneously the
top of ICE 1999's band and just under Lianes' measured degraded value — a cited number, not a nudge.

**Stated in advance and repeated here: ×1.5 on the dominant term cannot close a 1.93–14.8×
residual. The evidence does not support the value that would.**

---

## 7. Effect on the basin total, as a range

Area-weighted basin-mean C, and the **exact** effect on gross erosion (the engine is linear in C, so
these are not estimates):

| scenario | area-weighted mean C | ratio | **basin gross erosion** | **ratio** |
|---|---:|---:|---:|---:|
| prior (2026-08-11) | 0.010823 | 1.000 | 248.73 Mt/yr | 1.000 |
| **low** | 0.005516 | ×0.510 | **107.32 Mt/yr** | **×0.4315** |
| **central (adopted)** | 0.013083 | ×1.209 | **299.54 Mt/yr** | **×1.2043** |
| **high** | 0.071133 | ×6.572 | **1,896.26 Mt/yr** | **×7.6238** |

The adopted central case was verified end-to-end after writing the CSV: `load_geometry` +
`simulate_sediment(SedParams(), qsur_rel_mm)` returns 2,994.977042 Mt over 3,652 days =
**299.5387 Mt/yr**, against 299.539 predicted by the linear decomposition, with the mass ledger
exact (`residual_t == 0.0`, `exact: True`).

One-at-a-time, prior → central and prior → high:

| class | → central | → high |
|---|---|---|
| Forest | 309.23 Mt/yr ×1.243 | 1,277.18 Mt/yr ×5.135 |
| Grassland | 282.71 Mt/yr ×1.137 | 860.45 Mt/yr ×3.459 |
| **Bare** | **204.46 Mt/yr ×0.822** | 248.73 Mt/yr ×1.000 |
| Urban | 249.03 ×1.001 | 251.54 ×1.011 |
| Shrub | 249.02 ×1.001 | 251.48 ×1.011 |
| Cropland | 248.73 ×1.000 | 250.46 ×1.007 |
| Wetland | 248.74 ×1.000 | 248.76 ×1.000 |
| Water | 248.73 ×1.000 | 248.78 ×1.000 |

**So the ×1.20 central is a net of two opposing corrections**: Forest +×1.243 and Grassland +×1.137
pulling up, Bare ×0.822 pulling down. The largest revision in the table lowers the model.

### What this does, arithmetically, to the SDR clause

`docs/37` §4 reports an implied SDR of 0.579–0.740 at 248.73 Mt/yr, which back-implies an observed
outlet load of ~144–184 Mt/yr. Dividing that load by each scenario's gross erosion:

| scenario | gross erosion | implied SDR |
|---|---:|---|
| low | 107.32 Mt/yr | **1.34 – 1.72** |
| prior | 248.73 Mt/yr | 0.579 – 0.740 |
| central (adopted) | 299.54 Mt/yr | **0.481 – 0.614** |
| high | 1,896.26 Mt/yr | **0.076 – 0.097** |

Two things follow, and only two:

1. **The low end of the C range is refuted**, not by any plausibility band but by mass balance:
   it implies SDR > 1, i.e. the basin exporting more sediment than it erodes. That is a legitimate
   hard constraint and it is the only gate applied here.
2. The asserted 0.05–0.30 SDR band **is not cited in this repository** (`docs/37` residual 3), so
   per that document's own rule it may be used neither to pass nor to fail this revision. The
   central case lands at 0.48–0.61 and the high case at 0.08–0.10; **which of those is right is not
   decidable from an uncited band**, and this document does not decide it. Residual 1 is closed —
   C is now cited, conditioned and ranged.

### Cross-reference: `docs/40` retires the SDR gate outright

A parallel run settled residual 3 in [`docs/40_sdr_evidence.md`](40_sdr_evidence.md): the
0.05–0.30 band is **UNCITABLE**, because the published SDR-versus-area relations measure a
different quantity (gross erosion *including* gullies, banks and channels) from the hillslope-only
MUSLE sum, at ~3 orders of magnitude smaller scale. It replaces the SDR clause with a
**gross-erosion-rate** test and quantifies the residual at **1.59 – 2.74×** on the erosion side.

Read against that replacement yardstick rather than the retired SDR band, the arithmetic is:

| scenario | gross erosion | vs `docs/40`'s 1.59–2.74× target (395.5 – 681.5 Mt/yr) |
|---|---:|---|
| prior | 248.73 Mt/yr | short by ×1.59 – 2.74 (the residual as `docs/40` states it) |
| **central (adopted)** | **299.54 Mt/yr** | still short by **×1.32 – 2.27** |
| high | 1,896.26 Mt/yr | **overshoots** by ×2.78 – 4.79 |

So the cited-and-conditioned central revision accounts for roughly **a quarter to a third** of
`docs/40`'s residual (in log terms) and leaves the rest open — while some intermediate value inside
this table's own low-to-high range would land squarely inside the target. **That value is not
adopted, and deliberately so:** picking a C to hit a residual is the exact failure mode this run
was built to avoid, and `docs/35` §6 RULE 0 forbids the same move for α. The residual stays visible.
`docs/40` reaches the same conclusion from the other side — that its remaining gap "lands inside the
2–5× that `docs/37` §4 candidate 1 (the cover factor C) already estimated for itself" — and this
document is the measurement of how much of that 2–5× the *evidence* actually supports: **×1.20**,
not 2–5.

---

## 8. Consequences the caller must action

1. **`tests/test_sediment.py` has two stale hard-coded C values and now FAILS 2 of 50.** Not my file
   to edit; both are one-line provenance updates, not defects:
   - line 310, `assert abs(g.cell_c[j] - 0.003) < 1e-12` → `0.005`; and the load it then checks,
     `UNIT_DAY_LOAD_T = 1293.5691626849571`, becomes **2155.9486044749287** (× 0.005/0.003) for the
     *file-based* join guard `test_audit_unit_day_reproduces_from_the_real_files`. The **synthetic**
     §3b regression at line ~245 passes `class_c={1: 0.003}` explicitly and **must be left alone** —
     it is a convention-arithmetic regression, not a statement about the CSV.
   - lines 683–684, `set(np.unique(g.cell_c)) <= {0.003, 0.005, 0.01, 0.2, 1.0, 0.0, 0.001}` →
     `{0.0, 0.001, 0.005, 0.015, 0.03, 0.2, 0.5}`.
   - `test_dry_and_inert_cells_are_exactly_zero_on_real_data` still passes and constrains this table:
     **Water must stay exactly 0.0.**
2. **The 248.73 Mt/yr headline is superseded by 299.54 Mt/yr** wherever it is quoted — `docs/35`,
   `docs/36`, `docs/37` §3–§4, `docs/PROGRESS.md` and any figure or deck built from them. It remains
   a **lower bound** for all the reasons `docs/35` §5.3 gives; nothing here touches the peak deficit
   or the `f_peak` bracket.
3. **The ENSO contrast is unchanged.** C is a static per-class multiplier with no seasonality, so
   every scenario in §7 rescales all windows identically: the 2.29× primary / 3.93× sensitivity wet
   : dry ratios are invariant under any row-wise C revision.
4. **`docs/37` §3 gate (a)'s carried-forward artefact is now fixed** in the file it said the fix
   belonged in, with the reason written in the row.
5. **Correct the sensitivity ranking in `docs/agents/journal_c32-cp.md` §5** and anywhere it was
   propagated: cropland is 0.47 % of erosion, not the 29.1 % its area-weighted C share implied.
6. `data/processed/` is gitignored, so this hand-curated literature table is still unversioned
   (the `journal_c32-cp.md` residual (e) is unchanged). Everything needed to rebuild it is in this
   document and in the CSV's own `source` / `land_condition` / `note` columns.

## 9. Residuals

- **A.** Fagundes et al. (2021) is paywalled to this session, so MGB-SED's **own** per-URH C table is
  still un-ingested; only its cited review (Benavidez et al. 2018) was read. If the paper is
  obtained, diff its C per class against this table.
- **B.** IDEAM/MADS/U.D.C.A. (2015) was reached only via a secondary summary. The primary 188-pp
  study should replace it, and its per-department and per-basin erosion figures would sharpen the
  grassland condition call.
- **C.** The Nare basin is one Magdalena tributary (94,354 ha of 257,097 km²). A basin-wide
  *pastos limpios* : *enmalezados* : *arbolados* split from the IDEAM/IGAC/CORMAGDALENA
  *Mapa de Cobertura de la Tierra Cuenca Magdalena–Cauca* (1:100,000) would replace an extrapolation
  from one sub-basin with a measurement. The map exists; its class areas were not reachable here.
- **D.** `Pastos enmalezados` deserves a *lower* C than clean pasture on the argument in §6, but no
  source was found that states one. If the basin-wide split in (C) is obtained, the honest treatment
  is to give the *enmalezado* fraction a C at or below the clean-pasture value, which would lower
  the grassland row slightly, not raise it.
- **E.** Bare's central 0.50 and Wetland's 0.005 are labelled interpolations between cited
  endpoints, not table values. Bare matters (35.6 % of erosion at the prior C); a source that states
  C for *loose volcanic ash above the treeline* would replace the interpolation with a value.

## 10. Reproduction

```
python3.10 -m pytest tests/test_sediment.py -q     # 48 passed, 2 failed (stale C in tests, s8.1)
```

The per-class unit-C weights and every scenario in §7 follow from
`W_c = Σ_{cells in c} [ Σ_t term(t, mini) ] × (A_cell/a_p)·α·K·P·LS2D·FG`, i.e.
`cell_static_factor` on a geometry with `cell_c` replaced by ones, times the time-integrated
`runoff_energy_term` on `h2e_drivers.npz:qsur_rel_mm`. The identity
`Σ_c W_c·C_c == simulate_sediment(...).ledger["eroded_t"]` was checked and holds to
1.9 × 10⁻¹⁶ relative, so no scenario in §7 required a re-simulation and none is an approximation.
