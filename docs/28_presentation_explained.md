# 28 — Everything in the presentation, explained

**Who this is for:** anyone who needs to understand `MGB-SED_Magdalena_FIGURES.pptx` without
having worked on the project. No hydrological modelling background assumed.

**Companion:** `docs/27_presentation_script.md` is what to *say*. This document is what
everything *means*.

**How to use it:** read Parts 0–2 once (about ten minutes) and the rest becomes easy. Part 3
then goes slide by slide, and you can jump straight to whichever slide you are asked about.

> # ⚠ READ THIS FIRST — annotated 2026-08-12
>
> This document explains a deck **as delivered**. Several of its numbers have since been
> overtaken by measurement, and one of them is in the *five things to remember* list at the
> end. Every affected passage below is marked **⚠ SUPERSEDED / CORRECTED 2026-08-12** with the
> live statement beside it and the document that owns it named. **Where the two disagree, the
> owning document wins** — this file owns none of these facts.
>
> **The one that matters most, if you read nothing else:**
> ~~"the dry season went from worse-than-climatology to better"~~ →
> **that is true of attempt 1 → attempt 2 only. It is NOT true of the model the project
> adopted.** In the adopted model the dry El Niño phase scores **−0.0005** against a seasonal
> climatology — i.e. it **matches** climatology, it does not beat it. Owner:
> [docs/26](26_phase3_refit.md) Addendum **A.5**. Affected here: **Part 2**'s climatology
> table, **slide 9**, **slide 10**, **slide 16**, and **Part 4 item 2**.
>
> Also superseded: **slide 17**'s next-step list (four of five have been executed, with
> outcomes), **slide 18**'s advisor question (asked; the advisor declined; the team decided),
> and the "Phase C is blocked" framing in **Part 0** and **slide 3**.
>
> *(Not changed, and deliberately so: the **+38 %** in Part 2's PBIAS section is a worked
> teaching example of what percent bias means, not a project number. Leave it alone.)*

---

# Part 0 — The project in one page

**The physical problem.** The Magdalena river drains most of populated Colombia. It carries an
enormous amount of mud and sand — sediment — and how much it carries changes hugely from year
to year. Wet years move far more sediment than dry years. That sediment fills up reservoirs
behind dams, builds and erodes the delta, and affects drinking water.

**The climate driver.** The main reason for the year-to-year swing is **ENSO**, the Pacific
climate cycle. Its wet phase is called **La Niña**, its dry phase **El Niño**. We picked the
strongest recent example of each: **2011** (very wet) and **2015–16** (very dry).

**What already exists.** People have shown *statistically* that wet ENSO years move more
sediment — they correlated the two. That tells you the relationship exists, but not where in
the basin it comes from or why.

**What we are adding.** A **process-based model**: a computer model that actually simulates
rain falling, soaking into soil, evaporating, running off, and flowing down channels — and
then how much soil that moving water picks up and carries. Because it simulates the physics
in every part of the basin separately, it can tell you *which sub-basins* drive the
difference, and *which mechanism* is responsible.

**Why the talk is only about water.** Sediment transport is driven by **runoff** — the volume
and speed of water moving over the land — not directly by rainfall. So the water model has to
be right first. If you tuned the erosion parameters on top of a wrong water model, the erosion
parameters would silently absorb the water errors, and you would get numbers that look fine
and mean nothing.

**Where we actually are.** The water model works, conserves mass exactly, and is calibrated.
It performs moderately well overall, and noticeably worse in the dry El Niño phase. We spent
considerable effort finding out *why*, and the answer turned out to be **the rainfall data,
not the model** — a result we can quantify. ~~The sediment phase is built but blocked on data
quality.~~

> **⚠ CORRECTED 2026-08-12 — the last sentence.** → **The sediment phase has started.** Owner
> [docs/30](30_phase_c_plan.md), header: *"It supersedes the 'Phase C blocked' line in older
> docs."* The data-quality gate was run and its result is precise
> ([docs/32](32_ssc_qc_audit.md) §R6): **79 of 79 sediment stations classified**, each with a
> deciding measurement; **18 usable**; and *"`21237020` ARRANCAPLUMAS (Magdalena — **the only
> Magdalena-trunk SSC station in the entire network**)… This is the quantitative form of
> 'Phase C is blocked on mainstem SSC'."* So the constraint is real but it is **one station on
> the main river**, not "we cannot start". **For what stage the project is actually on today,
> read `progress_map.html`, not this document.**

---

# Part 1 — Glossary

Terms in the order you meet them, not alphabetical.

### Geography and units

| term | plain meaning |
|---|---|
| **basin** / **catchment** | all the land whose rain drains to one point |
| **Magdalena–Cauca basin** | our study area, **257,097 km²** — roughly half of Colombia's populated area |
| **outlet** | the single point everything drains through. Ours is at **Calamar** |
| **minibacia** | Portuguese for "small basin". We chop the basin into **8,672** of them; each gets its own water calculation. Think of it as the model's pixel |
| **mainstem** | the main river channel, as opposed to tributaries |
| **Depresión Momposina** | a vast inland wetland where the Magdalena and Cauca meet. Water spreads out and sits there for weeks. Hard to model |
| **mm/yr** | rainfall and river flow are both often expressed as a *depth*: how deep the water would be if spread evenly over the catchment. Lets you compare rainfall with river flow directly |
| **m³/s** | cubic metres per second — the usual unit for river discharge |

### The data we use

