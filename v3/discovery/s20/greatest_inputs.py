"""Deterministic prospective input builder; no optimization or probe runs."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import json
import random
from audit_inputs import encoded


def problem(dimensions, k, seed, epsilon=F(1,10), constant=False):
    rng = random.Random(seed)
    generators = []
    for d in dimensions:
        rows, rhs = [], []
        for j in range(d):
            e = [F(int(a == j)) for a in range(d)]
            rows.extend([e,[-a for a in e]])
            rhs.extend([F(1),F(0)])
            if d > 1:
                row = e.copy()
                row[(j+1)%d] -= F(1,2)
                rows.append(row)
                rhs.append(F(rng.randrange(2,6),10))
        rows.append([-F(1)]*d)
        rhs.append(-F(d,10))
        generators.append(dict(A=rows,b=rhs,c=[F(0) if constant else F(rng.randrange(4)) for _ in range(d)],
                               d=F(3) if constant else F(rng.randrange(-3,4),10)))
    receipts = []
    for j in range(k):
        forms, values = [], []
        for d in dimensions:
            coord, scale, off = rng.randrange(d), F(rng.randrange(1,3)), F(rng.randrange(-2,3),10)
            h = [F(0)]*d
            h[coord] = -scale
            forms.append(dict(c=h,d=-off))
            values.append(scale/F(10)+off)
        peak = max(values)
        receipts.append(dict(lo=-peak-epsilon,hi=-peak+epsilon,forms=forms))
    return dict(generators=generators,receipts=receipts)


def cases():
    rows = []
    for name,dims,k,seed,eps,constant in [
        ('no_receipts',[1],0,4001,F(1,10),False),
        ('two_coupled',[2,3],2,4002,F(1,10),False),
        ('single_four',[4],4,4003,F(1,10),False),
        ('many_mixed',[1,2,3,4],4,4004,F(1,10),False),
        ('exact_reports',[2,2,2],3,4005,F(0),False),
        ('constant_future',[2,3],2,4006,F(1,10),True),
    ]:
        rows.append(dict(name=name,problem=problem(dims,k,seed,eps,constant)))
    g = dict(A=[[F(1)],[-F(1)]],b=[F(1),F(0)],c=[F(1)],d=F(0))
    tied = dict(generators=[deepcopy(g),deepcopy(g)],receipts=[
        dict(lo=-F(1),hi=-F(1,2),forms=[dict(c=[-F(1)],d=F(0)) for _ in range(2)])])
    rows.append(dict(name='tied_outside',problem=tied))
    missed = deepcopy(tied)
    missed['receipts'][0].update(lo=-F(3),hi=-F(2))
    rows.append(dict(name='missed_receipt',problem=missed))
    empty = deepcopy(tied)
    empty['receipts'][0].update(lo=F(1),hi=F(2))
    rows.append(dict(name='empty_block',problem=empty))
    return encoded(rows)


if __name__ == '__main__':
    p = Path(__file__).with_name('greatest_inputs.json')
    if p.exists():
        raise SystemExit('refuse to replace prepared inputs')
    p.write_text(json.dumps(cases(),indent=2)+'\n',encoding='utf-8')
