# journal_tracker.md — progress_map.html sync for the C3 closure run

SLUG: tracker
GOAL: update `progress_map.html` to reflect the C3 closure run honestly. Accuracy over
optimism: if C3 is OPEN, the tracker says OPEN, and C4 stays blocked.

Scope of files I may touch: `progress_map.html` + this journal. Nothing else.
No git. No calibration. Frozen `sim_calibrated_v2/` H2E artifacts are read-only (I do not
read or write them at all).

## Checklist

- [ ] 0. Journal created (this file).
- [ ] 1. Read the source of truth: docs/37_c3_closure.md, docs/35 §9.x, the resolved-decision
      journals, and the critic's findings. Do not invent numbers.
- [ ] 2. Read progress_map.html: locate C3, C3.6, C4, the discoveries array, the palette and
      the code style.
- [ ] 3. Task 1 — C3.6 + C3 parent set to the closure verdict; C4 blocked with the reason as
      its note if C3 is OPEN.
- [ ] 4. Task 2 — 'why?' explanation panel for the factor chain: running total after each
      correction + implied SDR, inline SVG waterfall if it genuinely helps.
- [ ] 5. Task 3 — discoveries entries: one per resolved decision + one for the closure verdict.
- [ ] 6. Task 4 — VERIFY LAST: extract the <script>, `node --check`, and confirm the counts
      render headless. Report both.

## Ground rules I am holding myself to

- Numbers go in only if I can point to the file they came from. No re-derivation, no
  rounding drift; where the run's own documents disagree, I say so on the page rather than
  silently picking one.
- I am the reporting layer, not a decision layer. I do not resolve any open scientific
  question here; I transcribe verdicts that other agents derived and that docs/37 records.
- The critic flagged a REPORTING failure (a wrong-way finding present in no document) and a
  surviving false claim. As the tracker I must make sure the page does not repeat either.

---

## Log

### Step 0 — journal opened

