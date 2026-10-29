"""Development LP witness producer: numerical proposals, exact acceptance.

No assertion of a complete exact LP algorithm is made. Failure to reconstruct
raises an exception. Only an exact Farkas vector denotes an empty polyhedron.
The separately frozen s19 verifier does not import this module or SciPy.
"""
from fractions import Fraction as F
import itertools


def dot(a, b):
    if len(a) != len(b):
        raise ValueError('dot dimension')
    return sum((x*y for x, y in zip(a, b)), F(0))


def linear_solution(rows, rhs, width, free=None):
    """Rational RREF; retain supplied values for free coordinates."""
    if len(rows) != len(rhs) or any(len(r) != width for r in rows):
        raise ValueError('linear system dimension')
    a = [list(map(F, r))+[F(b)] for r, b in zip(rows, rhs)]
    pivots = []
    at = 0
    for col in range(width):
        pivot = next((r for r in range(at, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[at], a[pivot] = a[pivot], a[at]
        scale = a[at][col]
        a[at] = [v/scale for v in a[at]]
        for r in range(len(a)):
            if r != at and a[r][col]:
                scale = a[r][col]
                a[r] = [x-scale*y for x, y in zip(a[r], a[at])]
        pivots.append(col)
        at += 1
    if any(all(v == 0 for v in row[:-1]) and row[-1] for row in a):
        return None
    result = [F(0)]*width if free is None else list(map(F, free))
    for r, col in enumerate(pivots):
        result[col] = a[r][-1]-sum((a[r][j]*result[j]
            for j in range(width) if j not in pivots), F(0))
    return result


def approx(values):
    return [F(float(v)).limit_denominator(10**8) for v in values]


def feasible(rows, rhs, point):
    return all(dot(row, point) <= bound for row, bound in zip(rows, rhs))


def conic_from_support(columns, target, proposed):
    """Recover an exact nonnegative combination, or fail closed."""
    width = len(columns)
    if not any(target):
        return [F(0)]*width
    direct = approx(proposed)
    if all(v >= 0 for v in direct) and all(
            sum((direct[j]*columns[j][i] for j in range(width)), F(0)) == t
            for i, t in enumerate(target)):
        return direct
    support = [j for j, v in enumerate(proposed) if v > 1e-9]
    # A basic numerical dual normally already has a small support. Enumeration
    # here is a development fallback, not charged as a polynomial LP solver.
    if len(support) > 24:
        raise RuntimeError('dual support too large for reconstruction budget')
    for size in range(1, min(len(target), len(support))+1):
        for ids in itertools.combinations(support, size):
            subrows = [[columns[j][i] for j in ids] for i in range(len(target))]
            z = linear_solution(subrows, target, size)
            if z is not None and all(v >= 0 for v in z):
                dense = [F(0)]*width
                for j, value in zip(ids, z):
                    dense[j] = value
                return dense
    raise RuntimeError('cannot reconstruct exact nonnegative dual')


def minimize(rows, rhs, objective):
    """Return exact attained minimum plus dual, or exact infeasibility proof."""
    import scipy.optimize
    rows = [list(map(F, r)) for r in rows]
    rhs = list(map(F, rhs))
    objective = list(map(F, objective))
    d = len(objective)
    if d < 1 or len(rows) != len(rhs) or any(len(r) != d for r in rows):
        raise ValueError('LP shape')
    result = scipy.optimize.linprog(list(map(float, objective)),
        A_ub=[[float(v) for v in r] for r in rows] or None,
        b_ub=list(map(float, rhs)) or None, bounds=[(None, None)]*d,
        method='highs-ds')
    if result.status == 2:
        # Ask separately for a normalized Farkas vector. A numerical
        # infeasibility status alone is never emitted as exact evidence.
        eq = [[float(row[j]) for row in rows] for j in range(d)]
        eq.append(list(map(float, rhs)))
        ray = scipy.optimize.linprog([0.0]*len(rows), A_eq=eq,
            b_eq=[0.0]*d+[-1.0], bounds=[(0, None)]*len(rows), method='highs-ds')
        if not ray.success:
            raise RuntimeError('infeasible proposal lacks reconstructable ray')
        z = conic_from_support([r+[b] for r, b in zip(rows, rhs)],
                              [F(0)]*d+[F(-1)], ray.x)
        assert all(v >= 0 for v in z)
        assert all(sum((z[j]*rows[j][h] for j in range(len(rows))), F(0)) == 0
                   for h in range(d))
        assert dot(z, rhs) == -1
        return dict(kind='empty', dual=z, numerical_status=int(result.status))
    if not result.success:
        raise RuntimeError('LP proposal failed: '+str(result.status)+' '+result.message)
    dual = conic_from_support(rows, [-v for v in objective],
                             [-v for v in result.ineqlin.marginals])
    point = approx(result.x)
    bound = -dot(dual, rhs)
    if not (feasible(rows, rhs, point) and dot(objective, point) == bound):
        active = [j for j, v in enumerate(dual) if v > 0]
        candidates = active + [j for j in range(len(rows)) if j not in active
            and abs(float(rhs[j])-sum(float(a)*float(x)
                for a, x in zip(rows[j], result.x))) <= 1e-7]
        for ids in (active, candidates):
            trial = linear_solution([rows[j] for j in ids], [rhs[j] for j in ids],
                                    d, approx(result.x))
            if trial is not None and feasible(rows, rhs, trial) and dot(objective, trial) == bound:
                point = trial
                break
        else:
            raise RuntimeError('cannot reconstruct exact optimal primal')
    assert all(v >= 0 for v in dual)
    assert all(sum((dual[j]*rows[j][h] for j in range(len(rows))), F(0)) == -objective[h]
               for h in range(d))
    assert feasible(rows, rhs, point) and dot(objective, point) == bound
    return dict(kind='optimum', point=point, value=bound, dual=dual,
                numerical_status=int(result.status))


def extrema(rows, rhs, c, offset=F(0)):
    lo = minimize(rows, rhs, c)
    if lo['kind'] == 'empty':
        return dict(kind='empty', dual=lo['dual'])
    hi = minimize(rows, rhs, [-F(v) for v in c])
    if hi['kind'] != 'optimum':
        raise RuntimeError('inconsistent LP proposals')
    return dict(kind='bounded', lo=lo['value']+offset, hi=-hi['value']+offset,
                xlo=lo['point'], xhi=hi['point'], dlo=lo['dual'], dhi=hi['dual'])
