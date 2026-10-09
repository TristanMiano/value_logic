# Phase Three: Reasoning About Unresolved Mathematics

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Updated October 9, 2026 UTC.

**P3-01–07 are complete at their declared scopes; P3-A has passed at restricted-representation readiness scope.** The author has set a
minimum of **16 measured hours of research**, with longer work possible.
[TODO_v3.md](../TODO_v3.md) contains the tasks, gates and acceptance criteria;
[RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md) controls execution and accounting.

## Research direction

Can a reasoner improve decisions while it remains uncertain about mathematical
answers, the value of its models and the benefits of thinking longer? Phase
three investigates logical uncertainty, logical counterfactuals, simultaneous
use of fallible models, improving usefulness estimates and probability
information carried by values.

The [phase-two report](../paper_v2.md) supplies explicit loss meanings, shared
uncertain sources, conditional proofs, evidence revision and information
retention under changed costs. Those are useful starting materials. Its
bounded proof-search example predicts a procedure's success at proving
already-true requests. The wider inherited system also treats explicit
report-dependent behavior; neither establishes arbitrary mathematical-belief
learning. Its semantics rejects an empty deployment source, while its Boolean
fragment retains classical entailment. General counterpossible answers remain
a new obligation.

The initial research position is:

| Question | Starting hypothesis to investigate |
|---|---|
| Logical uncertainty | Versioned loss estimates and evidence may support a bounded learner, provided computation and unresolved claims have explicit semantics. |
| Logical counterfactuals | Declared changes and transported dependencies may support useful restricted hypotheticals; general impossible antecedents need their own analysis. |
| Several useful models | The strongest hope is better management of approximation, cost and revision. Compare with ordinary conditional modeling and decision theory. |
| Improving usefulness estimates | A sequence of forecasts should guide both decisions and the purchase of further reasoning; distinguish predictive accuracy from practical value. |
| Probability information in values | Known event-contingent losses can encode probabilities; arbitrary aggregate utility need not identify them. |

These are agenda statements, not completed phase-three findings. The
[claim ledger](claim_ledger.md) records their current status and evidence targets.

## A simple probability bridge

Suppose relying on a mathematical claim costs 10 units when it is false and
zero when it is true. With a declared subjective probability
$`p_t=\Pr_t(\varphi)`$, its estimated loss is

```math
\widehat L_t=10(1-p_t),\qquad p_t=1-\widehat L_t/10.
```

An estimated loss of 3 then encodes probability 0.7. This elementary conditional
identity is an illustration of an expected-loss model, not a learning algorithm.
Unknown stakes, additional costs or a different risk criterion can prevent
that recovery. Multiple known loss queries can retain more information than
one aggregate score. The [finite probability-information analysis](derivations/02_probability_information.md)
now gives exact conditions for full-law recovery, specified expected losses,
certified intervals and some optimal action. Those services can require
different information. Unknown shared scale or offset, restricted query
choices and dependence needed for joint actions have explicit consequences.

A [proper scoring rule](literature/00_orientation.md)
offers a related bridge: a loss for a reported probability can reward accurate
beliefs. The epistemic forecast, the stakes of an action and the cost of
computing an answer remain separate objects.

## What would make this phase worthwhile?

The central ambition is to connect uncertain mathematical prediction, paid
reasoning and justified model changes in a precise, useful system. A restricted
theorem, a constructive interface, an informative limitation or a modest
synthesis/application can qualify when its difference from the closest checked
work is supported. The [source orientation](literature/00_orientation.md)
identifies strong existing alternatives for that comparison.

The programme has an initial 16-hour research traversal and a 4-hour central
recurrence reserve. Its **20-hour central / 40-hour high research forecasts**
remain estimates. Setup and routine administration are separate O time and
do not reduce the sixteen-hour research requirement. Exact future effort is
recorded in [time_ledger.csv](time_ledger.csv).

