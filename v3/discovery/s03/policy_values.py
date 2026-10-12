"""Sparse Walsh costs for finite observation/flip policy DAGs.

Codex (GPT-6), 2026-10-12. DEVELOPMENT. Supplied operation semantics only.
"""
from fractions import Fraction as F
from functools import lru_cache


def add(*terms):
    result={}
    for scale,poly in terms:
        for mask,v in poly.items():result[mask]=result.get(mask,F(0))+scale*v
    return {mask:v for mask,v in result.items() if v}


def compile_cost(nodes,root,m):
    @lru_cache(None)
    def visit(k):
        node=nodes[k];kind=node['kind']
        if kind=='terminal':
            row=node['row'];assert len(row)==m+1
            return {mask:v for mask,v in [(0,row[0])]+[(1<<i,row[i+1]) for i in range(m)] if v}
        j=node['bit'];assert 0<=j<m
        charge={0:node['price']};assert node['price']>=0
        if kind=='flip':
            child=node['child'];assert 0<=child<k
            return add((1,charge),(1,{mask:(-v if mask&(1<<j) else v) for mask,v in visit(child).items()}))
        assert kind=='observe';p,n=node['plus'],node['minus'];assert 0<=p<k and 0<=n<k
        a,b=visit(p),visit(n)
        return add((1,charge),(F(1,2),a),(F(1,2),b),
                   (F(1,2),{mask^(1<<j):v for mask,v in add((1,a),(-1,b)).items()}))
    poly=visit(root)
    return poly,visit.cache_info().currsize


def execute(nodes,root,m,world):
    value=F(0);k=root
    while True:
        n=nodes[k]
        if n['kind']=='terminal':return value+n['row'][0]+sum(n['row'][i+1]*(1 if not world&(1<<i) else -1) for i in range(m))
        value+=n['price'];j=n['bit']
        if n['kind']=='flip':world^=1<<j;k=n['child']
        else:k=n['minus'] if world&(1<<j) else n['plus']


def evaluate(poly,world):return sum(v*(1 if (mask&world).bit_count()%2==0 else -1) for mask,v in poly.items())


def upper(poly,intervals):
    value=poly.get(0,F(0));witness={}
    for mask,v in poly.items():
        if mask==0:continue
        lo,hi=intervals[mask];assert -1<=lo<=hi<=1
        witness[mask]=hi if v>=0 else lo;value+=v*witness[mask]
    return value,witness


def bank_regret(polys,choice,intervals):
    rows=[]
    for j,other in enumerate(polys):
        bound,witness=upper(add((1,polys[choice]),(-1,other)),intervals)
        rows.append((bound,j,witness))
    return max(rows,key=lambda row:row[0])


def parity_dag(H,price):
    m=H+1;nodes=[];last={}
    for sign in (1,-1):
        last[sign]=len(nodes);nodes.append({'kind':'terminal','row':tuple([F(1,2)]+[F(0)]*H+[F(-sign,2)])})
    for j in reversed(range(H)):
        current={}
        for sign in (1,-1):
            current[sign]=len(nodes);nodes.append({'kind':'observe','bit':j,'price':price,'plus':last[sign],'minus':last[-sign]})
        last=current
    return nodes,last[1],last[-1]
