"""Read-only reconstruction of paid invoice-service labels and decisions."""
from ast import literal_eval
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys
import invoice_service as service
import check_invoice_syntax as sc
import g01

HERE=Path(__file__).resolve().parent;ROOT=HERE/'is01'


def run(name):
    design=json.loads((ROOT/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==name)
    record=next(c for c in json.loads((ROOT/'results.json').read_text())['cases'] if c['name']==name)
    data=service.ib.source(case['costs']);n=len(case['costs']);rows=service.ms.draw(n,case['r'],design['requests'],case['seed']);result={}
    for arm in design['arms']:
        unit=ROOT/record['units'][arm];saved=record['arms'][arm];raw=json.loads((unit/'bank.json').read_text());assert raw['source']==data
        all_policies={r:{literal_eval(k):v for k,v in p.items()} for r,p in raw['all_policies'].items()}
        bank={r:all_policies[r] for r in raw['retained']};ranges={r:tuple(map(F,v)) for r,v in raw['ranges'].items()}
        for r,policy in all_policies.items():
            for index,bits in enumerate(product((0,1),repeat=n)):
                _,queries=service.mk.conditional_trace(bits,policy)
                assert sum(case['costs'][i] for i in queries)==raw['invoice_vectors'][r][index]
        for group in raw['groups']:assert all(raw['invoice_vectors'][r]==raw['invoice_vectors'][group[0]] for r in group)
        for a,b in raw['dominated'].items():assert all(x>=y for x,y in zip(raw['invoice_vectors'][a],raw['invoice_vectors'][b])) and any(x>y for x,y in zip(raw['invoice_vectors'][a],raw['invoice_vectors'][b]))
        nodes=sc.load_nodes(raw['nodes'])
        for r,p in raw['syntax'].items():
            tables={m:{literal_eval(k):tuple(v) for k,v in table.items()} for m,table in p['tables'].items()}
            sc.check(nodes,case['costs'],bank[r],tables,tuple(p['edge']))
        t=fees=pilots=audits=action_audits=action_fee=units=labels_checked=completion_checks=0
        counts={r:0 for r in bank};sums={r:0 for r in bank};intervals=dict(ranges);rank={r:i for i,r in enumerate(bank)};selected=Counter();receipts=[];known={};plan=None;output=None;feedback={}
        meter=service.Meter()
        with(unit/'trace.jsonl').open() as stream:
            header=json.loads(next(stream));assert header['bank_sha256']==g01.sha(unit/'bank.json') and header['source']==data['identity'] and header['arm']==arm
            for line in stream:
                item=json.loads(line);kind=item['kind']
                if kind=='plan':
                    assert not receipts and plan is None;plan=item;known={};feedback={};output=None
                    if arm=='on_policy':chosen=min(bank,key=lambda r:(intervals[r][0],counts[r],rank[r]))
                    else:chosen=min(bank,key=lambda r:(F(sums[r],counts[r]) if counts[r] else F(0),rank[r]))
                    assert item['policy']==chosen and item['calibration']==(arm!='on_policy' and t<128 and len(bank)>1)
                    selected[chosen]+=1
                elif kind=='audit':
                    receipt=item['receipt'];assert plan is not None
                    assert receipt['identity']==g01.kernel.digest({k:v for k,v in receipt.items() if k!='identity'})
                    assert receipt['source']==data['identity'] and receipt['request']==plan['request'] and receipt['sequence']==len(receipts)
                    assert receipt['node']not in known and receipt['value']==rows[t][receipt['node']] and receipt['base_fee']==case['costs'][receipt['node']]
                    known[receipt['node']]=int(receipt['value']==1);receipts.append(receipt)
                elif kind=='output':
                    assert output is None;output=item;chosen=plan['policy'];bits=[int(v==1) for v in rows[t]]
                    _,expected_queries=service.mk.conditional_trace(bits,bank[chosen]);assert expected_queries==[r['node'] for r in receipts]
                    service.base.check(data,receipts,item['action'],meter)
                    assert service.ib.aa.direct_regret(data,item['action']['assignment'],rows[t])==0
                    paid=sum(r['base_fee'] for r in receipts);assert item['base_fee']==paid and item['physical_audits']==len(receipts)
                    action_fee+=paid;action_audits+=len(receipts);feedback[chosen]=paid
                elif kind=='counterfactual_invoice':
                    assert output is not None and plan['calibration'];other=item['policy'];assert other not in feedback
                    assert {int(k):v for k,v in item['observed_indicators'].items()}==known
                    missing=[i for i in range(n) if i not in known]
                    for values in product((0,1),repeat=len(missing)):
                        world=[known.get(i,0) for i in range(n)]
                        for i,v in zip(missing,values):world[i]=v
                        fee,_=service.pi.direct_fee(case['costs'],bank[other],world)
                        assert fee==item['from_scratch_fee'];completion_checks+=1
                    feedback[other]=item['from_scratch_fee'];labels_checked+=1
                elif kind=='request_end':
                    assert output is not None and item['labels']==feedback
                    extra=sum(r['base_fee'] for r in receipts[output['physical_audits']:]);count=len(receipts)-output['physical_audits']
                    assert (item['pilot_fee'],item['pilot_audits'])==(extra,count)
                    if arm=='on_policy':assert count==0
                    if plan['calibration']:assert set(feedback)==set(bank)
                    if arm=='on_policy' or(t<128 and len(bank)>1):
                        for r,value in feedback.items():
                            counts[r]+=1;sums[r]+=value;lo,hi=ranges[r]
                            if arm=='on_policy' and hi>lo:
                                a,b=service.base.confidence(counts[r],F(sums[r]-counts[r]*lo,hi-lo),len(bank),meter)
                                intervals[r]=(max(intervals[r][0],lo+(hi-lo)*a),min(intervals[r][1],lo+(hi-lo)*b))
                    assert item['counts']==counts and item['sums']==sums
                    fees+=output['base_fee']+extra;pilots+=count;audits+=len(receipts);units+=item['named_units'];t+=1;receipts=[];plan=None
                elif kind=='final_statistical_report':
                    if arm!='on_policy' and len(bank)>1:
                        for r in bank:
                            lo,hi=ranges[r];a,b=service.base.confidence(counts[r],F(sums[r]-counts[r]*lo,hi-lo) if hi>lo else F(0),len(bank),meter)
                            intervals[r]=(lo+(hi-lo)*a,lo+(hi-lo)*b)
                    chosen=min(bank,key=lambda r:(F(sums[r],counts[r]) if counts[r] else F(0),rank[r])) if arm!='on_policy' else min(bank,key=lambda r:(intervals[r][0],counts[r],rank[r]))
                    bound=max(F(0),intervals[chosen][1]-min(lo for lo,hi in intervals.values())) if len(bank)>1 else F(0)
                    assert item['choice']==chosen and F(item['mean_fee_regret_upper'])==bound
                    assert {r:tuple(map(F,v)) for r,v in item['intervals'].items()}==intervals
                else:raise ValueError(kind)
        assert t==saved['outputs']==256 and not receipts and plan is None
        assert (fees,audits,pilots,action_audits,action_fee)==tuple(saved[k] for k in('base_audit_fee','physical_audits','pilot_audits','action_audits','action_fee'))
        assert selected==saved['selected_policies'] and counts==saved['counts'] and sums==saved['sums']
        result[arm]=dict(outputs=t,physical_receipts=audits,pilot_receipts=pilots,fee=fees,labels_checked=labels_checked,
            compatible_label_completions=completion_checks,trace_sha256=g01.sha(unit/'trace.jsonl'),physical_new_audits=0)
    g01.save(ROOT/f'{name}_reconstruction.json',dict(status='checked',arms=result,physical_new_audits=0))
    print(name,sum(v['outputs'] for v in result.values()),sum(v['compatible_label_completions'] for v in result.values()))

if __name__=='__main__':run(sys.argv[1])
