"""Independent finite DEVELOPMENT diagnostics for P3-03; no final challenge.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-07.
The evaluator's complete tables and reference VM are never kernel inputs.
Run with --attempt N; each attempt records its manifest before scientific work.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import platform
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "v3/work_logs/P3_03_2026-10-07_S1/development"
METHOD = ROOT / "v3/checks/03_bounded_logic.py"
ASSERTIONS = 0
TRACES = {}


def encode(x):
    return json.dumps(x, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_new(path, value):
    with path.open("x") as f:
        f.write(encode(value))


def check(condition, label):
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(label)


def boolean(expr, x):
    """Ordinary two-valued reference; no call to the method's partial evaluator."""
    tag = expr[0]
    if tag == "var":
        return bool(x[expr[1]])
    if tag == "bool":
        return bool(expr[1])
    if tag == "not":
        return not boolean(expr[1], x)
    if tag == "and":
        return boolean(expr[1], x) and boolean(expr[2], x)
    if tag == "or":
        return boolean(expr[1], x) or boolean(expr[2], x)
    raise ValueError(tag)


def point_loss(expr, x):
    """Independent exact scalar evaluation, used only on small finite cases."""
    tag = expr[0]
    if tag == "var":
        return F(x[expr[1]])
    if tag == "rat":
        return F(expr[1])
    if tag == "scale":
        return F(expr[1]) * point_loss(expr[2], x)
    left, right = point_loss(expr[1], x), point_loss(expr[2], x)
    if tag == "add":
        return left + right
    if tag == "min":
        return left if left < right else right
    if tag == "max":
        return left if left > right else right
    if tag == "resid":
        d = left - right
        return d if d > 0 else F(0)
    raise ValueError(tag)


def reference_vm(query):
    """Separate direct interpreter, with no method VM state/helpers."""
    registers = deepcopy(query["registers"])
    position = 0
    for tick in range(query["horizon"]):
        op, *args = query["program"][position]
        if op == "HALT":
            return dict(answer=int(args[0] == query["target"]), executed=tick + 1,
                        halted=True, output=args[0])
        if op == "JUMP":
            position = args[0]
        elif op == "INC":
            registers[args[0]] = registers[args[0]] + 1
            position = position + 1
        elif op == "DECJZ":
            r, target = args
            if registers[r]:
                registers[r] = registers[r] - 1
                position = position + 1
            else:
                position = target
        else:
            raise ValueError(op)
    return dict(answer=0, executed=query["horizon"], halted=False, output=None)


def var(i):
    return ["var", i]


def rat(x):
    return ["rat", str(x)]


def negate(x):
    return ["not", x]


def xor(a, b):
    return ["or", ["and", a, negate(b)], ["and", negate(a), b]]


def premise(name, expr, dependencies=None):
    return dict(id=name, expr=expr, kind="conditional_assumption", depends_on=dependencies or [])


def opaque(i):
    return dict(id=f"q{i}", version="1", kind="opaque", statement=f"Unresolved deterministic atom {i}")


def loss(expr, unit="task-cost", version="1"):
    return dict(expr=expr, unit=unit, version=version)


def config(k=1, constraints=None, losses=None, cap=None, queries=None):
    return dict(scope="p303-development-v1", queries=queries or [opaque(i) for i in range(k)],
                constraints=constraints or [], losses=losses or {"f": loss(var(0))},
                cell_cap=(2 ** k if cap is None else cap))


def machine(name, program, horizon, target=1, registers=None):
    return dict(id=name, version="1", kind="bounded_run", program=program,
                registers=registers or [0], horizon=horizon, target=target)


