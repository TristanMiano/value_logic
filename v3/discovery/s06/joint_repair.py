#!/usr/bin/env python3
"""Finite-cohort cost audits and persistent checked logical repair purchases.

DEVELOPMENT, ChatGPT (GPT-6 Astra Pro), 2026-10-12. No population inference.
The controller sees possible cost modes and paid coordinate observations, never
the hidden realized mode or diagnostic optimum. A common source covers every
adaptively chosen action. Native status alone cannot supply a lower receipt.
"""
from __future__ import annotations

from collections import Counter
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import sys
import time

HERE = Path(__file__).resolve().parent
S05 = HERE.parent / 's05'
sys.path.insert(0, str(S05))
import maxsat_repair as src
import maxsat_reprice as raw
from native_repair import PersistentIHS, capabilities, structural_id

VERSION = 's06-joint-repair-v1'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def bits(mask, size):
    return tuple((mask >> j) & 1 for j in range(size))


def dot(a, b, meter, category='support'):
    meter.pay(category, 'coefficient_products_and_sum', 2 * len(a))
    return sum(x*y for x, y in zip(a, b))


def prepare(path):
    if path.exists():
        raise FileExistsError('Preserve source and exposed outcomes')
    base = list(src.WEIGHTS)
    modes = [
        [max(0, w-1) for w in base], base,
        [w+1 for w in base],
        [max(0, w+(1 if j % 2 == 0 else -1)) for j, w in enumerate(base)],
        [max(0, w+(-1 if j % 2 == 0 else 1)) for j, w in enumerate(base)],
        [max(0, w+(j % 3)-1) for j, w in enumerate(base)],
    ]
    rng = random.Random(261012606)
    cohort = 8
    data = dict(version=VERSION, evidence='DEVELOPMENT',
                contributor='ChatGPT (GPT-6 Astra Pro)',
                created_utc=datetime.now(timezone.utc).isoformat(),
                design='Fixed finite cohort with known possible cost vectors and unknown realized modes. No mode probabilities supplied to controllers.',
                seed=261012606, possible_cost_modes=modes, cohort_size=cohort,
                hidden_modes=[rng.randrange(len(modes)) for _ in range(cohort)],
                logical_archive='v3/discovery/s05/maxsat_repair_results.json',
                logical_archive_sha256=sha(S05/'maxsat_repair_results.json'),
                schedule=[dict(row=row, price=6*cohort, tolerance=cohort//2)
                          for row in range(16)],
                scale='Internal costs are cohort sums; divide price, regret and action costs by cohort_size for cohort means.',
                policies=['certificate_directed', 'audit_first', 'logic_first'],
                limits=dict(max_actions_per_request=80, max_observations=64,
                            max_logical_purchases=128,
                            native=dict(max_rounds=64, mip_seconds_per_call=0.1,
                                        sat_conflicts_per_call=10000, mip_nodes_per_call=10000,
                                        proof_units=1000000, adapter_units=1000000)),
                pricing='Each revealed cost coordinate is one paid external audit; expose its count and an unassigned monetary price. Named software-operation tariffs and native timings are separate, with no conversion into an economic headline.')
    data['source_identity'] = src.digest(data)
    path.write_text(json.dumps(data, indent=2)+'\n')
    return data


class CostOracle:
    """Trusted observation interface for a committed synthetic finite source.

    A receipt's checksum binds its recorded bytes; it does not establish that
    an external sensor is truthful. Here the actual fixed source is archived.
    """
    def __init__(self, data):
        if src.digest({k:v for k,v in data.items() if k != 'source_identity'}) != data['source_identity']:
            raise ValueError('Changed committed cost source')
        self._modes = copy.deepcopy(data['possible_cost_modes'])
        self._hidden = list(data['hidden_modes'])
        self.source_id = data['source_identity']
        self.calls = []

    def audit(self, row, coordinate):
        start, cpu = time.perf_counter_ns(), time.process_time_ns()
        value = self._modes[self._hidden[row]][coordinate]
        receipt = dict(source_id=self.source_id, row=row, coordinate=coordinate,
                       value=value, provider_call=len(self.calls),
                       observed_utc=datetime.now(timezone.utc).isoformat(),
                       observation_units=1,
                       provider_software_units=4,
                       timing=dict(wall_ns=time.perf_counter_ns()-start,
                                   process_ns=time.process_time_ns()-cpu))
        receipt['receipt_id'] = src.digest(receipt)
        self.calls.append(receipt)
        return receipt


class CostState:
    def __init__(self, public_modes, cohort_size, source_id, meter, representation='joint'):
        self.modes = tuple(tuple(v) for v in public_modes)
        self.n, self.m = cohort_size, len(self.modes[0])
        if self.n <= 0 or any(len(v) != self.m or any(type(x) is not int or x < 0 for x in v) for v in self.modes):
            raise ValueError('Nonnegative integral possible cost modes required')
        self.possible = [tuple(range(len(self.modes))) for _ in range(cohort_size)]
        self.source_id, self.meter = source_id, meter
        self.representation = representation
        self.receipts = []
        meter.pay('cost_admission', 'mode_and_row_words', len(self.modes)*self.m + self.n + 8)

    def support(self, coefficient):
        """Exact support and an attaining cohort-sum vector, or safe box support."""
        if len(coefficient) != self.m:
            raise ValueError('Cost feature meaning changed')
        total, point = 0, [0]*self.m
        for choices in self.possible:
            if self.representation == 'joint':
                values = [(dot(coefficient, self.modes[k], self.meter), k) for k in choices]
                value, winner = max(values)
                self.meter.pay('support', 'row_maximum', len(values))
                vector = self.modes[winner]
            else:
                vector = tuple((max if c >= 0 else min)(self.modes[k][j] for k in choices)
                               for j, c in enumerate(coefficient))
                self.meter.pay('support', 'coordinate_box_extrema', self.m*len(choices))
                value = dot(coefficient, vector, self.meter)
            total += value
            point = [x+y for x, y in zip(point, vector)]
            self.meter.pay('support', 'cohort_support_and_argmax_add', self.m+1)
        return total, point

    def observe(self, receipt):
        body = {k:v for k,v in receipt.items() if k != 'receipt_id'}
        if receipt['source_id'] != self.source_id or src.digest(body) != receipt['receipt_id']:
            raise ValueError('Observation source or receipt changed')
        row, j, value = receipt['row'], receipt['coordinate'], receipt['value']
        if not (type(row) is int and 0 <= row < self.n and type(j) is int and 0 <= j < self.m):
            raise ValueError('Observation indexing changed')
        remaining = tuple(k for k in self.possible[row] if self.modes[k][j] == value)
        self.meter.pay('cost_check', 'receipt_binding_and_mode_filter', 12+len(self.possible[row]))
        if not remaining:
            raise ValueError('Inconsistent cost source; cannot certify empty W')
        self.possible[row] = remaining
        self.receipts.append(receipt['receipt_id'])
        self.meter.pay('storage', 'cost_receipt_and_remaining_mode_ids', 8+len(remaining))

    def snapshot(self):
        return dict(source_id=self.source_id, representation=self.representation,
                    cohort_size=self.n, possible_modes=[list(v) for v in self.possible],
                    audit_receipts=list(self.receipts))


def certificate(profile, costs, price):
    """Min over checked fixed actions and individual retained proof regions."""
    trees = profile['trees'] or [dict(leaf_masks=[0], receipt_id='nonnegative_objective')]
    candidates = [(w['model'], w['violation_mask']) for w in profile['witnesses']] + [(None, None)]
    records = []
    for model, mask in candidates:
        u = bits(mask, costs.m) if mask is not None else (0,)*costs.m
        for ti, tree in enumerate(trees):
            inequalities = []
            if mask is not None:
                value, point = costs.support(u)
                inequalities.append((value-price, tuple(u), -price, point, 'replacement'))
            for leaf in tree['leaf_masks']:
                v = bits(leaf, costs.m)
                c = tuple(a-b for a,b in zip(u,v))
                value, point = costs.support(c)
                constant = price if mask is None else 0
                inequalities.append((value+constant, c, constant, point, 'proof_leaf'))
            worst = max(inequalities, key=lambda x:x[0])
            records.append(dict(bound=max(0,worst[0]), model=model, mask=mask,
                                action='replace' if mask is None else 'repair',
                                tree_index=None if not profile['trees'] else ti,
                                proof_id=tree.get('receipt_id', tree.get('source_receipt', 'archive-tree')),
                                critical_coefficient=list(worst[1]), critical_constant=worst[2],
                                critical_weights=worst[3], critical_role=worst[4]))
            costs.meter.pay('certificate', 'constraint_maximum_and_record', len(inequalities)+12)
    best = min(records, key=lambda r:(r['bound'], r['model'] is None,
                                      -1 if r['model'] is None else r['model']))
    costs.meter.pay('certificate', 'action_proof_pair_minimum', len(records))
    return best


def ambiguity(profile, costs, chosen, price):
    u = bits(chosen['mask'], costs.m) if chosen['mask'] is not None else (0,)*costs.m
    options = [(w['violation_mask'], 0) for w in profile['witnesses']] + [(None, price)]
    witnesses = []
    for mask, other_constant in options:
        v = bits(mask, costs.m) if mask is not None else (0,)*costs.m
        c = tuple(a-b for a,b in zip(u,v))
        constant = (price if chosen['mask'] is None else 0)-other_constant
        value, point = costs.support(c)
        witnesses.append(dict(bound=value+constant, coefficient=list(c), weights=point,
                              competing_mask=mask))
    costs.meter.pay('acquisition', 'feasible_ambiguity_maximum', len(witnesses))
    return max(witnesses, key=lambda v:v['bound'])


def audit_choice(costs, coefficient, directed):
    """Range-target score; no model of audit outcome probabilities is assumed."""
    options = []
    for row, choices in enumerate(costs.possible):
        if len(choices) <= 1:
            continue
        values = {k:dot(coefficient,costs.modes[k],costs.meter,'acquisition') for k in choices}
        span = max(values.values())-min(values.values())
        for j in range(costs.m):
            groups = {}
            for k in choices:
                groups.setdefault(costs.modes[k][j], []).append(k)
            costs.meter.pay('acquisition','audit_outcome_partition',len(choices))
            if len(groups) <= 1:
                continue
            widths = [max(values[k] for k in ks)-min(values[k] for k in ks) for ks in groups.values()]
            guaranteed, possible = span-max(widths), span-min(widths)
            options.append(dict(row=row, coordinate=j, guaranteed_contrast_span_reduction=guaranteed,
                                possible_contrast_span_reduction=possible,
                                largest_remaining_mode_count=max(map(len,groups.values())),
                                outcomes=sorted(groups)))
            costs.meter.pay('acquisition','audit_span_quote_and_record',4*len(groups)+8)
    if not options:
        return None
    if not directed:
        return min(options,key=lambda o:(o['row'],o['coordinate']))
    return min(options,key=lambda o:(-o['guaranteed_contrast_span_reduction'],
                                     -o['possible_contrast_span_reduction'],
                                     o['largest_remaining_mode_count'],o['row'],o['coordinate']))


def point_query(profile, weights, price, tolerance, meter):
    upper = min(raw.dot(w['violation_mask'],weights,meter,'point_objective') for w in profile['witnesses'])
    lower = max([0]+[min(raw.dot(v,weights,meter,'point_objective') for v in t['leaf_masks'])
                      for t in profile['trees']])
    meter.pay('acquisition','point_gap_and_budget',len(profile['witnesses'])+len(profile['trees'])+6)
    if min(upper,price)-min(lower,price) <= tolerance:
        return None
    return dict(weights=list(weights),budget=min(upper,price)-tolerance-1,
                checked_point_bounds=[lower,upper])


def run_arm(data, instances, initial, policy, representation='joint'):
    meter = src.Meter()
    start, cpu = time.perf_counter_ns(), time.process_time_ns()
    oracle = CostOracle(data)
    costs = CostState(data['possible_cost_modes'],data['cohort_size'],data['source_identity'],meter,representation)
    profiles = copy.deepcopy(initial)
    engines, purchased = {}, set()
    requests, events = [], []
    native_software, proof_units, native_setup = 0, 0, 0
    limits = data['limits']
    native_calls = 0
    try:
        for index, duty in enumerate(data['schedule']):
            row, price, tolerance = duty['row'], duty['price'], duty['tolerance']
            profile = profiles[row]
            before = certificate(profile,costs,price)
            chosen, steps = before, 0
            request_events = []
            reason = None
            while chosen['bound'] > tolerance and steps < limits['max_actions_per_request']:
                conflict = ambiguity(profile,costs,chosen,price)
                coefficient = conflict['coefficient'] if conflict['bound'] > tolerance else chosen['critical_coefficient']
                audit = audit_choice(costs,coefficient,policy == 'certificate_directed')
                query = point_query(profile,chosen['critical_weights'],price,tolerance,meter)
                key = None if query is None else (row,tuple(query['weights']),query['budget'])
                logical_available = query is not None and key not in purchased and native_calls < limits['max_logical_purchases']
                if policy == 'audit_first':
                    do_audit = audit is not None
                elif policy == 'logic_first':
                    do_audit = not logical_available
                else:
                    do_audit = conflict['bound'] > tolerance or not logical_available
                if do_audit and audit is not None and len(oracle.calls) < limits['max_observations']:
                    receipt = oracle.audit(audit['row'],audit['coordinate'])
                    costs.observe(receipt)
                    event = dict(kind='cost_audit',request=index,proposal=audit,receipt=receipt,
                                 choice_reason='known_feasible_cost_ambiguity' if conflict['bound'] > tolerance else 'precision_or_fixed_order',
                                 ambiguity=conflict)
                elif logical_available:
                    if row not in engines:
                        engines[row] = PersistentIHS(instances[row])
                        native_setup += engines[row].setup_meter.total
                    response = engines[row].purchase(query['weights'],query['budget'],limits['native'])
                    purchased.add(key)
                    native_calls += 1
                    native_software += response['adapter_invoice']['total']
                    if response['proof_provider_invoice']:
                        proof_units += response['proof_provider_invoice']['total']
                    if response.get('witness') is not None:
                        w = response['witness']
                        if not any(x['model'] == w['model'] for x in profile['witnesses']):
                            profile['witnesses'].append(copy.deepcopy(w))
                            meter.pay('storage','retained_dynamic_witness',instances[row]['variables']+4)
                    lower_receipt = response.get('checked_lower_receipt')
                    if lower_receipt is not None:
                        if (not lower_receipt['checked'] or lower_receipt['structural_source_id'] != structural_id(instances[row])):
                            raise ValueError('Unchecked or foreign lower receipt')
                        profile['trees'].append(dict(leaf_masks=lower_receipt['leaf_masks'],
                                                    receipt_id=lower_receipt['receipt_id'],
                                                    original_budget=lower_receipt['budget']))
                        meter.pay('storage','retained_dynamic_proof_link_and_masks',len(lower_receipt['leaf_masks'])+8)
                    event = dict(kind='logical_purchase',request=index,row=row,proposal=query,response=response)
                    if response['status'] == 'UNRESOLVED':
                        reason = response.get('reason','native_unresolved')
                else:
                    reason = 'spending_cap_or_no_supported_purchase'
                    break
                steps += 1
                event['certificate_before'] = chosen
                chosen = certificate(profile,costs,price)
                event['certificate_after'] = chosen
                event['cost_state_after'] = costs.snapshot()
                meter.pay('output','purchase_event_fields',32)
                request_events.append(len(events))
                events.append(event)
                if reason:
                    break
            status = 'checked_action' if chosen['bound'] <= tolerance else 'unresolved'
            meter.pay('output','action_and_evidence_response',24)
            requests.append(dict(request=index,row=row,logical_source_id=instances[row]['identity'],
                                 cost_source_id=costs.source_id,price=price,tolerance=tolerance,
                                 status=status,reason=reason,before=before,answer=chosen,
                                 closed_from_cache=before['bound'] <= tolerance,
                                 event_indices=request_events,cost_state=costs.snapshot()))
        states = {str(row):engine.state() for row,engine in engines.items()}
        current_memory = len(canonical(dict(profiles=profiles,costs=costs.snapshot())))
        invoice = dict(software_operation_units=meter.total,
                       native_adapter_operation_units=native_software,
                       native_setup_operation_units=native_setup,
                       proof_provider_operation_units=proof_units,
                       audit_provider_software_units=4*len(oracle.calls),
                       external_cost_observations=len(oracle.calls),
                       native_search_units=None,
                       native_cost_note='Native timings/call counters are separate; no operation-unit conversion.',
                       operation_breakdown=meter.record())
        return dict(policy=policy,representation=representation,requests=requests,events=events,
                    audit_receipts=oracle.calls,invoice=invoice,native_final_states=states,
                    final_profiles=profiles,final_cost_state=costs.snapshot(),
                    retained_certificate_state_bytes=current_memory,
                    summary=dict(requests=len(requests),checked=sum(r['status']=='checked_action' for r in requests),
                                 cache_hits=sum(r['closed_from_cache'] for r in requests),
                                 cost_observations=len(oracle.calls),logical_purchases=native_calls,
                                 unresolved=sum(r['status']=='unresolved' for r in requests)),
                    timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-start))
    finally:
        for engine in engines.values():
            engine.close()


