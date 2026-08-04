# 27 — Spoken script for `MGB-SED_Magdalena_FIGURES.pptx`

**Companion document:** `docs/28_presentation_explained.md` explains every term and number
slide by slide, for anyone who has not worked on the project.

**How to use this.** The text in *"quotation marks"* is what to say — written the way you
would speak it, not the way you would write it. `[Square brackets]` are stage directions.
Times are cumulative. Total as written: **~34 minutes**. If you have 25, take the three cuts
marked **[CUT IF SHORT]** and shorten slide 4.

**Three rules for delivery**
1. Never read a number off a slide without saying what it means. "KGE 0.45" means nothing
   to a listener; "about 0.45 on a scale where 1 is perfect" does.
2. When you show a figure, say what the axes are before you say what the result is.
3. Slide 18 is the one you actually want discussed. Do not let slides 1–17 eat its time.

---

## Slide 1 — Title  ·  0:00 → 0:30

> *"Good morning. This is our work on modelling suspended sediment in the Magdalena–Cauca
> basin, comparing a very wet year with a very dry one."*
>
> *"I want to be clear about the scope up front. Today is about the **water** side —
> the hydrology. The sediment module is built, but it is waiting on data quality, so it
> appears only at the end as an outlook."*
>
> *"And this is a progress talk, not a finished result. I will show you three attempts at
> calibrating the hydrological model, what each one measured, and where we now stand — with
> the limits stated as clearly as the successes."*

`[Move on quickly. The title slide should not take a minute.]`

---

## Slide 2 — The question, and why these two years  ·  0:30 → 2:00

> *"The Magdalena–Cauca drains about 257,000 square kilometres of Colombia, and it carries one
> of the highest sediment loads per unit area of any river in the world. That sediment fills
> reservoirs, reshapes the delta, and affects water quality."*
>
> *"How much sediment moves changes a lot from year to year, and the main driver is **ENSO** —
> the El Niño / La Niña cycle in the Pacific. La Niña brings wet years, El Niño brings dry
> ones."*
>
> *"We compare **2011**, a strongly wet La Niña year, with **2015 to 2016**, a dry El Niño
> period."*

`[Point at the left panel.]`

> *"And I want to stress: we did not take those years from the literature. This left panel is
> our own analysis of discharge across the basin, year by year. 2011 stands out at about
> 1.7 standard deviations above normal, and 2015–16 is about one standard deviation below.
> The years chose themselves from our data."*
>
> *"The right panel is the same signal, computed independently by the second half of our
> team, from a different pipeline. Two analyses, same answer."*
>
> *"The gap we are filling: this ENSO–sediment link is well documented **statistically** —
> people have correlated the two. But nobody has reproduced it with a **process-based
> model** that represents the physics across the whole basin. That is what a process model
> adds: it tells you not just that the difference exists, but **where** in the basin it comes
> from, and **why**."*

---

## Slide 3 — Where we are, honestly  ·  2:00 → 3:00

> *"Three phases. Phase A, all the model inputs, is complete. Phase B, the hydrology, is
> calibrated — three attempts — but **not closed**, and that is today's talk. Phase C, the
> sediment, is blocked on the quality of the sediment concentration data on the main stem."*
>
> *"Why in that order? Because the erosion equation we use is driven by **runoff**, not by
> rainfall. Water has to be right first. If we calibrated the sediment parameters on top of
> an uncalibrated water balance, the erosion parameters would just absorb our water errors,
> and we would get plausible-looking numbers that mean nothing."*

`[Point at the map.]`

> *"This is what the hydrology hands to the sediment module — simulated runoff per unit area
> across the basin. Getting this field right is the whole job of Phase B."*

---

## Slide 4 — Preprocessing pipeline  ·  3:00 → 4:30

> *"Before any modelling, we have to turn a digital elevation model into a river network. Four
> steps, left to right."*
>
> *"First, condition the elevation data — fill the artificial pits that would otherwise trap
> water. Second, compute for every cell how much land drains into it; that is what makes the
> river network appear, and you can see it emerge in the second panel. Third, threshold that
> to define the channels. Fourth, cut the basin into small units."*
>
> *"We end with **8,672 units** — we call them **minibacias**, small sub-catchments. Each one
> gets its own water balance."*