def inputs():
    """Prospectively bound deterministic catalogue; generated before any run."""
    scenarios = []
    for k in [1, 2, 3]:
        x, z = var(0), var(k - 1)
        terms = {
            "atom": x, "negative": ["scale", "-7/3", x],
            "constant": rat("11/5"), "add": ["add", x, z],
            "min": ["min", x, z], "max": ["max", x, z],
            "residual": ["resid", x, z],
            "shared_cancel": ["add", x, ["scale", "-1", x]],
            "shared_min": ["min", x, ["add", rat(1), ["scale", "-1", x]]],
            "nested": ["resid", ["max", ["scale", "-2/3", x], ["add", z, rat("-1/2")]],
                        ["min", x, ["scale", "3/2", z]]],
        }
        families = [[], [premise("true", ["bool", 1])], [premise("false", ["bool", 0])],
                    [premise("x", x)], [premise("nx", negate(x))],
                    [premise("both", ["and", x, negate(x)])]]
        if k >= 2:
            families += [[premise("xor", xor(x, z))], [premise("or", ["or", x, z])]]
        for j, constraints in enumerate(families):
            scenarios.append(dict(name=f"cover-k{k}-source{j}", config=config(k, constraints,
                {name: loss(expr) for name, expr in terms.items()})))
    vm_queries = [
        machine("true-immediate", [["HALT", 1]], 1),
        machine("false-target", [["HALT", 0]], 1),
        machine("zero-horizon", [["HALT", 1]], 0),
        machine("bounded-loop-false", [["JUMP", 0]], 7),
        machine("boundary-before-halt", [["INC", 0], ["HALT", 1]], 1),
        machine("boundary-at-halt", [["INC", 0], ["HALT", 1]], 2),
        machine("countdown-true", [["DECJZ", 0, 2], ["JUMP", 0], ["HALT", 1]], 9, registers=[3]),
        machine("countdown-false", [["DECJZ", 0, 2], ["JUMP", 0], ["HALT", 1]], 7, registers=[3]),
        machine("requested-zero", [["INC", 0], ["HALT", 0]], 2, target=0),
    ]
    return dict(schema="value_logic.P3-03.development.inputs.v1", stage="DEVELOPMENT",
                finite_cover_scenarios=scenarios, vm_queries=vm_queries,
                targeted_checks=["source_identity", "capacity_xor", "withdrawal", "independent_receipts",
                                 "objective_revision", "candidate_corruption", "evidence_capacity_retry",
                                 "conditional_literal", "ordinary_identity", "input_limits", "restart_obstruction"])


def assignments(k):
    return list(itertools.product([0, 1], repeat=k))


def in_cube(x, c):
    return all(b is None or b == a for a, b in zip(x, c))


def exact_source(kernel):
    return [x for x in assignments(kernel.k)
            if all(boolean(h["expr"], x) for h in kernel.constraints.values())]


def inspect_boundary(kernel, previous=None):
    truth = exact_source(kernel)
    cubes = list(kernel.cells.values())
    for x in assignments(kernel.k):
        count = sum(in_cube(x, c) for c in cubes)
        check(count <= 1, "committed cubes remain disjoint")
        if x in truth:
            check(count == 1, "every compatible assignment is still covered")
    row = dict(event_before_reports=kernel.event, source_size=len(truth), cells=len(cubes), reports={})
    for name, term in kernel.losses.items():
        r = kernel.report(name)
        row["reports"][name] = r
        if truth:
            ys = [point_loss(term["expr"], x) for x in truth]
            check(r["status"] == "CONDITIONAL_OUTER_BOUND", "nonempty small source has a bound")
            lo, hi = map(F, r["bounds"])
            check(lo <= min(ys) <= max(ys) <= hi, "interval contains exact finite extrema")
            if r["source_exactly_filtered"]:
                check((lo, hi) == (min(ys), max(ys)), "filtered singletons give exact extrema")
            if r["feasibility"] == "WITNESS":
                check(tuple(r["witness"]) in truth, "reported witness satisfies active source")
            if previous and previous[name]["bounds"]:
                oldlo, oldhi = map(F, previous[name]["bounds"])
                check(oldlo <= lo <= hi <= oldhi, "fixed-source structural refinement is nested")
        else:
            check(r["feasibility"] != "WITNESS", "inconsistent source has no witness")
        if r["status"] == "FINITE_CONFLICT":
            check(not truth and r["bounds"] is None, "conflict is justified and gives no number")
        if r["source_exactly_filtered"]:
            represented = [x for x in assignments(kernel.k) if any(in_cube(x, c) for c in cubes)]
            check(represented == truth, "exact filtering flag has its full source meaning")
    return row


def check_covers(m, catalogue):
    prefixes = 0
    for item in catalogue["finite_cover_scenarios"]:
        kernel = m.Kernel(item["config"])
        rows = [inspect_boundary(kernel)]
        for _ in range(2 ** (kernel.k + 1)):
            if not kernel.agenda:
                break
            outcome = kernel.run(1, "source")
            check(outcome["used_transactions"] == 1, "one source transaction per requested prefix")
            rows.append(inspect_boundary(kernel, rows[-1]["reports"]))
        check(not kernel.agenda, "sufficient small source capacity completes")
        prefixes += len(rows)
        TRACES[item["name"]] = rows
    return dict(scenarios=len(catalogue["finite_cover_scenarios"]), checked_prefixes=prefixes)


