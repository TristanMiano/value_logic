"""Fixed query trees with sound paid pruning; exposed-cohort DEVELOPMENT.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. Additional witness consequences may
prune a node, but never re-center or replace the original decision tree.
The original v1/v2 source and result bytes are dependencies, not overwritten.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time

import cnf_receipts as R
import threshold_cnf as old
import threshold_cnf_v2 as saturated
import threshold_plan as T


def simple_tree(lo, hi, mode, pair):
    """Original endpoint or midpoint rule on its own retained answers only."""
    if mode == "midpoint_full_threshold":
        if lo == hi:
            return "leaf", (lo,)
        j = (lo+hi-1)//2
    else:
        a, b = pair
        if hi <= a or lo > b:
            return "leaf", (0,)
        if lo > a and hi <= b:
            return "leaf", (1,)
        # Normalize away endpoints already entailed by the original answers.
        j = next(k for k in pair if lo <= k < hi)
    return ("query", j, simple_tree(lo, j, mode, pair),
            simple_tree(j+1, hi, mode, pair))


def admit_tree(tree, meter):
    """Retain an explicit tree and charge its node admission and storage."""
    if tree[0] == "leaf":
        meter.pay("controller", "fixed_leaf_admission", 2+len(tree[1]))
        meter.pay("storage", "fixed_leaf_retention", 2+len(tree[1]))
        return "leaf", tuple(tree[1])
    meter.pay("controller", "fixed_query_node_admission", 5)
    meter.pay("storage", "fixed_query_node_retention", 5)
    return "query", tree[1], admit_tree(tree[2], meter), admit_tree(tree[3], meter)


def walk(service, row, tree, shadow, events, counts, stage, draw,
         provider_cap=R.native.SERVICE_CAP):
    """Return the exact uncompleted subtree on a capped/failed purchase.

    shadow contains only answers at nodes on this original tree. It is not
    replaced by the stronger interval exposed by a saturated witness.
    """
    meter = service.adapter.meter
    while tree[0] == "query":
        j = tree[1]
        before = tuple(shadow)
        actual_before = service.interval(row)
        q = service.adapter.source.query(row, j)
        meter.pay("check", "fixed_node_source_and_entailment", q.key_words+10)
        lo, hi = actual_before
        pruned = j < lo or j >= hi
        bill_before = service.adapter.provider_total
        calls_before = service.adapter.counts["provider_calls"]
        if pruned:
            answer = int(j < lo)
            counts["entailed_tests_pruned"] += 1
        else:
            answer = service.get(row, j, provider_cap)
            counts["service_queries"] += 1
        counts["visited_nodes"] += 1
        if answer is not None:
            if answer:
                shadow[0] = max(shadow[0], j+1)
            else:
                shadow[1] = min(shadow[1], j)
            assert shadow[0] <= shadow[1]
            meter.pay("controller", "fixed_original_branch_update", 10)
        else:
            assert tuple(shadow) == before
            counts["unresolved_nodes_retained"] += 1
        actual_after = service.interval(row)
        assert shadow[0] <= actual_after[0] <= actual_after[1] <= shadow[1]
        meter.pay("storage", "fixed_node_trace_record", 24)
        events.append(dict(row=row, stage=stage, draw=draw, query=j,
                           shadow_before=before, shadow_after=tuple(shadow),
                           actual_before=actual_before, actual_after=actual_after,
                           answer=answer, pruned=pruned,
                           provider_units=service.adapter.provider_total-bill_before,
                           native_calls=service.adapter.counts["provider_calls"]-calls_before))
        if answer is None:
            return tree, False
        tree = tree[3] if answer else tree[2]
    return tree, True


def arm(source, sample, mode, service_class):
    wall, cpu = time.perf_counter_ns(), time.process_time_ns()
    service = service_class(source)
    shadows, pending, plan_cache = {}, {}, {}
    events, stages, active = [], [], []
    counts = Counter()
    planner = dict(calls=0, cache_hits=0, process_ns=0, wall_ns=0,
                   criterion="Original query rule on shadow answers; unit minimax weights target query count only")
    for stage, pair in enumerate(old.SCHEDULE):
        active.append(pair)
        masks = tuple((1 << a) | (1 << b) for a, b in active)
        features = []
        for draw, row in enumerate(sample):
            meter = service.adapter.meter
            meter.pay("controller", "fixed_shadow_and_continuation_lookup", 8)
            if row not in shadows:
                shadows[row] = [0, old.LEVELS]
                meter.pay("storage", "fixed_shadow_initialized", 4)
            shadow = shadows[row]
            key = mode, tuple(active), *shadow
            if (stage, row) in pending:
                tree = pending[stage, row]
            else:
                meter.pay("controller", "fixed_plan_cache_lookup", 8)
                if key not in plan_cache:
                    pw, pc = time.perf_counter_ns(), time.process_time_ns()
                    if mode == "minimax_query_count":
                        _, raw = T.plan([1]*old.LEVELS, masks, mode="minimax", interval=shadow)
                    else:
                        raw = simple_tree(*shadow, mode, pair)
                    plan_cache[key] = admit_tree(raw, meter)
                    planner["process_ns"] += time.process_time_ns()-pc
                    planner["wall_ns"] += time.perf_counter_ns()-pw
                    planner["calls"] += 1
                else:
                    planner["cache_hits"] += 1
                tree = plan_cache[key]
            rest, complete = walk(service, row, tree, shadow, events, counts, stage, draw)
            if complete:
                pending.pop((stage, row), None)
            else:
                pending[stage, row] = rest
                meter.pay("storage", "fixed_unresolved_continuation_retained", 5)
            features.append(service.feature(row, pair))
        cdf = old.bands(service, sample)
        intervals = [service.interval(row) for row in sample]
        stages.append(dict(stage=stage, pair=pair, feature_values=features,
                           draw_intervals=intervals,
                           mean_interval_width=str(Fraction(sum(hi-lo for lo, hi in intervals), len(sample))),
                           cdf_band=cdf, invoice=service.adapter.snapshot(),
                           pruning=dict(counts), planner=dict(planner)))
    final_intervals = {str(row): service.interval(row) for row in sorted(set(sample))}
    return dict(mode=mode, stages=stages, final=service.adapter.snapshot(),
                final_intervals=final_intervals, shadow_intervals=shadows,
                interval_counts=dict(service.counts), pruning=dict(counts),
                planner=planner, node_events=events, interval_events=service.events,
                acquisition_events=service.adapter.events,
                unresolved_continuations=[dict(stage=stage, row=row, tree=tree)
                                           for (stage, row), tree in pending.items()],
                process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-wall)


def native_trace(a):
    return [(e["row"], e["vertex"], e["answer"], e["witness"], e["provider_units"])
            for e in a["acquisition_events"] if e["provider_units"]]


def abstract_screen():
    """Check tree semantics and paid-subsequence property on every threshold.

    Every tighter, sound initial interval is tried. This is a bounded semantic
    screen; the separate induction covers adaptive receipt arrival as well.
    No source labels or real CNF price assumptions are used here.
    """
    rollouts = 0
    for mode in old.MODES:
        active = []
        for pair in old.SCHEDULE:
            active.append(pair)
            masks = tuple((1 << a) | (1 << b) for a, b in active)
            if mode == "minimax_query_count":
                _, tree = T.plan([1]*old.LEVELS, masks, interval=(0, old.LEVELS))
            else:
                tree = simple_tree(0, old.LEVELS, mode, pair)
            prices = tuple(1+(j*17)%23 for j in range(old.LEVELS))
            for h in range(old.LEVELS+1):
                original_work, output, original_trace = T.execute(tree, h, prices)
                if mode == "midpoint_full_threshold":
                    expected = (h,)
                elif mode == "endpoint_bank":
                    expected = (int(pair[0] < h <= pair[1]),)
                else:
                    expected = T.signature(h, masks)
                assert output == expected
                for lo in range(h+1):
                    for hi in range(h, old.LEVELS+1):
                        node, paid, visited, work = tree, [], [], 0
                        l, u = lo, hi
                        while node[0] == "query":
                            j = node[1]
                            answer = int(h > j)
                            visited.append((j, "SAT" if answer else "UNSAT"))
                            if not (j < l or j >= u):
                                paid.append(j)
                                work += prices[j]
                            if answer:
                                l = max(l, j+1)
                            else:
                                u = min(u, j)
                            node = node[3] if answer else node[2]
                        assert visited == original_trace
                        assert tuple(node[1]) == expected and work <= original_work
                        assert paid == [j for j, _ in original_trace if j in paid]
                        rollouts += 1
    return dict(rollouts=rollouts, all_fixed_paths_and_outputs_match=True,
                all_stateless_nonnegative_price_bills_nonincreasing=True,
                scope="Finite implementation screen on original trees; proof, not enumeration, covers arbitrary sound adaptive pruning")


def capped_smoke(source):
    service = saturated.SaturatedThresholdService(source)
    shadow, events, counts = [0, old.LEVELS], [], Counter()
    tree = simple_tree(0, old.LEVELS, "midpoint_full_threshold", (3, 4))
    rest, complete = walk(service, 0, tree, shadow, events, counts, 0, 0, provider_cap=32)
    assert not complete and rest == tree and shadow == [0, old.LEVELS]
    assert service.interval(0) == (0, old.LEVELS)
    assert events[-1]["answer"] is None and events[-1]["provider_units"] > 0
    return dict(unresolved_preserves_tree_and_shadow=True, events=events,
                invoice=service.adapter.snapshot())


def main(out):
    if out.exists():
        raise FileExistsError("Preserve previous fixed-tree exposure")
    root = R.EXPERIMENTS.parent.parent
    prior_paths = [Path(__file__).with_name(name) for name in
                   ("threshold_cnf_results.json", "threshold_cnf_v2_results.json")]
    v1, v2 = [json.loads(p.read_text()) for p in prior_paths]
    source, sample = old.cohort(), v1["sample_with_replacement"]
    assert source.identity == v1["source_identity"] == v2["source_identity"]
    files = {Path(__file__)} | {root/p for p in v2["sources"]}
    result = dict(status="running", evidence="DEVELOPMENT",
                  contributor="ChatGPT (GPT-6 Astra Pro)", python=sys.version,
                  start_utc=datetime.now(timezone.utc).isoformat(), command=sys.argv,
                  source_identity=source.identity, sample_with_replacement=sample,
                  previous_results={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in prior_paths},
                  sources={str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
                  scope="Exposed-cohort replay, no new sampling. Freeze each original query tree using only its own shadow answers; sound witness consequences may prune but never re-center it. Both ordinary and saturated services have the same paid guard, original-tree planner, checked provider and exhaustive proof reuse. Added adapter work is billed; planning arithmetic remains separately timed, with unit minimax weights meaning query count only.",
                  comparisons=[])
    def save():
        out.write_text(json.dumps(result, separators=(",", ":"))+"\n")
    save()
    result["abstract_screen"] = abstract_screen()
    result["capped_smoke"] = capped_smoke(source)
    save()
    for mode in old.MODES:
        ordinary = arm(source, sample, mode, old.ThresholdService)
        enhanced = arm(source, sample, mode, saturated.SaturatedThresholdService)
        original = next(a for a in v1["arms"] if a["mode"] == mode)
        recentered = next(a["saturated"] for a in v2["comparisons"] if a["mode"] == mode)
        assert native_trace(ordinary) == native_trace(original) == native_trace(enhanced)
        path = lambda a: [(e["stage"], e["draw"], e["row"], e["query"], e["answer"])
                          for e in a["node_events"]]
        assert path(ordinary) == path(enhanced)
        reference = [s["feature_values"] for s in original["stages"]]
        assert [s["feature_values"] for s in ordinary["stages"]] == reference
        assert [s["feature_values"] for s in enhanced["stages"]] == reference
        assert all(value in (0, 1) for stage in reference for value in stage)
        assert not ordinary["unresolved_continuations"] and not enhanced["unresolved_continuations"]
        result["comparisons"].append(dict(mode=mode, ordinary=ordinary, saturated=enhanced,
                                          native_purchase_traces_equal=True,
                                          original_tree_paths_equal=True,
                                          original_feature_answers_equal=True,
                                          previous_recentered_provider_units=recentered["final"]["provider_units"]))
        save()
        print(json.dumps(dict(mode=mode, arms=[dict(service=label,
              provider_units=a["final"]["provider_units"], total_units=a["final"]["total_units"],
              provider_calls=a["final"]["counts"].get("provider_calls", 0), pruning=a["pruning"],
              widths=[s["mean_interval_width"] for s in a["stages"]], process_ms=a["process_ns"]/1e6)
              for label, a in (("ordinary", ordinary), ("saturated", enhanced))])), flush=True)
    result.update(status="complete", end_utc=datetime.now(timezone.utc).isoformat())
    save()


if __name__ == "__main__":
    main(Path(sys.argv[1]))
