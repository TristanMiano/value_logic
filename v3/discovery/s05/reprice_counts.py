"""Paid fixed laminar count compression of retained repair trees. DEVELOPMENT.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. No new provider or exact-source calls.
Groups are fixed before exposure: whole, halves, pairs and singleton indices.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import maxsat_reprice as old


def fixed_family(meter):
    nodes = []
    def visit(start, stop, key):
        children = []
        if stop-start > 1:
            middle = (start+stop)//2
            children = [2*key, 2*key+1]
            visit(start, middle, children[0])
            visit(middle, stop, children[1])
        node = dict(key=key, mask=((1 << (stop-start))-1) << start,
                    size=stop-start, children=children)
        meter.pay("count_family", "public_laminar_node_build", 5)
        meter.pay("storage", "fixed_family_node_retained", 4+len(children))
        nodes.append(node)
    visit(0, 8, 1)
    return nodes


def compile_counts(profile, family, meter):
    raw, quota, support = {}, {}, {}
    for node in family:
        key, group = node["key"], node["mask"]
        best, origin = 0, None
        meter.pay("count_compile", "group_source_binding", 3)
        for t, tree in enumerate(profile["trees"]):
            minimum = node["size"]
            for leaf in tree["leaf_masks"]:
                meter.pay("count_compile", "leaf_group_intersection_popcount_minimum", 4)
                minimum = min(minimum, (leaf & group).bit_count())
            meter.pay("count_compile", "strongest_tree_count", 2)
            if minimum > best:
                best, origin = minimum, t
        raw[key], support[key] = best, origin
        child_sum = sum(quota[child] for child in node["children"])
        meter.pay("count_compile", "disjoint_child_sum_and_parent_closure", 2+len(node["children"]))
        quota[key] = max(best, child_sum)
        if not 0 <= quota[key] <= node["size"]:
            raise ValueError("Inconsistent source-bound group quota")
    meter.pay("storage", "raw_closed_quotas_and_support_provenance", 3*len(family)+2)
    return dict(row=profile["row"], source_identity=profile["source_identity"],
                raw=raw, quota=quota, support_tree=support)


def price_order(weights, meter):
    if len(weights) != 8 or any(type(w) is not int or w < 0 for w in weights):
        raise ValueError("Eight fixed soft identities and nonnegative integer weights required")
    meter.pay("count_reprice", "weight_vector_admission", len(weights))
    order = []
    for i in range(8):
        j = len(order)
        while j:
            meter.pay("count_reprice", "weight_index_sort_comparison")
            if (weights[order[j-1]], order[j-1]) <= (weights[i], i):
                break
            j -= 1
        meter.pay("count_reprice", "weight_index_sort_move", len(order)-j+1)
        order.insert(j, i)
    meter.pay("storage", "reprice_weight_order", len(order))
    return order


def minimum_cost(compiled, family, weights, order, meter):
    """Exact laminar lower-quota optimum by bottom-up cheapest additions.

    This uses the standard laminar-matroid complement greedy property, not a
    supplied source optimum or a distributional assumption. Quotas are closed.
    """
    chosen = 0
    for node in family:
        q = compiled["quota"][node["key"]]
        needed = q-(chosen & node["mask"]).bit_count()
        meter.pay("count_reprice", "quota_selected_count_and_deficit", 5)
        if needed > 0:
            for i in order:
                meter.pay("count_reprice", "ordered_group_candidate", 3)
                bit = 1 << i
                if node["mask"] & bit and not chosen & bit:
                    chosen |= bit
                    needed -= 1
                    meter.pay("count_reprice", "quota_element_selected", 3)
                    if needed == 0:
                        break
            assert needed == 0
    for node in family:
        meter.pay("count_check", "selected_quota_feasibility", 3)
        assert (chosen & node["mask"]).bit_count() >= compiled["quota"][node["key"]]
    cost = old.dot(chosen, weights, meter, "count_reprice")
    meter.pay("storage", "count_bound_and_relaxation_mask", 3)
    return cost, chosen


def kernel_smoke(family):
    # Hand-checkable quota problems, not diagnostics of any source instance.
    def closed(values):
        quota = {}
        for node in family:
            quota[node["key"]] = max(values.get(node["key"], 0),
                                     sum(quota[c] for c in node["children"]))
        return dict(quota=quota)
    checks = []
    weights = [9, 1, 7, 3, 8, 2, 6, 4]
    for raw, expected in (({}, 0), ({1: 3, 2: 1, 3: 1}, 6),
                           ({1: 3, 4: 2, 3: 1}, 12)):
        meter = old.original.Meter()
        value, mask = minimum_cost(closed(raw), family, weights, price_order(weights, meter), meter)
        assert value == expected
        checks.append(dict(raw=raw, expected=expected, value=value, chosen=mask))
    meter = old.original.Meter()
    value, _ = minimum_cost(closed({1: 8}), family, [0]*8, price_order([0]*8, meter), meter)
    assert value == 0
    return dict(cases=checks, zero_weight_case=True,
                scope="Synthetic kernel checks only; no source optimum enumerated")


def main(destination):
    if destination.exists():
        raise FileExistsError("Preserve existing count-profile exposure")
    start, cpu = time.perf_counter_ns(), time.process_time_ns()
    input_path = Path(old.__file__).with_name("maxsat_reprice_results.json")
    archived = json.loads(input_path.read_text())
    original_data = json.loads(old.INPUT.read_text())
    if archived["status"] != "complete" or original_data["status"] != "complete":
        raise ValueError("Incomplete retained source")
    if hashlib.sha256(Path(old.__file__).read_bytes()).hexdigest() != archived["implementation_sha256"]:
        raise ValueError("Original repricing implementation changed")
    if hashlib.sha256(old.INPUT.read_bytes()).hexdigest() != archived["input_result_sha256"]:
        raise ValueError("Retained source result changed")
    if hashlib.sha256(Path(old.original.__file__).read_bytes()).hexdigest() != original_data["implementation_sha256"]:
        raise ValueError("Original proof checker changed")
    result = dict(status="running", evidence="DEVELOPMENT", contributor="ChatGPT (GPT-6 Astra Pro)",
                  start_utc=datetime.now(timezone.utc).isoformat(), command=sys.argv,
                  implementation_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  previous_result_sha256=hashlib.sha256(input_path.read_bytes()).hexdigest(),
                  original_result_sha256=hashlib.sha256(old.INPUT.read_bytes()).hexdigest(),
                  new_solver_calls=0, exact_source_diagnostic_calls=0,
                  scope="Same five exposed weight recipes. Fixed whole/half/pair/singleton family; no group tuning. Old proof and witness compilation are rechecked and billed once as a common build cost for count/full profiles. Existing scalar receipts remain trusted like the original control. No archived or new diagnostic optimum enters this probe.",
                  tariff="One unit per named word operation; bit intersection/popcount/minimum charged four units on an eight-bit mask. Every control shares source/witness work. Count compilation, provenance storage, weight ordering, greedy selection and checks are additional. JSON/hash harness work is timed but not a full instruction tariff.",
                  cases=[])
    def save():
        destination.write_text(json.dumps(result, separators=(",", ":"))+"\n")
    save()
    profiles, shared_setup, tree_setup = old.acquire_profiles(original_data)
    assert profiles == archived["compiled_profiles"]
    count_setup = old.original.Meter()
    family = fixed_family(count_setup)
    result["family"] = family
    result["kernel_smoke"] = kernel_smoke(family)
    compiled = [compile_counts(p, family, count_setup) for p in profiles]
    witness_checks = old.original.Meter()
    for profile, counts in zip(profiles, compiled):
        for witness in profile["witnesses"]:
            for node in family:
                witness_checks.pay("validation", "retained_witness_quota", 3)
                assert (witness["violation_mask"] & node["mask"]).bit_count() >= counts["quota"][node["key"]]
    result["compiled_counts"] = compiled
    result["compilation"] = dict(shared=shared_setup.record(), proof_and_leaf=tree_setup.record(),
                                 count_addition=count_setup.record())
    result["retained_witness_validation"] = witness_checks.record()
    result["storage_shape"] = dict(active_quota_cells=len(compiled)*len(family),
                                    full_leaf_mask_cells=sum(len(t["leaf_masks"]) for p in profiles for t in p["trees"]),
                                    full_trees=sum(len(p["trees"]) for p in profiles),
                                    scope="Active runtime cells; common source identities and retained historical proof/provenance archives are additional")
    meters = tuple(old.original.Meter() for _ in range(4))
    count_meter = old.original.Meter()
    weights0 = archived["old_weights"]
    edits = old.recipes(weights0)
    assert [dict(name=n, weights=w) for n, w in edits] == archived["declared_edits"]
    for name, weights in edits:
        before = [m.total for m in meters]+[count_meter.total]
        rw, rc = time.perf_counter_ns(), time.process_time_ns()
        rows = old.evaluate(profiles, weights0, weights, meters)
        reference = next(c for c in archived["cases"] if c["name"] == name)
        assert rows == reference["rows"]
        base_time = dict(process_ns=time.process_time_ns()-rc, wall_ns=time.perf_counter_ns()-rw)
        rw, rc = time.perf_counter_ns(), time.process_time_ns()
        order = price_order(weights, count_meter)
        for row, counts in zip(rows, compiled):
            count_lower, mask = minimum_cost(counts, family, weights, order, count_meter)
            combined = max(count_lower, row["lower_scalar_with_ratio"])
            count_meter.pay("count_reprice", "combine_scalar_and_count_lower")
            assert combined <= row["upper_shared_witnesses"]
            row.update(lower_counts=count_lower, lower_scalar_plus_counts=combined,
                       quota_minimizer_mask=mask)
            for price in row["prices"]:
                count_meter.pay("price_profile", "count_action_regret_bound", 2)
                price["count_regret_bound"] = price["retained_action_cost"]-min(combined, price["price"])
        count_time = dict(process_ns=time.process_time_ns()-rc, wall_ns=time.perf_counter_ns()-rw)
        shared = shared_setup.total+meters[0].total
        scalar_extra = meters[1].total+meters[2].total
        incremental = dict(shared_witness=meters[0].total-before[0],
                           scalar=(meters[1].total-before[1])+(meters[2].total-before[2]),
                           full_leaf=meters[3].total-before[3], counts=count_meter.total-before[4])
        result["cases"].append(dict(name=name, weights=weights, rows=rows,
               incremental_repricing_units=incremental,
               cumulative_build_and_reprice_units=dict(scalar=shared+scalar_extra,
                   full_leaf=shared+tree_setup.total+meters[3].total,
                   scalar_plus_counts=shared+tree_setup.total+count_setup.total+scalar_extra+count_meter.total),
               count_profile_positive_rows=sum(r["lower_counts"] > 0 for r in rows),
               strict_over_scalar=sum(r["lower_scalar_plus_counts"] > r["lower_scalar_with_ratio"] for r in rows),
               count_matches_full=sum(r["lower_scalar_plus_counts"] == r["lower_tree"] for r in rows),
               count_above_full=sum(r["lower_scalar_plus_counts"] > r["lower_tree"] for r in rows),
               count_below_full=sum(r["lower_scalar_plus_counts"] < r["lower_tree"] for r in rows),
               ordinary_reprice_time=base_time, count_reprice_time=count_time))
        save()
    result["repricing_invoices"] = {k:m.record() for k,m in zip(("shared_witness","additive","ratio","full_leaf","counts"),(*meters,count_meter))}
    result.update(status="complete", end_utc=datetime.now(timezone.utc).isoformat(),
                  process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-start,
                  checks=dict(old_profiles_reconstructed_exactly=True, old_scalar_full_and_witness_rows_match=True,
                              all_retained_witnesses_satisfy_closed_quotas=True,
                              all_new_lower_bounds_below_shared_feasible_upper=True,
                              no_source_optimum_or_solver_invocation=True))
    save()
    print(json.dumps(dict(status=result["status"], compilation={k:v["total"] for k,v in result["compilation"].items()},
        storage=result["storage_shape"], cases=[{k:c[k] for k in ("name","count_profile_positive_rows","strict_over_scalar","count_matches_full","count_above_full","count_below_full","incremental_repricing_units","cumulative_build_and_reprice_units")} for c in result["cases"]])))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name("reprice_counts_results.json"))
