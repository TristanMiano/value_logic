#!/usr/bin/env python3
"""P3-B DEVELOPMENT: small independent semantic-bridge witnesses.

Prospective question: do the typed composition premises separate finite
assessment coverage, exceptional support, all-optimum transport, a checked
forecast inequality, and acquired complete-policy expectation?

Budget: at most 16 hypothetical assignments, four rank cases, two profile
rows and two scalar outcomes. No existing production module or test suite is
imported. This checks only the explicitly enumerated examples; the review
contains the general reconstructed implications. No principal-clock credit.

The exact profile example is a stipulated finite service/tariff, not a new
runtime measurement, statistical performance experiment or complexity claim.
"""

from datetime import datetime, timezone
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform
import sys
import time


def fraction(q):
    return str(Q(q))


def selected(points, rank):
    if not points:
        return []
    optimum = min(rank(x) for x in points)
    return [x for x in points if rank(x) == optimum]


def main():
    start_ns = time.monotonic_ns()
    started = datetime.now(timezone.utc).isoformat()
    results = {}

    # Truth and a received source are different objects.
    source = [0, 1]
    losses = [4 * q for q in source]
    assert losses == [0, 4]
    checked_sources = {str(q): [x for x in source if x == q] for q in source}
    assert checked_sources == {"0": [0], "1": [1]}
    assert not [q for q in source if q == 0 and q == 1]
    results["hard_source"] = {
        "unresolved_source": source,
        "loss_image": losses,
        "checked_sources": checked_sources,
        "conflict_status": "NO_NUMERIC_WARRANT",
    }

    # p & not-p has no ordinary valuation, but paired support admits p=(1,1).
    ordinary = list(product((0, 1), repeat=2))
    ordinary_antecedent = [x for x in ordinary if x[0] and not x[0]]
    assert ordinary_antecedent == []
    supports = list(product((0, 1), repeat=4))
    # Coordinates are (p+, p-, q+, q-); q stays normal, p may be abnormal.
    feasible = [s for s in supports if s[0] == s[1] == 1 and s[2] + s[3] == 1]
    old = [s for s in feasible if s[2:] == (0, 1)]
    rank = lambda s: int(s[0] + s[1] != 1)
    old_selected = selected(old, rank)
    current_selected = selected(feasible, rank)
    difference = lambda s: 4 * s[2] - 1
    image = sorted({difference(s) for s in current_selected})
    assert old_selected == [(1, 1, 0, 1)]
    assert current_selected == [(1, 1, 0, 1), (1, 1, 1, 0)]
    assert image == [-1, 3]
    mapping = lambda s: (s[0], s[1], 0, 1)
    corrections = [difference(s) - difference(mapping(s)) for s in current_selected]
    assert corrections == [0, 4]
    repaired_bound = -1 + max(corrections)
    assert repaired_bound == max(image) == 3
    assert any(difference(s) > -1 for s in current_selected)
    # Requiring normal p in this adapter leaves no feasible antecedent case.
    assert not [s for s in feasible if s[0] + s[1] == 1]
    results["counterpossible_transport"] = {
        "ordinary_antecedent_models": ordinary_antecedent,
        "old_selected_supports": old_selected,
        "current_selected_supports": current_selected,
        "current_difference_image": image,
        "old_bound": -1,
        "mapped_loss_corrections": corrections,
        "new_bound": repaired_bound,
        "stale_bound_refuted_by": [1, 1, 1, 0],
    }

    # Unresolved source facts must not be selected by their cheaper repair rank.
    by_source = [(0, 0, 0), (1, 1, 10)]  # source, local optimum rank, loss
    joint = selected(by_source, lambda row: row[1])
    assert [r[2] for r in by_source] == [0, 10]
    assert [r[2] for r in joint] == [0]
    results["sourcewise_quantifier"] = {
        "rows_source_rank_loss": by_source,
        "sourcewise_loss_image": [0, 10],
        "incorrect_joint_loss_image": [0],
    }

    # An incumbent sublevel can survive loss of every old optimum.
    points = list(product((0, 1), repeat=2))
    rank2 = lambda x: x[0] + 2 * x[1]
    d2 = lambda x: 4 * x[1] - 1
    old_winners = selected(points, rank2)
    band = [x for x in points if rank2(x) <= 1]
    p_edit = [x for x in points if x[0] == 1]
    q_edit = [x for x in points if x[1] == 1]
    p_winners = selected(p_edit, rank2)
    q_winners = selected(q_edit, rank2)
    assert old_winners == [(0, 0)]
    assert p_winners == [(1, 0)] and not set(old_winners).intersection(p_winners)
    assert all(x in band for x in p_winners)
    assert max(d2(x) for x in band) == -1
    assert q_winners == [(0, 1)] and rank2(q_winners[0]) == 2
    assert d2(q_winners[0]) == 3
    # Equality cannot be pruned in an all-optimum service.
    tied = selected([("a", 0, 0), ("b", 0, 4)], lambda r: r[1])
    assert [r[2] for r in tied] == [0, 4]
    results["all_optimum_sublevel"] = {
        "old_winners": old_winners,
        "certified_band": band,
        "p_edit_winners": p_winners,
        "p_edit_bound": -1,
        "q_edit_winners": q_winners,
        "q_edit_rank_exceeds_cutoff": True,
        "q_edit_actual_difference": 3,
        "equal_rank_loss_image": [r[2] for r in tied],
    }

    # CF-1 is an algebraic report certificate, not a guarantee of its forecast.
    p, phi, previous = Q(1, 2), Q(1), Q(0)
    score = previous * phi + (1 - 2 * p) * phi * phi / 2
    allowance = 2 * max(Q(0), (1 - p) * score, -p * score)
    binary_rows = []
    for y in (0, 1):
        residual = previous + (y - p) * phi
        budget = p * (1 - p) * phi * phi + allowance
        assert residual * residual <= budget
        binary_rows.append({"y": y, "residual_squared": fraction(residual * residual), "budget": fraction(budget)})
    assert 4 * p == 2 and 4 * 1 == 4
    results["forecast_guarantee_type"] = {
        "issued_scalar": fraction(p),
        "score": fraction(score),
        "allowance": fraction(allowance),
        "potential_cases": binary_rows,
        "forecast_risky_loss": fraction(4 * p),
        "actual_risky_loss_when_y_one": 4,
        "forecast_is_not_an_upper_loss_certificate": True,
    }

    # A finite acquired profile has a law over requests, not support identifiers.
    # Two deterministic query types occur with probability 1/2 each. A paid
    # exact evaluator obtains the type's q; the complete policy continues at
    # q=0 and falls back at q=1. Profile setup/assessment is stipulated to cost 2.
    evaluation_fee = Q(1, 5)
    setup_and_assessment = Q(2)
    horizon = 10
    rows = []
    for q in (0, 1):
        baseline = Q(1)
        policy = evaluation_fee + (Q(0) if q == 0 else Q(1))
        saving = baseline - policy
        rows.append({"q": q, "baseline": fraction(baseline), "complete_policy_cost": fraction(policy), "saving": fraction(saving)})
    mean_saving = sum(Q(row["saving"]) for row in rows) / 2
    root_gain = horizon * mean_saving - setup_and_assessment
    assert mean_saving == Q(3, 10) and root_gain == Q(1)
    assert Q(rows[1]["saving"]) < 0
    # An identifier-uniform average would change under a duplicate even though
    # neither the hypothetical loss image nor the declared request law changes.
    uniform_tie_mean = Q(sum((0, 4)), 2)
    duplicate_uniform_mean = Q(sum((0, 0, 4)), 3)
    assert uniform_tie_mean == 2 and duplicate_uniform_mean == Q(4, 3)
    results["paid_complete_policy"] = {
        "population": "two deterministic request types, mass 1/2 each",
        "profile_route": "paid exact evaluation of both types plus admitted finite table arithmetic; stipulated tariff",
        "profile_rows": rows,
        "mean_fresh_request_saving": fraction(mean_saving),
        "setup_and_assessment_cost": fraction(setup_and_assessment),
        "future_horizon_assumption": horizon,
        "all_in_expected_gain": fraction(root_gain),
        "individual_negative_gain_case": 1,
        "identifier_uniform_means_before_after_duplicate": [fraction(uniform_tie_mean), fraction(duplicate_uniform_mean)],
        "ordinary_same_policy_same_cost": True,
        "optimized_ordinary_shortcuts_not_excluded": True,
    }

    out = {
        "schema": "value_logic.p3b.semantic_bridge_checks.v1",
        "evidence_stage": "DEVELOPMENT",
        "scope": "six explicit finite separating/positive examples; no general theorem established by enumeration",
        "status": "PASS",
        "production_imports": [],
        "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "run_elapsed_ns": time.monotonic_ns() - start_ns,
        "python": sys.version,
        "platform": platform.platform(),
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "agent_resource_cost": "review work unmeasured; this run duration only; no principal-clock credit",
        "results": results,
    }
    target = Path(__file__).with_name("bridge_checks_result.json")
    with target.open("x", encoding="utf-8") as handle:
        json.dump(out, handle, indent=2)
        handle.write("\n")
    print(json.dumps({"status": out["status"], "groups": list(results), "result": str(target), "run_elapsed_ns": out["run_elapsed_ns"]}))


if __name__ == "__main__":
    main()
