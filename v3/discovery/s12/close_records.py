"""One-time administrative s12 closure. No experiments or clock starts."""
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DISC=HERE.parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def edit(p,old,new):
    s=p.read_text(encoding='utf-8'); assert old in s,(str(p),old[:50])
    p.write_text(s.replace(old,new,1),encoding='utf-8')

a=read(HERE/'effective_actuals.json')
assert not a['clock_active'] and a['research_ns']>=a['session_target_ns']
assert len(read(DISC/'recurrences.json')['rows'])==21, 'One-time closure; inspect state.'

cap=read(HERE/'cap_two_probe.json')['totals']
shared=read(HERE/'shared_coin_probe.json')
selected=[x for x in shared['large'] if x['cap']==4 and x['coin_price']=='0']
assert len(selected)==2
metrics=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',
    scope_id='s12_scoped_constructions_v1',measurement_date_utc='2026-10-19',
    observed_in_row='s12_cp01',age_in_recurrences=0,
    fee_examples=[dict(**x,change_percent=-100*float(Fraction(x['gain_against_shared_fixed'])),
        interpretation='Exact constructed query/reset bill; controller/preparation and random-bit computation excluded.') for x in selected],
    computation=dict(**cap,change_percent=100*(cap['reduced_choices']/cap['private_choices']-1),
        units='enumerated candidate private choices',runtime_change_percent=None,
        interpretation='Same 632040 nonterminal states per arm; single combined runtime, not a wall-time or complete-cost saving.'),
    noisy_design=dict(candidate_fee=3690,baseline_fee=35967,change_percent=100*(3690/35967-1),
        interpretation='Constructed worst bill for the same sufficient precision bound; no application or total-controller claim.'),
    new_measured_audit_fee_reduction=None,complete_economic_cost=None,
    ordinary_comparison='Identical ordinary implementations tie. Shared-coin control erases four of twelve earlier gains. Per-task model selection matches the ensemble marginal-error bound.',
    mathematical_deltas=['Exact permission compiler and binary receipt/lineage reuse',
        'Task and joint-model adequacy envelopes under a fixed observation interface',
        'Median/interval and temporal receipt adapters',
        'Invoice price/readout/source boundaries; five-bit finite optimum 97/16'],
    limitations='All development, same-model checks; no independent confirmation, complete-service workload or established contribution novelty.',
    sources=[dict(path='s12/'+name,sha256=sha(HERE/name)) for name in
        ('cap_two_probe.json','shared_coin_probe.json','noise_probe.json','prefix_complete.json',
         'prefix_complete_disposition.md','lineage_probe.json','task_adequacy_probe.json',
         'interval_probe.json','union_probe.json')])
save(HERE/'progress_metrics.json',metrics)

current='''**Current continuation — October 19, 2026 UTC, Codex (GPT-6):**
[s12 checkpoint](s12/checkpoint.md), [findings](s12/findings.md),
[exact actuals](s12/effective_actuals.json), [single recurrence table](recurrences.md).
The fresh four-hour increment is CLOSED: 240.373166666666666… research minutes;
C001/program is 1338.03883735245 and phase 2424.1702047166 minutes.
159 closed intervals in one runtime; seven interrupted research intervals and
explicit context/recovery intervals excluded. No active research clock remains.

**C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred; no candidate promoted.**
The 35-family count is unchanged: s12 develops connections and adapters.
Task-scoped permissions can survive globally false models, with an explicit
joint-model adequacy extension, exact receipt/lineage reuse and a temporal
adapter. Cap-two reduction cuts one named search count by 76.3158%; constructed
invoice fees improve in some stated regimes. Ordinary realizations tie and
stronger ordinary controls erase or constrain several apparent gains.
See the [assessment](s12/scientific_assessment.md) and
[claim-specific targets](s12/verification_targets.md); those targets remain
UNASSESSED. F01 carries its October 14 20–45%, central 30% assessment.
Continue broad discovery under the useful, moderately novel contribution
standard. The next session defaults to one hour unless explicitly overridden;
no automatic session or automation starts. Earlier dated records retain scope.

'''
for name,end in [('P3_SEARCH_01.md','## 1. Objective and scope'),('candidates.md','IDs S01 onward')]:
    p=DISC/name;s=p.read_text(encoding='utf-8');start=s.index('**Current continuation');stop=s.index(end,start)
    p.write_text(s[:start]+current+s[stop:],encoding='utf-8')

