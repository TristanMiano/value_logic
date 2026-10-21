"""Development screen of constrained failure margins and rank calibration.
24 small action panels; finite multinomial enumeration, no Monte Carlo claim.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, inf
from pathlib import Path
import hashlib
import importlib.util
import json
import random
import time

ROOT = Path(__file__).resolve().parent
dependency = ROOT/'ordered_probe.py'
spec = importlib.util.spec_from_file_location('ordered_helpers_slack', dependency)
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)
RNG = random.Random(2026102010)


def margin(upper, arcs, prices, edges, units, low, high, optimum):
    values = []
    for i, j in edges:
        added = [(H.TRUE, H.bit(upper, i, low[i])), (H.bit(upper, j, high[j]), H.FALSE)]
        cost, _ = H.optimize(upper, arcs+added, prices)
        values.append(inf if cost is None else cost-optimum)
    for i, b in units:
        added = [(H.bit(upper, i, high[i]), H.FALSE)] if b else [(H.TRUE, H.bit(upper, i, low[i]))]
        cost, _ = H.optimize(upper, arcs+added, prices)
        values.append(inf if cost is None else cost-optimum)
    return min(values, default=inf), len(values)


def histograms(total, categories):
    if categories == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in histograms(total-first, categories-1):
                yield (first,)+rest


def cutoff(scores, k, cap=4):
    return min(cap, sorted(scores)[k-1]-1)


def main():
    began = time.perf_counter_ns()
    count = dict(panels=0, exact_margins=0, box_margins=0, mincut_calls=0,
                 strict_partial_gaps=0, finite_population_worlds=0,
                 calibration_panels=0, calibration_histograms=0, no_rank_certificate=0)
    for n in range(2, 5):
        for _ in range(8):
            upper = tuple(RNG.randrange(1, 3) for _ in range(n))
            actions = list(product(*(range(k+1) for k in upper)))
            worlds = list(product(*(range(k+2) for k in upper)))
            seedworlds = list(product(*(range(k+1) for k in upper)))
            source = set(RNG.sample(seedworlds, RNG.randrange(1, min(6, len(seedworlds))+1)))
            edges = list({tuple(RNG.sample(range(n), 2)) for _ in range(n+1)})
            units = [(RNG.randrange(n), True)]
            prices = [tuple(RNG.randrange(8) for _ in range(k+1)) for k in upper]
            arcs = H.compile_actions(upper, source, edges, units, [])
            allowed = [a for a in actions if H.accepts(a, arcs)]
            costs = {a:sum(prices[i][a[i]] for i in range(n)) for a in allowed}
            optimum, _ = H.optimize(upper, arcs, prices)
            count['mincut_calls'] += 1
            assert optimum == min(costs.values())
            direct = {w:min((costs[a]-optimum for a in allowed if not H.goal_ok(a, w, edges, units)), default=inf) for w in worlds}
            count['finite_population_worlds'] += len(worlds)
            for w in RNG.sample(worlds, 8):
                z, calls = margin(upper, arcs, prices, edges, units, w, w, optimum)
                count['mincut_calls'] += calls
                count['exact_margins'] += 1
                assert z == direct[w]
                low = tuple(RNG.randrange(t+1) for t in w)
                high = tuple(RNG.randrange(t, upper[i]+2) for i, t in enumerate(w))
                lower, calls = margin(upper, arcs, prices, edges, units, low, high, optimum)
                count['mincut_calls'] += calls
                count['box_margins'] += 1
                box = [x for x in worlds if all(l <= t <= u for l, t, u in zip(low, x, high))]
                assert w in box and lower == min(direct[x] for x in box) <= z
                count['strict_partial_gaps'] += lower < z
            count['panels'] += 1

    scores = (0, 1, 3, inf)
    panels = []
    for weights in ((1, 2, 3, 4), (0, 1, 1, 8), (3, 3, 3, 1)):
        probs = tuple(F(w, sum(weights)) for w in weights)
        for size in (5, 8, 12):
            for alpha in (F(1, 4), F(1, 2)):
                for delta in (F(1, 10), F(1, 4)):
                    ranks = [k for k in range(1, size+1) if sum(F(comb(size, j))*alpha**j*(1-alpha)**(size-j) for j in range(k)) <= delta]
                    if not ranks:
                        count['no_rank_certificate'] += 1
                        continue
                    k = max(ranks)
                    bad = F(0)
                    mass_total = F(0)
                    for hist in histograms(size, len(scores)):
                        mass = F(factorial(size))
                        sample = []
                        for z, p, number in zip(scores, probs, hist):
                            mass *= p**number / factorial(number)
                            sample += [z]*number
                        mass_total += mass
                        epsilon = cutoff(sample, k)
                        risk = sum(p for z, p in zip(scores, probs) if z <= epsilon)
                        if epsilon >= 0 and risk > alpha:
                            bad += mass
                        # Simulate conservatively censored/refined scores. Their
                        # dependence on the whole histogram is intentionally allowed.
                        lower = [0 if (i+sum(hist[::2])) % 3 == 0 else max(0, z-1) for i, z in enumerate(sample)]
                        assert all(l <= z for l, z in zip(lower, sample))
                        eps_lower = cutoff(lower, k)
                        assert eps_lower <= epsilon
                        risk_lower = sum(p for z, p in zip(scores, probs) if z <= eps_lower)
                        assert risk_lower <= risk
                        count['calibration_histograms'] += 1
                    assert mass_total == 1 and bad <= delta
                    count['calibration_panels'] += 1
                    panels.append(dict(weights=weights, n=size, alpha=str(alpha), delta=str(delta),
                                       rank=k, actual_bad_certificate_probability=str(bad)))
    result = dict(status='PASS', contributor='Codex (GPT-6)', seed=2026102010,
                  counts=count, calibration_panels=panels,
                  elapsed_ns=time.perf_counter_ns()-began,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  dependency_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (dependency, ROOT/'edge_extension.py')},
                  scope='same-model finite development; neither application label savings nor independent confirmation')
    (ROOT/'slack_probe.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'], counts=count, elapsed_ns=result['elapsed_ns'])))


if __name__ == '__main__':
    main()
