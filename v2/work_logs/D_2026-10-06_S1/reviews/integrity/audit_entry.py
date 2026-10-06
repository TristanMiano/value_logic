"""Read-only Gate D integrity and historical accounting reconstruction.

Only a new result file under this script's own directory is written. Scientific
modules, experiment runners, the historical serializer and test suites are not
imported or executed. Run from the repository root with PYTHONDONTWRITEBYTECODE=1.
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, getcontext
import hashlib
import io
import json
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

getcontext().prec = 90
ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
BASE = "f7aa0bef07cb21da9336429426244f6e944644a4"
F17 = "v2/work_logs/F17_2026-10-06_S1"
C = "v2/work_logs/C_2026-10-06_S1"
D = "v2/work_logs/D_2026-10-06_S1"
CHECKS: list[dict] = []
INPUTS: dict[str, dict] = {}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def raw(path: str) -> bytes:
    data = (ROOT / path).read_bytes()
    INPUTS[path] = {"bytes": len(data), "sha256": sha(data)}
    return data


def js(path: str):
    return json.loads(raw(path))


def lines(path: str):
    return [json.loads(x) for x in raw(path).splitlines() if x.strip()]


def check(name: str, passed: bool, detail=None):
    item = {"id": name, "passed": bool(passed)}
    if detail is not None:
        item["detail"] = detail
    CHECKS.append(item)


def git_bytes(path: str, commit: str = BASE) -> bytes:
    return subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT,
                          check=True, capture_output=True).stdout


def totals(rows):
    mode = {m: Decimal(0) for m in "DLEO"}
    lane = {l: Decimal(0) for l in "RX"}
    for r in rows:
        amount = Decimal(r["engaged_seconds"] or "0")
        mode[r["mode"]] += amount
        if r["mode"] != "O" and amount:
            lane[r["lane"]] += amount
    research = sum(mode[m] for m in "DLE")
    return {"rows": len(rows), "mode_seconds": {k: str(v) for k, v in mode.items()},
            "research_seconds": str(research), "engaged_seconds": str(sum(mode.values())),
            "lane_seconds": {k: str(v) for k, v in lane.items()},
            "lane_percent": {k: str(100*v/research) if research else None for k, v in lane.items()}}


def verify_bindings(node, location="root"):
    results = []
    if isinstance(node, dict):
        if isinstance(node.get("path"), str) and isinstance(node.get("sha256"), str):
            p = node["path"]
            if p == "paper_v2.md":
                data = raw(F17 + "/drafts/report_v2.md")
                mode = "preserved_F17_report_snapshot"
                check("f17_paper_snapshot_matches_entry_git", data == git_bytes(p))
            else:
                data = raw(p)
                mode = "current_unchanged_evidence"
            match = sha(data) == node["sha256"] and ("bytes" not in node or len(data) == node["bytes"])
            check("claim_binding:" + location, match, {"path": p, "mode": mode})
            results.append({"location": location, "path": p, "mode": mode, "matches": match})
        for key, val in node.items():
            results.extend(verify_bindings(val, location + "/" + key))
    elif isinstance(node, list):
        for i, val in enumerate(node):
            results.extend(verify_bindings(val, location + f"/{i}"))
    return results


def audit():
    baseline = js(D + "/baseline.json")
    ledger_bytes = raw("v2/time_ledger.csv")
    original = git_bytes("v2/time_ledger.csv")
    check("historical_ledger_exact_entry_git", ledger_bytes == original)
    check("historical_ledger_baseline_bytes_hash", len(ledger_bytes) == baseline["ledger_bytes"]
          and sha(ledger_bytes) == baseline["ledger_sha256"])
    ledger = list(csv.DictReader(io.StringIO(ledger_bytes.decode())))
    check("historical_ledger_row_count", len(ledger) == baseline["ledger_rows"] == 1117)

    inventory = js("v2/work_logs/F16_2026-10-05_S1/reviews/integrity/inventory_before.json")["files"]
    scientific = []
    for expected in inventory:
        data = raw(expected["path"])
        match = len(data) == expected["bytes"] and sha(data) == expected["sha256"]
        check("scientific:" + expected["path"], match)
        scientific.append({"path": expected["path"], "bytes": len(data), "sha256": sha(data), "matches": match})
    check("scientific_inventory_count", len(scientific) == 973)

    freezes = []
    for p, expected_hash, expected_count in [
        ("v2/experiments/freeze.v1.json", "b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c", 34),
        ("v2/experiments/neural_diagnostic_v1/freeze.json", "9c15af55b83d7edf134542a9c70bcc0f087c6f4f6491f993361a27493b5cf24c", 47),
    ]:
        manifest = js(p)
        check("freeze_manifest:" + p, INPUTS[p]["sha256"] == expected_hash)
        members = manifest["files"]
        members = [{"path": k, **v} for k, v in members.items()] if isinstance(members, dict) else members
        check("freeze_count:" + p, len(members) == expected_count)
        for member in members:
            data = raw(member["path"])
            check("freeze_member:" + member["path"], len(data) == member["bytes"] and sha(data) == member["sha256"])
        freezes.append({"path": p, "sha256": INPUTS[p]["sha256"], "members": len(members)})

    entry = js(D + "/entry_inventory.json")
    python_records = [x for x in entry if x["path"].endswith(".py")]
    for expected in python_records:
        data = raw(expected["path"])
        check("preexisting_python:" + expected["path"], len(data) == expected["bytes"] and sha(data) == expected["sha256"])

    bcomparison = js(C + "/reviews/technical/gate_b_source_comparison.json")
    bcase = js(C + "/reviews/technical/gate_b_case_clarification.json")
    b_records = []
    for expected in bcomparison["records"]:
        path = expected["path"]
        if path == bcase["manifest_path"]:
            resolved = bcase["resolved_tracked_path"]
            expected_sha = bcase["current_hashes"]["raw"]
        else:
            resolved = path
            expected_sha = expected["current_sha256"]
        data = raw(resolved)
        match = sha(data) == expected_sha
        check("accepted_gate_b_binding:" + resolved, match)
        b_records.append({"manifest_path": path, "resolved_path": resolved, "category": expected["category"], "matches_gate_c_accepted_bytes": match})
    check("gate_b_record_counts", Counter(r["category"] for r in b_records) == {"sources": 38, "evidence": 24})
    cc = js("v2/checkpoints/C_1_assessment.json")
    check("gate_c_author_approved", cc["author_decision"] == "PASS" and cc["technical_readiness"] == "MET" and cc["contribution_status"] == "SUPPORTED")
    check("gate_c_approval_historical_separation", cc["assessment_author_decision_at_close"] == "PENDING")
    check("gate_c_author_record_exists", b"I approve the pass, and you can move on to F17." in raw(cc["author_decision_record"]))

    old_science = js(C + "/reviews/accounting/scientific_hash_checks.json")
    runs = []
    for run in old_science["runs"]:
        actual_attempts = sorted(p.name for p in (ROOT / run["run"]).iterdir() if p.is_dir() and "attempt" in p.name)
        check("attempt_directories:" + run["run"], actual_attempts == run["attempt_directories"])
        results = []
        for row in run["sidecars"]:
            data = raw(row["path"])
            same = len(data) == row["bytes"] and sha(data) == row["sha256"]
            match_sidecar = sha(data) == row["expected_sha256"]
            check("saved_unit_preserved:" + row["path"], same)
            check("saved_sidecar_disposition:" + row["path"], match_sidecar == row["matches"])
            results.append({"path": row["path"], "matches_original_sidecar": match_sidecar})
        runs.append({"path": run["run"], "attempts": actual_attempts, "sidecars": len(results), "matching_sidecars": sum(x["matches_original_sidecar"] for x in results), "exceptions": [x for x in results if not x["matches_original_sidecar"]]})
    recovery = old_science["exact_recovery"]
    recovered = raw(recovery["path"])
    check("separate_exact_aggregate_recovery", len(recovered) == recovery["bytes"] and sha(recovered) == recovery["sha256"])

    claim_map = js("v2/reporting/F17_v1/claim_map.json")
    bindings = verify_bindings(claim_map)
    check("F17_claim_groups", len(claim_map["claims"]) == claim_map["claim_count"] == 42)
    current_report = raw("paper_v2.md")
    report = {"current_sha256": sha(current_report), "F17_historical_sha256": claim_map["report"]["sha256"],
              "changed_from_F17": sha(current_report) != claim_map["report"]["sha256"],
              "binding_rule": "F17's map remains historical. Final Gate D must bind the current report separately; paper-only presentation edits do not invalidate unchanged proof sources."}

    historical = js(C + "/reviews/accounting/historical_timing.json")
    floors = []
    for p in ("v2/checkpoints/A_1_timing_review.json", "v2/checkpoints/B_1_timing_review.json"):
        for task, requirement in js(p)["floor_checks"].items():
            selected = [r for r in ledger if r["task_id"] == task and r["mode"] == requirement["mode"]]
            seconds = sum(Decimal(r["engaged_seconds"] or "0") for r in selected)
            met = seconds >= 60 * Decimal(requirement["required_minutes"])
            check("historical_floor:" + task, met)
            check("historical_floor_prior_review:" + task, abs(seconds/60 - Decimal(str(requirement["recorded_minutes"]))) < Decimal("0.0000005"))
            floors.append({"task": task, "modes": requirement["mode"], "required_minutes": requirement["required_minutes"], "seconds_exact": str(seconds), "met": met})
    for group in historical["groups"]:
        group_rows = [r for r in ledger if r["task_id"] == group["task"] and r["attempt_id"] == group["attempt"]]
        check("historical_group_rows:" + group["attempt"], len(group_rows) == group["row_count"])
        recomputed = totals(group_rows)
        check("historical_group_totals:" + group["attempt"], all(Decimal(v) == Decimal(group["mode_seconds_exact"][m]) for m, v in recomputed["mode_seconds"].items()))
        for f in group["floors"]:
            modes = f["modes"].split("+")
            seconds = sum(Decimal(recomputed["mode_seconds"][m]) for m in modes)
            met = seconds >= 60 * Decimal(f["minimum_minutes"])
            check("historical_floor:" + group["attempt"] + ":" + f["modes"], met and seconds == Decimal(f["observed_seconds_exact"]))
            floors.append({"task": group["task"], "attempt": group["attempt"], "modes": f["modes"], "required_minutes": f["minimum_minutes"], "seconds_exact": str(seconds), "met": met})
    for record in historical["input_records"]:
        data = raw(record["path"])
        check("historical_clock_review_input:" + record["path"], len(data) == record["bytes"] and sha(data) == record["sha256"])

    segments = lines(F17 + "/segments.jsonl")
    events = lines(F17 + "/clocks.jsonl")
    exclusions = lines(F17 + "/exclusions.jsonl")
    actuals = js(F17 + "/actuals.json")
    event_set = {(e["runtime"], e["monotonic_ns"], e["utc"]) for e in events}
    check("F17_stopped", js(F17 + "/clock_state.json") is None)
    f17_rows = [r for r in ledger if r["task_id"] == "F17"]
    mode_ns = dict.fromkeys("DLEO", 0)
    lane_ns = dict.fromkeys("RX", 0)
    excluded_ns = 0
    elapsed_ns = 0
    check("F17_segment_row_count", len(segments) == len(f17_rows) == 12)
    for i, (segment, row) in enumerate(zip(segments, f17_rows)):
        start, end = segment["start_monotonic_ns"], segment["end_monotonic_ns"]
        delta = end - start
        check(f"F17_interval:{i}", delta == segment["elapsed_ns"] and delta >= 0)
        check(f"F17_raw_endpoints:{i}", all((segment["runtime"], segment[k + "_monotonic_ns"], segment[k + "_utc"]) in event_set for k in ["start", "end"]))
        if i:
            check(f"F17_adjacent:{i}", segments[i-1]["end_monotonic_ns"] == start)
        removed = sum(max(0, min(end, e["end_monotonic_ns"]) - max(start, e["start_monotonic_ns"])) for e in exclusions)
        category = segment["mode"]
        engaged = 0 if category in ("recovery", "wait") else delta - removed
        excluded_ns += delta - engaged
        elapsed_ns += delta
        effective_mode = category if category in "DLEO" else "O"
        mode_ns[effective_mode] += engaged
        if category in "DLE":
            lane_ns[segment["lane"]] += engaged
        check(f"F17_ledger_elapsed:{i}", Decimal(row["elapsed_seconds"]) == Decimal(delta)/10**9)
        check(f"F17_ledger_engaged:{i}", Decimal(row["engaged_seconds"]) == Decimal(engaged)/10**9)
        check(f"F17_ledger_timestamps:{i}", row["start_utc"] == segment["start_utc"] and row["end_utc"] == segment["end_utc"])
    for i, exclusion in enumerate(exclusions):
        check(f"F17_exclusion_containment:{i}", sum(s["start_monotonic_ns"] <= exclusion["start_monotonic_ns"] < exclusion["end_monotonic_ns"] <= s["end_monotonic_ns"] for s in segments) == 1)
    check("F17_modes", all(actuals["mode_and_exclusion_ns"][m] == n for m, n in mode_ns.items()))
    check("F17_lanes", actuals["lane_ns"] == lane_ns)
    check("F17_total_partition", actuals["engaged_ns"] == sum(mode_ns.values()) and actuals["excluded_ns"] == excluded_ns and actuals["elapsed_ns"] == elapsed_ns == sum(mode_ns.values()) + excluded_ns)
    check("F17_zero_concurrent_credit", actuals["concurrent_agent_minutes_credited"] == 0)
    check("F17_no_floor", actuals["protected_minimum"] is None)
    append = raw(F17 + "/ledger_append.csv")
    prefix = original[:actuals["ledger_prior_bytes"]]
    check("F17_preserved_prefix_hash", sha(prefix) == actuals["ledger_prior_sha256"])
    check("F17_preserved_append_hash", sha(append) == actuals["ledger_append_sha256"])
    check("F17_exact_append", original == prefix + append)
    prior_close = js(C + "/actuals.json")["post_b_1"]["close_minutes_decimal"]
    check("F17_carry_entry", actuals["post_b_1"]["entry_minutes_decimal"] == prior_close)
    expected_close = Decimal(prior_close) + Decimal(actuals["engaged_ns"])/Decimal(60000000000)
    check("F17_carry_close", abs(expected_close - Decimal(actuals["post_b_1"]["close_minutes_decimal"])) < Decimal("1e-75"))
    check("D_carry_entry", baseline["post_b_1_entry_minutes_decimal"] == actuals["post_b_1"]["close_minutes_decimal"])
    post_b_rows = ledger[738:]
    check("post_b_first_row", post_b_rows[0]["task_id"] == "N01")
    post_b_seconds = sum(Decimal(r["engaged_seconds"] or "0") for r in post_b_rows)
    offset = Decimal(baseline["post_b_1_entry_minutes_decimal"]) * 60 - post_b_seconds
    # The inherited C close is a 50-significant-digit decimal, not an exact
    # repeating rational. Bound its last-place rounding in seconds, together
    # with F17's later 80-digit rendering. D's exact copied string was checked
    # above, and every ledger duration is checked independently as nanoseconds.
    carry_display_bound = (Decimal(30).scaleb(Decimal(prior_close).as_tuple().exponent)
                           + Decimal(30).scaleb(Decimal(actuals["post_b_1"]["close_minutes_decimal"]).as_tuple().exponent))
    check("inherited_carry_offset_preserved", abs(offset - Decimal("0.000073995")) <= carry_display_bound,
          {"difference_seconds": str(offset - Decimal("0.000073995")),
           "bound_from_recorded_decimal_places_seconds": str(carry_display_bound)})

    saved_validations = []
    for result_path in sorted((ROOT / F17 / "verification").glob("*_attempt1/result.json")):
        p = result_path.relative_to(ROOT).as_posix()
        record = js(p)
        matches = []
        for label in ("stdout", "stderr"):
            data = raw((result_path.parent / (label + ".txt")).relative_to(ROOT).as_posix())
            matches.append(sha(data) == record[label + "_sha256"])
        check("saved_validation:" + record["label"], record["attempt"] == 1 and record["exit_code"] == 0 and all(matches))
        saved_validations.append({"path": p, "label": record["label"], "exit_code": record["exit_code"], "stream_hashes_match": all(matches)})
    check("saved_validation_count", len(saved_validations) == 5)
    regression_path = C + "/reviews/technical/regression_attempt1/result.json"
    regression = js(regression_path)
    for label in ("stdout", "stderr"):
        data = raw(C + "/reviews/technical/regression_attempt1/" + label + ".txt")
        check("Gate_C_regression_stream:" + label, sha(data) == regression[label + "_sha256"])
    check("Gate_C_saved_288", regression["reported_tests"] == 288 and regression["exit_code"] == 0 and regression["attempt"] == 1)

    cycle_sets = {
        "I": {f"F{x:02d}" for x in range(1, 5)},
        "II": {f"F{x:02d}" for x in range(5, 11)},
        "III_required": {f"F{x:02d}" for x in range(11, 17)},
    }
    cycles = {name: totals([r for r in ledger if r["task_id"] in tasks]) for name, tasks in cycle_sets.items()}
    cycles["post_B_including_C_F17"] = totals(post_b_rows)
    return {"historical_ledger": {"bytes": len(ledger_bytes), "rows": len(ledger), "sha256": sha(ledger_bytes)},
            "frozen_manifests": freezes, "scientific_artifacts": scientific,
            "preexisting_python_count": len(python_records), "gate_B_accepted_records": b_records,
            "original_runs": runs, "F17_claim_binding_count": len(bindings),
            "F17_claim_unique_paths": len({x["path"] for x in bindings}), "F17_bindings": bindings,
            "report_version": report, "floors": floors, "cycles": cycles,
            "F17_reconstruction": {"mode_ns": mode_ns, "lane_ns": lane_ns, "elapsed_ns": elapsed_ns,
                                   "excluded_ns": excluded_ns, "engaged_ns": sum(mode_ns.values())},
            "post_B_entry_minutes_decimal": baseline["post_b_1_entry_minutes_decimal"],
            "historical_csv_engaged_seconds": str(post_b_seconds), "inherited_offset_seconds": str(offset),
            "inherited_offset_display_bound_seconds": str(carry_display_bound),
            "saved_F17_validations": saved_validations,
            "saved_Gate_C_tests": {"count": 288, "attempt": 1, "rerun_in_D": False}}


if __name__ == "__main__":
    destination = OUT / (sys.argv[1] if len(sys.argv) > 1 else "entry_audit_attempt1.json")
    if destination.parent != OUT or destination.exists():
        raise SystemExit("Require a new result filename inside the review directory")
    start_ns = time.monotonic_ns()
    result = {"schema": "gate-d-integrity-audit-v1", "started_utc": datetime.now(timezone.utc).isoformat(),
              "base_commit": BASE, "contributor": "ChatGPT (GPT-6 Astra Pro), separately assigned same-model internal reviewer",
              "principal_concurrent_minutes_credited": 0, "scientific_stages_or_tests_executed": False,
              "command": [sys.executable, str(Path(__file__).relative_to(ROOT)), *sys.argv[1:]],
              "python": sys.version, "platform": platform.platform(), "script_sha256": sha(Path(__file__).read_bytes())}
    try:
        result.update(audit())
        result["status"] = "PASS" if all(x["passed"] for x in CHECKS) else "FAIL"
    except Exception as exc:
        import traceback
        result.update(status="ERROR", error=repr(exc), traceback=traceback.format_exc())
    result.update(checks=CHECKS, checks_passed=sum(x["passed"] for x in CHECKS),
                  checks_failed=[x for x in CHECKS if not x["passed"]], input_bindings=INPUTS,
                  ended_utc=datetime.now(timezone.utc).isoformat(), elapsed_ns=time.monotonic_ns()-start_ns,
                  process_user_cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime,
                  process_system_cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_stime,
                  process_max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with destination.open("x") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "checks_passed": result["checks_passed"], "failures": result["checks_failed"], "error": result.get("error"), "output": str(destination.relative_to(ROOT))}))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
