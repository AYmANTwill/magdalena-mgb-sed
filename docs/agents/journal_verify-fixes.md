# journal_verify-fixes.md

Agent: verify-fixes. Started 2026-08-11.
Lens: hostile audit of commit 02e7e95 (cwd-independent default paths; nb19 load_geometry mini_ids).

## Log

- Read CLAUDE.md, docs/00_INDEX.md, and `git show 02e7e95` (src diff only).
- Diff confirmed: mgb_sediment gains _REPO_ROOT/DEFAULT_PROCESSED_DIR/DEFAULT_DRIVERS_PATH;
  mgb_transport gains DEFAULT_TOPOLOGY_PATH; nb19 generator now passes PROC + mini_ids
  AND ALSO changed load_drivers() -> load_drivers(FROZEN / 'h2e_drivers.npz') — the commit
  message did not mention that third change. Flag for (e).
- Next: reproduce the id-ordering measurement.

## Measurements (all executed, 2026-08-11)

(a) ORDERING — REPRODUCED, the commit's claim is TRUE.
    minibacias.csv id vs h2e_drivers.npz:minibacia_id -> 8672 vs 8672, differing
    positions = 0, np.array_equal = True, both strictly ascending, 0 duplicates.
    Independent witness: minibacias.area_km2 joined by id equals drivers own_area_km2
    with maxabs 0.0.
    BONUS: topology.npz:minibacia_id is ALSO identical to both (0 differing positions).
    So all three project id vectors coincide today.

(b/c) __file__ resolution is correct for both modules (both live directly in src/,
    so parent.parent is the repo root). Measured from cwd=notebooks/:
      relative 'data/processed' exists there? False
      sed.DEFAULT_PROCESSED_DIR -> C:\dev\...\data\processed  is_dir True
      sed.DEFAULT_DRIVERS_PATH  -> ...h2e_drivers.npz          is_file True
      tr.DEFAULT_TOPOLOGY_PATH  -> ...topology.npz             is_file True
      sed.load_geometry() from notebooks/ -> 8672 minibacias  PASS
    pyproject.toml explicitly states the repo is NOT an installable package and code is
    "run in place" -> the installed-copy objection is retired by project declaration.
    No symlinks are tracked (git ls-files mode 120000: none).

(f) THE SAME TRAP IS STILL LIVE IN src/mgb_hydrology.py — MEASURED:
      load_topology(processed_dir="data/processed")   <- unfixed
      load_soil_params(..., path="data/processed/minibacia_soil_params.csv") <- unfixed
      from cwd=notebooks/: hyd.load_topology() -> FileNotFoundError(2)
    Both are in mgb_hydrology.__all__.

TEST GAP: nothing in tests/ references DEFAULT_PROCESSED_DIR / DEFAULT_DRIVERS_PATH /
    DEFAULT_TOPOLOGY_PATH, and no test chdirs. The fix has zero regression coverage.

pytest: 138 passed, 1 warning in 127.96s (exit 0), `python -m pytest tests/ -q`.
    (`python` and `python3.10` are both 3.10.11 on this box.)

## Verdict on the two changes

CHANGE 1 (cwd-independent defaults): SOUND. parent.parent is the repo root for both files
    (both sit directly in src/). load_network handles a Path (pathlib.Path(path) at
    mgb_transport.py:435). No symlinks tracked. pyproject.toml declares the repo
    non-installable and "run in place", so the installed-copy objection is retired by
    project declaration, not by my assumption.
    Two nits, both LOW:
      - src/mgb_sediment.py now spells the repo root two ways in ONE file:
        line 449 `.parent.parent` (new) vs line 519 `.resolve().parents[1]` (pre-existing,
        for scripts/c3/qpeak.py). 15+ other files in src/ and scripts/ use `.parents[1]`.
      - mgb_transport duplicates the expression rather than importing it — but that is
        DEFENSIBLE: its module docstring makes the non-import of mgb_sediment a design
        commitment ("It is a SEPARATE module ... on purpose"). Not a finding.
    (d) __all__ / docstrings: the new constants are in __all__ and are NOT described in the
    module docstring — but neither are VOLUME_CONVENTIONS, K_UNIT_SYSTEMS or QSUR_FIELDS
    (measured: 0 docstring hits each). Consistent with existing practice. Not a finding.

CHANGE 2 (mini_ids in nb19): SOUND and numerically a no-op, reproduced above.

## Findings raised (see final report)
F1 HIGH   src/mgb_hydrology.py:990 and :1024 still carry the identical relative default.
F2 MEDIUM the fix has no regression test; every test passes an explicit path.
F3 MEDIUM src/nbgen/make_nb*.py (10 files) hardcode OUT = c:\dev\magdalena-mgb-sed\...
F4 MEDIUM scripts/c2b/peaks_measure.py: relative NPZ + OUT pinned to a Claude session
          scratchpad; its outputs back docs/33 §7 H-PEAK.
F5 LOW    commit-message accuracy: "cell 3" (it was the 2nd code cell / In[2], overall
          cell index 6 of the pre-fix notebook); the nb19 load_drivers() -> explicit
          FROZEN path edit is not mentioned; the title's "cwd-independent data paths"
          overstates scope given F1.
F6 LOW    remaining relative literals: src/fetch_station_coords.py:14/34/35,
          src/organize_precip_regions.py:19, src/download_era5.py:22,
          src/download_era5_strip.py:16.

DONE. Nothing left half-finished.
