"""Targeted DEVELOPMENT checks of the P3-03 terminal certificate wrapper.

Contributor: ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction agent.
Write a fresh attempt manifest and full fixed inputs before importing the
wrapper or executing scientific cases. No hidden final challenge or rerun claim.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
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
METHOD = ROOT / "v3/checks/03_task_certificate.py"
CORE = ROOT / "v3/checks/03_bounded_logic.py"
ASSERTIONS = 0
TRACES = {}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_new(path, value):
    with Path(path).open("x") as f:
        json.dump(value, f, sort_keys=True, indent=2, ensure_ascii=True)
        f.write("\n")


def check(value, reason):
    global ASSERTIONS
    ASSERTIONS += 1
    if not value:
        raise AssertionError(reason)


def row(expr, unit="task-cost", version="1"):
    return dict(expr=expr, unit=unit, version=version)


def request(actions, selected="A", tolerance="0", constraints=None):
    return dict(scope="p303-terminal-development-v1", queries=[dict(
        id="opaque-coordinate", version="1", kind="opaque", statement="Unresolved deterministic Boolean claim.")],
        cell_cap=2, constraints=[] if constraints is None else constraints,
        actions=actions, selected=selected, tolerance=tolerance)


def fixed_inputs():
    x = ["var", 0]
    tenx = ["scale", "10", x]
    one_minus_x = ["add", ["rat", "1"], ["scale", "-1", x]]
    common = request({"A": row(tenx), "B": row(["add", tenx, ["rat", "1"]])})
    reverse = deepcopy(common)
    reverse["actions"]["B"] = row(["add", ["rat", "11"], ["scale", "-10", x]])
    ambiguous_a = request({"A": row(x), "B": row(one_minus_x)}, tolerance="1/2")
    ambiguous_b = deepcopy(ambiguous_a); ambiguous_b["selected"] = "B"
    assumed = deepcopy(ambiguous_a); assumed["tolerance"] = "0"
    assumed["constraints"] = [dict(id="x-zero", expr=["not", x], kind="conditional_assumption", depends_on=[])]
    single = request({"A": row(x)})
    conflict = deepcopy(single)
    conflict["constraints"] = [dict(id="x", expr=x, kind="conditional_assumption", depends_on=[]),
                               dict(id="not-x", expr=["not", x], kind="conditional_assumption", depends_on=[])]
    repriced = deepcopy(common)
    repriced["actions"]["A"] = row(["scale", "20", x], version="2")
    wrong_unit = deepcopy(common); wrong_unit["actions"]["B"]["unit"] = "different-unit"
    wrong_selected = deepcopy(common); wrong_selected["selected"] = "missing"
    negative_tolerance = deepcopy(common); negative_tolerance["tolerance"] = "-1"
    big = x
    for _ in range(6):
        big = ["add", deepcopy(big), deepcopy(big)]
    compiled_limit = request({"A": row(big), "B": row(deepcopy(big)), "C": row(deepcopy(big))})
    return dict(schema="value_logic.P3-03.task_certificate.inputs.v1", stage="DEVELOPMENT",
                requests=dict(common=common, reversed=reverse, ambiguous_a=ambiguous_a,
                              ambiguous_b=ambiguous_b, assumed=assumed, single=single,
                              conflict=conflict, repriced=repriced),
                invalid_requests=dict(mixed_unit=wrong_unit, absent_action=wrong_selected,
                                      negative_tolerance=negative_tolerance, compiled_expression_cap=compiled_limit),
                fault_injections=["selected", "catalogue_expression", "catalogue_removal",
                                  "core_action_expression", "compiled_expression"],
                objective_update="A becomes 20x, version 2; original wrapper must reject until reconstructed",
                access="The complete two-assignment reference table is evaluator-only; wrapper receives the original finite request.")


def point(expr, x):
    """Separate scalar evaluator; never calls a method loss helper."""
    op = expr[0]
    if op == "var":
        return Fraction(x[expr[1]])
    if op == "rat":
        return Fraction(expr[1])
    if op == "scale":
        return Fraction(expr[1]) * point(expr[2], x)
    a, b = point(expr[1], x), point(expr[2], x)
    if op == "add":
        return a + b
    if op == "min":
        return a if a < b else b
    if op == "max":
        return a if a > b else b
    if op == "resid":
        return max(Fraction(0), a - b)
    raise ValueError(op)


def exact_regrets(req):
    return [point(req["actions"][req["selected"]]["expr"], x) -
            min(point(row["expr"], x) for row in req["actions"].values())
            for x in [(0,), (1,)]]


def source_step(wrapper):
    before = wrapper.core.work["kernel_transactions"]
    out = wrapper.run(1, "source")
    check(out["used_transactions"] == wrapper.core.work["kernel_transactions"] - before == 1,
          "wrapper guarding does not conceal extra core transactions")


def common_case(m, data):
    req = data["requests"]["common"]
    wrapper = m.TaskCertificate(deepcopy(req))
    before = wrapper.core.work["kernel_transactions"]
    initial = wrapper.certificate()
    check(wrapper.core.work["kernel_transactions"] - before == 1, "one mathematical report transaction")
    check(initial["core_report"]["bounds"] == ["0", "9"] and not initial["certified"], "initial uncancelled regret enclosure")
    source_step(wrapper)
    refined = wrapper.certificate()
    check(refined["certified"] and refined["core_report"]["bounds"] == ["0", "0"], "refinement certifies selected action")
    check(max(exact_regrets(req)) == 0, "independent pointwise regret is zero")
    check(refined["core_report"]["coordinates"]["opaque-coordinate"]["status"] == "UNRESOLVED", "truth remains unresolved")
    a, b = wrapper.core.report("A"), wrapper.core.report("B")
    check(a["bounds"] == ["0", "10"] and b["bounds"] == ["1", "11"], "both individual cost levels remain unknown")
    check(wrapper.certificate_is_current(initial) and wrapper.certificate_is_current(refined), "source refinement preserves earlier warranted bounds")
    cost = wrapper.accounting()
    work = cost["wrapper_boundary_work"]
    check(work["compilation_requests"] == 1 and work["compiled_nodes_validated"] > 0, "compilation work recorded")
    check(work["bytes_hashed"] > 0 and work["comparison_byte_envelope"] > 0 and work["threshold_comparisons"] == 2,
          "hash, guard and threshold work recorded outside core allowance")
    TRACES["common"] = dict(initial=initial, refined=refined, marginal_reports=[a, b], accounting=cost)
    return dict(initial_upper="9", refined_upper="0", truth_resolved=False, individual_losses_resolved=False)


def reversed_case(m, data):
    req = data["requests"]["reversed"]
    wrapper = m.TaskCertificate(deepcopy(req))
    source_step(wrapper)
    cert = wrapper.certificate()
    a, b = wrapper.core.report("A"), wrapper.core.report("B")
    check(a["bounds"] == ["0", "10"] and b["bounds"] == ["1", "11"], "same marginal ranges as shared-cost case")
    check(max(exact_regrets(req)) == 9 and cert["core_report"]["bounds"] == ["0", "9"], "shared-assignment contrast differs")
    check(not cert["certified"], "equal marginal ranges do not warrant zero regret")
    TRACES["reversed"] = dict(certificate=cert, marginal_reports=[a, b])
    return dict(exact_upper="9", zero_certificate=False)


def ambiguous_cases(m, data):
    rows = []
    for name in ["ambiguous_a", "ambiguous_b"]:
        req = data["requests"][name]
        wrapper = m.TaskCertificate(deepcopy(req))
        wrapper.run(3, "source")
        cert = wrapper.certificate()
        check(max(exact_regrets(req)) == 1, "each selected pure action has worst-case regret one")
        check(cert["core_report"]["bounds"] == ["0", "1"] and not cert["certified"], "tolerance below one cannot be certified")
        check(cert["core_report"]["source_exactly_filtered"], "failure persists after exact finite filtering")
        rows.append(cert)
    TRACES["ambiguous"] = rows
    return dict(selected_actions=2, tolerance="1/2", certified=0)


def withdrawal_case(m, data):
    wrapper = m.TaskCertificate(deepcopy(data["requests"]["assumed"]))
    before = wrapper.certificate()
    check(before["certified"] and before["core_report"]["bounds"] == ["0", "0"], "conditional premise supports task certificate")
    check(before["core_report"]["coordinates"]["opaque-coordinate"]["status"] == "UNRESOLVED", "conditional premise is not a checked answer")
    wrapper.withdraw("x-zero")
    check(not wrapper.certificate_is_current(before), "withdrawal invalidates old task warrant")
    wrapper.run(3, "source")
    after = wrapper.certificate()
    check(not after["certified"] and after["core_report"]["bounds"] == ["0", "1"], "recomputed source reopens regret")
    check(before["core_report"]["bounds"] == ["0", "0"], "historical certificate unchanged")
    TRACES["withdrawal"] = [before, after]
    return dict(reopened=True, old_warrant_current=False)


def request_binding_cases(m, data):
    wrapper = m.TaskCertificate(deepcopy(data["requests"]["common"]))
    source_step(wrapper)
    old = wrapper.certificate()
    variants = []
    selected = deepcopy(data["requests"]["common"]); selected["selected"] = "B"
    tolerance = deepcopy(data["requests"]["common"]); tolerance["tolerance"] = "1"
    unit = deepcopy(data["requests"]["common"])
    for row in unit["actions"].values():
        row["unit"] = "another-common-unit"
    for req in [selected, data["requests"]["reversed"], tolerance, unit]:
        other = m.TaskCertificate(deepcopy(req))
        check(not other.certificate_is_current(old), "different original task does not inherit certificate")
        variants.append(dict(request_sha256=other.request_sha256, old_certificate_current=False))
    TRACES["request-binding"] = variants
    return dict(different_tasks_rejected=len(variants))


def mutation_cases(m, data):
    results = []
    for fault in data["fault_injections"]:
        wrapper = m.TaskCertificate(deepcopy(data["requests"]["common"]))
        source_step(wrapper)
        old = wrapper.certificate()
        if fault == "selected":
            wrapper.selected = "B"
        elif fault == "catalogue_expression":
            wrapper.catalogue["B"]["expr"] = ["rat", "0"]
        elif fault == "catalogue_removal":
            del wrapper.catalogue["B"]
        elif fault == "core_action_expression":
            wrapper.core.losses["B"]["expr"] = ["rat", "0"]
        else:
            wrapper.core.losses[m.RESERVED_LOSS]["expr"] = ["rat", "0"]
        before = wrapper.core.work["kernel_transactions"]
        try:
            wrapper.certificate()
        except m.BindingError as error:
            check(True, "mutated meaning rejected before certification")
            reason = str(error)
        else:
            check(False, "mutated task was certified")
        check(wrapper.core.work["kernel_transactions"] == before, "failed wrapper guard performs no new mathematical report")
        check(not wrapper.certificate_is_current(old), "mutation invalidates current task binding")
        results.append(dict(fault=fault, rejected=True, reason=reason))
    TRACES["mutations"] = results
    return dict(rejected=len(results), access="Internal diagnostic fault injection; not a public mutation API.")


def objective_case(m, data):
    wrapper = m.TaskCertificate(deepcopy(data["requests"]["common"]))
    source_step(wrapper)
    old = wrapper.certificate()
    wrapper.core.change_loss("A", deepcopy(data["requests"]["repriced"]["actions"]["A"]))
    check(not wrapper.certificate_is_current(old), "core objective update invalidates compiled task")
    try:
        wrapper.certificate()
    except m.BindingError:
        check(True, "changed objective requires a newly validated wrapper")
    else:
        check(False, "stale compiled objective accepted")
    new = m.TaskCertificate(deepcopy(data["requests"]["repriced"]))
    source_step(new)
    cert = new.certificate()
    check(cert["core_report"]["bounds"] == ["0", "9"] and not cert["certified"], "fresh repriced request computes changed regret")
    check(max(exact_regrets(data["requests"]["repriced"])) == 9, "independent repriced maximum")
    TRACES["objective-update"] = dict(old=old, repriced=cert)
    return dict(stale_rejected=True, repriced_upper="9")


def one_action_and_conflict(m, data):
    wrapper = m.TaskCertificate(deepcopy(data["requests"]["single"]))
    cert = wrapper.certificate()
    check(wrapper.core.losses[m.RESERVED_LOSS]["expr"] == ["rat", "0"], "one action compiles directly to zero")
    check(cert["certified"] and cert["core_report"]["bounds"] == ["0", "0"], "one-action task has zero regret")
    check(max(exact_regrets(data["requests"]["single"])) == 0, "independent one-action identity")
    other = m.TaskCertificate(deepcopy(data["requests"]["conflict"]))
    bad = other.certificate()
    check(bad["status"] == "FINITE_CONFLICT" and not bad["certified"], "conflict never produces even a zero-term certificate")
    TRACES["one-action"] = cert
    TRACES["finite-conflict"] = bad
    return dict(one_action_zero=True, finite_conflict_certified=False)


def admission_cases(m, data):
    results = []
    for name, req in data["invalid_requests"].items():
        try:
            m.TaskCertificate(deepcopy(req))
        except (m.CORE.InputError, m.CORE.ResourceLimit) as error:
            check(True, "invalid comparison request has a typed refusal")
            results.append(dict(case=name, reason=str(error)))
        else:
            check(False, "invalid task request accepted")
    TRACES["admission"] = results
    return dict(typed_refusals=len(results))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error("attempt must be positive")
    out = SESSION / "development" / f"task_certificate_attempt_{args.attempt}"
    out.mkdir(parents=True, exist_ok=False)
    catalogue = fixed_inputs()
    save_new(out / "inputs.json", catalogue)
    dependencies = [METHOD, CORE, Path(__file__), SESSION / "development/task_certificate_plan.md"]
    start = dict(utc=datetime.now(timezone.utc).isoformat(), monotonic_ns=time.monotonic_ns(), process_ns=time.process_time_ns())
    manifest = dict(schema="value_logic.P3-03.task_certificate.manifest.v1", stage="DEVELOPMENT",
                    attempt=args.attempt, created=start, python=sys.version, platform=platform.platform(),
                    dependencies={str(p.relative_to(ROOT)): sha(p) for p in dependencies},
                    input_sha256=sha(out / "inputs.json"),
                    access=catalogue["access"], final_challenge=False,
                    concurrent_research_credit_ns=0, overwrite_policy="fresh numbered directory; preserve every failure")
    save_new(out / "manifest.json", manifest)
    spec = importlib.util.spec_from_file_location("p303_task_wrapper", METHOD)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    suites = [("shared_cost", common_case), ("reversed_dependence", reversed_case),
              ("pure_action_obstruction", ambiguous_cases), ("withdrawal", withdrawal_case),
              ("request_binding", request_binding_cases), ("mutation_guards", mutation_cases),
              ("objective_update", objective_case), ("one_action_and_conflict", one_action_and_conflict),
              ("admission_caps", admission_cases)]
    results = []
    for name, run in suites:
        before = ASSERTIONS
        try:
            detail = run(m, catalogue)
            results.append(dict(name=name, status="PASS", assertions=ASSERTIONS - before, detail=detail))
        except Exception:
            results.append(dict(name=name, status="FAIL", assertions=ASSERTIONS - before, traceback=traceback.format_exc()))
    end = dict(utc=datetime.now(timezone.utc).isoformat(), monotonic_ns=time.monotonic_ns(), process_ns=time.process_time_ns())
    save_new(out / "traces.json", TRACES)
    summary = dict(schema="value_logic.P3-03.task_certificate.summary.v1", stage="DEVELOPMENT",
                   attempt=args.attempt, status="PASS" if all(s["status"] == "PASS" for s in results) else "FAIL",
                   assertions=ASSERTIONS, suites=results, start=start, end=end,
                   host_elapsed_ns=end["monotonic_ns"] - start["monotonic_ns"],
                   host_process_ns=end["process_ns"] - start["process_ns"],
                   method_sha256=sha(METHOD), core_sha256=sha(CORE), evaluator_sha256=sha(__file__),
                   traces_sha256=sha(out / "traces.json"), concurrent_research_credit_ns=0,
                   interpretation="Finite terminal-task development checks; no policy, forecast, counterfactual or performance advantage.")
    save_new(out / "summary.json", summary)
    print(json.dumps(dict(directory=str(out), status=summary["status"], assertions=ASSERTIONS,
                         suites=[dict(name=s["name"], status=s["status"]) for s in results]), indent=2))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
