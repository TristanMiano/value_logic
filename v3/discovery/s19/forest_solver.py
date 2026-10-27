"""Development forest/cycle receipt solver with rational vertex LPs."""
from functools import lru_cache
from math import inf
import exact_flat_probe as lin

def upper_row(case,j,i):
    g=case['gs'][j][i]
    return tuple(g[:-1])+(case['his'][j]-g[-1],)

def base_rows(case):
    out=[list(map(tuple,b)) for b in case['bases']]
    for j,group in enumerate(case['gs']):
        for i,g in group.items():
            out[i].append(tuple(-v for v in g[:-1])+(g[-1]-case['los'][j],))
    return out

def spanning(case):
    n=len(case['bases']); k=len(case['gs']); par=list(range(n+k))
    def root(a):
        while par[a]!=a:
            par[a]=par[par[a]]; a=par[a]
        return a
    kept=[]; extra=[]
    for j,group in enumerate(case['gs']):
        for i in sorted(group):
            a,b=root(i),root(n+j)
            if a==b: extra.append((j,i))
            else: par[a]=b; kept.append((j,i))
    return kept,extra

class Forest:
    def __init__(self,case,kept,selected=(),floor=None,counts=None):
        self.case=case; self.n=len(case['bases']); self.k=len(case['gs'])
        self.counts=counts if counts is not None else {}
        self.q=base_rows(case); covered={j for j,i in selected}
        for j,i in selected: self.q[i].append(upper_row(case,j,i))
        if floor is not None:
            for i,f in enumerate(case['fs']):
                self.q[i].append(tuple(-a for a in f[:-1])+(f[-1]-floor,))
        self.vn=[[] for _ in range(self.n)]; self.rn={j:[] for j in range(self.k) if j not in covered}
        for j,i in kept:
            if j in self.rn: self.vn[i].append(j); self.rn[j].append(i)
        self.bad=any(not ns for ns in self.rn.values())
        seen=set(); self.roots=[]
        for i in range(self.n):
            if i in seen: continue
            self.roots.append(i); stack=[i]; seen.add(i)
            while stack:
                a=stack.pop()
                for j in self.vn[a]:
                    for b in self.rn[j]:
                        if b not in seen: seen.add(b); stack.append(b)

    def lp(self,i,rows,objective=None):
        self.counts['lp_calls']=self.counts.get('lp_calls',0)+1
        d=len(self.case['fs'][i])-1
        vs=lin.vertices(rows,(),d)
        if not vs: return None
        if objective is None: return vs[0]
        return max(vs,key=lambda x:lin.evaluate(objective,x))

    @lru_cache(None)
    def local(self,i,parent):
        rows=list(self.q[i])
        for j in self.vn[i]:
            if j==parent: continue
            children=[self.flags(h,j) for h in self.rn[j] if h!=i]
            if any(a is None for a,b in children): return None
            if not any(b is not None for a,b in children): rows.append(upper_row(self.case,j,i))
        return tuple(rows)

    @lru_cache(None)
    def flags(self,i,parent):
        rows=self.local(i,parent)
        if rows is None: return None,None
        a=self.lp(i,rows)
        if a is None: return None,None
        b=self.lp(i,(*rows,upper_row(self.case,parent,i)))
        return a,b

    def extend(self,i,parent,x,out):
        out[i]=x
        for j in self.vn[i]:
            if j==parent: continue
            children=[h for h in self.rn[j] if h!=i]
            chosen=None
            if lin.evaluate(self.case['gs'][j][i],x)>self.case['his'][j]:
                chosen=next(h for h in children if self.flags(h,j)[1] is not None)
            for h in children: self.extend(h,j,self.flags(h,j)[h==chosen],out)

    def lower(self):
        if self.bad: return None
        best=None; defaults={}
        for i in range(self.n):
            rows=self.local(i,None)
            if rows is None: return None
            f=self.case['fs'][i]
            x=self.lp(i,rows,tuple(-a for a in f))
            if x is None: return None
            defaults[i]=x; val=lin.evaluate(f,x)
            if best is None or val<best[0]: best=(val,i,x)
        val,anchor,x=best; out={}
        self.extend(anchor,None,x,out)
        for root in self.roots:
            if root not in out: self.extend(root,None,defaults[root],out)
        return val,[out[i] for i in range(self.n)]

    def sweep(self,i,thresholds,cap,require):
        if cap==-inf: return dict(value=-inf,x=None)
        rows=list(self.q[i])
        if require is not None: rows.append(upper_row(self.case,require,i))
        for t,j in thresholds:
            if t==-inf: rows.append(upper_row(self.case,j,i))
        f=self.case['fs'][i]; x=self.lp(i,rows,f)
        if x is None: return dict(value=-inf,x=None)
        value=min(cap,lin.evaluate(f,x))
        for t in sorted({t for t,j in thresholds if t!=-inf}):
            if value<=t: break
            previous=x
            rows.extend(upper_row(self.case,j,i) for u,j in thresholds if u==t)
            x=self.lp(i,rows,f)
            value=-inf if x is None else min(cap,lin.evaluate(f,x))
            if value<t: return dict(value=t,x=previous)
        return dict(value=value,x=x)

    @lru_cache(None)
    def caps(self,i,parent):
        cap=inf; thresholds=[]
        for j in self.vn[i]:
            if j==parent: continue
            vals=[self.caps(h,j) for h in self.rn[j] if h!=i]
            cap=min(cap,min((a['value'] for a,b in vals),default=inf))
            thresholds.append((max((b['value'] for a,b in vals),default=-inf),j))
        a=self.sweep(i,thresholds,cap,None)
        b=self.sweep(i,thresholds,cap,parent) if parent is not None else None
        return a,b

    def upper_extend(self,i,parent,need,out):
        result=self.caps(i,parent)[need]; x=result['x']; z=result['value']
        assert x is not None
        out[i]=x
        for j in self.vn[i]:
            if j==parent: continue
            children=[h for h in self.rn[j] if h!=i]; chosen=None
            if lin.evaluate(self.case['gs'][j][i],x)>self.case['his'][j]:
                chosen=next(h for h in children if self.caps(h,j)[1]['value']>=z)
            for h in children: self.upper_extend(h,j,h==chosen,out)

    def upper(self):
        if self.bad: return None
        vals=[self.caps(i,None)[0]['value'] for i in self.roots]
        if min(vals)==-inf: return None
        out={}
        for i in self.roots: self.upper_extend(i,None,False,out)
        return min(vals),[out[i] for i in range(self.n)]

