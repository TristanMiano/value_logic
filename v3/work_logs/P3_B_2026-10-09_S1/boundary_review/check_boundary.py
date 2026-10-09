"""Independent final P3-B binding/status/accounting audit; no scientific runs.

Contributor: ChatGPT (GPT-6 Astra Pro), same-model nonblind boundary reviewer.
Only this new sibling audit directory is writable. All principal time credit
is zero. Raw transitions are reconstructed without importing the clock writer.
"""
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
SESSION = OUT.parent
ROOT = SESSION.parents[2]
BASE = "c7e2967d18475bda54a327864601c245c8a29062"
PREFIX_SIZE = 148588
PREFIX_SHA = "b01210421436289bed04c123b151f89ee97a77a1624c4a2e5f2a2ae936aeda40"
GATE_SHA = "f4441edea890377efb958a72bb5089c57ecbbe419ff63d8375e1d59a7c510652"
ALLOWED = {"TODO_v3.md", "v3/README.md", "v3/claim_ledger.md", "v3/plan.v1.json", "v3/time_ledger.csv"}
INPUTS = {}
CHECKS = []


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def raw(path):
    path = ROOT / path
    value = path.read_bytes()
    INPUTS[str(path.relative_to(ROOT))] = {"sha256": sha(value), "bytes": len(value)}
    return value


def js(path):
    return json.loads(raw(path))


def records(path):
    return [json.loads(line) for line in raw(path).decode().splitlines() if line]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def check(name, condition, **evidence):
    CHECKS.append({"check": name, "pass": bool(condition), **evidence})


def ns(value):
    exact = Decimal(value) * 1_000_000_000
    assert exact == exact.to_integral_value(), "Nonintegral nanosecond quantity"
    return int(exact)


def minutes(value):
    return f"{Decimal(value) / Decimal(60_000_000_000):.12f}"


def file_bindings(value, trail="contract"):
    if isinstance(value, dict):
        if {"path", "sha256"} <= set(value):
            content = raw(value["path"])
            check("bound_current_file", sha(content) == value["sha256"] and ("bytes" not in value or len(content) == value["bytes"]), field=trail, path=value["path"], expected_sha256=value["sha256"])
        for key, item in value.items():
            file_bindings(item, trail + "/" + str(key))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            file_bindings(item, trail + "/" + str(i))