| term | plain meaning |
|---|---|
| **DEM** (digital elevation model) | a grid of ground heights. Ours is 30 m resolution from the Copernicus satellite programme |
| **gauge** / **station** | a physical measuring site. **Rain gauges** measure rainfall; **discharge gauges** measure river flow |
| **IDEAM** | Colombia's national hydrology and meteorology institute — the source of our gauge data |
| **ERA5-Land** | a global reanalysis: a model-plus-observations reconstruction of past weather on a grid. We use it for the variables needed to compute evaporation |
| **CHIRPS** | a satellite-based rainfall dataset. Coarser in accuracy than a good gauge, but it covers everywhere, including places with no gauges |
| **SSC** | suspended sediment concentration — how much sediment is in a litre of river water. The measurement Phase C needs |
| **rating curve** | rivers are almost never measured directly. What is measured is **water level**. A rating curve is a fitted equation converting level to flow. **This matters: "measured discharge" is actually a model output** |

### How the model works

| term | plain meaning |
|---|---|
| **water balance** | bookkeeping: rain in, minus evaporation out, minus river flow out, equals change in storage. Must balance exactly |
| **URH** / **HRU** | *hydrological response unit*. Inside each minibacia we don't assume one uniform surface — we cross **3 soil textures × 8 land-cover classes = 24 types**. Clay under forest sheds water differently from sand under pasture |
| **Wm** | how much water the soil can hold before it starts shedding. Ours: median 73 mm, range 13–255 mm |
| **PET** (potential evaporation) | how much water *could* evaporate given the available energy — the ceiling set by sun, wind, humidity |
| **actual ET** | how much actually evaporates. Less than PET when soil is dry |
| **runoff** | water that flows off the land instead of soaking in or evaporating |
| **saturation-excess runoff** | our runoff mechanism: as soil fills, a growing fraction of the area is saturated, and rain on saturated ground runs off entirely |
| **routing** | moving water down the channel network once it has left the land |
| **the three reservoirs** | the model splits water into a fast path (surface), a medium path (through shallow soil), and a slow path (groundwater). Each drains at its own rate |
| **recession** | when rain stops, river flow decays. The **recession constant** is roughly how many days the decay takes. **This is a fingerprint of underground storage** — you can measure it from real hydrographs and check the model against it. Ours: observed ~10–12 days |
| **celerity** | how fast a flood wave travels down the channel |
| **Muskingum X = 0** | the simple routing we use: each reach is a bucket that fills and drains. Water only goes downstream |
| **local-inertial / hydrodynamic routing** | proper physics: tracks water *depth*, computes flow from the slope of the water surface, so water can spill onto floodplains and even flow backwards. Needed for the Momposina. Far more expensive |
| **MUSLE** | the erosion equation for Phase C. Driven by **runoff and peak flow**, which is why the water model comes first |

### Calibration

| term | plain meaning |
|---|---|
| **parameter** | a number in the model we cannot measure directly and must infer — e.g. how fast groundwater drains |
| **calibration** | searching for the parameter values that best reproduce observed river flow |
| **validation** | testing on data the calibration never saw. **Without this, good performance means nothing** — you have only shown you can fit a curve |
| **split-sample** | the standard approach: calibrate on part of the record, validate on the rest |
| **differential split-sample (Klemeš 1986)** | stricter: calibrate on *one kind* of period and validate on a *different kind*. We calibrate only on **neutral** years, so both ENSO extremes are unseen. **Our headline results are therefore predictions, not fits** |
| **warm-up / spin-up** | the model needs time to forget its arbitrary starting soil moisture. We run 2008 purely to warm up, and score from 2009 |
| **objective function** | the single number the search maximises. Ours combines flow accuracy with, in attempts 2 and 3, a recession penalty |
| **DDS** | the search algorithm (Dynamically Dimensioned Search). Starts by exploring widely, then narrows in |
| **seed** | the random starting point of a search. Different seeds → slightly different answers. If two seeds disagree more than two experiments do, you cannot tell the experiments apart |
| **pre-registration** | writing down which experiments you will run *before* running them. Stops you from running twenty variants and reporting the luckiest |
| **railed / at a bound** | each parameter is searched inside allowed limits. If the best value sits *at* a limit, the search wanted to go further — a warning sign that the model is compensating for something wrong |
| **equifinality** | many different parameter sets fit equally well. Common and awkward: it means a good fit does not prove the parameters are right |

### Data-quality terms specific to this project

| term | plain meaning |
|---|---|
| **zero-suppression** | our central data defect: on dry days, some observers **wrote nothing**. So a blank means "zero" sometimes and "unknown" other times. Average only the recorded days and you average only the *rainy* ones |
| **selectivity statistic** | our detector. For station X, look **only at its neighbours**: on the days X chose to report, was it unusually wet at the neighbours? An honest station gives ~1.0. A rain-selective one gives >1 |
| **IDW** (inverse distance weighting) | turning point measurements into a continuous map by averaging nearby gauges, weighted by closeness |
| **LOOCV** (leave-one-out cross-validation) | hide one gauge, predict it from the others, compare. Repeat for all. Measures **how good the rainfall map itself is** — used heavily on slide 15 |
| **energy floor** | a physical impossibility check. A river cannot carry more water than rainfall minus evaporation can supply. Gauges failing it indicate an error somewhere |
| **mass-balance residual** | how badly the water bookkeeping fails. Ours is 10⁻¹⁷ — machine rounding error, i.e. exact |

---

# Part 2 — How to read the numbers

This part is worth reading twice. Almost every question you will be asked is about one of
these.

## KGE — the main score

**Kling-Gupta Efficiency.** Range: **1 is perfect**; lower is worse; it can go negative.

It bundles three separate questions:

| component | question | perfect |
|---|---|---|
| **r** (correlation) | do the rises and falls happen at the **right times**? | 1.0 |
| **α** (alpha) | is the flow as **variable** as reality — peaks as peaky, lows as low? | 1.0 |
| **β** (beta) | is the **total amount of water** right? | 1.0 |

`KGE = 1 − √[(r−1)² + (α−1)² + (β−1)²]`  — i.e. distance from perfect in three dimensions.

**Why this matters for our story:** a model can be good on one component and bad on another,
and KGE hides which. Reporting the components separately is what let us see that fixing the
volume (β) cost us variability (α), so overall KGE went slightly *down* even though the model
improved. Always ask which component moved.

