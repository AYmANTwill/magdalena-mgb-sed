# 59 — The cross-implementation comparison: **INDEPENDENT IMPLEMENTATION, NOT INDEPENDENT DATA**

**Written 2026-08-13** by the `x59-write` agent (process record:
`docs/agents/journal_x59-write.md`), synthesising four read-only measurement passes
(`docs/agents/journal_x59-overlap.md`, `journal_x59-bridge.md`, `journal_x59-inputs.md`,
`journal_x59-theirnumbers.md`) **and, overriding them where they conflict, the counterpart author's
own written answers and data bundle of 2026-08-13** (`data/raw/colleague_share/MANIFEST.md`,
`ANSWERS_C1_C2_C3.md`, `input_hashes.txt`).

A second implementation of MGB-SED on **this basin** exists:
**`github.com/yben409/simulating-suspended-sediment-transport` @ `d055561` (2026-08-03)**, hereafter
**R2** (this project is **R1**). It is the first time this project has had an external
implementation to check itself against. This document compares the two and records exactly what the
comparison establishes and at what grade.

**This document edits nothing.** `docs/34`, `docs/41`, `docs/45`, `docs/55`, `docs/56`, `docs/57`
and every frozen artifact were **read and not written**; what this comparison owes to their owners
is recorded in **§10**, not enacted here. R2's clone was **read-only throughout**; nothing in it was
executed and no git command was run in either repository (**§9**).

**A note on labels.** R2 is competent work by a colleague. It holds out both ENSO windows by name,
it cites the same published bar and the same no-skill benchmark this project uses, **it documents
its own collinearity in its own shipped output file**, and — between the four measurement passes and
this writing — **it found and reported a defect in its own simulated concentration that invalidates
its own published sediment score** (§3.1). Three of R1's own premises about R2 turned out to be
wrong and are corrected here in the body, not in a footnote (§1.3). Where R1 is the weaker party
this document says so. The reader should be able to tell which project is which only from the
labels.

---

## 0 — THE PIN. This document is a snapshot, and it says so before it says anything else.

Every R2 number below is pinned to **commit `d055561843d437419cc13d9fcbc45eefb0a2ffa9`
(2026-08-03)**, whose complete history is archived in this repository at
`data/raw/refs/yben409_sediment_repo.bundle`, **sha256
`adf7a1d1bf21d62057257de14bc8adf0584facfa1e37cfe1f5b7afafb551ca9e`** (verified by this writer this
session), plus the 2026-08-13 bundle `magdalena_share_for_colleague.zip` (306,200,202 bytes) whose
23 member hashes are listed in `data/raw/colleague_share/input_hashes.txt`.

**And the load convention, declared once for every R1 EROSION-TOTAL number in this document**
(added 2026-08-19; house rule from `docs/37` A2 — never a load without its convention *and* its
`cp_revision`): every R1 basin or sub-basin erosion **total** below (the 299.54 Mt/yr figure and the
199.29 / 66.53 % partition of it, §6.7 and §7.4) is **gross *hillslope* erosion** at
`cp_revision='cited_central_2026_08_11'`, `volume_convention='williams_m3'`,
`k_unit_system='us_customary'`, with **α and β unfitted** — so it is a **lower bound**, not a
delivered sediment yield. The superseded `cp_revision='prior_2026_08_11'` basin total
(~~248.73 Mt/yr~~) is shown for the audit trail and is **not** quoted as current. This declaration
does not reach the *observed* or *modelled-flux* numbers in §6, which carry their own units and
scopes where they appear. The `docs/23` §13.2 yield embargo is separately restated in §9.

**R2's counterpart numbers are expected to change, and its own manifest says so:**

> *"Withheld on purpose: a recalibration is running right now and those files are mid-rewrite.
> Sending them would hand you numbers about to be superseded. Specifically, Stage 1 hydrology was
> just refitted under a new objective and Stage 2 is being rerun on top of it."*
> — `data/raw/colleague_share/MANIFEST.md`, on `stage1_*` / `stage2_*`

Their re-run already reports stage 3 finding **3 rules** and improving **+0.068 → +0.087**, which
does not match the committed `0.05461202762457862` at all. **Anyone quoting a number from this
document must quote the commit and the date with it.** The bundle and the git archive are what keep
this document reproducible after their repository moves on.

---

> ## THE VERDICT
>
> **R2 is an INDEPENDENT IMPLEMENTATION. R2 is NOT INDEPENDENT DATA.** Both halves are measured,
> and the second half is the one that governs how this comparison may be used.
>
> **Independent implementation — grade DERIVED.** R2 is a separate codebase (`mgbsed`) with a
> separate hydraulic model (local-inertial routing, Bates et al. 2010, with 20-level floodplain
> level–volume–area curves), a separate sediment parameterisation (MUSLE with `alpha`, `beta`,
> `alpha_tc`, `c_mult`), a separate objective (median KGE on **log SSC concentration, mg/L**), a
> separate catchment discretisation (**7,929** unit catchments on a **184 m** routing grid, against
> our 8,672 minibacias), **LS2D computed on that routing grid deliberately** (against our native
> 90 m `buarque_2015_dg`), a separate HRU scheme (**12** = 3 texture × 4 cover, against our 24 = 3
> soil × 8 land), a separate rainfall field (**gauge–CHIRPS merge**, basin mean **1,965 mm/yr**,
> against our gauge-only IDW), a separate ET formulation (per-HRU Penman–Monteith, against our
> FAO-56 reference × `kc_mult`), a separate C table, and a separately chosen differential split
> (fit 2013–14; hold out 2011 and 2015–2017).
>
> **Not independent data — grade DERIVED, and this must be stated in these words wherever the
> comparison is quoted.** R2's observation sets are **strict subsets of ours**: **21 of 21** of its
> SSC calibration stations and **13 of 13** of its validation stations lie inside our 79-station
> SSC archive, and **90 of 90** of its discharge gauges lie inside our 192 — containment
> **1.000** in all three cases, with **zero** stations of theirs that we lack. Its ENSO windows
> **nest** with ours (both our La Niña windows 100 % inside theirs; their El Niño window 100 %
> inside our P-EN and 100 % containing our S-EN; **0 days** of cross-phase leakage). Its raw
> precipitation input is the same 294-station / **686,752**-station-day IDEAM DHIME export we
> shipped. And the strongest single item, measured by this writer this session and **not** by
> metadata agreement: **our `data/processed/minibacia_soil_params.csv` is BYTE-IDENTICAL to the
> soil/K product R2 declares it runs on** — sha256
> `6e5940ecdbd06c8b89b09e9134cbe6586933ff9c6971e896feb9e85b19ae38b1` on both sides (§5.1).
> **Which project supplied the shared data is UNRESOLVED and this document asserts no direction.**
>
> **Therefore the strongest honest sentence available is:** *R2 is a second, independently
> implemented model reaching a concordant direction on **largely the same observations** — a check
> on our implementation and our parameterisation, not on our data.* The word **replication** is
> admissible only as **METHODOLOGICAL replication**, never bare, and never as "independent
> replication". Every concordance below inherits every shared-data failure mode: a common IDEAM
> DHIME archive, a common gauge network, common ERA5-Land, a common soil/K table. **If those
> observations carry a systematic ENSO artifact, both projects reproduce it and neither detects it.**
>
> **THE SCORE COMPARISON IS VOID. No ranking of the two models exists, and none may be printed.**
> R2 found and fixed a defect in its own simulated concentration: SSC was read from the mass left in
> a reach *after* the step's export instead of from the flux, so any reach exporting its whole
> contents in one step reported **exactly 0.00 mg/L** — **74 % of 7,929 reaches** at a daily step,
> and **46 of 57 gauged reaches biased low**. Their words: ***"Any pre-fix SSC comparison against us
> is invalid."*** Their committed median KGE_log `0.05461202762457862` was therefore computed on
> **defective simulated SSC**, and it must not be set beside our **−0.118** (est. a) / **+0.139**
> (est. b) in any table, sentence or figure. **No grade is admissible for the comparison** — not
> CONSISTENT, not INCONSISTENT. Independently of the defect the two numbers were never the same
> measurement (concentration vs flux, 21 vs 8 stations, 4 vs 2 free parameters, 730 vs 1,096 days),
> so the defect removes a comparison that was already inadmissible (§3).
>
> **THE CENTRAL RESULT — non-identifiability — splits in two, and only one leg survives.**
> The **algebraic leg SURVIVES and is bug-independent**: `alpha` and `c_mult` enter MUSLE
> identically, so only their product can be identified — a property of the code, unaffected by any
> defect in the simulated series. R2 states it in its own shipped artifact, unprompted:
> ***"MUSLE is linear in both alpha and the C multiplier; only their product is identifiable from
> these data."*** R1 reached the same conclusion analytically: the design matrix of
> **Π = α · f_vol · f_K · f_LS · C_mult · P · FG** has **condition number `inf`**, exactly singular
> (`docs/42` §3.1). **Grade: DERIVED (R1 leg) + IDENTIFIED (R2 leg).** The **empirical leg is
> SUSPENDED**: the demonstration that `alpha × c_mult` moves ×2.0611616793829812 while the median
> score moves +0.004409952544391804 rests on **pre-fix scores** and must be re-run before it may be
> presented as a measured demonstration. It is recorded as **owed**, not as evidence (§4.3). R1's
> own analytic route is untouched.
>
> **What the comparison narrows.** Genuinely shared and therefore not exonerated by any
> code-difference argument: the **DEM archive**, the **domain**, the **WorldCover raster**, the
> **IDEAM gauge network as an observation set**, **ERA5-Land**, and — newly, at hash level — the
> **soil/K product**. Of the four C4.3 over-production suspects named in `docs/35` §6.1,
> **`K` is now the one the argument reaches** (one input, byte-identical, two implementations) and
> **`Qsur`, `C` and `LS` are NOT narrowed**, because R2's forcing construction, C table and LS all
> differ from ours — LS on a 184 m routing grid *by design*, `Qsur` from a CHIRPS merge landing
> 3.5 % below our like-for-like basin mean (§5.4). The narrowing is *narrower than it looked before
> the bundle arrived on three rows and wider on one*.
>
> **What the comparison does NOT establish.** It does not rank the two models (§3). It does not
> validate either C factor, either LS level, either rainfall field, our `f_LS` = 0.25146, or the
> satellite route. It does not locate the over-production in three of its four suspects. It does not
> show either model is wrong.

---

## 1 — What was compared, on what evidence, and what changed after the measurements

### 1.1 The evidence base, in two tiers

| tier | source | what it is |
|---|---|---|
| **A** | `docs/agents/journal_x59-{overlap,bridge,inputs,theirnumbers}.md` (M1–M4) | four read-only measurement passes over R2's **committed** `config/`, `scripts/`, `src/`, `outputs/`, `tests/` at `d055561`, plus recomputation on **our** data |
| **B** | `data/raw/colleague_share/{MANIFEST.md,ANSWERS_C1_C2_C3.md,input_hashes.txt}` (2026-08-13) | **the counterpart author's own account of their own code, with `file:line` citations** |

**Tier B overrides Tier A wherever they conflict**, and it did so on four substantive points
(§1.3). This is not a courtesy: an author reading their own source with line numbers beats an
external code read of a repository whose data is absent.

| pass | what it measured |
|---|---|
| **M1** overlap | station-set containment, window nesting, derived-input metadata identity |
| **M2** bridge | whether R2's concentration × discharge marginals can be bridged to our flux contrast |
| **M3** inputs | which inputs are genuinely shared vs merely the same agency or the same product |
| **M4** their numbers | re-derivation of every R2 figure from R2's committed artifacts, plus a code read of their objective |

### 1.2 What is, and is not, readable on this disk

R2's raw data is gitignored and **absent from the clone** — verified by listing: `data/`,
`data_Final/`, `data_chirps/` and `data precip` are all absent, and their `.gitignore` documents
15 GB + 7.5 GB obtained from a shared drive. **Nothing in R2 was re-executed**, and every R2 figure
below is recomputed **from committed CSV/JSON artifacts** plus a read of their source or of their
written answers.

