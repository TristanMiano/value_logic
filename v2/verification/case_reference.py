"""Independent F13 polynomial integration and finite-path semantic controls.

Does not import the native adapters, their loss formulas, or proof machinery.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations


def multiply(a, b):
    out = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return tuple(out)


def polynomial(a, b, u, v):
    g = (Q(0), Q(0), Q(30), Q(-60), Q(30))
    h = (Q(-2688),)
    for root in (Q(0), Q(1, 4), Q(1, 2), Q(1, 2), Q(3, 4), Q(1)):
        h = multiply(h, (-root, Q(1)))
    out = [Q(0)]*7
    out[0], out[1] = Q(a), Q(b)
    for i, coefficient in enumerate(g):
        out[i] += Q(u)*coefficient
    for i, coefficient in enumerate(h):
        out[i] += Q(v)*coefficient
    return tuple(out)


def evaluate(coefficients, x):
    total = Q(0)
    for coefficient in reversed(coefficients):
        total = total*x+coefficient
    return total


def integral(coefficients):
    return sum((coefficient/Q(i+1) for i, coefficient in enumerate(coefficients)), Q(0))


def vertices(u_cap, v_cap, joint_cap):
    rows = [(Q(1), Q(0), u_cap), (Q(-1), Q(0), u_cap),
            (Q(0), Q(1), v_cap), (Q(0), Q(-1), v_cap)]
    if joint_cap is not None:
        rows += [(Q(1, 4), Q(-1), joint_cap), (Q(-1, 4), Q(1), joint_cap)]
    points = set()
    for (a, b, c), (d, e, f) in combinations(rows, 2):
        determinant = a*e-b*d
        if determinant:
            x, y = (c*e-b*f)/determinant, (a*f-c*d)/determinant
            if all(s*x+t*y <= bound for s, t, bound in rows):
                points.add((x, y))
    if not points:
        raise ValueError('Expected a bounded nonempty source, including degenerate sources.')
    return tuple(sorted(points))


def scientific_bound(source, price):
    """Execute Simpson and four-node rule on expanded polynomials at all vertices."""
    # Solve this four-equation integration system independently of weights().
    nodes = (Q(0), Q(1, 2), Q(1), Q(1, 8))
    basis = [polynomial(*(Q(i == j) for i in range(4))) for j in range(4)]
    matrix = [[evaluate(p, x) for x in nodes]+[integral(p)] for p in basis]
    for i in range(4):
        pivot = next(j for j in range(i, 4) if matrix[j][i])
        matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
        divisor = matrix[i][i]
        matrix[i] = [x/divisor for x in matrix[i]]
        for j in range(4):
            if j != i:
                coefficient = matrix[j][i]
                matrix[j] = [x-coefficient*y for x, y in zip(matrix[j], matrix[i])]
    weights = [row[-1] for row in matrix]
    results = []
    for u, v in vertices(source.u_cap, source.v_cap, source.joint_cap):
        poly = polynomial(0, 0, u, v)
        truth = integral(poly)
        simpson = (evaluate(poly, Q(0))+4*evaluate(poly, Q(1, 2))+evaluate(poly, Q(1)))/6
        fourth = sum((w*evaluate(poly, x) for w, x in zip(weights, nodes)), Q(0))
        results.append((abs(simpson-truth)+3*price-abs(fourth-truth)-4*price, (u, v)))
    return max(results)


def execute(failures, order, costs, penalty):
    charge = Q(0)
    attempted = []
    for index in order:
        charge += costs[index]
        attempted.append(index)
        if not failures[index]:
            return charge, False, tuple(attempted)
    return charge+penalty, True, tuple(attempted)


def expected(population, order, costs, penalty):
    loss = unresolved = Q(0)
    for failures, probability in population.items():
        charge, missing, _ = execute(failures, order, costs, penalty)
        loss += probability*charge
        unresolved += probability*missing
    return loss, unresolved


def all_orders(k):
    return tuple(order for size in range(k+1) for order in permutations(range(k), size))


def choose(population, costs, penalty, fallback_cost):
    candidates = [(expected(population, order, costs, penalty)[0],
                   expected(population, order, costs, penalty)[1], len(order), order)
                  for order in all_orders(len(costs))]
    # Lower unresolved rate wins equal-cost ties, then fewer attempts, then order.
    candidates.append((fallback_cost, Q(0), 0, None))
    return min(candidates, key=lambda x: (x[0], x[1], x[2], () if x[3] is None else x[3]))
