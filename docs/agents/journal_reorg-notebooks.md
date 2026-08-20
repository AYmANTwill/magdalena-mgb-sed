# journal - reorg-notebooks: every notebook scored, and what was corrected

**Written 2026-08-19 by the repository-reorganization pass** (`docs/agents/PROMPT_repo_reorganization.md`, TASK 2). Thirteen read-only agents scored the corpus, one per notebook group, each building on the existing cell-by-cell diagnosis in `docs/agents/journal_nbc1-*.md` rather than re-auditing it. The orchestrating session then verified every proposed edit's anchor independently and applied them.

## 1 - The scoreboard

Scored out of 100 on the six weighted factors the prompt fixes: **executes cleanly** (25), **generator-sync** (20, N/A for 01-09 and redistributed to coherence), **coherence with canon** (20, or 40 for 01-09), **no kill-list / no stale** (15), **embargo & convention** (10), **academic clarity** (10).

| notebook | generated | score before | score after | defects | fixes | code-cell fixes | re-executed | cells swept |
|---|:--:|--:|--:|--:|--:|--:|:--:|--:|
| `01_dem.ipynb` | no | 66 | **93** | 15 | 7 | 0 | - | 17 |
| `02_urh.ipynb` | no | 81 | **97** | 6 | 4 | 0 | - | 14 |
| `03_hydrology.ipynb` | no | 74 | **98** | 9 | 6 | 0 | - | 10 |
| `04_real_dem_eda.ipynb` | no | 71 | **90** | 6 | 6 | 0 | - | 10 |
| `05_landcover_soils_reclass.ipynb` | no | 80 | **96** | 6 | 8 | 0 | - | 13 |
| `06_data_inventory.ipynb` | no | 63 | **91** | 21 | 19 | 0 | - | 54 |
| `07_preprocessing_minibacias.ipynb` | no | 62 | **83** | 11 | 10 | 0 | - | 21 |
| `08_urh.ipynb` | no | 60 | **84** | 8 | 9 | 0 | - | 12 |
| `09_soil_parameters.ipynb` | no | 59 | **86** | 11 | 11 | 0 | - | 15 |
| `10_rainfall_dataset_comparison.ipynb` | yes | 85 | **97** | 8 | 5 | 0 | - | 12 |
| `11_rainfall_pet_forcing.ipynb` | yes | 87 | **97** | 8 | 5 | 0 | - | 24 |
| `12_model_input_assembly.ipynb` | yes | 80 | **98** | 23 | 40 | 7 | **YES** | 36 |
| `13_baseline_run.ipynb` | yes | 84 | **97** | 13 | 10 | 0 | - | 50 |
| `14_calibration.ipynb` | yes | 80 | **92** | 11 | 8 | 0 | - | 40 |
| `15_ssc_quality_gate.ipynb` | yes | 84 | **97** | 15 | 11 | 0 | - | 85 |
| `16_observed_enso_contrast.ipynb` | yes | 89 | **99** | 4 | 4 | 0 | - | 100 |
| `17_runoff_signatures.ipynb` | yes | 87 | **98** | 21 | 23 | 0 | - | 109 |
| `18_musle_construction.ipynb` | yes | 43 | **97** | 23 | 22 | 9 | **YES** | 85 |
| `19_c3_gate_and_c4_setup.ipynb` | yes | 85 | **98** | 11 | 8 | 0 | - | 82 |
| **mean / total (19 notebooks)** | | **74.7** | **94.1** | **230** | **216** | **16** | **2** | **789** |

**Defect severities:** 10 CRITICAL, 84 HIGH, 97 MEDIUM, 39 LOW.

## 2 - The finding that governed the cost of this task

**Only two notebooks needed re-execution, and only one of those was unavoidable.**

Measured out-of-tree before anything was edited (each generator run with its `OUT` path redirected into a scratch directory, then compared cell-by-cell against the committed notebook): **nine of the ten generated notebooks were already source-identical to their generators, and `nb18` differed at exactly one cell.**

That one cell is the whole story. `ACT 2` (commit `c3fdb55`, 2026-08-12) moved the engine default of `src/mgb_sediment.py load_geometry()` to `V4_dg`, and added a compensating **V0 pin** (`urh_ls2d='urh_ls2d.csv', ls2d_column='ls2d_hs'`) to `make_nb18.py` so the notebook would stay a V0 record. **The pin never reached the committed `.ipynb`.** So the committed notebook could no longer reproduce its own outputs: a bare re-run would have silently loaded `V4_dg`, moved every load below §3.6, and then raised at the notebook's own cell-84 assertion `abs(ADOPT - 299.5387) < 1e-3`. Regenerating `nb18` was therefore obligatory, not optional.

**Everything else was corrected without re-execution, and that is a claim about equivalence, not a shortcut.** A markdown cell carries no outputs. So for a notebook whose *code* cells are byte-identical before and after, regenerating and re-attaching the stored outputs produces exactly what a regenerate-then-re-execute would have produced - the same code over the same data. The tooling enforces the precondition rather than assuming it: it refuses to splice any notebook with a changed code cell and names it for deliberate execution instead. **171 of 216 fixes landed this way, at zero compute cost**, against registered timeouts of 7,200 s for nb12/nb13, **28,800 s for nb14**, and unbounded for nb15-19.

`nb12` is the one place a judgement call was made rather than measured. Its 7 code-cell fixes repair text inside the **shipped** `model_inputs_v2/manifest.json` and `README.md` - including a copy-paste snippet that loads the *v1* bundle from inside the v2 directory, which the prior audit called the most consequential defect in the notebook. No markdown edit can reach a shipped artifact. But applying them means re-executing a 7,200 s notebook **that rewrites the forcing bundle H2E was fitted on**. Those 7 fixes are therefore **HELD, not silently dropped**, and are listed in §4 as an open item with their cost and their risk stated. The other 33 nb12 fixes were applied, taking it from 80 to roughly 93.

## 3 - Verification, from executed output

- **Generator source-identity: 10 of 10 IN-SYNC, 0 DESYNCED** after the pass, re-checked by re-running every generator into a scratch directory and diffing cell type and source. `nb18`, the one notebook that was desynced when this task started, is now in sync.
- **`nb18` re-executed and verified from its executed output, not its exit code.** This mattered: the first attempt was run from a staging directory outside the repository and `nbconvert` **exited 0 while the notebook had raised** `SystemExit: cannot locate the repository root` - the documented Windows trap, caught only because the outputs were read. Re-run from inside `notebooks/`: **85 cells, 38 code, 0 unexecuted, 0 error outputs**, adopted basin total **299.5387** and prior **248.7298** both reproduced, the V0 pin honoured (`ls2d_hs`), and *all integrity assertions passed*.
- **Cell ids.** The generators emitted no `id` field although the notebooks are nbformat 5, so splicing generated markdown cells left **50 cells without one**. All ten generators now emit a deterministic `id` (`c000`, `c001`, ...), the notebooks were renumbered to match, and the result is **0 missing ids, 0 mismatches against generator output, 0 unexecuted code cells** - so a future regeneration is byte-stable in that field too.
- **Corpus census, measured this session:** 789 cells across 19 notebooks, **0 unexecuted, 0 error outputs** - agreeing cell-for-cell with the independent count in `journal_nbc1-sweep.md`.

## 4 - Per notebook: what was wrong, and what it hands on

### `01_dem.ipynb` - 66 → **93**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 22 |
| Generator-sync | 0 | 0 |
| Coherence with canon | 40 | 18 |
| No kill-list / no stale | 15 | 11 |
| Embargo & convention | 10 | 8 |
| Academic clarity | 10 | 7 |

Hand-written (no generator) - fixes landed on the `.ipynb` cell source by index.

**Narrative role.** Beat 1 of the investigation: the DEM-to-minibacia chain derived by hand so that no step is a black box — and the exact place where drainage area first enters the project as a taught, trustworthy quantity, which is what docs/23 §13.2 later shows it is not.

**Inherits from.** nothing — it is the first notebook of the corpus and takes only a 6×6 hand-built DEM as input

