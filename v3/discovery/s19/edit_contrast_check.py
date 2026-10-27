"""Exact segment screen for conditioned source-edit contrasts."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import hashlib,json,math,random,sys,time,traceback
import value_set_check as V
HERE=Path(__file__).resolve().parent
INF=math.inf

def subsets(s):
    t=s
    while True:
        yield t
        if t==0:return
        t=(t-1)&s

def add(state,table,k):
    out={}
    for dest in range(1<<k):
        vals=[min(state[dest^t],table[t]) for t in subsets(dest) if t in table and dest^t in state]
        if vals:out[dest]=max(vals)
    return out

def upper(segs,hs,vs,fs,gs):
    n=len(segs); k=len(hs); full=(1<<k)-1
    ft,domains=V.face_tables(segs,hs,vs,fs)
    ut=[{s:v[1] for s,v in row.items()} for row in ft]
    pre=[{0:INF}]
    for row in ut:pre.append(add(pre[-1],row,k))
    suf=[None]*(n+1);suf[n]={0:INF}
    for i in range(n-1,-1,-1):suf[i]=add(suf[i+1],ut[i],k)
    best=None
    for i in range(n):
        omit={}
        for s in range(1<<k):
            vals=[min(pre[i][r],suf[i+1][s^r]) for r in subsets(s) if r in pre[i] and s^r in suf[i+1]]
            if vals:omit[s]=max(vals)
        for t,(lo,hi) in domains[i].items():
            if full^t not in omit:continue
            U=omit[full^t]; h,b=fs[i];gh,gb=gs[i]
            f0=V.dot(h,segs[i][0])+b; slope=V.dot(h,segs[i][1])-V.dot(h,segs[i][0])
            points={lo,hi}
            if slope and U!=INF and lo<=(U-f0)/slope<=hi:points.add((U-f0)/slope)
            for q in points:
                x=V.point(segs[i],q)
                value=min(V.dot(h,x)+b,U)-(V.dot(gh,x)+gb)
                best=value if best is None else max(best,value)
    return best

def solve(rows,n):
    a=[list(r)+[b] for r,b in rows]
    for c in range(n):
        pivot=next((r for r in range(c,n) if a[r][c]),None)
        if pivot is None:return None
        a[c],a[pivot]=a[pivot],a[c]
        div=a[c][c];a[c]=[v/div for v in a[c]]
        for r in range(n):
            if r!=c and a[r][c]:
                v=a[r][c];a[r]=[x-v*y for x,y in zip(a[r],a[c])]
    return tuple(row[-1] for row in a)

def direct(segs,hs,vs,fs,gs):
    n=len(segs); k=len(hs); full=(1<<k)-1; parts=[]
    for seg in segs:
        domain=V.clip(seg,hs,vs,0)
        if domain is None:return None
        lo,hi=domain;cuts={lo,hi}
        for h,v in zip(hs,vs):
            a=V.dot(h,seg[0]);b=V.dot(h,seg[1])-a
            if b and lo<=(v-a)/b<=hi:cuts.add((v-a)/b)
        cuts=sorted(cuts);row=[]
        for a,b in [(x,x) for x in cuts]+list(zip(cuts,cuts[1:])):
            x=V.point(seg,(a+b)/2)
            mask=sum(1<<j for j,(h,v) in enumerate(zip(hs,vs)) if V.dot(h,x)==v)
            row.append((a,b,mask))
        parts.append(row)
    forms=[]
    for objs in (fs,gs):
        forms.append([(V.dot(h,s[1])-V.dot(h,s[0]),V.dot(h,s[0])+b) for s,(h,b) in zip(segs,objs)])
    values=[];fvalues=[];gvalues=[];dvalues=[];vertices=0
    for cells in product(*parts):
        mask=0
        for a,b,m in cells:mask|=m
        if mask!=full:continue
        rows=set()
        for i,(a,b,_) in enumerate(cells):
            coeff=tuple(F(int(j==i)) for j in range(n))
            rows.add((coeff,a));rows.add((coeff,b))
        for ff in forms:
            for i,j in combinations(range(n),2):
                coeff=[F(0)]*n;coeff[i]=ff[i][0];coeff[j]=-ff[j][0]
                rhs=ff[j][1]-ff[i][1]
                if any(coeff):rows.add((tuple(coeff),rhs))
        for chosen in combinations(sorted(rows),n):
            x=solve(chosen,n)
            if x is None or any(not(a<=v<=b) for v,(a,b,_) in zip(x,cells)):continue
            xs=[V.point(seg,t) for seg,t in zip(segs,x)]
            assert all(min(V.dot(h,z) for z in xs)==v for h,v in zip(hs,vs))
            fv=[slope*t+off for (slope,off),t in zip(forms[0],x)]
            gv=[slope*t+off for (slope,off),t in zip(forms[1],x)]
            fvalues.append(min(fv));gvalues.append(min(gv));values.append(min(fv)-min(gv))
            dvalues.extend(a-b for a,b in zip(fv,gv));vertices+=1
    if not values:return None
    # Fair envelope control: separately sharp values AND globally sharp
    # pointwise difference envelope over the same compatible source cells.
    control=(max(min(fvalues)-max(gvalues),min(dvalues)),min(max(fvalues)-min(gvalues),max(dvalues)))
    return (min(values),max(values)),control,vertices

def run():
    rng=random.Random(190527);records=[];bad=0;better=0;vertices=0;sumwidth=F(0);sumcontrol=F(0)
    for trial in range(90):
        n=1+trial%3;d=2;k=trial%4
        segs=[tuple(tuple(F(rng.randrange(-2,4)) for _ in range(d)) for _ in range(2)) for _ in range(n)]
        actual=[V.point(s,F(rng.randrange(5),4)) for s in segs]
        hs=[tuple(F(rng.randrange(-2,3)) for _ in range(d)) for _ in range(k)]
        vs=[min(V.dot(h,x) for x in actual) for h in hs]
        if k and trial%4==1:vs[trial%k]+=F(1,3)
        gen=lambda:[(tuple(F(rng.randrange(-3,4)) for _ in range(d)),F(rng.randrange(-2,3))) for _ in range(n)]
        fs,gs=gen(),gen();U=upper(segs,hs,vs,fs,gs);negL=upper(segs,hs,vs,gs,fs);ref=direct(segs,hs,vs,fs,gs)
        if ref is None:
            assert U is None and negL is None;bad+=1;records.append(dict(case=trial,consistent=False));continue
        exact,control,ct=ref;got=(-negL,U)
        assert got==exact,(trial,got,exact)
        assert control[0]<=got[0]<=got[1]<=control[1]
        w=got[1]-got[0];cw=control[1]-control[0]
        better+=w<cw;sumwidth+=w;sumcontrol+=cw;vertices+=ct
        records.append(dict(case=trial,consistent=True,contrast=list(map(str,got)),control=list(map(str,control))))
    segs=[((F(0),),(F(1),)),((F(0),),(F(0),))]
    fs=[((F(1),),F(0)),((F(0),),F(1,2))];gs=[((F(2),),F(0)),((F(0),),F(1,2))]
    worked=(-upper(segs,[],[],gs,fs),upper(segs,[],[],fs,gs))
    assert worked==(F(-1,4),F(0))
    return dict(cases=90,inconsistent=bad,strictly_narrower_than_combined_control=better,arrangement_vertices_counted=vertices,sum_exact_width=str(sumwidth),sum_control_width=str(sumcontrol),worked_F_minus_G=list(map(str,worked)),records=records)

if __name__=='__main__':
    started=time.perf_counter_ns();plan=json.loads((HERE/'edit_contrast_plan.json').read_text())
    sha=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();assert sha==plan['source_sha256']
    for name,expected in plan['dependencies'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==expected
    try:
        result=dict(status='PASS',source_sha256=sha,dependencies=plan['dependencies'],python=sys.version,results=run(),runtime_ns=time.perf_counter_ns()-started)
        (HERE/'edit_contrast_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
        print(json.dumps({**result,'results':{k:v for k,v in result['results'].items() if k!='records'}}))
    except Exception:
        (HERE/'edit_contrast_failure.json').write_bytes((json.dumps(dict(status='FAIL',source_sha256=sha,traceback=traceback.format_exc()),indent=2)+'\n').encode());raise
