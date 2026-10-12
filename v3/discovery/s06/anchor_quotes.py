#!/usr/bin/env python3
"""Cheap, prior-free audit versus complete logical quotations from anchors.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. Quotations assume actual
admission of scalar lower anchors and feasible action masks. No native outcome
law or full economic price is supplied by these operations.
"""
from fractions import Fraction as F
import source_anchor


def best(masks,modes,possible,lowers,price,meter):
    choices=[dict(mask=mask,**source_anchor.bound(mask,modes,possible,lowers,price,meter)) for mask in list(masks)+[None]]
    return min(choices,key=lambda x:(x['bound'],x['mask'] is None,-1 if x['mask'] is None else x['mask']))


def audit_quote(masks,modes,possible,lowers,price,row,coordinate,meter):
    before=best(masks,modes,possible,lowers,price,meter)['bound']
    groups={}
    for h in possible[row]:
        groups.setdefault(modes[h][coordinate],[]).append(h)
    outcomes=[]
    for value,ids in sorted(groups.items()):
        after=[list(v) for v in possible]; after[row]=ids
        response=best(masks,modes,after,lowers,price,meter)
        outcomes.append(dict(value=value,remaining_modes=ids,response=response))
    worst=max(x['response']['bound'] for x in outcomes)
    meter.pay('audit_quote','declared_partition_and_complete_outcome_maximum',2*len(possible[row])+len(outcomes)+4)
    return dict(row=row,coordinate=coordinate,before=before,worst_bound=worst,
                guaranteed_gain=before-worst,outcomes=outcomes,
                contract='One exact source-bound cell observation with one of all declared outcomes; external price unassigned')


def logical_quote(masks,modes,possible,lowers,price,q,budget,meter,complete=False):
    """Two possible checked results, plus a no-progress outcome unless complete.

    A complete call needs a separately admitted finite-provider resource
    contract. This flag is a conditional quotation premise, not a proof that a
    capped native solve is complete. The caller must carry its supported quote.
    """
    n=len(possible);m=len(modes[0]);price=F(price)
    if len(q)!=m or any(type(w) is not int or w<0 for w in q) or type(budget) is not int:
        raise ValueError('Same ordered nonnegative integer query objective required')
    before=best(masks,modes,possible,lowers,price,meter)['bound']
    hi=[sum(max(modes[h][j] for h in row) for row in possible) for j in range(m)]
    alpha=sum(max(0,w-v) for w,v in zip(hi,q))
    common_lower=sum(min(F(lowers[h])/n for h in row) for row in possible)
    positive=min(before,max(F(0),min(price,F(budget+alpha))-min(price,common_lower)))
    negatives=[]
    for h,mode in enumerate(modes):
        anchor=[n*w for w in mode]
        loss=sum(max(0,x-y) for x,y in zip(q,anchor))
        negatives.append(max(F(lowers[h]),F(budget+1-loss),F(0)))
    negative=min(before,best(masks,modes,possible,negatives,price,meter)['bound'])
    worst=max(positive,negative) if complete else before
    meter.pay('logical_quote','coordinate_enclosure_and_scalar_cut_transport',
              3*m*sum(len(row) for row in possible)+3*m*len(modes)+12)
    return dict(weights=q,budget=budget,before=before,SAT_uniform_cost_upper=budget+alpha,
                positive_box_margin=alpha,current_uniform_lower=common_lower,
                SAT_bound=positive,UNSAT_anchor_lowers=negatives,UNSAT_bound=negative,
                no_progress_outcome=not complete,worst_bound=worst,guaranteed_gain=before-worst,
                premise='Two checked outcomes only under an admitted complete-call contract; otherwise unresolved preserves the old bound')
