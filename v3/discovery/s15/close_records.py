"""Guarded one-time s15 reporting closure. Administration; no research credit."""
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DISC = HERE.parent
BASE = '462249f13494709217cb1de71e552da576dbd4ca'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def text(p): return p.read_bytes().decode('utf-8')
def write(p, s): p.write_bytes(s.encode('utf-8'))
def save(p, o): write(p, json.dumps(o, indent=2, ensure_ascii=False)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

a = read(HERE/'effective_actuals.json')
assert a['research_ns'] == 14_413_279_000_000 and not a['clock_active']
assert len(read(DISC/'recurrences.json')['rows']) == 24, 'Already closed; inspect instead of rerunning.'
forecast = read(HERE/'forecast_probe.json')
metrics = dict(contributor='Codex (GPT-6)', status='DEVELOPMENT',
    scope_id='s15_counterfactual_correction_query_v1', observation_date_utc='2026-10-23',
    observed_in_row='s15_cp01', age_in_recurrences=0,
    numerical=dict(capability='Sharp one-receipt envelopes across finite real normed spaces, p>1, simultaneous operator/target changes and relative scale; endpoints and rank-one paths separately scoped.',
        new_operator_calls_after_receipts=0, complete_computation_change_percent=None,
        limitation='Receipt acquisition, edit warrants and scalar root/refinement work are paid; no new outward implementation or full-service benchmark.'),
    forecast_range=dict(degree=4, grid_size=257, rank=4, ambient_dimension='larger than rank',
        error_budget='1/1000', comparator='Declared fixed-theta rank-adaptive test; no certified rank upper bound supplied',
        baseline_expected_probe_lower=forecast['baseline_mean_lower'],
        candidate_expected_probe_upper=forecast['forecast_mean_upper'],
        guaranteed_expected_probe_reduction_percent=100*forecast['guaranteed_relative_probe_reduction'],
        both_worst_case_probe_caps=7, measurement_status='analytic resource bounds; exact abstract-law development probe',
        ordinary_comparison='Halt Fast! precedes generic learned/safe mixtures; known rank, private PIT and other mixtures are additional strong controls.'),
    feature_repair=dict(output_dimension=128, feature_dimension=35, error_rank=4,
        initial_full_probes=7, retained_feature_rank=7, candidate_truth_coordinates=1008,
        full_feature_interpolation_truth_coordinates=4480, component_reduction_percent=77.5,
        measurement_status='constructed access-accounting example, not measured application cost',
        ordinary_comparison='Identical two-sided interpolation ties; all bookkeeping, model work and oracle costs remain separately priced.'),
    conditional_margin=dict(joint_risk_upper='13/100', separate_risk_upper='13/47',
        bound_reduction_percent=53, calibration_failure_bound_approx=0.010654774993178336,
        calibration_target='1/20', measurement_status='same-receipt worst-case bounds, not observed error reduction'),
    partial_program=dict(before_certified_mean_cost_approx=16.165216,
        after_five_correct_receipts_approx=1.070587,
        measurement_status='constructed certified-cost frontier; proof acquisition assumed paid, no measured net gain'),
    query_interface=dict(randomized_hamming_cap=6, earlier_per_tape_purity_cap=7,
        comparison='Changed purity duty; more episodes, not a fee win.',
        balanced_binary_n8_query_reduction_percent=100*float(F(55,805)),
        balanced_binary_n8_reset100_fee_reduction_percent=100*float(F(55,12005)),
        comparison_scope='Same binary decision duty, cap8, equal prior; exact stopping vs full prefix; ordinary stopping ties.'),
    new_measured_audit_fee_reduction=None, new_measured_runtime_reduction=None,
    complete_economic_cost=None,
    historical_audit=dict(session='s10', observation_date_utc='2026-10-14', age_in_recurrences=5,
        near_target_fee_reduction_percent=57.12, named_work_reduction_percent=9.53,
        measurement_status='dated carry; no new audit-stream run'),
    ordinary_comparison='Same-information identical conventional implementations tie. Useful moderate novelty concerns the exact theorem or evidence/access composition, not conventional versus value-logic branding.',
    limitations='Same-model development; no independent confirmation, settled novelty, complete economics or promotion.',
    sources=[dict(path='s15/'+name, sha256=sha(HERE/name)) for name in (
        'norm_transport.md','joint_target.md','relative_scale.md','forecast_range.md',
        'forecast_probe.json','feature_repair.md','feature_probe.json','conditional_full.md',
        'conditional_probe.json','costed_programs.md','program_probe.json','pure_query_criteria.md',
        'symmetric_flows.md','stopping_probe.json')])
save(HERE/'progress_metrics.json', metrics)
save(HERE/'environment.json', dict(contributor='Codex (GPT-6)', python=sys.version,
    platform=platform.platform(), base_commit=BASE, branch='codex/discovery-20261023-s15',
    probe_environments='Bundled Python 3.12.14 for standard-library probes; C:/Python313/python.exe Python 3.13.14 with SciPy for LP/numerical probes. Inspect each source and recorded outcome. No failure attributed to hardware without evidence.'))

current = '''**Current continuation — October 23, 2026 UTC, Codex (GPT-6):**
[s15 checkpoint](s15/checkpoint.md), [findings](s15/findings.md),
[actuals](s15/effective_actuals.json), [single recurrence table](recurrences.md).
The fresh four-hour recurrence is CLOSED: 240.221316666666… research minutes.
C001/program is 2058.933820685783… and phase 3145.065188049933… minutes.
The 136 same-runtime intervals have sixteen research exclusions; explicit
context recovery and the long interruption are excluded. No active clock
remains. The 35-family inventory is unchanged; 39 passes are not new families.

**C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred; no promotion.**
Sharp counterfactual envelopes now cover general finite norms and joint
edits. A fallible forecast cuts an analytic expected-probe bound by at least
13.35499% against a declared control while retaining cap7. Structured model
repair and retained features give a 77.5% truth-coordinate reduction in a
constructed example. These are scoped resource/capability gains, not new
audit-stream fees or complete CPU savings. Identical ordinary methods tie.
[New targets](s15/verification_targets.md) N15-P/R15-C/I15-Q are UNASSESSED.
I13-R/v1's historical 55–75%, central65% and F01's 20–45%, central30% remain
different, unchanged events. Continue broad discovery under the useful,
moderately novel contribution standard. Default one hour unless overridden;
no automatic next session. Next deeper portfolio review:40 program hours.

'''
for name, end in [('P3_SEARCH_01.md','## 1. Objective and scope'), ('candidates.md','IDs S01 onward')]:
    p=DISC/name; s=text(p); i=s.index('**Current continuation'); j=s.index(end,i)
    write(p,s[:i]+current+s[j:])
p=HERE/'session.md'; s=text(p)
s=s.replace('Status: ACTIVE; fresh four-hour commitment.', 'Status: CLOSED; the fresh four-hour commitment is satisfied.',1)
s+=f"\n## Observed close\n\nResearch ended {a['research_closed_utc']}; the resident runtime closed\nat {a['clock_closed_utc']}. Session/program/phase research ns:\n{a['research_ns']:,} / {a['program_research_ns']:,} / {a['phase_research_ns']:,}.\nSee [checkpoint](checkpoint.md) and [effective actuals](effective_actuals.json).\nPublication is administration and receives zero research credit.\n"
write(p,s)
p=ROOT/'TODO_v3.md'; s=text(p); i=s.index('**Active recurrence'); j=s.index('Established October 6',i)
s=s[:i]+'''**Latest recurrence — October 23, 2026 UTC:** [s15](v3/discovery/s15/checkpoint.md)
is CLOSED after 240.221316666666… research minutes under the
[four-hour override](v3/decisions/2026-10-23_four_hour_recurrence.md).
[Actuals](v3/discovery/s15/effective_actuals.json) exclude interruption and
recovery. PR16 was verified merged before entry. C001 OPEN; P3-POS01
OUTSTANDING; no promotion or active clock remains.

'''+s[j:]
for old,new in [('1818.712504019117… research minutes','2058.933820685783… research minutes'),
    ('2904.843871383267… minutes','3145.065188049933… minutes'),
    ('1944.843871383267… minutes','2185.065188049933… minutes'),
    ('from [s14](v3/discovery/s14/checkpoint.md)','from [s15](v3/discovery/s15/checkpoint.md)')]:
    assert old in s; s=s.replace(old,new,1)
i=s.index('## Current author selection — October 23, 2026 UTC'); j=s.index('## Previous author selection',i)
s=s[:i]+'''## Current author selection — October 23, 2026 UTC

The resumed four-hour recurrence is complete. Read [findings](v3/discovery/s15/findings.md),
[assessment](v3/discovery/s15/scientific_assessment.md), [targets](v3/discovery/s15/verification_targets.md)
and the [progress table](v3/discovery/recurrences.md). Broader counterfactual
certificates, structured model correction, partial-proof policy selection and
restricted information channels advance the original five-question program.
Analytic probe bounds and constructed coordinate counts improve; no new
audit-stream or complete-cost gain is claimed. Ordinary identical methods tie.
New contribution events remain unassessed; historical forecasts retain their
separate scopes. Next deeper review:40 program hours; current total34.32 hours.
No automatic recurrence follows. Continue broad generation when next authorized.

'''+s[j:]; write(p,s)

p=ROOT/'v3/plan.v1.json'; plan=read(p)
for key in ('last_completed_session','last_preserved_session','last_discovery_session'): plan[key]='v3/discovery/s15/session.md'
plan['active_session']=None
plan['observed_progress'].update(research_ns=a['phase_research_ns'], research_minutes=a['phase_research_minutes'], source='v3/discovery/s15/effective_actuals.json', evidence_disposition='s15 closed; sixteen research exclusions and explicit recovery excluded; publication has zero research credit.')
plan['optional_recurrence_advice']['current_recommendation']='Continue broad generation from s15; cheaply test exact closest-prior overlap of numerical envelopes, an economical model-correction access regime, and the usefulness of the query-count interface before confirmation.'
d=plan['discovery_program']; d.update(research_ns=a['program_research_ns'], research_minutes=a['program_research_minutes'], latest_checkpoint='v3/discovery/s15/checkpoint.md', actuals='v3/discovery/s15/effective_actuals.json')
d['promotion'].update(forecast_status='N15-P/v1, R15-C/v1 and I15-Q/v1 unassessed; I13-R/v1 and F01 historical forecasts unchanged', new_target_record='v3/discovery/s15/verification_targets.md')
d['promotion']['additional_candidate_assessments'] += [dict(candidate=c,version='v1',probability=None,status='DEVELOPMENT; UNASSESSED',event='v3/discovery/s15/verification_targets.md') for c in ('N15-P','R15-C','I15-Q')]
d['current_cycle'].update(research_ns=a['program_research_ns'], research_minutes=a['program_research_minutes'], session='v3/discovery/s15/session.md', actuals='v3/discovery/s15/effective_actuals.json', clock_active=False, session_status=a['status'])
d['sessions'].append('v3/discovery/s15/session.md')
d['execution_cadence'].update(last_closed_session='s15', last_increment_research_ns=a['research_ns'],last_increment_research_minutes=a['research_minutes'],last_session_target_minutes=240,last_override_authority='v3/decisions/2026-10-23_four_hour_recurrence.md')
save(p,plan)

p=DISC/'recurrences.json'; raw=text(p); old=json.loads(raw); new=deepcopy(old)
fixed=deepcopy(old['rows'][-1]['fixed_metrics'])
for key,val in fixed.items():
    if key=='families_total': val.update(value=35,measurement_status='current inventory',observed_in_row='s15_cp01',absolute_delta=0,age_in_recurrences=0)
    else: val.update(measurement_status='carried_forward',age_in_recurrences=val.get('age_in_recurrences',0)+1,carried_in_row='s15_cp01',carried_from_row='s14_cp01',reason='No comparable new stream measurement or F01 reassessment in s15; dates/scopes retained.')
row=dict(id='s15_cp01',label='s15 resumed four-hour author override',checkpoint='s15/checkpoint.md',session='s15',contributor='Codex (GPT-6)',research_ns=a['research_ns'],cumulative_research_ns=a['program_research_ns'],research_minutes_rounded=240,cumulative_minutes_rounded=2059,new_family_ids=[],cumulative_new_family_count=35,
    metric_summary='General-norm joint-edit envelopes; at least13.35499% fewer expected range probes against declared control, cap7 retained; 1008 vs4480 truth-coordinate outputs in constructed feature-repair example. No fresh audit/CPU savings; ordinary ties.',
    metric_values=dict(scope_id=metrics['scope_id'],source='s15/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json')),
    description='39 constructive passes across numerical reuse, fallible models, partial proofs and computation-observation interfaces; early rejections and prior-art limits retained; no promotion.',
    time_evidence=dict(actuals='s15/effective_actuals.json',sha256=sha(HERE/'effective_actuals.json'),actuals_field='session_research_ns',cumulative_actuals_field='cycle_research_ns',research_closed_utc=a['research_closed_utc'],note='136 closed segments; sixteen research intervals and explicit recovery excluded.'),
    metric_sources=metrics['sources'],fixed_metrics=fixed,
    candidate_readiness=dict(new_candidates=['N15-P/v1','R15-C/v1','I15-Q/v1'],status='UNASSESSED; no promotion',record='s15/verification_targets.md',historical_I13_R=dict(range_percent=[55,75],central_percent=65,assessment_date_utc='2026-10-21',age_in_recurrences=2,status='carried, not reassessed')))
