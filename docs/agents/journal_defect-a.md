# journal — defect-a (resolve Defect A of docs/46 §1.1 with numbers)

Started 2026-08-11. Task: deliver (a) corrected eq.14 lever factor V2b/V0, (b) corrected joint
V4/V0, (c) corrected "how far our LS sits above the source", (d) area vs EROSION fraction below
the 5% breakpoint, (e) one-line verdict. Write docs/49_defect_a_resolution.md.

## Inputs inherited
- Harness result (ls-variants-harness) already measured V2a=20.004562 (x0.5024724),
  V2b=20.108817 (x0.5050912), V4=16.775413 (x0.4213630), V4'=16.749164 (x0.4207037),
  V0=39.8122601. Harness note: the published x0.421 was ALREADY the step (V4), not the cap.
- docs/47 §4.3 supersedes the docs/37 bracket with erosion-weighted [0.25146, 0.43194].

## Plan
1. Read scripts/c3/ls2d_variants.py + summary json + ls2d.py to confirm what V2a/V2b/V4/V4' are.
2. (d) is the only genuinely NEW measurement: area fraction and EROSION fraction below tan-theta
   0.05 (and the 1%/3% sub-steps). Erosion weights must come from the engine, not invented.
3. Write docs/49.

## Step 1 — erosion weights + f_ero for all eight variants (2026-08-11 22:21)
New script `scripts/c3/ls_erosion_weights.py` (committed-quality, NOT scratchpad — docs/00 §6
records scratchpad-only analysis code as a known loss mode; journal_ls-impact lost its harness
that way). It (i) runs `simulate_sediment` at adopted defaults on the frozen drivers read-only,
(ii) converts the variant CSV's f_area proxy into the EXACT f_ero, (iii) does a per-cell slope
class pass. Both gates PASS:
- GATE 1 basin gross erosion 299.5387088405831 Mt/yr vs docs/37 A1.3 299.5387 (diff 8.8e-6).
- GATE 2 f_ero reproduces docs/47 §4.3: V1 0.36243 (pub 0.3624), V2a 0.51748 (0.5175),
  V3 1.69405 (1.6941), V4 0.43194 (0.43194). All PASS at 5e-4.

NEW (never measured): f_ero(V2b eq.14 step) = 0.52204 · f_ero(V4' cap joint) = 0.43038 ·
f_ero(V5) = 0.76676.

Defect A, erosion-weighted:
- single lever: 0.52204 (step) vs 0.51748 (cap) → |ln| = 0.00877, 18.7x inside the 0.1644 bar.
- joint: 0.43194 (step) vs 0.43038 (cap) → |ln| = 0.00362, 45x inside the bar.
CONFIRMED independently that the published joint x0.421 was ALREADY the step (V4 16.775413 vs
V4' 16.749164; journal_decide-ls-resolution line 365 prints 16.775). So that journal's table
mixed the two objects: line 362's single-lever row is the CAP, line 365's joint row is the STEP.

Files written: data/processed/urh_erosion_weights.csv (32,782 rows), data/processed/ls_defect_a.json.
Protected files (urh_ls2d.csv, minibacia_ls2d.csv, h2e_drivers.npz, parameters_H2E.csv) hashed
before and after: UNCHANGED.

## Step 2 — per-cell slope-class pass (running)
Crossover where min(m_cont,0.5) == eq.14's 0.5 step solved exactly: tanθ = 0.08933250413265519
(8.9333 %), root of (sinθ/0.0896) = 3 sinθ^0.8 + 0.56. Classes: <1 % / 1-3 % / 3-5 % /
5 %-8.9333 % / >=8.9333 %. Erosion split is exact by linearity: E(S) = Σ_u E_u ·
(Σ_{j∈S∩u} LS_j w_j)/(Σ_{j∈u} LS_j w_j).

## Step 3 — the deciding measurement (2026-08-11 22:37). All numbers final.
Cell pass over 30,235,916 cells, 35 s (after ~4 min DEM/pit-fill/D8).

| class (Sf=100 tan) | area % | erosion % |
|---|---|---|
| <1 % | 11.993 | 0.041 |
| 1-3 % | 12.235 | 0.260 |
| 3-5 % | 6.280 | 0.428 |
| 5-8.9333 % | 7.350 | 1.411 |
| >=8.9333 % | 62.142 | 97.860 |
| **below 5 %** | **30.507** | **0.729** |
| **below crossover** | **37.858** | **2.140** |

Verified from the accumulators (not assumed): below the crossover sum(LS_V2a*w) == sum(LS_V0*w)
exactly (the cap does nothing there); above it sum(LS_V2b*w) == sum(LS_V2a*w) exactly (the step
does nothing there). The two objects act on DISJOINT terrain. On the sub-crossover erosion the
step raises the LS-weighted total by x1.2132; times the 2.14 % share -> +0.88 % on the basin
factor. Counterfactual: to reach the 0.1644 bar the sub-crossover terrain would need to carry
83.8 % of the source field's erosion; it carries 4.1 %.

### The thing that DOES matter, found while measuring the thing that does not
docs/46 (R6) - eq. 14's Sf units, untested. Measured as a labelled SENSITIVITY (single lever,
erosion-weighted): percent 0.52204 | degrees 0.51369 (|ln| 0.0161, inside the bar) | m/m 0.17175
(|ln| 1.1117, 6.8x the bar, basin 51.44 Mt/yr). No verdict on which reading is right - the
source pp. 46-48 were not obtained. But the live risk in the m lever is the UNITS, not the cap.

## Dead ends / traps hit
1. First full run completed the measurement then died in print() on 'θ' under cp1252, and the
   background wrapper still reported exit code 0 (the `; echo $?` chain). Caught by reading the
   log, not the status. Exactly the trap the brief names. Fixed by removing the character.
2. My first counterfactual algebra was wrong (I applied the below-crossover share against a base
   of 1 instead of f_ero(V2a)). Recomputed: the 83.8 % figure is the share of the SOURCE field's
   own erosion, not of V0's. Stated that way in docs/49.

## Deliverables (docs/49_defect_a_resolution.md written)
a) eq. 14 = x0.5051 area / x0.5220 erosion (published x0.502 was the cap: 0.5025/0.5175).
b) joint V4/V0 = x0.42136 area / x0.43194 erosion; the published x0.421 ALREADY was the step.
   V4' (cap joint) = 0.420704 / 0.430381, never measured before.
c) gap 2.3151x - 3.9768x (docs/47 §4.3 reproduced behind two gates). Defect A's own share of
   the move at the x0.421 end: 2.3235 -> 2.3151, -0.36 %. Prediction held in sign, immaterial in
   size, and ZERO as applied to the published number.
d) below 5 %: 30.507 % area / 0.729 % erosion. Below the true crossover: 37.858 % / 2.140 %.
e) x0.421 is NOT wrong; the 2.37x-3.00x bracket is, but not because of Defect A. Defect A is
   worth +0.018 on the alpha reference (5.079 -> 5.097). The defect is a LABEL defect.

Nothing adopted, no default moved, no git command run. Protected files hashed before/after by
the script: UNCHANGED.
