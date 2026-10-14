#!/usr/bin/env python3
"""Paid partial-observation Markov model selection. DEVELOPMENT.
Codex (GPT-6), 2026-10-14. Exact output checks do not trust the learned model.
"""
from collections import Counter
from datetime import datetime,timezone
from fractions import Fraction as F
from functools import reduce
from pathlib import Path
import json
import math
import random
import sys
import time
import g01
import action_audits as aa
import star_learning as base
import markov_paths as mk

HERE=Path(__file__).resolve().parent
VERSION='s08-markov-service-v1'
ARMS=('full','independent','robust_menu','learner','ordinary_learner','oracle')
Meter=g01.kernel.Meter


def source(costs):
    data=aa.original([[i,i+1,1] for i in range(len(costs)-1)],costs)
    data.pop('identity');data['bit_source']='Fresh symmetric Markov indicator rows; one fixed unknown menu member'
    data['alphabet']=[0,1,2];data['repeat_numerators']=list(mk.MENU)
    return g01.seal(data)


def admit(data,meter):
    if data!=source(data['audit_costs']):raise ValueError('Original path source mismatch')
    if any(type(c)is not int or c<=0 for c in data['audit_costs']):raise ValueError('Invalid audit fees')
    meter.pay('source','read_original_factors_fee_map_and_finite_model_menu',
        24+len(data['audit_costs'])+sum(1+len(c) for c in data['hard'])+5*len(data['features']))


def check_policy(data,r,policy):
    """Verify upper inequalities using independently multiplied transition matrices."""
    meter=Meter();costs=data['audit_costs'];n=data['n']
    if r not in data['repeat_numerators'] or policy['n']!=n or policy['r']!=r:raise ValueError('Policy/model binding')
    matrix=[[r,10-r],[10-r,r]];powers=[[[1,0],[0,1]]]
    for d in range(1,n+1):
        prior=powers[-1]
        powers.append([[sum(prior[a][k]*matrix[k][b] for k in range(2)) for b in range(2)] for a in range(2)])
        meter.pay('proof_check','transition_matrix_multiplication',12)
    def probability(a,b,mode,i):
        if a==0:left=[1,1]
        else:left=powers[i-a+1][int(mode=='left')]
        if b==n-1:right=[1,1]
        else:right=[powers[b-i+1][v][int(mode=='right')] for v in range(2)]
        numerator=left[0]*right[0];denominator=numerator+left[1]*right[1]
        meter.pay('proof_check','boundary_message_normalization',7)
        return F(numerator,denominator)
    states={(a,b) for a in range(n) for b in range(a,n)};tables=policy['tables']
    if set(tables)!= {'ordinary','left','right'} or set(policy['roots'])!={(a,b) for a,b in states if a<b}:raise ValueError('Policy state scope')
    for table in tables.values():
        if set(table)!=states or any(type(x) not in (int,F) or x<0 for x in table.values()):raise ValueError('Invalid certificate entries')
    def at(kind,a,b):return tables[kind][a,b] if a<=b else F(0)
    for a,b in states:
        terms=[('left',a,at('ordinary',a+1,b),at('left',a+1,b)),('right',b,at('ordinary',a,b-1),at('right',a,b-1))]
        if a==b:
            if tables['ordinary'][a,b]!=0:raise ValueError('Ordinary singleton must stop')
        else:
            i=policy['roots'][a,b]
            if type(i)is not int or not a<=i<=b:raise ValueError('Invalid root')
            terms.append(('ordinary',i,at('ordinary',a,i-1)+at('ordinary',i+1,b),at('right',a,i-1)+at('left',i+1,b)))
        for mode,i,extreme,middle in terms:
            p=probability(a,b,mode,i)
            if tables[mode][a,b]<costs[i]+p*extreme+(1-p)*middle:raise ValueError('Underestimated Markov continuation')
            meter.pay('proof_check','selected_policy_upper_inequality',7)
    if policy['bound']!=tables['ordinary'][0,n-1]:raise ValueError('Root invoice mismatch')
    return meter.record()


