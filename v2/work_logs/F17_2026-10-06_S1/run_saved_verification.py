"""Run one prospectively named, read-only F17 evidence check.

Contributor: ChatGPT (GPT-6 Astra Pro). No experimental stage is exposed.
Each label has one exclusive attempt directory; failures are preserved.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
COMMANDS = {
    "f14_freeze": ["-m", "v2.experiments.freeze", "verify"],
    "f15_saved": ["-m", "v2.experiments.summarize_f15", "--check"],
    "nd01_saved": ["-m", "v2.experiments.neural_diagnostic_v1.runner", "verify"],
    "nd01_summary": ["v2/experiments/F15_ND01_analysis/summarize.py", "--check"],
    "f17_tables": ["v2/reporting/build_f17_tables.py", "--check"],
}
THREADS = {
    "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1", "VECLIB_MAXIMUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1", "PYTHONHASHSEED": "0",
    "PYTHONDONTWRITEBYTECODE": "1",
}


def stamp():
    return {"utc": datetime.now(timezone.utc).isoformat(),
            "monotonic_ns": time.monotonic_ns()}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    label, = sys.argv[1:]
    command = [sys.executable, *COMMANDS[label]]
    plan = json.loads((HERE / "verification_plan.json").read_text())
    assert plan["commands"][label] == COMMANDS[label]
    target = HERE / "verification" / f"{label}_attempt1"
    target.mkdir(parents=True, exist_ok=False)
    start = stamp()
    record = {"label": label, "attempt": 1, "command": command,
              "cwd": str(REPO), "start": start, "environment": THREADS,
              "python": sys.version, "platform": platform.platform(),
              "runner_sha256": sha(Path(__file__).read_bytes()),
              "plan_sha256": sha((HERE / "verification_plan.json").read_bytes()),
              "scope": "Saved-data verification only; no new scientific exposure."}
    (target / "start.json").write_text(json.dumps(record, indent=2) + "\n")
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    stdout = stderr = b""
    code = None
    error = None
    try:
        result = subprocess.run(command, cwd=REPO, env={**os.environ, **THREADS},
                                capture_output=True, timeout=180)
        stdout, stderr, code = result.stdout, result.stderr, result.returncode
    except Exception:
        error = traceback.format_exc()
        stderr = error.encode()
    end = stamp()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    (target / "stdout.txt").write_bytes(stdout)
    (target / "stderr.txt").write_bytes(stderr)
    final = {**record, "end": end, "exit_code": code, "exception": error,
             "status": "pass" if code == 0 else "failure",
             "wall_ns": end["monotonic_ns"] - start["monotonic_ns"],
             "child_user_cpu_seconds": after.ru_utime - before.ru_utime,
             "child_system_cpu_seconds": after.ru_stime - before.ru_stime,
             "child_max_rss_kib": after.ru_maxrss,
             "stdout_sha256": sha(stdout), "stderr_sha256": sha(stderr)}
    (target / "result.json").write_text(json.dumps(final, indent=2) + "\n")
    print(json.dumps({k: final[k] for k in ["label", "attempt", "status", "exit_code", "wall_ns"]}))
    if code != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
