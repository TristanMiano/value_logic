"""Outward dyadic logs and certified support queries; DEVELOPMENT, Codex GPT-6.

Advice is ordinary scalar convex dual search, never a trusted source.
Existing bank_bounds.py and its exposures are unchanged.
"""
from fractions import Fraction as F
import math
from bank_bounds import log_interval


def ceil_dyadic(x,bits=40):
    d=1<<bits
    return F(-((-x.numerator*d)//x.denominator),d)


def log_upper(x,bits=40):return ceil_dyadic(log_interval(x)[1],bits)


def certificate(sums,t,Q,P,lam,alpha,bits=40):
    assert type(t) is int and t>0 and len(sums)==len(Q)==len(P)
    assert all(isinstance(x,F) for x in list(sums)+list(Q)+list(P)+[lam,alpha])
    assert all(0<=s<=t for s in sums) and all(q>=0 for q in Q) and all(p>0 for p in P)
    assert sum(Q)==sum(P)==1 and lam>0 and 0<alpha<1
    kl=sum(q*log_upper(q/p,bits) for q,p in zip(Q,P) if q)
    v=sum(q*s for q,s in zip(Q,sums))/t-(kl+log_upper(1/alpha,bits))/(lam*t)-lam/8
    return max(F(0),v)


def posterior(weights,den=1<<24):
    total=sum(weights);raw=[x*den/total for x in weights];counts=[int(x) for x in raw]
    rem=den-sum(counts);assert 0<=rem<=len(counts)
    for i in sorted(range(len(counts)),key=lambda i:(-(raw[i]-counts[i]),i))[:rem]:counts[i]+=1
    return tuple(F(c,den) for c in counts)


def logsumexp(logits):
    x=max(logits)
    return x+math.log(sum(math.exp(y-x) for y in logits))


def advise(sums,t,P,lam,alpha,w):
    eta=float(lam*t);loga=[math.log(float(p))+float(lam*s) for p,s in zip(P,sums)]
    logc=float(lam*lam*t/8)+math.log(float(1/alpha))
    positive=[i for i,v in enumerate(w) if v>0]
    end=[loga[i]-(0 if w[i]>0 else eta) for i in range(len(w))]
    if not positive or logsumexp(end)<=logc:return F(0),tuple(P),{'constraint_active':False}
    offsets={i:math.log(eta)+loga[i]-math.log(float(w[i])) for i in positive}
    def state(r):
        mu=[min(1.,max(0.,(r+offsets[i])/eta)) if i in offsets else 1. for i in range(len(w))]
        logs=[a-eta*x for a,x in zip(loga,mu)]
        return mu,logs,logsumexp(logs)
    low=min(-offsets[i] for i in positive)-1
    high=max(eta-offsets[i] for i in positive)+1
    assert state(low)[2]>logc and state(high)[2]<logc
    for _ in range(80):
        mid=(low+high)/2
        if state(mid)[2]>logc:low=mid
        else:high=mid
    r=(low+high)/2;mu,logs,lse=state(r);scale=max(logs)
    Q=posterior([math.exp(v-scale) for v in logs])
    B=F(round(math.exp(r+math.log(eta)+logc)*(1<<24)),1<<24)
    return B,Q,{'constraint_active':True,'numerical_primal':sum(float(a)*b for a,b in zip(w,mu)),
                'numerical_constraint_residual':lse-logc,'numerical_means':mu}


def check_query(sums,t,P,lam,alpha,w,B,Q):
    assert len(w)==len(P) and all(isinstance(x,F) for x in w) and isinstance(B,F) and B>=0
    L=certificate(sums,t,Q,P,lam,alpha)
    return B*L+sum(min(a-B*q,F(0)) for a,q in zip(w,Q))


def support(sums,t,P,lam,alpha,w):
    B,Q,diagnostic=advise(sums,t,P,lam,alpha,w)
    choices=[('box',sum(min(x,F(0)) for x in w)),('advised',check_query(sums,t,P,lam,alpha,w,B,Q))]
    mass=sum(max(x,F(0)) for x in w)
    if mass:
        direct=tuple(max(x,F(0))/mass for x in w)
        choices.append(('positive_part',check_query(sums,t,P,lam,alpha,w,mass,direct)))
    kind,lower=max(choices,key=lambda kv:kv[1])
    return dict(lower=lower,selected=kind,B=B,Q=Q,diagnostic=diagnostic,alternatives=dict(choices))
