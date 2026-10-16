"""One-time administrative closure of s11. No research credit or probe reruns."""
from pathlib import Path
from decimal import Decimal, getcontext
from copy import deepcopy
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DISC = HERE.parent
getcontext().prec = 45
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, obj): p.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def mins(ns): return str(Decimal(ns)/Decimal(60000000000))
def edit(p, old, new):
    text = p.read_text(encoding='utf-8')
    assert old in text, (p, old[:60])
    p.write_text(text.replace(old, new, 1), encoding='utf-8')

a = read(HERE/'effective_actuals.json')
assert a['clock_active'] is False and a['research_ns'] >= a['session_target_ns']
session_ns, program_ns, phase_ns = (a[k] for k in ('research_ns','program_research_ns','phase_research_ns'))
current = '''**Current continuation — October 15, 2026, Codex (GPT-6):**
[s11 checkpoint](s11/checkpoint.md), [findings](s11/findings.md),
[exact actuals](s11/effective_actuals.json), [single recurrence table](recurrences.md).
The four-hour increment is CLOSED: 240.069234431666666… research minutes;
C001/program is 1097.665670685783333… and phase 2183.797038049933333….
The effective clock is closed; the first dead runtime's raw open record is
preserved with zero credit for its unclosed interval. Default next session is
60 minutes, with explicit author overrides taking precedence.

**C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred; no candidate promoted.**
[F01](s11/forecast_final.md) carries its October 14 assessment: 20–45%, central
30%, without reassessment. Repair and invoice mathematical targets are
UNASSESSED. The 35 numbered families are unchanged; s11 develops connections
among S01/S04/S05/S06/S11/S31 rather than counting each variant as a new family.
Queries can enable certified edits; two of six exposed CNFs reduce minimax
regret by at least 46.0078% / 56.5029% against an equally querying static-menu
class. Exact ordinary realizations tie. Local feedback saves fees against full
feedback, but the ordinary bandit has the lowest total fees on the four streams.
Invoice information, source sensitivity and repeated-instance composition add
separate mathematical mechanisms. All are DEVELOPMENT. Read the
[scientific assessment](s11/scientific_assessment.md) and
[sixteen-hour portfolio review](s11/portfolio16.md), then use
[CONTINUE](CONTINUE.md) for broad discovery. Earlier dated records retain their scope.

'''
for name, end in [('P3_SEARCH_01.md','## 1. Objective and scope'), ('candidates.md','IDs S01 onward')]:
    p = DISC/name
    t = p.read_text(encoding='utf-8')
    start = t.index('**Current continuation')
    stop = t.index(end, start)
    p.write_text(t[:start]+current+t[stop:], encoding='utf-8')

edit(HERE/'session.md', 'Status: **IN PROGRESS; fresh four-hour commitment unfinished**.',
     'Status: **CLOSED; fresh four-hour commitment satisfied at a useful checkpoint**.')
edit(HERE/'session.md', 'This session is still in progress until its closing record says otherwise.',
'''The closing record is [checkpoint.md](checkpoint.md), with
[effective actuals](effective_actuals.json). Two runtimes supply 143 closed
intervals; six complete context intervals and the unknown final open interval
of the dead first runtime earn zero credit. The first runtime exited after an
invalid O/X command; no hardware cause is inferred. Its original bytes remain.
Research ended 2026-10-16T04:31:32.823678 UTC; the second runtime closed at
04:31:33.129541 UTC. Exact session/program/phase research nanoseconds are
14,404,154,065,900 / 65,859,940,241,147 / 131,027,822,282,996.
The publication phase earns no research credit. No automatic new session starts.
''')
edit(HERE/'checkpoint.md',
'''All credited intervals are exploratory X; same-model
proofs and exact checks do not manufacture an independent reliable-lane review.''',
'''The raw lanes record 91.38% X and 8.62% R, with R used for finite
screening. These are same-model exploratory-development checks, not independent
confirmation; the lower reliable-lane share follows the generative emphasis.''')

p = HERE/'interpretation.md'
t = p.read_text(encoding='utf-8'); first, rest = t.split('\n\n# ',1)
p.write_text('# '+rest.rstrip()+'\n\n'+first+'\n', encoding='utf-8')

