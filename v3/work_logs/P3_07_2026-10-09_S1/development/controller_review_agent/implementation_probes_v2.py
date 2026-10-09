"""Focused independent checks of the frozen P3-07 v2 implementation.

Uses preserved source snapshots and saved run_v2 evidence. No full driver
rerun, no edits of reviewed sources, zero principal Research90 credit.
"""
from collections import Counter
from dataclasses import replace
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUN = HERE.parent / "run_v2"
SNAPSHOT = HERE / "source_snapshot_v2"
SPEC = importlib.util.spec_from_file_location("controller_review_driver_v2",
    SNAPSHOT / "07_paid_reasoning_development.py")
D = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = D
SPEC.loader.exec_module(D)
C, A = D.C, D.A


def read(name):
    return json.loads((RUN / name).read_text())


def profile_from_record(raw):
    return C.Profile(C.Scope(**raw["scope"]), tuple(raw["names"]),
        tuple(raw["feature_names"]), tuple(tuple(tuple(pair) for pair in row) for row in raw["ranges"]),
        tuple(tuple(row) for row in raw["sums"]), raw["n"], tuple(raw["checkpoints"]),
        F(raw["delta"]), tuple(raw["setup_resources"]))


def capture(fn):
    try:
        return dict(returned=True, value=fn())
    except Exception as exc:
        return dict(returned=False, exception=type(exc).__name__, message=str(exc))


def meter_invariants(snapshot, cap):
    assert snapshot["total"] == sum(snapshot["by_category"].values())
    assert 0 <= snapshot["total"] <= cap == snapshot["limit_total"]
    assert all(snapshot["by_category"][c] <= snapshot["category_limits"][c] for c in A.CATEGORIES)
    if "partitions" in snapshot:
        assert sum(part["limit_total"] for part in snapshot["partitions"]) <= cap
        assert snapshot["total"] == sum(part["total"] for part in snapshot["partitions"])
        for part in snapshot["partitions"]:
            meter_invariants(part, part["limit_total"])