And the bundle's **data** files are likewise not on this disk. `ls -la data/raw/colleague_share/`
returns exactly **three** files — `MANIFEST.md`, `ANSWERS_C1_C2_C3.md`, `input_hashes.txt`. The
**20 data files** enumerated in `input_hashes.txt` (Tiers 1–5: the observed SSC and Q series and
station tables, `basin_magdalena.pkl`, `minibacia_soil_params.csv`, the two forcing parquets, the
four retrieval models, the five scripts and three configs) were **not extracted into this
repository**, and no bundle archive is present under `data/raw/`. **So every claim in this document
about a bundle data file rests on the manifest text or on a hash, never on a read of the file** —
with one exception, which is the one that matters most (§5.1).

### 1.3 Four framings of R1's brief that were WRONG, corrected here in the body

Recorded up front so no reader carries them forward. The first three are R1's errors about R2; all
four were caught by Tier B or by M4's code read, none by wishful reading.

| # | R1 believed | measured / stated by the author | where |
|---|---|---|---|
| **1** | R2 **runs on the unrepaired, zero-suppressed precipitation** we shipped | **FALSE.** *"No `precip_gauges_daily_qc.csv` exists anywhere in the repo, so no repaired file was bypassed."* Their QC runs **in-script** (`scripts/15_build_forcing_v2.py:52-108`): gauges reporting on < 80 % of days dropped (`:80-93`), no-coordinate records dropped (`:74-79`), abort under 20 surviving gauges (`:95-99`). And their rainfall is a **gauge–CHIRPS merge**, not raw IDW. Basin mean **1,965 mm/yr** | §5.5 |
| **2** | their ENSO station counts are **35/27** SSC and **108/93** Q | those are **window-specific** counts inside `enso_summary.csv`. Their universe is **SSC 59 total / 57 plausible / 2 rejected** and **discharge 118 / 114 / 4**. Their **21** = SSC stations with **≥ 30 obs days inside 2013-01-01…2014-12-31**; their **90** = discharge gauges with **≥ 180 overlapping in-window days** | §6.2 |
| **3** | their terrain **is** our terrain | **FALSE.** `basin_magdalena.pkl`: **7,929 unit catchments, 184 m routing grid, LS2D computed on the routing grid deliberately**, floodplain level–volume–area curves, **12** HRU fractions — against our 8,672 minibacias, native-90 m LS, 24 URH types | §5.2 |
| **4** | their marginals' product **brackets** our contrast | **NOT COMPARABLE** — unpaired marginals from different station sets over unequal windows; the bracket argument is **withdrawn** | §6.4 |

And two framings of the brief that M4's code read corrected:

| # | brief said | measured |
|---|---|---|
| 5 | their `kge_log` uses **ε = 1 % of mean(obs)** | **ε = max(median(obs) × 1e-3, 1e-6)**, computed inline in `scripts/21_calibrate_sediment.py`; the 1 %-of-mean default in `metrics.py` did not produce the reported column |
| 6 | they fitted a **transport-capacity / delivery-ratio knob we refuse to fit** | **FALSE.** `alpha_tc` is SWAT's rainfall-intensity fraction inside the MUSLE peak-flow term, `qpeak = alpha_tc · Qsur · A / (3.6 · tconc)`; their deposition is physical (Stokes settling) and their only delivery multiplier `gamma` is **pinned at 1.0**. **Neither project fitted a delivery ratio** |

Item 6 is the one that mattered most for tone: it would have read as a criticism of R2 and it is
simply not true. Item 1 is the one that mattered most for fairness: R1 was about to publish, as a
defect of R2's, something R2 had diagnosed and mitigated independently — and which R2 then improved
on by asking us for our statistic (§8.4).

---

## 2 — The two configurations, side by side

| | **R1 — this project** | **R2 — `yben409/…` @ `d055561`** |
|---|---|---|
| **variable scored** | sediment **FLUX**, t/day | SSC **CONCENTRATION**, mg/L, at a reach |
| **estimator of the observation** | (a) paired sample-day flux `Q·C·0.0864`; (b) rating-curve flux, Duan-corrected (`docs/34` §1.4–§1.5) | observed daily mean concentration (DHIME variable `CM`) |
| **transform** | `KGE_ln` — KGE on log flux | KGE on log concentration, **ε = max(median(obs)·1e-3, 1e-6)** |
| **aggregation** | **median** over the admissible CAL stations (`F_report`, `docs/45` §302) | **median** over stations — and see their own warning, §3.4 |
| **station universe → admissible** | 79 archived → **18 usable** (6 usable + 12 usable-with-caveat), `docs/32` | **59** archived → **57 plausible** (25 `discharge_validated` + 32 `nearest_centroid`, reach ≥ 20 km², snap ≤ 15 km), MANIFEST A2 |
| **stations in the score** | **8** (CAL-8; `docs/45` §3.4) | **21** (main) / **13** (validation) — those of the 57 with **≥ 30 obs days in-window** |
| **fit window** | **2012-01-01 … 2014-12-31**, 1,096 d (`docs/45` §3.5) | **2013-01-01 … 2014-12-31**, 730 d — a strict subset of ours |
| **held-out windows** | ENSO windows untouched by the fit; C5 is the out-of-sample application (`docs/56`) | *"2011 (La Niña) and 2015-2017 (El Niño) were not used"* — their own words, in the shipped JSON |
| **free parameters, count** | **2** — α, β (LS, C, K, `f_vol`, P, FG **fixed, not fitted**; `docs/45` §2.3) | **4** — `alpha`, `beta`, `alpha_tc`, `c_mult`; Monte Carlo, 500 trials, `default_rng(42)` |
| **search box** | α ∈ **[2.0, 30.0]** log-spaced; β under the G2.3 gate | α log-U[0.02, 200]; β U[0.25, 0.85]; `alpha_tc` U[0.15, 0.85]; `c_mult` log-U[0.02, 20] |
| **transport-capacity / delivery-ratio term FITTED?** | **NO.** `k_dep` default **0.0** (`src/mgb_transport.py`:521, verified this session); SDR = 1.0 asserted as a claim (`docs/45` §2.3, `docs/42` G5) | **NO.** `alpha_tc` is a rainfall-intensity fraction, not a capacity limiter; deposition is Stokes settling; `gamma` pinned **1.0** |
| **rule set / trigger mechanism** | **NONE EXISTS** — verified this session (§8.3) | `TriggerSet`, per-domain strength rules; committed run has `stage3_trigger_rules: []`, re-run finds **3** |
| **fitted values** | **NOT ADOPTED — RAILED.** In-box optimum at the **box floor** α = 2.0, β 0.60; unconstrained optimum α ≈ 0.48, below the floor (`docs/55` §1–§2) | `alpha` **55.40533705803028**, `beta` **0.3980082263356884**, `alpha_tc` **0.6174944111935904**, `c_mult` **0.04887856036752898** — all four **interior**, nothing on a rail |
| **median score reported** | `F_report` **−0.118** (est. a) / **+0.139** (est. b) | `stage2_median_kge_log` **0.05461202762457862** (21 st) / **0.05902198016897042** (13 st) — **both computed on defective simulated SSC; see §3.1. Superseded and mid-rewrite (§0)** |
| **the bar** | **[−0.26, 0.44]**, Fagundes (2018) §6.3.1 (`docs/45` §84) | **the same bar**, cited in `src/mgbsed/calibration/metrics.py` L7 as *"the KGE range quoted in its conclusions (−0.26 to 0.44)"* |
| **no-skill benchmark** | mean predictor scores **KGE = 1 − √2 = −0.414** (`docs/45` §311) | **the same benchmark**, `metrics.py` L53–54: *"KGE = −0.41, not 0, is the 'mean of observations' benchmark"* |

**Both projects cite the same two published anchors, independently.** That is a real convergence
and it survives everything else in this document: the two projects agree on *what would count as
skill* before they disagree about anything else. It is also the only row of this table on which a
comparison of numbers would have been admissible if the numbers had been sound.

### 2.1 Fitted position inside their own box, for completeness

`alpha` 0.861, `beta` 0.247, `alpha_tc` 0.668, `c_mult` 0.129 of the box range (main); 0.921 /
0.166 / 0.285 / 0.154 (validation). **No rail.** Their trial 0 is the Williams default set
(11.8, 0.56, 0.5, 1.0) and scores **−0.304786553973932**. This is a fact about their search
geometry and it survives §3.1, because a rail is a property of the box and the objective surface,
not of the level of the score. It is the input to §3.5.

---

## 3 — The score comparison: **VOID**

### 3.1 Why it is void, in their words

Between the four measurement passes and this writing, R2 found and fixed a defect in its own
simulated concentration. From `data/raw/colleague_share/MANIFEST.md`:

> *"We just fixed an SSC reporting defect. Concentration was taken from the mass left in a reach
> **after** the step's export rather than from the flux, so any reach exporting its whole contents in
> one step reported exactly 0.00 mg/L — **74 % of 7,929 reaches** at a daily step, and **46 of 57
> gauged reaches were biased low**. Now reported as flux-weighted `SSC = Qss/Q`. **Any pre-fix SSC
> comparison against us is invalid.**"*

Three consequences, and the first is absolute:

1. **`0.05461202762457862` must not be compared to R1's `−0.118` / `+0.139`.** Not in a table, not
   in a sentence, not in a figure, not with a caveat. The quantity on the left was computed on a
   simulated series that reported zero concentration in three of four reaches. **No grade applies to
   the comparison** — not CONSISTENT, not INCONSISTENT, not "coarser". **VOID** is the entire
   finding, and any statement that either project scores better is unsupported.
2. **It explains a degenerate row M4 measured and could not explain.** Their
   `stage2_best_station_metrics.csv` carries station `0021217250` with `sim_mean` **exactly 0.0**,
   ratio 0, PBIAS −100 %, `kge_log` −2.281251 over 472 paired days — which their README lists as
   *"Open bug … simulates exactly 0.00 mg/L … Unexplained."* It is now explained, by them, as an
   instance of the fixed defect. Excluding that one station moved their median by **+0.0032**; the
   defect touched **46 of 57** gauged reaches, so the true correction is not bounded by that figure.
3. **The direction of the bias is stated, and it does not help R1.** 46 of 57 gauged reaches were
   biased **low**, so the post-fix score is not predictable in sign from the pre-fix score, and R1
   has no basis for guessing it. **This document guesses nothing.**

**Independently of the defect, the comparison was already inadmissible**, and this is worth keeping
because it is the part that will still be true after their re-run lands. `+0.0546` and
`−0.118` / `+0.139` differ in at least five ways at once:

1. **Different quantity.** Concentration (mg/L) vs flux (t/day). Flux is `Q × C × 0.0864`, so a flux
   score is jointly a hydrology score; a concentration score is not. These are not two estimates of
   one skill.
2. **Different station sets** — 21 vs 8, with 6 in common.
3. **Different free-parameter counts** — 4 vs 2, unpenalised in both cases.
4. **Different windows** — 730 d vs 1,096 d.
5. **Different ε in the log transform** — 0.1 % of the median vs our registered `KGE_ln` convention.

And a ranking would additionally require both numbers to be **adoptions**, and neither is: R1's is
read at a **railed floor** and is explicitly `EXPLORATORY, not adopted` (`docs/55` §1), and R2
labels its own stage-2 numbers *"Not part of the current presentation. Recorded for completeness."*
**Treating either as a headline claim misrepresents its owner.**

### 3.2 The one number that is NOT a sediment score, recorded because it is the one most likely to be misread

**`+0.32933947922532514` is a DISCHARGE median KGE_log over 90 gauges, not a sediment result.**
`scripts/18_calibrate_hydrology.py`'s `score_discharge` reads `result.q_m3s[:, reach]` against
observed discharge and writes an `area_km2` column. Anyone who has heard "their model scores about
0.2 to 0.33" has heard a hydrology number. Two details carried from M4:

- `stage1_hydrology_params.json`'s `note` says *"area-sqrt-weighted mean"*, and `score_discharge`
  does return `np.average(..., weights=sqrt(area))` — but line 212 maximises
  `table.attrs["median_kge_log"]`. The **number is the median**; the note is stale. A documentation
  slip, reported for accuracy. **Their own fix for this class of problem is already in:** *"The saved
  JSON now records the objective by name plus every metric, so a switch of objective can no longer
  silently relabel one number as another"* (`ANSWERS_C1_C2_C3.md` C1).
