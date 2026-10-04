"""F12 process-isolated sequence comparison at a common receipt guarantee."""
from time import perf_counter_ns
_IMPORT_START = perf_counter_ns()
import argparse
from collections import Counter
from dataclasses import asdict
from fractions import Fraction as Q
import json
from pathlib import Path
import platform
import sys

from . import catalogue, receipts
from .model import Query
from .producer import produce
from .reuse import reuse
from .reference import reference
from .ordinary import analytic_bound
from .workloads import sequence

_IMPORT_NS = perf_counter_ns()-_IMPORT_START
STRATEGIES = ('fresh', 'catalogue', 'reuse', 'reuse-fallback')


def compact(value):
    return json.dumps(value, default=str, ensure_ascii=True, sort_keys=True, separators=(',', ':'))


def schema_key(evidence, query):
    return query.action, tuple(x is not None for x in evidence.bounds)


class Strategy:
    """One fixed strategy, with no access to oracle values or future events."""
    def __init__(self, name):
        if name not in STRATEGIES:
            raise ValueError('Unknown checked-answer strategy.')
        self.name = name
        self.catalogues = {}
        self.catalogue_sizes = {}
        self.saved = {}
        self.saved_sizes = {}

    def answer(self, evidence, query):
        stages = {}
        counters = {'fresh_calls': 0, 'catalogue_builds': 0, 'reuse_calls': 0,
                    'fallback_calls': 0, 'basis_checks': 0, 'template_evaluations': 0,
                    'row_candidates': 0}
        def measured(label, operation):
            start = perf_counter_ns()
            result = operation()
            stages[label] = stages.get(label, 0)+perf_counter_ns()-start
            return result
        def fresh():
            value = measured('fresh_generation_ns', lambda: produce(evidence, query))
            counters['fresh_calls'] += 1
            counters['basis_checks'] += value.basis_checks
            return value
        if self.name == 'catalogue':
            key = schema_key(evidence, query)
            if key not in self.catalogues:
                stored = measured('catalogue_build_ns', lambda: catalogue.build(evidence, query))
                self.catalogues[key] = stored
                self.catalogue_sizes[key] = measured('catalogue_storage_encoding_ns', lambda: len(compact(asdict(stored)).encode()))
                counters['catalogue_builds'] += 1
                counters['basis_checks'] += stored.build_basis_checks
            selected = measured('catalogue_select_emit_ns', lambda: catalogue.select(evidence, query, self.catalogues[key]))
            counters['template_evaluations'] += selected.template_evaluations
            outcome = selected.outcome
        elif self.name in ('reuse', 'reuse-fallback') and query.action in self.saved:
            outcome = measured('reconstruction_ns', lambda: reuse(evidence, query, self.saved[query.action]))
            counters['reuse_calls'] += 1
            counters['row_candidates'] += outcome.row_candidate_checks
            if self.name == 'reuse-fallback' and outcome.status != 'certified':
                counters['fallback_calls'] += 1
                outcome = fresh()
        else:
            outcome = fresh()
        wire = None
        if outcome.proof is not None:
            payload = measured('receipt_validate_pack_ns', lambda: receipts.make_receipt(evidence, query, outcome))
            wire = measured('receipt_encode_ns', lambda: compact(payload))
            # Every route crosses the same JSON/current-request boundary.
            # Insufficient upper bounds are received at their stated strength,
            # not falsely labeled a certificate of the original zero budget.
            bound_query = Query(query.action, outcome.upper_bound)
            measured('receiver_decode_check_ns', lambda: receipts.receive_receipt(evidence, bound_query, receipts.loads(wire)))
            if self.name in ('reuse', 'reuse-fallback'):
                self.saved[query.action] = payload
                self.saved_sizes[query.action] = len(wire.encode())
        return outcome, stages, counters, wire


