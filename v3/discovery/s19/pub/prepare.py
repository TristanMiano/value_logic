"""Rebuild the s19 administrative handoff from the immutable main baseline.

No research clock or scientific probe is run. Historical row bytes are retained.
"""
from pathlib import Path
from decimal import Decimal
import copy
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[4]
HERE=ROOT/'v3/discovery/s19'
DISC=HERE.parent
BASE='d1c7443f216ddb37c6083d5c503618d7a2441e97'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(n):return dict(path='s19/'+n,sha256=sha(HERE/n))
a=read(HERE/'effective_actuals.json')
assert a['research_ns']==14403095000000 and not a['clock_active']
metrics=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',
 scope_id='s19_broad_ranges_and_paid_proofs_v1',observation_date_utc='2026-10-27',
 observed_in_row='s19_cp01',age_in_recurrences=0,
 scalar_range=dict(event='V19-R/v1',local_LPs_at_most='2*n*2^k',
  combination_work='O(n*3^k+n*2^k*log(n*2^k))',intervals_at_most='n*2^k',
  comparator='s18 n^k attainer assignments and ordinary disjunctive/max-affine inference',
  observed_speedup=None,ordinary_equivalent='ties',
  noisy_example_ranges=[['21','21.2'],['21.9','22.2']],rejected_band=['21.4','21.6'],
  reciprocal_absolute_bound='10/3',anchor_cases=180,source_witness_checks=472,
  certificate_bundles=44,bounded_slices=854,empty_slices=336,rejected_corruptions=273),
 sparse_extension=dict(incidence_cycle_rank='t',local_LPs='O(2^t*(n+k))',
  intervals_at_most='2^t',development_cases=74,certificate_messages=255,
  rejected_corruptions=376,novelty='UNASSESSED'),
 proof_service=dict(scope='24 artificial CNF streams; proof ticks plus declared fallback tariff; controller overhead separate',
  fallback_bill='15079/3',uniform_bill='7570',first_advice_bill='16951/3',second_advice_bill='16597/3',
  uniform_change_vs_fallback_percent=str(Decimal(7570*3-15079)*100/Decimal(15079)),
  first_advice_change_vs_fallback_percent=str(Decimal(16951-15079)*100/Decimal(15079)),
  second_advice_change_vs_fallback_percent=str(Decimal(16597-15079)*100/Decimal(15079)),
  hindsight_advice_bill='14282/3',hindsight_is_oracle=True,
  uniform_controller_membership=23897,uniform_controller_credit=5083,
  second_advice_controller_membership=28568,second_advice_controller_credit=7982,
  ordinary_equivalent='ties',complete_economic_saving=None),
 readiness=dict(event='V19-R/v1',range_percent=[50,80],central_percent=65,
  status='continue with specific blockers; no promotion',record='s19/readiness.md'),
 o18=dict(event='O18-M/v1 unchanged',range_percent=[35,70],central_percent=50,
  central_change_percentage_points=-10,record='s19/o18_assessment.md'),
 n16=dict(event='N16-C/v1',range_percent=[55,80],central_percent=65,
  measurement_status='carried from s18; not reassessed'),
 carried_resources=dict(observed_in_row='s10_cp01',age_in_recurrences=9,
  audit_fee_reduction_percent=57.12,named_work_reduction_percent=9.53,
  note='Dated carry only; no fresh audit stream or complete-cost gain.'),
 sources=[record(n) for n in ['claim.md','anchor_ranges.md','anchor_range_result.json',
  'range_certificates.md','range_cert_result.json','robust_gap.md','range_decisions.md',
  'forest_receipts.md','forest_result.json','forest_cert_result.json','proof_integration.md',
  'proof_machine_result.json','o18_assessment.md','ordinal_perceptron.md',
  'perceptron_v1_failure.json','perceptron_result.json','readiness.md',
  'scientific_assessment.md','comparison.md','verification_targets.md']])
write(HERE/'progress_metrics.json',metrics)
oldtext=subprocess.check_output(['git','show',BASE+':v3/discovery/recurrences.json'],cwd=ROOT).decode('utf-8')
d=json.loads(oldtext);assert len(d['rows'])==28
oldrows=copy.deepcopy(d['rows']);fixed=copy.deepcopy(oldrows[-1]['fixed_metrics'])
for v in fixed.values():
 if isinstance(v,dict):
  if 'age_in_recurrences' in v:v['age_in_recurrences']+=1
  v.update(carried_in_row='s19_cp01',carried_from_row='s18_cp01',
   reason='No comparable fresh legacy-stream measurement or F01 reassessment in s19; original scope/date retained.')
