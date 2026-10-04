"""F12 exact finite sweep: native producer versus separate task execution.

Outputs only enumerated evidence. A completed shard never implies continuum
coverage or novelty. The oracle does not decode or normalize returned proofs.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from v2.checks import f07_soundness as A
from . import native, receipts
from .model import Query
from .producer import produce
from .reference import reference, feasible, task_losses
from .ordinary import analytic_bound
from .workloads import ACTIONS, SEED, sources


def check_source(evidence):
    records = []
    for action in ACTIONS:
        query = Query(action)
        generated = produce(evidence, query)
        semantic = reference(evidence, query)
        ordinary = analytic_bound(evidence, query)
        if generated.proof is None or generated.upper_bound != semantic.maximum or ordinary != semantic.maximum:
            raise AssertionError((evidence, action, 'bound disagreement', generated.upper_bound, semantic.maximum, ordinary))
        point = semantic.witness
        actual = task_losses(point)
        if not feasible(evidence, point) or actual[action]-actual['F'] != semantic.maximum:
            raise AssertionError('Reference attainer failed direct full-source execution.')
        ctx = native.context(evidence)
        threshold = Query(action, semantic.maximum)
        A.receive(ctx, generated.proof, native.request(ctx, threshold))
        try:
            A.receive(ctx, generated.proof, native.request(ctx, Query(action, semantic.maximum-Q(1, 1000003))))
        except A.AuditError:
            pass
        else:
            raise AssertionError('A stricter-than-proven request was accepted.')
        accepted = generated.status == 'certified'
        if accepted != (semantic.maximum <= 0):
            raise AssertionError('Zero-budget decision disagrees with exact semantics.')
        # Round-trip every scientific source, not just selected successes.
        wire = receipts.loads(json.dumps(receipts.make_receipt(evidence, query, generated)))
        root = receipts.receive_receipt(evidence, threshold, wire)
        if root.budget != semantic.maximum:
            raise AssertionError('Receipt transport changed the checked bound.')
        records.append({'action': action, 'bound': str(semantic.maximum),
                        'decision': 'certified' if accepted else 'full_source_refuted',
                        'point': [str(x) for x in point], 'steps': len(generated.proof.steps),
                        'basis_checks': generated.basis_checks})
    return records


def sweep(family, start=0, stop=None, progress=None):
    population = sources(family)
    stop = len(population) if stop is None else stop
    if type(start) is not int or type(stop) is not int or not 0 <= start < stop <= len(population):
        raise ValueError('Invalid nonempty shard interval.')
    counts = Counter()
    digest = hashlib.sha256()
    rows = []
    for i in range(start, stop):
        evidence = population[i]
        if progress is not None:
            progress({'event': 'begin_source', 'family': family, 'index': i})
        answers = check_source(evidence)
        row = {'index': i, 'bounds': [None if x is None else str(x) for x in evidence.bounds],
               'answers': answers}
        rows.append(row)
        digest.update(json.dumps(row, sort_keys=True, separators=(',', ':')).encode())
        counts.update(a['decision'] for a in answers)
    return {'status': 'PASS', 'family': family, 'seed': SEED, 'start': start, 'stop': stop,
            'population_sources': len(population), 'checked_sources': stop-start,
            'queries': 3*(stop-start), 'threshold_checks': 6*(stop-start),
            'receipt_roundtrips': 3*(stop-start), 'decisions': dict(counts),
            'exact_rows_sha256': digest.hexdigest(), 'rows': rows,
            'scope': 'enumerated development cases only; no held-out or continuum claim'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--family', choices=('grid', 'rational', 'boundary', 'offgrid'), required=True)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--stop', type=int)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    data = sweep(args.family, args.start, args.stop,
                 lambda item: print(json.dumps(item), flush=True))
    args.json.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k != 'rows'}, sort_keys=True))


if __name__ == '__main__':
    main()
