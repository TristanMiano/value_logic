#!/usr/bin/env python3
"""Complete, source-bound audit/proof bundles on a finite repair service.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12.
Plans condition on public possible cost modes, not hidden modes or optima.
All hypothetical audit outcomes are included; only executed branches acquire
receipts. The symbolic price expression retains the unquoted host/storage
remainder. A displayed numerical slice is a policy parameter, not a measured
external price or a prospective CPU guarantee.
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
S06 = HERE.parent / 's06'
sys.path.insert(0, str(S06))
import anchor_quotes
import contract_guard
import contract_quote
import joint_repair as joint
import joint_repair_v2 as compiled
import native_repair as native
import native_stream as stream
import lattice_quotes
import row_margins
from compiled_quotes import PreparedQuotes
from repair_interface import RepairEvaluator

VERSION = 's07-complete-bundle-v3'


def encode(obj):
    if isinstance(obj, F):
        return obj.numerator if obj.denominator == 1 else str(obj)
    raise TypeError(type(obj).__name__)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), default=encode).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


class BundlePlanner:
    """Depth-bounded robust audit tree ending in a checked complete proof reserve.

    Source rows with the same possible mode set are exchangeable for a cohort
    sum and equal observation fee. Plans name that set, then execution resolves
    the actual row identity. This permits cached quotations across equivalent
    public states without sharing unpurchased observations.
    """

    def __init__(self, instances, bank, costs, evaluator, meter, audit_rate=1000,
                 depth=1, methods=('tree', 'scalar_anchor')):
        self.instances, self.bank, self.costs = instances, bank, costs
        self.evaluator, self.meter = evaluator, meter
        self.audit_rate, self.depth, self.methods = audit_rate, depth, methods
        self.cache = {}
        self.enclosures, self.margin_cache = {}, {}
        self.prepared = PreparedQuotes(costs.modes, costs.n, meter)
        self.stats = dict(quote_nodes=0, quote_cache_hits=0, logical_quotes=0,
                          completed_plans=0, audit_outcomes_quoted=0,
                          bracket_width_rejections=0, margin_compilations=0,
                          margin_cache_hits=0, strict_row_margin_improvements=0)
        self.wrapper_caps = []
        for instance in instances:
            quote = contract_quote.finite_call_quote(instance)
            self.wrapper_caps.append(quote['complete_wrapper_units'])
            meter.pay('bundle_quote', 'source_length_and_complete_call_quote',
                      16 + sum(1+len(c) for c in instance['hard']) + 4*len(instance['soft']))

    def fingerprint(self, row, price, tau, depth):
        profile = self.bank.rows[row]
        return (row, price, tau, depth, tuple(sorted(tuple(p) for p in self.costs.possible)),
                tuple((w['model'], w['violation_mask'], w['receipt_id']) for w in profile['witnesses']),
                tuple(t['receipt_id'] for t in profile['trees']))

    def paths(self, plan):
        if plan['kind'] == 'terminal':
            return [dict(audits=0, complete_calls=0, wrapper_units_cap=0)]
        if plan['kind'] in ('logical', 'bracket'):
            calls = plan.get('max_complete_calls', 1)
            return [dict(audits=0, complete_calls=calls, wrapper_units_cap=calls*plan['wrapper_units_cap'])]
        paths = []
        for outcome in plan['outcomes']:
            for child in self.paths(outcome['plan']):
                paths.append(child | dict(audits=child['audits']+1))
        unique = {tuple(v.values()): v for v in paths}
        self.meter.pay('bundle_quote', 'all_outcome_resource_path_composition', 5*len(paths)+1)
        return list(unique.values())

    def score(self, plan):
        paths = self.paths(plan)
        # Conditional slice sigma=1, a=audit_rate, equal branch-independent
        # unquoted remainders. The full remainder is never asserted zero.
        score = max(p['audits']*self.audit_rate+p['wrapper_units_cap'] for p in paths)
        self.meter.pay('bundle_quote', 'conditional_symbolic_price_slice', 4*len(paths)+1)
        return score

    def enclosure(self):
        c = self.costs
        key = tuple(sorted(tuple(p) for p in c.possible))
        self.meter.pay('bundle_lookup', 'public_enclosure_multiset_key',
                       3*sum(map(len,c.possible))+c.n*c.n+2)
        if key in self.enclosures:
            return self.enclosures[key]
        lo = [sum(min(c.modes[k][j] for k in p) for p in c.possible) for j in range(c.m)]
        hi = [sum(max(c.modes[k][j] for k in p) for p in c.possible) for j in range(c.m)]
        row_mid = [sum((min(c.modes[k][j] for k in p)+max(c.modes[k][j] for k in p))//2
                       for p in c.possible) for j in range(c.m)]
        answer = dict(key=key,lo=lo,hi=hi,row_midpoint_sum=row_mid,
                      maximum_coordinate_width=max(h-l for l,h in zip(lo,hi)))
        self.meter.pay('bundle_compile','public_enclosure_and_row_midpoints',
                       5*c.m*sum(map(len,c.possible))+5*c.n*c.m+2*c.m)
        self.meter.pay('bundle_storage','public_enclosure_key_and_value_words',
                       sum(map(len,key))+len(key)+3*c.m+5)
        self.enclosures[key] = answer
        return answer

    def q_menu(self, current, enclosure):
        c = self.costs
        lo,hi = enclosure['lo'],enclosure['hi']
        menu = [lo, [(l+h)//2 for l,h in zip(lo,hi)], hi,enclosure['row_midpoint_sum']]
        tree = current.get('method_answers', {}).get('tree', current)
        critical = tree.get('critical_weights')
        if critical is not None:
            menu.append(critical)
        menu.extend([[c.n*w for w in mode] for mode in c.modes])
        self.meter.pay('bundle_quote', 'public_objective_menu_and_deduplication',
                       3*(len(menu)+2)*c.m)
        return list(dict.fromkeys(tuple(v) for v in menu if any(v)))

    def leaf(self, row, price, tau, current):
        if current['bound'] <= tau:
            return dict(kind='terminal', worst_bound=current['bound'], answer=current)
        profile = self.bank.rows[row]
        masks = [w['violation_mask'] for w in profile['witnesses']]
        lowers = self.evaluator.mode_anchor_lowers(row)
        enclosure = self.enclosure()
        complete = []
        for q in self.q_menu(current,enclosure):
            got = self.prepared.closing_query(masks,self.costs.possible,lowers,price,list(q),tau)
            self.stats['logical_quotes'] += 1
            if got.get('closes'):
                quote = got['quote']
                complete.append(dict(kind='logical', weights=list(q), budget=quote['budget'],
                                     worst_bound=quote['worst_bound'], quotation=quote,
                                     wrapper_units_cap=self.wrapper_caps[row]))
            # A leaf may reserve more than one proof. Known objective-only
            # transfer margins suffice to quote a complete clipped bracket
            # without enumerating logical models or possible proof replies.
            bracket = self.bracket(row, price, tau, q, enclosure)
            if bracket is not None:
                complete.append(bracket)
        if not complete:
            return None
        self.meter.pay('bundle_quote', 'completed_logical_menu_selection', len(complete)+1)
        return min(complete, key=lambda p:(self.score(p),p['worst_bound'],sum(p['weights']),p.get('budget',0),p['weights']))

    def bracket(self, row, price, tau, q, enclosure):
        c = self.costs
        # A margin valid on *all* Boolean masks has alpha+delta >= hi_j-lo_j:
        # apply both inequalities to e_j and sum. This safely rejects an
        # impossible residual budget before paying to tighten either margin.
        self.meter.pay('bundle_quote','boolean_coordinate_width_necessary_condition',2)
        if enclosure['maximum_coordinate_width'] > tau:
            self.stats['bracket_width_rejections'] += 1
            return None
        key = (enclosure['key'],tuple(q))
        self.meter.pay('bundle_lookup','row_margin_numerical_key',c.n+c.m+2)
        if key in self.margin_cache:
            margin = self.margin_cache[key]
            self.stats['margin_cache_hits'] += 1
        else:
            margin = row_margins.margins(c.modes,c.possible,list(q),self.meter)
            self.margin_cache[key] = margin
            self.stats['margin_compilations'] += 1
            self.stats['strict_row_margin_improvements'] += margin['strict_improvement']
            self.meter.pay('bundle_storage','row_margin_key_and_reconstruction_words',
                           sum(map(len,enclosure['key']))+c.n+c.m+12+4*c.n*c.m)
        alpha,delta = margin['alpha'],margin['delta']
        residual = alpha+delta
        if residual > tau:
            return None
        self.bank.set_weights(list(q))
        bounds = self.bank.bounds(row)
        lower,upper = min(bounds['lower'],price),min(bounds['upper'],price)
        if any(F(x).denominator != 1 for x in (lower,upper,price)):
            raise ValueError('The complete midpoint reserve requires integral clipped brackets')
        gap,calls = int(upper-lower),0
        gaps = [gap]
        while gap > tau-residual:
            gap //= 2
            calls += 1
            gaps.append(gap)
        if calls == 0:
            # Existing profile already supports the conservative envelope.
            # Its actual fixed-action evaluator is the output boundary.
            return None
        self.meter.pay('bundle_quote','complete_integer_bracket_reserve',8+3*len(gaps))
        return dict(kind='bracket',weights=list(q),initial_query_lower=lower,initial_query_upper=upper,
                    alpha=alpha,delta=delta,worst_bound=gap+residual,
                    margin_quotation=margin,
                    maximum_gap_sequence=gaps,max_complete_calls=calls,
                    wrapper_units_cap=self.wrapper_caps[row],
                    guarantee='Every checked complete midpoint reply halves the integral clipped q-gap; source transfer adds at most alpha+delta. No native deadline or reply probability.')

    def quote(self, row, price, tau, depth=None):
        depth = self.depth if depth is None else depth
        key = self.fingerprint(row, price, tau, depth)
        self.meter.pay('bundle_lookup', 'evidence_and_exchangeable_state_key',
                       10+sum(map(len, self.costs.possible))+len(key[-1])+3*len(key[-2]))
        if key in self.cache:
            self.stats['quote_cache_hits'] += 1
            return copy.deepcopy(self.cache[key])
        self.stats['quote_nodes'] += 1
        current = self.evaluator.evaluate(row, price, tau, methods=self.methods)
        direct = self.leaf(row, price, tau, current)
        if direct is not None and direct['kind'] == 'terminal':
            self.cache[key] = direct
            return copy.deepcopy(direct)
        plans = [] if direct is None else [direct]
        if depth:
            seen = set()
            for i, possible in enumerate(self.costs.possible):
                signature = tuple(possible)
                if len(possible) < 2 or signature in seen:
                    continue
                seen.add(signature)
                partitions = {}
                for j in range(self.costs.m):
                    groups = {}
                    for mode in possible:
                        groups.setdefault(self.costs.modes[mode][j], []).append(mode)
                    self.meter.pay('bundle_quote', 'public_complete_audit_partition', len(possible)+1)
                    if len(groups) < 2:
                        continue
                    # Identical partitions have identical information; keep
                    # the first equally priced coordinate. Values are carried
                    # from that coordinate, never mixed across coordinates.
                    partition_key = tuple(sorted(tuple(v) for v in groups.values()))
                    if partition_key in partitions:
                        continue
                    partitions[partition_key] = j
                    outcomes = []
                    old = self.costs.possible[i]
                    try:
                        for value, compatible in sorted(groups.items()):
                            self.costs.possible[i] = tuple(compatible)
                            child = self.quote(row, price, tau, depth-1)
                            self.stats['audit_outcomes_quoted'] += 1
                            if child is None:
                                break
                            outcomes.append(dict(value=value, compatible=compatible, plan=child))
                    finally:
                        self.costs.possible[i] = old
                    if len(outcomes) == len(groups):
                        plans.append(dict(kind='audit', mode_set=list(signature), coordinate=j,
                                          outcomes=outcomes, worst_bound=max(x['plan']['worst_bound'] for x in outcomes)))
        answer = None if not plans else min(plans, key=lambda p:(self.score(p), p['worst_bound'], p['kind']))
        if answer is not None:
            answer = copy.deepcopy(answer)
            answer['resource_paths'] = self.paths(answer)
            answer['price_quote'] = dict(expression='Q_sunk + max_path(a*audits + sigma*wrapper_units_cap + H_path)',
                symbols=dict(a='external audit charge beyond separately modelled provider software work',
                             sigma='price per named complete-wrapper operation',
                             H_path='remaining local observation/check/update/output, CPU, memory, serialization and retention charge not included in the wrapper or external audit fee'),
                conditional_selection_slice=dict(a_over_sigma=self.audit_rate,
                    H_path='equal branch-independent remainder for the displayed slice; an assumption, not an observed fee'),
                cost_guarantee='Certificate completion covers every compatible normal-execution outcome. Full monetary ceiling is conditional on finite all-in H_path quotations; CPU/host/deadline not supplied.')
            self.stats['completed_plans'] += 1
        self.cache[key] = answer
        return copy.deepcopy(answer)


def retain_complete(bank, row, instance, got, purchase):
    response = dict(source_identity=instance['identity'], witness=got.get('witness'), checked_lower_receipt=None)
    if 'leaf_masks' in got:
        response['checked_lower_receipt'] = dict(checked=True, receipt_id=got['receipt_id'],
                    leaf_masks=got['leaf_masks'], budget=got['budget'])
    bank.retain(row, response, purchase)


def run_arm(public, oracle, instances, initial, policy, audit_rate=1000, depth=1, progress=None):
    start_cpu, start_wall = time.process_time_ns(), time.perf_counter_ns()
    meter = native.kernel.Meter()
    costs = compiled.CompiledCosts(public['possible_cost_modes'], public['cohort_size'], public['source_identity'], meter)
    bank = stream.CompactBank(initial, meter)
    evaluator = RepairEvaluator(instances, bank, costs, meter)
    planner_setup_start = meter.total
    planner = BundlePlanner(instances, bank, costs, evaluator, meter, audit_rate, depth) if policy == 'bundle' else None
    planner_initialization_units = meter.total-planner_setup_start
    events, requests, plans, engines = [], [], [], {}
    purchased = set()
    wrapper_units = native_units = native_proof_units = native_setup_units = 0
    max_events, max_observations, max_logical = 80, 64, 128
    current_row = current_request = None

    def preserve():
        if progress is not None:
            progress(dict(policy=policy, status='active_prefix', requests=requests, events=events, plans=plans,
                current_request=current_request, cost_state=costs.snapshot(), profiles=bank.rows,
                invoice=dict(controller_and_interface_units=meter.total,complete_wrapper_units=wrapper_units,
                    native_adapter_units=native_units,native_proof_units=native_proof_units,
                    native_setup_units=native_setup_units,audit_provider_software_units=4*len(oracle.calls)),
                timing=dict(process_ns=time.process_time_ns()-start_cpu,wall_ns=time.perf_counter_ns()-start_wall)))

    def evaluate(row, price, tau):
        return evaluator.evaluate(row, price, tau)

    def audit(mode_set, coordinate):
        row = next(i for i,p in enumerate(costs.possible) if tuple(p) == tuple(mode_set))
        receipt = oracle.audit(row, coordinate)
        costs.observe(receipt)
        meter.pay('output', 'audit_event_record', 16)
        events.append(dict(kind='audit', request=current_request, receipt=receipt, state=costs.snapshot()))
        preserve()
        return receipt['value']

    def logical(q, budget, use_native=False):
        nonlocal wrapper_units, native_units, native_proof_units, native_setup_units
        if len(purchased) >= max_logical:
            raise RuntimeError('Logical purchase cap')
        source = instances[current_row]
        key = (current_row, tuple(q), budget, use_native)
        purchased.add(key)
        before = meter.total
        if use_native:
            if current_row not in engines:
                engines[current_row] = native.PersistentIHS(source)
                native_setup_units += engines[current_row].setup_meter.total
            got = engines[current_row].purchase(q, budget, public['limits']['native'])
            native_units += got['adapter_invoice']['total']
            if got.get('proof_provider_invoice'):
                native_proof_units += got['proof_provider_invoice']['total']
            bank.retain(current_row, got, len(events))
            events.append(dict(kind='native', request=current_request, row=current_row, weights=q,
                               budget=budget, response=got))
            preserve()
            if got['status'] != 'UNRESOLVED':
                return
            # An unresolved warm attempt remains paid; complete fallback is a
            # separate reserved purchase at the identical source/objective.
        weighted = native.weighted_instance(source, q)
        got = contract_quote.execute_complete(weighted, budget)
        wrapper_units += got['total_operation_units']
        retain_complete(bank, current_row, source, got, len(events))
        meter.pay('output', 'logical_receipt_and_retention_record', 20)
        events.append(dict(kind='complete', request=current_request, row=current_row, weights=q,
                           budget=budget, response=got, local_postprocessing_units=meter.total-before))
        preserve()

    def execute_plan(plan):
        if plan['kind'] == 'terminal':
            return
        if plan['kind'] == 'logical':
            logical(plan['weights'], plan['budget'])
            return
        if plan['kind'] == 'bracket':
            duty = public['schedule'][current_request]
            q, price, tau = plan['weights'],duty['price'],duty['tolerance']
            for _ in range(plan['max_complete_calls']):
                if evaluate(current_row,price,tau)['bound'] <= tau:
                    return
                bank.set_weights(q)
                b = bank.bounds(current_row)
                lower,upper = min(b['lower'],price),min(b['upper'],price)
                if upper-lower <= tau-plan['alpha']-plan['delta']:
                    raise AssertionError('Transfer reserve closed but actual default evaluator failed')
                logical(q,int((lower+upper)//2))
            return
        if len(oracle.calls) >= max_observations:
            raise RuntimeError('Cost observation cap')
        value = audit(plan['mode_set'], plan['coordinate'])
        child = next(c for c in plan['outcomes'] if c['value'] == value)
        execute_plan(child['plan'])

    try:
        for current_request, duty in enumerate(public['schedule']):
            current_row, price, tau = duty['row'], duty['price'], duty['tolerance']
            before = evaluate(current_row, price, tau)
            answer, first_event = before, len(events)
            for _ in range(max_events):
                if answer['bound'] <= tau:
                    break
                plan = None
                if policy == 'bundle':
                    quote_start = meter.total
                    plan = planner.quote(current_row, price, tau)
                    plans.append(dict(request=current_request, before=answer, plan=plan,
                                      quote_units=meter.total-quote_start, state=costs.snapshot()))
                if plan is not None:
                    execute_plan(plan)
                    answer = evaluate(current_row, price, tau)
                    if answer['bound'] > tau:
                        raise AssertionError('Executed complete bundle did not meet its quoted tolerance')
                    break
                first_audit = compiled.fixed_audit(costs)
                point = None
                if policy in ('logic_first', 'native_logic'):
                    tree = answer['method_answers']['tree']
                    point = joint.point_query(bank.rows[current_row], tree['critical_weights'], price, tau, meter)
                    if point is not None and (current_row,tuple(point['weights']),point['budget'],policy=='native_logic') in purchased:
                        point = None
                if policy in ('bundle', 'audit_first') and first_audit is not None:
                    audit(costs.possible[first_audit['row']], first_audit['coordinate'])
                elif point is not None:
                    logical(point['weights'], point['budget'], policy == 'native_logic')
                elif first_audit is not None:
                    audit(costs.possible[first_audit['row']], first_audit['coordinate'])
                else:
                    q = [sum(costs.modes[p[0]][j] for p in costs.possible) for j in range(costs.m)]
                    bank.set_weights(q)
                    bounds = bank.bounds(current_row)
                    low, high = min(bounds['lower'],price), min(bounds['upper'],price)
                    if high-low <= tau:
                        raise AssertionError('Pointwise gate is closed but uniform singleton evaluator is not')
                    logical(q, (low+high)//2, policy == 'native_logic')
                answer = evaluate(current_row, price, tau)
            meter.pay('output', 'checked_action_source_evidence_invoice', 28)
            requests.append(dict(request=current_request, row=current_row, price=price, tolerance=tau,
                status='checked_action' if answer['bound'] <= tau else 'unresolved', before=before, answer=answer,
                closed_from_cache=before['bound'] <= tau, event_indices=list(range(first_event,len(events))),
                cost_state=costs.snapshot()))
            preserve()
        numerical_storage = {}
        if planner is not None:
            prepared_cache = {name:list(getattr(planner.prepared,name).items()) for name in
                ('_mask_costs','_objectives','_raw_states','_states','_bases','_uppers')}
            numerical_storage = dict(
                prepared_quote_cache_bytes=len(canonical(prepared_cache)),
                prepared_quote_stored_words=planner.prepared.stored_words,
                enclosure_cache_bytes=len(canonical(list(planner.enclosures.items()))),
                margin_cache_bytes=len(canonical(list(planner.margin_cache.items()))),
                scope='Serialized retained numerical payloads, not a measurement of peak allocator memory or byte-time')
            meter.pay('output','retained_quote_payload_size_record',16)
        elapsed = dict(process_ns=time.process_time_ns()-start_cpu,wall_ns=time.perf_counter_ns()-start_wall)
        counts = {k:sum(e['kind']==k for e in events) for k in ('audit','complete','native')}
        result = dict(policy=policy, version=VERSION, requests=requests, events=events, plans=plans,
            final_profiles=bank.rows, final_cost_state=costs.snapshot(), native_final_states={str(k):v.state() for k,v in engines.items()},
            summary=dict(requests=len(requests),checked=sum(r['status']=='checked_action' for r in requests),
                         cache_hits=sum(r['closed_from_cache'] for r in requests),cost_observations=counts['audit'],
                         complete_calls=counts['complete'],native_attempts=counts['native'],logical_purchases=counts['complete']+counts['native'],
                         unresolved=sum(r['status']=='unresolved' for r in requests),
                         executed_complete_bundles=sum(p['plan'] is not None for p in plans),
                         quoted_unclosed_states=sum(p['plan'] is None for p in plans),
                         largest_final_bound=max(r['answer']['bound'] for r in requests)),
            invoice=dict(controller_and_interface_units=meter.total,complete_wrapper_units=wrapper_units,
                         planner_initialization_units=planner_initialization_units,
                         native_adapter_units=native_units,native_proof_units=native_proof_units,native_setup_units=native_setup_units,
                         audit_provider_software_units=4*counts['audit'],external_audits=counts['audit'],
                         operation_units=meter.total+wrapper_units+native_units+native_proof_units+native_setup_units+4*counts['audit'],
                         breakdown=meter.record(),symbolic_full_cost='U + a*A + rho*T + s*B + other_actual_external_fees',
                         external_audit_price=None,native_search_operation_units=None,
                         note='No conversion of measured host time/storage into a fee; no omitted component is assigned zero.'),
            planner_stats=planner.stats if planner else {},prepared_quote_stats=planner.prepared.stats if planner else {},
            timing=elapsed,storage=dict(profile_bytes=len(canonical(bank.rows)),
                planner_cache_bytes=len(canonical(list(planner.cache.values()))) if planner else 0,
                quotation_payload=numerical_storage,cost_support=costs.storage()))
        return result
    finally:
        for engine in engines.values():
            engine.close()


def execute(input_path, output, policies=('bundle','audit_first','logic_first','native_logic'), depth=1):
    if output.exists():
        raise FileExistsError('Preserve actual acquisition output')
    data = json.loads(input_path.read_text())
    # Only the provider receives hidden source outcomes; every arm receives
    # exactly these public bytes and its own paid source-bound oracle.
    public = {k:copy.deepcopy(v) for k,v in data.items() if k != 'hidden_modes'}
    archive, initial, admission = stream.admit_existing_cache()
    code_admission = contract_guard.admit()
    if joint.sha(joint.S05/'maxsat_repair_results.json') != data['logical_archive_sha256']:
        raise ValueError('Changed logical source')
    result = dict(version=VERSION,status='running',evidence='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
        start_utc=datetime.now(timezone.utc).isoformat(),source_sha256=joint.sha(input_path),source_identity=data['source_identity'],
        implementation_sha256=joint.sha(__file__),dependencies={p.name:joint.sha(p) for p in
            [Path(lattice_quotes.__file__),Path(row_margins.__file__),HERE/'compiled_quotes.py',HERE/'repair_interface.py',
             S06/'contract_quote.py',S06/'native_stream.py',S06/'native_repair.py']},
        initial_admission=admission,complete_code_admission=code_admission,historical_acquisition_units=77646,
        common_current_units=admission['total_declared_units']+code_admission['declared_admission_units'],
        configuration=dict(depth=depth,audit_price_slice=1000,policies=list(policies)),arms=[])
    def save():
        output.write_text(json.dumps(result,indent=2,default=encode)+'\n')
    save()
    try:
        for policy in policies:
            def progress(prefix):
                result['active_prefix'] = prefix
                save()
            arm = run_arm(public,joint.CostOracle(data),archive['instances'],initial,policy,depth=depth,progress=progress)
            result['arms'].append(arm)
            result.pop('active_prefix',None)
            save()
            print(json.dumps(arm['summary'] | dict(policy=policy,operation_units=arm['invoice']['operation_units']),default=encode),flush=True)
        result.update(status='complete',end_utc=datetime.now(timezone.utc).isoformat())
    except BaseException as exc:
        result.update(status='interrupted_or_failed',error=dict(type=type(exc).__name__,message=str(exc)))
        save()
        raise
    save()


if __name__ == '__main__':
    execute(Path(sys.argv[1]),Path(sys.argv[2]),depth=int(sys.argv[3]) if len(sys.argv)>3 else 1)
