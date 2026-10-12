#!/usr/bin/env python3
"""Reprice retained weighted-repair proofs. DEVELOPMENT, GPT-6 Astra Pro.

No new solver calls. Original hard/soft clauses stay fixed. Exact new optima
are computed only by a separately invoiced diagnostic after profiles are saved.
"""
from __future__ import annotations

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time

import maxsat_repair as original


INPUT = Path(__file__).with_name("maxsat_repair_results.json")
PRICES = (3, 6, 9)


def recipes(weights):
    # Fixed before any repriced exact-optimum diagnostic.
    return [
        ("identity", list(weights)),
        ("uniform_double", [2 * w for w in weights]),
        ("double_first_half", [w * (2 if j < len(weights) // 2 else 1)
                                for j, w in enumerate(weights)]),
        ("zero_last_half", [w if j < len(weights) // 2 else 0
                             for j, w in enumerate(weights)]),
        ("rotate_right", [weights[-1], *weights[:-1]]),
    ]


def compile_witness(instance, model, meter):
    n = instance["variables"]
    if type(model) is not int or not 0 <= model < 1 << n:
        raise ValueError("Invalid retained assignment")

    def satisfied(clause, category):
        meter.pay(category, "retained_clause_header")
        for lit in clause:
            meter.pay(category, "retained_literal")
            if ((model >> (abs(lit) - 1)) & 1) == int(lit > 0):
                return True
        return False

    if not all(satisfied(c, "witness_check") for c in instance["hard"]):
        raise ValueError("Retained witness is not hard-feasible")
    mask, cost = 0, 0
    meter.pay("witness_compile", "objective_violation_pass")
    for j, soft in enumerate(instance["soft"]):
        if not satisfied(soft["clause"], "witness_compile"):
            mask |= 1 << j
            cost += soft["weight"]
            meter.pay("witness_compile", "mask_and_original_weight", 2)
    meter.pay("storage", "retained_witness_and_violation_mask", n + 2)
    return {"model": model, "violation_mask": mask, "original_cost": cost}


def compile_tree(node, meter):
    leaves = set()

    def visit(part):
        meter.pay("tree_compile", "proof_node_read")
        if part[0] == "h":
            meter.pay("tree_compile", "hard_leaf_omitted")
        elif part[0] == "w":
            mask = 0
            for j in part[1]:
                meter.pay("tree_compile", "forced_clause_coefficient")
                mask |= 1 << j
            meter.pay("tree_compile", "leaf_mask_deduplication")
            leaves.add(mask)
        else:
            visit(part[2])
            visit(part[3])

    visit(node)
    if not leaves:
        raise ValueError("Hard-only refutation conflicts with the supplied feasible witness")
    meter.pay("storage", "compiled_tree_leaf_masks", len(leaves) + 1)
    return sorted(leaves)


def dot(mask, weights, meter, category):
    value = 0
    meter.pay(category, "objective_coefficient_pass")
    for j, w in enumerate(weights):
        meter.pay(category, "weight_and_coefficient_read")
        if mask & (1 << j):
            meter.pay(category, "weight_add")
            value += w
    return value


def acquire_profiles(data):
    shared = original.Meter()
    tree_setup = original.Meter()
    arm = next(a for a in data["arms"] if a["mode"] == "conventional_requested_value")
    result = []
    for row, instance in enumerate(data["instances"]):
        if instance["identity"] != original.digest({k: v for k, v in instance.items() if k != "identity"}):
            raise ValueError("Changed source identity")
        words = 8 + sum(1 + len(c) for c in instance["hard"])
        words += sum(2 + len(s["clause"]) for s in instance["soft"])
        shared.pay("source_admission", "immutable_clause_and_weight_words", words)
        shared.pay("source_admission", "checked_old_frontier_receipt", 8)
        events = [e for e in arm["events"] if e["row"] == row]
        model_limits = {instance["public_incumbent"]: None}
        for e in events:
            if e["source_identity"] != instance["identity"]:
                raise ValueError("Archived receipt has another source")
            if e["status"] == "SAT":
                model_limits[e["model"]] = e["budget"]
        witnesses = []
        for model, budget in sorted(model_limits.items()):
            compiled = compile_witness(instance, model, shared)
            if budget is not None and compiled["original_cost"] > budget:
                raise ValueError("Old positive receipt violates its original budget")
            witnesses.append(compiled)
        trees = []
        for e in events:
            if e["status"] == "UNSAT":
                # Profile compilation pays for rechecking every tree it uses.
                original.check_negative(instance, e["budget"], e["proof"], tree_setup)
                masks = compile_tree(e["proof"], tree_setup)
                trees.append({"original_budget": e["budget"], "leaf_masks": masks})
        result.append({"row": row, "source_identity": instance["identity"],
                       "old_lower": arm["final_state"][row]["lower"],
                       "old_upper": arm["final_state"][row]["upper"],
                       "witnesses": witnesses, "trees": trees})
    return result, shared, tree_setup


def evaluate(profiles, old_weights, weights, price_meters):
    witness_meter, additive_meter, ratio_meter, tree_meter = price_meters
    if len(weights) != len(old_weights) or any(type(w) is not int or w < 0 for w in weights):
        raise ValueError("Require nonnegative integer weights on the fixed soft clauses")
    if any(w <= 0 for w in old_weights):
        raise ValueError("The original source uses positive weights")
    witness_meter.pay("weight_admission", "new_nonnegative_weight_words", len(weights))
    rows = []
    for profile in profiles:
        upper, winner = None, None
        witness_costs = []
        for w in profile["witnesses"]:
            cost = dot(w["violation_mask"], weights, witness_meter, "witness_reprice")
            witness_costs.append({"model": w["model"], "cost": cost})
            witness_meter.pay("witness_reprice", "incumbent_minimum")
            if upper is None or cost < upper:
                upper, winner = cost, w["model"]
        additive_meter.pay("scalar_reprice", "delta_weight_bounds", 2 * len(weights))
        additive = max(0, profile["old_lower"] + sum(min(0, w - old) for w, old in zip(weights, old_weights)))
        ratio_meter.pay("scalar_ratio", "ratio_form_and_minimum", 2 * len(weights))
        ratio = min(Fraction(w, old) for w, old in zip(weights, old_weights))
        product = profile["old_lower"] * ratio
        ratio_lower = -(-product.numerator // product.denominator)
        ratio_meter.pay("scalar_ratio", "multiply_and_integer_round", 2)
        scalar = max(additive, ratio_lower)
        tree_lower, tree_values = 0, []
        for tree in profile["trees"]:
            leaf_values = [dot(mask, weights, tree_meter, "tree_reprice") for mask in tree["leaf_masks"]]
            tree_meter.pay("tree_reprice", "leaf_minimum", len(leaf_values))
            bound = min(leaf_values)
            tree_values.append(bound)
            tree_lower = max(tree_lower, bound)
            tree_meter.pay("tree_reprice", "tree_maximum")
        assert tree_lower >= scalar >= additive >= 0
        assert tree_lower <= upper
        prices = []
        for p in PRICES:
            witness_meter.pay("price_profile", "retained_action_cost", 1)
            additive_meter.pay("price_profile", "regret_bound", 2)
            ratio_meter.pay("price_profile", "regret_bound", 2)
            tree_meter.pay("price_profile", "regret_bound", 2)
            prices.append({"price": p, "retained_action_cost": min(upper, p),
                           "additive_regret_bound": min(upper, p) - min(additive, p),
                           "scalar_regret_bound": min(upper, p) - min(scalar, p),
                           "tree_regret_bound": min(upper, p) - min(tree_lower, p)})
        rows.append({"row": profile["row"], "lower_additive": additive,
                     "lower_scalar_with_ratio": scalar, "lower_tree": tree_lower,
                     "upper_shared_witnesses": upper, "selected_witness": winner,
                     "witness_costs": witness_costs, "tree_lower_values": tree_values,
                     "prices": prices})
    return rows


def exact_diagnostic(instances, edits):
    """Exhaustive source check; never called while constructing profiles."""
    meter = original.Meter()
    exact = {name: [] for name, _ in edits}
    feasible_models = []
    for instance in instances:
        feasible = []
        for model in range(1 << instance["variables"]):
            meter.pay("diagnostic", "assignment_considered")
            valid = True
            for clause in instance["hard"]:
                satisfied = False
                meter.pay("diagnostic", "hard_clause")
                for lit in clause:
                    meter.pay("diagnostic", "hard_literal")
                    if ((model >> (abs(lit) - 1)) & 1) == int(lit > 0):
                        satisfied = True
                        break
                if not satisfied:
                    valid = False
                    break
            if valid:
                mask = 0
                for j, soft in enumerate(instance["soft"]):
                    sat = False
                    meter.pay("diagnostic", "soft_clause")
                    for lit in soft["clause"]:
                        meter.pay("diagnostic", "soft_literal")
                        if ((model >> (abs(lit) - 1)) & 1) == int(lit > 0):
                            sat = True
                            break
                    if not sat:
                        mask |= 1 << j
                feasible.append((model, mask))
        feasible_models.append(len(feasible))
        for name, weights in edits:
            values = [dot(mask, weights, meter, "diagnostic_weight_evaluation") for _, mask in feasible]
            meter.pay("diagnostic", "exact_minimum", len(values))
            exact[name].append(min(values))
    return {"invoice": meter.record(), "assignments_enumerated": sum(1 << i["variables"] for i in instances),
            "feasible_assignment_counts": feasible_models, "exact_optima": exact,
            "scope": "Paid exhaustive diagnostic after profile construction; no values enter a transported profile."}


def main(destination):
    if destination.exists():
        raise FileExistsError("Preserve existing development evidence")
    start = time.perf_counter_ns()
    data = json.loads(INPUT.read_text())
    if data["status"] != "complete" or original.digest(data["instances"]) != data["source_identity"]:
        raise ValueError("Incomplete or changed original evidence")
    if hashlib.sha256(Path(original.__file__).read_bytes()).hexdigest() != data["implementation_sha256"]:
        raise ValueError("Original checked-provider implementation changed")
    old_weights = [s["weight"] for s in data["instances"][0]["soft"]]
    if any([s["weight"] for s in i["soft"]] != old_weights for i in data["instances"]):
        raise ValueError("This probe uses one common original weight vector")
    edits = recipes(old_weights)
    result = {"status": "running", "evidence": "DEVELOPMENT", "contributor": "ChatGPT (GPT-6 Astra Pro)",
              "start_utc": datetime.now(timezone.utc).isoformat(), "command": sys.argv,
              "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "input_result_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
              "input_source_identity": data["source_identity"], "old_weights": old_weights,
              "declared_edits": [{"name": name, "weights": weights} for name, weights in edits],
              "prices": PRICES, "new_solver_calls": 0,
              "tariff": "Named operations at one service unit each. Shared source/witness compilation paid equally. Only the tree method pays old-proof rechecking, leaf compilation and tree repricing. Additive/scalar comparators use previously checked scalar receipts as trusted archive records. Exact diagnostics invoiced separately.",
              "cases": []}

    def save():
        destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    save()
    try:
        cpu = time.process_time_ns()
        profiles, shared_setup, tree_setup = acquire_profiles(data)
        result["compiled_profiles"] = profiles
        result["compilation"] = {"shared": shared_setup.record(), "tree_only": tree_setup.record()}
        meters = tuple(original.Meter() for _ in range(4))
        for name, weights in edits:
            before = [m.total for m in meters]
            rows = evaluate(profiles, old_weights, weights, meters)
            cumulative_shared = shared_setup.total + meters[0].total
            result["cases"].append({"name": name, "weights": weights, "rows": rows,
                 "incremental_repricing_units": {key: meter.total - previous for key, meter, previous
                     in zip(("shared_witness", "additive", "ratio_extra", "tree"), meters, before)},
                 "cumulative_total_units": {"additive": cumulative_shared + meters[1].total,
                    "scalar_with_ratio": cumulative_shared + meters[1].total + meters[2].total,
                    "tree": cumulative_shared + tree_setup.total + meters[3].total},
                 "strict_lower_improvements_over_additive": sum(r["lower_tree"] > r["lower_additive"] for r in rows),
                 "strict_lower_improvements_over_scalar_ratio": sum(r["lower_tree"] > r["lower_scalar_with_ratio"] for r in rows)})
            save()
        result["profile_process_ns"] = time.process_time_ns() - cpu
        result["repricing_invoices"] = {key: meter.record() for key, meter
                    in zip(("shared_witness", "additive", "ratio_extra", "tree"), meters)}
        result["status"] = "profiles_complete_before_exact_diagnostic"
        save()
        diagnostic_cpu = time.process_time_ns()
        result["exact_diagnostic"] = exact_diagnostic(data["instances"], edits)
        result["diagnostic_process_ns"] = time.process_time_ns() - diagnostic_cpu
        for case in result["cases"]:
            exact = result["exact_diagnostic"]["exact_optima"][case["name"]]
            assert all(r["lower_tree"] <= optimum <= r["upper_shared_witnesses"] for r, optimum in zip(case["rows"], exact))
        result["checks"] = {"all_transported_bounds_contain_exact_diagnostic": True,
                            "tree_lower_dominates_additive_and_ratio_bounds": True,
                            "original_weight_exact_diagnostic_matches_saved_reference": result["exact_diagnostic"]["exact_optima"]["identity"] == data["post_run_exact_optima"],
                            "all_methods_share_identical_retained_witnesses": True}
        assert result["checks"]["original_weight_exact_diagnostic_matches_saved_reference"]
        result["status"] = "complete"
    except Exception as error:
        result["status"] = "failed"
        result["error"] = {"type": type(error).__name__, "message": str(error)}
        save()
        raise
    result["end_utc"] = datetime.now(timezone.utc).isoformat()
    result["elapsed_wall_ns"] = time.perf_counter_ns() - start
    save()
    print(json.dumps({"status": result["status"], "compilation_units": {k: v["total"] for k, v in result["compilation"].items()},
                     "cases": [{"name": c["name"], "strict_over_additive": c["strict_lower_improvements_over_additive"],
                       "strict_over_ratio": c["strict_lower_improvements_over_scalar_ratio"],
                       "units": c["cumulative_total_units"],
                       "price6_mean_regret_bounds": {key: sum(r["prices"][1][key] for r in c["rows"]) / len(c["rows"])
                          for key in ("additive_regret_bound", "scalar_regret_bound", "tree_regret_bound")}}
                         for c in result["cases"]],
                     "diagnostic_units": result["exact_diagnostic"]["invoice"]["total"]}))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("maxsat_reprice_results.json"))
