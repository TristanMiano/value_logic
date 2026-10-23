"""Cheap literal-cone screen for pure depth-five acceptance vanishing on Q=0."""
from fractions import Fraction as F
from itertools import combinations
import hashlib,json,platform,sys
from pathlib import Path
from time import perf_counter_ns
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
HERE=Path(__file__).resolve().parent
OUT=HERE/'zero_channel.json';RAW=HERE/'zero_channel_raw.json'
assert not OUT.exists() and not RAW.exists()
start=perf_counter_ns()
def syndrome(x):
    s=0
    for i in range(7):
        if (x>>i)&1:s^=i+1
    return s
def center(x):
    s=syndrome(x)
    return x if not s else x^(1<<(s-1))
code=[x for x in range(128) if center(x)==x]
columns=[]
for k in range(2,6):
    for bits in combinations(range(7),k):
        mask=sum(1<<i for i in bits)
        for a in range(1<<k):
            if a.bit_count()<2:continue
            val=sum(((a>>j)&1)<<i for j,i in enumerate(bits))
            columns.append((mask,val))
row_inputs=[x for x in range(128) if x!=center(x)]
rows=[]
for x in row_inputs:
    cx=center(x)
    rows.append({j:F(int(x&m==v)-int(cx&m==v)) for j,(m,v) in enumerate(columns)
                 if int(x&m==v)!=int(cx&m==v)})
ii,jj,vv=[],[],[]
for i,row in enumerate(rows):
    for j,v in row.items():ii.append(i);jj.append(j);vv.append(float(v))
A=coo_matrix((vv,(ii,jj)),shape=(len(rows),len(columns))).tocsr()
cost=[-F(1,1<<m.bit_count()) for m,v in columns]
res=linprog([float(v) for v in cost],A_eq=A,b_eq=np.zeros(len(rows)),
            A_ub=np.ones((1,len(columns))),b_ub=[1],bounds=(0,None),method='highs',
            options={'time_limit':45})
raw=dict(success=bool(res.success),message=res.message,python=sys.version,
         scipy=scipy.__version__,numpy=np.__version__,platform=platform.platform(),
         source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         elapsed_ns=perf_counter_ns()-start)
if res.x is not None:raw['primal']=res.x.tolist()
if res.eqlin.marginals is not None:raw['dual_eq']=res.eqlin.marginals.tolist()
if res.ineqlin.marginals is not None:raw['dual_ub']=res.ineqlin.marginals.tolist()
RAW.write_text(json.dumps(raw,separators=(',',':'))+'\n',encoding='utf-8')
assert res.success,res.message
w=[F(float(v)).limit_denominator(1000000) for v in res.x]
y=[F(float(v)).limit_denominator(1000000) for v in res.eqlin.marginals]
z=F(float(res.ineqlin.marginals[0])).limit_denominator(1000000)
assert all(v>=0 for v in w) and sum(w)<=1 and z<=0
assert all(sum(a*w[j] for j,a in row.items())==0 for row in rows)
ay=[z for _ in columns]
for i,row in enumerate(rows):
    for j,a in row.items():ay[j]+=y[i]*a
assert all(a<=c for a,c in zip(ay,cost))
objective=sum(c*v for c,v in zip(cost,w))
assert objective==z
values={c:sum(w[j] for j,(m,v) in enumerate(columns) if c&m==v) for c in code}
assert values[0]==0
result=dict(status='PASS',classification='DEVELOPMENT; exact literal-cone certificate',
            source_sha256=raw['source_sha256'],raw_sha256=hashlib.sha256(RAW.read_bytes()).hexdigest(),
            elapsed_ns=perf_counter_ns()-start,columns=len(columns),equations=len(rows),
            mean_acceptance=str(-objective),cell_probabilities={str(c):str(v) for c,v in values.items()},
            primal_nonzero=[dict(mask=m,value=v,weight=str(wj)) for (m,v),wj in zip(columns,w) if wj],
            dual_eq_nonzero=[dict(input=row_inputs[i],weight=str(yi)) for i,yi in enumerate(y) if yi],
            dual_ub=str(z),exact_primal_dual_gap_zero=True,
            interpretation='Nonnegative cylinder mixture normalized by total coefficient<=1; not optimal full decision tree acceptance.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in
                 ('primal_nonzero','dual_eq_nonzero')},indent=2))
