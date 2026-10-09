#!/usr/bin/env python3
"""Read-only saved-run audit and narrowly targeted frozen-v1 failure probes."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
import random
import sys

ROOT=Path(__file__).resolve().parent
RUN=ROOT.parents[1]/'development/multi_action_run_v1'


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    spec.loader.exec_module(module)
    return module


def norm2(vector):
    return sum((x*x for x in vector),F(0))


def safe_state(f):
    return {'settled':f.settled,'pending':f.pending is not None,
            'used_count':len(f.used),'work':f.work.record(),
            'variance_bits':max(abs(f.variance.numerator).bit_length(),f.variance.denominator.bit_length()),
            'allowance_bits':max(abs(f.allowances.numerator).bit_length(),f.allowances.denominator.bit_length()),
            'bound_bits':max(abs((f.variance+f.allowances).numerator).bit_length(),(f.variance+f.allowances).denominator.bit_length())}


def saved_evidence():
    results=[]
    for rowpath in sorted(RUN.glob('*_rows.json')):
        name=rowpath.name.removesuffix('_rows.json')
        rows=json.loads(rowpath.read_text())
        issued=[json.loads(line) for line in (RUN/(name+'_issued.jsonl')).read_text().splitlines()]
        saved=json.loads((RUN/(name+'_result.json')).read_text())
        assert len(rows)==len(issued)==32
        residual=[F(0)]*10
        variance=allowances=slack=mixed=rounded=sampled=fees=nonbuy=control=F(0)
        fixed=[F(0)]*4
        gaps=[F(0)]*4
        resource_totals={}
        for row,emitted in zip(rows,issued):
            assert all(row[k]==v for k,v in emitted.items())
            assert 'label' not in emitted and row['round']==emitted['round']
            p,w,eta=F(row['p']),F(row['weight']),F(row['eta'])
            q=tuple(map(F,row['mixture']));nu=tuple(map(F,row['dyadic_mixture']))
            y=row['label'];assert type(y) is int and y in (0,1)
            endpoints=tuple(tuple(F(x) for x in costs) for costs in row['cost_rows'])
            slopes=tuple(right-left for left,right in endpoints)
            mean=sum((qi*d for qi,d in zip(q,slopes)),F(0))
            phi=(w*(F(1,2)-p),)+tuple(w*max(F(0),1-abs(4*p-j)) for j in range(5))
            phi+=tuple(F(1,100)*w*(mean-d) for d in slopes)
            score=sum((r*f for r,f in zip(residual,phi)),F(0))+(1-2*p)*norm2(phi)/2
            allowance=2*max(F(0),(1-p)*score,-p*score)
            assert allowance==F(row['root_allowance'])
            residual=[r+(y-p)*f for r,f in zip(residual,phi)]
            variance+=p*(1-p)*norm2(phi);allowances+=allowance
            assert norm2(residual)<=variance+allowances
            assert F(row['B'])==variance+allowances
            costs=tuple(left+(right-left)*y for left,right in endpoints)
            predictions=tuple(left+(right-left)*p for left,right in endpoints)
            ideal=sum((qi*c for qi,c in zip(q,costs)),F(0))
            nu_cost=sum((qi*c for qi,c in zip(nu,costs)),F(0))
            assert ideal==F(row['ideal_cost']) and nu_cost==F(row['rounded_cost'])
            chosen=row['chosen_role']
            assert costs[chosen]==F(row['sampled_cost'])
            cumulative=0;selected=None
            for i,count in enumerate(row['slots']):
                cumulative+=count
                if row['draw']<cumulative:
                    selected=i;break
            assert selected==chosen
            mixed+=w*ideal;rounded+=w*nu_cost;sampled+=w*costs[chosen]
            predicted_mix=sum((qi*c for qi,c in zip(q,predictions)),F(0))
            slack+=w*eta*F(3,16)
            for a in range(4):
                fixed[a]+=w*costs[a]
                gaps[a]+=w*(predicted_mix-predictions[a])
                assert mixed-fixed[a]==gaps[a]+100*residual[-4+a]
                assert gaps[a]<=slack
            fee=F(row['checked_service_fee'])
            assert F(row['feedback_fee'])==(F(0) if chosen==3 else fee)
            fees+=w*fee
            nonbuy+=w*(F(0) if chosen==3 else costs[chosen])
            assert F(row['controller_fee'])==F(row['controller_ops'],100000)
            control+=w*F(row['controller_fee'])
            for k,v in row['service_resources'].items():resource_totals[k]=resource_totals.get(k,0)+v
        final=saved['final']
        assert mixed==F(final['mixed_cost']) and fixed==list(map(F,final['fixed_costs']))
        assert residual==list(map(F,final['residual']))
        assert gaps==list(map(F,final['predicted_gaps']))
        assert variance==F(final['variance']) and allowances==F(final['allowances'])
        assert slack==F(final['smoothing_slack'])
        assert rounded==F(saved['dyadic_mixed_cost']) and sampled==F(saved['sampled_action_cost'])
        assert fees==F(saved['always_buy_fee_cost']) and nonbuy==F(saved['nonbuy_task_loss'])
        assert control==F(saved['controller_fee'])
        assert fees+nonbuy+control==F(saved['all_in_cost_excluding_one_time_setup'])
        assert resource_totals==saved['raw_checked_service_resources']
        work=final['work']
        assert sum(work['counts'].values())==work['total']
        assert sum(row['controller_ops'] for row in rows)+64==work['total']
        results.append({'name':name,'rows':32,'status':'PASS',
                        'all_in_cost':str(fees+nonbuy+control),'always_buy_fee':str(fees),
                        'root_cap_misses':sum(not row['tolerance_met'] for row in rows),
                        'note':'Exact recomputation from stored records; no solver rerun.'})
    return results


def operation_caps(M):
    table=M.Table(((F(0),F(1)),(F(1),F(0))),F(1))
    no_work=M.Forecaster(actions=2,bins=2,work=M.Work(0))
    try:no_work.issue('zero-budget',table)
    except Exception as exc:issue_error=type(exc).__name__
    else:raise AssertionError('Zero budget unexpectedly issued.')
    assert issue_error=='Exhausted' and no_work.pending is None and not no_work.used
    ample=M.Forecaster(actions=2,bins=2,work=M.Work(10000))
    ample.issue('sizing',table,root_cap=0)
    issuance_cost=ample.work.total
    limited=M.Forecaster(actions=2,bins=2,work=M.Work(issuance_cost))
    limited.issue('sizing',table,root_cap=0)
    before=safe_state(limited)
    try:limited.settle('sizing',1,limited.scope)
    except Exception as exc:settle_error=type(exc).__name__
    else:raise AssertionError('Unfunded settlement unexpectedly succeeded.')
    after=safe_state(limited)
    assert settle_error=='Exhausted' and before==after
    return {'zero_budget_issue_error':issue_error,'zero_budget_state':safe_state(no_work),
            'exact_issue_budget':issuance_cost,'unfunded_settlement_error':settle_error,
            'unfunded_settlement_unchanged':before==after,'state':after,
            'boundary':'Pending forecast remains; there is no cancellation/fallback controller in this component.'}


def numeric_cap_commit(M):
    work=M.Work()
    f=M.Forecaster(actions=2,bins=4,work=work)
    table=M.Table(((F(0),F(0)),(F(0),F(0))),F(1))
    weight=1<<4093
    attempts=[]
    for t in range(1,17):
        issue=f.issue('numeric-cap-'+str(t),table,weight=weight,root_cap=0)
        assert issue.p==F(1,2)
        before=safe_state(f)
        try:
            f.settle(issue.query,1,f.scope)
        except Exception as exc:
            after=safe_state(f)
            attempts.append({'round':t,'error_type':type(exc).__name__,'error':str(exc),
                             'before':before,'after':after})
            return {'failure_observed':True,'failure':attempts[-1],
                    'committed_despite_exception':after['settled']==before['settled']+1 and not after['pending'],
                    'input_weight_bits':weight.bit_length(),'configured_component_cap':M.MAX_RATIONAL_BITS}
    return {'failure_observed':False,'final':safe_state(f)}


def sampling_caps(M):
    oversized_bits=33
    work=M.Work(100)
    selected=M.choose_slots((1<<oversized_bits,0),oversized_bits,0,work)
    rng=random.Random(1);before=rng.getstate()
    draw=rng.getrandbits(8)
    failed_work=M.Work(0)
    try:M.choose_slots((128,128),8,draw,failed_work)
    except Exception as exc:error=type(exc).__name__
    else:raise AssertionError('Zero-budget sampling charge unexpectedly succeeded.')
    return {'choose_slots_accepts_33_bits':selected==0,'accepted_33_bit_work':work.record(),
            'draw_before_denied_charge':{'error':error,'rng_state_already_changed':rng.getstate()!=before,
                                        'charged_units':failed_work.total},
            'scope':'The three-line draw/choose order reproduces the frozen harness order. No large allocation used.'}


def emitted_before_service(D):
    out=ROOT/'multi_action_code_v1_order_probe'
    out.mkdir(exist_ok=False)
    captured={}
    class StopAtFirstService(Exception):pass
    original=D.A.complete
    def capture(query,**kwargs):
        path=out/'audit_order_only_issued.jsonl'
        lines=path.read_text().splitlines()
        assert len(lines)==1
        record=json.loads(lines[0])
        assert 'label' not in record
        assert record['query']=={'a':query.a,'n':query.n,'m':query.m,'r':query.r}
        captured.update({'issued_file_readable_before_service':True,'rows':len(lines),
                         'record_has_label':False,'chosen_role':record['chosen_role'],
                         'service_calls_intercepted':1,'real_truth_computations':0})
        raise StopAtFirstService()
    D.A.complete=capture
    try:
        try:D.exercise('audit_order_only',32,8,out)
        except StopAtFirstService:pass
        else:raise AssertionError('Probe did not stop at first service call.')
    finally:D.A.complete=original
    return captured


def main():
    expected={'07_multi_action_forecasting.py':'4d52fb20d2ebd70cf7b4cf049ecdbf596cc49b353470d3a3782be2b095bb7a9f',
              '07_multi_action_development.py':'e71951eec94f481c7a621df3f3c82c67708be309ed161838db155e282a8470c5'}
    for name,digest in expected.items():assert sha256((RUN/'sources'/name).read_bytes()).hexdigest()==digest
    with (ROOT/'multi_action_code_v1_probe_attempt.json').open('x') as f:
        json.dump({'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
                   'data_class':'DEVELOPMENT','principal_credit_minutes':0},f,indent=2);f.write('\n')
    M=load('_review_frozen_multi_v1',RUN/'sources/07_multi_action_forecasting.py')
    D=load('_review_frozen_development_v1',RUN/'sources/07_multi_action_development.py')
    result={'saved_evidence':saved_evidence(),'operation_caps':operation_caps(M),
            'numeric_cap_commit':numeric_cap_commit(M),'sampling_caps':sampling_caps(M),
            'emission_order':emitted_before_service(D),'data_class':'DEVELOPMENT',
            'principal_credit_minutes':0}
    with (ROOT/'multi_action_code_v1_targeted_result.json').open('x') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'saved_run_recomputed_cases':len(result['saved_evidence']),
                      'numeric_cap_commit':result['numeric_cap_commit'],
                      'emission_order':result['emission_order'],
                      'sampling_caps':result['sampling_caps']},indent=2))


if __name__=='__main__':main()
