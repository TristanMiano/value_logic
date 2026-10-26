"""Initial one-time s18 handoff synchronization; later checked editorial corrections live in the committed records. Administration, zero research credit."""
from pathlib import Path
from decimal import Decimal
import copy
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[4]
HERE=ROOT/'v3/discovery/s18'
DISC=HERE.parent
BASE='64828a50e704ca17af79be693aee164b7ffb35ec'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(name):return dict(path='s18/'+name,sha256=sha(HERE/name))
a=read(HERE/'effective_actuals.json')
assert a['research_ns']==14414597000000 and not a['clock_active']
metrics=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',
    scope_id='s18_broad_information_and_feedback_v1',observation_date_utc='2026-10-25',
    observed_in_row='s18_cp01',age_in_recurrences=0,
    ordinal=dict(candidate='O18-M/v1',mistake_bound='binom(d,2)*(C+1)+C',
        assumptions='Fixed component utilities with arbitrary ties; changing matroids; C arbitrary feasible bad reports; C unknown',
        basic_work='O(d^3) elementary path work plus independence queries',
        named_item_incremental_work='O(d^2) elementary work per round',
        storage='O(d^2 log T) counter bits',
        comparator='Oki-Sakaue distinct-coordinate stronger rate; Cai et al known-budget general regret; ordinary last-response cache q+C on q repeat contexts',
        empirical_superiority=None),
    conditional_receipts=dict(face_optimizations_at_most='2*n*2^k',
        implemented_dp_work='O(n*3^k)',derived_cover_feasibility='O(n*k*2^k) integer operations',
        sieve_implemented=False,cover_integer_bits='O(n*k+k)',
        two_of_three_receipts_upper=4,all_three_receipts_exact=1,
        certified_attainer_message_bits=2,approximate_receipt_upper='min(4,1+3*epsilon)',
        decision_tolerance='epsilon<1/6 with solve fee1/2 and fallback2',
        ordinary_equivalent='ties',complete_cost_saving=None),
    paired_retention=dict(contexts=80,tree_closures_preserved=55,
        warm_bound_work_before=10655,warm_bound_work_after=9060,
        reduction_percent=str(Decimal(1595)*100/Decimal(10655)),
        tariff='Declared warm bound-work units, not CPU or complete cost',
        setup_tree_work=10655,admission_and_profile_check_work=7975,
        ordinary_selector='ties;68 local subsets and709 DP transitions',
        complete_cost_saving=None),
    n16=dict(event='N16-C/v1 unchanged from s17/claim.md',
        output_witness_dimension_before='at most2k',output_witness_dimension_after='at most k+1',
        readiness_range_percent=[55,80],central_percent=65,central_change_percentage_points=-10),
    readiness=dict(event='O18-M/v1',range_percent=[45,75],central_percent=60,
        status='continue developing with novelty blocker; no promotion',
        record='s18/scientific_assessment.md'),
    carried_resources=dict(observed_in_row='s10_cp01',age_in_recurrences=8,
        audit_fee_reduction_percent=57.12,named_work_reduction_percent=9.53,
        note='Dated carry only; no fresh audit stream. Complete costs remain unknown.'),
    sources=[record(n) for n in ['matroid_feedback.md','ordinal_comparison.md',
        'ordinal_incremental.md','ordinal_result.json','matroid_result.json','path_update_result.json',
        'attainer_dp.md','attainer_sieve.md','attainer_result.json','partial_receipt_proofs.md',
        'retention_result.json','retention_findings.md','n16_reduction.md','n16_assessment.md',
        'scientific_assessment.md','verification_targets.md']])
write(HERE/'progress_metrics.json',metrics)

target=DISC/'recurrences.json';oldtext=subprocess.check_output(['git','show',BASE+':v3/discovery/recurrences.json'],cwd=ROOT).decode('utf-8');d=json.loads(oldtext)
assert len(d['rows'])==27 and d['rows'][-1]['id']=='s17_cp01'
oldrows=copy.deepcopy(d['rows'])
fixed=copy.deepcopy(oldrows[-1]['fixed_metrics'])
for v in fixed.values():
    if isinstance(v,dict):
        if 'age_in_recurrences' in v:v['age_in_recurrences']+=1
        v.update(carried_in_row='s18_cp01',carried_from_row='s17_cp01',
            reason='No comparable fresh legacy-stream measurement or F01 reassessment in s18; original scope/date retained.')
