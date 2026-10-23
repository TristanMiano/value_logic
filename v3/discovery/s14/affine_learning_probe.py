"""Exact tiny-law screen for a sample-span adapter. Codex (GPT-6)."""
from datetime import datetime, timezone
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json
import platform
import random
import sys
import time

HERE=Path(__file__).resolve().parent
OUT=HERE/'affine_learning_probe.json'
assert not OUT.exists()
started=datetime.now(timezone.utc).isoformat();start=time.perf_counter_ns()
rng=random.Random(2026102226)
def parity(x):return x.bit_count()%2
def extend(S,x):return tuple(sorted(set(S)|{y^x for y in S}))
def span(rows):
    S=(0,)
    for x in rows:S=extend(S,x)
    return S
def tail(N,r,e):return sum((F(comb(N,j))*e**j*(1-e)**(N-j) for j in range(min(r-1,N)+1)),F(0))
def missing(S,p):return sum((v for x,v in enumerate(p) if x not in S),F(0))

law_checks=risk_inequalities=0
for r in range(1,5):
    for case in range(4):
        weights=[rng.randrange(5) for _ in range(1<<r)]
        if not sum(weights):weights[0]=1
        p=[F(w,sum(weights)) for w in weights]
        state={(0,):F(1)}
        for N in range(1,13):
            nxt={}
            for S,prob in state.items():
                for x,px in enumerate(p):
                    if px:
                        T=extend(S,x);nxt[T]=nxt.get(T,F(0))+prob*px
            state=nxt
            assert sum(state.values())==1
            expected=sum((prob*missing(S,p) for S,prob in state.items()),F(0))
            assert expected<=F(r,N+1)
            for e in (F(1,8),F(1,4),F(1,2),F(3,4)):
                exact=sum((prob for S,prob in state.items() if missing(S,p)>e),F(0))
                assert exact<=tail(N,r,e),(r,case,N,e,exact,tail(N,r,e))
                risk_inequalities+=1
            law_checks+=1

# Plugging retained rank into the fixed-dimension tail is invalid.
p=[F(0),F(1,3),F(1,3),F(1,3)]
assert all(missing(span([x]),p)==F(2,3) for x in (1,2,3))
assert tail(1,1,F(1,2))==F(1,2) # Actual event probability is one.

# Truthful partial linear measurements, including nonlinear choice of what to buy.
partial_panels=retained_rule_checks=0
for r in range(2,7):
    for case in range(20):
        truths=[rng.randrange(1<<r) for _ in range(4)]
        completions=[]
        for x in truths:
            rows=[rng.randrange(1,1<<r) for _ in range(rng.randrange(r+1))]
            Z=[y for y in range(1<<r) if all(parity(y&h)==parity(x&h) for h in rows)]
            assert x in Z
            completions.append(Z)
        S=span(y for Z in completions for y in Z)
        true_span=span(truths)
        assert set(true_span)<=set(S)
        retained=[h for h in range(1<<r) if all(not parity(h&y) for y in S)]
        assert {y for y in range(1<<r) if all(not parity(h&y) for h in retained)}==set(S)
        for h in retained:
            assert all(not parity(h&x) for x in truths)
            retained_rule_checks+=1
        partial_panels+=1

# A globally false model can yield useful trusted combinations.
Z=[x for x in range(16) if not parity(x&3) and not parity(x&12)]
S=span(Z)
retained=[h for h in range(16) if all(not parity(h&x) for x in S)]
assert S==(0,3,12,15) and retained==[0,3,12,15]
assert all(x!=0 for x in (3,15)) # The supplied zero-syndrome model always fails.
assert all(not parity(h&x) for h in retained for x in (3,15))

sample_requirements=[]
e=F(1,10);delta=F(1,20)
for r in (1,2,4,8):
    N=r
    while tail(N,r,e)>delta:N+=1
    sample_requirements.append(dict(fixed_dimension=r,epsilon=str(e),delta=str(delta),samples=N,tail=str(tail(N,r,e))))

result=dict(status='PASS',label='DEVELOPMENT exact finite laws; not an application learner benchmark',
            contributor='Codex (GPT-6)',started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),
            runtime_ns=time.perf_counter_ns()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            python=sys.version,platform=platform.platform(),law_sample_panels=law_checks,risk_inequalities=risk_inequalities,
            partial_receipt_panels=partial_panels,retained_rule_checks=retained_rule_checks,
            unsafe_rank_substitution=dict(actual_failure_probability='1',claimed_bound='1/2'),
            false_model_example=dict(actual_syndromes=[3,15],warrant_syndromes=list(S),retained_rows=retained),
            sample_requirements=sample_requirements)
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k!='sample_requirements'},indent=2))
print('Sample counts at epsilon=0.1, delta=0.05:',[(x['fixed_dimension'],x['samples']) for x in sample_requirements])
