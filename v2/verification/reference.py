"""Exact geometric reference and direct scientific execution.

Shares only the public input contract. It imports neither native ASTs nor
producer formulas, dual solvers, normalization, certificates or answer tables.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations

from .model import Evidence, InputError, Query


@dataclass(frozen=True)
class Reference:
    maximum: Q
    witness: tuple[Q, Q]
    candidate_count: int
    domain: str = 'full_source'
    target_unit_reduct_same: bool = True


def task_losses(point):
    """Evaluate the polynomial, quadrature algorithms, integral and sample cost."""
    if len(point) != 2 or any(isinstance(x, bool) or not isinstance(x, (int, Q)) for x in point):
        raise InputError('Reference execution requires two exact rational coordinates.')
    beta, gamma = map(Q, point)
    quadratic, quartic = 6 * beta + 60 * gamma, -30 * gamma
    def f(t):
        return Q(7, 3) - Q(2, 5) * t + quadratic * t * t + quartic * t**4
    integral = Q(7, 3) - Q(1, 5) + quadratic / 3 + quartic / 5
    def trapezoid(n):
        return ((f(Q(0)) + f(Q(1))) / 2
                + sum((f(Q(k, n)) for k in range(1, n)), Q(0))) / n
    t1, t2, t4 = trapezoid(1), trapezoid(2), trapezoid(4)
    estimates = {'T1': (t1, 2), 'T2': (t2, 3),
                 'R': ((4 * t2 - t1) / 3, 3), 'F': (t4, 5)}
    return {key: abs(value - integral) + Q(count, 32)
            for key, (value, count) in estimates.items()}


def source_halfplanes(evidence: Evidence):
    evidence.validate()
    rows = [(Q(1), Q(0), Q(1)), (Q(-1), Q(0), Q(1)),
            (Q(0), Q(1), Q(1)), (Q(0), Q(-1), Q(1))]
    if evidence.plus is not None:
        rows.append((Q(1), Q(1), Q(evidence.plus)))
    if evidence.minus is not None:
        rows.append((Q(-1), Q(-1), Q(evidence.minus)))
    if evidence.beta is not None:
        rows.extend(((Q(1), Q(0), Q(evidence.beta)),
                     (Q(-1), Q(0), Q(evidence.beta))))
    if evidence.gamma is not None:
        rows.extend(((Q(0), Q(1), Q(evidence.gamma)),
                     (Q(0), Q(-1), Q(evidence.gamma))))
    return tuple(rows)


def feasible(evidence, point):
    return all(a * point[0] + b * point[1] <= c
               for a, b, c in source_halfplanes(evidence))


def reference(evidence: Evidence, query: Query):
    query.validate()
    rows = source_halfplanes(evidence)
    # Independently declared zero-error lines from the scientific specification.
    # Multipliers avoid importing the producer's scaled coefficient vectors.
    action_line = {'T1': (1, 1), 'T2': (4, 1), 'R': (0, 1)}[query.action]
    boundaries = rows + ((Q(action_line[0]), Q(action_line[1]), Q(0)),
                          (Q(16), Q(1), Q(0)))
    points = {(Q(0), Q(0))}
    for left, right in combinations(boundaries, 2):
        a, b, c = left
        d, e, f = right
        determinant = a * e - b * d
        if not determinant:
            continue
        point = ((c * e - b * f) / determinant,
                 (a * f - c * d) / determinant)
        if all(r * point[0] + s * point[1] <= t for r, s, t in rows):
            points.add(point)
    scored = []
    for point in sorted(points):
        losses = task_losses(point)
        scored.append((losses[query.action] - losses['F'], point))
    maximum, witness = max(scored)
    return Reference(maximum, witness, len(points))
