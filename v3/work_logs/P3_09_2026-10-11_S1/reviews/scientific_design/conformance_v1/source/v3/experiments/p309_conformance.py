#!/usr/bin/env python3
"""P3-09 preparation adapter for explicitly labelled legacy conformance.

No scientific input is materialized on import, default_config(), groups(), or
units(). generate() first requires the lifecycle's P3-10-EXPOSED marker. The
nine structural inputs are the unchanged, already exposed P3-08 fixtures. The
nine named information definitions below are exact copies of the named tail of
02_finite_information_check.requests(), excluding its combinatorial corpus.
They remain regression/conformance, never unseen transfer evidence.

The outer task record and unchanged inner DEVELOPMENT proof format are distinct.
The structural worker retains its original paid tariff and exact fixture scope;
the information audit has no newly claimed paid economic service. This adapter,
input packaging and independent scoring are external experimental machinery.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
"""
from __future__ import annotations

import ast
from copy import deepcopy
from fractions import Fraction
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
VERSION = "p309-conformance-v1"
ARM = "conformance"
EXPOSURE_TOKEN = "P3-10-EXPOSED"
PUBLIC_SCHEMA = "p309.conformance.public.v1"
RESULT_SCHEMA = "p309.conformance.result.v1"
CALIBRATIONS = ("known", "unknown_offset", "unknown_scale", "unknown_affine")
STRUCTURAL_NAMES = (
    "counterpossible_tied_minima", "external_sources_not_repairs",
    "fixed_falsity_constant_infeasible", "conditioning", "occurrence",
    "actor_replacement", "shared_replacement", "shared_and_copy",
    "shared_copy_and_new_predictor",
)
INFORMATION_NAMES = (
    "one_state_empty", "one_state_duplicate", "one_state_no_target",
    "rational_signed", "brier_anchor", "four_state_basis", "zero_reference",
    "partial_target_offset", "larger_exact",
)
REJECTION_NAMES = (
    "boolean_state_count", "floating_loss", "unshared_scale_contract",
    "restricted_source_field", "wrong_row_width", "realized_score_tag",
)
TARIFF_NOTE = (
    "v3/work_logs/P3_08_2026-10-10_S1/development/structural/"
    "tariff_v4_1_scope_note.md"
)


def _jsonable(value):
    if isinstance(value, Fraction):
        return str(value)
    if type(value) in (tuple, list):
        return [_jsonable(v) for v in value]
    if type(value) is dict:
        if any(type(k) is not str for k in value):
            raise ValueError("String JSON keys required.")
        return {k: _jsonable(v) for k, v in value.items()}
    if value is None or type(value) in (str, int, bool, float):
        return value
    raise ValueError("Unsupported JSON value.")


def _wire(value):
    return json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False)


def _digest(value):
    return hashlib.sha256(_wire(value).encode("ascii")).hexdigest()


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _require_exposure(token):
    _require(type(token) is str and token == EXPOSURE_TOKEN,
             "Final materialization requires exact P3-10-EXPOSED authorization.")


def _load(relative):
    path = ROOT / relative
    tag = hashlib.sha256(str(path).encode()).hexdigest()[:16]
    name = "_p309_conformance_" + path.stem + "_" + tag
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        _require(spec is not None and spec.loader is not None,
                 "Missing frozen conformance dependency.")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            spec.loader.exec_module(module)
        except BaseException:
            sys.modules.pop(name, None)
            raise
    return sys.modules[name]


def source_paths():
    """Complete relative closure, including copied-case provenance/tariff text."""
    return [
        "v3/experiments/p309_conformance.py",
        "v3/experiments/p308_structural.py",
        "v3/checks/04_counterfactual_repair.py",
        "v3/checks/05_counterfactual_transport.py",
        "v3/checks/02_finite_information_audit.py",
        "v3/checks/02_finite_information_verify.py",
        "v3/checks/02_finite_information_check.py",
        TARIFF_NOTE,
    ]


