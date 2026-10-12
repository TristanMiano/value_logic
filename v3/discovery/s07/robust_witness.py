#!/usr/bin/env python3
"""Persistent ordinary MIP proposals for scalar-anchor robust repair actions.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. HiGHS searches for a
feasible action; its status, objective and dual bound are never certificates.
The caller supplies admitted source-specific scalar lowers and subsequently
uses the ordinary RepairEvaluator to certify any independently checked action.
"""
from __future__ import annotations

from collections import Counter
import copy
from fractions import Fraction as F
import math
from pathlib import Path
import sys
import time
import uuid

import highspy
import numpy as np

S06 = Path(__file__).resolve().parent.parent / 's06'
if str(S06) not in sys.path:
    sys.path.insert(0, str(S06))
import native_repair as native


VERSION = 's07-persistent-robust-witness-v1'
DEFAULT_SECONDS = 0.1
DEFAULT_NODES = 1000


def _finite_number(value):
    value = float(value)
    return value if math.isfinite(value) else None


class RobustWitness:
    """One permanent CNF/violation/epigraph MIP, updated through row bounds.

    ``propose(costs, anchor_lowers, price, *, seconds=.1, nodes=1000)``
    returns a checked source-feasible witness or UNRESOLVED, always with its
    actual API/checking invoice and native CPU/wall observations. A checked
    proposal may repeat an existing witness and does not promise progress.

    The supplied lowers must be independently admitted at N*mode[k] on this
    logical source. Checking that mathematical premise belongs to the caller;
    an untrusted vector of scalar values is not proof admission here.
    """

    def __init__(self, instance, costs, meter):
        wall, cpu = time.perf_counter_ns(), time.process_time_ns()
        before = self._mark(meter)
        self.meter = meter
        self.instance = copy.deepcopy(instance)
        self.source_id = instance.get('identity')
        if self.source_id != native.kernel.digest({k: v for k, v in instance.items() if k != 'identity'}):
            raise ValueError('Changed original logical source identity')
        self.n, self.m = instance['variables'], len(instance['soft'])
        clauses = instance['hard'] + [s['clause'] for s in instance['soft']]
        if (type(self.n) is not int or self.n < 1 or self.m < 1
                or any(not isinstance(c, list) or any(type(l) is not int or not 1 <= abs(l) <= self.n for l in c) for c in clauses)):
            raise ValueError('A finite fixed CNF and ordered soft-feature source required')
        self.cost_source_id, self.N = costs.source_id, costs.n
        self.modes = tuple(tuple(v) for v in costs.modes)
        self.K = len(self.modes)
        self._costs(costs)
        self.structural_id = native.structural_id(instance)
        self.state_id = 'robust-' + uuid.uuid4().hex
        meter.pay('robust_admission', 'logical_source_and_clause_words', 8 + self.m + sum(1 + len(c) for c in clauses))
        checked = native.profile_kernel.compile_witness(instance, instance['public_incumbent'], meter)
        self.last_model, self.last_mask = checked['model'], checked['violation_mask']
        self.calls = Counter()
        self.rows, self.columns = 0, 0
        self.hs = highspy.Highs()
        for name, value in [('output_flag', False), ('threads', 1), ('random_seed', 0),
                            ('mip_rel_gap', 0.0), ('mip_abs_gap', 0.0)]:
            self._ok(self.hs.setOptionValue(name, value))
            meter.pay('robust_setup', 'native_option_dispatch', 2)
        self.x = [self._column(0, 0, 1, True) for _ in range(self.n)]
        self.z = [self._column(0, 0, 1, True) for _ in range(self.m)]
        self.a = [self._column(0, -highspy.kHighsInf, highspy.kHighsInf) for _ in range(self.N)]
        self.b = [self._column(0, 0, highspy.kHighsInf) for _ in range(self.N)]
        self.t = self._column(1, 0, highspy.kHighsInf)

        # Clause truth is sign(l)*x + 1[l<0]. Hard clauses have at least one
        # true literal. Soft z is exactly 1 iff all its literals are false.
        for clause in instance['hard']:
            coefficients, negative = self._clause(clause)
            self._row(1 - negative, highspy.kHighsInf, coefficients)
        for j, soft in enumerate(instance['soft']):
            clause = soft['clause']
            coefficients, negative = self._clause(clause)
            coefficients[self.z[j]] = 1
            self._row(1 - negative, highspy.kHighsInf, coefficients)
            for literal in clause:
                self._row(-highspy.kHighsInf, 1 if literal > 0 else 0,
                          {self.z[j]: 1, self.x[abs(literal) - 1]: 1 if literal > 0 else -1})

        self.contrast_rows, self.upper_rows = {}, {}
        self._bounds = {}
        for i in range(self.N):
            for k, mode in enumerate(self.modes):
                c = {self.z[j]: -w for j, w in enumerate(mode) if w}
                self.contrast_rows[i, k] = self._row(-highspy.kHighsInf, highspy.kHighsInf, c | {self.a[i]: 1})
                self.upper_rows[i, k] = self._row(-highspy.kHighsInf, highspy.kHighsInf, c | {self.b[i]: 1})
        self._row(0, highspy.kHighsInf, {self.t: 1} | {a: -1 for a in self.a})
        self.price_row = self._row(0, highspy.kHighsInf, {self.t: 1} | {b: -1 for b in self.b})
        self._bounds[self.price_row] = F(0)
        self.current_possible, self.current_lowers, self.current_price = None, None, None
        self.setup_invoice = self._invoice(before)
        self.setup_timing = dict(process_ns=time.process_time_ns() - cpu, wall_ns=time.perf_counter_ns() - wall)

    @staticmethod
    def _ok(status):
        if status == highspy.HighsStatus.kError:
            raise RuntimeError('Native HiGHS API rejected the robust witness operation')

    @staticmethod
    def _mark(meter):
        return meter.total, Counter(meter.operations)

    def _invoice(self, before):
        total, previous = before
        difference = self.meter.operations - previous
        categories = Counter()
        for (category, _), value in difference.items():
            categories[category] += value
        return dict(total=self.meter.total - total, by_category=dict(categories),
                    operations=[dict(category=c, operation=o, units=v) for (c, o), v in sorted(difference.items())])

    def _costs(self, costs):
        if (costs.meter is not self.meter or costs.source_id != self.cost_source_id
                or costs.n != self.N or costs.m != self.m
                or tuple(tuple(v) for v in costs.modes) != self.modes):
            raise ValueError('Cost source, cohort, feature meanings or meter changed')
        if (type(self.N) is not int or self.N < 1 or not self.modes
                or any(len(v) != self.m or any(type(w) is not int or w < 0 for w in v) for v in self.modes)
                or len(costs.possible) != self.N):
            raise ValueError('Nonnegative integral finite-cohort cost modes required')
        possible = tuple(tuple(row) for row in costs.possible)
        if any(not row or len(set(row)) != len(row)
               or any(type(k) is not int or not 0 <= k < self.K for k in row) for row in possible):
            raise ValueError('Each actual cost row needs a nonempty set of admitted modes')
        if max(sum(v) for v in self.modes) * self.N > 2**50:
            raise ValueError('Conservative native finite-coefficient range exceeded')
        self.meter.pay('robust_admission', 'public_mode_and_possible_source_words',
                       self.K * self.m + sum(map(len, possible)) + self.N + 8)
        return possible

    def _column(self, cost, lower, upper, integer=False):
        index = self.columns
        self._ok(self.hs.addCol(float(cost), float(lower), float(upper), 0,
                               np.array([], dtype=np.int32), np.array([], dtype=float)))
        if integer:
            self._ok(self.hs.changeColIntegrality(index, highspy.HighsVarType.kInteger))
        self.columns += 1
        self.meter.pay('robust_setup', 'native_column_and_integrality', 6 + 2 * integer)
        return index

    def _clause(self, clause):
        coefficients, negative = {}, 0
        for literal in clause:
            variable = self.x[abs(literal) - 1]
            coefficients[variable] = coefficients.get(variable, 0) + (1 if literal > 0 else -1)
            negative += literal < 0
            self.meter.pay('robust_encoding', 'clause_literal_linear_truth', 4)
        return {j: a for j, a in coefficients.items() if a}, negative

    def _row(self, lower, upper, coefficients):
        pairs = sorted((j, a) for j, a in coefficients.items() if a)
        row = self.rows
        self._ok(self.hs.addRow(float(lower), float(upper), len(pairs),
                               np.array([j for j, _ in pairs], dtype=np.int32),
                               np.array([a for _, a in pairs], dtype=float)))
        self.rows += 1
        self.meter.pay('robust_encoding', 'native_linear_row_and_coefficient_words', 2 * len(pairs) + 6)
        return row

    def _bound(self, row, lower):
        self.meter.pay('robust_update', 'row_bound_lookup_and_comparison', 2)
        if row not in self._bounds or self._bounds[row] != lower:
            self._ok(self.hs.changeRowBounds(row, float(lower), highspy.kHighsInf))
            self._bounds[row] = lower
            self.meter.pay('robust_update', 'native_row_bound_change_and_storage', 5)
            return 1
        return 0

    def _warm_start(self, possible, lowers, price):
        values = [0.0] * self.columns
        for j in range(self.n):
            values[self.x[j]] = float((self.last_model >> j) & 1)
        for j in range(self.m):
            values[self.z[j]] = float((self.last_mask >> j) & 1)
        mode_costs = [sum(w for j, w in enumerate(mode) if self.last_mask & (1 << j)) for mode in self.modes]
        gaps, uppers = [], []
        for i, choices in enumerate(possible):
            gap = max(F(mode_costs[k]) - lowers[k] / self.N for k in choices)
            upper = max(mode_costs[k] for k in choices)
            values[self.a[i]], values[self.b[i]] = float(gap), float(upper)
            gaps.append(gap)
            uppers.append(upper)
            self.meter.pay('robust_start', 'exact_row_epigraph_values', 3 * len(choices) + 4)
        values[self.t] = float(max(F(0), sum(gaps, F(0)), sum(uppers) - price))
        self._ok(self.hs.setSolution(self.columns, np.arange(self.columns, dtype=np.int32), np.array(values, dtype=float)))
        self.meter.pay('robust_start', 'checked_assignment_and_full_mip_start',
                       self.n + self.m + 2 * self.K * self.m + self.columns + 2 * self.N + 8)
        self.calls['explicit_mip_starts'] += 1

    def state(self):
        return dict(state_id=self.state_id, structural_source_id=self.structural_id,
                    cost_source_id=self.cost_source_id, highs_object_id=id(self.hs),
                    native_row_count=self.hs.getNumRow(), native_column_count=self.hs.getNumCol(),
                    last_checked_model=self.last_model, last_checked_mask=self.last_mask,
                    calls=dict(self.calls))

    def propose(self, costs, anchor_lowers, price, *, seconds=DEFAULT_SECONDS, nodes=DEFAULT_NODES):
        wall, cpu = time.perf_counter_ns(), time.process_time_ns()
        before = self._mark(self.meter)
        state_before = self.state()
        possible = self._costs(costs)
        lowers, price = tuple(F(v) for v in anchor_lowers), F(price)
        if (len(lowers) != self.K or any(v < 0 or v > 2**50 for v in lowers)
                or price < 0 or price > 2**50 or not math.isfinite(seconds) or seconds < 0
                or type(nodes) is not int or nodes < 0):
            raise ValueError('Admitted finite nonnegative anchors/price and finite nonnegative caps required')
        self.meter.pay('robust_admission', 'anchor_price_and_cap_words', 2 * self.K + 8)
        self.calls['proposals'] += 1
        response = dict(version=VERSION, status='UNRESOLVED', witness=None, model=None,
                        source_identity=self.source_id, structural_source_id=self.structural_id,
                        cost_source_id=self.cost_source_id, possible_modes=[list(p) for p in possible],
                        anchor_lowers=list(lowers), price=price,
                        caps=dict(seconds=seconds, nodes=nodes),
                        checked_lower_receipt=None, independently_checked_lower=False,
                        native_lower_is_guidance_only=True, state_before=state_before)
        native_timing = dict(process_ns=0, wall_ns=0)
        try:
            changed = 0
            for i, choices in enumerate(possible):
                enabled = set(choices)
                self.meter.pay('robust_update', 'active_mode_set', len(choices) + 1)
                for k in range(self.K):
                    active = k in enabled
                    changed += self._bound(self.contrast_rows[i, k], -lowers[k] / self.N if active else -highspy.kHighsInf)
                    changed += self._bound(self.upper_rows[i, k], F(0) if active else -highspy.kHighsInf)
            changed += self._bound(self.price_row, -price)
            self.current_possible, self.current_lowers, self.current_price = possible, lowers, price
            self._ok(self.hs.setOptionValue('time_limit', float(seconds)))
            self._ok(self.hs.setOptionValue('mip_max_nodes', nodes))
            self.meter.pay('robust_update', 'native_time_and_node_caps', 4)
            self._warm_start(possible, lowers, price)
            response['changed_native_row_bounds'] = changed
            self.calls['native_mip_calls'] += 1
            self.meter.pay('robust_dispatch', 'native_mip_run')
            native_wall, native_cpu = time.perf_counter_ns(), time.process_time_ns()
            try:
                api_status = self.hs.run()
            finally:
                native_timing = dict(process_ns=time.process_time_ns() - native_cpu,
                                     wall_ns=time.perf_counter_ns() - native_wall)
            self._ok(api_status)
            status, info, solution = self.hs.getModelStatus(), self.hs.getInfo(), self.hs.getSolution()
            response['native'] = dict(api_status=str(api_status), model_status=str(status),
                objective_hint=_finite_number(info.objective_function_value),
                mip_dual_hint=_finite_number(info.mip_dual_bound), mip_gap_hint=_finite_number(info.mip_gap),
                nodes=int(info.mip_node_count), simplex_iterations=int(info.simplex_iteration_count),
                value_valid=bool(solution.value_valid), timing=native_timing)
            self.meter.pay('robust_result', 'native_status_and_primal_values', self.columns + 12)
            columns = list(solution.col_value)
            if not solution.value_valid or len(columns) != self.columns or any(not math.isfinite(v) for v in columns):
                response['reason'] = 'No finite native primal proposal under the supplied caps'
            else:
                proposed = [int(columns[j] > 0.5) for j in self.x + self.z]
                integral = all(abs(columns[j] - value) <= 1e-5 for j, value in zip(self.x + self.z, proposed))
                self.meter.pay('robust_result', 'native_binary_primal_admission', 3 * (self.n + self.m))
                if not integral:
                    response['reason'] = 'Native primal was not an integral source/violation proposal'
                else:
                    model = sum(value << j for j, value in enumerate(proposed[:self.n]))
                    claimed_mask = sum(value << j for j, value in enumerate(proposed[self.n:]))
                    try:
                        checked = native.profile_kernel.compile_witness(self.instance, model, self.meter)
                    except ValueError as exc:
                        response['reason'] = 'Native proposal failed the original hard-source check: ' + str(exc)
                    else:
                        if checked['violation_mask'] != claimed_mask:
                            response['reason'] = 'Native violation binaries disagreed with the actual original soft clauses'
                        else:
                            checked['receipt_id'] = native.kernel.digest(dict(source=self.source_id, model=model,
                                                                              violation_mask=checked['violation_mask']))
                            response.update(status='CHECKED_WITNESS', model=model, witness=checked,
                                            repeats_previous_model=model == self.last_model)
                            self.last_model, self.last_mask = model, checked['violation_mask']
                            self.calls['checked_witnesses'] += 1
                            self.meter.pay('robust_retention', 'checked_proposal_and_warm_assignment', self.n + self.m + 8)
        except RuntimeError as exc:
            response['reason'] = str(exc)
            response['native_api_failure'] = True
        self.meter.pay('robust_output', 'source_caps_witness_and_invoice_fields', 28)
        response.update(state_after=self.state(), invoice=self._invoice(before),
                        timing=dict(process_ns=time.process_time_ns() - cpu, wall_ns=time.perf_counter_ns() - wall),
                        native_timing=native_timing,
                        certificate_contract='Only the checked action is exportable. Native robust objective, status and dual bound do not certify regret or optimality; use RepairEvaluator with admitted evidence.',
                        costs='Actual setup/API/checking named units and native CPU/wall; native-search operation conversion, physical memory and economic price remain unassigned.')
        return response
