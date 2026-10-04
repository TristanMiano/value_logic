"""Ordinary exact linear summaries and path matrices for F13's optional audit.

Research controls, not native proofs or an empirical calibration procedure.
Contributor: Codex (GPT-6), October 4, 2026.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations, product

from . import case_reference as R


def rank(rows):
    """Exact elimination; callers construct rows from direct world execution."""
    matrix = [list(map(Q, row)) for row in rows]
    if not matrix:
        return 0
    columns = len(matrix[0])
    if any(len(row) != columns for row in matrix):
        raise ValueError('Ragged matrix.')
    pivot = 0
    for column in range(columns):
        selected = next((i for i in range(pivot, len(matrix)) if matrix[i][column]), None)
        if selected is None:
            continue
        matrix[pivot], matrix[selected] = matrix[selected], matrix[pivot]
        divisor = matrix[pivot][column]
        matrix[pivot] = [x/divisor for x in matrix[pivot]]
        for i in range(pivot+1, len(matrix)):
            factor = matrix[i][column]
            if factor:
                matrix[i] = [x-factor*y for x, y in zip(matrix[i], matrix[pivot])]
        pivot += 1
        if pivot == len(matrix):
            break
    return pivot


def path_rows(costs, penalty, distributions=False, subsets=False):
    """Linear queries on p_world-p_all_success, not a prefix-moment formula."""
    worlds = tuple(product((0, 1), repeat=len(costs)))
    orders = R.all_orders(len(costs)) if subsets else permutations(range(len(costs)))
    rows = []
    for order in orders:
        losses = tuple(R.execute(world, order, costs, penalty)[0] for world in worlds)
        if distributions:
            for value in sorted(set(losses)):
                rows.append(tuple(Q(loss == value)-Q(losses[0] == value) for loss in losses[1:]))
        else:
            rows.append(tuple(loss-losses[0] for loss in losses[1:]))
    return rows


def elementary(values, degree):
    result = [Q(1)]+[Q(0)]*degree
    for value in values:
        for j in range(degree, 0, -1):
            result[j] += value*result[j-1]
    return result[degree]


def retain(population, costs, penalty):
    """Fixed positive prices only; keep one base cost and non-chain residuals."""
    k = len(costs)
    if k < 2 or any(c <= 0 for c in costs):
        raise ValueError('This compression requires at least two positive costs.')
    moments = {
        subset: sum((p for world, p in population.items() if all(world[i] for i in subset)), Q(0))
        for size in range(1, k) for subset in combinations(range(k), size)
    }
    coefficients = {}
    for size in range(1, k):
        chain = tuple(range(size))
        coefficients[size] = (moments[chain]-sum(
            (coefficients[j]*elementary(costs[:size], j) for j in range(1, size)), Q(0)
        ))/elementary(costs[:size], size)
    residuals = {}
    for subset, value in moments.items():
        if subset != tuple(range(len(subset))):
            residuals[subset] = value-sum(
                (coefficients[j]*elementary(tuple(costs[i] for i in subset), j)
                 for j in range(1, len(subset)+1)), Q(0))
    base = R.expected(population, tuple(range(k)), costs, penalty)[0]
    return base, residuals


def recover(summary, order, costs):
    base, residuals = summary
    return base+costs[order[0]]-costs[0]+sum(
        (costs[index]*residuals.get(tuple(sorted(order[:j])), Q(0))
         for j, index in enumerate(order) if j), Q(0))


def identified_law(t, mean=Q(9, 4), marginal=Q(1, 2), penalty=Q(4)):
    """Three-bit law from a complete equal mean profile and fixed marginals."""
    b = mean-1
    mass = (1-6*marginal+3*b-(3*penalty+1)*t,
            3*marginal-2*b+(2*penalty+1)*t,
            b-marginal-(penalty+1)*t, t)
    if any(p < 0 for p in mass):
        raise ValueError('No probability law at this point in the summary fiber.')
    return {bits: mass[sum(bits)] for bits in product((0, 1), repeat=3)}


def independent_law(failures):
    population = {}
    for bits in product((0, 1), repeat=len(failures)):
        weight = Q(1)
        for bit, probability in zip(bits, failures):
            weight *= probability if bit else 1-probability
        population[bits] = weight
    return population


def independent_order(failures, costs, penalty=None):
    eligible = [i for i, f in enumerate(failures) if f < 1
                and (penalty is None or costs[i] < penalty*(1-f))]
    ordered = sorted(eligible, key=lambda i: (costs[i]/(1-failures[i]), i))
    if penalty is None:
        ordered += [i for i, f in enumerate(failures) if f == 1]
    return tuple(ordered)
