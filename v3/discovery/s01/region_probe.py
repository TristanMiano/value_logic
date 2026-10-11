"""Exact rational DEVELOPMENT prototype for decision-region acquisition.

Codex (GPT-6), 2026-10-11. Small-instance vertex enumeration is intentionally
expensive and is charged by reported planning counts, not a free oracle.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time
import traceback


def linear_solve(rows, rhs):
    n = len(rhs)
    a = [[F(x) for x in row] + [F(y)] for row, y in zip(rows, rhs)]
    for col in range(n):
        pivot = next((j for j in range(col, n) if a[j][col]), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x/scale for x in a[col]]
        for j in range(n):
            if j != col:
                scale = a[j][col]
                a[j] = [x-scale*y for x, y in zip(a[j], a[col])]
    return tuple(row[-1] for row in a)


def minmax(rows):
    """min_q max_h rows[h] dot q; q is a probability vector."""
    n, m = len(rows), len(rows[0])
    constraints = [tuple(row)+(-1,) for row in rows]
    constraints += [tuple(-int(a == b) for a in range(m))+(0,) for b in range(m)]
    vertices, systems = [], 0
    for active in combinations(range(len(constraints)), m):
        systems += 1
        point = linear_solve([(1,)*m+(0,)]+[constraints[i] for i in active], [1]+[0]*m)
        if point is not None and all(sum(a*b for a, b in zip(c, point)) <= 0 for c in constraints):
            vertices.append(point)
    assert vertices
    point = min(vertices, key=lambda p: (p[-1], p))
    return point[:-1], point[-1], systems


def certify(rows):
    q, value, primal_systems = minmax(rows)
    transpose_negative = tuple(tuple(-rows[h][a] for h in range(len(rows))) for a in range(len(rows[0])))
    lam, neg_value, dual_systems = minmax(transpose_negative)
    assert value == -neg_value
    assert sum(q) == sum(lam) == 1 and min(q) >= 0 and min(lam) >= 0
    assert all(sum(q[a]*row[a] for a in range(len(q))) <= value for row in rows)
    assert all(sum(lam[h]*rows[h][a] for h in range(len(rows))) >= value for a in range(len(q)))
    return dict(action=q, regret=value, dual=lam, systems=primal_systems+dual_systems)


def plan(losses, tests, prices, epsilon=None):
    """Ordinary exact worst-case query planning; epsilon=None permits paying
    residual regret as a terminal loss instead of demanding a fixed tolerance.
    """
    regrets = tuple(tuple(F(x)-min(row) for x in row) for row in losses)
    certificate_count = [0]
    systems = [0]
    @lru_cache(None)
    def terminal(state):
        c = certify(tuple(regrets[h] for h in state))
        certificate_count[0] += 1
        systems[0] += c['systems']
        return c
    @lru_cache(None)
    def solve(state, available):
        cert = terminal(state)
        if epsilon is not None and cert['regret'] <= epsilon:
            return F(0), None
        best = (cert['regret'], None) if epsilon is None else (None, None)
        for e in available:
            cells = [tuple(h for h in state if tests[e][h] == answer) for answer in sorted({tests[e][h] for h in state})]
            if len(cells) < 2:
                continue
            rest = tuple(j for j in available if j != e)
            children = [solve(cell, rest)[0] for cell in cells]
            if any(x is None for x in children):
                continue
            cost = prices[e] + max(children)
            if best[0] is None or cost < best[0]:
                best = cost, e
        return best
    root = tuple(range(len(losses)))
    available = tuple(range(len(tests)))
    cost, first = solve(root, available)
    root_cert = terminal(root)
    paths = []
    for h in root:
        state, remaining, path = root, available, []
        while True:
            _, e = solve(state, remaining)
            if e is None:
                break
            observed = tests[e][h]
            path.append((e, observed))
            state = tuple(g for g in state if tests[e][g] == observed)
            remaining = tuple(j for j in remaining if j != e)
        c = terminal(state)
        paths.append(dict(model=h, path=path, remaining_models=state, certificate=c,
                          query_cost=sum(prices[e] for e, _ in path)))
    return dict(root_cost=cost, first_test=first, root_certificate=root_cert,
                paths=paths, planning_states=solve.cache_info().currsize,
                certificates=certificate_count[0], rational_systems=systems[0])


def main(output):
    assert not output.exists()
    start = time.monotonic_ns()
    result = dict(status='running', evidence='DEVELOPMENT', contributor='Codex (GPT-6)',
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  start_utc=datetime.now(timezone.utc).isoformat(), command=sys.argv)
    try:
        triangle = ((0, 0, 1), (1, 0, 0), (0, 1, 0))
        pairs = [certify(tuple(triangle[i] for i in pair)) for pair in combinations(range(3), 2)]
        assert all(c['regret'] == 0 for c in pairs)
        all_three = certify(triangle)
        assert all_three['regret'] == F(1, 3)
        result['triangle'] = dict(pairs=pairs, whole=all_three)
        tests = ((0, 1, 1), (0, 0, 1))
        eps_plans = {}
        for epsilon in (F(0), F(1, 4), F(1, 3)):
            p = plan(triangle, tests, (F(1, 10), F(1, 5)), epsilon)
            eps_plans[str(epsilon)] = p
            assert p['root_cost'] == (0 if epsilon >= F(1, 3) else F(1, 10))
        result['triangle_tolerances'] = eps_plans
        result['triangle_economic'] = plan(triangle, tests, (F(1, 10), F(1, 5)))
        # A genuine joint conflict with no pairwise zero-regret obstruction.
        # Contrasting query prices show why complete identification is stronger.
        result['triangle_identification_worst_cost'] = F(3, 10)
        # No free counterfactual-identification claim: identical diagnostic
        # responses with incompatible action regions cannot reach epsilon=0.
        impossible = plan(triangle, ((0, 0, 0),), (F(1, 10),), F(0))
        assert impossible['root_cost'] is None
        result['indistinguishable_obstruction'] = impossible
        # Query complementarity: XOR labels; both singleton regret reductions
        # vanish even though a two-query policy is worth paying for.
        states = tuple(product((0, 1), repeat=2))
        xor_losses = tuple((a ^ b, 1-(a ^ b)) for a, b in states)
        xor_tests = (tuple(a for a, b in states), tuple(b for a, b in states))
        singleton = []
        for e in range(2):
            for answer in (0, 1):
                rows = tuple(xor_losses[h] for h in range(4) if xor_tests[e][h] == answer)
                c = certify(rows)
                assert c['regret'] == F(1, 2)
                singleton.append(c)
        xor = plan(xor_losses, xor_tests, (F(1, 10), F(1, 10)))
        assert xor['root_cost'] == F(1, 5) and xor['root_certificate']['regret'] == F(1, 2)
        result['xor_complementarity'] = dict(singleton=singleton, plan=xor)
        # Price revisions include a no-query regime, rather than only prices
        # chosen to make paid computation attractive.
        result['xor_price_sweep'] = []
        for c in (F(0), F(1, 10), F(1, 4), F(3, 10), F(1)):
            p = plan(xor_losses, xor_tests, (c, c))
            assert p['root_cost'] == min(F(1, 2), 2*c)
            result['xor_price_sweep'].append(dict(price=c, cost=p['root_cost'], first=p['first_test']))
        result['status'] = 'complete'
    except Exception:
        result['status'] = 'failed'
        result['failure'] = traceback.format_exc()
        raise
    finally:
        result['elapsed_ns'] = time.monotonic_ns()-start
        result['end_utc'] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(result, indent=2, default=str)+'\n', encoding='utf-8')
        print(json.dumps({k: result[k] for k in ('status', 'elapsed_ns', 'source_sha256')}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
