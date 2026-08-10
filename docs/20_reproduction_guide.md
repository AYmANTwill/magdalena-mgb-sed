# 20 — Reproduction guide: rebuilding everything this repo does not version

Written 2026-08-03 (the docs closeout). Audience: someone with a fresh clone, no
conversation history, and a working internet connection. Everything here was written from
artifacts on disk, not from memory. The companion document is
[doc 21](21_project_state_and_handoff.md) — *what* the project currently claims; this one
is *how* to rebuild the evidence.

---

## 1 — Environment

- **Python 3.10.** On the project box the interpreter is `python3.10` (`python` may not
  resolve), and running processes appear as **`python3.10.exe`** in `tasklist` —
  `tasklist /FI "IMAGENAME eq python.exe"` reports *nothing* while four searches are
  running. This trap caused three duplicate launch batches once (doc 26 §6).
- **Pinned dependencies:** `requirements.txt` (pip, `python3.10 -m pip freeze` of the
  project box, 2026-08-03) or `environment.yml` (conda-forge mirror of the same pins;
  `conda env create -f environment.yml`). Only packages the pipeline actually imports.
- **QGIS 3.44 LTR** + plugins IPH-HydroTools, MGB (Dec 2025), MGB-SED — installed
  separately, not via pip. MGB-SA proper runs as a QGIS plugin; the Python water balance
  (`src/mgb_hydrology.py`, derived in `notebooks/03_hydrology.ipynb`) is the diagnostic
  engine used for calibration.
- **Secrets:** `cds_keys.txt` / `.cdsapirc` are gitignored and never committed. You need
  your own CDS (Copernicus) credentials for the ERA5 downloads.
- **Jupyter is not on PATH.** Execute notebooks headless:
  `python -m nbconvert --to notebook --execute --inplace notebooks/<nb>.ipynb`
  (add `--ExecutePreprocessor.timeout=-1` for nb13/nb14).
- **Windows Defender makes small-buffer Python I/O ~30× slow.** Use 7-Zip
  (`C:\Program Files\7-Zip\7z.exe`) for archives and ≥4 MB read chunks for big files.

## 2 — What is versioned, what is not

Versioned: `src/`, `scripts/`, `notebooks/` (with executed outputs), `docs/`, the two
dependency manifests. **Gitignored and regenerable** (see `.gitignore`):

| gitignored | how to rebuild |
|---|---|
| `data/raw/*`, `data/processed/*` | the regeneration chain in §3 (sources in `data/README.md`) |
| `data_Final/`, `data_Final.zip` | `src/build_data_final.py` (itself gitignored packaging, ~14 GB) |
| `delivery/`, `*.pdf`, `notebooks/*.html` | packaging scripts; not project source |
| `figures/deck/` | `python scripts/extract_notebook_figures.py` (every PNG output of `notebooks/*.ipynb` → `figures/deck/<nb>_c<cell>_<n>.png`) then `python scripts/make_deck_charts.py` (the four `gen_*.png` charts from `data/processed/sim_calibrated_v2/*.csv`) |
| `*.pptx` | `python scripts/build_deck.py` → `MGB-SED_Magdalena_FIGURES.pptx`. Needs `figures/deck/` populated first. The `yb_*.png` figures come from the team's second-implementation repo — the one input not rebuildable from this repo alone |
| `sim_calibrated_v2/h2e_drivers.npz` (546 MB) | `python3.10 src/build_h2e_drivers.py` — the frozen per-minibacia sediment drivers of the adopted H2E run (docs/31 C0.5). Needs `_calib_cache/dds_H2E_20260901.npz` and `model_inputs_v2/`; regenerates its own forcing cache if absent |
| `_calib_cache/H1_*.npy`, `H2_*.npy` | `python3.10 -c "import sys; sys.path.insert(0,'src'); import calib_v2 as c; c.ensure_cache('H2E')"` — the memory-mapped forcing the cells read; deterministic, rebuilt from the bundle |
| `cds_keys.txt`, `.cdsapirc` | your own credentials |

Rule of thumb from the audits: **verify from on-disk artifacts and executed outputs, never
from an exit code or a file count** — a 43.7 MB ERA5 file was internally corrupt and passed
both a name count and a size check (doc 18 trap 20).

## 3 — The full regeneration chain

