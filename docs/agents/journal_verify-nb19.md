# journal — `verify-nb19` agent

**Task.** Lens: do notebook 19's CLAIMS match its EXECUTED OUTPUTS? Read stored outputs from
`notebooks/19_c3_gate_and_c4_setup.ipynb` JSON (do NOT re-execute), check markdown prose
against them. Interrogate (a) every numerical claim, (b) the self-checks for tautology,
(c) all 19 figures for accompanying analysis, (d) any unfitted Williams α = 11.8 presented as
calibrated, (e) explanation of technical terms.

## Log

- **2026-08-11 start.** Read CLAUDE.md, docs/00_INDEX.md. Notebook has **82 cells total**
  (29 code cells, hence "29/29"). Dumped cells + stored outputs to scratchpad
  `nb19_dump.txt` (220 kchars) with `dump_nb.py`. Read the whole dump.
- **Figure census (measured, not eyeballed).** 19 code cells emit exactly one `image/png`
  each: cells 7, 12, 15, 20, 25, 28, 31, 34, 40, 43, 46, 50, 53, 57, 63, 66, 69, 72, 75.
  **Every one is followed immediately by a markdown cell carrying the full
  What-is-plotted / What-it-shows / What-it-means triptych.** Item (c) passes structurally;
  the defects are in *content*, not coverage.
- **Recomputed** in a scratch python3.10 session: the β-inversions of cell 31, the cell-20
  exp(D) sweep, the NEH ratios, `1.239/0.0039`, the reading-B bracket at DR = 0.33 vs 1/3,
  the LS reciprocals, the Momposina path arithmetic, χ² p-values for the Q's.
- **Cross-checks against the record:** `docs/35` §5.4 (the 0.8875/0.8097 pair — they are
  `R_AMS^0.56`, not R_AMS), `docs/45` §415 (the 684.4 km figure), `docs/42` §4.1 (801.1 km),
  `journal_adj-alpha-role.md` L203–207 (the 42.7 % β-stop — **corroborated**, so the
  "42.7 points" line is NOT a defect despite coinciding with the `ok` share),
  `journal_adj-ratio.md` L132–137, L201–202 (0.203–4.550, 18 of 24, the EL PROFUNDO
  sensitivity — all carried correctly).
- **Dead ends / things I checked and cleared:**
  - CAL-8 drained area 13,862 km²: the printed per-station `up_area_km2` sum to 13,929.6, and
    13,929.6 − 68.0 (the nested BOCAS 22017030) = **13,861.6** ✓ — the hardcoded figure is the
    union, not a transcription error.
  - The funnel 79/28/18/13/9/8 and the 5 lost stations reconcile exactly (4 lost at filter (c),
    1 at (d)) ✓.
  - The "guard hard-stops 43.4 %, of which 42.7 points is the β stop" line looked like a
    copy of the `ok` share (182 = 42.7 %); the source journal independently reports
    "beta hard-stop trips on 182/426 = 42.7 %". **Not a defect.**
  - (d) — I found **no** place where the unfitted α = 11.8 is dressed as a calibrated result.
    It is flagged unfitted in cell 2's banner, cell 0, cell 4, §8 item 6 and a self-check.
    The nearest hazard is cell 46's `alpha_needed` column (14.21 / 7.10 / 2.84), which is
    labelled "α that keeps Π unchanged", not a fit.

## Findings (see the returned structure for the full list)

Ranked: the §5.4 mandatory statement contradicted by the notebook's own §2.4 like-for-like
result; cell 32's runoff-ratio numbers contradicting cell 31's printed output; cell 21's
exp(D) range; the 31 "integrity assertions" of which 3 are the literal `True` and several
more are identities; the 322-vs-318 title/legend clash; the reading-B 1.332–1.490 vs computed
1.319–1.475; the undefined 0.8875/0.8097; the sign-test power claim at n = 4; the Momposina
655-vs-684.4 km arithmetic; the 18-ticks-called-17 figure with synthesised positions;
terminology gaps (estimator (a)/(b), "EL PROFUNDO precedence", minibacia/URH, MOCOM-UA, DDS).

Fixes belong in the **generator** `src/nbgen/make_nb19.py` (line numbers given in the
findings), then a re-execute — not in the .ipynb.
