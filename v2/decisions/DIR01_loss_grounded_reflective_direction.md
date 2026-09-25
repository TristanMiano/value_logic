# DIR01 — Loss-grounded value, reflective uncertainty, and neural interpretation

Effective September 24, 2026 (America/Los_Angeles). Status: adopted research
direction at the author's request; **not a chosen calculus or proved result**.
Base: `15608f26a9d07fbd346fc105a583d2723f995be0`.
F03 remains complete at its original audit scope. F04 remains next and unstarted.
This decision supersedes blanket deferral of reflection and neural interpretation
in current planning; it does not revise phase-one results or historical logs.

## 1. The organizing question

Can a tractable calculus reason about pragmatic value through task-relative
losses, while remaining uncertain about its own evaluations and revealing
structure actually learned by neural networks?

The inspiration is Ruspini's utility-oriented synthesis; the mechanistic
starting comparison is Rational Lawvere Logic (RLL), not merely its number range.
The project is not claiming that lower training loss is final truth, that any
specific objective is true utility, or that every neuron implements this logic.
The [source orientation](../literature/directional_leads.md) distinguishes
checked descriptions from theorem imports requiring future work.

## 2. Loss as an accessible proxy, not a definition of ultimate utility

Use ML losses, rewards, empirical risks and resource costs as concrete semantic
candidates for something more general: the value of model use to an agent.
Track the distinction among an intended task criterion, its measured/learned
proxy, the training objective, and the evidence that connects them. The proxy
and its evaluator are themselves eligible objects of assessment and revision.

An illustrative objective is `J_q(m) = sum_j w_(q,j) L_(q,j)(m) + C_q(m)`.
It is a possible construction, not the chosen algebra. Terms require compatible
units, stated weights and meaning. Prediction error, a KL-based belief penalty,
resource cost and a constraint penalty can occupy different terms; this does
not identify their epistemic or normative roles. Keep vector or partially
ordered alternatives when scalarization discards a relevant distinction.

A proxy-to-value claim requires its own assumptions, counterexamples and evidence.
A useful theorem target relates proxy regret to task regret under explicit
calibration/misspecification conditions; mere improvement of the surrogate is
not such a theorem. Target uncertainty can be represented without inventing a
known ground-truth utility. Hard constraints need not be finite tradeoffs.

## 3. RLL-like mechanisms, with cost/value meaning

Give a serious first comparison to additive resource accounting, residuals,
order, arithmetic sequents and checkable derivations. For finite nonnegative
`a,b`, the additive residual `max(b-a,0)` is exactly `ReLU(b-a)`.
This elementary identity motivates a test; it is not a novelty claim or evidence
of how a trained hidden unit is used. RLL's infinity conventions and guards
must not be replaced silently with floating-point arithmetic.

Compare nonnegative cost semantics, signed-value encodings, and directly signed
alternatives. Boolean predicates should be recoverable where justified as a
fragment or special observation, not the only intended interpretation of all
quantities. Nonnegative inference-loss bounds can coexist with signed values.
Do not select a candidate solely because its range is unbounded, or reject a
better justified alternative merely because its syntax differs from RLL.
Document what each operation means for a task and which result it preserves.

## 4. Reflection is an active capability target

The calculus should support at least one explicit form of reasoning about its
own evaluator, loss estimate, inference behavior, or predicted reliability.
A staged self-model is a feasible starting fragment; it must name the system's
own versioned computation and have an observable consequence for later reasoning.
Relabeling an unrelated external model as 'self' is not sufficient.

Also test a genuinely feedback-dependent case in which an assessment influences
the behavior being assessed. Distinguish quotation/self-description, empirical
self-prediction, probabilistic introspection, and unrestricted proof reflection.
Acyclic staging may be an initial implementation, **not a permanent prohibition
on self-reference**. Cyclic proposals must state their fixed-point, partial,
randomized, or other semantics and show a nonempty interpretation. Existence,
uniqueness, convergence and computability are separate questions.

A minimal success target is a bounded reflective example that admits unresolved
self-assessment, updates it after evidence, and does not automatically certify
itself merely because it predicts its own success. Logical induction and
reflective oracles are comparisons, not off-the-shelf components or imported
guarantees. More ambitious reflection remains an explicitly tracked opportunity.

## 5. Modesty in object reasoning and in the metatheory

Permit uncertainty about outcomes, costs, model adequacy, proxy alignment,
proof search, evaluators and axiom choices wherever the selected semantics can
represent it meaningfully. Do not encode all these uncertainties by one
uninterpreted confidence number. State which questions the current language can
express and which remain external assumptions.

Ordinary conditional proofs in a named metatheory remain legitimate. Record
separately a formal theorem, empirical calibration, an agent's uncertain belief
about a theorem, and its belief about a proof checker. This distinction does
not freeze the metatheory as metaphysically privileged. Comparisons between
metatheories or evaluators can be scoped model-use questions. Neither 'unknown'
everywhere nor deleting all definite conditional consequences is the objective.

## 6. Discover neural structure; do not build in the desired answer

Maintain an explicit search for value/loss computations within ordinary learned
models, starting with small ReLU MLPs when informative. A deliberately compiled
network is useful as a positive control but does not show spontaneous learning.
Separate (i) exact representability, (ii) observational decoding, (iii) causal
participation, and (iv) stable task/value interpretation across perturbations.

Before an empirical claim, state the proposed internal variables and predicted
intervention effects on held-out task loss or behavior. Use suitable ablations
or interchange interventions and controls such as untrained networks, shuffled
labels, alternative decompositions, and function-preserving permutation/positive
rescaling of hidden units. Choose controls relevant to the claim, not a checklist
of mandatory large experiments. Distributed features are allowed; a neuron need
not have a privileged semantic label. Preserve negative findings.

Train the unconstrained baseline on the declared ordinary objective, not on
hidden logical labels or extra regularizers that force the proposed semantics.
An imposed variant must be labeled a separate comparison. This is a bounded
interpretability probe within phase two, not a requirement to build a large LLM.

## 7. Direction selection and phase-one continuity

The agent may pursue the best-supported tractable opportunity without seeking
approval for every lemma. Keep the [opportunity register](../opportunities.md)
small and current. Rank expected conceptual/empirical benefit against effort,
assumption burden and novelty uncertainty; easy algebra alone is not progress
on the central question. Preserve both a reliable route and a genuinely
uncertain route using the existing protocol's allocations.

Phase one remains a baseline for licenses, evidence modes, fallback, open-ended
succession, composition and selective revision. A phase-two value calculus
should preserve a useful restricted interface where possible and demonstrate
which additional conclusions the richer value structure enables. It need not
inherit `K_3`, exact external masks or an acyclic-only global architecture.
Failure of a proposed extension should narrow or redirect it, not erase the
original goal or rewrite the completed phase-one record.

## 8. Implementation in the roadmap

F04 compares proxy mismatch, typed self-assessment and a neural-structure
hypothesis alongside existing joint-information cases. It designs rather than
runs the final neural experiment. Gate A records how its shortlist serves these
objectives. F05-F09 develop the selected scoped semantics, reflective example,
proxy/fragment relationships and one substantive characterization. F13 includes
a self-assessment case. F14-F15 reserve a small unconstrained-network probe.
Gate C requires an honest disposition of that probe, not a positive discovery.

F03 need not be reopened to install this direction. A needed new source audit is
scoped inside the active task or given a named addendum with a prospective
budget. The prior protected minima, recurrence rules and historical credit
remain unchanged. A claimed new core, a passed gate, or a causal discovery still
requires its stated evidence; this decision supplies none of those results.
