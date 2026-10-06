# Research opportunity register

Owner: the active research agent, subject to DIR01 and the research protocol.
Last reviewed: October 5, 2026 UTC, through completed F16.
**F16 is complete; a separate Gate C assessment is next and unattempted.**
F15-ND02 remains optional, deferred and unstarted. Earlier dated updates below are historical;
this review refines OPP-02 without reranking the standing opportunities.
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

**Original F04 allocation/status (historical).** Design probe central 20 / high
40 minutes; that direction amendment did not include training. Compute and data
costs required separate forecasts before execution. At that stage,
[F04 design](experiments/F04_neural_probe_design.md) and analytical
reparameterization/unused-neuron controls existed; training and alignment search
were unstarted. Priority stayed 2 pending causal evidence, not decoder accuracy.

**S2 design refinement.** A positive input-dependent common scaling of action
costs preserves pointwise optimal outputs but can change isolated-cost
interchange predictions. Add the prospective competing high-level description
before any held-out test; do not force an absolute cost representation through
training labels. Existing hidden-neuron gauge controls remain separate.

**Current status — October 5, 2026 UTC.** F15 and F15-ND01 are complete;
F15's original **0/5 complete identity intervention support is unchanged**.
ND01 found better individual interventions without retraining and showed that
known cost layouts can miss the complete endpoint's control-advantage
requirement. It did not establish a joint cost representation. Ordinary training
does not require clean eight-neuron cost blocks: the task can depend only on
relative costs. Technical superposition remains unestablished. See the
[ND01 evidence and interpretation](experiments/F15_ND01_results.md).

