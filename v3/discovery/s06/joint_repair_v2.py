#!/usr/bin/env python3
"""Shared finite-cohort acquisition with paid, reusable contrast compilation.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. This extends, and does
not rewrite, the executed v1. Worst-outcome portfolio scores are information
priorities, not expected values or a theorem about total purchase cost.
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

import joint_repair as old
import native_stream
from native_repair import PersistentIHS, capabilities, structural_id

VERSION = 's06-joint-repair-v2'
HERE = Path(__file__).resolve().parent


class CompiledCosts(old.CostState):
    """Exact row supports. Reuse paid dot products and row subset extrema."""
    def __init__(self, modes, n, source_id, meter):
        super().__init__(modes, n, source_id, meter)
        self.dot_table = {}
        self.row_cache = {}
        self.hits = self.misses = 0

    def support(self, coefficient):
        c = tuple(coefficient)
        if len(c) != self.m:
            raise ValueError('Cost feature meaning changed')
        self.meter.pay('contrast_lookup', 'coefficient_key_and_lookup', self.m+1)
        if c not in self.dot_table:
            self.dot_table[c] = tuple(old.dot(c, v, self.meter, 'contrast_compile') for v in self.modes)
            self.meter.pay('contrast_compile', 'compiled_mode_values_storage', len(self.modes)+self.m)
        values = self.dot_table[c]
        total, point = 0, [0]*self.m
        for choices in self.possible:
            key = (c, choices)
            self.meter.pay('contrast_lookup', 'row_key_and_lookup', self.m+len(choices)+1)
            if key not in self.row_cache:
                value, winner = max((values[k], k) for k in choices)
                self.row_cache[key] = (value, winner)
                self.meter.pay('contrast_update', 'row_maximum_and_record', len(choices)+3)
                self.misses += 1
            else:
                self.hits += 1
            value, winner = self.row_cache[key]
            total += value
            point = [a+b for a,b in zip(point, self.modes[winner])]
            self.meter.pay('contrast_query', 'support_and_argmax_sum', self.m+1)
        return total, point

    def storage(self):
        return dict(compiled_contrasts=len(self.dot_table), row_extrema=len(self.row_cache),
                    row_cache_hits=self.hits, row_cache_misses=self.misses,
                    serialized_bytes=len(old.canonical(dict(dot_table=[(c,v) for c,v in self.dot_table.items()],
                                                           row_cache=[(c,k,v) for (c,k),v in self.row_cache.items()]))))


class Certificates:
    """Shared action/proof templates; no native search or exact optima here."""
    def __init__(self, meter):
        self.meter, self.cache = meter, {}

    def evaluate(self, profile, costs, price):
        # A profile only grows through checked retention. IDs make this usable
        # for rebuilt profiles, without relying on an object's memory address.
        key = (profile['source_identity'], price,
               tuple((w['model'],w['violation_mask']) for w in profile['witnesses']),
               tuple(t['receipt_id'] for t in profile['trees']))
        self.meter.pay('certificate_lookup', 'profile_key_and_lookup', 3+2*len(key[2])+len(key[3]))
        if key not in self.cache:
            templates = []
            trees = profile['trees'] or [dict(leaf_masks=[0],receipt_id='nonnegative_objective')]
            for model,mask in [(w['model'],w['violation_mask']) for w in profile['witnesses']]+[(None,None)]:
                u = old.bits(mask,costs.m) if mask is not None else (0,)*costs.m
                for ti,tree in enumerate(trees):
                    inequalities = []
                    if mask is not None:
                        inequalities.append((u,-price,'replacement'))
                    for leaf in tree['leaf_masks']:
                        v = old.bits(leaf,costs.m)
                        inequalities.append((tuple(a-b for a,b in zip(u,v)),price if mask is None else 0,'proof_leaf'))
                    templates.append((model,mask,ti if profile['trees'] else None,tree['receipt_id'],inequalities))
                    self.meter.pay('certificate_compile','action_proof_constraints',12+(costs.m+4)*len(inequalities))
            self.cache[key] = templates
        templates = self.cache[key]
        supports = {}
        records = []
        for model,mask,ti,proof_id,inequalities in templates:
            candidates = []
            for c,constant,role in inequalities:
                self.meter.pay('certificate_query','local_contrast_lookup',costs.m+1)
                if c not in supports:
                    supports[c] = costs.support(c)
                value,point = supports[c]
                candidates.append((value+constant,c,constant,point,role))
            worst = max(candidates,key=lambda x:x[0])
            records.append(dict(bound=max(0,worst[0]),model=model,mask=mask,
                                action='replace' if mask is None else 'repair',tree_index=ti,proof_id=proof_id,
                                critical_coefficient=list(worst[1]),critical_constant=worst[2],
                                critical_weights=worst[3],critical_role=worst[4]))
            self.meter.pay('certificate_query','constraint_maximum_and_record',len(candidates)+12)
        self.meter.pay('certificate_query','action_proof_minimum',len(records))
        return min(records,key=lambda r:(r['bound'],r['model'] is None,-1 if r['model'] is None else r['model']))


def partitions(costs):
    """Only declared possibilities, never the source's hidden mode indices."""
    for row,choices in enumerate(costs.possible):
        if len(choices) == 1:
            continue
        for j in range(costs.m):
            groups = {}
            for k in choices:
                groups.setdefault(costs.modes[k][j],[]).append(k)
            costs.meter.pay('audit_quote','mode_partition',len(choices)+1)
            if len(groups)>1:
                yield row,j,{value:tuple(ks) for value,ks in groups.items()}


