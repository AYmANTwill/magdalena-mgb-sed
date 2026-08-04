# Journal — calibration-launch agent

**Goal:** pre-register (docs/29_seed_expansion.md) and DETACH the seed-expansion
calibration queue (10 jobs: H1 seeds 20260903-06, H2 seeds 20260903-06, H2E seeds
20260901-02; budget 1000 evals each) so it survives Claude session shutdown.
Max 4 concurrent workers (~465 MB each). Owner of data/processed/_calib_cache/ this phase.

## Checklist

- [ ] 1. Journal created (this file)
- [ ] 2. Read src/calib_v2.py — find worker entry point / CLI used by completed runs
- [ ] 3. Inspect _calib_cache: checkpoints (dds_H1_20260901.part.npz etc.), logs format
- [ ] 4. Read watch_calib.py — log parsing contract (logs/<CELL>_<seed>.log, 'eval N/M best F')
- [ ] 5. Race check: tasklist for python3.10 heavyweights; target checkpoint names must not exist
- [ ] 6. Write docs/29_seed_expansion.md (pre-registration, BEFORE launch)
- [ ] 7. Write scripts/calib_queue_runner.py (queue, 4 slots, .err on crash, queue_runner.log heartbeat)
- [ ] 8. Detach via PowerShell Start-Process -WindowStyle Hidden python3.10; journal PID
- [ ] 9. Wait ~120 s; verify queue_runner.log + 4 workers >300 MB + 4 job logs + watch_calib.py lists new seeds
- [ ] 10. Return structured output (completed=true only if detached + verified + docs/29 written)

## Log

- Created journal. Next: read src/calib_v2.py and cache/log layout.
- Read src/calib_v2.py: CLI entry `_main()` — `python src/calib_v2.py --cell {H1,H2,H2E}
  --seed S --budget N --out data/processed/_calib_cache/dds_<CELL>_<SEED>.npz`.
  Checkpoint = out-file with `.part.npz` suffix, deleted on success. Resume replays
  checkpoints with an RNG assertion (dds() replay path). H2E reads H2's forcing cache
  (cache='H2'), so no new cache build needed; H1_* and H2_* cache .npy files all present.
- Read watch_calib.py: parses logs/*.log, header regex `^CELL seed N budget M`, eval regex
  `eval N/M best F`; workers counted from tasklist python3.10.exe >= 100 MB; errors from
  logs/*.err with nonzero size.
- Inspected _calib_cache: COMPLETED runs dds_H1_20260901.npz, dds_H1_20260902.npz,
  dds_H2_20260901.npz, dds_H2_20260902.npz (no .part.npz files remain — all 4 finished;
  logs end 'eval 1000/1000 ... DONE'). H1 20260901 final F 0.230232, 19.81 s/eval,
  330 min wall. Original launch via .bat: stdout+stderr 2>&1 into logs/<CELL>_<SEED>.log.
  I will keep that exact log redirect and additionally write logs/<CELL>_<SEED>.err on a
  nonzero exit (task spec), which watch_calib's *.err glob picks up.
- None of my 10 target output names (dds_H1_2026090{3..6}, dds_H2_2026090{3..6},
  dds_H2E_2026090{1,2}, or their .part.npz) exist on disk — verified in the ls above.
- python3.10 confirmed: Python 3.10.11 (WindowsApps shim). Next: race check via tasklist.
- RACE CHECK CLEAN: tasklist shows only 2 python3.10.exe at 2.9 MB and 8.7 MB (helpers,
  << 300 MB worker profile); no python.exe at all; no .part.npz anywhere; the only dds_*
  npz are the 4 completed runs. Safe to launch, no double-launch risk.
- Final F of completed runs (from DONE log lines): H1 0.230232 / 0.236772
  (mean 0.233502, spread 0.006540); H2 0.253365 / 0.234785 (mean 0.244075,
  spread 0.018580). Gap 0.010573 < 0.018580 — matches the task brief.
- Wrote docs/29_seed_expansion.md (pre-registration: 10 jobs, budget 1000, decision
  rules (a) pooled-6-seed separation test and (b) H2E kc_mult<1.85 on both seeds +
  recession median ratio <=1.5x + mean F within 0.01 of H2's, else refuted; reading
  instructions via nb14; RNG-verified checkpoint resume) BEFORE any launch.
- Wrote scripts/calib_queue_runner.py (10-job queue, max 4 concurrent, same CLI as the
  run_*.bat launches, stdout+stderr -> logs/<CELL>_<SEED>.log, crash -> logs/<name>.err
  + queue continues, heartbeat logs/queue_runner.log, skips jobs whose final npz exists).
  py_compile OK; calib_v2 CLI answers --help and accepts H2E.
- ABOUT TO DETACH the runner via PowerShell Start-Process -WindowStyle Hidden python3.10
  scripts\calib_queue_runner.py, workdir c:\dev\magdalena-mgb-sed. Expected: first wave
  = H1 seeds 20260903..20260906, ~19.8 s/eval, ~5.5 h/job, ~16.5 h total.
- DETACHED. Start-Process returned RUNNER_PID=26784. Now polling ~120-180 s for startup
  evidence (queue_runner.log START lines, 4 workers >300 MB, 4 job logs with headers).
- STARTUP VERIFIED (20:41-20:42):
  * logs/queue_runner.log: 'QUEUE START 10 jobs, max 4 concurrent, budget 1000' then
    START H1_20260903 pid 26428, H1_20260904 pid 14944, H1_20260905 pid 19500,
    H1_20260906 pid 36764 — the first 4 jobs, as required.
  * tasklist/Get-Process: 4 python3.10 workers at 456-457 MB each (matches the ~465 MB
    profile), runner 26784 at 26 MB, plus the 2 pre-existing tiny helpers.
  * All 4 new logs exist with the exact header watch_calib parses, e.g.
    'H1 seed 20260903 budget 1000  checkpoint dds_H1_20260903.part.npz'.
  * 'python3.10 watch_calib.py' ran clean: 'search workers alive: 4', lists all four new
    seeds ('no eval line yet' — expected, the first eval line prints at eval 26, i.e.
    ~8-9 min in at ~20 s/eval), errors: none. The 4 completed runs show 100% + STALE,
    which is correct (they finished ~16 h ago and are done).
- Known cosmetic quirks (no action needed): watch_calib prints a 'queue_runner: no eval
  line yet' row because queue_runner.log matches its logs/*.log glob; the completed runs
  carry a STALE flag by design.
- Checklist items 1-9 all done. Queue left RUNNING (that is the success condition).
  ETA ~16.5 h (3 waves x ~5.5 h): wave 2 = H2 20260903-06, wave 3 = H2E 20260901-02.
  When done: see docs/29_seed_expansion.md s4 for the reporting path. NOT committed to
  git (commit agent owns git). — calibration-launch agent, signing off 2026-08-03.
