"""s18 bounded DEVELOPMENT check; no imports of frozen executable probes."""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import platform
import random
import time

started = time.perf_counter_ns()
rng = random.Random(1819)
counts = Counter()

def binary_rank(vectors):
    pivots = {}
    for x in vectors:
        while x:
            p = x.bit_length()-1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                break
    return len(pivots)

def linear_bases(vectors):
    rank = binary_rank(vectors)
    return frozenset(frozenset(s) for s in combinations(range(len(vectors)), rank)
                     if binary_rank([vectors[i] for i in s]) == rank)

def greedy(bases, order):
    chosen = frozenset()
    for item in order:
        proposal = chosen | {item}
        counts['greedy_feasibility_queries'] += 1
        if any(proposal <= b for b in bases):
            chosen = proposal
    assert chosen in bases
    return chosen

def exchanges(a, bases, d):
    result = []
    for i in a:
        for j in range(d):
            if j not in a:
                counts['exchange_feasibility_queries'] += 1
                if a-{i}|{j} in bases:
                    result.append((i, j))
    return tuple(result)

def check_order(bases, order, utilities):
    d = len(order)
    position = {a:i for i,a in enumerate(order)}
    b = greedy(bases, order)
    for a in bases:
        left, right = tuple(sorted(b-a)), tuple(sorted(a-b))
        match = next((targets for targets in permutations(right)
                      if all(position[j] < position[i] and a-{i}|{j} in bases
                             for j,i in zip(left,targets))), None)
        assert match is not None
        counts['exchange_matchings'] += 1
    for utility in utilities:
        val = lambda a: sum(utility[i] for i in a)
        best = max(map(val, bases))
        if val(b) == best:
            continue
        for a in bases:
            if val(a) != best:
                continue
            assert any(utility[i] > utility[j] and position[j] < position[i]
                       for i,j in exchanges(a,bases,d))
            counts['strict_inverted_witnesses'] += 1

k4 = linear_bases([3,5,9,6,10,12])
assert len(k4) == 16
for order in permutations(range(6)):
    check_order(k4, order, [tuple(rng.randrange(3) for _ in range(6)) for _ in range(5)])

families = {6:[k4], 7:[]}
for d in (6,7):
    for _ in range(20):
        bases = linear_bases([rng.randrange(8) for _ in range(d)])
        families[d].append(bases)
        for _ in range(12):
            order = list(range(d))
            rng.shuffle(order)
            check_order(bases, order, [tuple(rng.randrange(3) for _ in range(d))])
    for rank in range(d+1):
        bases = frozenset(frozenset(s) for s in combinations(range(d),rank))
        families[d].append(bases)
        for _ in range(8):
            order = list(range(d))
            rng.shuffle(order)
            check_order(bases, order, [tuple(rng.randrange(3) for _ in range(d))])

def path_order(c, winning):
    d = len(c)
    p = [[c[i][j] if not winning or c[i][j] > c[j][i] else 0
          for j in range(d)] for i in range(d)]
    for k in range(d):
        for i in range(d):
            for j in range(d):
                if i != j:
                    p[i][j] = max(p[i][j], min(p[i][k], p[k][j]))
    remaining = set(range(d))
    order = []
    while remaining:
        valid = [i for i in sorted(remaining) if all(p[j][i] <= p[i][j] for j in remaining)]
        assert valid
        chosen = valid[0]
        order.append(chosen)
        remaining.remove(chosen)
    return order

streams = []
for case in range(200):
    d, ceiling, winning = 6+case%2, (case//2)%4, bool((case//8)%2)
    utility = tuple(rng.randrange(3) for _ in range(d))
    c = [[0]*d for _ in range(d)]
    bad_rounds = set(rng.sample(range(100), ceiling))
    mistakes = actual_bad = 0
    val = lambda a: sum(utility[i] for i in a)
    for t in range(100):
        bases = rng.choice(families[d])
        b = greedy(bases, path_order(c, winning))
        best = max(map(val,bases))
        mistakes += val(b) < best
        choices = list(bases) if t in bad_rounds else [a for a in bases if val(a) == best]
        # Explicit stable sorting before random selection keeps set hashing irrelevant.
        choices.sort(key=lambda a:tuple(sorted(a)))
        a = rng.choice(choices)
        actual_bad += val(a) < best
        for i,j in exchanges(a,bases,d):
            c[i][j] += 1
        counts['stream_rounds'] += 1
    bound = d*(d-1)//2*(actual_bad+1)+actual_bad
    assert mistakes <= bound
    assert all(c[i][j] <= actual_bad for i in range(d) for j in range(d) if utility[i] < utility[j])
    streams.append(dict(d=d, utility=utility, winning=winning, corruption_ceiling=ceiling,
                        actual_corruptions=actual_bad,mistakes=mistakes,bound=bound))

result = dict(status='PASS',attribution='Codex (GPT-6), DEVELOPMENT, same-model',
              python=platform.python_version(), elapsed_ns=time.perf_counter_ns()-started,
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              counts=dict(counts),streams=streams,
              limitation='Small exhaustive exchange checks and sampled streams, not independent confirmation.')
with Path(__file__).with_name('matroid_result.json').open('x',encoding='utf-8') as stream:
    json.dump(result,stream,indent=2)
print(json.dumps({k:v for k,v in result.items() if k != 'streams'}))
