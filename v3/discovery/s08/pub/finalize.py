"""Publication-only active pointers and recurrence append. Run once."""
from pathlib import Path
import json,hashlib,copy,subprocess
root=Path(__file__).resolve().parents[4]
def read(p):return (root/p).read_text(encoding='utf-8')
def write(p,s):(root/p).write_text(s,encoding='utf-8',newline='\n')
def save(p,x):write(p,json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
a=json.loads(read('v3/discovery/s08/effective_actuals.json'));s='v3/discovery/s08/'
assert a['research_ns']==14402318580700 and not a['clock_active']
close='''
## Closing disposition — October 14, 2026 UTC

**Codex (GPT-6)** completed the requested four-hour increment with
**14,402,318,580,700 ns =240.038643011666666… research minutes**.
C001/program: **44,251,453,147,247 ns =737.524219120783333… minutes**;
phase: **109,419,335,189,096 ns =1823.655586484933333… minutes**.
The research boundary is 04:16:50.790658 UTC; the final resident mark is
04:17:06.040059 UTC. No further research is credited.

[Checkpoint](cp01.md), [findings](findings.md), [effective actuals](effective_actuals.json),
[reconciliation](reconcile.py), and [reproduction](reproduce.md) are the closing
records. Five mixed context-refresh intervals are excluded, the crashed open
interval has zero credit, and one D/E interval is reclassified without changing
research. Raw clocks and all failure prefixes remain. Effective D/L/E minutes
are 92.101007283333… /18.15084489 /129.786790838333…; implementation exceeded its
central mode forecast. Purpose and lane totals are in effective actuals.

S31–S33 are three new families within this one recurrence. All remain
DEVELOPMENT. F01 remains **20–45%, central 30%, change 0 points** since s07.
C001 OPEN; P3-POS01 OUTSTANDING; P3-11 deferred. Publication and repository
maintenance add zero research credit. The next requested session defaults
to 60 minutes, with any explicit author override controlling its duration.
'''
assert '## Closing disposition' not in read(s+'session.md');write(s+'session.md',read(s+'session.md')+close)
write(s+'running.md', '> **Closed:** this is the historical in-session notebook. Use [cp01](cp01.md) and [findings](findings.md) for the reconciled closing state. No active clock remains.\n\n'+read(s+'running.md'))

p='TODO_v3.md';t=read(p)
for old,new in [('497.485576109117','737.524219120783'),('1583.616943473267','1823.655586484933'),('623.616943473267','863.655586484933')]:t=t.replace(old,new)
t=t.replace('The author now directs **one-hour increments**','The default is **one-hour increments**, subject to explicit author overrides,')
t=t.replace('from [s07](v3/discovery/s07/cp01.md)','from [s08](v3/discovery/s08/cp01.md)').replace('for one further requested hour','for the next requested duration (default one hour)')
start=t.index('## Current author selection');end=t.index('The program has',start)
t=t[:start]+'''## Current author selection — October 13–14, 2026

**P3-SEARCH-01-C001 remains OPEN; P3-POS01 is OUTSTANDING.** The author's
[four-hour override](v3/decisions/2026-10-13_four_hour_session.md) is complete.
The latest **Codex (GPT-6)** increment adds **240.038643011666666… minutes**;
C001/program is **737.524219120783333…** and phase research is
**1823.655586484933333… minutes**. The default remains 60-minute increments,
with explicit author overrides controlling individual sessions.

Read [s08 checkpoint](v3/discovery/s08/cp01.md),
[findings](v3/discovery/s08/findings.md), [exact actuals](v3/discovery/s08/effective_actuals.json),
[portfolio](v3/discovery/candidates.md), [recurrence table](v3/discovery/recurrences.md)
and [portable prompt](v3/discovery/CONTINUE.md). All clocks are closed. Exact
session research is **14,402,318,580,700 ns**; program **44,251,453,147,247 ns**;
phase **109,419,335,189,096 ns**. Failed and excluded intervals remain visible;
publication and checkout repair earn no research credit.

The budgeted source-bound query service delivers 512 outputs per arm with
2,886 physical fee and 137,310 named units, improving both recorded components
over greedy cover and anchor on this narrow development family. An ordinary
budgeted controller ties it. The larger graph cover has higher computation
and only 6.00% aggregate fee savings against anchor. New matroid/group-query
and box-regret bridges establish finite capability, including six actual
complete negative proofs; they do not establish a full-cost advantage.

The same-event [F01 forecast](v3/discovery/s08/forecast_final.md) remains
**20–45%, central 30%, change 0 points** since s07. No candidate is promoted.
**S31–S33 remain DEVELOPMENT; 33 families record breadth, not readiness.**
Next test a small source-bound matroid/group-query service with a cheap anchor,
priced bounded lookahead, actual proof admission, and strong ordinary controls.
Declare its useful claim separately before forecasting it. Generality, model
adequacy and the cost of source recognition remain open. Preserve the existing
F01 event rather than substitute a favorable new domain.

'''+t[end:];write(p,t)

p='v3/README.md';t=read(p);end=t.index('## Research direction')
write(p,'''# Phase Three: Reasoning About Unresolved Mathematics

Current update: **Codex (GPT-6), October 14, 2026 UTC**. Earlier contributor
attributions and scientific records retain their original scope.

**P3-01–10 are complete at their declared scopes. P3-SEARCH-01-C001 remains
OPEN; P3-POS01 OUTSTANDING; P3-11 deferred.** C001's original four-hour floor
is satisfied. The latest explicitly requested four-hour increment adds
**240.038643011666666… research minutes**. Cumulative C001/program research is
**737.524219120783333… minutes**; phase research is **1823.655586484933333…**.
All research clocks are closed. Default sessions are 60 minutes, subject to
[explicit author overrides](decisions/2026-10-13_four_hour_session.md).

Read [s08 checkpoint](discovery/s08/cp01.md), [findings](discovery/s08/findings.md),
[effective actuals](discovery/s08/effective_actuals.json),
[portfolio](discovery/candidates.md), [single recurrence table](discovery/recurrences.md),
and [portable continuation](discovery/CONTINUE.md).

The latest paid budgeted-query construction improves both recorded fee and
named computation against anchor/greedy cover on four star streams; ordinary
budgeted selection ties it. Broader graph results expose a computation cost
obstacle. Matroid/group-query cover and scalar box-regret proof bridges extend
capability, with explicit Cartesian versus shared-cost limits. None establishes
the complete-cost confirmation event. **F01 remains 20–45%, central 30%, change
0 points since s07.** The 33 candidate families measure breadth, not readiness.

Next construct a small paid matroid/group-query service with a cheap anchor
and priced lookahead; test source generality and setup repayment. Preserve
all failed attempts and use [reproduction](discovery/s08/reproduce.md) to separate
old evidence reconstruction from new acquisition. [TODO_v3.md](../TODO_v3.md)
and [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md) govern the open program.

'''+t[end:])

p='v3/discovery/P3_SEARCH_01.md';t=read(p);start=t.index('Latest execution contributor:');end=t.index('## 1. Objective and scope')
t=t[:start]+'''Latest execution contributor: **Codex (GPT-6)**. Earlier records retain their
original attributions. [Current checkpoint](s08/cp01.md), [findings](s08/findings.md),
[portfolio](candidates.md), [exact actuals](s08/effective_actuals.json), and
[single recurrence table](recurrences.md) give the closing state.

The explicit four-hour s08 increment is closed at **240.038643011666666…
research minutes**. Program/C001 research is **737.524219120783333… minutes**.
The default next session is 60 minutes; explicit author overrides take priority.
The [portable prompt](CONTINUE.md) governs recovery and a fresh observed clock.

Current direction: source-bound action queries and inexpensive anchor-backed
policies, with policy-invoice learning and shared-cost action frontiers as
separate branches. The budgeted star service improves both recorded fee and
computation, while an ordinary matching controller ties. General graph cover
still has a large computation bill; generated matroid geometry and scalar
box-regret proofs provide new capability but not demonstrated economic advantage.
**S31–S33 remain DEVELOPMENT; 33 families record breadth, not readiness.**

[F01/S28-B1/V1](s08/forecast_final.md) remains **20–45%, central 30%, change
0 percentage points** since s07. No candidate is promoted. Next test a small
paid matroid/group-query construction with bounded lookahead and strong
ordinary methods, keeping a new confirmation event separate from F01.

'''+t[end:];write(p,t)

p='v3/discovery/candidates.md';t=read(p);start=t.index('**Current continuation');end=t.index('IDs S01 onward')
t=t[:start]+'''**Current continuation — October 14, 2026:** **Codex (GPT-6)**,
[s08 checkpoint](s08/cp01.md), [effective actuals](s08/effective_actuals.json).
The explicit four-hour increment contributes **240.038643011666666… minutes**;
C001 remains OPEN at **737.524219120783333…**, phase **1823.655586484933333…**.
All clocks are closed. Default next duration is 60 minutes with explicit author
overrides. Earlier entries and attributions retain their historical scope.

[F01/S28-B1/V1](s08/forecast_final.md) remains **20–45%, central 30%, change
0 points** since s07; P3-POS01 OUTSTANDING, P3-11 deferred. **33 families**
record breadth, not readiness. New S31–S33 remain DEVELOPMENT.

'''+t[end:]
lines=t.splitlines();lines += ['', '## s08 constructive update — October 14, 2026, Codex (GPT-6)', '', '| ID | Mechanism and lineage | Intended useful delta / comparison | Evidence and obstacle | Disposition |', '|---|---|---|---|---|'];idx=len(lines)
lines[idx:idx]=[
'| S31 | Policy-invoice learning under partial feedback; continuation of S01/S25/S26. Q1/3/4. | Learn which computation is worth buying without identifying the entire latent law. Compare compulsory calibration, direct on-policy LCB and policy replay/circuit queries. | Calibrated pair observations can leave policy ranking unidentified. Circuit targets contract but paid pilot learning loses physical fee to direct on-policy learning on all 20 nontrivial is01 duties. Large exact diagrams hit caps. [Findings](s08/invoice_service_findings.md). | DEVELOPMENT; adequacy and calibration cost unresolved |',
'| S32 | Source-bound action-query and certificate-cover service, including graph/matroid rank and budgeted anchor policies. Q1/4/5. | Deliver a robust original-source action using fewer paid observations, with priced compilation and fallback. Compare ordinary stochastic cover, uncertainty queries and identical budgeted policy improvement. | bc02 improves recorded fee/computation against greedy/anchor; ordinary budgeted controller ties. General graphs retain a large computation bill. Matroid proof recognition is generated-family specific. [Findings](s08/graph_cover_findings.md), [matroids](s08/matroid_findings.md). | DEVELOPMENT; next constructive focus |',
'| S33 | Shared-cost robust action/replacement frontiers and scalar interval-regret proof transport. Q2/4/5. | Use nonnominal actions and retained source proofs under partial costs; compare ordinary robust optimization and exact/minimax policy planning. | Shared costs need two-copy frontiers and can encode MaxCut despite simple matroid geometry. Six actual scalar proofs establish a tiny Cartesian-box bridge; correlated costs only inherit an upper bound. [Shared frontiers](s08/shared_findings.md), [box proof](s08/box_bridge.md). | DEVELOPMENT; no complete-cost or novelty claim |']
write(p,'\n'.join(lines)+'\n')

p='v3/RESEARCH_PROTOCOL.md';t=read(p);old='requests one-hour engaged-research sessions with durable handoffs between\nChatGPT and Codex.';assert old in t
t=t.replace(old,'sets a default of one-hour engaged-research sessions with durable handoffs\nbetween ChatGPT and Codex. Explicit author duration overrides take precedence\nfor that session; the [October 13 four-hour instruction](decisions/2026-10-13_four_hour_session.md)\nis one such override. It does not change the default for later sessions.');write(p,t)

p='v3/plan.v1.json';x=json.loads(read(p));x['last_completed_session']=s+'session.md';x['last_preserved_session']=s+'session.md';x['last_discovery_session']=s+'session.md'
x['observed_progress'].update(research_ns=a['phase_research_ns'],research_minutes=a['phase_research_minutes'],source=s+'effective_actuals.json',evidence_disposition='s08 explicit four-hour increment closed after conservative exclusions; source-bound budget/cover and scalar proofs remain DEVELOPMENT. No publication credit.')
# The old measured_engaged_ns was a stale s06 aggregate; retain as historical,
# rather than fabricate a later phase-wide administration total.
x['observed_progress']['historical_s06_measured_engaged_ns']=x['observed_progress'].pop('measured_engaged_ns',None)
x['observed_progress']['measured_engaged_ns']=None;x['observed_progress']['measured_engaged_scope_note']='Current phase-wide D/L/E/O total not recomputed; exact qualifying research is reconstructed.'
d=x['discovery_program'];d.update(research_ns=a['program_research_ns'],research_minutes=a['program_research_minutes'],latest_checkpoint=s+'cp01.md',actuals=s+'effective_actuals.json')
d['sessions'] += [v for v in ['v3/discovery/s07/session.md',s+'session.md'] if v not in d['sessions']]
d['current_cycle'].update(research_ns=a['cycle_research_ns'],research_minutes=a['cycle_research_minutes'],session=s+'session.md',actuals=s+'effective_actuals.json',clock_active=False,session_status='closed_author_directed_four_hour_handoff')
d['execution_cadence'].update(session_research_minutes=60,explicit_author_override_allowed=True,last_session_target_minutes=240,last_override_authority='v3/decisions/2026-10-13_four_hour_session.md',last_closed_session='s08',last_increment_research_ns=a['research_ns'],last_increment_research_minutes=a['research_minutes'])
d['promotion'].update(current_candidate='S28-B1',current_probability=0.30,current_probability_range=[0.20,0.45],forecast_status='F01 reassessed unchanged; no promotion',event_id='F01',verification_plan_version='V1',assessment=s+'forecast_final.md')
x['optional_recurrence_advice']['current_recommendation']='Continue from s08 using v3/discovery/CONTINUE.md for the next explicitly requested duration, default60 minutes. Construct a small source-bound matroid/group-query service with cheap anchor and priced lookahead. C001 OPEN; F01 20-45%, central30%; P3-11 deferred.'
save(p,x)

p='v3/claim_ledger.md';write(p,read(p)+'''
## Discovery s08 — October 13–14, 2026; Codex (GPT-6)

The [four-hour checkpoint](discovery/s08/cp01.md) adds **240.038643011666666…**
research minutes; C001/program **737.524219120783333…**, phase
**1823.655586484933333…**. [Exact effective records](discovery/s08/effective_actuals.json)
exclude compaction, crashed open time and publication. All clocks are closed.

| Claim | Current disposition | Evidence and restriction |
|---|---|---|
| DS-S31 invoice-target learning | DEVELOPMENT | [Paid comparison](discovery/s08/invoice_service_findings.md): query targets can contract, but direct on-policy learning wins physical fee on the 20 nontrivial fresh development duties. Pair calibration alone does not establish policy adequacy; no general learning superiority. |
| DS-S32 source-bound budgeted cover | DEVELOPMENT | [Actual service](discovery/s08/graph_cover_findings.md): bc02 delivers 512 outputs per arm, budget 2,886 fee/137,310 named units versus cover 2,937/157,452 and anchor 4,608/152,022. Ordinary budget ties. General graph computation remains costly; complete economic prices unknown. |
| DS-S32 matroid/group queries | DEVELOPMENT | [Finite extension](discovery/s08/matroid_findings.md): weighted rank cover under stated geometry, shared groups retain cover submodularity, but robust action selection can remain hard. Generated source admission is not a general recognizer. |
| DS-S33 robust frontiers and box proof | DEVELOPMENT | [Shared frontier](discovery/s08/shared_findings.md), [six actual scalar proofs](discovery/s08/box_bridge.md). Cartesian cost boxes support the exact induced objective; correlated groups need their own geometry and only inherit the box upper. Ordinary interval optimization is prior art. |
| P3-POS01 / F01 | OUTSTANDING; no promotion | [Same-event reassessment](discovery/s08/forecast_final.md): 20–45%, central30%, change0 points since s07. New branches do not inherit F01. Ordinary mirroring rules out superiority over that mirror but does not alone disqualify substantial synthesis. |

S31–S33 add three families, bringing breadth to 33. Next use the
[portable continuation](discovery/CONTINUE.md); default60 minutes with explicit
author duration overrides. P3-11 remains deferred.
''')

print('active pointers and session closed')
