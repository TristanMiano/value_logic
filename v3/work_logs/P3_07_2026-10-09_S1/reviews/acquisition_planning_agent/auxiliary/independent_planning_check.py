#!/usr/bin/env python3
"""Bounded, independently authored rational audit; no candidate code is imported.

Backward: unnormalized two-law likelihood messages.
Forward: unmerged ordered-history enumeration under each stipulated law.
Every output is confined to this script's auxiliary directory.
"""

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
import json


ROOT = Path('/workspace/scratch/26a4ba8a7dcb/value_logic')
WORK = ROOT / 'v3/work_logs/P3_07_2026-10-09_S1'
SAVED = WORK / 'development/acquisition_planning_run_v1'
OUT = Path(__file__).resolve().parent
EXPECTED_HASH = '94fb8efcbb924470d883733f3c317fc0a79c4047089104ee4ee1c03ca5141f37'
R = Fraction
CAPS = (1, 12)
HORIZONS = (128, 512, 4096, 16384)
PRICES = (R(0), R(1, 10000), R(1, 1000))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def reconstruct(cap, horizon, price):
    """Return all states using U=(high_weight+low_weight)*value.

    This has no posterior-predictive transition arithmetic in the Bellman
    recurrence. Child unnormalized values sum, then divide by 20.
    """
    table = {}
    marginal_cost = R(1, 2) + 16 * price

    @lru_cache(None)
    def weighted_value(depth, successes, high_weight, low_weight):
        weight = high_weight + low_weight
        weighted_deploy = R(horizon * (high_weight - low_weight), 20)
        best = max(R(0), weighted_deploy)
        action = 'compute' if weighted_deploy > 0 else 'fallback'
        weighted_continue = None
        if depth < cap:
            success_value = weighted_value(depth + 1, successes + 1,
                                           11 * high_weight, 9 * low_weight)
            failure_value = weighted_value(depth + 1, successes,
                                           9 * high_weight, 11 * low_weight)
            weighted_continue = (success_value + failure_value) / 20 - marginal_cost * weight
            if weighted_continue > best:
                best, action = weighted_continue, 'acquire'
        # Posterior fields are derived separately for comparison with evidence.
        table[(depth, successes)] = (
            depth, successes, action, best / weight,
            R(high_weight, weight),
            R(11 * high_weight + 9 * low_weight, 20 * weight),
            weighted_deploy / weight,
            None if weighted_continue is None else weighted_continue / weight,
        )
        return best

    root_value = weighted_value(0, 0, 1, 1) / 2
    assert len(table) == (cap + 1) * (cap + 2) // 2
    return root_value, table


def enumerate_histories(cap, horizon, price, table, success_numerator):
    """Walk every reached binary prefix without merging probabilities by state."""
    frontier = [(0, 0, 1)]
    terminal_mass = R(0)
    deploy_mass = R(0)
    expected_attempts = R(0)
    reachable_states = set()
    terminal_history_count = 0
    terminal_attempt_distribution = {}
    while frontier:
        depth, successes, likelihood_numerator = frontier.pop()
        reachable_states.add((depth, successes))
        mass = R(likelihood_numerator, 20 ** depth)
        action = table[(depth, successes)][2]
        if action == 'acquire':
            assert depth < cap
            expected_attempts += mass
            frontier.append((depth + 1, successes + 1,
                             likelihood_numerator * success_numerator))
            frontier.append((depth + 1, successes,
                             likelihood_numerator * (20 - success_numerator)))
        else:
            assert action in ('compute', 'fallback')
            terminal_mass += mass
            terminal_history_count += 1
            terminal_attempt_distribution[depth] = terminal_attempt_distribution.get(depth, R(0)) + mass
            if action == 'compute':
                deploy_mass += mass
    assert terminal_mass == 1
    assert sum(depth * mass for depth, mass in terminal_attempt_distribution.items()) == expected_attempts
    theta = R(success_numerator, 20)
    control_units = 8 + 16 * expected_attempts
    gain = horizon * (theta - R(1, 2)) * deploy_mass - R(1, 2) * expected_attempts - price * control_units
    return {
        'theta': theta,
        'buy_probability': deploy_mass,
        'expected_profile_attempts': expected_attempts,
        'expected_online_control_units': control_units,
        'gain_excluding_construction': gain,
        'reachable_state_count': len(reachable_states),
        'terminal_mass': terminal_mass,
        'terminal_history_count': terminal_history_count,
        'terminal_attempt_distribution': terminal_attempt_distribution,
    }


