# journal — nbc1-sweep (mechanical kill-list sweep)

Agent: `nbc1-sweep`. Phase 1 = T1 audit, **READ-ONLY**. The only file I write is this journal.

## What I was asked

Run a **deterministic regex sweep** for every kill-list row plus a list of extra patterns, over three
surfaces:

- (a) notebook text extracts `…/scratchpad/nbtext/*.txt` (source AND text outputs, 0-based cell idx)
- (b) generators `src/nbgen/make_nb1*.py`
- (c) `docs/*.md` — context only, to distinguish a retired number from one a doc still publishes

Plus one thing nobody else is doing: **generator-vs-notebook divergence** — a pattern present in a
committed notebook but ABSENT from its generator means the notebook was hand-edited or is stale
relative to its generator.

Deliverable: structured object with `cells_swept`, `files_swept`, per-pattern counts + locations +
a sampled LIVE/STRUCK/FALSE-POSITIVE note, and `generator_notebook_divergences`.

Binding rules I am operating under: measure before asserting; verify from executed output not exit
code; never report a count I did not measure; every finding needs a cell index and a verbatim quote.

---

## Step 1 — baseline counts (MEASURED)

`grep -c '^\[CELL '` over each extract:

```
01_dem.txt 17          11_rainfall_pet_forcing.txt 24
02_urh.txt 14          12_model_input_assembly.txt 36
03_hydrology.txt 10    13_baseline_run.txt 50
04_real_dem_eda.txt 10 14_calibration.txt 40
05_landcover…txt 13    15_ssc_quality_gate.txt 85
06_data_inventory 54   16_observed_enso_contrast.txt 100
07_preprocessing 21    17_runoff_signatures.txt 109
08_urh.txt 12          18_musle_construction.txt 85
09_soil_parameters 15  19_c3_gate_and_c4_setup.txt 82
10_rainfall_dataset 12
```

**TOTAL cells_swept = 789.** This agrees cell-for-cell with `manifest.csv` (independent count),
and manifest reports `code_unexecuted=0` and `cells_with_error=0` for all 19 notebooks.

Generators present: `make_nb10.py … make_nb19.py` = **10** files. Note mtimes: nb10–nb17 and nb18
are 2026-08-12, **make_nb19.py is 2026-08-13 03:43** — the only generator touched after the
engine-default LS move. Consistent with the orchestrator's note that `8c139f9` touched nb19.

---