def check_partial_evaluator(m, catalogue):
    from collections import Counter
    cubes_checked = 0
    for item in catalogue["finite_cover_scenarios"]:
        cfg = item["config"]
        k = len(cfg["queries"])
        for cube in itertools.product([None, 0, 1], repeat=k):
            completion = [x for x in assignments(k) if in_cube(x, cube)]
            for h in cfg["constraints"]:
                partial = m.tri(h["expr"], cube, Counter())
                if partial is not None:
                    check(all(boolean(h["expr"], x) == bool(partial) for x in completion),
                          "definite partial Boolean answer holds on every completion")
            for term in cfg["losses"].values():
                lower, upper = m.interval(term["expr"], cube, Counter())
                actual = [point_loss(term["expr"], x) for x in completion]
                check(lower <= min(actual) <= max(actual) <= upper, "cell interval sound on all completions")
            cubes_checked += 1
    return dict(cubes_checked=cubes_checked)


def check_vm(m, catalogue):
    for q in catalogue["vm_queries"]:
        kernel = m.Kernel(config(queries=[q]))
        reference = reference_vm(q)
        rounds = 2 * max(1, reference["executed"])
        reports = [kernel.report("f")]
        for i in range(rounds):
            before = kernel.work["kernel_transactions"]
            outcome = kernel.run(1, "evidence")
            check(kernel.work["kernel_transactions"] - before == outcome["used_transactions"] == 1,
                  "bounded evidence transaction accounting")
            r = kernel.report("f")
            reports.append(r)
            if i < rounds - 1:
                check(r["coordinates"][q["id"]]["status"] == "UNRESOLVED", "no hard answer before full replay")
        r = reports[-1]
        expected = "CHECKED_TRUE" if reference["answer"] else "CHECKED_FALSE"
        check(r["coordinates"][q["id"]]["status"] == expected, "checked VM sign matches independent answer")
        check(r["bounds"] == [str(reference["answer"])] * 2, "accepted literal updates next loss report")
        job = kernel.jobs[0]
        for field in ["answer", "executed", "halted", "output"]:
            check(job["candidate"][field] == reference[field], "receipt matches independent reference field")
        check(r["coordinates"][q["id"]]["accepted_event"] >
              r["coordinates"][q["id"]]["produced_event"], "production and acceptance have distinct order")
        TRACES[q["id"]] = reports
    return dict(queries=len(catalogue["vm_queries"]))


def check_source_identity(m):
    a, b = m.Kernel(config()), m.Kernel(config())
    a.add_assumption(premise("left", var(0)))
    b.add_assumption(premise("right", negate(var(0))))
    ra, rb = a.report("f"), b.report("f")
    check(ra["source_epoch"] == rb["source_epoch"], "counter collision witness constructed")
    check(ra["active_source_sha256"] != rb["active_source_sha256"], "actual sources have different bindings")
    check(not a.report_is_current(rb) and not b.report_is_current(ra), "cross-source report rejected")
    check(a.report_is_current(ra), "own bound keeps current warrant")
    a.run(20, "source")
    check(a.report_is_current(ra), "same-source refinement retains earlier conservative warrant")
    later = a.report("f")
    check(later["cover_sha256"] != ra["cover_sha256"], "cover snapshot distinguishes changed computation")
    TRACES["source-identity"] = [ra, rb, later]
    return dict(equal_epoch_collision_rejected=True)


def check_capacity_xor(m):
    x, y = var(0), var(1)
    h = [premise("xor", xor(x, y))]
    losses = {"sum": loss(["add", x, y])}
    kernel = m.Kernel(config(2, h, losses, cap=1))
    initial = kernel.report("sum")
    used = kernel.run(20, "source")
    limited = kernel.report("sum")
    check(used["used_transactions"] == 20, "capacity stops consume allowance")
    check(limited["bounds"] == initial["bounds"] == ["0", "2"], "one cube retains wide XOR enclosure")
    check(kernel.work["peak_cells"] == 1 and len(kernel.cells) == 1, "committed frontier cap preserved")
    check(not limited["source_exactly_filtered"], "capacity does not claim exactness")
    full = m.Kernel(config(2, h, losses))
    full.run(20, "source")
    refined = full.report("sum")
    check(refined["bounds"] == ["1", "1"], "cost can be identified under XOR")
    check(all(c["status"] == "UNRESOLVED" for c in refined["coordinates"].values()),
          "value identification need not resolve either opaque atom")
    truth = exact_source(full)
    check({x[0] for x in truth} == {0, 1} and {x[1] for x in truth} == {0, 1},
          "both truth coordinates really vary across compatible assignments")
    TRACES["capacity-xor"] = [initial, limited, refined]
    return dict(limited_bounds=limited["bounds"], full_bounds=refined["bounds"])


