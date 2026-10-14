"""Partial star robust action DP, Codex (GPT-6), DEVELOPMENT."""
from itertools import product
from pathlib import Path
import json
import random
import sys
import g01
Meter=g01.kernel.Meter;HERE=Path(__file__).resolve().parent

def endpoint_metrics(weights,H,known,count,meter):
    if len(count)!=len(weights) or any(type(k)is not int or k not in(0,1,2) for k in count):raise ValueError('Invalid action count')
    rr=[];uu=[];ll=[]
    for z in ([known[0]] if 0 in known else [0,H]):
        r=u=l=0
        for i,(w,k) in enumerate(zip(weights,count),1):
            lo=hi=known[i] if i in known else None
            if i not in known:lo,hi=0,H
            r+=max(w*(k*y+(2-k)*z-2*min(y,z)) for y in(lo,hi))
            u+=w*(k*hi+(2-k)*z);l+=2*w*min(lo,z)
            meter.pay('bounds','source_endpoint_regret_upper_and_optimum_lower',25)
        rr.append(r);uu.append(u);ll.append(l)
    return max(rr),max(uu),min(ll)

def propose(weights,H,known,tau,meter,cap=100000):
    if (type(H)is not int or H<=0 or type(tau)is not int or tau<0 or not weights
        or any(type(w)is not int or w<=0 for w in weights)
        or any(type(i)is not int or not 0<=i<=len(weights) or type(v)is not int or not 0<=v<=H for i,v in known.items())):
        raise ValueError('Invalid source/partial receipt/tolerance')
    center=known.get(0);table={(0,0):(0,())} if center is None else {0:(0,())}
    states=1;transitions=0
    for i,w in enumerate(weights,1):
        lo,hi=(known[i],known[i]) if i in known else (0,H);nxt={}
        for state,(u,count) in table.items():
            for k in(0,1,2):
                transitions+=1;meter.pay('planning','partial_star_dp_transition',18+len(count))
                if center is None:
                    x,y=state;key=x+k*w*hi,y+(2-k)*w*(H-lo)
                    if max(key)>tau:continue
                    upper=u+w*(k*hi+(2-k)*H)
                else:
                    delta=max(w*(k*v+(2-k)*center-2*min(v,center)) for v in(lo,hi))
                    key=state+delta
                    if key>tau:continue
                    upper=u+w*(k*hi+(2-k)*center)
                candidate=(upper,count+(k,))
                if key not in nxt or candidate<nxt[key]:nxt[key]=candidate
                if len(nxt)>cap:return dict(status='UNRESOLVED',reason='state_cap',states=states+len(nxt),transitions=transitions)
        table=nxt;states+=len(table)
        if not table:return dict(status='INFEASIBLE',states=states,transitions=transitions)
    upper,count=min(table.values());R,U,L=endpoint_metrics(weights,H,known,count,meter)
    if R>tau or U!=upper:raise AssertionError('Producer endpoint mismatch')
    return dict(status='WITNESS',count=list(count),R=R,U=U,L=L,states=states,transitions=transitions)

def world_metrics(weights,row,count):
    cost=sum(w*(k*row[i]+(2-k)*row[0]) for i,(w,k) in enumerate(zip(weights,count),1))
    opt=sum(2*w*min(row[0],row[i]) for i,w in enumerate(weights,1))
    return cost-opt,cost,opt

def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes());(directory/'declaration.md').write_bytes((HERE/'partial_star.md').read_bytes())
    rng=random.Random(8141650);cases=[dict(name=f'n{n}r{j}',weights=[1]*n if j==0 else [rng.randrange(1,7) for _ in range(n)],H=4) for n in range(1,5) for j in range(2)]
    g01.save(directory/'design.json',dict(cases=cases,physical_audits=0,source_sha256=g01.sha(__file__),stage='DEVELOPMENT'));results=[]
    for case in cases:
        weights=case['weights'];H=case['H'];n=len(weights);meter=Meter();states=actions=worlds=targets=cap_tests=0
        for observation in product((None,0,2,4),repeat=n+1):
            known={i:v for i,v in enumerate(observation) if v is not None};points=[];states+=1
            options=[(known[i],) if i in known else(0,H) for i in range(n+1)]
            for count in product((0,1,2),repeat=n):
                metrics=endpoint_metrics(weights,H,known,count,Meter());checks=[world_metrics(weights,row,count) for row in product(*options)]
                brute=(max(r for r,u,l in checks),max(u for r,u,l in checks),min(l for r,u,l in checks))
                assert metrics==brute;worlds+=len(checks);actions+=1;points.append((*metrics[:2],count))
                if n<=2 and all(x is None for x in observation):
                    for row in product(range(H+1),repeat=n+1):
                        r,u,l=world_metrics(weights,row,count);assert r<=metrics[0] and u<=metrics[1] and l>=metrics[2];worlds+=1
            taus=sorted({max(0,r+d) for r,u,c in points for d in(-1,0,1)})
            for tau in taus:
                answer=propose(weights,H,known,tau,meter);expect=min((u for r,u,c in points if r<=tau),default=None)
                assert (answer['status']=='INFEASIBLE')==(expect is None)
                if expect is not None:assert answer['status']=='WITNESS' and answer['U']==expect
                targets+=1
            if states==1:
                answer=propose(weights,H,known,2*H*sum(weights),Meter(),cap=0)
                assert answer['status']=='UNRESOLVED' and answer['reason']=='state_cap';cap_tests+=1
        record=dict(name=case['name'],partial_states=states,action_checks=actions,world_checks=worlds,target_checks=targets,cap_tests=cap_tests,invoice=meter.record())
        g01.save(directory/f"{case['name']}.json",record);results.append({k:v for k,v in record.items() if k!='invoice'});print(record['name'],states,actions,targets,flush=True)
    g01.save(directory/'results.json',dict(status='complete',cases=results,physical_audits=0))

if __name__=='__main__':run(Path(sys.argv[1]))
