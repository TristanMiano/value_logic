"""Hostile F12 evidence-accounting tests; all timings here are synthetic."""
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from v2.verification.summarize_cost import (
    SEQUENCES, STRATEGIES, persistent_prefix_advantage, summarize, validate_report,
)


def synthetic_report(sequence='fixed-directions', strategy='fresh'):
    rows = [dict(index=i, revision=f'{sequence}-0-{i//3}', action=('T1', 'T2', 'R')[i % 3],
                 status='certified', bound='-1', reference_bound='-1', exact_bound=True,
                 true_request=True, missed_true_request=False, operation_ns=10,
                 cumulative_ns=10*(i+1), stage_ns={'generation': 5}, counters={'calls': 1},
                 request_bytes_including_source=1, output_receipt_bytes=10,
                 retained_receipt_bytes_including_old_sources=0, retained_catalogue_bytes=0,
                 total_live_serialized_bytes=11) for i in range(18)]
    return dict(schema='F12-sequence-cost-v1', status='PASS', sequence=sequence, strategy=strategy,
                cycles=1, queries=18, module_import_ns=1, strategy_loop_ns=181,
                reference_assessment_ns=1, total_operation_ns=180,
                true_requests=18, missed_true_requests=0, exact_bounds=18,
                peak_total_live_serialized_bytes=11, counters={'calls': 18}, rows=rows)


def synthetic_manifest(directory):
    units = []
    for sequence in SEQUENCES:
        for strategy in STRATEGIES['original']:
            name = f'{sequence}_{strategy}.json'
            (directory/name).write_text(json.dumps(synthetic_report(sequence, strategy)), encoding='utf-8')
            units.append(dict(sequence=sequence, strategy=strategy, repetition=1, status='PASS',
                              attempts=[dict(number=1, report=name, exit_code=0, timed_out=False,
                                             valid_report=True, process_elapsed_seconds=1)]))
    return dict(schema='F12-cost-manifest-v1', repetitions=1, max_attempts=3, complete=True, units=units)


class F12ReportTests(unittest.TestCase):
    def test_report_rejects_false_quality_and_aggregate_claims(self):
        mutations = (
            lambda d: d['rows'][0].update(exact_bound=False),
            lambda d: d['rows'][0].update(bound='-2'),
            lambda d: d['rows'][0].update(status='refuted'),
            lambda d: d['rows'][0].update(bound='1'),
            lambda d: d.update(true_requests=17),
            lambda d: d.update(counters={'calls': 0}),
            lambda d: d.update(peak_total_live_serialized_bytes=0),
        )
        for mutate in mutations:
            data = synthetic_report()
            mutate(data)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                validate_report(data)

    def test_report_rejects_bad_measurements_missing_storage_and_reordered_requests(self):
        mutations = (
            lambda d: d['rows'][0].update(operation_ns=True),
            lambda d: d['rows'][0].update(stage_ns={'generation': -1}),
            lambda d: d['rows'][0].update(stage_ns={'generation': 11}),
            lambda d: d['rows'][0].update(cumulative_ns=0),
            lambda d: d['rows'][0].update(total_live_serialized_bytes=1),
            lambda d: d['rows'][0].update(output_receipt_bytes=0, total_live_serialized_bytes=1),
            lambda d: d['rows'][0].update(action='R'),
            lambda d: d.update(rows=d['rows'][:-1]),
        )
        for mutate in mutations:
            data = synthetic_report()
            mutate(data)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                validate_report(data)

    def test_prefix_quality_distinguishes_valid_looser_bound_from_exact_bound(self):
        fresh = synthetic_report()
        candidate = deepcopy(fresh)
        for row in candidate['rows']:
            row.update(cumulative_ns=row['cumulative_ns']//2, bound='0', exact_bound=False)
        self.assertIsNone(persistent_prefix_advantage(candidate, fresh))
        self.assertEqual(persistent_prefix_advantage(candidate, fresh, require_exact_quality=False), 1)
        candidate['rows'][0].update(bound=None, status='unavailable')
        self.assertIsNone(persistent_prefix_advantage(candidate, fresh, require_exact_quality=False))

    def test_prefix_is_finite_horizon_and_requires_matching_requests(self):
        fresh = synthetic_report()
        candidate = deepcopy(fresh)
        candidate['rows'][-1]['cumulative_ns'] -= 1
        self.assertEqual(persistent_prefix_advantage(candidate, fresh), 18)
        candidate['rows'][0]['reference_bound'] = '0'
        with self.assertRaises(ValueError):
            persistent_prefix_advantage(candidate, fresh)

    def test_incomplete_manifest_never_becomes_complete_from_report_count(self):
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            manifest = synthetic_manifest(directory)
            manifest['complete'] = False
            (directory/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            self.assertEqual(summarize(directory)['status'], 'INCOMPLETE')
            manifest['units'].pop()
            (directory/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            result = summarize(directory)
            self.assertEqual(len(result['incomplete_units']), 1)
            manifest['complete'] = True
            (directory/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            with self.assertRaises(ValueError):
                summarize(directory)

    def test_bounded_retry_preserves_failure_cost(self):
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            manifest = synthetic_manifest(directory)
            attempts = manifest['units'][0]['attempts']
            attempts[0]['number'] = 2
            attempts.insert(0, dict(number=1, report='failed.json', exit_code=-1,
                                   timed_out=False, valid_report=False, process_elapsed_seconds=7))
            (directory/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            result = summarize(directory)
            self.assertEqual(result['status'], 'COMPLETE')
            self.assertEqual(result['failed_process_seconds'], 7)
            self.assertEqual(result['total_process_seconds_including_failed_attempts'], 19)
            fresh = next(row for row in result['rows'] if row['sequence'] == 'fixed-directions' and row['strategy'] == 'fresh')
            self.assertEqual(fresh['process_costs'][0]['seconds_including_failed_attempts'], 8)
            catalogue = next(row for row in result['rows'] if row['sequence'] == 'fixed-directions' and row['strategy'] == 'catalogue')
            pair = catalogue['paired_fresh_comparisons'][0]
            self.assertEqual(pair['completed_process_ratio_to_fresh'], 1)
            self.assertEqual(pair['process_ratio_including_retries_to_fresh'], 1/8)

    def test_manifest_rejects_duplicates_extra_units_and_invalid_attempt_histories(self):
        mutations = (
            lambda m: m['units'].append(deepcopy(m['units'][0])),
            lambda m: m['units'][0].update(strategy='invented'),
            lambda m: m['units'][0].update(repetition=True),
            lambda m: m['units'][0].update(status='INCOMPLETE'),
            lambda m: m['units'][0]['attempts'][0].update(number=2),
            lambda m: m['units'][0]['attempts'][0].update(process_elapsed_seconds=float('nan')),
            lambda m: m['units'][0]['attempts'].append(deepcopy(m['units'][0]['attempts'][0])),
            lambda m: m['units'][0]['attempts'][0].update(report='../outside.json'),
        )
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            for mutate in mutations:
                manifest = synthetic_manifest(directory)
                mutate(manifest)
                (directory/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
                with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                    summarize(directory)


if __name__ == '__main__':
    unittest.main()
