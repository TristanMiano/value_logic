"""Narrow P3-03 exact-record binding diagnostics; DEVELOPMENT, not authentication.

Contributor: ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction agent.
The forced fingerprint cases are deliberate field substitutions, not SHA-256
collisions. Save inputs/manifest before module import and never overwrite an
earlier attempt. No generic scientific suite is rerun here.
"""
from __future__ import annotations

import argparse
import ast
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parents[2]
SESSION = ROOT / "v3/work_logs/P3_03_2026-10-07_S1"
CORE = ROOT / "v3/checks/03_bounded_logic.py"
WRAPPER = ROOT / "v3/checks/03_task_certificate.py"
BASELINE = SESSION / "development/binding_baseline_ast.json"
ASSERTIONS = 0
TRACES = {}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_new(path, value):
    with Path(path).open("x") as file:
        json.dump(value, file, indent=2, sort_keys=True, ensure_ascii=True)
        file.write("\n")


def check(value, reason):
    global ASSERTIONS
    ASSERTIONS += 1
    if not value:
        raise AssertionError(reason)


def inputs():
    x = ["var", 0]
    query = dict(id="opaque-bit", version="1", kind="opaque", statement="Unresolved Boolean claim.")
    base = dict(scope="p303-binding-development-v1", queries=[query], constraints=[], cell_cap=2,
                losses={"f": dict(unit="cost", version="1", expr=["min", x, ["add", ["rat", "1"], ["scale", "-1", x]]])})
    task = dict(scope=base["scope"], queries=deepcopy(base["queries"]), constraints=[], cell_cap=2,
                actions={"A": dict(unit="cost", version="1", expr=["scale", "10", x]),
                         "B": dict(unit="cost", version="1", expr=["add", ["scale", "10", x], ["rat", "1"]])},
                selected="A", tolerance="0")
    other = deepcopy(task)
    other["actions"]["B"]["version"] = "2"
    other["actions"]["B"]["expr"] = ["add", ["scale", "10", x], ["rat", "2"]]
    selected = deepcopy(task); selected["selected"] = "B"
    return dict(schema="value_logic.P3-03.binding.inputs.v1", stage="DEVELOPMENT",
                core=base, task=task, other_task=other, other_selection=selected,
                source_premises=[dict(id="h", kind="conditional_assumption", depends_on=[], expr=x),
                                 dict(id="h", kind="conditional_assumption", depends_on=[], expr=["not", x])],
                loss_variants=[dict(unit="cost", version="2", expr=["rat", "0"]),
                               dict(unit="cost", version="2", expr=["rat", "1"])],
                audit_fields=["input_sha256", "active_source_sha256", "loss_sha256", "cover_sha256"],
                substitutions="Force audit fields equal while full records differ; splice a current core report into another task's output; alter only numeric bounds.",
                interpretation="Synthetic identity diagnostics, not cryptographic collision discovery, numeric proof verification or JSON authentication.")


def equalize_audits(report, reference, names):
    result = deepcopy(report)
    for name in names:
        result[name] = reference[name]
    return result


def source_divergence(core, wrapper, data):
    left, right = core.Kernel(deepcopy(data["core"])), core.Kernel(deepcopy(data["core"]))
    left.add_assumption(deepcopy(data["source_premises"][0]))
    right.add_assumption(deepcopy(data["source_premises"][1]))
    a, b = left.report("f"), right.report("f")
    check(a["source_epoch"] == b["source_epoch"] and a["input_sha256"] == b["input_sha256"], "same original input and epoch counters")
    check(canonical(a["source_record"]) != canonical(b["source_record"]), "actual admitted records differ")
    check(left.report_is_current(a) and right.report_is_current(b), "genuine local warrants accepted")
    check(not left.report_is_current(b) and not right.report_is_current(a), "cross-source current warrant rejected")
    substituted = equalize_audits(b, a, data["audit_fields"])
    check(all(substituted[name] == a[name] for name in data["audit_fields"]), "equal audit fields forced as a surrogate")
    check(not left.report_is_current(substituted), "unequal exact source records defeat matching audit fields")
    TRACES["source-divergence"] = dict(left=a, right=b, substituted=substituted,
                                      genuine_sha_collision=False, substituted_current=False)
    return dict(counter_collision=True, fingerprint_substitution_rejected=True)