**Optional deferred continuation.** **F15-ND02, Research90, is unstarted** and
available after F16 or later if selected. On the same five unchanged networks,
jointly select a representation of both cost variables in one common, fixed
subspace geometry. Test held-out single-role and two-donor joint semantic
outcomes with known-structure calibration and matched controls; distinguish absolute adequacy
from control superiority. Repeatability and commutation may be guaranteed
algebraically by the chosen operators, so the scientific target is semantic
behavior, not the imposed algebra. Before any new validation, freeze geometry
and normalization, inactive-coordinate treatment, ranks, budgets, selection and
acceptance rules; fix and save all five fitted alignments. The
[ND01 follow-up plan](experiments/F15_ND01_results.md#8-contribution-protected-effort-and-recommended-next-work)
supplies the detailed allocation and scope. Neither this optional continuation
nor a positive neural result is a prerequisite for Gate C; ND02 is not the
automatic next task. Contributor for this refinement: **ChatGPT (GPT-6 Astra Pro)**.

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


## S4 evidence update — portfolios and a neural certificate fingerprint

Rankings stay unchanged. OPP-01 now has a sharper cost baseline: sparse exact
certificates can have large precision costs, while a compact min-plus program
can represent an exponentially large flat proof list. Unknown source modes may
require separate same-policy proofs; prematurely convexifying premise bounds
loses useful conclusions. These are scoped uses of established linear/convex
patterns, not verified novel fields or a reason to abandon the viable alternatives.

For OPP-02, the [S4 characterization](derivations/01c_certificate_portfolios.md)
gives a predeclared structural fingerprint: nonnegative affine coefficients,
A-transpose times coefficients equal to the query, and a nonnegative intercept.
A learned function could be examined for this pattern without constraining its
architecture. A/source meaning must be fixed before inspecting a convenient
gradient, and independent zero-ReLU masks can fail even for an exact function.
No training, intervention result or alignment success is claimed.

OPP-03 retains one common reflective controller in the case-proof witness.
OPP-04 gains a finite exact update library for fixed source directions, with a
clear distinction between proof reuse, proof-family memory and changed semantics.
Next: use these controls in a focused remaining F04 reconstruction, not another
catalogue of equivalent counterexamples. The prospective experiment remains
unexecuted; no new task is selected by this register update.


### S5 evidence update — source-aware fingerprints

The [new derivation](derivations/01d_source_transport_and_identifiability.md)
keeps OPP-01 first and strengthens OPP-02's discriminator: evaluate certificates
on a predeclared source chart and region, not by the sign of an ambient gradient
alone. A nonempty lift family is evidence of possible numerical justification,
not a uniquely identified causal mechanism. Measure permitted intervention rank
and precision, and retain coherent-cell and affine-offset negative controls.
OPP-03 remains connected through the same report-dependent controller; OPP-04
gains an explicit context-change residual check and alternative-proof transport.
Next useful comparison: fixed versus parameterized queries on the same
source-changing workload, with identical information and explicit proof cost.
No ranking change, new task, novelty claim or neural training is implied.


## F04 completion update — September 26, 2026

Ranking unchanged. OPP-01 has a complete equal-information reconstruction:
finite arithmetic proof bounds agree with lower-value semantics, while source
retention, operation order and nonlinear precision determine useful conclusions.
The next review should not confuse this established duality with novelty.
OPP-02 now distinguishes coefficient proposals from final nonlinear value maps;
no task label, imposed architecture or mathematical certificate establishes
causal use in an ordinarily trained network. OPP-03 retains the two-fallible-
branch example and adds a concrete exact-report discontinuity with a declared
slack-stability alternative. OPP-04 has an exact budget for selective source
revision in the same example. These refine the existing four opportunities,
not create a new catalogue. **Gate A is next and unattempted.**


## Gate A disposition — September 26, 2026

[A_1](checkpoints/A_1.md) keeps OPP-01 as the first development opportunity:
source-aware paired-loss inference with a small checked language. The finite
linear theorem itself is established prior art, not the proposed novelty.
OPP-03's uncertain report-dependent evaluator remains a required interpretation;
OPP-02 remains a falsifiable ordinary-network experiment, not evidence of learning.
OPP-04 informs the one declared source-update question. No ranking change or
extra task is introduced. F05 is to specify semantics for these existing tests,
not expand the catalogue or begin later training. Continuation-value semantics
remains a substantive alternative if exact closure or proof costs favor it.


## F05 S1 — semantic narrowing without a rank change

OPP-01 now has an explicit provisional cost interpretation rather than only
numerical certificate examples. The next useful question is how much of the
source/meaning structure is essential for the three complete uses, not another
catalogue of countermodels. The signed-budget versus clipped-shortfall distinction
and lower-gain counterexample should constrain the later proof rules.
OPP-03 has an uncertain versioned report whose own behavior is evaluated; kernel,
proxy alignment and data-dependent selection assumptions remain external premises.
OPP-02 remains prospective: a native expression's ReLU representation is not a
learned mechanism. OPP-04 is tied to the explicit discrepancy-bound weakening,
which changes one comparison while leaving self-report warrant intact.

No ranking change, new subproject or novelty claim is warranted by this semantic
pass. Continue F05's fresh reconstruction, source/observation interface audit and
minimality review with the remaining protected D time. F06 is not selected.


## F05 completion checkpoint — no ranking change

OPP-01 remains first. A precise native signed-loss semantics now supports
same-source comparisons, visible policy tables, and update-aware relative
summaries. The direct ML check is stronger than a resemblance of activations:
a zero-margin ReLU loss with a proved component enclosure supports a log-loss
comparison including a resource charge. This is an analytic adapter, not a new
loss-calibration theorem or a discovered trained mechanism.

OPP-03 gains two discriminators: expected-report validity can hide a bad emitted
report, and optimizing a proper loss under report-induced outcomes can favor an
invalid self-report. A later rule set should preserve the exact report contract,
not equate improved score with reliable reflection. OPP-04 retains the two-cut
source-update counterexample and a constructive restricted fibre-summary case.
OPP-02 remains prospective: do not infer causal neural structure from these
mathematical constructions. See [S2](foundations/03b_observation_and_revision_audit.md).
F05 is complete, **F06 is next and unstarted**; no broader scope change is made.


## F06 S1 evidence update — ranking retained

OPP-01 now has explicit finite rule traces deriving a shared-source half-unit
improvement from partial contracts and propagating loss comparisons through
native consumers. OPP-03 includes report transfer after an old report loses
validity, plus a specified proof-bound calculator modeled numerically by the
same language. OPP-04 has restricted RHS-only replay and guard/withdrawal
countermodels. OPP-02 remains untested: a mathematically derived proof-budget
function is a hypothesis for neural interpretation, not a discovered circuit.

The next bounded gain is to reconstruct source restriction/withdrawal and the
minimal primitive-versus-derived rule boundary against F05, not add another
large catalogue of toy cases. Reuse the existing signed and hidden-case witnesses
as falsifiers. No ranking change or novel-priority claim is warranted merely
by the number of passing fixture tests.


## F06 S2 — a concrete residual-loss bridge; ranking retained

OPP-01 and OPP-04 now meet in a proof-producing construction: a removed row
can be retained as a residual-violation loss, and the existing argument turns
that loss into a task-specific deterioration allowance. The emitted traces
use the unchanged checking kernel. Signed joint repair can still be stronger;
this is not a claim that independent nonnegative errors retain all information.
OPP-03 supplies the fixed reflective comparison and uncertain proxy bridge.
OPP-02 gains a precise constructed ReLU interpretation and availability-domain
controls, not evidence of a discovered or trained mechanism.

The immediate bounded next question is whether affine sign splitting can be
elaborated through the now-checked discharge and disjoint-hinge machinery while
handling empty branches and one fixed observation-legal policy. Derive and test
that interface before adding a trusted split instruction. Do not begin F07 or
F11. A prospective D32/L2/E8/O10 central and D45/L5/E15/O18 high block is a
planning suggestion, not measured credit or a new task minimum.

Assumption-based truth maintenance is a substantive antecedent for alternative
supports and context-sensitive reasoning, not a newly invented idea here. The
new source note also records the Laskey–Lehner 1989 probability/ATMS abstract as
a further comparison lead; no theorem is imported from its unread full text.
No ranking change or priority claim is warranted by fixture counts alone.


## F06 completion update — September 27, 2026

OPP-01 remains the lead. [S3](derivations/02c_derived_cases_and_completion.md)
connects residual assumptions to executable case and coverage arguments, while
preserving useful negative information in signed alternatives. Its ingredients
are quantitative/lattice and finite linear reasoning, not established novelty.
OPP-04 now has a precise discriminator: semantic source equivalence can coexist
with a weaker replayed trace; retaining and recompiling higher-level proof
structure can recover precision. OPP-03 retains the fixed bound-calculator and
report-dependent policy examples, not unrestricted self-certification. OPP-02
remains unexecuted; no trained network is inferred from a constructed identity.

Next, F07 must reconstruct the explicit local rules, source/typing conditions,
normalization and admitted macro boundary before a general soundness claim.
Do not replace that proof task with more toy cases or a new architecture. The
standing task minimum and next-session forecast remain prospective obligations.

### F07 S1 evidence update — ranking unchanged

OPP-01/04 now have a general native soundness reconstruction and a proof-relative
premise-violation allowance theorem, not merely individual demonstrations.
The [graded note](derivations/03b_graded_soundness_reconstruction.md) makes a
specific overrun loss and its propagation explicit. The next bounded work is
producer/request/observation contract reconstruction; it is not a new novelty
claim or an instruction to expand the calculus prematurely. OPP-03 remains a
conditional report-dependent interpretation. OPP-02 is still untested in an
ordinarily trained network; arithmetic soundness does not establish causal
participation. No direction or task order is changed.

## F07 S2 checkpoint — no ranking change

OPP-01/OPP-04 now have a producer-level contract audit: a receiver checks what
an assumption-loss computation claims to have returned, while case-local
proof alternatives can survive more withdrawals than a static global family.
OPP-03 retains separate checks for self-report validity, paired improvement
at the current source, and historical performance after an actual source
change. The latter needs a drift premise. Fault-aware evidence handling is a
useful baseline comparison, not a newly established novelty claim.

Keep the final F07 reconstruction focused on the combined theorem's exact
fragment. The uncertainty envelopes require premises about which evidence can
fail; deriving or learning those premises remains a distinct future question.
No neural experiment, stronger core selection or change of task is introduced.

## F07 completion checkpoint — September 28, 2026

OPP-01 remains the leading calculus question, with OPP-04 evidence-sensitive
reuse and OPP-03 bounded reflection served by the current soundness/receiving
proofs. No opportunity ranking is changed merely by test counts. The report-
update countermodel sharpens the current-query requirement; it does not resolve
the broader reflective aim. The neural probe is still unstarted. F07 is complete
at its declared scope; F08 is selected, with its exact conjecture to be chosen
prospectively under its own forecast. No new novelty claim is made.
Research author: ChatGPT (GPT-6 Astra Pro).

## F08 completion checkpoint — September 30, 2026

OPP-01 remains the lead; no ordering change is justified by test counts alone.
F08's unit-directed completeness theorem and full-source obstruction give the
calculus a precise boundary. OPP-04 now has a constructive optimal-retention
result for fixed RHS families and withdrawals, plus exact source-substitution
criteria and quantitative transfer. OPP-03 has an exact fixed-law report
boundary and explicit distinctions between least warrant, robust loss and
paired improvement. The geometry refinement connects source violations to
loss sensitivity without treating small numerical error as inherently small
value loss. These are conditional mathematical gains, not empirical premises.

A bounded future F08 refinement could ask which complete dual alternatives
can be discarded while preserving every allowed future revision and withdrawal.
The present complete catalogue is a sufficient baseline; minimal retention
and practical search cost are unestablished. A discriminating next step would
be an exact parameter-domain dominance criterion with a rational witness when
an alternative is necessary. Estimate D 45 central / 90 high, review at 45;
smallest useful result: one correct pruning criterion and one unsafe-pruning
counterexample. This is an optional lead, not a started task or novelty claim.
Integrated search remains for F11 after F09/F10 and Gate B. Neural work is
unstarted. Research contributor: **Codex (GPT-6)**.

## F09 completion checkpoint — September 30, 2026

OPP-01 remains the lead. F09 distinguishes exact logical/evidence interfaces
from numerical resemblance, and strengthens the comparison through component
geometry and joint-profile information. OPP-02 gains explicit affine controls
and nonlinear/bounded failure modes for future representation studies; this is
not evidence about a trained network. OPP-04 gains a paper reconstruction for
affine certificate transport while retaining context, cases and proof-minimum
parents. Its commutation with RHS replay is not established. No ranking change
or new novelty claim follows merely from these additional results.

The clearest optional F09 continuation is to implement and check the
[S8 construction](derivations/05h_affine_certificate_transport.md). Closest
checked antecedents are F08's forward-path lattice equality producer and F09's
common-scale trace compiler. The general unit-specific affine algorithm is
currently paper-only. Discriminating tests should include one-way edges,
heterogeneous scales, nonzero origins, nested residuals, negative allowances,
lexical lets and exact all-case query pairs. Benefit: a reusable producer that
preserves existing certificates under declared affine coordinates without
integrated proof search. Prospective central/high effort: **E 35/60, D 10/20,
O 5/10 minutes**; review after E35 or the first unresolved proof-shape failure.
Smallest useful stopping point: a checked affine lattice/endpoint bridge
producer plus the two blind-relabeling counterexamples repaired through the
unchanged receiver. Full S8 acceptance would cover all native rules. This is
an offered optional continuation, not a started task or a substitute for F10.

The 60-minute derivation floor proved useful: required comparisons were ready
earlier, and the remaining block produced stronger paper results and assumption
checks. F10 is next, unstarted. Gate B, integrated F11 search and neural work
remain unattempted. Research contributor: **Codex (GPT-6)**.

## F10 completion checkpoint — September 30, 2026

The ranking remains, but the [external audit](literature/02_core_audit.md)
narrows the expected contribution. OPP-01's most useful next investment joins
OPP-04 in a bounded loss-model revision study: compare selective checked
retention against full retention, a current-best proof, fresh solving, and
cached-proof/replacement search. Parametric LP, ATMS, provenance, incremental
maintenance, revision-sufficient memory proposals and whole-certificate
coverage are close antecedents. Generic reuse or pruning alone is not the
candidate contribution; the application result and total-cost comparison matter.

[Package A's original forecast](literature/02a_research_calibration.md#3-prospective-research-packages)
was **12 central / 24 high engaged hours**, including a **3 / 6-hour
checkpoint**, for one supplied model and finite revision/query workload.
Useful outcome: a reproducible preservation/cost result or a scoped obstruction.
Automatic production is missing from F08's supplied-candidate replay and is an
early implementation risk. A more defended result is **24 / 48 hours total**.
Distinctiveness is uncertain; these figures do not price all remaining v2 work.
The earlier D45/90 pruning lead is now subordinate to choosing a workload:
all-RHS exactness can require every vertex in an explicit affine catalogue,
whereas finite whole-proof coverage admits an established greedy baseline.

OPP-02 remains a required, separate empirical uncertainty. Reuse established
causal-alignment methods and held-out tests; successful patching still needs
matched controls. The [neural package](literature/02a_research_calibration.md#3-prospective-research-packages)
forecasts **6 / 12 hours** for an informative pilot, with a **2 / 4-hour
checkpoint**; the original stronger-interpretation estimate is **20 / 40 hours total**. The new
log-cost and transported-projection diagnostics inform F14, not a training run.
OPP-03 remains conditional on supplied self-model/revision premises; choosing
which commitments should change is a distinct normative question.

L45 was reasonable for the targeted audit plus these optional comparisons.
Future work should record an early core-ready checkpoint and pair usage
readings with measured milestones before estimating a weekly allowance.
No new permanent quota, core, phase or gate is selected. Gate B is next,
unattempted. Research contributor: **Codex (GPT-6)**.

### Author's subsequent breadth-and-evidence amendment

The preferred expansion policy is now the
[cumulative 4/8/16/32-hour ladder](literature/02a_research_calibration.md#3-prospective-research-packages).
Each additional block should buy substantive scope and stronger support in
roughly equal measure. The illustrative path adds revision handling, bounded
self-assessment and a scoped neural question while deepening evidence across
the growing result set. The original A/B forecasts above remain effort-risk
anchors; their higher-effort tiers are not instructions to keep the same scope
and spend every additional hour defending it. Reforecast the next increment
at each checkpoint. Rankings, required gates and current completion claims
are unchanged; this amendment starts no research package.

## Gate B readiness checkpoint — September 30 local / October 1 UTC, 2026

[B_1 passed](checkpoints/B_1.md) after fresh same-agent reconstruction. This
supersedes the preceding F10 next pointer: **F11 is selected and unstarted**.
OPP-01/OPP-04 remain the preferred integrated revision/loss lead; OPP-03 keeps
its explicit self-model contracts and OPP-02 remains an empirical uncertainty.
No contribution candidate is promoted to established novelty or performance.

The recorded cycle-II allocation was D/L/E 80.11/8.71/11.17 and R/X 60.95/39.05.
Prospectively use **D35/L10/E55 and R60/X40 for cycle III**, reviewed after F13
and at Gate C. The E-heavy deviation is justified by implementation, differential
checks and model evaluation. Preserve existing task floors and the approximate
25% recurrence reserve. Apply the author's breadth/evidence ladder to each
future package, with fixed-scope central/high forecasts kept distinct from
cumulative scope milestones. Gate B itself has no protected floor and starts
no later package. Research contributor: **Codex (GPT-6)**.

## PLAN01 — contribution selection before implementation

The author-approved [amendment](decisions/2026-09-30_novelty_and_recurrence.md)
selects **N01, unstarted**, superseding B_1's F11 pointer. The starting lead
remains OPP-01/OPP-04's joint-loss-evidence revision question, with OPP-03's
bounded self-assessment family and the required OPP-02 pilot retained. N01
must compare the closest ordinary-method combination and may replace the lead
if another bounded question is better justified; no lead is a proven open problem.

An assessment of NOT YET SUPPORTED or DISPLACED distinctiveness must assign a
named 60/90-minute recurrence or further-work chunk. Gates C/D require supported
project-level novelty as well as technical evidence; component novelty quotas
are not imposed. Grow breadth and support together at cumulative 4/8/16/32-hour
checkpoints, retaining earlier clocks and task floors. This is a change to the
selection and advancement rules, not new evidence promoting any opportunity.

## N01 — consumer-relative evidence, with stronger ordinary controls

The [contribution plan](contribution_plan.md) completes target selection.
OPP-01/OPP-04 remain the leading integrated question, but generic caching,
query preservation, robust preference and checked arithmetic are established.
The quartic fixture has a twelve-expression ordinary closed form; all twelve
are needed for uniform exact threshold answers in the stated affine model.
An optional priority policy needs nine, and a changed order needs twelve.
This is a useful, narrowly scoped distinction, not a supported novelty claim.
Gaussian quadrature, factorized provenance, complete-source access and a
two-endpoint post-observation reduction are required baseline controls where
their hypotheses apply. More states or more flat proof roots alone add little.

**R-N01-01 is open.** F11/C1 is the selected E60 producer/reference feasibility
chunk. C2 supplies differential/cost evidence; C3 compares a justified richer
scientific consumer with a bounded self-assessment/update protocol. Do not
spend recurring chunks trying to recover full-vector affine savings already
disproved in the seed. Preserve OPP-03's meaning and OPP-02's ordinary-training
pilot; neither was attempted here. The 4/8/16/32-hour ladder still grows breadth
and supporting evidence together. Contributor: **Codex (GPT-6)**.

## N01/C3 — revision across programs and consumers

The [two-hour recurrence](work_logs/N01R_2026-10-02_S1.md) is complete at
refinement scope. It leaves the four standing opportunities and their ranking
intact, while sharpening OPP-01/04 and OPP-03. Scientific action restrictions
must survive quadrature and known-output projection controls. Calibrated
feedback distinguishes fixed points from actual execution and nonlinear
summary information, but ordinary fractional/conic optimization, splitting,
finite interpolation and stronger policy selection repair the examples.

The optional two-bit program gives a more concrete lead: an old complete loss
law can remain unchanged while a program edit changes from improving to
worsening. The [C22/C26 derivations](derivations/08_n01_evidence_consumers.md)
identify the missing joint-source information and its ordinary repair.
Twenty-five [primary comparisons](literature/04_n01_recurrence_comparison.md)
make decision-state compression, exact policy vectors, metareasoning, risk
comparison and program-cost certificates mandatory comparison families where
applicable. Their reuse is encouraged; their existence limits generic claims.

**R-N01-01 stays OPEN; novelty NOT YET SUPPORTED.** Select C1/F11 E60 on the
16-state/three-query scientific negative control, then C2/F12 cost and revision
evidence. Use those costs to choose a richer F13 family; its D60 is still due.
The next decisive evidence is an implemented matched comparison, not another
unbounded theory-only N01 recurrence. If both richer routes are displaced,
prospectively scope C4 to reconsider the question. OPP-02's neural pilot remains
unstarted. Broaden questions and supporting evidence together; no new lead is
promoted as an established open problem. Contributor: **Codex (GPT-6)**.

## F11/C1 and four-hour checkpoint — October 3 local / October 4 UTC, 2026

The [implemented comparison](verification/README.md) supplies missing
producer/reference feasibility evidence for OPP-01/04. Opportunity rankings
remain unchanged. Selected-proof reconstruction can miss a true closed
threshold; one timing observation was slower than fresh search. Ordinary
coefficient preprocessing competes with equally checked receipts. The program
adapter broadens OPP-03 preparation, but ordinary formulas solve its fixed
family exactly. This improves the next discriminator, not an open-problem claim.

**R-N01-01 OPEN; novelty NOT YET SUPPORTED.** Select **C2/F12, fresh E60**,
central D0/L0/E60/O10=70, high D10/L0/E90/O20=120, unstarted. Smallest useful
gain: a declared revision-family comparison showing where reconstruction
loses and what total checked-answer costs each route incurs. Include
source/build/storage/checking/fallback and cache conditions. At close, select
a richer F13 application or prospectively assign C4 if no credible useful
distinction survives. F13 D60, reflection and the neural pilot remain due.
[Checkpoint and stopping conditions](checkpoints/POST_B_4H_1.md).
Contributor: **Codex (GPT-6)**.

## F12 opportunity update — October 3 local / October 4 UTC, 2026

**OPP-01/04:** the [F12 comparisons](verification/F12_results.md) lower the
priority of repeated proof reconstruction as a candidate advantage. Ordinary
coefficient catalogues preserve exact bounds and repay setup over the measured
72-query sequences; cheaper selected coefficients can preserve decisions with
weaker bounds. This is a strong existing-method baseline, not project novelty.
Checking/receipt work consumes much of the pipeline, so basis-search reductions
alone do not imply comparable task-value gains. Generic cache optimization is
lower priority than a meaningful application question.

**OPP-03:** prefer the actual-program/edit/consumer route joined to staged,
versioned self-assessment for **R-N01-01/F13-A**. Keep the scientific case and
the evaluator's influence on later reasoning explicit. The rival cyclic
feedback route retains C3's nonlinear-admission/calibration/stability burden
and strong ordinary reductions; coding its solved loop alone has low expected
contribution value. The [selected question, forecasts and stop condition](contribution_plan.md#10-f12-close-and-application-selection)
require broader useful scope plus stronger evidence, with central/high 100/160
engaged minutes and a fresh D60. Renew the closest-work comparison for the actual
claim; neither the old loss-law counterexample nor an ordinary caching gain
is enough. If no useful distinction emerges, select C4 reconsideration or
named further evidence before F14. **Novelty NOT YET SUPPORTED; R-N01-01 OPEN.**
F13 is selected but unstarted. The neural pilot remains a later distinct task.

## C4 ranking update — October 4, 2026

Contributor: **Codex (GPT-6)**. The [broader contribution assessment](contribution_review.md)
supports modest synthesis and small technical applications relative to checked
work. R-N01-01 closes at that scope, with F16 reopening if its delta is displaced.
Worldwide priority and stronger practical claims remain unestablished.

**OPP-01/04:** prioritize consumer-appropriate revision/retention: exact
numeric answers, useful tolerances and refusal, and consequential decisions
are different requirements. C4 now supplies price-family ranks, minimal repair,
sharp/general equal-price recovery and a conditional sampling bridge. The
strong ordinary method gets the same source, certificates, recovery tools and
acquisition opportunities. Proof-reconstruction speed remains a negative
control. More ambitious work should study jointly noisy old/new information,
unequal prices or stateful outcomes, with measured acquisition and decision cost.

**OPP-03:** preserve staged, versioned evaluator influence from F13. The new
consumer calculations clarify which observations later reasoning needs; they
do not establish unrestricted cyclic self-justification or empirical validity.

**OPP-02:** select F14's existing ordinary-training neural probe alongside one
small revision challenge, then F15 execution. F14 is **unstarted**, research90,
central/high 105/155 engaged minutes, R/X55/45. Do not multiply experimental
families merely because C4 added optional theorems. The
[4/8/16/32 additional-hour ladder](contribution_review.md#7-effort-ladder-breadth-and-defense-grow-together)
grows substantive scope and defense together. Keep the separate cumulative
POST-B-1 clock and its [eight-hour checkpoint](checkpoints/POST_B_8H_1.md).
