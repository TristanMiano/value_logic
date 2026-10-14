"""Read-only reconstruction of the added ordinary control after host failures."""
from ast import literal_eval
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import invoice_bandit as ib

HERE=Path(__file__).resolve().parent;ROOT=HERE/'ib01'

def run(name):
    design=json.loads((ROOT/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==name)
    saved=next(c for c in json.loads((ROOT/'results.json').read_text())['cases'] if c['name']==name)
    unit=ROOT/saved['unit'];summary=saved['ordinary_invoice'];raw=json.loads((unit/'bank.json').read_text())
    data=ib.source(case['costs']);assert raw['source']==data
    roots={int(r):{literal_eval(k):i for k,i in tree.items()} for r,tree in raw['roots'].items()}
    ranges={int(r):tuple(map(F,v)) for r,v in raw['ranges'].items()}
    for r,tree in roots.items():
        proof=raw['certificates'][str(r)]['proof'];proof['tables']={k:{m:{literal_eval(s):F(v) for s,v in table.items()} for m,table in modes.items()} for k,modes in proof['tables'].items()}
        ib.ic.check(case['costs'],tree,{},proof);assert ranges[r]==(proof['lower'],proof['upper'])
    rows=ib.ms.draw(len(case['costs']),case['r'],design['requests'],case['seed'])
    counts={r:0 for r in roots};sums={r:F(0) for r in roots};intervals=dict(ranges);fee=audits=t=0;receipts=[];meter=ib.Meter()
    with (unit/'trace.jsonl').open() as stream:
        header=json.loads(next(stream));assert header['bank_sha256']==ib.g01.sha(unit/'bank.json') and header['source']==data['identity']
        for line in stream:
            record=json.loads(line)
            if record['kind']=='plan':
                assert not receipts;plan=record;chosen=min(roots,key=lambda i:(intervals[i][0],counts[i],i))
                assert record['policy']==chosen and tuple(map(F,record['interval']))==intervals[chosen]
            elif record['kind']=='audit':
                receipt=record['receipt'];assert receipt['identity']==ib.g01.kernel.digest({k:v for k,v in receipt.items() if k!='identity'})
                assert receipt['source']==data['identity'] and receipt['request']==plan['request']
                assert receipt['sequence']==len(receipts) and receipt['node']not in {r['node'] for r in receipts}
                assert receipt['value']==rows[t][receipt['node']] and receipt['base_fee']==case['costs'][receipt['node']]
                receipts.append(receipt)
            elif record['kind']=='output':
                bits=[int(v==1) for v in rows[t]];_,queries=ib.mk.conditional_trace(bits,roots[chosen])
                assert queries==[r['node'] for r in receipts]
                ib.base.check(data,receipts,record['action'],meter)
                assert ib.aa.direct_regret(data,record['action']['assignment'],rows[t])==0
                paid=sum(r['base_fee'] for r in receipts);assert record['base_fee']==paid and record['physical_audits']==len(receipts)
                lo,hi=ranges[chosen];counts[chosen]+=1
                if hi>lo:
                    sums[chosen]+=F(paid-lo,hi-lo);a,b=ib.base.confidence(counts[chosen],sums[chosen],len(roots),meter)
                    intervals[chosen]=(max(intervals[chosen][0],lo+(hi-lo)*a),min(intervals[chosen][1],lo+(hi-lo)*b))
                assert tuple(map(F,record['interval']))==intervals[chosen] and F(record['normalized_sum'])==sums[chosen] and record['count']==counts[chosen]
                fee+=paid;audits+=len(receipts);t+=1;receipts=[]
            else:raise ValueError(record['kind'])
    assert not receipts and t==summary['outputs']==1024
    assert (fee,audits)==(summary['base_audit_fee'],summary['physical_audits'])
    assert counts=={int(k):v for k,v in summary['counts'].items()}
    result=dict(status='checked',name=name,outputs=t,physical_new_audits=0,checked_invoice_certificates=len(roots),
        trace_sha256=ib.g01.sha(unit/'trace.jsonl'),base_audit_fee=fee,physical_receipts=audits)
    ib.g01.save(ROOT/f'{name}_reconstruction.json',result);print(json.dumps(result))

if __name__=='__main__':run(sys.argv[1])
