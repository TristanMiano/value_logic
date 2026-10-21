"""Exact finite screen of canonical price-ray policies and staircase warrants."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib
import importlib.util
import json
import random
import time

HERE=Path(__file__).resolve().parent
dep=HERE/'ordered_probe.py'
spec=importlib.util.spec_from_file_location('ray_ordered',dep)
H=importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)
rng=random.Random(202610213)


def main():
    start=time.perf_counter_ns()
    counts=dict(panels=0,price_points=0,chain_actions=0,worlds=0,boxes=0,
                raw_pairs=0,compressed_pairs=0,strict_warrant=0,tied_prices=0)
    for n in (2,3):
        for case in range(12):
            upper=tuple(rng.randrange(1,3) for _ in range(n))
            actions=list(product(*(range(k+1) for k in upper)))
            worlds=list(product(*(range(k+2) for k in upper)))
            source={tuple(rng.randrange(k+1) for k in upper)}
            edges=sorted({tuple(rng.sample(range(n),2)) for _ in range(n)})
            units=[(rng.randrange(n),True)] if case%3==0 else []
            arcs=H.compile_actions(upper,source,edges,units,[])
            allowed=[a for a in actions if H.accepts(a,arcs)]
            assert allowed
            d=[tuple(rng.randrange(-3,4) for _ in range(k)) for k in upper]
            w=[tuple(rng.randrange(0,4) for _ in range(k)) for k in upper]
            lines={a:(sum(sum(d[i][:a[i]]) for i in range(n)),
                      sum(sum(w[i][:a[i]]) for i in range(n))) for a in allowed}
            breaks={F(-3),F(3)}
            for a in allowed:
                for b in allowed:
                    da,wa=lines[a];db,wb=lines[b]
                    if wa!=wb:
                        x=F(da-db,wa-wb)
                        if -3<=x<=3:breaks.add(x)
            points=sorted(breaks)
            points=sorted(set(points+[(a+b)/2 for a,b in zip(points,points[1:])]))
            chain=[]
            for lam in points:
                costs={a:F(da)-lam*wa for a,(da,wa) in lines.items()}
                opt=min(costs.values());ties=[a for a,v in costs.items() if v==opt]
                greatest=tuple(max(a[i] for a in ties) for i in range(n))
                assert greatest in ties
                if chain:assert all(a<=b for a,b in zip(chain[-1],greatest))
                if not chain or greatest!=chain[-1]:chain.append(greatest)
                if len(ties)>1:counts['tied_prices']+=1
                counts['price_points']+=1
            assert len(chain)<=1+sum(upper)
            pairs={}
            for i,j in edges:
                raw={(a[i],a[j]) for a in chain}
                keep={(s,t) for s,t in raw if not any((u>=s and v<=t and (u,v)!=(s,t)) for u,v in raw)}
                assert len(keep)<=min(upper[i]+1,upper[j]+1)
                pairs[i,j]=keep
                counts['raw_pairs']+=len(raw);counts['compressed_pairs']+=len(keep)
            def compact(theta):
                return all(not(theta[i]<=s and theta[j]>t) for (i,j),ps in pairs.items() for s,t in ps) and all(
                    theta[i]<=chain[0][i] if b else theta[i]>chain[-1][i] for i,b in units)
            def box_ok(lo,hi):
                for i,j in edges:
                    first=next((a for a in chain if a[i]>=lo[i]),None)
                    if first is not None and hi[j]>first[j]:return False
                return all(hi[i]<=chain[0][i] if b else lo[i]>chain[-1][i] for i,b in units)
            wray=set()
            for theta in worlds:
                truth=all(H.goal_ok(a,theta,edges,units) for a in chain)
                assert compact(theta)==truth==box_ok(theta,theta)
                if truth:wray.add(theta)
                counts['worlds']+=1
            assert source<=wray
            full={theta for theta in worlds if all(H.goal_ok(a,theta,edges,units) for a in allowed)}
            assert full<=wray
            if full<wray:counts['strict_warrant']+=1
            for _ in range(12):
                endpoints=[sorted(rng.sample(range(k+2),2)) for k in upper]
                lo=tuple(a for a,b in endpoints);hi=tuple(b for a,b in endpoints)
                box=[theta for theta in worlds if all(l<=v<=u for l,v,u in zip(lo,theta,hi))]
                assert box_ok(lo,hi)==all(theta in wray for theta in box)
                counts['boxes']+=1
            counts['panels']+=1;counts['chain_actions']+=len(chain)
    out=dict(status='PASS',contributor='Codex (GPT-6)',seed=202610213,counts=counts,
             elapsed_ns=time.perf_counter_ns()-start,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             dependency_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (dep,H.dependency)},
             scope='Finite exact canonical policy and warrant checks; no parametric solver timing or deployment saving.')
    (HERE/'ray_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()