def diagnostic(data,instances,arms):
    """Only after every paid controller has finished; no diagnostic feeds a gate."""
    meter = src.Meter()
    weights = [sum(data['possible_cost_modes'][k][j] for k in data['hidden_modes'])
               for j in range(len(data['possible_cost_modes'][0]))]
    results = []
    for arm in arms:
        rows = []
        for request in arm['requests']:
            instance = copy.deepcopy(instances[request['row']])
            for soft,w in zip(instance['soft'],weights):
                soft['weight'] = w
            values = []
            for model in range(1 << instance['variables']):
                meter.pay('diagnostic','enumerated_assignment')
                try:
                    values.append(src.checked_objective(instance,model,meter))
                except ValueError:
                    pass
            optimum = min(min(values),request['price'])
            a = request['answer']
            actual = request['price'] if a['model'] is None else src.checked_objective(instance,a['model'],meter)
            regret = actual-optimum
            if regret > a['bound']:
                raise AssertionError('Uniform certificate failed at realized cost source')
            rows.append(dict(request=request['request'],actual_action_cost=actual,actual_optimum=optimum,
                             realized_regret=regret,certified_regret=a['bound']))
        results.append(dict(policy=arm['policy'],representation=arm['representation'],rows=rows,
                            sum_realized_regret=sum(r['realized_regret'] for r in rows)))
    return dict(weights=weights,results=results,invoice=meter.record(),
                scope='Post-controller exhaustive diagnostic on DEVELOPMENT fixture; no held-out validation or controller access.')


