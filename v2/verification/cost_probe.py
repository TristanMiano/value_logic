"""Small F11 instrumentation probe, not F12's amortized cost study.

Single observations on one potentially unstable host are retained verbatim.
Plain numerical answers and request-checked receipts have different guarantees.
The ordinary producer can use the very same native emitter/checker; this probe
does not manufacture an independent weaker checked competitor.
"""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import platform
import sys
from time import perf_counter_ns

from .model import Evidence, Query
from .ordinary import analytic_bound
from .producer import produce
from .reference import reference
from .receipts import make_receipt, receive_receipt
from .reuse import reuse


def timed(function, *args):
    start = perf_counter_ns()
    result = function(*args)
    return result, perf_counter_ns()-start


def packed_metrics(payload):
    wire = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('utf-8')
    proof = payload['proof']
    return {'receipt_bytes_including_source': len(wire),
            'proof_steps': len(proof['steps']), 'term_dag_nodes': len(proof['terms'])}


def report():
    cases = (
        Evidence(revision='cost-none'),
        Evidence(Q(0), Q(0), Q(0), Q(0), 'cost-exact'),
        Evidence(Q(0), Q(0), revision='cost-joint'),
        Evidence(beta=Q(0), revision='cost-beta'),
        Evidence(gamma=Q(0), revision='cost-gamma'),
        Evidence(Q(1, 4), Q(1, 16), Q(1, 64), Q(1, 4), 'cost-mixed'),
    )
    observations = []
    for evidence in cases:
        for action in ('T1', 'T2', 'R'):
            query = Query(action)
            ordinary, ordinary_ns = timed(analytic_bound, evidence, query)
            semantic, reference_ns = timed(reference, evidence, query)
            outcome, produce_ns = timed(produce, evidence, query)
            if ordinary != semantic.maximum or outcome.upper_bound != ordinary:
                raise AssertionError('Instrumentation case has inconsistent bounds.')
            payload, pack_ns = timed(make_receipt, evidence, query, outcome)
            # Check the actual bound, even for an original zero-budget refusal.
            _, receive_ns = timed(receive_receipt, evidence, Query(action, ordinary), payload)
            observations.append({
                'revision': evidence.revision, 'action': action,
                'producer_status': outcome.status, 'bound': str(ordinary),
                'basis_checks': outcome.basis_checks, **packed_metrics(payload),
                'stage_ns': {'ordinary_numeric_answer': ordinary_ns,
                             'independent_reference': reference_ns,
                             'native_generation_and_request_check': produce_ns,
                             'receipt_validation_and_pack': pack_ns,
                             'receipt_decode_and_current_request_check': receive_ns},
            })
    old = cases[1]
    query = Query('T1')
    payload = make_receipt(old, query, produce(old, query))
    current = Evidence(beta=Q(0), gamma=Q(8, 85), revision='cost-boundary')
    reused, reuse_ns = timed(reuse, current, query, payload)
    fresh, fresh_ns = timed(produce, current, query)
    if reused.upper_bound != Q(1, 1360) or fresh.upper_bound != 0:
        raise AssertionError('Selected-proof reuse control changed.')
    return {
        'scope': '18 fixed-query snapshots and one reuse boundary; descriptive F11 instrumentation',
        'python': sys.version, 'platform': platform.platform(),
        'timing_unit': 'nanoseconds from perf_counter_ns; single sequential observations',
        'cache_condition': 'Shared process; prior reference, producer and checker calls can warm caches. No cache-reset comparison.',
        'comparison_limit': 'Numeric-only answers lack native receipts; same-guarantee ordinary methods may use the same emitter/checker.',
        'costs_not_measured': ['amortized sequences', 'alternative-retention selection',
                               'cold process import/startup', 'empirical premise generation',
                               'distribution of runtime across repetitions or hosts'],
        'observations': observations,
        'reuse_boundary': {'old_receipt_bytes': packed_metrics(payload)['receipt_bytes_including_source'],
                           'row_candidate_checks': reused.row_candidate_checks,
                           'replacement_count': reused.replacement_count,
                           'reused_bound': str(reused.upper_bound), 'fresh_bound': str(fresh.upper_bound),
                           'reused_status': reused.status, 'fresh_status': fresh.status,
                           'reuse_ns': reuse_ns, 'fresh_generation_ns': fresh_ns},
        'novelty': 'NOT YET SUPPORTED', 'status': 'PASS',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    result = report()
    if args.json:
        args.json.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    metrics = result['observations']
    summary = {k: v for k, v in result.items() if k != 'observations'}
    summary['receipt_byte_range'] = [min(x['receipt_bytes_including_source'] for x in metrics),
                                     max(x['receipt_bytes_including_source'] for x in metrics)]
    summary['proof_step_range'] = [min(x['proof_steps'] for x in metrics), max(x['proof_steps'] for x in metrics)]
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
