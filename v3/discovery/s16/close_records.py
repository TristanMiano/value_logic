"""Administrative s16 pointer/metric update; preserves historical recurrence bytes."""
from pathlib import Path
import copy, hashlib, json, re, subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DISC=HERE.parent
BASE='8b1ed04967871a6e505e62e01c83fa401d35fa91'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(p,s):p.write_bytes((s.rstrip()+'\n').encode('utf-8'))
a=read(HERE/'effective_actuals.json')
assert a['research_ns']==14409577000000 and not a['clock_active']
source_names=['matrix_receipt.md','matrix_lower.md','operator_receipt.md',
    'matrix_lower_probe.json','fixed_output.md','shape_budget.md','joint_allocation.md',
    'allocation_probe.json','decision_receipts.md','reuse_ratio.md','reuse_exact_probe.json',
    'nonquadratic_reuse.md','p_reuse_probe.json','private_repairs.md','checker_prices.md',
    'cost_leakage.md','completion_bias.md','block_checker.md','block_check.py','block_probe.json',
    'query_witness.md','query_probe.json','rounded_queries.md','query_limits.md',
    'block_acquisition.md','adaptive_thresholds.md','scientific_assessment.md']
metrics=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',
    scope_id='s16_retained_information_reuse_checks_v1',observation_date_utc='2026-10-24',
    observed_in_row='s16_cp01',age_in_recurrences=0,
    retained_block=dict(old_scalar_queries=3,one_value_comparator_queries=1,
        certified_lower='618573873750/1340748094907',
        certified_upper='867127945275459/1611861132384100',
        certified_width_approx=0.07660218212390271,width_reduction_percent_lower=23.4,
        status='analytic information gain; extra acquisition paid',
        conditional_full_value_call_reduction_percent_lower=23.4,
        call_reduction_premise='Fresh uniform threshold independent of fixed truthful receipts; excludes receipt acquisition and arithmetic'),
    same_information_contrast=dict(reduction_percent=100*read(HERE/'allocation_probe.json')['reduction_float'],
        comparator='Subtracting individually sharp target intervals under the same shared Frobenius edit budget',
        candidate_radius_upper=read(HERE/'allocation_probe.json')['upper'],
        comparator_radius='4000/40001',decision_offset='2/25',
        interpretation='Exact finite rational certificate, conditional on the concavity proof; ordinary joint optimization ties'),
    output_shape=dict(one_output_interval=['1/17','1/5'],unrestricted_width='sqrt(5)/10',
        width_reduction_percent_approx=36.86396298824124,additional_value_queries=0,
        status='Different warranted source-shape information, not new task-error or fee measurement'),
    solution_reuse=dict(quadratic_sharp_ratio='(1+e^2/2)^2',
        nonquadratic_sharp_uniform_exponent='min(p,p/(p-1))',
        nonquadratic_sharp_constants=False,inexact_primal_dual_adapter=True),
    private_repairs=dict(conditional_expected_queries_upper='1534/253',
        fresh_epoch_control_queries=8,strong_univariate_interpolation_queries=5,
        status='Five-query ordinary interpolation defeats the motivating economic comparison; no general saving'),
    query_witness=dict(old_scalar_queries=2,rounded_interval_approx=[0.5672462113427743,0.6546098398643968],
        task='One declared target and edit budget; full-block support for all later targets is a stronger duty',
        model_accuracy_required_for_validity=False,source_value_warrants_required=True),
    exact_checker=dict(max_dimension=16,input_byte_limit=1048576,rational_component_bit_limit=4096,
        source='block_check.py',status='Development; external source/target/edit premises remain'),
    new_measured_audit_fee_reduction=None,new_measured_runtime_reduction=None,
    new_measured_complete_computation_reduction=None,complete_economic_cost=None,
    historical_audit=dict(session='s10',observation_date_utc='2026-10-14',age_in_recurrences=6,
        near_target_fee_reduction_percent=57.12,named_work_reduction_percent=9.53,
        measurement_status='dated carry; no new audit-stream run'),
    ordinary_comparison='Identical conventional implementation ties. Joint sensitivity explains the approximate scale of the contrast gain. Strong interpolation and paired-test controls defeat two proposed cost claims.',
    limitations='Same-model development; no independent confirmation, established moderate novelty, full economic comparison or promotion.',
    sources=[dict(path='s16/'+n,sha256=sha(HERE/n)) for n in source_names])
