"""Finite denominator-ordered search for a simpler F11 reuse miss.

This studies one old source, beta=0, action T1 and gamma in [0,1]. It is
not a globally minimal counterexample claim or a soundness failure. Exact
semantics screens false requests before the expensive reconstruction; this
search is not a benchmark strategy and its oracle is not available to reuse.
"""
import argparse
from fractions import Fraction as Q
import json
from math import gcd
from pathlib import Path

from . import receipts
from .model import Evidence, Query
from .producer import produce
from .reference import reference
from .reuse import reuse


def candidates(max_denominator=32):
    if type(max_denominator) is not int or not 1 <= max_denominator <= 32:
        raise ValueError('This search is bounded by denominator 32.')
    yield Q(0)
    yield Q(1)
    for denominator in range(2, max_denominator+1):
        for numerator in range(1, denominator):
            if gcd(numerator, denominator) == 1:
                yield Q(numerator, denominator)


def search(max_denominator=32, progress=None):
    query = Query('T1')
    old = Evidence(0, 0, 0, 0, 'minimization-origin')
    saved = receipts.make_receipt(old, query, produce(old, query))
    rows = []
    for cap in candidates(max_denominator):
        current = Evidence(beta=0, gamma=cap, revision=f'gamma-{cap}')
        maximum = reference(current, query).maximum
        row = {'gamma': str(cap), 'reference_bound': str(maximum)}
        if progress:
            progress({'event': 'candidate', 'index': len(rows), 'gamma': str(cap)})
        if maximum > 0:
            row['outcome'] = 'screened_semantically_false'
            rows.append(row)
            continue
        result = reuse(current, query, saved)
        row['reused_bound'] = None if result.upper_bound is None else str(result.upper_bound)
        row['reused_status'] = result.status
        row['outcome'] = 'missed_true_request' if result.status != 'certified' else 'certified'
        rows.append(row)
        if result.proof is not None:
            payload = receipts.make_receipt(current, query, result)
            receipts.receive_receipt(current, Query('T1', result.upper_bound), payload)
            if result.upper_bound < maximum:
                raise AssertionError('Reconstruction would be unsound, not merely incomplete.')
        if row['outcome'] == 'missed_true_request':
            fresh = produce(current, query)
            if fresh.status != 'certified' or fresh.upper_bound != maximum:
                raise AssertionError('Fresh native proof did not establish the true request.')
            return {'status': 'FOUND', 'declared_max_denominator': max_denominator,
                    'witness': row, 'fresh_bound': str(fresh.upper_bound),
                    'searched_candidates': len(rows),
                    'native_reconstructions': sum(r['outcome'] != 'screened_semantically_false' for r in rows),
                    'rows': rows,
                    'scope': 'First miss in reduced denominator/numerator order on this one-dimensional family; all lower denominators and earlier numerators were screened exactly. Not global minimality or a kernel failure.'}
    return {'status': 'NOT_FOUND', 'declared_max_denominator': max_denominator,
            'searched_candidates': len(rows), 'rows': rows,
            'scope': 'No miss in this declared finite family only.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-denominator', type=int, default=32)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    data = search(args.max_denominator, lambda x: print(json.dumps(x), flush=True))
    args.json.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k != 'rows'}, sort_keys=True))


if __name__ == '__main__':
    main()
