"""Independent, read-only F15-ND01 accounting audit.

Contributor: delegated ChatGPT (GPT-6 Astra Pro), protocol/accounting audit.
Uses only the standard library; does not import or invoke the clock or ledger
serializer. --final requires a stopped clock and finalized accounting. --save
writes only this auditor's audit_accounting_{preclose,final}.{json,md} files.
Auditor/parallel-agent minutes are never added to principal time.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
import hashlib
import io
import json
from pathlib import Path
import subprocess

getcontext().prec = 50
SESSION = Path(__file__).resolve().parent
REPO = SESSION.parents[2]
BASE_COMMIT = "9f42a047126618b0364cf334002f846e5839d726"
BASE_BYTES = 217776
BASE_ROWS = 949
BASE_SHA = "44c93cc930fdea2d588f663688e71615a84b32f98517eadd4bab3943efa154bd"
ENTRY = Decimal("701.64299296445")
CHECKPOINT = Decimal(960)
NS = 1_000_000_000
MNS = 60 * NS
RUNTIME = "linux-F15-ND01-S1"
MODES = ("D", "L", "E", "O", "wait", "recovery")
RESEARCH = ("D", "L", "E")
NAMES = ("clocks.jsonl", "segments.jsonl", "clock_state.json", "forecast.json",
         "ledger_baseline.json", "adjustments.jsonl", "recovery_exclusions.jsonl",
         "mode_reclassifications.jsonl", "actuals.json", "ledger_integrity.json",
         "finalization_intent.json")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"Duplicate JSON key: {key}")
        out[key] = value
    return out


def decode(data):
    return json.loads(data, parse_float=Decimal, object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def utc(text):
    value = datetime.fromisoformat(text)
    if value.utcoffset() is None or value.utcoffset().total_seconds() != 0:
        raise ValueError(f"Non-UTC timestamp: {text}")
    return value


def audit(final=False):
    checks = []
    errors = []
    warnings = []

    def check(value, name):
        checks.append(name)
        if not value:
            errors.append(name)

    def approximately(value, expected, name, tolerance=Decimal("1e-9")):
        check(abs(Decimal(str(value)) - expected) <= tolerance, name)

    raw = {name: (SESSION / name).read_bytes() if (SESSION / name).exists() else None
           for name in NAMES}
    ledger = (REPO / "v2/time_ledger.csv").read_bytes()
    # Bind the historical prefix to the actual preserved Git object as well as
    # to the recorded SHA; no checkout, fetch, or other mutation is performed.
    prior = subprocess.check_output(
        ["git", "show", f"{BASE_COMMIT}:v2/time_ledger.csv"], cwd=REPO)
    check(len(prior) == BASE_BYTES and sha(prior) == BASE_SHA, "Git baseline size/hash")
    check(ledger[:BASE_BYTES] == prior, "All historical ledger bytes preserved")
    old_rows = list(csv.DictReader(io.StringIO(prior.decode(), newline="")))
    check(len(old_rows) == BASE_ROWS, "Historical ledger has exactly 949 data rows")
    check(not any(r["task_id"] == "F15-ND01" for r in old_rows), "No prior ND01 rows reused")

    def document(name):
        if raw[name] is None:
            raise ValueError(f"Required source missing: {name}")
        return decode(raw[name])

    def records(name):
        if raw[name] is None:
            return []
        return [decode(line) for line in raw[name].splitlines() if line.strip()]

    baseline = document("ledger_baseline.json")
    check(baseline["ledger_bytes"] == BASE_BYTES and baseline["ledger_rows"] == BASE_ROWS
          and baseline["ledger_sha256"] == BASE_SHA, "Baseline declaration unchanged")
    check(Decimal(baseline["post_b_1_entry_minutes_decimal"]) == ENTRY,
          "POST-B-1 entry preserved without reset")
    check(baseline["post_b_1_remaining_minutes"] == CHECKPOINT - ENTRY,
          "Starting checkpoint remainder correct")
    forecast = document("forecast.json")
    central = {"D": 10, "L": 10, "E": 70, "O": 10, "engaged": 100, "research": 90, "wait": 3}
    high = {"D": 15, "L": 15, "E": 90, "O": 15, "engaged": 135, "research": 120, "wait": 10}
    check(forecast["central_minutes"] == central and forecast["high_minutes"] == high,
          "Original central/high mode forecasts preserved")
    check(forecast["protected_minimum"] == {"mode": "D+L+E", "minutes": 90},
          "Fresh Research90 obligation preserved")
    check(forecast["lane_percent"] == {"R": 60, "X": 40}, "Original R/X forecast preserved")
    check(forecast["parallel_agent_minutes_added"] == 0, "Forecast adds zero parallel time")
    check(forecast["task"] == "F15-ND01" and forecast["attempt"] == "F15-ND01-A1"
          and forecast["session"] == "2026-10-05-S1" and forecast["runtime"] == RUNTIME,
          "Forecast task/session/runtime identity")

    events = records("clocks.jsonl")
    segments = records("segments.jsonl")
    check(bool(events) and bool(segments), "Principal observations exist")
    check(events[0]["utc"] == "2026-10-05T16:29:47.117754+00:00"
          and events[0]["command"] == "start", "Fresh observed clock start")
    check(utc(forecast["created_utc"]) < utc(events[0]["utc"]), "Forecast predates clock")
    expected = []
    state = None
    previous = None
    for i, event in enumerate(events):
        now = event["monotonic_ns"]
        check(type(now) is int and (previous is None or now >= previous), f"Event {i}: monotonic time")
        check(event["runtime"] == RUNTIME, f"Event {i}: common runtime")
        utc(event["utc"])
        previous = now
        if event["command"] == "check":
            continue
        if state is not None:
            expected.append(dict(state, end_utc=event["utc"], end_monotonic_ns=now))
        command, args = event["command"], event["args"]
        if command in ("start", "switch", "resume"):
            mode, lane = args[:2]
            state = dict(mode=mode, lane="" if lane == "-" else lane,
                         start_utc=event["utc"], start_monotonic_ns=now,
                         note=" ".join(args[2:]), runtime=RUNTIME)
        elif command == "pause":
            state = dict(mode="wait", lane="", start_utc=event["utc"],
                         start_monotonic_ns=now, note=" ".join(args), runtime=RUNTIME)
        elif command == "stop":
            state = None
        else:
            raise ValueError(f"Unexpected clock event {command}")
    check(document("clock_state.json") == state, "Current clock state equals event replay")
    check(len(expected) == len(segments), "Exactly one raw segment per closed transition")
    for i, (wanted, got) in enumerate(zip(expected, segments)):
        check(all(got.get(k) == v for k, v in wanted.items()), f"Segment {i}: event replay equality")
        elapsed = got["end_monotonic_ns"] - got["start_monotonic_ns"]
        check(elapsed >= 0, f"Segment {i}: nonnegative duration")
        approximately(got["elapsed_seconds"], Decimal(elapsed)/NS,
                      f"Segment {i}: saved seconds match integer endpoints", Decimal("1e-9"))
        if i:
            check(got["start_monotonic_ns"] == segments[i-1]["end_monotonic_ns"]
                  and got["start_utc"] == segments[i-1]["end_utc"], f"Segment {i}: contiguous, no overlap")
    closed = state is None and events[-1]["command"] == "stop"
    if final:
        check(closed, "Final accounting has an explicitly stopped clock")

    by_start = {s["start_monotonic_ns"]: s for s in segments}
    check(len(by_start) == len(segments), "Unique closed segment keys")
    exclusions = {name: {} for name in ("wait", "recovery")}
    normalizations = []
    for filename, field, category in (("adjustments.jsonl", "observed_wait_seconds", "wait"),
                                     ("recovery_exclusions.jsonl", "seconds", "recovery")):
        for i, record in enumerate(records(filename)):
            key = record["segment_start_monotonic_ns"]
            check(key in by_start, f"{filename}:{i}: binds observed segment")
            check(bool(record.get("reason", "").strip()), f"{filename}:{i}: reason preserved")
            seconds = Decimal(str(record[field]))
            ns = int((seconds * NS).to_integral_value(rounding=ROUND_HALF_EVEN))
            delta = Decimal(ns)/NS - seconds
            check(seconds.is_finite() and seconds >= 0 and abs(delta) <= Decimal("5e-10"),
                  f"{filename}:{i}: nonnegative nanosecond-resolved exclusion")
            exclusions[category][key] = exclusions[category].get(key, 0) + ns
            if delta:
                normalizations.append({"record": f"{filename}:{i+1}", "delta_seconds": str(delta)})
    changes = {}
    for i, change in enumerate(records("mode_reclassifications.jsonl")):
        key = change["segment_start_monotonic_ns"]
        check(key in by_start and key not in changes, f"Reclassification {i}: unique observed segment")
        original = by_start[key]
        check(change["original_mode"] == original["mode"] and change["original_lane"] == original["lane"],
              f"Reclassification {i}: original mode/lane preserved")
        check(bool(change.get("reason", "").strip()), f"Reclassification {i}: reason preserved")
        check(original["mode"] in (*RESEARCH, "O") or change["mode"] not in (*RESEARCH, "O"),
              f"Reclassification {i}: excluded time not promoted to engaged")
        changes[key] = change

    totals = dict.fromkeys(MODES, 0)
    lanes = dict.fromkeys(("R", "X"), 0)
    rows_expected = []
    for i, segment in enumerate(segments):
        key = segment["start_monotonic_ns"]
        elapsed = segment["end_monotonic_ns"] - key
        wait = exclusions["wait"].get(key, 0)
        recovery = exclusions["recovery"].get(key, 0)
        remaining = elapsed - wait - recovery
        check(remaining >= 0, f"Segment {i}: exclusions do not overlap beyond duration")
        mode = changes.get(key, segment)["mode"]
        lane = changes.get(key, segment)["lane"]
        if mode == "wait" and segment["note"].startswith("Artifact integrity recovery:"):
            mode = "recovery"
        check(mode in MODES and (lane in ("R", "X") if mode in RESEARCH else lane == ""),
              f"Segment {i}: effective mode/lane valid")
        totals[mode] += remaining
        totals["wait"] += wait
        totals["recovery"] += recovery
        if mode in RESEARCH:
            lanes[lane] += remaining
        engaged = remaining if mode in (*RESEARCH, "O") else 0
        wait += remaining if mode == "wait" else 0
        recovery += remaining if mode == "recovery" else 0
        check(engaged + wait + recovery == elapsed, f"Segment {i}: exact conservation")
        rows_expected.append(dict(segment=segment, mode=mode, lane=lane, elapsed=elapsed,
                                  engaged=engaged, wait=wait, recovery=recovery))
    research = sum(totals[k] for k in RESEARCH)
    engaged = research + totals["O"]
    wall = sum(totals.values())
    check(sum(lanes.values()) == research, "Research counted once on R/X axis")
    check(wall == sum(s["end_monotonic_ns"]-s["start_monotonic_ns"] for s in segments),
          "Total observed time conserved")
    if final:
        check(research >= 90 * MNS, "Research90 proven by integer nanoseconds, excluding O/waits/recovery")

    gap_reviews = []
    for first, last in zip(events, events[1:]):
        gap = last["monotonic_ns"] - first["monotonic_ns"]
        covering = [r for r in rows_expected if r["segment"]["start_monotonic_ns"] <= first["monotonic_ns"]
                    and r["segment"]["end_monotonic_ns"] >= last["monotonic_ns"]]
        if gap > 15 * MNS and covering and covering[0]["engaged"] > 0:
            gap_reviews.append({"start_utc": first["utc"], "end_utc": last["utc"], "gap_ns": gap})
    check(not gap_reviews, "No unqualified active observation gap exceeds 15 minutes")

    appended = ledger[BASE_BYTES:]
    ledger_rows = list(csv.DictReader(io.StringIO(ledger.decode(), newline="")))[BASE_ROWS:]
    if final:
        check(len(ledger_rows) == len(rows_expected), "One appended ledger row per closed segment")
        forecast_modes_seen = set()
        for i, (row, wanted) in enumerate(zip(ledger_rows, rows_expected)):
            segment = wanted["segment"]
            check(row["task_id"] == "F15-ND01" and row["attempt_id"] == "F15-ND01-A1"
                  and row["session_id"] == "2026-10-05-S1", f"Ledger {i}: task identity")
            check(row["start_utc"] == segment["start_utc"] and row["end_utc"] == segment["end_utc"],
                  f"Ledger {i}: observed boundaries")
            for field, name in (("elapsed_seconds", "elapsed"), ("engaged_seconds", "engaged"),
                                ("tool_wait_seconds", "wait"), ("unmeasured_seconds", "recovery")):
                check(Decimal(row[field]) * NS == wanted[name], f"Ledger {i}: exact {field}")
            check(Decimal(row["idle_seconds"]) == 0, f"Ledger {i}: no invented idle estimate")
            expected_mode = wanted["mode"] if wanted["mode"] in (*RESEARCH, "O") else (
                "E" if wanted["mode"] == "wait" else "O")
            check(row["mode"] == expected_mode and row["lane"] == wanted["lane"], f"Ledger {i}: effective mode/lane")
            check((REPO / row["artifact"]).is_file(), f"Ledger {i}: evidence path exists")
            forecast_mode = wanted["mode"]
            forecast_amount = str(central[forecast_mode]*60) if forecast_mode in (*RESEARCH, "O") and forecast_mode not in forecast_modes_seen else ""
            check(row["forecast_seconds"] == forecast_amount, f"Ledger {i}: central mode forecast recorded once")
            if forecast_mode in (*RESEARCH, "O"):
                forecast_modes_seen.add(forecast_mode)
    elif appended:
        warnings.append("Ledger already contains new rows; use --final after explicit clock close to audit them.")

    minute_totals = {k: Decimal(v)/MNS for k, v in totals.items()}
    close_minutes = ENTRY + Decimal(engaged)/MNS
    if final:
        actuals = document("actuals.json")
        check(actuals["exact_nanoseconds"] == totals, "Final mode nanoseconds independently reproduced")
        check(actuals["lane_exact_nanoseconds"] == lanes, "Final lane nanoseconds independently reproduced")
        check(actuals["research_nanoseconds"] == research and actuals["engaged_nanoseconds"] == engaged
              and actuals["observed_wall_nanoseconds"] == wall, "Final research/engaged/wall exact nanoseconds")
        check(actuals["parallel_agent_minutes_added"] == 0, "Final adds zero parallel-agent minutes")
        check(actuals["protected_floor"]["mode"] == "D+L+E" and actuals["protected_floor"]["minutes"] == 90
              and actuals["protected_floor"]["observed_nanoseconds"] == research
              and actuals["protected_floor"]["required_nanoseconds"] == 90 * MNS
              and actuals["protected_floor"]["satisfied"] is True, "Final protected floor is fresh Research90")
        for mode, expected_minutes in minute_totals.items():
            approximately(actuals["minutes"][mode], expected_minutes, f"Final {mode} minutes")
        for field, ns in (("research_minutes", research), ("engaged_minutes", engaged), ("observed_wall_minutes", wall)):
            approximately(actuals[field], Decimal(ns)/MNS, f"Final {field}")
        for lane, ns in lanes.items():
            approximately(actuals["lane_minutes"][lane], Decimal(ns)/MNS, f"Final {lane} lane minutes")
            percent = Decimal(ns)*100/research
            approximately(actuals["lane_percent_of_research"][lane], percent, f"Final {lane} research share")
            approximately(actuals["lane_forecast_error_percentage_points"][lane], percent-forecast["lane_percent"][lane],
                          f"Final {lane} lane forecast error")
        for label, planned in (("central", central), ("high", high)):
            for mode, amount in planned.items():
                observed = minute_totals.get(mode, Decimal(research if mode == "research" else engaged)/MNS)
                approximately(actuals[f"{label}_forecast_error_minutes"][mode], observed-amount,
                              f"Final {label} {mode} forecast error")
        post = actuals["post_b_1"]
        approximately(post["entry_minutes"], ENTRY, "Final POST entry unchanged")
        approximately(post["close_minutes"], close_minutes, "Final POST cumulative sum")
        approximately(post["remaining_minutes"], max(Decimal(0), CHECKPOINT-close_minutes), "Final checkpoint remainder")
        check(Decimal(post["close_minutes_decimal"]) == close_minutes, "Full-precision Decimal cumulative sum")
        check(Decimal(post["remaining_minutes_decimal"]) == max(Decimal(0), CHECKPOINT-close_minutes),
              "Full-precision Decimal checkpoint remainder")
        check(post["recurrence_clock_reset"] is False and post["next_checkpoint_minutes"] == 960,
              "Final cumulative clock was not reset")
        check(actuals["accounting_cutoff_monotonic_ns"] == segments[-1]["end_monotonic_ns"]
              and actuals["accounting_cutoff_utc"] == segments[-1]["end_utc"], "Final cutoff binds observed stop")
        check(bool(actuals.get("uncredited_administrative_tail")), "Unquantified post-cutoff administration disclosed")
        for name, metadata in actuals["raw_inputs"].items():
            source = (REPO / metadata["path"]).read_bytes()
            check(sha(source) == metadata["sha256"] and len(source) == metadata["bytes"], f"Final raw source hash: {name}")
        integrity = document("ledger_integrity.json")
        for key, expected_value in (("baseline_bytes", BASE_BYTES), ("baseline_sha256", BASE_SHA),
                                    ("old_ledger_rows", BASE_ROWS), ("appended_rows", len(segments)),
                                    ("appended_bytes", len(appended)), ("appended_sha256", sha(appended)),
                                    ("observed_new_bytes", len(ledger)), ("observed_new_sha256", sha(ledger))):
            check(integrity[key] == expected_value, f"Final ledger integrity: {key}")
        check(integrity["effective_research_nanoseconds"] == research and integrity["protected_Research90_verified"] is True,
              "Integrity record binds exact Research90 duration")
        check(integrity["parallel_agent_minutes_added"] == 0 and integrity["administration_after_cutoff_credited"] is False,
              "Integrity excludes agents and administrative tail")
        intent = document("finalization_intent.json")
        check(intent["actuals"] == actuals, "Durable intent carries identical actuals")
        check(intent["append_csv_utf8"].encode() == appended, "Durable intent matches exact appended bytes")
        for name in ("actuals.json", "ledger_integrity.json", "finalization_intent.json"):
            sidecar = SESSION / (name + ".sha256")
            check(sidecar.is_file() and sidecar.read_text().split()[0] == sha(raw[name]), f"Final SHA sidecar: {name}")

    for name, data in raw.items():
        current = (SESSION / name).read_bytes() if (SESSION / name).exists() else None
        check(current == data, f"Stable read snapshot: {name}")
    check((REPO / "v2/time_ledger.csv").read_bytes() == ledger, "Stable read snapshot: ledger")
    return {
        "schema": "F15-ND01-independent-accounting-audit-v1",
        "auditor": "delegated ChatGPT (GPT-6 Astra Pro), protocol/accounting audit",
        "audited_utc": datetime.now(timezone.utc).isoformat(),
        "status": ("PASS" if not errors else "FAIL") if final else ("PROVISIONAL" if not errors else "FAIL"),
        "final_requested": final, "clock_closed": closed, "check_count": len(checks),
        "errors": errors, "warnings": warnings,
        "principal_segments": len(segments), "historical_rows": BASE_ROWS,
        "ledger_prefix_sha256": sha(ledger[:BASE_BYTES]),
        "ledger_rows_added": len(ledger_rows), "ledger_sha256": sha(ledger),
        "exact_nanoseconds": totals, "lane_nanoseconds": lanes,
        "minutes_decimal": {k: str(v) for k, v in minute_totals.items()},
        "research_nanoseconds": research, "required_research_nanoseconds": 90*MNS,
        "research_floor_satisfied_in_closed_segments": research >= 90*MNS,
        "research_minutes_decimal": str(Decimal(research)/MNS),
        "engaged_minutes_decimal": str(Decimal(engaged)/MNS),
        "post_b_1_entry_minutes_decimal": str(ENTRY),
        "post_b_1_close_minutes_decimal": str(close_minutes),
        "remaining_to_960_minutes_decimal": str(max(Decimal(0), CHECKPOINT-close_minutes)),
        "normalizations": normalizations, "active_gap_reviews": gap_reviews,
        "auditor_minutes_added": 0,
        "limitations": "Arithmetic and recorded continuity audited; raw timestamps alone cannot prove substantive engagement. Open segments receive no provisional credit; task completion and scientific support are separate.",
        "inputs": {name: {"sha256": sha(data), "bytes": len(data)} for name, data in raw.items() if data is not None},
        "audit_script_sha256": sha(Path(__file__).read_bytes()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    result = audit(args.final)
    if args.save:
        phase = "final" if args.final else "preclose"
        output = SESSION / f"audit_accounting_{phase}.json"
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        output.with_suffix(".md").write_text(
            f"# F15-ND01 independent accounting audit ({phase})\n\n"
            f"Status: **{result['status']}**. {result['check_count']} arithmetic, continuity and integrity checks; "
            f"{len(result['errors'])} failures. Clock closed: {result['clock_closed']}.\n\n"
            f"Research in closed segments: {result['research_minutes_decimal']} minutes; "
            f"engaged: {result['engaged_minutes_decimal']} minutes. "
            f"Protected Research90 satisfied: {result['research_floor_satisfied_in_closed_segments']}.\n\n"
            f"The historical 949-row /217,776-byte ledger prefix has SHA256 `{result['ledger_prefix_sha256']}`. "
            f"New rows observed: {result['ledger_rows_added']}. Parallel/auditor minutes added: zero.\n\n"
            f"POST-B-1 entry: {result['post_b_1_entry_minutes_decimal']}; "
            f"observed closed-segment cumulative total: {result['post_b_1_close_minutes_decimal']}; "
            f"remaining to 960: {result['remaining_to_960_minutes_decimal']}.\n\n"
            f"{result['limitations']}\n\n"
            f"Machine-readable evidence: [{output.name}]({output.name}). "
            "Contributor: delegated ChatGPT (GPT-6 Astra Pro), protocol/accounting audit.\n")
    print(json.dumps({k: result[k] for k in ("status", "clock_closed", "check_count", "errors", "principal_segments",
                     "research_minutes_decimal", "engaged_minutes_decimal", "ledger_rows_added")}, indent=2))
    if result["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