def main():
    manifest = read("manifest.json")
    for name, expected in manifest["source_hashes"].items():
        assert hashlib.sha256((SNAPSHOT / name).read_bytes()).hexdigest() == expected
    profile = profile_from_record(read("profile_1024.json"))
    assert profile.identity == C.digest(profile.record())

    assessment_rows = []
    caps = (0, 1, 64, 256, 257, 258, 320, 321, 1296, 1297,
            1936, 1937, 2017, 2180, 3273, 3860, 3861, 20000)
    for cap in caps:
        result = C.select(profile, profile.scope, D.PRICES["high"], 1,
                          assessment_limit=cap)
        meter_invariants(result["meter"], cap)
        if cap == 0:
            assert result["policy"] is None and result["profile_id"] is None
        elif cap < C.SELECT_FINAL_UNITS + 65:
            assert result["policy"] == "fallback" and result["profile_id"] is None
        if result["assessment_cost"] is not None:
            expected_cost = sum((p * result["meter"]["by_category"][c]
                for p, c in zip(D.PRICES["high"][3:], A.CATEGORIES)), F(0))
            assert F(result["assessment_cost"]) == expected_cost
        assessment_rows.append(dict(cap=cap, kind=result["kind"],
            policy=result["policy"], total=result["meter"]["total"],
            profile_identity_returned=result["profile_id"] is not None,
            priced_certificate_returned=result["assessment_cost"] is not None))

    # A valid generic Profile can have another catalogue. Exhaustion before
    # catalogue validation must not turn its first name into the fallback.
    names = (profile.names[1], profile.names[0]) + profile.names[2:]
    wrong_catalogue = replace(profile, names=names)
    admission_gap = []
    for cap in (320, 321, 1296, 1297, 20000):
        check = capture(lambda cap=cap: C.select(wrong_catalogue, wrong_catalogue.scope,
            D.PRICES["high"], 1, assessment_limit=cap))
        if check["returned"]:
            result = check.pop("value")
            check.update(kind=result["kind"], policy=result["policy"],
                conditional_lower=result["conditional_batch_lower_gain"],
                profile_id=result["profile_id"], total=result["meter"]["total"])
        admission_gap.append(dict(cap=cap, **check))

    original_adapter = A.Adapter
    observed = []
    class ObservedAdapter(original_adapter):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            observed.append(self)
    A.Adapter = ObservedAdapter
    policy_rows = []
    try:
        queries = (A.Query("review", 7, 47, 97, 1),
                   A.Query("x" * 128, 7, 191, 97, 1, source_version="s" * 128))
        for qi, query in enumerate(queries):
            for policy in (C.CATALOGUE[0], C.CATALOGUE[2], C.CATALOGUE[3], C.CATALOGUE[-1]):
                for cap in (0, 1, 2, 64, 65, 66, 67, 120, 160, 190, 256, 400, 477, 512, 1024):
                    result = C.run_policy(query, policy, limit=cap)
                    meter_invariants(result["meter"], cap)
                    assert observed[-1].public_state()["active_jobs"] == 0
                    if cap == 0:
                        assert result["initial_report"] is None and result["status"] == "no_output_budget"
                    if result["answer"] is not None:
                        assert result["action"] == int(pow(query.a, query.n, query.m) == query.r)
                    if cap == 1024 and policy is C.CATALOGUE[-1]:
                        assert result["answer"] is not None
                    policy_rows.append(dict(query=qi, policy=policy.name, cap=cap,
                        action=result["action"], status=result["status"], initial_report=result["initial_report"],
                        total=result["meter"]["total"], cancelled=result["meter"]["operations"].get("storage.cancelled_job_release", 0),
                        completed=result["meter"]["operations"].get("storage.completed_job_release", 0)))
    finally:
        A.Adapter = original_adapter

    # The former accepted 2048-bit setup input is now outside the documented
    # 256-bit domain; exercise one admitted high-denominator edge as well.
    setup_rows = []
    for name, setup in (("maximum_256bit_fraction", F(2**256-1, 2**256-189)),
                        ("former_2048bit_counterexample", F(1, 2**2048-159))):
        result = capture(lambda setup=setup: C.select(profile, profile.scope,
            D.PRICES["high"], 10000, setup_to_recover=setup))
        if result["returned"]:
            outcome = result.pop("value")
            numbers = [F(outcome[key]) for key in ("lower_gain_per_query", "conditional_batch_lower_gain",
                "assessment_cost", "setup_to_recover", "all_in_lower_gain")]
            if outcome["scores"]:
                numbers += [F(value) for value in outcome["scores"].values()]
            bits = max(max(value.numerator.bit_length(), value.denominator.bit_length()) for value in numbers)
            assert bits <= C.MAX_ARITHMETIC_BITS
            result.update(max_returned_rational_bits=bits,
                paid_final_bundle=outcome["meter"]["operations"]["assessment.final_bounded_arithmetic_identity_and_readout"])
        setup_rows.append(dict(case=name, **result))

    expected_ranges = tuple(C.paired_ranges(policy) for policy in C.CATALOGUE)
    cumulative = [[0] * len(C.FEATURES) for _ in C.CATALOGUE]
    resource_sum = Counter({c: 0 for c in A.CATEGORIES})
    prefixes, raw_by_index = [], {}
    population_rows = [json.loads(line) for line in (RUN / "population_rows.jsonl").read_text().splitlines()]
    assert len(population_rows) == len(D.POPULATION) == 248
    population_sums = [[0] * len(C.FEATURES) for _ in C.CATALOGUE]
    population_paired_sums = [[0] * len(C.FEATURES) for _ in C.CATALOGUE]
    for row in population_rows:
        raw_by_index[row["index"]] = row
        for i, values in enumerate(row["features"]):
            assert row["paired"][i] == [b-x for b,x in zip(row["features"][0], values)]
            for j, value in enumerate(values):
                population_sums[i][j] += value
                population_paired_sums[i][j] += row["paired"][i][j]
    profile_rows = [json.loads(line) for line in (RUN / "profile_rows.jsonl").read_text().splitlines()]
    profile_rng = random.Random(D.PROFILE_SEED)
    for n, row in enumerate(profile_rows, 1):
        assert row["index"] == profile_rng.randrange(len(D.POPULATION))
        reference = raw_by_index[row["index"]]
        for key in ("query", "label", "features", "paired", "actions", "statuses", "initial_reports"):
            assert row[key] == reference[key]
        for i, values in enumerate(row["paired"]):
            for j, value in enumerate(values):
                lo, hi = expected_ranges[i][j]
                assert lo <= value <= hi
                cumulative[i][j] += value
        for values in row["features"]:
            resource_sum.update(dict(zip(A.CATEGORIES, values[3:])))
        if n in D.CHECKPOINTS:
            saved = profile_from_record(read(f"profile_{n}.json"))
            assert saved.sums == tuple(tuple(values) for values in cumulative)
            assert saved.ranges == expected_ranges
            prefixes.append(n)
    assert len(profile_rows) == 1024
    run_result = read("result.json")
    assert dict(resource_sum) == run_result["profile_setup"]["executed_policy_resources"]
    for category, quantity in zip(A.CATEGORIES, profile.setup_resources):
        assert quantity == resource_sum[category] + run_result["profile_setup"]["profile_build_meter"]["by_category"][category]

    population = read("population_exact.json")
    for i, policy in enumerate(C.CATALOGUE):
        assert tuple(F(value) for value in population["feature_means"][policy.name]) == tuple(F(value, 248) for value in population_sums[i])
        assert tuple(F(value) for value in population["paired_means"][policy.name]) == tuple(F(value, 248) for value in population_paired_sums[i])
    radius_rows = []
    for n in D.CHECKPOINTS:
        saved = profile_from_record(read(f"profile_{n}.json"))
        intervals, radius = C.profile_intervals(saved, saved.scope, A.Meter(20000))
        r, k = F(radius["r"]), radius["k"]
        assert 2*n*r*r >= k and F(2*22*4, 1<<k) <= F(1,20)
        assert all(lo <= F(population_paired_sums[i][j], 248) <= hi
            for i, row in enumerate(intervals) for j, (lo,hi) in enumerate(row))
        radius_rows.append(dict(n=n, radius=str(r), k=k, simultaneous_cells=22,
            simultaneous_prefixes=4, exact_population_coverage=True))

    selections = read("selections.json")
    for row in selections:
        result, prices = row["selection"], tuple(F(v) for v in row["prices"])
        meter_invariants(result["meter"], 20000)
        assert F(result["assessment_cost"]) == sum((prices[j+3]*result["meter"]["by_category"][c]
            for j,c in enumerate(A.CATEGORIES)), F(0))
        assert F(result["all_in_lower_gain"]) == F(result["conditional_batch_lower_gain"])-F(result["assessment_cost"])-F(result["setup_to_recover"])
        assert F(result["conditional_batch_lower_gain"]) <= F(row["true_batch_gain_before_assessment"])
        assert F(result["all_in_lower_gain"]) <= F(row["true_all_in_gain"])
        assert row["ordinary_controller_equal"] is True

    audit = read("self_audit.json")
    audit_profile = profile_from_record(audit["audit_profile"])
    audit_sums = [0] * len(C.FEATURES)
    audit_rng, audit_rows, audit_costs = random.Random(D.AUDIT_SEED), 0, Counter()
    prices = tuple(F(v) for v in audit["closure"]["prices"])
    for line in (RUN / "self_audit_rows.jsonl").read_text().splitlines():
        row = json.loads(line)
        audit_rows += 1
        assert row["indices"] == [audit_rng.randrange(len(D.POPULATION)) for _ in range(16)]
        assert row["paired"] == [b-x for b,x in zip(row["baseline_features"], row["controller_features"])]
        # Here the frozen selected policy is full_fallback: the query-level
        # exact comparator must have precisely the same raw outcomes/costs.
        assert row["controller_features"][:3] == row["charged_exact_features"][:3]
        for j, category in enumerate(A.CATEGORIES):
            delta = row["controller_features"][j+3] - row["charged_exact_features"][j+3]
            if category not in ("assessment", "storage"):
                assert delta == 0
        for j, value in enumerate(row["paired"]):
            lo, hi = audit_profile.ranges[0][j]
            assert lo <= value <= hi
            audit_sums[j] += value
        for name, key in (("controller", "controller_features"), ("fallback", "baseline_features"), ("charged_exact", "charged_exact_features")):
            audit_costs[name] += sum((F(v)*p for v,p in zip(row[key], prices)), F(0))
    assert audit_rows == 256 and tuple(audit_sums) == audit_profile.sums[0]
    assert dict(audit_costs) == {k:F(v) for k,v in audit["observed_total_costs"].items()}
    closure = dict(audit["closure"])
    closure_id = closure.pop("identity")
    closure.pop("frozen_utc_before_first_audit_row")
    assert C.digest(closure) == closure_id
    assert closure["profile_id"] == profile.identity
    assert closure["source_hashes"] == manifest["source_hashes"]

    return dict(reviewed_source_hashes=manifest["source_hashes"],
        assessment_budget_edges=assessment_rows, prevalidation_exhaustion_catalogue_gap=admission_gap,
        policy_budget_cases=policy_rows, no_pending_jobs_at_return=True,
        setup_arithmetic_boundary=setup_rows, radius_checks=radius_rows,
        saved_evidence=dict(profile_rows=1024, population_rows=248, exact_prefix_sums=prefixes,
            profile_rows_match_public_population=True, profile_procurement_resources_match=True,
            seeds_match_manifest=True, selections_reconciled=len(selections),
            audit_rows=audit_rows, exact_audit_sums=True, audit_costs_reconciled=True,
            audit_source_and_profile_closure_valid=True),
        scope="Frozen v2 focused diagnostics and saved-data reconciliation; no full run or old-suite rerun.",
        principal_research90_credit_seconds=0)


if __name__ == "__main__":
    result = main()
    with (HERE / "implementation_probe_results_v2.json").open("x") as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps({key:value for key,value in result.items() if key != "policy_budget_cases"}, sort_keys=True, indent=2))
