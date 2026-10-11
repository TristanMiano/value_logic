"""DEVELOPMENT: exact post-certificate feedback and incomparability witnesses.

Codex (GPT-6), 2026-10-11. Prices are explicitly stipulated query prices;
controller operation counts and measured wall times are separate quantities.
"""
from datetime import datetime, timezone
from itertools import permutations, product
import hashlib
import json
from pathlib import Path
import random
import sys
import time
import traceback


def execute(order, x, k, prices):
    ones = zeros = bill = 0
    receipts = {}
    for t in order:
        bit = x[t]
        receipts[t] = bit
        bill += prices[t][bit]
        ones += bit
        zeros += 1-bit
        if ones >= k or zeros >= len(order)-k+1:
            return bill, receipts, int(ones >= k)
    raise AssertionError('Threshold never resolved')


def post_bounds(order, k, prices, receipts):
    """Exact retrospective bounds, outcome-independent prices only."""
    n = len(order)
    assert all(c[0] == c[1] and c[0] >= 0 for c in prices)
    ones, zeros = sum(receipts.values()), len(receipts)-sum(receipts.values())
    assert ones >= k or zeros >= n-k+1
    e = int(ones >= k)
    low_x = [receipts.get(t, e) for t in range(n)]
    high_x = [receipts.get(t, 1-e) for t in range(n)]
    low, lr, _ = execute(order, low_x, k, prices)
    high, hr, _ = execute(order, high_x, k, prices)
    return dict(lower=low, upper=high, endpoint_query_visits=len(lr)+len(hr),
                lower_witness=low_x, upper_witness=high_x)


def incomparable(a, b, k):
    """Return cost-independent witnesses, or None for equivalent orders."""
    n, m = len(a), min(k, len(a)-k+1)
    e = int(k <= n-k+1)
    aa, bb = set(a[:m]), set(b[:m])
    j = m
    if aa == bb:
        while j < n and a[j] == b[j]:
            j += 1
        if j == n:
            return None
        common = a[:j]
        win_a = set(common[:m-1]) | {a[j]}
        win_b = set(common[:m-1]) | {b[j]}
    else:
        win_a, win_b = aa, bb
    a_faster = [e if t in win_a else 1-e for t in range(n)]
    b_faster = [e if t in win_b else 1-e for t in range(n)]
    return a_faster, b_faster


def main(output):
    assert not output.exists()
    started = time.monotonic_ns()
    r = dict(status='running', evidence='DEVELOPMENT', contributor='Codex (GPT-6)',
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             seed=8401, command=sys.argv, start_utc=datetime.now(timezone.utc).isoformat())
    try:
        rng = random.Random(8401)
        dominance_cases = equivalence_cases = witness_checks = 0
        for n in range(1, 7):
            a = list(range(n))
            prices = [(rng.randrange(1, 100), rng.randrange(1, 100)) for _ in a]
            for b in permutations(a):
                for k in range(1, n+1):
                    witness = incomparable(a, b, k)
                    dominance_cases += 1
                    if witness is None:
                        equivalence_cases += 1
                        for x in product((0, 1), repeat=n):
                            assert execute(a, x, k, prices)[0] == execute(b, x, k, prices)[0]
                    else:
                        xa, xb = witness
                        assert execute(a, xa, k, prices)[0] < execute(b, xa, k, prices)[0]
                        assert execute(b, xb, k, prices)[0] < execute(a, xb, k, prices)[0]
                        witness_checks += 2
        feedback_cases = compatible = 0
        examples = []
        for n in range(1, 10):
            for trial in range(30):
                a, b = list(range(n)), list(range(n))
                rng.shuffle(a)
                rng.shuffle(b)
                k = rng.randrange(1, n+1)
                x = [rng.randrange(2) for _ in a]
                prices = [(c, c) for c in [rng.randrange(1, 50) for _ in a]]
                selected_bill, receipts, e = execute(a, x, k, prices)
                got = post_bounds(b, k, prices, receipts)
                all_bills = []
                for xx in product((0, 1), repeat=n):
                    if all(xx[t] == bit for t, bit in receipts.items()):
                        all_bills.append(execute(b, xx, k, prices)[0])
                        assert execute(a, xx, k, prices)[0] == selected_bill
                assert (got['lower'], got['upper']) == (min(all_bills), max(all_bills))
                feedback_cases += 1
                compatible += len(all_bills)
                if len(examples) < 6 and len(receipts) < n and got['lower'] != got['upper']:
                    examples.append(dict(a=a, b=b, x=x, k=k, prices=prices,
                                         selected_bill=selected_bill, receipts=receipts, result=got))
        r.update(status='complete', dominance_cases=dominance_cases,
                 equivalent_order_cases=equivalence_cases, strict_witness_checks=witness_checks,
                 feedback_cases=feedback_cases, compatible_completions=compatible, examples=examples)
    except Exception:
        r.update(status='failed', failure=traceback.format_exc())
        raise
    finally:
        r['elapsed_ns'] = time.monotonic_ns()-started
        r['end_utc'] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(r, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({k:v for k,v in r.items() if k != 'examples'}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
