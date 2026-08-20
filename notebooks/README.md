# Notebooks — the investigation, in order

**Nineteen notebooks, 789 cells, all executed, no error outputs.** Read them as one argument rather
than as a pile of exercises: the repository's whole narrative arc is laid out in
[`../README.md`](../README.md) §3, and each notebook below says what it inherits and what it hands
on. Rewritten 2026-08-19; every notebook was scored and corrected in that pass
(`../docs/agents/journal_reorg-notebooks.md` carries the scoreboard).

> ## ⚠ Two rules before you edit anything here
>
> **1. Notebooks 10–19 are GENERATED** by `../src/nbgen/make_nb10.py … make_nb19.py`.
> **Never hand-edit one of them** — the next regeneration destroys the edit silently. Edit the
> **generator**, rerun it, execute the notebook, verify from the executed output, then re-confirm
> that every generator still reproduces its notebook source-identically. As of 2026-08-19 all ten
> do, and each cell carries a deterministic `id` so regeneration is byte-stable.
>
> **2. Re-execution is not free.** nb12 and nb13 register a 7,200 s timeout, **nb14 28,800 s (8 h)**,
> and nb15–19 are unbounded. A part-way failure leaves a notebook *less* executed than you found it.
> And **verify from the executed output, never from the exit code**: `nbconvert` has been observed
> in this project to exit 0 on a notebook that raised.

Execute headless (`jupyter` is **not** on PATH):

```
python3.10 -m nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=-1 notebooks/<nb>.ipynb
```

---

## Part I — the didactic derivations (01–03, hand-written)

Small, self-contained derivations on a 6×6 toy DEM you can check by hand. They explain *what the
QGIS plugins do*; they do not replace them.

| notebook | what it establishes |
|---|---|
| **`01_dem.ipynb`** | DEM → minibacias by hand: NODATA handling, pit filling (Planchon–Darboux), D8 flow direction, flow accumulation, stream definition, segmentation, watershed delineation. It is also **the exact place drainage area first enters the project as a trustworthy quantity** — which `../docs/23` §13.2 later shows it is not, and which is why the yield embargo exists. |
| **`02_urh.ipynb`** | The soil × land-cover crossing, and **the only place in the repository where the Fréchet-bounds argument is made**: why marginal totals can never substitute for a real spatial overlay, and therefore why the production URH had to be built from rasters. |
| **`03_hydrology.ipynb`** | The project's own derivation of the MGB-SA daily water balance — saturation-excess runoff on a variable contributing area, linear-reservoir recession, a full one-URH simulation, and routing. **`../src/mgb_hydrology.py` implements this notebook section by section, and pytest pins the agreement to 1e-12.** |

## Part II — the real inputs (04–09, hand-written)

Phase A on the real basin. These are the oldest text in the project and the place stale claims hid.

| notebook | what it establishes |
|---|---|
| **`04_real_dem_eda.ipynb`** | **A recorded negative result.** With one diagnostic number — maximum flow accumulation 1,341 cells ≈ 98 km² where a real Magdalena would fill the grid — it proves a stream threshold *cannot* be chosen on the lower-Magdalena box, because the upstream basin is off-map and the delta is flat. That is what forced the whole-basin DEM. |
| **`05_landcover_soils_reclass.ipynb`** | The crossing **method**: WorldCover reduced to 8 hydrological classes, IGAC landscapes grouped in relief order, both snapped to one grid and crossed into the real URH map. |
| **`06_data_inventory.ipynb`** | The entry inventory: what data exists, what is missing from each dataset, and what the project intends to do about every gap — and where **the ENSO year choice is validated model-free from the records themselves** rather than assumed from the literature. |
| **`07_preprocessing_minibacias.ipynb`** | Beat 1 of *"inputs are not innocent"*: the corrected COP90 DEM becomes the model's spatial units — **8,672 minibacias**, the D8 routing topology, and the gauge→minibacia index every later number is keyed on. Every discharge gauge is burned in as a pour point so it lands on its own minibacia. |
| **`08_urh.ipynb`** | Beat 2: WorldCover × IGAC texture families on nb07's grid → the **24-URH** area-fraction table that the water balance *and* the sediment engine both read. |
| **`09_soil_parameters.ipynb`** | Beat 3, and the close of Part II: IGAC free-text soil descriptions become the two parameters the model needs — `Wm` (storage, a calibratable prior) and `K` (MUSLE erodibility, **pinned, not fitted**). |

## Part III — forcing and the water model (10–14, generated)

