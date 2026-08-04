#!/usr/bin/env python
"""Monitor the nb14 DDS calibration workers.

    python watch_calib.py            one snapshot
    python watch_calib.py -w         refresh every 30 s until all workers exit
    python watch_calib.py -w 10      refresh every 10 s

Reads only; never writes to the repo. Rate and ETA come from each log's own
creation-to-last-write span, so they are per worker and need no prior state.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import time

REPO = pathlib.Path(r"c:\dev\magdalena-mgb-sed")
CACHE = REPO / "data" / "processed" / "_calib_cache"
LOGS = CACHE / "logs"
STATE = pathlib.Path(tempfile.gettempdir()) / "watch_calib_state.json"

HEAD = re.compile(r"^(?P<cell>\S+)\s+seed\s+(?P<seed>\d+)\s+budget\s+(?P<budget>\d+)")
EVAL = re.compile(r"eval\s+(?P<n>\d+)\s*/\s*(?P<m>\d+)\s+best\s+(?P<f>[-\d.]+)")
WORKER_MIN_MB = 100          # below this it is a helper, not a search worker

# fixed reference points, docs/18 §5 and sim_calibrated/calibration.json
REFS = (("prior", 0.1276), ("random null", 0.1729), ("Config B", 0.2429))


try:                                     # block glyphs where the console allows them
    "█░".encode(sys.stdout.encoding or "utf-8")
    FULL, EMPTY = "█", "░"
except Exception:
    FULL, EMPTY = "#", "-"


def bar(frac: float, width: int = 34) -> str:
    frac = min(max(frac, 0.0), 1.0)
    filled = int(round(frac * width))
    return f"[{FULL * filled}{EMPTY * (width - filled)}]"


def workers() -> list[tuple[int, float]]:
    """(pid, resident MB) for every python3.10.exe above WORKER_MIN_MB."""
    try:
        out = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH", "/FI", "IMAGENAME eq python3.10.exe"],
            capture_output=True, text=True, timeout=20,
        ).stdout
    except Exception:
        return []
    found = []
    for line in out.splitlines():
        parts = [p.strip('"') for p in line.split('","')]
        if len(parts) < 5:
            continue
        try:
            pid = int(parts[1])
            mb = int(re.sub(r"\D", "", parts[4])) / 1024.0
        except ValueError:
            continue
        if mb >= WORKER_MIN_MB:
            found.append((pid, mb))
    return sorted(found)


def fmt_eta(seconds: float) -> str:
    if seconds <= 0 or seconds != seconds:
        return "--"
    end = time.localtime(time.time() + seconds)
    h, m = divmod(int(seconds // 60), 60)
    return f"{h}h{m:02d}m  (~{time.strftime('%H:%M', end)})"


def snapshot() -> bool:
    """Print one status block. Returns True while search workers are alive."""
    live = workers()
    now = time.strftime("%H:%M:%S")
    print(f"\n=== {now}   search workers alive: {len(live)} ===")

    if not LOGS.is_dir():
        print(f"  no log directory at {LOGS}")
        return bool(live)

    try:
        old = json.loads(STATE.read_text())
    except Exception:
        old = {}
    new: dict[str, dict] = {}

    rows, slowest_eta = [], 0.0
    done_evals = total_evals = 0
    for log in sorted(LOGS.glob("*.log")):
        text = log.read_text(errors="replace").splitlines()
        head = next((HEAD.match(l) for l in text if HEAD.match(l)), None)
        evals = [EVAL.search(l) for l in text]
        last = next((m for m in reversed(evals) if m), None)
        if last is None:
            print(f"  {log.stem}: no eval line yet")
            continue

        n, m, best = int(last["n"]), int(last["m"]), float(last["f"])
        st = log.stat()
        stale = time.time() - st.st_mtime

        # Rate from the delta since the PREVIOUS run of this script. st_ctime is
        # unusable here: the logs were created by an earlier racing launch batch
        # and only appended to by the surviving one, so ctime->mtime overstates
        # the span and understates the rate.
        prev = old.get(log.stem)
        per = src = None
        if prev and prev["n"] < n:
            per = (st.st_mtime - prev["t"]) / (n - prev["n"])
            src = "measured"
        elif prev and prev["n"] == n:
            per, src = prev.get("per"), "carried"
        if per is None:                                       # first ever run
            per = max(st.st_mtime - st.st_ctime, 1e-9) / max(n, 1)
            src = "ctime est"
        new[log.stem] = {"n": n, "m": m, "t": st.st_mtime, "per": per, "best": best}
        slowest_eta = max(slowest_eta, per * (m - n))

        tag = f"{head['cell']} {head['seed']}" if head else log.stem
        flag = "" if stale < 900 else "  <-- STALE, check .err"
        rows.append((tag, n, m,
                     f"F {best:.5f}  {per:4.1f}s/ev {src[:4]}"
                     f"  upd {stale / 60:4.1f}m{flag}"))
        done_evals += n
        total_evals += m

    w = max((len(r[0]) for r in rows), default=8)
    for tag, n, m, tail in rows:
        print(f"  {tag:<{w}}  {bar(n / m)} {100 * n / m:5.1f}%  {n:>4}/{m}  {tail}")

    if total_evals:
        print(f"  {'OVERALL':<{w}}  {bar(done_evals / total_evals)} "
              f"{100 * done_evals / total_evals:5.1f}%  {done_evals:>4}/{total_evals}"
              f"  ETA {fmt_eta(slowest_eta) if live else '--'}")

    # errors
    errs = [(p.name, p.stat().st_size) for p in LOGS.glob("*.err") if p.stat().st_size]
    print("  errors: " + ("none" if not errs
                          else ", ".join(f"{n} ({s} B)" for n, s in errs)))

    # best-so-far against the fixed reference points
    bests = [v["best"] for v in new.values() if "best" in v]
    if bests:
        scale = "  ".join(f"{lbl} {val:.4f}" for lbl, val in REFS)
        print(f"  best any cell: {max(bests):.5f}   |   {scale}")
        spread = max(bests) - min(bests)
        print(f"  spread across all four cells: {spread:.4f}"
              + ("   <- larger than any cell difference; nothing separable yet"
                 if spread > 0.02 else "   <- cells now separable, compare H2 vs H1"))

    try:
        STATE.write_text(json.dumps(new, indent=1))
    except Exception as exc:
        print(f"  (could not persist rate state: {exc})")

    if not live:
        incomplete = [k for k, v in new.items() if v.get("n", 0) < v.get("m", 1)]
        print("  NO WORKERS RUNNING — " + ("all budgets complete."
              if not incomplete else
              f"budgets NOT complete ({', '.join(incomplete)}) — they stopped "
              "early; check the .err files before trusting anything."))
        print("  next step:  python -m nbconvert --to notebook --execute --inplace "
              "--ExecutePreprocessor.timeout=-1 notebooks/14_calibration.ipynb")
    return bool(live)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--watch", nargs="?", type=int, const=30, default=None,
                    metavar="SEC", help="refresh every SEC seconds (default 30)")
    a = ap.parse_args()
    if a.watch is None:
        snapshot()
        return 0
    try:
        while snapshot():
            time.sleep(a.watch)
    except KeyboardInterrupt:
        print("\nstopped watching (the workers are unaffected)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
