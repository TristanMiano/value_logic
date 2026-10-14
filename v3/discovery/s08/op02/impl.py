"""Source-bound sufficient query DAGs; Codex (GPT-6), DEVELOPMENT."""
from pathlib import Path
import copy
import json
import sys
import time
import observation_policy as op
g01=op.g01;Meter=op.Meter;HERE=Path(__file__).resolve().parent

def extract(case,original,meter):
    data=op.source(case);nodes={};n=len(data['supports'])
    if original['source']!=data['identity']:raise ValueError('Changed original policy source')
    meter.pay('policy_extraction','read_actual_unpruned_policy_words',12+sum(8+len(key.split(',')) for key in original['nodes']))
    def visit(key):
        if key in nodes:return
        state=op.state_from(key);node=original['nodes'][key];nodes[key]=copy.deepcopy(node)
        meter.pay('policy_extraction','retain_reachable_selected_node',10+n)
        if 'query' in node:
            i=node['query']
            for value in data['supports'][i]:
                child=list(state);child[i]=value;visit(op.state_key(child))
    visit(original['root'])
    return dict(source=data['identity'],price=original['price'],tau=original['tau'],root=original['root'],value=original['value'],nodes=nodes)

def check(case,policy,geometry,meter):
    data=op.source(case);op.admit(case,data,geometry,meter);n=len(data['supports']);seen={};price,tau=policy['price'],policy['tau']
    if policy['source']!=data['identity'] or policy['root']!=op.state_key((None,)*n) or type(price)is not int or price<0 or type(tau)is not int or tau<0:raise ValueError('Wrong policy scope')
    def visit(state):
        key=op.state_key(state)
        if key in seen:return seen[key]
        if key not in policy['nodes']:raise ValueError('Missing admitted response branch')
        node=policy['nodes'][key];meter.pay('policy_check','source_state_node_lookup',8+n)
        if 'action' in node:
            if 'query' in node:raise ValueError('Ambiguous node')
            action=node['action'];known={i:v for i,v in enumerate(state[:-1]) if v is not None};a=state[-1];loA,hiA=(0,case['A']) if a is None else(a,a)
            if action['kind']=='replace':
                R,U,L=op.ps.endpoint_metrics(case['weights'],case['H'],known,[1]*len(case['weights']),meter);bound=max(0,price-L-loA)
            elif action['kind']=='repair':
                count=action['count'];model=op.fs.model(data,[2-k for k in count])
                R,U,L=op.ps.endpoint_metrics(case['weights'],case['H'],known,count,meter);bound=max(R,U+hiA-price)
                for clause in data['hard']:
                    if not any(bool(model>>(abs(l)-1)&1)==(l>0) for l in clause):raise ValueError('Original terminal action infeasible')
                    meter.pay('policy_check','terminal_original_clause',1+len(clause))
            else:raise ValueError('Unknown action')
            if node['value']!=0 or bound!=action['bound'] or bound>tau:raise ValueError('Wrong terminal warranty')
            result=0
        else:
            i=node['query']
            if type(i)is not int or not 0<=i<n or state[i] is not None:raise ValueError('Repeated or invalid query')
            children=[]
            for value in data['supports'][i]:
                child=list(state);child[i]=value;children.append(visit(tuple(child)))
                meter.pay('policy_check','every_actual_response_branch',5+n)
            result=case['fees'][i]+max(children)
            if result!=node['value']:raise ValueError('Incorrect upper fee recurrence')
        seen[key]=result;return result
    value=visit((None,)*n)
    if value!=policy['value'] or set(seen)!=set(policy['nodes']):raise ValueError('Wrong root bound or unreachable surplus nodes')
    return dict(status='complete',reachable_states=len(seen),worst_fee=value,contract='safe complete action and upper fee only; no optimality premise')

def prepare(root):
    root.mkdir(exist_ok=False);old=HERE/'op01';design=json.loads((old/'design.json').read_text());design['arms']=['safe_policy','ordinary_safe'];design['parent_design_sha256']=g01.sha(old/'design.json');design['source_sha256']=g01.sha(__file__)
    design['dependencies']={name:g01.sha(HERE/name) for name in ('observation_policy.py','partial_star.py','frontier_service.py','replacement_frontier.py','action_audits.py','g01.py','joint_guard.py')}
    g01.save(root/'design.json',design);(root/'impl.py').write_bytes(Path(__file__).read_bytes());(root/'declaration.md').write_bytes((HERE/'policy_admission.md').read_bytes())
    for case in design['cases']:
        geometry=json.loads((old/f"{case['name']}_geometry.json").read_text());g01.save(root/f"{case['name']}_geometry.json",geometry)
        for price,tau in case['duties']:
            label=f"{case['name']}_{price}_{tau}_policy";source=old/label;directory=root/label;directory.mkdir()
            original=json.loads((source/'policy.json').read_text());meter=Meter();policy=extract(case,original,meter);extraction=meter.record();meter=Meter();checked=check(case,policy,geometry,meter);checking=meter.record();negatives=[]
            for label in ('source','fee','terminal','branch'):
                bad=copy.deepcopy(policy)
                if label=='source':bad['source']='wrong'
                elif label=='fee':bad['value']+=1
                elif label=='terminal':
                    node=next(v for v in bad['nodes'].values() if 'action' in v);node['action']['bound']-=1
                else:
                    nonterminal=next(((k,v) for k,v in bad['nodes'].items() if 'query' in v),None)
                    if nonterminal is None:continue
                    key,node=nonterminal;child=list(op.state_from(key));child[node['query']]=op.source(case)['supports'][node['query']][0];del bad['nodes'][op.state_key(child)]
                try:check(case,bad,geometry,Meter())
                except ValueError:negatives.append(label)
                else:raise AssertionError('Changed certificate accepted')
            (directory/'policy.json').write_text(json.dumps(policy,separators=(',',':'))+'\n')
            original_build=json.loads((source/'planning.json').read_text())
            g01.save(directory/'preparation.json',dict(parent_policy_sha256=g01.sha(source/'policy.json'),parent_build_sha256=g01.sha(source/'planning.json'),original_build_units=original_build['invoice']['total'],extraction_invoice=extraction,safety_invoice=checking,checked=checked,negative_controls=negatives))
    print('prepared',sum(len(c['duties']) for c in design['cases']),flush=True)

