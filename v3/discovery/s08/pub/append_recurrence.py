"""Append one s08 recurrence; preserve all 18 historical row objects."""
from pathlib import Path
import json,hashlib,copy,subprocess
root=Path(__file__).resolve().parents[4];base=root/'v3/discovery';here=base/'s08'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
a=load(here/'effective_actuals.json');p=base/'recurrences.json';doc=load(p)
old=copy.deepcopy(doc['rows']);assert len(old)==18 and old[-1]['id']=='s07_cp01'
sources=[];totals={}
design=load(here/'bc02/design.json')
for arm in design['arms']:
 values={k:0 for k in ('outputs','base_audit_fee','physical_audits','named_units','setup_units')}
 for case in design['cases']:
  path=here/'bc02'/f"{case['name']}_{arm}"/'result.json';v=load(path)
  for k in values:values[k]+=v[k]
  sources.append(dict(path=path.relative_to(base).as_posix(),sha256=sha(path)))
 totals[arm]=values
progress=dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',prepared_date_utc='2026-10-14',research_credit_ns=0,scope_id='s32_bc02_star4_h128_v1',measurement_date_utc='2026-10-14',denominator_per_arm=512,duty='Same original-source tolerance/replacement duties on four fresh 128-row star streams',seeds=list(range(8141740,8141744)),menu=design['arms'],source=design,cost_convention='Physical base audit fees and instrumented named work reported separately; setup included; no complete economic conversion, unmeasured host/native/retention costs not zero.',logical_acquisition='Four historical resolution steps reused, zero new complete SAT calls',totals=totals,sources=sources,all_16_acquisitions_first_attempt=True,failed_checking_attempts=1,comparison_scope='Within bc02 only; not a rerun of ac02 or F01.')
save(here/'progress_results.json',progress)
bc=dict(scope_id=progress['scope_id'],measurement_date_utc='2026-10-14',observed_in_row='s08_cp01',age_in_recurrences=0,measurement_status='first measurement',denominator=512,source='s08/progress_results.json',sha256=sha(here/'progress_results.json'),totals=totals,fee_delta_budget_minus_cover=totals['budget']['base_audit_fee']-totals['cover']['base_audit_fee'],named_delta_budget_minus_cover=totals['budget']['named_units']-totals['cover']['named_units'],ordinary_mirror_delta_fee=0,ordinary_mirror_delta_named=0,complete_economic_cost=None,complete_cost_reason='Unassigned economic prices, host/native work and retention; no F01-domain observation.')
gc=dict(scope_id='s32_gc02_graph12_h64_v1',measurement_date_utc='2026-10-14',observed_in_row='s08_cp01',age_in_recurrences=0,measurement_status='first measurement',denominator=768,source='s08/gc02/summary.json',sha256=sha(here/'gc02/summary.json'),totals=load(here/'gc02/summary.json')['selected_complete_totals'],additional_failed_prefix=dict(fee=6595,receipts=1216,named_units_lower_bound=18576219,unfinished_computation='unknown'))
doc['comparison_scopes'][bc['scope_id']]=dict(duty=progress['duty'],horizon=128,cases=4,arms=design['arms'],units=progress['cost_convention'],caps='Query budget B=C and checked anchor; original-source action tolerance fixed by design',design_source='s08/bc02/design.json',design_sha256=sha(here/'bc02/design.json'))
doc['comparison_scopes'][gc['scope_id']]=dict(duty='Original-source graph robust repair/replacement, twelve sources, 64 requests each',arms=['lazy','ordinary_lazy','scan','anchor'],sizes=[8,16,32],graphs=['path','cycle','clique','sparse'],units=progress['cost_convention'],design_source='s08/gc02/design.json',design_sha256=sha(here/'gc02/design.json'))
doc['separate_scope_measurements'] += [bc,gc]
f=copy.deepcopy(doc['current_forecast']);f.update(assessment_id='F01_s08_final',observed_in_row='s08_cp01',assessment_utc='2026-10-14T04:14:54.314199+00:00',assessment_time_scope='Recorded end of in-session synthesis containing the final assessment',previous_comparable_row='s07_cp01',recurrence_absolute_delta=0,previous_comparable_assessment_id='F01_s07_final',change_since_previous_assessment_percentage_points=0,rationale='New source-bound policy/cover and scalar-proof capability is constructive, but its ordinary mirror ties and its domains do not establish the unchanged F01 full-cost event. General graph costs and model-adequacy negatives support no upward revision.',sources=[dict(path='s08/forecast_final.md',sha256=sha(here/'forecast_final.md'),locator='Final unchanged-event assessment')],next_decision='Construct a small paid matroid/group-query route; specify a separate useful event before forecasting it. F01 requires its original matched complete-cost evidence.')
f['sensitivity']=dict(raise_forecast='Material matched complete-cost gains on the specified F01 domain with a robust price region and sound checked outputs.',lower_forecast='Further inability to change purchases or nonquotation costs on that domain, or failure of required soundness/generalization assumptions.')
fixed=copy.deepcopy(old[-1]['fixed_metrics'])
for k,v in fixed.items():
 if k in ('families_total','confirmation_forecast_percent'):continue
 v.update(measurement_status='carried_forward',age_in_recurrences=v.get('age_in_recurrences',0)+1,carried_in_row='s08_cp01',carried_from_row='s07_cp01',last_actual_row=v.get('last_actual_row',v.get('observed_in_row')),absolute_delta=None,reason='No comparable new acquisition in s08; original dated measurement carried, not a measured zero change.')
 if 'coverage_delta_percentage_points' in v:v['coverage_delta_percentage_points']=None
