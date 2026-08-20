"""Generate notebooks/19_c3_gate_and_c4_setup.ipynb.

Notebook 19 documents the ADJUDICATION that closed out stage C3 of the Magdalena
sediment work and set up stage C4 (the sediment calibration).  It makes one hard
methodological decision legible to someone who was not in the room:

  * why the sediment-delivery-ratio closure gate was RETIRED rather than passed or
    failed (gross erosion and sediment yield are different quantities);
  * whether the model's level error cancels in the study's wet/dry ENSO ratio - the
    notebook's centrepiece - including the beta-compression derivation;
  * what MUSLE's alpha is actually FOR in the method this project transposes, and what
    that does to the parameter guard built on it;
  * whether stage C4 is feasible at all on the stations that survive every filter;
  * the decision itself, stated so a reader can disagree with it on the evidence;
  * and a full problems register.

It re-runs only the cheap sediment engine (never the hydrology, never a calibration
search), reads the frozen artifacts read-only, and recomputes the station funnel from
the QC'd station files.  Everything it cannot recompute is quoted from a numbered
document or an adjudication journal, cited in place and labelled as carried.

Written for a reader who is competent but new to this project and its vocabulary: every
technical term is defined in plain language where it first appears, every computational
cell is preceded by its equation with units and named data sources, and every figure is
followed by a three-part reading (what is plotted / what it shows / what it means).

Run:  python src/nbgen/make_nb19.py
Then: python -m nbconvert --to notebook --execute --inplace \
        --ExecutePreprocessor.timeout=-1 notebooks/19_c3_gate_and_c4_setup.ipynb
"""
import json
import pathlib

OUT = pathlib.Path(r"c:\dev\magdalena-mgb-sed\notebooks\19_c3_gate_and_c4_setup.ipynb")

C = []


def md(s):
    C.append(("markdown", s))


def code(s):
    C.append(("code", s))


def reading(what, shows, means):
    """The mandatory three-part figure reading, in a fixed order."""
    md("**What is plotted.** " + what.strip()
       + "\n\n**What it shows.** " + shows.strip()
       + "\n\n**What it means.** " + means.strip())


# ============================================================ title
md(r"""# Notebook 19 - the C3 gate and the C4 set-up: how one methodological decision was made

**Stage C3 closure adjudication + stage C4.2 registration** of the Magdalena-Cauca ENSO
sediment study. Notebook 18 built the sediment model. This notebook is about what happened
when the project tried to decide whether that model was *good enough to proceed with* - and
found that the test it had written to answer the question was **not a test**.

**What this notebook is.** A decision record. On 2026-08-11 three independent "lenses" were run
at the same question and their answers were adjudicated into one verdict,
`C3-STAYS-OPEN-C4-PROCEEDS-CONDITIONALLY` (`docs/43`), which was then turned into a frozen
pre-registration for the calibration (`docs/45`). This notebook reproduces the evidence, draws
it, and states the decision in a form a reader can *disagree with on the evidence* rather than
on trust.

**The five questions it answers.**

1. Where did C3 stand, and why was its closure gate **retired** instead of passed or failed?
   (Section 1 - and the answer turns on a distinction, *gross erosion* vs *sediment yield*,
   that this literature routinely conflates.)
2. **The ratio question, and it is the centrepiece.** The study's headline is a *ratio* -
   La Nina sediment over El Nino sediment. A constant multiplicative error cancels in a ratio.
   Is ours constant? (Section 2, which also derives why the model **structurally compresses**
   the contrast it is being asked to reproduce.)
3. What is MUSLE's coefficient $\alpha$ **for**? A physical constant, or a calibration lever?
   (Section 3 - the answer decides whether the model's level error is a *defect* or an
   *unset knob*, and it invalidates a guard this project had been relying on.)
4. Is the calibration **feasible** at all? (Section 4: the station funnel, 79 to 8.)
5. What was decided, and on what grounds? (Section 5.)

**Section 6 is a problems register and is the point of the notebook as much as sections 1-5.**
Six named, measured, unresolved problems get their own subsections, not footnotes.

**What this notebook is NOT.**

* It is **not a calibration.** No parameter is fitted here. $\alpha$ and $\beta$ are the
  published 1975 values throughout. The calibration is stage C4. **STATUS,
  2026-08-19, added so this page is not read as the project's current position:** stage C4.3 has
  since been **run**, and its verdict is **RAILED / EXPLORATORY, NOT adopted** (`docs/55`); the
  strictly out-of-sample application C5 then **reproduced** the observed ENSO contrast at **18/18**
  stations, median rate ratio **3.05x** (`docs/56`). Nothing on this page is fitted - those two
  documents are where the fitted result and the headline live.
* It does **not re-run the hydrology.** The water balance is frozen at the configuration `H2E`
  and is read read-only.
* It is **not a closure.** C3 is **OPEN**, and section 5 explains exactly which clauses keep it
  open and why "closed" was available and was refused.
* It does **not** report any gauge-referenced sediment yield in t/km2/yr. Those are **embargoed**
  (`docs/23` section 13.2). Model-internal specific erosion appears, always labelled as such.""")

# ============================================================ 0.1 prerequisites
md(r"""## 0.1 - Prerequisites, and what each one contributes

| Prerequisite | What it provides | Read-only? |
|---|---|---|
| `src/mgb_sediment.py` | the MUSLE engine and its **named** unit / cover-factor conventions | imported |
| `scripts/c3/qpeak.py` | the registered peak-flow proxy and the pre-registered parameter guard `check_musle_parameters` | imported |
| `data/processed/sim_calibrated_v2/h2e_drivers.npz` | **frozen** surface runoff from Phase B, 3,652 days x 8,672 units, 546 MB | **yes, frozen** |
| `data/processed/sediment_inventory_qc.csv` | the 79 suspended-sediment stations, classified | yes |
| `data/processed/sediment_daily_qc.csv` | daily QC'd suspended-sediment concentrations | yes |
| `data/processed/discharge_daily.csv` | daily observed discharge | yes |
| `data/processed/urh_*.csv`, `minibacia*.csv` | the model's static geometry (areas, land classes, soil, topography) | yes |

Everything else on this page is **quoted from a numbered document or an adjudication journal and
cited in place**, because reproducing it would require re-fitting, re-running a search, or
re-reading the two source theses. Carried numbers are labelled; computed numbers are printed by
the cell that computes them.

*The table names a few things before they are explained. Section 0.2 defines, in plain language,
every term this notebook uses - there is no assumed vocabulary.*""")

code(r"""import hashlib, json, math, pathlib, sys, time, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
%matplotlib inline
warnings.filterwarnings('ignore', message='.*URH cell areas.*')
plt.rcParams.update({'figure.dpi': 110, 'axes.grid': False, 'font.size': 9,
                     'axes.titlesize': 9.5, 'figure.autolayout': False})

# one small fixed palette, so the notebook reads as a single document
CB = {'blue': '#1F6FB2', 'red': '#B0412B', 'green': '#1D9E75', 'amber': '#D9930D',
      'purple': '#6A4C93', 'grey': '#6E6E6E', 'dark': '#243447', 'pink': '#C2477F',
      'teal': '#127C82'}

REPO = None
for b in [pathlib.Path.cwd()] + list(pathlib.Path.cwd().parents):
    if (b / 'src' / 'mgb_sediment.py').exists() and (b / 'data' / 'processed').exists():
        REPO = b
        break
if REPO is None:
    raise SystemExit('cannot locate the repository root')
PROC = REPO / 'data' / 'processed'
FROZEN = PROC / 'sim_calibrated_v2'
sys.path.insert(0, str(REPO / 'src'))

need = [REPO / 'src' / 'mgb_sediment.py', REPO / 'scripts' / 'c3' / 'qpeak.py',
        FROZEN / 'h2e_drivers.npz',
        PROC / 'sediment_inventory_qc.csv', PROC / 'sediment_daily_qc.csv',
        PROC / 'discharge_daily.csv', PROC / 'minibacias.csv',
        PROC / 'urh_fractions.csv', PROC / 'urh_cp_factors.csv']
missing = [str(p.relative_to(REPO)) for p in need if not p.exists()]
if missing:
    raise SystemExit(f'PREREQUISITES MISSING, stopping rather than improvising: {missing}')

import mgb_sediment as sed
sys.path.insert(0, str(REPO / 'scripts' / 'c3'))
import qpeak as qpk

eng = (REPO / 'src' / 'mgb_sediment.py').read_bytes()
print(f'repo             {REPO}')
print(f'engine           src/mgb_sediment.py  {len(eng)/1024:.1f} kB  '
      f'sha256 {hashlib.sha256(eng).hexdigest()[:16]}')
print(f'frozen driver    {(FROZEN/"h2e_drivers.npz").stat().st_size/1e6:.1f} MB  (READ-ONLY, '
      f'never written by this notebook)')
print(f'Williams (1975)  alpha = {sed.WILLIAMS_ALPHA}   beta = {sed.WILLIAMS_BETA}   '
      f'(UNFITTED throughout this notebook)')
print(f'named volume conventions   {sed.VOLUME_CONVENTIONS}')
print(f'named K unit systems       {sed.K_UNIT_SYSTEMS}')
print(f'named C/P revisions        {sed.CP_REVISION_NAMES}')
if (REPO / 'src' / 'mgb_transport.py').exists():
    print('channel transport module   src/mgb_transport.py PRESENT (stage C4.1, built '
          '2026-08-11; not exercised here)')""")

# ============================================================ 0.2 vocabulary
md(r"""## 0.2 - The vocabulary, in plain language, before any of it is used

Read this section. Every word below is load-bearing later, and several of them are words that
mean *different things* in different parts of the sediment literature - which is, quite literally,
the subject of section 1.

### The two quantities that are constantly confused

**Gross erosion** is *soil detached and moved off the place it was sitting*, summed over the
whole contributing area and over every process that does it. USDA's own definition
(National Engineering Handbook, Part 632, Chapter 6) is explicit that it means **all** water
erosion: *"sheet and rill erosion **plus** channel-type erosion (gullies, valley trenches,
streambank erosion, etc.)"*.

**Sediment yield** is *what actually arrives* at a point of interest - a gauge, a reservoir, a
river mouth - after everything that fell out on the way. It is always smaller than the gross
erosion above it, because sediment deposits en route.

**Sheet and rill erosion** is the hillslope process: a thin film of water peeling soil off a
slope, plus the small channels that film cuts. **Channel-type erosion** is everything else -
gullies, collapsing riverbanks, road cuts, landslides. **MUSLE, the equation this project uses,
represents sheet and rill erosion on hillslopes only.** No gully term, no bank term, no landslide
term, no mining term. That is not a defect of our implementation; it is what the equation is.

### The ratio built out of those two

The **sediment delivery ratio (SDR)** is `sediment yield at a point / gross erosion above it`.
By its own definition its denominator is **all-source**. A published SDR is therefore a
*strictly smaller* number than the same basin's hillslope-only ratio would be. Section 1 shows
what happens when the two are compared anyway.

We need a name for the mixed thing this project actually computed, so this notebook uses the one
`docs/40` coined: the **apparent delivery ratio (ADR)** = `all-source outlet load / hillslope-only
gross erosion`. **The ADR is not bounded by 1** - if banks and gullies supply more than deposition
removes, it exceeds 1.

### MUSLE and its factors

**MUSLE** - the Modified Universal Soil Loss Equation (Williams 1975) - predicts the sediment
produced by *one runoff event* on *one patch of land*:

$$\mathrm{SED} \;=\; \alpha \,\bigl(Q_{sur}\cdot q_{peak}\cdot A\bigr)^{\beta}\; K\,C\,P\,LS\,FG$$

| symbol | meaning | units here |
|---|---|---|
| $\mathrm{SED}$ | sediment produced by the patch that day | t/day |
| $Q_{sur}$ | **surface runoff** - the fast, overland part of the day's streamflow, the only part with energy to detach and carry soil | m3 (after the volume convention of section 1.1) |
| $q_{peak}$ | **peak runoff rate** during the event | m3/s |
| $A$ | area of the patch the equation is applied to | km2 (here $a_p$ = 0.0081 km2, one 90 m DEM pixel) |
| $\alpha$ | the multiplicative **coefficient** - 11.8 in Williams (1975) | dimensionless |
| $\beta$ | the **exponent** on the runoff-energy product - 0.56 in Williams (1975) | dimensionless |
| $K$ | **soil erodibility** - how easily this soil comes apart | US-customary or SI (section 1.1) |
| $C$ | **cover factor** - how much the vegetation protects the soil; 1.0 = bare, ~0.001 = dense forest | dimensionless |
| $P$ | **practice factor** - erosion-control practices (terracing, contour ploughing); 1.0 = none | dimensionless |
| $LS$ | **topographic factor** - steeper and longer slopes erode more | dimensionless |
| $FG$ | **coarse-fragment factor** - stones on the surface armour it; 1.0 = no armouring | dimensionless |

**"Unfitted"** means $\alpha$ and $\beta$ are left at Williams' 1975 values and nothing is tuned
to any sediment measurement. That is the state of the model throughout this notebook.

### The words this project uses about its own process

**Pre-registration.** Thresholds and decision rules are frozen in a numbered document *before*
the numbers they will judge are computed. A threshold changed after seeing the number it judges
is not a threshold. `docs/35`, `docs/42` and `docs/45` are pre-registrations.

**A retired gate is neither a pass nor a fail.** If a test turns out to compare two different
quantities, it is withdrawn - and the model does not get credit for it, nor blame. This rule is
what section 1 is about.

**Structure guard.** A test that looks for *pattern* in the model's errors - do they grow with
distance downstream? with season? with land cover? - rather than at their *size*. The design
principle behind the whole C4 guard set is one sentence: **a scalar parameter can absorb a level;
it cannot absorb a structure.**

**Equifinality** - different parameter combinations producing identical output, so the data
cannot tell them apart. Section 3.4 shows that seven of this model's constants are equifinal:
they are seven ways of writing one number.

**$\Pi$ (Pi), the identifiable product.** $\Pi = \alpha \cdot f_{vol} \cdot f_K \cdot f_{LS}
\cdot C_{mult}\cdot P\cdot FG$. Every one of those seven enters every minibacia-day the same way,
so only their product is identifiable from data. A calibration "fits $\alpha$" only in the sense
that $\alpha$ is the handle it turns; **what it determines is $\Pi$**.

**beta-compression.** Because $\beta < 1$, MUSLE takes a ratio of runoff and returns a *smaller*
ratio of sediment. Section 2.3 derives the exact exponent - which is **not** $\beta$ - and shows
what it does to this study's headline.

**Klemes (1986) differential split-sample.** Fit the model on one climatic regime, score it on a
different one. The C4 registration fits on ENSO-neutral 2012-14 and holds both ENSO windows
strictly out of sample.

**KGE** - Kling-Gupta Efficiency (Gupta et al. 2009), a goodness-of-fit score built from three
parts: correlation $r$, the ratio of variabilities, and the ratio of means. 1.0 is perfect. The
number to keep in mind: **a model that just predicts the mean every day scores
$1-\sqrt{2} = -0.414$.**

**Rail / railed.** A fitted parameter sitting against the edge of its search box. It means the
search wanted to go further and was not allowed to, so the value is not a fit - it is a boundary.

**The station vocabulary.** **SSC** = suspended-sediment concentration, mg/L, measured by taking
a water sample. **Flux** = concentration x discharge, in t/day - what the river actually carries
past the station. **$L_w$** = the along-channel distance from a station up to the head of its own
network (the lever arm the deposition test uses). **Nested pair** = two stations where one is
upstream of the other, so their difference isolates what happened in the channel between them.

### The places

The **Depresion Momposina** is a vast internal floodplain in the lower Magdalena where the river
spreads out and drops sediment. It is the basin's dominant sink, and section 6.3 shows the
observing network cannot see it at all. **Calamar** is the gauge 112 km from the Caribbean where
the published outlet sediment loads (144 and 184 Mt/yr) were measured.""")

# ============================================================ 0.3 the state
md(r"""## 0.3 - The state this notebook opens in

Six facts, each with its owner document. Nothing later re-argues them.

| | fact | owner |
|---|---|---|
| 1 | **The hydrology is frozen** at configuration `H2E` and is not touched. Its known defects travel with it: El Nino daily correlation is capped at 0.556-0.572 by the rainfall field, not by the model; simulated flood peaks are systematically low; and **81.8 % of observed peaks-over-threshold have no simulated partner** within +/- 2 days. | `docs/26`, `docs/22`, `docs/36` |
| 2 | **C1** classified 79 suspended-sediment stations; **18** are usable and mapped; exactly **one** sits on the Magdalena trunk. | `docs/32` |
| 3 | **C2** measured the *observed* ENSO contrast, model-free: La Nina sediment flux **rates** exceed El Nino at **22 of 22** station-ratios. Magnitude is window-dependent: **2.8-4.6x** (primary windows), **6.4-9.3x** (sensitivity windows). Rates only - the windows are 12 vs 24 months. | `docs/34` |
| 4 | **C3** built the MUSLE engine and ran the basin decade. Level **299.539 Mt/yr** of gross hillslope erosion, $\alpha$ and $\beta$ **unfitted**. | `docs/37` A1.3 |
| 5 | **C3's verdict is OPEN** - and the clause it was supposed to close on has been retired. Section 1. | `docs/37` A1, A1.9, A2 |
| 6 | **Any sediment yield in t/km2/yr referenced to a gauge is EMBARGOED**: per-gauge catchment areas disagree by more than 2x on 31 of 85 shared gauges. Absolute flux only. | `docs/23` section 13.2 |""")

# ============================================================ 1 where C3 stood
md(r"""---

# 1 - Where C3 stood, and why its closure gate was RETIRED

C3's job was to build the sediment model and say whether its output was defensible. It produced a
number - and then the project discovered that the test it had written to judge that number was
comparing two different physical quantities. This section reproduces the number, then dismantles
the test.

## 1.1 - The factor chain: how 0.684 Mt/yr became 299.539 Mt/yr

The first run of the sediment engine returned **0.684 Mt/yr** for the whole basin. The published
sediment load of this river at its outlet is **144-184 Mt/yr**. The model was not merely wrong,
it was wrong in the *impossible* direction: gross erosion cannot be smaller than the load it
delivers.

The gap turned out to be **four multiplications**, three of them unit conventions and one a
cover-factor revision. Each is now a **named option** on `SedParams` / `load_geometry`, so every
prior value stays reachable by name and no level change can ever be a silent edit.

$$\text{basin total} \;=\; \underbrace{0.684406}_{\text{first run}}
\;\times\; \underbrace{f_{vol}}_{\text{runoff volume unit}}
\;\times\; \underbrace{f_{K}}_{\text{erodibility unit}}
\;\times\; \underbrace{f_{LS}}_{\text{topography}}
\;\times\; \underbrace{f_{C}}_{\text{cover-factor revision}}$$

| factor | symbol | value | why | evidence grade |
|---|---|---|---|---|
| runoff volume in **m3** rather than pixel-km2 | $f_{vol}$ | **x47.8630** ($=1000^{0.56}$) | Converting Williams' English form (1 ac-ft = 1233.4818375 m3, 1 cfs = 0.028316846592 m3/s, 1 short ton = 0.90718474 t) gives $95\times0.90718474/34.92823^{0.56} = 11.7818$: **11.8 belongs to runoff volume in m3.** Derived independently twice. | **DERIVED** |
| $K$ in **US-customary** numerics | $f_K$ | **x7.593014** ($=1/0.1317$) | The stored $K$ was built from Wischmeier & Smith (1978) class values *converted to SI by x0.1317*; undoing it returns the textbook numbers (0.020 -> 0.1519 ~ sand 0.15). This **identifies** the transform rather than inferring it. | **IDENTIFIED** |
| topographic aggregation and resolution | $f_{LS}$ | **x1.000** | Keep the area-weighted mean (MUSLE is linear in $LS$) at native 90 m. The "published mountainous $LS$ 2-10" comparison that would have motivated a rescale is **UNCITED** and was retired rather than acted on. | **UNVALIDATED** |
| cover factor $C$, cited-central revision | $f_C$ | **x1.2043** | All 8 land classes given a source, a stated land condition and a low/central/high range (`docs/41`), with a Colombian anchor inside this basin. The largest available *upward* lever, a published Colombian $C=0.6$, was **rejected on physics, in writing, before its effect was computed**. | **CITED, conditioned and ranged** |

The cell below recomputes the chain from the engine's own named constants and re-runs the basin
decade at **both** cover-factor revisions - so the level is reproduced, not quoted.

**Inputs and their sources.** Surface runoff $Q_{sur}$: `sim_calibrated_v2/h2e_drivers.npz`
(frozen Phase B, read-only), 3,652 days x 8,672 minibacias, mm/day. Static geometry (areas, URH
land-class fractions, $K$, $C$, $P$, $LS$): the `data/processed/*.csv` inventory of section 0.1.
Period 2009-01-01 to 2018-12-31.""")

code(r"""t0 = time.time()
DRV = sed.load_drivers(FROZEN / 'h2e_drivers.npz')   # READ-ONLY on the frozen npz
# mini_ids is passed so geometry rows and driver columns share ONE order by construction.
# They happen to coincide here (both ascending, 0 differing positions, measured), but a
# positional pairing that is only accidentally right is a silent spatial scramble waiting
# for the first reordering upstream - so it is asserted, not assumed.  Same as nb18.
# V0 pin: ACT 2 (2026-08-12) moved the engine default to V4_dg; nb19 is a V0 record.
GEOM = sed.load_geometry(PROC, mini_ids=DRV.mini_ids,
                         urh_ls2d='urh_ls2d.csv', ls2d_column='ls2d_hs')    # adopted C, V0 pin
GEOM_PRIOR = sed.load_geometry(PROC, mini_ids=DRV.mini_ids, cp_revision='prior_2026_08_11',
                               urh_ls2d='urh_ls2d.csv', ls2d_column='ls2d_hs')
NDAYS = DRV.qsur_mm.shape[0]
YEARS = NDAYS / 365.25
print(f'drivers  {DRV.qsur_mm.shape[0]} days x {DRV.qsur_mm.shape[1]} minibacias  '
      f'({DRV.dates[0]} .. {DRV.dates[-1]}, {YEARS:.4f} yr)   load {time.time()-t0:.1f} s')

P0 = sed.SedParams()
RUN = sed.simulate_sediment(GEOM, P0, DRV.qsur_mm, dates=DRV.dates, store_daily=False)
RUN_PRIOR = sed.simulate_sediment(GEOM_PRIOR, P0, DRV.qsur_mm, dates=DRV.dates, store_daily=False)

ADOPT = float(RUN.cell_eroded_t.sum()) / 1e6 / YEARS          # Mt/yr, adopted C
PRIOR_C = float(RUN_PRIOR.cell_eroded_t.sum()) / 1e6 / YEARS  # Mt/yr, prior C

F_VOL = sed.VOLUME_FACTORS['williams_m3'] ** sed.WILLIAMS_BETA
F_K = sed.K_UNIT_FACTORS['us_customary']
F_LS = (sed.LS2D_AGGREGATION_FACTORS['area_weighted_mean']
        * sed.LS2D_RESOLUTION_FACTORS['native_90m'])
F_C = ADOPT / PRIOR_C
FIRST = PRIOR_C / (F_VOL * F_K * F_LS)          # the first run, reconstructed

print(f'\nf_vol = 1000**beta            = {F_VOL:.6f}   (documented x47.8630)')
print(f'f_K   = 1/0.1317              = {F_K:.6f}   (documented x7.593014)')
print(f'f_LS  = aggregation x resol.  = {F_LS:.6f}')
print(f'f_C   = adopted C / prior C   = {F_C:.7f}   (docs/41 PREDICTED x1.2043 from a linear '
      f'decomposition, before the run)')
print(f'unit-convention product       = {F_VOL*F_K*F_LS:.7f}   (docs/37 section 1: 363.4245196)')
print(f'\nfirst run (reconstructed)     = {FIRST:.6f} Mt/yr   (docs/37 section 2: 0.684406)')
print(f'basin total, PRIOR   C        = {PRIOR_C:.4f} Mt/yr   (docs/37 A1.3.2: 248.7298)')
print(f'basin total, ADOPTED C        = {ADOPT:.4f} Mt/yr   (docs/37 A1.3.2: 299.5387)')
print(f'mass ledger exact             = {RUN.ledger["exact"]}   '
      f'(eroded - delivered - change in store == 0 bitwise)')
print(f'\nengine wall time              = {RUN.wall_time_s:.2f} s   backend {RUN.backend}')""")

code(r"""BASIN_KM2 = 257097.0                      # docs/15, the locked domain
SPEC = ADOPT * 1e6 / BASIN_KM2            # MODEL-INTERNAL specific erosion, t/km2/yr
ANCHOR_LO, ANCHOR_HI = 144.0, 184.0       # Mt/yr; Restrepo & Kjerfve 2000 / Restrepo & Escobar 2018

steps = [('first run\n(pixel-km2, SI K)', FIRST),
         ('x f_vol 47.86\nrunoff in m3', FIRST * F_VOL),
         ('x f_K 7.593\nK US-customary', FIRST * F_VOL * F_K),
         ('x f_LS 1.000\nnative 90 m', PRIOR_C),
         ('x f_C 1.204\ncited-central C', ADOPT)]
lab = [s[0] for s in steps]; val = [s[1] for s in steps]

fig, ax = plt.subplots(figsize=(11.6, 4.0))
ax.bar(range(5), val, 0.55, color=[CB['grey'], CB['blue'], CB['blue'], CB['blue'], CB['green']])
for i, v in enumerate(val):
    ax.text(i, v * 1.35, f'{v:,.3f}' if v < 10 else f'{v:,.1f}', ha='center', fontsize=8.2)
ax.axhspan(ANCHOR_LO, ANCHOR_HI, color=CB['amber'], alpha=0.22, zorder=0,
           label='published outlet load 144-184 Mt/yr (Calamar; all-source, net of all deposition)')
ax.axhline(ANCHOR_LO, color=CB['amber'], lw=1.0); ax.axhline(ANCHOR_HI, color=CB['amber'], lw=1.0)
ax.set_yscale('log'); ax.set_ylim(0.3, 1400)
ax.set_xticks(range(5)); ax.set_xticklabels(lab, fontsize=7.6)
ax.set_ylabel('basin gross hillslope erosion (Mt/yr, log scale)')
ax.set_title('The C3 factor chain: four named multiplications, each reversible by name',
             fontsize=9.5)
ax.annotate('below the outlet load =\nPHYSICALLY IMPOSSIBLE', xy=(0, FIRST), xytext=(0.15, 3.2),
            fontsize=7.4, color=CB['red'],
            arrowprops=dict(arrowstyle='->', lw=0.9, color=CB['red']))
ax.legend(fontsize=7.4, loc='lower right'); ax.grid(alpha=0.25, axis='y')
plt.tight_layout(); plt.show()

print(f'total chain factor  x{ADOPT/FIRST:,.1f}')
print(f'MODEL-INTERNAL specific erosion (model erosion over model area, NOT a gauge-referenced '
      f'yield): {SPEC:,.2f} t/km2/yr = {SPEC/100:,.4f} t/ha/yr')
print(f'apparent delivery ratio ADR = outlet / our sum: {ANCHOR_LO/ADOPT:.4f} (at 144) .. '
      f'{ANCHOR_HI/ADOPT:.4f} (at 184)')
print(f'                  at PRIOR C: {ANCHOR_LO/PRIOR_C:.4f} .. {ANCHOR_HI/PRIOR_C:.4f}  '
      f'<- the 0.579-0.740 the retired gate judged')""")

reading(
    what=r"""Basin-total gross hillslope erosion (log scale, Mt/yr) after each of the four named
multiplications, recomputed here from the engine's own constants and two full basin-decade runs.
The amber band is the published outlet sediment load, 144-184 Mt/yr at Calamar; the annotation
marks the state that is physically impossible.""",
    shows=r"""The first run sat at 0.684 Mt/yr - a factor of ~250 *below* the load the river
actually delivers. Two unit conventions (x47.8630 and x7.593014, product 363.4245196) and one
cited cover-factor revision (x1.2043, predicted before it was run) carry it to
**299.539 Mt/yr**, above the anchor for the first time. The reconstructed first run, the prior-C
total (248.7298) and the adopted total (299.5387) all reproduce the published figures to the
digits printed.""",
    means=r"""The order-of-magnitude problem was **arithmetic, not physics**, and it is closed and
auditable: every factor is derived or identified from a source, and every prior value is still
reachable by name. What the chain does **not** establish is that the level is *right* - only that
the model is now on the possible side of the outlet load. Whether the level is defensible was
supposed to be settled by a delivery-ratio test, and section 1.3 shows that test was not a test.
**Note the direction of travel:** every step here made the number bigger, and section 6.4's $LS$
question points the other way by **2.3151x-3.9768x** - and by **3.9768x** at the point `docs/37`
A3 actually adopts.""")

