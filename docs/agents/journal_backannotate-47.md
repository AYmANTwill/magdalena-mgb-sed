# journal — `backannotate-47` (agent A7)

**Run 2026-08-12.** This agent wrote **exactly two files**: `docs/47_c4_entry_verdict.md` (dated
in-place annotations + a new §9) and **this journal**. Nothing else was edited. No `git add` /
`commit` / `push`. No engine default moved. No frozen artifact under `sim_calibrated_v2/` opened.
No calibration, no simulation, no `KGE_ln` evaluation, no α̂ quoted.

**Working-tree state was read, not `HEAD`.** The uncommitted edits to `docs/35`, `37`, `42`, `43`,
`45`, `46`, `51`, `src/mgb_sediment.py` and both nbgen generators were treated as current — which
turned out to matter decisively for finding **4** below.

**Method.** RULE 0 applied throughout: for a FACT the numbered doc that owns the topic wins.
`docs/agents/journal_sweep-phasec.md` was read in full and its findings were treated as **leads**,
not facts; every one was re-checked against the owning document, and **one of the five reported
findings did not survive the re-check** (§B). Two quantities were recomputed from disk rather than
adjudicated by preference (§D).

---

## A — THE LEDGER

`docs/47:line` refers to the **pre-edit** file (the state the sweep and the task brief describe).

