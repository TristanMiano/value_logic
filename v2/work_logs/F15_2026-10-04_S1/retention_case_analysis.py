"""Descriptive F15 case and resource analysis of immutable saved results.

Contributor: ChatGPT (GPT-6 Astra Pro). No experiment module imports, new
populations, optimization, proof production, or inferential intervals. The
case-selection rules below are post-exposure illustrations, not new tests.
"""
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import statistics
import sys


ROOT = Path(__file__).resolve().parents[3]
SESSION = Path(__file__).resolve().parent
RUN = ROOT / "v2/work_logs/F15_v1_run1"
INPUTS = []


def checked(path):
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == Path(str(path) + ".sha256").read_text().strip()
    INPUTS.append({"path": str(path.relative_to(ROOT)), "bytes": len(raw), "sha256": sha})
    return json.loads(raw)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def stats(values):
    values = list(values)
    if not values:
        return {"n": 0}
    return {"n": len(values), "minimum": min(values), "median": statistics.median(values),
            "mean": statistics.mean(values), "maximum": max(values)}


def ordinary_signature(row):
    return {key: row[key] for key in (
        "numeric", "selected", "selected_index", "executed", "executed_index",
        "decision_status", "refused", "useful_decision", "coherent_worst_regret",
        "pre_repair", "scoring", "acquisition_sensitivity")}


def native_signature(row):
    return {key: row["native"][key] for key in (
        "candidate_order", "certificate_role", "comparison", "requested_budget",
        "semantic_valid", "status", "upper_bound", "useful_derivation_candidate")}


def successful_service(row):
    return (all(x["status"] != "refused" for x in row["numeric"])
            and row["decision_status"] == "certified_order"
            and row["native"]["certificate_role"] == "selected_order"
            and row["native"]["status"] == "received")


def illustrative_row(case, row, selection_rule):
    selected = row["executed_index"]
    return {
        "seed": case["seed"], "variant": case["variant"],
        "selection_rule": selection_rule,
        "scope": "post-exposure illustration from saved rows; not a new confirmatory test",
        "row": row,
        "selected_numeric": row["numeric"][selected] if selected < 6 else None,
        "matched_fresh_same_access": next(x for x in case["methods"]
                                          if x["method"] == "fresh" and x["access"] == row["access"]),
    }