def default_config():
    return {
        "version": VERSION,
        "structural_budget": 50_000_000,
        "structural_fixture_count": 9,
        "information_named_case_count": 9,
        "information_calibrations": list(CALIBRATIONS),
        "information_rejection_controls": list(REJECTION_NAMES),
        "unit_count": 60,
        "evidence_class": "REGRESSION_CONFORMANCE_NOT_TRANSFER",
        "inner_information_format": "P3-02-finite-information-audit/v1:development",
        "structural_tariff_note": TARIFF_NOTE,
        "information_resource_superiority_claim": False,
    }


def validate_config(config):
    _require(type(config) is dict and _wire(config) == _wire(default_config()),
             "Conformance configuration differs from the fixed preparation contract.")
    return True


def groups(config):
    validate_config(config)
    return [
        {"id": "conformance_structural_legacy", "arm": ARM,
         "recipe": {"kind": "legacy_structural", "version": VERSION,
                    "evidence_class": "REGRESSION", "case_names": list(STRUCTURAL_NAMES),
                    "case_count": 9, "unit_count": 18}},
        {"id": "conformance_information", "arm": ARM,
         "recipe": {"kind": "information", "version": VERSION,
                    "evidence_class": "CONFORMANCE", "case_names": list(INFORMATION_NAMES),
                    "calibrations": list(CALIBRATIONS),
                    "rejection_controls": list(REJECTION_NAMES),
                    "case_count": 42, "unit_count": 42}},
    ]


def _bound_group(group, config):
    validate_config(config)
    _require(type(group) is dict, "Group must be a frozen metadata record.")
    for expected in groups(config):
        if _wire(group) == _wire(expected):
            return expected
    raise ValueError("Unrecognized or altered conformance group.")


def units(group, config):
    group = _bound_group(group, config)
    result = []
    if group["recipe"]["kind"] == "legacy_structural":
        for index, name in enumerate(STRUCTURAL_NAMES):
            for method in ("candidate", "ordinary"):
                result.append({
                    "id": group["id"] + "__" + name + "__" + method,
                    "group_id": group["id"], "arm": ARM,
                    "method": "legacy_structural_" + method,
                    "configuration_id": "legacy_structural_" + method,
                    "method_kind": "conformance", "engine": "legacy_structural",
                    "worker_method": method, "case_index": index, "case_name": name,
                    "expected_kind": "complete_reply", "evidence_class": "REGRESSION",
                })
    else:
        index = 0
        for name in INFORMATION_NAMES:
            for mode in CALIBRATIONS:
                result.append({
                    "id": group["id"] + "__" + name + "__" + mode,
                    "group_id": group["id"], "arm": ARM,
                    "method": "information_audit", "configuration_id": "information_" + mode,
                    "method_kind": "conformance", "engine": "information",
                    "case_index": index, "case_name": name, "calibration": mode,
                    "expected_kind": "certificate", "evidence_class": "CONFORMANCE",
                })
                index += 1
        for name in REJECTION_NAMES:
            result.append({
                "id": group["id"] + "__" + name,
                "group_id": group["id"], "arm": ARM,
                "method": "information_audit", "configuration_id": "information_rejection",
                "method_kind": "conformance", "engine": "information",
                "case_index": index, "case_name": name,
                "expected_kind": "input_rejection", "evidence_class": "CONFORMANCE",
            })
            index += 1
    return result


