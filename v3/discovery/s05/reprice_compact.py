#!/usr/bin/env python3
"""Exact nonnegative-weight profile compression. DEVELOPMENT, GPT-6 Astra Pro.

Fixed subset reductions and LSB recurrence; no solver or optimum diagnostic.
Preserves every earlier evidence file. Costs are named service operations,
not measured instruction counts or a claim about production solver speed.
"""
from __future__ import annotations

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time

import maxsat_repair as source
import maxsat_reprice as raw


HERE = Path(__file__).parent
INPUT = HERE / "maxsat_reprice_results.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subset(a, b, meter, category):
    meter.pay(category, "mask_pair_read", 2)
    meter.pay(category, "bitwise_and_and_equality", 2)
    return a & b == a


def minimal_indices(masks, meter, category):
    """Fixed input-order all-pairs scan, stopping at first valid dominator."""
    kept, removed = [], []
    for i, b in enumerate(masks):
        meter.pay(category, "candidate_mask_read")
        dominator = None
        for j, a in enumerate(masks):
            if i == j:
                continue
            if subset(a, b, meter, category):
                meter.pay(category, "strict_or_earlier_tie_test", 2)
                if a != b or j < i:
                    dominator = j
                    break
        if dominator is None:
            kept.append(i)
        else:
            removed.append({"removed_index": i, "dominator_index": dominator})
        meter.pay(category, "reduction_decision_write")
    return kept, removed


def family_leq(left, right, meter):
    """Sufficient certificate min(left.w) <= min(right.w), for all w>=0."""
    for b in right:
        found = False
        for a in left:
            if subset(a, b, meter, "tree_family_reduction"):
                found = True
                break
        if not found:
            return False
    return True


def compile_reductions(profiles, variable_counts):
    shared, trees = source.Meter(), source.Meter()
    compact, certificates = [], []
    for profile, n in zip(profiles, variable_counts):
        witnesses = profile["witnesses"]
        keep, removed_witnesses = minimal_indices(
            [w["violation_mask"] for w in witnesses], shared, "witness_reduction")
        retained_witnesses = [witnesses[i] for i in keep]
        shared.pay("storage", "compact_witness_words", (n + 2) * len(keep))
        families, leaf_certificates = [], []
        for tree in profile["trees"]:
            indices, removed = minimal_indices(tree["leaf_masks"], trees, "leaf_reduction")
            families.append([tree["leaf_masks"][i] for i in indices])
            leaf_certificates.append(removed)
        leq = {}
        for i, left in enumerate(families):
            for j, right in enumerate(families):
                if i != j:
                    leq[i, j] = family_leq(left, right, trees)
                    trees.pay("tree_family_reduction", "relation_bit_write")
        retained_trees, removed_trees = [], []
        for i, family in enumerate(families):
            dominator = None
            for j in range(len(families)):
                if i != j:
                    trees.pay("tree_family_reduction", "dominance_and_tie_decision", 2)
                    if leq[i, j] and (not leq[j, i] or j < i):
                        dominator = j
                        break
            if dominator is None:
                retained_trees.append({"original_tree_index": i, "leaf_masks": family})
                trees.pay("storage", "compact_tree_header_and_masks", 1 + len(family))
            else:
                removed_trees.append({"removed_index": i, "dominator_index": dominator})
        compact.append({"row": profile["row"], "source_identity": profile["source_identity"],
                        "old_lower": profile["old_lower"], "witnesses": retained_witnesses,
                        "trees": retained_trees})
        certificates.append({"row": profile["row"], "witness_removals": removed_witnesses,
                             "leaf_removals_by_original_tree": leaf_certificates,
                             "tree_removals": removed_trees})
    return compact, certificates, shared, trees


