"""Append the s20 recurrence without rewriting historical row objects."""
import copy, hashlib, json, re, subprocess
from pathlib import Path
R=Path.cwd();D=R/'v3/discovery';H=D/'s20'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
a=read(H/'effective_actuals.json'); scope='s20_confirmation_and_partial_decisions_v1'
files=['greatest_runs/a01/result.json','partial_runs/a01/result.json','refine_runs/a01/result.json','observe_runs/a01/result.json','incumbent_runs/a01/result.json','integration_runs/a01/result.json','continuous_runs/a01/result.json','transport_runs/a01/result.json','noise_runs/a02/result.json']
metrics=dict(contributor='Codex (GPT-6)',date_utc='2026-10-29',scope_id=scope,classification='Fixed V19 confirmation plus separately labeled development',confirmation=dict(event='V19-R/v1',status='PASS',source='v3/confirmation/v19a/result.json',sha256=sha(R/'v3/confirmation/v19a/result.json'),prospective_range_percent=[80,90],prospective_central_percent=85,previous_central_percent=65,post_review_confidence_range_percent=[80,90],post_review_confidence_central_percent=85,author_acceptance=False,ordinary_equivalent='ties outputs and resource bounds',calibrated=False),measurements={})
for name in files:
 d=read(H/name);metrics['measurements'][name]=dict(source='s20/'+name,sha256=sha(H/name),scalars={k:v for k,v in d.items() if not isinstance(v,(list,dict))})