- Their `outputs/calibration_fast{,_b}/` cells score 0.368 / 0.372 on the same 90 gauges but declare
  `"routing": "linear_reservoir (NOT hydrodynamic)"`. Stage 2 uses the script-18 hydrodynamic
  multipliers bit-identically, so **0.3293 is the hydrology number that belongs beside their
  sediment number** — whatever their sediment number turns out to be.

**This number is also superseded** (§0): *"Stage 1 hydrology was just refitted under a new
objective."* And their own caveat applies to it too: *"Our headline was median KGE on **log**
discharge; on **linear** KGE the same run scores far lower."*

### 3.3 The one comparison of skill that IS structurally sound — and it is theirs, not between us

**Their reading — "the Stage-1-vs-Stage-2 gap is the finding" (≈ 0.33 on discharge against ≈ 0.06
on sediment, same code, same basin, same window, same aggregation) — is a within-implementation
comparison and it does not depend on any cross-project commensurability.** It is the same shape as
R1's own conclusion that the binding constraint is inherited from the forcing and the runoff timing
rather than from a sediment parameter (`docs/22`; `docs/55` §5; the `r ≈ 0.57` ceiling). This
project endorses the *shape* of that reading and notes that **the magnitude of their gap must be
recomputed post-fix** before it carries a number.

### 3.4 Their metric warning, recorded because it binds us too

> *"Please state which transform, which aggregation (median vs area-weighted mean — **on our data
> these ranked trials in opposite order**), gauge count, and in-sample vs held-out, or the numbers
> are not comparable."* — MANIFEST.md

**Median and area-weighted mean ranking trials in opposite order on their data is a finding, not a
pedantic point.** R1 aggregates by median (`F_report`, `docs/45` §302) and has never measured
whether an area-weighted mean would rank its own trials differently. That is now a named item we
owe them and ourselves (§8.4, item 2).

### 3.5 Which setup is the more constrained, and why that matters — a different choice with a stated reason

This section is about **design**, not scores, so it survives §3.1 intact. **R1 is the more
constrained setup**, on four counts, and this is a *choice with a registered reason*, not a virtue:

- **2 free parameters against 4**, because α, C, K, LS, `f_vol`, P and FG were measured to be
  **seven ways of writing one identifiable product Π** with condition number `inf` (`docs/42`
  §3.1) — so fitting more of them cannot add information, only redistribute it.
- **C is fixed at a cited level and has never been fitted** (`cp_revision =
  'cited_central_2026_08_11'`, used as read; `src/mgb_sediment.py` L1024–1025).
- **The α box is narrow** — [2.0, 30.0] against their log-U[0.02, 200] — because it was
  pre-registered against Williams (1975) and Fagundes' own MOCOM-UA prior (`docs/45` §84).
- **The score is on flux**, which requires same-code discharge and therefore admits fewer stations
  (§6.3).

Why it matters: **the constraint is exactly why R1 railed and R2 did not.** With C fixed and the α
box narrow, an upstream over-production has nowhere to go and shows up as a rail at the floor —
which `docs/35` §6.1 registered in advance as the signature of over-production upstream
(`Qsur`, `K`, `C`, `LS`) *to be found, not offset*. With `c_mult` free over two decades, the same
over-production is absorbed silently into a multiplier. **Neither behaviour is an error.** R1 bought
a diagnostic at the cost of a fit; R2 bought a fit at the cost of the diagnostic, and then
**documented the resulting non-identifiability itself** (§4). The comparison does not adjudicate
which purchase was better and this document does not try.

---

## 4 — THE CENTRAL RESULT: non-identifiability. One leg survives, one is suspended.

This is the strongest thing in the comparison and it is the section to lead with — **but only its
algebraic leg**, and the distinction is the whole of §4.3.

### 4.1 The algebraic leg — SURVIVES, and it is bug-independent

**R1's route, analytic — grade DERIVED.** The design matrix of
**Π = α · f_vol · f_K · f_LS · C_mult · P · FG** over the calibration station set has
**condition number measured as `inf`** — **exactly singular** (`docs/42` §3.1, §115; carried by
`docs/37`:789/1133, `docs/43`:76, `docs/31`:633). Only the **product** is identifiable. No
calibration on any objective can separate the LS level, the C level or α from one another
(`docs/37`:1596 (C)). This is why C4 reports Π, the equifinal family and per-factor evidence grades,
and **never** the word "validated" — and why `docs/47` blocked the search rather than spending a
one-shot registration on an answer that was already computable.

**R2's route, from the structure of their own code — grade IDENTIFIED, and stated by them first.**
Both `outputs/calibration/stage2_sediment_params.json` and
`outputs/calibration_val/stage2_sediment_params.json` carry, verbatim:

> **"MUSLE is linear in both alpha and the C multiplier; only their product is identifiable from
> these data."**
> — `notes.alpha_c_collinearity`, in both shipped parameter files

**This statement is a property of the MUSLE code and is unaffected by the SSC reporting defect.**
`musle_yield` computes `yield_t = alpha · energy^beta · K · C · P · LS`; `alpha` and the `C`
multiplier multiply the same expression. Their exact collinearity does not depend on any simulated
series being correct, on any score, or on any station set. **It is the one R2 result in this
document that no re-run can move.**

### 4.2 Why the two routes together are worth more than either alone

They fail in opposite ways. R1's argument is a linear-algebra statement about **our own
factorisation** of Π and could in principle be an artifact of how we chose to write it. R2's is a
statement about the algebraic form of **their** MUSLE implementation. **They share no model code, no
objective, no station set and no scored quantity**, and they land on the same conclusion: *the
sediment level is not identifiable from these data.* **Grade: DERIVED (R1 leg) + IDENTIFIED (R2
leg).** The joint statement is the reason this project declined to fit the level first, and R2's
note is the first external corroboration that decision has ever had.

**And the degeneracy is one term deeper than R2 states — offered as convergent evidence, not a
gotcha.** `musle.py` computes `energy = qsur · qpeak · area_ha` with
`qpeak = alpha_tc · Qsur · A / (3.6 · tconc)`, so `alpha_tc` scales `energy` by a global scalar and
`energy^beta = alpha_tc^beta · (…)^beta`. **At fixed β, `alpha` and `alpha_tc` are exactly collinear
too**, and their identifiable scale group is **`alpha · c_mult · alpha_tc^beta`** — a three-way
degeneracy of which their note documents two terms. This is a *deeper form of their own finding*, in
exactly the shape of R1's seven-factor Π. And note the symmetry honestly: **R1's Π has seven factors
and R1 did not catch every collinearity in its first pass either** — `docs/42` §3 is a later
document than the model.

### 4.3 The empirical leg — **SUSPENDED**, and recorded as owed

The demonstration R1's brief wanted to lead with was this:

| | `alpha` | `c_mult` | `alpha × c_mult` | median KGE_log | n |
|---|--:|--:|--:|--:|--:|
| `outputs/calibration/` | 55.40533705803028 | 0.04887856036752898 | **2.7081331120742234** | 0.05461202762457862 | 21 |
| `outputs/calibration_val/` | 96.58548959666564 | 0.05779232694874972 | **5.581900193275565** | 0.05902198016897042 | 13 |
| ratio | ×1.7432524504905407 | ×1.1823655712074193 | **×2.0611616793829812** | **+0.004409952544391804** | — |

*A factor of 2.06 in the only identifiable product, for 0.0044 of median score.* **It may not be
presented as a measured demonstration, because both scores in the right-hand column were computed
on the defective simulated concentration of §3.1.** The **parameters** are what they are; the
**scores** are void; and the claim "×2.06 for 0.0044" is a statement about the scores.

**What is owed, to make it a measurement again:** a re-run of both cells on the post-fix
flux-weighted `SSC = Qss/Q`, reporting the same two products and the same score delta. That is
R2's to run and this document asks for nothing else on this point (§8.4).

Two further cautions that apply to the suspended leg and would still apply after a re-run, both
from M4:

- **These are not two independent searches.** The two `stage2_search_history.csv` files share the
  same trial index and **byte-identical** `alpha/beta/alpha_tc/c_mult` for all 300 common trials
  (same seed 42; max absolute difference **0.0** per column). It is **one seeded sample re-scored on
  a different station set**. The correct description is a station-set change, never "two independent
  fits agreeing".
- **The 8 dropped stations are not an arbitrary deletion.** The validation cell keeps only
  `mapping == "discharge_validated"` (`--only-validated-stations`) — a **mapping-quality filter**,
  which arguably makes the validation cell the *better* fit of the two.
- **`alpha × c_mult` is not dimensionless across the two cells**, because β differs (0.398 vs
  0.349) and the MUSLE bracket is raised to β. The cleanest single statement, once rescored, is the
  one measured on a **common station set**.

### 4.4 What the central result does NOT show

1. **It does not show either model is wrong.** Non-identifiability is a property of the data and the
   model structure jointly, not a defect in either implementation.
2. **It does not validate our LS choice.** `f_LS` = **0.25146** is ADOPT-SOURCE on **CITED**
   provenance grounds (`docs/37` A3); the **level** stays **UNVALIDATED** (`docs/42` G4.2), and
   `docs/37`:1596 (C) already states that *cited is not validated* and *fitted is not validated
   either*. R2's collinearity note is evidence **that a fit cannot settle the level** — an argument
   *against* using any fit as LS evidence, ours or theirs. It cuts toward humility on both sides.
3. **It does not make the two fitted α's comparable.** Their `alpha` 55.4053… is ×4.695368 of
   Williams' 11.8, at a **different β** (0.398 vs 0.56), on a **different LS field on a different
   grid** (184 m routing grid, by design), multiplied by a **different C table** and a fitted
   `c_mult`. Their α carries no standalone information by their own note — which is precisely R1's
   own G6 rule that α is *never reported alone*.
4. **It does not license "fitted product 2.7 vs Williams' 11.8" as a transferability ratio.** The
   MUSLE bracket is raised to β, and their β is 0.398, not 0.56, so the two numbers are not
   dimensionally comparable.
5. **It does not license any statement about the LEVEL either project produces.** No basin sediment
   load of theirs exists on this disk in any form (**X11**), so no sentence of the form *"their model
   produces X Mt/yr against our 299.539"* can be written at all. Any such number would be fabricated.

---

## 5 — What the comparison narrows, and what it does not

**M3 governs this section, as amended by the bundle.** The tempting inference — *"if their code
differs and the answer is the same, the shared inputs must be where the over-production lives"* — is
**valid only over the rows that are genuinely shared**. The bundle moved three rows *away* from
shared and one row *decisively into* shared, and the net effect is that the argument now reaches
**one** of the four C4.3 suspects instead of none.

### 5.1 Genuinely SHARED — and one row is now proved at hash level

| row | shared thing | evidence |
|---|---|---|
| **soil / K product** | `minibacia_soil_params.csv` — **BYTE-IDENTICAL** | **sha256 `6e5940ecdbd06c8b89b09e9134cbe6586933ff9c6971e896feb9e85b19ae38b1`** on both sides: `input_hashes.txt` line for `02_basin_and_soils/minibacia_soil_params.csv`, and `sha256sum data/processed/minibacia_soil_params.csv` run by this writer this session (398,698 bytes). MANIFEST A9: *"soil/K source as used"* |
| **DEM archive** | `rasters_COP90_Correcte_Corrdinatzs.tar.gz`, member `output_hh.tif`, 0.000833° | theirs `config/data_sources.yaml` L9–14; ours `docs/15` L24/L31 — **same archive, same member, same filename typo** |
| **domain bbox** | lon −77.0 … −72.3, lat 1.4 … 11.4 | theirs `basin_domain`; ours `docs/15` |
| **land-cover product** | ESA WorldCover **10 m 2021 v200** | theirs `data_sources.yaml` L24; ours `data/processed/worldcover/ESA_WorldCover_10m_2021_v200_*.tif` |
| **raw precipitation gauge export** | the same 294-station IDEAM DHIME table + inventory | theirs `stations: 294`, `station_days: 686752`, and their C3 answer names `precip_gauges_daily.csv` / `precip_gauges_inventory.csv` as its defaults; ours `precip_gauges_daily.csv` = **686,752 rows / 294 stations**, exact |
| **meteorological reanalysis** | ERA5-Land 9 km, `valid_time`, numerically equivalent `ssrd` daily-total rule (both land on the 23:00 value) | theirs `forcing.py`; ours `docs/16` §6.1 |
| **the observations themselves** | 21/21 SSC calibration, 13/13 SSC validation, 90/90 discharge — containment **1.000**, zero stations of theirs we lack | M1 |

