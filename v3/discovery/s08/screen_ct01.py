"""Post-screen interpretation: explicitly compute ordinary pointwise pruning."""
from ast import literal_eval
from collections import Counter
from itertools import product
from pathlib import Path
import json
import sys
import paired_invoices as pi
import g01
HERE=Path(__file__).resolve().parent;ROOT=HERE/'ct01'

def run(name):
    record=next(c for c in json.loads((ROOT/'results.json').read_text())['cases'] if c['name']==name);unit=ROOT/record['unit']
    raw=json.loads((unit/'source.json').read_text());costs=raw['costs'];n=len(costs);meter=g01.kernel.Meter()
    roots={r:{literal_eval(k):v for k,v in p['roots'].items()} for r,p in raw['policies'].items()};vectors={};groups={}
    for r,policy in roots.items():
        values=[]
        for bits in product((0,1),repeat=n):
            fee,queries=pi.direct_fee(costs,policy,bits);values.append(fee);meter.pay('ordinary_pruning','complete_policy_world_execution',10*n+6*len(queries))
        vector=tuple(values);vectors[r]=vector;groups.setdefault(vector,[]).append(r)
    representatives=[g[0] for g in groups.values()];dominated={}
    for a in representatives:
        for b in representatives:
            if a==b:continue
            meter.pay('ordinary_pruning','pointwise_invoice_comparison',2**n)
            if all(x>=y for x,y in zip(vectors[a],vectors[b])) and any(x>y for x,y in zip(vectors[a],vectors[b])):
                dominated[a]=b;break
    retained=set(representatives)-set(dominated);totals=Counter();witnesses=[]
    for line in(unit/'worlds.jsonl').read_text().splitlines():
        row=json.loads(line)
        if row['logger']not in retained or row['alternative']not in retained:continue
        totals['cases']+=1;totals['target_fee']+=row['target_fee'];totals['replay_fee']+=row['replay_fee']
        totals['wins']+=row['target_fee']<row['replay_fee'];totals['losses']+=row['target_fee']>row['replay_fee'];totals['ties']+=row['target_fee']==row['replay_fee']
        if row['target_fee']<row['replay_fee'] and len(witnesses)<4:witnesses.append(row)
    result=dict(stage='DEVELOPMENT post-screen analysis',name=name,invoice_equivalence_groups=list(groups.values()),
        dominance_witnesses=dominated,retained_representatives=sorted(retained),conditional_comparison=totals,witnesses=witnesses,
        invoice=meter.record(),physical_audits=0,warning='All-world pruning is an executed exponential ordinary screen; its bill is not free and no full-cost advantage is claimed')
    g01.save(ROOT/f'{name}_pruning.json',result);print(json.dumps({k:result[k] for k in('name','retained_representatives','conditional_comparison')}))
if __name__=='__main__':run(sys.argv[1])
