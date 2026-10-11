"""DEVELOPMENT S07: explicit-edit SAT evidence, with ordinary controls.

Codex (GPT-6), 2026-10-11. Trusted local MiniSat22 supplies fallback truth;
SAT assignments are independently clause-checked. No external UNSAT proof
authentication claim. Timings are warm installed-runtime stream costs,
including state construction, edits, checks, failed reuse and native calls.
Diagnostic counts are not interchangeable primitive-work tariffs.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import random
import sys
import time
import traceback

if os.environ.get('VL_SAT_DEPS'):
    sys.path.insert(0, os.environ['VL_SAT_DEPS'])
from pysat.solvers import Minisat22


class InvalidEdit(ValueError):
    pass


class Engine:
    def __init__(self, n, mode):
        assert mode in ('fresh', 'full_cache', 'native', 'delta', 'native_delta')
        self.n, self.mode, self.version = n, mode, 0
        self.registry, self.active, self.sat_bits = {}, {}, {}
        self.witness, self.core, self.missing, self.violations = None, set(), 0, 0
        self.counts = Counter()
        self.solver = Minisat22() if mode in ('native', 'native_delta') else None

    def truth(self, clause, assignment):
        self.counts['clause_evaluations'] += 1
        for lit in clause:
            self.counts['literal_tests'] += 1
            if bool(assignment & (1 << (abs(lit)-1))) == (lit > 0):
                return True
        return False

    def edit(self, parent, op, cid, raw=()):
        self.counts['edit_attempts'] += 1
        if type(parent) is not int or parent != self.version or type(cid) is not int or not 0 <= cid < 100000:
            raise InvalidEdit('Wrong parent or ID')
        if op == 'add':
            if cid in self.registry or not isinstance(raw, (tuple, list)) or len(raw) > 4:
                raise InvalidEdit('Recycled ID or bad clause')
            self.counts['admitted_literals'] += len(raw)
            if any(type(lit) is not int or not 0 < abs(lit) <= self.n for lit in raw):
                raise InvalidEdit('Invalid literal')
            clause = tuple(raw)
        elif op == 'off':
            if cid not in self.active:
                raise InvalidEdit('Inactive deletion')
            clause = self.registry[cid]
        elif op == 'on':
            if cid not in self.registry or cid in self.active:
                raise InvalidEdit('Missing or active restoration')
            clause = self.registry[cid]
        else:
            raise InvalidEdit('Unknown operation')
        # Everything above validates before state mutation.
        if op == 'add':
            self.registry[cid] = clause
            if self.solver is not None:
                self.solver.add_clause([-(self.n+1+cid), *clause])
                self.counts['native_clause_literals'] += len(clause)+1
        delta = self.mode in ('delta', 'native_delta')
        if op == 'off':
            del self.active[cid]
            if delta:
                if self.witness is not None:
                    self.violations -= not self.sat_bits.pop(cid)
                if cid in self.core:
                    self.missing += 1
        else:
            self.active[cid] = clause
            if delta:
                if self.witness is not None:
                    satisfied = self.truth(clause, self.witness)
                    self.sat_bits[cid] = satisfied
                    self.violations += not satisfied
                if cid in self.core:
                    self.missing -= 1
        self.version += 1
        self.counts['accepted_edits'] += 1
        self.counts['max_registered_clauses'] = max(self.counts['max_registered_clauses'], len(self.registry))
        self.counts['max_active_clauses'] = max(self.counts['max_active_clauses'], len(self.active))

    def answer(self):
        self.counts['requests'] += 1
        delta = self.mode in ('delta', 'native_delta')
        if delta:
            if self.witness is not None and self.violations == 0:
                self.counts['witness_hits'] += 1
                return 1
            if self.core and self.missing == 0:
                self.counts['support_hits'] += 1
                return 0
        elif self.mode == 'full_cache':
            if self.witness is not None and all(self.truth(c, self.witness) for c in self.active.values()):
                self.counts['witness_hits'] += 1
                return 1
            self.counts['core_membership_tests'] += len(self.core)
            if self.core and self.core.issubset(self.active):
                self.counts['support_hits'] += 1
                return 0
        self.counts['solver_calls'] += 1
        if self.solver is None:
            self.counts['native_clause_literals'] += sum(len(c) for c in self.active.values())
            with Minisat22(bootstrap_with=list(self.active.values())) as solver:
                sat = solver.solve()
                model = solver.get_model() if sat else None
        else:
            assumptions = [self.n+1+cid for cid in sorted(self.active)]
            self.counts['assumption_literals'] += len(assumptions)
            sat = self.solver.solve(assumptions=assumptions)
            model = self.solver.get_model() if sat else None
        if sat:
            assignment = sum(1 << (v-1) for v in (model or []) if 0 < v <= self.n)
            # Independent SAT checker and initial maintenance construction.
            values = {cid:self.truth(c, assignment) for cid,c in self.active.items()}
            if not all(values.values()):
                raise AssertionError('Native SAT witness fails independent check')
            if self.mode in ('delta', 'native_delta', 'full_cache'):
                self.witness = assignment
                if delta:
                    self.sat_bits, self.violations = values, 0
        elif self.mode in ('delta', 'native_delta', 'full_cache'):
            self.core, self.missing = set(self.active), 0
            self.counts['support_retained_ids'] += len(self.core)
        return int(sat)

    def close(self):
        if self.solver is not None:
            self.solver.delete()


def streams(seed):
    rng = random.Random(seed)
    result = []
    for kind in ('random_edits', 'sparse_edits', 'explicit_switches'):
        for n in (8, 12, 20):
            initial = []
            for cid in range(3*n):
                variables = rng.sample(range(1,n+1), 3)
                clause = [v if rng.randrange(2) else -v for v in variables]
                initial.append([cid, clause])
            active = set(range(len(initial)))
            inactive = set()
            patches, next_id = [], len(initial)
            for t in range(96):
                if kind == 'explicit_switches':
                    phase = t % 8
                    if phase in (0, 1):
                        clause = [1] if phase == 0 else [-1]
                        cid = next_id
                        next_id += 1
                        active.add(cid)
                        patches.append(['add', cid, clause])
                    elif phase in (2, 3):
                        cid = next_id-(2 if phase == 2 else 1)
                        active.remove(cid)
                        inactive.add(cid)
                        patches.append(['off', cid, []])
                    else:
                        # Explicit tautological edits are public structural controls.
                        cid = next_id
                        next_id += 1
                        active.add(cid)
                        patches.append(['add', cid, [2, -2]])
                elif inactive and rng.randrange(5) == 0:
                    cid = rng.choice(sorted(inactive))
                    inactive.remove(cid)
                    active.add(cid)
                    patches.append(['on', cid, []])
                elif active and (rng.randrange(2) == 0 or len(active) >= 5*n):
                    cid = rng.choice(sorted(active))
                    active.remove(cid)
                    inactive.add(cid)
                    patches.append(['off', cid, []])
                else:
                    width = 3 if kind == 'random_edits' else rng.choice((2,3,4))
                    variables = rng.sample(range(1,n+1), width)
                    clause = [v if rng.randrange(2) else -v for v in variables]
                    cid = next_id
                    next_id += 1
                    active.add(cid)
                    patches.append(['add', cid, clause])
            result.append(dict(kind=kind, n=n, initial=initial, patches=patches))
    return result


def run(stream, mode):
    start = time.perf_counter_ns()
    engine = Engine(stream['n'], mode)
    try:
        for cid, clause in stream['initial']:
            engine.edit(engine.version, 'add', cid, clause)
        answers = [engine.answer()]
        for op, cid, clause in stream['patches']:
            engine.edit(engine.version, op, cid, clause)
            answers.append(engine.answer())
        counts = dict(engine.counts)
    finally:
        engine.close()
    elapsed = time.perf_counter_ns()-start
    return dict(mode=mode, elapsed_ns=elapsed, counts=counts, answers=answers)


def invalid_edits():
    engine = Engine(4, 'delta')
    engine.edit(0, 'add', 0, [1])
    answer = engine.answer()
    checks = 0
    for args in ((0,'add',1,[2]), (1,'add',0,[-1]), (1,'off',2,[]),
                 (1,'on',0,[]), (1,'add',1,[5]), (1,'add',1,[True])):
        before = (engine.version, dict(engine.active), dict(engine.registry), engine.witness,
                  engine.violations, dict(engine.sat_bits), set(engine.core), engine.missing)
        try:
            engine.edit(*args)
        except InvalidEdit:
            pass
        else:
            raise AssertionError('Invalid edit accepted')
        after = (engine.version, dict(engine.active), dict(engine.registry), engine.witness,
                 engine.violations, dict(engine.sat_bits), set(engine.core), engine.missing)
        assert before == after and engine.answer() == answer
        checks += 1
    return checks


def main(output):
    assert not output.exists()
    start = time.monotonic_ns()
    result = dict(status='running', evidence='DEVELOPMENT', contributor='Codex (GPT-6)',
                  seed=8402, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  python=sys.version, dependency_versions={p:importlib.metadata.version(p) for p in ('python-sat','six')},
                  start_utc=datetime.now(timezone.utc).isoformat(), command=sys.argv,
                  timing_scope='warm installed-runtime stream, including initialization, edits, checks, retention, failed reuse, native calls and solver cleanup; excludes common import/download and harness generation/serialization; not a cold end-to-end benchmark')
    try:
        cohort = streams(8402)
        result['streams'] = cohort
        result['invalid_edit_checks'] = invalid_edits()
        rows = []
        for index, stream in enumerate(cohort):
            modes = ('fresh', 'full_cache', 'native', 'delta', 'native_delta')
            # Two alternating passes only diagnose gross overhead; no significance claim.
            expected = None
            for repetition in range(2):
                for mode in modes if repetition == 0 else reversed(modes):
                    row = run(stream, mode)
                    if expected is None:
                        expected = row['answers']
                    assert row['answers'] == expected
                    row.update(stream=index, kind=stream['kind'], n=stream['n'], repetition=repetition)
                    rows.append(row)
        result.update(status='complete', rows=rows, checked_answers=sum(len(r['answers']) for r in rows))
    except Exception:
        result.update(status='failed', failure=traceback.format_exc())
        raise
    finally:
        result['elapsed_ns'] = time.monotonic_ns()-start
        result['end_utc'] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ('rows','streams')}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
