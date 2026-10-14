"""Resume last five ic01 units after stochastic KeyError; no new audits."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import copy
import json
import random
import sys
import g01
import invoice_completion as ic

HERE=Path(__file__).resolve().parent
ROOT=HERE/'ic01'
assert g01.sha(HERE/'invoice_completion.py')==g01.sha(ROOT/'impl.py')
rng=random.Random(8141480)
for n in range(2,8):
    for repeat in range(2):costs=[rng.randrange(1,10) for _ in range(n)]

if len(sys.argv)>1:
    r=int(sys.argv[1]);roots=ic.mk.plan(costs,r)['roots'];worlds=[];collapse=states=completions=0
    for bits in product((0,1),repeat=7):
        observed,queries=ic.mk.conditional_trace(bits,roots);fee=sum(costs[i] for i in queries);worlds.append((bits,fee))
        cert=ic.produce(costs,roots,{i:v for i,v in enumerate(observed) if v>=0})
        assert cert['lower']==cert['upper']==fee;collapse+=1
    for partial in product((-1,0,1),repeat=7):
        observed={i:v for i,v in enumerate(partial) if v>=0};cert=ic.produce(costs,roots,observed);ic.check(costs,roots,observed,cert)
        fees=[fee for bits,fee in worlds if all(bits[i]==v for i,v in observed.items())]
        assert (cert['lower'],cert['upper'])==(min(fees),max(fees));states+=1;completions+=len(fees)
    g01.save(ROOT/f'last_r{r}.json',dict(n=7,costs=costs,r=r,partial_states=states,completion_comparisons=completions,on_policy_collapses=collapse))
    print('checked r',r)
else:
    progress=json.loads((ROOT/'progress.json').read_text());cases=progress['cases']
    assert len(cases)==55
    cases +=[json.loads((ROOT/f'last_r{r}.json').read_text()) for r in ic.mk.MENU]
    costs=[2,7,2];roots=ic.mk.plan(costs,5)['roots'];interval=[F(0),F(0)]
    for bits in product((0,1),repeat=3):
        observed=dict(ic.aq.trace(bits,'center'));cert=ic.produce(costs,roots,observed)
        interval[0]+=F(cert['lower'],8);interval[1]+=F(cert['upper'],8)
    assert interval==[F(53,8),F(81,8)]
    negative=[];cert=ic.produce(costs,roots,{1:0})
    for label,changed in [('lower',copy.deepcopy(cert)),('witness',copy.deepcopy(cert)),('binding',copy.deepcopy(cert))]:
        if label=='lower':changed['tables']['lower']['ordinary'][0,2]+=1
        if label=='witness':changed['witnesses']['upper'][1]=1
        if label=='binding':changed['binding']='wrong'
        rejected=False
        try:ic.check(costs,roots,{1:0},changed)
        except ValueError:rejected=True
        assert rejected;negative.append(dict(kind=label,rejected=True))
    counts=[0,0];sums=[F(0),F(0)]
    for t in range(10000):
        i=min(range(2),key=lambda j:(sums[j],j));counts[i]+=1;sums[i]+=[F(3,4),F(1)][i]
    assert abs(F(counts[1],10000)-F(3,7))<F(1,10000)
    result=dict(status='complete_after_preserved_stochastic_failure',cases=cases,partial_states=sum(c['partial_states'] for c in cases),
        completion_comparisons=sum(4**c['n'] for c in cases),on_policy_collapses=sum(2**c['n'] for c in cases),
        sharp_countermodel_mean_interval=interval,negative_controls=negative,naive_partial_pooling_counts=counts,
        naive_partial_pooling_regret=F(counts[1],4),physical_audits=0,failed_prefix_cost='unknown; original ic01_output.txt retained')
    g01.save(ROOT/'results.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('cases','negative_controls')},default=g01.encode))
