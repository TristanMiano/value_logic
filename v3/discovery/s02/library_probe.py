"""DEVELOPMENT: lazy witness retention, same native solver/trust scope.

Codex (GPT-6), 2026-10-11. No novelty or statistical timing claim.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback

from revision_probe import Engine, InvalidEdit, run, streams


class LazyEngine(Engine):
    def __init__(self, n, capacity, max_active=128):
        super().__init__(n, 'native')
        assert 1 <= capacity <= max_active
        self.capacity, self.max_active = capacity, max_active
        self.library, self.activations = [], []

    def edit(self, parent, op, cid, raw=()):
        if op in ('add', 'on') and len(self.active) >= self.max_active:
            raise InvalidEdit('Active formula cap')
        super().edit(parent, op, cid, raw)
        if op == 'off':
            if cid in self.core:
                self.missing += 1
        else:
            self.activations.append(cid)
            if cid in self.core:
                self.missing -= 1
        if len(self.activations) >= 2*self.max_active:
            self.activations = list(self.active)
            for entry in self.library:
                entry['cursor'] = 0
            self.counts['rebases'] += 1
            self.counts['rebase_ids'] += len(self.activations)
        self.counts['peak_activation_entries'] = max(self.counts['peak_activation_entries'],len(self.activations))

    def answer(self):
        if self.core and self.missing == 0:
            self.counts['requests'] += 1
            self.counts['support_hits'] += 1
            return 0
        for i, entry in enumerate(self.library):
            self.counts['witness_attempts'] += 1
            while entry['cursor'] < len(self.activations):
                cid = self.activations[entry['cursor']]
                self.counts['activation_membership_tests'] += 1
                if cid in self.active and not self.truth(self.registry[cid], entry['assignment']):
                    self.counts['blocked_attempts'] += 1
                    break
                entry['cursor'] += 1
                self.counts['cursor_advances'] += 1
            else:
                self.library.insert(0, self.library.pop(i))
                self.counts['requests'] += 1
                self.counts['witness_hits'] += 1
                return 1
        # Base native answer performs an independent full SAT witness check.
        answer = super().answer()
        if answer:
            model = self.solver.get_model() or []
            assignment = sum(1 << (v-1) for v in model if 0 < v <= self.n)
            self.library.insert(0, dict(assignment=assignment, cursor=len(self.activations)))
            if len(self.library) > self.capacity:
                self.library.pop()
                self.counts['evictions'] += 1
            self.counts['admitted_witnesses'] += 1
            self.counts['peak_witnesses'] = max(self.counts['peak_witnesses'], len(self.library))
        else:
            self.core, self.missing = set(self.active), 0
            self.counts['support_retained_ids'] += len(self.core)
        return answer


def alternations(n):
    clauses = []
    for i in range(1,n):
        clauses.extend(([-i,i+1],[i,-(i+1)]))
    positive, negative = len(clauses), len(clauses)+1
    clauses.extend(([1],[-1]))
    patches = []
    # Every four operations visits SAT(ones), SAT(either), SAT(zeros), UNSAT.
    for _ in range(96):
        patches.extend((['off',negative,[]],['off',positive,[]],
                        ['on',negative,[]],['on',positive,[]]))
    return dict(kind='declared_two_model_alternation', n=n,
                initial=[[i,c] for i,c in enumerate(clauses)],patches=patches)


def run_lazy(stream, capacity):
    start = time.perf_counter_ns()
    engine = LazyEngine(stream['n'], capacity, max_active=128)
    try:
        for cid,clause in stream['initial']:
            engine.edit(engine.version, 'add', cid, clause)
        answers = [engine.answer()]
        for op,cid,clause in stream['patches']:
            engine.edit(engine.version, op, cid, clause)
            answers.append(engine.answer())
        counts = dict(engine.counts)
    finally:
        engine.close()
    return dict(mode=f'lazy_{capacity}',elapsed_ns=time.perf_counter_ns()-start,
                counts=counts,answers=answers)


def main(output):
    assert not output.exists()
    started = time.monotonic_ns()
    result = dict(status='running', evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                  start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (Path(__file__),Path(__file__).with_name('revision_probe.py'))},
                  timing_scope='warm streams; same limits as revision01; diagnostic counts are not equal-cost primitives')
    try:
        cohort = streams(8402)+[alternations(n) for n in (8,12,20)]
        result['additional_streams'] = cohort[9:]
        result['base_streams_record'] = 'revision01.json'
        rows = []
        for index,stream in enumerate(cohort):
            expected = None
            modes = ['fresh','native','native_delta',1,2,4,8]
            for repetition in range(2):
                for mode in modes if repetition == 0 else reversed(modes):
                    row = run_lazy(stream,mode) if type(mode) is int else run(stream,mode)
                    if expected is None:
                        expected = row['answers']
                    assert row['answers'] == expected
                    row['answers'] = ''.join(map(str,row['answers']))
                    row.update(stream=index,kind=stream['kind'],n=stream['n'],repetition=repetition)
                    rows.append(row)
        result.update(status='complete',rows=rows,answer_comparisons=sum(len(r['answers']) for r in rows))
    except Exception:
        result.update(status='failed',failure=traceback.format_exc())
        raise
    finally:
        result['elapsed_ns'] = time.monotonic_ns()-started
        result['end_utc'] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ('rows','additional_streams')}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
