"""Administrative s17 closure. No research credit; preserve historical row bytes."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DISC = HERE.parent
BASE = 'e709bc316c352547242fbb43b4fcd6d7ce97927b'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def text(p, s): p.write_bytes((s.rstrip()+'\n').encode('utf-8'))
def write(p, obj): text(p, json.dumps(obj, indent=2, ensure_ascii=False))
def basefile(name): return subprocess.check_output(['git', 'show', BASE+':'+name], cwd=ROOT).decode('utf-8')
a = read(HERE/'effective_actuals.json')
assert a['research_ns'] == 14423719000000 and not a['clock_active']
sources = ['claim.md', 'proof.md', 'comparison.md', 'gram_sdp.md', 'gram_result.json',
    'dual_certificates.md', 'endpoint_result.json', 'width_result.json',
    'cancellation_result.json', 'retention_tradeoff.md', 'acquisition_result.json',
    'checker_review.md', 'format_limits.md', 'format_result.json', 'block_check_v2.py',
    'format_repair_result.json', 'search_guarantee.md', 'scalar_search_result.json',
    'algebraic_result.json', 'rejection_result.json', 'pair_radius.md',
    'pair_radius_result.json', 'pair_criterion.md', 'criterion_result.json',
    'pair_gap.md', 'gap_result.json', 'pair_norm.md', 'portfolio40.md',
    'scientific_assessment.md', 'verification_targets.md', 'readiness.md']
w = read(HERE/'width_result.json')
metrics = dict(contributor='Codex (GPT-6)', status='DEVELOPMENT',
    scope_id='s17_N16_C_contribution_assessment_v1', observation_date_utc='2026-10-24',
    observed_in_row='s17_cp01', age_in_recurrences=0,
    retained_block=dict(comparator='Strong old-vector/two-scalar information bound, not the original one-value bound',
        certified_width=w['block_certificate_width'],
        comparator_width_interval=w['width_interval'],
        reduction_fraction_interval=w['certificate_width_reduction_interval'],
        reduction_percent_approx=[100*x for x in w['decimal_summary']['fractional_reduction']],
        interpretation='Scoped width improvement from additional retained information; not fee, variance or CPU saving'),
    decision=dict(rounded_upper_bound_approx=0.58311909, threshold=0.6,
        old_vector_compatible_value=1, source_norm_warrant_matched=True,
        sufficient_block_acquisition_queries=3, targeted_sufficient_queries=1,
        no_minimal_acquisition_claim=True),
    analytic_representation=dict(stationary_parameter_degree_bound='4k-2',
        strict_threshold_polynomial_degree_bound='2k',
        generic_prior_SDP_exact=True, measured_solver_speed_advantage=None),
    checker=dict(original_version='s16/block_check.py', repaired_version='s17/block_check_v2.py',
        repaired_defect='Valid-input output serialization exceeded Python decimal digit guard',
        false_approval_observed=False, input_rational_bit_limit=4096,
        example_sufficient_witness_bits=8189, bounded_format_complete=False,
        process_digit_guard_unchanged=True),
    separate_pair=dict(universal_coefficient_at_radius_one=2.1596436631325404,
        strongest_ordinary_coefficient_gain_percent=0,
        superseded_weaker_comparator_gain_percent_approx=0.33156,
        exact_block_equality_criterion=True,
        equal_first_two_moments_block_gap_at_least='8835006207069881667/41021651174048000000000',
        bounded_source_deficit_order='Theta(1/B^2) in the specified strict low-block regime',
        novelty='UNASSESSED; separate from N16-C/v1'),
    readiness=dict(candidate='N16-C/v1', central_percent=75, range_percent=[60,85],
        event='s17/claim.md', record='s17/readiness.md', calibrated=False,
        independent_confirmation=False, disposition='continue developing',
        blocker='Moderate novelty/usefulness of the analytic endpoint solution beyond exact prior SDP and routine reductions'),
    new_measured_audit_fee_reduction=None, new_measured_runtime_reduction=None,
    new_measured_counted_computation_reduction=None, complete_economic_cost=None,
    historical_audit=dict(session='s10', observation_date_utc='2026-10-14', age_in_recurrences=7,
        near_target_fee_reduction_percent=57.12, named_work_reduction_percent=9.53,
        measurement_status='dated carry; no new audit-stream run'),
    ordinary_comparison='The exact prior operator-interpolation SDP ties. Strong old-vector control reduces the previous width headline to about1.80%; one targeted query suffices for the upper decision; the two-edit universal ordinary coefficient ties.',
    limitations='Same-model development; novelty unresolved; no new complete-cost, audit-fee or counted-work saving; no promotion.',
    sources=[dict(path='s17/'+n, sha256=sha(HERE/n)) for n in sources])
write(HERE/'progress_metrics.json', metrics)

def spans(s):
    i=s.index('[',s.index('"rows"'))+1; out=[]; decoder=json.JSONDecoder()
    while True:
        while s[i].isspace() or s[i]==',': i+=1
        if s[i]==']': return out
        _,end=decoder.raw_decode(s,i); out.append((i,end)); i=end
oldtext=basefile('v3/discovery/recurrences.json')
table=json.loads(oldtext)
assert len(table['rows'])==26
row=copy.deepcopy(table['rows'][-1])
row.update(id='s17_cp01',label='s17 four-hour N16 contribution assessment',checkpoint='s17/checkpoint.md',
    session='s17', research_ns=a['research_ns'],cumulative_research_ns=a['program_research_ns'],
    research_minutes_rounded=240,cumulative_minutes_rounded=2539,
    metric_summary='N16 readiness60–85%, central75%; explicit sharp endpoints and finite witnesses. Strong old-vector control leaves1.80049–1.80553% width gain. Rounded upper0.58311909<0.6 versus compatible1; one targeted query also suffices. No fresh economic gain; ordinary SDP ties.',
    metric_values=dict(scope_id=metrics['scope_id'],source='s17/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json')),
    description='Focused author-directed assessment, critical proof reconstruction, close prior SDP comparison, checker serialization repair and forty-hour portfolio review;35 families retained; no promotion.',
    time_evidence=dict(actuals='s17/effective_actuals.json',sha256=sha(HERE/'effective_actuals.json'),
        actuals_field='session_research_ns',cumulative_actuals_field='cycle_research_ns',
        research_closed_utc=a['research_closed_utc'],note='178 same-runtime segments;20 research and1 O interval excluded explicitly, plus O/context recovery. Publication zero credit.'),
    metric_sources=metrics['sources'],
    candidate_readiness=dict(candidate='N16-C/v1',range_percent=[60,85],central_percent=75,
        status='continue developing; below minimum; no promotion',event='s17/claim.md',record='s17/readiness.md',
        historical_I13_R=dict(range_percent=[55,75],central_percent=65,assessment_date_utc='2026-10-21',
            age_in_recurrences=4,status='carried, not reassessed')))
for key,item in row['fixed_metrics'].items():
    if key=='families_total': item.update(observed_in_row='s17_cp01',age_in_recurrences=0)
    else:
        if isinstance(item.get('age_in_recurrences'),int): item['age_in_recurrences']+=1
        item.update(carried_in_row='s17_cp01',carried_from_row='s16_cp01',
            reason='No comparable new stream measurement or F01 reassessment in s17; dates and scopes retained.')
table['rows'].append(row)
table.update(prepared_by='Codex (GPT-6)',prepared_date_utc='2026-10-24',source_commit=BASE,
    previous_table_commit=BASE,latest_checkpoint='s17/checkpoint.md',latest_effective_actuals='s17/effective_actuals.json',
    total_research_ns=a['program_research_ns'],total_minutes_rounded=2539,total_research_minutes=a['program_research_minutes'],
    program_research_ns=a['program_research_ns'],phase_research_ns=a['phase_research_ns'],
    active_scope_id=metrics['scope_id'],active_row_ids=['s17_cp01'],current_separate_scope_ids=[metrics['scope_id']],
    current_readiness_assessment=dict(candidate='N16-C/v1',range_percent=[60,85],central_percent=75,
        status='continue developing; no promotion',record='s17/readiness.md',event='s17/claim.md'))
table['rendered_table']['row_ids'].append('s17_cp01')
table['rendered_table']['latest_row_id']='s17_cp01'
table['visible_resource_metrics']['s17']=dict(source='s17/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json'),observation_date_utc='2026-10-24',age_at_s17=0)
out=json.dumps(table,indent=2,ensure_ascii=False)+'\n'
for (start,end),(oldstart,oldend) in reversed(list(zip(spans(out),spans(oldtext)))):
    out=out[:start]+oldtext[oldstart:oldend]+out[end:]
text(DISC/'recurrences.json',out)
assert json.loads(out)['rows'][:26]==json.loads(oldtext)['rows']
md=basefile('v3/discovery/recurrences.md').replace('26 recorded rows, ending\nwith s16','27 recorded rows, ending\nwith s17').replace('2299 cumulative research minutes','2539 cumulative research minutes').replace('new s16 events UNASSESSED','N16-C/v1 60–85%, central75%, continue developing')
lines=md.splitlines(); last=max(i for i,l in enumerate(lines) if l.startswith('| '))
lines.insert(last+1,'| **[s17 N16 assessment](s17/checkpoint.md)** | **240** | **2539** | **35 (0)** | Sharp retained-block contribution assessment; Oct24 UTC;40h portfolio review | **No fresh audit-fee run.** s10 **−57.12% carried, age7**. Three queries acquire a block; **one targeted query also settles the chosen upper decision** | **No new CPU/count saving.** s10 named work **−9.53% carried, age7**. Exact checker serialization repaired; bounded format remains incomplete | **Exact prior SDP ties.** Strong old-vector control leaves **1.80049–1.80553% width gain**; universal two-edit analytic coefficient ties | 144/272;254/272;258/272; carried, age21 | 80/80;60/80;223; carried, age10 | 16/16;11/11;1,718,749;4.7544×; carried, age9 | 0; carried, age9 | **N16-C/v1 60–85%, central75%; continue developing.** I13 central65%, age4; F01 central30%, age7; distinct events | Explicit endpoint proof and finite witnesses; **rounded upper0.58311909<0.6 versus old-vector-compatible1**. Separate exact two-edit block criterion/gap. Novelty remains unresolved; no promotion. |')
text(DISC/'recurrences.md','\n'.join(lines)+'''\n\n## s17 scope and relevant gains

[Metrics](s17/progress_metrics.json) and [assessment](s17/scientific_assessment.md)
separate the analytic contribution from information gains and dated resource
carries. The previous23.4% width headline becomes about1.80% against a stronger
old-vector control. The rounded upper decision compares different retained
information; one targeted query also suffices. Ordinary identical optimization
ties, including the exact prior SDP. The checker repair is an availability
improvement, not a measured CPU saving. No new audit-fee or counted-work gain.
The first N16 forecast is60–85%, central75%, for [this event](s17/claim.md).
Historical I13 and F01 forecasts remain different, unchanged events.
''')
p=read(ROOT/'v3/plan.v1.json');p['active_session']=None
for key in ('last_completed_session','last_preserved_session','last_discovery_session'):p[key]='v3/discovery/s17/session.md'
p['observed_progress'].update(research_ns=a['phase_research_ns'],source='v3/discovery/s17/effective_actuals.json',research_minutes=a['phase_research_minutes'],evidence_disposition='s17 closed; explicit exclusions and recovery reconciled; publication zero research credit.')
p['optional_recurrence_advice']['current_recommendation']='Restore broad75/20/5 discovery. N16 analytic moderate-novelty/usefulness comparison remains the blocker; keep solution reuse, stronger information, model repair and partial-proof alternatives.'
d=p['discovery_program'];d.update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],latest_checkpoint='v3/discovery/s17/checkpoint.md',actuals='v3/discovery/s17/effective_actuals.json',next_portfolio_review_minutes=6000)
d['current_cycle'].update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],session='v3/discovery/s17/session.md',actuals='v3/discovery/s17/effective_actuals.json',clock_active=False,session_status=a['status'])
if 'v3/discovery/s17/session.md' not in d['sessions']:d['sessions'].append('v3/discovery/s17/session.md')
d['execution_cadence'].update(last_closed_session='s17',last_increment_research_ns=a['research_ns'],last_increment_research_minutes=a['research_minutes'],last_override_authority='v3/decisions/2026-10-24_s17_assessment.md')
d['promotion'].update(forecast_status='N16-C/v1 60–85%, central75%, continue developing; R16-V unassessed; I13 and F01 historical forecasts unchanged',new_target_record='v3/discovery/s17/verification_targets.md')
for item in d['promotion']['additional_candidate_assessments']:
    if item['candidate']=='N16-C':item.update(probability=0.75,probability_range=[0.6,0.85],status='DEVELOPMENT; continue developing; below readiness',event='v3/discovery/s17/claim.md',assessment='v3/discovery/s17/readiness.md',calibrated=False)
if not any(x['horizon_minutes']==2400 for x in d['completed_portfolio_reviews']):
    d['completed_portfolio_reviews'].append(dict(horizon_minutes=2400,session='s17',record='v3/discovery/s17/portfolio40.md',observed_program_research_ns=144030544241147,scope='Focused contribution assessment and broad portfolio review; no promotion'))
write(ROOT/'v3/plan.v1.json',p)
summary='''**Current continuation — October24,2026 UTC, Codex (GPT-6):**
[s17 checkpoint](s17/checkpoint.md), [findings](s17/findings.md),
[actuals](s17/effective_actuals.json), [single recurrence table](recurrences.md).
The focused four-hour assessment is CLOSED:240.395316666666… research minutes.
Program2539.488754019116… and phase3625.620121383266… minutes. No active
clock remains;178 same-runtime segments and explicit exclusions are reconciled.
The35-family inventory is unchanged. C001 OPEN; P3-POS01 OUTSTANDING;
P3-11 deferred; no promotion.

**N16-C/v1:60–85%, central75%; continue developing.** The bounded event includes
useful moderate novelty. The critical proof and finite witnesses are reconstructed;
the exact prior operator-interpolation SDP ties. The remaining blocker is the
analytic solution's useful increment beyond routine prior reductions. Stronger
old-vector comparison leaves about1.80% width gain. Rounded upper0.58311909<0.6
contrasts with compatible1, but one targeted query also suffices. No fresh fees
or counted-work saving. The checker serialization repair preserves old evidence.

The [40-hour review](s17/portfolio40.md) is complete; the next deeper review is
100 program hours, with42.32 hours now recorded. Restore broad75/20/5 discovery
and keep the other promising routes. Default next duration one hour unless
freshly overridden; no automatic recurrence or merge. Historical forecasts
remain scoped to their own events. [Next prompt](CONTINUE.md).

'''
for name in ('P3_SEARCH_01.md','candidates.md'):
    f=DISC/name;s=f.read_text(encoding='utf-8');start=s.index('**Current continuation')
    end=s.index('IDs S01 onward',start) if name=='candidates.md' else s.index('\n## ',start)+1
    text(f,s[:start]+summary+s[end:])
f=ROOT/'v3/claim_ledger.md';s=f.read_text(encoding='utf-8');pos=s.index('\n\n')+2
note='''**Latest pointer — October24,2026 UTC, Codex (GPT-6):**
[s17 claim](discovery/s17/claim.md), [assessment](discovery/s17/scientific_assessment.md),
[metrics](discovery/s17/progress_metrics.json). N16-C/v1 is DEVELOPMENT,
60–85%, central75%; continue developing. The critical proof, prior exact SDP
comparison and conditional checker are reconstructed. A valid-input formatting
failure has a versioned repair. Moderate novelty/usefulness of the analytic
increment remains unresolved. No fresh economic gain or promotion. Other
targets and historical forecasts retain their scopes;40-hour review completed.

'''
if '[s17 claim]' not in s:text(f,s[:pos]+note+s[pos:])
f=ROOT/'TODO_v3.md';s=f.read_text(encoding='utf-8');end=s.index('Established October 6')
s=s[:s.index('\n\n')+2]+'''**Latest recurrence — October24,2026 UTC:** [s17](v3/discovery/s17/checkpoint.md)
is CLOSED after240.395316666666… effective research minutes under the
[four-hour assessment override](v3/decisions/2026-10-24_s17_assessment.md).
PR18 was verified merged before entry. [N16-C/v1](v3/discovery/s17/claim.md)
has subjective readiness60–85%, central75%: continue developing while resolving
the analytic contribution's moderate novelty/usefulness beyond the exact prior
SDP. C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred; no promotion or active clock.

'''+s[end:]
s=s.replace('2299.09343735245','2539.488754019116…').replace('3385.2248047166','3625.620121383266…').replace('2425.2248047166','2665.620121383266…').replace('from [s16](v3/discovery/s16/checkpoint.md)','from [s17](v3/discovery/s17/checkpoint.md)')
marker='## Current author selection — October 23, 2026 UTC'
if marker in s:s=s.replace(marker,'''## Current author selection — October 24, 2026 UTC

The focused assessment and [40-hour review](v3/discovery/s17/portfolio40.md)
are complete. Read [findings](v3/discovery/s17/findings.md) and the
[single progress table](v3/discovery/recurrences.md). The next session restores
broad75/20/5 discovery; retain other promising routes. Current program42.32h;
next deeper review100h. N16's readiness is below80%; no automatic recurrence.

## Previous author selection — October 23, 2026 UTC''')
text(f,s)
f=HERE/'active_checkpoint.md';s=f.read_text(encoding='utf-8')
if not s.startswith('> Superseded'):text(f,'> Superseded by the [closing checkpoint](checkpoint.md). The historical\n> mid-session state below no longer describes an active commitment.\n\n'+s)
print(json.dumps(dict(status='updated',rows=27,prior_rows_preserved=26,research_ns=a['research_ns']),indent=2))
