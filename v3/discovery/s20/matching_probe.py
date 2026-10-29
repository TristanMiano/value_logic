"""Finite DEVELOPMENT screen; exact arithmetic, no V19 implementation import."""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import math
import platform
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent


def echelon(rows, width):
    a = [list(map(F, row)) for row in rows]
    at = 0
    pivots = []
    for col in range(width):
        pivot = next((r for r in range(at, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[at], a[pivot] = a[pivot], a[at]
        scale = a[at][col]
        a[at] = [x / scale for x in a[at]]
        for r in range(len(a)):
            if r != at and a[r][col]:
                scale = a[r][col]
                a[r] = [x - scale*y for x, y in zip(a[r], a[at])]
        pivots.append(col)
        at += 1
    return a, pivots


def weights(n):
    diagonal = [(i, i) for i in range(n)]
    shift = [(i, (i+1) % n) for i in range(n)] if n > 1 else []
    late = set(diagonal + shift)
    order = [(i, j) for i in range(n) for j in range(n) if (i, j) not in late]
    order += shift + diagonal
    assert len(order) == n*n and len(set(order)) == n*n
    result = [[0]*n for _ in range(n)]
    for w, (i, j) in enumerate(order, 1):
        result[i][j] = w
    return result


def residual_matching(w, row, col, threshold):
    n = len(w)
    owner = {}

    def augment(i, seen):
        for j in range(n):
            if j == col or j in seen or w[i][j] < threshold:
                continue
            seen.add(j)
            if j not in owner or augment(owner[j], seen):
                owner[j] = i
                return True
        return False

    for i in range(n):
        if i != row and not augment(i, set()):
            return None
    p = [None]*n
    p[row] = col
    for j, i in owner.items():
        p[i] = j
    assert sorted(p) == list(range(n))
    return p


def spectrum(n):
    w = weights(n)
    seen = {}
    count = 0
    for p in permutations(range(n)):
        v = min(w[i][p[i]] for i in range(n))
        seen.setdefault(v, p)
        count += 1
    assert count == math.factorial(n)
    expected = (n-1)**2+1
    assert len(seen) == expected, (n, len(seen), expected)
    oracle = {}
    for i in range(n):
        for j in range(n):
            p = residual_matching(w, i, j, w[i][j])
            if p is not None:
                assert min(w[h][p[h]] for h in range(n)) == w[i][j]
                oracle[w[i][j]] = p
    assert set(oracle) == set(seen)
    return dict(n=n, weights=w, permutations=count, values=len(seen), bound=expected,
                enumeration_witnesses=seen, matching_witnesses=oracle)


def local_vertices(n, assigned):
    eps = F(1, 100*n*n)
    rows, rhs = [], []
    for j in range(n):
        unit = [F(int(h == j)) for h in range(n)]
        rows.extend([unit, [-x for x in unit]])
        rhs.extend([F(1), F(0)])
    rows.extend([[F(1)]*n, [F(-1)]*n,
                 [-F(int(h == assigned)) for h in range(n)]])
    rhs.extend([1+eps, -(1-eps), -(1-eps)])
    vertices = set()
    for ids in combinations(range(len(rows)), n):
        matrix, pivots = echelon([rows[i]+[rhs[i]] for i in ids], n)
        if len(pivots) != n:
            continue
        point = tuple(matrix[h][-1] for h in range(n))
        if all(sum(a*x for a, x in zip(row, point)) <= b
               for row, b in zip(rows, rhs)):
            vertices.add(point)
    assert vertices
    return vertices


def merge(intervals):
    answer = []
    for lo, hi in sorted(intervals):
        assert lo <= hi
        if not answer or lo > answer[-1][1]:
            answer.append([lo, hi])
        else:
            answer[-1][1] = max(answer[-1][1], hi)
    return answer


def noisy(n):
    w = weights(n)
    eps = F(1, 100*n*n)
    local = {}
    vertices_by_column = [local_vertices(n, j) for j in range(n)]
    for i in range(n):
        for j in range(n):
            vertices = vertices_by_column[j]
            values = [sum(a*x for a, x in zip(w[i], p)) for p in vertices]
            lo, hi = min(values), max(values)
            assert lo == w[i][j]*(1-eps)
            if n == 1:
                predicted_hi = F(w[i][j])
            else:
                other = max(w[i][h] for h in range(n) if h != j)
                predicted_hi = (w[i][j]*(1-eps)+2*eps*other
                                if other > w[i][j] else w[i][j]+eps*other)
            assert hi == predicted_hi, (n, i, j, hi, predicted_hi)
            assert lo < hi and lo <= w[i][j] <= hi
            assert w[i][j]-F(3, 100) <= lo <= hi <= w[i][j]+F(3, 100)
            local[i, j] = (lo, hi)
    branches = []
    for p in permutations(range(n)):
        intervals = [local[i, p[i]] for i in range(n)]
        branch = (min(x[0] for x in intervals), min(x[1] for x in intervals))
        minimum_edge = min(range(n), key=lambda i: w[i][p[i]])
        assert branch == local[minimum_edge, p[minimum_edge]]
        branches.append(branch)
    output = merge(branches)
    assert len(output) == (n-1)**2+1
    assert all(lo < hi for lo, hi in output)
    return dict(n=n, epsilon=str(eps), local=[dict(row=i, col=j,
                vertices=len(vertices_by_column[j]), interval=list(map(str, interval)))
                for (i, j), interval in sorted(local.items())],
                output=[list(map(str, interval)) for interval in output])


def partition_dimension(n, k):
    vectors = []
    for assignment in product(range(n), repeat=k):
        masks = [0]*n
        for j, i in enumerate(assignment):
            masks[i] |= 1 << j
        row = [0]*(n*(1 << k))
        for i, mask in enumerate(masks):
            row[i*(1 << k)+mask] = 1
        vectors.append(row)
    differences = [[x-y for x, y in zip(row, vectors[0])] for row in vectors[1:]]
    _, pivots = echelon(differences, n*(1 << k))
    expected = 0 if n == 1 else (1 << k)-1 if n == 2 else n*(1 << k)-n-k
    assert len(pivots) == expected, (n, k, len(pivots), expected)
    return dict(n=n, k=k, vertices=len(vectors), dimension=len(pivots), expected=expected)


def main():
    output = HERE / 'matching_result.json'
    failure = HERE / 'matching_failure.json'
    if output.exists() or failure.exists():
        raise RuntimeError('Refusing to replace exposed matching output')
    freeze = json.loads((HERE / 'matching_freeze.json').read_text(encoding='utf-8'))
    for name, digest in freeze['sha256'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, name
    began = time.monotonic_ns()
    result = dict(status='IN_PROGRESS', spectrum=[], noisy=[], dimensions=[])
    try:
        for key, cases, function in [('spectrum', [(n,) for n in range(1, 9)], spectrum),
                                      ('noisy', [(n,) for n in range(1, 5)], noisy),
                                      ('dimensions', list(product(range(1, 5), range(5))),
                                       partition_dimension)]:
            for args in cases:
                if time.monotonic_ns()-began > 120_000_000_000:
                    raise TimeoutError('Prospective run cap exceeded')
                result[key].append(function(*args))
        result.update(status='PASS', scope='finite development; not independent confirmation',
                      runtime_ns=time.monotonic_ns()-began, freeze=freeze,
                      python=sys.version, platform=platform.platform())
        output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(json.dumps(dict(status='PASS', spectrum_cases=len(result['spectrum']),
              enumerated_permutations=sum(r['permutations'] for r in result['spectrum']),
              noisy_cases=len(result['noisy']), dimension_cases=len(result['dimensions']),
              runtime_ns=result['runtime_ns'])))
    except BaseException:
        result.update(status='FAIL', traceback=traceback.format_exc())
        failure.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        raise


if __name__ == '__main__':
    main()
