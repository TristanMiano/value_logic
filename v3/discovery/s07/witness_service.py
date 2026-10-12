#!/usr/bin/env python3
"""Expanded-menu ordinary acquisition screen: when to propose robust witnesses.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. Both schedules receive
identical source, evidence, MIP and complete-proof services. Native numerical
bounds only guide proposal; actual output comes from the admitted evaluator.
No comparison to an older purchase menu is labeled a matched economic gain.
"""
from datetime import datetime,timezone
from fractions import Fraction as F
import copy
import json
from pathlib import Path
import sys
import time
import bundle_service as shared
from robust_witness import RobustWitness

HERE=Path(__file__).resolve().parent
VERSION='s07-witness-acquisition-screen-v1'


def run(public,oracle,instances,initial,policy,progress):
    meter=shared.native.kernel.Meter()
    cpu,wall=time.process_time_ns(),time.perf_counter_ns()
    costs=shared.compiled.CompiledCosts(public['possible_cost_modes'],public['cohort_size'],public['source_identity'],meter)
    bank=shared.stream.CompactBank(initial,meter)
    evaluator=shared.RepairEvaluator(instances,bank,costs,meter)
    engines={}; queried=set(); events=[]; requests=[]
    wrapper_units=0; current=None
    def save(status='active_prefix'):
        progress(dict(policy=policy,status=status,current_request=current,events=events,requests=requests,
            profiles=bank.rows,cost_state=costs.snapshot(),named_local_units=meter.total,
            complete_wrapper_units=wrapper_units,
            timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall)))
    def audit(action):
        receipt=oracle.audit(action['row'],action['coordinate'])
        costs.observe(receipt)
        meter.pay('output','cost_audit_record',16)
        events.append(dict(kind='audit',request=current,receipt=receipt,cost_state=costs.snapshot()))
        save()
    def propose(row,price,tau):
        lowers=evaluator.mode_anchor_lowers(row)
        key=(row,price,tuple(tuple(p) for p in costs.possible),tuple(lowers))
        meter.pay('controller','actual_evidence_state_proposal_lookup',8+sum(map(len,costs.possible))+len(lowers))
        if key in queried:
            return False
        if sum(e['kind']!='audit' for e in events)>=public['limits']['max_logical_purchases']:
            raise RuntimeError('Expanded-menu logical call cap')
        queried.add(key)
        setup=None
        if row not in engines:
            engines[row]=RobustWitness(instances[row],costs,meter)
            setup=dict(invoice=engines[row].setup_invoice,timing=engines[row].setup_timing,state=engines[row].state())
        before=evaluator.evaluate(row,price,tau)
        save('native_witness_attempt_started')
        got=engines[row].propose(costs,lowers,price,seconds=.1,nodes=1000)
        bank.retain(row,got,len(events))
        after=evaluator.evaluate(row,price,tau)
        meter.pay('output','native_proposal_and_checked_gate_record',28)
        events.append(dict(kind='robust_witness',request=current,row=row,setup=setup,response=got,
            before=before,after=after,strict_bound_improvement=after['bound']<before['bound']))
        save()
        return True
    def complete(row,price,tau):
        nonlocal wrapper_units
        if sum(e['kind']!='audit' for e in events)>=public['limits']['max_logical_purchases']:
            raise RuntimeError('Expanded-menu logical call cap')
        if any(len(p)!=1 for p in costs.possible):
            raise AssertionError('This schedule reserves its complete query after the cost state is a singleton')
        q=[sum(costs.modes[p[0]][j] for p in costs.possible) for j in range(costs.m)]
        bank.set_weights(q)
        bounds=bank.bounds(row)
        budget=min(bounds['upper'],price)-tau-1
        if type(budget) is not int:
            raise ValueError('Current fixed-source target budget must be integral')
        save('complete_fallback_attempt_started')
        got=shared.contract_quote.execute_complete(shared.native.weighted_instance(instances[row],q),budget)
        wrapper_units+=got['total_operation_units']
        shared.retain_complete(bank,row,instances[row],got,len(events))
        meter.pay('output','complete_fallback_receipt_record',20)
        events.append(dict(kind='complete',request=current,row=row,weights=q,budget=budget,response=got))
        save()
    for current,duty in enumerate(public['schedule']):
        row,price,tau=duty['row'],duty['price'],duty['tolerance']
        before=evaluator.evaluate(row,price,tau);answer=before;first=len(events)
        save()
        for _ in range(public['limits']['max_actions_per_request']):
            if answer['bound']<=tau:
                break
            action=shared.compiled.fixed_audit(costs)
            if policy=='witness_before_audit' or action is None:
                propose(row,price,tau)
                answer=evaluator.evaluate(row,price,tau)
                if answer['bound']<=tau:
                    break
            if action is not None:
                if len(oracle.calls)>=public['limits']['max_observations']:
                    raise RuntimeError('Cost audit cap')
                audit(action)
            else:
                complete(row,price,tau)
            answer=evaluator.evaluate(row,price,tau)
        meter.pay('output','final_checked_action_source_invoice',28)
        requests.append(dict(request=current,row=row,price=price,tolerance=tau,before=before,answer=answer,
            status='checked_action' if answer['bound']<=tau else 'unresolved',
            closed_from_cache=before['bound']<=tau,event_indices=list(range(first,len(events))),cost_state=costs.snapshot()))
        save()
    counts={kind:sum(e['kind']==kind for e in events) for kind in ('audit','complete','robust_witness')}
    named=meter.total+wrapper_units+4*counts['audit']
    states={str(row):engine.state() for row,engine in engines.items()}
    return dict(policy=policy,version=VERSION,requests=requests,events=events,final_profiles=bank.rows,
        final_cost_state=costs.snapshot(),native_final_states=states,
        summary=dict(requests=len(requests),checked=sum(r['status']=='checked_action' for r in requests),
            cache_hits=sum(r['closed_from_cache'] for r in requests),cost_observations=counts['audit'],
            complete_calls=counts['complete'],robust_witness_calls=counts['robust_witness'],
            logical_purchases=counts['complete']+counts['robust_witness'],
            witness_calls_with_strict_bound_improvement=sum(e.get('strict_bound_improvement',False) for e in events),
            native_unresolved=sum(e['response']['status']=='UNRESOLVED' for e in events if e['kind']=='robust_witness'),
            unresolved=sum(r['status']=='unresolved' for r in requests),largest_final_bound=max(r['answer']['bound'] for r in requests)),
        invoice=dict(controller_and_interface_units=meter.total,complete_wrapper_units=wrapper_units,
            audit_provider_software_units=4*counts['audit'],operation_units=named,breakdown=meter.record(),
            symbolic_full_cost='Common S + U + a*A + rho*T + s*B + all remaining actual fees',
            note='All native proposal setup/API/checking units are in the shared local meter. Native search has CPU/wall/call/node evidence, no invented operation conversion; prices/byte-time/peak memory are unassigned.'),
        storage=dict(profile_bytes=len(shared.canonical(bank.rows)),cost_support=costs.storage(),
            native_observable_state_bytes=len(shared.canonical(states)),
            events_bytes=len(shared.canonical(events)),native_resident_allocator_bytes=None),
        timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))