edit(HERE/'session.md','Status: **IN PROGRESS; fresh four-hour commitment unfinished**.',
    'Status: **CLOSED; fresh four-hour commitment satisfied at a useful checkpoint**.')
with (HERE/'session.md').open('a',encoding='utf-8') as f:
    f.write('\n## Observed close\n\nResearch ended 2026-10-19T09:02:56.247919 UTC; runtime closed at\n09:02:56.323638 UTC. Exact session/program/phase research nanoseconds:\n14,422,390,000,000 / 80,282,330,241,147 / 145,450,212,282,996.\nSee [checkpoint](checkpoint.md) and [effective actuals](effective_actuals.json).\nRaw observations remain intact; publication earns no research credit.\n')

p=ROOT/'TODO_v3.md';s=p.read_text(encoding='utf-8');start=s.index('**Active recurrence');stop=s.index('Established October 6',start)
s=s[:start]+'''**Latest recurrence — October 19, 2026 UTC:** [s12](v3/discovery/s12/checkpoint.md)
is CLOSED after 240.373166666666666… research minutes under the
[four-hour override](v3/decisions/2026-10-18_four_hour_recurrence.md).
Its [effective actuals](v3/discovery/s12/effective_actuals.json) exclude context
and recovery gaps. C001 remains OPEN; P3-POS01 OUTSTANDING; no promotion.

'''+s[stop:]
s=s.replace('1097.665670685783 research minutes','1338.03883735245 research minutes',1)
s=s.replace('2183.797038049933 minutes','2424.1702047166 minutes',1)
s=s.replace('1223.797038049933 minutes','1464.1702047166 minutes',1)
s=s.replace('from [s11](v3/discovery/s11/checkpoint.md)','from [s12](v3/discovery/s12/checkpoint.md)',1)
s=s.replace('## Current author selection — October 15, 2026','''## Current author selection — October 19, 2026 UTC

The fresh four-hour recurrence is complete. Exact session/program/phase
nanoseconds: 14,422,390,000,000 / 80,282,330,241,147 / 145,450,212,282,996.
Read [findings](v3/discovery/s12/findings.md),
[assessment](v3/discovery/s12/scientific_assessment.md), and the
[progress table](v3/discovery/recurrences.md). Task-scoped model adequacy,
permission/evidence reuse, temporal constraints and invoice acquisition prices
provide constructive deltas across the five questions. The cap-two reduction
uses 76.3158% fewer candidate choices in one finite screen; this is not a runtime
or complete-cost percentage. Ordinary counterparts tie; several stronger
ordinary comparisons reject easy superiority claims.

No candidate is promoted. R12-S/I12-M/E12-R remain UNASSESSED; older R11-M/I11-M
remain unassessed and F01's October 14 range is carried. Broad discovery and
early rejection continue to be the policy. The next deeper portfolio review
is at 40 program hours; the program currently has about 22.30 hours.

## Previous author selection — October 15, 2026''',1)
p.write_text(s,encoding='utf-8')

p=ROOT/'v3/plan.v1.json';plan=read(p)
for k in ('last_completed_session','last_preserved_session','last_discovery_session'): plan[k]='v3/discovery/s12/session.md'
plan['active_session']=None
plan['observed_progress'].update(research_ns=a['phase_research_ns'],research_minutes=a['phase_research_minutes'],
    source='v3/discovery/s12/effective_actuals.json',evidence_disposition='s12 closed; exact one-runtime reconciliation excludes all context/recovery. Development only; no publication credit.')
plan['optional_recurrence_advice']['current_recommendation']='Continue broad discovery from s12, including task-motivated scoped reliance, invoice-limited measurement or a different connection. Keep strong ordinary controls and early rejection; no required large learner benchmark.'
d=plan['discovery_program'];d.update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],
    latest_checkpoint='v3/discovery/s12/checkpoint.md',actuals='v3/discovery/s12/effective_actuals.json')
