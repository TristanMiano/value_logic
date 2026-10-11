"""DEVELOPMENT: symmetric working mixtures and a stronger decision control.

Codex (GPT-6), 2026-10-11. Preserves sampling_probe.py and its exposed run.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import random
import sys
import time
import traceback
import sampling_probe as first


def interval(N,s,e,alpha,counter=None,rho=F(1,2)):
    counter = counter if counter is not None else Counter()
    counter['intervals'] += 1
    if s==0:return 0,N
    if s==N:return e,e
    level=alpha*((1-rho)/F(s+1)+rho/2*int(e in (0,s)))
    lhs=level.numerator*comb(N,s)
    counter['binomial_calls']+=1
    def inside(M):
        rhs=level.denominator*comb(M,e)*comb(N-M,s-e)
        counter['membership_checks']+=1
        counter['binomial_calls']+=2
        counter['largest_integer_bits']=max(counter['largest_integer_bits'],lhs.bit_length(),rhs.bit_length())
        return lhs < rhs
    a,b=e,N-s+e
    mode=max(a,min(b,e*(N+1)//s))
    assert inside(mode)
    lo,hi=a,mode
    while lo<hi:
        mid=(lo+hi)//2
        if inside(mid):hi=mid
        else:lo=mid+1
    lower=lo
    lo,hi=mode,b
    while lo<hi:
        mid=(lo+hi+1)//2
        if inside(mid):lo=mid
        else:hi=mid-1
    return lower,lo


def reject_lower(N,s,e,M0,M1,alpha,counter=None):
    """Reject composite M<=M0. M1>M0 fixed before sampling."""
    assert 0<=e<=s<=N and 0<=M0<M1<=N
    counter=counter if counter is not None else Counter()
    counter['likelihood_tests']+=1
    if e>M0:return True
    if s-e>N-M0 or e>M1 or s-e>N-M1:return False
    null=comb(M0,e)*comb(N-M0,s-e)
    alternative=comb(M1,e)*comb(N-M1,s-e)
    counter['binomial_calls']+=4
    return alpha.numerator*alternative >= alpha.denominator*null


def direct(y,pred,alpha,epsilon,seed):
    assert epsilon==0
    start=time.perf_counter_ns()
    N=len(y)
    predicted=sum(pred)
    # Same pre-lottery prediction input as guidance, with scan charged.
    M0=(N+1)//2-1
    M1=max(M0+1,(N+abs(2*predicted-N)+1)//2)
    sampler=first.WithoutReplacement(N,random.Random(seed))
    s=e=0
    counts=Counter(prediction_reads=N)
    stages=[]
    action=None
    while action is None:
        target=min(N,max(1,2*s))
        while s<target:
            e+=y[sampler.take()]
            s+=1
        if reject_lower(N,s,e,M0,M1,alpha/2,counts):action=1
        elif reject_lower(N,s,s-e,M0,M1,alpha/2,counts):action=0
        elif s==N:action=int(2*e>=N)
        stages.append(dict(queries=s,ones=e,action=action))
    return dict(mode='direct_prediction_gap',queries=s,action=action,counts=dict(counts),
                M0=M0,M1=M1,stages=stages,controller_ns=time.perf_counter_ns()-start)


def small_screen():
    cases=0
    largest=F(0)
    for N in range(1,10):
        for alpha in (F(1,5),F(1,20)):
            cis={(s,e):interval(N,s,e,alpha) for s in range(N+1) for e in range(s+1)}
            for (s,e),ci in cis.items():
                if s==0:allowed=list(range(N+1))
                else:
                    q=(F(1,2)/F(s+1)+F(1,4)*int(e in (0,s)))
                    allowed=[M for M in range(e,N-s+e+1) if F(comb(M,e)*comb(N-M,s-e),comb(N,s))>alpha*q]
                assert ci==(min(allowed),max(allowed))
            failures=Counter()
            for bits in product((0,1),repeat=N):
                M,e=sum(bits),0
                bad=False
                for s,b in enumerate(bits,1):
                    e+=b
                    L,U=cis[s,e]
                    bad |= not L<=M<=U
                failures[M]+=bad
            for M in range(N+1):
                risk=F(failures[M],comb(N,M))
                assert risk<=alpha
                largest=max(largest,risk)
                cases+=1
    direct_cases=0
    for N in range(2,10):
        M0=(N+1)//2-1
        for M1 in range(M0+1,N+1):
            for alpha in (F(1,5),F(1,20)):
                failures=Counter()
                for bits in product((0,1),repeat=N):
                    M=sum(bits)
                    if M>M0:continue
                    e=0
                    bad=False
                    for s,b in enumerate(bits,1):
                        e+=b
                        bad |= reject_lower(N,s,e,M0,M1,alpha)
                    failures[M]+=bad
                for M in range(M0+1):
                    risk=F(failures[M],comb(N,M))
                    assert risk<=alpha
                    direct_cases+=1
    return dict(mixture_count_cases=cases,direct_composite_null_cases=direct_cases,
                largest_mixture_risk=largest)


def main(output):
    assert not output.exists()
    result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(first.__file__))},
                scope='Same synthetic populations as sampling01, stronger ordinary control; runtime includes controller and synthetic labels, excludes unmeasured prediction inference and real mathematical evaluation')
    start=time.monotonic_ns()
    original=first.interval
    try:
        result['checks']=small_screen()
        rng=random.Random(8406)
        rows=[]
        for fraction in (F(13,25),F(11,20),F(13,20)):
            N=4096
            y=[int(i<N*fraction) for i in range(N)]
            rng.shuffle(y)
            for corruption in (F(0),F(1,50),F(1,5),F(1)):
                pred=[1-bit if rng.randrange(corruption.denominator)<corruption.numerator else bit for bit in y]
                row=dict(actual_mean=F(sum(y),N),corruption=corruption,predicted_ones=sum(pred),
                         population_sha256=hashlib.sha256(bytes(y)).hexdigest(),
                         predictions_sha256=hashlib.sha256(bytes(pred)).hexdigest())
                row['direct']=direct(y,pred,F(1,20),F(0),8407)
                first.interval=interval
                row['guided_mixture']=first.guided(y,pred,F(1,20),F(0),8407)
                row['guided_mixture']['mode']='guided_extreme_mixture'
                first.interval=original
                row['guided_uniform']=first.guided(y,pred,F(1,20),F(0),8407)
                row['ordinary_uniform']=first.ordinary(y,pred,F(1,20),F(0),8407)
                row['realized_correct']={m:row[m]['action']==int(sum(y)*2>=N) for m in ('direct','guided_mixture','guided_uniform','ordinary_uniform')}
                rows.append(row)
        result.update(status='complete',rows=rows)
    except Exception:
        result.update(status='failed',failure=traceback.format_exc())
        raise
    finally:
        first.interval=original
        result.update(elapsed_ns=time.monotonic_ns()-start,end_utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='rows'},default=str))


if __name__=='__main__':main(Path(sys.argv[1]))