def execute(output):
    if output.exists():
        raise FileExistsError('Preserve actual expanded-menu acquisitions')
    input_path=HERE.parent/'s06'/'joint_source.json'
    data=json.loads(input_path.read_text())
    public={k:copy.deepcopy(v) for k,v in data.items() if k!='hidden_modes'}
    result=dict(version=VERSION,status='prospectively_prepared',evidence='DEVELOPMENT expanded-menu opportunity screen',
        contributor='ChatGPT (GPT-6 Astra Pro)',start_utc=datetime.now(timezone.utc).isoformat(),
        source_sha256=shared.joint.sha(input_path),source_identity=data['source_identity'],
        implementation_sha256=shared.joint.sha(__file__),dependencies={p.name:shared.joint.sha(p) for p in
            [HERE/'bundle_service.py',HERE/'robust_witness.py',HERE/'repair_interface.py',HERE.parent/'s06'/'native_stream.py']},
        policies=['witness_before_audit','audit_before_witness'],
        contract='Same expanded menu and all current caps for both new schedules. At most one native proposal per actual source/lower state, retaining own warm state; no probability of success or native lower certificate. Old a01/a03 invoices are context, not a matched menu comparison.',arms=[])
    def save():
        output.write_text(json.dumps(result,indent=2,default=shared.encode)+'\n')
    save()
    archive,initial,admission=shared.stream.admit_existing_cache()
    result['initial_admission']=admission
    result['code_admission']=shared.contract_guard.admit()
    result['historical_acquisition_units']=77646
    result['common_current_units']=admission['total_declared_units']+result['code_admission']['declared_admission_units']
    try:
        for policy in result['policies']:
            def progress(prefix):
                result['active_prefix']=prefix;save()
            got=run(public,shared.joint.CostOracle(data),archive['instances'],initial,policy,progress)
            result['arms'].append(got);result.pop('active_prefix',None);save()
            print(json.dumps(got['summary']|dict(policy=policy,operation_units=got['invoice']['operation_units']),default=shared.encode),flush=True)
        result.update(status='complete',end_utc=datetime.now(timezone.utc).isoformat())
    except BaseException as exc:
        result.update(status='interrupted_or_failed',error=dict(type=type(exc).__name__,message=str(exc)));save();raise
    save()


if __name__=='__main__':
    execute(Path(sys.argv[1]))
