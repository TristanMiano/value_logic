"""Finite F12 revision/reconstruction differential controls."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import json
from pathlib import Path

from v2.checks import f07_soundness as A
from . import native, receipts
from .model import Query
from .producer import produce
from .reference import reference
from .reuse import reuse
from .workloads import ACTIONS, revisions


def check_revision(change, action):
    query = Query(action)
    original = produce(change.old, query)
    payload = receipts.make_receipt(change.old, query, original)
    try:
        receipts.receive_receipt(change.new, Query(action, Q(10)), payload)
    except receipts.ReceiptError:
        pass
    else:
        raise AssertionError('A stale revision was accepted without reconstruction.')
    old_max = reference(change.old, query).maximum
    new_max = reference(change.new, query).maximum
    if change.relation == 'same' and new_max != old_max:
        raise AssertionError('Version alone changed semantic validity.')
    if change.relation == 'subset' and new_max > old_max:
        raise AssertionError('Source strengthening increased the robust maximum.')
    if change.relation == 'superset' and new_max < old_max:
        raise AssertionError('Source relaxation decreased the robust maximum.')
    fresh = produce(change.new, query)
    rebuilt = reuse(change.new, query, payload)
    if fresh.upper_bound != new_max:
        raise AssertionError('Fresh query differs from independent revision reference.')
    if rebuilt.proof is not None:
        if rebuilt.upper_bound < new_max:
            raise AssertionError('Reconstruction is below a full-source counterexample.')
        ctx = native.context(change.new)
        A.receive(ctx, rebuilt.proof, native.bound_request(ctx, action, rebuilt.upper_bound))
    if rebuilt.status == 'certified' and new_max > 0:
        raise AssertionError('Reconstruction falsely certifies the request.')
    return {'revision': change.name, 'action': action, 'relation': change.relation,
            'old_bound': str(old_max), 'fresh_bound': str(new_max),
            'reused_bound': None if rebuilt.upper_bound is None else str(rebuilt.upper_bound),
            'reused_status': rebuilt.status, 'reason': rebuilt.reason,
            'true_request': new_max <= 0,
            'missed_true_request': new_max <= 0 and rebuilt.status != 'certified',
            'gap': None if rebuilt.upper_bound is None else str(rebuilt.upper_bound-new_max),
            'row_candidates': rebuilt.row_candidate_checks,
            'proof_steps': 0 if rebuilt.proof is None else len(rebuilt.proof.steps)}


def report(start=0, stop=None, progress=None):
    cases = revisions()
    stop = len(cases) if stop is None else stop
    if type(start) is not int or type(stop) is not int or not 0 <= start < stop <= len(cases):
        raise ValueError('Invalid revision interval.')
    rows = []
    for i in range(start, stop):
        for action in ACTIONS:
            if progress:
                progress({'event': 'begin_revision', 'index': i, 'action': action})
            rows.append(check_revision(cases[i], action))
    return {'status': 'PASS', 'start': start, 'stop': stop, 'queries': len(rows),
            'stale_rejections': len(rows), 'missed_true_requests': sum(r['missed_true_request'] for r in rows),
            'strict_reuse_gaps': sum(r['gap'] is not None and Q(r['gap']) > 0 for r in rows),
            'reasons': dict(Counter(r['reason'] for r in rows)), 'rows': rows,
            'scope': '24 declared revision pairs only; no optimality or novelty claim'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--stop', type=int)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    data = report(args.start, args.stop, lambda x: print(json.dumps(x), flush=True))
    args.json.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k != 'rows'}, sort_keys=True))


if __name__ == '__main__':
    main()
