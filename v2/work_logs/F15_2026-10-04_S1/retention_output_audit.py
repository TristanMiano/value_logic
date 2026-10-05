#!/usr/bin/env python3
"""Independent exact audit of completed F15 retention JSON outputs.

Contributor: delegated ChatGPT (GPT-6 Astra Pro), F15 saved-output audit.
This script uses only the standard library and saved JSON. It imports no
project module, invokes no generator, and never prepares or evaluates a model.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import prod
from pathlib import Path
import platform
import shlex
import sys
from time import perf_counter, process_time


WORLDS = tuple(product((0, 1), repeat=3))
FULL_ORDERS = tuple(permutations(range(3)))
MARGINAL_ROWS = tuple(tuple(Q(w[i]) for w in WORLDS) for i in range(3))
STABLE_PRICE_VARIANTS = (
    'small_price', 'small_negative_price', 'large_price', 'large_negative_price')
SIGNATURE = 'delegated ChatGPT (GPT-6 Astra Pro), F15 saved-output audit'


def encode(value):
    if isinstance(value, Q):
        return str(value)
    raise TypeError(type(value).__name__)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), Q(0))


def prefix_vector(order, prices, penalty):
    """Closed prefix-product cost formula, independent of path execution code."""
    return tuple(sum((prices[i]*prod(w[j] for j in order[:t])
                      for t, i in enumerate(order)), Q(0))
                 + penalty*prod(w[j] for j in order) for w in WORLDS)


def solve_unique(rows, rhs, dimension):
    """Exact forward elimination/back substitution on rectangular equations.

    Returns (solution or None, rank, consistency). This deliberately does not
    use the experiment's inverse matrices, RREF, or native dual production.
    """
    work = [list(map(Q, row)) + [Q(b)] for row, b in zip(rows, rhs)]
    pivots = []
    for column in range(dimension):
        candidate = next((i for i in range(len(pivots), len(work))
                          if work[i][column]), None)
        if candidate is None:
            continue
        current = len(pivots)
        work[current], work[candidate] = work[candidate], work[current]
        for i in range(current+1, len(work)):
            if work[i][column]:
                ratio = work[i][column]/work[current][column]
                for j in range(column, dimension+1):
                    work[i][j] -= ratio*work[current][j]
        pivots.append(column)
    consistent = all(any(row[:dimension]) or not row[dimension] for row in work)
    if not consistent or len(pivots) != dimension:
        return None, len(pivots), consistent
    answer = [Q(0)]*dimension
    for i in range(dimension-1, -1, -1):
        column = pivots[i]
        answer[column] = (work[i][-1] - sum(
            (work[i][j]*answer[j] for j in range(column+1, dimension)), Q(0)
        )) / work[i][column]
    return tuple(answer), len(pivots), True


@lru_cache(maxsize=None)
def feasible_vertices(rows, rhs):
    """Enumerate nonnegative supports using all original equalities."""
    _, rank, consistent = solve_unique(rows, rhs, 8)
    if not consistent:
        raise ValueError('inconsistent saved-data reconstruction equations')
    vertices = set()
    for support in combinations(range(8), rank):
        coefficients = tuple(tuple(row[i] for i in support) for row in rows)
        solution, _, consistent = solve_unique(coefficients, rhs, rank)
        if solution is None or not consistent or min(solution) < 0:
            continue
        vector = [Q(0)]*8
        for i, p in zip(support, solution):
            vector[i] = p
        vertex = tuple(vector)
        if all(dot(row, vertex) == b for row, b in zip(rows, rhs)):
            vertices.add(vertex)
    if not vertices:
        raise ValueError('empty reconstructed information fiber')
    return tuple(sorted(vertices)), rank


def point_prediction(means, orders, fallback, tau, epsilon):
    return cost_table_prediction((tuple(means)+(fallback,),), orders, tau, epsilon)


def cost_table_prediction(costs, orders, tau, epsilon):
    # Each row is one coherent law's costs. Compute regret against that same
    # row's best action before taking any maximum over laws.
    n = len(orders)+1
    lower = tuple(min(row[i] for row in costs) for i in range(n))
    upper = tuple(max(row[i] for row in costs) for i in range(n))
    regrets = tuple(max(row[i]-min(row) for row in costs) for i in range(n))
    selected = min(range(n), key=lambda i: (regrets[i], upper[i], i))
    refused = regrets[selected] > epsilon
    executed = n-1 if refused else selected
    candidate = selected if not refused and selected < n-1 else 0
    status = tuple('exact' if lo == hi else
                   'approximate' if hi-lo <= 2*tau else 'refused'
                   for lo, hi in zip(lower[:-1], upper[:-1]))
    estimates = tuple(None if s == 'refused' else (lo+hi)/2
                      for s, lo, hi in zip(status, lower, upper))
    return dict(lower=lower, upper=upper, status=status, estimates=estimates,
                regrets=regrets, selected=selected, refused=refused,
                executed=executed, candidate=candidate)


class Audit:
    def __init__(self):
        self.checks = Counter()
        self.failures = []
        self.hashes = {}

    def check(self, category, where, actual, expected):
        self.checks[category] += 1
        if actual != expected:
            self.failures.append(dict(category=category, location=where,
                                      actual=actual, expected=expected))

    def read(self, path, sidecar=False):
        raw = path.read_bytes()
        digest = sha256(raw).hexdigest()
        self.hashes[str(path)] = digest
        if sidecar:
            self.check('artifact_hash', str(path), digest,
                       Path(str(path)+'.sha256').read_text().strip())
        return json.loads(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path,
                        default=Path(__file__).resolve().parents[3])
    parser.add_argument('--run', type=Path,
                        default=Path('v2/work_logs/F15_v1_run1'))
    parser.add_argument('--out', type=Path,
                        default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    started_utc = datetime.now(timezone.utc).isoformat()
    started_wall, started_cpu = perf_counter(), process_time()
    root = args.repo.resolve()
    run = args.run if args.run.is_absolute() else root/args.run
    if not (run/'evaluation_complete.json').is_file():
        raise SystemExit('Completed evaluation marker required; no evaluation data read.')
    audit = Audit()
    config = audit.read(root/'v2/experiments/config.v1.json')
    audit.read(root/'v2/experiments/freeze.v1.json')
    complete = audit.read(run/'evaluation_complete.json', sidecar=True)
    audit.check('completion', 'evaluation.status', complete['status'], 'evaluation_complete')
    folder = (run/complete['retention_assessment_file']).parent
    rc = config['retention']
    expected_keys = [(s, v) for s in rc['evaluation_seeds'] for v in rc['variants']]
    unit_paths = {Path(p).name: run/p for p in
                  complete['generated_units']+complete['reused_units']
                  if Path(p).name.startswith('retention_')}
    cases = []
    for seed, variant in expected_keys:
        filename = f'retention_{seed}_{variant}.json'
        case = audit.read(unit_paths[filename], sidecar=True)
        audit.check('case_inventory', filename, (case['seed'], case['variant']), (seed, variant))
        cases.append(case)
    # A post-completion zero-byte aggregate was independently observed. Read
    # the intact original case units instead; never rewrite the original.
    aggregate = folder/'retention_results.json'
    aggregate_raw = aggregate.read_bytes()
    aggregate_digest = sha256(aggregate_raw).hexdigest()
    aggregate_sidecar = Path(str(aggregate)+'.sha256').read_text().strip()
    audit.hashes[str(aggregate)] = aggregate_digest
    rebuilt_digest = sha256((json.dumps(cases, sort_keys=True, indent=2,
                                       allow_nan=False)+'\n').encode('utf-8')).hexdigest()
    audit.check('canonical_reassembly', str(aggregate), rebuilt_digest, aggregate_sidecar)
    aggregate_provenance = dict(
        original_bytes=len(aggregate_raw), observed_sha256=aggregate_digest,
        original_sidecar_sha256=aggregate_sidecar, canonical_reassembly_sha256=rebuilt_digest,
        original_aggregate_hash_valid=aggregate_digest == aggregate_sidecar,
        input_policy='read original individually hash-checked case units in frozen order',
        original_preserved=True, scientific_rerun=False)
    index = {(c['seed'], c['variant']): c for c in cases}
    fallback = Q(rc['fallback_cost'])
    tau = Q(rc['numeric_tolerance'])
    epsilon = Q(rc['decision_regret_tolerance'])
    old_prices = tuple(map(Q, rc['old_prices']))
    old_penalty = Q(rc['old_penalty'])
    old_vectors = tuple(prefix_vector(o, old_prices, old_penalty) for o in FULL_ORDERS)
    normalize = (Q(1),)*8

    def reference(case):
        return next(row for row in case['methods'] if row['method'] == 'fresh'
                    and row['access'] == 'adaptive_reacquisition')

    def saved_means(case):
        base = reference(case)
        for i, row in enumerate(base['numeric']):
            where = f"{case['seed']}/{case['variant']}/fresh-reference/{i}"
            audit.check('reference_point', where+'/status', row['status'], 'exact')
            audit.check('reference_point', where+'/point', row['lower'], row['upper'])
            audit.check('reference_point', where+'/estimate', row['estimate'], row['lower'])
        return tuple(Q(row['estimate']) for row in base['numeric'])

    # Use six old means and exactly two prescribed current means (orders
    # 0,2,1 and 0,1,2 under the large edit). No seed-to-law generator is used.
    reconstructed = {}
    laws = {}
    old_means_by_seed = {}
    for seed in rc['evaluation_seeds']:
        old_means = saved_means(index[seed, 'unchanged'])
        large_means = saved_means(index[seed, 'large_price'])
        prices = list(old_prices)
        prices[2] += Q(rc['large_price_change'])
        large_vectors = tuple(prefix_vector(o, prices, old_penalty) for o in FULL_ORDERS)
        probe_indices = (1, 0)
        rows = (normalize,)+old_vectors+tuple(large_vectors[i] for i in probe_indices)
        rhs = (Q(1),)+old_means+tuple(large_means[i] for i in probe_indices)
        law, rank, consistent = solve_unique(rows, rhs, 8)
        audit.check('law_reconstruction', f'{seed}/rank', rank, 8)
        audit.check('law_reconstruction', f'{seed}/consistency', consistent, True)
        if law is None:
            raise ValueError(f'unique saved-data reconstruction failed for seed {seed}')
        audit.check('law_reconstruction', f'{seed}/normalization', sum(law), Q(1))
        audit.check('law_reconstruction', f'{seed}/nonnegative', min(law) >= 0, True)
        audit.check('law_reconstruction', f'{seed}/all_large_means',
                    tuple(dot(v, law) for v in large_vectors), large_means)
        laws[seed], old_means_by_seed[seed] = law, old_means
        reconstructed[str(seed)] = dict(law=law, rank=rank,
            measurements='six saved old means plus two saved large-price means and normalization',
            current_probe_orders=[FULL_ORDERS[i] for i in probe_indices],
            other_four_large_price_means_verified=True)

    counts = Counter()
    by_variant = defaultdict(Counter)
    scopes = Counter()
    max_admitted_error = Q(0)
    max_realized_regret = Q(0)
    for case in cases:
        seed, variant = case['seed'], case['variant']
        current_means = saved_means(case)
        prices, penalty, orders = list(old_prices), old_penalty, FULL_ORDERS
        if variant in STABLE_PRICE_VARIANTS:
            prices[2] += Q(rc[variant+'_change'])
        elif variant == 'proportional':
            scale = Q(rc['proportional_scale'])
            prices, penalty = [p*scale for p in prices], penalty*scale
        elif variant == 'program_edit':
            orders = tuple(permutations(range(3), 2))
        vectors = tuple(prefix_vector(o, prices, penalty) for o in orders)
        vectors += ((fallback,)*8,)
        authority = variant not in ('withdrawal', 'source_drift')
        audit.check('source_authority', f'{seed}/{variant}', case['facts_live'], authority)
        if variant != 'source_drift':
            audit.check('independent_prefix_cost', f'{seed}/{variant}', current_means,
                        tuple(dot(v, laws[seed]) for v in vectors[:-1]))
            counts['stable_or_unchanged_law_profiles_independently_rebuilt'] += 1
        else:
            counts['drift_profiles_checked_without_reconstructing_drift_law'] += 1
        expected_inventory = [(a, m) for a in rc['access_regimes'] for m in rc['methods']]
        audit.check('method_inventory', f'{seed}/{variant}',
                    [(r['access'], r['method']) for r in case['methods']], expected_inventory)
        predictions = {}
        ranks = {}
        vertex_counts = {}
        for method in rc['methods']:
            if not authority:
                rows, rhs = (normalize,), (Q(1),)
                scope = 'whole_simplex_after_authority_loss'
            elif method in ('fresh', 'cached_proof', 'full_joint'):
                rows = tuple(tuple(Q(i == j) for i in range(8)) for j in range(8))
                rhs = laws[seed]
                scope = 'stable_full_source_reconstructed_point'
            else:
                if method in ('tailored', 'exact_intervals'):
                    rows, rhs = (normalize,)+old_vectors, (Q(1),)+old_means_by_seed[seed]
                    scope = 'old_six_mean_fiber'
                elif method == 'marginal_diagnostic':
                    rows = (normalize,)+MARGINAL_ROWS
                    rhs = (Q(1),)+tuple(dot(v, laws[seed]) for v in MARGINAL_ROWS)
                    scope = 'marginal_fiber'
                else:
                    raise ValueError(f'unknown frozen method {method}')
                if variant == 'known_marginals':
                    rows += MARGINAL_ROWS
                    rhs += tuple(dot(v, laws[seed]) for v in MARGINAL_ROWS)
                    scope += '_with_current_marginals'
            vertices, rank = feasible_vertices(rows, rhs)
            cost_rows = tuple(tuple(dot(v, law) for v in vectors) for law in vertices)
            predictions[method] = cost_table_prediction(cost_rows, orders, tau, epsilon)
            ranks[method], vertex_counts[method] = rank, len(vertices)
            scopes[scope] += 1

        for row in case['methods']:
            method, access = row['method'], row['access']
            where = f'{seed}/{variant}/{access}/{method}'
            pre = predictions[method]
            pre_refusals = sum(s == 'refused' for s in pre['status'])
            audit.check('pre_repair', where, row['pre_repair'],
                        dict(numeric_refusals=pre_refusals, decision_refused=pre['refused']))
            repaired = access == 'adaptive_reacquisition' and (pre_refusals or pre['refused'])
            selective_repair = repaired and authority and method in ('tailored', 'exact_intervals') \
                and variant in STABLE_PRICE_VARIANTS
            scalars = 2 if selective_repair else 8 if repaired else 0
            expected = point_prediction(current_means, orders, fallback, tau, epsilon) if repaired else pre
            r = row['resources']
            for name, value in {
                'acquisition_scalar_measurements': scalars,
                'acquisition_calls': 2 if selective_repair else 1 if repaired else 0,
                'acquisition_path_world_executions': 16 if selective_repair else 0,
                'acquisition_kinds': ['two_current_order_means'] if selective_repair else
                    ['full_eight_world_law'] if repaired else [],
                'fiber_equation_rank': 8 if repaired else ranks[method],
                'fiber_vertex_count': 1 if repaired else vertex_counts[method],
                'initial_common_scalar_inputs': 8,
                'current_common_scalar_inputs': 3 if variant == 'known_marginals' else 0,
            }.items():
                audit.check('repair_and_fiber', where+'/'+name, r[name], value)
            counts['method_rows'] += 1
            counts['repaired_rows'] += bool(repaired)
            counts['selectively_repaired_rows'] += bool(selective_repair)
            for i, numeric in enumerate(row['numeric']):
                for name, value in {
                    'order': list(orders[i]), 'lower': expected['lower'][i],
                    'upper': expected['upper'][i], 'status': expected['status'][i],
                    'estimate': expected['estimates'][i],
                }.items():
                    actual = numeric[name]
                    if name in ('lower', 'upper', 'estimate') and actual is not None:
                        actual = Q(actual)
                    audit.check('exact_numeric_reconstruction', f'{where}/{i}/{name}', actual, value)
                lo, hi = Q(numeric['lower']), Q(numeric['upper'])
                audit.check('scalar_contains_fresh_reference', f'{where}/{i}',
                            lo <= current_means[i] <= hi, True)
                estimate = None if numeric['estimate'] is None else Q(numeric['estimate'])
                error = None if estimate is None else abs(estimate-current_means[i])
                saved_error = row['scoring']['numeric_errors'][i]
                audit.check('admitted_numeric_error', f'{where}/{i}/recorded',
                            None if saved_error is None else Q(saved_error), error)
                if error is not None:
                    audit.check('admitted_numeric_error', f'{where}/{i}/tolerance', error <= tau, True)
                    max_admitted_error = max(max_admitted_error, error)
                counts['scalar_intervals'] += 1
                counts['numeric_'+numeric['status']] += 1
                by_variant[variant]['numeric_'+numeric['status']] += 1
            choices = tuple(orders)+(None,)
            e = expected
            decision_status = 'refusal_to_fallback' if e['refused'] else \
                'certified_fallback' if e['selected'] == len(orders) else 'certified_order'
            candidate_order = list(orders[e['candidate']])
            role = 'selected_order' if not e['refused'] and e['selected'] < len(orders) \
                else 'diagnostic_option_only'
            for name, value in {
                'selected_index': e['selected'], 'executed_index': e['executed'],
                'selected': None if choices[e['selected']] is None else list(choices[e['selected']]),
                'executed': None if choices[e['executed']] is None else list(choices[e['executed']]),
                'refused': e['refused'], 'useful_decision': not e['refused'],
                'decision_status': decision_status,
                'native_candidate_order': candidate_order, 'native_certificate_role': role,
            }.items():
                audit.check('same_law_decision', where+'/'+name, row[name], value)
            audit.check('same_law_decision', where+'/coherent_worst_regret',
                        Q(row['coherent_worst_regret']), e['regrets'][e['selected']])
            counts['decision_'+decision_status] += 1
            by_variant[variant]['decision_'+decision_status] += 1
            actual_costs = current_means+(fallback,)
            actual_executed = actual_costs[e['executed']]
            realized = actual_executed-min(actual_costs)
            max_realized_regret = max(max_realized_regret, realized)
            n = row['native']
            native_bound = e['upper'][e['candidate']]-fallback
            native_actual = current_means[e['candidate']]-fallback
            for name, value in {
                'actual_executed_cost': actual_executed,
                'full_information_oracle_best_cost': min(actual_costs),
                'realized_regret': realized,
                'full_source_semantic_value': native_actual,
            }.items():
                audit.check('realized_scoring', where+'/'+name, Q(row['scoring'][name]), value)
            audit.check('realized_scoring', where+'/full_source_semantic_valid',
                        row['scoring']['full_source_semantic_valid'], native_actual <= 0)
            if not e['refused']:
                audit.check('realized_scoring', where+'/decision_tolerance', realized <= epsilon, True)
            for name, value in {'upper_bound': native_bound, 'semantic_valid': native_bound <= 0,
                                'candidate_order': candidate_order, 'certificate_role': role,
                                'comparison': 'candidate_expected_cost_minus_fallback',
                                'requested_budget': Q(0)}.items():
                actual = Q(n[name]) if name in ('upper_bound', 'requested_budget') else n[name]
                audit.check('native_numeric_target', where+'/'+name, actual, value)
            if n['status'] != 'unavailable_budget':
                audit.check('native_numeric_target', where+'/receipt_disposition', n['status'],
                            'received' if native_bound <= 0 else 'insufficient_current_request')
            useful = variant in STABLE_PRICE_VARIANTS+('program_edit',) and role == 'selected_order' \
                and n['status'] == 'received' and native_bound <= -tau and n['source_premises_used'] >= 2
            audit.check('native_numeric_target', where+'/useful_derivation_candidate',
                        n['useful_derivation_candidate'], useful)
            for sensitivity in row['acquisition_sensitivity']:
                charge = Q(sensitivity['per_scalar_measurement_cost'])
                shared = 3 if variant == 'known_marginals' else 0
                for name, value in {
                    'initial_common_source_loss': 8*charge,
                    'current_common_source_loss': shared*charge,
                    'method_specific_acquisition_loss': scalars*charge,
                    'decision_plus_acquisition_loss': actual_executed+(shared+scalars)*charge,
                }.items():
                    audit.check('source_price_arithmetic', where+'/'+str(charge)+'/'+name,
                                Q(sensitivity[name]), value)
                for horizon in rc['horizons']:
                    expected_cost = 8*charge+horizon*(actual_executed+(shared+scalars)*charge)
                    audit.check('source_price_arithmetic', where+'/'+str(charge)+f'/h{horizon}',
                        Q(sensitivity['horizon_decision_plus_source_loss'][str(horizon)]), expected_cost)

    script = Path(__file__).resolve()
    audit.hashes[str(script)] = sha256(script.read_bytes()).hexdigest()
    result = {
        'schema': 'f15-retention-saved-output-audit-v1', 'contributor': SIGNATURE,
        'started_utc': started_utc, 'completed_utc': datetime.now(timezone.utc).isoformat(),
        'command': shlex.join([sys.executable, *sys.argv]),
        'python': sys.version, 'platform': platform.platform(),
        'seconds': {'wall': perf_counter()-started_wall, 'process': process_time()-started_cpu},
        'passed': not audit.failures, 'checks_by_category': dict(audit.checks),
        'total_checks': sum(audit.checks.values()), 'failure_count': len(audit.failures),
        'failures': audit.failures, 'counts': dict(counts),
        'aggregate_provenance': aggregate_provenance,
        'by_variant': {k: dict(v) for k, v in by_variant.items()},
        'reconstructed_fiber_scopes': dict(scopes),
        'max_admitted_absolute_error': max_admitted_error,
        'max_realized_regret_including_refusals': max_realized_regret,
        'stable_law_reconstructions': reconstructed,
        'input_and_script_sha256': audit.hashes,
        'scope_limits': [
            'Post-exposure independent numerical consistency audit; no new evaluation population.',
            'No experiment module imported, no sampling, no training, no frozen file edited.',
            'Stable source laws reconstructed from saved action means, never from generator seeds.',
            'Exact fibers rebuilt from the protocol-declared measurements; payload isolation is not retested.',
            'Source-drift law is not identifiable from its six saved point means and was not inferred.',
            'Drift simplex bounds and repaired point-query regret are exactly checkable without that law.',
            'Native numerical targets and recorded receipt dispositions checked; proof objects are not in these outputs.',
            'This audit does not establish novelty, new theorems, causal neural use, or Gates C/D.',
            'Delegated effort overlaps the principal session and is not additive engaged project time.',
        ],
    }
    with args.out.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2, sort_keys=True, default=encode)
        handle.write('\n')
    print(json.dumps({k: result[k] for k in ('passed', 'total_checks', 'failure_count', 'counts', 'seconds')},
                     indent=2, default=encode))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
