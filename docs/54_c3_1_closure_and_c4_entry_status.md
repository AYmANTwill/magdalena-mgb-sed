# 54 — C3.1 enactment: closure record and C4.3 entry status

**Synthesis written 2026-08-12 (orchestrating-session/thinking layer) from the C3.1-enactment
run's outputs, every claim verified against its primary on disk this pass.** This is a
**pointer-justified** document: the evidence for each statement lives in the cited primary
(`docs/37` A3, `docs/47` §9.2, the `refute-t6-*` journals), not duplicated here.

> **What this document does and does not do.** It **records** the state after the C3.1-enactment
> run. It moves **no engine default**, opens **no frozen artifact**, introduces **no new number and
> no band**, and is **not committed** (the orchestrating session commits). It is written under the
> same standing rules the run was: *an uncited band cannot pass or fail a gate; a negative result is
> publishable; measure before asserting.*
>
> **The C3.1 closeout is NOT complete.** The run that produced A3 **crashed in its Phase 4/5**
> (finding-refutation + this synthesis) on a usage limit. Four adversarial findings survived
> refutation and are **unresolved**; the whole ~40-file changeset is **uncommitted** (last commit
> `e5b3c8e` is the *pre-run* state). §7 is the residue owed before C3.1 can be called closed.

---

## 1 — The verdict

