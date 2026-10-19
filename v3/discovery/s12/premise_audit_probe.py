"""Finite DEVELOPMENT screen; source and output freeze after first execution."""
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial, ceil
from pathlib import Path
import hashlib
import json
import random
import sys
import time

HERE = Path(__file__).resolve().parent


def hg(n, b, m):
    return F(comb(n-b, m), comb(n, m)) if m <= n-b else F(0)


def main():
    started = time.perf_counter_ns()
    alphas = [F(1, 100), F(1, 10), F(1, 3)]
    executions = comparisons = packing_checks = 0
    for n in range(1, 8):
        # All thresholds are fixed before enumerating audit orders.
        thresholds = {(b, a): next(m for m in range(n+1) if hg(n,b,m)<=a)
                      for b in range(1,n+1) for a in alphas}
        for b in range(1,n+1):
            for m in range(n+1):
                for k in range(1,b+1):
                    assert hg(n,b,m) <= hg(n,k,m)
        for bad in range(1,1<<n):
            b = bad.bit_count()
            crossings = [0]*len(alphas)
            for order in permutations(range(n)):
                first_bad = next(j+1 for j,i in enumerate(order) if bad>>i&1)
                for j,a in enumerate(alphas):
                    crossings[j] += first_bad > thresholds[b,a]
                executions += 1
            for j,a in enumerate(alphas):
                risk = F(crossings[j],factorial(n))
                assert risk == hg(n,b,thresholds[b,a]) and risk<=a
                comparisons += 1
    rng = random.Random(121019)
    for n in range(2,7):
        for _ in range(24):
            supports = sorted(set(rng.randrange(1,1<<n) for _ in range(2*n)))
            degree = max(sum(bool(s>>i&1) for s in supports) for i in range(n))
            k = ceil(F(len(supports),degree))
            minimum = min(b.bit_count() for b in range(1<<n)
                          if all(b&s for s in supports))
            assert k <= minimum
            for b in range(1<<n):
                if all(b&s for s in supports):
                    assert b.bit_count() >= k
                packing_checks += 1
    example=[]
    for a in [F(1,20),F(1,100),F(1,1000)]:
        m = next(m for m in range(101) if hg(100,50,m)<=a)
        example.append(dict(alpha=str(a), audits=m, false_release_bound=str(hg(100,50,m)),
                            bound_decimal=float(hg(100,50,m)), exact_positive_certificate=51,
                            query_count_reduction=str(F(51-m,51))))
    result=dict(status='PASS', contributor='Codex (GPT-6)', scope='DEVELOPMENT',
                python=sys.version, elapsed_ns=time.perf_counter_ns()-started,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                totals=dict(fixed_bad_set_permutation_executions=executions,
                            exact_crossing_comparisons=comparisons,
                            support_packing_bad_set_checks=packing_checks),
                example=example,
                limitations='Zero-failure uniform audits of a fixed premise universe. '
                'Constructed acceptance-sampling example; computational setup, sampling, '
                'proof discovery/checking and nonuniform premise costs excluded. '
                'Ordinary acceptance sampling and logical checking give the same result.')
    (HERE/'premise_audit_probe.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