fixed['families_total']=dict(scope_id='c001_numbered_families',measurement_status='measured',observed_in_row='s08_cp01',age_in_recurrences=0,value=33,units='families',previous_comparable_row='s07_cp01',absolute_delta=3,delta_units='families',sources=[dict(path='candidates.md',locator='S31-S33')],interpretation='Breadth, not readiness.')
fixed['confirmation_forecast_percent']=dict(f,age_in_recurrences=0,absolute_delta=0)
row=dict(id='s08_cp01',label='s08 four-hour author override',checkpoint='s08/cp01.md',session='s08',contributor='Codex (GPT-6)',research_ns=a['research_ns'],cumulative_research_ns=a['cycle_research_ns'],research_minutes_rounded=240,cumulative_minutes_rounded=738,new_family_ids=['S31','S32','S33'],cumulative_new_family_count=33,metric_summary='bc02 budget/ordinary tie: 512 outputs each, 2886 fee/137310 named units; cover2937/157452 and anchor4608/152022. gc02 saves6.00% fees against anchor with much higher computation. No new F01 measurement; forecast20-45%, central30%, change0.',metric_values=dict(metric_type='New separate-scope development; old S28 and legacy duties carried',scope_id=bc['scope_id'],separate_scope_ids=[bc['scope_id'],gc['scope_id']],new_scope_measurements=[bc,gc]),description='Source-bound budgeted cover improves both recorded components on star sources and ordinary budget ties. Matroid/group-query and scalar box-proof bridges extend capability; policy-learning adequacy and broader graph costs remain obstacles. All failed work retained.',time_evidence=dict(actuals='s08/effective_actuals.json',sha256=sha(here/'effective_actuals.json'),actuals_field='session_research_ns',cumulative_actuals_field='cycle_research_ns',dispositions='s08/dispositions.json',effective_observation=a['observed'],research_closed_utc=a['research_closed_utc'],note='139 same-runtime closed segments, five exclusions, no stale open/crash or publication credit.'),metric_sources=[dict(path='s08/progress_results.json',sha256=sha(here/'progress_results.json')),dict(path='s08/gc02/summary.json',sha256=sha(here/'gc02/summary.json')),dict(path='s08/forecast_final.md',sha256=sha(here/'forecast_final.md'))],fixed_metrics=fixed)
doc['rows'].append(row);assert doc['rows'][:-1]==old
doc.update(prepared_by='Codex (GPT-6)',prepared_date_utc='2026-10-14',source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip(),latest_checkpoint='s08/cp01.md',latest_effective_actuals='s08/effective_actuals.json',row_scope='19 chronological recorded boundaries; s08 four-hour override is one recurrence, all 18 previous rows unchanged.',total_research_ns=a['cycle_research_ns'],total_minutes_rounded=738,total_research_minutes=a['cycle_research_minutes'],program_research_ns=a['program_research_ns'],phase_research_ns=a['phase_research_ns'],current_forecast=f,active_scope_id=bc['scope_id'])
doc['forecast_assessments'].append(copy.deepcopy(f));doc['readiness_assessment_history'].append(copy.deepcopy(doc['current_readiness_assessment']))
doc['current_readiness_assessment'].update(prepared_by='Codex (GPT-6)',assessment_utc=f['assessment_utc'],basis_checkpoint='s08/cp01.md',principal_blocker=f['rationale'],sources=f['sources'],central_change_since_previous_recurrence_percentage_points=0)
doc['active_row_ids']=[x['id'] for x in doc['rows']];doc['rendered_table'].update(row_ids=doc['active_row_ids'],latest_row_id='s08_cp01')
doc['reporting_history'].append(dict(date_utc='2026-10-14',contributor='Codex (GPT-6)',change='Append s08 as row19; preserve previous18 row objects; carry dated old metrics and add separate bc02/gc02 scope records.',research_credit_ns=0))
save(p,doc)
md=base/'recurrences.md';t=md.read_text(encoding='utf-8');oldlines=[l for l in t.splitlines() if l.startswith('| [') or l.startswith('| **[')]
t=t.replace('Maintained by **ChatGPT (GPT-6 Astra Pro)**.','Current maintenance: **Codex (GPT-6)**; earlier attributions preserved.').replace('**18 recorded rows, ending\nwith s07**','**19 recorded rows, ending\nwith s08**').replace('497 cumulative research minutes','738 cumulative research minutes')
lines=t.splitlines();idx=max(i for i,l in enumerate(lines) if l.startswith('| ') and '(s07/cp01.md)' in l)+1
lines.insert(idx,'| [s08 cp01](s08/cp01.md) | 240 | 738 | 33 (+3) | 144/272; carried, age13 | 254/272; carried, age13 | 258/272; carried, age13 | 80/80; carried, age2 | 60/80; carried, age2 | 223; carried, age2 | 16/16; carried, age1 | 11/11; carried, age1 | 1,718,749; carried, age1 | 4.7544×; carried, age1 | 0; carried, age1 | **20–45%, central30%; Δ0 pp** | Four-hour override. New bc02 scope: budget/ordinary tie at2,886 fee/137,310 named units for512 outputs each; cover2,937/157,452, anchor4,608/152,022. gc02 graph fees save6.00% versus anchor with much higher computation. Matroid/group-query and six actual scalar proofs extend capability. No F01 rerun or promotion. |')
t='\n'.join(lines)+'\n';assert [l for l in t.splitlines() if l.startswith('| [') or l.startswith('| **[')][:-1]==oldlines
t+='''
## s08 closing update

The final row is the October13–14 **Codex (GPT-6)** four-hour override, one
recurrence. Exact research is **14,402,318,580,700 ns =240.038643011666666… minutes**;
C001/program **44,251,453,147,247 ns =737.524219120783333… minutes**;
phase **109,419,335,189,096 ns =1823.655586484933333… minutes**.
[Effective actuals](s08/effective_actuals.json) and [checkpoint](s08/cp01.md).

The old272-edit measurement remains October11,23:12:23.271094 UTC, age13;
the80-request duty remains October12,17:03:32.626949 UTC, age2. S28 a03 remains
October12,20:22:24.594133 UTC, age1 (ordinary comparison20:08:46.807687).
They were not rerun. New bc02/gc02 observations are October14,2026, age0, in
separate duties with their declarations, complete-arm denominators, raw source
hashes and failed-prefix accounting in [progress](s08/progress_results.json),
[graph summary](s08/gc02/summary.json) and the JSON comparison scopes.

Within bc02, budget minus greedy-cover is **−51 physical fee, −20,142 named
units**; against ordinary-budget both deltas are zero. These are within-run
comparisons, not improvement on the old F01 duty. Complete economic costs are
unknown. [F01 reassessment](s08/forecast_final.md) stays20–45%, central30%,
change0 points; central gaps50/60 points to80%/90%. New branch events remain
unspecified and unassessed. C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred.
'''
md.write_text(t,encoding='utf-8',newline='\n')
save(here/'pub/recurrence_preservation.json',dict(historical_rows_preserved=doc['rows'][:-1]==old,historical_markdown_rows_preserved=True,rows=19,latest='s08_cp01',research_credit_ns=0))
print('recurrences',len(doc['rows']),'bc02',totals)
