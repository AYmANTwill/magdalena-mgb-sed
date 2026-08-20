"""Detached queue runner for the pre-registered calibration job lists.

Runs a pre-registered job list - a table fixed in a frozen document BEFORE any of its
numbers exist - with AT MOST `MAX_CONCURRENT` workers: each worker holds ~465 MB
resident and the machine cannot take more than four. Jobs are fed to free slots in
table order.

Two queues are registered, and the runner takes the queue name as its only argument
(default: the active one, `c2b`):

    docs29  the seed expansion of docs/29_seed_expansion.md - COMPLETE, all 10 final
            .npz on disk, `logs/queue_runner.log` ends
            "2026-08-05 02:26:49  QUEUE COMPLETE  ok 10  crashed 0  skipped 0".
            Kept verbatim rather than deleted so the list that produced the adopted
            H2E can still be read off the runner that ran it.
    c2b     the docs/33 §3.3 refit: cell H2E-S (H2E + the C2b peak signature term),
            seeds 20260907 and 20260908, budget 1000. docs/33 §3.3 authorises this
            cell and no other - no third seed, no budget change.

Each job is the SAME CLI entry point the four completed runs used:

    python src/calib_v2.py --cell <CELL> --seed <SEED> --budget 1000
        --out data/processed/_calib_cache/dds_<CELL>_<SEED>.npz

with stdout+stderr into data/processed/_calib_cache/logs/<CELL>_<SEED>.log, exactly
like the original run_*.bat launches, so watch_calib.py parses the logs unchanged.

Failure handling: a job that exits nonzero gets logs/<CELL>_<SEED>.err (exit code +
log tail) and the queue CONTINUES. Idempotent: a job whose final .npz already exists
is skipped (the completed 20260901/02 runs are protected by this as well as by not
being in the list); a re-launched job resumes from its .part.npz checkpoint, which
calib_v2.dds replays with an RNG assertion.

Launch DETACHED (shell '&' does not survive session close on this box):

    Start-Process -WindowStyle Hidden python3.10 `
        -ArgumentList 'scripts\\calib_queue_runner.py','c2b' `
        -WorkingDirectory 'c:\\dev\\magdalena-mgb-sed'
"""
from __future__ import annotations

import pathlib
import subprocess
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[2]   # scripts/b/ -> scripts/ -> repo root
CACHE = REPO / 'data' / 'processed' / '_calib_cache'
LOGS = CACHE / 'logs'
WORKER = REPO / 'src' / 'calib_v2.py'

BUDGET = 1000                 # identical to the completed runs, for comparability
MAX_CONCURRENT = 4            # ~465 MB per worker; the box cannot take more
POLL_SECONDS = 20
ERR_TAIL_LINES = 40
CREATE_NO_WINDOW = 0x08000000  # workers must not pop console windows when detached

# The pre-registered queues, in launch order. Do not edit either one mid-run.
QUEUES: dict[str, list[tuple[str, int]]] = {
    # docs/29 §2 - COMPLETE 2026-08-05 (ok 10, crashed 0). Left here as the record.
    'docs29': [
        ('H1', 20260903), ('H1', 20260904), ('H1', 20260905), ('H1', 20260906),
        ('H2', 20260903), ('H2', 20260904), ('H2', 20260905), ('H2', 20260906),
        ('H2E', 20260901), ('H2E', 20260902),
    ],
    # docs/33 §3.3 - the C2b refit. Two seeds, verified unused: _calib_cache holds
    # 20260901-06 for H1/H2 and 20260901-02 for H2E, and nothing at all for H2E-S.
    'c2b': [
        ('H2E-S', 20260907), ('H2E-S', 20260908),
    ],
}
DEFAULT_QUEUE = 'c2b'


def stamp() -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S')


class Heartbeat:
    """Append-only queue log: one line per queue event, flushed immediately."""

    def __init__(self, path: pathlib.Path):
        self.fh = open(path, 'a', encoding='utf-8')

    def line(self, msg: str) -> None:
        self.fh.write(f'{stamp()}  {msg}\n')
        self.fh.flush()


