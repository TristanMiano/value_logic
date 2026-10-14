"""Read-only original-source reconstruction of actual ac02 outputs."""
from itertools import product
from pathlib import Path
import json
import sys
import budget_service as service
op=service.op;ac=service.ac;g01=service.g01;Meter=service.Meter;ROOT=service.HERE/'bc02'

def run(name,arm):
    design=json.loads((ROOT/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==name);directory=ROOT/(name+'_'+arm);data=json.loads((directory/'source.json').read_text());geometry=json.loads((ROOT/f'{name}_geometry.json').read_text());op.admit(case,data,geometry,Meter());price,tau=case['duties'][0]
    policy=json.loads((ROOT/(name+('_cover_policy' if arm=='cover' else '_budget_policy'))/'policy.json').read_text()) if arm in('budget','ordinary_budget','cover') else None
    saved=json.loads((directory/'result.json').read_text());rows=service.rows(case);state=[None]*len(data['supports']);receipts=[];index=fee=audits=units=world_checks=0
    def expected():
        if policy:
            node=policy['nodes'][op.state_key(state)];return node.get('action'),node.get('query')
        if arm=='anchor':return (None,len(state)-1) if state[-1] is None else(ac.action(case,state,Meter()),None)
        action=op.terminal(case,state,price,tau,Meter());query=min((i for i,v in enumerate(state) if v is None),key=lambda i:(case['fees'][i],i)) if action is None else None
        return action,query
    with(directory/'trace.jsonl').open() as f:
        for line in f:
            item=json.loads(line)
            if item['kind']=='header':assert item==dict(kind='header',source=data['identity'],price=price,tau=tau,arm=arm);continue
            request=f'{name}-{arm}-{index}';action,query=expected()
            if item['kind']=='audit':
                assert action is None;r=item['receipt'];assert r['request']==request and r['coordinate']==query and r['value']==rows[index][query];receipts.append(r);state[query]=r['value']
            elif item['kind']=='output':
                assert action is not None and item['request']==request;decision=item['action'];assert {k:v for k,v in decision.items() if k!='model'}==action
                op.check_output(case,data,geometry,receipts,request,price,tau,decision,Meter());supports=[(v,) if v is not None else data['supports'][i] for i,v in enumerate(state)];coefficients=[0]*len(state)
                if decision['kind']=='repair':
                    for feature in data['features']:
                        if not any(bool(decision['model']>>(abs(l)-1)&1)==(l>0) for l in feature['clause']):coefficients[feature['node']]+=feature['scale']
                worst=0
                for world in product(*supports):
                    opt=world[-1]+sum(2*w*min(world[0],world[i]) for i,w in enumerate(case['weights'],1));value=price if decision['kind']=='replace' else sum(c*v for c,v in zip(coefficients,world));worst=max(worst,value-min(price,opt));world_checks+=1
                assert worst==decision['bound']<=tau;paid=sum(r['fee'] for r in receipts);assert item['base_fee']==paid and item['physical_audits']==len(receipts)
                fee+=paid;audits+=len(receipts);units+=item['named_units'];index+=1;receipts=[];state=[None]*len(state)
            else:raise ValueError('Unknown trace kind')
    assert index==128 and not receipts and(index,fee,audits,units+saved['setup_units'])==tuple(saved[k] for k in('outputs','base_audit_fee','physical_audits','named_units'))
    g01.save(ROOT/f'{name}_{arm}_reconstruction.json',dict(status='complete',outputs=index,base_audit_fee=fee,physical_receipts=audits,service_named_units=units,compatible_world_checks=world_checks,trace_sha256=g01.sha(directory/'trace.jsonl'),physical_new_audits=0));print(name,arm,index,world_checks,flush=True)

if __name__=='__main__':run(sys.argv[1],sys.argv[2])
