"""Exact coupled query-policy comparison; DEVELOPMENT, Codex (GPT-6).

See comparison.md for input contract and derivation. This compares fixed
orders, not adaptive SBB. Integer prices are stipulated, not solver runtime.
"""
from datetime import datetime, timezone
from itertools import product
import hashlib
import json
from pathlib import Path
import random
import sys
import time
import traceback


def cumulative(items):
    out = [0]
    for x in items:
        out.append(out[-1]+x)
    return out


def actual_cost(order, x, k, prices, setup=0, step=0):
    ones = zeros = 0
    cost = setup
    for i in order:
        cost += prices[i] + step
        ones += x[i]
        zeros += 1-x[i]
        if ones >= k or zeros >= len(x)-k+1:
            return cost
    raise AssertionError('Threshold never resolved.')


def witness(a, b, known, e, i, j, k):
    x = dict(known)
    x[a[i]] = x[b[j]] = e
    X, Y = set(a[:i]), set(b[:j])
    I = sorted((X & Y)-x.keys())
    P = sorted((X-Y)-x.keys())
    Q = sorted((Y-X)-x.keys())
    need = (k if e else len(a)-k+1)-1
    rx = need-sum(x[t] == e for t in X if t in x)
    ry = need-sum(x[t] == e for t in Y if t in x)
    z = max(0, rx-len(P), ry-len(Q))
    assert z <= min(len(I), rx, ry)
    for group, count in ((I, z), (P, rx-z), (Q, ry-z)):
        for index, t in enumerate(group):
            x[t] = e if index < count else 1-e
    return tuple(x.get(t, 1-e) for t in range(len(a)))


def compare(a, b, k, prices, known, setup=(0, 0), step=(0, 0)):
    n = len(a)
    assert sorted(a) == sorted(b) == list(range(n))
    assert len(prices) == n and min(prices) >= 0 and 1 <= k <= n
    assert all(i in range(n) and x in (0, 1) for i, x in known.items())
    pa, pb = [0]*n, [0]*n
    for i in range(n):
        pa[a[i]], pb[b[i]] = i, i
    unknown_a = cumulative(int(i not in known) for i in a)
    unknown_b = cumulative(int(i not in known) for i in b)
    fixed_a = {e: cumulative(int(known.get(i) == e) for i in a) for e in (0, 1)}
    fixed_b = {e: cumulative(int(known.get(i) == e) for i in b) for e in (0, 1)}
    ca = cumulative(prices[t]+step[0] for t in a)
    cb = cumulative(prices[t]+step[1] for t in b)
    intersections = [[0]*(n+1) for _ in range(n+1)]
    for i in range(n):
        for j in range(n):
            intersections[i+1][j+1] = (intersections[i][j+1]+intersections[i+1][j]-intersections[i][j]
                                            + int(a[i] == b[j] and a[i] not in known))
    minimum, maximum, lower_key, upper_key = None, None, None, None
    feasible, pairs = 0, 0
    for e in (0, 1):
        need = (k if e else n-k+1)-1
        for i in range(n):
            if a[i] in known and known[a[i]] != e:
                continue
            for j in range(n):
                pairs += 1
                if b[j] in known and known[b[j]] != e:
                    continue
                extra_a = int(b[j] not in known and pa[b[j]] < i)
                extra_b = int(a[i] not in known and pb[a[i]] < j)
                u_i = intersections[i][j]
                u_p = unknown_a[i]-extra_a-u_i
                u_q = unknown_b[j]-extra_b-u_i
                rx = need-fixed_a[e][i]-extra_a
                ry = need-fixed_b[e][j]-extra_b
                lo, hi = max(0, rx-u_p, ry-u_q), min(u_i, rx, ry)
                if lo > hi:
                    continue
                feasible += 1
                delta = setup[0]-setup[1]+ca[i+1]-cb[j+1]
                if minimum is None or delta < minimum:
                    minimum, lower_key = delta, (e, i, j)
                if maximum is None or delta > maximum:
                    maximum, upper_key = delta, (e, i, j)
    assert minimum is not None
    lower_x = witness(a, b, known, *lower_key, k)
    upper_x = witness(a, b, known, *upper_key, k)
    for value, x in ((minimum, lower_x), (maximum, upper_x)):
        assert all(x[t] == bit for t, bit in known.items())
        assert actual_cost(a, x, k, prices, setup[0], step[0])-actual_cost(b, x, k, prices, setup[1], step[1]) == value
    return dict(lower=minimum, upper=maximum, lower_witness=lower_x, upper_witness=upper_x,
                lower_stop=lower_key, upper_stop=upper_key, feasible_stop_pairs=feasible,
                visited_pairs=pairs, prefix_cells=n*n)