def _information_inputs():
    """Materialization: frozen copied named legacy definitions, no population search."""
    cases = [
        ("one_state_empty", {"n_states": 1, "losses": [], "targets": [[1], [-3]]}),
        ("one_state_duplicate", {"n_states": 1, "losses": [[7], [7]], "targets": [[1]]}),
        ("one_state_no_target", {"n_states": 1, "losses": [], "targets": []}),
        ("rational_signed", {"n_states": 3,
         "losses": [["1/2", "-2/3", "7/5"], ["1/4", 0, "-1/2"]],
         "targets": [["2/7", "-1/5", "3/11"], [4, 4, 4]]}),
        ("brier_anchor", {"n_states": 3,
         "losses": [["2/3", "2/3", "2/3"], [0, 2, 2], [2, 0, 2], [2, 2, 0]]}),
        ("four_state_basis", {"n_states": 4,
         "losses": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]}),
        ("zero_reference", {"n_states": 3, "losses": [[0, 0, 0]], "targets": [[1, 0, 0]]}),
        ("partial_target_offset", {"n_states": 3,
         "losses": [[0, 1, 0], [1, 2, 1], [1, 1, 0]], "targets": [[1, 0, 0]]}),
        ("larger_exact", {"n_states": 8,
         "losses": [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0],
                    [2, 0, 0, 0, 0, 0, 0, 0]],
         "targets": [[0, 0, 1, 0, 0, 0, 0, 0], ["1/3", "-2/5", 0, 0, 0, 0, 0, "7/11"]]}),
    ]
    _require(tuple(name for name, _ in cases) == INFORMATION_NAMES,
             "Copied named information roster differs.")
    rows = []
    for name, request in cases:
        for mode in CALIBRATIONS:
            rows.append({"name": name, "request": {**deepcopy(request), "calibration": mode},
                         "expected_kind": "certificate"})
    base = {"n_states": 3, "losses": [[0, 1, 0]], "targets": [[1, 0, 0]],
            "calibration": "known"}
    invalid = [
        ("boolean_state_count", {**base, "n_states": True},
         "n_states must be a positive integer."),
        ("floating_loss", {**base, "losses": [[0.5, 1, 0]]},
         "Use integers or rational strings; floats and booleans are not exact inputs."),
        ("unshared_scale_contract", {**base, "calibration": "independent_row_scales"},
         "Unsupported calibration contract."),
        ("restricted_source_field", {**base, "source": "restricted"},
         "Unsupported input fields; this tool accepts only its declared full-simplex contract."),
        ("wrong_row_width", {**base, "losses": [[0, 1]]},
         "Every losses row must have n_states entries."),
        ("realized_score_tag", {**base, "observation_kind": "realized_score"},
         "Unsupported input fields; this tool accepts only its declared full-simplex contract."),
    ]
    for name, request, message in invalid:
        rows.append({"name": name, "request": deepcopy(request),
                     "expected_kind": "input_rejection", "expected_error": message})
    return rows


def generate(group, config, *, exposure_token=None):
    _require_exposure(exposure_token)
    group = _bound_group(group, config)
    if group["recipe"]["kind"] == "legacy_structural":
        legacy = _load("v3/experiments/p308_structural.py")
        inputs = legacy.fixtures()
        _require(tuple(item["name"] for item in inputs) == STRUCTURAL_NAMES,
                 "Legacy fixture identities differ from the fixed roster.")
        payload = _jsonable(inputs)
    else:
        payload = _information_inputs()
    return {"schema": PUBLIC_SCHEMA, "stage": EXPOSURE_TOKEN, "arm": ARM,
            "version": VERSION, "group_id": group["id"], "recipe": deepcopy(group["recipe"]),
            "evidence_class": group["recipe"]["evidence_class"], "inputs": payload,
            "scope": "Known regression/conformance definitions; not unseen transfer."}


def _bound_inputs(unit, public_input, config):
    _require(type(public_input) is dict, "Public input must be a sealed JSON record.")
    _require_exposure(public_input.get("stage"))
    validate_config(config)
    _require(public_input.get("schema") == PUBLIC_SCHEMA and public_input.get("version") == VERSION
             and public_input.get("arm") == ARM, "Public conformance schema/version differs.")
    group = next((g for g in groups(config) if g["id"] == public_input.get("group_id")), None)
    _require(group is not None and _wire(group["recipe"]) == _wire(public_input.get("recipe")),
             "Public recipe does not match the frozen group.")
    _require(any(_wire(unit) == _wire(u) for u in units(group, config)),
             "Unit is not an exact member of the frozen group.")
    if unit["engine"] == "legacy_structural":
        legacy = _load("v3/experiments/p308_structural.py")
        native = legacy.fixtures()
        _require(tuple(s["name"] for s in native) == STRUCTURAL_NAMES,
                 "Legacy fixture identities differ.")
        expected = _jsonable(native)
        selected = native[unit["case_index"]]
    else:
        expected = _information_inputs()
        selected = expected[unit["case_index"]]
    _require(_wire(expected) == _wire(public_input.get("inputs")),
             "Public materialization differs from the fixed known definitions.")
    return selected


