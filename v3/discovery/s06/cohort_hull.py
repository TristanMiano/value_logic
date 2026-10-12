#!/usr/bin/env python3
"""Paid finite generators for an exact common cohort weight hull.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. No hidden modes are read.
Rows retain distinct observation identities even when hull work is grouped.
"""
from collections import defaultdict
from itertools import product


def generators(modes,possible,meter,max_generators=256):
    if not modes or not possible or type(max_generators) is not int or max_generators<1:
        raise ValueError('Nonempty modes, cohort and positive construction cap required')
    m=len(modes[0])
    if any(len(v)!=m or any(type(w) is not int or w<0 for w in v) for v in modes):
        raise ValueError('Same ordered integral nonnegative objective coordinates required')
    groups=defaultdict(list)
    for row,choices in enumerate(possible):
        key=tuple(sorted(set(choices)))
        if not key or any(type(k) is not int or not 0<=k<len(modes) for k in key):
            raise ValueError('Every fixed cost row needs a nonempty admitted mode set')
        groups[key].append(row)
        meter.pay('hull_group','admit_mode_ids_and_group_rows',len(choices)+4)
    rows=[dict(allowed_modes=list(k),members=v,count=len(v)) for k,v in sorted(groups.items())]
    count=1
    for g in rows:
        count*=len(g['allowed_modes'])
        meter.pay('hull_quote','generator_count_product',2)
    report=dict(groups=rows,group_product_size=count,cap=max_generators,
                domain='Cohort sums, not means. Exact hull of all compatible fixed-row configurations; no stochastic independence.',
                construction='Sum over groups count_g * conv(public_modes allowed to group g)')
    if count>max_generators:
        return report|dict(status='unresolved',reason='Generator construction cap',vertices=None)
    unique={}
    for choices in product(*(g['allowed_modes'] for g in rows)):
        point=tuple(sum(g['count']*modes[k][j] for g,k in zip(rows,choices)) for j in range(m))
        meter.pay('hull_compile','group_scaled_coordinate_sums',2*m*len(rows))
        if point not in unique:
            unique[point]=choices
            meter.pay('hull_compile','generator_and_choice_storage',m+len(rows)+1)
    vertices=[list(p) for p in sorted(unique)]
    return report|dict(status='complete',vertices=vertices,generating_points=len(vertices),
                       redundancy='Duplicate generators removed; no claim every retained point is extreme',
                       generator_choices=[list(unique[tuple(p)]) for p in vertices])
