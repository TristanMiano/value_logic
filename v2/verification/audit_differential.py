"""Read-back audit of F12 shard coverage and exact reported task witnesses.

This checks preserved evidence, not a second execution of the native receiver.
It uses the separate geometric reference and direct task losses, without
importing the proof producer, checker, decoder or native normalizer.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from pathlib import Path

from .model import Query
from .reference import reference, feasible, source_halfplanes, task_losses
from .workloads import ACTIONS, SEED, sources

FAMILIES = ('grid', 'rational', 'boundary', 'offgrid')


def source_vertices(evidence):
    """Canonical vertex set for these bounded nonempty planar sources only."""
    rows = source_halfplanes(evidence)
    vertices = set()
    for (a, b, c), (d, e, f) in combinations(rows, 2):
        determinant = a*e-b*d
        if determinant:
            point = ((c*e-b*f)/determinant, (a*f-c*d)/determinant)
            if all(x*point[0]+y*point[1] <= z for x, y, z in rows):
                vertices.add(point)
    if not vertices:
        raise ValueError('The frozen bounded, nonempty family lost all vertices.')
    return tuple(sorted(vertices))


def validate_shard(data, family, start, stop):
    population = sources(family)
    expected = dict(status='PASS', family=family, seed=SEED, start=start, stop=stop,
                    population_sources=len(population), checked_sources=stop-start,
                    queries=3*(stop-start), threshold_checks=6*(stop-start),
                    receipt_roundtrips=3*(stop-start))
    if any(type(data[key]) is not type(value) or data[key] != value for key, value in expected.items()):
        raise ValueError('Shard identity or declared coverage differs from its frozen workload.')
    if len(data['rows']) != stop-start:
        raise ValueError('Truncated or extended shard.')
    digest = hashlib.sha256()
    counts = Counter()
    for index, row in zip(range(start, stop), data['rows']):
        evidence = population[index]
        if type(row['index']) is not int or row['index'] != index:
            raise ValueError('Missing, duplicate or reordered source.')
        if row['bounds'] != [None if x is None else str(x) for x in evidence.bounds]:
            raise ValueError('Source bounds differ from the frozen generator.')
        if len(row['answers']) != len(ACTIONS):
            raise ValueError('Missing or extra consumer.')
        for action, answer in zip(ACTIONS, row['answers']):
            bound = Q(answer['bound'])
            point = tuple(Q(x) for x in answer['point'])
            semantic = reference(evidence, Query(action))
            if answer['action'] != action or bound != semantic.maximum:
                raise ValueError('Reported consumer/bound differs from independent reference.')
            if len(point) != 2 or not feasible(evidence, point):
                raise ValueError('Reported attainer violates its complete source.')
            losses = task_losses(point)
            if losses[action]-losses['F'] != bound:
                raise ValueError('Direct execution does not attain the reported bound.')
            if answer['decision'] != ('certified' if bound <= 0 else 'full_source_refuted'):
                raise ValueError('Reported decision differs from its exact bound.')
            if type(answer['steps']) is not int or not 1 <= answer['steps'] <= 128:
                raise ValueError('Invalid recorded bounded proof size.')
            if type(answer['basis_checks']) is not int or not 0 <= answer['basis_checks'] <= 440:
                raise ValueError('Invalid recorded bounded search work.')
            counts[answer['decision']] += 1
        digest.update(json.dumps(row, sort_keys=True, separators=(',', ':')).encode())
    if digest.hexdigest() != data['exact_rows_sha256'] or dict(counts) != data['decisions']:
        raise ValueError('Shard digest or decision totals disagree with its rows.')
    return counts


def audit(directory):
    directory = Path(directory)
    manifest = json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    if manifest['schema'] != 'F12-differential-manifest-v1' or manifest['shard_size'] != 100:
        raise ValueError('Unknown differential execution design.')
    if type(manifest['complete']) is not bool or type(manifest['max_attempts']) is not int or not 1 <= manifest['max_attempts'] <= 3:
        raise ValueError('Invalid completion or bounded-attempt declaration.')
    families = FAMILIES if manifest['family'] == 'all' else (manifest['family'],)
    if any(family not in FAMILIES for family in families):
        raise ValueError('Unknown differential family.')
    expected = {(family, start, min(start+100, len(sources(family))))
                for family in families for start in range(0, len(sources(family)), 100)}
    seen, completed = set(), set()
    counts = Counter()
    failures = []
    report_hashes = {}
    for unit in manifest['units']:
        key = unit['family'], unit['start'], unit['stop']
        if type(unit['start']) is not int or type(unit['stop']) is not int or key not in expected or key in seen:
            raise ValueError('Duplicate or undeclared shard.')
        if unit['status'] not in ('PASS', 'INCOMPLETE'):
            raise ValueError('Unknown shard status.')
        seen.add(key)
        passing = []
        if not 1 <= len(unit['attempts']) <= manifest['max_attempts'] <= 3:
            raise ValueError('Invalid bounded attempts.')
        for number, attempt in enumerate(unit['attempts'], 1):
            if type(attempt['number']) is not int or attempt['number'] != number or passing:
                raise ValueError('Attempts must stop at first success.')
            if type(attempt['valid_report']) is not bool or type(attempt['timed_out']) is not bool or type(attempt['exit_code']) is not int:
                raise ValueError('Malformed process outcome cannot establish execution coverage.')
            if attempt['valid_report'] and attempt['exit_code'] == 0 and not attempt['timed_out']:
                passing.append(attempt)
            else:
                failures.append({'unit': list(key), 'attempt': number, 'exit_code': attempt['exit_code']})
        if (unit['status'] == 'PASS') != (len(passing) == 1):
            raise ValueError('Shard status conflicts with its process attempts.')
        if not passing:
            continue
        filename = passing[0]['report']
        if Path(filename).name != filename:
            raise ValueError('A report must be a local filename.')
        raw = (directory/filename).read_bytes()
        report_hashes[filename] = hashlib.sha256(raw).hexdigest()
        counts.update(validate_shard(json.loads(raw), *key))
        completed.add(key)
    missing = sorted(expected-completed)
    if manifest['complete'] and missing:
        raise ValueError('A declared complete run has missing differential coverage.')
    distinct_bounds, distinct_regions = set(), set()
    family_coverage = {}
    for family in families:
        bounds, regions = set(), set()
        indices = set()
        population = sources(family)
        for name, start, stop in completed:
            if name != family:
                continue
            indices.update(range(start, stop))
            for evidence in population[start:stop]:
                bounds.add(evidence.bounds)
                regions.add(source_vertices(evidence))
        distinct_bounds.update(bounds)
        distinct_regions.update(regions)
        family_coverage[family] = {'source_records': len(indices), 'distinct_bound_tuples': len(bounds),
                                   'distinct_planar_source_regions': len(regions)}
    return {'status': 'COMPLETE' if manifest['complete'] and not missing else 'INCOMPLETE',
            'completed_shards': len(completed), 'expected_shards': len(expected),
            'checked_sources': sum(stop-start for _, start, stop in completed),
            'queries': sum(counts.values()), 'decisions': dict(counts),
            'missing_shards': [list(key) for key in missing], 'failed_attempts': failures,
            'distinct_bound_tuples': len(distinct_bounds), 'distinct_planar_source_regions': len(distinct_regions),
            'family_coverage': family_coverage,
            'report_sha256': report_hashes,
            'scope': 'Read-back coverage/digest/exact semantic witness audit; native receiver execution remains evidenced by the original process reports. Distinct source regions use exact vertex sets in this bounded planar family; different revision/row contexts may define the same region.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    data = audit(args.directory)
    args.json.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k != 'report_sha256'}, sort_keys=True))


if __name__ == '__main__':
    main()
