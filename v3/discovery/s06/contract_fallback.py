#!/usr/bin/env python3
"""Check a complete acquisition fallback using public cost modes only.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. No native/provider calls,
no cost observations, no source-model optimum enumeration. Abstract integer
interval cases check the public recurrence, not any exposed repair optimum.
"""
from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
import json
from pathlib import Path
import time

import contract_guard as guard


def run():
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    here = Path(__file__).resolve().parent
    output = here / "contract_fallback_results.json"
    if output.exists():
        raise FileExistsError("Preserve previous fallback evidence")
    # Only this explicitly public projection enters the construction.
    data = json.loads((here/"joint_source.json").read_text())
    public = {k:data[k] for k in ["possible_cost_modes","cohort_size","schedule","source_identity"]}
    modes = tuple(tuple(v) for v in public["possible_cost_modes"])
    meter = guard.quote.source.Meter()
    m = len(modes[0])
    assert len(set(modes)) == len(modes)
    assert len({(v[0],v[1]) for v in modes}) == len(modes)
    assert all(len({v[j] for v in modes}) < len(modes) for j in range(m))
    meter.pay("cost_tree", "public_mode_validation", len(modes)*(m+3))

    @lru_cache(None)
    def row_tree(choices):
        meter.pay("cost_tree", "new_mode_subset", len(choices)+1)
        if len(choices) == 1:
            return dict(depth=0,mode=choices[0])
        candidates = []
        for j in range(m):
            groups = {}
            for k in choices:
                groups.setdefault(modes[k][j],[]).append(k)
            meter.pay("cost_tree", "coordinate_outcome_partition", len(choices))
            if len(groups) == 1:
                continue
            children = {value:row_tree(tuple(ks)) for value,ks in sorted(groups.items())}
            depth = 1+max(v["depth"] for v in children.values())
            meter.pay("cost_tree", "worst_child_and_candidate", len(children)+3)
            candidates.append(dict(depth=depth,coordinate=j,outcomes=children))
        if not candidates:
            raise ValueError("Identically observed distinct cost modes")
        meter.pay("cost_tree", "minimum_worst_depth", len(candidates))
        return min(candidates,key=lambda v:(v["depth"],v["coordinate"]))

    tree = row_tree(tuple(range(len(modes))))
    assert tree["depth"] == 2 and tree["coordinate"] == 0
    assert tree["outcomes"][1]["depth"] == 0
    assert tree["outcomes"][0]["coordinate"] == tree["outcomes"][2]["coordinate"] == 1
    assert all(d["price"] == 48 and d["tolerance"] == 4 for d in public["schedule"])
    # Abstract bracket states: a feasible SAT receipt may give a better upper;
    # retaining b is its conservative update for the quoted worst case.
    traces = []
    for clipped_optimum in range(49):
        low, upper, steps = 0, 48, []
        while upper-low > 4:
            old_gap = upper-low
            budget = (low+upper)//2
            status = "SAT" if clipped_optimum <= budget else "checked_UNSAT"
            if status == "SAT":
                upper = budget
            else:
                low = budget+1
            assert low <= clipped_optimum <= upper
            assert upper-low <= old_gap//2
            steps.append(dict(budget=budget,status=status,lower=low,upper=upper))
            meter.pay("bracket_check", "abstract_integer_update", 8)
        assert len(steps) <= 4 and upper-low <= 4
        traces.append(dict(abstract_clipped_optimum=clipped_optimum,steps=steps))
    assert max(len(r["steps"]) for r in traces) == 4
    # This applies the bound to public syntax; it does not inspect fixture
    # optimal values or execute its possible worst-case search calls.
    previous = json.loads((here/"contract_results.json").read_text())
    admission = guard.admit()
    maximum_wrapper = max(q["complete_wrapper_units"] for q in previous["public_source_complete_quotes"])
    maximum_calls = 4*len(public["schedule"])
    result = dict(
        version="s06-complete-fallback-v1", evidence="DEVELOPMENT",
        contributor="ChatGPT (GPT-6 Astra Pro)", created_utc=datetime.now(timezone.utc).isoformat(),
        implementation_sha256=guard.quote.sha(__file__),
        prior_quote_result_sha256=guard.quote.sha(here/"contract_results.json"),
        public_cost_projection=public, public_projection_id=guard.quote.source.digest(public),
        public_row_identification_tree=tree, memoized_mode_subsets=row_tree.cache_info().currsize,
        maximum_external_observations=tree["depth"]*public["cohort_size"],
        maximum_complete_calls_per_request=4, maximum_complete_calls=maximum_calls,
        per_call_declared_wrapper_ceiling=maximum_wrapper,
        all_calls_declared_wrapper_ceiling=maximum_calls*maximum_wrapper,
        initial_code_admission=admission, constructive_check_invoice=meter.record(),
        abstract_integer_bracket_traces=traces,
        new_branch_provider_calls=0,new_native_calls=0,new_external_observations=0,
        measured_timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall),
        result="PASS: public full-calibration tree and complete integer-query fallback bounds.",
        separate_costs=["External audit price", "Audit provider and checking/processing", "Controller evaluation", "Controller and proof storage beyond declared wrapper", "Code/source admission", "CPU and wall time", "Host/deadline interruption and unresolved work"],
        scope="A conservative complete fallback contract; not an executed controller, expected-cost policy or relative-efficiency result.",
    )
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:result[k] for k in ["result","maximum_external_observations","maximum_complete_calls","all_calls_declared_wrapper_ceiling","new_branch_provider_calls"]}))


if __name__ == "__main__":
    run()
