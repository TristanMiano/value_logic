"""Independent development probes for the P3-07 arithmetic adapter.

Agent implementation time unmeasured; zero principal Research90 credit.
These are adapter boundary/correctness checks, not a scientific evaluation.
"""
from dataclasses import replace
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[5]
PATH = ROOT / "v3/checks/07_computation_adapter.py"
SPEC = importlib.util.spec_from_file_location("p307_adapter_development_probe", PATH)
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


def full(query, *, cap=1024, transactions=M.MAX_FULL_TRANSACTIONS, shortcut=True):
    return M.complete(query, cap, transactions, use_shortcut=shortcut)


def main():
    counters = dict(exact_crosschecks=0, shortcut_crosschecks=0, hard_cap_probes=0)
    maximum = dict(units=0, transactions=0, input=None)
    # Systematic boundary/interior sweep; Python pow is only a private test
    # oracle, and no controller or training profile receives its work for free.
    for modulus in (2, 3, 5, 17, 97):
        for exponent in range(M.MAX_N + 1):
            for base in sorted({0, 1, 2, modulus - 1, 7, M.MAX_A}):
                query = M.Query("x" * M.MAX_LABEL, base, exponent, modulus,
                                exponent % modulus, "s" * M.MAX_LABEL)
                result = full(query, shortcut=False)
                answer = result["answer"]
                assert answer is not None, result
                residue = pow(base, exponent, modulus)
                assert answer["residue"] == residue
                assert answer["answer"] == int(residue == query.r)
                assert result["meter"]["total"] == sum(result["meter"]["by_category"].values())
                assert result["meter"]["total"] <= M.MAX_COLD_COMPLETION_UNITS
                progress = result["progress"]
                assert progress["transactions"] <= M.MAX_FULL_TRANSACTIONS
                counters["exact_crosschecks"] += 1
                if result["meter"]["total"] > maximum["units"]:
                    maximum = dict(units=result["meter"]["total"],
                                   transactions=progress["transactions"], input=answer["claim_key"])
                if exponent in (0, 1, 2, 47, 192):
                    fast = full(query)
                    assert fast["answer"] is not None
                    assert fast["answer"]["residue"] == residue
                    counters["shortcut_crosschecks"] += 1
    query = M.Query("hard-cap", 7, 191, 97, 1)
    for limit in range(650):
        result = full(query, cap=limit)
        assert result["meter"]["total"] <= limit
        if result["answer"] is not None:
            assert result["answer"]["residue"] == pow(query.a, query.n, query.m)
        counters["hard_cap_probes"] += 1

    meter, query = M.Meter(2000), M.Query("cache", 7, 47, 97, 1)
    adapter = M.Adapter(meter)
    handle = adapter.start(query)
    short = adapter.advance(handle, 3)
    assert not short.checked_ready
    assert not hasattr(short, "residue") and not hasattr(short, "answer")
    # Python equality conflates bool/float/int; handles must not inherit that
    # identity ambiguity, even though the private job would remain unchanged.
    for bad_key in (handle.claim_key[:-1] + (True,), handle.claim_key[:-1] + (1.0,)):
        try:
            adapter.advance(M.JobHandle(handle.job_id, bad_key), 1)
        except M.ProtocolError:
            pass
        else:
            raise AssertionError("A representation-aliased handle was accepted.")
    try:
        adapter.acquire(handle)
    except M.ProtocolError:
        pass
    else:
        raise AssertionError("An unchecked answer was acquired.")
    done = adapter.advance(handle, M.MAX_FULL_TRANSACTIONS)
    assert done.checked_ready
    answer = adapter.acquire(handle)
    assert answer.residue == pow(query.a, query.n, query.m)
    changed_target = replace(query, query_id="new-display-id", r=(query.r + 1) % query.m)
    cached = adapter.lookup(changed_target)
    assert cached.provenance == "exact_semantic_cache"
    assert cached.answer == int(answer.residue == changed_target.r)
    assert adapter.lookup(replace(query, source_version="new-source")) is None

    # Acquisition is one atomic publication boundary.  Denial preserves the
    # checked private job and does not create a cache entry or return a bit.
    meter2 = M.Meter(2000, {"acquisition": 0})
    adapter2 = M.Adapter(meter2)
    handle2 = adapter2.start(query)
    assert adapter2.advance(handle2, 19).checked_ready
    try:
        adapter2.acquire(handle2)
    except M.BudgetExhausted:
        pass
    else:
        raise AssertionError("Unpaid acquisition was accepted.")
    assert adapter2.public_state()["cached_residues"] == 0
    assert adapter2.public_state()["active_jobs"] == 1

    # Perturbed producer output must be rejected by the independently executed
    # checker.  Private state access here is hostile test instrumentation.
    meter3, adapter3 = M.Meter(2000), None
    adapter3 = M.Adapter(meter3)
    handle3 = adapter3.start(query)
    job = adapter3._jobs[handle3.job_id]
    while job["phase"] == "produce":
        adapter3.advance(handle3, 1)
    job["result"] = (job["result"] + 1) % query.m
    try:
        adapter3.advance(handle3, 19)
    except AssertionError:
        pass
    else:
        raise AssertionError("Perturbed producer was not rejected.")
    assert adapter3.public_state()["cached_residues"] == 0

    for invalid in (True, -1, M.MAX_N + 1):
        try:
            replace(query, n=invalid)
        except M.ProtocolError:
            pass
        else:
            raise AssertionError("Out-of-scope exponent accepted.")

    # Include the common lookup/shortcut prefix in the declared complete cost.
    prefix_maximum = 0
    for exponent in range(M.MAX_N + 1):
        query = M.Query("z" * 128, 7, exponent, 97, 0, "s" * 128)
        result = full(query)
        assert result["answer"] is not None
        prefix_maximum = max(prefix_maximum, result["meter"]["total"])
    assert prefix_maximum <= M.MAX_COLD_COMPLETION_UNITS
    return dict(status="PASS", classification="DEVELOPMENT_ADAPTER_PROBES",
                adapter_version=M.VERSION, counters=counters, maximum_without_shortcut=maximum,
                adapter_sha256=hashlib.sha256(PATH.read_bytes()).hexdigest(),
                maximum_with_common_prefix=prefix_maximum,
                declared_cold_response_bound=M.MAX_COLD_COMPLETION_UNITS,
                declared_max_transactions=M.MAX_FULL_TRANSACTIONS,
                independent_checker_tamper="rejected", same_residue_new_target="reused",
                source_version_change="cache_miss", denied_acquisition="no_cache_publication",
                short_transaction_allowance="no_answer", principal_research90_credit_seconds=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error("Refusing to overwrite existing development evidence.")
    text = json.dumps(main(), sort_keys=True, indent=2) + "\n"
    if args.output is not None:
        with args.output.open("x") as stream:
            stream.write(text)
    print(text, end="")
