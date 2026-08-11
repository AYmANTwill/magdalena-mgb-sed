# Journal — research-synthesis

GOAL: adjudicate three research lenses (empirical peak-gap diagnosis, sub-daily data
reconnaissance, method/literature) into ONE ranked, decision-ready document at
`docs/36_peak_deficit_options.md`. No new research; adjudication only.

Constraints acknowledged:
- Touch ONLY `docs/36_peak_deficit_options.md` + this journal.
- No git add/commit/push. No calibration search. No hydrology re-run.
- Yields in t/km2/yr EMBARGOED; absolute flux only.
- Report effects at BOTH fleet and per-unit scale.
- Verify from executed outputs, not exit codes.

## Checklist
- [x] 1. Create journal
- [x] 2. Read the doc context I must be consistent with: 33 (s5.1, s8), 35 (q_peak
      prereg — may already cover option 3), 30/31 (Phase C plan), 26 s5.1, 23 s13.2
- [x] 3. Verify the lens-1 numbers exist in the artifacts on disk
      (data/processed/peakgap/summary.json, per_gauge.csv, events.csv)
- [x] 4. Draft docs/36 — sections 1..6 per task
- [x] 5. Self-check: every option has an explicit NOT-worth-doing condition;
      top-ranked option has a pre-registration sketch
- [x] 6. Structured output

## Log

### Step 1 — journal created (this file)
docs/agents/ already contains 27 journals; docs/ already contains 35 numbered docs, so
36 is the correct next number and does NOT already exist (verified by `ls docs/`).
Note: `docs/35_qpeak_preregistration.md` EXISTS — must read before ranking, because the
"sub-daily peak parameterisation" option may already be pre-registered elsewhere.

### Step 2 — context read (executed output, not assumed)
- `docs/35` §3(ii)/§4: the SCS triangular unit hydrograph IS ALREADY ADJUDICATED and
  **REJECTED for production** (registered 2026-08-11). `q_peak = Qsur·a/86.4` at
  a_p = 0.0081 km². §6 forbids α/β absorbing the peak deficit (hard stop α > 35.4).
  ⇒ task candidate "sub-daily peak parameterisation (unit hydrograph)" must be reported as
  ALREADY DECIDED, not re-opened.
- `docs/35` §2: no slope field exists basin-wide; the only DEM covers 17.4 % of minibacias
  and is the FLAT 17.4 %. t_c not computable ⇒ UH not computable today.
- `docs/33` §5.1: a successful refit forces re-running C0 (new parameters_*.csv,
  q_gauge_*.npz, metrics_fleet.csv, regenerated h2e_drivers.npz 521 MB) and **everything
  downstream of C0 already run**. C1 and C2 are NOT invalidated (§5.3).
- `docs/33` §8: R_AMS 0.820 → 0.94–1.00 achievable, but cost ΔF −0.0319 vs a 0.02 budget
  and two new rails (kc_mult 0.975, lai_mult 0.006).
- `docs/31` §"Dependencies": core path ≈ **8–12 sessions**; C0/C1/C2 done ⇒ **≈5–8 left**.
- `docs/31` §C3.5 + `docs/30` line 53: implementation B's `musle.py`/`sediment.py` are
  external, NOT in this repo ⇒ the "local-inertial routing (implementation B)" candidate
  has no acquirable code today.

### Step 3 — lens-1 numbers verified against artifacts on disk (executed)
`data/processed/peakgap/summary.json` opened and every quoted figure checked:
obs POT 2236, sim 1285, ratio 0.57469, missed 1829, missed_frac 0.81798 ✓;
timing 0.0505/0.1422/0.1820/0.2075/0.2433/0.2876/0.3117/0.3381 ✓;
area ρ +0.01762 p 0.8919 n 62, terciles 0.7925/0.8292/0.8408 ✓;
P3_pct rb −0.57847 p 1.25e−74, P30_pct rb −0.38829, intensity_ratio 0.14562 vs 0.19450
rb −0.33913 p 8.6e−27 ✓; duration 0.84899/0.75967/0.68696/0.61039 ✓;
season χ² 63.091 dof 11 p 2.46e−09, Aug 0.94340 Sep 0.93396 Oct 0.76596 Nov 0.75439 ✓;
classes absent 737 / sub-extreme 631 / sim-extreme 461, median sim/Q5obs 0.61628 ✓;
i_obs_response_per_mm 0.56757 vs 0.28571 rb +0.39682 ✓;
f_storm_x_antecedent top-storm × dry-P30 n 130 miss 0.76154 ⇒ **99 events** ✓;
x_enso 0.71619 / 0.88710 / 0.83669 ✓; h_storm_confirmed n 257 miss 0.51751 ✓.
NEW (per-unit scale, computed here from `per_gauge.csv`, n = 63):
per-gauge miss fraction mean 0.7696, median **0.7895**, IQR 0.6545–0.9303, min 0.25,
**8 of 63 gauges miss 100 % of their observed POT**, 5 of 63 miss < 50 %,
**4 of 63 gauges simulate ZERO POT events**; per-gauge R_POT median 0.5672 (IQR 0.155–1.141).

