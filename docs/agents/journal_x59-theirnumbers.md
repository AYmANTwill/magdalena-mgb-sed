# Journal — x59-theirnumbers (M4: independently reproduce every number docs/59 will quote from THEIR repo)

Started 2026-08-12. READ-ONLY agent. Writes only this file.

THEIR REPO (read-only):
`C:/Users/KNADE~1.MSI/AppData/Local/Temp/claude/c--dev-magdalena-mgb-sed/5b31ac56-2c65-4a16-ac08-d810606ee036/scratchpad/friend_repo`

## Log

### 1. Equifinality (params JSONs) — REPRODUCES

`python3.10` on `outputs/{calibration,calibration_val}/stage2_sediment_params.json`:

| | main (`calibration/`) | val (`calibration_val/`) |
|---|---|---|
| alpha | 55.40533705803028 | 96.58548959666564 |
| beta | 0.3980082263356884 | 0.3493190336411669 |
| alpha_tc | 0.6174944111935904 | 0.34930405763655487 |
| c_mult | 0.04887856036752898 | 0.05779232694874972 |
| alpha*c_mult | 2.7081331120742234 | 5.581900193275565 |
| stage2_median_kge_log | 0.05461202762457862 | 0.05902198016897042 |
| n_stations | 21 | 13 |
| window | 2013-01-01..2014-12-31 | same |

product ratio = 2.0611616793829812 (x2.06); alpha ratio 1.7432524504905407;
c_mult ratio 1.1823655712074193; alpha_tc ratio 0.5656797070622307;
delta stage2_median_kge_log = +0.004409952544391804.
Both JSONs carry the identical stage1_hydrology multipliers (wm 1.0419334532095188,
b 0.7867948846826227, kbas 0.4638904558079048, kint 0.20598552185041888) and the identical
`notes.alpha_c_collinearity` / `notes.held_out` strings. ORCHESTRATOR NUMBERS ALL CONFIRMED.

Row counts: `wc -l` -> 22 / 14 / 91 (i.e. 21, 13, 90 data rows). unique station ids = 21 / 13 / 90.

**Subset check (val vs main): CONFIRMED SUBSET.** `set(val.station) <= set(main.station)` is True;
`val - main` empty; the 8 dropped are
0021187030, 0022027010, 0024017830, 0024037030, 0024037040, 0024037130, 0026177030, 0028037090.
So the "drop 8 stations" framing is correct.

**NEW, not in the orchestrator's list:** the 21 sediment stations are NOT a subset of the 90
stage1 discharge gauges. Overlap = 12; the 9 sediment stations with no stage1 row are
0021187030, 0022027010, 0022057090, 0024017830, 0024037030, 0024037040, 0024037130, 0026177030,
0028037090. (Note 8 of those 9 are exactly the 8 dropped in the val run.)

### 2. Their sediment metrics — REPRODUCE (with two degeneracies)

MAIN (21 stations), from `stage2_best_station_metrics.csv`:
- kge_log: median 0.0546120276245786, mean -0.4009524187026002, IQR [-0.755856631445291, 0.2058048313996633] (0.9616614628449544), range -3.9404296349448185 .. 0.5649324004081645, n=21
- kge: median -0.6116615042541171, mean -4.865754074970896, IQR [-1.4825372803386625, -0.1500246262369255], range -53.11303946929499 .. 0.3527542649644392
- peak_kge: median -0.707685835442408, mean -1.8816519453611373, range -16.32909527440084 .. 0.59793739236106, **n=20 (one NaN)**
- r: median 0.08705689420035126, mean 0.15000112661199114, range -0.0464776038914307 .. 0.5886233051354063, **n=20 (one NaN)**
- ratio (sim_mean/obs_mean): median 1.4894761031788255, mean 3.4689435528250927, range 0.0 .. 22.64216150017258
- nse median -1.9148322219442944 (min -4671.307410057857); log_nse median -2.6628075393490165
- pbias_pct median 48.94761031788255; n (paired obs) median 237, range 44..633

