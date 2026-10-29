"""Construct the fixed developmental audit inputs; does not run an optimizer."""
from fractions import Fraction as F
from pathlib import Path
import json
import random
from lp_witness import dot, linear_solution

HERE = Path(__file__).resolve().parent


def encoded(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k:encoded(v) for k,v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encoded(v) for v in x]
    return x


def box(d, c=None, offset=0):
    rows = []; rhs = []
    for j in range(d):
        row = [F(int(i == j)) for i in range(d)]
        rows.extend([row, [-x for x in row]]); rhs.extend([F(1), F(1)])
    return dict(A=rows, b=rhs, c=[F(1)]*d if c is None else list(map(F,c)), d=F(offset))


def transformed_case(name, dimensions, k, seed, epsilon=F(1,5)):
    rng = random.Random(seed)
    generators = []; inverse = []; shifts = []; source = []
    for d in dimensions:
        transform = [[F(int(a == b) if a <= b else rng.choice((-1,0,1)))
                      for b in range(d)] for a in range(d)]
        columns = [linear_solution(transform, [F(int(j == a)) for a in range(d)], d)
                   for j in range(d)]
        inv = [[columns[j][i] for j in range(d)] for i in range(d)]
        shift = [F(rng.randrange(-2,3),3) for _ in range(d)]
        y = [F(rng.randrange(-2,3),5) for _ in range(d)]
        x = [dot(row,y)+t for row,t in zip(transform,shift)]
        h = [F(rng.randrange(-3,4)) for _ in range(d)]
        c = [sum((h[a]*inv[a][j] for a in range(d)), F(0)) for j in range(d)]
        off = F(rng.randrange(-2,3),7)-dot(c,shift)
        rows = []; rhs = []
        for row in inv:
            rows.extend([row, [-v for v in row]])
            rhs.extend([F(1)+dot(row,shift), F(1)-dot(row,shift)])
        generators.append(dict(A=rows,b=rhs,c=c,d=off))
        inverse.append(inv); shifts.append(shift); source.append(x)
    receipts = []
    for _ in range(k):
        forms = []; vals = []
        for d, inv, shift, x in zip(dimensions,inverse,shifts,source):
            h = [F(rng.randrange(-2,3)) for _ in range(d)]
            c = [sum((h[a]*inv[a][j] for a in range(d)), F(0)) for j in range(d)]
            off = F(rng.randrange(-3,4),4)-dot(c,shift)
            forms.append(dict(c=c,d=off)); vals.append(dot(c,x)+off)
        value = min(vals)
        receipts.append(dict(lo=value-epsilon,hi=value+epsilon,forms=forms))
    return dict(name=name,problem=dict(generators=generators,receipts=receipts),
                known_source=source)


def prediction_duty():
    gs = []
    for c in (F(6,5),F(9,5)):
        gs.append(dict(A=[[F(1),F(0)],[F(-1),F(0)],[F(0),F(1)],
                          [F(0),F(-1)],[F(1),F(1)],[F(-1),F(-1)]],
                       b=[F(1),F(0),F(1),F(0),c+F(1,100),-c+F(1,100)],
                       c=[F(1,2),F(-3,2)],d=F(0)))
    rs = [dict(lo=F(-1),hi=F(-99,100),forms=[dict(c=h,d=F(0)) for _ in gs])
          for h in ([F(-1),F(0)],[F(0),F(-1)])]
    return dict(name='noisy_envelope',problem=dict(generators=gs,receipts=rs),
                expected=[['-281/200','-11/8'],['-221/200','-43/40']])


def cases():
    out = [dict(name='no_receipts',problem=dict(generators=[box(1,[2],1)],receipts=[]),
                expected=[['-1','3']]), prediction_duty()]
    for name,dims,k,seed in (
        ('mixed_1_3_7',[1,3,7],3,2001),
        ('mixed_2_5',[2,5],4,2002),
        ('single_7',[7],3,2003),
        ('three_4',[4,4,4],3,2004),
        ('four_3',[3,3,3,3],3,2005),
        ('exact_mixed',[2,4,6],3,2006),
        ('empty_receipts_mixed',[3,5,7],0,2007)):
        out.append(transformed_case(name,dims,k,seed,F(0) if name=='exact_mixed' else F(1,5)))
    # A lower-dimensional segment in five coordinates, with exact equalities
    # represented by pairs of inequalities and a constant observed response.
    g=box(5,[1,-2,3,-4,5],F(2,3))
    for j in range(1,5):
        row=[F(int(i==j)-int(i==0)) for i in range(5)]
        g['A'].extend([row,[-v for v in row]]);g['b'].extend([F(0),F(0)])
    rs=[dict(lo=F(7,3),hi=F(7,3),forms=[dict(c=[F(0)]*5,d=F(7,3))])]
    out.append(dict(name='degenerate_segment',problem=dict(generators=[g],receipts=rs),
                    expected=[['-7/3','11/3']]))
    huge=F(10**400+1,3)
    out.append(dict(name='huge_constant',problem=dict(generators=[box(3,[0,0,0],huge)],receipts=[]),
                    expected=[[str(huge),str(huge)]]))
    # Global lower constraints contradict a constant response. All local
    # slices are empty; the producer must give actual Farkas multipliers.
    out.append(dict(name='inconsistent_constant',problem=dict(generators=[box(2),box(4)],
        receipts=[dict(lo=F(1),hi=F(2),forms=[dict(c=[F(0)]*d,d=F(0)) for d in (2,4)])]),
        expected=[]))
    # The maximal-compatible-cover counterexample in comparison.md.
    gs=[dict(A=[[F(1)],[F(-1)]],b=[F(1),F(0)],c=[F(-1)],d=F(0)) for _ in range(2)]
    out.append(dict(name='maximal_cover_loss',problem=dict(generators=gs,receipts=[
        dict(lo=F(0),hi=F(0),forms=[dict(c=[F(1)],d=F(0)) for _ in gs])]),
        expected=[['-1','0']]))
    return out


if __name__ == '__main__':
    path=HERE/'audit_inputs.json'
    if path.exists():
        raise SystemExit('refuse to overwrite prepared inputs')
    path.write_text(json.dumps(encoded(cases()),indent=2)+'\n',encoding='utf-8')
    print('Prepared 13 developmental input cases; no optimization executed.')