| notebook | what it establishes |
|---|---|
| **`10_rainfall_dataset_comparison.ipynb`** | Which rainfall product forces the model — and where the **zero-suppression defect** was found: dry days absent from the record rather than recorded as zero, invisible to any value screen, caught by neighbour-ratio tests. Finding it **invalidated this notebook's own earlier verdict**. The CHIRPS-vs-gauges question is decided here, and later overturned by measurement (`../docs/18` §15.5, `../docs/58`). |
| **`11_rainfall_pet_forcing.ipynb`** | nb10's verdict becomes the two fields MGB-SA consumes: per-minibacia daily rainfall (deterministic IDW, order-invariance asserted in the notebook) and FAO-56 Penman–Monteith PET. **This is where "v2 forcing" is written — and v2 means GAUGE-ONLY**: the zero-suppression repair plus deterministic IDW. A CHIRPS-merged v3 **does not exist**. |
| **`12_model_input_assembly.ipynb`** | The notebook that refuses to let a join, a date index or a gauge mapping fail silently — 11 analytic smoke tests, every headline computed two independent ways — and writes one manifest saying exactly what the water balance may consume. |
| **`13_baseline_run.ipynb`** | **The control experiment**: the last notebook before anything is fitted. It proves the engine conserves mass on the real basin, fixes a DATA/PRIOR parameter set *before any gauge is consulted*, registers a prediction, and confronts it with the result. Three mutually incompatible initial states converge to within 0.179 % of mean flow — which is what makes every later number something other than curve-fitting. |
| **`14_calibration.ipynb`** | Phase B's decisive experiment: the refit under the revised objective across two pre-registered forcing cells. **H2 − H1 settles the question** — the zero-suppression repair moved *volume* and left *correlation* untouched, so the two are independent, and the ceiling is not a volume problem. |

## Part IV — sediment (15–19, generated)

| notebook | what it establishes |
|---|---|
| **`15_ssc_quality_gate.ipynb`** | **The hinge of the investigation.** It freezes the water model at **H2E** behind a bit-exact reproduction gate, so no sediment number can later move because the hydrology shifted underneath it — then decides which of the **79** SSC stations may ever be used (**18 usable**). It is also the notebook that *declares* the t/km²/yr embargo and enforces it. |
| **`16_observed_enso_contrast.ipynb`** | The **observational anchor**: the model-free, pre-registered ENSO sediment contrast measured from IDEAM records alone — two estimators, two window pairs, **unanimous direction (22/22)**, magnitude quoted only as a range. It exists so the modelled contrast has a target that owes the model nothing. |
| **`17_runoff_signatures.ipynb`** | The driver-validation gate between the water model and the sediment model: are the only two hydrological quantities MUSLE actually reads — surface runoff and flood peak — right? Answer: the first is not refutable with the available test, and **the second is refuted** (H-PEAK). Pre-registration earning its keep. |
| **`18_musle_construction.ipynb`** | The C3 construction record: frozen surface runoff → a MUSLE field over 8,672 minibacias × 3,652 days. It documents a **×363.4245196 unit error and its closure to twelve significant figures**, and prices every convention. Basin gross hillslope erosion **299.5387 Mt/yr** at the adopted `cp_revision` (**248.7298** at the prior one) — a V0 record, pinned explicitly. |
| **`19_c3_gate_and_c4_setup.ipynb`** | **The decision record.** Where the C3 closure gate was *dismantled* rather than passed or failed; where α was established as a fitted coefficient of adjustment rather than a physical constant; where the C4 fit was measured to be feasible only as a small one (2 free + 1 bounded, on 8 stations); and where 33 integrity assertions run and pass. |

## What comes after nb19 — and is not here yet

The corpus ends where the *answers* begin. `docs/55` (the C4.3 verdict: **RAILED / EXPLORATORY, not
adopted**) and `docs/56` (**the headline: 18/18, median 3.05×**) have **no notebook**. Two are worth
building — *nb20: the C4.3 verdict, and why a pre-computable search is not a test*, and *nb21: C5,
and why a contrast survives a non-identifiable level*. **They must be written as generators**
(`make_nb20.py`, `make_nb21.py`), matching the existing generators' structure, voice and
`reading(what=…, shows=…, means=…)` idiom. Recorded as an open item in
`../docs/agents/journal_reorg-notebooks.md` §5.

## Requirements

`numpy`, `pandas`, `matplotlib`, `rasterio`, `scipy` and the project's own `src/` modules — see
[`../requirements.txt`](../requirements.txt). Notebooks 04–19 read real data from `../data/`, which
is gitignored and rebuilt by the chain in [`../docs/20_reproduction_guide.md`](../docs/20_reproduction_guide.md) §3.
