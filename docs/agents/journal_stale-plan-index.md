# journal — `stale-plan-index` (agent A1), 2026-08-12

**Task.** Repair stale claims in the two documents I own — `docs/30_phase_c_plan.md` and
`docs/00_INDEX.md` — and write the canonical v1/v2/v3 forcing definition into the index.

**Files edited:** `docs/30_phase_c_plan.md`, `docs/00_INDEX.md`, this journal. **Nothing else.**
No notebook, no `src/`, no other doc, no frozen doc, no git command. `docs/33`, `docs/42`,
`docs/45`, `docs/46` were read as evidence and **not** edited.

**Method.** Every correction is **strike-through-and-annotate**, dated 2026-08-12, with a
pointer to the doc that owns the outcome — the pattern `docs/37` A3.3 states explicitly
(*"NOTHING IS DELETED… The record of what was believed survives intact"*). Where the owning
doc could be quoted, it is quoted verbatim rather than paraphrased. **No number was moved by
picking the more convenient of two.**

---

## 1 — The section created in `docs/00_INDEX.md` (TASK B)

> ### Exact title / anchor for cross-referencing
>
> **`docs/00_INDEX.md` → `## Forcing versions — v1 / v2 / v3, stated once`**
>
> - Markdown anchor: **`#forcing-versions--v1--v2--v3-stated-once`**
> - Located **between §4 (WHERE IS IT) and §5 (Live status vs. the record)**.
> - **Deliberately unnumbered.** `docs/51` §7 item 8 cites "`docs/00` §6" and `docs/47` cites
>   "O11 / `docs/00` §6", so numbering this section would have renumbered §5/§6/§7 and broken
>   live citations in other people's frozen documents. The title is therefore the stable handle.
> - The agent adding banners to `notebooks/10` and `notebooks/11` should link to that title.
>   The section already names those two notebooks and states what each of them means by "v2",
>   so the banners can be short.

### Every clause verified before it was written

| clause | verified against | verdict |
|---|---|---|
| v1 = the original gauge forcing, gauge-only | `docs/18` §14.2 (*"the v1 bundle is untouched"*); nb11 cell 21 (*"v2 is written ALONGSIDE v1"*, `[v1 was 2174.3, gauge-only v2 2036.4]`) | **confirmed** |
| v1 areal mean 2,174.3 mm/yr | nb11 cell 21 print; `docs/23` §11.1 (*"The **areal mean is unchanged: 2,174.3 mm/yr either way**"*) | **confirmed**, and the window is the same 2009–2017 as v2's (one print statement) |
| v2 = zero-suppression repair | `docs/16` §4.1 — 70 of 294 stations rain-days-only; repair inserts absent days as 0.0 marked `Inferido_seco`; gauge-mean 2,904 → 2,304 mm/yr | **confirmed** |
| v2 = + deterministic IDW | `docs/23` §11.1 — G3 `lexsort` on (distance, gauge code), byte-identical over 5 shuffles; `docs/18` §14.1 — *"3 gauge-column shuffles, byte-identical field each time — asserted inside the notebook"* | **confirmed** (the deterministic interpolator is what nb11 ran to build v2) |
| v2 is **still gauge-only** | `docs/18` §14.1 (*"gauge-only LOOCV \| daily r median 0.429"*); nb11 cell 21's own label *"gauge-only v2"* | **confirmed** |
| v2 areal mean 2,036.4 (2009–17) / 2,073.1 (2008–18) | `docs/18` §14.1, §14.2 | **confirmed** |
| v2 = the adopted forcing, the one H2E was fitted on | `CLAUDE.md` "Phase status"; `docs/31`:23 (*"H2E = v2 forcing + revised objective + FAO-56 ET"*); `docs/33` §3.3 (*"forcing \| `model_inputs_v2/` (v2)"*); `docs/26` Addendum | **confirmed** |
| v3 = a CHIRPS-merged forcing, **does not exist** | `docs/18` §15.4 (*"A v3 calibration was never launched"*), §15.5 (*"No forcing file was written - v2 stands"*) | **confirmed** |
| a v3 would need a new pre-registration | `docs/30` §1; `docs/33` §1 (*"A pass does not authorise adopting v3"*) and §5.1 | **confirmed** |
| the merge was rejected by its volume gate | `docs/18` §15.1 and §15.5; `docs/33` §1 H-CHIRPS | **confirmed** |
| nb10/nb11 use the older CHIRPS-inclusive sense | read from the `.ipynb` cell sources directly | **confirmed, with a refinement — see below** |

