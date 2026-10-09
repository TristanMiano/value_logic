#!/usr/bin/env python3
"""Narrow frozen-v1.1 evidence audit: no candidate import, execution, or DP.

Checks canonical core hashes, source-byte/stat-derived resource bills, and
literal saved mathematical-result equality against the frozen v1 evidence.
All output is written beside this script; previous review artifacts are read-only.
"""
import ast
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

ROOT = Path('/workspace/scratch/26a4ba8a7dcb/value_logic')
WORK = ROOT / 'v3/work_logs/P3_07_2026-10-09_S1'
OLD = WORK / 'development/acquisition_planning_run_v1'
NEW = WORK / 'development/acquisition_planning_run_v1_1'
OUT = Path(__file__).resolve().parent
EXPECTED_NEW = '88c73b82ac2809da8f31a8dcb93237e732f93b73665a42f5ec180d6355c782b7'
EXPECTED_OLD = '94fb8efcbb924470d883733f3c317fc0a79c4047089104ee4ee1c03ca5141f37'
SOURCE_NAMES = ('07_computation_adapter.py', '07_acquisition_planning.py')
CAPS, HORIZONS, PRICES = (1, 12), (128, 512, 4096, 16384), (Fraction(0), Fraction(1, 10000), Fraction(1, 1000))


