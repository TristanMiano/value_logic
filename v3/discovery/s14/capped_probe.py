"""Capped response development screen; Codex (GPT-6). Float optimization, exact inputs."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import random
import time

out=Path(__file__).with_suffix('.json')
assert not out.exists()
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter_ns()

def uncapped(s,e):
    a=(math.sqrt(e*e+4)+e)/2
    sp=a*a/(1+a*a)
    return s/(a*a) if s<=sp else 1/(1+(math.sqrt((1-s)/s)+e)**2)

def endpoint(s,K,e):
    assert 1/(1+K*K)-1e-12<=s<=1+1e-12
    if e==0:
        return s,'unchanged',None
    if s>=1-1e-14:
        return 1/(1+e*e),'one',None
    a=(math.sqrt(e*e+4)+e)/2
    sp=a*a/(1+a*a)
    sc=(1+a*a)/(K*K+2+a*a)
    if s>=sp:
        return uncapped(s,e),'scalar',None
    if s>=sc:
        return s/(a*a),'linear',None
    c=math.sqrt((1-s)*(1+K*K))
    hi=math.sqrt((1-s)/(1+K*K))
    lo=0.0
    for _ in range(85):
        t=(lo+hi)/2
        r=math.sqrt(max(0,1-2*c*t+K*K*t*t))
        z=r-e*t
        derivative=2*t if z<=0 else 2*z*((K*K*t-c)/r-e)+2*t
        if derivative>0:
            hi=t
        else:
            lo=t
    t=(lo+hi)/2
    r=math.sqrt(max(0,1-2*c*t+K*K*t*t))
    return max(0,r-e*t)**2+t*t,'capped',t

def value_col(c):
    return (1+c[1]*c[1])/(1+c[0]*c[0]+c[1]*c[1])

def value_matrix(M):
    a=1+sum(x*x for x in M[0])
    b=sum(x*y for x,y in zip(*M))
    d=1+sum(x*x for x in M[1])
    return d/(a*d-b*b)

branches={}
attainments=0
worst_error=0.0
for K in (.2,.5,1,2,4,10):
    l=1/(1+K*K)
    for weight in (0,.01,.1,.5,.9):
        s=l+weight*(1-l)
        for e in (.1,.5,1,3):
            lower,branch,t=endpoint(s,K,e)
            branches[branch]=branches.get(branch,0)+1
            a=(math.sqrt(e*e+4)+e)/2
            if branch=='capped':
                c=math.sqrt((1-s)*(1+K*K))
                M=[c,math.sqrt(max(0,K*K-c*c))]
                residual=[1-t*M[0],-t*M[1]]
                norm=math.hypot(*residual)
                assert norm>e*t-1e-12
                N=[m+e*z/norm for m,z in zip(M,residual)]
            elif branch=='scalar':
                M=[math.sqrt((1-s)/s),0]
                N=[M[0]+e,0]
            else:
                target=s/(a*a)
                m=s*s/(s+target)
                w=[s,math.sqrt(max(0,m-s*s))]
                z=math.sqrt(s*target/(s+target))
                M=[(1-w[0])/z,-w[1]/z]
                N=[(1-target*w[0]/s)/z,-target*w[1]/(s*z)]
            assert math.hypot(*M)<=K+1e-10
            assert math.hypot(*(n-m for m,n in zip(M,N)))<=e+1e-10
            err=max(abs(value_col(M)-s),abs(value_col(N)-lower))
            assert err<2e-10
            assert lower>=uncapped(s,e)-2e-12
            worst_error=max(worst_error,err)
            attainments+=1

rng=random.Random(20261022)
actual_checks=0
residual_checks=0
for _ in range(60):
    M=[[Q(rng.randint(-8,8),3) for _ in range(2)] for _ in range(2)]
    K=max(1,math.ceil(math.sqrt(float(sum(x*x for row in M for x in row)))))
    s=value_matrix(M)
    for e in (Q(1,10),Q(1,2),Q(1),Q(2)):
        H=[[e*Q(3,5),Q(0)],[e*Q(4,5),Q(0)]]
        N=[[M[i][j]+H[i][j] for j in range(2)] for i in range(2)]
        target=value_matrix(N)
        lower,_,_=endpoint(float(s),K,float(e))
        assert lower<=float(target)+1e-11
        actual_checks+=1
    for _ in range(4):
        z=[Q(rng.randint(-8,8),5) for _ in range(2)]
        norm=math.sqrt(float(sum(t*t for t in z)))
        residual=float(sum(((1 if i==0 else 0)-sum(M[i][j]*z[j] for j in range(2)))**2 for i in range(2)))
        sf=float(s)
        if sf==1:
            smallest=1.0
        else:
            tk=math.sqrt((1-sf)/(1+K*K))
            t0=math.sqrt(sf*(1-sf))
            x=math.sqrt((1-sf)/sf)
            if norm<=tk:
                smallest=1-2*math.sqrt((1-sf)*(1+K*K))*norm+K*K*norm*norm
            elif norm<=t0:
                smallest=sf-norm*norm
            elif norm<=1/x:
                smallest=(1-x*norm)**2
            else:
                smallest=0.0
        assert residual>=smallest-1e-11
        residual_checks+=1

examples=[]
for K in (3,4,5,6,10):
    lower,branch,t=endpoint(.1,K,1)
    examples.append({'s':.1,'K':K,'edit':1,'lower':lower,'branch':branch,
                     'uncapped_lower':uncapped(.1,1),'minimizing_t':t,
                     'relative_bound_increase_percent':100*(lower/uncapped(.1,1)-1)})
result={'status':'PASS','contributor':'Codex (GPT-6)',
        'scope':'floating scalar optimization and extremizers; exact rational input matrices',
        'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),
        'attainments':attainments,'branches':branches,'max_attainment_error':worst_error,
        'actual_matrix_checks':actual_checks,'residual_curve_checks':residual_checks,
        'examples':examples,'rigorous_outward_solver':False,'complete_cost_or_cpu_gain':False,
        'elapsed_ns':time.perf_counter_ns()-clock,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
