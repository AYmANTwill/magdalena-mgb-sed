# FINAL PASS — make the deliverables catch up to the science

> **How to use.** Open a session in `c:\dev\magdalena-mgb-sed` and say:
> *"Read `docs/agents/PROMPT_final_presentation.md` and execute it."*
> Written 2026-08-13. Single agent, sequential — **do not spawn subagents or run a workflow.**
> Do the tasks in order; each is small. Use `python3.10`, never `python`.

## Why this exists

**The science is finished. The deliverables have not caught up to it.** Phase C completed
2026-08-12/13 with `docs/55` (C4.3 verdict), `docs/56` (C5 — the ENSO contrast, which SUCCEEDED),
`docs/57` (B5), `docs/58` (the rainfall-ceiling bound) and `docs/59` (cross-implementation). The
presentation materials were last touched **before most of that landed**. Four small jobs close the
gap. **This pass adds no new science and runs no fit.**

## STATE — do not re-derive any of this

| | |
|---|---|
| headline result | modelled ENSO contrast **18/18 stations, median rate ratio 3.05**, geo-mean 3.06, range 1.62–4.85 (`docs/56`) |
| observed reference | primary windows, median **4.62** on estimator (a) / **2.84–2.95** on (b); 22/22 station-ratios > 1; range up to ~9 (`docs/34`) |
| why it survives C4.3 railing | the wet/dry ratio is a **ratio**, so α and the LS level cancel **exactly** |
| C4.3 | **RAILED / EXPLORATORY, not adopted** (`docs/55`). est (a) median KGE_ln **−0.118**, est (b) **+0.139** |
| the bar | `F_report ∈ [−0.26, 0.44]`; mean predictor scores **1 − √2 = −0.414** (`docs/45` §3.2, line 307) |
| LS adopted | `ls_formulation = buarque_2015_dg`, `f_LS` = **0.25146** (`docs/37` A3). **ACT 2 moved the engine default** to that field |
| basin gross hillslope erosion | **299.5387 Mt/yr** at adopted `cp_revision`; **248.7298** at the prior one |
| gauge limit | flux gauge set **cannot grow past ~18** — 0 of 43 recovered SSC sites have any discharge record (`docs/57`) |
| unobserved | **66.53 %** of modelled erosion is upstream of no usable SSC station |
| rainfall ceiling | `r ≈ 0.57`, structural; last residual route bounded at max **+0.006 r** (`docs/58`) |
| tests | `python3.10 -m pytest -q` → **154 passed** (the "140" in older docs is stale) |

## TASK 1 — Fetch the ONI 2012–2014 record  *(the only genuinely blocking item)*

`docs/55` §6 records this as **owed**. Until it is filed, the calibration window can only be
labelled **OUT-OF-WINDOW (by date)** and **NOT out-of-phase** — which weakens the strongest claim
C5 has, that it is strictly out of sample.

- NOAA CPC's ONI v5 web page is **JS-rendered** and defeated a previous attempt. Try the
  plain-text / ASCII ENSO products, or a NOAA PSL Niño-3.4 mirror, instead of the HTML page.
- Record **all four** of: the monthly ONI values for 2012-01 … 2014-12, the **exact source URL**,
  the **retrieval date**, and the **threshold** used to classify a phase (state it, e.g. ±0.5 °C
  over N consecutive overlapping seasons — and cite whose definition it is).
- Write them into `data/processed/report_C4.json` and note the fetch in `docs/55` §6.
- **Then say plainly which it is:** was CAL 2013-01-01…2014-12-31 ENSO-neutral or not? If neutral,
  the out-of-sample claim is clean. If not, qualify it — do not overstate it.
- **If the fetch fails again, that is a finding.** Record it as a named open item, keep the
  out-of-window label, and move on. Do not invent values.

## TASK 2 — Bring the presentation materials through to the ending

Owners: `docs/14_presentation_plan.md`, `docs/24_presentation_outline.md`,
`docs/27_presentation_script.md`, `docs/28_presentation_explained.md`.

1. **First check where they stop.** They were updated 08-11/08-12; `docs/55`–`docs/59` landed after.
   If the deck stops at C3 or "C4 setup", it is missing the part where the study succeeds.
2. Add the ending: **C4.3 railed and was not adopted → why that is a finding, not a failure → C5
   reproduces the observed contrast out-of-sample → B5 proves the gauge network cannot be grown.**
3. **`docs/28` carries 2 kill-list hits** (grep it, see the kill list below). Fix them.
4. Confirm **no slide, table or figure carries t/km²/yr** — the `docs/23` §13.2 yield embargo is in
   force, absolute flux only.

## TASK 3 — Regenerate the deck figures on the adopted configuration