Environment confirmed: repo `C:\dev\magdalena-mgb-sed`, branch main, HEAD `a4746a8`
("ops: commit-agent journal — post-push verification"). `progress_map.html` exists at repo
root, 112,237 bytes, mtime Aug 11 06:17 — i.e. written by the previous tracker pass at
commit `2296988` ("tracker: sync progress_map with the C3 build, the OOM gap and the ranked
options"), BEFORE the closure run. So the page currently still describes the
order-of-magnitude gap as unexplained. That is the gap I am closing.

Working tree already carries `docs/37_c3_closure.md` (untracked) — that is the closure
document I must read as source of truth.

### Step 1 — sources read (no numbers invented; every figure below has a file behind it)

Read in full: `docs/37_c3_closure.md`; `docs/35_qpeak_preregistration.md` §9.2 and §9.3;
`docs/agents/journal_critic.md` run-2 findings (lines ~262–360); the tail of
`docs/agents/journal_fixer.md`; `docs/39_contradiction_audit.md`:192.

The verdict I must transcribe, verbatim from `docs/37` line 1 and its closure table:

- **C3 is OPEN.** Four closure conditions: 2 MET (chain fully explained by evidence; the
  independent audit agreed), **2 NOT MET** — (i) a fifth question, the **LS formulation
  level**, is explicitly UNRESOLVED, and (ii) the **implied SDR is 0.579 – 0.740** against a
  plausibility band of 0.05 – 0.30.
- ⇒ under the standing rule, **C4 stays blocked** and the reason goes in its note.

The factor chain, with running totals (`docs/35` §9.2 table + `docs/37` §1–2):

| step | factor | running basin total | implied SDR vs 144 / 184 |
|---|---|---|---|
| first run, `pixel_km2` + `si_stored` | — | 0.6844 Mt/yr | 210× / 269× short — impossible |
| (`swat_mm_ha`, ×10^0.56 short of m³) | ×13.1826 | 9.0222 Mt/yr | 15.96× / 20.39× short — impossible |
| **1. volume in m³** `williams_m3` | **×47.8630** = 1000^0.56 | 32.7577 Mt/yr | 4.40× / 5.62× short — impossible |
| **2. K in US-customary numerics** | **×7.593014** = 1/0.1317 | **248.730 Mt/yr** | **0.579 / 0.740** — possible, but above 0.05–0.30 |
| **3. LS aggregation** area-wtd mean | ×1.000 | 248.730 | unchanged |
| **4. LS resolution** native 90 m | ×1.000 | 248.730 | unchanged |
| *(NOT adopted — measured, UNRESOLVED)* LS **formulation** | ×0.421 … ×0.333 | ≈104.8 … 82.8 Mt/yr *(proxy)* | **1.37 … 2.22 — impossible again** |

Combined adopted factor ×363.4245196. I re-derived every one of these with `python3.10`
rather than copying: `1000**0.56 = 47.86300923226385`, `1/0.1317 = 7.59301442672741`,
product `363.42451960716664`; `0.6844056401724942 × that = 248.72979099612405` (matches
`docs/37` §2's 248.730 and the critic's independent re-run 248.729790996124);
`144/248.72979 = 0.578941`, `184/248.72979 = 0.739759`; proxy `×0.421 = 104.715`,
`×0.333 = 82.827`, SDR `1.3752 … 2.2215`. Also `100**0.56 = 13.182567`,
`10**0.56 = 3.630781`.

Williams' derivation, re-computed: `(1233.4818375 × 0.028316846592) = 34.92831596650577`,
`^0.56 = 7.3144130627006`, `95 × 0.90718474 / that = 11.782565403570468`. **NOTE the
critic's Finding C:** `docs/35` §9.2 and `docs/37` §1 both print this as
`86.1826 / 7.31494 = 11.7818`; the correct intermediates are 7.3144131 and 11.782565. The
page will print the **correct** digits and say plainly that two committed documents carry the
last-digit slip. I am not silently harmonising anything.

`python3.10 -m pytest tests/ -q` → **96 passed in 7.52s** (executed just now; the page's
current "82/82" is the pre-amendment count).

### Step 2 — DECISIONS FOR THIS EDIT, written BEFORE I touch the file

I am a reporting layer: I resolve no scientific question. My decisions are editorial, and I
state them here in advance so they cannot be reverse-engineered from the result.

1. **C3 parent → `blocked`.** The page's own legend reads red as "blocked / **open**", so
   `blocked` is the honest status for a stage whose verdict is OPEN. Note leads with
   "CLOSURE VERDICT: OPEN".
2. **C3.6 → `blocked`, not `done`.** `docs/37` names itself "Stage C3.6", so C3.6's
   deliverable *is* the closure verdict, and that verdict is OPEN. Downgrading a leaf from
   done→blocked lowers the completion percentage; that is the correct direction and I accept
   it. (Counted-leaf effect: done −1, blocked +1.)
3. **C4 → `blocked`** with the closure reason as its note, per the task and the standing rule.
   Its children stay `todo` (they are un-started, not blocked individually).
4. **The factor chain gets BOTH** a rewritten C3.6 panel *and* its own new `decision`-status
   node under C3 carrying the waterfall figure — a `decision` node is excluded from the leaf
   counts, so adding it cannot inflate the percentage.
5. **New inline SVG `factorchain`** (waterfall, log-x, running totals + implied SDR band).
   It earns its place: the chain is multiplicative over 3 orders of magnitude, which a table
   shows badly and a log waterfall shows immediately. Existing dark palette only.
6. **Superseded claims are marked, not deleted.** The old "third area convention (hectares) —
   the form α = 11.8 is normally quoted with" discovery is the claim the critic's Finding B
   calls false; I mark that entry ⛔ SUPERSEDED in place and say what replaced it.
7. **Known-unfixed reporting defects get their own open-register row** rather than being
   quietly omitted: the surviving "normally quoted with" claim in `src/mgb_sediment.py`
   (Finding B), the reversed `1.35× / 1.73×` line 170, the 7.31494/11.7818 slips (Finding C),
   and the fixer's disclosed gap that the engine still exposes **no `ls2d_formulation`
   option**.
8. **I will not put any t/km²/yr number on the page** except where already labelled
   MODEL-INTERNAL, and I add none.

NOTHING on this page moves any number toward the 144–184 Mt/yr anchor; the largest single
item I am adding (candidate 0) moves the model *away* from it and tightens the α guard.


### Steps 3–5 — edits applied (progress_map.html only)

Task 1 (statuses):
- `C3 — MUSLE hillslope erosion` → **blocked**, note leads "CLOSURE VERDICT: 🔴 OPEN (docs/37)"
  with the 2-of-4 conditions and the ×363.4245 chain; doc tag now `docs/37 + docs/35 §9.2–9.3`.
- `C3.6` retitled "closure verdict — 🔴 OPEN: the chain is explained, the LEVEL is not yet
  defensible", **done → blocked**; its panel replaced (closure table, the SDR/α table, both
  pattern gates unchanged, the five residual candidates).
- `C4` → **blocked**, note gives the two reasons (SDR 0.579–0.740; LS level unresolved and
  linear in α) and states the old 13×/48× blocker is retired. New child **C4.0** carries the
  entry condition + the new α-guard trap panel; C4.1–C4.3 unchanged and still `todo`.
- New `C3.1-LS` leaf (**todo**) = the resolver, with the frozen decision rule and the
  registered expected consequence (104.8/82.8 Mt/yr, SDR 1.37–2.22).

