"""Paid finite-source observation policies. Codex (GPT-6), DEVELOPMENT."""
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import random
import sys
import time
import frontier_service as fs
import partial_star as ps
g01=ps.g01;Meter=ps.Meter;HERE=Path(__file__).resolve().parent

def source(case):
    data=fs.source(case['weights'],case['fees'],case['A']);data.pop('identity')
    data['supports']=[case['alphabet']]*(len(case['weights'])+1)+[[0,case['A']]]
    data['H']=case['H'];data['bit_source']='declared independent finite Cartesian support; common mandatory anchor'
    return g01.seal(data)

def admit(case,data,geometry,meter):
    if data!=source(case):raise ValueError('Changed original source')
    receipt=geometry['receipt'];n=data['variables'];left,right=receipt['parents'];pivot=receipt['pivot']
    if receipt['identity']!=g01.kernel.digest({k:v for k,v in receipt.items() if k!='identity'}) or receipt['source']!=data['identity']:raise ValueError('Wrong geometry scope')
    a,b=data['hard'][left],data['hard'][right]
    if pivot not in a or -pivot not in b or sorted(set(a)-{pivot}|set(b)-{-pivot})!=[n] or receipt['derived']!=[n] or receipt['mandatory_variable']!=n:raise ValueError('Bad mandatory resolution')
    meter.pay('source','original_clauses_features_support_and_fee_admission',24+sum(1+len(c) for c in data['hard'])+5*len(data['features'])+sum(map(len,data['supports'])))
    meter.pay('geometry','exact_original_resolution_check',24+len(a)+len(b))

def state_key(state):return ','.join('_' if v is None else str(v) for v in state)
def state_from(key):return tuple(None if v=='_' else int(v) for v in key.split(','))

def narrow_counts(case,known):
    zvalues=[known[0]] if 0 in known else case['alphabet'];menu={(1,)*len(case['weights'])};median=case['alphabet'][1]
    for z in zvalues:
        options=[]
        for i in range(1,len(case['weights'])+1):
            y=known.get(i,median);options.append((0,) if y>z else (2,) if y<z else(0,1,2))
        menu.update(product(*options))
    return sorted(menu)

def terminal(case,state,price,tau,meter,narrow=False):
    n=len(case['weights']);known={i:v for i,v in enumerate(state[:n+1]) if v is not None};anchor=state[-1]
    loA,hiA=(0,case['A']) if anchor is None else(anchor,anchor)
    _,_,L=ps.endpoint_metrics(case['weights'],case['H'],known,[1]*n,meter);replace=max(0,price-L-loA)
    if replace<=tau:return dict(kind='replace',bound=replace,count=None)
    if narrow:
        options=[]
        for count in narrow_counts(case,known):
            R,U,L=ps.endpoint_metrics(case['weights'],case['H'],known,count,meter)
            if R<=tau:options.append((U,count,R))
            meter.pay('planning','narrow_witness_menu_and_comparison',6+n)
        if not options:return None
        U,count,R=min(options)
    else:
        proposal=ps.propose(case['weights'],case['H'],known,tau,meter)
        if proposal['status']=='UNRESOLVED':raise RuntimeError('Declared exact small policy exceeded its state cap')
        if proposal['status']=='INFEASIBLE':return None
        R,U,count=proposal['R'],proposal['U'],proposal['count']
    bound=max(R,U+hiA-price)
    return dict(kind='repair',bound=bound,count=list(count)) if bound<=tau else None

def independent_risk(case,state,count):
    """Direct corner evaluation, used only by the planning certificate checker."""
    n=len(case['weights']);options=[(v,) if v is not None else(0,case['H']) for v in state[:n+1]]
    regrets=[];costs=[];opts=[]
    for row in product(*options):
        r,u,l=ps.world_metrics(case['weights'],row,count);regrets.append(r);costs.append(u);opts.append(l)
    a=state[-1];lowA,highA=(0,case['A']) if a is None else(a,a)
    return max(regrets),max(costs)+highA,min(opts)+lowA

def build(case,price,tau,directory,geometry):
    data=source(case);meter=Meter();admit(case,data,geometry,meter);nodes={};n=len(data['supports'])
    @lru_cache(None)
    def visit(state):
        action=terminal(case,state,price,tau,meter)
        if action is not None:
            nodes[state_key(state)]=dict(value=0,action=action);return 0
        values=[]
        for i,v in enumerate(state):
            if v is not None:continue
            children=[]
            for response in data['supports'][i]:
                next_state=list(state);next_state[i]=response;children.append(visit(tuple(next_state)))
                meter.pay('planning','minimax_child_dispatch_and_comparison',5+n)
            values.append((case['fees'][i]+max(children),i))
        if not values:raise AssertionError('Fully known duty unresolved')
        value,query=min(values);nodes[state_key(state)]=dict(value=value,query=query)
        meter.pay('planning','minimax_query_selection_and_retention',6+len(values)+n);return value
    root=(None,)*n;V=visit(root)
    certificate=dict(source=data['identity'],price=price,tau=tau,nodes=nodes,root=state_key(root),value=V)
    directory.mkdir(exist_ok=False);(directory/'policy.json').write_text(json.dumps(certificate,separators=(',',':'))+'\n')
    g01.save(directory/'planning.json',dict(invoice=meter.record(),states=len(nodes),value=V))
    return certificate