**Rough interpretation for daily river flow:**

| KGE | reading |
|---|---|
| > 0.75 | very good |
| 0.5 – 0.75 | good |
| 0.3 – 0.5 | moderate — **this is where we are** |
| 0 – 0.3 | weak |
| < 0 | worse than a flat line at the mean |

Daily is much harder than monthly. Most published thresholds are for monthly flows.

## NSE — and why we stopped trusting it

**Nash-Sutcliffe Efficiency.** 1 is perfect. **0 means "no better than predicting the average
of the period you are looking at."**

That last clause is the trap. The benchmark is the variance **inside your chosen window**. So
NSE is **not comparable between windows** with different variability.

Our El Niño window has the most variable flows in the whole record. In that window a *perfect
seasonal climatology* scores NSE **−0.06**. So a negative NSE there does not mean the model is
useless — it means NSE is the wrong yardstick. **About a third of our apparent dry-season
failure was the metric.** This is slide 10.

## PBIAS

Percent bias: is there systematically too much or too little water?

- **0 %** = perfect. **+38 %** = the model produces 38 % too much water.
- Slide 8's attempt 1 had **+6.8 %** after calibration, from **+46 %** before.

## The "climatology benchmark" — what we report instead

A **day-of-year climatology** is the simplest defensible competitor: for every calendar day,
predict the long-term average flow for that day. It knows the seasons and nothing else.

We score that in every window and report **model minus climatology**. This is fair across
windows, because both are measured in the same window.

| period | our gain over climatology — ⚠ **this is ATTEMPT 2 (H1), not the adopted model** |
|---|---|
| La Niña 2011 (wet) | **+0.126** |
| El Niño 2015–16 (dry) | **+0.026** |

~~So we are about **five times better in the wet phase than the dry phase**. That is the honest
statement of our biggest remaining problem.~~

> **⚠ CORRECTED 2026-08-12 — these are not the project's current numbers, and the "five times"
> ratio does not survive.** Presented unqualified as "our gain", the pair above reads as the
> adopted model's. It is not. Owner: [docs/26](26_phase3_refit.md) Addendum **A.5**, which
> tabulates the **adopted** configuration (H2E):
>
> | | La Niña 2011 | El Niño 2015–16 |
> |---|---|---|
> | median KGE | 0.344 | 0.200 |
> | day-of-year climatology KGE | 0.238 | 0.201 |
> | **skill over climatology** | **+0.106** | **−0.0005** |
>
> Quoted: *"**The dry phase in the adopted configuration is at climatology, not above it:
> −0.0005.** Across attempts 2 → 3 → 4 the El Niño skill-over-climatology reads +0.026 →
> +0.006 → −0.0005."*
>
> **The honest statement, in plain language:** in the wet La Niña year the model is genuinely
> better than just knowing the time of year — by about 0.11. In the dry El Niño period it is
> **exactly as good as knowing the time of year, and no better**. **Do not say "five times
> better"** of the adopted model: you cannot form that ratio when the dry-phase number is
> zero. [docs/26](26_phase3_refit.md) A.5 gives the wording to use instead — *"**the wet phase
> is predictable, the dry phase is not**"* — and adds that this *"is the hydrology caveat
> every Phase C sediment claim inside the El Niño window inherits."*

## Recession ratio

`simulated recession constant ÷ observed recession constant`. **1.0 is correct.**

- Attempt 1: **2.98** — groundwater drained about three times too slowly
- Attempt 2: **0.96** — essentially right

## The objective function value, F

The single number the search maximises. Useful only against its own reference points:

| | F |
|---|---|
| unfitted starting parameters | 0.128 |
| best of random guessing | 0.173 |
| attempt 1 | 0.243 |
| a perfect model | 1.000 |

Note that random guessing beat the textbook starting values — those priors were poor for this
basin.

## Orders of magnitude, for reading exponents

`1.67 × 10⁻¹⁷` = 0.0000000000000000167 — i.e. zero to the computer's precision.
When we say water is conserved to 10⁻¹⁷, we mean **exactly**, not "closely".

---

# Part 3 — Slide by slide

Each slide: **what you are looking at**, **what it means**, **why it is there**, and the
**likely question**.

---

## Slide 1 — Title

**Looking at:** the basin's terrain from the 30 m elevation model. Andes on the left in three
ranges, flat lowlands to the north.

**Means:** the physical setting. The three mountain ranges are why rainfall is so patchy — and
patchy rainfall becomes the central problem by slide 15.

**Why:** context, and the subtitle sets scope: *attempts*, not a finished calibration.

---

## Slide 2 — The question, and why these two years

**Looking at:** two panels. Left: basin discharge anomaly per year, from our own gauge
composite. Right: the same ENSO contrast computed independently by the other half of the team.

**Means:** an *anomaly* is a departure from normal, in standard deviations (σ). **2011 sits
~+1.7σ** (much wetter than normal); **2015–16 ~−1σ**. Roughly, ±1σ is the range that contains
about two-thirds of ordinary years, so +1.7σ is genuinely unusual.

**Why:** it forestalls the obvious challenge — *"why those years?"* We did not inherit them
from a paper; they fall out of our own data. And two independent analyses agree.

**Likely question:** *"Why not 2010–2012 for La Niña, since the event spanned it?"*
> An open question we flag for the advisor. 2011 is the peak; widening the window would dilute
> the contrast but increase the sample.

---

## Slide 3 — Where we are, honestly

**Looking at:** a three-row status table, plus a map of simulated runoff per unit area.

**Means:** "specific runoff in mm/yr" = how much water leaves each unit of area per year,
expressed as a depth. High values in the wet Andean flanks, low in dry inter-Andean valleys.
This is the field the sediment module will consume.

**Why:** stating "Phase B is not closed" up front buys credibility for everything after it.
And it explains the ordering — sediment depends on runoff, so water must be right first.