`[Point at the bottom-left panel.]`

> *"Inside each minibacia we do not assume one uniform surface. We cross soil texture with
> land cover, which gives **24 combinations** — each behaving differently when it rains. Clay
> under forest does not shed water like sand under pasture."*
>
> *"Bottom right is the accumulated drainage area on a log scale. The single outlet at Calamar
> accumulates the full 257,000 square kilometres, which is the first check that the network
> is connected correctly."*

**[CUT IF SHORT]** — compress this to *"we turn the DEM into 8,672 sub-catchments, each split
into 24 soil-by-land-cover classes"* and move on.

---

## Slide 5 — Spatial discretisation and its verification  ·  4:30 → 6:00

> *"I want to spend thirty seconds on verification, because it is a theme of this talk."*
>
> *"Geometry is easy to get subtly wrong and hard to notice. So we do not just compute the
> drainage areas — we compute them **two independent ways** and compare."*

`[Point at the table, line by line.]`

> *"The area accumulated at the outlet, and the sum of all the individual sub-catchment areas,
> agree to eight decimal places. Zero edges where a downstream catchment is somehow smaller
> than its upstream one, which would be physically impossible. The soil-and-land-cover
> fractions sum to exactly one, to machine precision."*
>
> *"None of that is a result. It is the floor you have to be standing on before any result
> means anything."*

`[Point at the map.]`

> *"And this is one real input: how much water the soil can hold, from Colombian soil survey
> data. Median about 73 millimetres, but ranging from 13 to 255. A nineteen-fold spatial
> range. We could have used one average number for the whole basin — that would have thrown
> away real, measured variation."*

---

## Slide 6 — Two implementations  ·  6:00 → 8:30

> *"Now the piece I am most pleased about, and it needs explaining."*
>
> *"Our team built **two** versions of this model, deliberately."*

`[Point at column A.]`

> *"Implementation A uses simple channel routing. Water moves downstream through a chain of
> storage reservoirs. It is physically crude, but it runs the whole basin for eleven years in
> **twelve seconds**."*

`[Point at column B.]`

> *"Implementation B uses proper hydrodynamics — it solves shallow-water physics, tracks water
> depth, and represents floodplains. That matters here because of the **Depresión
> Momposina**, the huge wetland where the Magdalena and Cauca meet, which stores water for
> weeks. But it costs about **1,500 seconds per run** — twenty-five minutes."*
>
> *"So: A buys **search**, B buys **physics**. To calibrate you need hundreds or thousands of
> runs. On implementation B, the search we ran overnight would have taken **thirteen days**.
> On A it took a few hours."*

`[Point at the callout.]`

> *"And here is the payoff. Both are now calibrated, and they land within about 0.02 of each
> other on our skill metric — from independent code, independent input processing, and
> different physics. That agreement is a genuine cross-check. Neither version alone could
> have told us that."*

`[Point at the convergence figure.]`

> *"This is the search itself. Each line is one optimisation run — four running at once. You
> can see them climbing and flattening out. The flattening is what tells you the search has
> found what it is going to find."*

---

## Slide 7 — Model period and the split  ·  8:30 → 11:00

> *"This slide is the reason you should believe anything I say afterwards. Please stay with me
> for two minutes."*
>
> *"We run 2008 to 2018 — about four thousand days. 2008 is used to warm the model up, and
> we score 2009 to 2018."*
>
> *"Now, the honest problem with calibration: if you tune a model on some data and then report
> how well it does on that same data, you have proved nothing. You have proved you can fit a
> curve."*
>
> *"The standard fix is to hold some data back. We do something stricter, from a 1986 paper
> by Klemeš. **We calibrate only on the neutral years** — the ordinary ones, neither El Niño
> nor La Niña."*
>
> *"Which means both of the years we actually care about, 2011 and 2015–16, are **never seen
> by the calibration**. When I show you how the model does in those years, that is a
> **prediction**, not a fit."*
>
> *"And we check for overfitting directly: the drop in performance from the calibration years
> to the validation years is 0.159 — only 0.011 worse than what an **unfitted** model loses.
> So the fitting is not memorising."*

