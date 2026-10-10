#!/usr/bin/env python3
"""Exact, post-exposure price analysis of fixed R-P3-B-B delivery invoices.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
No worker imports, policy executions, new service prices or clock credit.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def ratio(value):
    if value is None:
        return None
    return str(value.numerator) + '/' + str(value.denominator)


def is_consumer(stage):
    return stage.startswith('receiver_') or stage in (
        'common_source', 'terminal', 'failure_terminal')


def vector(row):
    result = Counter()
    for counts in row['invoice']['by_stage'].values():
        result.update(counts)
    assert sum(result.values()) == row['invoice']['total_units']
    assert all(isinstance(v, int) and v >= 0 for v in result.values())
    return result


def compare(left, right):
    """Return exact left-minus-right vector; absent coordinates mean zero."""
    keys = sorted(set(left) | set(right))
    delta = {key: left[key] - right[key] for key in keys}
    return {'left_minus_right': delta,
            'left_componentwise_le_right': all(v <= 0 for v in delta.values()),
            'strictly_lower_coordinates': [k for k, v in delta.items() if v < 0],
            'higher_coordinates': [k for k, v in delta.items() if v > 0]}


def envelope(lines):
    """Complete exact lower envelope of a + rho*b, rho >= 0."""
    names = sorted(lines)
    crossings, knots = [], {Fraction(0)}
    for i, left in enumerate(names):
        for right in names[i + 1:]:
            a, b = lines[left]
            c, d = lines[right]
            if b == d:
                crossings.append({'left': left, 'right': right,
                                  'relation': 'identical' if a == c else 'parallel',
                                  'rho': None})
                continue
            root = Fraction(c - a, b - d)
            crossings.append({'left': left, 'right': right,
                              'relation': 'crossing', 'rho': ratio(root),
                              'in_nonnegative_domain': root >= 0})
            if root >= 0:
                knots.add(root)

    def minimum(at):
        values = {name: Fraction(a) + at * b for name, (a, b) in lines.items()}
        value = min(values.values())
        return sorted(name for name, cost in values.items() if cost == value), value

    knots = sorted(knots)
    intervals = []
    for i, lower in enumerate(knots):
        upper = knots[i + 1] if i + 1 < len(knots) else None
        at = (lower + upper) / 2 if upper is not None else lower + 1
        winners, _ = minimum(at)
        if intervals and intervals[-1]['methods'] == winners:
            intervals[-1]['upper'] = upper
        else:
            intervals.append({'lower': lower, 'upper': upper, 'methods': winners})

    # Intersections that do not change the winning line are still retained in
    # pair_crossings. Equalities on the envelope are reported separately.
    points = []
    for at in knots:
        winners, value = minimum(at)
        if at == 0 or len(winners) > 1 or any(s['lower'] == at for s in intervals):
            points.append({'rho': ratio(at), 'methods': winners,
                           'cost': ratio(value)})
    return {'lines': {name: {'nonconsumer': a, 'consumer': b}
                      for name, (a, b) in sorted(lines.items())},
            'open_intervals': [{'lower': ratio(s['lower']), 'upper': ratio(s['upper']),
                                'methods': s['methods']} for s in intervals],
            'boundary_points': points, 'pair_crossings': crossings}


def analyze(run, out):
    manifest = read(run / 'manifest.json')
    summary = read(run / 'summary.json')
    raw = (run / 'completed_units.jsonl').read_bytes()
    assert summary['status'] == 'PASS'
    assert manifest['stage'] == summary['stage'] == 'DEVELOPMENT'
    assert digest(raw) == summary['completed_units_sha256']
    assert digest((run / 'manifest.json').read_bytes()) == summary['manifest_sha256']
    for relative, expected in manifest['source_hashes'].items():
        assert digest((run / 'sources' / relative).read_bytes()) == expected
    units = [json.loads(line) for line in raw.splitlines()]
    assert len(units) == summary['units']
    rows = [row for row in units if row.get('kind') in (
        'primary_delivery', 'secondary_delivery')]
    groups, outputs = defaultdict(list), defaultdict(set)
    for row in rows:
        assert row['status'] == 'DELIVERED', 'No equal-service ranking for an incomplete stream.'
        assert row['invoice']['consumer_units'] == sum(
            sum(values.values()) for stage, values in row['invoice']['by_stage'].items()
            if is_consumer(stage))
        vector(row)
        groups[row['stream'], row['recipient'], row['method']].append(row)
        outputs[row['stream'], row['request_index']].add(row['output'])
    assert all(len(values) == 1 for values in outputs.values())
    cells, requests, prefixes = [], [], []
    for stream, recipient in sorted({key[:2] for key in groups}):
        seqs = {key[2]: sorted(seq, key=lambda r: r['request_index'])
                for key, seq in groups.items() if key[:2] == (stream, recipient)}
        for seq in seqs.values():
            assert [r['request_index'] for r in seq] == list(range(1, 7))
        pseq, eseq = seqs['P-REUSE'], seqs['O-ENUM-RECEIVER']
        ptotal, etotal = Counter(), Counter()
        for p, e in zip(pseq, eseq):
            pv, ev = vector(p), vector(e)
            ptotal.update(pv)
            etotal.update(ev)
            context = {'stream': stream, 'recipient': recipient,
                       'request_index': p['request_index']}
            requests.append(dict(context, ordinary_vector=dict(ev), portfolio_vector=dict(pv),
                                 **compare(ev, pv)))
            prefixes.append(dict(context, **compare(etotal, ptotal)))
        lines = {}
        all_vectors = {}
        for method, seq in seqs.items():
            total = sum(row['invoice']['total_units'] for row in seq)
            consumer = sum(row['invoice']['consumer_units'] for row in seq)
            assert total >= consumer >= 0
            lines[method] = (total - consumer, consumer)
            pooled = Counter()
            for row in seq:
                pooled.update(vector(row))
            all_vectors[method] = dict(pooled)
        full_frontier = envelope(lines)
        ordinary_frontier = envelope({name: line for name, line in lines.items()
                                      if name.startswith('O-')})
        pareto_dominators = []
        pa, pb = lines['P-REUSE']
        for name, (a, b) in sorted(lines.items()):
            if name != 'P-REUSE' and a <= pa and b <= pb and (a < pa or b < pb):
                pareto_dominators.append(name)
        cells.append({'stream': stream, 'recipient': recipient,
                      'ordinary_vector': dict(etotal), 'portfolio_vector': dict(ptotal),
                      'all_method_vectors': all_vectors, **compare(etotal, ptotal),
                      'all_method_recipient_price_envelope': full_frontier,
                      'ordinary_recipient_price_envelope': ordinary_frontier,
                      'portfolio_two_coordinate_dominators': pareto_dominators})

    result = {'schema': 'value_logic.rp3bb.fixed-path-prices.v1',
              'stage': 'DEVELOPMENT', 'analysis_selection': 'POST_EXPOSURE',
              'created_utc': datetime.now(timezone.utc).isoformat(),
              'command': sys.argv, 'input_run': str(run),
              'input_manifest_sha256': summary['manifest_sha256'],
              'input_completed_units_sha256': summary['completed_units_sha256'],
              'source_hashes': manifest['source_hashes'],
              'scope': 'Reprice fixed successful invoice vectors only. No new policy, trace, governor completion, hardware time, arbitrary stage-specific price or population inference.',
              'price_family': 'C_rho = total - consumer + rho*consumer, rho >= 0. Common source and publication costs follow the declared consumer partition.',
              'dominance_theorem': 'If every pooled category count in e is no larger than in p, dot(w,e) <= dot(w,p) for all w >= 0; strict exactly when some strictly lower coordinate has positive weight.',
              'cells': cells, 'request_comparisons': requests, 'prefix_comparisons': prefixes,
              'request_exceptions': [row for row in requests
                                     if not row['left_componentwise_le_right']],
              'prefix_exceptions': [row for row in prefixes
                                    if not row['left_componentwise_le_right']]}
    out.mkdir(parents=True, exist_ok=False)
    (out / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    write(out / 'prices.json', result)
    write(out / 'files.sha256.json', {p.name: digest(p.read_bytes()) for p in out.iterdir()
                                    if p.is_file()})
    print(json.dumps({'cells': len(cells), 'request_pairs': len(requests),
                      'all_streams_category_dominated': all(c['left_componentwise_le_right'] for c in cells),
                      'request_exceptions': [{k: row[k] for k in ('stream', 'recipient', 'request_index', 'higher_coordinates')}
                                             for row in result['request_exceptions']],
                      'prefix_exceptions': len(result['prefix_exceptions']),
                      'envelopes': [{'stream': c['stream'], 'recipient': c['recipient'],
                                     'open_intervals': c['all_method_recipient_price_envelope']['open_intervals'],
                                     'boundary_points': c['all_method_recipient_price_envelope']['boundary_points'],
                                     'portfolio_dominators': c['portfolio_two_coordinate_dominators']}
                                    for c in cells]}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    analyze(args.run, args.out)
