"""Extract the retained failed rational reconstruction; no solver rerun."""
from pathlib import Path
from fractions import Fraction as F
import ast
import hashlib
import json
import random

root=Path(__file__).resolve().parent
log=root/'if02'/'c13a0.log'
raw=log.read_text(encoding='utf-8')
proposal=ast.literal_eval(raw.split('AssertionError: ',1)[1].strip())
n,Q=80,15
rng=random.Random(1113)
fees=[F(rng.randrange(1,4)) for _ in range(n)]
C=sum(fees)
p=[]
for i in range(n):
    nums=[rng.randrange(1,8) for _ in range(3)]
    p.append([F(x,sum(nums)) for x in nums])
prices=[[F(x) for x in row] for row in proposal['prices']]
h=[{int(s):F(v) for s,v in row.items()} for row in proposal['potential']]
checks=0
for i in range(n):
    for s in range(min(Q,2*i)+1):
        for x in range(3):
            assert h[i][s]+prices[i][x]>=fees[i]*int(s<Q)+h[i+1][min(Q,s+x)]
            checks+=1
assert all(h[n][s]>=C*int(s<Q) for s in h[n])
bound=h[0][0]+sum((p[i][x]*prices[i][x] for i in range(n) for x in range(3)),F(0))
assert str(bound)==proposal['upper']
result={'source':'Retained c13a0.log; no new LP solve','n':n,'Q':Q,'marginals':[[str(x) for x in row] for row in p],
        'fees':list(map(str,fees)),'fallback':str(C),'proposal':proposal,'verified_upper':str(bound),
        'exact_arc_checks':checks,'raw_log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),
        'limitation':'Primal reconstruction fails. This is a verified upper bound only; sharpness not established for this instance.'}
target=root/'if02'/'c13_upper_only.json'
with target.open('x',encoding='utf-8',newline='\n') as f:
    f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('proposal','marginals','fees')}))