fixed['families_total']=dict(scope_id='c001_numbered_families',measurement_status='current inventory',
 observed_in_row='s19_cp01',age_in_recurrences=0,value=36,units='families',
 previous_comparable_row='s18_cp01',absolute_delta=0,delta_units='families',
 sources=[dict(path='candidates.md',locator='s19 constructive update; variants not separate families')],
 interpretation='Breadth inventory, not readiness.')
ready=dict(candidate='V19-R/v1',range_percent=[50,80],central_percent=65,
 status='continue developing; no promotion',event='s19/claim.md',record='s19/readiness.md',
 o18_same_event=metrics['o18'],n16_carried=metrics['n16'])
row=dict(id='s19_cp01',label='s19 four-hour broad discovery',checkpoint='s19/checkpoint.md',
 session='s19',contributor='Codex (GPT-6)',research_ns=a['research_ns'],
 cumulative_research_ns=a['program_research_ns'],research_minutes_rounded=240,
 cumulative_minutes_rounded=(a['program_research_ns']+30000000000)//60000000000,
 new_family_ids=[],cumulative_new_family_count=36,
 metric_summary='Exact gap-preserving ranges and rational certificates; O18 novelty estimate lower; actual shared-proof bill exceeds fallback; no fresh audit-fee or full-cost saving.',
 metric_values=dict(scope_id=metrics['scope_id'],source='s19/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json')),
 description='Broad discovery; capped O18 screen; V19-R/v1 bounded event introduced; ordinary reductions parked; no promotion.',
 time_evidence=dict(actuals='s19/effective_actuals.json',sha256=sha(HERE/'effective_actuals.json'),
 actuals_field='session_research_ns',cumulative_actuals_field='cycle_research_ns',
 research_closed_utc=a['research_closed_utc'],note='153 segments;21 research exclusions plus O/context recovery; publication zero credit.'),
 metric_sources=metrics['sources'],fixed_metrics=fixed,candidate_readiness=ready)
d.update(prepared_date_utc='2026-10-27',source_commit=BASE,previous_table_commit=BASE,
 latest_checkpoint='s19/checkpoint.md',latest_effective_actuals='s19/effective_actuals.json',
 row_scope='29 chronological boundaries; one s19 recurrence; all28 earlier row objects byte-preserved.',
 total_research_ns=a['program_research_ns'],total_minutes_rounded=row['cumulative_minutes_rounded'],
 total_research_minutes=a['program_research_minutes'],program_research_ns=a['program_research_ns'],
 phase_research_ns=a['phase_research_ns'],active_scope_id=metrics['scope_id'],active_row_ids=['s19_cp01'],
 current_separate_scope_ids=[metrics['scope_id']],current_readiness_assessment=ready)
d['visible_resource_metrics']['s19']=dict(source='s19/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json'),observation_date_utc='2026-10-27',age_at_s19=0)
d['current_forecast'].update(age_in_recurrences=9,carried_in_row='s19_cp01',carried_from_row='s18_cp01',reason='F01 not reassessed in s19; distinct V19 event introduced.')
d['carried_f01_forecast']=copy.deepcopy(d['current_forecast'])
forecast=dict(assessment_id='V19_R_s19',event_id='V19-R/v1',candidate_id='retained_optimum_ranges',
 candidate_version='V19-R/v1',scope_id='candidate_specific_confirmation_event',
 observed_in_row='s19_cp01',measurement_status='first same-model assessment',
 assessment_status='continue with specific blockers; no promotion',central_percent=65,
 probability_range_percent=[50,80],value=65,units='subjective probability percent',
 previous_comparable_assessment_id=None,change_since_previous_assessment_percentage_points=None,
 gap_to_80_central_percentage_points=15,calibration_status='not established',
 sources=[record('claim.md'),record('readiness.md')],
 uncertainty='Judgmental range, not a confidence interval; new event distinct from N16, O18 and F01.')
