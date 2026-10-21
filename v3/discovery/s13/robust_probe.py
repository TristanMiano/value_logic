"""Finite exact checks of two new interface bounds; no empirical gain."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import time

HERE=Path(__file__).resolve().parent


def main():
    start=time.perf_counter_ns();rng=random.Random(202610213)
    counts=dict(tariff_maps=0,valid_tariff_panels=0,spectral_panels=0,
                spectral_bounds=0,sharp_endpoints=0,interval_bounds=0)
    n=3;full=(1<<(1<<n))-1
    ones=[sum(1<<x for x in range(1<<n) if x>>i&1) for i in range(n)]
    for root in range(n):
        choices=[(full,0,0),(0,full,0),(0,0,full)]
        for second in range(n):
            if second!=root:
                choices.extend([(0,ones[second],full^ones[second]),
                                (0,full^ones[second],ones[second])])
        for left,right in product(choices,repeat=2):
            m=tuple((left[k]&(full^ones[root]))|(right[k]&ones[root])
                    for k in range(3))
            # Reporting b at count1, 2b at count2/3 leaves only first-bit information.
            assert m[0] in (0,full,ones[root],full^ones[root])
            assert (m[1]|m[2])==(full^m[0])
            counts['tariff_maps']+=1
    for b in (F(3,2),F(7,4),F(199,100)):
        for k,bill in ((1,b),(2,2*b),(3,2*b)):
            assert k<=bill<=k*b
        assert b<2
        counts['valid_tariff_panels']+=1

    def h(z,s):return z/(s+(1-s)*z)
    def envelope(mu,a,b,s):
        chord=h(a,s) if a==b else ((b-mu)*h(a,s)+(mu-a)*h(b,s))/(b-a)
        return (h(mu,s),chord) if s>=1 else (chord,h(mu,s))

    for _ in range(100):
        atoms=[F(rng.randrange(0,21),rng.randrange(1,8)) for _ in range(rng.randrange(1,7))]
        raw=[rng.randrange(1,9) for _ in atoms];weights=[F(x,sum(raw)) for x in raw]
        t0=F(rng.randrange(1,9),rng.randrange(1,8))
        z=[1/(1+t0*x) for x in atoms];mu=sum(w*x for w,x in zip(weights,z))
        a,b=min(z),max(z)
        for s in (F(1,10),F(1,2),F(1),F(2),F(10)):
            actual=sum(w*h(x,s) for w,x in zip(weights,z))
            lo,hi=envelope(mu,a,b,s)
            assert lo<=actual<=hi
            wide=(h(mu,s),mu) if s>=1 else (mu,h(mu,s))
            assert wide[0]<=lo<=hi<=wide[1]
            counts['spectral_bounds']+=2
            # Matching one-atom and two-endpoint laws.
            if a<b:
                p=(mu-a)/(b-a);end=p*h(b,s)+(1-p)*h(a,s)
                assert end==(hi if s>=1 else lo)
                counts['sharp_endpoints']+=1
            L=max(a,mu-F(1,100));U=min(b,mu+F(1,100))
            assert envelope(L,a,b,s)[0]<=actual<=envelope(U,a,b,s)[1]
            counts['interval_bounds']+=1
        counts['spectral_panels']+=1
    assert envelope(F(3,4),F(1,2),F(1),F(2))==(F(3,5),F(2,3))
    out=dict(status='PASS',contributor='Codex (GPT-6)',seed=202610213,counts=counts,
             elapsed_ns=time.perf_counter_ns()-start,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scope='Finite exact interface/algebra checks, not independent proof or measured saving')
    (HERE/'robust_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()