### One clause of my brief I could not write as given, and why

My brief said to write *"The cause of the volume failure is now **UNKNOWN**."*
**I did not write that**, because the owning documents say something more specific and I may
not upgrade or downgrade an owner's confidence to make a sentence cleaner.

`docs/18` §15.5 (the owner) says the *tested* half of the diagnosis is refuted and the
*surviving* half is named:

> "The half of s15.3 that survives is the other half — the days the repair *never inferred*, at
> the 139 stations that still report rain-selectively after it (s9.3). Those cannot be put into
> a pool by any change to `merge_chirps_gauges.py`, because they are not in the record at all."

And one thing about the cause **was** positively measured: the merged field is near-unbiased at
the 287 LOOCV gauges (+2.00 % merged vs +1.73 % gauge-only) and puts its whole surplus in the
ungauged terrain where the blend weight → 1.

So the accurate statement — which is what both `docs/30` and the index now carry — is:
**the diagnosed cause was wrong; the surviving candidate is an untested hypothesis that cannot
be tested inside the merge; no route to a passing volume gate exists inside the merge code.**
That is stronger than "unknown" in one respect and weaker in another, and it is what the owner
says. The practical conclusion my brief wanted is preserved verbatim: **no fix exists, and no
reader may conclude one is waiting.**

### A refinement to my brief's nb10/nb11 claim

The brief said nb10 and nb11 use "v2" in the older CHIRPS-inclusive sense. Measured from the
cell sources, it is sharper than that and the banner agent should know:

- **nb11 uses BOTH senses, in the same notebook.** Prose (cells 0, 13, 22): *"the v1 baseline,
  deliberately gauge-only"*, *"a CHIRPS-merged v2"*, *"**Next:** v2 forcing - quantile-map
  CHIRPS onto these gauges"* — the CHIRPS-inclusive sense. Code (cells 1, 21):
  `VERSION = 'v2'` for the **repaired gauge-only** field, and the print
  `[v1 was 2174.3, gauge-only v2 2036.4]` — the sense that won and that matches
  `model_inputs_v2/`. **The notebook's prose contradicts its own code.**
- **nb10 has no forcing-version usage at all.** Its only "v2" is *"CHIRPS v2.0"* — the satellite
  product's own version number, a **third** unrelated meaning of the token.

---

## 2 — Ledger: every stale claim found

### `docs/30_phase_c_plan.md` (all corrected)