d['forecast_events']['V19-R/v1']=dict(event_id='V19-R/v1',claim='s19/claim.md',
 assessment='s19/readiness.md',standard='Useful moderately novel exact-range algorithm/certificate/consequence synthesis',
 optional_extensions_required=False,confirmation_plan_status='not frozen; DEVELOPMENT')
d['forecast_assessments'].append(forecast)
d['current_forecast']=forecast
d['readiness_assessment_history'].append(copy.deepcopy(ready))
d['rendered_table']['row_ids'].append('s19_cp01');d['rendered_table']['latest_row_id']='s19_cp01'
d['rows']='__RAW_ROWS__'
start=oldtext.index('[',oldtext.index('"rows"'));_,end=json.JSONDecoder().raw_decode(oldtext,start)
rawarray=oldtext[start:end].rstrip()[:-1].rstrip()+',\n'+'\n'.join('    '+s for s in json.dumps(row,indent=2,ensure_ascii=False).splitlines())+'\n  ]'
out=json.dumps(d,indent=2,ensure_ascii=False).replace('"__RAW_ROWS__"',rawarray)+'\n'
(DISC/'recurrences.json').write_bytes(out.encode('utf-8'));assert json.loads(out)['rows'][:28]==oldrows

p=ROOT/'v3/plan.v1.json';plan=read(p)
for field in ['last_completed_session','last_preserved_session','last_discovery_session']:plan[field]='v3/discovery/s19/session.md'
plan['active_session']=None
plan['observed_progress'].update(research_ns=a['phase_research_ns'],research_minutes=a['phase_research_minutes'],source='v3/discovery/s19/effective_actuals.json',evidence_disposition='s19 closed; explicit exclusions and context recovery reconciled; publication zero credit.')
pr=plan['discovery_program'];pr.update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],latest_checkpoint='v3/discovery/s19/checkpoint.md',actuals='v3/discovery/s19/effective_actuals.json')
pr['current_cycle'].update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],session='v3/discovery/s19/session.md',actuals='v3/discovery/s19/effective_actuals.json',clock_active=False,session_status='closed_author_directed_four_hour_handoff')
if 'v3/discovery/s19/session.md' not in pr['sessions']:pr['sessions'].append('v3/discovery/s19/session.md')
pr['execution_cadence'].update(last_closed_session='s19',last_increment_research_ns=a['research_ns'],last_increment_research_minutes=a['research_minutes'],last_override_authority='v3/decisions/2026-10-26_s19_broad_four_hours.md')
promotion=pr['promotion'];promotion.update(forecast_status='V19-R/v1 50-80%, central65%; O18-M/v1 35-70%, central50%; N16 carried55-80%, central65%; no promotion.',new_target_record='v3/discovery/s19/verification_targets.md')
oldplan=json.loads(subprocess.check_output(['git','show',BASE+':v3/plan.v1.json'],cwd=ROOT))
legacy=oldplan['discovery_program']['promotion']
promotion['historical_f01_forecast']={k:legacy[k] for k in ['current_candidate','current_probability','current_probability_range','event_id','verification_plan_version','assessment']}
promotion.update(current_candidate='V19-R/v1',current_probability=.65,current_probability_range=[.5,.8],
 event_id='V19-R/v1',verification_plan_version='DEVELOPMENT; not frozen',assessment='v3/discovery/s19/readiness.md')
assessments=promotion['additional_candidate_assessments']
for name,prob,rng,recordname,event in [('N16-C',.65,[.55,.8],'s18/n16_assessment.md','s17/claim.md'),('O18-M',.5,[.35,.7],'s19/o18_assessment.md','s18/scientific_assessment.md'),('V19-R',.65,[.5,.8],'s19/readiness.md','s19/claim.md')]:
 item=next((x for x in assessments if x['candidate']==name),None)
 if item is None:item=dict(candidate=name,version='v1');assessments.append(item)
 item.update(probability=prob,probability_range=rng,assessment='v3/discovery/'+recordname,event='v3/discovery/'+event,status='DEVELOPMENT; continue with specific blockers; no promotion',calibrated=False)
plan['optional_recurrence_advice']['current_recommendation']='Broad discovery when authorized; short V19 exact-contract novelty/duty comparison; preserve alternatives. O18 capped screen complete. No automatic recurrence.'
write(p,plan)
print(json.dumps(dict(status='prepared',rows=29,research_ns=a['research_ns'])))
