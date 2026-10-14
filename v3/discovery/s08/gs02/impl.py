"""Improved ordinary graph service. Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import time
import graph_incremental as inc
ga=inc.ga;gs=inc.gs;g01=ga.g01;base=ga.base;Meter=ga.Meter
HERE=Path(__file__).resolve().parent

def run(directory,case,arm):
    data=ga.source(case['costs'],case['edges']);g01.save(directory/'source.json',data)
    meter=Meter();ga.admit(data,meter);adj=inc.adjacency(data,meter)
    static=None
    if arm=='greedy':static=ga.primal_dual(data,meter);ga.check_dual(data,static,meter)
    g01.save(directory/'static.json',static);setup=meter.total;fee=audits=0;ratios=[];lower_sum=0
    start=time.perf_counter_ns();cpu=time.process_time_ns()
    with(directory/'trace.jsonl').open('w') as trace,(directory/'diagnostics.jsonl').open('w') as diag:
        trace.write(json.dumps(dict(kind='header',source=data['identity'],arm=arm))+'\n');trace.flush()
        for t,row in enumerate(gs.rows(data['n'],case['seed'])):
            before=meter.total;request=f"{case['name']}-{arm}-{t}";receipts=[]
            provider=base.Provider(data,row,request,trace,meter)
            def get(i):
                r=provider.audit(i);receipts.append(r);return r['value']
            if arm=='greedy':known=inc.greedy(data,adj,get,meter);plan=static
            elif arm in('adaptive_dual','ordinary_adaptive'):known,plan=inc.adaptive_dual(data,adj,get,meter)
            else:raise ValueError(arm)
            action=base.construct(data,receipts,request,meter);base.check(data,receipts,action,meter)
            cert=ga.lower_certificate(data,plan,known,meter);lower=ga.check_lower(data,plan,receipts,request,cert,meter)
            paid=sum(r['base_fee'] for r in receipts)
            if arm!='greedy' and paid>2*lower:raise ValueError('Two-factor certificate failed')
            ratio=F(paid,lower) if lower else F(1);ratios.append(ratio);lower_sum+=lower;fee+=paid;audits+=len(receipts)
            meter.pay('export','action_and_cost_certificate_words',20+len(action['selected'])+len(cert['mandatory'])+(len(plan['dual']) if arm!='greedy' else 0))
            trace.write(json.dumps(dict(kind='output',request=request,action=action,certificate=cert,dual=plan if arm!='greedy' else None,
                base_fee=paid,physical_audits=len(receipts),checked_fee_ratio=ratio,named_units=meter.total-before),default=g01.encode,separators=(',',':'))+'\n');trace.flush()
            assert ga.aa.direct_regret(data,action['assignment'],row)==0
            diag.write(json.dumps(dict(request=request,hidden=row,regret=0))+'\n')
    result=dict(outputs=32,base_audit_fee=fee,physical_audits=audits,named_units=meter.total,setup_units=setup,
        lower_bound_sum=lower_sum,aggregate_checked_ratio=F(fee,lower_sum),max_checked_ratio=max(ratios),
        invoice=meter.record(),trace_bytes=(directory/'trace.jsonl').stat().st_size,diagnostic_bytes=(directory/'diagnostics.jsonl').stat().st_size,
        arm_cpu_ns=time.process_time_ns()-cpu,arm_wall_ns=time.perf_counter_ns()-start)
    g01.save(directory/'result.json',result)

if __name__=='__main__':
    directory=Path(sys.argv[1]);directory.mkdir(exist_ok=False);design=json.loads(Path(sys.argv[2]).read_text())
    if g01.sha(__file__)!=design['source_sha256']:raise ValueError('Changed service')
    for name,digest in design['dependencies'].items():
        if g01.sha(HERE/name)!=digest:raise ValueError('Changed dependency '+name)
    case=next(c for c in design['cases'] if c['name']==sys.argv[3]);run(directory,case,sys.argv[4])