def check_witness(case,xs,target):
    for i,x in enumerate(xs):
        assert all(sum(a*b for a,b in zip(row[:-1],x))<=row[-1] for row in case['bases'][i])
    for j,group in enumerate(case['gs']):
        v=min(lin.evaluate(g,xs[i]) for i,g in group.items())
        assert case['los'][j]<=v<=case['his'][j],(j,v)
    assert min(lin.evaluate(f,x) for f,x in zip(case['fs'],xs))==target

def cycle_range(case,counts=None):
    kept,extra=spanning(case); intervals=[]; witnesses=0; branches=0
    for mask in range(1<<len(extra)):
        selected=[e for j,e in enumerate(extra) if mask&1<<j]
        model=Forest(case,kept,selected,counts=counts); branches+=1
        lower=model.lower(); upper=model.upper()
        assert (lower is None)==(upper is None)
        if lower is None: continue
        lo,xlo=lower; hi,xhi=upper
        assert lo<=hi
        check_witness(case,xlo,lo); check_witness(case,xhi,hi); witnesses+=2
        mid=(lo+hi)/2
        raised=Forest(case,kept,selected,floor=mid,counts=counts).lower()
        assert raised is not None and raised[0]==mid
        check_witness(case,raised[1],mid); witnesses+=1
        intervals.append((lo,hi))
    return dict(ranges=lin.merge(intervals),rank=len(extra),branches=branches,witnesses=witnesses)
