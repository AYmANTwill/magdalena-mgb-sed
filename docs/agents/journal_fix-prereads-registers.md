# journal — `fix-prereads-registers` (agent A10): the two mandatory pre-reads and the three open registers

**Run 2026-08-12.** Files edited, and the only files edited:

| file | role | why it mattered |
|---|---|---|
| `docs/16_forcing_pipeline_audit.md` | **mandatory pre-read** (CLAUDE.md: *"Do not touch precipitation or ERA5 code before reading §6"*) | carried **no banner**, marked LIVE, and its §1 said Phase B *"has not started"* |
| `docs/18_hydrology_journal.md` | **mandatory pre-read** (the Phase B record) | its §8 register contradicted its own §15 |
| `docs/PROGRESS.md` | open register | checklist + two copied registers |
| `docs/progress_journal.md` | open register (chronology) | banner range only — **historical entries not touched** |
| `docs/open_questions.md` | open register | three "pending advisor action" status lines |

No `git add` / `commit` / `push` was run. No other file was edited; `git diff --stat` confirms the
five above plus this journal. `docs/33`, `docs/42`, `docs/45`, `docs/46` are FROZEN and I own no
amendment slot in any of them — none was touched.

**Method.** Every correction was checked against the numbered doc that *owns* the outcome (RULE 0),
and that doc is quoted verbatim in the ledger below. Nothing was reconciled by preferring the more
convenient number. Original text is **preserved** — `~~struck~~ → **new**`, dated, with the
owning-doc pointer, in the house style `docs/18` §8 already used for its closed items. Where a
claim could be settled only by measurement, it was measured (see ledger row 14).

**Correction received mid-run, and applied.** My brief said the CHIRPS volume-gate cause "is now
UNKNOWN". I grepped `docs/33`, `docs/18` §15.5 and `docs/agents/journal_chirps-refit.md` and the
word does not appear in any of them. **The word "UNKNOWN" is written nowhere in this pass.** What
the owning docs say — and what I wrote instead — is: the intervention was a **no-op**, the
**diagnosed cause was wrong**, *"no route to a passing volume gate exists inside the merge code"*,
and one **untested** upstream hypothesis survives (the 139 residual rain-selective stations) which
cannot be tested inside the merge. The practical conclusion is stated plainly everywhere it
appears: **no fix is available and none is pending.**

---

## 1 — Ledger

`file:line` is the **pre-edit** state (from `git show HEAD:`), so the rows are locatable against
the commit this pass started from.

### The two confirmed high-severity findings

