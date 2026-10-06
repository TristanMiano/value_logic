"""Independent F17 postappend audit; reads evidence and creates one audit result.

Contributor: ChatGPT (GPT-6 Astra Pro), same-model internal review.
Administrative tail, zero credited minutes. No experimental imports or execution.
This does not import/run the serializer, clock, tests, or any scientific runner.
"""

import csv
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
SESSION = HERE.parents[1]
REPO = SESSION.parents[2]
OUTPUT = HERE / "postappend_result.json"
NS = 10**9
MINUTE_NS = 60 * NS
CHECKS = []
SOURCES = {}


def require(condition, description):
    if not condition:
        raise ValueError(description)
    CHECKS.append(description)


def source(path):
    path = path.resolve()
    raw = path.read_bytes()
    SOURCES[str(path.relative_to(REPO))] = {
        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()
    }
    return raw


def read_json(path):
    return json.loads(source(path))


def read_jsonl(path):
    return [json.loads(line) for line in source(path).splitlines()]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def decimal80(value):
    value = Fraction(value)
    with localcontext() as context:
        context.prec = 80
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def minutes(ns):
    return decimal80(Fraction(ns, MINUTE_NS))


def check_decimal(observed, expected, description):
    require(Decimal(observed) == Decimal(decimal80(expected)), description)


def csv_ns(value):
    value_ns = Fraction(value) * NS
    require(value_ns.denominator == 1, "CSV seconds resolve to an integer nanosecond")
    require(value_ns >= 0, "CSV duration is nonnegative")
    return value_ns.numerator