Phase two remains complete. Its records, clocks, paper and scientific freezes
are preserved; its neural follow-ups remain optional. P3-01 supplies a
[question contract](foundations/01_problem_contract.md), exact comparison
duties, primary-source reconstructions and finite development diagnostics.
P3-02 adds finite identification, calibration, decision and repair results,
[source comparisons](literature/02_probability_sources.md), and a
[rational certificate companion](checks/02_finite_information_audit.py).
This supplies a concrete restricted information interface for later research.
The [P3-A readiness assessment](checkpoints/A_1.md) selects a provisional
versioned interface for finite rational constraints and loss queries, with
known calibrated payoffs and interval/set uncertainty as the starting choice.
Its probability adapter is explicit; alternative representations remain open.
P3-03 now supplies a [finite bounded information process](derivations/03_logical_uncertainty.md):
retained execution/checking, an interruptible outer cover, conditional loss
bounds and named-action certificates. Its [companion proofs](derivations/03_refinement_extensions.md)
separate finite-prefix completion, task certainty, source recovery and revision
support. The general proof-stream adapter is mathematical; the actual prototype
handles its declared finite Boolean/bounded-VM fragment. The P3-03 prototype itself supplies no anticipatory learner or
paid-computation policy. Later P3-06/07 add scoped forecasting and paid selection;
no final experiment has been established. P3-04 now supplies [finite counterfactual semantics](derivations/04_counterfactual_semantics.md),
[selection extensions](derivations/04_selection_extensions.md), and
[separately reconstructed executable evidence](work_logs/P3_04_2026-10-08_S2.md).
It covers typed structural changes, explicitly exceptional paired-support
counterpossibles, ranked selection, all-optimum coverage and task bounds.
The original lost execution archives are not represented as recovered.
P3-05 is **complete** at [finite transport and checked-reuse scope](derivations/05_counterfactual_transport.md),
with [joined conditional proofs](derivations/05_portfolio_transport.md),
[edit-stable information](derivations/05_edit_information.md), finite dependency
and counterpossible front ends, rank-weight robustness and retained proof chains.
The [ordinary-method comparison](derivations/05_resource_comparison.md) retains
both savings over fresh proof search and faster warm decision-diagram reasoning.
[Exact S2/S3 records](work_logs/P3_05_2026-10-08_S3.md) give 90.008903419667 research
minutes. P3-06 is now **complete** at its declared
[finite cost-forecast scope](derivations/06_cost_forecast_refinement.md).
The [closing record](work_logs/P3_06_2026-10-09_S1.md) gives **90.210938375717**
new research minutes. P3-07 is **complete** at its declared
[bounded paid-reasoning scope](derivations/07_paid_reasoning.md), with
**90.187687312067** observed research minutes. Phase research is
**664.368606879483 minutes**, with **295.631393120517** remaining to the
960-minute floor. **P3-B has passed** at restricted mathematical/local implementation
readiness. P3-08 remains unstarted. Optional paid-selective-feedback recurrence
is recommended before it and remains unselected; see the [gate assessment](checkpoints/B_1.md).
The contribution obligation remains **NOT YET SUPPORTED**.

## Workspace

