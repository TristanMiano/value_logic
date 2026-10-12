"""Administrative active checkpoint cp05; no added research or cycle reset."""
import csv,json,subprocess
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
s=Path('v3/discovery/s03');assert not (s/'cp05.md').exists()
segments=[json.loads(l) for l in (s/'segments.jsonl').read_text().splitlines()]
prior_ds=[json.loads(l) for l in (s/'dispositions.jsonl').read_text().splitlines()]
changes={863915426378800:'After reading the primary corrected-factor theorem, the dominant work derived lower-proof and delayed-refinement extensions and drafted their mathematics.',864134048628500:'After the short exact/synthetic result read, most work derived fallback significance costs and the distinction between forecast and target adaptation.'}
with (s/'dispositions.jsonl').open('a') as f:
    for start,why in changes.items():
        assert not any(d['segment_start_monotonic_ns']==start for d in prior_ds)
        seg=next(x for x in segments if x['start']['monotonic_ns']==start)
        f.write(json.dumps(dict(segment_start_monotonic_ns=start,segment_end_monotonic_ns=seg['end']['monotonic_ns'],original_mode=seg['effective_mode'],effective_mode='D',elapsed_ns=seg['elapsed_ns'],reason=why+' Dominant-mode correction only; no added research.',purpose='generation',lane='X'))+'\n')
subprocess.run(['python','v3/discovery/reconcile.py',str(s)],check=True)
eff=json.loads((s/'effective_actuals.json').read_text());prior=json.loads(Path('v3/discovery/s02/effective_actuals.json').read_text())
base=json.loads(subprocess.check_output(['git','show','920b717b59c781a6c6126dbbce0e5ab0cccf6bc0:v3/plan.v1.json']))
p=Path('v3/plan.v1.json');plan=json.loads(p.read_text());pr=plan['discovery_program'];cy=pr['current_cycle']
old_minutes=str(Decimal(cy['research_ns'])/Decimal(60_000_000_000));old_remaining=str(Decimal(cy['remaining_research_floor_ns'])/Decimal(60_000_000_000));old_phase=str(plan['observed_progress']['research_minutes'])
assert eff['cycle_research_ns']>=cy['research_floor_ns']
pr.update(research_ns=eff['program_research_ns'],latest_checkpoint='v3/discovery/s03/cp05.md')
cy.update(research_ns=eff['cycle_research_ns'],remaining_research_floor_ns=0,research_floor_satisfied=True,session_status='active_beyond_floor_fifth_publication_checkpoint')
plan['observed_progress'].update(research_ns=eff['phase_research_ns'],research_minutes=eff['exact_phase_research_minutes'],measured_engaged_ns=base['observed_progress']['measured_engaged_ns']+prior['total_engaged_ns']+eff['total_engaged_ns'],evidence_disposition='C001 active beyond its actual fresh floor; fifth s03 publication checkpoint. DEVELOPMENT, material objective outstanding. No credit from publication, waits or excluded recovery.')
p.write_text(json.dumps(plan,indent=2)+'\n')
for name in ('TODO_v3.md','v3/README.md','v3/discovery/P3_SEARCH_01.md'):
    p=Path(name);body=p.read_text(encoding='utf-8').replace('s03/cp04.md','s03/cp05.md')
    body=body.replace(old_minutes,eff['exact_cycle_research_minutes']).replace(old_remaining,'0').replace(old_phase,eff['exact_phase_research_minutes'])
    body=body.replace('C001 unfinished','C001 continuing beyond its satisfied floor')
    body=body.replace('its four-hour commitment remains\nunfinished','its four-hour floor is satisfied and work continues')
    body=body.replace('its fresh Research240 floor remains unfinished','its fresh Research240 floor is satisfied and research continues')
    body=body.replace('C001 continues with its unfinished floor','C001 continues beyond its satisfied floor')
    body=body.replace('P3-SEARCH-01-C001; in progress, unfinished','P3-SEARCH-01-C001; active beyond its satisfied floor')
    body=body.replace('resume its unfinished C001 commitment','continue C001 beyond its now-satisfied floor')
    if name=='TODO_v3.md':body=body.replace(str(Decimal(old_phase)-960),str(Decimal(eff['exact_phase_research_minutes'])-960))
    if name=='v3/discovery/P3_SEARCH_01.md':
        body=body.replace('Current s03 direction: stateful counterfactual probes, continuation-aware value\nrepresentations and sharp marginal-value certificates.','Current s03 direction: checked parameter families, paid forecast audits and\ndecision-relevant program-edit residuals.')
        body=body.replace('develop informative extensions and paid acquisition for the value representation, retaining alternatives.','develop a checked program-edit residual service and paid conditional acquisition, retaining alternatives.')
    p.write_text(body,encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
with Path('v3/time_ledger.csv').open('a',newline='') as f:csv.writer(f,lineterminator='\n').writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s03','O','',now,now,0,0,0,0,0,0,'v3/discovery/s03/dispositions.jsonl','Zero-credit notice: two dominant-mode corrections to mathematical generation; no research added.'])
(s/'cp05.md').write_text(f'''# C001 active checkpoint: price families and audited model revisions

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.
C001 has **{eff['exact_cycle_research_minutes']} research minutes**. Its fresh
240-minute floor is satisfied, with exact recorded overshoot and no historical
surplus, publication, waits or interruption gaps credited. [Effective actuals](effective_actuals.json)
preserve raw observations and additive dispositions. C001 remains active;
this publication checkpoint does not end the session or start another clock.

- [Flow advice](flow_results.md) and [per-query retention](flow_retention.md)
  preserve negative comparisons. A box-family certificate amortizes well on
  its supplied 96-query zero-value workload.
- [Exact price profiles](price_profiles.md) answer changing acquisition-bound
  queries with endpoint certificates. Two supplied 128-query workloads cost
  85/118 ms including setup/checks versus 273/255 ms for cold recomputation.
  Ordinary parametric flow is the stronger relevant comparison, not displaced.
- [Model mixtures](model_mixture.md) need an explicit model-identification
  value term. [Prior robustness](prior_robustness.md) and [weight roles](weight_roles.md)
  preserve the independence, semantics and conditional-selection boundaries.
- [Paid forecast audits](audit_bets.md) specialize known prediction-powered
  e-values to checked lower program values and delayed refinement. Exact
  small checks pass; the synthetic tariff screen includes gains and severe losses.

[Five-question assessment](synthesis05.md) states the constructive next move:
develop program edits with cheaply checked unaffected contexts, then estimate
only their decision-relevant residual under paid conditional sampling. Keep
ordinary incremental evaluation and prediction-powered inference as controls.
P3-POS01 remains OUTSTANDING, P3-11 deferred, readiness unassessed. The
360/480-minute central/high C001 forecasts remain estimates, not stop times.
Prior publication `361f8e3e0e70624322c1ddf68e7481c5fa46aa1f` was verified remote.
''',encoding='utf-8')
print(json.dumps({k:eff[k] for k in ['exact_cycle_research_minutes','exact_remaining_floor_minutes','exact_phase_research_minutes']}))
