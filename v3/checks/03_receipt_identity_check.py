"""Narrow checked-receipt identity repair diagnostics; DEVELOPMENT only.

Contributor: ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction agent.
The equal query-digest fields are deliberate substitutions, not SHA collisions.
Save prospective inputs and manifest before core execution; never reuse an
attempt directory. Independent four-world coverage checks use no core evaluator.
"""
from __future__ import annotations

import argparse
import ast
from copy import deepcopy
from datetime import datetime, timezone
import difflib
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
CORE = ROOT / "v3/checks/03_bounded_logic.py"
WRAPPER = ROOT / "v3/checks/03_task_certificate.py"
AREA = ROOT / "v3/work_logs/P3_03_2026-10-07_S1/development/receipt_identity_repair"
BEFORE = AREA / "core_before.py"
EXPECTED_BEFORE = "e8ac9bfda4addd9853a3b7ac174062a1152c8ec25cf6d2d09274d463c7d0419e"
ASSERTIONS = 0
TRACES = {}
DELTA = {}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_new(path, value):
    with Path(path).open("x") as output:
        json.dump(value, output, indent=2, sort_keys=True, ensure_ascii=True)
        output.write("\n")


def check(condition, reason):
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(reason)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inputs():
    first = dict(id="fast-true", version="short-v1", kind="bounded_run",
                 program=[["HALT", 1]], registers=[0], horizon=1, target=1)
    second = dict(id="slow-false", version="delayed-v2", kind="bounded_run",
                  program=[["INC", 0] for _ in range(7)] + [["HALT", 0]],
                  registers=[0], horizon=8, target=1)
    config = dict(scope="p303-receipt-identity-development-v1", queries=[first, second],
                  constraints=[], cell_cap=4,
                  losses={"x0": dict(unit="cost", version="1", expr=["var", 0])})
    task = dict(scope="p303-receipt-wrapper-development-v1", queries=deepcopy(config["queries"]),
                constraints=[], cell_cap=4, selected="A", tolerance="0",
                actions={"A": dict(unit="cost", version="1", expr=["rat", "0"]),
                         "B": dict(unit="cost", version="1", expr=["rat", "1"])})
    return dict(schema="value_logic.P3-03.receipt_identity.inputs.v1", stage="DEVELOPMENT",
                config=config, task=task, expected_answers={"fast-true": 1, "slow-false": 0},
                expected_execution_lengths={"fast-true": 1, "slow-false": 8},
                equal_query_digest="0" * 64, maximum_allowance_one_calls=128,
                post_receipt_source_allowance=16,
                maximum_label_example="vm:11:" + "a" * 64,
                changed_loss=dict(unit="cost", version="2", expr=["rat", "7"]),
                field_surrogate="Only digest calls on the two exact immutable query records return the same 64-character field; all other digest calls remain genuine.",
                interpretation="DEVELOPMENT field-substitution diagnostic, not a discovered SHA-256 collision, cryptographic authentication claim or broad rerun.")


def truth(expr, assignment):
    """Independent ordinary Boolean evaluation; no tri/interval calls."""
    op = expr[0]
    if op == "var":
        return bool(assignment[expr[1]])
    if op == "bool":
        return bool(expr[1])
    if op == "not":
        return not truth(expr[1], assignment)
    if op == "and":
        return truth(expr[1], assignment) and truth(expr[2], assignment)
    if op == "or":
        return truth(expr[1], assignment) or truth(expr[2], assignment)
    raise AssertionError("unexpected diagnostic constraint syntax")


def state(kernel):
    worlds = list(itertools.product((0, 1), repeat=2))
    source = [x for x in worlds if all(truth(h["expr"], x) for h in kernel.constraints.values())]
    cover = [x for x in worlds if any(all(a is None or a == b for a, b in zip(c, x))
                                     for c in kernel.cells.values())]
    return dict(source_epoch=kernel.source_epoch, cover_revision=kernel.cover_revision,
                cells={str(i): list(c) for i, c in kernel.cells.items()}, agenda=list(kernel.agenda),
                constraints=deepcopy(kernel.constraints), known=deepcopy(kernel.known),
                jobs=deepcopy(kernel.jobs), last_event=deepcopy(kernel.last_event),
                current_source=[list(x) for x in source], represented_cover=[list(x) for x in cover],
                missing_current_assignments=[list(x) for x in source if x not in cover])


