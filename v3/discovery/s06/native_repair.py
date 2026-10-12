#!/usr/bin/env python3
"""Persistent native IHS with a separately paid checked negative-proof bridge.

DEVELOPMENT, ChatGPT (GPT-6 Astra Pro), 2026-10-12.
Install python-sat==1.8.dev24 highspy==1.11.0. Importing performs no research run.
Native cores and numeric bounds are guidance, never independent certificates.
"""
from __future__ import annotations

from collections import Counter
import copy
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys
import time
import uuid

import highspy
import highspy._core
import numpy as np
import pysat
import pysat.solvers
import pysolvers
from pysat.solvers import Minisat22

S05 = Path(__file__).resolve().parent.parent / 's05'
if str(S05) not in sys.path:
    sys.path.insert(0, str(S05))
import maxsat_repair as kernel
import maxsat_reprice as profile_kernel

VERSION = 's06-persistent-native-ihs-v2'
DEFAULT_LIMITS = dict(max_rounds=256, sat_conflicts_per_call=100_000,
                      mip_nodes_per_call=100_000, mip_seconds_per_call=2.0,
                      proof_units=1_000_000, adapter_units=1_000_000)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def structural_id(instance):
    return kernel.digest(dict(variables=instance['variables'], hard=instance['hard'],
                              soft_clauses=[s['clause'] for s in instance['soft']]))


def weighted_instance(instance, weights):
    if (len(weights) != len(instance['soft'])
            or any(type(w) is not int or w < 0 for w in weights)):
        raise ValueError('Fixed soft-clause indexing and nonnegative integer weights required')
    # The native MIP uses doubles. Restrict exact integer admission conservatively;
    # independent checks still use Python integers and do not trust MIP arithmetic.
    if sum(weights) > 2**50:
        raise ValueError('Native adapter integer-weight range exceeded')
    answer = copy.deepcopy(instance)
    for soft, value in zip(answer['soft'], weights):
        soft['weight'] = value
    answer['objective_max'] = sum(weights)
    answer['identity'] = kernel.digest({k: v for k, v in answer.items() if k != 'identity'})
    return answer


def capabilities():
    paths = dict(adapter=__file__, pysat_wrapper=pysat.solvers.__file__,
                 pysat_native=pysolvers.__file__, highs_python=highspy.Highs.__module__,
                 highs_native=highspy._core.__file__, checker=kernel.__file__,
                 profile_compiler=profile_kernel.__file__)
    paths['highs_python'] = str(Path(highspy.__file__).with_name('highs.py'))
    return dict(adapter_version=VERSION, python=sys.version,
                platform=platform.platform(), numpy=np.__version__,
                python_sat=importlib.metadata.version('python-sat'),
                sat_engine='MiniSat 2.2', highspy=importlib.metadata.version('highspy'),
                highs_native_version=highspy.Highs().version(),
                implementation_files={k: dict(path=str(v), sha256=sha(v))
                                      for k, v in paths.items()},
                persistence=['One MiniSat object and assumption-independent learned clauses per source',
                             'One native HiGHS model with retained weight-independent core rows',
                             'Direct changeColsCost; explicit previous hitting-set MIP start',
                             'Source-bound checked witnesses and branching proofs can survive processes'],
                excluded_claims=['No claim of HiGHS branch-and-bound tree retention across weight changes',
                                 'No proof export from native MiniSat/HiGHS enters the checked lower bank',
                                 'No equivalence to optimized iMaxHS or commercial MaxHS implementation',
                                 'Native solver state is resident only, not serializable by this adapter'],
                negative_bridge='Separately paid s05 weighted-budget branching provider; independent s05 checker',
                primary_api_sources=['https://pysathq.github.io/docs/html/api/solvers.html',
                                     'https://ergo-code.github.io/HiGHS/dev/interfaces/python/example-py/'],
                api_source_note='Official current docs read 2026-10-12; installed versions and source hashes above control execution.')


