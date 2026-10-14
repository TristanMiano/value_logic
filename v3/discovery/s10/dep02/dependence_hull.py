"""Finite three-score marginal-coupling certificates; Codex (GPT-6)."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json, hashlib, time
ROOT=Path(__file__).resolve().parent
D=24001; P=(9000,9000,6001); Q=6
def enc(x): return [x.numerator,x.denominator]
def solve(k):
    if k==0:
        return {"k":0,"upper":[1,1],"primal":[{"state":[0,0],"weight":[1,1]}],"dual":[[1,1],[0,1],[0,1]],"bases":0,"named_units":8}
    raw=[(a,b,int(a+2*b<Q)) for a in range(k+1) for b in range(k-a+1)]
    hull_units=6*len(raw);states=[]
    def cross(o,a,b):
        nonlocal hull_units
        hull_units+=8
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    for event in [0,1]:
        points=sorted(x for x in raw if x[2]==event)
        hull_units+=len(points)*max(1,len(points).bit_length())
        if len(points)<=1:
            states+=points
            continue
        low=[];high=[]
        for pt in points:
            while len(low)>=2 and cross(low[-2],low[-1],pt)<=0:low.pop()
            low.append(pt)
        for pt in reversed(points):
            while len(high)>=2 and cross(high[-2],high[-1],pt)<=0:high.pop()
            high.append(pt)
        states+=low[:-1]+high[:-1]
    states=sorted(set(states));hull_units+=8*len(states)
    best=F(-1); primal=None; dual=None; bases=0; checks=0
    for x,y,z in combinations(states,3):
        a,b,c=y[0]-x[0],y[1]-x[1],z[0]-x[0]
        e=z[1]-x[1]; det=a*e-b*c
        if det==0: continue
        bases+=1
        mx,my=k*P[1]-D*x[0],k*P[2]-D*x[1]
        v=mx*e-my*c; w=a*my-b*mx; u=D*det-v-w; denom=D*det
        if denom<0: u,v,w,denom=-u,-v,-w,-denom
        if min(u,v,w)<0: continue
        score=F(u*x[2]+v*y[2]+w*z[2],denom)
        if score<best: continue
        beta=F((y[2]-x[2])*e-(z[2]-x[2])*b,det)
        gamma=F(a*(z[2]-x[2])-c*(y[2]-x[2]),det)
        alpha=F(x[2])-beta*x[0]-gamma*x[1]
        checks+=len(states)
        feasible=all(alpha+beta*i+gamma*j>=t for i,j,t in states)
        if score>best:
            best=score;primal=[{"state":[s[0],s[1]],"weight":enc(F(n,denom))} for s,n in zip((x,y,z),(u,v,w))];dual=None
        if feasible: dual=[enc(alpha),enc(beta),enc(gamma)]
    assert dual is not None
    return {"k":k,"upper":enc(best),"primal":primal,"dual":dual,"bases":bases,"dual_state_checks":checks,"named_units":hull_units+30*bases+8*checks+20*len(states)}
def main():
    out=ROOT/"dep02";out.mkdir()
    files=["dependence_hull.py","dependent_scores.md","dependence_hulls.md"]
    design={"contributor":"Codex (GPT-6)","created_utc":time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),"stage":"DEVELOPMENT","quota":Q,"marginals":P,"denominator":D,"lengths":list(range(13)),"hashes":{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}}
    (out/"design.json").write_text(json.dumps(design,indent=2)+'\n')
    for f in files:(out/f).write_bytes((ROOT/f).read_bytes())
    rows=[]
    for k in range(13):
        row=solve(k);rows.append(row)
        (out/f"k{k:02}.json").write_text(json.dumps(row,indent=2)+'\n')
        print(k,float(F(*row["upper"])),row["named_units"],flush=True)
    (out/"results.json").write_text(json.dumps({"status":"pass","rows":rows,"named_units":sum(r["named_units"] for r in rows),"physical_acquisitions":0,"unknown_costs":["Python/runtime","complete economic tariffs"]},indent=2)+'\n')
if __name__=='__main__':main()