def run_pair(module, data, trace_name, forced, expect_cover):
    if forced:
        original = module.digest
        query_bytes = {canonical(q) for q in data["config"]["queries"]}

        def field_surrogate(obj):
            return data["equal_query_digest"] if canonical(obj) in query_bytes else original(obj)

        module.digest = field_surrogate
    kernel = module.Kernel(deepcopy(data["config"]))
    trace = [state(kernel)]
    TRACES[trace_name] = dict(forced_equal_query_fields=forced, actual_sha_collision=False,
                             kernel_version=module.KERNEL_VERSION, transactions=trace)
    pruned_between = False
    for _ in range(data["maximum_allowance_one_calls"]):
        result = kernel.run(1)
        check(result["used_transactions"] <= 1, "one-call transaction allowance respected")
        record = state(kernel)
        record["run_result"] = result
        trace.append(record)
        if record["last_event"]["kind"] == "prune" and len(kernel.known) == 1:
            pruned_between = True
        if expect_cover:
            check(not record["missing_current_assignments"], "all assignments of current H remain represented at every transaction")
        if len(kernel.known) == 2:
            break
    check(len(kernel.known) == 2, "both bounded queries complete within the fixed diagnostic limit")
    check(pruned_between, "first checked receipt justified pruning before second acceptance")
    check({name: row["answer"] for name, row in kernel.known.items()} == data["expected_answers"],
          "independently specified true and false answers returned")
    for q, job in zip(kernel.queries, kernel.jobs):
        check(job["vm"]["steps"] == data["expected_execution_lengths"][q["id"]], "replay reaches expected fixed instruction count")
    TRACES[trace_name]["pruning_between_acceptances"] = pruned_between
    return kernel


def baseline_obstruction(data):
    module = load(BEFORE, "receipt_identity_preserved_baseline")
    kernel = run_pair(module, data, "baseline-surrogate", True, False)
    final = state(kernel)
    check(len(kernel.constraints) == 1, "preserved baseline aliases two accepted constraints under one digest key")
    check(final["current_source"] == [[0, 0], [1, 0]], "overwritten source now retains only the negative second literal")
    check(final["missing_current_assignments"] == [[0, 0]], "earlier pruning omits a newly admitted assignment")
    check(kernel.known["fast-true"]["evidence"] == kernel.known["slow-false"]["evidence"], "old checked records share the same aliased key")
    TRACES["baseline-surrogate"]["final_report"] = kernel.report("x0")
    return dict(expected_obstruction_reproduced=True, missing_assignment=[0, 0],
                interpretation="Counterexample to preserved-v1 all-current-source coverage under a deliberately equal digest field.")


def repaired_coexistence_withdrawal(data):
    module = load(CORE, "receipt_identity_repaired_surrogate")
    kernel = run_pair(module, data, "repaired-surrogate", True, True)
    expected_ids = [f"vm:{i}:{data['equal_query_digest']}" for i in range(2)]
    check(set(kernel.constraints) == set(expected_ids), "both indexed receipt constraints coexist despite equal audit suffixes")
    check(kernel.known["fast-true"]["evidence"] == expected_ids[0] and
          kernel.known["slow-false"]["evidence"] == expected_ids[1], "each checked query retains its own indexed evidence reference")
    check(state(kernel)["current_source"] == [[1, 0]], "both active literals give the expected current finite source")
    report = kernel.report("x0")
    frozen = canonical(report["source_record"])
    check(kernel.report_is_current(report), "genuine new-version current report accepted")
    kernel.run(data["post_receipt_source_allowance"], mode="source")
    refined = state(kernel)
    check(not refined["missing_current_assignments"], "post-receipt source refinement preserves coverage")
    check(kernel.report_is_current(report), "same-source refinement preserves current warrant")
    removed = kernel.withdraw(expected_ids[0])
    after = state(kernel)
    check(removed == [expected_ids[0]], "withdrawal closure removes only the independent selected receipt")
    check(set(kernel.constraints) == {expected_ids[1]}, "independent second literal survives withdrawal")
    check(set(kernel.known) == {"slow-false"} and kernel.known["slow-false"]["answer"] == 0,
          "independent negative checked answer survives withdrawal")
    check(kernel.jobs[1]["phase"] == "done" and kernel.jobs[0]["phase"] == "produce",
          "withdrawal restarts only its own producer")
    check(after["current_source"] == [[0, 0], [1, 0]] and not after["missing_current_assignments"],
          "reset covers the widened current source")
    check(not kernel.report_is_current(report), "withdrawal invalidates old report warrant")
    check(canonical(report["source_record"]) == frozen, "returned source record remains historical after withdrawal")
    kernel.run(data["post_receipt_source_allowance"], mode="source")
    complete = state(kernel)
    check(complete["represented_cover"] == complete["current_source"] == [[0, 0], [1, 0]],
          "source-only refinement exactly filters the retained independent literal")
    widened = kernel.report("x0")
    check(widened["bounds"] == ["0", "1"], "first coordinate regains its full conditional range after withdrawal")
    TRACES["repaired-surrogate"].update(report_before_withdrawal=report, refined=refined,
                                      removed=removed, after_withdrawal=after,
                                      final=complete, final_report=widened)
    return dict(distinct_indexed_ids=expected_ids, independent_withdrawal=True,
                all_current_source_assignments_covered=True)


