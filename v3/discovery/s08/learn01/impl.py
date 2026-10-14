#!/usr/bin/env python3
"""Independent-source repeated repair with learning from paid receipts.
Codex (GPT-6), 2026-10-14. DEVELOPMENT. No free unqueried labels.
"""
from collections import Counter
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import json
import math
import platform
import random
import sys
import time
import g01
import action_audits as aa
import star_check

HERE=Path(__file__).resolve().parent
VERSION='s08-star-learning-v1'
Meter=g01.kernel.Meter


def source(costs):
    data=aa.original([[0,i,1] for i in range(1,len(costs))],costs)
    data.pop('identity');data['bit_source']='independent fresh rows; mutually independent ternary vertices'
    data['alphabet']=[0,1,2]
    return g01.seal(data)


def admit(data,meter):
    if data!=source(data['audit_costs']):raise ValueError('Unadmitted original ternary star source')
    if any(type(c)is not int or c<=0 for c in data['audit_costs']):raise ValueError('Audit fees must be positive integers')
    meter.pay('source','original_clauses_features_star_and_cost_alphabet',
        20+len(data['audit_costs'])+sum(1+len(c) for c in data['hard'])+5*len(data['features']))


def confidence(count,success,m,meter):
    if not 0<=success<=count:raise ValueError('Invalid Bernoulli count')
    if count==0:return (F(0),F(1))
    # alpha=1/20. Integer arithmetic proves 2 exp(-2 n r^2)<=alpha/(m n(n+1)).
    target=40*m*count*(count+1);power=(target-1).bit_length()
    numerator=power*1024*1024
    radius_grid=math.isqrt(numerator//(2*count))
    while 2*count*radius_grid*radius_grid<numerator:radius_grid+=1
    radius=F(radius_grid,1024);mean=F(success,count)
    meter.pay('confidence','integer_tail_grid_and_clipped_interval',18+target.bit_length())
    return max(F(0),mean-radius),min(F(1),mean+radius)


def select(costs,counts,successes,meter):
    intervals=[confidence(n,s,len(costs),meter) for n,s in zip(counts,successes)]
    pessimistic=[intervals[0][1]]+[bounds[0] for bounds in intervals[1:]]
    decision=star_check.closed_form(list(map(F,costs)),pessimistic)
    meter.pay('planning','ratio_order_and_robust_bundle_gain',12*len(costs)+len(costs)*len(costs))
    return dict(route='leaves' if decision['gain']>0 else 'center',order=decision['order'],
        lower_gain=max(F(0),decision['gain']),intervals=intervals)


class Provider:
    def __init__(self,data,row,request,trace,meter):
        self.data=data;self._row=row;self.request=request;self.trace=trace;self.meter=meter;self.seen=set()
    def audit(self,i):
        if i in self.seen or not 0<=i<len(self._row):raise ValueError('Invalid physical query')
        receipt=g01.seal(dict(source=self.data['identity'],request=self.request,node=i,value=self._row[i],
            base_fee=self.data['audit_costs'][i],sequence=len(self.seen)))
        self.seen.add(i)
        self.trace.write(json.dumps(dict(kind='audit',receipt=receipt),separators=(',',':'))+'\n');self.trace.flush()
        self.meter.pay('provider','construct_and_export_receipt_words',12)
        return receipt


def purchase(provider,decision,n):
    receipts=[];known={}
    def get(i):
        receipt=provider.audit(i);receipts.append(receipt);known[i]=receipt['value'];return receipt['value']
    if decision['route']=='full':
        for i in range(n):get(i)
    elif decision['route']=='center':
        if get(0)==1:
            for i in range(1,n):get(i)
    elif decision['route']=='leaves':
        for i in decision['order']:
            if get(i)==1:
                if get(0)==1:
                    for j in range(1,n):
                        if j not in known:get(j)
                break
    else:raise ValueError('Unknown acquisition route')
    return receipts


def construct(data,receipts,request,meter):
    known={}
    for receipt in receipts:
        if receipt['identity']!=g01.kernel.digest({k:v for k,v in receipt.items() if k!='identity'}):raise ValueError('Receipt hash mismatch')
        if receipt['source']!=data['identity'] or receipt['request']!=request:raise ValueError('Wrong source/request receipt')
        i=receipt['node']
        if i in known or receipt['value'] not in (0,1,2) or receipt['base_fee']!=data['audit_costs'][i]:raise ValueError('Invalid receipt')
        known[i]=receipt['value'];meter.pay('receipt','bind_source_request_value_and_fee',15)
    assignment=0;selected=[]
    for e,(a,b,w) in enumerate(data['edges']):
        qa=[known[a]] if a in known else [0,1,2];qb=[known[b]] if b in known else [0,1,2]
        if max(qa)<=min(qb):node=a;offset=0
        elif max(qb)<=min(qa):node=b;offset=1
        else:raise ValueError('Acquisition left an unresolved edge')
        selected.extend([node,node]);assignment|=(1<<(4*e+offset))|(1<<(4*e+2+offset))
        meter.pay('action','two_component_endpoint_choice',12)
    return dict(assignment=assignment,selected=selected,regret_bound=0)


def check(data,receipts,action,meter):
    assignment=action['assignment'];known={r['node']:r['value'] for r in receipts}
    for clause in data['hard']:
        if not any(bool(assignment>>(abs(lit)-1)&1)==(lit>0) for lit in clause):raise ValueError('Infeasible output')
        meter.pay('check','original_clause',len(clause)+1)
    for e,(a,b,w) in enumerate(data['edges']):
        qa=[known[a]] if a in known else [0,1,2];qb=[known[b]] if b in known else [0,1,2]
        chosen=[f['node'] for j,f in enumerate(data['features'][4*e:4*e+4]) if assignment>>(4*e+j)&1]
        if chosen!=action['selected'][2*e:2*e+2]:raise ValueError('Action decoding mismatch')
        for va in qa:
            for vb in qb:
                costs={a:va,b:vb}
                if sum(costs[i] for i in chosen)!=2*min(va,vb):raise ValueError('Nonzero compatible regret')
                meter.pay('check','compatible_local_cost_comparison',8)


def environment_rows(probabilities,count,seed):
    rng=random.Random(seed);rows=[]
    for _ in range(count):
        row=[]
        for p in probabilities:
            extreme=rng.randrange(p.denominator)<p.numerator
            row.append(2*rng.randrange(2) if extreme else 1)
        rows.append(row)
    return rows


def run_arm(directory,name,data,rows,probabilities,arm):
    trace_path=directory/f'{name}_{arm}.jsonl';diagnostics_path=directory/f'{name}_{arm}_diag.jsonl'
    meter=Meter();admit(data,meter);setup=meter.total
    counts=[0]*data['n'];successes=[0]*data['n'];fees=audits=0;routes=Counter();switches=[];previous=None
    true_formula=star_check.closed_form(list(map(F,data['audit_costs'])),probabilities) if arm=='oracle' else None
    cpu=time.process_time_ns();wall=time.perf_counter_ns();final_intervals=None
    with trace_path.open('w',encoding='utf-8') as trace,diagnostics_path.open('w',encoding='utf-8') as diag:
        trace.write(json.dumps(dict(kind='header',version=VERSION,source=data['identity'],arm=arm))+'\n');trace.flush()
        for k,row in enumerate(rows):
            before=meter.total
            if arm in ('learner','ordinary_learner'):
                decision=select(data['audit_costs'],counts,successes,meter);final_intervals=decision['intervals']
            elif arm=='oracle':decision=dict(route='leaves' if true_formula['gain']>0 else 'center',order=true_formula['order'])
            else:decision=dict(route='full' if arm=='full' else 'center',order=list(range(1,data['n'])))
            meter.pay('planning','route_dispatch',4)
            if previous!=decision['route']:switches.append(dict(request=k,route=decision['route']));previous=decision['route']
            request=f'{name}-{arm}-{k}'
            trace.write(json.dumps(dict(kind='plan',request=request,decision=decision,counts_before=counts,successes_before=successes),default=g01.encode,separators=(',',':'))+'\n');trace.flush()
            provider=Provider(data,row,request,trace,meter)
            receipts=purchase(provider,decision,data['n']);action=construct(data,receipts,request,meter);check(data,receipts,action,meter)
            paid=sum(r['base_fee'] for r in receipts);fees+=paid;audits+=len(receipts);routes[decision['route']]+=1
            output=dict(kind='output',request=request,action=action,physical_audits=len(receipts),base_fee=paid,named_units=meter.total-before)
            trace.write(json.dumps(output,separators=(',',':'))+'\n');trace.flush()
            # Post-output truth diagnostics never enter the learner's state.
            regret=aa.direct_regret(data,action['assignment'],row);assert regret==0
            covers=all(F(s,n)-F(0)<=1 for n,s in zip(counts,successes) if n) # basic state sanity only
            if arm in ('learner','ordinary_learner'):
                covers=all(lo<=p<=hi for (lo,hi),p in zip(decision['intervals'],probabilities))
            diag.write(json.dumps(dict(request=k,hidden=row,regret=regret,pre_request_confidence_covers_truth=covers),separators=(',',':'))+'\n')
            if arm in ('learner','ordinary_learner'):
                for receipt in receipts:
                    i=receipt['node'];counts[i]+=1;successes[i]+=receipt['value']!=1
                    meter.pay('learning','update_acquired_extreme_indicator',4)
    return dict(outputs=len(rows),physical_audits=audits,base_audit_fee=fees,named_units=meter.total,setup_units=setup,
        invoice=meter.record(),routes=dict(routes),switches=switches,counts=counts,successes=successes,
        final_pre_request_intervals=final_intervals,trace_bytes=trace_path.stat().st_size,diagnostic_bytes=diagnostics_path.stat().st_size,
        arm_cpu_ns=time.process_time_ns()-cpu,arm_wall_ns=time.perf_counter_ns()-wall,
        timing_scope='Complete arm including exports and diagnostics; not isolated solver or controller speed')


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    cases=[dict(name='favorable',costs=[10,1,1,1,1],p=[F(1,2)]+[F(9,10)]*4,seed=814140),
        dict(name='unfavorable',costs=[2,1,1,1,1],p=[F(4,5)]+[F(1,2)]*4,seed=814141),
        dict(name='unequal',costs=[9,1,2,1,3],p=[F(2,5),F(19,20),F(4,5),F(9,10),F(3,5)],seed=814142)]
    arms=['center','full','learner','ordinary_learner','oracle'];count=2048
    g01.save(directory/'design.json',dict(version=VERSION,contributor='Codex (GPT-6)',stage='DEVELOPMENT',
        created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,arms=arms,requests_per_case=count,alpha='1/20',
        python=platform.python_version(),source_declarations=[source(c['costs']) for c in cases],
        source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'star_learning_design.md'),
        dependencies={p.name:g01.sha(p) for p in (HERE/'star_check.py',HERE/'action_audits.py',HERE/'g01.py')}))
    result=dict(status='running',cases=[])
    for case in cases:
        data=source(case['costs']);rows=environment_rows(case['p'],count,case['seed'])
        record=dict(name=case['name'],arms={},true_fee_formula=star_check.closed_form(list(map(F,case['costs'])),case['p']))
        for arm in arms:
            record['arms'][arm]=run_arm(directory,case['name'],data,rows,case['p'],arm)
            g01.save(directory/'progress.json',dict(completed_cases=result['cases'],current=record))
        for key in ('base_audit_fee','physical_audits','named_units','counts','successes','routes'):
            assert record['arms']['learner'][key]==record['arms']['ordinary_learner'][key]
        result['cases'].append(record);g01.save(directory/'results.json',result)
    result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat())
    g01.save(directory/'results.json',result)
    print(json.dumps(dict(status=result['status'],cases=[dict(name=c['name'],arms={a:{k:r[k] for k in
        ('outputs','physical_audits','base_audit_fee','named_units','routes','switches')} for a,r in c['arms'].items()}) for c in result['cases']]),default=g01.encode))


if __name__=='__main__':run(Path(sys.argv[1]))
