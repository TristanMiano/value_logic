"""Source-copied focused stronger-control checks. DEVELOPMENT only."""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import asdict, replace
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import struct
import sys
import time
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[4]
LOG = REPO / "v3/work_logs/P3_08_2026-10-10_S1"


def dump(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise RuntimeError("Retain earlier evidence; use a new output directory.")
    args.out.mkdir(parents=True)
    snapshot = args.out / "source_snapshot"
    source_map = {}
    # The independently modified broker is intentionally outside this focused
    # check. Use its already sealed common_v1 kernel; root owns combined v2.
    for name in ("p308_common.py", "p308_broker.py", "p308_cnf.py"):
        source_map["v3/experiments/" + name] = LOG / "development/common_v1/source/v3/experiments" / name
    for name in ("p308_ordinary.py", "p308_hashcache.py"):
        source_map["v3/experiments/" + name] = REPO / "v3/experiments" / name
    for name in ("07_selective_feedback.py", "07_selective_feedback_service.py", "07_computation_adapter.py"):
        source_map["v3/checks/" + name] = LOG / "development/common_v1/source/v3/checks" / name
    source_map["reviews/hashcache_input_plan.json"] = Path(__file__).with_name("hashcache_input_plan.json")
    source_map["reviews/hashcache_development_check.py"] = Path(__file__).resolve()
    source_map["reviews/p308_ordinary_v1_3.py"] = Path(__file__).with_name("source_revisions") / "p308_ordinary_v1_3.py"
    hashes = {}
    for relative, source in source_map.items():
        target = snapshot / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        blob = source.read_bytes()
        target.write_bytes(blob)
        hashes[relative] = hashlib.sha256(blob).hexdigest()
    dump(args.out / "started.json", {
        "stage": "DEVELOPMENT", "wall_start_ns": time.time_ns(), "argv": sys.argv,
        "sources": hashes, "principal_clock_credit_ns": 0,
        "copied_transitive_source_closure": True,
        "broker_scope": "Sealed common_v1 kernel; separate broker extension and final combined closure belong to root.",
        "private_main_scoring": False,
    })
    sys.path.insert(0, str(snapshot / "v3/experiments"))
    import p308_cnf as S
    import p308_hashcache as H
    import p308_ordinary as O
    from p308_common import C
    checks, runs, receipts = [], {}, []

    def purchase(q):
        receipt = S.checked_purchase(q, limit_total=S.service_cap(q, "dpll"), solver="dpll")
        assert receipt.successful and receipt.checked
        receipts.append(receipt.record())
        return receipt

    def state(cache):
        return {"initialized": cache._initialized, "buckets": deepcopy(cache._buckets),
                "slots": None if cache._slots is None else [None if e is None else asdict(e) for e in cache._slots],
                "cursor": cache._cursor, "count": cache._count,
                "entry_words": cache._entry_words, "retained_words": cache.retained_words}

    def invariant(cache):
        if not cache._initialized:
            assert cache.entries == cache.retained_words == 0
            return
        seen = set()
        for bucket, first in enumerate(cache._buckets):
            previous, slot = -1, first
            while slot != -1:
                assert 0 <= slot < cache.capacity and slot not in seen
                entry = cache._slots[slot]
                assert entry is not None and entry.bucket == bucket and entry.previous == previous
                seen.add(slot)
                previous, slot = slot, entry.next
        occupied = {i for i, e in enumerate(cache._slots) if e is not None}
        assert seen == occupied and len(occupied) == cache.entries <= cache.capacity
        assert cache._entry_words == sum(H.ENTRY_WORDS + cache._slots[i].key_words for i in occupied)
        assert cache.retained_words == H.HEADER_WORDS + len(cache._buckets) + cache.capacity + cache._entry_words

    def expect_denial(call):
        try:
            call()
        except C.BudgetExceeded:
            return
        raise AssertionError("Expected a paid-operation budget denial.")

    basic = (
        S.make_query("syntax-sat", 3, ((1,), (-2,), (3,))),
        S.make_query("syntax-unsat", 3, ((1,), (-1,))),
        S.make_query("syntax-empty", 1, ()),
        S.make_query("syntax-duplicates", 3, ((1, 1), (-2, 2), (1, 1))),
        S.make_query("syntax-max", 12, ((-12, -1, 1, 12),) * 64),
    )
    dump(args.out / "public_syntax_tape.json", [q.record() for q in basic])
    for q in basic:
        pieces = []
        for label in (q.semantics_version, q.source_version):
            raw = label.encode("ascii")
            pieces += [struct.pack("<Q", len(raw)), raw + b"\0" * (-len(raw) % 8)]
        pieces += [struct.pack("<Q", q.variables), struct.pack("<Q", len(q.clauses))]
        for clause in q.clauses:
            pieces.append(struct.pack("<Q", len(clause)))
            pieces.extend(struct.pack("<q", lit) for lit in clause)
        encoded = b"".join(pieces)
        meter = C.CostMeter()
        digest = H.paid_key_digest(q, meter)
        assert len(encoded) == 8 * q.key_words
        assert digest == hashlib.sha256(encoded).digest()
        assert meter.operations["cache", "hashcache_sha256_input_block"] == (len(encoded) + 72) // 64
        assert meter.total == 3 * q.key_words + 8 + (len(encoded) + 72) // 64
        for count in H.BUCKET_COUNTS:
            assert H.paid_key_bucket(q, C.CostMeter(), count) == int.from_bytes(digest[:2], "little") & (count - 1)
    for bad in (0, True, 127, 512):
        try:
            H.ExactHashCache(bucket_count=bad)
        except S.Rejected:
            pass
        else:
            raise AssertionError("Invalid bucket shape was admitted.")
    for bad in (-1, True, 65):
        try:
            H.ExactHashCache(capacity=bad)
        except S.Rejected:
            pass
        else:
            raise AssertionError("Invalid capacity was admitted.")
    for invalid_call in (
        lambda: H.paid_key_digest({}, C.CostMeter()),
        lambda: H.paid_digest_bucket(b"x", C.CostMeter()),
        lambda: H.paid_digest_bucket(b"x" * 32, C.CostMeter(), 64),
        lambda: O.run_method(basic, "exact_cache", cache_kind="oracle"),
    ):
        try:
            invalid = invalid_call()
        except S.Rejected:
            continue
        assert invalid["status"] == "failed"
    checks.append({"name": "canonical_encoding_hash_tariff_and_bounded_syntax", "queries": len(basic)})

    cache, meter = H.ExactHashCache(4), C.CostMeter()
    q, false_q = basic[:2]
    true_receipt, false_receipt = purchase(q), purchase(false_q)
    assert cache.lookup(q, meter) is None
    assert cache.remember(q, true_receipt, meter)
    rebound = S.Query("new-request-id", q.variables, q.clauses, q.source_version)
    hit = cache.lookup(rebound, meter)
    assert hit.query_id == rebound.query_id and hit.claim_key == q.claim_key
    assert hit.provider == H.PROVIDER and hit.provider_version == S.VERSION and hit.answer == 1
    assert hit.resources.total == sum(n for _, n in hit.resources.by_category)
    assert not cache.remember(rebound, hit, meter)
    version = S.Query("new-version-id", q.variables, q.clauses, "cnf-input-v2")
    assert cache.lookup(version, meter) is None and cache.lookup(false_q, meter) is None
    for bad in (replace(true_receipt, query_id="wrong"), replace(true_receipt, provider_version="stale"),
                replace(true_receipt, claim_key=false_q.claim_key), replace(true_receipt, checked=False),
                replace(true_receipt, answer=True), replace(true_receipt, provider="external")):
        before = state(cache)
        try:
            cache.remember(q, bad, meter)
        except S.Rejected:
            pass
        else:
            raise AssertionError("A misbound receipt was admitted.")
        assert before == state(cache)
    invariant(cache)
    disabled = H.ExactHashCache(0)
    disabled_meter = C.CostMeter()
    assert disabled.lookup(q, disabled_meter) is None
    assert not disabled.remember(q, true_receipt, disabled_meter)
    assert disabled.entries == 0 and disabled.retained_words == H.HEADER_WORDS
    checks.append({"name": "receipt_version_content_request_binding_and_zero_capacity"})

    buckets, collision, discovery = {}, None, C.CostMeter()
    collision_candidates = tuple(S.Query(f"collision-{i}", q.variables, q.clauses, f"source-collision-{i}")
                                 for i in range(129))
    for candidate in collision_candidates:
        bucket = H.paid_key_bucket(candidate, discovery)
        if bucket in buckets:
            collision = (buckets[bucket], candidate)
            break
        buckets[bucket] = candidate
    assert collision is not None
    collision_cache, collision_meter = H.ExactHashCache(2), C.CostMeter()
    for candidate in collision:
        assert collision_cache.remember(candidate, purchase(candidate), collision_meter)
    for candidate in collision:
        assert collision_cache.lookup(candidate, collision_meter).claim_key == candidate.claim_key
    invariant(collision_cache)
    real_digest = H._digest

    def forced_digest(query, paid_meter):
        real_digest(query, paid_meter)
        return b"\0" * 32

    with patch.object(H, "_digest", forced_digest):
        forced, paid = H.ExactHashCache(2), C.CostMeter()
        assert forced.remember(q, true_receipt, paid)
        assert forced.remember(false_q, false_receipt, paid)
        assert forced.lookup(q, paid).answer == 1
        assert forced.lookup(false_q, paid).answer == 0
        before = state(forced)
        try:
            forced.remember(q, replace(true_receipt, answer=0), paid)
        except S.Rejected:
            pass
        else:
            raise AssertionError("Same-key conflicting answer was accepted.")
        assert before == state(forced)
        invariant(forced)
    checks.append({"name": "real_bucket_and_forced_paid_digest_collisions_are_full_key_safe",
                   "real_collision_queries": [c.record() for c in collision],
                   "test_discovery_hash_units": discovery.total})

    fifo_inputs = tuple(S.Query(f"fifo-{i}", q.variables, q.clauses, f"fifo-source-{i}") for i in range(7))
    fifo_receipts = tuple(purchase(candidate) for candidate in fifo_inputs)
    for same_bucket in (False, True):
        manager = patch.object(H, "_digest", forced_digest) if same_bucket else patch.object(H, "_digest", real_digest)
        with manager:
            fifo, paid = H.ExactHashCache(3, 256), C.CostMeter()
            order = []
            for i, (candidate, receipt) in enumerate(zip(fifo_inputs, fifo_receipts)):
                if i == 3:
                    assert fifo.lookup(fifo_inputs[0], paid) is not None
                    assert not fifo.remember(fifo_inputs[1], fifo_receipts[1], paid)
                assert fifo.remember(candidate, receipt, paid)
                order.append(candidate.claim_key)
                order = order[-3:]
                invariant(fifo)
                assert {entry.key for entry in fifo._slots if entry is not None} == set(order)
            assert fifo.lookup(fifo_inputs[0], paid) is None
            assert paid.operations["cache", "hashcache_fifo_eviction_reference_release"] == 16
    checks.append({"name": "FIFO_wraparound_duplicates_hits_and_collision_unlink_preserve_order"})

    blank = H.ExactHashCache(2)
    rejected_setup = C.CostMeter(0)
    expect_denial(lambda: blank.lookup(q, rejected_setup))
    assert not blank._initialized and rejected_setup.total == 0
    admitted = C.CostMeter()
    S._admit(q, admitted)
    paid_init = C.CostMeter()
    blank._setup(paid_init)
    before = state(blank)
    rejected_hash = C.CostMeter(admitted.total + 3)
    expect_denial(lambda: blank.lookup(q, rejected_hash))
    assert rejected_hash.total > 0 and before == state(blank)

    full, past = H.ExactHashCache(1), C.CostMeter()
    full.remember(q, true_receipt, past)
    probe, completion = deepcopy(full), C.CostMeter()
    assert probe.remember(false_q, false_receipt, completion)
    before = state(full)
    denied_insert = C.CostMeter(completion.total - 1)
    expect_denial(lambda: full.remember(false_q, false_receipt, denied_insert))
    assert denied_insert.total > 0 and before == state(full)
    hit_probe = C.CostMeter()
    assert full.lookup(q, hit_probe).answer == 1
    denied_output = C.CostMeter(hit_probe.total - 1)
    expect_denial(lambda: full.lookup(q, denied_output))
    assert before == state(full) and denied_output.total > 0
    checks.append({"name": "failed_setup_hash_eviction_and_output_preserve_paid_prefix_and_state",
                   "denied_hash_units": rejected_hash.total,
                   "denied_eviction_units": denied_insert.total,
                   "denied_output_units": denied_output.total})

    small = basic[:4]

    def forbidden(*args, **kwargs):
        raise AssertionError("no_compute invoked a computation/feedback component.")

    with patch.object(S, "checked_purchase", forbidden), patch.object(S, "expert_predictions", forbidden), \
            patch.object(O, "NumericProd", forbidden), patch.object(C.BitTape, "seeded", forbidden):
        for fallback in (0, 1):
            result = O.run_method(small, "no_compute", fallback_action=fallback)
            runs[f"no_compute_small_{fallback}"] = result
            assert result["status"] == "success" and result["purchases"] == result["feedback_updates"] == 0
            assert result["random_bits_consumed"] == result["known_terminal_rounds"] == 0
            assert result["invoices"] == [] and result["weights"] is None
            assert all(row["terminal_action"] == fallback and row["hard_after"]["status"] == "unresolved"
                       and row["provider_status"] == "not_requested" for row in result["trace"])
    checks.append({"name": "direct_no_compute_never_calls_provider_experts_numeric_or_randomness"})

    spec = importlib.util.spec_from_file_location("_prior_ordinary_v1_3", snapshot / "reviews/p308_ordinary_v1_3.py")
    prior = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior)
    duplicate_tape = (q, false_q, S.Query("repeat-sat", q.variables, q.clauses),
                      S.Query("repeat-unsat", false_q.variables, false_q.clauses))
    for method in ("exact_cache", "ordinary_combo"):
        default = O.run_method(duplicate_tape, method, seed=11)
        linear = O.run_method(duplicate_tape, method, seed=11, cache_kind="linear")
        hashed = O.run_method(duplicate_tape, method, seed=11, cache_kind="hashed")
        old = prior.run_method(duplicate_tape, method, seed=11)
        assert default == linear
        normalized = deepcopy(linear)
        normalized["version"] = old["version"]
        del normalized["configuration"]["cache_kind"]
        del normalized["configuration"]["cache_bucket_count"]
        assert normalized == old
        assert hashed["status"] == "success"
        assert [r["terminal_action"] for r in hashed["trace"]] == [r["terminal_action"] for r in linear["trace"]]
        assert hashed["purchases"] == linear["purchases"]
        assert hashed["configuration"]["cache_bucket_count"] == 128
        runs[method + "_small_linear"] = linear
        runs[method + "_small_hashed"] = hashed
    checks.append({"name": "linear_default_preserves_v1_3_and_hashed_controller_integration"})

    catalogue = []
    for repeats, signs in itertools.product(range(4), itertools.product((-1, 1), repeat=3)):
        clause = tuple((i + 1) * signs[i] for i in range(3))
        catalogue.append(S.make_query(f"invoice-{len(catalogue)}", 3, (clause,) + ((1,),) * repeats))
    tape = tuple(S.Query(f"invoice-online-{i}", catalogue[i % 32].variables, catalogue[i % 32].clauses)
                 for i in range(64))
    dump(args.out / "public_invoice_tape.json", [q.record() for q in tape])
    comparison = {}
    for kind in ("linear", "hashed"):
        result = O.run_method(tape, "exact_cache", cache_kind=kind)
        runs["initial_invoice_exact_cache_" + kind] = result
        assert result["status"] == "success" and result["purchases"] == result["cache_hits"] == 32
        assert result["meter"]["total"] == sum(result["meter"]["by_category"].values())
        comparison[kind] = {"local_units": result["meter"]["total"],
                            "provider_units": sum(i["resources"]["total"] for i in result["invoices"]),
                            "purchases": result["purchases"], "cache_hits": result["cache_hits"],
                            "by_category": result["meter"]["by_category"],
                            "retained_words": result["cache_retained_words"]}
    assert comparison["linear"]["provider_units"] == comparison["hashed"]["provider_units"]
    assert [r["terminal_action"] for r in runs["initial_invoice_exact_cache_linear"]["trace"]] == [
        r["terminal_action"] for r in runs["initial_invoice_exact_cache_hashed"]["trace"]]
    for fallback in (0, 1):
        result = O.run_method(tape, "no_compute", fallback_action=fallback)
        runs[f"initial_invoice_no_compute_{fallback}"] = result
        comparison[f"no_compute_{fallback}"] = {"local_units": result["meter"]["total"],
                                               "purchases": result["purchases"]}
    checks.append({"name": "predeclared_32_key_two_pass_invoice_comparison", "comparison": comparison})

    assert hashes == {relative: sha(snapshot / relative) for relative in hashes}
    for name in ("p308_ordinary.py", "p308_hashcache.py"):
        assert sha(REPO / "v3/experiments" / name) == hashes["v3/experiments/" + name]
    dump(args.out / "runs.json", runs)
    dump(args.out / "service_test_receipts.json", receipts)
    result = {"stage": "DEVELOPMENT", "status": "PASS", "sources": hashes,
              "checks": checks, "principal_clock_credit_ns": 0, "wall_end_ns": time.time_ns(),
              "main_private_scores_inspected": False}
    dump(args.out / "result.json", result)
    print(json.dumps({"status": "PASS", "checks": len(checks), "comparison": comparison,
                      "ordinary_sha256": hashes["v3/experiments/p308_ordinary.py"],
                      "hashcache_sha256": hashes["v3/experiments/p308_hashcache.py"]}, sort_keys=True))


if __name__ == "__main__":
    main()