def main():
    require(not OUTPUT.exists(), "Audit output is absent; exclusive creation permitted")
    baseline = read_json(SESSION / "baseline.json")
    forecast = read_json(SESSION / "forecast.json")
    actuals = read_json(SESSION / "actuals.json")
    integrity = read_json(SESSION / "ledger_integrity.json")
    boundary = read_json(SESSION / "checkpoint_boundary.json")
    gate_c_actuals = read_json(REPO / "v2/work_logs/C_2026-10-06_S1/actuals.json")
    require(read_json(SESSION / "clock_state.json") is None, "Observed clock is stopped")
    event_bytes = source(SESSION / "clocks.jsonl")
    event_lines = event_bytes.splitlines(keepends=True)
    events = [json.loads(line) for line in event_lines]
    segments = read_jsonl(SESSION / "segments.jsonl")
    exclusions = read_jsonl(SESSION / "exclusions.jsonl")
    append = source(SESSION / "ledger_append.csv")
    ledger = source(REPO / "v2/time_ledger.csv")
    prefix = ledger[:baseline["ledger_bytes"]]
    git_result = subprocess.run(
        ["git", "show", baseline["head"] + ":v2/time_ledger.csv"],
        cwd=REPO, capture_output=True, check=False,
    )
    require(git_result.returncode == 0, "Read-only Git entry-ledger extraction succeeded")
    require(prefix == git_result.stdout, "Prior ledger bytes exactly equal the Git entry blob")
    require(digest(prefix) == baseline["ledger_sha256"], "Prior ledger SHA256 matches baseline")
    require(ledger == prefix + append, "Current ledger is exactly original bytes plus saved append")
    require(len(prefix) == 269074, "Exactly 269074 prior bytes are preserved")
    reader = csv.DictReader(io.StringIO(prefix.decode()))
    fields, prior_rows = reader.fieldnames, list(reader)
    rows = list(csv.DictReader(io.StringIO(append.decode()), fieldnames=fields))
    all_rows = list(csv.DictReader(io.StringIO(ledger.decode())))
    require(len(prior_rows) == baseline["ledger_rows"] == 1105, "Exactly 1105 prior rows are preserved")
    require(not any(r["task_id"] == "F17" or r["attempt_id"] == "F17-A1" for r in prior_rows),
            "No F17 row occurs in the prior ledger")
    require(len(rows) == 12 and len(all_rows) == 1117, "Exactly 12 new rows give 1117 final rows")
    require(all_rows == prior_rows + rows, "Parsed ledger rows equal prior plus append without other change")

    require(events[0]["command"] == "start" and events[-1]["command"] == "stop",
            "Observed events begin with start and end with stop")
    require(all(e["runtime"] == "linux-F17-S1" for e in events), "Events share one monotonic runtime")
    require(all(a["monotonic_ns"] < b["monotonic_ns"] for a, b in zip(events, events[1:])),
            "Every observed event is strictly increasing")
    reconstructed = []
    active = None
    for event in events:
        command = event["command"]
        require(command in {"start", "switch", "pause", "resume", "check", "stop"},
                "Clock command is recognized")
        if command == "check":
            require(active is not None, "Check occurs while a recorded state is open")
            continue
        if active is not None:
            reconstructed.append({
                **active, "end_utc": event["utc"], "end_monotonic_ns": event["monotonic_ns"],
                "elapsed_ns": event["monotonic_ns"] - active["start_monotonic_ns"],
            })
        if command == "stop":
            active = None
        else:
            mode = event["args"][0]
            lane = "" if command == "pause" or event["args"][1] == "-" else event["args"][1]
            note = event["args"][1] if command == "pause" else event["args"][2]
            active = {"mode": mode, "lane": lane, "note": note,
                      "start_utc": event["utc"], "start_monotonic_ns": event["monotonic_ns"],
                      "runtime": event["runtime"]}
    require(active is None and reconstructed == segments, "State-machine reconstruction exactly matches all raw segments")
    require(len(segments) == actuals["raw_segment_count"] == 12, "Raw segment count is 12")
    observed_utc = {e["monotonic_ns"]: e["utc"] for e in events}
    exclusion_ranges = sorted((e["start_monotonic_ns"], e["end_monotonic_ns"]) for e in exclusions)
    require(all(a[1] <= b[0] for a, b in zip(exclusion_ranges, exclusion_ranges[1:])),
            "Explicit exclusions do not overlap")
    for exclusion in exclusions:
        left, right = exclusion["start_monotonic_ns"], exclusion["end_monotonic_ns"]
        require(left < right and left in observed_utc and right in observed_utc,
                "Exclusion endpoints are distinct observed monotonic ticks")
        require(exclusion["start_utc"] == observed_utc[left] and exclusion["end_utc"] == observed_utc[right],
                "Exclusion UTC labels match their observed endpoints")
        require(sum(s["start_monotonic_ns"] <= left < right <= s["end_monotonic_ns"] for s in segments) == 1,
                "Each exclusion is contained in exactly one raw segment")

    effective = []
    max_observed_gap = 0
    for index, segment in enumerate(segments):
        start, stop = segment["start_monotonic_ns"], segment["end_monotonic_ns"]
        cuts = {start, stop}
        for left, right in exclusion_ranges:
            if start <= left < right <= stop:
                cuts.update((left, right))
        cuts = sorted(cuts)
        for left, right in zip(cuts, cuts[1:]):
            duration = right - left
            excluded = any(a <= left < right <= b for a, b in exclusion_ranges)
            if excluded:
                category, mode, lane = "recovery_unobserved", "O", ""
            elif segment["mode"] == "recovery":
                category, mode, lane = "paused_recovery", "O", ""
            elif segment["mode"] == "wait":
                category, mode, lane = "tool_wait", "O", ""
            else:
                category, mode, lane = segment["mode"], segment["mode"], segment["lane"]
                require(mode in {"D", "L", "E", "O"}, "Credited interval has a permitted mode")
                require((mode == "O" and not lane) or (mode != "O" and lane in {"R", "X"}),
                        "Lane applies exactly to a research interval")
                ticks = sorted({left, right, *(e["monotonic_ns"] for e in events if left < e["monotonic_ns"] < right)})
                max_observed_gap = max(max_observed_gap, *(b - a for a, b in zip(ticks, ticks[1:])))
            effective.append({
                "raw_segment_index": index, "start_monotonic_ns": left, "end_monotonic_ns": right,
                "elapsed_ns": duration, "category": category, "effective_mode": mode, "effective_lane": lane,
                "engaged_ns": duration if category in {"D", "L", "E", "O"} else 0,
                "tool_wait_ns": duration if category == "tool_wait" else 0,
                "unmeasured_ns": duration if category in {"recovery_unobserved", "paused_recovery"} else 0,
            })
    require(effective == actuals["effective_segment_accounting"], "Independent effective interval partition matches actuals")
    require(max_observed_gap <= 900 * NS, "Maximum credited gap between observations is at most 900 seconds")
    require(len(effective) == len(rows), "Every effective interval has exactly one appended CSV row")
    categories = ("D", "L", "E", "O", "tool_wait", "recovery_unobserved", "paused_recovery")
    totals = {category: sum(p["elapsed_ns"] for p in effective if p["category"] == category) for category in categories}
    lanes = {lane: sum(p["engaged_ns"] for p in effective if p["effective_lane"] == lane) for lane in ("R", "X")}
    first_forecasts = set()
    forecast_rows = []
    for index, (row, part) in enumerate(zip(rows, effective)):
        require((row["task_id"], row["attempt_id"], row["session_id"]) == ("F17", "F17-A1", "2026-10-06-S1"),
                "Appended row belongs only to F17-A1 principal session")
        require((row["mode"], row["lane"]) == (part["effective_mode"], part["effective_lane"]),
                "Appended mode/lane matches independently reconstructed interval")
        require((row["start_utc"], row["end_utc"]) ==
                (observed_utc[part["start_monotonic_ns"]], observed_utc[part["end_monotonic_ns"]]),
                "Appended UTC endpoints match original observations")
        row_ns = {name: csv_ns(row[name + "_seconds"]) for name in ("elapsed", "engaged", "tool_wait", "idle", "unmeasured")}
        for name in ("elapsed", "engaged", "tool_wait", "unmeasured"):
            require(row_ns[name] == part[name + "_ns"], "Appended duration matches exact independent nanoseconds")
        require(row_ns["idle"] == 0 and row_ns["elapsed"] == sum(row_ns[x] for x in ("engaged", "tool_wait", "idle", "unmeasured")),
                "Every CSV row exactly partitions elapsed time without credited idle")
        if part["engaged_ns"] and row["mode"] not in first_forecasts:
            require(row["forecast_seconds"] == str(60 * forecast["central_minutes"][row["mode"]]),
                    "Mode forecast appears once on its first engaged row")
            first_forecasts.add(row["mode"])
            forecast_rows.append({"append_row_1_based": index + 1, "mode": row["mode"], "forecast_seconds": row["forecast_seconds"]})
        else:
            require(row["forecast_seconds"] == "", "No forecast duplication or assignment to excluded intervals")
        require(row["artifact"] == "v2/work_logs/F17_2026-10-06_S1.md", "Ledger artifact points to F17 work log")
        require("Gate D unattempted" in row["status"], "Appended row preserves Gate D unattempted status")
    require(first_forecasts == {"D", "L", "E", "O"}, "All four forecasts are retained exactly once")
    elapsed = events[-1]["monotonic_ns"] - events[0]["monotonic_ns"]
    research = sum(totals[x] for x in ("D", "L", "E"))
    engaged = research + totals["O"]
    excluded = sum(totals[x] for x in ("tool_wait", "recovery_unobserved", "paused_recovery"))
    require(sum(s["elapsed_ns"] for s in segments) == elapsed == engaged + excluded,
            "Whole observed interval is exactly engaged plus excluded, with no gap or double count")
    require(research == sum(lanes.values()), "Research total equals the disjoint R and X lanes")
    require(totals == actuals["mode_and_exclusion_ns"] and lanes == actuals["lane_ns"],
            "All mode, exclusion and lane integer totals match actuals")
    for key, value in (("elapsed", elapsed), ("research", research), ("engaged", engaged), ("excluded", excluded)):
        require(actuals[key + "_ns"] == value, "Actual " + key + " nanoseconds reconcile")
        if key != "elapsed":
            check_decimal(actuals[key + "_minutes_decimal"], Fraction(value, MINUTE_NS),
                          "Actual " + key + " minute display is correctly rounded at precision 80")
    for key, value in totals.items():
        check_decimal(actuals["minutes_decimal"][key], Fraction(value, MINUTE_NS), "Mode/exclusion decimal matches exact ns")
    for key, value in lanes.items():
        check_decimal(actuals["lane_minutes_decimal"][key], Fraction(value, MINUTE_NS), "Lane decimal matches exact ns")
    for mode in ("D", "L", "E", "O"):
        check_decimal(actuals["forecast_error_minutes_decimal"][mode],
                      Fraction(totals[mode] - MINUTE_NS * forecast["central_minutes"][mode], MINUTE_NS),
                      "Forecast residual is formed from integer nanoseconds without default-context truncation")
    require(actuals["central_forecast_minutes"] == forecast["central_minutes"] and
            actuals["high_forecast_minutes"] == forecast["high_minutes"], "Original central/high forecasts are preserved")
    require(actuals["protected_minimum"] is forecast["protected_minimum"] is None, "No F17 protected floor is introduced")
    require(actuals["concurrent_agent_minutes_credited"] == forecast["concurrent_agent_credit"] == 0,
            "Concurrent agents receive zero additional principal credit")
    require(actuals["accounting_cutoff_monotonic_ns"] == events[-1]["monotonic_ns"] and
            actuals["accounting_cutoff_utc"] == events[-1]["utc"], "Accounting cutoff is the final observed stop")
    research_cutoff = max(p["end_monotonic_ns"] for p in effective if p["category"] in {"D", "L", "E"})
    require(actuals["research_cutoff_monotonic_ns"] == research_cutoff and
            actuals["research_cutoff_utc"] == observed_utc[research_cutoff], "Research cutoff is last credited research endpoint")

    entry = Fraction(forecast["post_b_1_entry_minutes"])
    require(entry == Fraction(gate_c_actuals["post_b_1"]["close_minutes_decimal"]), "F17 entry preserves prior Gate C POST-B close")
    require(actuals["post_b_1"]["entry_minutes_decimal"] == forecast["post_b_1_entry_minutes"], "Actuals preserve inherited decimal carry exactly")
    close_exact = entry + Fraction(engaged, MINUTE_NS)
    check_decimal(actuals["post_b_1"]["close_minutes_decimal"], close_exact, "POST-B close adds only exact F17 engaged ns")
    with localcontext() as context:
        context.prec = 80
        displayed_remaining = Decimal(960) - Decimal(actuals["post_b_1"]["close_minutes_decimal"])
    require(Decimal(actuals["post_b_1"]["remaining_minutes_decimal"]) == displayed_remaining,
            "POST-B remaining exactly subtracts the declared 80-digit close")
    close_remaining_display_error = Fraction(actuals["post_b_1"]["remaining_minutes_decimal"]) - (960 - close_exact)
    require(abs(close_remaining_display_error) < Fraction(1, 10**77),
            "Derived remaining display differs from the unrounded rational by less than one 80-digit close unit")
    require(actuals["post_b_1"]["checkpoint_reached"] is True and actuals["post_b_1"]["recurrence_clock_reset"] is False,
            "Sixteen-hour crossing is flagged without resetting recurrence clock")
    require(actuals["post_b_1"]["inherited_declared_minus_historical_csv_seconds_decimal"] ==
            gate_c_actuals["post_b_1"]["inherited_declared_minus_historical_csv_seconds_decimal"] == "0.000073995",
            "Inherited historical rounding residual is unchanged")

    boundary_event = boundary["clock_event"]
    boundary_index = events.index(boundary_event)
    boundary_ns = boundary_event["monotonic_ns"]
    require(digest(b"".join(event_lines[:boundary_index + 1])) == boundary["source_events_sha256_at_boundary"],
            "Checkpoint binds exactly the original event-file prefix at that boundary")
    boundary_totals = {category: 0 for category in categories}
    def engaged_at(tick):
        return sum(max(0, min(tick, p["end_monotonic_ns"]) - p["start_monotonic_ns"])
                   for p in effective if p["engaged_ns"])
    for part in effective:
        boundary_totals[part["category"]] += max(0, min(boundary_ns, part["end_monotonic_ns"]) - part["start_monotonic_ns"])
    checkpoint_categories = {mode: boundary_totals[mode] for mode in ("D", "L", "E", "O")}
    checkpoint_categories.update(wait=boundary_totals["tool_wait"],
                                 recovery=boundary_totals["recovery_unobserved"] + boundary_totals["paused_recovery"])
    boundary_engaged = engaged_at(boundary_ns)
    boundary_cumulative = entry + Fraction(boundary_engaged, MINUTE_NS)
    require(boundary["mode_and_exclusion_ns"] == checkpoint_categories, "Checkpoint categories match clipped effective intervals")
    require(boundary["F17_engaged_ns_at_boundary"] == boundary_engaged, "Checkpoint F17 engaged ns are exact")
    check_decimal(boundary["F17_engaged_minutes_decimal_at_boundary"], Fraction(boundary_engaged, MINUTE_NS),
                  "Checkpoint F17 minute display matches exact ns")
    check_decimal(boundary["cumulative_minutes_decimal_at_boundary"], boundary_cumulative, "Checkpoint POST-B cumulative is exact at declared precision")
    with localcontext() as context:
        context.prec = 80
        displayed_overshoot = Decimal(boundary["cumulative_minutes_decimal_at_boundary"]) - Decimal(960)
    require(Decimal(boundary["overshoot_minutes_decimal_at_boundary"]) == displayed_overshoot,
            "Checkpoint overshoot exactly subtracts from its declared 80-digit cumulative")
    boundary_overshoot_display_error = Fraction(boundary["overshoot_minutes_decimal_at_boundary"]) - (boundary_cumulative - 960)
    require(abs(boundary_overshoot_display_error) < Fraction(1, 10**77),
            "Derived checkpoint overshoot differs from the unrounded rational by less than one 80-digit cumulative unit")
    require(boundary["post_b_1_entry_minutes_decimal"] == forecast["post_b_1_entry_minutes"] and
            boundary["milestone_minutes"] == 960 and boundary["recurrence_clock_reset"] is False and
            boundary["subagent_additional_credit"] == 0, "Checkpoint preserves entry, milestone and zero concurrency credit")
    require(digest(source(REPO / boundary["report"]["path"])) == boundary["report"]["sha256"],
            "Checkpoint report hash matches delivered report")
    require(digest(source(SESSION / "drafts/report_v2.md")) == boundary["report"]["sha256"],
            "Checkpoint report hash matches reviewed v2 snapshot")
    tail_ns = engaged - boundary_engaged
    require(tail_ns == events[-1]["monotonic_ns"] - boundary_ns, "Boundary-to-close interval is entirely credited O")
    require(tail_ns == totals["O"] - boundary_totals["O"], "Boundary-to-close adds no research or excluded time")
    first_above = next(e for e in events if entry + Fraction(engaged_at(e["monotonic_ns"]), MINUTE_NS) >= 960)
    first_above_cumulative = entry + Fraction(engaged_at(first_above["monotonic_ns"]), MINUTE_NS)

    for name, expected in actuals["input_sha256"].items():
        require(digest(source(SESSION / name)) == expected, "Actuals input hash verified: " + name)
    require(actuals["input_sha256"]["close_accounting.py"] == "355577bdcc20cb2d3c727b0ace1246ce1a6ace4baa05c74da682e19ca7cc7766",
            "Executed serializer is the corrected version reviewed before execution")
    expected_ledger = {
        "ledger_prior_rows": len(prior_rows), "ledger_final_rows": len(all_rows), "ledger_rows_added": len(rows),
        "ledger_prior_bytes": len(prefix), "ledger_prior_sha256": digest(prefix),
        "ledger_append_bytes": len(append), "ledger_append_sha256": digest(append), "ledger_final_sha256": digest(ledger),
    }
    for key, expected in expected_ledger.items():
        require(actuals[key] == expected, "Actuals ledger field verified: " + key)
    integrity_expected = {
        "status": "pass", "prior_rows": len(prior_rows), "rows_added": len(rows), "final_rows": len(all_rows),
        "prior_bytes_preserved": len(prefix), "prior_sha256": digest(prefix), "append_sha256": digest(append),
        "final_sha256": digest(ledger), "prior_bytes_equal": True, "observed_time_exactly_partitioned": True,
        "exclusions_contained_and_nonoverlapping": True, "clock_stopped": True,
    }
    require(integrity == integrity_expected, "Serializer integrity record independently reconciles in full")
    require(actuals["source_commit"] == baseline["head"] and actuals["gate_d"] == "UNATTEMPTED",
            "Entry commit and unattempted Gate D disposition are preserved")
    require("uncredited" in actuals["final_administrative_tail"], "After-stop administrative audit/publication tail is explicitly uncredited")
    source(Path(__file__))
    result = {
        "schema": "F17-postappend-independent-accounting-audit-v1",
        "status": "PASS_NUMERIC_AND_BYTE_INTEGRITY",
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "review_kind": "Same-model internal independent reconstruction; not independent external review",
        "credited_minutes": 0,
        "executed_serializer": False, "edited_ledger": False, "scientific_stages_or_tests_executed": False,
        "checks_passed": len(CHECKS), "checks": CHECKS,
        "ledger": {**expected_ledger, "final_bytes": len(ledger), "prior_bytes_equal_git_entry": True},
        "clock": {"events": len(events), "raw_segments": len(segments), "effective_intervals": len(effective),
                  "excluded_intervals": len(exclusions), "start_utc": events[0]["utc"],
                  "close_utc": events[-1]["utc"], "elapsed_ns": elapsed, "engaged_ns": engaged,
                  "excluded_ns": excluded, "research_ns": research, "mode_and_exclusion_ns": totals,
                  "lane_ns": lanes, "engaged_minutes_decimal": minutes(engaged),
                  "research_minutes_decimal": minutes(research), "excluded_minutes_decimal": minutes(excluded),
                  "max_credited_observation_gap_ns": max_observed_gap, "research_cutoff_monotonic_ns": research_cutoff},
        "forecast_rows": forecast_rows,
        "post_b_1": {"entry_minutes_decimal": forecast["post_b_1_entry_minutes"],
                     "close_minutes_decimal": decimal80(close_exact),
                     "declared_remaining_minutes_decimal": actuals["post_b_1"]["remaining_minutes_decimal"],
                     "unrounded_rational_remaining_rounded80": decimal80(960 - close_exact),
                     "derived_remaining_display_error_minutes_decimal": decimal80(close_remaining_display_error)},
        "checkpoint_reconciliation": {
            "declared_content_boundary_utc": boundary_event["utc"], "F17_engaged_ns": boundary_engaged,
            "cumulative_minutes_decimal": decimal80(boundary_cumulative),
            "boundary_to_close_engaged_ns": tail_ns, "boundary_to_close_O_minutes_decimal": minutes(tail_ns),
            "first_observed_event_at_or_above_960": first_above,
            "first_observed_event_cumulative_minutes_decimal": decimal80(first_above_cumulative),
            "derived_overshoot_display_error_minutes_decimal": decimal80(boundary_overshoot_display_error),
            "interpretation": "17:41:06 is the explicitly declared complete report-content boundary, not the first observed clock check above 960. An earlier 17:37:08 check was already above 960. TODO requires the first chunk boundary; raw clock records alone do not establish which administrative check is a completed content chunk. This distinction is recorded without changing either cutoff or the exact carry.",
        },
        "source_bindings": SOURCES,
        "limits": ["Numeric reconciliation cannot establish cognitive engagement independently of observed task notes.",
                   "This audit verifies ledger, clocks, checkpoint arithmetic and input hashes; it does not repeat scientific stages or scientific tests.",
                   "All time after the principal stop, including this audit, is uncredited."],
    }
    with OUTPUT.open("x") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "checks_passed": result["checks_passed"],
                      "engaged_minutes_decimal": minutes(engaged), "ledger_final_sha256": digest(ledger),
                      "output": str(OUTPUT.relative_to(REPO)), "output_sha256": digest(OUTPUT.read_bytes())}))


if __name__ == "__main__":
    main()