| # | item | `docs/47:line` (pre-edit) | what it claimed | owning doc + quoted current truth | verdict | annotation written |
|---|---|---|---|---|---|---|
| 1 | **`_DRAFT` filename**, verdict box | `:35` | *"the pre-registration drafted as `docs/46_ls_preregistration_DRAFT.md`"* | `docs/46_ls_preregistration.md`:1 — *"# 46 — Resolving the LS **level**: pre-registration — **FROZEN (READ OUT)**"*; `:3` — *"⚠ FROZEN 2026-08-11. §1–§8 ARE IN FORCE. §10 IS THE AMENDMENT SLOT."* **`ls -la docs/` confirms no `_DRAFT` file exists.** | **VERIFIED — corrected** | `~~…_DRAFT.md~~ → **docs/46_ls_preregistration.md, FROZEN (READ OUT) 2026-08-11; §10 is its amendment slot**`, both quotes carried |
| 2 | **`_DRAFT` filename**, cross-ref table | `:675` | table row *"`docs/46_ls_preregistration_DRAFT.md` \| the LS pre-registration … Its `Δ_shape` pre-test is open item O6"* | as above, plus `docs/53` for O6 | **VERIFIED — corrected** | filename struck + replaced; the O6 clause struck and replaced with the measured value and Branch B |
| 3 | **O6 — `Δ_shape` "has not been run"** | `:604-606` (§6.3 bullet), `:629` (O7 table row **O6**) | *"It is the registered Branch A/B discriminator, it has **not been run** (O6)"* | `docs/53_delta_shape_pretest.md`:19 — **`Δ_shape` = 0.1299456916752905**; `:24` — *"**VERDICT — `Δ_shape` > 0 ⇒ BRANCH B IS MANDATORY**"*; `:397` — *"`docs/47` **O6** … **CLOSED.** Value 0.1299456916752905; Branch B."* Registered in `docs/46` §10 amd 1; bar fixed blind beforehand by `docs/52` | **VERIFIED-CLOSED** | §6.3 bullet struck with the full read-out (argmax `24037390` CAPITANEJO; smallest CAL station `26127010` at 0.0179854753; **no CAL station invariant**) + the consequence: Branch A is closed, so no legal PROVISIONAL C4.3 exists. O6 row struck in §7. |
| 4 | **D3 / B3 — NaN-blind mass audit, BLOCKING** | `:187-217`, `:571` | *"the per-node mass audit is blind to NaN … **BLOCKING**"*; *"`tests/test_transport.py:583` currently passes on an all-NaN run"* | **Read on disk by me, not taken on trust.** `src/mgb_transport.py`:**908** = `if not (m <= max_resid):`, with the IEEE-754 rationale at :902–907. `tests/test_transport.py`:**245–277** = `test_the_partition_claim_does_not_survive_an_overflowing_run`, input all-finite by assertion, `assert math.isnan(res.ledger["max_node_residual_t"])` at :**274** and `assert not res.ledger["node_partition_exact"]` at :271; door screen at :**232**. Corroborated `docs/37` A3.4 item 1 + commit `a0d8afb` | **VERIFIED-DISCHARGED** | §2.3 heading gets `✅ RESOLVED 2026-08-12`; a dated block quotes the new code line, the comment, both test line numbers and the corroborating owners; **the finding's body preserved verbatim as the provenance**, with its pre-fix line refs flagged as pre-fix. B3 row marked `✅ DISCHARGED`. |
| 5 | **D4 / B4 — `docs/42` §9 transcription, BLOCKING** | `:219-237`, `:572`, `:672` | *"the `docs/42` §9 transcription is unperformed and C4 has already started"* | `docs/42`:**648** — *"⚠ **THREE, all dated 2026-08-11 — A-P1, A-P2, A-P3, plus A-P1.1 … Plus A-P4, dated 2026-08-12 (§9.7)**"*; `:660` — *"§9.1 — Amendment log: opened 2026-08-11, and it is late"*; `:644` — the station cell now carries *"SUPERSEDED by amendment A-P1 (§9.2): it is the CAL 8"* with the all-18 clause **unchanged**; `:901` **F5** — *"**`docs/47` §2.4 D4** … **is discharged** by §9.1–§9.5. **D4 may be CLOSED.**"* | **VERIFIED-DISCHARGED** | §2.4 heading gets `✅ CLOSED 2026-08-11/12`; block quotes A-P1…A-P4, F5 and F4 (which also closes O7); **records the residue F1 — §4.2's body still prints `0.0104` — as `docs/42`'s owner's, not mine.** B4 row + the `docs/42` cross-ref row annotated. |
| 6 | **B1 / the verdict's framing** | `:33-36`, `:569` | *"The condition for unblocking is a single named event: **C3.1 lands**"* | `docs/37`:**1342** — *"**AMENDMENT A3 (2026-08-12) — THE C3.1 ENACTMENT.** … **ADOPT-SOURCE**, `ls_formulation = buarque_2015_dg`. **No engine default moves here. C3 stays OPEN. C4.3 stays BLOCKED.**"*; A3.4 heading — *"Is C4.3 thereby UNBLOCKED? **NO** — and this amendment is the act that makes the block *dischargeable*, not the act that discharges it"*; `docs/46` §9's card pins A3 as the B1 event | **VERIFIED-LANDED (reduced form); BLOCK NOT LIFTED** | A dated sub-block inside the verdict box: *"THIS SENTENCE IS NOW WRONG IN ONE DIRECTION ONLY, AND IT IS NOT THE PERMISSIVE ONE."* **Title left unchanged.** Corrected blocking condition written out in full at **§9.2** (four conditions, each with its owner and how I verified it). |
| 7 | **`f_area` 0.42135** | `:391` | §4.3 table, area-weighted × = **0.42135** | `docs/46` §10 **Amendment 2 (v) item 1** — which names this exact cell: *"That is **not** a rounding of the corrected value … It reconstructs as the **`urh_ls2d_variants.csv` `area_km2` weighting**, 0.4213519856784954 … The same table's DG cell prints **0.24466** where the registered value is 0.2446790094097074 … **So `docs/47` §4.3's area column is a third support**, owed to `docs/47`'s owner, and it changes no `docs/47` verdict"* | **VERIFIED — annotated, deliberately NOT replaced** | Footnote ᴬ on both area cells quoting the owning amendment verbatim, printing my own independent recomputation (§D), and stating the **registered** bracket `[0.2446790094097074, 0.42136300143291305]` with `docs/46` §3.3 ground **G-ii** (`f_ero` decides). Explicit "do NOT fix §4.1's ×0.4214" note. |

### The rest of `docs/47`, swept by me (task item 6)