Reported vs recomputed: reported stage2_median_kge_log 0.05461202762457862 vs column median
0.0546120276245786 -> differ by 2.0816681711721685e-17 (float printing only). SAME for val
(0.05902198016897042 vs 0.0590219801689704). The reported scalar IS the median of the
per-station kge_log column.

Degenerate stations (MAIN):
- **0021217250: sim_mean = 0.00000 exactly, ratio 0, pbias -100 %, r = NaN, kge_log -2.281251.**
  The model simulates zero SSC at this station for all 472 paired days. kge/peak_kge are still
  finite (-0.732051) because `kge()` only NaNs when sd_obs or mean_obs is 0, and r is set to 0.0
  when sd_sim == 0 (metrics.py: `r = ... if sd_s > 0 else 0.0`), so a dead series scores
  1-sqrt(0+1+1)... in the log space, not NaN. It is counted in the median.
- 0026017060: only 90 paired obs, ratio 22.23, kge -53.11, peak_kge NaN.
Removing the dead station moves the median from 0.0546120276245786 to 0.05783141598210405
(+0.0032) — immaterial to the headline, but the headline median is the 11th of 21 values
(station 0029067120), i.e. it rests on a single station.

Distribution against the cited bar [-0.26, 0.44] (bar taken from their own metrics.py docstring):
MAIN 12/21 stations inside; 14/21 above the -0.414 mean-predictor benchmark; 11/21 with
kge_log > 0. VAL 7/13 inside. STAGE1 46/90 inside, 32/90 above 0.44.

VAL (13 stations): kge_log median 0.0590219801689704, mean -0.6222438871165349,
range -4.06874666617062 .. 0.3207294698001179; kge median -0.900256502459243;
peak_kge median -0.7746422518767224 (n=12); r median 0.14111609901242134 (n=12);
ratio median 1.868218743644456, max 25.687516706323468.

### 3. Their hydrology metrics (90 gauges) — REPRODUCE
From `outputs/calibration/stage1_best_station_metrics.csv` (90 rows, has an `area_km2` column):
- kge_log median 0.32933947922532514, mean -17.835613697297546, IQR [-0.09024535839564155, 0.5373107642390704], min -1586.675112808096, max 0.8005422804102756
- kge median 0.07007094536185275, mean 0.017828265907860175, range -2.231352330313804 .. 0.7470307562934062
- peak_kge median -0.48819254632353637, range -8.573036638432797 .. 0.3710855361775562
- r median 0.4338397362795588, range -0.3324995251054851 .. 0.933587092206802
`stage1_hydrology_params.json.score_kge_log` = 0.32933947922532514 = EXACTLY the median of the
kge_log column, **although the JSON `note` says "area-sqrt-weighted mean KGE on log discharge"**.
That note and the number disagree — see the code read below.

### 3b. It IS discharge (code-confirmed), and the objective is the MEDIAN
`scripts/18_calibrate_hydrology.py` — `score_discharge(result, obs, station_reach, area_km2)` reads
`result.q_m3s[:, reach]` (line ~85) against observed discharge; the output table carries an
`area_km2` column. Stage 1 is unambiguously DISCHARGE, not sediment. Its default `--out-dir` is
`outputs/calibration` (line 126), 16 trials in `stage1_search_history.csv` (17 lines), hydrodynamic
(local-inertial) routing.
Selection: line 212 `s = table.attrs.get("median_kge_log", ...)` — i.e. the **unweighted median**
is the score that is maximised and written as `score_kge_log`, even though
`score_discharge` *returns* `np.average(scores, weights=sqrt(area))` (line 116, unused) and the JSON
`note` still says "area-sqrt-weighted mean". **The note is stale; the number is the median.** That
is why `score_kge_log` == median of the column exactly.
Also present: `outputs/calibration_fast` (400 trials) and `calibration_fast_b` (300 trials) score
0.36820537350137134 / 0.37235713475898685 on 90 gauges but declare
`"routing": "linear_reservoir (NOT hydrodynamic) -- confirm with script 18"`. Stage 2 uses the
script-18 hydrodynamic multipliers (they match `outputs/calibration/stage1_hydrology_params.json`
bit-for-bit), NOT the faster/higher-scoring linear-reservoir ones. So **0.329 is the right
hydrology number to quote next to their sediment 0.055**; 0.368/0.372 belong to a different router.