p = ROOT/'TODO_v3.md'; t=p.read_text(encoding='utf-8')
start=t.index('**Active recurrence'); stop=t.index('Established October 6', start)
t=t[:start]+'''**Latest recurrence — October 15, 2026:** [s11](v3/discovery/s11/checkpoint.md)
is CLOSED after 240.069234431666666… research minutes under the
[four-hour override](v3/decisions/2026-10-15_four_hour_recurrence.md).
Its [effective actuals](v3/discovery/s11/effective_actuals.json) exclude context
and recovery gaps. C001 remains OPEN; P3-POS01 OUTSTANDING; no promotion.

'''+t[stop:]
t=t.replace('857.596436254117 research minutes','1097.665670685783 research minutes',1)
t=t.replace('Phase-three qualifying research is **1943.727803618267 minutes**.', 'Phase-three qualifying research is **2183.797038049933 minutes**.',1)
t=t.replace('**983.727803618267 minutes**','**1223.797038049933 minutes**',1)
t=t.replace('from [s10](v3/discovery/s10/checkpoint.md)', 'from [s11](v3/discovery/s11/checkpoint.md)',1)
idx=t.index('## Current author selection — October14,2026')
t=t[:idx]+'''## Current author selection — October 15, 2026

The fresh four-hour commitment is complete. Exact session/program/phase
nanoseconds: 14,404,154,065,900 / 65,859,940,241,147 / 131,027,822,282,996.
Read [findings](v3/discovery/s11/findings.md),
[assessment](v3/discovery/s11/scientific_assessment.md),
[portfolio review](v3/discovery/s11/portfolio16.md), and the updated
[progress table](v3/discovery/recurrences.md). Certified repair, local/free
feedback and invoice information connect several author questions. Two of six
inherited CNFs show at least 46.0078% / 56.5029% less regret than a static-menu
ablation that may query equally; identical ordinary procedures tie. Local
feedback saves 10.24% total fees against full feedback but costs more than
bandit0. No complete-computation saving is established on these new streams.

The 35-family count is unchanged. F01 carries its October 14 20–45%, central
30% assessment without reassessment; the new R11-M/I11-M mathematical targets
are UNASSESSED. Continue broad discovery under the useful, moderately novel
contribution standard. No candidate is promoted, P3-11 remains deferred, and
the next session defaults to one hour unless the author overrides it.

## Previous author selection — October 14, 2026
'''+t[idx+len('## Current author selection — October14,2026'):]
p.write_text(t,encoding='utf-8')

p=ROOT/'v3/plan.v1.json'; plan=read(p)
for key in ('last_completed_session','last_preserved_session','last_discovery_session'):
    plan[key]='v3/discovery/s11/session.md'
plan['active_session']=None
plan['observed_progress'].update(research_ns=phase_ns,source='v3/discovery/s11/effective_actuals.json',research_minutes=mins(phase_ns),evidence_disposition='s11 four-hour session closed after two-runtime reconciliation; all unknown gaps excluded. Development only; no s09, installation or publication credit.')
plan['optional_recurrence_advice']['current_recommendation']='Continue broad generative discovery from s11: source-sensitive certified repair, task-specific invoice information and inexpensive usefulness screens. Do not require another learning sweep or convergence on F01.'
d=plan['discovery_program']; d.update(research_ns=program_ns,research_minutes=mins(program_ns),latest_checkpoint='v3/discovery/s11/checkpoint.md',actuals='v3/discovery/s11/effective_actuals.json')
d['promotion']['forecast_status']='F01 October 14 assessment carried without reassessment; new R11-M and I11-M targets unassessed; no promotion'
d['promotion']['new_target_record']='v3/discovery/s11/verification_targets.md'
d['current_cycle'].update(research_ns=program_ns,research_minutes=mins(program_ns),session='v3/discovery/s11/session.md',actuals='v3/discovery/s11/effective_actuals.json',clock_active=False,session_status=a['status'])
d['sessions'].append('v3/discovery/s11/session.md')
d['execution_cadence'].update(last_closed_session='s11',last_increment_research_ns=session_ns,last_increment_research_minutes=mins(session_ns),last_session_target_minutes=240,last_override_authority='v3/decisions/2026-10-15_four_hour_recurrence.md')
d['completed_portfolio_reviews']=[{'horizon_minutes':960,'session':'s11','record':'v3/discovery/s11/portfolio16.md','scope':'generative portfolio review; no promotion'}]
d['next_portfolio_review_minutes']=2400
save(p,plan)

