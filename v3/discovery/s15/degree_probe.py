"""Small all-input screens of the all-length analytic Hamming identity."""
from collections import Counter
from fractions import Fraction as F
import hashlib,json
from pathlib import Path
from time import perf_counter_ns
HERE=Path(__file__).resolve().parent;OUT=HERE/'degree_probe.json'
assert not OUT.exists()
start=perf_counter_ns()
results=[]
for r in (2,3,4):
    m=1<<(r-1);g=2*m-1
    dual=[sum(((a&(i+1)).bit_count()%2)<<i for i in range(g)) for a in range(1<<r)]
    cosets={tuple(sorted(s^d for d in dual)) for s in range(1<<g)}
    deg=Counter(max(s.bit_count() for s in coset if s.bit_count()!=m) for coset in cosets)
    assert min(k for k in deg if k)>m
    assert deg[m+1]>0
    terms=[(1^d,m-(1^d).bit_count()) for d in dual]
    assert sum(abs(a) for s,a in terms)==3*m-2
    for x in range(1<<g):
        syndrome=0
        for i in range(g):
            if (x>>i)&1:syndrome^=i+1
        c=x if syndrome==0 else x^(1<<(syndrome-1))
        val=sum(a*(-1)**((x&s).bit_count()%2) for s,a in terms)
        assert val==m*(-1)**(c&1)
    results.append(dict(r=r,length=g,inputs=1<<g,cosets=len(cosets),
                        degree_distribution=dict(deg),minimum_information_cap=m+2,
                        coordinate_channel_success=str(F(2*m-1,3*m-2))))
result=dict(status='PASS',classification='DEVELOPMENT; finite exact identities',
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            elapsed_ns=perf_counter_ns()-start,panels=results,
            scope='Single coordinate checked at all inputs; all nonconstant coset degree minima enumerated for lengths3,7,15 only.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
