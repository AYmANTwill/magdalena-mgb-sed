# 40 — The sediment delivery ratio band: **UNCITABLE**, and the test that replaces it

**Written 2026-08-11.** Settles residual 3 of [`docs/37`](37_c3_closure.md) §4 — the only clause on
which C3's closure still hangs. `docs/37` withheld closure because the implied sediment delivery
ratio, **0.579 – 0.740**, sat above an asserted plausibility band of **0.05 – 0.30**, and it
recorded that the band "arrived as a brief-level assertion, exactly like the *mountainous LS 2–10*
comparison that decision 4 retired."

**Verdict: UNCITABLE.** Not because the *number* 0.05–0.30 is unfindable — it is approximately
reproducible from three published relations (§3) — but because those relations measure a
**different quantity** from the one we computed (§2, §5), were fitted about three orders of
magnitude below this basin's scale on US agricultural land (§3.2), and are accompanied by their own
source's explicit prohibition on out-of-domain use (§3.3). For the Magdalena itself **no sediment
delivery ratio has ever been published**, and none can be constructed from the literature, because
every Magdalena "erosion rate" in print is a sediment *yield* — the SDR numerator — never the
denominator (§4.2). A gate comparing two different quantities can neither pass nor fail.

So the SDR test is **retired as a gate**. §8 proposes the exact replacement wording for `docs/37`'s
third closure clause: a **gross-erosion-rate** test, which *can* be evaluated, has three
independent citable legs, and **fails in the same direction on all three** — quantifying the
residual at **1.59 – 2.74×** on the erosion side. That is far tighter than `docs/37`'s
1.93 – 14.8×, and it lands inside the 2–5× that `docs/37` §4 candidate 1 (the cover factor `C`)
already estimated for itself. The residual is real; it is just not an SDR problem.

> **AMENDED 2026-08-11 — read §0 before quoting the sentence above.** The replacement clause's
> decisive leg turned out to repeat the same quantity error on the erosion side: it compares our
> MUSLE sum against a **RUSLE gross erosion**, while SWAT's own documentation of this exact equation
> defines its output as a sediment **yield**. Under that reading the sign inverts, and Leg C's
> max-yield form is invalid at basin scale in either reading. **"Fails in the same direction on all
> three" is superseded: the residual's direction is UNKNOWN**, spanning 2.27× too low to 1.49× too
> high. C3 stays OPEN regardless, on `docs/37` A1.1 clauses 2 and 3.

---

## 0. AMENDMENT, 2026-08-11 — **which quantity is the MUSLE sum?** The replacement clause's decisive leg is not like-for-like either

*Added after the rest of this document was written, by `docs/agents/journal_fixer.md` run 3, because
the §7/§8.2 replacement clause repeats — on the erosion side — the exact error it was built to fix
on the delivery-ratio side: it compares two different quantities. Nothing below this section is
rewritten. The three legs are re-derived under both readings, at the adopted `C`, in
[`docs/37`](37_c3_closure.md) **A1.9**; this section pins the definitional question they turn on.*

### 0.1 The reference implementation of this exact equation calls its output a sediment **yield**

**SWAT Theoretical Documentation, Version 2009**, Section 4 Chapter 1, *"Equations: Sediment"*,
printed p. 252 — the reference implementation of the same MUSLE with the same α = 11.8, β = 0.56 and
`CFRG`, and (per `docs/agents/journal_decide-units.md` §1d) the text Buarque (2015) and
Fagundes (2018) transcribe their unit strings from. Retrieved and text-extracted for this section
(7,690,470 B, 647 pp). **Verbatim:**

> "USLE predicts average annual gross erosion as a function of rainfall energy. In MUSLE, the
> rainfall energy factor is replaced with a runoff factor. This improves the sediment yield
> prediction, **eliminates the need for delivery ratios**, and allows the equation to be applied to
> individual storm events. … **Delivery ratios** (the sediment yield at any point along the channel
> divided by the source erosion above that point) **are required by the USLE because the rainfall
> factor represents energy used in detachment only. Delivery ratios are not needed with MUSLE
> because the runoff factor represents energy used in detaching *and transporting* sediment.**"

and, defining the left-hand side of eq. 4:1.1.1 on the same page:

> "where **`sed` is the sediment yield on a given day** (metric tons), `Qsurf` is the surface runoff
> volume (mm H₂O/ha), `qpeak` is the peak runoff rate (m³/s), `areahru` is the area of the HRU (ha)"

`notebooks/18_musle_construction.ipynb` §1 states the same thing in its own words and warns that it
matters: *"MUSLE's output is closer to 'sediment delivered from this patch to its stream' than to
'soil detached on this patch'. Section 6 shows this distinction is not pedantic — a whole closure
gate was retired over it."*

### 0.2 What that does to §7

**RUSLE is USLE's descendant, so a RUSLE rate is a detachment-side quantity — a gross erosion.**
§7 Leg A compares our MUSLE sum against Tan, Liu & Lu (2024)'s **RUSLE** 23.7–26.5 t ha⁻¹ a⁻¹ and
calls it *"the only like-for-like denominator"*; `nb18` §6.4 goes further — *"Hillslope against
hillslope, so this is the leg that counts."* Under §0.1 that is **yield against gross erosion**, the
same category of comparison §2 retired the SDR gate over. The label used throughout this document —
*"gross hillslope erosion, MUSLE"* (§1, §7, §8.2, §11) — is an **assumption stated as a definition**,
and it is the assumption on which the residual's *direction* depends.

Put Tan's gross erosion on our side of the line using **NEH Table 6-2's own sheet-erosion delivery
ratio of 0.33** (§2.3's table: 300,000/900,000) and it becomes **7.821 – 8.745 t ha⁻¹ a⁻¹** as a
hillslope *yield*. Ours at the adopted `C` is **11.6508 t ha⁻¹ a⁻¹** — **1.332 – 1.490× above**, not
2.034 – 2.275× below. **The sign inverts.** A second, conversion-free check points the same way:
Tan et al.'s own reported specific sediment **yield** is 1.3 – 16.9 t ha⁻¹ a⁻¹, and ours sits
**inside** it.

The other two legs cannot carry the clause either:

- **Leg B** is conceded in `docs/37` A1.4 to have *"stopped being a proof … it is no longer
  evidence"* — the gap is 2.8 % (1.027×), inside the noise of a comparison this document itself
  labels order-of-magnitude.
- **Leg C's shortfall form is invalid at basin scale, under either reading.** It compares our basin
  **mean** over 257,097 km² against the **maximum** of 32 sub-basins of 320 – 59,600 km². A
  spatially variable field's mean is *arithmetically required* to lie below its own maximum: this
  model's own internal range is **18.671×** (Andean flanks 1,445.32 vs lowland floodplain 77.41
  t km⁻² yr⁻¹, `docs/37` A1.3.3). So "0.530× the maximum measured yield" is not evidence of
  under-erosion; it is evidence that a mean is not a maximum. **The max-yield form is dropped.**
  Leg C's *mean* form survives and is a **yield-vs-yield** test: 1,165.08 vs ~690 t km⁻² yr⁻¹,
  i.e. **1.689× above** — which under the yield reading is the *expected* direction.

### 0.3 What this section concludes, and what it deliberately does not

**It does not flip the verdict, and it does not adopt the yield reading.** The yield reading makes
the adopted result look better, which is exactly the reason to hold it at arm's length; and it has a
real counter-argument, recorded here rather than buried: MUSLE was fitted to sediment yields measured
at the **outlets of 18 small watersheds**, whereas this project applies it **per 90 m DEM pixel and
sums 30 million pixels**. A per-pixel sum over 257,097 km² is therefore not a basin sediment yield
either — every pixel is credited with delivering to a stream it may be 100 km from. Our sum is a
transposition of a small-watershed regression, and the honest statement is that it is **neither
exactly gross erosion nor exactly a basin yield**.

