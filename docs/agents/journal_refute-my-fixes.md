# Journal: adversarial refutation of "relative-path default survives in src/mgb_hydrology.py"

Agent: refute-my-fixes. Started 2026-08-11.
Posture: default = the finding is WRONG; trying to prove it.

## Finding under test
`load_topology(processed_dir="data/processed")` (src/mgb_hydrology.py:990) and
`load_soil_params(..., path="data/processed/minibacia_soil_params.csv")` (:1024) still carry
the cwd-dependent-default defect that commit 02e7e95 ("fix: cwd-independent data paths")
claims to have fixed; both are in `mgb_hydrology.__all__`.

## Step 1 — read the commit
02e7e95 diff touches ONLY: notebooks/19_..., src/mgb_sediment.py, src/mgb_transport.py,
src/nbgen/make_nb19.py. src/mgb_hydrology.py is NOT in the diff. Commit body names
load_geometry/load_drivers/load_network specifically (sediment+transport), not a repo sweep.
So the module-level fact is already consistent with the finding. -> cannot refute on the diff.

## Step 2 — read the actual lines
grep -n "def load_topology|def load_soil_params" src/mgb_hydrology.py
  990:def load_topology(processed_dir="data/processed", *, minibacias="minibacias.csv",
 1024:def load_soil_params(topo, path="data/processed/minibacia_soil_params.csv",
Line numbers and defaults are EXACT. __all__ (lines 168-185) contains both names. -> literal
claim confirmed so far.

## Step 3 — callers (this is where the "why it matters" may break)
grep across *.py/*.ipynb: the ONLY callers of load_topology/load_soil_params anywhere in the
repo are src/test_mgb_hydrology.py:735,737,824 — and all three pass an explicit `proc`.
nb13 (src/nbgen/make_nb13.py) does NOT call load_topology; it calls mgb.build_topology() on
arrays from model_inputs_v2/topology.npz, and it has its own REPO-discovery bootstrap
(walks cwd + parents for src/mgb_hydrology.py & data/processed) making it cwd-independent.
-> the stated mechanism "notebooks 13/14 ... dies the same way nb19 did" is NOT how nb13 works.

## Step 4 — ran the reproduction myself (python3.10, cwd=notebooks/, src on sys.path)
    cwd: C:\dev\magdalena-mgb-sed\notebooks
    load_topology default:    'data/processed'
    load_soil_params default: 'data/processed/minibacia_soil_params.csv'
    in __all__: True True
    load_topology() RAISED: FileNotFoundError [Errno 2] ... 'data\processed\minibacias.csv'
    sed.load_geometry() OK, n= 8672
    sed/tr defaults are absolute WindowsPath(C:/dev/magdalena-mgb-sed/data/processed/...)
=> the finding's evidence reproduces EXACTLY. Core code claim CANNOT be refuted.

## Step 5 — AST scan of every function-signature str default in src/+scripts/+tests
9 path-ish defaults total. Only TWO are relative *directory* defaults:
mgb_hydrology.py:990 processed_dir='data/processed' and :1024 path='data/processed/...'.
mgb_sediment.py:855's five are BARE FILENAMES joined onto the absolute
DEFAULT_PROCESSED_DIR -> harmless. So the finding's "no other unfixed function-signature
path default" is ACCURATE as stated. (Module-level relative literals do exist:
src/fetch_station_coords.py:35, scripts/c2b/peaks_measure.py:10 — not signature defaults.)

## Step 6 — where the finding DOES break (severity + mechanism)
- Callers of load_topology/load_soil_params in the ENTIRE repo: 3, all in
  src/test_mgb_hydrology.py (735, 737, 824), all passing an explicit `proc` built from
  os.path.dirname(os.path.abspath(__file__)) -> already cwd-independent.
- notebooks/13_baseline_run.ipynb and notebooks/14_calibration.ipynb: grep -c load_topology
  = 0 and 0. nb13 uses mgb.build_topology() on model_inputs_v2/topology.npz, and both
  generators open with a REPO-discovery loop (walk cwd + parents for src/mgb_hydrology.py
  AND data/processed) -> those notebooks are cwd-independent by construction, so the
  asserted mechanism ("nb13/14 ... dies the same way nb19 did") does not apply to them.
- src/report_h2e.py, src/calib_v2.py, src/build_h2e_drivers.py, src/mgb_drivers.py: 0 hits.
  The adopted H2E path never touches these two loaders.
- Failure mode is a LOUD FileNotFoundError. From repo root both defaults load correctly
  (measured: 8672 / 8672). It can never produce a wrong number, only a crash.
- The written record is SCOPED, not repo-wide: 02e7e95's body names
  load_geometry/load_drivers/load_network, and progress_map.html (commit 608a39e) repeats
  exactly those three. Only the 5-word commit TITLE reads broadly. So "the next reader will
  reasonably believe this class of bug is closed" is weakened by the actual tracker text.

## Verdict
NOT refuted on fact. Refuted on severity and on the stated mechanism.
Surviving version: MEDIUM, latent-only, consistency defect. See final report.
DONE.
