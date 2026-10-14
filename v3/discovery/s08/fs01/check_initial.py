"""Independent read-only acquisition/controller and full cost-world checks."""
from itertools import product
from pathlib import Path
import copy
import json
import sys
import frontier_service as fs
g01=fs.g01;Meter=fs.Meter;HERE=Path(__file__).resolve().parent;ROOT=HERE/'fs01'

def run(name):
    design=json.loads((ROOT/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==name)
    record=next(c for c in json.loads((ROOT/'results.json').read_text())['cases'] if c['name']==name)
    geometry=json.loads((ROOT/f'{name}_geometry.json').read_text());n=len(case['weights']);answers={}
    for arm,unitname in record['units'].items():
        unit=ROOT/unitname;data=json.loads((unit/'source.json').read_text());fs.admit(data,geometry,Meter());saved=json.loads((unit/'result.json').read_text())
        schedule=[(price,tau,t,row) for price,tau in case['duties'] for t,row in enumerate(fs.rows(case))]
        receipts=[];known={};index=fees=audits=units=world_checks=0;last=None
        with(unit/'trace.jsonl').open() as f:
            for line in f:
                item=json.loads(line)
                if item['kind']=='header':assert item['source']==data['identity'] and item['geometry']==geometry['receipt']['identity']
                elif item['kind']=='gate':
                    price,tau,t,row=schedule[index];request=f'{name}-{price}-{tau}-{arm}-{t}';assert item['request']==request and item['price']==price and item['tau']==tau
                    reconstructed=fs.choose(data,known,price,tau,arm,Meter())
                    if arm=='full' and len(known)<n+2:reconstructed['kind']='audit'
                    assert reconstructed==item['decision'];last=item
                elif item['kind']=='audit':
                    assert last is not None and last['decision']['kind']=='audit';r=item['receipt']
                    if 0 not in known:expected=0
                    elif known[0]==1 and sum(w for j,w in enumerate(case['weights'],1) if j not in known)>tau:expected=min((j for j in range(1,n+1) if j not in known),key=lambda j:(case['fees'][j],j))
                    else:expected=min((j for j in range(n+2) if j not in known),key=lambda j:(case['fees'][j],j))
                    assert r['coordinate']==expected and r['value']==row[expected]
                    receipts.append(r);known[expected]=r['value'];last=None
                elif item['kind']=='output':
                    assert last is not None and last['decision']['kind']!='audit';decision=item['decision']
                    assert {k:v for k,v in decision.items() if k!='model'}==last['decision']
                    fs.check(data,geometry,receipts,request,price,tau,decision,Meter())
                    supports=[[known[i]] if i in known else data['supports'][i] for i in range(n+2)];worst=0
                    for world in product(*supports):
                        opt=world[-1]+sum(2*w*min(world[0],world[i]) for i,w in enumerate(case['weights'],1))
                        if decision['kind']=='replace':value=price
                        else:
                            value=sum(feature['scale']*world[feature['node']] for j,feature in enumerate(data['features']) if decision['model']>>j&1)
                        worst=max(worst,value-min(price,opt));world_checks+=1
                    assert worst==decision['bound']<=tau
                    paid=sum(r['fee'] for r in receipts);assert item['base_fee']==paid and item['physical_audits']==len(receipts)
                    fees+=paid;audits+=len(receipts);units+=item['named_units'];index+=1;receipts=[];known={};last=None
                else:raise ValueError(item['kind'])
        assert not receipts and index==saved['outputs']==len(schedule)
        assert (fees,audits,units+saved['setup_units'])==tuple(saved[k] for k in('base_audit_fee','physical_audits','named_units'))
        answers[arm]=dict(outputs=index,fee=fees,physical_receipts=audits,compatible_cost_worlds=world_checks,trace_sha256=g01.sha(unit/'trace.jsonl'))
    rejects=[]
    for label,edit in [('wrong_source',lambda r:r.update(source='wrong')),('wrong_unit',lambda r:r.update(derived=[1])),('wrong_pivot',lambda r:r.update(pivot=2))]:
        bad=copy.deepcopy(geometry);edit(bad['receipt']);bad['receipt']=g01.seal({k:v for k,v in bad['receipt'].items() if k!='identity'})
        try:fs.admit(data,bad,Meter())
        except ValueError:rejects.append(label)
        else:raise AssertionError('Invalid geometry accepted')
    g01.save(ROOT/f'{name}_reconstruction.json',dict(status='checked',arms=answers,negative_controls=rejects,physical_new_audits=0));print(name,sum(x['outputs'] for x in answers.values()),sum(x['compatible_cost_worlds'] for x in answers.values()))

if __name__=='__main__':run(sys.argv[1])
