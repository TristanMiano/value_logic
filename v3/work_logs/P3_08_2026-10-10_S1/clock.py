"""Observed P3-08 clock. ChatGPT (GPT-6 Astra Pro), 2026-10-10.

start/switch/resume MODE LANE NOTE; check NOTE; pause CATEGORY NOTE;
stop NOTE; report. Only closed, observed principal segments earn time.
"""
from datetime import datetime, timezone
from pathlib import Path
import json
import sys
import time

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "clock_state.json"
EVENTS = ROOT / "clocks.jsonl"
SEGMENTS = ROOT / "segments.jsonl"
DISPOSITIONS = ROOT / "clock_dispositions.jsonl"
BOOT = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
RUNTIME = "linux-P3-08-S1:" + BOOT


def read_records(path):
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def effective_segments():
    """Split raw observations at explicit corrections; never alter raw clocks."""
    raw = read_records(SEGMENTS)
    corrections = read_records(DISPOSITIONS)
    ordered = sorted(corrections, key=lambda c: c["start_monotonic_ns"])
    for left, right in zip(ordered, ordered[1:]):
        assert left["end_monotonic_ns"] <= right["start_monotonic_ns"], "Overlapping dispositions."
    for correction in corrections:
        assert correction["runtime"] == RUNTIME
        assert correction["start_monotonic_ns"] < correction["end_monotonic_ns"]
        assert any(s["start_monotonic_ns"] <= correction["start_monotonic_ns"]
                   and correction["end_monotonic_ns"] <= s["end_monotonic_ns"] for s in raw)
    effective = []
    for index, segment in enumerate(raw):
        assert segment["elapsed_ns"] == segment["end_monotonic_ns"] - segment["start_monotonic_ns"]
        applicable = [c for c in corrections if segment["start_monotonic_ns"] <= c["start_monotonic_ns"]
                      and c["end_monotonic_ns"] <= segment["end_monotonic_ns"]]
        boundaries = {segment["start_monotonic_ns"]: segment["start_utc"],
                      segment["end_monotonic_ns"]: segment["end_utc"]}
        for correction in applicable:
            boundaries[correction["start_monotonic_ns"]] = correction["start_utc"]
            boundaries[correction["end_monotonic_ns"]] = correction["end_utc"]
        points = sorted(boundaries)
        for start, end in zip(points, points[1:]):
            covering = [c for c in applicable if c["start_monotonic_ns"] <= start and end <= c["end_monotonic_ns"]]
            assert len(covering) <= 1
            part = dict(segment, raw_segment_index=index, start_monotonic_ns=start, end_monotonic_ns=end,
                        start_utc=boundaries[start], end_utc=boundaries[end], elapsed_ns=end-start)
            if covering:
                correction = covering[0]
                assert correction["original_mode"] == segment["mode"]
                part.update(mode=correction["mode"], lane=correction["lane"],
                            note=correction["reason"], disposition_id=correction["id"])
            effective.append(part)
    assert sum(s["elapsed_ns"] for s in effective) == sum(s["elapsed_ns"] for s in raw)
    return effective


def main():
    command, *args = sys.argv[1:]
    state = json.loads(STATE.read_text()) if STATE.exists() else None
    now = {"utc": datetime.now(timezone.utc).isoformat(),
           "monotonic_ns": time.monotonic_ns(), "runtime": RUNTIME}
    if state is not None:
        assert state["runtime"] == RUNTIME, "Different runtime: preserve and disposition the unobserved segment."
    if command == "report":
        totals = dict.fromkeys(["D", "L", "E", "O", "wait", "idle", "unmeasured", "recovery"], 0)
        lanes = dict.fromkeys(["R", "X"], 0)
        for segment in effective_segments():
            totals[segment["mode"]] += segment["elapsed_ns"]
            if segment["lane"] in lanes:
                lanes[segment["lane"]] += segment["elapsed_ns"]
        print(json.dumps({"closed_ns": totals, "closed_minutes": {k: v / 60e9 for k, v in totals.items()},
                          "lane_ns": lanes, "open_segment": state,
                          "open_elapsed_ns": now["monotonic_ns"] - state["start_monotonic_ns"] if state else 0}, indent=2))
        return
    assert command in ["start", "switch", "resume", "pause", "check", "stop"]
    if command == "start":
        assert not EVENTS.exists(), "Inspect and resume this attempt; do not restart its clock."
    elif command in ["switch", "pause", "stop", "check"]:
        assert state is not None, "No open segment."
    elif command == "resume":
        assert state is None or state["mode"] in ["wait", "idle", "unmeasured", "recovery"]
    if command in ["start", "switch", "resume"]:
        mode, lane, *note = args
        assert mode in ["D", "L", "E", "O"]
        assert (mode == "O" and lane == "-") or (mode != "O" and lane in ["R", "X"])
        new_mode, new_lane, new_note = mode, "" if lane == "-" else lane, " ".join(note)
    elif command == "pause":
        new_mode, *note = args
        assert new_mode in ["wait", "idle", "unmeasured", "recovery"]
        new_lane, new_note = "", " ".join(note)
    event = dict(now, command=command, args=args)
    with EVENTS.open("a") as f:
        f.write(json.dumps(event) + "\n")
    if command == "check":
        print(json.dumps(event))
        return
    if state is not None:
        segment = dict(state, end_utc=now["utc"], end_monotonic_ns=now["monotonic_ns"],
                       elapsed_ns=now["monotonic_ns"] - state["start_monotonic_ns"])
        with SEGMENTS.open("a") as f:
            f.write(json.dumps(segment) + "\n")
    state = None if command == "stop" else {
        "mode": new_mode, "lane": new_lane, "note": new_note,
        "start_utc": now["utc"], "start_monotonic_ns": now["monotonic_ns"], "runtime": RUNTIME}
    temp = STATE.with_suffix(".tmp")
    temp.write_text(json.dumps(state, indent=2) + "\n")
    temp.replace(STATE)
    print(json.dumps(event))


if __name__ == "__main__":
    main()
