#!/usr/bin/env python3
"""Minimal observed clock for phase-four recurrence cycles (v4/RECURRENCE.md).

Written by Claude (Fable 5.2), 2026-11-09. One JSON line per observation:
UTC, time.monotonic_ns(), runtime identity, mode and event. The mode of an
observation labels the work that FOLLOWS it. An interval between consecutive
observations is credited only when both share a runtime, the opening event is
not pause/stop, and the gap is at most 15 minutes. Research credit is D+L+E.

  clock.py FILE MODE EVENT [note]   MODE in D L E O; EVENT in start tick pause resume stop
  clock.py FILE --sum

A correction is an appended record with event "exclude", a mode and
"exclude_ns": that many nanoseconds are removed from the mode's credit, for
example when an interval turns out to have been waiting on a computation.
Run long computations under mode O so that waiting is never credited.
"""
import datetime, json, pathlib, socket, sys, time

MAX_GAP_NS = 900 * 10**9


def runtime():
    try:
        boot = pathlib.Path("/proc/sys/kernel/random/boot_id").read_text().strip()
    except OSError:
        boot = "unknown"
    return f"{socket.gethostname()}:{boot}"


def observe(path, mode, event, note=""):
    if mode not in "DLEO" or event not in ("start", "tick", "pause", "resume", "stop"):
        raise SystemExit("bad mode or event")
    rec = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "mono_ns": time.monotonic_ns(), "runtime": runtime(),
           "mode": mode, "event": event, "note": note}
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


def credit(path):
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    total = dict.fromkeys("DLEO", 0)
    excluded = 0
    for a, b in zip(rows, rows[1:]):
        gap = b["mono_ns"] - a["mono_ns"]
        if (a["runtime"] == b["runtime"] and a["event"] not in ("pause", "stop", "exclude")
                and b["event"] != "exclude" and 0 <= gap <= MAX_GAP_NS):
            total[a["mode"]] += gap
        else:
            excluded += 1
    for row in rows:
        if row["event"] == "exclude":
            total[row["mode"]] -= row["exclude_ns"]
    research = total["D"] + total["L"] + total["E"]
    return {"ns": total, "research_ns": research, "research_min": research / 6e10,
            "floor_remaining_min": max(0.0, 240 - research / 6e10),
            "observations": len(rows), "uncredited_intervals": excluded}


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[2] == "--sum":
        print(json.dumps(credit(sys.argv[1]), indent=1))
    else:
        print(json.dumps(observe(sys.argv[1], sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))))
