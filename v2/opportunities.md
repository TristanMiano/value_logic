# Research opportunity register

Owner: the active research agent, subject to DIR01 and the research protocol.
Updated: September 26, 2026 (UTC).
These are **ranked leads**, not proven gaps or claims of first discovery.
The relevant primary-source descriptions and inspection limits are in
[literature/directional_leads.md](literature/directional_leads.md).

## Working rule

Keep at most five live entries. Reassess after relevant evidence and at gates,
not by generating a new list every session. Rank benefit per unit of effort,
assumption burden, relevance to the author's aims and uncertainty about novelty.
Preserve one reliable result and one exploratory result; existing protocol
allocations apply. A known result is a useful baseline, not automatically a
new contribution. Before a novelty claim, verify the nearest theorem and search
alternative terminology. Record failed searches without treating them as proof
of absence. A lead can be replaced by a better one with a short written reason.

Each entry needs a question, closest antecedent, unresolved delta, smallest
useful result, decisive test, budget/review condition and current disposition.
Budgets below are proposed first-probe allocations, not measured work or changes
to the enclosing task's protected minimum.

## OPP-01 — Loss-grounded residual inference (priority 1)

**Question.** In a small additive/residual fragment, what conditions make
inferences about a measured loss preserve an intended task-value comparison?
What joint information must be retained when proxy components are composed?

**Closest antecedents.** RLL arithmetic (D02); surrogate-risk relationships
(D06); the completed F01/F02 joint-information examples; phase-one
profile/refinement and certificate interfaces. The finite residual/ReLU identity
and generic surrogate-risk bounds are already-known starting points.

**Unresolved delta.** A scoped bridge combining proxy calibration, declared
composition and revisable evidence. No claim that this combination is absent
from the literature has been established. Ordinary rephrasing of a risk bound
is insufficient as the project's main result.

**Smallest useful result/test.** F04 constructs paired proxy/target examples,
including a reversal, and identifies assumptions sufficient to exclude the
reversal. Specify a candidate compositional rule with a concrete countermodel
when one assumption is removed. Carry forward to F08 only if the prospective
characterization adds a nontrivial relation to the known baseline.

**Allocation.** First probe central 30 / high 60 engaged minutes inside F04;
reliable baseline with exploratory composition. Review after the first decisive
example or 30 minutes. Stop expanding the fragment if its operational meaning
is unclear. Status: F04 S1 first-pass evidence exists. The proxy reversal and
shared-source comparison are in [the countermodel note](derivations/01_candidate_countermodels.md).
Priority stays 1, now focused on difference-sufficient source/evaluator certificates.
Affine arithmetic is a closer baseline for shared errors; a new contribution must
add a useful composition/revision or information characterization, not just this
linear-algebra result.

**S2 refinement.** [The nonlinear continuation](derivations/01a_nonlinear_and_reflective_reconstruction.md)
separates bounded nonlinear dependence from exact cancellation and from a useful
tight margin. Finite-ReLU geometry is established background; compare the cost
of producing sharp certificates from a joint source description rather than
claiming novelty for the zero-bias envelope. Next decisive test: a multivariate
case where compact certified information beats independent marginal summaries
at equal evidence access. Priority remains 1.

## OPP-02 — Is the loss/value structure actually learned? (priority 2)

**Question.** Can an ordinary small ReLU MLP's internal computation be
usefully described by task-relevant residuals or loss/value comparisons, in a
way that predicts interventions rather than only decoding outputs?

**Closest antecedents.** ReLU representation results (D07), causal abstractions
and interchange interventions (D08), phase-one hybrid realization and the
F03 theorem agenda. Representability does not establish training or causality.

**Unresolved delta.** A nontrivial, task-grounded correspondence stable under
function-preserving hidden-unit rescaling/permutation, which improves predictions
of interventions over matched alternative descriptions. This is an empirical
hypothesis, not an assumption that a network implements a unique utility.

**Smallest useful result/test.** F04 writes a hypothesis and negative control;
F14 freezes a small probe and F15 runs it. Use ordinary training without injected
logic labels. Compare untrained/shuffled or matched-random descriptions as
appropriate; hold out intervention cases. A deliberately compiled network can
check the method but is not evidence of emergent structure. Record partial or
negative results rather than choosing a new test after seeing the answer.

**Allocation.** F04 design probe central 20 / high 40 minutes; no training in this
direction amendment. Compute and data costs must be forecast separately before
execution. Status: [F04 design](experiments/F04_neural_probe_design.md) and analytical
reparameterization/unused-neuron controls exist; training and alignment search
are unstarted. Priority stays 2 pending causal evidence, not decoder accuracy.

