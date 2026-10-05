"""Inspect saved F15 artifacts only; never invoke an experimental generator.

Contributor: delegated ChatGPT (GPT-6 Astra Pro), execution audit.
The original zero-byte redundant aggregate is preserved. Its separately saved
exact reconstruction is verified against the original sidecar and case units.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
LOG = Path(__file__).resolve().parent
RUN = ROOT / "v2/work_logs/F15_v1_run1"
sys.path.insert(0, str(ROOT))
from v2.experiments import freeze as F


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=LOG / "artifact_integrity_audit.json")
    args = parser.parse_args()
    errors, checks = [], 0

    def check(condition, name, detail=None):
        nonlocal checks
        checks += 1
        if not condition:
            errors.append({"check": name, "detail": detail})

    config = F.validate_config(F.load_json(F.DEFAULT_CONFIG))
    freeze = F.verify_manifest()
    runtime = F.verify_environment(config)
    check(freeze["manifest_sha256"] == "b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c", "supplied_freeze_anchor")
    check(freeze["files"] == 34, "frozen_file_count")
    nc, rc = config["neural"], config["retention"]
    prep_names = [f"preparation_attempt_1/model_{i}_prepared.json" for i in range(5)]
    case_names = [f"evaluation_attempt_1/retention_{seed}_{variant}.json"
                  for seed in rc["evaluation_seeds"] for variant in rc["variants"]]
    eval_names = [f"evaluation_attempt_1/model_{i}_evaluation.json" for i in range(5)]
    expected_json = {f"{stage}_{kind}.json" for stage in ("preparation", "evaluation") for kind in ("start", "complete")}
    expected_json |= {f"{stage}_attempt_1/{kind}.json" for stage in ("preparation", "evaluation") for kind in ("start", "complete")}
    expected_json |= set(prep_names + case_names + eval_names)
    expected_json |= {"evaluation_attempt_1/retention_results.json", "evaluation_attempt_1/retention_assessment.json", "evaluation_attempt_1/neural_assessment.json"}
    observed_files = {p.relative_to(RUN).as_posix() for p in RUN.rglob("*") if p.is_file()}
    expected_files = expected_json | {name + ".sha256" for name in expected_json}
    check(observed_files == expected_files, "complete_run_file_inventory", {"missing": sorted(expected_files-observed_files), "unexpected": sorted(observed_files-expected_files)})
    inventory, mismatches = [], []
    for name in sorted(expected_json):
        path = RUN / name
        sidecar = Path(str(path) + ".sha256")
        actual, saved = digest(path), sidecar.read_text(encoding="ascii").strip()
        valid = actual == saved
        inventory.append({"path": name, "bytes": path.stat().st_size, "sha256": actual,
                          "sidecar_expected_sha256": saved, "sidecar_valid": valid,
                          "sidecar_file_sha256": digest(sidecar)})
        if not valid:
            mismatches.append(name)
    original_name = "evaluation_attempt_1/retention_results.json"
    original = RUN / original_name
    check(mismatches == [original_name], "only_preserved_aggregate_exception", mismatches)
    check(original.stat().st_size == 0, "original_empty_aggregate_preserved")
    original_expected = Path(str(original)+".sha256").read_text(encoding="ascii").strip()
    recovered = LOG / "retention_results_recovered.json"
    check(digest(recovered) == original_expected, "recovered_aggregate_original_digest")
    check(Path(str(recovered)+".sha256").read_text(encoding="ascii").strip() == original_expected, "recovered_aggregate_sidecar")

    stages = {name: F.load_json(RUN / f"{name}.json") for name in ("preparation_start", "preparation_complete", "evaluation_start", "evaluation_complete")}
    for stage in ("preparation", "evaluation"):
        for kind in ("start", "complete"):
            record = stages[f"{stage}_{kind}"]
            check(record == F.load_json(RUN / f"{stage}_attempt_1/{kind}.json"), f"{stage}_{kind}_root_copy")
            check(record["freeze"] == freeze, f"{stage}_{kind}_freeze")
            check(record["attempt"] == 1 and record["unchanged_unexplained_retry"] is False, f"{stage}_{kind}_attempt")
            check(not record["preserved_incomplete_artifacts"] and not record["reused_units"], f"{stage}_{kind}_no_recovery_units")
            check(record["environment"]["numpy"] == "2.3.5" and record["environment"]["python"].startswith("3.12."), f"{stage}_{kind}_runtime")
            check(all(v == "1" for v in record["environment"]["thread_environment"].values()), f"{stage}_{kind}_threads")
    pc, ec, es = stages["preparation_complete"], stages["evaluation_complete"], stages["evaluation_start"]
    check(pc["status"] == "all_models_prepared" and pc["evaluation_started"] is False, "preparation_complete_status")
    check(ec["status"] == "evaluation_complete", "evaluation_complete_status")
    check(pc["generated_units"] == prep_names, "preparation_unit_order")
    check(ec["generated_units"] == case_names + eval_names, "evaluation_unit_order")
    prep_hash = digest(RUN / "preparation_complete.json")
    check(es["preparation_manifest_sha256"] == ec["preparation_manifest_sha256"] == prep_hash, "exposure_binds_preparation")
    pre = F.load_json(LOG / "pre_evaluation_validation.json")
    check(pre["freeze"] == freeze and pre["preparation_manifest_sha256"] == prep_hash, "preexposure_freeze_and_manifest")
    check(pre["all_five_validated"] is True and pre["evaluation_marker_absent"] is True and pre["final_retention_or_neural_population_generated"] is False, "preexposure_flags")
    check(len(pc["models"]) == len(pre["models"]) == 5, "all_five_model_records")
    prepared, model_summary = [], []
    expected_alignments = {f"{g}/{control}" for g in nc["g_family"] for control in nc["controls"]}
    for i, seed in enumerate(nc["model_seeds"]):
        info, before = pc["models"][i], pre["models"][i]
        path = RUN / prep_names[i]
        p = F.load_json(path)
        F.validate_prepared(p, config, seed)
        prepared.append(p)
        check(info["file"] == prep_names[i] and info["index"] == i and info["discovery_seed"] == seed, f"model{i}_manifest_identity")
        check(info["sha256"] == before["sha256"] == digest(path), f"model{i}_preexposure_external_hash")
        check(info["alignment_artifact_hash"] == before["alignment_artifact_hash"] == p["artifact_hash"], f"model{i}_preexposure_internal_hash")
        check(before["file_bytes"] == path.stat().st_size, f"model{i}_preexposure_bytes")
        check(before["all_selected_subsets"] == {k: [r["subset"] for r in a["roles"]] for k, a in p["alignments"].items()}, f"model{i}_preexposure_subsets")
        check(before["all_selected_indices"] == {k: [r["selected_index"] for r in a["roles"]] for k, a in p["alignments"].items()}, f"model{i}_preexposure_indices")
        check(before["training"] == p["training"] and before["resource"] == p["resource"], f"model{i}_preexposure_budget_records")
        check(set(p["alignments"]) == expected_alignments, f"model{i}_all_alignments")
        for name, alignment in p["alignments"].items():
            for role_index, role in enumerate(alignment["roles"]):
                check(all(len(s) == len(set(s)) == nc["subset_size"] and all(type(j) is int and 0 <= j < nc["width"] for j in s) for s in role["candidate_pool"]), f"model{i}_{name}_role{role_index}_all_candidate_shapes")
        model_summary.append({"index": i, "discovery_seed": seed, "prepared_file_sha256": digest(path),
                              "discovery_artifact_hash": p["artifact_hash"], "alignment_count": len(p["alignments"]),
                              "training_outcomes": p["training"]["stochastic_outcome_labels"],
                              "expected_cost_training_labels": p["training"]["expected_cost_training_labels"],
                              "candidate_evaluations": p["resource"]["candidate_evaluations"], "decoder_fits": p["resource"]["decoder_fits"]})

    cases = F.load_json(recovered)
    check(len(cases) == 160, "retention_case_count")
    method_order = [(access, method) for access in rc["access_regimes"] for method in rc["methods"]]
    for i, name in enumerate(case_names):
        individual = F.load_json(RUN / name)
        check(cases[i] == individual, f"case{i}_aggregate_exact_case_equality")
        expected_seed = rc["evaluation_seeds"][i // len(rc["variants"])]
        expected_variant = rc["variants"][i % len(rc["variants"])]
        check((individual["seed"], individual["variant"]) == (expected_seed, expected_variant), f"case{i}_frozen_seed_variant")
        check([(m["access"], m["method"]) for m in individual["methods"]] == method_order, f"case{i}_method_panel_order")
        check(all(len(m["numeric"]) == 6 for m in individual["methods"]), f"case{i}_six_numeric_queries_per_method")
    check(hashlib.sha256(canonical(cases)).hexdigest() == original_expected, "recovered_aggregate_canonical_byte_identity")
    method_rows = sum(len(c["methods"]) for c in cases)
    numeric_queries = sum(len(m["numeric"]) for c in cases for m in c["methods"])
    check(method_rows == 1920 and numeric_queries == 11520, "retention_complete_row_counts")
    retention_assessment = F.load_json(RUN / "evaluation_attempt_1/retention_assessment.json")
    check(retention_assessment["case_count"] == 160 and retention_assessment["method_rows"] == 1920 and retention_assessment["development_only"] is False, "retention_assessment_scope_counts")

    neural = []
    n = nc["evaluation_pairs_per_stratum"]
    pair_total = wrong_total = role_eval_total = task_total = 0
    for i, seed in enumerate(nc["evaluation_seeds"]):
        value = F.load_json(RUN / eval_names[i])
        neural.append(value)
        check(value["evaluation_seed"] == seed and value["discovery_artifact_hash"] == prepared[i]["artifact_hash"], f"neural{i}_seed_prepared_binding")
        check(value["selected_alternative"] == prepared[i]["selected_alternative"], f"neural{i}_discovery_selected_rival")
        check(value["pairs_per_stratum"] == n and value["task"]["n"] == nc["task_evaluation_samples"], f"neural{i}_sample_budgets")
        check(set(value["alignments"]) == expected_alignments, f"neural{i}_all_controls_hypotheses")
        for name, a in value["alignments"].items():
            check(len(a["roles"]) == 2, f"neural{i}_{name}_roles")
            for ri, role in enumerate(a["roles"]):
                check(set(role) == set(nc["strata"]) and all(role[s]["n"] == n for s in nc["strata"]), f"neural{i}_{name}_role{ri}_strata_counts")
                for s in nc["strata"]:
                    check(all(role[s][metric]["n"] == n for metric in ("base_prediction", "no_swap", "whole_layer_swap")), f"neural{i}_{name}_role{ri}_{s}_baseline_counts")
        for key in ("pair_generation", "wrong_donor_generation"):
            check(len(value[key]) == 2, f"neural{i}_{key}_roles")
            for ri, role in enumerate(value[key]):
                check(set(role) == set(nc["strata"]), f"neural{i}_{key}_role{ri}_strata")
                check(all(v["accepted"] == n and n <= v["proposals_generated"] <= nc["pair_attempt_multiplier"] * n for v in role.values()), f"neural{i}_{key}_role{ri}_budgets")
        check(value["resource"]["alignment_refits"] == 0, f"neural{i}_zero_refits")
        check(value["resource"]["pair_examples"] == 2 * len(nc["strata"]) * n, f"neural{i}_pair_resource_count")
        check(value["resource"]["alignment_role_pair_evaluations"] == len(expected_alignments) * 2 * len(nc["strata"]) * n, f"neural{i}_alignment_resource_count")
        for g in nc["g_family"][1:]:
            for ri in (0, 1):
                contrast = value["alternative_comparisons"][g][f"{ri}/scale_separating"]
                check(contrast["total_pairs"] == contrast["separating_pairs"] == contrast["same_identity_subset_comparison"]["n"] == n, f"neural{i}_{g}_role{ri}_unselected_scale_population")
        pair_total += sum(v["accepted"] for r in value["pair_generation"] for v in r.values())
        wrong_total += sum(v["accepted"] for r in value["wrong_donor_generation"] for v in r.values())
        role_eval_total += value["resource"]["alignment_role_pair_evaluations"]
        task_total += value["task"]["n"]
    check((pair_total, wrong_total, role_eval_total, task_total) == (409600, 409600, 8192000, 40960), "neural_complete_population_counts")
    na = F.load_json(RUN / "evaluation_attempt_1/neural_assessment.json")
    check(na["development_only"] is False and len(na["models"]) == 5, "neural_assessment_scope")
    check(na["actual_interval_rows"] == na["interval_family_cap"] == config["analysis"]["maximum_interval_rows"] == 560, "frozen_interval_family_size")
    intervals = {}

    def walk(value):
        if isinstance(value, dict):
            if {"id", "mean", "n", "lower", "upper", "radius", "sample_range"} <= value.keys():
                if value["id"] in intervals:
                    check(intervals[value["id"]] == value, "shared_interval_identical", value["id"])
                intervals[value["id"]] = value
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(na)
    check(len(intervals) == 560, "saved_unique_interval_count")
    interval_by_model = Counter(k.split("/", 1)[0] for k in intervals)
    check(interval_by_model == Counter({f"model{i}": 112 for i in range(5)}), "intervals_per_model")
    for name, interval in intervals.items():
        lo, hi = interval["sample_range"]
        radius = (hi-lo) * math.sqrt(math.log(2*560/.05)/(2*interval["n"]))
        check(math.isclose(radius, interval["radius"], rel_tol=0, abs_tol=1e-15), "interval_radius_fixed_K560", name)
        check(math.isclose(interval["lower"], max(lo, interval["mean"]-radius), rel_tol=0, abs_tol=1e-15) and math.isclose(interval["upper"], min(hi, interval["mean"]+radius), rel_tol=0, abs_tol=1e-15), "interval_endpoints", name)

    commands, external_failures = [], []
    command_folder = LOG / "commands"
    starts = sorted(command_folder.glob("*.start.json"))
    labels = {p.name.removesuffix(".start.json") for p in starts}
    check({"freeze_verify_before", "focused_tests", "prepare_attempt1", "evaluate_attempt1"} <= labels, "required_external_commands")
    for path in starts:
        label = path.name.removesuffix(".start.json")
        start = F.load_json(path)
        end = F.load_json(command_folder / f"{label}.end.json")
        check(all(end[k] == v for k, v in start.items()), f"external_{label}_start_preserved")
        check(end["completed_monotonic_ns"] >= end["started_monotonic_ns"], f"external_{label}_observed_duration")
        streams = {}
        for stream in ("stdout", "stderr"):
            logpath = command_folder / f"{label}.{stream}.log"
            streams[stream] = {"path": logpath.relative_to(ROOT).as_posix(), "bytes": logpath.stat().st_size, "sha256": digest(logpath)}
            check(streams[stream]["sha256"] == end[f"{stream}_sha256"], f"external_{label}_{stream}_hash")
        if end["returncode"] != 0:
            external_failures.append(label)
        if label in ("prepare_attempt1", "evaluate_attempt1"):
            action = "prepare" if label.startswith("prepare") else "evaluate"
            check(end["command"][1:] == ["-m", "v2.experiments.runner", action, "--task", "F15", "--out", "v2/work_logs/F15_v1_run1"], f"external_{label}_exact_arguments")
            check(end["returncode"] == 0 and streams["stderr"]["bytes"] == 0, f"external_{label}_successful_exit")
        commands.append(dict(end, streams=streams))
    by_label = {r["label"]: r for r in commands}
    check(F.load_json(command_folder / "evaluate_attempt1.stdout.log") == ec, "evaluation_stdout_equals_completion_manifest")
    prep_stdout = F.load_json(command_folder / "prepare_attempt1.stdout.log")
    check(prep_stdout["models"] == 5 and prep_stdout["evaluation_started"] is False and prep_stdout["attempt"] == 1, "preparation_stdout_counts")
    focused_text = (command_folder / "focused_tests.stderr.log").read_text(encoding="utf-8")
    check(re.search(r"Ran 78 tests in [0-9.]+s\s+OK\s*$", focused_text) is not None, "focused_suite_captured_78_passes")
    chronology = [
        ("freeze_command_completed", by_label["freeze_verify_before"]["completed_utc"]),
        ("focused_suite_completed", by_label["focused_tests"]["completed_utc"]),
        ("preparation_external_start", by_label["prepare_attempt1"]["started_utc"]),
        ("preparation_stage_start", stages["preparation_start"]["started_utc"]),
        ("all_five_preparation_complete", pc["completed_utc"]),
        ("preparation_external_end", by_label["prepare_attempt1"]["completed_utc"]),
        ("all_five_preexposure_validation", pre["validated_utc"]),
        ("evaluation_external_start", by_label["evaluate_attempt1"]["started_utc"]),
        ("evaluation_exposure_marker", es["started_utc"]),
        ("evaluation_stage_complete", ec["completed_utc"]),
        ("evaluation_external_end", by_label["evaluate_attempt1"]["completed_utc"]),
    ]
    times = [datetime.fromisoformat(t) for _, t in chronology]
    check(times == sorted(times), "prepared_validated_then_exposed_chronology")
    check(ec["retention_cases"] == 160 and ec["neural_models"] == 5, "completion_unit_counts")
    check(not list(RUN.rglob("failure.json")), "no_saved_stage_failure")
    result = {
        "schema": "F15-saved-artifact-execution-audit-v1",
        "contributor": "delegated ChatGPT (GPT-6 Astra Pro), execution audit",
        "audited_utc": datetime.now(timezone.utc).isoformat(),
        "audit_script_sha256": digest(Path(__file__)),
        "scope": "saved files and controls only; no F16 or scientific/contribution gate assignment",
        "source_revision_at_audit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "freeze": freeze, "audit_runtime": runtime,
        "verification_checks": checks, "unexpected_errors": errors,
        "primary_run_json_artifacts": len(expected_json), "primary_run_sidecars": len(expected_json),
        "primary_run_original_hashes_valid": len(expected_json)-len(mismatches),
        "primary_run_original_hash_exceptions": mismatches,
        "all_original_artifact_hashes_pass": not mismatches,
        "artifact_exception_disposition": "Original zero-byte redundant aggregate and original sidecar preserved; canonical bytes recovered separately with exact original SHA256 from all 160 intact case units. Cause unknown.",
        "recovery_record": (LOG / "retention_aggregate_recovery.json").relative_to(ROOT).as_posix(),
        "recovered_aggregate": {"path": recovered.relative_to(ROOT).as_posix(), "bytes": recovered.stat().st_size, "sha256": digest(recovered)},
        "source_units_complete_and_hash_valid": not errors,
        "missing_experimental_units": [], "stage_attempts": {"preparation": 1, "evaluation": 1},
        "stage_retry_count": 0, "external_command_failures": external_failures,
        "prepared_models": model_summary,
        "counts": {"retention_cases": len(cases), "retention_population_draws": len(rc["evaluation_seeds"]), "retention_method_rows": method_rows, "retention_numeric_queries": numeric_queries,
                   "neural_models": len(neural), "training_outcome_labels": sum(p["training"]["stochastic_outcome_labels"] for p in prepared), "candidate_evaluations": sum(p["resource"]["candidate_evaluations"] for p in prepared),
                   "decoder_fits": sum(p["resource"]["decoder_fits"] for p in prepared), "intended_evaluation_pairs": pair_total, "incorrect_donor_pair_records": wrong_total,
                   "alignment_role_pair_evaluations": role_eval_total, "ordinary_task_inputs": task_total, "unique_interval_rows": len(intervals), "interval_rows_per_model": dict(interval_by_model)},
        "chronology": [{"event": e, "utc": t} for e, t in chronology],
        "pre_evaluation_validation_sha256": digest(LOG / "pre_evaluation_validation.json"),
        "preparation_manifest_sha256": prep_hash,
        "evaluation_manifest_sha256": digest(RUN / "evaluation_complete.json"),
        "external_commands": commands, "artifact_inventory": inventory,
        "provenance_limits": ["Original aggregate bytes were missing at audit; exact checksum-matching recovery is disclosed rather than silently overwriting the original.",
                              "Saved start markers and validation records document this observed run; they do not prove global absence of unrecorded external evaluations.",
                              "Saved neural statistics and input/pair digests were checked without regenerating raw populations; no independent bitwise replay or cross-host numerical identity is claimed.",
                              "The pre-exposure record reports additional directory fsync; this audit checks the preserved record and model identity, not a separate historical syscall trace."],
        "population_generation_performed": False, "training_or_alignment_selection_performed": False,
        "stage_command_or_retry_performed": False, "principal_engaged_minutes_added": 0,
    }
    payload = canonical(result)
    with args.out.open("xb") as handle:
        handle.write(payload); handle.flush(); os.fsync(handle.fileno())
    with Path(str(args.out)+".sha256").open("x", encoding="ascii") as handle:
        handle.write(hashlib.sha256(payload).hexdigest()+"\n"); handle.flush(); os.fsync(handle.fileno())
    fd = os.open(args.out.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    print(json.dumps({"output": str(args.out.relative_to(ROOT)), "checks": checks, "unexpected_errors": errors,
                      "original_hashes_valid": result["primary_run_original_hashes_valid"], "original_hash_exception": mismatches,
                      "recovered_original_digest_valid": digest(recovered) == original_expected, "counts": result["counts"]}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
