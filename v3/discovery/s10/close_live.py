"""One-time live handoff synchronization; historical row objects stay unchanged."""
from pathlib import Path
from decimal import Decimal
import copy,hashlib,json,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];D=ROOT/'v3/discovery'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=read(HERE/'effective_actuals.json');x=read(D/'recurrences.json');assert x['rows'][-1]['id']=='s08_cp01'
old=copy.deepcopy(x['rows']);previous=old[-1];row=copy.deepcopy(previous)
row.update(id='s10_cp01',label='s10 two-hour author override',checkpoint='s10/checkpoint.md',session='s10',research_ns=a['research_ns'],cumulative_research_ns=a['program_research_ns'],research_minutes_rounded=120,cumulative_minutes_rounded=858,new_family_ids=['S34','S35'],cumulative_new_family_count=35,metric_summary='sf01 near target: 3584 outputs per arm; scalar/ordinary tie at31010 fee/14586157 named versus full72320/16123044, savings57.12%/9.53%. Fixed18 savings7.37%/1.65%; exact threshold trades fewer fees for more computation. Unit source compilation90.15% cheaper by named counts; six-patch reuse69.61%. F01 unchanged.',description='Cheaper checked source compilation and conditioning, response certificate reuse, scalar prefix service, confidence learning and reserve stress tests, and sharp dependence-robust score bounds. Strong ordinary alternatives and unknown full prices prevent promotion.')
for name,m in row['fixed_metrics'].items():
    if name in ('families_total','confirmation_forecast_percent'):continue
    m.update(measurement_status='carried_forward',age_in_recurrences=m.get('age_in_recurrences',0)+1,carried_in_row='s10_cp01',carried_from_row='s08_cp01',reason='No comparable new acquisition in s10; original dated measurement carried, not a measured zero change.')
row['fixed_metrics']['families_total'].update(observed_in_row='s10_cp01',value=35,previous_comparable_row='s08_cp01',absolute_delta=2,sources=[{'path':'candidates.md','locator':'S34-S35'}])
f=copy.deepcopy(x['current_forecast']);f.update(assessment_id='F01_s10_final',observed_in_row='s10_cp01',assessment_utc='2026-10-14T22:25:05.909460+00:00',previous_comparable_row='s08_cp01',previous_comparable_assessment_id='F01_s08_final',rationale='Constructive source, response and dependence results are different duties. Ordinary mirrors tie, stronger thresholds trade fees against computation, and full prices remain unknown. No new F01 complete-cost evidence.',sources=[{'path':'s10/forecast_final.md','sha256':sha(HERE/'forecast_final.md'),'locator':'Unchanged-event final assessment'}],next_decision='Target cheap source admission/conditioning and conservative score learning on fresh priced services; keep a new event separate from F01.')
row['fixed_metrics']['confirmation_forecast_percent']=f
row['time_evidence']={'actuals':'s10/effective_actuals.json','sha256':sha(HERE/'effective_actuals.json'),'actuals_field':'session_research_ns','cumulative_actuals_field':'cycle_research_ns','dispositions':'s10/dispositions.json','effective_observation':a['observed'],'research_closed_utc':a['research_closed_utc'],'note':'78 closed same-runtime segments, exact conservative exclusions, no s09 or publication credit.'}
sf=read(HERE/'sf01/checked.json');measurements=[]
for stratum,values in sf['strata'].items():
    sid='s33_sf01_'+stratum+'_28x128_v1'
    item={'scope_id':sid,'measurement_date_utc':'2026-10-14','observed_in_row':'s10_cp01','age_in_recurrences':0,'measurement_status':'first measurement','denominator':3584,'source':'s10/sf01/checked.json','sha256':sha(HERE/'sf01/checked.json'),'totals':values,'ordinary_mirror_delta_fee':0,'ordinary_mirror_delta_named':0,'complete_economic_cost':None,'complete_cost_reason':'Named units are implementation counters; host, bit complexity, archive acquisition, storage and native prices remain unknown.'}
    measurements.append(item)
    x['comparison_scopes'][sid]={'stage':'DEVELOPMENT','source_family':'24 SATLIB uf20 and4 uf50 satisfiable formulas; prospectively selected, synthetic latent costs','horizon_per_source':128,'outputs_per_arm':3584,'tolerance':'18' if stratum=='fixed18' else 'max(0, initial robust bound in units minus6), derived prospectively from source','latent_law':'Independent uniform integer ticks0..24000 for each true/false cost, scale6000','fee_rule':'Individual1..3; full bundle ceil(0.75 sum individual fees)','arms':list(values),'source':'s10/sf01/design.json','caps':'50,000 source states; bounded witness pool; prefix listed fee<=fallback C','price_convention':'physical fee + separately reported named semantic units; no complete-cost conversion','observation_date_utc':'2026-10-14'}
