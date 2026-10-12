"""Repricing/support repair, exact comparison and finite retention cost."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from flow_repair import repair
from flow_v2 import exact,check


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def main(out):
    assert not out.exists();base=Path(__file__).parent;source=base/'flow01.json';old=json.loads(source.read_text());rng=random.Random(12943);start=time.perf_counter_ns();rows=[]
    for row in old['small_cases']:
        terms0=[(m,F(v)) for m,v in row['terms']];prices0=list(map(F,row['prices']));allocation=[(e,i,F(a)) for e,i,a in row['exact_allocation']]
        terms=[(mask&~(1<<rng.randrange(len(prices0))) if rng.random()<.3 else mask,max(F(0),r+F(rng.randrange(-4,5),16))) for mask,r in terms0]
        prices=[max(F(0),q+F(rng.randrange(-4,5),16)) for q in prices0]
        a,record=repair(terms0,prices0,allocation,terms,prices,fill=True);best,w=exact(terms,prices);oracle=check(terms,prices,best)
        assert oracle['upper']<=record['bound']['upper']<=record['transport_upper']
        rows.append(dict(case=row['case'],terms=terms,prices=prices,repair=record,oracle=oracle,allocation=a))
    row=old['workloads'][0];initial_terms=[(m,F(v)) for m,v in row['terms']];initial_prices=list(map(F,row['prices']))
    begin=time.perf_counter_ns();a,w=exact(initial_terms,initial_prices);check(initial_terms,initial_prices,a);initial_ns=time.perf_counter_ns()-begin
    previous_terms=initial_terms;previous_prices=initial_prices;stages=[]
    for step in range(32):
        terms=[(mask,max(F(0),r+F(rng.randrange(-1,2),64))) for mask,r in previous_terms]
        prices=[max(F(0),q+F(rng.randrange(-1,2),64)) for q in previous_prices]
        begin=time.perf_counter_ns();new_a,record=repair(previous_terms,previous_prices,a,terms,prices,fill=True);repair_ns=time.perf_counter_ns()-begin
        begin=time.perf_counter_ns();best,w=exact(terms,prices);oracle=check(terms,prices,best);exact_ns=time.perf_counter_ns()-begin
        assert oracle['upper']<=record['bound']['upper']
        stages.append(dict(step=step,terms=terms,prices=prices,repair=record,oracle=oracle,repair_and_checks_ns=repair_ns,cold_exact_and_check_ns=exact_ns))
        previous_terms,previous_prices,a=terms,prices,new_a
    a,edge_case=repair([(3,F(1))],[F(3,4),F(1,4)],[(0,0,F(3,4)),(0,1,F(1,4))],[(2,F(1))],[F(0),F(1,4)],fill=True)
    assert edge_case['bound']['upper']==F(3,4)
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=12943,
        sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['flow_repair.py','flow_v2.py','repair_probe.py']},reused_input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        perturbed_cases=rows,sequence_initial_terms=initial_terms,sequence_initial_prices=initial_prices,initial_exact_and_check_ns=initial_ns,sequence=stages,sunk_cost_example=edge_case,elapsed_ns=time.perf_counter_ns()-start,
        limits='Source/graph semantics supplied; repair calls include old/new algebraic checks. Single exposed trace, cold exact comparison; a full incremental residual-flow control is not implemented. No external source-validation/deployment costs.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',cases=len(rows),sequence_steps=len(stages),zero_bounds=sum(r['repair']['bound']['upper']==0 for r in stages),
        repair_total_ns=sum(r['repair_and_checks_ns'] for r in stages),cold_exact_total_ns=sum(r['cold_exact_and_check_ns'] for r in stages),initial_ns=initial_ns,
        max_quality_gap=max(r['repair']['bound']['upper']-r['oracle']['upper'] for r in stages),sunk_cost_upper=edge_case['bound']['upper'],elapsed_ns=result['elapsed_ns']))))


if __name__=='__main__':main(Path(sys.argv[1]))