| # | quoted text | file:line (pre-edit) | owns the outcome | what the owner actually says | correction applied |
|---|---|---|---|---|---|
| **D1** | *"the CHIRPS merge … **failed only its volume gate, with the fix identified**. It continues as **bounded background work** (§5)"* | `docs/30`:23–25 | `docs/33` §1 (H-CHIRPS) · `docs/18` §15.5 (the read-out) | `docs/33` §1: *"H-CHIRPS is **REFUTED by its own volume gate** (2,188.5 mm/yr against the required [2,016.0, 2,056.8]). The registered intervention turned out to be a **no-op**: the quantile maps already included the inferred-dry days, so the diagnosed cause in docs/18 §15.3 was wrong."* `docs/18` §15.5: *"no route to a passing volume gate exists inside the merge code."* | **Struck** the "fix identified" clause and the "continues as background work" clause; kept the one true part (non-gating). Added a dated correction blockquote quoting **both** owners verbatim, the bit-identical-re-run evidence (max \|diff\| 0.000e+00), the 25.9 % fit-input measurement, what the diagnosis actually is now, and the fact that **v3 does not exist** |
| **D2** | *"**CHIRPS refit** (≤ 2 sessions): … If both pass → v3 forcing + ONE new pre-registered calibration cell. If not, the negative result closes the question."* | `docs/30`:126–128 (§5 item 1) | `docs/18` §15.5 · `docs/33` §1 | Gate table: LOOCV **0.447 PASSES**; volume **2,188.5 mm/yr, +7.47 %, FAILS**; decision **DO NOT ADOPT**. The intervention *"was already the code's behaviour"* | **Struck** the whole item and back-annotated: **DONE and NEGATIVE, CLOSED — not pending work.** Added the gate table, the no-op finding, the item's own closing clause invoked (*"the negative result closes the question"*), the explicit statement that **no v3 and no new cell were produced**, and the note that the residual open question is the *unknown/untested upstream cause*, not the refit |
| **D3** | *"There is no further calibration question whose answer would change Phase C's inputs."* | `docs/30`:21–22 | `docs/33` §7.1, §8 | H-PEAK **REFUTED** (`R_AMS` 0.820, `R_Q1` 0.847); `H2E-S` refit **failed 2 of 3** conditions; *"No further refit."* | **Struck.** Annotated: there *was* a further question, it *was* asked, and it *would* have changed Phase C's inputs had it succeeded (`docs/33` §5.1 budgets that cost). The conclusion survives on a measurement this bullet did not have |
| **D4** | *"Any future forcing change (CHIRPS v3) re-opens it only through a new pre-registration."* | `docs/30`:28–29 | `docs/33` §5.1 | *"Amended to: the hydrology is frozen except through a pre-registered re-opening, of which **this document is the first**."* | **Not struck** (the sentence is still true; it is *narrower* than the rule now is). Added the amendment blockquote quoting `docs/33` §5.1 verbatim, **plus** the second Phase-B close (`docs/33` §8: *"on a **measured conflict**"*) |
| **D5** | Runoff-driver asset row: *"calibrated H2E hydrology, recession-correct (ratio 1.08–1.11), mass-conservative"* | `docs/30`:51 (§2 table) | `docs/33` §7–§8 · `docs/36` | `R_AMS` 0.820, `R_Q1` 0.847 ⇒ H-PEAK refuted; El Niño 0.686; *"C3/C4 must treat simulated sediment as a lower bound"*; `docs/36`: 81.8 % event-identity deficit | Row flagged; correction blockquote added under the table with the numbers and the `docs/36` §7.1 rule that "43 % missed" may never be quoted without the 81.8 %. **`R_POT` quoted at its owner's 0.567 with the 0.5747-in-artifact disagreement named, not silently resolved** |
| **D6** | *"`calibration_safe` has **no SSC-quality gate**; … LS2D factor not yet computed; MUSLE needs a peak-flow proxy from a daily model."* | `docs/30`:55–57 | `docs/32` · `docs/37`/`docs/46`/`docs/51` · `docs/35` | C1 built the gate (79/79 classified); LS2D built at 90 m and its *level* then contested (`f_LS` 2.3151×–3.9768×, UNVALIDATED); `q_peak` proxy registered in `docs/35` | **Three of four struck** and back-annotated with what happened. **Areas left standing** — still open, still the reason for the yield embargo |
| **D7** | *"land anywhere in that band and the transposition claim holds"* | `docs/30`:214–215 (§3 C4) | `docs/45` §3.2/§6 · `docs/42` §3 · `docs/47` | `docs/45`: ADOPT needs **all eight** conditions and is *"**NOT** a validated α, C, LS, P, FG, K-unit or volume convention"*; `docs/42` §3: seven scalars, one product Π, condition number `inf`, *"never 'validated'"*; `docs/47`: **`C4.3-BLOCKED-UNTIL-LS-LANDS`** | **Struck.** The band itself is **kept** (`docs/45` re-registers it verbatim) — only the "and therefore the claim holds" inference is struck. Added the block verdict and its four upholders |
| **D8** | §4 done-criterion: *"sediment KGE within Fagundes' −0.26…0.44 band"* | `docs/30`:119 (§4 table) | same as D7 | same | Flagged in-row as **necessary but not sufficient**, pointing at D7's correction |
| **D9** | §3's stage list read as a status board (C0…C5 with no outcome pointers) | `docs/30`:61+ | `progress_map.html` (RULE 0) + each stage's own doc | — | Added a status **pointer** (not a status restatement): each stage → its owning doc, C2b named as a stage that did not exist when the list was written, C3 **OPEN**, C4.3 **BLOCKED** |

