"""Exact averaged-purity channel and finite Fourier obstruction screen."""
from collections import Counter
from fractions import Fraction as F
from math import comb,sqrt
import hashlib,json
from pathlib import Path
from time import perf_counter_ns

HERE=Path(__file__).resolve().parent
OUT=HERE/'summary_probe.json'
assert not OUT.exists(), 'Preserve exposed evidence.'
start=perf_counter_ns()
parity=lambda z:z.bit_count()%2
syndrome=lambda x:__import__('functools').reduce(int.__xor__,
                    (i+1 for i in range(7) if (x>>i)&1),0)
code=[x for x in range(128) if syndrome(x)==0]
dual=[sum(parity(a&(i+1))<<i for i in range(7)) for a in range(8)]
center=lambda x:x if syndrome(x)==0 else x^(1<<(syndrome(x)-1))
assert len(code)==16 and all(center(x) in code for x in range(128))
assert all((x^center(x)).bit_count()<=1 for x in range(128))
cosets={tuple(sorted(s^d for d in dual)) for s in range(128)}
degree_counts=Counter(max(s.bit_count() for s in coset if s.bit_count()!=4)
                      for coset in cosets)
assert degree_counts=={0:1,5:7,6:7,7:1}
equalities=0
pure_channels=[]
for i in range(7):
    terms=[(s,F(4-s.bit_count(),4)) for s in sorted((1<<i)^d for d in dual)]
    norm=sum(abs(a) for s,a in terms)
    assert norm==F(5,2)
    assert Counter(s.bit_count() for s,a in terms)=={1:1,3:4,5:3}
    by_center={}
    for x in range(128):
        c=center(x)
        fi=(-1)**((c>>i)&1)
        fs=sum(a*(-1)**parity(x&s) for s,a in terms)
        assert fs==fi
        count5=F(0)
        for support,a in terms:
            z=(1 if a>0 else -1)*(-1)**parity(x&support)
            count=5 if z==1 else 6
            queried=[j for j in range(7) if (support>>j)&1]
            queried += [j for j in range(7) if j not in queried][:count-len(queried)]
            assert len(queried)==len(set(queried))==count<=6
            if count==5:
                count5+=abs(a)/norm
        assert count5==(F(7,10) if fi==1 else F(3,10))
        if c in by_center:
            assert by_center[c]==count5
        by_center[c]=count5
        equalities+=1
    pure_channels.append(dict(coordinate=i,terms=[dict(mask=s,coefficient=str(a))
                                               for s,a in terms]))
info=[2,4,5,6]
assert len({tuple((c>>i)&1 for i in info) for c in code})==16
def tail(k):
    return sum(F(comb(k,j))*F(7,10)**j*F(3,10)**(k-j) for j in range(k//2+1))
k=next(k for k in range(1,200,2) if 4*tail(k)<=F(1,100))
assert k==1 or 4*tail(k-2)>F(1,100)

# Diagnostic floating arithmetic for a separate analytic anchored-bound example.
R=lambda e:((sqrt(e*e+4)+e)/2)**2
seq=F(1,10)*R(1)**2
anchor=F(1,10)*R(2)
assert anchor<.6<seq
assert 1/sqrt(2)+1/sqrt(6)<2/sqrt(3)
result=dict(status='PASS',classification='DEVELOPMENT; exact channel enumeration',
  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  elapsed_ns=perf_counter_ns()-start,code_size=len(code),dual_size=len(dual),
  pure_coset_degree_counts=dict(degree_counts),channel_input_equalities=equalities,
  cap=6,code_bit_success='7/10',private_terms=pure_channels,
  amplification=dict(info_coordinates=info,repetitions_per_bit=k,episodes=4*k,
                     codeword_error_union_upper=str(4*tail(k))),
  anchor_example=dict(old_value='.1',edits=[1,1],sequential_upper=seq,
                      anchored_upper=anchor,decision_threshold=.6,
                      relative_bound_reduction=1-anchor/seq),
  limits='No exact finite decoder at cap6; no fee or CPU saving; averaged purity only.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='private_terms'},indent=2))
