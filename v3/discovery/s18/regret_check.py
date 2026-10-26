"""Frozen finite screen of a first-positive normal form for minimax regret."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import random
import time

started = time.perf_counter_ns()
stats = dict(cases=0, adaptive_states=0, restricted_states=0)
full = 15


def check(family, costs, losses):
    worlds = tuple(f for f in range(1, 16) if all(f & e for e in family))
    minima = {f: min(losses[j] for j in range(4) if f >> j & 1) for f in worlds}

    def stop(current):
        common = full
        for f in current:
            common &= f
        options = [(max(losses[j]-minima[f] for f in current), ('return', j))
                   for j in range(4) if common >> j & 1]
        return min(options) if options else (10**9, ('impossible',))

    @lru_cache(None)
    def adaptive(current):
        stats['adaptive_states'] += 1
        best = stop(current)
        for j in range(4):
            yes = tuple(f for f in current if f >> j & 1)
            no = tuple(f for f in current if not(f >> j & 1))
            if yes and no:
                y, n = adaptive(yes), adaptive(no)
                option = (costs[j]+max(y[0], n[0]), ('query', j, y[1], n[1]))
                if option[0] < best[0]:
                    best = option
        return best

    @lru_cache(None)
    def restricted(current):
        stats['restricted_states'] += 1
        best = stop(current)
        for j in range(4):
            yes = tuple(f for f in current if f >> j & 1)
            no = tuple(f for f in current if not(f >> j & 1))
            if yes and no:
                y, n = stop(yes), restricted(no)
                option = (costs[j]+max(y[0], n[0]), ('query', j, y[1], n[1]))
                if option[0] < best[0]:
                    best = option
        return best

    def bill(policy, f):
        paid = 0
        while policy[0] == 'query':
            j = policy[1]
            paid += costs[j]
            policy = policy[2] if f >> j & 1 else policy[3]
        assert policy[0] == 'return' and f >> policy[1] & 1
        regret = losses[policy[1]]-minima[f]
        return dict(world=f, fees=paid, regret=regret, total=paid+regret,
                    action=policy[1])

    a, r = adaptive(worlds), restricted(worlds)
    assert a[0] <= r[0]
    stats['cases'] += 1
    if a[0] < r[0]:
        ab = [bill(a[1], f) for f in worlds]
        rb = [bill(r[1], f) for f in worlds]
        assert max(x['total'] for x in ab) == a[0]
        assert max(x['total'] for x in rb) == r[0]
        return dict(family=family, costs=costs, losses=losses,
                    adaptive=a, restricted=r, adaptive_bills=ab, restricted_bills=rb)
    return None


edges = tuple(range(1, 16))
families = []
for bits in range(1, 1 << len(edges)):
    f = tuple(edges[j] for j in range(len(edges)) if bits >> j & 1)
    if all((a & b) not in (a, b) for a, b in combinations(f, 2)):
        families.append(f)
assert len(families) == 166
profiles = [((1, 1, 1, 1), (0, 2, 5, 9)),
            ((1, 2, 3, 5), (7, 0, 2, 1)),
            ((10, 9, 9, 1), (100, 0, 0, 4)),
            ((5, 100, 1, 7), (0, 5, 10, 3)),
            ((8, 1, 3, 2), (0, 11, 3, 8))]
rng = random.Random(20261025)
profiles += [(tuple(rng.randrange(1, 11) for _ in range(4)),
              tuple(rng.randrange(21) for _ in range(4))) for _ in range(32)]
counterexample = None
for costs, losses in profiles:
    for family in families:
        counterexample = check(family, costs, losses)
        if counterexample is not None:
            break
    if counterexample is not None:
        break
source = Path(__file__)
result = dict(status='COUNTEREXAMPLE' if counterexample else 'NO_GAP_IN_PANEL',
              contributor='Codex (GPT-6)', python=platform.python_version(),
              source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              elapsed_ns=time.perf_counter_ns()-started, counts=stats,
              counterexample=counterexample)
source.with_name('regret_result.json').write_text(json.dumps(result, indent=2)+'\n',
                                               encoding='utf-8')
print(json.dumps(result))