**The soils row is the most important measurement in this document that was not carried from
M1–M4.** M3's code read found `src/mgbsed/preprocess/hru.py:build_k_factor` calling
`erodibility_sharpley_williams` on SoilGrids, and concluded soils were **DIFFERENT**. The author's
own account says the shipped soil/K source is `minibacia_soil_params.csv`, and **the hash proves
that file is bit-for-bit ours**. Under the Tier-B rule the author wins, and here the author is
corroborated by arithmetic rather than believed. Two honest limits: a hash proves **the file is the
same file**, not **which code path consumed it** (their two statements about their own soil source
conflict at `d055561`, and the conflict is theirs to resolve, not ours to adjudicate — **X13**); and
this is **one** row of `input_hashes.txt` tested, not twenty (**X12**).

### 5.2 What moved OUT of shared, and why the narrowing got weaker on three rows

`basin_magdalena.pkl` (MANIFEST A8) settles what M3 could not: **7,929 unit catchments, a 184 m
routing grid, LS2D computed on the routing grid deliberately, floodplain level–volume–area curves,
12 HRU fractions.** So the catchment discretisation, the LS field and the HRU scheme are **theirs**,
not ours, and M3's alternative reading (275 m, from the `--resample 3` argparse default) is
**closed at 184 m** (**X5 CLOSED**). Their forcing is likewise theirs: **3,287 days × 7,929
catchments** (2009–2017, verified: 3,287 days) of a **gauge–CHIRPS merge**, not our IDW field.

### 5.3 The narrowing, stated exactly

| C4.3 suspect (`docs/35` §6.1) | R1 | R2 | narrowed? |
|---|---|---|---|
| **`K`** | IGAC field survey → `minibacia_soil_params.csv`; measured over 8,672 minibacias: median **0.030550**, mean 0.031824, range 0.019–0.0495, CV 0.2289 | **the same file, byte-identical** (§5.1) — though aggregated onto 7,929 catchments × 12 HRUs rather than 8,672 × 24 URH, and their code also contains a SoilGrids/EPIC path (**X13**) | **YES — the one suspect the argument reaches.** A code-difference argument cannot exonerate `K`: both implementations read the same numbers |
| **`Qsur`** (the rainfall→runoff field) | gauge-only IDW, k=6, on the **repaired** `precip_gauges_daily_qc_v2.csv`; FAO-56 PET × `kc_mult` 1.662; basin P **2,036.4 mm/yr** (2009–2017) / **2,073.1** (2008–2018), PET **1,251.6 mm/yr** | **gauge–CHIRPS merge**: 88 gauges at ≥ 80 % completeness supply the level, CHIRPS the spatial pattern, monthly log-ratio IDW-interpolated and applied multiplicatively, ratios clipped **0.25–4.0**; basin mean **1,965 mm/yr**; per-HRU Penman–Monteith, ETp **1,239 mm/yr** quoted | **NO** |
| **`C`** | 8 classes, **cited** Colombian/Neotropical values, used as read, never fitted; area-weighted **0.0130829583** | 4 cover groups, **Guaiba-inherited** table (forest_wetland 0.0001), area-weighted **0.0101226238**, × a **fitted** `c_mult` | **NO** — §5.6 |
| **`LS`** | `buarque_2015_dg` at native **90 m**; area-wt mean **9.920900**, median **5.090050** | Desmet & Govers with **m fixed at 0.4** + W&S-78 S, on the **184 m routing grid, deliberately**, with their own written caveat that a coarse grid overstates slope length | **NO** |

**So the shared-inputs argument reaches `K` and nothing else among the four.** And even there it
produces **no positive evidence against** `K` — it establishes only that a code-difference argument
cannot clear it. On `Qsur`, `C` and `LS` the argument is silent, which is exactly where C4.3 needs
it not to be. **This is the honest and disappointing content of §5, and it is the opposite of what a
favourable comparison would have wanted.**

Two rainfall figures worth setting down side by side, because they are the closest thing to an
independent check on our forcing volume that exists: their **1,965 mm/yr** against our
**2,036.4 mm/yr** on the matching 2009–2017 span — **ours is 3.51 % higher** (1965/2036.4 =
0.9649381261048909) — or **5.21 % higher** against our 2008–2018 figure of 2,073.1. Both sit near
the *"published ~2,050"* their own docstring cites. **This is not a gate and nothing passes or
fails**; it is two numbers from two constructions, recorded. (Our **2,206 mm/yr** headline is
**stale** — `docs/16` §14 supersedes it, and quoting it here would have manufactured a disagreement
that does not exist.)

One further asymmetry worth naming: **"shared product" is not "shared input".** CHIRPS v2.0
`days_p05` is byte-for-byte the same product in both repositories — and it is **the field** in R2
and **absent from the adopted forcing** in R1. ERA5-Land is the same product with different ET
formulations and different available years (ours 2008–2018 complete; theirs 2009–2017).
WorldCover is the same raster reclassified into 8 classes on one side and 4 groups on the other.

### 5.4 R1's own DEM provenance is UNRESOLVED, and it is ours to fix

`data/processed/model_inputs_v2/manifest.json` records the topology as *"notebook 07 D8 delineation
on **COP30**"*, while all the terrain and LS work (`docs/35` §65, `docs/37` §3) is on the corrected
**COP90** — and `docs/35` §58–59 says the processed `cop30_dem.tif` covers only
(−75.400, 8.200) → (−73.700, 11.300), which **cannot** produce a 257,096.93 km² basin. One of the
two statements is wrong. Until it is settled, the DEM row of §5.1 is *"shared archive, different
working product"* **on our side too**, and the narrowing above is weaker than the table suggests
(**X6**). R2's working grid, by contrast, is now **settled at 184 m** — theirs got resolved by the
bundle and ours did not.

### 5.5 On precipitation, R1's accusation is WITHDRAWN — and a smaller item survives

**The withdrawal, first and plainly.** R1 was about to publish that R2 runs on the
zero-suppression-defective gauge file. **That is false.** Their C3 answer:

> *"A filesystem search of `data/` and `data_Final/` for `precip_gauges_daily*` returns exactly one
> file … **No `precip_gauges_daily_qc.csv` exists anywhere in the repo**, so no repaired file was
> bypassed."*