# Append an explicit current claim assessment, preserving all earlier claims.
p=ROOT/'v3/claim_ledger.md'; t=p.read_text(encoding='utf-8'); h,tail=t.split('\n',1)
t=h+'\n\n**Current pointer — October 15, 2026, Codex (GPT-6):** '
t+='[s11 assessment](discovery/s11/scientific_assessment.md) and '
t+='[claim-specific targets](discovery/s11/verification_targets.md). '
t+='P3-POS01 OUTSTANDING; no promotion. Earlier dated entries below retain their scope.\n'+tail
t+='''
## s11 broad discovery closure — October 15, 2026

Contributor: Codex (GPT-6). All evidence DEVELOPMENT; no new confirmation.

| Object / type | Explicit useful delta | Comparison and limitations | Evidence |
| --- | --- | --- | --- |
| Certified repair / mechanism and compact representation | Observations enable universally valid edit masks; two of six inherited CNFs reduce regret at least 46.0078% / 56.5029% against equally querying static menus | Query fees included; preparation and native prices unknown. Identical ordinary optimizer ties. Bounded-width extension is derived, not implemented. | [CNF results](discovery/s11/cnf_results.md), [prior comparison](discovery/s11/repair_prior.md), [structured extension](discovery/s11/structured_repair.md) |
| Local feedback / acquisition and learning | Feedback-only fees 4999 vs 112193, total 940053 vs 1047247 full feedback over four streams | Ordinary bandit0 is cheaper at 937656. Free estimator costs 938744; path control 944395. No complete-compute percentage. | [Paid results](discovery/s11/local_service_results.md), [path results](discovery/s11/path_results.md) |
| Invoice-limited information / mathematical characterization | Cap H gives degree H−1 span; checked support can restore identification; repeated same-instance episodes compose degrees | Explicit source-misspecification instability; fixed task surrogate bills, not general optimal experimental design or application validation | [Information](discovery/s11/invoice_information.md), [robust design](discovery/s11/invoice_design.md), [composition](discovery/s11/invoice_composition.md) |

R11-M and I11-M are proposed mathematical verification targets with UNASSESSED
readiness. The October 14 F01/S28-B1/V1 forecast is carried, not reassessed.
These developments support continued search for a useful, moderately novel
contribution; they do not establish priority or satisfy P3-POS01 yet.
'''
p.write_text(t,encoding='utf-8')

# Reconstruct only reporting aggregates from sealed development outputs.
sources=[]; streams=[]
for i in range(4):
    paths=[HERE/f'{folder}/c{i:02d}a0.json' for folder in ('ls01','fs01','ps01')]
    local,free,path=(read(p) for p in paths)
    assert local['worlds_sha256']==free['worlds_sha256']==path['worlds_sha256']
    arms={x['kind']:x for x in local['arms']}
    streams.append(dict(case=i,rounds=local['rounds'],worlds_sha256=local['worlds_sha256'],
                        local=arms['local']['total_query_fees'],full=arms['full']['total_query_fees'],bandit0=arms['bandit0']['total_query_fees'],
                        local_feedback=arms['local']['feedback_fees'],full_feedback=arms['full']['feedback_fees'],
                        free=free['total_query_fees'],path=path['execution_fees'],
                        local_matrix_products=arms['local']['matrix_counts']['matrix_products'],
                        full_matrix_products=arms['full']['matrix_counts']['matrix_products'],free_matrix_products=free['matrix_counts']['matrix_products']))
    sources += [dict(path=p.relative_to(DISC).as_posix(),sha256=sha(p)) for p in paths]
totals={k:sum(s[k] for s in streams) for k in streams[0] if k not in ('case','rounds','worlds_sha256')}
assert totals['local']==940053 and totals['full']==1047247 and totals['bandit0']==937656
metrics=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',scope_id='s11_four_stream_learning_v1',measurement_date_utc='2026-10-16',observed_in_row='s11_cp01',age_in_recurrences=0,streams=streams,totals=totals,
             change_percent=dict(local_vs_full=100*(totals['local']/totals['full']-1),local_feedback_vs_full=100*(totals['local_feedback']/totals['full_feedback']-1),local_vs_bandit0=100*(totals['local']/totals['bandit0']-1),free_vs_bandit0=100*(totals['free']/totals['bandit0']-1)),
             complete_economic_cost=None,complete_computation_change_percent=None,
             limitations='Four exposed synthetic streams, 2000 rounds each. Counter types differ; matrix products alone are not complete computation. Setup/native/retention prices remain unknown. Repair comparisons are a distinct regret scope.',sources=sources,
             repair=dict(scope_id='s11_cnf6_repair_v1',sources=6,query_cap=2,flip_cap=2,query_fee='1/4',flip_fee='1/8',ordinary_equivalent='same optimizer ties',source='s11/cnf_results.json',sha256=sha(HERE/'cnf_results.json')))
