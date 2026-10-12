"""Fresh exposed lottery with prospective code prior; not confirmation."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from program_bound import encode,decode,parse,predict,parity_code,table_code,point_bound


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def propose_parity(pairs,dimension):
    for mask in range(1<<dimension):
        for invert in (0,1):
            if all(((mask&x).bit_count()%2^invert)==y for x,y in pairs):return parity_code(mask,dimension,invert)
    raise ValueError('No parity fits')


def main(out):
    assert not out.exists();base=Path(__file__).parent;manifest=json.loads((base/'program01_plan.json').read_text())
    for name,h in manifest['sources'].items():assert hashlib.sha256((base/name).read_bytes()).hexdigest()==h
    begin=time.perf_counter_ns();codes=[]
    for n in range(11):
        for k in range(1<<n):
            payload=format(k,f'0{n}b') if n else ''
            code=encode(payload);assert decode(code)==payload;codes.append(code)
    ordered=sorted(codes);assert all(not b.startswith(a) for a,b in zip(ordered,ordered[1:]))
    kraft=sum(F(1,1<<len(c)) for c in codes);assert kraft<=1
    rng=random.Random(manifest['seed']);d=manifest['dimension'];target=manifest['target_mask'];pairs=[];rows=[]
    truth=lambda x:(target&x).bit_count()%2
    for t in range(1,1025):
        x=rng.randrange(1<<d);pairs.append((x,truth(x)))
        if t not in (16,64,256,1024):continue
        start=time.perf_counter_ns();programs=[('fitted_parity',propose_parity(pairs,d)),('memorized_positive_ids',table_code([x for x,y in pairs if y],d))];proposal_ns=time.perf_counter_ns()-start
        for label,code in programs:
            ast=parse(code,d);start=time.perf_counter_ns();cache={x:int(predict(ast,x)==y) for x,y in pairs};S=F(sum(cache[x] for x,y in pairs));evaluation_ns=time.perf_counter_ns()-start
            true=F(sum(predict(ast,x)==truth(x) for x in range(1<<d)),1<<d)
            before=point_bound(F(0),t,len(code));after=point_bound(S,t,len(code))
            assert before['lower']<=after['lower']<=true
            rows.append(dict(t=t,label=label,code=code,payload_bits=len(decode(code)),description_bits=len(code),partial_sum_before=F(0),evaluated_sum=S,
                unique_evaluation_contexts=len(cache),actual_lottery_occurrences=t,before=before,after=after,diagnostic_population_mean=true,
                proposal_ns_shared_between_two_arms=proposal_ns,evaluation_ns=evaluation_ns))
    thresholds=[]
    for length in (32,128,1024):
        values=[]
        for exponent in range(8,23):
            t=1<<exponent;bound=point_bound(F(11*t,20),t,length)
            values.append(dict(t=t,bound=bound,beats_half=bound['lower']>F(1,2)))
        thresholds.append(dict(length=length,stages=values))
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,
        sources=manifest['sources'],plan_sha256=hashlib.sha256((base/'program01_plan.json').read_bytes()).hexdigest(),
        prefix_codes_checked=len(codes),partial_kraft_sum=kraft,seed=manifest['seed'],dimension=d,target_mask=target,sampled_pairs=pairs,
        stages=rows,idealized_margin_thresholds=thresholds,elapsed_ns=time.perf_counter_ns()-begin,
        limits='Supplied deterministic parity classification, no deployment costs or external evaluator. One path, selected posterior programs, primary theorem imported; finite bound checks do not establish coverage.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',prefix_codes=len(codes),stages=[{k:r[k] for k in ['t','label','description_bits','diagnostic_population_mean']}|{'lower':r['after']['lower']} for r in rows],
        margin_thresholds=[dict(length=x['length'],first_t=next((r['t'] for r in x['stages'] if r['beats_half']),None)) for x in thresholds],elapsed_ns=result['elapsed_ns']))))


if __name__=='__main__':main(Path(sys.argv[1]))