class PersistentIHS:
    """Callable native IHS engine for one fixed hard/soft clause source.

    purchase(weights, budget, limits=None, exact=False) is an actual purchase.
    It returns checked SAT witness or checked UNSAT tree for cost <= budget.
    exact=True asks native IHS to complete optimization and then buys/checks a
    lower proof at its checked witness cost minus one. Neither mode uses a
    diagnostic optimum. Bounds and action stopping belong to the outer service.

    Limits are a vector, not an invented conversion of MIP nodes into DPLL units.
    Partial work and raw unchecked receipts survive a cap in returned events.
    """
    def __init__(self, instance):
        self.instance = copy.deepcopy(instance)
        if instance.get('identity') != kernel.digest({k: v for k, v in instance.items() if k != 'identity'}):
            raise ValueError('Source identity mismatch')
        n = instance['variables']
        if type(n) is not int or n < 1:
            raise ValueError('Positive variable count required')
        clauses = instance['hard'] + [s['clause'] for s in instance['soft']]
        if not instance['soft'] or any(not isinstance(c, list) or any(type(l) is not int or not 1 <= abs(l) <= n for l in c) for c in clauses):
            raise ValueError('Malformed source clauses')
        weighted_instance(instance, [s['weight'] for s in instance['soft']])
        self.structural_id = structural_id(instance)
        self.state_id = 'native-' + uuid.uuid4().hex
        self.n, self.m = n, len(instance['soft'])
        self.selectors = list(range(n + 1, n + self.m + 1))
        self.cores = []
        self.core_keys = set()
        self.weights = None
        self.last_hs = None
        self.calls = Counter()
        self.purchases = 0
        self.setup_meter = kernel.Meter()
        self.setup_meter.pay('admission', 'source_and_clause_words',
                             8 + sum(1 + len(c) for c in clauses) + self.m)
        cpu, wall = time.process_time_ns(), time.perf_counter_ns()
        encoded = copy.deepcopy(instance['hard'])
        encoded += [list(s['clause']) + [-selector]
                    for s, selector in zip(instance['soft'], self.selectors)]
        # Retain the solver object/learned clauses, but do not enable PySAT's
        # enumeration-oriented warm_start mode: the preserved development
        # attempt exposed a stale model under changing assumptions with it.
        self.sat = Minisat22(bootstrap_with=encoded, use_timer=True)
        self.setup_meter.pay('encoding', 'sat_clause_and_selector_words',
                             sum(len(c) + 1 for c in encoded) + self.m)
        self.hs = highspy.Highs()
        self._ok(self.hs.setOptionValue('output_flag', False))
        self._ok(self.hs.setOptionValue('threads', 1))
        self._ok(self.hs.setOptionValue('random_seed', 0))
        self._ok(self.hs.setOptionValue('mip_rel_gap', 0.0))
        self._ok(self.hs.setOptionValue('mip_abs_gap', 0.0))
        empty_i, empty_v = np.array([], dtype=np.int32), np.array([], dtype=float)
        for j in range(self.m):
            self._ok(self.hs.addCol(0., 0., 1., 0, empty_i, empty_v))
            self._ok(self.hs.changeColIntegrality(j, highspy.HighsVarType.kInteger))
            self.setup_meter.pay('encoding', 'native_hitting_set_column', 6)
        self.setup_timing = dict(process_ns=time.process_time_ns() - cpu,
                                 wall_ns=time.perf_counter_ns() - wall)

    @staticmethod
    def _ok(status):
        if status == highspy.HighsStatus.kError:
            raise RuntimeError('Native HiGHS API rejected operation')

    def close(self):
        if self.sat is not None:
            self.sat.delete()
            self.sat = None

    def state(self):
        return dict(state_id=self.state_id, structural_source_id=self.structural_id,
                    sat_object_id=id(self.sat), highs_object_id=id(self.hs),
                    core_rows=len(self.cores), native_row_count=self.hs.getNumRow(),
                    native_column_count=self.hs.getNumCol(), objective_weights=self.weights,
                    sat_accumulated_stats=self.sat.accum_stats(),
                    last_hitting_set=self.last_hs, calls=dict(self.calls))

    def _update(self, weights, limits, meter, events):
        for k, option in [('mip_seconds_per_call', 'time_limit'),
                          ('mip_nodes_per_call', 'mip_max_nodes')]:
            self._ok(self.hs.setOptionValue(option, limits[k]))
        changed = self.weights != list(weights)
        event = dict(kind='objective_update', changed=changed,
                     old_weights=self.weights, new_weights=list(weights),
                     existing_core_rows=len(self.cores), previous_mip_start=False)
        if changed:
            self._ok(self.hs.changeColsCost(self.m, np.arange(self.m, dtype=np.int32),
                                            np.array(weights, dtype=float)))
            self.weights = list(weights)
            self.calls['objective_updates'] += 1
            meter.pay('objective_update', 'weight_read_and_native_column_update', 2*self.m + 2)
        if self.last_hs is not None:
            self._ok(self.hs.setSolution(self.m, np.arange(self.m, dtype=np.int32),
                                         np.array(self.last_hs, dtype=float)))
            event['previous_mip_start'] = True
            meter.pay('objective_update', 'previous_hitting_set_mip_start', self.m + 2)
            self.calls['mip_starts'] += 1
        events.append(event)

    def _native(self, weighted, budget, exact, limits, meter, events):
        self._update([s['weight'] for s in weighted['soft']], limits, meter, events)
        weights = self.weights
        for round_no in range(limits['max_rounds']):
            meter.pay('native_dispatch', 'hitting_set_solve_call')
            self.calls['hitting_set_calls'] += 1
            cpu, wall = time.process_time_ns(), time.perf_counter_ns()
            self.hs.run()
            status, info = self.hs.getModelStatus(), self.hs.getInfo()
            elapsed = dict(process_ns=time.process_time_ns()-cpu,
                           wall_ns=time.perf_counter_ns()-wall)
            event = dict(kind='native_hitting_set', round=round_no,
                         status=str(status), core_rows=len(self.cores),
                         mip_nodes=int(info.mip_node_count), timing=elapsed,
                         independently_checked_lower=False)
            events.append(event)
            if status != highspy.HighsModelStatus.kOptimal:
                return dict(status='UNRESOLVED', reason='native_hitting_set_incomplete')
            col = self.hs.getSolution().col_value
            hs = [int(v > .5) for v in col]
            if (any(abs(v-z) > 1e-5 for v, z in zip(col, hs))
                    or any(not any(hs[j] for j in core) for core in self.cores)):
                return dict(status='UNRESOLVED', reason='native_hitting_set_model_malformed')
            self.last_hs = hs
            hint = sum(w*z for w, z in zip(weights, hs))
            event.update(hitting_set=hs, objective_hint=hint)
            meter.pay('native_result', 'hitting_set_values_and_objective', 3*self.m)
            if not exact and hint > budget:
                return dict(status='LOWER_HINT', lower_hint=hint)
            assumptions = [s for s, relaxed in zip(self.selectors, hs) if not relaxed]
            meter.pay('native_dispatch', 'sat_assumption_words', len(assumptions) + 1)
            self.sat.conf_budget(limits['sat_conflicts_per_call'])
            before = self.sat.accum_stats()
            cpu, wall = time.process_time_ns(), time.perf_counter_ns()
            sat = self.sat.solve_limited(assumptions=assumptions)
            elapsed = dict(process_ns=time.process_time_ns()-cpu,
                           wall_ns=time.perf_counter_ns()-wall)
            after = self.sat.accum_stats()
            self.calls['sat_calls'] += 1
            event = dict(kind='native_sat', round=round_no, assumptions=assumptions,
                         status='SAT' if sat is True else 'UNSAT' if sat is False else 'UNRESOLVED',
                         stats={k: after[k]-before[k] for k in after}, timing=elapsed)
            events.append(event)
            if sat is None:
                return dict(status='UNRESOLVED', reason='native_sat_limit')
            if sat:
                literals = self.sat.get_model()
                literal_set = set(literals)
                meter.pay('native_result', 'assumption_model_validation', len(assumptions))
                if any(l not in literal_set for l in assumptions):
                    event['model_literals'] = literals
                    return dict(status='UNRESOLVED', reason='native_model_misses_assumptions')
                positive = {l for l in literals if 1 <= l <= self.n}
                model = sum(1 << (j-1) for j in positive)
                compiled = profile_kernel.compile_witness(weighted, model, meter)
                event.update(model=model, checked_objective=compiled['original_cost'])
                if compiled['original_cost'] > hint:
                    return dict(status='UNRESOLVED', reason='native_model_misses_hitting_set_cost',
                                witness=compiled)
                if not exact and compiled['original_cost'] > budget:
                    return dict(status='UNRESOLVED', reason='native_model_misses_requested_budget',
                                witness=compiled)
                return dict(status='SAT', witness=compiled, optimum_hint=exact,
                            native_lower_hint=hint)
            core_literals = self.sat.get_core()
            if (not core_literals or any(l not in assumptions for l in core_literals)):
                return dict(status='UNRESOLVED', reason='empty_or_malformed_native_core')
            core = sorted({l - self.n - 1 for l in core_literals})
            event.update(core_soft_indices=core, independently_checked_core=False)
            key = tuple(core)
            if key in self.core_keys:
                return dict(status='UNRESOLVED', reason='native_duplicate_core_no_progress')
            self.core_keys.add(key)
            self.cores.append(core)
            self._ok(self.hs.addRow(1., highspy.kHighsInf, len(core),
                                    np.array(core, dtype=np.int32), np.ones(len(core))))
            meter.pay('core_storage', 'native_core_rows_and_indices', 2*len(core) + 3)
            self.calls['cores_added'] += 1
        return dict(status='UNRESOLVED', reason='native_round_limit')

    def purchase(self, weights, budget, limits=None, exact=False):
        if self.sat is None:
            raise RuntimeError('Native runtime has been closed')
        if type(budget) is not int:
            raise ValueError('Integer bounded-decision budget required')
        caps = dict(DEFAULT_LIMITS)
        if limits:
            if set(limits) - set(caps):
                raise ValueError('Unknown resource cap')
            caps.update(limits)
        for k, value in caps.items():
            if value < 0 or (k != 'mip_seconds_per_call' and type(value) is not int):
                raise ValueError('Nonnegative resource limits required')
        weighted = weighted_instance(self.instance, list(weights))
        meter = kernel.Meter(caps['adapter_units'])
        events, proof_record, native = [], None, None
        before = self.state()
        cpu, wall = time.process_time_ns(), time.perf_counter_ns()
        answer = dict(status='UNRESOLVED', model=None, proof=None, witness=None,
                      checked_lower=None, checked_lower_receipt=None)
        try:
            meter.pay('admission', 'weight_source_and_budget_words', len(weights) + 10)
            native = self._native(weighted, budget, exact, caps, meter, events)
            if native.get('witness') is not None:
                answer.update(witness=native['witness'], model=native['witness']['model'])
            if native['status'] == 'SAT' and not exact:
                answer['status'] = 'SAT'
            elif native['status'] in ('LOWER_HINT', 'SAT'):
                proof_budget = native['witness']['original_cost'] - 1 if exact else budget
                # This is new independent proof production, not a conversion of
                # native core or status into the archived tree format.
                pcpu, pwall = time.process_time_ns(), time.perf_counter_ns()
                got = kernel.budget_provider(weighted, proof_budget, caps['proof_units'])
                self.calls['proof_provider_calls'] += 1
                proof_record = dict(kind='separate_bounded_proof_provider',
                                    source_identity=weighted['identity'], weights=list(weights),
                                    structural_source_id=self.structural_id,
                                    budget=proof_budget, cap=caps['proof_units'],
                                    timing=dict(process_ns=time.process_time_ns()-pcpu,
                                                wall_ns=time.perf_counter_ns()-pwall),
                                    checked=False, **got)
                events.append(proof_record)
                if got['status'] == 'UNSAT':
                    kernel.check_negative(weighted, proof_budget, got['proof'], meter)
                    leaves = profile_kernel.compile_tree(got['proof'], meter)
                    receipt_id = kernel.digest(dict(source=weighted['identity'], budget=proof_budget,
                                                     proof=got['proof']))
                    meter.pay('proof_storage', 'checked_raw_proof_receipt',
                              kernel.proof_words(got['proof']) + len(weights) + 12)
                    proof_record.update(checked=True, receipt_id=receipt_id, leaf_masks=leaves)
                    answer.update(status='SAT' if exact else 'UNSAT', proof=got['proof'],
                                  checked_lower=proof_budget + 1,
                                  checked_lower_receipt=proof_record)
                elif got['status'] == 'SAT':
                    witness = profile_kernel.compile_witness(weighted, got['model'], meter)
                    if witness['original_cost'] > proof_budget:
                        raise ValueError('Independent proof provider witness exceeds budget')
                    proof_record['checked'] = True
                    answer.update(status='SAT', model=witness['model'], witness=witness)
                    if exact:
                        answer['native_optimum_disconfirmed'] = True
                else:
                    answer['reason'] = 'negative_proof_provider_limit'
            else:
                answer['reason'] = native.get('reason', 'native_incomplete')
        except kernel.CapReached:
            answer['reason'] = 'adapter_check_or_retention_limit'
            answer['status'] = 'UNRESOLVED'
            # A raw proof may be in events; only the fully checked receipt
            # assigned above may enter a consumer's lower bank.
        self.purchases += 1
        answer.update(version=VERSION, source_identity=weighted['identity'],
                      structural_source_id=self.structural_id, weight_id=kernel.digest(list(weights)),
                      weights=list(weights), requested_budget=budget, exact_requested=exact,
                      caps=caps, state_before=before, state_after=self.state(),
                      native_result=native, events=events,
                      adapter_invoice=meter.record(),
                      proof_provider_invoice=None if proof_record is None else proof_record['invoice'],
                      native_search_units=None,
                      native_cost_note='Native search has measured timings, calls, SAT stats and MIP nodes; no DPLL-tariff conversion.',
                      timing=dict(process_ns=time.process_time_ns()-cpu,
                                  wall_ns=time.perf_counter_ns()-wall))
        return answer