| # | item | `docs/47:line` | owning doc + truth | verdict | annotation |
|---|---|---|---|---|---|
| 8 | **B2** | `:570` | `docs/45` **§8 Amendment 4** (`:1215`) — *"**Discharges `docs/47` §6.1 repair B2**"*; its own verdict *"the re-expression does NOT fix `docs/47`'s `FAIL — RAILED` / `FAIL — NUMERIC` pre-computability problem. It RELABELS it — and in the Π coordinate the problem is measurably WORSE, not better … `C4.3-BLOCKED-UNTIL-LS-LANDS` is unchanged"* | **VERIFIED-DISCHARGED** *(contradicts the brief — see §B)* | B2 row marked `✅ DISCHARGED`, with the route-(A) choice and the note that the `docs/35` §6.1 half is **PROPOSED, not enacted** |
| 9 | **B5** | `:576` | `docs/45` §8 **Amendment 1** — band replaced by the station bootstrap (pre-fit ×0.29–×3.73, registered as a **procedure not a constant**); `docs/42` §9.7 A-P4; `docs/43` §7 amd 1 + 4 | **VERIFIED-DISCHARGED** | row marked `✅`, with the note that `docs/42` §9.6 F5's *"B5 … remains open"* was written 2026-08-11 and is superseded by A-P4 the next day |
| 10 | **§5.5 disclosure** | `:578` | `docs/45` §8 **Amendment 2** — *"(discharges `docs/47` §5.5; `docs/47` **O9** carried, not decided)"*; `docs/45` §7.2 now carries an inline `[WARN]`: *"STILL TRUE OF THIS PASS, NO LONGER TRUE OF THE PROJECT"* | **VERIFIED-DISCHARGED**; **O9 STILL-OPEN** | `✅ DISCHARGED` under the B5 table, with O9 explicitly carried as undecided |
| 11 | **O7** | `:630` | `docs/42` §9.5 (A-P1.1) — *"the **0.0096-vs-0.0104 discrepancy resolved**"*; `:803` CAL 13 = **0.009640**, *"§4.2 prints 0.0104 — does not reproduce"*; §9.6 **F4** — *"O7 may be **CLOSED**"*; `docs/43` §7 amd 6 | **VERIFIED-CLOSED** | O7 row struck; records F3 (the `journal_adj-c4-feasibility` "method rounding" explanation **WITHDRAWN**) and F1 (§4.2 body residue) |
| 12 | **O1** | `:624` | `docs/51` §1 — *"**The PDF is obtainable, it was obtained, and it is on disk**"* (sha256 `3047624f…c0037`, 182 pp., handle `10183/129875`); (R6) resolved, `Sf` is slope **PERCENT**; `docs/46`:119 — *"Every lever is **CITED**"*. **But `docs/37` A3.7 still lists O1 as open** — D&G (1996) and Fagundes (2026) unobtained | **NARROWED, STILL-OPEN** | row headed `NARROWED 2026-08-12, still open`; both halves stated; **not closed**, because the owning doc says it is open |
| 13 | **§4.3's p. 94 caveat** | `:406-412` | `docs/51` — *"**And the interval is not an uncertainty over readings of the source**: with Buarque eq. 13 now read verbatim (§1), the source formulation read whole is a **POINT at ×0.25146** … The span between them is the `L`-form lever, not a reading ambiguity"* | **VERIFIED — WITHDRAWN** | *"A different reading of p. 94 moves both rows"* struck; adds the **POINT-branch consequence for §6.2 item 2** (`f_LS` = 0.25146, `1/f_LS` = 3.976775630318937, per `docs/37` A3.4) |
| 14 | **§5.2 P2 / "one corner clears"** | `:486-489`, `:491-493` | `docs/45` §8.5.12 item 3 — **owed to this document by name**: *"do not survive the fix B2 asks for … **`docs/47`'s VERDICT is strengthened, not weakened** … **P1 is discharged by this amendment; P3 and Branch B / `Δ_shape` now carry the block**"* | **VERIFIED — WITHDRAWN as stated; verdict strengthened** | dated block quoting the owed correction verbatim, the convention-(i)/(ii) mechanism, `docs/45` §8.5.8's three-of-three rail and §8.5.9's `exp(±Δ_shape)` bound, and the re-ordering of §5's propositions |
| 15 | **§6.2 item 4 + §2.6 item 2 — the `k` bound** | `:589-590`, `:262` | `docs/42` §9.7 A-P4:1005–1009 — *"`k_min` is a **detection floor** … the true comparative is **weaker** … A-P4 registers the `weaker` / `detectable` pairing"*. `docs/45` §8.1 row 5 labels ≈ 10× the **all-18** figure; row 4 gives the **CAL-8 fit set** at `k_min` **0.0838 /km ⇒ ≈ 173× over 61.5 km** | **VERIFIED — corrected (comparative + set)** | both sites struck and restated; **explicitly does not claim `docs/45`'s own registered sentence is wrong** — that wording is `docs/45`'s to own |
| 16 | **§2.1's ×2.37–3.00** | `:116` | This document's own §4.3 supersedes it; `docs/51` — *"This **supersedes ×0.333 – ×0.421 and '2.37× – 3.00×'**"*; enacted `docs/37` A3.3.1, `docs/43` §7 amd 3, `docs/45` §8 amd 3 | **VERIFIED — annotated** | dated note; re-derives at the corrected bracket (2.804 – 4.816), showing the finding **strengthens**; the passage preserved as the record of how the defence was mounted |
| 17 | **C1's propagation list** | `:246` | Read this pass: `docs/42`:299 is a C-class erosion-share row, `:472` is G3.3's opening — **neither carries the band**; `docs/45`:404 is in §3.5's ONI clause. The correction is **enacted** in `docs/43` §7 amd 5 (gap **0.6715** in α, bands **DISJOINT**) | **PARTLY ENACTED; line refs stale** | disposition cell struck and rewritten with (a) the enactment, (b) the drifted refs flagged *"quote the sentence, not the line"*, (c) `docs/42` §9.7 F7's **named refusal** recorded as correct process, (d) **O12 still open** |

