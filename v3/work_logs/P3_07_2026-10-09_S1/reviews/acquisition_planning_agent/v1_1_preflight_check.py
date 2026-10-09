#!/usr/bin/env python3
"""Targeted changed-preflight checks; no Bellman state is evaluated."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parent
RUN = ROOT.parents[1] / 'development/acquisition_planning_run_v1_1'
EXPECTED = '88c73b82ac2809da8f31a8dcb93237e732f93b73665a42f5ec180d6355c782b7'


def load():
    path = RUN / 'sources/07_acquisition_planning.py'
    assert sha256(path.read_bytes()).hexdigest() == EXPECTED
    name = '_targeted_acquisition_planning_v1_1'
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def probe(module, name, limit, price, cap=1, budget_denial=False,
          expected_paid=96, expected_stats=0, expected_reads=0,
          expected_equalities=None, message_contains=None):
    meter = module.A.Meter(limit)
    seen = {'stat_paid_totals': [], 'byte_read_paid_totals': [],
            'fraction_equalities': 0, 'oversized_fraction_equalities': 0,
            'bellman_numeric_checks': 0}
    old_stat, old_read, old_equal, old_bounded = Path.stat, Path.read_bytes, F.__eq__, module.bounded

    def stat_spy(path, *args, **kwargs):
        seen['stat_paid_totals'].append(meter.total)
        return old_stat(path, *args, **kwargs)

    def read_spy(path):
        seen['byte_read_paid_totals'].append(meter.total)
        return old_read(path)

    def equal_spy(left, right):
        seen['fraction_equalities'] += 1
        for value in (left, right):
            if type(value) is F and max(value.numerator.bit_length(), value.denominator.bit_length()) > 256:
                seen['oversized_fraction_equalities'] += 1
                raise AssertionError('An oversized Fraction reached equality.')
        return old_equal(left, right)

    def bounded_spy(value):
        seen['bellman_numeric_checks'] += 1
        return old_bounded(value)

    Path.stat, Path.read_bytes, F.__eq__, module.bounded = stat_spy, read_spy, equal_spy, bounded_spy
    try:
        try:
            module.build(cap, 128, price, meter)
        except Exception as exc:
            error_type, error = type(exc).__name__, str(exc)
            if budget_denial:
                assert meter.denials == 1
            else:
                assert isinstance(exc, ValueError) and meter.denials == 0
        else:
            raise AssertionError('Focused preflight fixture unexpectedly returned a plan.')
    finally:
        Path.stat, Path.read_bytes, F.__eq__, module.bounded = old_stat, old_read, old_equal, old_bounded
    assert meter.total == expected_paid
    assert len(seen['stat_paid_totals']) == expected_stats
    assert all(total >= 98 for total in seen['stat_paid_totals'])
    assert len(seen['byte_read_paid_totals']) == expected_reads
    assert all(total >= 8178 for total in seen['byte_read_paid_totals'])
    assert seen['oversized_fraction_equalities'] == seen['bellman_numeric_checks'] == 0
    if expected_equalities is not None:
        assert seen['fraction_equalities'] == expected_equalities
    if message_contains is not None:
        assert message_contains in error
    price_bits = None
    if type(price) is F:
        price_bits = {'numerator': price.numerator.bit_length(), 'denominator': price.denominator.bit_length()}
    return {'name': name, 'limit': limit, 'price_bits': price_bits,
            'error_type': error_type, 'error': error,
            'observed': seen, 'meter': meter.snapshot(), 'status': 'PASS'}


def main():
    with (ROOT / 'v1_1_preflight_attempt.json').open('x') as f:
        json.dump({'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
                   'source_sha256': EXPECTED, 'principal_credit_minutes': 0}, f, indent=2)
        f.write('\n')
    module = load()
    cases = []
    valid = F(1, 1000)
    cases.append(probe(module, 'unfunded_valid_admission', 0, valid, budget_denial=True,
                       expected_paid=0, expected_equalities=0))
    cases.append(probe(module, 'unfunded_invalid_values', 0, F(-(1 << 256)), cap=2,
                       budget_denial=True, expected_paid=0, expected_equalities=0))
    cases.append(probe(module, 'funded_invalid_cap', 96, valid, cap=2,
                       expected_equalities=0, message_contains='cap and horizon'))
    cases.append(probe(module, 'funded_wrong_price_type', 96, 0.001,
                       expected_equalities=0, message_contains='Exact rational'))
    cases.append(probe(module, 'denied_stat_bundle', 96, valid, budget_denial=True,
                       expected_paid=96, expected_equalities=3))
    cases.append(probe(module, 'denied_source_hash_bundle', 98, valid, budget_denial=True,
                       expected_paid=98, expected_stats=2, expected_equalities=3))
    cases.append(probe(module, 'denied_first_state_bundle', 8178, valid, budget_denial=True,
                       expected_paid=8178, expected_stats=2, expected_reads=2, expected_equalities=3))
    for name, price in (
            ('oversized_positive_numerator', F(1 << 256)),
            ('oversized_negative_numerator', F(-(1 << 256))),
            ('oversized_denominator', F(1, 1 << 256))):
        cases.append(probe(module, name, 96, price, expected_equalities=0,
                           message_contains='bounded comparison domain'))
    for name, price in (
            ('at_cap_positive_numerator', F(1 << 255)),
            ('at_cap_negative_numerator', F(-(1 << 255))),
            ('at_cap_denominator', F(1, 1 << 255))):
        cases.append(probe(module, name, 96, price, expected_equalities=3,
                           message_contains='Fixed rational resource price'))
    result = {'status': 'PASS', 'cases': cases, 'principal_credit_minutes': 0,
              'scope': 'Changed preflight only. Zero Bellman numeric checks, no model/DP re-audit, observations or deployments.',
              'source_sha256': EXPECTED}
    with (ROOT / 'v1_1_preflight_result.json').open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps({'status': 'PASS', 'targeted_preflight_cases': len(cases),
                      'oversized_equality_calls': 0, 'bellman_numeric_checks': 0,
                      'source_stat_prepaid_total': 98, 'source_bytes_prepaid_total': 8178}, indent=2))


if __name__ == '__main__':
    main()