> **⚠ UPDATED 2026-08-12 — the status row on this slide has moved.** Phase B is now **CLOSED**
> ([docs/30](30_phase_c_plan.md) §1) and Phase C has **started** — the "blocked" row is
> superseded (see the correction in Part 0). The *credibility* argument still works, but the
> honest version of it has changed shape: what buys credibility now is saying that Phase B was
> closed **by decision on a measured ceiling, not by passing its own criteria** — the adopted
> configuration scores 3 of the 9 criteria set in advance ([docs/26](26_phase3_refit.md) A.4).

---

## Slide 4 — Preprocessing pipeline

**Looking at:** four panels left to right, then two below.

1. **Conditioned DEM** — raw elevation data has artificial pits from measurement error. Water
   would get trapped there, so they are filled first.
2. **Upstream area** — for every cell, how much land drains into it. Rivers appear
   automatically as the lines of high accumulation. This panel is the most visually striking
   proof the topology is right.
3. **River network** — the above, above a threshold.
4. **Minibacias** — the basin cut into 8,672 units.

Below-left: **URH composition** — the 24 soil × land-cover combinations.
Below-right: **upstream area on a log scale**, outlet at 257,097 km².

**Means:** this is standard hydrological preprocessing, but every step compounds — an error
here propagates into every later number.

**Why:** answers *"how did you get from a satellite DEM to a model?"* in one slide.

**Likely question:** *"Why 8,672 units — why not more or fewer?"*
> A trade-off: finer units capture more spatial detail but cost run time and need input data
> at a resolution we do not have. 8,672 puts the typical unit at ~30 km², comparable to our
> rainfall gauge spacing — finer would be false precision.

---

## Slide 5 — Spatial discretisation and its verification

**Looking at:** a verification table and a map of soil water storage Wm.

**Means the table:**
- **257,096.93 vs 257,096.93 km²** — the area accumulated at the outlet, versus the sum of all
  individual unit areas, computed by two independent algorithms. They must agree; they do, to
  eight decimals.
- **0 area-monotonicity violating edges** — no case where a downstream catchment is smaller
  than one draining into it, which would be impossible.
- **8.9 × 10⁻¹⁶** — the land-cover fractions in each unit sum to 1, to machine precision.

**Means the map:** how much water each unit's soil can hold, from Colombian field survey
(IGAC). Median 73 mm, range 13–255 mm — a **19-fold** spatial range.

**Why:** verification is a theme. Also, using measured soil variation rather than a single
average number is a real modelling choice worth defending.

---

## Slide 6 — Two implementations

**Looking at:** a comparison table, a green highlight, and the search convergence figure.

**Means the table:** the two versions differ in how they move water down channels.

- **A** treats each channel reach as a bucket: simple, one-directional, **12 seconds** for the
  whole basin over eleven years.
- **B** solves shallow-water physics: tracks depth, lets water spill onto floodplains and flow
  backwards. Necessary for the Momposina wetland. **1,500 seconds per run** — 125× slower.

**Means the highlight:** both are calibrated, and they agree to about 0.02 KGE. Since they
share almost no code and process inputs differently, that agreement is a real cross-check —
if either had a serious bug, they would not land in the same place.

**Means the figure:** each line is one optimisation run — objective value climbing as it tries
more parameter sets. Four ran concurrently. **The flattening is the important part**: it means
more searching stops helping.

**Why:** it converts what looks like duplicated effort into a deliberate strategy — *A buys
search, B buys physics* — and the agreement is a result.

**Likely question:** *"Why is A's KGE higher than B's if B has better physics?"*
> Because A has been calibrated far harder — 4,000 evaluations against B's few. Better physics
> with default parameters loses to simpler physics that has been fitted. That is exactly why
> we need both.

---

## Slide 7 — Model period and the split

**Looking at:** the split description, and the warm-up convergence figure.

**Means the split:** we run 2008–2018. **2008 is warm-up only.** We calibrate on **neutral**
years and validate on the ENSO extremes — so 2011 and 2015–16 are never seen by the fitting.

This is stricter than usual. Normal split-sample holds back a random chunk. **Differential**
split-sample holds back a *different kind of period*, which tests whether the model transfers
to conditions it was not tuned for — precisely the question this project asks.

**Means "cal→val degradation −0.159, only 0.011 worse than an unfitted model":** every model
does worse on unseen data. The question is *how much* worse. Ours degrades barely more than a
model that was never fitted at all — so the fitting is capturing real behaviour, not
memorising noise.

**Means the figure:** three deliberately incompatible starting states — dry soil, saturated
soil, and equilibrium. By the end of 2008 they converge to within **0.18 %** of mean flow, so
the results do not depend on our starting guess.

**Why:** the single most important credibility slide. Everything after depends on it.

**Likely question:** *"Isn't calibrating on only three neutral years too little data?"*
> It is a deliberate cost. We trade sample size for a genuinely independent test of the thing
> we care about. And the overfitting check says we did not pay for it in generalisation.

---

## Slide 8 — ~~Three~~ **Four** calibration attempts

> **⚠ CORRECTED 2026-08-12 — there are four.** [docs/24](24_presentation_outline.md) slide 8's
> table was updated on 2026-08-10 to add attempt **4 — H2E**, the adopted configuration:
> VAL KGE **0.356**, recession **0.98×**, PBIAS **+3.51 %**. Owner
> [docs/26](26_phase3_refit.md) Addendum **A.4**, and its honest reading: *"H2E's gain over H2
> is **in volume, not in skill**… VAL KGE moves +0.011 and r +0.008 — both inside the 0.051
> seed spread docs/29 measured, so neither is a separation."* Everything below about attempts
> 1–3 is unchanged and still correct.

**Looking at:** a dual-axis bar chart and a summary table.

**Means the chart:**
- **Navy bars, left axis** — VAL KGE, our accuracy score. Higher is better.
- **Red bars, right axis** — recession ratio, simulated ÷ observed. **1.0 is correct**, and the
  green shaded band marks the acceptable range.

