# Journal — cite-cfactor

## Goal

Settle docs/37 residual 1: put the MUSLE cover factor **C** (and practice factor **P**) on a
citable footing, per land class, with a stated land CONDITION and a low/central/high RANGE.
Basin area-weighted C is currently 0.01082, dominated by Grassland C = 0.01 ("savanna/prairie
in good condition", Roose) carrying 36.8 % of it. Roose's own table spans ×10 up to
overgrazed/burnt pasture, so this single value could account for a factor 2–5 of the SDR
residual.

## Honesty gate (the whole discipline of this task)

I will record the CHOSEN central value for grassland (and every other class) in this journal
**before** computing the effect on the 248.73 Mt/yr basin total. If the evidence supports
staying at 0.01 I will say so, even though it leaves the residual open.

## Checklist

- [ ] 1. Read `data/processed/urh_cp_factors.csv` and `docs/agents/journal_c32-cp.md`
- [ ] 2. Read docs/37 (residuals 1, 3, 4) and docs/00_INDEX.md for context
- [ ] 3. Get class areas / area weights (recompute, don't trust memory)
- [ ] 4. Literature search: (a) Magdalena-Cauca / Colombian Andean MUSLE-RUSLE study;
        (b) Latin American tropical; (c) FAO/Roose with condition stated
- [ ] 5. Evidence on ACTUAL Colombian Andean pasture condition (degradation, overgrazing)
- [ ] 6. Evidence on P: any citable basin-wide P < 1? Note P < 1 LOWERS erosion and WIDENS residual
- [ ] 7. RECORD CHOSEN VALUES HERE (before computing effect)
- [ ] 8. Recompute area-weighted basin-mean C low/central/high; multiplicative effect on 248.73 Mt/yr
- [ ] 9. Write revised `data/processed/urh_cp_factors.csv` (prior values kept in
        `value_prior_2026_08_11`) and `docs/41_cfactor_evidence.md`

## Log

### Step 1 — start, read current state

Current table (`data/processed/urh_cp_factors.csv`), 8 classes, point values only:

| id | class | C | P |
|----|-------|---|---|
| 1 | Forest | 0.003 | 1.0 |
| 2 | Shrub | 0.005 | 1.0 |
| 3 | Grassland | 0.01 | 1.0 |
| 4 | Cropland | 0.2 | 1.0 |
| 5 | Urban | 0.01 | 1.0 |
| 6 | Bare | 1.0 | 1.0 |
| 7 | Water | 0.0 | 1.0 |
| 8 | Wetland | 0.001 | 1.0 |

Sources already in the file: Wischmeier & Smith (1978) AH-537 Table 10 for Forest/Bare;
Roose (1977, in Greenland & Lal; reproduced FAO Soils Bulletin 70, Roose 1996) for
Grassland/Wetland/Cropland components. Shrub and Urban are marked ASSUMED with no table value.
All P = 1.0, marked as an EXPLICIT ASSUMPTION (no conservation-practice layer exists).

### Step 2 — area weights RECOMPUTED (not trusted from the prior journal)

`model_inputs_v2/parameters.npz:urh_fraction` × `topology.npz:own_area_km2`, land class = `urh_id % 10`.
8,672 units, total 257,096.93 km². Reproduces the c32-cp numbers exactly:

| class | km² | % of basin |
|---|---|---|
| 1 Forest | 143,394.393 | 55.774448 |
| 2 Shrub | 305.237 | 0.118724 |
| 3 Grassland | 102,496.016 | 39.866682 |
| 4 Cropland | 4,049.105 | 1.574933 |
| 5 Urban | 763.720 | 0.297055 |
| 6 Bare | 504.571 | 0.196257 |
| 7 Water | 1,667.919 | 0.648751 |
| 8 Wetland | 3,915.969 | 1.523149 |

Sum check 257,096.931 km² (= total, no loss).

### Step 3 — literature found (running list, with what each establishes)

**(b/c) Lianes, Marchamalo & Roldán (2009)**, "Evaluación del factor C de la RUSLE para el manejo
de coberturas vegetales en el control de la erosión en la cuenca del río Birrís, Costa Rica",
*Agronomía Costarricense* 33(2): 217–235, ISSN 0377-9424. Andisol volcanic highland catchment
(4,802 ha, 1,245–3,432 m, Irazú volcano), dairy pasture + horticulture. Retrieved and read in
full (PyMuPDF, 20 pp).
- **Cuadro 4** = C SUBFACTORS AND SLR MEASURED IN THE FIELD by the original RUSLE formulation
  (Renard et al. 1996): bosque natural 0.003 · bosque degradado 0.037 · pasto de corta 0.012 ·
  **potrero carga normal 0.002 · potrero degradado 0.002 · potrero muy degradado 0.016** ·
  papa (4 stages) 0.122–0.731 · zanahoria 0.051–0.990 · brócoli 0.015–0.735.
- The authors explain WHY degraded pasture stays low (p. 229): potrero carga normal and potrero
  degradado both keep near-complete ground-contact cover (Sp 100 %), and the extra compaction of
  the heavier stocking rate "está compensado por la alta rugosidad del escalonamiento
  característico" (cattle terracettes, their Fig. 4 caption is literally
  "Potrero con escalonamiento por sobrepastoreo") "y la baja densidad de los andisoles". The
  ground-contact subfactor SC is the dominant control on C, not canopy.
- **Cuadro 5** is a compilation across sources. Column x-positions resolved from the PDF word
  coordinates so attributions are not guessed: x≈222 Mora 1987 · x≈258 FAO 1989 · x≈288 ICE 1999 ·
  x≈334 a single shared column headed Saborío 2002 / Gómez 2002 / CATIE 2003 · x≈394 Marchamalo
  2004, 2007 · x≈438 Lianes 2009.
  The x≈334 (Saborío/Gómez/CATIE) column is the one that states CONDITION and gives RANGES:
  Bosque denso 0.003–0.010 · Bosque claro, subestrato herbáceo denso 0.003–0.010 ·
  Bosque claro, subestrato herbáceo **degradado 0.010–0.100** · Matorral denso 0.003–0.030 ·
  Matorral claro, subestrato herbáceo degradado 0.030–0.100 · **Páramo 0.003–0.040** ·
  Pastizal natural completo 0.003–0.010 (printed "0,030-0,010", a transposition typo — the
  ordering of the three pastizal rows fixes the intent) ·
  **Pastizal natural pastoreado 0.040–0.200** · **Pastizal cultivado (manejado) 0.003–0.040** ·
  Cultivos permanentes asociados (densos) 0.010–0.300 · Cultivos permanentes no densos
  0.100–0.450 · Huertos de subsistencia 0.300–0.900 · Cultivos anuales ciclo corto 0.300–0.800 ·
  ciclo largo 0.400–0.900.
  FAO 1989 column: Pasto 0.009 · Pasto (natural o mejorado) 0.008 · Café 0.09 · Banano 0.062 ·
  Cacao 0.05 · Caña 0.263 · Cultivos anuales 0.495 · Maíz 0.519.
  ICE 1999 column: Bosque natural 0.001–0.003 · Pasto 0.01–0.015 · Cultivos perennes 0.086.
  Marchamalo 2004/2007: Bosque 0.003 · Charral 0.012 · Pasto 0.013 · Café 0.080 · Caña 0.050.

**TENSION recorded immediately, before any choice:** the tabulated tropical value for *grazed*
natural grassland is 0.040–0.200, i.e. 4–20× the current 0.01 — but the only FIELD-MEASURED
tropical-highland pasture values in the same paper say degraded pasture is 0.002 and *very*
degraded pasture 0.016, i.e. at or barely above the current 0.01. These point in opposite
directions and the honest reading has to weigh them, not pick one.

**(a) Rengifo-Rengifo et al. (2022)**, "Modelo USLE para estimar la erosión hídrica en siete
municipios de la zona andina colombiana", *Biotecnología en el Sector Agropecuario y
Agroindustrial* 20(2): 29–44, DOI 10.18684/rbsaa.v20.n2.2022.1738. **Cauca department — inside
the Magdalena–Cauca basin** (Almaguer, Bolívar, Cajibío, Mercaderes, Popayán, Puracé, Santander
de Quilichao; inter-Andean valley / sub-Andean / high-Andean). Retrieved full PDF (16 pp).
Their **Cuadro 4** C values, keyed on the Colombian (Corine-style) land-cover legend, attributed
by them to Pacheco et al. (2019):
Afloramientos rocosos 0.25 · Arbustos 0.25 · Bosque de galería/ripario 0.09 · **Bosque denso
0.001** · Herbazal 0.01 · Lagunas/lagos/ciénagas 0.001 · Mosaico de cultivos, pastos y espacios
naturales 0.003 · Mosaico de pastos con espacios naturales 0.003 · Mosaico de pastos y cultivos
0.003 · Mosaico de cultivos 0.25 · **Pastos enmalezados o enrastrojados 0.6** ·
**Pastos limpios 0.01** · Red vial 0.001 · Ríos 0.001 · Tejido urbano continuo 0.001 ·
**Tierras desnudas o degradadas 1** · Zonas glaciares y nivales 0.25.
Their **Cuadro 5** P values (same Pacheco et al. 2019 method): Tierra agrícola 0.4 ·
Terreno edificable/baldío (incl. BOTH pasto classes, urban, bare, rock, glacier) 1.0 ·
Área arbolada 0.1 · Cuerpos de agua 0.5.

Quality caveats I am recording rather than hiding: this table is internally inconsistent in
places (mosaics of crops at 0.003, *below* clean pasture 0.01; continuous urban fabric 0.001 for
a class that also contains construction ground; bare rock 0.25 while "tierras desnudas" is 1.0),
and its "P" is keyed on LAND USE, not on any mapped conservation practice — assigning P = 0.1 to
forest double-counts cover in the practice term. So I will use it for the two pasture rows
(where it is direct, Colombian, and condition-explicit) and treat its P column with suspicion.

### Step 4 — more evidence: MGB-SED's own C source, and CONDITION data

**MGB-SED's own upstream C source.** Fagundes et al. (2021, *WRR* 57, e2020WR027884) state that
MGB-SED's C per URH comes from Benavidez et al. (2018), Buarque (2015) and Fagundes et al. (2019);
the Wiley full text is 403 to me, so I could not read Fagundes' own table (recorded as a residual).
I *could* read the cited review: **Benavidez, Jackson, Maxwell & Norton (2018)**, "A review of the
(Revised) Universal Soil Loss Equation ((R)USLE)...", *HESS* 22: 6059-6086, doi:10.5194/hess-22-6059-2018.
**Table 8** ("C factors for general types of land cover compiled from various sources"), columns
resolved by right-edge x so attributions are not guessed (x1: 161.2 Dymond 2010 NZ / 221.0 David
1988 Philippines / 265.1 Morgan 2005 / 334.1 Fernandez et al. 2003 USA / 396.8 Dumas & Fossey 2009
Vanuatu / 522.0 Land Development Department 2002 Thailand):
- Bare ground **1** (Dymond, David, Morgan)
- Urban 0.2 (David) / 0.03 (Fernandez) / 0 (Dumas) / 0 (LDD)
- Crop 0.128 (Fernandez) / 0.01 (Dumas) / 0.255-0.525 (LDD)
- Forest 0.005 (Dymond) / 0.001-0.006 (David) / 0.001 (Morgan) / 0.001 (Fernandez) / 0.001 (Dumas)
  / 0.003-0.048 (LDD)
- **Pasture 0.01 (Dymond 2010) / 0.1 (Morgan 2005)** — a factor of 10, the same spread as Roose
- Scrub 0.005 (Dymond) / 0.007-0.9 (David) / 0.01 (Morgan) / 0.003 (Fernandez) / 0.16 (Dumas) /
  0.01-0.1 (LDD)

**CONDITION evidence 1 — national erosion.** IDEAM, MADS & U.D.C.A. (2015), *Estudio Nacional de
la Degradacion de Suelos por Erosion en Colombia*, Bogota, 188 pp. As summarised by IECA
Iberoamerica (secondary route; the primary PDF was not reachable, so this is flagged SECONDARY):
**40 % of continental Colombia is eroded — 20 % ligera, 17 % moderada, 3 % severa, 0.2 % muy
severa**; water erosion 39.16 % (laminar 19.33 %, laminar+gullies 9.31 %, terracettes+laminar
7.30 %), wind 0.61 %; 29.9 % of the surface is under livestock and **77 % of that shows some
degree of erosion**; **74 % of the Magdalena-Cauca watershed is affected**; "territorios
ganaderos" = 36.59 % of the causal factors. Reading: erosion under pasture is WIDESPREAD but
overwhelmingly in the *ligera*/*moderada* classes — severe + very severe is 3.2 % of the country.

**CONDITION evidence 2 — pasture productivity, Colombia.** MADS/IDEAM/UNCCD (2018), *Republica de
Colombia: Neutralidad en la Degradacion de las Tierras — informe pais (LDN TSP)*, 54 pp,
Tabla 12, JRC Land Productivity Dynamics on the CLC "Pastos y herbazales" class
(383,732 km2 2002 -> 414,505 km2 2012):
declining **5,774.2 km2 (1.7 %)** / early deterioration **7,281.3 km2 (2.2 %)** /
stable-but-stressed **35,170.4 km2 (10.5 %)** / stable-not-stressed **172,508.7 km2 (51.6 %)** /
**increasing 112,269.1 km2 (33.6 %)** / no data 0.4 %.
So ~14.4 % of Colombian pasture is stressed-or-worse and ~85 % is stable-unstressed or improving.
Same report, section 5.1, lists *sobrepastoreo* among the direct causes of land degradation but
does not quantify it. Caveat I am recording: LPD is an NDVI-productivity indicator, not a
ground-cover measurement, and a productivity rise can come from fertiliser or improved grasses.

**CONDITION evidence 3 — the pasture-condition split MEASURED inside the Magdalena basin.**
Consorcio POMCAS Oriente Antioqueno (2016), *POMCA rio Nare, Fase Diagnostico, 4.11 Cobertura y
uso de la tierra* (CORNARE), Corine Land Cover Colombia, basin 94,353.7 ha, a direct Magdalena
tributary. **2011** (Tabla 211 / Anexo 4.11.9.5.2): Pastos limpios (231) 38,039.83 ha = 40.24 % /
Pastos enmalezados (233) 5,338.43 ha = 5.65 % / Pastos arbolados (232) 75.94 ha = 0.08 % /
Areas erosionadas (3331) 76.42 ha = 0.08 %. **Within the pasture classes: 87.5 % limpios,
12.3 % enmalezados, 0.2 % arbolados.** For contrast, 1986 (Tabla 210): limpios 21.57 %,
enmalezados 9.64 % -> 69 % / 31 %. Forest in the same 2011 table is dominated by *secondary and
open* stands, not dense forest: bosque abierto alto 10.73 %, vegetacion secundaria alta 10.58 %,
vegetacion secundaria baja 7.54 %, bosque fragmentado c/ veg. secundaria 1.90 %, versus bosque
denso alto only 5.91 %.

**CONDITION evidence 4 (secondary).** CIAT (1999, 2005), as cited in the *Rehabilitacion de
praderas degradadas en el tropico de Mexico* review (Rev. Mex. Cienc. Pecu.): ~60 % of tropical
America's ~400 Mha of pasture is degraded. Flagged SECONDARY — I could not read CIAT directly, and
"degraded" there is an agronomic-productivity term, not a ground-cover term.

### Step 5 — a value I am REFUSING even though it would close the gap

Rengifo-Rengifo et al. (2022) give **Pastos enmalezados o enrastrojados C = 0.6**. Adopting it with
the Nare split (87.5 % limpios @ 0.01 + 12.3 % enmalezados @ 0.6) would put grassland C at approx
0.083, i.e. **x8.3**, and would close most of the SDR residual in one move. I am not adopting it,
for a physical reason that does not depend on the outcome:
- IDEAM's own legend defines 2.3.3 *Pastos enmalezados o enrastrojados* as pasture **invaded by
  weeds and secondary vegetation** through scarce management or abandonment. In (R)USLE the
  dominant subfactor is ground-contact cover (SC) — Lianes et al. (2009) p. 229 measure and state
  exactly this. Weed and rastrojo invasion *increases* ground cover, so C for enmalezado pasture
  must be **lower** than for clean pasture, not 60x higher.
- Rengifo's own P table puts *pastos enmalezados* in "Terreno edificable / Tierra baldia"
  (wasteland), which shows they read "enmalezado" as bare/derelict — a misreading of the class.
- The same table is internally inconsistent elsewhere (mosaics of crops 0.003, *below* clean
  pasture 0.01; continuous urban fabric 0.001; rock outcrop 0.25 but "tierras desnudas" 1.0).
So the single largest available upward lever is rejected on physics, and it is rejected *before*
I compute anything. This is the one decision in this task that the honesty gate exists for.

### Step 6 — CHOSEN VALUES, RECORDED BEFORE ANY EFFECT IS COMPUTED

I have not yet run the area-weighting with these numbers. I am writing them down first,
deliberately, so the record shows the choice was made from the evidence and not from the
answer it produces. **I have not computed the basin total for these values yet.**

| class | low | **central** | high | why the central is what it is |
|---|---|---|---|---|
| 1 Forest | 0.001 | **0.005** | 0.037 | Nare CLC 2011 shows the basin's tree cover is mostly secondary/open, not closed: central = Saborio/Gomez/CATIE "bosque claro, subestrato herbaceo denso" 0.003-0.010 mid, = Dymond (2010) Forest 0.005 in Benavidez Tab. 8. Low = Roose/Morgan closed canopy 0.001; high = Lianes' field-measured *bosque degradado* 0.037. |
| 2 Shrub | 0.003 | **0.015** | 0.10 | Saborio/Gomez/CATIE *Matorral denso* 0.003-0.030 (central = its mid); high = *Matorral claro, subestrato herbaceo degradado* 0.030-0.100. Replaces an uncited ASSUMED 0.005. 0.12 % of area — immaterial either way. |
| 3 Grassland | 0.008 | **0.015** | 0.10 | See the paragraph below. |
| 4 Cropland | 0.08 | **0.20** | 0.495 | Low = all-perennial mosaic (FAO 1989 Cafe 0.09 / Marchamalo 0.080); central unchanged at 0.20, the top of *cultivos permanentes asociados (densos)* 0.010-0.300 and the bottom of *no densos* 0.100-0.450; high = FAO 1989 *Cultivos anuales* 0.495. |
| 5 Urban | 0.0 | **0.03** | 0.20 | Now cited instead of ASSUMED: Benavidez Tab. 8 Urban = 0 (Dumas 2009; LDD 2002), 0.03 (Fernandez et al. 2003), 0.2 (David 1988). Central = Fernandez 0.03. 0.30 % of area. |
| 6 Bare | 0.25 | **0.50** | 1.00 | The class is measured to be rock/ash/ice above the treeline, NOT clean-tilled fallow (docs/37 section 3 gate (a) asked for exactly this fix). Rengifo (Colombia) gives *Afloramientos rocosos* 0.25 and *Zonas glaciares y nivales* 0.25; W&S 1978 / Roose / Benavidez give bare soil 1.00. Central 0.50 = geometric mean of the two cited endpoints sqrt(0.25 x 1.00), because the class is a mixture of bare rock and ice (cited 0.25) and loose, genuinely detachable volcanic ash in the Los Nevados / Purace cells (cited 1.00). This is an interpolation and is labelled as one. |
| 7 Water | 0.0 | **0.0** | 0.001 | Definitional; high = Rengifo *Rios / Lagunas* 0.001. |
| 8 Wetland | 0.001 | **0.005** | 0.010 | Low = Roose "dense cover" 0.001; high = Rengifo (Colombia) *Herbazal* 0.010; central = midpoint, labelled as an interpolation. |

**Grassland, the decisive row — chosen central 0.015 (was 0.010), range 0.008-0.10.**
The class is *grazed cattle pasture*, so Roose's label "savanna and prairie in good condition" was
the wrong label even if the number was close. But the evidence does NOT support moving it to the
degraded end, and it is worth being explicit that four independent lines converge low:
Rengifo-Rengifo et al. (2022) *Pastos limpios* (Colombia, Cauca) **0.01**; FAO 1989 *Pasto* 0.009
and *Pasto natural o mejorado* 0.008; ICE 1999 *Pasto* **0.01-0.015**; Marchamalo 2004/2007 *Pasto*
0.013; and Lianes et al. (2009) FIELD-MEASURED tropical-highland cattle pasture 0.002 (normal
stocking), 0.002 (degraded) and 0.016 (very degraded). The high tabulated band
(*Pastizal natural pastoreado* 0.040-0.200; Roose overgrazed/burnt 0.1; Morgan 2005 pasture 0.1)
is for **natural rangeland under grazing** with incomplete cover — a semi-arid situation. The
Magdalena's grassland is humid-tropical *sown* pasture (Brachiaria/kikuyu, CLC *pastos limpios*),
which is the *Pastizal cultivado (manejado)* row, **0.003-0.040**.
I choose the TOP of the converging low band, 0.015, rather than 0.010, for three reasons that are
each cited: 77 % of Colombia's livestock land carries some erosion and 74 % of the Magdalena-Cauca
is affected (IDEAM 2015); ~14.4 % of Colombian pasture is stressed or declining (LDN 2018
Tabla 12); and Lianes' *measured* value for very degraded tropical pasture is 0.016. 0.015 is
simultaneously the top of ICE 1999's band and just under Lianes' measured degraded value, so it is
a cited number, not a nudge.
**I am stating in advance that this is a x1.5 change on the dominant term and therefore CANNOT
close a 1.93-14.8x residual. The evidence does not support the value that would.** Recording that
here, before the arithmetic, is the point.

**P — chosen 1.0 for every class (unchanged), range: low = the land-use-keyed Rengifo/Pacheco
values, high = 1.0.**
1. Wischmeier & Smith (1978) define P only for *support practices* (contouring, strip-cropping,
   terracing) and set P = 1.0 for up-and-down-slope tillage / no practice. No conservation-practice
   layer exists for the Magdalena-Cauca, so 1.0 is the definitional value, not a lazy default.
2. The only citable sub-1 scheme I found is Rengifo-Rengifo et al. (2022) Cuadro 5 after Pacheco
   et al. (2019): Area arbolada 0.1 / Tierra agricola 0.4 / Cuerpos de agua 0.5 / Terreno
   edificable-baldio 1.0. It is keyed on LAND USE, not on any mapped practice, so it double-counts
   the cover effect that C already carries — a category error. Note that even in that scheme
   **both pasture classes keep P = 1.0**, so it would not touch 39.9 % of this basin.
3. Empirical check that P approx 1 basin-wide is *right* and not merely conservative:
   MADS/IDEAM/UNCCD (2018) sets national 2030 targets of **9,000 ha** of pasture converted to
   silvopastoral systems and **100,000 ha** of degraded land restored nationally, against
   **414,505 km2 (41.45 Mha)** of national pasture — i.e. adopted conservation practice is of order
   0.02-0.24 % of the pasture area. FEDEGAN's *Ganaderia Colombiana Sostenible* project reports
   50,500 ha converted.
4. **Direction, stated per docs/37 residual 4:** any P < 1 *lowers* modelled erosion and *widens*
   the SDR residual. Applying the Rengifo/Pacheco P column would push the model further from the
   asserted SDR band, not closer. That P = 1.0 happens to be the erosion-maximising choice is a
   reason to hold it to the definitional justification above, which it meets, and to keep flagging
   the level as an upper bound in the practice term.

### Step 7 — EXACT erosion weights (the yardstick the prior journal got wrong)

The engine is `Sed_mini(t) = term(t,mini) * sum_cells[(A/a_p)*alpha*K*C*P*LS2D*FG]`, so the basin
total is **exactly linear in C** and decomposes as `sum_c W_c * C_c`. I computed W_c on the frozen
drivers (`h2e_drivers.npz:qsur_rel_mm`, the registered Qsur per docs/35 s1) as
`cell_static_factor` on a geometry with `cell_c` replaced by ones, times the time-integrated
`runoff_energy_term`. Cross-checked against one full engine run: **relative difference 1.917e-16**,
and the decomposition reproduces the published headline exactly:
2,486.957417 Mt / (3652 d / 365.25) = **248.729791 Mt/yr** = the documented 248.73.

| class | area % | C_prior | erosion share % | area-weighted-C share % | W_c (Mt/decade per unit C) |
|---|---:|---:|---:|---:|---:|
| Forest | 55.774 | 0.003 | **36.4836** | 15.4597 | 302,443.49 |
| Bare | 0.196 | 1.0 | **35.5983** | 18.1330 | 885.32 |
| Grassland | 39.867 | 0.01 | 27.3262 | 36.8344 | 67,959.16 |
| Cropland | 1.575 | 0.2 | **0.4728** | **29.1029** | 58.80 |
| Urban | 0.297 | 0.01 | 0.0594 | 0.2745 | 147.77 |
| Shrub | 0.119 | 0.005 | 0.0582 | 0.0548 | 289.31 |
| Wetland | 1.523 | 0.001 | 0.0015 | 0.1407 | 36.50 |
| Water | 0.649 | 0 | 0 | 0 | 450.10 |

**This overturns journal_c32-cp.md step 5's sensitivity ranking.** Cropland is 29.10 % of the
area-weighted C but **0.4728 %** of actual erosion (it sits in the flat valleys where LS2D and Qsur
are small); Forest is the largest term at 36.48 %, not 15.46 %. Recorded in docs/41 s2.

### Step 8 — EFFECT (computed only after step 6 recorded the choice)

Area-weighted basin-mean C, and the exact basin total (no re-simulation needed — linearity):

| scenario | area-weighted C | ratio | basin gross erosion | ratio |
|---|---:|---:|---:|---:|
| prior | 0.010823 | 1.0000 | 248.730 Mt/yr | 1.0000 |
| low | 0.005516 | 0.5097 | **107.320 Mt/yr** | **0.4315** |
| **central (adopted)** | **0.013083** | **1.2088** | **299.539 Mt/yr** | **1.2043** |
| high | 0.071133 | 6.5723 | **1896.264 Mt/yr** | **7.6238** |

One-at-a-time prior -> central / high: Forest x1.2432 / x5.1348 · Grassland x1.1366 / x3.4594 ·
**Bare x0.8220 / x1.0000** · Urban x1.0012 / x1.0113 · Shrub x1.0012 / x1.0111 ·
Cropland x1.0000 / x1.0070 · Wetland x1.0001 / x1.0001 · Water x1.0000 / x1.0002.
So the x1.20 central is a NET: Forest and Grassland pull up, and the largest single revision in the
table (Bare 1.0 -> 0.5) pulls DOWN by x0.822.

Rejected-value arithmetic, computed after the rejection was written (step 5): grassland 0.0826 gives
**742.181 Mt/yr, x2.9839**. It would indeed have closed most of the residual. It stays rejected.

P sensitivity, NOT adopted: Rengifo/Pacheco land-use-keyed P gives 248.730 -> 166.264 (x0.6685) on
the prior C and 299.539 -> 162.443 (**x0.5423**) on the revised C. Confirms docs/37 residual 4's
direction quantitatively: P < 1 lowers the model and widens the residual.

SDR arithmetic (docs/37 back-implies an observed outlet load of ~144-184 Mt/yr from its
0.579-0.740 at 248.73): low -> **1.34-1.72**, prior 0.579-0.740, central -> **0.481-0.614**,
high -> **0.076-0.097**. The LOW end of the C range is REFUTED by mass balance (SDR > 1 is
impossible) — that is the only gate I applied. The asserted 0.05-0.30 band is **UNCITED** in this
repo (docs/37 residual 3), so per the run constraint it is used to pass nor fail nothing here.

### Step 9 — files written and verified

1. **`data/processed/urh_cp_factors.csv`** rewritten, 8 rows x 20 columns, 31,086 bytes.
   Loader-facing `class_id, C, P` preserved (`C` == `C_central`); new
   `C_low/C_central/C_high`, `P_low/P_central/P_high`, `land_condition`, `source`, `note`,
   `area_pct`, `erosion_share_pct_at_prior_C`, `unit_C_weight_Mt_decade`; prior values preserved in
   `value_prior_2026_08_11`, `P_prior_2026_08_11`, `source_prior_2026_08_11`,
   `note_prior_2026_08_11` (the old source/note text is kept verbatim, nothing lost).
   Read back and asserted: 8 rows, `C == C_central` on every row, `P == 1.0` on every row,
   `C_low <= C_central <= C_high` on every row, and `land_condition`/`source`/`note` non-null and
   >40 chars on every row. Prior file backed up to the scratchpad
   (`urh_cp_factors_PRIOR_backup.csv`).
   End-to-end verify: `load_geometry` + `simulate_sediment(SedParams(), qsur_rel_mm)` returns
   2,994.977042 Mt / 3652 d = **299.5387 Mt/yr** vs 299.539 predicted, ledger
   `residual_t = 0.0, exact: True`.
2. **`docs/41_cfactor_evidence.md`** written (10 sections: what changed; the area-weight error; the
   evidence by source with full citations; per-class reasoning; P; grassland + the refusal; the
   effect as a range + SDR arithmetic; consequences for the caller; residuals; reproduction).
3. **This journal.**

### Step 10 — test suite: 2 FAILURES, both stale hard-coded C in tests/ (NOT my file)

`python3.10 -m pytest tests/test_sediment.py -q` -> **48 passed, 2 failed** (was 50/50).
Both are provenance staleness, not defects:
- `test_real_geometry_shape_and_ranges`, lines 683-684: asserts the unique C set is a subset of
  `{0.003, 0.005, 0.01, 0.2, 1.0, 0.0, 0.001}`; the new set is
  `{0.0, 0.001, 0.005, 0.015, 0.03, 0.2, 0.5}` (extras 0.015, 0.03, 0.5).
- `test_audit_unit_day_reproduces_from_the_real_files`, line 310:
  `assert abs(g.cell_c[j] - 0.003) < 1e-12` -> now 0.005, so the load it then checks against
  `UNIT_DAY_LOAD_T` must become **2155.9486044749287** (= 1293.5691626849571 x 0.005/0.003) for the
  FILE-BASED guard only.
- The synthetic s3b regression `test_...` at ~line 245 passes `class_c={1: 0.003}` explicitly and
  **still passes** — leave it alone, it is a convention-arithmetic regression, not a CSV claim.
- `test_dry_and_inert_cells_are_exactly_zero_on_real_data` passes and constrains this table
  permanently: Water must stay exactly 0.0.
I did not touch tests/. Reported in docs/41 s8.1.

### Step 11 — honesty-gate attestation

I recorded the chosen central value for every class, and the grassland reasoning in full, in
**step 6 of this journal, before computing any effect on the basin total** — and I recorded the
refusal of the one value that would have closed the SDR gap (Rengifo's *pastos enmalezados* 0.6) in
**step 5, also before computing its effect**. Step 8 is the first place in this file where a basin
total appears for the revised values. I wrote in step 6, in advance, that a x1.5 grassland change
cannot close a 1.93-14.8x residual, and that is what the arithmetic then showed: **x1.20 net**.
The evidence supports staying essentially where the table was on grassland (0.010 -> 0.015, a label
correction more than a value correction), and the largest single revision I made (Bare 1.0 -> 0.50)
moves the model in the *unhelpful* direction. docs/37 residual 1 is closed on its own terms — C is
now cited, condition-stated and ranged — and the SDR clause is left open, because residual 3's band
is still uncited and nothing here can decide it.

### Checklist — final

- [x] 1. Read `urh_cp_factors.csv` and `journal_c32-cp.md`
- [x] 2. Read docs/37 residuals 1, 3, 4
- [x] 3. Area weights recomputed from `parameters.npz` + `topology.npz`
- [x] 4. Literature: (a) Rengifo-Rengifo et al. 2022 (Cauca, in-basin);
      (b) Lianes et al. 2009 + FAO 1989 / ICE 1999 / Saborio-Gomez-CATIE / Marchamalo / Mora 1987;
      (c) Benavidez et al. 2018 (= MGB-SED's own cited C source) + Roose already in file
- [x] 5. Pasture-CONDITION evidence: Nare POMCA in-basin CLC split (87.5/12.3/0.2),
      IDEAM 2015 erosion (40 % national, 74 % of the Magdalena-Cauca, 77 % of livestock land),
      LDN 2018 Tabla 12 productivity dynamics (14.4 % stressed-or-worse), CIAT via secondary
- [x] 6. P: no defensible basin-wide P < 1; direction (lowers erosion, widens residual) measured
      at x0.5423 and stated
- [x] 7. CHOICE RECORDED BEFORE EFFECT (step 6 precedes step 8)
- [x] 8. Table revised with source + condition + low/central/high + prior values preserved
- [x] 9. Basin-mean C and the exact basin total for low/central/high, as a range
- [x] 10. `docs/41_cfactor_evidence.md` written

### Step 12 — cross-reference to the parallel run (docs/40)

A sibling run settled docs/37 residual 3 in `docs/40_sdr_evidence.md`: the 0.05-0.30 SDR band is
**UNCITABLE** (the published SDR-area relations measure gross erosion INCLUDING gullies, banks and
channels, at ~3 orders of magnitude smaller scale, so they are a different quantity from a
hillslope-only MUSLE sum), and it replaces the SDR clause with a gross-erosion-rate test that puts
the residual at **1.59-2.74x** on the erosion side. Added a cross-reference section to docs/41 s7 so
the two documents do not contradict each other, with the arithmetic against that replacement target
(395.5-681.5 Mt/yr): prior short by x1.59-2.74, **central still short by x1.32-2.27**, high
overshoots by x2.78-4.79. Stated explicitly there that an intermediate C inside this table's own
low-high range would land inside the target and that it is NOT adopted, because choosing C to hit a
residual is exactly the failure mode this run exists to avoid (and is what docs/35 s6 RULE 0
forbids for alpha). docs/40 independently says its remaining gap "lands inside the 2-5x that
docs/37 s4 candidate 1 (the cover factor C) already estimated for itself"; this run is the
measurement of how much of that 2-5x the evidence supports, and the answer is **x1.20, not 2-5**.