write(HERE/'progress_metrics.json',metrics)

def row_spans(s):
    i=s.index('[',s.index('"rows"'))+1;out=[];decoder=json.JSONDecoder()
    while True:
        while s[i].isspace() or s[i]==',':i+=1
        if s[i]==']':return out
        _,end=decoder.raw_decode(s,i);out.append((i,end));i=end
base_text=subprocess.check_output(['git','show',BASE+':v3/discovery/recurrences.json'],cwd=ROOT).decode('utf-8')
table=json.loads(base_text)
old=table['rows'][-1]
row=copy.deepcopy(old)
row.update(id='s16_cp01',label='s16 fresh four-hour author override',checkpoint='s16/checkpoint.md',
    session='s16',research_ns=a['research_ns'],cumulative_research_ns=a['program_research_ns'],
    research_minutes_rounded=240,cumulative_minutes_rounded=2299,
    metric_summary='More than23.4% narrower paid three-value interval;29.11406857% smaller same-information joint contrast radius; exact checker and sharp solution reuse. No fresh audit/CPU measurements; ordinary ties.',
    metric_values=dict(scope_id=metrics['scope_id'],source='s16/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json')),
    description='63 connected constructive passes across retained numerical information, model repair, partial proofs and reasoning costs; not63 new families. Early conventional-control rejections retained; no promotion.',
    time_evidence=dict(actuals='s16/effective_actuals.json',sha256=sha(HERE/'effective_actuals.json'),
        actuals_field='session_research_ns',cumulative_actuals_field='cycle_research_ns',
        research_closed_utc=a['research_closed_utc'],note='152 same-runtime intervals; twelve research exclusions, one E-to-D correction, and explicit context recovery excluded.'),
    metric_sources=metrics['sources'],
    candidate_readiness=dict(new_candidates=['N16-C/v1','R16-V/v1'],status='UNASSESSED; no promotion',
        record='s16/verification_targets.md',historical_I13_R=dict(range_percent=[55,75],central_percent=65,
        assessment_date_utc='2026-10-21',age_in_recurrences=3,status='carried, not reassessed')))
for key,item in row['fixed_metrics'].items():
    if key=='families_total':
        item.update(observed_in_row='s16_cp01',age_in_recurrences=0)
    else:
        if isinstance(item.get('age_in_recurrences'),int):item['age_in_recurrences']+=1
        item.update(carried_in_row='s16_cp01',carried_from_row='s15_cp01',
            reason='No comparable new stream measurement or F01 reassessment in s16; dates/scopes retained.')
table['rows'].append(row)
table.update(prepared_by='Codex (GPT-6)',prepared_date_utc='2026-10-24',source_commit=BASE,
    previous_table_commit=BASE,latest_checkpoint='s16/checkpoint.md',
    latest_effective_actuals='s16/effective_actuals.json',total_research_ns=a['program_research_ns'],
    total_minutes_rounded=2299,total_research_minutes=a['program_research_minutes'],
    program_research_ns=a['program_research_ns'],phase_research_ns=a['phase_research_ns'],
    active_scope_id=metrics['scope_id'],active_row_ids=['s16_cp01'],current_separate_scope_ids=[metrics['scope_id']],
    current_readiness_assessment=dict(status='N16-C/v1 and R16-V/v1 UNASSESSED; historical forecasts unchanged',
        record='s16/verification_targets.md',research_credit_ns=0))
table['rendered_table']['row_ids'].append('s16_cp01')
table['rendered_table']['latest_row_id']='s16_cp01'
table['visible_resource_metrics']['s16']=dict(source='s16/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json'),observation_date_utc='2026-10-24',age_at_s16=0)
out=json.dumps(table,indent=2,ensure_ascii=False)+'\n'
old_spans=row_spans(base_text);new_spans=row_spans(out)
for (start,end),(old_start,old_end) in reversed(list(zip(new_spans,old_spans))):
    out=out[:start]+base_text[old_start:old_end]+out[end:]
text(DISC/'recurrences.json',out)
assert json.loads(out)['rows'][:25]==json.loads(base_text)['rows']