`[Point at the figure.]`

> *"One more thing on this slide. A model like this carries memory in its soil moisture, so
> the starting condition matters. We tested three deliberately incompatible starting states —
> bone dry, saturated, and equilibrium. By the end of the warm-up year they converge to within
> **0.18 percent** of mean flow. So the answers do not depend on our guess about initial
> conditions."*

---

## Slide 8 — Three calibration attempts  ·  11:00 → 13:30

> *"Now the actual work: three attempts."*
>
> *"First, let me explain the metric, because everything depends on it. **KGE** — Kling-Gupta
> Efficiency. One is perfect. It combines three things: does the model get the **timing** of
> the rises and falls right, does it get the **variability** right, and does it get the
> **total volume** right. Above about 0.5 is generally considered decent for daily river
> flow, which is a hard target."*

`[Point at the blue bars.]`

> *"Attempt one reached 0.450."*

`[Point at the red bars.]`

> *"But we also measured something else, and this is where it gets interesting. When rain
> stops, a river's flow decays. How fast it decays is called the **recession**, and it tells
> you about how water is stored underground. We measured it in the observations: about ten to
> twelve days."*
>
> *"Attempt one's simulated recession was **thirty to forty-five days**. Three to four times
> too slow. The model was getting the right total volume of water, but releasing it far too
> slowly — and no one had checked."*
>
> *"So attempts two and three add a term to the objective that explicitly penalises a wrong
> recession, and attempt three additionally uses a repaired rainfall dataset."*
>
> *"One methodological point: we **wrote down which experiments we would run before running
> them**. Two configurations, two random seeds each, four thousand model evaluations total.
> That matters — if you run twenty variants and report the best one, you have fooled yourself.
> Pre-registering stops that."*

---

## Slide 9 — The central result  ·  13:30 → 16:30

> *"This is the most important slide in the talk."*

`[Point at the green bars.]`

> *"Green is the recession we measured in the real rivers, by period — nine to twelve days."*

`[Red bars.]`

> *"Red is attempt one. Two-point-nine to three-point-nine times too slow."*

`[Navy bars.]`

> *"Navy is attempt two, after we told the objective function to care about recession. Between
> 0.92 and 1.27 times observed. Essentially right."*
>
> *"And here is the trade."*

`[Point at the callout.]`

> *"We **lost** KGE. From 0.450 down to 0.421. About 0.03."*
>
> *"I want to be very deliberate about how I present that, because it would be easy to hide.
> We did not lose skill by accident. We chose it. A model that reproduces the hydrograph well
> but drains groundwater three times too slowly is **getting the right answer for the wrong
> reason** — and it will fail the moment you ask it something new, like a different climate
> period, or feed it into a sediment module."*
>
> *"And we gained something concrete. In the El Niño dry period, attempt one was **worse** than
> a simple seasonal average; attempt two is **better** than it. First time. I will show you
> that on the next slide."*
>
> *"So: three-hundredths of a metric, for physics that is right and a dry season that finally
> works. We would make that trade again."*

---

## Slide 10 — Scoring against a benchmark  ·  16:30 → 18:30

> *"A short methodological slide, because it changed how we read our own results."*
>
> *"We were looking at a metric called NSE for the dry El Niño period, and it was **negative**
> — which is conventionally read as 'the model is worse than just predicting the average'.
> That sounds catastrophic."*
>
> *"Before accepting that, we asked: how would a **perfect seasonal average** score in that
> same window? Something that knows the typical flow for every day of the year and nothing
> else."*
>
> *"It also scored negative. Minus 0.06."*
>
> *"The reason is that NSE compares against the variability **within the window you chose**,
> and the El Niño window happens to have the most variable flows in our whole record. So NSE
> is **not comparable between windows**. About a third of what looked like model failure was
> the measuring stick."*

`[Point at the figure.]`

> *"So we report this instead: how much better than that seasonal climatology is the model, in
> each period. In the wet La Niña year we add about 0.13. In the dry El Niño period, about
> 0.03."*
>
> *"That is still a real and uncomfortable asymmetry — we are five times better at wet than at
> dry. But it is an honest statement of the gap, and it is not 'worse than the mean'."*

---