row=dict(id='s18_cp01',label='s18 four-hour broad discovery',checkpoint='s18/checkpoint.md',
    session='s18',contributor='Codex (GPT-6)',research_ns=a['research_ns'],
    cumulative_research_ns=a['program_research_ns'],research_minutes_rounded=240,
    cumulative_minutes_rounded=(a['program_research_ns']+30000000000)//60000000000,
    new_family_ids=['S36'],cumulative_new_family_count=36,
    metric_summary='Tied unknown-budget matroid mistake bound; joint receipts upper4 to exact1, two-bit attainer action; warm tariff10655 to9060 with ordinary tie; N16 witnesses2k to k+1. No fresh audit/full-cost saving.',
    metric_values=dict(scope_id=metrics['scope_id'],source='s18/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json')),
    description='Broad mechanisms and early rejections; capped N16 novelty comparison; one new family; no promotion.',
    time_evidence=dict(actuals='s18/effective_actuals.json',sha256=sha(HERE/'effective_actuals.json'),
        actuals_field='session_research_ns',cumulative_actuals_field='cycle_research_ns',
        research_closed_utc=a['research_closed_utc'],
        note='184 same-runtime segments;22 research exclusions plus O/context recovery; publication zero credit.'),
    metric_sources=metrics['sources'],fixed_metrics=fixed,
    candidate_readiness=dict(candidate='O18-M/v1',range_percent=[45,75],central_percent=60,
        status='continue developing; no promotion',event='s18/scientific_assessment.md',
        n16_same_event=dict(candidate='N16-C/v1',range_percent=[55,80],central_percent=65,
            change_percentage_points=-10,record='s18/n16_assessment.md'),
        conditional_receipts='UNASSESSED'))
d.update(prepared_date_utc='2026-10-25',source_commit=BASE,
    latest_checkpoint='s18/checkpoint.md',latest_effective_actuals='s18/effective_actuals.json',
    row_scope='28 chronological boundaries; one s18 recurrence; all27 earlier row objects byte-preserved.',
    total_research_ns=a['program_research_ns'],total_minutes_rounded=row['cumulative_minutes_rounded'],
    total_research_minutes=a['program_research_minutes'],program_research_ns=a['program_research_ns'],
    phase_research_ns=a['phase_research_ns'],active_scope_id=metrics['scope_id'],active_row_ids=['s18_cp01'])
d['current_readiness_assessment']=row['candidate_readiness']
d['visible_resource_metrics']['s18']=dict(source='s18/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json'),observation_date_utc='2026-10-25',age_at_s18=0)
d['current_forecast']['age_in_recurrences']=8
d['current_forecast']['carried_in_row']='s18_cp01'
d['current_forecast']['carried_from_row']='s17_cp01'
d['rows']='__RAW_ROWS__'
decoder=json.JSONDecoder();start=oldtext.index('[',oldtext.index('"rows"'));_,end=decoder.raw_decode(oldtext,start)
rawarray=oldtext[start:end].rstrip()[:-1].rstrip()+',\n'+ '\n'.join('    '+line for line in json.dumps(row,indent=2,ensure_ascii=False).splitlines())+'\n  ]'
out=json.dumps(d,indent=2,ensure_ascii=False).replace('"__RAW_ROWS__"',rawarray)+'\n'
target.write_bytes(out.encode('utf-8'));assert json.loads(out)['rows'][:27]==oldrows

p=ROOT/'v3/plan.v1.json';plan=read(p)
for field in ['last_completed_session','last_preserved_session','last_discovery_session']:plan[field]='v3/discovery/s18/session.md'
plan['active_session']=None
plan['observed_progress'].update(research_ns=a['phase_research_ns'],research_minutes=a['phase_research_minutes'],
    source='v3/discovery/s18/effective_actuals.json',evidence_disposition='s18 closed; explicit exclusions and context recovery reconciled; publication zero credit.')
pr=plan['discovery_program'];pr.update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],
    latest_checkpoint='v3/discovery/s18/checkpoint.md',actuals='v3/discovery/s18/effective_actuals.json')
pr['current_cycle'].update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],
    session='v3/discovery/s18/session.md',actuals='v3/discovery/s18/effective_actuals.json',clock_active=False,
    session_status='closed_author_directed_four_hour_handoff')
pr['sessions'].append('v3/discovery/s18/session.md')
pr['execution_cadence'].update(last_closed_session='s18',last_increment_research_ns=a['research_ns'],
    last_increment_research_minutes=a['research_minutes'],last_override_authority='v3/decisions/2026-10-25_s18_broad_four_hours.md')
plan['optional_recurrence_advice']['current_recommendation']='Continue broad discovery when authorized, with capped early O18-M novelty screen; preserve conditional receipts and other alternatives. N16 same-event central65%; no promotion.'
write(p,plan)

p=HERE/'session.md';s=p.read_text(encoding='utf-8').replace('DEVELOPMENT; ACTIVE.','DEVELOPMENT; CLOSED.');s+='\nClosing record: [checkpoint](checkpoint.md);240.243283333333â€¦ research minutes.\nNo active clock or unfinished floor remains. Publication earns zero research credit.\n';p.write_text(s,encoding='utf-8')
print(json.dumps(dict(status='prepared',rows=28,research_ns=a['research_ns'])))