`figures/deck/` and `*.pptx` are gitignored and **regenerable from `scripts/`** — find the
generating script and run it. **ACT 2 moved the engine default LS to `V4_dg`**, so any figure
showing LS levels or basin loads is on the *old* default and is stale. Re-check each figure that
prints a load, an LS value or an α, and say in your report which were stale and are now current.

## TASK 4 — Fix the observed-estimator reference in one sentence

`docs/56` and the deck must not silently pick whichever observed estimator flatters the model. The
modelled 3.05 matches estimator **(b)** closely and sits **below** (a)'s 4.62. `docs/34` registers
*"gate on one, report both."* Add one explicit sentence naming the reference estimator and printing
**both** observed values beside the modelled one. Nothing more.

## TASK 5 — *(optional, cheap, mechanical)* apply the `docs/59` fix list

`docs/agents/FIXLIST_docs59.md` is a pre-verified work order: 4 confirmed findings, 11 MEDIUM/LOW,
1 refuted. Every item was already independently confirmed or refuted — **do not re-audit**. A1 is
HIGH and removes `docs/59`'s only new positive result (the narrowing to `K`), which is the correct
outcome. Apply A in full, apply B only where the locator is unambiguous, never apply C.

## THE FRAMING — settle this before writing a slide

**The headline is the ENSO contrast, reproduced out-of-sample and robust, PLUS the
non-identifiability of the absolute level as a finding — not a calibrated model.**

Say plainly: the sediment equation multiplies everything by seven constants that the observations
cannot separate (design matrix condition number = ∞; only the product Π is identifiable), so a
fitted α would hide errors rather than find them. Two independent implementations of the method on
this basin reached that conclusion by different routes (`docs/59`). The absolute tonnage is
therefore reported as unresolved with a stated reason, while the contrast — a ratio, immune to
every unidentifiable multiplier — is the result.

Present the open items as open: the **upstream over-production** (`docs/35` §6.1 names **five**
suspects, including the delivery step — not four), and the unresolved absolute level. A study that
says *"here is the contrast, here is the proof the level is not identifiable from this network, and
here is what would settle it"* is stronger than one that quietly tunes a coefficient.

## KILL LIST — must not appear as current anywhere

Acceptable only inside a strike-through or an explicitly-labelled superseded block.

`2.37× – 3.00×` · `×0.333 – ×0.421` · α reference `3.9–5.0` · band `2.0–9.9` · hard stop
`11.8–14.9` · proxy loads `104.8 / 82.8 / 126.1 / 99.7` Mt/yr · `±38 %` Π band · `SE 0.1644 ln` ·
`σ_r = 0.465` as a per-station residual sd · `k_min 0.00216 / 0.0209 / 0.0104` /km · `2.12× over
348.4 km` · the uncited **"mountainous LS 2–10"** band · the uncited **SDR 0.05–0.30** band ·
**"the model is ~2× under-erosive"** (direction WITHDRAWN, `docs/37` A1.9 — the residual's direction
is **UNKNOWN**) · `min(m, 0.5)` labelled "Buarque eq. 14" · any product of single-lever factors
quoted as the joint factor (joint/product = **×1.34762**).

Never quote a load without its **convention AND its `cp_revision`**.

## CONSTRAINTS

- Do **NOT** change an engine default, run a fit, or produce a new α̂.
- Do **NOT** modify `data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv`, `urh_ls2d_variants.csv`, or
  anything in `data/processed/sim_calibrated_v2/`.
- Do **NOT** touch `notebooks/` or `src/nbgen/` — a separate session owns the notebook coherence
  pass (`docs/agents/PROMPT_notebook_coherence.md`) and will collide with you.
- Do **NOT** edit a frozen pre-registration (`docs/33`, `35`, `42`, `45`, `46`) except through its
  own amendment slot.
- Introduce no materiality bar, band or tolerance, and reconstruct none (`docs/52` §7).
- **Verify from executed output, never from an exit code.**

## UNCOMMITTED WORK FROM THE PREVIOUS SESSION — review it, do not clobber it

`git status` will show: `.gitignore` (a zip guard — keep it), `docs/59_cross_implementation_comparison.md`,
`docs/agents/FIXLIST_docs59.md`, `docs/agents/PROMPT_notebook_coherence.md`, several
`docs/agents/journal_x59-*.md`, plus `_eq/` and `scripts/build_report_pdf.py` from an earlier
Desktop session. **Commit deliberately in logical groups — do not `git add .` blindly.**
`magdalena_share_for_colleague.zip` (306 MB) is gitignored on purpose; keep it that way.

## REPORT BACK

1. The ONI verdict — neutral or not — with the source URL and retrieval date, or the named failure.
2. Where the deck stopped, and what you added.
3. Which figures were stale and are now regenerated.
4. Any kill-list hit you found and fixed, with file and line.
5. Anything you could not settle, named as an open item.
6. Files changed, and what you committed.
