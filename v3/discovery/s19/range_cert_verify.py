"""Exact certificate verifier for anchored scalar ranges; no optimization oracle."""
from fractions import Fraction
import hashlib, json, math


def require(ok,message):
    if not ok: raise ValueError(message)

def digest(problem):
    return hashlib.sha256(json.dumps(problem,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def rational(value):
    require(isinstance(value,str),'rational must be an exact string')
    return Fraction(value)

def vector(values,n):
    require(isinstance(values,list) and len(values)==n,'vector shape')
    return [rational(v) for v in values]

def dot(a,b):
    require(len(a)==len(b),'dot shape')
    return sum((x*y for x,y in zip(a,b)),Fraction(0))

def constraints(problem,i,mask):
    gs=problem['generators']; g=gs[i]; n=len(g['c'])
    require(n>=1,'positive dimension')
    c=vector(g['c'],n); d=rational(g['d'])
    rows=[vector(row,n) for row in g['A']]; rhs=vector(g['b'],len(rows))
    for j,r in enumerate(problem['receipts']):
        lo=rational(r['lo']); hi=rational(r['hi'])
        require(lo<=hi and len(r['forms'])==len(gs),'receipt contract')
        form=r['forms'][i]; h=vector(form['c'],n); off=rational(form['d'])
        rows.append([-v for v in h]); rhs.append(off-lo)
        if mask>>j&1: rows.append(h); rhs.append(hi-off)
    return rows,rhs,c,d

def check_dual(rows,rhs,weights,target):
    z=vector(weights,len(rows))
    require(all(v>=0 for v in z),'negative multiplier')
    require(all(sum((z[j]*rows[j][h] for j in range(len(rows))),Fraction(0))==target[h]
                for h in range(len(target))),'dual coefficient identity')
    return dot(z,rhs)

def normalize(intervals):
    out=[]
    for a,b in sorted(intervals):
        require(a<=b,'reversed interval')
        if out and a<=out[-1][1]: out[-1]=(out[-1][0],max(b,out[-1][1]))
        else: out.append((a,b))
    return out

def advance(prev,table,k):
    out={}
    for s in range(1<<k):
        t=s; best=-math.inf
        while True:
            if t in table and (s^t) in prev: best=max(best,min(table[t][1],prev[s^t]))
            if t==0: break
            t=(t-1)&s
        if best!=-math.inf: out[s]=best
    return out

def whole_range(tables,k):
    n=len(tables); full=(1<<k)-1
    p=[{0:math.inf}]
    for table in tables: p.append(advance(p[-1],table,k))
    s=[None]*(n+1); s[n]={0:math.inf}
    for i in range(n-1,-1,-1): s[i]=advance(s[i+1],tables[i],k)
    intervals=[]
    for i,table in enumerate(tables):
        for t,(lo,hi) in table.items():
            outside=full^t; a=outside; cap=-math.inf
            while True:
                if a in p[i] and (outside^a) in s[i+1]:
                    cap=max(cap,min(p[i][a],s[i+1][outside^a]))
                if a==0: break
                a=(a-1)&outside
            if lo<=min(hi,cap): intervals.append((lo,min(hi,cap)))
    return normalize(intervals)

def verify(problem,certificate):
    require(set(problem)=={'generators','receipts'},'problem fields')
    require(set(certificate)=={'problem_sha256','faces','ranges'},'certificate fields')
    require(certificate['problem_sha256']==digest(problem),'problem digest mismatch')
    n=len(problem['generators']); k=len(problem['receipts'])
    require(n>=1 and len(certificate['faces'])==n,'generator count')
    tables=[]; bounded=0; infeasible=0; dual_entries=0
    for i,faces in enumerate(certificate['faces']):
        require(len(faces)==1<<k,'missing or extra face')
        table={}
        for mask,entry in enumerate(faces):
            rows,rhs,c,d=constraints(problem,i,mask)
            if entry['kind']=='empty':
                require(set(entry)=={'kind','dual'},'infeasible fields')
                value=check_dual(rows,rhs,entry['dual'],[Fraction(0)]*len(c))
                require(value<0,'nonnegative infeasibility bound')
                infeasible+=1; dual_entries+=len(rows)
            elif entry['kind']=='bounded':
                require(set(entry)=={'kind','lo','hi','xlo','xhi','dlo','dhi'},'bounded fields')
                lo=rational(entry['lo']); hi=rational(entry['hi'])
                require(lo<=hi,'extrema order')
                a=vector(entry['xlo'],len(c)); b=vector(entry['xhi'],len(c))
                require(all(dot(row,a)<=r and dot(row,b)<=r for row,r in zip(rows,rhs)),'primal infeasible')
                require(dot(c,a)+d==lo and dot(c,b)+d==hi,'primal objective')
                low=check_dual(rows,rhs,entry['dlo'],[-v for v in c])
                high=check_dual(rows,rhs,entry['dhi'],c)
                require(-low+d==lo and high+d==hi,'dual objective')
                table[mask]=(lo,hi); bounded+=1; dual_entries+=2*len(rows)
            else: raise ValueError('unknown face kind')
        tables.append(table)
    claimed=[]
    for row in certificate['ranges']:
        require(isinstance(row,list) and len(row)==2,'range shape')
        claimed.append((rational(row[0]),rational(row[1])))
    require(claimed==normalize(claimed),'range list not normalized')
    answer=whole_range(tables,k)
    require(claimed==answer,'whole range mismatch')
    return dict(status='VERIFIED' if answer else 'INCONSISTENT_SOURCE',problem_sha256=digest(problem),
                ranges=[[str(a),str(b)] for a,b in answer],bounded_faces=bounded,
                infeasible_faces=infeasible,dual_entries=dual_entries)
