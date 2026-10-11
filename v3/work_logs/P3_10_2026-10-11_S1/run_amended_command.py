"""Record a source-bound P3-10-A1 command and its process observations.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
This wrapper supplies no inputs or scientific parameters and has no retry mode.
The amendment driver owns its lineage; the original failed root is preserved.
"""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import shlex
import subprocess
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def stamp():
    return {"utc": datetime.now(timezone.utc).isoformat(),
            "monotonic_ns": time.monotonic_ns(),
            "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip()}


def publish(path, value):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("public", "evaluation", "analysis"))
    args = parser.parse_args()
    target = HERE / "commands" / "P3-10-A1" / args.stage
    target.mkdir(parents=True, exist_ok=False)
    command = ["python3", "-E", "-S", "-B", "-X",
               "pycache_prefix=/dev/null/value_logic_p309",
               "v3/experiments/amendments/P3_10_A1/continue.py", "--task", "P3-10",
               "--stage", args.stage]
    before = stamp()
    publish(target / "start.json", {
        "schema": "value_logic.p310.command_start.v1", "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "command": command, "shell_display": shlex.join(command), "cwd": str(REPO),
        "observed": before, "attempt_role": "initial explicit P3-10-A1 amendment; no infrastructure retry",
        "driver_sha256": hashlib.sha256((REPO / command[6]).read_bytes()).hexdigest()})
    with (target / "stdout.json").open("xb") as stdout, (target / "stderr.txt").open("xb") as stderr:
        process = subprocess.run(command, cwd=REPO, stdout=stdout, stderr=stderr)
        stdout.flush()
        stderr.flush()
        os.fsync(stdout.fileno())
        os.fsync(stderr.fileno())
    after = stamp()
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    record = {
        "schema": "value_logic.p310.command_completion.v1", "command": command,
        "start": before, "end": after, "returncode": process.returncode,
        "wall_ns": after["monotonic_ns"] - before["monotonic_ns"],
        "child_user_cpu_seconds": usage.ru_utime, "child_system_cpu_seconds": usage.ru_stime,
        "child_peak_rss_kib": usage.ru_maxrss,
        "resource_scope": "Outer child process including verification and orchestration; not a paid service tariff or principal research credit.",
        "stdout_bytes": (target / "stdout.json").stat().st_size,
        "stdout_sha256": hashlib.sha256((target / "stdout.json").read_bytes()).hexdigest(),
        "stderr_bytes": (target / "stderr.txt").stat().st_size,
        "stderr_sha256": hashlib.sha256((target / "stderr.txt").read_bytes()).hexdigest()}
    publish(target / "completion.json", record)
    print(json.dumps(record, indent=2), flush=True)
    if process.returncode == 0:
        result = json.loads((target / "stdout.json").read_text())
        print(json.dumps({k: v for k, v in result.items() if k != "completion"}, indent=2), flush=True)
    raise SystemExit(process.returncode)


if __name__ == "__main__":
    main()