**S2 design refinement.** A positive input-dependent common scaling of action
costs preserves pointwise optimal outputs but can change isolated-cost
interchange predictions. Add the prospective competing high-level description
before any held-out test; do not force an absolute cost representation through
training labels. Existing hidden-neuron gauge controls remain separate.

## OPP-03 — Modest reflective evaluation (priority 3; required capability track)

**Question.** Can an evaluator reason about its own versioned reliability or
future loss while retaining uncertainty and reacting coherently when that
assessment changes the behavior being predicted?

**Closest antecedents.** Logical induction (D04), reflective oracles (D05),
phase-one ranked system assessment and evidence updates. Do not conflate a
staged self-model, randomized fixed point and unrestricted provability reflection.

**Unresolved delta.** A tractable loss-grounded fragment with explicit self-model
semantics and useful update behavior. The full precedents' guarantees have not
been imported; efficiency or unrestricted reflection is not assumed.

**Smallest useful result/test.** Specify one staged self-prediction and one
feedback-dependent hostile case. An informative unknown/interval/randomized
answer is allowed. Prove nonempty semantics and what the update warrants; a
self-endorsement must not be a proof of its own target adequacy. Extend toward a
cyclic construction only after specifying which existence/uniqueness/computation
question is actually being pursued. A bounded staged implementation meets only
the corresponding scoped claim, not the stronger cyclic claim.

**Allocation.** First source-and-example probe central 30 / high 60 minutes in
F04; exploratory lane. Review after the feedback example. Preserve a bounded
reflective route even if the ambitious one fails. Status: F04 S1 supplies a genuinely feedback-dependent versioned example,
with unknown/interval outcomes and a deployable self-bound. Its small algebraic
solution is not unrestricted reflection. Next reconstruction must retain the
common deployed policy, finite-iteration bounds and evidence-version conditions.
Priority stays 3 as a required capability track.

**S2 refinement and baseline.** Performative Prediction (Perdomo et al., ICML
2020; see [source N2](derivations/F04_S2_sources.md)) is a closer local antecedent
for report-induced outcomes. The two-fallible-branch model now admits an exact
common-report optimizer. A better robust score can worsen true-model expected
cost; the paired-budget repair constrains that change and stays nonempty by
retaining the old valid policy. Next: determine whether coarser certificates
preserve this useful guarantee, with no claim of new general safe improvement.
Priority stays 3; reflection remains an active required capability track.

## OPP-04 — Value summaries that survive revision (priority 4)

**Question.** Which proxy/value summaries preserve what future evidence updates
and model-library extensions can make relevant, without retaining the whole
history? Can the necessary refinement be made locally and quantitatively?

**Closest antecedents.** F03's context-family counterexamples, abstract
interpretation/repair sources already in its register, and phase-one read/write
locality and open-library semantics.

**Unresolved delta.** An independently characterized, useful quantitative
summary and selective repair algorithm for a declared family of updates. A
quotient defined by 'all observations agree' alone is not the target result.

**Smallest useful result/test.** Reuse an existing F03 update witness to compare
two finite summaries; derive a constructive additional statistic or explicit
small-family obstruction. Reuse earlier proofs where exact assumptions match.

**Allocation.** First probe central 20 / high 40 minutes if this becomes the best
F04/F08 direction. Do not run it in parallel merely to exhaust the list.
Status: candidate alternative; no new search or theorem claim.


## S3 evidence update — same rankings, sharper tests

OPP-01 and OPP-04 now share a concrete next comparison: finite directional
premises admit small linear certificates; adding one justified coupling premise
can repair a conclusion without restoring the entire source model. Existing
certificate margins can tolerate weighted changes in the bounds they read.
These are standard linear/convex techniques applied to the project's scoped
interface, not verified new open problems. See
[the S3 derivation](derivations/01b_compressed_revision_certificates.md).

OPP-03 gains an exact three-number check interface for the specified two-branch
controller, with explicit counterexamples to general exact evidence updating
and absolute optimization from that interface alone. Do not spend the next
session producing more equivalent toy variants: compare certificate size and
informativeness against the same-information lower-functional route, or
reconstruct the remaining weakest hypotheses. OPP-02 gains a transported
certificate control for hidden-coordinate scaling/permutation, but no training.
The four rankings remain unchanged; no permanent core is selected.