**Therefore: the residual's direction is UNKNOWN**, spanning **2.27× too low** (erosion reading) to
**1.49× too high** (yield reading), and clause 4′ is **NOT ESTABLISHED** rather than NOT MET. C3
stays **OPEN** either way — `docs/37` A1.1 clauses 2 (the LS formulation level, UNRESOLVED) and 3
(the 2026-08-11 decisions unaudited) each forbid closure on their own, and this section removes a
*reason*, not the verdict. **`docs/42` G5 keeps its force and gains a number:** under the yield
reading the α that reproduces Tan's converted level is **7.92 – 8.86**, which overlaps G5's
deposition-free fit band of **6.83 – 8.73** — so a fit that "works" under the yield reading is
nearly indistinguishable from one silently asserting SDR = 1.0 between hillslope and station. **C4
must not fit α against clause 4′ until §0 is settled.**

### 0.4 The reading that the retired ratio may have been telling us something true

If the MUSLE sum is a hillslope-to-stream **yield**, then `outlet load ÷ MUSLE sum` is not a
delivery ratio at all — it is a **channel-and-floodplain throughput**, and its complement is transit
loss. Measured, both levels:

| | ratio 144 Mt/yr | ratio 184 Mt/yr | implied transit loss |
|---|---:|---:|---|
| at the prior `C` (248.7298 Mt/yr) | 0.5789 | 0.7398 | **26.0 – 42.1 %** |
| at the adopted `C` (299.5387 Mt/yr) | 0.4807 | 0.6143 | **38.6 – 51.9 %** |

The prior-`C` figure sits inside **C11**'s primary-verified Depresión Momposina retention of
**20 – 45 %** (36 – 80 Mt/yr, labelled *preliminar* by its own author). That agreement is real and it
is worth putting to the advisor — the number this project retired as an implausible SDR is, under the
yield reading, an ordinary transit loss. **But it is a prior-`C` agreement and must not be quoted as
current:** at the adopted `C` the required loss is 38.6 – 51.9 %, *above* the Momposina band, so the
Momposina alone no longer accounts for it. Decomposed: total transit loss 155.54 Mt/yr (low anchor)
or 115.54 Mt/yr (high anchor), of which M9's Momposina takes 36 – 80; the remainder for **every other
sink** is 75.5 – 119.5 Mt/yr (25.2 – 39.9 % of the hillslope yield) at the low anchor and
35.5 – 79.5 Mt/yr (11.9 – 26.6 %) at the high one. Physically open, not physically closed.

---

## 1. What is being tested, and with which numbers

| quantity | value | provenance |
|---|---|---|
| gross **hillslope** erosion, MUSLE, basin decade 2009–2018 | **248.730 Mt/yr** | `docs/37` §2; `src/mgb_sediment.py`, adopted conventions |
| — as a basin-mean rate over 257,097 km² | **967.46 t/km²/yr = 9.675 t/ha/yr** | computed here |
| outlet anchor, low | **144 Mt/yr** (Calamar, 1975–1995) | Restrepo & Kjerfve (2000), verified in `docs/34` §5.1 |
| outlet anchor, high | **184 Mt/yr** (1980–2010) | Restrepo & Escobar (2018), verified in `docs/34` §5.1 |
| implied ratio | **144/248.730 = 0.5789** · **184/248.730 = 0.7397** | `docs/37` §2 |
| asserted comparison band | **0.05 – 0.30** | **no citation in this repository** — the thing this document settles |

MUSLE in `src/mgb_sediment.py` represents **sheet and rill erosion on hillslopes only**. There is
no gully term, no channel-bank term, no landslide term, no mining term. This is not a defect
peculiar to this implementation — it is what the (M)USLE family is, and it is the fact that decides
the verdict.

---

## 2. Definitions pinned first, because the answer depends entirely on them

### 2.1 SDR as the literature defines it — the denominator is *all* erosion

The authoritative operational definition is USDA's, because the SDR-versus-area relations in §3 are
USDA-derived. From the **USDA NRCS National Engineering Handbook, Part 632, Chapter 6, "Sediment
Sources, Yields, and Delivery Ratios"**, in the *Sediment Yield* introduction (verbatim, from the
scanned chapter text):

> "Sediment yield is the gross (total) erosion minus the sediment deposited en route to the point
> of concern. **Gross erosion is the sum of all the water erosion occurring in the drainage area.
> It includes sheet and rill erosion plus channel-type erosion (gullies, valley trenches,
> streambank erosion, etc.)**"

and, under *Methods of Determination*:

> "Y = E(DR) … Y = annual sediment yield (tons/unit area). E = annual **gross erosion**
> (tons/unit area). DR = sediment delivery ratio (less than 1). The gross (total) erosion in a
> drainage area is **the sum of all the water erosion taking place**."

A published SDR is therefore **`sediment yield at the point of interest / total erosion from every
water-erosion process in the contributing area`**. Its denominator is strictly larger than a
hillslope-only denominator, so a published SDR is strictly smaller than the same basin's
hillslope-only ratio. Any comparison that ignores this is biased in a known direction.

### 2.2 What our two numbers actually are

- **Numerator, 144–184 Mt/yr:** total suspended load past Calamar. It contains sediment from
  *every* source — hillslopes, gullies, banks, landslides, mining — and it is net of *all*
  deposition upstream of Calamar, including the Depresión Momposina (§5.2).
- **Denominator, 248.730 Mt/yr:** hillslope sheet-and-rill erosion only.

### 2.3 Therefore the quantity we computed is **not** an SDR

It is a mixed ratio — call it the **apparent delivery ratio (ADR)** — with an all-source numerator
over a hillslope-only denominator. Two consequences, both fatal to the gate as written:

1. **The ADR is not bounded by 1.** `docs/37` §2 argued "`SDR = outlet / gross` must be < 1". That
   is true of a true SDR and false of the ADR: whenever non-hillslope sources supply more than
   in-transit deposition removes, the ADR exceeds 1.
2. **The reference literature's own worked example gives ADR = 1.78.** NEH Ch. 6 Table 6-2
   ("Sediment source and the delivery ratio") is USDA's illustration of source-texture analysis:

   | source | erosion (t/yr) | sediment yield (t/yr) | delivery ratio |
   |---|---:|---:|---:|
   | Sheet erosion | 900,000 | 300,000 | **33 %** |
   | Gullies | 350,000 | 280,000 | 80 % |
   | Roadbanks | 150,000 | 120,000 | 80 % |
   | Streambanks | 900,000 | 900,000 | 100 % |
   | **Total** | **2,300,000** | **1,600,000** | **70 %** |

   In this single watershed: the **true SDR is 0.6957**; the **hillslope-only delivery ratio is
   0.33**; sheet erosion is only **900,000/2,300,000 = 39.13 %** of gross erosion; and the **ADR —
   the exact quantity we computed — is 1,600,000/900,000 = 1.7778**.

   Our 0.579–0.740 is **below**, not above, the ADR of USDA's own reference example, and it is
   almost exactly equal to that example's *true* SDR of 0.70. Read either way, the direction of the
   alleged failure inverts.

This is the single most important line in this document: **`docs/37`'s third clause compares an ADR
against an SDR band.** It was never an evaluable test.

---

## 3. Task 1 — what is actually published for large basins, and what it predicts here

### 3.1 The classic area-decay relations, evaluated at A = 257,097 km² (= 99,265.7 mi²)

