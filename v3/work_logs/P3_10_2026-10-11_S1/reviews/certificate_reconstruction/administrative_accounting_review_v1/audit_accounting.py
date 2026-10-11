"""Independent, read-only P3-10 administrative clock/ledger audit.

ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction, 2026-10-11.
No production clock, accounting script or scientific module is imported/run.
Raw commands are replayed as an in-memory state machine; no real clock starts.
All writes are confined to a new exclusive child of this review directory.
"""
from bisect import bisect_right
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import traceback

HERE = Path(__file__).resolve().parent
SESSION = HERE.parents[2]
ROOT = SESSION.parents[2]
W = SESSION.relative_to(ROOT)
BASE = "ea3e20dd9889c2ee22141c17390595867d33d8ab"
BASE_SHA = "6326ca24bbbc2958f176ae9c542a26a46aaae508a2ab711bcd0c8363a2a545b5"
MODES = ("D", "L", "E", "O", "wait", "idle", "unmeasured", "recovery")
RESEARCH = {"D", "L", "E"}
ENGAGED = RESEARCH | {"O"}
checks = []
read_cache = {}
mutable_document_paths = set()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compare(name, observed, expected):
    same = observed == expected
    entry = {"check": name, "pass": same}
    if not same:
        entry.update(observed=observed, expected=expected)
    checks.append(entry)
    return same


def require(name, predicate):
    compare(name, bool(predicate), True)
    if not predicate:
        raise AssertionError(name)


def read_bytes(path):
    relative = str(path)
    if relative not in read_cache:
        read_cache[relative] = (ROOT / relative).read_bytes()
    return read_cache[relative]


def read_json(path):
    return json.loads(read_bytes(path))


def jsonl(path):
    return [json.loads(line) for line in read_bytes(path).decode().splitlines()]


def utc(value):
    parsed = datetime.fromisoformat(value)
    require("UTC timezone declared: " + value, parsed.utcoffset().total_seconds() == 0)
    return parsed


def seconds_string(ns):
    integer, remainder = divmod(ns, 1_000_000_000)
    return str(integer) + "." + str(remainder).zfill(9)


def minutes_string(ns):
    # 10^12 / (60*10^9) = 50/3. No half-way rounding case can occur.
    scaled, remainder = divmod(ns * 50, 3)
    scaled += remainder == 2
    integer, decimal = divmod(scaled, 1_000_000_000_000)
    return str(integer) + "." + str(decimal).zfill(12)


def percentage(ns, total):
    with localcontext() as context:
        context.prec = 48
        return str(Decimal(100) * ns / total)


def check_links(path):
    data = read_bytes(path).decode()
    mutable_document_paths.add(str(path))
    links = []
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", data):
        target = target.split("#", 1)[0]
        if not target or re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target):
            continue
        resolved = (ROOT / path).parent / target
        exists = resolved.exists()
        compare("local artifact link: " + str(path) + " -> " + target, exists, True)
        links.append({"target": target, "resolved": str(resolved.resolve()), "exists": exists})
    return links


