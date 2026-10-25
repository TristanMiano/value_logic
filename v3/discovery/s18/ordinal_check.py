"""Bounded s18 DEVELOPMENT screen; standard algorithms, no benchmark claim."""
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import platform
import random
import time

started = time.perf_counter_ns()
counts = Counter()
rng = random.Random(1818)

def paths(matrix, winning=False):
    n = len(matrix)
    p = [[matrix[a][b] if not winning or matrix[a][b] > matrix[b][a]
          else 0 for b in range(n)] for a in range(n)]
    for k in range(n):
        for a in range(n):
            for b in range(n):
                if a != b and a != k and b != k:
                    p[a][b] = max(p[a][b], min(p[a][k], p[k][b]))
                    counts['floyd_updates'] += 1
    return p

def ranking(p):
    n = len(p)
    for a, b, c in permutations(range(n), 3):
        assert not (p[a][b] > p[b][a] and p[b][c] > p[c][b]) or p[a][c] > p[c][a]
    pending = set(range(n))
    order = []
    while pending:
        top = [a for a in sorted(pending)
               if not any(p[b][a] > p[a][b] for b in pending)]
        assert top
        order.append(top[0])
        pending.remove(top[0])
    return order

for d in range(2, 6):
    for case in range(20):
        matrix = [[rng.randrange(5) if a != b else 0 for b in range(d)] for a in range(d)]
        for winning in (False, True):
            p = paths(matrix, winning)
            w = [[matrix[a][b] if not winning or matrix[a][b] > matrix[b][a]
                  else 0 for b in range(d)] for a in range(d)]
            for a, b in permutations(range(d), 2):
                middle = [i for i in range(d) if i not in (a, b)]
                exact = 0
                for k in range(len(middle) + 1):
                    for mid in permutations(middle, k):
                        seq = (a,) + mid + (b,)
                        exact = max(exact, min(w[x][y] for x, y in zip(seq, seq[1:])))
                        counts['enumerated_simple_paths'] += 1
                assert p[a][b] == exact
            ranking(p)
            counts['path_matrix_cases'] += 1

adversary_cases = []
for utility in ((0, 1), (0, 0), (0, 1, 2), (0, 0, 1), (0, 1, 1), (0, 0, 0)):
    d = len(utility)
    subsets = [s for k in range(1, d + 1) for s in combinations(range(d), k)]
    for budget, winning, improve, all_pairs in product(range(3), (False, True), (False, True), (False, True)):
        if improve and all_pairs:
            continue
        @lru_cache(None)
        def choose(state):
            counts['rankings'] += 1
            matrix = [list(state[a*d:(a+1)*d]) for a in range(d)]
            return tuple(ranking(paths(matrix, winning)))
        @lru_cache(None)
        def worst(state, steps, left):
            counts['adversary_states'] += 1
            if steps == 0:
                return 0
            order = choose(state)
            best = 0
            for subset in subsets:
                j = next(a for a in order if a in subset)
                optimum = max(utility[a] for a in subset)
                mistake = utility[j] < optimum
                for i in subset:
                    good = (utility[i] >= utility[j] and (not mistake or utility[i] > utility[j])) if improve else utility[i] == optimum
                    bad = int(not good)
                    if bad > left:
                        continue
                    nxt = list(state)
                    targets = subset if all_pairs else (j,)
                    for other in targets:
                        if i != other:
                            nxt[i*d+other] += 1
                    counts['adversary_transitions'] += 1
                    best = max(best, int(mistake) + worst(tuple(nxt), steps-1, left-bad))
            return best
        horizon = 9
        maximum = worst((0,)*(d*d), horizon, budget)
        bound = d*(d-1)//2*(budget+1)+budget
        assert maximum <= bound
        adversary_cases.append(dict(utility=utility, budget=budget, winning=winning,
                                    improve=improve, all_pairs=all_pairs, horizon=horizon,
                                    worst=maximum, bound=bound))

def flow(cap, a, b):
    n = len(cap)
    residual = [row[:] for row in cap]
    result = 0
    while True:
        prev = {a: None}
        queue = deque([a])
        while queue and b not in prev:
            x = queue.popleft()
            for y in range(n):
                counts['flow_arc_scans'] += 1
                if y not in prev and residual[x][y]:
                    prev[y] = x
                    queue.append(y)
        if b not in prev:
            return result
        v, amount = b, 10**9
        while prev[v] is not None:
            amount = min(amount, residual[prev[v]][v])
            v = prev[v]
        v = b
        while prev[v] is not None:
            u = prev[v]
            residual[u][v] -= amount
            residual[v][u] += amount
            v = u
        result += amount
        counts['flow_augmentations'] += 1

