# Journal — nbc1: notebook coherence audit, nb10 + nb11 (forcing)

Agent: nbc1-nb10-11-forcing. Phase 1 = T1 AUDIT ONLY, READ-ONLY. Fix nothing.
Started 2026-08-13.

## Assignment (restated)
Audit `notebooks/10_rainfall_dataset_comparison.ipynb` (12 cells) and
`notebooks/11_rainfall_pet_forcing.ipynb` (24 cells) for narrative coherence and stale/killed
numbers. I own the headline **prose-vs-code contradiction**: nb11's prose uses the older
CHIRPS-inclusive sense of "v2 forcing" while its own code sets VERSION=v2 for the repaired
GAUGE-ONLY field. I must verify every cell index myself against the extract (the index may be
off-by-one or stale) and find any the index missed. nb10 uses "v2" in a third sense: "CHIRPS v2.0"
(the satellite product's version). Also: does either notebook still present the CHIRPS merge as a
LIVE route? It is CLOSED. Does nb11 record zero-suppression repair + order-dependent-IDW fix as the
two things that define v2? Beats 1 and 3. Fix locations MUST cite `src/nbgen/make_nb10.py` /
`make_nb11.py` line numbers.

## Constraints I am holding
- Read-only. No notebook execution, no git write, no edits outside this journal.
- Measure before asserting; every finding needs a 0-based cell index + verbatim quote.
- Yield embargo: no t/km2/yr as a live claim.

## Log

### 2026-08-13 — sweep 1: read both extracts in full
- Read `nbtext/10_rainfall_dataset_comparison.txt` (12 cells, 0-11) and
  `nbtext/11_rainfall_pet_forcing.txt` (24 cells, 0-23) end to end. Both already carry a
  2026-08-12 `⚠ STATUS` banner at cell 0 plus several in-place annotations.
- **Kill-list grep over both extracts: NO hits.** Searched t/km2, km2/yr, 0.333/0.421, 2.37/3.00x,
  Buarque, SDR, f_LS, 11.8, Mt/yr, cp_revision, under-erosive, 0.1644, 0.465, k_min, 348.4,
  V4_dg, ls2d. Single numeric hit was `-2  0.095  -11.8` in nb10 cell 8's lag table — that is a
  CHIRPS **bias percentage**, NOT the Williams alpha reference 11.8. **FALSE POSITIVE, checked.**
- **Yield embargo: CLEAN in both.** No t/km2/yr string anywhere. nb11 cell 2 prints
  `total area 257,097 km2` (a minibacia area sum, not a yield) — not a violation.
- **No engine call in either notebook** — no `mgb_sediment`, no `ls2d`, no `cp_revision`.
  Both are pure forcing-construction notebooks. Engine-default staleness is N/A.

### Sweep 2 — the headline prose-vs-code contradiction, VERIFIED AND RE-INDEXED
docs/00_INDEX.md:215-225 cites nb11 prose at cells **0, 13, 22** and code at cells **1, 21**.
Measured against the extract, every one is **off by exactly +1**:

| index says | measured (0-based, extract) | text |
|---|---|---|
| prose 0 | **cell 1** | "This is the v1 baseline, deliberately gauge-only" / "adding CHIRPS in v2" |
| prose 13 | **cell 14** | "the baseline skill a CHIRPS-merged v2 must beat" |
| prose 22 | **cell 23** | "**Next:** v2 forcing - quantile-map CHIRPS onto these gauges" |
| code 1 | **cell 2** | `VERSION = 'v2'`, reads `precip_gauges_daily_qc_v2.csv` |
| code 21 | **cell 22** | prints `[v1 was 2174.3, gauge-only v2 2036.4]` |

Cause: the ⚠ STATUS banner was prepended as cell 0 by commit `57f9761` (2026-08-12), *after* the
index text was written — the index itself says "Banners ... are being added by a separate pass".
The index **missed no cell**; it is uniformly one short. **The index needs re-indexing, not the
notebook.** (docs/00_INDEX.md:192 "nb11 cell 21" → cell 22; :219 "cells 0, 13, 22" → 1, 14, 23;
:221 "cells 1, 21" → 2, 22.)

All three prose instances ARE annotated in place by 57f9761 — so the contradiction is *disclosed*,
not live. **But nb11's own banner (cell 0) says "two forward references" when there are three.**

### Sweep 3 — is the CHIRPS merge presented as a live route?
No, in both notebooks — every forward reference carries a strike-through + DO NOT ADOPT + H-CHIRPS
REFUTED annotation. **But both stop at `docs/18` §15.5 and neither cites `docs/58`.**
docs/58 (2026-08-12) bounded the last surviving route (the 139 rain-selective gauges) at
**Δr = +0.0058 area-weighted, r 0.57 → ~0.576, discharge gain ≤ that** — and it did so using
**nb11's own** `forcing_minibacia_provenance_v2.csv` isolation distribution and the 25.8/57.1/17.1 %
area shares nb11 cell 13 prints. nb10 cell 11's last line still reads *"What remains open is the
139 residual rain-selective stations ... the only remaining upstream route"* — **stale by event.**

### Sweep 4 — does nb11 record the two things that DEFINE v2?
**Yes, both, and correctly.** Zero-suppression repair: cell 2 comment "153 stations, 240,158
inferred-dry station-days ... 2,174.3 -> 2,036.4 mm/yr for 2009-2017" — matches docs/18 §10.2 /
open item 7 and docs/18:750. Deterministic IDW: cell 9 comment "lexsort on (distance, gauge code)
... up to 83 minibacias by up to 20.5 mm/day (doc 18 s11.1)" + a live
`idwf.assert_order_invariant(...)` whose output prints "3 gauge-column shuffles, byte-identical
field each time" — matches docs/23 §11 G2/G3. **Beat 1 is carried.**

### Sweep 5 — the structural duplicate nobody guarded
`src/idw_forcing.py:94` `neighbour_order()` breaks distance ties by `np.lexsort` on the gauge code.
**Both LOOCV sections re-implement the interpolator inline with plain `np.argsort`:**
`make_nb10.py:306` and `make_nb11.py:365`. The *field* (nb11 cell 9) is guarded; the **LOOCV that
produced the registered 0.429 gate is not.**
- **nb10 is the exposed one:** it does NOT call `merge_colocated`, so three gauge pairs at
  **0.000000 m** (nb11 cell 2's classification table, same inventory file) are still present ⇒
  exact distance ties from every third gauge ⇒ neighbour set resolved by COLUMN ORDER. That is the
  exact defect docs/23 §11 fixed. nb10 §4's r 0.41 / P99 0.73 / wet +18.3 pts sit on it.
- **nb11 is latent:** after the merge only the CATAM pair (0.051952 m) remains, so no *exact* ties
  survive and 0.429 is deterministic in practice. Reasoned from cell 2's printed distances; **not
  re-verified by execution** (execution is prohibited this phase).

### Sweep 6 — executed-output staleness, measured from git
- `git show --stat 57f9761 -- nb10 nb11` → markdown only; `git diff 57f9761^ 57f9761 -- nb10 |
  grep -c "outputs\|execution_count"` → **0**. The 2026-08-12 pass annotated, it did not re-execute.
- nb10 outputs date from **368e8ca (2026-08-02)**, computed on `precip_gauges_daily_qc.csv`
  (70-station repair). nb11 outputs date from **4b6fb5c (2026-08-02)**, on
  `precip_gauges_daily_qc_v2.csv` (153-station). **The two notebooks read different gauge
  datasets** — nb10's cell 3 annotation flags this for §1's counts only, never for §3/§4's CHIRPS
  and IDW metrics, which docs/16 §4.3 shows move at every cleaning stage (−13.6 → −7.6 → −5.8 %).
- **Engine staleness N/A for both:** neither generator imports `mgb_sediment` (grep of both files:
  nb11 imports only `idw_forcing`). `src/mgb_sediment.py` :818/:862 `ls2d_hs` vs :925 `V4_dg` is
  irrelevant here. No `cp_revision` in either notebook. `c3fdb55` cannot have staled them.

### Refused conclusions (measure-before-asserting)
- nb11 exports `area_km2` per minibacia (cell 22 → `forcing_minibacia_provenance_v2.csv`). I
  considered filing a yield-embargo convention gap. **Checked docs/23 §13.2: the embargoed
  quantity is the per-GAUGE upstream catchment area (D8, two implementations disagreeing >2× on
  36 % of 85 shared gauges), not the minibacia polygon area.** Not a violation. NOT filed.
- nb10 cell 8 prints `-2  0.095  -11.8` — checked, that is a CHIRPS volume-bias percentage at
  lag −2, **not** the Williams α reference 11.8. False positive. NOT filed.
- docs/31 §0's "two different LOOCV statistics" warning is 0.429 (all-period) vs 0.40 (docs/22
  §4.7 per-window El Niño) — **not** nb10's 0.41. I filed the nb10-0.41-vs-nb11-0.429 gap on its
  own evidence (same estimator, different input), not by borrowing that warning.

### Final tally
- **Cells swept: 12/12 (nb10) + 24/24 (nb11) = 36.** Every cell of both notebooks read in the
  extract; every finding carries a 0-based cell index, a verbatim quote and a generator line.
- **21 findings.** nb10: 9 (4 HIGH). nb11: 11 (2 HIGH). docs/00_INDEX off-by-one: 1 (MEDIUM).
- **0 CRITICAL.** No yield-embargo violation, no kill-list number, no reconstructed materiality
  bar, no withdrawn direction restated. Both notebooks are clean on the kill list.
- Structured object returned to the orchestrator. Nothing in the repo was edited but this file.