metrics['greatest_point_control']=dict(cases=9,feasible=7,inconsistent=2,shortcut_optimizer_calls=34,complete_mask_optimizer_calls=266,relative_call_change_percent=(34-266)*100/266,scope='Restricted max-closed structural class; ordinary same shortcut ties; calls are not runtime or complete costs.')
metrics['partial_noisy_band']=dict(optimizer_calls=0,row_visits=134,coordinate_updates=28,scope='Specific band exclusion, not full range reconstruction or calibrated premises.')
metrics['new_economic_gain']=dict(audit_fee=None,host_cpu=None,complete_cost=None,reason='Not measured; no fresh saving claimed.')
metrics['carried_resource_measurements']=dict(source='s10/sf01/checked.json',sha256=sha(D/'s10/sf01/checked.json'),observed_session='s10',date_utc='2026-10-14',age_in_recurrences=10,audit_fee_change_percent=-57.12,counted_work_change_percent=-9.53,comparison='Prior scoped near6 scalar-prefix versus audit baseline; ordinary mirror ties; rounded historical values, not new data.')
metrics['source_records']=[dict(path=p,sha256=sha(R/p)) for p in ['v3/discovery/s20/decision_findings.md','v3/discovery/s20/scientific_assessment.md','v3/discovery/s20/readiness_pre.md','v3/contribution_review.md']]
put(H/'progress_metrics.json',metrics)
p=D/'recurrences.json';old=p.read_bytes().decode('utf-8');d=json.loads(old);assert len(d['rows'])==29
historical=copy.deepcopy(d['rows']);r=copy.deepcopy(d['rows'][-1]);rid='s20_cp01'
r.update(id=rid,label='s20 completion-oriented four-hour recurrence',checkpoint='s20/checkpoint.md',session='s20',research_ns=a['discovery_research_ns'],session_research_ns=a['research_ns'],confirmation_research_ns=a['confirmation_research_ns'],cumulative_research_ns=a['program_research_ns'],research_minutes_rounded=(a['discovery_research_ns']+30000000000)//60000000000,cumulative_minutes_rounded=(a['program_research_ns']+30000000000)//60000000000,metric_summary='V19 fixed contribution PASS; restricted control34 vs266 optimizer calls; partial zero-LP decision; no fresh fee/full-cost gain.',metric_values=dict(scope_id=scope,source='s20/progress_metrics.json',sha256=sha(H/'progress_metrics.json')),description='P3-11-A1 PASS after90.41min confirmation, plus149.67min discovery. P3-C pending author acceptance; ordinary equivalent ties; optional extensions unassessed.',time_evidence=dict(actuals='s20/effective_actuals.json',sha256=sha(H/'effective_actuals.json'),actuals_field='discovery_research_ns',cumulative_actuals_field='cycle_research_ns',research_closed_utc=a['research_closed_utc'],note='Discovery increment excludes90.41min P3-11; both count once to240.08min session and phase.'),metric_sources=[dict(path='s20/'+x,sha256=sha(H/x)) for x in ['findings.md','scientific_assessment.md','verification_targets.md','progress_metrics.json','decision_findings.md','greatest_findings.md']])
for k,v in r['fixed_metrics'].items():
 if k in ['families_total','confirmation_forecast_percent']:continue
 if 'age_in_recurrences'in v:v['age_in_recurrences']+=1
 v.update(carried_in_row=rid,carried_from_row='s19_cp01',reason='No fresh comparable legacy-stream measurement in s20; original date and scope retained.')
r['fixed_metrics']['families_total'].update(value=36,observed_in_row=rid,measurement_status='inventory unchanged')
f=copy.deepcopy(d['current_forecast']);f.update(assessment_id='V19_R_s20_pre',observed_in_row=rid,measurement_status='prospective same-event reassessment before A1',assessment_status='promoted; A1 subsequently PASS; author acceptance pending',central_percent=85,probability_range_percent=[80,90],value=85,previous_comparable_assessment_id='V19_R_s19',change_since_previous_assessment_percentage_points=20,gap_to_80_central_percentage_points=0,sources=[dict(path='s20/readiness_pre.md',sha256=sha(H/'readiness_pre.md'))],uncertainty='Subjective uncalibrated range; post-review confidence remains80--90. Recorded PASS is an outcome, not a probability.')
r['fixed_metrics']['confirmation_forecast_percent']=copy.deepcopy(f)
readiness=copy.deepcopy(d['current_readiness_assessment']);readiness.update(range_percent=[80,90],central_percent=85,status='P3-11-A1 PASS; P3-C author acceptance pending',record='s20/verification_targets.md');readiness['o18_same_event']['measurement_status']='carried from s19; not reassessed in s20';r['candidate_readiness']=readiness
r['confirmation_outcome']=metrics['confirmation'];d['rows'].append(r)
d.update(prepared_date_utc='2026-10-29',source_commit='54685b9b55039e2513d1aeda263841ed43fa82cd',previous_table_commit='54685b9b55039e2513d1aeda263841ed43fa82cd',latest_checkpoint='s20/checkpoint.md',latest_effective_actuals='s20/effective_actuals.json',row_scope='30 chronological boundaries; all29 earlier row object bytes preserved. s20 increment excludes separate P3-11 confirmation.',total_research_ns=a['program_research_ns'],total_minutes_rounded=r['cumulative_minutes_rounded'],total_research_minutes=a['program_research_minutes'],program_research_ns=a['program_research_ns'],phase_research_ns=a['phase_research_ns'],current_forecast=f,current_readiness_assessment=readiness,active_scope_id=scope,active_row_ids=[rid],current_separate_scope_ids=[scope])
d['forecast_assessments'].append(f);d['rendered_table']['row_ids'].append(rid);d['rendered_table']['latest_row_id']=rid;d['visible_resource_metrics']['s20']=dict(source='s20/progress_metrics.json',sha256=sha(H/'progress_metrics.json'),observation_date_utc='2026-10-29',age_at_s20=0)
d['s20_preservation']=dict(previous_rows=29,previous_row_canonical_sha256=hashlib.sha256(json.dumps(historical,sort_keys=True,separators=(',',':')).encode()).hexdigest(),previous_record_sha256=hashlib.sha256(old.encode()).hexdigest(),policy='Old row JSON text and all29 rendered row lines preserved exactly.')
# Preserve the entire preexisting rows-array content, including internal whitespace.
def span(s):
 i=re.search(r'"rows"\s*:\s*\[',s).end()-1
 _,end=json.JSONDecoder().raw_decode(s[i:]); return i,i+end
start,end=span(old);oldarray=old[start:end];new=json.dumps(d,indent=2,ensure_ascii=False)+'\n';x,y=span(new)
rowtext=json.dumps(r,indent=2,ensure_ascii=False);rowtext='\n'.join('    '+line for line in rowtext.splitlines())
newarray=oldarray[:-1].rstrip()+',\n'+rowtext+'\n  ]';new=new[:x]+newarray+new[y:];p.write_bytes(new.encode())
assert read(p)['rows'][:29]==historical
assert oldarray[:-1].rstrip() in new
p=D/'recurrences.md';oldmd=p.read_bytes();s=oldmd.decode();oldrows=[x for x in oldmd.splitlines(keepends=True) if x.startswith(b'| ')];assert len(oldrows)==31
start=s.index('This is the single');end=s.index('**Reading the table:**',start)
s=s[:start]+'''This is the single chronological recurrence table: **30 recorded rows, ending
with s20**. Append future recurrences to this same table.

**C001 OPEN pending author disposition · 3169 cumulative discovery minutes ·
V19-R/v1 P3-11-A1 PASS; P3-C acceptance pending.** Prospective readiness and
post-review confidence80--90%, central85%; ordinary equivalent ties. O18 carries
35--70%, central50%; N16 carries55--80%, central65%. Historical F01 and I13
retain their dated scopes. The[source record](recurrences.json) keeps exact clocks.
s20's240.08-minute session contains149.67 discovery plus90.41 confirmation
minutes; only discovery enters this table's cumulative program total.

'''+s[end:]
row='| **[s20 completion-oriented round](s20/checkpoint.md)** | **150 discovery +90.41 confirmation (240.08 session)** | **3169** | **36 (0)** | Fixed V19 confirmation; separate structural/partial-decision development; Oct28--29 UTC | **No fresh audit saving.** s10 −57.12% carried, age10; previous proof-service cost excess unchanged | **34 vs266 optimizer calls** on9 restricted-class cases; **0 LP** band exclusion after134 row visits/28 updates. Not a runtime/full-cost saving. s10 −9.53% carried, age10 | **Identical ordinary construction ties.** Greatest-point shortcut credited to established machinery; direct band, winner-label and full-source controls retained | 144/272;254/272;258/272; carried, age24 | 80/80;60/80;223; carried, age13 | 16/16;11/11;1,718,749;4.7544×; carried, age12 | 0; carried, age12 | **V19 80--90%, central85% (+20pp), then P3-11-A1 PASS.** Same confidence retained; P3-C author acceptance pending. N16/O18 carried | **Useful moderate synthesis supported:** complete gap-preserving range, rational checker and source recovery;12 supplemental Lean units with limits. Separate sharp stopping adds118 optimality certificates; incumbent-aware observation and continuous-loss controls. |'
lines=s.splitlines(keepends=True);last=max(i for i,l in enumerate(lines) if l.startswith('| '));lines.insert(last+1,row+'\n');s=''.join(lines)+'''
## s20 scope and relevant gains

[Metrics](s20/progress_metrics.json),[review](../contribution_review.md) and
[assessment](s20/scientific_assessment.md) separate completed confirmation from
optional development. The restricted34/266 call comparison is not universal
superiority or measured CPU saving. The zero-LP band duty can finish before
full range reconstruction. Ordinary equivalents tie. No fresh fee/full-cost
measurement is implied by dated carries. The240.08-minute session includes
90.41 confirmation minutes excluded from this discovery cumulative total.
All29 previous row objects and rendered rows are unchanged. The author gate
remains pending; no phase completion is inferred from a code merge.
'''
p.write_bytes(s.encode());assert all(x in p.read_bytes() for x in oldrows)
print('Appended row30, preserved29 historical JSON objects and Markdown row bytes, recorded separate stage minutes and scoped metrics.')