**Reading it:** attempt 1 has the best KGE **and** by far the worst recession — a factor of
three too slow. Attempts 2 and 3 give up some KGE and land the recession almost exactly right.

**Means "params at bound":** how many parameters ended pressed against their allowed limits.
Any non-zero count is a warning that the model is compensating for something.

**Why:** it sets up slide 9 by showing the trade rather than asserting it.

**Likely question:** *"You made it worse. Why present that?"*
> Because KGE is not the objective — a usable model is. See slide 9.

---

## Slide 9 — The central result

**Looking at:** three bar groups per period.

- **Green** — recession constant measured in the **real rivers**, ~9.5–11.9 days
- **Red** — attempt 1, 27–45 days. Labels show the ratio: **2.9× to 3.9× too slow**
- **Navy** — attempt 2 after refitting, **0.92× to 1.27×**

**Means it physically:** the recession constant reflects how water is released from
underground storage. Three times too slow means the model was holding water back far too long
— it happened to produce roughly the right *total*, but by the wrong *mechanism*. Fine as long
as you only ask it questions like the ones it was fitted to; unreliable the moment you ask
something new — a different climate period, or feeding a sediment module that responds to
*peaks*.

**Means the trade:** we lost **0.029 KGE**. We gained a correct recession, and the dry El Niño
phase went from **worse** than a seasonal average (−0.026) to **better** (+0.026) — for the
first time.

> **⚠ CORRECTED 2026-08-12 — the sentence above is true of this comparison and ONLY of this
> comparison.** It is attempt 1 → attempt 2. **It does not survive into the model the project
> adopted.** Owner [docs/26](26_phase3_refit.md) Addendum **A.5**, quoted in full because this
> is the most-quoted wrong sentence in the deck:
>
> > "The deck's slide-9 argument ('the dry phase turns from worse-than-climatology to better')
> > was measured on attempt 1 → attempt 2 and remains true *of that comparison*; it is **not**
> > true of the configuration the project adopted, and docs/24 must not be read as claiming it
> > is."
>
> > "**The dry phase in the adopted configuration is at climatology, not above it: −0.0005.**"
>
> **What to say if asked:** the trade was real and we would make it again — but the dry-season
> gain was later given back. Across attempts 2 → 3 → 4 it reads **+0.026 → +0.006 → −0.0005**.
> In the adopted model the dry phase **matches** a seasonal average; it does not beat it.
> [docs/24](24_presentation_outline.md) slide 9 carries this same correction (added
> 2026-08-10) and its instruction is *"it must be spoken, not skipped"*.

**Why:** it is the argument that we are optimising for a defensible model rather than a
flattering number. It is also the most likely thing to be challenged, so know it cold.

**Likely question:** *"How do you measure the observed recession?"*
> Find stretches where flow declines steadily for at least three days at low flow, fit an
> exponential decay, take the median. We validated the estimator by checking it reproduces
> ratios recorded independently earlier in the project.

---

## Slide 10 — Scoring against a benchmark

**Looking at:** grouped bars — KGE gain over a day-of-year climatology, by period, for all
three attempts. Above zero = beats the seasonal average.

**Means:** we discovered our dry-season NSE was negative and nearly over-reacted. Before
concluding the model was useless there, we scored a **perfect seasonal climatology** in the
same window. It also came out negative (−0.06), because NSE's benchmark is the variability
*within the chosen window* and that window is the most variable in the record.

So we report the difference from that fixed benchmark instead — fair across windows.

**Reading it:** every period is positive except El Niño for attempt 1. La Niña **+0.126** vs
El Niño **+0.026** — ~~about **five times better wet than dry**~~ **for attempt 2**.

> **⚠ CORRECTED 2026-08-12.** Those two numbers are **attempt 2 (H1)**. In the **adopted**
> configuration they are **+0.106** (La Niña) and **−0.0005** (El Niño) —
> [docs/26](26_phase3_refit.md) Addendum **A.5**. So the figure's rightmost group, not the one
> the sentence describes, is the project's current position: the dry phase is **level with**
> climatology, and the "five times" ratio cannot be formed at all. See the correction in
> **Part 2** for the full table and the wording to use.

**Why:** it shows we scrutinise our own metrics, and it is where the honest statement of the
remaining gap comes from.

---

## Slide 11 — Did repairing the rainfall help?

**Looking at:** signed horizontal bars (attempt 3 minus attempt 2) and a per-gauge scatter.

**Means the design:** a **controlled** comparison — same model, same objective, same gauges,
same window. **Only** the rainfall changed. So any difference is attributable to the rainfall.

**Reading the bars:**
- **PBIAS −4.44 points** — volume bias roughly halved, 8.9 % → 4.4 %. Clear improvement
- **r +0.0033** — timing correlation did not move at all
- **KGE −0.022** — slightly down, because KGE also penalises the accompanying change in α
- **+2 gauges** crossed from useless to useful

**Means scientifically:** volume error and timing error are **independent problems**. We had
been treating "the rainfall is wrong" as one issue; it is two, and fixing one leaves the other
untouched. That is what makes slide 17's ordering evidence-based rather than a guess.

**Why:** we wrote the prediction down before running it, and it came back +0.003. Prediction
followed by confirmation is the strongest form of evidence available here.

**Likely question:** *"So the repair was pointless?"*
> No. It halved the volume bias, removed physically impossible gauges, and — importantly — it
> told us that no amount of *volume* correction will fix the timing. That redirects the whole
> work plan.

---

## Slide 12 — What the model actually produces

**Looking at:** observed (usually black) against simulated (coloured) daily discharge, for
several gauges of very different sizes.

**Means:** this is the raw thing all the metrics summarise. You can see directly where the
model tracks reality and where it does not — typically decent seasonal timing, imperfect peaks.

