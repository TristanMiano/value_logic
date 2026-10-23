"""Guarded one-time administrative s14 closure; never starts research."""
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DISC=HERE.parent
BASE='e2fa680858db59b502991789f21db18d4854d7ec'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def text(p):return p.read_bytes().decode('utf-8')
def write(p,s):p.write_bytes(s.encode('utf-8'))
def save(p,o):write(p,json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

a=read(HERE/'effective_actuals.json')
assert a['research_ns']==14_407_076_000_000 and not a['clock_active']
assert len(read(DISC/'recurrences.json')['rows'])==23,'Already closed; inspect instead of rerunning.'
interval=read(HERE/'partial_receipt_probe.json')
design=read(HERE/'receipt_design_probe_v2.json')
metrics=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',scope_id='s14_receipt_scope_quantizer_v1',
    measurement_date_utc='2026-10-23',observed_in_row='s14_cp01',age_in_recurrences=0,
    acquisition=dict(duty='Seven-bit Hamming quantizer; cap22; mean bit error1/8; reset100',
        candidate_fee='229/2',affine_class_conservative_lower='1463/12',
        saving_fraction='89/1463',saving_percent=100*float(F(89,1463)),
        comparison='All affine-terminal-cell strategies at the same expected error; internal arithmetic excluded.'),
    computation=dict(new_matrix_calls_in_partial_certificate=0,certificate_outward_sqrt_calls=4,
        complete_computation_change_percent=None,runtime_change_percent=None,
        interpretation='Zero calls describes the receipt certificate function only; its acquisition and validation harness are paid separately.'),
    numerical=dict(certified_band=interval['certified_band'],threshold='6/25',
        smaller_information_counterexample='32/125',norm_cap_lower_certificate='40000/885149',
        norm_cap_threshold='9/200',four_receipt_width=design['uniform_width'],
        earlier_four_receipt_width=design['previous_width'],
        four_receipt_width_reduction_percent=100*float(F(design['relative_width_reduction'])),
        interpretation='Exact constructed guarantees, not measured runtime or observed-error changes.'),
    learned_scope=dict(initial_max_integer_budget=1,refined_max_integer_budget=5,
        joint_receipt_rank_upper=1,marginal_cloud_rank_upper=20,retained_equations=980,
        same_scenario_risk_upper_joint='3369/100000',same_scenario_risk_upper_marginal='34413/200000',
        comparison='Same imported scenario envelope; improvement from preserving cross-case dependence, not a new statistical bound.'),
    closer_statistical_baseline=dict(N=200,k_bar=1,confidence='19/20',
        new_binomial_upper='33743/1000000',established_scenario_upper='3369/100000',
        finding='Established scenario bound is slightly stronger; do not headline improvement over weaker stable compression as a new statistical advance.'),
    pure_summary=dict(block=7,minimum_private_cap=7,mean_queries=23,episodes=4,
        earlier_cap=8,earlier_mean_queries=30,query_reduction_percent=100*7/30,
        scope='Finite deterministic/coin-tape-pure characterization; not optimum mean bill or loss-only duty.'),
    new_measured_audit_fee_reduction=None,complete_economic_cost=None,
    historical_audit=dict(session='s10',observation_date_utc='2026-10-14',age_in_recurrences=4,
        near_target_fee_reduction_percent=57.12,named_work_reduction_percent=9.53,measurement_status='dated carry'),
    ordinary_comparison='Identical conventional implementations tie. Hamming, matrix completion, scenario learning, abstract interpretation and robust least squares are explicit antecedents.',
    limitations='Same-model development; no independent confirmation, complete-service economics, settled moderate novelty or promotion.',
    sources=[dict(path='s14/'+name,sha256=sha(HERE/name)) for name in
        ('perfect_probe.json','partial_receipt_probe.json','receipt_design_probe_v2.json',
         'capped_upper_probe.json','scenario_compare_v2.json','joint_probe.json',
         'pure_functions_v4.json','learned_scope.md','joint_receipts.md')])
save(HERE/'progress_metrics.json',metrics)
save(HERE/'environment.json',dict(contributor='Codex (GPT-6)',python=sys.version,
    platform=platform.platform(),base_commit=BASE,branch='codex/discovery-20261022-s14',
    scientific_probes='Python standard library; no installed SciPy. Hardware instability permission available; no failure assigned to hardware without evidence.'))

