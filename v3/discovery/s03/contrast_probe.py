"""Explicit-world VOI comparison and sparse high-degree examples; DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from contrast_plan import evsi,plan,expected_absolute


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def worlds_voi(poly,m,bits):
    groups={};totals=[F(0),F(0)]
    for x in range(1<<m):
        d=sum(a*(-1 if (mask&x).bit_count()%2 else 1) for mask,a in poly.items())
        y=[(1-d)/2,(1+d)/2];key=x&bits
        if key not in groups:groups[key]=[F(0),F(0)]
        for i in range(2):groups[key][i]+=y[i];totals[i]+=y[i]
    return (sum(max(row) for row in groups.values())-max(totals))/(1<<m)


def main(out):
    assert not out.exists();rng=random.Random(72314);start=time.perf_counter_ns();rows=[];checks=0
    for case in range(60):
        m=rng.randrange(1,7);k=rng.randrange(1,min(8,1<<m));poly={}
        for _ in range(k):
            mask=rng.randrange(1<<m);poly[mask]=poly.get(mask,F(0))+F(rng.randrange(-4,5),4*k)
        poly={mask:a for mask,a in poly.items() if a};prices=[F(rng.randrange(1,9),64) for _ in range(m)]
        candidates=[]
        for B in range(1<<m):
            a,r=evsi(poly,B);b=worlds_voi(poly,m,B);assert a==b
            net=b-sum(q for i,q in enumerate(prices) if B&(1<<i));candidates.append(net);checks+=1
        chosen=plan(poly,prices);assert chosen['net']==max(candidates)
        rows.append(dict(case=case,m=m,poly=poly,prices=prices,plan=chosen,world_optimum=max(candidates)))
    examples=[]
    for label,poly,prices in [
        ('64_bit_parity',{(1<<64)-1:F(1)},[F(1,256)]*64),
        ('common_value_cancels',{},[F(1,64)]*64),
        ('dominant_offset',{0:F(3,4),15:F(1,4)},[F(1,64)]*4)]:
        a=time.perf_counter_ns();p=plan(poly,prices);elapsed=time.perf_counter_ns()-a
        examples.append(dict(label=label,poly=poly,prices=prices,plan=p,elapsed_ns=elapsed))
    basis=[(1<<20)-1,((1<<20)-1)<<20,((1<<24)-1)<<40];poly={}
    for c in range(1,8):
        mask=0
        for i in range(3):
            if c&(1<<i):mask^=basis[i]
        poly[mask]=F((-1)**c,8)
    a=time.perf_counter_ns();p=plan(poly,[F(1,512)]*64);elapsed=time.perf_counter_ns()-a
    examples.append(dict(label='rank_three_64_bits',poly=poly,prices=[F(1,512)]*64,plan=p,elapsed_ns=elapsed))
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=72314,
        sources={p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ['acquire_flow.py','contrast_plan.py','contrast_probe.py']},
        cases=rows,explicit_world_batch_checks=checks,examples=examples,elapsed_ns=time.perf_counter_ns()-start,
        limits='Uniform independent prior is supplied, costs are rational tariffs, pure observations assumed. Native primitive evaluation and source acquisition absent; no external economic or confirmation claim.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',cases=len(rows),explicit_world_batch_checks=checks,examples=[dict(label=e['label'],plan=e['plan'],elapsed_ns=e['elapsed_ns']) for e in examples],elapsed_ns=result['elapsed_ns']))))


if __name__=='__main__':main(Path(sys.argv[1]))