row['metric_values']={'metric_type':'New separate-scope development; old S28 and legacy duties carried','scope_id':measurements[1]['scope_id'],'separate_scope_ids':[m['scope_id'] for m in measurements],'new_scope_measurements':measurements}
row['metric_sources']=[{'path':p,'sha256':sha(D/p)} for p in ['s10/sf01/checked.json','s10/component_analysis.json','s10/forecast_final.md']]
x['rows'].append(row);assert x['rows'][:-1]==old
x.update(prepared_by='Codex (GPT-6)',prepared_date_utc='2026-10-14',latest_checkpoint='s10/checkpoint.md',latest_effective_actuals='s10/effective_actuals.json',total_research_ns=a['program_research_ns'],total_research_minutes=a['program_research_minutes'],total_minutes_rounded=858,program_research_ns=a['program_research_ns'],phase_research_ns=a['phase_research_ns'],current_forecast=f,active_scope_id=measurements[1]['scope_id'],active_row_ids=[r['id'] for r in x['rows']],current_separate_scope_ids=[m['scope_id'] for m in measurements])
x['forecast_assessments'].append(f);x['separate_scope_measurements'].extend(measurements)
x['readiness_assessment_history'].append(copy.deepcopy(x['current_readiness_assessment']))
x['current_readiness_assessment'].update(assessment_utc=f['assessment_utc'],basis_checkpoint='s10/checkpoint.md',principal_blocker=f['rationale'],sources=f['sources'])
x['visible_resource_metrics']['s10']={'observation_date_utc':'2026-10-14','age_at_s10':0,'sf01':measurements,'source_compilation':{'sources':39,'unit_named':1390207,'baseline_named':14106926,'scope':'unit propagation vs previous branching compiler; no native speed claim'},'conditioning':{'patches':168,'sources':28,'incremental_including_parent':7031748,'fresh':23141569,'scope':'six patches/source; single-patch benefit only2/28'},'source':'s10/component_analysis.json'}
labels=['Recurrence / recorded boundary','Research min','Cumulative min','Families (Δ)','Resource comparison scope','Audit fees','Counted computation','Ordinary-method comparison','272 edits: transport / broad / targeted','80 requests: outputs / cache / action cost','S28: outputs / plans / quotation / bill ratio','F01: ≥10% full-cost regions','Promotion forecast (80% minimum)','What changed']
fields=['checkpoint','research_minutes_rounded','cumulative_minutes_rounded','families_total','resource_scope','physical_audit_fee','named_computation','ordinary_comparison','legacy272','legacy80','legacyS28','f01_demonstrated_cost_regions','confirmation_forecast_percent','description']
x['rendered_table'].update(row_ids=[r['id'] for r in x['rows']],latest_row_id='s10_cp01',columns=[{'field':f,'label':l} for f,l in zip(fields,labels)])
save(D/'recurrences.json',x)
md=(D/'recurrences.md').read_text(encoding='utf-8').replace('**19 recorded rows, ending\nwith s08**','**20 recorded rows, ending\nwith s10**').replace('738 cumulative research minutes','858 cumulative research minutes')
lines=md.splitlines();last=max(i for i,l in enumerate(lines) if l.startswith('|'))
lines.insert(last+1,'| **[s10 cp01](s10/checkpoint.md)** | **120** | **858** | **35 (+2)** | **sf01:** 3,584 outputs/arm/stratum, 28 sources ×128; Oct14<br>Unit compilation:39 sources; conditioning:168 patches | **Near target:31,010 vs72,320 full audit; −57.12%**<br>Fixed18:66,991 vs72,320; −7.37% | **Near target:14,586,157 vs16,123,044; −9.53%**<br>Fixed18:15,857,399 vs16,123,044; −1.65%<br>Source compilation−90.15%; six-patch reuse−69.61% | **Ordinary scalar prefix ties.** Near target exact threshold:9,657 fees/19,261,900 units; scalar threshold:32,302/14,453,502 | 144/272;254/272;258/272; carried, age14 | 80/80;60/80;223; carried, age3 | 16/16;11/11;1,718,749;4.7544×; carried, age2 | 0; carried, age2 | **20–45%, central30%; Δ0 pp** | Two-hour override. Cheaper checked sources, response/source reuse, paid scalar policy, learning/reserve stress tests and sharp dependence bounds. Setup repayment at28/88 observed requests per source; broad full-cost claim remains open. |')
md='\n'.join(lines)+'\n';md=md.replace('The final row is the October13–14','The historical s08 row is the October13–14')
md+='''
## s10 closing update

The final row is the October14 two-hour override by **Codex (GPT-6)**.
Exact research is **7,204,333,028,000 ns =120.072217133333333… minutes**;
C001/program **51,455,786,175,247 ns =857.596436254116666… minutes**;
phase **116,623,668,217,096 ns =1943.727803618266666… minutes**.
[Checkpoint](s10/checkpoint.md), [actuals](s10/effective_actuals.json),
[findings](s10/findings.md), [exact component analysis](s10/component_analysis.json).

The new sf01 strata have different tolerances from s08 and from F01. These are
first measurements, not measured improvements on those older duties. Fees and
counted computation include each arm's setup and executed checks; unknown full
prices remain unknown. Prior bc02/gc02 values remain visible in their historical
row. The272-edit,80-request andS28 observations are carried at ages14,3,2.
Ordinary equivalent policies tie; exact threshold and scalar threshold expose
fee/computation tradeoffs. The source compiler comparison is against the prior
branching compiler, and conditioning amortizes one parent over six patches.
Neither percentage is native runtime or an economic tariff. [F01](s10/forecast_final.md)
remains20–45%, central30%, change0 points. No candidate is promoted.
'''
(D/'recurrences.md').write_text(md,encoding='utf-8')
plan=read(ROOT/'v3/plan.v1.json');plan['active_session']=None
for key in ['last_completed_session','last_preserved_session','last_discovery_session']:plan[key]='v3/discovery/s10/session.md'
plan['observed_progress'].update(research_ns=a['phase_research_ns'],source='v3/discovery/s10/effective_actuals.json',research_minutes=a['phase_research_minutes'],evidence_disposition='s10 explicit two-hour increment closed after exact exclusions; source, response, policy and dependence work remains DEVELOPMENT. No s09 or publication credit.')
recommend='Continue from s10 using v3/discovery/CONTINUE.md for the explicitly requested duration, default60 minutes. Test priced source changes and cheap dependence-robust score learning against strong ordinary methods. C001 OPEN; F01 20-45%, central30%; P3-11 deferred.'
plan['optional_recurrence_advice']['current_recommendation']=recommend
p=plan['discovery_program'];p.update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],latest_checkpoint='v3/discovery/s10/checkpoint.md',actuals='v3/discovery/s10/effective_actuals.json')
p['sessions'].append('v3/discovery/s10/session.md');p['promotion']['assessment']='v3/discovery/s10/forecast_final.md'
p['current_cycle'].update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],session='v3/discovery/s10/session.md',actuals='v3/discovery/s10/effective_actuals.json',session_status=a['status'],clock_active=False)
p['execution_cadence'].update(last_closed_session='s10',last_increment_research_ns=a['research_ns'],last_increment_research_minutes=a['research_minutes'],last_session_target_minutes=120,last_override_authority='v3/decisions/2026-10-14_two_hour_metrics.md')
save(ROOT/'v3/plan.v1.json',plan)
todo=(ROOT/'TODO_v3.md').read_text(encoding='utf-8');todo=todo.replace('737.524219120783','857.596436254117').replace('1823.655586484933','1943.727803618267').replace('863.655586484933','983.727803618267').replace('from [s08](v3/discovery/s08/cp01.md)','from [s10](v3/discovery/s10/checkpoint.md)')
start=todo.index('## Current author selection');end=todo.index('## Previous author selection',start)
todo=todo[:start]+'''## Current author selection — October14,2026

**P3-SEARCH-01-C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred.** The
[two-hour override](v3/decisions/2026-10-14_two_hour_metrics.md) is complete.
Codex (GPT-6) adds **120.072217133333333… engaged research minutes**;
program/C001 is **857.596436254116666…** and phase **1943.727803618266666…**.
Exact session/program/phase nanoseconds are7,204,333,028,000 /
51,455,786,175,247 /116,623,668,217,096. The clock is closed. Default next
duration remains60 minutes, subject to an explicit author override.

Read [s10 checkpoint](v3/discovery/s10/checkpoint.md),
[findings](v3/discovery/s10/findings.md), [actuals](v3/discovery/s10/effective_actuals.json),
[portfolio](v3/discovery/candidates.md), [recurrence table](v3/discovery/recurrences.md)
and [continuation prompt](v3/discovery/CONTINUE.md). Recovery, context gaps,
installation and publication do not earn research credit. s09 is reserved for
the separate remote transfer branch; no scientific time is assumed from it.

The28-source near-target scalar service reduces recorded audit fees57.12% and
counted computation9.53% versus full audit; its ordinary equivalent ties.
Fixed18 yields7.37%/1.65%; stronger threshold methods expose real tradeoffs.
Checked unit propagation reduces the previous compiler's counted work90.15%,
and six-patch source reuse reduces it69.61% with initial setup included.
These are DEVELOPMENT component comparisons with unknown full prices.

**35 families record breadth, not readiness.** S34 checked source compilation
and S35 response-certificate reuse join the portfolio. Confidence learning,
physical reserves and a sharp three-score dependence bound extend existing
branches. The [same F01](v3/discovery/s10/forecast_final.md) remains20–45%,
central30%, change0 points. No candidate is promoted. Next test cheap checked
source changes and conservative score learning on fresh, priced services with
strong ordinary controls. P3-N01 keeps its historical modest support; P3-C/D
remain unattempted. Elapsed floors do not close the discovery program.

'''+todo[end:]
(ROOT/'TODO_v3.md').write_text(todo,encoding='utf-8')
for filename,heading in [('candidates.md','IDs S01 onward'),('P3_SEARCH_01.md','## 1. Objective')]:
    p=D/filename;text=p.read_text(encoding='utf-8');start=text.index('**Current continuation') if filename=='candidates.md' else text.index('Latest execution contributor:');end=text.index(heading,start)
    text=text[:start]+'''**Current continuation — October14,2026, Codex (GPT-6):**
[s10 checkpoint](s10/checkpoint.md), [findings](s10/findings.md),
[exact actuals](s10/effective_actuals.json), [single recurrence table](recurrences.md).
The two-hour increment adds120.072217133333333… research minutes;
C001/program is857.596436254116666… and phase1943.727803618266666….
All clocks are closed. Default next session60 minutes, explicit overrides allowed.

**C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred; no candidate promoted.**
[F01](s10/forecast_final.md) remains20–45%, central30%, change0 points since s08.
The35 families measure breadth. Cheaper source compilation and conditioning,
response-certificate reuse, scalar policies and dependence-robust score bounds
are DEVELOPMENT. Ordinary equivalents tie; threshold controls and broader
negative transfers limit the resource claims. Use [CONTINUE](CONTINUE.md) for
the next priced construction and recover remote state before starting a clock.
Earlier dated sections below retain their historical scope.

'''+text[end:]
    p.write_text(text,encoding='utf-8')