def execute(input_path, output_path):
    if output_path.exists():
        raise FileExistsError('Preserve earlier runs')
    data = json.loads(input_path.read_text())
    archive_path = S05/'maxsat_repair_results.json'
    if sha(archive_path) != data['logical_archive_sha256']:
        raise ValueError('Logical source archive changed')
    archive = json.loads(archive_path.read_text())
    if sha(src.__file__) != archive['implementation_sha256'] or src.digest(archive['instances']) != archive['source_identity']:
        raise ValueError('Unbound original source/checker')
    # Actual independent re-admission of the raw witnesses/trees. Each arm gets
    # exactly this admitted bank; no historical solver calls are repeated.
    pcpu,pwall = time.process_time_ns(),time.perf_counter_ns()
    initial,shared,trees = raw.acquire_profiles(archive)
    initial_admission = dict(source_and_witness_units=shared.total,proof_and_compilation_units=trees.total,
                            raw_read_and_hash_words=(archive_path.stat().st_size+7)//8+(archive_path.stat().st_size+72)//64,
                            source_identity=archive['source_identity'],raw_archive_sha256=sha(archive_path),
                            historical_acquisition_units=next(a['final']['total_units'] for a in archive['arms'] if a['mode']=='conventional_requested_value'),
                            new_historical_solver_calls=0,
                            timing=dict(process_ns=time.process_time_ns()-pcpu,wall_ns=time.perf_counter_ns()-pwall))
    for profile in initial:
        for j,tree in enumerate(profile['trees']):
            tree['source_receipt'] = f"raw-admission-row-{profile['row']}-tree-{j}"
    result = dict(version=VERSION,evidence='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
                  status='running',start_utc=datetime.now(timezone.utc).isoformat(),
                  source_sha256=sha(input_path),source_identity=data['source_identity'],
                  implementation_sha256=sha(__file__),native_capabilities=capabilities(),
                  dependency_sha256={p.name:sha(p) for p in [Path(src.__file__),Path(raw.__file__)]},
                  initial_admission=initial_admission,arms=[],
                  claims='Callable joint acquisition and uniform finite-cohort action certification. Acquisition policies are proposals, not optimal rules or calibrated expected-value estimates.',
                  monetary_audit_price=None,native_runtime_price=None)
    def save():
        output_path.write_text(json.dumps(result,indent=2)+'\n')
    save()
    for policy in data['policies']:
        arm=run_arm(data,archive['instances'],initial,policy)
        result['arms'].append(arm)
        save()
        print(json.dumps(arm['summary']|{'policy':policy}),flush=True)
    result['diagnostic']=diagnostic(data,archive['instances'],result['arms'])
    result['status']='complete'
    result['end_utc']=datetime.now(timezone.utc).isoformat()
    save()


if __name__ == '__main__':
    command, *args = sys.argv[1:]
    if command == 'prepare':
        prepare(Path(args[0]))
    elif command == 'run':
        execute(Path(args[0]),Path(args[1]))
    else:
        raise ValueError('Use prepare SOURCE or run SOURCE OUTPUT')
