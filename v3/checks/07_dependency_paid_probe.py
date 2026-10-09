"""P3-07 deterministic paid dependency/repair diagnostic; DEVELOPMENT ONLY.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
Agent work is unmeasured, with zero principal Research90 credit.

This executes the existing P3-05 compiler and P3-04 repair Search on one fixed
four-bit supplied model.  It is separate from the modular cold-episode policy
comparison.  Heterogeneous counters are retained and scalarized only by the
explicit posted tariffs below.  Old code does not provide a full CPU or total
memory hard cap, and this diagnostic does not retrofit one by counting pops.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import replace
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import platform
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
VERSION = "p307-dependency-paid-diagnostic-v2"
SPEC = importlib.util.spec_from_file_location("p307_paid_dependency_frontend",
                                             HERE / "05_dependency_frontend.py")
D = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = D
SPEC.loader.exec_module(D)
K = D.K

CHECKPOINTS = (0, 1, 3, 8, 31)
POSTED_FEES = (F(1, 4), F(1, 2), F(1), F(2), F(4))
TARIFF_MULTIPLIERS = (F(1, 10), F(1), F(10))
SOURCE_FILES = (
    "07_dependency_paid_probe.py", "05_dependency_frontend.py", "05_portfolio_transport.py",
    "05_counterfactual_transport.py", "04_counterfactual_repair.py",
)

# Every included counter has a named, predeclared cash price.  These are
# illustrative service-accounting tariffs, not estimated hardware prices.
BASE_TARIFFS = {
    "model_construction": {
        "admitted_table_entries": F(1, 1000),
        "validated_program_nodes": F(1, 1000),
        "compiled_program_nodes": F(1, 1000),
        "compiled_definition_lookups": F(1, 1000),
        "compiled_table_rows": F(1, 1000),
        "compiled_comparisons": F(1, 1000),
    },
    "repair_search": {
        "cells_popped": F(1, 1000),
        "expression_nodes": F(1, 1000),
        "reports": F(1, 1000),
        "seed_checks": F(1, 1000),
    },
    "independent_check": {
        "assignments": F(1, 1000),
        "raw_expression_nodes": F(1, 1000),
        "table_lookups": F(1, 1000),
        "table_index_bit_updates": F(1, 10000),
        "input_reads": F(1, 10000),
        "definition_reads": F(1, 10000),
        "boolean_binary_operations": F(1, 10000),
        "definition_bindings": F(1, 10000),
        "output_bindings": F(1, 10000),
        "table_records_indexed": F(1, 10000),
        "source_predicates": F(1, 10000),
        "rank_terms": F(1, 10000),
        "difference_evaluations": F(1, 10000),
        "rank_comparisons": F(1, 10000),
        "report_binding_characters_compared": F(1, 100000),
        "reported_witness_checks": F(1, 10000),
        "report_claim_checks": F(1, 10000),
    },
    "retention": {"retained_bytes": F(1, 100000)},
}

OMISSIONS = (
    "The finite program, table contents, baseline, source antecedent, soft weights, and fee schedule are supplied model input; semantic model design/acquisition is not measured.",
    "The inherited compiler's counters do not count every validation, record reconstruction, canonicalization, substitution, comparison, or Fraction operation.",
    "The inherited Search's counters do not count complete request.record binding reconstruction, all Python control, object allocation, arithmetic bit work, or total memory.",
    "One frontier pop is heterogeneous work; the four-bit bound of 31 pops is not a CPU, storage, or total response budget.",
    "Independent enumeration is charged under its displayed counters; it is run only after the search reports are frozen and never feeds answers back into the search.",
    "Host imports, immutable source snapshots, manifest writing, diagnostic rendering, and the separate source-binding corruption probe are audit work outside the scalarized service cost.",
    "Retained byte lengths cover the displayed source/comparison/frame/final-report records, not Python heap size, physical RAM use, or all serialized audit evidence.",
    "Counter tariffs are posted illustrative prices. One local elapsed-time observation per stage is reported only for reproducibility, with no population runtime claim.",
)


def encoded(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, (tuple, list)):
        return [encoded(x) for x in value]
    if isinstance(value, dict):
        return {str(k): encoded(v) for k, v in value.items()}
    return value


def canonical(value):
    return json.dumps(encoded(value), sort_keys=True, separators=(",", ":")).encode()


def write_json(path, value):
    with path.open("x") as stream:
        stream.write(json.dumps(encoded(value), sort_keys=True, indent=2) + "\n")


def source_programs():
    definitions = (
        ("left", ("and", ("input", 0), ("input", 1))),
        ("right", ("and", ("input", 2), ("input", 3))),
    )
    output = (("alarm", ("call", "fuse", (("ref", "left"), ("ref", "right")))),)
    old = D.Program("p307-supplied-source-v1", ("a", "b", "c", "d"),
                    (D.Table("fuse", 2, (0, 0, 1, 1)),), definitions, output)
    new = replace(old, scope="p307-supplied-source-v2",
                  tables=(D.Table("fuse", 2, (0, 1, 1, 1)),))
    return old, new


def plan():
    return dict(version=VERSION, classification="DEVELOPMENT_DETERMINISTIC_DIAGNOSTIC",
                supplied_model={"inputs": ["a", "b", "c", "d"],
                    "old_alarm": "a AND b", "new_alarm": "(a AND b) OR (c AND d)",
                    "hypothetical_source": "a=1 AND new_alarm=1", "baseline": [0, 0, 0, 0],
                    "preservation_weights": [1, 2, 1, 1],
                    "reported_loss": "new_alarm - old_alarm"},
                actual_calls=["P3-05 compile_program(new)", "P3-05 compile_comparison",
                              "P3-04 Search.advance/report", "independent raw-program enumeration"],
                cumulative_pop_checkpoints=CHECKPOINTS, raw_check_assignments=16,
                base_counter_tariffs=BASE_TARIFFS, tariff_multipliers=TARIFF_MULTIPLIERS,
                posted_fees=POSTED_FEES,
                fee_semantics="Known posted payment for a checked complete best-repair report; zero for an incomplete report. This is not a supplied future-benefit distribution.",
                omissions=OMISSIONS, principal_research90_credit_seconds=0)


def evaluate_raw(program, values, counts):
    tables = {table.name: table for table in program.tables}
    counts["table_records_indexed"] += len(program.tables)
    definitions = {}

    def ev(expression):
        counts["raw_expression_nodes"] += 1
        op = expression[0]
        if op == "input":
            counts["input_reads"] += 1
            return values[expression[1]]
        if op == "ref":
            counts["definition_reads"] += 1
            return definitions[expression[1]]
        if op == "and":
            a, b = ev(expression[1]), ev(expression[2])
            counts["boolean_binary_operations"] += 1
            return a & b
        if op == "call":
            table = tables[expression[1]]
            index = 0
            for argument in expression[2]:
                index = 2 * index + ev(argument)
                counts["table_index_bit_updates"] += 1
            counts["table_lookups"] += 1
            return table.values[index]
        raise ValueError("The independent diagnostic interpreter has a fixed small grammar.")

    for name, expression in program.definitions:
        definitions[name] = ev(expression)
        counts["definition_bindings"] += 1
    result = {}
    for name, expression in program.outputs:
        result[name] = ev(expression)
        counts["output_bindings"] += 1
    return result


def report_status(report):
    if (report["feasibility"] == "NONEMPTY" and report["rank_exact"]
            and report["identities_complete"]):
        return "CHECKED_COMPLETE_BEST_REPAIRS"
    if report["rank_exact"]:
        return "EXACT_RANK_REPAIR_IDENTITIES_OPEN"
    return "OUTER_REPORT_RANK_UNRESOLVED"


def independent_check(old, new, comparison, frame, checkpoints):
    counts = Counter()

    def check_claim(condition):
        counts["report_claim_checks"] += 1
        if not condition:
            raise AssertionError("An independently checked report claim failed.")

    rows, best, incumbent = [], [], None
    for values in product((0, 1), repeat=4):
        counts["assignments"] += 1
        old_value = evaluate_raw(old, values, counts)["alarm"]
        new_value = evaluate_raw(new, values, counts)["alarm"]
        counts["source_predicates"] += 2
        source_antecedent, source_output = values[0] == 1, new_value == 1
        feasible = source_antecedent and source_output
        counts["rank_terms"] += 4
        rank = sum(weight * value for weight, value in zip((1, 2, 1, 1), values))
        counts["difference_evaluations"] += 1
        difference = new_value - old_value
        rows.append(dict(values=values, feasible=feasible, rank=rank, difference=difference))
        if feasible:
            counts["rank_comparisons"] += 1
            if incumbent is None or rank < incumbent:
                incumbent, best = rank, [values]
            elif rank == incumbent:
                best.append(values)
    lookup = {row["values"]: row for row in rows}
    exact_values = sorted({lookup[values]["difference"] for values in best})
    hull = [min(exact_values), max(exact_values)]
    expected_request = frame.request.record()
    expected_metadata = json.loads(comparison.record())
    # Exact complete source records bind the checked report; hashes are audit
    # labels rather than a substitute for mathematical request equality.
    check_claim(expected_request["metadata"] == expected_metadata)
    for checkpoint in checkpoints:
        report = checkpoint["report"]
        counts["report_binding_characters_compared"] += len(canonical(expected_request))
        assert canonical(report["request"]) == canonical(expected_request)
        for witness in report["best_witnesses"]:
            counts["reported_witness_checks"] += 1
            row = lookup[tuple(witness)]
            assert row["feasible"] and report["incumbent_rank"] == (F(row["rank"]),)
        outer = report["losses"]["D"]["outer"]
        check_claim(outer is not None and outer[0] <= hull[0] <= hull[1] <= outer[1])
        if report["rank_exact"]:
            check_claim(report["incumbent_rank"] == (F(incumbent),))
        if report["identities_complete"]:
            check_claim(report["best_witnesses"] == sorted(best))
            check_claim(report["losses"]["D"]["image"] == list(map(F, exact_values)))
        else:
            check_claim(report["losses"]["D"]["image"] is None)
    final = checkpoints[-1]["report"]
    check_claim(final["rank_exact"] and final["identities_complete"])
    check_claim(final["losses"]["D"]["hull_exact"])
    check_claim(tuple(final["losses"]["D"]["outer"]) == tuple(map(F, hull)))
    check_claim(best == [(1, 0, 1, 1), (1, 1, 0, 0)] and incumbent == 3)
    return dict(work=dict(counts), exact_rank=incumbent, best_repairs=best,
                exact_difference_image=exact_values, exact_difference_hull=hull,
                all_raw_assignments=rows, passed=True)


def priced(work, tariff):
    if set(work) - set(tariff):
        raise AssertionError("Every included heterogeneous counter needs an explicit price.")
    return sum(F(value) * tariff[key] for key, value in work.items())


def execute():
    old, new = source_programs()
    construction = {}
    started = time.perf_counter_ns()
    compiled_new = D.compile_program(new, construction)
    new_alarm = dict(compiled_new.outputs)["alarm"]
    soft = tuple(K.Soft(name + "-default-zero", K.neg(K.bit(i)), F(weight))
                 for i, (name, weight) in enumerate(zip(old.inputs, (1, 2, 1, 1))))
    comparison = D.Comparison("p307-paid-hypothetical-source-v1", old, new,
        (("alarm", F(1)),), (K.bit(0), new_alarm), soft, "alarm-loss-unit")
    frame = D.compile_comparison(comparison, construction)
    construction_ns = time.perf_counter_ns() - started

    started = time.perf_counter_ns()
    search = K.Search(frame.request)
    checkpoints, last = [], 0
    for target in CHECKPOINTS:
        search.advance(target - last)
        report = search.report()
        checkpoints.append(dict(requested_total_pops=target,
                                actual_total_pops=search.work["cells_popped"],
                                status=report_status(report), report=report))
        last = target
    search_ns = time.perf_counter_ns() - started
    search_work = dict(search.work)
    # Deeply freeze the already issued search reports before any oracle check.
    frozen_reports_sha256 = hashlib.sha256(canonical(checkpoints)).hexdigest()

    started = time.perf_counter_ns()
    checked = independent_check(old, new, comparison, frame, checkpoints)
    checking_ns = time.perf_counter_ns() - started
    assert hashlib.sha256(canonical(checkpoints)).hexdigest() == frozen_reports_sha256

    # A source mutation must require fresh search.  This is separate audit
    # work and never replaces or improves the main diagnostic's search state.
    changed = K.Search(frame.request)
    changed.request = replace(frame.request, scope="p307-different-source-query")
    try:
        changed.advance(1)
    except ValueError as exc:
        binding_probe = dict(status="REJECTED", error=str(exc))
    else:
        raise AssertionError("Changed source was silently accepted by inherited Search.")

    retained_records = dict(old_program=old.record(), new_program=new.record(),
                            comparison=comparison.record(), compiled_frame=frame.record(),
                            final_report=checkpoints[-1]["report"])
    retention = {"retained_bytes": len(canonical(retained_records))}
    work = dict(model_construction=construction, repair_search=search_work,
                independent_check=checked["work"], retention=retention)
    base_costs = {stage: priced(counters, BASE_TARIFFS[stage]) for stage, counters in work.items()}
    complete_base = sum(base_costs.values())
    omitted_base = base_costs["independent_check"] + base_costs["retention"]
    grid = []
    for multiplier in TARIFF_MULTIPLIERS:
        for fee in POSTED_FEES:
            complete_cost, omitted_cost = multiplier * complete_base, multiplier * omitted_base
            grid.append(dict(tariff_multiplier=multiplier, posted_service_fee=fee,
                checker_retention_only_cost=omitted_cost, complete_counted_cost=complete_cost,
                checker_retention_only_net=fee - omitted_cost, complete_counted_net=fee - complete_cost,
                incomplete_accounting_decision="PAY" if fee > omitted_cost else "DO_NOT_PAY",
                complete_counted_decision="PAY" if fee > complete_cost else "DO_NOT_PAY",
                omitted_costs_reverse_decision=omitted_cost < fee <= complete_cost))
    return dict(version=VERSION, classification="DEVELOPMENT_DETERMINISTIC_DIAGNOSTIC",
                status="PASS", model=plan()["supplied_model"],
                comparison_record=comparison.record(), compiled_frame_record=frame.record(),
                compiled_new_supports=compiled_new.supports, checkpoints=checkpoints,
                frozen_search_reports_sha256=frozen_reports_sha256,
                independent_check=checked, source_binding_probe=binding_probe,
                heterogeneous_work=work, base_counter_tariffs=BASE_TARIFFS,
                base_stage_costs=base_costs, tariff_grid=grid,
                reversal_rows=sum(row["omitted_costs_reverse_decision"] for row in grid),
                elapsed_ns=dict(model_construction=construction_ns, repair_search=search_ns,
                                independent_check=checking_ns), omissions=OMISSIONS,
                hard_limit_scope="At most 31 frontier pops for this supplied four-bit tree; no inherited total CPU/memory response bound.",
                principal_research90_credit_seconds=0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    snapshot = args.out / "source_snapshot"
    snapshot.mkdir()
    source_hashes = {}
    for name in SOURCE_FILES:
        raw = (HERE / name).read_bytes()
        (snapshot / name).write_bytes(raw)
        source_hashes[name] = hashlib.sha256(raw).hexdigest()
    write_json(args.out / "prospective_plan.json", plan())
    write_json(args.out / "manifest.json", dict(version=VERSION,
        source_sha256=source_hashes, python=sys.version, platform=platform.platform(),
        command=sys.argv, stage="DEVELOPMENT", principal_research90_credit_seconds=0))
    result = execute()
    write_json(args.out / "results.json", result)
    summary = dict(version=VERSION, status=result["status"],
                   checkpoints=[dict(requested_pops=row["requested_total_pops"],
                                     actual_pops=row["actual_total_pops"], status=row["status"])
                                for row in result["checkpoints"]],
                   best_repairs=result["independent_check"]["best_repairs"],
                   exact_rank=result["independent_check"]["exact_rank"],
                   exact_difference_hull=result["independent_check"]["exact_difference_hull"],
                   base_stage_costs=result["base_stage_costs"], reversal_rows=result["reversal_rows"],
                   tariff_rows=len(result["tariff_grid"]), source_sha256=source_hashes,
                   results_canonical_sha256=hashlib.sha256(canonical(result)).hexdigest(),
                   results_file_sha256=hashlib.sha256((args.out / "results.json").read_bytes()).hexdigest())
    write_json(args.out / "summary.json", summary)
    print(json.dumps(encoded(summary), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
