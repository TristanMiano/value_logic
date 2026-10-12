#!/usr/bin/env python3
"""Exact prior-free expected tariff of one randomized threshold policy.

DEVELOPMENT, ChatGPT (GPT-6 Astra Pro), 2026-10-12. Conditional on the
already admitted homogeneous source in quotient_closed_form.md. No acquisition.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json
import sys

VERSION = 's07-random-order-quote-v1'


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def quote(n, r, l, m, audit=1, decision=1):
    if any(type(x) is not int for x in (n, r, l, m)) or not (r > 0 and l > 0 and r+l-1 <= n and 0 <= m <= n):
        raise ValueError('Positive complete thresholds and a fixed binary source required')
    audit, decision = F(audit), F(decision)
    if audit <= 0 or decision <= 0:
        raise ValueError('Positive declared observation tariffs required')
    kmax = r+l-1
    et = sum((sum((F(choose(m, h)*choose(n-m, k-h), choose(n, k))
                  for h in range(max(0, k-l+1), min(k, r-1)+1)), F(0))
              for k in range(kmax)), F(0))
    pr = sum((F(choose(m, h)*choose(n-m, kmax-h), choose(n, kmax))
              for h in range(r)), F(0))
    # Independent stopping-distribution formula.
    stopped = sum((F(choose(l+h-1, h)*choose(n-l-h, m-h), choose(n, m))
                   * (audit*(l+h)+decision) for h in range(r)), F(0))
    stopped += sum((F(choose(r+j-1, j)*choose(n-r-j, m-r), choose(n, m))
                    * audit*(r+j) for j in range(l)), F(0))
    bill = audit*et+decision*pr
    if stopped != bill:
        raise AssertionError('Survival and stopping-distribution formulas disagree')
    return dict(mean_mandatory_audits=et, repair_probability=pr, expected_observation_tariff=bill)


def literal(n, r, l, m):
    total_t = total_repair = count = 0
    for highs in combinations(range(n), m):
        highs = set(highs)
        h = lo = 0
        for i in range(n):
            h += i in highs
            lo += i not in highs
            if h >= r or lo >= l:
                total_t += i+1
                total_repair += lo >= l
                count += 1
                break
    return F(total_t, count), F(total_repair, count)


def run(output):
    if output.exists():
        raise FileExistsError('Preserve executed development records')
    checks = 0
    for n in range(1, 8):
        for r in range(1, n+1):
            for l in range(1, n-r+2):
                for m in range(n+1):
                    q = quote(n, r, l, m)
                    t, p = literal(n, r, l, m)
                    assert q['mean_mandatory_audits'] == t
                    assert q['repair_probability'] == p
                    checks += 1
    examples = []
    for n, r, l in [(3, 2, 2), (127, 64, 64), (128, 64, 64)]:
        bills = [(m, quote(n, r, l, m)) for m in range(n+1)]
        worst = max(q['expected_observation_tariff'] for m, q in bills)
        reduced = max(q['expected_observation_tariff'] for m, q in bills if r-1 <= m <= n-l+1)
        assert worst == reduced
        if r+l-1 == n:
            assert worst == max(F(l*(n+1), l+1)+1, F(r*(n+1), r+1))
        examples.append(dict(n=n, high_threshold=r, low_threshold=l,
            full_count_search=n+1, reduced_count_search=n-(r+l-1)+2,
            fixed_source_worst_expected_tariff=worst,
            attaining_high_counts=[m for m, q in bills if q['expected_observation_tariff'] == worst],
            maximum_realized_tariff=r+l,
            audit_price=1, decision_audit_price=1))
    result = dict(version=VERSION, status='passed', contributor='ChatGPT (GPT-6 Astra Pro)',
        created_utc=datetime.now(timezone.utc).isoformat(),
        implementation_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        exact_literal_comparisons=checks, examples=examples, actual_new_acquisitions=0,
        scope='Expectation over a uniform internal row permutation; each source assignment is fixed independently beforehand. All actions are checked pathwise. This is one policy, not randomized-policy optimality or a complete-cost comparison.')
    output.write_text(json.dumps(result, indent=2, default=str)+'\n')
    print(json.dumps(result, default=str))


if __name__ == '__main__':
    run(Path(sys.argv[1]))