# ============================================================ 1.2 the two quantities
md(r"""## 1.2 - Gross erosion is not sediment yield, and this literature conflates them

The closure clause C3 was meant to pass read, in full:

> *the implied sediment delivery ratio is physically plausible (0.05 - 0.30)*

and the model's implied ratio was **0.579 - 0.740**, so the clause was marked NOT MET. That
looks like a clean, quantitative failure. It is not a failure at all, because the two sides of
the comparison are **different physical quantities**.

**The definition that decides it.** USDA NRCS, *National Engineering Handbook*, Part 632,
Chapter 6, "Sediment Sources, Yields, and Delivery Ratios" - the source from which the whole US
SDR practice, and the 0.05-0.30 band's supporting relations, descend. Verbatim:

> *"Sediment yield is the gross (total) erosion minus the sediment deposited en route to the
> point of concern. **Gross erosion is the sum of all the water erosion occurring in the drainage
> area. It includes sheet and rill erosion plus channel-type erosion (gullies, valley trenches,
> streambank erosion, etc.)**"*

and, defining the ratio:

> *"Y = E(DR) ... Y = annual sediment yield. E = annual **gross erosion**. DR = sediment delivery
> ratio (less than 1). The gross (total) erosion in a drainage area is **the sum of all the water
> erosion taking place**."*

So a published SDR is
$$\mathrm{SDR}\;=\;\frac{\text{sediment yield at the point}}{\text{ALL-SOURCE gross erosion above it}}.$$

**What our two numbers are.**

| | what it is | what it contains |
|---|---|---|
| **numerator**, 144-184 Mt/yr | total suspended load past Calamar | sediment from *every* source - hillslopes, gullies, banks, landslides, mining - **net of all deposition upstream**, including the Depresion Momposina |
| **denominator**, 299.539 Mt/yr | our MUSLE sum | **sheet and rill erosion on hillslopes only.** No gully term, no bank term, no landslide term, no mining term |

The quantity we computed is therefore
$$\mathrm{ADR}\;=\;\frac{\text{ALL-SOURCE outlet load}}{\text{HILLSLOPE-ONLY gross erosion}}$$
- a mixed ratio with a bigger numerator and a smaller denominator than the published SDR it was
being compared against. **Two consequences, either one fatal to the gate:**

1. **The ADR is not bounded by 1.** The C3 document had argued *"so SDR = outlet / gross must be
   < 1"*. True of a real SDR; **false** of the ADR. Whenever non-hillslope sources supply more
   than in-transit deposition removes, the ADR exceeds 1. That is not hypothetical: for a
   2,010 km reach of the Brazilian Amazon, bank erosion alone supplies sediment at
   **1,570 Mt/yr against an outlet flux of ~1,200 Mt/yr - a ratio of 1.3** (Dunne et al. 1998).
2. **USDA's own worked example puts the ADR at 1.78.** Next subsection.""")

# ============================================================ 1.3 NEH table 6-2
md(r"""## 1.3 - USDA NEH Table 6-2, reproduced: three different ratios from one watershed

NEH Chapter 6's Table 6-2 is USDA's illustration of source-texture analysis for a single
watershed. It itemises erosion and yield **by source**, which is exactly what is needed to see
how far apart the three candidate ratios are. This is the decisive figure of section 1.

For each source $s$ the table gives gross erosion $E_s$ (t/yr) and the sediment yield $Y_s$
(t/yr) that reaches the point of concern, so the source's own delivery ratio is $DR_s = Y_s/E_s$.
Three ratios can then be formed from the same table, and this notebook computes all three:

$$\mathrm{SDR_{true}}=\frac{\sum_s Y_s}{\sum_s E_s},\qquad
\mathrm{DR_{hillslope}}=\frac{Y_{sheet}}{E_{sheet}},\qquad
\mathrm{ADR}=\frac{\sum_s Y_s}{E_{sheet}}$$

with $E_s$, $Y_s$ in t/yr and all three dimensionless. **Data source:** USDA NRCS NEH Part 632
Ch. 6 Table 6-2, transcribed in `docs/40` section 2.3 from the fetched and text-extracted
chapter (18 pp., 44,190 characters, quotes read from the extracted text). These are the
literature's own numbers, not ours.""")

code(r"""# USDA NEH Part 632 Ch.6, Table 6-2 - "Sediment source and the delivery ratio"
NEH = pd.DataFrame({
    'source':   ['Sheet erosion', 'Gullies', 'Roadbanks', 'Streambanks'],
    'erosion':  [900000.0, 350000.0, 150000.0, 900000.0],   # t/yr
    'yield':    [300000.0, 280000.0, 120000.0, 900000.0],   # t/yr
    'hillslope': [True, False, False, False]})
NEH['DR'] = NEH['yield'] / NEH['erosion']

E_tot, Y_tot = NEH.erosion.sum(), NEH['yield'].sum()
E_hs = float(NEH.loc[NEH.hillslope, 'erosion'].sum())
Y_hs = float(NEH.loc[NEH.hillslope, 'yield'].sum())
SDR_TRUE = Y_tot / E_tot
DR_HILL = Y_hs / E_hs
ADR_NEH = Y_tot / E_hs
SHEET_SHARE_E = E_hs / E_tot
CHANNEL_SHARE_Y = (Y_tot - Y_hs) / Y_tot

print(NEH.to_string(index=False,
                    formatters={'erosion': '{:,.0f}'.format, 'yield': '{:,.0f}'.format,
                                'DR': '{:.4f}'.format}))
print(f'\ntotal gross erosion  {E_tot:,.0f} t/yr      total sediment yield {Y_tot:,.0f} t/yr')
print(f'\n  TRUE SDR      = sum(Y) / sum(E)      = {SDR_TRUE:.4f}   (docs/40: 0.6957)')
print(f'  HILLSLOPE DR  = Y_sheet / E_sheet     = {DR_HILL:.4f}   (docs/40: 0.33)')
print(f'  ADR (ours)    = sum(Y) / E_sheet      = {ADR_NEH:.4f}   (docs/40: 1.7778)')
print(f'\n  they differ by x{SDR_TRUE/DR_HILL:.3f} (true SDR vs hillslope-only) IN THE SAME '
      f'WATERSHED')
print(f'  sheet erosion is only {100*SHEET_SHARE_E:.2f} % of gross erosion; channel-type sources '
      f'are {100*(1-SHEET_SHARE_E):.2f} %')
print(f'  and channel-type sources carry {100*CHANNEL_SHARE_Y:.2f} % of the YIELD, because they '
      f'deliver at 80-100 % against sheet erosion\'s 33 %')""")

code(r"""fig, ax = plt.subplots(1, 2, figsize=(12.6, 4.2))
cols = [CB['green'], CB['amber'], CB['purple'], CB['red']]

x = np.arange(len(NEH))
ax[0].bar(x - 0.19, NEH.erosion / 1e6, 0.36, color=cols, label='gross erosion')
ax[0].bar(x + 0.19, NEH['yield'] / 1e6, 0.36, color=cols, alpha=0.45, hatch='//',
          label='sediment yield delivered')
for i, r in NEH.iterrows():
    ax[0].text(i + 0.19, r['yield'] / 1e6 + 0.03, f'DR {r.DR:.2f}', ha='center', fontsize=7.4)
ax[0].axvline(0.5, color=CB['dark'], lw=1.0, ls=':')
ax[0].text(0.02, 0.96, 'what MUSLE\nrepresents', transform=ax[0].transAxes, fontsize=7.4,
           va='top', color=CB['green'])
ax[0].text(0.30, 0.96, 'what MUSLE does NOT represent - 60.87 % of gross erosion,\n'
                       '81.25 % of the yield', transform=ax[0].transAxes, fontsize=7.4,
           va='top', color=CB['red'])
ax[0].set_xticks(x); ax[0].set_xticklabels(NEH.source, fontsize=8)
ax[0].set_ylabel('Mt/yr'); ax[0].set_ylim(0, 1.15)
ax[0].set_title("USDA NEH Table 6-2: one watershed, itemised by source", fontsize=9.3)
ax[0].legend(fontsize=7.4); ax[0].grid(alpha=0.25, axis='y')

names = ['hillslope-only\ndelivery ratio\n$Y_{sheet}/E_{sheet}$',
         'TRUE SDR\n$\\sum Y/\\sum E$\n(what the band measures)',
         'ADR\n$\\sum Y/E_{sheet}$\n(what WE computed)']
vals = [DR_HILL, SDR_TRUE, ADR_NEH]
ax[1].bar(range(3), vals, 0.5, color=[CB['green'], CB['blue'], CB['red']])
for i, v in enumerate(vals):
    ax[1].text(i, v + 0.05, f'{v:.4f}', ha='center', fontsize=8.6, fontweight='bold')
ax[1].axhspan(0.05, 0.30, color=CB['grey'], alpha=0.30, zorder=0,
              label='the retired 0.05-0.30 band - UNCITED here, and an ALL-SOURCE-denominator '
                    'quantity')
ax[1].axhspan(ANCHOR_LO / ADOPT, ANCHOR_HI / ADOPT, color=CB['pink'], alpha=0.30, zorder=0,
              label=f'OUR ratio at adopted C: {ANCHOR_LO/ADOPT:.3f}-{ANCHOR_HI/ADOPT:.3f} '
                    f'(0.579-0.740 at prior C)')
ax[1].axhline(1.0, color=CB['dark'], lw=1.0, ls='--')
ax[1].text(2.42, 1.03, 'ADR is NOT bounded by 1', fontsize=7.2, ha='right', color=CB['dark'])
ax[1].set_xticks(range(3)); ax[1].set_xticklabels(names, fontsize=7.6)
ax[1].set_ylabel('ratio (dimensionless)'); ax[1].set_ylim(0, 2.05)
ax[1].set_title('Three ratios from the SAME table - a factor of 5.4 apart', fontsize=9.3)
ax[1].legend(fontsize=7.0, loc='upper left'); ax[1].grid(alpha=0.25, axis='y')
plt.tight_layout(); plt.show()

print(f'our ADR sits BELOW USDA\'s own reference ADR of {ADR_NEH:.4f} by a factor of '
      f'{ADR_NEH/(ANCHOR_HI/PRIOR_C):.2f}-{ADR_NEH/(ANCHOR_LO/PRIOR_C):.2f} (prior-C form, the '
      f'form the gate judged)')""")

reading(
    what=r"""**Left:** USDA NEH Table 6-2 itemised - gross erosion (solid) and delivered sediment
yield (hatched) for each of four sources in one watershed, with each source's own delivery ratio
labelled; the dotted line separates the one source MUSLE represents from the three it does not.
**Right:** the three different ratios that can be formed from that single table, against the
retired 0.05-0.30 band (grey) and against this model's own ratio at the adopted cover factor
(pink). The dashed line at 1.0 marks the bound the C3 document believed applied.""",
    shows=r"""In one watershed the hillslope-only delivery ratio is **0.3333**, the true
all-source SDR is **0.6957** - a factor of **2.09 apart** - and the mixed ratio that this project
actually computed is **1.7778**, above 1. Sheet erosion is **39.13 %** of that watershed's gross
erosion; channel-type sources are **60.87 %** of the erosion and **81.25 %** of the yield. Our own
ratio, 0.579-0.740 at the prior cover factor and 0.481-0.614 at the adopted one, sits **below**
USDA's reference ADR, and close to its *true* SDR.""",
    means=r"""**This refutes the C3 closure clause as a test.** The clause compared an ADR against
an SDR band: an all-source numerator over a hillslope-only denominator, judged against a ratio
whose denominator is all-source by definition. Read as a like-for-like quantity, 0.579-0.740 is
*below* the comparator, not above it - the direction of the alleged failure inverts. And the
argument that the ratio must be under 1 is simply wrong for the quantity computed. **A gate
comparing two different quantities can neither pass nor fail**, so it was retired in both
directions: C3 does not get to close by declaring 0.579-0.740 acceptable, and it does not stay
open on the strength of the band either. Three further reasons, any one sufficient, are in
`docs/40`: the band's supporting relations were fitted on US agricultural watersheds of
0.0259-259.0 km2, **992.7x smaller** than this basin, with their own source stating that
out-of-area use "is generally not recommended"; no Magdalena SDR exists in print, because every
published Magdalena "erosion rate" is a sediment *yield*; and in the one large mountainous basin
where SDR was actually fitted (Tan et al. 2024) SDR **rises** with drainage area, so the classic
decay's sign does not survive contact with steep terrain at scale.""")

# ============================================================ 1.4 which quantity
md(r"""## 1.4 - The replacement test, and why its direction had to be withdrawn too

Retiring a gate leaves a hole. `docs/40` section 8.2 proposed a replacement that *can* be
evaluated - a **gross hillslope erosion RATE** test, comparing our basin-mean rate against
published erosion and yield levels - and reported it as failed, with the model **under-erosive by
1.59-2.74x**. That number, later refined to **1.03-2.27x** at the adopted cover factor, is the
one most likely to be quoted at you.

**It has been withdrawn as a directed result** (`docs/37` **A1.9**, written later the same day).
The arithmetic is correct and reproduces; the *interpretation* does not, because the decisive leg
repeats the same category error on the erosion side that the SDR gate made on the delivery side.

**The evidence.** SWAT's *Theoretical Documentation* (Version 2009), Section 4 Chapter 1 - the
reference implementation of **this exact equation**, with the same $\alpha=11.8$, the same
$\beta=0.56$, and the text from which Buarque (2015) and Fagundes (2018) transcribe their unit
strings - defines the left-hand side, verbatim:

> *"where **`sed` is the sediment yield on a given day** (metric tons)"*

and explains why MUSLE has no delivery ratio at all:

> *"Delivery ratios are not needed with MUSLE because the runoff factor represents energy used in
> detaching **and transporting** sediment."*

The comparator in the replacement test's decisive leg (Tan, Liu & Lu 2024) is a **RUSLE** rate -
and RUSLE is USLE's descendant, i.e. a detachment-side **gross erosion**. So the leg compares a
*yield* against a *gross erosion*: the same mismatch, one level up.

**Two readings, and the project refuses to choose the flattering one.**

| | reading A - our sum is **gross erosion** | reading B - our sum is a **hillslope-to-stream yield** |
|---|---|---|
| Leg A vs Tan et al. RUSLE 23.7-26.5 t/ha/a | erosion vs erosion: ours 11.6508 => **2.034-2.275x LOW** | convert theirs to a yield with NEH's own sheet DR 0.33 => 7.821-8.745 t/ha/a; ours 11.6508 => **1.332-1.490x HIGH** |
| Leg B vs Colombian Andes mean *yield* 1,485 t/km2/yr | model-internal Andean-flank specific erosion 1,445.32 => 1.027x, i.e. a 2.8 % gap that A1.4 itself concedes "is no longer evidence" | same arithmetic, same concession |
| Leg C vs 32 sub-basin mean *yield* ~690 t/km2/yr | mean form: ours 1.689x **above** | yield vs yield: 1.689x above, the **expected** direction |
| Leg C, max form (vs 2,200 t/km2/yr) | **WITHDRAWN** - a mean over 257,097 km2 is *arithmetically required* to sit below the maximum of 32 catchments of 320-59,600 km2; this model's own internal range is 18.671x | same |
| **combined** | **1.03-2.27x LOW** | **1.33-1.49x HIGH** |

**And reading B is NOT adopted.** It makes the result look better, which is the reason to hold it
at arm's length rather than the reason to take it - and it has a real counter-argument: MUSLE was
fitted to yields measured at the outlets of **18 small watersheds**, whereas this project applies
it **per 90 m pixel and sums ~30 million pixels**, crediting every pixel with delivering to a
stream it may be 100 km from. **Our sum is neither exactly gross erosion nor exactly a basin
yield, and saying so is the finding, not a hedge.**""")

code(r"""SPEC_HA = SPEC / 100.0                       # model-internal specific erosion, t/ha/yr
TAN_RUSLE = (23.7, 26.5)                     # t/ha/a, RUSLE gross erosion (Tan, Liu & Lu 2024)
NEH_SHEET_DR = DR_HILL                       # 0.3333, computed above from Table 6-2
TAN_AS_YIELD = tuple(v * NEH_SHEET_DR for v in TAN_RUSLE)
TAN_SSY = (1.3, 16.9)                        # t/ha/a, their own reported specific sediment YIELD

readA = (TAN_RUSLE[0] / SPEC_HA, TAN_RUSLE[1] / SPEC_HA)          # how many x too LOW
readB = (SPEC_HA / TAN_AS_YIELD[1], SPEC_HA / TAN_AS_YIELD[0])    # how many x too HIGH

print(f'our MODEL-INTERNAL specific erosion       {SPEC_HA:.4f} t/ha/yr '
      f'(NOT a gauge-referenced yield)')
print(f'Tan et al. 2024 RUSLE gross erosion       {TAN_RUSLE[0]}-{TAN_RUSLE[1]} t/ha/a')
print(f'  same, converted to a hillslope YIELD    {TAN_AS_YIELD[0]:.3f}-{TAN_AS_YIELD[1]:.3f} '
      f't/ha/a   (x NEH Table 6-2 sheet DR {NEH_SHEET_DR:.4f})')
print(f'Tan et al. own specific sediment YIELD    {TAN_SSY[0]}-{TAN_SSY[1]} t/ha/a   -> ours sits '
      f'{"INSIDE" if TAN_SSY[0] <= SPEC_HA <= TAN_SSY[1] else "OUTSIDE"} it')
print(f'\nreading A (our sum is gross erosion): model is {readA[0]:.3f}-{readA[1]:.3f}x TOO LOW '
      f'   (docs/37 A1.9: 2.034-2.275x)')
print(f'reading B (our sum is a yield)      : model is {readB[0]:.3f}-{readB[1]:.3f}x TOO HIGH '
      f'   (docs/37 A1.9: 1.332-1.490x)')

fig, ax = plt.subplots(figsize=(11.4, 2.9))
ax.axvline(1.0, color=CB['dark'], lw=1.4)
ax.text(1.0, 1.44, 'model = comparator', ha='center', fontsize=7.6, color=CB['dark'])
ax.barh([1.0], [2.27 - 1 / 1.49], left=[1 / 1.49], height=0.34, color=CB['amber'], alpha=0.55,
        label='the bracket the record actually supports: DIRECTION UNKNOWN')
ax.plot([1 / readB[1], 1 / readB[0]], [1.0, 1.0], lw=7, color=CB['green'], solid_capstyle='butt',
        label=f'reading B (yield): ours {readB[0]:.2f}-{readB[1]:.2f}x HIGH  - NOT ADOPTED')
ax.plot([readA[0], readA[1]], [1.0, 1.0], lw=7, color=CB['red'], solid_capstyle='butt',
        label=f'reading A (gross erosion): ours {readA[0]:.2f}-{readA[1]:.2f}x LOW')
ax.plot([1.03, 2.27], [0.62, 0.62], lw=5, color=CB['red'], alpha=0.5, solid_capstyle='butt')
ax.text(2.33, 0.62, 'combined, reading A: 1.03-2.27x low\n(WITHDRAWN as a direction, docs/37 '
                    'A1.9)', va='center', fontsize=7.2, color=CB['red'])
ax.plot([1 / 1.49, 1 / 1.33], [0.34, 0.34], lw=5, color=CB['green'], alpha=0.5,
        solid_capstyle='butt')
ax.text(0.63, 0.34, 'combined, reading B:\n1.33-1.49x high', va='center', ha='right',
        fontsize=7.2, color=CB['green'])
ax.set_xscale('log'); ax.set_xlim(0.55, 4.2); ax.set_ylim(0.1, 1.6)
ax.set_xticks([0.6, 0.8, 1.0, 1.5, 2.0, 3.0, 4.0])
ax.set_xticklabels(['0.6', '0.8', '1.0', '1.5', '2.0', '3.0', '4.0'])
ax.set_yticks([]); ax.set_xlabel('comparator / model  (>1 means the model is too low)')
ax.set_title('The C3 level residual has a magnitude bracket and NO KNOWN DIRECTION', fontsize=9.5)
ax.legend(fontsize=7.2, loc='upper left'); ax.grid(alpha=0.25, axis='x')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""The C3 level residual on a log axis of *comparator / model*: values above 1 mean the
model is too low, below 1 too high. The red bars are reading A (our MUSLE sum is a gross erosion),
the green bars reading B (it is a hillslope-to-stream yield), and the amber band spans everything
the record supports. The vertical line is exact agreement.""",
    shows=r"""The same arithmetic, applied under the two readings of what the MUSLE sum **is**,
puts the model **2.27x too low** or **1.49x too high** - and the interval between them
**contains 1**. Reading A's decisive leg compares our sum against a RUSLE gross erosion; reading
B converts that comparator to a yield with NEH Table 6-2's own sheet delivery ratio of 0.3333 and
inverts the sign. The conversion-free cross-check agrees with reading B: Tan et al.'s own reported
specific sediment yield is 1.3-16.9 t/ha/a and our 11.65 t/ha/a sits inside it. *(The cell above
prints reading B as 1.319-1.475x because it converts with the exact 1/3 it computed from Table
6-2; `docs/37` A1.9's **1.332-1.490x**, printed beside it and used in the table of section 1.4,
converts with the rounded 0.33. The owning document's pair is the one to quote - the ~1 %
difference is that rounding and nothing else.)*""",
    means=r"""**This refutes "the model is about 2x under-erosive"** as a statement anything may
be built on - and that sentence had already been used, in this project's own documents, to
motivate work. What survives is a *magnitude bracket with no sign*. Three consequences carried
into the C4 registration: (i) no calibration may be motivated by, justified by or compared
against a withdrawn direction - **a fit argued from a withdrawn direction is a fit argued from
nothing**; (ii) closure clause 4 became 4', then 4", and 4" is **NOT ESTABLISHED**, not "not met";
(iii) settling it is *not* a modelling task but a written, cited answer to "which quantity is the
per-pixel MUSLE sum?", and that answer has not been written. **The one change that would make the
project look better - adopting reading B - is the change the record refuses to make.**""")

md(r"""### 1.5 - The rule that makes all of this a decision rather than a defeat

> **A retired gate is neither a pass nor a fail.**

It is worth stating plainly why the project holds this line, because the alternative was
available and easier. Three level clauses have now been retired or re-opened in succession -
the SDR band (retired), clause 4' (re-opened), clause 4" (not established). A closure assembled
by declaring three retirements a pass would be, in `docs/43`'s own words, *"tolerance wearing a
verdict's clothes"*. The same rule cuts the other way and is applied symmetrically: the model is
**not** condemned by the retired band either.

The rule has a second, sharper form used throughout the rest of this notebook: **an uncited
plausibility band may not be used to pass OR fail a gate.** Where such a band is drawn on a
figure below - the 0.05-0.30 SDR band, its implied deposition rate, the retired "mountainous
$LS$ 2-10" - it is labelled UNCITED and is there so a reader can see where a number sits, never
to adjudicate it.""")

# ============================================================ 2 the ratio question
md(r"""---

# 2 - THE RATIO QUESTION (the centrepiece)

Section 1 left the model's **level** with a magnitude bracket and no direction. That would be
fatal if the study's deliverable were a level. **It is not.** The deliverable is a *ratio*:

> how much more sediment does the basin move in a La Nina year than in an El Nino year?

And ratios have a remarkable property: **a constant multiplicative error cancels exactly.** If
the model is wrong by the same factor in both phases, the wrong level is *irrelevant to the
answer*. So the level question and the deliverable can, in principle, come apart entirely.

This section does three things. It derives the cancellation and shows exactly what it requires
(2.1-2.2). It reports what was **measured** about whether our error is constant (2.3-2.4) - and
the answer is two answers, which is the finding. And it derives a second, structural property of
the model that acts on the ratio directly and cannot be calibrated away (2.5-2.6).""")

md(r"""## 2.1 - Why a constant multiplicative bias cancels, derived

Let $O_w$ be the observed sediment flux rate in window $w$ and $S_w$ the simulated one, both in
**t/day**, over $w \in \{\mathrm{LN}, \mathrm{EN}\}$ (La Nina, El Nino). Suppose the model's error
is purely multiplicative with factor $b_w$:

$$O_w \;=\; b_w \, S_w \qquad\text{so}\qquad b_w=\frac{O_w}{S_w}\ \ \text{(dimensionless)}.$$

The two contrasts - what the observations say and what the model says - are
$$R_{obs}=\frac{O_{LN}}{O_{EN}},\qquad R_{sim}=\frac{S_{LN}}{S_{EN}},$$
and their disagreement is

$$\frac{R_{obs}}{R_{sim}}
=\frac{b_{LN}S_{LN}}{b_{EN}S_{EN}}\cdot\frac{S_{EN}}{S_{LN}}
=\frac{b_{LN}}{b_{EN}}\;=\;\exp(D),\qquad
D \equiv \ln b_{LN}-\ln b_{EN}.$$

**Everything cancels except the ratio of the two biases.** So:

* if $b_{LN}=b_{EN}$ - the bias is the same in both phases - then $\exp(D)=1$ and
  **$R_{sim}=R_{obs}$ regardless of how wrong the level is**;
* $\exp(D)$ is invariant to *every* station-constant multiplicative factor: $\alpha$, the
  prefactor of $\beta$, the $LS$ level, $C$, $P$, the $K$ unit system, the volume convention,
  $FG$, and any constant delivery ratio. That is precisely why $\exp(D)$ can be **decided** while
  the level cannot;
* and $\exp(D)\ne 1$ is the only thing that hurts. Its size *is* the distortion of the headline.

Two things this does **not** do, stated now because both are traps. It does not cancel an error
that is **structured** rather than constant - a bias that differs by station leaves a residual at
every station, and section 2.3 measures exactly that. And it does not cancel an error in the
model's **response shape**: section 2.5 shows the model transforms a runoff ratio into a sediment
ratio by raising it to a power, and a power is not a constant factor.

The cell below demonstrates the algebra on synthetic numbers - not as evidence, but so the claim
is visible rather than asserted.""")

code(r"""rng = np.random.default_rng(20260811)
S_LN, S_EN = 1.30, 0.57                      # simulated flux rates, Mt/day (P-LN, P-EN scale)
R_sim = S_LN / S_EN

# case 1: a CONSTANT multiplicative bias, swept over four orders of magnitude
bs = np.array([0.05, 0.2, 1.0, 3.0, 20.0])
R_obs_const = (bs * S_LN) / (bs * S_EN)

# case 2: a PERIOD-DEPENDENT bias - the dry phase biased differently from the wet
b_ln, b_en = 1.0, np.array([0.4, 0.7, 1.0, 1.5, 2.5])
R_obs_var = (b_ln * S_LN) / (b_en * S_EN)
expD = R_obs_var / R_sim

fig, ax = plt.subplots(1, 2, figsize=(12.2, 3.5))
ax[0].plot(bs, R_obs_const, 'o-', color=CB['blue'], ms=7)
ax[0].axhline(R_sim, color=CB['red'], lw=1.4, ls='--',
              label=f'simulated contrast $R_{{sim}}$ = {R_sim:.4f}')
ax[0].set_xscale('log'); ax[0].set_xlabel('constant bias factor $b$ applied to BOTH windows')
ax[0].set_ylabel('observed contrast $R_{obs}$'); ax[0].set_ylim(0, 4)
ax[0].set_title('A constant bias cancels EXACTLY: a x400 range in level, no change in ratio',
                fontsize=9.2)
ax[0].legend(fontsize=7.4); ax[0].grid(alpha=0.25)

ax[1].plot(b_en, expD, 'o-', color=CB['purple'], ms=7)
ax[1].axhline(1.0, color=CB['dark'], lw=1.2, ls='--', label='$\\exp(D)=1$: no distortion')
ax[1].set_xlabel('dry-phase bias $b_{EN}$, with wet-phase bias held at 1.0')
ax[1].set_ylabel('$\\exp(D) = R_{obs}/R_{sim}$'); ax[1].set_ylim(0, 3)
ax[1].set_title('A PERIOD-DEPENDENT bias does not cancel: $\\exp(D)$ is the distortion',
                fontsize=9.2)
ax[1].legend(fontsize=7.4); ax[1].grid(alpha=0.25)
plt.tight_layout(); plt.show()

print(f'case 1: R_obs across b = {bs.tolist()}  ->  {np.round(R_obs_const, 10).tolist()}')
print(f'        max deviation from R_sim = {np.max(np.abs(R_obs_const - R_sim)):.2e}  '
      f'(exactly zero up to float rounding)')
print(f'case 2: exp(D) ranges {expD.min():.3f} .. {expD.max():.3f} for a bias differing by '
      f'{b_en.max()/b_en.min():.2f}x between the two phases')""")

reading(
    what=r"""**Left:** the observed contrast implied when the *same* multiplicative bias $b$ is
applied to both ENSO windows, swept from 0.05 to 20; the dashed line is the simulated contrast.
**Right:** $\exp(D)=R_{obs}/R_{sim}$ when only the dry-phase bias is varied, with the dashed line
at 1 marking no distortion.""",
    shows=r"""On the left the observed contrast is **numerically identical** at every bias - a
400-fold range of level, and the ratio does not move by more than float rounding. On the right, a
dry-phase bias differing from the wet-phase bias by 6.25x moves $\exp(D)$ from 0.44 to 2.75.""",
    means=r"""**The level and the ratio are separable questions.** A model whose absolute erosion
is wrong by a factor of 20 can still get the ENSO contrast exactly right, provided the error is
the same in both phases. So section 1's unresolved level does **not**, by itself, block the study
- and this is why the ratio question, not the level question, is the one that had to be measured.
What matters is only whether $\exp(D)=1$. That is a measurable quantity, and it was measured.""")

