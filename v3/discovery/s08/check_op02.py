"""Read-only original output/world reconstruction for one op01 duty and arm."""
from itertools import product
from pathlib import Path
import json
import sys
import observation_policy as op
ROOT=op.HERE/'op02';Meter=op.Meter

def run(name,price,tau,arm):
    design=json.loads((ROOT/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==name)
    label=f'{name}_{price}_{tau}_{arm}';directory=ROOT/label;data=json.loads((directory/'source.json').read_text());geometry=json.loads((ROOT/f'{name}_geometry.json').read_text());op.admit(case,data,geometry,Meter())
    policy=json.loads((ROOT/f'{name}_{price}_{tau}_policy/policy.json').read_text()) if arm in('safe_policy','ordinary_safe') else None
    rows=op.rows(case);saved=json.loads((directory/'result.json').read_text());state=[None]*len(data['supports']);receipts=[];index=fee=audits=units=world_checks=0
    def expected():
        if policy:
            node=policy['nodes'][op.state_key(state)];return node.get('action'),node.get('query')
        action=op.terminal(case,state,price,tau,Meter(),narrow=arm=='narrow')
        query=min((i for i,v in enumerate(state) if v is None),key=lambda i:(case['fees'][i],i)) if action is None else None
        return action,query
    with(directory/'trace.jsonl').open() as f:
        for line in f:
            item=json.loads(line)
            if item['kind']=='header':
                assert item['source']==data['identity'] and (item['price'],item['tau'],item['arm'])==(price,tau,arm);continue
            request=f'{name}-{price}-{tau}-{arm}-{index}';row=rows[index]
            action,query=expected()
            if item['kind']=='audit':
                assert action is None;r=item['receipt'];assert r['request']==request and r['coordinate']==query and r['value']==row[query]
                receipts.append(r);state[query]=r['value']
            elif item['kind']=='output':
                assert action is not None and item['request']==request
                decision=item['action'];assert {k:v for k,v in decision.items() if k!='model'}==action
                op.check_output(case,data,geometry,receipts,request,price,tau,decision,Meter())
                supports=[(v,) if v is not None else data['supports'][i] for i,v in enumerate(state)];worst=0
                coefficients=[0]*len(state)
                if decision['kind']=='repair':
                    model=decision['model']
                    for feature in data['features']:
                        satisfied=any(bool(model>>(abs(l)-1)&1)==(l>0) for l in feature['clause'])
                        if not satisfied:coefficients[feature['node']]+=feature['scale']
                for world in product(*supports):
                    opt=world[-1]+sum(2*w*min(world[0],world[i]) for i,w in enumerate(case['weights'],1))
                    actual=price if decision['kind']=='replace' else sum(a*b for a,b in zip(coefficients,world))
                    worst=max(worst,actual-min(price,opt));world_checks+=1
                assert worst==decision['bound']<=tau
                paid=sum(r['fee'] for r in receipts);assert paid==item['base_fee'] and len(receipts)==item['physical_audits']
                if policy:assert paid<=policy['value']
                fee+=paid;audits+=len(receipts);units+=item['named_units'];index+=1;receipts=[];state=[None]*len(state)
            else:raise ValueError('Unknown trace item')
    assert index==64 and not receipts
    assert (index,fee,audits,units+saved['setup_units'])==tuple(saved[k] for k in('outputs','base_audit_fee','physical_audits','named_units'))
    record=dict(status='complete',unit=label,outputs=index,physical_receipts=audits,base_audit_fee=fee,service_named_units=units,compatible_world_checks=world_checks,trace_sha256=op.g01.sha(directory/'trace.jsonl'),physical_new_audits=0)
    op.g01.save(ROOT/f'{label}_reconstruction.json',record);print(label,index,world_checks,flush=True)

if __name__=='__main__':run(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4])

