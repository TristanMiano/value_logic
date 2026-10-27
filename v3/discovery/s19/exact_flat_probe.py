"""Small rational development check for exact-flat receipt inference."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib, json, random, sys, time, traceback

HERE=Path(__file__).resolve().parent

def reduce_rows(rows,d):
    a=[list(map(F,row)) for row in rows]
    pivot=0
    for col in range(d):
        found=next((j for j in range(pivot,len(a)) if a[j][col]),None)
        if found is None: continue
        a[pivot],a[found]=a[found],a[pivot]
        scale=a[pivot][col]; a[pivot]=[x/scale for x in a[pivot]]
        for j in range(len(a)):
            if j!=pivot and a[j][col]:
                scale=a[j][col]
                a[j]=[x-scale*y for x,y in zip(a[j],a[pivot])]
        pivot+=1
    if any(not any(row[:d]) and row[d] for row in a): return None
    return tuple(tuple(row) for row in a[:pivot])

def vertices(ineq,eq,d):
    eq=reduce_rows(eq,d)
    if eq is None: return []
    out=set()
    for chosen in combinations(ineq,d-len(eq)):
        solved=reduce_rows((*eq,*chosen),d)
        if solved is None or len(solved)!=d: continue
        x=tuple(row[-1] for row in solved)
        if all(sum(c*y for c,y in zip(row[:d],x))<=row[d] for row in ineq):
            out.add(x)
    return sorted(out)

def evaluate(f,x): return sum(a*b for a,b in zip(f[:-1],x))+f[-1]

def merge(intervals):
    out=[]
    for a,b in sorted(intervals):
        if out and a<=out[-1][1]: out[-1]=(out[-1][0],max(b,out[-1][1]))
        else: out.append((a,b))
    return out

def range_on(ineq,eq,fs,d):
    vs=vertices(ineq,eq,d)
    if not vs: return None
    xlo=min(vs,key=lambda x:min(evaluate(f,x) for f in fs))
    lo=min(evaluate(f,xlo) for f in fs)
    lifted=[tuple(row[:d])+(F(0),row[d]) for row in ineq]
    lifted += [tuple(-a for a in f[:d])+(F(1),f[d]) for f in fs]
    leq=[tuple(row[:d])+(F(0),row[d]) for row in eq]
    zv=vertices(lifted,leq,d+1)
    assert zv
    zhi=max(zv,key=lambda z:z[-1]); hi=zhi[-1]; xhi=zhi[:-1]
    assert min(evaluate(f,xhi) for f in fs)==hi
    witnesses=[]
    for q in (lo,(lo+hi)/2,hi):
        ratios=[(q-evaluate(f,xlo))/(evaluate(f,xhi)-evaluate(f,xlo))
                for f in fs if evaluate(f,xlo)<q]
        t=max(ratios,default=F(0))
        x=tuple((1-t)*a+t*b for a,b in zip(xlo,xhi))
        assert 0<=t<=1
        assert min(evaluate(f,x) for f in fs)==q
        assert all(sum(a*b for a,b in zip(row[:d],x))<=row[d] for row in ineq)
        assert all(sum(a*b for a,b in zip(row[:d],x))==row[d] for row in eq)
        witnesses.append(x)
    return (lo,hi),witnesses

def exact_flats(equations,d):
    flats={()}; max_count=1; skips=0
    for alternatives in equations:
        nxt=set()
        for flat in flats:
            children=[reduce_rows((*flat,e),d) for e in alternatives]
            if flat in children:
                nxt.add(flat); skips+=1
            else: nxt.update(child for child in children if child is not None)
        flats=nxt; max_count=max(max_count,len(flats))
    return flats,max_count,skips

def inputs():
    rng=random.Random(191934); rows=[]
    for trial in range(54):
        d=1+trial%2; n=1+trial%3; k=trial%6
        base=[]
        for i in range(d):
            a=[0]*d; a[i]=1; base.append(a+[1])
            a=[0]*d; a[i]=-1; base.append(a+[1])
        if d==2: base.extend([[1,1,1],[-1,1,1]])
        gs=[[[rng.randrange(-2,3) for _ in range(d+1)] for _ in range(n)] for _ in range(k)]
        if trial%7==0 and k: gs[0][0]=[0]*(d+1)
        planted=[F(0)]*d
        values=[min(evaluate(g,planted) for g in group) for group in gs]
        if trial%3==0 and k: values[-1]+=F(1,2)
        fs=[[rng.randrange(-3,4) for _ in range(d+1)] for _ in range(n)]
        rows.append(dict(d=d,n=n,k=k,base=base,gs=gs,values=values,fs=fs))
    return rows

def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x

def run():
    rows=inputs(); blob=(json.dumps(encode(rows),indent=2)+'\n').encode()
    (HERE/'exact_flat_inputs.json').write_bytes(blob)
    counts=dict(cases=0,empty=0,source_witnesses=0,assignment_systems=0,
                final_flats=0,skips=0,noisy_deletion_witnesses=0)
    summaries=[]
    for index,row in enumerate(rows):
        d,n,k=(row[s] for s in ('d','n','k'))
        equations=[[tuple(g[:d])+(F(v)-g[d],) for g in group]
                   for group,v in zip(row['gs'],row['values'])]
        ineq=[tuple(map(F,a)) for a in row['base']]
        ineq += [tuple(-F(a) for a in g[:d])+(F(g[d])-v,)
                 for group,v in zip(row['gs'],row['values']) for g in group]
        flats,max_count,skips=exact_flats(equations,d)
        normals=[tuple(g[:d])+(F(0),) for group in row['gs'] for g in group]
        rank=len(reduce_rows(normals,d))
        assert max_count<=n**min(k,rank)
        actual=[]
        for flat in flats:
            result=range_on(ineq,flat,row['fs'],d)
            if result:
                interval,witnesses=result; actual.append(interval)
                for x in witnesses:
                    assert all(min(evaluate(g,x) for g in group)==v
                               for group,v in zip(row['gs'],row['values']))
                counts['source_witnesses']+=len(witnesses)
        expected=[]; systems=set()
        for assignment in product(range(n),repeat=k):
            eq=reduce_rows([equations[j][i] for j,i in enumerate(assignment)],d)
            counts['assignment_systems']+=1
            if eq is not None: systems.add(eq)
        for eq in systems:
            result=range_on(ineq,eq,row['fs'],d)
            if result: expected.append(result[0])
        assert merge(actual)==merge(expected),(index,actual,expected)
        counts['cases']+=1; counts['empty']+=not actual
        counts['final_flats']+=len(flats); counts['skips']+=skips
        summaries.append(dict(case=index,rank=rank,max_flats=max_count,ranges=merge(actual)))
    for N in (1,2,3,5,10,25):
        e=F(1,4*N)
        def satisfied(j,kind,x,y):
            if kind=='A': return x<=F(j,N)-e or y<=1-F(j+1,N)
            return x>=F(j+1,N)+e or y>=1-F(j,N)
        for i in range(N):
            for kind in ('A','B'):
                x=F(2*i+1,2*N); y=1-F(i+(kind=='B'),N)
                assert 0<=x<=1 and 0<=y<=1
                assert not satisfied(i,kind,x,y)
                assert all(satisfied(j,t,x,y) for j in range(N) for t in ('A','B')
                           if (j,t)!=(i,kind))
                counts['noisy_deletion_witnesses']+=1
    return dict(counts=counts,rows=summaries,input_sha256=hashlib.sha256(blob).hexdigest(),
                scope='Finite rational algorithm check; shared linear-algebra helper, no independent proof confirmation.')

if __name__=='__main__':
    start=time.monotonic_ns()
    result=dict(source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    try: result.update(status='COMPLETED_SCREEN',results=run())
    except Exception: result.update(status='FAILED',traceback=traceback.format_exc())
    result['elapsed_ns']=time.monotonic_ns()-start
    (HERE/'exact_flat_result.json').write_bytes((json.dumps(encode(result),indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k!='results'}))
    if result['status']=='FAILED': sys.exit(1)
