# journal — verify-gate-logic

Agent: adversarial verification of the C3->C4 gate decision (docs/43).
Started 2026-08-11.

## Task
Try to break docs/43's decision. Four attack lines:
 a) is "reclassify level as calibration target" distinguishable from "absorb error into fitted alpha"?
 b) does Amendment A2 rest on primary sources or on this project's own docs? follow >=2 citations to origin.
 c) are the three blocking guards actually blocking? find a fit that passes all three and is still wrong.
 d) any uncited band/threshold load-bearing in the decision?

## Progress log
- Read CLAUDE.md, docs/00_INDEX.md, docs/43 in full.
- Note: docs/45_c4_preregistration.md exists (2026-08-11 12:30) and is NEWER than docs/43 (12:10).
  Not in the index. Must check whether it already transcribes P1/P2/P3 or contradicts them.

## Reads completed
docs/43 (full), docs/37 A1 / A1.9 / A2 (full), docs/42 §1-§9, docs/45 (§0-§3, §6-§7),
journals adj-ratio / adj-alpha-role / adj-c4-feasibility.

## Measurements I ran (scratchpad artifacts of the adj-ratio lens are still on disk)
Source: <session-scratchpad>/adj_ratio_station_window.csv (72 station-window rows, produced by
adj_ratio.py which uses ms.load_geometry at the adopted cp_revision and SedParams() defaults, i.e.
exactly the docs/45 C4 configuration: k=0, C=docs/41 central, alpha=11.8).

1. Between-station spread of the LEVEL residual ln r (r = obs/sim), station medians:
   all stations est (b) n=16 sd = 1.4175 ln ; est (a) n=15 sd = 1.2643 ln
   CAL 8       est (b) n=8  sd = 1.7159 ln ; est (a) n=7  sd = 1.5419 ln
   => SE(fleet-mean level) on the CAL 8 = 0.6067 ln (b) / 0.5828 ln (a), NOT 0.1644 ln.
   docs/43 §3.2 / docs/45 §2.2's "+-38 % at 95 %" is understated ~3.7x in log units
   (true 95 % factor 3.28x, i.e. -70 %/+228 %).
   Cause: sigma_r = 0.465 is docs/42 §4.2's OBSERVATION-noise floor (estimator disagreement).
   It excludes model structural error, which is the dominant term.

2. G1.2 regression run on the same real data (ln r ~ Lw, Lw from docs/42 §4.1):
   all-18 form  n=16 resid sd 1.456 ln  k_min(95%) = 0.00680 /km => 10.5x over 345.8 km
   CAL 8 form   n=8  resid sd 1.837 ln  k_min(95%) = 0.08262 /km => 118.5x over 57.8 km
   Registered:  0.00216 /km => 2.12x, and 0.0209 /km => 3.54x. Overstated 3.1x / 4.0x.
   Fitting Pi removes only a constant, so it cannot change SE(k). G5's second leg is vacuous.

3. Level the CAL 8 implies for a k=0 (SDR=1.0) configuration:
   geo-mean r = 0.0721 (est a, the registered fitting estimator) / 0.0966 (est b)
   => alpha_implied = 11.8 x r = 0.85 (a) / 1.14 (b); per-station range 0.08 - 8.7.
   docs/45 §2.1 box is [2.0, 30.0] and docs/35's hard stop is alpha < 3.9.
   The level the fit set implies is BELOW the box floor.

4. Deposition-free alpha at the ADOPTED cp_revision:
   11.8 x 144/299.5387 = 5.673 ; 11.8 x 184/299.5387 = 7.249  -> [5.67, 7.25]
   docs/43 §3.4 quotes [6.83, 8.73], which is 11.8 x {144,184}/248.730 = the PRIOR C.
   Reading-B alpha [7.92, 8.86] (A1.9.4) IS at the adopted C.
   So "These overlap" is false at the adopted C: [5.67,7.25] and [7.92,8.86] are disjoint.

5. Primary-source verification (attack b): PASSES.
   fagundes2018.txt L3773 = eq.11 "coeficientes de ajuste, ora adotados como 11,8 e 0,56"
   fagundes2018.txt L4907 = §6.3.1 "parametros adotados como calibraveis ... alpha e beta ... TKS"
   fagundes2018.txt L4189 = search prior "entre 2,0 e 25,0 ... entre 0,2 e 1,7 ... TKS 0,1 e 3,0"
   swat2009.txt L24759/24765/24804 = A1.9.1's three verbatim quotes.
   All four verified against the PDFs. BUT: the PDFs and the parse scripts live only in a session
   scratchpad, not in the repo -- the docs/00 §6 known-loss mode.

6. Process check: docs/42 §9 still reads "Amendments | none" and its §4.2/§9 still register
   CAL 13 and k_min 0.0104. git log shows c4.1, c4.2 (docs/45) and nb19 already committed and
   "C4 is under way". docs/43 §3.1 made P1/P2/P3 blocking on a docs/42 §9 transcription that
   has not happened.

7. docs/43 §3.1 P1 says "not 0.0096 /km"; docs/42 §4.2 actually prints 0.0104 /km.
   (lens journal discloses the 7 % method difference; docs/43 does not.)

## VERDICT (written after the measurements above)

SURVIVES my attack:
 - (a) in principle. docs/43 §1.3 leg 1 destroys the instrument by which a fitted alpha would
   "look fine" (43.4 % STOP over the source's own 426 published adopted pairs; 97.7 % inside the
   "expected" band only because the source prior [2,25] contains it). I verified the underlying
   Fagundes quotes verbatim. The Pi-invariance argument is also sound: a later C3.1 decision on
   the LS LEVEL re-partitions Pi between alpha and LS and leaves predictions unchanged, so
   confining the surviving defect to the LS SHAPE is correct, not a dodge.
 - (b) largely. Four citations followed to origin and verified verbatim. Caveat: sources and
   scripts are scratchpad-only; leg 2 is a self-citation.
 - §1.5's refusal to close on three accumulated retirements.

BREAKS:
 1. the level the CAL 8 implies (alpha 0.85-1.14) is BELOW C4's registered box floor 2.0
 2. the Pi band and every guard power number are computed at an observation-noise floor
    3.1-3.9x below the measured residual scatter; G1.2 excludes nothing
 3. P1/P2/P3 cannot fail a fit; docs/45 satisfies all three while asserting SDR = 1.0
 4. "these overlap" (§3.4) mixes two cp_revisions; disjoint at the adopted one
 5. §5.1's registered C5 statement embeds the artifact §5.3 forbids
 6. the blocking precondition was not transcribed and C4 started anyway
 7. P1 misquotes the number it instructs be corrected (0.0096 vs docs/42's 0.0104)