def check_policy(case,certificate,geometry):
    data=source(case);meter=Meter();admit(case,data,geometry,meter)
    if certificate['source']!=data['identity']:raise ValueError('Changed policy source')
    price,tau=certificate['price'],certificate['tau'];nodes=certificate['nodes'];checked={};action_checks=world_checks=0
    for key in sorted(nodes,key=lambda s:s.count('_')):
        state=state_from(key)
        if len(state)!=len(data['supports']) or any(v is not None and v not in data['supports'][i] for i,v in enumerate(state)):raise ValueError('Bad policy state')
        node=nodes[key];count=[1]*len(case['weights']);_,_,lower=independent_risk(case,state,count)
        replacement=max(0,price-lower)
        if 'action' in node:
            action=node['action']
            if action['kind']=='replace':bound=replacement
            else:
                R,U,L=independent_risk(case,state,action['count']);bound=max(R,U-price)
            if bound!=action['bound'] or bound>tau or node['value']!=0:raise ValueError('Wrong terminal action')
            meter.pay('policy_check','terminal_corner_bound',40*(2**state[:-1].count(None))*len(case['weights']));action_checks+=1
            checked[key]=0;continue
        # Exact lower premise: no feasible source action may have been omitted.
        if replacement<=tau:raise ValueError('Replacement available at nonterminal')
        for count in product((0,1,2),repeat=len(case['weights'])):
            R,U,L=independent_risk(case,state,count)
            if max(R,U-price)<=tau:raise ValueError('A repair was omitted at nonterminal')
            count_worlds=2**state[:-1].count(None);world_checks+=count_worlds;action_checks+=1
            meter.pay('policy_check','all_action_corner_nonterminal_lower',40*count_worlds*len(case['weights']))
        values=[]
        for i,v in enumerate(state):
            if v is not None:continue
            children=[]
            for response in data['supports'][i]:
                child=list(state);child[i]=response;children.append(checked[state_key(child)])
                meter.pay('policy_check','source_response_branch_and_child_value',6+len(state))
            values.append((case['fees'][i]+max(children),i))
        expected=min(values)
        if (node['value'],node['query'])!=expected:raise ValueError('Wrong minimax recurrence')
        checked[key]=expected[0]
    if certificate['root']!=state_key((None,)*len(data['supports'])) or checked[certificate['root']]!=certificate['value']:raise ValueError('Wrong root')
    return dict(status='complete',states=len(checked),action_checks=action_checks,corner_checks=world_checks,invoice=meter.record())

def check_output(case,data,geometry,receipts,request,price,tau,action,meter):
    state=[None]*len(data['supports'])
    for r in receipts:
        i=r['coordinate']
        if (r['identity']!=g01.kernel.digest({k:v for k,v in r.items() if k!='identity'}) or r['source']!=data['identity'] or r['request']!=request
            or type(i)is not int or not 0<=i<len(state) or state[i] is not None or r['sequence']!=sum(v is not None for v in state)
            or r['value'] not in data['supports'][i] or r['fee']!=case['fees'][i]):raise ValueError('Wrong receipt scope/content')
        state[i]=r['value'];meter.pay('receipt_check','bound_source_request_fee_sequence',20)
    known={i:v for i,v in enumerate(state[:-1]) if v is not None};n=len(case['weights']);a=state[-1];loA,hiA=(0,case['A']) if a is None else(a,a)
    if action['kind']=='replace':
        R,U,L=ps.endpoint_metrics(case['weights'],case['H'],known,[1]*n,meter);bound=max(0,price-L-loA)
    else:
        model=action['model']
        for clause in data['hard']:
            if not any(bool(model>>(abs(l)-1)&1)==(l>0) for l in clause):raise ValueError('Original action infeasible')
            meter.pay('action_check','original_clause',1+len(clause))
        count=[int(bool(model>>(4*i+1)&1))+int(bool(model>>(4*i+3)&1)) for i in range(n)]
        if count!=action['count']:raise ValueError('Wrong original action count')
        R,U,L=ps.endpoint_metrics(case['weights'],case['H'],known,count,meter);bound=max(R,U+hiA-price)
    if action['bound']!=bound or bound>tau:raise ValueError('Unwarranted output')
    return state

def rows(case):
    rng=random.Random(case['seed']);return [[rng.choice(case['alphabet']) for _ in range(len(case['weights'])+1)]+[rng.choice((0,case['A']))] for t in range(64)]

