"""F15 external process recorder; does not alter frozen experimental code.

Contributor: ChatGPT (GPT-6 Astra Pro), October 4/5, 2026.
Usage: python <this file> LABEL -- COMMAND [ARG ...]
Writes exclusive start/end records and separate stdout/stderr, preserving
native return codes even when the experiment cannot catch an exception.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def save(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def main():
    label, separator, *command = sys.argv[1:]
    assert separator == "--" and command
    folder = Path(__file__).resolve().parent / "commands"
    folder.mkdir(exist_ok=True)
    start = {
        "schema": "F15-external-command-v1",
        "label": label,
        "command": command,
        "cwd": str(Path.cwd()),
        "started_utc": utc(),
        "started_monotonic_ns": time.monotonic_ns(),
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "thread_environment": {key: os.environ.get(key) for key in
                               ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")},
    }
    save(folder / f"{label}.start.json", start)
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    wall = time.perf_counter()
    with (folder / f"{label}.stdout.log").open("xb") as stdout, \
            (folder / f"{label}.stderr.log").open("xb") as stderr:
        result = subprocess.run(command, stdout=stdout, stderr=stderr, check=False)
        for handle in (stdout, stderr):
            handle.flush()
            os.fsync(handle.fileno())
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    end = dict(start, completed_utc=utc(), completed_monotonic_ns=time.monotonic_ns(),
               returncode=result.returncode, observed_wall_seconds=time.perf_counter()-wall,
               child_user_cpu_seconds=after.ru_utime-before.ru_utime,
               child_system_cpu_seconds=after.ru_stime-before.ru_stime,
               child_max_rss_kib=after.ru_maxrss,
               stdout_sha256=hashlib.sha256((folder / f"{label}.stdout.log").read_bytes()).hexdigest(),
               stderr_sha256=hashlib.sha256((folder / f"{label}.stderr.log").read_bytes()).hexdigest())
    save(folder / f"{label}.end.json", end)
    print(json.dumps(end, indent=2))
    raise SystemExit(result.returncode if result.returncode >= 0 else 128-result.returncode)


if __name__ == "__main__":
    main()
