# Journal - refute-t6-5

Role: REFUTER (read-only). Target finding: docs/45 §7.1 registration card says
"Amendments | THREE" while §8 contains four; the missing one is Amendment 4
(re-expresses the C4.3 gate into Pi).

Default posture: the finding is WRONG until I fail to kill it.

## Step 1 - is the quote verbatim? YES

```
grep -n "^## 8\.[0-9]" docs/45_c4_preregistration.md
700:  ## 8.1 - Amendment 1 - the +-38 % Pi band is REPLACED ...
951:  ## 8.2 - Amendment 2 - PRE-FIT DISCLOSURE ...
1109: ## 8.3 - Amendment 3 - LS bracket 2.37x-3.00x SUPERSEDED ...
1163: ## 8.4 - Disclosure for this amendment set
1213: ## 8.5 - Amendment 4 - the C4.3 gate is RE-EXPRESSED IN Pi ...

sed -n '644p' docs/45_c4_preregistration.md
| Amendments | **THREE, all dated 2026-08-12, all in §8, by the `amend-45-piband-disclosure`
agent** ... **Amendment 1** ... **Amendment 2** ... **Amendment 3** ... |
```

`grep -c "^## 8\.[0-9]* — Amendment"` = **4**. §8.4 is a disclosure, not an amendment.
So the count is objectively FOUR and the card says THREE. **The misquote route is closed.**

## Step 2 - is the context a supersession block / historical register? NO

§7 is "Registration record"; §7.1 "The card". It is body text of a frozen pre-registration whose
whole job is to be the authoritative summary a C4.3 session reads. It is not a strike-through, not
a `[WARN]` block, not a register of deliberately-printed superseded numbers (unlike docs/39,
docs/46 §1.0/§3.5, docs/47 §3). The card cell was itself UPDATED by the first amendment pass
(docs/45:889 change log: `| 17 | §7.1 card, :577 | Amendments **none** | **Amendments 1, 2, 3** |`),
which proves the house treats this cell as live and updatable, not as a frozen historical string.

House precedent confirms the same: `docs/42`:648's card cell was extended by a later pass -
*"THREE, all dated 2026-08-11 - A-P1, A-P2, A-P3, plus A-P1.1 ... **Plus A-P4, dated 2026-08-12
(§9.7)**"*. And `docs/47` §2.4 **D4** numbered the docs/42 card cell reading `none` as an
audit-trail defect. So this defect CLASS is already recognised in this project.

## Step 3 - the finding's ONE real weakness: the defect is already self-disclosed

`docs/45`:1789, inside Amendment 4's own §8.5.12 ("Defects ... in files this amendment does not
own - REPORTED, NOT FIXED"), item 4:

> **§7.1's card cell now under-counts the amendments** - it reads *"Amendments | **THREE**, all
> dated 2026-08-12"*; there are **four**. §7 is outside this amendment's ownership (§8 only) and
> is **not edited**; the correction is owed to that section's owner.

So the artifact ALREADY carries the correct count, dated, with the ownership reason and an explicit
"owed to that section's owner". The finding presents this as an undiscovered defect; it is a
disclosed, ownership-blocked one. That does not kill the finding (the wrong number is still in the
frozen card, unfixed) but it caps the severity.

## Step 4 - is the claimed CONSEQUENCE sound? Partly - it overclaims

Claimed: "A session trusting the card would run the gate in the retired convention and could read a
corner as clearing that Amendment 4 measures as railed."

Checked against §8.5.5 / §8.5.8 / §8.5.10:
- §8.5.5 proves and verifies bitwise that at the REGISTERED configuration (`f_LS` = 1.000) the Pi
  re-expression is the **IDENTITY**: same admissible set, same rail band, same grid step, same
  budget, same bar. §8.5.10 item 9: nothing in §2-§6 is struck "because [2.0, 30.0] is still
  correct". So a session running the gate TODAY gets the identical answer with or without
  Amendment 4. No gate number is wrong in the card.
- The conventions diverge only for `f_LS != 1`, i.e. after an LS-field swap. That requires C3.1's
  ACT 2 and a committed `V4_dg` column, which §8.5.2 measures as non-existent, and
  `C4.3-BLOCKED-UNTIL-LS-LANDS` is standing with Branch B mandatory.
- The card states no convention at all, so it cannot itself steer a session into convention (i).
- BUT the direction of the claimed harm is real, not invented: under convention (i) the beta = 0.65
  corner *does* clear (alpha-equivalent 5.125963930785862 > 3.9), and under (ii) it rails. I
  reproduced Amendment 4's arithmetic:

```
python3.10 -c "k0=437.66113721058014; f=0.2514648985839397; ..."
Pi_lo 875.3222744211603
Pi_lo*f 220.11282696558052
rail_lo 1488.0478665159726
564.145../Pi_lo shortfall 1.5515903801396431
5.126 vs 3.9 clears under (i): True
```
Every figure matches the published values to every printed digit. So the substance the card omits
is real and consequential in the convention-(i) world - just gated behind an LS swap that is
currently impossible.

## Step 5 - re-raise of a retired/refuted claim? NO
Checked docs/47's refutation register (R6/R7/R8 etc., all LS-formulation matters) and the retired
items (0.1644 bar, (R10), SDR 0.05-0.30, mountainous LS 2-10). None concerns an amendment count.
Not a category error either: it is a count, not a bar, not f_ero-vs-f_area, not level-vs-shape.

## Step 6 - something the LENS MISSED, which strengthens the finding
`docs/45`:691, the §8 preamble - **"No longer empty. Three amendments, all 2026-08-12, all by the
`amend-45-piband-disclosure` agent."** A SECOND stale-count site, and this one is inside §8, the
slot Amendment 4 does own (its disclosure only claims §8.1-§8.4 were untouched). So Amendment 4
could have fixed that site without any ownership problem and did not. The fix must cover both
sites, not just line 644.

## VERDICT
**Could not kill it.** refuted = false. The string is verbatim, the count is objectively four, the
site is live body text of the registration record, and the house has fixed exactly this cell before
(docs/45:889) and in a sibling document (docs/42:648).

Severity corrected **HIGH -> MEDIUM**: no gate number, threshold, box or admissible set is
misstated by the card (the re-expression is the identity at the registered configuration, verified
bitwise and re-verified here); the defect is already registered with the correct count and correct
ownership at §8.5.12 item 4; and the claimed operational harm requires an LS swap that the standing
C4.3 block precludes. It is a real, unfixed audit-trail/navigation defect in a frozen document's
own registration record - worth fixing, not blocking.
