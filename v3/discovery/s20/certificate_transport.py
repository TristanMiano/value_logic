"""Development-only exact outer ranges from retained LP multipliers.

No optimizer, source witness, or exact-range promise for changed premises.
Known coordinate bounds are extracted from the new base constraints.
"""
from fractions import Fraction as F
import importlib.util
from pathlib import Path

_path = Path(__file__).resolve().parent.parent / 's19/range_cert_verify.py'
_spec = importlib.util.spec_from_file_location('transport_verifier', _path)
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)


def dot(a, b):
    if len(a) != len(b):
        raise ValueError('dot shape')
    return sum((x*y for x, y in zip(a, b)), F(0))


def transpose_product(rows, y, dimension):
    if len(rows) != len(y) or any(len(r) != dimension for r in rows):
        raise ValueError('matrix shape')
    if any(v < 0 for v in y):
        raise ValueError('negative multiplier')
    return [sum((w*r[j] for w, r in zip(y, rows)), F(0))
            for j in range(dimension)]


def box_extrema(c, box):
    if len(c) != len(box):
        raise ValueError('box shape')
    if any(l > u for l, u in box):
        raise ValueError('reversed box')
    return (sum((min(v*l, v*u) for v, (l, u) in zip(c, box)), F(0)),
            sum((max(v*l, v*u) for v, (l, u) in zip(c, box)), F(0)))


def implied_box(generator):
    """Use only explicit one-coordinate rows of the *new* base model."""
    dimension = len(generator['c'])
    lower, upper = [None]*dimension, [None]*dimension
    rows = [V.vector(row, dimension) for row in generator['A']]
    rhs = V.vector(generator['b'], len(rows))
    for row, bound in zip(rows, rhs):
        support = [j for j, a in enumerate(row) if a]
        if len(support) != 1:
            continue
        j = support[0]
        value = bound/row[j]
        if row[j] > 0:
            upper[j] = value if upper[j] is None else min(upper[j], value)
        else:
            lower[j] = value if lower[j] is None else max(lower[j], value)
    if any(a is None or b is None for a, b in zip(lower, upper)):
        raise ValueError('new model lacks explicit finite coordinate bounds')
    if any(a > b for a, b in zip(lower, upper)):
        raise ValueError('contradictory explicit coordinate bounds')
    return list(zip(lower, upper))


def local_outer(rows, rhs, c, d, box, old_entry):
    """Bounds hold for every new feasible point, including if none exists."""
    blo, bhi = box_extrema(c, box)
    lo, hi = d+blo, d+bhi
    if old_entry['kind'] == 'empty':
        y = list(map(F, old_entry['dual']))
        residual = transpose_product(rows, y, len(c))
        margin = box_extrema(residual, box)[0]-dot(y, rhs)
        if margin > 0:
            return dict(kind='excluded', reason='strict_residual_farkas', margin=margin)
        return dict(kind='outer', lo=lo, hi=hi, reason='old_empty_reintroduced',
                    failed_margin=margin)
    y, z = [list(map(F, old_entry[key])) for key in ('dlo', 'dhi')]
    aty, atz = [transpose_product(rows, w, len(c)) for w in (y, z)]
    lres = [a+b for a, b in zip(c, aty)]
    ures = [a-b for a, b in zip(c, atz)]
    lo = max(lo, d-dot(y, rhs)+box_extrema(lres, box)[0])
    hi = min(hi, d+dot(z, rhs)+box_extrema(ures, box)[1])
    if lo > hi:
        return dict(kind='excluded', reason='inconsistent_sound_bounds', lo=lo, hi=hi)
    return dict(kind='outer', lo=lo, hi=hi, reason='retained_dual_residual')


def transport(old_problem, old_certificate, new_problem):
    V.verify(old_problem, old_certificate)
    if set(new_problem) != {'generators', 'receipts'}:
        raise ValueError('new problem fields')
    n, k = len(old_problem['generators']), len(old_problem['receipts'])
    if len(new_problem['generators']) != n or len(new_problem['receipts']) != k:
        raise ValueError('changed block or receipt indexing')
    tables, evidence = [], []
    for i in range(n):
        oldg, newg = old_problem['generators'][i], new_problem['generators'][i]
        if len(oldg['A']) != len(newg['A']) or len(oldg['c']) != len(newg['c']):
            raise ValueError('changed base row or coordinate indexing')
        box = implied_box(newg)
        table, row = {}, []
        for mask, entry in enumerate(old_certificate['faces'][i]):
            a, b, c, d = V.constraints(new_problem, i, mask)
            out = local_outer(a, b, c, d, box, entry)
            row.append(out)
            if out['kind'] == 'outer':
                table[mask] = (out['lo'], out['hi'])
        tables.append(table)
        evidence.append(row)
    return dict(kind='OUTER_ONLY', old_problem_sha256=V.digest(old_problem),
                new_problem_sha256=V.digest(new_problem),
                ranges=V.whole_range(tables, k), faces=evidence, new_lp_calls=0)