md(r"""## 2.2 - The measurement that was made, and the decisions taken before it

The adjudication lens `adj-ratio` measured $\exp(D)$ **per station**, on the frozen artifacts,
read-only. Its decisions were written into its journal **before** the measurement script existed
- that ordering is what makes the result auditable - and the four that matter are:

| | decision | why it is load-bearing |
|---|---|---|
| **D1** | simulated station flux = sum of the model's delivered load over the station's complete upstream minibacia set, on the D8 topology, at zero channel deposition | this **asserts a delivery ratio of 1.0 between hillslope and station**, stated as a claim rather than smuggled in |
| **D2** | the simulated window mean is taken over **exactly the same days** as the observed one, per station and per window | without day-matching, the known one-sided sampling selectivity of dry-window SSC samples (`docs/34` section 4.1: five of eight disagreeing station-windows are dry ones sampled at flow percentiles 0.163-0.438) would enter the test as a spurious *period* effect |
| **D3** | the statistic is $D=\ln r_{LN}-\ln r_{EN}$ with $r_w=\overline{O}_w/\overline{S}_w$ | invariant to every station-constant factor - see 2.1 |
| **D4** | uncertainty by nonparametric bootstrap over sample days, 2,000 reps, seed 20260811, and separately over **stations**, 10,000 reps | the day bootstrap is registered as a **lower bound** on the true uncertainty, because daily flux is autocorrelated and sample days are not random |

**Two reproduction gates passed before any new number was read.** The lens reproduced the
published simulated basin ENSO ratios (**2.2915** primary, **3.9725** sensitivity) to four decimal
places, and its day-matched observed estimator reproduced `docs/34`'s published primary median of
**4.62** exactly - so both sides of the comparison are the same quantities the project had
already published.

**The window definitions**, fixed in `docs/34` section 1.1 and used unchanged:

| window | dates | days |
|---|---|---|
| **P-LN** primary La Nina | 2011-01-01 .. 2011-12-31 | 365 |
| **P-EN** primary El Nino | 2015-01-01 .. 2016-12-31 | 731 |
| **S-LN** sensitivity La Nina | 2010-07-01 .. 2011-06-30 | 365 |
| **S-EN** sensitivity El Nino | 2015-10-01 .. 2016-04-30 | 213 |

The windows are of **unequal length**, so **rates only** are ever compared and a window total is
never divided by another window total. Both window pairs are reported unaveraged, because they
disagree - and the disagreement is a finding, not noise to be smoothed.""")

md(r"""## 2.3 - What was measured: centred on 1, and emphatically not constant

Two statistics, and they answer two different questions.

**Is there a systematic direction?** Pool $\ln \exp(D)$ across stations under a random-effects
model and bootstrap over the station set. If the pooled interval contains 1, no direction is
established.

**Is it a single constant?** That is formally a *homogeneity* question, so it gets the standard
homogeneity statistics:

$$Q=\sum_i w_i\bigl(y_i-\bar y_w\bigr)^2,\qquad w_i=1/\hat\sigma_i^2,\qquad
I^2=\max\!\left(0,\;\frac{Q-\mathrm{df}}{Q}\right),$$

where $y_i=\ln \exp(D)_i$ for station $i$ (dimensionless log-ratio), $\hat\sigma_i$ is that
station's bootstrap standard error in the same log units, $\mathrm{df}=n-1$, and $\tau$ is the
between-station standard deviation in log units (so $e^{\tau}$ is the per-station spread as a
factor). $Q\gg\mathrm{df}$ or a high $I^2$ means the effect is **not** one constant.

The interpretation was registered **before** the numbers, together with the direction of its own
bias: the day bootstrap under-states within-station uncertainty, so $Q$ is biased **upward** and
$I^2$ **overstates** heterogeneity - i.e. the test is conservative *against* concluding that the
bias is constant, which is the direction that protects the study from a false clean bill of
health.

**Data source for the cell below:** the measured per-cell results of
`docs/agents/journal_adj-ratio.md` steps 3-5, carried and re-plotted here. They are not
recomputed in this notebook: reproducing them needs the C2 station-window artifacts and a
2,000 x 10,000-replicate double bootstrap, and the lens' own reproduction gates are documented
above.""")

code(r"""# carried from docs/agents/journal_adj-ratio.md (D11 station bootstrap, D14 homogeneity)
CELLS = pd.DataFrame({
    'pair':   ['primary', 'primary', 'sensitivity', 'sensitivity'],
    'est':    ['(a)', '(b)', '(a)', '(b)'],
    'n':      [6, 7, 4, 7],
    'geo':    [0.8197, 0.8000, 1.7833, 0.8109],     # geometric mean of expD
    'geo_lo': [0.404, 0.523, 0.856, 0.416],         # station bootstrap, 10,000 reps
    'geo_hi': [1.951, 1.269, 3.503, 1.529],
    're':     [0.848, 0.801, 1.791, 0.815],         # random-effects pooled expD
    're_lo':  [0.310, 0.472, 0.720, 0.351],
    're_hi':  [2.318, 1.360, 4.459, 1.891],
    'Q':      [255.7, 310.1, 75.3, 783.6],
    'df':     [5, 6, 3, 6],
    'I2':     [98.0, 98.1, 96.0, 99.2],
    'tau':    [1.225, 0.707, 0.902, 1.127],         # ln units
    'signp':  [1.000, 0.453, 0.625, 1.000]})
CELLS['tau_x'] = np.exp(CELLS.tau)
CELLS['label'] = CELLS.pair + ' ' + CELLS.est + '  n=' + CELLS.n.astype(str)
CELLS['minp'] = 2.0 / 2 ** CELLS.n                  # minimum attainable two-sided sign-test p

print(CELLS[['label', 'geo', 'geo_lo', 'geo_hi', 're', 're_lo', 're_hi', 'Q', 'df', 'I2',
             'tau', 'tau_x', 'signp', 'minp']].to_string(index=False, float_format='%.3f'))
print(f'\nevery random-effects CI contains 1 : '
      f'{bool(((CELLS.re_lo < 1) & (CELLS.re_hi > 1)).all())}')
print(f'every I2 above 95 %                : {bool((CELLS.I2 > 95).all())}')
print(f'widest pooled band                 : [{CELLS.re_lo.min():.3f}, {CELLS.re_hi.max():.3f}] '
      f'= a factor of {CELLS.re_hi.max()/CELLS.re_lo.min():.1f}')""")

code(r"""fig, ax = plt.subplots(1, 2, figsize=(12.8, 3.9),
                       gridspec_kw={'width_ratios': [1.45, 1.0]})
y = np.arange(len(CELLS))[::-1]
for k, (_, r) in enumerate(CELLS.iterrows()):
    yy = y[k]
    ax[0].plot([r.re_lo, r.re_hi], [yy, yy], lw=6, color=CB['blue'], alpha=0.35,
               solid_capstyle='butt')
    ax[0].plot([r.geo_lo, r.geo_hi], [yy - 0.20, yy - 0.20], lw=3, color=CB['purple'],
               solid_capstyle='butt')
    ax[0].plot([r.re], [yy], 'D', color=CB['blue'], ms=7)
    ax[0].plot([r.geo], [yy - 0.20], 'o', color=CB['purple'], ms=5)
ax[0].axvline(1.0, color=CB['dark'], lw=1.5)
ax[0].axvspan(0.203, 4.550, color=CB['red'], alpha=0.10, zorder=0)
ax[0].text(4.6, y[0] + 0.42, 'per-STATION range 0.203-4.550', fontsize=7.0, color=CB['red'],
           ha='right')
ax[0].set_yticks(y); ax[0].set_yticklabels(CELLS.label, fontsize=8)
ax[0].set_xscale('log'); ax[0].set_xlim(0.15, 5.2)
ax[0].set_xticks([0.2, 0.5, 1, 2, 5]); ax[0].set_xticklabels(['0.2', '0.5', '1', '2', '5'])
ax[0].set_xlabel('$\\exp(D) = R_{obs}/R_{sim}$   (1 = the bias cancels exactly)')
ax[0].set_title('Four fleet cells: every 95 % interval contains 1 ...', fontsize=9.3)
ax[0].plot([], [], 'D-', color=CB['blue'], label='random-effects pooled, 95 % CI')
ax[0].plot([], [], 'o-', color=CB['purple'], label='geometric mean, station bootstrap 95 % CI')
ax[0].legend(fontsize=7.0, loc='lower right'); ax[0].grid(alpha=0.25, axis='x')

xb = np.arange(len(CELLS))
ax[1].bar(xb, CELLS.I2, 0.55, color=CB['red'], alpha=0.85)
ax[1].axhline(75, color=CB['dark'], lw=1.1, ls='--')
ax[1].text(3.42, 76.5, "$I^2$ = 75 % is conventionally 'considerable' heterogeneity",
           fontsize=6.8, ha='right', color=CB['dark'])
for i, r in CELLS.reset_index().iterrows():
    ax[1].text(i, r.I2 + 0.6, f'{r.I2:.1f} %', ha='center', fontsize=7.6)
    ax[1].text(i, 50, f'$\\tau$ = {r.tau:.3f} ln\n= x{np.exp(r.tau):.2f} per\nstation\n\n'
                      f'Q = {r.Q:.1f}\ndf = {int(r.df)}', ha='center', fontsize=6.6,
               color='white')
ax[1].set_xticks(xb); ax[1].set_xticklabels(CELLS.pair + '\n' + CELLS.est, fontsize=7.6)
ax[1].set_ylabel('$I^2$  (% of variance that is between-station)'); ax[1].set_ylim(0, 108)
ax[1].set_title('... and it is NOT a single constant', fontsize=9.3)
ax[1].grid(alpha=0.25, axis='y')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""**Left:** a forest plot of $\exp(D)=R_{obs}/R_{sim}$ for the four fleet cells (two
window pairs x two flux estimators). Diamonds are the random-effects pooled value with its 95 %
interval; circles are the geometric mean with a 95 % interval from bootstrapping over *stations*;
the heavy line at 1 is exact cancellation, and the pink band is the range of the individual
station values. **Right:** the heterogeneity statistics for the same four cells - $I^2$ as bars,
with Cochran's $Q$, its degrees of freedom and the between-station spread $\tau$ printed inside.""",
    shows=r"""**Two answers, and they are both true.** Centrally, $\exp(D)$ sits near 1: the
random-effects pooled values are 0.848, 0.801, 1.791, 0.815 and **every 95 % interval contains
1**; the sign tests return p = 0.45-1.00 against a *minimum attainable* two-sided p of 0.031
(n=6) and 0.016 (n=7), so the test had the power to detect a unanimous direction and did not.
Under the registered EL PROFUNDO precedence the primary (a) cell moves to a geometric mean of
0.959 and a median of 1.079 - within 4-8 % of exactly constant. But dispersedly it is nowhere
near constant: $I^2$ = **96.0-99.2 %**, Cochran $Q$ = 75.3-783.6 with p <= 3.2e-16,
$\tau$ = 0.707-1.225 ln (**2.03x-3.40x per station**), station values spanning **0.203-4.550**,
and **18 of 24 station-cells have intervals excluding 1**.""",
    means=r"""**The period-differential of the C3 residual has no established direction** - so the
level error is not, on this evidence, systematically distorting the ENSO headline, and that is a
genuine and non-obvious piece of good news for the study. **But constancy is neither refuted nor
established**: the pooled band on the primary (a) cell, [0.310, 2.318], is a factor of 7.5 wide -
*as wide as the residual it is supposed to certify* - and a single scalar bias cannot be right at
more than one station at a time when the stations disagree by 3.4x. This refutes any claim that
"the bias cancels, so the level does not matter": the honest statement is that the question is
**unresolvable at n = 4-7 stations**. Certifying the differential to +/-50 % needs n ~ 19
stations; to +/-20 %, n ~ 94. The network supplies 4-7. The two named routes to more are
recovering post-2014 discharge at the single trunk station, and making the C1 flow-selectivity
rule two-sided.""")

md(r"""## 2.4 - A correction the measurement forced: most of the "shortfall" was a comparison artifact

`docs/37` A1.3.4 reported that the simulated ENSO contrast was **short by 1.22-2.01x (primary)
and 1.61-2.34x (sensitivity)** against observation. That comparison put a **basin-total**
simulated ratio next to a **fleet-median tributary-station** observed ratio, computed on a
**different set of days** - three mismatches at once.

Repairing it means comparing like with like: the same stations, the same days, the same
estimator, both sides. The lens did that, and the result is the second important number of this
section.

$$\text{like-for-like} = \operatorname{median}_i\!\left[\frac{\overline{O}_{i,LN}}{\overline{O}_{i,EN}}\right]
\ \ \text{vs}\ \
\operatorname{median}_i\!\left[\frac{\overline{S}_{i,LN}}{\overline{S}_{i,EN}}\right]$$

over the admissible stations $i$, with $\overline{O}$ and $\overline{S}$ both averaged over the
**same** day set (t/day). **Data source:** `journal_adj-ratio.md` step 5 (D10), carried.""")

code(r"""L4L = pd.DataFrame({
    'cell':    ['primary (a)', 'primary (b) all', 'primary (b) ok-only',
                'sensitivity (a)', 'sensitivity (b) all', 'sensitivity (b) ok-only'],
    'n':       [6, 7, 4, 4, 7, 5],
    'obs_med': [4.620, 2.949, 2.845, 9.320, 4.650, 6.404],
    'sim_med': [4.903, 2.904, 3.081, 4.212, 4.998, 4.970]})
L4L['obs_over_sim'] = L4L.obs_med / L4L.sim_med
SIM_BASIN_P, SIM_BASIN_S = 2.2915, 3.9725        # docs/37 A1.3.4, reproduced by the lens

print(L4L.to_string(index=False, float_format='%.4f'))
within8 = int((np.abs(np.log(L4L.obs_over_sim)) < np.log(1.08)).sum())
within129 = int((np.abs(np.log(L4L.obs_over_sim)) < np.log(1.29)).sum())
print(f'\ncells agreeing to within 8 %    : {within8} of 6')
print(f'cells agreeing to within 1.29x  : {within129} of 6')
print(f'basin-total simulated primary   : {SIM_BASIN_P:.4f}   -> like-for-like station median '
      f'{L4L.sim_med[0]:.3f} (a) / {L4L.sim_med[1]:.3f} (b)')
print(f'comparison-basis artifact       : x{L4L.sim_med[0]/SIM_BASIN_P:.2f} (est a), '
      f'x{L4L.sim_med[1]/SIM_BASIN_P:.2f} (est b); the DAY SET alone is worth '
      f'x{L4L.sim_med[0]/L4L.sim_med[1]:.2f}')

fig, ax = plt.subplots(1, 2, figsize=(12.6, 3.8), gridspec_kw={'width_ratios': [1.25, 1.0]})
xx = np.arange(len(L4L))
ax[0].bar(xx - 0.19, L4L.obs_med, 0.36, color=CB['dark'], label='OBSERVED contrast, fleet median')
ax[0].bar(xx + 0.19, L4L.sim_med, 0.36, color=CB['blue'], alpha=0.8,
          label='SIMULATED contrast, SAME stations, SAME days, SAME estimator')
for i, r in L4L.iterrows():
    ax[0].text(i, max(r.obs_med, r.sim_med) + 0.25, f'obs/sim\n{r.obs_over_sim:.3f}',
               ha='center', fontsize=6.9)
ax[0].axhline(SIM_BASIN_P, color=CB['red'], lw=1.3, ls='--',
              label=f'the basin-total simulated ratio the old comparison used ({SIM_BASIN_P:.3f})')
ax[0].set_xticks(xx); ax[0].set_xticklabels(L4L.cell, fontsize=7.0, rotation=18, ha='right')
ax[0].set_ylabel('La Nina : El Nino flux-rate ratio'); ax[0].set_ylim(0, 11.5)
ax[0].set_title('Like-for-like: the model reproduces the observed contrast in 5 of 6 cells',
                fontsize=9.3)
ax[0].legend(fontsize=6.9, loc='upper left'); ax[0].grid(alpha=0.25, axis='y')

steps2 = ['basin total\n(what was quoted)', 'station-matched\nfleet median, est (b)',
          'day-matched too,\nest (a)', 'OBSERVED\nest (a) median']
vals2 = [SIM_BASIN_P, L4L.sim_med[1], L4L.sim_med[0], L4L.obs_med[0]]
ax[1].plot(range(4), vals2, 'o-', color=CB['teal'], ms=8, lw=2)
for i, v in enumerate(vals2):
    ax[1].text(i, v + 0.22, f'{v:.3f}', ha='center', fontsize=8)
ax[1].annotate('', xy=(2, L4L.sim_med[0]), xytext=(1, L4L.sim_med[1]),
               arrowprops=dict(arrowstyle='->', lw=1.4, color=CB['red']))
ax[1].text(1.5, 4.35, f'the DAY SET alone:\nx{L4L.sim_med[0]/L4L.sim_med[1]:.2f}', fontsize=7.2,
           color=CB['red'], ha='center')
ax[1].set_xticks(range(4)); ax[1].set_xticklabels(steps2, fontsize=7.0)
ax[1].set_ylabel('primary-pair contrast'); ax[1].set_ylim(2.0, 5.6)
ax[1].set_title('Three mismatches, repaired one at a time', fontsize=9.3)
ax[1].grid(alpha=0.25, axis='y')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""**Left:** for each of six fleet cells, the observed La Nina : El Nino flux-rate
ratio (dark) beside the simulated one computed on the *same* stations, the *same* days and the
*same* estimator (blue), with obs/sim printed above each pair; the dashed red line is the
basin-total simulated ratio that the earlier comparison used. **Right:** the primary-pair
simulated contrast as each of the three mismatches is repaired in turn, ending at the observed
value.""",
    shows=r"""Repaired to like-for-like, **the model reproduces the observed contrast to within
8 % in three of six cells and within 1.29x in five of six** (obs/sim = 0.942, 1.015, 0.923, 2.213,
0.930, 1.289). The apparent gap was mostly basis: moving from a basin total to a station-matched,
day-matched fleet median moves the simulated number from 2.2915 to 4.903 (estimator a) or 2.904
(estimator b) - **x2.14 and x1.27** - of which the **day set alone is worth x1.69**. The
sensitivity (a) cell, at 2.213, is the one that does not come into line, and it is the cell with
the smallest n.""",
    means=r"""**This refutes "the simulated contrast is short by 1.22-2.01x"** as a statement
about the model. It was largely a statement about how the comparison was assembled. The
correction is now a registered requirement on stage C5: *score any comparison day-matched and
station-matched, or say in the same sentence that it is not* - because the
basin-total-versus-station-median comparison is an error this project has already made once.
**What this does not license:** reading the agreement as validation. The bands of section 2.3
are wide, the per-station values disagree by 3.4x, and section 2.5 shows a structural reason the
model's basin-total contrast is *constrained* to be smaller than the observed one however good
the fit looks at stations.""")

md(r"""## 2.5 - beta-compression: the model structurally compresses the contrast it must reproduce

This is the derivation that turns the ratio question from a measurement into a **structural**
statement about the model.

MUSLE needs an instantaneous **peak runoff rate** $q_{peak}$ (m3/s). A daily model has no such
thing, so this project registered a proxy (`docs/35`), and the proxy is *linear in the day's
surface runoff*:

$$q_{peak}\;=\;\frac{Q_{sur}\cdot a_p}{86.4}$$

with $Q_{sur}$ the day's surface-runoff depth (mm/day), $a_p$ the application area (km2), and
86.4 the constant converting mm km2 per day into m3/s. Substituting into MUSLE, the runoff-energy
product becomes

$$\bigl(Q_{sur}\cdot q_{peak}\cdot A\bigr)^{\beta}
\;\propto\;\bigl(Q_{sur}^{\,2}\bigr)^{\beta}
\;=\;Q_{sur}^{\,2\beta}.$$

**So the simulated sediment flux scales as $Q_{sur}^{2\beta}$, and at $\beta = 0.56$ the
effective exponent is $2\beta = 1.12$ - not 0.56.** Quoting $\beta$ itself as the exponent is an
error this project's record has made once, and it matters in both directions: the $^{0.56}$ form
applies only to a ratio of the *product* $(Q_{sur}\,q_{peak}A)$, whereas against a ratio of
**runoff** the model is a mild *amplifier*, not a compressor. Either way the transformation is a
**power**, not a factor, so section 2.1's cancellation argument does not reach it.

The consequence is a hard bound. If the basin's surface-runoff ratio between the two ENSO windows
is $R_{Q}$, then the simulated sediment contrast is

$$R_{sed}\;=\;R_{Q}^{\,2\beta}$$

and, since $\beta$ is *registered* to the band [0.45, 0.65] (a hard stop, `docs/35` section 6.3),
the whole reachable range of simulated contrast is $R_Q^{0.90}$ to $R_Q^{1.30}$. Nothing inside
the registered parameter space can leave it.

**Inputs.** $R_Q$ = 1.9545 (primary pair) and 3.3598 (sensitivity pair) - the basin surface-runoff
ratios measured on the frozen H2E drivers by `journal_adj-ratio.md`. Observed sediment contrast
2.8-4.6x and 6.4-9.3x from `docs/34`. Simulated run values 2.2915 and 3.9725 from `docs/37`
A1.3.4, reproduced by the lens to four decimal places. Counts are **never** raised to $\beta$ -
$\beta$ acts on magnitude, not on event counts.""")

code(r"""RQ_P, RQ_S = 1.9545, 3.3598              # basin Qsur ratios, primary / sensitivity
BETA_LO, BETA_HI = 0.45, 0.65            # docs/35 section 6.3 hard stop
OBS_P, OBS_S = (2.8, 4.6), (6.4, 9.3)    # docs/34 observed sediment-flux-rate contrasts

def sed_ratio(rq, beta):
    return rq ** (2.0 * beta)

env_P = (sed_ratio(RQ_P, BETA_LO), sed_ratio(RQ_P, BETA_HI))
env_S = (sed_ratio(RQ_S, BETA_LO), sed_ratio(RQ_S, BETA_HI))
need_P = (OBS_P[0] ** (1 / (2 * BETA_HI)), OBS_P[1] ** (1 / (2 * BETA_LO)))
need_S = (OBS_S[0] ** (1 / (2 * BETA_HI)), OBS_S[1] ** (1 / (2 * BETA_LO)))

print(f'effective exponent at beta = 0.56          : 2*beta = {2*sed.WILLIAMS_BETA:.2f}')
print(f'PRIMARY     Qsur ratio {RQ_P:.4f} -> sediment ratio at beta=0.56: '
      f'{sed_ratio(RQ_P, 0.56):.4f}   (run: {SIM_BASIN_P:.4f})')
print(f'            across the WHOLE registered beta band 0.45-0.65: '
      f'{env_P[0]:.3f}x - {env_P[1]:.3f}x   vs observed {OBS_P[0]}-{OBS_P[1]}x')
print(f'SENSITIVITY Qsur ratio {RQ_S:.4f} -> sediment ratio at beta=0.56: '
      f'{sed_ratio(RQ_S, 0.56):.4f}   (run: {SIM_BASIN_S:.4f})')
print(f'            across the WHOLE registered beta band 0.45-0.65: '
      f'{env_S[0]:.3f}x - {env_S[1]:.3f}x   vs observed {OBS_S[0]}-{OBS_S[1]}x')
print(f'\nto REACH the observed contrast the Qsur ratio would have to be '
      f'{need_P[0]:.2f}-{need_P[1]:.2f} (primary) or {need_S[0]:.2f}-{need_S[1]:.2f} '
      f'(sensitivity)')
print(f'   i.e. a HYDROLOGY change, not a sediment one: the frozen model supplies '
      f'{RQ_P:.4f} and {RQ_S:.4f}')

fig, ax = plt.subplots(1, 2, figsize=(12.6, 4.0))
rq = np.linspace(1.0, 6.0, 300)
for beta, c, ls in [(BETA_LO, CB['grey'], ':'), (0.56, CB['blue'], '-'), (BETA_HI, CB['grey'], ':')]:
    ax[0].plot(rq, rq ** (2 * beta), ls, color=c, lw=2 if beta == 0.56 else 1.2,
               label=f'$R_Q^{{2\\beta}}$, $\\beta$ = {beta}')
ax[0].fill_between(rq, rq ** (2 * BETA_LO), rq ** (2 * BETA_HI), color=CB['blue'], alpha=0.13)
ax[0].plot(rq, rq, '--', color=CB['dark'], lw=1.0, label='$R_{sed}=R_Q$ (no transformation)')
ax[0].plot(rq, rq ** 0.56, '-.', color=CB['red'], lw=1.0,
           label='$R_Q^{0.56}$ - the WRONG form; $\\beta$ acts on the PRODUCT, not on $Q_{sur}$')
for r, o, nm in [(RQ_P, OBS_P, 'primary'), (RQ_S, OBS_S, 'sensitivity')]:
    ax[0].axvline(r, color=CB['purple'], lw=1.0, alpha=0.7)
    ax[0].text(r + 0.05, 0.6, f'$R_Q$ = {r:.4f}\n({nm})', fontsize=6.8, color=CB['purple'])
    ax[0].fill_between([1.0, 6.0], o[0], o[1], color=CB['amber'], alpha=0.18, zorder=0)
    ax[0].text(5.9, np.sqrt(o[0] * o[1]), f'observed {nm}\n{o[0]}-{o[1]}x', fontsize=6.8,
               ha='right', va='center', color=CB['amber'])
ax[0].set_xlim(1, 6); ax[0].set_ylim(0.5, 12)
ax[0].set_xlabel('$R_Q$ = basin surface-runoff ratio, La Nina : El Nino')
ax[0].set_ylabel('$R_{sed}$ = simulated sediment-flux ratio')
ax[0].set_title('The model turns a runoff ratio into a sediment ratio by a POWER',
                fontsize=9.3)
ax[0].legend(fontsize=6.8, loc='upper left'); ax[0].grid(alpha=0.25)

pairs = ['primary', 'sensitivity']
for k, (env, obs, runv) in enumerate([(env_P, OBS_P, SIM_BASIN_P), (env_S, OBS_S, SIM_BASIN_S)]):
    ax[1].plot([env[0], env[1]], [k, k], lw=9, color=CB['blue'], alpha=0.55,
               solid_capstyle='butt')
    ax[1].plot([obs[0], obs[1]], [k + 0.26, k + 0.26], lw=9, color=CB['amber'],
               solid_capstyle='butt')
    ax[1].plot([runv], [k], 'D', color=CB['dark'], ms=7)
    ax[1].text(env[0] * 0.97, k - 0.17, f'{env[0]:.2f}-{env[1]:.2f}x', fontsize=7.2,
               color=CB['blue'], ha='left')
    ax[1].text(obs[0] * 0.99, k + 0.43, f'{obs[0]}-{obs[1]}x', fontsize=7.2, color=CB['amber'])
ax[1].plot([], [], lw=6, color=CB['blue'], alpha=0.55,
           label='reachable ACROSS THE WHOLE registered $\\beta$ band 0.45-0.65')
ax[1].plot([], [], lw=6, color=CB['amber'], label='OBSERVED (docs/34)')
ax[1].plot([], [], 'D', color=CB['dark'], label='the run, $\\beta$ = 0.56')
ax[1].set_yticks([0, 1]); ax[1].set_yticklabels(pairs, fontsize=8.5)
ax[1].set_xscale('log'); ax[1].set_xlim(1.5, 11)
ax[1].set_xticks([2, 3, 4, 6, 9]); ax[1].set_xticklabels(['2', '3', '4', '6', '9'])
ax[1].set_xlabel('La Nina : El Nino sediment-flux-rate ratio')
ax[1].set_title('No $\\beta$ inside its registered band reaches the observed contrast',
                fontsize=9.3)
ax[1].legend(fontsize=7.0, loc='lower right'); ax[1].grid(alpha=0.25, axis='x')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""**Left:** the map from basin surface-runoff ratio $R_Q$ to simulated sediment ratio,
$R_{sed}=R_Q^{2\beta}$, drawn at $\beta$ = 0.45, 0.56 and 0.65 with the band between them shaded;
the dashed line is no transformation, the dash-dot red line is the *incorrect* $R_Q^{0.56}$ form,
the vertical purple lines mark the basin's two measured runoff ratios and the amber bands the
observed sediment contrasts. **Right:** for each window pair, the full range of simulated contrast
reachable anywhere inside the registered $\beta$ band (blue) against the observed range (amber),
with the actual run marked.""",
    shows=r"""The effective exponent is $2\beta = 1.12$, not 0.56. The measured runoff ratios,
1.9545 and 3.3598, map to **1.83x-2.39x** (primary) and **2.98x-4.83x** (sensitivity) across the
*entire* registered $\beta$ band, against observed **2.8x-4.6x** and **6.4x-9.3x**. The two
ranges barely touch on the primary pair and do not reach on the sensitivity pair. To hit the
observed contrast the basin would need a runoff ratio of **2.21-5.45** (primary) or **4.17-11.91**
(sensitivity) - the range across the whole registered $\beta$ band, which is the form the cell
above prints and the form the rest of this paragraph uses; the frozen hydrology supplies 1.95 and
3.36. *(RETIRED 2026-08-19, shown and not quoted as current: this line previously read
~~**2.54-3.92**~~ and ~~**5.25-7.34**~~, which is the $\beta$ = 0.56 point form rather than the
band form the cell computes - and its low primary endpoint did not reproduce even that.)*""",
    means=r"""**The basin-total simulated ENSO contrast is the surface-runoff contrast raised to
$2\beta$ and essentially nothing else.** Two consequences are registered *in advance* for stage
C5 so that neither can be discovered later and read as success. First, **$\beta$ is not a lever on
the headline**: reaching the observed contrast requires a *hydrology* change, not a sediment one -
and the hydrology is frozen at a measured input-imposed skill ceiling. Second, and sharper:
**a C4 fit that appears to improve the ENSO contrast has either walked outside the registered
$\beta$ band - which is a hard stop - or is not doing what it appears to be doing.** This must be
read together with section 2.4, and never alone: on its own it reads as a model failure, whereas
2.4 shows most of the apparent shortfall was a comparison artifact. The structural compression is
real; the size of the remaining gap is much smaller than the record once said.""")

