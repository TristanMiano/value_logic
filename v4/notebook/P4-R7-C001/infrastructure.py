"""W7.1. Common-garden and transplantation tests for inherited infrastructure."""
from collections import Counter, deque
from fractions import Fraction as F
from math import exp, log, sqrt
from random import Random


def logistic(z):
    return 1/(1+exp(-z))


def logit(x):
    return log(x/(1-x))


def teaching(x,z):
    # Two independently nominated teachers must be the same person. If a
    # service has no teacher, all referrals go to the existing service.
    if x in (0,1):
        return 3/16+5/8*x
    demand=logistic(z)
    a=demand*demand/x
    b=(1-demand)**2/(1-x)
    return 3/16+5/8*a/(a+b)


def carry(x,z):
    return .5*z+.75*logit(x)


def analytic():
    slope=F(5,8)*F(9,100)/F(3,16)
    trace=-slope+F(1,2)
    det=-slope*F(1,2)-2*slope*F(3,4)
    assert slope==F(3,10) and trace==F(1,5) and det==-F(3,5)
    assert 1-trace+det>0 and 1+trace+det>0 and 1-det>0
    ell=log(3)
    for a in (-1,1):
        x=logistic(a*ell)
        for z,flip in ((1.5*a*ell,1),(-.5*a*ell,-1)):
            assert abs(logit(teaching(x,z))-flip*a*ell)<1e-12
            assert abs(carry(x,z)-flip*z)<1e-12
    for name,z in (("fixed",1.5*ell),("alternating",-.5*ell)):
        print(name,"demand",round(logistic(z),6),"next cohort",round(teaching(.75,z),6),
              "clients served",round(1-abs(.75-logistic(z)),6))
    print("spectral radii per step at either class",
          max(abs((float(trace)+s*sqrt(float(trace**2-4*det)))/2) for s in (-1,1)))


def draw_binomial(rng,n,p):
    if hasattr(rng,"binomialvariate"):
        return rng.binomialvariate(n,p)
    return sum(rng.random()<p for _ in range(n))


def pattern(signs):
    if all(x==1 for x in signs):
        return "positive"
    if all(x==-1 for x in signs):
        return "negative"
    if all(x!=0 for x in signs) and all(a!=b for a,b in zip(signs,list(signs)[1:])):
        return "alternating"
    return "other"


def finite(n,z_start,runs,horizons,seed):
    rng=Random(seed)
    results={t:Counter() for t in horizons}
    for _ in range(runs):
        count,z=3*n//4,z_start
        signs=deque(maxlen=8)
        for t in range(1,max(horizons)+1):
            x=count/n
            p=teaching(x,z)
            z=carry((count+.5)/(n+1),z)
            count=draw_binomial(rng,n,p)
            signs.append((count*2>n)-(count*2<n))
            if t in results:
                results[t][pattern(signs)]+=1
                results[t]["service"]+=1-abs(count/n-logistic(z))
    return results


def main():
    analytic()
    for n in (64,256,1024):
        for name,z in (("fixed",1.5*log(3)),("alternating",-.5*log(3))):
            runs=1000
            for t,row in finite(n,z,runs,(32,128),71000+n).items():
                print(n,name,t,"positive / negative / alternating / other",
                      *(row[k] for k in ("positive","negative","alternating","other")),
                      "mean service",round(row["service"]/runs,4))


if __name__=="__main__":
    main()