def check_revision(m):
    h = [premise("root", var(0)), premise("dependent", var(1), ["root"])]
    kernel = m.Kernel(config(2, h, {"sum": loss(["add", var(0), var(1)])}))
    kernel.run(20, "source")
    old = kernel.report("sum")
    check(old["bounds"] == ["2", "2"], "premise-restricted source")
    removed = kernel.withdraw("root")
    reopened = kernel.report("sum")
    check(removed == ["dependent", "root"], "transitive dependencies withdrawn")
    check(reopened["bounds"] == ["0", "2"], "withdrawal restores previously pruned cases")
    check(not kernel.report_is_current(old), "withdrawn warrant stale")
    prior_cover = deepcopy(kernel.cells)
    kernel.change_loss("sum", loss(["scale", "-3", ["add", var(0), var(1)]], unit="new-units", version="2"))
    changed = kernel.report("sum")
    check(changed["bounds"] == ["-6", "0"] and changed["unit"] == "new-units", "new loss/unit recomputed")
    check(kernel.cells == prior_cover, "objective change retains source computation")
    check(not kernel.report_is_current(reopened), "old objective binding stale")
    check(old["bounds"] == ["2", "2"], "prior output object remains unchanged")
    TRACES["revision"] = [old, reopened, changed]
    return dict(transitive_withdrawal=True, objective_revision=True)


def check_independent_receipts(m):
    q = machine("signed", [["HALT", 1]], 1)
    kernel = m.Kernel(config(queries=[q], constraints=[premise("assumed", var(0))]))
    initial = kernel.report("f")
    check(initial["bounds"] == ["1", "1"] and initial["coordinates"][q["id"]]["status"] == "UNRESOLVED",
          "conditional narrowing does not claim independently checked truth")
    kernel.run(2, "evidence")
    certified = kernel.report("f")
    kernel.withdraw("assumed")
    retained = kernel.report("f")
    check(retained["coordinates"][q["id"]]["status"] == "CHECKED_TRUE", "independent VM fact survives premise withdrawal")
    rid = retained["coordinates"][q["id"]]["evidence"]
    kernel.withdraw(rid)
    removed = kernel.report("f")
    check(removed["coordinates"][q["id"]]["status"] == "UNRESOLVED" and removed["bounds"] == ["0", "1"],
          "withdrawing checked receipt resets its job and reopens its source")
    kernel.run(2, "evidence")
    check(kernel.report("f")["coordinates"][q["id"]]["status"] == "CHECKED_TRUE", "restarted job can be checked again")
    TRACES["independent-receipts"] = [initial, certified, retained, removed]
    return dict(retention_and_reopening=True)


def check_candidate_corruption(m):
    q = machine("binding", [["INC", 0], ["HALT", 1]], 2)
    attacks = {"answer": 0, "executed": 0, "terminal_sha256": "0" * 64,
               "query_sha256": "1" * 64, "query_id": "other", "vm_version": "other",
               "answer_json_bool": True}
    results = []
    for field, value in attacks.items():
        kernel = m.Kernel(config(queries=[q]))
        kernel.run(2, "evidence")
        check(kernel.jobs[0]["phase"] == "check" and not kernel.known, "produced candidate awaits checking")
        target = "answer" if field == "answer_json_bool" else field
        kernel.jobs[0]["candidate"][target] = value  # Diagnostic fault injection, not an external API.
        kernel.run(3, "evidence")
        r = kernel.report("f")
        check(not kernel.known and r["processes"][q["id"]]["phase"] == "rejected", "corrupt candidate rejected")
        check(r["bounds"] == ["0", "1"], "candidate corruption adds no hard restriction")
        results.append(dict(attack=field, report=r))
    TRACES["candidate-corruption"] = results
    # A receipt for a different target/version/horizon is bound to different input.
    original = m.Kernel(config(queries=[q])); original.run(4, "evidence")
    old = original.report("f")
    for field, value in [("version", "2"), ("target", 0), ("horizon", 1)]:
        otherq = deepcopy(q); otherq[field] = value
        other = m.Kernel(config(queries=[otherq]))
        check(not other.report_is_current(old), "changed query interpretation does not inherit receipt")
    return dict(corruptions=len(attacks), changed_query_cases=3)


