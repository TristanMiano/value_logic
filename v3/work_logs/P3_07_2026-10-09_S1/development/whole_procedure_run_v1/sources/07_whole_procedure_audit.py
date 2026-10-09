"""A fresh DEVELOPMENT audit of the entire P3-07 profile-building policy.

Each episode starts with no acquired performance profile, pays 64 full-policy
profile rows, freezes it, selects once, and serves 64 fresh queries. This is
distinct from the warm-profile audit in 07_paid_reasoning_development.py.
The outer audit itself has a separately retained procurement bill. It does
not establish that conducting that audit was ex ante optimal.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
from dataclasses import replace
import argparse
import hashlib
import importlib.util
import json
import random
import sys
import time
import traceback

HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_p307_rebuilding_driver',HERE/'07_paid_reasoning_development.py')
D=importlib.util.module_from_spec(sp);sys.modules[sp.name]=D;sp.loader.exec_module(D)
C,A=D.C,D.A
VERSION='p307-whole-profile-rebuilding-audit-v1'
PROFILE_N,HORIZON,AUDIT_N,AUDIT_SEED=64,64,256,307139
BUILD_CAP,ASSESS_CAP=150000,20000
WHOLE_RESOURCE_CAP=PROFILE_N*len(C.CATALOGUE)*C.POLICY_BUDGET+BUILD_CAP+ASSESS_CAP+HORIZON*C.POLICY_BUDGET
LOW,HIGH=-80*HORIZON-F(WHOLE_RESOURCE_CAP,1000),F(20*HORIZON)
PRICES=D.PRICES['high']


def write(path,value):
    path.write_text(json.dumps(value,indent=2,default=str)+'\n')


def hashes():
    result=D.source_hashes()
    result[Path(__file__).name]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return result


def priced_resources(counter):
    return sum((PRICES[3+j]*counter[c] for j,c in enumerate(A.CATEGORIES)),F(0))


def build_profile(episode,rng,scope,source_hashes):
    """Disjoint child caps give a deterministic whole acquisition budget.

    At most64*6 adapter calls each use <=1024, and the builder has its own
    150000-unit meter. An exhausted builder leaves its incurred bill and the
    complete procedure deploys fallback. No incomplete profile is assessed.
    """
    evidence=Counter({c:0 for c in A.CATEGORIES})
    meter=A.Meter(BUILD_CAP)
    indices=[];profile=None;kind='acquired'
    try:
        registry_bytes=sum((HERE/name).stat().st_size for name in source_hashes)
        if registry_bytes>512000:
            raise C.Rejected('Whole source registry exceeds fixed byte cap.')
        registry_words=sum(((HERE/name).stat().st_size+7)//8 for name in source_hashes)
        meter.pay_many((('profile','whole_source_read_and_hash_words',2*registry_words),
                        ('profile','public_population_construction',4*len(D.POPULATION)),
                        ('storage','public_population_word_write',2*len(D.POPULATION))))
        if hashes()!=source_hashes:
            raise C.Rejected('Frozen source registry changed during audit.')
        builder=C.ProfileBuilder(scope,tuple(p.name for p in C.CATALOGUE),C.FEATURES,
                  tuple(C.paired_ranges(p) for p in C.CATALOGUE),(PROFILE_N,),F(1,20),meter)
        for i in range(PROFILE_N):
            meter.pay_many((('profile','uniform_profile_index_draw',1),
                            ('storage','profile_query_word_read',4)))
            index=rng.randrange(len(D.POPULATION));indices.append(index)
            row=D.evaluate_row(index,f'whole-profile-{episode}-{i}',evidence)
            meter.pay('profile','checked_label_and_feature_interpretation',4*len(C.FEATURES)*len(C.CATALOGUE))
            builder.add(row['paired'],meter)
        profile=builder.freeze(meter,tuple(evidence[c] for c in A.CATEGORIES))
    except A.BudgetExhausted:
        kind='profile_budget_exhausted'
    resources=Counter({c:evidence[c]+meter.by_category[c] for c in A.CATEGORIES})
    assert sum(resources.values())<=PROFILE_N*len(C.CATALOGUE)*C.POLICY_BUDGET+BUILD_CAP
    if profile is not None:
        assert tuple(resources[c] for c in A.CATEGORIES)==profile.setup_resources
    return profile,resources,{'kind':kind,'indices':indices,'builder_meter':meter.snapshot(),
             'policy_rollout_resources':dict(evidence),'total_resources':dict(resources)}


def episode_run(episode,rng,scope,source_hashes,profile_trace,audit_meter):
    profile,resources,procurement=build_profile(episode,rng,scope,source_hashes)
    if profile is None:
        # This constant branch spends its own one-unit terminal selection.
        selection_meter=A.Meter(ASSESS_CAP)
        selection_meter.pay('assessment','emit_profile_failure_fallback',1)
        selection={'policy':'fallback','kind':'no_profile','meter':selection_meter.snapshot()}
    else:
        selection=C.select(profile,scope,PRICES,HORIZON,assessment_limit=ASSESS_CAP)
    D.record_resources(resources,selection)
    chosen=next(p for p in C.CATALOGUE if p.name==selection['policy'])
    audit_meter.pay_many((('profile','whole_profile_closure_copy_and_hash',2*C.PROFILE_WORD_BOUND),
                           ('storage','whole_profile_closure_retention',C.PROFILE_WORD_BOUND)))
    closure={'episode':episode,'profile':None if profile is None else profile.record(),
             'profile_id':None if profile is None else profile.identity,
             'procurement':procurement,'selection':selection,
             'frozen_utc_before_deployment':datetime.now(timezone.utc).isoformat()}
    profile_trace.write(json.dumps(closure,default=str)+'\n');profile_trace.flush()
    cohort_indices=[];task_cost=F(0);baseline_cost=F(0);exact_cost=F(0)
    audit_extra=Counter({c:0 for c in A.CATEGORIES})
    deploy_resources=Counter({c:0 for c in A.CATEGORIES})
    base_resources=Counter({c:0 for c in A.CATEGORIES})
    exact_resources=Counter({c:0 for c in A.CATEGORIES})
    for j in range(HORIZON):
        audit_meter.pay('profile','fresh_deployment_index_draw',1)
        index=rng.randrange(len(D.POPULATION));cohort_indices.append(index)
        query=D.query(index,f'whole-deploy-{episode}-{j}')
        run=C.run_policy(query,chosen)
        baseline=C.run_policy(query,C.CATALOGUE[0])
        # Reuse a checked complete-solver result for audit scoring when it is
        # already present. Otherwise the external auditor buys its own label.
        if chosen==C.CATALOGUE[-1] and run['answer'] is not None:
            exact=run
        else:
            exact=C.run_policy(query,C.CATALOGUE[-1])
            D.record_resources(audit_extra,exact)
        label=exact['answer']['answer']
        audit_meter.pay('profile','whole_episode_feature_and_cost_readout',4*3*len(C.FEATURES))
        features=C.features_from_checked_label(run,label)
        task_cost+=sum((p*f for p,f in zip(PRICES[:3],features[:3])),F(0))
        baseline_cost+=C.total_cost(C.features_from_checked_label(baseline,label),PRICES)
        exact_cost+=C.total_cost(C.features_from_checked_label(exact,label),PRICES)
        D.record_resources(resources,run);D.record_resources(deploy_resources,run)
        D.record_resources(base_resources,baseline);D.record_resources(exact_resources,exact)
        D.record_resources(audit_extra,baseline)
    assert sum(resources.values())<=WHOLE_RESOURCE_CAP
    cost=task_cost+priced_resources(resources)
    gain=baseline_cost-cost
    assert LOW<=gain<=HIGH
    audit_meter.pay_many((('profile','whole_episode_scalar_sum_and_range_check',64),
                           ('storage','whole_episode_record_retention',C.PROFILE_WORD_BOUND)))
    return {'episode':episode,'policy':chosen.name,'profile_id':closure['profile_id'],
            'profile_kind':procurement['kind'],'cohort_indices':cohort_indices,
            'controller_resources':dict(resources),'profile_resources':procurement['total_resources'],
            'assessment_resources':selection['meter']['by_category'],
            'deployment_resources':dict(deploy_resources),'baseline_resources':dict(base_resources),
            'exact_resources':dict(exact_resources),'audit_extra_resources':dict(audit_extra),
            'controller_task_cost':str(task_cost),'controller_all_in_cost':str(cost),
            'baseline_cost':str(baseline_cost),'charged_exact_cost':str(exact_cost),
            'paired_all_in_gain':str(gain),'resource_cap':WHOLE_RESOURCE_CAP}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True)
    args=parser.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    (out/'sources').mkdir();source_hashes=hashes()
    for name in source_hashes:(out/'sources'/name).write_bytes((HERE/name).read_bytes())
    scope=replace(D.actual_scope(source_hashes),
                 law=D.LAW+';whole-generator-sha256:'+source_hashes[Path(__file__).name])
    closure={'version':VERSION,'stage':'DEVELOPMENT','source_hashes':source_hashes,
             'profile_scope':scope.record(),'audit_seed':AUDIT_SEED,'audit_n':AUDIT_N,
             'profile_n':PROFILE_N,'horizon':HORIZON,'prices':tuple(map(str,PRICES)),
             'whole_resource_cap':WHOLE_RESOURCE_CAP,'scalar_range':(str(LOW),str(HIGH)),
             'sampling':'IID complete episodes is a model assumption; seeded development realization.',
             'reset':'No acquired profile and cold adapter/cache for every query at every episode.',
             'frozen_utc_before_first_episode':datetime.now(timezone.utc).isoformat(),
             'plan':'v3/work_logs/P3_07_2026-10-09_S1/development/whole_procedure_plan_v1.json'}
    closure['identity']=C.digest(closure);write(out/'closure.json',closure)
    start=time.perf_counter_ns();result={'status':'FAIL'}
    # This is only the outer audit's accounting budget, independent of every
    # bounded tested episode. Use disjoint per-episode meters to avoid the
    # adapter's 10-million-unit single-meter envelope.
    audit_bill=Counter({c:0 for c in A.CATEGORIES});policies=Counter()
    total_gain=F(0);total_controller=F(0);total_baseline=F(0);total_exact=F(0)
    rng=random.Random(AUDIT_SEED)
    try:
        with (out/'profile_closures.jsonl').open('x') as pt,(out/'episode_rows.jsonl').open('x') as trace:
            for episode in range(AUDIT_N):
                audit_meter=A.Meter(100000)
                row=episode_run(episode,rng,scope,source_hashes,pt,audit_meter)
                for c in A.CATEGORIES:
                    audit_bill[c]+=row['controller_resources'][c]+row['audit_extra_resources'][c]+audit_meter.by_category[c]
                row['outer_audit_meter']=audit_meter.snapshot()
                total_gain+=F(row['paired_all_in_gain']);total_controller+=F(row['controller_all_in_cost'])
                total_baseline+=F(row['baseline_cost']);total_exact+=F(row['charged_exact_cost'])
                policies[row['policy']]+=1
                trace.write(json.dumps(row)+'\n')
                if (episode+1)%32==0:print(f'Whole episodes {episode+1}/{AUDIT_N}',flush=True)
        check=A.Meter(20000)
        r,k=C.certified_radius(AUDIT_N,1,F(1,20),1,check)
        check.pay_many((('assessment','whole_mean_and_lower_bound_readout',64),
                        ('storage','whole_audit_certificate_retention',C.PROFILE_WORD_BOUND)))
        mean=total_gain/AUDIT_N;lower=max(LOW,mean-(HIGH-LOW)*r)
        audit_bill.update(check.by_category)
        result.update(status='PASS',closure=closure,policies=dict(policies),
                      mean_all_in_gain=str(mean),lower_all_in_gain=str(lower),
                      positive_whole_procedure_certificate=lower>0,radius=str(r),radius_k=k,
                      mean_controller_all_in_cost=str(total_controller/AUDIT_N),
                      mean_baseline_cost=str(total_baseline/AUDIT_N),
                      mean_charged_exact_cost=str(total_exact/AUDIT_N),
                      outer_audit_procurement_resources=dict(audit_bill),
                      outer_audit_procurement_cost=str(priced_resources(audit_bill)),
                      final_certificate_meter=check.snapshot(),
                      boundary='Whole profile-rebuilding episode at fixed high prices only. Outer audit procurement is additional; no claim that acquiring this audit was optimal, no final evaluation claim.')
    except Exception as exc:
        result.update(error=repr(exc),traceback=traceback.format_exc())
    result.update(elapsed_ns=time.perf_counter_ns()-start,finished_utc=datetime.now(timezone.utc).isoformat())
    write(out/'result.json',result);print(json.dumps(result,indent=2),flush=True)
    if result['status']!='PASS':raise SystemExit(1)


if __name__=='__main__':main()
