#!/usr/bin/env python3
"""Independent JSON-only review of forecast mechanism records; no project imports."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib,json,time,traceback

HERE=Path(__file__).resolve().parent
ROOT=Path('/workspace/scratch/095cdac579b7/value_logic')
WORK='v3/work_logs/P3_10_2026-10-11_S1/'
OUT=HERE/'independent_observation_v1'
OUT.mkdir(exist_ok=False)
READS={};CHECKS=Counter();DIFF=[];OFFICIAL={}

def digest(data):return hashlib.sha256(data).hexdigest()
def req(ok,label):
 CHECKS[label]+=1
 if not ok:raise AssertionError(label)
def loads(data):
 def pairs(items):
  x={}
  for k,v in items:
   if k in x:raise AssertionError('Duplicate JSON key '+k)
   x[k]=v
  return x
 return json.loads(data,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def read(path,parse=True):
 path=Path(path);data=path.read_bytes();key=str(path.relative_to(ROOT))
 rec={'path':key,'bytes':len(data),'sha256':digest(data)}
 req(key not in READS or READS[key]==rec,'read_stability')
 READS[key]=rec
 if key.startswith(('v3/experiments/final_v1/','v3/experiments/final_v1_amended_A1/','v3/experiments/frozen_v1/')):
  req(key in OFFICIAL and OFFICIAL[key]==rec,'matches_prior_independent_lineage_hash')
 return loads(data) if parse else data

def rat(x):return F(*x) if isinstance(x,list) else F(x)
def encode(x):
 if isinstance(x,F):return [x.numerator,x.denominator]
 if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [encode(v) for v in x]
 return x

def same(actual,expected,where):
 if actual!=encode(expected):DIFF.append({'where':where,'actual':actual,'expected':encode(expected)})
def qkey(q):return (q['semantics_version'],q['source_version'],q['variables'],tuple(tuple(c) for c in q['clauses']))
TRUTHS={}
def truth(q):
 key=qkey(q)
 if key not in TRUTHS:
  # Set-based Boolean assignment filtering is separate from the principal's
  # bit-parallel mask truth and never invokes the frozen private scorer.
  remaining=set(range(1<<q['variables']))
  for clause in q['clauses']:
   remaining={a for a in remaining if any(((a>>(abs(v)-1))&1)==int(v>0) for v in clause)}
   if not remaining:break
  TRUTHS[key]=int(bool(remaining))
 return TRUTHS[key]

def means(rows,fields):return {f:sum((x[f] for x in rows),F(0))/len(rows) for f in fields}
def verified_result(path):
 path=Path(path);seal=read(path.parent/'seal.json');start=read(path.parent/'start.json');result=read(path)
 req(digest(path.read_bytes())==seal['result_sha256'],'result_seal_hash')
 req(result['identity']==start['identity']==seal['identity'] and result['unit']==start['unit']
     and result['attempt']==start['attempt']==seal['attempt'],'result_outer_identity')
 return result

started=datetime.now(timezone.utc).isoformat();wall=time.monotonic_ns()
try:
 prior_hashfile=ROOT/(WORK+'reviews/certificate_reconstruction/final_observation_v4/source_hashes.json')
 prior_bytes=prior_hashfile.read_bytes()
 req(digest(prior_bytes)=='58b51d1f1379ddf41ed34f8949fdc315de524aa5e61a3f38fe5d2aba7e0c75fb','prior_independent_source_hash_manifest')
 OFFICIAL={x['path']:x for x in loads(prior_bytes)['consumed_files']}
 read(prior_hashfile)
 snapshot=read(HERE/'initial_snapshot_manifest.json')
 for src in snapshot['files']:
  data=read(ROOT/src['review_snapshot'],False)
  req(digest(data)==src['sha256'] and len(data)==src['bytes'],'review_snapshot_integrity')
 snap=HERE/'source_and_data'
 mechanism=read(snap/'forecast_mechanism_observation_A1/results.json')
 numeric=read(snap/'numeric_observation_A1/results.json')
 req(mechanism['status']==numeric['status']=='PASS','principal_observer_pass_status')
 req(mechanism['source_sha256']==digest(read(snap/'forecast_mechanism_observer.py',False)),'mechanism_source_pin')
 req(mechanism['derivation_sha256']==digest(read(snap/'forecast_action_decomposition.md',False)),'derivation_pin')
 req(mechanism['numeric_source_sha256']==digest(read(snap/'numeric_observation_A1/results.json',False)),'numeric_artifact_pin')
 req(numeric['source_sha256']==digest(read(snap/'numeric_transcript_observer.py',False)),'numeric_source_pin')
 req(mechanism['amendment_lineage']==numeric['amendment_lineage'],'same_exact_lineage_receipt')
 schedule=read(ROOT/'v3/experiments/frozen_v1/schedule.json')
 groups={g['id']:g for g in schedule['groups']}
 units=[u for u in schedule['units'] if u['arm']=='broker' and u['engine'] in ('broker','mirror')]
 req(len(units)==126 and len({u['id'] for u in units})==126,'126_unique_frozen_parents')
 expected_ids=[u['id'] for u in units]
 req([x['unit_id'] for x in mechanism['per_episode']]==expected_ids
     and [x['unit_id'] for x in numeric['per_episode']]==expected_ids,'exact_126_parent_rosters')
 composite=read(ROOT/'v3/experiments/final_v1_amended_A1/composite_public.json')
 refs={x['unit_id']:x for x in composite['seals']}
 inp=read(ROOT/'v3/experiments/final_v1_amended_A1/input_reference.json')
 inputs={x['unit_id']:verified_result(ROOT/x['origin_root']/x['result_path']) for x in inp['seals'] if groups[x['unit_id']]['arm']=='broker'}
 frozen=verified_result(ROOT/'v3/experiments/final_v1_amended_A1/stages/analysis/units/all-frozen-endpoints/attempt_01/result.json')['value']['broker']
 frozen_configs={(x['family'],x['configuration_id']):x for x in frozen['configuration_means'] if x['engine'] in ('broker','mirror')}
 by_num={x['unit_id']:x for x in numeric['per_episode']};by_mech={x['unit_id']:x for x in mechanism['per_episode']}
 fields=['a2_brier_improvement','unrounded_reweighting_improvement','quantization_contribution','binary_error_functional_improvement',
         'variance_difference','hard_brier_gain','terminal_error_gain','base_brier','live_brier','equal_brier','half_brier','prior_known','selected','first_occurrence']
 D=65536;M=6*D;BOUND=F(5,3*D)
 SAME=[];POINTS=[];SLICE_BUCKETS=defaultdict(list);signed_counts=Counter();exposures=Counter();perparents=[]
 for unit in units:
  uid=unit['id'];ref=refs[uid]
  outer=verified_result(ROOT/ref['origin_root']/ref['result_path']);paid=outer['value']['paid_result'];episode=paid['episode']
  score_outer=verified_result(ROOT/'v3/experiments/final_v1_amended_A1/stages/evaluation/units'/('score-'+uid)/'attempt_01/result.json')
  score=score_outer['value']['score'];queries=inputs[unit['group_id']]['value']['queries']
  req(score_outer['value']['public_result_sha256']==ref['result_sha256'],'score_to_public_binding')
  req(episode['status']=='success' and score['status']=='success' and score['full_horizon'] is True and score['validity_pass'] is True,'all_parent_paths_complete')
  req(by_num[uid]['status']==by_mech[uid]['status']=='audited','all_supplemental_parent_statuses')
  trace=episode['trace'];blocks=episode['blocks'];nblocks=by_num[uid]['blocks'];mp=by_mech[uid]
  req(len(trace)==len(queries)==score['horizon']==mp['scheduled_horizon'],'whole_horizon_match')
  req(len(blocks)==len(nblocks)==len(mp['block_profiles'])==len(trace)//4,'complete_block_partition')
  flat=[x for block in nblocks for x in block['rows']]
  req([x['index'] for x in flat]==[x['index'] for x in trace]==list(range(len(trace))),'exact_ordered_row_rosters')
  req(episode['hard_enabled']==unit['parameters']['hard'],'frozen_hard_mode')
  known={};seen=set();rows=[];blockrows=defaultdict(list);receiptmap={x['query_id']:x for x in episode['invoices']}
  req(len(receiptmap)==len(episode['invoices'])==len(blocks),'distinct_selected_receipts')
  for i,(row,nrow,qry) in enumerate(zip(trace,flat,queries)):
   bi=i//4;weights=blocks[bi]['weights_before']
   req(weights==nblocks[bi]['weights_before'] and len(weights)==6 and all(type(x)is int and x>0 for x in weights) and sum(weights)==M,'positive_recorded_fixed_mass')
   key=qkey(qry);y=truth(qry);first=key not in seen;prior=bool(episode['hard_enabled'] and key in known);sel=row['selected']
   req(type(sel)is bool,'selected_boolean')
   advice=row['advice'];req(len(advice)==6 and all(type(a)is int and a in (0,1) for a in advice),'six_binary_original_advice')
   r=F(sum(advice),6);w=F(sum(x*a for x,a in zip(weights,advice)),M);p=rat(row['base_q']);q=rat(row['emitted_q'])
   req(p==F(sum(x*a for x,a in zip(weights,advice))//6,D),'final_forecast_projection')
   req(q==(F(known[key]) if prior else p),'forecast_uses_prior_receipt_only')
   req(row['hard_before']==('checked' if prior else 'unresolved'),'raw_hard_before_timing')
   req(not first or not prior,'no_first_key_prior_hard')
   base_error=int(row['base_terminal']!=y);live_error=int(row['terminal_action']!=y)
   req(nrow['truth']==y and nrow['first_occurrence']==first and nrow['prior_known']==prior and nrow['selected']==sel,'independent_truth_and_chronology_agree_numeric')
   req(nrow['base_terminal_error']==base_error and nrow['live_terminal_error']==live_error,'independent_terminal_errors_agree_numeric')
   if sel:
    receipt=receiptmap[row['query_id']]
    req(receipt['checked'] is True and receipt['status']=='success' and receipt['answer']==y
        and row['purchased_label']==y and row['base_terminal']==row['terminal_action']==y,'selected_checked_terminal_truth')
    req(receipt['claim_key']==row['claim_key']==[qry['semantics_version'],qry['source_version'],qry['variables'],qry['clauses']],'current_receipt_full_key')
    if not prior:exposures['selected_without_prior_receipt']+=1;req(q==p,'new_purchase_cannot_retrofix_forecast')
   else:
    req(row['base_terminal']==row['base_action'] and row['terminal_action']==row['prospective_action'],'unselected_terminal_is_drawn_action')
   b0=(p-y)**2;b1=(q-y)**2;br=(r-y)**2;bw=(w-y)**2
   a2=br-b0;rw=br-bw;quant=bw-b0;binary=(r if y==0 else 1-r)-(p if y==0 else 1-p);variance=(r-r*r)-(p-p*p)
   hard=b0-b1;terminal=F(base_error-live_error)
   req(a2==rw+quant==binary-variance,'exact_a2_identities')
   req(quant==(w-p)*(w+p-2*y) and 0<=w-p<=F(5,6*D) and abs(quant)<=BOUND,'exact_quantization_factor_bound')
   req(quant>=0 if y==0 else quant<=0,'signed_quantization_by_truth')
   req(hard==int(prior)*b0 and hard>=0,'exact_prior_hard_brier_gain')
   req(terminal==int(not sel and prior and base_error==1) and terminal>=0,'exact_terminal_correction_gain')
   req(not first or (hard==terminal==0),'first_key_zero_hard_correction')
   if bi==0:req(rw==0,'first_block_reweighting_zero')
   same(nrow['base_brier'],b0,[uid,i,'numeric_base_brier']);same(nrow['live_brier'],b1,[uid,i,'numeric_live_brier']);same(nrow['frozen_equal_brier'],br,[uid,i,'numeric_equal_brier'])
   d=dict(index=i,block=bi,truth=y,a2_brier_improvement=a2,unrounded_reweighting_improvement=rw,quantization_contribution=quant,
          binary_error_functional_improvement=binary,variance_difference=variance,hard_brier_gain=hard,terminal_error_gain=terminal,
          base_brier=b0,live_brier=b1,equal_brier=br,half_brier=F(1,4),prior_known=F(prior),selected=F(sel),first_occurrence=F(first))
   rows.append(d);blockrows[bi].append(d);POINTS.append(d)
   exposures['positions']+=1;exposures['prior_hard_receipt_positions']+=prior;exposures['first_key_positions']+=first
   exposures['terminal_corrections']+=int(terminal);exposures['changed_forecasts']+=int(p!=q)
   if a2>0 and binary<0:signed_counts['pointwise_a2_positive_binary_negative']+=1
   if a2<0 and binary>0:signed_counts['pointwise_a2_negative_binary_positive']+=1
   if sel and episode['hard_enabled']:known[key]=y
   seen.add(key)
  same(score['base_issued_brier_sum'],sum((x['base_brier'] for x in rows),F(0)),[uid,'frozen_base_sum'])
  same(score['issued_brier_sum'],sum((x['live_brier'] for x in rows),F(0)),[uid,'frozen_live_sum'])
  selections={s['name']:[x for x in rows if s['start']<=x['index']<s['stop']] for s in unit['segments']}
  selections['first_occurrence']=[x for x in rows if x['first_occurrence']]
  req([x['slice'] for x in mp['slices']]==list(selections),'exact_parent_slice_roster')
  same(score['first_occurrence']['indices'],[x['index'] for x in selections['first_occurrence']],[uid,'frozen_first_indices'])
  for name,part in selections.items():
   m=means(part,fields);actual=next(x for x in mp['slices'] if x['slice']==name)
   same(actual,{'slice':name,'denominator':len(part),'means':m},[uid,name,'complete_slice'])
   met=score['first_occurrence'] if name=='first_occurrence' else score['segments'][name]
   req(met['full_horizon'] is True and met['horizon']==len(part),'frozen_slice_complete_denominator')
   for rawkey,derived in [('base_brier_mean','base_brier'),('brier_mean','live_brier'),('uniform_brier_mean','equal_brier')]:same(met[rawkey],m[derived],[uid,name,rawkey])
   SLICE_BUCKETS[(groups[unit['group_id']]['recipe']['family'],unit['configuration_id'],name)].append({'unit':unit,'denominator':len(part),'means':m})
  for b,part in blockrows.items():same(mp['block_profiles'][b],{'block':b,'denominator':len(part),'means':means(part,fields)},[uid,b,'block_profile'])
  perparents.append({'unit_id':uid,'rows':len(rows),'blocks':len(blockrows),'slices':len(selections),'complete':True})
 req(len(SLICE_BUCKETS)==len(mechanism['aggregates'])==56,'56_hierarchical_slice_cells')
 reported={(x['family'],x['configuration_id'],x['slice']):x for x in mechanism['aggregates']}
 req(set(reported)==set(SLICE_BUCKETS),'exact_aggregate_cell_roster')
 aggregate_rows=[]
 for (family,configuration,name),rows in sorted(SLICE_BUCKETS.items()):
  req(len(rows)==6 and len({(x['unit']['group_id'],x['unit']['seed']) for x in rows})==6,'six_distinct_population_seed_parents')
  populations=defaultdict(list)
  for x in rows:populations[x['unit']['group_id']].append(x)
  req(len(populations)==2 and all(len(v)==3 for v in populations.values()),'two_populations_three_seeds')
  req(len({json.dumps(x['unit']['stakes'],sort_keys=True) for x in rows})==1,'configuration_fixes_stakes')
  expected={f:sum((sum((x['means'][f] for x in pop),F(0))/3 for pop in populations.values()),F(0))/2 for f in fields}
  actual=reported[(family,configuration,name)]
  same(actual['hierarchical_means'],expected,[family,configuration,name,'all_hierarchical_means'])
  same(actual['per_episode_denominators'],[{'unit_id':x['unit']['id'],'positions':x['denominator']} for x in rows],[family,configuration,name,'episode_denominators'])
  req(actual['planned_episodes']==actual['available_episodes']==6 and actual['complete_primary_denominator'] is True and actual['unavailable_unit_ids']==[], 'complete_aggregate_denominator')
  same(actual['a2_practical_threshold_met_descriptively'],expected['a2_brier_improvement']>=F(1,100),[family,configuration,name,'threshold'])
  same(actual['beats_constant_half_brier'],expected['base_brier']<F(1,4),[family,configuration,name,'half_comparison'])
  same(actual['base_brier_worse_than_equal'],expected['a2_brier_improvement']<0,[family,configuration,name,'adverse_a2'])
  frozen_config=frozen_configs[(family,configuration)]
  frow=next(x for x in frozen_config['prespecified_slices'] if x['slice']==name)
  same(frow['uniform_minus_base_brier'],expected['a2_brier_improvement'],[family,configuration,name,'frozen_a2'])
  same(frow['practical_learning_effect'],actual['a2_practical_threshold_met_descriptively'],[family,configuration,name,'frozen_threshold'])
  same(frow['forecast_readout_means']['equal_mixture_brier_mean'],expected['equal_brier'],[family,configuration,name,'frozen_equal_reference'])
  for key,field in [('base_brier_mean','base_brier'),('brier_mean','live_brier'),('uniform_brier_mean','equal_brier')]:same(frow['means'][key],expected[field],[family,configuration,name,'frozen_'+key])
  if name=='whole':same(frozen_config['uniform_minus_base_brier'],expected['a2_brier_improvement'],[family,configuration,'frozen_main_a2'])
  req(expected['a2_brier_improvement']==expected['unrounded_reweighting_improvement']+expected['quantization_contribution']==expected['binary_error_functional_improvement']-expected['variance_difference'],'hierarchical_exact_additive_identities')
  req(abs(expected['quantization_contribution'])<=BOUND,'hierarchical_quantization_bound')
  if expected['a2_brier_improvement']>=F(1,100):req(expected['unrounded_reweighting_improvement']>=F(1,100)-BOUND,'practical_effect_requires_reweighting')
  aggregate_rows.append({'family':family,'configuration_id':configuration,'slice':name,'means':expected,
      'a2_practical':actual['a2_practical_threshold_met_descriptively'],'beats_half':actual['beats_constant_half_brier'],
      'adverse_a2':actual['base_brier_worse_than_equal']})
 result={'schema':'p310.independent_forecast_mechanism_review_observer.v1','status':'PASS' if not DIFF else 'FAIL','signed_by':'ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction',
    'principal_mechanism_result_sha256':digest(read(snap/'forecast_mechanism_observation_A1/results.json',False)),
    'parents':len(perparents),'positions':len(POINTS),'blocks':sum(x['blocks'] for x in perparents),'hierarchical_slice_cells':len(aggregate_rows),
    'available_parents':126,'unavailable_parents':0,'truths_computed_from_distinct_full_public_keys':len(TRUTHS),
    'all_reported_parent_slices_block_profiles_and_hierarchical_means_exact':not DIFF,
    'all56_cells_agree_with_frozen_a2':not DIFF,'checks_by_kind':dict(CHECKS),'mismatches':DIFF,'observed_counts':dict(exposures),'sign_counts':dict(signed_counts),
    'quantization_bound':BOUND,'pointwise_quantization_min':min(x['quantization_contribution'] for x in POINTS),'pointwise_quantization_max':max(x['quantization_contribution'] for x in POINTS),
    'hierarchical_quantization_min':min(x['means']['quantization_contribution'] for x in aggregate_rows),'hierarchical_quantization_max':max(x['means']['quantization_contribution'] for x in aggregate_rows),
    'aggregate_practical_a2_cells':sum(x['a2_practical'] for x in aggregate_rows),'aggregate_adverse_a2_cells':sum(x['adverse_a2'] for x in aggregate_rows),
    'aggregate_beats_half_cells':sum(x['beats_half'] for x in aggregate_rows),'aggregates':aggregate_rows,'parents_checked':perparents,
    'scope':'Supplemental exact arithmetic over fixed recorded paths; independent set-based truth; no paid worker, generator, private scorer, frozen analyzer or principal observer execution',
    'principal_clock_credit_ns':0,'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'wall_ns':time.monotonic_ns()-wall}
 name='results.json'
except BaseException as e:
 result={'status':'OBSERVER_FAILURE','error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc(),'mismatches_before_failure':DIFF,'checks_before_failure':dict(CHECKS),'failed_observer_preserved':True,'principal_clock_credit_ns':0}
 name='failure.json'
(OUT/name).write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
(OUT/'source_hashes.json').write_text(json.dumps({'observer_source':{'path':str(Path(__file__).relative_to(ROOT)),'sha256':digest(Path(__file__).read_bytes())},'reads':sorted(READS.values(),key=lambda x:x['path'])},indent=2,sort_keys=True)+'\n')
(OUT/'signature.json').write_text(json.dumps({'signed_by':'ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction','signed_utc':datetime.now(timezone.utc).isoformat(),'outputs':[{'path':name,'sha256':digest((OUT/name).read_bytes())},{'path':'source_hashes.json','sha256':digest((OUT/'source_hashes.json').read_bytes())}],'principal_clock_credit_ns':0},indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':result['status'],'path':str(OUT/name),'mismatches':len(DIFF)}))
raise SystemExit(0 if result['status']=='PASS' else 1)
