"""Specialized ordinary analytic profile for the P3-07 finite prime domain.

This comparator uses the separately proved prime/root-count and branch-class
lemmas. It pays for representative computation and model construction. The
theorems are source-bound mathematical prerequisites, not a newly executed
general proof checker. Full reference rows are opened only AFTER the analytic
profile is frozen, to falsify its claims on this development population.
"""
from collections import Counter,defaultdict
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
from math import isqrt
import sys

HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('_p307_analytic_driver',HERE/'07_paid_reasoning_development.py')
D=importlib.util.module_from_spec(sp);sys.modules[sp.name]=D;sp.loader.exec_module(D)
C,A=D.C,D.A
VERSION='p307-ordinary-analytic-class-profile-v2'


def write(path,value):
    path.write_text(json.dumps(value,indent=2,default=str)+'\n')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True)
    parser.add_argument('--reference',required=True);args=parser.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False);(out/'sources').mkdir()
    meter=A.Meter(1000000);evidence=Counter({c:0 for c in A.CATEGORIES})
    names=('07_computation_adapter.py','07_paid_reasoning.py',
           '07_paid_reasoning_development.py',Path(__file__).name)
    sizes=[(HERE/name).stat().st_size for name in names]
    if sum(sizes)>512000:raise C.Rejected('Analytic registry byte cap exceeded.')
    meter.pay_many((('profile','analytic_registry_read_hash_words',2*sum((n+7)//8 for n in sizes)),
                    ('profile','source_bound_class_model_construction',2048),
                    ('storage','class_model_retention',1024)))
    hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names}
    for name in names:(out/'sources'/name).write_bytes((HERE/name).read_bytes())
    totals=[[0]*len(C.FEATURES) for _ in C.CATALOGUE];classes=[]
    for prime in D.PRIMES:
        meter.pay('check','prime_hypothesis_loop_setup',4)
        assert prime%2==1 and prime>=5
        for divisor in range(2,isqrt(prime)+1):
            meter.pay('check','trial_division_for_prime_hypothesis',2)
            assert prime%divisor
        n=(prime-1)//2
        minus_positive=int(n%2==0)
        groups=(('one',1,1,1),('minus_one',prime-1,1,minus_positive),
                ('ordinary',2,prime-3,n-1-minus_positive))
        for kind,base,size,positive in groups:
            meter.pay('profile','class_size_label_count_and_query_construction',16)
            q=A.Query(f'analytic-{prime}-{kind}',base,n,prime,1)
            runs=[C.run_policy(q,p) for p in C.CATALOGUE]
            features=[]
            for policy,run in zip(C.CATALOGUE,runs):
                D.record_resources(evidence,run)
                meter.pay_many((('profile','class_feature_and_sum_arithmetic',4*len(C.FEATURES)),
                                ('storage','class_feature_read_write',2*len(C.FEATURES))))
                if run['status']=='checked_answer':
                    errors=(0,0,0)
                elif policy.unresolved_action==0:
                    errors=(0,positive,0)
                elif policy.unresolved_action==1:
                    errors=(size-positive,0,0)
                else:
                    errors=(0,0,size)
                row=errors+tuple(size*run['meter']['by_category'][c] for c in A.CATEGORIES)
                features.append(row)
            for total,row in zip(totals,features):
                for k,x in enumerate(row):total[k]+=x
            classes.append({'prime':prime,'kind':kind,'representative':base,'size':size,
                            'positive':positive,'negative':size-positive,
                            'feature_sums':features,'representative_runs':runs})
    meter.pay_many((('profile','analytic_profile_finalize_validate_hash',2*C.PROFILE_WORD_BOUND),
                    ('storage','analytic_profile_retention',C.PROFILE_WORD_BOUND)))
    count=sum(g['size'] for g in classes)
    means=tuple(tuple(F(x,count) for x in row) for row in totals)
    resources={c:evidence[c]+meter.by_category[c] for c in A.CATEGORIES}
    core={'version':VERSION,'source_hashes':hashes,'law':D.LAW,'size':count,
          'means':means,'total_resources':resources,
          'classes':[{k:g[k] for k in ('prime','kind','size','positive','negative','feature_sums')} for g in classes]}
    # The paid numerical table is bounded separately from raw Meter snapshots,
    # which are retained as audit instrumentation and never read by selection.
    encoded=C.canonical(core).encode('ascii')
    if len(encoded)>8*C.PROFILE_WORD_BOUND:raise C.Rejected('Analytic table exceeds prepaid word cap.')
    profile={'version':VERSION,'source_hashes':hashes,'law':D.LAW,'size':count,
             'class_count':len(classes),'representative_policy_runs':len(classes)*len(C.CATALOGUE),
             'means':means,'classes':classes,'total_resources':resources,
             'model_meter':meter.snapshot(),'representative_execution_resources':dict(evidence),
             'frozen_utc_before_reference_read':datetime.now(timezone.utc).isoformat(),
             'prerequisites':'Prime/root-count theorem and source-specific path-class lemma; fixed flat operation model. No full machine-checked generic algebra theorem or measured theorem-development bill.'}
    profile['core']=core;profile['core_bytes']=len(encoded)
    profile['identity']=hashlib.sha256(encoded).hexdigest();write(out/'analytic_profile.json',profile)
    # Independent retained data can now try to falsify the already fixed table.
    raw=[json.loads(line) for line in Path(args.reference).read_text().splitlines()]
    grouped=defaultdict(lambda:[[0]*len(C.FEATURES) for _ in C.CATALOGUE])
    by_class={(g['prime'],g['kind']):g for g in classes};checks=0
    for row in raw:
        p,a=row['query']['m'],row['query']['a']
        kind='one' if a==1 else 'minus_one' if a==p-1 else 'ordinary'
        group=by_class[(p,kind)]
        for j,fs in enumerate(row['features']):
            run=group['representative_runs'][j]
            assert tuple(fs[3:])==tuple(run['meter']['by_category'][c] for c in A.CATEGORIES)
            assert (row['statuses'][j]=='checked_answer')==(run['status']=='checked_answer')
            for k,x in enumerate(fs):grouped[(p,kind)][j][k]+=x
            checks+=1
    for key,group in by_class.items():
        assert tuple(map(tuple,grouped[key]))==tuple(map(tuple,group['feature_sums']))
    selections=[]
    for price_name,prices in D.PRICES.items():
        selection_meter=A.Meter(20000)
        selection_meter.pay_many((('assessment','analytic_price_readout_multiply_add_and_max',4*len(C.CATALOGUE)*len(C.FEATURES)+4*len(C.CATALOGUE)+128),
                                   ('storage','analytic_profile_price_word_read',3*len(C.CATALOGUE)*len(C.FEATURES))))
        costs=tuple(C.total_cost(mu,prices) for mu in means)
        chosen=min(range(len(costs)),key=lambda i:(costs[i],i))
        setup=sum((prices[3+j]*resources[c] for j,c in enumerate(A.CATEGORIES)),F(0))
        online=sum((prices[3+j]*selection_meter.by_category[c] for j,c in enumerate(A.CATEGORIES)),F(0))
        selections.append({'price':price_name,'policy':C.CATALOGUE[chosen].name,
                'exact_costs':dict(zip((p.name for p in C.CATALOGUE),costs)),
                'setup_cost':setup,'assessment_cost':online,'meter':selection_meter.snapshot(),
                'all_in_gain_H64':64*(costs[0]-costs[chosen])-setup-online,
                'all_in_gain_H10000':10000*(costs[0]-costs[chosen])-setup-online})
    result={'status':'PASS','version':VERSION,'profile_id':profile['identity'],
            'class_count':len(classes),'representative_policy_runs':len(classes)*len(C.CATALOGUE),
            'checked_query_policy_resource_and_completion_rows':checks,
            'total_procurement_units':sum(resources.values()),'selections':selections,
            'reference_sha256':hashlib.sha256(Path(args.reference).read_bytes()).hexdigest(),
            'source_hashes':hashes,
            'boundary':'A specialized ordinary comparator. The retained reference is an external development audit, not a construction input; human theorem/program development cost and physical CPU time are not quantified by this abstract operation bill.'}
    write(out/'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='selections'},indent=2))


if __name__=='__main__':main()
