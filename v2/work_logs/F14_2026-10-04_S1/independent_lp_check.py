"""Development-only, independently formulated SciPy/HiGHS interface check.

Contributor: ChatGPT (GPT-6 Astra Pro), F14. SciPy is an optional audit tool,
not a frozen F15 runtime dependency. No final seeds are used. The independent
rows below deliberately do not use the project's path or payload decoders.
Run from repository root with python -m ... unavailable for this date-named
directory; instead PYTHONPATH=. python <this file> --out <result.json>.
"""
import argparse
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import json
from pathlib import Path
import platform
import time

import numpy as np
import scipy
from scipy.optimize import linprog
from v2.experiments import retention as R


WORLDS = tuple(product((0, 1), repeat=3))


def costs(order, prices, penalty):
    result = []
    for world in WORLDS:
        prefix, value = 1, Q(0)
        for index in order:
            value += prices[index] * prefix
            prefix *= world[index]
        result.append(value + penalty * prefix)
    return tuple(result)


def independent_rows(payload, case):
    rows, values = [(Q(1),)*8], [Q(1)]
    if case.facts_live:
        method, data = payload['method'], payload['data']
        if method == 'fresh':
            rows += [tuple(Q(i == j) for j in range(8)) for i in range(8)]
            values += list(map(Q, data['law']))
        elif method == 'full_joint':
            subsets = [s for k in range(1, 4) for s in combinations(range(3), k)]
            rows += [tuple(Q(all(w[i] for i in s)) for w in WORLDS) for s in subsets]
            values += list(map(Q, data['moments']))
        elif method == 'tailored':
            # At the frozen equal old prices the four residuals are simple
            # moment differences; this avoids the implementation's decoder.
            rows += [costs((0, 1, 2), (Q(1),)*3, Q(4))]
            rows += [tuple(Q(w[i]-w[0]) for w in WORLDS) for i in (1, 2)]
            rows += [tuple(Q(w[i]*w[j]-w[0]*w[1]) for w in WORLDS)
                     for i, j in ((0, 2), (1, 2))]
            values += list(map(Q, data['profile']))
        elif method == 'exact_intervals':
            rows += [costs(o, (Q(1),)*3, Q(4)) for o in permutations(range(3))]
            values += list(map(Q, data['means']))
        elif method == 'marginal_diagnostic':
            rows += [tuple(Q(w[i]) for w in WORLDS) for i in range(3)]
            values += list(map(Q, data['marginals']))
        else:
            raise ValueError(method)
    if case.known_marginals:
        rows += [tuple(Q(w[i]) for w in WORLDS) for i in range(3)]
        values += list(case.known_marginals)
    return rows, values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    cfg = R.defaults()
    assert cfg['development_seeds'] == [14101, 14102]
    report = {'schema': 'F14-independent-lp-development-v1',
              'python': platform.python_version(), 'numpy': np.__version__,
              'scipy': scipy.__version__, 'solver': 'HiGHS via scipy.optimize.linprog',
              'development_seeds': cfg['development_seeds'], 'evaluation_generated': False,
              'lp_feasibility_tolerance': 1e-9, 'comparison_tolerance': 1e-8,
              'f15_admission_tolerances_changed': False,
              'fiber_count': 0, 'objectives': 0, 'lp_solves': 0,
              'exact_primal_dual_checks': 0, 'maximum_endpoint_difference': 0.0,
              'maximum_primal_residual': 0.0, 'cases': []}
    start = time.perf_counter()
    for seed in cfg['development_seeds']:
        for variant in cfg['variants']:
            case = R.generate_case(seed, variant, cfg)
            vectors = [costs(o, case.prices, case.penalty) for o in case.orders]
            vectors.append((Q(cfg['fallback_cost']),)*8)
            objectives = vectors + [tuple(a-b for a,b in zip(vectors[i], vectors[j]))
                                    for i,j in combinations(range(7), 2)]
            record = {'seed': seed, 'variant': variant, 'methods': []}
            for method in ('fresh', 'full_joint', 'tailored', 'exact_intervals', 'marginal_diagnostic'):
                payload = R.retain(case.old_law, method, cfg)
                rows, values = independent_rows(payload, case)
                # Check the independent retained equations against the old/current
                # scoring law where still admitted; this law never enters linprog.
                if case.facts_live:
                    assert all(sum(x*p for x,p in zip(row,case.scoring_law)) == b
                               for row,b in zip(rows, values))
                aeq, beq = np.array(rows, dtype=float), np.array(values, dtype=float)
                fiber = R.recover_fiber(payload, cfg, facts_live=case.facts_live,
                                        known_marginals=case.known_marginals)
                for objective in objectives:
                    exact_lo, exact_hi = fiber.bounds(objective)
                    assert fiber.maximum_with_dual(objective)[0] == exact_hi
                    report['exact_primal_dual_checks'] += 1
                    for sign, exact in ((1, exact_lo), (-1, exact_hi)):
                        result = linprog(sign*np.array(objective, dtype=float), A_eq=aeq,
                                         b_eq=beq, bounds=(0, None), method='highs',
                                         options={'primal_feasibility_tolerance': 1e-9,
                                                  'dual_feasibility_tolerance': 1e-9})
                        assert result.success, (seed, variant, method, result.message)
                        error = abs(sign*result.fun-float(exact))
                        residual = float(np.max(np.abs(aeq@result.x-beq)))
                        assert error <= 1e-8 and residual <= 1e-8
                        report['maximum_endpoint_difference'] = max(report['maximum_endpoint_difference'], error)
                        report['maximum_primal_residual'] = max(report['maximum_primal_residual'], residual)
                        report['lp_solves'] += 1
                    report['objectives'] += 1
                report['fiber_count'] += 1
                record['methods'].append({'method': method, 'rank': fiber.rank,
                                          'vertices': len(fiber.vertices),
                                          'independent_constraint_rows': len(rows)})
            report['cases'].append(record)
    report.update(passed=True, wall_seconds=time.perf_counter()-start)
    target = Path(args.out)
    with target.open('x') as handle:
        json.dump(report, handle, indent=2); handle.write('\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
