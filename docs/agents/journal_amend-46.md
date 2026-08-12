# journal — `amend-46` (the docs/46 amendment + freeze session)

**Task.** Sole permitted editor of `docs/46_ls_preregistration_DRAFT.md`. Apply `docs/51` §5.6
amendment set (a)–(e), with the bar decision handed down as NO NUMERIC BAR (`docs/52`), then
freeze the document honestly (as READ OUT), fill §9's card, open §10, and `git mv` the file to
`docs/46_ls_preregistration.md`.

## Log

### S1 — orientation (start)
Read, in order: `CLAUDE.md` (context), `docs/51_ls_freeze_decision.md` (full, 510 lines),
`docs/46_ls_preregistration_DRAFT.md` (full, 705 lines), `docs/52_materiality_bar_decision.md`
(full, 494 lines).

Key facts fixed before editing:
- The amendment set is `docs/51` §5.6 (a)–(e), five items; §7 items 1–3 are the same list as an
  execution order (enact, then decide the bar, then freeze — **do not edit §1–§8 after freezing**).
- `docs/52` §6 is the authoritative site-by-site disposition for item (e), and it says the bar has
  **fifteen** consumers, not ten: the ten literal-number lines plus `:163`, `:166`, `:220`, `:249`,
  `:421`. I must reach all fifteen or the frozen document retires a bar in §2 and then invokes it
  by name five more times.
- `docs/52` §8(d) flags a label change I inherit: under the (R4) disposition, H-M's field clause is
  **confirmed on its sign** (magnitude ×1.0088), not "REFUTED" as `docs/51` §3 records it. I am
  forbidden to edit `docs/51`, so this must be recorded in `docs/46` and reported.

### S2 — amendments applied (all edits are to `docs/46` only)
Order of application (each verified against `docs/51`/`docs/52` before writing):
1. Title + banner → FROZEN (READ OUT); READ-OUT disclosure hoisted into the banner.
2. (a) §1 "Also already known" → new **§1.0 THE BRACKET**: superseded numbers boxed as
   NOT QUOTABLE, registered statement `f_LS ∈ [0.25146, 0.43194]` ero / [0.24468, 0.42148]
   area, `1/f` 2.3151–3.9768, α ref 2.967–5.097, docs/35 band 1.484–2.548 … 5.935–10.194,
   hard stop 8.902–15.291, engine loads 129.3840 / 75.3235, POINT-plus-hybrid statement,
   three residues.
   *Arithmetic re-verified in python3.10 before writing*: 11.8·f, 35.4·f, 5.9/23.6·f, 1/f,
   299.5387·f, ln(0.43194/0.25146)=0.5410, |ln| endpoints 0.8395/1.3805, ratio 1.7177.
3. (c) §1.1 heading + verdict box; MEASURED annotations under Defect A and Defect B.
4. New **§1.2 READ-OUT register** — 11 clause rows, full precision, with sources.
5. (e) §2 bar block → **§2.0** (STRUCK; 4 grounds G-i…G-iv; prohibitions) + **§2.0.1**
   BAR-DEPENDENT register (5 entries + the NOT-bar-dependent list + the A5 σ_r note).
6. (e) clause sites: (R1) :163, (R2) :166, (R4) :189, (R7)/(R8) :216/:220, (R10) :240,
   (R12) :249, H-L :265, ADOPT-BAND :421, Δ_shape :490-491, Branch A :506, B1 :538 — all
   fifteen reached (the ten literal-number lines + the five `"materiality bar"`-only lines
   that `docs/52` §1.3 found).
7. (d) §2.2 (R6) closed CITED with the p. 47 quote, the p. 48 corroboration, the provenance
   card (LUME 10183/129875, sha256 3047624f…c0037, `data/raw/refs/buarque2015.pdf`,
   `docs/38` §9.1), the m/m sensitivity struck as retired; **§2.5.2** added for eq. 13 `Xdir`.
