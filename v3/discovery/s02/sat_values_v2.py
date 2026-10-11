"""DEVELOPMENT: fixed alternative mixtures and larger SAT populations.

Codex (GPT-6), 2026-10-11. Original source and run remain unchanged.
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
import sat_values as old


def reject(N,s,e,M0,alpha,counts):
    assert 0<=e<=s<=N and 0<=M0<N
    counts['mixture_tests']+=1
    if e>M0:return True
    if s-e>N-M0:return False
    gap=N-M0
    alternatives=sorted({M0+(gap+d-1)//d for d in (64,16,4,2,1)})
    null=comb(M0,e)*comb(N-M0,s-e)
    mixed=0
    counts['binomial_calls']+=2
    for M1 in alternatives:
        if e<=M1 and s-e<=N-M1:
            mixed+=comb(M1,e)*comb(N-M1,s-e)
            counts['binomial_calls']+=2
    return alpha.numerator*mixed>=alpha.denominator*len(alternatives)*null


def action(N,s,ones,zeros,offset,total,alpha,counts):
    assert ones+zeros<=s<=N
    if 2*(offset+ones)>=total:return 1
    if 2*(offset+N-zeros)<=total:return 0
    m0=(total+1)//2-1-offset
    if 0<=m0<N and reject(N,s,ones,m0,alpha/2,counts):return 1
    z0=offset+N-total//2-1
    if 0<=z0<N and reject(N,s,zeros,z0,alpha/2,counts):return 0
    return None


def request(family,lit,mode,alpha,seed):
    if mode in ('exact_proof_first','proof_first_fixed'):
        return old.request(family,lit,mode.replace('_fixed','_direct'),alpha,seed)
    start=time.perf_counter_ns()
    before=family.counts.copy()
    total=len(family.forms)
    counts=Counter()
    group=list(range(total)) if mode=='uniform_mixture' else [i for i,b in enumerate(family.base) if b]
    offset=0
    counts['partition_reads']+=total
    if mode=='proof_first_mixture':
        pending=[]
        for i in group:
            if family.proof(i,lit)==1:offset+=1
            else:pending.append(i)
        group=pending
    N=len(group)
    sampler=old.base_sampling.WithoutReplacement(N,random.Random(seed))
    s=ones=zeros=0
    stages=[]
    while True:
        got=action(N,s,ones,zeros,offset,total,alpha,counts)
        if got is not None:break
        target=min(N,max(s+1,(s*1415+999)//1000))
        assert target>s
        while s<target:
            bit=family.label(group[sampler.take()],lit)
            ones+=bit;zeros+=1-bit;s+=1
        stages.append(dict(sampled=s,ones=ones,zeros=zeros))
    return dict(mode=mode,unit_literal=lit,action=got,sampled=s,remaining_population=N,
                proved_ones=offset,counts=dict(counts+family.counts-before),stages=stages,
                request_ns=time.perf_counter_ns()-start)


def small_screen():
    cases=0
    for N in range(2,9):
        for M0 in range(N):
            for alpha in (F(1,5),F(1,20)):
                failures=Counter()
                table={(s,e):reject(N,s,e,M0,alpha,Counter()) for s in range(N+1) for e in range(s+1)}
                for s in range(N+1):
                    vals=[table[s,e] for e in range(s+1)]
                    assert vals==sorted(vals)
                for bits in product((0,1),repeat=N):
                    M=sum(bits)
                    if M>M0:continue
                    e=0;bad=False
                    for s,b in enumerate(bits,1):
                        e+=b;bad |= table[s,e]
                    failures[M]+=bad
                for M in range(M0+1):
                    assert F(failures[M],comb(N,M))<=alpha
                    cases+=1
    return dict(composite_count_cases=cases,monotone_in_observed_ones=True)


def main(output):
    assert not output.exists()
    sources=[Path(__file__),Path(old.__file__),Path(old.sampling.__file__),Path(old.base_sampling.__file__)]
    rows=[]
    result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,rows=rows,
                sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                scope='Two larger seeded populations; warm installed runtime, common generation/import excluded; separate paid histories, charged proof scan/solver/checks/sampling/cleanup. Trusted native UNSAT. Total stream alpha=.05 over eight requests. Exact stage traces reduced to count and final three entries; source/seed reconstructs all inputs.')
    start=time.monotonic_ns()
    try:
        result['small_screen']=small_screen()
        for n in (60,100):
            ratio=F(83,20);N=1024
            seed=8500+n*100+int(ratio*100)
            rng=random.Random(seed)
            forms=tuple(old.formula(n,int(n*ratio),rng) for _ in range(N))
            edits=[lit for i in range(1,5) for lit in (i,-i)]
            definition=dict(n=n,ratio=str(ratio),N=N,seed=seed,
                            source_sha256=hashlib.sha256(json.dumps(forms).encode()).hexdigest())
            reference=old.Family(forms)
            truth=[[reference.label(i,lit) for i in range(N)] for lit in edits]
            reference.close()
            exact_actions=[int(2*sum(y)>=N) for y in truth]
            definition.update(base_sat=sum(reference.base),edited_sat=list(map(sum,truth)),
                              edited_truth_sha256=[hashlib.sha256(bytes(y)).hexdigest() for y in truth])
            for mode in ('exact_proof_first','proof_first_fixed','uniform_mixture','monotone_mixture','proof_first_mixture'):
                family=old.Family(forms)
                margin_start=time.perf_counter_ns();requests=[]
                for j,lit in enumerate(edits):
                    r=request(family,lit,mode,F(1,160),seed+j)
                    r['realized_correct']=r['action']==exact_actions[j] or 2*sum(truth[j])==N
                    if mode=='exact_proof_first':
                        stages=r.pop('stages');r['stage_count']=len(stages);r['final_three_stages']=stages[-3:]
                    requests.append(r)
                family.close();marginal=time.perf_counter_ns()-margin_start
                rows.append(dict(definition=definition,mode=mode,requests=requests,history_ns=family.history_ns,
                                 marginal_ns=marginal,total_ns=family.history_ns+marginal,counts=dict(family.counts)))
        result['status']='complete'
    except Exception:
        result.update(status='failed',failure=traceback.format_exc());raise
    finally:
        result.update(elapsed_ns=time.monotonic_ns()-start,end_utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='rows'},default=str))


if __name__=='__main__':main(Path(sys.argv[1]))
