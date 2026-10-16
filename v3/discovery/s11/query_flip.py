"""DEVELOPMENT paid queries and counterfactual flips from conditional values.

Codex (GPT-6). Exact fractions. The compact source gives cell masses and
unnormalized conditional first moments; it does not specify unqueried dependence.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import random
import time


def signs(n):
    return list(product((-1, 1), repeat=n))


def source(m, r, seed):
    rng = random.Random(seed)
    cells = signs(r)
    raw = [rng.randrange(1, 8) for _ in cells]
    mass = [F(x, sum(raw)) for x in raw]
    thresholds = [[rng.randrange(9) for _ in range(m-r)] for _ in cells]
    moments = [[p * F(2*t-8, 8) for t in row] for p, row in zip(mass, thresholds)]
    return dict(m=m, r=r, cells=cells, mass=mass, moments=moments, thresholds=thresholds)


def full_law(src, dependence):
    """Two exact couplings having the same compact source; tiny m only."""
    m, r = src['m'], src['r']
    assert m <= 6
    law = {}
    for z, p, row in zip(src['cells'], src['mass'], src['thresholds']):
        if dependence == 'common_uniform':
            for u in range(1, 9):
                x = z + tuple(1 if u <= t else -1 for t in row)
                law[x] = law.get(x, F(0)) + p/8
        elif dependence == 'conditional_independent':
            for y in signs(m-r):
                probability = p
                for t, yi in zip(row, y):
                    probability *= F(t if yi == 1 else 8-t, 8)
                if probability:
                    law[z+y] = probability
        else:
            raise ValueError(dependence)
    assert sum(law.values()) == 1
    return law


def matches(z, h):
    return all(o == 0 or z[i] == o for i, o in enumerate(h))


def compact_plan(src, weights, flip_fee, query_fee, H):
    m, r = src['m'], src['r']
    counters = dict(contexts=0, source_rows_read=0, moment_terms_added=0,
                    stop_options=0, query_options=0, flip_keys_sorted=0)

    @lru_cache(None)
    def values(h):
        counters['contexts'] += 1
        mass = F(0)
        moments = [F(0)]*m
        for z, p, row in zip(src['cells'], src['mass'], src['moments']):
            counters['source_rows_read'] += 1
            if matches(z, h):
                mass += p
                for i in range(r):
                    moments[i] += z[i]*p
                for i in range(r, m):
                    moments[i] += row[i-r]
                counters['moment_terms_added'] += m
        return mass, tuple(moments)

    @lru_cache(None)
    def solve(h, budget):
        mass, moment = values(h)
        if mass == 0:
            return F(0), ('null',)
        counters['stop_options'] += 1
        gains = sorted(((2*weights[i]*moment[i]-flip_fee[i]*mass, i) for i in range(m)), reverse=True)
        counters['flip_keys_sorted'] += m
        chosen = tuple(i for gain, i in gains[:budget] if gain > 0)
        stopping = sum((weights[i]*moment[i] for i in range(m)), F(0)) - sum((2*weights[i]*moment[i]-flip_fee[i]*mass for i in chosen), F(0))
        best, action = (stopping, ('terminal_1', chosen)) if stopping < 0 else (F(0), ('terminal_0',))
        if budget:
            for j in range(r):
                if h[j]:
                    continue
                counters['query_options'] += 1
                total = query_fee[j]*mass
                for o in (-1, 1):
                    child = list(h)
                    child[j] = o
                    total += solve(tuple(child), budget-1)[0]
                if total < best:
                    best, action = total, ('query', j)
        return best, action

    root = (0,)*r
    value, action = solve(root, H)
    plan = {}

    def trace(h, budget):
        key = ''.join({-1:'-', 0:'?', 1:'+'}[x] for x in h) + ':' + str(budget)
        value, decision = solve(h, budget)
        plan[key] = {'value': str(value), 'action': decision}
        if decision[0] == 'query':
            for o in (-1, 1):
                child = list(h)
                child[decision[1]] = o
                trace(tuple(child), budget-1)
    trace(root, H)
    return value, action, plan, counters, solve


def unrestricted_plan(law, weights, flip_fee, query_fee, H):
    m, r = len(weights), len(query_fee)
    counter = {'states': 0, 'world_visits': 0, 'flip_options': 0, 'query_options': 0}

    @lru_cache(None)
    def moment(h):
        mass = F(0)
        means = [F(0)]*m
        for x, p in law.items():
            counter['world_visits'] += 1
            if matches(x, h):
                mass += p
                for i in range(m):
                    means[i] += p*x[i]
        return mass, tuple(means)

    @lru_cache(None)
    def solve(h, mask, budget):
        counter['states'] += 1
        mass, means = moment(h)
        if not mass:
            return F(0)
        best = min(F(0), sum((weights[i]*means[i]*(-1 if mask & (1<<i) else 1) for i in range(m)), F(0)))
        if budget:
            for i in range(m):
                counter['flip_options'] += 1
                best = min(best, flip_fee[i]*mass + solve(h, mask ^ (1<<i), budget-1))
            for j in range(r):
                if h[j]:
                    continue
                counter['query_options'] += 1
                total = query_fee[j]*mass
                for o in (-1, 1):
                    child = list(h)
                    child[j] = o
                    total += solve(tuple(child), mask, budget-1)
                best = min(best, total)
        return best
    return solve((0,)*r, 0, H), counter


def case(index):
    # Ten small comparisons plus two genuinely executed compact large sources.
    large = index >= 10
    m, r, H = ((31, 3, 6) if index == 10 else (101, 4, 8)) if large else (3+index%3, min(2, 1+index%2), 2+index%3)
    src = source(m, r, 100+index)
    rng = random.Random(500+index)
    weights = tuple(F(rng.choice((-3,-2,-1,1,2,3))) for _ in range(m))
    flip_fee = tuple(F(rng.randrange(1,5), 4) for _ in range(m))
    query_fee = tuple(F(1, 16) for _ in range(r))
    start = time.perf_counter_ns()
    value, action, plan, counts, _ = compact_plan(src, weights, flip_fee, query_fee, H)
    elapsed = time.perf_counter_ns()-start
    comparisons = []
    if not large:
        for dependence in ('conditional_independent', 'common_uniform'):
            law = full_law(src, dependence)
            exact, counters = unrestricted_plan(law, weights, flip_fee, query_fee, H)
            assert exact == value, (index, dependence, exact, value)
            comparisons.append({'dependence': dependence, 'nonzero_worlds': len(law), 'value': str(exact), 'work': counters})
    # Strong ordinary counterpart is identical conditional-moment DP.
    ordinary, ordinary_action, ordinary_plan, ordinary_counts, _ = compact_plan(src, weights, flip_fee, query_fee, H)
    assert (value, action, plan, counts) == (ordinary, ordinary_action, ordinary_plan, ordinary_counts)
    return dict(index=index, m=m, r=r, horizon=H,
                source_entries=2**r*(m-r+1), full_joint_slots=2**m,
                compact_value=str(value), root_action=action, plan=plan, compact_work=counts,
                compact_elapsed_ns=elapsed, full_comparisons=comparisons,
                ordinary_equivalent='exact value, chosen plan and counted work tie',
                source={'mass': list(map(str,src['mass'])), 'thresholds': src['thresholds'],
                        'weights': list(map(str,weights)), 'flip_fees': list(map(str,flip_fee)), 'query_fees': list(map(str,query_fee))},
                limitations='Supplied compact value source; no sample-learning or full economic-cost claim. Full-joint large comparator is a slot count, not an executed allocation.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    try:
        result = case(args.case)
    except Exception as exc:
        args.out.with_suffix('.failure.json').write_text(json.dumps({'case': args.case, 'error': repr(exc), 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}, indent=2)+'\n',encoding='utf-8',newline='\n')
        raise
    result['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('plan','source','full_comparisons')}))


if __name__ == '__main__':
    main()
