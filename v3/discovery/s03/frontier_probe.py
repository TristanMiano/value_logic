"""Targeted sequential repair on reused development inputs, Codex GPT-6."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,sys,time
from frontier_value import frontier


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def main(out):
    assert not out.exists();base=Path(__file__).parent;source=base/'adaptive01.json';old=json.loads(source.read_text());cases=[];start=time.perf_counter_ns()
    part=old['partition_obstruction'];inputs=[('matching',part['polys'],[part['price']]*4,part['oracle']['value'])]
    for i,c in enumerate(old['random_cases'][:6]):inputs.append((f'reused_{i}',c['polys'],c['prices'],c['oracle']['value']))
    for name,raw,prices,truth in inputs:
        polys=[{int(k):F(v) for k,v in p.items()} for p in raw];prices=list(map(F,prices));truth=F(truth);rows=[]
        for kind in ['coefficient','perfect_info','closure']:
            prev=(None,None)
            for depth in range(len(prices)+1):
                begin=time.perf_counter_ns();r=frontier(polys,prices,depth,kind);elapsed=time.perf_counter_ns()-begin
                assert r['lower']<=truth<=r['upper']
                if prev[0] is not None:assert r['lower']>=prev[0] and r['upper']<=prev[1]
                if depth==len(prices):assert r['lower']==r['upper']==truth
                prev=r['lower'],r['upper'];rows.append(dict(kind=kind,depth=depth,result=r,full_call_ns=elapsed))
        cases.append(dict(name=name,polys=polys,prices=prices,truth=truth,stages=rows))
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,
        sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['acquire_flow.py','contrast_plan.py','adaptive_value.py','frontier_value.py','frontier_probe.py']},
        reused_input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),cases=cases,elapsed_ns=time.perf_counter_ns()-start,
        limits='Reused exposed inputs, cold repeated calls by depth, small complete-cost kernel comparison. No optimized caching, external utility service, independent confirmation or generic performance ranking.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',cases=len(cases),matching=[dict(kind=r['kind'],depth=r['depth'],lower=r['result']['lower'],upper=r['result']['upper'],states=r['result']['states'],ns=r['full_call_ns']) for r in cases[0]['stages']],elapsed_ns=result['elapsed_ns']))))


if __name__=='__main__':main(Path(sys.argv[1]))
