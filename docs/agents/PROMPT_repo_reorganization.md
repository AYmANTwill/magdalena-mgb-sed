# REPO REORGANIZATION & COHERENCE PASS — one clean, academic, reproducible repository

> **How to use.** Open a fresh session in `c:\dev\magdalena-mgb-sed` and say:
> *"Read `docs/agents/PROMPT_repo_reorganization.md` and execute it."*
> Written 2026-08-13. Run in **STAGES**, not one shot. Use `python3.10`, **never** `python`.
> `jupyter` is **not** on PATH — execute notebooks only with
> `python3.10 -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 <nb>`.
> **This is a big, destructive-capable task. Nothing is deleted until TASK 1's triage plan is
> written, reviewed, and each deletion is justified in one line. Get the decisions right first.**

## The goal, in one sentence

Turn this repository into a **coherent, academic, reproducible whole** — one consistent narrative,
no contradictions, no dead weight in the live tree, every notebook scored and corrected, and a
**roadmap that a new reader can follow from zero to the result** — *without* destroying the
project's audit trail, breaking its generated notebooks, or touching its frozen artifacts.

## 0 — Orient before touching anything (mandatory reading, in order)

`CLAUDE.md` → `docs/00_INDEX.md` (the map + WHERE-IS-IT table) → `notebooks/README.md` →
`progress_map.html` (live status) → `docs/16` §6 (the traps reference) → `docs/20` (reproduction
guide). **If a doc disagrees with the index, the doc wins.** Read the owning doc for anything you
touch. Do not re-derive any result — the canonical state is fixed in the table below.

## STATE — the canonical facts (do NOT re-derive; use these to detect mismatch)

| | |
|---|---|
| Phase A (inputs) | complete |
| Phase B (hydrology) | **CLOSED on H2E** (F = 0.25931), at the **r ≈ 0.57** rainfall-input ceiling; El Niño skill-over-climatology **−0.0005** |
| LS adopted | `ls_formulation = buarque_2015_dg` (V4_dg); **`f_LS` = 0.25146** erosion-wtd / 0.2446790094097074 area-wtd; ACT 1 materialised it, ACT 2 moved the engine default to it |
| basin gross hillslope erosion | **299.5387 Mt/yr** at adopted `cp_revision`; **248.7298** at the prior one — **never quote a load without its convention AND `cp_revision`** |
| C4.3 (sediment calibration) | **RAILED / EXPLORATORY, not adopted.** est (a) median KGE_ln **−0.118**, est (b) **+0.139** (same sign ⇒ not indeterminate); α wants ≈ 0.48 (below the floor); design-matrix condition number **∞** (only Π identifiable) |
| C5 (ENSO contrast) | **REPRODUCED, 18/18 stations, median rate ratio 3.05×** (range 1.62–4.85; robust across β and both window pairs). Observed: 22/22 > 1, median ~3–5 primary / ~5–9 sensitivity. **This is the headline result.** |
| gauge limit (B5) | flux gauge set **cannot grow past ~18** — 46 SSC sites geocoded, 0 have any discharge record |
| rainfall ceiling | the last lever bounded at **≤ +0.006 r** (`docs/58`) — the ceiling is structural |
| ONI | recorded 2026-08-13 (`report_C4.json`): CAL neutral-core (2013), weak edge signals (early 2012, late 2014) |
| tests | `python3.10 -m pytest -q` → **154 passed** (older docs say 140/82 — stale) |
| result docs | `docs/55` (C4.3 verdict) · `docs/56` (C5) · `docs/57` (B5) · `docs/58` (ceiling bound) · `docs/59` (cross-implementation) |
| deliverables | `MGB-SED_complete_report.pdf` (report) · `MGB-SED_Magdalena_FIGURES.pptx` (deck) — both **gitignored/regenerable** from `scripts/` |

## HARD RULES — these bind every action and cannot be overridden by the cleanup goal

1. **Notebooks 10–19 are GENERATED** by `src/nbgen/make_nb10.py … make_nb19.py`. **NEVER hand-edit
   a notebook in that range** — the next regeneration silently destroys the edit. Edit the
   **generator**, rerun it, execute the notebook, verify from executed output, then confirm the
   source-identical property still holds. Notebooks 01–09 are hand-written (no generator) — edit
   those directly, but they are the oldest text and where stale claims hide.
