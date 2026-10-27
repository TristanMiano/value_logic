"""Bounded rational development probe; no numerical LP oracle or statistical claims."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib, json, math, random, sys, time, traceback

HERE=Path(__file__).resolve().parent
INF=math.inf

def merged(intervals):
    out=[]
    for a,b in sorted(intervals):
        assert a<=b
        if out and a<=out[-1][1]: out[-1]=(out[-1][0],max(out[-1][1],b))
        else: out.append((a,b))
    return out

def dp(tables,k):
    layers=[{0:[(INF,INF)]}]
    for table in tables:
        nxt={}
        for dest in range(1<<k):
            vals=[]; sub=dest
            while True:
                if sub in table:
                    l,u=table[sub]
                    for a,b in layers[-1].get(dest^sub,[]):
                        vals.append((min(a,l),min(b,u)))
                if sub==0: break
                sub=(sub-1)&dest
            if vals: nxt[dest]=merged(vals)
        layers.append(nxt)
    return layers

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def point(seg,t): return tuple(a+t*(b-a) for a,b in zip(*seg))
def clip(seg,hs,vs,mask):
    lo,hi=F(0),F(1)
    for j,(h,v) in enumerate(zip(hs,vs)):
        a=dot(h,seg[0])-v; b=dot(h,seg[1])-dot(h,seg[0])
        if mask>>j&1:
            if b==0:
                if a!=0: return None
            else: lo=max(lo,-a/b); hi=min(hi,-a/b)
        elif b>0: lo=max(lo,-a/b)
        elif b<0: hi=min(hi,-a/b)
        elif a<0: return None
        if lo>hi: return None
    return lo,hi

def face_tables(segs,hs,vs,objs):
    tables=[]; domains=[]
    for seg,obj in zip(segs,objs):
        table={}; domain={}
        for mask in range(1<<len(hs)):
            bounds=clip(seg,hs,vs,mask)
            if bounds is None: continue
            domain[mask]=bounds
            if obj is None: table[mask]=(INF,INF)
            else:
                h,offset=obj
                vals=[dot(h,point(seg,t))+offset for t in bounds]
                table[mask]=(min(vals),max(vals))
        tables.append(table); domains.append(domain)
    return tables,domains

def direct_strata(segs,hs,vs,objs):
    parts=[]
    for seg,obj in zip(segs,objs):
        domain=clip(seg,hs,vs,0)
        if domain is None: return []
        lo,hi=domain; cuts={lo,hi}
        for h,v in zip(hs,vs):
            a=dot(h,seg[0]); b=dot(h,seg[1])-a
            if b and lo<= (v-a)/b <=hi: cuts.add((v-a)/b)
        cuts=sorted(cuts)
        cells=[(t,t) for t in cuts]+list(zip(cuts,cuts[1:]))
        row=[]
        for a,b in cells:
            mid=point(seg,(a+b)/2)
            mask=sum(1<<j for j,(h,v) in enumerate(zip(hs,vs)) if dot(h,mid)==v)
            if obj is None: interval=(INF,INF)
            else:
                h,off=obj; vals=[dot(h,point(seg,t))+off for t in (a,b)]
                interval=(min(vals),max(vals))
            row.append((mask,interval))
        parts.append(row)
    out=[]; full=(1<<len(hs))-1
    for cells in product(*parts):
        mask=0
        for m,_ in cells: mask|=m
        if mask==full:
            out.append((min(c[1][0] for c in cells),min(c[1][1] for c in cells)))
    return merged(out)

def recover(layers,tables,domains,segs,objs,k,q):
    params=[None]*len(tables)
    dest=(1<<k)-1
    for i in range(len(tables)-1,-1,-1):
        found=False; sub=dest
        while True:
            if sub in tables[i]:
                l,u=tables[i][sub]
                for a,b in layers[i].get(dest^sub,[]):
                    if min(a,l)<=q<=min(b,u):
                        if a<=q<=b and u>=q: prev=q; new=max(l,q)
                        else: new=q; prev=max(a,q)
                        t0,t1=domains[i][sub]
                        if objs[i] is None: t=t0
                        else:
                            h,off=objs[i]; y0=dot(h,point(segs[i],t0))+off; y1=dot(h,point(segs[i],t1))+off
                            t=t0 if y0==y1 else t0+(new-y0)*(t1-t0)/(y1-y0)
                        assert t0<=t<=t1
                        params[i]=t; dest^=sub; q=prev; found=True; break
            if found or sub==0: break
            sub=(sub-1)&dest
        assert found
    assert dest==0 and q==INF
    return [point(seg,t) for seg,t in zip(segs,params)]

def run():
    rng=random.Random(190526); cases=0; witnesses=0; inconsistent=0; multi=0
    for trial in range(180):
        n=1+trial%4; d=2+trial%2; k=trial%5
        segs=[tuple(tuple(F(rng.randrange(-2,4)) for _ in range(d)) for _ in range(2)) for _ in range(n)]
        actual=[point(seg,F(rng.randrange(5),4)) for seg in segs]
        hs=[tuple(F(rng.randrange(-2,3)) for _ in range(d)) for _ in range(k)]
        vs=[min(dot(h,x) for x in actual) for h in hs]
        if k and trial%3==0: vs[trial%k]+=F(1,3)
        objs=[(tuple(F(rng.randrange(-3,4)) for _ in range(d)),F(rng.randrange(-2,3))) if i==0 or rng.randrange(4) else None for i in range(n)]
        tables,domains=face_tables(segs,hs,vs,objs); layers=dp(tables,k)
        got=layers[-1].get((1<<k)-1,[]); want=direct_strata(segs,hs,vs,objs)
        assert got==want,(trial,got,want)
        inconsistent+=not got; multi+=len(got)>1
        for a,b in got:
            for q in sorted({a,b,(a+b)/2}):
                xs=recover(layers,tables,domains,segs,objs,k,q)
                assert all(min(dot(h,x) for x in xs)==v for h,v in zip(hs,vs))
                assert min(dot(obj[0],x)+obj[1] for x,obj in zip(xs,objs) if obj is not None)==q
                witnesses+=1
        cases+=1
    # The disconnected s18 example is separate from random generation.
    segs=[((F(0),F(1)),(F(2),F(0))),((F(0),F(2)),(F(1),F(0)))]
    hs=[(F(1),F(0)),(F(0),F(1))]; vs=[F(0),F(0)]; objs=[((F(1),F(1)),F(0))]*2
    tables,_=face_tables(segs,hs,vs,objs)
    gap=dp(tables,2)[-1][3]; assert gap==[(F(1),F(1)),(F(2),F(2))]
    hyp=[]
    for k in (2,4,6,8,10):
        m=k//2; weights=[1<<j for j in range(k)]; table={}
        for mask in range(1<<k):
            remain=[weights[j] for j in range(k) if not(mask>>j&1)]
            if len(remain)>=m: table[mask]=(sum(remain[:m]),sum(remain[-m:]))
        got=dp([table,table],k)[-1][(1<<k)-1]
        vals=sorted({min(sum(weights[j] for j in s),sum(weights)-sum(weights[j] for j in s)) for s in combinations(range(k),m)})
        assert got==[(v,v) for v in vals]
        assert len(vals)==math.comb(k,m)//2
        hyp.append(dict(k=k,components=len(vals),minimum=vals[0],maximum=vals[-1]))
    return dict(random_segment_cases=cases,consistent_endpoint_midpoint_witnesses=witnesses,inconsistent_cases=inconsistent,random_disconnected_cases=multi,two_segment_values=[1,2],hypersimplex_cases=hyp)

if __name__=='__main__':
    started=time.perf_counter_ns()
    plan=json.loads((HERE/'value_set_plan.json').read_text())
    sha=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    assert sha==plan['source_sha256']
    try:
        result=dict(status='PASS',source_sha256=sha,python=sys.version,scope=plan['scope'],results=run(),runtime_ns=time.perf_counter_ns()-started)
        (HERE/'value_set_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
        print(json.dumps(result))
    except Exception:
        failure=dict(status='FAIL',source_sha256=sha,traceback=traceback.format_exc(),runtime_ns=time.perf_counter_ns()-started)
        (HERE/'value_set_failure.json').write_bytes((json.dumps(failure,indent=2)+'\n').encode())
        raise