new['rows'].append(row)
new.update(prepared_date_utc='2026-10-23',source_commit=BASE,latest_checkpoint='s15/checkpoint.md',latest_effective_actuals='s15/effective_actuals.json',row_scope='25 chronological boundaries; one s15 recurrence; all24 earlier row objects byte-preserved.',total_research_ns=a['program_research_ns'],total_minutes_rounded=2059,total_research_minutes=a['program_research_minutes'],program_research_ns=a['program_research_ns'],phase_research_ns=a['phase_research_ns'],active_scope_id=metrics['scope_id'],active_row_ids=['s15_cp01'],current_separate_scope_ids=[metrics['scope_id']])
new['rendered_table']['row_ids'].append('s15_cp01'); new['rendered_table']['latest_row_id']='s15_cp01'
new['visible_resource_metrics']['s15']=dict(source='s15/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json'),observation_date_utc='2026-10-23',age_at_s15=0)
new['current_forecast']=deepcopy(fixed['confirmation_forecast_percent'])
new['current_readiness_assessment']=dict(status='New s15 events UNASSESSED; I13-R/v1 and F01 remain dated historical forecasts',record='s15/verification_targets.md',research_credit_ns=0)
# Replace top-level values without serializing historical row objects again.
decoder=json.JSONDecoder(); spans={}; pos=1
while True:
    while raw[pos].isspace() or raw[pos]==',': pos+=1
    if raw[pos]=='}': break
    key,pos=decoder.raw_decode(raw,pos)
    while raw[pos].isspace() or raw[pos]==':': pos+=1
    start=pos; _,pos=decoder.raw_decode(raw,pos); spans[key]=(start,pos)