Task 2 (the 'why?' factor-chain panel):
- New `decision` node "📌 Decision: the four conventions — the factor chain 0.6844 → 248.730
  Mt/yr (×363.4245)" under C3, with why / fig / math / gate / risk. The math block carries the
  running total AND the implied SDR after every step, plus Williams' derivation and the
  K-transform quotation.
- New inline SVG `factorchain`: log-x waterfall (equal length = equal factor), the 144–184
  anchor band, the two ×1.000 steps drawn as zero length, and the candidate-0 term as a red
  dashed arrow pointing back DOWN.
- Rewrote it once after a measurement: the caption lines overflowed the 560-unit viewBox, so
  they were split to ≤ ~100 chars at font-size 10. Measured overflow now 0 texts.
- `oomgate` relabelled as the FIRST run's record; its "registered NOWHERE" hectare label and
  its "α needed 2,480 ⇒ a unit question" caption corrected to the resolved position.

Task 3 (discoveries): 6 new entries prepended — closure verdict OPEN; decision 1 (m³);
decision 2 (K US-customary); decisions 3+4 (both ×1.000); candidate 0 (LS formulation, wrong
way); the new α-guard trap. Two existing entries marked in place: the "third area convention"
entry as ⛔ SUPERSEDED **with the false half named**, and the first-run entry as 📜 superseded
on level / intact on pattern. Nothing deleted.

Also corrected for accuracy, all inside the named file: open register (convention row → ✅
RESOLVED; three new rows: LS formulation, uncited SDR band, reporting defects); commit-status
row (C3 build committed a4746a8, closure run not); "no runnable artifact" row (still true, now
with the independent re-run and the pinned unit-day); doc numbering row (37/38/39 taken ⇒ C5.4
takes 40+); C3.4 82 → 96 tests + the missing `ls2d_formulation` option; C3.1 risk now points at
candidate 0 and records that the 2–10 band was retired; banner, `updated`, Phase C note and the
completion sentence.

Two rendering bugs found and handled: `<b>` inside an SVG `<text>` is an HTML-parser breakout
element that truncates the figure — I avoided it in the new SVG and removed the one existing
instance (`attempts`). Pre-existing, NOT fixed and disclosed instead: 12 caption lines across
other figures are longer than the viewBox and are clipped in a browser (e.g. `oomgate` 170
chars, `attempts` 140). Out of scope for this task; worth a pass later.

### Step 6 — VERIFICATION (executed output only)

1. `python3.10 extract.py map.js` → file 140,891 chars; **`<script`: 1, `</script>`: 1**;
   external-looking `src`/`href` attributes: **[]** (only `docs/…` relative links) ⇒ still
   SELF-CONTAINED; SVG `<text>` lines containing `<b>`: **0**.
2. `node --check map.js` (node v24.14.1) → **passes**, prints nothing, echo confirms
   `NODE_CHECK_RESULT: syntax OK`. It failed once first — my banner contained unescaped `"`
   around ‘third area convention’ (`SyntaxError: Unexpected identifier 'third'`, map.js:323);
   replaced with typographic quotes and re-checked.
3. Headless render (`harness.js`, Node `vm` + a stub DOM; the real code builds the real tree):
   - cards: **41 done · 4 in progress · 18 todo · 9 blocked · 72 tracked leaves**
   - `by()` agrees: {done 41, wip 4, todo 18, blocked 9}, tot 72 ⇒ **57 %**
   - overall bar: 4 spans, widths 56.94 / 5.56 / 25 / 12.5 % (sum 100)
   - tree: **91 rows**, **44 xboxes**, 13 kid wrappers, 393 div + 91 span + 91 i created;
     44 explanation ids assigned; 78 leaves visited
   - side panel: **16 figures** (factorchain present, 4,150 chars), **31 discoveries**,
     disclist 19,617 chars and contains `363.4245196`
   - key nodes: C3 **blocked** (8 kids) · C3.6 **blocked** + panel · C3.1-LS **todo** + panel ·
     the decision node **decision** + panel · C4 **blocked** (4 kids) · C4.0 **blocked** + panel
4. All 16 inline SVGs parse as well-formed XML (`xml.etree`), and the new figure has **0**
   texts overflowing the viewBox.
5. Delta against `git show HEAD:progress_map.html` run through the same harness:
   old **41/3/17/6, tot 67 (61 %)** → new **41/4/18/9, tot 72 (57 %)**. done is unchanged
   because C3.6 left `done` (−1) while the resolved-convention register row entered it (+1).
   The page states this drop and its cause rather than hiding it.

Frozen artifacts: never opened. No git. No calibration. Files touched: `progress_map.html`
and this journal, nothing else. Scratchpad scripts (extract.py, harness.js, dumpfig.js) live
outside the repository.

CHECKLIST: [x]0 [x]1 [x]2 [x]3 [x]4 [x]5 [x]6.
