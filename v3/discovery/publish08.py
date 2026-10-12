"""Administrative cp06 active publication; retain raw clocks and all failures."""
import csv,json,subprocess
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
s=Path('v3/discovery/s03');assert not (s/'cp06.md').exists()
segments=[json.loads(l) for l in (s/'segments.jsonl').read_text().splitlines()]
prior_ds=[json.loads(l) for l in (s/'dispositions.jsonl').read_text().splitlines()]
changes={864868159791700:'After the short portfolio result read, most work derived the affine-source and physical-query extensions.',865135827388800:'After the affine result read, most work derived the basis obstruction and rank-dependent query planner.',865431302085400:'After the rank result read, most work derived minimax reports, bounded model reliance and the randomized-policy proof.'}
with (s/'dispositions.jsonl').open('a') as f:
    for start,why in changes.items():
        assert not any(d['segment_start_monotonic_ns']==start for d in prior_ds)
        seg=next(x for x in segments if x['start']['monotonic_ns']==start)
        f.write(json.dumps(dict(segment_start_monotonic_ns=start,segment_end_monotonic_ns=seg['end']['monotonic_ns'],original_mode=seg['effective_mode'],effective_mode='D',elapsed_ns=seg['elapsed_ns'],reason=why+' Dominant-mode correction only; no added research.',purpose='generation',lane='X'))+'\n')
subprocess.run(['python','v3/discovery/reconcile.py',str(s)],check=True)
eff=json.loads((s/'effective_actuals.json').read_text());prior=json.loads(Path('v3/discovery/s02/effective_actuals.json').read_text())
base=json.loads(subprocess.check_output(['git','show','920b717b59c781a6c6126dbbce0e5ab0cccf6bc0:v3/plan.v1.json']))
p=Path('v3/plan.v1.json');plan=json.loads(p.read_text());pr=plan['discovery_program'];cy=pr['current_cycle']
old_minutes=str(Decimal(cy['research_ns'])/Decimal(60_000_000_000));old_phase=str(plan['observed_progress']['research_minutes'])
pr.update(research_ns=eff['program_research_ns'],latest_checkpoint='v3/discovery/s03/cp06.md')
cy.update(research_ns=eff['cycle_research_ns'],remaining_research_floor_ns=0,research_floor_satisfied=True,session_status='active_beyond_floor_sixth_publication_checkpoint')
plan['observed_progress'].update(research_ns=eff['phase_research_ns'],research_minutes=eff['exact_phase_research_minutes'],measured_engaged_ns=base['observed_progress']['measured_engaged_ns']+prior['total_engaged_ns']+eff['total_engaged_ns'],evidence_disposition='C001 continues beyond its fresh floor; sixth s03 active checkpoint. DEVELOPMENT, P3-POS01 outstanding. Report probe failure and one unchanged retry retained.')
p.write_text(json.dumps(plan,indent=2)+'\n')
for name in ('TODO_v3.md','v3/README.md','v3/discovery/P3_SEARCH_01.md'):
    p=Path(name);body=p.read_text(encoding='utf-8').replace('s03/cp05.md','s03/cp06.md').replace(old_minutes,eff['exact_cycle_research_minutes']).replace(old_phase,eff['exact_phase_research_minutes'])
    if name=='TODO_v3.md':body=body.replace(str(Decimal(old_phase)-960),str(Decimal(eff['exact_phase_research_minutes'])-960))
    if name=='v3/discovery/P3_SEARCH_01.md':
        body=body.replace('Current s03 direction: checked parameter families, paid forecast audits and\ndecision-relevant program-edit residuals.','Current s03 direction: exact affine decision services, explicit model/assumption\ntransport and alternative physical query methods.')
        body=body.replace('develop a checked program-edit residual service and paid conditional acquisition, retaining alternatives.','develop graph-based observation acquisition for weighted fact predictions, retaining alternatives.')
    p.write_text(body,encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
with Path('v3/time_ledger.csv').open('a',newline='') as f:csv.writer(f,lineterminator='\n').writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s03','O','',now,now,0,0,0,0,0,0,'v3/discovery/s03/dispositions.jsonl','Zero-credit notice: three dominant-mode corrections to constructive mathematical development; no research added.'])
(s/'cp06.md').write_text(f'''# C001 active checkpoint: exact affine decision services

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.
C001 has **{eff['exact_cycle_research_minutes']} research minutes**, continuing
beyond its satisfied 240-minute floor. [Effective actuals](effective_actuals.json)
retain raw same-runtime observations, additive mode corrections and excluded
interruption gaps. This is an active publication boundary; no cycle or session
is being ended merely because of the floor.

- [Parity portfolios](parity_portfolio.md): exact closure reduction for all
  adaptive policies at the specified query interface; 28 Bellman cases and
  140 expected-budget comparisons. Affine compilation and 48 assumption
  revisions preserve value profiles, with physical-query restrictions explicit.
- [Rank-dependent values and reports](rank_values.md): arbitrary linear queries
  for full-state prediction or minimax logarithmic reporting; 36 planning cases,
  executable guesses and supported fallible forecasts. The report probe's first
  TypeError and one successful unchanged retry are both preserved.
- [Explicit policy transport](affine_transport.md): 32 correlated sources,
  226 paired-world checks, matching recomputed optima and normalized expansions.
  The supplied semantic correspondence is essential; equal values do not infer it.
- [Program-edit residuals](edit_residuals.md): signed receipt polarity and fresh
  conditional-sampling construction; no manufactured full-program benchmark.

[Five-question assessment](synthesis06.md) distinguishes exact restricted
capabilities, standard ingredients, negative boundaries and missing usefulness.
P3-POS01 remains OUTSTANDING, P3-11 deferred, readiness unassessed.

Next: allow alternative physical observations without changing weighted fact
prediction into a different objective. Node observations anchor graph components;
edge parity observations connect them. Derive/check an exact tree acquisition
algorithm and compare ordinary prize-collecting forest methods. Continue C001;
360/480-minute forecasts are not limits. Prior published remote main was
`cf21d0b3e5f3a4d5af8417640b1e668012cfa3e7`.
''',encoding='utf-8')
print(json.dumps({k:eff[k] for k in ['exact_cycle_research_minutes','exact_remaining_floor_minutes','exact_phase_research_minutes']}))