def check_evidence_capacity(m):
    q = machine("capacity", [["HALT", 1]], 1)
    hs = [premise(f"h{i}", ["bool", 1]) for i in range(m.LIMITS["constraints"])]
    kernel = m.Kernel(config(queries=[q], constraints=hs))
    kernel.run(2, "evidence")
    blocked = kernel.report("f")
    check(blocked["processes"][q["id"]]["phase"] == "capacity" and not kernel.known,
          "full constraint store blocks receipt admission explicitly")
    kernel.withdraw("h0")
    kernel.run(1, "evidence")
    admitted = kernel.report("f")
    check(admitted["coordinates"][q["id"]]["status"] == "CHECKED_TRUE", "capacity-blocked complete check retries after space is freed")
    TRACES["evidence-capacity"] = [blocked, admitted]
    return dict(retry_after_withdrawal=True)


def check_ordinary_identity(m):
    q = machine("paired", [["INC", 0], ["HALT", 1]], 2)
    cfg = config(queries=[q])
    value, ordinary = m.Kernel(cfg), m.Kernel(deepcopy(cfg))
    commands = [("run", (1, "all")), ("report", ("f",)), ("run", (3, "all")),
                ("report", ("f",)), ("run", (20, "all")), ("report", ("f",)),
                ("change_loss", ("f", loss(["scale", "7", var(0)], "priced-unit", "2"))),
                ("report", ("f",))]
    for method, args in commands:
        left = getattr(value, method)(*deepcopy(args))
        right = getattr(ordinary, method)(*deepcopy(args))
        check(left == right, "ordinary interpretation returns identical output on the same command")
        check(value.snapshot() == ordinary.snapshot(), "ordinary interpretation retains identical state and work")
    TRACES["ordinary-identity"] = dict(commands=[(n, a) for n, a in commands], snapshot=value.snapshot())
    return dict(commands=len(commands), separate_algorithm=False, reconstruction="identity on the same engine")


def check_input_limits(m):
    bad_rationals = ["1e1000000000", "1.5", "1/0", "1/-2", "9" * 21, "18446744073709551616", "nan", "inf"]
    for literal in bad_rationals:
        try:
            m.Kernel(config(losses={"f": loss(rat(literal))}))
        except m.InputError:
            check(True, "bad rational rejected before evaluation")
        else:
            check(False, "bad rational unexpectedly admitted")
    for mutation in [lambda c: c.update(cell_cap=0),
                     lambda c: c["queries"][0].update(version=""),
                     lambda c: c.update(queries=[]),
                     lambda c: c.update(constraints=[premise("cycle", var(0), ["cycle"])]),
                     lambda c: c.update(losses={"f": loss(["product", var(0), var(0)])})]:
        cfg = config(); mutation(cfg)
        try:
            m.Kernel(cfg)
        except (m.InputError, m.ResourceLimit):
            check(True, "inadmissible input has typed refusal")
        else:
            check(False, "inadmissible input accepted")
    kernel = m.Kernel(config())
    before = deepcopy(kernel.cells)
    try:
        kernel.change_loss("f", loss(rat("1e1000000000")))
    except m.InputError:
        check(kernel.cells == before and kernel.losses["f"]["expr"] == var(0), "failed objective update preserves committed state")
    else:
        check(False, "unsafe loss update accepted")
    check(kernel.work["peak_cells"] == 1, "initial storage is counted")
    # Large but admitted literals can overflow the intermediate work cap later.
    expr = rat("18446744073709551615")
    for _ in range(40):
        expr = ["scale", "18446744073709551615", expr]
    large = m.Kernel(config(losses={"f": loss(expr)}))
    cover = deepcopy(large.cells)
    result = large.report("f")
    check(result["status"] == "ARITHMETIC_LIMIT" and result["bounds"] is None,
          "intermediate arithmetic refuses before oversized next operation")
    check(large.cells == cover, "arithmetic refusal preserves source cover")
    TRACES["arithmetic-limit"] = result
    return dict(bad_rationals=len(bad_rationals), input_shape_cases=5, arithmetic_limit=True)