def compile_dag(profiles, include_trees):
    """Parent-before-child DFS; one fixed least-significant-bit recurrence."""
    meter, nodes, known = source.Meter(), [], {0}
    meter.pay("storage", "constant_zero_cell")

    def ensure(mask):
        meter.pay("dag_compile", "mask_read_and_seen_lookup", 2)
        if mask in known:
            return
        low = mask & -mask
        parent = mask ^ low
        index = low.bit_length() - 1
        meter.pay("dag_compile", "lsb_parent_and_index_arithmetic", 5)
        ensure(parent)
        known.add(mask)
        nodes.append({"mask": mask, "parent": parent, "weight_index": index})
        meter.pay("dag_compile", "node_registration")
        meter.pay("storage", "compiled_node_words", 3)
    for profile in profiles:
        for witness in profile["witnesses"]:
            meter.pay("dag_compile", "demanded_mask_read")
            ensure(witness["violation_mask"])
        if include_trees:
            for tree in profile["trees"]:
                for mask in tree["leaf_masks"]:
                    meter.pay("dag_compile", "demanded_mask_read")
                    ensure(mask)
    meter.pay("storage", "evaluation_workspace_cells", len(nodes) + 1)
    return nodes, meter


def evaluate(profiles, nodes, old_weights, weights, tree_mode):
    meter = source.Meter()
    if len(weights) != len(old_weights) or any(type(w) is not int or w < 0 for w in weights):
        raise ValueError("Fixed clause identities and nonnegative integer weights required")
    meter.pay("weight_admission", "new_nonnegative_weight_words", len(weights))
    sums = {0: 0}
    meter.pay("dag_evaluation", "zero_cell_write")
    for node in nodes:
        meter.pay("dag_evaluation", "instruction_words_read", 3)
        meter.pay("dag_evaluation", "parent_value_and_weight_read", 2)
        meter.pay("dag_evaluation", "sum_add_and_write", 2)
        sums[node["mask"]] = sums[node["parent"]] + weights[node["weight_index"]]
    if not tree_mode:
        # The strengthened scalar control also shares vector-level arithmetic.
        meter.pay("scalar_global", "delta_weight_bounds", 2 * len(weights))
        delta = sum(min(0, w - old) for w, old in zip(weights, old_weights))
        meter.pay("scalar_global", "ratio_form_and_minimum", 2 * len(weights))
        ratio = min(Fraction(w, old) for w, old in zip(weights, old_weights))
    rows = []
    for profile in profiles:
        upper, winner = None, None
        for witness in profile["witnesses"]:
            meter.pay("witness_selection", "sum_lookup_and_minimum", 2)
            cost = sums[witness["violation_mask"]]
            if upper is None or cost < upper:
                upper, winner = cost, witness["model"]
        if tree_mode:
            lower = 0
            for tree in profile["trees"]:
                values = []
                for mask in tree["leaf_masks"]:
                    meter.pay("tree_selection", "sum_lookup_and_leaf_minimum", 2)
                    values.append(sums[mask])
                meter.pay("tree_selection", "tree_maximum")
                lower = max(lower, min(values))
        else:
            meter.pay("scalar_row", "additive_shift_clip_and_compare", 3)
            additive = max(0, profile["old_lower"] + delta)
            product = profile["old_lower"] * ratio
            meter.pay("scalar_row", "multiply_and_integer_round", 2)
            lower = max(additive, -(-product.numerator // product.denominator))
        prices = []
        for p in raw.PRICES:
            meter.pay("price_profile", "retained_action_cost")
            meter.pay("price_profile", "regret_bound", 2)
            prices.append({"price": p, "retained_action_cost": min(upper, p),
                           "regret_bound": min(upper, p) - min(lower, p)})
        rows.append({"row": profile["row"], "lower": lower, "upper": upper,
                     "selected_witness": winner, "prices": prices})
    return rows, meter


def payload(profiles, variable_counts, nodes=None, include_trees=True):
    witnesses = sum((n + 2) * len(p["witnesses"]) for p, n in zip(profiles, variable_counts))
    trees = sum(1 + len(t["leaf_masks"]) for p in profiles for t in p["trees"]) if include_trees else 0
    dag = 0 if nodes is None else 3 * len(nodes) + 1
    workspace = 0 if nodes is None else len(nodes) + 1
    return {"witness_words": witnesses, "tree_words": trees, "dag_words": dag,
            "persistent_words": witnesses + trees + dag, "dag_workspace_cells": workspace,
            "persistent_plus_dag_workspace": witnesses + trees + dag + workspace}


def main(destination):
    if destination.exists():
        raise FileExistsError("Preserve existing development evidence")
    start = time.perf_counter_ns()
    archive_bytes = INPUT.read_bytes()
    saved = json.loads(archive_bytes)
    original_bytes = raw.INPUT.read_bytes()
    data = json.loads(original_bytes)
    if saved["status"] != "complete" or data["status"] != "complete":
        raise ValueError("Need complete original receipts")
    if sha(Path(raw.__file__)) != saved["implementation_sha256"]:
        raise ValueError("Original repricing implementation changed")
    if sha(Path(source.__file__)) != data["implementation_sha256"]:
        raise ValueError("Original provider implementation changed")
    if hashlib.sha256(original_bytes).hexdigest() != saved["input_result_sha256"]:
        raise ValueError("Original input evidence changed")
    if source.digest(data["instances"]) != data["source_identity"]:
        raise ValueError("Changed source instances")
    weights = saved["old_weights"]
    edits = raw.recipes(weights)
    assert [{"name": name, "weights": w} for name, w in edits] == saved["declared_edits"]
    result = {"status": "running", "evidence": "DEVELOPMENT",
              "contributor": "ChatGPT (GPT-6 Astra Pro)",
              "start_utc": datetime.now(timezone.utc).isoformat(), "command": sys.argv,
              "implementation_sha256": sha(Path(__file__)),
              "input_result_sha256": hashlib.sha256(archive_bytes).hexdigest(),
              "input_source_identity": data["source_identity"], "declared_edits": saved["declared_edits"],
              "new_solver_calls": 0, "new_optimum_diagnostics": 0,
              "tariff": "One unit per named operation. Original admissions, witness checks and proof checks are inherited/reproduced in full. New reductions charge each pair read, AND/equality, decision and profile word. Each LSB node charges compilation, three instruction words and a workspace cell; each edit charges seven units per node plus zero initialization. Selection reads/comparisons and price reports are charged. Original raw bills are preserved. A strengthened scalar control receives witness reduction, its own shared DAG and once-per-vector delta/ratio computation. JSON, hashing, Python bookkeeping and diagnostic report serialization are infrastructure, as in the original service tariff; units are not CPU instructions or bytes.",
              "cases": []}

    def save():
        destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    save()
    try:
        cpu = time.process_time_ns()
        profiles, admission, tree_admission = raw.acquire_profiles(data)
        assert profiles == saved["compiled_profiles"]
        assert admission.record() == saved["compilation"]["shared"]
        assert tree_admission.record() == saved["compilation"]["tree_only"]
        counts = [i["variables"] for i in data["instances"]]
        compact, certificates, witness_reduction, tree_reduction = compile_reductions(profiles, counts)
        tree_dag, tree_dag_compile = compile_dag(compact, True)
        scalar_dag, scalar_dag_compile = compile_dag(compact, False)
        result["compiled_profiles"] = compact
        result["reduction_certificates"] = certificates
        result["dag"] = {"tree_and_witness": tree_dag, "scalar_witness_only": scalar_dag}
        result["compilation_invoices"] = {key: meter.record() for key, meter in (
            ("shared_original_admission", admission), ("original_tree_check_and_compile", tree_admission),
            ("shared_witness_reduction", witness_reduction), ("tree_reduction", tree_reduction),
            ("tree_dag", tree_dag_compile), ("scalar_witness_dag", scalar_dag_compile))}
        tree_extra = witness_reduction.total + tree_reduction.total + tree_dag_compile.total
        scalar_extra = witness_reduction.total + scalar_dag_compile.total
        tree_setup = admission.total + tree_admission.total + tree_extra
        scalar_setup = admission.total + scalar_extra
        result["setup_totals"] = {"raw_tree": admission.total + tree_admission.total,
                                  "original_scalar_ratio": admission.total,
                                  "compact_tree": tree_setup, "compact_scalar_ratio": scalar_setup,
                                  "compact_tree_increment_from_existing_raw_profiles": tree_extra,
                                  "compact_scalar_increment_from_existing_witness_profiles": scalar_extra}
        result["storage"] = {"scope": "Logical payload under the original witness n+2-word convention, one word per tree header/mask, three per DAG instruction and one zero cell. Excludes unchanged source/receipt archive, common row metadata, Python containers and execution stack. DAG workspace is shown separately. Old profile writes are still charged during migration although raw transient profiles may subsequently be released.",
                             "raw_tree": payload(profiles, counts),
                             "original_scalar_ratio": payload(profiles, counts, include_trees=False),
                             "compact_tree": payload(compact, counts, tree_dag),
                             "compact_scalar_ratio": payload(compact, counts, scalar_dag, False)}
        result["counts"] = {"raw_witnesses": sum(len(p["witnesses"]) for p in profiles),
                            "retained_witnesses": sum(len(p["witnesses"]) for p in compact),
                            "raw_trees": sum(len(p["trees"]) for p in profiles),
                            "retained_trees": sum(len(p["trees"]) for p in compact),
                            "raw_leaf_occurrences": sum(len(t["leaf_masks"]) for p in profiles for t in p["trees"]),
                            "retained_leaf_occurrences": sum(len(t["leaf_masks"]) for p in compact for t in p["trees"]),
                            "tree_dag_nonzero_nodes": len(tree_dag), "scalar_dag_nonzero_nodes": len(scalar_dag)}
        tree_running, scalar_running = tree_setup, scalar_setup
        equality_rows, tie_changed = 0, 0
        result["evaluation_invoices"] = []
        for (name, new_weights), reference in zip(edits, saved["cases"]):
            assert name == reference["name"]
            tree_rows, tree_meter = evaluate(compact, tree_dag, weights, new_weights, True)
            scalar_rows, scalar_meter = evaluate(compact, scalar_dag, weights, new_weights, False)
            tree_running += tree_meter.total
            scalar_running += scalar_meter.total
            for t, s, ref in zip(tree_rows, scalar_rows, reference["rows"]):
                assert t["upper"] == s["upper"] == ref["upper_shared_witnesses"]
                assert t["lower"] == ref["lower_tree"]
                assert s["lower"] == ref["lower_scalar_with_ratio"]
                assert t["lower"] <= t["upper"]
                assert t["selected_witness"] == s["selected_witness"]
                tie_changed += t["selected_witness"] != ref["selected_witness"]
                equality_rows += 1
            raw_increment = reference["incremental_repricing_units"]
            result["cases"].append({"name": name, "weights": new_weights,
                "rows": {"compact_tree": tree_rows, "compact_scalar_ratio": scalar_rows},
                "incremental_units": {"raw_tree": raw_increment["shared_witness"] + raw_increment["tree"],
                                      "original_scalar_ratio": raw_increment["shared_witness"] + raw_increment["additive"] + raw_increment["ratio_extra"],
                                      "compact_tree": tree_meter.total, "compact_scalar_ratio": scalar_meter.total},
                "cumulative_units": {"raw_tree": reference["cumulative_total_units"]["tree"],
                                     "original_scalar_ratio": reference["cumulative_total_units"]["scalar_with_ratio"],
                                     "compact_tree": tree_running, "compact_scalar_ratio": scalar_running}})
            result["evaluation_invoices"].append({"name": name, "tree": tree_meter.record(), "scalar": scalar_meter.record()})
        result["process_ns"] = time.process_time_ns() - cpu
        result["checks"] = {"recompiled_raw_profiles_equal_saved": True,
                            "reproduced_original_setup_invoices": True,
                            "equal_tree_lower_and_witness_upper_row_edits": equality_rows,
                            "equal_scalar_lower_row_edits": equality_rows,
                            "changed_equal_cost_witness_ties": tie_changed,
                            "original_files_unchanged": sha(INPUT) == result["input_result_sha256"] and sha(raw.INPUT) == saved["input_result_sha256"],
                            "no_exact_optimum_field_used": True,
                            "all_five_exposed_recipes_retained": True}
        assert result["checks"]["original_files_unchanged"]
        result["status"] = "complete"
    except Exception as error:
        result["status"] = "failed"
        result["error"] = {"type": type(error).__name__, "message": str(error)}
        save()
        raise
    result["end_utc"] = datetime.now(timezone.utc).isoformat()
    result["elapsed_wall_ns"] = time.perf_counter_ns() - start
    save()
    print(json.dumps({"status": result["status"], "counts": result["counts"],
                      "setup": result["setup_totals"], "storage": result["storage"],
                      "cases": [{k: c[k] for k in ("name", "incremental_units", "cumulative_units")} for c in result["cases"]],
                      "checks": result["checks"]}, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "reprice_compact_results.json")
