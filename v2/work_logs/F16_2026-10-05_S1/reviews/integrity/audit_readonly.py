"""Bounded saved-byte F16 integrity review. No scientific run is launched.

Contributor: ChatGPT (GPT-6 Astra Pro), delegated F16 integrity reviewer.
All writes stay inside this review directory. The only experiment-module
commands are the two documented read-only verify entry points.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
BASE = "6ef27f20e3ac0920953a27dd84d6c91a021ba58f"
SCOPES = [
    "v2/experiments",
    "v2/work_logs/F15_v1_run1",
    "v2/work_logs/F15_ND01_v1_run1",
    "v2/work_logs/F15_2026-10-04_S1",
    "v2/work_logs/F15_ND01_2026-10-05_S1",
    "v2/work_logs/F15_2026-10-04_S1.md",
    "v2/work_logs/F15_ND01_2026-10-05_S1.md",
]
RUNS = SCOPES[1:3]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def save(name, data):
    path = HERE / name
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def command(label, argv, *, extra_environment=None):
    environment = os.environ.copy()
    environment.update(extra_environment or {})
    record = {"label": label, "argv": argv, "cwd": str(ROOT),
              "started_utc": utc(), "attempt": 1,
              "extra_environment": extra_environment or {},
              "scientific_execution": False}
    save(label + ".start.json", record)
    started = time.monotonic()
    with (HERE / (label + ".stdout.log")).open("xb") as out:
        with (HERE / (label + ".stderr.log")).open("xb") as err:
            result = subprocess.run(argv, cwd=ROOT, env=environment,
                                    stdout=out, stderr=err, check=False)
    record.update({"ended_utc": utc(), "wall_seconds": time.monotonic() - started,
                   "returncode": result.returncode})
    for stream in ("stdout", "stderr"):
        raw = (HERE / (label + "." + stream + ".log")).read_bytes()
        record[stream + "_bytes"] = len(raw)
        record[stream + "_sha256"] = hashlib.sha256(raw).hexdigest()
    save(label + ".end.json", record)
    print(json.dumps(record), flush=True)
    return record


def inventory():
    tree = subprocess.run(["git", "ls-tree", "-r", "-z", BASE, "--", *SCOPES],
                          cwd=ROOT, stdout=subprocess.PIPE, check=True).stdout
    old = {}
    for entry in tree.split(b"\0"):
        if entry:
            metadata, name = entry.split(b"\t", 1)
            old[name.decode()] = metadata.decode().split()[2]
    paths = set(old)
    for scope in SCOPES:
        base = ROOT / scope
        if base.is_file():
            paths.add(scope)
        elif base.is_dir():
            paths.update(p.relative_to(ROOT).as_posix() for p in base.rglob("*")
                         if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    items = []
    for name in sorted(paths):
        path = ROOT / name
        if not path.is_file():
            items.append({"path": name, "status": "missing_from_worktree", "base_blob": old.get(name)})
            continue
        raw = path.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        status = "same_as_base" if blob == old.get(name) else ("changed_since_base" if name in old else "new_since_base")
        items.append({"path": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                      "git_blob": blob, "base_blob": old.get(name), "status": status})
    return {"observed_utc": utc(), "base": BASE, "scope": SCOPES, "files": items,
            "count": len(items), "differences": [item for item in items if item["status"] != "same_as_base"]}


def registrations():
    results = []
    for name in ["v2/experiments/freeze.v1.json", "v2/experiments/neural_diagnostic_v1/freeze.json"]:
        manifest = read(name)
        files = manifest["files"]
        entries = ([{"path": p, **value} for p, value in files.items()]
                   if isinstance(files, dict) else files)
        checked = []
        for entry in [*entries, *manifest.get("source_prepared", [])]:
            path = ROOT / entry["path"]
            checked.append({**entry, "actual_sha256": digest(entry["path"]),
                            "actual_bytes": path.stat().st_size,
                            "matches": digest(entry["path"]) == entry["sha256"] and path.stat().st_size == entry["bytes"]})
        results.append({"manifest": name, "sha256": digest(name), "files_count": len(entries),
                        "source_prepared_count": len(manifest.get("source_prepared", [])),
                        "derivation09_member": any(e["path"] == "v2/derivations/09_c4_price_revision.md" for e in entries),
                        "markdown_members": [e["path"] for e in entries if e["path"].endswith(".md")],
                        "checks": checked, "all_registered_bytes_match": all(c["matches"] for c in checked)})
    return results


def sidecars_and_markers():
    results = []
    for name in RUNS:
        folder = ROOT / name
        checks = []
        for sidecar in sorted(folder.rglob("*.sha256")):
            target = Path(str(sidecar)[:-7])
            expected = sidecar.read_text().strip()
            raw = target.read_bytes()
            actual = hashlib.sha256(raw).hexdigest()
            checks.append({"path": target.relative_to(ROOT).as_posix(), "bytes": len(raw),
                           "expected_sha256": expected, "actual_sha256": actual, "matches": expected == actual})
        markers = []
        for path in sorted(folder.rglob("*.json")):
            if path.name in {"start.json", "complete.json", "preparation_complete.json", "evaluation_complete.json",
                             "evaluation_start.json", "evaluation_exposure.json", "pre_evaluation_validation.json"}:
                value = json.loads(path.read_text())
                scalar = {k: v for k, v in value.items() if not isinstance(v, (dict, list))}
                markers.append({"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path.relative_to(ROOT)),
                                "fields": scalar})
        results.append({"run": name, "attempt_directories": sorted(p.name for p in folder.iterdir() if p.is_dir()),
                        "sidecar_count": len(checks), "matching_sidecars": sum(c["matches"] for c in checks),
                        "sidecar_exceptions": [c for c in checks if not c["matches"]], "markers": markers})
    return results


def saved_report_hashes():
    result = {"reports": [], "input_registrations": []}
    for name in ["v2/experiments/results.md", "v2/experiments/F15_ND01_results.md"]:
        raw = subprocess.run(["git", "show", f"{BASE}:{name}"], cwd=ROOT,
                             stdout=subprocess.PIPE, check=True).stdout
        result["reports"].append({"path": name, "current_sha256": digest(name),
                                  "base_sha256": hashlib.sha256(raw).hexdigest(),
                                  "byte_identical_to_base": raw == (ROOT / name).read_bytes()})
    f15 = "v2/experiments/F15_v1_analysis/"
    for entry in read(f15 + "input_manifest.json")["files"]:
        result["input_registrations"].append({"registry": f15 + "input_manifest.json", "path": entry["file"],
                                               "expected_sha256": entry["sha256"], "actual_sha256": digest(entry["file"]),
                                               "matches": digest(entry["file"]) == entry["sha256"]})
    for name, entry in read(f15 + "output_manifest.json")["files"].items():
        result["input_registrations"].append({"registry": f15 + "output_manifest.json", "path": f15 + name,
                                               "expected_sha256": entry["sha256"], "actual_sha256": digest(f15 + name),
                                               "matches": digest(f15 + name) == entry["sha256"]})
    for audit in ["audit_final_report.json", "audit_report_addendum.json"]:
        path = "v2/work_logs/F15_ND01_2026-10-05_S1/" + audit
        value = read(path)
        result.setdefault("historical_report_snapshots", []).append({"audit": path,
            "recorded_report_sha256": value["report_sha256"],
            "matches_current_report": value["report_sha256"] == digest("v2/experiments/F15_ND01_results.md")})
        for name, expected in value["inputs"].items():
            result["input_registrations"].append({"registry": path, "path": name,
                                                 "expected_sha256": expected, "actual_sha256": digest(name),
                                                 "matches": digest(name) == expected})
        for name, expected in value.get("historical_report_audit_preserved", {}).items():
            result["input_registrations"].append({"registry": path, "path": name,
                                                 "expected_sha256": expected, "actual_sha256": digest(name),
                                                 "matches": digest(name) == expected})
    result["registration_exceptions"] = [c for c in result["input_registrations"] if not c["matches"]]
    return result


def main():
    started = utc()
    save("inventory_before.json", inventory())
    command("f14_verify_attempt1", [sys.executable, "-m", "v2.experiments.freeze", "verify"],
            extra_environment={"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1"})
    command("nd01_verify_attempt1", [sys.executable, "-m", "v2.experiments.neural_diagnostic_v1.runner", "verify"],
            extra_environment={"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1"})
    after = inventory()
    save("inventory_after.json", after)
    before = json.loads((HERE / "inventory_before.json").read_text())
    result = {"contributor": "ChatGPT (GPT-6 Astra Pro), delegated F16 integrity reviewer",
              "started_utc": started, "finished_utc": utc(), "source_base": BASE,
              "head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip(),
              "registered_freezes": registrations(), "runs": sidecars_and_markers(), "reports": saved_report_hashes(),
              "inventory_files": after["count"], "differences_from_base": after["differences"],
              "scientific_artifact_inventory_unchanged_during_review": before["files"] == after["files"],
              "principal_minutes_added": 0, "scientific_commands_performed": [], "experiment_reruns": 0,
              "limits": "Saved bytes and markers can establish local recorded continuity, not rule out unrecorded or deleted execution elsewhere."}
    save("integrity_result.json", result)
    print(json.dumps({"inventory_files": result["inventory_files"], "base_differences": len(result["differences_from_base"]),
                      "unchanged_during_review": result["scientific_artifact_inventory_unchanged_during_review"],
                      "report_registration_exceptions": result["reports"]["registration_exceptions"],
                      "sidecar_exceptions": [r["sidecar_exceptions"] for r in result["runs"]]}, indent=2))


if __name__ == "__main__":
    main()