def fixed_audit(costs):
    for row,j,groups in partitions(costs):
        return dict(row=row,coordinate=j,outcomes=sorted(groups),kind='first_informative_coordinate')
    return None


def shared_audit(profiles,costs,suffix,evaluator):
    """Exact worst-outcome decrease of a declared, finite schedule potential.

    Phi=sum max(0,certificate_bound-tolerance), over the current and remaining
    requests, using current checked banks. Pure information purchases do not
    add witnesses or proofs in this forecast. A common possible observation
    outcome conditions all requests together before summing their deficits.
    """
    def potential():
        bounds = [evaluator.evaluate(profiles[d['row']],costs,d['price'])['bound'] for d in suffix]
        costs.meter.pay('audit_quote','portfolio_deficits_and_closures',3*len(bounds))
        return sum(max(0,b-d['tolerance']) for b,d in zip(bounds,suffix)),sum(b<=d['tolerance'] for b,d in zip(bounds,suffix))
    before,closed = potential()
    quotes = []
    # Distinct rows with identical unresolved mode sets are exchangeable for
    # this finite mean and equal audit tariff. Evaluate one representative.
    seen = set()
    for row,j,groups in partitions(costs):
        signature = (costs.possible[row],j)
        costs.meter.pay('audit_quote','exchangeable_row_quote_lookup',len(signature[0])+2)
        if signature in seen:
            continue
        seen.add(signature)
        original = costs.possible[row]
        after = []
        try:
            for value,ks in groups.items():
                costs.possible[row] = ks
                phi,nclosed = potential()
                after.append(dict(value=value,potential=phi,closed=nclosed))
        finally:
            costs.possible[row] = original
        quotes.append(dict(row=row,coordinate=j,outcomes=after,
                           guaranteed_deficit_reduction=before-max(a['potential'] for a in after),
                           possible_deficit_reduction=before-min(a['potential'] for a in after),
                           guaranteed_extra_closures=min(a['closed'] for a in after)-closed,
                           kind='shared_worst_outcome_deficit'))
        costs.meter.pay('audit_quote','quote_record',12+3*len(after))
    if not quotes:
        return None
    chosen = min(quotes,key=lambda a:(-a['guaranteed_deficit_reduction'],-a['guaranteed_extra_closures'],
                                      -a['possible_deficit_reduction'],a['row'],a['coordinate']))
    return dict(chosen=chosen,potential_before=before,closed_before=closed,
                schedule_requests=len(suffix),quotes=quotes,
                assumption='Known finite request suffix, same cohort source, equal external audit price; worst outcomes, no outcome probabilities.')


