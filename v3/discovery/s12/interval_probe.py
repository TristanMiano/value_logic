"""DEVELOPMENT interval-projection and anchored temporal-update check."""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random
import sys
import time

HERE = Path(__file__).resolve().parent


def closure(matrix):
    d = [row[:] for row in matrix]
    for k in range(len(d)):
        for i in range(len(d)):
            for j in range(len(d)):
                d[i][j] = min(d[i][j], d[i][k]+d[k][j])
    return d


def proj(worlds, scope):
    return {tuple(x[i] for i in scope) for x in worlds}


def main():
    begin = time.perf_counter_ns()
    rng = random.Random(121936)
    counts = dict(sources=0, interval_panels=0, conflicts=0, projections=0,
                  tight_difference_bounds=0, sequential_updates=0,
                  sequential_difference_queries=0)
    for n in range(2, 6):
        for _ in range(12):
            witness = tuple(rng.randrange(4) for _ in range(n))+(0,)
            a = [[0 if i == j else 1000 for j in range(n+1)] for i in range(n+1)]
            for i in range(n):
                a[n][i], a[i][n] = 3, 0
            for i in range(n):
                for j in range(n):
                    if i != j and rng.random() < .4:
                        a[i][j] = witness[j]-witness[i]+rng.randrange(3)
            worlds = {x+(0,) for x in product(range(4), repeat=n)
                      if all((x+(0,))[j]-(x+(0,))[i] <= a[i][j]
                             for i in range(n+1) for j in range(n+1))}
            assert worlds
            d = closure(a)
            for i in range(n+1):
                for j in range(n+1):
                    assert d[i][j] == max(x[j]-x[i] for x in worlds)
            scopes = [s for k in range(1, min(3, n)+1) for s in combinations(range(n), k)]
            initial = {s: proj(worlds, s) for s in scopes}
            for _ in range(24):
                limits = [sorted((rng.randrange(4), rng.randrange(4))) for _ in range(n)]+[[0, 0]]
                posterior = {x for x in worlds if all(l <= x[i] <= u for i, (l, u) in enumerate(limits))}
                upper = [min(limits[k][1]+d[k][i] for k in range(n+1)) for i in range(n+1)]
                lower = [max(limits[k][0]-d[i][k] for k in range(n+1)) for i in range(n+1)]
                assert bool(posterior) == all(l <= u for l, u in zip(lower, upper))
                counts['interval_panels'] += 1
                if not posterior:
                    counts['conflicts'] += 1
                    continue
                domains = [proj(posterior, (i,)) for i in range(n)]
                for scope in scopes:
                    filtered = {v for v in initial[scope]
                                if all((b,) in domains[i] for i, b in zip(scope, v))}
                    assert filtered == proj(posterior, scope)
                    counts['projections'] += 1
                modified = [row[:] for row in a]
                for i, (l, u) in enumerate(limits):
                    modified[n][i] = min(modified[n][i], u)
                    modified[i][n] = min(modified[i][n], -l)
                fresh = closure(modified)
                for i in range(n+1):
                    for j in range(n+1):
                        predicted = min(d[i][j], upper[j]-lower[i])
                        assert predicted == fresh[i][j] == max(x[j]-x[i] for x in posterior)
                        counts['tight_difference_bounds'] += 1
            upper, lower = d[n][:], [-d[i][n] for i in range(n+1)]
            modified = [row[:] for row in a]
            for _ in range(20):
                k = rng.randrange(n)
                if rng.randrange(2):
                    u = rng.randrange(witness[k], 4)
                    upper = [min(upper[i], u+d[k][i]) for i in range(n+1)]
                    modified[n][k] = min(modified[n][k], u)
                else:
                    l = rng.randrange(witness[k]+1)
                    lower = [max(lower[i], l-d[i][k]) for i in range(n+1)]
                    modified[k][n] = min(modified[k][n], -l)
                fresh = closure(modified)
                assert all(l <= u for l, u in zip(lower, upper))
                for i in range(n+1):
                    for j in range(n+1):
                        assert min(d[i][j], upper[j]-lower[i]) == fresh[i][j]
                        counts['sequential_difference_queries'] += 1
                counts['sequential_updates'] += 1
            counts['sources'] += 1
    # Nonconvex observation defeats the general interval cache rule.
    f = {(x, z, y) for x, z, y in product(range(3), repeat=3) if x <= z <= y}
    g = {w for w in f if w[1] in (0, 2)}
    assert (1, 1) in proj(f, (0, 2)) and (1, 1) not in proj(g, (0, 2))
    assert (1,) in proj(g, (0,)) and (1,) in proj(g, (2,))
    result = dict(status='PASS', scope='DEVELOPMENT', contributor='Codex (GPT-6)',
                  python=sys.version, counts=counts, nonconvex_counterexample=True,
                  elapsed_ns=time.perf_counter_ns()-begin,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  limitation='Finite difference-constraint sources; not every median-closed '
                             'relation, independent confirmation, or runtime superiority.')
    (HERE/'interval_probe.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
