"""DEVELOPMENT: rational identities, exhaustive small decoding, finite bill DP.
Budget: caps<=20 for identities, n<=8 decoding, n<=100 DP; expected <10s.
No native runtime gain or complete-cost theorem is tested. Codex (GPT-6).
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent
begun=time.perf_counter_ns()
counts=dict(rate_identities=0,decoded_worlds=0,decoded_episodes=0,mean_checks=0)

def shapes(h):
    return [(r,d) for r in range(h-1) for d in range(1,h-r)]

def coefficient(h,f):
    options=[]
    for r in range(h-1):
        d=h-1-r
        a=F(r,2)+1-F(1,2**d)
        b=r+2-F(1,2**d)
        options.append(((b+f)/(2*a),r,d,a,b))
    beta,r,d,_,_=min(options)
    rho=1/(2*beta)
    relax=-rho
    for _ in range(2,h+1):relax=F(1,2)-rho+max(relax/2,relax)
    assert relax==rho*f
    assert relax==max(a-rho*b for _,_,_,a,b in options)
    return beta,(r,d)

for h in range(2,21):
    for f in map(F,[0,F(1,16),F(1,6),F(1,4),F(1,2),1,2,8]):
        coefficient(h,f);counts['rate_identities']+=1

def episode(x,remaining,r,d,n):
    used=remaining[:r+d]
    prelude=0
    for i in used[:r]:prelude^=x>>i&1
    for j,i in enumerate(used[r:],1):
        bit=(x>>i&1)^(prelude if j==1 else 0)
        if bit==0:
            bill=r+j
            break
    else:
        marker=next(i for i in range(n) if i not in used)
        _private_discarded=x>>marker&1
        bill=r+d+1
    # Public decoding uses only the known r,d and observed invoice.
    if bill==r+d+1:resolved=r+d;value=d&1
    else:resolved=bill;value=(bill-r-1)&1
    actual=0
    for i in remaining[:resolved]:actual^=x>>i&1
    assert value==actual
    counts['decoded_episodes']+=1
    return bill,resolved,value

def outcomes(r,d,f,g=F(0)):
    answer=[]
    for j in range(1,d+1):answer.append((F(1,2**j),r+j,r+j+f+r*g))
    answer.append((F(1,2**d),r+d,r+d+1+f+r*g))
    assert sum(p for p,_,_ in answer)==1
    return answer

def fixed_value(n,r,d,f):
    @lru_cache(None)
    def v(k):
        if not k:return F(0)
        rr,dd=(r,d) if k>=r+d else (0,1)
        return sum(p*(c+v(k-l)) for p,l,c in outcomes(rr,dd,f))
    return v(n)

for n in range(2,9):
    for h in range(2,min(n,5)+1):
        for r,d in shapes(h):
            f=F(1,2)
            total=F(0)
            for x in range(1<<n):
                remaining=list(range(n));public_parity=0;bill=F(0)
                while remaining:
                    rr,dd=(r,d) if len(remaining)>=r+d else (0,1)
                    c,l,value=episode(x,remaining,rr,dd,n)
                    remaining=remaining[l:];public_parity^=value;bill+=c+f
                assert public_parity==x.bit_count()%2
                total+=bill;counts['decoded_worlds']+=1
            assert total/(1<<n)==fixed_value(n,r,d,f)
            counts['mean_checks']+=1

def dp(n,h,f,full,g=F(0)):
    values=[F(0)];choices=[None];options=0
    for k in range(1,n+1):
        scored=[]
        for r,d in shapes(h):
            if r+d>k or (not full and r and d>1):continue
            score=sum(p*(c+values[k-l]) for p,l,c in outcomes(r,d,f,g))
            scored.append((score,r,d));options+=1
        score,r,d=min(scored);values.append(score);choices.append((r,d))
    return values[n],choices[n],options

panels=[]
for h in (3,4,5,6):
    for f in map(F,[0,F(1,4),F(1,2),1,2]):
        old,old_first,old_count=dp(100,h,f,False)
        new,new_first,new_count=dp(100,h,f,True)
        beta,shape=coefficient(h,f)
        assert new>=100*beta
        r,d=shape
        upper=fixed_value(100,r,d,f)
        assert upper<=100*beta+(h-2)*(F(3,2)+f-beta)
        assert new<=upper and new<=old
        panels.append(dict(n=100,cap=h,reset=str(f),old_menu_fee=str(old),new_menu_fee=str(new),
                           old_float=float(old),new_float=float(new),reduction=float((old-new)/old),
                           old_first=old_first,new_first=new_first,old_options=old_count,
                           new_options=new_count,optimal_rate=str(beta),rate_shape=shape,
                           lower_bound=str(100*beta)))

tariffs=[]
for g in (F(0),F(1,10),F(1,7),F(1,5)):
    old,_,_=dp(100,4,F(1,2),False,g)
    new,first,_=dp(100,4,F(1,2),True,g)
    tariffs.append(dict(private_parity_xor_fee=str(g),old_fee=str(old),new_fee=str(new),
                        reduction=float((old-new)/old),new_first=first,
                        scope='constructed r*gamma price only; no all-program optimality with this tariff'))

result=dict(status='PASS',contributor='Codex (GPT-6)',counts=counts,panels=panels,
            parity_tariff_panels=tariffs,elapsed_ns=time.perf_counter_ns()-begun,
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            scope='exact constructed bills and finite identities/decoding; same-model; no empirical or full-cost gain')
(HERE/'rate_probe.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status=result['status'],counts=counts,elapsed_ns=result['elapsed_ns'],
                     headline=next(p for p in panels if p['cap']==4 and p['reset']=='1/2'),
                     parity_tariffs=tariffs)))
