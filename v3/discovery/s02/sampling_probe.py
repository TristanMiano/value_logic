"""DEVELOPMENT: exact finite-population confidence-sequence specialization.

Codex (GPT-6), 2026-10-11. Synthetic paid-bit interface; no measured solver
benefit. Seeded sample streams are development fixtures, not a claim that
their deterministic pseudorandom generator supplies the theorem's randomness.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb
import hashlib
import json
from pathlib import Path
import random
import sys
import time
import traceback


def interval(N,s,e,alpha,counter=None):
    assert 0 <= e <= s <= N and 0 < alpha < 1
    counter = counter if counter is not None else Counter()
    counter['intervals'] += 1
    if s == 0:
        return 0,N
    if s == N:
        return e,e
    denominator = comb(N,s)
    counter['binomial_calls'] += 1
    lhs = alpha.numerator*denominator
    def inside(M):
        rhs = alpha.denominator*(s+1)*comb(M,e)*comb(N-M,s-e)
        counter['membership_checks'] += 1
        counter['binomial_calls'] += 2
        counter['largest_integer_bits'] = max(counter['largest_integer_bits'],lhs.bit_length(),rhs.bit_length())
        return lhs < rhs
    a,b = e,N-s+e
    mode = max(a,min(b,e*(N+1)//s))
    assert inside(mode)
    lo,hi = a,mode
    while lo < hi:
        mid=(lo+hi)//2
        if inside(mid):hi=mid
        else:lo=mid+1
    lower=lo
    lo,hi = mode,b
    while lo < hi:
        mid=(lo+hi+1)//2
        if inside(mid):lo=mid
        else:hi=mid-1
    return lower,lo


def small_coverage():
    records=[]
    for N in range(1,11):
        for alpha in (F(1,5),F(1,20)):
            @lru_cache(None)
            def ci(s,e):
                got=interval(N,s,e,alpha)
                denom=comb(N,s)
                allowed=[M for M in range(N+1) if M>=e and N-M>=s-e and
                         alpha.numerator*denom < alpha.denominator*(s+1)*comb(M,e)*comb(N-M,s-e)]
                assert got == (min(allowed),max(allowed))
                return got
            failures=Counter()
            for bits in product((0,1),repeat=N):
                M,e=sum(bits),0
                bad=False
                for s,bit in enumerate(bits,1):
                    e+=bit
                    L,U=ci(s,e)
                    bad |= not L <= M <= U
                failures[M]+=bad
            for M in range(N+1):
                risk=F(failures[M],comb(N,M))
                assert risk <= alpha
                records.append(dict(N=N,M=M,alpha=alpha,ever_excluded=risk))
    return records


class WithoutReplacement:
    """Partial Fisher-Yates over virtual indices; avoids a free full shuffle."""
    def __init__(self,N,rng):
        self.left,self.rng,self.swaps=N,rng,{}
    def take(self):
        j=self.rng.randrange(self.left)
        item=self.swaps.get(j,j)
        last=self.left-1
        self.swaps[j]=self.swaps.get(last,last)
        self.swaps.pop(last,None)
        self.left-=1
        return item


def choose(L,U,epsilon):
    # First action has loss 1-mu; second has loss mu.
    if max(F(0),1-2*L) <= epsilon:
        return 1
    if max(F(0),2*U-1) <= epsilon:
        return 0
    return None


def ordinary(y,pred,alpha,epsilon,seed):
    start=time.perf_counter_ns()
    N=len(y)
    sampler=WithoutReplacement(N,random.Random(seed))
    s=e=0
    L,U=F(0),F(1)
    counts=Counter()
    stages=[]
    while choose(L,U,epsilon) is None:
        target=min(N,max(1,2*s))
        while s<target:
            e+=y[sampler.take()]
            s+=1
        low,high=interval(N,s,e,alpha,counts)
        L,U=max(L,F(low,N)),min(U,F(high,N))
        stages.append(dict(queries=s,lower=L,upper=U))
    return dict(mode='ordinary_uniform',queries=s,action=choose(L,U,epsilon),lower=L,upper=U,
                counts=dict(counts),stages=stages,controller_ns=time.perf_counter_ns()-start)


def guided(y,pred,alpha,epsilon,seed):
    start=time.perf_counter_ns()
    N=len(y)
    groups=[[],[]]
    for i,bit in enumerate(pred):groups[bit].append(i)
    sizes=list(map(len,groups))
    samplers=[WithoutReplacement(size,random.Random(seed+h)) for h,size in enumerate(sizes)]
    samples,errors=[0,0],[0,0]
    lows,highs=[0,0],sizes.copy()
    counts,stages=Counter(),[]
    counts['prediction_partition_reads']=N
    order=[1,0] if sizes[1]>=sizes[0] else [0,1]
    def value_bounds():
        return F(sizes[1]-highs[1]+lows[0],N),F(sizes[1]-lows[1]+highs[0],N)
    for h in order:
        while samples[h]<sizes[h]:
            L,U=value_bounds()
            if choose(L,U,epsilon) is not None:break
            target=min(sizes[h],max(1,2*samples[h]))
            while samples[h]<target:
                i=groups[h][samplers[h].take()]
                errors[h]+=int(y[i]!=pred[i])
                samples[h]+=1
            low,high=interval(sizes[h],samples[h],errors[h],alpha/2,counts)
            lows[h],highs[h]=max(lows[h],low),min(highs[h],high)
            L,U=value_bounds()
            stages.append(dict(stratum=h,queries=sum(samples),stratum_samples=samples.copy(),
                               observed_errors=errors.copy(),lower=L,upper=U))
        L,U=value_bounds()
        if choose(L,U,epsilon) is not None:break
    assert choose(L,U,epsilon) is not None
    return dict(mode='prediction_strata',queries=sum(samples),action=choose(L,U,epsilon),lower=L,upper=U,
                counts=dict(counts),stages=stages,controller_ns=time.perf_counter_ns()-start)


def main(output):
    assert not output.exists()
    started=time.monotonic_ns()
    result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='exact small sampling-law enumeration and synthetic fixed truth populations; controller runtime includes interval arithmetic, sampling and partitioning; prediction inference and exact mathematical evaluator prices are not supplied')
    try:
        coverage=small_coverage()
        result['coverage']=coverage
        result['largest_exact_ever_exclusion']=max(r['ever_excluded'] for r in coverage)
        rng=random.Random(8406)
        rows=[]
        for fraction in (F(13,25),F(11,20),F(13,20)):
            N=4096
            y=[int(i<N*fraction) for i in range(N)]
            rng.shuffle(y)
            for corruption in (F(0),F(1,50),F(1,5),F(1)):
                pred=[1-bit if rng.randrange(corruption.denominator)<corruption.numerator else bit for bit in y]
                record=dict(N=N,actual_mean=F(sum(y),N),corruption_design=corruption,
                            predicted_ones=sum(pred),actual_prediction_errors=sum(a!=b for a,b in zip(y,pred)),
                            population_sha256=hashlib.sha256(bytes(y)).hexdigest(),
                            predictions_sha256=hashlib.sha256(bytes(pred)).hexdigest())
                record['ordinary']=ordinary(y,pred,F(1,20),F(0),8407)
                record['guided']=guided(y,pred,F(1,20),F(0),8407)
                record['realized_correct']={m:record[m]['action']==int(sum(y)*2>=N) for m in ('ordinary','guided')}
                rows.append(record)
        result.update(status='complete',rows=rows,seed=8406,sample_seed=8407)
    except Exception:
        result.update(status='failed',failure=traceback.format_exc())
        raise
    finally:
        result['elapsed_ns']=time.monotonic_ns()-started
        result['end_utc']=datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ('coverage','rows')},default=str))


if __name__=='__main__':
    main(Path(sys.argv[1]))
