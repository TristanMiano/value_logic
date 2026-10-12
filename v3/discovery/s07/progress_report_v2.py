#!/usr/bin/env python3
"""Read saved S07 acquisitions and print source-bound progress measurements.

DEVELOPMENT reporting only. ChatGPT (GPT-6 Astra Pro), 2026-10-12.
This program does not run controllers, query hidden observations, modify input
files, assign a probability, or make a full-cost claim from named-unit totals.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
VERSION = "s07-progress-extraction-v2"
REQUEST_FIELDS = ("request", "row", "price", "tolerance")
INVOICE_COMPONENTS = (
    "controller_and_interface_units", "complete_wrapper_units",
    "native_adapter_units", "native_proof_units", "native_setup_units",
    "audit_provider_software_units",
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def path_label(path):
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def fraction(value):
    return Fraction(str(value))


def planner_initialization(arm):
    """Prefer an actual constructor meter delta when a later run records one."""
    for scope in (arm, arm["invoice"], arm["summary"], arm["planner_stats"]):
        if "planner_initialization_units" in scope:
            return int(scope["planner_initialization_units"]), "explicit constructor meter delta"
    known = {"s07-complete-bundle-v1", "s07-complete-bundle-v2"}
    units = sum(
        item["units"] for item in arm["invoice"]["breakdown"]["operations"]
        if item["category"] == "bundle_quote"
        and item["operation"] == "source_length_and_complete_call_quote"
    )
    if arm["policy"] != "bundle":
        return 0, "no bundle planner constructed"
    if arm["version"] in known:
        return units, "known v1/v2 constructor's separately metered complete-call quotations"
    raise ValueError("New planner version needs an explicit constructor meter delta")


def extract_arm(run, arm, source_path, source_sha):
    requests, events, plans = arm["requests"], arm["events"], arm["plans"]
    invoice, summary = arm["invoice"], arm["summary"]
    counts = Counter(event["kind"] for event in events)
    checked = sum(
        request["status"] == "checked_action"
        and fraction(request["answer"]["bound"]) <= fraction(request["tolerance"])
        for request in requests
    )
    cache = sum(bool(request["closed_from_cache"]) for request in requests)
    completed = [plan for plan in plans if plan["plan"] is not None]
    completed_requests = sorted({plan["request"] for plan in completed})
    closed_requests = {request["request"] for request in requests
                       if request["status"] == "checked_action"}
    if not set(completed_requests) <= closed_requests:
        raise ValueError("A recorded completed plan has no checked final request")
    derived = dict(requests=len(requests), checked=checked, cache_hits=cache,
                   cost_observations=counts["audit"], complete_calls=counts["complete"],
                   native_attempts=counts["native"],
                   logical_purchases=counts["complete"]+counts["native"],
                   unresolved=len(requests)-checked,
                   executed_complete_bundles=len(completed),
                   quoted_unclosed_states=len(plans)-len(completed))
    for key, value in derived.items():
        if summary[key] != value:
            raise ValueError(f"Reported/derived {key} mismatch in {source_path}:{arm['policy']}")
    operations = sum(invoice[key] for key in INVOICE_COMPONENTS)
    if operations != invoice["operation_units"]:
        raise ValueError("Named invoice component sum mismatch")
    meter = invoice["breakdown"]
    if sum(item["units"] for item in meter["operations"]) != meter["total"]:
        raise ValueError("Detailed operation tariff mismatch")
    if meter["total"] != invoice["controller_and_interface_units"]:
        raise ValueError("Controller meter mismatch")
    quote_calls = sum(plan["quote_units"] for plan in plans)
    if any(type(plan["quote_units"]) is not int or plan["quote_units"] < 0
           for plan in plans):
        raise ValueError("Quotation meter deltas must be nonnegative integers")
    quote_init, quote_init_basis = planner_initialization(arm)
    quote_total = quote_calls + quote_init
    if quote_total > invoice["controller_and_interface_units"]:
        raise ValueError("Planner attribution exceeds enclosing controller meter")
    request_signature = digest(canonical([
        {key: request[key] for key in REQUEST_FIELDS} for request in requests
    ]))
    source_scope = dict(source_identity=run["source_identity"],
                        source_sha256=run["source_sha256"],
                        request_signature_sha256=request_signature,
                        initial_admission_hashes=run["initial_admission"]["hashes"])
    storage = arm["storage"]
    recorded_bytes = sum(storage[key] for key in ("profile_bytes", "planner_cache_bytes"))
    recorded_bytes += storage["cost_support"]["serialized_bytes"]
    quotation_payload = storage.get("quotation_payload")
    payload_byte_components = None if quotation_payload is None else {
        key:value for key,value in quotation_payload.items() if key.endswith("_bytes")
    }
    payload_bytes = None if payload_byte_components is None else sum(payload_byte_components.values())
    common_units = run["common_current_units"]
    history_units = run["historical_acquisition_units"]
    admission_cpu = sum(run[key]["timing"]["process_ns"]
                        for key in ("initial_admission", "complete_code_admission"))
    admission_wall = sum(run[key]["timing"]["wall_ns"]
                         for key in ("initial_admission", "complete_code_admission"))
    return dict(
        measurement_status="new actual acquisitions in the source run; this extraction is read-only",
        source=dict(path=path_label(source_path), sha256=source_sha,
                    selector=f"arms[policy={arm['policy']}]",
                    started_utc=run["start_utc"], completed_utc=run["end_utc"]),
        version=arm["version"], policy=arm["policy"],
        implementation_sha256=run["implementation_sha256"],
        dependency_hashes=run["dependencies"], scope_id=digest(canonical(source_scope)),
        scope_binding=source_scope, configuration=run["configuration"],
        counts=derived, checked_coverage_percent=100*checked/len(requests),
        complete_plan_requests=completed_requests,
        complete_plan_request_coverage=dict(numerator=len(completed_requests),
            denominator=len(requests)-cache,
            meaning="Requests closed after executing a complete quoted plan / requests needing new work"),
        complete_plan_root_kinds=dict(Counter(plan["plan"]["kind"] for plan in completed)),
        quotation=dict(call_meter_delta_units=quote_calls,
            initialization_units=quote_init, initialization_basis=quote_init_basis,
            total_units=quote_total, arm_named_units_share_percent=100*quote_total/operations,
            meaning="Full per-plan meter deltas across all categories plus separately metered planner setup; included in the enclosing invoice, never added to it again",
            selectors=["sum(plans[].quote_units)", "planner constructor meter delta or known v1/v2 initialization operation"]),
        resources=dict(arm_named_units=operations, common_current_named_units=common_units,
            historical_acquisition_named_units=history_units,
            standalone_current_named_units=operations+common_units,
            full_horizon_named_units=operations+common_units+history_units,
            external_audits=counts["audit"], arm_process_ns=arm["timing"]["process_ns"],
            arm_wall_ns=arm["timing"]["wall_ns"],
            recorded_current_process_ns=arm["timing"]["process_ns"]+admission_cpu,
            recorded_current_wall_ns=arm["timing"]["wall_ns"]+admission_wall,
            recorded_retained_bytes=recorded_bytes,
            recorded_common_storage_scope="profile_bytes + planner_cache_bytes + cost_support.serialized_bytes",
            additional_quotation_payload_byte_components=payload_byte_components,
            additional_quotation_payload_bytes=payload_bytes,
            all_reported_serialized_payload_bytes=None if payload_bytes is None else recorded_bytes+payload_bytes,
            quotation_payload_record=quotation_payload,
            missing_payload_policy="An absent older quotation_payload record is unmeasured, not zero. Cross-version common-component comparisons keep the missing payload in explicit symbolic terms.",
            retained_bytes_components=storage,
            storage_limit="Serialized profile/planner/support records only; not complete live/native memory, archive storage or byte-time",
            time_limit="Recorded current admission and arm intervals only; excludes unmeasured source I/O, historical CPU and unitemized host work"),
        invoice_components={key:invoice[key] for key in INVOICE_COMPONENTS},
        demonstrated_ten_percent_full_cost_regions=dict(value=0,
            status="none established by these development invoices",
            meaning="Count of warranted >=10% complete-cost price regions, not a claim that every symbolic assignment is impossible",
            remaining="External rates, complete retained byte-time, unitemized host work/fees and fresh-domain verification remain open"),
        output_certificate_limit="Counts and bounds reconstructed from saved records; raw-proof rechecking is a separate verification artifact",
    )


def extract_file(path):
    path = path.resolve()
    raw = path.read_bytes()
    run = json.loads(raw)
    if run["status"] != "complete":
        raise ValueError(f"Use completed acquisition records; preserve partial work separately: {path}")
    snapshot = path.parent / "bundle_service.py"
    if not snapshot.is_file() or digest(snapshot.read_bytes()) != run["implementation_sha256"]:
        raise ValueError(f"Missing or changed bound implementation snapshot: {snapshot}")
    for name, expected in run["dependencies"].items():
        snapshot = path.parent / name
        if snapshot.exists() and digest(snapshot.read_bytes()) != expected:
            raise ValueError(f"Changed archived dependency: {snapshot}")
    return [extract_arm(run, arm, path, digest(raw)) for arm in run["arms"]]


def comparison(candidate, control):
    if candidate["scope_id"] != control["scope_id"]:
        raise ValueError("Cannot compare different source/request/admission scopes")
    c, b = candidate["resources"], control["resources"]
    delta = c["arm_named_units"]-b["arm_named_units"]
    # Decimal-free coefficients for 10*C_candidate - 9*C_control <= 0.
    coefficients = dict(
        constant_named_units=10*c["full_horizon_named_units"]-9*b["full_horizon_named_units"],
        audit_price_a=10*c["external_audits"]-9*b["external_audits"],
        cpu_rate_per_ns_rho=10*c["recorded_current_process_ns"]-9*b["recorded_current_process_ns"],
        recorded_byte_retention_rate_s=10*c["recorded_retained_bytes"]-9*b["recorded_retained_bytes"],
        candidate_unpriced_remainder=10, control_unpriced_remainder=-9,
    )
    payload_known = 0
    payload_unmeasured = {}
    for label, resource, coefficient in (("candidate", c, 10), ("control", b, -9)):
        payload = resource["additional_quotation_payload_bytes"]
        if payload is None:
            payload_unmeasured[f"{label}_unmeasured_quotation_payload_bytes"] = coefficient
        else:
            payload_known += coefficient*payload
    coefficients["known_additional_payload_bytes"] = payload_known
    return dict(candidate_source=candidate["source"], control_source=control["source"],
        candidate_version=candidate["version"], control_policy=control["policy"],
        arm_named_unit_ratio=c["arm_named_units"]/b["arm_named_units"],
        arm_named_savings_percent=-100*delta/b["arm_named_units"],
        full_horizon_named_savings_percent=100*(b["full_horizon_named_units"]-c["full_horizon_named_units"])/b["full_horizon_named_units"],
        actual_audit_difference=c["external_audits"]-b["external_audits"],
        actual_complete_call_difference=candidate["counts"]["complete_calls"]-control["counts"]["complete_calls"],
        actual_native_attempt_difference=candidate["counts"]["native_attempts"]-control["counts"]["native_attempts"],
        common_evaluator_hash_equal=candidate["dependency_hashes"]["repair_interface.py"] == control["dependency_hashes"]["repair_interface.py"],
        ten_percent_full_cost_condition=dict(coefficients=coefficients,
            unmeasured_payload_coefficients=payload_unmeasured,
            inequality="constant + a*A_coefficient + rho*T_coefficient + s*(B_coefficient + known_additional_payload_bytes + sum(unmeasured_payload_coefficient*payload_bytes)) + 10*R_candidate - 9*R_control <= 0",
            notes="U includes history and current admission once per standalone full horizon. T and B are recorded components only; Q payloads missing from older records remain explicit unknowns, and R retains all other missing components. Rates must avoid duplicate billing. This inequality is not an established economic saving."),
        timing_limit="One ordered development execution per input, not a repeated timing benchmark",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", nargs="+", type=Path)
    args = parser.parse_args()
    arms = [arm for path in args.results for arm in extract_file(path)]
    controls = [arm for arm in arms if arm["policy"] != "bundle"]
    comparisons = [comparison(candidate, control)
        for candidate in arms if candidate["policy"] == "bundle"
        for control in controls if candidate["scope_id"] == control["scope_id"]]
    print(json.dumps(dict(version=VERSION, evidence="DEVELOPMENT read-only extraction",
        contributor="ChatGPT (GPT-6 Astra Pro)", new_acquisitions=0,
        extractor_sha256=digest(Path(__file__).read_bytes()),
        arms=arms, comparisons=comparisons,
        policy="Latest completed implementation for the active row; retain intermediate records. Carry prior measurements with source age, never an invented repeated measurement. All full-cost regions remain unestablished until complete pricing and verification support them."), indent=2))


if __name__ == "__main__":
    main()