d['promotion'].update(forecast_status='F01 October 14 carry; R11-M/I11-M and R12-S/I12-M/E12-R unassessed; no promotion',new_target_record='v3/discovery/s12/verification_targets.md')
d['current_cycle'].update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],
    session='v3/discovery/s12/session.md',actuals='v3/discovery/s12/effective_actuals.json',clock_active=False,session_status=a['status'])
d['sessions'].append('v3/discovery/s12/session.md')
d['execution_cadence'].update(last_closed_session='s12',last_increment_research_ns=a['research_ns'],
    last_increment_research_minutes=a['research_minutes'],last_session_target_minutes=240,
    last_override_authority='v3/decisions/2026-10-18_four_hour_recurrence.md')
save(p,plan)

p=DISC/'recurrences.json';raw=p.read_bytes().decode('utf-8');old=json.loads(raw);new=deepcopy(old)
fixed=deepcopy(old['rows'][-1]['fixed_metrics'])
for k,v in fixed.items():
    if k=='families_total': v.update(value=35,measurement_status='current inventory',observed_in_row='s12_cp01',absolute_delta=0,age_in_recurrences=0)
    else: v.update(measurement_status='carried_forward',age_in_recurrences=v.get('age_in_recurrences',0)+1,
        carried_in_row='s12_cp01',carried_from_row='s11_cp01',reason='No comparable new measurement or F01 reassessment in s12; original dates and scopes retained.')
row=dict(id='s12_cp01',label='s12 four-hour author override',checkpoint='s12/checkpoint.md',session='s12',contributor='Codex (GPT-6)',
    research_ns=a['research_ns'],cumulative_research_ns=a['program_research_ns'],research_minutes_rounded=240,cumulative_minutes_rounded=1338,
    new_family_ids=[],cumulative_new_family_count=35,metric_summary='Task/joint-model adequacy and exact evidence-reuse capabilities. Cap-two named choices -76.3158%; constructed query fees -8.1458% or query/reset -3.0612%. Ordinary equivalents tie; no new measured audit-fee or complete-cost gain.',
    metric_values=dict(scope_id=metrics['scope_id'],source='s12/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json')),
    description='Broad development across scoped reliance, counterfactual permissions, temporal models, invoice information/prices and reliability; strong ordinary controls and early negatives retained. No promotion.',
    time_evidence=dict(actuals='s12/effective_actuals.json',sha256=sha(HERE/'effective_actuals.json'),actuals_field='session_research_ns',cumulative_actuals_field='cycle_research_ns',research_closed_utc=a['research_closed_utc'],note='159 closed segments; seven interrupted research intervals and explicit recovery excluded.'),
    metric_sources=metrics['sources'],fixed_metrics=fixed)
new['rows'].append(row)
new.update(prepared_date_utc='2026-10-19',source_commit='b815009c1fcc458b85bd83129f2ab23c554e65eb',latest_checkpoint='s12/checkpoint.md',
    latest_effective_actuals='s12/effective_actuals.json',row_scope='22 chronological boundaries; one s12 recurrence; all 21 earlier row objects byte-preserved.',
    total_research_ns=a['program_research_ns'],total_minutes_rounded=1338,total_research_minutes=a['program_research_minutes'],
    program_research_ns=a['program_research_ns'],phase_research_ns=a['phase_research_ns'],active_scope_id=metrics['scope_id'],active_row_ids=['s12_cp01'],current_separate_scope_ids=[metrics['scope_id']])