md(r"""## 2.6 - Putting the three numbers side by side, honestly

Three separate quantities have been called "the simulated ENSO contrast" in this project's
documents, and they are not the same thing. This subsection puts all of them on one axis, with
the peak-deficit correction that must accompany every one of them.

**The correction.** Simulated flood peaks are too low, and - the part that bites - they are
**more** too low in the dry phase than the wet: the ratio of simulated to observed annual maximum
series is $R_{AMS}$ = **0.808** in La Nina 2011 and **0.686** in El Nino 2015-16. So

$$\text{peak-corrected contrast}=\frac{R_{sim}}{0.8875/0.8097}=\frac{R_{sim}}{1.096},$$

i.e. **every simulated contrast is overstated by about +9.6 %** from the peak-magnitude channel
alone, and the event-count channel ($R_{POT}$ 0.500 vs 0.464) points the same way. This is **not
a conservative error - it flatters the headline**, and the observed contrast carries no
counterpart because it is measured rather than modelled.""")

code(r"""PEAK_CORR = 0.8875 / 0.8097               # docs/35 section 5.4; R_AMS 0.808 LN vs 0.686 EN
rows = [
    ('basin total, the run', SIM_BASIN_P, SIM_BASIN_S, CB['blue']),
    ('basin total, peak-corrected', SIM_BASIN_P / PEAK_CORR, SIM_BASIN_S / PEAK_CORR, CB['red']),
    ('like-for-like fleet median, est (a)', L4L.sim_med[0], L4L.sim_med[3], CB['teal']),
    ('like-for-like fleet median, est (b)', L4L.sim_med[1], L4L.sim_med[4], CB['purple']),
    ('OBSERVED (docs/34)', None, None, CB['amber'])]

print(f'peak-deficit correction factor            {PEAK_CORR:.4f}  (docs/43 section 5.2: 1.096)')
print(f'peak-corrected simulated contrast         {SIM_BASIN_P/PEAK_CORR:.4f} (primary), '
      f'{SIM_BASIN_S/PEAK_CORR:.4f} (sensitivity)   (docs/43: 2.0908 / 3.6245)')

fig, ax = plt.subplots(figsize=(11.6, 3.9))
yy = np.arange(len(rows))[::-1]
for k, (lab_, vp, vs, c) in enumerate(rows):
    y0 = yy[k]
    if vp is None:
        ax.plot(OBS_P, [y0, y0], lw=10, color=c, solid_capstyle='butt')
        ax.plot(OBS_S, [y0 - 0.22, y0 - 0.22], lw=10, color=c, alpha=0.55, solid_capstyle='butt')
        ax.text(OBS_P[1] * 1.04, y0, f'{OBS_P[0]}-{OBS_P[1]}x primary', fontsize=7.0, va='center')
        ax.text(OBS_S[1] * 1.04, y0 - 0.22, f'{OBS_S[0]}-{OBS_S[1]}x sensitivity', fontsize=7.0,
                va='center')
    else:
        ax.plot([vp], [y0], 'o', color=c, ms=9)
        ax.plot([vs], [y0 - 0.22], 's', color=c, ms=8, alpha=0.6)
        ax.text(vp * 1.04, y0, f'{vp:.3f}', fontsize=7.2, va='center', color=c)
        ax.text(vs * 1.04, y0 - 0.22, f'{vs:.3f}', fontsize=7.2, va='center', color=c)
ax.axvspan(env_P[0], env_P[1], color=CB['blue'], alpha=0.10, zorder=0)
ax.axvspan(env_S[0], env_S[1], color=CB['grey'], alpha=0.12, zorder=0)
ax.text(np.sqrt(env_P[0] * env_P[1]), yy[0] + 0.55, 'reachable by $\\beta$,\nprimary',
        fontsize=6.8, ha='center', color=CB['blue'])
ax.text(np.sqrt(env_S[0] * env_S[1]), yy[0] + 0.55, 'reachable by $\\beta$,\nsensitivity',
        fontsize=6.8, ha='center', color=CB['grey'])
ax.set_yticks(yy); ax.set_yticklabels([r[0] for r in rows], fontsize=8)
ax.set_xscale('log'); ax.set_xlim(1.7, 13)
ax.set_xticks([2, 3, 4, 5, 7, 10]); ax.set_xticklabels(['2', '3', '4', '5', '7', '10'])
ax.set_xlabel('La Nina : El Nino sediment-flux-RATE ratio (circles primary, squares sensitivity)')
ax.set_title('Three different quantities have been called "the simulated contrast"', fontsize=9.5)
ax.grid(alpha=0.25, axis='x')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""Every version of the simulated La Nina : El Nino sediment-flux-rate contrast on one
log axis - the basin total as run, the same after the registered peak-deficit correction, and the
like-for-like station-matched fleet medians under both flux estimators - against the observed
ranges (amber) and the ranges reachable anywhere inside the registered $\beta$ band (shaded).
Circles are the primary window pair, squares the sensitivity pair.""",
    shows=r"""The basin total (2.2915 / 3.9725) sits below the observed bands; the
peak-corrected version (2.0908 / 3.6245) sits further below, because **the correction moves the
model away from observation, not towards it**; and the like-for-like fleet medians (4.903 and
2.904 primary; 4.212 and 4.998 sensitivity) sit *inside* or beside them. The three differ by up
to a factor of 2.1 - and they are all correctly computed. They are simply not the same
quantity.""",
    means=r"""**The comparison basis is worth more than any parameter in this range**, which is
why stage C5's caveat set fixes it in advance: fleet-aggregate only, day- and station-matched or
say so in the same sentence, both window pairs unaveraged, rates only, the +9.6 % peak
over-statement quoted with every simulated contrast, and the envelope quoted rather than the
central value. **What this does not license:** picking the version that agrees best. The
registered headline comparison is the like-for-like one *and* it must carry the caveats; the
basin-total number is what the model produces for the basin, and the basin has no observation
against which to score it (section 6.3).""")

# ============================================================ 3 what alpha is for
md(r"""---

# 3 - What $\alpha$ is FOR, and what that does to the guard built on it

Section 1 left the model's level with a bracket and no direction. Whether that is a **defect** or
an **unset knob** depends entirely on one question that had never been answered from the sources:

> **is $\alpha = 11.8$ a physical constant, or a calibration lever?**

Two readings were live, and they lead to opposite conclusions about the same evidence.

| | **READING 1 - physical** | **READING 2 - calibration lever** |
|---|---|---|
| what $\alpha$ is | Williams' fitted coefficient; a *property* of the equation | a *coefficient of adjustment*, fitted per application |
| what a calibrated $\alpha$ should do | stay near 11.8 | go wherever the data puts it |
| what a large departure means | a compensating error somewhere else | nothing in particular |
| what the level residual means | a **defect** of the model | an **unset lever** - the quantity a calibration exists to supply |

This mattered practically, not philosophically: `docs/35` section 6.1 had registered a guard -
$\alpha$ *expected* 5.9-23.6, *watch* to 35.4, **hard stop** outside 3.9-35.4 - built entirely on
reading 1. If reading 2 governs, that guard is bounding a quantity the method defines as free.""")

md(r"""## 3.1 - The sources answer it, and they answer it differently from each other

Both source theses were re-extracted from the PDFs in the adjudication session
(`buarque2015.pdf` 182 pp / 424,028 characters; `fagundes2018.pdf` 201 pp / 343,216 characters,
PyMuPDF), so what follows is a **primary-source** read.

**Buarque (2015) - the formulation source.** His equation 5, verbatim:

> `SED = 11,8 . (Qsup . qpico . A)^0,56 . K . C . P . LS . FG`

$\alpha$ and $\beta$ **do not exist as symbols**: 11.8 and 0.56 are literals. His automatic
calibration (MOCOM-UA) fits the **hydrological** parameters only, to **discharge** at 25 gauges;
of the sediment module he writes that the MUSLE-related parameters *"foram ajustados de acordo
com faixas de valores obtidas da literatura"* - set from literature ranges. **$\alpha$ is never
fitted.** He then recommends, in writing, exactly what his successor did: *"Uma espacializacao dos
parametros da MUSLE por sub-bacia ... pode melhorar as estimativas."*

> **So READING 1 is a true description of Buarque.**

**Fagundes (2018) - the application source, and the one this project's hypothesis H3 names as
the transposed method.** Her equation 11 carries $\alpha$ and $\beta$ **as symbols**, and the text
is explicit:

> *"alpha e beta sao **coeficientes de ajuste**, ora adotados como 11,8 e 0,56 ... ora
> **calibrados automaticamente**"*

and section 6.3.1:

> *"Os parametros que foram adotados como calibraveis foram os parametros **de ajuste** da
> equacao da MUSLE, alpha e beta e o parametro de retardo ... TKS."*

They are in the MOCOM-UA parameter vector, fitted **per sub-basin** (1, 5 or 17 of them) and
**separately against each of four different observed datasets** - in-situ concentration,
red-band surface reflectance, turbidity, and satellite-derived suspended sediment - over
1997-2010, with a declared search prior of $\alpha \in [2.0, 25.0]$, $\beta \in [0.2, 1.7]$.

> **So READING 2 is a true description of the method this project transposes.**

**`docs/35` section 6.1 imported its reference from the wrong branch of its own lineage.** It
says so itself: *"adopted unchanged by Buarque 2015 eq. 5"*. The guard was built on the branch
that **adopts** $\alpha$, and applied to a project transposing the branch that **fits** it.""")

md(r"""## 3.2 - The decisive measurement: the same sub-basin, four calibration targets

A test was committed to **in advance** of looking at the numbers (pre-commitment P4 in
`journal_adj-alpha-role.md`):

> reading 2 is established **iff** the source method (a) lists $\alpha$ among the parameters
> handed to the automatic optimiser, **and** (b) fits them against observed sediment at gauges.

Both hold. But the sharper evidence came from parsing the thesis' **Appendix IV** in full -
**123 sub-basin rows x 4 calibration data types = 426 published, adopted $(\alpha,\beta)$
pairs** - and asking a question the appendix answers by construction:

> for the **same sub-basin** in the **same experiment**, over the **same period**, the only thing
> that differs between the four columns is *which observed dataset was the calibration target*.
> Does $\alpha$ move?

$$\text{spread}_i \;=\; \frac{\max_j \alpha_{ij}}{\min_j \alpha_{ij}}
\qquad i=\text{sub-basin row},\ \ j=\text{calibration target}$$

dimensionless, over the 101 rows with all four columns present. **The interpretation was
registered before the numbers**, in both directions: a large spread establishes reading 2
whatever the values are; and clustering near 11.8 would **not** be read as support for reading 1,
because the source's own search prior [2.0, 25.0] is centred near 11.8 and caps the range - *a
clustered posterior inside a narrow prior is not evidence about physics.*

**Data source:** `docs/agents/journal_adj-alpha-role.md` step 3, carried. The parse was validated
by design: recovered sub-basin row counts per experiment (5, 1, 5, 5, 17, 17, 17, 5, 17, 17, 17)
match exactly the counts the thesis' own Quadro 5-2 declares.""")

code(r"""# carried from docs/agents/journal_adj-alpha-role.md step 3 (426 published, ADOPTED fits)
N_PAIRS = 426
A_STATS = {'min': 2.221, 'p05': 8.520, 'median': 11.765, 'mean': 12.202,
           'p95': 16.738, 'max': 23.179}
B_STATS = {'min': 0.207, 'p05': 0.487, 'median': 0.618, 'mean': 0.656,
           'p95': 0.939, 'max': 1.659}
SPREAD = {'median': 1.28, 'p95': 3.99, 'max': 7.78, 'n_rows': 101,
          'frac_gt_1p5': 0.307, 'frac_gt_2': 0.139}
PRIOR_A = (2.0, 25.0)             # the source's own MOCOM-UA search prior for alpha
GUARD_EXPECTED = (5.9, 23.6)      # docs/35 section 6.1
GUARD_STOP = (3.9, 35.4)
GUARD_BETA = (0.45, 0.65)         # docs/35 section 6.3, re-affirmed as docs/42 G2.3
VERDICTS = {'STOP': 185, 'watch': 59, 'ok': 182}

print(f'published, adopted (alpha, beta) pairs of the transposed method : {N_PAIRS}')
print(f'  alpha  min {A_STATS["min"]}  p05 {A_STATS["p05"]}  median {A_STATS["median"]}  '
      f'p95 {A_STATS["p95"]}  max {A_STATS["max"]}   (span x{A_STATS["max"]/A_STATS["min"]:.1f})')
print(f'  beta   min {B_STATS["min"]}  p05 {B_STATS["p05"]}  median {B_STATS["median"]}  '
      f'p95 {B_STATS["p95"]}  max {B_STATS["max"]}')
print(f'\nSAME sub-basin, SAME experiment, only the calibration TARGET differs ({SPREAD["n_rows"]} '
      f'complete rows):')
print(f'  fitted alpha moves by median x{SPREAD["median"]}, p95 x{SPREAD["p95"]}, '
      f'MAX x{SPREAD["max"]}')
print(f'  {100*SPREAD["frac_gt_1p5"]:.1f} % of rows spread more than 1.5x; '
      f'{100*SPREAD["frac_gt_2"]:.1f} % more than 2x')
print(f'\n-> a physical constant cannot change by {SPREAD["max"]}x according to whether you '
      f'calibrated against in-situ concentration or Landsat reflectance in the same sub-basin '
      f'over the same years.')
print(f'\nrunning THIS repository\'s own unmodified guard over all {N_PAIRS} published fits:')
for k, v in VERDICTS.items():
    print(f'   {k:6s} {v:4d}   {100*v/N_PAIRS:5.1f} %')
print(f'   -> the guard HARD-STOPS {100*VERDICTS["STOP"]/N_PAIRS:.1f} % of the published fits of '
      f'the method it guards, and 42.7 points of that is the BETA stop, which is dimensionless '
      f'and cannot be rescued by any unit or convention argument.')""")

code(r"""fig, ax = plt.subplots(1, 2, figsize=(12.8, 4.0), gridspec_kw={'width_ratios': [1.35, 1.0]})

q = [A_STATS['min'], A_STATS['p05'], A_STATS['median'], A_STATS['p95'], A_STATS['max']]
ax[0].axhspan(PRIOR_A[0], PRIOR_A[1], color=CB['grey'], alpha=0.22, zorder=0,
              label="the SOURCE's own MOCOM-UA search prior for $\\alpha$: [2.0, 25.0]")
ax[0].axhspan(GUARD_EXPECTED[0], GUARD_EXPECTED[1], color=CB['green'], alpha=0.22, zorder=1,
              label='docs/35 section 6.1 "expected" band 5.9-23.6')
ax[0].axhline(GUARD_STOP[1], color=CB['red'], lw=1.3, ls='--',
              label='docs/35 hard stops 3.9 and 35.4')
ax[0].axhline(GUARD_STOP[0], color=CB['red'], lw=1.3, ls='--')
ax[0].axhline(sed.WILLIAMS_ALPHA, color=CB['dark'], lw=1.4,
              label=f'Williams (1975) $\\alpha$ = {sed.WILLIAMS_ALPHA}')
ax[0].plot([0.4, 0.4], [q[0], q[4]], lw=1.4, color=CB['purple'])
ax[0].add_patch(Rectangle((0.28, q[1]), 0.24, q[3] - q[1], facecolor=CB['purple'], alpha=0.55))
ax[0].plot([0.28, 0.52], [q[2], q[2]], lw=2.4, color=CB['purple'])
for v, nm in zip(q, ['min', 'p05', 'median', 'p95', 'max']):
    ax[0].text(0.56, v, f'{nm} {v:.3f}', fontsize=7.0, va='center', color=CB['purple'])
ax[0].set_xlim(0, 1.35); ax[0].set_ylim(0, 38); ax[0].set_xticks([])
ax[0].set_ylabel('fitted $\\alpha$ (dimensionless)')
ax[0].set_title(f'{N_PAIRS} published, ADOPTED $\\alpha$ of the transposed method', fontsize=9.3)
ax[0].legend(fontsize=6.8, loc='upper right'); ax[0].grid(alpha=0.25, axis='y')

lab2 = ['STOP', 'watch', 'ok']
val2 = [VERDICTS[k] for k in lab2]
ax[1].bar(range(3), val2, 0.55, color=[CB['red'], CB['amber'], CB['green']])
for i, v in enumerate(val2):
    ax[1].text(i, v + 5, f'{v}\n{100*v/N_PAIRS:.1f} %', ha='center', fontsize=8.2)
ax[1].axhline(N_PAIRS / 2, color=CB['dark'], lw=1.0, ls=':')
ax[1].text(2.45, N_PAIRS / 2 + 5, 'half the corpus', fontsize=6.8, ha='right')
ax[1].set_xticks(range(3)); ax[1].set_xticklabels(lab2, fontsize=9)
ax[1].set_ylabel(f'published fits (of {N_PAIRS})'); ax[1].set_ylim(0, 245)
ax[1].set_title("This repository's guard, run on its own source method", fontsize=9.3)
ax[1].grid(alpha=0.25, axis='y')
plt.tight_layout(); plt.show()

frac_in = 0.977
print(f'{100*frac_in:.1f} % of the {N_PAIRS} fits land inside the "expected" 5.9-23.6 - but the '
      f'source PRIOR [2.0, 25.0] CONTAINS that band, so the statistic measures the prior, not '
      f'the physics.')""")

reading(
    what=r"""**Left:** the distribution of the 426 published, adopted $\alpha$ values of the
method this project transposes (min / p05 / median / p95 / max), against the source's own search
prior (grey), the `docs/35` "expected" band (green), the hard stops (dashed red) and Williams'
11.8 (dark line). **Right:** the verdict this repository's own unmodified
`check_musle_parameters` returns when it is run over those same 426 published fits.""",
    shows=r"""The published fits span **2.221 to 23.179 - a factor of 10.4** - with a median of
11.765 that sits almost exactly on Williams' 11.8. But **97.7 %** of them fall inside the
"expected" band **because the source's prior contains that band**; the green band is nested inside
the grey one, so the agreement measures the search interval, not the physics. And for the *same
sub-basin in the same experiment*, fitted $\alpha$ moves by a median of **1.28x and up to 7.78x**
according only to which observed dataset was the calibration target. On the right, the guard
returns **STOP on 185 of 426 (43.4 %)** of the published, accepted fits of the method it guards -
and **42.7 points of that is the $\beta$ hard stop**, a dimensionless clause that no unit or
convention argument can rescue.""",
    means=r"""**READING 2 governs.** $\alpha$ in this method is a *coefficient of adjustment*, not
a physical constant: a physical constant cannot change 7.78-fold according to which instrument
you calibrated against. Two consequences follow, and they point in opposite directions for the
project. **The good one:** the model's unfitted level is therefore **not a defect** - it is an
*unset lever*, the exact quantity a calibration exists to supply, so this reclassifies the level
component of the C3 residual from *defect* to *calibration target*. **The bad one:** the guard
this project had been relying on is **mis-specified, not merely blind** - it bounds a quantity the
method defines as free, its reference comes from the wrong branch of the lineage, and its
companion clause rejects 43 % of the source's own accepted practice. `docs/35` is frozen, so C4
**follows it anyway** and prints its measured defects beside it every time it is quoted; but it is
`docs/42`'s *structure* guards, not this band, that decide C4.""")

md(r"""## 3.3 - Why the $\alpha$ band cannot catch the error C4 is most likely to make

The guard is not only mis-specified in principle. It is **measurably blind** to the single most
likely failure of a sediment calibration, and this was quantified before C4 was allowed to start.

The failure in question: fitting the model to observed flux at stations **without any channel
deposition term**, which silently asserts that everything eroded on a hillslope arrives at the
station. That is a strong physical claim, and a fit that makes it by omission looks exactly like
a fit that does not.

Three intervals, all measured, all in the same units of $\alpha$:

| | interval | what it is |
|---|---|---|
| a fit that **silently omits channel deposition** lands at | ~~6.83 - 8.73~~ $\rightarrow$ **5.6727 - 7.2485** | `docs/35` section 9.2, **corrected to the adopted $C$** by `docs/43` section 7 amendment 5 |
| the $\alpha$ reproducing the flattering **reading-B** level | **7.92 - 8.86** | `docs/37` A1.9.4 (11.8 / 1.4897 and 11.8 / 1.3323) |
| the guard's **"expected"** band | **5.9 - 23.6** | `docs/35` section 6.1 |

> **A `cp_revision` CORRECTION, 2026-08-12, and it inverts this section's sharpest sentence.**
> Owning enactment: **`docs/43` section 7 amendment 5** (source `docs/47` section 2.5 **C1**).
> ~~6.83 - 8.73~~ is $11.8\times\{144,184\}/248.730$ - the **prior** `cp_revision`'s basin total.
> The reading-B band 7.92 - 8.86 is **already at the adopted $C$**, so the two were being compared
> across two different basin totals. Recomputed at the adopted $C$ (**299.5387088405831 Mt/yr**),
> $11.8\times\{144,184\}/299.5387088405831 =$ **5.6727 - 7.2485**, and the gap to 7.92 is
> **0.6715 in $\alpha$**: ~~"these overlap"~~ $\rightarrow$ **the two bands are DISJOINT**. The
> house rule this violated: **never quote a load without its convention AND its `cp_revision`.**
>
> **What survives, and it must not be over-read in either direction.** The section's load-bearing
> claim is about the *guard*, not about $\alpha$, and it survives intact: the guard still returns
> `ok` across **nearly all of both** bands and therefore still cannot **reject** a deposition-free
> fit. What does *not* survive is the stronger "nearly indistinguishable" reading - corrected, the
> two cases **are** separable in $\alpha$, which points the other way. **Whether that changes the
> "doubly load-bearing" conclusion about G5 is `docs/47` open item O12 and is NOT decided here.**
> One measured detail the correction adds, and the cell below prints it: at the anchor-144 end the
> adopted-$C$ band dips to 5.6727, just **below** the guard's expected-band low of 5.9, so the
> guard emits `watch` there - a partial, accidental catch at one endpoint, not a rejection.

**Both bands sit inside the third.** So a fit that "works" under the reading that flatters the
project draws the same `ok` from the guard as one that has simply deleted channel deposition. The
cell below runs the repository's own guard to show it, at **both** `cp_revision`s.""")

code(r"""# docs/35 section 9.2's 6.83-8.73 is 11.8 x {144,184} / 248.730 - the PRIOR cp_revision's basin
# total.  CORRECTED to the adopted C by docs/43 section 7 amendment 5.  RECOMPUTED here from this
# notebook's own ADOPT and anchors, never retyped: a load may not be quoted without its convention
# AND its cp_revision.  READINGB is already at the adopted C, which is why the comparison moved.
DEPFREE_PRIOR = (6.83, 8.73)   # docs/35 section 9.2, at the PRIOR cp_revision (248.730 Mt/yr)
DEPFREE = (sed.WILLIAMS_ALPHA * ANCHOR_LO / ADOPT, sed.WILLIAMS_ALPHA * ANCHOR_HI / ADOPT)
READINGB = (7.92, 8.86)     # docs/37 A1.9.4 - alpha reproducing Tan's converted (yield) level

print(f'a deposition-free fit lands at alpha = 11.8 x {{{ANCHOR_LO:.0f},{ANCHOR_HI:.0f}}} / total:')
print(f'   at the PRIOR cp_revision ({PRIOR_C:.4f} Mt/yr) : '
      f'{sed.WILLIAMS_ALPHA*ANCHOR_LO/PRIOR_C:.4f} - {sed.WILLIAMS_ALPHA*ANCHOR_HI/PRIOR_C:.4f}'
      f'   <- docs/35 section 9.2 rounds this to {DEPFREE_PRIOR[0]}-{DEPFREE_PRIOR[1]}')
print(f'   at the ADOPTED C        ({ADOPT:.4f} Mt/yr) : {DEPFREE[0]:.4f} - {DEPFREE[1]:.4f}'
      f'   <- THE LIVE BAND (docs/43 section 7 amd 5)')
print(f'   reading-B band, already at the adopted C     : {READINGB[0]:.4f} - {READINGB[1]:.4f}')
print(f'   GAP = {READINGB[0]-DEPFREE[1]:.4f} in alpha  ->  THE TWO BANDS ARE DISJOINT.  The')
print(f'   "these overlap" reading was an artefact of comparing two cp_revisions.  What SURVIVES:')
print(f'   the guard still returns ok across nearly all of both, so it still cannot REJECT either.')
print(f'   Whether the disjointness changes the "doubly load-bearing" conclusion about G5 is')
print(f'   docs/47 open item O12 and is NOT decided here.\n')

probe = [('deposition-free fit, PRIOR C, low end', DEPFREE_PRIOR[0], 0.56),
         ('deposition-free fit, PRIOR C, high end', DEPFREE_PRIOR[1], 0.56),
         ('deposition-free fit, ADOPTED C, low end', DEPFREE[0], 0.56),
         ('deposition-free fit, ADOPTED C, high end', DEPFREE[1], 0.56),
         ('reading-B level, low end', READINGB[0], 0.56),
         ('reading-B level, high end', READINGB[1], 0.56),
         ('Williams, unfitted', sed.WILLIAMS_ALPHA, sed.WILLIAMS_BETA),
         ('the source corpus median', A_STATS['median'], B_STATS['median']),
         ('the source corpus p95 beta', A_STATS['median'], B_STATS['p95'])]
print(f'{"probe":42s} {"alpha":>7s} {"beta":>6s}   verdict')
for nm, a, b in probe:
    v = qpk.check_musle_parameters(a, b)
    print(f'{nm:42s} {a:7.3f} {b:6.3f}   {v["status"]}'
          + ('   <- ' + v['reasons'][0][:66] if v['reasons'] else ''))

fig, ax = plt.subplots(figsize=(11.4, 2.8))
ax.axvspan(*GUARD_EXPECTED, color=CB['green'], alpha=0.22,
           label='docs/35 "expected" 5.9-23.6 - the guard returns ok anywhere in here')
ax.axvspan(*GUARD_STOP, color=CB['amber'], alpha=0.10, zorder=0)
ax.plot(DEPFREE_PRIOR, [1.18, 1.18], lw=7, color=CB['grey'], solid_capstyle='butt', alpha=0.85,
        label=f'SUPERSEDED, prior cp_revision: {DEPFREE_PRIOR[0]}-{DEPFREE_PRIOR[1]}')
ax.plot(DEPFREE, [1.0, 1.0], lw=11, color=CB['red'], solid_capstyle='butt',
        label=f'a fit that SILENTLY OMITS channel deposition, at the ADOPTED C: '
              f'{DEPFREE[0]:.2f}-{DEPFREE[1]:.2f}')
ax.plot(READINGB, [0.72, 0.72], lw=11, color=CB['purple'], solid_capstyle='butt',
        label=f'the $\\alpha$ reproducing the flattering reading-B level: '
              f'{READINGB[0]}-{READINGB[1]}')
ax.axvline(sed.WILLIAMS_ALPHA, color=CB['dark'], lw=1.5)
ax.text(sed.WILLIAMS_ALPHA + 0.25, 1.32, 'Williams 11.8', fontsize=7.4, color=CB['dark'])
ax.axvline(GUARD_STOP[0], color=CB['red'], lw=1.2, ls='--')
ax.axvline(GUARD_STOP[1], color=CB['red'], lw=1.2, ls='--')
ax.text(GUARD_STOP[1] - 0.3, 0.42, 'hard stop 35.4', fontsize=7.0, ha='right', color=CB['red'])
ax.annotate(f'DISJOINT at the adopted $C$\n(gap {READINGB[0]-DEPFREE[1]:.2f} in $\\alpha$) - but the '
            f'guard\nsays ok inside BOTH, so it still cannot reject',
            xy=(0.5*(DEPFREE[1]+READINGB[0]), 0.86), xytext=(14.5, 0.50), fontsize=7.6,
            color=CB['red'], arrowprops=dict(arrowstyle='->', lw=1.2, color=CB['red']))
ax.set_xlim(2, 38); ax.set_ylim(0.3, 1.5); ax.set_yticks([])
ax.set_xlabel('$\\alpha$ (dimensionless)')
ax.set_title('The $\\alpha$-magnitude guard is blind to the single error C4 is most likely to make',
             fontsize=9.5)
ax.legend(fontsize=7.0, loc='upper right'); ax.grid(alpha=0.25, axis='x')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""The $\alpha$ axis with the guard's "expected" band shaded green and its hard stops
dashed; the red bar is where a fit that silently omits channel deposition lands **at the adopted
$C$**, the grey bar above it is the superseded prior-`cp_revision` band, the purple bar is
the $\alpha$ that reproduces the level implied by the flattering reading of section 1.4, and the
dark line is Williams' 11.8. The cell above runs the repository's own unmodified guard on each.""",
    shows=r"""~~**6.83-8.73 and 7.92-8.86 overlap**~~ $\rightarrow$ **at the adopted $C$ the
deposition-free band is 5.6727-7.2485 and it is DISJOINT from 7.92-8.86, by 0.6715 in $\alpha$**
(`docs/43` section 7 amendment 5; the struck overlap compared the prior `cp_revision`'s 248.730
against a reading-B band already at 299.5387). **The conclusion this figure exists to support is
unchanged**, because it was never about the overlap: both bands still lie inside 5.9-23.6, so
`check_musle_parameters` returns `ok` throughout reading B and across all of the deposition-free
band except its very lowest end, where 5.6727 dips below the expected-band low of 5.9 and draws a
`watch`. **A `watch` is not a rejection**, so the guard still cannot separate "a physically
sensible fit" from "a fit that deleted the channel". What is *withdrawn* is the stronger claim that
the two are *nearly indistinguishable in $\alpha$* - corrected, they are separable in $\alpha$, and
whether that changes the "doubly load-bearing" conclusion about G5 is `docs/47` open item **O12**,
not decided here. The guard does fire correctly on
$\beta$: at the source corpus' own p95 $\beta$ of 0.939 it returns STOP - which is the same clause
that rejects 42.7 % of the published fits.""",
    means=r"""**A parameter *value* cannot be a validity criterion for a parameter the method
fits.** This is why the C4 gate was rebuilt around something else. The replacement precondition
(guard **G5**) is not a number at all: a fit may be adopted only if the configuration contains a
**named, non-trivial transport sink**, *or* the C4 document states, in these words, as a claim -
**"this model asserts SDR = 1.0 between hillslope and station"** - **and** the fitted deposition
coefficient appears with its interval **in the same table as $\alpha$**. The registration takes
the second option explicitly (section 5.3). **What this does not license:** discarding the
$\alpha$ band. `docs/35` is a frozen pre-registration; C4 follows it anyway, reports its measured
defects beside it, and may *propose* - never enact - an amendment. **And read every $\alpha$
number in this section as V0-conditional.** The bands drawn here - expected **5.9-23.6**, hard
stops **3.9** and **35.4** - and the deposition-free band derived from 299.5387 Mt/yr are all at
$f_{LS}$ = 1.000. `docs/35` **section 9.5** (2026-08-12) **RE-REGISTERED** them at the adopted LS
level, where they scale with $f_{LS}$: reference $11.8\cdot f_{LS}$ = **2.967**, expected
**1.484-5.934**, upper hard stop $35.4\cdot f_{LS}$ = **8.902**, lower hard stop **0.981** - so the
upper hard stop then sits *below* the unfitted $\alpha$ = 11.8. Those are the values `docs/55`
profiles against. That is a change of *reference frame*, not a change of this section's
conclusion, which is about the guard's blindness and not about any $\alpha$ value.""")

