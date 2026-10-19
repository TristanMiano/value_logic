"""DEVELOPMENT: cut/min-marginal adapter versus direct finite worlds."""
from collections import deque
from itertools import combinations
from pathlib import Path
import hashlib
import json
import random
import sys
import time

HERE = Path(__file__).resolve().parent


def flow(capacity, source, sink):
    r = [row[:] for row in capacity]
    value = 0
    while True:
        previous = {source: None}
        queue = deque([source])
        while queue and sink not in previous:
            u = queue.popleft()
            for v, c in enumerate(r[u]):
                if c > 0 and v not in previous:
                    previous[v] = u
                    queue.append(v)
        if sink not in previous:
            return value, r
        v = sink
        amount = sum(map(sum, capacity))+1
        while previous[v] is not None:
            u = previous[v]
            amount = min(amount, r[u][v])
            v = u
        v = sink
        while previous[v] is not None:
            u = previous[v]
            r[u][v] -= amount
            r[v][u] += amount
            v = u
        value += amount


def energy(x, arcs, units):
    return (sum(c for u, v, c in arcs if x >> u & 1 and not x >> v & 1)
            + sum(c for u, b, c in units if (x >> u & 1) != b))


def capacity(n, arcs, units, hard):
    c = [[0]*(n+2) for _ in range(n+2)]
    for u, v, fee in arcs:
        c[u][v] += fee
    for u, b, fee in units:
        c[n if b else u][u if b else n+1] += fee
    big = 1+sum(fee for _, _, fee in arcs+units)
    for u, b in hard.items():
        c[n if b else u][u if b else n+1] += big
    return c


def matches(x, h):
    return all((x >> u & 1) == b for u, b in h.items())


def project(x, scope):
    return sum(((x >> u) & 1) << j for j, u in enumerate(scope))


def main():
    begin = time.perf_counter_ns()
    rng = random.Random(121931)
    counts = dict(fixtures=0, residual_identity=0, optimum_sources=0,
                  min_marginals=0, mask_margins=0, threshold_permissions=0,
                  maximum_tolerance=0)
    examples = []
    for n in range(2, 7):
        for repetition in range(12):
            arcs = [(u, v, rng.randrange(1, 8)) for u in range(n)
                    for v in range(n) if u != v and rng.random() < .25]
            units = [(u, rng.randrange(2), rng.randrange(1, 8))
                     for u in range(n) if rng.random() < .8]
            hard = {u: rng.randrange(2) for u in range(n) if rng.random() < .2}
            worlds = [x for x in range(1 << n) if matches(x, hard)]
            energies = {x: energy(x, arcs, units) for x in worlds}
            e0, residual = flow(capacity(n, arcs, units, hard), n, n+1)
            assert e0 == min(energies.values())
            optimum = {x for x in worlds if energies[x] == e0}
            represented = set()
            for x in range(1 << n):
                side = [x >> u & 1 for u in range(n)]+[1, 0]
                cost = sum(residual[u][v] for u in range(n+2)
                           for v in range(n+2) if side[u] and not side[v])
                if cost == 0:
                    represented.add(x)
                if x in energies:
                    assert cost == energies[x]-e0
                    counts['residual_identity'] += 1
            assert represented == optimum
            counts['optimum_sources'] += 1
            scopes = [(u,) for u in range(n)]+list(combinations(range(n), 2))
            tables = {}
            for scope in scopes:
                table = []
                for pattern in range(1 << len(scope)):
                    added = {u: pattern >> j & 1 for j, u in enumerate(scope)}
                    valid = all(u not in hard or hard[u] == b for u, b in added.items())
                    measured = (flow(capacity(n, arcs, units, hard | added), n, n+1)[0]-e0
                                if valid else float('inf'))
                    direct = min((e-e0 for x, e in energies.items()
                                  if project(x, scope) == pattern), default=float('inf'))
                    assert measured == direct
                    table.append(measured)
                    counts['min_marginals'] += 1
                tables[scope] = table
            target = [(rng.choice(scopes), rng.randrange(4)) for _ in range(5)]
            target = [(scope, a % (1 << len(scope))) for scope, a in target]
            # Legal masks have one or two explicitly forbidden local patterns.
            legal_constraints = [(rng.choice(scopes), rng.randrange(4)) for _ in range(2)]
            legal_constraints = [(scope, a % (1 << len(scope)))
                                 for scope, a in legal_constraints]
            legal = [d for d in range(1 << n)
                     if all(project(d, scope) != a for scope, a in legal_constraints)]
            margins = {}
            for d in legal:
                margin = min(tables[scope][project(d, scope) ^ a] for scope, a in target)
                direct = min((e-e0 for x, e in energies.items()
                              if any(project(x ^ d, scope) == a for scope, a in target)),
                             default=float('inf'))
                assert margin == direct
                margins[d] = margin
                counts['mask_margins'] += 1
            thresholds = sorted({0} | {e-e0 for e in energies.values()})
            for rho in thresholds:
                compiled = {d for d in legal if all(
                    project(d, scope) != (v ^ a)
                    for scope, a in target for v, mu in enumerate(tables[scope]) if mu <= rho)}
                direct = {d for d in legal if all(
                    all(project(x ^ d, scope) != a for scope, a in target)
                    for x, e in energies.items() if e-e0 <= rho)}
                assert compiled == direct == {d for d in legal if margins[d] > rho}
                counts['threshold_permissions'] += len(legal)
            if margins:
                best = max(margins.values())
                assert all(any(m > rho for m in margins.values()) == (rho < best)
                           for rho in thresholds)
                counts['maximum_tolerance'] += 1
            counts['fixtures'] += 1
    # The three-unit source explicitly defeats forced-coordinate pruning.
    near = [x for x in range(8) if x.bit_count() <= 2]
    posterior = [x for x in near if x & 1]
    assert {project(x, (1, 2)) for x in near} == {0, 1, 2, 3}
    assert {project(x, (1, 2)) for x in posterior} == {0, 1, 2}
    assert all({x >> u & 1 for x in posterior} == {0, 1} for u in (1, 2))
    result = dict(status='PASS', scope='DEVELOPMENT', contributor='Codex (GPT-6)',
                  python=sys.version, counts=counts, positive_slack_counterexample=True,
                  elapsed_ns=time.perf_counter_ns()-begin,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  limitation='Finite synthetic cases; no independent confirmation, '
                             '2-SAT implementation benchmark or application-cost claim.')
    (HERE/'repair_margin_probe.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