def main():
    complete = checked(RUN / "evaluation_complete.json")
    assert complete["status"] == "evaluation_complete"
    config_raw = (ROOT / "v2/experiments/config.v1.json").read_bytes()
    config = json.loads(config_raw)
    cases = [checked(RUN / f"evaluation_attempt_1/retention_{seed}_{variant}.json")
             for seed in config["retention"]["evaluation_seeds"]
             for variant in config["retention"]["variants"]]
    assert len(cases) == 160
    flat = [(case, row) for case in cases for row in case["methods"]]
    assert len(flat) == 1920

    examples = {}
    rules = {
        "useful_approximate_selected_cost": (
            "First frozen-order tailored/no-reacquisition row with a useful native derivation and approximate selected cost",
            lambda c, r: r["method"] == "tailored" and r["access"] == "no_reacquisition"
            and r["native"]["useful_derivation_candidate"]
            and r["executed_index"] < 6 and r["numeric"][r["executed_index"]]["status"] == "approximate"),
        "useful_program_decision_despite_numeric_refusal": (
            "First frozen-order tailored/no-reacquisition program-edit row with a useful native derivation and all scalar queries refused",
            lambda c, r: c["variant"] == "program_edit" and r["method"] == "tailored"
            and r["access"] == "no_reacquisition" and r["native"]["useful_derivation_candidate"]
            and all(x["status"] == "refused" for x in r["numeric"])),
        "full_law_valid_current_fiber_insufficient": (
            "First frozen-order fresh/no-reacquisition authority-loss row whose actual comparison is true but whose current fiber does not establish it",
            lambda c, r: c["variant"] in ("withdrawal", "source_drift") and r["method"] == "fresh"
            and r["access"] == "no_reacquisition" and r["scoring"]["full_source_semantic_valid"]
            and not r["native"]["semantic_valid"]),
        "two_mean_repair_without_action_improvement": (
            "First frozen-order tailored adaptive two-mean repair with the same actual action cost as its no-reacquisition mate",
            lambda c, r: r["method"] == "tailored" and r["access"] == "adaptive_reacquisition"
            and r["resources"]["acquisition_scalar_measurements"] == 2
            and any(x["method"] == "tailored" and x["access"] == "no_reacquisition"
                    and x["scoring"]["actual_executed_cost"] == r["scoring"]["actual_executed_cost"]
                    for x in c["methods"])),
        "certified_order_without_requested_fallback_receipt": (
            "First frozen-order row with certified all-alternative epsilon regret but insufficient zero-budget fallback comparison",
            lambda c, r: r["decision_status"] == "certified_order"
            and r["native"]["status"] == "insufficient_current_request"),
        "diagnostic_receipt_without_certified_order": (
            "First frozen-order row with a received fallback-comparison diagnostic but no certified procedure choice",
            lambda c, r: r["native"]["status"] == "received" and r["decision_status"] != "certified_order"),
    }
    for key, (description, predicate) in rules.items():
        matches = [(c, r) for c, r in flat if predicate(c, r)]
        examples[key] = {"matching_rows": len(matches),
                         "example": illustrative_row(*matches[0], description) if matches else None}
    worst = max(Q(r["scoring"]["realized_regret"]) for _, r in flat)
    worst_rows = [(c, r) for c, r in flat if Q(r["scoring"]["realized_regret"]) == worst]
    examples["maximum_realized_regret_including_refusal"] = {
        "maximum": str(worst), "matching_rows": len(worst_rows),
        "example": illustrative_row(*worst_rows[0], "First frozen-order row attaining the maximum recorded actual regret, including refusals"),
    }

    useful_episodes = {}
    for case in cases:
        useful = [r for r in case["methods"] if r["native"]["useful_derivation_candidate"]]
        if useful:
            useful_episodes[(case["seed"], case["variant"])] = len(useful)
    useful_by_variant = Counter(variant for seed, variant in useful_episodes)
    useful_by_seed = Counter(seed for seed, variant in useful_episodes)

    # Three comparisons within the full-information family plus one selective
    # pair give four comparisons/case/access = 1,280 direct paired checks.
    # fresh vs each other full-information method and tailored vs intervals
    # is the nonredundant baseline-facing subset: 960 paired checks.
    baseline_pairs = (("cached_proof", "fresh"), ("full_joint", "fresh"),
                      ("tailored", "exact_intervals"))
    comparisons = []
    for access in config["retention"]["access_regimes"]:
        for method, baseline in baseline_pairs:
            pairs = []
            for case in cases:
                left = next(r for r in case["methods"] if r["method"] == method and r["access"] == access)
                right = next(r for r in case["methods"] if r["method"] == baseline and r["access"] == access)
                assert ordinary_signature(left) == ordinary_signature(right)
                assert native_signature(left) == native_signature(right)
                for resource in ("acquisition_calls", "acquisition_scalar_measurements",
                                 "acquisition_path_world_executions", "acquisition_transferred_bytes"):
                    assert left["resources"][resource] == right["resources"][resource]
                pairs.append((left, right))
            groups = {}
            for label, selected_pairs in (
                ("all_equal_information_rows", pairs),
                ("both_admit_all_numbers_certify_order_and_receive_current_proof",
                 [(a, b) for a, b in pairs if successful_service(a) and successful_service(b)]),
            ):
                costs = {}
                for resource in ("resident_bytes", "total_stored_serialized_upper_bytes",
                                 "peak_serialized_working_state_upper_bytes", "initial_total_ns",
                                 "one_update_arithmetic_ns", "one_update_total_ns", "one_case_method_plus_common_ns"):
                    costs[resource] = {
                        "method": stats(a["resources"][resource] for a, b in selected_pairs),
                        "baseline": stats(b["resources"][resource] for a, b in selected_pairs),
                        "paired_method_minus_baseline": stats(a["resources"][resource] - b["resources"][resource] for a, b in selected_pairs),
                        "method_strictly_lower_count": sum(a["resources"][resource] < b["resources"][resource] for a, b in selected_pairs),
                    }
                groups[label] = {"pair_count": len(selected_pairs), "costs": costs}
            comparisons.append({"method": method, "baseline": baseline, "access": access,
                                "exact_semantic_and_acquisition_equality": True,
                                "scope": "descriptive paired local observations; no population-speed inference", "groups": groups})

    output = {
        "schema": "F15-saved-retention-case-analysis-v1",
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "new_generation": False, "new_confirmatory_intervals": 0,
        "post_exposure_illustrations": examples,
        "useful_distinct_episodes": len(useful_episodes),
        "useful_episode_count_by_variant": dict(useful_by_variant),
        "useful_episode_count_by_seed": dict(useful_by_seed),
        "equal_information_semantic_and_acquisition_pairs": 960,
        "resource_comparisons": comparisons,
        "input_manifest": INPUTS,
        "configuration_sha256": hashlib.sha256(config_raw).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    path = SESSION / "retention_case_analysis.json"
    raw = canonical(output)
    if "--check" in sys.argv:
        assert path.read_bytes() == raw
    else:
        with path.open("xb") as handle:
            handle.write(raw)
        with Path(str(path) + ".sha256").open("x") as handle:
            handle.write(hashlib.sha256(raw).hexdigest() + "\n")
    print(json.dumps({"output": str(path.relative_to(ROOT)), "bytes": len(raw),
                      "sha256": hashlib.sha256(raw).hexdigest(), "equal_information_pairs": 960,
                      "illustrations": {k: v["matching_rows"] for k, v in examples.items()}}))


if __name__ == "__main__":
    main()