def retain(profile,response,instance,meter,purchase_id):
    if response.get('witness') is not None:
        w = response['witness']
        if not any(v['model']==w['model'] for v in profile['witnesses']):
            receipt = old.src.digest(dict(source=instance['identity'],model=w['model'],violation_mask=w['violation_mask']))
            profile['witnesses'].append(dict(model=w['model'],violation_mask=w['violation_mask'],receipt_id=receipt,
                                             dependency=dict(purchase=purchase_id)))
            meter.pay('storage','checked_witness_with_source_dependency',instance['variables']+8)
    lower = response.get('checked_lower_receipt')
    if lower is not None:
        if not lower['checked'] or lower['structural_source_id']!=structural_id(instance):
            raise ValueError('Foreign or unchecked lower proof')
        profile['trees'].append(dict(leaf_masks=lower['leaf_masks'],receipt_id=lower['receipt_id'],
                                     original_budget=lower['budget'],dependency=dict(purchase=purchase_id)))
        meter.pay('storage','checked_proof_dependency_and_masks',len(lower['leaf_masks'])+10)


def run_arm(data,instances,initial,policy):
    cpu,wall = time.process_time_ns(),time.perf_counter_ns()
    meter = old.src.Meter()
    costs = CompiledCosts(data['possible_cost_modes'],data['cohort_size'],data['source_identity'],meter)
    oracle = old.CostOracle(data)
    evaluator = Certificates(meter)
    profiles = copy.deepcopy(initial)
    meter.pay('cache_admission','checked_profile_projection',sum(4+3*len(p['witnesses'])+sum(4+len(t['leaf_masks']) for t in p['trees']) for p in profiles))
    engines,purchased,events,requests = {},set(),[],[]
    ncall,native_units,proof_units,setup = 0,0,0,0
    try:
        for index,duty in enumerate(data['schedule']):
            row,price,tau = duty['row'],duty['price'],duty['tolerance']
            profile = profiles[row]
            before = evaluator.evaluate(profile,costs,price)
            chosen,reason,indices = before,None,[]
            for step in range(data['limits']['max_actions_per_request']):
                if chosen['bound']<=tau:
                    break
                query = old.point_query(profile,chosen['critical_weights'],price,tau,meter)
                key = None if query is None else (row,tuple(query['weights']),query['budget'])
                logical = query is not None and key not in purchased and ncall<data['limits']['max_logical_purchases']
                plan = None
                audit = None
                if policy=='audit_first' or not logical:
                    audit = fixed_audit(costs)
                elif policy=='shared_deficit':
                    plan = shared_audit(profiles,costs,data['schedule'][index:],evaluator)
                    if plan is not None:
                        quoted = plan['chosen']
                        if quoted['guaranteed_deficit_reduction']>0:
                            audit = quoted
                        else:
                            conflict = old.ambiguity(profile,costs,chosen,price)
                            if conflict['bound']>tau:
                                audit = quoted
                                plan['fallback_reason']='Known feasible-action cost ambiguity; possible-gain tie-break is exploratory, not a guarantee.'
                elif policy=='certificate_directed':
                    conflict = old.ambiguity(profile,costs,chosen,price)
                    if conflict['bound']>tau:
                        audit = old.audit_choice(costs,conflict['coefficient'],True)
                elif policy!='logic_first':
                    raise ValueError('Unknown policy')
                if audit is not None and len(oracle.calls)<data['limits']['max_observations']:
                    receipt = oracle.audit(audit['row'],audit['coordinate'])
                    costs.observe(receipt)
                    event = dict(kind='cost_audit',request=index,proposal=audit,portfolio_plan=plan,receipt=receipt)
                elif logical:
                    if row not in engines:
                        engines[row] = PersistentIHS(instances[row])
                        setup += engines[row].setup_meter.total
                    response = engines[row].purchase(query['weights'],query['budget'],data['limits']['native'])
                    purchased.add(key)
                    ncall += 1
                    native_units += response['adapter_invoice']['total']
                    if response['proof_provider_invoice']:
                        proof_units += response['proof_provider_invoice']['total']
                    retain(profile,response,instances[row],meter,len(events))
                    event = dict(kind='logical_purchase',request=index,row=row,proposal=query,
                                 portfolio_plan=plan,response=response)
                    if response['status']=='UNRESOLVED':
                        reason = response.get('reason','native_unresolved')
                else:
                    reason = 'spending_cap_or_no_supported_purchase'
                    break
                event['certificate_before'] = chosen
                chosen = evaluator.evaluate(profile,costs,price)
                event['certificate_after'] = chosen
                event['cost_state_after'] = costs.snapshot()
                meter.pay('output','purchase_event_fields',32)
                indices.append(len(events))
                events.append(event)
                if reason:
                    break
            status = 'checked_action' if chosen['bound']<=tau else 'unresolved'
            requests.append(dict(request=index,row=row,logical_source_id=instances[row]['identity'],cost_source_id=costs.source_id,
                                 price=price,tolerance=tau,status=status,reason=reason,before=before,answer=chosen,
                                 closed_from_cache=before['bound']<=tau,event_indices=indices,cost_state=costs.snapshot()))
            meter.pay('output','action_evidence_invoice_fields',24)
        states = {str(row):engine.state() for row,engine in engines.items()}
        timings = [e['timing'] for ev in events if ev['kind']=='logical_purchase'
                   for e in ev['response']['events'] if e['kind'] in ('native_sat','native_hitting_set')]
        storage = costs.storage()
        storage['profile_bytes'] = len(old.canonical(profiles))
        storage['certificate_template_bytes'] = len(old.canonical(list(evaluator.cache.values())))
        return dict(policy=policy,representation='same_compiled_joint_support',requests=requests,events=events,
                    audit_receipts=oracle.calls,final_profiles=profiles,final_cost_state=costs.snapshot(),
                    native_final_states=states,storage=storage,
                    summary=dict(requests=len(requests),checked=sum(r['status']=='checked_action' for r in requests),
                                 cache_hits=sum(r['closed_from_cache'] for r in requests),cost_observations=len(oracle.calls),
                                 logical_purchases=ncall,unresolved=sum(r['status']=='unresolved' for r in requests)),
                    invoice=dict(software_operation_units=meter.total,native_adapter_operation_units=native_units,
                                 native_setup_operation_units=setup,proof_provider_operation_units=proof_units,
                                 audit_provider_software_units=4*len(oracle.calls),external_cost_observations=len(oracle.calls),
                                 operation_breakdown=meter.record(),native_search_units=None),
                    timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall,
                                native_process_ns=sum(t['process_ns'] for t in timings),native_wall_ns=sum(t['wall_ns'] for t in timings)))
    finally:
        for engine in engines.values():
            engine.close()


