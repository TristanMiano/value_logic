"""Nine small exact cap-three price panels, prospective under15 seconds."""
from pathlib import Path
from itertools import product
from functools import lru_cache
from fractions import Fraction as F
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent


def solve(n,mu):
    allmask=(1<<(1<<n))-1
    ones=[sum(1<<x for x in range(1<<n) if x>>i&1) for i in range(n)]
    parity=sum(1<<x for x in range(1<<n) if x.bit_count()%2)
    maps=set()
    for root in range(n):
        choices=[(allmask,0,0),(0,allmask,0),(0,0,allmask)]
        for second in range(n):
            if second!=root:
                choices += [(0,ones[second],allmask^ones[second]),(0,allmask^ones[second],ones[second])]
        for a,b in product(choices,repeat=2):
            maps.add(tuple((a[k]&(allmask^ones[root]))|(b[k]&ones[root]) for k in range(3)))
    maps=sorted(maps)
    @lru_cache(None)
    def mass(w):
        return (mu.denominator+mu.numerator)*(w&parity).bit_count()+(mu.denominator-mu.numerator)*(w&(allmask^parity)).bit_count()
    splits=0
    @lru_cache(None)
    def value(w):
        nonlocal splits
        if not(w&parity) or not(w&(allmask^parity)):return 0
        best=10**9;seen=set()
        for m in maps:
            g=tuple(w&v for v in m)
            if w in g or g in seen:continue
            seen.add(g);splits+=1
            c=sum((k+1)*mass(v) for k,v in enumerate(g))
            if c<best:best=min(best,c+sum(value(v) for v in g if v))
        return best
    expected=F(value(allmask),mass(allmask))
    return dict(n=n,mu=str(mu),price=str(expected),count_maps=len(maps),states=value.cache_info().currsize,splits=splits)


def main():
    start=time.perf_counter_ns()
    panels=[solve(n,mu) for n in (2,3,4) for mu in (F(0),F(1,2),F(9,10))]
    out=dict(status='PASS',contributor='Codex (GPT-6)',panels=panels,
             elapsed_ns=time.perf_counter_ns()-start,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scope='Exact finite ordinary oracle; no higher-cap generalization is asserted')
    (HERE/'biased_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()
