"""Frozen finite same-model comparison against unrestricted adaptive minimax."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import time

started = time.perf_counter_ns()
stats = dict(cases=0, dp_states=0, final_member_choices=0)


def schedule(edge, costs, losses):
    order = sorted((j for j in range(len(costs)) if edge >> j & 1),
                   key=lambda j: (-losses[j], j))
    prefix_cost = []
    total = 0
    for j in order:
        total += costs[j]
        prefix_cost.append(total)
    values = [t+losses[j] for t, j in zip(prefix_cost, order)]
    prefix_max = [-float('inf')]
    for v in values:
        prefix_max.append(max(prefix_max[-1], v))
    suffix_max = [-float('inf')]*(len(order)+1)
    for r in reversed(range(len(order))):
        suffix_max[r] = max(suffix_max[r+1], values[r])
    best = float('inf')
    for r, final in enumerate(order):
        stats['final_member_choices'] += 1
        fast = max(prefix_max[r], suffix_max[r+1]-costs[final],
                   total-costs[final]+losses[final])
        paid = 0
        direct = -float('inf')
        for j in order:
            if j == final:
                continue
            paid += costs[j]
            direct = max(direct, paid+losses[j])
        direct = max(direct, paid+losses[final])
        assert fast == direct
        best = min(best, fast)
    return best


def check(family, costs, losses, retained=0):
    n = len(costs)
    full = (1 << n)-1
    worlds = tuple(f for f in range(1, full+1)
                   if f & retained == retained and all(f & e for e in family))
    assert worlds

    @lru_cache(None)
    def value(current):
        stats['dp_states'] += 1
        common = full
        for f in current:
            common &= f
        choices = [losses[j] for j in range(n) if common >> j & 1]
        for j in range(n):
            yes = tuple(f for f in current if f >> j & 1)
            no = tuple(f for f in current if not(f >> j & 1))
            if yes and no:
                choices.append(costs[j]+max(value(yes), value(no)))
        assert choices
        return min(choices)

    options = [schedule(e, costs, losses) for e in family]
    options += [losses[j] for j in range(n) if retained >> j & 1]
    formula = min(options)
    adaptive = value(worlds)
    assert formula == adaptive, (family, costs, losses, retained, formula, adaptive)
    stats['cases'] += 1
    return adaptive


edges = tuple(range(1, 16))
families = []
for bits in range(1, 1 << len(edges)):
    family = tuple(edges[j] for j in range(len(edges)) if bits >> j & 1)
    if all((a & b) not in (a, b) for a, b in combinations(family, 2)):
        families.append(family)
assert len(families) == 166
profiles = [((1, 1, 1, 1), (0, 2, 5, 9)),
            ((1, 2, 3, 5), (7, 0, 2, 1)),
            ((10, 9, 9, 1), (100, 0, 0, 4))]
for family in families:
    for costs, losses in profiles:
        check(family, costs, losses)

example = check((7,), (10, 9, 9), (100, 0, 0))
assert example == 110
factor_cases = []
for k in range(1, 7):
    n = k+1
    total = check(((1 << n)-1,), (1,)*n, (k-1,)+(0,)*k)
    assert total == k
    factor_cases.append(dict(k=k, exact_total=total, uncoupled_bound=2*k-1))
retained_cases = [check((15,), *profiles[0], retained=1),
                  check((3, 12), *profiles[1], retained=5)]

source = Path(__file__)
result = dict(status='PASS', contributor='Codex (GPT-6)', python=platform.python_version(),
              source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              elapsed_ns=time.perf_counter_ns()-started,
              scope='Finite deterministic oracle comparison; no measured economic claim',
              antichains=166, profiles=profiles, counts=stats,
              example=dict(exact_total=example, uncoupled_bound=118),
              factor_cases=factor_cases, retained_values=retained_cases)
source.with_name('total_search_result.json').write_text(
    json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result))