# None denotes +infinity. All finite costs below are nonnegative.
def maximum(a, b):
    return None if a is None or b is None else max(a, b)


def minimum(a, b):
    return b if a is None else a if b is None else min(a, b)


def deficit_time(deficit, slope):
    if slope < 0:
        raise ValueError('negative expansion slope')
    if deficit <= 0:
        return F(0)
    return None if slope == 0 else deficit/slope


def subsets(mask):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            return
        sub = (sub-1) & mask


def advance_cost(previous, table, k):
    result = {}
    for mask in range(1 << k):
        best = None
        for sub in subsets(mask):
            rest = mask ^ sub
            if sub in table and rest in previous:
                best = minimum(best, maximum(table[sub], previous[rest]))
        if best is not None:
            result[mask] = best
    return result


def band_radius(families, k, band):
    """Exact first hit of artificial expanding intervals, not actual sources.

    family[mask]=(activation or None, lower, upper, lower_slope, upper_slope).
    Every nonempty family must cover all masks explicitly, even infinite ones.
    """
    n = len(families)
    h, H = band
    if n < 1 or k < 0 or h > H:
        raise ValueError('radius contract')
    ordinary, anchors = [], []
    for family in families:
        if set(family) != set(range(1 << k)):
            raise ValueError('missing expanding slice')
        table, anchor = {}, {}
        for mask, (activation, lo, hi, p, q) in family.items():
            if lo > hi or p < 0 or q < 0 or (activation is not None and activation < 0):
                raise ValueError('expansion contract')
            up = maximum(activation, deficit_time(h-hi, q))
            down = maximum(up, deficit_time(lo-H, p))
            if up is not None:
                table[mask] = up
            if down is not None:
                anchor[mask] = down
        ordinary.append(table)
        anchors.append(anchor)
    prefix = [{0: F(0)}]
    for table in ordinary:
        prefix.append(advance_cost(prefix[-1], table, k))
    suffix = [None]*(n+1)
    suffix[n] = {0: F(0)}
    for i in range(n-1, -1, -1):
        suffix[i] = advance_cost(suffix[i+1], ordinary[i], k)
    best, witness = None, None
    full = (1 << k)-1
    for i, table in enumerate(anchors):
        for mask, anchor in table.items():
            outside = full ^ mask
            for left in subsets(outside):
                right = outside ^ left
                if left in prefix[i] and right in suffix[i+1]:
                    value = max(anchor, prefix[i][left], suffix[i+1][right])
                    if best is None or value < best:
                        best, witness = value, dict(anchor=i, mask=mask, left=left)
    return dict(first_outer_hit=best, threshold_choice=witness,
                source_witness=False, new_lp_calls=0)


def receipt_expansion_families(problem, certificate):
    """Specialization: each receipt expands [lo-t, hi+t], all else fixed."""
    V.verify(problem, certificate)
    families = []
    for i, entries in enumerate(certificate['faces']):
        g = problem['generators'][i]
        box = implied_box(g)
        base_count = len(g['A'])
        family = {}
        for mask, entry in enumerate(entries):
            if entry['kind'] == 'bounded':
                slopes = [sum(map(F, entry[key][base_count:]), F(0))
                          for key in ('dlo', 'dhi')]
                family[mask] = (F(0), F(entry['lo']), F(entry['hi']), *slopes)
            else:
                a, b, c, d = V.constraints(problem, i, mask)
                w = list(map(F, entry['dual']))
                gamma = sum(w[base_count:], F(0))
                alpha = -dot(w, b)/gamma if gamma else None
                lo, hi = box_extrema(c, box)
                family[mask] = (alpha, d+lo, d+hi, F(0), F(0))
        families.append(family)
    return families


def evaluate_families(families, k, time):
    if time < 0:
        raise ValueError('negative time')
    tables = []
    for family in families:
        table = {}
        for mask, (a, lo, hi, p, q) in family.items():
            if a is not None and a <= time:
                table[mask] = (lo-time*p, hi+time*q)
        tables.append(table)
    return V.whole_range(tables, k)
