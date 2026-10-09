#!/usr/bin/env python3
"""Read-only 24-core accounting audit and four narrow cap-one charge probes."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import ast
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parent
RUN = ROOT.parents[1] / 'development/acquisition_planning_run_v1'
EXPECTED_SOURCE = '94fb8efcbb924470d883733f3c317fc0a79c4047089104ee4ee1c03ca5141f37'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('ascii')


def categories_from_source(path):
    tree = ast.parse(path.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'CATEGORIES' for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError('No declared resource categories.')


def audit_saved_cores():
    result = json.loads((RUN / 'result.json').read_text())
    prospective = json.loads((RUN.parent / 'acquisition_planning_plan_v1.json').read_text())
    assert result['status'] == 'PASS' and result['plans'] == len(result['rows']) == 24
    assert prospective['profile_caps'] == [1, 12]
    assert prospective['future_horizons'] == [128, 512, 4096, 16384]
    assert prospective['unit_prices'] == ['0', '1/10000', '1/1000']
    assert prospective['hypotheses'] == ['9/20', '11/20'] and prospective['prior_good'] == '1/2'
    hashes = result['source_hashes']
    assert hashes['07_acquisition_planning.py'] == EXPECTED_SOURCE
    for name, digest in hashes.items():
        assert sha256((RUN / 'sources' / name).read_bytes()).hexdigest() == digest
    categories = categories_from_source(RUN / 'sources/07_computation_adapter.py')
    sizes = {name: (RUN / 'sources' / name).stat().st_size for name in hashes}
    assert sum(sizes.values()) <= 512000
    source_units = 2 * sum((size + 7) // 8 for size in sizes.values())
    assert source_units == 7962
    seen, cases, total = set(), [], 0
    for row in result['rows']:
        cap, horizon, price = row['cap'], row['horizon'], F(row['unit_price'])
        key = (cap, horizon, price)
        assert key not in seen
        seen.add(key)
        stem = f'cap{cap}_h{horizon}_price{price.numerator}_{price.denominator}'
        saved = json.loads((RUN / (stem + '_plan.json')).read_text())
        core = saved['core']
        encoded = canonical(core)
        assert sha256(encoded).hexdigest() == saved['identity'] == row['plan_id']
        assert len(encoded) == row['core_bytes']
        count = (cap + 1) * (cap + 2) // 2
        words = 1024 + 64 * count
        assert len(core['rows']) == count
        assert core['word_envelope'] == words and len(encoded) <= 8 * words
        assert core['cap'] == cap and core['horizon'] == horizon and F(core['unit_price']) == price
        assert core['hypotheses'] == ['9/20', '11/20'] and core['prior'] == ['1/2', '1/2']
        assert core['attempt_loss_cost'] == '1/2'
        assert core['lookup_units'] == core['acquisition_control_units'] == 8
        assert core['numeric_cap_bits'] == 256
        assert dict(core['source_hashes']) == hashes
        expected_operations = {
            'admission.fixed_planner_model_admission': 96,
            'profile.planner_source_read_hash_words': source_units,
            'assessment.bounded_bellman_state_bundle': 128 * count,
            'storage.bounded_state_child_read_and_retention': 64 * count,
            'profile.bounded_planner_freeze_validate_hash': 2 * words,
            'storage.bounded_planner_core_retention': words,
        }
        by_category = {category: 0 for category in categories}
        for operation, units in expected_operations.items():
            by_category[operation.split('.', 1)[0]] += units
        units = sum(expected_operations.values())
        meter = row['meter']
        assert meter['operations'] == expected_operations
        assert meter['by_category'] == by_category
        assert meter['total'] == row['construction_units'] == units
        assert meter['remaining'] == meter['limit_total'] - units
        assert meter['events'] == count + 2 and meter['denials'] == 0
        assert core['construction_resources'] == [by_category[category] for category in categories]
        assert F(row['construction_cost']) == price * units
        assert F(row['prior_gain_excluding_construction']) == F(row['bellman_value_after_initial_lookup']) - 8 * price
        assert F(row['all_in_prior_gain']) == F(row['prior_gain_excluding_construction']) - price * units
        peak = 0
        for state in core['rows']:
            for value in state[:2] + state[3:]:
                if value is None:
                    continue
                q = F(value)
                peak = max(peak, q.numerator.bit_length(), q.denominator.bit_length())
        assert peak <= 256
        total += units
        cases.append({'cap': cap, 'horizon': horizon, 'unit_price': str(price),
                      'states': count, 'construction_units': units,
                      'core_bytes': len(encoded), 'core_word_envelope': words,
                      'peak_saved_numeric_bits': peak, 'identity': saved['identity'], 'status': 'PASS'})
    assert len(seen) == 24 and total == result['total_24_plan_construction_units'] == 700272
    return {'status': 'PASS', 'source_sizes': sizes, 'source_read_hash_units': source_units,
            'cases': cases, 'total_construction_units': total,
            'scope': 'Canonical numerical cores, saved resources and declared tariff arithmetic; no CPU measurement or observation generation.'}


def load_candidate():
    name = '_focused_saved_acquisition_planner'
    spec = importlib.util.spec_from_file_location(name, RUN / 'sources/07_acquisition_planning.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def narrow_charge_boundaries():
    module = load_candidate()
    cases = []
    for limit, expected_reads, expected_bounded, expected_canonical, succeeds in (
            (0, 0, 0, 0, False),
            (8058, 2, 0, 0, False),
            (8634, 2, 13, 0, False),
            (12282, 2, 13, 1, True)):
        meter = module.A.Meter(limit)
        counts = {'source_byte_reads': 0, 'bounded_value_checks': 0, 'canonical_encodings': 0,
                  'metadata_stats': 0, 'metadata_stats_before_any_charge': 0}
        original_read, original_stat = Path.read_bytes, Path.stat
        original_bounded, original_canonical = module.bounded, module.canonical

        def read_spy(path):
            counts['source_byte_reads'] += 1
            return original_read(path)

        def stat_spy(path, *args, **kwargs):
            counts['metadata_stats'] += 1
            counts['metadata_stats_before_any_charge'] += int(meter.total == 0)
            return original_stat(path, *args, **kwargs)

        def bounded_spy(value):
            counts['bounded_value_checks'] += 1
            return original_bounded(value)

        def canonical_spy(value):
            counts['canonical_encodings'] += 1
            return original_canonical(value)

        Path.read_bytes, Path.stat = read_spy, stat_spy
        module.bounded, module.canonical = bounded_spy, canonical_spy
        try:
            try:
                plan, core = module.build(1, 128, F(1, 1000), meter)
            except Exception as exc:
                error_type, returned_plan = type(exc).__name__, False
                if succeeds:
                    raise
            else:
                error_type, returned_plan = None, True
                assert succeeds
                assert sum(plan.construction_resources) == 12282
                assert plan.identity == 'a08ffff9d34266476d3deb50498a5879bd703e06f58cc38bca5177cf57ac2527'
        finally:
            Path.read_bytes, Path.stat = original_read, original_stat
            module.bounded, module.canonical = original_bounded, original_canonical
        assert counts['source_byte_reads'] == expected_reads
        assert counts['bounded_value_checks'] == expected_bounded
        assert counts['canonical_encodings'] == expected_canonical
        assert counts['metadata_stats'] == counts['metadata_stats_before_any_charge'] == 2
        assert returned_plan == succeeds
        cases.append({'limit': limit, 'returned_plan': returned_plan,
                      'error_type': error_type, 'observed_calls': counts,
                      'meter': meter.snapshot(), 'status': 'PASS'})
    return {'status': 'PASS', 'cases': cases,
            'scope': 'Only cap-one, H128, price1/1000, at four payment boundaries. No profile observations or future deployments.',
            'preflight_boundary': 'Two fixed source-stat metadata reads and input guards precede the first charge. Source-byte hashing, Bellman work and core encoding are prepaid.'}


def main():
    with (ROOT / 'core_accounting_attempt.json').open('x') as f:
        json.dump({'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
                   'source_sha256': EXPECTED_SOURCE, 'principal_credit_minutes': 0}, f, indent=2)
        f.write('\n')
    result = {'saved_core_accounting': audit_saved_cores(),
              'charge_boundaries': narrow_charge_boundaries(),
              'status': 'PASS', 'stage': 'DEVELOPMENT', 'principal_credit_minutes': 0}
    with (ROOT / 'core_accounting_result.json').open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps({'status': 'PASS', 'saved_cores': 24,
                      'total_construction_units': result['saved_core_accounting']['total_construction_units'],
                      'charge_boundary_probes': len(result['charge_boundaries']['cases']),
                      'preflight_boundary': result['charge_boundaries']['preflight_boundary']}, indent=2))


if __name__ == '__main__':
    main()
