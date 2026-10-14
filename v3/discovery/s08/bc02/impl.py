"""bc02 frozen paid budget policy, Codex (GPT-6), DEVELOPMENT."""
from pathlib import Path
import json
import random
import sys
import time
import anchor_cover as ac
import budget_cover as bc
from anchor_service import rows
op=ac.op;safe=ac.safe;Meter=ac.Meter;g01=ac.g01;HERE=ac.HERE

def compile_budget(case,geometry):
    data=op.source(case);meter=Meter();op.admit(case,data,geometry,meter);Q=case['H']*sum(case['weights']);C=case['fees'][-1]
    planner=bc.Planner(data['supports'],case['fees'],Q,lambda s,m:ac.utility(case,s,m),1);nodes={}
    def visit(state):
        key=op.state_key(state)
        if key in nodes:return nodes[key]['value']
        b=C-sum(case['fees'][i] for i,v in enumerate(state[:-1]) if v is not None)
        query=planner.choose(state,b);meter.pay('compilation','selected_budget_policy_state',12+len(state))
        if query is None:nodes[key]=dict(value=0,action=ac.action(case,state,meter));return 0
        values=[]
        for v in data['supports'][query]:
            child=list(state);child[query]=v;values.append(visit(tuple(child)));meter.pay('compilation','selected_budget_policy_response',7+len(state))
        value=case['fees'][query]+max(values);nodes[key]=dict(value=value,query=query);return value
    initial=(None,)*len(data['supports']);value=visit(initial);meter.pay('preparation','all_actual_lookahead_states',planner.meter.total)
    assert value<=2*C
    return dict(source=data['identity'],price=case['A'],tau=Q,root=op.state_key(initial),value=value,nodes=nodes),dict(invoice=meter.record(),states=len(nodes),lookahead_states=planner.value.cache_info().currsize)

def prepare(root):
    root.mkdir(exist_ok=False);design=json.loads((HERE/'ac02/design.json').read_text());design['arms']=['budget','ordinary_budget','cover','anchor']
    for j,case in enumerate(design['cases']):case['seed']=8141740+j
    design.update(source_sha256=g01.sha(__file__),dependencies={name:g01.sha(HERE/name) for name in('budget_cover.py','anchor_service.py','anchor_cover.py','observation_policy.py','policy_safety.py','partial_star.py','frontier_service.py','replacement_frontier.py','action_audits.py','g01.py','joint_guard.py')})
    g01.save(root/'design.json',design);(root/'impl.py').write_bytes(Path(__file__).read_bytes());(root/'declaration.md').write_bytes((HERE/'budget_service.md').read_bytes())
    for name in design['dependencies']:(root/name).write_bytes((HERE/name).read_bytes())
    for case in design['cases']:
        geometry=json.loads((HERE/'op01'/f"{case['name']}_geometry.json").read_text());g01.save(root/f"{case['name']}_geometry.json",geometry)
        for label,builder in [('budget',compile_budget),('cover',ac.compile_policy)]:
            directory=root/(case['name']+'_'+label+'_policy');directory.mkdir();policy,prep=builder(case,geometry);meter=Meter();checked=safe.check(case,policy,geometry,meter)
            g01.save(directory/'preparation.json',prep);g01.save(directory/'checking.json',dict(**checked,invoice=meter.record()));g01.save(directory/'policy.json',policy)
    print('prepared bc02',flush=True)