def main():
    started = datetime.now(timezone.utc).isoformat()
    base_plan = json.loads(git("show", BASE + ":v3/plan.v1.json"))
    contract = js("v3/checkpoints/B_1.v1.json")
    gate = raw("v3/checkpoints/B_1.md").decode()
    plan = js("v3/plan.v1.json")
    actuals = js(SESSION / "actuals.json")
    decision = js(SESSION / "decision.json")
    recurrence = js(SESSION / "recurrence_options.json")
    forecast = js(SESSION / "forecast.json")
    accounting_base = js(SESSION / "accounting_base.json")
    file_bindings(contract)
    file_bindings(decision, "decision")
    resolution = js(SESSION / "reviews/semantics_agent/resolution.json")
    file_bindings({"final_reviewed_gate": resolution["final_reviewed_gate"], "earlier_observation": resolution["earlier_observation"]}, "semantic_resolution")
    check("accepted_exact_gate_hash", sha(gate.encode()) == GATE_SHA)
    check("source_commit_and_tree", contract["source_commit"] == BASE == decision["source_commit"] and contract["source_tree"] == git("rev-parse", BASE + "^{tree}").decode().strip() == decision["source_tree"])
    check("all_semantic_wording_resolutions_present", resolution["all_three_issues_resolved"] and all(i["status"] == "RESOLVED" and i["exact_reviewed_wording"] in gate for i in resolution["issues"]))

    # Reconstruct raw mode intervals from the observed transition records.
    clocks = records(SESSION / "clocks.jsonl")
    saved_raw = records(SESSION / "segments.jsonl")
    dispositions = records(SESSION / "clock_dispositions.jsonl")
    effective = records(SESSION / "effective_segments.jsonl")
    reconstructed = []
    active = None
    for event in clocks:
        if event["command"] == "check":
            continue
        if active is not None:
            reconstructed.append({**active, "end_utc": event["utc"],
                "end_monotonic_ns": event["monotonic_ns"],
                "elapsed_ns": event["monotonic_ns"] - active["start_monotonic_ns"]})
            check("same_runtime_transition", event["runtime"] == active["runtime"])
        if event["command"] == "stop":
            active = None
        else:
            args = event["args"]
            mode = args[0]
            lane = "" if event["command"] == "pause" or args[1] == "-" else args[1]
            note = args[-1]
            active = {"mode": mode, "lane": lane, "note": note,
                      "start_utc": event["utc"], "start_monotonic_ns": event["monotonic_ns"],
                      "runtime": event["runtime"]}
    check("raw_clock_transition_reconstruction", reconstructed == saved_raw and len(reconstructed) == 7, events=len(clocks), segments=len(reconstructed))
    check("observed_clock_closed", active is None and clocks[0]["command"] == "start" and clocks[-1]["command"] == "stop" and js(SESSION / "clock_state.json") is None and actuals["recorded_end_utc"] == clocks[-1]["utc"])
    reconstructed_effective = []
    used_dispositions = set()
    for index, interval in enumerate(reconstructed):
        item = {**interval, "raw_segment_index": index}
        for d in dispositions:
            if (d["runtime"], d["start_monotonic_ns"], d["end_monotonic_ns"]) == (item["runtime"], item["start_monotonic_ns"], item["end_monotonic_ns"]):
                check("exact_gap_disposition", d["original_mode"] == item["mode"] and d["start_utc"] == item["start_utc"] and d["end_utc"] == item["end_utc"] and d["mode"] == "unmeasured" and d["lane"] == "")
                check("disposition_applied_once", d["id"] not in used_dispositions)
                used_dispositions.add(d["id"])
                item.update(mode=d["mode"], lane=d["lane"], note=d["reason"], disposition_id=d["id"])
        reconstructed_effective.append(item)
    check("effective_segments_reconstructed", reconstructed_effective == effective == actuals["segments"] and len(used_dispositions) == len(dispositions) == 1)
    check("all_segments_contiguous", all(a["end_monotonic_ns"] == b["start_monotonic_ns"] and a["end_utc"] == b["start_utc"] for a, b in zip(effective, effective[1:])))

    category = Counter()
    lanes = Counter()
    cadence_gaps = []
    for row in effective:
        category[row["mode"]] += row["elapsed_ns"]
        if row["mode"] in ("D", "L", "E"):
            lanes[row["lane"]] += row["elapsed_ns"]
        if row["mode"] in ("D", "L", "E", "O"):
            ticks = sorted({row["start_monotonic_ns"], row["end_monotonic_ns"]} | {e["monotonic_ns"] for e in clocks if e["runtime"] == row["runtime"] and row["start_monotonic_ns"] <= e["monotonic_ns"] <= row["end_monotonic_ns"]})
            cadence_gaps += [b-a for a,b in zip(ticks,ticks[1:])]
    research = sum(category[m] for m in ("D", "L", "E"))
    engaged = research + category["O"]
    check("exact_category_and_lane_totals", dict(category) == actuals["category_ns"] and dict(lanes) == actuals["lane_research_ns"])
    check("exact_credit_totals", research == actuals["research_ns"] == actuals["task_research_ns"] == contract["research_ns"] == 732509997658 and engaged == actuals["total_engaged_ns"] == 933722811578)
    check("exclusions_are_not_research_or_engaged", sum(category.values()) == clocks[-1]["monotonic_ns"] - clocks[0]["monotonic_ns"] and sum(category.values()) - engaged == category["unmeasured"] + category["recovery"] == 171893466175)
    check("observed_cadence", max(cadence_gaps) <= 900_000_000_000 and actuals["cadence_violations"] == [], max_active_observation_gap_ns=max(cadence_gaps))
    check("no_historical_parallel_or_added_floor_credit", all(actuals[k] == 0 for k in ("prior_verified_task_research_ns", "historical_recredit_ns", "parallel_reviewer_credit_ns", "gate_research_floor_minutes")) and contract["parallel_reviewer_credit_ns"] == decision["parallel_reviewer_credit_ns"] == 0)
    for mode, amount in category.items():
        check("category_minutes", actuals["category_minutes"][mode] == minutes(amount), mode=mode)
    for lane, amount in lanes.items():
        check("lane_minutes_and_percentage", actuals["lane_research_minutes"][lane] == minutes(amount) and Decimal(actuals["lane_percent"][lane]) == Decimal(amount) * 100 / Decimal(research), lane=lane)
    for mode, expected in forecast["central_minutes"].items():
        check("forecast_error", Decimal(actuals["forecast_error_minutes"][mode]) == Decimal(category[mode]) / Decimal(60_000_000_000) - Decimal(expected), mode=mode)

    # Reconstruct exact nanoseconds from the CSV independently of its writer.
    base_ledger = git("show", BASE + ":v3/time_ledger.csv")
    ledger = raw("v3/time_ledger.csv")
    appended = raw(SESSION / "ledger_append.csv")
    check("exact_prior_prefix_and_only_append", len(base_ledger) == PREFIX_SIZE and sha(base_ledger) == PREFIX_SHA and ledger[:PREFIX_SIZE] == base_ledger and ledger[PREFIX_SIZE:] == appended)
    expected_receipt = {"base_sha256": sha(base_ledger), "base_bytes": len(base_ledger), "append_sha256": sha(appended), "append_bytes": len(appended), "append_rows": 7, "result_sha256": sha(ledger)}
    check("ledger_receipt", actuals["ledger"] == expected_receipt, reconstructed_receipt=expected_receipt)
    previous = list(csv.DictReader(io.StringIO(base_ledger.decode())))
    full = list(csv.DictReader(io.StringIO(ledger.decode())))
    new = full[len(previous):]
    check("exactly_seven_new_p3b_rows", len(new) == 7 and full[:len(previous)] == previous and not any(r["task_id"] == "P3-B" for r in previous) and all(r["task_id"] == "P3-B" and r["attempt_id"] == "P3-B-1" and r["session_id"] == "2026-10-09-S1" for r in new))
    forecasted = set()
    for index, (r, s) in enumerate(zip(new, effective)):
        credit = s["elapsed_ns"] if s["mode"] in ("D", "L", "E", "O") else 0
        excluded = s["elapsed_ns"] if s["mode"] in ("unmeasured", "recovery") else 0
        forecast_seconds = forecast["central_minutes"].get(s["mode"], 0) * 60 if s["mode"] not in forecasted else 0
        forecasted.add(s["mode"])
        check("ledger_row_matches_effective_interval", r["mode"] == s["mode"] and r["lane"] == s["lane"] and r["start_utc"] == s["start_utc"] and r["end_utc"] == s["end_utc"] and ns(r["elapsed_seconds"]) == s["elapsed_ns"] and ns(r["engaged_seconds"]) == credit and ns(r["unmeasured_seconds"]) == excluded and ns(r["idle_seconds"]) == ns(r["tool_wait_seconds"]) == 0 and int(r["forecast_seconds"]) == forecast_seconds and r["artifact"] == "v3/work_logs/P3_B_2026-10-09_S1.md" and r["status"].endswith(s["note"]), row=index)
    ids = [tuple(r[k] for k in ("task_id", "attempt_id", "session_id", "start_utc", "end_utc")) for r in full]
    check("unique_ledger_intervals", len(set(ids)) == len(ids))
    old_research = sum(ns(r["engaged_seconds"]) for r in previous if r["mode"] in ("D", "L", "E"))
    old_engaged = sum(ns(r["engaged_seconds"]) for r in previous)
    phase_research = old_research + research
    phase_engaged = old_engaged + engaged
    remaining = 960 * 60_000_000_000 - phase_research
    check("base_accounting_matches_prior_ledger", accounting_base == {"base_commit": BASE, "v3_ledger_sha256": PREFIX_SHA, "v3_ledger_bytes": PREFIX_SIZE, "prior_phase_research_ns": old_research, "prior_phase_engaged_ns": old_engaged, "v2_ledger_sha256": actuals["phase_two_ledger_sha256"]})
    check("phase_totals", phase_research == actuals["phase_research_ns"] == contract["phase_research_ns"] == plan["observed_progress"]["research_ns"] and phase_engaged == actuals["phase_measured_engaged_ns"] == plan["observed_progress"]["measured_engaged_ns"] and remaining == actuals["phase_remaining_floor_ns"] == plan["observed_progress"]["remaining_floor_ns"])
    check("rounded_reported_totals", actuals["research_minutes"] == minutes(research) and actuals["total_engaged_minutes"] == minutes(engaged) and actuals["phase_research_minutes"] == minutes(phase_research) and actuals["phase_remaining_floor_minutes"] == minutes(remaining))
    crossed = [m for m in (240, 480, 960) if old_research < m * 60_000_000_000 <= phase_research]
    check("phase_checkpoint_boundary", crossed == [] and not actuals["new_phase_checkpoint_crossed"] and plan["completed_research_checkpoints"] == base_plan["completed_research_checkpoints"] and actuals["next_phase_checkpoint_minutes"] == plan["observed_progress"]["next_checkpoint_minutes"] == 960)

    # Current state is separate from dated historical status paragraphs.
    check("p3a_unchanged", plan["gates"]["P3-A"] == base_plan["gates"]["P3-A"])
    check("p3b_pass_scope", plan["gates"]["P3-B"]["status"] == "passed" and plan["gates"]["P3-B"]["verdict"] == contract["verdict"] == decision["verdict"] == "PASS" and plan["gates"]["P3-B"]["research_ns"] == research and plan["gates"]["P3-B"]["scope"] == contract["scope"] == decision["scope"] == "restricted_mathematical_and_local_implementation_readiness")
    check("all_task_chunks_unchanged", plan["chunks"] == base_plan["chunks"])
    check("next_task_unstarted_no_active_session", plan["next_task"] == contract["next_task"] == decision["technical_next_task"] == "P3-08" and next(c for c in plan["chunks"] if c["id"] == "P3-08")["status"] == "unstarted" and not contract["next_task_started"] and not decision["next_task_started"] and plan["active_session"] is None)
    check("author_gates_unattempted_and_unchanged", all(plan["gates"][g] == base_plan["gates"][g] and plan["gates"][g]["status"] == "unattempted" for g in ("P3-C", "P3-D")))
    check("contribution_obligation_unchanged", plan["contribution_obligation"] == base_plan["contribution_obligation"] == contract["contribution_obligation"] == "P3-N01" and plan["contribution_status"] == base_plan["contribution_status"] == contract["contribution_status"] == decision["contribution_status"] == "NOT YET SUPPORTED")
    check("recurrence_recommended_not_selected", plan["optional_recurrence_advice"]["recommended"] == contract["optional_recurrence_recommended"] == decision["optional_recurrence_recommended"] == recurrence["recommended"] == "P3-B-OPTION-A" and plan["optional_recurrence_advice"]["selected"] is contract["optional_recurrence_selected"] is decision["optional_recurrence_selected"] is recurrence["selected"] is None and all(o["status"] == "unselected" and not o["started"] for o in recurrence["options"]) and not contract["named_contribution_recurrence_selected"] and not decision["named_contribution_recurrence_R_P3_N01_selected"])
    check("no_freeze_or_final_exposure", all(not d[k] for d in (plan, contract, decision) for k in ("experimental_freeze_created", "final_evaluation_exposed")))
    check("restricted_scope_and_no_end_to_end_claim", not contract["accepted_representation"]["end_to_end_reasoner_implemented"] and not decision["end_to_end_combined_reasoner_implemented"] and "has **not** yet been\nimplemented and validated" in gate and "No all-issued guarantee under\nselectively purchased feedback is accepted at this gate" in gate and "Seeded development traces do not verify the\nIID assumptions" in gate)
    check("six_predictions_and_twenty_one_duties", contract["implementable_predictions"] == [f"B-P0{i}" for i in range(1,7)] and all(f"| B-P0{i} |" in gate for i in range(1,7)) and len(contract["duties"]) == len({r["id"] for r in contract["duties"]}) == 21)
    todo = raw("TODO_v3.md").decode()
    readme = raw("v3/README.md").decode()
    claim = raw("v3/claim_ledger.md").decode()
    session_text = raw("v3/work_logs/P3_B_2026-10-09_S1.md").decode()
    check("todo_current_pointer", "- [x] **P3-B" in todo and "- [ ] **P3-08" in todo and "**Next: P3-08, unstarted.**" in todo and "All three remain unselected" in todo)
    check("current_document_totals", all(minutes(phase_research) in d and minutes(remaining) in d for d in (todo, readme, claim, session_text)))
    check("historical_status_distinction", "Historical completion sections above retain their original\ngate status" in readme and "earlier dated entries retain their historical task/gate pointers" in claim)

    current_v2 = raw("v2/time_ledger.csv")
    check("v2_ledger_exactly_unchanged", current_v2 == git("show", BASE + ":v2/time_ledger.csv") and sha(current_v2) == actuals["phase_two_ledger_sha256"])
    changed = git("diff", "--name-only", BASE, "--").decode().splitlines()
    check("all_prior_tracked_scientific_files_unchanged", set(changed) == ALLOWED, intentional_changed_controls=changed)
    untracked = git("ls-files", "--others", "--exclude-standard").decode().splitlines()
    unexpected = [p for p in untracked if p not in {"v3/checkpoints/B_1.md", "v3/checkpoints/B_1.v1.json", "v3/work_logs/P3_B_2026-10-09_S1.md"} and not p.startswith("v3/work_logs/P3_B_2026-10-09_S1/")]
    check("no_unstarted_task_artifacts", not unexpected, unexpected_untracked=unexpected)
    changed_inputs = [p for p, d in INPUTS.items() if sha((ROOT/p).read_bytes()) != d["sha256"]]
    check("all_frozen_inputs_unchanged_during_audit", not changed_inputs, changed=changed_inputs)
    failures = [c for c in CHECKS if not c["pass"]]
    result = {"schema": "value_logic.p3b.final_boundary_review.v1", "status": "PASS" if not failures else "BLOCKED",
              "scope": "Final local B_1 contract bindings, restricted scope, current controls, raw-clock/effective-segment accounting and protected prior bytes. No scientific reruns, no publication or remote-state assertion.",
              "contributor": "ChatGPT (GPT-6 Astra Pro), independent same-model nonblind boundary reviewer",
              "base_commit": BASE, "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
              "principal_research_credit_ns": 0, "checks": CHECKS, "failures": failures,
              "reconstructed_totals": {"research_ns": research, "engaged_ns": engaged, "excluded_ns": category["unmeasured"]+category["recovery"], "phase_research_ns": phase_research, "phase_engaged_ns": phase_engaged, "phase_remaining_floor_ns": remaining, "new_ledger_rows": len(new)},
              "input_sha256": INPUTS, "review_script_sha256": sha(Path(__file__).read_bytes()),
              "historical_source_manifest_policy": "Final JSON direct file bindings are checked against the actual frozen files. Earlier review input manifests retain base-version control hashes; authorized current TODO/README/claims/plan/ledger updates do not overwrite or invalidate those historical inputs."}
    with (OUT / "result.json").open("x") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"status": result["status"], "checks": len(CHECKS), "failures": failures, "totals": result["reconstructed_totals"], "input_files": len(INPUTS)}, indent=2))


if __name__ == "__main__":
    main()