**The counter-intuitive finding:** the **largest** catchments have the **best** timing
(r ≈ 0.91), because they average over enough area that individual rain-gauge errors cancel.
The 6 gauges above 20,000 km² reach validation KGE **0.712** against **0.433** for the 55
smaller ones.

We had predicted the opposite — big rivers are where our simple routing should be weakest. We
were wrong, and we only found out because we tested the prediction. Their weakness is in peak
**magnitude**, not in **timing**.

**Why:** the most intuitive slide in the deck, and it demonstrates testing an expectation
rather than asserting it.

---

## Slide 13 — The data defect that value screens cannot see

**Looking at:** two panels and a before/after table.

**Means the defect:** rainfall comes from gauges read by human observers. Some report almost
daily, others patchily. We found patchy stations reported **much more rain on average**:

```
reporting > 90 % of days   →   4.4 mm/day
reporting < 50 % of days   →  11.7 mm/day
```

Nearly 3× more rain purely as a function of how often someone wrote something down. That is
not geography — it is a recording artefact. On dry days many observers **wrote nothing**, so a
blank means "zero" sometimes and "unknown" other times. Average only the recorded days and you
average only the rainy ones.

**Why standard checks miss it — the key insight.** Normal quality control asks: is this value
too large? Does it disagree with neighbours? Is it an outlier? **Every one of those looks at
values that are present.** A record that was never written is invisible to all of them, *by
construction*. This is a defect class that an entire family of standard methods cannot detect.

**Means the detector:** for station X, use **only its neighbours' data**. On the days X chose
to report, was it unusually wet at the neighbours? If X reports honestly, those should be
ordinary days, giving ~1.0.

The clever part is that this has a **calibrated null**: on the 89 healthy dense stations it
reads **1.001** — correctly finding no bias where there should be none. That is what makes
**1.777** on the patchy stations trustworthy rather than an arbitrary threshold.

**Means the table:** after repairing 153 stations, the patchy band drops to **1.040**, and the
healthy band **stays at 1.001** — the control proving we did not over-correct and invent dry
days on good stations. Basin rainfall falls 2,174 → 2,036 mm/yr.

**Why:** the most transferable methodological lesson in the deck. Anyone using station data
anywhere has this problem.

**Likely question:** *"How do you know the inferred dry days really were dry?"*
> We check at independent neighbours: on the days we inserted, neighbour wet-day rate was 0.17
> against 0.33 overall. So those days were genuinely much drier than average — though not
> bone dry, which is why we report the corrected basin rainfall as a bounded range rather
> than a single exact figure.

---

## Slide 14 — Verification as a first-class activity

**Looking at:** four findings, a join-integrity figure, and a guarantees box.

**Finding 1, the serious one.** Our rainfall table is ~180 MB (4,018 rows × 8,673 columns).
The standard Python CSV reader returned **1,309 rows** on one call and **3,630** on another,
from a file we then proved complete — **with no error raised**.

Why it is dangerous: the missing rows were always from the **end**, a contiguous prefix. So
the data passed every sanity check — right column count, dates in order, no duplicates, no
calendar gaps. The **only** thing that caught it was an assertion comparing the file's dates
against a period declared separately from two literal dates. Without that one line we would
have calibrated on a third of the data with every diagnostic green.

**Finding 2.** The rainfall interpolation was not **reproducible**: three gauge pairs share
identical coordinates, so which neighbours were used depended on the accidental order of the
columns. Shuffling moved rainfall by up to 20 mm/day in some catchments. Now fixed and
asserted invariant on every run.

**Finding 3.** We reported "132 of 132 climate files present" — that was a count of
**filenames**. One file was internally corrupt at a perfectly plausible 43.7 MB. **A file
listing is not a file check.**

**Finding 4.** Two gauges 5 cm apart in the catalogue were **not** duplicates — they disagree
on 1,000 of 1,470 shared days, so one simply has wrong coordinates. A merge rule based on
distance would have silently destroyed a real measurement.

**Means the guarantees:** water conserved to **10⁻¹⁷** (exact), and two independent
implementations of the routing agreeing **bit for bit**.

**Why:** it demonstrates that our numbers are trustworthy for reasons we can name — the
strongest possible answer to *"how do you know?"*

---

## Slide 15 — The model is at its input's ceiling

**The main scientific result.** Take time here.

**Looking at:** the "skill vs gauge density" figure and a table of correlation values.

**The logic, step by step:**

1. **We could not fix the dry season by tuning.** We swept the groundwater parameter across an
   order of magnitude, the subsurface parameter, channel speed from 0.22 to 2 m/s, and scaled
   all rainfall down by up to 20 %. **Twelve configurations.**
2. **Correlation refused to move** — it stayed between **0.556 and 0.572** in every one. When a
   result is that insensitive to everything you change, it is not a parameter problem.
3. **We measured what the rainfall data itself can do.** Hide one gauge, predict it from the
   others, compare (LOOCV). The rainfall field's own skill: **r ≈ 0.43**.
4. **Our model achieves r ≈ 0.476** — *just above* the quality of its own input.
5. **The physical reason.** Daily rainfall at two gauges 25 km apart correlates only **0.33**.
   Tropical mountain storms are small: one hits a valley and misses the next. Our average gauge
   spacing is **~30 km**. We are trying to reconstruct a field that varies faster than our
   network can sample it.

**Therefore:** the ceiling belongs to the **observing network**, not the model. No parameter
set gets past it.

**Why it matters:** it reframes a weakness as a measurement. Not *"we underperform in the dry
season"* but *"we have quantified the limit of daily rainfall–runoff modelling at ~30 km gauge
spacing in a tropical mountain basin"* — which is transferable to any data-sparse basin, and is
the most publishable thing in the work.

**Likely question:** *"Could you not just interpolate the rainfall better?"*
> Better interpolation cannot invent information that was never sampled. If the field
> decorrelates over 25 km and gauges are 30 km apart, the missing structure is not recoverable
> from those gauges. That is why step 1 on slide 17 is satellite rainfall — a genuinely
> different observation, not a cleverer average of the same points.

