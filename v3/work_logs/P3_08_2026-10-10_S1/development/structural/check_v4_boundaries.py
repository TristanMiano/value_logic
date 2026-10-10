#!/usr/bin/env python3
"""Focused, source-bound v4 resource-failure API probes; not performance runs."""
from __future__ import annotations

import argparse
import dis
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import shutil
import sys
import traceback
from unittest.mock import patch

sys.dont_write_bytecode = True
VERSION = "p308-structural-v4-boundary-review-v2"


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def cold_leaf():
    value = 7
    return value


def cold_caller():
    return cold_leaf()


def main(root, output):
    root, out = Path(root).resolve(), Path(output).resolve()
    out.mkdir(parents=True, exist_ok=False)
    code = root / "v3/experiments/p308_structural.py"
    spec = importlib.util.spec_from_file_location("p308_structural_v4_boundary_subject", code)
    subject = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = subject
    spec.loader.exec_module(subject)
    assert subject.VERSION == "p308-structural-v4.1"
    subject._load_legacy()
    fixture = subject.fixtures()[0]
    sources = subject.source_files("candidate")
    own = Path(__file__).resolve()
    paths = sources + [own, own.parent / "v4_amendment.md", own.parent / "v4_1_trace_amendment.md"]

    def manifest():
        return [{"path": str(p.relative_to(root)), "bytes": p.stat().st_size,
                 "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]

    before = manifest()
    save(out / "manifest_before.json", before)
    for p in paths:
        target = out / "source" / p.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
    checks, rows = [], []

    def passed(name, **details):
        checks.append({"check": name, "passed": True, **details})

    assert sys.gettrace() is None and sys.getprofile() is None
    cold_codes = {cold_caller.__code__, cold_leaf.__code__}
    expected_offsets = {c.co_name: [i.offset for i in dis.get_instructions(c)
                                   if i.opname not in ("RESUME", "CACHE", "COPY_FREE_VARS")]
                        for c in cold_codes}
    observed_offsets = {c.co_name: [] for c in cold_codes}
    original_trace = subject.StructuralMeter._meter_trace

    def observed_trace(self, frame, event, arg):
        if event == "opcode" and frame.f_code in cold_codes:
            observed_offsets[frame.f_code.co_name].append(frame.f_lasti)
        callback = original_trace(self, frame, event, arg)
        return self._meter_trace if callback is not None else None

    cold_meter = subject.StructuralMeter()
    with patch.object(subject.StructuralMeter, "_meter_trace", observed_trace):
        value = cold_meter._meter_run("cold_first_worker", cold_caller)
    assert value == 7 and observed_offsets == expected_offsets
    expected_units = sum(len(v) for v in expected_offsets.values())
    assert cold_meter.units == expected_units
    passed("first_worker_and_first_leaf_have_every_opcode_event",
           observed_offsets=observed_offsets, expected_offsets=expected_offsets,
           opcode_units=expected_units, invoice=cold_meter._meter_invoice())

    for value in (True, 100000.0, -1, 0, subject.TERMINAL_RESERVE - 1):
        with patch.object(subject, "deployment_setup", side_effect=AssertionError("Admission was attempted")):
            try:
                subject.run_method(fixture, "candidate", budget=value)
            except ValueError as exc:
                assert "no paid work occurred" in str(exc)
            else:
                raise AssertionError("Invalid account was admitted")
        passed("invalid_account_rejected_before_paid_admission", value=repr(value))

    payload = subject.UNKNOWN_BUDGET_PAYLOAD
    expected = json.loads(payload)
    assert len(payload.encode("ascii")) == 140
    assert expected["status"] == "UNKNOWN_BUDGET"
    assert expected["received_answer"] is False
    assert expected["decision"]["useful_action_warrant"] is False
    assert subject.wire(expected) == payload

    meter = subject.StructuralMeter(subject.TERMINAL_RESERVE)
    meter._meter_charge("terminal_reporting", "normal_terminal_saturation",
                        meter.budget - subject.FAILURE_READOUT_RESERVE)
    prefix = meter.units
    meter.failure_readout = True
    actual = meter._meter_run("terminal_reporting", subject.unknown_budget_payload)
    meter._meter_bytes("terminal_reporting", "report_bytes", actual)
    fixed_cost = meter.units - prefix
    assert actual == payload and fixed_cost == 142
    assert fixed_cost <= subject.FAILURE_READOUT_RESERVE
    passed("fixed_failure_tranche_is_sufficient", fixed_payload_bytes=140,
           traced_literal_return_units=fixed_cost - 140, fixed_receipt_units=fixed_cost,
           reserve=subject.FAILURE_READOUT_RESERVE, invoice=meter._meter_invoice())

    def verify_failure(name, record, admitted_count, input_complete, stage, prefix=None):
        inv = record["invoice"]
        admitted = record["source_admission"]
        assert record["output"] == expected
        assert len(admitted) == admitted_count
        assert record["admission"] == {
            "sources_complete": admitted_count == len(subject.source_files(record["method"])),
            "input_complete": input_complete}
        assert len(inv["failures"]) == 1
        failure = inv["failures"][0]
        assert failure["stage"] == stage
        if prefix is not None:
            assert failure["paid_prefix_units"] == prefix
        assert inv["total_units"] == failure["paid_prefix_units"] + fixed_cost
        assert inv["total_units"] <= inv["budget"]
        assert inv["failure_readout_released"] is True
        assert inv["by_stage"]["terminal_reporting"]["report_bytes"] == 140
        assert sum(sum(v.values()) for v in inv["by_stage"].values()) == inv["total_units"]
        assert sum(v["bytes"] for v in admitted) == inv["by_stage"].get("setup", {}).get("source_admission_bytes", 0)
        rows.append({"case": name, "record": record})
        passed(name, failure_stage=stage, admitted_sources=admitted_count,
               input_complete=input_complete, paid_prefix_units=failure["paid_prefix_units"],
               fixed_failure_receipt_units=fixed_cost)

    for method in ("candidate", "ordinary"):
        record = subject.run_method(fixture, method, budget=subject.TERMINAL_RESERVE)
        verify_failure(method + "_first_source_denied", record, 0, False, "setup", 0)
    first_size = sources[0].stat().st_size
    record = subject.run_method(fixture, "candidate", budget=subject.TERMINAL_RESERVE + first_size)
    verify_failure("candidate_second_source_denied", record, 1, False, "setup", first_size)
    for method in ("candidate", "ordinary"):
        current_sources = subject.source_files(method)
        source_bill = sum(p.stat().st_size for p in current_sources)
        record = subject.run_method(fixture, method, budget=subject.TERMINAL_RESERVE + source_bill)
        verify_failure(method + "_input_admission_denied", record, len(current_sources), False,
                       "input_admission", source_bill)

    # These two interventions saturate a tariff allowance at a declared stage.
    # They exercise handler/reserve boundaries, not the natural cost of a policy.
    original_run = subject.StructuralMeter._meter_run
    for boundary in ("before_success_serialization", "before_success_report_bytes"):
        state = {"injections": 0}

        def saturated_run(self, stage, function):
            inject = (stage == "terminal_reporting" and self.current is None
                      and not self.active and not self.failure_readout)
            if inject and boundary == "before_success_serialization":
                self._meter_charge(stage, "boundary_injected_work",
                                   self.budget - subject.FAILURE_READOUT_RESERVE - self.units)
                state["injections"] += 1
            value = original_run(self, stage, function)
            if inject and boundary == "before_success_report_bytes":
                self._meter_charge(stage, "boundary_injected_work",
                                   self.budget - subject.FAILURE_READOUT_RESERVE - self.units)
                state["injections"] += 1
            return value

        # The harness hook is measuring apparatus, never a worker primitive.
        subject._METER_CODES.add(saturated_run.__code__)
        try:
            with patch.object(subject.StructuralMeter, "_meter_run", saturated_run):
                record = subject.run_method(fixture, "ordinary")
        finally:
            subject._METER_CODES.remove(saturated_run.__code__)
        assert state["injections"] == 1
        verify_failure(boundary, record, 1, True, "terminal_reporting",
                       subject.SUCCESS_BUDGET - subject.FAILURE_READOUT_RESERVE)
        checks[-1]["fault_injection_not_a_performance_case"] = True
        assert record["invoice"]["by_stage"]["terminal_reporting"]["boundary_injected_work"] > 0

    after = manifest()
    save(out / "manifest_after.json", after)
    assert before == after
    passed("complete_source_closure_unchanged")
    save(out / "boundary_records.json", rows)
    save(out / "checks.json", checks)
    summary = {"version": VERSION, "subject_version": subject.VERSION, "stage": "DEVELOPMENT",
               "python": sys.version, "platform": platform.platform(),
               "checks": len(checks), "passed": len(checks), "failures": [],
               "resource_failure_records": len(rows), "fixed_failure_receipt_units": fixed_cost,
               "source_closure_unchanged": True, "principal_time_credit_seconds": 0,
               "native_finite_contract_only": True, "terminal_cases_are_fault_injection": True,
               "reproduce": "python " + str(own) + " " + str(root) + " /tmp/p308_structural_v4_boundary_replay"}
    save(out / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root")
    parser.add_argument("out")
    args = parser.parse_args()
    try:
        main(args.root, args.out)
    except BaseException as exc:
        out = Path(args.out)
        if out.is_dir():
            save(out / "failure.json", {"type": type(exc).__name__, "message": str(exc),
                                       "traceback": traceback.format_exc(), "stage": "DEVELOPMENT"})
        raise