Run in this order. Each step's own header comments state its inputs and outputs.

```
# A. Rain gauges (DHIME)
python src/organize_precip_regions.py           # consolidate raw DHIME downloads -> 98 organised CSVs
python src/build_precip_gauges.py               # QC v1: value screens only
python src/repair_precip_zero_suppression.py    # QC v2: REQUIRED (docs/16 s4.1) -> *_qc files
python src/repair_precip_selectivity.py         # QC v3: selectivity detector; 153 stations,
                                                #   240,158 inferred-dry days (docs/18 s10)

# B. Discharge gauges
python src/build_discharge_gauges.py            # consolidate + clean discharge

# C. Gridded forcing
python src/download_chirps.py [years]           # CHIRPS daily (file is a BOUNDING BOX,
                                                #   not a basin clip - doc 18 trap 8)
python src/download_era5.py                     # ERA5-Land, basin box (CDS credentials)
python src/download_era5_strip.py               # the east strip
python src/mosaic_era5.py                       # -> era5land_ext_*.nc

# D. Forcing fields and model inputs (generated notebooks)
python src/nbgen/make_nb10.py                   # nb10: rainfall dataset comparison
python -m nbconvert --to notebook --execute --inplace notebooks/10_rainfall_dataset_comparison.ipynb
python src/nbgen/make_nb11.py                   # nb11: IDW rainfall + PET forcing
python -m nbconvert --to notebook --execute --inplace notebooks/11_rainfall_pet_forcing.ipynb
python -m nbconvert --to notebook --execute --inplace notebooks/12_model_input_assembly.ipynb
                                                # -> data/processed/model_inputs_v2/

# E. Simulation and calibration
python -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 notebooks/13_baseline_run.ipynb
                                                # -> sim_baseline_v2/ (2008 warm-up, 2009-2018 scored)
python -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 notebooks/14_calibration.ipynb
                                                # -> sim_calibrated_v2/ (reads finished DDS
                                                #   checkpoints; see s5 for the workers)

# F. Phase B closeout: the adopted H2E configuration, reported and frozen (docs/31 C0)
python3.10 src/report_h2e.py                    # C0.1-C0.4: reproduction gate, then
                                                #   parameters_H2E.csv, q_gauge_H2E.npz,
                                                #   report_H2E.json, +12 metrics_fleet rows
python3.10 src/build_h2e_drivers.py             # C0.5: -> sim_calibrated_v2/h2e_drivers.npz
                                                #   (the per-minibacia daily sediment drivers)

# G. Sediment (Phase C; the "blocked as science" framing is superseded - docs/30 s1)
python src/build_sediment_gauges.py             # -> sediment_daily.csv, sediment_inventory.csv
```

`report_h2e.py` runs the **reproduction gate first** and exits non-zero if the recomputed
objective does not match the archived `F = 0.25931` to 1e-8 relative; a failure there means
the environment drifted and nothing downstream is trustworthy (docs/31 Stage C0). Both
scripts are idempotent: re-running replaces the H2E rows and files rather than appending
duplicates, and the 27 pre-existing `metrics_fleet.csv` rows are preserved byte-for-byte
(a pandas read/write round trip re-emits them 3 ULP different — see docs/26 addendum A.6).

Non-negotiable conventions on this chain:

- **Use the `_qc` files** (`precip_gauges_daily_qc.csv`, `precip_gauges_inventory_qc.csv`)
  for any analysis; `approval == 'Inferido_seco'` marks inferred dry days.
- **Notebooks 10–14 are generated** by `src/nbgen/make_nb*.py`. Edit the generator, rerun
  it, then execute the notebook. Verify results from the executed outputs, not the exit
  code.
- **Never `pd.read_csv` the wide forcing CSVs** (`forcing_minibacia_*.csv`, ~180 MB,
  4,018 × 8,673): pandas silently returns a truncated *prefix* with no exception (doc 18
  trap 19). Use `src/forcing_npy.py`.
- ERA5-Land quirks (time coord `valid_time`; `ssrd` daily-resetting accumulation; scalar
  coords dropped with `drop_vars`) are in CLAUDE.md and doc 16 §6 — read before touching
  ERA5 code.
