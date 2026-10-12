"""Uniform unresolved-bit forecast only; exact sparse batch VOI, Codex GPT-6."""
from fractions import Fraction as F
from acquire_flow import solve


def coordinates(masks):
    rows={};result={}
    for mask in masks:
        value=mask;tag=0
        while value:
            pivot=value.bit_length()-1
            if pivot in rows:
                row,code=rows[pivot];value^=row;tag^=code
            else:
                code=1<<len(rows);rows[pivot]=(value,code);tag^=code;break
        result[mask]=tag
    return result,len(rows)


def expected_absolute(poly):
    nonzero=[mask for mask,a in poly.items() if mask and a]
    codes,rank=coordinates(nonzero)
    total=F(0)
    for world in range(1<<rank):
        value=poly.get(0,F(0))+sum(poly[mask]*(-1 if (world&code).bit_count()%2 else 1) for mask,code in codes.items())
        total+=abs(value)
    return total/(1<<rank),rank


def evsi(poly,bits):
    reduced={mask:a for mask,a in poly.items() if mask&bits==mask}
    value,rank=expected_absolute(reduced)
    return (value-abs(poly.get(0,F(0))))/2,rank


def plan(poly,prices):
    assert all(isinstance(a,F) for a in poly.values()) and all(isinstance(q,F) and q>=0 for q in prices)
    assert all(0<=mask<1<<len(prices) for mask in poly)
    masks=[mask for mask,a in poly.items() if mask and a]
    upper=solve([(mask,abs(poly[mask])/2) for mask in masks],prices)
    sign_fixed=abs(poly.get(0,F(0)))>=sum(abs(poly[m]) for m in masks)
    if sign_fixed or upper['objective']==0:
        return dict(bits=0,net=F(0),evsi=F(0),price=F(0),batches_evaluated=0,max_rank=0,
                    certificate_upper=upper['objective'],sign_fixed=sign_fixed)
    unions={0}
    for mask in masks:unions|={u|mask for u in unions}
    best=(F(0),0,F(0),F(0));max_rank=0
    for bits in sorted(unions):
        benefit,rank=evsi(poly,bits);price=sum(q for i,q in enumerate(prices) if bits&(1<<i));net=benefit-price
        max_rank=max(rank,max_rank)
        if net>best[0]:best=net,bits,benefit,price
    assert best[0]<=upper['objective']
    return dict(bits=best[1],net=best[0],evsi=best[2],price=best[3],batches_evaluated=len(unions),max_rank=max_rank,
                certificate_upper=upper['objective'],sign_fixed=False)
