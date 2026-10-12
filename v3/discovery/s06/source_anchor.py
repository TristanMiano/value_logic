#!/usr/bin/env python3
"""Uniform repair certificates from scalar anchors and partial row observations.

ChatGPT (GPT-6 Astra Pro), DEVELOPMENT, 2026-10-12. An internal admitted-data
interface: ell[k] must be independently warranted at weights N*modes[k], on
this same logical source and ordered objective. A serialized number/flag is
not admission. No hull-generator or Boolean objective-mask enumeration.
"""
from fractions import Fraction as F


def bound(mask,modes,possible,anchor_lowers,price,meter):
    if not possible or not modes or len(modes)!=len(anchor_lowers):
        raise ValueError('Nonempty common finite cohort and one admitted bound per anchor required')
    n=len(possible); m=len(modes[0]); price=F(price)
    if any(len(v)!=m or any(F(w)<0 for w in v) for v in modes):
        raise ValueError('Same ordered nonnegative cost features required')
    if mask is not None and (type(mask) is not int or not 0<=mask<(1<<m)):
        raise ValueError('Checked Boolean action mask or replacement required')
    lower=[F(x)/n for x in anchor_lowers]
    unit_cost=[F(0) if mask is None else sum(F(w) for j,w in enumerate(v) if mask&(1<<j)) for v in modes]
    meter.pay('source_anchor_compile','mode_action_costs_and_lower_scaling',2*m*len(modes)+len(modes))
    contrasts=[];upper=[]
    for choices in possible:
        if not choices or any(type(k) is not int or not 0<=k<len(modes) for k in choices):
            raise ValueError('Every observed row needs a nonempty admitted mode set')
        if mask is None:
            contrasts.append(-min(lower[k] for k in choices))
        else:
            contrasts.append(max(unit_cost[k]-lower[k] for k in choices))
            upper.append(max(unit_cost[k] for k in choices))
        meter.pay('source_anchor_query','row_mode_contrast_extrema',3*len(choices)+2)
    gap=(price if mask is None else F(0))+sum(contrasts,F(0))
    price_gap=F(0) if mask is None else sum(upper,F(0))-price
    result=max(F(0),gap,price_gap)
    meter.pay('source_anchor_query','cohort_sums_and_clipped_regret',len(contrasts)+len(upper)+5)
    return dict(bound=result,repair_gap=gap,replacement_gap=price_gap,mode_anchor_lowers=list(map(F,anchor_lowers)),
                domain='All compatible partial-row configurations and their convex hull, for this fixed checked action',
                method='Concavity/homogeneity transports each scalar anchor lower by one over cohort size')
