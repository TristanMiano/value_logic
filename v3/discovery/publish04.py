"""One-time s03 checkpoint 2 publication. O only; raw clocks preserved."""
import csv,json,re,subprocess
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path

root=Path('v3/discovery/s03');assert not (root/'cp02.md').exists()
segments=[json.loads(l) for l in (root/'segments.jsonl').read_text().splitlines()]
corrections={
    854973069274800:('D','The mixed implementation interval chiefly developed the heterogeneous service plan and its paid information/cost boundaries.'),
    855397581653700:('D','The interval chiefly interpreted the native failure and derived the stronger ordinary allocation control, before coding it.'),
    857425753305000:('D','After reading the retrieved primary theorem, the dominant work wrote the continuation/preservation derivation; the mode switch was delayed until the tool boundary.'),
    857880284170600:('D','No implementation occurred in this interval: mathematical development expanded to error cancellation and sharp box-regret certificates before code was drafted.')}
existing=[json.loads(l) for l in (root/'dispositions.jsonl').read_text().splitlines()]
with (root/'dispositions.jsonl').open('a',encoding='utf-8') as f:
    for a,(mode,reason) in corrections.items():
        assert not any(d['segment_start_monotonic_ns']==a for d in existing)
        s=next(s for s in segments if s['start']['monotonic_ns']==a)
        f.write(json.dumps(dict(segment_start_monotonic_ns=a,segment_end_monotonic_ns=s['end']['monotonic_ns'],
            original_mode=s['effective_mode'],effective_mode=mode,purpose='generation',lane='X',elapsed_ns=s['elapsed_ns'],reason=reason+' No added time.'))+'\n')
subprocess.run(['python','v3/discovery/reconcile.py',str(root)],check=True)
eff=json.loads((root/'effective_actuals.json').read_text());prior=json.loads(Path('v3/discovery/s02/effective_actuals.json').read_text())
base=json.loads(subprocess.check_output(['git','show','920b717b59c781a6c6126dbbce0e5ab0cccf6bc0:v3/plan.v1.json']))
p=Path('v3/plan.v1.json');plan=json.loads(p.read_text());pr=plan['discovery_program'];c=pr['current_cycle']
old_cycle=str(Decimal(c['research_ns'])/Decimal(60_000_000_000));old_remaining=str(Decimal(c['remaining_research_floor_ns'])/Decimal(60_000_000_000))
old_phase=str(plan['observed_progress']['research_minutes'])
pr.update(research_ns=eff['program_research_ns'],latest_checkpoint='v3/discovery/s03/cp02.md')
c.update(research_ns=eff['cycle_research_ns'],remaining_research_floor_ns=eff['remaining_floor_ns'],clock_active=True,session_status='active_second_publication_checkpoint')
plan['active_session']=c['session']
plan['observed_progress'].update(research_ns=eff['phase_research_ns'],research_minutes=eff['exact_phase_research_minutes'],source=pr['actuals'],
    measured_engaged_ns=base['observed_progress']['measured_engaged_ns']+prior['total_engaged_ns']+eff['total_engaged_ns'])