| relation | form | source data | value at our A |
|---|---|---|---:|
| **Vanoni (1975)**, ASCE Manual 54 | `SDR = 0.42 · A^(−0.125)`, A in mi² | "300 watersheds throughout the world" | **0.0997** |
| **USDA-SCS (1979)** | `SDR = 0.51 · A^(−0.11)`, A in mi² | Blackland Prairie, Texas | **0.1439** |
| **Renfro (1975)** | `log SDR[%] = 1.7935 − 0.14191 · log A`, A in km², R² = 0.92 | **14 watersheds**, Blackland Prairie, Texas | **0.1061** |
| **USDA NEH Ch. 6, fig. 6-2** | SDR "vary inversely as the **0.2 power** of the size of the drainage area" | Gottschalk & Brune 1950; Woodburn & Roehl; Maner & Barnes 1953; Glymph 1954; Maner 1957; Roehl 1962 | curve does not reach our A (§3.2) |
| **Walling (1983)** | area exponent reported in the range **−0.01 to −0.25** *(secondary attribution — see §9)* | compilation | — |

So the asserted 0.05–0.30 band is **not fabricated**: three independent relations land at
0.10–0.14, comfortably inside it. To that extent the band is traceable. Everything that follows is
about whether it is *applicable*.

### 3.2 These relations were never calibrated on basins remotely this large, or on tropical mountains

- NEH Ch. 6 **figure 6-2**, the figure the whole US SDR practice rests on, has a drainage-area axis
  spanning **0.01 to 100 square miles = 0.0259 to 259.0 km²**. Our basin is
  **257,097 / 259.0 = 992.7×** the largest watershed in that figure. The relation is being asked
  to extrapolate three orders of magnitude.
- **Renfro (1975)** is **14 watersheds** in one Texas physiographic province.
- **USDA-SCS (1979)** is the same province.
- **Vanoni (1975)**'s 300 watersheds are described as worldwide, but the area range of that sample
  is **not established in this document** (§9) — it must not be assumed to reach 10⁵ km².
- None of these datasets is described as containing a humid tropical Andean catchment.
- NEH fig. 6-2 itself is reported as showing "a **wide variation** in the sediment delivery ratio
  for any given size of drainage area"; the plotted band is a range, and the line quoted is its
  **median**.

### 3.3 The sources forbid this use, in their own words

NEH Ch. 6, *Summary*:

> "**Using an equation to obtain sediment data outside the physiographic area for which the
> equation was developed is generally not recommended.**"

and, on the area relation specifically:

> "Rough estimates of the sediment delivery ratio can be made from figure 6-2, but any such
> estimate should be **tempered with judgment**, and other factors such as texture, relief, type of
> erosion, sediment transport system, and **areas of deposition within the drainage area** should be
> considered."

### 3.4 The modern literature has retired the generality of the relation

- **de Vente, Poesen, Arabkhedri & Verstraeten (2007)**, *Progress in Physical Geography*
  31(2):155–178, abstract, verbatim: area-specific sediment yield "is often **assumed** to decrease
  with increasing drainage basin area (A) … However, over the last two decades **several studies
  reported a positive or non-linear relation** between A and SSY." And, decisively for a basin like
  ours: "**land-cover conditions and human impact determine if hillslope erosion is dominant over
  channel erosion or vice versa.** In the first case, SSY is expected to decrease with increasing
  A, while in the latter case **SSY will show a continuous positive relation with A**. Only for very
  large areas (A > ~10⁴ km²) a decrease in SSY is observed **when drainage density decreases or
  channel banks are stabilized**."
  The Magdalena–Cauca has high drainage density and unstabilized banks, so the one condition under
  which the decay is stated to hold at >10⁴ km² is the condition this basin does not meet.
- **Parsons, Wainwright, Brazier & Powell (2006)**, *Earth Surface Processes and Landforms*
  31(10):1325–1328, is titled **"Is sediment delivery a fallacy?"** — the concept's status as a
  transferable constant is contested in the primary literature, not merely by us.

### 3.5 The closest genuine modern analogue points the *other* way

**Tan, Liu & Lu (2024)**, *ESPL* 49:1778–1795 — *"Predicting soil erosion and sediment delivery in
large, data-sparse, mountainous basins"* — is the best available comparator: large, data-sparse,
mountainous, and with a **RUSLE (hillslope) gross-erosion denominator**, which is the same kind of
denominator as ours. From its abstract, verbatim:

- basin-average erosion rates "decreased from **26.5 to 23.7 t ha⁻¹ a⁻¹**", with hotspots
  >50 t ha⁻¹ a⁻¹ on 21.1 % of area contributing 69.5 % of gross erosion;
- "regionalised **SDRs ranging from 0.07 to 0.38 for 39 subbasins**, about 30 % of which were no
  less than 0.35";
- specific sediment yield 1.3–16.9 t ha⁻¹ a⁻¹;
- the optimal SDR predictors were Specific Catchment Area, Maximum Elevation and Drainage Area, and
  "**these three variables all had a positive correlation with SDR**", the model explaining 86 % of
  SDR variance.

Two things follow. First, their 0.07–0.38 is a **subbasin-scale** band (39 subbasins of a lower-reach
catchment on the order of 10⁴–10⁵ km²), not a basin-scale one. Second, and more important, in the
one large mountainous basin where SDR was actually fitted, **SDR increases with drainage area** —
so extrapolating their relation to 257,097 km² would predict an SDR **above 0.38**, not below 0.30.
The classic decay's sign does not survive contact with steep terrain at scale.

---

## 4. Task 2 — Magdalena-specific evidence, which outranks any generic relation

### 4.1 Everything published, with measurement point and window

| # | source | number | measurement point | window |
|---|---|---|---|---|
| M1 | Restrepo & Kjerfve (2000), *J. Hydrol.* 235:137–149 | **144 Mt/yr** suspended load | **Calamar**, 112 km from the Caribbean | 1975–1995 |
| M2 | Restrepo & Escobar (2018), *Geomorphology* 302:76–91 | **184 Mt/yr** suspended load | basin outlet | 1980–2010 |
| M3 | Restrepo A. (2015), *RACCEFYN* 39(151):250, doi 10.18257/raccefyn.141 | erosion rate "**550 t km⁻² a⁻¹** before 2000 → **710 t km⁻² a⁻¹** in 2000–2010", **+34 %**, load **+44 Mt a⁻¹** | basin, from gauged load / BQART | pre-2000 vs 2000–2010 |
| M4 | Restrepo A. (2015), same | "**690 ton km⁻² año⁻¹**, valor estimado en la **estación de Calamar** en el 2000" — highest on the continent vs Amazon **167**, Orinoco **158**, Paraná **43**, São Francisco **10** | Calamar | 2000 |
| M5 | Restrepo A. (2015), same | "**78 %** de la cuenca se encuentra en estado crítico de erosión"; primary-forest loss >60 % 1980–2010; **9 %** of three-decade cumulative load due to deforestation; **~160 Mt** from forest clearance 2000–2010; **16 Mt a⁻¹** from deforestation in that decade | basin | 1980–2010 |
| M6 | Restrepo, Kettner & Syvitski (2015), *Anthropocene* 10:13–28 | erosion rates **+33 %** 1972–2010, load **+44 Mt/yr**; **482 Mt** from forest clearance over three decades; **79 %** of catchment under severe erosional conditions | basin, BQART | 1972–2010 |
| M7 | Restrepo, Kjerfve, Hermelin & Restrepo (2006), *J. Hydrol.* 316:213–232 | sediment yield **128 – 2,200 t km⁻² yr⁻¹** for catchments **320 – 59,600 km²**; mean **~690 t km⁻² yr⁻¹** over **32** sub-basins; mean annual runoff explains 51 % of yield variance | 32 tributary gauges | multi-year |
| M8 | Latrubesse & Restrepo (2014), *Geomorphology* 216:225–233 | **Colombian Andes mean sediment yield 1,485 t km⁻² y⁻¹**; northern+central Andes weighted mean **2,045 t km⁻² y⁻¹** producing **2.25 Gt y⁻¹**; **119** Andean gauging stations | Andean gauges | compilation |
| M9 | Restrepo A. (2015), same as M3 | "**entre el 20 y 45 %** de los sedimentos del sistema de los ríos Magdalena-Cauca-Cesar quedan **retenidos en la Depresión** cada año, una cifra que fluctúa entre **36 y 80 millones de toneladas** anualmente" — the author labels this "una cifra **preliminar** del estudio de la Universidad Eafit y la Universidad de Colorado" | **Depresión Momposina** | annual |
| M10 | Restrepo & Syvitski (2006), *AMBIO* 35(2):65–74 | Magdalena among the world's top 10 rivers by sediment load, "approximately **150 Mt/yr**" | basin | — |

