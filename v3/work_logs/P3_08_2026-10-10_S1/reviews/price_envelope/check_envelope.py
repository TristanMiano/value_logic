"""Independent sealed DEVELOPMENT repricing reconstruction; no policy imports.

Contributor: ChatGPT (GPT-6 Astra Pro), same-model nonblind. Input evidence is
read-only. Errors use the sealed evaluator target, not a new SAT oracle proof.
Pairwise feasibility is checked separately against all rational crossing cells.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip
import json
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
WORK = HERE.parents[1]
ANALYSIS = WORK/'development/price_envelope/run_v1'
ARCHIVES = {'common_v2':WORK/'development/common_v2',
            'reuse_v1_1':WORK/'development/selected_receipt_reuse/main_v1_1'}
DETERMINISTIC = {'proof_enumeration','proof_dpll','exact_enumeration','exact_dpll',
                 'exact_cache','exact_cache_hashed','no_compute_0','no_compute_1'}
RANDOM_ORDINARY = {'probability_cost','ordinary_combo','ordinary_combo_hashed'}
SOURCE = 50115


def read(p): return json.loads(p.read_text())
def digest(p): return sha256(p.read_bytes()).hexdigest()
def pair(x): return None if x is None else [x.numerator,x.denominator]
def unpack(x): return None if x is None else F(*x)


def meter_ok(m):
    assert m['total'] == sum(m['by_category'].values()) == sum(x['units'] for x in m['operations'])
    assert len(m['operations']) == len({(x['category'],x['operation']) for x in m['operations']})
    for c,n in m['by_category'].items():
        assert n == sum(x['units'] for x in m['operations'] if x['category']==c)


def objective(line,x): return line['terminal_errors']+line['cold_units_current_common_bundle']*x


def feasible(line, group, field='cold_units_current_common_bundle'):
    # Independently write the condition as a*x <= b, with x >= 0.
    lower,upper = F(0),None
    for other in group:
        a = line[field]-other[field]
        b = other['terminal_errors']-line['terminal_errors']
        if a == 0:
            if b < 0:return None
        elif a > 0:
            bound=F(b,a)
            upper=bound if upper is None else min(upper,bound)
        else:
            lower=max(lower,F(b,a))
    if upper is not None and upper<lower:return None
    return lower,upper


def crossing_cells(group):
    # This construction does not solve per-line inequalities. It evaluates the
    # lower envelope at every crossing, every intervening cell, and its tail.
    points={F(0)}
    for a,b in combinations(group,2):
        difference=a['cold_units_current_common_bundle']-b['cold_units_current_common_bundle']
        if difference:
            x=F(b['terminal_errors']-a['terminal_errors'],difference)
            if x>=0:points.add(x)
    points=sorted(points)
    cells=[(x,x,x) for x in points]
    cells += [(a,b,(a+b)/2) for a,b in zip(points,points[1:])]
    cells += [(points[-1],None,points[-1]+1)]
    active=defaultdict(list)
    for left,right,witness in cells:
        values=[objective(line,witness) for line in group]
        best=min(values)
        for line,val in zip(group,values):
            if val==best:active[line['record']].append((left,right))
    result={}
    for rid,ranges in active.items():
        ranges.sort(key=lambda x:x[0])
        low,high=ranges[0]
        for left,right in ranges[1:]:
            assert high is None or left<=high,('disconnected optimal set',rid)
            high=None if high is None or right is None else max(high,right)
        result[rid]=(low,high)
    return result,len(points),len(cells)


def sealed_lines():
    lines=[];record_count=position_count=0;core_sets={};score_hashes={};truths={}
    for name,base in ARCHIVES.items():
        run=base/'run'
        for folder,sealf in ((run,'public_seal.json'),(run/'private','seal.json')):
            for source in read(folder/sealf)['files']:
                p=folder/source['path'];assert digest(p)==source['sha256']
                if 'bytes' in source:assert p.stat().st_size==source['bytes']
        before=read(run/'source_before.json')['sources']
        assert before==read(run/'source_after.json')['sources']
        for src in before:
            p=base/'source'/src['path'];assert digest(p)==src['sha256'] and p.stat().st_size==src['bytes']
        tf=read(run/'private/truth.json')
        assert tf['public_seal_sha256']==digest(run/'public_seal.json')
        truths[name]=tf['answers']
        scores={r['run_id']:r for r in read(run/'private/scores.json')['runs']}
        index={r['run_id']:r for r in read(run/'public_index.json')['records']}
        score_hashes[name]=digest(run/'private/scores.json')
        assert len(scores)==len(index)==(186 if name=='common_v2' else 48)
        seen=set();det_by_scenario=defaultdict(set)
        with gzip.open(run/'public_records.jsonl.gz','rb') as stream:
            for raw in stream:
                record=json.loads(raw);rid=record['run_id'];cfg=record['configuration'];e=record['episode']
                assert rid not in seen;seen.add(rid)
                assert sha256(raw.rstrip(b'\n')).hexdigest()==index[rid]['record_sha256']
                score=scores[rid]
                assert all(score[k]==v for k,v in index[rid].items())
                assert score['configuration']==cfg and e['status']==score['status']=='success'
                scenario=record['scenario'] if name=='common_v2' else cfg['scenario']
                target=truths[name][scenario]
                assert len(e['trace'])==len(target)
                assert all(r['index']==i for i,r in enumerate(e['trace']))
                errors=sum(r['terminal_action']!=y for r,y in zip(e['trace'],target))
                assert errors==score['terminal_errors']
                source_key='common_source_invoice' if name=='common_v2' else 'source_invoice'
                sources_key='common_sources' if name=='common_v2' else 'sources'
                meter_ok(e['meter']);meter_ok(record[source_key])
                sources=record[sources_key]
                for src in sources:
                    p=base/'source'/src['path'];assert digest(p)==src['sha256'] and p.stat().st_size==src['bytes']
                bill=sum(2*((s['bytes']+7)//8)+(s['bytes']+72)//64 for s in sources)
                expected_source=48274 if name=='common_v2' else SOURCE
                assert bill==record[source_key]['total']==score['source_units']==expected_source
                assert score['local_units']==e['meter']['total']
                assert score['cold_units']==score['local_units']+expected_source
                current_sources={s['path']:(s['bytes'],s['sha256']) for s in sources}
                if name in core_sets:assert current_sources==core_sets[name]
                else:core_sets[name]=current_sources
                broker=name=='reuse_v1_1' or cfg['kind']=='broker'
                deterministic=False
                if not broker:
                    assert cfg['method'] in DETERMINISTIC|RANDOM_ORDINARY
                    deterministic=cfg['method'] in DETERMINISTIC
                    if deterministic:
                        assert cfg['seed']==11 and e['random_bits_consumed']==0 and e['randomness'] is None
                        det_by_scenario[scenario].add(cfg['method'])
                lines.append({'record':name+'/'+rid,'scenario':scenario,'seed':cfg['seed'],
                    'configuration':cfg,'deterministic_across_seeds':deterministic,
                    'terminal_errors':errors,'local_units':e['meter']['total'],
                    'cold_units_current_common_bundle':e['meter']['total']+SOURCE,
                    'source_procurement_transfer':SOURCE-expected_source,
                    'recorded_acquisition_price':cfg.get('unit_price'),
                    'ordinary_kernel_equivalent':broker,'ordinary_control':not broker})
                record_count+=1;position_count+=len(e['trace'])
        assert seen==scores.keys()==index.keys()
        if name=='common_v2':
            assert set(det_by_scenario)=={'cold_mixed','repeat_online','cheap_structure'}
            assert all(s==DETERMINISTIC for s in det_by_scenario.values())
    assert truths['common_v2']==truths['reuse_v1_1']
    old,new=core_sets['common_v2'],core_sets['reuse_v1_1']
    assert all(new[p]==v for p,v in old.items())
    extra=set(new)-set(old);assert extra=={'v3/experiments/p308_cached_service.py'}
    n,_=new[next(iter(extra))]
    assert n==6924 and 2*((n+7)//8)+(n+72)//64==1841==SOURCE-48274
    return lines,{'records':record_count,'trace_positions':position_count,
                  'score_hashes':score_hashes,'added_paid_source':sorted(extra),'added_source_units':1841}


def run():
    for row in read(HERE/'plan.json')['sources']:
        p=ROOT/row['path'];assert digest(p)==row['sha256'] and p.stat().st_size==row['bytes']
    for row in read(ANALYSIS/'manifest.json')['files']:
        p=ANALYSIS/row['path'];assert digest(p)==row['sha256'] and p.stat().st_size==row['bytes']
    assert digest(ANALYSIS/'p308_price_envelope.py')==digest(ROOT/'v3/experiments/p308_price_envelope.py')
    saved=read(ANALYSIS/'results.json')
    lines,summary=sealed_lines()
    assert len(lines)==234
    assert {x['record']:x for x in lines}=={x['record']:x for x in saved['lines']}
    assert len(saved['lines'])==234 and len(saved['envelopes'])==9
    assert saved['common_source_units']==SOURCE and saved['policy_runs_added']==0
    assert saved['hindsight_envelope_is_deployable_selector'] is False
    assert saved['ordinary_kernel_equivalence_retained'] is True
    assert saved['common_scores_sha256']==summary['score_hashes']['common_v2']
    assert saved['reuse_scores_sha256']==summary['score_hashes']['reuse_v1_1']
    groups=[];all_intervals=[]
    for scenario in ('cold_mixed','repeat_online','cheap_structure'):
        for seed in (11,29,47):
            group=[x for x in lines if x['scenario']==scenario and (x['seed']==seed or x['deterministic_across_seeds'])]
            expected={x['record']:interval for x in group if (interval:=feasible(x,group)) is not None}
            assert all(feasible(x,group,'local_units')==feasible(x,group) for x in group)
            alternate,crossings,cells=crossing_cells(group)
            assert alternate==expected
            found=[x for x in saved['envelopes'] if x['scenario']==scenario and x['seed']==seed]
            assert len(found)==1;env=found[0]
            assert env['line_count']==len(group)
            observed={x['record']:(unpack(x['lambda_min']),unpack(x['lambda_max'])) for x in env['frontier']}
            assert len(observed)==len(env['frontier']) and observed==expected
            line_map={x['record']:x for x in group}
            for r in env['frontier']:
                line=line_map[r['record']];low,high=expected[r['record']]
                assert r['terminal_errors']==line['terminal_errors'] and r['cold_units']==line['cold_units_current_common_bundle']
                assert r['positive_width']==(high is None or low<high)
                witness=unpack(r['rational_witness'])
                assert witness>=low and (high is None or witness<=high)
                assert unpack(r['witness_objective'])==objective(line,witness)
                assert all(objective(line,witness)<=objective(x,witness) for x in group)
                assert set(r['coincident_record_lines'])=={x['record'] for x in group if (x['terminal_errors'],x['cold_units_current_common_bundle'])==(line['terminal_errors'],line['cold_units_current_common_bundle'])}
                assert r['has_identical_ordinary_kernel']==line['ordinary_kernel_equivalent']
                assert r['ordinary_control']==line['ordinary_control']
                binding={}
                for name,x in (('lower',low),('upper',high)):
                    binding[name]=[] if x is None else [q['record'] for q in group if q['record']!=r['record'] and objective(q,x)==objective(line,x)]
                all_intervals.append({'scenario':scenario,'seed':seed,**r,'binding_at_endpoints':binding})
            display=F(1,30000)
            assert unpack(env['display_price'])==display
            values=[objective(x,display) for x in group];best=min(values)
            assert unpack(env['display_objective'])==best
            assert set(env['display_winners'])=={x['record'] for x,v in zip(group,values) if v==best}
            assert env['native_controller_at_display_price_was_not_executed'] is True
            distinct={}
            for r in env['frontier']:
                key=(r['terminal_errors'],r['cold_units'])
                if key not in distinct:distinct[key]={'terminal_errors':key[0],'cold_units':key[1],'lambda_min':r['lambda_min'],'lambda_max':r['lambda_max'],'positive_width':r['positive_width'],'records':[]}
                distinct[key]['records'].append(r['record'])
            groups.append({'scenario':scenario,'seed':seed,'eligible_lines':len(group),
                'ordinary_control_lines':sum(x['ordinary_control'] for x in group),
                'broker_lines_with_ordinary_kernel':sum(x['ordinary_kernel_equivalent'] for x in group),
                'deterministic_controls_reused':sum(x['deterministic_across_seeds'] for x in group),
                'acquisition_prices_retained':{m:sorted({str(x['recorded_acquisition_price']) for x in group if x['configuration'].get('method')==m}) for m in ('ordinary_combo','ordinary_combo_hashed')},
                'frontier_records':len(expected),'positive_width_frontier_records':sum(x['positive_width'] for x in env['frontier']),
                'zero_price_only_frontier_records':sum(x['lambda_min']==x['lambda_max']==[0,1] for x in env['frontier']),
                'positive_price_only_singletons':sum(x['lambda_min']==x['lambda_max'] and x['lambda_min']!=[0,1] for x in env['frontier']),
                'pairwise_crossings_including_zero':crossings,'crossing_cells_and_points_evaluated':cells,
                'distinct_frontier_lines':list(distinct.values()),'display_winners':env['display_winners']})
    assert len(groups)==9 and all(x['ordinary_control_lines']==19 and x['deterministic_controls_reused']==8 for x in groups)
    summary.update({'groups':groups,'eligible_group_lines':sum(x['eligible_lines'] for x in groups),
                    'frontier_record_intervals':len(all_intervals),
                    'positive_width_record_intervals':sum(x['positive_width'] for x in all_intervals),
                    'zero_price_only_record_intervals':sum(x['lambda_min']==x['lambda_max']==[0,1] for x in all_intervals),
                    'ordinary_control_records':sum(x['ordinary_control'] for x in lines),
                    'broker_records_with_identical_ordinary_kernel':sum(x['ordinary_kernel_equivalent'] for x in lines)})
    details={'stage':'DEVELOPMENT','reconstructed_lines':lines,'all_verified_intervals':all_intervals}
    with (HERE/'details.json').open('x') as f:json.dump(details,f,indent=2,sort_keys=True);f.write('\n')
    return summary


if __name__=='__main__':
    result={'stage':'DEVELOPMENT','started_utc':datetime.now(timezone.utc).isoformat(),
            'script_sha256':digest(Path(__file__)),'research_credit_seconds':0,'policy_or_report_runs':0,
            'reviewer':'ChatGPT (GPT-6 Astra Pro), same-model nonblind'}
    try:result['summary']=run();result['pass']=True
    except Exception:result['pass']=False;result['exception']=traceback.format_exc()
    result['finished_utc']=datetime.now(timezone.utc).isoformat()
    with (HERE/'results.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='summary'}|{'summary':{k:v for k,v in result.get('summary',{}).items() if k!='groups'}},sort_keys=True))
    raise SystemExit(0 if result['pass'] else 1)
