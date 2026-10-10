"""Source-bound hashed HardState development probes; no final evaluation.

ChatGPT (GPT-6 Astra Pro), reviewer-authored implementation self-check.
All actual failures are retained. Hash collision search is a bounded public
shape fixture search, not a policy search or a private performance selection.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import traceback

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE / "source_snapshot"
sys.path.insert(0, str(SNAPSHOT / "v3/experiments"))
import p308_common as M
import p308_cnf as S
import p308_hashcache as H
import p308_broker as B
import p308_reporting as R

C = M.C
spec = importlib.util.spec_from_file_location(
    "_p308_review_pre_hash_broker", HERE / "source_before/v3/experiments/p308_broker.py")
OLD = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = OLD
spec.loader.exec_module(OLD)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rejected(kind, action):
    try:
        action()
    except kind as error:
        return {"type": type(error).__name__, "message": str(error)}
    raise AssertionError("Expected rejection did not occur")


def save(name, value):
    data = json.dumps(value, indent=2).encode() + b"\n"
    (HERE / name).write_bytes(data)
    return {"path": name, "sha256": hashlib.sha256(data).hexdigest()}


def operations(meter):
    return {(row["category"], row["operation"]): row["units"]
            for row in meter["operations"]}


def reconcile(meter):
    require(meter["total"] == sum(meter["by_category"].values())
            == sum(row["units"] for row in meter["operations"]), "Meter fails reconciliation")
    require(meter["total"] <= meter["limit_total"], "Meter overspent its limit")


def tape(count=32, *, repeated=False):
    forms = [((),), ((1,),), ((-1,), (1,)), ((-2, 1), (2,)),
             ((-3,),), ((-2, -1), (1, 2)), ((1, 2, 3),), ((-3, 1), (3,))]
    return tuple(S.make_query(f"hard-index-{i}", 3,
                              forms[0] if repeated else forms[i % len(forms)])
                 for i in range(count))


def receipt(query, solver="enumeration"):
    result = S.checked_purchase(query, limit_total=S.service_cap(query, solver), solver=solver)
    require(result.successful, "Real local fixture receipt failed")
    return result


def node_count(state):
    if state.index_kind == "linear":
        return 0
    visited = []
    for head in state._buckets:
        while head is not None:
            slot, head = head
            require(type(slot) is int and 0 <= slot < len(state.entries), "Dangling index slot")
            visited.append(slot)
    require(sorted(visited) == list(range(len(state.entries))), "Missing or repeated bucket node")
    return len(visited)


def contract_compatibility():
    legacy = B.Contract(8, 4, 6, 4, 4, "tickets", 2)
    indexed = B.Contract(8, 4, 6, 4, 4, "tickets", 2, "hashed")
    require(legacy.hard_index == "linear" and indexed.hard_index == "hashed",
            "Appending the optional contract field changed positional meaning")
    failures = []
    for value in (None, True, [], 1, "HASHED", "linear\n"):
        result = rejected(C.Rejected, lambda value=value: B.Contract(8, hard_index=value))
        failures.append({"input_repr": repr(value), "rejection": result})
    return {"legacy": legacy.record(), "new_last_positional": indexed.record(), "invalid_values": failures}


def legacy_linear():
    comparisons = []
    queries = tape(8)
    for selector in ("uniform", "tickets"):
        old = OLD.execute(S, queries, OLD.Contract(8, 4, 6, 4, 4, selector, 4), seed=308881)
        new = B.execute(S, queries, B.Contract(8, 4, 6, 4, 4, selector, 4), seed=308881)
        artifact = save(f"legacy_linear_{selector}.json", {"old": old, "new": new})
        require(old["status"] == new["status"] == "success", "Legacy comparison did not complete")
        for field in ("trace", "blocks", "invoices", "weights", "purchases", "random_bits_consumed",
                      "randomness", "scope", "all_path_funded", "expectation_theorem_eligible"):
            require(old[field] == new[field], "Default linear changed legacy field " + field)
        old_hard = old["hard_state"]
        require(all(new["hard_state"][field] == value for field, value in old_hard.items()),
                "Default linear changed hard state")
        expected_ops = operations(old["meter"])
        expected_ops[("output", "hard_index_configuration_words")] = 8
        require(operations(new["meter"]) == expected_ops, "Unexpected default-linear tariff change")
        require(new["meter"]["total"] == old["meter"]["total"] + 8
                and new["funded_cap"] == old["funded_cap"] + 8,
                "New configuration record cost/cap was not exactly eight units")
        comparisons.append({"selector": selector, "artifact": artifact,
                            "old_paid": old["meter"]["total"], "new_paid": new["meter"]["total"],
                            "old_cap": old["funded_cap"], "new_cap": new["funded_cap"]})
    return comparisons


def compare_pair(queries, selector, *, hard=True, seed=308882):
    base = B.Contract(len(queries), 4, 6, 4, 4, selector, len(queries) // 4)
    linear = B.execute(S, queries, base, seed=seed, hard=hard)
    hashed = B.execute(S, queries, replace(base, hard_index="hashed"), seed=seed, hard=hard)
    require(linear["status"] == hashed["status"] == "success", "Paired index episode failed")
    for field in ("trace", "blocks", "invoices", "weights", "purchases", "random_bits_consumed",
                  "randomness", "scope", "hard_enabled", "all_path_funded", "expectation_theorem_eligible"):
        require(linear[field] == hashed[field], "Indexing changed paired field " + field)
    for field in ("entries_retained", "active_entries", "conflicts", "withdrawals", "generation"):
        require(linear["hard_state"][field] == hashed["hard_state"][field], "Indexing changed hard state " + field)
    require(linear["index_kind"] == linear["contract"]["hard_index"] == "linear"
            and hashed["index_kind"] == hashed["contract"]["hard_index"] == "hashed",
            "Index provenance is missing or inconsistent")
    for episode in (linear, hashed):
        reconcile(episode["meter"])
    if not hard:
        require(not hashed["hard_enabled"]
                and operations(hashed["meter"]).get(("cache", "hashcache_sha256_input_block"), 0) == 0,
                "Disabled hard overrides performed live hashing")
    return linear, hashed


def paired_index_paths():
    comparisons = []
    for selector in ("uniform", "tickets"):
        for repeated in (False, True):
            queries = tape(32, repeated=repeated)
            linear, hashed = compare_pair(queries, selector)
            artifact = save(f"paired_{selector}_{'repeated' if repeated else 'varied'}.json",
                            {"linear": linear, "hashed": hashed})
            comparisons.append({"selector": selector, "repeated": repeated, "artifact": artifact,
                                "retained_keys": linear["hard_state"]["entries_retained"],
                                "linear_paid": linear["meter"]["total"],
                                "hashed_paid": hashed["meter"]["total"],
                                "provider_invoices_identical": True, "complete_trace_identical": True})
    linear, hashed = compare_pair(tape(8), "uniform", hard=False)
    artifact = save("paired_hard_disabled.json", {"linear": linear, "hashed": hashed})
    comparisons.append({"hard": False, "artifact": artifact,
                        "linear_paid": linear["meter"]["total"], "hashed_paid": hashed["meter"]["total"],
                        "hashing_units": 0, "hash_initialization_delta": hashed["meter"]["total"] - linear["meter"]["total"]})
    return comparisons


def find_collision():
    meter = C.CostMeter()
    seen = {0: {}, 1: {}}
    attempts = 0
    literals = tuple(range(-4, 0)) + tuple(range(1, 5))
    for width in range(1, 5):
        for clause in itertools.combinations(literals, width):
            for answer in (0, 1):
                # Empty clause forces UNSAT; one nonempty clause is SAT.
                # These public syntactic cases are fixture construction,
                # not hidden labels supplied to a broker or cache policy.
                clauses = ((), clause) if answer == 0 else (clause,)
                query = S.make_query(f"collision-search-{attempts}", 4, clauses)
                bucket = H.paid_key_bucket(query, meter, B.HARD_BUCKET_COUNT)
                attempts += 1
                if bucket in seen[1 - answer]:
                    pair = {answer: query, 1 - answer: seen[1 - answer][bucket]}
                    require(pair[0].claim_key != pair[1].claim_key, "Collision fixture keys coincide")
                    data = {"stage": "DEVELOPMENT", "preparation": "public shape-only fixture search",
                            "bucket": bucket, "attempts": attempts,
                            "queries": [pair[a].record() for a in (0, 1)], "meter": meter.snapshot()}
                    artifact = save("collision_fixture_before_receipts.json", data)
                    return pair[0], pair[1], bucket, artifact
                seen[answer].setdefault(bucket, query)
    raise AssertionError("Declared finite fixture search found no cross-answer bucket collision")


def real_bucket_collision_and_versions():
    false_query, true_query, bucket, fixture = find_collision()
    rf, rt = receipt(false_query), receipt(true_query)
    require(rf.answer == 0 and rt.answer == 1, "Real receipt disproved the simple collision fixture")
    outcomes = []
    for kind in ("linear", "hashed"):
        meter = C.CostMeter()
        scope = (S.SEMANTICS_VERSION, S.SOURCE_VERSION, "collision-epoch")
        state = B.HardState(meter, 4, scope, index_kind=kind)
        state.admit(false_query, rf)
        require(state.lookup(true_query)["status"] == "unresolved",
                "Bucket collision authorized another complete key")
        state.admit(true_query, rt)
        require(state.lookup(false_query)["answer"] == 0 and state.lookup(true_query)["answer"] == 1,
                "Collision chain lost a correct answer")
        rebound = S.make_query("same-key-new-request", 4, false_query.clauses)
        rebound_receipt = receipt(rebound)
        state.admit(rebound, rebound_receipt)
        require(len(state.entries) == 2 and state.lookup(rebound)["answer"] == 0,
                "Request identity changed semantic hard-key lookup or duplicate retention")
        # This direct store test injects a contradictory claimed receipt to
        # exercise conflict semantics. The actual source did not produce it.
        conflict = rejected(C.Rejected, lambda: state.admit(false_query, replace(rf, answer=1)))
        require(state.lookup(false_query)["status"] == "conflict"
                and state.lookup(true_query)["answer"] == 1, "Conflict escaped its complete coordinate")
        changed_scope = (S.SEMANTICS_VERSION, S.SOURCE_VERSION, "next-epoch")
        state.invalidate(changed_scope)
        require(state.lookup(false_query)["status"] == state.lookup(true_query)["status"] == "stale",
                "Withdrawal hid or revived a historical key")
        state.invalidate(scope)
        require(state.lookup(false_query)["status"] == "stale", "Returning to an old scope revived a generation")
        state.admit(false_query, rf)
        require(state.lookup(false_query)["answer"] == 0 and state.lookup(true_query)["status"] == "stale",
                "New current admission did not supersede only its old coordinate")
        state.admit(true_query, rt)
        require(len(state.entries) == 4 and state.record()["active_entries"] == 2,
                "Old generations were discarded from capacity accounting")
        fresh = S.make_query("capacity-extra", 4, ())
        failure = rejected(C.BudgetExceeded, lambda: state.admit(fresh, receipt(fresh)))
        require(len(state.entries) == 4, "Capacity rejection changed entries")
        count = node_count(state)
        snapshot = meter.snapshot()
        reconcile(snapshot)
        if kind == "hashed":
            require(operations(snapshot).get(("cache", "hard_hash_bucket_collision_step"), 0) > 0,
                    "Real bucket collisions were not charged")
        outcomes.append({"index": kind, "record": state.record(), "node_count": count,
                         "conflict": conflict, "capacity_failure": failure, "meter": snapshot})
    artifact = save("collision_generation_outcomes.json", outcomes)
    return {"fixture": fixture, "outcomes": artifact, "bucket": bucket,
            "same_bucket_distinct_answers": [rf.answer, rt.answer],
            "summaries": [{"index": row["index"], "state": row["record"],
                           "paid": row["meter"]["total"], "node_count": row["node_count"]} for row in outcomes]}


def atomic_index_commit():
    query = tape(4, repeated=True)[0]
    checked = receipt(query)
    scope = (S.SEMANTICS_VERSION, S.SOURCE_VERSION, "atomic-epoch")
    full_meter = C.CostMeter()
    full = B.HardState(full_meter, 4, scope, index_kind="hashed")
    full.admit(query, checked)
    exact_total = full_meter.total
    short_meter = C.CostMeter(exact_total - 1)
    short = B.HardState(short_meter, 4, scope, index_kind="hashed")
    failure = rejected(C.BudgetExceeded, lambda: short.admit(query, checked))
    require(len(short.entries) == 0 and all(head is None for head in short._buckets)
            and node_count(short) == 0, "Denied atomic commit left an orphan entry or bucket node")
    reconcile(short_meter.snapshot())
    return {"full_commit_total": exact_total, "short_limit": exact_total - 1,
            "short_spent": short_meter.total, "failure": failure, "state": short.record(),
            "meter": short_meter.snapshot()}


def funding_and_failure():
    outcomes = []
    queries = tape(16)
    for selector in ("uniform", "tickets"):
        contract = B.Contract(16, 4, 6, 4, 4, selector, 4, "hashed")
        cap = B.funded_cap(S, queries, contract)
        exact = B.execute(S, queries, contract, seed=308883, unit_limit=cap)
        require(exact["status"] == "success" and exact["all_path_funded"]
                and exact["expectation_theorem_eligible"], "Exact advertised hashed cap did not fund all work")
        reserve_headroom = max(S.service_cap(query, "enumeration") for query in queries)
        limited_budget = exact["meter"]["total"] + reserve_headroom
        limited = B.execute(S, queries, contract, seed=308883, unit_limit=limited_budget)
        require(limited_budget < cap and limited["status"] == "success"
                and not limited["all_path_funded"] and not limited["expectation_theorem_eligible"],
                "Completed sub-cap hashed path acquired all-path eligibility")
        denied = B.execute(S, queries, contract, seed=308883, unit_limit=1)
        provider_failed = B.execute(S, queries, contract, seed=308883, provider_limit=0)
        capacity_failed = B.execute(S, queries, replace(contract, hard_capacity=0), seed=308883)
        for episode in (denied, provider_failed, capacity_failed):
            require(episode["status"] == "failed" and not episode["successful_quota_contract"]
                    and not episode["expectation_theorem_eligible"], "Failed hashed path retained a theorem flag")
            reconcile(episode["meter"])
        require(provider_failed["invoices"] and provider_failed["invoices"][-1]["status"] != "success",
                "Failed provider invoice disappeared")
        require(capacity_failed["purchases"] == 1 and capacity_failed["invoices"][-1]["checked"] is True,
                "Hard capacity failure erased an already paid checked purchase")
        artifact = save(f"funding_{selector}.json", {"exact_cap": exact, "limited": limited,
                        "denied": denied, "provider_failed": provider_failed, "capacity_failed": capacity_failed})
        outcomes.append({"selector": selector, "artifact": artifact, "funded_cap": cap,
                         "actual_paid": exact["meter"]["total"], "limited_budget": limited_budget,
                         "limited_eligible": limited["expectation_theorem_eligible"],
                         "provider_failure_paid": provider_failed["meter"]["total"],
                         "capacity_failure_paid": capacity_failed["meter"]["total"]})
    return outcomes


def unfunded_withdrawal():
    queries = tape(4, repeated=True)
    contract = B.Contract(4, 4, 6, 4, 4, "uniform", 4, "hashed")
    meter = C.CostMeter(1_000_000)
    bits = C.BitTape((0,), contract.random_bits, meter, provenance="explicit-zero-development-words")
    broker = B.Broker(S, contract, meter, bits,
                      (S.SEMANTICS_VERSION, S.SOURCE_VERSION, "withdraw-epoch"))
    broker.begin_block(queries)
    for _ in queries:
        broker.close(broker.issue())
    require(broker.record()["status"] == "success", "Withdrawal fixture did not first complete")
    # Explicit test-only spend exhausts the provided parent budget.
    meter.pay("controller", "test_only_budget_exhaustion", meter.limit_total - meter.total)
    failure = rejected(C.BudgetExceeded, lambda: broker.withdraw(
        (S.SEMANTICS_VERSION, S.SOURCE_VERSION, "withdrawn-epoch")))
    record = broker.record()
    require(record["status"] == "failed" and not record["successful_quota_contract"],
            "Unfunded hashed withdrawal left a live successful warrant")
    blocked = rejected(C.Rejected, broker.issue)
    require(node_count(broker.hard) == len(broker.hard.entries), "Withdrawal corrupted historical index")
    artifact = save("unfunded_hashed_withdrawal.json", {"record": record, "meter": meter.snapshot()})
    return {"failure": failure, "blocked_issue": blocked, "artifact": artifact,
            "historical_entries": len(broker.hard.entries), "failed": broker.failed}


def maximal_key_precision():
    queries = tuple(S.make_query(f"maximum-index-{i}", 12,
                                 [(-4, -3, -2, -1)] * 64,
                                 source_version="s" * 128) for i in range(2))
    contract = B.Contract(2, 2, 6, 32, 32, "uniform", 1, "hashed")
    cap = B.funded_cap(S, queries, contract, solver="dpll")
    episode = B.execute(S, queries, contract, seed=308775,
                        purchase_solver="dpll", unit_limit=cap)
    artifact = save("maximum_key_precision.json", episode)
    require(episode["status"] == "success" and episode["all_path_funded"],
            "Maximum key/precision hashed path did not complete at its cap")
    require(queries[0].key_words == 343, "Maximum shape key no longer meets intended size")
    reconcile(episode["meter"])
    return {"artifact": artifact, "key_words": queries[0].key_words, "funded_cap": cap,
            "actual_paid": episode["meter"]["total"], "peak_numeric_bits": episode["peak_numeric_bits"],
            "hash_block_units": operations(episode["meter"])[("cache", "hashcache_sha256_input_block")]}


def reporter_index_invariance():
    linear, hashed = compare_pair(tape(8), "tickets", seed=308884)
    left = R.report_owned_episode(S, linear, basis="base", radius="fixed")
    right = R.report_owned_episode(S, hashed, basis="base", radius="fixed")
    artifact = save("reporter_index_invariance.json", {"linear_episode": linear, "hashed_episode": hashed,
                                                       "linear_report": left, "hashed_report": right})
    require(left["status"] == right["status"] == "success", "Reporter rejected the new explicit index schema")
    for field in ("reference_centers", "live_centers", "corrections", "Q", "R", "sampling_radius",
                  "action_radius", "n_live", "intervals", "deterministic_envelopes", "confidence_eligible"):
        require(left[field] == right[field], "Indexing changed report field " + field)
    return {"artifact": artifact, "identical_statistical_fields": True,
            "linear_report_paid": left["meter"]["total"], "hashed_report_paid": right["meter"]["total"],
            "scope": "Index-invariance check only; new snapshot/grid extensions are reviewed separately"}


def main():
    started = datetime.now(timezone.utc).isoformat()
    results = []
    for case in (contract_compatibility, legacy_linear, paired_index_paths,
                 real_bucket_collision_and_versions, atomic_index_commit,
                 funding_and_failure, unfunded_withdrawal,
                 maximal_key_precision, reporter_index_invariance):
        try:
            results.append({"case": case.__name__, "status": "PASS", "detail": case()})
        except Exception as error:
            results.append({"case": case.__name__, "status": "FAIL", "exception": type(error).__name__,
                            "message": str(error), "traceback": traceback.format_exc()})
    result = {"stage": "DEVELOPMENT", "started_utc": started,
              "finished_utc": datetime.now(timezone.utc).isoformat(),
              "source_manifest": "source_manifest.json", "script": Path(__file__).name,
              "review_attribution": "reviewer-authored implementation self-check",
              "principal_clock_credit_seconds": 0,
              "passed": sum(row["status"] == "PASS" for row in results),
              "failed": sum(row["status"] == "FAIL" for row in results), "results": results}
    save("results.json", result)
    print(json.dumps({key: result[key] for key in ("stage", "passed", "failed")}))
    for row in results:
        print(row["case"], row["status"], row.get("message", ""))
    raise SystemExit(int(result["failed"] != 0))


if __name__ == "__main__":
    main()
