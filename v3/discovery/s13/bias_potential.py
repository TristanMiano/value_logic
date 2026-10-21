"""Attempted parity-imbalance potential: retain a failure, never repair in place."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent


def main():
    start=time.perf_counter_ns()
    n=3; universe=(1<<(1<<n))-1
    ones=[sum(1<<x for x in range(1<<n) if x>>i&1) for i in range(n)]
    plus=sum(1<<x for x in range(1<<n) if x.bit_count()%2==0)
    minus=universe^plus
    edges=[(x,x^(1<<i)) for x in range(1<<n) for i in range(n) if not(x>>i&1)]
    def ecount(w):return sum(bool(w>>x&1) and bool(w>>y&1) for x,y in edges)
    def imb(w):return abs((w&plus).bit_count()-(w&minus).bit_count())
    maps=set()
    for root in range(n):
        choices=[(universe,0,0),(0,universe,0),(0,0,universe)]
        for second in range(n):
            if second!=root:
                choices += [(0,ones[second],universe^ones[second]),(0,universe^ones[second],ones[second])]
        for a,b in product(choices,repeat=2):
            maps.add(tuple((a[k]&(universe^ones[root]))|(b[k]&ones[root]) for k in range(3)))
    checked=0;failures=[];tight=0
    for w in range(1,universe+1):
        for m in sorted(maps):
            g=tuple(w&z for z in m)
            crossed=ecount(w)-sum(ecount(z) for z in g)
            delta=sum(imb(z) for z in g)-imb(w)
            for favored in (plus,minus):
                cost=2*sum((k+1)*(z&favored).bit_count() for k,z in enumerate(g))
                rhs=F(7,3)*crossed-F(delta,2)
                checked+=1
                if cost<rhs and len(failures)<5:
                    failures.append(dict(w=w,m=list(m),favored=favored,cost=cost,
                                         rhs=str(rhs),crossed=crossed,delta=delta))
                if cost==rhs:tight+=1
    out=dict(status='REFUTED' if failures else 'FINITE_PASS',contributor='Codex (GPT-6)',
             proposed='cost under parity-weighted mass >= (7/3)*crossed_edges - delta_abs_imbalance/2',
             n=n,maps=len(maps),checks=checked,tight=tight,failures=failures,
             elapsed_ns=time.perf_counter_ns()-start,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scope='Cheap local candidate potential test, not a higher-cap biased theorem.')
    (HERE/'bias_potential.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()
