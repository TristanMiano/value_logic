"""DEVELOPMENT exact cycle-guard semantics and rational envelope attainment."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import sys
import time

HERE = Path(__file__).resolve().parent


def circle_pairs(capacities):
    total = sum(capacities)
    if total == 0:
        return {}
    half = total/2
    assert max(capacities) <= half
    ends = [F(0)]
    for c in capacities:
        ends.append(ends[-1]+c)
    points = sorted({F(0), half} | {x for x in ends if 0 < x < half}
                    | {x-half for x in ends if half < x < total})
    masses = {}
    for left, right in zip(points, points[1:]):
        u = (left+right)/2
        i = next(i for i in range(len(capacities)) if ends[i] <= u < ends[i+1])
        j = next(i for i in range(len(capacities)) if ends[i] <= u+half < ends[i+1])
        assert i != j
        key = (1 << i) | (1 << j)
        masses[key] = masses.get(key, F(0))+right-left
    assert sum(masses.values()) == half
    return masses


def unconditional(eps):
    total, maximum = sum(eps), max(eps)
    others = total-maximum
    optimum = min(F(1), total/2, others)
    if optimum == 0:
        return optimum, {0: F(1)}
    if others < total/2:
        i = eps.index(maximum)
        masses = {(1 << i) | (1 << j): p for j, p in enumerate(eps) if j != i and p}
    else:
        cap, remaining = [], 2*optimum
        for p in eps:
            cap.append(min(p, remaining))
            remaining -= cap[-1]
        assert remaining == 0
        masses = circle_pairs(cap)
    masses[0] = 1-sum(masses.values())
    return optimum, masses


def conditional(eps):
    total, maximum = sum(eps), max(eps)
    others = total-maximum
    if others == 0:
        return F(0), {0: F(1)}
    if total <= 1:
        if maximum <= total/2:
            return unconditional(eps)
        i = eps.index(maximum)
        masses = {(1 << i) | (1 << j): p for j, p in enumerate(eps) if j != i and p}
        masses[1 << i] = maximum-others
        masses[0] = 1-maximum
        return others/(1-maximum+others), masses
    i, j = [i for i, p in enumerate(eps) if p][:2]
    bad = min((total-1)/2, eps[i]/2, eps[j]/2, F(1, 2))
    cap = list(eps)
    cap[i] -= bad
    cap[j] -= bad
    masses = {(1 << i) | (1 << j): bad}
    remaining = 1-bad
    for k, p in enumerate(cap):
        use = min(p, remaining)
        masses[1 << k] = use
        remaining -= use
    assert remaining == 0
    return F(1), masses


def verify_distribution(eps, masses):
    assert sum(masses.values()) == 1
    assert all(p >= 0 for p in masses.values())
    for i, bound in enumerate(eps):
        assert sum(p for e, p in masses.items() if e >> i & 1) <= bound
    accept = sum(p for e, p in masses.items() if e.bit_count() % 2 == 0)
    bad = accept-masses.get(0, F(0))
    reject = 1-accept
    assert 2*bad+reject <= sum(eps)
    assert accept > 0
    return bad, bad/accept, accept


def semantics():
    checks = 0
    for n in range(3, 8):
        for x in range(1 << n):
            truth = sum((((x >> i) ^ (x >> ((i+1) % n))) & 1) << i for i in range(n))
            for predicted in range(1 << n):
                error = predicted ^ truth
                y = x & 1
                for i in range(1, n):
                    bit = ((y >> (i-1)) ^ (predicted >> (i-1))) & 1
                    y |= bit << i
                accepted = ((y >> (n-1)) ^ y ^ (predicted >> (n-1))) & 1 == 0
                assert accepted == (error.bit_count() % 2 == 0)
                bad = accepted and y != x
                assert bad == (accepted and error != 0)
                assert 2*int(bad)+int(not accepted) <= error.bit_count()
                checks += 1
    return checks


def main():
    begun = time.perf_counter_ns()
    rng = random.Random(120032)
    panels = [tuple(F(k, 10) for k in row) for row in product(range(11), repeat=3)]
    panels += [tuple(F(rng.randrange(101), 100) for _ in range(n))
               for n in range(4, 9) for _ in range(100)]
    # Add heterogeneous small-total regimes; the uniform grid is mostly S>1.
    panels += [tuple(F(rng.randrange(21), 100*n) for _ in range(n))
               for n in range(4, 9) for _ in range(100)]
    examples = []
    for eps in panels:
        ub, up = unconditional(eps)
        cb, cp = conditional(eps)
        observed_u, _, _ = verify_distribution(eps, up)
        _, observed_c, _ = verify_distribution(eps, cp)
        assert ub == observed_u, (eps, ub, observed_u)
        assert cb == observed_c, (eps, cb, observed_c)
    for eps in [(F(1, 100),)*10, (F(1, 2), F(1, 20), F(1, 20)),
                (F(1, 2), F(1, 2), F(1, 100))]:
        ub, up = unconditional(eps)
        cb, cp = conditional(eps)
        _, _, acceptance = verify_distribution(eps, cp)
        examples.append(dict(marginal_bounds=list(map(str, eps)),
                             bad_release=str(ub), conditional_error=str(cb),
                             conditional_attainment_acceptance=str(acceptance)))
    result = dict(status='PASS', scope='DEVELOPMENT', contributor='Codex (GPT-6)',
                  python=sys.version, seed=120032, marginal_panels=len(panels),
                  exact_attainment_checks=2*len(panels),
                  semantic_checks=semantics(), examples=examples,
                  elapsed_ns=time.perf_counter_ns()-begun,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  limitations='Exact finite semantics and explicit extremal distributions; '
                              'not a trained-model experiment, calibration purchase, or '
                              'independent proof of the all-size envelopes.')
    (HERE/'coherence_probe.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
