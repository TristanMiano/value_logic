"""Focused v1.1 admission/accounting repair checks; no broad arithmetic rerun.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
Agent time unmeasured; zero principal Research90 credit.
"""
import argparse
from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "v3/checks/07_computation_adapter.py"
SPEC = importlib.util.spec_from_file_location("p307_adapter_boundary_v1_1", SOURCE)
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


def reject(fn, exception):
    try:
        fn()
    except exception:
        return
    raise AssertionError("Expected boundary rejection did not occur.")


def run():
    assert M.VERSION == "p307-modular-computation-adapter-v1.1"
    query = M.Query("q" * 128, 7, 191, 97, 0, "s" * 128)
    rejected = 0
    for updates in ({"query_id": "caf\u00e9"}, {"source_version": "\u03b1"},
                    {"query_id": "x" * 129}, {"source_version": "y" * 129}):
        reject(lambda updates=updates: replace(query, **updates), M.ProtocolError)
        rejected += 1
    reject(lambda: M.Meter(100).pay("assessment", "\u03bb", 1), M.ProtocolError)
    rejected += 1
    meter, adapter = M.Meter(1024), None
    adapter = M.Adapter(meter)
    assert adapter.lookup(query) is None
    assert adapter.shortcut(query) is None
    handle = adapter.start(query)
    before = meter.total
    progress = adapter.advance(handle, M.MAX_FULL_TRANSACTIONS)
    assert progress.checked_ready and progress.transactions == 19
    assert progress.spent_units == meter.total - before
    answer = adapter.acquire(handle)
    assert answer.residue == pow(query.a, query.n, query.m) == 14 and answer.answer == 0
    assert meter.total <= M.MAX_COLD_COMPLETION_UNITS
    assert meter.operations["admission.handle_scalar_field_check"] == 16
    assert meter.operations["admission.handle_identity_word_compare"] == 48
    assert meter.operations["storage.completed_job_release"] == 1
    assert adapter.public_state()["active_jobs"] == 0

    class RejectMembership(dict):
        def __contains__(self, key):
            raise AssertionError("Invalid identity reached dictionary lookup.")

    boundary_adapter = M.Adapter(M.Meter(2000))
    boundary_handle = boundary_adapter.start(query)
    ordinary_jobs = boundary_adapter._jobs
    boundary_adapter._jobs = RejectMembership(ordinary_jobs)
    for bad_id in (False, -1, M.MAX_TOTAL_UNITS + 1, 1 << 1_000_000):
        reject(lambda bad_id=bad_id: boundary_adapter.advance(
            M.JobHandle(bad_id, boundary_handle.claim_key), 1), M.ProtocolError)
        rejected += 1
    for bad_claim in (
        boundary_handle.claim_key[:-1] + (True,),
        boundary_handle.claim_key[:-1] + (0.0,),
        (boundary_handle.claim_key[0], "\u03b1") + boundary_handle.claim_key[2:],
        boundary_handle.claim_key[:3] + (M.MAX_N + 1,) + boundary_handle.claim_key[4:],
    ):
        reject(lambda bad_claim=bad_claim: boundary_adapter.advance(
            M.JobHandle(boundary_handle.job_id, bad_claim), 1), M.ProtocolError)
        rejected += 1
    boundary_adapter._jobs = ordinary_jobs

    blocked_meter = M.Meter(2000, {"admission": 8 + query.key_words})
    blocked_adapter = M.Adapter(blocked_meter)
    blocked_handle = blocked_adapter.start(query)
    private_before = dict(blocked_adapter._jobs[blocked_handle.job_id])
    reject(lambda: blocked_adapter.advance(blocked_handle, 1), M.BudgetExhausted)
    assert blocked_adapter._jobs[blocked_handle.job_id] == private_before
    assert blocked_meter.total <= blocked_meter.limit_total

    denied_meter = M.Meter(2000, {"acquisition": 0})
    denied_adapter = M.Adapter(denied_meter)
    denied_handle = denied_adapter.start(query)
    assert denied_adapter.advance(denied_handle, 19).checked_ready
    reject(lambda: denied_adapter.acquire(denied_handle), M.BudgetExhausted)
    assert denied_adapter.public_state()["active_jobs"] == 1
    assert denied_adapter.public_state()["cached_residues"] == 0
    assert denied_meter.operations["storage.completed_job_release"] == 0
    return dict(status="PASS", classification="FOCUSED_DEVELOPMENT_BOUNDARY_REPAIR",
        adapter_version=M.VERSION, adapter_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        rejected_admission_cases=rejected, large_id_rejected_before_hash_lookup=True,
        paid_handle_preflight_in_progress_total=True, denied_preflight_state_unchanged=True,
        denied_publication_retains_job_and_empty_cache=True,
        completed_release_inside_publication_bundle=True,
        cold_complete_units=meter.total, cold_complete_transactions=progress.transactions,
        conservative_component_bound=594, exported_cold_bound=M.MAX_COLD_COMPLETION_UNITS,
        complete_meter=meter.snapshot(), broad_arithmetic_sweep_repeated=False,
        principal_research90_credit_seconds=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite existing development evidence.")
    result = run()
    with args.output.open("x") as stream:
        stream.write(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "complete_meter"},
                     sort_keys=True, indent=2))
