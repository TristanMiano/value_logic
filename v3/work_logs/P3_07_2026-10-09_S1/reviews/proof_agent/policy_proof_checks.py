#!/usr/bin/env python3
"""Exact finite development checks for the independent P3-07 review.

These are arithmetic witnesses and a finite enumeration, not deployment
profiling, an empirical performance comparison, or a complete proof by tests.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import math
import platform


ROOT = Path(__file__).resolve().parent


def encode(value):
    if isinstance(value, F):
        return {"numerator": str(value.numerator), "denominator": str(value.denominator), "decimal": float(value)}
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def policies(remaining):
    result = [("act", 0), ("act", 1)]
    for bit in remaining:
        children = policies(tuple(j for j in remaining if j != bit))
        result.extend(("read", bit, p0, p1) for p0, p1 in product(children, repeat=2))
    return result


def execute(policy, bits):
    count = 0
    while policy[0] == "read":
        count += 1
        policy = policy[2 + bits[policy[1]]]
    answer = policy[1]
    return F(answer != (bits[0] ^ bits[1])) + F(count, 10), count


def complete_policy_witness():
    catalogue = policies((0, 1))
    cases = list(product((0, 1), repeat=2))
    records = []
    for policy in catalogue:
        traces = [execute(policy, bits) for bits in cases]
        records.append((sum((loss for loss, _ in traces), F(0)) / 4,
                        max(count for _, count in traces), policy))
    assert len(catalogue) == 74
    assert max(count for _, count, _ in records) == 2
    best = min(loss for loss, _, _ in records)
    best_one_step = min(loss for loss, count, _ in records if count <= 1)
    forced_one_step = min(loss for loss, count, p in records if count <= 1 and p[0] == "read")
    assert (best, best_one_step, forced_one_step) == (F(1, 5), F(1, 2), F(3, 5))
    return {"catalogue_size": len(catalogue), "world_count": 4,
            "hard_maximum_reads": 2, "stop_loss": F(1, 2),
            "best_complete_policy_loss": best,
            "best_complete_policy_gain": F(1, 2) - best,
            "best_policy_with_at_most_one_read_loss": best_one_step,
            "best_forced_one_read_loss": forced_one_step,
            "best_policy_count": sum(loss == best for loss, _, _ in records)}


def success_profile_witness():
    result = {}
    for name, succeeds in [("success_on_baseline_errors", lambda y: y == 1),
                           ("success_on_baseline_correct_cases", lambda y: y == 0)]:
        gain = F(0)
        successes = 0
        for y in (0, 1):
            success = succeeds(y)
            successes += success
            chosen = y if success else 0
            gain += F(10 * y - (10 * (chosen != y) + 1), 2)
        result[name] = {"success_rate": F(successes, 2),
                        "accuracy_given_success": F(1), "paid_cost": F(1), "expected_gain": gain}
    assert result["success_on_baseline_errors"]["expected_gain"] == 4
    assert result["success_on_baseline_correct_cases"]["expected_gain"] == -1
    return result


def contextual_price_witness():
    records = {}
    price = (F(1), F(9))
    for name, improvements in [("gain_at_low_stakes", (F(1), F(0))),
                               ("gain_at_high_stakes", (F(0), F(1)))]:
        raw_mean = sum(improvements, F(0)) / 2
        actual = sum((p * d for p, d in zip(price, improvements)), F(0)) / 2 - 2
        proxy = (sum(price) / 2) * raw_mean - 2
        records[name] = {"unweighted_gain_feature_mean": raw_mean,
                         "resource_feature_mean": F(-1),
                         "mean_price_times_mean_feature_proxy": proxy,
                         "true_contextually_priced_gain": actual}
    assert records["gain_at_low_stakes"]["true_contextually_priced_gain"] == F(-3, 2)
    assert records["gain_at_high_stakes"]["true_contextually_priced_gain"] == F(5, 2)
    assert all(row["mean_price_times_mean_feature_proxy"] == F(1, 2) for row in records.values())
    return records


def coordinate_box_check():
    center = (F(1, 2), F(-2), F(1, 4))
    epsilon = (F(1, 10), F(1, 5), F(1, 20))
    vertices = [tuple(m + s * e for m, e, s in zip(center, epsilon, signs))
                for signs in product((-1, 1), repeat=3)]
    records = []
    for weights in [(F(1), F(1), F(1)), (F(-3), F(0), F(2)),
                    (F(7, 3), F(-1, 2), F(-5)), (F(0), F(0), F(0))]:
        formula = sum((w * m - abs(w) * e for w, m, e in zip(weights, center, epsilon)), F(0))
        enumerated = min(sum((w * v for w, v in zip(weights, vertex)), F(0)) for vertex in vertices)
        assert formula == enumerated
        records.append({"weights": weights, "formula_lower_bound": formula, "enumerated_minimum": enumerated})
    return {"dimension": 3, "vertex_count": 8, "price_vectors_checked": records,
            "scope": "Exact checks of four examples; the general all-prices result is proved in the review."}


def shared_law_witness():
    baseline = F(3, 4)
    acquisition = F(1, 10)
    endpoint_laws = ((F(1), F(0)), (F(0), F(1)))
    root_costs = [acquisition + sum(y) / 2 for y in endpoint_laws]
    committed_lower_gain = baseline - max(root_costs)
    replanned_cost = acquisition + baseline
    replanned_gain = baseline - replanned_cost
    assert committed_lower_gain == F(3, 20)
    assert replanned_gain == F(-1, 10)
    return {"fallback_loss": baseline, "observation_cost": acquisition,
            "shared_theta_endpoint_conditional_costs": endpoint_laws,
            "committed_policy_costs": root_costs,
            "root_committed_lower_gain": committed_lower_gain,
            "conditional_worst_case_cost_in_either_branch": F(1),
            "conditional_replanning_choice": "fallback in either branch",
            "replanned_gain": replanned_gain}


def accounting_and_version_witnesses():
    return {"cold_start_stop_after_assessment": {"assessment_cost": F(1, 20),
             "deployment_gain": F(0), "total_gain": F(-1, 20)},
            "positive_deployment_certificate_below_setup_cost": {"assessment_cost": F(1, 20),
             "deployment_gain": F(3, 100), "total_gain": F(-1, 50)},
            "stale_version_same_accuracy_changed_compute_cost": {
             "stop_task_loss": F(1, 2), "old_exact_policy_cost": F(1, 5),
             "old_expected_gain": F(3, 10), "new_exact_policy_cost": F(7, 10),
             "new_expected_gain": F(-1, 5), "accuracy_both_versions": F(1)},
            "mean_budget_is_not_a_hard_budget": {"equiprobable_resource_use": [0, 4],
             "mean_resource_use": F(2), "hard_budget": 2, "violation_probability": F(1, 2)}}


def optional_stopping_witness(cap=2000):
    # X_i are equiprobable +/-1, with true mean zero and range length two.
    # At any fixed n, P(S_n > sqrt(6 n)) <= exp(-3) < 1/20.
    # The exponential comparison is certified without floating point:
    partial_exp3 = sum((F(3 ** k, math.factorial(k)) for k in range(9)), F(0))
    assert partial_exp3 > 20
    safe_counts = {0: 1}
    snapshots = {}
    for n in range(1, cap + 1):
        next_counts = {}
        for s, count in safe_counts.items():
            for new_s in (s - 1, s + 1):
                if new_s > 0 and new_s * new_s > 6 * n:
                    continue
                next_counts[new_s] = next_counts.get(new_s, 0) + count
        safe_counts = next_counts
        if n in (100, 250, 500, 1000, 2000):
            crossed = F((1 << n) - sum(safe_counts.values()), 1 << n)
            snapshots[str(n)] = crossed
    crossed = F((1 << cap) - sum(safe_counts.values()), 1 << cap)
    assert crossed > F(1, 20)
    return {"maximum_profile_samples": cap, "null_mean": F(0),
            "individual_fixed_time_failure_bound": F(1, 20),
            "fixed_time_bound_is_strict": True,
            "fixed_time_boundary": "S_n > 0 and S_n^2 > 6*n",
            "rational_lower_bound_for_exp_3": partial_exp3,
            "optional_stopping_false_positive_probability": crossed,
            "prefix_crossing_probabilities": snapshots,
            "scope": "Exact integer count of all 2^cap paths via dynamic programming; not a simulation."}


def main():
    start = ROOT / "probe_attempt.json"
    with start.open("x") as handle:
        json.dump({"data_class": "DEVELOPMENT", "frozen_evaluation": False,
                   "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
                   "python": platform.python_version(), "principal_credit_minutes": 0,
                   "agent_research_cost": "unmeasured"}, handle, indent=2)
        handle.write("\n")
    result = {"status": "PASS", "data_class": "DEVELOPMENT", "frozen_evaluation": False,
              "complete_policy_complementarity": complete_policy_witness(),
              "success_rate_nonidentification": success_profile_witness(),
              "contextual_price_nonidentification": contextual_price_witness(),
              "coordinate_box_examples": coordinate_box_check(),
              "nonrectangular_replanning": shared_law_witness(),
              "accounting_version_and_budget": accounting_and_version_witnesses(),
              "optional_stopping": optional_stopping_witness()}
    with (ROOT / "policy_proof_checks_result.json").open("x") as handle:
        json.dump(encode(result), handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": result["status"], "catalogue_size": 74,
                      "optional_stop_false_positive": float(result["optional_stopping"]["optional_stopping_false_positive_probability"]),
                      "output": str(ROOT / "policy_proof_checks_result.json")}))


if __name__ == "__main__":
    main()
