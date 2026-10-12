"""Normalized product forecasts mixed with uniform finite affine reports."""
from fractions import Fraction as F
from affine_source import compile_source,eliminate,parity

def prepare(matrix,b,n,probabilities,eta):
    assert isinstance(eta,F) and 0<=eta<1
    compiled=compile_source(matrix,n,[],set(range(n)),eliminate(matrix,n))
    assert compiled['revise'](b) is not None,'empty source'
    h=len(compiled['free']);probs=tuple(probabilities)
    assert len(probs)==h and all(isinstance(p,F) and 0<=p<=1 for p in probs)
    frozen_matrix=tuple(matrix);free=compiled['free'];uniform=F(1,1<<h)
    def mass(x):
        assert type(x) is int and 0<=x<1<<n
        if any(parity(row&x)!=((b>>i)&1) for i,row in enumerate(frozen_matrix)):return F(0)
        model=F(1)
        for p,j in zip(probs,free):model*=p if x>>j&1 else 1-p
        return (1-eta)*uniform+eta*model
    def partial(known,bits):
        assert type(known) is int and type(bits) is int and 0<=known<1<<h and bits&~known==0
        lo=hi=model_event=F(1)
        for j,p in enumerate(probs):
            if known>>j&1:
                value=p if bits>>j&1 else 1-p;lo*=value;hi*=value;model_event*=value
            else:lo*=min(p,1-p);hi*=max(p,1-p)
        event=(1-eta)*F(1,1<<known.bit_count())+eta*model_event
        return dict(lower=(1-eta)*uniform+eta*lo,upper=(1-eta)*uniform+eta*hi,
            event_mass=event,conditional_model_weight=eta*model_event/event)
    return dict(free=free,uniform=uniform,point_floor=(1-eta)*uniform,mass=mass,partial=partial)
