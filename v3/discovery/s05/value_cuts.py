#!/usr/bin/env python3
"""Checked dual combinations of historical weighted lower bounds.

DEVELOPMENT, ChatGPT (GPT-6 Astra Pro). Existing exposed recipes only;
past cuts only enter each prefix query. No source solver/optimum diagnostic.
"""
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import hashlib
import json
import time
import scipy
from scipy.optimize import linprog


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def combine(cuts, weights):
    started = time.perf_counter_ns()
    result = linprog(weights,
                     A_ub=[[-v for v in cut['weights']] for cut in cuts],
                     b_ub=[-cut['lower'] for cut in cuts],
                     bounds=[(0, 1)] * len(weights), method='highs')
    proposal_ns = time.perf_counter_ns() - started
    if not result.success:
        raise ValueError('No feasible cut relaxation: ' + result.message)
    started = time.perf_counter_ns()
    lam = [max(Fraction(0), Fraction(float(-x)).limit_denominator(10**6))
           for x in result.ineqlin.marginals]
    mu = [max(Fraction(0), sum(t * cut['weights'][j]
                             for t, cut in zip(lam, cuts)) - w)
          for j, w in enumerate(weights)]
    dual = sum(t * cut['lower'] for t, cut in zip(lam, cuts)) - sum(mu)
    # This exact check is the warrant. Numerical LP success is not a proof.
    assert all(t >= 0 for t in lam + mu)
    for j, w in enumerate(weights):
        assert sum(t * cut['weights'][j] for t, cut in zip(lam, cuts)) - mu[j] <= w
    lower = max(0, -(-dual.numerator // dual.denominator))
    return {'integer_lower': lower, 'rational_lower': str(dual),
            'nonnegative_cut_multipliers': list(map(str, lam)),
            'box_multipliers': list(map(str, mu)),
            'numerical_relaxation_value': result.fun,
            'proposal_runtime_ns': proposal_ns,
            'exact_check_runtime_ns': time.perf_counter_ns() - started,
            'cut_count': len(cuts),
            'checker_rational_products': len(cuts) * (2 * len(weights) + 1)}


def main():
    here = Path(__file__).parent
    destination = here / 'value_cuts_results.json'
    if destination.exists():
        raise FileExistsError('Preserve earlier development evidence')
    p = here / 'reprice_compact_results.json'
    data = json.loads(p.read_text())
    if sha(here / 'reprice_compact.py') != data['implementation_sha256']:
        raise ValueError('Changed source implementation')
    old = data['cases'][0]['weights']
    histories = [[{'weights': old, 'lower': row['old_lower'],
                   'receipt': 'original_checked_budget_lower'}]
                 for row in data['compiled_profiles']]
    cases = []
    for case in data['cases']:
        rows = []
        for i, (past, direct, scalar) in enumerate(zip(
                histories, case['rows']['compact_tree'], case['rows']['compact_scalar_ratio'])):
            combined = combine(past, case['weights'])
            assert combined['integer_lower'] <= direct['upper']
            rows.append({'row': i, 'prior_cuts': list(past), 'combined': combined,
                         'current_tree_lower_comparison_only': direct['lower'],
                         'current_scalar_lower_comparison_only': scalar['lower'],
                         'shared_witness_upper_comparison_only': direct['upper']})
            # New numeric receipt enters only after its own query has completed.
            past.append({'weights': case['weights'], 'lower': direct['lower'],
                         'receipt': 'saved_tree_profile:' + case['name']})
        cases.append({'name': case['name'], 'weights': case['weights'], 'rows': rows,
                      'strict_improvement_over_scalar': sum(
                          r['combined']['integer_lower'] > r['current_scalar_lower_comparison_only']
                          for r in rows),
                      'strict_improvement_over_current_tree': sum(
                          r['combined']['integer_lower'] > r['current_tree_lower_comparison_only']
                          for r in rows)})
    illustrative = {'cuts': [{'weights': [1, 0], 'lower': 1},
                             {'weights': [0, 1], 'lower': 1}], 'weights': [1, 1]}
    illustrative['combined'] = combine(illustrative['cuts'], illustrative['weights'])
    assert illustrative['combined']['integer_lower'] == 2
    result = {'status': 'complete', 'evidence': 'DEVELOPMENT',
              'contributor': 'ChatGPT (GPT-6 Astra Pro)',
              'utc': datetime.now(timezone.utc).isoformat(),
              'implementation_sha256': sha(Path(__file__)),
              'input_result_sha256': sha(p), 'source': p.name,
              'scipy_version': scipy.__version__,
              'new_solver_calls': 0, 'new_source_diagnostic_calls': 0,
              'new_empirical_exposure': False,
              'auxiliary_numerical_lp_calls': 81,
              'cases': cases, 'illustrative_complementary_cuts': illustrative,
              'accounting': {'source_bundle_bytes_read': p.stat().st_size,
                             'proposal_runtime_ns': sum(r['combined']['proposal_runtime_ns'] for c in cases for r in c['rows']),
                             'exact_check_runtime_ns': sum(r['combined']['exact_check_runtime_ns'] for c in cases for r in c['rows']),
                             'complete_native_instruction_invoice': False},
              'scope': 'Exact valid lower certificates; no claim of LP optimality, net cost benefit, or native MaxSAT superiority'}
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'cases': [{k: c[k] for k in ('name', 'strict_improvement_over_scalar', 'strict_improvement_over_current_tree')} for c in cases],
                      'accounting': result['accounting']}))


if __name__ == '__main__':
    main()