8. (c) **§2.5.1** — the mandatory re-derivation re-hung UNCONDITIONALLY (was "if H-L is not
   refuted", which could not fire); §7.3 items 2 and 3 re-hung the same way.
9. (b) §3.1 variant table — V4/V4′ **un-swapped**, `measured` column added, `V4_dg` row added
   (it is the variant that produces the registered POINT and was absent from the registry).
10. (a) §3.5 exact-engine load table added as the superseding box; heading corrected.
11. §4.2 item 5 three→**four** levers; ADOPT-SOURCE and ADOPT-BAND rows restated; three notes
    added (band not triggered; the interval is NOT an ADOPT-BAND band; reachable ≠ exercised).
12. §4.4 — honest statement that the ordering guarantee **cannot** be satisfied as written any
    more (totals already published) and what replaces it.
13. §6.1 exact discriminator `Δ_shape = 0`; §6.2 A2 bracket, **A4 recomputed** (7.54 / 12.958,
    plus the symmetric lower stop 2.10 per `docs/51` §5.4), **A5 σ_r = 0.465 struck** with no
    replacement (O8 open); §6.3 B1/B4/B5 + the standing-verdict box.
14. §8.3 "2.4×–3.0×" → 2.3151×–3.9768×.
15. §9 card filled (FROZEN (READ OUT), 2026-08-11, `amend-46`), §9.1 four conditions answered,
    **§9.2** added (what the freeze does NOT do), **§10 OPENED**.

### S3 — things I had to decide, and flagged in the return
- `docs/52` §8(d)'s label reversal: (R4)'s field clause is **confirmed on its sign**, not
  "REFUTED" as `docs/51` §3 has it. Recorded at the (R4) site and in §1.2; `docs/51` not edited.
- H-S is the **one** hypothesis not read out (`docs/51`'s own list omits it). Said so plainly
  rather than claiming a clean sweep.
- Added `V4_dg` to §3.1 and required CITED on **four** levers in §4.2 item 5 — both beyond the
  literal §5.6 list, both in the restrictive/completeness direction, both flagged.

### S4 — rename + a late, load-bearing complication
- `git mv docs/46_ls_preregistration_DRAFT.md docs/46_ls_preregistration.md` — the one permitted
  git command. `git status` confirms `RM`, history preserved. **No commit.**
- **While I was writing, `docs/53_delta_shape_pretest.md` landed**: `Δ_shape` was computed
  concurrently by the `delta-shape` agent. My §9 card said `Δ_shape` was "unmeasured and
  blinded", which stopped being true the same day.
  Resolution: I did **not** touch §1–§8 (they are frozen). I recorded it in **§10 as
  amendment 1**, dated, and corrected the three *card/banner* wordings (§9 is the card, not a
  frozen section) to point at it.
  The number: **0.1299456916752905**, argmax CAPITANEJO, null control 2.22e-16 ⇒ **Branch B
  mandatory**. **And the fact that matters most: under the STRUCK 0.1644 bar this would have
  said Branch A is available** — every V4-family reading is ≤ 0.1644, the largest by 0.3 %.
  `docs/52` decided blind and predicted its own asymmetry; this is the case that makes it bite.
  That is exactly the kind of thing this project would rather publish than tidy away, so it is
  in a box of its own in §10.
- docs/53 also discharges `docs/51` §7 item 7 (second erosion-weighted reproduction of the lower
  endpoint, `f_ero(V4_dg)` = 0.2514648985839397). §1.0's residue 2 struck in §10; residues 1 and
  3 stand.

### S5 — could not apply / out of scope
- Nothing in `docs/51` §5.6 (a)–(e) was left unapplied.
- `docs/51` §7 items 4, 6, 8, 9 are owed to **other** files (docs/37, docs/47, docs/38, docs/42)
  and I am not permitted to edit them; each is registered in `docs/46` §7.3 as owed.
- `docs/51` §3's "(R4) FIRES ⇒ H-M field clause REFUTED" is now wrong under the bar decision.
  `docs/51` is evidence I may not edit; flagged at the (R4) site, in §1.2, and in the return.