### `docs/00_INDEX.md` (all corrected)

| # | quoted text | file:line (pre-edit) | owns the outcome | what the owner actually says | correction applied |
|---|---|---|---|---|---|
| **I1** | *"**May C4 start…?** \| **Yes** — but only held to `docs/42` G1–G9"* | `docs/00`:155 | `docs/47` | **`C4.3-BLOCKED-UNTIL-LS-LANDS`. C4.3 may not start.** In-box `F_report` **−0.305 … −0.350**, below the bar's −0.26; `FAIL — RAILED / HARD STOP` **and** `FAIL — NUMERIC` | **Struck the "Yes."** Replaced with the block verdict, its arithmetic reason, the four documents that uphold it (`docs/46` §6.4, `docs/51` §4, `docs/53`, `docs/37` **A3.4**), and `docs/47` §6.3's bounded LS-invariant exception. The `docs/42` constraint set is explicitly kept — *it was never the part that was wrong* |
| **I2** | *"a fit that silently omits channel deposition lands α at **6.83–8.73**"* | `docs/00`:155 | `docs/47` §2.5 C1 | 6.83–8.73 is `11.8 × {144,184} / 248.730` — computed at the **prior** `C`, on a superseded base. At the adopted `C` the band is **5.67–7.25** | **Struck and replaced**, with the reason and the note that the *trap itself survives unqualified either way* |
| **I3** | *"The C4 tributary set is **13 stations**."* | `docs/00`:150 | `docs/45` §3.4, §3.6 | Three different sets: **CAL 8** is the fit set (5 of the 13 have no paired SSC + observed-Q day in CAL); **EVAL 5** scored never fitted; **all 18** for every structure guard | **Struck.** All three sets spelled out. **The all-18 clause is stated explicitly so the correction cannot be over-applied** — CAL 8 supersedes 13 *for fitting only* |
| **I4** | r-ceiling row ended at the first CHIRPS rejection | `docs/00`:148 | `docs/18` §15.5 · `docs/33` §1 | second rejection; repair was a no-op; diagnosed cause wrong | Appended the second read-out, *"There is no known fix and no v3 forcing"*, a link to the new forcing-versions section, and the corrected pointer (`docs/33` §1's *"see §7"* mis-fires) |
| **I5** | *"Why did Phase B close?"* — one close only | `docs/00`:147 | `docs/33` §8 | *"Phase B closes for the second time… on a **measured conflict**"* | Second close added with its numbers |
| **I6** | C3 row stopped at Amendment A1 | `docs/00`:153 | `docs/37` A1.9, A2, A3 | A1.9 (clause 4″ NOT ESTABLISHED), A2 (level reclassified, C3 still OPEN), A3 (2026-08-12 C3.1 enactment: ADOPT-SOURCE; *no engine default moves, C4.3 stays BLOCKED*); A3.3.1 supersedes the LS bracket | Three amendments added; the superseded LS bracket (×0.333 / ×0.421 / 2.37×–3.00×) shown struck against its replacement |
| **I7** | Pre-registration row listed 29/32/33/34/35/42 only | `docs/00`:156 | `docs/45`, `docs/46` | both are frozen registrations; `docs/46` is **FROZEN (READ OUT)** — four of five hypotheses already measured at freeze | Both added; `docs/46`'s read-out status stated as its own §1.2 requires, so it cannot be cited as prospective |
| **I8** | §3 doc table **stopped at 42**; 38 and 39 listed as `RESERVED` | `docs/00`:116–120 | the documents themselves | 38 and 39 are written; 43, 45–53 exist; 44 was never assigned | Table rebuilt: 38/39 changed from RESERVED to LIVE with real subjects; **43, 44 (never assigned), 45, 46, 47, 48, 49, 50, 51, 52, 53 added**; heading changed from "docs 30–37+" to "docs 30–53"; the numbering-discipline note's *"C4's and C5's write-ups take 37+"* struck for *"the next free number is 54"* |
| **I9** | §1 paragraph: C3 *"being closed"*, C4/C5 *"remain"* | `docs/00`:28 | `docs/37`, `docs/47` | C3 is **OPEN**; C4.3 is **BLOCKED** | Struck and corrected |
| **I10** | §7 defect list stopped at 6 | `docs/00`:262+ | — | — | Five defects added (7–11), each naming the owner it is owed to |

### Values on the known-superseded watch list — checked, and mostly absent

`×0.333` · `×0.421` · `2.37×–3.00×` · `±38 %` · `0.1644 ln` · `σ_r = 0.465` · `CAL 13`:
**grepped both owned files. None of the first six appeared as a live claim anywhere in
`docs/30` or `docs/00_INDEX.md`** — so there was nothing to over-correct. `CAL 13` appeared
once, as I3, and was corrected **with the all-18 clause preserved**. The superseded LS bracket
now appears only inside I6, shown struck against its replacement, which is the safe form.

---

## 3 — Found and deliberately NOT changed

| finding | why not changed |
|---|---|
| **`docs/31`:28 header table — *"CHIRPS merge \| … rejected; fix identified"*** and **`docs/31` B1**, which reads as ≤2-session pending work | **`docs/31` is not mine.** Recorded as index defect 8. Worth noting in its favour: B1's own body was the *most* careful text in the corpus on this — it warned in advance that the `Inferido_seco` change alone *"would leave the volume gate failing"*, which is precisely what was then measured |
| **`docs/PROGRESS.md`:162 *"fix identified"*, :93 *"refit re-spec'd … ≤2 sessions then stop"*; `docs/29`:206 *"remains the only identified path to moving r"*** | Not mine. Recorded as index defect 8. `docs/PROGRESS.md` is already flagged SUPERSEDED by the index |
| **`docs/33` §1's read-out pointer *"see §7"* points at the H-PEAK section** | `docs/33` is **FROZEN** and is not mine. Changing it would need its own §-slot amendment by its owner. Recorded as index defect 7, and the corrected pointer (`docs/18` §15.5) is carried in both files I do own |
| **CLAUDE.md "Phase status": *"Stage C0 is complete; C1 … is next"*** | Not mine, and it is the file most likely to be inside a concurrent agent's blast radius. Recorded as index defect 9 |
| **`docs/47`/`49`/`50`/`51`/`52` all cite `docs/46_ls_preregistration_DRAFT.md`, a filename that no longer exists** | Five documents, none mine, several frozen. Stale by filename only — the section numbers still resolve. Recorded as index defect 10 |
| **`R_POT` 0.567 (docs) vs 0.5747 (`peakgap/summary.json`)** | **Deliberately not resolved.** `docs/36` §7.3 raised it and index defect 2 requires *"a dated amendment note, not a silent edit"*. I quoted the owning doc's 0.567 and named the disagreement in the same sentence, both places I touched it |
| **`docs/00_INDEX.md` §6's "not yet promoted" table** (LS2D, C/P factors, the sediment engine, the first run, the area-unit fix — all *"expected in 37"*) | These have almost certainly landed in `docs/37` by now, but confirming each promotion means auditing `docs/37`'s 2,250+ lines finding by finding, which is a different task from a staleness sweep and risks asserting a promotion that did not happen. **Left as-is and flagged here** as the single largest remaining staleness in the index |
| **`docs/30` §3's stage bodies (C0/C1/C2/C3/C5 prose)** | They describe *intent*, which is what a plan document is for, and they are not false. I added a status **pointer** rather than rewriting them into a status board — `progress_map.html` owns status (RULE 0) |
| **`docs/30` §5 items 2 (k_int_frac), 3 (areas), 4 (B5 coordinate fetch)** | Checked against `progress_map.html` and `docs/31`: B2 is still `todo`, B3 still open (it is why the yield embargo stands), B5's C1.0 decision still holds. **Genuinely still pending — correctly stated** |

---

## 4 — Disclosure

- **No number in either file was recomputed by me.** Every quantity is either quoted from the
  document that owns it (with the quote marked) or was read directly from a notebook's cell
  source (nb10/nb11, stated as such).
- **No frozen document was edited.** `docs/33`, `docs/42`, `docs/45`, `docs/46` read-only.
- **No file outside my three was written.** No `git add`, `commit`, `push`, or any other git
  command was run.
- Markdown integrity of both edited files verified programmatically: balanced backticks,
  balanced `~~` strike markers, and consistent column counts across every table block.