current=f'''**Current continuation — October 23, 2026 UTC, Codex (GPT-6):**
[s14 checkpoint](s14/checkpoint.md), [findings](s14/findings.md),
[actuals](s14/effective_actuals.json), [single recurrence table](recurrences.md).
The fresh four-hour recurrence is CLOSED: 240.117933333333… research minutes.
C001/program is 1818.712504019117… and phase 2904.843871383267… minutes.
The142 same-runtime intervals have fourteen research exclusions and one
E-to-D reclassification; explicit context recovery is also excluded.
No active research clock remains. The35-family count is unchanged.

**C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred; no promotion.**
Small numerical receipts now certify new counterfactual thresholds; partial
and joint evidence supports changing model scopes; a nonlinear query/reset
construction saves at least6.0834% against its declared affine class at12.5%
mean error/reset100. Ordinary identical implementations tie. No new CPU or
audit-stream gain is claimed. A closer established scenario bound beats the
new elementary bound on its headline example; that comparison is retained.
[New contribution targets](s14/verification_targets.md) are UNASSESSED.
I13-R/v1's historical55-75%, central65% and F01's20-45%, central30% concern
different events and are unchanged. Continue broad discovery under the
useful, moderately novel contribution standard; default one hour unless
the author overrides. No automatic next session.

'''
for name,end in [('P3_SEARCH_01.md','## 1. Objective and scope'),('candidates.md','IDs S01 onward')]:
    p=DISC/name;s=text(p);i=s.index('**Current continuation');j=s.index(end,i)
    write(p,s[:i]+current+s[j:])
p=HERE/'session.md';s=text(p).replace('Status: ACTIVE.','Status: CLOSED; the four-hour commitment is satisfied.',1)
s+=f"\n## Observed close\n\nResearch ended {a['research_closed_utc']}; the resident runtime closed\nat {a['clock_closed_utc']}. Session/program/phase research ns:\n{a['research_ns']:,} / {a['program_research_ns']:,} / {a['phase_research_ns']:,}.\nSee [checkpoint](checkpoint.md) and [effective actuals](effective_actuals.json).\nPublication is administration and receives zero research credit.\n"
write(p,s)

p=ROOT/'TODO_v3.md';s=text(p);i=s.index('**Latest recurrence');j=s.index('Established October 6',i)
s=s[:i]+'''**Latest recurrence — October 23, 2026 UTC:** [s14](v3/discovery/s14/checkpoint.md)
is CLOSED after240.117933333333… research minutes under the
[four-hour override](v3/decisions/2026-10-22_four_hour_recurrence.md).
[Actuals](v3/discovery/s14/effective_actuals.json) exclude interruption and
recovery. C001 OPEN; P3-POS01 OUTSTANDING; no promotion.

'''+s[j:]
s=s.replace('1578.594570685783… research minutes','1818.712504019117… research minutes',1)
s=s.replace('2664.725938049933… minutes','2904.843871383267… minutes',1)
s=s.replace('1704.725938049933… minutes','1944.843871383267… minutes',1)
s=s.replace('from [s13](v3/discovery/s13/checkpoint.md)','from [s14](v3/discovery/s14/checkpoint.md)',1)
marker='## Current author selection — October 21, 2026 UTC';assert marker in s
s=s.replace(marker,'''## Current author selection — October 23, 2026 UTC

The requested four-hour recurrence is complete. Read [findings](v3/discovery/s14/findings.md),
[assessment](v3/discovery/s14/scientific_assessment.md), [targets](v3/discovery/s14/verification_targets.md)
and the [progress table](v3/discovery/recurrences.md). Stronger numerical
receipt decisions, jointly learned model scopes and nonlinear acquisition
extend the portfolio. Ordinary identical methods tie; new contribution
events remain unassessed. I13-R/v1 and F01 forecasts are dated carries,
not an overall program probability. Next deeper review:40 program hours;
current program research is about30.31 hours. No automatic recurrence.

## Previous author selection — October 21, 2026 UTC''',1)
write(p,s)