def audit(output):
    events = jsonl(W / "clocks.jsonl")
    raw = jsonl(W / "segments.jsonl")
    corrections = jsonl(W / "clock_dispositions.jsonl")
    saved_effective = read_json(W / "effective_segments.json")
    actuals = read_json(W / "actuals.json")
    prior_path = Path("v3/work_logs/P3_09_2026-10-11_S1/actuals.json")
    prior = read_json(prior_path)
    forecast = read_json(W / "forecast.json")
    preclose = read_json(W / "actuals_preclose.json")
    prepared = read_json(W / "accounting_prepared.json")
    completion = read_json(W / "accounting_completion.json")
    control_error = read_json(W / "clock_control_error_01.json")
    compare("stopped state is JSON null", read_json(W / "clock_state.json"), None)
    compare("event count", len(events), 72)
    compare("raw interval count", len(raw), 50)
    compare("first event is start", events[0]["command"], "start")
    compare("last event is stop", events[-1]["command"], "stop")
    runtimes = {event["runtime"] for event in events}
    compare("one recorded runtime", len(runtimes), 1)
    runtime = events[0]["runtime"]
    compare("actuals runtime", actuals["runtime"], runtime)
    compare("event instants unique", len({e["monotonic_ns"] for e in events}), len(events))
    for left, right in zip(events, events[1:]):
        require("strictly increasing event monotonic times", left["monotonic_ns"] < right["monotonic_ns"])
        require("strictly increasing event UTC times", utc(left["utc"]) < utc(right["utc"]))

    # Reconstruct raw intervals from command semantics, independently of clock.py.
    reconstructed_raw = []
    state = None
    starts = 0
    for i, event in enumerate(events):
        command, args = event["command"], event["args"]
        if command == "check":
            require("check has an open interval", state is not None)
            continue
        if command == "start":
            starts += 1
            require("start occurs only first with no open interval", i == 0 and state is None)
        elif command == "resume":
            require("resume only from excluded mode or closed state", state is None or state["mode"] in set(MODES) - ENGAGED)
        else:
            require("transition has open interval", state is not None)
        if state is not None:
            reconstructed_raw.append({**state, "end_utc": event["utc"],
                                      "end_monotonic_ns": event["monotonic_ns"],
                                      "elapsed_ns": event["monotonic_ns"] - state["start_monotonic_ns"]})
        if command == "stop":
            require("stop is final event", i == len(events) - 1)
            state = None
            continue
        if command == "pause":
            mode, lane, note = args[0], "", " ".join(args[1:])
            require("pause category excluded", mode in set(MODES) - ENGAGED)
        else:
            require("recognized research/admin transition", command in {"start", "resume", "switch"})
            mode, lane, note = args[0], args[1], " ".join(args[2:])
            require("active category and lane", (mode in RESEARCH and lane in {"R", "X"}) or (mode == "O" and lane == "-"))
            lane = "" if lane == "-" else lane
        state = {"mode": mode, "lane": lane, "note": note,
                 "start_utc": event["utc"], "start_monotonic_ns": event["monotonic_ns"], "runtime": runtime}
    compare("exactly one start", starts, 1)
    compare("reconstructed clock stopped", state, None)
    compare("all raw interval fields reconstructed from events", reconstructed_raw, raw)

    by_ns = {e["monotonic_ns"]: e for e in events}
    compare("disposition count", len(corrections), 8)
    compare("unique disposition IDs", len({c["id"] for c in corrections}), 8)
    ordered = sorted(corrections, key=lambda c: c["start_monotonic_ns"])
    for left, right in zip(ordered, ordered[1:]):
        require("dispositions never overlap", left["end_monotonic_ns"] <= right["start_monotonic_ns"])
    disposition_rows = []
    for c in corrections:
        lo, hi = c["start_monotonic_ns"], c["end_monotonic_ns"]
        require("positive disposition duration", lo < hi)
        require("both disposition boundaries are actual recorded events", lo in by_ns and hi in by_ns)
        compare("disposition start UTC bound to event", c["start_utc"], by_ns[lo]["utc"])
        compare("disposition end UTC bound to event", c["end_utc"], by_ns[hi]["utc"])
        compare("disposition runtime", c["runtime"], runtime)
        containing = [i for i,s in enumerate(reconstructed_raw) if s["start_monotonic_ns"] <= lo < hi <= s["end_monotonic_ns"]]
        require("disposition contained in exactly one raw interval", len(containing) == 1)
        raw_index = containing[0]
        compare("disposition original category", c["original_mode"], reconstructed_raw[raw_index]["mode"])
        require("disposition cannot add research credit", c["original_mode"] in RESEARCH and c["mode"] in {"O", "recovery", "unmeasured"} and c["lane"] == "")
        disposition_rows.append({"id": c["id"], "raw_segment_index": raw_index,
                                 "from": c["original_mode"], "to": c["mode"],
                                 "elapsed_ns": hi-lo, "start_utc": c["start_utc"], "end_utc": c["end_utc"]})

    # Global boundary overlay, rather than the principal's per-segment splitter.
    raw_starts = [s["start_monotonic_ns"] for s in reconstructed_raw]
    boundaries = set(raw_starts) | {reconstructed_raw[-1]["end_monotonic_ns"]}
    boundaries |= {c[edge] for c in corrections for edge in ("start_monotonic_ns", "end_monotonic_ns")}
    points = sorted(boundaries)
    rebuilt = []
    for lo, hi in zip(points, points[1:]):
        index = bisect_right(raw_starts, lo) - 1
        original = reconstructed_raw[index]
        require("overlay interval remains inside raw interval", original["start_monotonic_ns"] <= lo < hi <= original["end_monotonic_ns"])
        cover = [c for c in corrections if c["start_monotonic_ns"] <= lo and hi <= c["end_monotonic_ns"]]
        require("at most one covering disposition", len(cover) <= 1)
        replacement = cover[0] if cover else None
        piece = {"mode": replacement["mode"] if replacement else original["mode"],
                 "lane": replacement["lane"] if replacement else original["lane"],
                 "note": replacement["reason"] if replacement else original["note"],
                 "start_utc": by_ns[lo]["utc"], "end_utc": by_ns[hi]["utc"],
                 "start_monotonic_ns": lo, "end_monotonic_ns": hi,
                 "elapsed_ns": hi-lo, "runtime": runtime, "raw_segment_index": index}
        if replacement:
            piece["disposition_id"] = replacement["id"]
        rebuilt.append(piece)
    compare("effective interval count", len(rebuilt), 51)
    compare("all effective interval fields independently reconstructed", rebuilt, saved_effective)
    for left, right in zip(rebuilt, rebuilt[1:]):
        compare("effective intervals contiguous without overlap", left["end_monotonic_ns"], right["start_monotonic_ns"])

    totals = {mode: 0 for mode in MODES}
    lanes = {"R": 0, "X": 0}
    heartbeat_gaps = []
    for piece in rebuilt:
        duration = piece["elapsed_ns"]
        totals[piece["mode"]] += duration
        if piece["mode"] in RESEARCH:
            require("only R/X on credited research", piece["lane"] in lanes)
            lanes[piece["lane"]] += duration
        else:
            compare("nonresearch carries no lane credit", piece["lane"], "")
        if piece["mode"] in ENGAGED:
            instants = [e["monotonic_ns"] for e in events if piece["start_monotonic_ns"] <= e["monotonic_ns"] <= piece["end_monotonic_ns"]]
            heartbeat_gaps.extend(b-a for a,b in zip(instants, instants[1:]))
    total_span = events[-1]["monotonic_ns"] - events[0]["monotonic_ns"]
    compare("all observed elapsed time conserved exactly", sum(totals.values()), total_span)
    compare("raw elapsed time conserved exactly", sum(r["elapsed_ns"] for r in raw), total_span)
    research = sum(totals[m] for m in RESEARCH)
    engaged = research + totals["O"]
    compare("independent research equals lane sum", research, sum(lanes.values()))
    compare("expected final research nanoseconds", research, 5_417_014_164_347)
    compare("expected D nanoseconds", totals["D"], 1_517_688_942_982)
    compare("expected E nanoseconds", totals["E"], 3_899_325_221_365)
    compare("all actuals category nanoseconds", actuals["category_ns"], totals)
    compare("all actuals category minutes", actuals["category_minutes"], {m:minutes_string(n) for m,n in totals.items()})
    compare("actuals research lanes", actuals["lane_research_ns"], lanes)
    compare("actuals lane minutes", actuals["lane_research_minutes"], {k:minutes_string(v) for k,v in lanes.items()})
    compare("actuals lane percentages", actuals["lane_percent"], {k:percentage(v,research) for k,v in lanes.items()})
    for key in ("research_ns", "task_research_ns"):
        compare(key, actuals[key], research)
    for key in ("research_minutes", "task_research_minutes"):
        compare(key, actuals[key], minutes_string(research))
    compare("Research90 reached", research >= 5_400_000_000_000, True)
    compare("task floor margin", actuals["task_floor_margin_ns"], research - 5_400_000_000_000)
    compare("engaged nanoseconds", actuals["total_engaged_ns"], engaged)
    compare("engaged minutes", actuals["total_engaged_minutes"], minutes_string(engaged))
    compare("maximum active heartbeat gap", actuals["maximum_observed_active_gap_ns"], max(heartbeat_gaps))
    compare("all active heartbeat gaps at most fifteen minutes", max(heartbeat_gaps) <= 900_000_000_000, True)
    compare("no declared cadence violations", actuals["cadence_violations"], [])
    for key in ("recorded_start_utc", "recorded_start_monotonic_ns", "recorded_end_utc", "recorded_end_monotonic_ns"):
        event = events[0] if "start" in key else events[-1]
        field = "utc" if key.endswith("utc") else "monotonic_ns"
        compare(key, actuals[key], event[field])
    last_research = [p for p in rebuilt if p["mode"] in RESEARCH][-1]
    compare("research closing UTC", actuals["research_closed_utc"], last_research["end_utc"])
    compare("research closing monotonic instant", actuals["research_closed_monotonic_ns"], last_research["end_monotonic_ns"])
    compare("nothing after research boundary earns research", all(p["mode"] not in RESEARCH for p in rebuilt if p["start_monotonic_ns"] >= last_research["end_monotonic_ns"]), True)
    error_time = utc(control_error["utc"])
    error_intervals = [p for p in rebuilt if utc(p["start_utc"]) <= error_time < utc(p["end_utc"])]
    compare("preserved control error lies in one O interval", [p["mode"] for p in error_intervals], ["O"])
    compare("control error research credit zero", control_error["principal_credit_for_error_interval"], 0)

    two_lanes = {lane: lanes[lane] + prior["lane_research_ns"][lane] for lane in lanes}
    two_total = research + prior["research_ns"]
    compare("two-cycle research equals two lane totals", two_total, sum(two_lanes.values()))
    compare("two-cycle lane ns", actuals["two_cycle_lane_ns"], two_lanes)
    compare("two-cycle research ns", actuals["two_cycle_research_ns"], two_total)
    compare("two-cycle lane percentages", actuals["two_cycle_lane_percent"], {k:percentage(v,two_total) for k,v in two_lanes.items()})
    for lane,value in two_lanes.items():
        compare("two-cycle " + lane + " at least 25 percent by integer comparison", 4*value >= two_total, True)
    phase_research = prior["phase_research_ns"] + research
    phase_engaged = prior["phase_measured_engaged_ns"] + engaged
    compare("phase research ns", actuals["phase_research_ns"], phase_research)
    compare("expected phase research ns", phase_research, 65_167_882_041_849)
    compare("phase research minutes", actuals["phase_research_minutes"], minutes_string(phase_research))
    compare("phase engaged ns", actuals["phase_measured_engaged_ns"], phase_engaged)
    compare("prior phase research preserved", actuals["prior_phase_research_ns"], prior["phase_research_ns"])
    compare("prior phase engaged preserved", actuals["prior_phase_measured_engaged_ns"], prior["phase_measured_engaged_ns"])
    compare("phase floor overshoot", actuals["phase_floor_overshoot_ns"], phase_research - 57_600_000_000_000)
    for key in ("historical_recredit_ns", "parallel_reviewer_credit_ns", "agent_overlap_added_ns", "prior_verified_task_research_ns", "remaining_research_floor_ns", "task_remaining_floor_ns", "phase_remaining_floor_ns"):
        compare("zero credit or remaining floor: " + key, actuals[key], 0)
    for key in ("clock_stopped", "research_floor_satisfied", "two_cycle_lane_floor_satisfied", "phase_research_floor_satisfied"):
        compare(key, actuals[key], True)
    for key in ("ledger_append_pending", "additional_recurrence_selected", "lane_repair_emergency", "new_phase_checkpoint_crossed", "global_positive_end_to_end_economic_gate", "original_confirmatory_full_500_run_complete"):
        compare(key, actuals[key], False)
    compare("protected floor", actuals["research_floor_ns"], forecast["research_floor_minutes"] * 60_000_000_000)
    compare("forecast central copied unchanged", actuals["forecast_central_minutes"], forecast["central_minutes"])
    compare("forecast high copied unchanged", actuals["forecast_high_minutes"], forecast["high_minutes"])
    with localcontext() as context:
        context.prec = 48
        errors = {k:str(Decimal(totals[k])/Decimal(60_000_000_000)-v) for k,v in forecast["central_minutes"].items()}
    compare("forecast errors", actuals["forecast_error_minutes"], errors)
    compare("preclose retained as in-progress", preclose["status"], "in_progress")
    compare("prepared actuals exactly equal completed actuals", prepared["actuals"], actuals)
    compare("completion status", completion["status"], "PASS")
    compare("completion research", completion["research_ns"], research)
    compare("completion actuals hash", completion["actuals_sha256"], sha(read_bytes(W / "actuals.json")))
    compare("eight dispositions declared", actuals["clock_dispositions"]["count"], len(corrections))

    # git show is a read-only byte source; no command from the project is run.
    base_ledger = subprocess.run(["git", "show", BASE + ":v3/time_ledger.csv"], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    base_prior = subprocess.run(["git", "show", BASE + ":" + str(prior_path)], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    compare("prior actuals are unchanged from entry commit", read_bytes(prior_path), base_prior)
    ledger = read_bytes("v3/time_ledger.csv")
    append = read_bytes(W / "ledger_append.csv")
    compare("base ledger pinned bytes", len(base_ledger), 200471)
    compare("base ledger pinned SHA256", sha(base_ledger), BASE_SHA)
    compare("prior ledger retained as exact prefix", ledger[:len(base_ledger)], base_ledger)
    compare("ledger is exactly original plus one append", ledger, base_ledger + append)
    compare("append byte count", len(append), 19928)
    header_reader = csv.DictReader(io.StringIO(base_ledger.decode()))
    header = header_reader.fieldnames
    base_rows = list(header_reader)
    appended_rows = list(csv.DictReader(io.StringIO(append.decode()), fieldnames=header))
    full_rows = list(csv.DictReader(io.StringIO(ledger.decode())))
    compare("base ledger row count", len(base_rows), 484)
    compare("append row count", len(appended_rows), 51)
    compare("complete ledger row count", len(full_rows), 535)
    compare("no old P3-10 ledger rows", [r for r in base_rows if r["task_id"] == "P3-10"], [])
    compare("all new rows belong to this principal task/attempt/session", {(r["task_id"],r["attempt_id"],r["session_id"]) for r in appended_rows}, {("P3-10","P3-10-1","2026-10-11-S1")})
    expected_rows = []
    artifact_path = "v3/work_logs/P3_10_2026-10-11_S1.md"
    for i,(row,piece) in enumerate(zip(appended_rows,rebuilt)):
        n, mode = piece["elapsed_ns"], piece["mode"]
        status = "Closed observed P3-10 principal interval; " + piece["note"]
        if "disposition_id" in piece:
            status += "; disposition=" + piece["disposition_id"]
        values = ["P3-10", "P3-10-1", "2026-10-11-S1", mode, piece["lane"], piece["start_utc"], piece["end_utc"], seconds_string(n),
                  seconds_string(n if mode in ENGAGED else 0), seconds_string(n if mode == "wait" else 0),
                  seconds_string(n if mode == "idle" else 0), seconds_string(n if mode in {"unmeasured","recovery"} else 0), "0", artifact_path, status]
        expected_rows.append(values)
        compare("every CSV field for reconstructed interval " + str(i), row, dict(zip(header,values)))
        allocations = sum(Fraction(row[k]) for k in ("engaged_seconds","tool_wait_seconds","idle_seconds","unmeasured_seconds"))
        compare("CSV allocations partition elapsed interval " + str(i), allocations, Fraction(n,1_000_000_000))
    serialized = io.StringIO(newline="")
    csv.writer(serialized, lineterminator="\n").writerows(expected_rows)
    compare("independent CSV serialization equals exact appended bytes", serialized.getvalue().encode(), append)
    declared_ledger = {"base_bytes":len(base_ledger), "base_rows":len(base_rows), "base_sha256":sha(base_ledger),
                       "append_bytes":len(append), "append_rows":len(appended_rows), "append_sha256":sha(append),
                       "result_sha256":sha(ledger), "prior_bytes_preserved":True}
    compare("actuals ledger metadata", actuals["ledger"], declared_ledger)
    compare("prepared append hash", prepared["ledger_append_sha256"], sha(append))
    compare("completion ledger hash", completion["ledger_sha256"], sha(ledger))
    for field,path in {
        "clock_source_sha256":W/"clock.py", "clock_events_sha256":W/"clocks.jsonl", "clock_segments_sha256":W/"segments.jsonl",
        "clock_dispositions_sha256":W/"clock_dispositions.jsonl", "accounting_source_sha256":W/"close_accounting.py",
        "phase_two_ledger_sha256":Path("v2/time_ledger.csv"), "freeze_manifest_sha256":Path("v3/experiments/frozen_v1/manifest.json"),
        "freeze_protocol_sha256":Path("v3/experiments/protocol.v1.json")}.items():
        compare("declared source binding: " + field, actuals[field], sha(read_bytes(path)))
    for path in (artifact_path, actuals["checkpoint_record"], forecast["principal_artifact"], str(W / actuals["clock_dispositions"]["file"])):
        compare("linked artifact exists: " + path, (ROOT/path).is_file(), True)
    session_links = check_links(Path(artifact_path))
    compare("all append forecast allocations are zero", {r["forecast_seconds"] for r in appended_rows}, {"0"})
    compare("no intervals beyond stopped clock admitted", max(p["end_monotonic_ns"] for p in rebuilt), events[-1]["monotonic_ns"])
    (output / "entry_commit_ledger.csv").write_bytes(base_ledger)
    (output / "independently_reconstructed_effective_segments.json").write_text(json.dumps(rebuilt,indent=2,sort_keys=True)+"\n")
    for relative,data in list(read_cache.items()):
        if relative not in mutable_document_paths:
            compare("read-only source unchanged through audit: " + relative, (ROOT/relative).read_bytes(), data)
    return {"event_count":len(events), "raw_segments":len(raw), "effective_segments":len(rebuilt),
            "dispositions":disposition_rows, "observed_span_ns":total_span, "category_ns":totals,
            "research_ns":research, "research_minutes":minutes_string(research), "engaged_ns":engaged,
            "engaged_minutes":minutes_string(engaged), "task_floor_margin_ns":research-5_400_000_000_000,
            "lane_research_ns":lanes, "two_cycle_lane_ns":two_lanes, "two_cycle_research_ns":two_total,
            "two_cycle_lane_percent":{k:percentage(v,two_total) for k,v in two_lanes.items()},
            "phase_research_ns":phase_research, "phase_research_minutes":minutes_string(phase_research),
            "phase_engaged_ns":phase_engaged, "maximum_active_gap_ns":max(heartbeat_gaps),
            "research_closed_utc":last_research["end_utc"], "clock_stopped_utc":events[-1]["utc"],
            "ledger":declared_ledger, "session_document_links":session_links,
            "administrative_and_agent_research_credit_ns":0,
            "limitations":["Validates recorded principal observations and arithmetic; does not independently observe historical attention or CPU activity.",
                           "Concurrent root status/control synchronization and later publication are separate from the stopped accounting interval.",
                           "Reads clock/accounting source without importing it; executes no scientific method or existing observer."]}


def fallback(value):
    if isinstance(value, bytes):
        return {"bytes":len(value), "sha256":sha(value)}
    if isinstance(value, set):
        return sorted(value)
    if isinstance(value, Fraction):
        return [value.numerator,value.denominator]
    return str(value)


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "run_01"
    if not re.fullmatch(r"run_[0-9]+", name):
        raise ValueError("Exclusive output must be an owned run_NN child.")
    output = HERE / name
    output.mkdir(exist_ok=False)
    start = datetime.now(timezone.utc).isoformat()
    result = {"schema":"P3-10-independent-administrative-accounting-audit-v1", "reviewer":"/root/certificate_reconstruction",
              "started_utc":start, "source_sha256":sha(Path(__file__).read_bytes()),
              "scientific_methods_executed":0, "existing_observers_executed":0, "agents_started":0,
              "principal_research_credit_ns":0, "core_accounting_records_modified":False}
    error = None
    try:
        result["reconstruction"] = audit(output)
    except Exception as exc:
        error = {"type":type(exc).__name__, "message":str(exc)}
        (output/"failure_traceback.txt").write_text(traceback.format_exc())
    failures = [entry for entry in checks if not entry["pass"]]
    result.update(status="PASS" if not failures and error is None else "FAIL", finished_utc=datetime.now(timezone.utc).isoformat(),
                  checks=len(checks), failed_checks=len(failures), failures=failures, exception=error)
    inventory=[]
    for relative,data in read_cache.items():
        target=output/"source_snapshot"/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
        inventory.append({"path":relative,"bytes":len(data),"sha256":sha(data),"concurrent_root_document":relative in mutable_document_paths})
    inventory_bytes=(json.dumps(inventory,indent=2,sort_keys=True)+"\n").encode()
    (output/"source_hashes.json").write_bytes(inventory_bytes)
    result["source_hashes_sha256"]=sha(inventory_bytes)
    (output/"checks.json").write_text(json.dumps(checks,indent=2,sort_keys=True,default=fallback)+"\n")
    result_bytes=(json.dumps(result,indent=2,sort_keys=True,default=fallback)+"\n").encode()
    (output/"results.json").write_bytes(result_bytes)
    print(json.dumps({"status":result["status"],"checks":len(checks),"failed_checks":len(failures),"exception":error,
                      "results_sha256":sha(result_bytes),"source_sha256":result["source_sha256"]},sort_keys=True))
    return 0 if result["status"]=="PASS" else 1


if __name__=="__main__":
    sys.exit(main())