**Also annotated:** the `docs/37`, `docs/42` and `docs/45` cross-reference rows in §8.1, and a new
row for the `docs/46` §10 / `docs/51` / `docs/52` / `docs/53` LS track that ran after this document.

---

## B — WHERE I DISAGREE WITH THE BRIEF (and with the sweep), on evidence

**The task brief states: *"the block rests on B2 alone."* That is no longer true, and I did not
adopt it.** `docs/45` §8 **Amendment 4** (`docs/45:1213-1215`, `gate-reexpression` agent, process
record `docs/agents/journal_gate-reexpression.md`, untracked in the working tree) reads:
*"**Discharges `docs/47` §6.1 repair B2**"*, and `docs/45` §8.5.10 item 8 states *"**B2 is
discharged; B1 is not**, Branch B is mandatory, and the pre-computed FAIL stands."*

**How the error arose, so it is not repeated.** Both the brief and `journal_sweep-phasec.md`
finding 33 rest on `docs/45`'s **§2.1 inline note** (`docs/45:109-110`): *"**The α box [2.0, 30.0]
is NOT amended here** — re-expressing the gate is `docs/47` B2 and belongs to its owner."* That
note is **correct and still live** — §2.1 genuinely was not amended, because Amendment 4 changes
the *coordinate* and not the *admissible set*, and §8.5.10 item 9 says so explicitly (*"§2.1's box
still reads [2.0, 30.0] because [2.0, 30.0] is still correct"*). The repair lives in **§8.5**, 1,100
lines below. `docs/37` A3.4 (2) likewise reports *"`docs/45` §8 at :610–612 still reads 'Empty at
registration'"* — true **when A3 was written**, and A3 itself flags it: *"Their landing is stated
here as a CONDITION and is NOT claimed as a fact. A later reader must check `docs/45` §8 … "*
I checked. §8 now carries **four** amendments. *(`docs/45` §7.1's own card cell still says "THREE";
`docs/45` §8.5.12 item 4 records that under-count as owed to §7's owner. Not mine.)*

**So the corrected blocking condition — written into `docs/47` §9.2 — rests on four legs, none of
which is a §6.1 repair:** Branch B's mandatory first-run-on-the-adopted-field; the **absent
committed `V4_dg` column**; **ACT 2** (the default switch) not done and not yet draftable; and the
outstanding deliverables (`docs/46` §3.3's stratified report, §2.3's H-S (R7)/(R8) items 2–3, the
`docs/35` §9 amendment A3.1.3 records as owed).

**One genuine owner-vs-owner disagreement is recorded, not resolved** (`docs/47` §9.4): `docs/37`
A3.4 says *"B1 lands here, in the reduced form A3.1.6 permits"*; `docs/45` §8.5.10 item 8 says
*"B1 is not"* discharged. Both are 2026-08-12, and `docs/45` §8.5.2 (ii) cites `docs/37` A3 while
disagreeing with its label — so this is a naming disagreement over one shared fact (**DECIDED and
RECORDED, NOT EXERCISABLE**), not a factual conflict. Under RULE 0 `docs/37` owns C3.1 and
`docs/46` §9's card pins the B1 event to A3, so the *event* occurred; I printed **both** wordings
verbatim and added: *"A reader must not resolve this by picking the more permissive label."*
**Either way, C4.3 does not start** — no reading of B1 touches any of §9.2's four legs.

---

## C — FOUND STALE AND DELIBERATELY **NOT** CHANGED

1. **`docs/47:338` — *"joint 16.7754 / ×0.4214"*.** **Not stale.** Recomputed: `16.7754 / 39.8123`
   = 0.42136224232209646 → **0.4214** at 4 d.p., which is the **corrected** value; the superseded
   0.4214751420286394 rounds to 0.4215. **Correct as printed** — and I added a note saying so, so
   a later pass does not "fix" it into being wrong.
2. **`docs/47:391`'s 0.42135 was NOT overwritten with 0.42136.** The owning amendment
   (`docs/46` §10 amd 2 (v) item 1) had already adjudicated this exact cell and ruled it a
   *legitimately computed number on a third area support*, not an arithmetic error. Replacing it
   would destroy the evidence of which support the table was built on. I annotated instead, exactly
   as the owning amendment directs. Same treatment for the DG cell's 0.24466.
3. **The document title and the `C4.3-BLOCKED-UNTIL-LS-LANDS` verdict string.** Left untouched.
   The block is real, is re-affirmed by six downstream owners, and I was correcting *why*, not
   *whether*. The title's now-imprecise *"UNTIL LS LANDS"* is annotated, not rewritten.
4. **"CAL 13" at `docs/47:429-431`.** `docs/42` §9's supersession of CAL 13 is **for FITTING ONLY**
   (`docs/42:644`: *"The all-18 clause and the never-fit rule are **unchanged**"*), and
   `docs/53:368` already flags that "CAL 13" also names the C1-usable tributary set — a different
   object. §4.4's `sd(ln)` and minimum-detectable-slope figures are a **detectability** computation
   over a station set, not a fitting-set claim. **Deliberately not corrected**; over-correcting it
   would import a supersession that does not apply.
5. **`docs/45`'s registered `k`-bound sentence** (*"…detectable on this fit set"*, `docs/45:838`,
   `docs/42:987`). I corrected **this document's** comparative and its conflation of the two sets,
   and said in the annotation that `docs/45`'s own wording is `docs/45`'s to own and is not
   contradicted here. Not my file.
6. **`docs/42` §4.2's body still printing `0.0104`** (its own §9.6 **F1**), and **§4.2's power
   table**. Recorded in my annotation as a residue belonging to `docs/42`'s owner. Not mine.
7. **`docs/47:246`'s remaining live 6.83–8.73 copies in `docs/35`, `docs/37` §A2, `docs/40`,
   `docs/42`, `docs/45`, `src/mgb_sediment.py:268`, `make_nb19.py`.** Flagged in the annotation as
   owed with a named refusal on the record (`docs/42` §9.7 **F7**), and **`docs/47` O12 left open**.
   Those are seven other owners' files; three are frozen.
8. **§2.5 C2, C3, C4, C5** — checked, none discharged by anything I could verify. C4's registered
   ONI remedy is still unexercised. Left as carried, recorded in `docs/47` §9.3.
9. **O2, O3, O4, O5, O8, O9, O10, O12** — all re-checked and all **still open**, each with the
   owner that re-affirms it, listed in `docs/47` §9.3 so a later session does not re-litigate them.
   **O11 is PARTLY discharged and I did not close it:** `docs/51` §1 supplies the Buarque provenance
   card, but `docs/51` §7 item 8 records that the durable copy and the same record for `ah703.pdf`
   and the parse scripts are **still owed**.
10. **`progress_map.html`.** The sweep's highest-value finding (its banner says *"C4 MAY NOW
    START"*, the opposite of the live verdict). **Not my file** and not in my scope. Flagged here
    because RULE 0 makes it the *status* authority and the sweep records that **no agent owns it**.

---

## D — RECOMPUTATION (measure before asserting)

Read-only against `data/processed/`; nothing written, no producing script run.

```
python3.10  — urh_ls2d_variants.csv, 32,782 rows, V4_buarque_2015 / V0_ours_2026_08

  weighted by area_km2   ->  0.421351985678496      -> 0.42135   (reproduces docs/47:391)
  weighted by n_cells    ->  0.42136472954222043
  weighted by area_frac  ->  0.4216185646720824

  ls2d_variants_summary.json : variants.V4_buarque_2015.ratio_to_V0 = 0.42136300143291305  REGISTERED
  ls2d_defect_b.json         : decomposition.V4_over_V0             = 0.42136300143291344  (independent)
  ls2d_defect_b.json         : decomposition.V4dg_over_V0           = 0.2446790094097074   REGISTERED (DG)
  ls_defect_a.json           : variants.V4_buarque_2015.f_area_urhfrac_areas = 0.4214751420286394
  ls_defect_a.json           : variants.V4_buarque_2015.f_ero       = 0.43194417543884817  (unmoved)

  16.7754 / 39.8123 = 0.42136224232209646  -> 0.4214 at 4 d.p.
  0.4214751420286394                       -> 0.4215 at 4 d.p.
```

**Conclusion, independently reached before reading the owning amendment's arithmetic.**
`docs/47:391`'s **0.42135** is the `urh_ls2d_variants.csv` **`area_km2`** support — a fourth
distinct number in the corpus after the registered per-cell 0.42136300143291305, the engine
`urh_fractions × minibacias` 0.4214751420286394, and the `n_cells` 0.42136472954222043. It is **not
a truncation** of the registered value (which both rounds *and* truncates to 0.42136). This matches
`docs/46` §10 amendment 2 (v) item 1 exactly. **`f_ero` — the number that decides — does not move**,
so no registered bracket, no α reference, no hard stop and no basin load moves.

**Also verified on disk this pass, first-hand:**
`src/mgb_transport.py`:908 = `if not (m <= max_resid):` · `tests/test_transport.py`:232, :245–277,
:274 = the NaN regression tests · `docs/42`:644, :648, :660, :803, :901 = the §9 amendment log,
A-P1.1's 0.009640 and F4/F5 · `docs/45`:644, :700, :1213–1215, :1731, :1850 = §8 Amendments 1–4 ·
`docs/35` §9 = §9.1–§9.4 **only**, no α-box re-registration · `urh_ls2d_variants.csv` and
`urh_ls2d.csv` headers = **no `V4_dg` column in either** · `ls -la docs/` = **no
`46_ls_preregistration_DRAFT.md`**.

---

## E — DISCLOSURE

- **Files written:** `docs/47_c4_entry_verdict.md` and this journal. **Nothing else.**
  `docs/30`, `docs/00_INDEX.md`, `docs/33`, `docs/35`, `docs/37`, `docs/42`, `docs/43`, `docs/45`,
  `docs/46`, `docs/48`–`docs/53`, `progress_map.html`, all notebooks, `src/mgb_transport.py`,
  `tests/test_transport.py`, `src/mgb_sediment.py` and both nbgen generators were **read and not
  edited**. No frozen document's registered text was touched; I own none of their amendment slots.
- **No original text was deleted anywhere in `docs/47`.** Every correction is a `~~strike~~` with a
  dated pointer naming the owning document, in the `docs/37` A2.7 / `docs/46` §10 house pattern.
  The two BLOCKING findings' bodies (§2.3, §2.4) are preserved verbatim as the provenance for the
  fixes that discharged them.
- **The verdict is not weakened.** `C4.3-BLOCKED` still holds; the title is unchanged; §9.2 states
  four surviving blockers where the document previously named one. **Nothing I wrote licenses a
  C4.3 start.**
- **No `git add` / `commit` / `push`. No engine default moved. No frozen artifact under
  `sim_calibrated_v2/` opened.** No calibration, no simulation, no `KGE_ln` evaluation, no α̂
  quoted, no materiality bar created or rescaled. The `docs/23` §13.2 yield embargo is in force —
  no t/km²/yr appears in anything I wrote.
- **Two numbers recomputed** (§D) rather than adjudicated by preference; every other number is
  quoted from the document that owns it, in place. **Where I could not close an item I said so** —
  O1 narrowed-not-closed, O11 partly-discharged-not-closed, and the B1 labelling disagreement
  printed rather than resolved.