p=ROOT/'v3/plan.v1.json';plan=read(p)
for key in ('last_completed_session','last_preserved_session','last_discovery_session'):plan[key]='v3/discovery/s14/session.md'
plan['active_session']=None
plan['observed_progress'].update(research_ns=a['phase_research_ns'],research_minutes=a['phase_research_minutes'],source='v3/discovery/s14/effective_actuals.json',evidence_disposition='s14 closed; exclusions and E-to-D reclassification reconciled; publication excluded.')
plan['optional_recurrence_advice']['current_recommendation']='Continue broad generation from s14; cheaply assess closest-prior overlap and paid-usefulness for small numerical receipts, incomplete model scopes and nonlinear acquisition before expensive confirmation.'
d=plan['discovery_program'];d.update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],latest_checkpoint='v3/discovery/s14/checkpoint.md',actuals='v3/discovery/s14/effective_actuals.json')
d['promotion'].update(forecast_status='N14-T/v1, R14-L/v1 and I14-Q/v1 unassessed; I13-R/v1 and F01 historical forecasts unchanged',new_target_record='v3/discovery/s14/verification_targets.md')
d['promotion']['additional_candidate_assessments'] += [dict(candidate=c,version='v1',probability=None,status='DEVELOPMENT; UNASSESSED',event='v3/discovery/s14/verification_targets.md') for c in ('N14-T','R14-L','I14-Q')]
d['current_cycle'].update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],session='v3/discovery/s14/session.md',actuals='v3/discovery/s14/effective_actuals.json',clock_active=False,session_status=a['status'])
d['sessions'].append('v3/discovery/s14/session.md')
d['execution_cadence'].update(last_closed_session='s14',last_increment_research_ns=a['research_ns'],last_increment_research_minutes=a['research_minutes'],last_session_target_minutes=240,last_override_authority='v3/decisions/2026-10-22_four_hour_recurrence.md')
save(p,plan)

p=DISC/'recurrences.json';raw=text(p);old=json.loads(raw);new=deepcopy(old)
fixed=deepcopy(old['rows'][-1]['fixed_metrics'])
for key,val in fixed.items():
    if key=='families_total':val.update(value=35,measurement_status='current inventory',observed_in_row='s14_cp01',absolute_delta=0,age_in_recurrences=0)
    else:val.update(measurement_status='carried_forward',age_in_recurrences=val.get('age_in_recurrences',0)+1,carried_in_row='s14_cp01',carried_from_row='s13_cp01',reason='No comparable new stream measurement or F01 reassessment in s14; dates/scopes retained.')
row=dict(id='s14_cp01',label='s14 four-hour author override',checkpoint='s14/checkpoint.md',session='s14',contributor='Codex (GPT-6)',research_ns=a['research_ns'],cumulative_research_ns=a['program_research_ns'],research_minutes_rounded=240,cumulative_minutes_rounded=1819,new_family_ids=[],cumulative_new_family_count=35,
    metric_summary='Constructed fee at least6.0834% lower vs affine class at12.5% mean error; exact numerical thresholds; shared scope1->5; same scenario bound0.172065->0.033690 from retained joint evidence. No fresh audit or CPU savings; ordinary ties.',
    metric_values=dict(scope_id=metrics['scope_id'],source='s14/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json')),
    description='Broad constructive discovery, early rejections and closest-prior corrections; no promotion.',
    time_evidence=dict(actuals='s14/effective_actuals.json',sha256=sha(HERE/'effective_actuals.json'),actuals_field='session_research_ns',cumulative_actuals_field='cycle_research_ns',research_closed_utc=a['research_closed_utc'],note='142 closed segments; fourteen research exclusions, one E-to-D reclassification, explicit recovery excluded.'),
    metric_sources=metrics['sources'],fixed_metrics=fixed,
    candidate_readiness=dict(new_candidates=['N14-T/v1','R14-L/v1','I14-Q/v1'],status='UNASSESSED; no promotion',record='s14/verification_targets.md',historical_I13_R=dict(range_percent=[55,75],central_percent=65,assessment_date_utc='2026-10-21',age_in_recurrences=1,status='carried, not reassessed')))
