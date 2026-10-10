#!/usr/bin/env python3
"""Fixed post-primary ordinary-pruning development comparison and paid failures.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. No final challenge.
The observer/writer reuses the original artifact machinery; worker source v5
and its completed primary run remain immutable. See contract amendment 5.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import importlib.util
import json
import sys
import traceback

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name, filename):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R = load('_rp3bb_delivery_run', '05_certificate_delivery_run.py')
X = load('_rp3bb_pruned_delivery_service', '05_certificate_delivery_pruned_service.py')
assert X.S is R.S and X.PRUNE.E is X.S.A, 'One owned worker and evidence module required.'


class Writer(R.Writer):
    def __init__(self, destination, args):
        super().__init__(destination, 'secondary-pruning', args)
        relative = 'v3/checks/05_certificate_delivery_pruned_run.py'
        content = (ROOT / relative).read_bytes()
        target = self.out / 'sources' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        self.source_hashes[relative] = R.sha(content)
        self.manifest.update(
            methods=list(X.METHODS), recipients=['fresh'],
            source_hashes=self.source_hashes, exposure='Post-primary DEVELOPMENT strengthening.',
            contract='service_contract_amendment_5.json', delivery_units=144,
            planned_prune_limit_failure_units=4, all_primary_worker_sources_unchanged=True,
            adapter_version=X.VERSION, pruner_version=X.PRUNE.VERSION,
            prune_limit_steps=X.PRUNE.MAX_DEPENDENCY_STEPS,
            unused_old_recipe_retention='Only P-REUSE and O-ADD-PORTFOLIO retain old inputs.',
            truth_reference={'primary_v5_manifest_sha256':
                '173291f1ba26a65ac0ef9d68d54c017c12d47bc7853c6ba89bb971fdade16cca',
                'primary_v5_completed_units_sha256':
                '555d0af18e958053f06b14940e6a725d28514877191a0982d976c91eb210254e'})
        self.manifest_hash = R.write_json(self.out / 'manifest.json', self.manifest)


def secondary(writer, args):
    for stream in R.FAMILY.streams():
        for method in X.METHODS:
            worker = X.make_session(method, stream, writer.expected_source_record)
            for case in stream.edits:
                row = worker.deliver(case.frame, case.witness, case.bound, budget=args.budget)
                row.update(kind='secondary_delivery', case=case.name)
                writer.save(row)
                R.assert_service(writer, case, row)
                writer.check(worker.current_receipt(row['request_id']) is not None
                             if row['status'] == 'DELIVERED' else worker.current_receipt(row['request_id']) is None,
                             'Current receipt disagrees with paid publication.')
            if method == X.METHOD:
                previous_id = row['request_id']
                worker.prune_limit_steps = 1
                case = stream.edits[2]
                denied = worker.deliver(case.frame, case.witness, case.bound, budget=args.budget)
                denied.update(kind='secondary_prune_limit_failure', case=case.name)
                writer.save(denied)
                writer.check(denied['status'] == 'NO_CURRENT_CERTIFICATE', 'One-step pruning cap delivered.')
                writer.check(denied['error']['type'] == 'PruneLimit', 'Different failure obscured the pruning boundary.')
                writer.check(denied['invoice']['total_units'] > 113, 'Paid export/pruning prefix was discarded.')
                writer.check(worker.manager is None and worker.receiver is None, 'Failed warm state survived.')
                writer.check(worker.current_receipt(previous_id) is None, 'Stale receipt remained current.')
                writer.check(worker.current_receipt(denied['request_id']) is None, 'Failed receipt was published.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--budget', type=int, default=R.S.SUCCESS_BUDGET)
    args = parser.parse_args()
    writer = Writer(args.out, args)
    error = None
    try:
        secondary(writer, args)
        writer.check(len(writer.units) == 148, 'Declared units not completed.')
        writer.stable()
    except BaseException as failure:
        error = {'type': type(failure).__name__, 'message': str(failure),
                 'traceback': traceback.format_exc()}
    result = writer.finish(error)
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