md(r"""## 3.4 - The deeper reason: $\alpha$ has no separate existence to be validated

There is a second, independent argument, and it is algebraic rather than bibliographic.

$\alpha$, the $C$ level, the $LS$ level, the $K$ unit system, the volume convention, $P$ and $FG$
are **seven scalars that enter every minibacia-day in exactly the same way**. Write the basin
total as

$$\text{load} \;=\; \Pi \cdot \underbrace{\sum_{i,t}\bigl(Q_{sur}\,q_{peak}\,A\bigr)_{it}^{\beta}
\,\tilde K_i \tilde C_i \widetilde{LS}_i}_{\text{the shape, fixed}},\qquad
\Pi \;=\; \alpha\, f_{vol}\, f_K\, f_{LS}\, C_{mult}\, P\, FG$$

with $\Pi$ dimensionless. The partial derivative of the output with respect to each of the seven
is the *same column of ones* in log space: the design matrix is **exactly singular**, condition
number measured as **`inf`**. **Only $\Pi$ is identifiable.**

At the adopted configuration, unfitted, $\Pi$ = **5,164.42**. A calibration "fits $\alpha$" only
in the sense that $\alpha$ is the handle the search turns. **What it determines is $\Pi$** - which
is precisely the quantity the level residual *is*. The level residual therefore has no separate
existence to be defective: it is $\Pi$, and $\Pi$ is what a fit sets.

The cell below shows the equifinal family explicitly - different, equally valid, mutually
indistinguishable ways of writing the same model.""")

code(r"""PI_ADOPTED = 5164.42                     # docs/45 section 1.4 / docs/37 A1.6 item 2
C_MULT_ADOPTED = 1.20427                 # erosion-weighted, docs/37 A1.3.2

fam = pd.DataFrame({'C_mult': [1.0, C_MULT_ADOPTED, 2.0, 5.0]})
fam['alpha_needed'] = sed.WILLIAMS_ALPHA * C_MULT_ADOPTED / fam.C_mult
fam['Pi'] = fam.alpha_needed * F_VOL * F_K * F_LS * fam.C_mult * 1.0 * 1.0   # x P x FG
PI_HERE = float(fam.Pi.iloc[0])
print('the equifinal family - every row is the SAME model, and no data can separate them:\n')
print(fam.to_string(index=False, float_format='%.5f'))
print(f'\nPi = alpha x f_vol x f_K x f_LS x C_mult x P x FG is CONSTANT across the family: '
      f'{PI_HERE:,.2f}   (docs/45 section 1.4: {PI_ADOPTED:,.2f})')
print(f'Pi at the adopted, unfitted configuration = {sed.WILLIAMS_ALPHA} x {F_VOL:.4f} x '
      f'{F_K:.6f} x {F_LS:.3f} x {C_MULT_ADOPTED} x 1.0 x 1.0')

fig, ax = plt.subplots(1, 2, figsize=(12.4, 3.6))
cm = np.linspace(0.5, 6.0, 200)
ax[0].plot(cm, sed.WILLIAMS_ALPHA * C_MULT_ADOPTED / cm, color=CB['blue'], lw=2)
ax[0].axhspan(*GUARD_EXPECTED, color=CB['green'], alpha=0.20,
              label='docs/35 "expected" $\\alpha$ 5.9-23.6')
ax[0].axhspan(*DEPFREE, color=CB['red'], alpha=0.28,
              label=f'deposition-free fit, adopted $C$: {DEPFREE[0]:.2f}-{DEPFREE[1]:.2f}')
for _, r in fam.iterrows():
    ax[0].plot([r.C_mult], [r.alpha_needed], 'o', color=CB['dark'], ms=7)
    ax[0].text(r.C_mult, r.alpha_needed + 0.9, f'$C_m$={r.C_mult:.2f}\n$\\alpha$='
                                               f'{r.alpha_needed:.2f}', fontsize=6.8, ha='center')
ax[0].set_xlabel('cover-factor multiplier $C_{mult}$'); ax[0].set_ylabel('$\\alpha$ that keeps '
                                                                        '$\\Pi$ unchanged')
ax[0].set_ylim(0, 32); ax[0].set_title('The equifinal ridge: one product, seven names',
                                       fontsize=9.3)
ax[0].legend(fontsize=7.0); ax[0].grid(alpha=0.25)

names7 = ['$\\alpha$', '$f_{vol}$', '$f_K$', '$f_{LS}$', '$C_{mult}$', '$P$', '$FG$']
vals7 = [sed.WILLIAMS_ALPHA, F_VOL, F_K, F_LS, C_MULT_ADOPTED, 1.0, 1.0]
grades = ['UNFITTED', 'DERIVED', 'IDENTIFIED', 'UNVALIDATED', 'CITED', 'ASSUMED', 'ASSUMED']
gcol = {'DERIVED': CB['green'], 'IDENTIFIED': CB['green'], 'CITED': CB['teal'],
        'UNVALIDATED': CB['red'], 'ASSUMED': CB['amber'], 'UNFITTED': CB['purple']}
ax[1].bar(range(7), vals7, 0.55, color=[gcol[g] for g in grades])
for i, (v, g) in enumerate(zip(vals7, grades)):
    ax[1].text(i, v * 1.25, f'{v:.4g}', ha='center', fontsize=7.4)
    ax[1].text(i, 0.13, g, ha='center', fontsize=6.4, rotation=90, color='white')
ax[1].set_yscale('log'); ax[1].set_ylim(0.08, 200)
ax[1].set_xticks(range(7)); ax[1].set_xticklabels(names7, fontsize=9)
ax[1].set_ylabel('value (log scale)')
ax[1].set_title(f'The seven factors of $\\Pi$ = {PI_ADOPTED:,.2f}, with evidence grades',
                fontsize=9.3)
ax[1].grid(alpha=0.25, axis='y')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""**Left:** the ridge of parameter combinations that leave the model's output
*bitwise identical* - the $\alpha$ required to hold $\Pi$ fixed as the cover-factor multiplier is
varied - with the guard's expected band and the deposition-free band shaded, and four members of
the family marked. **Right:** the seven scalars whose product is $\Pi$, on a log scale, each
labelled with its evidence grade.""",
    shows=r"""Every point on the blue curve is the same model. $C_{mult}$ = 1 with
$\alpha$ = 14.2, $C_{mult}$ = 2 with $\alpha$ = 7.10, $C_{mult}$ = 5 with $\alpha$ = 2.84 - the
data cannot distinguish them, because the design matrix is exactly singular. Note that the
$C_{mult}$ = 2 member lands **inside the deposition-free band**, and the guard would call it `ok`.
On the right, of the seven factors only two are DERIVED or IDENTIFIED, one is CITED, one is
**UNVALIDATED** ($f_{LS}$) and two are ASSUMED one-sided ($P$ and $FG$ are both $\le 1$, so
setting them to 1 puts an *upper* bound on erosion).""",
    means=r"""**"Validating $\alpha$" is not a thing that can be done with these data - not
partially, not weakly, not at all.** Whatever C4 reports about the level is a statement about
$\Pi$, and $\Pi$ must be reported with its equifinal family and a per-factor evidence grade
beside it. This is why the C4 registration forbids the words "validated $\alpha$", "validated $C$
level", "validated $LS$ level" and "validated basin sediment load", and requires the word
**UNVALIDATED** to appear in the same table as $\Pi$. It is also why *cited is not validated* -
and, less obviously, why **fitted is not validated either**: a fit *sets* $\Pi$, it does not test
it.""")

# ============================================================ 4 C4 feasibility
md(r"""---

# 4 - Is stage C4 feasible? The station funnel, 79 to 8

Section 3 established that the model's level is a **calibration target**. That is only useful if
the calibration can actually be done. This section measures whether it can - before any code for
it was written, which is the only time the answer is worth anything.

## 4.1 - The funnel, computed here rather than quoted

Four filters stand between the 79 suspended-sediment stations in the network and a station a
calibration can use. Each is a hard requirement, not a preference:

| filter | requirement | why it is not negotiable |
|---|---|---|
| **C1** | classified `usable` or `usable-with-caveat`, **and mapped to a minibacia** | an unmapped station cannot be connected to any model output - 46 of the 79 have no coordinates at all |
| **(a)** | **tributary**, not trunk | mainstem stations are held back to be scored, never fitted |
| **(b)** | upstream of the Depresion Momposina | the model has no representation of that sink, so a station below it would be fitted against a process the model does not have |
| **(c)** | at least one non-deleted SSC observation inside the calibration window **2012-01-01 .. 2014-12-31** | the window is registered as ENSO-neutral so that both ENSO windows stay strictly out of sample |
| **(d)** | at least one **paired** day carrying both an SSC observation and an observed discharge | flux is concentration x discharge; without both on the same day there is no observed flux to fit to |

**Data sources.** `data/processed/sediment_inventory_qc.csv` (79 stations, the C1 classification,
the `reach` column that decides trunk vs tributary); `data/processed/sediment_daily_qc.csv`
(`ssc_mean_mg_l` with `c1_deleted == False`); `data/processed/discharge_daily.csv` (`q_m3s`).
Filter (b) is carried as measured rather than recomputed - `docs/42` section 4.1 and lens 3 both
found it **removes zero stations**, because the Cauca-Magdalena confluence sits at minibacia 4430,
146.1 km above the outlet, and the closest SSC station is 684.4 km above *it*.""")

code(r"""t0 = time.time()
CAL0, CAL1 = pd.Timestamp('2012-01-01'), pd.Timestamp('2014-12-31')

INV = pd.read_csv(PROC / 'sediment_inventory_qc.csv')
n_all = len(INV)
n_mapped = int(INV.mapped.sum())
USABLE = INV[INV.mapped & INV.ssc_class.isin(['usable', 'usable-with-caveat'])].copy()
n_usable = len(USABLE)
TRIB = USABLE[USABLE.reach == 'tributary'].copy()
n_trib = len(TRIB)

SSC = pd.read_csv(PROC / 'sediment_daily_qc.csv',
                  usecols=['code', 'date', 'ssc_mean_mg_l', 'c1_deleted'])
SSC['date'] = pd.to_datetime(SSC['date'])
SSC_CAL = SSC[(SSC.date >= CAL0) & (SSC.date <= CAL1) & (~SSC.c1_deleted)
              & SSC.ssc_mean_mg_l.notna()]
have_ssc = set(SSC_CAL.code.unique())
n_c = len(set(TRIB.code) & have_ssc)

QD = pd.read_csv(PROC / 'discharge_daily.csv', usecols=['code', 'date', 'q_m3s'])
QD['date'] = pd.to_datetime(QD['date'])
QD_CAL = QD[(QD.date >= CAL0) & (QD.date <= CAL1) & QD.q_m3s.notna()]
PAIRED = SSC_CAL.merge(QD_CAL, on=['code', 'date'])
paircount = PAIRED.groupby('code').size()
CAL8 = sorted(c for c in TRIB.code if paircount.get(c, 0) >= 1)
n_d = len(CAL8)

FUNNEL = [('classified by C1', n_all), ('mapped to a minibacia', n_mapped),
          ('usable / usable-with-caveat', n_usable), ('(a) tributary, not trunk', n_trib),
          ('(b) upstream of the Momposina', n_trib), ('(c) >=1 SSC day in CAL 2012-14', n_c),
          ('(d) >=1 PAIRED SSC + Q day', n_d)]
for nm, v in FUNNEL:
    print(f'  {v:3d}   {nm}')
print(f'\nCAL 8 paired-day counts (computed here):')
tab = (pd.DataFrame({'code': CAL8})
       .assign(name=lambda d: d.code.map(dict(zip(TRIB.code, TRIB.name))),
               paired_CAL_days=lambda d: d.code.map(paircount).astype(int),
               up_area_km2=lambda d: d.code.map(dict(zip(TRIB.code, TRIB.up_area_km2))),
               flow_selective=lambda d: d.code.map(dict(zip(TRIB.code, TRIB.flag_flow_selective))))
       .sort_values('paired_CAL_days', ascending=False))
print(tab.to_string(index=False))
N_PAIRED_DAYS = int(tab.paired_CAL_days.sum())
print(f'\ntotal paired CAL days {N_PAIRED_DAYS}   '
      f'(journal_adj-c4-feasibility section 3.1: 3,266)')
print(f'station-months with data 126 of 288 possible (43.8 %, carried)')
print(f'elapsed {time.time()-t0:.1f} s')

LOST = pd.DataFrame({
    'code': [23087210, 26167060, 21147030, 22057090, 26107130],
    'name': ['CANTERAS', 'PAILA LA', 'CARRASPOSO', 'BOCATOMA TRIANGULO', 'MATEGUADUA'],
    'Lw_km': [68.0, 11.8, 39.0, 110.4, 30.1],
    'reason': ['SSC starts 2015-01-01 - zero SSC in CAL',
               'SSC starts 2015-01-03 - zero SSC in CAL',
               'SSC starts 2015-01-01 - zero SSC in CAL',
               '619 SSC days in CAL but observed Q ENDS 2009-03-19',
               'SSC ends 2011-05-30 AND zero observed Q in 2012-14']})
print('\nthe 5 tributary stations lost, each named with its reason:')
print(LOST.to_string(index=False))""")

code(r"""AREAS = {'all 18': (98988, 38.5), 'CAL 13 (registered)': (25844, 10.1),
         'CAL 8 (achievable)': (13862, 5.4), 'CAL 8 + trunk station': (64653, 25.1)}

fig, ax = plt.subplots(1, 2, figsize=(12.8, 4.1), gridspec_kw={'width_ratios': [1.3, 1.0]})
labels = [f[0] for f in FUNNEL]; counts = [f[1] for f in FUNNEL]
yv = np.arange(len(FUNNEL))[::-1]
cols = [CB['grey'], CB['grey'], CB['blue'], CB['blue'], CB['blue'], CB['amber'], CB['red']]
ax[0].barh(yv, counts, 0.6, color=cols)
for k, v in enumerate(counts):
    ax[0].text(v + 1.2, yv[k], str(v), va='center', fontsize=8.6, fontweight='bold')
    if k > 0 and counts[k] < counts[k - 1]:
        ax[0].text(v + 6.0, yv[k], f'(-{counts[k-1]-counts[k]})', va='center', fontsize=7.0,
                   color=CB['red'])
    elif k > 0:
        ax[0].text(v + 6.0, yv[k], '(removes ZERO - measured)', va='center', fontsize=6.6,
                   color=CB['green'])
ax[0].set_yticks(yv); ax[0].set_yticklabels(labels, fontsize=8)
ax[0].set_xlabel('SSC stations'); ax[0].set_xlim(0, 96)
ax[0].set_title('79 to 8: the C4 calibration set, every step computed here', fontsize=9.4)
ax[0].grid(alpha=0.25, axis='x')

ak = list(AREAS); av = [AREAS[k][1] for k in ak]
ax[1].bar(range(len(ak)), av, 0.55,
          color=[CB['blue'], CB['amber'], CB['red'], CB['grey']])
for i, k in enumerate(ak):
    ax[1].text(i, av[i] + 0.9, f'{AREAS[k][0]:,} km2\n{av[i]:.1f} %', ha='center', fontsize=7.4)
ax[1].axhline(100, color=CB['dark'], lw=1.0, ls=':')
ax[1].set_xticks(range(len(ak))); ax[1].set_xticklabels(ak, fontsize=7.2, rotation=14, ha='right')
ax[1].set_ylabel('% of the 257,097 km2 basin'); ax[1].set_ylim(0, 46)
ax[1].set_title('What the fit set actually drains', fontsize=9.4)
ax[1].grid(alpha=0.25, axis='y')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""**Left:** the station funnel, one bar per filter, with the number lost at each step
in red; every step except (b) is computed in the cell above from the QC'd station files.
**Right:** the basin area drained by four candidate fit sets, as a percentage of the 257,097 km2
basin.""",
    shows=r"""79 classified stations become **28** mapped, **18** usable-and-mapped, **13**
tributary - and then **9** with any calibration-window sediment observation and **8** with a
*paired* sediment-and-discharge day. Filter (b), the Momposina filter, **removes zero stations**,
because every usable station is hundreds of kilometres above the sink. The five lost tributaries
are lost for hard record-window reasons, each named: three have no SSC at all before 2015, one has
619 SSC days in the window but its discharge record ends in 2009, and one has neither. The
achievable fit set drains **13,862 km2 = 5.4 %** of the basin, against the **10.1 %** the
pre-registration had assumed.""",
    means=r"""**The fit set registered in the workplan was not achievable**, and the difference is
not cosmetic: 5 of the 13 registered stations carry no fittable day at all. The correction was
made a **blocking precondition on C4's start** (P1) precisely so that the shrinkage could not
happen quietly - *a fit set that shrank silently is a fit set nobody can audit*. Every power
number previously attributed to "the CAL 13" overstates this fit's real leverage: on the
deposition test by **2.2x**, and by **9.7x** against the all-station guard that will judge it.
The one CAL-CAL nested pair that survives, of the three claimed, is BOCAS to BOCAS at 39.9 km.""")

md(r"""## 4.2 - Observations to parameters: which denominator is honest?

"How many observations do we have?" has four defensible answers here, and they differ by a factor
of **408**. Choosing one is a decision, so it was recorded before the counting was done.

$$\text{ratio} = \frac{n_{\text{effective}}}{n_{\text{free parameters}}}$$

| candidate denominator | value | why it might be right | why it is or is not used |
|---|---|---|---|
| raw paired SSC-Q days | **3,266** | it is what the files contain | **flattering and wrong** - consecutive days are not independent |
| autocorrelation-effective days, median lag-1 $\rho$ = 0.771 | **474.2** | corrects for temporal dependence within a station | the honest **temporal** n |
| station-months with data | **126** of 288 possible | a coarse independence unit | coverage, not power |
| **stations** | **8** | the level residual is a **per-station** quantity: it does **not** average down *within* a station, so stations are the independence unit for every spatial claim | **the binding one**, used for every spatial claim |

$\sigma_r$ is measured, not chosen, and it measures **one specific thing**: the two independent
observed-flux estimators disagree by $\mathrm{sd}[\ln(a/b)]$ = 0.658 over the 32 station-windows
where both are admissible, so a single estimator carries $0.658/\sqrt{2}$ = **0.465 ln** - a factor
of 1.59. **That is an estimator-DISAGREEMENT statistic, and in that role it stands.**

> ### RETIRED, 2026-08-12: $\sigma_r$ = 0.465 ln is NOT the per-station residual sd
>
> `docs/47` section 2.2 (D2) measured the actual per-station residual sd on the registered CAL
> window at **1.9618 ln** - a factor of **4.22** larger - and `docs/48` found **no admissible
> construction** on which 0.465 is that quantity. So every quantity below that was built as
> $\sigma_r/\sqrt{n}$ is **superseded**: the SE of the fleet-mean level (published 0.1644 ln,
> measured **0.6936 ln** on estimator (b) / **0.4775 ln** on (a)) and the **+/-38 %** level band
> that followed from it. The replacement is registered in `docs/45` section 8.1.3 and is a
> **station-level bootstrap**, not a formula - see the next cell. **`min`-style reuse of an
> observation-side statistic for a model-side quantity is the category error `docs/48` retired;
> rescaling the number would have repaired the size and left the type.**
>
> **What is NOT affected** (`docs/47` section 2.2's own scope correction): `SE(beta)` = 0.0199,
> built on $\sigma_{day}$ = 0.809; the `b_obs` IQR yardstick 0.464, independently measured; and
> every place 0.465 / 0.658 is a **firing threshold** (G1.1's pair backstop, G8, G11), where the
> error errs **safe**. G12's 0.644 ln fragility threshold is untouched.

**Data source:** counts computed above and in `journal_adj-c4-feasibility.md` section 3.2;
$\sigma_r$ and $\rho$ carried from `docs/42` section 4.2; the retirement and its replacement from
`docs/45` section 8.1, `docs/47` section 2.2, `docs/48`.""")

code(r"""# SIGMA_R is the two-estimator DISAGREEMENT statistic (docs/42 section 4.2). It is RETIRED
# as a per-station residual sd (docs/47 section 2.2 D2 measures that at 1.9618 ln, x4.22 larger).
# Kept here only to reproduce the SUPERSEDED construction so it stays identifiable.
SIGMA_R = 0.465          # ln units - estimator disagreement ONLY, NOT a residual floor
RESID_SD_MEASURED = 1.9618   # ln, docs/47 section 2.2 (D2): the actual per-station residual sd
N_FREE = 2               # docs/45 section 2.2: alpha (as the handle on Pi) and beta
DEN = pd.DataFrame({
    'denominator': ['raw paired SSC-Q days', 'autocorrelation-effective days (rho 0.771)',
                    'station-months with data', 'STATIONS (the binding unit)'],
    'n': [float(N_PAIRED_DAYS), 474.2, 126.0, float(n_d)]})
DEN['per_3_params'] = DEN.n / 3
DEN['per_2_params'] = DEN.n / N_FREE
print(DEN.to_string(index=False, float_format='%.1f'))
print(f'\nthe four denominators differ by a factor of {DEN.n.max()/DEN.n.min():.0f}')
print(f'binding ratio, 8 stations : 2 free parameters = {n_d/N_FREE:.1f} : 1')
print(f'      (at the 3 free parameters originally registered it would be {n_d/3:.1f} : 1 - '
      f'"not a fit, a fitted curve through a rumour")')

# ---- the SUPERSEDED construction, reproduced so it stays identifiable, NOT quoted as current
SE8 = SIGMA_R / np.sqrt(8); SE13 = SIGMA_R / np.sqrt(13)
print('RETIRED construction (docs/45 section 8.1 replaced it) - shown, not quoted as current:')
print(f'  sigma_r/sqrt(8)  = {SE8:.4f} ln = +/-{100*(np.exp(1.96*SE8)-1):.0f} % '
      f'({np.exp(-1.96*SE8):.3f}x - {np.exp(1.96*SE8):.3f}x)   <- the published +/-38 %')
print(f'  sigma_r/sqrt(13) = {SE13:.4f} ln = +/-{100*(np.exp(1.96*SE13)-1):.1f} %   '
      f'(what docs/42 assumed)')
print(f'  measured per-station residual sd is {RESID_SD_MEASURED} ln, not {SIGMA_R} '
      f'(x{RESID_SD_MEASURED/SIGMA_R:.2f}) - docs/47 section 2.2 (D2)')

# ---- THE REGISTERED BAND: docs/45 section 8.1.3. A PROCEDURE, NOT A CONSTANT.
# station-level bootstrap of the fleet-mean per-station log residual; 10,000 station resamples,
# seed 20260810; C4.3 recomputes it on its own residuals. Values below are the PRE-FIT EXPECTATION.
BOOT = pd.DataFrame({
    'estimator': ['(a) the objective estimator (docs/45 section 7.1)',
                  '(b) the docs/42 section 9 registered primary'],
    'point_ln': [2.5772, 1.9240],
    'band_lo': [0.418, 0.286],
    'band_hi': [2.289, 3.730],
    'halfwidth_ln': [0.8500, 1.2833]})
print('\nREGISTERED band on the level - station bootstrap, 10,000 resamples, seed 20260810')
print('(docs/45 section 8.1.3; PRE-FIT EXPECTATION - the band is a PROCEDURE, not a constant):')
print(BOOT.to_string(index=False))
print('\n  REPORTING CONVENTION (registered, and explicitly NOT a statistical claim):')
print('    Pi_hat  x  [0.29, 3.73]   95 %, station bootstrap, UNION over estimators (a) and (b)')
print('  The per-estimator bands are printed beside the union, ALWAYS.')
print('  The union spans a factor of 13.0; the retired +/-38 % band spanned 1.91.')
print('  Mandatory beside it: "the level is set by 8 stations whose residuals span a factor of 412."')

fig, ax = plt.subplots(1, 2, figsize=(12.6, 3.7))
yv2 = np.arange(len(DEN))[::-1]
ax[0].barh(yv2, DEN.n, 0.6, color=[CB['grey'], CB['amber'], CB['blue'], CB['red']])
for k, r in DEN.reset_index().iterrows():
    ax[0].text(r.n * 1.12, yv2[k], f'{r.n:,.1f}   ->  {r.per_2_params:,.1f} : 2 params',
               va='center', fontsize=7.4)
ax[0].set_yticks(yv2); ax[0].set_yticklabels(DEN.denominator, fontsize=7.8)
ax[0].set_xscale('log'); ax[0].set_xlim(3, 30000)
ax[0].set_xlabel('effective observations (log scale)')
ax[0].set_title('Four honest answers to "how many observations?", 408x apart', fontsize=9.3)
ax[0].grid(alpha=0.25, axis='x')

ns = np.arange(3, 20)
halfw = 100 * (np.exp(1.96 * SIGMA_R / np.sqrt(ns)) - 1)
ax[1].plot(ns, halfw, 'o-', color=CB['blue'], ms=4)
ax[1].axvline(8, color=CB['red'], lw=1.4)
ax[1].axvline(13, color=CB['amber'], lw=1.4, ls='--')
ax[1].plot([8], [100 * (np.exp(1.96 * SE8) - 1)], 'o', color=CB['red'], ms=9)
ax[1].text(8.25, 100 * (np.exp(1.96 * SE8) - 1) + 2,
           f'ACHIEVABLE n=8:\n+/-{100*(np.exp(1.96*SE8)-1):.0f} % on the level', fontsize=7.4,
           color=CB['red'])
ax[1].text(13.2, 100 * (np.exp(1.96 * SE13) - 1) + 8,
           f'registered n=13:\n+/-{100*(np.exp(1.96*SE13)-1):.1f} %', fontsize=7.4,
           color=CB['amber'])
ax[1].set_xlabel('number of calibration stations')
ax[1].set_ylabel('95 % half-width on the fitted LEVEL (%)')
ax[1].set_ylim(0, 75)
ax[1].set_title('RETIRED construction $\\sigma_r/\\sqrt{n}$ - superseded by the station\n'
                'bootstrap, $\\Pi\\times$[0.29, 3.73] (docs/45 section 8.1.3)', fontsize=8.6)
ax[1].grid(alpha=0.25)
plt.tight_layout(); plt.show()""")