changes=[]
for key,(start,end) in spans.items():
    if old[key]==new[key]: continue
    if key=='rows':
        body=raw[start:end]; value=body[:body.rfind(']')].rstrip()+',\n'+json.dumps(row,indent=2,ensure_ascii=False)+'\n  ]'
    else: value=json.dumps(new[key],indent=2,ensure_ascii=False)
    changes.append((start,end,value))
for start,end,value in sorted(changes,reverse=True): raw=raw[:start]+value+raw[end:]
assert json.loads(raw)==new and new['rows'][:24]==old['rows']
write(p,raw)
p=DISC/'recurrences.md'; s=text(p)
s=s.replace('24 recorded rows','25 recorded rows',1).replace('with s14**','with s15**',1).replace('1819 cumulative research minutes','2059 cumulative research minutes',1).replace('new s14 events UNASSESSED','new s15 events UNASSESSED',1)
line='| **[s15 resumed four-hour round](s15/checkpoint.md)** | **240** | **2059** | **35 (0)** | General-norm counterfactuals; polynomial-model correction; partial proofs; count-only interfaces; Oct23 UTC | **No fresh audit-fee run.** s10 **−57.12% carried, age5**. Constructed feature repair: **1008 vs4480 truth-coordinate outputs (−77.5%)**; full access/computation costs unpriced | Forecast: **expected full-vector probes at most6.060819 vs baseline at least6.995 (at least−13.35499%), cap7 retained**. Analytic, rank4/degree4/grid257/error.001. No new runtime/complete-work gain; s10 work **−9.53% carried, age5** | **Identical ordinary methods tie.** Halt Fast! precedes safe learned mixtures; two-sided interpolation is a strong correction control. No universal superiority claim | 144/272;254/272;258/272; carried, age19 | 80/80;60/80;223; carried, age8 | 16/16;11/11;1,718,749;4.7544×; carried, age7 | 0; carried, age7 | **N15-P/R15-C/I15-Q UNASSESSED.** I13-R/v1 55–75%, central65%, carried age2; F01 20–45%, central30%, age5 | **Sharp joint model/target/scale envelopes across finite norms.** Shared evidence supports all-input correction and late proof refinement. Same-receipt conditional risk upper13% vs27.66% is a guarantee comparison, not observed error. No promotion. |'
marker='\n## Resource columns: scope and evidence'; assert marker in s
s=s.replace(marker,'\n'+line+'\n'+marker,1)
s=s.replace('|\r\n\r\n|','|\r\n|').replace('|\n\n|','|\n|').replace('|\r\n\n|','|\r\n|')
s+='''\n## s15 scope and relevant gains

[Metrics](s15/progress_metrics.json) distinguish analytic expected-probe
bounds, constructed coordinate-output counts, mathematical capability and
unknown complete cost. Both percentages in the latest row have explicit
comparators; neither is a fresh audit-fee or CPU measurement. The latter
historical measures remain visibly dated carries. The conditional-risk
comparison uses the same calibration failure bound about0.010654775,
below0.05; its risk bound is a separate probability quantity. See
[assessment](s15/scientific_assessment.md) and [targets](s15/verification_targets.md)
for the broader useful-contribution goal and strong ordinary comparisons.
'''
write(p,s)
print(json.dumps(dict(status='CLOSED',rows=25,research_ns=a['research_ns'],program_ns=a['program_research_ns'])))