**C3.1 — the LS *formulation* subtask — is ENACTED.** `docs/37` **A3** (2026-08-12), the owner of
C3.1 named by `docs/46` §9's registration card: **ADOPT-SOURCE**, `ls_formulation =
buarque_2015_dg`, decided on written source grounds.

**C3 stays OPEN. `C4.3-BLOCKED` STILL HOLDS — C4.3 may not start.** B1 (the C3.1 formulation
decision) was **necessary and is measured NOT to have been sufficient** (`docs/47` §9.2; `docs/37`
A3.4 heading: *"Is C4.3 thereby UNBLOCKED? **NO** — this amendment is the act that makes the block
*dischargeable*, not the act that discharges it."*).

One-line reason: the LS **formulation** is decided; the LS **level** and α's like-for-likeness with
a 2-D contributing-area LS are **not**, and cannot be settled by any fit — the design matrix has
condition number **∞**, so only Π = α·f_vol·f_K·f_LS·C_mult·P·FG is identifiable (`docs/47` §8.1,
A3.1.4(C)). The C4.3 gate is denominated in a unit whose *scale* C3.1 has not fixed.

## 2 — The adopted formulation and its evidence grades (`docs/37` A3.1.4 — four distinct propositions)

| # | proposition | grade |
|---|---|---|
| A | the adopted formulation is what Buarque (2015) prints, on all four levers (limiter pp. 94+98, `m` eq. 14 p. 47, `S` eq. 18 p. 48, `L` eq. 13 p. 47) | **CITED** |
| B | `f_LS(buarque_2015_dg)` = **0.25146** erosion-weighted / **0.2446790094097074** area-weighted, **on our terrain, our engine, at adopted defaults** | **DERIVED** |
| C | the LS **LEVEL** is correct / validated | **UNVALIDATED**, unchanged by adoption (`docs/42` G4.2; *cited ≠ validated ≠ fitted*) |
| D | α = 11.8 (Williams 1975) is like-for-like with this 2-D contributing-area LS | **UNRESOLVED**, no band offered (`docs/47` §4.2 O4) — bounds every A3.2 number from above |

Excluded from grade A **by name**: `min(m, 0.5)` — *"nobody's published formulation; may NEVER be
graded CITED"* (`docs/46` §2.2). Buarque's eq. 14 is a **step function on slope percent**, a
different object (the T2b correction, §6).

## 3 — The named unblock events (`docs/47` B1–B5)

| event | what | status |
|---|---|---|
| **B1** | C3.1 LS-formulation decision | **LANDED** (`docs/37` A3) — necessary, not sufficient |
| **B2** | re-express the C4.3 gate off the ±38 % Π band / α box | **DISCHARGED** (`docs/45` §8 amd 4); the *threshold-moving* half is PROPOSED only (`docs/45` §8.5.11 item 2) |
| **B3** | `mgb_transport` NaN mass-audit fix | **DISCHARGED** (`docs/47` §2.3; suite **140 passed** at that commit — re-verify, §7) |
| **B4** | `docs/42` §9 transcription | **DISCHARGED** (`docs/47` §2.4) |
| **B5** | (SSC coordinate fetch — Phase-C data track, unrelated to C4.3 entry) | not in scope here |

## 4 — Why C4.3 STILL may not start: the four surviving blockers (`docs/47` §9.2, verbatim-owned)

The block **no longer rests on B1, and not on B2 either.** It rests on four conditions, each
verified against its owner:

1. **Branch B is MANDATORY → the fit must be a FIRST RUN on the adopted LS field.** `Δ_shape =
   0.1299456916752905 ≠ 0`, so `α̂` is **not** recoverable by rescaling a surface already seen
   (`docs/53`; `docs/37` A3.4(3)). Branch A is **CLOSED** — there is **no legal PROVISIONAL C4.3**.
2. **The adopted variant is NOT a committed product.** `urh_ls2d_variants.csv` has **no `V4_dg`
   column** and `urh_ls2d.csv` may not be overwritten; *"C4.3 cannot consume a variant that no
   committed product carries"* (`docs/37` A3.4(4)) — confirmed on disk (its columns are
   `V0_ours_2026_08 … V5_L_dg96_fd`; no `V4_dg`).
3. **ACT 2 — the default switch — is NOT DONE and cannot yet be drafted.** ADOPT-SOURCE is
   *determined and recorded but not exercisable*; `src/mgb_sediment.py` defaults remain
   `ls2d_column = "ls2d_hs"`, `urh_ls2d = "urh_ls2d.csv"`. ACT 2 **may not precede ACT 1** (`docs/37`
   A3.5.1).
4. **Deliverables owed before entry:** `docs/46` §3.3 stratified report (slope terciles per variant;
   per-station erosion-weighted `LS̄` as **levels**, not ratios) · `docs/46` §2.3 H-S field clause
   (R7)/(R8) items 2–3 · the `docs/35` §9 amendment `A3.1.3` records as owed.

Still-open items re-affirmed by this pass (`docs/47` §9.3): **O4** (α like-for-likeness), **O5** (the
objective re-profiled on a corrected LS **field**, not axis — *"nobody has done this"*), O2, O3, O8,
O9, O10, O11 (partly discharged — `docs/51` §1), O12.

## 5 — What enactment does NOT do (the ownership boundary)

No engine default moved in A3, and none moves here. **ACT 2** — switching `ls2d_column` and
`urh_ls2d` to the source variant — is a **separate dated act in the file that owns
`scripts/c3/ls2d.py` and `urh_ls2d.csv`**, and its trigger is **ACT 1**: materialising the `V4_dg`
column into a committed product (blocker 2). Switching a default by name before ACT 1 is forbidden
(`docs/37` A3.5.1).

## 6 — Defect and finding status (T2, T3, T6)

- **T2b — the `min(m,0.5)` = "Buarque eq. 14" mislabel: CORRECTED.** `docs/35` §9.4 strikes it
  (`min(m,0.5)` is a **CAP** (variant V2a); Buarque eq. 14 is a **STEP FUNCTION on slope percent**
  (V2b) — a different object), strikes the superseded `×0.333–×0.421` / `2.37×–3.00×` brackets, and
  re-bases §9.3.3 to the adopted **299.5387088405831 Mt/yr**. **`min(m,0.5)` may never be graded
  CITED.** Notebook safety **verified this pass:** nb18 and nb19 were regenerated and **still
  reproduce 299.5387 / 248.7298**.
- **T2a — `f_area(V4)` cross-file discrepancy: FLAGGED, reconciliation OWED.** `0.42136300143291305`
  (`ls2d_variants_summary.json`, `ls2d_defect_b.json`) vs `0.42147514` (`docs/51` §2.2, `docs/46`
  §3.1), 2.7e-4 relative; the on-disk value makes R7's consistency check *better*. Not adjudicated
  here — the correction is owed through the amendment slots (recompute from
  `urh_ls2d_variants.csv`), because `docs/46` is FROZEN and this is a synthesis, not its owner.
- **T3 — the ±38 % Π band revision: ENACTED.** `docs/45` §8 Amendment 1 (2026-08-12) **retired** the
  `0.1644 ln = ±38 %` band (measured SE `0.6936`/`0.4775 ln`, not `0.1644`) for the **station
  bootstrap**, and corrected `k_min` `0.0209 → 0.0838 /km` (≈173× detectability floor, not 3.54×).
  Carried through `docs/42`, `docs/43`, `docs/45`, `docs/48`.
- **T6 — four adversarial findings SURVIVED refutation and are OPEN** (the crash hit before they were
  resolved). All four are **wording / dangling-reference / label** defects; **none touches a
  canonical result number.** Each must be closed through its owning doc's amendment slot (or, for the
  generator, the notebook track):
  1. `refute-t6-1` (**HIGH**, freeze-honesty) — an over-strong *"asserts"* at **`docs/37`:241**;
     *"could not kill it — HIGH stands."*
  2. `refute-t6-4` (**HIGH**) — `docs/51` §3/§4 verdict tables still print struck-instrument verdicts
     *"(R4) FIRES ⇒ REFUTED"* against the **struck 0.1644 `bar`** with no `docs/52` pointer, in tables
     the INDEX advertises as executable; the *"fourth retired band"* wording is an overclaim to drop
     (owed to `docs/51`'s owner per `docs/52` §8(d)).
  3. `refute-t6-6` (**HIGH**, a3-overreach) — `docs/37`:1421–1422 (A3.1.1 verdict cells): an
     engine-state/outcome conflation (*"V0 retained"* as a §4.2 outcome), a factor correction (the
     fallback-vs-fallback gap is **×2.3151**, not ×1.7177), and a missing locator (A3.7's `docs/35`
     row (a)).
  4. `refute-t6-2` (**CRITICAL**, dangling reference) — the **retired ±38 % / 0.1644 ln band is still
     live in `src/nbgen/make_nb19.py`** (the `σ_r = 0.465`, 8-station block). Fix is a generator edit
     + re-execute, which this run's *"enactment is a written amendment"* rule defers to the notebook
     track: **register `make_nb19.py` as an owed site** now, hand the regeneration over.

## 7 — Residue owed before C3.1 is CLOSED (the crash left this undone)

1. **Resolve the four §6 T6 findings** — each via a refuter that defaults to "the finding is wrong,"
   then the wording/label fix through the owning doc's amendment slot (and, for finding 4, register
   `make_nb19.py` for the notebook track).
2. **Commit the changeset.** ~40 files are uncommitted (`git status`); nothing from the run is in
   history. The orchestrating session reviews and commits — *before* any new agent run, or a fresh
   session may clobber it.
3. **Re-run the test suite** — `src/mgb_sediment.py` is in the uncommitted set, so confirm still
   **140 passed** (or record the new count) from executed output, never an exit code.
4. **This document** is a synthesis pending the orchestrator's review and commit.

## 8 — Grade of this document

A synthesis whose every claim is a pointer to a primary verified on disk this pass. The C4.3 verdict
is **CITED** from `docs/47` §9.2 and `docs/37` A3.4; the four blockers are **CITED** from `docs/47`
§9.2's table (each re-verified — e.g. the absent `V4_dg` column read from disk); the four T6 findings
are **CITED** from their journals and carried **OPEN** (unresolved), never as closed. **No new number,
no band, no engine default.**