Cross-check, and it is a good one: **M3's 710 t/km²/yr × 257,097 km² = 182.54 Mt/yr**, which
independently reproduces **M2's 184 Mt/yr** anchor to 0.8 %. The outlet anchor is not the weak link.

### 4.2 The decisive negative result: no Magdalena gross erosion has ever been published

Searching the Magdalena sediment corpus for a gross-erosion estimate returns nothing. Specifically,
in Restrepo A. (2015) — the fullest Spanish-language treatment, retrieved and searched in full —
the strings `USLE` and `RUSLE` occur **zero times**. Its "tasas de erosión" are BQART-calibrated
**sediment loads** divided by area, i.e. **specific sediment yields at gauges**. The same is true of
M4 (explicitly "estimado en la estación de Calamar"), M6 (BQART), M7 (gauged yields) and M8 (gauge
compilation).

Consequence: **every Magdalena number that looks like an erosion rate is the SDR *numerator*.** The
denominator has never been measured or modelled for this basin by anyone. Therefore:

- no Magdalena SDR exists in the literature;
- no Magdalena SDR can be assembled from the literature;
- and the Magdalena literature's habit of calling outlet-derived specific yield an "erosion rate"
  is itself a trap that would let a careless reader "validate" a gross-erosion model against a
  yield. **Add to the traps register.**

---

## 5. Task 3 — the comparability audit: hillslope-to-outlet or hillslope-to-channel?

### 5.1 Which quantity each citation reports

| citation | numerator | denominator | comparable with our 248.73 Mt/yr? |
|---|---|---|---|
| Vanoni 1975 / SCS 1979 / Renfro 1975 / NEH fig. 6-2 | sediment yield at a point (reservoir surveys, gauges) | **total** gross erosion: sheet + rill + gullies + valley trenches + streambanks | **NO** — denominator mismatch, and it biases their SDR *low* relative to a hillslope-only ratio |
| NEH Ch. 6 Table 6-2 | as above, itemised | as above, itemised | **YES, as a worked reference**: gives hillslope-only DR **0.33**, true SDR **0.6957**, ADR **1.7778** |
| Tan, Liu & Lu 2024 | subbasin sediment yield | **RUSLE hillslope** gross erosion | **denominator YES**; numerator is hillslope-to-**subbasin-outlet**, above the basin's major sinks, and their SDR rises with area |
| Restrepo M1–M8, M10 | sediment **yield / load** | *none reported* | **NO** — these are numerators only |
| Restrepo M9 (Momposina) | deposition flux | — | this is the **sink term**, and it is the key to §5.2 |

So: of everything published, **not one hillslope-to-outlet SDR for a large humid tropical Andean
basin exists.** The only hillslope-denominator SDRs found anywhere (Tan et al.) are
hillslope-to-subbasin-outlet in a different climate, at ~10³–10⁴ km², with the area trend reversed.

### 5.2 The Momposina is already netted out of our anchor — and this cuts against the gate

Our anchor is measured at **Calamar**, which is **downstream** of the Depresión Momposina, the
basin's dominant floodplain sink. `docs/34` §4 already recorded that **no station in the C1 usable
set can observe this sink at all** (the outlet-most, ARRANCAPLUMAS at 54,035 km², sits above the
Cauca confluence and above the Momposina). So the 144–184 Mt/yr has the Momposina's deposition
**already subtracted**.

Adding M9's sink back gives the flux **entering the channel network above the Momposina**:

| | low end | high end |
|---|---:|---:|
| outlet load | 144 | 184 |
| + Momposina retention (M9) | +36 | +80 |
| **= channel input above the sink** | **180 Mt/yr** | **264 Mt/yr** |
| **÷ our gross hillslope erosion 248.730** | **0.7237** | **1.0614** |

M9's two forms are internally consistent: 36 Mt at 20 % and 80 Mt at 45 % both imply a channel
input of ~178–180 Mt/yr, matching 144 + 36 exactly.

**Read this carefully, because it is the opposite of what the gate assumed.** The
hillslope-to-channel ratio is **0.72 – 1.06 ≈ 1**. A hillslope-to-channel delivery of ~1.0 requires
essentially **zero net hillslope and low-order-channel deposition**, and it leaves **no room at all**
for the gully, bank, landslide and mining sources that demonstrably contribute (§6). The only way
to restore a physically sensible hillslope delivery ratio *and* leave room for non-hillslope
sources is for **gross hillslope erosion to be substantially larger than 248.73 Mt/yr**. Netting the
Momposina out and back in therefore points at the **erosion side**, not at the anchor — which is
exactly the conclusion §7 reaches from three independent directions.

Getting this wrong in the other direction — treating the published 0.05–0.30 as
hillslope-to-outlet — would have made the model look 1.9–14.8× too small in gross erosion when the
honest, comparability-corrected figure is 1.6–2.7× (§7).

---

## 6. Task 4 — the sources MUSLE does not represent

A **Magdalena-specific partition** of load among hillslope, gully, bank, landslide and mining
sources **does not exist in the literature. This is UNCITED, and the fraction is therefore treated
as unquantified for this basin.** What *is* citable is that the omitted fraction is large in systems
of this kind, from four directions:

1. **USDA's own reference partition.** NEH Ch. 6 Table 6-2: sheet erosion is **39.13 %** of gross
   erosion; channel-type sources (gullies, roadbanks, streambanks) are **60.87 %** — and they
   deliver at **80–100 %** against sheet erosion's **33 %**, so their share of the *yield* is
   larger still (1,300,000 of 1,600,000 = **81.25 %**).
2. **Channel sources alone can exceed the outlet load in a large lowland river.**
   **Dunne, Mertes, Meade, Richey & Forsberg (1998)**, *GSA Bulletin* 110(4):450–467, for the
   2,010 km Brazilian Amazon reach: sediment supplied to the channel by **bank erosion averages
   1,570 Mt/yr, which is 1.3× the ~1,200 Mt/yr flux past Óbidos**. Exchanges in each direction
   exceed the annual outlet flux. This is the cleanest published demonstration that the ADR of §2.3
   is not bounded by 1 in a large river with an active floodplain — and the Magdalena's Momposina
   reach is precisely such a system.
3. **Mining.** **Dethier et al. (2023)**, *Nature* 620:787–793: **396 mining districts in 49
   countries**, and "**of 173 mining-affected rivers, 80 % have suspended sediment concentrations
   (SSCs) more than double pre-mining levels**"; in 30 countries with mining on large (>50 m)
   rivers, **23 ± 19 %** of large-river length is altered, i.e. **35,000 river km**. Colombia's
   Cauca–Nechí alluvial gold district is one of the tropics' largest; a **Magdalena-specific
   mining-derived tonnage is UNCITED**.
4. **Mass wasting and channel erosion in steep Andean terrain.** de Vente et al. (2007) frame the
   controlling question as exactly this — whether hillslope erosion or channel erosion dominates —
   and note that where channel erosion dominates, specific yield *rises* with area. M5/M6 place
   **78–79 %** of the Magdalena catchment in a critical/severe erosional state, and M8 gives the
   Colombian Andes a mean yield of **1,485 t km⁻² y⁻¹**. A **quantified landslide/gully share for
   the Magdalena is UNCITED.**