### Step 4 — drafting docs/36_peak_deficit_options.md
Ranking currency fixed BEFORE scoring, so the table cannot be reverse-engineered:
gain = ceiling on how many of the 1,829 missed events the option could address, with the
measured basis named; feasibility = does the data AND the code exist today; cost in
sessions against the ≈5–8 remaining; and Phase-B-reopen yes/no.


### Step 5 — self-check (executed)
`grep -c "NOT WORTH DOING IF" docs/36_peak_deficit_options.md` → **7**, one per option
(§3.0 accept, §3.1 CHIRPS audit, §3.2 densify, §3.3 sub-daily, §3.4 disaggregation,
§3.5 Hortonian, §3.6 routing). §5 carries the pre-registration sketch for the top-ranked
INTERVENTION (the CHIRPS storm-presence audit); rank 0 needs none because it is already
registered in docs/35 §5.3/§6. File is 792 lines. `git status --short docs/` shows
`?? docs/36_peak_deficit_options.md` and `?? docs/agents/journal_research-synthesis.md` —
no other file touched by this session. No git add/commit/push run. No calibration launched.
No hydrology re-run. No t/km²/yr yield computed anywhere in the document.

### Adjudication decisions I made that the lenses did not (recorded so they can be challenged)
1. **Ranked "accept and propagate" as the incumbent (rank 0) and the CHIRPS storm-presence
   audit as rank 1 among interventions.** The audit is not in any lens's option list in this
   form — lens 1 proposed re-running the POT diagnosis on a CHIRPS-*forced* run (which needs
   a hydrology re-run). I reduced it to a pure data test that needs NO engine run: does an
   independent product see the storms, measured on the frozen event table. That is the cheap
   half of lens 1's falsifier and it is the only thing that breaks §2.5.1's circularity.
2. **Option 2 (densification) — I added a structural objection no lens raised:** basin
   automatic-station counts are ~53–66 in 2011 (La Niña) vs ~75–84 in 2015 and ~103–120 in
   2016 (El Niño). Densifying with a network whose density nearly doubles between the two
   contrast windows injects a non-climatic trend into the study's headline result. This is
   why option 2 ranks below a ½-session diagnostic despite having the largest gain ceiling.
3. **Option 6 (local-inertial routing) was researched by NO lens.** I adjudicated it on
   structure (routing conserves volume, is downstream of generation, and is upstream of
   nothing MUSLE reads — the source term is at pixel/hillslope scale per docs/35 §4) and
   flagged the weaker evidence base in the text. Also noted the sign is not clearly positive:
   better floodplain hydraulics in the lower Magdalena would ATTENUATE, and the project has
   already caught celerity absorbing floodplain storage.
4. **Fourth, independent ground for docs/35's UH rejection**, from lens 1: any q_peak formula
   is monotone in daily Q_sur, so it cannot create the 737 ABSENT events. Recorded in §3.7 as
   reinforcement, NOT as a re-opening.
5. **Numbering collision flagged:** docs/33 §5.2 reserved 36 for "C5.4 ENSO contrast results".
   This file takes 36; C5.4 must take 37+. Stated in the doc header.
6. **Two corrections propagated in §7:** (a) the "43 %" figure is a COUNT deficit — the
   event-identity deficit is 81.8 % and 68.3 % of SIMULATED peaks are unmatched; both must
   be quoted together (affects docs/33 §8, docs/35 §5.2, docs/31). (b) the fleet median hides
   8/63 gauges missing 100 % of their POT and 4/63 simulating zero — a per-unit fact absent
   from every prior write-up.

### What I did NOT do
- Did not re-open docs/33 §8 (refit), docs/35 §4 (q_peak), or docs/32 (CHIRPS merge). All
  three are recorded in §3.7 as already adjudicated.
- Did not attempt C3.5 (implementation B `musle.py` absent from repo) — recorded as STILL
  BLOCKED for the fourth time.
- Did not compute any new statistic beyond the per-gauge miss-fraction distribution read from
  `per_gauge.csv` (a read-only aggregate of an existing artifact).