def run(unit, public_input, config):
    selected = _bound_inputs(unit, public_input, config)
    result = {"schema": RESULT_SCHEMA, "version": VERSION, "stage": "P3-10-PUBLIC",
              "unit_id": unit["id"], "group_id": unit["group_id"], "arm": ARM,
              "configuration_id": unit["configuration_id"], "method": unit["method"],
              "evidence_class": unit["evidence_class"],
              "public_input_sha256": _digest(public_input),
              "case_sha256": _digest(selected)}
    if unit["engine"] == "legacy_structural":
        legacy = _load("v3/experiments/p308_structural.py")
        inner = legacy.run_method(selected, unit["worker_method"], budget=config["structural_budget"])
        result.update(status=inner["output"]["status"], inner_record=inner,
                      inner_provenance="P3-08 DEVELOPMENT worker on its exact published fixtures",
                      resource_scope="STRUCTURAL-VM-v1 worker events and declared bytes; "
                      "authoritative v4.1 scope note applies")
    else:
        audit = _load("v3/checks/02_finite_information_audit.py")
        try:
            certificate = audit.audit(deepcopy(selected["request"]))
        except ValueError as exc:
            result.update(status="INPUT_REJECTED", error_type=type(exc).__name__, error=str(exc))
        else:
            result.update(status="CERTIFICATE", certificate=certificate)
        result.update(inner_provenance="Unchanged P3-02-finite-information-audit/v1 development format",
                      resource_scope="No new paid economic service or physical runtime claim",
                      task_hypotheses="One supplied full-simplex law, exact expected-loss rows, "
                      "and the named shared nuisance convention")
    return _jsonable(result)


def _exact_matrix(rows):
    return [[Fraction(x) if type(x) in (int, str) else
             (_ for _ in ()).throw(ValueError("Exact rational matrix required."))
             for x in row] for row in rows]


def _information_binding(request, certificate):
    n = request["n_states"]
    target = request.get("targets", [[int(i == j) for j in range(n)] for i in range(n)])
    _require(type(certificate.get("n_states")) is int and certificate["n_states"] == n,
             "Information certificate state count differs from the request.")
    _require(certificate.get("calibration") == request.get("calibration", "known"),
             "Information certificate nuisance contract differs from the request.")
    _require(_exact_matrix(certificate["losses"]) == _exact_matrix(request["losses"]),
             "Information certificate loss rows differ from the request.")
    _require(_exact_matrix(certificate["targets"]) == _exact_matrix(target),
             "Information certificate target rows differ from the request.")


def _invoice_check(inner, expected_budget):
    invoice = inner["invoice"]
    _require(invoice["tariff"] == "STRUCTURAL-VM-v1" and invoice["budget"] == expected_budget,
             "Legacy structural tariff/budget differs.")
    values = [v for counts in invoice["by_stage"].values() for v in counts.values()]
    _require(all(type(v) is int and v >= 0 for v in values), "Invalid structural invoice component.")
    _require(type(invoice["total_units"]) is int and sum(values) == invoice["total_units"]
             and invoice["total_units"] <= expected_budget, "Structural invoice does not reconcile.")
    return invoice["total_units"]


