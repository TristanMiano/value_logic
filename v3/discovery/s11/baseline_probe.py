"""DEVELOPMENT exact baseline usefulness identities, Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
from matching_core import matching_orders,sparse_delta
from local_feedback import stopping


def receipts(world,edges,stop):
    observed={};events=[];j=0;n=len(world);queries=0;edges=set(edges)
    while j<n and not stop(observed):
        if j in edges:
            observed[j+1]=world[j+1];queries+=1
            events.append((j,'edge',int(stop(observed))))
            if stop(observed):break
            observed[j]=world[j];queries+=1;j+=2
        else:
            observed[j]=world[j];queries+=1
            if j<n-1:events.append((j,'singleton',int(stop(observed))))
            j+=1
    return events,queries


def case(index):
    n=(4,5,6,7)[index];mode=('sum','sum','dnf','two_sided')[index];threshold=(1,3,0,4)[index]
    family=matching_orders(n);fees=[1+(j*3%7) for j in range(n)];c=max(fees)
    stop=lambda r:stopping(r,mode,threshold,n);gamma=F(1,5)
    counts={'panels':0,'paths':0,'mean_identities':0,'second_moment_identities':0,'score_identities':0,'convexity_checks':0}
    summaries={key:[] for key in ('zero','half','full','oracle')}
    for scheme in range(3):
        weights=[F(1) if scheme==0 else F(1+(j*7+scheme)%9,1+(j*2+scheme)%5) for j in range(n-1)]
        masses=[]
        for _,edges in family:
            mass=F(1)
            for j in edges:mass*=weights[j]
            masses.append(mass)
        total=sum(masses,F(0));Q=[v/total for v in masses];P=[(1-gamma)*q+gamma/F(len(family)) for q in Q]
        qe=[sum((q for q,(_,edges) in zip(Q,family) if j in edges),F(0)) for j in range(n-1)]
        pe=[sum((p for p,(_,edges) in zip(P,family) if j in edges),F(0)) for j in range(n-1)]
        ps=[sum((p for p,(_,edges) in zip(P,family) if j not in edges and j-1 not in edges),F(0)) for j in range(n-1)]
        for world in product((0,1),repeat=n):
            a=[];d=[];live=[];opt=[]
            for j in range(n-1):
                prefix={i:world[i] for i in range(j)};live.append(not stop(prefix))
                a.append(fees[j+1]*int(stop(prefix|{j:world[j]})) if live[-1] else 0)
                d.append(fees[j]*int(stop(prefix|{j+1:world[j+1]})) if live[-1] else 0)
                opt.append((pe[j]*a[j]+ps[j]*d[j])/(pe[j]+ps[j]))
            baselines={'zero':[F(0)]*(n-1),'half':[F(c,2)]*(n-1),'full':[F(c)]*(n-1),'oracle':opt}
            means={name:[F(0)]*(n-1) for name in baselines}
            seconds={name:[F(0)]*(n-1) for name in baselines}
            score_means={name:F(0) for name in baselines}
            for probability,(_,edges) in zip(P,family):
                events,_=receipts(world,edges,stop);scores={}
                for name,baseline in baselines.items():
                    estimate=[F(0)]*(n-1);score=F(0)
                    for j,kind,certified in events:
                        if kind=='singleton':difference=fees[j+1]*certified-baseline[j];p=ps[j]
                        else:difference=baseline[j]-fees[j]*certified;p=pe[j]
                        estimate[j]=difference/p;score+=qe[j]*difference**2/p**2
                    for j in range(n-1):means[name][j]+=probability*estimate[j];seconds[name][j]+=probability*estimate[j]**2
                    score_means[name]+=probability*score;scores[name]=score
                assert scores['half']<=(scores['zero']+scores['full'])/2
                counts['convexity_checks']+=1;counts['paths']+=1
            true,_,_=sparse_delta(dict(enumerate(world)),n,fees,stop)
            for name,baseline in baselines.items():
                V=F(0)
                for j,b in enumerate(baseline):
                    assert means[name][j]==true.get(j,F(0));counts['mean_identities']+=1
                    expected=F(live[j])*((a[j]-b)**2/ps[j]+(d[j]-b)**2/pe[j])
                    decomposed=F(live[j])*((a[j]-d[j])**2/(ps[j]+pe[j])+(1/ps[j]+1/pe[j])*(b-opt[j])**2)
                    assert seconds[name][j]==expected==decomposed;counts['second_moment_identities']+=1
                    V+=qe[j]*expected
                assert score_means[name]==V;counts['score_identities']+=1;summaries[name].append(V)
            counts['panels']+=1
    # One deliberately invalid orientation-dependent baseline: no stopping is
    # possible, singleton baseline zero, paired baseline one. True delta=0,
    # but the pair contribution has expectation one, independent of its p.
    e=F(1,2);bad_mean=e*(F(1)/e);assert bad_mean==1
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'n':n,'mode':mode,'threshold':threshold,
      'counts':counts,'gamma':str(gamma),'baseline_score_sums':{name:str(sum(vals,F(0))) for name,vals in summaries.items()},
      'orientation_dependent_counterexample':{'true_delta':'0','mean_estimate':str(bad_mean)},
      'hashes':{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('baseline_probe.py','matching_core.py','local_feedback.py')},
      'scope':'Finite exact estimator and observable score identities. Oracle baseline is diagnostic, not an available model. No service or model-price claim.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