md=subprocess.check_output(['git','show',BASE+':v3/discovery/recurrences.md'],cwd=ROOT).decode('utf-8')
md=md.replace('25 recorded rows, ending\nwith s15','26 recorded rows, ending\nwith s16').replace('2059 cumulative research minutes','2299 cumulative research minutes').replace('new s15 events UNASSESSED','new s16 events UNASSESSED')
lines=md.splitlines();last=max(i for i,l in enumerate(lines) if l.startswith('| '))
newrow='| **[s16 four-hour round](s16/checkpoint.md)** | **240** | **2299** | **35 (0)** | Retained response blocks; shared edits; solution reuse; model checks and partial proofs; Oct23–24 UTC | **No fresh audit-fee run.** s10 **−57.12% carried, age6**. Fixed independent-threshold example: **>23.4% fewer expected full-value calls**, conditional on paid three-value receipts | **No new CPU/complete-work gain.** s10 named work **−9.53% carried, age6**. Sharp reuse ratio **(1+e²/2)²** bounds the benefit of another solve | **Identical ordinary methods tie.** Joint robust control matches; **five-query interpolation beats6.063 private-check bound** | 144/272;254/272;258/272; carried, age20 | 80/80;60/80;223; carried, age9 | 16/16;11/11;1,718,749;4.7544×; carried, age8 | 0; carried, age8 | **N16-C/R16-V UNASSESSED.** I13-R/v1 55–75%, central65%, carried age3; F01 20–45%, central30%, age6 | **>23.4% narrower three-value interval;29.114% smaller same-information joint contrast radius**, settling a worked action. Rounded exact checker and model-proposed query witnesses. No novelty or promotion claim. |'
lines.insert(last+1,newrow)
md='\n'.join(lines)+'\n\n## s16 scope and relevant gains\n\n[Metrics](s16/progress_metrics.json) separate retained-information width, shared-edit\ncontrast, analytic acquisition counts and dated resource carries. The23.4% call\ncomparison requires a fresh threshold independent of fixed truthful receipts;\n[threshold-aware acquisition](s16/adaptive_thresholds.md) needs a different bound.\nThe29.114% contrast gain is against separate bounds with the same information;\nordinary joint optimization ties. Complete economic costs remain unknown.\nSee [assessment](s16/scientific_assessment.md) and [targets](s16/verification_targets.md).\n'
text(DISC/'recurrences.md',md)

p=read(ROOT/'v3/plan.v1.json')
p['active_session']=None
for key in ('last_completed_session','last_preserved_session','last_discovery_session'):p[key]='v3/discovery/s16/session.md'
p['observed_progress'].update(research_ns=a['phase_research_ns'],source='v3/discovery/s16/effective_actuals.json',
    research_minutes=a['phase_research_minutes'],evidence_disposition='s16 closed; twelve research exclusions, one E-to-D correction and explicit recovery; publication zero research credit.')
if 'current_recommendation' in p.get('optional_recurrence_advice',{}):
    p['optional_recurrence_advice']['current_recommendation']='Continue broad generation from s16; compare the retained-block theorem to closest primary prior and a fair retention/access control; preserve model-repair and proof-acquisition alternatives.'
d=p['discovery_program'];d.update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],latest_checkpoint='v3/discovery/s16/checkpoint.md',actuals='v3/discovery/s16/effective_actuals.json')
d['current_cycle'].update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],actuals='v3/discovery/s16/effective_actuals.json',clock_active=False,session_status='closed_author_directed_four_hour_handoff')
if 'v3/discovery/s16/session.md' not in d['sessions']:d['sessions'].append('v3/discovery/s16/session.md')
d['execution_cadence'].update(last_closed_session='s16',last_increment_research_ns=a['research_ns'],last_increment_research_minutes=a['research_minutes'],last_override_authority='v3/decisions/2026-10-23_s16_four_hours.md')
d['promotion'].update(forecast_status='N16-C/v1 and R16-V/v1 unassessed; I13-R/v1 and F01 historical forecasts unchanged',new_target_record='v3/discovery/s16/verification_targets.md')
for candidate in ('N16-C','R16-V'):
    if not any(x['candidate']==candidate for x in d['promotion']['additional_candidate_assessments']):
        d['promotion']['additional_candidate_assessments'].append(dict(candidate=candidate,version='v1',probability=None,status='DEVELOPMENT; UNASSESSED',event='v3/discovery/s16/verification_targets.md'))