## Slide 11 — Did repairing the rainfall help?  ·  18:30 → 21:00

> *"Attempt three tested one thing only: does better rainfall data help? Same model, same
> objective, same gauges, same time window — **only** the rainfall changed."*
>
> *"And we wrote down what we expected **before** we ran it. We expected the volume error to
> improve and the timing correlation not to move. Here is what happened."*

`[Point at the bars.]`

> *"Volume bias: from about 8.9 percent down to 4.4 percent. Cut roughly in half."*
>
> *"Correlation: plus **zero-point-zero-zero-three**. Which is nothing."*
>
> *"Two more gauges crossed from useless to useful."*
>
> *"Overall KGE went slightly down, because KGE also penalises the change in variability."*

`[Point at the callout.]`

> *"So the repair fixed **volume** and did not touch **timing**. Exactly as predicted."*
>
> *"That sounds like a small result. It is actually the most useful thing we learned, because
> it tells us these are **two separate problems**. We had been treating 'the rainfall is
> wrong' as one issue. It is two, and fixing one does not touch the other. That is what points
> us at what to do next — which I will come to."*

---

## Slide 12 — What the model actually produces  ·  21:00 → 22:30

> *"Enough metrics. This is what it actually looks like. Observed discharge against simulated,
> for gauges spanning three orders of magnitude in catchment area."*
>
> *"One thing worth pointing out, because it surprised us. The **biggest** catchments have the
> **best** timing — correlation around 0.91. Because they average over so much area that the
> errors in individual rain gauges cancel out."*
>
> *"We had predicted the opposite — we expected the big rivers to be worst, because that is
> where our simple routing is weakest. We were wrong, and we found out because we tested the
> prediction instead of assuming it. Their weakness turns out to be in the **size** of the
> peaks, not in **when** the peaks arrive."*

**[CUT IF SHORT]** — this slide can go, though it is the most intuitive one in the deck.

---

## Slide 13 — The data defect that value screens cannot see  ·  22:30 → 25:00

> *"I want to show you one data problem, because the lesson generalises."*
>
> *"Our rainfall comes from Colombian gauge stations. Some report almost every day, others
> report patchily. We noticed something odd: the patchy stations reported **much higher**
> average rainfall. Stations reporting more than 90 percent of days averaged about 4.4
> millimetres a day. Stations reporting less than half the days averaged **11.7**."*
>
> *"Nearly three times more rain, purely as a function of how often the observer wrote
> something down. That is not geography."*
>
> *"What is happening: on dry days, some observers simply **wrote nothing**. So a blank does
> not mean 'unknown' — it often means zero. If you average only the days that were recorded,
> you systematically average only the rainy ones."*
>
> *"Now here is the part I want you to take away. Every standard quality check looks at the
> **values that are there** — is this number too big, is it an outlier, does it agree with
> the neighbours. **None of those can see a record that was never written.** The defect is
> invisible by construction to the entire class of checks people normally run."*
>
> *"What worked was a test built only from the **neighbouring** stations' data: on the days
> station X chose to report, was it raining at its neighbours? If X reports honestly, that
> should be an ordinary day. We calibrated it on the healthy dense stations, where it reads
> 1.001 — correctly finding no bias. On the patchy stations it read 1.777."*

`[Point at the table.]`

> *"After repairing 153 stations, the patchy band comes down to 1.040, and — this is the
> control that matters — the healthy band **stays** at 1.001. So we did not over-correct and
> invent dry days on good stations."*
>
> *"Basin rainfall dropped from about 2,174 to 2,036 millimetres a year. A six percent
> correction, but on a quantity that drives everything downstream."*

---

## Slide 14 — Verification as a first-class activity  ·  25:00 → 27:00

