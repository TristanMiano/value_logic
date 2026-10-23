"""Exact F3 checks of two-sided error interpolation and one-query ambiguity."""
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import platform
from time import perf_counter_ns

start=perf_counter_ns()
p=3
U=[[1,0],[0,1],[1,1],[1,2]]
prices=[3,4,1,2]
def mul(A,x):
    return [sum(a*b for a,b in zip(row,x))%p for row in A]
def solve(A,b):
    cols=len(A[0])
    rows=[list(a)+[v] for a,v in zip(A,b)]
    pivot=[]
    at=0
    for j in range(cols):
        hit=next((i for i in range(at,len(rows)) if rows[i][j]%p),None)
        if hit is None:
            continue
        rows[at],rows[hit]=rows[hit],rows[at]
        inv=pow(rows[at][j],-1,p)
        rows[at]=[v*inv%p for v in rows[at]]
        for i in range(len(rows)):
            if i!=at:
                v=rows[i][j]
                rows[i]=[(a-v*b)%p for a,b in zip(rows[i],rows[at])]
        pivot.append(j)
        at+=1
    if any(not any(row[:cols]) and row[-1] for row in rows):
        return None
    x=[0]*cols
    for i,j in enumerate(pivot):
        x[j]=rows[i][-1]
    return x
def transpose(A):
    return list(map(list,zip(*A)))
def rank2(rows):
    return (rows[0][0]*rows[1][1]-rows[0][1]*rows[1][0])%p!=0

available=[pair for pair in combinations(range(4),2) if rank2([U[i] for i in pair])]
J=min(available,key=lambda js:sum(prices[j] for j in js))
assert J==(2,3)
checked=0
new_query_counts=[]
for coeffs in product(range(p),repeat=6):
    C=[list(coeffs[:3]),list(coeffs[3:])]
    truth=lambda phi:mul(U,mul(C,phi))
    basis=[[1,0,0]]
    images=[truth(basis[0])]
    queried=0
    for phi in product(range(p),repeat=3):
        alpha=solve(transpose(basis),list(phi))
        if alpha is not None:
            repaired=mul(transpose(images),alpha)
        else:
            direct=truth(phi)
            coeff=solve([U[j] for j in J],[direct[j] for j in J])
            assert coeff is not None
            repaired=mul(U,coeff)
            basis.append(list(phi))
            images.append(repaired)
            queried+=len(J)
        assert repaired==truth(phi)
        checked+=1
    assert queried==4
    new_query_counts.append(queried)

fibers=0
for row in U:
    for value in range(p):
        candidates=[z for z in product(range(p),repeat=2) if mul([row],z)==[value]]
        assert len(candidates)==3
        assert len({tuple(mul(U,z)) for z in candidates})==3
        fibers+=1
result=dict(status='PASS',model='Codex (GPT-6)',python=platform.python_version(),
    source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
    field=p,output_dimension=4,error_dimension=2,feature_dimension=3,
    coefficient_maps=len(new_query_counts),repaired_vectors_checked=checked,
    new_exact_coordinate_queries_per_map=4,minimum_price_anchor_rows=list(J),
    anchor_price=sum(prices[j] for j in J),one_query_ambiguous_fibers=fibers,
    elapsed_ns=perf_counter_ns()-start,
    scope='Exact finite-field development checks; no general cost benchmark or independent reconstruction.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
