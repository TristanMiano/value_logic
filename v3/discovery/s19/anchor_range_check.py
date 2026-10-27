"""Exact development check for anchored attainable ranges; independent polygons."""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import hashlib, json, math, random, sys, time, traceback
import value_set_check as old

HERE=Path(__file__).resolve().parent
POS=math.inf
NEG=-math.inf

def cross(o,a,b):
    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])

def hull(points):
    ps=sorted(set(points))
    if len(ps)<=1: return ps
    lower=[]; upper=[]
    for p in ps:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0: lower.pop()
        lower.append(p)
    for p in reversed(ps):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0: upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]

def dot(a,b): return sum(x*y for x,y in zip(a,b))

def clip(poly,h,b):
    """Retain h.x >= b; handles points and segments as well as polygons."""
    if not poly: return []
    out=[]
    for a,z in zip(poly,poly[1:]+poly[:1]):
        fa=dot(h,a)-b; fz=dot(h,z)-b
        if fa>=0: out.append(a)
        if (fa<0<fz) or (fz<0<fa):
            t=fa/(fa-fz)
            out.append(tuple(x+t*(y-x) for x,y in zip(a,z)))
        elif fa<0 and fz==0: out.append(z)
    return hull(out)

def contains(poly,x):
    if len(poly)==1: return x==poly[0]
    if len(poly)==2:
        a,b=poly
        return cross(a,b,x)==0 and all(min(u,v)<=w<=max(u,v) for u,v,w in zip(a,b,x))
    return bool(poly) and all(cross(a,b,x)>=0 for a,b in zip(poly,poly[1:]+poly[:1]))

def local_tables(polys,hs,los,his,objs):
    tables=[]; extrema=[]
    for poly,obj in zip(polys,objs):
        base=poly
        for h,b in zip(hs,los): base=clip(base,h,b)
        table={}; ends={}
        for mask in range(1<<len(hs)):
            face=base
            for j,(h,b) in enumerate(zip(hs,his)):
                if mask>>j&1: face=clip(face,tuple(-x for x in h),-b)
            if face:
                val=lambda x: dot(obj[0],x)+obj[1]
                a=min(face,key=val); b=max(face,key=val)
                table[mask]=(val(a),val(b)); ends[mask]=(a,b)
        tables.append(table); extrema.append(ends)
    return tables,extrema

def advance(previous,table,k,counter):
    out={}; choices={}
    for dest in range(1<<k):
        sub=dest; best=NEG
        while True:
            counter['split_scans']+=1
            if sub in table and dest^sub in previous:
                value=min(previous[dest^sub],table[sub][1])
                if value>best: best=value; choices[dest]=sub
            if sub==0: break
            sub=(sub-1)&dest
        if best!=NEG: out[dest]=best
    return out,choices

def anchored(tables,k):
    n=len(tables); full=(1<<k)-1; counts=dict(split_scans=0,anchor_intervals=0)
    pref=[{0:POS}]; pb=[None]
    for tab in tables:
        nxt,ch=advance(pref[-1],tab,k,counts); pref.append(nxt); pb.append(ch)
    suff=[None]*(n+1); sb=[None]*n; suff[n]={0:POS}
    for i in range(n-1,-1,-1): suff[i],sb[i]=advance(suff[i+1],tables[i],k,counts)
    outside=[]; ob=[]; intervals=[]
    for i,tab in enumerate(tables):
        row={}; choices={}
        for dest in range(1<<k):
            sub=dest; best=NEG
            while True:
                counts['split_scans']+=1
                if sub in pref[i] and dest^sub in suff[i+1]:
                    value=min(pref[i][sub],suff[i+1][dest^sub])
                    if value>best: best=value; choices[dest]=sub
                if sub==0: break
                sub=(sub-1)&dest
            if best!=NEG: row[dest]=best
        outside.append(row); ob.append(choices)
        for mask,(lo,hi) in tab.items():
            cap=row.get(full^mask,NEG)
            if lo<=min(hi,cap): intervals.append((lo,min(hi,cap),i,mask))
    counts['anchor_intervals']=len(intervals)
    assert counts['split_scans']==3*n*3**k
    return dict(ranges=old.merged([(a,b) for a,b,_,_ in intervals]), intervals=intervals,
                pb=pb,sb=sb,ob=ob,counts=counts,k=k)

def recover(result,tables,extrema,q):
    k=result['k']; full=(1<<k)-1; n=len(tables)
    _,_,i,mask=next(z for z in result['intervals'] if z[0]<=q<=z[1])
    assignment=[None]*n; assignment[i]=mask
    left=result['ob'][i][full^mask]; right=(full^mask)^left
    for j in range(i,0,-1):
        sub=result['pb'][j][left]; assignment[j-1]=sub; left^=sub
    for j in range(i+1,n):
        sub=result['sb'][j][right]; assignment[j]=sub; right^=sub
    assert left==right==0 and all(m is not None for m in assignment)
    xs=[extrema[j][m][1] for j,m in enumerate(assignment)]
    a,b=extrema[i][mask]; lo,hi=tables[i][mask]
    t=Q(0) if lo==hi else (q-lo)/(hi-lo)
    xs[i]=tuple(x+t*(y-x) for x,y in zip(a,b))
    return xs

def brute(tables,k):
    n=len(tables); ranges=[]; assignments=0
    for labels in product(range(n),repeat=k):
        assignments+=1; masks=[0]*n
        for j,i in enumerate(labels): masks[i]|=1<<j
        if all(m in tab for m,tab in zip(masks,tables)):
            ranges.append((min(tab[m][0] for m,tab in zip(masks,tables)),
                           min(tab[m][1] for m,tab in zip(masks,tables))))
    return old.merged(ranges),assignments