save(HERE/'progress_metrics.json',metrics)

# Preserve the raw bytes of all twenty previous JSON row objects.
p=DISC/'recurrences.json'; raw=p.read_bytes().decode('utf-8'); old=json.loads(raw); assert len(old['rows'])==20
new=deepcopy(old)
fixed=deepcopy(old['rows'][-1]['fixed_metrics'])
for k,v in fixed.items():
    if k=='families_total':
        v.update(value=35,measurement_status='current inventory',observed_in_row='s11_cp01',absolute_delta=0,age_in_recurrences=0)
    else:
        v.update(measurement_status='carried_forward',age_in_recurrences=v.get('age_in_recurrences',0)+1,carried_in_row='s11_cp01',carried_from_row='s10_cp01',reason='No comparable new measurement or F01 reassessment in s11; retain original date and event.')
row=dict(id='s11_cp01',label='s11 four-hour author override',checkpoint='s11/checkpoint.md',session='s11',contributor='Codex (GPT-6)',research_ns=session_ns,cumulative_research_ns=program_ns,research_minutes_rounded=240,cumulative_minutes_rounded=1098,new_family_ids=[],cumulative_new_family_count=35,
         metric_summary='Certified-repair regret improves at least 46.0078%/56.5029% vs equally querying static menus on two of six CNFs; ordinary equivalents tie. Local total fees 940053 vs full 1047247, but bandit0 937656 is lower. Free fees 938744; no complete-computation reduction established. Invoice span and composition are separate mathematical results.',
         metric_values={'scope_id':metrics['scope_id'],'separate_scope_ids':[metrics['scope_id'],metrics['repair']['scope_id']],'source':'s11/progress_metrics.json','sha256':sha(HERE/'progress_metrics.json')},
         description='Broad generation across checked sources/repairs, nearby-procedure feedback and invoice-limited information; 16-program-hour portfolio review completed. Mathematical targets R11-M/I11-M unassessed; F01 dated carry.',
         time_evidence={'actuals':'s11/effective_actuals.json','sha256':sha(HERE/'effective_actuals.json'),'actuals_field':'session_research_ns','cumulative_actuals_field':'cycle_research_ns','research_closed_utc':a['research_closed_utc'],'note':'143 closed intervals across two runtimes, six complete context exclusions and zero credit for dead-runtime open interval.'},
         metric_sources=sources+[{'path':'s11/cnf_results.json','sha256':sha(HERE/'cnf_results.json')}],fixed_metrics=fixed)
new['rows'].append(row)
new.update(prepared_date_utc='2026-10-16',source_commit='131f534c55cbd2b366074e255d4075e08e0b0933',latest_checkpoint='s11/checkpoint.md',latest_effective_actuals='s11/effective_actuals.json',row_scope='21 chronological recorded boundaries; s11 four-hour override is one recurrence. All twenty prior row objects remain byte-preserved.',total_research_ns=program_ns,total_minutes_rounded=1098,total_research_minutes=mins(program_ns),program_research_ns=program_ns,phase_research_ns=phase_ns,active_scope_id=metrics['scope_id'],active_row_ids=['s11_cp01'],current_separate_scope_ids=[metrics['scope_id'],metrics['repair']['scope_id']])
new['rendered_table']['row_ids'].append('s11_cp01'); new['rendered_table']['latest_row_id']='s11_cp01'
new['visible_resource_metrics']['s11']={'source':'s11/progress_metrics.json','sha256':sha(HERE/'progress_metrics.json'),'observation_date_utc':'2026-10-16','age_at_s11':0}
new['current_forecast']=deepcopy(fixed['confirmation_forecast_percent'])
new['current_readiness_assessment']={'status':'No new assessment; F01 October 14 carry, R11-M/I11-M UNASSESSED','record':'s11/forecast_final.md','historical_assessment_id':'F01_s10_final','research_credit_ns':0}

