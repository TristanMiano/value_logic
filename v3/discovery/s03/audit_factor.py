"""Exact affine prediction-powered audit factors; DEVELOPMENT specialization."""
from fractions import Fraction as F

def factor(b,p,r,lower,lam,m):
    assert all(isinstance(x,F) for x in (b,p,lower,lam,m))
    assert 0<=b<=1 and 0<=lower<=1 and 0<=m<=1 and lam>=0 and 1-lam*m>0
    assert type(r) is int and r in (0,1) and 0<=p<=1
    if p==0:
        assert b==0 and r==0
        return 1-lam*m
    assert p>=lam*b/(1+lam*(b-m))
    result=1+lam*(b+F(r)*(lower-b)/p-m)
    assert result>=0
    return result