---

## Slide 16 — What we cannot yet claim

**Looking at:** a list of limits, and the sediment rating curves.

**Each limit, explained:**

- ~~**Calibration not closed** — three attempts, none meeting every pre-set criterion.~~
  → ⚠ **CORRECTED 2026-08-12: four attempts, and the calibration IS closed** — but *by
  decision, not by passing*. [docs/30](30_phase_c_plan.md) §1: *"**Phase B closes on the
  input-ceiling result, with H2E as the adopted configuration.**"* **The "none meeting every
  criterion" half is still true and still has to be said**:
  [docs/26](26_phase3_refit.md) A.4 — *"**H2E scores 3/9**… Adoption was on the docs/29 rules,
  which H2E passed; **it was never a claim that the pre-registered adequacy criteria were
  met**."*
- **Conventional adequacy not reached** — the usual daily NSE threshold is >0.5; we are
  0.16–0.26. Slide 15 explains why, but it is still true and we say so.
- ~~**The ENSO asymmetry persists** — five times better wet than dry. We aimed to halve that
  ratio and did not.~~
  → ⚠ **CORRECTED 2026-08-12: in the adopted model it is worse than "five times".** Wet
  **+0.106**, dry **−0.0005** ([docs/26](26_phase3_refit.md) Addendum A.5). The dry phase
  matches climatology rather than beating it, so no ratio exists. We aimed to halve the gap
  and did not.
- ~~**Parameters at bounds** — a vegetation coefficient sits at 2.0, beyond any physically
  sensible value. That is compensation, and we think we know for what: our evaporation formula
  throttles evaporation even in moist soil, so the model needs an unrealistic coefficient to
  evaporate enough. A one-function fix, next on the list.~~
  → ⚠ **CORRECTED 2026-08-12: the fix was made and the diagnosis was RIGHT.** Replacing the
  evaporation formula with the FAO-56 threshold form moved the coefficient **off its bound**,
  2.0 → **1.6625**, at no cost in the objective — [docs/29](29_seed_expansion.md) rule (b):
  *"**SUCCESS, all three conditions**… the FAO-56 threshold form releases it at no cost"*, and
  [docs/26](26_phase3_refit.md) A.2: *"confirmed off the rail that held H1 at 98.8 % and H2 at
  93.3 %"*. **The limit itself still stands, with the corrected number:** 1.66 is still beyond
  FAO-56's plausible ≤ 1.2 ([docs/29](29_seed_expansion.md) caveats), and **2 of 10 global /
  3 of 18 dimensions** remain railed in the adopted fit.
- **No per-catchment sediment yield** — our two implementations' drainage areas disagree by
  more than 2× on **36 %** of shared gauges, while their **averages** agree to 1 %. So neither
  network is trustworthy gauge by gauge. Yield is mass **per unit area**, so a 2× area error is
  a 2× yield error. Must be resolved externally before any specific yield is publishable.
- **Celerity is a surrogate** — the fitted channel speed of 0.221 m/s is doing the job of the
  floodplain storage that implementation A does not represent. It cannot be reported as a
  physical velocity.

**Means the figure:** sediment rating curves — fitted relationships between discharge and
sediment load. Median R² ≈ 0.5, i.e. mediocre. A limit on Phase C independent of anything in
the water model.

**Why:** stating limits yourself is what makes the positive claims believable. And every limit
here comes with a measurement, not a hedge.

---

## Slide 17 — Next steps

**Looking at:** a five-step table, plus two panels showing the sediment components exist.

**Why this order — each step is justified by a measurement:**

> **⚠ SUPERSEDED 2026-08-12 — this is no longer a plan. Four of the five steps have been
> executed.** The list is preserved as the delivery-date record; here is what happened, with
> the owning document for each.
>
> 1. **Satellite rainfall merge — DONE, and REJECTED. Twice.** It really was the only measured
>    lever, and it did not work. The correlation gate **passed** (merged r **0.447** against
>    the gauge-only **0.429**); the volume gate **failed** — the merged field is **2,188.5
>    mm/yr**, about **7.5 %** too wet, against a required band of **[2,016.0, 2,056.8]**.
>    ([docs/18](18_hydrology_journal.md) §15: *"**DO NOT ADOPT.**"*) The fix we had diagnosed
>    was then written down as a formal prediction (**H-CHIRPS**,
>    [docs/33](33_c2b_preregistration.md) §1), run — and it changed **nothing**. The thing we
>    thought was missing from the calculation was already **25.9 %** of it, so the re-run came
>    back **bit-for-bit identical** to the run it was meant to repair.
>    [docs/33](33_c2b_preregistration.md) §1: *"The registered intervention turned out to be a
>    **no-op**… so the diagnosed cause in docs/18 §15.3 was **wrong**."*
>    [docs/18](18_hydrology_journal.md) §15.5: *"**no route to a passing volume gate exists
>    inside the merge code.**"*
>    **⇒ The cause of the volume failure is now UNKNOWN.** One hypothesis survives — 139
>    stations that still under-report dry days — but those days *"are not in the record at
>    all"*, so it cannot be tested inside the merge, and it has not been tested anywhere else.
>    **There is no merged rainfall product and none is pending.** *(In this project's
>    vocabulary: there is no "v3" forcing. "v2", the adopted forcing, is the **repaired
>    gauge** field — it is **gauge-only** and contains no satellite data. See
>    `docs/00_INDEX.md` § "Forcing versions — v1 / v2 / v3, stated once".)*
> 2. **Evaporation formula — DONE, and it WORKED.** [docs/29](29_seed_expansion.md) rule (b):
>    *"**SUCCESS, all three conditions**"*. The stuck coefficient came off its bound
>    (2.0 → 1.66). That configuration is the one the project adopted.
> 3. **More search seeds — DONE, and they did NOT separate the two rainfall versions.**
>    [docs/29](29_seed_expansion.md) rule (a): *"**NOT SEPARATED**… Six seeds per cell did not
>    separate the forcings."* Gap **0.009** against a between-seed spread of **0.051**. The
>    comparison is now settled as a negative rather than pending.
> 4. **Catchment areas — STILL OPEN.** Unchanged. The yield embargo stands
>    ([docs/23](23_gauge_geometry.md) §13.2).
> 5. **Then sediment — STARTED.** [docs/30](30_phase_c_plan.md) §1.

