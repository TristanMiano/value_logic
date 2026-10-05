"""Independent saved-record F15 accounting audit; no clock/serializer imports.

Contributor: delegated ChatGPT (GPT-6 Astra Pro), execution audit.
The review adds zero principal time and writes only its own exclusive output.
"""
import csv
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN
import hashlib
import io
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
NS = 1_000_000_000
MINUTE = 60 * NS
PREFIX_SIZE = 203501
PREFIX_SHA = "7f777f89e0aff82d58752d0b1774c30e015fe9f3dbbf4faa1caae9b35c49988f"
checks = defaultdict(int)
inputs = {}


def check(group, value):
    checks[group] += 1
    if not value:
        raise ValueError(f"Failed independent accounting check: {group}")


def digest(b):
    return hashlib.sha256(b).hexdigest()


def read(path):
    b = path.read_bytes()
    inputs[path.relative_to(REPO).as_posix()] = {"bytes": len(b), "sha256": digest(b)}
    return b


def obj(name):
    return json.loads(read(ROOT / name), parse_float=Decimal)


def records(name):
    return [json.loads(line, parse_float=Decimal) for line in read(ROOT / name).splitlines()]


segments = records("segments.jsonl")
events = records("clocks.jsonl")
waits = records("adjustments.jsonl")
recoveries = records("recovery_exclusions.jsonl")
changes = records("mode_reclassifications.jsonl")
actual = obj("actuals.json")
integrity = obj("ledger_integrity.json")
intent = obj("finalization_intent.json")
forecast = obj("forecast.json")
check("closed_state", obj("clock_state.json") is None)
transitions = [e for e in events if e["command"] != "check"]
check("transition_count", len(transitions) == len(segments) + 1)
check("explicit_stop", transitions[-1]["command"] == "stop")
check("cutoff", transitions[-1]["utc"] == "2026-10-05T05:09:37.119388+00:00")
check("monotonic_events", all(a["monotonic_ns"] <= b["monotonic_ns"] for a, b in zip(events, events[1:])))

totals = dict.fromkeys(("D", "L", "E", "O", "wait", "recovery"), 0)
lanes = {"R": 0, "X": 0}
by_start, durations = {}, {}
for i, s in enumerate(segments):
    first, last = transitions[i:i+2]
    check("raw_transition", first["command"] in ("start", "switch", "resume", "pause"))
    check("endpoint_replay", (s["start_monotonic_ns"], s["end_monotonic_ns"], s["start_utc"], s["end_utc"]) ==
          (first["monotonic_ns"], last["monotonic_ns"], first["utc"], last["utc"]))
    paused = first["command"] == "pause"
    mode = "wait" if paused else first["args"][0]
    lane = "" if paused or first["args"][1] == "-" else first["args"][1]
    note = " ".join(first["args"] if paused else first["args"][2:])
    check("state_replay", (s["mode"], s["lane"], s["note"]) == (mode, lane, note))
    check("runtime", s["runtime"] == first["runtime"] == last["runtime"] == "linux-F15-S1")
    key = s["start_monotonic_ns"]
    n = s["end_monotonic_ns"] - key
    check("duration", type(key) is int and type(n) is int and n >= 0)
    check("elapsed_serialization", abs(Decimal(s["elapsed_seconds"]) * NS - n) <= 1)
    check("unique_segments", key not in by_start)
    if i:
        check("contiguous_nonoverlap", key == segments[i-1]["end_monotonic_ns"])
    by_start[key], durations[key] = s, n
    totals[mode] += n
    if mode in ("D", "L", "E"):
        check("raw_research_lane", lane in lanes)
        lanes[lane] += n
raw_totals = totals.copy()

# Reconcile aggregate time by transfers from the original mode totals. This
# differs from the serializer's construction of effective rows and supplies
# a second route to the same result.
exclusions = defaultdict(lambda: {"wait": 0, "recovery": 0})
normalizations, transfers = [], []
for kind, rows, field in (("wait", waits, "observed_wait_seconds"), ("recovery", recoveries, "seconds")):
    for row in rows:
        key = row["segment_start_monotonic_ns"]
        check("bound_exclusion", key in by_start and bool(row["reason"]))
        exact = Decimal(row[field]) * NS
        n = int(exact.to_integral_value(rounding=ROUND_HALF_EVEN))
        check("exclusion_resolution", n >= 0 and abs(Decimal(n)-exact) <= Decimal("0.5"))
        if Decimal(n) != exact:
            normalizations.append({"kind": kind, "start_monotonic_ns": key,
                                   "raw_seconds": str(row[field]), "normalized_ns": n,
                                   "delta_seconds": str((Decimal(n)-exact)/NS)})
        s = by_start[key]
        if kind == "recovery":
            check("recovery_binding", row["classification"] == "recovery" and
                  all(row[f] == s[f] for f in ("start_utc", "end_utc")))
        exclusions[key][kind] += n
        totals[s["mode"]] -= n
        totals[kind] += n
        if s["mode"] in ("D", "L", "E"):
            lanes[s["lane"]] -= n
        transfers.append({"reason": kind, "start_monotonic_ns": key, "from": s["mode"], "to": kind, "ns": n})

