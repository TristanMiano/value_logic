"""Exact, conservative P3-01 accounting. GPT-6 Astra Pro, 2026-10-07.

preview: read-only JSON audit of CLOSED observations; no open time is counted.
finalize: after the principal clock stops, append this attempt exactly once.
Never imports or mutates clock.py. Failed finalization artifacts need explicit
inspection; this helper never repairs, truncates, or silently retries them.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import hashlib
import io
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LEDGER = REPO / "v3/time_ledger.csv"
TASK, ATTEMPT, SESSION = "P3-01", "P3-01-1", "2026-10-07-S1"
ARTIFACT = "v3/work_logs/P3_01_2026-10-07_S1.md"
MODES = ("D", "L", "E", "O", "wait", "idle", "unmeasured", "recovery")
RESEARCH = {"D", "L", "E"}
ENGAGED = RESEARCH | {"O"}
NS_SECOND, NS_MINUTE = 1_000_000_000, 60_000_000_000
INPUTS = ("baseline.json", "forecast.json", "clock.py", "clocks.jsonl",
          "segments.jsonl", "clock_dispositions.jsonl", "clock_state.json")
FIELDS = ("task_id", "attempt_id", "session_id", "mode", "lane", "start_utc",
          "end_utc", "elapsed_seconds", "engaged_seconds", "tool_wait_seconds",
          "idle_seconds", "unmeasured_seconds", "forecast_seconds", "artifact", "status")


class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dumps(value):
    return json.dumps(value, indent=2, sort_keys=True, default=str) + "\n"


def parse(data):
    return json.loads(data, parse_float=Decimal)


def records(data):
    return [parse(line) for line in data.splitlines() if line.strip()]


def seconds(ns):
    whole, fraction = divmod(ns, NS_SECOND)
    return f"{whole}.{fraction:09d}"


def minutes(ns):
    with localcontext() as context:
        context.prec = 50
        return format(Decimal(ns) / Decimal(NS_MINUTE), ".12f")


def exact_ns(value, unit):
    number = Decimal(value)
    require(number.is_finite() and number >= 0, "Nonnegative finite quantity required")
    numerator, denominator = number.as_integer_ratio()
    scaled = numerator * unit
    require(scaled % denominator == 0, "Quantity is not an exact number of nanoseconds")
    return scaled // denominator


def category(mode, lane):
    require(mode in MODES, f"Unknown category: {mode}")
    require(lane in ("R", "X") if mode in RESEARCH else lane == "",
            f"Invalid category/lane pair: {mode}/{lane}")


def checked_utc(value):
    result = datetime.fromisoformat(value)
    require(result.tzinfo is not None and result.utcoffset().total_seconds() == 0,
            "Clock timestamps must specify UTC")
    return result


def snapshot():
    first = {name: (HERE / name).read_bytes() for name in INPUTS}
    second = {name: (HERE / name).read_bytes() for name in INPUTS}
    require(first == second, "Clock inputs changed during the read; inspect/rerun preview")
    return first


def replay(events, raw, state):
    """Rebuild raw closed segments from the saved events, not wall-clock guesses."""
    require(events and events[0]["command"] == "start", "Missing original start event")
    active, rebuilt, previous_ns, runtime = None, [], -1, events[0]["runtime"]
    anchors = {}
    for index, event in enumerate(events):
        ns, utc, command, args = (event[k] for k in ("monotonic_ns", "utc", "command", "args"))
        require(type(ns) is int and ns > previous_ns, "Non-increasing event nanoseconds")
        require(event["runtime"] == runtime, "Mixed runtimes require explicit separate accounting")
        require(isinstance(args, list) and all(isinstance(x, str) for x in args), "Invalid event args")
        checked_utc(utc)
        anchors[ns] = utc
        previous_ns = ns
        require(command in {"start", "switch", "resume", "pause", "check", "stop"}, "Unknown event command")
        if command == "start":
            require(index == 0 and active is None, "Attempt clock restarted")
        elif command == "resume":
            require(active is None or active["mode"] not in ENGAGED, "Resume from engaged segment")
        else:
            require(active is not None, f"{command} without an open segment")
        if command == "check":
            continue
        if active is not None:
            rebuilt.append(dict(active, end_utc=utc, end_monotonic_ns=ns,
                                elapsed_ns=ns-active["start_monotonic_ns"]))
        if command == "stop":
            active = None
            continue
        if command in {"start", "switch", "resume"}:
            require(len(args) >= 2, "Mode/lane missing")
            mode, lane, *note = args
            require(mode in ENGAGED, "Active mode outside D/L/E/O")
            lane = "" if lane == "-" else lane
        else:
            require(args, "Pause category missing")
            mode, *note = args
            require(mode in set(MODES)-ENGAGED, "Invalid pause category")
            lane = ""
        category(mode, lane)
        active = dict(mode=mode, lane=lane, note=" ".join(note), start_utc=utc,
                      start_monotonic_ns=ns, runtime=runtime)
    require(rebuilt == raw, "Raw segments do not equal replayed clock events")
    require(active == state, "Saved open/closed state does not equal event replay")
    return runtime, anchors


def effective(raw, corrections, runtime, anchors):
    ids = set()
    ordered = sorted(corrections, key=lambda c: c["start_monotonic_ns"])
    for left, right in zip(ordered, ordered[1:]):
        require(left["end_monotonic_ns"] <= right["start_monotonic_ns"], "Overlapping dispositions")
    for correction in corrections:
        start, end = correction["start_monotonic_ns"], correction["end_monotonic_ns"]
        require(correction["id"] not in ids, "Duplicate disposition id")
        ids.add(correction["id"])
        require(type(start) is int and type(end) is int and start < end, "Invalid disposition interval")
        require(correction["runtime"] == runtime, "Disposition runtime differs")
        category(correction["mode"], correction["lane"])
        matches = [s for s in raw if s["start_monotonic_ns"] <= start < end <= s["end_monotonic_ns"]]
        require(len(matches) == 1 and matches[0]["mode"] == correction["original_mode"],
                "Disposition must belong to exactly one closed original-mode segment")
        require(anchors.get(start) == correction["start_utc"] and anchors.get(end) == correction["end_utc"],
                "Disposition boundaries must match saved clock observations")
        require(isinstance(correction["reason"], str) and correction["reason"].strip(), "Disposition lacks reason")
    result = []
    for index, segment in enumerate(raw):
        start, end = segment["start_monotonic_ns"], segment["end_monotonic_ns"]
        require(type(start) is int and type(end) is int and end > start, "Invalid closed segment")
        require(type(segment["elapsed_ns"]) is int and segment["elapsed_ns"] == end-start,
                "Elapsed nanoseconds mismatch")
        category(segment["mode"], segment["lane"])
        applicable = [c for c in corrections if start <= c["start_monotonic_ns"] < c["end_monotonic_ns"] <= end]
        points = sorted({start, end} | {c[k] for c in applicable for k in ("start_monotonic_ns", "end_monotonic_ns")})
        for a, b in zip(points, points[1:]):
            part = dict(segment, raw_segment_index=index, start_monotonic_ns=a, end_monotonic_ns=b,
                        start_utc=anchors[a], end_utc=anchors[b], elapsed_ns=b-a)
            covering = [c for c in applicable if c["start_monotonic_ns"] <= a and b <= c["end_monotonic_ns"]]
            require(len(covering) <= 1, "Ambiguous disposition")
            if covering:
                correction = covering[0]
                part.update(mode=correction["mode"], lane=correction["lane"], note=correction["reason"],
                            disposition_id=correction["id"], original_mode=segment["mode"])
            result.append(part)
    require(sum(s["elapsed_ns"] for s in result) == sum(s["elapsed_ns"] for s in raw), "Split lost elapsed time")
    return result


def prior_and_preservation(baseline):
    prefix = baseline["prior_v3_ledger_bytes"].encode("utf-8")
    meta = baseline["files"]["v3/time_ledger.csv"]
    require(len(prefix) == meta["bytes"] and digest(prefix) == meta["sha256"], "Baseline setup bytes/hash disagree")
    current = LEDGER.read_bytes()
    require(current.startswith(prefix), "Original phase-three ledger prefix changed")
    require(prefix.endswith(b"\n"), "Original prefix lacks terminal newline")
    parsed = csv.DictReader(io.StringIO(prefix.decode("utf-8")))
    require(tuple(parsed.fieldnames or ()) == FIELDS, "Unexpected ledger schema")
    prior = list(parsed)
    require(not any(r["task_id"] == TASK or r["attempt_id"] == ATTEMPT for r in prior), "Task already in baseline")
    research_ns = sum(exact_ns(r["engaged_seconds"], NS_SECOND) for r in prior if r["mode"] in RESEARCH)
    engaged_ns = sum(exact_ns(r["engaged_seconds"], NS_SECOND) for r in prior)
    require(research_ns == exact_ns(baseline["prior_phase_research_minutes"], NS_MINUTE), "Prior research total mismatch")
    require(Decimal(baseline["prior_task_research_minutes"]) == 0, "Unexpected prior task credit")
    preserved = {}
    for name, expected in baseline["files"].items():
        if name.startswith("v2/") or name in {"paper_v2.md", "TODO_v2.md"}:
            data = (REPO / name).read_bytes()
            require(len(data) == expected["bytes"] and digest(data) == expected["sha256"], f"Phase-two file changed: {name}")
            preserved[name] = dict(sha256=digest(data), bytes=len(data), matches_baseline=True)
    phase2_rows = len(list(csv.DictReader(io.StringIO((REPO / "v2/time_ledger.csv").read_text()))))
    require(phase2_rows == baseline["prior_v2_ledger_rows"], "Phase-two row count changed")
    return prefix, current, dict(original_v3_prefix_sha256=digest(prefix), original_v3_prefix_bytes=len(prefix),
                                original_v3_rows=len(prior), prefix_preserved=True,
                                phase2=preserved, phase2_rows=phase2_rows), research_ns, engaged_ns


def render_rows(parts, forecast):
    used = set()
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    for part in parts:
        mode, lane, ns = part["mode"], part["lane"], part["elapsed_ns"]
        engaged = ns if mode in ENGAGED else 0
        planned = ""
        if mode in ENGAGED and mode not in used:
            planned = seconds(exact_ns(forecast["central_minutes"][mode], NS_MINUTE))
            used.add(mode)
        row = dict(task_id=TASK, attempt_id=ATTEMPT, session_id=SESSION,
                   mode=mode if mode in ENGAGED else "O", lane=lane,
                   start_utc=part["start_utc"], end_utc=part["end_utc"],
                   elapsed_seconds=seconds(ns), engaged_seconds=seconds(engaged),
                   tool_wait_seconds=seconds(ns if mode == "wait" else 0),
                   idle_seconds=seconds(ns if mode == "idle" else 0),
                   unmeasured_seconds=seconds(ns if mode in {"unmeasured", "recovery"} else 0),
                   forecast_seconds=planned, artifact=ARTIFACT,
                   status=f"Closed P3-01 observation; scientific completion not inferred; later tasks/gates unattempted; {mode}; "
                          + (f"{part['disposition_id']}; " if "disposition_id" in part else "") + part["note"])
        require(sum(exact_ns(row[k], NS_SECOND) for k in
                    ("engaged_seconds", "tool_wait_seconds", "idle_seconds", "unmeasured_seconds")) == ns,
                "Ledger row does not partition elapsed time")
        writer.writerow(row)
    return buffer.getvalue().encode("utf-8")


def audit():
    inputs = snapshot()
    baseline, forecast, state = (parse(inputs[name]) for name in ("baseline.json", "forecast.json", "clock_state.json"))
    require(forecast["attempt"] == ATTEMPT and forecast["principal_time_only"] is True, "Forecast attempt/principal mismatch")
    require(set(forecast["central_minutes"]) == ENGAGED and set(forecast["high_minutes"]) == ENGAGED, "Forecast mode mismatch")
    require(set(forecast["lane_fraction"]) == {"R", "X"} and sum(forecast["lane_fraction"].values()) == 1, "Forecast lane mismatch")
    raw, corrections, events = (records(inputs[name]) for name in ("segments.jsonl", "clock_dispositions.jsonl", "clocks.jsonl"))
    runtime, anchors = replay(events, raw, state)
    parts = effective(raw, corrections, runtime, anchors)
    prefix, current, preservation, prior_research, prior_engaged = prior_and_preservation(baseline)
    totals = {mode: sum(s["elapsed_ns"] for s in parts if s["mode"] == mode) for mode in MODES}
    lane_ns = {lane: sum(s["elapsed_ns"] for s in parts if s["lane"] == lane) for lane in ("R", "X")}
    research_ns = sum(totals[m] for m in RESEARCH)
    engaged_ns = research_ns + totals["O"]
    excluded_ns = sum(totals[m] for m in set(MODES)-ENGAGED)
    require(sum(lane_ns.values()) == research_ns, "Lane totals differ from research")
    append = render_rows(parts, forecast)
    if current == prefix:
        relation = "original_prefix_only"
    elif current == prefix + append:
        relation = "already_matches_this_attempt_append"
    else:
        relation = "other_or_partial_suffix_preserved"
    floor_ns = exact_ns(forecast["protected_research_minutes"], NS_MINUTE)
    blockers = []
    if state is not None:
        blockers.append("principal_clock_open")
    if research_ns < floor_ns:
        blockers.append("protected_research_floor_not_met")
    if relation != "original_prefix_only":
        blockers.append(relation)
    for name in ("actuals.json", "ledger_append.csv", "accounting.finalize.lock"):
        if (HERE / name).exists():
            blockers.append("existing_" + name)
    attempts = HERE / "accounting_attempts"
    if attempts.exists() and any(attempts.iterdir()):
        blockers.append("existing_accounting_attempts_require_manual_disposition")
    payload = dict(schema="value_logic.P3-01.accounting.v1", task=TASK, attempt=ATTEMPT,
                   contributor="ChatGPT (GPT-6 Astra Pro)", principal_time_only=True,
                   research_completion_or_gate_pass_inferred=False, later_tasks_and_gates="unattempted",
                   exact_units="integer nanoseconds and fixed-nine-place seconds; minutes below are display-rounded to 12 places",
                   runtime=runtime, closed_raw_segments=len(raw), closed_effective_segments=len(parts),
                   disposition_count=len(corrections), open_segment=state, open_time_credited_ns=0,
                   category_ns=totals, category_seconds={k: seconds(v) for k, v in totals.items()},
                   category_minutes={k: minutes(v) for k, v in totals.items()}, lane_research_ns=lane_ns,
                   research_ns=research_ns, research_seconds=seconds(research_ns), research_minutes=minutes(research_ns),
                   engaged_ns=engaged_ns, engaged_seconds=seconds(engaged_ns), engaged_minutes=minutes(engaged_ns),
                   excluded_ns=excluded_ns, observed_closed_ns=engaged_ns+excluded_ns,
                   prior_phase3_research_ns=prior_research, prior_phase3_engaged_ns=prior_engaged,
                   phase3_research_ns=prior_research+research_ns, phase3_engaged_ns=prior_engaged+engaged_ns,
                   protected_research_ns=floor_ns, protected_research_floor_met=research_ns >= floor_ns,
                   forecast=forecast, preservation=preservation, ledger_relation=relation,
                   proposed_append_sha256=digest(append), proposed_append_bytes=len(append),
                   input_files={name: dict(sha256=digest(data), bytes=len(data)) for name, data in inputs.items()},
                   accounting_script_sha256=digest(Path(__file__).read_bytes()),
                   effective_segments=parts, finalize_blockers=blockers)
    return payload, inputs, prefix, append


def sync_directory(path):
    if os.name == "posix":
        descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def exclusive_write(path, data):
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    sync_directory(path.parent)


def finalize():
    payload, inputs, prefix, append = audit()
    require(not payload["finalize_blockers"], "Finalization refused: " + ", ".join(payload["finalize_blockers"]))
    lock = HERE / "accounting.finalize.lock"
    exclusive_write(lock, dumps({"pid": os.getpid(), "attempt": ATTEMPT}).encode())
    attempts = HERE / "accounting_attempts"
    attempts.mkdir(exist_ok=True)
    sync_directory(HERE)
    attempt_dir = attempts / "attempt0001"
    attempt_dir.mkdir()
    sync_directory(attempts)
    try:
        exclusive_write(attempt_dir / "prepared.json", dumps(payload).encode())
        exclusive_write(attempt_dir / "ledger_append.csv", append)
        require(snapshot() == inputs, "Clock/input files changed after audit")
        require(LEDGER.read_bytes() == prefix, "Ledger changed after audit")
        prior_and_preservation(parse(inputs["baseline.json"]))
        exclusive_write(HERE / "ledger_append.csv", append)
        with LEDGER.open("ab", buffering=0) as stream:
            require(os.fstat(stream.fileno()).st_size == len(prefix), "Ledger size changed before append")
            written = stream.write(append)
            require(written == len(append), "Short append; preserve all records and inspect manually")
            os.fsync(stream.fileno())
        require(LEDGER.read_bytes() == prefix + append, "Postappend bytes differ; manual reconciliation required")
        require(snapshot() == inputs, "Clock/input files changed during finalization; inspect manually")
        prior_and_preservation(parse(inputs["baseline.json"]))
        payload.update(finalized=True, finalized_utc=datetime.now(timezone.utc).isoformat(),
                       ledger_after_sha256=digest(prefix+append), ledger_after_bytes=len(prefix+append),
                       ledger_rows_appended=payload["closed_effective_segments"],
                       ledger_relation="finalized_exact_append", finalize_blockers=[])
        exclusive_write(HERE / "actuals.json", dumps(payload).encode())
        exclusive_write(attempt_dir / "result.json", dumps({"status": "finalized", "actuals_sha256": digest((HERE / "actuals.json").read_bytes())}).encode())
        lock.unlink()
        sync_directory(HERE)
        return payload
    except Exception as error:
        exclusive_write(attempt_dir / "failure.json", dumps({"error": type(error).__name__, "message": str(error),
                        "utc": datetime.now(timezone.utc).isoformat(), "automatic_retry": False}).encode())
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preview", "finalize"))
    args = parser.parse_args()
    try:
        payload = audit()[0] if args.command == "preview" else finalize()
        print(dumps(payload), end="")
    except (AuditError, OSError, ValueError, KeyError, TypeError) as error:
        print(dumps({"error": type(error).__name__, "message": str(error), "no_automatic_retry": True}), file=sys.stderr, end="")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
