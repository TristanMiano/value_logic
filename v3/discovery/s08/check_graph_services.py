"""Read-only reconstruction of gs01/gs02 actual graph services."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import graph_incremental as inc
ga=inc.ga;gs=inc.gs;g01=ga.g01;Meter=ga.Meter;HERE=Path(__file__).resolve().parent

def run(series,name):
    root=HERE/series;design=json.loads((root/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==name)
    record=next(c for c in json.loads((root/'results.json').read_text())['cases'] if c['name']==name);answers={}
    for arm,unitname in record['units'].items():
        unit=root/unitname;saved=json.loads((unit/'result.json').read_text());data=json.loads((unit/'source.json').read_text())
        ga.admit(data,Meter());assert data==ga.source(case['costs'],case['edges']);adj=inc.adjacency(data,Meter())
        static=json.loads((unit/('dual.json' if series=='gs01' else 'static.json')).read_text())
        receipts=[];t=fee=audits=lower_sum=units=0;ratios=[];rows=gs.rows(data['n'],case['seed'])
        with(unit/'trace.jsonl').open() as f:
            for line in f:
                item=json.loads(line)
                if item['kind']=='header':assert item['source']==data['identity'] and item['arm']==arm
                elif item['kind']=='audit':receipts.append(item['receipt'])
                elif item['kind']=='output':
                    request=f'{name}-{arm}-{t}';assert item['request']==request
                    assert all(r['value']==rows[t][r['node']] for r in receipts)
                    ga.base.construct(data,receipts,request,Meter());ga.base.check(data,receipts,item['action'],Meter())
                    plan=item.get('dual') or static;lower=ga.check_lower(data,plan,receipts,request,item['certificate'],Meter())
                    paid=sum(r['base_fee'] for r in receipts);assert item['base_fee']==paid and item['physical_audits']==len(receipts)
                    actual=[r['node'] for r in receipts];expected=[]
                    def get(i):expected.append(i);return rows[t][i]
                    if arm in('primal_dual','ordinary_dual'):ga.two_pass(data,static,get,Meter())
                    elif arm=='full':
                        for i in sorted({i for a,b,w in data['edges'] for i in(a,b)}):get(i)
                    elif arm=='greedy':
                        if series=='gs01':gs.greedy(data,get,Meter())
                        else:inc.greedy(data,adj,get,Meter())
                    else:
                        known,reconstructed=inc.adaptive_dual(data,adj,get,Meter());assert plan==reconstructed
                    assert actual==expected
                    ratio=F(paid,lower) if lower else F(1);assert F(item['checked_fee_ratio'])==ratio
                    if arm in('primal_dual','ordinary_dual','adaptive_dual','ordinary_adaptive'):assert ratio<=2
                    assert ga.aa.direct_regret(data,item['action']['assignment'],rows[t])==0
                    t+=1;fee+=paid;audits+=len(receipts);lower_sum+=lower;units+=item['named_units'];ratios.append(ratio);receipts=[]
                else:raise ValueError(item['kind'])
        assert not receipts and t==saved['outputs']==32
        assert (fee,audits,lower_sum)==tuple(saved[k] for k in('base_audit_fee','physical_audits','lower_bound_sum'))
        assert units+saved['setup_units']==saved['named_units']
        assert F(saved['aggregate_checked_ratio'])==F(fee,lower_sum) and F(saved['max_checked_ratio'])==max(ratios)
        answers[arm]=dict(outputs=t,physical_receipts=audits,fee=fee,lower_sum=lower_sum,trace_sha256=g01.sha(unit/'trace.jsonl'))
    g01.save(root/f'{name}_reconstruction.json',dict(status='checked',arms=answers,physical_new_audits=0));print(series,name,sum(x['outputs'] for x in answers.values()))

if __name__=='__main__':run(sys.argv[1],sys.argv[2])
