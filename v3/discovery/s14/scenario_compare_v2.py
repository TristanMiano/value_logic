"""DEVELOPMENT: exact endpoint comparison, not a theorem reconstruction.

Codex (GPT-6). Garatti/Campi equation (5), beta=1/20, N=200.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import time

path=Path(__file__)
out=path.with_suffix('.json')
assert not out.exists()
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter_ns()
den=1_000_000
n=200

def sign_poly(u,k):
    a=den-u
    # Multiply equation (5) by 20*N*den**(N-k).
    return (sum(comb(m,k)*a**(m-k)*den**(n-m) for m in range(k,n))
            -20*n*comb(n,k)*a**(n-k))

def cdf_num(u,k):
    return sum(comb(n,j)*u**j*(den-u)**(n-j) for j in range(k+1))

def bracket(k,kind):
    lo,hi=0,den
    if kind=='scenario':
        yes=lambda u:sign_poly(u,k)>=0
    else:
        yes=lambda u:20*(k+1)*(k+2)*cdf_num(u,k)<=den**n
    while hi-lo>1:
        mid=(lo+hi)//2
        if yes(mid):hi=mid
        else:lo=mid
    assert not yes(lo) and yes(hi)
    return [str(F(lo,den)),str(F(hi,den))]

rows=[]
for k in (0,1,2,3,5,10,20,50,100,150,199):
    rows.append(dict(k=k,scenario=bracket(k,'scenario'),
                     binomial=bracket(k,'binomial')))

assert F(39,38)**197>=160
first_rank3_N=next(N for N in range(3,201) if F(39,38)**(N-3)>=160)
prices=(2,4,6)
initial_span=tuple(range(8))
refined_span=(0,4)
def first_bad(span):
    return min((price for j,price in enumerate(prices)
                if any((z>>j)&1 for z in span)),default=None)
assert first_bad(initial_span)==2 and first_bad(refined_span)==6
for z in refined_span:
    assert (z&3)==0
result=dict(status='PASS',attribution='Codex (GPT-6)',started_utc=started,
            ended_utc=datetime.now(timezone.utc).isoformat(),
            elapsed_ns=time.perf_counter_ns()-clock,
            source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            N=n,delta='1/20',risk_grid_denominator=den,rows=rows,
            scope_example=dict(initial_k_bar=3,refined_k_bar=1,
                               initial_first_bad_price=2,refined_first_bad_price=6,
                               initial_max_integer_budget=1,refined_max_integer_budget=5,
                               first_acceptance_at_rank3_N=first_rank3_N),
            scope='Exact rational endpoints and one worked scope witness only. '
                  'No empirical risk, acquisition cost, general optimum or prior-art novelty test.')
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