def report_flow(d, reports, a, b):
    m = len(reports)
    cap = [[0]*(d+m) for _ in range(d+m)]
    for t, (winner, subset) in enumerate(reports):
        cap[winner][d+t] = 1
        for j in subset:
            if j != winner:
                cap[d+t][j] = m+1
    return flow(cap, a, b)

def violated(utility, reports):
    return sum(any(utility[j] > utility[i] for j in subset) for i, subset in reports)

for d in range(2, 6):
    for case in range(35):
        reports = []
        for _ in range(rng.randrange(9)):
            subset = tuple(i for i in range(d) if rng.randrange(2))
            if not subset:
                subset = (rng.randrange(d),)
            reports.append((rng.choice(subset), subset))
        for a, b in permutations(range(d), 2):
            binary = min(violated(u, reports) for u in product(range(2), repeat=d) if u[a] == 0 and u[b] == 1)
            got = report_flow(d, reports, a, b)
            assert got == binary
            counts['cut_queries'] += 1
            if d <= 3:
                real = min(violated(u, reports) for u in product(range(d), repeat=d) if u[a] < u[b])
                assert real == got
                counts['ordered_level_queries'] += 1
        counts['report_graph_cases'] += 1

disjoint = [(0, (0, 1)), (1, (1, 3)), (0, (0, 2)), (2, (2, 3))]
assert report_flow(4, disjoint, 0, 3) == 2
shared = [(0, (0, 1, 2)), (1, (1, 3)), (2, (2, 3))]
assert report_flow(4, shared, 0, 3) == 1
cycle = [[0]*4 for _ in range(4)]
complete = [[2*int(a != b) for b in range(4)] for a in range(4)]
for a, b in ((0, 1), (1, 2), (2, 3), (3, 0)):
    cycle[a][b] = cycle[b][a] = 3
for a, b in permutations(range(4), 2):
    assert flow(cycle, a, b) == flow(complete, a, b) == 6
for a, b in ((0, 1), (2, 3)):
    for graph in (cycle, complete):
        graph[a][b] += 10
        graph[b][a] += 10
assert flow(cycle, 0, 2) == 6 and flow(complete, 0, 2) == 8

# Every covering family on a three-element universe, using nonempty sets.
sets = list(range(1, 8))
for mask in range(1, 128):
    family = [s for index, s in enumerate(sets) if mask >> index & 1]
    if any(not any(s >> e & 1 for s in family) for e in range(3)):
        continue
    cover = min(sum(bits) for bits in product(range(2), repeat=len(family))
                if all(any(bit and s >> e & 1 for bit, s in zip(bits, family)) for e in range(3)))
    edges, next_vertex = [], 2
    for e in range(3):
        labels = [j for j, s in enumerate(family) if s >> e & 1]
        route = [0] + list(range(next_vertex, next_vertex+len(labels)-1)) + [1]
        next_vertex += len(labels)-1
        edges.extend((a, b, label) for a, b, label in zip(route, route[1:], labels))
    label_cut = min(len({label for a, b, label in edges if u[a] == 0 and u[b] == 1})
                    for middle in product(range(2), repeat=next_vertex-2)
                    for u in [(0, 1)+middle])
    assert label_cut == cover
    counts['label_cut_reductions'] += 1

result = dict(status='PASS', attribution='Codex (GPT-6), DEVELOPMENT, same-model',
              python=platform.python_version(), elapsed_ns=time.perf_counter_ns()-started,
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              counts=dict(counts), adversary_cases=adversary_cases,
              fixtures=dict(independent_paths=2, shared_report_paths=1,
                            old_pair_cuts=6, updated_pair_cuts=[6, 8]),
              limitation='Bounded construction screen, not independent confirmation or a speed benchmark.')
out = Path(__file__).with_name('ordinal_result.json')
with out.open('x', encoding='utf-8') as stream:
    json.dump(result, stream, indent=2)
print(json.dumps({key:value for key,value in result.items() if key != 'adversary_cases'}))
