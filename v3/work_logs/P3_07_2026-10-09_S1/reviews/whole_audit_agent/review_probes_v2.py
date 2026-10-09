"""Targeted same-model, nonblind P3-07 v3 / whole-audit-v2 review.

Uses preserved sources and saved population rows. No full solver/driver rerun.
All output is new in this directory; principal Research90 credit is zero.
"""
from collections import Counter
from dataclasses import replace
from datetime import datetime
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import isqrt
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
WORKLOG = HERE.parent.parent
ROOT = WORKLOG.parents[2]
RUN = WORKLOG / "development/whole_procedure_run_v2"
POP_RUN = WORKLOG / "development/run_v3"
SNAPSHOT = RUN / "sources"
SPEC = importlib.util.spec_from_file_location("whole_review_frozen_v2", SNAPSHOT / "07_whole_procedure_audit.py")
W = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = W
SPEC.loader.exec_module(W)
D, C, A = W.D, W.C, W.A


def read(path):
    return json.loads(path.read_text())


def lines(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def filehash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_profile(raw):
    return C.Profile(C.Scope(**raw["scope"]), tuple(raw["names"]), tuple(raw["feature_names"]),
        tuple(tuple(tuple(pair) for pair in row) for row in raw["ranges"]),
        tuple(tuple(row) for row in raw["sums"]), raw["n"], tuple(raw["checkpoints"]),
        F(raw["delta"]), tuple(raw["setup_resources"]))


def zero():
    return Counter({c: 0 for c in A.CATEGORIES})


def resource_values(features):
    return dict(zip(A.CATEGORIES, features[3:]))


def meter_checks(meter):
    assert meter["total"] == sum(meter["by_category"].values()) == sum(meter["operations"].values())
    assert meter["remaining"] == meter["limit_total"] - meter["total"] >= 0
    totals = zero()
    for key, value in meter["operations"].items():
        totals[key.split(".", 1)[0]] += value
    assert totals == meter["by_category"]
    assert all(0 <= meter["by_category"][c] <= meter["category_limits"][c] for c in A.CATEGORIES)
    if "partitions" in meter:
        assert sum(p["limit_total"] for p in meter["partitions"]) <= meter["limit_total"]
        assert sum(p["total"] for p in meter["partitions"]) == meter["total"]
        merged = zero()
        for part in meter["partitions"]:
            meter_checks(part)
            merged.update(part["by_category"])
        assert merged == meter["by_category"]


def independent_radius(n, cells, delta, checkpoints):
    k = 0
    while F(2 * max(1, cells) * checkpoints, 2**k) > delta:
        k += 1
    scaled_square = F(k * 2**32, 2 * n)
    root = isqrt(scaled_square.numerator // scaled_square.denominator)
    if root**2 < scaled_square:
        root += 1
    radius = F(root, 2**16)
    assert 2 * n * radius**2 >= k
    assert 2 * n * (radius - F(1, 2**16))**2 < k
    assert F(2 * max(1, cells) * checkpoints, 2**k) <= delta
    return radius, k


def independent_scores(raw, prices):
    cells = sum(lo != hi for row in raw["ranges"] for lo, hi in row)
    radius, k = independent_radius(raw["n"], cells, F(raw["delta"]), len(raw["checkpoints"]))
    intervals, scores = [], []
    for bounds, sums in zip(raw["ranges"], raw["sums"]):
        row = []
        for (lo, hi), value in zip(bounds, sums):
            mean = F(value, raw["n"])
            row.append((max(F(lo), mean - (hi-lo)*radius), min(F(hi), mean + (hi-lo)*radius)))
        intervals.append(row)
        scores.append(sum((price * (lo if price >= 0 else hi) for price, (lo, hi) in zip(prices, row)), F(0)))
    return intervals, scores, radius, k, cells


def main():
    closure = read(RUN / "closure.json")
    result = read(RUN / "result.json")
    plan = read(WORKLOG / "development/whole_procedure_plan_v2.json")
    base_plan = read(WORKLOG / "development/whole_procedure_plan_v1.json")
    source_hashes = closure["source_hashes"]
    root_hashes = {}
    for name, expected in source_hashes.items():
        assert filehash(SNAPSHOT / name) == expected
        root_hashes[name] = filehash(ROOT / "v3/checks" / name)
        assert root_hashes[name] == expected
        if (POP_RUN / "sources" / name).exists():
            assert filehash(POP_RUN / "sources" / name) == expected
    assert source_hashes["07_computation_adapter.py"] == "06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615"
    assert result["closure"] == closure
    plain_closure = dict(closure)
    closure_id = plain_closure.pop("identity")
    assert digest(plain_closure) == closure_id
    assert datetime.fromisoformat(plan["frozen_utc"]) < datetime.fromisoformat(closure["frozen_utc_before_first_episode"])

    prices = tuple(F(value) for value in closure["prices"])
    assert prices == (F(100), F(100), F(20)) + (F(1, 1000),) * 11
    profile_n, horizon, audit_n = 64, 64, 256
    assert (closure["profile_n"], closure["horizon"], closure["audit_n"]) == (profile_n, horizon, audit_n)
    resource_cap = profile_n*6*1024 + 150000 + 20000 + horizon*1024
    low, high = -80*horizon - F(resource_cap, 1000), F(20*horizon)
    assert resource_cap == closure["whole_resource_cap"] == base_plan["single_episode_controller_resource_upper"] == 628752
    assert list(map(str, (low, high))) == closure["scalar_range"] == base_plan["paired_scalar_loss_range"]

    population_rows = lines(POP_RUN / "population_rows.jsonl")
    population = {row["index"]: row for row in population_rows}
    public_population = tuple((p, a) for p in (17, 31, 47, 61, 97) for a in range(1, p))
    assert len(population_rows) == len(population) == len(public_population) == 248
    assert tuple(D.POPULATION) == public_population
    expected_ranges = tuple(C.paired_ranges(policy) for policy in C.CATALOGUE)
    population_sums = [[0]*14 for _ in range(6)]
    max_policy_resource = 0
    for index, (p, a) in enumerate(public_population):
        row = population[index]
        assert row["query"] == {"a": a, "n": (p-1)//2, "m": p, "r": 1}
        assert row["label"] in (0, 1) and row["actions"][-1] == row["label"]
        assert row["statuses"][-1] == "checked_answer"
        assert row["initial_reports"] == ["1/2"]*6
        for pi, features in enumerate(row["features"]):
            action = row["actions"][pi]
            assert features[:3] == [int(action == 1 and row["label"] == 0), int(action == 0 and row["label"] == 1), int(action is None)]
            assert row["paired"][pi] == [base - value for base, value in zip(row["features"][0], features)]
            assert all(type(value) is int and value >= 0 for value in features[3:])
            max_policy_resource = max(max_policy_resource, sum(features[3:]))
            assert sum(features[3:]) <= 1024
            for j, value in enumerate(row["paired"][pi]):
                lo, hi = expected_ranges[pi][j]
                assert lo <= value <= hi
                population_sums[pi][j] += value
            # The common public prefix proves resource saving is never positive.
            assert all(base <= value for base, value in zip(row["features"][0][3:], features[3:]))

    changed = dict(source_hashes)
    changed["07_paid_reasoning_development.py"] = "0"*64
    def whole_scope(hashes):
        joint = digest({name: hashes[name] for name in ("07_paid_reasoning_development.py", "07_whole_procedure_audit.py")})
        return replace(D.actual_scope(hashes), law=D.LAW + ";joint-generator-sha256:" + joint)
    scope = whole_scope(source_hashes)
    assert scope.record() == closure["profile_scope"]
    assert D.actual_scope(source_hashes) != D.actual_scope(changed)
    assert whole_scope(source_hashes) != whole_scope(changed)
    changed_wrapper = dict(source_hashes)
    changed_wrapper["07_whole_procedure_audit.py"] = "0"*64
    assert whole_scope(source_hashes) != whole_scope(changed_wrapper)
    assert scope.law.endswith("abc70b2a81de8e3ee0521d5f898ffe20710574947f0aeacd03d3f3f76d0a4ff4")

    profile_closures = lines(RUN / "profile_closures.jsonl")
    episode_rows = lines(RUN / "episode_rows.jsonl")
    assert len(profile_closures) == len(episode_rows) == audit_n
    source_words = sum(((SNAPSHOT / name).stat().st_size + 7)//8 for name in source_hashes)
    builder_ops = {
        "profile.whole_source_read_and_hash_words": 2*source_words,
        "profile.public_population_construction": 4*248,
        "storage.public_population_word_write": 2*248,
        "profile.builder_bounded_metadata_admission": 8192,
        "profile.uniform_profile_index_draw": profile_n,
        "storage.profile_query_word_read": 4*profile_n,
        "profile.checked_label_and_feature_interpretation": 4*14*6*profile_n,
        "profile.paired_cell_check_add": 3*14*6*profile_n,
        "storage.paired_cell_read_write": 2*14*6*profile_n,
        "profile.profile_count_increment": profile_n,
        "profile.freeze_validate_copy_and_hash_words": 2*8192,
        "storage.freeze_retained_profile_words": 8192,
    }
    outer_ops = {
        "profile.whole_profile_closure_copy_and_hash": 2*8192,
        "storage.whole_profile_closure_retention": 8192,
        "profile.fresh_deployment_index_draw": horizon,
        "profile.whole_episode_feature_and_cost_readout": 4*3*14*horizon,
        "profile.whole_episode_scalar_sum_and_range_check": 64,
        "storage.whole_episode_record_retention": 8192,
    }
    rng = random.Random(closure["audit_seed"])
    total_gain = total_controller = total_baseline = total_exact = F(0)
    startup_meter = result["outer_startup_meter"]
    meter_checks(startup_meter)
    assert startup_meter["operations"] == {"profile.outer_source_registry_read_hash_words": 2*source_words, "profile.outer_global_closure_construct_hash": 16384, "storage.outer_global_closure_retention": 8192}
    assert startup_meter["total"] == 45598 and startup_meter["events"] == 1 and startup_meter["denials"] == 0
    outer_bill = Counter(startup_meter["by_category"])
    gains, caps_used, setup_costs, interval_coverage = [], [], [], []
    policies = Counter()
    for episode, (pc, row) in enumerate(zip(profile_closures, episode_rows)):
        assert pc["episode"] == row["episode"] == episode
        assert pc["procurement"]["indices"] == [rng.randrange(248) for _ in range(profile_n)]
        assert row["cohort_indices"] == [rng.randrange(248) for _ in range(horizon)]
        assert datetime.fromisoformat(closure["frozen_utc_before_first_episode"]) < datetime.fromisoformat(pc["frozen_utc_before_deployment"]) < datetime.fromisoformat(result["finished_utc"])
        if episode:
            assert pc["frozen_utc_before_deployment"] > profile_closures[episode-1]["frozen_utc_before_deployment"]
        raw = pc["profile"]
        profile = frozen_profile(raw)
        assert raw["scope"] == scope.record() and raw["n"] == profile_n
        assert raw["checkpoints"] == [profile_n] and raw["delta"] == "1/20"
        assert pc["profile_id"] == row["profile_id"] == digest(raw) == profile.identity
        assert pc["procurement"]["kind"] == row["profile_kind"] == "acquired"
        sums = [[0]*14 for _ in range(6)]
        rollout = zero()
        for index in pc["procurement"]["indices"]:
            sampled = population[index]
            for pi in range(6):
                rollout.update(resource_values(sampled["features"][pi]))
                for j, value in enumerate(sampled["paired"][pi]):
                    sums[pi][j] += value
        assert sums == raw["sums"]
        assert rollout == pc["procurement"]["policy_rollout_resources"]
        build_meter = pc["procurement"]["builder_meter"]
        meter_checks(build_meter)
        assert build_meter["operations"] == builder_ops and build_meter["events"] == 195 and build_meter["denials"] == 0
        setup = rollout.copy()
        setup.update(build_meter["by_category"])
        assert setup == pc["procurement"]["total_resources"] == row["profile_resources"]
        assert list(setup[c] for c in A.CATEGORIES) == raw["setup_resources"]
        setup_costs.append(F(sum(setup.values()), 1000))

        selection = pc["selection"]
        meter_checks(selection["meter"])
        assert selection["profile_id"] == profile.identity and selection["profile_scope_validated"] is True
        assert selection["scope"] == scope.record() and selection["horizon"] == horizon
        assert selection["kind"] == "assessed" and selection["setup_to_recover"] == "0"
        intervals, scores, radius, k, cells = independent_scores(raw, prices)
        assert selection["scores"] == dict(zip(raw["names"], map(str, scores)))
        assert selection["radius"] == {"r": str(radius), "k": k, "nonconstant_cells": cells, "checkpoints": 1, "tail_budget": "1/20"}
        assert cells == 22
        selected_index = max(range(6), key=lambda i: (scores[i], -i))
        assert selection["policy"] == row["policy"] == raw["names"][selected_index]
        expected_assessment = sum((prices[j+3]*selection["meter"]["by_category"][c] for j, c in enumerate(A.CATEGORIES)), F(0))
        conditional = horizon*scores[selected_index]
        assert F(selection["lower_gain_per_query"]) == scores[selected_index]
        assert F(selection["conditional_batch_lower_gain"]) == conditional
        assert F(selection["assessment_cost"]) == expected_assessment
        assert F(selection["all_in_lower_gain"]) == conditional - expected_assessment
        assert selection["positive_continuation_certificate"] == (scores[selected_index] > 0)
        assert selection["positive_all_in_certificate"] == (conditional > expected_assessment)
        # Replay only the small selector, never any solver or experiment driver.
        assert C.select(profile, scope, prices, horizon) == selection
        coverage = all(lo <= F(population_sums[pi][j], 248) <= hi for pi, values in enumerate(intervals) for j, (lo, hi) in enumerate(values))
        interval_coverage.append(coverage)
        assert scores[selected_index] <= sum((prices[j]*F(population_sums[selected_index][j], 248) for j in range(14)), F(0))

        deployment, baseline_resources, exact_resources = zero(), zero(), zero()
        task_cost = baseline_cost = exact_cost = F(0)
        for index in row["cohort_indices"]:
            features = population[index]["features"]
            deployment.update(resource_values(features[selected_index]))
            baseline_resources.update(resource_values(features[0]))
            exact_resources.update(resource_values(features[-1]))
            task_cost += sum((p*v for p, v in zip(prices[:3], features[selected_index][:3])), F(0))
            baseline_cost += sum((p*v for p, v in zip(prices, features[0])), F(0))
            exact_cost += sum((p*v for p, v in zip(prices, features[-1])), F(0))
        assert deployment == row["deployment_resources"]
        assert baseline_resources == row["baseline_resources"]
        assert exact_resources == row["exact_resources"]
        assert selection["meter"]["by_category"] == row["assessment_resources"]
        all_resources = setup.copy()
        all_resources.update(row["assessment_resources"])
        all_resources.update(deployment)
        assert all_resources == row["controller_resources"]
        all_cost = task_cost + F(sum(all_resources.values()), 1000)
        gain = baseline_cost - all_cost
        assert F(row["controller_task_cost"]) == task_cost
        assert F(row["controller_all_in_cost"]) == all_cost
        assert F(row["baseline_cost"]) == baseline_cost
        assert F(row["charged_exact_cost"]) == exact_cost
        assert F(row["paired_all_in_gain"]) == gain
        assert sum(all_resources.values()) <= row["resource_cap"] == resource_cap
        assert low <= gain <= high
        extra = baseline_resources.copy()
        if selected_index != 5:
            extra.update(exact_resources)
        assert extra == row["audit_extra_resources"]
        outer_meter = row["outer_audit_meter"]
        meter_checks(outer_meter)
        assert outer_meter["operations"] == outer_ops and outer_meter["events"] == 130 and outer_meter["denials"] == 0
        outer_bill.update(all_resources)
        outer_bill.update(extra)
        outer_bill.update(outer_meter["by_category"])
        total_gain += gain
        total_controller += all_cost
        total_baseline += baseline_cost
        total_exact += exact_cost
        gains.append(gain)
        caps_used.append(sum(all_resources.values()))
        policies[row["policy"]] += 1

    cert_meter = result["final_certificate_meter"]
    meter_checks(cert_meter)
    assert cert_meter["operations"] == {"assessment.radius_integer_bound_bundle": 160, "assessment.whole_mean_and_lower_bound_readout": 64, "storage.whole_audit_certificate_retention": 8192}
    outer_bill.update(cert_meter["by_category"])
    assert outer_bill == result["outer_audit_procurement_resources"]
    assert F(result["outer_audit_procurement_cost"]) == F(sum(outer_bill.values()), 1000)
    radius, k = independent_radius(audit_n, 1, F(1, 20), 1)
    mean = total_gain/audit_n
    lower = max(low, mean - (high-low)*radius)
    assert F(result["radius"]) == radius and result["radius_k"] == k
    assert F(result["mean_all_in_gain"]) == mean == F(270489329, 256000)
    assert F(result["lower_all_in_gain"]) == lower == F(1211017049, 4096000)
    assert F(result["mean_controller_all_in_cost"]) == total_controller/audit_n
    assert F(result["mean_baseline_cost"]) == total_baseline/audit_n
    assert F(result["mean_charged_exact_cost"]) == total_exact/audit_n
    assert result["policies"] == policies == {"full_fallback": 256}
    assert result["positive_whole_procedure_certificate"] == (lower > 0)
    assert total_exact < total_controller < total_baseline

    # Controller v3 is byte-identical to the completed v1 review. Do not repeat
    # its old boundary suite; check the now-distinct generator scopes instead.
    profile = frozen_profile(profile_closures[0]["profile"])
    edges = []
    for name, altered in (("driver_only_change", changed), ("wrapper_only_change", changed_wrapper)):
        try:
            C.select(profile, whole_scope(altered), prices, horizon)
        except C.Rejected:
            edges.append({"case": name, "scope_changed": True, "old_profile_rejected": True})
        else:
            raise AssertionError("A changed generator scope admitted the old profile.")

    # Instrument only the actual wrapper order; stop before any deployment solve.
    order = []
    class Trace:
        def __init__(self):
            self.row = None
            self.flushed = False
        def write(self, value):
            self.row = json.loads(value)
            order.append("profile_and_selection_written")
        def flush(self):
            assert self.row["profile_id"] == profile.identity
            self.flushed = True
            order.append("profile_and_selection_flushed")
    trace = Trace()
    class Rng:
        def randrange(self, bound):
            assert trace.flushed and bound == 248
            order.append("first_deployment_index_draw")
            return episode_rows[0]["cohort_indices"][0]
    class StoppedBeforeSolver(Exception):
        pass
    original_build, original_run = W.build_profile, C.run_policy
    def build_stub(*args):
        order.append("profile_acquired")
        return profile, Counter(profile.setup_resources and dict(zip(A.CATEGORIES, profile.setup_resources))), profile_closures[0]["procurement"]
    def stop_run(*args, **kwargs):
        assert trace.flushed
        order.append("first_deployment_policy_call")
        raise StoppedBeforeSolver()
    try:
        W.build_profile, C.run_policy = build_stub, stop_run
        try:
            W.episode_run(0, Rng(), scope, source_hashes, trace, A.Meter(100000))
        except StoppedBeforeSolver:
            pass
        else:
            raise AssertionError("Ordering probe did not stop at the solver boundary.")
    finally:
        W.build_profile, C.run_policy = original_build, original_run
    assert order == ["profile_acquired", "profile_and_selection_written", "profile_and_selection_flushed", "first_deployment_index_draw", "first_deployment_policy_call"]

    # Execute main's startup prefix and stop before its first source hash.
    # Only new, empty directories inside this review directory are created.
    startup_order = []
    real_meter, real_hashes, real_argv = A.Meter, W.hashes, sys.argv
    for denied in (False, True):
        observed = []
        events = []
        class ObservedMeter(real_meter):
            def __init__(self, limit_total, category_limits=None):
                super().__init__(0 if denied and limit_total == 200000 else limit_total, category_limits)
                observed.append(self)
            def pay_many(self, charges):
                events.append("startup_charge_attempt")
                super().pay_many(charges)
                events.append("startup_funded")
        class StoppedBeforeHashes(Exception):
            pass
        def checked_hashes():
            events.append("first_source_hash_call")
            assert observed[0].total == 45598
            assert observed[0].snapshot()["operations"] == startup_meter["operations"]
            raise StoppedBeforeHashes()
        try:
            A.Meter, W.hashes = ObservedMeter, checked_hashes
            sys.argv = [str(SNAPSHOT / "07_whole_procedure_audit.py"), "--out", str(HERE / ("startup_denial_order_v2" if denied else "startup_funded_order_v2"))]
            try:
                W.main()
            except StoppedBeforeHashes:
                assert not denied
            except A.BudgetExhausted:
                assert denied
            else:
                raise AssertionError("Startup probe unexpectedly reached an episode.")
        finally:
            A.Meter, W.hashes, sys.argv = real_meter, real_hashes, real_argv
        expected = ["startup_charge_attempt"] if denied else ["startup_charge_attempt", "startup_funded", "first_source_hash_call"]
        assert events == expected
        startup_order.append({"charge_denied": denied, "events": events, "source_hash_called": not denied})

    evidence_files = sorted(path for directory in (RUN, POP_RUN) for path in directory.iterdir() if path.suffix in (".json", ".jsonl"))
    evidence_files += [WORKLOG / "development/whole_procedure_plan_v1.json", WORKLOG / "development/whole_procedure_plan_v2.json", WORKLOG / "reviews/controller_implementation_review_v2.md", HERE / "review_v1.md"]
    evidence_hashes = {str(path.relative_to(ROOT)): filehash(path) for path in evidence_files}
    for name, expected in root_hashes.items():
        assert filehash(ROOT / "v3/checks" / name) == expected
    return {
        "status": "WHOLE_V2_FIXES_AND_ALL_SAVED_NUMERICS_PASS",
        "review_type": "Independent reasoning within the same GPT-6 Astra Pro model; targeted nonblind source and saved-evidence review.",
        "reviewed_source_hashes": source_hashes,
        "source_snapshots_and_root_match_at_start_and_finish": True,
        "closure_identity": closure_id,
        "saved_evidence": {"population_rows": 248, "profile_closures": audit_n, "acquired_profile_rows_reconstructed": profile_n*audit_n, "deployment_queries_reconstructed": horizon*audit_n, "all_profile_sums_and_setup_vectors_match": True, "all_selection_scores_and_meters_match": True, "all_episode_feature_cost_and_resource_vectors_match": True, "all_indices_match_seed": closure["audit_seed"], "realized_profiles_cover_exact_population": sum(interval_coverage), "maximum_saved_policy_resource_units": max_policy_resource},
        "whole_certificate": {"resource_cap": resource_cap, "scalar_range": list(map(str, (low, high))), "mean_all_in_gain": str(mean), "radius": str(radius), "k": k, "lower_all_in_gain": str(lower), "mean_controller_cost": str(total_controller/audit_n), "mean_baseline_cost": str(total_baseline/audit_n), "mean_charged_exact_cost": str(total_exact/audit_n), "mean_profile_cost": str(sum(setup_costs)/audit_n), "observed_gain_range": list(map(str, (min(gains), max(gains)))), "observed_controller_resource_range": [min(caps_used), max(caps_used)], "policies": dict(policies)},
        "outer_recorded_bill": {"resources": dict(outer_bill), "total_units": sum(outer_bill.values()), "cost": result["outer_audit_procurement_cost"], "per_episode_audit_meter_units": sum(outer_ops.values()), "final_certificate_units": cert_meter["total"], "global_closure_startup_included": True, "global_startup_units": startup_meter["total"], "startup_order_probes": startup_order},
        "builder": {"source_words": source_words, "constant_operations": builder_ops, "constant_total": sum(builder_ops.values()), "limit": 150000},
        "joint_generator_scope_rejection_checks": edges,
        "profile_freeze_before_deployment_probe_order": order,
        "whole_v2_repair_checks": {"driver_only_hash_change_alters_whole_profile_scope": True, "wrapper_only_hash_change_alters_whole_profile_scope": True, "source_registry_and_global_closure_startup_prepaid": True, "startup_in_outer_bill": True, "source_archival_copies_declared_harness_instrumentation": True},
        "coverage_boundary": "All saved episodes acquired a complete 64-row profile and selected full_fallback; no saved profile-budget-failure or alternative-selection episode. No fresh solver audit or broad old-budget-suite rerun was performed. IID episodes are a model assumption; deterministic seeded trace is DEVELOPMENT only.",
        "principal_research90_credit_seconds": 0,
        "evidence_sha256": evidence_hashes,
    }


if __name__ == "__main__":
    result = main()
    with (HERE / "review_probe_results_v2.json").open("x") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    summary = {key: value for key, value in result.items() if key not in ("evidence_sha256", "joint_generator_scope_rejection_checks", "builder")}
    print(json.dumps(summary, indent=2, sort_keys=True))
