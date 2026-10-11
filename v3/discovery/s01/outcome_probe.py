"""DEVELOPMENT: outcome-local query costs and cache-aware remaining bills.

Codex (GPT-6), 2026-10-11. Extends the derivation in comparison.md; neither
the tariffs nor the hidden bits are claims about measured solver behavior.
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


def actual(order, x, k, prices):
    ones = zeros = cost = 0
    for t in order:
        cost += prices[t][x[t]]
        ones += x[t]
        zeros += 1-x[t]
        if ones >= k or zeros >= len(x)-k+1:
            return cost
    raise AssertionError('No stop.')


def compare(a, b, k, prices, known):
    n = len(a)
    assert sorted(a) == sorted(b) == list(range(n))
    assert len(prices) == n and all(len(c) == 2 and min(c) >= 0 for c in prices)
    assert 1 <= k <= n and all(t in range(n) and bit in (0, 1) for t, bit in known.items())
    best = {'lower': None, 'upper': None}
    cases = z_cases = 0
    for e in (0, 1):
        need = (k if e else n-k+1)-1
        for i in range(n):
            for j in range(n):
                if any(t in known and known[t] != e for t in (a[i], b[j])):
                    continue
                fixed = dict(known)
                fixed[a[i]] = fixed[b[j]] = e
                X, Y = set(a[:i]), set(b[:j])
                groups = [sorted((X & Y)-fixed.keys()), sorted((X-Y)-fixed.keys()), sorted((Y-X)-fixed.keys())]
                rx = need-sum(fixed[t] == e for t in X if t in fixed)
                ry = need-sum(fixed[t] == e for t in Y if t in fixed)
                lo, hi = max(0, rx-len(groups[1]), ry-len(groups[2])), min(len(groups[0]), rx, ry)
                if lo > hi:
                    continue
                cases += 1
                queried_a, queried_b = X | {a[i]}, Y | {b[j]}
                signs = {t: int(t in queried_a)-int(t in queried_b) for t in range(n)}
                base_x = [fixed.get(t, 1-e) for t in range(n)]
                base = sum(signs[t]*prices[t][base_x[t]] for t in range(n))
                for direction in ('lower', 'upper'):
                    ordered = [sorted(g, key=lambda t: (signs[t]*(prices[t][e]-prices[t][1-e]), t),
                                      reverse=direction == 'upper') for g in groups]
                    prefix = []
                    for g in ordered:
                        sums = [0]
                        for t in g:
                            sums.append(sums[-1]+signs[t]*(prices[t][e]-prices[t][1-e]))
                        prefix.append(sums)
                    for z in range(lo, hi+1):
                        z_cases += 1
                        counts = (z, rx-z, ry-z)
                        delta = base+sum(sums[count] for sums, count in zip(prefix, counts))
                        improve = best[direction] is None or (delta < best[direction] if direction == 'lower' else delta > best[direction])
                        if improve:
                            x = base_x.copy()
                            for g, count in zip(ordered, counts):
                                for t in g[:count]:
                                    x[t] = e
                            best[direction] = delta
                            best[direction+'_witness'] = x
                            best[direction+'_stop'] = [e, i, j]
    assert best['lower'] is not None
    for key in ('lower', 'upper'):
        x = best[key+'_witness']
        assert all(x[t] == bit for t, bit in known.items())
        assert actual(a, x, k, prices)-actual(b, x, k, prices) == best[key]
    return dict(best, feasible_stop_pairs=cases, intersection_count_choices=z_cases)


def remaining(a, b, k, prices, receipts):
    new_k = k-sum(receipts.values())
    unknown = [i for i in range(len(a)) if i not in receipts]
    if new_k <= 0 or new_k > len(unknown):
        return dict(lower=0, upper=0, already_decided=True, remaining_coordinates=unknown)
    renamed = {t:i for i,t in enumerate(unknown)}
    aa = [renamed[t] for t in a if t in renamed]
    bb = [renamed[t] for t in b if t in renamed]
    answer = compare(aa, bb, new_k, [prices[t] for t in unknown], {})
    return dict(answer, already_decided=False, remaining_coordinates=unknown)


def brute(a, b, k, prices, receipts, from_now=False):
    deltas = []
    for x in product((0, 1), repeat=len(a)):
        if not all(x[t] == bit for t, bit in receipts.items()):
            continue
        if from_now:
            new_k = k-sum(receipts.values())
            unknown = [t for t in range(len(a)) if t not in receipts]
            if new_k <= 0 or new_k > len(unknown):
                deltas.append(0)
                continue
            rename = {t:i for i,t in enumerate(unknown)}
            aa, bb = [[rename[t] for t in order if t in rename] for order in (a, b)]
            xx, pp = [x[t] for t in unknown], [prices[t] for t in unknown]
            deltas.append(actual(aa, xx, new_k, pp)-actual(bb, xx, new_k, pp))
        else:
            deltas.append(actual(a, x, k, prices)-actual(b, x, k, prices))
    return min(deltas), max(deltas), len(deltas)


def main(output):
    assert not output.exists()
    start = time.monotonic_ns()
    r = dict(status='running', evidence='DEVELOPMENT', contributor='Codex (GPT-6)', seed=7402,
             start_utc=datetime.now(timezone.utc).isoformat(), command=sys.argv,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    try:
        rng, cases, completions = random.Random(7402), 0, 0
        distinctions, dominance = [], []
        for n in range(1, 8):
            for trial in range(30):
                a, b = list(range(n)), list(range(n))
                rng.shuffle(a)
                rng.shuffle(b)
                k = rng.randrange(1, n+1)
                prices = [(rng.randrange(1, 15), rng.randrange(1, 15)) for _ in range(n)]
                receipts = {i:rng.randrange(2) for i in range(n) if rng.randrange(3) == 0}
                retro = compare(a, b, k, prices, receipts)
                live = remaining(a, b, k, prices, receipts)
                for got, is_live in ((retro, False), (live, True)):
                    low, high, count = brute(a, b, k, prices, receipts, is_live)
                    assert (got['lower'], got['upper']) == (low, high)
                    cases += 1
                    completions += count
                record = dict(a=a, b=b, k=k, prices=prices, receipts=receipts, retrospective=retro, remaining=live)
                if len(distinctions) < 4 and (retro['lower'], retro['upper']) != (live['lower'], live['upper']):
                    distinctions.append(record)
                if len(dominance) < 4 and a != b and live['upper'] <= 0 and not live['already_decided']:
                    dominance.append(record)
        r.update(status='complete', comparison_checks=cases, compatible_completions=completions,
                 retrospective_remaining_distinctions=distinctions, remaining_dominance_examples=dominance)
    except Exception:
        r.update(status='failed', failure=traceback.format_exc())
        raise
    finally:
        r['elapsed_ns'] = time.monotonic_ns()-start
        r['end_utc'] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(r, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({k:v for k,v in r.items() if k not in ('retrospective_remaining_distinctions', 'remaining_dominance_examples')}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
