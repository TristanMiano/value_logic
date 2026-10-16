"""Exact bounded-variable lower reconstruction on a common probability-free grid."""
from fractions import Fraction as F


def grid(value, denominator=2**40):
    v=F(float(value))*denominator+F(1,2)
    return F(v.numerator//v.denominator,denominator)


def lower_bound(eq,beq,ub,bub,bounds,c,raw_lambda,raw_nu):
    lam=[min(F(0),grid(v)) for v in raw_lambda]
    nu=[grid(v) for v in raw_nu]
    residual=list(c)
    for rows,multipliers in ((ub,lam),(eq,nu)):
        for row,v in zip(rows,multipliers):
            for j,a in row.items():residual[j]-=a*v
    base=sum((v*b for v,b in zip(lam,bub)),F(0))+sum((v*b for v,b in zip(nu,beq)),F(0))
    correction=sum((min(a*lo,a*hi) for a,(lo,hi) in zip(residual,bounds)),F(0))
    result=base+correction
    return result,{'lambda':list(map(str,lam)),'nu':list(map(str,nu)),
                   'base':str(base),'box_infimum_correction':str(correction),
                   'residual_l1':str(sum(map(abs,residual),F(0))),
                   'denominator':2**40,'bound':str(result),
                   'bound_bits':max(result.numerator.bit_length(),result.denominator.bit_length())}
