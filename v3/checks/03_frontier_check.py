"""Narrow P3-03 DEVELOPMENT probe; exact prospective frontier cases.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-07.
No method changes, no final challenge and no time credit inferred from runs.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "v3/work_logs/P3_03_2026-10-07_S1/development"
METHOD = ROOT / "v3/checks/03_bounded_logic.py"
TRACES = {}
ASSERTIONS = 0


def encoded(x):
    return (json.dumps(x, sort_keys=True, indent=2) + "\n").encode()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    with path.open("xb") as f:
        f.write(encoded(value))


def check(condition, label):
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(label)


def stamp():
    return dict(utc=datetime.now(timezone.utc).isoformat(),
                monotonic_ns=time.monotonic_ns(), process_ns=time.process_time_ns())


def parity(indices, loss=False):
    if len(indices) == 1:
        return ["var", indices[0]]
    half = len(indices) // 2
    a, b = parity(indices[:half], loss), parity(indices[half:], loss)
    if loss:
        return ["max", ["resid", deepcopy(a), deepcopy(b)], ["resid", b, a]]
    return ["or", ["and", deepcopy(a), ["not", deepcopy(b)]],
                  ["and", ["not", a], b]]


def premise(name, expr):
    return dict(id=name, expr=expr, kind="conditional_assumption", depends_on=[])


def config(k, cap, expr, constraints=()):
    return dict(scope="frontier-development-v1", cell_cap=cap,
                queries=[dict(id=f"q{i}", version="v1", kind="opaque",
                              statement=f"Unresolved assessment coordinate {i}") for i in range(k)],
                constraints=list(constraints),
                losses={"task": dict(expr=expr, unit="cost", version="v1")})


def inputs():
    cases = dict(parity=[], ordering=[], withdrawal=[])
    for k in (2, 3, 6):
        C = 2 ** (k - 1)
        for cap in (C, C + 1):
            cases["parity"].append(dict(k=k, C=C, cap=cap,
                config=config(k, cap, parity(list(range(k)), True),
                              [premise("odd", parity(list(range(k))))])))
    for k in (2, 4, 6):
        for position in (k - 1, 0):
            x = ["var", position]
            loss = ["min", x, ["add", ["rat", "1"], ["scale", "-1", deepcopy(x)]]]
            cases["ordering"].append(dict(k=k, position=position,
                config=config(k, 2 ** k if position else 2, loss)))
    for history in ("A", "B"):
        h1 = ["var", 1] if history == "A" else ["not", parity([0, 1])]
        cases["withdrawal"].append(dict(history=history,
            config=config(2, 4, ["var", 1],
                          [premise("h0", ["var", 0]), premise("h1", h1)])))
    return cases


def source_run(kernel, trace, *, stop_at_zero=False):
    events, counts = [], Counter()
    stalled = 0
    terminal = None
    for _ in range(50_000):
        if not kernel.agenda:
            terminal = "complete"
            break
        used = kernel.run(1, "source")
        event = deepcopy(kernel.last_event)
        counts[event["kind"]] += 1
        events.append(dict(event=event, committed_cells=len(kernel.cells),
                           queued_cells=len(kernel.agenda), cover_revision=kernel.cover_revision))
        check(used["used_transactions"] == 1, "one source transaction")
        check(len(kernel.cells) <= kernel.cell_cap, "committed cell cap")
        if event["kind"] == "capacity_stop":
            stalled += 1
            if stalled >= len(kernel.agenda):
                terminal = "fixed_input_stall"
                break
        else:
            stalled = 0
        if stop_at_zero:
            report = kernel.report("task")
            events[-1]["report"] = report
            if report["bounds"] is not None and report["bounds"][1] == "0":
                terminal = "task_bound_zero"
                break
    check(terminal is not None, "unexpected transaction ceiling is a failure")
    report = kernel.report("task")
    trace.update(events=events, counts=dict(counts), terminal=terminal,
                 final_report=report, final_snapshot=kernel.snapshot())
    return terminal, counts, report


def complete_cells(kernel):
    check(all(None not in c for c in kernel.cells.values()), "all retained cells are singletons")
    return set(kernel.cells.values())


def exercise(core, cases):
    summaries = []
    for case in cases["parity"]:
        k, C, cap = case["k"], case["C"], case["cap"]
        name = f"parity_k{k}_cap{cap}"
        before = ASSERTIONS
        kernel = core.Kernel(case["config"])
        trace = TRACES[name] = dict(initial=kernel.report("task"))
        terminal, counts, report = source_run(kernel, trace)
        check(all(v["status"] == "UNRESOLVED" for v in report["coordinates"].values()),
              "conditional source does not become checked atom truth")
        if cap == C:
            check(terminal == "fixed_input_stall", "minimum representation cap stalls")
            check(len(kernel.cells) == C and all(c.count(None) == 1 for c in kernel.cells.values()),
                  "stall frontier has C one-free-bit cells")
            check(counts["split"] == C - 1 and counts["capacity_stop"] == C,
                  "stall includes one complete unchanged queue cycle")
            check(not report["source_exactly_filtered"], "stall is not completion")
            check(report["bounds"] == ["0", "1"], "stalled parity loss remains enclosed")
        else:
            truth = {x for x in itertools.product((0, 1), repeat=k) if sum(x) % 2 == 1}
            check(terminal == "complete" and report["source_exactly_filtered"], "spare slot completes")
            check(complete_cells(kernel) == truth, "retained source equals independent odd assignments")
            check(report["bounds"] == ["1", "1"], "parity task exact without atom truth")
            check(counts["split"] == 2 * C - 1, "successful split formula")
            check(counts["prune"] + counts["feasible_leaf"] == 2 * C, "singleton visit formula")
            check(counts["capacity_stop"] == C * (C - 1) // 2, "FIFO capacity revisit formula")
            check(sum(counts.values()) == 4 * C - 1 + C * (C - 1) // 2, "source transaction formula")
        summaries.append(dict(name=name, assertions=ASSERTIONS-before, terminal=terminal,
                              source_transactions=sum(counts.values()), counts=dict(counts),
                              bounds=report["bounds"], status="PASS"))
    for case in cases["ordering"]:
        k, pos = case["k"], case["position"]
        name = f"ordering_k{k}_coordinate{pos}"
        before = ASSERTIONS
        kernel = core.Kernel(case["config"])
        trace = TRACES[name] = dict(initial=kernel.report("task"))
        check(trace["initial"]["bounds"] == ["0", "1"], "compositional initial range")
        terminal, counts, report = source_run(kernel, trace, stop_at_zero=True)
        check(terminal == "task_bound_zero" and report["bounds"] == ["0", "0"], "task settles")
        expected = 1 if pos == 0 else 2 ** k - 1
        check(counts["split"] == expected and sum(counts.values()) == expected,
              "exact order-dependent successful split count")
        check(not report["source_exactly_filtered"], "task settles before whole-source completion")
        check(all(v["status"] == "UNRESOLVED" for v in report["coordinates"].values()),
              "all individual query truth statuses remain unresolved")
        summaries.append(dict(name=name, assertions=ASSERTIONS-before, status="PASS",
                              splits=counts["split"], source_exactly_filtered=False))
    old_views = []
    for case in cases["withdrawal"]:
        history = case["history"]
        name = f"withdrawal_{history}"
        before = ASSERTIONS
        kernel = core.Kernel(case["config"])
        trace = TRACES[name] = dict(before={}, after={})
        terminal, _, old_report = source_run(kernel, trace["before"])
        old_source = complete_cells(kernel)
        check(terminal == "complete" and old_source == {(1,1)}, "same exact present source")
        check(old_report["bounds"] == ["1", "1"], "same exact present task")
        old_views.append(dict(source=sorted(old_source), bounds=old_report["bounds"]))
        kernel.withdraw("h0")
        check(not kernel.report_is_current(old_report), "old warrant becomes stale after withdrawal")
        terminal, _, new_report = source_run(kernel, trace["after"])
        expected = {(0,1),(1,1)} if history == "A" else {(0,0),(1,1)}
        check(terminal == "complete" and complete_cells(kernel) == expected, "distinct revised source")
        check(new_report["bounds"] == (["1", "1"] if history == "A" else ["0", "1"]),
              "distinct revised task range")
        summaries.append(dict(name=name, assertions=ASSERTIONS-before, status="PASS",
                              revised_source=sorted(expected), bounds=new_report["bounds"]))
    check(old_views[0] == old_views[1], "the deliberately retained present-source/task views coincide")
    return summaries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt", type=int, required=True)
    parser.add_argument("--part", choices=("all", "ordering_withdrawal"), default="all")
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error("attempt must be positive")
    out = BASE / f"frontier_attempt_{args.attempt}"
    out.mkdir(exist_ok=False)
    cases = inputs()
    if args.part == "ordering_withdrawal":
        cases["parity"] = []
    save(out / "inputs.json", cases)
    start = stamp()
    save(out / "manifest.json", dict(stage="DEVELOPMENT", attempt=args.attempt,
        start=start, part=args.part, python=sys.version, method_sha256=sha(METHOD), evaluator_sha256=sha(__file__),
        inputs_sha256=sha(out / "inputs.json"), plan_sha256=sha(BASE / "frontier_plan.md"),
        ordinary_comparison="Same permitted finite constraints and algebra; no general complexity lower bound.",
        oracle_access="Complete truth/source tables are evaluator-only.", concurrent_research_credit_ns=0))
    status, error, summaries = "PASS", None, []
    try:
        spec = importlib.util.spec_from_file_location("p303_frontier_core", METHOD)
        core = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(core)
        summaries = exercise(core, cases)
    except Exception:
        status, error = "FAIL", traceback.format_exc()
    end = stamp()
    save(out / "traces.json", TRACES)
    summary = dict(stage="DEVELOPMENT", attempt=args.attempt, status=status, error=error,
        assertions=ASSERTIONS, cases=summaries, start=start, end=end,
        host_elapsed_ns=end["monotonic_ns"]-start["monotonic_ns"],
        host_process_ns=end["process_ns"]-start["process_ns"],
        method_sha256=sha(METHOD), evaluator_sha256=sha(__file__),
        inputs_sha256=sha(out / "inputs.json"), traces_sha256=sha(out / "traces.json"),
        concurrent_research_credit_ns=0)
    save(out / "summary.json", summary)
    print(json.dumps(dict(status=status, assertions=ASSERTIONS, cases=len(summaries), output=str(out), error=error)))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