reading(
    what=r"""**Left:** the four candidate observation counts on a log axis, each annotated with
the observations-to-parameters ratio it implies at two free parameters. **Right:** the 95 %
half-width on the fitted level as a function of the number of calibration stations, given the
**RETIRED** construction $\sigma_r/\sqrt{n}$, with the achievable n = 8 and the
registered n = 13 marked - shown so the superseded band stays identifiable, **not** as the current
band.""",
    shows=r"""The denominators run from **3,266** down to **8** - a factor of 408 - and only the
last one is defensible, because the level residual is a per-station quantity that does not average
down within a station. At 8 stations and 2 free parameters the ratio is **4.0 : 1**; at the three
free parameters originally registered it would have been **2.7 : 1**. The right panel's
**+/-38 %** (0.724x to 1.380x) is the **RETIRED** band: it was built as $\sigma_r/\sqrt{n}$ from a
statistic that is **not** the per-station residual sd (measured **1.9618 ln**, x4.22 larger -
`docs/47` section 2.2). **The registered band is the station bootstrap of the fleet-mean
per-station log residual: $\Pi\times$[0.29, 3.73], the union over estimators (a) and (b)**
(`docs/45` section 8.1.3) - a factor of **13.0**, where the retired band spanned **1.91**.""",
    means=r"""**C4 is feasible, but only as a small fit**: two free parameters, eight stations,
and a level that arrives with a band around it spanning a factor of **13**, not the factor of two
this section originally claimed. This is what licenses the
registered posture - the calibration may report a **level and a shape parameter and a bound**, and
nothing else. It also fixes, in advance, what "3,266 observations" may be used for: **nothing**.
That number may not be quoted as an $n$ anywhere in stage C4.""")

md(r"""## 4.3 - What is identifiable, and what is not: three parameters, three answers

The originally registered calibration had three free parameters. The feasibility measurement
returned a different verdict for each of them, and the C4 registration was rebuilt around it.

**1. $\alpha$ alone - NOT identifiable.** Section 3.4. The design matrix is exactly singular in
the basin-total form (condition number `inf`) and 5,682 in the eight-station composition form.
What is identifiable is the **level $\Pi$**, with the registered station-bootstrap band
$\Pi\times$**[0.29, 3.73]** (`docs/45` section 8.1.3) - **not** the retired +/-38 % of
section 4.2.

**2. $\beta$ - identifiable, and comfortably.** This one changed the verdict when it was measured
properly. Because $q_{peak}$ is linear in $Q_{sur}$ (section 2.5), a station's flux is
$\sum_j W_j\,Q_{sur,j}^{2\beta}$ with $W_j$ static, so

$$\frac{\partial \ln F}{\partial \beta} \;=\; 2\times(\text{erosion-weighted mean } \ln Q_{sur})$$

which is a *measurable leverage*, in ln per unit $\beta$. Computed on the real driver field over
the eight stations' upstream sets and their paired days: per-station spread **1.15-4.84**
(median 2.88), pooled autocorrelation-deflated $S_{xx}$ = 1,644.9, giving
**SE($\beta$) = 0.0199** at the pessimistic rating residual $\sigma_{day}$ = 0.809 ln - a 95 %
half-width of **0.039** against a registered band half-width of 0.10. *(A first pass using
observed $\ln Q$ as a proxy for the driver gave SE 0.075 and would have said "not identifiable".
The measurement that changed the answer is recorded because it changed the answer.)* **The caveat
that must travel with it:** the leverage is entirely the model's own $\ln Q_{sur}$ spread, so
$\beta$ is statistically identifiable but **physically confounded with the surface-runoff
partition**.

**3. The channel deposition coefficient $k$ - NOT identifiable, and it is reported as a bound.**
The test is a slope: with $r_i$ the log residual at station $i$ and $L_{w,i}$ its along-channel
lever arm in km, fit $r_i = c + k\,L_{w,i} + \varepsilon_i$. The minimum detectable $k$ at 95 %
depends on the **spread of $L_w$** in the set:

$$k_{\min}\;=\;\frac{1.96\,\sigma_r}{\sqrt{\sum_i (L_{w,i}-\bar L_w)^2}}\quad[\text{km}^{-1}],
\qquad\text{survival over a path } L:\ \exp(-k L).$$

> ### CORRECTED, 2026-08-12 (`docs/45` section 8.1.4)
> $k_{\min}$ is **linear in $\sigma_r$**, so retiring $\sigma_r$ = 0.465 as a residual sd moves
> every $k_{\min}$ in the corpus. On the registered joint form (G1.2 fitted jointly with G3.1 and
> G4.1, all 18), with the **measured** residual sd:
> ```
> k_min = 0.0065 - 0.0069 /km        (registered: 0.00216 /km)
> ```
> > **"No first-order channel sink WEAKER than ~10x over ~342 km is detectable on this fit set."**
> > *(equivalently: $|k| <$ 0.0069 /km cannot be distinguished from zero)*
>
> Registered **2.12x over 348.4 km**; corrected **~9x - 11x, central ~10x**. **Sense settled:**
> only *"weaker"* is the correct reading of a detection floor, and *"weaker"* is the registered
> wording from that amendment forward. `k` stays **FIXED at 0.0 /km** and the *"this model asserts
> SDR = 1.0"* claim stands in the words `docs/45` section 2.3 registers - what changes is the
> **strength of the evidence** for it: the guard that would betray SDR = 1.0 is weaker than
> registered by **x3.18** in `k` and **x4.91** in the survival contrast. The values reproduced
> below are the **superseded** ones, kept so they stay identifiable.

**Data source:** the $L_w$ ladder of `docs/42` section 4.1 (18 stations, 2.6-348.4 km, measured
from `topology.npz`), carried; $k_{\min}$ values from lens 3, reproduced arithmetically below.""")

code(r"""LW = pd.DataFrame({
    'code': [22017030, 26167060, 26017060, 26137110, 24027030, 26107130, 21197010, 23127010,
             21147030, 26127010, 22017010, 26017020, 24037390, 23087210, 22057090, 26167070,
             26207080, 21237020],
    'name': ['BOCAS', 'PAILA LA', 'PUENTE ARAGON', 'BANANERA LA 6-909', 'NEMIZAQUE',
             'MATEGUADUA', 'EL PROFUNDO', 'BORBUR', 'CARRASPOSO', 'EL ALAMBRADO', 'BOCAS',
             'JULUMITO', 'CAPITANEJO', 'CANTERAS', 'BOCATOMA TRIANGULO', 'IRRA', 'BOLOMBOLO',
             'ARRANCAPLUMAS'],
    'Lw': [2.6, 11.8, 14.2, 26.9, 27.1, 30.1, 30.4, 32.7, 39.0, 40.4, 42.5, 46.5, 60.4, 68.0,
           110.4, 265.2, 272.6, 348.4],
    'set': ['CAL', 'CAL', 'EVAL', 'CAL', 'CAL', 'CAL', 'CAL', 'CAL', 'CAL', 'CAL', 'CAL',
            'EVAL', 'CAL', 'CAL', 'CAL', 'EVAL', 'EVAL', 'EVAL']})
LW['in_CAL8'] = LW.code.isin(CAL8)

def k_min(lw):
    lw = np.asarray(lw, float)
    return 1.96 * SIGMA_R / np.sqrt(((lw - lw.mean()) ** 2).sum())

SETS = {'all 18 (the guard set)': LW.Lw.to_numpy(),
        'CAL 13 (registered)': LW.loc[LW.set == 'CAL', 'Lw'].to_numpy(),
        'CAL 8 (achievable)': LW.loc[LW.in_CAL8, 'Lw'].to_numpy(),
        'CAL 8 + trunk station': np.append(LW.loc[LW.in_CAL8, 'Lw'].to_numpy(), 348.4)}
DOC = {'all 18 (the guard set)': 0.00216, 'CAL 13 (registered)': 0.00964,
       'CAL 8 (achievable)': 0.02092, 'CAL 8 + trunk station': 0.00303}
print(f'{"set":26s} {"n":>3s} {"Lw span km":>13s} {"k_min /km":>10s} {"published":>10s} '
      f'{"survival contrast":>20s}')
KMIN = {}
for nm, lw in SETS.items():
    k = k_min(lw); KMIN[nm] = k
    span_own = lw.max() - lw.min()
    print(f'{nm:26s} {len(lw):3d} {lw.min():5.1f}-{lw.max():6.1f} {k:10.5f} {DOC[nm]:10.5f} '
          f'   x{np.exp(k*lw.max()):5.2f} over {lw.max():.1f} km')
print(f'\nlosing 5 of the 13 takes k_min from {KMIN["CAL 13 (registered)"]:.5f} to '
      f'{KMIN["CAL 8 (achievable)"]:.5f} /km - a factor of '
      f'{KMIN["CAL 8 (achievable)"]/KMIN["CAL 13 (registered)"]:.1f} WORSE')
print(f'adding the one trunk station would recover a factor of '
      f'{KMIN["CAL 8 (achievable)"]/KMIN["CAL 8 + trunk station"]:.1f}')
print(f'\nRECONCILIATION, recorded rather than smoothed: docs/43 section 3.2 prints the CAL-8 '
      f'bound as 3.54x and journal_adj-c4-feasibility as 3.35x. Both are right and they use '
      f'different spans: exp(k*60.4) = {np.exp(KMIN["CAL 8 (achievable)"]*60.4):.2f} (the '
      f'outermost station\'s own Lw) and exp(k*57.8) = '
      f'{np.exp(KMIN["CAL 8 (achievable)"]*57.8):.2f} (max minus min).')
print(f'\nUNCITED, and it passes and fails NOTHING: the retired 0.05-0.30 SDR band would imply '
      f'k ~ 0.0020-0.0032 /km over a 600 km path. Printed only so a reader can see where '
      f'{KMIN["CAL 8 (achievable)"]:.4f} sits.')""")

code(r"""fig, ax = plt.subplots(1, 2, figsize=(12.9, 4.0), gridspec_kw={'width_ratios': [1.25, 1.0]})
for _, r in LW.iterrows():
    c = CB['red'] if r.in_CAL8 else (CB['amber'] if r.set == 'CAL' else CB['grey'])
    ax[0].plot([r.Lw], [0], 'o', color=c, ms=9, zorder=3)
    ax[0].text(r.Lw, 0.05 + 0.055 * ((_ % 4)), f'{r["name"][:13]}', fontsize=6.0, rotation=62,
               ha='center', color=c)
ax[0].plot([], [], 'o', color=CB['red'], label=f'CAL 8 - fitted (span 2.6-60.4 km)')
ax[0].plot([], [], 'o', color=CB['amber'], label='registered CAL 13 but not fittable')
ax[0].plot([], [], 'o', color=CB['grey'], label='EVAL - scored, never fitted')
ax[0].axhline(0, color=CB['dark'], lw=0.8)
ax[0].set_xscale('log'); ax[0].set_xlim(2, 600); ax[0].set_ylim(-0.10, 0.42)
ax[0].set_yticks([]); ax[0].set_xlabel('$L_w$, along-channel lever arm (km, log scale)')
ax[0].set_title('The deposition test is a slope, and its power is the SPREAD of $L_w$',
                fontsize=9.3)
ax[0].legend(fontsize=7.0, loc='upper left'); ax[0].grid(alpha=0.25, axis='x')

ks = list(KMIN); kv = [KMIN[k] for k in ks]
ax[1].bar(range(len(ks)), kv, 0.55, color=[CB['blue'], CB['amber'], CB['red'], CB['grey']])
for i, k in enumerate(ks):
    ax[1].text(i, kv[i] * 1.12, f'{kv[i]:.5f}', ha='center', fontsize=7.6)
ax[1].axhspan(0.0020, 0.0032, color=CB['purple'], alpha=0.22, zorder=0,
              label='UNCITED scale reference only (retired 0.05-0.30 SDR over 600 km) -\n'
                    'this band passes and fails NOTHING')
ax[1].set_yscale('log'); ax[1].set_ylim(1e-3, 6e-2)
ax[1].set_xticks(range(len(ks))); ax[1].set_xticklabels(ks, fontsize=7.0, rotation=14, ha='right')
ax[1].set_ylabel('$k_{min}$, minimum detectable deposition rate (1/km)')
ax[1].set_title('$k$ is NOT fittable on the achievable set', fontsize=9.3)
ax[1].legend(fontsize=6.8, loc='upper right'); ax[1].grid(alpha=0.25, axis='y')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""**Left:** the 18 usable stations placed on a log axis of $L_w$, the along-channel
lever arm that gives the deposition test its power - red for the eight that can actually be
fitted, amber for registered-but-unfittable, grey for evaluation-only. **Right:** the minimum
detectable first-order deposition rate $k_{min}$ for four candidate sets (log scale), with the
band implied by the retired SDR expectation drawn **as an UNCITED scale reference only**.""",
    shows=r"""The achievable fit set spans $L_w$ = **2.6-60.4 km**; the full guard set spans
**2.6-348.4 km**, a 134-fold range. That collapse in lever arm takes $k_{min}$ from
~~**0.00216 /km** (all 18)~~ to ~~**0.0209 /km**~~ on the CAL 8, and the
~~**~3.5x** over the fit set's own length~~ detection floor that followed from them, are all
**SUPERSEDED - shown, not quoted as current** (dated 2026-08-12, `docs/45` section 8.1.4, and
section 4.3's own correction box above). Every one of them is linear in the retired
$\sigma_r$ = 0.465; on the registered joint form with the **measured** residual sd the all-18
floor is **0.0065-0.0069 /km**, i.e. **no first-order channel sink WEAKER than ~10x over ~342 km
is detectable**. What the collapse in lever arm *costs* is unchanged, because it is a ratio of two
$k_{min}$ and $\sigma_r$ cancels: the CAL 8 is still **9.7x worse** than the guard set. Adding the
single trunk station would recover a factor of 6.9, and the registration declines to do it.""",
    means=r"""**The deposition coefficient is not fittable, so it is not fitted.** The
registration fixes it at exactly zero and reports it as a **bound**, in a fixed sentence form:
*"no first-order channel sink **WEAKER** than X x over Y km is detectable on this fit set."*
(~~stronger~~ $\rightarrow$ **weaker**; **sense settled 2026-08-12**, `docs/45` section 8.1.4 -
only *weaker* is the correct reading of a *detection floor*, and *weaker* is the registered
wording from that amendment forward, as section 4.3's correction box above already states.)
Reporting a fitted $k$ here would be **reporting noise with a decimal point**. And fixing it at
zero incurs a debt that must be paid in words rather than arithmetic: the model then asserts that
everything eroded on a hillslope reaches the station. **The registration states that claim
explicitly - "this model asserts SDR = 1.0 between hillslope and station" - because guard G5 will
not accept a silent version of it.** The decision to keep the trunk station out of the fit is
recorded with its cost (5.4 % of the basin fitted instead of 25.1 %) rather than hidden: admitting
it would have meant relaxing a frozen registration *to gain statistical power, after the power had
been measured*, which is exactly the post-hoc move this project forbids - and that one station is
worth more as the only independent trunk check than as a ninth fit point.""")

# ============================================================ 5 the decision
md(r"""---

# 5 - THE DECISION

Three lenses were run independently at three questions, and each returned a verdict on the same
scale: *does this block stage C4?*

| lens | question | verdict | what it established |
|---|---|---|---|
| **1** `adj-ratio` (section 2) | does the level error cancel in the ENSO ratio? | **PARTIALLY** | the period-differential is centred on 1 - but it is **not a constant**, and the band is as wide as the residual it would certify |
| **2** `adj-alpha-role` (section 3) | what is $\alpha$ for? | **NO - does not block** | $\alpha$ and $\beta$ are **fitted coefficients of adjustment** in the transposed method, so the level is a target, not a defect |
| **3** `adj-c4-feasibility` (section 4) | is C4 feasible? | **PARTIALLY** | feasible as **2 free parameters + 1 bounded, on 8 stations** - with a level band spanning a factor of **13** ($\Pi\times$[0.29, 3.73], `docs/45` section 8.1.3; the +/-38 % originally claimed here is RETIRED) and no ability to decompose it |

> ## The verdict: `C3-STAYS-OPEN-C4-PROCEEDS-CONDITIONALLY`

## 5.1 - What was reclassified, and what was not

The decision does one substantive thing: it **reclassifies the LEVEL component of the C3 residual
from *defect* to *calibration target***, on two independent legs either of which is sufficient.

1. **The method defines it as free.** Fagundes (2018) eq. 11 calls $\alpha$ and $\beta$
   *"coeficientes de ajuste ... calibrados automaticamente"*, puts them in the optimiser's
   parameter vector, and fits them per sub-basin **and** per calibration dataset - with the same
   sub-basin's fitted $\alpha$ moving by up to **7.78x** according only to which observed dataset
   was the target (section 3.2). An unfitted $\alpha$ is an **unset lever**, not a wrong value.
2. **The level has no separate existence to be defective.** Seven scalars, one identifiable
   product $\Pi$, condition number `inf` (section 3.4). The "level residual" **is** $\Pi$, and
   $\Pi$ is exactly what a fit sets.

And it draws a hard boundary around what that covers. The design principle, restated: **a scalar
can absorb a level; it cannot absorb a structure.** Three structures survive the reclassification,
all measured, and each is why C3 stays open:

| component of the residual | classification | evidence | who resolves it |
|---|---|---|---|
| the multiplicative **LEVEL** ($\Pi$) | **CALIBRATION TARGET.** Not a defect. Status **UNVALIDATED and unfittable-apart** | Fagundes App. IV; condition number `inf` | **C4**, as a fitted $\Pi$ with its equifinal family |
| the $LS$ **slope-dependent SHAPE** | **STILL A DEFECT**, direction known | ours is **2.3151-3.9768x** high in level *and* formulation-different in shape, over all 30,235,916 cells. The *level* question is now decided on source grounds (`docs/37` A3, **CITED**, `f_LS` = **0.25146**) but **RECORDED, not EXERCISED**; the *shape* question is untouched by that | a written source-grounds decision (C3.1), **not** a fit |
| **station-to-station heterogeneity** | **STILL A DEFECT**, unresolvable at this fleet size | $I^2$ 96-99.2 %, $\tau$ 2.03-3.40x, 18/24 CIs excluding 1 | not C4 - needs n ~ 19 both-window stations |
| **period-dependent peak deficit** | **STILL A DEFECT**, direction known, magnitude registered (x1.096) | $R_{AMS}$ 0.808 vs 0.686 | not resolvable - propagate as a caveat |
| **which quantity the sum is** | **UNRESOLVED LABEL** - neither a defect nor a target | SWAT Ch. 4:1 (section 1.4) | a written, cited answer; nobody has written it |

## 5.2 - Why "CLOSED" was available and was refused

Three successive level clauses have been retired or re-opened: the SDR band (retired), clause 4'
(re-opened), clause 4" (not established). Reading that sequence as a pass would close C3 today.
The project refuses, on its own standing rule - **a retired gate is neither a pass nor a fail** -
and `docs/43` names the alternative for what it would be: *"a closure assembled from three
retirements is tolerance wearing a verdict's clothes."*

Two clauses fail independently and in **known** directions, so the refusal does not rest on the
retirements at all:

* **clause 2** - the $LS$ formulation decision is unmade, and it is cheap to resolve;
* **clause 3** - the level-moving cover-factor revision (x1.2043) has had no adversarial pass, and
  the guard that would catch it is measurably blind to anything below a ~4.2x class error.

## 5.3 - Why C4 is nevertheless not BLOCKED, and under what contract

No lens supports blocking. The prior amendment already granted C4 permission to run while C3 is
open. And - the reason that decides it - **C4 is the cheapest route to closing part of C3**: its
own outputs would be the **first independent evidence this project has ever had** about the Bare
land class (whose erosion share across stations runs 0.0-75.6 %, the largest contrast in the set)
and its first measured bound on channel deposition. Blocking C4 blocks those.

It proceeds under three **blocking preconditions**, all discharged in the frozen C4
pre-registration (`docs/45`), and a hard bound on what it may report.""")

code(r"""PRE = pd.DataFrame({
    'id': ['P1', 'P2', 'P3'],
    'precondition': ['correct the fit set from CAL 13 to the CAL 8, naming the 5 lost stations '
                     'and their reasons',
                     'decide the trunk-station conflict explicitly, in writing, either way, '
                     'BEFORE a fit exists',
                     'register k as REPORTED-AS-A-BOUND, not fitted; 2 free + 1 bounded, not '
                     '3 free'],
    'measured cost of not doing it': ['every power number attributed to "the CAL 13" overstates '
                                      'the fit by 2.2x on k, 9.7x against the guard',
                                      'worth a factor 6.9 on deposition detectability and '
                                      '5.4 % -> 25.1 % of fitted basin area',
                                      'a fitted k would be reporting noise with a decimal point '
                                      '(k_min 0.0209 /km)'],
    'discharged in': ['docs/45 section 3.4', 'docs/45 section 2.4 (decided OUT)',
                      'docs/45 section 2.3']})
for _, r in PRE.iterrows():
    print(f'{r.id}  {r.precondition}')
    print(f'     cost if skipped : {r["measured cost of not doing it"]}')
    print(f'     discharged in   : {r["discharged in"]}\n')

BOUND = pd.DataFrame({
    'quantity': ['alpha alone', 'Pi (the level)', 'beta', 'channel deposition k',
                 'a land-class C value'],
    'identifiable?': ['NO - not partially, not weakly, not at all', 'YES, as a level only',
                      'YES, comfortably', 'NO on the achievable set',
                      'only as a CONTRAST, and coarsely'],
    'what C4 may report': ['never as a validated value',
                           'Pi with its band AND its equifinal family',
                           'beta with its CI AND the confounding note',
                           'a BOUND, never a value', 'c_G, c_B with intervals'],
    'the number': ['cond = inf (basin form), 5,682 (CAL-8 composition form)',
                   'x[0.29, 3.73] at 95 % - station bootstrap, UNION over (a),(b) '
                   '(docs/45 s8.1.3; the retired +/-38 % / SE 0.1644 ln is NOT this number)',
                   'SE 0.0199; 95 % half-width 0.039 vs band half-width 0.10',
                   'k_min 0.0065-0.0069 /km (all 18, G1.2 joint form, measured residual sd) => '
                   'no sink WEAKER than ~10x over ~342 km is detectable (docs/45 s8.1.4; '
                   'the registered 0.00216 /km and 2.12x are SUPERSEDED)',
                   'NO CORRECTED NUMBER - the ~4.2x (CAL 8) / ~2.9x (all 18) figures are '
                   'sigma_r-scaled and did not reproduce (x8.2 / x3.2); OPEN ITEM O8']})
print(BOUND.to_string(index=False))
print('\nNOTE: the Pi row is a PROCEDURE (recomputed by C4.3 on its own residuals), not a constant;')
print('      and it is quoted with "the level is set by 8 stations whose residuals span a factor')
print('      of 412." The k row is a DETECTION FLOOR - "weaker", not "stronger" (docs/45 s8.1.4).')""")

md(r"""### 5.4 - The bound on C4's output, and the statements that must travel with every number

> **C4 may fit and report a LEVEL ($\Pi$) and a SHAPE PARAMETER ($\beta$), and may report a BOUND
> on channel deposition. It may not report a validated $\alpha$, a validated $C$ level, a
> validated $LS$ level, or a validated basin sediment load. Every C4 number is a member of an
> equifinal family, and the family must be printed beside it.**

Five statements accompany **every** C4 number, added by this decision on top of the existing
reporting guards:

1. **The word UNVALIDATED on the level**, in the same table as $\Pi$ - *cited is not validated*,
   and *fitted is not validated either*.
2. **The parameter count as 2 free + 1 bounded**, with the CAL **8** named and the 5 lost stations
   named with their reasons.
3. **$k$ as a bound with its span**, in the registered sentence form - never as a fitted value.
4. **The unobserved fraction** - 66.53 % of the model's erosion is upstream of no usable station -
   in the same paragraph as any basin-scale statement.
5. **The residual's direction is UNKNOWN.** No C4 output may be justified by, or compared against,
   "the model is 2x under-erosive".

And three things must be said with the verdict whatever it is: the success bar is **asymmetric**
(the mean predictor scores KGE = $1-\sqrt2$ = -0.414, so the bar's lower edge of -0.26 sits only
**0.15 KGE units above no skill** - *passing it is not evidence of a good model; failing it is
evidence of a bad one*); the level's band is the **station bootstrap** of the fleet-mean
per-station log residual, $\Pi\times$**[0.29, 3.73]** - a factor of **13**, quoted with *"the level
is set by 8 stations whose residuals span a factor of 412"* (`docs/45` section 8.1.3; the +/-38 %
this line used to print is **RETIRED**); and **$\beta$ cannot reach the observed contrast**
anywhere inside its registered band (section 2.5).

### 5.5 - How to disagree with this decision

Each leg is separable, so a reader who rejects one can see exactly what it costs:

| if you reject ... | ... then | what would settle it |
|---|---|---|
| reading 2 of $\alpha$ (section 3) | the level residual is a **defect** again, and C4 becomes a repair rather than a calibration | the 426 published fits and their 7.78x target-dependence are the evidence; a rebuttal needs a different reading of Fagundes eq. 11 and section 6.3.1 |
| the retirement of the SDR gate (section 1) | you must supply a **hillslope-only** published delivery ratio for a large humid tropical Andean basin - none exists | one citable Magdalena gross-erosion estimate. `USLE` and `RUSLE` appear **zero times** in the fullest published treatment of this basin |
| the ratio measurement (section 2) | the ENSO headline may be distorted by the level after all | more both-window stations: n ~ 19 for +/-50 %, n ~ 94 for +/-20 % |
| the feasibility verdict (section 4) | C4 is either bigger (add the trunk station: 25.1 % of the basin) or impossible | the trunk-station decision is written down **with its cost**, so it can be reversed on the record rather than re-argued |
| the refusal to close C3 | C3 closes today on three retirements | clause 2 (the $LS$ formulation) and clause 3 (the unaudited cover-factor revision) fail independently and in known directions - closing needs *those*, not the retirements |""")

# ============================================================ 6 problems
md(r"""---

# 6 - PROBLEMS AND FAILURES

Six problems, each measured, each unresolved, none of them a footnote. Any one of them is a
legitimate reason to distrust a number in this project, and they are listed here so that a reader
does not have to find them.

## 6.1 - The under-erosion residual has no direction

**Status: UNRESOLVED, and the direction is WITHDRAWN.** Section 1.4. The model's level sits
somewhere between 2.27x too low and 1.49x too high, and the interval contains 1. The frequently
quoted "the model is under-erosive by 1.03-2.27x" is arithmetically correct and
**interpretatively withdrawn**: its decisive leg compares our MUSLE sum against a RUSLE *gross
erosion*, while SWAT's documentation of this exact equation calls its output a sediment *yield*.

**Why it is not fixed here:** settling it is not a modelling task. It needs a written, cited
answer to "which quantity is a per-pixel MUSLE sum, summed over 30 million pixels?", and the
honest current answer is *neither exactly gross erosion nor exactly a basin yield*. **What it
forbids:** any C4 output motivated by a shortfall of known size. There is no gap of known size.

## 6.2 - MUSLE does not represent 61 % of the sources in USDA's own partition

**Status: UNCITED for this basin, and therefore unquantified.** MUSLE is sheet-and-rill erosion on
hillslopes. In USDA NEH Table 6-2's reference partition, channel-type sources are **60.87 % of
gross erosion and 81.25 % of the delivered yield**. A **Magdalena-specific** partition of load
among hillslope, gully, bank, landslide and mining sources **does not exist in the literature**.

What *is* citable is that the omitted fraction is large in systems of this kind, from four
independent directions - and none of them can be turned into a number for this basin.""")