decoder=json.JSONDecoder(); spans={}; pos=1
while True:
    while raw[pos].isspace() or raw[pos]==',': pos+=1
    if raw[pos]=='}': break
    key,end=decoder.raw_decode(raw,pos); pos=end
    while raw[pos].isspace() or raw[pos]==':': pos+=1
    start=pos; _,pos=decoder.raw_decode(raw,pos); spans[key]=(start,pos)
changes=[]
for key,(start,end) in spans.items():
    if old[key]==new[key]: continue
    if key=='rows':
        body=raw[start:end]; close=body.rfind(']'); prefix=body[:close].rstrip()
        value=prefix+',\n'+json.dumps(row,ensure_ascii=False,indent=2)+'\n  ]'
    else: value=json.dumps(new[key],ensure_ascii=False,indent=2)
    changes.append((start,end,value))
for start,end,value in sorted(changes,reverse=True): raw=raw[:start]+value+raw[end:]
assert json.loads(raw)==new
p.write_bytes(raw.encode('utf-8'))
assert read(p)['rows'][:20]==old['rows']

p=DISC/'recurrences.md'; t=p.read_text(encoding='utf-8')
t=t.replace('**20 recorded rows, ending\nwith s10**','**21 recorded rows, ending\nwith s11**',1)
t=t.replace('**C001 OPEN · 858 cumulative research minutes · latest promotion forecast:\n20–45%, central 30%.**','**C001 OPEN · 1098 cumulative research minutes · F01 forecast carried from\nOctober 14: 20–45%, central 30%; new mathematical targets UNASSESSED.**',1)
t=t.replace('assessment is in the final row.','dated assessment is carried explicitly in the final row when not reassessed.',1)
line='| **[s11 four-hour round](s11/checkpoint.md)** | **240** | **1098** | **35 (0)** | **Learning:** four exposed streams ×2000 rounds; **repair:** six inherited CNFs; Oct16 UTC | **Local 940,053 vs full 1,047,247; −10.24%**<br>Feedback only 4,999 vs112,193; −95.54%<br>Free 938,744; bandit0 **937,656** | Local/full both **2,008,402 matrix products**; free1,658,916, with different other operations. Complete computation change unknown.<br>s10 near-target −9.53% carried, age1 | **Bandit0 beats local/free fees. Identical repair optimizers tie.** Local +0.256%, free +0.116% vs bandit0 | 144/272;254/272;258/272; carried, age15 | 80/80;60/80;223; carried, age4 | 16/16;11/11;1,718,749;4.7544×; carried, age3 | 0; carried, age3 | **F01 Oct14 carry:20–45%, central30%; age1. R11-M/I11-M unassessed** | **Certified-repair regret ≥46.01% / ≥56.50% lower than an equally querying static-menu class on two of six CNFs.** Three zero ties; one predictive-only gain. Invoice span, misspecification and same-instance composition results. 16-hour portfolio review complete; no promotion. |'
marker='\n## Resource columns: scope and evidence'
t=t.replace(marker,'\n'+line+'\n'+marker,1)
t+='''
## s11 scope and relevant gains

[Metrics and source hashes](s11/progress_metrics.json) preserve the four-stream
fee totals and partial counters. The local/full trajectories are identical;
local observation purchases are cheaper. Bandit0 has lower total fees than
both local and free learning, and the ordinary path learner costs 944395.
No complete computation improvement is claimed. The s10 near-target result is
a dated carry at age one, not a new measurement on these streams.

The [repair comparison](s11/cnf_results.md) concerns minimax regret with query
fees and certified edits. Its static-menu comparator can query but cannot add
newly certified masks. Two of six cases benefit from that capability; a third
benefits from prediction alone, and three have zero regret already. It is not
a superiority claim over the identical ordinary optimizer or a complete-cost
comparison. [Invoice results](s11/invoice_information.md) and
[composition](s11/invoice_composition.md) are mathematical deltas, not empirical
fee percentages. [Assessment](s11/scientific_assessment.md) separates each claim.
'''
p.write_text(t,encoding='utf-8')
print(json.dumps({'rows':21,'session_research_ns':session_ns,'program_research_ns':program_ns,'metrics_totals':totals,'historical_rows_preserved':True},indent=2))