new['rendered_table']['row_ids'].append('s12_cp01');new['rendered_table']['latest_row_id']='s12_cp01'
new['visible_resource_metrics']['s12']=dict(source='s12/progress_metrics.json',sha256=sha(HERE/'progress_metrics.json'),observation_date_utc='2026-10-19',age_at_s12=0)
new['current_forecast']=deepcopy(fixed['confirmation_forecast_percent'])
new['current_readiness_assessment']=dict(status='F01 dated carry; R12-S/I12-M/E12-R and older R11-M/I11-M unassessed',record='s12/forecast_final.md',historical_assessment_id='F01_s10_final',research_credit_ns=0)
# Replace only changed top-level values; preserve every old row's exact bytes.
decoder=json.JSONDecoder();spans={};pos=1
while True:
    while raw[pos].isspace() or raw[pos]==',': pos+=1
    if raw[pos]=='}': break
    key,pos=decoder.raw_decode(raw,pos)
    while raw[pos].isspace() or raw[pos]==':': pos+=1
    start=pos;_,pos=decoder.raw_decode(raw,pos);spans[key]=(start,pos)
changes=[]
for key,(start,end) in spans.items():
    if old[key]==new[key]: continue
    if key=='rows':
        body=raw[start:end];value=body[:body.rfind(']')].rstrip()+',\n'+json.dumps(row,indent=2,ensure_ascii=False)+'\n  ]'
    else: value=json.dumps(new[key],indent=2,ensure_ascii=False)
    changes.append((start,end,value))
for start,end,value in sorted(changes,reverse=True):raw=raw[:start]+value+raw[end:]
assert json.loads(raw)==new and new['rows'][:21]==old['rows']
p.write_bytes(raw.encode('utf-8'))

p=DISC/'recurrences.md';s=p.read_text(encoding='utf-8')
s=s.replace('**21 recorded rows, ending\nwith s11**','**22 recorded rows, ending\nwith s12**',1).replace('1098 cumulative research minutes','1338 cumulative research minutes',1)
s=s.replace('| Audit fees |','| Audit / acquisition fees |',1)
line='| **[s12 four-hour round](s12/checkpoint.md)** | **240** | **1338** | **35 (0)** | Exact constructed invoice bills; finite cap-two search; scoped mathematical services; Oct19 UTC | **Constructed query −8.1458%; query/reset −3.0612%** at n100, H4, stated zero coin price. No new measured audit saving. s10 near-target audit **−57.12% carried, age2** | **1,769,400 vs 7,470,800 choices: −76.3158%**, same632,040 states; no separate runtime or complete-cost saving. s10 named work −9.53% carried, age2 | **Identical ordinary routines tie.** Shared-coin control erases4/12 earlier gains; per-task model selection matches marginal ensemble bound | 144/272;254/272;258/272; carried, age16 | 80/80;60/80;223; carried, age5 | 16/16;11/11;1,718,749;4.7544×; carried, age4 | 0; carried, age4 | **F01 Oct14 carry20–45%, central30%; age2. R12-S/I12-M/E12-R UNASSESSED** | **Task and joint-model adequacy can support edits even when all full models are false.** Exact receipt/lineage reuse; median/temporal extension; invoice source/readout/prices; five-bit optimum97/16. No promotion. |'
marker='\n## Resource columns: scope and evidence';assert marker in s;s=s.replace(marker,'\n'+line+'\n'+marker,1)
s+='''
## s12 scope and relevant gains

[Metrics](s12/progress_metrics.json) distinguish constructed acquisition bills,
one named search-operation count and historical audit measurements. The cap-two
arms share 632,040 states; no separate wall-time reduction was measured. The
noisy-readout example's 89.7406% lower worst fee is also a constructed comparison
under one sufficient precision bound, not an application result. Ordinary
implementations tie. Stronger shared randomness erases four of twelve earlier
gains and positive random-choice prices can erase the remaining advantage.

[Task adequacy](s12/task_adequacy.md), [joint models](s12/union_adequacy.md),
[reuse](s12/scoped_service.md) and [temporal constraints](s12/temporal_receipts.md)
are explicit mathematical/capability deltas. The envelope is an ordinary
closure-based abstraction; contribution novelty and economical deployment
remain unassessed. [Assessment](s12/scientific_assessment.md) retains strong
ordinary controls and cheap rejections. All earlier rows and their dates remain.
'''
p.write_text(s,encoding='utf-8')
print(json.dumps(dict(rows=22,research_ns=a['research_ns'],program_ns=a['program_research_ns'],historical_rows_preserved=True)))
