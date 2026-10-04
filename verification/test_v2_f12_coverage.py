"""Read-back coverage controls using synthetic, explicitly non-native reports."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from v2.verification.audit_differential import audit, source_vertices, validate_shard
from v2.verification.model import Evidence, Query
from v2.verification.reference import reference
from v2.verification.workloads import ACTIONS, SEED, sources


def seal(data):
    digest = hashlib.sha256()
    counts = Counter()
    for row in data['rows']:
        digest.update(json.dumps(row, sort_keys=True, separators=(',', ':')).encode())
        counts.update(answer['decision'] for answer in row['answers'])
    data['exact_rows_sha256'] = digest.hexdigest()
    data['decisions'] = dict(counts)
    return data


def synthetic_shard():
    rows = []
    for i, evidence in enumerate(sources('offgrid')):
        answers = []
        for action in ACTIONS:
            result = reference(evidence, Query(action))
            answers.append(dict(action=action, bound=str(result.maximum),
                                point=[str(x) for x in result.witness],
                                decision='certified' if result.maximum <= 0 else 'full_source_refuted',
                                steps=1, basis_checks=0))
        rows.append(dict(index=i, bounds=[None if x is None else str(x) for x in evidence.bounds], answers=answers))
    return seal(dict(status='PASS', family='offgrid', seed=SEED, start=0, stop=4,
                     population_sources=4, checked_sources=4, queries=12,
                     threshold_checks=24, receipt_roundtrips=12, rows=rows))


class F12CoverageTests(unittest.TestCase):
    def test_audit_checks_semantics_even_when_digest_is_recomputed(self):
        mutations = (
            lambda d: d['rows'][0]['answers'][0].update(bound='-100'),
            lambda d: d['rows'][0]['answers'][0].update(point=['2', '2']),
            lambda d: d['rows'][0]['answers'][0].update(action='R'),
            lambda d: d['rows'][0].update(bounds=[None]*4),
            lambda d: d['rows'][1].update(index=0),
        )
        for mutate in mutations:
            data = synthetic_shard()
            mutate(data)
            seal(data)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                validate_shard(data, 'offgrid', 0, 4)

    def test_audit_checks_declared_coverage_and_exact_digest(self):
        data = synthetic_shard()
        self.assertEqual(sum(validate_shard(data, 'offgrid', 0, 4).values()), 12)
        for field, value in (('queries', 11), ('seed', 0), ('exact_rows_sha256', '0'*64)):
            changed = deepcopy(data)
            changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_shard(changed, 'offgrid', 0, 4)

    def test_geometric_duplicates_remain_distinct_contexts(self):
        absent = Evidence()
        redundant = Evidence(2, 2, 1, 1)
        self.assertNotEqual(absent.bounds, redundant.bounds)
        self.assertEqual(source_vertices(absent), source_vertices(redundant))
        self.assertEqual(source_vertices(Evidence(beta=0, gamma=0)), ((Q(0), Q(0)),))
        self.assertEqual(source_vertices(Evidence(beta=0)), ((Q(0), Q(-1)), (Q(0), Q(1))))

    def test_missing_and_duplicate_shards_cannot_become_complete(self):
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory/'report.json').write_text(json.dumps(synthetic_shard()), encoding='utf-8')
            unit = dict(family='offgrid', start=0, stop=4, status='PASS', attempts=[
                dict(number=1, valid_report=True, exit_code=0, timed_out=False, report='report.json')])
            manifest = dict(schema='F12-differential-manifest-v1', family='offgrid', shard_size=100,
                            max_attempts=3, complete=True, units=[unit])
            def evaluate():
                (directory/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
                return audit(directory)
            self.assertEqual(evaluate()['queries'], 12)
            for field, bad in (('complete', 'false'), ('max_attempts', True)):
                old = manifest[field]
                manifest[field] = bad
                with self.subTest(field=field), self.assertRaises(ValueError):
                    evaluate()
                manifest[field] = old
            unit['attempts'][0]['valid_report'] = 'false'
            with self.assertRaises(ValueError):
                evaluate()
            unit['attempts'][0]['valid_report'] = True
            manifest['units'].append(deepcopy(unit))
            with self.assertRaises(ValueError):
                evaluate()
            manifest['units'] = []
            with self.assertRaises(ValueError):
                evaluate()
            manifest['complete'] = False
            self.assertEqual(evaluate()['status'], 'INCOMPLETE')


if __name__ == '__main__':
    unittest.main()