Their QC runs **in-script** at `scripts/15_build_forcing_v2.py:52-108` — gauges reporting on < 80 %
of days dropped (`:80-93`), no-coordinate records dropped (`:74-79`), abort under 20 surviving
gauges (`:95-99`) — and their rainfall is then the **merge**, not raw IDW. **They diagnosed the same
defect this project diagnosed, independently, from the data**, recording the reporting-density
signature in their own loader docstring (> 90 % of days → 4.5 mm/day; 50–90 % → 6.9; < 50 % →
**13.0 mm/day** — *"a 2.9× spread in rainfall as a function of how often the observer wrote
something down is not geography"*), and its consequence (*"raises basin rainfall to 2,420 mm/yr
against a published ~2,050, which forced actual ET (1,659 mm/yr) above potential ET (1,239)"*).
**Their mitigation is exclusion; ours is repair** (`Inferido_seco`, all 294 gauges kept). Two
independent diagnoses of one defect, and neither project handed the other the answer.

**The smaller item that survives, and it is ours.** `src/build_data_final.py` routes only
`precip_gauges_daily.csv` and `precip_gauges_inventory.csv` (L86–87) and **never** the `_qc` files
(`grep -n "_qc"` → no match) — against this project's own standing rule (`CLAUDE.md`: *"Use the
`_qc` files … never the pre-repair ones"*; `docs/16` §4.1). Measured on our disk:

| file | rows | stations | zero fraction | `Inferido_seco` | mean |
|---|--:|--:|--:|--:|--:|
| `precip_gauges_daily.csv` (**what the router ships**) | 686,752 | 294 | 0.441793 | 0 | **6.821825 mm/d** |
| `precip_gauges_daily_qc.csv` | 795,881 | 294 | 0.518333 | 109,129 | 5.886435 mm/d |
| `precip_gauges_daily_qc_v2.csv` (**what we use**) | 926,910 | 294 | 0.586422 | 240,158 | **5.054322 mm/d** |

6.821825 / 5.054322 = **×1.3496976**, and 6.821825 × 365.25 = **2,491.67 mm/yr** against their
docstring's *"the gauges average 2,492 mm/yr"* — exact, which is how the router's behaviour was
identified in the first place. **The defect is in the handoff router, not in their model**, and the
correct statement of it is: *our bundle ships the pre-repair file, and it caused no harm because the
recipient had its own QC.* That is a much smaller finding than the one R1 nearly published, and it
is still owed to `src/build_data_final.py` and `docs/16` §4.1 (§10).

### 5.6 The C-factor disagreement — and whether the two C's are the same object

**M3's ruling stands: they are not the same object, and the disagreement decomposes.**

| | area-weighted mean C | erosion-potential-weighted |
|---|--:|--:|
| **R1 table** (`urh_cp_factors.csv`, `cp_revision='cited_central_2026_08_11'`) | **0.0130829583** | 0.0080549035 |
| **R2 table** as printed, on our area shares | **0.0101226238** | 0.0040460557 |
| ratio R1 / R2, **tables only** | **×1.292447** | **×1.990804** |
| **R2 effective**, after `c_mult` = 0.04887856036752898 | **0.000494779278** | — |
| ratio R1 / R2-effective | **×26.442009** | ×40.7296 |

Independent cross-check that the two land-cover distributions really do agree closely: R2's own
`scripts/21_calibrate_sediment.py` docstring states *"the area-weighted basin C was 0.0104"*;
M3's recompute of **their table on our area shares** gives 0.0101226238 — **2.67 %** apart.

**Three things follow, and only the first is a comparison of like with like:**

1. **The table disagreement is ×1.29 (area) / ×1.99 (erosion-potential)** — modest, and it is a
   disagreement about *which C values apply to Colombian Andean cover*, not about the model. The
   sharpest single instance: on the **same** WorldCover codes, code 60/70 maps to our **Bare
   C = 0.500** and their **cropland_urban_bare 0.100** (×5), and code 100 (moss/lichen, i.e.
   páramo) maps to our Bare 0.500 and their **grassland 0.020** (**×25**). Our land class 6 is only
   **0.196257 %** of area but **14.780004 %** of our modelled erosion, so that mapping choice is
   load-bearing for us, and the code split across 60/70/100 is **not available from the tiles on
   disk** (**X7**).
2. **The remaining ×20.46 is their fitted `c_mult`, and it moved in the direction opposite to its
   stated motive.** Their own words: *"Sediment came out ~25× too low, because the C factor for the
   forest/wetland HRU group (0.0001) was inherited from the Guaiba basin and applied to WorldCover
   'tree cover' in the Colombian Andes — coffee, plantain, degraded hillside … implying an
   erosion-proof landscape in a basin with among the highest sediment yields on earth. Hence the C
   multiplier."* The multiplier was introduced to **raise** the level; the fitted value **lowers**
   it ×20.458868, with `alpha` moving **up** ×4.695368, net **×4.357245 down** relative to
   (Williams' 11.8, their C table as printed). **And that fitted value is a pre-fix number** — the
   fit that produced it scored defective concentration (§3.1), so the ×26.44 and ×20.46 figures are
   *arithmetic on published parameters*, not statements about what their model needs (**X14**).
3. **Therefore R1 revising C UP ×1.20427 and R2 fitting `c_mult` DOWN to 0.04888 is NOT two
   measurements of one quantity, and must not be presented as convergence or as conflict.** Ours is
   a **cited, unfitted revision of a table** (`docs/41`; `docs/37`:542 measured the adopted/prior
   ratio at 1.204272539864846, predicted ×1.2043 from a linear decomposition and confirmed by
   simulation). Theirs is a **fitted scalar on a different table under a different class mapping,
   scored on concentration, from a fit whose scores are void, and non-identifiable from `alpha` by
   their own note.** The two live in different currencies. **Neither table has been tested against
   measured erosion.**

**This connects directly to open item O10** (`docs/47` §7, §9.3): *"`docs/41` remains unaudited"*
(C3 clause 3), *"and G3.1 is measured blind to its ×1.2043 revision, so C4 cannot audit it however
it comes out"* — and `docs/47` §9.3 confirms **no `docs/41` audit exists in `docs/agents/`**. The
existence of a sibling implementation whose C table is ×1.29–×1.99 **lower** than ours before any
fit, built from the same WorldCover raster, **raises the value of the O10 audit and supplies it a
concrete external comparator with one specific target** — the code 60/70/100 → class-6 mapping. It
does **not** discharge O10, does **not** show our C is wrong, and does **not** show theirs is
(**X8**). The audit is still owed to `docs/41`'s owner (§10).

### 5.7 What "both want a lower level" is NOT

A premise worth killing explicitly. **R2's reduction is a FITTED level**:
`(alpha × c_mult)/11.8` = **0.2295028061**, i.e. ×4.357245 down, scored — on defective concentration
— as median KGE_log over 21 stations in a 730-day window. **R1's is not a fitted level at all**: our
α stays at Williams' 11.8, our LS reduction is a **formulation correction** (`docs/37` A3, no engine
default moved), and C4.3 is **RAILED / EXPLORATORY** on log **flux**. **Same direction is not the
same measurement**, and this document does not present the two as independent estimates converging.

### 5.8 A named candidate this opens for R1 — recorded, not proposed

**Their gauge–CHIRPS merge works, and lands at 1,965 mm/yr.** Ours was built, failed its volume
gate twice (**+7.5 %**), and `docs/26` §7's *"the CHIRPS merge is the only remaining lever"* was
declared spent by `docs/18` §15.5: *"no route to a passing volume gate exists inside the merge
code."* Their construction differs from ours in specifics this project never tried, and they are
recorded here so the candidate is *named* rather than *rediscovered*:

- **88 gauges at ≥ 80 % completeness supply the LEVEL; CHIRPS supplies the SPATIAL PATTERN** — a
  division of labour, not a blend.
- the correction is a **monthly log-ratio**, **IDW-interpolated**, applied **multiplicatively**;
- **ratios clipped to 0.25–4.0**, with ≥ 10 shared days required per gauge-month;
- fallback to plain gauge IDW only if no `chirps_basin_*.nc` is found.

**Phase B is CLOSED on H2E, and re-opening it — forcing or objective — requires a new
pre-registration** (`docs/33` §5.1). **This document proposes nothing, re-opens nothing, and
pre-registers nothing.** It records a construction, its clip bounds and its measured basin mean, so
that whoever writes that pre-registration does not have to reconstruct them. Note also what would
make this cheap to evaluate: their basin volume is a **published number**, not a bound inferred from
our own failed attempt — and it is 3.51 % below ours on the matching span, not above it, which is
the direction our own merge failed in.

---

## 6 — The ENSO contrast: an external check on the deliverable, at a coarser grade

### 6.1 The correct pairing is observation-vs-observation — and a model-vs-model check is now IN PROGRESS on their side

**R2's repository at `d055561` contains no modelled ENSO contrast.** `grep -ril` for
`nino|nina|enso` over their `outputs/` returns only the two stage-2 JSONs, `eda/enso_summary.csv`
and two `rs_retrieval` files. So the pairing available today is **their `enso_summary.csv` ↔ our
`docs/34`** (observation vs observation), **not their model ↔ our `docs/56`**.

**That will change.** MANIFEST item **B3** is *"in progress"*:
`scripts/23_validate_heldout.py` *"runs the held-out 2011 / 2015–17 windows and reports observed vs
simulated La Niña / El Niño load ratio. Yours is 3.05 across 18/18 — we will send ours for the
direct check."* And their `paired_load()` already computes **sampling-matched observed vs simulated
load, `Qss = SSC × Q × 0.0864` on paired days only** — the same estimator as `docs/34` §1.3.
**So the one comparison this project most wants is a run away, on their side, and it is on the
right quantity: load, paired, on the held-out windows.** It is not in this document because it does
not exist yet (**X2**).

Note also that their **held-out dry span is 2015–2017**, wider than either project's EDA dry window
— a conservative choice in their favour.

### 6.2 Their station counts, corrected

R1's brief carried **35/27** SSC and **108/93** Q as R2's station counts. Those are **window-specific
counts inside `enso_summary.csv`**, not their universe. From MANIFEST A2/A4:

| | total | plausible | rejected | admissibility rule |
|---|--:|--:|--:|---|
| **their SSC** | **59** | **57** | 2 | mapped to a reach; **25 `discharge_validated`** + **32 `nearest_centroid`** (proximity-snapped, reach ≥ 20 km², snap ≤ 15 km) |
| **their discharge** | **118** | **114** | 4 | *"specific discharge fell inside 5–150 L/s/km²"* — stations outside that band *"snapped to the wrong watercourse and produce a believable hydrograph of a different river"* |
| **our SSC** | **79** | **18 usable** (6 usable + 12 usable-with-caveat) | 61 excluded | `docs/32`: coordinates, in-domain, paired discharge, flow-selectivity, rating quality, both-window coverage |
| **our discharge** | **192** | — | — | `docs/17` / `docs/23` |

**Compare the BARS, not the counts.** Their 57-of-59 admits 32 stations on a **proximity snap**;
our 18-of-79 requires same-code paired discharge and survives a flow-selectivity screen. **Their
bar is looser, and it is looser for a stated and coherent reason:** their objective scores
**concentration**, which needs no paired discharge at all, so the constraint that eliminates most of
our 79 does not apply to them. **Neither bar is wrong on its own terms**, and the difference in n is
a design consequence, not a difference in care. (Their 5–150 L/s/km² is a **specific-discharge**
screen on hydrology, not a sediment yield; the `docs/23` §13.2 embargo is not engaged by quoting
it.)

The nesting of the 21 / 13 / 90 **calibration** sets inside ours (containment 1.000, §1) is measured
and unaffected by this correction. Whether their full **59**-station SSC universe is also a subset
of our 79 is **not measured** — the file that would settle it, `observed_ssc_stations.csv`, is in the
bundle's Tier 1 and was not extracted here (**X4**, now *settleable* rather than blocked).

### 6.3 Their windows, read from their code — not the calendar reading

`src/mgbsed/viz/observations.py` L41–46: `ENSO_EVENTS = {"La Nina 2010-12": ("2010-06-01",
"2012-04-30"), "El Nino 2015-16": ("2015-03-01", "2016-05-31")}` — **700 d** and **458 d**.
*"2010-12"* means **June 2010 → April 2012**, not calendar 2010–2012. This mattered: on our data the
calendar reading shifts the flux median by ~19 % (4.485827 vs 3.766024). **Any sentence using the
calendar reading is wrong.**

The nesting with our own windows (`docs/34` §1.1) is the signature of the same events measured over
the same days:

| pair | overlap | % of theirs | % of ours |
|---|--:|--:|--:|
| their LN ∩ our **P-LN** (2011) | 365 d | 52.142857 | **100.000000** |
| their LN ∩ our **S-LN** | 365 d | 52.142857 | **100.000000** |
| their EN ∩ our **P-EN** | 458 d | **100.000000** | 62.653899 |
| their EN ∩ our **S-EN** | 213 d | 46.506550 | **100.000000** |
| their LN ∩ our S-EN, and their EN ∩ our P-LN | **0 d** | — | — |

Their fit window (730 d) is a **strict subset** of our CAL (1,096 d), 66.605839 % of ours. The
methodological agreement — same events, same holdouts, arrived at without coordination as far as
anything on disk shows — is creditable. **It is agreement on METHOD, which is what "independent
implementation" names; it is not data independence.**

### 6.4 Their EDA numbers ARE POOLED — and the product of their marginals is NOT COMPARABLE

Their `outputs/eda/enso_summary.csv`, verbatim:

| | n | median | mean | p90 | stations in window |
|---|--:|--:|--:|--:|--:|
| SSC mg/L, La Niña 2010-12 | 14,722 | 48.0 | 213.35545442195354 | 607.0 | 35 |
| SSC mg/L, El Niño 2015-16 | 4,139 | 36.0 | 106.1816597825161 | 204.0 | 27 |
| Q m³/s, La Niña | 65,065 | 21.2 | 589.2964713876403 | 1582.0 | 108 |
| Q m³/s, El Niño | 32,666 | 10.57 | 298.51300188766066 | 793.8458541666671 | 93 |

These are **pooled station-day marginals across different station sets over unequal windows
(700 d vs 458 d)** — precisely the construction `docs/34` §1.2 forbids for our own numbers
(*"Cross-window comparison uses RATES ONLY … Window totals … are NEVER divided by each other"*; the
SSC marginal is drawn from 35/27 stations and the Q marginal from 108/93 **different** stations,
unpaired). **Reporting them as pooled is mandatory here.**

**The algebra, and why the product fails.** With `rho ≡ Cov(C,Q)/(E[C]E[Q]) = corr(C,Q)·CV_C·CV_Q`:

```
F_ratio  =  [C_ratio × Q_ratio] × (1 + rho_wet)/(1 + rho_dry)
                                   \_______ B, the bridge factor _______/
```

Equality with the product of marginals holds **iff** `rho_wet = rho_dry`. **The sign of the bias is
not determinable from pooled marginals** — they do not contain `rho`. No bound is asserted; **B was
measured**. And the covariance term turns out **not** to be what breaks the bridge; the **pooling**
is:

| construction, on **our** data | implied bridge factor B |
|---|--:|
| per-station, composition fixed, our P windows (6 stations) | **0.961590** |
| per-station, composition fixed, their T windows (6 stations) | **1.002192** |
| pooled, composition free, our P windows | **1.917123** |
| pooled, composition free, their T windows | **1.426062** |

Pooling moves B by **5–20× the size of the within-station covariance term**, and drives the pooled
Q ratio in our primary pair to **0.810879** — **below 1**, i.e. it flips the sign of the discharge
contrast. **NOT COMPARABLE is the grade for the product of their marginals**, and R1's bracket
argument is **withdrawn**. Blaming the covariance term would be a *wrong diagnosis that happens to
reach the cautious conclusion* — the exact failure mode this project has reversed before.

### 6.5 What IS corroborated: their two marginals, taken separately — grade CONSISTENT

Recomputed on our independently QC'd copy of the same IDEAM network, on **their exact windows**:

| statistic | ours | theirs | agreement |
|---|--:|--:|--:|
| SSC **mean** ratio | 1.922268 | 2.009344 | **4.3 %** |
| Q **mean** ratio | 2.043922 | 1.974107 | **3.5 %** |
| Q **median** ratio | 2.077275 | 2.005676 | **3.6 %** |
| product of means | 3.928965 | 3.966659 | 1.0 % |
| SSC **median** ratio | **1.525000** | **1.333333** | **14 % — disagrees** |

**Three of four agree to 3.5–4.3 % and this is a genuine point in R2's favour**, independently
verifiable and unaffected by the SSC simulation defect (these are **observed** series on both
sides). **The one disagreement is stated too**: the SSC median ratio differs by 14 %, cause
**unidentified**. The bundle narrows the candidates: their SSC universe is **59 / 57 plausible** with
**32** stations admitted on a proximity snap, against our 41/32 in-window — so **station
composition** is now the leading candidate and our C1 deletions (269,305 of 269,337 rows) remain too
small to explain it. `observed_ssc_daily.parquet` + `observed_ssc_stations.csv` (bundle Tier 1)
would settle it (**X3**).

**CONSISTENT here describes commensurability — whether two quantities are the same kind of number —
and is not the outcome of any numeric gate. No band was introduced or reconstructed; nothing above
passes or fails anything** (`docs/52` §7).

### 6.6 The measured concentration→flux bridge, and the only defensible transfer

In this basin, at the gauges that support a both-window paired ratio, the bridge is **measured, not
assumed**. Per-station **F/C** (flux ratio ÷ concentration ratio):

| window pair | n stations | median F/C | range | median B |
|---|--:|--:|---|--:|
| our **P** (2011 vs 2015–16) | 6 | **2.222674** | 1.280070 – 2.843132 | 0.961590 |
| their **T** (2010-06→2012-04 vs 2015-03→2016-05) | 6 | **2.103858** | 1.161955 – 2.443523 | 1.002192 |
| our **S** (sensitivity) | 4 | 2.871403 | — | 1.165177 |

B never leaves **0.810929 – 1.511812** at any station in any pair. **If a single transferred number
is wanted it must be labelled as THEIR concentration × OUR discharge bridge, and it is not
independent corroboration:**

> their SSC **mean** ratio 2.009343749748812 × our F/C(T) median 2.103858 = **4.227373**
> (station range 2.334767 – 4.909878); their SSC **median** ratio 1.3333333333333333 × 2.103858 =
> **2.805144**.

**B ≈ 1 is a finding about OUR basin at OUR 4–6 both-window gauges**, not a general property of C–Q
data, and it licenses exactly one statement: *in this basin, at these gauges, on paired sample days,
the covariance term is not what breaks the bridge.* No interval is registered for B and none is
invented; the per-station spread above is the only uncertainty statement available.

### 6.7 Verification that the bridge machinery is sound, and the honest bottom line

M2's independent reimplementation of `docs/34` §1.3–§1.4 reproduced **6 of 6** primary
estimator-(a) station ratios **to printed precision** (21197010 1.211804 vs 1.21; 22017010 1.701723
vs 1.70; 22017030 9.678658 vs 9.68; 23127010 11.680023 vs 11.68; 24037390 2.451295 vs 2.45;
26017060 6.789032 vs 6.79), median **4.620164** vs registered 4.62, and cross-checked two values
against `c5_enso_contrast.json` **identically**. That verifies M2's code against `docs/34`'s
registered numbers; **it does not re-verify `docs/34`'s underlying QC** — and it is an unusually
clean reproduction that `docs/34`'s owner should know about (§10).

**The bottom line for the deliverable.** Our C5 result — the model reproduces the observed contrast,
**18/18** stations, modelled median rate ratio **3.046755091543662** (geomean 3.0563436523427323)
against observed ~3–5 (`docs/34` primary windows: est. (a) median **4.620163547568586**, est. (b)
**2.948674885718534**, range up to ~9) — now has an **external observational comparator that points
the same way at a coarser grade**: R2's pooled SSC and Q marginals both fall wet-over-dry, and
recompute on our data to within 3.5–4.3 % on three of four statistics. **It does not yet have a
model comparator**, and the one being prepared (B3) is the item to wait for.

**And, in the same paragraph, as `docs/42` G9 requires:** **66.53 % of the model's gross *hillslope*
erosion — 199.29 of 299.54 Mt/yr at `cp_revision='cited_central_2026_08_11'` (conventions in §0) —
is upstream of no usable SSC station**, including **801.1 km** of channel
and the whole Depresión Momposina below the outlet-most station; only **33.47 %** is observed, and
*"above vs below the Momposina"* is **NOT EVALUABLE, measured** (`docs/45` §4.1, §499). **The
external comparator does not change that fraction by one station**, because its calibration stations
are a **subset of ours** (§1). And because both projects read the same IDEAM archive — and, now
measured, the same soil/K table — a systematic ENSO artifact in those observations would be
reproduced by both and detected by neither.

Two station-level cautions, so the concordance is not read as tighter than it is: at **21197010**
the primary-pair **concentration** ratio is **0.432980** — concentration is *lower* in La Niña —
driven by the uncorroborated 15,180 mg/L EL PROFUNDO point of 2016-06-04 sitting in the dry window
(`docs/34` §3.4, +156.7 % leverage), and its B of 1.315351 is spike-driven, not physics. At
**24037390** on their windows `C_ratio` = **0.998722** — flat concentration, with the entire
contrast carried by discharge. **"Concentration contrast" and "flux contrast" are not the same
statement at the station level even when both are positive.** And **26017060** has only 33 (P) /
16 (T) paired dry-window days, not down-weighted.

---

## 7 — The satellite SSC retrieval: a route that is already built, with its leakage now measured

### 7.1 Their shipped numbers, verbatim

`outputs/tables/rs_retrieval_summary.csv` at `d055561`:

| variant | n | features | train r_log | **test r_log** | test r_linear | ε % | bias % | MAPE % | SSC range mg/L |
|---|--:|--:|--:|--:|--:|--:|--:|--:|---|
| nir / **sentinel2_msi** | 787 | 13 | 0.9802614949886186 | **0.8958905992406959** | 0.8221718849670736 | 31.4913239467016 | −1.419175214904289 | 60.778163282633514 | 0.283 – 1033.3 |
| nir / landsat8_oli | 787 | 10 | 0.97687502129253 | **0.8857823492676947** | 0.816025821941709 | 35.0303060561723 | −0.7502172772418492 | 66.42652277636707 | 0.283 – 1033.3 |
| no-nir / sentinel2_msi | 2,041 | 10 | 0.9645235161032423 | 0.8239336472336656 | 0.7159926583211268 | 38.37416081961271 | 8.615965362881518 | 74.44147522861627 | 0.1 – 1033.3 |
| no-nir / landsat8_oli | 2,041 | 5 | 0.9572967603009032 | 0.763103716267502 | 0.6237400550493547 | 48.17027601513448 | 8.708639734396485 | 93.28658366273734 | 0.1 – 1033.3 |

**What it is:** a `RandomForestRegressor(500, min_samples_leaf=2)` on **GLORIA-2022 laboratory TSS**
(g/m³ ≡ mg/L), target `log1p(TSS)`, predictors **GLORIA in-situ hyperspectral Rrs convolved to
sensor bands** and their ratios. **There is no satellite pixel anywhere in it**, and `outputs/`
holds **no imagery matchup product at all.**

### 7.2 The leakage is CONFIRMED AND QUANTIFIED — by them, and they retract their own docstring

M4 measured that the split is `train_test_split(test_size=0.30, random_state=seed)` — a plain random
**row** split — and could not measure the inflation because GLORIA is absent. **Their C2 answer
measured it.** `src/mgbsed/remote_sensing/ssc.py:448`, no `groups`, no `GroupShuffleSplit`, on
arrays from which site identity was already dropped (`:441-442`); and of the docstring at
`:427-430` that defends the split — *"GLORIA samples come from many independent water bodies
worldwide, so there is no temporal autocorrelation to leak"* — they write:
***"that defence is empirically wrong for the subset actually used."***

**Site structure of the 787-sample training set:**

| | |
|---|--:|
| distinct `Site_name` | **82** |
| sites with > 1 sample | **58** |
| **samples in repeat-visit sites** | **97 %** |
| largest site: Taihu | **113** samples = **14.36 %** of the set |

(then Lake Kasumigaura 86, Lake Peipsi 67, Lake Hume 39, Red River 35.) *"Under a 70/30 row-random
split the probability that Taihu appears in both train and test is essentially 1."*

**The measured inflation — same features, same RandomForest, 5 seeds, only the split changes:**

| sensor | row-random (as shipped) | **site-grouped (honest)** | inflation |
|---|--:|--:|--:|
| Sentinel-2 MSI | **0.918** (0.917–0.923) | **0.801** (0.755–0.875) | **+0.118** |
| Landsat-8 OLI | **0.905** (0.897–0.914) | **0.781** (0.734–0.878) | **+0.124** |

So: **the reported ≈ 0.896 is inflated by roughly +0.12 and is not a site-independent
generalisation estimate. The retrieval is nonetheless REAL at r ≈ 0.78–0.80 on unseen sites.** And
the **site-grouped spread is much wider** — 0.73–0.88 against 0.90–0.92 — *"That range is the real
uncertainty, and it is driven by which sites land in the test fold."* (Their 5-seed row-random means
0.918 / 0.905 sit above the single shipped CSV row 0.8959 / 0.8858; the difference is seeds, and the
**inflation** is the like-for-like quantity.)

