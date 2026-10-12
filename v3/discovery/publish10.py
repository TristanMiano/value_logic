"""Administrative cp08 publication; retain clocks and development failures."""
import csv,json,subprocess
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
s=Path('v3/discovery/s03');assert not (s/'cp08.md').exists()
segments=[json.loads(l) for l in (s/'segments.jsonl').read_text().splitlines()]
old_ds=[json.loads(l) for l in (s/'dispositions.jsonl').read_text().splitlines()]
changes={870463097663000:'After the short amended result read, most work derived endpoint-design KKT conditions.',870568675828900:'After the short diagnostic run, most work derived two-level allocation and its exact-budget repair.',870990446374200:'After the short profile result read, most work derived local observation/revision and optimality-certificate conditions.'}
with (s/'dispositions.jsonl').open('a') as f:
 for start,why in changes.items():
  assert not any(d['segment_start_monotonic_ns']==start for d in old_ds)
  seg=next(x for x in segments if x['start']['monotonic_ns']==start)
  f.write(json.dumps(dict(segment_start_monotonic_ns=start,segment_end_monotonic_ns=seg['end']['monotonic_ns'],original_mode=seg['effective_mode'],effective_mode='D',elapsed_ns=seg['elapsed_ns'],reason=why+' Dominant-mode correction; no added research.',purpose='generation',lane='X'))+'\n')
subprocess.run(['python','v3/discovery/reconcile.py',str(s)],check=True)
eff=json.loads((s/'effective_actuals.json').read_text());prior=json.loads(Path('v3/discovery/s02/effective_actuals.json').read_text())
base=json.loads(subprocess.check_output(['git','show','920b717b59c781a6c6126dbbce0e5ab0cccf6bc0:v3/plan.v1.json']))
p=Path('v3/plan.v1.json');plan=json.loads(p.read_text());pr=plan['discovery_program'];cy=pr['current_cycle']
old_minutes=str(Decimal(cy['research_ns'])/Decimal(60_000_000_000));old_phase=str(plan['observed_progress']['research_minutes'])
pr.update(research_ns=eff['program_research_ns'],latest_checkpoint='v3/discovery/s03/cp08.md')
cy.update(research_ns=eff['cycle_research_ns'],remaining_research_floor_ns=0,research_floor_satisfied=True,session_status='active_beyond_floor_eighth_publication_checkpoint')
plan['observed_progress'].update(research_ns=eff['phase_research_ns'],research_minutes=eff['exact_phase_research_minutes'],measured_engaged_ns=base['observed_progress']['measured_engaged_ns']+prior['total_engaged_ns']+eff['total_engaged_ns'],evidence_disposition='C001 active beyond floor; eighth s03 checkpoint. DEVELOPMENT, P3-POS01 outstanding. Censor serialization and hinge comparison failures retained with source-versioned repairs; no readiness promotion.')
p.write_text(json.dumps(plan,indent=2)+'\n')
for name in ('TODO_v3.md','v3/README.md','v3/discovery/P3_SEARCH_01.md'):
 p=Path(name);body=p.read_text(encoding='utf-8').replace('s03/cp07.md','s03/cp08.md').replace(old_minutes,eff['exact_cycle_research_minutes']).replace(old_phase,eff['exact_phase_research_minutes'])
 if name=='TODO_v3.md':body=body.replace(str(Decimal(old_phase)-960),str(Decimal(eff['exact_phase_research_minutes'])-960))
 if name=='v3/discovery/P3_SEARCH_01.md':
  body=body.replace('Current s03 direction: graph observation policies, capped/failed computations\nand learning decision values from incomplete execution.','Current s03 direction: compact profiles for graded or marginally calibrated\nforecasts, and paid calibration of their reusable premises.')
  body=body.replace('develop censoring-safe learning of cutoff-policy values, retaining alternatives.','develop paid marginal calibration versus direct policy audits, retaining alternatives.')
 p.write_text(body,encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
with Path('v3/time_ledger.csv').open('a',newline='') as f:csv.writer(f,lineterminator='\n').writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s03','O','',now,now,0,0,0,0,0,0,'v3/discovery/s03/dispositions.jsonl','Zero-credit notice: three dominant-mode corrections after short computational result reads. No research added.'])
(s/'cp08.md').write_text(f'''# C001 active checkpoint: compact calibrated-value profiles

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.
C001 has **{eff['exact_cycle_research_minutes']} research minutes**, continuing
beyond its satisfied fresh 240-minute floor. Exact [effective actuals](effective_actuals.json)
preserve raw clocks, excluded gaps and additive mode corrections. The 360/480
forecasts are not limits; this checkpoint does not end the active cycle.

- [Censored values](censored_values.md): exact tail-residual variance and
  prediction-assisted cap contrasts. Arbitrary nested designs lose 65/72
  matched-work comparisons. The two-level repair's oracle gain averages only
  about 0.6% before overhead, so a larger optimizer is deprioritized.
- [Biased tree profiles](biased_tree.md): an exact profile has at most one
  internal knot per descendant edge. 19,432 subsets, 579 requests and 5,685
  full-belief states agree. Reused values/plans have explicit preparation costs.
- [Marginal robust profiles](robust_tree.md): a different compact DP optimizes
  a conservative guarantee without edge independence. 17,792 subsets, 724
  requests and 760 dependent-source score checks agree. An explicit correlated
  example exposes the product assumption. A common marginal event can support
  later signs, query plans and stakes under its fixed-source scope.

The censoring output serialization bug and marginal probe's wrong evaluator
call are preserved with explicit same-input repairs, not erased or counted as
independent confirmations. [Five-question assessment](synthesis08.md) keeps
these developmental capabilities separate from material usefulness.
P3-POS01 OUTSTANDING; P3-11 deferred; readiness unassessed.

Next: price the acquisition of reusable marginal calibration certificates
against direct evaluation of a prospectively fixed small policy bank. Preserve
timeouts, source identities and source-level versus instance-level meanings.
Continue C001 through this publication boundary. Prior published main was
`246637633c8d8014825f209d810e674c7a948b0f`.
''',encoding='utf-8')
print(json.dumps({k:eff[k] for k in ['exact_cycle_research_minutes','exact_phase_research_minutes']}))