def score(unit, result, public_input, config):
    selected = _bound_inputs(unit, public_input, config)
    _require(result.get("schema") == RESULT_SCHEMA and result.get("version") == VERSION
             and result.get("stage") == "P3-10-PUBLIC", "Result schema/stage differs.")
    _require(result.get("unit_id") == unit["id"] and result.get("group_id") == unit["group_id"]
             and result.get("method") == unit["method"]
             and result.get("configuration_id") == unit["configuration_id"], "Result unit binding differs.")
    _require(result.get("public_input_sha256") == _digest(public_input)
             and result.get("case_sha256") == _digest(selected), "Result input binding differs.")
    answer = {"stage": "P3-10-SCORED", "arm": ARM, "unit_id": unit["id"],
              "configuration_id": unit["configuration_id"], "method": unit["method"],
              "evidence_class": unit["evidence_class"], "status": "FAIL",
              "validity_pass": False, "checks": {"outer_binding": 1},
              "counts": {}, "duty_scope": [], "failure_is_interpreted_falsity": False}
    if unit["engine"] == "legacy_structural":
        legacy = _load("v3/experiments/p308_structural.py")
        inner = result["inner_record"]
        cost = _invoice_check(inner, config["structural_budget"])
        _require(inner["method"] == unit["worker_method"] and inner["input_sha256"] == legacy.digest(selected),
                 "Inner structural method/input binding differs.")
        answer.update(cold_units=cost,
                      local_units=cost - inner["invoice"]["by_stage"].get("setup", {}).get("source_admission_bytes", 0),
                      delivered=inner["output"].get("status") == "SUCCESS",
                      tariff=inner["invoice"]["tariff"],
                      duty_scope=["U01", "U02", "V01", "V03", "V04", "M01", "C01", "C02", "C03", "C04", "I01"],
                      resource_scope="Exact nine-fixture worker event/byte tariff; no CPU/heap claim")
        answer["checks"]["invoice_reconciled"] = 1
        if result["status"] == "SUCCESS" and inner["output"].get("status") == "SUCCESS":
            checked = legacy.verify_complete_reply(selected, inner["output"]["sources"])
            expected = legacy.make_terminal(selected, checked)
            equal = legacy.wire(expected) == legacy.wire(inner["output"])
            answer.update(status="PASS" if equal else "FAIL", validity_pass=equal,
                          output_sha256=legacy.digest(inner["output"]),
                          semantic_action_available=inner["output"]["decision"]["useful_action_warrant"])
            answer["checks"].update(complete_local_reconstruction=1, exact_terminal_comparison=1)
            answer["counts"] = {"retained_sources": len(inner["output"]["sources"]),
                                "current_complete_reply": int(equal)}
        else:
            # A valid paid no-answer is preserved, but does not complete the
            # declared complete-reply regression endpoint at this fixed cap.
            failure_valid = (inner["output"] == json.loads(legacy.UNKNOWN_BUDGET_PAYLOAD)
                             and inner["invoice"]["failure_readout_released"] is True
                             and bool(inner["invoice"]["failures"]))
            answer.update(status="NO_COMPLETE_REPLY", output_integrity_pass=failure_valid,
                          required_endpoint_pass=False, semantic_action_available=False)
    else:
        answer.update(cold_units=None, local_units=None, tariff=None,
                      duty_scope=["U01", "U03", "V01", "V02", "I01"],
                      resource_scope="No priced economic comparison")
        if selected["expected_kind"] == "input_rejection":
            passed = (result["status"] == "INPUT_REJECTED" and result.get("error_type") == "ValueError"
                      and result.get("error") == selected["expected_error"])
            answer.update(status="PASS" if passed else "FAIL", validity_pass=passed, delivered=False,
                          hypothesis_rejection=True,
                          rejection_scope="Explicit unsupported/ill-typed input tag; numeric validation "
                          "alone cannot establish the expected-loss or common-nuisance semantics")
            answer["checks"]["expected_input_rejection"] = int(passed)
            answer["counts"]["input_rejections"] = int(passed)
        elif result["status"] == "CERTIFICATE":
            certificate = result["certificate"]
            _information_binding(selected["request"], certificate)
            verifier = _load("v3/checks/02_finite_information_verify.py")
            counts = verifier.verify(certificate)
            answer.update(status="PASS", validity_pass=True, delivered=True,
                          inner_stage=certificate["stage"], full_law_recoverable=certificate["full_law_recoverable"],
                          all_targets_recoverable=certificate["all_targets_recoverable"],
                          minimum_extra_raw_queries=certificate["repair"]["minimum_extra_raw_queries"])
            answer["checks"].update(exact_request_binding=1, independent_certificate_verification=1)
            answer["counts"] = counts
        else:
            answer.update(status="NO_CERTIFICATE", delivered=False, required_endpoint_pass=False)
    return _jsonable(answer)


