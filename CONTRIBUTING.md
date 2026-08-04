# Contributing

## Setup

Python 3.10 (`python3.10` on the project box). Install the pinned dependencies:

    python3.10 -m pip install -r requirements.txt

or, with conda: `conda env create -f environment.yml`.

## Pipeline order

The processing pipeline and its hard-won rules live in `CLAUDE.md` ("Pipeline commands"
and "Conventions") and, in depth, in `docs/16_forcing_pipeline_audit.md`. Run the scripts
in the order given there. In particular, `src/repair_precip_zero_suppression.py` is
REQUIRED after `src/build_precip_gauges.py` — value screens cannot see absent records.

## The `_qc` files rule

For any analysis, use `precip_gauges_daily_qc.csv` / `precip_gauges_inventory_qc.csv`
(the post-repair files), never the pre-repair ones. `approval == 'Inferido_seco'` marks
inferred dry days.

## Notebook generators

Notebooks 10–14 are generated — do NOT edit the `.ipynb` by hand. Edit the generator,
regenerate, then execute headlessly (`jupyter` is not on PATH):

    python3.10 src/nbgen/make_nb13.py
    python3.10 -m nbconvert --to notebook --execute --inplace notebooks/13_*.ipynb

Verify results from the executed outputs, never from the run's exit code alone.

## Never `pd.read_csv` the wide forcing CSVs

`forcing_minibacia_*.csv` (~180 MB, 8,673 columns) can be **silently truncated** by
pandas: a plausible prefix, no exception, and the calendar-hole check still passes.
Read them only through `src/forcing_npy.py`, which verifies row and column counts
against the raw bytes. See that module's docstring for the incident report.

## Tests

    python3.10 -m pytest tests/ -q

## Commits

`<area>: <summary>` (e.g. `precip: ...`); the body explains the why. Push to `origin main`.
`data/`, `data_Final/`, `delivery/` are gitignored (regenerable).