def check_restart(m):
    q = machine("retained", [["INC", 0], ["JUMP", 0]], 5)
    restarted = []
    for _ in range(12):
        fresh = m.Kernel(config(queries=[q]))
        fresh.run(1, "evidence")
        restarted.append(fresh.report("f"))
    check(all(r["coordinates"][q["id"]]["status"] == "UNRESOLVED" for r in restarted),
          "large summed allowances do not help when usable progress is lost")
    retained = m.Kernel(config(queries=[q]))
    for _ in range(10):
        retained.run(1, "evidence")
    final = retained.report("f")
    check(final["coordinates"][q["id"]]["status"] == "CHECKED_FALSE", "retained production and checking work resolves fixed bounded claim")
    TRACES["restart-obstruction"] = dict(restarted=restarted, retained=final)
    return dict(restarted_allowance=12, retained_allowance=10, fresh_restart_resolves=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error("attempt must be positive")
    out = HERE / f"attempt_{args.attempt}"
    out.mkdir(parents=True, exist_ok=False)
    catalogue = inputs()
    save_new(out / "inputs.json", catalogue)
    dependencies = [METHOD, Path(__file__), HERE / "plan.md", ROOT / "v3/derivations/03_logical_uncertainty.md",
                    ROOT / "v3/literature/03_bounded_sources.md"]
    start = dict(utc=datetime.now(timezone.utc).isoformat(), monotonic_ns=time.monotonic_ns(),
                 process_ns=time.process_time_ns())
    manifest = dict(schema="value_logic.P3-03.development.manifest.v1", stage="DEVELOPMENT",
                    attempt=args.attempt, created=start, python=sys.version, platform=platform.platform(),
                    input_sha256=sha(out / "inputs.json"),
                    dependencies={str(p.relative_to(ROOT)): sha(p) for p in dependencies},
                    access="Reference tables/interpreter are evaluator-only; no method oracle access.",
                    final_challenge=False, overwrite_policy="new attempt directory required")
    save_new(out / "manifest.json", manifest)
    spec = importlib.util.spec_from_file_location("bounded_method", METHOD)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    suites = [("cover_prefixes", lambda: check_covers(m, catalogue)),
              ("partial_evaluator", lambda: check_partial_evaluator(m, catalogue)),
              ("bounded_vm", lambda: check_vm(m, catalogue)),
              ("source_identity", lambda: check_source_identity(m)),
              ("capacity_xor", lambda: check_capacity_xor(m)),
              ("revision", lambda: check_revision(m)),
              ("independent_receipts", lambda: check_independent_receipts(m)),
              ("candidate_corruption", lambda: check_candidate_corruption(m)),
              ("evidence_capacity", lambda: check_evidence_capacity(m)),
              ("ordinary_identity", lambda: check_ordinary_identity(m)),
              ("input_limits", lambda: check_input_limits(m)),
              ("restart_obstruction", lambda: check_restart(m))]
    results = []
    for name, run in suites:
        before = ASSERTIONS
        try:
            detail = run()
            results.append(dict(name=name, status="PASS", assertions=ASSERTIONS - before, detail=detail))
        except Exception:
            results.append(dict(name=name, status="FAIL", assertions=ASSERTIONS - before, traceback=traceback.format_exc()))
    end = dict(utc=datetime.now(timezone.utc).isoformat(), monotonic_ns=time.monotonic_ns(),
               process_ns=time.process_time_ns())
    save_new(out / "traces.json", TRACES)
    summary = dict(stage="DEVELOPMENT", attempt=args.attempt, status="PASS" if all(r["status"] == "PASS" for r in results) else "FAIL",
                   suites=results, assertions=ASSERTIONS, start=start, end=end,
                   host_elapsed_ns=end["monotonic_ns"] - start["monotonic_ns"],
                   host_process_ns=end["process_ns"] - start["process_ns"],
                   method_sha256=sha(METHOD), evaluator_sha256=sha(__file__), traces_sha256=sha(out / "traces.json"),
                   interpretation="Finite development diagnostics; no final evidence, rate claim or performance advantage.")
    save_new(out / "summary.json", summary)
    print(encode(dict(directory=str(out), status=summary["status"], assertions=ASSERTIONS,
                      suites=[dict(name=r["name"], status=r["status"]) for r in results])))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