> *"Four things we found only by running the code. I will do the first one properly and name
> the others."*
>
> *"Our rainfall table is about 180 megabytes — four thousand rows by eight thousand columns.
> We asked the standard Python library to read it. On one call it returned **1,309 rows**. On
> another call, **3,630**. From a file we then proved was complete. With **no error message**."*
>
> *"And the cruel part: the missing rows were always from the **end**. So the data looked
> perfect. Correct number of columns, dates in order, no duplicates, no gaps in the calendar.
> Every sanity check we had would pass."*
>
> *"The only thing that caught it was an assertion comparing the dates in the file against a
> period we had **declared separately, from two literal dates**. Without that one line, we
> would have calibrated this entire model on about a third of the data, and every diagnostic
> would have been green."*
>
> *"Briefly, the other three. Our rainfall interpolation was not **reproducible** — three
> stations share identical coordinates, so which neighbours got used depended on the order
> the columns happened to be in; shuffling it moved rainfall by up to 20 millimetres a day in
> some catchments. We reported '132 of 132 climate files present' — that was a count of
> **filenames**; one file was internally corrupt at a perfectly plausible size. And two
> stations five centimetres apart in the catalogue turned out **not** to be duplicates — they
> disagree on a thousand days — so a rule based on distance would have silently destroyed a
> real measurement."*

`[Point at the callout.]`

> *"Underneath all of it, two guarantees that run on every single execution: water is
> conserved to seventeen decimal places, and two completely independent implementations of the
> routing agree **exactly** — bit for bit."*

---

## Slide 15 — The model is at its input's ceiling  ·  27:00 → 30:00

> *"This is our main scientific result, and it took us a while to see it."*
>
> *"We could not get the dry El Niño period to work. So we tested the obvious explanations. We
> swept the groundwater parameter across an order of magnitude. The subsurface parameter.
> Channel speed, from 0.22 to 2 metres per second. We even scaled all the rainfall down by
> twenty percent."*
>
> *"**Twelve** different configurations. And the timing correlation stayed between 0.556 and
> 0.572 in every single one."*
>
> *"That flatness is the finding. When a result refuses to move no matter what you change,
> you are not looking at a parameter problem."*

`[Point at the table.]`

> *"So we measured what the rainfall data itself is capable of. We hid each gauge in turn,
> predicted its rainfall from its neighbours, and checked. The rainfall field's own skill is
> about **0.43**."*
>
> *"Our model achieves **0.476**."*
>
> *"We are sitting just above the quality of the data we feed it. There is no parameter set
> that gets past that."*
>
> *"And the reason is physical. Look at the bottom rows. Daily rainfall at two gauges 25
> kilometres apart correlates at only **0.33**. Tropical mountain rain is spatially patchy —
> a storm hits one valley and misses the next. Our average gauge spacing is about 30
> kilometres. So we are trying to reconstruct a field that decorrelates faster than our
> network can sample it."*
>
> *"The ceiling is a property of the **observing network**, not of our model. And that
> reframes everything: it is not that we underperform in the dry season. It is that we have
> **measured the limit** of what daily rainfall–runoff modelling can do at this gauge density
> — which is a result other people in data-sparse basins can use."*

---

## Slide 16 — What we cannot yet claim  ·  30:00 → 32:00

> *"I want to state the limits myself rather than have them found."*
>
> *"The calibration is **not closed**. Three attempts, none meeting every criterion we set in
> advance."*
>
> *"We do not reach the conventional adequacy threshold — the usual benchmark for daily NSE is
> above 0.5, and we are between 0.16 and 0.26. Slide 15 explains why, but it is still true."*
>
> *"The ENSO asymmetry persists. We are about five times better in the wet phase than the dry
> phase. We set out to halve that ratio. We have not."*
>
> *"Two or three parameters are still pressed against their allowed limits — in particular a
> vegetation coefficient sitting at 2.0, which is beyond any physically sensible value. That
> is the model compensating for something. We think we know what: our evaporation formula
> throttles evaporation even when soil is quite wet, and doubling that coefficient is exactly
> the compensation that implies. It is a one-function fix and it is next on the list."*
>
> *"And an important one for Phase C: we **cannot publish sediment yield per catchment**. Our
> two implementations disagree by more than a factor of two on the catchment area for
> **36 percent** of shared gauges — while their averages agree to one percent. So neither
> drainage network is trustworthy gauge by gauge. And since yield is mass **per unit area**, a
> factor-of-two area error is a factor-of-two yield error. We have to resolve that against an
> external source before any specific yield is reportable."*

---

## Slide 17 — Next steps  ·  32:00 → 33:00

