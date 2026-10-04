"""Versioned F12 extension: fixed-origin receipts and selected coefficients."""
from time import perf_counter_ns
_START = perf_counter_ns()
import argparse
from dataclasses import asdict
import json
from pathlib import Path

from . import selected_cache, receipts
from .model import Query
from .producer import produce
from .sequence_cost import Strategy, compact, run

_IMPORT_NS = perf_counter_ns()-_START
STRATEGIES = ('fresh', 'catalogue', 'anchored-reuse', 'selected-fresh')


class Anchored(Strategy):
    def __init__(self):
        super().__init__('reuse')

    def answer(self, evidence, query):
        old = self.saved.get(query.action)
        old_size = self.saved_sizes.get(query.action)
        outcome, stages, counters, wire = super().answer(evidence, query)
        if old is not None:
            # Always rebuild from the originally charged seed receipt. A new
            # output is transmitted, not retained or silently made the seed.
            self.saved[query.action] = old
            self.saved_sizes[query.action] = old_size
            self.output_is_retained = False
        return outcome, stages, counters, wire


class SelectedFresh(Strategy):
    def __init__(self):
        super().__init__('fresh')
        self.selected = {}

    def answer(self, evidence, query):
        self.output_is_retained = False
        stages = {}
        counters = {'fresh_calls': 0, 'catalogue_builds': 0, 'reuse_calls': 0,
                    'fallback_calls': 0, 'basis_checks': 0, 'template_evaluations': 0,
                    'row_candidates': 0, 'selected_attempts': 0, 'selected_hits': 0}
        def measured(label, operation):
            start = perf_counter_ns()
            result = operation()
            stages[label] = perf_counter_ns()-start
            return result
        outcome = None
        cached = self.selected.get(query.action)
        if cached is not None:
            counters['selected_attempts'] = 1
            outcome = measured('selected_screen_emit_ns', lambda: selected_cache.replay(evidence, query, cached))
            counters['template_evaluations'] = outcome.feasible_bases
            if outcome.status == 'certified':
                counters['selected_hits'] = 1
            else:
                counters['fallback_calls'] = 1
        if outcome is None or outcome.status != 'certified':
            outcome = measured('fresh_generation_ns', lambda: produce(evidence, query))
            counters['fresh_calls'] = 1
            counters['basis_checks'] = outcome.basis_checks
            def store_coefficients():
                stored = selected_cache.from_outcome(evidence, query, outcome)
                self.selected[query.action] = stored
                self.catalogue_sizes[query.action] = len(compact(asdict(stored)).encode())
            measured('selected_storage_encoding_ns', store_coefficients)
        wire = None
        if outcome.proof is not None:
            payload = measured('receipt_validate_pack_ns', lambda: receipts.make_receipt(evidence, query, outcome))
            wire = measured('receipt_encode_ns', lambda: compact(payload))
            measured('receiver_decode_check_ns', lambda: receipts.receive_receipt(
                evidence, Query(query.action, outcome.upper_bound), receipts.loads(wire)))
        return outcome, stages, counters, wire


def factory(name):
    if name == 'anchored-reuse':
        return Anchored()
    if name == 'selected-fresh':
        return SelectedFresh()
    return Strategy(name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strategy', choices=STRATEGIES, required=True)
    parser.add_argument('--sequence', choices=('fixed-directions', 'withdrawals', 'stable-revisions'), required=True)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    data = run(args.strategy, args.sequence, progress=lambda x: print(json.dumps(x), flush=True), strategy_factory=factory)
    data['module_import_ns'] = _IMPORT_NS
    data['experiment_version'] = 'F12-optional-cost-v2'
    args.json.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k != 'rows'}, sort_keys=True))


if __name__ == '__main__':
    main()
