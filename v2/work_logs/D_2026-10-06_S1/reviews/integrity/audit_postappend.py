"""Independently reconstruct Gate D's stopped accounting and report bindings.

Run only after the principal's explicit closure. This script does not import
the serializer, write the ledger, operate the clock, or execute scientific
modules. Its sole output is an exclusive audit file beside this script.
"""
from __future__ import annotations

from collections import Counter
import csv
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
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
REPO = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
SESSION = "v2/work_logs/D_2026-10-06_S1"
BASE = "f7aa0bef07cb21da9336429426244f6e944644a4"
NS = 10**9
EXPECTED_REPORT_SHA = "c8f490ce94584fc93d27b759f1f524d5eeeb0d3885729d24db413cb4f5205c5d"
CHECKS = []
INPUTS = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    data = (REPO / path).read_bytes()
    INPUTS[path] = {"bytes": len(data), "sha256": sha(data)}
    return data


def js(path):
    return json.loads(read(path))


def records(path):
    return [json.loads(row) for row in read(path).splitlines() if row.strip()]


def check(name, passed, detail=None):
    row = {"id": name, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    CHECKS.append(row)


def as_ns(value):
    exact = Decimal(value or "0") * NS
    assert exact == exact.to_integral_value(), "Ledger duration exceeds nanosecond precision"
    return int(exact)


def render_error(value, exact):
    rendered = Fraction(Decimal(value))
    exponent = Decimal(value).as_tuple().exponent
    unit = Fraction(10**exponent) if exponent >= 0 else Fraction(1, 10**(-exponent))
    return rendered - exact, unit/2


def verify_bound_tree(value, trail="root", historical=False):
    checked = []
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
            path = value["path"]
            resolved = "v2/work_logs/F17_2026-10-06_S1/drafts/report_v2.md" if historical and path == "paper_v2.md" else path
            data = read(resolved)
            match = sha(data) == value["sha256"] and ("bytes" not in value or len(data) == value["bytes"])
            check("bound_file:" + trail, match, {"path": path, "resolved": resolved})
            checked.append({"path": path, "resolved": resolved, "location": trail, "matches": match})
        for key, item in value.items():
            checked.extend(verify_bound_tree(item, trail + "/" + key, historical))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            checked.extend(verify_bound_tree(item, trail + f"/{i}", historical))
    return checked


def run():
    baseline = js(SESSION + "/baseline.json")
    forecast = js(SESSION + "/forecast.json")
    actuals = js(SESSION + "/actuals.json")
    previous_actuals = js("v2/work_logs/F17_2026-10-06_S1/actuals.json")
    integrity = js(SESSION + "/ledger_integrity.json")
    ledger_bytes = read("v2/time_ledger.csv")
    append_bytes = read(SESSION + "/ledger_append.csv")
    old = subprocess.run(["git", "show", BASE + ":v2/time_ledger.csv"], cwd=REPO,
                         check=True, capture_output=True).stdout
    check("historical_prefix_baseline", len(old) == baseline["ledger_bytes"] == 273391
          and sha(old) == baseline["ledger_sha256"] == "ac1bdbb521f4ffe09843850dfadcab509a0f6c20f35db20202a79e5efb8ec36c")
    check("ledger_exact_git_prefix_plus_append", ledger_bytes == old + append_bytes)
    before_reader = csv.DictReader(io.StringIO(old.decode()))
    fields = before_reader.fieldnames
    before = list(before_reader)
    ledger = list(csv.DictReader(io.StringIO(ledger_bytes.decode())))
    appended = list(csv.DictReader(io.StringIO(append_bytes.decode()), fieldnames=fields))
    check("prior_rows_exact", len(before) == baseline["ledger_rows"] == 1117 and ledger[:1117] == before)
    check("append_rows_exact", ledger[1117:] == appended and len(appended) == actuals["ledger_rows_added"])
    check("no_prior_D_rows", not any(r["task_id"] == "D" or r["attempt_id"] == "D_1" for r in before))
    check("current_identity", actuals["task"] == "D" and actuals["attempt"] == "D_1" and all(r["task_id"] == "D" and r["attempt_id"] == "D_1" and r["session_id"] == "2026-10-06-S1" for r in appended))

    events = records(SESSION + "/clocks.jsonl")
    segments = records(SESSION + "/segments.jsonl")
    exclusions = records(SESSION + "/exclusions.jsonl")
    check("clock_stopped", js(SESSION + "/clock_state.json") is None)
    check("event_endpoints", events[0]["command"] == "start" and events[-1]["command"] == "stop")
    check("same_runtime", all(e["runtime"] == "linux-GateD-S1" for e in events)
          and all(s["runtime"] == "linux-GateD-S1" for s in segments))
    check("strict_event_order", all(a["monotonic_ns"] < b["monotonic_ns"] for a, b in zip(events, events[1:])))
    changes = [e for e in events if e["command"] != "check"]
    check("segment_transition_count", len(segments) == len(changes)-1)
    stamps = {e["monotonic_ns"]: e["utc"] for e in events}
    for i, exclusion in enumerate(exclusions):
        a, b = exclusion["start_monotonic_ns"], exclusion["end_monotonic_ns"]
        check(f"exclusion_observed_endpoints:{i}", a in stamps and b in stamps and a < b)
        check(f"exclusion_one_container:{i}", sum(s["start_monotonic_ns"] <= a < b <= s["end_monotonic_ns"] for s in segments) == 1)
        for j, other in enumerate(exclusions[:i]):
            check(f"exclusion_disjoint:{j}:{i}", b <= other["start_monotonic_ns"] or other["end_monotonic_ns"] <= a)

    partitions = []
    max_observed_gap = 0
    for i, (s, a, b) in enumerate(zip(segments, changes, changes[1:])):
        start, end = a["monotonic_ns"], b["monotonic_ns"]
        check(f"raw_segment_bounds:{i}", s["start_monotonic_ns"] == start and s["end_monotonic_ns"] == end and s["elapsed_ns"] == end-start)
        check(f"raw_segment_utc:{i}", s["start_utc"] == a["utc"] and s["end_utc"] == b["utc"])
        expected_mode = a["args"][0]
        expected_lane = "" if a["command"] == "pause" or a["args"][1] == "-" else a["args"][1]
        check(f"raw_segment_mode_lane:{i}", s["mode"] == expected_mode and s["lane"] == expected_lane)
        endpoints = {start, end}
        for exclusion in exclusions:
            if start <= exclusion["start_monotonic_ns"] < exclusion["end_monotonic_ns"] <= end:
                endpoints.update((exclusion["start_monotonic_ns"], exclusion["end_monotonic_ns"]))
        points = sorted(endpoints)
        for left, right in zip(points, points[1:]):
            duration = right-left
            is_removed = any(x["start_monotonic_ns"] <= left < right <= x["end_monotonic_ns"] for x in exclusions)
            mode, lane = s["mode"], s["lane"]
            engaged = wait = unobserved = 0
            if is_removed:
                category, mode, lane, unobserved = "recovery_unobserved", "O", "", duration
            elif mode == "recovery":
                category, mode, lane, unobserved = "paused_recovery", "O", "", duration
            elif mode == "wait":
                category, mode, lane, wait = "tool_wait", "O", "", duration
            else:
                category, engaged = mode, duration
                check(f"valid_positive_lane:{i}:{left}", (mode == "O" and not lane) or (mode in "DLE" and lane in "RX"))
                observations = sorted({left, right, *[t for t in stamps if left < t < right]})
                gap = max(y-x for x,y in zip(observations, observations[1:]))
                max_observed_gap = max(max_observed_gap, gap)
                check(f"observed_gap:{i}:{left}", gap <= 900*NS)
            partitions.append({"raw_segment_index": i, "start_monotonic_ns": left,
                               "end_monotonic_ns": right, "elapsed_ns": duration,
                               "engaged_ns": engaged, "tool_wait_ns": wait, "unmeasured_ns": unobserved,
                               "category": category, "effective_mode": mode, "effective_lane": lane})
    check("effective_partition_count", len(partitions) == len(appended))
    check("effective_partition_matches_actuals", partitions == actuals["effective_segment_accounting"])
    for i, (part, row) in enumerate(zip(partitions, appended)):
        check(f"row_timestamps:{i}", row["start_utc"] == stamps[part["start_monotonic_ns"]] and row["end_utc"] == stamps[part["end_monotonic_ns"]])
        check(f"row_mode_lane:{i}", row["mode"] == part["effective_mode"] and row["lane"] == part["effective_lane"])
        for field, expected in [("elapsed_seconds", part["elapsed_ns"]), ("engaged_seconds", part["engaged_ns"]), ("tool_wait_seconds", part["tool_wait_ns"]), ("unmeasured_seconds", part["unmeasured_ns"]), ("idle_seconds", 0)]:
            check(f"row_duration:{i}:{field}", as_ns(row[field]) == expected)
        check(f"row_partition:{i}", as_ns(row["elapsed_seconds"]) == sum(as_ns(row[k]) for k in ["engaged_seconds", "tool_wait_seconds", "idle_seconds", "unmeasured_seconds"]))
        check(f"row_pending_author:{i}", "author phase decision pending" in row["status"])

    mode_totals = {k: sum(p["elapsed_ns"] for p in partitions if p["category"] == k) for k in actuals["mode_and_exclusion_ns"]}
    lanes = {k: sum(p["engaged_ns"] for p in partitions if p["effective_lane"] == k) for k in "RX"}
    engaged = sum(p["engaged_ns"] for p in partitions)
    research = sum(p["engaged_ns"] for p in partitions if p["effective_mode"] in "DLE")
    elapsed = events[-1]["monotonic_ns"]-events[0]["monotonic_ns"]
    excluded = sum(p["tool_wait_ns"]+p["unmeasured_ns"] for p in partitions)
    check("mode_totals", mode_totals == actuals["mode_and_exclusion_ns"])
    check("lane_totals", lanes == actuals["lane_ns"] and research == sum(lanes.values()))
    check("complete_time_partition", elapsed == engaged+excluded == actuals["elapsed_ns"] and engaged == actuals["engaged_ns"] and excluded == actuals["excluded_ns"] and research == actuals["research_ns"])
    research_ends = [p["end_monotonic_ns"] for p in partitions if p["engaged_ns"] and p["effective_mode"] in "DLE"]
    check("actual_research_cutoff", actuals["research_cutoff_monotonic_ns"] == max(research_ends))
    check("no_floor_or_concurrent_credit", actuals["protected_minimum"] is None and actuals["concurrent_agent_minutes_credited"] == 0)
    check("gate_author_status", actuals["gate_c_author_decision"] == "PASS" and actuals["gate_d_author_decision"] == "PENDING")
    for key, count in [("engaged_minutes_decimal", engaged), ("research_minutes_decimal", research), ("excluded_minutes_decimal", excluded)]:
        error, half_unit = render_error(actuals[key], Fraction(count, 60*NS))
        check("rendered_total:" + key, abs(error) <= half_unit)
    for mode in "DLEO":
        matches = [row for row in appended if row["mode"] == mode and row["forecast_seconds"]]
        positive = [row for row in appended if row["mode"] == mode and as_ns(row["engaged_seconds"]) > 0]
        check("forecast_once:" + mode, len(matches) == bool(positive))
        if positive:
            check("forecast_first_positive:" + mode, matches[0] is positive[0] and Decimal(matches[0]["forecast_seconds"]) == forecast["central_minutes"][mode]*60)
        err = Fraction(mode_totals[mode], 60*NS) - forecast["central_minutes"][mode]
        error, half_unit = render_error(actuals["forecast_error_minutes_decimal"][mode], err)
        check("forecast_error:" + mode, abs(error) <= half_unit)

    entry = forecast["post_b_1_entry_minutes"]
    check("entry_three_way_exact", entry == baseline["post_b_1_entry_minutes_decimal"] == previous_actuals["post_b_1"]["close_minutes_decimal"] == actuals["post_b_1"]["entry_minutes_decimal"])
    exact_close = Fraction(Decimal(entry)) + Fraction(engaged, 60*NS)
    carry_error, carry_half_unit = render_error(actuals["post_b_1"]["close_minutes_decimal"], exact_close)
    check("close_carry_rounding_only", abs(carry_error) <= carry_half_unit)
    exact_remaining_from_displayed_close = 1920 - Fraction(Decimal(actuals["post_b_1"]["close_minutes_decimal"]))
    remaining_error, remaining_half_unit = render_error(actuals["post_b_1"]["remaining_minutes_decimal"], exact_remaining_from_displayed_close)
    check("remaining_carry_rounding_only", abs(remaining_error) <= remaining_half_unit)
    post = actuals["post_b_1"]
    check("checkpoint_scope", post["checkpoint_minutes"] == 1920 and post["previous_checkpoint_minutes"] == 960 and post["previous_checkpoint_completed_in_F17"] is True and post["automatic_next_phase_authorized"] is False and post["recurrence_clock_reset"] is False)
    check("unchanged_inherited_offset", post["inherited_declared_minus_historical_csv_seconds_decimal"] == baseline["inherited_declared_minus_historical_csv_seconds_decimal"] == "0.000073995")
    for name, expected in actuals["input_sha256"].items():
        check("accounting_input_hash:" + name, sha(read(SESSION + "/" + name)) == expected)
    for name, expected in [("ledger_prior_sha256", sha(old)), ("ledger_append_sha256", sha(append_bytes)), ("ledger_final_sha256", sha(ledger_bytes))]:
        check("actuals_ledger_hash:" + name, actuals[name] == expected)
    check("integrity_record", integrity["prior_sha256"] == sha(old) and integrity["append_sha256"] == sha(append_bytes) and integrity["final_sha256"] == sha(ledger_bytes) and integrity["prior_bytes_equal"] is True and integrity["final_rows"] == len(ledger))

    current_map = js("v2/reporting/D_1/claim_map.json")
    current_bindings = verify_bound_tree(current_map, "D_map")
    old_map = js("v2/reporting/F17_v1/claim_map.json")
    historical_bindings = verify_bound_tree(old_map, "F17_map", historical=True)
    check("final_report_pinned", current_map["report"]["sha256"] == current_map["reviewed_snapshot"]["sha256"] == EXPECTED_REPORT_SHA)
    check("claim_count", len(current_map["claims"]) == len({x["id"] for x in current_map["claims"]}) == 42)
    old_by_id = {x["id"]: x for x in old_map["claims"]}
    changed_claims = []
    for claim in current_map["claims"]:
        old_claim = old_by_id[claim["id"]]
        if claim != old_claim:
            changed_claims.append(claim["id"])
            check("revised_claim_evidence_unchanged:" + claim["id"], claim["evidence"] == old_claim["evidence"])
    check("only_disclosed_claim_clarification", changed_claims == ["F17-MATH-13"])
    check("historical_map_support_count", len(historical_bindings) == 145)
    check("D_report_author_pending", current_map["gate_D_author_decision"] == "PENDING")
    inventory = js(SESSION + "/entry_inventory.json")
    python = [x for x in inventory if x["path"].endswith(".py")]
    for expected in python:
        data = read(expected["path"])
        check("preexisting_python:" + expected["path"], len(data) == expected["bytes"] and sha(data) == expected["sha256"])
    scientific = js("v2/work_logs/F16_2026-10-05_S1/reviews/integrity/inventory_before.json")["files"]
    for expected in scientific:
        data = read(expected["path"])
        check("scientific:" + expected["path"], len(data) == expected["bytes"] and sha(data) == expected["sha256"])

    post_b_start = next(i for i,r in enumerate(ledger) if r["task_id"] == "N01" and r["attempt_id"] == "N01-A1")
    post_b_rows = ledger[post_b_start:]
    lane_sums = {lane: sum(Decimal(r["engaged_seconds"] or "0") for r in post_b_rows if r["mode"] in "DLE" and r["lane"] == lane) for lane in "RX"}
    combined_research = sum(lane_sums.values())
    check("post_B_plus_consolidation_lane_balance", all(value >= combined_research/4 for value in lane_sums.values()))
    return {"ledger": {"prior_bytes": len(old), "prior_rows": len(before), "append_bytes": len(append_bytes), "rows_added": len(appended), "final_bytes": len(ledger_bytes), "final_rows": len(ledger), "prior_sha256": sha(old), "append_sha256": sha(append_bytes), "final_sha256": sha(ledger_bytes)},
            "clock": {"events": len(events), "raw_segments": len(segments), "effective_intervals": len(partitions), "exclusions": len(exclusions), "mode_ns": mode_totals, "lane_ns": lanes, "engaged_ns": engaged, "research_ns": research, "excluded_ns": excluded, "elapsed_ns": elapsed, "max_credited_observation_gap_ns": max_observed_gap},
            "post_B": {"entry_minutes_decimal": entry, "close_minutes_decimal": post["close_minutes_decimal"], "remaining_to_1920_minutes_decimal": post["remaining_minutes_decimal"], "close_exact_rational": str(exact_close), "display_error_rational_minutes": str(carry_error), "combined_research_minutes_decimal": str(combined_research/60), "combined_lane_percent": {k:str(100*v/combined_research) for k,v in lane_sums.items()}},
            "current_report_sha256": EXPECTED_REPORT_SHA, "current_map_bindings": len(current_bindings), "historical_map_bindings": len(historical_bindings), "only_changed_claim": changed_claims, "scientific_file_count": len(scientific), "preexisting_python_count": len(python)}


if __name__ == "__main__":
    destination = OUT / (sys.argv[1] if len(sys.argv) > 1 else "postappend_attempt1.json")
    if destination.parent != OUT or destination.exists():
        raise SystemExit("Require a new audit output filename beside this script")
    started = time.monotonic_ns()
    result = {"schema": "gate-d-independent-postappend-audit-v1", "started_utc": datetime.now(timezone.utc).isoformat(),
              "contributor": "ChatGPT (GPT-6 Astra Pro), separately assigned same-model internal reviewer",
              "command": [sys.executable, str(Path(__file__).relative_to(REPO)), *sys.argv[1:]],
              "script_sha256": sha(Path(__file__).read_bytes()), "python": sys.version, "platform": platform.platform(),
              "principal_concurrent_credit_minutes": 0, "serializer_executed": False, "ledger_or_clock_written": False, "scientific_execution": False}
    try:
        result.update(run())
        result["status"] = "PASS" if all(c["passed"] for c in CHECKS) else "FAIL"
    except Exception as exc:
        import traceback
        result.update(status="ERROR", error=repr(exc), traceback=traceback.format_exc())
    result.update(checks=CHECKS, checks_passed=sum(c["passed"] for c in CHECKS), checks_failed=[c for c in CHECKS if not c["passed"]], input_bindings=INPUTS,
                  ended_utc=datetime.now(timezone.utc).isoformat(), elapsed_ns=time.monotonic_ns()-started,
                  process_user_cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime,
                  process_system_cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_stime,
                  process_max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with destination.open("x") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "checks_passed": result["checks_passed"], "checks_failed": result["checks_failed"], "error": result.get("error"), "output": str(destination.relative_to(REPO))}))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