| Material | Location |
|---|---|
| Author direction | [Scope decision](decisions/2026-10-06_phase_three_scope.md) |
| Tasks and completion criteria | [TODO_v3.md](../TODO_v3.md) |
| Research execution | [Procedure](RESEARCH_PROTOCOL.md) · [Work-item template](templates/work_item.md) |
| Initial literature | [Primary-source orientation](literature/00_orientation.md) |
| Current question contract | [Problem and comparisons](foundations/01_problem_contract.md) · [Exact duties](foundations/01_desiderata.md) · [Machine-readable index](foundations/01_contract.v1.json) |
| Worked boundaries | [Separating examples](foundations/01_separating_examples.md) · [Information](foundations/01_evidence_boundaries.md) · [Composition](foundations/01_composition_boundaries.md) · [Representation](foundations/01_representation_boundaries.md) |
| Observation and refinement | [Records and revisions](foundations/01_observation_contract.md) · [Criterion probes](foundations/01_criterion_probes.md) |
| Reconstructed primary definitions | [Source contracts](literature/01_source_contracts.md) |
| Probability information | [Finite derivation](derivations/02_probability_information.md) · [Primary comparisons](literature/02_probability_sources.md) · [Certificate companion](checks/02_finite_information_audit.py) |
| Representation readiness | [P3-A decision](checkpoints/A_1.md) · [Current contract overlay](checkpoints/A_1.v1.json) |
| Bounded logical uncertainty | [Construction and duties](derivations/03_logical_uncertainty.md) · [Extensions](derivations/03_refinement_extensions.md) · [Sources](literature/03_bounded_sources.md) · [Kernel](checks/03_bounded_logic.py) |
| Counterfactual semantics | [Construction](derivations/04_counterfactual_semantics.md) · [Extensions](derivations/04_selection_extensions.md) · [Sources](literature/04_source_contracts.md) · [Replacement code](checks/04_README.md) |
| Sequential cost forecasts | [Construction and duties](derivations/06_cost_forecast_refinement.md) · [Repricing](derivations/06_price_replay.md) · [Capital comparison](derivations/06_capital_comparison.md) · [Calibration](derivations/06_calibration_scope.md) · [BRIA boundary](derivations/06_bria_boundary.md) |
| Paid reasoning | [Rule and costs](derivations/07_paid_reasoning.md) · [Four-action extension](derivations/07_multi_action_forecasting.md) · [Analytical ordinary control](derivations/07_ordinary_analytic_profile.md) · [Acquisition planner](derivations/07_acquisition_planning.md) · [Closing record](work_logs/P3_07_2026-10-09_S1.md) |
| Mathematics and implementation readiness | [P3-B decision](checkpoints/B_1.md) · [Current 21-duty overlay](checkpoints/B_1.v1.json) · [Optional recurrence advice](work_logs/P3_B_2026-10-09_S1/reviews/recurrence_agent/advice.md) |
| Mathematical Markdown | [Rendering conventions and guard](STYLE.md) |
| Claims and open obligations | [Claim ledger](claim_ledger.md) |
| Setup record | [P3-SETUP](work_logs/P3_SETUP_2026-10-06_S1.md) |
| Research records | [P3-01](work_logs/P3_01_2026-10-07_S1.md) · [P3-02](work_logs/P3_02_2026-10-07_S1.md) · [P3-A](work_logs/P3_A_2026-10-07_S1.md) · [P3-03](work_logs/P3_03_2026-10-07_S1.md) |


## P3-06 completion — October 9, 2026

The [readiness assessment](work_logs/P3_06_2026-10-09_S1/readiness_audit.md)
closes the finite task. One issued scalar has exact recorded numerical
allowances and finite expert, continuous-bin and smooth-action guarantees.
The declared arithmetic adapter separates forecasts, checked residues,
admission times and immutable history. Pending labels remain unscored.

The [repricing analysis](derivations/06_price_replay.md) distinguishes rescoring
old decisions, making new decisions from old estimates and rerunning the
learning policy. It includes represented-profile and coordinated-unit
transfers; arbitrary new objectives do not inherit every old certificate.
The [resource and calibration comparison](derivations/06_calibration_scope.md)
retains the restricted input premises and stronger ordinary alternatives.

The numerical comparison is unfavorable to a predictive-superiority claim:
ordinary Brier aggregation beats both polynomial variants on all four full
development cases, and exact arithmetic has zero Brier loss. The separate
capital method improves the polynomial scores on four shorter prefixes, with
mixed results against ordinary aggregation. Some certificates sharpen simple
bounds, but this is a different question from better predictions.
The [BRIA witness](derivations/06_bria_boundary.md) separates summable forecast
errors and bounded actual-path capital from exact coverage; it has optimal
realized decisions and establishes no practical decision failure.

