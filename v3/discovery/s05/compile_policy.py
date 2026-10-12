#!/usr/bin/env python3
"""Source-bound rent-or-compile arithmetic; no solver or new workload exposure.

DEVELOPMENT, ChatGPT (GPT-6 Astra Pro). This is a standard rent-or-buy rule
applied to two exactly equivalent retained-proof evaluators.
"""
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import hashlib
import json
import sys
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schedule(buy, base, deltas):
    if buy < 0 or len(base) != len(deltas) or any(x < 0 for x in base + deltas):
        raise ValueError("Nonnegative paid costs and matched query sequence required")
    rented = 0
    acquired = False
    total = 0
    rows = []
    for j, (common, extra) in enumerate(zip(base, deltas), 1):
        build = 0
        if not acquired and rented + extra >= buy:
            acquired = True
            build = buy
        if acquired:
            total += common + build
            mode = "compile_then_evaluate" if build else "compiled"
        else:
            total += common + extra
            rented += extra
            mode = "raw"
        oracle = sum(base[:j]) + min(buy, sum(deltas[:j]))
        assert total <= 2 * oracle
        rows.append({"query": j, "mode": mode, "compilation_units": build,
                     "cumulative_query_units": total,
                     "offline_two_representation_units": oracle,
                     "ratio": str(Fraction(total, oracle)) if oracle else "1"})
    return rows


def main(destination):
    if destination.exists():
        raise FileExistsError("Preserve earlier development evidence")
    started = time.perf_counter_ns()
    here = Path(__file__).parent
    source = here / "reprice_compact_results.json"
    data = json.loads(source.read_text())
    if sha(here / "reprice_compact.py") != data["implementation_sha256"]:
        raise ValueError("Changed compact evaluator source")
    setup = data["setup_totals"]["raw_tree"]
    buy = data["setup_totals"]["compact_tree_increment_from_existing_raw_profiles"]
    base = [c["incremental_units"]["compact_tree"] for c in data["cases"]]
    deltas = [c["incremental_units"]["raw_tree"] - b
              for c, b in zip(data["cases"], base)]
    rows = schedule(buy, base, deltas)
    for row, case in zip(rows, data["cases"]):
        row["recipe"] = case["name"]
        row["total_with_shared_raw_setup"] = setup + row["cumulative_query_units"]
        row["always_raw_total"] = case["cumulative_units"]["raw_tree"]
        row["compile_at_start_total"] = case["cumulative_units"]["compact_tree"]
    # Boundary examples exercise arbitrary known-before-service increments;
    # these are arithmetic cases, not additional empirical source instances.
    boundaries = [
        {"buy": 5, "base": [1, 1], "deltas": [0, 0]},
        {"buy": 5, "base": [1], "deltas": [5]},
        {"buy": 5, "base": [1, 1], "deltas": [4, 9]},
        {"buy": 0, "base": [1], "deltas": [0]},
    ]
    for case in boundaries:
        case["rows"] = schedule(case["buy"], case["base"], case["deltas"])
    result = {
        "status": "complete", "evidence": "DEVELOPMENT",
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "utc": datetime.now(timezone.utc).isoformat(),
        "implementation_sha256": sha(Path(__file__)),
        "input_result_sha256": sha(source),
        "source": source.name, "new_solver_calls": 0,
        "new_source_diagnostic_calls": 0, "new_empirical_exposure": False,
        "analysis_kind": "Exact arithmetic on previously exposed fixed invoices",
        "shared_raw_setup": setup, "additional_compilation": buy,
        "rows": rows, "boundary_cases": boundaries,
        "analysis_runtime_ns": time.perf_counter_ns() - started,
        "limits": ["Two equivalent evaluators only, not all useful services",
                   "Stable admitted proof archive and fixed setup cost",
                   "Query cost differences known before serving; no free price oracle",
                   "Declared service units, not constant hardware or bit complexity"]}
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"queries": len(rows), "last": rows[-1],
                      "new_solver_calls": 0}))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else
         Path(__file__).with_name("compile_policy_results.json"))
