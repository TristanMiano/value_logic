"""Supplemental exact decomposition of sealed P3-10 broker forecasts/actions.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
No frozen module or paid method is imported. Pre-data derivation is separate.
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

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CHECKS = Counter()


def stamp():
    return {'utc': datetime.now(timezone.utc).isoformat(), 'monotonic_ns': time.monotonic_ns()}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rat(x):
    return F(*x) if isinstance(x, (list, tuple)) else F(x)


def require(ok, name, detail):
    CHECKS[name] += 1
    if not ok:
        raise AssertionError((name, detail))


def encode(x):
    if isinstance(x, F): return [x.numerator, x.denominator]
    if isinstance(x, dict): return {str(k): encode(v) for k,v in x.items()}
    if isinstance(x, (list, tuple)): return [encode(v) for v in x]
    return x


def save(path, value):
    with path.open('x') as out:
        json.dump(encode(value), out, indent=2, sort_keys=True, allow_nan=False)
        out.write('\n')


def means(rows, fields):
    if not rows: return {k: None for k in fields}
    return {k: sum((r[k] for r in rows), F(0)) / len(rows) for k in fields}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--numeric',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=False)
    before=stamp()
    try:
        lineage=Lineage()
        source=Path(args.numeric).resolve()
        numeric=json.loads(source.read_text())
        require(numeric['status']=='PASS','independent_numeric_pass',str(source))
        require(numeric['amendment_lineage']['manifest_sha256']==lineage.receipt['manifest_sha256'],
                'same_amendment',str(source))
        numeric_by_id={a['unit_id']:a for a in numeric['per_episode']}
        schedule=lineage.schedule
        units=[u for u in schedule['units'] if u['arm']=='broker' and u['engine'] in ('broker','mirror')]
        require(len(units)==len(numeric_by_id)==126,'full_numeric_unit_denominator',len(units))
        families={g['id']:g['recipe']['family'] for g in schedule['groups'] if g['arm']=='broker'}
        config=json.loads((REPO/'v3/experiments/protocol.v1.json').read_text())['arms']['broker']
        D=1<<config['action_bits'];mass=6<<config['state_bits']
        require(config['action_bits']==config['state_bits']==16,'declared_precision',config)
        bound=F(5,3*D)
        fields=['a2_brier_improvement','unrounded_reweighting_improvement','quantization_contribution',
                'binary_error_functional_improvement','variance_difference','hard_brier_gain',
                'terminal_error_gain','base_brier','live_brier','equal_brier','half_brier',
                'prior_known','selected','first_occurrence']
        summaries=[];all_rows=[];per_episode=[]
        for unit in units:
            uid=unit['id'];audit=numeric_by_id[uid]
            base={'unit_id':uid,'group_id':unit['group_id'],'configuration_id':unit['configuration_id'],
                  'family':families[unit['group_id']],'seed':unit['seed']}
            public,_=lineage.record('public',uid)
            paid=public['value']['paid_result'];episode=paid['episode'];trace=episode['trace']
            scored,_=lineage.record('evaluation','score-'+uid)
            score=scored['value']['score']
            available=(audit['status']=='audited' and score['validity_pass'] is True and score['full_horizon'] is True)
            if not available:
                per_episode.append(dict(base,status='unavailable',scheduled_horizon=score['horizon'],slices=[]))
                continue
            nt=[r for b in audit['blocks'] for r in b['rows']]
            require(len(nt)==len(trace)==score['horizon'],'whole_horizon',uid)
            rows=[]
            for block in audit['blocks']:
                weights=block['weights_before']
                require(sum(weights)==mass,'fixed_mass',uid)
                for nrow in block['rows']:
                    row=trace[nrow['index']];y=nrow['truth']
                    advice=row['advice'];r=F(sum(advice),6)
                    w=F(sum(a*v for a,v in zip(advice,weights)),mass)
                    p=rat(row['base_q']);q=rat(row['emitted_q'])
                    require(p==F((w*D).numerator//(w*D).denominator,D),'actual_dyadic_base',uid)
                    quant=(w-p)*(w+p-2*y)
                    reweight=(r-y)**2-(w-y)**2
                    a2=(r-y)**2-(p-y)**2
                    binary=(r+(1-2*r)*y)-(p+(1-2*p)*y)
                    variance=r*(1-r)-p*(1-p)
                    hard=(p-y)**2-(q-y)**2
                    terminal=nrow['base_terminal_error']-nrow['live_terminal_error']
                    require(a2==reweight+quant==binary-variance,'exact_three_way_a2_identity',[uid,nrow['index']])
                    require(F(0)<=w-p<=F(5,6*D) and abs(quant)<=bound,'pointwise_quantization_bound',uid)
                    require(quant>=0 if y==0 else quant<=0,'directional_rounding',uid)
                    prior=bool(nrow['prior_known']);selected=bool(nrow['selected'])
                    require(hard==int(prior)*(p-y)**2>=0,'exact_hard_forecast_identity',uid)
                    require(terminal==int(not selected and prior and nrow['base_terminal_error']==1),
                            'exact_terminal_correction_identity',uid)
                    require(not nrow['first_occurrence'] or not prior,'no_first_occurrence_hardening',uid)
                    require(rat(nrow['base_brier'])==(p-y)**2 and rat(nrow['live_brier'])==(q-y)**2 and
                            rat(nrow['frozen_equal_brier'])==(r-y)**2,'independent_numeric_loss_agreement',uid)
                    detail=dict(base,index=nrow['index'],block=block['block'],truth=y,
                        a2_brier_improvement=a2,unrounded_reweighting_improvement=reweight,
                        quantization_contribution=quant,binary_error_functional_improvement=binary,
                        variance_difference=variance,hard_brier_gain=hard,terminal_error_gain=terminal,
                        base_brier=(p-y)**2,live_brier=(q-y)**2,equal_brier=(r-y)**2,half_brier=F(1,4),
                        prior_known=int(prior),selected=int(selected),first_occurrence=int(nrow['first_occurrence']))
                    rows.append(detail)
            require(sum((r['base_brier'] for r in rows),F(0))==rat(score['base_issued_brier_sum']) and
                    sum((r['live_brier'] for r in rows),F(0))==rat(score['issued_brier_sum']),
                    'frozen_score_brier_totals',uid)
            slices=[]
            selections={s['name']:[r for r in rows if s['start']<=r['index']<s['stop']] for s in unit['segments']}
            selections['first_occurrence']=[r for r in rows if r['first_occurrence']]
            for name,part in selections.items():
                v=means(part,fields)
                slices.append(dict(slice=name,denominator=len(part),means=v))
                summaries.append(dict(base,slice=name,denominator=len(part),means=v,complete=True))
            per_episode.append(dict(base,status='audited',scheduled_horizon=len(rows),slices=slices,
                                    block_profiles=[dict(block=b,denominator=len(part),means=means(part,fields))
                                        for b,part in ((b,[r for r in rows if r['block']==b]) for b in range(len(audit['blocks'])))]))
            all_rows.extend(rows)
        grouped=defaultdict(list)
        for unit in units:
            for name in [s['name'] for s in unit['segments']]+['first_occurrence']:
                grouped[(families[unit['group_id']],unit['configuration_id'],name)]
        for row in summaries:grouped[(row['family'],row['configuration_id'],row['slice'])].append(row)
        aggregates=[]
        for (family,configuration,slice_name), bucket in sorted(grouped.items()):
            populations=defaultdict(list)
            for row in bucket:populations[row['group_id']].append(row)
            v={k:sum((sum((r['means'][k] for r in rs),F(0))/len(rs) for rs in populations.values()),F(0))/len(populations) for k in fields} if populations else {k:None for k in fields}
            expected=[u for u in units if families[u['group_id']]==family and u['configuration_id']==configuration]
            complete=len(bucket)==len(expected) and all(r['denominator']>0 for r in bucket)
            aggregates.append({'family':family,'configuration_id':configuration,'slice':slice_name,
                'planned_episodes':len(expected),'available_episodes':len(bucket),'complete_primary_denominator':complete,
                'unavailable_unit_ids':sorted({u['id'] for u in expected}-{r['unit_id'] for r in bucket}),
                'means_scope':'complete hierarchical cohort' if complete else 'available parents only; no primary positive claim',
                'per_episode_denominators':[{'unit_id':r['unit_id'],'positions':r['denominator']} for r in bucket],
                'hierarchical_means':v,'weighting':'equal seeds within population then equal populations',
                'a2_practical_threshold_met_descriptively':bool(complete and v['a2_brier_improvement']>=F(1,100)),
                'beats_constant_half_brier':bool(complete and v['base_brier']<F(1,4)),
                'base_brier_worse_than_equal':bool(complete and v['a2_brier_improvement']<0)})
        result={'schema':'value_logic.p310.forecast_mechanism_observer.v1','status':'PASS','start':before,'end':stamp(),
                'contributor':'ChatGPT (GPT-6 Astra Pro)','source_sha256':sha(Path(__file__)),
                'derivation_sha256':sha(HERE/'forecast_action_decomposition.md'),
                'numeric_source_sha256':sha(source),'amendment_lineage':lineage.receipt,
                'scheduled_episodes':126,'audited_episodes':sum(r['status']=='audited' for r in per_episode),
                'unavailable_unit_ids':[r['unit_id'] for r in per_episode if r['status']!='audited'],
                'checks_by_kind':dict(CHECKS),'quantization_bound':bound,'per_episode':per_episode,'aggregates':aggregates,
                'scope':'Exact supplemental decomposition on fixed recorded paths; no frozen endpoint replacement, free controller, fair-bit claim, or new economic claim.'}
        save(out/'results.json',result)
        print(json.dumps(encode({k:v for k,v in result.items() if k not in ('per_episode','aggregates')}),indent=2))
    except BaseException as exc:
        save(out/'failure.json',{'status':'OBSERVER_FAILURE','start':before,'end':stamp(),'error_type':type(exc).__name__,
             'error':str(exc),'traceback':traceback.format_exc(),'source_sha256':sha(Path(__file__)),
             'scientific_stage_failure':False,'checks_completed':dict(CHECKS)})
        raise


if __name__=='__main__':main()