def prepare(directory,label,data,arm,true_r,meter):
    if arm=='full':return {},{}
    proposal_models=list(mk.MENU) if arm in ('robust_menu','learner','ordinary_learner') else [true_r if arm=='oracle' else 5]
    evaluated_models=list(mk.MENU) if arm in ('robust_menu','learner','ordinary_learner') else proposal_models
    bank={};values={};certificates={}
    for r in proposal_models:
        bank[r]=mk.plan(data['audit_costs'],r)
        meter.pay('preparation','optimal_model_root_policy',bank[r]['invoice']['total'])
        values[r]={};certificates[r]={}
        for q in evaluated_models:
            evaluated=mk.plan(data['audit_costs'],q,bank[r]['roots'])
            checked=check_policy(data,q,evaluated)
            meter.pay('preparation','cross_model_policy_evaluation',evaluated['invoice']['total'])
            meter.pay('preparation','independent_upper_certificate_check',checked['total'])
            values[r][q]=evaluated['bound'];certificates[r][q]=dict(policy=mk.export(evaluated),checking=checked)
    g01.save(directory/f'{label}_{arm}_bank.json',dict(source=data['identity'],values=values,certificates=certificates))
    return bank,values


def acquire(provider,n,roots,meter):
    if roots is None:return [provider.audit(i) for i in range(n)]
    tasks=[('ordinary',0,n-1)];receipts=[]
    while tasks:
        mode,a,b=tasks.pop();meter.pay('execution','pop_interval_task',3)
        if a>b or (a==b and mode=='ordinary'):continue
        i=a if mode=='left' else b if mode=='right' else roots[a,b]
        receipt=provider.audit(i);receipts.append(receipt);middle=receipt['value']==1
        if mode=='left':tasks.append(('left' if middle else 'ordinary',a+1,b))
        elif mode=='right':tasks.append(('right' if middle else 'ordinary',a,b-1))
        else:
            tasks.append(('left' if middle else 'ordinary',i+1,b));tasks.append(('right' if middle else 'ordinary',a,i-1))
        meter.pay('execution','branch_and_push_continuations',6)
    return receipts


def draw(n,r,count,seed):
    rng=random.Random(seed);rows=[]
    for _ in range(count):
        indicator=rng.randrange(2);row=[]
        for i in range(n):
            if i and rng.randrange(10)>=r:indicator=1-indicator
            row.append(1 if indicator else 2*rng.randrange(2))
        rows.append(row)
    return rows


