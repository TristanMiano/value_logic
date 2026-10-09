"""Close observed recurrence accounting; preserve every prior ledger byte.
ChatGPT (GPT-6 Astra Pro), 2026-10-09. Run only after clock.py stop.
"""
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timezone
from hashlib import sha256
import csv, io, json, importlib.util

ROOT=Path(__file__).resolve().parents[3]
S=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('recurrence_clock',S/'clock.py')
cl=importlib.util.module_from_spec(sp);sp.loader.exec_module(cl)
def h(b):return sha256(b).hexdigest()
def mins(n):return f'{Decimal(n)/Decimal(60000000000):.12f}'
def secs(n):return f'{Decimal(n)/Decimal(1000000000):.9f}'
def save(p,x):
    with p.open('x') as f:json.dump(x,f,indent=2);f.write('\n')

def main():
    assert json.loads((S/'clock_state.json').read_text()) is None
    assert not (S/'actuals.json').exists(), 'Already closed; inspect the saved closure instead.'
    startup=json.loads((S/'startup.json').read_text())
    segments=cl.effective_segments()
    events=cl.read_records(S/'clocks.jsonl')
    assert events[-1]['command']=='stop'
    categories={k:sum(s['elapsed_ns'] for s in segments if s['mode']==k) for k in ['D','L','E','O','wait','idle','unmeasured','recovery']}
    research=sum(categories[k] for k in ['D','L','E'])
    assert research==5408785554031 and research>=5400000000000
    engaged=research+categories['O']
    lanes={k:sum(s['elapsed_ns'] for s in segments if s['lane']==k and s['mode'] in ('D','L','E')) for k in ('R','X')}
    assert sum(lanes.values())==research
    cadence=[]
    for s in segments:
        if s['mode'] not in ('D','L','E','O'):continue
        points=sorted(set([s['start_monotonic_ns'],s['end_monotonic_ns']]+[e['monotonic_ns'] for e in events if s['start_monotonic_ns']<=e['monotonic_ns']<=s['end_monotonic_ns']]))
        for a,b in zip(points,points[1:]):
            if b-a>900000000000:cadence.append({'start':a,'end':b,'elapsed_ns':b-a})
    assert not cadence
    ledger=ROOT/'v3/time_ledger.csv';base=ledger.read_bytes()
    assert len(base)==151465 and h(base)==startup['v3_ledger_sha256']
    assert b'R-P3-B-A,' not in base
    v2=ROOT/'v2/time_ledger.csv'
    v2sha=h(v2.read_bytes())
    assert v2sha=='5c71a4727f1cb7e03565f1c495b0c63b351863583120f0ec5684aca48bd122c6'
    fields=next(csv.reader(io.StringIO(base.decode())))
    out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=fields,lineterminator='\n')
    seen=set(); forecasts={'D':3000,'L':1200,'E':1200,'O':600}
    for s in segments:
        mode=s['mode'];n=s['elapsed_ns'];active=mode in forecasts
        forecast=forecasts[mode] if active and mode not in seen else 0
        seen.add(mode)
        writer.writerow(dict(task_id='R-P3-B-A',attempt_id='R-P3-B-A-1',session_id='2026-10-09-S1',
            mode=mode,lane=s['lane'],start_utc=s['start_utc'],end_utc=s['end_utc'],elapsed_seconds=secs(n),
            engaged_seconds=secs(n if active else 0),tool_wait_seconds=secs(n if mode=='wait' else 0),
            idle_seconds=secs(n if mode=='idle' else 0),unmeasured_seconds=secs(n if mode in ('unmeasured','recovery') else 0),
            forecast_seconds=str(forecast),artifact='v3/work_logs/R_P3_B_A_2026-10-09_S1.md',
            status='Closed observed recurrence interval; scientific completion separately assessed; '+s['note']))
    appended=out.getvalue().encode();combined=base+appended
    assert base.endswith(b'\n')
    with ledger.open('ab') as f:f.write(appended)
    assert ledger.read_bytes()[:len(base)]==base
    receipt=dict(base_bytes=len(base),base_sha256=h(base),append_bytes=len(appended),append_rows=len(segments),
        append_sha256=h(appended),result_sha256=h(combined),prior_bytes_preserved=True)
    save(S/'ledger_append_receipt.json',receipt)
    with (S/'effective_segments.jsonl').open('x') as f:
        for s in segments:f.write(json.dumps(s)+'\n')
    phase=startup['prior_phase_research_ns']+research
    remaining=57600000000000-phase
    a=dict(schema='value_logic.r_p3b_a.actuals.v1',task='R-P3-B-A',attempt='R-P3-B-A-1',
        session='2026-10-09-S1',base_commit=startup['base_commit'],clock_stopped=True,
        recorded_end_utc=events[-1]['utc'],research_ns=research,research_minutes=mins(research),
        task_research_ns=research,task_research_minutes=mins(research),protected_research_floor_minutes=90,
        prior_verified_task_research_ns=0,historical_recredit_ns=0,parallel_reviewer_credit_ns=0,
        prior_clock_recovery='Entry found no earlier clock for this selected recurrence. Current raw observations and five additive dispositions are retained; unobserved recovery receives no credit.',
        research_floor_satisfied=True,task_floor_margin_ns=research-5400000000000,task_remaining_floor_ns=0,
        total_engaged_ns=engaged,total_engaged_minutes=mins(engaged),category_ns=categories,
        category_minutes={k:mins(v) for k,v in categories.items()},lane_research_ns=lanes,
        lane_research_minutes={k:mins(v) for k,v in lanes.items()},
        lane_percent={k:str(Decimal(v)*100/Decimal(research)) for k,v in lanes.items()},
        prior_phase_research_ns=startup['prior_phase_research_ns'],prior_phase_measured_engaged_ns=startup['prior_phase_engaged_ns'],
        phase_research_ns=phase,phase_research_minutes=mins(phase),
        phase_measured_engaged_ns=startup['prior_phase_engaged_ns']+engaged,
        phase_remaining_floor_ns=remaining,phase_remaining_floor_minutes=mins(remaining),
        next_phase_checkpoint_minutes=960,new_phase_checkpoint_crossed=False,cadence_violations=cadence,
        forecast_error_minutes={k:str(Decimal(categories[k])/Decimal(60000000000)-Decimal(forecasts[k])/60) for k in forecasts},
        ledger=receipt,phase_two_ledger_sha256=v2sha,
        accounting_source_sha256=h(Path(__file__).read_bytes()),
        publication_tail='After this observed stop, final files, packaging, transfer, remote verification and response work are conservatively unmeasured, with zero additional engaged or research credit. No duration is inferred.',
        status='COMPLETE at restricted paid-feedback/observable-performance scope; P3-08 unstarted; P3-C/D unattempted.')
    save(S/'actuals.json',a)
    save(S/'boundary_accounting.json',dict(status='PASS',clock_closed=True,research90_satisfied=True,
        research_ns=research,phase_research_ns=phase,ledger_prior_bytes_preserved=True,
        effective_segments=len(segments),all_segment_arithmetic_exact=True,all_lanes_reconcile=True,
        historical_and_parallel_recredit_ns=0,cadence_violations=[],phase_two_ledger_unchanged=True,
        original_clock_events_sha256=h((S/'clocks.jsonl').read_bytes()),
        raw_segments_sha256=h((S/'segments.jsonl').read_bytes()),
        dispositions_sha256=h((S/'clock_dispositions.jsonl').read_bytes()),
        effective_segments_sha256=h((S/'effective_segments.jsonl').read_bytes())))
    plan=ROOT/'v3/plan.v1.json';x=json.loads(plan.read_text())
    x['active_session']=None
    x['last_completed_session']='v3/work_logs/R_P3_B_A_2026-10-09_S1.md'
    x['last_preserved_session']=x['last_completed_session']
    x['observed_progress']['measured_engaged_ns']=a['phase_measured_engaged_ns']
    x['selected_recurrence']['actuals']='v3/work_logs/R_P3_B_A_2026-10-09_S1/actuals.json'
    x['selected_recurrence']['completion_recorded_utc']=events[-1]['utc']
    plan.write_text(json.dumps(x,indent=2)+'\n')
    text=f'''# R-P3-B-A — paid selective-feedback recurrence

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Session **2026-10-09-S1**,
attempt **R-P3-B-A-1**. Selected by the author after the published P3-B gate.

## Boundary result

**COMPLETE at the declared finite paid-feedback and observable-performance
scope.** Research90 is satisfied by **{mins(research)} measured research
minutes**. The [additive checkpoint](../checkpoints/B_1_R_P3_B_A.md),
[current 21-duty overlay](../checkpoints/B_1_R_P3_B_A.v1.json),
[scientific review closure](R_P3_B_A_2026-10-09_S1/review_closure.md) and
[contribution assessment](R_P3_B_A_2026-10-09_S1/contribution_assessment.md)
record the scientific disposition. P3-N01 is **SUPPORTED at modest formal
adaptation and implementation synthesis scope**. Q3 affirmative advantage
against the strongest ordinary combination remains open.

P3-08 is the recommended next item and remains **unstarted**. P3-C/D remain
unattempted. Options B/C and R-P3-N01 remain unselected. No final challenge is
frozen or exposed. This closes only the recurrence the author selected.

## Entry and preservation

Current GitHub main was inspected before work at
[6ce7391](https://github.com/TristanMiano/value_logic/commit/{startup['base_commit']}).
P3-07 and P3-B were already complete and published. The entry found no prior
clock for this new recurrence; the [startup record](R_P3_B_A_2026-10-09_S1/startup.json),
[selection](R_P3_B_A_2026-10-09_S1/selection.json) and
[prospective forecast](R_P3_B_A_2026-10-09_S1/forecast.json) retain the decision.

Completed P3-01–07 experiments were not repeated. Old scientific files,
including the surviving defensive-forecasting addendum and its evidence,
remain byte-identical. The original P3-B gate and duty matrix are historical;
the new checkpoint is an additive overlay, not a rewrite of that decision.

## What the research established

The [main derivation](../derivations/07_selective_feedback.md) joins a fixed
exogenous mathematical-query tape, exact one-purchase-per-block feedback,
checked action corrections and all-issued expected loss. It derives the
fixed-mass normalization and dyadic-action allowances, a separately justified
Brier bound, adaptive propensity correction, and actual setup/controller/
purchase costs. Exact witnesses show why immediate block updates, adaptive
query tapes, greedy actions and omitted propensities cannot inherit that bound.

The [observable companion](../derivations/07_observable_performance.md) uses
only purchased labels and public forecasts to assess the completed episode.
Binary Brier and remaining-action loss have one shared unknown residual.
Predictable width bounds with a predeclared exponential rate give scoped joint
certificates; the two-sided extension can expose poor performance. The final
hard-answer analysis supplies a predictable block-entry snapshot interface,
with known losses removed by public centering. It remains unexecuted
mathematics, not a completed hard-state integration.

The executed development programme contains 20 uniform learner arms, three
adaptive arms and eight ordinary controls. All completed arms and unfavorable
results remain. At T=3,968 and block size eight, the exact-state uniform v1.1
learner costs 2,935,898 units and its finite-state counterpart 1,039,110,
about a 64.6% reduction. Their errors are 1,703 and 1,702. Current v1.2 adds
26 setup-registry units by a source-only transfer, not a rerun. The adaptive
learner costs 1,382,703 with 1,754 errors. The cold exact table costs 171,880
with zero errors. A source-level inequality proves the current table's
common-tariff advantage on all successful admitted tapes.

Public-only diagnostics retain 49,600 forecast rows and 10,664 already-paid
labels across all 23 learner episodes. Independent principal reconstruction
checks the basic, centered and two-sided formulas directly from the public
archives, without private scores or a new policy run. Ten uniform rows have
Brier lower endpoints above the constant-half null; no row gives a strict
conditional-action-null decision. No interval intersection is empty.
These fixed-seed development flags do not validate frequentist coverage or
give simultaneous 95% coverage across the grid.

## Evidence and review

- [Uniform results and archive correction](R_P3_B_A_2026-10-09_S1/development/service_comparison/README.md)
- [Adaptive analysis, portable display](R_P3_B_A_2026-10-09_S1/development/allocation_comparison/analysis_portable.md)
- [Observable analysis, portable display](R_P3_B_A_2026-10-09_S1/development/observable_certificate/analysis_portable.md)
- [Complete two-sided grid](R_P3_B_A_2026-10-09_S1/development/observable_certificate/two_sided_grid.md)
- [Primary-source comparison](../literature/07_selective_feedback_sources.md)
- [Final checkpoint review](R_P3_B_A_2026-10-09_S1/reviews/literature_agent/final_checkpoint_review.md)
- [Frozen hard-answer proof review](R_P3_B_A_2026-10-09_S1/reviews/proof_agent/frozen_hard_composition_review.md)
- [Source and archive audit](R_P3_B_A_2026-10-09_S1/reviews/final_evidence_audit.json)

Reviews were separate same-model, nonblind assignments. Their time adds zero
to the principal clock. The principal read and reconciled their findings and
independently reconstructed the public certificate statistics. Source-bound
initial failures, numerical repairs, setup erratum, version transfer and
negative ordinary comparisons remain attached to their actual versions.

All ten ZIPs passed complete membership, byte count, CRC and SHA-256 checks:
117 payloads, 159,486,160 uncompressed payload bytes. The first uniform ZIP
was an incomplete prefix. Its guard stopped before any original deletion;
the full expected container was rebuilt from intact hash-matching originals,
verified, then substituted. Only redundant raw originals were removed.
The failure and exact correction history remain; no scientific run was repeated.
Two original reviewed analysis files retain their eight legacy math delimiters;
portable display copies preserve the original source hashes and content.

## Observed accounting

| Mode | Measured minutes |
|---|---:|
| D — derivation and interpretation | {mins(categories['D'])} |
| L — primary-source work | {mins(categories['L'])} |
| E — implementation, experiments and evidence analysis | {mins(categories['E'])} |
| **D + L + E** | **{mins(research)}** |
| O — recorded administration and publication preparation | {mins(categories['O'])} |
| **Total engaged** | **{mins(engaged)}** |
| Unmeasured intervals, excluded | {mins(categories['unmeasured'])} |
| Recovery intervals, excluded | {mins(categories['recovery'])} |

The research floor margin is {research-5400000000000:,} nanoseconds.
Reliable/exploratory research is {mins(lanes['R'])} / {mins(lanes['X'])}
minutes. The central forecast was D/L/E = 50/20/20 and O = 10 minutes;
actual modes reflect the work performed, not retrospective quotas. Existing
primary comparisons reduced new literature time, while finite implementation,
observable-performance and assumption analysis used more of D/E.

[Actuals](R_P3_B_A_2026-10-09_S1/actuals.json),
[raw observations](R_P3_B_A_2026-10-09_S1/clocks.jsonl),
[additive clock dispositions](R_P3_B_A_2026-10-09_S1/clock_dispositions.jsonl)
and [boundary audit](R_P3_B_A_2026-10-09_S1/boundary_accounting.json)
retain exact nanosecond arithmetic. Five dispositions preserve recovery
exclusions and one mode-label correction. No historical duration was inferred
from conversation length and no concurrent-agent effort was added.

The append contains {len(segments)} rows and preserves all 151,465 prior
phase-three ledger bytes; the phase-two ledger is unchanged. Phase research
is **{mins(phase)} minutes**, leaving **{mins(remaining)} minutes** to the
960-minute floor. No new 4/8/16-hour checkpoint was crossed. The observed
clock stops at **{events[-1]['utc']}**. Subsequent final packaging, transfer,
remote verification and response work are conservatively unmeasured and
receive no additional engaged or research credit.

## Next useful work

Proceed to P3-08 when selected by the author. Integrate the accepted paid
feedback, hard-answer, version-invalidation and reporting contracts with the
strong ordinary fallback. The standalone learner does not yet discharge U04.
More retuning on this same easily solved family has low expected value.

Retain optional **B, Research90**, before P3-09 if independently delivered
checkable evidence is a primary endpoint. Compare equal construction, export,
edits, checking and storage. Optional **C, Research60**, remains a later
opportunity for counterpossible-policy robustness. Neither starts at this
boundary. The author retains the later P3-C and P3-D decisions.
'''
    (ROOT/'v3/work_logs/R_P3_B_A_2026-10-09_S1.md').write_text(text)
    print(json.dumps({k:a[k] for k in ('research_minutes','total_engaged_minutes','phase_research_minutes','phase_remaining_floor_minutes','recorded_end_utc')}))

if __name__=='__main__':main()