write(ROOT/'v3/plan.v1.json',p)

summary='''**Current continuation — October24,2026 UTC, Codex (GPT-6):**
[s16 checkpoint](s16/checkpoint.md), [findings](s16/findings.md),
[actuals](s16/effective_actuals.json), [single recurrence table](recurrences.md).
The fresh four-hour recurrence is CLOSED:240.159616666666… research minutes.
C001/program is2299.09343735245 and phase3385.2248047166 minutes.
All152 same-runtime intervals are reconciled; twelve research exclusions,
one E-to-D correction and explicit context recovery are recorded. No active
clock remains. The35-family inventory is unchanged;63 passes are not63 families.

**C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred; no promotion.**
Retained response blocks yield a worked interval>23.4% narrower than one
old value; shared-edit coupling gives29.114% less contrast radius than
separate sharp bounds with the same information. Exact rounded certificates,
query witnesses and sharp solution-reuse bounds provide usable interfaces.
These are scoped formal gains, not new audit fees or complete CPU savings.
Identical ordinary methods tie; strong interpolation defeats a proposed
private-check saving. [N16-C/R16-V targets](s16/verification_targets.md)
are UNASSESSED. Historical I13-R/v1 and F01 forecasts remain unchanged.
Continue broad discovery toward a useful, moderately novel contribution.
Default one hour unless overridden; no automatic next session. Next deeper
portfolio review:40 program hours, with38.32 hours now recorded.

'''
for name in ('P3_SEARCH_01.md','candidates.md'):
    f=DISC/name;s=f.read_text(encoding='utf-8');start=s.index('**Current continuation');end=s.index('IDs S01 onward',start)-1 if name=='candidates.md' else s.index('\n## ',start)
    text(f,s[:start]+summary+s[end+1:])
f=ROOT/'v3/claim_ledger.md';s=f.read_text(encoding='utf-8');pos=s.index('\n\n')+2
text(f,s[:pos]+'''**Latest pointer — October24,2026 UTC, Codex (GPT-6):** [s16 assessment](discovery/s16/scientific_assessment.md),
[targets](discovery/s16/verification_targets.md), [metrics](discovery/s16/progress_metrics.json).
Retained-information envelopes, shared-edit contrasts, solution reuse and
partial-proof/model-query adapters remain DEVELOPMENT. The23.4% interval
and29.114% contrast gains have different explicit comparison duties.
No fresh audit-fee/CPU benchmark; ordinary equivalents tie. N16-C/R16-V
UNASSESSED; historical forecasts unchanged; no promotion. Earlier records
retain their exact scopes.

'''+s[pos:])
f=ROOT/'TODO_v3.md';s=f.read_text(encoding='utf-8');end=s.index('Established October 6')
s=s[:s.index('\n\n')+2]+'''**Latest recurrence — October24,2026 UTC:** [s16](v3/discovery/s16/checkpoint.md)
is CLOSED after240.159616666666… research minutes under the
[four-hour override](v3/decisions/2026-10-23_s16_four_hours.md).
[Actuals](v3/discovery/s16/effective_actuals.json) exclude recovery and mixed
intervals. PR17 was verified merged before entry. C001 OPEN; P3-POS01
OUTSTANDING; no promotion or active clock remains.

'''+s[end:]
s=s.replace('2058.933820685783…','2299.09343735245').replace('3145.065188049933…','3385.2248047166').replace('2185.065188049933…','2425.2248047166').replace('from [s15](v3/discovery/s15/checkpoint.md)','from [s16](v3/discovery/s16/checkpoint.md)')
text(f,s)
f=HERE/'session.md';s=f.read_text(encoding='utf-8').replace('Status: ACTIVE; fresh four-hour author commitment.','Status: CLOSED at240.159616666666… research minutes; see [checkpoint](checkpoint.md).')
text(f,s)
print(json.dumps(dict(status='updated',rows=26,prior_rows_preserved=25,research_ns=a['research_ns']),indent=2))