| # | `file:line` | stale claim (quoted) | owning doc | what the owning doc actually says (quoted) | correction written |
|---|---|---|---|---|---|
| 1 | `docs/16:25-26` | *"**Phase A (model inputs) is complete.** Phase B (water balance + discharge calibration) **has not started**. Phase C (sediment) **remains blocked on mainstem SSC data**."* | CLAUDE.md "Phase status" · `docs/30` §1 + header · `docs/32` §R6 | CLAUDE.md: *"**Phase B (water balance + discharge calibration): CLOSED on H2E**"*; *"**Phase C (sediment): ACTIVE**"*. `docs/30` §1: *"**Phase B closes on the input-ceiling result, with H2E as the adopted configuration.**"* `docs/30` header: *"It supersedes the 'Phase C blocked' line in older docs."* `docs/32` §R6: *"**79/79 classified, each with a deciding measurement**"*; *"`21237020` ARRANCAPLUMAS (Magdalena — **the only Magdalena-trunk SSC station in the entire network**) … This is the quantitative form of 'Phase C is blocked on mainstem SSC'."* | **A dated STATUS banner at the top of `docs/16`** (full text in §2 below) **plus** an in-place back-annotation at §1: the two clauses struck, both replaced with the quoted owning-doc statements, the *measured* form of "blocked on mainstem SSC" given (79/79 classified · 28 mapped · 18 usable), and a forward pointer that **C4.3 is BLOCKED** (`docs/47`). Phase-A clause left standing — it is still true. |
| 2 | `docs/18:306` (§8 item 20) | *"**CHIRPS merge not attempted** — and after doc 26 it is the **only remaining lever on the dry phase** (§14). Quantile-map CHIRPS *to* the gauge distribution so volume stays gauge-controlled; gate on LOOCV beating 0.429."* | `docs/18` §15 / §15.5 — **the same document** · `docs/33` §1 | §15 title: *"The CHIRPS-gauge merge: **built, validated, and NOT adopted**"*; §15.1: LOOCV *"**0.447** (> 0.429) - **PASSES**"*, VOLUME *"**2,188.5 mm/yr** … **FAILS (+7.5 %)**"*. §15.5: *"`merge_loocv_report_v2.csv` is **bit-identical** … (max \|diff\| 0.000e+00)"*; *"**240,115 of 926,268 paired station-days, 25.9 %**"*; *"**no route to a passing volume gate exists inside the merge code**"*; *"The only remaining route is upstream: repair the 139 residual rain-selective stations"*. `docs/33` §1: *"The registered intervention turned out to be a **no-op**: the quantile maps already included the inferred-dry days, so **the diagnosed cause in docs/18 §15.3 was wrong**."* | Item 20 **struck in the sibling style** (11/13/16/18) and closed as **DONE, and NEGATIVE — CLOSED-NEGATIVE (§15) / CLOSED (§15.5)**, carrying both gate results, the no-op, the wrong diagnosis, the bit-identical re-run, the 25.9 % figure, and the **untested** 139-station hypothesis. Explicitly: *"No fix is available and none is pending; no v3 forcing exists."* A **register note** was added under the table recording that §8 and §15 of one document disagreed, and that item 18's closing phrase *"item 20 is now the only lever"* is superseded. |

### Same claim classes, found by sweeping all five files

