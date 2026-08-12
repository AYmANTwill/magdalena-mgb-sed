# journal — ls-freeze-decision

Agent: `ls-freeze-decision`. Started 2026-08-11.
Task: decide whether `docs/46_ls_preregistration_DRAFT.md` can be FROZEN; restate the LS
bracket; answer §9.1's four items; state the consequence for `docs/47`'s BLOCKED verdict.
Deliverable: `docs/51_ls_freeze_decision.md`. May not edit `docs/46`. No git.

## 1 — Orientation (done)

Read in full: `CLAUDE.md`, `docs/46` (704 lines, all sections), `docs/47` (677 lines, all
sections). Inputs supplied by the orchestrator: the variants harness read-out + its audit,
the two defect-resolution read-outs (A and B), and the two debt-track read-outs (B4, B5).

Key numbers carried in from those read-outs, to be checked against the files on disk:
- V4 = 16.775413430326214 area-wtd, f_area 0.42136; f_ero 0.43194 (docs/47 §4.3)
- V4' (cap joint) = 16.749164, f_ero 0.430381 — NEVER previously measured
- V2b (eq. 14 step) = 20.108840, f_area 0.50509, f_ero 0.52200
- V5 (L form isolated) f_area 0.769833 vs published 0.790 -> |dln| 0.0258
- source-formulation DG-L endpoint: f_area 0.244679 / f_ero 0.25146
- docs/47 bracket: f_LS in [0.25146, 0.43194] ero-wtd => 1/f in [2.3151, 3.9768]

## 2 — Work log

### 2026-08-11 — §9.1 item 2 SETTLED FROM THE PRIMARY SOURCE (the big one)

The Buarque (2015) thesis PDF is **on disk in this session's own scratchpad**:
`.../3d81998f-.../scratchpad/buarque2015.pdf`, 9,646,521 bytes,
sha256 `3047624f641b335900eb3bc2191308b03a22148bd30aeb7227031bf42e1c0037`, 182 pages,
retrieved by `ls-evidence` from `lume.ufrgs.br` handle `10183/129875` (journal_ls-evidence S4).
PDF page 63 = printed page **47**; PDF page 64 = printed page **48**.

**(R6) is RESOLVED: `Sf` is slope PERCENT.** Verbatim, printed p. 47, immediately under eq. (14):

    onde Sf [%] é a declividade do pixel.

and eq. (14) itself reads `m = 0,2 se Sf < 1 | 0,3 se 1 <= Sf < 3 | 0,4 se 3 <= Sf < 5 |
0,5 se Sf >= 5`. Corroborated independently on printed p. 48 under eq. (18):
`S_k = 65,41 sin^2(theta_k) + 4,56 sin(theta_k) + 0,065`, **"sendo theta o valor de Sf em
graus"** — a conversion note that is only meaningful if Sf is NOT already in degrees.
Residual honesty: eq. (15) `Sf = sqrt((dz/dx)^2+(dz/dy)^2)` is written as a dimensionless
gradient; the x100 is not written. The source is therefore internally loose, but the unit tag
is explicit, the degrees reading is excluded by the eq.-18 note, and the m/m reading is
excluded by both the tag and physical inadmissibility (breakpoints at 100/300/500 % slope).
**Single admissible reading.** So the docs/49 sensitivity "x0.329 if m/m, 6.8x the bar" is
RETIRED as a live risk, and the harness's `sf = 100*tan(theta)` is the source's own unit.

Also on p. 47, for the record: eq. 13's `Xdir` = 1 orthogonal / sqrt(2) diagonal, and slope by
centred finite differences over the 4 orthogonal neighbours (Wilson & Gallant 2000) — ours is
Horn 3x3. That is a slope-FIELD difference, declared, not part of (R6).

### Checks I ran myself (not carried)

- `data/processed/ls_defect_a.json` and `ls2d_defect_b.json` read directly. f_ero(V4)=0.43194418,
  f_ero(V4')=0.43038143 => |ln| 0.003625. Area: V4_dg/V0 = 0.2446790094, V4p_dg/V0 = 0.2444309.
  So Defect A moves the LOWER end by |ln| 0.00101 and the UPPER end by 0.00362 — immaterial at
  both ends, not just at the one docs/49 measured.
- Cross-check of the two erosion-weighted endpoints against docs/47 R7's independently measured
  proxy bias: 0.43194418/0.42147514 = 1.024839 (R7 says 1.0251) and 0.25146/0.24467901 = 1.027714
  (R7 says 1.0278). Consistent to 4 s.f. — the ero and area endpoint pairs are mutually coherent.
- 1/f: 1/0.43194418 = 2.3151140; 1/0.25146 = 3.9767756. ln width 0.5410 vs published 0.2345
  (x2.307 wider). alpha ref 11.8*f = 2.9672 - 5.0969.
- `scripts/c3/ls2d_variants.py:148` `m_step_eq14` uses sf = 100*tan(theta), half-open 1/3/5 —
  EXACTLY the source's eq. 14 under the now-verified [%] reading. `:186-190` and
  `ls2d_defect_b.py:146` carry `x_aspect ** m` in the D&G denominator — exactly Buarque eq. 13's
  `Xdir^m` (Xdir = 1 orthogonal, sqrt(2) diagonal, p. 47). So the aspect convention docs/50 flagged
  as UNVERIFIED (worth x1.149 on the lower endpoint) is now CITED to the transposed source itself.
- No per-URH V4_dg column exists (`urh_ls2d_variants.csv` header checked), so the lower endpoint's
  EROSION-weighted value rests on ONE engine re-run (docs/47 4.3) against THREE area-weighted
  reproductions. Recorded as a verification gap, not a blocker. I did not re-measure it.

### Decision taken

DO NOT FREEZE as drafted; freeze after a 5-item amendment set (all but one mechanical). Reasons:
the draft's headline bracket, its V4/V4' labels and its (R6) status are now falsified/settled by
measurement, and its 0.1644 materiality bar rests on a derivation docs/47 D2 measures 4.2x wrong
(docs/48 says decouple, not rescale — and it flips (R10)). docs/47's BLOCKED verdict HOLDS.

### Deliverable written

`docs/51_ls_freeze_decision.md` (8 sections). Verdicts: Defect A RESOLVED-IMMATERIAL, Defect B
RESOLVED-MATERIAL, freeze = DO NOT FREEZE AS DRAFTED (5-item amendment set first, 4 mechanical
+ 1 decision on the materiality bar), docs/47 BLOCKED verdict HOLDS.

Things a successor must not re-derive:
- The Buarque PDF is at `.../3d81998f-.../scratchpad/buarque2015.pdf`, sha256 3047624f...c0037.
  PDF page 63 = printed 47, PDF page 64 = printed 48. It WILL be lost with the scratchpad —
  docs/51 item 8 asks for a durable copy.
- The bracket does NOT move: [0.25146, 0.43194] ero, exactly docs/47 4.3. My run confirms it.
- The interval is a POINT (source read whole, x0.25146) plus a HYBRID (x0.43194, our L). The
  span between them IS the L-form lever: ln(0.43194/0.25146) = 0.5410 = -ln(0.5807).
- Do not "fix" docs/46's 0.1644 bar by substituting 0.6936: at 0.6936 (R10) flips and the
  bracket width becomes immaterial. docs/48 says decouple. That is a decision, not arithmetic.

Dead ends / traps hit:
- cp1252 UnicodeEncodeError printing the extracted Portuguese/math text to stdout on this box
  (same trap docs/49 hit). Write to a utf-8 file and Read it instead.
