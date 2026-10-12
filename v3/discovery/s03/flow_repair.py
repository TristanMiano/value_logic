"""Checked finite-graph witness repair; semantic version relation is external."""
from fractions import Fraction as F
from flow_v2 import check


def repair(old_terms,old_prices,allocation,terms,prices,fill=False):
    assert len(old_terms)==len(terms) and len(old_prices)==len(prices)
    old=check(old_terms,old_prices,allocation)
    assert all(isinstance(r,F) and r>=0 and 0<=m<1<<len(prices) for m,r in terms)
    assert all(isinstance(q,F) and q>=0 for q in prices)
    row_left=[r for _,r in terms];col_left=list(prices);kept={};removed=F(0);row_loss=F(0);col_loss=F(0)
    for e,i,amount in allocation:
        if not terms[e][0]&(1<<i):removed+=amount;continue
        row_amount=min(amount,row_left[e]);row_left[e]-=row_amount;row_loss+=amount-row_amount
        final=min(row_amount,col_left[i]);col_left[i]-=final;col_loss+=row_amount-final
        # Releasing a column-trimmed amount cannot create a row overflow.
        row_left[e]+=row_amount-final
        if final:kept[e,i]=final
    coarse=old['upper']+sum(max(r-old_r,F(0)) for (_,old_r),(_,r) in zip(old_terms,terms))+sum(max(a-b,F(0)) for a,b in zip(old_prices,prices))+removed
    trimmed=check(terms,prices,[(e,i,a) for (e,i),a in kept.items()])
    assert trimmed['upper']<=coarse
    added=F(0)
    if fill:
        for e,(mask,_) in enumerate(terms):
            while row_left[e] and mask:
                bit=mask&-mask;i=bit.bit_length()-1;mask^=bit;amount=min(row_left[e],col_left[i])
                if amount:kept[e,i]=kept.get((e,i),F(0))+amount;row_left[e]-=amount;col_left[i]-=amount;added+=amount
    out=[(e,i,a) for (e,i),a in kept.items()];bound=check(terms,prices,out)
    assert bound['upper']<=trimmed['upper']<=coarse
    return out,dict(bound=bound,transport_upper=coarse,trimmed_upper=trimmed['upper'],removed_incidence_mass=removed,row_trim=row_loss,column_trim=col_loss,local_fill=added)