def run(case,price,tau,arm,directory,root):
    data=source(case);geometry=json.loads((root/f"{case['name']}_geometry.json").read_text());meter=Meter();admit(case,data,geometry,meter)
    meter.pay('shared_acquisition','allocated_original_resolution',geometry['invoice']['total']);policy=None
    if arm in('minimax','ordinary_minimax'):
        pd=root/f"{case['name']}_{price}_{tau}_policy";policy=json.loads((pd/'policy.json').read_text())
        planning=json.loads((pd/'planning.json').read_text());checking=json.loads((pd/'checking.json').read_text())
        if checking['status']!='complete':raise ValueError('Policy unchecked')
        meter.pay('shared_planning','allocated_actual_policy_build',planning['invoice']['total'])
        meter.pay('shared_checking','allocated_actual_policy_reconstruction',checking['invoice']['total'])
        meter.pay('policy_load','source_bound_policy_words',10+sum(6+len(k.split(',')) for k in policy['nodes']))
        if policy['source']!=data['identity'] or (policy['price'],policy['tau'])!=(price,tau):raise ValueError('Wrong policy duty')
    setup=meter.total;outputs=fee=audits=0;maximum=0;cpu=time.process_time_ns();wall=time.perf_counter_ns()
    directory.mkdir(exist_ok=False);g01.save(directory/'source.json',data)
    with(directory/'trace.jsonl').open('w') as trace,(directory/'diagnostics.jsonl').open('w') as diagnostics:
        trace.write(json.dumps(dict(kind='header',source=data['identity'],price=price,tau=tau,arm=arm))+'\n');trace.flush()
        for t,row in enumerate(rows(case)):
            request=f"{case['name']}-{price}-{tau}-{arm}-{t}";state=[None]*len(row);receipts=[];before=meter.total;provider=fs.Provider(data,row,request,trace,meter)
            while True:
                if policy:
                    node=policy['nodes'][state_key(state)];action=node.get('action');query=node.get('query');meter.pay('selection','policy_state_lookup',5+len(state))
                else:
                    action=terminal(case,state,price,tau,meter,narrow=arm=='narrow');query=None
                    if action is None:query=min((i for i,v in enumerate(state) if v is None),key=lambda i:(case['fees'][i],i));meter.pay('selection','cheapest_unseen_query',3*len(state))
                if action is not None:action=dict(action);break
                r=provider.audit(query);receipts.append(r);state[query]=r['value']
            if action['kind']=='repair':action['model']=fs.model(data,[2-k for k in action['count']])
            check_output(case,data,geometry,receipts,request,price,tau,action,meter);paid=sum(r['fee'] for r in receipts)
            meter.pay('export','source_action_receipts_and_bill',22+len(case['weights']))
            trace.write(json.dumps(dict(kind='output',request=request,action=action,physical_audits=len(receipts),base_fee=paid,named_units=meter.total-before))+'\n');trace.flush()
            opt=row[-1]+sum(2*w*min(row[0],row[i]) for i,w in enumerate(case['weights'],1))
            cost=price if action['kind']=='replace' else row[-1]+sum(w*(k*row[i]+(2-k)*row[0]) for i,(w,k) in enumerate(zip(case['weights'],action['count']),1))
            assert cost-min(price,opt)<=action['bound']<=tau
            diagnostics.write(json.dumps(dict(request=request,hidden=row,regret=cost-min(price,opt)))+'\n')
            outputs+=1;fee+=paid;audits+=len(receipts);maximum=max(maximum,paid)
    g01.save(directory/'result.json',dict(outputs=outputs,base_audit_fee=fee,physical_audits=audits,named_units=meter.total,setup_units=setup,invoice=meter.record(),observed_max_fee=maximum,policy_worst_fee=policy['value'] if policy else None,complete_query_cap=len(data['supports']),cpu_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))

if __name__=='__main__':
    mode=sys.argv[1];root=Path(sys.argv[2]);design=json.loads((root/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==sys.argv[3]);price,tau=map(int,sys.argv[4:6]);geometry=json.loads((root/f"{case['name']}_geometry.json").read_text())
    if g01.sha(__file__)!=design['source_sha256']:raise ValueError('Changed service implementation')
    for name,digest in design['dependencies'].items():
        if g01.sha(HERE/name)!=digest:raise ValueError('Changed dependency '+name)
    pd=root/f"{case['name']}_{price}_{tau}_policy"
    if mode=='build':build(case,price,tau,pd,geometry)
    elif mode=='check':
        checked=check_policy(case,json.loads((pd/'policy.json').read_text()),geometry);g01.save(pd/'checking.json',checked);print(checked['states'],checked['action_checks'],flush=True)
    elif mode=='run':run(case,price,tau,sys.argv[6],Path(sys.argv[7]),root)
    else:raise ValueError('Unknown operation')
