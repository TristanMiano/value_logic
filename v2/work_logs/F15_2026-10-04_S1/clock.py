"""Observed principal-agent clock; parallel agent time is not added.

Contributor: ChatGPT (GPT-6 Astra Pro), F15. This is accounting tooling only.
Commands: start MODE LANE NOTE; switch MODE LANE NOTE; check NOTE;
pause NOTE; resume MODE LANE NOTE; stop NOTE; report.
All subprocess/tool waits should be bracketed by pause/resume when blocking.
"""
import datetime
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent
EVENTS = ROOT / "clocks.jsonl"
STATE = ROOT / "clock_state.json"
SEGMENTS = ROOT / "segments.jsonl"
ADJUSTMENTS = ROOT / "adjustments.jsonl"
RECOVERY_EXCLUSIONS = ROOT / "recovery_exclusions.jsonl"
RECLASSIFICATIONS = ROOT / "mode_reclassifications.jsonl"


def main():
    command, *args = sys.argv[1:]
    state = json.loads(STATE.read_text()) if STATE.exists() else None
    now = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "monotonic_ns": time.monotonic_ns(), "runtime": "linux-F15-S1"}
    if command == "report":
        totals = dict.fromkeys(("D", "L", "E", "O", "wait", "recovery"), 0.0)
        lanes = {"R": 0.0, "X": 0.0}
        segments = [json.loads(line) for line in SEGMENTS.read_text().splitlines()] if SEGMENTS.exists() else []
        adjustments = [json.loads(line) for line in ADJUSTMENTS.read_text().splitlines()] if ADJUSTMENTS.exists() else []
        recovery = [json.loads(line) for line in RECOVERY_EXCLUSIONS.read_text().splitlines()] if RECOVERY_EXCLUSIONS.exists() else []
        classifications = [json.loads(line) for line in RECLASSIFICATIONS.read_text().splitlines()] if RECLASSIFICATIONS.exists() else []
        for segment in segments:
            excluded_wait = sum(a["observed_wait_seconds"] for a in adjustments
                                if a["segment_start_monotonic_ns"] == segment["start_monotonic_ns"])
            excluded_recovery = sum(a["seconds"] for a in recovery
                                    if a["segment_start_monotonic_ns"] == segment["start_monotonic_ns"])
            seconds = segment["elapsed_seconds"]-excluded_wait-excluded_recovery
            assert 0 <= seconds <= segment["elapsed_seconds"]
            mode = segment["mode"]
            lane = segment["lane"]
            changes = [r for r in classifications if r["segment_start_monotonic_ns"] == segment["start_monotonic_ns"]]
            assert len(changes) <= 1
            if changes:
                mode, lane = changes[0]["mode"], changes[0]["lane"]
            if mode == "wait" and segment["note"].startswith("Artifact integrity recovery:"):
                mode = "recovery"
            totals[mode] += seconds
            totals["wait"] += excluded_wait
            totals["recovery"] += excluded_recovery
            if lane in lanes:
                lanes[lane] += seconds
        print(json.dumps({"closed_minutes": {k: v/60 for k, v in totals.items()},
                          "lane_minutes": {k: v/60 for k, v in lanes.items()},
                          "research_minutes": sum(totals[k] for k in ("D", "L", "E"))/60,
                          "open_segment": state, "now": now}, indent=2))
        return
    event = dict(now, command=command, args=args)
    with EVENTS.open("a") as handle:
        handle.write(json.dumps(event)+"\n")
    if command == "check":
        print(json.dumps(event))
        return
    if state:
        segment = dict(state, end_utc=now["utc"], end_monotonic_ns=now["monotonic_ns"],
                       elapsed_seconds=(now["monotonic_ns"]-state["start_monotonic_ns"])/1e9)
        with SEGMENTS.open("a") as handle:
            handle.write(json.dumps(segment)+"\n")
    if command in ("start", "switch", "resume"):
        mode, lane, *notes = args
        assert mode in ("D", "L", "E", "O")
        assert lane in ("R", "X", "-")
        state = {"mode": mode, "lane": "" if lane == "-" else lane,
                 "start_utc": now["utc"], "start_monotonic_ns": now["monotonic_ns"],
                 "note": " ".join(notes), "runtime": now["runtime"]}
    elif command == "pause":
        state = {"mode": "wait", "lane": "", "start_utc": now["utc"],
                 "start_monotonic_ns": now["monotonic_ns"], "note": " ".join(args),
                 "runtime": now["runtime"]}
    elif command == "stop":
        state = None
    else:
        raise ValueError(command)
    STATE.write_text(json.dumps(state, indent=2)+"\n")
    print(json.dumps(event))


if __name__ == "__main__":
    main()