def run(strategy_name, sequence_name, cycles=1, progress=None):
    events = sequence(sequence_name, cycles)
    strategy = Strategy(strategy_name)
    rows = []
    cumulative_ns = 0
    loop_start = perf_counter_ns()
    for i, (evidence, query) in enumerate(events):
        if progress:
            progress({'event': 'begin_query', 'index': i, 'revision': evidence.revision, 'action': query.action})
        start = perf_counter_ns()
        request_wire = compact(receipts.request_payload(evidence, query))
        outcome, stages, counters, wire = strategy.answer(evidence, query)
        # Retained archives include each proof's original source. Current input
        # request includes full current evidence. Do not count an output twice
        # when that same serialized object is retained by the strategy.
        retained_receipts = sum(strategy.saved_sizes.values())
        retained_catalogues = sum(strategy.catalogue_sizes.values())
        output_bytes = 0 if wire is None else len(wire.encode())
        transient_output = output_bytes if strategy_name not in ('reuse', 'reuse-fallback') else 0
        current_bytes = len(request_wire.encode())
        elapsed = perf_counter_ns()-start
        cumulative_ns += elapsed
        rows.append({'index': i, 'revision': evidence.revision, 'action': query.action,
                     'status': outcome.status, 'reason': outcome.reason,
                     'bound': None if outcome.upper_bound is None else str(outcome.upper_bound),
                     'operation_ns': elapsed, 'cumulative_ns': cumulative_ns,
                     'stage_ns': stages, 'counters': counters,
                     'request_bytes_including_source': current_bytes, 'output_receipt_bytes': output_bytes,
                     'retained_receipt_bytes_including_old_sources': retained_receipts,
                     'retained_catalogue_bytes': retained_catalogues,
                     'total_live_serialized_bytes': current_bytes+retained_receipts+retained_catalogues+transient_output})
    loop_ns = perf_counter_ns()-loop_start
    reference_start = perf_counter_ns()
    for row, (evidence, query) in zip(rows, events):
        maximum = reference(evidence, query).maximum
        if analytic_bound(evidence, query) != maximum:
            raise AssertionError('Ordinary/reference disagreement in benchmark assessment.')
        if row['bound'] is not None and Q(row['bound']) < maximum:
            raise AssertionError('Strategy returned an unsound upper bound.')
        if row['status'] == 'certified' and maximum > query.budget:
            raise AssertionError('Strategy falsely certified a comparison.')
        row['reference_bound'] = str(maximum)
        row['true_request'] = maximum <= query.budget
        row['missed_true_request'] = row['true_request'] and row['status'] != 'certified'
        row['exact_bound'] = row['bound'] is not None and Q(row['bound']) == maximum
    reference_ns = perf_counter_ns()-reference_start
    total_counters = Counter()
    for row in rows:
        total_counters.update(row['counters'])
    return {'schema': 'F12-sequence-cost-v1', 'status': 'PASS', 'strategy': strategy_name,
            'sequence': sequence_name, 'cycles': cycles, 'queries': len(rows),
            'module_import_ns': _IMPORT_NS, 'strategy_loop_ns': loop_ns,
            'total_operation_ns': cumulative_ns, 'reference_assessment_ns': reference_ns,
            'true_requests': sum(r['true_request'] for r in rows),
            'missed_true_requests': sum(r['missed_true_request'] for r in rows),
            'exact_bounds': sum(r['exact_bound'] for r in rows),
            'peak_total_live_serialized_bytes': max(r['total_live_serialized_bytes'] for r in rows),
            'counters': dict(total_counters), 'rows': rows,
            'python': sys.version, 'platform': platform.platform(),
            'guarantee': 'current checked upper-bound receipt; original request certified only when bound suffices',
            'cache_condition': 'fresh process per run; caches naturally warm within the sequence; no free external setup',
            'timing_scope': 'operation includes setup, request encoding, generation/reconstruction, receipt encoding and receiver; module imports separate; parent wall time also includes reference assessment and report I/O',
            'storage_scope': 'compact JSON-equivalent live source/receipt/catalogue bytes, not Python resident memory',
            'novelty': 'NOT YET SUPPORTED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strategy', choices=STRATEGIES, required=True)
    parser.add_argument('--sequence', choices=('fixed-directions', 'withdrawals', 'stable-revisions'), required=True)
    parser.add_argument('--cycles', type=int, default=1)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    data = run(args.strategy, args.sequence, args.cycles,
               lambda x: print(json.dumps(x), flush=True))
    args.json.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k != 'rows'}, sort_keys=True))


if __name__ == '__main__':
    main()