def loss_divergence(core, wrapper, data):
    left, right = core.Kernel(deepcopy(data["core"])), core.Kernel(deepcopy(data["core"]))
    left.change_loss("f", deepcopy(data["loss_variants"][0]))
    right.change_loss("f", deepcopy(data["loss_variants"][1]))
    a, b = left.report("f"), right.report("f")
    check(a["objective_epoch"] == b["objective_epoch"], "objective counter collision")
    check(a["source_record"] == b["source_record"] and a["loss_record"] != b["loss_record"], "only exact loss record differs")
    substituted = equalize_audits(b, a, data["audit_fields"])
    check(not left.report_is_current(substituted), "exact loss record defeats substituted fingerprint")
    TRACES["loss-divergence"] = dict(left=a, right=b, substituted=substituted, genuine_sha_collision=False)
    return dict(loss_substitution_rejected=True)


def copies_and_revision(core, wrapper, data):
    kernel = core.Kernel(deepcopy(data["core"]))
    kernel.add_assumption(deepcopy(data["source_premises"][0]))
    old = kernel.report("f")
    source_before, loss_before = canonical(old["source_record"]), canonical(old["loss_record"])
    kernel.withdraw("h")
    check(canonical(old["source_record"]) == source_before, "withdrawal cannot mutate a returned source record")
    check(not kernel.report_is_current(old), "withdrawal rejects old warrant")
    current = kernel.report("f")
    kernel.change_loss("f", deepcopy(data["loss_variants"][1]))
    check(canonical(old["loss_record"]) == loss_before, "objective update cannot mutate returned loss record")
    check(not kernel.report_is_current(current), "new objective rejects old warrant")
    # Editing a caller's returned record also must not mutate the live kernel.
    edited = kernel.report("f")
    edited["source_record"]["queries"][0]["statement"] = "caller edit"
    edited["loss_record"]["expr"] = ["rat", "99"]
    check(kernel.queries[0]["statement"] != "caller edit" and kernel.losses["f"]["expr"] == ["rat", "1"], "report records do not alias live source/objective")

    task = wrapper.TaskCertificate(deepcopy(data["task"]))
    task.run(1, "source")
    certificate = task.certificate()
    task_before = canonical(certificate["task_binding"])
    task.catalogue["B"]["version"] = "modified-live-catalogue"
    check(canonical(certificate["task_binding"]) == task_before, "returned task record is a historical copy")
    check(not task.certificate_is_current(certificate), "mutated live catalogue rejects the prior task binding")
    TRACES["historical-copies"] = dict(old=old, task_certificate=certificate,
                                      source_copy_preserved=True, loss_copy_preserved=True, task_copy_preserved=True)
    return dict(source_loss_task_copies=True, withdrawal_rejected=True, objective_rejected=True)


def refinement_reuse(core, wrapper, data):
    kernel = core.Kernel(deepcopy(data["core"]))
    old = kernel.report("f")
    kernel.run(1, "source")
    new = kernel.report("f")
    check(old["bounds"] == ["0", "1"] and new["bounds"] == ["0", "0"], "existing numerical refinement remains present")
    check(kernel.report_is_current(old), "same source/loss keeps a looser historical warrant")
    check(old["cover_sha256"] != new["cover_sha256"] and old["source_record"] == new["source_record"], "cover change does not replace source semantics")
    task = wrapper.TaskCertificate(deepcopy(data["task"]))
    task.run(1, "source")
    certificate = task.certificate()
    task.run(2, "source")
    check(certificate["certified"] and task.certificate_is_current(certificate), "genuine task certificate survives same-source processing")
    TRACES["refinement-reuse"] = dict(old=old, new=new, task_certificate=certificate)
    return dict(core_and_task_reuse=True)