def brute(a, b, k, prices, known, setup=(0, 0), step=(0, 0)):
    values_a, values_b, differences = [], [], []
    for x in product((0, 1), repeat=len(a)):
        if not all(x[t] == bit for t, bit in known.items()):
            continue
        ca = actual_cost(a, x, k, prices, setup[0], step[0])
        cb = actual_cost(b, x, k, prices, setup[1], step[1])
        values_a.append(ca)
        values_b.append(cb)
        differences.append(ca-cb)
    return dict(lower=min(differences), upper=max(differences),
                independent_lower=min(values_a)-max(values_b),
                independent_upper=max(values_a)-min(values_b), completions=len(differences))


def main(output):
    assert not output.exists()
    start = time.monotonic_ns()
    result = dict(status='running', evidence='DEVELOPMENT', contributor='Codex (GPT-6)',
                  start_utc=datetime.now(timezone.utc).isoformat(), command=sys.argv,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  seed=7401, contract='fixed-order k-of-n; nonnegative integer fixed query prices; optional fixed setup/step tariffs')
    try:
        rng = random.Random(7401)
        cases, completions, tightened = 0, 0, 0
        examples = []
        # Varied development, not independent confirmation or exhaustive over
        # orders. Within each fixture enumerate EVERY compatible completion.
        for n in range(1, 9):
            for trial in range(40):
                a, b = list(range(n)), list(range(n))
                rng.shuffle(a)
                rng.shuffle(b)
                k = rng.randrange(1, n+1)
                prices = [rng.randrange(0, 10) for _ in range(n)]
                known = {i: rng.randrange(2) for i in range(n) if rng.randrange(3) == 0}
                setup = (rng.randrange(4), rng.randrange(4))
                step = (rng.randrange(3), rng.randrange(3))
                exact = compare(a, b, k, prices, known, setup, step)
                enum = brute(a, b, k, prices, known, setup, step)
                assert (exact['lower'], exact['upper']) == (enum['lower'], enum['upper'])
                cases += 1
                completions += enum['completions']
                if exact['upper']-exact['lower'] < enum['independent_upper']-enum['independent_lower']:
                    tightened += 1
                if a != b and exact['upper'] <= 0 < enum['independent_upper'] and len(known) <= n//2:
                    examples.append(dict(a=a, b=b, k=k, prices=prices, known=known, setup=setup, step=step,
                                         exact=exact, enumeration=enum))
        result['small_checks'] = dict(fixtures=cases, completions=completions, narrower_than_independent=tightened)
        result['dominance_examples'] = examples
        # Structured nonidentical orders agree on the first n-2 positions.
        # Any cost difference lies in the final swap; most labels stay unknown.
        large = []
        for n in (32, 64, 128):
            a = list(range(n))
            b = list(range(n-2))+[n-1, n-2]
            prices = [100]*n
            prices[-1] = 200
            before = time.monotonic_ns()
            exact = compare(a, b, n//2, prices, {})
            large.append(dict(n=n, known_count=0, exact=exact, runtime_ns=time.monotonic_ns()-before,
                              note='No brute-force enumeration at this size; endpoint witnesses checked. Simple exchange is a stronger cheap control.'))
        result['large_development'] = large
        result['status'] = 'complete'
    except Exception:
        result['status'] = 'failed'
        result['failure'] = traceback.format_exc()
        raise
    finally:
        result['elapsed_ns'] = time.monotonic_ns()-start
        result['end_utc'] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ('dominance_examples', 'large_development')}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
