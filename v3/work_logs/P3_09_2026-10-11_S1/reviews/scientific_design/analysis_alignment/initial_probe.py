"""Independent P3-09 DEVELOPMENT-only analyzer/schema counterexamples.

This imports only the captured analyzer and its lifecycle dependency. It never
imports an adapter, loads a final configuration, or invokes generate/run/score.
The report-width helper is extracted by AST from captured source and receives a
synthetic public report. All score dictionaries below are hand-written toys.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11. Principal credit: zero.
"""
from __future__ import annotations

import ast
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CAPTURE = HERE / "initial_source" / "v3" / "experiments"
sys.path.insert(0, str(CAPTURE))
spec = importlib.util.spec_from_file_location("_p309_alignment_initial_analyzer", CAPTURE / "p309_analyze.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)


def pair(value):
    value = F(value)
    return [value.numerator, value.denominator]


def broker_row(identifier, stakes, *, reference=None):
    maximum = max(F(*stakes["fp"]), F(*stakes["fn"]))
    # Two positions, identical actions in both records, exactly one false
    # positive and zero false negatives. No forecast/decision path changes.
    raw_loss = F(*stakes["fp"])
    return {
        "unit": {
            "id": identifier, "group_id": "dev-illustration", "arm": "broker",
            "configuration_id": identifier, "method": "probability_cost",
            "method_kind": "ordinary", "engine": "ordinary", "seed": None,
            "stakes": stakes, "pairing": {} if reference is None else {"stakes_reference": reference},
        },
        "score": {
            "status": "success", "validity_pass": True, "full_horizon": True,
            "horizon": 2, "rounds_closed": 2, "brier_mean": [1, 4],
            "base_brier_mean": [1, 4], "uniform_brier_mean": [1, 4],
            "action_loss_mean": pair(raw_loss / (2 * maximum)),
            "false_positives": 1, "false_negatives": 0, "terminal_errors": 1,
            "task_max_loss": pair(maximum), "weighted_action_loss_sum": pair(raw_loss),
            "cold_units": 100, "local_units": 80, "optional_reporting_units": 0,
            "native_price_normalized": pair(F(1, 10000) / maximum),
            "base_path_sha256": "development-identical-base",
            "delivered_path_sha256": "development-identical-delivered",
            "action_path_sha256": "development-identical-actions",
        },
    }


def main():
    config = {"analysis": {"loss_improvement_threshold": [1, 100],
                           "saving_ratio_threshold": [19, 20],
                           "repricing_grid": [[0, 1], [1, 10000]]}}
    group_map = {"dev-illustration": {"recipe": {"family": "disjoint-development-illustration"}}}
    reference = broker_row("dev-symmetric", {"fp": [1, 1], "fn": [1, 1]})
    current = broker_row("dev-asymmetric", {"fp": [1, 2], "fn": [3, 2]}, reference="dev-symmetric")
    analysis = A.broker_analysis(config, group_map, [reference, current])
    comparison = next(row for row in analysis["paired_records"] if row["relation"] == "stakes_reference")
    wrong_delta = comparison["differences"]["action_loss_mean_target_minus_current"]
    assert wrong_delta == [1, 3]
    correct_delta = F(1, 6) - F(1, 6)
    assert correct_delta == 0
    observations = [{
        "name": "unchanged_actions_apparent_asymmetric_improvement",
        "status": "REPRODUCED_INTERPRETATION_DEFECT",
        "reference_normalized_action_loss": reference["score"]["action_loss_mean"],
        "current_normalized_action_loss": current["score"]["action_loss_mean"],
        "analyzer_reported_target_minus_current": wrong_delta,
        "both_paths_at_current_stakes": [[1, 6], [1, 6]],
        "correct_current_objective_delta": pair(correct_delta),
        "paired_normalized_price_example": [1, 15000],
        "correct_current_priced_objective_delta": [0, 1],
        "same_action_path": comparison["path_equalities"]["action_path_sha256"],
        "explanation": "The only change is the metric's stake vector and normalization; path, confusion counts and cost are identical.",
    }]

    cold = broker_row("dev-cold", {"fp": [1, 1], "fn": [1, 1]})
    reuse = broker_row("dev-reuse", {"fp": [1, 1], "fn": [1, 1]})
    reuse["unit"]["pairing"] = {"cold_id": "dev-cold"}
    reuse["score"].update(cold_units=94, local_units=74)
    reuse_pair = A.broker_analysis(config, group_map, [cold, reuse])["paired_records"][0]
    assert reuse_pair["differences"]["cold_units_target_minus_current"] == [6, 1]
    assert reuse_pair["ordinary_identity_pass"] is None
    observations.append({
        "name": "equal_output_six_percent_saving_has_no_A4_predicate",
        "status": "REPRODUCED_MISSING_DECLARED_ENDPOINT",
        "paired_record": reuse_pair, "exact_cold_cost_ratio": [47, 50],
        "expected_A4_practical_saving_if_complete_equal_output": True,
        "absence": "No cold cost ratio, 5 percent predicate, or relation-specific A1 eligibility field is recorded.",
    })

    missing = deepcopy(reference)
    missing["score"].update(status="failed", full_horizon=False, brier_mean=None,
                            base_brier_mean=None, uniform_brier_mean=None,
                            action_loss_mean=None, cold_units=99)
    missing_analysis = A.broker_analysis(config, group_map, [missing])
    summary = missing_analysis["configuration_means"][0]
    assert not summary["complete_primary_denominator"]
    assert summary["known_total_executed_cold_units"] == 99
    assert summary["missing_or_incomplete_unit_ids"] == ["dev-symmetric"]
    assert all(not row["distinct_ordinary_minimum"]["complete_catalogue"]
               for row in missing_analysis["catalogue_comparisons"])
    observations.append({"name": "incomplete_episode_keeps_cost_and_blocks_ranking", "status": "PASS",
                         "summary": summary})
    try:
        A.rows_from_seals({"units": [{"id": "dev-required"}]}, [])
    except A.L.IntegrityError as error:
        observations.append({"name": "missing_expected_seal_cannot_shrink_denominator",
                             "status": "PASS", "exception": str(error)})
    else:
        raise AssertionError("Missing final-score seal was accepted.")

    # Only these three pure helpers are compiled; adapter module imports,
    # configuration, population recipes and execution endpoints never execute.
    source = (CAPTURE / "p309_broker.py").read_text()
    tree = ast.parse(source)
    selected = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name in {"_fraction", "_pair", "_report_widths"}]
    assert len(selected) == 3
    helpers = {"F": F}
    exec(compile(ast.Module(body=selected, type_ignores=[]), "<captured-pure-report-helpers>", "exec"), helpers)
    optional = {"report": {"status": "success", "intervals": {
        "F": {"lower": [1, 1], "upper": [9, 1], "confidence_conflict": False}},
        "deterministic_envelopes": {"F": [[0, 1], [10, 1]]}}}
    width = helpers["_report_widths"](optional, 10)
    assert width["F"]["width_per_horizon"] == [4, 5]
    assert set(width["F"]) == {"width", "width_per_horizon", "lower", "upper", "confidence_conflict"}
    observations.append({"name": "report_width_has_no_reduction_reference",
                         "status": "REPRODUCED_MISSING_DECLARED_ENDPOINT",
                         "actual_helper_output": width,
                         "deterministic_envelope_width_per_horizon": [1, 1],
                         "strict_normalized_width_gain_from_supplied_envelope": [1, 5],
                         "expected_practical_gain_at_one_percent": True,
                         "absence": "The supplied observable envelope and resulting gain are omitted, so the promised reduction threshold is not computed."})

    def certificate_row(method, ids, units, raw):
        return {"unit": {"id": "dev-certificate-" + method, "group_id": "dev-illustration",
                          "recipient": "fresh", "budget_condition": "development",
                          "method": method, "method_kind": "ordinary"},
                "score": {"all_request_ids": ["dev-1", "dev-2"], "delivered_request_ids": ids,
                          "request_count": 2, "total_units": units, "validity_pass": True,
                          "category_totals": {"producer": 0, "consumer": units, "output": 0,
                                              "storage": 0, "source": 0},
                          "tariff_category_totals": raw, "category_totals_complete": True,
                          "category_convention": "PRODUCER_IS_ALL_NONCONSUMER; OUTPUT_STORAGE_SOURCE_ARE_OVERLAPPING_DIAGNOSTICS"}}
    left = certificate_row("left", ["dev-1", "dev-2"], 90, {"native_calls": 90})
    right = certificate_row("right", ["dev-1", "dev-2"], 100, {"opcode_events": 100})
    cap_analysis = A.certificate_analysis(config, group_map, [left, right])
    cap_pair = next(row for row in cap_analysis["coverage_cost_comparisons"]
                    if row["scope"] == "dev-illustration" and row["left"] == "left")
    assert cap_pair["componentwise_resource_dominance"] is True
    assert left["score"]["tariff_category_totals"]["native_calls"] > right["score"]["tariff_category_totals"].get("native_calls", 0)
    observations.append({"name": "named_stage_dominance_is_not_raw_tariff_dominance",
                         "status": "REPRODUCED_SCOPE_QUALIFICATION",
                         "aggregate_comparison": cap_pair,
                         "raw_tariff_vectors": {"left": left["score"]["tariff_category_totals"],
                                                "right": right["score"]["tariff_category_totals"]},
                         "native_price_two_opcode_price_one_costs": {"left": 180, "right": 100},
                         "interpretation": "The predicate is correct for the five reported coordinates, but not an all-primitive-category dominance claim."})
    disjoint = A.certificate_analysis(config, group_map, [
        certificate_row("a", ["dev-1"], 90, {"native_calls": 90}),
        certificate_row("b", ["dev-2"], 100, {"native_calls": 100})])
    assert not any(row["left_practical_cost_dominance"] for row in disjoint["coverage_cost_comparisons"])
    observations.append({"name": "same_count_distinct_request_ids_not_equal_service", "status": "PASS"})
    result = {"stage": "P3-09-DEVELOPMENT-OBSERVER-ONLY", "principal_clock_credit": 0,
              "final_population_generated_or_opened": False, "adapter_endpoint_calls": 0,
              "source_manifest_sha256": hashlib.sha256((HERE / "initial_source_manifest.json").read_bytes()).hexdigest(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "observations": observations}
    out = HERE / "initial_probe_results.json"
    with out.open("x") as handle:
        json.dump(result, handle, sort_keys=True, indent=2)
        handle.write("\n")
    print(json.dumps({"status": "OBSERVATIONS_PRESERVED", "observations": len(observations),
                      "result_sha256": hashlib.sha256(out.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
