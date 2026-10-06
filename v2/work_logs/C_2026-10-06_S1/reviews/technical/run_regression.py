"""One bounded Gate C regression unit; unchanged existing phase-two tests."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PLAN = HERE / "regression_plan.json"


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def main():
    plan = json.loads(PLAN.read_text())
    assert plan["attempt"] == 1
    assert plan["cwd"] == str(ROOT)
    assert platform.python_implementation() == "CPython"
    assert sys.version_info[:2] == (3, 12)
    import numpy
    assert numpy.__version__ == "2.3.5"
    command = [sys.executable, "-X", "faulthandler", "-m", "unittest", *plan["modules"], "-v"]
    assert command == plan["command"]
    env = os.environ.copy()
    env.update(plan["environment_overrides"])
    attempt = HERE / "regression_attempt1"
    attempt.mkdir(exist_ok=False)
    save(attempt / "start.json", {
        "started_utc": now(), "command": command, "cwd": str(ROOT),
        "plan_sha256": hashlib.sha256(PLAN.read_bytes()).hexdigest(),
        "source_manifest_sha256": hashlib.sha256((HERE / "source_manifest.json").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {k: env[k] for k in plan["environment_overrides"]},
        "python": sys.version, "executable": sys.executable,
        "numpy": numpy.__version__, "platform": platform.platform(),
        "timeout_seconds": plan["timeout_seconds"], "attempt": 1,
    })
    start = time.monotonic_ns()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    timed_out = False
    with (attempt / "stdout.txt").open("xb") as stdout, (attempt / "stderr.txt").open("xb") as stderr:
        process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        try:
            code = process.wait(timeout=plan["timeout_seconds"])
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            code = process.wait()
    end = time.monotonic_ns()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    text = (attempt / "stderr.txt").read_text(errors="replace")
    import re
    match = re.search(r"^Ran (\d+) tests? in ([0-9.]+)s$", text, re.MULTILINE)
    success = code == 0 and not timed_out and match is not None and text.rstrip().endswith("OK")
    result = {
        "attempt": 1, "ended_utc": now(), "exit_code": code, "timed_out": timed_out,
        "status": "PASS" if success else "FAILED_REQUIRES_DISPOSITION",
        "elapsed_ns": end-start, "wall_seconds": (end-start)/1e9,
        "user_cpu_seconds": after.ru_utime-before.ru_utime,
        "system_cpu_seconds": after.ru_stime-before.ru_stime,
        "max_rss_kib": after.ru_maxrss,
        "resource_scope": "RUSAGE_CHILDREN for waited regression process and its waited children; Linux ru_maxrss in KiB",
        "reported_tests": int(match.group(1)) if match else None,
        "reported_unittest_seconds": match.group(2) if match else None,
        "stdout_sha256": hashlib.sha256((attempt / "stdout.txt").read_bytes()).hexdigest(),
        "stderr_sha256": hashlib.sha256((attempt / "stderr.txt").read_bytes()).hexdigest(),
        "scientific_reexecution": False,
        "principal_engaged_minutes_credited_by_this_agent": 0,
    }
    save(attempt / "result.json", result)
    print(json.dumps(result, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