def task_records(core, wrapper, data):
    current = wrapper.TaskCertificate(deepcopy(data["task"]))
    current.run(1, "source")
    a = current.certificate()
    other = wrapper.TaskCertificate(deepcopy(data["other_task"]))
    other.run(1, "source")
    b = other.certificate()
    check(a["task_binding"] != b["task_binding"], "catalogue versions/expressions are retained in exact task records")
    check(not current.certificate_is_current(b), "different original catalogue rejected")
    substituted = deepcopy(b)
    for name in ["request_sha256", "catalogue_sha256", "compiled_loss_sha256"]:
        substituted[name] = a[name]
    # Deliberately splice a genuine current core binding to isolate the full
    # task-record obligation. This is not a discovered hash collision.
    substituted["core_report"] = deepcopy(a["core_report"])
    check(current.core.report_is_current(substituted["core_report"]), "spliced core binding is genuinely current")
    check(not current.certificate_is_current(substituted), "full unequal task binding still rejects substituted audit/core fields")
    selected = wrapper.TaskCertificate(deepcopy(data["other_selection"]))
    check(not selected.certificate_is_current(a), "other selected action does not inherit the output")
    TRACES["task-records"] = dict(current=a, other=b, substituted=substituted, genuine_sha_collision=False)
    return dict(full_task_required=True, changed_selection_rejected=True)


def non_authentication(core, wrapper, data):
    kernel = core.Kernel(deepcopy(data["core"]))
    kernel.run(1, "source")
    genuine = kernel.report("f")
    altered = deepcopy(genuine)
    altered["bounds"] = ["100", "100"]
    check(kernel.report_is_current(altered), "identity helper deliberately does not verify altered numerical bounds")
    altered_audit = deepcopy(genuine)
    for name in data["audit_fields"]:
        altered_audit[name] = "0" * 64
    check(kernel.report_is_current(altered_audit), "audit fingerprints are not substitutes for full-record equality")
    task = wrapper.TaskCertificate(deepcopy(data["task"]))
    task.run(1, "source")
    cert = task.certificate()
    changed = deepcopy(cert)
    changed["core_report"]["bounds"] = ["100", "100"]
    check(task.certificate_is_current(changed), "task currentness is not authentication or a numeric proof verifier")
    check(cert["core_report"]["bounds"] == ["0", "0"], "genuine task output remains numerically unchanged")
    legacy = deepcopy(genuine)
    legacy.pop("report_version")
    legacy.pop("source_record")
    legacy.pop("loss_record")
    check(not kernel.report_is_current(legacy), "old fingerprint-only interface is not silently accepted as exact records")
    TRACES["non-authentication"] = dict(genuine=genuine, altered=altered, altered_identity_current=True,
                                       task_original=cert, task_altered=changed, task_altered_identity_current=True,
                                       meaning="Only current represented-premise/target identity was checked, not the correctness of altered numbers.")
    return dict(altered_numeric_fields_not_verified=True, audit_only=True, legacy_interface_rejected=True)


def ast_data(path):
    def fingerprint(node):
        return hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    tree = ast.parse(path.read_bytes())
    funcs, nodes = {}, {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs[node.name] = fingerprint(node); nodes[node.name] = node
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    name = node.name + "." + child.name
                    funcs[name] = fingerprint(child); nodes[name] = child
    def prefix(node, name):
        body = []
        for entry in node.body:
            if isinstance(entry, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in entry.targets):
                break
            body.append(entry)
        return fingerprint(ast.Module(body=body, type_ignores=[]))
    fragments = {}
    if path == CORE:
        fragments["Kernel.report.before_result"] = prefix(nodes["Kernel.report"], "result")
    else:
        fragments["TaskCertificate.certificate.before_result"] = prefix(nodes["TaskCertificate.certificate"], "result")
        body = nodes["TaskCertificate.__init__"].body
        first = next(i for i, n in enumerate(body) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "pieces" for t in n.targets))
        last = next(i for i, n in enumerate(body) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Attribute) and t.attr == "core" for t in n.targets))
        fragments["TaskCertificate.__init__.compiler_to_core"] = fingerprint(ast.Module(body=body[first:last + 1], type_ignores=[]))
    return dict(sha256=sha(path), functions=funcs, fragments=fragments)


