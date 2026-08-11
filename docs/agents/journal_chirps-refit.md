# Journal: chirps-refit (C2b.3 CHIRPS refit)

GOAL: refit CHIRPS-gauge merge quantile maps on REPAIRED series INCLUDING
inferred-dry days (approval == 'Inferido_seco'), then re-run BOTH original
gates unchanged. BOTH gates or no adoption.

Gates (FROZEN):
- VOLUME: area-weighted basin mean, 2009-2017, within 1% of 2036.4 mm/yr
  => allowed band [2016.0, 2056.8] mm/yr
- LOOCV: nb11 s6 protocol exactly (same k, same distance fn, same station set),
  merged-without-that-gauge, median daily r must EXCEED 0.429

## Checklist
- [ ] 1. Read src/merge_chirps_gauges.py + docs/18 s15
- [ ] 2. Identify the single fit-input change
- [ ] 3. Implement (one change only)
- [ ] 4. Run VOLUME gate
- [ ] 5. Run LOOCV gate
- [ ] 6. Decide by rule; write outputs
- [ ] 7. Append outcome to docs/18

## Log
- [step 0] Journal created. Starting reads.

- [step 1] READ src/merge_chirps_gauges.py (460 lines), src/idw_forcing.py, src/forcing_npy.py,
  docs/18 s15 (lines 815-882), docs/33 H-CHIRPS (lines 98-122).
  Gate values confirmed identical in all three places: volume [2016.0, 2056.8] mm/yr on
  2009-2017; LOOCV median daily r > 0.429 over 287 gauges; baseline self-check assert
  |med_base - 0.429| < 6e-4.