> *"Five steps, and the order is set by the measurements, not by preference."*
>
> *"One: merge satellite rainfall with our repaired gauges. This is the **only** thing we have
> measured to be capable of moving the timing correlation — and therefore the dry season. The
> satellite gives us spatial pattern and covers the seventeen percent of the basin with no
> nearby gauge; we keep the gauges in control of the total volume."*
>
> *"Two: fix the evaporation formula. Cheap, and it should release that stuck parameter."*
>
> *"Three: more random seeds, because our two rainfall versions differ by less than the
> variation between seeds — so that comparison is not yet established."*
>
> *"Four: resolve the catchment areas."*
>
> *"Five: then sediment."*

`[Point at the two panels.]

> *"And to be clear that Phase C is not vapour: the sediment retrieval from satellite imagery
> and the sediment transport module are both built and tested. They are waiting on data
> quality, not on code."*

---

## Slide 18 — The question for you  ·  33:00 → 34:00  ·  **THEN STOP AND DISCUSS**

> *"I would like to end with a question, because your answer changes what we do next."*
>
> *"Is the ceiling result on slide 15 an acceptable way to **close** the hydrological phase?"*
>
> *"If yes — then we can finish Phase B on a quantified limit, whether or not the satellite
> merge works, and move to sediment."*
>
> *"If no — if you expect us to reach the conventional adequacy threshold — then the satellite
> merge has to succeed. And if it does not, we would need either denser rainfall input than
> IDEAM has, or a reduced target: monthly instead of daily, or a few well-gauged sub-basins
> instead of the whole network."*
>
> *"Either answer is workable. But it changes what 'done' means, so it is the most useful
> thing we can settle today."*

`[Stop. Let the discussion happen. Slide 19 is a backup for the summary if he asks
"so what have you got?" — otherwise you may never need it.]`

---

## Slide 19 — What we have contributed  ·  backup only

> *"Briefly: the first application of this model family to the Magdalena, in two independent
> implementations that agree; a water-conserving, reproducible engine fast enough to actually
> calibrate; a measured ceiling on what is achievable at this gauge density; and a
> quality-control method for Colombian station data that catches a defect the standard checks
> cannot see."*

---

## Anticipated questions

**"Why is the KGE only 0.45? That seems low."**
> *"Two reasons, and the second is the real one. First, this is **daily** flow, which is much
> harder than monthly — most published thresholds are for monthly. Second, and more
> importantly, we have measured the ceiling: the rainfall data's own skill is 0.43 and we
> achieve 0.476. We are already above our input. No parameter set beats that, so the honest
> next step is better rainfall, not more tuning."*

**"Why not just use the model with the better physics?"**
> *"We do — it is calibrated too, at 0.329, and it is what we will use for floodplain
> processes. But it costs twenty-five minutes per run, so the search we did overnight would
> take thirteen days on it. We need both: one to find the parameters, one to represent the
> physics."*

**"Are you sure the dry-season problem is the rainfall and not the model?"**
> *"As sure as we can be from measurement. We tested twelve parameter configurations spanning
> more than an order of magnitude on three different parameters, and the correlation moved by
> less than 0.02 in all of them. Then we measured the rainfall field's own skill independently
> and found the model sitting just above it. We also tested three specific explanations for
> the dry-season failure — and all three were refuted, one of them backwards from what we had
> assumed."*

**"What happened to the sediment?"**
> *"The module is built and tested; the satellite retrieval works. It is blocked on two data
> issues: the concentration measurements on the main stem, and the catchment-area disagreement
> on slide 16. Both are data problems, not modelling problems, and we would rather report no
> yield than a yield with a factor-of-two area error in it."*

**"Is 6 % a big correction to the rainfall?"**
> *"On the basin average, it sounds modest. But it cut the volume bias in our discharge by
> nearly half, and it took the number of physically impossible gauges — where the observed
> river carries less water than the rainfall implies — from 18 down to 14. And locally the
> correction is much larger than 6 %; it is concentrated on 153 specific stations."*

**"Who did what?"**
> *"We are three, and the work is joint. The two model implementations are two arms of one
> project — deliberately, so we would have one version fast enough to calibrate and one with
> the physics we eventually need. Their agreement to within 0.02 is a result we could only get
> by having both."*