def run_arm(directory,case,data,rows,arm):
    cpu=time.process_time_ns();wall=time.perf_counter_ns();meter=Meter();admit(data,meter)
    bank,values=prepare(directory,case['name'],data,arm,case['r'],meter);setup=meter.total
    weights=[1]*len(mk.MENU);active=set(mk.MENU);changes=[];selected=Counter();fees=audits=failures=0;maximum_bits=1
    trace_path=directory/f"{case['name']}_{arm}.jsonl";diag_path=directory/f"{case['name']}_{arm}_diag.jsonl"
    with trace_path.open('w',encoding='utf-8') as trace,diag_path.open('w',encoding='utf-8') as diag:
        trace.write(json.dumps(dict(kind='header',source=data['identity'],version=VERSION,arm=arm))+'\n');trace.flush()
        for t,row in enumerate(rows):
            before=meter.total
            if arm=='full':r=None;bound=sum(data['audit_costs']);roots=None;scope='All source values'
            elif arm in ('learner','ordinary_learner','robust_menu'):
                r=min(bank,key=lambda k:(max(values[k][q] for q in active),k))
                bound=max(values[r][q] for q in active);roots=bank[r]['roots'];scope='Current retained finite-model set'
                meter.pay('selection','minimize_largest_retained_model_invoice',2*len(bank)*len(active))
            else:
                r=case['r'] if arm=='oracle' else 5;bound=values[r][r];roots=bank[r]['roots']
                scope='True-model oracle diagnostic' if arm=='oracle' else 'Independence-model diagnostic only'
            selected[str(r)]+=1;request=f"{case['name']}-{arm}-{t}"
            trace.write(json.dumps(dict(kind='plan',request=request,selected_model_policy=r,active=sorted(active),
                expected_fee_bound=bound,scope=scope),default=g01.encode,separators=(',',':'))+'\n');trace.flush()
            provider=base.Provider(data,row,request,trace,meter)
            receipts=acquire(provider,data['n'],roots,meter);action=base.construct(data,receipts,request,meter);base.check(data,receipts,action,meter)
            paid=sum(r['base_fee'] for r in receipts);fees+=paid;audits+=len(receipts)
            trace.write(json.dumps(dict(kind='output',request=request,action=action,base_fee=paid,physical_audits=len(receipts),
                named_units=meter.total-before),separators=(',',':'))+'\n');trace.flush()
            regret=aa.direct_regret(data,action['assignment'],row);assert regret==0
            diag.write(json.dumps(dict(request=t,hidden=row,regret=regret,true_model_retained_before=case['r'] in active),separators=(',',':'))+'\n')
            if arm in ('learner','ordinary_learner'):
                observed={r['node']:int(r['value']==1) for r in receipts}
                numerators=[mk.likelihood(data['n'],q,observed,meter) for q in mk.MENU]
                weights=[w*z for w,z in zip(weights,numerators)];divisor=reduce(math.gcd,weights);weights=[w//divisor for w in weights]
                old=active.copy();total=sum(weights)
                active &= {q for q,w in zip(mk.MENU,weights) if 100*w>=total}
                if not active:failures+=1;active=set(mk.MENU)
                bits=max(w.bit_length() for w in weights);maximum_bits=max(maximum_bits,bits)
                meter.pay('learning','integer_likelihood_multiplication_gcd_and_set_check',sum(w.bit_length() for w in weights)+10*len(weights))
                payload=dict(request=t,pattern=observed,row_likelihood_numerators=numerators,active=sorted(active),
                    weight_state_sha256=g01.kernel.digest([hex(w) for w in weights]),max_weight_bits=bits,empty_set_fallbacks=failures)
                if old!=active or t==0 or (t+1)&t==0:payload['weights_hex']=[hex(w) for w in weights]
                if old!=active:changes.append(dict(after_request=t,active=sorted(active)))
                trace.write(json.dumps(dict(kind='model_update',**payload),separators=(',',':'))+'\n');trace.flush()
    return dict(outputs=len(rows),physical_audits=audits,base_audit_fee=fees,named_units=meter.total,setup_units=setup,
        invoice=meter.record(),selected_policies=dict(selected),model_set_changes=changes,final_active=sorted(active),
        confidence_failures=failures,max_likelihood_bits=maximum_bits,trace_bytes=trace_path.stat().st_size,
        diagnostic_bytes=diag_path.stat().st_size,arm_cpu_ns=time.process_time_ns()-cpu,arm_wall_ns=time.perf_counter_ns()-wall,
        timing_scope='Preparation, execution, learning, trace export and diagnostics; shared row generation and outer packaging excluded')


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    rng=random.Random(8141440);cases=[]
    for n in (6,10,16):
        costs=[rng.randrange(1,10) for _ in range(n)]
        for r in (1,5,9):cases.append(dict(name=f'n{n}r{r}',costs=costs,r=r,seed=8141450+len(cases)))
    g01.save(directory/'design.json',dict(version=VERSION,stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,requests=256,arms=ARMS,
        public_sources=[source(c['costs']) for c in cases],source_sha256=g01.sha(__file__),
        declaration_sha256=g01.sha(HERE/'markov_service_design.md'),
        dependencies={name:g01.sha(HERE/name) for name in ('markov_paths.py','star_learning.py','action_audits.py','g01.py')}))
    result=dict(status='running',cases=[])
    for case in cases:
        data=source(case['costs']);rows=draw(data['n'],case['r'],256,case['seed']);record=dict(name=case['name'],arms={})
        for arm in ARMS:
            record['arms'][arm]=run_arm(directory,case,data,rows,arm)
            g01.save(directory/'progress.json',dict(completed=result['cases'],current=record))
        for key in ('physical_audits','base_audit_fee','named_units','selected_policies','model_set_changes','final_active'):
            assert record['arms']['learner'][key]==record['arms']['ordinary_learner'][key]
        result['cases'].append(record);g01.save(directory/'results.json',result)
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat())
    g01.save(directory/'results.json',result)
    print(json.dumps(dict(status=result['status'],cases=[dict(name=c['name'],arms={arm:{k:r[k] for k in
        ('outputs','base_audit_fee','named_units','final_active','confidence_failures')} for arm,r in c['arms'].items()}) for c in result['cases']])))


if __name__=='__main__':run(Path(sys.argv[1]))
