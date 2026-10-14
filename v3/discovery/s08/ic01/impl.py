"""Exact extrema of a supplied policy's from-scratch invoice under receipts.
DEVELOPMENT, Codex (GPT-6), 2026-10-14.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import copy
import json
import random
import sys
import g01
import markov_paths as mk
import continuum_policy as cp
import adequacy_countermodel as aq

HERE=Path(__file__).resolve().parent
VERSION='s08-invoice-completion-v1'
Meter=g01.kernel.Meter


def binding(costs,roots,observed):return g01.kernel.digest(cp.normalize(dict(costs=costs,roots=roots,observed=observed)))


def validate(costs,roots,observed):
    n=len(costs)
    if not n or any(type(c)not in(int,F) or c<=0 for c in costs):raise ValueError('Positive finite fees')
    if set(roots)!={(a,b) for a in range(n) for b in range(a+1,n)}:raise ValueError('Root scope')
    if any(type(i)is not int or not a<=i<=b for (a,b),i in roots.items()):raise ValueError('Root range')
    if any(type(i)is not int or not 0<=i<n or type(v)is not int or v not in(0,1) for i,v in observed.items()):raise ValueError('Receipt indicator scope')


def branches(mode,a,b,roots):
    i=a if mode=='left' else b if mode=='right' else roots[a,b]
    if mode=='left':return i,[('ordinary',a+1,b)],[('left',a+1,b)]
    if mode=='right':return i,[('ordinary',a,b-1)],[('right',a,b-1)]
    return i,[('ordinary',a,i-1),('ordinary',i+1,b)],[('right',a,i-1),('left',i+1,b)]


def produce(costs,roots,observed):
    validate(costs,roots,observed);n=len(costs);meter=Meter();tables={key:{mode:{} for mode in ('ordinary','left','right')} for key in ('lower','upper')};choices=copy.deepcopy(tables)
    for length in range(1,n+1):
        for a in range(n-length+1):
            b=a+length-1
            for mode in ('ordinary','left','right'):
                if mode=='ordinary' and a==b:
                    for kind in tables:tables[kind][mode][a,b]=0;choices[kind][mode][a,b]=None
                    continue
                i,extreme,middle=branches(mode,a,b,roots)
                allowed=[observed[i]] if i in observed else [0,1]
                for kind in tables:
                    options=[]
                    for value in allowed:
                        cost=costs[i]+sum(tables[kind][m][l,h] for m,l,h in (middle if value else extreme) if l<=h)
                        options.append((cost,value));meter.pay('completion','candidate_branch_fee',1+2*len(middle if value else extreme))
                    selected=min(options) if kind=='lower' else max(options)
                    tables[kind][mode][a,b],choices[kind][mode][a,b]=selected
                    meter.pay('completion','extremum_selection_and_retention',len(options)+2)
    witnesses={}
    for kind in tables:
        world=dict(observed);tasks=[('ordinary',0,n-1)]
        while tasks:
            mode,a,b=tasks.pop()
            if a>b or (mode=='ordinary' and a==b):continue
            i,e,m=branches(mode,a,b,roots);value=choices[kind][mode][a,b]
            if i in world:assert world[i]==value
            world[i]=value;tasks.extend(m if value else e);meter.pay('completion','attaining_world_reconstruction',5)
        witnesses[kind]=[world.get(i,0) for i in range(n)]
    return dict(binding=binding(costs,roots,observed),tables=tables,witnesses=witnesses,
        lower=tables['lower']['ordinary'][0,n-1],upper=tables['upper']['ordinary'][0,n-1],invoice=meter.record())


def check(costs,roots,observed,cert):
    validate(costs,roots,observed);n=len(costs);meter=Meter();states={(a,b) for a in range(n) for b in range(a,n)}
    if cert['binding']!=binding(costs,roots,observed) or set(cert['tables'])!={'lower','upper'}:raise ValueError('Completion source binding')
    for kind,tables in cert['tables'].items():
        if set(tables)!={'ordinary','left','right'}:raise ValueError('Completion mode scope')
        if any(set(table)!=states or any(type(v)not in(int,F) or v<0 for v in table.values()) for table in tables.values()):raise ValueError('Completion state scope')
        def get(mode,a,b):return tables[mode][a,b] if a<=b else 0
        for a,b in states:
            for mode in tables:
                if a==b and mode=='ordinary':expected=0
                else:
                    i=a if mode=='left' else b if mode=='right' else roots[a,b]
                    if mode=='left':ev=get('ordinary',a+1,b);mv=get('left',a+1,b)
                    elif mode=='right':ev=get('ordinary',a,b-1);mv=get('right',a,b-1)
                    else:ev=get('ordinary',a,i-1)+get('ordinary',i+1,b);mv=get('right',a,i-1)+get('left',i+1,b)
                    if i in observed:expected=costs[i]+(mv if observed[i] else ev)
                    else:expected=costs[i]+(min(ev,mv) if kind=='lower' else max(ev,mv))
                if tables[mode][a,b]!=expected:raise ValueError('Invalid completion extremum')
                meter.pay('completion_check','independent_extremum_recurrence',12)
        world=cert['witnesses'][kind]
        if len(world)!=n or any(v not in(0,1) for v in world) or any(world[i]!=v for i,v in observed.items()):raise ValueError('Invalid completion witness')
        _,queries=mk.conditional_trace(world,roots);fee=sum(costs[i] for i in queries)
        if fee!=cert[kind] or fee!=tables['ordinary'][0,n-1]:raise ValueError('Unattained completion bound')
        meter.pay('completion_check','execute_attaining_policy_world',n+len(queries)*5)
    if cert['lower']>cert['upper']:raise ValueError('Reversed completion bounds')
    return meter.record()


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    rng=random.Random(8141480);cases=[];completions=states=collapse=0
    g01.save(directory/'design.json',dict(version=VERSION,stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        seed=8141480,sizes=list(range(2,8)),repeats=2,policy_menu=list(mk.MENU),source_sha256=g01.sha(__file__),
        declaration_sha256=g01.sha(HERE/'invoice_completion.md'),physical_audits=0))
    for n in range(2,8):
        for repeat in range(2):
            costs=[rng.randrange(1,10) for _ in range(n)]
            for r in mk.MENU:
                roots=mk.plan(costs,r)['roots'];worlds=[];local_states=0
                for bits in product((0,1),repeat=n):
                    observed,queries=mk.conditional_trace(bits,roots);fee=sum(costs[i] for i in queries)
                    worlds.append((bits,fee));known={i:v for i,v in enumerate(observed) if v>=0}
                    cert=produce(costs,roots,known);assert cert['lower']==cert['upper']==fee;collapse+=1
                for partial in product((-1,0,1),repeat=n):
                    observed={i:v for i,v in enumerate(partial) if v>=0};cert=produce(costs,roots,observed);check(costs,roots,observed,cert)
                    fees=[fee for bits,fee in worlds if all(bits[i]==v for i,v in observed.items())]
                    assert (cert['lower'],cert['upper'])==(min(fees),max(fees));completions+=len(fees);states+=1;local_states+=1
                cases.append(dict(n=n,costs=costs,r=r,partial_states=local_states))
            g01.save(directory/'progress.json',dict(cases=cases,checked_states=states,completion_comparisons=completions))
    costs=[2,7,2];roots=mk.plan(costs,5)['roots'];interval=[F(0),F(0)]
    for bits in product((0,1),repeat=3):
        observed=dict(aq.trace(bits,'center'));cert=produce(costs,roots,observed)
        interval[0]+=F(cert['lower'],8);interval[1]+=F(cert['upper'],8)
    assert interval==[F(53,8),F(81,8)]
    negative=[];cert=produce(costs,roots,{1:0})
    for label,changed in [('lower',copy.deepcopy(cert)),('witness',copy.deepcopy(cert)),('binding',copy.deepcopy(cert))]:
        if label=='lower':changed['tables']['lower']['ordinary'][0,2]+=1
        if label=='witness':changed['witnesses']['upper'][1]=1
        if label=='binding':changed['binding']='wrong'
        rejected=False
        try:check(costs,roots,{1:0},changed)
        except ValueError:rejected=True
        assert rejected;negative.append(dict(kind=label,rejected=True))
    counts=[0,0];sums=[F(0),F(0)]
    for t in range(10000):
        i=min(range(2),key=lambda j:(sums[j],j));counts[i]+=1;sums[i]+=[F(3,4),F(1)][i]
    assert abs(F(counts[1],10000)-F(3,7))<F(1,10000)
    g01.save(directory/'results.json',dict(status='complete',cases=cases,partial_states=states,completion_comparisons=completions,
        on_policy_collapses=collapse,sharp_countermodel_mean_interval=interval,negative_controls=negative,
        naive_partial_pooling_counts=counts,naive_partial_pooling_regret=F(counts[1],4),physical_audits=0))
    print(json.dumps(dict(status='complete',partial_states=states,completion_comparisons=completions,on_policy_collapses=collapse,
        sharp_interval=interval,pooling_counts=counts),default=g01.encode))


if __name__=='__main__':run(Path(sys.argv[1]))