2. **Do NOT delete the audit trail.** This project deliberately preserves superseded material via
   strike-throughs and "superseded" blocks, and keeps a register of refuted hypotheses. Superseded
   ≠ irrelevant. Historical docs that record *how a verdict was reached* are KEEP-or-ARCHIVE, never
   DELETE. When in doubt, **archive, do not delete** (TASK 1).
3. **Do NOT modify frozen artifacts:** `data/processed/urh_ls2d.csv`, `minibacia_ls2d.csv`,
   `urh_ls2d_variants.csv`, anything in `data/processed/sim_calibrated_v2/`. Do NOT edit a frozen
   pre-registration (`docs/33, 35, 42, 45, 46`) except through its own amendment slot.
4. **Yield embargo** (`docs/23` §13.2): absolute flux only — t/day, Mt/yr, mg/L, m³/s. **No
   t/km²/yr referenced to a gauge, anywhere.** Model-internal specific erosion, if present, must be
   labelled as such.
5. **Never quote a product of single-lever factors as a joint factor** (joint/product = ×1.34762).
   **Never quote a load without its convention AND `cp_revision`.** "CITED is not validated;
   fitted is not validated."
6. **Introduce no uncited band, threshold or materiality bar, and reconstruct none** (four have
   been retired on this rule).
7. **VERIFY FROM EXECUTED OUTPUT, never from an exit code** (a documented Windows trap).
8. **Do NOT `git commit / add / push`** — *except* TASK 0's authorship history-rewrite, which the
   agent completes end to end (including the `--force-with-lease` push) **only after its verification
   gate passes**. All *other* changes (TASK 1–5) are presented for the human to commit. Data
   (`data/`, `data_Final/`, `delivery/`), `figures/deck/` and `*.pptx/*.pdf` are gitignored and
   regenerable — do not commit them and do not treat their absence as data loss.
9. **Cost awareness (stage the work):** nb12/13 register 7,200 s, **nb14 register 28,800 s (8 h)**,
   nb15–19 `timeout=-1`. A part-way failure leaves a notebook LESS executed than you found it.
   Never launch a full re-execute sweep casually; do the cheap notebooks first and the expensive
   ones deliberately, one at a time.

## KILL LIST — must not appear as a *current* claim anywhere (only inside a struck/superseded block)

`2.37×–3.00×` · `×0.333–×0.421` · α reference `3.9–5.0` · band `2.0–9.9` · hard stop `11.8–14.9` ·
proxy loads `104.8 / 82.8 / 126.1 / 99.7` Mt/yr · `±38 %` Π band · `SE 0.1644 ln` · `σ_r = 0.465`
as a per-station residual sd · `k_min 0.00216 / 0.0209 / 0.0104` /km · `2.12× over 348.4 km` · the
uncited **"mountainous LS 2–10"** band · the uncited **SDR 0.05–0.30** band · **"the model is ~2×
under-erosive"** (direction WITHDRAWN, `docs/37` A1.9 — the residual's direction is UNKNOWN) ·
`min(m, 0.5)` labelled "Buarque eq. 14" · **"82 tests" / "140 tests"** (now 154) · **"Phase C is
blocked on SSC data quality"** (superseded — Phase C is COMPLETE).

---

## TASK 0 — CRITICAL: remove "Claude" as a git contributor (authorship cleanup)

**The owner's GitHub profile lists "Claude" as a contributor** because commits carry
`Co-Authored-By: Claude <noreply@anthropic.com>` trailers (and possibly some commits are authored
by Claude). Remove this so the history attributes the work **solely to the owner**. This is the
**one** git-history operation this session performs, it is **destructive** (rewrites commit SHAs and
needs a force-push), and it must run **before** any reorganization commits so the cleaned history is
the base.

1. **Confirm the owner's git identity first** (name + email to attribute everything to). Default:
   `TWILL <knadelayman3@gmail.com>` — but CONFIRM before rewriting.
2. **Back up:** `git branch backup-before-authorship-rewrite` and record the current HEAD SHA.
   Ensure the working tree is clean (stash if needed).
3. **Scope it:**
   - `git log --format='%H %an <%ae>' | grep -i claude` — commits authored/committed by Claude.
   - `git log -i --grep='Co-Authored-By: Claude' --grep='Generated with Claude' --format='%H %s'`
     — messages carrying a Claude trailer.
