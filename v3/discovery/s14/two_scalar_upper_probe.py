"""Small upper-envelope construction screen, DEVELOPMENT, Codex (GPT-6)."""
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import platform
import sys
import time

HERE=Path(__file__).resolve().parent
OUT=HERE/'two_scalar_upper_probe.json'
assert not OUT.exists()
started=datetime.now(timezone.utc).isoformat()
start=time.perf_counter_ns()

def response(column):return 1-column[0]**2/(1+sum(x*x for x in column))

exact=[]
for e in (F(1,2),F(3,4),F(1),F(2)):
    for c,d in ((F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(4,5),F(3,5))):
        x=(e+1/e)/c
        M=[x,F(0)]
        N=[x-e*c,-e*d]
        assert sum((a-b)**2 for a,b in zip(M,N))==e*e
        s=response(M)
        assert s==1/(1+x*x)
        expected=(1+e*e)/(x*x)
        assert response(N)==expected
        scalar=1/(1+(x-e)**2)
        assert expected>scalar
        exact.append(dict(e=e,x=x,s=s,m=s*s,new_response=expected,scalar_only=scalar,M=M,N=N))

def J(alpha,s,m,e):
    q=math.sqrt(s-m)
    rad=max(0.,1-2*alpha*(1-s)+alpha*alpha*(1-2*s+m))
    return (math.sqrt(rad)+alpha*e*q)**2+alpha*alpha*q*q

def deriv(alpha,s,m,e):
    q=math.sqrt(s-m)
    b=1-2*s+m
    r=math.sqrt(1-2*alpha*(1-s)+alpha*alpha*b)
    return 2*(r+alpha*e*q)*((alpha*b-(1-s))/r+e*q)+2*alpha*q*q

general=[]
max_error=0.
for s in (.1,.25,.5,.8):
    for mix in (.2,.6):
        m=s*s+mix*(s-s*s)
        q=math.sqrt(s-m)
        M=[(1-s)/q,-math.sqrt(m-s*s)/q]
        assert abs(response(M)-s)<1e-13
        # Recover the old resolvent vector without a numerical matrix inverse.
        w=[1-M[0]*M[0]/(1+sum(x*x for x in M)),
           -M[1]*M[0]/(1+sum(x*x for x in M))]
        assert abs(sum(x*x for x in w)-m)<1e-13
        for e in (0.,.1,.5,1.,3.):
            if e>=(1-s)/q:
                alpha=0.
                N=[0.,M[1]]
            else:
                lo,hi=0.,1/q
                assert deriv(lo,s,m,e)<0 and deriv(hi,s,m,e)>0
                for _ in range(70):
                    mid=(lo+hi)/2
                    if deriv(mid,s,m,e)<0:lo=mid
                    else:hi=mid
                alpha=(lo+hi)/2
                residual=[1-alpha*q*M[0],-alpha*q*M[1]]
                rn=math.hypot(*residual)
                N=[M[i]-e*residual[i]/rn for i in range(2)]
            expected=J(alpha,s,m,e)
            actual=response(N)
            error=abs(actual-expected)
            max_error=max(max_error,error)
            assert error<2e-12,(s,m,e,alpha,actual,expected)
            assert math.dist(M,N)<=e+2e-12
            # Bracket probes are a finite numerical supplement to convexity proof.
            for a in (0.,alpha/2,alpha,alpha*1.5,1/q):
                assert J(a,s,m,e)>=expected-2e-12
            general.append(dict(s=s,m=m,e=e,alpha=alpha,upper=expected,attained=actual,error=error))

result=dict(status='PASS',label='DEVELOPMENT exact rotational cases plus floating constructive checks',
            contributor='Codex (GPT-6)',started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),
            runtime_ns=time.perf_counter_ns()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            python=sys.version,platform=platform.platform(),exact_rotational_cases=exact,
            numerical_general_cases=general,maximum_attainment_error=max_error)
OUT.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('exact_rotational_cases','numerical_general_cases')},indent=2))
print('Exact rotational cases:',len(exact),'Numerical general cases:',len(general))
