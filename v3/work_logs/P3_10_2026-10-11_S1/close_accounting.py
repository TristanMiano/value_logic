"""Close P3-10 observed accounting and append, never rewrite, prior ledger bytes.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11. Administrative observer.
Only the stopped principal clock is imported. No scientific method is run.
"""
from decimal import Decimal, getcontext
from pathlib import Path
import csv
import hashlib
import importlib.util
import io
import json
import subprocess

getcontext().prec = 48
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = "ea3e20dd9889c2ee22141c17390595867d33d8ab"
MODES = ("D", "L", "E", "O", "wait", "idle", "unmeasured", "recovery")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def minutes(ns):
    return format(Decimal(ns) / Decimal(60_000_000_000), ".12f")


def seconds(ns):
    return format(Decimal(ns) / Decimal(1_000_000_000), ".9f")


def save_new(name, data):
    with (HERE / name).open("x") as stream:
        json.dump(data, stream, indent=2, sort_keys=True)
        stream.write("\n")


def main():
    assert json.loads((HERE / "clock_state.json").read_text()) is None
    assert not (HERE / "effective_segments.json").exists()
    current_actuals = (HERE / "actuals.json").read_bytes()
    assert json.loads(current_actuals)["status"] == "in_progress"
    spec = importlib.util.spec_from_file_location("p310_accounting_clock", HERE / "clock.py")
    clock = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(clock)
    segments = clock.effective_segments()
    events = clock.read_records(HERE / "clocks.jsonl")
    dispositions = clock.read_records(HERE / "clock_dispositions.jsonl")
    assert events[-1]["command"] == "stop"
    assert all(a["end_monotonic_ns"] == b["start_monotonic_ns"]
               for a, b in zip(segments, segments[1:]))
    totals = dict.fromkeys(MODES, 0)
    lanes = dict.fromkeys(("R", "X"), 0)
    gaps, violations = [], []
    for part in segments:
        totals[part["mode"]] += part["elapsed_ns"]
        if part["mode"] in ("D", "L", "E"):
            lanes[part["lane"]] += part["elapsed_ns"]
        else:
            assert part["lane"] == ""
        if part["mode"] in ("D", "L", "E", "O"):
            points = sorted({part["start_monotonic_ns"], part["end_monotonic_ns"]} | {
                e["monotonic_ns"] for e in events
                if e["runtime"] == part["runtime"]
                and part["start_monotonic_ns"] <= e["monotonic_ns"] <= part["end_monotonic_ns"]})
            for left, right in zip(points, points[1:]):
                gaps.append(right - left)
                if right - left > 900_000_000_000:
                    violations.append({"raw_segment_index": part["raw_segment_index"], "gap_ns": right-left})
    assert not violations, violations
    research = sum(totals[k] for k in ("D", "L", "E"))
    engaged = research + totals["O"]
    assert research == sum(lanes.values()) == 5_417_014_164_347
    assert research >= 5_400_000_000_000
    prior = json.loads((ROOT / "v3/work_logs/P3_09_2026-10-11_S1/actuals.json").read_text())
    assert prior["phase_research_ns"] == 59_750_867_877_502
    assert prior["phase_measured_engaged_ns"] == 66_505_421_555_229
    two_lanes = {k: lanes[k] + prior["lane_research_ns"][k] for k in lanes}
    two_total = sum(two_lanes.values())
    assert all(4 * v >= two_total for v in two_lanes.values())
    ledger = ROOT / "v3/time_ledger.csv"
    original = subprocess.check_output(["git", "show", BASE + ":v3/time_ledger.csv"], cwd=ROOT)
    assert ledger.read_bytes() == original, "Unexpected prior edit or duplicate append."
    assert len(original) == 200471 and original.endswith(b"\n")
    assert sha(original) == "6326ca24bbbc2958f176ae9c542a26a46aaae508a2ab711bcd0c8363a2a545b5"
    original_rows = list(csv.DictReader(io.StringIO(original.decode())))
    assert len(original_rows) == 484
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    for part in segments:
        elapsed = part["elapsed_ns"]
        status = "Closed observed P3-10 principal interval; " + part["note"]
        if "disposition_id" in part:
            status += "; disposition=" + part["disposition_id"]
        writer.writerow([
            "P3-10", "P3-10-1", "2026-10-11-S1", part["mode"], part["lane"],
            part["start_utc"], part["end_utc"], seconds(elapsed),
            seconds(elapsed if part["mode"] in ("D", "L", "E", "O") else 0),
            seconds(elapsed if part["mode"] == "wait" else 0),
            seconds(elapsed if part["mode"] == "idle" else 0),
            seconds(elapsed if part["mode"] in ("unmeasured", "recovery") else 0),
            0, "v3/work_logs/P3_10_2026-10-11_S1.md", status])
    appended = output.getvalue().encode()
    forecast = json.loads((HERE / "forecast.json").read_text())
    phase_research = prior["phase_research_ns"] + research
    phase_engaged = prior["phase_measured_engaged_ns"] + engaged
    actuals = {
        "schema": "value_logic.p310.actuals.v1", "task": "P3-10", "attempt": "P3-10-1",
        "session": "2026-10-11-S1", "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "base_commit": BASE, "clock_stopped": True, "runtime": clock.RUNTIME,
        "status": "COMPLETE at explicit amended frozen-execution and interpretation scope; original failure preserved; P3-11 unstarted; author gates unattempted.",
        "recorded_start_utc": events[0]["utc"], "recorded_end_utc": events[-1]["utc"],
        "recorded_start_monotonic_ns": events[0]["monotonic_ns"],
        "recorded_end_monotonic_ns": events[-1]["monotonic_ns"],
        "research_closed_utc": "2026-10-11T16:51:05.035415+00:00",
        "research_closed_monotonic_ns": 10556002853751,
        "research_ns": research, "research_minutes": minutes(research),
        "task_research_ns": research, "task_research_minutes": minutes(research),
        "protected_research_floor_minutes": 90, "research_floor_ns": 5_400_000_000_000,
        "research_floor_satisfied": True, "task_floor_margin_ns": research-5_400_000_000_000,
        "task_remaining_floor_ns": 0, "remaining_research_floor_ns": 0,
        "prior_verified_task_research_ns": 0, "historical_recredit_ns": 0,
        "parallel_reviewer_credit_ns": 0, "agent_overlap_added_ns": 0,
        "total_engaged_ns": engaged, "total_engaged_minutes": minutes(engaged),
        "category_ns": totals, "category_minutes": {k: minutes(v) for k,v in totals.items()},
        "lane_research_ns": lanes, "lane_research_minutes": {k: minutes(v) for k,v in lanes.items()},
        "lane_percent": {k: str(Decimal(100)*v/research) for k,v in lanes.items()},
        "two_cycle_lane_ns": two_lanes, "two_cycle_research_ns": two_total,
        "two_cycle_lane_percent": {k: str(Decimal(100)*v/two_total) for k,v in two_lanes.items()},
        "two_cycle_lane_floor_satisfied": True, "lane_repair_emergency": False,
        "prior_phase_research_ns": prior["phase_research_ns"],
        "prior_phase_measured_engaged_ns": prior["phase_measured_engaged_ns"],
        "phase_research_ns": phase_research, "phase_research_minutes": minutes(phase_research),
        "phase_measured_engaged_ns": phase_engaged,
        "phase_remaining_floor_ns": 0, "phase_remaining_floor_minutes": minutes(0),
        "phase_research_floor_satisfied": True, "phase_floor_overshoot_ns": phase_research-57_600_000_000_000,
        "new_phase_checkpoint_crossed": False, "next_phase_checkpoint_minutes": None,
        "checkpoint_record": "v3/work_logs/P3_09_2026-10-11_S1/checkpoint_960.md",
        "maximum_observed_active_gap_ns": max(gaps), "cadence_violations": violations,
        "forecast_central_minutes": forecast["central_minutes"],
        "forecast_high_minutes": forecast["high_minutes"],
        "forecast_error_minutes": {k: str(Decimal(totals[k])/Decimal(60_000_000_000)-v)
                                   for k,v in forecast["central_minutes"].items()},
        "forecast_error_scope": "Closed observed intervals only. The subsequent administrative completion/publication tail is unmeasured and earns zero further engaged or research credit.",
        "forecast_seconds_ledger_policy": "Zero per-segment forecast allocation; prospective task/mode forecasts remain in forecast.json and this actuals record, without repeated per-row forecast credit.",
        "additional_recurrence_selected": False,
        "clock_dispositions": {"count": len(dispositions), "file": "clock_dispositions.jsonl",
                               "rule": "Eight additive dispositions conservatively exclude recovery, unmeasured work and administratively mixed intervals. Raw observations are immutable."},
        "ledger": {"base_bytes": len(original), "base_rows": len(original_rows), "base_sha256": sha(original),
                   "append_bytes": len(appended), "append_rows": len(segments), "append_sha256": sha(appended),
                   "result_sha256": sha(original+appended), "prior_bytes_preserved": True},
        "ledger_append_pending": False,
        "clock_source_sha256": sha((HERE / "clock.py").read_bytes()),
        "clock_events_sha256": sha((HERE / "clocks.jsonl").read_bytes()),
        "clock_segments_sha256": sha((HERE / "segments.jsonl").read_bytes()),
        "clock_dispositions_sha256": sha((HERE / "clock_dispositions.jsonl").read_bytes()),
        "accounting_source_sha256": sha(Path(__file__).read_bytes()),
        "phase_two_ledger_sha256": sha((ROOT / "v2/time_ledger.csv").read_bytes()),
        "publication_tail": "After the observed stop, completion-file integration, preservation verification, publication and response are administrative and unmeasured, with zero additional engaged or research credit.",
        "experimental_freeze_created": True, "final_evaluation_exposed": True,
        "amended_completion": True, "original_confirmatory_full_500_run_complete": False,
        "original_failed_prefix_exact_cost": "unknown", "global_positive_end_to_end_economic_gate": False,
        "completed_public_unit_count": 500, "original_reused_public_units": 440,
        "amended_inherited_conformance_units": 60, "private_evaluation_units": 500,
        "freeze_manifest_sha256": sha((ROOT / "v3/experiments/frozen_v1/manifest.json").read_bytes()),
        "freeze_protocol_sha256": sha((ROOT / "v3/experiments/protocol.v1.json").read_bytes())}
    save_new("effective_segments.json", segments)
    save_new("actuals_preclose.json", json.loads(current_actuals))
    with (HERE / "ledger_append.csv").open("xb") as stream:
        stream.write(appended)
    save_new("accounting_prepared.json", {"actuals": actuals, "ledger_append_sha256": sha(appended)})
    with ledger.open("ab") as stream:
        stream.write(appended)
    assert ledger.read_bytes() == original + appended
    (HERE / "actuals.json").write_text(json.dumps(actuals, indent=2, sort_keys=True) + "\n")
    save_new("accounting_completion.json", {"status": "PASS", "actuals_sha256": sha((HERE/"actuals.json").read_bytes()),
                                           "ledger_sha256": sha(ledger.read_bytes()), "research_ns": research})
    print(json.dumps({k: actuals[k] for k in ("research_ns", "research_minutes", "total_engaged_ns",
        "total_engaged_minutes", "phase_research_ns", "phase_research_minutes", "phase_measured_engaged_ns",
        "maximum_observed_active_gap_ns", "two_cycle_lane_percent", "category_minutes", "ledger")}))


if __name__ == "__main__":
    main()