def main():
    live_path = ROOT / 'v3/checks/07_acquisition_planning.py'
    saved_path = SAVED / 'sources/07_acquisition_planning.py'
    live_hash, saved_hash = digest(live_path), digest(saved_path)
    assert live_hash == saved_hash == EXPECTED_HASH
    result_path = SAVED / 'result.json'
    evidence = json.loads(result_path.read_text())
    expected_grid = set(product(CAPS, HORIZONS, PRICES))
    saved_by_case = {(r['cap'], r['horizon'], R(r['unit_price'])): r for r in evidence['rows']}
    assert len(evidence['rows']) == len(saved_by_case) == 24
    assert set(saved_by_case) == expected_grid
    assert evidence['plans'] == 24
    assert evidence['source_hashes']['07_acquisition_planning.py'] == EXPECTED_HASH

    mismatches = []
    comparisons = 0
    total_states = 0
    independent_rows = []
    independent_tables = []
    evidence_hashes = {'result.json': digest(result_path)}

    def check(case, field, actual, expected):
        nonlocal comparisons
        comparisons += 1
        if actual != expected:
            mismatches.append({'case': list(case), 'field': field,
                               'independent': actual, 'saved': expected})

    for case in product(CAPS, HORIZONS, PRICES):
        cap, horizon, price = case
        stored = saved_by_case[case]
        value, table = reconstruct(cap, horizon, price)
        plan_name = f'cap{cap}_h{horizon}_price{price.numerator}_{price.denominator}_plan.json'
        plan_path = SAVED / plan_name
        evidence_hashes[plan_name] = digest(plan_path)
        saved_plan = json.loads(plan_path.read_text())
        saved_states = saved_plan['core']['rows']
        check(case, 'state_count', len(table), len(saved_states))
        for index, key in enumerate(sorted(table)):
            actual = table[key]
            stored_state = saved_states[index]
            check(case, f'state_{key}_width', len(actual), len(stored_state))
            for field_index, actual_item in enumerate(actual):
                saved_item = stored_state[field_index]
                if field_index >= 3 and saved_item is not None:
                    saved_item = R(saved_item)
                check(case, f'state_{key}_field_{field_index}', actual_item, saved_item)
        total_states += len(table)
        law_results = [enumerate_histories(cap, horizon, price, table, numerator)
                       for numerator in (9, 11)]
        prior_gain = sum((r['gain_excluding_construction'] for r in law_results), R(0)) / 2
        assert prior_gain == value - 8 * price
        prior_attempts = sum((r['expected_profile_attempts'] for r in law_results), R(0)) / 2
        # Use the recorded construction-unit count only to verify stated result
        # arithmetic. Independent derivation of the tariff belongs to the parent.
        construction_units = stored['construction_units']
        construction_cost = price * construction_units
        all_in_gain = prior_gain - construction_cost
        computed = {
            'cap': cap, 'horizon': horizon, 'unit_price': price,
            'root_action': table[(0, 0)][2],
            'bellman_value_after_initial_lookup': value,
            'prior_gain_excluding_construction': prior_gain,
            'construction_units_from_saved_record': construction_units,
            'construction_cost': construction_cost,
            'all_in_prior_gain': all_in_gain,
            'expected_profile_attempts_prior': prior_attempts,
            'conditional_laws': law_results,
            'table_state_count': len(table),
        }
        for field in ('root_action', 'bellman_value_after_initial_lookup',
                      'prior_gain_excluding_construction', 'construction_cost', 'all_in_prior_gain'):
            stored_item = stored[field] if field == 'root_action' else R(stored[field])
            check(case, field, computed[field], stored_item)
        check(case, 'conditional_law_count', len(law_results), len(stored['conditional_laws']))
        for law_index, independent in enumerate(law_results):
            saved_law = stored['conditional_laws'][law_index]
            for field in ('theta', 'buy_probability', 'expected_profile_attempts',
                          'expected_online_control_units', 'gain_excluding_construction', 'reachable_state_count'):
                saved_item = saved_law[field] if field == 'reachable_state_count' else R(saved_law[field])
                check(case, f'law_{law_index}_{field}', independent[field], saved_item)
        independent_rows.append(computed)
        independent_tables.append({'cap': cap, 'horizon': horizon, 'unit_price': price,
                                   'rows': [table[k] for k in sorted(table)]})

    report = {
        'status': 'PASS' if not mismatches else 'FAIL',
        'scope': 'Frozen acquisition-planning v1 mathematical subreview only',
        'independence': 'Same model; nonblind candidate prompt; generic reconstruction preceded source inspection; independently authored code without importing candidate source.',
        'time_status': 'Unmeasured auxiliary work; zero principal credit.',
        'frozen_source_sha256': EXPECTED_HASH,
        'live_source_sha256': live_hash,
        'saved_source_sha256': saved_hash,
        'saved_evidence_sha256': evidence_hashes,
        'independent_script_sha256': digest(Path(__file__).resolve()),
        'checked_rows': len(independent_rows),
        'checked_table_states': total_states,
        'exact_comparisons': comparisons,
        'mismatch_count': len(mismatches),
        'mismatches': mismatches,
        'accounting_scope': 'Construction costs and all-in values checked arithmetically using saved construction units; tariff derivation, adapter/core integrity, and CPU-cost adequacy left to parent review.',
        'rows': independent_rows,
    }
    (OUT / 'independent_results.json').write_text(json.dumps(report, indent=2, default=str) + '\n')
    (OUT / 'independent_tables.json').write_text(json.dumps(independent_tables, indent=2, default=str) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'checked_rows', 'checked_table_states',
                                           'exact_comparisons', 'mismatch_count')}, indent=2))
    for row in independent_rows:
        print(f"N={row['cap']:2d} H={row['horizon']:5d} price={str(row['unit_price']):7s} "
              f"action={row['root_action']:8s} E[T]={float(row['expected_profile_attempts_prior']):.8f} "
              f"prior={float(row['prior_gain_excluding_construction']):.9f} "
              f"all_in={float(row['all_in_prior_gain']):.9f}")
    if mismatches:
        raise AssertionError(f'{len(mismatches)} exact comparisons failed.')


if __name__ == '__main__':
    main()