- [step 2] *** FINDING THAT CHANGES THE TASK'S PREMISE (measured, not assumed) ***
  The refit the task specifies is ALREADY the code's behaviour. Evidence, from disk:
    data/processed/precip_gauges_daily_qc_v2.csv approval counts:
      Definitivo 512,324 | Inferido_seco 240,158 | Preliminar 136,155 | En revision 38,273
      = 926,910 rows, 294 codes, precip_mm NaN count 0, Inferido_seco precip_mm all 0.0
    (v1 precip_gauges_daily_qc.csv has 795,881 rows / 109,129 Inferido_seco - the first
     repair pass only.)
  merge_chirps_gauges.load_gauges() reads *_v2* and applies only dropna(subset=['precip_mm']),
  which drops nothing (0 NaN). No approval filter exists anywhere in the path
  (grep 'Inferido_seco' src/*.py -> only idw_forcing APPROVAL_RANK and the repair script).
  QmapPools builds its pairs on m = obs[:,j] & ~isnan(C_gauge[:,j]) with obs = ~isnan(Gv),
  and Gv is the pivot of that v2 frame => the 240,158 inferred-dry zeros are ALREADY in
  every quantile-map pool.
  => docs/18 s15.3's diagnosis ("maps fitted on reporting-day pairs") is only half right:
     the maps already saw the inferred dry days; what they cannot see is the dry days the
     repair never inferred (the 139 residual rain-selective stations, s9.3).
  ISSUE journalled; NOT acted on by changing any gate. Plan: (a) make the inclusion explicit
  and ASSERT it, (b) add an opt-in 'exclude' diagnostic mode that drops Inferido_seco from the
  fit pool ONLY, to measure how much of the volume surplus the inclusion already removes.
  The gate decision is taken on the registered 'include' mode alone.

- [step 3] Edited src/merge_chirps_gauges.py (the ONLY source file touched). Changes:
  1. load_gauges() now also returns INF = (days x gauges) bool for approval=='Inferido_seco'
     (pivot_table aggfunc='max' on a float flag, reindexed exactly like W).
  2. QmapPools takes inferred_dry + mode ('include' default = registered C2b.3 config;
     'exclude' = reporting-days-only counterfactual). The mode gates ONLY the fit-pool mask
     m; obs, the IDW field and every LOOCV scoring mask are untouched in both modes.
     Asserts: inferred_dry subset of obs; include => n_inferred_pairs > 0; exclude => == 0.
     Prints pool size and inferred-dry share.
  3. main() gains --qmap-inferred-dry; 'exclude' writes nothing and takes no decision.
  4. Report output renamed merge_loocv_report.csv -> merge_loocv_report_v2.csv (the
     pre-refit docs/18 s15 report is preserved untouched), with a qmap_inferred_dry column.
  NOTHING else changed: stratification, blending, weights, lag, gap-fill, determinism,
  both gate constants (VOLUME_TARGET 2036.4 / VOLUME_TOL 0.01 / BASELINE_MEDIAN_R 0.429)
  are byte-identical to the rejected run.
  Syntax check passed; --help renders.

- [step 4] BEFORE RISKY OP: launching the registered 'include' run (full LOOCV + full-basin
  field build, ~4018 days x 8672 minibacias float32). Log -> scratchpad/run_include.log.

- [step 5] REGISTERED RUN COMPLETE (--qmap-inferred-dry include). Log:
  scratchpad/run_include.log. Numbers, from the executed output (not an exit code):
    gauge matrix        291 gauges x 4018 days, 2008-01-01..2018-12-31
    inferred-dry days   240,115 station-days = 25.9 % of all reporting station-days
    fit pools           926,268 paired station-days, 240,115 (25.9 %) repair-inferred dry
    baseline self-check 287 gauges, median daily r 0.429  (assert |d| < 6e-4 PASSED)
    LOOCV GATE          merged median daily r 0.447  > 0.429  -> PASS
                        (baseline-mask-only diagnostic 0.449)
                        <10 km n=98  0.481 -> 0.475 ; 10-30 km n=169 0.426 -> 0.449 ;
                        >30 km n=20  0.343 -> 0.300
    VOLUME GATE         2009-2017 area-weighted basin mean 2188.5 mm/yr
                        band [2016.0, 2056.8] -> FAIL (+7.47 %)
                        2008-2018 context 2219.2 mm/yr (trap 9: window attached)
    order-invariance    2 gauge-column shuffles, byte-identical field
    fallback cells      41,180 k=6-silent minibacia-days, all filled by mapped CHIRPS
    DECISION            DO NOT ADOPT (both gates required; volume fails)
  These reproduce the rejected Aug-3 run to the last printed digit (0.447 / 2188.5 /
  2219.2 / 41,180 / 0.481-0.426-0.343 -> 0.475-0.449-0.300), which is the *proof* that the
  registered change was already in force. Wrote merge_loocv_report_v2.csv (291 rows);
  merge_loocv_report.csv untouched. No forcing file written.

- [step 6] BEFORE RISKY OP: launching the counterfactual --qmap-inferred-dry exclude to
  measure what the inferred-dry inclusion is already worth on volume. Diagnostic only;
  writes nothing, takes no decision. Log -> scratchpad/run_exclude.log.

- [step 7] COUNTERFACTUAL COMPLETE (--qmap-inferred-dry exclude, diagnostic, wrote nothing):
    fit pools    686,153 pairs, 0 inferred-dry (assert n_inf == 0 passed)
    LOOCV        median daily r 0.448 (baseline 0.429 reproduced again);
                 <10 km 0.475, 10-30 km 0.452, >30 km 0.300
    VOLUME       2009-2017 2294.1 mm/yr (+12.65 %); 2008-2018 2324.6 mm/yr
  => including the inferred-dry days is worth 105.6 mm/yr = 41.0 % of the exclude surplus.
     Remaining surplus after the lever is fully pulled: +152.1 mm/yr; the field would have to
     shed a further 131.7 mm/yr (6.0 % of itself) just to touch the band top 2056.8.
     Correlation is indifferent to the fit pool (0.448 vs 0.447) - the volume/correlation
     independence of docs/26 H2-H1, reappearing in the forcing.

- [step 8] PER-GAUGE scale (fleet numbers above; both required):
    merge_loocv_report_v2.csv vs merge_loocv_report.csv: 291/291 codes aligned,
      max |diff| 0.000e+00 on r_base, r_merged, bias_merged_pct, n_base, n_merged
      -> bit-identical, the no-op is proven not asserted.
    287 eval gauges: 149 improved, 51 worsened, 87 unchanged; median delta +0.0003.
    per-gauge volume signal: bias_base median +1.73 %, bias_merged median +2.00 %,
      per-gauge delta median +0.00 pts (108 wetter / 92 drier).
      By isolation band the delta is monotone: +0.00 pts <10 km, +0.24 pts 10-30 km,
      +0.89 pts >30 km. The field is unbiased where it can be tested and +7.5 % over the
      basin => the surplus sits in ungauged terrain, where w_chirps -> 1.
    qmap pool level used at the eval gauges: 273 ('bz') / 14 ('z' fallback).

- [step 9] DECISION under the pre-registered rule, quoted:
    "ADOPT if merged median r > 0.429 by any margin AND the volume gate holds; otherwise
     DO NOT ADOPT."
    LOOCV 0.447 > 0.429 PASS ; VOLUME 2188.5 outside [2016.0, 2056.8] FAIL
    => DO NOT ADOPT. Written per the task: ONLY merge_loocv_report_v2.csv.
    Verified on disk: forcing_minibacia_precip_v3.csv ABSENT,
    forcing_minibacia_provenance_v3.csv ABSENT, no forcing_precip_v3*.npy;
    merge_loocv_report.csv still dated Aug 3 20:28 (untouched).

- [step 10] docs/18 s15.5 appended (line 884, file now 951 lines): both gate numbers with
  their windows attached (trap 9), the rule quoted, the counterfactual, the per-gauge
  distribution, and an explicit CORRECTION to s15.3 (which implied the inferred-dry days
  were absent from the fit; they were 25.9 % of it).

## Outcome

BOTH GATES RAN. LOOCV PASS (0.447 > 0.429), VOLUME FAIL (2188.5 vs [2016.0, 2056.8]).
=> DO NOT ADOPT. v3 not created. The CHIRPS question is closed inside the merge code; the
only remaining route is upstream repair of the 139 residual rain-selective stations.

## Files touched
- src/merge_chirps_gauges.py       (fit input made explicit + asserted; diagnostic flag;
                                    report renamed to merge_loocv_report_v2.csv)
- data/processed/merge_loocv_report_v2.csv   (new, 291 rows)
- docs/18_hydrology_journal.md     (s15.5 appended)
- docs/agents/journal_chirps-refit.md (this journal)
No git commands run. model_inputs* untouched, nb11/nb12 untouched, no calibration launched.

## Issues for the parent
1. The registered intervention was a no-op: the inferred-dry days were already in the fit
   pools. docs/33 H-CHIRPS and docs/18 s15.3 both rested on the opposite belief. s15.5
   corrects the record; docs/33 is frozen and was NOT edited.
2. A v3 calibration cell is moot here (v3 does not exist), but the standing note stands: it
   would need a FRESH pre-registration and an nb12 rebuild, and is not part of this task.
3. Doc 33's H-CHIRPS hypothesis is REFUTED by its own gate. Whoever updates the C2b results
   table should record it as refuted, not as untested.
