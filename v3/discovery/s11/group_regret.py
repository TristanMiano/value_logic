"""DEVELOPMENT exact grouped-mean regret oracle. Codex (GPT-6)."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations,product
from pathlib import Path
import argparse
import hashlib
import json
import random
import time

from query_flip import compact_plan,matches,signs,unrestricted_plan
from robust_flip import point_source,policy_value,regret_oracle,summarize_policy


def group_oracle(src,groups,rows,weights,flip_fee,query_fee,H,box,check_profiles=False):
    r=src['r'];G=len(groups)
    S=[[sum((weights[i]*row[1][i] for i in group),F(0)) for group in groups] for row in rows]
    A=[sum((weights[i] for i in group),F(0)) for group in groups]
    counts=dict(histories=0,lines=0,sorted_gain_entries=0,profile_subset_checks=0,convolution_options=0)

    @lru_cache(None)
    def leaf(h):
        counts['histories']+=1
        ids=[t for t,z in enumerate(src['cells']) if matches(z,h)]
        P=sum((src['mass'][t] for t in ids),F(0))
        fee=sum((src['mass'][t]*rows[t][0] for t in ids),F(0))
        zero=F(0);profiles=[]
        for g,group in enumerate(groups):
            slope=F(0);intercept=F(0);crossings={}
            for t in ids:
                p=src['mass'][t];lo,hi=box[t][g]
                zero+=p*max(lo*S[t][g],hi*S[t][g])
                slope+=2*p*lo;intercept+=p*lo*(S[t][g]-A[g])
                if hi>lo and p:
                    key=(A[g]-S[t][g])/2
                    da,db=crossings.get(key,(F(0),F(0)))
                    crossings[key]=(da+2*p*(hi-lo),db+p*(hi-lo)*(S[t][g]-A[g]))
            lines=[(slope,intercept)]
            for key,(da,db) in sorted(crossings.items()):
                slope+=da;intercept+=db;lines.append((slope,intercept))
            counts['lines']+=len(lines)
            limit=min(H,len(group));profile=[None]*(limit+1)
            for alpha,beta in lines:
                gains=sorted(((alpha*weights[i]-P*flip_fee[i],i) for i in group),reverse=True)
                counts['sorted_gain_entries']+=len(gains)
                value=beta;chosen=[]
                for j in range(limit+1):
                    if j:
                        gain,i=gains[j-1];value+=gain;chosen.append(i)
                    if profile[j] is None or value>profile[j][0]:profile[j]=(value,tuple(chosen))
            if check_profiles:
                for j in range(limit+1):
                    expected=None
                    for chosen in combinations(group,j):
                        value=F(0);total=sum((weights[i] for i in chosen),F(0))
                        for t in ids:
                            c=S[t][g]-A[g]+2*total;lo,hi=box[t][g]
                            value+=src['mass'][t]*max(c*lo,c*hi)
                        value-=P*sum((flip_fee[i] for i in chosen),F(0))
                        expected=value if expected is None else max(expected,value)
                        counts['profile_subset_checks']+=1
                    assert expected==profile[j][0],(h,g,j,expected,profile[j])
            profiles.append(profile)
        return P,fee,zero,profiles

    @lru_cache(None)
    def solve(h,k):
        P,fee,zero,profiles=leaf(h)
        dp={0:(F(0),())}
        for profile in profiles:
            nxt={}
            for used,(v,chosen) in dp.items():
                for j,(cost,selection) in enumerate(profile[:k-used+1]):
                    counts['convolution_options']+=1
                    proposed=(v+cost,chosen+selection)
                    if used+j not in nxt or proposed[0]>nxt[used+j][0]:nxt[used+j]=proposed
            dp=nxt
        one,chosen=max(dp.values(),key=lambda x:x[0])
        best,action=fee+zero,('terminal_0',)
        if fee+one>best:best,action=fee+one,('terminal_1',chosen)
        if k:
            for j in range(r):
                if h[j]:continue
                value=-query_fee[j]*P
                for o in (-1,1):
                    child=tuple(o if j==i else h[i] for i in range(r))
                    value+=solve(child,k-1)[0]
                if value>best:best,action=value,('query',j)
        return best,action

    value,action=solve((0,)*r,H)
    adversary=summarize_policy(src,solve,flip_fee,query_fee,H)
    witness=[]
    for t in range(len(src['cells'])):
        mu=[]
        for g,group in enumerate(groups):
            other=sum((weights[i]*adversary[t][1][i] for i in group),F(0))
            lo,hi=box[t][g];mu.append(hi if S[t][g]>other else lo)
        witness.append(mu)
    return value,action,adversary,witness,counts


def expand(groups,rows,r):
    mapping={i:g for g,group in enumerate(groups) for i in group}
    m=len(mapping)
    return [[row[mapping[i]] for i in range(r,m)] for row in rows]


def law(src,groups,means):
    mapping={i:g for g,group in enumerate(groups) for i in group};r=src['r'];result={}
    for z,p,mus in zip(src['cells'],src['mass'],means):
        for y in signs(len(groups)-r):
            prob=p
            for yi,mu in zip(y,mus[r:]):prob*=(1+yi*mu)/2
            latent=z+y;world=tuple(latent[mapping[i]] for i in range(src['m']))
            result[world]=result.get(world,F(0))+prob
    assert sum(result.values())==1
    return {x:p for x,p in result.items() if p}


def case(index):
    settings=((4,1,2,0),(5,1,3,2),(6,2,4,3),(6,1,3,4),(5,0,2,7),(101,3,10,6))
    m,r,G,H=settings[index];rng=random.Random(60000+index);start=time.perf_counter_ns()
    groups=[(i,) for i in range(r)]+[tuple(i for i in range(r,m) if (i-r)%(G-r)==g) for g in range(G-r)]
    cells=signs(r);raw=[rng.randrange(1,8) for z in cells]
    if index==2:raw[0]=0
    mass=[F(v,sum(raw)) for v in raw]
    weights=tuple(F(rng.randrange(-3,4),2) for _ in range(m))
    flip_fee=tuple(F(rng.randrange(0,5),4) for _ in range(m));query_fee=(F(1,8),)*r
    box=[]
    for z in cells:
        b=[(F(zi),F(zi)) for zi in z]
        for _ in range(G-r):
            center=F(rng.randrange(-3,4),4);width=F(rng.randrange(1,5),4)
            b.append((max(F(-1),center-width),min(F(1),center+width)))
        box.append(b)
    means=[[(lo+hi)/2 for lo,hi in row] for row in box]
    src=dict(m=m,r=r,cells=cells,mass=mass,moments=[])
    src=point_source(src,expand(groups,means,r))
    nominal=compact_plan(src,weights,flip_fee,query_fee,H)
    rows=summarize_policy(src,nominal[4],flip_fee,query_fee,H)
    if index in (1,3,5):rows=[(fee*F(2,3),tuple(F(2,3)*s for s in coeff)) for fee,coeff in rows]
    value,action,adversary,witness,counts=group_oracle(src,groups,rows,weights,flip_fee,query_fee,H,box,index<5)
    expanded=expand(groups,witness,r)
    opt=compact_plan(point_source(src,expanded),weights,flip_fee,query_fee,H)[0]
    assert policy_value(src,rows,weights,expanded)-opt==value
    assert policy_value(src,rows,weights,expanded)-policy_value(src,adversary,weights,expanded)==value
    assert value>=0
    corner_checks=0;unrestricted_checks=0;corner_max=None
    if index<5:
        endpoints=[tuple(sorted(set(pair))) for row in box for pair in row[r:]]
        for values in product(*endpoints):
            mus=[list(z)+list(values[t*(G-r):(t+1)*(G-r)]) for t,z in enumerate(cells)]
            emu=expand(groups,mus,r)
            other=compact_plan(point_source(src,emu),weights,flip_fee,query_fee,H)[0]
            regret=policy_value(src,rows,weights,emu)-other
            corner_max=regret if corner_max is None else max(corner_max,regret)
            corner_checks+=1
            if index in (0,1,4):
                actual,_=unrestricted_plan(law(src,groups,mus),weights,flip_fee,query_fee,H)
                assert actual==other
                unrestricted_checks+=1
        assert corner_max==value,(index,corner_max,value)
    outer=regret_oracle(src,rows,weights,flip_fee,query_fee,H,expand(groups,box,r))[0]
    assert outer>=value
    return {'case':index,'m':m,'r':r,'groups':groups,'H':H,'group_regret':str(value),
            'independent_coordinate_outer_regret':str(outer),'outer_minus_group':str(outer-value),
            'corner_checks':corner_checks,'unrestricted_checks':unrestricted_checks,'counts':counts,
            'query_cell_count':len(cells),'retained_mass_and_group_moment_entries':len(cells)*(G-r+1),
            'action':action,'mass':list(map(str,mass)),'weights':list(map(str,weights)),
            'flip_fee':list(map(str,flip_fee)),'query_fee':list(map(str,query_fee)),
            'proposal':[{'fee':str(fee),'coefficients':list(map(str,co))} for fee,co in rows],
            'box':[[[str(lo),str(hi)] for lo,hi in row] for row in box],
            'witness':[[str(mu) for mu in row] for row in witness],
            'elapsed_ns':time.perf_counter_ns()-start,
            'scope':'Exact fixed-policy grouped conditional-mean regret. Aliases and interval source supplied, not learned. Independent-coordinate bound is a relaxation, not strongest ordinary comparator.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case);result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','m','r','group_regret','independent_coordinate_outer_regret','corner_checks','unrestricted_checks','counts','elapsed_ns')}))


if __name__=='__main__':main()