new['rows'].append(row)
new.update(prepared_date_utc='2026-10-23',source_commit=BASE,latest_checkpoint='s14/checkpoint.md',latest_effective_actuals='s14/effective_actuals.json',row_scope='24 chronological boundaries; one s14 recurrence; all23 earlier row objects byte-preserved.',total_research_ns=a['program_research_ns'],total_minutes_rounded=1819,total_research_minutes=a['program_research_minutes'],program_research_ns=a['program_research_ns'],phase_research_ns=a['phase_research_ns'],active_scope_id=metrics['scope_id'],active_row_ids=['s14_cp01'],current_separate_scope_ids=[metrics['scope_id']])
new['rendered_table']['row_ids'].append('s14_cp01');new['rendered_table']['latest_row_id']='s14_cp01'
new['visible_resource_metrics']['s14']=dict(source='s14/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json'),observation_date_utc='2026-10-23',age_at_s14=0)
new['current_forecast']=deepcopy(fixed['confirmation_forecast_percent'])
new['current_readiness_assessment']=dict(status='New s14 events UNASSESSED; I13-R/v1 and F01 remain dated historical forecasts',record='s14/verification_targets.md',research_credit_ns=0)
decoder=json.JSONDecoder();spans={};pos=1
while True:
    while raw[pos].isspace() or raw[pos]==',':pos+=1
    if raw[pos]=='}':break
    key,pos=decoder.raw_decode(raw,pos)
    while raw[pos].isspace() or raw[pos]==':':pos+=1
    start=pos;_,pos=decoder.raw_decode(raw,pos);spans[key]=(start,pos)
changes=[]
for key,(start,end) in spans.items():
    if old[key]==new[key]:continue
    if key=='rows':
        body=raw[start:end];value=body[:body.rfind(']')].rstrip()+',\n'+json.dumps(row,indent=2,ensure_ascii=False)+'\n  ]'
    else:value=json.dumps(new[key],indent=2,ensure_ascii=False)
    changes.append((start,end,value))
for start,end,value in sorted(changes,reverse=True):raw=raw[:start]+value+raw[end:]
assert json.loads(raw)==new and new['rows'][:23]==old['rows']
write(p,raw)

p=DISC/'recurrences.md';s=text(p)
s=s.replace('23 recorded rows','24 recorded rows',1).replace('with s13**','with s14**',1).replace('1579 cumulative research minutes','1819 cumulative research minutes',1)
s=s.replace('I13-R/v1 subjective55–75%, central65%; R13-W/N13-V UNASSESSED.','I13-R/v1 historical55–75%, central65%; new s14 events UNASSESSED.',1)
line='| **[s14 four-hour round](s14/checkpoint.md)** | **240** | **1819** | **35 (0)** | Constructed nonlinear invoice; retained numerical receipts; partial/joint learned scope; Oct23 UTC | **114.5 vs affine lower121.9167: at least−6.0834%**, cap22/reset100,12.5% mean error. No fresh audit saving; s10 **−57.12% carried, age4** | **0 new operator calls in the partial-receipt certificate**, original acquisition paid; no CPU/complete-work gain. Pure-summary queries23 vs30 at smaller cap7 vs8, same4 episodes. s10 work **−9.53% carried, age4** | **Identical ordinary methods tie.** Established scenario bound slightly beats new elementary bound; Hamming, robust LS and matrix completion are prior ingredients | 144/272;254/272;258/272; carried, age18 | 80/80;60/80;223; carried, age7 | 16/16;11/11;1,718,749;4.7544×; carried, age6 | 0; carried, age6 | **New N14-T/R14-L/I14-Q UNASSESSED.** I13-R/v1 55–75%, central65%, carried age1; F01 20–45%, central30%, age4 | **Two partial receipts certify value<0.24 where one admits0.256.** Authorized budget1→5; retaining cross-case dependence tightens same risk certificate17.21%→3.37%; four-receipt width−49.68%. No promotion. |'
marker='\n## Resource columns: scope and evidence';assert marker in s
s=s.replace(marker,'\n'+line+'\n'+marker,1)
# Keep one continuous table without changing any historical row bytes.
s=s.replace('|\r\n\r\n|','|\r\n|').replace('|\n\n|','|\n|').replace('|\r\n\n|','|\r\n|')
s+='''\n## s14 scope and relevant gains\n\n[Metrics](s14/progress_metrics.json) distinguish modeled query/reset fees,\ncertificate capabilities, zero post-receipt operator calls and unmeasured\ncomplete economics. The same scenario envelope underlies17.21%→3.37%; this\nis retained-information value, not observed error reduction or a new bound.\nThe elementary statistical bound lost to a closer established comparator.\n[Assessment](s14/scientific_assessment.md) and [targets](s14/verification_targets.md)\nkeep the broader useful-contribution goal and exact ordinary comparisons.\n'''
write(p,s)
print(json.dumps(dict(status='CLOSED',rows=24,research_ns=a['research_ns'],program_ns=a['program_research_ns'])))