Lower bound on how much 248.73 Mt/yr must under-represent gross basin erosion: **at least the
non-hillslope share**, which is unquantified for the Magdalena but is 61 % of gross erosion in
USDA's reference partition. Two independent statements to keep separate:

- **We cannot cite a Magdalena non-hillslope fraction.** Treated as unvalidated.
- **We can cite, in the same basin, that our hillslope erosion rate is already too low on its own**
  — which is §7, and which does not depend on the non-hillslope fraction at all.

---

## 7. The test that *can* be evaluated, and what it says

Drop the ADR. Test the **gross hillslope erosion rate** directly against published erosion and
yield levels. Three legs, three independent sources, all failing in the same direction.

> **QUALIFIED BY §0 (2026-08-11), and this is the section §0 qualifies.** The label "gross hillslope
> erosion" used below is an assumption, not a definition: SWAT's Ch. 4:1 defines this equation's
> output as a sediment **yield**. Under that reading **Leg A's sign inverts** (ours is 1.33 – 1.49×
> *above* Tan's converted level, not 2.03 – 2.27× below), **Leg C's max-yield form is invalid at
> basin scale** and is dropped, and Leg B was already conceded not to be evidence. The three legs are
> re-derived under both readings, at the adopted `C`, in `docs/37` **A1.9**. Read "all failing in the
> same direction" as **superseded**: the direction is unknown.

**Leg A — against a published mountainous-basin gross erosion rate (like-for-like denominator).**
Tan, Liu & Lu (2024) report **23.7 – 26.5 t ha⁻¹ a⁻¹** basin-average RUSLE hillslope erosion. Ours
is **9.675 t ha⁻¹ a⁻¹**.

| | our rate | Tan et al. | ratio | their rate over 257,097 km² | implied ADR vs 144 – 184 Mt/yr |
|---|---:|---:|---:|---:|---:|
| low | 9.675 | 23.7 | **2.450×** | **609.32 Mt/yr** | 0.2363 – 0.3020 |
| high | 9.675 | 26.5 | **2.739×** | **681.31 Mt/yr** | 0.2114 – 0.2701 |

Note the convergence: `docs/37` §2's own table said "SDR 0.30 ⇒ required gross erosion
**480 – 613 Mt/yr**". Leg A's independent, citation-derived 609.32 Mt/yr **lands inside that row**.

**Leg B — against measured yield inside our own basin's Andean interior. This leg is a hard
inequality, not a comparison.** Since sediment yield ≤ gross erosion wherever net deposition is
non-negative, a measured yield that exceeds our modelled gross erosion over the same terrain is a
proof of under-erosion, independent of any SDR band.

| quantity | value | source |
|---|---:|---|
| Colombian Andes mean sediment **yield** | **1,485 t km⁻² y⁻¹** | M8, 119 Andean gauging stations |
| our **model-internal specific erosion**, Andean flanks 500–3,000 m, area-weighted | **931.95 t km⁻² y⁻¹** | `docs/37` §3 gate (a) |
| shortfall | **1.593×** | computed here |