def job_paths(cell: str, seed: int) -> dict[str, pathlib.Path]:
    name = f'{cell}_{seed}'
    return dict(
        out=CACHE / f'dds_{name}.npz',
        log=LOGS / f'{name}.log',
        err=LOGS / f'{name}.err',
    )


def launch(cell: str, seed: int) -> subprocess.Popen:
    p = job_paths(cell, seed)
    cmd = [sys.executable, str(WORKER), '--cell', cell, '--seed', str(seed),
           '--budget', str(BUDGET), '--out', str(p['out'])]
    log_fh = open(p['log'], 'a', encoding='utf-8')   # append: a resume keeps history
    return subprocess.Popen(cmd, cwd=str(REPO), stdout=log_fh,
                            stderr=subprocess.STDOUT,
                            creationflags=CREATE_NO_WINDOW)


def record_crash(cell: str, seed: int, code: int) -> pathlib.Path:
    p = job_paths(cell, seed)
    try:
        tail = p['log'].read_text(encoding='utf-8', errors='replace').splitlines()
        tail_txt = '\n'.join(tail[-ERR_TAIL_LINES:])
    except OSError as exc:
        tail_txt = f'(log unreadable: {exc})'
    p['err'].write_text(
        f'{stamp()}  {cell} seed {seed} exited with code {code}\n'
        f'checkpoint {p["out"].with_suffix("").name}.part.npz is kept; re-running the '
        f'same job resumes it (RNG-verified replay).\n\n'
        f'--- last {ERR_TAIL_LINES} log lines ---\n{tail_txt}\n',
        encoding='utf-8')
    return p['err']


def main() -> int:
    qname = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUEUE
    if qname not in QUEUES:
        print(f'unknown queue {qname!r}; known: {", ".join(sorted(QUEUES))}')
        return 2
    jobs = QUEUES[qname]

    LOGS.mkdir(parents=True, exist_ok=True)
    hb = Heartbeat(LOGS / 'queue_runner.log')
    hb.line(f'QUEUE START  queue {qname}  {len(jobs)} jobs '
            f'({", ".join(f"{c}_{s}" for c, s in jobs)}), max {MAX_CONCURRENT} '
            f'concurrent, budget {BUDGET}, python {sys.executable}')

    pending = list(jobs)
    running: dict[str, tuple[subprocess.Popen, str, int, float]] = {}
    n_ok = n_crashed = n_skipped = 0
    launched = 0

    while pending or running:
        # reap finished workers
        for name in list(running):
            proc, cell, seed, t0 = running[name]
            code = proc.poll()
            if code is None:
                continue
            del running[name]
            mins = (time.time() - t0) / 60.0
            if code == 0:
                n_ok += 1
                hb.line(f'DONE  {name}  exit 0  wall {mins:.1f} min')
            else:
                n_crashed += 1
                err = record_crash(cell, seed, code)
                hb.line(f'CRASH {name}  exit {code}  wall {mins:.1f} min  '
                        f'-> {err.name}  (queue continues)')

        # feed free slots
        while pending and len(running) < MAX_CONCURRENT:
            cell, seed = pending.pop(0)
            name = f'{cell}_{seed}'
            if job_paths(cell, seed)['out'].exists():
                n_skipped += 1
                hb.line(f'SKIP  {name}  final npz already on disk')
                continue
            proc = launch(cell, seed)
            launched += 1
            running[name] = (proc, cell, seed, time.time())
            hb.line(f'START {name}  pid {proc.pid}  '
                    f'({launched + n_skipped}/{len(jobs)}, slot {len(running)})')

        if running:
            time.sleep(POLL_SECONDS)

    hb.line(f'QUEUE COMPLETE  queue {qname}  ok {n_ok}  crashed {n_crashed}  '
            f'skipped {n_skipped}')
    return 0 if n_crashed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