def ordinary_identifiers_and_reports(data):
    module = load(CORE, "receipt_identity_repaired_ordinary")
    kernel = run_pair(module, data, "repaired-ordinary", False, True)
    expected = [f"vm:{i}:{hashlib.sha256(canonical(q)).hexdigest()}" for i, q in enumerate(kernel.queries)]
    check(set(kernel.constraints) == set(expected), "ordinary genuine-digest identifiers use exact catalogue indices")
    check(len({x.rsplit(":", 1)[1] for x in expected}) == 2, "ordinary fixed query digest suffixes differ")
    max_id = data["maximum_label_example"]
    check(len(max_id) == 70 and module.label(max_id) == max_id, "largest admitted index identifier fits withdrawal label cap")
    report = kernel.report("x0")
    check(kernel.report_is_current(report), "ordinary current report accepted")
    substituted = deepcopy(report)
    substituted["source_record"]["queries"][0]["version"] = "different-record"
    check(substituted["active_source_sha256"] == report["active_source_sha256"], "audit field intentionally retained while record differs")
    check(not kernel.report_is_current(substituted), "unchanged exact-record helper rejects substituted source record")
    historical = canonical(report["loss_record"])
    kernel.change_loss("x0", deepcopy(data["changed_loss"]))
    check(not kernel.report_is_current(report), "objective change invalidates old report warrant")
    check(canonical(report["loss_record"]) == historical, "returned loss record remains historical")
    TRACES["repaired-ordinary"].update(expected_receipt_ids=expected, report=report,
                                     substituted_record=substituted, after_objective=kernel.report("x0"))
    return dict(ordinary_ids=expected, maximum_id_length=len(max_id), exact_binding_preserved=True)


def wrapper_compatibility(data):
    wrapper = load(WRAPPER, "receipt_identity_task_wrapper")
    task = wrapper.TaskCertificate(deepcopy(data["task"]))
    before = task.certificate()
    check(before["certified"] and task.certificate_is_current(before), "unchanged wrapper produces a current terminal certificate")
    check(before["core_report"]["kernel_version"] == "finite-cover-v2", "wrapper reports the repaired kernel version")
    task.run(1, mode="source")
    check(task.certificate_is_current(before), "same-source refinement preserves wrapper current warrant")
    task.run(64, mode="evidence")
    current = task.certificate()
    check(not task.certificate_is_current(before), "new checked source invalidates the wrapper's prior warrant")
    check(current["certified"] and task.certificate_is_current(current), "wrapper accepts a fresh certificate over indexed receipts")
    check(len(task.core.constraints) == 2, "unchanged wrapper retains both ordinary accepted receipts")
    TRACES["wrapper-compatibility"] = dict(before=before, after=current)
    return dict(wrapper_version=wrapper.WRAPPER_VERSION, kernel_version=wrapper.CORE.KERNEL_VERSION,
                wrapper_source_unchanged=True)


def function_hashes(tree):
    result = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[node.name] = hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    result[node.name + "." + child.name] = hashlib.sha256(ast.dump(child, include_attributes=False).encode()).hexdigest()
    return result


