"""Prospectively specified P3-07 four-action DEVELOPMENT evidence."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys
import time
import traceback

HERE=Path(__file__).resolve().parent

def load(name,file):
    spec=importlib.util.spec_from_file_location(name,HERE/file)
    mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod
    spec.loader.exec_module(mod);return mod

M=load('_p307_multi','07_multi_action_forecasting.py')
A=load('_p307_multi_adapter','07_computation_adapter.py')
VERSION='p307-multi-action-development-v2'
POP=tuple((p,a) for p in (17,31,47,61,97) for a in range(1,p))
PRICE_CYCLE=((100,100,20,1),(1,1,F(1,5),1),(100,1,20,1),
             (1,100,20,1),(100,100,0,1),(100,100,10,20))

def write(p,obj):p.write_text(json.dumps(obj,indent=2,default=str)+'\n')

def exercise(name,root_cap,bits,out):
    qr,ar=random.Random(307113),random.Random(307127)
    work=M.Work()
    work.pay('frozen_controller_initial_state',64)
    forecaster=M.Forecaster(scope='p307-'+name,work=work)
    weighted_sampled=weighted_rounded=rounding_bound=actual_rounding=F(0)
    allin=exact_fees=nonbuy_task=control_cost=F(0)
    computation_resources=Counter({c:0 for c in A.CATEGORIES})
    counts=Counter();records=[]
    initial_setup_cost=F(work.total,100000)
    with (out/(name+'_issued.jsonl')).open('x') as issued_file:
        for t in range(1,33):
            start_ops=work.total
            index=qr.randrange(len(POP));p,a=POP[index]
            query=A.Query('multi-'+name+'-'+str(t),a,(p-1)//2,p,1)
            fp,fn,fallback,fee=map(F,PRICE_CYCLE[(t-1)%len(PRICE_CYCLE)])
            weight=F((1,4,1,2)[(t-1)%4]);eta=F(8,1 << t.bit_length())
            table=M.Table(((F(0),fn),(fp,F(0)),(fallback,fallback),(fee,fee)),eta)
            issue=forecaster.issue(query.query_id,table,weight=weight,root_cap=root_cap)
            slots,nu,tv,tv_bound=M.dyadic_round(issue.mixture,bits,work)
            work.pay('fair_random_bits',bits)
            draw=ar.getrandbits(bits)
            chosen=M.choose_slots(slots,bits,draw,work)
            # Freeze the report/action before executing the query's truth computation.
            public={'round':t,'query':{'a':query.a,'n':query.n,'m':query.m,'r':query.r},
                    'p':str(issue.p),'mixture':list(map(str,issue.mixture)),
                    'dyadic_mixture':list(map(str,nu)),'slots':slots,'draw':draw,'chosen_role':chosen,
                    'weight':str(weight),'cost_rows':table.rows,'eta':str(eta),
                    'root_allowance':str(issue.allowance),'tolerance_met':issue.tolerance_met,
                    'root_steps':issue.root_steps,'evaluations':issue.evaluations,
                    'issued_utc':datetime.now(timezone.utc).isoformat()}
            issued_file.write(json.dumps(public,default=str)+'\n');issued_file.flush()
            service=A.complete(query,limit_total=1024,transaction_cap=A.MAX_FULL_TRANSACTIONS,cache_cap=0)
            if service['answer'] is None:
                raise AssertionError('Declared checked service failed.')
            y=service['answer']['answer']
            computation_resources.update(service['meter']['by_category'])
            # Provider fee includes its solve/check/acquisition/storage. Raw
            # operations are retained for scope, not silently billed a second time.
            realized=table.costs(F(y))
            ideal=sum((q*c for q,c in zip(issue.mixture,realized)),F(0))
            rounded=sum((q*c for q,c in zip(nu,realized)),F(0))
            delta_cost=max(realized)-min(realized)
            if abs(rounded-ideal)>delta_cost*tv or tv>tv_bound:
                raise AssertionError('Rounded mixed-cost transport failed.')
            # Exhaustively verify the categorical primitive on this finite table.
            lookup=[0]*4
            for k in range(1 << bits):
                cumulative=0
                for i,count in enumerate(slots):
                    cumulative+=count
                    if k<cumulative:
                        lookup[i]+=1;break
            if tuple(lookup)!=slots:
                raise AssertionError('Categorical lookup does not realize the dyadic distribution.')
            report=forecaster.settle(query.query_id,y,forecaster.scope)
            if any(r>report['generic_action_bound'] for r in report['action_regrets']):
                raise AssertionError('Generic four-action mixed bound failed.')
            for r,b in zip(report['action_regrets'],report['retained_gap_bounds']):
                if r>b:raise AssertionError('Retained-gap four-action bound failed.')
            step_control=F(work.total-start_ops,100000)
            # All labels are paid: an early buy is reused, every other choice
            # requires the same fee later for this fully supervised protocol.
            selected_task=F(0) if chosen==3 else realized[chosen]
            exact_fees+=weight*fee
            nonbuy_task+=weight*selected_task
            control_cost+=weight*step_control
            allin+=weight*(fee+selected_task+step_control)
            weighted_sampled+=weight*realized[chosen]
            weighted_rounded+=weight*rounded
            rounding_bound+=weight*delta_cost*tv_bound
            actual_rounding+=weight*(rounded-ideal)
            counts['role_'+str(chosen)]+=1
            counts['root_cap_misses']+=int(not issue.tolerance_met)
            row=dict(public,label=y,feedback_reused_from_buy=chosen==3,
                     feedback_fee=str(F(0) if chosen==3 else fee),
                     checked_service_fee=str(fee),service_resources=service['meter']['by_category'],
                     ideal_cost=str(ideal),rounded_cost=str(rounded),sampled_cost=str(realized[chosen]),
                     actual_tv=str(tv),tv_bound=str(tv_bound),controller_ops=work.total-start_ops,
                     controller_fee=str(step_control),B=str(report['B']),
                     action_regrets=list(map(str,report['action_regrets'])),
                     generic_action_bound=str(report['generic_action_bound']))
            records.append(row)
    if allin!=exact_fees+nonbuy_task+control_cost or allin<exact_fees:
        raise AssertionError('Fully paid feedback dominance identity failed.')
    report=forecaster.report()
    result={'name':name,'root_cap':root_cap,'fair_bits':bits,'status':'PASS','rounds':32,
            'final':report,'counts':dict(counts),'dyadic_mixed_cost':weighted_rounded,
            'sampled_action_cost':weighted_sampled,'dyadic_actual_correction':actual_rounding,
            'dyadic_certified_correction':rounding_bound,
            'all_in_cost_excluding_one_time_setup':allin,'always_buy_fee_cost':exact_fees,
            'nonbuy_task_loss':nonbuy_task,'controller_fee':control_cost,
            'initial_setup_fee':initial_setup_cost,'fully_paid_dominance_margin':allin-exact_fees,
            'raw_checked_service_resources':dict(computation_resources),
            'sampling_boundary':'Exact dyadic lookup checked. Seeded draw trace is development; martingale probability theorem assumes independent fair bits and is not inferred from this trace.',
            'cost_boundary':'Flat fee is a stipulated service tariff covering the real bounded solver/checker. Per-operation controller tariff is separate. Lookup-frequency verification and private report serialization are harness diagnostics.'}
    write(out/(name+'_rows.json'),records);write(out/(name+'_result.json'),result)
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);args=parser.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False);(out/'sources').mkdir()
    names=('07_computation_adapter.py','07_multi_action_forecasting.py','07_multi_action_development.py')
    hashes={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names}
    for n in names:(out/'sources'/n).write_bytes((HERE/n).read_bytes())
    write(out/'manifest.json',{'version':VERSION,'stage':'DEVELOPMENT','source_hashes':hashes,
          'started_utc':datetime.now(timezone.utc).isoformat(),'command':sys.argv,
          'plan':'v3/work_logs/P3_07_2026-10-09_S1/development/multi_action_plan_v2.json'})
    started=time.perf_counter_ns();result={'status':'FAIL'}
    try:
        cases=[exercise('full_root_eight_bits',32,8,out),exercise('capped_root_eight_bits',0,8,out),
               exercise('full_root_one_bit',32,1,out)]
        result.update(status='PASS',cases=[{'name':x['name'],'counts':x['counts'],
                      'all_in_cost':x['all_in_cost_excluding_one_time_setup'],
                      'always_buy_cost':x['always_buy_fee_cost'],
                      'generic_action_bound':x['final']['generic_action_bound'],
                      'regrets':x['final']['action_regrets']} for x in cases])
    except Exception as exc:result.update(error=repr(exc),traceback=traceback.format_exc())
    result.update(elapsed_ns=time.perf_counter_ns()-started,source_hashes=hashes,
                  finished_utc=datetime.now(timezone.utc).isoformat())
    write(out/'result.json',result);print(json.dumps(result,indent=2,default=str))
    if result['status']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
