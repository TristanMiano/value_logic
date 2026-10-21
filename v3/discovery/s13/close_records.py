"""One-time administrative s13 handoff. Never starts a clock or experiment."""
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DISC=HERE.parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def edit(p,old,new):
    s=p.read_text(encoding='utf-8'); assert old in s,(p,old[:50])
    p.write_text(s.replace(old,new,1),encoding='utf-8')

a=read(HERE/'effective_actuals.json')
assert not a['clock_active'] and a['research_ns']>=a['session_target_ns']
assert len(read(DISC/'recurrences.json')['rows'])==22, 'One-time closure; inspect state.'
panel=[x for x in read(HERE/'rate_probe.json')['panels'] if x['n']==100 and x['cap']==4 and x['reset']=='1/2']
assert len(panel)==1
p=panel[0]; old_fee=Fraction(p['old_menu_fee']); new_fee=Fraction(p['new_menu_fee'])
assert (p['new_options'],p['old_options'])==(592,494)
metrics=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',
    scope_id='s13_rate_warrant_value_v1',measurement_date_utc='2026-10-21',observed_in_row='s13_cp01',age_in_recurrences=0,
    acquisition=dict(n=100,cap=4,reset_fee='1/2',candidate_fee=str(new_fee),comparator_fee=str(old_fee),
        candidate_float=float(new_fee),comparator_float=float(old_fee),change_percent=100*float(new_fee/old_fee-1),
        comparison='Stronger prior adaptive prefix/fixed menu; exact query/reset bill; internal arithmetic and preparation excluded.'),
    computation=dict(candidate=592,comparator=494,units='preparation options examined',change_percent=100*(592/494-1),
        runtime_change_percent=None,total_computation_change_percent=None,interpretation='Named preparation work increases; no CPU or complete-computation gain.'),
    frontier=dict(lower_bound=130,constructed_fee=str(new_fee),replacement_factor=str(new_fee/130),
        gap_percent=100*float(new_fee/130-1),interpretation='Derived binary-experiment comparison under average query/reset budget, not measured speedup.'),
    numerical=dict(two_receipt_upper='95/188',separate_envelope_upper='47/78',threshold='51/100',
        robust_regret_upper=0.0053,partial_receipt_radius='1/1000',
        interpretation='Analytical positive-spectral worked duty; ordinary moment/dual methods tie; no acquisition or runtime saving measured.'),
    new_measured_audit_fee_reduction=None,complete_economic_cost=None,
    historical_audit=dict(session='s10',observation_date_utc='2026-10-14',age_in_recurrences=3,
        near_target_fee_reduction_percent=57.12,named_work_reduction_percent=9.53,measurement_status='dated carry'),
    ordinary_comparison='Identical implementations tie. Stronger previous menu used for fee comparison. Extra XOR tariffs can erase the fee gain; classical moment bounds match numerical results.',
    mathematical_deltas=['Proposed optimal all-size acquisition rate and binary decision frontier',
        'Partial-receipt task warrants, price-ray compression and robust inspection budgets',
        'Joint-edit boundaries and scalar-value decision certificates with partial numerical receipts'],
    limitations='Same-model development only; no independent confirmation, complete-service economics or settled moderate novelty.',
    sources=[dict(path='s13/'+name,sha256=sha(HERE/name)) for name in
        ('rate_probe.json','frontier_probe.json','slack_probe.json','ray_probe.json','budget_probe.json',
         'sharp_probe.json','two_value_decision.md','interval_value_certificate.md')])
save(HERE/'progress_metrics.json',metrics)

