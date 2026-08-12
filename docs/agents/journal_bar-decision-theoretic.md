# journal — `bar-decision-theoretic`

Agent task: propose ONE materiality bar for `docs/46` §5.6 item (e), argued from the
DECISION-THEORETIC angle (what is the bar FOR?). Independent option; I do not edit `docs/46`.

**Blinding contract accepted.** I will not compute, estimate, or reason toward where
`Δ_shape` lands. If I catch myself doing it I will say so here.

## Log

### 2026-08-11 — orientation
- Read `docs/51` in full. The five-item amendment set is §5.6; (e) is mine.
- Confirmed the bar-dependence table (`docs/51` §5.5): only (R10) at 0.2983 and the bracket
  WIDTH at 0.5410 turn on the bar. Everything else is robust at both 0.1644 and 0.6936.
- Next: `docs/46` (all ten decision points, verbatim), `docs/47` §2.2 + the ENSO-ratio
  measurement, `docs/48` §5, `docs/34` (the deliverable itself).

### finding 1 — the bar is invoked at **13** sites, not 10
`grep -n "0.1644\|materiality bar" docs/46` gives 135,138,140,163,166,189,216,220,239-240,
249,265,421,490,491,506,538. Grouped into *decision sites*: definition (135-142), **R1 (:163)**,
**R2 (:166)**, R4 (:189), R7 (:216), **R8 (:220)**, R10 (:239-240), **R12 (:249)**, H-L (:265),
**ADOPT-BAND (:421)**, branch table (:490-491), Branch A (:506), B1 (:538).
`docs/48` §5.3's enumeration (the one the task carries) omits **R1, R2, R8, R12 and
ADOPT-BAND**. An amendment that edits only the enumerated ten leaves the bar live in five
places. Flagged for whoever edits `docs/46`.

### finding 2 — every measured comparison is bar-insensitive over a factor-9.3 window
Recomputed from the primary numbers, not copied:

| comparison | \|ln\| |
|---|---:|
| (R4) H-M field, 0.52204 vs 0.51748 | 0.00877 |
| (R12) proxy vs exact, 0.43194 vs 0.42148 | 0.02454 |
| H-L, f(V5) vs 0.790 | 0.02580 |
| (R2) f_ero(V1) 0.362435 vs area 0.351 | **0.03206** ← largest "immaterial" |
| (R10) product vs joint | **0.29834** ← smallest "material" |
| bracket width / endpoints | 0.54100 / 0.83947 / 1.38047 |

(R10) reproduces at 0.29834 only with the **step** `m` (0.362435 × 0.52204 × 1.694054 =
0.320524); with the cap it is 0.30711. Any bar in **(0.0321, 0.2983)** returns the identical
verdict on *everything docs/46 has already measured*. So the bar's only undetermined consumer
is `Δ_shape`. **Blinding note:** I noticed that `docs/51`'s stated bound on `Δ_shape` lies
inside this window. I did not use it, and Rule 4 below returns the same action at every value,
so it cannot have been influenced by it.

### finding 3 — my own brief's derivation is REFUTED by measurement
Deliverable elasticity, computed from `docs/47` §4.4's four measured pairs:
2.2915→2.2694 / 2.2665 and 3.9725→3.9364 / 3.9329 against |ln f_LS| 0.8395 / 1.3805 ⇒
`|Δln contrast| / |Δln f_LS|` = **0.00726 – 0.01154**. Inverting at the most favourable end:
a 1 % tolerance on the contrast ⇒ bar **0.862 ln** (×2.37); 2 % ⇒ 1.715 (×5.6); 10 % ⇒ 8.26
(×3,851). And `docs/34` §2 registers the observed contrast as a **range ≈3–5**, forbids a single
number, and tests agreement by **CI overlap** — so no tolerance is cited and none is sharp.
**A deliverable-derived bar swallows its own subject worse than the corrected SE does.** The
naive reading of my angle is dead; the useful reading is the loss-function one.

### finding 4 — the α route is forbidden by the document's own rule
Narrowest registered verdict cell in α is [3.40, 3.9] ⇒ ln = **0.1372** (suspiciously near
0.1644 — which is itself a reason for suspicion, not comfort). **Discarded:** `docs/46` §4.3
bullet 4 forbids "any α band" as evidence in any outcome, and the box is LS-conditional, so
deriving the LS bar from it is circular. Computed, then thrown away, recorded here so it is
not re-derived by someone else.

### 2026-08-11 — conclusion
Three candidate derivations of a single number (noise / deliverable / α-gate) are each
excluded — one falsified, one refuted by measurement this pass, one forbidden. Proposal is
therefore **retire the number**; replace with four consequence-typed rules. Structured output
submitted.
