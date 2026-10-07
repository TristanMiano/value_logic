#!/usr/bin/env python3
"""DEVELOPMENT: exact finite checks for P3-02 decision-summary geometry.

This is internal same-model reconstruction evidence, not a frozen challenge,
an independent-model review, or principal-session time credit.  Its two
predicates use different calculations: positive-area optimal cells versus
common minimizing actions at the endpoints of every observation fiber.

Scope: real Delta_3, exact rational loss rows, finite action menus, fixed
linear observation y=p_1, and returning SOME Bayes-optimal action.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


def normalize_rows(rows):
    result = tuple(tuple(F(value) for value in row) for row in rows)
    if not result or any(len(row) != 3 for row in result):
        raise ValueError("This development check requires a nonempty Delta_3 menu.")
    return result


def essential_indices(rows):
    """Merge duplicate rows, then find positive-area closed optimal cells."""
    rows = normalize_rows(rows)
    representatives = {}
    for index, row in enumerate(rows):
        representatives.setdefault(row, index)
    distinct = list(representatives.items())
    essential = []
    for candidate, original_index in distinct:
        # p=(x,z,1-x-z); each constraint is a*x+b*z+c <= 0.
        constraints = [(-1, 0, 0), (0, -1, 0), (1, 1, -1)]
        for other, _ in distinct:
            if candidate != other:
                difference = [candidate[t] - other[t] for t in range(3)]
                constraints.append(
                    (
                        difference[0] - difference[2],
                        difference[1] - difference[2],
                        difference[2],
                    )
                )
        vertices = set()
        for (a, b, c), (d, e, f) in combinations(constraints, 2):
            determinant = a * e - b * d
            if determinant:
                x = F(b * f - c * e, determinant)
                z = F(c * d - a * f, determinant)
                if all(u * x + v * z + w <= 0 for u, v, w in constraints):
                    vertices.add((x, z))
        vertices = sorted(vertices)
        if len(vertices) >= 3:
            x0, z0 = vertices[0]
            if any(
                (x1 - x0) * (z2 - z0) - (z1 - z0) * (x2 - x0) != 0
                for (x1, z1), (x2, z2) in combinations(vertices[1:], 2)
            ):
                essential.append(original_index)
    if not essential:
        raise AssertionError("A finite distinct menu must have an essential row.")
    return essential


def geometry_predicate(rows):
    """Test essential differences against hidden direction (0,1,-1)."""
    rows = normalize_rows(rows)
    essential = essential_indices(rows)
    hidden_coefficients = {rows[index][1] - rows[index][2] for index in essential}
    return len(hidden_coefficients) == 1, essential


def losses(rows, law):
    return [sum(c * p for c, p in zip(row, law)) for row in rows]


def argmins(rows, law):
    values = losses(rows, law)
    minimum = min(values)
    return {index for index, value in enumerate(values) if value == minimum}


def fiber_endpoints(y):
    y = F(y)
    if not 0 <= y <= 1:
        raise ValueError("A feasible summary must lie in [0,1].")
    return ((y, 1 - y, F(0)), (y, F(0), 1 - y))


def direct_fiber_oracle(rows):
    """Exact endpoint oracle; it never computes optimal cells or their rank."""
    rows = normalize_rows(rows)
    cuts = {F(0), F(1)}
    for column in (1, 2):
        for first, second in combinations(rows, 2):
            slope = (first[0] - first[column]) - (
                second[0] - second[column]
            )
            intercept = first[column] - second[column]
            if slope:
                y = -intercept / slope
                if 0 <= y <= 1:
                    cuts.add(y)
    cuts = sorted(cuts)
    checks = sorted(
        set(cuts + [(left + right) / 2 for left, right in zip(cuts, cuts[1:])])
    )
    examined = 0
    for y in checks:
        examined += 1
        first, second = fiber_endpoints(y)
        first_optimal = argmins(rows, first)
        second_optimal = argmins(rows, second)
        if not first_optimal.intersection(second_optimal):
            return {
                "sufficient": False,
                "partition_points": len(checks),
                "examined_points": examined,
                "failure_witness": {
                    "y": str(y),
                    "endpoint_laws": [[str(x) for x in p] for p in (first, second)],
                    "endpoint_argmins": [
                        sorted(first_optimal),
                        sorted(second_optimal),
                    ],
                },
            }
    return {
        "sufficient": True,
        "partition_points": len(checks),
        "examined_points": examined,
        "failure_witness": None,
    }


def exact_profile(rows, names, law):
    rows = normalize_rows(rows)
    law = tuple(F(value) for value in law)
    if min(law) < 0 or sum(law) != 1:
        raise ValueError("Invalid probability law.")
    values = losses(rows, law)
    ranking = [
        [names[i] for i, cost in enumerate(values) if cost == value]
        for value in sorted(set(values))
    ]
    return {
        "law": [str(value) for value in law],
        "y": str(law[0]),
        "losses": {name: str(value) for name, value in zip(names, values)},
        "preference_groups_best_first": ranking,
        "optimal_actions": ranking[0],
    }


def fiber_profile(rows, names, y):
    endpoints = fiber_endpoints(y)
    common = argmins(rows, endpoints[0]).intersection(argmins(rows, endpoints[1]))
    return {
        "y": str(F(y)),
        "endpoint_profiles": [exact_profile(rows, names, p) for p in endpoints],
        "common_optimal_actions": [names[i] for i in range(len(names)) if i in common],
        "singleton_fiber": endpoints[0] == endpoints[1],
    }


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def focused_examples():
    # Nonconstant optimal action; a strictly dominated row has a hidden ranking.
    names = ("A", "B", "D")
    rows = normalize_rows(((0, 1, 1), (1, 0, 0), (F(1, 4), F(5, 4), F(9, 4))))
    predicted, essential = geometry_predicate(rows)
    direct = direct_fiber_oracle(rows)
    check(predicted and direct["sufficient"] and essential == [0, 1], "Positive case")
    check(all(d > a for d, a in zip(rows[2], rows[0])), "Strict domination")
    first = exact_profile(rows, names, (F(2, 3), F(1, 3), 0))
    second = exact_profile(rows, names, (F(2, 3), 0, F(1, 3)))
    check(first["preference_groups_best_first"] == [["A"], ["D"], ["B"]], "First rank")
    check(second["preference_groups_best_first"] == [["A"], ["B"], ["D"]], "Second rank")
    profiles = {str(y): fiber_profile(rows, names, y) for y in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))}
    expected_common = {"0": ["B"], "1/4": ["B"], "1/2": ["A", "B"], "3/4": ["A"], "1": ["A"]}
    for y, expected in expected_common.items():
        check(profiles[y]["common_optimal_actions"] == expected, f"Positive fiber {y}")

    # SOME optimal action can survive loss of the complete optimal-action set.
    boundary_rows = normalize_rows(((0, 0, 0), (0, 1, 0)))
    boundary_names = ("A", "B")
    boundary = fiber_profile(boundary_rows, boundary_names, F(1, 2))
    check(geometry_predicate(boundary_rows) == (True, [0]), "Inactive boundary action")
    check(direct_fiber_oracle(boundary_rows)["sufficient"], "Common optimum with extra ties")
    check(boundary["common_optimal_actions"] == ["A"], "Common A")
    check(boundary["endpoint_profiles"][0]["optimal_actions"] == ["A"], "Strict endpoint")
    check(boundary["endpoint_profiles"][1]["optimal_actions"] == ["A", "B"], "Tied endpoint")

    # Failure in the interior, although the extreme observation is a singleton.
    crossing_rows = normalize_rows(((0, 1, 0), (0, 0, 1)))
    crossing_names = ("A", "B")
    check(geometry_predicate(crossing_rows) == (False, [0, 1]), "Crossing prediction")
    check(not direct_fiber_oracle(crossing_rows)["sufficient"], "Crossing oracle")
    crossing = [
        exact_profile(crossing_rows, crossing_names, (F(1, 3), F(1, 2), F(1, 6))),
        exact_profile(crossing_rows, crossing_names, (F(1, 3), F(1, 6), F(1, 2))),
    ]
    check(crossing[0]["optimal_actions"] == ["B"], "First strict interior optimum")
    check(crossing[1]["optimal_actions"] == ["A"], "Second strict interior optimum")
    singleton = fiber_profile(crossing_rows, crossing_names, F(1))
    check(singleton["singleton_fiber"], "Boundary singleton")
    check(singleton["common_optimal_actions"] == ["A", "B"], "Boundary tie")

    # One-sided differences: sign is retained while magnitude need not be.
    one_sided_rows = normalize_rows(((0, 1, 2), (0, 0, 0)))
    check(geometry_predicate(one_sided_rows) == (True, [1]), "One-sided exception")
    check(direct_fiber_oracle(one_sided_rows)["sufficient"], "One-sided oracle")
    one_sided = fiber_profile(one_sided_rows, crossing_names, F(1, 2))
    one_sided_boundary = fiber_profile(one_sided_rows, crossing_names, F(1))
    check(one_sided["endpoint_profiles"][0]["losses"]["A"] == "1/2", "First magnitude")
    check(one_sided["endpoint_profiles"][1]["losses"]["A"] == "1", "Second magnitude")
    check(one_sided["common_optimal_actions"] == ["B"], "One-sided strict preference")
    check(one_sided_boundary["common_optimal_actions"] == ["A", "B"], "One-sided boundary tie")

    # The geometric reduction must merge exact duplicate rows explicitly.
    duplicate_rows = normalize_rows(((0, 1, 1), (0, 1, 1), (1, 0, 0)))
    duplicate_names = ("A", "A_copy", "B")
    check(geometry_predicate(duplicate_rows) == (True, [0, 2]), "Duplicate merge")
    check(direct_fiber_oracle(duplicate_rows)["sufficient"], "Duplicate oracle")
    duplicate_tie = fiber_profile(duplicate_rows, duplicate_names, F(1, 2))
    check(duplicate_tie["common_optimal_actions"] == list(duplicate_names), "Duplicate ties")

    return {
        "strictly_dominated_action": {
            "loss_rows": {name: [str(x) for x in row] for name, row in zip(names, rows)},
            "essential_representatives": ["A", "B"],
            "strict_componentwise_dominance": "D has greater loss than A in every state.",
            "same_summary_different_full_preferences": [first, second],
            "nonconstant_selector": "Choose B for y<1/2, A for y>1/2, either at y=1/2.",
            "tie_and_boundary_profiles": profiles,
            "all_essential_hidden_coefficients_equal": True,
            "all_menu_hidden_coefficients_equal": False,
        },
        "some_optimum_vs_complete_tie_set": {
            "loss_rows": [[str(x) for x in row] for row in boundary_rows],
            "fiber": boundary,
            "fixed_tie_policy": "A policy prioritizing B at ties selects different actions at these identical summaries.",
        },
        "strict_interior_failure_and_boundary_singleton": {
            "loss_rows": [[str(x) for x in row] for row in crossing_rows],
            "global_service": False,
            "interior_laws": crossing,
            "boundary_fiber": singleton,
        },
        "one_sided_sign_exception": {
            "loss_rows": [[str(x) for x in row] for row in one_sided_rows],
            "interior_fiber": one_sided,
            "boundary_fiber": one_sided_boundary,
            "interpretation": "The gap is positive for y<1 and zero at y=1; its magnitude is not generally identified.",
        },
        "duplicate_rows": {
            "loss_rows": [[str(x) for x in row] for row in duplicate_rows],
            "essential_representatives": ["A", "B"],
            "tie_fiber": duplicate_tie,
        },
    }


def exhaustive_menus():
    row_set = list(product((-1, 0, 1), repeat=3))
    records = []
    disagreements = []
    for size in (2, 3):
        count = sufficient_count = examined_points = 0
        for rows in combinations(row_set, size):
            predicted, essential = geometry_predicate(rows)
            direct = direct_fiber_oracle(rows)
            actual = direct["sufficient"]
            count += 1
            sufficient_count += actual
            examined_points += direct["examined_points"]
            if predicted != actual:
                disagreements.append(
                    {
                        "rows": rows,
                        "essential_indices": essential,
                        "geometry_prediction": predicted,
                        "direct_oracle": direct,
                    }
                )
        records.append(
            {
                "actions": size,
                "menus": count,
                "sufficient_menus": sufficient_count,
                "oracle_observation_points_examined": examined_points,
            }
        )
    check(
        [(r["menus"], r["sufficient_menus"]) for r in records] == [(351, 204), (2925, 1224)],
        "Exact enumeration counts changed.",
    )
    check(not disagreements, f"Geometric/oracle disagreements: {disagreements[:3]}")
    return {
        "row_entries": [-1, 0, 1],
        "distinct_available_rows": len(row_set),
        "menus": records,
        "total_menus": sum(record["menus"] for record in records),
        "predicate_disagreements": len(disagreements),
    }


def run():
    return {
        "schema": "value_logic.p3_02.decision_geometry_development.v1",
        "status": "DEVELOPMENT",
        "passed": True,
        "contributor": "ChatGPT (GPT-6 Astra Pro), internal same-model independent reconstruction",
        "time_credit": "No additional or duplicate principal-session credit.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": {
            "domain": "Full real normalized simplex Delta_3",
            "observation": "The fixed exact linear expectation y=p_1",
            "losses": "Known finite rational action-loss rows",
            "service": "Return SOME Bayes-optimal action, preserving no prescribed tie policy",
            "excluded": [
                "Arbitrary nonlinear reports or convex elicitation dimension",
                "Restricted or nonconvex law domains",
                "Learning, paid acquisition, resource-optimality or final challenge evidence",
            ],
        },
        "independent_oracle_description": {
            "geometric_predicate": (
                "Merge duplicate rows. Find each closed optimal cell by rational half-plane "
                "intersection; positive area identifies an essential row. Test equality of "
                "the essential rows' coefficients along hidden direction (0,1,-1)."
            ),
            "direct_oracle": (
                "For every exact rational pairwise crossing value on either endpoint curve "
                "(y,1-y,0) and (y,0,1-y), and each intervening interval midpoint, compute "
                "endpoint argmin sets directly and test their intersection. A common endpoint "
                "action is optimal throughout the whole fiber by linearity. Include y=0 "
                "and y=1 and all ties; a negative case may stop at its first witnessed failure."
            ),
            "independence_scope": (
                "The endpoint oracle does not call the cell or rank calculation. Both "
                "calculations were written by the same model; this is internal reconstruction, "
                "not independent-model validation."
            ),
        },
        "exhaustive": exhaustive_menus(),
        "focused_examples": focused_examples(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write exact DEVELOPMENT JSON here.")
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "passed": result["passed"],
                    "total_menus": result["exhaustive"]["total_menus"],
                    "predicate_disagreements": result["exhaustive"]["predicate_disagreements"],
                    "output": str(args.output),
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
