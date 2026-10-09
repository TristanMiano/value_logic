"""Bounded exact algebra probe for the sourced Fermi-Sobolev kernel.

No forecasts are selected. Prefix sums are computed by transparent list scans;
this is not a balanced-tree implementation or a computational benchmark.
"""
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = 0


def check(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(label)


def source_kernel(q, p):
    distance = abs(q - p)
    return 1 + (q - F(1, 2)) * (p - F(1, 2)) + (distance ** 2 - distance + F(1, 6)) / 2


def simplified_kernel(q, p):
    return F(4, 3) + (q * q + p * p) / 2 - max(q, p)


def integrate(coefficients, left, right):
    return sum((c * (right ** (i + 1) - left ** (i + 1)) / (i + 1)
                for i, c in enumerate(coefficients)), F(0))


def feature_inner_product(q, p):
    # h_q(t) = t - 1[t>q], and k(q,p) = 1 + integral h_q h_p.
    cuts = sorted({F(0), q, p, F(1)})
    integral = F(0)
    for left, right in zip(cuts, cuts[1:]):
        midpoint = (left + right) / 2
        u, v = int(midpoint > q), int(midpoint > p)
        integral += integrate((F(u * v), F(-u - v), F(1)), left, right)
    return 1 + integral


def prefix_formula(history, p):
    total = sum((a for q, a in history), F(0))
    first = sum((a * q for q, a in history), F(0))
    second = sum((a * q * q for q, a in history), F(0))
    prefix = sum((a for q, a in history if q <= p), F(0))
    prefix_first = sum((a * q for q, a in history if q <= p), F(0))
    return (F(4, 3) + p * p / 2) * total + second / 2 - p * prefix - (first - prefix_first)


def direct_sum(history, p):
    return sum((a * source_kernel(q, p) for q, a in history), F(0))


def score(history, p, weight, beta):
    return (weight * beta * beta * direct_sum(history, p)
            + (F(1, 2) - p) * weight * weight * beta * beta * source_kernel(p, p))


def quadratic(coefficients, p):
    return sum((c * p ** i for i, c in enumerate(coefficients)), F(0))


def main():
    # All residual coefficients come from valid binary outcomes and
    # nonnegative weights. The first two sum to zero without giving a zero
    # kernel function. Repeated locations later exercise the <= convention.
    records = ((F(0), F(1), 1), (F(1), F(1), 0), (F(1, 2), F(1), 1),
               (F(0), F(3, 2), 0), (F(1), F(0), 1), (F(1, 3), F(5, 4), 0),
               (F(2, 3), F(2), 1), (F(1, 2), F(1), 0), (F(3, 7), F(1, 3), 1),
               (F(1), F(1), 0), (F(0), F(2, 5), 1), (F(1, 3), F(3, 4), 1))
    history = tuple((q, w * (y - q)) for q, w, y in records)
    points = sorted({q for q, w, y in records} | {F(k, 8) for k in range(9)}
                    | {F(1, 3) - F(1, 1024), F(1, 3) + F(1, 1024),
                       F(1, 2) - F(1, 1024), F(1, 2) + F(1, 1024)})
    for q, p in product(points, repeat=2):
        k = source_kernel(q, p)
        check(k == simplified_kernel(q, p), ('source simplification', q, p))
        check(k == feature_inner_product(q, p), ('RKHS feature representation', q, p))
        check(source_kernel(q, q) + source_kernel(p, p) - 2 * k == abs(p - q),
              ('feature squared distance', q, p))
    for p in points:
        diagonal = source_kernel(p, p)
        check(diagonal == F(4, 3) - p * (1 - p), ('diagonal formula', p))
        check(F(13, 12) <= diagonal <= F(4, 3), ('diagonal range', p))
        check(p * (1 - p) * diagonal <= F(13, 48), ('K29-star variance diagonal', p))
    current_weight, beta = F(3, 2), F(2, 3)
    prefix_checks, derivative_extrema = 0, 0
    for length in range(len(history) + 1):
        prefix_history = history[:length]
        total = sum((a for q, a in prefix_history), F(0))
        absolute_total = sum((abs(a) for q, a in prefix_history), F(0))
        lip = current_weight * beta ** 2 * absolute_total + F(11, 6) * current_weight ** 2 * beta ** 2
        for p in points:
            check(prefix_formula(prefix_history, p) == direct_sum(prefix_history, p), ('prefix identity', length, p))
            prefix_checks += 1
        for p, q in combinations(points, 2):
            check(abs(score(prefix_history, q, current_weight, beta) - score(prefix_history, p, current_weight, beta))
                  <= lip * (q - p), ('score Lipschitz across knots', length, p, q))
        cuts = sorted({F(0), F(1)} | {q for q, a in prefix_history})
        for left, right in zip(cuts, cuts[1:]):
            midpoint = (left + right) / 2
            left_sum = sum((a for q, a in prefix_history if q <= midpoint), F(0))
            c2 = -3 * current_weight ** 2 * beta ** 2
            c1 = current_weight * beta ** 2 * total + 3 * current_weight ** 2 * beta ** 2
            c0 = -current_weight * beta ** 2 * left_sum - F(11, 6) * current_weight ** 2 * beta ** 2
            vertex = -c1 / (2 * c2)
            extrema = [left, right] + ([vertex] if left < vertex < right else [])
            for p in extrema:
                check(abs(quadratic((c0, c1, c2), p)) <= lip,
                      ('entire piece derivative bound', length, left, right, p))
                derivative_extrema += 1
        gram = sum((a * b * source_kernel(q, p) for q, a in prefix_history for p, b in prefix_history), F(0))
        feature_norm = total * total
        for left, right in zip(cuts, cuts[1:]):
            midpoint = (left + right) / 2
            tail = sum((a for q, a in prefix_history if q < midpoint), F(0))
            feature_norm += integrate((tail * tail, -2 * total * tail, total * total), left, right)
        check(gram == feature_norm and gram >= 0, ('signed Gram norm', length))
    check(sum((a for q, a in history[:2]), F(0)) == 0, 'cancellation fixture')
    check(prefix_formula(history[:2], F(1, 4)) == F(1, 4), 'zero-total residual is not zero function')
    result = {'status': 'PASS', 'checks': CHECKS,
              'principal_research90_seconds': 0,
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'records': [[str(q), str(w), y] for q, w, y in records],
              'query_point_count': len(points), 'prefix_cases': len(history) + 1,
              'prefix_identity_checks': prefix_checks, 'derivative_extrema_checked': derivative_extrema,
              'kernel_pair_cases': len(points) ** 2,
              'current_weight': str(current_weight), 'beta': str(beta),
              'diagonal_minimum': '13/12', 'diagonal_maximum': '4/3',
              'star_variance_diagonal_maximum': '13/48',
              'correction_derivative_maximum_absolute_value': '11/6',
              'forecaster_implemented': False, 'ordered_data_structure_implemented': False,
              'resource_claim': 'Conditional O(log n) rational comparisons/operations with an augmented balanced ordered tree; no bit/CPU claim.'}
    with (HERE / 'probe_fs_kernel_result.json').open('x') as handle:
        json.dump(result, handle, indent=2, sort_keys=True); handle.write('\n')
    print(json.dumps({k: result[k] for k in ('status', 'checks', 'prefix_cases', 'prefix_identity_checks', 'kernel_pair_cases', 'derivative_extrema_checked')}))


if __name__ == '__main__':
    main()