changed = {}
for row in changes:
    key = row["segment_start_monotonic_ns"]
    check("bound_reclassification", key in by_start and key not in changed)
    s = by_start[key]
    check("raw_reclassification", row["original_mode"] == s["mode"] and row["original_lane"] == s["lane"])
    n = durations[key] - sum(exclusions[key].values())
    check("nonnegative_remaining", n >= 0)
    totals[s["mode"]] -= n
    totals[row["mode"]] += n
    if s["mode"] in ("D", "L", "E"):
        lanes[s["lane"]] -= n
    if row["mode"] in ("D", "L", "E"):
        lanes[row["lane"]] += n
    changed[key] = row
    transfers.append({"reason": "reclassification", "start_monotonic_ns": key, "from": s["mode"], "to": row["mode"], "ns": n})

for key, s in by_start.items():
    mode = changed.get(key, s)["mode"]
    if mode == "wait" and s["note"].startswith("Artifact integrity recovery:"):
        n = durations[key] - sum(exclusions[key].values())
        totals["wait"] -= n
        totals["recovery"] += n
        transfers.append({"reason": "explicit_recovery_segment", "start_monotonic_ns": key, "from": "wait", "to": "recovery", "ns": n})

ledger = read(REPO / "v2/time_ledger.csv")
prefix, append = ledger[:PREFIX_SIZE], ledger[PREFIX_SIZE:]
check("historical_prefix", digest(prefix) == PREFIX_SHA)
check("intent_append", append == intent["append_csv_utf8"].encode())
old = list(csv.DictReader(io.StringIO(prefix.decode(), newline="")))
all_rows = list(csv.DictReader(io.StringIO(ledger.decode(), newline="")))
rows = all_rows[len(old):]
check("historical_rows", len(old) == 906 and all(r["task_id"] != "F15" for r in old))
check("row_count", len(rows) == len(segments) == 43)
check("row_task", all((r["task_id"], r["attempt_id"], r["session_id"]) == ("F15", "F15-A", "2026-10-04-S1") for r in rows))
row_totals = dict.fromkeys(totals, 0)
row_lanes = {"R": 0, "X": 0}
for s, row in zip(segments, rows):
    key = s["start_monotonic_ns"]
    amounts = {f: int(Decimal(row[f])*NS) for f in ("elapsed_seconds", "engaged_seconds", "tool_wait_seconds", "idle_seconds", "unmeasured_seconds")}
    check("row_endpoints", row["start_utc"] == s["start_utc"] and row["end_utc"] == s["end_utc"])
    check("row_elapsed", amounts["elapsed_seconds"] == durations[key])
    check("row_conservation", amounts["elapsed_seconds"] == sum(v for k,v in amounts.items() if k != "elapsed_seconds"))
    mode, lane = changed.get(key, s)["mode"], changed.get(key, s)["lane"]
    if mode == "wait" and s["note"].startswith("Artifact integrity recovery:"):
        mode = "recovery"
    left = durations[key] - sum(exclusions[key].values())
    check("row_nonnegative", left >= 0 and all(n >= 0 for n in amounts.values()))
    check("row_credit", amounts["engaged_seconds"] == (left if mode in ("D", "L", "E", "O") else 0))
    check("row_wait", amounts["tool_wait_seconds"] == exclusions[key]["wait"] + (left if mode == "wait" else 0))
    check("row_recovery", amounts["unmeasured_seconds"] == exclusions[key]["recovery"] + (left if mode == "recovery" else 0))
    check("row_mode_lane", row["mode"] == (mode if mode in ("D", "L", "E", "O") else "E" if mode == "wait" else "O") and row["lane"] == lane)
    row_totals[row["mode"]] += amounts["engaged_seconds"]
    row_totals["wait"] += amounts["tool_wait_seconds"]
    row_totals["recovery"] += amounts["unmeasured_seconds"]
    if row["lane"] in row_lanes:
        row_lanes[row["lane"]] += amounts["engaged_seconds"]

check("independent_totals", totals == row_totals == actual["exact_nanoseconds"])
check("independent_lanes", lanes == row_lanes == actual["lane_exact_nanoseconds"])
wall = segments[-1]["end_monotonic_ns"]-segments[0]["start_monotonic_ns"]
check("exact_wall_conservation", sum(totals.values()) == wall == actual["observed_wall_nanoseconds"])
engaged = sum(totals[k] for k in ("D", "L", "E", "O"))
research = sum(totals[k] for k in ("D", "L", "E"))
check("lane_conservation", sum(lanes.values()) == research)
check("E60_integer_floor", totals["E"] >= 60*MINUTE)
check("no_parallel_credit", actual["parallel_agent_minutes_added"] == integrity["parallel_agent_minutes_added"] == 0)
for k in totals:
    check("minute_serialization", abs(Decimal(actual["minutes"][k])*MINUTE-totals[k]) < Decimal("0.5"))