def execute(input_path,output_path):
    if output_path.exists():
        raise FileExistsError('Preserve exposed runs')
    data = json.loads(input_path.read_text())
    old.CostOracle(data)  # Verify the committed source; does not reveal a cost.
    archive,initial,admission = native_stream.admit_existing_cache()
    if old.sha(old.S05/'maxsat_repair_results.json')!=data['logical_archive_sha256']:
        raise ValueError('Wrong logical source archive')
    result = dict(version=VERSION,status='running',evidence='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
                  start_utc=datetime.now(timezone.utc).isoformat(),source_identity=data['source_identity'],
                  source_sha256=old.sha(input_path),implementation_sha256=old.sha(__file__),
                  dependencies={p.name:old.sha(p) for p in (Path(old.__file__),Path(native_stream.__file__),HERE/'native_repair.py')},
                  capabilities=capabilities(),initial_admission=admission,
                  historical_acquisition_units=77646,arms=[],
                  design='Shared known future request suffix; exact worst-outcome audit deficit forecasts. All controls have identical compact admission, compiled support class, native reuse, proof bridge and spending caps. Policies choose which computations to buy.',
                  pricing='Operation tariffs, external audit count and native timing remain separate. No outcome probabilities, calibrated runtime price or total-cost superiority are assumed.',
                  accounting_limits='Named operation tariffs account modelled primitive work; JSON serialization and memory allocation are timed but not assigned an extra operation tariff. Source-manifest read/hash is common measured setup outside arm counters. Native memory is not measured.')
    def save():
        output_path.write_text(json.dumps(result,indent=2)+'\n')
    save()
    for policy in ('shared_deficit','audit_first','logic_first','certificate_directed'):
        arm = run_arm(data,archive['instances'],initial,policy)
        result['arms'].append(arm)
        save()
        print(json.dumps(arm['summary']|dict(policy=policy)),flush=True)
    result['diagnostic'] = old.diagnostic(data,archive['instances'],result['arms'])
    result['status']='complete'
    result['end_utc']=datetime.now(timezone.utc).isoformat()
    save()


if __name__=='__main__':
    execute(Path(sys.argv[1]),Path(sys.argv[2]))
