#!/usr/bin/env python3
"""Compulsory-pair calibration with exact policy-cell stopping. DEVELOPMENT.
Codex (GPT-6), 2026-10-14. Reuses exposed ms01 rows as a controlled ablation.
"""
from collections import Counter
from datetime import datetime,timezone
from fractions import Fraction as F
from functools import reduce
from pathlib import Path
import json
import math
import sys
import time
import g01
import action_audits as aa
import star_learning as base
import markov_paths as mk
import markov_service as ms
import model_cells as cells

HERE=Path(__file__).resolve().parent
VERSION='s08-pair-learning-v1'
ARMS=tuple(f'{method}_{stop}' for method in ('hoeffding','mixture') for stop in ('cell','ordinary_cell','singleton'))
Meter=g01.kernel.Meter


def run_arm(directory,case,data,rows,arm):
    cpu=time.process_time_ns();wall=time.perf_counter_ns();meter=Meter();ms.admit(data,meter)
    bank,values,supports,bank_hash=cells.prepare(directory,f"{case['name']}_{arm}",data,meter);setup=meter.total
    active=set(mk.MENU);weights=[1]*len(mk.MENU);samples=success=fees=audits=failures=0
    selected=Counter();changes=[];frozen=None;stop_row=None;maximum_bits=1;eligible_pairs=0;coverage_failures=0
    trace_path=directory/f"{case['name']}_{arm}.jsonl";diag_path=directory/f"{case['name']}_{arm}_diag.jsonl"
    with trace_path.open('w',encoding='utf-8') as trace,diag_path.open('w',encoding='utf-8') as diag:
        trace.write(json.dumps(dict(kind='header',source=data['identity'],version=VERSION,arm=arm,bank_sha256=bank_hash))+'\n');trace.flush()
        for t,row in enumerate(rows):
            before=meter.total
            if frozen is None:
                eligible=[r for r in bank if active<=supports[r]]
                meter.pay('selection','check_common_minimizing_policy_cells',len(bank)*len(active))
                may_stop=bool(eligible) and ('singleton' not in arm or len(active)==1)
                if may_stop:
                    frozen=min(eligible);stop_row=t
                    trace.write(json.dumps(dict(kind='stop_learning',before_request=t,source=data['identity'],
                        bank_sha256=bank_hash,active=sorted(active),selected=frozen,support=sorted(supports[frozen])))+'\n')
                    meter.pay('selection','retain_source_bound_stopping_certificate',12+len(active))
            if frozen is None:
                r=min(bank,key=lambda k:(max(values[k][q] for q in active),k))
                meter.pay('selection','minimize_largest_retained_model_invoice',2*len(bank)*len(active))
            else:r=frozen;meter.pay('selection','reuse_frozen_policy',1)
            bound=max(values[r][q] for q in active);selected[str(r)]+=1;request=f"{case['name']}-{arm}-{t}"
            trace.write(json.dumps(dict(kind='plan',request=request,selected_model_policy=r,active=sorted(active),
                expected_fee_bound=bound,learning_frozen=frozen is not None),default=g01.encode,separators=(',',':'))+'\n');trace.flush()
            provider=base.Provider(data,row,request,trace,meter)
            receipts=ms.acquire(provider,data['n'],bank[r]['roots'],meter)
            action=base.construct(data,receipts,request,meter);base.check(data,receipts,action,meter)
            paid=sum(r['base_fee'] for r in receipts);fees+=paid;audits+=len(receipts)
            trace.write(json.dumps(dict(kind='output',request=request,action=action,base_fee=paid,
                physical_audits=len(receipts),named_units=meter.total-before),separators=(',',':'))+'\n');trace.flush()
            regret=aa.direct_regret(data,action['assignment'],row);assert regret==0
            covered=case['r'] in active;coverage_failures+=not covered
            diag.write(json.dumps(dict(request=t,hidden=row,regret=regret,true_model_retained_before=covered),separators=(',',':'))+'\n')
            if receipts[0]['value']==1:
                assert len(receipts)>=2 and abs(receipts[0]['node']-receipts[1]['node'])==1
                eligible_pairs+=1
                if frozen is None:
                    repeat=int(receipts[1]['value']==1);samples+=1;success+=repeat;old=active.copy()
                    meter.pay('learning','extract_forced_receipt_pair_and_count',8)
                    if arm.startswith('hoeffding'):
                        lower,upper=base.confidence(samples,success,1,meter)
                        retained={q for q in mk.MENU if lower<=F(q,10)<=upper}
                        state=dict(samples=samples,repeats=success,interval=[lower,upper])
                        meter.pay('learning','intersect_finite_menu_with_interval',2*len(mk.MENU))
                    else:
                        weights=[w*(q if repeat else 10-q) for q,w in zip(mk.MENU,weights)]
                        divisor=reduce(math.gcd,weights);weights=[w//divisor for w in weights];total=sum(weights)
                        retained={q for q,w in zip(mk.MENU,weights) if 100*w>=total}
                        bits=max(w.bit_length() for w in weights);maximum_bits=max(maximum_bits,bits)
                        state=dict(samples=samples,repeats=success,weights_hex=[hex(w) for w in weights])
                        meter.pay('learning','integer_bernoulli_weights_gcd_and_set_check',sum(w.bit_length() for w in weights)+10*len(weights))
                    active &=retained
                    if not active:failures+=1;active=set(mk.MENU)
                    if old!=active:changes.append(dict(after_request=t,samples=samples,active=sorted(active)))
                    trace.write(json.dumps(dict(kind='pair_update',request=t,first_receipt=receipts[0]['identity'],
                        next_receipt=receipts[1]['identity'],active=sorted(active),empty_set_fallbacks=failures,**state),
                        default=g01.encode,separators=(',',':'))+'\n');trace.flush()
    return dict(outputs=len(rows),physical_audits=audits,base_audit_fee=fees,named_units=meter.total,setup_units=setup,
        invoice=meter.record(),selected_policies=dict(selected),model_set_changes=changes,final_active=sorted(active),
        eligible_pairs=eligible_pairs,learning_samples=samples,repeats=success,stop_before_request=stop_row,
        confidence_failures=failures,observed_coverage_failures=coverage_failures,max_weight_bits=maximum_bits,
        trace_bytes=trace_path.stat().st_size,diagnostic_bytes=diag_path.stat().st_size,
        arm_cpu_ns=time.process_time_ns()-cpu,arm_wall_ns=time.perf_counter_ns()-wall,
        timing_scope='Own preparation, execution, learning, trace export and diagnostics; shared row generation and outer packaging excluded')


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    prior=json.loads((HERE/'ms01/design.json').read_text());cases=prior['cases']
    g01.save(directory/'design.json',dict(version=VERSION,stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,requests=256,arms=ARMS,
        exposure='Same rows as ms01; mechanism ablation, no independent confirmation',
        public_sources=[ms.source(c['costs']) for c in cases],source_sha256=g01.sha(__file__),
        declaration_sha256=g01.sha(HERE/'forced_calibration.md'),
        dependencies={name:g01.sha(HERE/name) for name in ('model_cells.py','markov_service.py','markov_paths.py','star_learning.py','action_audits.py','g01.py')}))
    result=dict(status='running',cases=[])
    for case in cases:
        data=ms.source(case['costs']);rows=ms.draw(data['n'],case['r'],256,case['seed']);record=dict(name=case['name'],arms={})
        for arm in ARMS:
            record['arms'][arm]=run_arm(directory,case,data,rows,arm)
            g01.save(directory/'progress.json',dict(completed=result['cases'],current=record))
        for method in ('hoeffding','mixture'):
            for key in ('physical_audits','base_audit_fee','named_units','selected_policies','model_set_changes','final_active','learning_samples','stop_before_request'):
                assert record['arms'][method+'_cell'][key]==record['arms'][method+'_ordinary_cell'][key]
        result['cases'].append(record);g01.save(directory/'results.json',result)
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat())
    g01.save(directory/'results.json',result)
    print(json.dumps(dict(status='complete',cases=[dict(name=c['name'],arms={a:{k:v[k] for k in
        ('base_audit_fee','named_units','learning_samples','stop_before_request','final_active','observed_coverage_failures')}
        for a,v in c['arms'].items()}) for c in result['cases']])))


if __name__=='__main__':run(Path(sys.argv[1]))