def run(root,case,arm,directory):
    data=op.source(case);geometry=json.loads((root/f"{case['name']}_geometry.json").read_text());price,tau=case['duties'][0];meter=Meter();op.admit(case,data,geometry,meter)
    meter.pay('shared_geometry','actual_original_resolution_reuse',geometry['invoice']['total']);policy=None
    if arm in('budget','ordinary_budget','cover'):
        pd=root/(case['name']+('_cover_policy' if arm=='cover' else '_budget_policy'));policy=json.loads((pd/'policy.json').read_text());prep=json.loads((pd/'preparation.json').read_text());checked=json.loads((pd/'checking.json').read_text())
        meter.pay('preparation','actual_cover_policy_compilation',prep['invoice']['total']);meter.pay('admission','actual_cover_policy_safety_check',checked['invoice']['total'])
        meter.pay('load','policy_source_and_state_words',12+sum(8+len(k.split(',')) for k in policy['nodes']))
        if policy['source']!=data['identity'] or (policy['price'],policy['tau'])!=(price,tau):raise ValueError('Wrong policy scope')
    setup=meter.total;fee=audits=outputs=0;maximum=0;cpu=time.process_time_ns();wall=time.perf_counter_ns();directory.mkdir(exist_ok=False);g01.save(directory/'source.json',data)
    with(directory/'trace.jsonl').open('w') as trace,(directory/'diagnostics.jsonl').open('w') as diagnostics:
        trace.write(json.dumps(dict(kind='header',source=data['identity'],price=price,tau=tau,arm=arm))+'\n');trace.flush()
        for t,row in enumerate(rows(case)):
            request=f"{case['name']}-{arm}-{t}";state=[None]*len(row);receipts=[];before=meter.total;provider=op.fs.Provider(data,row,request,trace,meter)
            while True:
                if policy:
                    node=policy['nodes'][op.state_key(state)];action=node.get('action');query=node.get('query');meter.pay('selection','compiled_cover_lookup',5+len(state))
                elif arm=='anchor':
                    if state[-1] is None:action=None;query=len(state)-1
                    else:action=ac.action(case,state,meter);query=None
                    meter.pay('selection','single_anchor_rule',4)
                else:
                    action=op.terminal(case,state,price,tau,meter);query=None
                    if action is None:query=min((i for i,v in enumerate(state) if v is None),key=lambda i:(case['fees'][i],i));meter.pay('selection','cheapest_unseen_coordinate',3*len(state))
                if action is not None:action=dict(action);break
                r=provider.audit(query);receipts.append(r);state[query]=r['value']
            if action['kind']=='repair':action['model']=op.fs.model(data,[2-k for k in action['count']])
            op.check_output(case,data,geometry,receipts,request,price,tau,action,meter);paid=sum(r['fee'] for r in receipts);meter.pay('export','completed_original_action_and_invoice',22+len(case['weights']))
            trace.write(json.dumps(dict(kind='output',request=request,action=action,base_fee=paid,physical_audits=len(receipts),named_units=meter.total-before))+'\n');trace.flush()
            opt=row[-1]+sum(2*w*min(row[0],row[i]) for i,w in enumerate(case['weights'],1));cost=price if action['kind']=='replace' else row[-1]+sum(w*(k*row[i]+(2-k)*row[0]) for i,(w,k) in enumerate(zip(case['weights'],action['count']),1))
            assert cost-min(price,opt)<=action['bound']<=tau;diagnostics.write(json.dumps(dict(request=request,hidden=row,regret=cost-min(price,opt)))+'\n')
            outputs+=1;fee+=paid;audits+=len(receipts);maximum=max(maximum,paid)
    g01.save(directory/'result.json',dict(outputs=outputs,base_audit_fee=fee,physical_audits=audits,named_units=meter.total,setup_units=setup,invoice=meter.record(),observed_max_fee=maximum,declared_query_cap=len(data['supports']),cpu_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))

if __name__=='__main__':
    mode=sys.argv[1];root=Path(sys.argv[2])
    if mode=='prepare':prepare(root)
    elif mode=='run':
        design=json.loads((root/'design.json').read_text())
        if g01.sha(__file__)!=design['source_sha256']:raise ValueError('Changed implementation')
        for name,digest in design['dependencies'].items():
            if g01.sha(HERE/name)!=digest:raise ValueError('Changed dependency '+name)
        case=next(c for c in design['cases'] if c['name']==sys.argv[3]);run(root,case,sys.argv[4],Path(sys.argv[5]))
    else:raise ValueError('Unknown mode')
