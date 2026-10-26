"""Frozen small exact adversary screen for tied-feedback ordinal learning."""
from collections import Counter
from functools import lru_cache
from itertools import permutations
from math import comb
from pathlib import Path
import hashlib
import json
import platform
import random
import time

started = time.perf_counter_ns()
stats = Counter()


def score(order, counts, d):
    return sum(counts[a*d+b] for k, a in enumerate(order) for b in order[k+1:])


def rank_dp(counts, d):
    incoming = [[0]*(1 << d) for _ in range(d)]
    for b in range(d):
        for mask in range(1, 1 << d):
            bit = mask & -mask
            a = bit.bit_length()-1
            incoming[b][mask] = incoming[b][mask ^ bit]+counts[a*d+b]
    best = {0: (0, ())}
    for mask in range(1, 1 << d):
        choices = []
        for b in range(d):
            if mask >> b & 1:
                prev = mask ^ (1 << b)
                val, order = best[prev]
                choices.append((val+incoming[b][prev], order+(b,)))
                stats['ranking_dp_transitions'] += 1
        best[mask] = min(choices, key=lambda p: (-p[0], p[1]))
    return best[(1 << d)-1]


@lru_cache(None)
def choose(counts, d, gap):
    stats['distinct_rankings'] += 1
    val, order = rank_dp(counts, d)
    if gap:
        # Only a tiny finite oracle for the absolute-gap variant.
        order = next(p for p in permutations(range(d)) if score(p, counts, d) >= val-gap)
    assert score(order, counts, d) >= val-gap
    return order


def adversary(utility, horizon, corruption, gap, saturated):
    d = len(utility)
    cap = corruption+gap+1 if saturated else None
    contexts = [tuple(i for i in range(d) if mask >> i & 1)
                for mask in range(1, 1 << d) if mask.bit_count() > 1]

    @lru_cache(None)
    def rec(counts, rounds, left):
        stats['adversary_states'] += 1
        if not rounds:
            return 0
        order = choose(counts, d, gap)
        ans = 0
        for subset in contexts:
            pred = next(x for x in order if x in subset)
            optimum = max(utility[x] for x in subset)
            loss = int(utility[pred] < optimum)
            for observed in subset:
                bad = int(utility[observed] < optimum)
                if bad > left:
                    continue
                nxt = list(counts)
                if observed != pred:
                    at = observed*d+pred
                    nxt[at] += 1
                    if cap is not None:
                        nxt[at] = min(nxt[at], cap)
                stats['adversary_transitions'] += 1
                ans = max(ans, loss+rec(tuple(nxt), rounds-1, left-bad))
        return ans

    worst = rec((0,)*(d*d), horizon, corruption)
    bound = comb(d, 2)*(corruption+gap+1)+corruption
    assert worst <= bound, (utility, horizon, corruption, gap, saturated, worst, bound)
    out = dict(utility=utility, horizon=horizon, corruption_ceiling=corruption,
               additive_gap=gap, saturated=saturated, worst_mistakes=worst,
               theorem_bound=bound, states=rec.cache_info().currsize)
    rec.cache_clear()
    return out


rng = random.Random(2026102518)
for case in range(100):
    d = 2+case % 5
    counts = tuple(0 if a == b else rng.randrange(6)
                   for a in range(d) for b in range(d))
    val, order = rank_dp(counts, d)
    oracle = min(((score(p, counts, d), p) for p in permutations(range(d))),
                 key=lambda p: (-p[0], p[1]))
    assert (val, order) == oracle
    stats['permutation_crosschecks'] += 1

results = []
for utility in ((0, 1), (1, 0), (0, 0)):
    for corruption in (0, 1, 2):
        for gap in (0, 1):
            for saturated in (False, True):
                results.append(adversary(utility, 12, corruption, gap, saturated))
for utility in ((0, 1, 2), (0, 0, 1), (0, 1, 1), (0, 0, 0)):
    for corruption in (0, 1):
        for gap in (0, 1):
            for saturated in (False, True):
                results.append(adversary(utility, 10, corruption, gap, saturated))
for utility in ((0, 1, 2), (0, 0, 1)):
    for saturated in (False, True):
        results.append(adversary(utility, 12, 2, 0, saturated))

# One false response followed by truthful feedback: no permanent tie collapse.
counts = (0,)*4
trace = []
for observed in (1,)+(0,)*9:
    pred = choose(counts, 2, 0)[0]
    trace.append(dict(predicted=pred, observed=observed, mistake=pred != 0))
    nxt = list(counts)
    if observed != pred:
        nxt[observed*2+pred] += 1
    counts = tuple(nxt)
assert sum(t['mistake'] for t in trace) <= 3
assert all(t['predicted'] == 0 for t in trace[3:])

result = dict(status='PASS', python=platform.python_version(),
              runtime_ns=time.perf_counter_ns()-started, stats=dict(stats),
              adversary_cases=results, recovery_trace=trace,
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              limitation='Same-model finite development check; no novelty, audit-fee or full-cost speed claim.')
Path(__file__).with_name('tied_result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(status=result['status'], runtime_ns=result['runtime_ns'],
                     source_sha256=result['source_sha256'], stats=result['stats'],
                     adversary_case_count=len(results))))
