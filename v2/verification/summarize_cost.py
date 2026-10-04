"""Audit F12 cost manifests and summarize matched completed repetitions.

Incomplete units and failed-attempt wall costs remain explicit. Prefix
repayment means only persistence to the observed finite horizon.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import json
import math
from pathlib import Path
from statistics import median

SEQUENCES = ('fixed-directions', 'withdrawals', 'stable-revisions')
STRATEGIES = {
    'original': ('fresh', 'catalogue', 'reuse', 'reuse-fallback'),
    'optional': ('fresh', 'catalogue', 'anchored-reuse', 'selected-fresh'),
}


def nonnegative(value):
    if type(value) is not int or value < 0:
        raise ValueError('Expected a nonnegative integer measurement.')
    return value


def measurements(values):
    if not isinstance(values, dict):
        raise ValueError('Expected a measurement map.')
    return {key: nonnegative(value) for key, value in values.items()}


def validate_report(data):
    """Check internal accounting; this does not re-execute proof checking."""
    if data['status'] != 'PASS' or data['schema'] != 'F12-sequence-cost-v1':
        raise ValueError('Invalid completed report.')
    if type(data['cycles']) is not int or not 1 <= data['cycles'] <= 4 or data['queries'] != 18*data['cycles'] or len(data['rows']) != data['queries']:
        raise ValueError('Report differs from the declared bounded workload.')
    for field in ('module_import_ns', 'strategy_loop_ns', 'reference_assessment_ns', 'total_operation_ns'):
        nonnegative(data[field])
    previous = 0
    totals = Counter()
    for i, row in enumerate(data['rows']):
        if type(row['index']) is not int or row['index'] != i:
            raise ValueError('Invalid event identity.')
        if (row['revision'], row['action']) != (f"{data['sequence']}-{i//18}-{(i//3) % 6}", ('T1', 'T2', 'R')[i % 3]):
            raise ValueError('Event differs from the declared request order.')
        operation = nonnegative(row['operation_ns'])
        if nonnegative(row['cumulative_ns']) != previous+operation:
            raise ValueError('Cumulative time does not equal charged operation costs.')
        if sum(measurements(row['stage_ns']).values()) > operation:
            raise ValueError('Stage timings exceed the enclosing operation.')
        totals.update(measurements(row['counters']))
        previous = row['cumulative_ns']
        maximum = Fraction(row['reference_bound'])
        bound = None if row['bound'] is None else Fraction(row['bound'])
        if bound is not None and bound < maximum:
            raise ValueError('Reported bound is below the reported reference maximum.')
        if row['status'] not in ('certified', 'unavailable'):
            raise ValueError('An upper-bound producer cannot report semantic refutation.')
        if row['status'] == 'certified' and (bound is None or bound > 0):
            raise ValueError('Certificate does not establish the requested zero budget.')
        expected = {'true_request': maximum <= 0,
                    'missed_true_request': maximum <= 0 and row['status'] != 'certified',
                    'exact_bound': bound == maximum}
        for field, value in expected.items():
            if type(row[field]) is not bool or row[field] != value:
                raise ValueError('Outcome flags disagree with the reported bounds.')
        fields = ('request_bytes_including_source', 'output_receipt_bytes',
                  'retained_receipt_bytes_including_old_sources', 'retained_catalogue_bytes',
                  'total_live_serialized_bytes')
        size = {field: nonnegative(row[field]) for field in fields}
        base = size[fields[0]]+size[fields[2]]+size[fields[3]]
        if size[fields[4]] not in (base, base+size[fields[1]]):
            raise ValueError('Live storage accounting omits or duplicates an object.')
        if size[fields[4]] == base and size[fields[2]] < size[fields[1]]:
            raise ValueError('An uncounted output cannot be the retained receipt.')
        if (bound is None) != (size[fields[1]] == 0):
            raise ValueError('Reported bound lacks its serialized checked receipt.')
    if previous != data['total_operation_ns'] or previous > data['strategy_loop_ns']:
        raise ValueError('Report totals disagree with event timings.')
    for total, flag in (('true_requests', 'true_request'), ('missed_true_requests', 'missed_true_request'), ('exact_bounds', 'exact_bound')):
        if nonnegative(data[total]) != sum(row[flag] for row in data['rows']):
            raise ValueError('Aggregate quality count disagrees with event rows.')
    if measurements(data['counters']) != dict(totals):
        raise ValueError('Aggregate work counters disagree with event rows.')
    if nonnegative(data['peak_total_live_serialized_bytes']) != max(row['total_live_serialized_bytes'] for row in data['rows']):
        raise ValueError('Peak storage disagrees with event rows.')
    return data


def load_result(directory, attempt):
    name = attempt['report']
    if Path(name).name != name:
        raise ValueError('Report references must be local filenames.')
    data = json.loads((directory/name).read_text(encoding='utf-8'))
    return validate_report(data)


def persistent_prefix_advantage(candidate, fresh, *, require_exact_quality=True):
    """Equal current receipts/decisions; optionally equal exact-bound coverage."""
    if len(candidate['rows']) != len(fresh['rows']):
        raise ValueError('Different workloads cannot be paired.')
    favorable = []
    quality_equal = True
    for x, y in zip(candidate['rows'], fresh['rows']):
        if (x['revision'], x['action'], x['reference_bound']) != (y['revision'], y['action'], y['reference_bound']):
            raise ValueError('Paired run has a different request or oracle result.')
        quality_equal = quality_equal and (x['status'], x['bound'] is not None) == (y['status'], y['bound'] is not None)
        if require_exact_quality:
            quality_equal = quality_equal and x['exact_bound'] == y['exact_bound']
        favorable.append(quality_equal and x['cumulative_ns'] < y['cumulative_ns'])
    return next((i+1 for i in range(len(favorable)) if all(favorable[i:])), None)


def summarize(directory):
    directory = Path(directory)
    manifest = json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    if manifest['schema'] != 'F12-cost-manifest-v1':
        raise ValueError('Unknown cost manifest.')
    experiment = manifest.get('experiment', 'original')  # Original v1 runner omitted this label.
    cycles = manifest.get('cycles', 1)
    if type(cycles) is not int or not 1 <= cycles <= 4:
        raise ValueError('Invalid declared horizon.')
    if experiment not in STRATEGIES or type(manifest['repetitions']) is not int or not 1 <= manifest['repetitions'] <= 3:
        raise ValueError('Unknown experiment or repetition count.')
    if type(manifest['max_attempts']) is not int or not 1 <= manifest['max_attempts'] <= 3 or type(manifest['complete']) is not bool:
        raise ValueError('Invalid bounded-attempt/completion declaration.')
    expected = {(name, strategy, repetition) for name in SEQUENCES
                for strategy in STRATEGIES[experiment] for repetition in range(1, manifest['repetitions']+1)}
    reports = {}
    process_costs = {}
    seen = set()
    report_names = set()
    incomplete = []
    total_process_seconds = failed_process_seconds = 0.0
    failures = []
    for unit in manifest['units']:
        key = unit['sequence'], unit['strategy'], unit['repetition']
        if type(unit['repetition']) is not int or key not in expected or key in seen:
            raise ValueError('Duplicate or undeclared execution unit.')
        seen.add(key)
        if unit['status'] not in ('PASS', 'INCOMPLETE') or not 1 <= len(unit['attempts']) <= manifest['max_attempts']:
            raise ValueError('Invalid unit status or attempt count.')
        success = []
        unit_seconds = 0.0
        for number, attempt in enumerate(unit['attempts'], 1):
            if attempt['number'] != number or type(attempt['number']) is not int or success:
                raise ValueError('Attempts must be consecutive and stop at first success.')
            if type(attempt['valid_report']) is not bool or type(attempt['timed_out']) is not bool or type(attempt['exit_code']) is not int:
                raise ValueError('Malformed attempt outcome.')
            if attempt['report'] in report_names:
                raise ValueError('Attempt reports cannot be shared between units.')
            report_names.add(attempt['report'])
            elapsed = attempt['process_elapsed_seconds']
            if type(elapsed) not in (int, float) or not math.isfinite(elapsed) or elapsed < 0:
                raise ValueError('Invalid process duration.')
            total_process_seconds += elapsed
            unit_seconds += elapsed
            if attempt['valid_report'] and attempt['exit_code'] == 0 and not attempt['timed_out']:
                success.append(attempt)
            else:
                failed_process_seconds += elapsed
                failures.append({'unit': list(key), 'attempt': attempt['number'],
                                 'exit_code': attempt['exit_code'], 'timed_out': attempt['timed_out'],
                                 'elapsed_seconds': elapsed})
        if (unit['status'] == 'PASS') != (len(success) == 1):
            raise ValueError('Unit status disagrees with its successful attempts.')
        if not success:
            incomplete.append(list(key))
            continue
        data = load_result(directory, success[0])
        if (data['sequence'], data['strategy']) != key[:2] or data['cycles'] != cycles:
            raise ValueError('Report does not match its manifest unit.')
        reports[key] = data
        process_costs[key] = {'completed_seconds': success[0]['process_elapsed_seconds'],
                              'seconds_including_failed_attempts': unit_seconds,
                              'attempts': len(unit['attempts'])}
    incomplete.extend(list(key) for key in sorted(expected-seen))
    if manifest['complete'] and incomplete:
        raise ValueError('A declared-complete manifest lacks its required coverage.')
    grouped = defaultdict(list)
    for (name, strategy, repetition), data in reports.items():
        grouped[name, strategy].append((repetition, data))
    summary = []
    for (name, strategy), values in sorted(grouped.items()):
        values.sort()
        first = values[0][1]
        pattern = lambda data: [(r['status'], r['bound'], r['reference_bound']) for r in data['rows']]
        if any(pattern(data) != pattern(first) for _, data in values):
            raise ValueError('Repeated deterministic strategy returned different decisions or bounds.')
        durations = [data['total_operation_ns'] for _, data in values]
        stage_totals = []
        for _, data in values:
            totals = Counter()
            for row in data['rows']:
                totals.update(row['stage_ns'])
            stage_totals.append(dict(totals))
        pairs = []
        for repetition, data in values:
            fresh = reports.get((name, 'fresh', repetition))
            if fresh is not None and strategy != 'fresh':
                candidate_process = process_costs[name, strategy, repetition]
                fresh_process = process_costs[name, 'fresh', repetition]
                ratio = lambda a, b: a/b if b else None
                pairs.append({'repetition': repetition,
                              'operation_ratio_to_fresh': ratio(data['total_operation_ns'], fresh['total_operation_ns']),
                              'completed_process_ratio_to_fresh': ratio(candidate_process['completed_seconds'], fresh_process['completed_seconds']),
                              'process_ratio_including_retries_to_fresh': ratio(candidate_process['seconds_including_failed_attempts'], fresh_process['seconds_including_failed_attempts']),
                              'persistent_prefix_advantage_at_query': persistent_prefix_advantage(data, fresh),
                              'requested_decision_prefix_advantage_at_query': persistent_prefix_advantage(data, fresh, require_exact_quality=False)})
        summary.append({'sequence': name, 'strategy': strategy,
                        'completed_repetitions': len(values), 'operation_ns': durations,
                        'median_operation_ns': median(durations),
                        'min_operation_ns': min(durations), 'max_operation_ns': max(durations),
                        'module_import_ns': [data['module_import_ns'] for _, data in values],
                        'process_costs': [process_costs[name, strategy, repetition] for repetition, _ in values],
                        'stage_totals_ns': stage_totals,
                        'true_requests': first['true_requests'], 'missed_true_requests': first['missed_true_requests'],
                        'exact_bounds': first['exact_bounds'], 'queries': first['queries'],
                        'peak_total_live_serialized_bytes': first['peak_total_live_serialized_bytes'],
                        'counters': first['counters'], 'paired_fresh_comparisons': pairs})
    return {'status': 'COMPLETE' if manifest['complete'] and len(reports) == len(expected) and not incomplete else 'INCOMPLETE',
            'cycles': cycles, 'queries_per_unit': 18*cycles,
            'expected_units': len(expected), 'completed_units': len(reports), 'incomplete_units': incomplete,
            'failed_attempts': failures, 'failed_process_seconds': failed_process_seconds,
            'total_process_seconds_including_failed_attempts': total_process_seconds,
            'rows': summary,
            'interpretation': 'Timing distributions are descriptive and conditional on completed attempts; failures and their process time are retained. Prefix advantages hold only to the measured horizon. The strict field matches exact-bound/decision quality; the requested-decision field matches current receipt availability and decisions but permits weaker valid bounds.',
            'process_scope': 'Full child-process duration includes imports, strategy initialization, reference assessment and report I/O. It is not pure startup or pure strategy latency. Retry-inclusive values additionally charge failed attempts.',
            'novelty': 'NOT YET SUPPORTED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    data = summarize(args.directory)
    args.json.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k != 'rows'}, sort_keys=True))


if __name__ == '__main__':
    main()
