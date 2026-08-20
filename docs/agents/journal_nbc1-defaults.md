# journal — nbc1-defaults (engine-default / executed-output staleness fact sheet)

**Agent:** nbc1-defaults. **Phase:** T1 audit, READ-ONLY. **Date:** 2026-08-13.

## What I was asked

Be the single authority on whether each notebook's *executed outputs* are stale relative to the
current sediment-engine defaults (chiefly `ls2d_column`, after the ACT 2 move to `V4_dg`).
Deliverables: (1) current defaults from code with file:line; (2) the ACT 2 effect measured from
git; (3) per-notebook 01–19 verdict STALE / CURRENT / N-A with evidence; (4) sanity-anchor the
gate numbers WITHOUT executing anything.

Hard constraints obeyed: no edits to notebooks / nbgen / src / docs; no git write ops; no notebook
execution; no fits; only this journal is written by me.

## Log

### 00 — orientation
- `git log --oneline -25` confirms the ACT-1/ACT-2 pair and the ordering claim to verify:
  `57f9761 WIP c3.1: A3 enactment + defect/T3 fixes + docs/54 closure` sits BELOW (older than)
  `7e2daef c3.1 ACT 1: materialise V4_dg` and `c3fdb55 c3.1 ACT 2: switch engine default LS to
  adopted source field V4_dg; pin V0 records explicitly`.
- Notebook extracts present for 01–19 in the scratchpad `nbtext/` dir.
