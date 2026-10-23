"""Reconstruct the exposed zero-channel LP basis exactly; no new solver exposure."""
from fractions import Fraction as F
from itertools import combinations
import hashlib,json
from pathlib import Path
from time import perf_counter_ns
HERE=Path(__file__).resolve().parent
OUT=HERE/'zero_repair.json'
assert not OUT.exists()
start=perf_counter_ns()
raw_path=HERE/'zero_channel_raw.json'
raw=json.loads(raw_path.read_text())
assert raw['source_sha256']==hashlib.sha256((HERE/'zero_channel.py').read_bytes()).hexdigest()
def syndrome(x):
    s=0
    for i in range(7):
        if (x>>i)&1:s^=i+1
    return s
def center(x):
    s=syndrome(x)
    return x if not s else x^(1<<(s-1))
code=[x for x in range(128) if center(x)==x]
cols=[]
for k in range(2,6):
    for bits in combinations(range(7),k):
        mask=sum(1<<i for i in bits)
        for a in range(1<<k):
            if a.bit_count()<2:continue
            val=sum(((a>>j)&1)<<i for j,i in enumerate(bits))
            cols.append((mask,val))
xs=[x for x in range(128) if x!=center(x)]
rows=[{j:F(int(x&m==v)-int(center(x)&m==v)) for j,(m,v) in enumerate(cols)
       if int(x&m==v)!=int(center(x)&m==v)} for x in xs]
cost=[-F(1,1<<m.bit_count()) for m,v in cols]
y=[F(v).limit_denominator(1000000) for v in raw['dual_eq']]
z=F(raw['dual_ub'][0]).limit_denominator(1000000)
ay=[z for _ in cols]
for i,row in enumerate(rows):
    for j,a in row.items():ay[j]+=y[i]*a
assert z<=0 and all(a<=c for a,c in zip(ay,cost))
support=[j for j,w in enumerate(raw['primal']) if w>1e-10]
mat=[[row.get(j,F(0)) for j in support]+[F(0)] for row in rows]
mat.append([F(1) for j in support]+[F(1)])
mat.append([cost[j] for j in support]+[z])
pivots=[]
r=0
for col in range(len(support)):
    pivot=next((i for i in range(r,len(mat)) if mat[i][col]),None)
    if pivot is None:continue
    mat[r],mat[pivot]=mat[pivot],mat[r]
    div=mat[r][col]
    mat[r]=[a/div for a in mat[r]]
    for i in range(len(mat)):
        if i==r or not mat[i][col]:continue
        factor=mat[i][col]
        mat[i]=[a-factor*b for a,b in zip(mat[i],mat[r])]
    pivots.append(col);r+=1
assert all(any(row[:-1]) or row[-1]==0 for row in mat)
assert len(pivots)==len(support), 'Nonunique exposed support needs another declared reconstruction.'
w=[F(0) for _ in cols]
for i,col in enumerate(pivots):w[support[col]]=mat[i][-1]
assert all(a>=0 for a in w) and sum(w)<=1
assert all(sum(a*w[j] for j,a in row.items())==0 for row in rows)
assert sum(a*b for a,b in zip(cost,w))==z
values={c:sum(w[j] for j,(m,v) in enumerate(cols) if c&m==v) for c in code}
assert values[0]==0
result=dict(status='PASS',classification='DEVELOPMENT; exact repair of exposed LP support',
  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  input_raw_sha256=hashlib.sha256(raw_path.read_bytes()).hexdigest(),
  elapsed_ns=perf_counter_ns()-start,support_size=len(support),rank=r,
  mean_acceptance=str(-z),cell_probabilities={str(c):str(v) for c,v in values.items()},
  primal_nonzero=[dict(mask=m,value=v,weight=str(wj)) for (m,v),wj in zip(cols,w) if wj],
  dual_eq_nonzero=[dict(input=xs[i],weight=str(yi)) for i,yi in enumerate(y) if yi],
  dual_ub=str(z),exact_primal_dual_gap_zero=True,
  prior_failure='Independent limit_denominator rounding did not satisfy exact normalization. Raw solver exposure retained; no hardware attribution.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('primal_nonzero','dual_eq_nonzero')},indent=2))