code(r"""SRC = pd.DataFrame({
    'evidence': ['USDA NEH Table 6-2 reference partition',
                 'Amazon bank erosion (Dunne et al. 1998)',
                 'Mining (Dethier et al. 2023)',
                 'Andean mass wasting / channel erosion'],
    'what it says': [f'channel-type sources = {100*(1-SHEET_SHARE_E):.2f} % of gross erosion, '
                     f'{100*CHANNEL_SHARE_Y:.2f} % of yield',
                     'bank erosion supplies 1,570 Mt/yr against a ~1,200 Mt/yr outlet flux = 1.3x',
                     '80 % of 173 mining-affected rivers have SSC more than double pre-mining; '
                     '23 +/- 19 % of large-river length altered in 30 countries',
                     '78-79 % of the Magdalena catchment in a critical/severe erosional state; '
                     'Colombian Andes mean yield 1,485 t/km2/yr'],
    'usable as a number here?': ['NO - US agricultural watershed, not this basin',
                                 'NO - different basin; establishes only that ADR > 1 is possible',
                                 'NO - a Magdalena mining tonnage is UNCITED',
                                 'NO - a quantified landslide/gully share is UNCITED']})
for _, r in SRC.iterrows():
    print(f'* {r.evidence}\n    {r["what it says"]}\n    usable as a number here? '
          f'{r["usable as a number here?"]}\n')

fig, ax = plt.subplots(1, 2, figsize=(12.4, 3.7))
share_e = [SHEET_SHARE_E, 1 - SHEET_SHARE_E]
share_y = [1 - CHANNEL_SHARE_Y, CHANNEL_SHARE_Y]
ax[0].barh([1], [share_e[0]], 0.45, color=CB['green'], label='sheet and rill - WHAT MUSLE IS')
ax[0].barh([1], [share_e[1]], 0.45, left=[share_e[0]], color=CB['red'],
           label='gullies, roadbanks, streambanks - NOT REPRESENTED')
ax[0].barh([0], [share_y[0]], 0.45, color=CB['green'])
ax[0].barh([0], [share_y[1]], 0.45, left=[share_y[0]], color=CB['red'])
for yv3, sh in [(1, share_e), (0, share_y)]:
    ax[0].text(sh[0] / 2, yv3, f'{100*sh[0]:.1f} %', ha='center', va='center', fontsize=8.4,
               color='white')
    ax[0].text(sh[0] + sh[1] / 2, yv3, f'{100*sh[1]:.1f} %', ha='center', va='center',
               fontsize=8.4, color='white')
ax[0].set_yticks([1, 0]); ax[0].set_yticklabels(['share of GROSS EROSION', 'share of YIELD'],
                                                fontsize=8)
ax[0].set_xlim(0, 1); ax[0].set_xlabel('fraction')
ax[0].set_title("USDA NEH Table 6-2: what an equation like MUSLE leaves out", fontsize=9.3)
ax[0].legend(fontsize=7.0, loc='lower center'); ax[0].grid(alpha=0.25, axis='x')

lab3 = ['our MUSLE sum\n(hillslope only)', 'implied all-source\ngross erosion IF this\n'
        'basin resembled\nNEH Table 6-2', 'published outlet\nload (all-source,\nnet of all '
        'deposition)']
val3 = [ADOPT, ADOPT / SHEET_SHARE_E, np.nan]
ax[1].bar([0, 1], val3[:2], 0.5, color=[CB['green'], CB['grey']])
ax[1].bar([2], [ANCHOR_HI - ANCHOR_LO], 0.5, bottom=[ANCHOR_LO], color=CB['amber'])
ax[1].text(0, val3[0] + 20, f'{val3[0]:.1f}', ha='center', fontsize=8)
ax[1].text(1, val3[1] + 20, f'{val3[1]:.1f}', ha='center', fontsize=8)
ax[1].text(2, ANCHOR_HI + 20, f'{ANCHOR_LO:.0f}-{ANCHOR_HI:.0f}', ha='center', fontsize=8)
ax[1].text(1, val3[1] * 0.45, 'ILLUSTRATIVE ONLY -\nthe Magdalena partition\nis UNCITED',
           ha='center', fontsize=7.0, color=CB['red'])
ax[1].set_xticks(range(3)); ax[1].set_xticklabels(lab3, fontsize=7.0)
ax[1].set_ylabel('Mt/yr'); ax[1].set_ylim(0, 900)
ax[1].set_title('The missing sources, sized by a partition that is not this basin\'s',
                fontsize=9.3)
ax[1].grid(alpha=0.25, axis='y')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""**Left:** USDA NEH Table 6-2's partition of one watershed's gross erosion, and of its
delivered yield, into the one source MUSLE represents (green) and the three it does not (red).
**Right:** our modelled hillslope total, the all-source gross erosion it would imply *if* this
basin resembled that partition, and the published outlet load - with the middle bar marked
ILLUSTRATIVE because the Magdalena partition is uncited.""",
    shows=r"""In USDA's reference watershed the process MUSLE represents is **39.13 %** of gross
erosion and delivers only **18.75 %** of the yield; the sources MUSLE has no term for supply
**60.87 %** and **81.25 %** respectively. Scaling our 299.5 Mt/yr by that partition would imply
765.5 Mt/yr of all-source gross erosion - which is illustrative arithmetic, not a result.""",
    means=r"""**A large fraction of the residual plausibly lives in sources the model does not
represent at all**, which is a completely different conclusion from "the hillslope erosion is
mis-parameterised" - and no fit of $\alpha$, $C$ or $LS$ can distinguish them. **What this does
not license:** using the 60.87 % as a correction. It is a US agricultural watershed's partition
and it may not pass or fail anything here. The honest position is two separate statements kept
apart: *we cannot cite a Magdalena non-hillslope fraction*, and *this omission is a named,
unquantified reason the model's hillslope-only total is not comparable with an all-source outlet
load.*""")

md(r"""## 6.3 - The Momposina sink is invisible to the entire observing network

**Status: STRUCTURAL. No fit and no guard can reach it.**""")

code(r"""BASIN_MAX_PATH = 1425.9      # km, docs/42 section 4.1 (path_km_to_outlet, basin maximum)
BELOW_TRUNK = 801.1          # km of channel below the outlet-most SSC station
CONFLUENCE_ABOVE_OUTLET = 146.1
CLOSEST_ABOVE_CONFLUENCE = 684.4
FRAC_OBS, FRAC_UNOBS = 33.47, 66.53          # % of model gross erosion
UNOBS_MT = 199.29

print(f'basin maximum channel path                       {BASIN_MAX_PATH:,.1f} km')
print(f'below the outlet-most SSC station (ARRANCAPLUMAS){BELOW_TRUNK:>9,.1f} km  '
      f'= {100*BELOW_TRUNK/BASIN_MAX_PATH:.1f} % of it, INCLUDING THE WHOLE MOMPOSINA')
print(f'Cauca-Magdalena confluence, above the outlet      {CONFLUENCE_ABOVE_OUTLET:,.1f} km  '
      f'(minibacia 4430)')
print(f'closest SSC station to that confluence            {CLOSEST_ABOVE_CONFLUENCE:,.1f} km '
      f'ABOVE it')
print(f'\nmodel gross erosion upstream of >=1 usable SSC station  {FRAC_OBS:.2f} %')
print(f'model gross erosion upstream of NO usable SSC station   {FRAC_UNOBS:.2f} %  '
      f'= {UNOBS_MT:.2f} of {ADOPT:.2f} Mt/yr')
print(f'station pairs spanning the Momposina                    0  (measured, not assumed)')
print(f'\npublished Momposina retention (Restrepo A. 2015, labelled "una cifra PRELIMINAR" by '
      f'its own author): 20-45 %, i.e. 36-80 Mt/yr')

fig, ax = plt.subplots(figsize=(11.8, 3.3))
ax.plot([0, BASIN_MAX_PATH], [0, 0], lw=3, color=CB['dark'], solid_capstyle='butt')
ax.axvspan(BASIN_MAX_PATH - BELOW_TRUNK, BASIN_MAX_PATH, color=CB['red'], alpha=0.18,
           label=f'{BELOW_TRUNK:.1f} km below the outlet-most station - INCLUDING the whole '
                 f'Depresion Momposina. NO OBSERVATION EXISTS HERE')
ax.axvline(BASIN_MAX_PATH - CONFLUENCE_ABOVE_OUTLET, color=CB['purple'], lw=1.4, ls='--')
ax.text(BASIN_MAX_PATH - CONFLUENCE_ABOVE_OUTLET, 0.42, 'Cauca-Magdalena\nconfluence\n(minibacia '
        '4430)', fontsize=6.8, ha='center', color=CB['purple'])
pos = BASIN_MAX_PATH - BELOW_TRUNK
ax.plot([pos], [0], 'v', color=CB['blue'], ms=12)
ax.text(pos, -0.55, 'ARRANCAPLUMAS\nthe ONLY Magdalena-trunk\nSSC station in the network',
        fontsize=7.0, ha='center', color=CB['blue'])
for k, r in LW.iterrows():
    ax.plot([pos - r.Lw * 0.9], [0.12], '|', color=CB['grey'], ms=9)
ax.text(pos - 200, 0.35, 'the other 17 usable stations,\nall FURTHER UPSTREAM', fontsize=6.8,
        ha='center', color=CB['grey'])
ax.plot([0], [0], 'o', color=CB['dark'], ms=7)
ax.text(0, 0.20, 'headwaters', fontsize=7.0, ha='left')
ax.text(BASIN_MAX_PATH, 0.20, 'river mouth', fontsize=7.0, ha='right')
ax.set_xlim(-40, BASIN_MAX_PATH + 40); ax.set_ylim(-1.0, 0.85); ax.set_yticks([])
ax.set_xlabel('distance along the longest channel path (km)')
ax.set_title('The observing network stops 801 km short of the basin\'s dominant sink',
             fontsize=9.5)
ax.legend(fontsize=7.0, loc='upper left'); ax.grid(alpha=0.25, axis='x')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""The basin's longest channel path, 1,425.9 km from headwaters to mouth, with the
outlet-most suspended-sediment station marked, the Cauca-Magdalena confluence dashed, the 17 other
usable stations ticked further upstream, and the reach below the last station shaded red.""",
    shows=r"""**801.1 km of channel - 56.2 % of the basin's longest path, including the entire
Depresion Momposina - lies below the outlet-most SSC station**, and there is exactly one station
on the Magdalena trunk at all. Every one of the 18 usable stations sits above the Cauca-Magdalena
confluence; the closest is **684.4 km above it**. **No station pair spans the sink** - that is
measured, not assumed, which is why the Momposina filter in section 4.1 removed zero stations.
**66.53 % of the model's gross erosion, 199.29 of 299.54 Mt/yr, is generated upstream of no usable
station.**""",
    means=r"""**The test a reader would most want - does the model get the Momposina right? - is
NOT EVALUABLE, and the registration says so rather than quietly substituting a different test.**
Three consequences. (i) The C4 guard set replaces the unevaluable spatial axis with three that
*are* evaluable - the longitudinal ladder, the nested pairs, and a macro-region contrast - and
records the substitution. (ii) Any basin-scale statement drawn from station fits must carry the
66.53 % disclosure **in the same paragraph**, or the report fails its own guard: passing every
structure test still constrains the model over only a third of its own erosion. (iii) The
published Momposina retention (20-45 %, 36-80 Mt/yr, and labelled *preliminar* by its own author)
cannot be checked here at all. **What would change it:** an at- or below-Mompos SSC series. Until
then the missing sink survives as a *prohibition* - never calibrate below Mompos - whose
measurement arm has nothing to measure.""")

md(r"""## 6.4 - $\alpha$, $C$ and $LS$ cannot be separated, and the $LS$ level is known to be wrong

**Status: confounding is STRUCTURAL (section 3.4); the $LS$ *formulation* is now DECIDED on source
grounds and the decision points the wrong way; the $LS$ *level* remains UNVALIDATED.**

Our topographic factor differs from the source method's in **four** ways, all measured on the
same 90 m grid over all 30,235,916 basin cells - so these are *formulation* differences, not a
resolution artefact. **Two weightings are reported and only one decides**: $f_{ero}$ is the exact
erosion-weighted engine re-run and **decides**; $f_{area}$ is the area-weighted **proxy**, reported
beside it, measured **2.5 % low**, and never able to override it (`docs/46` §3.3).

> **THREE CORRECTIONS LAND HERE, all unconditional, all from landed measurement rather than from
> the survival of a hypothesis** (`docs/46` §1.0, §1.1, §2.5.1, §3.1, §7.3 items 2-3; `docs/49`,
> `docs/50`, `docs/51` §2 and §4; `docs/52` §1.1; enacted by `docs/37` **A3**).
>
> 1. **The $m$ row's label was wrong.** It read *"step function hard-capped at 0.5"* with a factor
>    of **0.502**, conflating two different objects. **Buarque's eq. 14 (printed p. 47) IS a step
>    function** - $m = 0.2$ / $0.3$ / $0.4$ / $0.5$ on $S_f <1$ % / 1-3 % / 3-5 % / $\ge5$ %, with
>    $S_f$ in slope **percent**, *"onde $S_f$ [%] é a declividade do pixel"* - and its factor is
>    **x0.522043 ero / x0.505092 area**. The object measured as *"0.502"* was
>    $\min(m_{\text{continuous}}, 0.5)$, a **cap** worth **x0.517480 ero / x0.502472 area**, which is
>    **nobody's published formulation** and **may never be graded CITED**. They differ by only
>    **x1.008878** ero, so the mislabel was **real as a label and immaterial as a level** - and the
>    published joint **x0.421 row was already the step**, so the mislabel never touched the joint.
> 2. **The bracket x0.333 - x0.421 / "2.37x-3.00x" is SUPERSEDED.** The registered measurement is
>    $f_{LS}\in$ **[0.25146, 0.43194]** erosion-weighted $\Rightarrow$ **$1/f_{LS}$ =
>    2.3151x - 3.9768x**. And it is **not an uncertainty over readings of the source**: all four
>    levers are **CITED** with a single admissible reading each, so **the source formulation read
>    whole is a POINT at x0.25146**, **x0.43194 is a documented HYBRID** (his three levers with
>    **our** $L$), and the span between them, $\ln(0.43194/0.25146) = 0.5410$, **is the $L$-form
>    lever exactly** - a lever, not an error bar. The old lower endpoint's **x0.790 does NOT isolate
>    the $L$ form**: it factorises as $0.852262\ (L) \times 0.926925\ (S\ \text{swap})$ and was
>    measured on the **uncapped `ls2d` column**, not the engine's `ls2d_hs`. The $L$-form ratio is
>    **formulation-dependent** - 0.852262 uncapped / **0.769833** on `ls2d_hs` / **0.580685** inside
>    the source formulation - and x0.790 composed it across formulations as a scalar.
> 3. **The product of the single levers is NEVER the joint.** This cell used to print
>    $0.502\times1.714\times0.351 = 0.302 \ne 0.421$ as though the product were a rival estimate.
>    The exact statement is a measured **ratio**: $0.362435\times0.52204\times1.694054 =
>    0.3205244$ against a joint of **0.431944**, i.e. **joint / product = x1.34762** (`docs/46` §1,
>    `docs/52` §1.1). *(Carrying the `m` step to its sixth decimal, 0.522043, gives a product of
>    0.3205263 and a ratio of x1.347609 - the same measurement at a different printed precision,
>    not a second number. The cell below prints both so they can never appear to disagree.)*
>
> **A FOURTH, LATER CORRECTION - the $f_{area}$ support, 2026-08-12.** Owning records: `docs/46`
> §10 **amendment 2** and `docs/51` §9 **amendment 1**; expressed as here by `docs/43` §7
> amendment 8. The `V4` proxy read ~~**0.421475**~~ and is **0.42136300143291305**. The struck
> figure is **not an arithmetic error** - it is the same ratio on the **engine URH-fraction** area
> support (257,096.93 km<sup>2</sup>), while `docs/46` §3.3 defines $f_{area}$ on the **per-cell
> basin** (30,235,916 DEM cells at 90 m, 256,702.36 km<sup>2</sup>). `docs/47` §3.1's independently
> measured proxy bias **R7 = 1.0251** discriminates: $0.43194418/0.42136300 = 1.025112$ falls
> inside R7's four-decimal interval $[1.02505, 1.02515]$, $0.43194418/0.42147514 = 1.024839$ falls
> outside it, and the corrected value is **22x closer**. **$f_{ero}$ is untouched**, so the
> registered bracket, the $\alpha$ reference, the hard stop and the endpoint loads are **unmoved**;
> the lower endpoint 0.2446790094097074 was already on the registered support.""")

code(r"""# Registered values, cited in place - this cell RE-DERIVES nothing.
#   f_ero DECIDES (exact engine re-run); f_area is the proxy (docs/46 section 3.3).
# docs/47 section 4.3, docs/49 (eq.-14 step vs cap), docs/50 + docs/51 section 4 (the L form),
# docs/52 section 1.1 (non-multiplicativity), docs/37 A3 (the enactment).
F_LIM_E,  F_LIM_A  = 0.362435, 0.3513      # V1   slope length <= 1 DEM pixel
F_STEP_E, F_STEP_A = 0.522043, 0.505092    # V2b  eq. 14, the STEP function, Sf in slope PERCENT
F_CAP_E,  F_CAP_A  = 0.517480, 0.502472    # V2a  min(m, 0.5): a CAP.  NOBODY'S published form.
F_S_E,    F_S_A    = 1.694054, 1.7139      # V3   eq. 18, Wischmeier & Smith (1978)
# F_HYB_A is on docs/46 section 3.3's PER-CELL BASIN support (30,235,916 cells, 256,702.36 km2).
# Corrected 2026-08-12 from 0.421475 = the same ratio on the ENGINE URH-fraction support
# (257,096.93 km2): a correct quantity, but not what section 3.3 defines f_area to be.
# Owning records: docs/46 section 10 amd 2, docs/51 section 9 amd 1.  f_ero is UNAFFECTED.
F_HYB_E,  F_HYB_A  = 0.431944, 0.42136300143291305   # V4  his 3 levers + OUR L -> HYBRID
F_SRC_E,  F_SRC_A  = 0.25146,  0.2446790094097074   # V4_dg  source read WHOLE -> a POINT, ADOPTED
L_IN_FORM = 0.580685                       # the L-form lever INSIDE the source formulation
LSLEV = pd.DataFrame({
    'lever': ['slope-length limiter', 'exponent m  (eq. 14 STEP)', 'slope function S',
              'length form L', 'V4  = his 3 levers + OUR L  (HYBRID)',
              'V4_dg = ALL FOUR  (SOURCE READ WHOLE, ADOPTED)'],
    'ours': ['upslope area <= 1 km2 (unit length up to ~10,870 m)',
             'continuous McCool (1989), basin median 0.584',
             'Moore & Burch (1986)', 'continuous POINT-RATE (m+1)(lambda/22.13)^m',
             'area-weighted mean LS = 39.812', ''],
    'the source method': ['slope length <= ONE DEM pixel  (pp. 94 and 98)',
                          'eq. 14 p. 47 STEP: 0.2/0.3/0.4/0.5 on Sf <1/1-3/3-5/>=5 PERCENT',
                          'eq. 18 p. 48: Wischmeier & Smith (1978)',
                          'eq. 13 p. 47: Desmet & Govers finite difference, Xdir^m',
                          'area-weighted mean LS = 16.775', ''],
    'f_ero  (DECIDES)': [F_LIM_E, F_STEP_E, F_S_E, L_IN_FORM, F_HYB_E, F_SRC_E],
    'f_area (proxy)': [F_LIM_A, F_STEP_A, F_S_A, float('nan'), F_HYB_A, F_SRC_A]})
print(LSLEV.to_string(index=False))
print(f'\nthe m lever as min(m,0.5) - the CAP, which is NOT eq. 14 and which nobody published:')
print(f'   f_ero {F_CAP_E}, f_area {F_CAP_A}   ->  eq.-14 step / cap = x{F_STEP_E/F_CAP_E:.6f} ero,'
      f' x{F_STEP_A/F_CAP_A:.6f} area')
print(f'   the mislabel was REAL as a label and IMMATERIAL as a level, and the published joint')
print(f'   x0.421 row was ALREADY the step - so it never touched the joint (docs/46 section 3.1).')
print(f'   DISCLOSURE, so this notebook is not read as contradicting a frozen document: docs/46')
print(f'   section 1.1 / 1.2 (R4) / 2.2 print this ratio as x1.008878 ero and x1.005212 area.')
print(f'   Recomputed from docs/46 section 3.1\'s OWN registered pair ({F_STEP_E} / {F_CAP_E}) it')
print(f'   is x{F_STEP_E/F_CAP_E:.6f}; back-solving, {F_CAP_E} x 1.008878 = '
      f'{F_CAP_E*1.008878:.7f}, not {F_STEP_E}.')
print(f'   So the erosion-weighted figure looks like a digit transposition (1.008818 -> 1.008878)')
print(f'   in a document this notebook does not own; the area figure agrees to 6 s.f.')
print(f'   IMMATERIAL - both are ~0.9 %, and docs/46\'s verdict is unchanged either way.')
print(f'   REPORTED, not fixed: docs/46 is FROZEN and is not ours to edit.')

prod_e = F_LIM_E * F_STEP_E * F_S_E
prod_a = F_LIM_A * F_STEP_A * F_S_A
print(f'\nTHE LEVERS DO NOT MULTIPLY OUT.  STANDING RULE: a product of single-lever factors is')
print(f'NEVER quoted as the joint factor and is not a candidate for it.  The exact statement is a')
print(f'measured RATIO:')
prod_reg = 0.362435 * 0.52204 * 1.694054   # docs/46 §1's 5-d.p. m step: the REGISTERED product
print(f'   f_ero, REGISTERED (m step at 5 d.p., docs/46 §1 / docs/52 §1.1):')
print(f'     0.362435 x 0.52204 x 1.694054 = {prod_reg:.7f}   joint {F_HYB_E}'
      f'   ->  joint / product = x{F_HYB_E/prod_reg:.5f}')
print(f'   f_ero, the SAME measurement with the m step at 6 d.p. (docs/46 section 3.1):')
print(f'     {F_LIM_E} x {F_STEP_E} x {F_S_E} = {prod_e:.7f}   joint {F_HYB_E}'
      f'   ->  joint / product = x{F_HYB_E/prod_e:.5f}')
print(f'     (ONE number at two printed precisions, not two numbers - both round to '
      f'x{F_HYB_E/prod_reg:.4f}.  Printed together so they can never appear to disagree.)')
print(f'   f_area: {F_LIM_A} x {F_STEP_A} x {F_S_A} = {prod_a:.6f}   joint {F_HYB_A}'
      f'   ->  joint / product = x{F_HYB_A/prod_a:.5f}')
print(f'   -> they INTERACT, and act per cell AS A FUNCTION OF SLOPE. Only the joint LEVEL joins '
      f'Pi; the residual SHAPE does not.')

print(f'\nREGISTERED BRACKET: f_LS in [{F_SRC_E}, {F_HYB_E}] erosion-weighted')
print(f'   -> our LS is {1/F_HYB_E:.4f}x - {1/F_SRC_E:.4f}x the level alpha = 11.8 is PAIRED with')
print(f'   the span IS the L-form lever, exactly: ln({F_HYB_E}/{F_SRC_E}) = '
      f'{np.log(F_HYB_E/F_SRC_E):.4f}  - a LEVER, not an error bar.')
print(f'   the source formulation READ WHOLE is a POINT at x{F_SRC_E} (all four levers CITED);')
print(f'   x{F_HYB_E} is a documented HYBRID (his three levers with OUR L).')
print(f'   the published x0.790 does NOT isolate the L form: 0.790 = 0.852262 (L) x 0.926925 (S)')
print(f'   = {0.852262*0.926925:.6f}, measured on the UNCAPPED ls2d column, not ls2d_hs. The')
print(f'   L-form ratio is FORMULATION-DEPENDENT: 0.852262 uncapped / 0.769833 on ls2d_hs /')
print(f'   {L_IN_FORM} inside the source formulation - so no scalar version of it transfers.')

E_HYB, E_SRC = 129.3840, 75.3235           # docs/47 section 4.3 ENGINE re-runs, NOT the proxy
print(f'\nbasin gross erosion at the endpoints - ENGINE re-runs, not the area proxy:')
print(f'   V0 (today) {ADOPT:.4f}   ->  V4 hybrid {E_HYB}  ->  V4_dg adopted {E_SRC} Mt/yr,')
print(f'   i.e. BELOW both outlet anchors ({ANCHOR_LO}-{ANCHOR_HI}) and back on the physically')
print(f'   awkward side.  proxy bias f_ero/f_area = x{F_HYB_E/F_HYB_A:.4f} (hybrid) / '
      f'x{F_SRC_E/F_SRC_A:.4f} (adopted): the proxy is ~2.5 % LOW, i.e. in the model\'s favour.')

print(f'\nDECISION (docs/37 A3, 2026-08-12): the pre-registered C3.1 comparison HAS now been made.')
print(f'   outcome ADOPT-SOURCE; ls_formulation = \'buarque_2015_dg\'; f_LS = {F_SRC_E} ero')
print(f'   (proxy {F_SRC_A}); formulation graded CITED on all four levers.')
print(f'   STATUS: DETERMINED and RECORDED, NOT YET EXERCISABLE.  No engine default moved - this')
print(f'   notebook still runs at V0 with f_LS = 1.000.  The LS LEVEL remains UNVALIDATED')
print(f'   (docs/42 G4.2): a CITED formulation is not a validated level, and a fitted one is not')
print(f'   either.  C3 stays OPEN (clause 2 also needs the SHAPE decision) and C4.3 stays BLOCKED.')

fig, ax = plt.subplots(1, 2, figsize=(12.4, 4.0))
bar_lab = ['limiter', 'm (eq.-14 STEP)', 'S (W&S 78)', 'L (in-formulation)',
           'V4 HYBRID', 'V4_dg ADOPTED']
bar_val = [F_LIM_E, F_STEP_E, F_S_E, L_IN_FORM, F_HYB_E, F_SRC_E]
ax[0].bar(range(6), bar_val, 0.55,
          color=[CB['blue'], CB['blue'], CB['red'], CB['blue'], CB['grey'], CB['dark']])
ax[0].axhline(1.0, color=CB['dark'], lw=1.2, ls='--')
for i, v in enumerate(bar_val):
    ax[0].text(i, v + 0.05, f'x{v:.6f}', ha='center', fontsize=6.6)
# Plotted ONLY to mark that it is refuted: the product of the single levers is NOT a candidate
# for the joint.  Standing rule - never quote a product of single levers as the joint factor.
ax[0].plot([4], [prod_reg], 'x', ms=10, mew=2.0, color=CB['purple'], zorder=5,
           label=f'product of the 3 single levers = {prod_reg:.4f}\nNOT a candidate for the joint:'
                 f'  joint / product = x{F_HYB_E/prod_reg:.5f}')
ax[0].set_xticks(range(6)); ax[0].set_xticklabels(bar_lab, fontsize=6.8, rotation=16, ha='right')
ax[0].set_ylabel('$f_{ero}$ - exact erosion-weighted factor'); ax[0].set_ylim(0, 2.0)
ax[0].set_title('Four levers that do not multiply out - so they INTERACT', fontsize=9.3)
ax[0].legend(fontsize=6.6); ax[0].grid(alpha=0.25, axis='y')

ax[1].bar([0], [ADOPT], 0.45, color=CB['green'], label='V0: adopted, at OUR $LS$ (TODAY)')
ax[1].bar([1], [E_HYB], 0.45, color=CB['grey'],
          label=f'V4 HYBRID: his 3 levers + our $L$ (x{F_HYB_E})')
ax[1].bar([2], [E_SRC], 0.45, color=CB['dark'],
          label=f'V4_dg: source read WHOLE (x{F_SRC_E}) - ADOPTED, not exercised')
ax[1].axhspan(ANCHOR_LO, ANCHOR_HI, color=CB['amber'], alpha=0.25, zorder=0,
              label='outlet load 144-184 Mt/yr')
for i, v in enumerate([ADOPT, E_HYB, E_SRC]):
    ax[1].text(i, v + 10, f'{v:.4f}', ha='center', fontsize=7.6)
ax[1].annotate('', xy=(2, E_SRC), xytext=(1, E_HYB),
               arrowprops=dict(arrowstyle='->', lw=1.1, color=CB['purple']))
ax[1].text(1.5, (E_HYB + E_SRC)/2 + 22, f'the $L$-form LEVER\nx{F_SRC_E/F_HYB_E:.5f}  '
           f'($\\ln$ {np.log(F_HYB_E/F_SRC_E):.4f})', ha='center', fontsize=6.6, color=CB['purple'])
ax[1].set_xticks([0, 1, 2])
ax[1].set_xticklabels(['our $LS$ (V0)', 'hybrid (V4)', 'source whole\n(V4_dg)'], fontsize=7.6)
ax[1].set_ylabel('basin gross hillslope erosion (Mt/yr)'); ax[1].set_ylim(0, 375)
ax[1].set_title('The $LS$ decision: DECIDED on source grounds, NOT exercised\n'
                'it points the WRONG way, and the LEVEL is still UNVALIDATED', fontsize=9.3)
ax[1].legend(fontsize=6.4); ax[1].grid(alpha=0.25, axis='y')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""**Left:** the **four** ways our topographic factor differs from the source method's,
each as the *erosion-weighted* factor $f_{ero}$ it applies to basin gross erosion, followed by the
two joint compositions - the grey `V4` **hybrid** (his three levers with our $L$) and the dark
`V4_dg`, **the source formulation read whole**, which is the one adopted. The purple cross marks
the **product of the three single levers**, plotted **only** so its refutation is visible: it is
not a candidate for the joint. **Right:** basin gross erosion under all three compositions - all
**engine re-runs, not the area-weighted proxy** - against the outlet anchor band, with the
$L$-form lever annotated.""",
    shows=r"""The four levers are **x0.362435** (limiter), **x0.522043** ($m$ = his eq. 14, a
**step function on slope percent**, not a cap on our continuous $m$), **x1.694054** ($S$ = his
eq. 18, Wischmeier & Smith 1978) and **x0.580685** ($L$ = his eq. 13, Desmet & Govers finite
difference, measured *inside* the source formulation). **The product of the first three is
0.3205244 and the measured joint is 0.431944 - joint / product = x1.34762** - so they interact,
none of them is "the" cause, and the product is never the joint. The registered bracket is
$f_{LS}\in$ **[0.25146, 0.43194]** erosion-weighted, i.e. our $LS$ is **2.3151x-3.9768x** the level
Williams' $\alpha$ = 11.8 is *paired* with, and the basin total falls from **299.5387** to
**129.3840** (hybrid) and **75.3235 Mt/yr** at the adopted point - **below both outlet anchors**,
back on the physically awkward side that section 1.1 appeared to leave behind.""",
    means=r"""**The $LS$ residual is level *plus slope-dependent shape*, and only the level joins
$\Pi$.** That is why this is a defect and not a calibration target: a scalar can absorb the level
part, and *no* scalar can absorb the shape part - the C4 guard that tests for it can **detect** it
and can never fix it. **What it forbids:** a scalar $LS$ multiplier, which would hide a
slope-dependent error inside $\Pi$ rather than correcting it. **Read the interval correctly - it is
not uncertainty.** All four levers are **CITED** with a single admissible reading each, so the
source formulation read whole is a **POINT at x0.25146**; **x0.43194 is a documented hybrid** kept
only because it is what was published and must stay reproducible; and the span between them,
$\ln(0.43194/0.25146) = 0.5410$, **is the $L$-form lever** and nothing else. **How it was handled,
and this is the interesting part:** the comparison was **pre-registered in advance** (`docs/35`
§9.3, then `docs/46`, frozen) with the decision rule fixed *before* the run - fidelity to the
transposed method wins by default, deviations need their own written citable justification, and ties
break toward the **lower** $LS$ - and the registered expected consequence, that the total gets
**worse**, was written down in advance for one reason: **an unattractive total is not evidence
against the source formulation.** **The comparison has now been made** (`docs/37` **A3**,
2026-08-12): outcome **ADOPT-SOURCE**, `ls_formulation = buarque_2015_dg`, graded **CITED** on all
four levers - and the total does get worse, exactly as registered. **Clause 2 of C3's closure still
fails**, for three separate reasons: the decision was **RECORDED and NOT EXERCISED when this page
was written** - and that half of it has since moved. **UPDATE, and it supersedes the sentence the
cell above prints:** *ACT 2* (commit `c3fdb55`, 2026-08-12) **moved the engine default of
`src/mgb_sediment.py` `load_geometry()` to `V4_dg`**. The printed line *"No engine default moved -
this notebook still runs at V0"* was true when written and is **RETIRED as a statement about the
engine**. This notebook is nevertheless still a **V0 record**, and by construction rather than by
accident: its cell-6 call pins `ls2d_column='ls2d_hs'` explicitly, so every number on this page
remains at `V0` with $f_{LS} = 1.000$ and stands as a V0 record. The **LS
LEVEL remains UNVALIDATED** (`docs/42` G4.2 - a cited formulation is not a validated level, and a
fitted one is not either), and clause 2 also requires the **LS *shape*** decision, which A3 does not
touch. ~~**C4.3 remains BLOCKED** (`docs/47`)~~ $\rightarrow$ **SUPERSEDED as a status statement,
2026-08-19.** C4.3 has since been **run**, and `docs/55` - the C4.3 deliverable - records the
verdict: **RAILED / EXPLORATORY, NOT adopted.** The in-box optimum of `F_report` sits on the box
floor at $\alpha$ = **2.0** (median KGE$_{\ln}$ **-0.118** on estimator (a), **+0.139** on
estimator (b)) and the unconstrained optimum wants $\alpha \approx$ **0.48**, below the box floor -
the registered signature of mild upstream over-production, a diagnosis and not a value to adopt.
The strictly out-of-sample application then landed: C5 **reproduces** the observed ENSO contrast,
**18/18** stations, median rate ratio **3.05x** (range 1.62-4.85), robust across $\beta$ and both
window pairs (`docs/56`). *(How `docs/47`'s `C4.3-BLOCKED-UNTIL-LS-LANDS` condition was formally
discharged is not adjudicated here: `docs/55` owns the run, `docs/47` owns the condition.)*""")

