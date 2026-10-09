#!/usr/bin/env python3
"""Exact finite checks of the proposed new action block and bounded sampler.

No P3-06 implementation or root P3-07 code is imported. The short potential
trace checks the application of the inherited interface to the new feature
map, not the completed P3-06 research task or a mathematical query engine.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import platform


OUT = Path(__file__).resolve().parent


def encode(value):
    if isinstance(value, F):
        return {"numerator": str(value.numerator), "denominator": str(value.denominator), "decimal": float(value)}
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def norm2(a):
    return dot(a, a)


def projection(costs, eta):
    assert eta > 0 and costs
    prefix = F(0)
    tau = None
    for m, value in enumerate(sorted(costs), 1):
        prefix += value
        candidate = (eta + prefix) / m
        if value < candidate:
            tau = candidate
    assert tau is not None
    q = tuple(max(F(0), (tau - c) / eta) for c in costs)
    assert sum(q) == 1
    gradient = tuple(c + eta * qi for c, qi in zip(costs, q))
    assert all(g == tau if qi > 0 else g >= tau for g, qi in zip(gradient, q))
    return q


def smoothing_checks():
    comparisons = 0
    for actions in range(1, 6):
        for costs in product((F(-1), F(0), F(1)), repeat=actions):
            for eta in (F(1, 2), F(1), F(3)):
                q = projection(costs, eta)
                cap = eta * F(actions - 1, 4 * actions)
                for a in range(actions):
                    gap = dot(q, costs) - costs[a]
                    middle = eta * (q[a] - norm2(q))
                    assert gap <= middle <= cap
                    comparisons += 1
    sharp = []
    for actions in range(1, 9):
        eta = F(7, 3)
        costs = (F(0),) + (eta / 2,) * (actions - 1)
        q = projection(costs, eta)
        expected = (F(actions + 1, 2 * actions),) + (F(1, 2 * actions),) * (actions - 1)
        assert q == expected
        gap = dot(q, costs)
        assert gap == eta * F(actions - 1, 4 * actions)
        sharp.append({"actions": actions, "eta": eta, "q": q, "attained_gap": gap})
    return {"exact_comparator_checks": comparisons, "sharp_examples": sharp}


def rows_costs(rows, p):
    return tuple(b + d * p for b, d in rows)


def features(rows, eta, gammas, weight, p):
    q = projection(rows_costs(rows, p), eta)
    slopes = tuple(d for _, d in rows)
    mean = dot(q, slopes)
    phi = tuple(g * weight * (mean - d) for g, d in zip(gammas, slopes))
    return q, phi


def geometry_checks():
    tables = [((F(0), F(1)), (F(1), F(-1))),
              ((F(0), F(1)), (F(2), F(-2)), (F(1, 4), F(0)), (F(3, 8), F(0))),
              ((F(-1), F(3)), (F(1), F(-2)), (F(0), F(1)), (F(1, 3), F(0)), (F(5, 6), F(-1)))]
    tested = 0
    records = []
    for rows in tables:
        actions = len(rows)
        eta = F(3, 8)
        gammas = tuple(F(a + 1, 2) for a in range(actions))
        slopes = tuple(d for _, d in rows)
        width = max(slopes) - min(slopes)
        squared_cap = width * width * (norm2(gammas) - min(g * g for g in gammas))
        lip = F(actions) * width * width / (4 * eta)
        previous = None
        supports = set()
        for k in range(33):
            p = F(k, 32)
            q, phi = features(rows, eta, gammas, F(1), p)
            assert norm2(phi) <= squared_cap
            support = tuple(i for i, qi in enumerate(q) if qi > 0)
            supports.add(support)
            active_slopes = tuple(slopes[i] for i in support)
            average = sum(active_slopes) / len(support)
            derivative_magnitude = sum((d - average) ** 2 for d in active_slopes) / eta
            assert derivative_magnitude <= lip
            mean = dot(q, slopes)
            if previous is not None:
                old_p, old_mean = previous
                assert mean <= old_mean
                assert old_mean - mean <= lip * (p - old_p)
            previous = p, mean
            tested += 1
        records.append({"actions": actions, "slope_range": width,
                        "feature_squared_cap": squared_cap,
                        "mean_slope_lipschitz_cap": lip,
                        "observed_supports_on_grid": sorted(supports)})
    return {"exact_geometry_grid_points": tested, "tables": records,
            "scope": "Grid checks illustrate the independently proved global continuity and bounds."}


def score(residual, rows, eta, gammas, weight, p):
    q, phi = features(rows, eta, gammas, weight, p)
    value = dot(residual, phi) + (1 - 2 * p) * norm2(phi) / 2
    return value, q, phi


def choose(residual, rows, eta, gammas, weight, steps=12):
    left = score(residual, rows, eta, gammas, weight, F(0))
    if left[0] <= 0:
        p, result, route = F(0), left, "endpoint_zero"
    else:
        right = score(residual, rows, eta, gammas, weight, F(1))
        if right[0] >= 0:
            p, result, route = F(1), right, "endpoint_one"
        else:
            lo, hi = F(0), F(1)
            for _ in range(steps):
                p = (lo + hi) / 2
                result = score(residual, rows, eta, gammas, weight, p)
                if result[0] == 0:
                    break
                if result[0] > 0:
                    lo = p
                else:
                    hi = p
            route = "interior_exact" if result[0] == 0 else "interior_allowance"
    s, q, phi = result
    allowance = 2 * max(F(0), (1 - p) * s, -p * s)
    return p, q, phi, allowance, route


def potential_application_check():
    actions = 4
    gammas = (F(1), F(1, 2), F(2), F(3, 2))
    residual = (F(0),) * actions
    bound = F(0)
    mixed = F(0)
    comparator = [F(0)] * actions
    predicted_gaps = [F(0)] * actions
    smoothing = F(0)
    routes = {}
    answers = [1] * 6 + [0] * 6 + [i % 2 for i in range(12)]
    for t, y in enumerate(answers):
        rows = ((F(0), F(1 + t % 4, 2)),
                (F(2 + t % 3, 2), F(-(2 + t % 3), 2)),
                (F(2 + t % 2, 8), F(0)),
                (F(3 + t % 3, 8), F(0)))
        eta = F(1, 4 * (1 << (t % 3)))
        weight = F(0) if t == 7 else F(1 + t % 2, 2)
        p, q, phi, allowance, route = choose(residual, rows, eta, gammas, weight)
        routes[route] = routes.get(route, 0) + 1
        residual = tuple(r + (y - p) * f for r, f in zip(residual, phi))
        bound += p * (1 - p) * norm2(phi) + allowance
        assert norm2(residual) <= bound
        actual_costs = rows_costs(rows, F(y))
        predicted_costs = rows_costs(rows, p)
        mixed += weight * dot(q, actual_costs)
        smoothing += weight * eta * F(actions - 1, 4 * actions)
        for a in range(actions):
            comparator[a] += weight * actual_costs[a]
            predicted_gaps[a] += weight * (dot(q, predicted_costs) - predicted_costs[a])
            regret = mixed - comparator[a]
            assert regret == predicted_gaps[a] + residual[a] / gammas[a]
            assert predicted_gaps[a] <= smoothing
            positive_excess = max(F(0), regret - smoothing)
            assert (positive_excess * gammas[a]) ** 2 <= bound
    return {"rounds": len(answers), "actions": actions, "gamma": gammas,
            "root_routes": routes, "mixed_total": mixed, "fixed_action_totals": comparator,
            "regrets": [mixed - c for c in comparator], "smoothing_allowance": smoothing,
            "potential_bound": bound, "actual_residual_squared_norm": norm2(residual),
            "scope": "New action-feature application on rational fixtures; no mathematical solver, random sampler, delayed wrapper or deployment performance claim."}


def endpoint_checks():
    rows = ((F(0), F(1)), (F(1), F(-1)))
    results = []
    for residual, expected in [((F(0), F(-10)), "endpoint_zero"),
                               ((F(-10), F(0)), "endpoint_one"),
                               ((F(0), F(0)), "interior_exact")]:
        p, q, phi, allowance, route = choose(residual, rows, F(1, 4), (F(1), F(1)), F(1))
        assert route == expected and allowance == 0
        for y in (F(0), F(1)):
            updated = tuple(r + (y - p) * f for r, f in zip(residual, phi))
            assert norm2(updated) - norm2(residual) <= p * (1 - p) * norm2(phi) + allowance
        results.append({"route": route, "probability": p, "q": q, "allowance": allowance})
    return results


def largest_remainder(q, denominator):
    scaled = tuple(denominator * qi for qi in q)
    floors = [value.numerator // value.denominator for value in scaled]
    fractions = tuple(value - floor for value, floor in zip(scaled, floors))
    residual_count = denominator - sum(floors)
    assert sum(fractions) == residual_count
    order = sorted(range(len(q)), key=lambda i: (-fractions[i], i))
    rounded = floors[:]
    for i in order[:residual_count]:
        rounded[i] += 1
    nu = tuple(F(value, denominator) for value in rounded)
    tv = sum(abs(n - qi) for n, qi in zip(nu, q)) / 2
    identity = F(residual_count) - sum((fractions[i] for i in order[:residual_count]), F(0))
    assert tv == identity / denominator
    return nu, tv, residual_count


def exact_tv_cap(actions, denominator):
    return max(F(r * (actions - r), actions * denominator)
               for r in range(min(actions - 1, denominator) + 1))


def compositions(total, count):
    if count == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, count - 1):
                yield (first,) + rest


def dyadic_checks():
    checked = 0
    sharp = []
    for actions in range(1, 6):
        for parts in compositions(12, actions):
            q = tuple(F(part, 12) for part in parts)
            for denominator in (1, 2, 4, 8):
                nu, tv, r = largest_remainder(q, denominator)
                assert sum(nu) == 1 and all(ni >= 0 for ni in nu)
                assert tv <= F(r * (actions - r), actions * denominator)
                assert tv <= exact_tv_cap(actions, denominator)
                assert tv <= F((actions * actions) // 4, actions * denominator)
                checked += 1
    for actions in range(1, 9):
        for denominator in (1, 2, 4, 8):
            r = min(denominator, actions // 2)
            floors = (denominator - r,) + (0,) * (actions - 1)
            q = tuple(F(k, denominator) + F(r, actions * denominator) for k in floors)
            nu, tv, actual_r = largest_remainder(q, denominator)
            assert r == actual_r
            assert tv == exact_tv_cap(actions, denominator)
            counts = [0] * actions
            cumulative = []
            total = 0
            for ni in nu:
                total += ni * denominator
                assert total.denominator == 1
                cumulative.append(total.numerator)
            for random_integer in range(denominator):
                action = next(i for i, cutoff in enumerate(cumulative) if random_integer < cutoff)
                counts[action] += 1
            assert tuple(F(n, denominator) for n in counts) == nu
            sharp.append({"actions": actions, "denominator": denominator, "R": r,
                          "ideal_q": q, "rounded_nu": nu, "attained_TV": tv,
                          "general_bound": F((actions * actions) // 4, actions * denominator),
                          "exact_fixed_dimension_bound": exact_tv_cap(actions, denominator)})
    return {"rational_grid_checks": checked, "sharp_and_sampler_examples": sharp}


def boundary_witnesses():
    q = projection((F(0), F(1)), F(2))
    assert q == (F(3, 4), F(1, 4))
    mixed = dot(q, (F(0), F(1)))
    unfiltered_noise_mean = sum((qi * (c - mixed) for qi, c in zip(q, (F(0), F(1)))), F(0))
    filtered_noise_mean = q[1] * (1 - mixed)
    assert unfiltered_noise_mean == 0 and filtered_noise_mean == F(3, 16)

    rows = ((F(0), F(1)), (F(1), F(-1)), (F(1, 10), F(0)), (F(1, 5), F(0)))
    p, q_no_feedback, _, _, _ = choose((F(0),) * 4, rows, F(1, 20), (F(1),) * 4, F(1))
    assert p == F(1, 2) and q_no_feedback == (F(0), F(0), F(1), F(0))

    bound_only_q = projection((F(2), F(10)), F(1))
    assert bound_only_q == (F(1), F(0))
    return {"bounded_fair_bits": {"three_action_equal_cost_mix": projection((F(0),) * 3, F(1)),
             "obstruction": "1/3 is not dyadic, so no finite worst-case fair-bit sampler can implement it exactly without another primitive."},
            "action_selected_feedback_noise": {"ideal_and_sampled_mix": q,
             "costs_fallback_buy": [0, 1], "mixture_cost": mixed,
             "unfiltered_increment_mean": unfiltered_noise_mean,
             "only_buy_settles_filtered_increment_mean": filtered_noise_mean,
             "increment_given_settlement": F(3, 4)},
            "no_labels_no_whole_cohort_potential": {"fresh_copy_p": p, "action_mix": q_no_feedback,
             "eight_fallback_query_total_when_answers_all_one": F(4, 5),
             "best_fixed_guess_one_total": F(0), "settled_observations": 0,
             "settled_potential_bound": F(0), "invalid_all_issue_smoothing_only_claim": 8 * F(1, 20) * F(3, 16)},
            "cost_upper_bound_is_not_tariff": {"surrogate_costs": [2, 10], "actual_costs": [2, 1],
             "eta": F(1), "q": bound_only_q, "surrogate_regret_to_buy": F(-8),
             "actual_regret_to_buy": F(1), "smoothing_only_bound": F(1, 8)}}


def main():
    with (OUT / "multi_action_attempt.json").open("x") as handle:
        json.dump({"data_class": "DEVELOPMENT", "frozen_evaluation": False,
                   "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
                   "python": platform.python_version(), "principal_credit_minutes": 0,
                   "research_time": "unmeasured"}, handle, indent=2)
        handle.write("\n")
    result = {"status": "PASS", "data_class": "DEVELOPMENT", "frozen_evaluation": False,
              "smoothing": smoothing_checks(), "geometry": geometry_checks(),
              "endpoint_conditions": endpoint_checks(),
              "new_feature_potential_application": potential_application_check(),
              "largest_remainder_dyadic": dyadic_checks(), "boundaries": boundary_witnesses()}
    with (OUT / "multi_action_checks_result.json").open("x") as handle:
        json.dump(encode(result), handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"status": result["status"],
                      "comparator_checks": result["smoothing"]["exact_comparator_checks"],
                      "dyadic_grid_checks": result["largest_remainder_dyadic"]["rational_grid_checks"],
                      "root_routes": result["new_feature_potential_application"]["root_routes"],
                      "result": str(OUT / "multi_action_checks_result.json")}))


if __name__ == "__main__":
    main()