### 4. What their stage-2 objective actually was — `scripts/21_calibrate_sediment.py`
- **Maximised scalar**: `median` over stations of a per-station **KGE on log SSC concentration**.
  `score_ssc()` lines 100-115:
      eps = max(np.median(o) * 1e-3, 1e-6)
      lo, ls = np.log(o + eps), np.log(np.maximum(s, 0) + eps)
      m.update(..., kge_log=float(evaluate(lo, ls)["kge"]), ...)
      return float(np.median(scores)), table
  **CORRECTION to the orchestrator's brief:** the epsilon actually used for the reported
  `kge_log` is **0.1 % of the MEDIAN observation**, not 1 % of the mean. The 1 %-of-mean default
  lives in `metrics.kge_log`, which script 21 does NOT call for this column — the inline
  `kge_log` overwrites `evaluate()`'s one. (The `kge`, `r`, `peak_kge`, `eps_pct`, `beta_pct`
  columns are `evaluate(o, s)` on the LINEAR series.)
- `composite_objective` (peak_weight 0.35) exists in `metrics.py` but is **NOT used** by script 21
  (grep: no reference). No peak weighting entered their sediment fit.
- **Concentration, not flux**: `result.ssc_mg_l[:, reach]` (line 95). Confirmed.
- **Search**: 400-default plain Monte Carlo (`--n-musle`, `rng = default_rng(seed=42)`), trial 0 =
  Williams defaults (alpha 11.8, beta 0.56, a_tc 0.5, c_mult 1.0). The main history has **500**
  rows, the val history **300**. Bounds (lines 225-228):
  alpha log-uniform [0.02, 200]; beta uniform [0.25, 0.85]; alpha_tc uniform [0.15, 0.85];
  c_mult log-uniform [0.02, 20]. No greedy/DDS refinement in stage 2.
- **Station set**: `load_observed_ssc` keeps `st.plausible` and, with `--only-validated-stations`,
  only `mapping == "discharge_validated"`; `min_days` default 30, and `score_ssc` additionally
  needs >= 20 paired positive days. So the 21 -> 13 drop is the **discharge-validated subset**,
  a mapping-quality filter, not an arbitrary 8-station deletion. docs/59 must say so.
- Reported vs optimised: **the same scalar** (median kge_log). No mismatch there.
- Stage 3 triggers: `stage3_trigger_rules: []` and `final == stage2` score in both JSONs. Whether
  `--skip-triggers` was passed or no rule cleared the `gain < 1e-3` stop cannot be settled from
  the artefacts on disk.

Fitted values vs their own bounds (log-position in the sampled box):
main alpha 0.8606304013961301 of log[0.02,200]; beta 0.24668037722614733 of [0.25,0.85];
alpha_tc 0.6678491588479862 of [0.15,0.85]; c_mult 0.12936280345827444 of log[0.02,20].
val  alpha 0.9209704724874503; beta 0.16553172273527816; alpha_tc 0.28472008233793555;
c_mult 0.1536133951920586. **Nothing is on a rail** — both optima sit interior.

### 4b. The equifinality, measured on ONE station set (strongest available statement)
`stage2_search_history.csv` for the two runs share the same `i` and byte-identical
alpha/beta/alpha_tc/c_mult for all 300 common trials (same seed, same draws; max abs diff 0.0 in
every column). Score correlation 0.9965067408833312; 133/300 scores identical (the median lands on
the same station).
=> On the SAME 13 discharge-validated stations: main's optimum (alpha*c_mult 2.7081331120742234)
scores 0.0546120276245786 and val's optimum (alpha*c_mult 5.581900193275565) scores
0.0590219801689704 — **a 2.061x change in the only identifiable product for
0.004409952544391804 of median KGE_log.** Reverse direction: on the 21 stations the val optimum
scores 0.0143660572220518 vs 0.0546120276245786 (gap 0.040245970402526796).
Flatness of the ridge (descriptive, no bar introduced): the 5 best of 500 main trials span
alpha*c_mult 2.0517770216664286..3.8522003200015518 within 0.01 of the best; the 7 best span
1.745571109150601..4.525747918693924 within 0.02. In the val pool the 10 best within 0.02 span
1.745571109150601..12.723488760917752.