plan['observed_progress']['evidence_disposition']='C001 active; s03 second publication checkpoint. DEVELOPMENT, P3-POS01 outstanding, readiness unassessed. Closed effective intervals only; disconnected gap excluded.'
p.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
for name in ('TODO_v3.md','v3/README.md','v3/discovery/P3_SEARCH_01.md'):
    p=Path(name);s=p.read_text(encoding='utf-8').replace('s03/cp01.md','s03/cp02.md')
    s=s.replace(old_cycle,eff['exact_cycle_research_minutes']).replace(old_remaining,eff['exact_remaining_floor_minutes']).replace(old_phase,eff['exact_phase_research_minutes'])
    if name=='TODO_v3.md':s=s.replace('226.01994934415',str(Decimal(eff['exact_phase_research_minutes'])-960))
    if name.endswith('P3_SEARCH_01.md'):
        s=s.replace('Current s02 direction: persistent value margins and targeted positive-proof\nrepair under explicit local edits, with reusable censored count confidence.\nPaid pilot selection narrowed the computation-scheduling lead.','Current s03 direction: stateful counterfactual probes, continuation-aware value\nrepresentations and sharp marginal-value certificates. The heterogeneous proof\nservice narrowed the joint-controller economic lead; preserve all outcomes.')
        s=re.sub(r'\| Research already credited \|.*?\|',f"| Research already credited | {eff['exact_cycle_research_minutes']} minutes at active s03 checkpoint; continuation proceeds |",s)
        s=s.replace('20.598738101667',eff['exact_cycle_research_minutes']).replace('219.401261898333',eff['exact_remaining_floor_minutes'])
        s=s.replace('[the saved checkpoint](s01/checkpoint.md):\ndevelop the coupled policy-cost comparison and its application while retaining alternatives.','[the saved checkpoint](s03/cp02.md):\ndevelop informative extensions and paid acquisition for the value representation, retaining alternatives.')
    p.write_text(s,encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
with Path('v3/time_ledger.csv').open('a',encoding='utf-8',newline='') as f:
    csv.writer(f,lineterminator='\n').writerow(['P3-SEARCH-01','P3-SEARCH-01-C001','s03','O','',now,now,0,0,0,0,0,0,
        'v3/discovery/s03/dispositions.jsonl','Zero-credit correction notice: one additional whole mixed retrieval/input interval excluded; four dominant-mode corrections. Disconnected 1082091166200 ns gap already unmeasured.'])
(root/'recovery04.json').write_text(json.dumps({'status':'resumed_existing_runtime','contributor':'Codex (GPT-6)',
    'reported_failure':'Remote compact task stream disconnected before completion','reported_request_id':'b71a769c-5a0f-4e39-839a-52b290df27f6',
    'last_pre_gap_boundary_utc':'2026-10-12T00:06:45.056480+00:00','resume_observed_utc':'2026-10-12T00:24:47.147640+00:00',
    'runtime':eff['observed']['runtime'],'unobserved_gap_ns':1082091166200,'gap_research_credit_ns':0,
    'additional_excluded_interval_ns':74683854600,'new_clock_started':False,
    'experiment_disposition':'hetero02 completed during the gap; native resource time remains recorded separately and earns no principal research credit'},indent=2)+'\n',encoding='utf-8')
(root/'cp02.md').write_text(f'''# C001 active checkpoint: stateful probes and value baselines

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.
P3-POS01 OUTSTANDING; P3-11 deferred. C001 has **{eff['exact_cycle_research_minutes']}
research minutes**, with **{eff['exact_remaining_floor_minutes']} minutes** still
owed to its fresh 240-minute floor. [Exact closed actuals](effective_actuals.json)
exclude waits, publication and the disconnected interval. This is an active
checkpoint; the existing s03 clock remains live and continuation is authorized.

## Scientific work and constructive progress

- Delayed checked proofs can refine the original sampled factors without
  counting another draw. Small domination/refinement checks passed.
  [Construction](delayed_proofs.md).
- The heterogeneous service completed on an explicitly changed engine after
  a preserved native fault. A strong conventional allocation wins cohort A;
  the sole B finisher uses enough hard proofs to need no statistical warrant.
  No incremental joint economic benefit is established. [Outcomes](service_results.md).
- Actual mutable predictors expose the error in treating state-changing probes
  as pure information. A broader two-probe menu supports beneficial cache
  preparation. Exact ordinary belief control reproduces the policies.
  [Counterfactual example](stateful_cf.md), [continuation quotient](continuation.md).
- A fixed-reference value representation needs m+1 features in the Boolean-flip
  family; per-model minimum-cost normalization needs 2^(m−1)+m to preserve its
  transformed values. A reconstructable Walsh argument and odd m<=11 checks
  support this design consequence. A sorting-based exact regret certificate
  handles a proposed intervention plan given warranted marginal bounds.
  [Derivation and finite outcomes](linear_values.md).

These are constructive developmental findings, including adaptations of
ordinary potential transformations, belief compression and robust optimization.
The closest comparisons are named. No material external-task benefit or >=80%
verification forecast has been established. No confirmation gate is attempted.

## Next constructive move

Develop informative observations and paid marginal acquisition for the compact
value controller: determine which correlations re-enter, how to certify a
useful proposed plan, and whether choosing computations by its obstruction
beats equally informed conventional acquisition. Keep statistical count
transport and the broader five-question portfolio available. Do not spend
another long screen tuning the exposed joint SAT scheduler without a changed
mechanism; any revived claim needs a matched bounded ordinary control.

## Recovery and continuation

The user reported a remote compaction stream error. The resident clock survived;
no new clock or duplicate cycle was started. The entire unobserved 18-minute
gap and one inseparable failed-retrieval/input interval earn zero research.
[Recovery record](recovery04.json) and appended dispositions preserve raw bytes.
Experiment completion during that gap earns no principal time. C001 remains
unfinished; continue useful work through its floor and into subsequent research.
Prior main publication was `e2f4e8ee977aa3001cbe96c8a69ae7f523f92493`, remote verified.
''',encoding='utf-8')
print(json.dumps({k:eff[k] for k in ('exact_cycle_research_minutes','exact_remaining_floor_minutes','exact_phase_research_minutes')}))
