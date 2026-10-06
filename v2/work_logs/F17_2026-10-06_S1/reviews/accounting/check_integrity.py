"""Independent read-only F17 entry-integrity and open-clock inspection.

Contributor: ChatGPT (GPT-6 Astra Pro), same-model delegated review.
Writes only its exclusive result beside this script. No ledger append,
experimental import, training, evaluation, test or accounting serializer run.
"""
from collections import Counter
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import subprocess
import time


HERE = Path(__file__).resolve().parent
SESSION = HERE.parents[1]
REPO = SESSION.parents[2]
OUT = HERE / "integrity_result.json"
EXPECTED_LEDGER_SHA = "94c1b965f9ec1b9245ea65419c9d521e7c2712dc2eb4387125119426a508992d"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def check_entries(entries):
    checks = []
    for expected in entries:
        path = REPO / expected["path"]
        raw = path.read_bytes()
        checks.append({"path": expected["path"], "expected_sha256": expected["sha256"],
                       "actual_sha256": digest(raw), "expected_bytes": expected["bytes"],
                       "actual_bytes": len(raw), "matches": len(raw) == expected["bytes"] and digest(raw) == expected["sha256"]})
    return checks


def main():
    if OUT.exists():
        raise FileExistsError("Preserve this review result; do not overwrite it.")
    started = datetime.now(timezone.utc).isoformat()
    tick = time.monotonic_ns()
    names = ["baseline.json", "forecast.json", "entry_inventory.json", "clocks.jsonl",
             "segments.jsonl", "exclusions.jsonl", "clock_state.json", "clock.py", "close_accounting.py"]
    raw = {name: (SESSION / name).read_bytes() for name in names}
    source_bindings = [{"path": (SESSION / name).relative_to(REPO).as_posix(),
                        "bytes": len(data), "sha256": digest(data)} for name, data in raw.items()]
    baseline = json.loads(raw["baseline.json"])
    forecast = json.loads(raw["forecast.json"])
    entry = json.loads(raw["entry_inventory.json"])
    ledger = (REPO / "v2/time_ledger.csv").read_bytes()
    csv_rows = list(csv.DictReader(io.StringIO(ledger.decode())))
    ledger_ok = (len(ledger) == baseline["ledger_bytes"] == 269074
                 and digest(ledger) == baseline["ledger_sha256"] == EXPECTED_LEDGER_SHA
                 and len(csv_rows) == baseline["ledger_rows"] == 1105
                 and not any(r["task_id"] == "F17" or r["attempt_id"] == "F17-A1" for r in csv_rows))
    tree_command = ["git", "ls-tree", "-r", "--name-only", baseline["head"]]
    tree = subprocess.run(tree_command, cwd=REPO, capture_output=True, text=True, check=True)
    tracked_python = sorted(p for p in tree.stdout.splitlines() if p.endswith(".py"))
    python_entry = sorted((r for r in entry if r["path"].endswith(".py")), key=lambda r: r["path"])
    python_paths_ok = [r["path"] for r in python_entry] == tracked_python
    python_checks = check_entries(python_entry)
    old_inventory_path = "v2/work_logs/F16_2026-10-05_S1/reviews/integrity/inventory_before.json"
    old_inventory_raw = (REPO / old_inventory_path).read_bytes()
    old_inventory = json.loads(old_inventory_raw)
    scientific_checks = check_entries(old_inventory["files"])
    prior_integrity_path = "v2/work_logs/F16_2026-10-05_S1/reviews/integrity/integrity_result.json"
    prior_integrity_raw = (REPO / prior_integrity_path).read_bytes()
    prior_integrity = json.loads(prior_integrity_raw)
    run_checks = []
    for old_run in prior_integrity["runs"]:
        actual = sorted(path.name for path in (REPO / old_run["run"]).iterdir() if path.is_dir())
        run_checks.append({"path": old_run["run"], "expected_directories": old_run["attempt_directories"],
                           "actual_directories": actual, "matches": actual == old_run["attempt_directories"]})
    freeze_checks = []
    for path, expected_sha in (
        ("v2/experiments/freeze.v1.json", "b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c"),
        ("v2/experiments/neural_diagnostic_v1/freeze.json", "9c15af55b83d7edf134542a9c70bcc0f087c6f4f6491f993361a27493b5cf24c"),
    ):
        manifest_raw = (REPO / path).read_bytes()
        manifest = json.loads(manifest_raw)
        registered = manifest["files"]
        if isinstance(registered, dict):
            registered = [{"path": name, **entry} for name, entry in registered.items()]
        dependencies = check_entries(registered + manifest.get("source_prepared", []))
        freeze_checks.append({"path": path, "sha256": digest(manifest_raw),
                              "manifest_matches": digest(manifest_raw) == expected_sha,
                              "registered_files": len(manifest["files"]), "source_preparations": len(manifest.get("source_prepared", [])),
                              "dependencies_all_match": all(r["matches"] for r in dependencies), "checks": dependencies})
    previous_actuals_path = "v2/work_logs/C_2026-10-06_S1/actuals.json"
    previous_actuals_raw = (REPO / previous_actuals_path).read_bytes()
    previous_actuals = json.loads(previous_actuals_raw)
    entry_ok = (forecast["post_b_1_entry_minutes"] == previous_actuals["post_b_1"]["close_minutes_decimal"]
                == "932.46514142531666666666666666666666666666666666667"
                and forecast["remaining_to_16h_minutes"] == previous_actuals["post_b_1"]["remaining_minutes_decimal"])
    events, segments, exclusions = ([json.loads(line) for line in raw[name].decode().splitlines()]
                                    for name in ("clocks.jsonl", "segments.jsonl", "exclusions.jsonl"))
    transitions = [e for e in events if e["command"] != "check"]
    observed = {e["monotonic_ns"]: e["utc"] for e in events}
    assert events[0]["command"] == "start" and len(observed) == len(events)
    assert all(e["runtime"] == "linux-F17-S1" for e in events)
    assert all(a["monotonic_ns"] < b["monotonic_ns"] for a, b in zip(events, events[1:]))
    assert len(segments) == len(transitions) - 1
    categories = Counter()
    lane_ns = Counter()
    for segment, a, b in zip(segments, transitions, transitions[1:]):
        left, right = segment["start_monotonic_ns"], segment["end_monotonic_ns"]
        assert left == a["monotonic_ns"] and right == b["monotonic_ns"]
        assert segment["start_utc"] == a["utc"] and segment["end_utc"] == b["utc"]
        assert segment["elapsed_ns"] == right - left > 0
        assert segment["mode"] == a["args"][0]
        expected_lane = "" if a["command"] == "pause" or a["args"][1] == "-" else a["args"][1]
        assert segment["lane"] == expected_lane
        cut_ns = 0
        for exclusion in exclusions:
            el, er = exclusion["start_monotonic_ns"], exclusion["end_monotonic_ns"]
            if left <= el < er <= right:
                cut_ns += er - el
        category = segment["mode"]
        categories[category] += right - left - cut_ns
        categories["excluded_unobserved"] += cut_ns
        if category in ("D", "L", "E"):
            lane_ns[segment["lane"]] += right - left - cut_ns
    exclusions_sorted = sorted(exclusions, key=lambda e: e["start_monotonic_ns"])
    for index, exclusion in enumerate(exclusions_sorted):
        left, right = exclusion["start_monotonic_ns"], exclusion["end_monotonic_ns"]
        assert left in observed and right in observed and left < right
        assert exclusion["start_utc"] == observed[left] and exclusion["end_utc"] == observed[right]
        assert sum(s["start_monotonic_ns"] <= left < right <= s["end_monotonic_ns"] for s in segments) == 1
        if index:
            assert exclusions_sorted[index - 1]["end_monotonic_ns"] <= left
    closed_elapsed = segments[-1]["end_monotonic_ns"] - segments[0]["start_monotonic_ns"]
    closed_research = sum(categories[m] for m in ("D", "L", "E"))
    closed_engaged = closed_research + categories["O"]
    closed_excluded = sum(categories[m] for m in ("wait", "recovery", "excluded_unobserved"))
    assert closed_elapsed == closed_engaged + closed_excluded and closed_research == sum(lane_ns.values())
    state = json.loads(raw["clock_state.json"])
    if state is not None:
        assert state["start_monotonic_ns"] == transitions[-1]["monotonic_ns"]
        assert state["mode"] == transitions[-1]["args"][0]
    source_bindings.extend({"path": name, "bytes": len(data), "sha256": digest(data)} for name, data in (
        (old_inventory_path, old_inventory_raw), (prior_integrity_path, prior_integrity_raw),
        (previous_actuals_path, previous_actuals_raw), ("v2/time_ledger.csv", ledger)))
    status = (ledger_ok and python_paths_ok and len(scientific_checks) == 973
              and all(r["matches"] for r in scientific_checks + python_checks + run_checks)
              and all(r["manifest_matches"] and r["dependencies_all_match"] for r in freeze_checks)
              and entry_ok and forecast["protected_minimum"] is None)
    result = {"schema": "F17-independent-entry-integrity-v1", "status": "PASS" if status else "FAIL",
              "contributor": "ChatGPT (GPT-6 Astra Pro), same-model internal delegated reviewer",
              "started_utc": started, "completed_utc": datetime.now(timezone.utc).isoformat(),
              "observed_wall_ns": time.monotonic_ns() - tick, "source_bindings": source_bindings,
              "script_sha256": digest(Path(__file__).read_bytes()), "scientific_checks": scientific_checks,
              "scientific_count": len(scientific_checks), "scientific_all_match": all(r["matches"] for r in scientific_checks),
              "python_checks": python_checks, "python_count": len(python_checks), "entry_python_paths_equal_git_tree": python_paths_ok,
              "python_all_match": all(r["matches"] for r in python_checks), "git_tree_command": tree_command,
              "original_run_attempt_directories": run_checks, "registered_freezes": freeze_checks,
              "ledger": {"bytes": len(ledger), "rows": len(csv_rows), "sha256": digest(ledger), "entry_unchanged": ledger_ok},
              "post_b_entry_matches_prior_close": entry_ok, "post_b_entry_minutes": forecast["post_b_1_entry_minutes"],
              "protected_minimum": forecast["protected_minimum"],
              "clock_snapshot": {"events": len(events), "closed_segments": len(segments), "exclusions": len(exclusions),
                                 "closed_through_utc": segments[-1]["end_utc"], "closed_elapsed_ns": closed_elapsed,
                                 "closed_categories_ns": dict(categories), "closed_lane_ns": dict(lane_ns),
                                 "closed_research_ns": closed_research, "closed_engaged_ns": closed_engaged,
                                 "closed_excluded_ns": closed_excluded, "closed_engaged_minutes_exact": str(Fraction(closed_engaged, 60_000_000_000)),
                                 "open_state": state, "open_segment_credit_in_this_review": 0,
                                 "scope": "Closed segments only; final clock stop and ledger append require a later audit."},
              "prior_inspection_failure": "One inline ledger/schema read failed with an unmatched parenthesis before execution; corrected read succeeded. First integrity reader then stopped on the distinct F14-dict/ND01-list manifest schemas. That failed source and failure record are preserved; corrected schema normalization changes no inputs.",
              "serializer_executed": False, "ledger_appended": False, "scientific_stages_or_tests_executed": False,
              "principal_concurrent_minutes_credited": 0}
    with OUT.open("x") as handle:
        json.dump(result, handle, sort_keys=True, indent=2)
        handle.write("\n")
    print(json.dumps({"status": result["status"], "scientific_files": len(scientific_checks),
                      "entry_python_files": len(python_checks), "ledger_entry_unchanged": ledger_ok,
                      "post_b_entry_matches": entry_ok, "clock_open": state is not None,
                      "output_sha256": digest(OUT.read_bytes())}, sort_keys=True))


if __name__ == "__main__":
    main()
