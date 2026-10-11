"""Disjoint DEVELOPMENT dictionaries for amended paired/slice/report analysis.

No population or truth is materialized, and no adapter endpoint is imported or
called. The differing population/slot counts deliberately test hierarchical
weighting; they are not a recipe or result for the final experiment.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11. Principal credit: zero.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import traceback

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "amended_v1/source/v3/experiments"
sys.path.insert(0, str(SOURCE))
spec = importlib.util.spec_from_file_location("_p309_alignment_synthetic_analyzer", SOURCE / "p309_analyze.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
checks = []


def p(value):
    value = F(value)
    return [value.numerator, value.denominator]


def check(name, actual, expected):
    if actual != expected:
        raise AssertionError(repr((name, actual, expected)))
    checks.append({"name": name, "value": actual})


def metrics(horizon, base):
    return {"horizon": horizon, "rounds_closed": horizon, "full_horizon": True,
            "brier_mean": p(base), "base_brier_mean": p(base),
            "uniform_brier_mean": [1, 1], "action_loss_mean": p(base),
            "forecast_readouts": {"constant_half_brier_mean": [1, 4],
                                  "equal_mixture_brier_mean": [1, 1],
                                  "expert_brier_means": [[1, 1]] * 6}}


def slice_row(identifier, group, high_prefix):
    prefix, suffix = F(int(high_prefix)), F(int(not high_prefix))
    first_n, first_loss = (3, F(2, 3)) if high_prefix else (2, F(1, 2))
    gain = F() if high_prefix else F(1, 50)
    endpoint = {"status": "success", "deterministic_width_per_horizon": [1, 1],
                "width_per_horizon": p(1 - gain), "normalized_width_reduction": p(gain),
                "normalized_lower_endpoint_gain": p(gain / 2),
                "normalized_upper_endpoint_gain": p(gain / 2)}
    return {"unit": {"id": identifier, "group_id": group, "engine": "broker",
                     "segments": [{"name": "dev_prefix", "start": 0, "stop": 2},
                                  {"name": "dev_new_structure_suffix", "start": 2, "stop": 4}]},
            "score": {"full_horizon": True, "validity_pass": True,
                      "first_occurrence": metrics(first_n, first_loss),
                      "segments": {"dev_prefix": metrics(2, prefix),
                                   "dev_new_structure_suffix": metrics(2, suffix)},
                      "optional_reporting_units": 200 if high_prefix else 100,
                      "paid_report_comparison": {"status": "success", "endpoints": {
                          name: deepcopy(endpoint) for name in ("F", "V", "Z")}}}}


def main():
    config = {"analysis": {"loss_improvement_threshold": [1, 100],
                           "report_width_improvement_threshold": [1, 100],
                           "saving_ratio_threshold": [19, 20], "repricing_grid": [[0, 1]]}}
    rows = [slice_row("dev-pop-a-slot", "dev-pop-a", False),
            slice_row("dev-pop-b-slot-one", "dev-pop-b", True),
            slice_row("dev-pop-b-slot-two", "dev-pop-b", True)]
    sliced = {row["slice"]: row for row in A.broker_slice_summaries(config, rows)}
    suffix = sliced["dev_new_structure_suffix"]
    first = sliced["first_occurrence"]
    check("suffix equal-population mean, not execution-weighted", suffix["means"]["base_brier_mean"], [1, 2])
    check("first-key mean, not pooled-position mean", first["means"]["base_brier_mean"], [7, 12])
    check("first-key exact scheduled positions", first["known_scheduled_positions"], 8)
    check("first-key original episode denominator", first["planned_episodes"], 3)
    report = A.broker_report_summary(config, rows)
    check("report mean at inclusive practical threshold", report["endpoints"]["F"]["means"]["normalized_width_reduction"], [1, 100])
    check("report inclusive practical flag", report["endpoints"]["F"]["practical_width_reduction"], True)
    check("report fee hierarchical mean", report["mean_additional_units"], [150, 1])
    check("report complete executed fees", report["known_total_additional_units"], 500)

    incomplete = deepcopy(rows)
    incomplete[0]["score"]["full_horizon"] = False
    bad_slice = {row["slice"]: row for row in A.broker_slice_summaries(config, incomplete)}["dev_new_structure_suffix"]
    check("complete suffix cannot repair incomplete parent denominator", bad_slice["means"]["base_brier_mean"], None)
    check("incomplete parent withholds slice practical flag", bad_slice["practical_learning_effect"], False)
    bad_report = A.broker_report_summary(config, incomplete)
    check("no success-only report mean", bad_report["endpoints"]["F"]["means"]["normalized_width_reduction"], None)
    check("no success-only report positive flag", bad_report["endpoints"]["F"]["practical_width_reduction"], False)
    check("incomplete parent fees retained", bad_report["known_total_additional_units"], 500)

    adverse = deepcopy(rows)
    for row in adverse[1:]:
        for endpoint in row["score"]["paid_report_comparison"]["endpoints"].values():
            endpoint.update(width_per_horizon=[26, 25], normalized_width_reduction=[-1, 25],
                            normalized_lower_endpoint_gain=[-1, 50], normalized_upper_endpoint_gain=[-1, 50])
    adverse_report = A.broker_report_summary(config, adverse)
    check("adverse widths are not clamped", adverse_report["endpoints"]["F"]["means"]["normalized_width_reduction"], [-1, 100])
    check("adverse mean is not practical", adverse_report["endpoints"]["F"]["practical_width_reduction"], False)
    conflict = deepcopy(rows)
    conflict[0]["score"]["paid_report_comparison"]["status"] = "confidence_conflict"
    conflict[0]["score"]["paid_report_comparison"]["endpoints"]["F"]["status"] = "confidence_conflict"
    conflicted = A.broker_report_summary(config, conflict)
    check("conflict cannot supply a usable mean width", conflicted["endpoints"]["F"]["means"]["width_per_horizon"], None)
    check("conflict ID remains in denominator", conflicted["endpoints"]["F"]["unavailable_unit_ids"], ["dev-pop-a-slot"])

    def pair_row(identifier, stakes, target=None):
        maximum = max(F(*stakes["fp"]), F(*stakes["fn"]))
        return {"unit": {"id": identifier, "group_id": "dev-common-stakes",
                         "configuration_id": identifier, "method": "probability_cost",
                         "method_kind": "ordinary", "engine": "ordinary", "stakes": stakes,
                         "pairing": {} if target is None else {"stakes_reference": target}},
                "score": {"status": "success", "full_horizon": True, "validity_pass": True,
                          "horizon": 2, "false_positives": 1, "false_negatives": 0,
                          "brier_mean": [1, 4], "base_brier_mean": [1, 4], "uniform_brier_mean": [1, 4],
                          "action_loss_mean": p(F(*stakes["fp"]) / (2 * maximum)),
                          "cold_units": 100, "local_units": 80, "optional_reporting_units": 0,
                          "native_price_normalized": p(F(1, 10000) / maximum),
                          "base_path_sha256": "development-identical", "delivered_path_sha256": "development-identical",
                          "action_path_sha256": "development-identical"}}
    reference = pair_row("dev-original-stakes", {"fp": [1, 1], "fn": [1, 1]})
    current = pair_row("dev-new-stakes", {"fp": [1, 2], "fn": [3, 2]}, "dev-original-stakes")
    paired = A.broker_analysis(config, {"dev-common-stakes": {"recipe": {"family": "DEVELOPMENT_common_objective"}}}, [reference, current])
    difference = paired["paired_records"][0]["differences"]
    check("full analyzer fixes unchanged-action stakes witness", difference["action_loss_mean_target_minus_current"], [0, 1])
    check("full analyzer fixes common priced objective", difference["common_native_objective_target_minus_current"], [0, 1])
    check("whole-pair mean cannot call it practical", paired["paired_configuration_effects"][0]["practical_action_effect"], False)
    return {"stage": "P3-09-DEVELOPMENT-SYNTHETIC-OBSERVER", "status": "PASS",
            "principal_clock_credit": 0, "final_population_generated": False,
            "worker_provider_reporter_or_private_truth_calls": 0,
            "analyzer_sha256": hashlib.sha256((SOURCE / "p309_analyze.py").read_bytes()).hexdigest(),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "checks": checks, "scope": "Hand-written score dictionaries test arithmetic and missing-data semantics. They are not outputs of any paid scientific policy."}


if __name__ == "__main__":
    try:
        result = main()
    except Exception as error:
        result = {"stage": "P3-09-DEVELOPMENT-SYNTHETIC-OBSERVER", "status": "FAIL",
                  "error": repr(error), "traceback": traceback.format_exc(), "checks": checks,
                  "principal_clock_credit": 0}
    target = HERE / "amended_v1/synthetic_results.json"
    with target.open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": result["status"], "checks": len(checks),
                      "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "error": result.get("error")}))