for key, n in (("engaged_minutes", engaged), ("research_minutes", research)):
    check("minute_serialization", abs(Decimal(actual[key])*MINUTE-n) < Decimal("0.5"))
entry = Decimal("636.727190")
close = entry + Decimal(engaged)/MINUTE
check("cumulative_entry", Decimal(actual["post_b_1"]["entry_minutes"]) == entry)
check("cumulative_close", Decimal(actual["post_b_1"]["close_minutes_decimal"]) == close)
check("checkpoint_remainder", Decimal(actual["post_b_1"]["remaining_minutes"]) == Decimal(960)-close)
check("no_reset", actual["post_b_1"]["recurrence_clock_reset"] is False)
check("inherited_overshoot", Decimal(actual["post_b_1"]["inherited_eight_hour_overshoot_minutes"]) == Decimal("54.976816"))
check("forecast_preserved", actual["central_forecast_minutes"] == forecast["central_minutes"] and actual["high_forecast_minutes"] == forecast["high_minutes"])
check("source_preserved", actual["source_revision"] == forecast["source_revision"] == "5388a3f9b0f18ad4f4e33d7e0cd04ea38f03e43e")
check("finalizer_output_binding", len(ledger) == integrity["observed_new_bytes"] and digest(ledger) == integrity["observed_new_sha256"])
for name in ("actuals.json", "ledger_integrity.json", "finalization_intent.json"):
    data = read(ROOT/name)
    check("output_sidecar", read(ROOT/(name+".sha256")).decode().strip() == digest(data))
for record in actual["raw_inputs"].values():
    data = read(REPO/record["path"])
    check("raw_input_preserved", len(data) == record["bytes"] and digest(data) == record["sha256"])
launch = obj("commands/finalize_accounting_attempt1.end.json")
check("single_launcher_success", launch["returncode"] == 0 and launch["started_monotonic_ns"] > segments[-1]["end_monotonic_ns"])
check("no_finalizer_retry", not any("finalize_accounting_attempt2" in p.name for p in (ROOT/"commands").iterdir()))
check("post_cutoff_administration", actual["uncredited_administrative_tail"] and integrity["administration_after_cutoff_credited"] is False)

result = {
    "schema": "F15-independent-final-accounting-review-v1", "passed": True,
    "contributor": "delegated ChatGPT (GPT-6 Astra Pro), execution audit",
    "audited_utc": datetime.now(timezone.utc).isoformat(), "principal_minutes_added": 0,
    "scope": "Saved raw-record arithmetic and ledger integrity; no clock command, serializer execution, experiment, or historical mutation.",
    "method": "Sum original raw-mode durations from integer endpoints, transfer explicit exclusions/reclassifications between mode totals, and independently sum and inspect all appended CSV rows.",
    "checks": dict(checks), "checks_total": sum(checks.values()), "raw_mode_nanoseconds": raw_totals,
    "accounted_nanoseconds": totals, "lane_nanoseconds": lanes,
    "minutes_decimal": {k: str(Decimal(n)/MINUTE) for k,n in totals.items()},
    "engaged_minutes_decimal": str(Decimal(engaged)/MINUTE), "research_minutes_decimal": str(Decimal(research)/MINUTE),
    "E_floor_excess_nanoseconds": totals["E"]-60*MINUTE,
    "E_floor_excess_seconds": str(Decimal(totals["E"]-60*MINUTE)/NS),
    "wall_nanoseconds": wall, "normalizations": normalizations, "accounting_transfers": transfers,
    "cutoff_utc": segments[-1]["end_utc"], "post_b_1_entry_minutes": str(entry),
    "post_b_1_close_minutes": str(close), "remaining_to_sixteen_hours_minutes": str(Decimal(960)-close),
    "historical_ledger": {"bytes": len(prefix), "sha256": digest(prefix), "rows": len(old)},
    "append": {"bytes": len(append), "sha256": digest(append), "rows": len(rows)},
    "current_ledger": {"bytes": len(ledger), "sha256": digest(ledger), "rows": len(all_rows)},
    "input_manifest": inputs, "review_script_sha256": digest(Path(__file__).read_bytes()),
    "limitation": "Observed timestamps and operator classifications are audited as preserved records; no independent historical activity trace, unrecorded interruption duration, or scientific/contribution gate pass is inferred."
}
target = ROOT / "accounting_final_review.json"
payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
with target.open("xb") as handle:
    handle.write(payload); handle.flush(); os.fsync(handle.fileno())
with Path(str(target)+".sha256").open("x") as handle:
    handle.write(digest(payload)+"\n"); handle.flush(); os.fsync(handle.fileno())
fd = os.open(ROOT, os.O_RDONLY)
try:
    os.fsync(fd)
finally:
    os.close(fd)
if target.read_bytes() != payload:
    raise ValueError("Review output did not survive exact reread")
print(json.dumps({"passed": True, "checks": sum(checks.values()), "E_ns": totals["E"],
                  "E_floor_excess_seconds": result["E_floor_excess_seconds"],
                  "engaged_minutes": result["engaged_minutes_decimal"], "review_sha256": digest(payload)}, indent=2))