- Before trusting any station dataset, test for **absent records** (zero-suppression), not
  just outlier values; and prove the **date format from field values > 12** before parsing
  any DHIME export (doc 19 §3.1 rule box). DHIME units are per-row (`Unidad`), and CM
  arrives in kg/m³ — a silent ×1000 (doc 19 §3.2).

## 4 — Verification bars a rebuild must pass

- `python src/test_mgb_hydrology.py` — the engine's smoke/regression tests.
- Mass-balance residual < 1e-15 (measured 1.67e-17); numpy vs numba routers identical.
- Any calibration harness must reproduce the stored flows before its output is interpreted
  (bar used in doc 22: median relative error 9.1×10⁻⁹ against `q_sim_B_m3s`).
- `python3.10 src/report_h2e.py` is the standing version of that bar for the adopted
  configuration: it re-evaluates the archived best `x` of `dds_H2E_20260901.npz` and requires
  `F` to match `0.25930593639066796` to ≤ 1e-8 relative. Measured 2026-08-10: **0.000e+00**,
  with all 3 × 63 stored per-gauge terms bit-identical. Run it after any environment change
  before trusting anything built on H2E.
- nb13's assertions (period, forcing identity) must pass in the executed notebook. If a
  re-run of nb14 starts a *new* search instead of reading the four checkpoints, kill it —
  the fix belongs in `src/calib_v2.py` (doc 25 stage 0).

## 5 — Monitoring and resuming a calibration search

The DDS searches run as **separate OS processes**, one per (cell, seed) — deliberately not
a `ProcessPoolExecutor` inside the notebook (Windows spawn from a Jupyter kernel can hang;
separate processes give one log each and cannot take the kernel down):

```
python src/calib_v2.py --cell H1 --seed 20260901 --budget 1000 --out data/processed/_calib_cache/H1_s20260901.npz
```

Launch detached with `Start-Process` or `schtasks` — shell-backgrounded children
(`nohup … &`) die with the tool call that started them (doc 26 §6).

**Monitor:** `python watch_calib.py` (one snapshot) or `python watch_calib.py -w 30`
(refresh until all workers exit). It reads `data/processed/_calib_cache/logs/*.log`, never
writes to the repo, shows per-worker progress/rate/ETA, flags stale logs and non-empty
`.err` files, and places the best objective against fixed reference points (prior 0.1276,
random null 0.1729, Config B 0.2429). Remember: workers are **`python3.10.exe`** in
`tasklist`, not `python.exe`.

**Resume:** each worker checkpoints its archive to `<out>.part.npz` every 25 evaluations
(atomic tmp-then-replace, so a kill mid-write cannot leave a torn file). On restart with
the same `(cell, seed, budget)`, the RNG is re-created from the seed and the stored
evaluations are **replayed with verification** — each replayed proposal is asserted against
the checkpoint, so a resume against a checkpoint written by different code, a different
seed or different bounds *raises* instead of silently continuing a different search. A
checkpoint for a different (cell, seed, budget) is ignored; an unreadable one falls back to
a fresh start. When all budgets complete, execute nb14 to read the checkpoints and write
`sim_calibrated_v2/`.

Do not touch `data/processed/_calib_cache/` by hand while workers run.

## 6 — Traps index

The project's hard-won failure catalogue, in reading order:

| where | what it covers |
|---|---|
| [doc 16 §6](16_forcing_pipeline_audit.md) | forcing pipeline: ERA5/DHIME/IDW pitfalls that produce plausible wrong numbers |
| [doc 18 §7](18_hydrology_journal.md) | hydrology: NSE across windows, DDS archives, railed parameters, `pd.read_csv` prefix truncation, datetime64 resolution, file-count gates |
| [doc 19 §3.1, §3.11](19_sediment_qc_audit.md) | DHIME date-layout proof rule (adopt verbatim), per-row units, dedup bases, row vs calendar adjacency |
| [doc 22](22_dry_phase_diagnosis.md) | why the dry phase fails: read before touching calibration |
| [doc 23](23_gauge_geometry.md) | gauge/interpolation geometry: IDW order-dependence, co-located gauges, catchment-area unreliability |
| [doc 26 §6](26_phase3_refit.md) | the climatology-benchmark trap, datetime64[D] vs [ns], the python3.10.exe process-name trap |
| CLAUDE.md | the one-page distillation of all of the above |