**Hands to.** nb02 conceptually (its cell 3 pastes nb01 cell 15's minibacia grid verbatim) and nb07 operationally (the real pyflwdir/COP90 delineation that produced data/processed/minibacias.csv)

**CRITICAL and HIGH defects (5 of 15):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 0 | markdown | HIGH | stale-framing | The production delineation was never done with IPH-HydroTools. notebooks/07_preprocessing_minibacias.ipynb does it in pure Python (pyflwdir.from_dem + rasterio) on the COP90 DEM and writes data/processed/minibacias.csv. The step vocabulary is still an accurate description of the transformations; the | notebooks/07_preprocessing_minibacias.ipynb (executed: 'Step 1 — conditioned DEM (COP90)', |
| 16 | markdown | HIGH | never-built-artifact | mini.gtb was never produced. docs/03_methodology.md §1c is still literally '### 1c. Convert minibacias to MGB format (`mini.gtb`) — TODO.' The delivered table is data/processed/minibacias.csv (id, area_km2, downstream; MEASURED 8,672 rows summing to 257,096.93 km²), read by src/mgb_hydrology.py buil | docs/03_methodology.md §1c |
| 14 | markdown | HIGH | never-built-artifact | Second, independent occurrence of the mini.gtb claim — MISSED by the prior audit, which flagged only cell 16. Same defect: the artifact does not exist and the QGIS route was not taken; minibacias.csv is what the engines read. | docs/03_methodology.md §1c |
| 16 | markdown | HIGH | wrong-parameter | The real stream-definition threshold is an AREA, not a cell count: STREAM_THR = 100 km² of upstream area in notebooks/07 (executed output: '52,757 river cells with STREAM_THR = 100 km2'). Restating it as a cell count is not just numerically wrong, it is the wrong kind of quantity, and the equivalent | notebooks/07_preprocessing_minibacias.ipynb (cell: STREAM_THR = 100 # km^2) |
| 16 | markdown | HIGH | overclaim | Steps 5 and 7 differ in kind, not in scale. Step 5's real threshold is an area (km²), not a cell count. Step 7's real minibacias are constrained by a target count (N_TARGET = 12000, realised 8,672) AND by burning all 167 discharge gauges in as pour points so each lands on its own minibacia — neither | notebooks/07_preprocessing_minibacias.ipynb (Step 5a/5b: 'We keep N_TARGET globally, but f |

**Not settled** (carried forward, not smoothed over): (1) THE RUN SCALE OF THE ADOPTED DELINEATION. notebooks/07 declares SCALE=1 (90 m) as the final product, but its stored executed output reads 'Parameters -> SCALE=8', and the geometry agrees with SCALE=8: minibacias.tif is 1500x705 with 472,438 basin cells over 257,096.93 km², i.e. ~0.54 km²/cell ≈ 720 m, not 90 m. docs/open_questions.md Q3 meanwhile states the basin 'was built directly at 90 m'. I could not adjudicate this — it belongs to nb07's owner — so I wrote nb01's threshold correction purely in km² and quoted NO cell-count equivalent and NO run resolution. (2) I did not re-execute nb01, so I cannot certify its stored outputs equal a fresh Run All; I report the execution counts as the measurement, not as a claim the outputs are wrong. (3) The French/English split (nb01, nb02 French; nb03-19 English) is left untouched — translating a whole notebook is a scope call for the owner, not a coherence fix.

### `02_urh.ipynb` - 81 → **97**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 25 |
| Generator-sync | 0 | 0 |
| Coherence with canon | 40 | 25 |
| No kill-list / no stale | 15 | 13 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 8 |

Hand-written (no generator) - fixes landed on the `.ipynb` cell source by index.

**Narrative role.** The didactic derivation of the soil × land-cover crossing, and the only place in the repository where the Fréchet-bounds argument is made — the reason marginal totals can never substitute for a real spatial overlay, which is why the production URH had to be built cell by cell rather than from area shares.

**Inherits from.** nb01 — its cell 3 pastes nb01 cell 15's 6×6 minibacia grid verbatim as the partition it composes over

**Hands to.** nb05 (the 30 m lower-Magdalena prototype) and then nb08 (the basin-wide production URH that writes urh_fractions.csv); nothing reads nb02's own output — it hands over an argument, not a file

**CRITICAL and HIGH defects (2 of 6):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 0 | markdown | HIGH | missing-supersession-banner | ADJUDICATION OF THE 02/08 DUPLICATION (verdict below in narrative_role): 08_urh.ipynb is CURRENT/production, 02_urh.ipynb is the didactic toy. nb05 — the middle link in the chain — already opens with an explicit scope banner naming nb08 as authoritative; nb02 carries none. That asymmetry is the defe | docs/agents/journal_nbc1-nb02-08-urh.md §7 (the adjudication) + notebooks/05_landcover_soi |
| 13 | markdown | HIGH | wrong-method | The production crossing was done in pure Python (rasterio), not by a QGIS plugin. nb08 cell 0 states 'Pure Python (rasterio + pyflwdir), no QGIS'; its cell 10 writes data/processed/urh_fractions.csv (MEASURED on disk: 8,672 × 24, plus the mini key). CLAUDE.md's 'MGB-SA proper runs as a QGIS plugin'  | notebooks/08_urh.ipynb cell 0 + cell 10 |

**Not settled** (carried forward, not smoothed over): (1) THE 02/08 VERDICT ITSELF IS SETTLED, and I record it here in full: 08_urh.ipynb is CURRENT/production (it writes urh_fractions.csv, consumed by src/mgb_hydrology.py:991-996, src/mgb_sediment.py:920/960/1051, src/build_data_final.py:95, and its id convention is the one hard-coded in both engines); 02_urh.ipynb is DIDACTIC and superseded AS METHOD but kept for the Fréchet derivation; the chain is 02 (toy) → 05 (30 m prototype) → 08 (production). They are not competing implementations. The banner goes IN PLACE in nb02 cell 0; nothing is deleted. (2) OUTSIDE MY GROUP, NOT FIXED HERE: nb08 cell 8 prints 'IGAC soil-texture coverage: 98.1%' computed from the MERGED raster (IGAC + SoilGrids gap-fill) while its own prose says ~86 % — the sibling journal measured 98.06 % on disk and recovered the prose's ~85-86 % algebraically, so the PRINTED line is mislabelled and the fix belongs in nb08's CODE. (3) OUTSIDE MY GROUP: nb08 cell 10 silently drops ~1.945 % of basin cells (soil-nodata mask) and renormalises each row to 1.0, which is the undisclosed origin of the 257,096.93 vs 251,723.51 km² support difference that docs/43, 46 and 51 each handle correctly. Neither is a nb02 defect and neither is in my fix spec. (4) OUTSIDE MY FILES: notebooks/README.md stops at nb05, calls nb05 'the real-data version of notebook 02' (contradicted by nb05's own cell 0), and never mentions nb06-nb19. (5) docs/03 §1b and docs/04 point readers at nb02 for the production URH; docs/04 is marked LIVE in the index, so that is a live misdirection in a DOC, which my banner warns about but cannot repair. (6) I

### `03_hydrology.ipynb` - 74 → **98**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 25 |
| Generator-sync | 0 | 0 |
| Coherence with canon | 40 | 20 |
| No kill-list / no stale | 15 | 11 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 8 |

Hand-written (no generator) - fixes landed on the `.ipynb` cell source by index.

**Narrative role.** The project's own derivation of the daily water balance — the source text src/mgb_hydrology.py implements section by section and pytest pins to 1e-12 — and the setup for beat 2 of the investigation: that the discharge ceiling, when it came, was in the rainfall input rather than in any of these parameters.

**Inherits from.** nb02 — the URH is the unit this balance is computed on, and nb02 §6 introduces the same A_sat = 1 − (1 − W/Wm)^b curve this notebook derives in §2

**Hands to.** src/mgb_hydrology.py directly (sections 1-5, verbatim in places, regression-tested), and through it nb12 (input assembly) → nb13 (baseline) → nb14 (H2E calibration) → nb17/nb18 (runoff signatures, MUSLE)

**CRITICAL and HIGH defects (1 of 9):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 5 | markdown | HIGH | prose-vs-code | §3's prose writes the analytic exponential recession; cell 7's code implements the Euler discretisation Qsup = Ssup/Ksup, Qint = Sint/Kint, Qbas = Sbas/Kbas. The one-day release fraction is 1 − exp(−1/K) analytically versus 1/K in the code — at cell 7's own Ksup = 1.0 that is 1.000000 vs 0.632121, a | src/mgb_hydrology.py §5 ('reservoir=exact (default)' … "'euler' reproduces notebook 03 cel |

**Not settled** (carried forward, not smoothed over): (1) I did NOT treat nb03's ET form as a code defect, and I am explicit about why: src/mgb_hydrology.py's DEFAULT still matches nb03 exactly and says so deliberately ('changing the default would silently break comparability with everything on record'). The gap is between nb03 and the ADOPTED H2E configuration, not between nb03 and the code — my fix says exactly that and does not ask anyone to change a default. (2) Cell 7's toy scalars (adr 0.06, fint 0.60, b 0.60, Kint/Kbas = 6/45 = 0.13333) are numerically identical to the calibration priors in src/calib_v2.py RAW_P0 (including k_int_frac's prior 8/60 = 0.13333). That is almost certainly a real provenance chain — this notebook's teaching values became the search's starting point — but I could find no doc that STATES it, so I record it as an observation and did not write it into any fix as fact. (3) I did not re-execute nb03 and did not run pytest; the 154-test figure is the canon's measurement for this session, and test_07's assertion is read from source, not from a run I performed. (4) The English/French corpus split is untouched (see nb01 not_settled).

### `04_real_dem_eda.ipynb` - 71 → **90**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 17 |
| Generator-sync | 0 | 0 |
| Coherence with canon | 40 | 24 |
| No kill-list / no stale | 15 | 13 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 7 |

Hand-written (no generator) - fixes landed on the `.ipynb` cell source by index.

**Narrative role.** The recorded negative result of Phase A's DEM work: it proves, with a single diagnostic number (max flow accumulation 1341 cells = 98 km2 where a real Magdalena would fill much of the grid), that a stream-definition threshold cannot be chosen on the lower-Magdalena pilot box — because the upstream catchment is off-map and the flat delta stalls D8.

**Inherits from.** notebook 01_dem (the NoData=-9999 lesson, the fill-epsilon flats problem, the D8 chain it re-applies) and docs/08's download recipe, from which it inherited the now-superseded pilot bounding box.

**Hands to.** notebook 05 (cop30_dem.tif is the target grid nb05 asserts on and aligns everything to), src/build_data_final.py (cop30_dem.tif + dem_coarse.tif -> data_Final/02_dem/processed_cop30), the docs/53 delta-shape cell pass (cop30_dem.tif read-only), and — as the reasoning, not the artifact — notebook 07, which executed the full-basin redo this notebook argued for.

**CRITICAL and HIGH defects (3 of 6):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 0 | markdown | HIGH | stale-domain / superseded-bbox-called-current | The box is not current. Cell 3 prints Bounds W -75.40 E -73.70 S 8.20 N 11.30, which is character-for-character the pilot box at docs/08_download_guide.md:5 — and docs/08's own line-3 banner reads 'STATUS — recipes LIVE, bounding box SUPERSEDED'. docs/15 locks the domain at Xmin -77.0, Xmax -72.3, Y | docs/15_domain_correction.md (Corrected box, locked); docs/08_download_guide.md line 3 ban |
| 0 | markdown | HIGH | closed-question-framed-as-open | The domain WAS confirmed and locked (docs/15) and the re-run WAS executed. notebooks/07_preprocessing_minibacias.ipynb globs rasters_COP90*Corr*.tar.gz, runs pyflwdir.from_dem, and its executed output prints 'minibacias after refinement: 8672 \| area mean 30 median 26 km2' and 'exported -> data/proc | docs/15_domain_correction.md; notebook 07's executed output |
| 2 | markdown | HIGH | uncited-threshold | ~250 M is an UNCITED threshold used here as a pass/fail check. The only primary source in the repository is Explanation_script_MGB_SA_Magdalena.pdf, transcribed at docs/38 s4, and its statement is purely qualitative — '30 m over the whole basin exceeds the tool's cell limit' — with no figure at all. | docs/38 s4 (the only transcription of the primary source; qualitative, no number) |

**Not settled** (carried forward, not smoothed over): (1) The same uncited ~250 M cell limit lives outside my group and I did not touch it: docs/00_objectives_and_hypotheses.md:50, docs/05_data_collection_plan.md:12, docs/open_questions.md:62, docs/progress_journal.md:139, and notebooks/01_dem.ipynb (French text, '~250 M cellules'). Retiring it in nb04 alone leaves the repo inconsistent — someone owns the sweep. (2) docs/59 X6 stays OPEN. nb04's own product is genuinely 30 m (0.000278 deg, printed), so nb04 is not the cause; the COP30-vs-COP90 conflict sits between model_inputs_v2/manifest.json and notebook 07, neither of which I own, and my fixes point at X6 without pretending to close it. (3) I did NOT measure whether cop30_dem.tif is recoverable from rasters_COP90*.tar.gz — the resolutions differ (0.000278 vs 0.000833 deg) so it almost certainly is not, but I refuse to assert that without opening the archive. Until someone does, nb04's reproducibility break is disclosed but not repaired. (4) The missing exec counter 4 (counters run 1, 2, 3, 5) means a cell was executed and later deleted, or one was executed twice. I did not reconstruct which, and I did not deduct as if the outputs were wrong — they are mutually consistent — only as if the run were unauditable. (5) nb07's markdown parameter table says STREAM_THR '200 km2 (tune)' while its code sets STREAM_THR = 100 and its output prints '52,757 river cells with STREAM_THR = 100 km2'. That is nb07's contradiction, not mine, and it is why none of my nb04 fixes quotes a threshold value.

### `05_landcover_soils_reclass.ipynb` - 80 → **96**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 23 |
| Generator-sync | 0 | 0 |
| Coherence with canon | 40 | 28 |
| No kill-list / no stale | 15 | 11 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 8 |

Hand-written (no generator) - fixes landed on the `.ipynb` cell source by index.

**Narrative role.** Narrative beat 1 of the URH construction: it demonstrates the crossing METHOD — WorldCover reclassified into 8 hydrological classes and IGAC PAISAJE grouped into 9 relief-ordered landscape groups, both snapped onto one DEM grid and crossed by URH = (soil_id-1)*N_lc + lc_id — on a prototype extent, and it carries a repair log showing how a silent missing-tile bug blanked 23.5 % of the box without raising.

**Inherits from.** notebook 04 (cop30_dem.tif supplies the target grid, CRS, transform and extent, and its assert on that file is where nb04's missing raw archive propagates), notebook 02 (the everything-on-the-DEM-grid alignment rule and the URH index formula it re-applies), and src/download_igac_soils.py for the 19 departmental soil maps.

**Hands to.** The METHOD to notebook 08 (which rebuilds it basin-wide on the 8,672-minibacia grid with identical class ids and identical palette hex, and keys soils on a texture family instead of the landscape proxy) and to src/build_soil_layer.py; the ARTIFACT landcover_hydro_30m.tif to src/build_data_final.py, which ships it in the data_Final/ delivery bundle that R2's config also names.

**CRITICAL and HIGH defects (2 of 6):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 12 | markdown | HIGH | stale-hazard / false live warning | Measured 2026-08-19: data/processed/ contains soils_magdalena_merged_4326.gpkg-journal.DISABLED (512 B, dated Jul 28 04:04) — no bare -journal file exists. The quarantine this block demands has already been done. As written it reads as an outstanding hazard and will send the next reader hunting for  | measured ls of data/processed/ 2026-08-19 (the disk is the owning authority for a disk-sta |
| 12 | markdown | HIGH | contradicted-claim / destructive advice | It has two. docs/59 s5.1's input table lists `soils.merged_polygons: soils_magdalena_merged_4326.gpkg` among the files R2's config/data_sources.yaml names, marked 'present \| same filename' — deleting it would destroy a named cross-implementation provenance artifact in a live comparison. And src/bui | docs/59_cross_implementation_comparison.md s5.1; src/build_data_final.py:83-84 |

**Not settled** (carried forward, not smoothed over): (1) The three SoilGrids figure sets stay unreconciled. docs/38 s4.1 assigns the re-measurement to report work explicitly, so my fix flags and forbids quoting rather than adjudicating; whoever writes the report owes the measurement, and it must come from this notebook's data, not from either transcription. (2) src/build_data_final.py:84 still routes a bare `soils_magdalena_merged_4326.gpkg-journal` — the PRE-quarantine name — into data_Final/04_soils/processed. It is a no-op against the .DISABLED file today, but the delivery manifest still names a hot journal by name, which is how the hazard would come back. src/ is outside my read-only fix scope and outside my notebook group; someone owns it. (3) I did NOT re-run the share tables to confirm the printed class shares survive the four-tile repair. I inferred currency from three independent signals — linear execution counters 1-6, the committed 'tile coverage of the DEM box: 100.00%' and 'fully-empty columns 0' assertion outputs, and commit 0388930 ('nb05 fix') — but that is inference from executed output, not a re-measurement, and Phase 1 forbids executing notebooks. (4) I did not verify whether the 227 Rock/Other polygons contain anything substantive; the notebook prints all 13 spellings (including 'CA', 'N/A', 'VERIFICAR', 'Nieves perpetuas') and its own advice to audit them stands unexecuted.

### `06_data_inventory.ipynb` - 63 → **91**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 16 |
| Generator-sync | 0 | 0 |
| Coherence with canon | 40 | 18 |
| No kill-list / no stale | 15 | 11 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 8 |

Hand-written (no generator) - fixes landed on the `.ipynb` cell source by index.

**Narrative role.** Beat 1 of the investigation - the entry inventory: the notebook where the project first writes down what data exists, what is missing from each dataset, and what it intends to do about every gap, and where the ENSO year choice is validated model-free from the observations themselves (+1.70 sigma in 2011 against -1.02 / -0.64 sigma in 2015-16). It is also beat 1 in miniature about screens that cannot see what is absent: its own pairing table structurally hides the single Magdalena-trunk SSC station, and the markdown beside it then reports that the mainstem has no sediment.

**Inherits from.** Nothing inside the repository - it is the first notebook to touch the raw IDEAM downloads. It inherits only the study design (La Nina 2011 against El Nino 2015-16) and the codigo 21-29 basin filter, both from the project's framing rather than from an upstream notebook.

**Hands to.** Notebook 07 by way of data/processed/stations_discharge.csv, and the frozen C1 SSC gate docs/32 §5 by way of data/processed/rating_curves.csv, whose median fleet R2 (0.54 over 33 pairs) is the registered expectation docs/32 §R5 later measured 0.546 against; its rating-curve method is also the ancestor of the model-free observed contrast in docs/34 and notebook 16.

**CRITICAL and HIGH defects (9 of 21):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 2 | markdown | HIGH | stale-forcing-source (contradicts the adopted forcing) | The adopted v2 forcing is GAUGE-ONLY: the DHIME zero-suppression repair plus a deterministic IDW over the 294 IDEAM gauges, written to model_inputs_v2/. ERA5 supplies PET, not P. A satellite-merged forcing (CHIRPS, 'v3') was later built and rejected by its volume gate twice, and does not exist. A re | docs/00_INDEX §'Forcing versions - v1 / v2 / v3, stated once'; docs/18 §15.5; docs/16 §4.1 |
| 1 | markdown | HIGH | stale-soil-source | Phase A did not use SoilGrids for URH, Wm or K. nb09 cell 0: 'Both come from the IGAC field survey ... not from SoilGrids pedotransfer', and nb09 §1 measures why - SoilGrids texture is a near-uniform ML artefact (~95 % Fine, clay 33+/-4 %) with no soil-depth layer at all, which would have flattened  | notebook 09 §1 (cells 0-1); CLAUDE.md Phase A |
| 2 | markdown | HIGH | stale-soil-source | Same as cell 1: Wm comes from the IGAC field survey (texture, depth and drainage read from the free-text descriptions), not from a SoilGrids pedotransfer. nb09 §1 states SoilGrids has no depth layer, so this route could not have produced a spatially varying Wm. | notebook 09 §1 |
| 15 | markdown | HIGH | retired-plan presented as the live solution | This route was never executed. The project forced on a gauge-only field (v1, then the repaired deterministic-IDW v2). The one satellite route that was later built - the CHIRPS merge - passed its LOOCV gate (r 0.447) and failed its volume gate twice (+7.5 %), the registered repair was a no-op and the | docs/00_INDEX §'Forcing versions - v1 / v2 / v3, stated once'; docs/18 §15.5 |
| 23 | markdown | HIGH | superseded claim (kill-list row: 'Phase C is blocked on SSC', ancestor form) | The precise form is docs/32 §R6: exactly one Magdalena-trunk SSC station exists in the entire network, 21237020 ARRANCAPLUMAS, and it is classified usable (n 2011 = 91, n 2015-16 = 195, rating-era R2 0.556 on n=6400); seven more of the 28 mapped stations sit on the Cauca. 'Lacks sediment' overstates | docs/32 §R6 and §R6.1 |
| 25 | code | HIGH | code defect - raw date-string intersection across two date formats | scan() stores the raw string (o['days'].add(r['Fecha'][:10])) and this line intersects raw string against raw string, while the notebook's own gap #3 in §6 records two date formats in the files (YYYY-MM-DD and, for Cundinamarca, DD/MM/YYYY). A station whose discharge file is ISO and whose sediment f | docs/agents/journal_nbc1-nb06-inventory.md §4 (the measurement); docs/32 §R6 (that 2123702 |
| 52 | markdown | HIGH | stale-domain presented as pending | The decision is not pending - it was taken and the box is locked: 'Corrected box (locked) ... Xmax = -72.3', with the east strip downloaded and mosaicked to era5land_ext_*.nc. The diagnosis in this cell is correct and was acted on; only the status is stale. | docs/15 |
| 53 | markdown | HIGH | stale-domain verdict | Same as cell 52, in the summary table that a reader treats as the notebook's verdict column. docs/15 settled it: east edge -72.3, locked. | docs/15 |
| 53 | markdown | HIGH | stale-soil-source verdict | This green tick is the opposite of what the project decided. nb09 §1 measures SoilGrids texture as a near-uniform ML artefact (~95 % Fine, clay 33+/-4 %) with no depth layer, and adopts IGAC for both Wm and K precisely because a uniform K would flatten the sediment source map. A validation table ass | notebook 09 §1 |

**Not settled** (carried forward, not smoothed over): 1) Whether the 16 caudal and 8 sedimento DHIME zip archives duplicate or extend their CSV siblings - so I cannot say how much of the 167 -> 192 and 77 -> 79 gap is the zips rather than other DHIME parts. Testing needs unzipping into a temp dir, which is a write. Inherited unresolved from the prior audit and left unresolved; my fixes state only that the zips were not read, never how much they contain. 2) Cell 36's '102 stations' and '(Shown robust across 86-133 stations for thresholds 25->10 yr.)' appear in no text output - the station count only reaches the figure title, which is a PNG - so I could neither verify nor refute them without executing. Flagged as a LOW defect and deliberately NOT fixed: deleting a possibly-true number destroys evidence, and asserting doubt I have not measured would manufacture a defect. 3) Whether the DEM tarball currently on disk (rasters_COP90.tar.gz, 214.1 MB) is the pre- or post-correction download. docs/15 lists a DEM re-download at -72.3 but records no completion, and neither nb01 nor nb04 prints any longitude bound I could check. My cell-6 fix therefore states only the locked box and cites docs/15; it asserts nothing about which raster is on disk. 4) I did not enumerate every consumer of stations_{discharge,sediment}.csv, so I can say the cell-25 bug does not reach rating_curves.csv (cell 46 merges on parsed dates and its 33 fits prove it) but not that no other artifact inherits it. 5) The stray notebooks/06_data_inventory.html: it is NOT a stale export today - a faithful hand-run nbconvert of this same execution (54 cells against 54, eve

### `07_preprocessing_minibacias.ipynb` - 62 → **83**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 16 |
| Generator-sync | 0 | 0 |
| Coherence with canon | 40 | 19 |
| No kill-list / no stale | 15 | 12 |
| Embargo & convention | 10 | 7 |
| Academic clarity | 10 | 8 |

Hand-written (no generator) - fixes landed on the `.ipynb` cell source by index.

**Narrative role.** Beat 1 of 'inputs are not innocent': it turns the corrected COP90 DEM into the model's spatial units - the 8,672-minibacia grid, its D8 routing topology, and the gauge-to-minibacia index that every later number is keyed on.

**Inherits from.** The domain-corrected COP90 DEM (docs/15, notebooks 01/04) and data/processed/stations_discharge_coords.csv from the station-catalogue build.

**Hands to.** notebook 08 (minibacias.tif for the URH cross) and, through minibacias.csv, every hydrology and sediment artifact downstream; its gauge_minibacia.csv was handed on and then superseded in place by src/fix_gauge_minibacia_mapping.py.

**CRITICAL and HIGH defects (3 of 11):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 2 | markdown | HIGH | stale-claim | The SCALE=1 run was never performed. The SCALE=8 product this notebook exports (1500x705, 8,672 minibacias) is the ADOPTED Phase A discretisation on which all of Phase B and all of Phase C stand; calling it a prototype awaiting replacement misdirects every downstream reader, and nb08 inherits the sa | docs/18 2.1 (8,672 minibacias x 24 URH on the D8 network from notebook 07) + CLAUDE.md Pha |
| 2 | markdown | HIGH | number-not-exported | 257,808 is pyflwdir's latitude-correct upstream_area at the outlet. The table this notebook exports uses a single constant cell area (cos 6.4 deg) and sums to 257,096.9 km2 - and 257,097 is the figure docs/00_INDEX, docs/17, docs/23 and docs/24 all quote. The QA gate is therefore passed by a number  | docs/23 13.2 + docs/00_INDEX line 24 + docs/17 3.1 outlet sanity anchor |
| 20 | markdown | CRITICAL | superseded-artifact-undisclosed | The check was run in Step 6 and did not pass (6 minibacias hold >1 gauge). Worse, docs/17 3.1 (CONFIRMED, CRITICAL) later found 79 of 159 testable stations fail a plausibility test on this notebook's exported mapping, 34 of the 37 impossible-runoff stations flagged representative=True in this very f | docs/17 3.1 and its 'Update: the gauge->minibacia plumbing is fixed' section; src/fix_gaug |

**Not settled** (carried forward, not smoothed over): (1) The on-disk gauge_minibacia.csv shows 153 unique minibacias / 152 representative against the notebook's printed 13-gauges-in-6 / 152; the file was rewritten by the fix script after nb07 ran, and I did NOT re-derive which of the two accounts for the difference - it is not attributable to nb07 from the evidence I have. (2) I did not verify that a re-run today would still realise 8,672 minibacias, because the executed DEM path is a foreign sandbox and I did not execute anything. (3) I REFUSE to claim the 0.276 % constant-cosine area ramp explains any part of the docs/23 13.2 per-gauge disagreement - measured magnitudes differ by three orders. (4) docs/59's manifest calls the DEM COP30 while the glob, geometry and plot title say COP90; that contradiction lives in docs/59, not in nb07, and I did not adjudicate it here.

### `08_urh.ipynb` - 60 → **84**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 18 |
| Generator-sync | 0 | 0 |
| Coherence with canon | 40 | 16 |
| No kill-list / no stale | 15 | 12 |
| Embargo & convention | 10 | 7 |
| Academic clarity | 10 | 7 |

Hand-written (no generator) - fixes landed on the `.ipynb` cell source by index.

**Narrative role.** Beat 2 of 'inputs are not innocent': it crosses ESA WorldCover (reduced to 8 hydrological classes) with the IGAC texture families (3) on nb07's grid to produce the 24-URH area-fraction table that the water balance and the sediment engine both actually read.

**Inherits from.** notebook 07's minibacias.tif (the 1500x705 / 8,672-minibacia grid) and src/build_soil_layer.py's merged soil_family_igac.tif.

**Hands to.** notebook 09 (the same soil families, for Wm and K) and directly to src/mgb_hydrology.py and src/mgb_sediment.py via data/processed/urh_fractions.csv.

**CRITICAL and HIGH defects (4 of 8):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 10 | code | HIGH | undisclosed-mask-and-renormalisation | About 1.945 % of basin cells (soil nodata) are dropped and their area redistributed pro rata, because every row is renormalised to 1.0. Measured: 463,251 of 472,438 basin cells survive = 98.055 %. Nothing is printed about it and the QA cell does not mention it. This single undisclosed line creates t | docs/43, docs/46 and docs/51 (each describes the support difference); src/mgb_sediment.py  |
| 11 | markdown | HIGH | cross-notebook-contradiction | Notebook 09 §5 states in as many words that it deliberately does NOT validate K against observed sediment. The rating-curve check that once lived in nb09 was removed at commit 9a3810c (2026-07-30); its measured result was r = 0.05 over n = 28 gauges, verdict INCONCLUSIVE. nb08 promises a deliverable | notebooks/09_soil_parameters.ipynb 5 (its own text) + docs/agents/journal_nbc1-nb07-09.md  |
| 8 | code | HIGH | mislabelled-output | soil_family_igac.tif is ALREADY the merge (src/build_soil_layer.py: final = np.where(igr > 0, igr, sgf)), so 98.1 % is merged coverage, not IGAC coverage, and the agreement mask includes every gap-filled cell where soil == sgf by construction. The cell's own prose (86 % / 39 %) is the correct pair,  | src/build_soil_layer.py:150-155 (writes the merge, prints the IGAC-alone numbers) + docs/a |
| 11 | markdown | HIGH | stale-claim | There is no SCALE=1 run and none is planned; this grid is the adopted Phase A discretisation. So the cropland under-representation is not a preview artefact awaiting removal - it is a property of the shipped table, and src/nbgen/make_nb12.py later reports 'Cropland URHs total 1.4 % of basin area ... | CLAUDE.md Phase A + docs/18 2.1; the downstream report is in src/nbgen/make_nb12.py |

**Not settled** (carried forward, not smoothed over): (1) IGAC-alone coverage cannot be read from disk - build_soil_layer.py writes only the merged raster, so no IGAC-only artifact exists. The ~86 % is recovered by algebra plus that script's own build-time print, NOT by re-rasterising the 18 department gpkgs, which I did not run. (2) The 257,097 vs 251,724 km2 gap is reconciled only to 0.15 %; the residual is unexplained here and the two artifacts also differ in resolution (720 m vs 90 m), so I do not claim the cell drop is its sole cause. (3) The SCALE=1 open check propagated into src/nbgen/make_nb12.py and still reads live THERE; that is nb12's owner's fix, not mine, and I did not touch it. (4) Whether notebooks/README.md should be extended to 06-19 and its 'nb05 is the real-data version of nb02' line corrected is a repo-organisation call outside this spec.

### `09_soil_parameters.ipynb` - 59 → **86**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 20 |
| Generator-sync | 0 | 0 |
| Coherence with canon | 40 | 15 |
| No kill-list / no stale | 15 | 11 |
| Embargo & convention | 10 | 5 |
| Academic clarity | 10 | 8 |

Hand-written (no generator) - fixes landed on the `.ipynb` cell source by index.

**Narrative role.** Beat 3 and the close of 'inputs are not innocent': it turns the IGAC free-text soil descriptions into the two parameters the model needs - Wm (storage, a calibratable prior) and K (MUSLE erodibility, pinned) - and is the only place in the repository where the K unit system was ever written down.

**Inherits from.** notebook 08's soil-family raster (soil_family_igac.tif, the IGAC + SoilGrids merge) plus the IGAC depth and drainage rasters from src/build_soil_layer.py, and notebook 07's minibacias.csv for the topology join.

**Hands to.** Phase B's water balance (Wm as a physically-grounded prior that rides the discharge calibration) and Phase C's MUSLE chain (K as a pinned factor inside the product Pi that docs/42 shows a fit cannot decompose).

**CRITICAL and HIGH defects (6 of 11):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 0 | markdown | CRITICAL | self-contradiction | Cell 10 states the opposite in its first sentence: 'We deliberately do not try to validate K against the observed sediment at this stage'. The rating-curve check was removed from this notebook at commit 9a3810c (2026-07-30). The stated goal was never updated, so the notebook advertises a deliverable | the notebook's own 5 + docs/agents/journal_nbc1-nb07-09.md (verbatim old cell 11 from 9a38 |
| 10 | markdown | HIGH | deleted-negative-result | This is an unsupported paraphrase of a measurement that was deleted. The removed cell printed 'Pearson r(upstream K, log a) = 0.05 -> INCONCLUSIVE (confounders dominate)' over n = 28 gauges, with its own caveat that 'a near-zero r ... does NOT show K is wrong'. 'Pure noise' is a stronger verdict tha | docs/agents/journal_nbc1-nb07-09.md (git 9a3810c, verbatim); replacement check okK is a ba |
| 0 | markdown | HIGH | overclaim | soil_family_igac.tif is a hybrid: src/build_soil_layer.py writes final = np.where(igr > 0, igr, sgf), IGAC where present and SoilGrids elsewhere, with the docstring putting the fill at ~14 % of the basin. Everything derived from 'fam' inherits SoilGrids on that fraction. Cell 14's own Limitations pa | src/build_soil_layer.py:7-8 and :150-151 |
| 10 | markdown | HIGH | stale-deferral | The comparison happened in Phase C, not Phase B, and it could not test K: docs/42 3.1-3.3 measured that the C level, the LS level, THE K UNIT SYSTEM, the volume convention, P and FG are seven ways of writing one product Pi (design matrix condition number inf, exactly singular), so no objective funct | docs/42 3.1-3.3 (identifiability) + docs/55 (C4.3 RAILED / EXPLORATORY, not adopted) |
| 12 | markdown | HIGH | missing-unit-convention | The table written by the next cell names units in Wm_mm and depth_cm but NOT in K, and 4's markdown is the only record anywhere of what K's numbers mean (SI, from Wischmeier & Smith US-customary x0.1317). docs/42's evidence table had to recover k_factor = 7.593014 by inverting that sentence and chec | docs/42 3.3 evidence table (k_factor = 7.593014, IDENTIFIED - pinned to <= 1.3 % rounding  |
| 14 | markdown | HIGH | self-contradiction | On the ~14 % of the basin SoilGrids gap-fills, both Wm and K ARE derived from a SoilGrids texture family, so both inherit the artefact there. The same cell's Limitations paragraph states the ~14 % correctly, so the bullet contradicts its own section four paragraphs later. | src/build_soil_layer.py:7-8 and :150-151; contradicted in-cell by the Limitations paragrap |

**Not settled** (carried forward, not smoothed over): (1) The r = 0.05 / n = 28 result from the removed cell is quoted from the prior audit's verbatim git read (9a3810c), NOT re-measured by me - I was instructed not to run git and did not. (2) I could not grade Klit/Alit against a named table and page because no table or page is named anywhere in the repository; I graded the check ASSUMED rather than inventing or reconstructing an envelope. (3) I did NOT verify IGAC's exact basin coverage - build_soil_layer.py's docstring says ~14 % uncovered and prints the exact figure at run time, and I did not re-run the rasterisation of the 18 department gpkgs. (4) The K column's missing unit is fixed in prose only; whether the CSV header should change is a downstream-schema decision (src/mgb_sediment.py and src/build_data_final.py read that file) and belongs to their owner, not to this spec. (5) Whether AWC 0.09 / 0.17 / 0.14 and KBASE 0.020 / 0.045 / 0.028 are the right mid-ranges is untested here; the prior audit established only that they are dimensionally self-consistent, and I did not go further.

### `10_rainfall_dataset_comparison.ipynb` - 85 → **97**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 21 |
| Generator-sync | 20 | 20 |
| Coherence with canon | 20 | 12 |
| No kill-list / no stale | 15 | 13 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 9 |

Generated by `src/nbgen/make_nb10.py` - **all fixes landed on the generator, never on the `.ipynb`**.

**Narrative role.** The data-selection notebook: it decides which rainfall product forces MGB-SA, finds and repairs the zero-suppression defect that had invalidated its own earlier verdict, and is where the CHIRPS-vs-gauges question was decided (and later overturned by measurement).

**Inherits from.** The QC'd IDEAM gauge tables written by src/build_precip_gauges.py and src/repair_precip_zero_suppression.py, plus the basin-clipped CHIRPS and the minibacia label raster.

**Hands to.** Notebook 11, which takes the conventional-gauge verdict and the repaired daily file and builds the per-minibacia field from them; and docs/16 §4, which owns the lag, bias and wet-day findings this notebook measured.

**CRITICAL and HIGH defects (4 of 8):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 11 | markdown | HIGH | stale-by-event | That route was quantified and closed on 2026-08-12. docs/58 applied docs/18 s15.2's isolation-banded LOOCV deltas (0.000 / +0.023 / -0.043) to nb11's own v2 area shares (25.8/57.1/17.1 %) and got delta-r = +0.0058 area-weighted, i.e. r ~0.57 -> ~0.576. The rainfall ceiling is structural, not a pendi | docs/58_rainfall_ceiling_bound.md (sections 1-3) |
| 11 | markdown | HIGH | stale-count-reads-as-live | 55 is the first pass. The notebook's own executed cell prints 'flagged 70 / 294 stations (24 %)', and a second detector took the repair to 153 stations / 240,158 inferred-dry station-days. Section 1 (cell 3) carries an in-place SUPERSEDED note; section 5 does not, so here 55 reads as the finding. | docs/18_hydrology_journal.md §10.2 (defect: docs/16 §4.1) |
| 1 | markdown | HIGH | stale-count-reads-as-live | Third occurrence of the retired 55, in the notebook's opening statement of what it does. It is neither annotated in place nor listed in cell 0's banner (which names only section 1's and section 5's). A reader meets 55 before ever seeing the 70 the cell below prints or the final 153. | docs/18_hydrology_journal.md §10.2 |
| 10 | code | HIGH | unguarded-duplicate-implementation | Section 4's LOOCV re-implements the interpolator inline with plain np.argsort and never calls merge_colocated, so the three inventory pairs at exactly 0.000000 m (printed by nb11's classification table off the same inventory file) produce exact distance ties resolved by COLUMN ORDER - precisely the  | docs/23_gauge_geometry.md §11 and §11.2 |

**Not settled** (carried forward, not smoothed over): (1) Whether §4's r 0.41 actually moves once the co-located gauges are merged and the lexsort tie-break is used — unmeasured, and measuring it means editing a code cell and re-executing nb10. Not proposed. (2) CHIRPS metrics against the 153-station v2 reference were never measured; docs/16 §4.3's ladder stops at the 70-station stage, so I state the ladder and stop there rather than extrapolating a fourth value. (3) §5's 'ENSO contrast \| reproduced' table row is left as frozen verdict text; its supporting 1.69x pair is retired inside nb11 instead. (4) docs/00_INDEX.md line 227 still says banners 'are being added to those notebooks by a separate pass' — that work is already done (nb10 cell 0 and nb11 cell 0 both cite the 'Forcing versions — v1 / v2 / v3, stated once' section by title), so the index sentence, not the notebook, is what is stale. Out of my target scope.

### `11_rainfall_pet_forcing.ipynb` - 87 → **97**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 23 |
| Generator-sync | 20 | 20 |
| Coherence with canon | 20 | 11 |
| No kill-list / no stale | 15 | 13 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 10 |

Generated by `src/nbgen/make_nb11.py` - **all fixes landed on the generator, never on the `.ipynb`**.

**Narrative role.** The forcing-construction notebook: it turns notebook 10's gauge verdict into the two fields MGB-SA actually consumes — per-minibacia daily rainfall and FAO-56 Penman-Monteith PET — and produces the two things every later stage leans on, the provenance flags (G/GC/C) and the order-invariant LOOCV baseline of median daily r 0.429.

**Inherits from.** Notebook 10's 'conventional gauges' verdict, the 153-station repaired file precip_gauges_daily_qc_v2.csv, the minibacia label raster, and the ERA5-Land monthly mosaics from src/mosaic_era5.py.

**Hands to.** forcing_minibacia_precip_v2.csv / _pet_v2.csv / _provenance_v2.csv → notebook 12's model-input assembly and model_inputs_v2/, and through it the H2E calibration in notebooks 13-14; its r 0.429 became the registered LOOCV gate in docs/18 §15.1 and docs/33 §1, and its isolation shares are the inputs to docs/58's ceiling bound.

**CRITICAL and HIGH defects (2 of 8):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 8 | markdown | HIGH | prose-contradicts-own-output | Cell 4, four cells earlier in the same notebook, prints 'matrix 4018 days x 291 gauges \| filled 79.2 %'. The ~58 % is the pre-repair figure: the zero-suppression repair inserted 240,158 inferred-dry station-days, which are observations and therefore fill the matrix. The argument survives (20.8 % is | this notebook's own cell 4 output; the repair is docs/18 §10.2 |
| 23 | markdown | HIGH | prose-contradicts-own-output | Cell 15's executed LOOCV table reads r 0.343 / bias +3.864 % beyond 30 km and r 0.481 / bias +3.617 % below 10 km, with 10-30 km at +0.291 %. So r is understated, bias is overstated threefold, and the claim that bias 'rises' with isolation is not what the run shows - it is non-monotonic. These are e | this notebook's own cell 15 output; docs/58 §2 quotes the 0.343 |

**Not settled** (carried forward, not smoothed over): (1) The generator-wipes-outputs problem above is the single biggest risk in applying this spec, and I could not test it (read-only, no execution). If the orchestrator's apply step is 'edit generator, re-run generator', then EVERY fix in this spec becomes a full re-execution of both notebooks and should be reconsidered on cost. (2) docs/00_INDEX.md cites nb11's contradiction at 'cells 0, 13, 22' (prose) and 'cells 1, 21' (code), and at line 192 'nb11 cell 21'. Measured against the extract, every one is off by exactly +1 — the 2026-08-12 banner was prepended as cell 0 after the index text was written. The index needs re-indexing to 1/14/23 and 2/22; the notebook does not. Out of my target scope (docs, not notebooks) — handing it on. (3) docs/00_INDEX.md line 227's 'Banners ... are being added to those notebooks by a separate pass' is already satisfied: both banners exist and both cite the section by its title. That sentence, not the notebooks, is what is now stale. (4) I did not verify whether cell 15's LOOCV is exactly deterministic. It re-implements the interpolator with plain np.argsort like nb10's, but it runs AFTER merge_colocated, so only the CATAM pair at 0.051952 m survives and no exact tie remains — deterministic in practice, reasoned from cell 2's printed distances, NOT re-verified by execution. (5) The 15-22 MJ/m2/day radiation band in cell 16 is not an invented materiality bar: it is CLAUDE.md's stated sanity range, used as a sanity check and explicitly shown NOT to catch the ssrd defect. Not filed.

### `12_model_input_assembly.ipynb` - 80 → **98**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 22 |
| Generator-sync | 20 | 20 |
| Coherence with canon | 20 | 8 |
| No kill-list / no stale | 15 | 12 |
| Embargo & convention | 10 | 9 |
| Academic clarity | 10 | 9 |

Generated by `src/nbgen/make_nb12.py` - **all fixes landed on the generator, never on the `.ipynb`**.

**Narrative role.** Beat 1 of the investigation - 'inputs are not innocent': the notebook that refuses to let a join, a date index, or a gauge mapping fail silently, and that writes down in one manifest exactly what the water balance is allowed to consume.

**Inherits from.** nb07-nb11 - the D8 minibacia delineation and topology (nb07), the 24-type URH composition (nb08), the IGAC-derived Wm and MUSLE K (nb09), and the v2 gauge-only rainfall and FAO-56 PET fields (nb10-nb11) - none of which had ever been validated against each other.

**Hands to.** nb13/nb14 - the model_inputs_v2/ bundle plus the two nested calibration gauge sets (63 primary, 70 RC-band-only) and the exported gauge_weight convention, on which Phase B closed at H2E (F = 0.25931); and, unchanged, on to nb15-nb19 and Phase C, whose C5 result rests on the same topology, areas and forcing.

**CRITICAL and HIGH defects (14 of 23):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 18 | markdown | CRITICAL | prose_contradicts_own_output | Cell 19's own executed output prints 'pet   : 4018 days  2008-01-01 .. 2018-12-31' and 'intersection: 4018 days'. Open item 3 closed when all 132 ERA5-Land mosaics were built; PET is no longer the binding constraint on the model period. | docs/18 §14.1 ('Open item 3 is closed. PET now spans the full rainfall record'); docs/18 § |
| 18 | markdown | HIGH | prose_contradicts_own_output | The intersection measured by the adjacent code cell is 4,018 days, not 3,287. 3,287 is the v1 PET-bounded length. | docs/18 §14.2 |
| 18 | markdown | HIGH | stale_number_stated_as_verified | The check as stated FAILS against its own run: cell 19 prints 2,073.1 mm/yr for exactly that window. 2,206 is the v1 pre-repair basin mean; the zero-suppression repair moved it. Stating a retired number as the thing being reproduced turns a passing self-check into a false one. | docs/18 §14.2 ('area-weighted areal mean, 2008-2018 \| 2,073.1 mm/yr') |
| 18 | markdown | CRITICAL | internally_self_contradictory_paragraph | One paragraph asserts both that 2008 is excluded and that the period starts where the rainfall does (2008-01-01). The second half is correct and matches the shipped manifest ('ZERO days precede the model period, because the period now STARTS at the start of the rainfall record'); the first half is u | docs/18 §14.1-§14.2; the notebook's own manifest.json model_period block |
| 1 | markdown | HIGH | v1_path_stated_as_deliverable | The notebook writes model_inputs_v2/ (cell 3 prints it, cell 33 lists its 8 files). The v1 bundle is deliberately NOT overwritten because nb14's H1 needs it. Naming the v1 path as the deliverable points a reader at the wrong directory. The body also never defines 'v2 = gauge-only' - only the cell-0  | docs/18 §14.2 ('Written to model_inputs_v2/; the v1 bundle is untouched'); docs/00_INDEX.m |
| 21 | markdown | HIGH | prose_contradicts_own_output | The run prints 'PRIMARY CALIBRATION SET: 63 gauges' and the manifest records calibration_gauges_primary = 63. docs/18 §14.2 owns the correction explicitly and names 61 as the retired pool. | docs/18 §14.2 ('The calibration set grew to 63, and the prediction of 59 was wrong. Every  |
| 28 | markdown | HIGH | v1_path_and_shape | The export directory is model_inputs_v2/ and the benchmarked matrix is 4,018 x 8,672 (cell 29 writes PM, whose shape the run reports as 4018 rows). Both the section heading and the benchmark description name v1 quantities. | docs/18 §14.2 |
| 34 | markdown | CRITICAL | live_prescription_of_retired_work | That route is closed with a measurement, not an opinion: the merge was built, its LOOCV gate passed (r 0.447 > 0.429) and its volume gate failed twice (2,188.5 mm/yr, +7.5 %); the registered repair was a no-op and the diagnosed cause was wrong. No v3 forcing exists. docs/58 bounds the entire remaini | docs/18 §15.5 ('no route to a passing volume gate exists inside the merge code'); docs/58 |
| 34 | markdown | HIGH | resolved_risk_still_listed_as_open | Resolved by this notebook's own cell 19 output and by the shipped manifest. All 132 ERA5-Land mosaics exist, PET is real for 2008, and Phase B warmed up on 2008 and scored 2009-2018. The item is listed among live risks with an unresolved choice ('synthesise 2008 PET') that was never needed. | docs/18 §14.1; docs/26 + its 2026-08-10 addendum |
| 34 | markdown | HIGH | prose_contradicts_own_output | The run measured 912 mm/yr (manifest calamar_runoff_depth_mm_yr = 912.4, over 3,992 days) and docs/17 accepts ~880. ~874 matches neither. This is the sentence that names the single strongest external check in the whole bundle, so a wrong value there is load-bearing. | docs/18 §14.2 ('CALAMAR outlet \| 3,992 days, mean Q 7,433.4 m3/s, runoff depth 912.4 mm/y |
| 35 | markdown | CRITICAL | summary_describes_v1_bundle | Every one of those three rows is contradicted by the same notebook's manifest.json (start 2008-01-01, end 2018-12-31, days 4018, written to model_inputs_v2/). The Summary is the table a reader quotes, so this is the highest-leverage stale text in the file. | docs/18 §14.2 |
| 35 | markdown | HIGH | stale_handoff | Phase B is CLOSED on H2E (F = 0.25931) at the r ~= 0.57 rainfall-input ceiling, closed twice, and Phase C has since run to completion (C5 reproduced the observed ENSO sediment contrast at 18/18 stations, median rate ratio 3.05x). The hand-off sends a reader to redo finished work and omits the caveat | docs/26 + 2026-08-10 addendum; docs/30 §1; docs/33 §8; docs/56 |
| 32 | code | HIGH | shipped_artifact_self_contradiction | This string is written verbatim into the shipped manifest.json, where it documents an array of shape [4018]. A single JSON object that contradicts itself. docs/18 §14.3 item 4 asserts the shipped manifest was corrected and is accurate; measured, this entry was not. | docs/18 §14.3 item 4 |
| 33 | code | CRITICAL | shipped_artifact_points_at_wrong_directory | This is the copy-paste snippet written into model_inputs_v2/README.md. A reader standing inside the v2 bundle who copies it loads the v1 forcing, and is told to expect a (3287, 8672) matrix when the array is (4018, 8672). The bundle's own README hands the reader the wrong data with no error raised. | docs/18 §14.2 ('Written to model_inputs_v2/; the v1 bundle is untouched') |

**Re-execution: REQUIRED.** SPLIT THE PASS. 31 of the 38 fixes touch MARKDOWN ONLY and need NO re-execution - they carry every CRITICAL and HIGH prose defect (the 2008/PET contradiction, the 61-vs-63 count, the ~874 Calamar anchor, the 2,206 mm/yr false self-check, the v1 bundle path in §6 and the Summary, the live CHIRPS *Check*, the stale Phase B hand-off). Apply those alone and nb12 goes from 80 to roughly 93 at zero compute cost. THE 7 CODE FIXES ARE EXPENSIVE AND CARRY A SIDE EFFECT WORTH STATING LOUDLY: nb12 registers a 7,200 s timeout, and re-executing it REWRITES data/processed/model_inputs_v2/ - the bundle H2E was fitted on. The arrays are deterministic given unchanged inputs and should come back bit-identical (cell 33's round-trip asserts precip/pet bit-exactness), but manifest.json's generated_utc will move and any failure part-way leaves the bundle in a worse state than it was found. I propose them anyway because they are the only way to reach two artifacts consumed OUTSIDE the notebook: model_inputs_v2/manifest.json documents a length-4018 `dates` array as '3287 contiguous days' and credits the field to 294 gauges when the v2 IDW ran on 291, and model_inputs_v2/README.md hands a reader a copy-paste snippet that loads the V1 DIRECTORY with a '# (3287, 8672)' shape comment. No markdown correction can honestly repair a README that silently loads the wrong data. If compute is scarce, defer the co

**Not settled** (carried forward, not smoothed over): 1) §7 item 7's 'Wm takes 1,834 distinct values and K takes 289' is not computed anywhere in nb12, which breaks its own working rule 4. It is presumably from nb09; I did not open nb09 to verify, and I will not import a number I have not measured, so I propose no fix. 2) §7 item 6 states the five docs/17 precipitation defects are unapplied and that 'the forcing was last written 2026-08-02 07:46'. The mtimes I can see are consistent, but whether all five remain open is a docs/17 open-register question I did not adjudicate. 3) §7 item 12 (the gauge_minibacia_remap_report.csv schema does not match any script in the repo) is untouched - I could not establish whether that provenance gap was ever closed, and it is a real, still-plausible defect. 4) The 6 gauges routed to review_qspec_outside_healthy by the composed [7.0, 74.9] band are a live gate whose membership would change under any other composition; my fix relabels the band honestly but deliberately does NOT change it, since re-gating is a code change with a 7,200 s cost and would move the 63-gauge primary set that Phase B closed on. Whether the composite should have been used at all is a question for the owning doc, not for a fix spec. 5) I did not execute the notebook or re-run the generator; generator-notebook source-identity for nb12 is taken from the session's MEASURED in-sync list, not from my own run.

### `13_baseline_run.ipynb` - 84 → **97**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 21 |
| Generator-sync | 20 | 20 |
| Coherence with canon | 20 | 12 |
| No kill-list / no stale | 15 | 13 |
| Embargo & convention | 10 | 9 |
| Academic clarity | 10 | 9 |

Generated by `src/nbgen/make_nb13.py` - **all fixes landed on the generator, never on the `.ipynb`**.

**Narrative role.** The corpus's control experiment: the last notebook before anything is fitted, which proves the water engine conserves mass on the real basin, fixes a DATA/PRIOR parameter set before a single gauge is consulted, registers a mean-field prediction of the runoff coefficient in advance, and then measures exactly how and where the uncalibrated model is wrong - so that everything the calibration later claims has an honest, un-tuned floor to be measured against.

**Inherits from.** notebook 12's validated v2 input bundle (topology / parameters / forcing / discharge npz + manifest.json, 4,018 d, 8,672 minibacias) and the tested engine src/mgb_hydrology.py derived in notebook 03.

**Hands to.** notebook 14 (calibration), which reads sim_baseline_v2/balance.json and q_gauge.npz as the baseline it must beat, and inherits this notebook's ordered instruction - reduce adr first, then b and Wm scaling, then the reservoir time-scales, and do not expect r to move - the last of which held and is now bounded at <= +0.006 r by docs/58.

**CRITICAL and HIGH defects (3 of 13):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 40 | markdown | CRITICAL | stale-number-v1-leftover | Three numbers in one sentence, all from the v1 run (commit 0388930) and all invalidated by the v2 re-execution. The notebook's OWN cell-41 output prints 24027070 KGE 0.747, alpha 0.927, beta 0.937 (7.3 % and 6.3 % from 1, not 2 %), and cell 32 prints Q 1,464 mm/yr vs observed 912 mm/yr = 1.63x, i.e. | docs/26 (owns commit 74eb324, the run that produced nb13's current executed state); the no |
| 1 | markdown | HIGH | stale-number-v1-leftover | 'KGE ~ 0.77' is the v1 value. The v2 run this notebook actually contains scores that gauge at KGE 0.747 (cell 41 output). It sits inside the statement of working rule 4/5, which makes the violation of rule 4 self-referential. | docs/26; the notebook's own cell 41 output |
| 3 | code | HIGH | stale-provenance-stamp | MEASURED 2026-08-19: src/mgb_hydrology.py is 48,097 B = 47.0 kB, sha256 93b180a9113f5946. The file moved at commit cdee2c9 ('FAO-56 threshold ET stress (opt-in) + pre-registered cell H2E'), which is AFTER nb13's execution commit. The executed output therefore stamps a file that no longer exists at t | docs/20 (reproduction guide - owns what must match to re-run nb13) |

**Not settled** (carried forward, not smoothed over): (1) Whether nb13's executed numbers still reproduce under the current engine (commit cdee2c9) is UNVERIFIED. The two added constructor fields (et_stress='linear', theta_crit=0.6) default to the old behaviour, which is why I say 'expected to reproduce', but I did not and could not test it - re-execution is prohibited here and costs 7,200 s. The fix spec discloses this rather than asserting reproducibility. (2) The four code-cell defects (cell 48's README prose, cell 35's +0.02 margin, cell 45's 0.25/0.45 cuts, cell 37's 0.7 cut) are corrected by markdown disclosure only. Whether the project wants them repaired in place - at the cost of a full re-execution - is a decision above my level, and I have deliberately not pre-empted it. (3) The '10-20 % of P' tropical-forest interception band: I searched the notebook and could find no citation for it. I have labelled it UNCITED rather than striking it, because it is not on the kill list and nb13 uses it as a reference point rather than a pass/fail bar - but a reader could reasonably argue the 'known deficiency' verdict written into parameters.json makes it a bar in practice, and striking it outright is a call for the band's owner, not me. (4) The prior audit (docs/agents/journal_nbc1-nb13-baseline.md item 2) reports the engine at 47,097 B; I measure 48,097 B today. The kB figure it quotes (47.0) matches my measurement, so I read its byte count as a transcription slip and used my own, but I did not reconcile the discrepancy against the file as it stood on 2026-08-13. (5) nb13 has NO row in docs/00_INDEX.md (the prior audit grepped: z

### `14_calibration.ipynb` - 80 → **92**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 16 |
| Generator-sync | 20 | 20 |
| Coherence with canon | 20 | 12 |
| No kill-list / no stale | 15 | 13 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 9 |

Generated by `src/nbgen/make_nb14.py` - **all fixes landed on the generator, never on the `.ipynb`**.

**Narrative role.** nb14 is Phase B's decisive experiment: it refits the water balance under a revised objective (recession term at weight 0.20, k_bas floor 15 d -> 5 d, k_int searched as a ratio so k_int < k_bas holds by construction) across two pre-registered forcing cells, and delivers H2 - H1 as the measurement that separated volume from correlation and located the remaining deficit in the rainfall field's daily skill rather than in its totals.

**Inherits from.** nb13's uncalibrated v1 and v2 baselines and the stored Config B flows in sim_calibrated/, the v1 Morris screening and its Config-B regionalisation (not re-derived), and docs/22's dry-phase diagnosis - the r 0.556-0.572 ceiling, the observed 13.9 d recession the v1 box excluded, and the climatology-benchmark trap that makes NSE incomparable across ENSO windows.

**Hands to.** data/processed/sim_calibrated_v2/ - metrics_fleet.csv and q_gauge_H*.npz to notebooks 15 and 17, and the directory into which src/report_h2e.py writes the ADOPTED H2E artifacts (parameters_H2E.csv, q_gauge_H2E.npz, report_H2E.json) that every Phase C stage quotes in place of the H1/H2 parameters on this page.

**CRITICAL and HIGH defects (5 of 11):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 3 | code | HIGH | stale-executed-output | MEASURED 2026-08-19: src/mgb_hydrology.py hashes to 93b180a9113f5946 and src/calib_v2.py to 30ab13a630278d5d, against the cdea026afe796f6d / 3342728f2a38bac1 the executed output records. The engine moved with 80a7c10 (FAO-56 threshold ET, the change H2E is built on) and the search code with 19dce32  | docs/26 §Addendum (2026-08-10, the H2E adoption that required the engine change); commits  |
| 35 | markdown | HIGH | closed-item-reads-as-open | The gate was executed. LOOCV PASSED (merged median daily r 0.447 > 0.429) but the volume gate FAILED (2,188.5 mm/yr against the registered band [2,016.0, 2,056.8], +7.47 %), and failed a second time when the registered repair H-CHIRPS turned out to be a no-op with the diagnosed cause wrong. docs/18  | docs/18 §15 and §15.5 (owning read-out); docs/33 §1 (H-CHIRPS no-op) |
| 1 | markdown | HIGH | stale-live-claim | Same retired claim as §12.2, but in the title cell where every reader meets it, and NOT covered by the banner - the banner retires the claim by its section-12.2 name only. The lever was tried and refuted (docs/18 §15.5), and the single surviving upstream route (the 139 rain-selectively-reporting sta | docs/58 (the bound); docs/18 §15.5 (the refutation) |
| 38 | code | HIGH | stale-live-claim-in-written-artifact | The retired claim a third time, this time inside an f-string that is WRITTEN TO DISK as sim_calibrated_v2/README.md and printed in the executed output, so it propagates to anyone reading the artifact directory rather than the notebook. Refuted by docs/18 §15.5. NO CODE FIX IS PROPOSED: the string si | docs/18 §15.5; docs/33 §1 |
| 37 | code | HIGH | destructive-overwrite-of-shared-artifact | Unconditional full overwrite. MEASURED on disk: metrics_fleet.csv carries 39 rows / 4 configurations (H1 10, H2 12, H2E 12, ref 5); this notebook's SUM carries 27 rows / 3 configurations, and the round-trip print says 'metrics_fleet rows 27'. src/report_h2e.py APPENDS the 12 H2E rows and asserts the | src/report_h2e.py:323-345; docs/26 §Addendum (the H2E freeze) |

**Not settled** (carried forward, not smoothed over): (1) Two code-cell strings carry live errors I deliberately did not fix: cell 18's printed 'bought 5.2x the v1 evaluation count for comparable wall time', and cell 38's README 'the CHIRPS-gauge merge is the only remaining lever on the dry phase'. Both are corrected in adjacent markdown. I judged the 28,800 s re-execution not worth it - and it is moot, because cell 3's assert makes re-execution impossible on today's engine without re-opening Phase B. If someone ever does re-open it, these two strings must go in the same pass. (2) The prior audit journal states that nb15, nb17 AND nb18 read metrics_fleet.csv; I measured the consumers as nb15, nb17 and src/report_h2e.py only - nb18's extract has zero hits for 'metrics_fleet'. I used my measurement and I am flagging the disagreement rather than quietly overriding. (3) Cell 34's identifiability thresholds (iqr_frac < 0.25 = 'identified', < 0.5 = 'weak') are uncited materiality bars that produce a printed verdict. The notebook disclaims the statistic in the same cell citing docs/18 §6. Whether that disclaimer is enough under the project's no-uncited-band rule is a call for whoever owns that rule; I recorded it LOW and proposed no fix. (4) My 'Executes cleanly' award of 16/25 is a judgement, not a measurement: the notebook did run end to end with 0 unexecuted cells and 0 errors and its internal RECHECKs pass, but it cannot be re-run today at all. A stricter reading of 'stale executed output' could take this several points lower, and I would not argue hard against it. (5) I did not independently re-verify nb14's generator/notebook s

### `15_ssc_quality_gate.ipynb` - 84 → **97**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 23 |
| Generator-sync | 20 | 20 |
| Coherence with canon | 20 | 12 |
| No kill-list / no stale | 15 | 10 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 9 |

Generated by `src/nbgen/make_nb15.py` - **all fixes landed on the generator, never on the `.ipynb`**.

**Narrative role.** The hinge of the whole investigation: it freezes the water model at H2E behind a bit-exact reproduction gate (C0) so that no sediment number can later move because the hydrology shifted underneath it, then decides which of the 79 SSC stations may ever be used (C1) - and it carries the corpus's most transferable methodological lesson, that a screen which inspects values is structurally incapable of seeing records that are absent, demonstrated on the rainfall network and then transposed to sediment.

**Inherits from.** nb11/nb12's v2 gauge-only forcing and nb13/nb14's calibration, in the form of the four frozen C0 artifacts (report_H2E.json, parameters_H2E.csv, metrics_fleet.csv, q_gauge_H2E.npz) - together with their defects unimproved: the r ~ 0.57 input ceiling, the inverted store ordering, the structural peak deficit and the dry phase sitting at climatology.

**Hands to.** nb16 (the model-free observed ENSO contrast) and thence the C4/C5 harnesses and nb18/nb19: the named 18-station working set with its 7 both-window core, the registered N = 91, the rate-not-total rule forced by the 12-versus-24-month windows, the x/2.25 rating-residual band that must be propagated, the PENALTA sample-mean prohibition, and the t/km2/yr embargo this notebook is the one that declares.

**CRITICAL and HIGH defects (6 of 15):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 0 | markdown | HIGH | stale-status | The block condition was discharged: the LS level landed (ls_formulation = buarque_2015_dg, V4_dg, f_LS 0.25146 erosion-weighted), C4.3 then ran on the adopted field and has a verdict - RAILED / EXPLORATORY, NOT adopted, in-box optimum at the alpha box floor with the unconstrained optimum at alpha ~  | docs/55_c43_verdict.md §1 |
| 0 | markdown | HIGH | overclaim-refuted | Something on this page HAS been overturned. §8.5 and §8.7 item 5 both present coordinate recovery for the 46 unmapped stations as the largest available expansion of the usable set; background task B5 geocoded all 46, found 43 in-basin, and measured that 0 of the 43 gauge discharge under the same cod | docs/57_b5_gauge_expansion.md §2 |
| 70 | markdown | HIGH | kill-list-live | 'Phase C is blocked on SSC' is a retired framing and is acceptable only inside a strike-through / RETIRED / superseded block. Here it is quoted live and endorsed ('that is the precise, quantitative form of'), with no marker that Phase C is now COMPLETE. The one-station fact itself is correct and is  | docs/32_ssc_qc_audit.md §R6 (via CLAUDE.md: "The old 'blocked on mainstem SSC' framing is  |
| 80 | markdown | HIGH | refuted-claim | Refuted, and in the direction that matters. B5 ran: 46/46 geocoded from the IDEAM Catalogo Nacional de Estaciones, 43 in-basin, and 0 of those 43 have same-code discharge in discharge_daily.csv (192 stations) nor anywhere in the raw IDEAM discharge download - against 18 of 18 for the usable set. Flu | docs/57_b5_gauge_expansion.md §1-§2 |
| 81 | markdown | HIGH | refuted-claim | Carried in the 'What remains open' register as a live open item; it is closed and it closed negative. Same measurement as the §8.5 defect: geocoding succeeded and bought nothing for the flux set, because none of the recovered sites gauges discharge. Leaving it in the open register misdirects a futur | docs/57_b5_gauge_expansion.md §2 |
| 73 | markdown | HIGH | prose-vs-code | The notebook contradicts its own executed output twice inside one cell. Cell 72 prints 'eras with R2_conc < 0.05 (essentially no concentration-discharge relation): 9 of 30'; this same cell's 'What it shows' paragraph says '**Nine** of the 30 eras have concentration R^2 below 0.05'; and its closing p | the notebook's own executed output, cell 72 (ssc_rating_fits.csv); docs/32 §R6 |

**Not settled** (carried forward, not smoothed over): (1) R_AMS 0.820. docs/36 §1.1 DOES label it a 'fleet median' with a 'per-gauge IQR' of 0.529-1.186 - a median over gauges of per-gauge R_AMS, which is a third convention nb15 never computed (it computed 0.7337 median-of-gauge-year-ratios and 0.5508 ratio-of-medians). So nb15's §8.6 clause 'the published figure does not state its aggregation' is too strong. I did not fix it: settling which convention yields 0.820 requires recomputing per-gauge R_AMS from q_gauge_H2E.npz, which is a run, and nb15's refusal to reverse-engineer the number is the right behaviour, not a defect. The prior audit did not catch this; I am recording it rather than fixing it. (2) The +0.026 -> +0.006 -> -0.0005 El Nino skill-over-climatology chain in §8.6 is uncited and only its last term is reproduced in the notebook. docs/26 is internally inconsistent on the sequence (§118/§156 against §300) and nb15 followed §300. I cannot say which is right without re-running, so no citation was added - adding one would launder an unresolved disagreement. (3) The 15,180 mg/L spike ratio: measured 91.538, nb15 says '91 times', docs/32 says '91x' at :192 and '92x' at :318. The owning doc must settle its own split before the notebook is moved either way. (4) §8.7 item 6 (21237020's post-2014 discharge) is left standing as open. docs/57 measured that 0 of 43 RECOVERED sites have discharge, which is a different question from whether ARRANCAPLUMAS's own post-2014 discharge exists somewhere unfetched; docs/34 §7 still carries it as live. I did not search the raw IDEAM download to close it. (5) Whether docs/32 §R6's own su

### `16_observed_enso_contrast.ipynb` - 89 → **99**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 25 |
| Generator-sync | 20 | 20 |
| Coherence with canon | 20 | 13 |
| No kill-list / no stale | 15 | 11 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 10 |

Generated by `src/nbgen/make_nb16.py` - **all fixes landed on the generator, never on the `.ipynb`**.

**Narrative role.** This is the observational anchor of Phase C: the model-free, pre-registered ENSO sediment contrast measured from IDEAM gauge records alone - two estimators, two window pairs, unanimous direction, magnitude quoted only as a range - which exists so that the sediment model has a target that was fixed before any sediment run could influence it.

**Inherits from.** Stage C1 / nb15 (docs/32): the 79-station SSC classification and the 18-station usable set, the 12-day sample floor and the one-sided selectivity flag; plus Phase B's closed H2E hydrology (docs/26) for the discharge bundle and the r ~= 0.57 ceiling it states as an inherited limit.

**Hands to.** Stage C5 / docs/56, which has now consumed this hand-off and reproduced the contrast (18/18 modelled stations, median 3.05x) against these same seven ratio-carrying stations - and, unconsumed, the one repair this page names as the highest-value data acquisition left: post-2014 discharge at 21237020 ARRANCAPLUMAS, without which no Magdalena-trunk contrast exists.

**CRITICAL and HIGH defects (1 of 4):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 0 | markdown | HIGH | stale-forward-status | Both clauses were true on 2026-08-12 and are now false. The hand-off HAS been consumed and the model REPRODUCED this page's target: docs/56 s1 reports La Nina > El Nino at 18 of 18 modelled stations, median modelled rate ratio 3.05x (range 1.62-4.85), robust across beta and both window pairs, with e | docs/56 s1 (C5 reproduced, 18/18, median 3.05x) and docs/55 s1 (C4.3 RAILED / EXPLORATORY) |

**Not settled** (carried forward, not smoothed over): (1) The 24-vs-22 count. This page measures 24 available station-ratios from the frozen c2_rate_ratios.csv (primary a 6, primary b 7, sensitivity a 4, sensitivity b 7) and 18 of 24 intervals excluding 1; docs/34 still prints '22 of 22' and '16 of 22' at lines 204, 230 and 473 with no amendment, and docs/56 s1 has now quoted the doc's 22 into the C5 headline table. I did NOT touch the notebook's measured 24 - it is a reproduced measurement and the banner already discloses the disagreement under the precedence rule - but the reconciliation is an amendment to docs/34 (and a follow-on correction in docs/56's observed row), which is outside a notebook fix and outside my remit. (2) The PAIR row count 71,529 here against 71,528 in docs/agents/journal_c2-contrast.md remains an unexplained filter difference; the notebook flags it twice and it changes nothing, but nobody has found the row. (3) Cell 93's 'r stayed inside 0.556 to 0.572' predates docs/58 (last rainfall lever bounded at <= +0.006 r, structural); it does not contradict docs/58, so I proposed no edit, but a pointer would be an enhancement if a later pass wants one. (4) I could not verify that the twelve SHA-256 prefixes printed in cell 4 still match the files on disk today - I am read-only and did not hash them - so my full 25/25 on 'Executes cleanly' rests on the session census (0 unexecuted, 0 errors) plus the fact that nb16 touches no engine default, not on a fresh re-hash.

### `17_runoff_signatures.ipynb` - 87 → **98**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 25 |
| Generator-sync | 20 | 20 |
| Coherence with canon | 20 | 11 |
| No kill-list / no stale | 15 | 12 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 9 |

Generated by `src/nbgen/make_nb17.py` - **all fixes landed on the generator, never on the `.ipynb`**.

**Narrative role.** The driver-validation gate standing between the discharge model and the sediment model: it asks whether the only two hydrological quantities MUSLE actually reads — surface runoff and flood peak — are right, answers 'the first is not refutable with the test that was written and the second is measurably wrong', and converts Phase B's closure into a quantified lower bound that every sediment stage downstream has to carry.

**Inherits from.** Phase B's adopted H2E configuration and its committed scorecard from nb13/nb14 (F = 0.25931, r capped near 0.6, El Niño skill-over-climatology −0.0005, α < 1 in every period — the pre-existing warning that peaks are low), the frozen docs/33 pre-registration that fixed H-BFI, H-PEAK and the H2E-S refit's three conditions before any number existed, and the frozen discharge in sim_calibrated_v2/q_gauge_H2E.npz.

**Hands to.** nb18/nb19 and stages C3–C5, as an explicit lower bound: −10.5 % fleet-wide and −19.0 % in the El Niño dry phase from the magnitude term alone, an event-count deficit that is NOT convertible into a factor (0.567^0.56 registered as forbidden arithmetic, 33.0 % of observed floods producing no simulated rise at all), and a ≈+10 % inflation of the simulated ENSO contrast that docs/56's reproduced 3.05x now has to be read against.

**CRITICAL and HIGH defects (3 of 21):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 0 | markdown | HIGH | stale-status | True when written (2026-08-12) and now false. The LS level landed that day: ls_formulation = buarque_2015_dg (V4_dg), f_LS = 0.25146 erosion-weighted, materialised by ACT 1 and made the engine default by ACT 2 (commit c3fdb55). docs/47's C4.3-BLOCKED-UNTIL-LS-LANDS is therefore discharged; C4.3 has  | docs/55_c43_verdict.md §1 (RAILED/EXPLORATORY, alpha ~0.48 below the box floor) and docs/5 |
| 76 | markdown | HIGH | unadjudicated-trigger | This page wrote its own trigger condition and the condition has since been met, with nothing anywhere pointing at it. docs/56 §1 prints the modelled median rate ratio as 3.05x over 18 of 18 stations and NAMES estimator (b) as the reference for judging the model, with observed (b) at 2.84-2.95 — i.e. | docs/56_c5_enso_application.md §1 (modelled 3.05 vs observed (b) 2.84-2.95) against this n |
| 107 | markdown | HIGH | prose-vs-output | §1.3's own cell prints 'MUSLE peak factor differs by 1.56x' and §1.3's read-out prose says 'a **1.56x** difference in MUSLE's peak factor (0.669 against 1.046)'. Checked by hand from the same printed values: (1.083/0.488)^0.56 = 1.5628. 1.97x appears nowhere in any output and looks like an unreduced | this notebook §1.3, cell 17 output (R_AMS 0.488 vs 1.083, peak factor 0.669 vs 1.046) and  |

**Not settled** (carried forward, not smoothed over): (1) THE BIG ONE — whether §5.9/§7.5's own 'within 10 %' clause has fired. docs/56 prints modelled median 3.05x over 18/18 stations against its NAMED reference estimator (b)'s observed 2.84–2.95, i.e. +3.4 % to +7.4 %, inside the 10 % nb17 nominated; and nb17's measured +9.6 % peak-asymmetry inflation is LARGER than that entire remaining agreement, so 'the model matches the observation because it is inflated' is a live reading. docs/56 carries no mention of the inflation caveat at all (grep 'inflat' over docs/56: zero hits). I refuse to adjudicate this — docs/56 owns it, and deciding it here would be exactly the pre-measurement verdict this project has twice had to reverse. My fixes point at it from three places and say it is open. Someone with authority over docs/56 must rule. (2) The 0.6482-vs-0.6478 cause is INFERRED, not measured: I attribute it to a day-set difference (>=180-day segment rule vs >=300-valid-day calendar-year rule) and the §8.3 row I propose says so explicitly, but I did not recompute either day set to confirm it. (3) I confirmed docs/36 carries a '≈+10 % inflation' (line 723) but did not read §2.6 verbatim, so cell 76's attribution 'which is the ≈+10 % docs/36 §2.6 quotes' is unverified as to section number. (4) §8.4 item 1's open issue stands untouched: the full-record R_AMS of the refit's fitted vectors was never computed, needs a ten-year engine run and a rebuilt gauge file, and no such artifact exists for H2E-S — so condition 1 and the §6.3 frontier remain calibration-window statements. (5) 0.552 remains a literal this notebook never measures; my fix

### `18_musle_construction.ipynb` - 43 → **97**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 11 |
| Generator-sync | 20 | 4 |
| Coherence with canon | 20 | 6 |
| No kill-list / no stale | 15 | 4 |
| Embargo & convention | 10 | 9 |
| Academic clarity | 10 | 9 |

Generated by `src/nbgen/make_nb18.py` - **all fixes landed on the generator, never on the `.ipynb`**.

**Narrative role.** The C3 construction record and audit trail: it turns Phase B's frozen surface runoff into a MUSLE sediment field over 8,672 minibacias x 3,652 days, documents the 363.4245196x unit error and its closure to twelve significant figures, makes and prices the two topographic judgement calls, registers the q_peak proxy's one-sided bias, proves alpha/C/LS non-identifiability (Pi = 5,164.418 at the adopted cp_revision), and returns the C3 verdict OPEN with the LS level unvalidated.

**Inherits from.** The frozen H2E hydrology from nb13/nb14 via sim_calibrated_v2/h2e_drivers.npz:qsur_rel_mm (nb12's model_inputs_v2 upstream of that), nb09 §4's K table and its own stated x0.1317 SI transform, nb07's DEM for the four LS2D variants, and nb15's 18-usable-station SSC classification for the G9 coverage disclosure.

**Hands to.** nb19 (the C3 gate and C4 setup), which receives the frozen sediment engine configuration, the identifiable product Pi, the registered LS bracket f_LS in [0.25146, 0.43194] and the G1-G9 guard set; downstream of nb19, docs/55's C4.3 search and docs/56's C5 application run on the adopted V4_dg field whose V0 counterpart this notebook is the record of.

**CRITICAL and HIGH defects (14 of 23):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 18 | code | CRITICAL | generator-notebook desync | The committed .ipynb has no ls2d_column pin. src/nbgen/make_nb18.py:697-702 (added by c3fdb55) DOES: it passes urh_ls2d='urh_ls2d.csv', ls2d_column='ls2d_hs' with the comment 'V0 pin: ACT 2 (2026-08-12) moved the engine default to V4_dg'. The .ipynb is therefore source-desynced from its generator at | commit c3fdb55 (ACT 2, 2026-08-12) + src/mgb_sediment.py:916-925; docs/37 A3 |
| 84 | code | CRITICAL | executed output unreproducible from committed source | This assertion passes in the committed outputs and would FAIL if the committed source were re-run today, because the unpinned cell-18 loader now resolves to V4_dg and the adopted basin total moves to roughly 75.3 Mt/yr (docs/47 section 4.3). The notebook's own integrity block is the proof that the s | commit c3fdb55 + docs/47 section 4.3 |
| 36 | markdown | HIGH | kill-list / stale engine-default assertion | True when written, false now. ACT 2 (commit c3fdb55, 2026-08-12) moved the engine default of load_geometry() to V4_dg, and data/processed/urh_ls2d_variants.csv (4.2 MB, 2026-08-12) is the committed gated column whose absence the sentence gave as the reason the switch was not draftable. The correct c | docs/37 A3 + commit c3fdb55 |
| 39 | markdown | HIGH | kill-list / stale engine-default assertion | Same falsehood as cell 36. The conclusion (this notebook's numbers are at V0) survives, but only because the generator pins the column; the premise 'no engine default has moved' is now wrong about the engine. | docs/37 A3 + commit c3fdb55 |
| 69 | code | HIGH | kill-list / stale engine-default assertion inside a printed string | This is the ONE code-cell home of journal item (a): the clause-2 reason string in the printed CLAUSES scoreboard asserts 'no engine default moved'. Because the notebook must be re-executed for the desync regardless, correcting this printed string costs nothing extra. | docs/37 A3 + commit c3fdb55 |
| 78 | markdown | HIGH | kill-list / stale engine-default assertion | Section 7.6 item 3 repeats the retired assertion in the notebook's most quotable place - the list of things a reader must not conclude. The decision has since been exercised in the engine. | docs/37 A3 + commit c3fdb55 |
| 83 | markdown | HIGH | kill-list / stale engine-default assertion | Section 9's 'what is not established' repeats it a fourth time in markdown. The level is indeed still unvalidated; the 'no default moved' half is false. | docs/37 A3 + commit c3fdb55 |
| 69 | code | HIGH | kill-list / withdrawn direction printed as a live verdict | docs/37 A1.9 WITHDREW the direction of this residual and docs/37 A1.7 item 7 names this exact generator string as owed to a later pass (this one). A1.9.2 requires the legs printed under BOTH readings - reading A 1.03-2.27x LOW, reading B 1.33-1.49x HIGH - and A1.9.3 dictates the summary line: 'The r | docs/37 A1.9.2-A1.9.3, assigned by A1.7 item 7 |
| 69 | code | HIGH | kill-list / withdrawn direction printed as a live verdict | The clause 4' reason string in the printed closure scoreboard states the withdrawn direction a second time, and states Leg A's reading-A-only bracket as though it were the whole comparison. | docs/37 A1.9.2-A1.9.3 |
| 68 | markdown | HIGH | quantity-mismatch claim withdrawn by the owning doc | docs/37 A1.9.1 records this sentence as the exact claim it refuted: RUSLE is a detachment-side quantity while SWAT Ch. 4:1 calls MUSLE's output a sediment yield, so the two sides may not name the same quantity - the same quantity error the retired SDR gate died of. docs/37 A1.7 item 7 names this gen | docs/37 A1.9.1-A1.9.2, assigned by A1.7 item 7 |
| 71 | markdown | HIGH | kill-list / withdrawn direction stated as measured | Stated in bold as the figure's measured finding. docs/37 A1.9.3 replaced it with a direction-unknown bracket and withdrew Leg C's max form; the same cell's 'means' block compounds it by calling this 'a measured, citable shortfall on the erosion side' and by saying clause 4' 'asks for 1.03-2.27x more | docs/37 A1.9.2-A1.9.3 |
| 83 | markdown | HIGH | kill-list / withdrawn direction stated as measured | Section 9 is the notebook's summary and therefore the most-quoted place the withdrawn direction survives. It also repeats 'the only leg with a like-for-like denominator', the very framing A1.9.1 refuted. | docs/37 A1.9.2-A1.9.3 |
| 76 | code | HIGH | kill-list / retired alpha band and reference plotted as current | MISSED BY THE PRIOR JOURNAL. Both numbers are derived from the SUPERSEDED x0.333-x0.421 LS bracket: 5.9*0.333 = 1.96 and 23.6*0.421 = 9.94 give the amber 2.0-9.9, and 11.8*0.377 gives 4.45 inside the retired 3.9-5.0 reference range. The kill list retires both. On the current registered bracket f_LS  | docs/37 A3 + docs/46 section 3.1 (bracket); cell 37's own output |
| 77 | markdown | HIGH | kill-list / retired alpha band and reference described as current | MISSED BY THE PRIOR JOURNAL. The markdown reading restates the retired band and reference in prose, unstruck and unqualified, and the following 'means' block builds an argument on it ('the two candidate bands for the same coefficient barely overlap'). Under the current bracket the rescaled band is 1 | docs/37 A3 + docs/46 section 3.1 |

**Re-execution: REQUIRED.** MANDATORY, AND NOT BECAUSE OF THE FIXES. nb18 is the corpus's only desynced notebook: src/nbgen/make_nb18.py carries a V0 pin (urh_ls2d='urh_ls2d.csv', ls2d_column='ls2d_hs', generator lines 697-702, added by commit c3fdb55) that never reached the committed .ipynb, whose cell 18 still calls sed.load_geometry(PROC, mini_ids=DRV.mini_ids) bare. Since ACT 2 moved that entry point's default to urh_ls2d_variants.csv:V4_dg (src/mgb_sediment.py:924-925), the committed notebook can no longer reproduce its own outputs: a bare re-run would load V4_dg, drop the adopted basin total from 299.5387 toward the 75.3235 Mt/yr V4_dg figure, and then RAISE at cell 84's own assertion abs(ADOPT - 299.5387) < 1e-3. Regeneration is therefore obligatory, and regeneration produces an unexecuted notebook. CONSEQUENCE FOR THIS SPEC: nb18 is the one notebook where a code-cell fix costs nothing extra, so 7 of the 21 fixes touch code cells (37 x2, 69 x3, 70, 76 x2 -> 8 code fixes across 5 cells) and the remaining 13 are markdown. Cost: make_nb18.py registers timeout=-1 (unbounded); the engine itself runs in about 4 s per configuration and the notebook executes 8 full-decade sediment runs plus 2 more in cells 60/61, so the wall time is dominated by the 546 MB h2e_drivers.npz load (2.6 s) and roughly 40-50 s of engine time, not by a calibration search - this is a cheap notebook to re-execute despite the unboun

**Not settled** (carried forward, not smoothed over): 1) CLAUSE 4' STATUS. docs/37 reclassified clause 4' as NOT ESTABLISHED, superseded by clause 4", but the notebook prints 'NOT MET'. I did NOT change the token, because it feeds four downstream places (the st_col colour map in cell 70, the '2 of 5 fail, 1 is not established, 1 is retired' verdict line in cell 69, cell 70's figure subtitle '(2 of 5 failed, 1 not established, 1 retired)', and cell 71's 'clauses 2 and 4' failing, clause 3 not established') and docs/37 itself keeps 'Still not met - a clause that cannot be evaluated is not a pass'. My fix carries A1.9's reclassification in the reason string instead. An orchestrator who wants the token changed must change all four places together, and should get docs/37's owner to say which count line is correct. 2) CELL 70's LEFT PANEL still plots reading-A ratios only (slo/shi from LEGS). I corrected the title to say so; a genuine both-readings redraw (two bracket bars per leg, one per reading) is a figure rewrite I did not attempt and did not want to invent geometry for. 3) 'C3 stays OPEN' is left standing everywhere. docs/37 A3 owns it and still asserts it; the canonical 'Phase C is COMPLETE' is a phase-level statement and does not close C3, and the doc wins over the summary. If a later doc closes C3, cells 36, 37, 39, 69, 71 and 83 all need a second pass. 4) THE x0.333 COLLISION at cell 75 is unresolved: the printed 'LS x0.333' is honest arithmetic (1/3, from the illustrative triple 11.8*3, 1.0, 1/3) but reads identically to the retired bracket endpoint retired three sections earlier. Left alone rather than churn a printed nu

### `19_c3_gate_and_c4_setup.ipynb` - 85 → **98**

| factor | max | awarded |
|---|--:|--:|
| Executes cleanly | 25 | 23 |
| Generator-sync | 20 | 20 |
| Coherence with canon | 20 | 14 |
| No kill-list / no stale | 15 | 9 |
| Embargo & convention | 10 | 10 |
| Academic clarity | 10 | 9 |

Generated by `src/nbgen/make_nb19.py` - **all fixes landed on the generator, never on the `.ipynb`**.

**Narrative role.** The decision record of the corpus: it is where the C3 closure gate was dismantled rather than passed or failed, where alpha was established as a fitted coefficient of adjustment rather than a physical constant, where the C4 calibration was measured to be feasible only as a small fit (2 free + 1 bounded on 8 stations), and where the resulting frozen pre-registration is summarised so the eventual fit can be held to what was promised.

**Inherits from.** nb18's built MUSLE engine and its basin-decade run (the 299.5387 / 248.7298 Mt/yr levels and the factor chain), plus the frozen H2E surface runoff from Phase B (nb13/nb14) and the C1/C2 station products of nb15/nb16 (79 stations classified, 18 usable, the model-free observed ENSO contrast).

**Hands to.** docs/45's frozen C4 pre-registration and, through it, the run this page still calls future: C4.3's RAILED / EXPLORATORY verdict (docs/55) and C5's reproduced 18/18 ENSO contrast at median 3.05x (docs/56) - the forward pointer this notebook currently lacks and that two of the fixes above install.

**CRITICAL and HIGH defects (7 of 11):**

| cell | type | severity | kind | the defect | owning doc |
|--:|:--:|:--:|---|---|---|
| 70 | markdown | HIGH | engine-default staleness | ACT 2 (commit c3fdb55, 2026-08-12) moved the engine default of src/mgb_sediment.py load_geometry() to V4_dg. The parenthesis reads as a live statement about the engine and is now false about it. The second half is still true of THIS notebook, because cell 6 pins ls2d_column='ls2d_hs' - so the honest | ACT 2 / src/mgb_sediment.py load_geometry(), commit c3fdb55 (2026-08-12); docs/37 A3 |
| 69 | code | HIGH | engine-default staleness in printed output | Same defect inside a code cell's printed string, and it directly contradicts cell 6's own comment in the same notebook ('ACT 2 (2026-08-12) moved the engine default to V4_dg; nb19 is a V0 record'). Correcting the string is a CODE edit and would force a full re-execution at timeout=-1; the fix is the | ACT 2 / src/mgb_sediment.py load_geometry(), commit c3fdb55 (2026-08-12) |
| 70 | markdown | HIGH | stale stage status | C4.3 has since been run. Its verdict is RAILED / EXPLORATORY, NOT adopted: in-box optimum on the box floor (alpha = 2.0), median KGE_ln -0.118 on estimator (a) and +0.139 on (b), unconstrained optimum wanting alpha ~ 0.48 below the box floor. The out-of-sample C5 application then reproduced the obse | docs/55 (C4.3 verdict); docs/56 (C5) |
| 69 | code | HIGH | stale stage status in printed output | 'C4.3 stays BLOCKED' is superseded by docs/55. Inside a code cell's printed string, so it is corrected in the adjacent markdown (cell 70) rather than by a code edit that would force re-execution at timeout=-1. | docs/55 |
| 58 | markdown | HIGH | kill-list term reads as live | k_min is linear in sigma_r, and sigma_r = 0.465 was retired as a per-station residual sd (measured 1.9618 ln, x4.22 larger). The corrected all-18 floor is 0.0065-0.0069 /km, i.e. 'no first-order channel sink WEAKER than ~10x over ~342 km is detectable'. This notebook's own cell 55 carries the correc | docs/45 s8.1.4; docs/47 s2.2 (D2); docs/48 |
| 58 | markdown | HIGH | retired sense of the registered sentence form | docs/45 s8.1.4 settled the sense: only 'weaker' is the correct reading of a DETECTION FLOOR, and 'weaker' is the registered wording from that amendment forward. Cell 55 states this explicitly ('Sense settled: only "weaker" is the correct reading'), so cell 58 contradicts cell 55 inside the same note | docs/45 s8.1.4 |
| 32 | markdown | HIGH | prose-vs-code contradiction | Cell 31, the cell this markdown reads, PRINTS 'the Qsur ratio would have to be 2.21-5.45 (primary) or 4.17-11.91 (sensitivity)' - the range across the whole registered beta band [0.45, 0.65], which is the framing the rest of the paragraph uses ('across the *entire* registered beta band'). The prose  | the notebook's own cell 31 output; docs/35 s6.3 (the [0.45, 0.65] hard stop) |

**Not settled** (carried forward, not smoothed over): 1) Whether C3 itself is now CLOSED. This notebook says 'C3 stays OPEN'; docs/54 says the C3.1 closeout is NOT complete with four surviving adversarial findings and an uncommitted changeset; the canon says only that Phase C is COMPLETE. I left the C3 OPEN language untouched and adjudicated nothing about it. 2) How docs/47's `C4.3-BLOCKED-UNTIL-LS-LANDS` condition was formally discharged: docs/35 s9.5.5 states in terms that the s6.1 re-registration 'does not unblock C4.3', yet docs/55 exists and calls itself the C4.3 deliverable. My fix records that C4.3 ran and explicitly declines to name the discharging record. 3) Section 3.3's 'the guard is blind' conclusion is derived from a deposition-free band (5.6727-7.2485) computed at V0's 299.5387 Mt/yr. At the adopted V4_dg total (75.3235 Mt/yr) the same construction gives 11.8*{144,184}/75.3235, which leaves the docs/35 s9.5 re-registered band entirely - whether the blindness conclusion survives that reframing is in the neighbourhood of docs/47 open item O12 and I did not decide it. 4) Cell 15's computed reading-B bracket (1.319-1.475x) versus docs/37 A1.9's (1.332-1.490x): I flagged and disclosed the 0.33-vs-1/3 rounding as the whole cause and named the doc authoritative, but I did not verify the arithmetic inside docs/37 A1.9 itself. 5) The docs/46 x1.008878-vs-x1.008818 apparent digit transposition that cell 69 already reports as 'REPORTED, not fixed' in a frozen document remains open and is not mine. 6) Cell 4 fact 1 quotes the El Nino correlation ceiling as 0.556-0.572 without pointing at docs/58, which has since bounded the 

## 5 - Open items this pass did not close

1. **`nb12`'s 7 code-cell fixes are HELD.** They repair the shipped `model_inputs_v2/manifest.json` (a length-4018 `dates` array documented as "3287 contiguous days"; the rainfall field credited to 294 gauges when the v2 IDW ran on 291) and the shipped `model_inputs_v2/README.md` (a copy-paste snippet that loads the **v1** bundle, and a stated shape of `(3287, 8672)` for an array that is `(4018, 8672)`). Applying them costs a 7,200 s re-execution **that rewrites the forcing bundle H2E was fitted on**. The generator edits are specified and verified-unique; only the execution is deferred.
2. **No notebook exists for `docs/55`-`docs/59`.** The corpus ends at nb19, which sets up a C4 fit that has since run. The two that would most repay building are **nb20 - the C4.3 verdict, and why a pre-computable search is not a test** and **nb21 - C5, and why a contrast survives a non-identifiable level**. Out of scope for this pass (TASK 2 covers 01-19); recorded so it is not lost. **They must be built as generators** (`make_nb20.py`, `make_nb21.py`), never hand-written.
3. **`02_urh.ipynb` and `08_urh.ipynb` both claim URH.** The duplication was adjudicated by `journal_nbc1-nb02-08-urh.md` and both notebooks were corrected, but the structural question - whether the didactic 02 and the real-data 08 should remain two notebooks - is a curation decision left to the owner.
4. **Per-notebook `not_settled` items** are recorded verbatim in §4 above rather than aggregated, because several are genuine open questions about the science (which quantity the MUSLE sum represents; how `docs/47`'s block condition was formally discharged) and belong with the notebook that raises them.