def ast_delta(core, wrapper, data):
    baseline = json.loads(BASELINE.read_text())
    allowed = {str(CORE.relative_to(ROOT)): {"Kernel.source_identity", "Kernel.report", "Kernel.report_is_current", "Kernel.snapshot"},
               str(WRAPPER.relative_to(ROOT)): {"TaskCertificate.__init__", "TaskCertificate.certificate", "TaskCertificate.certificate_is_current"}}
    result = {}
    for path in [CORE, WRAPPER]:
        name = str(path.relative_to(ROOT))
        old, new = baseline["files"][name], ast_data(path)
        changed = [key for key in old["functions"] if new["functions"].get(key) != old["functions"][key]]
        added = sorted(set(new["functions"]) - set(old["functions"]))
        check(set(changed) <= allowed[name], "no unplanned numerical/VM/refinement function changed")
        unchanged = sorted(set(old["functions"]) - set(changed))
        for fragment, value in old["fragments"].items():
            check(new["fragments"][fragment] == value, "mathematical report/compiler fragment unchanged")
        result[name] = dict(before_sha256=old["sha256"], after_sha256=new["sha256"], changed_functions=changed,
                            added_functions=added, unchanged_functions=unchanged, unchanged_fragments=old["fragments"])
    TRACES["ast-delta"] = result
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error("attempt must be positive")
    out = SESSION / "development" / f"binding_attempt_{args.attempt}"
    out.mkdir(parents=True, exist_ok=False)
    data = inputs()
    save_new(out / "inputs.json", data)
    dependencies = [CORE, WRAPPER, Path(__file__), BASELINE, SESSION / "development/binding_plan.md"]
    start = dict(utc=datetime.now(timezone.utc).isoformat(), monotonic_ns=time.monotonic_ns(), process_ns=time.process_time_ns())
    manifest = dict(schema="value_logic.P3-03.binding.manifest.v1", stage="DEVELOPMENT", attempt=args.attempt,
                    created=start, python=sys.version, platform=platform.platform(),
                    dependencies={str(p.relative_to(ROOT)): sha(p) for p in dependencies},
                    input_sha256=sha(out / "inputs.json"), final_challenge=False, concurrent_research_credit_ns=0,
                    interpretation=data["interpretation"], overwrite_policy="new numbered directory; retain failures")
    save_new(out / "manifest.json", manifest)
    c_spec = importlib.util.spec_from_file_location("binding_core", CORE)
    c = importlib.util.module_from_spec(c_spec); c_spec.loader.exec_module(c)
    w_spec = importlib.util.spec_from_file_location("binding_wrapper", WRAPPER)
    w = importlib.util.module_from_spec(w_spec); w_spec.loader.exec_module(w)
    suites = [("source_records", source_divergence), ("loss_records", loss_divergence),
              ("historical_copies_and_revision", copies_and_revision), ("refinement_reuse", refinement_reuse),
              ("task_records", task_records), ("non_authentication", non_authentication), ("ast_delta", ast_delta)]
    results = []
    for name, run in suites:
        before = ASSERTIONS
        try:
            detail = run(c, w, data)
            results.append(dict(name=name, status="PASS", assertions=ASSERTIONS - before, detail=detail))
        except Exception:
            results.append(dict(name=name, status="FAIL", assertions=ASSERTIONS - before, traceback=traceback.format_exc()))
    end = dict(utc=datetime.now(timezone.utc).isoformat(), monotonic_ns=time.monotonic_ns(), process_ns=time.process_time_ns())
    save_new(out / "traces.json", TRACES)
    summary = dict(schema="value_logic.P3-03.binding.summary.v1", stage="DEVELOPMENT", attempt=args.attempt,
                   status="PASS" if all(r["status"] == "PASS" for r in results) else "FAIL", assertions=ASSERTIONS,
                   suites=results, start=start, end=end, host_elapsed_ns=end["monotonic_ns"] - start["monotonic_ns"],
                   host_process_ns=end["process_ns"] - start["process_ns"], core_sha256=sha(CORE), wrapper_sha256=sha(WRAPPER),
                   evaluator_sha256=sha(__file__), traces_sha256=sha(out / "traces.json"), concurrent_research_credit_ns=0,
                   interpretation="Exact represented-record identity diagnostics; no authentication, numeric proof verification, SHA collision discovery or broad numerical rerun.")
    save_new(out / "summary.json", summary)
    print(json.dumps(dict(directory=str(out), status=summary["status"], assertions=ASSERTIONS,
                         suites=[dict(name=r["name"], status=r["status"]) for r in results]), indent=2))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
