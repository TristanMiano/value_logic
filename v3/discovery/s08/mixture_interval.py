"""Exact outer grid brackets for a uniform Bernoulli-mixture CS.
DEVELOPMENT, Codex (GPT-6), 2026-10-14.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import sys
import g01

HERE=Path(__file__).resolve().parent
D=4096


def confidence(n,s,m,meter):
    if m!=1 or type(n)is not int or type(s)is not int or not 0<=s<=n:raise ValueError('Single Bernoulli count required')
    if n==0:return F(0),F(1)
    factor=20*(n+1)*comb(n,s);right=D**n
    def accepted(k):
        a=k**s;b=(D-k)**(n-s);left=factor*a*b
        meter.pay('confidence','exact_grid_power_and_integer_likelihood_comparison',
            8+(a.bit_length()+b.bit_length()+left.bit_length()+right.bit_length()+63)//64)
        return left>=right
    floor=D*s//n;ceil=(D*s+n-1)//n
    if accepted(0):lo=0
    elif not accepted(floor):lo=floor
    else:
        a,b=0,floor
        while b-a>1:
            mid=(a+b)//2
            if accepted(mid):b=mid
            else:a=mid
        lo=a
    if accepted(D):hi=D
    elif not accepted(ceil):hi=ceil
    else:
        a,b=ceil,D
        while b-a>1:
            mid=(a+b)//2
            if accepted(mid):a=mid
            else:b=mid
        hi=b
    meter.pay('confidence','binomial_factor_grid_bracketing_and_retention',20+factor.bit_length())
    assert F(lo,D)<=F(s,n)<=F(hi,D)
    return F(lo,D),F(hi,D)


def allowed(n,s,p):return 20*(n+1)*comb(n,s)*p**s*(1-p)**(n-s)>=1


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    meter=g01.kernel.Meter();checks=0;intervals=0
    for n in range(65):
        for s in range(n+1):
            lo,hi=confidence(n,s,1,meter);intervals+=1
            for j in range(65):
                p=F(j,64)
                if allowed(n,s,p):assert lo<=p<=hi
                checks+=1
            if lo>0:assert not allowed(n,s,lo)
            if hi<1:assert not allowed(n,s,hi)
    first_rejections=[]
    for p in [F(0),F(1,100),F(1,10),F(1,4),F(1,2),F(3,4),F(9,10),F(99,100),F(1)]:
        alive={0:F(1)};rejected=F(0);records=[]
        for n in range(1,129):
            updated={}
            for s,prob in alive.items():
                for bit,chance in [(0,1-p),(1,p)]:
                    weight=prob*chance
                    if not weight:continue
                    new=s+bit
                    if allowed(n,new,p):updated[new]=updated.get(new,F(0))+weight
                    else:rejected+=weight
            alive=updated
            assert rejected<=F(1,20) and rejected+sum(alive.values())==1
            if n in (8,32,128):records.append(dict(n=n,first_rejection_probability=rejected))
        first_rejections.append(dict(p=p,checkpoints=records))
    g01.save(directory/'results.json',dict(status='complete',stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        intervals=intervals,membership_checks=checks,first_rejections=first_rejections,invoice=meter.record(),
        physical_audits=0,source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'mixture_interval.md')))
    print(json.dumps(dict(status='complete',intervals=intervals,membership_checks=checks,finite_horizon_sources=len(first_rejections))))


if __name__=='__main__':run(Path(sys.argv[1]))
