"""Exact planning probes for N01 recurrence C3; not F11's native producer.

Codex (GPT-6), October 2, 2026. Standard library only.
The scalar semantic oracle checks a quadratic on its entire rational interval.
The outer-profile reference enumerates geometric vertices independently of
dual-bound enumeration. No timing/speed or unrestricted theorem is inferred.
Run: python -X faulthandler -m v2.checks.n01_recurrence
"""

from fractions import Fraction as Q
from itertools import combinations, product
import json


def clip(q):
    return min(Q(1), max(Q(0), q))


def equilibrium(a, b, k, tau=Q(0)):
    q = clip(k * (a - tau) / (1 + k * b))
    return q, a - b * q


def direct_regret(b, price, calibration=Q(0), saturated=False):
    q1, z1 = equilibrium(Q(1), b, Q(1))
    q2, z2 = equilibrium(Q(1), b, Q(2))
    assert (b <= Q(1, 2)) == saturated or b == Q(1, 2)
    return (z1 + price * q1) - (z2 + price * q2) + calibration


def quadratic_minimum(a, b, c, lo, hi):
    """Exact minimum and rational witness, including degenerate quadratics."""
    points = [lo, hi]
    if a > 0 and lo < -b / (2 * a) < hi:
        points.append(-b / (2 * a))
    return min((a * x * x + b * x + c, x) for x in points)


def semantic_leq(b_lo, b_hi, effective_price, budget):
    """All-b comparison, without a sampled or radical stationary-point oracle.

    Clear the positive denominator of (b-price)/((1+b)*(1+2*b)).
    If false, the returned rational b is an actual violating response model.
    """
    value, witness = quadratic_minimum(
        2 * budget, 3 * budget - 1, budget + effective_price, b_lo, b_hi
    )
    return value >= 0, witness


def graph(x):
    return x / (2 - x)


def tangent(t):
    return 2 / (2 - t) ** 2, -(t * t) / (2 - t) ** 2


def chord(lo, hi):
    return 2 / ((2 - lo) * (2 - hi)), -lo * hi / ((2 - lo) * (2 - hi))


def profile_rows(lo, hi, knots):
    rows = [(-Q(1), Q(0), -lo), (Q(1), Q(0), hi)]
    rows.extend((m, -Q(1), -d) for m, d in map(tangent, knots))
    m, d = chord(lo, hi)
    rows.append((-m, Q(1), d))
    return rows


def polygon_vertices(rows):
    vertices = set()
    for (a, b, c), (d, e, f) in combinations(rows, 2):
        determinant = a * e - b * d
        if determinant:
            x, y = (c * e - b * f) / determinant, (a * f - c * d) / determinant
            if all(u * x + v * y <= w for u, v, w in rows):
                vertices.add((x, y))
    assert vertices
    return vertices


def dual_upper_bound(rows, objective):
    """Enumerate sound two-row dual combinations; separate from vertex oracle."""
    cx, cy = objective
    candidates = []
    for i, j in combinations(range(len(rows)), 2):
        ax, ay, rhs_a = rows[i]
        bx, by, rhs_b = rows[j]
        determinant = ax * by - ay * bx
        if not determinant:
            continue
        wa = (cx * by - cy * bx) / determinant
        wb = (ax * cy - ay * cx) / determinant
        if wa >= 0 and wb >= 0:
            assert wa * ax + wb * bx == cx
            assert wa * ay + wb * by == cy
            candidates.append((wa * rhs_a + wb * rhs_b, i, j, wa, wb))
    assert candidates
    return min(candidates)


