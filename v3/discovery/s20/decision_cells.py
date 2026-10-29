"""Exact piecewise-constant loss interface for an existing range bracket."""
from fractions import Fraction as F


def rational(value):
    if not isinstance(value, str):
        raise ValueError('exact rational string required')
    return F(value)


def union(rows):
    answer = []
    for row in rows:
        if not isinstance(row, list) or len(row) != 2:
            raise ValueError('interval shape')
        a, b = map(rational, row)
        if a > b or (answer and a <= answer[-1][1]):
            raise ValueError('unnormalized interval union')
        answer.append((a, b))
    return answer


def cell_witness(ranges, breaks, cell):
    if cell % 2:
        q = breaks[cell//2]
        return q if any(a <= q <= b for a, b in ranges) else None
    left = None if cell == 0 else breaks[cell//2-1]
    right = None if cell == 2*len(breaks) else breaks[cell//2]
    for a, b in ranges:
        lo = a if left is None else max(a, left)
        hi = b if right is None else min(b, right)
        if lo < hi:
            return (lo+hi)/2
        if lo == hi and (left is None or left < lo) and (right is None or lo < right):
            return lo
    return None


def assess(bracket, breakpoints, losses, criterion='loss'):
    cuts = list(map(rational, breakpoints))
    if cuts != sorted(set(cuts)):
        raise ValueError('breakpoints must be strictly increasing')
    if criterion not in ('loss', 'regret'):
        raise ValueError('decision criterion')
    inner, outer = union(bracket['inner']), union(bracket['outer'])
    if any(not any(c <= a <= b <= d for c, d in outer) for a, b in inner):
        raise ValueError('inner outside outer')
    if len(losses) != 2*len(cuts)+1:
        raise ValueError('loss cell count')
    values = [list(map(rational, row)) for row in losses]
    if not values or not values[0] or any(len(row) != len(values[0]) for row in values):
        raise ValueError('action count')
    if criterion == 'regret':
        values = [[v-min(row) for v in row] for row in values]
    known, possible, witnesses = [], [], {}
    for j in range(len(values)):
        q = cell_witness(inner, cuts, j)
        if q is not None:
            known.append(j)
            witnesses[j] = str(q)
        if cell_witness(outer, cuts, j) is not None:
            possible.append(j)
    if not possible:
        return dict(status='INCONSISTENT_BRACKET', criterion=criterion)
    n = len(values[0])
    lower = [max(values[j][a] for j in known) if known else
             min(values[j][a] for j in possible) for a in range(n)]
    upper = [max(values[j][a] for j in possible) for a in range(n)]
    eta = [max(F(0), upper[a]-min(lower[b] for b in range(n) if b != a))
           if n > 1 else F(0) for a in range(n)]
    worst = min(range(n), key=lambda a: (upper[a], a))
    gap = min(range(n), key=lambda a: (eta[a], a))
    irrelevant = [j for j in possible if j not in known and known and
                  all(values[j][a] <= lower[a] for a in range(n))]
    return dict(status='BOUNDED_DECISION', criterion=criterion,
                assumes_nonempty_source=not bool(known),
                known_cells=known, possible_cells=possible, inner_witnesses=witnesses,
                lower=list(map(str, lower)), upper=list(map(str, upper)),
                improvement_bounds=list(map(str, eta)),
                conservative_action=worst, smallest_gap_action=gap,
                certified_optimal_actions=[a for a in range(n) if eta[a] == 0],
                irrelevant_unknown_cells=irrelevant)