1. **Satellite rainfall merge** — the *only* intervention measured capable of moving
   correlation (slide 15), and therefore the dry season. The satellite supplies **spatial
   pattern** and covers the 17 % of the basin with no nearby gauge; the gauges stay in control
   of total **volume** (because slide 11 showed volume is now nearly right and we must not
   break it).
2. **Fix the evaporation formula** — cheap, and should release the stuck parameter (slide 16).
3. **More search seeds** — our two rainfall versions differ by 0.011 on the objective while
   different random seeds differ by 0.019. **The seed noise is larger than the effect**, so
   that comparison is not yet established. More seeds, not a longer search.
4. **Resolve catchment areas** — blocks all yield reporting.
5. **Then sediment.**

**Means the panels:** satellite-based sediment concentration retrieval, and the sediment
transport module on a synthetic test. Phase C is **built and tested** — it waits on data
quality, not on code.

---

## Slide 18 — The question for the advisor

**Looking at:** one question and its two branches.

**Why this is the most important slide:** it is a genuine decision only the advisor can make,
and it changes what work happens next.

> **⚠ SUPERSEDED 2026-08-12 — THE QUESTION WAS ASKED AND THE ADVISOR DECLINED TO ANSWER IT.**
> Do not put it in front of him again. Owner [docs/30](30_phase_c_plan.md), header, quoted:
>
> > "**The advisor was asked the Phase B scope question (docs/24 item 17) and declined to
> > answer — told the team to decide.** This document records the decision and the plan that
> > follows from it."
>
> **What the team decided**, [docs/30](30_phase_c_plan.md) §1: *"**Phase B closes on the
> input-ceiling result, with H2E as the adopted configuration.**"* — i.e. the first branch
> below. The grounds are all measured: parameter headroom exhausted (twelve configurations
> moved El Niño r by less than 0.016), the ceiling belongs to the observing network, and the
> seed expansion settled the last two calibration questions.
>
> **And the second branch's premise no longer holds either.** It says "if conventional
> adequacy is expected, the merge *must* succeed". The merge was tried twice and **failed both
> times** (see the correction at slide 17). So that branch would not have been available.
>
> **Phase B then closed a second time, on separate evidence** —
> [docs/33](33_c2b_preregistration.md) §8, after a pre-registered re-examination of the two
> quantities the sediment model actually consumes. H2E survived both closes.

- **If the ceiling result is an acceptable close** — Phase B can finish on a quantified limit
  whether or not the satellite merge succeeds, and effort moves to sediment.
- **If conventional adequacy is expected** — the merge *must* succeed. If it does not, the
  options are denser rainfall input than IDEAM has, or a reduced target: monthly instead of
  daily, or a few well-gauged sub-basins instead of the whole network.

Both answers are workable. What is not workable is leaving it undecided, because "done" means
different things under each.

---

## Slide 19 — What we have contributed

Backup summary if asked *"so what have you got?"*. Five claims, each traceable to an earlier
slide: two agreeing implementations (6), a mass-conserving calibratable engine (7, 14), the
input ceiling (15), the QC methodology (13), and the audit trail.

---

# Part 4 — The five things to remember if you remember nothing else

1. **Both ENSO years are out-of-sample.** We calibrate only on neutral years, so the headline
   results are predictions, not fits. *(Slide 7)*
2. ~~**We traded 0.029 KGE for a correct groundwater recession** — and the dry season went from
   worse-than-climatology to better. A flattering number from wrong physics is not the better
   model. *(Slide 9)*~~

   → ⚠ **SUPERSEDED 2026-08-12. REMEMBER THIS INSTEAD:**
   **We traded 0.029 KGE for a correct groundwater recession, and we would do it again — a
   flattering number from wrong physics is not the better model. But the dry-season gain that
   came with it did not last: in the model the project actually adopted, the dry El Niño phase
   sits *at* a seasonal climatology, not above it — skill over climatology **−0.0005**, against
   **+0.106** in the wet La Niña year.** *(Slide 9, and the correction in Part 2.)*

   > **Why this was changed.** As written, the struck sentence was the most quotable wrong
   > statement in the deck material, and it sat in the list a briefer is most likely to repeat
   > verbatim. Owner: [docs/26](26_phase3_refit.md) Addendum **A.5**, quoted:
   > *"The deck's slide-9 argument ('the dry phase turns from worse-than-climatology to
   > better') was measured on attempt 1 → attempt 2 and remains true *of that comparison*; it
   > is **not** true of the configuration the project adopted."* … *"**The dry phase in the
   > adopted configuration is at climatology, not above it: −0.0005.**"* The trade itself —
   > 0.029 KGE for a recession of 0.96× instead of 2.98× — is unaffected and stands.
   >
   > A.5 also states the consequence that must travel with it: this is *"the hydrology caveat
   > every Phase C sediment claim inside the El Niño window inherits."*
3. **Repairing the rainfall fixed volume and did not touch timing** — predicted in advance,
   confirmed at +0.003. They are two independent problems. *(Slide 11)*
4. **The model sits just above its input's own skill** (0.476 vs 0.43), and daily rainfall
   decorrelates over 25 km while our gauges are 30 km apart. The ceiling belongs to the
   network, not the model. *(Slide 15)*
5. **Test for absent records, not just bad values.** Standard outlier checks cannot see a
   measurement that was never written down. *(Slide 13)*