def run():
    counts = {}
    fixed_points = 0
    for a, b, k, tau in product(
        (Q(0), Q(1, 4), Q(1, 2), Q(1)),
        (Q(0), Q(1, 4), Q(1, 2), Q(1)),
        (Q(1, 2), Q(1), Q(2), Q(4)),
        (Q(0), Q(1, 4), Q(1, 2), Q(1)),
    ):
        if b > a:
            continue
        q, r = equilibrium(a, b, k, tau)
        assert Q(0) <= q <= 1 and Q(0) <= r <= 1
        assert q == clip(k * (r - tau))
        fixed_points += 1
    counts["fixed_point_cases"] = fixed_points

    q = Q(0)
    raw = []
    for _ in range(8):
        raw.append(q)
        q = clip(2 * (1 - q))
    assert raw == [Q(0), Q(1)] * 4
    q = Q(0)
    errors = []
    for _ in range(8):
        errors.append(abs(q - Q(2, 3)))
        q = Q(2, 3) * q + Q(1, 3) * clip(2 * (1 - q))
    assert all(new <= Q(2, 3) * old for old, new in zip(errors, errors[1:]))
    counts["dynamic_controls"] = 2

    lo, hi = Q(1, 2), Q(2, 3)
    identity_count = 0
    for j, k in product(range(31), repeat=2):
        x = lo + (hi - lo) * Q(j, 30)
        t = lo + (hi - lo) * Q(k, 30)
        m, d = tangent(t)
        assert graph(x) - m * x - d == 2 * (x - t) ** 2 / ((2 - x) * (2 - t) ** 2)
        cm, cd = chord(lo, hi)
        assert cm * x + cd - graph(x) == 2 * (x - lo) * (hi - x) / ((2 - x) * (2 - lo) * (2 - hi))
        # The exact 2-by-2 conic boundary has determinant zero.
        assert (4 - 2 * x) * (1 + graph(x)) - 4 == 0
        identity_count += 1
    counts["rational_identity_triples"] = identity_count

    comparisons = 0
    max_errors = {}
    for n in (1, 2, 4, 8, 16):
        knots = [lo + (hi - lo) * Q(i, n) for i in range(n + 1)]
        rows = profile_rows(lo, hi, knots)
        vertices = polygon_vertices(rows)
        largest_verified_error = Q(0)
        for j in range(33):
            price = Q(j, 224)  # [0,1/7], including both endpoints.
            objective = (1 + price, -(1 + 2 * price))
            upper, x, y = max((objective[0] * x + objective[1] * y, x, y) for x, y in vertices)
            dual = dual_upper_bound(rows, objective)
            assert dual[0] == upper
            assert semantic_leq(Q(1, 2), Q(1), price, upper)[0]
            b = 1 / x - 1
            actual_at_x = direct_regret(b, price)
            error = upper - actual_at_x
            assert Q(0) <= error <= Q(27, 3584 * n * n)
            largest_verified_error = max(largest_verified_error, error)
            comparisons += 1
        max_errors[str(n)] = str(largest_verified_error)
    counts["dual_polygon_continuum_comparisons"] = comparisons

    # Revised, imperfect-calibration fixture: endpoints pass but an interior
    # model defeats their conclusion. The scalar oracle covers the interval.
    price, budget = Q(1, 16), Q(63, 400)
    assert direct_regret(Q(1, 2), price) == Q(7, 48)
    assert direct_regret(Q(9, 10), price) == Q(335, 2128)
    assert direct_regret(Q(13, 16), price) == Q(32, 203)
    assert all(direct_regret(b, price) < budget for b in (Q(1, 2), Q(9, 10)))
    accepted, witness = semantic_leq(Q(1, 2), Q(9, 10), price, budget)
    assert not accepted and direct_regret(witness, price) > budget

    # A relational calibration premise supports the decision; withdrawing it
    # leaves bounded absolute errors but loses this particular guarantee.
    assert semantic_leq(Q(1, 2), Q(9, 10), price - Q(1, 8), Q(1, 5))[0]
    accepted_after, after_witness = semantic_leq(Q(1, 2), Q(9, 10), price, Q(1, 5) - Q(1, 10))
    assert not accepted_after
    assert direct_regret(after_witness, price, Q(1, 10)) > Q(1, 5)
    counts["calibration_withdrawal_controls"] = 2

    # Saturation: direct controller evaluation supplies a different path from
    # the x-coordinate derivation. Each branch is convex, so its endpoint
    # maximum is an exact interval bound (also verify the cleared polynomials).
    sat_candidates = []
    for x in (Q(2, 3), Q(5, 6), Q(1)):
        b = 1 / x - 1
        regret = direct_regret(b, Q(1), min(Q(1, 6), 1 - x), saturated=True)
        sat_candidates.append(regret)
    assert sat_candidates == [Q(0), Q(1, 30), Q(0)]
    assert quadratic_minimum(-Q(2), Q(1, 30) + 3 - Q(1, 6), -Q(1), Q(2, 3), Q(5, 6))[0] == 0
    assert quadratic_minimum(-Q(1), Q(1, 30) + 2, -Q(1), Q(5, 6), Q(1))[0] == 0
    x, y, t = Q(5, 6), Q(3, 4), Q(1, 6)
    assert y == Q(3, 2) * x - Q(1, 2) and y < 2 - 1 / x
    assert t <= Q(1, 6) and t <= 1 - x
    assert 2 * x - y - 1 + t == Q(1, 12)
    assert Q(1, 30) < Q(1, 20) < Q(1, 12)
    counts["saturation_composition_counterexample"] = 1

    # Old exact observation matches two worlds with opposite revision value.
    observation_worlds = []
    for a, b in ((Q(1, 2), Q(0)), (Q(1), Q(1))):
        q1, r1 = equilibrium(a, b, Q(1))
        q2, r2 = equilibrium(a, b, Q(2))
        assert (q1, r1) == (Q(1, 2), Q(1, 2))
        observation_worlds.append((r1 + q1 / 4, r2 + q2 / 4))
    assert observation_worlds == [(Q(5, 8), Q(3, 4)), (Q(5, 8), Q(1, 2))]
    counts["indistinguishable_observation_worlds"] = 2

    return {
        "status": "PASS",
        "scope": "exact planning controls; no native producer or speed claim",
        "counts": counts,
        "outer_profile_max_verified_error": max_errors,
        "interior_countermodel": str(witness),
        "withdrawal_countermodel": str(after_witness),
        "saturation_true_bound": "1/30",
        "saturation_relaxed_bound": "1/12",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