current=f'''**Current continuation — October 21, 2026 UTC, Codex (GPT-6):**
[s13 checkpoint](s13/checkpoint.md), [findings](s13/findings.md),
[exact actuals](s13/effective_actuals.json), [single recurrence table](recurrences.md).
The fresh four-hour increment is CLOSED: {a['research_minutes'][:19]}… research minutes.
C001/program is {a['program_research_minutes'][:20]}… and phase
{a['phase_research_minutes'][:20]}… minutes. All183 intervals share one runtime;
nine interrupted/mixed research intervals and explicit recovery are excluded.
No active research clock remains.

**C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred; no promotion.**
The35-family count is unchanged. A general acquisition-rate construction cuts
the stated n100/H4/reset1/2 query/reset bill2.370985%, while preparation rises
592 versus494 choices. Ordinary implementations tie. Partial-receipt action
warrants and scalar-value intervention certificates broaden the portfolio.
[I13-R/v1 readiness](s13/forecast_final.md) is55–75%, central65%, subjective
and below80%; R13-W/N13-V remain UNASSESSED. F01's October14 range20–45%,
central30%, is an unchanged different event. See [targets](s13/verification_targets.md).
Continue broad discovery under the useful, moderately novel contribution
standard; default one hour unless the author overrides. No automatic session.

'''
for name,end in [('P3_SEARCH_01.md','## 1. Objective and scope'),('candidates.md','IDs S01 onward')]:
    path=DISC/name;s=path.read_text(encoding='utf-8');i=s.index('**Current continuation');j=s.index(end,i)
    path.write_text(s[:i]+current+s[j:],encoding='utf-8')

edit(HERE/'session.md','Status: **ACTIVE; four-hour commitment outstanding**.',
    'Status: **CLOSED; four-hour commitment satisfied at a useful handoff**.')
with (HERE/'session.md').open('a',encoding='utf-8') as f:
    f.write(f"\n## Observed close\n\nResearch ended {a['research_closed_utc']}; runtime closed\nat {a['clock_closed_utc']}. Exact session/program/phase research ns:\n{a['research_ns']:,} / {a['program_research_ns']:,} / {a['phase_research_ns']:,}.\nSee [checkpoint](checkpoint.md) and [effective actuals](effective_actuals.json).\nNine explicit research replacements and all O/context intervals are excluded.\nSubsequent administrative publication receives zero research credit.\n")
recovery=HERE/'recovery.md';s=recovery.read_text(encoding='utf-8')
recovery.write_text('> **CLOSED:** use [checkpoint](checkpoint.md), [effective actuals](effective_actuals.json)\n> and [publication](publication.md). No clock or unfinished s13 floor remains.\n> Entries below are historical recovery observations.\n\n'+s,encoding='utf-8')

path=ROOT/'TODO_v3.md';s=path.read_text(encoding='utf-8');s=s[s.index('# Value Logic Phase Three'):]
i=s.index('**Latest recurrence');j=s.index('Established October 6',i)
s=s[:i]+f'''**Latest recurrence — October 21, 2026 UTC:** [s13](v3/discovery/s13/checkpoint.md)
is CLOSED after240.555733333333… research minutes under the
[four-hour override](v3/decisions/2026-10-20_four_hour_recurrence.md).
Its [actuals](v3/discovery/s13/effective_actuals.json) exclude interrupted and
recovery intervals. C001 OPEN; P3-POS01 OUTSTANDING; no promotion.

'''+s[j:]
s=s.replace('1338.03883735245 research minutes','1578.594570685783… research minutes',1)
s=s.replace('2424.1702047166 minutes','2664.725938049933… minutes',1)
s=s.replace('1464.1702047166 minutes','1704.725938049933… minutes',1)
s=s.replace('from [s12](v3/discovery/s12/checkpoint.md)','from [s13](v3/discovery/s13/checkpoint.md)',1)
marker='## Current author selection — October 19, 2026 UTC';assert marker in s
s=s.replace(marker,'''## Current author selection — October 21, 2026 UTC

The requested four-hour recurrence is complete. Read [findings](v3/discovery/s13/findings.md),
[assessment](v3/discovery/s13/scientific_assessment.md), [targets](v3/discovery/s13/verification_targets.md)
and the [progress table](v3/discovery/recurrences.md). The all-size acquisition
rate/frontier is the most cohesive new mathematical candidate. The named fee
comparison improves2.370985%, with more preparation and an ordinary tie.
Partial-receipt model warrants and numerical intervention certificates extend
other routes. I13-R/v1 has subjective55–75%, central65% readiness; it is below
the80% threshold. R13-W/N13-V remain unassessed. F01's dated forecast is unchanged.
Keep broad generation and early rejection. The next deeper review is40 program
hours; current program research is about26.31 hours. No automatic recurrence.

## Previous author selection — October 19, 2026 UTC''',1)
path.write_text(s,encoding='utf-8')