| # | `file:line` | stale claim (quoted) | owning doc | what the owning doc actually says (quoted) | correction written |
|---|---|---|---|---|---|
| 3 | `docs/18:35` (§1 table) | *"Phase C (sediment) \| Still blocked — on mainstem SSC data and on the doc 19 `calibration_safe` gate"* | `docs/30` header · `docs/32` §R6 (both grounds) | `docs/30`: *"It supersedes the 'Phase C blocked' line in older docs."* `docs/32` is itself the explicit SSC-quality gate `docs/19` §3.7 demanded — pre-registered §0–§6, read out R1–R7. | Row struck; both grounds discharged in a note under the table, with the §R6 measurement quoted and the `docs/47` C4.3 block named. |
| 4 | `docs/18:23-34` (§1 "Current state") | attempt-1 numbers presented as current: *"Validation skill \| median KGE **+0.450**"*, *"El Niño 2015–16 \| KGE **+0.193**"*, *"`kc_mult` railed at its 2.00 ceiling"*, *"`k_int` (117.4 d) **slower than** `k_bas` (68.6 d)"* | `docs/26` Addendum A.2 / A.3 / A.4 / A.5 | A.4 (attempt 4, H2E): VAL KGE **0.356**, r 0.591, α 0.905, β 1.035, PBIAS **+3.51**. A.5: La Niña **0.344** / El Niño **0.200**, and *"**The dry phase in the adopted configuration is at climatology, not above it: −0.0005.**"* A.2: *"`kc_mult` **1.6625** … **confirmed off the rail** that held H1 at 98.8 % and H2 at 93.3 %"*; railed *"**2 of 10 global** … **3 of 18 dimensions**"*; *"**a constrained ordering relocates compensation, it does not remove it**"*. | Table left intact (it is what was true when §4–§6's diagnosis ran) and a **dated crosswalk table** added under it mapping each stale row to its H2E successor with the owning A-section. The −0.0005 caveat is carried, flagged as the thing every Phase C El Niño claim inherits. |
| 5 | `docs/18:287` (§8 item 2) | *"CHIRPS–gauge merged rainfall (nb11 → 12 → 13 → 14) \| **r, and therefore the dry phase**"* | `docs/18` §15/§15.5 | as row 2 | Struck; **DONE, and NEGATIVE — CLOSED**, with both gate numbers and *"No forcing file was written; nb13/nb14 were never re-run on a merged field."* |
| 6 | `docs/18:290` (§8 item 5) | *"PET review against the 49 mm/yr basin ET deficit"* — presented as fully open | `docs/29` rule (b) · `docs/31` register #2 · `docs/18` §14.2 | `docs/29`: *"### Rule (b) — H2E (FAO-56 threshold ET): **SUCCESS, all three conditions** … the linear stress ET = kc·PET·(W/Wm) was why kc railed; the FAO-56 threshold form releases it at no cost."* `docs/31` register #2: *"kc_mult 1.662/1.836 is off its rail but **still above the FAO-56 plausibility bar of ≤1.2** — the ET form was a real cause, not the whole story."* `docs/18` §14.2: basin PET *"**1,251.6 mm/yr** — the figure §3's energy floor has used since it was written"*. | Marked **PARTLY DONE**, deliberately *not* closed: the ET-function half succeeded and was adopted; the residue is named as `docs/31` register #2; and the **49 mm/yr deficit itself is explicitly not retired**, because §14.2 re-measures the same PET the floor uses. |
| 7 | `docs/18:164-166` (§5 item 4) | *"**Fix the rainfall field.** This is the only lever measured to be capable of moving r … The CHIRPS–gauge merge … then re-run notebook 11 → 12 → 13 → 14."* | `docs/18` §14, §15.5 | §15.5: *"no route to a passing volume gate exists inside the merge code."* | Original preserved; a dated read-out appended — the rebuild ran (§14), the merge was rejected twice, **no nb13→nb14 run on a merged field was ever launched and no v3 forcing exists**, and the surviving upstream route is **untested**. |
| 8 | `docs/18:878-882` (§15.4) | *"not until its volume can be held - **either by conditioning the quantile maps on inferred-complete records only**, or by repairing the remaining rain-selective stations first"* | `docs/18` §15.5 (the next subsection) · `docs/33` §1 | §15.5: the refit found the inferred-dry days were *"already the code's behaviour"* — **25.9 %** of the fit input. | A three-line pointer: of the two routes named, the **first was measured and is a no-op**; the second is **untested**. Read §15.5 before quoting §15.4. |
| 9 | `docs/16:23` (§1 table) | *"**Model period** \| **2009-01-01 → 2017-12-31 (3287 days)** — bounded by ERA5, not rainfall"* | `docs/18` §14.1–§14.2 · CLAUDE.md | §14.2: *"period assertion \| `DATES.equals(want)` → **True**, 4,018 days"*. §14.1: *"**Open item 3 is closed.** PET now spans the full rainfall record."* CLAUDE.md: *"2008 warms up, 2009-2018 is scored."* | A note under the table: v2 spans **2008-01-01 → 2018-12-31, 4,018 days**; PET is no longer the binding constraint; *"Anyone sizing an array or a window off this table gets the **v1** shape."* |
| 10 | `docs/16:296-310` (§7) | *"### Blocking Phase B — … 2. **Discharge dataset QC.** Never audited."* and, under **"Forcing improvements (v2)"**, item 3's *"**Expected:** wet-day error 18.1 → ~3 pts"* | `docs/17` (the audit) · `docs/18` §15/§15.5 · `docs/33` §1 · `docs/00_INDEX.md` § *"Forcing versions — v1 / v2 / v3, stated once"* | `docs/17` §3.1 is the discharge audit and found *"the gauge→minibacia mapping was broken for half the network"*. For the merge, as row 2. INDEX: *"**v2** = the **zero-suppression repair** … **+ deterministic IDW** … **Still GAUGE-ONLY** … **This is the ADOPTED forcing**"*; v3 *"**IT DOES NOT EXIST.**"* | Register head marked *"no longer a to-do list"*; item 2 struck **DONE → `docs/17`**; item 1 (day convention) marked **STILL OPEN with its owner reassigned to `docs/17`** and its §4 quote carried; the **"(v2)" heading flagged as the old CHIRPS-inclusive sense** with the canonical section cited by its exact title; item 3 given the full **rejected-twice** read-out ending *"This section's 'Expected' numbers were never achieved, and no reader may conclude a fix is waiting."* |
| 11 | `docs/16:327-337` (§8) | *"## 8 — Proposed next steps, in order … 3. **CHIRPS merge (v2)** — only if step 2 shows rainfall-driven error. 4. **Phase C sediment** — still blocked on mainstem SSC data."* | `docs/26` · `docs/18` §15.5 · `docs/30` header | as rows 1, 2 | Per-item read-out appended (1 DONE → `docs/17`; 2 DONE → `docs/26`, and its rationale vindicated by the `docs/22` §4.7 ceiling; 3 **DONE and NEGATIVE**; 4 premise superseded), and item 4's *"still blocked"* struck inline → **ACTIVE**. |
| 12 | `docs/16:344-375` (§9 "Key numbers") | *"Final values, after the 70-station repair"* — incl. *"Basin-mean rainfall \| **2,206 mm/yr**"*, *"PET \| **3.40 mm/day ≈ 1,255 mm/yr**"*, *"LOOCV daily *r* \| 0.467 / 0.398 / **0.313**"* | `docs/18` §10, §14.1, §14.2, §15.2 · `docs/00_INDEX.md` § *"Forcing versions…"* | §10: the selectivity repair covered **153** stations, 240,158 inferred-dry days. §14.2: 2008–2018 areal mean **2,073.1 mm/yr**; basin PET **1,251.6**. §14.1: 2009–2017 **2,036.4**; gauge-only LOOCV **r 0.429** over 287 gauges; PET **3.41 mm/day**. §15.2 bands: 0.481 / 0.426 / 0.343. | Header note: *"These are the v1 numbers … 'Final' meant final **for the 70-station repair**"*, plus a three-row crosswalk to the v2 successors with owners, plus `docs/18` §7 trap 9 quoted (*"No basin-mean rainfall figure means anything without its window attached"*). Table itself untouched. |
| 13 | `docs/16:471-476` (§11) | *"Two things genuinely help: (a) the CHIRPS merge (v2) is *independent of whether an IDEAM observer showed up*, so it does not share the MNAR mechanism — **an argument for the merge beyond anything previously measured**"* | `docs/18` §15.5 | *"the merged field is very nearly unbiased against the gauges themselves: median per-gauge bias **+2.00 %** merged vs **+1.73 %** gauge-only … A field that is unbiased where it can be tested and +7.5 % over the basin **puts its whole surplus in the terrain with no gauge to test it**."* | Honest read-out: the MNAR **argument was never refuted** — the merge was. It does not fix MNAR; it relocates the surplus into ungauged terrain. *"Do not read (a) as a pending improvement."* Recommendation **(b)** is separately confirmed as the one that *was* adopted, with §15.5's measurement (**105.6 mm/yr, 41.0 % of the surplus**, leaving **+152.1 mm/yr**). |
| 14 | `docs/PROGRESS.md:106` (docs/21 register item 9) | *"9. ✅ `PET_READY` file-count gate"* — marked **closed** | `docs/18` §14.3 + §8 item 17, **and a direct measurement** | `docs/18` §14.3: *"**`PET_READY = len(ext) >= 132` in nb11 still has this hole** — it counts names."* **Measured on disk 2026-08-12:** `src/nbgen/make_nb11.py:461` and `notebooks/11_rainfall_pet_forcing.ipynb:819` both still read `PET_READY = len(ext) >= 132`. | ~~✅~~ → **🔴 NOT FIXED**, with the grep evidence and file:line recorded in the register itself. **This is the ledger's one reverse defect: the tracker said closed, the doc said open, and the code says the doc was right.** Notebook and `src/` are outside my file scope, so only the register entry was corrected. |
| 15 | `docs/PROGRESS.md:93` (background track B1) | *"🟡 **B1 CHIRPS refit** — merge attempted & **rejected** … refit **re-spec'd** to fit maps on **selectivity-passing stations** (F3), ≤2 sessions then stop"* | `docs/33` §1 · `docs/18` §15.5 · `docs/30` §5 item 1 | as row 2; `docs/30` §5 item 1: *"→ **DONE, and NEGATIVE. This item is CLOSED — it is not pending work.**"* | Struck and closed **CLOSED-NEGATIVE**, carrying the no-op, the wrong diagnosis, the bit-identical re-run, +7.47 %, *"no route to a passing volume gate exists inside the merge code"*, and the **untested** 139-station hypothesis. Noted that `progress_map.html` already had it right, so this was tracker-copy drift, not project ambiguity. |
| 16 | `docs/PROGRESS.md:162` (decisions & discoveries log) | *"**2026-08 (docs/18 §15)** — CHIRPS merge **rejected** (volume gate +7.5%); **fix identified**."* | `docs/33` §1 · `docs/18` §15.5 | as row 2 | *"fix identified"* struck: **"no fix was identified"**, with both quotes. The file's SUPERSEDED banner governs only *numbering*, so a fact claim in a discoveries log was not covered by it. |
| 17 | `docs/PROGRESS.md:104` (docs/21 register item 1) | *"1. 🟡 CHIRPS–gauge merge (→ B1)"* | `docs/18` §15.5 | *"This closes the CHIRPS question as it currently stands."* | ~~🟡~~ → **✅ CLOSED-NEGATIVE**, cross-referenced to the B1 entry. |
| 18 | `docs/PROGRESS.md:111` (docs/31 register item 5) | *"5. 🔴 Restrepo anchor unverified (→ C2.4)"* | `docs/34` §C2.4 | *"**Restrepo, J.D. & Kjerfve, B. (2000)** … **144 Mt/yr**"*; *"**Restrepo, J.D. & Escobar, H.A. (2018)** … **184 Mt/yr**, an upward revision covering 1980–2010."* | ~~🔴~~ → **✅ RESOLVED**, both figures with citations. Noted that `docs/31`'s own copy still reads unresolved and belongs to that document's owner. |
| 19 | `docs/PROGRESS.md:3` (banner) | banner warns only about the **document index numbering** | `progress_map.html` (RULE 0) · `docs/26` Addendum, `docs/32`, `docs/34`, `docs/33`, `docs/37`, `docs/47` | `docs/47`: *"`C4.3-BLOCKED-UNTIL-LS-LANDS`. **C4.3 may not start.**"* | Banner widened: the whole C0–C5 checklist has drifted (C0/C1/C2 complete, C2b ran, C3 OPEN, **C4.3 BLOCKED**), the doc index stops at 35 while the docs run to **53**, and — per RULE 0 — the checklist is **not** restated item-by-item because the tracker owns status. Fact claims and registers corrected instead. |
| 20 | `docs/progress_journal.md:3` (banner) | *"Everything after that date (Phase B's closure, and Phase C stages C0–**C3**) is recorded in docs/30–**docs/36**"* | the file listing (`ls docs/*.md`) · `docs/47` | numbered docs run to **53** (44 never assigned); `docs/47` decides the current stage gate. | Range widened to **docs/30–53**, `docs/47`'s verdict quoted, and an explicit statement that **the dated entries below are correct as history and are not edited**. |
| 21 | `docs/open_questions.md:29`, `:40`, `:53` | *"**Status:** ESCALATED TO ADVISOR — memo drafted … Decision (Path A vs B) depends on his answer."* · *"**Status:** RECOMMENDATION READY — … to approve with the advisor."* · *"**Status:** DECISION PROPOSED — … still to confirm."* | Q1 → `docs/12`, `docs/32` §R6 · Q2 → `docs/07`, `docs/30` §1 · Q3 → `docs/15`, CLAUDE.md | `docs/12`: *"we now have observed daily sediment concentration in **both study years**"*. `docs/32` §R6 as row 1. `docs/30` §1: *"**Decision: keep 2011 (La Niña) vs 2015–16 (El Niño).**"* and *"The advisor was asked … and **declined to answer** — told the team to decide."* `docs/07`: *"**2017 is NOT an El Niño year**."* | Three per-question dated stamps, each struck-and-replaced: **RESOLVED / DECIDED / DECIDED AND BUILT — no advisor action is pending.** The doc-level banner already resolved the *facts*; what survived was three lines that read as **pending advisor actions**, which is precisely the failure mode that started this run (a team member preparing an advisor briefing). |

---

## 2 — The `docs/16` status banner, exact text as written

```markdown
> **STATUS — 2026-08-12. LIVE as a knowledge base; its *status framing* is not.**
> **What this document is for:** the rainfall + PET pipeline record. §4 (defects found in the
> data), §5 (errors made in development) and **§6 (traps)** are still true, nothing in them is
> retracted, and they are why CLAUDE.md says *"Do not touch precipitation or ERA5 code before
> reading §6."* Read it for those.
> **What has changed since it was written:** it predates Phase B entirely. Phase B has since run
> and **CLOSED on the adopted configuration H2E**, and Phase C (sediment) is **ACTIVE** — so every
> *status*, *next-step* and *still-blocked* statement below is stale and is back-annotated in
> place at **§1, §7, §8, §9 and §11**. Its forcing numbers are the **v1** field; the adopted
> forcing is **v2** (see [docs/00_INDEX.md](00_INDEX.md) § *"Forcing versions — v1 / v2 / v3,
> stated once"* — v1 and v2 are **both gauge-only**, and there is no v3).
> **Where current status lives:** `progress_map.html` (RULE 0: for status, the tracker wins), then
> [docs/00_INDEX.md](00_INDEX.md) and CLAUDE.md "Phase status".
```

`docs/18` received a parallel banner in the same shape (purpose · what changed · where status
lives), naming its §1 table as attempt-1 vintage and pointing at `docs/26` Addendum A.2/A.4/A.5.

**§6 of `docs/16` was not touched, and neither were §4 or §5.** The traps reference, the
zero-suppression finding, the `ssrd` accumulation trap and the ten development errors are still
true; only the *status* framing around them was stale. The banner says so explicitly so that a
reader who arrives via CLAUDE.md's *"read §6"* instruction is not made to doubt it.

---

## 3 — Checked and deliberately NOT changed

| checked | verdict / reason |
|---|---|
| `docs/16:432` — *"flagged stations now sit at **0.465** against healthy…"* | **Cleared, as briefed.** It is a post-repair **dry-day fraction**, not `σ_r`. Different quantity; `docs/48` owns `σ_r = 0.465 ln` and it does not appear in any file I own. Re-verified in context. |
| `×0.333` · `×0.421` / `0.421475` · `2.37×–3.00×` · `±38 %` · `0.1644 ln` · `σ_r` · `CAL 13` · `248.730` · `299.539` · `f_LS` · "Buarque" | **Absent from all five files.** Grep over the whole scope returns zero hits (the only near-miss is the row above). Nothing to correct, and nothing was imported — a doc that does not own a number should not start carrying it. |
| Any claim that **C4.3 may start** | **Absent.** `docs/PROGRESS.md:83` *describes* C4.3 as a subtask but asserts no permission. The gap was the reverse one — **nothing in these five files recorded that C4.3 is BLOCKED** — so `docs/47`'s verdict was added as a pointer in `docs/16` §1, `docs/18` §1, the `PROGRESS.md` banner and register, and the `progress_journal.md` banner. It is quoted, never paraphrased, and always attributed to `docs/47`. |
| Any claim that **`docs/46` is a DRAFT** | **Absent.** `docs/46` is not referenced anywhere in these five files. The stale `_DRAFT` filename survives in other docs (`docs/00_INDEX.md` §7 defect 10) — not my scope. |
| `docs/progress_journal.md` — every dated entry | **Not edited, by rule.** A chronology is correct as history. The 2026-07-27 entry's *"To confirm with advisor"* and the 2026-07-28 Path A/B/C entry are accurate records of what was believed then. Only the **banner** (which speaks in the present tense about where current material lives) was corrected. |
| `docs/open_questions.md` body text (Q1's DHIME findings, Q2's ONI table, Q3's cell-limit arithmetic) | **Not edited.** All of it is correct as the record of a dated investigation, and the doc-level banner already routes readers to the successors. Only the three **`Status:`** lines were stamped, because those alone read as live instructions. |
| `docs/16` §7 item 1 — the day-convention offset | **Confirmed STILL OPEN, not closed.** `docs/17` §4: *"the averaging window **cannot be proven from the export**"*; carried as `docs/17` §5.2 item 4. I annotated it to reassign its **owner** to `docs/17` and recorded that it was *absorbed* (±1 day slack), not resolved. **Not marked done** — it is not. |
| `docs/16` §7 items 4, 5, 6 (orographic correction · 7 residual stations · 5–20 % dry-fraction band) and §7 items 7–9 (housekeeping) | **Left as open.** I could find no owning doc that closes any of them. Asserting closure without a measurement is the failure mode this run exists to fix. |
| `docs/PROGRESS.md` C0–C5 checklist boxes | **Not restated item by item.** RULE 0 gives *status* to `progress_map.html`, and rewriting a superseded tracker into a second source of truth is exactly what its own header forbids (*"never let it drift into a second source of truth"*). The banner now states the scale of the drift and names the owning doc for each stage instead. |
| `docs/PROGRESS.md` docs/21 register items 2–8, 10–12; docs/31 register items 1, 2, 3, 6, 7 | **Re-checked against their owners and unchanged.** Item 5 of the docs/21 list (the collaborator drops sparse gauges where we repair them) is genuinely still open: the advisor declined the *Phase B scope* question, which is a **different** question — recorded in the register so the next reader does not conflate them. |
| `docs/33` §1's *"see §7"* read-out pointer | **Not fixed — `docs/33` is FROZEN and I own no amendment slot.** Recorded in place in `docs/16` §7 and `docs/18` §8 item 20 that the pointer mis-fires (§7 of `docs/33` is H-PEAK) and that the CHIRPS read-out is `docs/18` §15.5. |

---

## 4 — What this pass could not resolve

1. **`PET_READY` is still a filename count** (ledger row 14). I corrected the *register*, and the
   measurement is recorded there with `file:line`. **The code is unfixed**, in
   `src/nbgen/make_nb11.py:461` and `notebooks/11_rainfall_pet_forcing.ipynb:819`, both outside
   this pass's file scope. `docs/18` §8 item 17 already carries it as an open item and is correct
   as written. Whoever owns `src/nbgen/` should replace it with an open-and-read-a-timestep check.
2. **`docs/31`'s own copy of the known-open register still lists the Restrepo anchor as
   unresolved** (ledger row 18). `docs/34` resolved it. `docs/31` belongs to another owner; only
   the `PROGRESS.md` copy was corrected, and the divergence is named there.
3. **The 139 residual rain-selective stations.** Every doc I touched now says this hypothesis is
   **untested** and lies upstream of the merge. No doc owns it as a work item — it is not on
   `docs/31`'s background track (B1 is closed) and it is not in the `docs/21` register. It is a
   real, named, unowned lever on the r-ceiling. Flagged, not assigned.
4. **`docs/16` §7's remaining forcing improvements (items 4–6)** have no owning doc and no closing
   measurement. They may be live, may be abandoned; the record does not say, so neither does my
   annotation.

---

## 5 — The pattern, restated from the evidence

Of the 21 ledger rows, **13 are one structural defect**: a decision was recorded where it was
taken, and the document that *asked* the question was never told. The sharpest instance is
internal — `docs/18` §8 item 20 said the CHIRPS merge was *"not attempted"* while §15 of **the
same file** recorded that it was built, measured and rejected twice. Citation travelled forward
(§15 cites §8's gate), the outcome never travelled back.

The second pattern is **selective back-annotation**, and it produced the reverse defect too:
`docs/PROGRESS.md` marked `PET_READY` ✅ while `docs/18` §14.3 said the hole was still open — and
the code agreed with the doc. **A register that is partly updated is read as fully updated**,
in both directions. That is why every correction in this pass is dated and carries its owning-doc
quote: so the next reader can tell what was checked from what was inherited.