def encoded(value):
    if isinstance(value,Q): return str(value)
    if isinstance(value,dict): return {str(k):encoded(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [encoded(v) for v in value]
    return value

def inputs():
    rng=random.Random(191928); cases=[]
    for trial in range(180):
        n=1+trial%5; k=trial%6
        polys=[hull([tuple(Q(rng.randrange(-3,5)) for _ in range(2)) for _ in range(7)]) for _ in range(n)]
        actual=[tuple(sum(x[a] for x in p)/len(p) for a in range(2)) for p in polys]
        hs=[tuple(Q(rng.randrange(-2,3)) for _ in range(2)) for _ in range(k)]
        vals=[min(dot(h,x) for x in actual) for h in hs]
        width=Q(0) if trial%2==0 else Q(1+trial%3,3)
        los=[v-width for v in vals]; his=[v+width for v in vals]
        if k and trial%7==0: los[0]+=7; his[0]+=7
        objs=[(tuple(Q(rng.randrange(-3,4)) for _ in range(2)),Q(rng.randrange(-2,3))) for _ in polys]
        cases.append(dict(polys=polys,hs=hs,los=los,his=his,objs=objs))
    return cases

def run(cases):
    rows=[]; witness_count=0
    for trial,c in enumerate(cases):
        tabs,ends=local_tables(**c); k=len(c['hs'])
        ans=anchored(tabs,k); direct,num=brute(tabs,k)
        earlier=old.dp(tabs,k)[-1].get((1<<k)-1,[])
        assert ans['ranges']==direct==earlier,(trial,ans['ranges'],direct,earlier)
        for a,b in ans['ranges']:
            for q in sorted({a,b,(a+b)/2}):
                xs=recover(ans,tabs,ends,q)
                assert all(contains(p,x) for p,x in zip(c['polys'],xs))
                assert all(lo<=min(dot(h,x) for x in xs)<=hi for h,lo,hi in zip(c['hs'],c['los'],c['his']))
                assert min(dot(o[0],x)+o[1] for o,x in zip(c['objs'],xs))==q
                witness_count+=1
        rows.append(dict(trial=trial,n=len(tabs),k=k,ranges=ans['ranges'],assignment_scans=num,**ans['counts']))
    gap_rows=[]
    polys=[[(Q(0),Q(1)),(Q(2),Q(0))],[(Q(0),Q(2)),(Q(1),Q(0))]]
    hs=[(Q(1),Q(0)),(Q(0),Q(1))]; objs=[((Q(1),Q(1)),Q(0))]*2
    for eps in (Q(0),Q(1,10),Q(1,2),Q(2,3),Q(1)):
        tabs,_=local_tables(polys,hs,[-eps]*2,[eps]*2,objs)
        got=anchored(tabs,2)['ranges']
        expected=old.merged([(Q(1),1+eps/2),(2-eps,Q(2))]) if eps<Q(2,3) else [(Q(1),Q(2))]
        assert got==expected,(eps,got,expected)
        gap_rows.append(dict(epsilon=eps,ranges=got))
    hyp=[]
    for k in (2,4,6,8,10):
        m=k//2; weights=[1<<j for j in range(k)]; tab={}
        for mask in range(1<<k):
            remaining=[weights[j] for j in range(k) if not(mask>>j&1)]
            if len(remaining)>=m: tab[mask]=(sum(remaining[:m]),sum(remaining[-m:]))
        ans=anchored([tab,tab],k)
        vals=sorted({min(sum(weights[j] for j in s),sum(weights)-sum(weights[j] for j in s)) for s in combinations(range(k),m)})
        assert ans['ranges']==[(v,v) for v in vals]
        hyp.append(dict(k=k,components=len(vals),**ans['counts']))
    return dict(polygon_cases=len(rows),witness_checks=witness_count,
                inconsistent=sum(not r['ranges'] for r in rows),
                disconnected=sum(len(r['ranges'])>1 for r in rows),
                brute_assignment_scans=sum(r['assignment_scans'] for r in rows),
                split_scans=sum(r['split_scans'] for r in rows),
                rows=rows,noisy_gap_cases=gap_rows,hypersimplex_cases=hyp)

if __name__=='__main__':
    plan=json.loads((HERE/'anchor_range_plan.json').read_text())
    sha=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    assert sha==plan['source_sha256']
    assert hashlib.sha256((HERE/'value_set_check.py').read_bytes()).hexdigest()==plan['dependency_sha256']
    assert not (HERE/'anchor_range_result.json').exists()
    start=time.perf_counter_ns()
    try:
        cases=inputs(); raw=(json.dumps(encoded(cases),separators=(',',':'))+'\n').encode()
        (HERE/'anchor_range_inputs.json').write_bytes(raw)
        result=dict(status='PASS',source_sha256=sha,input_sha256=hashlib.sha256(raw).hexdigest(),
                    results=encoded(run(cases)),runtime_ns=time.perf_counter_ns()-start,python=sys.version)
        (HERE/'anchor_range_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
        print(json.dumps({k:v for k,v in result.items() if k!='results'}))
        print(json.dumps({k:v for k,v in result['results'].items() if k!='rows'}))
    except Exception:
        failure=dict(status='FAIL',source_sha256=sha,traceback=traceback.format_exc(),runtime_ns=time.perf_counter_ns()-start)
        (HERE/'anchor_range_failure.json').write_bytes((json.dumps(failure,indent=2)+'\n').encode())
        raise
