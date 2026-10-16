"""DEVELOPMENT exact support-leakage amplification, Codex (GPT-6)."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse
import hashlib
import json


def coefficient(a,b,d):
    return sum((-1)**i*comb(a,i)*comb(b,d-i) for i in range(d+1) if i<=a and 0<=d-i<=b)


def case(index):
    n=(3,5,7,21,41,101)[index];d=(n-1)//2;size=2**(n-1)
    values={j:F(coefficient(j-1,n-j,d),size) for j in range(1,n+1,2)}
    L=sum((comb(n,j)*abs(v) for j,v in values.items()),F(0))
    assert sum((comb(n,j)*v for j,v in values.items()),F(0))==1
    # Independent central-coefficient formula, checked at every distance.
    for j,v in values.items():
        r=(j-1)//2
        assert v==F((-1)**r*comb(2*d,d)*comb(d,r),size*comb(2*d,2*r))
    epsilon=1/(2*(1+L));amplification=(1+L)/2
    assert epsilon*amplification==F(1,4)
    witness=None;moment_checks=0
    if n<=7:
        source=[x for x in range(2**n) if x.bit_count()%2==0];z=1
        chars=[s for s in range(2**n) if s.bit_count()<=d]
        kernel={x:F(sum((-1)**((s&(x^z)).bit_count()%2) for s in chars),size) for x in source}
        assert sum(kernel.values())==1 and sum(map(abs,kernel.values()))==L
        assert all(kernel[x]==values[(x^z).bit_count()] for x in source)
        P={x:epsilon*max(F(0),-v) for x,v in kernel.items()}
        P[z]=epsilon;P[0]+=1-sum(P.values())
        Q={x:P[x]+epsilon*kernel[x] for x in source}
        assert all(v>=0 for v in P.values()) and all(v>=0 for v in Q.values())
        assert sum(P.values())==sum(Q.values())==1
        for s in chars:
            a=sum((p*(-1)**((s&x).bit_count()%2) for x,p in P.items()),F(0))
            b=sum((p*(-1)**((s&x).bit_count()%2) for x,p in Q.items()),F(0))
            assert a==b;moment_checks+=1
        tv=sum((abs(P.get(x,F(0))-Q.get(x,F(0))) for x in set(P)|set(Q)),F(0))/2
        assert tv==F(1,4)
        witness={'outside_world':z,'P':{str(x):str(p) for x,p in P.items()},'Q':{str(x):str(p) for x,p in Q.items()},
                 'TV':str(tv),'outside_mass':str(epsilon),'kernel':{str(x):str(v) for x,v in kernel.items()}}
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'n':n,'cap':d+1,
      'kernel_l1':str(L),'amplification':str(amplification),'epsilon_for_TV_one_quarter':str(epsilon),
      'epsilon_decimal':float(epsilon),'distance_kernel':{str(j):str(v) for j,v in values.items()},
      'explicit_moment_checks':moment_checks,'witness':witness,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'scope':'Exact combinatorial formula; explicit distribution witnesses only for n<=7. No empirical prevalence or practical failure-rate claim.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','n','cap','kernel_l1','amplification','epsilon_for_TV_one_quarter','epsilon_decimal','explicit_moment_checks')}))
