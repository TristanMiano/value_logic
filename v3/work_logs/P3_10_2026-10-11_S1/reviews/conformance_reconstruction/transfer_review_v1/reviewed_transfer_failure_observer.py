"""Post-outcome finite path mechanism audit; no paid rerun or fitted controller.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import time
import traceback
from amended_lineage_reader import Lineage

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
CHECKS=Counter()


def stamp():return {'utc':datetime.now(timezone.utc).isoformat(),'monotonic_ns':time.monotonic_ns()}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def rat(x):return F(*x) if isinstance(x,(tuple,list)) else F(x)

def require(ok,name,detail):
    CHECKS[name]+=1
    if not ok:raise AssertionError((name,detail))

def encode(x):
    if isinstance(x,F):return [x.numerator,x.denominator]
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x

def save(path,value):
    with path.open('x') as file:json.dump(encode(value),file,sort_keys=True,indent=2,allow_nan=False);file.write('\n')

def avg(xs):return sum(xs,F(0))/len(xs)

def moment(ps,ys):
    p,y=avg(ps),avg(ys)
    vp=avg([(x-p)**2 for x in ps])
    cov=avg([(a-p)*(b-y) for a,b in zip(ps,ys)])
    loss=avg([(a-b)**2 for a,b in zip(ps,ys)])
    result={'mean_forecast':p,'mean_truth':y,'label_variance':y*(1-y),
            'squared_mean_bias':(p-y)**2,'forecast_variance':vp,
            'truth_covariance':cov,'negative_twice_covariance':-2*cov,'brier_mean':loss}
    require(loss==result['label_variance']+result['squared_mean_bias']+vp-2*cov,
            'exact_moment_identity',result)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--numeric',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=False);start=stamp()
    try:
        lineage=Lineage();numeric_path=Path(args.numeric).resolve()
        numeric=json.loads(numeric_path.read_text())
        require(numeric['status']=='PASS','numeric_source_pass',str(numeric_path))
        by_id={e['unit_id']:e for e in numeric['per_episode']}
        units=[u for u in lineage.schedule['units'] if u['arm']=='broker' and u['engine'] in ('broker','mirror')]
        require(len(units)==len(by_id)==126,'full_episode_roster',len(units))
        groups={g['id']:g for g in lineage.schedule['groups'] if g['arm']=='broker'}
        records=[];signature_groups={};query_rows={};parents=[]
        for unit in units:
            uid=unit['id'];nr=by_id[uid];group=groups[unit['group_id']]
            public,_=lineage.record('public',uid);paid=public['value']['paid_result'];trace=paid['episode']['trace']
            if nr['status']!='audited':
                parents.append({'unit_id':uid,'status':'unavailable'});continue
            nrows=[r for b in nr['blocks'] for r in b['rows']]
            require(len(trace)==len(nrows)==group['recipe']['horizon'],'complete_parent',uid)
            require([r['index'] for r in nrows]==list(range(len(trace))),'numeric_chronology',uid)
            parents.append({'unit_id':uid,'status':'audited'})
            data=[{'index':r['index'],'base':rat(r['base_q']),'equal':F(sum(r['advice']),6),
                   'truth':n['truth'],'signature':tuple(r['advice']),'selected':r['selected'],
                   'first':n['first_occurrence'],'key':json.dumps(r['claim_key'],separators=(',',':'))}
                   for r,n in zip(trace,nrows)]
            group_key=unit['group_id']
            same=[{k:r[k] for k in ('index','truth','signature','first','key')} for r in data]
            if group_key in query_rows:require(same==query_rows[group_key],'same_population_truth_and_advice',uid)
            else:query_rows[group_key]=same
            selections={s['name']:[r for r in data if s['start']<=r['index']<s['stop']] for s in unit['segments']}
            selections['first_occurrence']=[r for r in data if r['first']]
            for name,rows in selections.items():
                ys=[r['truth'] for r in rows];base=moment([r['base'] for r in rows],ys);equal=moment([r['equal'] for r in rows],ys)
                delta=equal['brier_mean']-base['brier_mean']
                pieces={k:equal[k]-base[k] for k in ('squared_mean_bias','forecast_variance','negative_twice_covariance')}
                require(delta==sum(pieces.values(),F(0)),'exact_a2_moment_difference',[uid,name])
                selected=[r for r in rows if r['selected']]
                records.append({'unit_id':uid,'configuration_id':unit['configuration_id'],'group_id':group_key,
                    'family':group['recipe']['family'],'seed':unit['seed'],'slice':name,'denominator':len(rows),
                    'true_count':sum(ys),'selected_count':len(selected),'selected_true_count':sum(r['truth'] for r in selected),
                    'selected_true_fraction':F(sum(r['truth'] for r in selected),len(selected)) if selected else None,
                    'base_moments':base,'equal_moments':equal,'a2_difference':delta,'a2_contributions':pieces})
            profiles=[]
            for block in nr['blocks']:
                i=block['block'];part=data[4*i:4*i+4]
                profiles.append({'block':i,'slice':'transfer' if group['recipe']['family']=='gate_transfer' and 4*i>=64 else 'prefix' if group['recipe']['family']=='gate_transfer' else 'whole',
                    'weights_before':block['weights_before'],'weights_after':block['weights_after'],
                    'mean_base':avg([r['base'] for r in part]),'true_count':sum(r['truth'] for r in part),
                    'selected_truth':next(r['truth'] for r in part if r['selected'])})
            # Preserve one profile for every configured path; aliases remain explicit duplicates.
            parents[-1]['block_profiles']=profiles
        for gid,rows in query_rows.items():
            group=groups[gid]
            selections={'whole':rows,'first_occurrence':[r for r in rows if r['first']]}
            if group['recipe']['prefix_length']:
                split=group['recipe']['prefix_length'];selections.update(prefix=rows[:split],transfer=rows[split:])
            for name,part in selections.items():
                signatures=defaultdict(list)
                for r in part:signatures[r['signature']].append(r)
                strata=[]
                for sig,rs in sorted(signatures.items()):
                    n,k=len(rs),sum(r['truth'] for r in rs);p=F(k,n)
                    strata.append({'advice_signature':list(sig),'positions':n,'true_count':k,'false_count':n-k,
                        'empirical_true_fraction':p,'unique_full_keys':len({r['key'] for r in rs}),
                        'retrospective_best_constant_brier_sum':n*p*(1-p)})
                signature_groups[(gid,name)]={'group_id':gid,'family':group['recipe']['family'],'slice':name,
                    'positions':len(part),'true_count':sum(r['truth'] for r in part),'unique_full_keys':len({r['key'] for r in part}),
                    'signature_strata':strata,'retrospective_signature_fit_brier_mean':sum((r['retrospective_best_constant_brier_sum'] for r in strata),F(0))/len(part),
                    'fitted_oracle_is_deployed_comparator':False}
        buckets=defaultdict(list)
        for unit in units:
            for name in [s['name'] for s in unit['segments']]+['first_occurrence']:
                buckets[(groups[unit['group_id']]['recipe']['family'],unit['configuration_id'],name)]
        for row in records:buckets[(row['family'],row['configuration_id'],row['slice'])].append(row)
        aggregates=[]
        for (family,conf,slice_name),bucket in sorted(buckets.items()):
            pops=defaultdict(list)
            for row in bucket:pops[row['group_id']].append(row)
            expected=[u for u in units if groups[u['group_id']]['recipe']['family']==family and u['configuration_id']==conf]
            def h(get):return avg([avg([get(r) for r in rs]) for rs in pops.values()]) if pops else None
            aggregates.append({'family':family,'configuration_id':conf,'slice':slice_name,'planned_episodes':len(expected),
                'available_episodes':len(bucket),'complete_parent_denominator':len(bucket)==len(expected),
                'missing_unit_ids':sorted({u['id'] for u in expected}-{r['unit_id'] for r in bucket}),
                'a2_difference':h(lambda r:r['a2_difference']),
                'a2_contributions':{k:h(lambda r:r['a2_contributions'][k]) for k in ('squared_mean_bias','forecast_variance','negative_twice_covariance')},
                'base_moments':{k:h(lambda r:r['base_moments'][k]) for k in ('mean_forecast','mean_truth','squared_mean_bias','forecast_variance','negative_twice_covariance','brier_mean')},
                'weighting':'moments within each slice, then equal seeds within population, then equal populations'})
        result={'schema':'value_logic.p310.transfer_failure_observer.v1','status':'PASS','start':start,'end':stamp(),
            'source_sha256':sha(Path(__file__)),'derivation_sha256':sha(HERE/'transfer_failure_derivation.md'),
            'numeric_result_sha256':sha(numeric_path),'amendment_lineage':lineage.receipt,
            'scheduled_episodes':126,'available_episodes':sum(r['status']=='audited' for r in parents),
            'checks_by_kind':dict(CHECKS),'parents':parents,'per_episode_slices':records,
            'population_advice_signatures':list(signature_groups.values()),'aggregates':aggregates,
            'scope':'Post-outcome exact finite-path explanation; no causal identification, sample-probability claim, policy rerun, fitted deployed comparator, or frozen endpoint replacement.'}
        save(out/'results.json',result)
        print(json.dumps(encode({k:v for k,v in result.items() if k not in ('parents','per_episode_slices','population_advice_signatures','aggregates')}),indent=2))
    except BaseException as error:
        save(out/'failure.json',{'status':'OBSERVER_FAILURE','start':start,'end':stamp(),'error_type':type(error).__name__,
            'error':str(error),'traceback':traceback.format_exc(),'scientific_stage_failure':False,'source_sha256':sha(Path(__file__))});raise


if __name__=='__main__':main()
