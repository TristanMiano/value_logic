# Phase Three: Reasoning About Unresolved Mathematics

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Updated October 7, 2026 UTC.

**P3-01 and P3-02 are complete at their declared scopes; P3-A is next and unattempted.** The author has set a
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
$p_t=\Pr_t(\varphi)$, its estimated loss is

$$
\widehat L_t=10(1-p_t),\qquad p_t=1-\widehat L_t/10.
$$

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
No phase-three learner, final experiment or gate is established by these tasks;
the contribution obligation remains **NOT YET SUPPORTED**. The separate next
item is P3-A, which must assess representation readiness and alternatives.

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
| Claims and open obligations | [Claim ledger](claim_ledger.md) |
| Setup record | [P3-SETUP](work_logs/P3_SETUP_2026-10-06_S1.md) |
| Research records | [P3-01](work_logs/P3_01_2026-10-07_S1.md) · [P3-02](work_logs/P3_02_2026-10-07_S1.md) |