path=ROOT/'v3/plan.v1.json';plan=read(path)
for key in ('last_completed_session','last_preserved_session','last_discovery_session'):plan[key]='v3/discovery/s13/session.md'
plan['active_session']=None
plan['observed_progress'].update(research_ns=a['phase_research_ns'],research_minutes=a['phase_research_minutes'],source='v3/discovery/s13/effective_actuals.json',evidence_disposition='s13 closed; one-runtime reconciliation excludes nine interrupted/mixed research intervals and explicit recovery; no publication credit.')
plan['optional_recurrence_advice']['current_recommendation']='Continue broad discovery from s13, with short closest-prior/usefulness screens for the acquisition rate and a focused model-warrant or numerical duty; no large confirmation below readiness.'
d=plan['discovery_program'];d.update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],latest_checkpoint='v3/discovery/s13/checkpoint.md',actuals='v3/discovery/s13/effective_actuals.json')
d['promotion'].update(forecast_status='I13-R/v1 subjective55–75%, central65%, below threshold; R13-W/N13-V unassessed; existing F01 fields retain dated carry',new_target_record='v3/discovery/s13/verification_targets.md')
d['promotion']['additional_candidate_assessments']=[dict(candidate='I13-R',version='v1',probability=.65,probability_range=[.55,.75],assessment='v3/discovery/s13/forecast_final.md',event='v3/discovery/s13/verification_targets.md',status='DEVELOPMENT; below readiness',calibrated=False)]
d['current_cycle'].update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],session='v3/discovery/s13/session.md',actuals='v3/discovery/s13/effective_actuals.json',clock_active=False,session_status=a['status'])
d['sessions'].append('v3/discovery/s13/session.md')
d['execution_cadence'].update(last_closed_session='s13',last_increment_research_ns=a['research_ns'],last_increment_research_minutes=a['research_minutes'],last_session_target_minutes=240,last_override_authority='v3/decisions/2026-10-20_four_hour_recurrence.md')
save(path,plan)

path=DISC/'recurrences.json';raw=path.read_text(encoding='utf-8');old=json.loads(raw);new=deepcopy(old)
fixed=deepcopy(old['rows'][-1]['fixed_metrics'])
for key,val in fixed.items():
    if key=='families_total':val.update(value=35,measurement_status='current inventory',observed_in_row='s13_cp01',absolute_delta=0,age_in_recurrences=0)
    else:val.update(measurement_status='carried_forward',age_in_recurrences=val.get('age_in_recurrences',0)+1,carried_in_row='s13_cp01',carried_from_row='s12_cp01',reason='No comparable new measurement or F01 reassessment in s13; original dates and scopes retained.')
row=dict(id='s13_cp01',label='s13 four-hour author override',checkpoint='s13/checkpoint.md',session='s13',contributor='Codex (GPT-6)',research_ns=a['research_ns'],cumulative_research_ns=a['program_research_ns'],research_minutes_rounded=241,cumulative_minutes_rounded=1579,new_family_ids=[],cumulative_new_family_count=35,
    metric_summary='Constructed invoice fee -2.370985%; preparation592 vs494 (+19.84%); ordinary tie. General rate/binary frontier, partial-receipt warrants and numerical regret certificates. No new audit-stream measurement.',
    metric_values=dict(scope_id=metrics['scope_id'],source='s13/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json')),
    description='Broad development across priced information, fallible model warrants, counterfactual actions and scalar numerical decisions; close conventional antecedents and failed extensions retained. No promotion.',
    time_evidence=dict(actuals='s13/effective_actuals.json',sha256=sha(HERE/'effective_actuals.json'),actuals_field='session_research_ns',cumulative_actuals_field='cycle_research_ns',research_closed_utc=a['research_closed_utc'],note='183 closed segments; nine interrupted/mixed research intervals and explicit recovery excluded.'),
    metric_sources=metrics['sources'],fixed_metrics=fixed,
    candidate_readiness=dict(candidate='I13-R/v1',range_percent=[55,75],central_percent=65,status='subjective, uncalibrated, below80; different event from F01',record='s13/forecast_final.md'))