def selfcheck():
    """Only disjoint DEVELOPMENT toys and source-level barrier checks.

    No final groups, units, materialization function or accepted exposure token
    is called. The input is outside the copied legacy named/binary corpus.
    """
    checks = []
    tree = ast.parse(inspect.getsource(generate))
    first = tree.body[0].body[0]
    _require(isinstance(first, ast.Expr) and isinstance(first.value, ast.Call)
             and isinstance(first.value.func, ast.Name) and first.value.func.id == "_require_exposure",
             "Exposure gate is no longer the first generation operation.")
    checks.append("generation_gate_is_first_operation")
    try:
        _require_exposure("DEVELOPMENT-SELFTEST-NOT-FINAL")
    except ValueError:
        checks.append("unaccepted_exposure_marker_rejected")
    else:
        raise AssertionError("Preparation marker admitted final materialization.")
    toy = {"n_states": 2, "losses": [[17, 19]], "targets": [[2, -5]], "calibration": "known"}
    audit = _load("v3/checks/02_finite_information_audit.py")
    verifier = _load("v3/checks/02_finite_information_verify.py")
    certificate = _jsonable(audit.audit(deepcopy(toy)))
    _information_binding(toy, certificate)
    counts = verifier.verify(json.loads(_wire(certificate)))
    _require(certificate["full_law_recoverable"] is True
             and certificate["all_targets_recoverable"] is True
             and certificate["repair"]["minimum_extra_raw_queries"] == 0,
             "Disjoint development toy recovery failed.")
    checks.append("disjoint_development_exact_certificate_roundtrip")
    tampered = deepcopy(certificate)
    tampered["target_certificates"][0]["constant"] = str(
        Fraction(tampered["target_certificates"][0]["constant"]) + 1)
    try:
        verifier.verify(tampered)
    except verifier.InvalidCertificate:
        checks.append("disjoint_development_tampered_identity_rejected")
    else:
        raise AssertionError("Tampered exact identity was accepted.")
    altered_request = {**toy, "targets": [[2, -4]]}
    try:
        _information_binding(altered_request, certificate)
    except ValueError:
        checks.append("disjoint_development_request_mismatch_rejected")
    else:
        raise AssertionError("A certificate for another requested target was accepted.")
    invalid = {**toy, "losses": [[17, 19.25]]}
    try:
        audit.audit(invalid)
    except ValueError:
        checks.append("disjoint_development_float_input_rejected")
    else:
        raise AssertionError("A nonexact input was admitted.")
    legacy = _load("v3/experiments/p308_structural.py")
    _require(sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 12, 14),
             "Legacy structural tariff requires CPython 3.12.14.")
    try:
        legacy.StructuralMeter(legacy.TERMINAL_RESERVE - 1)
    except ValueError:
        checks.append("legacy_pre_admission_budget_denial_without_fixture")
    else:
        raise AssertionError("Legacy subminimum account was admitted.")
    files = []
    for relative in source_paths():
        data = (ROOT / relative).read_bytes()
        files.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return {"schema": "p309.conformance.selfcheck.v1", "stage": "DEVELOPMENT",
            "status": "PASS", "version": VERSION, "checks": checks,
            "toy": toy, "toy_verifier_counts": counts, "sources": files,
            "final_population_materializations": 0, "final_group_executions": 0,
            "final_seed_reads": 0, "principal_clock_credit_seconds": 0,
            "scope": "Disjoint toy and pre-materialization checks only; not final conformance outcomes."}


if __name__ == "__main__":
    if sys.argv[1:] != ["selfcheck"]:
        raise SystemExit("Only explicit DEVELOPMENT selfcheck is exposed here; use the frozen lifecycle for P3-10.")
    print(json.dumps(selfcheck(), sort_keys=True, indent=2))
