"""Append F15 accounting after the principal has explicitly stopped its clock.

Prepared by delegated ChatGPT (GPT-6 Astra Pro), execution audit; adapted from
F14's serializer. Administrative code outside the experimental freeze.

This program never stops/starts a clock, edits raw records or documents, runs
an experiment, or credits its own administration. --dry-run performs all
validation on a CLOSED clock with E60 satisfied and writes nothing. Normal
execution is one-shot: existing F15 ledger rows or any finalization output
cause refusal. If interrupted after writing the durable intent, inspect that
intent and the ledger rather than blindly rerunning or deleting evidence.

Timing arithmetic uses observed monotonic integer nanoseconds. Decimal text
of an exclusion may contain binary-float serialization noise; conversion to
the clock's nanosecond resolution records every nonzero normalization delta.
No minute/second rounding is used to satisfy E60.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN
import fcntl
import hashlib
import io
import json
import math
import os
from pathlib import Path


SESSION = Path(__file__).resolve().parent
REPO = SESSION.parents[2]
LEDGER = REPO / "v2/time_ledger.csv"
SOURCE = "5388a3f9b0f18ad4f4e33d7e0cd04ea38f03e43e"
BASELINE_BYTES = 203501
BASELINE_SHA256 = "7f777f89e0aff82d58752d0b1774c30e015fe9f3dbbf4faa1caae9b35c49988f"
FORECAST_SHA256 = "415041ebd29375da25919f3a281a7414b2b61ace613b818d3101d92da06b5b0f"
NS = 1_000_000_000
MINUTE_NS = 60 * NS
ENTRY = Decimal("636.727190")
INHERITED_OVERSHOOT = Decimal("54.976816")
CHECKPOINT = Decimal("960")
CENTRAL = {"D": 10, "L": 0, "E": 90, "O": 20, "engaged": 120, "wait": 5}
HIGH = {"D": 20, "L": 10, "E": 180, "O": 30, "engaged": 240, "wait": 20}
RESEARCH = ("D", "L", "E")
ENGAGED = (*RESEARCH, "O")
MODES = (*ENGAGED, "wait", "recovery")
INPUT_NAMES = ("clock_state.json", "clocks.jsonl", "segments.jsonl", "adjustments.jsonl",
               "recovery_exclusions.jsonl", "mode_reclassifications.jsonl",
               "forecast.json", "ledger_baseline.json", "clock.py")
OUTPUT_NAMES = ("actuals.json", "ledger_integrity.json", "finalization_intent.json")
HEADER = ["task_id", "attempt_id", "session_id", "mode", "lane", "start_utc", "end_utc",
          "elapsed_seconds", "engaged_seconds", "tool_wait_seconds", "idle_seconds",
          "unmeasured_seconds", "forecast_seconds", "artifact", "status"]


def require(condition, message):
    # Explicit checks remain active even if Python is launched with -O.
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load(data):
    def reject(value):
        raise ValueError(f"Nonfinite JSON constant: {value}")
    def finite_float(value):
        parsed = float(value)
        require(math.isfinite(parsed), f"Nonfinite JSON number: {value}")
        return parsed
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=reject,
                      parse_float=finite_float)


def lines(data, name):
    decoded = data.decode("utf-8").splitlines()
    require(all(line.strip() for line in decoded), f"Blank record in {name}")
    return [load(line) for line in decoded]


def utc(value):
    parsed = datetime.fromisoformat(value)
    require(parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0,
            f"Expected recorded UTC timestamp: {value}")
    return parsed


def seconds_text(value_ns):
    require(type(value_ns) is int and value_ns >= 0, "Negative/noninteger duration")
    return f"{value_ns // NS}.{value_ns % NS:09d}"


def validate_segments(segments, events):
    require(bool(segments) and bool(events), "No observed principal segments/events")
    expected, state = [], None
    previous_event_ns = None
    last_transition = None
    for event in events:
        now = event["monotonic_ns"]
        require(type(now) is int, "Noninteger event monotonic time")
        require(previous_event_ns is None or now >= previous_event_ns, "Clock events run backward")
        previous_event_ns = now
        require(event["runtime"] == "linux-F15-S1", "Mixed clock runtimes")
        utc(event["utc"])
        command, args = event["command"], event["args"]
        if command == "check":
            continue
        require(command in ("start", "switch", "resume", "pause", "stop"), "Unknown clock transition")
        if state is not None:
            expected.append(dict(state, end_utc=event["utc"], end_monotonic_ns=now))
        if command in ("start", "switch", "resume"):
            require(len(args) >= 2 and args[0] in ENGAGED and args[1] in ("R", "X", "-"), "Malformed clock start")
            state = {"mode": args[0], "lane": "" if args[1] == "-" else args[1],
                     "start_utc": event["utc"], "start_monotonic_ns": now,
                     "note": " ".join(args[2:]), "runtime": event["runtime"]}
        elif command == "pause":
            state = {"mode": "wait", "lane": "", "start_utc": event["utc"],
                     "start_monotonic_ns": now, "note": " ".join(args), "runtime": event["runtime"]}
        else:
            state = None
        last_transition = event
    require(state is None and last_transition is not None and last_transition["command"] == "stop",
            "Raw events do not end at an explicit stopped clock")
    require(len(expected) == len(segments), "Raw segments do not match clock transitions")
    starts = set()
    for index, (segment, replayed) in enumerate(zip(segments, expected)):
        require(all(segment.get(k) == v for k, v in replayed.items()), f"Segment {index} differs from raw transition replay")
        start, end = segment["start_monotonic_ns"], segment["end_monotonic_ns"]
        require(type(start) is int and type(end) is int and end >= start, f"Invalid segment {index} duration")
        require(start not in starts, "Repeated principal segment start")
        starts.add(start)
        require(utc(segment["end_utc"]) >= utc(segment["start_utc"]), "Segment UTC runs backward")
        recorded = Decimal(str(segment["elapsed_seconds"]))
        require(recorded.is_finite() and abs(recorded-Decimal(end-start)/NS) <= Decimal("0.000000001"), "Recorded duration disagrees with monotonic endpoints")
        if index:
            require(start == segments[index-1]["end_monotonic_ns"], "Principal segments have an overlap or unobserved gap; do not infer time")
            require(segment["start_utc"] == segments[index-1]["end_utc"], "Adjacent segment UTC boundaries differ")
    require(segments[-1]["end_monotonic_ns"] == last_transition["monotonic_ns"], "Final stop does not match accounting cutoff")


def build_plan(raw, prior):
    require(load(raw["clock_state.json"]) is None, "Principal clock is open; only the principal may explicitly stop it")
    baseline, forecast = load(raw["ledger_baseline.json"]), load(raw["forecast.json"])
    require(baseline["bytes"] == BASELINE_BYTES and baseline["sha256"] == BASELINE_SHA256, "Baseline declaration changed")
    require(Decimal(str(baseline["POST_B_1_entry_minutes"])) == ENTRY, "POST-B-1 entry changed")
    require(len(prior) == BASELINE_BYTES and sha(prior) == BASELINE_SHA256, "Prior ledger is not the exact recorded baseline")
    require(prior.endswith(b"\n"), "Prior CSV has no terminal newline")
    old_rows = list(csv.reader(io.StringIO(prior.decode("utf-8"), newline="")))
    require(old_rows[0] == HEADER and all(len(row) == len(HEADER) for row in old_rows), "Unexpected prior CSV structure")
    require(not any(row[0].strip() == "F15" for row in old_rows[1:]), "F15 ledger rows already exist; refuse repeated finalization")
    require(sha(raw["forecast.json"]) == FORECAST_SHA256, "Immutable initial forecast bytes changed")
    require(forecast["source_revision"] == SOURCE and forecast["task"] == "F15" and forecast["attempt"] == "F15-A", "Forecast identity changed")
    require(forecast["central_minutes"] == CENTRAL and forecast["high_minutes"] == HIGH, "Forecast allocations changed")
    require(forecast["research_lane_percent"] == {"R": 60, "X": 40}, "Forecast lanes changed")
    require(forecast["protected_E_minutes"] == 60 and forecast["concurrent_agent_minutes_added"] == 0, "Protected E floor or parallel-time contract changed")
    require(Decimal(str(forecast["POST_B_1_entry_minutes"])) == ENTRY and forecast["next_checkpoint_minutes"] == 960, "Forecast cumulative clock changed")
    require(Decimal(str(forecast["remaining_minutes_at_start"])) == CHECKPOINT-ENTRY, "Starting checkpoint remainder changed")
    segments = lines(raw["segments.jsonl"], "segments.jsonl")
    events = lines(raw["clocks.jsonl"], "clocks.jsonl")
    waits = lines(raw["adjustments.jsonl"], "adjustments.jsonl")
    recoveries = lines(raw["recovery_exclusions.jsonl"], "recovery_exclusions.jsonl")
    changes = lines(raw["mode_reclassifications.jsonl"], "mode_reclassifications.jsonl")
    validate_segments(segments, events)
    by_start = {s["start_monotonic_ns"]: s for s in segments}
    normalization = []

    def duration_ns(value, label):
        require(type(value) in (int, float) and not isinstance(value, bool), f"Nonnumeric exclusion: {label}")
        seconds = Decimal(str(value))
        require(seconds.is_finite() and seconds >= 0, f"Negative/nonfinite exclusion: {label}")
        result = int((seconds*NS).to_integral_value(rounding=ROUND_HALF_EVEN))
        delta = Decimal(result)/NS-seconds
        require(abs(delta) <= Decimal("0.0000000005"), f"Exclusion precision exceeds nanosecond normalization: {label}")
        if delta:
            normalization.append({"record": label, "raw_seconds": str(value), "normalized_nanoseconds": result,
                                  "normalization_delta_seconds": str(delta)})
        return result

    wait_by, recovery_by, change_by = {}, {}, {}
    for name, records, value_key, destination in (
            ("adjustments.jsonl", waits, "observed_wait_seconds", wait_by),
            ("recovery_exclusions.jsonl", recoveries, "seconds", recovery_by)):
        for index, record in enumerate(records):
            key = record["segment_start_monotonic_ns"]
            require(type(key) is int and key in by_start, f"Orphan exclusion in {name}:{index+1}")
            require(bool(record.get("reason", "").strip()), f"Unexplained exclusion in {name}:{index+1}")
            if name == "recovery_exclusions.jsonl":
                require(record["classification"] == "recovery", "Recovery exclusion has another classification")
                require(all(record[field] == by_start[key][field] for field in ("start_utc", "end_utc")),
                        f"Recovery exclusion boundaries do not bind the raw segment: {index+1}")
            amount = duration_ns(record[value_key], f"{name}:{index+1}")
            destination[key] = destination.get(key, 0) + amount
    for index, record in enumerate(changes):
        key = record["segment_start_monotonic_ns"]
        require(type(key) is int and key in by_start and key not in change_by, "Orphan or repeated mode reclassification")
        original = by_start[key]
        require(record["original_mode"] == original["mode"] and record["original_lane"] == original["lane"], "Reclassification does not bind the raw mode/lane")
        require(record["mode"] in MODES and record["lane"] in ("R", "X", ""), "Invalid effective mode/lane")
        require(bool(record.get("reason", "").strip()), "Reclassification requires its preserved reason")
        require(original["mode"] in ENGAGED or record["mode"] not in ENGAGED, "Excluded wait/recovery cannot be promoted to engaged credit")
        change_by[key] = record
    totals = dict.fromkeys(MODES, 0)
    lanes = {"R": 0, "X": 0}
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    seen_forecasts, dispositions = set(), []
    for index, segment in enumerate(segments):
        key = segment["start_monotonic_ns"]
        elapsed = segment["end_monotonic_ns"]-key
        excluded_wait, excluded_recovery = wait_by.get(key, 0), recovery_by.get(key, 0)
        require(excluded_wait+excluded_recovery <= elapsed, f"Exclusions exceed segment {index}; do not clamp substantive overlap")
        remaining = elapsed-excluded_wait-excluded_recovery
        reclassification = change_by.get(key)
        mode = reclassification["mode"] if reclassification else segment["mode"]
        lane = reclassification["lane"] if reclassification else segment["lane"]
        if mode == "wait" and segment["note"].startswith("Artifact integrity recovery:"):
            mode = "recovery"
        require(mode in MODES, "Unknown effective mode")
        require(lane in ("R", "X") if mode in RESEARCH else lane == "", "Research/nonresearch lane mismatch")
        totals[mode] += remaining
        totals["wait"] += excluded_wait
        totals["recovery"] += excluded_recovery
        if mode in RESEARCH:
            lanes[lane] += remaining
        credited = remaining if mode in ENGAGED else 0
        row_wait = excluded_wait + (remaining if mode == "wait" else 0)
        row_recovery = excluded_recovery + (remaining if mode == "recovery" else 0)
        require(credited+row_wait+row_recovery == elapsed, "Per-segment accounting does not conserve observed time")
        ledger_mode = mode if mode in ENGAGED else "E" if mode == "wait" else "O"
        planned = CENTRAL[mode]*60 if mode in ENGAGED and mode not in seen_forecasts else ""
        if mode in ENGAGED:
            seen_forecasts.add(mode)
        status = ("complete; measured principal segment" if credited else "excluded segment; no engaged credit")
        status += "; " + segment["note"]
        if excluded_wait:
            status += "; excluded tool wait " + seconds_text(excluded_wait) + " seconds"
        if row_recovery:
            status += "; excluded recovery/unobserved " + seconds_text(row_recovery) + " seconds"
        if reclassification:
            status += "; mode reclassification: " + reclassification["reason"]
        writer.writerow(["F15", "F15-A", "2026-10-04-S1", ledger_mode, lane,
                         segment["start_utc"], segment["end_utc"], seconds_text(elapsed),
                         seconds_text(credited), seconds_text(row_wait), "0", seconds_text(row_recovery),
                         planned, "v2/work_logs/F15_2026-10-04_S1.md", status])
        dispositions.append({"index": index, "raw_segment": segment, "effective_mode": mode,
                             "effective_lane": lane, "elapsed_ns": elapsed, "engaged_ns": credited,
                             "tool_wait_ns": row_wait, "recovery_or_unobserved_ns": row_recovery,
                             "inline_wait_exclusion_ns": excluded_wait, "recovery_exclusion_ns": excluded_recovery,
                             "mode_reclassification": reclassification})
    wall_ns = segments[-1]["end_monotonic_ns"]-segments[0]["start_monotonic_ns"]
    require(sum(totals.values()) == wall_ns, "Wall span differs from disjoint mode/exclusion totals")
    research_ns, engaged_ns = sum(totals[k] for k in RESEARCH), sum(totals[k] for k in ENGAGED)
    require(sum(lanes.values()) == research_ns, "R/X totals do not equal D/L/E research time")
    require(totals["E"] >= 60*MINUTE_NS, "Protected E60 not met; D/L/O and exclusions cannot substitute")
    appended = output.getvalue().encode("utf-8")
    added_rows = list(csv.DictReader(io.StringIO(",".join(HEADER)+"\n"+appended.decode("utf-8"), newline="")))
    require(len(added_rows) == len(segments), "CSV does not have exactly one row per segment")
    ledger_mode_ns = dict.fromkeys(ENGAGED, 0)
    for row in added_rows:
        require(Decimal(row["elapsed_seconds"]) == sum(Decimal(row[k]) for k in ("engaged_seconds", "tool_wait_seconds", "idle_seconds", "unmeasured_seconds")), "Serialized CSV time conservation failed")
        ledger_mode_ns[row["mode"]] += int(Decimal(row["engaged_seconds"])*NS)
    require(ledger_mode_ns == {k: totals[k] for k in ENGAGED}, "Ledger engaged mode totals differ from actuals")
    require(sum(int(Decimal(row["tool_wait_seconds"])*NS) for row in added_rows) == totals["wait"], "Ledger wait total differs")
    require(sum(int(Decimal(row["unmeasured_seconds"])*NS) for row in added_rows) == totals["recovery"], "Ledger recovery total differs")
    minutes = {k: v/MINUTE_NS for k, v in totals.items()}
    research, engaged = research_ns/MINUTE_NS, engaged_ns/MINUTE_NS
    close = ENTRY + Decimal(engaged_ns)/MINUTE_NS
    lane_percent = {k: 100*v/research_ns for k, v in lanes.items()}
    inputs = {name: {"path": (SESSION/name).relative_to(REPO).as_posix(), "bytes": len(data), "sha256": sha(data)} for name, data in raw.items()}
    actuals = {
        "schema": "F15-measured-actuals-v1", "status": "accounting finalized; protected E60 satisfied; scientific and contribution dispositions remain separate",
        "contributor": "ChatGPT (GPT-6 Astra Pro)", "serializer_contributor": "delegated ChatGPT (GPT-6 Astra Pro), execution audit",
        "task": "F15", "attempt": "F15-A", "session": "2026-10-04-S1", "source_revision": SOURCE,
        "start_utc": segments[0]["start_utc"], "accounting_cutoff_utc": segments[-1]["end_utc"],
        "start_monotonic_ns": segments[0]["start_monotonic_ns"], "accounting_cutoff_monotonic_ns": segments[-1]["end_monotonic_ns"],
        "serialized_utc": datetime.now(timezone.utc).isoformat(), "runtime": "linux-F15-S1",
        "principal_segments": len(segments), "minutes": minutes, "exact_nanoseconds": totals,
        "research_minutes": research, "engaged_minutes": engaged, "lane_minutes": {k: v/MINUTE_NS for k, v in lanes.items()},
        "lane_exact_nanoseconds": lanes, "lane_percent_of_research": lane_percent,
        "protected_floor": {"mode": "E", "minutes": 60, "required_nanoseconds": 60*MINUTE_NS, "observed_nanoseconds": totals["E"], "satisfied": True},
        "E_floor_minutes": 60, "E_floor_satisfied": True, "O_satisfies_research_floor": False,
        "D_L_O_satisfy_protected_E_floor": False,
        "observed_wall_minutes": wall_ns/MINUTE_NS, "observed_wall_nanoseconds": wall_ns,
        "uncredited_transition_gap_seconds": 0, "strict_contiguous_nonoverlap_verified": True,
        "exclusion_record_counts": {"wait_adjustments": len(waits), "recovery_exclusions": len(recoveries), "mode_reclassifications": len(changes)},
        "inline_exclusion_nanoseconds": {"wait": sum(wait_by.values()), "recovery": sum(recovery_by.values())},
        "exclusion_numeric_normalizations": normalization, "effective_segment_accounting": dispositions,
        "uncredited_administrative_tail": "Ledger serialization, document updates, commit/push handling and response after cutoff are not quantified or credited.",
        "uncredited_preclock_work": forecast["preclock_work"], "parallel_agent_minutes_added": 0,
        "central_forecast_minutes": CENTRAL, "high_forecast_minutes": HIGH,
        "central_forecast_error_minutes": {**{k: minutes[k]-CENTRAL[k] for k in (*ENGAGED, "wait")}, "research": research-100, "engaged": engaged-120},
        "high_forecast_error_minutes": {**{k: minutes[k]-HIGH[k] for k in (*ENGAGED, "wait")}, "research": research-210, "engaged": engaged-240},
        "forecast_lane_percent": {"R": 60, "X": 40}, "lane_forecast_error_percentage_points": {k: lane_percent[k]-forecast["research_lane_percent"][k] for k in lanes},
        "post_b_1": {"entry_minutes": float(ENTRY), "inherited_eight_hour_overshoot_minutes": float(INHERITED_OVERSHOOT),
                     "close_minutes": float(close), "close_minutes_decimal": str(close), "next_checkpoint_minutes": 960,
                     "remaining_minutes": float(CHECKPOINT-close), "checkpoint_reached": close >= CHECKPOINT,
                     "sixteen_hour_overshoot_minutes": float(max(Decimal(0), close-CHECKPOINT)), "recurrence_clock_reset": False},
        "raw_inputs": inputs, "raw_records_modified": False, "serializer_sha256": sha(Path(__file__).read_bytes()),
        "ledger_prior_bytes": len(prior), "ledger_prior_sha256": sha(prior), "ledger_append_bytes": len(appended),
        "ledger_append_sha256": sha(appended), "ledger_rows_added": len(segments),
        "F16_started": False, "gate_C_D_attempted": False, "continuation_required_for_E60": False,
    }
    integrity = {"schema": "F15-ledger-integrity-v1", "ledger_path": LEDGER.relative_to(REPO).as_posix(),
                 "baseline_bytes": BASELINE_BYTES, "baseline_sha256": BASELINE_SHA256,
                 "old_ledger_rows": len(old_rows)-1, "appended_rows": len(segments), "appended_bytes": len(appended),
                 "appended_sha256": sha(appended), "expected_new_bytes": len(prior)+len(appended),
                 "expected_new_sha256": sha(prior+appended), "exact_old_prefix_preserved": True,
                 "append_only_write": True, "raw_inputs": inputs, "effective_E_nanoseconds": totals["E"],
                 "protected_E60_verified": True, "one_row_per_segment_verified": True,
                 "per_row_and_total_conservation_verified": True, "raw_records_modified": False,
                 "parallel_agent_minutes_added": 0, "administration_after_cutoff_credited": False}
    return actuals, integrity, appended


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_exclusive(path, value):
    payload = canonical(value)
    with path.open("xb") as handle:
        handle.write(payload); handle.flush(); os.fsync(handle.fileno())
    sidecar = Path(str(path)+".sha256")
    digest_line = sha(payload)+"\n"
    with sidecar.open("x", encoding="ascii") as handle:
        handle.write(digest_line); handle.flush(); os.fsync(handle.fileno())
    sync_directory(path.parent)
    require(path.read_bytes() == payload, f"Saved output failed exact reread: {path}")
    require(sidecar.read_bytes() == digest_line.encode("ascii"), f"Saved sidecar failed exact reread: {sidecar}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Validate a stopped E60-complete clock; write nothing")
    args = parser.parse_args()
    raw = {name: (SESSION/name).read_bytes() for name in INPUT_NAMES}
    expected_outputs = [SESSION/name for name in OUTPUT_NAMES]
    expected_outputs += [Path(str(path)+".sha256") for path in expected_outputs]
    require(not any(path.exists() for path in expected_outputs), "A finalization output/intent already exists; inspect it instead of overwriting or rerunning")
    flags = os.O_RDONLY if args.dry_run else os.O_RDWR | os.O_APPEND
    fd = os.open(LEDGER, flags)
    with os.fdopen(fd, "rb" if args.dry_run else "r+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_SH if args.dry_run else fcntl.LOCK_EX)
        prior = handle.read()
        actuals, integrity, appended = build_plan(raw, prior)
        summary = {"dry_run": args.dry_run, "E_minutes": actuals["minutes"]["E"],
                   "research_minutes": actuals["research_minutes"], "engaged_minutes": actuals["engaged_minutes"],
                   "O_minutes": actuals["minutes"]["O"], "wait_minutes": actuals["minutes"]["wait"],
                   "recovery_minutes": actuals["minutes"]["recovery"], "lane_minutes": actuals["lane_minutes"],
                   "post_b_close_minutes": actuals["post_b_1"]["close_minutes"],
                   "remaining_to_sixteen_hours": actuals["post_b_1"]["remaining_minutes"],
                   "ledger_rows_added" if not args.dry_run else "ledger_rows_proposed": actuals["ledger_rows_added"]}
        require(all((SESSION/name).read_bytes() == data for name, data in raw.items()), "Raw clock/accounting inputs changed during validation")
        handle.seek(0)
        require(handle.read() == prior, "Ledger changed while validating; no append performed")
        if args.dry_run:
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 0
        require(not any(path.exists() for path in expected_outputs), "Finalization outputs appeared during validation")
        intent = {"schema": "F15-accounting-finalization-intent-v1", "actuals": actuals,
                  "ledger_integrity_plan": integrity, "append_csv_utf8": appended.decode("utf-8"),
                  "recovery_instruction": "If interrupted, preserve these files and inspect exact old/new ledger hashes. Never blindly rerun, duplicate rows, or rewrite historical bytes."}
        write_exclusive(SESSION / "finalization_intent.json", intent)
        handle.seek(0)
        require(handle.read() == prior, "Ledger changed before append")
        require(all((SESSION/name).read_bytes() == data for name, data in raw.items()), "Raw inputs changed before append")
        handle.seek(0, os.SEEK_END)
        require(handle.tell() == BASELINE_BYTES, "Ledger length changed before append")
        written = handle.write(appended)
        require(written == len(appended), "Partial ledger append; preserve intent and inspect before any recovery")
        handle.flush(); os.fsync(handle.fileno())
        sync_directory(LEDGER.parent)
        handle.seek(0)
        observed = handle.read()
        require(observed[:len(prior)] == prior and observed == prior+appended, "Post-append bytes do not match exact old prefix plus planned rows")
        integrity.update(observed_new_bytes=len(observed), observed_new_sha256=sha(observed),
                         post_append_readback_verified=True, verified_utc=datetime.now(timezone.utc).isoformat())
        write_exclusive(SESSION / "actuals.json", actuals)
        write_exclusive(SESSION / "ledger_integrity.json", integrity)
        require(all((SESSION/name).read_bytes() == data for name, data in raw.items()), "Raw records changed during final serialization")
        summary["exact_old_ledger_prefix_preserved"] = True
        summary["write_performed"] = True
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
