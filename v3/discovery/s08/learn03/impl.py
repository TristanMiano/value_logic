#!/usr/bin/env python3
"""Development ablation: persist and reuse a stationary probability certificate.
Codex (GPT-6), 2026-10-14. Prior exposed rows; not confirmation.
"""
from collections import Counter
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import time
import g01
import star_learning as base

HERE=Path(__file__).resolve().parent
VERSION='s08-star-epoch-v2'


def arm(directory,case,data,rows,name):
    meter=base.Meter();base.admit(data,meter);setup=meter.total
    trace_path=directory/f"{case['name']}_{name}.jsonl";diag_path=directory/f"{case['name']}_{name}_diag.jsonl"
    counts=[0]*data['n'];successes=[0]*data['n'];fees=audits=epochs=0;routes=Counter();switches=[];previous=None
    cpu=time.process_time_ns();wall=time.perf_counter_ns();certificate=None
    with trace_path.open('w',encoding='utf-8') as trace,diag_path.open('w',encoding='utf-8') as diag:
        trace.write(json.dumps(dict(kind='header',version=VERSION,source=data['identity'],arm=name))+'\n');trace.flush()
        for k,row in enumerate(rows):
            before=meter.total
            if k==0 or k&(k-1)==0:
                decision=base.select(data['audit_costs'],counts,successes,meter)
                certificate=g01.seal(json.loads(json.dumps(dict(source=data['identity'],created_request=k,
                    counts=counts.copy(),successes=successes.copy(),decision=decision,
                    validity='Stationary admitted product source, common all-count confidence event'),default=g01.encode)))
                trace.write(json.dumps(dict(kind='probability_certificate',certificate=certificate),default=g01.encode,separators=(',',':'))+'\n');trace.flush()
                meter.pay('certificate','construct_bind_and_export_words',16+6*data['n']);epochs+=1
            if certificate['source']!=data['identity']:raise ValueError('Stale source certificate')
            # Keep the live exact-rational decision; certificate hashes its canonical export.
            meter.pay('planning','check_certificate_binding_and_dispatch',7)
            if previous!=decision['route']:switches.append(dict(request=k,route=decision['route']));previous=decision['route']
            request=f"{case['name']}-{name}-{k}"
            trace.write(json.dumps(dict(kind='plan',request=request,certificate=certificate['identity']),separators=(',',':'))+'\n');trace.flush()
            provider=base.Provider(data,row,request,trace,meter)
            receipts=base.purchase(provider,decision,data['n']);action=base.construct(data,receipts,request,meter);base.check(data,receipts,action,meter)
            paid=sum(r['base_fee'] for r in receipts);fees+=paid;audits+=len(receipts);routes[decision['route']]+=1
            trace.write(json.dumps(dict(kind='output',request=request,action=action,physical_audits=len(receipts),base_fee=paid,named_units=meter.total-before),separators=(',',':'))+'\n');trace.flush()
            regret=base.aa.direct_regret(data,action['assignment'],row);assert regret==0
            covers=all(lo<=p<=hi for (lo,hi),p in zip(decision['intervals'],case['p']))
            diag.write(json.dumps(dict(request=k,hidden=row,regret=regret,confidence_covers_truth=covers),separators=(',',':'))+'\n')
            for receipt in receipts:
                i=receipt['node'];counts[i]+=1;successes[i]+=receipt['value']!=1
                meter.pay('learning','update_acquired_extreme_indicator',4)
    return dict(outputs=len(rows),physical_audits=audits,base_audit_fee=fees,named_units=meter.total,
        setup_units=setup,invoice=meter.record(),routes=dict(routes),switches=switches,epochs=epochs,
        counts=counts,successes=successes,last_certificate=certificate,
        trace_bytes=trace_path.stat().st_size,diagnostic_bytes=diag_path.stat().st_size,
        arm_cpu_ns=time.process_time_ns()-cpu,arm_wall_ns=time.perf_counter_ns()-wall,
        timing_scope='Complete arm including exports and diagnostics; not isolated solver speed')


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    old=json.loads((HERE/'learn01'/'design.json').read_text())
    cases=[dict(c,p=list(map(F,c['p']))) for c in old['cases']]
    g01.save(directory/'design.json',dict(version=VERSION,stage='DEVELOPMENT_EXPOSED_ABLATION',
        contributor='Codex (GPT-6)',created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,
        requests=old['requests_per_case'],arms=['epoch_learner','ordinary_epoch_learner'],
        prior_design_sha256=g01.sha(HERE/'learn01'/'design.json'),
        source_sha256=g01.sha(__file__),base_sha256=g01.sha(HERE/'star_learning.py'),
        declaration_sha256=g01.sha(HERE/'learning_epochs.md')))
    result=dict(status='running',cases=[])
    for case in cases:
        data=base.source(case['costs']);rows=base.environment_rows(case['p'],old['requests_per_case'],case['seed'])
        record=dict(name=case['name'],arms={})
        for name in ('epoch_learner','ordinary_epoch_learner'):
            record['arms'][name]=arm(directory,case,data,rows,name)
            g01.save(directory/'progress.json',dict(completed=result['cases'],current=record))
        for key in ('base_audit_fee','physical_audits','named_units','counts','successes','routes'):
            assert record['arms']['epoch_learner'][key]==record['arms']['ordinary_epoch_learner'][key]
        result['cases'].append(record);g01.save(directory/'results.json',result)
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat())
    g01.save(directory/'results.json',result)
    print(json.dumps(dict(status=result['status'],cases=[dict(name=c['name'],result={k:c['arms']['epoch_learner'][k]
        for k in ('outputs','physical_audits','base_audit_fee','named_units','epochs','routes','switches','trace_bytes')}) for c in result['cases']]),default=g01.encode))


if __name__=='__main__':run(Path(sys.argv[1]))