def read_json(path):
    return json.loads(path.read_text())


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical(value):
    # Saved JSON already contains the exact canonical fraction strings.
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def main():
    failures = []
    comparisons = 0

    def check(label, actual, expected):
        nonlocal comparisons
        comparisons += 1
        if actual != expected:
            failures.append({'check': label, 'actual': actual, 'expected': expected})

    old_result = read_json(OLD / 'result.json')
    new_result = read_json(NEW / 'result.json')
    old_source_bytes = {name: (OLD / 'sources' / name).stat().st_size for name in SOURCE_NAMES}
    new_source_bytes = {name: (NEW / 'sources' / name).stat().st_size for name in SOURCE_NAMES}
    old_hashes = {name: file_hash(OLD / 'sources' / name) for name in SOURCE_NAMES}
    new_hashes = {name: file_hash(NEW / 'sources' / name) for name in SOURCE_NAMES}
    check('new saved source hash', new_hashes[SOURCE_NAMES[1]], EXPECTED_NEW)
    check('new live source hash', file_hash(ROOT / 'v3/checks' / SOURCE_NAMES[1]), EXPECTED_NEW)
    check('old saved source hash', old_hashes[SOURCE_NAMES[1]], EXPECTED_OLD)
    check('unchanged adapter bytes', new_hashes[SOURCE_NAMES[0]], old_hashes[SOURCE_NAMES[0]])
    check('new result source hashes', new_result['source_hashes'], new_hashes)
    check('old result source hashes', old_result['source_hashes'], old_hashes)
    check('new version', new_result['version'], 'p307-bounded-two-law-acquisition-planner-v1.1')

    # Read only the category-order literal from the frozen adapter syntax tree.
    adapter_ast = ast.parse((NEW / 'sources' / SOURCE_NAMES[0]).read_text())
    category_assignments = [node for node in adapter_ast.body if isinstance(node, ast.Assign)
                            and any(isinstance(target, ast.Name) and target.id == 'CATEGORIES'
                                    for target in node.targets)]
    assert len(category_assignments) == 1
    categories = ast.literal_eval(category_assignments[0].value)

    old_source_units = 2 * sum((size + 7) // 8 for size in old_source_bytes.values())
    new_source_units = 2 * sum((size + 7) // 8 for size in new_source_bytes.values())
    new_stat_units = len(SOURCE_NAMES)
    derived_delta = new_source_units + new_stat_units - old_source_units
    check('derived delta matches disclosed candidate', derived_delta, 120)
    check('new source hash-read units', new_source_units, 8080)
    check('old source hash-read units', old_source_units, 7962)

    def case_map(result):
        return {(r['cap'], r['horizon'], Fraction(r['unit_price'])): r for r in result['rows']}

    old_cases, new_cases = case_map(old_result), case_map(new_result)
    grid = set(product(CAPS, HORIZONS, PRICES))
    check('new grid', set(new_cases), grid)
    check('old grid', set(old_cases), grid)
    check('new row count', len(new_result['rows']), 24)
    check('old row count', len(old_result['rows']), 24)
    check('new saved plan count', len(list(NEW.glob('*_plan.json'))), 24)
    check('new reported plan count', new_result['plans'], 24)

    rows = []
    checked_states = 0
    identities = set()
    derived_total = 0
    for cap, horizon, price in product(CAPS, HORIZONS, PRICES):
        key = (cap, horizon, price)
        label = f'N={cap};H={horizon};price={price}'
        old_row, new_row = old_cases[key], new_cases[key]
        name = f'cap{cap}_h{horizon}_price{price.numerator}_{price.denominator}_plan.json'
        old_plan, new_plan = read_json(OLD / name), read_json(NEW / name)
        old_core, new_core = old_plan['core'], new_plan['core']
        encoded_core = canonical(new_core)
        derived_identity = sha256(encoded_core).hexdigest()
        identities.add(derived_identity)
        check(label + ' identity inside plan', derived_identity, new_plan['identity'])
        check(label + ' identity in result', derived_identity, new_row['plan_id'])
        check(label + ' canonical envelope bytes', (NEW / name).read_bytes(), canonical(new_plan) + b'\n')
        check(label + ' core bytes', len(encoded_core), new_row['core_bytes'])
        check(label + ' core version', new_core['version'], new_result['version'])
        check(label + ' core source hashes', new_core['source_hashes'], [[name, new_hashes[name]] for name in SOURCE_NAMES])

        count = (cap + 1) * (cap + 2) // 2
        words = 1024 + 64 * count
        expected_operations = {
            'admission.fixed_planner_model_admission': 96,
            'assessment.bounded_bellman_state_bundle': 128 * count,
            'profile.bounded_planner_freeze_validate_hash': 2 * words,
            'profile.bounded_registry_file_stat': new_stat_units,
            'profile.planner_source_read_hash_words': new_source_units,
            'storage.bounded_planner_core_retention': words,
            'storage.bounded_state_child_read_and_retention': 64 * count,
        }
        expected_categories = {category: 0 for category in categories}
        for operation, units in expected_operations.items():
            expected_categories[operation.split('.')[0]] += units
        units = sum(expected_operations.values())
        derived_total += units
        check(label + ' expected candidate total', units, {1: 12402, 12: 46194}[cap])
        check(label + ' operation bill', new_row['meter']['operations'], expected_operations)
        check(label + ' category bill', new_row['meter']['by_category'], expected_categories)
        check(label + ' core construction vector', new_core['construction_resources'],
              [expected_categories[category] for category in categories])
        check(label + ' construction units', new_row['construction_units'], units)
        check(label + ' meter total', new_row['meter']['total'], units)
        check(label + ' meter remaining', new_row['meter']['remaining'], new_row['meter']['limit_total'] - units)
        check(label + ' construction delta', new_row['construction_units'] - old_row['construction_units'], derived_delta)
        check(label + ' word envelope', new_core['word_envelope'], words)
        check(label + ' core fits envelope', len(encoded_core) <= 8 * words, True)

        # Evidence-to-evidence equality only: no theorem or DP is recomputed.
        changed_core_fields = {'version', 'source_hashes', 'construction_resources'}
        check(label + ' unchanged core model and table',
              {k: v for k, v in new_core.items() if k not in changed_core_fields},
              {k: v for k, v in old_core.items() if k not in changed_core_fields})
        check(label + ' state count', len(new_core['rows']), count)
        check(label + ' old/new state count', len(new_core['rows']), len(old_core['rows']))
        checked_states += count
        for index, (new_state, old_state) in enumerate(zip(new_core['rows'], old_core['rows'])):
            for column, (new_value, old_value) in enumerate(zip(new_state, old_state)):
                check(label + f' saved state {index} column {column}', new_value, old_value)
        for field in ('cap', 'horizon', 'unit_price', 'root_action', 'bellman_value_after_initial_lookup',
                      'prior_gain_excluding_construction', 'conditional_laws'):
            check(label + ' unchanged ' + field, new_row[field], old_row[field])

        expected_cost = price * units
        expected_all_in = Fraction(new_row['prior_gain_excluding_construction']) - expected_cost
        cost_delta = Fraction(new_row['construction_cost']) - Fraction(old_row['construction_cost'])
        all_in_delta = Fraction(new_row['all_in_prior_gain']) - Fraction(old_row['all_in_prior_gain'])
        check(label + ' construction cost', Fraction(new_row['construction_cost']), expected_cost)
        check(label + ' all-in gain', Fraction(new_row['all_in_prior_gain']), expected_all_in)
        check(label + ' cost delta', cost_delta, derived_delta * price)
        check(label + ' all-in delta', all_in_delta, -derived_delta * price)
        rows.append({'cap': cap, 'horizon': horizon, 'unit_price': price,
                     'canonical_core_identity': derived_identity,
                     'canonical_core_bytes': len(encoded_core), 'construction_units': units,
                     'construction_unit_delta': derived_delta,
                     'construction_cost': expected_cost, 'all_in_prior_gain': expected_all_in,
                     'all_in_prior_gain_delta': all_in_delta,
                     'saved_v1_plan_sha256': file_hash(OLD / name),
                     'saved_v1_1_plan_sha256': file_hash(NEW / name)})

    check('distinct canonical identities', len(identities), 24)
    check('total construction units', new_result['total_24_plan_construction_units'], derived_total)
    check('total delta', derived_total - old_result['total_24_plan_construction_units'], 24 * derived_delta)
    report = {
        'status': 'PASS' if not failures else 'FAIL',
        'scope': 'Frozen v1.1 canonical identities and construction tariff; saved mathematical values compared with v1; no DP recomputation or candidate execution.',
        'independence': 'Same-model, nonblind follow-up; source hash and expected unit/cost changes disclosed by assignment.',
        'time_status': 'Unmeasured auxiliary work; zero principal credit.',
        'excluded_scope': 'Preflight ordering, denial and oversized-price behavior, DP theorem, optional stopping, CPU or human cost adequacy.',
        'source_sha256': new_hashes, 'old_source_sha256': old_hashes,
        'source_bytes': new_source_bytes, 'old_source_bytes': old_source_bytes,
        'source_read_hash_units': new_source_units, 'old_source_read_hash_units': old_source_units,
        'new_file_stat_units': new_stat_units, 'derived_per_plan_unit_delta': derived_delta,
        'canonical_identities_verified': len(identities), 'saved_table_states_compared': checked_states,
        'exact_comparisons': comparisons, 'mismatch_count': len(failures), 'mismatches': failures,
        'total_construction_units': derived_total,
        'new_result_sha256': file_hash(NEW / 'result.json'),
        'old_result_sha256': file_hash(OLD / 'result.json'),
        'checker_sha256': file_hash(Path(__file__).resolve()),
        'rows': rows,
    }
    (OUT / 'verification.json').write_text(json.dumps(report, indent=2, default=str) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'canonical_identities_verified',
                      'saved_table_states_compared', 'exact_comparisons', 'mismatch_count',
                      'source_read_hash_units', 'new_file_stat_units',
                      'derived_per_plan_unit_delta', 'total_construction_units')}, indent=2))
    if failures:
        raise AssertionError(f'{len(failures)} mismatches.')


if __name__ == '__main__':
    main()