### 7.3 The binding limitation for this basin is REGIONAL TRANSFER, not the split

| | |
|---|--:|
| South American samples in the used subset | **41**, from **3** sites, **all Brazil** (5.21 % of 787) |
| **Colombian samples** | **0** |

Raw `GLORIA_meta_and_lab.csv` holds 7,572 rows / 486 sites / 30 countries, of which 239 South
American TSS > 0 rows (191 of them French overseas territory coordinates). Their conclusion, which
this project adopts:

> *"So the retrieval is applied to the Magdalena with **essentially no regional training data**, and
> it is dominated by temperate lakes (Taihu, Kasumigaura, Peipsi) whose optical properties need not
> resemble an Andean sediment-laden river. **In our view this is a larger threat to validity than
> the split**, and neither of us can currently test it without Magdalena in-situ Rrs.
> **Recommend:** report the site-grouped number, state the zero-Colombia coverage as a limitation,
> and treat the retrieval as indicative rather than calibrated."*

**Grade: UNVALIDATED for this basin**, and the reason is now specific — not "the split is
optimistic" (measured: +0.12) but **"no Colombian and effectively no Andean-river training data
exists in the sample"**, which no re-split can fix. **They found this themselves and reported it
against their own headline number.** That is the behaviour this project's own rules demand of it,
and it should be said plainly.

### 7.4 Why it matters here specifically

Because R1 has an observational dead end that no amount of modelling fixes:

1. **66.53 % of modelled gross *hillslope* erosion — 199.29 of 299.54 Mt/yr at
   `cp_revision='cited_central_2026_08_11'` (conventions in §0) — is upstream of no usable SSC
   station** (`docs/42` G9), and *"above vs below the Momposina"* is **NOT EVALUABLE, measured**
   (`docs/45` §4.1).
2. **B5 proved the flux gauge set cannot grow past ~18** (`docs/57`): all 46 previously unmapped SSC
   stations were geocoded, **43 fall inside the basin**, **44 carry SSC records** — and **0 of 43
   have same-code discharge**, in `discharge_daily` (192 stations) or anywhere in the raw IDEAM
   discharge download. They are sediment-only sampling points.

So the **only** remaining route to that 66.53 % and to the Momposina question is an observation that
does not require a discharge gauge — and **R2 has already built one, and has already told us how
optimistic its headline is.** That is the single most useful thing this comparison surfaces for
future work.

### 7.5 The three limits, plainly, before anyone gets optimistic

1. **It is SURFACE concentration, not depth-integrated.** Satellite reflectance sees the optical
   surface layer; IDEAM's `CM` and our rating curves are not that quantity. (Our own
   `sediment_daily_qc.csv` carries both `ssc_mean_mg_l` and `ssc_surface_mg_l`, so the distinction is
   already live in our data.)
2. **It is CONCENTRATION, not flux — so it cannot supply a flux constraint.** Flux is
   `Q × C × 0.0864`, and the reason the 43 recovered sites are unusable is the **missing Q**, not the
   missing C. **A satellite SSC product does not fix that**, and this is precisely the distinction of
   §3.1. What it *could* constrain is a **concentration** field, a **spatial pattern**, or a
   **contrast ratio** — all valuable, none a flux constraint.