### 2b. Their own README's stage-2 numbers vs the files (two mismatches, both minor)
`README.md` s10.2/10.3 quotes "Median KGE_log +0.055" (matches), "sim/obs ratio median 1.49"
(matches `ratio` median 1.4894761031788255), "beta (volume bias) median 0.99" (= `kge_beta`
median 0.9927759308582056, the LOG-space bias term) and "Correlation r median 0.16" (= `kge_r`
median 0.1591360800547902, log-space; the linear-space `r` median is 0.08705689420035126).
Mismatches: (i) README says "the 26 discharge-validated stations", the val artefacts say
**13** (`n_stations` 13, 13 rows) — the "+0.004" delta itself reproduces exactly
(0.004409952544391804); (ii) README says "trials converged on alpha.C ~ 1.7-2.0" whereas the
fitted product is 2.708 and the near-best trials span 2.05-3.85 (README also says "fitted
product ~ 2.7" two sentences later, so this reads like a stale range, not a claim in conflict).
They also flag the dead station themselves: README s10.3 "**Open bug.** Station `0021217250`
(reach 6126) simulates exactly 0.00 mg/L ... Unexplained." — we found the same station
independently; credit where due.

### 5. alpha_tc is NOT a transport-capacity / delivery-ratio knob -- OUR CLAIM IS WRONG
src/mgbsed/model/musle.py:156-177 --
    def peak_runoff_rate(surface_runoff_mm, area_km2, tconc_s, alpha_tc=0.5):
        """Peak runoff rate qpeak [m3/s] (modified rational method, as in SWAT).
            qpeak = alpha_tc * Qsur * A / (3.6 * tconc)
        ``alpha_tc`` is the fraction of the daily rainfall that falls within the
        time of concentration."""
        return float(alpha_tc) * qsur * area / (3.6 * tc_h)
and musle_yield (lines 300-343) --
    qpeak  = peak_runoff_rate(qsur, area_km2, tconc_s, params.alpha_tc)
    energy = qsur * qpeak * area_ha
    yield_t = alpha * np.power(energy, beta) * k_factor * c_factor * p_factor * ls2d

So alpha_tc is the SWAT rainfall-intensity fraction inside the MUSLE peak-flow term, physically
bounded in [0,1] and sampled over [0.15, 0.85]. It is NOT a deposition limiter and NOT a fitted
delivery ratio. docs/59 must not say we refuse to fit a delivery ratio that they fitted.
Their deposition is PHYSICAL, not fitted: sediment.py module docstring -- suspended load is
"neither deposited in nor resuspended from" the channel, and floodplain retention is Stokes
settling (settle = conc_fp * ws * flooded_area_m2 * dt, lines 377-386) with ws from the class
diameter, plus a 3-reservoir catchment-to-channel delay whose only free multiplier gamma is
pinned at 1.0 in config/magdalena.yaml. Nothing delivery-ratio-shaped is fitted anywhere.

What IS true, and is stronger: because alpha_tc multiplies energy by a GLOBAL scalar,
energy**beta = alpha_tc**beta * (qsur^2 * A_km2 * A_ha / (3.6 tc_h))**beta, so at fixed beta the
pair (alpha, alpha_tc) is EXACTLY collinear, just as (alpha, c_mult) is. Their identifiable scale
group is alpha * c_mult * alpha_tc**beta -- a THREE-way degeneracy, of which their note documents
two terms. Measured at each run's own beta:
  main 55.40533705803028 * 0.04887856036752898 * 0.6174944111935904**0.3980082263356884
       = 2.23532271514266
  val  96.58548959666564 * 0.05779232694874972 * 0.34930405763655487**0.3493190336411669
       = 3.8655776402965714
  ratio = 1.7293152411999122
Caveats I must state: (i) the config triggers carry per-catchment-day beta_mult (0.95/0.91/0.87
for sogamoso) and stage 2 never disables them (simulate.py run_sediment uses self.triggers from
config; script 21 passes no triggers argument), so beta is not strictly uniform and alpha_tc is
MARGINALLY identifiable through that rare-event channel. Their own docstring says the absolute
LS2D thresholds sit above almost the whole distribution ("only ~2 % of reaches could ever exceed
the first and none the second"), and in BOTH JSONs final_median_kge_log == stage2_median_kge_log
to the last digit, which is what you see if the triggers never fired (or if --skip-triggers was
passed). Cannot distinguish from disk. (ii) alpha is not comparable across runs with different
beta either, since the effective multiplier is alpha*C*E**beta for a bracket E >> 1. Their README
"fitted product 2.7 against Williams 11.8" therefore compares products at beta 0.398 vs 0.56;
docs/59 must not repeat that ratio as if it were dimensionless.
Also: stage-2 trials run with check_mass_balance=False (script 21 line 236); mass closure is
exercised in tests/test_physics.py, not per trial.

### 6. Their RS retrieval -- reproduces, but it is NOT a satellite validation
outputs/tables/rs_retrieval_summary.csv verbatim, all four rows:
  nir    / landsat8_oli : n 787,  feat 10, train_r_log 0.97687502129253,
      test_r_log 0.8857823492676947, test_r_linear 0.816025821941709,
      eps 35.0303060561723, bias -0.7502172772418492, mape 66.42652277636707,
      rmse 19.666958812092627, ssc 0.283..1033.3
  nir    / sentinel2_msi: n 787,  feat 13, train_r_log 0.9802614949886186,
      test_r_log 0.8958905992406959, test_r_linear 0.8221718849670736,
      eps 31.4913239467016, bias -1.419175214904289, mape 60.778163282633514,
      rmse 19.147034231671654, ssc 0.283..1033.3
  no-nir / landsat8_oli : n 2041, feat 5,  train_r_log 0.9572967603009032,
      test_r_log 0.763103716267502, test_r_linear 0.6237400550493547,
      eps 48.17027601513448, bias 8.708639734396485, mape 93.28658366273734,
      rmse 20.403383888324555, ssc 0.1..1033.3
  no-nir / sentinel2_msi: n 2041, feat 10, train_r_log 0.9645235161032423,
      test_r_log 0.8239336472336656, test_r_linear 0.7159926583211268,
      eps 38.37416081961271, bias 8.615965362881518, mape 74.44147522861627,
      rmse 18.46931582005816, ssc 0.1..1033.3
ORCHESTRATOR NUMBERS CONFIRMED. One correction: bias -1.42 is sentinel2+nir (as briefed);
landsat8+nir bias is -0.7502172772418492.

What the number actually is (scripts/03_train_rs_model.py + src/mgbsed/remote_sensing/ssc.py):
- TARGET: GLORIA-2022 lab TSS in g/m3 (== mg/L), meta["TSS"], trained as log1p(TSS) with
  RandomForestRegressor(n_estimators=500, min_samples_leaf=2, random_state=seed); predictions
  expm1-ed and clipped at 0.
- PREDICTORS: GLORIA IN-SITU HYPERSPECTRAL Rrs, Gaussian-convolved to the sensor bands, then band
  ratios (convolve_to_bands -> band_ratios). NO SATELLITE PIXEL IS INVOLVED IN THIS NUMBER.
  outputs/ contains no imagery matchup product at all (02_survey_imagery.py left nothing on
  disk), so the retrieval has never been applied to the Magdalena in this repo, and the README has
  no results section for it.
- SPLIT: train_test_split(X, y, test_size=0.30, random_state=seed) -- a plain random 70/30 ROW
  split with NO grouping by water body, site, campaign or date. Their docstring defends it:
  "GLORIA samples come from many independent water bodies worldwide, so there is no temporal
  autocorrelation to leak." That covers temporal leakage, not campaign/site clustering: repeated
  spectra from one water body can straddle the split. So test_r_log 0.896 is an OPTIMISTIC UPPER
  BOUND relative to a leave-water-body-out design, and docs/59 must label it so. There is no
  target leakage and no test-set peeking -- the split is honest, just not grouped.
- COVERAGE: describe_training_set prints "NOTE: no Colombian samples ..." and the module docstring
  says GLORIA contains no Colombian data at all -- the retrieval is transferred and they say so.
  Freshwater types only (FRESHWATER_TYPES = (1, 4, 5)), GLORIA Suspect/Flagged rows dropped, TSS
  clipped to [0.1, 2000] mg/L by config.
- n_samples is the LOADED row count, not the fitted count: the finite/positive filter runs after
  loading (ok = isfinite(X).all(1) & isfinite(y) & (y>0)), so 787/2041 overstate slightly. An
  in-code comment records "5 of 219 test points", i.e. n_test = 219 for a nir variant (=> ~730
  usable rows, not 787). Nominal test sizes would be ceil(0.30 n) = 237 and 613.
- A RandomForest cannot extrapolate, and the trained SSC ceiling is 1033.3 mg/L -- below
  Magdalena flood concentrations (their own load step keeps records up to 15,901 mg/L as
  plausible). The retrieval is capped exactly where the problem is hardest.
- NUMBER OF STATIONS behind 787/2041: NOT DETERMINABLE. The loader has no station concept and
  data/raw/remote_sensing/GLORIA_2022 is absent from the clone.

### 7. outputs/eda/enso_summary.csv -- reproduces exactly (column is `stations`, not n_stations)
SSC (mg/L): La Nina 2010-12 n 14722, median 48.0, mean 213.35545442195354, p90 607.0, 35 stations;
El Nino 2015-16 n 4139, median 36.0, mean 106.1816597825161, p90 204.0, 27 stations.
Q (m3/s): La Nina n 65065, median 21.2, mean 589.2964713876403, p90 1582.0, 108 stations;
El Nino n 32666, median 10.57, mean 298.51300188766066, p90 793.8458541666671, 93 stations.
Wet/dry ratios: SSC median 1.3333333333333333, mean 2.0093437497488122, p90 2.9754901960784315;
Q median 2.0056764427625353, mean 1.9741065469885632, p90 1.992830209664181.
CAVEAT that must survive into docs/59: these are POOLED MARGINALS over unequal windows (3 y vs
2 y) and DIFFERENT station sets (35 vs 27 SSC; 108 vs 93 Q), so the wet/dry ratio is confounded
by station composition. It is not a per-station paired ratio and is therefore not directly
comparable to our docs/34 per-station median rate ratios (4.62 est (a), 2.84-2.95 est (b)) nor to
docs/56 modelled 3.05. Their own inventory (README s3.2) gives 2013 = 3,090 SSC records /
12 stations and 2014 = 3,547 / 21 -- the calibration window is among the thinnest SSC periods in
their record -- and 97 % of SSC records are flagged Preliminar (their s3.2 and s11.4).

### 8. Station-mapping context for the 21 -> 13 drop (their README s6.2)
"229,490 CM records, 71 stations. Mapped two ways: 26 inherit the discharge-validated reach;
33 by nearest centroid, flagged as lower-trust. 57 of 59 stations pass." So the
discharge-validated POOL is 26; only 13 of them clear the 2013-14 window filters, which is why
n_stations is 13 while the README prose says "the 26 discharge-validated stations". The +0.004
delta is real and reproduces exactly; the station count attached to it in the prose does not.

### 9. What I could NOT measure
- Whether stage 3 was skipped or simply found no helping rule (both give the observed
  final == stage2 identity). Settled only by their run log, which is not in the repo.
- Whether the 787 nir rows are a subset of the 2041 no-nir rows, and how many distinct GLORIA
  water bodies / sites they represent: GLORIA raw data is gitignored and absent.
- Any reach-scale or flux-scale comparison with ours: they score CONCENTRATION (mg/L) at a
  reach, we score FLUX; their repo holds no simulated flux time series (no netCDF/parquet model
  output is committed), so no like-for-like flux comparison is possible from disk.
- Whether their 0021217250 zero-SSC bug biases the median in a particular direction beyond the
  +0.0032 shift measured above -- that needs their absent data to diagnose.
