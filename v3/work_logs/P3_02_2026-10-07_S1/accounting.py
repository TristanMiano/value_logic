"""Conservative P3-02 accounting; ChatGPT (GPT-6 Astra Pro), 2026-10-07.

preview/snapshot are read-only and count CLOSED effective observations only.
finalize is an explicit, single append after the principal clock has stopped.
It does not decide scientific completion, contribution support or a gate.
No raw record is edited; failed or partial finalization requires inspection.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True
import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LEDGER = REPO / "v3/time_ledger.csv"
TASK, ATTEMPT, SESSION = "P3-02", "P3-02-1", "2026-10-07-S1"
ARTIFACT = "v3/work_logs/P3_02_2026-10-07_S1.md"
MODES = ("D", "L", "E", "O", "wait", "idle", "unmeasured", "recovery")
RESEARCH, ENGAGED = {"D", "L", "E"}, {"D", "L", "E", "O"}
EXCLUDED = set(MODES) - ENGAGED
NS_SECOND, NS_MINUTE = 1_000_000_000, 60_000_000_000
TASK_FLOOR, PHASE_FLOOR, CADENCE = 90*NS_MINUTE, 960*NS_MINUTE, 15*NS_MINUTE
INPUTS = ("baseline.json", "forecast.json", "attempt_started.json", "environment.json",
          "clock.py", "clocks.jsonl", "segments.jsonl", "clock_dispositions.jsonl",
          "clock_state.json", "accounting.py", "verify_close.py")
FIELDS = ("task_id", "attempt_id", "session_id", "mode", "lane", "start_utc",
          "end_utc", "elapsed_seconds", "engaged_seconds", "tool_wait_seconds",
          "idle_seconds", "unmeasured_seconds", "forecast_seconds", "artifact", "status")
MUTABLE_OLD_V3 = {"v3/README.md", "v3/claim_ledger.md", "v3/plan.v1.json", "v3/time_ledger.csv"}


class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dumps(value):
    return json.dumps(value, indent=2, sort_keys=True, default=str, allow_nan=False) + "\n"


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, f"Duplicate JSON key: {key}")
        obj[key] = value
    return obj


def parse(data):
    def bad_constant(value):
        raise AuditError("Nonfinite JSON constant: " + value)
    return json.loads(data, parse_float=Decimal, parse_constant=bad_constant,
                      object_pairs_hook=unique_object)


def records(data):
    require(not data or data.endswith(b"\n"), "Unterminated JSONL record; preserve and inspect")
    return [parse(line) for line in data.splitlines() if line.strip()]


def integer(value, name):
    require(type(value) is int and value >= 0, f"{name} must be nonnegative integer nanoseconds")
    return value


def exact_ns(value, unit=NS_SECOND):
    require(not isinstance(value, (float, bool)), "Use exact decimal text/integer, not binary float")
    number = Decimal(value)
    require(number.is_finite() and number >= 0, "Nonnegative finite quantity required")
    numerator, denominator = number.as_integer_ratio()
    require((numerator*unit) % denominator == 0, "Quantity is not an exact number of nanoseconds")
    return numerator*unit//denominator


def seconds(ns):
    sign = "-" if ns < 0 else ""
    whole, fraction = divmod(abs(ns), NS_SECOND)
    return f"{sign}{whole}.{fraction:09d}"


def minutes(ns):
    with localcontext() as context:
        context.prec = 60
        return format(Decimal(ns)/NS_MINUTE, ".12f")


def ratio(numerator, denominator):
    if denominator == 0:
        return None
    with localcontext() as context:
        context.prec = 60
        return format(Decimal(numerator)/Decimal(denominator), ".12f")


def category(mode, lane):
    require(mode in MODES, f"Unknown mode: {mode}")
    require(lane in ("R", "X") if mode in RESEARCH else lane == "",
            f"Invalid mode/lane: {mode}/{lane}")


def checked_utc(value):
    require(isinstance(value, str), "UTC must be a string")
    dt = datetime.fromisoformat(value)
    require(dt.tzinfo is not None and dt.utcoffset().total_seconds() == 0, "Explicit UTC required")
    return dt


def snapshot():
    def names():
        extra = [p.name for pattern in ("progress_*.json", "remaining_forecast_*.json")
                 for p in HERE.glob(pattern)]
        return sorted(set(INPUTS) | set(extra))
    first_names = names()
    first = {name: (HERE/name).read_bytes() for name in first_names}
    second_names = names()
    second = {name: (HERE/name).read_bytes() for name in second_names}
    require(first_names == second_names and first == second,
            "Live inputs changed during read; rerun the read-only snapshot")
    return first


def replay(events, raw, state):
    require(events and events[0]["command"] == "start", "Missing original start event")
    active, rebuilt, anchors, gaps = None, [], {}, []
    runtime, previous_ns, previous_utc = events[0]["runtime"], -1, None
    for index, event in enumerate(events):
        ns = integer(event["monotonic_ns"], "event monotonic_ns")
        utc, command, args = event["utc"], event["command"], event["args"]
        dt = checked_utc(utc)
        require(ns > previous_ns, "Repeated or reversed clock observations")
        require(previous_utc is None or dt >= previous_utc, "UTC reversed; requires explicit reconciliation")
        require(event["runtime"] == runtime, "Mixed runtimes cannot be subtracted")
        require(isinstance(args, list) and all(isinstance(x, str) for x in args), "Invalid event args")
        require(command in {"start", "switch", "resume", "pause", "check", "stop"}, "Unknown clock command")
        if index and active is None:
            gaps.append(dict(start_monotonic_ns=previous_ns, end_monotonic_ns=ns,
                             start_utc=events[index-1]["utc"], end_utc=utc, elapsed_ns=ns-previous_ns))
        anchors[ns] = utc
        previous_ns, previous_utc = ns, dt
        if command == "start":
            require(index == 0 and active is None, "Attempt was restarted")
        elif command == "resume":
            require(active is None or active["mode"] in EXCLUDED, "Resume from engaged work")
        else:
            require(active is not None, f"{command} without an open interval")
        if command == "check":
            continue
        if active is not None:
            rebuilt.append(dict(active, end_utc=utc, end_monotonic_ns=ns,
                                elapsed_ns=ns-active["start_monotonic_ns"]))
        if command == "stop":
            active = None
            continue
        if command in {"start", "switch", "resume"}:
            require(len(args) >= 3, "Mode, lane and durable note required")
            mode, lane, *note = args
            require(mode in ENGAGED, "Invalid active mode")
            lane = "" if lane == "-" else lane
        else:
            require(len(args) >= 2, "Pause mode and note required")
            mode, *note = args
            require(mode in EXCLUDED, "Invalid excluded mode")
            lane = ""
        category(mode, lane)
        active = dict(mode=mode, lane=lane, note=" ".join(note), start_utc=utc,
                      start_monotonic_ns=ns, runtime=runtime)
    require(rebuilt == raw, "Raw segments differ from exact event replay")
    require(active == state, "Clock state differs from exact event replay")
    return runtime, anchors, gaps


def effective_segments(raw, corrections, runtime, anchors):
    """The current clock.py split semantics, with additional rejection checks."""
    ids = set()
    ordered = sorted(corrections, key=lambda c: c["start_monotonic_ns"])
    for left, right in zip(ordered, ordered[1:]):
        require(left["end_monotonic_ns"] <= right["start_monotonic_ns"], "Overlapping dispositions")
    for correction in corrections:
        start = integer(correction["start_monotonic_ns"], "disposition start")
        end = integer(correction["end_monotonic_ns"], "disposition end")
        require(start < end, "Empty/reversed disposition")
        require(isinstance(correction["id"], str) and correction["id"] not in ids, "Repeated disposition id")
        ids.add(correction["id"])
        require(correction["runtime"] == runtime, "Disposition runtime mismatch")
        category(correction["mode"], correction["lane"])
        matches = [s for s in raw if s["start_monotonic_ns"] <= start < end <= s["end_monotonic_ns"]]
        require(len(matches) == 1 and matches[0]["mode"] == correction["original_mode"],
                "Disposition must lie in exactly one closed original-mode interval")
        require(not (matches[0]["mode"] in EXCLUDED and correction["mode"] in ENGAGED),
                "An excluded interval cannot acquire engaged credit through this helper")
        require(anchors.get(start) == correction["start_utc"] and anchors.get(end) == correction["end_utc"],
                "Disposition boundary lacks a matching saved UTC/monotonic observation")
        require(isinstance(correction["reason"], str) and correction["reason"].strip(), "Disposition lacks reason")
    result = []
    for index, segment in enumerate(raw):
        start, end = segment["start_monotonic_ns"], segment["end_monotonic_ns"]
        require(type(start) is int and type(end) is int and start < end, "Invalid raw interval")
        require(type(segment["elapsed_ns"]) is int and segment["elapsed_ns"] == end-start, "Raw elapsed mismatch")
        category(segment["mode"], segment["lane"])
        applicable = [c for c in corrections if start <= c["start_monotonic_ns"] < c["end_monotonic_ns"] <= end]
        points = sorted({start, end} | {c[k] for c in applicable
                                       for k in ("start_monotonic_ns", "end_monotonic_ns")})
        for a, b in zip(points, points[1:]):
            part = dict(segment, raw_segment_index=index, start_monotonic_ns=a, end_monotonic_ns=b,
                        start_utc=anchors[a], end_utc=anchors[b], elapsed_ns=b-a)
            covering = [c for c in applicable if c["start_monotonic_ns"] <= a and b <= c["end_monotonic_ns"]]
            require(len(covering) <= 1, "Ambiguous disposition")
            if covering:
                correction = covering[0]
                part.update(mode=correction["mode"], lane=correction["lane"],
                            note=correction["reason"], disposition_id=correction["id"])
            result.append(part)
    require(sum(p["elapsed_ns"] for p in result) == sum(s["elapsed_ns"] for s in raw), "Split lost elapsed time")
    for left, right in zip(result, result[1:]):
        require(left["end_monotonic_ns"] <= right["start_monotonic_ns"], "Duplicate/concurrent interval credit")
    return result


def git(*args):
    result = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True)
    require(result.returncode == 0, "Git read failed: " + result.stderr.decode("utf-8", "replace"))
    return result.stdout


def preservation(baseline):
    require((baseline["task"], baseline["attempt"], baseline["session"]) == (TASK, ATTEMPT, SESSION), "Baseline identity mismatch")
    meta = baseline["files"]["v3/time_ledger.csv"]
    current = LEDGER.read_bytes()
    prefix = current[:meta["bytes"]]
    require(len(prefix) == meta["bytes"] and digest(prefix) == meta["sha256"], "Prior v3 ledger bytes/hash changed")
    require(prefix.endswith(b"\n"), "Prior ledger prefix is incomplete")
    reader = csv.DictReader(io.StringIO(prefix.decode("utf-8")))
    require(tuple(reader.fieldnames or ()) == FIELDS, "Unexpected ledger schema")
    rows = list(reader)
    research, engaged, prior_task = 0, 0, 0
    for row in rows:
        require(set(row) == set(FIELDS) and all(value is not None for value in row.values()), "Malformed prior ledger row")
        require(row["attempt_id"] != ATTEMPT, "Current attempt already present in immutable baseline")
        category(row["mode"], row["lane"])
        elapsed, active = exact_ns(row["elapsed_seconds"]), exact_ns(row["engaged_seconds"])
        require(active + sum(exact_ns(row[k]) for k in
                            ("tool_wait_seconds", "idle_seconds", "unmeasured_seconds")) == elapsed,
                "Prior row does not partition elapsed time")
        engaged += active
        if row["mode"] in RESEARCH:
            require(active == elapsed, "Prior research row has mixed credit")
            research += active
            if row["task_id"] == TASK:
                prior_task += active
    require(research == integer(baseline["prior_phase3_research_ns"], "prior research"), "Prior research total differs")
    require(engaged == integer(baseline["prior_phase3_engaged_ns"], "prior engaged"), "Prior engaged total differs")
    require(prior_task == integer(baseline["prior_task_research_ns"], "prior task"), "Prior task total differs")
    retained = {}
    for name, expected in baseline["files"].items():
        if name == "v3/time_ledger.csv":
            continue
        data = (REPO/name).read_bytes()
        require(len(data) == expected["bytes"] and digest(data) == expected["sha256"], "Preserved baseline file changed: " + name)
        retained[name] = dict(bytes=len(data), sha256=digest(data))
    source = baseline["source_commit"]
    require(re.fullmatch(r"[0-9a-f]{40}", source) is not None, "Invalid baseline source commit")
    require(git("show", source+":v3/time_ledger.csv") == prefix,
            "Ledger baseline prefix differs from the preserved source commit")
    immutable = {}
    for record in git("ls-tree", "-r", "-z", source, "--", "v3").split(b"\0"):
        if not record:
            continue
        header, encoded_name = record.split(b"\t", 1)
        mode, kind, oid = header.decode().split()
        name = encoded_name.decode()
        if name in MUTABLE_OLD_V3:
            continue
        require(kind == "blob" and mode in {"100644", "100755"}, "Unexpected old v3 object type: " + name)
        data = (REPO/name).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == oid, "Immutable pre-P3-02 file changed: " + name)
        immutable[name] = dict(bytes=len(data), sha256=digest(data), source_blob=oid)
    phase2_diff = git("diff", "--name-only", source, "--", "v2", "TODO_v2.md", "paper_v2.md").decode().splitlines()
    require(not phase2_diff, "Tracked phase-two content changed: " + ", ".join(phase2_diff))
    proof = dict(source_commit=source, prior_ledger_prefix_bytes=len(prefix),
                 prior_ledger_prefix_sha256=digest(prefix), prior_ledger_rows=len(rows),
                 prefix_preserved=True, baseline_files=retained,
                 immutable_old_v3_files=immutable, immutable_old_v3_count=len(immutable),
                 phase2_tracked_diff=[], phase2_ledger_sha256=retained["v2/time_ledger.csv"]["sha256"])
    return prefix, current, rows, research, engaged, prior_task, proof


def forecast_audit(forecast):
    require((forecast["task"], forecast["attempt"]) == (TASK, ATTEMPT), "Forecast identity mismatch")
    require(forecast["principal_time_only"] is True and set(forecast["qualifying_modes"]) == RESEARCH,
            "Forecast must count principal D+L+E only")
    require(exact_ns(forecast["protected_research_minutes"], NS_MINUTE) == TASK_FLOOR, "Research90 floor changed")
    for level in ("central_minutes", "high_minutes"):
        require(set(forecast[level]) == ENGAGED, "Forecast D/L/E/O keys mismatch")
        for value in forecast[level].values():
            exact_ns(value, NS_MINUTE)
    lanes = {k: Decimal(v) for k, v in forecast["lane_fraction"].items()}
    require(set(lanes) == {"R", "X"} and sum(lanes.values()) == 1
            and all(0 <= v <= 1 for v in lanes.values()), "Invalid prospective R/X fractions")
    waits = forecast["expected_excluded_wait_minutes"]
    require(set(waits) == {"central", "high"}, "Expected wait forecasts missing")
    return {level: {**{m: exact_ns(forecast[level+"_minutes"][m], NS_MINUTE) for m in ENGAGED},
                    "wait": exact_ns(waits[level], NS_MINUTE)} for level in ("central", "high")}


def forecast_comparison(actual, planned):
    result = {}
    for level, values in planned.items():
        expanded = dict(values, research=sum(values[m] for m in RESEARCH),
                        engaged=sum(values[m] for m in ENGAGED))
        result[level] = {mode: dict(forecast_ns=ns, actual_ns=actual[mode],
                                   actual_minus_forecast_ns=actual[mode]-ns,
                                   actual_minus_forecast_minutes=minutes(actual[mode]-ns),
                                   actual_over_forecast=ratio(actual[mode], ns))
                         for mode, ns in expanded.items()}
    return result


def render_rows(parts, forecast):
    used, buffer = set(), io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    for part in parts:
        mode, lane, ns = part["mode"], part["lane"], part["elapsed_ns"]
        planned = ""
        if mode in ENGAGED and mode not in used:
            planned = seconds(exact_ns(forecast["central_minutes"][mode], NS_MINUTE))
            used.add(mode)
        row = dict(task_id=TASK, attempt_id=ATTEMPT, session_id=SESSION,
                   mode=mode if mode in ENGAGED else "O", lane=lane,
                   start_utc=part["start_utc"], end_utc=part["end_utc"],
                   elapsed_seconds=seconds(ns), engaged_seconds=seconds(ns if mode in ENGAGED else 0),
                   tool_wait_seconds=seconds(ns if mode == "wait" else 0),
                   idle_seconds=seconds(ns if mode == "idle" else 0),
                   unmeasured_seconds=seconds(ns if mode in {"unmeasured", "recovery"} else 0),
                   forecast_seconds=planned, artifact=ARTIFACT,
                   status="Closed P3-02 observation; scientific completion not inferred; P3-A/later tasks unattempted; "
                          + mode + "; " + (part["disposition_id"]+"; " if "disposition_id" in part else "") + part["note"])
        require(sum(exact_ns(row[k]) for k in ("engaged_seconds", "tool_wait_seconds", "idle_seconds", "unmeasured_seconds")) == ns,
                "Proposed ledger row does not partition elapsed time")
        writer.writerow(row)
    return buffer.getvalue().encode("utf-8")


def audit():
    inputs = snapshot()
    baseline, forecast, state = [parse(inputs[name]) for name in ("baseline.json", "forecast.json", "clock_state.json")]
    marker = parse(inputs["attempt_started.json"])
    require((marker["task"], marker["attempt"], marker["source_commit"]) == (TASK, ATTEMPT, baseline["source_commit"]),
            "Attempt marker identity mismatch")
    planned = forecast_audit(forecast)
    events, raw, corrections = [records(inputs[name]) for name in ("clocks.jsonl", "segments.jsonl", "clock_dispositions.jsonl")]
    runtime, anchors, gaps = replay(events, raw, state)
    parts = effective_segments(raw, corrections, runtime, anchors)
    prefix, current, prior_rows, prior_research, prior_engaged, prior_task, retained = preservation(baseline)
    totals = {m: sum(p["elapsed_ns"] for p in parts if p["mode"] == m) for m in MODES}
    lane_ns = {lane: sum(p["elapsed_ns"] for p in parts if p["lane"] == lane) for lane in ("R", "X")}
    research, engaged = sum(totals[m] for m in RESEARCH), sum(totals[m] for m in ENGAGED)
    excluded = sum(totals[m] for m in EXCLUDED)
    require(sum(lane_ns.values()) == research, "Research and lane totals differ")
    # Compare credit intervals only. UTC is not used to calculate durations.
    for part in parts:
        if part["mode"] not in ENGAGED:
            continue
        start, end = checked_utc(part["start_utc"]), checked_utc(part["end_utc"])
        for row in prior_rows:
            if exact_ns(row["engaged_seconds"]) and start < checked_utc(row["end_utc"]) and checked_utc(row["start_utc"]) < end:
                raise AuditError("New credit overlaps an immutable prior engaged interval")
    observation_windows = []
    for left, right in zip(events, events[1:]):
        a, b = left["monotonic_ns"], right["monotonic_ns"]
        active = sum(max(0, min(b, p["end_monotonic_ns"])-max(a, p["start_monotonic_ns"]))
                     for p in parts if p["mode"] in ENGAGED)
        observation_windows.append(dict(start_monotonic_ns=a, end_monotonic_ns=b, closed_engaged_ns=active))
    violations = [w for w in observation_windows if w["closed_engaged_ns"] > CADENCE]
    prior_attempts = list(dict.fromkeys(row["attempt_id"] for row in prior_rows if row["mode"] in RESEARCH))
    previous_attempt = prior_attempts[-1] if prior_attempts else None
    previous_lanes = {lane: sum(exact_ns(row["engaged_seconds"]) for row in prior_rows
                               if row["attempt_id"] == previous_attempt and row["mode"] in RESEARCH and row["lane"] == lane)
                      for lane in ("R", "X")}
    combined_lanes = {lane: previous_lanes[lane]+lane_ns[lane] for lane in ("R", "X")}
    combined_total = sum(combined_lanes.values())
    progress_records, remaining_comparisons = {}, {}
    for name, data in inputs.items():
        if not name.startswith("progress_"):
            continue
        progress = parse(data)
        through = integer(progress["through_monotonic_ns"], "progress cutoff")
        require(through in anchors, "Progress cutoff is not a saved clock observation")
        upto = {m: sum(max(0, min(through, p["end_monotonic_ns"])-p["start_monotonic_ns"])
                       for p in parts if p["mode"] == m) for m in MODES}
        recorded = progress["closed_mode_ns"]
        progress_records[name] = dict(through_monotonic_ns=through, recorded_category_ns=recorded,
                                     current_effective_category_ns=upto,
                                     unchanged_by_later_dispositions=recorded == upto, separately_credited_ns=0)
    for name, data in inputs.items():
        if not name.startswith("remaining_forecast_"):
            continue
        revision = parse(data)
        progress_name = revision["based_on_progress"]
        require(progress_name in progress_records, "Remaining forecast lacks its preserved progress record")
        through = progress_records[progress_name]["through_monotonic_ns"]
        since = {m: sum(max(0, p["end_monotonic_ns"]-max(through, p["start_monotonic_ns"]))
                        for p in parts if p["mode"] == m) for m in MODES}
        since.update(research=sum(since[m] for m in RESEARCH), engaged=sum(since[m] for m in ENGAGED))
        revised = {level: {**{m: exact_ns(revision[level+"_minutes"][m], NS_MINUTE) for m in ENGAGED},
                           "wait": exact_ns(revision[level+"_minutes"]["expected_waits"], NS_MINUTE)}
                   for level in ("central", "high")}
        remaining_comparisons[name] = dict(based_on_progress=progress_name, cutoff_monotonic_ns=through,
                                           comparison=forecast_comparison(since, revised), separately_credited_ns=0)
    append = render_rows(parts, forecast)
    relation = ("original_prefix_only" if current == prefix else
                "already_matches_this_attempt_append" if current == prefix+append else "other_or_partial_suffix_preserved")
    blockers = []
    if state is not None:
        blockers.append("principal_clock_open")
    if prior_task+research < TASK_FLOOR:
        blockers.append("protected_research_floor_not_met")
    if violations:
        blockers.append("engaged_observation_gap_over_15_minutes")
    if gaps:
        blockers.append("stopped_gaps_need_explicit_separate_disposition")
    if relation != "original_prefix_only":
        blockers.append(relation)
    for name in ("actuals.json", "ledger_append.csv", "accounting.finalize.lock"):
        if (HERE/name).exists():
            blockers.append("existing_"+name)
    attempts = HERE/"accounting_attempts"
    if attempts.exists() and any(attempts.iterdir()):
        blockers.append("existing_accounting_attempts_require_inspection")
    phase_research, phase_engaged = prior_research+research, prior_engaged+engaged
    actual_modes = dict(totals, research=research, engaged=engaged)
    payload = dict(schema="value_logic.P3-02.accounting.v1", task=TASK, attempt=ATTEMPT, session=SESSION,
                   contributor="ChatGPT (GPT-6 Astra Pro)", principal_time_only=True,
                   task_completion_or_contribution_or_gate_pass_inferred=False,
                   extra_agent_time_credited_ns=0, open_time_credited_ns=0,
                   exact_units="integer nanoseconds; exact fixed-nine-place seconds; minutes/fractions are display-rounded to 12 places",
                   runtime=runtime, open_segment=state, first_observation_utc=events[0]["utc"],
                   last_observation_utc=events[-1]["utc"], closed_raw_segments=len(raw),
                   closed_effective_segments=len(parts), disposition_count=len(corrections),
                   raw_clock_events=events, raw_segments=raw, raw_dispositions=corrections, effective_segments=parts,
                   category_ns=totals, category_seconds={m: seconds(n) for m, n in totals.items()},
                   category_minutes={m: minutes(n) for m, n in totals.items()}, lane_research_ns=lane_ns,
                   lane_research_fraction={m: ratio(n, research) for m, n in lane_ns.items()},
                   research_ns=research, research_seconds=seconds(research), research_minutes=minutes(research),
                   engaged_ns=engaged, engaged_seconds=seconds(engaged), engaged_minutes=minutes(engaged),
                   excluded_ns=excluded, excluded_minutes=minutes(excluded), observed_closed_ns=engaged+excluded,
                   prior_task_research_ns=prior_task, task_research_ns=prior_task+research,
                   protected_research_ns=TASK_FLOOR, protected_research_floor_met=prior_task+research >= TASK_FLOOR,
                   remaining_task_research_ns=max(0, TASK_FLOOR-prior_task-research),
                   research_floor_overshoot_ns=max(0, prior_task+research-TASK_FLOOR),
                   prior_phase3_research_ns=prior_research, prior_phase3_engaged_ns=prior_engaged,
                   phase3_research_ns=phase_research, phase3_engaged_ns=phase_engaged,
                   phase3_research_minutes=minutes(phase_research), phase3_engaged_minutes=minutes(phase_engaged),
                   phase3_research_floor_ns=PHASE_FLOOR, phase3_research_floor_met=phase_research >= PHASE_FLOOR,
                   remaining_phase3_research_ns=max(0, PHASE_FLOOR-phase_research),
                   remaining_phase3_research_minutes=minutes(max(0, PHASE_FLOOR-phase_research)),
                   phase_checkpoints=[dict(minutes=m, reached=phase_research >= m*NS_MINUTE,
                                           crossed_this_attempt=prior_research < m*NS_MINUTE <= phase_research,
                                           overshoot_ns=max(0, phase_research-m*NS_MINUTE)) for m in (240, 480, 960)],
                   cadence=dict(limit_ns=CADENCE, maximum_closed_engaged_between_observations_ns=max(
                       (w["closed_engaged_ns"] for w in observation_windows), default=0),
                       violations=violations, open_interval_not_credited=True),
                   uncredited_stopped_gaps=gaps,
                   two_research_attempt_lane_window=dict(previous_attempt=previous_attempt, current_attempt=ATTEMPT,
                       previous_lane_ns=previous_lanes, combined_lane_ns=combined_lanes,
                       fractions={m: ratio(n, combined_total) for m, n in combined_lanes.items()},
                       at_least_25_percent_each=bool(combined_total) and all(4*n >= combined_total for n in combined_lanes.values()),
                       scope="Diagnostic using the last two research attempts; any different cycle definition or documented exception requires explicit review, not automatic relabeling."),
                   forecast=forecast, forecast_actual_comparison=forecast_comparison(actual_modes, planned),
                   progress_snapshots=progress_records, remaining_forecast_actual_comparisons=remaining_comparisons,
                   preservation=retained, ledger_relation=relation,
                   proposed_append_sha256=digest(append), proposed_append_bytes=len(append),
                   input_files={name: dict(bytes=len(data), sha256=digest(data)) for name, data in inputs.items()},
                   accounting_script_sha256=digest(inputs["accounting.py"]), finalize_blockers=blockers)
    require(snapshot() == inputs and LEDGER.read_bytes() == current, "Inputs or ledger changed during audit")
    return payload, inputs, prefix, append


def sync_directory(path):
    if os.name == "posix":
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def exclusive_write(path, data):
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    sync_directory(path.parent)


def finalize():
    payload, inputs, prefix, append = audit()
    require(not payload["finalize_blockers"], "Finalization refused: " + ", ".join(payload["finalize_blockers"]))
    lock = HERE/"accounting.finalize.lock"
    exclusive_write(lock, dumps(dict(pid=os.getpid(), attempt=ATTEMPT,
                                    utc=datetime.now(timezone.utc).isoformat())).encode())
    attempts = HERE/"accounting_attempts"
    attempts.mkdir(exist_ok=True)
    attempt_dir = attempts/"attempt0001"
    attempt_dir.mkdir()
    sync_directory(attempts)
    try:
        exclusive_write(attempt_dir/"prepared.json", dumps(payload).encode())
        exclusive_write(attempt_dir/"ledger_append.csv", append)
        require(snapshot() == inputs and LEDGER.read_bytes() == prefix, "Inputs/ledger changed before append")
        preservation(parse(inputs["baseline.json"]))
        exclusive_write(HERE/"ledger_append.csv", append)
        with LEDGER.open("ab", buffering=0) as stream:
            if os.name == "posix":
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            require(os.fstat(stream.fileno()).st_size == len(prefix), "Ledger size changed before append")
            require(LEDGER.read_bytes() == prefix, "Ledger bytes changed before append")
            require(stream.write(append) == len(append), "Short append: preserve bytes and inspect")
            os.fsync(stream.fileno())
        require(LEDGER.read_bytes() == prefix+append, "Concurrent/partial suffix: preserve and reconcile manually")
        require(snapshot() == inputs, "Clock/forecast inputs changed during finalization")
        preservation(parse(inputs["baseline.json"]))
        payload.update(finalized=True, finalized_utc=datetime.now(timezone.utc).isoformat(),
                       ledger_after_sha256=digest(prefix+append), ledger_after_bytes=len(prefix+append),
                       ledger_rows_appended=len(payload["effective_segments"]),
                       ledger_relation="finalized_exact_append", finalize_blockers=[],
                       post_stop_administration_credited_ns=0)
        exclusive_write(HERE/"actuals.json", dumps(payload).encode())
        exclusive_write(attempt_dir/"result.json", dumps(dict(status="finalized",
                        actuals_sha256=digest((HERE/"actuals.json").read_bytes()))).encode())
        lock.unlink()
        sync_directory(HERE)
        return payload
    except Exception as error:
        failure = attempt_dir/"failure.json"
        if not failure.exists():
            exclusive_write(failure, dumps(dict(error=type(error).__name__, message=str(error),
                            utc=datetime.now(timezone.utc).isoformat(), automatic_retry=False)).encode())
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preview", "snapshot", "finalize"), nargs="?", default="preview")
    parser.add_argument("--summary", action="store_true", help="Print totals/blockers without full raw/provenance arrays")
    args = parser.parse_args()
    try:
        payload = finalize() if args.command == "finalize" else audit()[0]
        if args.summary:
            keys = ("task", "attempt", "research_ns", "research_minutes", "engaged_minutes", "excluded_minutes",
                    "category_minutes", "lane_research_fraction", "remaining_task_research_ns",
                    "phase3_research_minutes", "remaining_phase3_research_minutes", "protected_research_floor_met",
                    "cadence", "two_research_attempt_lane_window", "ledger_relation", "finalize_blockers")
            payload = {key: payload[key] for key in keys}
        print(dumps(payload), end="")
        return 0
    except (AuditError, OSError, ValueError, KeyError, TypeError, ArithmeticError) as error:
        print(dumps(dict(error=type(error).__name__, message=str(error), automatic_retry=False)), file=sys.stderr, end="")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