3. **Cloud clearing is not random with respect to rainfall.** Clear-sky days in a wet Andean basin
   are systematically drier days, so any satellite SSC series is **selected on the very variable the
   study contrasts**. This is a selectivity bias of the **same family as `flag_flow_selective`**
   (`docs/34` §1.4's C1.2 gate, which already refuses estimator (a) at flagged stations) — and it
   would bite **hardest on the ENSO contrast**, biasing the wet window toward its drier days.

To which the bundle adds a fourth, larger one: **4. no Colombian and effectively no Andean-river
training data** (§7.3), plus the standing limit that a random forest **cannot extrapolate** above
its training ceiling of **1033.3 mg/L** — a hard bound in a basin whose observed SSC reaches many
thousands of mg/L.

### 7.6 Recommendation — a pre-registration is required, and this document does not write one

**Recommended: pre-register a satellite-SSC evaluation before any retrieval is run against this
basin.** It must fix, in advance and in the `docs/33` / `docs/45` / `docs/46` pattern: the target
quantity (surface vs depth-integrated, and the conversion or the refusal to convert); the split
(**grouped by water body / site**, not random rows — now measured, not merely suspected, as worth
+0.12); **the regional-transfer branch, which is the binding one — what local matchup set is
required and what happens if none can be built**; the cloud-selectivity diagnostic and the
window-composition statistic that would detect it; whether any concentration-only constraint may
enter an objective at all; and the **negative branch** — the words that get published if the route
does not work. **No threshold, tolerance or band is proposed here, and none may be reconstructed
later** (`docs/52` §7). **Nothing is pre-registered by this document.**

---

## 8 — Open items, closed items, and one check we were asked to run

### 8.1 What this comparison could NOT settle

Named as open items with what would settle each. **None of these is a finding.** They are numbered
**X1–X14** so they cannot be confused with `docs/47`'s **O1–O12**, which remain in force unchanged.

| # | open item | what would settle it |
|---|---|---|
| **X1** | **No R2 number was re-executed**, and R2's calibration outputs are **withheld as mid-rewrite** (§0). Their raw data is absent from the clone; the bundle's 20 data files were not extracted here (§1.2). Nothing validates that their artifacts came from the code as committed. | Their post-fix, post-recalibration `stage1_*` / `stage2_*` set, which they have offered to send. **Publishable negative as it stands.** |
| **X2** | **Their per-station paired series and per-window paired summary** (bundle items **B1**, **B2**) — the one thing that would let both projects be scored on **log flux** and put on one metric for the first time. Script 21 reports metrics only and writes no series. | A dump at the Stage 2 best params: per station, per window, n paired days, mean C, mean Q, mean `Qss`, `corr(C,Q)`. **A small CSV, not the 22 GB.** They agree this is the item that matters. |
| **X3** | **Why their pooled SSC MEDIAN ratio (1.333333) sits 14 % below ours (1.525000)** on identical windows while their two means and their Q median agree to 3.5–4.3 %. | `observed_ssc_daily.parquet` + `observed_ssc_stations.csv` (bundle Tier 1, **present in the bundle, not extracted here**). |
| **X4** | **Which stations stand behind their ENSO EDA marginals** (35/27 SSC, 108/93 Q are window counts only), and whether their full **59**-station SSC universe is a subset of our 79. | The same Tier-1 files. **Settleable now; not done.** |
| **X6** | **R1's own DEM provenance for the delineation** — `manifest.json` says COP30; all terrain/LS work is corrected COP90; the processed `cop30_dem.tif` extent cannot produce a 257,096.93 km² basin. **This is ours, not theirs** (§5.4). | Notebook 07's executed output, or the DEM path recorded inside it. |
| **X7** | **The split of R1's land class 6 across WorldCover codes 60 / 70 / 100** — needed to close §5.6's erosion-weighted C comparison, and load-bearing because class 6 is 0.196 % of area but **14.78 %** of our modelled erosion. The tiles on disk cover lat 6–12 only. | The full WorldCover tile set, or a per-code histogram from notebook 05 over the basin mask. |
| **X8** | **Neither C table has been tested against measured erosion**, and `docs/41` remains **unaudited** (`docs/47` **O10**). | An independent adversarial pass on `docs/41`. **Not this document's job, and not C4's** (`docs/47` O10). |
| **X11** | **Their LS2D mean distribution** (only the SUM is quoted, in a docstring: median 9,037, max 344,390) and **their basin sediment level**. Their rainfall (1,965 mm/yr) and K source are now known; these two are not. | `basin_magdalena.pkl` (bundle Tier 2, not extracted here) for LS2D; and for the level, a run they have not dumped. **No "their model produces X Mt/yr" sentence is possible today.** |
| **X12** | **Byte-identity of the shared inputs, beyond the one row tested.** §5.1 proves `minibacia_soil_params.csv` identical by hash; the DEM, WorldCover and precipitation rows still rest on **metadata agreement, not hashes**. And the **DIRECTION** of the sharing — whether R2 derived from our Phase A products, we from theirs, or both from a common advisor pack — is **UNRESOLVED**; this document asserts no direction. | The remaining 19 hashes in `input_hashes.txt` against our files (cheap, not done); and for direction, the advisor. |
| **X13** | **Which soil/K code path R2's shipped run actually used.** Their MANIFEST says `minibacia_soil_params.csv` *"as used"* (and it is byte-identical to ours); their `hru.py:build_k_factor` calls `erodibility_sharpley_williams` on SoilGrids, and their `data_sources.yaml` says SoilGrids is *"comparison and gap-fill only"*. **Two of their own statements conflict at `d055561`.** | Theirs to resolve; one log line from `build_k_factor` (*"K factor: basin mean %.4f, range %.4f–%.4f"*) would do it. **This document quotes both and adjudicates neither.** |
| **X14** | **Whether their fitted `c_mult` = 0.04888 survives the SSC fix.** It came from a fit scored on defective concentration (§3.1), so §5.6's ×26.44 / ×20.46 ratios are arithmetic on published parameters, not statements about what their model needs. | Their post-fix recalibration (§0). |
| — | Minor, grouped: whether their zero-SSC station biased their median beyond the measured +0.0032 (now explained by the defect); their claimed *"uncalibrated ≈ 0.04"* underestimate factor; and their README's *"26 discharge-validated stations"* against 13 in the artifacts (26 is the mapping pool; 13 clear the window). | Their post-fix outputs and `observed_ssc_stations.csv`. |

### 8.2 Items the bundle CLOSED — including two that were closed against R1

| was | now |
|---|---|
| **X5** — which grid produced their parameters, 275 m or 184 m | **CLOSED: 184 m**, `basin_magdalena.pkl` per MANIFEST A8, with LS2D on the routing grid *deliberately* |
| **X9** — whether their production run read our unrepaired `precip_gauges_daily.csv` | **CLOSED: yes, and it did no harm.** It is their default and the only such file in their tree; their QC is in-script and their field is the CHIRPS merge (§5.5). **R1's accusation is withdrawn** |
| **X10** — whether their 0.896 survives a grouped split | **CLOSED, by them: no.** 0.918 → **0.801** site-grouped (S2, +0.118); 0.905 → **0.781** (L8, +0.124); 82 sites, 97 % of samples in repeat-visit sites (§7.2) |
| their **stage 3**: skipped, or ran and found nothing? | **CLOSED as UNANSWERABLE FROM GIT**, by construction — both paths emit byte-identical JSON (`21_calibrate_sediment.py:256-258`, `:300`, `:316-318`, `:328-345`) and no stage-3 rows are ever written. Their re-run: stage 3 **does** fire, **3 rules**, +0.068 → +0.087. *"So the committed empty list was either a skip or an older code path, not a property of the method"* |
| M1's *"they are ahead of us on coordinates"* | **DISCHARGED by `docs/57` (B5)** — §8.5 |

### 8.3 The check R2 asked us to run — and its negative result, which is worth printing

R2 found a real bug on their side and flagged the pattern to us:

> *"stage 3 appended rules, but `TriggerSet` resolves overlaps by **last-match-wins**
> (`src/mgbsed/model/musle.py:204-208`). Two of our three rules shared an identical domain
> (`lower_magdalena / p≥20 / q0.90`), differing only in strength (×2 then ×5) — so **the ×2 rule was
> dead on arrival**, reported as a finding while having zero effect on any catchment-day. Now the
> search replaces rather than appends … **Worth checking your own trigger output for the same
> pattern.**"*

**WE CHECKED. NOT APPLICABLE — this engine has no rule-set or trigger mechanism at all.** Verified
this session, read-only:

```
grep -ric "trigger" src/mgb_sediment.py src/mgb_transport.py   →  0 and 0
grep -ril "trigger" src/                                        →  src/calib_v2.py, src/dhime_dates.py,
                                                                   src/nbgen/make_nb16.py, make_nb17.py
grep -in  "trigger" <those four>                                →  every hit is PROSE about pre-registered
                                                                   TEST triggers (docs/33's BFI term "NOT
                                                                   triggered"; the 25 % single-point leverage
                                                                   trigger at EL PROFUNDO; the H-PEAK refit)
src/mgb_transport.py:521                                        →  k_dep: object = 0.0
```

There is no rule set, no per-domain strength multiplier and no overlap resolution to get wrong.
**C4.3 fits `alpha` and `beta` only, with `k_dep` FIXED at 0.0 /km** (`docs/45` §2.3). A
checked-and-clean is worth printing: it is the difference between *"we do not have that bug"* and
*"we did not look"*.

### 8.4 What R1 OWES R2 — asked for, and worth sending

| # | what | why |
|---|---|---|
| **1** | **Our `selectivity` statistic**, with its definition and code path (`docs/16` §4.1, `docs/23` §12, the `Inferido_seco` repair) | **They asked for it and intend to adopt it**, in their own words: *"Our 80 % completeness cutoff is blunt: it discards 199 of 287 gauges, including honest sparse reporters. Your `selectivity` statistic — computed only from dense neighbours, so it is immune to the station's own wetness — separates biased reporters from merely sparse ones. That would let us retain fair sparse gauges and densify the merge instead of throwing them away. Credit where due; we plan to implement it."* **This is the clearest reciprocity item in the comparison and it is ours to send.** |
| **2** | **Our metric definitions, stated explicitly** — transform (`KGE_ln` on log flux), aggregation (**median**, `F_report`), station count (**8** CAL of 18 usable of 79), in-sample vs held-out, and the ε convention | They asked, on the strength of a finding that binds us: *"on our data these ranked trials in **opposite order**"* for median vs area-weighted mean. **R1 has never measured whether its own trial ranking is aggregation-dependent.** Sending the definitions is the minimum; measuring the sensitivity is a separate, unregistered question and **this document does not open it** |
| **3** | **Three courtesy items** | the stale `stage1_hydrology_params.json` `note` (§3.2); their README's two internal mismatches; and `scripts/15_build_forcing_v2.py:build_etp`'s domain loop `chunk = got if chunk is None else chunk`, which makes the `east_strip` ERA5-Land file unreachable so centroids east of −72.9 silently take the basin file's nearest edge cell. **Offered as reciprocity for §5.5, which they found for us** |

### 8.5 One item this comparison CLOSED, and it closed against a reading that flattered R2

M1 concluded *"they are ahead of us on coordinates"* — 8 of their 21 fitted stations were excluded
by our C1.0 for absent lat/lon, sourced by them from an IDEAM station catalog we did not hold. **As
of C1.0 that was true. It was discharged by `docs/57` (B5) on 2026-08-12**, the day before this
document. This writer verified it directly, read-only, because publishing M1's sentence unqualified
would have been wrong:

| code | lat | lon | minibacia | in basin | n SSC | same-code Q? |
|---|--:|--:|--:|---|--:|---|
| 21187030 | 4.231946 | −75.092981 | 14265 | ✔ | 5,853 | **no** |
| 22027010 | 3.328278 | −75.613111 | 15927 | ✔ | 6,253 | **no** |
| 24017830 | 5.618389 | −73.612861 | 11540 | ✔ | 5,829 | **no** |
| 24037030 | 5.681722 | −73.231139 | 11404 | ✔ | 5,147 | **no** |
| 24037040 | 6.453972 | −72.403056 | 9910 | ✔ | 6,253 | **no** |
| 24037130 | 5.748833 | −73.189889 | 11319 | ✔ | 6,253 | **no** |
| 26177030 | 4.892500 | −75.882694 | 12893 | ✔ | 6,642 | **no** |
| 28037090 | 9.648193 | −73.646367 | 3909 | ✔ | 3,133 | **no** |

All 46 recovered codes: **43 in basin**, and **`self_paired_q` False for 46 of 46**.

**This is the exact, measured reason their n = 21 exceeds our n = 18, and it exonerates both
projects.** Of their 13 stations not in our usable 18: **8** were excluded by us for absent
coordinates (**now recovered** — and still unusable *by us*, because they have no discharge), **4**
fall outside our 8,672-minibacia delineation (29067010, 29067050, 29067120, 29067130 — lower
Magdalena / Ciénaga Grande, lat 10.5–10.8), and **1** (21217250 BOCATOMA) on data grounds
(single-window coverage, La Niña 344 / El Niño 0; flow-selective 0.551; rating R² 0.145 on
n = 7,049). **So the 21-vs-18 difference is a domain, geolocation and objective difference — not
laxity on their side, and not a defect on ours once B5 landed.** Their objective scores
concentration and needs no paired Q; ours scores flux and cannot exist without it. Both are right on
their own terms, and §6.2 states the two admissibility bars side by side rather than the two counts.

One consequence for us, recorded not resolved: **B measured on 6 tributary/Cauca gauges cannot be
measured at their 4 delta gauges at all** — and those are exactly where C–Q coupling is most likely
to differ from our tributary sample (part of **X2**).

---

## 9 — Disclosure

- **Files written by this pass:** `docs/59_cross_implementation_comparison.md` (this file) and
  `docs/agents/journal_x59-write.md`. **Nothing else.** `docs/16`, `docs/34`, `docs/41`, `docs/45`,
  `docs/55`, `docs/56`, `docs/57`, `docs/58`, `docs/00_INDEX.md`, `progress_map.html`, every notebook
  and every source file were **read and not edited**. What this comparison owes them is in **§10**,
  not enacted here.
- **R2's clone was READ-ONLY.** Nothing in it was written, nothing in it was executed, and **no git
  command was run in either repository.** Read-only inspection of their committed `config/`,
  `scripts/`, `src/`, `outputs/`, `tests/` and README only. Their `data/`, `data_Final/`,
  `data_chirps/` and `data precip` are absent and were verified absent by listing. The
  2026-08-13 bundle was read as **three text files** (`MANIFEST.md`, `ANSWERS_C1_C2_C3.md`,
  `input_hashes.txt`); **its 20 data files were not extracted into this repository and none was
  opened** (§1.2). `data/raw/refs/yben409_sediment_repo.bundle` was **hashed and not unpacked**.
- **No engine default moved. No fit was run. No calibration was launched. No simulation was run.
  No α̂ of ours was produced or quoted. No frozen artifact was opened or written** —
  `data/processed/sim_calibrated_v2/*` (including `parameters_H2E.csv`, `q_gauge_H2E.npz`,
  `report_H2E.json`, `h2e_drivers.npz`), `urh_ls2d.csv`, `minibacia_ls2d.csv` and
  `urh_ls2d_variants.csv` untouched. **No headline number was moved. Nothing is backdated.**
- **Measured here vs carried and cited.** Everything attributed to M1–M4 is **carried** from
  `docs/agents/journal_x59-{overlap,bridge,inputs,theirnumbers}.md` and cited in place; those four
  passes were themselves read-only. Everything attributed to `MANIFEST.md` or `ANSWERS_C1_C2_C3.md`
  is **quoted from the counterpart author**, with their own `file:line` citations preserved.
  **This writer made four measurements of its own**, all read-only, all logged with command and
  output in `docs/agents/journal_x59-write.md`:
  1. **The soils hash** (§5.1) — `sha256sum data/processed/minibacia_soil_params.csv` =
     `6e5940ec…38d82`, matching `input_hashes.txt`'s entry for
     `02_basin_and_soils/minibacia_soil_params.csv`. **The one hash-level proof of a shared input in
     this document, and it reversed M3's soils ruling.**
  2. **The trigger-mechanism check** (§8.3) — negative, and printed as such.
  3. **The `docs/57` reconciliation** (§8.5), made because M1's coordinate finding would otherwise
     have been published in a form `docs/57` had already superseded.
  4. **The rainfall comparator** — `grep` of `docs/16` §14 confirming our figures are **2,036.4**
     (2009–2017) / **2,073.1** (2008–2018) mm/yr and that **2,206 is stale**; and the derived gaps
     3.5061873895109055 % / 5.2144131976267385 %. Quoting the stale 2,206 would have manufactured a
     disagreement with their 1,965 that does not exist.
  Plus the git-bundle hash of §0. All our-side numbers quoted in §3–§7 were re-verified against
  their owning documents and the verification table is in that journal §1.3.
- **One numeric disagreement between two measurement passes was resolved by recomputation, not by
  preference.** M1 reported their validation `alpha × c_mult` as 5.5818822479283315 and M4 as
  5.581900193275565. From the two JSON fields at full precision,
  96.58548959666564 × 0.05779232694874972 = **5.581900193275565** — **M4 is correct; M1's value is a
  rounding artifact.** The derived ratio ×2.0611616793829812 and the score delta
  +0.004409952544391804 are unaffected — **and both are SUSPENDED under §4.3 regardless**, because
  the scores behind them are void.
- **M2's "shared = 8" is reconciled** with M1 §C (identical eight codes) and may be quoted.
- **No threshold, tolerance, materiality bar or band is introduced anywhere in this document, and
  none is reconstructed** (`docs/52` §7 — four have been retired on that rule). Every figure is a
  ratio, a count, a containment fraction, a day count or a hash, with the artifact it came from. The
  words **CONSISTENT**, **NOT COMPARABLE** and **VOID** describe *commensurability and validity* —
  whether two quantities are the same kind of number, and whether one of them was computed on a
  defective series — and are **not** the outcome of any numeric gate. Nothing above passes or fails
  anything. The 3.51 % rainfall gap, the +0.12 retrieval inflation and the 3.5–4.3 % marginal
  agreements are **descriptive differences, not verdicts against a bar**. Counts of "n stations
  inside the bar" are descriptive tallies against the **CITED** Fagundes band that both projects
  already use, not a new gate.
- **`docs/23` §13.2 yield embargo in force.** Absolute flux only — t/day, Mt/yr, mg/L, m³/s.
  **No t/km²/yr appears anywhere in this document.** R2's `5–150 L/s/km²` station screen (§6.2) is a
  **specific-discharge** criterion on hydrology, quoted as theirs, and does not engage the embargo;
  R2's outputs contain no sediment yield figure to quote in any case.
- **Nothing was reasoned backwards from a desired verdict.** The governing results of this document
  — that R2 is **not independent data**; that the score comparison is **VOID**; that the central
  result's **empirical leg is suspended**; and that the shared-inputs argument reaches **one** of the
  four C4.3 suspects — are all *worse* for this project than the alternatives, and all are reported
  as measured. Every item that flattered R1 was checked and corrected against R1: the precipitation
  accusation (§5.5, **withdrawn**), the station-count comparison (§6.2, **their bar is looser for a
  stated reason**), the score comparison (§3, **void, and R1 does not get to keep the favourable
  half**). The one item that flattered R2 (§8.5) was checked and corrected against R2.
- **No claim is made about the correctness of R2's code**, and no measurement here supports one.
  Their raw data is absent from the clone, the bundle's data files were not opened, and nothing was
  executed. Where R2 is careful in ways R1 is not — the self-reported SSC defect, the self-measured
  retrieval leakage, the retracted docstring, the independent precipitation diagnosis, the
  collinearity note, the held-out ENSO design, the same cited bar — §2, §3.1, §4.1, §5.5, §6.1 and
  §7.2 say so.

---

## 10 — Cross-references, and what is OWED to other owners

**Read alongside:** `docs/42` (§3.1 the condition number, §6 G5/G6/G9) · `docs/45` (§2.3 fixed
factors, §3 the objective, §3.4 CAL-8/EVAL-5, §4.1 Momposina NOT EVALUABLE) · `docs/55` (the C4.3
verdict) · `docs/56` (C5) · `docs/34` (the observed contrast) · `docs/32` (SSC admissibility) ·
`docs/57` (B5) · `docs/37` A3 (the LS formulation) · `docs/41` (the C evidence) · `docs/16` §4.1 and
§14 (zero suppression; the basin rainfall figures) · `docs/26` §7 / `docs/18` §15.5 / `docs/58` (the
CHIRPS lever, declared spent) · `docs/33` §5.1 (Phase B re-opening requires a pre-registration) ·
`docs/23` §13.2 (the embargo) · `docs/52` §7 (no reconstructed bands) ·
`data/raw/colleague_share/{MANIFEST.md,ANSWERS_C1_C2_C3.md,input_hashes.txt}` and
`data/raw/refs/yben409_sediment_repo.bundle` (the pinned counterpart evidence).

**OWED, not enacted here.** Each item names the owner; this document has no authority over any of
them.

| # | owed to | what is owed |
|---|---|---|
| 1 | **`docs/56`** §4 (*"What this is, and is NOT"*) | A line recording that the external ENSO comparator is **methodological, not data-independent**, with the containment figures (21/21, 13/13, 90/90), the window nesting, **and the byte-identical soil/K table** — so the C5 concordance is never quoted as independent replication. And a pointer that a **model-vs-model** check (their B3, held-out 2011 / 2015–17 load ratio against our 3.046755091543662) is **in progress on their side**, not available today. §6. |
| 2 | **`docs/34`** | Two notes: (i) an independent reimplementation reproduced its **6 of 6** primary estimator-(a) ratios and its median (4.620164 vs 4.62) **to printed precision** (§6.7) — an unusually clean external check of the estimator, though **not** of its QC; (ii) the §1.2 pooling prohibition now has an external illustration — pooling moves the implied bridge factor by 5–20× the covariance term and flips the pooled Q ratio below 1 (§6.4). |
| 3 | **`src/build_data_final.py`** + **`docs/16`** §4.1 | The handoff router ships `precip_gauges_daily.csv` and never the `_qc` files, against this project's own standing rule. **State it at its true size:** it caused no harm, because the recipient applied its own in-script QC and a CHIRPS merge (§5.5). A fix to the router, and a note that R1's inference from the router to the recipient's forcing was **wrong and is withdrawn**. |
| 4 | **`docs/41`** owner, and **`docs/47` O10** | The `docs/41` audit is **still owed and still unopened**. §5.6 supplies it a concrete external comparator (a sibling C table ×1.29–×1.99 lower before any fit, from the same WorldCover raster) and one specific target: the code 60/70/100 → class-6 mapping, 0.196 % of area but **14.78 %** of modelled erosion (**X7**). Note also **X14**: their `c_mult` is a pre-fix number. This document does **not** discharge O10. |
| 5 | **`docs/32`** | Their admissibility bar, for the record beside ours: **59 archived → 57 plausible**, of which **32 admitted on a proximity snap** (reach ≥ 20 km², snap ≤ 15 km), against our **79 → 18 usable**. Our bar is stricter because our objective is on **flux** and needs paired discharge; theirs is on concentration and does not. §6.2. |
| 6 | **`docs/57`** (B5) | An annotation that B5 discharged an external-facing exclusion — the 8 stations R2 fitted and our C1.0 dropped for absent lat/lon are all recovered, all in-basin, all rich in SSC — and that `self_paired_q` **False 46/46** is the measured reason their n = 21 exceeds our n = 18. §8.5. |
| 7 | **`docs/26`** §7 / **`docs/18`** §15.5 / **`docs/58`** owners, and whoever writes a Phase-B pre-registration | **A NAMED CANDIDATE, recorded and not proposed.** `docs/26` §7 called the CHIRPS-gauge merge *"the only remaining lever"* and `docs/18` §15.5 declared *"no route to a passing volume gate exists inside the merge code."* **R2 implemented a merge that runs as its default and lands at 1,965 mm/yr** — 3.51 % **below** our 2,036.4 on the matching 2009–2017 span, i.e. the opposite direction from our own merge's +7.5 % volume failure. Its construction, in specifics we never tried: **88 gauges at ≥ 80 % completeness for the LEVEL, CHIRPS for the PATTERN, monthly log-ratio, IDW-interpolated, applied multiplicatively, ratios clipped 0.25–4.0, ≥ 10 shared days per gauge-month.** **Phase B is CLOSED on H2E; re-opening it requires a new pre-registration (`docs/33` §5.1). This document proposes nothing and re-opens nothing.** §5.8. |
| 8 | **`docs/45`** §4.1 / **`docs/42`** G9 owners | The **NOT EVALUABLE** Momposina row and the **66.53 %** unobserved fraction now have a *candidate* route (satellite SSC, §7) that does not require a discharge gauge — recorded as a candidate only, with its measured inflation (**+0.12** row-random vs site-grouped) and its **binding** limitation (**0 Colombian, 41 South American samples from 3 Brazilian sites**). §7.6 **recommends a pre-registration and writes none.** Nothing in G9 or §4.1 changes. |
| 9 | **`docs/00_INDEX.md`** owner, and `progress_map.html` | A status row for `docs/59` (live), a WHERE-IS-IT entry for *"is there an external check on this project?"*, and the answer: **independent implementation, not independent data — and no score comparison exists.** Plus the pin: `d055561`, bundle sha256 `adf7a1d1…ca9e`, dated 2026-08-13, **counterpart numbers expected to change**. |
| 10 | **R2's authors** | §8.4: **(1)** our `selectivity` statistic, which they asked for and intend to adopt; **(2)** our metric definitions stated explicitly — transform, aggregation, gauge count, in-sample vs held-out — as they asked, on the strength of their finding that **median and area-weighted mean ranked their trials in opposite order**; **(3)** three courtesy code notes. And one ask, in priority order: **X2** (the per-station paired series / the B1–B2 dump — a small CSV), then their **post-fix** stage-2 set (**X1**, **X14**), then **B3** (§6.1), then Tier-1 `observed_ssc_stations.csv` (**X3**, **X4**), then the direction of the shared data (**X12**), which only the advisor can answer. |
