"""Administrative cp07 publication; no research credit for this script."""
import csv,json,subprocess
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
s=Path('v3/discovery/s03');assert not (s/'cp07.md').exists()
segments=[json.loads(l) for l in (s/'segments.jsonl').read_text().splitlines()]
prior_ds=[json.loads(l) for l in (s/'dispositions.jsonl').read_text().splitlines()]
changes={
 867507710936100:('D','generation','X','After the short primary restart-law read, most work derived latent-mixture stopping and the capped numeric planner.'),
 867604559063100:('E','generation','X','Most work implemented the capped-tree prototype, composed before its next boundary mark.'),
 869926075040800:('unmeasured','recovery','-','Conservatively exclude the mixed publication/compaction/recovery interval from total engaged; already zero research.')}
with (s/'dispositions.jsonl').open('a') as f:
 for start,(mode,purpose,lane,reason) in changes.items():
  assert not any(d['segment_start_monotonic_ns']==start for d in prior_ds)
  seg=next(x for x in segments if x['start']['monotonic_ns']==start)
  f.write(json.dumps(dict(segment_start_monotonic_ns=start,segment_end_monotonic_ns=seg['end']['monotonic_ns'],original_mode=seg['effective_mode'],effective_mode=mode,elapsed_ns=seg['elapsed_ns'],reason=reason+' No research added.',purpose=purpose,lane=lane))+'\n')
subprocess.run(['python','v3/discovery/reconcile.py',str(s)],check=True)
eff=json.loads((s/'effective_actuals.json').read_text());prior=json.loads(Path('v3/discovery/s02/effective_actuals.json').read_text())
base=json.loads(subprocess.check_output(['git','show','920b717b59c781a6c6126dbbce0e5ab0cccf6bc0:v3/plan.v1.json']))
p=Path('v3/plan.v1.json');plan=json.loads(p.read_text());pr=plan['discovery_program'];cy=pr['current_cycle']
old_minutes=str(Decimal(cy['research_ns'])/Decimal(60_000_000_000));old_phase=str(plan['observed_progress']['research_minutes'])
pr.update(research_ns=eff['program_research_ns'],latest_checkpoint='v3/discovery/s03/cp07.md')
cy.update(research_ns=eff['cycle_research_ns'],remaining_research_floor_ns=0,research_floor_satisfied=True,session_status='active_beyond_floor_seventh_publication_checkpoint')
plan['observed_progress'].update(research_ns=eff['phase_research_ns'],research_minutes=eff['exact_phase_research_minutes'],measured_engaged_ns=base['observed_progress']['measured_engaged_ns']+prior['total_engaged_ns']+eff['total_engaged_ns'],evidence_disposition='C001 active beyond fresh floor; seventh s03 checkpoint. DEVELOPMENT, P3-POS01 outstanding. Graph native failure and failed unchanged retry retained; Node amendment source-bound. Disconnected intervals excluded.')
p.write_text(json.dumps(plan,indent=2)+'\n')
for name in ('TODO_v3.md','v3/README.md','v3/discovery/P3_SEARCH_01.md'):
 p=Path(name);body=p.read_text(encoding='utf-8').replace('s03/cp06.md','s03/cp07.md').replace(old_minutes,eff['exact_cycle_research_minutes']).replace(old_phase,eff['exact_phase_research_minutes'])
 if name=='TODO_v3.md':body=body.replace(str(Decimal(old_phase)-960),str(Decimal(eff['exact_phase_research_minutes'])-960))
 if name=='v3/discovery/P3_SEARCH_01.md':
  body=body.replace('Current s03 direction: exact affine decision services, explicit model/assumption\ntransport and alternative physical query methods.','Current s03 direction: graph observation policies, capped/failed computations\nand learning decision values from incomplete execution.')
  body=body.replace('develop graph-based observation acquisition for weighted fact predictions, retaining alternatives.','develop censoring-safe learning of cutoff-policy values, retaining alternatives.')
 p.write_text(body,encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
with Path('v3/time_ledger.csv').open('a',newline='') as f:csv.writer(f,lineterminator='\n').writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s03','O','',now,now,0,0,0,0,0,0,'v3/discovery/s03/dispositions.jsonl','Zero-credit notice: two dominant-mode corrections and excluded mixed compaction/recovery interval. Two >15-minute disconnected gaps already excluded by raw cadence rule.'])
(s/'cp07.md').write_text(f'''# C001 active checkpoint: failed computations and retry values

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.
C001 has **{eff['exact_cycle_research_minutes']} research minutes**, with zero
remaining to its fresh 240-minute floor. It continues beyond that floor;
360/480-minute forecasts are estimates, not stopping conditions. The exact
[effective actuals](effective_actuals.json) preserve raw observations and
exclude disconnected/compaction intervals without resetting the commitment.

- [Graph acquisition](graph_values.md): alternative physical node/parity
  observations reduce to ordinary prize-collecting trees; an exact physical-tree
  planner matched 6,216 subsets, 744 world scores and 12 Bellman cases.
  Its first Python run and single unchanged retry both failed; the explicit
  [Node amendment](graph_amend.md) preserves original inputs and both failures.
- [Failed/capped queries](failed_queries.md): success-conditioned policies can
  beat fixed batches. Conditional per-history success bounds give a robust
  lower planner; capped single-anchor tree policies admit linear all-root
  planning with certified grid error. Thirty-two small trees / 3,148 rooted
  choices and three 4,096-node kernels were checked with supplied bounds.
- [Retry models](retry_models.md): pooled success rates do not warrant geometric
  retry prices. Latent-mixture hazards decrease after failure; bounded cutoff
  values retain decision-relevant survival information. Twenty-four exact
  mixtures support the stated identities and stopping rule.

[Five-question synthesis](synthesis07.md) separates these capabilities from
model learning and material usefulness. P3-POS01 remains OUTSTANDING; P3-11
is deferred. No confirmation promotion or readiness percentage is assigned.

Next constructive move: [censoring-safe value learning](censored_values.md).
Develop same-prefix counterfactual receipts and prediction-assisted nested
random-truncation estimators; derive their tail-residual variance and priced
allocation, compare established random-truncation methods, then use a small
exact screen. Supplied probability bounds must not masquerade as learned ones.
Prior published main: `7ddab2cc2d53551443611ffa54126decf4ef341e`.
This publication boundary does not close the session or discovery cycle.
''',encoding='utf-8')
print(json.dumps({k:eff[k] for k in ['exact_cycle_research_minutes','exact_remaining_floor_minutes','exact_phase_research_minutes']}))