def run(root,case,price,tau,arm,directory):
    data=op.source(case);geometry=json.loads((root/f"{case['name']}_geometry.json").read_text());meter=Meter();op.admit(case,data,geometry,meter)
    policy_dir=root/f"{case['name']}_{price}_{tau}_policy";policy=json.loads((policy_dir/'policy.json').read_text());prep=json.loads((policy_dir/'preparation.json').read_text())
    meter.pay('shared_acquisition','allocated_original_resolution',geometry['invoice']['total'])
    meter.pay('shared_planning','actual_original_build_including_discarded_states',prep['original_build_units'])
    meter.pay('shared_extraction','actual_reachable_extraction',prep['extraction_invoice']['total'])
    meter.pay('shared_admission','actual_safe_policy_check',prep['safety_invoice']['total'])
    meter.pay('policy_load','compact_policy_words',10+sum(6+len(k.split(',')) for k in policy['nodes']))
    if policy['source']!=data['identity'] or (policy['price'],policy['tau'])!=(price,tau):raise ValueError('Wrong service source/duty')
    setup=meter.total;fee=audits=outputs=0;maximum=0;cpu=time.process_time_ns();wall=time.perf_counter_ns();directory.mkdir(exist_ok=False);g01.save(directory/'source.json',data)
    with(directory/'trace.jsonl').open('w') as trace,(directory/'diagnostics.jsonl').open('w') as diagnostics:
        trace.write(json.dumps(dict(kind='header',source=data['identity'],price=price,tau=tau,arm=arm))+'\n');trace.flush()
        for t,row in enumerate(op.rows(case)):
            request=f"{case['name']}-{price}-{tau}-{arm}-{t}";state=[None]*len(row);receipts=[];before=meter.total;provider=op.fs.Provider(data,row,request,trace,meter)
            while True:
                node=policy['nodes'][op.state_key(state)];meter.pay('selection','policy_state_lookup',5+len(state))
                if 'action' in node:action=dict(node['action']);break
                i=node['query'];r=provider.audit(i);receipts.append(r);state[i]=r['value']
            if action['kind']=='repair':action['model']=op.fs.model(data,[2-k for k in action['count']])
            op.check_output(case,data,geometry,receipts,request,price,tau,action,meter);paid=sum(r['fee'] for r in receipts)
            meter.pay('export','source_action_receipts_and_bill',22+len(case['weights']))
            trace.write(json.dumps(dict(kind='output',request=request,action=action,physical_audits=len(receipts),base_fee=paid,named_units=meter.total-before))+'\n');trace.flush()
            opt=row[-1]+sum(2*w*min(row[0],row[i]) for i,w in enumerate(case['weights'],1));cost=price if action['kind']=='replace' else row[-1]+sum(w*(k*row[i]+(2-k)*row[0]) for i,(w,k) in enumerate(zip(case['weights'],action['count']),1))
            assert cost-min(price,opt)<=action['bound']<=tau and paid<=policy['value']
            diagnostics.write(json.dumps(dict(request=request,hidden=row,regret=cost-min(price,opt)))+'\n');fee+=paid;audits+=len(receipts);outputs+=1;maximum=max(maximum,paid)
    g01.save(directory/'result.json',dict(outputs=outputs,base_audit_fee=fee,physical_audits=audits,named_units=meter.total,setup_units=setup,invoice=meter.record(),observed_max_fee=maximum,policy_worst_fee=policy['value'],complete_query_cap=len(data['supports']),cpu_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))

if __name__=='__main__':
    mode=sys.argv[1];root=Path(sys.argv[2])
    if mode=='prepare':prepare(root)
    elif mode=='run':
        design=json.loads((root/'design.json').read_text())
        if g01.sha(__file__)!=design['source_sha256']:raise ValueError('Changed source')
        for name,digest in design['dependencies'].items():
            if g01.sha(HERE/name)!=digest:raise ValueError('Changed dependency '+name)
        case=next(c for c in design['cases'] if c['name']==sys.argv[3]);run(root,case,int(sys.argv[4]),int(sys.argv[5]),sys.argv[6],Path(sys.argv[7]))
    else:raise ValueError('Unknown operation')
