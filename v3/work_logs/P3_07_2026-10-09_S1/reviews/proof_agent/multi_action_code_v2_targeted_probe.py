#!/usr/bin/env python3
"""Focused v2 review: saved records and the three repaired failure boundaries.

All new synthetic fixtures are DEVELOPMENT unit probes. This script never
executes a mathematical query's truth service or a development evidence run.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from math import isqrt
from types import SimpleNamespace
from datetime import datetime
import importlib.util
import json
import random
import sys

ROOT = Path(__file__).resolve().parent
RUN = ROOT.parents[1] / 'development/multi_action_run_v2'
DEVELOPMENT = RUN.parent
EXPECTED = {
    '07_multi_action_forecasting.py': '9605a0fa3483358bd6f0f98770b154888cbc37a37c4a746bfbf3e9f3f62453a7',
    '07_multi_action_development.py': 'cb5e191150905d9c1615277ab7b5dac0811e8646d2a76924499226dfa0fd7291',
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def semantic_state(f):
    return (f.residual, f.variance, f.allowances, f.slack, f.mixed,
            f.fixed, f.gaps, f.pending, f.settled, frozenset(f.used))


def numeric_cap_is_transactional(M, previous):
    f = M.Forecaster(actions=2, bins=4, work=M.Work())
    table = M.Table(((F(0), F(0)), (F(0), F(0))), F(1))
    for t in range(1, 17):
        issue = f.issue('numeric-cap-' + str(t), table,
                        weight=1 << 4093, root_cap=0)
        assert issue.p == F(1, 2)
        state = semantic_state(f)
        before = previous.safe_state(f)
        try:
            f.settle(issue.query, 1, f.scope)
        except M.Rejected as exc:
            after = previous.safe_state(f)
            assert t == 16
            assert semantic_state(f) == state
            assert f.pending is issue and f.settled == 15
            assert after['work']['total'] - before['work']['total'] == 312
            assert after['bound_bits'] <= M.MAX_RATIONAL_BITS
            report = f.report()
            assert report['pending'] and report['settled'] == 15
            return {'status': 'PASS', 'rejected_round': t,
                    'error_type': type(exc).__name__, 'error': str(exc),
                    'semantic_state_unchanged': True,
                    'retained_state_export_succeeds': True,
                    'paid_failed_settlement_units': 312,
                    'before': before, 'after': after,
                    'fixture_scope': '16 synthetic binary unit settlements; no real truth computation.'}
    raise AssertionError('The original numeric-cap fixture did not reject.')


def lookup_admission(M):
    checks = []
    for bits in (-1, 33, True, F(8), '8', 100000):
        work = M.Work(100)
        try:
            M.choose_slots((1, 0), bits, 0, work)
        except M.Rejected:
            pass
        else:
            raise AssertionError('Invalid direct bit count accepted.')
        assert work.total == 0
        checks.append({'bits_repr': repr(bits), 'outcome': 'Rejected', 'paid_units': 0})
    for slots in ((), (1,), (1,) + (0,) * 8):
        work = M.Work(100)
        try:
            M.choose_slots(slots, 0, 0, work)
        except M.Rejected:
            pass
        else:
            raise AssertionError('Invalid action count accepted.')
        assert work.total == 0
    for bits, slots, draw, expected in ((0, (1, 0), 0, 0),
                                        (8, (128, 128), 127, 0),
                                        (8, (128, 128), 128, 1),
                                        (32, (1 << 32, 0), (1 << 32) - 1, 0)):
        work = M.Work(6)
        assert M.choose_slots(slots, bits, draw, work) == expected
        assert work.counts == {'cumulative_selection': 6}
    invalid_cell = object()
    denied = M.Work(0)
    try:
        M.choose_slots((256, invalid_cell), 8, 0, denied)
    except M.Exhausted:
        pass
    else:
        raise AssertionError('Cell validation preceded its prepaid lookup bundle.')
    funded = M.Work(6)
    try:
        M.choose_slots((256, invalid_cell), 8, 0, funded)
    except M.Rejected:
        pass
    else:
        raise AssertionError('Malformed slot accepted.')
    assert funded.counts == {'cumulative_selection': 6}
    return {'status': 'PASS', 'invalid_bit_checks': checks,
            'invalid_action_counts_rejected_before_traversal': [0, 1, 9],
            'valid_boundary_bit_counts_checked': [0, 8, 32],
            'zero_budget_precedes_cell_validation': True,
            'funded_invalid_cell_charged_units': funded.total,
            'boundary': 'Lookup consumes an admitted draw; its caller separately prepays fair bits.'}


def harness_rng_failure_order(D, denied_name):
    out = ROOT / 'multi_action_code_v2_order_probes' / denied_name
    out.mkdir(parents=True, exist_ok=False)
    original_random, original_pay, original_complete = D.random, D.M.Work.pay, D.A.complete
    events, capture = [], {}

    class ActionRandom:
        def __init__(self, seed):
            self.rng = random.Random(seed)
            self.initial = self.rng.getstate()
            self.draws = 0

        def getrandbits(self, bits):
            events.append('getrandbits')
            self.draws += 1
            return self.rng.getrandbits(bits)

    def rng_factory(seed):
        if seed == 307127:
            capture['action_rng'] = ActionRandom(seed)
            return capture['action_rng']
        return random.Random(seed)

    def pay_at_boundary(work, name, count):
        if name in ('fair_random_bits', 'cumulative_selection'):
            events.append('pay:' + name)
        if name == denied_name:
            # Restrict only this fresh test object's remaining funds exactly at
            # the target prepaid boundary; this is not a production mutation.
            work.limit = work.total
            capture['work'] = work
        return original_pay(work, name, count)

    def no_truth(*args, **kwargs):
        raise AssertionError('A focused denial probe reached the truth service.')

    D.random = SimpleNamespace(Random=rng_factory)
    D.M.Work.pay = pay_at_boundary
    D.A.complete = no_truth
    try:
        try:
            D.exercise('denied_' + denied_name, 32, 8, out)
        except D.M.Exhausted as exc:
            error = str(exc)
        else:
            raise AssertionError('Injected insufficient funds did not stop execution.')
    finally:
        D.random, D.M.Work.pay, D.A.complete = original_random, original_pay, original_complete
    rng, work = capture['action_rng'], capture['work']
    if denied_name == 'fair_random_bits':
        assert events == ['pay:fair_random_bits']
        assert rng.draws == 0 and rng.rng.getstate() == rng.initial
        assert work.counts.get('fair_random_bits', 0) == 0
    else:
        assert events == ['pay:fair_random_bits', 'getrandbits', 'pay:cumulative_selection']
        assert rng.draws == 1 and work.counts['fair_random_bits'] == 8
        assert work.counts.get('cumulative_selection', 0) == 0
    issued = next(out.glob('*_issued.jsonl'))
    assert issued.read_bytes() == b''
    return {'status': 'PASS', 'denied_category': denied_name,
            'events': events, 'action_rng_draws': rng.draws,
            'rng_unchanged': rng.rng.getstate() == rng.initial,
            'paid_fair_bit_units': work.counts.get('fair_random_bits', 0),
            'paid_prefix_units': work.total, 'error': error,
            'issued_records': 0, 'real_truth_computations': 0}


def root_upper(value):
    scaled_num = value.numerator * (1 << 64)
    floor = isqrt(scaled_num // value.denominator)
    return F(floor + int(floor * floor * value.denominator < scaled_num), 1 << 32)


def additional_saved_checks():
    manifest = json.loads((RUN / 'manifest.json').read_text())
    summary = json.loads((RUN / 'result.json').read_text())
    plan = json.loads((DEVELOPMENT / 'multi_action_plan_v2.json').read_text())
    disposition = json.loads((DEVELOPMENT / 'multi_action_plan_v2_disposition.json').read_text())
    assert summary['status'] == 'PASS'
    assert plan['query_seed'] == 307113 and plan['action_seed'] == 307127
    assert manifest['source_hashes'] == summary['source_hashes'] == disposition['actual_v2_sources']
    for name, digest in manifest['source_hashes'].items():
        assert sha256((RUN / 'sources' / name).read_bytes()).hexdigest() == digest
    population = tuple((p, a) for p in (17, 31, 47, 61, 97) for a in range(1, p))
    results = []
    for rowpath in sorted(RUN.glob('*_rows.json')):
        name = rowpath.name.removesuffix('_rows.json')
        rows = json.loads(rowpath.read_text())
        saved = json.loads((RUN / (name + '_result.json')).read_text())
        old = json.loads((DEVELOPMENT / 'multi_action_run_v1' / rowpath.name).read_text())
        bits = saved['fair_bits']
        qr, ar = random.Random(307113), random.Random(307127)
        mixture, fixed, slack = F(0), [F(0)] * 4, F(0)
        rounding_correction, rounding_bound = F(0), F(0)
        for row in rows:
            assert datetime.fromisoformat(manifest['started_utc']) < datetime.fromisoformat(row['issued_utc'])
            assert datetime.fromisoformat(row['issued_utc']) < datetime.fromisoformat(summary['finished_utc'])
            modulus, base = population[qr.randrange(len(population))]
            assert row['query'] == {'a': base, 'n': (modulus - 1) // 2, 'm': modulus, 'r': 1}
            assert row['draw'] == ar.getrandbits(bits)
            q = tuple(map(F, row['mixture']))
            nu = tuple(map(F, row['dyadic_mixture']))
            p, eta, weight = map(F, (row['p'], row['eta'], row['weight']))
            assert sum(q) == sum(nu) == 1 and min(q) >= 0 and min(nu) >= 0
            costs = tuple(tuple(map(F, x)) for x in row['cost_rows'])
            predicted = tuple(left + (right-left)*p for left, right in costs)
            realized = tuple(left + (right-left)*row['label'] for left, right in costs)
            kkt = tuple(c + eta*qi for c, qi in zip(predicted, q))
            active_value = next(value for qi, value in zip(q, kkt) if qi > 0)
            assert all(value == active_value if qi > 0 else value >= active_value
                       for qi, value in zip(q, kkt))
            d = 1 << bits
            floors = tuple((d*x).numerator // (d*x).denominator for x in q)
            fractions = tuple(d*x-floor for x, floor in zip(q, floors))
            rem = d-sum(floors)
            top = sorted(range(4), key=lambda i: (-fractions[i], i))[:rem]
            expected_slots = tuple(floor+int(i in top) for i, floor in enumerate(floors))
            assert tuple(row['slots']) == expected_slots
            assert nu == tuple(F(x, d) for x in expected_slots)
            tv = sum((abs(a-b) for a, b in zip(q, nu)), F(0)) / 2
            rstar = min(d, 2)
            cap = F(rstar*(4-rstar), 4*d)
            assert tv == F(row['actual_tv']) <= F(row['tv_bound']) == cap
            transport = F(row['rounded_cost']) - F(row['ideal_cost'])
            cost_range = max(realized) - min(realized)
            assert abs(transport) <= cost_range*tv
            rounding_correction += weight*transport
            rounding_bound += weight*cost_range*cap
            mixture += weight*F(row['ideal_cost'])
            fixed = [a+weight*c for a, c in zip(fixed, realized)]
            slack += weight*eta*F(3, 16)
            regrets = tuple(mixture-c for c in fixed)
            assert regrets == tuple(map(F, row['action_regrets']))
            generic_bound = slack+100*root_upper(F(row['B']))
            assert generic_bound == F(row['generic_action_bound'])
            assert all(regret <= generic_bound for regret in regrets)
        assert rounding_correction == F(saved['dyadic_actual_correction'])
        assert rounding_bound == F(saved['dyadic_certified_correction'])
        assert saved['final']['work']['counts']['fair_random_bits'] == 32*bits
        assert saved['final']['work']['counts']['cumulative_selection'] == 320
        assert 'fair_bits_and_cumulative_selection' not in saved['final']['work']['counts']
        query_changes = sum(a['query'] != b['query'] for a, b in zip(rows, old))
        assert query_changes > 0
        results.append({'name': name, 'rows': len(rows), 'status': 'PASS',
                        'v1_query_positions_changed': query_changes,
                        'new_seed_streams_reconstructed': True,
                        'projection_kkt_dyadic_transport_and_row_bounds': 'PASS',
                        'separate_fair_bit_and_lookup_charges': 'PASS'})
    assert datetime.fromisoformat(plan['frozen_utc']) < datetime.fromisoformat(manifest['started_utc'])
    return {'status': 'PASS', 'cases': results,
            'plan_disposition': 'Inherited v1 metadata remains visible; appended v2 revision/seeds and prospective actual run manifest identify v2. Clarification preserves original plan bytes.',
            'manifest_source_hashes': manifest['source_hashes']}


def main():
    for name, digest in EXPECTED.items():
        assert sha256((RUN/'sources'/name).read_bytes()).hexdigest() == digest
        assert sha256((ROOT/('multi_action_code_v2_'+name)).read_bytes()).hexdigest() == digest
    previous = load('_review_v1_saved_equations', ROOT/'multi_action_code_v1_targeted_probe.py')
    previous.RUN = RUN
    M = load('_review_frozen_multi_v2', RUN/'sources/07_multi_action_forecasting.py')
    D = load('_review_frozen_development_v2', RUN/'sources/07_multi_action_development.py')
    with (ROOT/'multi_action_code_v2_probe_attempt.json').open('x') as out:
        json.dump({'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
                   'reused_saved_row_audit_sha256': sha256((ROOT/'multi_action_code_v1_targeted_probe.py').read_bytes()).hexdigest(),
                   'data_class': 'DEVELOPMENT', 'principal_credit_minutes': 0}, out, indent=2)
        out.write('\n')
    result = {'saved_evidence': previous.saved_evidence(),
              'additional_saved_checks': additional_saved_checks(),
              'numeric_cap_transaction': numeric_cap_is_transactional(M, previous),
              'lookup_admission': lookup_admission(M),
              'fair_bits_denial': harness_rng_failure_order(D, 'fair_random_bits'),
              'lookup_denial_after_paid_draw': harness_rng_failure_order(D, 'cumulative_selection'),
              'data_class': 'DEVELOPMENT', 'principal_credit_minutes': 0}
    result['status'] = 'PASS'
    with (ROOT/'multi_action_code_v2_targeted_result.json').open('x') as out:
        json.dump(result, out, indent=2)
        out.write('\n')
    print(json.dumps({'status': 'PASS', 'saved_rows_recomputed': 96,
                      'numeric_cap_rejected_before_commit': True,
                      'lookup_admission': 'PASS',
                      'fair_bits_denial': result['fair_bits_denial'],
                      'lookup_denial_after_paid_draw': result['lookup_denial_after_paid_draw']}, indent=2))


if __name__ == '__main__':
    main()