def exact_code_delta(data):
    global DELTA
    old, new = ast.parse(BEFORE.read_bytes()), ast.parse(CORE.read_bytes())
    old_functions, new_functions = function_hashes(old), function_hashes(new)
    changed = sorted(name for name in old_functions if old_functions[name] != new_functions.get(name))
    check(changed == ["Kernel._job_step"], "only the receipt-admission function changes")
    counts = dict(version=0, receipt=0)
    old_rid = ast.dump(ast.parse('rid = "vm:" + digest(q)').body[0], include_attributes=False)
    new_rid = ast.parse('rid = f"vm:{i}:{digest(q)}"').body[0]

    class ExpectedRepair(ast.NodeTransformer):
        def visit_Assign(self, node):
            if any(isinstance(t, ast.Name) and t.id == "KERNEL_VERSION" for t in node.targets):
                check(isinstance(node.value, ast.Constant) and node.value.value == "finite-cover-v1", "expected old kernel version")
                node.value = ast.Constant(value="finite-cover-v2")
                counts["version"] += 1
                return node
            if ast.dump(node, include_attributes=False) == old_rid:
                counts["receipt"] += 1
                return deepcopy(new_rid)
            return self.generic_visit(node)

    expected = ExpectedRepair().visit(deepcopy(old))
    check(counts == dict(version=1, receipt=1), "exactly the two authorized AST substitutions occur")
    check(ast.dump(expected, include_attributes=False) == ast.dump(new, include_attributes=False),
          "entire AST equals baseline plus only the authorized version and identity changes")
    DELTA = dict(before_sha256=sha(BEFORE), after_sha256=sha(CORE), changed_functions=changed,
                 added_functions=sorted(set(new_functions) - set(old_functions)),
                 removed_functions=sorted(set(old_functions) - set(new_functions)),
                 function_hashes_before=old_functions, function_hashes_after=new_functions,
                 exact_authorized_ast_delta=True, wrapper_sha256=sha(WRAPPER),
                 unchanged_scope="VM, replay checking except the final key expression, numeric interpreter, source-refinement, scheduler, withdrawal/reset, reports and exact current-warrant helper.")
    return dict(changed_functions=changed, exact_authorized_ast_delta=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()
    if args.attempt != 1:
        parser.error("this prospective plan authorizes only fresh attempt 1")
    if sha(BEFORE) != EXPECTED_BEFORE:
        raise RuntimeError("preserved baseline hash differs")
    out = AREA / "attempt_1"
    out.mkdir(exist_ok=False)
    data = inputs()
    save_new(out / "inputs.json", data)
    with (out / "core_after.py").open("xb") as output:
        output.write(CORE.read_bytes())
    with (out / "evaluator.py").open("xb") as output:
        output.write(Path(__file__).read_bytes())
    with (out / "core_delta.diff").open("x") as output:
        output.writelines(difflib.unified_diff(BEFORE.read_text().splitlines(keepends=True),
                                             CORE.read_text().splitlines(keepends=True),
                                             fromfile="preserved-core-v1", tofile="repaired-core-v2"))
    paths = [CORE, WRAPPER, Path(__file__), BEFORE, AREA / "plan.md", AREA / "baseline_manifest.json",
             out / "core_after.py", out / "evaluator.py", out / "core_delta.diff"]
    start = dict(utc=datetime.now(timezone.utc).isoformat(), monotonic_ns=time.monotonic_ns(), process_ns=time.process_time_ns())
    manifest = dict(schema="value_logic.P3-03.receipt_identity.manifest.v1", stage="DEVELOPMENT", attempt=1,
                    created=start, python=sys.version, platform=platform.platform(),
                    files_sha256={str(p.relative_to(ROOT)): sha(p) for p in paths},
                    inputs_sha256=sha(out / "inputs.json"), final_challenge=False,
                    concurrent_research_credit_ns=0, saved_before_module_execution=True,
                    interpretation=data["interpretation"], overwrite_policy="exclusive creation; retain all outcomes")
    save_new(out / "manifest.json", manifest)
    results = []
    suites = [("preserved_baseline_obstruction", baseline_obstruction),
              ("repaired_coexistence_and_withdrawal", repaired_coexistence_withdrawal),
              ("ordinary_identifiers_and_exact_reports", ordinary_identifiers_and_reports),
              ("unchanged_wrapper_compatibility", wrapper_compatibility),
              ("exact_authorized_code_delta", exact_code_delta)]
    for name, run in suites:
        before_count = ASSERTIONS
        try:
            detail = run(data)
            results.append(dict(name=name, status="PASS", assertions=ASSERTIONS - before_count, detail=detail))
        except Exception:
            results.append(dict(name=name, status="FAIL", assertions=ASSERTIONS - before_count, traceback=traceback.format_exc()))
    end = dict(utc=datetime.now(timezone.utc).isoformat(), monotonic_ns=time.monotonic_ns(), process_ns=time.process_time_ns())
    save_new(out / "traces.json", TRACES)
    save_new(out / "code_delta.json", DELTA)
    files_unchanged = all(sha(p) == manifest["files_sha256"][str(p.relative_to(ROOT))] for p in paths)
    summary = dict(schema="value_logic.P3-03.receipt_identity.summary.v1", stage="DEVELOPMENT", attempt=1,
                   status="PASS" if files_unchanged and all(r["status"] == "PASS" for r in results) else "FAIL",
                   assertions=ASSERTIONS, suites=results, files_unchanged_during_attempt=files_unchanged,
                   start=start, end=end, host_elapsed_ns=end["monotonic_ns"] - start["monotonic_ns"],
                   host_process_ns=end["process_ns"] - start["process_ns"], concurrent_research_credit_ns=0,
                   artifact_sha256={p.name: sha(p) for p in out.iterdir() if p.is_file()},
                   interpretation=data["interpretation"])
    save_new(out / "summary.json", summary)
    print(json.dumps(dict(directory=str(out), status=summary["status"], assertions=ASSERTIONS,
                         suites=[dict(name=r["name"], status=r["status"]) for r in results]), indent=2))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