4. **Rewrite all history.** Prefer `git filter-repo`; fall back to `git filter-branch`. It must
   (a) strip every `Co-authored-by: Claude…`, `Generated with Claude Code…` and `🤖` line from all
   commit messages, and (b) reset author AND committer of any Claude-authored commit to the owner.
   `filter-branch` fallback (runs on Windows via Git Bash's bundled `sed`):
   ```
   git filter-branch --force --env-filter '
     if [ "$GIT_AUTHOR_EMAIL" = "noreply@anthropic.com" ]; then
       export GIT_AUTHOR_NAME="TWILL"; export GIT_AUTHOR_EMAIL="knadelayman3@gmail.com"; fi
     if [ "$GIT_COMMITTER_EMAIL" = "noreply@anthropic.com" ]; then
       export GIT_COMMITTER_NAME="TWILL"; export GIT_COMMITTER_EMAIL="knadelayman3@gmail.com"; fi' \
     --msg-filter "sed -E '/^Co-authored-by: Claude/Id; /Generated with Claude Code/Id; /🤖/d'" \
     -- --all
   ```
5. **Verify from output** (not exit code): `git log --format='%an <%ae>' | sort -u` shows ONLY the
   owner; `git log -i --grep='Claude'` returns nothing; `git diff backup-before-authorship-rewrite
   --stat` shows **no file changes** (only history/authorship changed, the tree is byte-identical).
6. **Push — the AGENT performs this, but ONLY if step 5's verification fully passed.**
   `git push --force-with-lease origin main`. **Gate:** if `git log --format='%an <%ae>' | sort -u`
   still lists any Claude/Anthropic identity, OR `git diff backup-before-authorship-rewrite --stat`
   shows any file change, **do NOT push — stop and report the failure.** After a clean push, KEEP
   the `backup-before-authorship-rewrite` branch until the owner confirms GitHub no longer lists
   Claude as a contributor (can take minutes to a day to refresh), then it may be deleted. Warn the
   owner that any other existing clones of the repo must be re-cloned, or they will re-introduce the
   old history on the next push.

## TASK 1 — Inventory & triage (decide before deleting)

Catalogue **every** file (scripts/, src/, docs/, notebooks/, figures/, root, and gitignored
data/). For each, assign exactly one disposition, with a one-line reason:

- **KEEP (live)** — part of the current narrative, pipeline, or reproduction chain.
- **ARCHIVE** — historical record with audit value but not part of the live narrative (superseded
  docs, refuted-hypothesis registers, old journals). **Move to `docs/archive/` or `scripts/archive/`
  — do NOT delete.** Add a one-line header to each archived file saying what superseded it.
- **DELETE** — genuine dead weight ONLY: temporary scratch (`_eq/`), `*_backup.*`, `*_ORIG_*`,
  true byte-duplicates, editor cruft, empty stubs, regenerable artifacts checked into the tree by
  mistake. Each deletion needs a one-line justification and a pointer to what regenerates it (if
  anything).

Write the full triage as `docs/agents/journal_reorg-triage.md` (a table: path · disposition ·
reason). **Present it and pause for human review before executing any DELETE.** Known dead-weight
candidates to check: `_eq/`, `data/processed/gauge_minibacia_ORIG_backup.csv`, any `*_backup`,
duplicated scratch under `nbtext/`, the 306 MB `magdalena_share_for_colleague.zip` (gitignored —
keep or move, do not commit). **When unsure, ARCHIVE.**

## TASK 2 — Score every notebook, then correct it

For **each** notebook 01–19, compute a score out of 100 from these weighted factors, and record it
in `docs/agents/journal_reorg-notebooks.md` (one section per notebook: score, per-factor marks,
the specific defects, and the fix applied or owed):

| factor | weight | what "full marks" means |
|---|---:|---|
| **Executes cleanly** | 25 | runs end-to-end with the registered timeout; verified from executed output, not exit code |
| **Generator-sync** (nb10–19) | 20 | the committed `.ipynb` is source-identical to `make_nbNN.py` output; nb01–09 score this as N/A → redistribute to Coherence |
| **Coherence with canon** | 20 | every number agrees with the STATE table; no contradiction with `docs/55–59` |
| **No kill-list / no stale** | 15 | none of the kill-list terms appear as current; "154 tests", not 82/140; "Phase C complete", not blocked |
| **Embargo & convention** | 10 | no gauge-referenced t/km²/yr; every load carries convention + `cp_revision` |
| **Academic clarity** | 10 | a new reader can follow it: purpose stated, inputs/outputs named, narrative not just code |

Then **correct** each notebook to raise its score: edit the **generator** for 10–19 (never the
`.ipynb`), rerun the generator, execute, verify from output, re-confirm source-identical. Build on
the existing diagnosis in the `docs/agents/journal_nbc1-*.md` files — **do not re-audit what they
already measured.** Stage the executions (cheap first; nb14 is 8 h — do it alone, deliberately).
A notebook whose only defect is being *un-regenerated* after ACT 1/2 is **not wrong** — regenerate
it and say so.

## TASK 3 — Coherence sweep across the whole corpus (no mismatch)

- Grep **all** docs and generators for every kill-list term and every stale count; fix each to the
  STATE table (inside a dated superseded note where the house style requires it — see `docs/46`
  §10, `docs/37` A2.7 for the pattern).
- Confirm every doc that states the canonical numbers (r ≈ 0.57, H2E F 0.25931, f_LS 0.25146,
  299.5387/248.7298 Mt/yr, C4.3 railed, C5 18/18, gauge limit 18, ceiling +0.006) agrees. List and
  fix every disagreement in `docs/agents/journal_reorg-coherence.md`.
- Make `docs/00_INDEX.md` an **accurate map of the FINAL state** — its status table must show every
  doc's live/historical/superseded status and successor, and the WHERE-IS-IT table must resolve to
  the real answers (including the C4.3 verdict, the C5 result, the gauge limit, the ceiling bound).

## TASK 4 — The academic roadmap for a new reader (the headline deliverable)

Produce a single, self-contained entry point — extend `docs/00_INDEX.md` and add a top-level
`README.md` — that lets someone with no context reach full understanding:

1. **One-paragraph project statement** — the question (does ENSO change sediment transport?), the
   method (process-based MUSLE on calibrated MGB-SA hydrology), and the two-level result (absolute
   daily prediction is rainfall-limited and non-identifiable; the ENSO *contrast* is reproduced,
   18/18, and is the finding).
2. **A reading order** — the 5–8 documents a newcomer reads, in sequence, with one line each on why.
3. **The narrative arc** — inputs → hydrology (r ≈ 0.57 ceiling) → LS resolution → sediment
   calibration (railed, and why that is a finding) → the ENSO contrast (the success) → the limits.
4. **A glossary** — every technical term (MUSLE, KGE, r, non-identifiable, railing, out-of-sample,
   the ceiling, the contrast, yield embargo) in one plain sentence each.
5. **A reproduction quick-start** — environment, the regeneration chain, how to rebuild the report
   and deck, and the one gate that proves it worked (154 tests; F = 0.25931; erosion 299.5387).
6. **A repository map** — the final folder layout, what lives where, and what is regenerable.

Write it so it reads like the front matter of a thesis, not a changelog.

## TASK 5 — Final structure & verification

- Propose and (after review) apply a clean, documented folder layout: `src/`, `scripts/` (grouped
  by phase: `scripts/c3/`, `scripts/c4/`, `scripts/c5/`, …), `notebooks/`, `docs/` (with
  `docs/archive/`), `figures/`, `data/` (gitignored). Update every path reference you move.
- **Verification (do these and report the outputs, not exit codes):** `python3.10 -m pytest -q`
  → 154; `python3.10 src/report_h2e.py` → F matches 0.25931 to 1e-8; regenerate the report and deck
  from `scripts/` and confirm they build; re-confirm nb10–19 source-identical after any generator
  edit. A verification that only checks an exit code is a FAIL.

## REPORT BACK

1. The triage summary: how many KEEP / ARCHIVE / DELETE, and the DELETE list with justifications.
2. The notebook scoreboard: each notebook's score before and after, and what you fixed.
3. Every coherence mismatch found and fixed (file · line · old → new).
4. The new reader roadmap: where it lives and what it covers.
5. The final folder layout, and every path reference you updated.
6. The verification outputs (pytest count, F value, report/deck rebuilt, notebooks re-synced).
7. Anything you could not settle, named as an open item — never smoothed over.

## CONSTRAINTS RECAP

Stage the work. Don't commit. Don't delete the audit trail (archive instead). Don't hand-edit
generated notebooks. Don't touch frozen artifacts or frozen pre-registrations except via amendment
slots. No t/km²/yr. No uncited bands. Verify from executed output. When unsure, ARCHIVE and ask.