Our modelled Andean gross erosion is **below** a published Andean *yield*, which implies a local
delivery ratio **> 1**. That is impossible, so the modelled erosion is too low there by at least
1.59×.
*Label discipline (`docs/23` §13.2, and this run's embargo):* the 931.95 is **model-internal
specific erosion** — model erosion over model area — **not** a gauge-referenced yield. It is
compared here against a published yield as a directional diagnostic. The spatial supports differ
(our 500–3,000 m elevation bands vs M8's 119-station Andean compilation), so the 1.593× is an order
of magnitude statement, not a calibrated factor.

**Leg C — against measured yield in this basin's own tributaries.** M7 reports in-basin yields up
to **2,200 t km⁻² yr⁻¹** (catchments 320 – 59,600 km²), and a 32-sub-basin mean of
**~690 t km⁻² yr⁻¹**. Our **basin-mean gross hillslope erosion is 967.46 t km⁻² yr⁻¹** — only
**1.40×** the mean measured *yield*, and **0.44×** the maximum measured yield
(2,200/967.46 = **2.274×** the other way). A basin-mean gross erosion barely above the mean gauged
yield, and less than half the maximum gauged yield, is the signature of an under-erosive model.

> **The max-yield half of Leg C is WITHDRAWN by §0.2.** A basin mean over 257,097 km² is
> arithmetically required to sit below the maximum of 32 sub-basins of 320 – 59,600 km²; this model's
> own internal range is 18.671×. The "0.44×" (0.530× at the adopted `C`) measures spatial variability,
> not under-erosion. Only Leg C's **mean** form survives, and it is a yield-vs-yield test in which the
> model sits **above** the measured mean — the expected direction, not a shortfall.

**Combined:** the residual is **1.59 – 2.74×** on the gross-erosion side. That is a *far* tighter
bracket than `docs/37`'s 1.93 – 14.8×, and it sits inside the **2–5×** that `docs/37` §4 candidate 1
(grassland `C = 0.01`, Roose "good condition", 36.8 % of the area-weighted basin C, against a Roose
table spanning a factor of 10) already estimated for itself. The two independent lines of evidence
agree, which is the strongest statement this document makes.

**And the 0.05 and 0.15 rows of `docs/37` §2's requirement table must be struck.** They demanded
960 – 3,680 Mt/yr of gross erosion and tripped the `docs/35` §6.1 hard stop; they rest entirely on
the retired band and on the ADR/SDR conflation, and they overstated the problem by 4 – 8×.

---

## 8. VERDICT and the replacement clause

### 8.1 Verdict: **UNCITABLE**

Restating the criterion from the task: *no defensible basin-scale SDR band exists for a system like
this, so the SDR test must be retired as a gate — it cannot pass or fail an unvalidated level — and
`docs/37`'s closure conjunction must be rewritten around a test that can actually be evaluated.*

Four findings, each sufficient on its own:

1. **Quantity mismatch.** Published SDR has all-source gross erosion in the denominator
   (NEH Ch. 6). Ours has hillslope only. The two are not the same ratio, and USDA's own worked
   example puts them **2.1× apart in the same watershed** (0.33 vs 0.6957) with the mixed
   version at **1.7778**.
2. **Scale and region.** The band's supporting relations were fitted over **0.0259 – 259.0 km²** of
   US agricultural land (**992.7×** below our basin) and their own source states that using them
   outside their physiographic area "is generally not recommended".
3. **No Magdalena SDR, and none constructible.** Every Magdalena "erosion rate" in print
   (550, 690, 710, 1,485, 128–2,200 t km⁻² yr⁻¹) is a sediment **yield** — the numerator. `USLE`
   and `RUSLE` appear **zero times** in the fullest published treatment.
4. **The area trend's sign does not hold here.** The one fitted SDR study in a large, data-sparse,
   mountainous basin (Tan et al. 2024) finds SDR **increasing** with drainage area; de Vente et al.
   (2007) state the decay holds above 10⁴ km² only "when drainage density decreases or channel
   banks are stabilized", neither of which describes the Magdalena–Cauca; and Parsons et al. (2006)
   ask in a title whether sediment delivery is a fallacy at all.

Per this run's standing rule — *an uncited plausibility band may not be used to pass **or** fail a
gate* — the band is retired in **both** directions. C3 does **not** get to close by declaring
0.579–0.740 acceptable, and it does **not** stay open on the strength of the band either. It stays
open on the **replacement test**, which fails on measured, cited grounds.

### 8.2 Exact replacement wording for `docs/37`'s third closure clause

> **AMENDED BY §0.** The wording below was adopted verbatim as `docs/37` A1.1 clause 4′ and then
> **re-opened**: its Leg A is not like-for-like, its Leg C max form is invalid at basin scale, and its
> Leg B was already conceded not to be evidence. The clause that supersedes it — **4″, a
> quantity-explicit test that must be evaluated under both readings and is currently NOT
> ESTABLISHED** — is written in `docs/37` **A1.9**, together with the re-derivation at the adopted
> `C`. Do not re-adopt the wording below without §0.

Replace the fourth row of `docs/37` §1's closure table:

> | **the implied sediment delivery ratio is physically plausible (0.05 – 0.30)** | **NOT MET — implied SDR is 0.579 – 0.740** |

with:

> | ~~the implied sediment delivery ratio is physically plausible (0.05 – 0.30)~~ **RETIRED — see `docs/40`** | **the ratio 248.730 Mt/yr ↔ 144–184 Mt/yr is not a sediment delivery ratio** (all-source numerator, hillslope-only denominator) and cannot be tested against a published SDR band in either direction. The band was uncited, its supporting relations use an all-source denominator and were fitted 993× below this scale, and no Magdalena SDR exists in the literature. |
> | **the basin-mean gross HILLSLOPE erosion rate is consistent with published erosion and yield levels for humid tropical Andean and comparably mountainous large basins** | **NOT MET — the model is under-erosive by 1.59 – 2.74×**, on three independent citable legs: (A) 9.675 t ha⁻¹ a⁻¹ vs 23.7–26.5 t ha⁻¹ a⁻¹ RUSLE hillslope erosion in a large data-sparse mountainous basin (Tan et al. 2024) ⇒ **2.450 – 2.739×**; (B) modelled Andean-flank specific erosion 931.95 t km⁻² yr⁻¹ **below** the Colombian Andes measured mean *yield* of 1,485 t km⁻² yr⁻¹ (Latrubesse & Restrepo 2014), which implies a local delivery ratio > 1 and is impossible ⇒ **≥ 1.593×**; (C) basin-mean gross erosion 967.46 t km⁻² yr⁻¹ only 1.40× the 32-sub-basin mean measured *yield* of ~690 and 0.44× the maximum measured yield of 2,200 t km⁻² yr⁻¹ (Restrepo et al. 2006) ⇒ **up to 2.274×**. |

And in `docs/37` §4, replace residual 3 with:

> 3. ~~The 0.05 – 0.30 SDR expectation itself is uncited in this repository.~~ **RESOLVED AND
>    RETIRED (`docs/40`).** The band is retired as a gate: the tested quantity is an *apparent*
>    delivery ratio (all-source outlet load ÷ hillslope-only gross erosion), not an SDR, and the
>    same mixed ratio is **1.7778** in USDA NEH Ch. 6's own reference example (where the true SDR
>    is 0.6957 and the hillslope-only ratio 0.33). No Magdalena SDR exists, because every published
>    Magdalena "erosion rate" is a sediment *yield*. The residual survives, relocated and much
>    smaller: **1.59 – 2.74× of gross hillslope erosion**, on the erosion side, consistent with
>    candidate 1 (`C`) alone. `docs/37` §2's SDR = 0.15 and SDR = 0.05 requirement rows are struck.

Two further edits `docs/37` needs, both consequences of the above:

- **§2, "So `SDR = outlet / gross` must be < 1":** false for the quantity computed. Replace with:
  *the ratio of outlet load to hillslope-only gross erosion has no upper bound of 1 — channel-bank
  supply alone averages 1.3× the outlet flux in the Brazilian Amazon (Dunne et al. 1998).*
- **§5.1's new trap stands and strengthens.** Fitting α to outlet load without an explicit
  deposition step still silently encodes ADR = 1. `docs/40` §5.2 makes this worse, not better: with
  the Momposina added back, the hillslope-to-channel ratio is already **0.72 – 1.06**, so the model
  is within ~40 % of encoding zero hillslope deposition **before** any fitting. The
  `docs/35` §6.1 guard cannot see this. Keep the prohibition.

### 8.3 What this does *not* license

- It does **not** close C3. One closure condition is now evaluable and **failed** — *amended by §0:
  the replacement condition is **not established**, because its own decisive leg compares two
  different quantities. C3 remains open on `docs/37` A1.1 clauses 2 and 3 independently.*
- It does **not** authorise moving α, or any convention, to close the gap (`docs/35` §6 RULE 0).
- It does **not** license a `C`-factor revision without its own citation — `docs/37` §4 candidate 1's
  resolver (a citable land-condition source for Colombian Andean pasture and cropland) is unchanged
  and is now the **single highest-value open item in Phase C**, because §7 shows the residual is the
  size that `C` alone can explain.
- It does **not** unembargo gauge-referenced t/km²/yr yields (`docs/23` §13.2). §7 Leg B's model
  figure is labelled model-internal throughout.

---

## 9. Citations, with what each establishes and how it was retrieved

Retrieval status is stated for every item, because two of them are load-bearing and one is a
secondary attribution.

| ref | full reference | establishes | retrieval |
|---|---|---|---|
| C1 | **USDA NRCS**, *National Engineering Handbook*, **Part 632, Chapter 6, "Sediment Sources, Yields, and Delivery Ratios"** | gross erosion = **all** water erosion incl. gullies, valley trenches, streambanks; `Y = E·DR`; fig. 6-2 axis **0.01–100 mi²**; SDR ∝ A^(−0.2); Table 6-2 (sheet DR 33 %, total DR 70 %, sheet share 39.13 %, ADR 1.7778); out-of-domain prohibition | **VERIFIED** — PDF fetched and text-extracted (18 pp., 44,190 chars); all quotes read from the extracted text |
| C2 | **Vanoni, V.A. (ed.) (1975).** *Sedimentation Engineering.* ASCE Manuals and Reports on Engineering Practice No. 54, New York, 745 pp. | `SDR = 0.42 A^(−0.125)`, A in mi², 300 watersheds → **0.0997** at our A | equation quoted **via a secondary compilation** (Michigan State Univ. RUSLE/SDR page); ASCE Manual 54 itself is listed in C1's reference list, confirming the source exists as cited. **Area range of the 300-watershed sample: NOT ESTABLISHED.** |
| C3 | **Renfro, G.W. (1975).** SDR relation for the Blackland Prairie, Texas | `log SDR[%] = 1.7935 − 0.14191 log A`, A in km², R² = 0.92, **14 watersheds** → **0.1061** | same secondary compilation as C2 |
| C4 | **USDA-SCS (1979)** | `SDR = 0.51 A^(−0.11)`, A in mi² → **0.1439** | same secondary compilation as C2 |
| C5 | **Walling, D.E. (1983).** *The sediment delivery problem.* **Journal of Hydrology 65:209–237**, doi 10.1016/0022-1694(83)90217-2 | the canonical statement of the problem; area exponent range **−0.01 to −0.25** | bibliographic record **VERIFIED via Crossref**; the exponent range is **SECONDARY** — the primary PDF located is an image scan with **0 extractable characters** and no OCR was available. **Treat the −0.01/−0.25 range as unverified.** |
| C6 | **de Vente, J., Poesen, J., Arabkhedri, M. & Verstraeten, G. (2007).** *The sediment delivery problem revisited.* **Progress in Physical Geography 31(2):155–178**, doi 10.1177/0309133307076485 | SSY–area decay is an assumption, not a law; positive relations reported; hillslope-vs-channel dominance decides the sign; decay above ~10⁴ km² conditional on falling drainage density or stabilized banks | **VERIFIED** — full abstract retrieved verbatim via Crossref |
| C7 | **Parsons, A.J., Wainwright, J., Brazier, R.E. & Powell, D.M. (2006).** *Is sediment delivery a fallacy?* **Earth Surface Processes and Landforms 31(10):1325–1328**, doi 10.1002/esp.1395 | the concept's transferability is contested in the primary literature | bibliographic record **VERIFIED via Crossref**; abstract not retrieved — cited for its existence and title only |
| C8 | **Tan, Y., Liu, H. & Lu, Y. (2024).** *Predicting soil erosion and sediment delivery in large, data-sparse, mountainous basins.* **Earth Surface Processes and Landforms 49:1778–1795**, doi 10.1002/esp.5797 | mountainous-basin RUSLE hillslope erosion **23.7–26.5 t ha⁻¹ a⁻¹**; SDR **0.07–0.38** over 39 subbasins, ~30 % ≥ 0.35; SSY 1.3–16.9 t ha⁻¹ a⁻¹; **SDR positively correlated with drainage area**; 86 % of SDR variance explained | **VERIFIED** — full abstract retrieved verbatim via Crossref. Full text 403 (paywall); the lower-reach catchment area (~86,000 km², secondary) is **not verified** and is used only to say the 39 subbasins are ≪ 257,097 km² |
| C9 | **Restrepo, J.D. & Kjerfve, B. (2000).** *Magdalena river: interannual variability (1975–1995) and revised water discharge and sediment load estimates.* **Journal of Hydrology 235(1–2):137–149**, doi 10.1016/S0022-1694(00)00269-9 | **144 Mt/yr** at Calamar, 1975–1995 | **VERIFIED** in `docs/34` §5.1 (Crossref) |
| C10 | **Restrepo, J.D. & Escobar, H.A. (2018).** *Sediment load trends in the Magdalena River basin (1980–2010): anthropogenic and climate-induced causes.* **Geomorphology 302:76–91**, doi 10.1016/j.geomorph.2016.12.013 | **184 Mt/yr**, 1980–2010 | bibliographic record **VERIFIED via Crossref**; abstract elided by publisher, full text 403 on four hosts. A widely-quoted "major floodplains trap ~10–40 % of upstream sediment production" attributed to this paper was seen **only in a search-engine paraphrase** and is therefore **NOT USED** here — M9 (C11) is used instead |
| C11 | **Restrepo A., J.D. (2015).** *El impacto de la deforestación en la erosión de la cuenca del río Magdalena (1980–2010).* **Revista de la Academia Colombiana de Ciencias Exactas, Físicas y Naturales 39(151):250–…**, doi 10.18257/raccefyn.141 | 550 → **710 t km⁻² a⁻¹** (+34 %), +44 Mt a⁻¹; **690 t km⁻² año⁻¹ at Calamar** in 2000 vs Amazon 167 / Orinoco 158 / Paraná 43 / São Francisco 10; **78 %** critical erosion; 9 % / ~160 Mt / 16 Mt a⁻¹ from deforestation; **Momposina retention 20–45 %, 36–80 Mt/yr**; and the negative result that `USLE`/`RUSLE` appear **zero times** | **VERIFIED** — full article HTML fetched (curl, ISO-8859-1) and searched; all quotes verbatim from that text. **M9 is labelled by its own author as "una cifra preliminar"** and must be quoted as preliminary |
| C12 | **Restrepo, J.D., Kettner, A.J. & Syvitski, J.P.M. (2015).** *Recent deforestation causes rapid increase in river sediment load in the Colombian Andes.* **Anthropocene 10:13–28**, doi 10.1016/j.ancene.2015.09.001 | erosion **+33 %** 1972–2010, load **+44 Mt/yr**, **482 Mt** from forest clearance over three decades, **79 %** severe erosion | bibliographic record **VERIFIED via Crossref**; the numbers are from a search-result summary of the abstract, and they are the English counterparts of C11's verified figures (33 % vs 34 %, 79 % vs 78 %) — the small discrepancies are noted rather than reconciled |
| C13 | **Restrepo, J.D., Kjerfve, B., Hermelin, M. & Restrepo, J.C. (2006).** *Factors controlling sediment yield in a major South American drainage basin: the Magdalena River, Colombia.* **Journal of Hydrology 316:213–232**, doi 10.1016/j.jhydrol.2005.05.002 | in-basin yields **128–2,200 t km⁻² yr⁻¹** for **320–59,600 km²**; 32-sub-basin mean **~690**; runoff explains 51 % of variance | bibliographic record **VERIFIED via Crossref** (authors, journal, volume, pages); numbers from a search-result summary of the abstract |
| C14 | **Latrubesse, E.M. & Restrepo, J.D. (2014).** *Sediment yield along the Andes: continental budget, regional variations, and comparisons with other basins from orogenic mountain belts.* **Geomorphology 216:225–233**, doi 10.1016/j.geomorph.2014.04.007 | **Colombian Andes mean sediment yield 1,485 t km⁻² y⁻¹**; N+C Andes weighted mean **2,045 t km⁻² y⁻¹**, **2.25 Gt y⁻¹**; **119** Andean gauging stations | bibliographic record **VERIFIED via Crossref**; the 1,485 figure was returned **verbatim and identically by two independent searches** of the paper's text, but the full text was not retrieved — treat as **high-confidence secondary** |
| C15 | **Restrepo, J.D. & Syvitski, J.P.M. (2006).** *Assessing the effect of natural controls and land use change on sediment yield in a major Andean river: the Magdalena drainage basin, Colombia.* **AMBIO 35(2):65–74**, doi 10.1579/0044-7447(2006)35[65:ATEONC]2.0.CO;2 | Magdalena in the world's top 10 by load, "approximately **150 Mt/yr**" | bibliographic record **VERIFIED via Crossref**; number from a search-result summary |
| C16 | **Dunne, T., Mertes, L.A.K., Meade, R.H., Richey, J.E. & Forsberg, B.R. (1998).** *Exchanges of sediment between the flood plain and channel of the Amazon River in Brazil.* **GSA Bulletin 110(4):450–467** | **bank-erosion supply averages 1,570 Mt/yr = 1.3× the ~1,200 Mt/yr Óbidos flux** over 2,010 km — channel sources alone can exceed the outlet load, so the ADR is not bounded by 1 | volume/issue/pages **VERIFIED** from the GeoScienceWorld article listing; numbers from a search-result summary of the abstract. Not found under the Crossref bibliographic query attempted |
| C17 | **Dethier, E.N., Silman, M., Díaz Leiva, J., Alqahtani, S., Fernandez, L.E., Pauca, P., Çamalan, S., Tomhave, P., Magilligan, F.J., Renshaw, C.E. & Lutz, D.A. (2023).** *A global rise in alluvial mining increases sediment load in tropical rivers.* **Nature 620:787–793**, doi 10.1038/s41586-023-06309-9 | **396 mining districts in 49 countries**; **80 % of 173 mining-affected rivers have SSC > 2× pre-mining**; **23 ± 19 %** of large-river length altered in 30 countries, **35,000 river km** | **VERIFIED** — full abstract retrieved verbatim via Europe PMC; author list and pagination via Crossref |

| C18 | **Neitsch, S.L., Arnold, J.G., Kiniry, J.R. & Williams, J.R. (2011).** *Soil and Water Assessment Tool Theoretical Documentation, Version 2009.* Texas Water Resources Institute Technical Report No. 406, Texas A&M. Section 4 Chapter 1, "Equations: Sediment", **p. 252** | **the identity of the quantity MUSLE computes** (§0): USLE predicts gross erosion from rainfall energy; MUSLE's runoff factor "represents energy used in detaching **and transporting** sediment" and therefore "eliminates the need for delivery ratios"; eq. 4:1.1.1's `sed` is "the **sediment yield** on a given day (metric tons)", with `areahru` in **ha** | **VERIFIED (primary)** — PDF fetched from `swat.tamu.edu/media/99192/swat2009-theory.pdf` (7,690,470 B, 647 pp) and text-extracted with PyMuPDF; both quotes read off printed p. 252 (PDF p. 277). Authorship, report number and imprint read off the PDF's own title page (p. 2): *"TR-406 / 2011 … By S.L. Neitsch, J.G. Arnold, J.R. Kiniry, J.R. Williams … September 2011 … Texas Water Resources Institute Technical Report No. 406, Texas A&M University System"*. The `sed`-definition half was **independently reconfirmed** from the SWAT+ theoretical documentation MUSLE page, which does *not* carry the delivery-ratio passage — the 2009 PDF is the load-bearing retrieval |

### 9.1 Explicitly UNCITED — treated as unvalidated, used to pass or fail nothing

1. **A Magdalena-specific partition of sediment among hillslope / gully / bank / landslide / mining
   sources.** Nothing published. §6 therefore states a lower bound only by analogy (C1, C16) and
   labels it as such.
2. **A Magdalena mining-derived sediment tonnage.** C17 is global-tropical; no Cauca–Nechí figure
   was found.
3. **A hillslope-to-outlet SDR for any humid tropical Andean basin.** None exists.
4. **The drainage-area range of Vanoni's 300-watershed sample.** Not established; must not be
   assumed to reach 10⁵ km².
5. **Walling (1983)'s −0.01 to −0.25 exponent range as a primary quotation.** Secondary only.
6. **Restrepo & Escobar (2018)'s floodplain-trapping percentage.** Search-paraphrase only;
   deliberately excluded from every calculation here.

---

## 10. Traps this investigation adds

1. **"Erosion rate" in the Magdalena literature means sediment YIELD.** 550, 690, 710, 1,485 and
   128–2,200 t km⁻² yr⁻¹ are all outlet- or gauge-derived loads divided by area. Validating a
   gross-erosion model against any of them as if they were erosion is a one-step route to a
   confidently wrong answer — and it is a route this project would have taken if the SDR gate had
   been resolved by pattern-matching numbers. Where the inequality runs the *right* way
   (§7 Leg B: a yield **above** our modelled erosion is impossible) the comparison is still valid,
   and that is the only way it is used here.
2. **`SDR` and `ADR` differ by the non-hillslope share, which is the majority of gross erosion in
   the one published partition available.** Always state which denominator a delivery ratio uses
   before comparing it with anything.
3. **A gauge downstream of a major floodplain sink has that sink already netted out.** Calamar sits
   below the Momposina; the anchor is a *post-sink* number and cannot be compared with a *pre-sink*
   modelled flux without adding the sink back (§5.2).
4. **A MUSLE sum is not self-evidently a gross erosion, and calling it one is a *definitional*
   assumption that sets the sign of the residual.** SWAT Ch. 4:1 (C18) says this equation's output is
   a sediment **yield** whose runoff factor already covers transport, which is why MUSLE
   "eliminates the need for delivery ratios". Comparing a MUSLE sum against a (R)USLE erosion rate is
   the *same* quantity error as comparing an ADR against an SDR — and this document made it, on the
   erosion side, in the very clause it wrote to replace the delivery-ratio gate (§0). Before any
   erosion- or yield-level comparison: say which quantity **both** sides are, in writing.
5. **A basin mean can never reach a sub-basin maximum, so "below the maximum" is never evidence.**
   Leg C's withdrawn form compared a mean over 257,097 km² with the maximum of 32 catchments of
   320 – 59,600 km², while the model's own internal range is 18.671×. Compare means with means; if a
   maximum is used at all, it must be against the model's own maximum over comparable supports.
6. **An empirical SDR–area relation carries its calibration domain with it.** NEH fig. 6-2 spans
   0.0259–259.0 km². Extrapolating it 993× is not conservative in either direction — the sign of
   the area trend itself reverses in the one large mountainous basin where it was refitted (C8).

---

## 11. Reproduction

Every arithmetic result in this document is closed-form from the values in §1 and the cited rates.
The full set, as computed:

```
A = 257097 km2 ; gross = 248.730 Mt/yr
basin-mean gross hillslope erosion = 248.730e6 / 257097        = 967.46 t/km2/yr = 9.675 t/ha/yr
implied ADR                         = 144/248.730, 184/248.730  = 0.5789, 0.7397
Vanoni      0.42 * (257097/2.589988110336)^-0.125               = 0.0997
USDA-SCS 79 0.51 * (257097/2.589988110336)^-0.11                = 0.1439
Renfro      10^(1.7935 - 0.14191*log10(257097)) / 100           = 0.1061
NEH fig 6-2 upper limit 100 mi2                                 = 259.0 km2 ; 257097/259.0 = 992.7x
NEH table 6-2 sheet share 900000/2300000 = 0.3913 ; true SDR 1600000/2300000 = 0.6957
              ADR 1600000/900000 = 1.7778
Momposina channel input 144+36 = 180 ; 184+80 = 264 Mt/yr
              /248.730 = 0.7237 ; 1.0614
Tan et al 23.7 t/ha/yr over A = 609.32 Mt/yr ; ratio to ours 2.450 ; ADR 0.2363-0.3020
Tan et al 26.5 t/ha/yr over A = 681.31 Mt/yr ; ratio to ours 2.739 ; ADR 0.2114-0.2701
Leg B  1485 / 931.95 = 1.593
Leg C  2200 / 967.46 = 2.274 ; 967.46 / 690 = 1.402
cross-check  710 t/km2/yr * 257097 km2 = 182.54 Mt/yr  (vs the 184 Mt/yr anchor, 0.8 % apart)

--- section 0 (2026-08-11), at the ADOPTED C: gross = 299.5387 Mt/yr ---
rate            299.5387e6 / 257097 = 1165.0805 t/km2/yr = 11.6508 t/ha/yr
Leg A  erosion reading   23.7 / 11.6508 = 2.0342 ; 26.5 / 11.6508 = 2.2745   (low)
Leg A' yield  reading    NEH sheet DR = 300000/900000 = 0.3333 ; tabulated 0.33
                         23.7*0.33 = 7.8210 ; 26.5*0.33 = 8.7450
                         11.6508/7.8210 = 1.4897 ; 11.6508/8.7450 = 1.3323   (HIGH - sign inverts)
                         with 1/3 exactly: 1.4748 ; 1.3190
   cross-check, no conversion: Tan specific sediment YIELD 1.3-16.9 t/ha/a contains 11.6508
Leg B  1485 / 1445.32 = 1.0275                                    (2.8 %, not evidence)
Leg C  1165.0805/690 = 1.6885 (mean, yield-vs-yield, ABOVE)
       1165.0805/2200 = 0.5296 -> 1.8883 (max form, WITHDRAWN)
       model internal range 1445.32/77.41 = 18.671
throughput  144/248.7298 = 0.5789 ; 184/248.7298 = 0.7398  -> loss 26.02-42.11 % (prior C)
            144/299.5387 = 0.4807 ; 184/299.5387 = 0.6143  -> loss 38.57-51.93 % (adopted C)
   Momposina 36-80 Mt/yr = 12.02-26.71 % of 299.5387
   residual sinks  (299.5387-144) - [36,80] = 75.54-119.54 Mt/yr = 25.2-39.9 %
                   (299.5387-184) - [36,80] = 35.54-79.54 Mt/yr = 11.9-26.6 %
alpha under the yield reading  11.8/1.4897 = 7.921 ; 11.8/1.3323 = 8.857
   (docs/42 G5 deposition-free fit band 6.83-8.73 -> overlaps)
alpha under the erosion reading 11.8*2.034 = 24.00 ; 11.8*2.275 = 26.84
```

No model code, notebook or frozen artifact was executed or modified for this document. The only
files written are this one and `docs/agents/journal_cite-sdr.md`.

**§0's amendment (2026-08-11)** was written by `docs/agents/journal_fixer.md` run 3 and likewise
executed no model code and modified no frozen artifact: it fetched and text-extracted the SWAT 2009
theoretical documentation PDF (C18) into the scratchpad and computed the block above in a throwaway
`python3.10` session. Its erosion levels are quoted from `docs/37` A1.3–A1.4 rather than re-simulated.
The files it wrote are this one, `docs/37_c3_closure.md`, `src/mgb_sediment.py` and its own journal.