The [final evidence audit](work_logs/P3_06_2026-10-09_S1/reviews/final_evidence_audit.md)
preserves historical failures and one unavailable whole-draft source hash;
its theorem-section snapshot and associated evidence survive. Exact reviewed
whole-document snapshots are now retained before status edits. No historical
P3-06 minutes were recovered or inferred. The [480-minute checkpoint](work_logs/P3_06_2026-10-09_S1/checkpoint_480.md)
is a progress review, not a later gate or a phase-completion decision.

P3-N01 remains **NOT YET SUPPORTED**, as explained in the
[contribution assessment](work_logs/P3_06_2026-10-09_S1/contribution_assessment.md).
P3-A remains PASS; P3-B–D remain unattempted. All evidence is development.
At the P3-06 boundary, P3-07 had not been started. Its later completion is
recorded below.


## P3-07 completion — October 9, 2026

The [paid-reasoning construction](derivations/07_paid_reasoning.md) acquires
version-bound policy costs, prices selection and execution, and makes a bounded
lower-gain decision against fallback. It separates sunk evidence costs from
continuation value and assesses both a fixed-profile controller and a complete
profile-rebuilding procedure. Its [task audit](work_logs/P3_07_2026-10-09_S1/readiness_audit.md)
maps the exact acceptance criteria and remaining generality limits.

The strongest ordinary controls remain explicit. Analytical class profiles
cost 64,581 resource units versus 1,692,957 for empirical acquisition in the
transparent finite task. Exact computation is cheaper than the audited
controller. A paid finite Bayesian planner repays its construction only in
some long-horizon cases; its prior does not imply per-law safety. The
four-action full-feedback implementation and the dependency construction/search
probe preserve negative total-cost results alongside their valid finite proofs.

The [closed session](work_logs/P3_07_2026-10-09_S1.md) records
**90.187687312067 research minutes** and all excluded intervals. P3-01–06,
including the defensive-forecasting addendum and its evidence, are preserved.
[Contribution status](work_logs/P3_07_2026-10-09_S1/contribution_assessment.md)
is **NOT YET SUPPORTED** under the author's modest-synthesis criterion.
P3-A remains PASS; P3-B–D remain unattempted. P3-08 is unstarted, all experiments
remain development and no final challenge is frozen or exposed.


## P3-B completion and recurrence advice — October 9, 2026

The [technical gate](checkpoints/B_1.md) is **PASS**. Independent targeted
reviews reconstruct the received-source soundness bridge, sourcewise repair
selection, all-current-optimum transport, forecast/feedback distinction and
complete-policy expectation contract. Current local evidence and bounded
admission interfaces support integration; the single combined reasoner is
still P3-08 work. Historical completion sections above retain their original
gate status; this section and the current plan give the latest state.

The five-question assessment gives Q5 the strongest mature answer and
identifies useful model-combination evidence (Q3) and economical selected
feedback (Q4) as the weakest links. P3-N01 remains **NOT YET SUPPORTED**
under the broad modest-synthesis criterion. No empirical superiority or
unrestricted Logical Induction is inferred from the gate.

**Recommended optional recurrence: one Research90 chunk now, before
P3-08, on paid selective feedback.** Target a justified all-issued cost
inequality and an informative break-even regime or precise obstruction.
[The dossier](work_logs/P3_B_2026-10-09_S1/reviews/recurrence_agent/advice.md)
also specifies certificate-delivery recurrence before final freeze and
counterpossible-policy robustness later in the phase. All options remain
unselected and unstarted; none activates R-P3-N01. Direct P3-08 progression
is technically justified under the narrower accepted contract.

The [session](work_logs/P3_B_2026-10-09_S1.md) records **12.208499960967 research
minutes**, with no added gate floor, no historical inference and no parallel
reviewer credit. P3-01–07 and the surviving defensive-forecasting evidence
remain unchanged. P3-A/B are PASS; P3-08 is unstarted; P3-C/D are
unattempted. No final challenge is frozen or exposed.
