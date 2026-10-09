"""Focused new-service correctness/cost probe, not a learner population run."""
from __future__ import annotations
import argparse
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import traceback


ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "v3/checks/07_selective_feedback_service.py"
SPEC = importlib.util.spec_from_file_location("_r_p3ba_service_probe", SOURCE)
assert SPEC is not None and SPEC.loader is not None
S = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = S
SPEC.loader.exec_module(S)


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def resource_check(record):
    assert record.total == sum(dict(record.by_category).values())
    assert record.total == sum(v for _, _, v in record.operations)
    encoded = record.record()
    assert encoded["total"] == sum(encoded["by_category"].values())
    assert encoded["total"] == sum(o["units"] for o in encoded["operations"])
    assert all(type(o["units"]) is int and o["units"] >= 0 for o in encoded["operations"])


def bound_result(result, query, truth, residue):
    assert result.successful and result.status == "success"
    assert result.answer == truth and result.residue == residue
    assert result.query_id == query.query_id
    assert result.claim_key == query.claim_key
    assert result.provider_version == S.VERSION + ";adapter=" + S.A.VERSION
    resource_check(result.resources)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    paths = (SOURCE, S.ADAPTER_PATH, Path(__file__).resolve(),
             ROOT / "v3/work_logs/R_P3_B_A_2026-10-09_S1/development/contract_v1.json")
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    write(out / "plan.json", {
        "stage": "DEVELOPMENT",
        "recorded_before_execution": True,
        "scope": "New service correctness and tariff probe over every one of the 248 admitted mathematical keys; no learner population.",
        "checks": ["All public expert outputs", "Checked/direct/table/cache mathematical agreement with private pow",
                   "Request and claim binding", "Cold and warm cache behavior", "Table square counts and word cap",
                   "Quota-independent completion caps", "Denied work preserves resources and emits no answer",
                   "Wrong family/source rejection", "FIFO eviction", "Frozen records", "Source registry accounting"],
        "source_sha256": manifest,
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "principal_clock_credit_ns": 0,
    })
    result = {"status": "FAIL", "source_sha256": manifest}
    try:
        table = S.QuadraticResidueTable()
        cache = S.ExactCache()
        resource_check(table.setup_resources)
        resource_check(cache.setup_resources)
        setup_operations = {(c, op): v for c, op, v in table.setup_resources.operations}
        assert setup_operations[("solve", "square_table_modular_square")] == 124
        assert setup_operations[("solve", "square_table_modular_reduce")] == 124
        assert sum(len(words) for words in table._tables) == 6
        assert all(0 <= value < 2 ** 64 for words in table._tables for value in words)
        rows = []
        first_receipt = None
        for p in S.PRIMES:
            for a in range(1, p):
                query = S.make_query(p, a, f"service-probe-{p}-{a}")
                # This independently evaluated answer is private diagnostic
                # truth. It is never an argument to an expert or service.
                expected_residue = pow(a, (p - 1) // 2, p)
                truth = int(expected_residue == 1)
                em = S.A.Meter(256)
                predictions = S.expert_predictions(query, em)
                assert predictions == (0, 1, a & 1, int(2 * a < p))
                assert all(type(x) is int and x in (0, 1) for x in predictions)
                checked = S.checked_purchase(query)
                direct = S.direct_exact(query)
                tabulated = table.answer(query)
                cached = cache.answer(query)
                for named in (checked, direct, tabulated, cached):
                    bound_result(named, query, truth, expected_residue)
                assert checked.checked is True
                assert all(x.checked is False for x in (direct, tabulated, cached))
                assert checked.resources.total <= S.CHECKED_PURCHASE_CAP
                assert direct.resources.total <= S.DIRECT_CAP
                assert cached.detail == "semantic_cache_miss_direct_compute"
                first_receipt = first_receipt or checked
                rows.append({"p": p, "a": a, "private_truth": truth,
                             "checked": checked.record(), "direct": direct.record(),
                             "table": tabulated.record(), "cache_cold": cached.record(),
                             "experts": list(predictions), "expert_units": em.total})
        assert len(rows) == S.POPULATION_SIZE
        assert sum(row["private_truth"] for row in rows) == 124
        assert cache._size == S.POPULATION_SIZE
        for row in rows:
            query = S.make_query(row["p"], row["a"], f"fresh-id-{row['p']}-{row['a']}")
            cached = cache.answer(query)
            bound_result(cached, query, row["private_truth"], 1 if row["private_truth"] else row["p"] - 1)
            assert cached.detail == "semantic_cache_hit"
            assert not any(op.startswith("direct_modular") for _, op, _ in cached.resources.operations)
            row["cache_warm"] = cached.record()
        assert first_receipt is not None
        try:
            first_receipt.answer = 9
            raise AssertionError("ServiceResult unexpectedly mutable")
        except FrozenInstanceError:
            pass
        small_cache = S.ExactCache(capacity=1)
        q1, q2 = S.make_query(17, 1, "fifo-1"), S.make_query(17, 2, "fifo-2")
        assert small_cache.answer(q1).detail == "semantic_cache_miss_direct_compute"
        assert small_cache.answer(q1).detail == "semantic_cache_hit"
        assert small_cache.answer(q2).detail == "semantic_cache_miss_direct_compute"
        assert small_cache.answer(q1).detail == "semantic_cache_miss_direct_compute"
        zero_cache = S.ExactCache(capacity=0)
        assert zero_cache.answer(q1).detail == "semantic_cache_miss_direct_compute"
        assert zero_cache.answer(q1).detail == "semantic_cache_miss_direct_compute"
        assert zero_cache._size == 0
        denial_records = []
        for cap in (0, 1, 8, 24, 40, 64, 100):
            query = S.make_query(97, 23, f"denied-{cap}")
            for function in (S.checked_purchase, S.direct_exact):
                answer = function(query, limit_total=cap)
                assert answer.resources.total <= cap
                resource_check(answer.resources)
                if not answer.successful:
                    assert answer.answer is None and answer.residue is None and not answer.checked
                denial_records.append({"cap": cap, "function": function.__name__, "result": answer.record()})
        assert any(r["result"]["resources"]["total"] > 0 and r["result"]["status"] == "budget_exhausted"
                   for r in denial_records)
        wrong_source = replace(q1, source_version="other-source-v1")
        wrong_exponent = replace(q1, n=q1.n + 1)
        for query in (wrong_source, wrong_exponent):
            for answer in (S.checked_purchase(query), S.direct_exact(query), table.answer(query), cache.answer(query)):
                assert answer.status == "rejected" and answer.answer is None and answer.residue is None
                assert answer.resources.total > 0
                resource_check(answer.resources)
        for constructor in (S.ExactCache, S.QuadraticResidueTable):
            try:
                constructor(limit_total=10)
                raise AssertionError("Insufficient setup cap unexpectedly accepted")
            except S.ServiceSetupError as exc:
                assert exc.resources.total <= 10
                resource_check(exc.resources)
        registry = S.registry_setup((SOURCE, S.ADAPTER_PATH))
        resource_check(registry.resources)
        assert len(registry.files) == 2
        for p, n, h in registry.files:
            data = Path(p).read_bytes()
            assert len(data) == n and hashlib.sha256(data).hexdigest() == h
        try:
            S.registry_setup((SOURCE, SOURCE))
            raise AssertionError("Duplicate source registry accepted")
        except S.ServiceSetupError as exc:
            assert exc.resources.total > 0
            resource_check(exc.resources)
        after = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        assert after == manifest
        totals = {name: sum(row[name]["resources"]["total"] for row in rows)
                  for name in ("checked", "direct", "table", "cache_cold", "cache_warm")}
        result.update({
            "status": "PASS", "checked_queries": len(rows), "positive_queries": 124,
            "table_square_reduce_evaluations": 124, "table_bitset_words": 6,
            "table_setup_resources": table.setup_resources.record(),
            "cache_setup_resources": cache.setup_resources.record(),
            "registry": registry.record(),
            "per_domain_actual_units": totals,
            "checked_max_units": max(row["checked"]["resources"]["total"] for row in rows),
            "direct_max_units": max(row["direct"]["resources"]["total"] for row in rows),
            "expert_total_units": sum(row["expert_units"] for row in rows),
            "scope": "248 distinct deterministic keys checked; cache warm pass changes request IDs. These are service-correctness/resource observations, not learner performance or an IID experiment.",
            "binding_and_caps": "PASS", "frozen_records": "PASS", "failure_costs": "PASS",
            "wrong_source_and_family": "PASS", "fifo_eviction": "PASS", "source_registry": "PASS",
            "principal_clock_credit_ns": 0,
        })
        write(out / "domain_checks.json", rows)
        write(out / "denial_checks.json", denial_records)
    except Exception as exc:
        result.update(error=repr(exc), traceback=traceback.format_exc())
    result["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write(out / "result.json", result)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {"table_setup_resources", "cache_setup_resources", "registry"}}, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
