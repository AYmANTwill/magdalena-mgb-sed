# Journal — c3gate-synthesis

Task: write docs/47_c4_entry_verdict.md; decide whether C4.3 may start and under what contract.
Started 2026-08-11.

## Plan
1. Orient: CLAUDE.md, docs/00_INDEX.md, docs/43, docs/45, docs/42 (§4.2, §9), docs/37 (§4, A1, A2), docs/46 DRAFT.
2. Weigh the 8-lens evidence handed to me (2 surviving critical/high on gate logic, 1 high on transport code,
   plus LS track: evidence / impact / draft prereg).
3. Independently verify the load-bearing arithmetic where cheap (alpha implied level, sigma_r propagation,
   LS bracket, alpha-absorption factor).
4. Write docs/47. Do not commit.

## Log
- (start) listed docs/, git log. docs/45 and docs/46_ls_preregistration_DRAFT.md exist; docs/44 does NOT exist
  (numbering gap — note in the doc if load-bearing).

## Orientation done (read, not skimmed)
- docs/43 in full (360 lines). docs/45 in full (615). docs/42 §1-2, §4.2-4.3, §8.2, §9. docs/37
  clause table, §4 candidate 0 (lines 177-265), §5. docs/46 DRAFT §6 (the C4.3 gate) + §7.
- CONFIRMED by direct read, not carried: docs/42 §9 still reads "Amendments | none" and
  "Registered station sets | CAL 13"; §4.2's power table still prints CAL-13 k_min 0.0104 /km
  (NOT 0.0096, which is what docs/43 P1 says it prints). P1/P2/P3 transcription is unperformed.
- CONFIRMED: docs/44 does not exist (docs/45 §7.2 explicitly declines to claim it). 47 unclaimed.

## Measurements I made myself (not carried)
1. src/mgb_transport.py:901-903 read directly. `m = float(np.abs(resid).max()); if m > max_resid`.
   Ran: np.abs([nan,0,0]).max() -> nan; nan > 0.0 -> False; max_resid stays 0.0; line 803
   `node_partition_exact = float(max_node_residual) == 0.0` -> True. inf*0.0 -> nan confirmed.
   The transport-code finding is CONFIRMED by reading the code + the IEEE-754 demonstration.
2. THE DECISIVE ARITHMETIC (mine). alpha and f_LS are both pure multiplicative level factors
   entering MUSLE linearly (docs/42 §3.1), so the objective depends only on the product
   alpha*f_LS and the argmax alpha scales EXACTLY as 1/f. Erosion-weighted LS bracket
   f in [0.25146, 0.43194] -> 1/f in [2.3151, 3.9768]. Applied to the refutation agent's
   measured optima on the REGISTERED window/estimator/objective:
     geo-mean log-level      1.211 -> 2.804 .. 4.816
     argmax F_search b=0.56  0.625 -> 1.447 .. 2.485
     argmax F_search b=0.65  1.289 -> 2.984 .. 5.126
     argmax F_report b=0.56  0.117 -> 0.271 .. 0.465
   Rail band on box [2,30] at 5% of linear range = alpha < 3.40 or > 28.60. docs/35 stop 3.9.
   => At adopted LS the search rails at the floor in EVERY G2.3-admissible beta. Under the LS
   bracket, one corner (beta near 0.65, DG-L endpoint) reaches 5.13, i.e. clean. THE LS DECISION
   DETERMINES THE C4 VERDICT. That is the decisive argument.
3. Scalar-proxy check: erosion-wtd/area-wtd = 1.0251 (continuous L) / 1.0278 (DG L).

## Dead end / not done
- I did NOT run docs/46 §6.1's Delta_shape pre-test (the registered Branch A/B discriminator).
  It costs minutes and is now an OPEN ITEM, not a finding.
- I did NOT re-profile F_report under a corrected LS field. Rescaling the alpha axis is exact
  for the LEVEL but does not hand me F values at the new box endpoints. Stated as open item.

## Verdict reached
BLOCKED_UNTIL_LS_LANDS, with a narrow LS-invariant exception. Writing docs/47 now.

## Done
Wrote c:\dev\magdalena-mgb-sed\docs\47_c4_entry_verdict.md (8 sections + cross-reference table).
Verdict: C4.3-BLOCKED-UNTIL-LS-LANDS. Four blocking repairs B1-B4 (+B5 owed before printing),
six-item contract in §6.2, bounded now-permitted work in §6.3, 12 open items in §7.
NO git command run. docs/35/37/42/43/45/46 read, none edited. No frozen artifact opened.

Successor notes:
- The single most useful unrun measurement is docs/46 §6.1's Delta_shape. Minutes. Run it BEFORE
  C3.1 reports so it cannot be read backwards.
- If someone argues for Branch A anyway, the killer is §5.4 point 2: the objective surface has
  ALREADY been profiled across the whole registered box (journal_refute-gate-logic-alpha.md), so
  Branch A buys nothing and costs the registration.
- I did NOT decide the governance question (O9): amendment vs fresh pre-registration for docs/45
  after the pre-fit profile. Deliberately left to the document owner.
