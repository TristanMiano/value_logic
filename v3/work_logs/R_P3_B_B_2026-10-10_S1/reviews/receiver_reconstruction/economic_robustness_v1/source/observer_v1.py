#!/usr/bin/env python3
"""Independent exact frozen-invoice economics; no worker or analyzer imports.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import argparse
import csv
import hashlib
import json
import sys
import traceback

sys.dont_write_bytecode = True
SESSION = Path('v3/work_logs/R_P3_B_B_2026-10-10_S1')
RUN = SESSION / 'development/primary_v5'
ANALYSIS = SESSION / 'development/primary_analysis_v1'
METHODS = ('P-REUSE', 'P-FRESH', 'O-ADD-COLD', 'O-ADD-WARM',
           'O-ENUM-RECEIVER', 'O-ADD-PORTFOLIO')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def read_csv(path):
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle))


def write_json(path, value):
    raw = (json.dumps(value, sort_keys=True, indent=2) + '\n').encode('ascii')
    with path.open('xb') as handle:
        handle.write(raw)
    return {'file': path.name, 'bytes': len(raw), 'sha256': sha(raw)}


def inventory(root, wanted):
    return {name: {'bytes': len(raw), 'sha256': sha(raw)}
            for name in sorted(wanted)
            for raw in [(root / name).read_bytes()]}


def consumer_stage(stage):
    return stage.startswith('receiver_') or stage in {
        'terminal', 'failure_terminal', 'common_source'}


def key3(row):
    return row['stream'], row['recipient'], row['method']


def row_key(row):
    return (*key3(row), int(row['request_index']))


def cell_key(key):
    return {'stream': key[0], 'recipient': key[1]}


def string_fields(record):
    return {key: '' if value is None else str(value) for key, value in record.items()}


def compare_vectors(key, enum, portfolio, enum_units, portfolio_units):
    categories = sorted(set(enum) | set(portfolio))
    difference = {name: portfolio.get(name, 0) - enum.get(name, 0) for name in categories}
    lower = [name for name in categories if difference[name] > 0]
    higher = [name for name in categories if difference[name] < 0]
    equal = [name for name in categories if difference[name] == 0]
    return {**cell_key(key), 'enum_vector': dict(sorted(enum.items())),
            'portfolio_vector': dict(sorted(portfolio.items())),
            'portfolio_minus_enum_vector': difference,
            'enum_componentwise_weakly_lower': not higher,
            'enum_strictly_lower_categories': lower,
            'enum_higher_categories': higher,
            'equal_categories': equal,
            'enum_total_units': enum_units, 'portfolio_total_units': portfolio_units,
            'portfolio_minus_enum_total_units': portfolio_units - enum_units}


def minimizing_interval(method, lines):
    """Intersect exact a_i+rho*c_i <= a_j+rho*c_j half-lines."""
    a, c = lines[method]
    low, high = Fraction(0), None
    constraints, impossible = [], []
    for other, (other_a, other_c) in sorted(lines.items()):
        if other == method:
            continue
        slope = c - other_c
        rhs = other_a - a
        if slope == 0:
            if rhs < 0:
                impossible.append(other)
            constraints.append({'other': other, 'kind': 'parallel',
                                'satisfied': rhs >= 0, 'rhs': rhs})
        else:
            boundary = Fraction(rhs, slope)
            if slope > 0:
                high = boundary if high is None else min(high, boundary)
                kind = 'upper'
            else:
                low = max(low, boundary)
                kind = 'lower'
            constraints.append({'other': other, 'kind': kind,
                                'boundary': str(boundary)})
    feasible = not impossible and (high is None or low <= high)
    return {'method': method, 'nonempty': feasible, 'lower': str(low),
            'upper': None if high is None else str(high),
            'endpoints_closed': True, 'parallel_blockers': impossible,
            'constraints': constraints}


def exact_envelope(lines):
    domains = {method: minimizing_interval(method, lines) for method in lines}
    breakpoints = {Fraction(0)}
    ordered = sorted(lines)
    for i, one in enumerate(ordered):
        a, c = lines[one]
        for two in ordered[i+1:]:
            other_a, other_c = lines[two]
            if c != other_c:
                crossing = Fraction(other_a - a, c - other_c)
                if crossing >= 0:
                    breakpoints.add(crossing)
    points = sorted(breakpoints)
    samples = [(value, 'crossing_or_zero') for value in points]
    samples += [((left + right)/2, 'between_crossings')
                for left, right in zip(points, points[1:])]
    samples.append((points[-1] + 1, 'unbounded_tail'))
    witnesses = []
    for rho, kind in sorted(samples):
        costs = {method: a + rho*c for method, (a, c) in lines.items()}
        least = min(costs.values())
        direct = sorted(method for method, cost in costs.items() if cost == least)
        predicted = sorted(method for method, domain in domains.items()
                           if domain['nonempty'] and Fraction(domain['lower']) <= rho
                           and (domain['upper'] is None or rho <= Fraction(domain['upper'])))
        assert direct == predicted, (rho, direct, predicted)
        witnesses.append({'rho': str(rho), 'kind': kind,
                          'minimizers': direct, 'minimum_cost': str(least)})
    winning = [domain for domain in domains.values() if domain['nonempty']]
    winning.sort(key=lambda d: (Fraction(d['lower']), d['method']))
    return {'all_line_domains': domains, 'winning_intervals': winning,
            'partition_checks': witnesses,
            'nonnegative_pairwise_crossings_plus_zero': [str(x) for x in points],
            'independent_partition_check': 'PASS'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = args.repository.resolve()
    args.out.mkdir(parents=True, exist_ok=False)
    expected_inventory = read_json(args.inputs)
    before = inventory(root, expected_inventory)
    assert before == expected_inventory
    artifacts = []
    result = {'schema': 'rp3bb.independent-economic-robustness.v1',
              'stage': 'DEVELOPMENT', 'status': 'RUNNING', 'error': None}
    try:
        run, analysis_dir = root / RUN, root / ANALYSIS
        manifest, summary = read_json(run/'manifest.json'), read_json(run/'summary.json')
        analysis = read_json(analysis_dir/'analysis.json')
        raw = (run/'completed_units.jsonl').read_bytes()
        assert manifest['suite'] == summary['suite'] == 'primary'
        assert manifest['stage'] == summary['stage'] == 'DEVELOPMENT'
        assert summary['status'] == 'PASS'
        assert sha((run/'manifest.json').read_bytes()) == summary['manifest_sha256']
        assert sha(raw) == summary['completed_units_sha256']
        assert manifest['source_hashes'] == summary['source_hashes'] == analysis['input_source_hashes']
        for name, expected in manifest['source_hashes'].items():
            assert sha((run/'sources'/name).read_bytes()) == expected
        for name, expected in read_json(analysis_dir/'files.sha256.json').items():
            assert sha((analysis_dir/name).read_bytes()) == expected
        assert analysis['input_manifest_sha256'] == summary['manifest_sha256']
        assert analysis['input_completed_units_sha256'] == summary['completed_units_sha256']
        units = [json.loads(line) for line in raw.splitlines()]
        assert len(units) == summary['units']
        rows = [row for row in units if row.get('kind') == 'primary_delivery']
        assert len(rows) == 288 and analysis['delivery_rows'] == 288
        assert tuple(manifest['methods']) == METHODS
        assert {row['status'] for row in rows} == {'DELIVERED'}
        groups = defaultdict(list)
        request_vectors = {}
        raw_category_rows = {}
        expected_detail = {}
        outputs = defaultdict(set)
        for row in rows:
            key = row_key(row)
            assert key not in request_vectors
            groups[key[:3]].append(row)
            invoice = row['invoice']
            vector = Counter()
            total = consumer = 0
            for stage, categories in invoice['by_stage'].items():
                for category, count in categories.items():
                    assert type(count) is int and count >= 0
                    vector[category] += count
                    total += count
                    if consumer_stage(stage):
                        consumer += count
                    category_key = (*key, stage, category)
                    assert category_key not in raw_category_rows
                    raw_category_rows[category_key] = count
            assert total == invoice['total_units']
            assert consumer == invoice['consumer_units'] <= total
            assert total + invoice['failure_terminal_reserve'] <= invoice['budget']
            if invoice['consumer_budget'] is not None:
                assert consumer + invoice['failure_terminal_reserve'] <= invoice['consumer_budget']
            request_vectors[key] = vector
            outputs[row['stream'], row['case']].add(row['output'])
            one = dict(stream=row['stream'], recipient=row['recipient'], method=row['method'],
                       request_index=row['request_index'], case=row['case'], status=row['status'],
                       total_units=total, consumer_units=consumer,
                       source_units=sum(invoice['by_stage'].get('common_source', {}).values()),
                       proof_bytes=row['proof_bytes'],
                       producer_live_bytes=row['producer_live_snapshot_bytes'],
                       receiver_live_bytes=row['receiver_live_snapshot_bytes'],
                       producer_retained_bytes=row['producer_retained_bytes'],
                       receiver_retained_bytes=row['receiver_retained_bytes'])
            for threshold in manifest['consumer_thresholds']:
                one['observed_consumer_bill_le_' + str(threshold)] = consumer <= threshold
                one['observed_bill_plus_reserve_le_' + str(threshold)] = (
                    consumer + invoice['failure_terminal_reserve'] <= threshold)
            expected_detail[key] = string_fields(one)
        assert len(outputs) == 24 and all(len(values) == 1 for values in outputs.values())
        published_detail = {row_key(row): row for row in read_csv(analysis_dir/'per_request.csv')}
        assert published_detail == expected_detail
        published_categories = {}
        for row in read_csv(analysis_dir/'raw_categories.csv'):
            key = (*row_key(row), row['stage'], row['category'])
            assert key not in published_categories
            published_categories[key] = int(row['count'])
        assert published_categories == raw_category_rows

        complete_vectors, expected_totals, coordinates = {}, {}, {}
        for key, sequence in sorted(groups.items()):
            sequence.sort(key=lambda row: row['request_index'])
            assert [row['request_index'] for row in sequence] == list(range(1, 7))
            vector = Counter()
            for row in sequence:
                vector.update(request_vectors[row_key(row)])
            complete_vectors[key] = vector
            total = sum(row['invoice']['total_units'] for row in sequence)
            consumer = sum(row['invoice']['consumer_units'] for row in sequence)
            coordinates[key] = (total-consumer, consumer)
            first, last = sequence[0], sequence[-1]
            one = dict(stream=key[0], recipient=key[1], method=key[2], requests=6,
                       delivered=6, failed=0, all_delivered=True, total_units=total,
                       first_request_units=first['invoice']['total_units'],
                       later_five_units=total-first['invoice']['total_units'],
                       consumer_units=consumer,
                       maximum_consumer_units=max(row['invoice']['consumer_units'] for row in sequence),
                       source_units=sum(sum(row['invoice']['by_stage'].get('common_source', {}).values())
                                        for row in sequence),
                       python_opcode_events=vector['observed_python_opcode_events'],
                       bounded_native_c_call_events=vector['bounded_native_c_call_events'],
                       live_serialized_byte_periods=vector['live_serialized_byte_periods'],
                       proof_output_bytes=sum(row['proof_bytes'] for row in sequence),
                       final_producer_retained_bytes=last['producer_retained_bytes'],
                       final_receiver_retained_bytes=last['receiver_retained_bytes'])
            expected_totals[key] = string_fields(one)
        assert len(groups) == 48
        published_totals = {key3(row): row for row in read_csv(analysis_dir/'totals.csv')}
        assert expected_totals == published_totals
        cells = sorted({key[:2] for key in groups})
        assert len(cells) == 8
        published_cells = {(row['stream'], row['recipient']): row for row in analysis['cells']}
        for cell in cells:
            ordinary = {method: sum(coordinates[*cell, method])
                        for method in METHODS if method.startswith('O-')}
            best = min(ordinary.values())
            published = published_cells[cell]
            assert published['best_complete_fixed_ordinary_units'] == best
            assert sorted(published['best_complete_fixed_ordinary_methods']) == sorted(
                method for method, cost in ordinary.items() if cost == best)
            assert published['portfolio_reuse_units'] == sum(coordinates[*cell, 'P-REUSE'])
            assert published['portfolio_minus_best_ordinary_units'] == sum(coordinates[*cell, 'P-REUSE']) - best

        pooled, requestwise, envelopes = [], [], []
        for cell in cells:
            ekey, pkey = (*cell, 'O-ENUM-RECEIVER'), (*cell, 'P-REUSE')
            comparison = compare_vectors(cell, complete_vectors[ekey], complete_vectors[pkey],
                                         sum(coordinates[ekey]), sum(coordinates[pkey]))
            comparison['requests'] = 6
            pooled.append(comparison)
            for index in range(1, 7):
                enum_row = groups[ekey][index-1]
                portfolio_row = groups[pkey][index-1]
                assert enum_row['case'] == portfolio_row['case']
                comp = compare_vectors(cell, request_vectors[(*ekey, index)], request_vectors[(*pkey, index)],
                                       enum_row['invoice']['total_units'], portfolio_row['invoice']['total_units'])
                comp.update(request_index=index, case=enum_row['case'])
                requestwise.append(comp)
            lines = {method: coordinates[*cell, method] for method in METHODS}
            envelope = exact_envelope(lines)
            p_a, p_c = lines['P-REUSE']
            dominators = [dict(method=method, fixed_nonconsumer_saving=p_a-a, consumer_saving=p_c-c)
                          for method, (a, c) in lines.items()
                          if method.startswith('O-') and a <= p_a and c <= p_c and (a < p_a or c < p_c)]
            envelopes.append({**cell_key(cell),
                              'coordinates': {method: {'fixed_nonconsumer': a, 'consumer': c,
                                                       'unit_price_total': a+c}
                                              for method, (a, c) in lines.items()},
                              **envelope,
                              'portfolio_ever_minimizes_including_ties':
                                  envelope['all_line_domains']['P-REUSE']['nonempty'],
                              'ordinary_coordinate_dominators_of_portfolio': dominators})
        assert len(requestwise) == 48
        artifacts.append(write_json(args.out/'pooled_category_comparisons.json', pooled))
        artifacts.append(write_json(args.out/'request_category_comparisons.json', requestwise))
        artifacts.append(write_json(args.out/'price_envelopes.json', envelopes))
        concise = {
            'pooled_groups': len(pooled),
            'pooled_enum_componentwise_weakly_lower': sum(r['enum_componentwise_weakly_lower'] for r in pooled),
            'pooled_vector_exceptions': [r for r in pooled if not r['enum_componentwise_weakly_lower']],
            'pooled_enum_strict_total_savings': sum(r['portfolio_minus_enum_total_units'] > 0 for r in pooled),
            'paired_requests': len(requestwise),
            'request_enum_componentwise_weakly_lower': sum(r['enum_componentwise_weakly_lower'] for r in requestwise),
            'request_vector_exceptions': [r for r in requestwise if not r['enum_componentwise_weakly_lower']],
            'request_enum_strict_total_savings': sum(r['portfolio_minus_enum_total_units'] > 0 for r in requestwise),
            'request_unit_price_exceptions': [r for r in requestwise if r['portfolio_minus_enum_total_units'] <= 0],
            'groups_where_portfolio_can_minimize_including_ties': [
                cell_key((r['stream'], r['recipient'])) for r in envelopes
                if r['portfolio_ever_minimizes_including_ties']],
            'winning_intervals': [{**cell_key((r['stream'], r['recipient'])),
                                   'intervals': [{key: value for key, value in domain.items()
                                                  if key in ('method', 'lower', 'upper', 'endpoints_closed')}
                                                 for domain in r['winning_intervals']]}
                                  for r in envelopes],
        }
        result.update(status='PASS', findings=concise,
                      reconciliation={'raw_primary_deliveries': len(rows), 'full_method_streams': len(groups),
                                      'per_request_csv_rows': len(published_detail),
                                      'raw_category_csv_rows': len(published_categories),
                                      'totals_csv_rows': len(published_totals),
                                      'published_unit_price_cells': len(published_cells),
                                      'common_output_cases': len(outputs),
                                      'all_compared_fields_equal': True,
                                      'proof_correctness_reexecuted': False,
                                      'blob_proofs_rechecked': False})
    except BaseException as error:
        result.update(status='UNEXPECTED_FAILURE_PRESERVED',
                      error={'type': type(error).__name__, 'message': str(error),
                             'traceback': traceback.format_exc()})
    after = inventory(root, expected_inventory)
    if after != before:
        result['status'] = 'UNEXPECTED_SOURCE_CHANGE'
    result.update(artifacts=artifacts, input_before=before, input_after=after,
                  inputs_unchanged=before == after,
                  observer_sha256=sha(Path(__file__).read_bytes()),
                  price_scope='Fixed recorded path: nonconsumer + rho*consumer; rho>=0. No reexecution, threshold admission, governor, physical-cost or population inference.',
                  policy_runs=0, worker_edits=0, principal_clock_credit_seconds=0)
    receipt = write_json(args.out/'results.json', result)
    print(json.dumps({'status': result['status'], 'results': receipt,
                      'summary': {key: value for key, value in result.get('findings', {}).items()
                                  if key not in ('pooled_vector_exceptions', 'request_vector_exceptions',
                                                 'request_unit_price_exceptions', 'winning_intervals')}}, indent=2))
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