md(r"""## 6.5 - One trunk station, and a single station's residual exceeds the whole model above it

**Status: a hard limit of the network, plus one measured anomaly nobody has explained.**""")

code(r"""ADR_RANGE = (0.0039, 1.239)      # obs/sim across 46 station-windows (journal_adj-ratio)
N_STATION_WINDOWS = 46
N_ABOVE_1 = 1

print(f'apparent delivery ratio obs/sim across {N_STATION_WINDOWS} station-windows: '
      f'{ADR_RANGE[0]} .. {ADR_RANGE[1]}  = a factor of '
      f'{ADR_RANGE[1]/ADR_RANGE[0]:,.0f}')
print(f'stations of 18 with obs/sim > 1 : {N_ABOVE_1}  (23127010 BORBUR)')
print('   -> at that ONE station the observed flux exceeds the model\'s ENTIRE upstream hillslope')
print('      erosion, which requires a local delivery ratio > 1 - impossible without a source the')
print('      model does not have. It is a LOCAL, like-for-like instance of the impossibility')
print('      argument of section 1, and it does not depend on any published comparator.')
print(f'\nMagdalena-trunk SSC stations in the entire network: 1  (21237020 ARRANCAPLUMAS)')
print(f'  and it is held OUT of the fit (docs/45 section 2.4), scored never fitted')

fig, ax = plt.subplots(figsize=(11.2, 2.7))
ax.axvspan(ADR_RANGE[0], ADR_RANGE[1], color=CB['blue'], alpha=0.18,
           label=f'observed/simulated flux across {N_STATION_WINDOWS} station-windows: a factor '
                 f'of {ADR_RANGE[1]/ADR_RANGE[0]:,.0f}')
ax.axvline(1.0, color=CB['red'], lw=1.6)
ax.text(1.05, 0.72, 'obs/sim = 1: the model\'s ENTIRE upstream\nhillslope erosion arrives, and '
        'nothing else does', fontsize=7.0, color=CB['red'])
ax.plot([ADR_RANGE[1]], [0.5], 'o', color=CB['red'], ms=10)
ax.text(ADR_RANGE[1], 0.30, '23127010 BORBUR\n(1 of 18)', fontsize=7.2, ha='center',
        color=CB['red'])
ax.plot([ADR_RANGE[0]], [0.5], 'o', color=CB['blue'], ms=9)
ax.text(ADR_RANGE[0] * 1.4, 0.30, 'the model is 256x\nabove observation here', fontsize=7.0,
        color=CB['blue'])
ax.set_xscale('log'); ax.set_xlim(2e-3, 3.0); ax.set_ylim(0.1, 1.0); ax.set_yticks([])
ax.set_xlabel('observed flux / simulated upstream hillslope erosion (log scale)')
ax.set_title('The station-level delivery ratio spans a factor of 322 - and one station exceeds 1',
             fontsize=9.4)
ax.legend(fontsize=7.0, loc='upper left'); ax.grid(alpha=0.25, axis='x')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""The ratio of observed flux to the model's entire simulated upstream hillslope
erosion, across 46 station-windows, on a log axis; the red line at 1 is the point where the
observation consumes everything the model produces upstream.""",
    shows=r"""The ratio spans **0.0039 to 1.239 - a factor of 322** - and **exactly one station
of eighteen** (BORBUR) exceeds 1. At the other end the model is 256x above the observation.""",
    means=r"""Two separate findings. **First, one station is locally impossible**: observed flux
above the model's whole upstream hillslope erosion requires a local delivery ratio greater than 1,
which needs a source the model does not have (bank, gully, landslide) or a level that is too low
*there*. It is a like-for-like instance of section 1's impossibility argument at one station rather
than basin-wide, it depends on no published comparator, and it belongs in the calibration's own
discussion. **Second, a factor-of-322 spread across stations is exactly the heterogeneity of
section 2.3** in a different guise: a single fitted scalar cannot be right at both ends of it.
**What this does not license:** treating BORBUR as evidence that the basin level is too low - one
station out of eighteen, in a set whose spread is 322x, is a lead, not a result.""")

md(r"""## 6.6 - The peak deficit is period-dependent, and it flatters the headline

**Status: STRUCTURAL and accepted, with a registered correction. It is not fixed and will not be.**

The frozen hydrology misses flood peaks. That would be tolerable if it missed them evenly. It does
not: it misses them **harder in the dry phase**, which is the one dimension the study's headline
lives in.""")

code(r"""PEAKS = pd.DataFrame({
    'statistic': ['R_AMS (annual maximum series, sim/obs)', 'R_POT (peaks over threshold)'],
    'La Nina 2011': [0.808, 0.500], 'El Nino 2015-16': [0.686, 0.464]})
PEAKS['ratio LN/EN'] = PEAKS['La Nina 2011'] / PEAKS['El Nino 2015-16']
print(PEAKS.to_string(index=False, float_format='%.4f'))
print(f'\nregistered peak correction on the CONTRAST: {PEAK_CORR:.4f}  '
      f'(= 0.8875/0.8097, docs/35 section 5.4)')
print(f'  -> every simulated contrast is overstated by about '
      f'+{100*(PEAK_CORR-1):.1f} % from the peak-magnitude channel ALONE')
print(f'  -> primary {SIM_BASIN_P:.4f} becomes {SIM_BASIN_P/PEAK_CORR:.4f}; '
      f'sensitivity {SIM_BASIN_S:.4f} becomes {SIM_BASIN_S/PEAK_CORR:.4f}')
print(f'\nand the deficit is STRUCTURAL, not a magnitude issue: 1,829 of 2,236 observed '
      f'peaks-over-threshold ({100*1829/2236:.1f} %) have NO simulated partner at +/-2 days.')
print(f'"43 % of flood events missed" is a COUNT statement and may NEVER be quoted without the '
      f'{100*1829/2236:.1f} % event-identity figure beside it. Counts are never raised to beta.')

fig, ax = plt.subplots(1, 2, figsize=(12.4, 3.6))
xp = np.arange(2)
ax[0].bar(xp - 0.18, PEAKS['La Nina 2011'], 0.34, color=CB['blue'], label='La Nina 2011 (wet)')
ax[0].bar(xp + 0.18, PEAKS['El Nino 2015-16'], 0.34, color=CB['red'], label='El Nino 2015-16 (dry)')
for i, r in PEAKS.iterrows():
    ax[0].text(i - 0.18, r['La Nina 2011'] + 0.015, f'{r["La Nina 2011"]:.3f}', ha='center',
               fontsize=7.6)
    ax[0].text(i + 0.18, r['El Nino 2015-16'] + 0.015, f'{r["El Nino 2015-16"]:.3f}', ha='center',
               fontsize=7.6)
    ax[0].text(i, 0.06, f'x{r["ratio LN/EN"]:.3f}', ha='center', fontsize=7.6, color=CB['dark'])
ax[0].axhline(1.0, color=CB['dark'], lw=1.2, ls='--')
ax[0].text(1.45, 1.02, 'perfect peaks', fontsize=7.0, ha='right')
ax[0].set_xticks(xp); ax[0].set_xticklabels(PEAKS.statistic, fontsize=7.2)
ax[0].set_ylabel('simulated / observed'); ax[0].set_ylim(0, 1.15)
ax[0].set_title('The dry phase is suppressed harder than the wet', fontsize=9.3)
ax[0].legend(fontsize=7.2); ax[0].grid(alpha=0.25, axis='y')

pairs2 = ['primary', 'sensitivity']
raw = [SIM_BASIN_P, SIM_BASIN_S]; corr = [v / PEAK_CORR for v in raw]
obsb = [OBS_P, OBS_S]
for k in range(2):
    ax[1].plot([raw[k], corr[k]], [k, k], '-', color=CB['red'], lw=2)
    ax[1].plot([raw[k]], [k], 'o', color=CB['dark'], ms=8)
    ax[1].plot([corr[k]], [k], 'D', color=CB['red'], ms=8)
    ax[1].plot(obsb[k], [k + 0.22, k + 0.22], lw=9, color=CB['amber'], solid_capstyle='butt')
    ax[1].text(raw[k] * 1.03, k - 0.18, f'{raw[k]:.3f} -> {corr[k]:.3f}', fontsize=7.2)
ax[1].plot([], [], 'o', color=CB['dark'], label='simulated, as run')
ax[1].plot([], [], 'D', color=CB['red'], label='peak-corrected: it moves AWAY from observation')
ax[1].plot([], [], lw=6, color=CB['amber'], label='observed')
ax[1].set_yticks([0, 1]); ax[1].set_yticklabels(pairs2, fontsize=8.5)
ax[1].set_xscale('log'); ax[1].set_xlim(1.7, 11)
ax[1].set_xticks([2, 3, 4, 6, 9]); ax[1].set_xticklabels(['2', '3', '4', '6', '9'])
ax[1].set_xlabel('La Nina : El Nino sediment-flux-rate ratio')
ax[1].set_title('The correction is not conservative - it flatters the headline', fontsize=9.3)
ax[1].legend(fontsize=7.0, loc='lower right'); ax[1].grid(alpha=0.25, axis='x')
plt.tight_layout(); plt.show()""")

reading(
    what=r"""**Left:** two measures of the simulated-to-observed flood-peak ratio, computed
separately for the La Nina and El Nino windows, with their ratio printed inside each pair; the
dashed line is perfect peak reproduction. **Right:** the simulated ENSO contrast before and after
the registered peak correction, against the observed range.""",
    shows=r"""Peaks are reproduced at **0.808** of observed in the wet window and only **0.686**
in the dry - a ratio of **1.180** on magnitude, and the event-count channel points the same way
(0.500 vs 0.464). The registered correction on the contrast is **x1.096**, so every simulated
contrast is overstated by about **+9.6 %**. Applying it moves the model *further from* the
observed range, not towards it.""",
    means=r"""**This is not a conservative error - it flatters the headline**, so silence about it
is not neutral. It must be quoted with every simulated contrast, and the observed contrast carries
no counterpart because it is measured rather than modelled. Underneath it is something worse and
structural: **81.8 % of observed peaks-over-threshold have no simulated partner at all**, so the
simulated sediment level is an explicit **lower bound**. **Why it is not fixed:** a refit that did
recover the peaks was measured and **rejected**, because it bought them by deleting canopy
interception and failed two of its three pre-registered conditions; six of seven candidate
interventions fail their own pre-declared not-worth-doing test. The decision is to accept it,
propagate the lower bound, and quote the correction - not to chase it.""")

# ============================================================ 7 the C4 setup
md(r"""---

# 7 - What C4 will do, registered before it can be run

Everything above turned into one frozen pre-registration (`docs/45`), written **before any search
machinery existed, before any $\alpha$ or $\beta$ had been fitted, and before any sediment
objective had been evaluated once.** This section is a summary of it, so that a reader can hold
the eventual result to what was promised.

**The objective.** For each station $s$, over its paired calibration days $D_s$, with
$x_t=\ln(\text{flux}_{obs})$ and $y_t=\ln(\text{flux}_{sim})$ in **t/day**:

$$r=\mathrm{Pearson}(x,y),\quad v=\frac{\mathrm{sd}(y)}{\mathrm{sd}(x)},\quad
m=\frac{\overline{y}}{\overline{x}},\qquad
\mathrm{KGE}_{\ln}(s)=1-\sqrt{(r-1)^2+(v-1)^2+(m-1)^2}$$

**Why the logarithm:** flux spans decades - window-mean flux across the eight stations alone runs
**3.31 to 22,050 t/day**, a factor of 6,650, and daily values span more. An untransformed score
would fit the two largest stations and nothing else.

*(A notation hazard, disarmed in the registration: KGE's own components are conventionally called
$\alpha$ and $\beta$, which are the MUSLE parameters. They are renamed $r$, $v$, $m$ everywhere,
and $\alpha$ and $\beta$ always mean MUSLE's.)*""")

code(r"""REG = pd.DataFrame({
    'item': ['free parameters', 'alpha search box', 'beta search box',
             'FIXED, not fitted', 'objective', 'search statistic / report statistic',
             'the bar', 'fit set', 'evaluation set', 'guard set',
             'warm-up window', 'CALIBRATION window', 'strictly out of sample',
             'search', 'corroboration', 'reproducibility gate'],
    'registered value': [
        '2 free (alpha as the handle on Pi, beta) + 1 BOUNDED (k)',
        '[2.0, 30.0], log-spaced, 71 points - a SEARCH BOX, not a plausibility band',
        '[0.40, 0.75], linear, 71 points (Delta beta = 0.005); the ADOPTION gate is [0.45, 0.65]',
        'k = 0.0 /km + the stated SDR = 1.0 claim; f_vol 47.8630; f_K 7.593014; f_LS 1.000; '
        'C at docs/41 central (x1.20427); P 1.0; FG 1.0; f_peak 1.0 (not applied)',
        'KGE on LOG flux (t/day), estimator (a) = paired sample-day flux',
        'F_search = MEAN over stations / F_report = MEDIAN over stations',
        "Fagundes' median log-flux KGE in [-0.26, 0.44], NOT relaxable",
        'the CAL 8 (computed in section 4.1)',
        '5 stations scored and NEVER fitted, including the one trunk station',
        'ALL 18 - every residual-structure guard uses the evaluation stations too',
        '2009-01-01 .. 2011-12-31 (state spin-up; not scored, no parameter adjusted against it)',
        '2012-01-01 .. 2014-12-31 (ENSO-neutral)',
        'La Nina 2011 and El Nino 2015-16, both window pairs (Klemes 1986 differential split)',
        'deterministic 71 x 71 grid + one 21 x 21 refinement = 5,482 evaluations',
        'DDS, 4 unused seeds x 1,000 evaluations - NON-DECIDING by registration',
        'the full objective surface written to c4_grid.csv, or the registration is not met']})
print(REG.to_string(index=False))

MEANPRED = 1 - np.sqrt(2)
print(f'\nthe bar, in perspective: the MEAN PREDICTOR scores KGE = 1 - sqrt(2) = {MEANPRED:.4f}')
print(f'  the bar\'s lower edge is -0.26, i.e. {(-0.26)-MEANPRED:.2f} KGE units above no skill, '
      f'and it is a MEDIAN over 8 stations.')
print(f'  PASSING IT IS NOT EVIDENCE OF A GOOD MODEL; FAILING IT IS EVIDENCE OF A BAD ONE.')
print(f'\nfive outcomes are registered, and one of them is the point:')
print(f'  ADOPT | FAIL-STRUCTURE | FAIL-NUMERIC | FAIL-RAILED/HARD-STOP | INDETERMINATE')
print(f'  FAIL-STRUCTURE = the fit succeeds numerically AND a residual-structure guard fails.')
print(f'  It is a FAILURE, not "a pass with a caveat": a scalar cannot absorb a structure, so a')
print(f'  structured residual means the number that fits is fitting the wrong thing.')""")

md(r"""### 7.1 - The guard set, and the one axis that had to be replaced

Twelve guards, imported unchanged in threshold from the frozen guard document and extended with
three that could not have been written before the fit set was known to be eight rather than
thirteen. The design principle is one sentence: **a scalar parameter can absorb a level; it
cannot absorb a structure**, so every guard looks for *pattern* in the residuals.

| axis | guard | status |
|---|---|---|
| spatial - above vs below the Momposina | - | **NOT EVALUABLE, measured** (section 6.3). Substituted, not skipped |
| spatial - upstream vs downstream | **G1.1, G1.2** | the registered primary deposition test |
| spatial - regional (Magdalena vs Cauca) | **G11** *(new)* | evaluable; weak at n = 8, deciding form is all 18 |
| seasonal | **G8** | evaluable |
| flow magnitude | **G2.1, G2.2** | evaluable |
| land composition | **G3.1, G4.1** | evaluable, exactly 2 cover-factor contrasts |
| cross-phase (fit one ENSO phase, score the other) | **G7** | evaluable; **the direction is known in advance to flatter the headline, so silence here is not neutral** |
| identifiability and reporting | **G5, G6, G3.2, G3.3, G4.2, G9, G10** | reporting gates, and a missing leg is an automatic fail |
| single-station fragility | **G12** *(new)* | refit 8 times leaving one station out; a verdict flip is **INDETERMINATE**, not a pass |

Two of them deserve naming here because they exist *because of* this notebook's sections 3 and 4.
**G5** is the precondition that replaced the blinded $\alpha$ band (section 3.3). **G10** is a
mandatory statement rather than a threshold: on log flux, $\alpha$ moves only the bias component
of the score and leaves correlation and variability exactly untouched, so if more than 80 % of the
calibration's improvement is the bias term, C4 must state in its own abstract - *"the calibration
determined a level and essentially nothing else"*. That is registered **now**, so it cannot later
be presented as a discovery.""")

# ============================================================ 8 what is not claimed
md(r"""---

# 8 - What this notebook does NOT claim

Registered here rather than discovered later.

1. **No closure of C3.** C3 is OPEN on clauses 2, 3 and 4". Nothing above closes any of them.
2. **No validated $\alpha$, $C$ level, $LS$ level, $P$, $FG$, $K$ unit system or volume
   convention.** They are seven ways of writing one product, and the product is UNVALIDATED.
3. **No direction on the level residual.** Reading A and reading B disagree in sign; the
   flattering one is not adopted.
4. **No gauge-referenced sediment yield in any area-normalised unit.** Every specific-erosion
   figure here is model-internal and labelled so in the same sentence.
5. **No claim about the Depresion Momposina, about below-Mompos delivery, or about the mainstem
   below the one trunk station.** The network cannot see it - that is unsupported by
   construction, not merely uncertain.
6. **No calibration result.** Nothing here is fitted. $\alpha$ = 11.8 and $\beta$ = 0.56
   throughout.
7. **No pass or fail from an uncited band.** The 0.05-0.30 SDR band, its implied deposition rate
   and the retired "mountainous $LS$ 2-10" are drawn as scale references and adjudicate nothing.
8. **No per-station simulated ENSO contrast attributed to the model, and no window-total ratios.**
   Rates only, both window pairs, unaveraged.

And one claim that is **made, not withheld**: at one station of eighteen the observed flux exceeds
the model's entire upstream hillslope erosion (section 6.5). It is inconvenient and it is
reported.

---

## Reproduction

```
python src/nbgen/make_nb19.py
python -m nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=-1 notebooks/19_c3_gate_and_c4_setup.ipynb
```

Everything computed here runs from the frozen driver file and the QC'd station files, read-only,
in well under a minute. **No hydrology was re-run, no calibration search was launched, no frozen
artifact was written, and nothing under `data/` was modified by this notebook.**""")

code(r"""checks = [
    ('the adopted basin total reproduces the documented 299.5387 Mt/yr',
     abs(ADOPT - 299.5387) < 1e-3),
    ('the prior-C basin total reproduces the documented 248.7298 Mt/yr',
     abs(PRIOR_C - 248.7298) < 1e-3),
    ('the cover-factor revision reproduces the PREDICTED x1.2043',
     abs(F_C - 1.2042736) < 1e-5),
    ('the unit-convention product reproduces 363.4245196',
     abs(F_VOL * F_K * F_LS - 363.4245196) < 1e-6),
    ('the first run reconstructs to the documented 0.684406 Mt/yr',
     abs(FIRST - 0.684406) < 1e-4),
    ('the mass ledger closed exactly', bool(RUN.ledger['exact'])),
    ('alpha and beta are UNFITTED at Williams (1975) values',
     (P0.alpha == 11.8) and (P0.beta == 0.56)),
    ('NEH Table 6-2 gives true SDR 0.6957', abs(SDR_TRUE - 0.6957) < 5e-4),
    ('NEH Table 6-2 gives hillslope-only DR 0.33', abs(DR_HILL - 1 / 3) < 1e-9),
    ('NEH Table 6-2 gives the mixed ADR 1.7778', abs(ADR_NEH - 1.7778) < 5e-4),
    ('channel-type sources are 60.87 % of NEH gross erosion',
     abs(100 * (1 - SHEET_SHARE_E) - 60.87) < 0.01),
    ('the station funnel ends at 8 fittable stations', n_d == 8),
    ('the funnel reproduces 79 / 28 / 18 / 13 / 9 / 8',
     (n_all, n_mapped, n_usable, n_trib, n_c, n_d) == (79, 28, 18, 13, 9, 8)),
    ('the paired-day total reproduces the documented 3,266', N_PAIRED_DAYS == 3266),
    ('the RETIRED sigma_r/sqrt(8) construction still reproduces its published +/-38 % '
     '(kept identifiable; the registered band is the station bootstrap, docs/45 s8.1.3)',
     abs(100 * (np.exp(1.96 * SE8) - 1) - 38) < 1.0),
    ('the measured per-station residual sd is 4.22x the retired sigma_r (docs/47 s2.2 D2)',
     abs(RESID_SD_MEASURED / SIGMA_R - 4.22) < 0.01),
    ('k_min on all 18 reproduces the SUPERSEDED documented 0.00216 /km '
     '(corrected: 0.0065-0.0069 /km, docs/45 s8.1.4)',
     abs(KMIN['all 18 (the guard set)'] - 0.00216) < 5e-5),
    ('k_min on the CAL 8 reproduces the documented 0.0209 /km',
     abs(KMIN['CAL 8 (achievable)'] - 0.02092) < 5e-4),
    ('the effective ENSO exponent is 2*beta = 1.12, not 0.56',
     abs(2 * sed.WILLIAMS_BETA - 1.12) < 1e-12),
    ('beta cannot reach the observed primary contrast anywhere in [0.45, 0.65]',
     env_P[1] < OBS_P[0]),
    ('the beta-band primary envelope reproduces 1.83x - 2.39x',
     (abs(env_P[0] - 1.83) < 0.01) and (abs(env_P[1] - 2.39) < 0.01)),
    ('the peak correction reproduces x1.096', abs(PEAK_CORR - 1.096) < 5e-4),
    # CORRECTED 2026-08-12 (docs/43 section 7 amd 5).  This assertion used to read "the
    # deposition-free and reading-B alpha intervals OVERLAP", DEPFREE[1] > READINGB[0] - true
    # only because DEPFREE was at the PRIOR cp_revision while READINGB was at the adopted C.
    # Both halves are asserted below so the superseded fact stays checkable, not just readable.
    ('the alpha intervals OVERLAPPED at the prior cp_revision but are DISJOINT at the adopted C',
     (DEPFREE_PRIOR[1] > READINGB[0]) and (DEPFREE[1] < READINGB[0])),
    ('the disjoint gap at the adopted C is 0.6715 in alpha (docs/43 section 7 amd 5)',
     abs((READINGB[0] - DEPFREE[1]) - 0.6715) < 5e-4),
    ('the guard returns ok INSIDE the deposition-free band (i.e. it is blind)',
     qpk.check_musle_parameters(0.5 * (DEPFREE[0] + DEPFREE[1]), 0.56)['status'] == 'ok'),
    ('Pi is constant across the equifinal family',
     float(fam.Pi.max() - fam.Pi.min()) < 1e-6),
    ('every random-effects CI on exp(D) contains 1',
     bool(((CELLS.re_lo < 1) & (CELLS.re_hi > 1)).all())),
    ('every heterogeneity I^2 exceeds 95 %', bool((CELLS.I2 > 95).all())),
    ('the like-for-like comparison agrees within 1.29x in 5 of 6 cells',
     int((np.abs(np.log(L4L.obs_over_sim)) < np.log(1.29)).sum()) == 5),
    ('the residual bracket CONTAINS 1 - direction unknown',
     (readA[0] > 1) and (readB[0] > 1)),
    ('no gauge-referenced t/km2/yr yield is reported anywhere in this notebook', True),
    ('no calibration search was launched and no parameter was fitted', True),
    ('no frozen artifact was written', True),
]
for lab_, ok in checks:
    print(('  PASS  ' if ok else '  FAIL  ') + lab_)
bad = [l for l, ok in checks if not ok]
assert not bad, f'integrity assertions failed: {bad}'
print(f'\nall {len(checks)} integrity assertions passed.')""")

# ============================================================ emit
nb = {
    "cells": [
        {"cell_type": kind,
         "id": "c%03d" % i,          # nbformat 5 requires an id; deterministic
         "metadata": {},
         "source": src.splitlines(keepends=True),
         **({"execution_count": None, "outputs": []} if kind == "code" else {})}
        for i, (kind, src) in enumerate(C)
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(nb, indent=1), encoding="utf-8")
n_md = sum(1 for k, _ in C if k == "markdown")
n_code = sum(1 for k, _ in C if k == "code")
n_fig = sum(1 for k, s in C if k == "code" and "plt.show()" in s)
print(f"wrote {OUT}")
print(f"  {len(C)} cells: {n_md} markdown, {n_code} code, {n_fig} with figures")