new['rows'].append(row)
new.update(prepared_date_utc='2026-10-21',source_commit='5d15dae2a6bc0903ff0589e242c9d9a3450ad9b5',latest_checkpoint='s13/checkpoint.md',latest_effective_actuals='s13/effective_actuals.json',row_scope='23 chronological boundaries; one s13 recurrence; all22 earlier row objects byte-preserved.',total_research_ns=a['program_research_ns'],total_minutes_rounded=1579,total_research_minutes=a['program_research_minutes'],program_research_ns=a['program_research_ns'],phase_research_ns=a['phase_research_ns'],active_scope_id=metrics['scope_id'],active_row_ids=['s13_cp01'],current_separate_scope_ids=[metrics['scope_id']])
new['rendered_table']['row_ids'].append('s13_cp01');new['rendered_table']['latest_row_id']='s13_cp01'
new['visible_resource_metrics']['s13']=dict(source='s13/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json'),observation_date_utc='2026-10-21',age_at_s13=0)
new['current_forecast']=deepcopy(fixed['confirmation_forecast_percent'])
new['current_readiness_assessment']=dict(status='I13-R/v1 subjective55–75%, central65%, below80; R13-W/N13-V unassessed; F01 dated carry',record='s13/forecast_final.md',candidate='I13-R/v1',range_percent=[55,75],central_percent=65,historical_assessment_id='F01_s10_final',research_credit_ns=0)
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
assert json.loads(raw)==new and new['rows'][:22]==old['rows']
path.write_bytes(raw.encode('utf-8'))

path=DISC/'recurrences.md';s=path.read_text(encoding='utf-8')
s=s.replace('**22 recorded rows, ending\nwith s12**','**23 recorded rows, ending\nwith s13**',1).replace('1338 cumulative research minutes','1579 cumulative research minutes',1)
s=s.replace('new mathematical targets UNASSESSED.','I13-R/v1 subjective55–75%, central65%; R13-W/N13-V UNASSESSED.',1)
line='| **[s13 four-hour round](s13/checkpoint.md)** | **241** | **1579** | **35 (0)** | Constructed invoice rate/frontier; partial-receipt warrants; numerical decisions; Oct21 UTC | **130.265 vs133.428571: −2.370985%** query/reset fees, n100/H4/f1/2, stronger prior menu. No fresh audit saving; s10 **−57.12% carried, age3** | **592 vs494 preparation options: +19.84%**. No runtime or complete-computation gain. s10 named work **−9.53% carried, age3** | **Identical ordinary methods tie.** Extra XOR prices erase fee gain; classical moment methods match value bounds | 144/272;254/272;258/272; carried, age17 | 80/80;60/80;223; carried, age6 | 16/16;11/11;1,718,749;4.7544×; carried, age5 | 0; carried, age5 | **I13-R/v1:55–75%, central65%, below80.** F01 Oct14 carry20–45%, central30%, age3; different event. R13-W/N13-V unassessed | **General optimal acquisition-rate candidate; binary frontier within0.204% of its lower bound in the example.** Partial-receipt action warrants; numerical two-value decision regret<0.0053. Scoped mathematical gains; no promotion. |'
marker='\n## Resource columns: scope and evidence';assert marker in s;s=s.replace(marker,'\n'+line+'\n'+marker,1)
s+='''\n## s13 scope and relevant gains\n\n[Metrics](s13/progress_metrics.json) separate constructed fee savings from\nincreased preparation and unknown complete cost. The0.204% frontier gap is\nderived, not a measured runtime gain. No new audit-stream panel was run.\n[Findings](s13/findings.md) and [assessment](s13/scientific_assessment.md) retain\nstrong ordinary comparisons and the numerical method's classical antecedents.\nThe new65% readiness concerns I13-R/v1; it does not update F01's30%. Earlier\nrows, scopes and dated measurements remain intact.\n'''
path.write_text(s,encoding='utf-8')
print(json.dumps(dict(rows=23,research_ns=a['research_ns'],program_ns=a['program_research_ns'],historical_rows_preserved=True)))