with (D/'candidates.md').open('a',encoding='utf-8') as out:out.write('''
## s10 constructive update — October14,2026, Codex (GPT-6)

| ID | Mechanism and lineage | Useful comparison | Evidence and obstacle | Disposition |
|---|---|---|---|---|
| S34 | Checked unit-propagated source diagrams, signed objectives and hard-source conditioning; extends S09/S19/S33. | Reuse source-complete computations across objectives and constraint changes; compare fresh compilation and persistent native solving. |39-source predecessor comparison−90.15% named work;168 patches−69.61% at six-patch horizon; native prices unknown and one-patch setup often loses. [Findings](s10/findings.md), [conditioning](s10/source_patches.md). | DEVELOPMENT |
| S35 | Positive affine response covers, negative witness regions and response neighborhoods; extends S29/S30/S33. | Reuse proofs over ranges of observations instead of exact-value cache hits; compare ordinary local and threshold methods. | Broader wt02 saves under1% fees with over5× full-audit computation. Scalar scores are cheaper; ordinary counterparts tie. [Findings](s10/findings.md). | DEVELOPMENT |

S31 learning now has actual receipt-based confidence policies and wrong-law
stress tests. S33 gains a sharp three-score marginal bound and a proposed
dependence-robust learning composition. These are extensions, not extra family
counts. [Assessment](s10/scientific_assessment.md) separates useful capability,
unknown full-cost benefit and unchanged confirmation readiness.
''')
with (ROOT/'v3/claim_ledger.md').open('a',encoding='utf-8') as out:out.write('''
## s10 additive discovery update — October14,2026, Codex (GPT-6)

All new findings are DEVELOPMENT and same-model reviewed. Prior dated claims
retain their scope. [Checkpoint](discovery/s10/checkpoint.md), [findings](discovery/s10/findings.md).

| ID | Supported scoped statement | Evidence and limits |
|---|---|---|
| DS-S34 | Checked source compilation and exact unit conditioning reduce repeated source work on the declared finite sources. |39-source prior-compiler named reduction90.15%;168 patches69.61% with parent admission. Ordinary SAT/compilation mechanisms; no native-runtime or general tractability claim. |
| DS-S35 | Affine positive and witness-negative regions support checked response reuse beyond exact-value matches. |Broader transfer remains costly; no general economic benefit. All ordinary mirrors tie. |
| S10-SCALAR |28-source near-target scalar prefix reduces audit fees57.12% and counted work9.53% against full audit on3,584 outputs per arm. |Fixed18 gives7.37%/1.65%; exact threshold uses fewer fees but more computation; ordinary scalar implementation ties. Unknown complete prices. |
| S10-DEPENDENCE |Three elementary bounds give the sharp worst prefix survival for identical three-valued score marginals with arbitrary dependence. |[Proof](discovery/s10/three_score_sharp.md),47,520 exact allocation checks. Individual-prefix sharpness does not make the summed invoice jointly sharp; robust service benefit not yet measured. |
| S10-LEARNING |Confidence policies and a pathwise physical-fee reserve have distinct premises and guarantees. |[Learning interpretation](discovery/s10/learning_interpretation.md), [reserve](discovery/s10/fee_reserve.md).36 changed-law confidence violations retained; no best-policy regret rate or full-cost guarantee. |
| Current P3-POS01 / Q3 |OUTSTANDING / affirmative strongest-ordinary advantage OPEN. |F01 remains20–45%, central30%, Δ0; P3-11 deferred; no promotion. |
''')
protocol=ROOT/'v3/RESEARCH_PROTOCOL.md';text=protocol.read_text(encoding='utf-8');text=text.replace('is one such override. It does not change the default for later sessions.','and the [October14 two-hour instruction](decisions/2026-10-14_two_hour_metrics.md)\nare such overrides. They do not change the default for later sessions.');protocol.write_text(text,encoding='utf-8')
save(HERE/'live_sync.json',{'contributor':'Codex (GPT-6)','research_credit_ns':0,'historical_rows_preserved':len(old),'canonical_historical_rows_sha256':hashlib.sha256(json.dumps(old,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'new_row':'s10_cp01','research_ns':a['research_ns'],'note':'One-time synchronization; do not rerun against a table already ending in s10.'})
print('Synchronized live pointers and20-row table; preserved19 historical row objects.')
