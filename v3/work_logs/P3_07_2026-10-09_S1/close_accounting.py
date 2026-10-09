"""Close observed P3-07 accounting once; never reconstruct missing time.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09. Operational work only.
Run on the original clock runtime after clock.py stop. The saved JSON/CSV are
portable evidence; this one-shot writer refuses an already-posted ledger.
"""
from collections import Counter
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import csv
import hashlib
import io
import json
import subprocess

from clock import effective_segments, read_records

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASE = "c7386f115bf60a9eb3a419515c844b81fc6ba073"
REL = "v3/work_logs/P3_07_2026-10-09_S1"
PRIOR_RESEARCH = 33_718_345_176_387
PRIOR_ENGAGED = 39_021_742_019_116
FLOOR = 960 * 60_000_000_000


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decimal_ns(ns, divisor=60_000_000_000, places=12):
    return f"{Decimal(ns) / Decimal(divisor):.{places}f}"


def write_json(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")


def main():
    assert json.loads((HERE / "clock_state.json").read_text()) is None, "Stop the clock first."
    ledger = REPO / "v3/time_ledger.csv"
    base = subprocess.check_output(["git", "show", f"{BASE}:v3/time_ledger.csv"], cwd=REPO)
    assert sha(base) == "6bcac52c02ed1a154646422352e2bdd3b66d734a808e118cac5b697c85503bf4"
    assert ledger.read_bytes() == base, "Ledger already appended or advanced; inspect instead of overwriting."
    old_rows = list(csv.DictReader(io.StringIO(base.decode())))
    assert not any(row["task_id"] == "P3-07" for row in old_rows)
    old_research = sum(Decimal(row["engaged_seconds"]) for row in old_rows if row["mode"] in ("D", "L", "E"))
    old_engaged = sum(Decimal(row["engaged_seconds"]) for row in old_rows)
    assert int(old_research * 1_000_000_000) == PRIOR_RESEARCH
    assert int(old_engaged * 1_000_000_000) == PRIOR_ENGAGED
    phase_two_hash = sha((REPO / "v2/time_ledger.csv").read_bytes())
    assert phase_two_hash == "5c71a4727f1cb7e03565f1c495b0c63b351863583120f0ec5684aca48bd122c6"
    segments = effective_segments()
    events = read_records(HERE / "clocks.jsonl")
    totals = Counter()
    lanes = Counter()
    cadence = []
    for previous, following in zip(segments, segments[1:]):
        assert previous["end_monotonic_ns"] == following["start_monotonic_ns"]
        assert previous["runtime"] == following["runtime"]
    for segment in segments:
        totals[segment["mode"]] += segment["elapsed_ns"]
        if segment["mode"] in ("D", "L", "E"):
            lanes[segment["lane"]] += segment["elapsed_ns"]
        if segment["mode"] in ("D", "L", "E", "O"):
            points = sorted({segment["start_monotonic_ns"], segment["end_monotonic_ns"]} |
                            {e["monotonic_ns"] for e in events if segment["start_monotonic_ns"] <= e["monotonic_ns"] <= segment["end_monotonic_ns"]})
            for a, b in zip(points, points[1:]):
                if b - a > 900_000_000_000:
                    cadence.append({"start_ns": a, "end_ns": b, "gap_ns": b-a})
    assert not cadence, "Active observation cadence exceeded fifteen minutes."
    research = sum(totals[m] for m in ("D", "L", "E"))
    assert research == 5_411_261_238_724
    assert sum(lanes.values()) == research
    engaged = research + totals["O"]
    phase = PRIOR_RESEARCH + research
    fields = list(old_rows[0])
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    forecast = json.loads((HERE / "forecast.json").read_text())
    forecasted = set()
    for segment in segments:
        mode, ns = segment["mode"], segment["elapsed_ns"]
        credit = ns if mode in ("D", "L", "E", "O") else 0
        fc = forecast["central_minutes"].get(mode, 0) * 60 if mode not in forecasted else 0
        forecasted.add(mode)
        writer.writerow({
            "task_id": "P3-07", "attempt_id": "P3-07-1", "session_id": "2026-10-09-S1",
            "mode": mode, "lane": segment["lane"], "start_utc": segment["start_utc"], "end_utc": segment["end_utc"],
            "elapsed_seconds": decimal_ns(ns, 1_000_000_000, 9),
            "engaged_seconds": decimal_ns(credit, 1_000_000_000, 9),
            "tool_wait_seconds": decimal_ns(ns if mode == "wait" else 0, 1_000_000_000, 9),
            "idle_seconds": decimal_ns(ns if mode == "idle" else 0, 1_000_000_000, 9),
            "unmeasured_seconds": decimal_ns(ns if mode in ("unmeasured", "recovery") else 0, 1_000_000_000, 9),
            "forecast_seconds": str(fc), "artifact": REL + ".md",
            "status": "Closed observed P3-07 interval; completion and contribution assessed separately; " + segment["note"]})
    appended = output.getvalue().encode()
    identities = set()
    for row in old_rows + list(csv.DictReader(io.StringIO(base.decode().splitlines()[0]+"\n"+appended.decode()))):
        identity = tuple(row[k] for k in ("task_id", "attempt_id", "session_id", "start_utc", "end_utc"))
        assert identity not in identities
        identities.add(identity)
    actuals = {
        "schema": "value_logic.p307.actuals.v1", "base_commit": BASE,
        "task": "P3-07", "attempt": "P3-07-1", "session": "2026-10-09-S1",
        "clock_stopped": True, "recorded_end_utc": events[-1]["utc"],
        "research_ns": research, "research_minutes": decimal_ns(research),
        "prior_verified_task_research_ns": 0, "historical_recredit_ns": 0,
        "prior_attempt_research": "NO_PRIOR_P3_07_CLOCKS_OR_ATTEMPT_FOUND_AT_ENTRY",
        "task_research_ns": research, "task_research_minutes": decimal_ns(research),
        "research_floor_satisfied": research >= 90*60_000_000_000,
        "task_floor_margin_ns": research-90*60_000_000_000,
        "task_remaining_floor_ns": max(0, 90*60_000_000_000-research),
        "total_engaged_ns": engaged, "total_engaged_minutes": decimal_ns(engaged),
        "category_ns": dict(totals), "category_minutes": {k: decimal_ns(v) for k,v in totals.items()},
        "lane_research_ns": dict(lanes), "lane_research_minutes": {k: decimal_ns(v) for k,v in lanes.items()},
        "lane_percent": {k: str(Decimal(v)*100/Decimal(research)) for k,v in lanes.items()},
        "prior_phase_research_ns": PRIOR_RESEARCH, "prior_phase_measured_engaged_ns": PRIOR_ENGAGED,
        "phase_research_ns": phase, "phase_research_minutes": decimal_ns(phase),
        "phase_measured_engaged_ns": PRIOR_ENGAGED+engaged,
        "phase_remaining_floor_ns": FLOOR-phase, "phase_remaining_floor_minutes": decimal_ns(FLOOR-phase),
        "next_phase_checkpoint_minutes": 960,
        "new_phase_checkpoint_crossed": False,
        "cadence_violations": cadence, "parallel_reviewer_credit_ns": 0,
        "segments": segments,
        "forecast_error_minutes": {k: str(Decimal(totals[k])/Decimal(60_000_000_000)-Decimal(v)) for k,v in forecast["central_minutes"].items()},
        "publication_tail": "After this observed stop, final packaging, transfer, remote verification and response work are conservatively unmeasured, with zero additional engaged or research credit. No duration is inferred.",
        "ledger": {"base_sha256": sha(base), "base_bytes": len(base), "append_sha256": sha(appended), "append_bytes": len(appended), "append_rows": len(segments), "result_sha256": sha(base+appended)},
        "phase_two_ledger_sha256": phase_two_hash,
    }
    write_json("accounting_base.json", {"base_commit": BASE, "v3_ledger_sha256": sha(base), "v3_ledger_bytes": len(base), "prior_phase_research_ns": PRIOR_RESEARCH, "prior_phase_engaged_ns": PRIOR_ENGAGED, "v2_ledger_sha256": phase_two_hash})
    write_json("actuals.json", actuals)
    (HERE / "effective_segments.jsonl").write_text("".join(json.dumps(s)+"\n" for s in segments))
    (HERE / "ledger_append.csv").write_bytes(appended)
    ledger.write_bytes(base+appended)
    assert ledger.read_bytes()[:len(base)] == base
    plan_path = REPO / "v3/plan.v1.json"
    plan = json.loads(plan_path.read_text())
    chunk = next(c for c in plan["chunks"] if c["id"] == "P3-07")
    chunk.update(status="complete", actuals=REL+"/actuals.json", research_ns=research,
                 research_floor_satisfied=True, remaining_research_floor_ns=0,
                 closure_status="complete_at_declared_finite_scope",
                 completion_scope="bounded_paid_computation_with_acquired_profiles_and_versioned_self_assessment",
                 readiness_audit=REL+"/readiness_audit.md", sessions=[REL+".md"],
                 companion_artifacts=["v3/derivations/07_"+name+".md" for name in ("multi_action_forecasting", "ordinary_analytic_profile", "acquisition_planning")],
                 implementation="v3/checks/07_paid_reasoning.py", implementation_version="p307-paid-reasoning-v3",
                 contribution_assessment=REL+"/contribution_assessment.md",
                 duty_assessment=REL+"/duty_assessment.md")
    plan.update(next_task="P3-B", active_session=None, last_completed_session=REL+".md", last_preserved_session=REL+".md")
    plan["observed_progress"] = {"research_ns": phase, "measured_engaged_ns": PRIOR_ENGAGED+engaged,
        "remaining_floor_ns": FLOOR-phase, "source": REL+"/actuals.json", "next_checkpoint_minutes": 960,
        "evidence_disposition": "P3-07 finite paid-reasoning scope complete; prior P3-01–06 evidence and ledgers preserved; no historical or parallel-agent credit; P3-N01 not yet supported; P3-B and P3-08 unattempted."}
    assert [c["minutes"] for c in plan["completed_research_checkpoints"]] == [240, 480]
    assert plan["gates"]["P3-B"]["status"] == "unattempted"
    assert next(c for c in plan["chunks"] if c["id"] == "P3-08")["status"] == "unstarted"
    plan_path.write_text(json.dumps(plan, indent=2)+"\n")
    print(json.dumps({k:actuals[k] for k in ("research_minutes", "total_engaged_minutes", "phase_research_minutes", "phase_remaining_floor_minutes", "category_minutes", "ledger")}, indent=2))


if __name__ == "__main__":
    main()
