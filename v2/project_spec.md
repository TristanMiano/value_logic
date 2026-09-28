# Phase Two Project Specification

Version: F07 first soundness reconstruction, September 27, 2026 (UTC).
Status: **F01–F05 complete at task scope; Gate A passed at readiness scope; F06 complete at rule-development scope; F07 partial; the semantic core remains provisional**.
Authoritative queue: [TODO_v2.md](../TODO_v2.md).
The dated sections below retain historical dispositions; the current gate decision is [A_1](checkpoints/A_1.md).
Execution: [RESEARCH_PROTOCOL.md](RESEARCH_PROTOCOL.md).

## Question and commitments

What semantic objects and inference rules permit useful reasoning from pragmatic
value without assuming possession of final metaphysical truth?

The commitments are epistemic nonfinality, pragmatic use and revision of models
under declared tasks/error or reward/resource conditions, and investigating
value as the primary semantic object. They do not uniquely determine an algebra.
A scalar, a structured object, an ordering, a contract, a probability model,
three-valued states, and a neural implementation remain optional choices.
Ordinary conditional mathematical proof is allowed in an explicit metatheory.

Phase one remains a completed realization. Its paper, experimental outcomes,
code, and historical completion records are preserved. Reusing a result requires
its hypotheses; phase-two compatibility is a research question, not a mandate.

## Active direction after the F03 audit

[DIR01](decisions/DIR01_loss_grounded_reflective_direction.md) is the current
steering decision. Losses and rewards are operational proxies for broader value,
not automatically adequate utility measures. Compare RLL-like arithmetic with
explicit cost/value meanings and admit signed alternatives. Require a scoped
self-assessment capability that can remain uncertain and be revised. Keep
stronger self-reference eligible subject to explicit semantics, rather than
inheriting phase one's blanket exclusion of cycles.

A small probe of a normally trained ReLU MLP will test a proposed internal
value/loss computation without forcing that structure during training. Its
status must distinguish representation, decoding, and causal evidence. These
requirements narrow the question for F04 and the later selected core; they do
not assert that any such structure has already been discovered.

The agent has bounded discretion to pursue the best-supported opportunities
under the protocol. Earlier mentions of neural interpretation and self-revision
as deferred branches are historical: their bounded forms are now active;
large-scale implementation and a general reflection theory remain later work.
F03's evidence and time totals are unchanged. No F04 result or gate is added.

## Initial operational requirements

The [F01 derivation note](foundations/01_requirements_and_separating_examples.md)
contains eight worked examples and conditional requirements R01-R09. They test
cost versus accuracy, task changes, joint and sequential composition, hidden
dependence, incomplete/conflicting evaluation, toy axiom systems, unbounded
values/recodings, and information-dependent attainability.

Candidates must state which of these queries they admit and what inputs a
consumer can access. Distinguish exact answers, valid bounds, underdetermination,
adequate decisions at a declared tolerance, and explicit scope restrictions.
Always returning unknown on fully specified admitted examples is not the desired inference capability. Conversely, a
particular summary's failure must not be promoted into an impossibility for
all scalar encodings or all value-based systems.

Positive sufficiency results are required alongside counterexamples. Current
examples show that scalar comparisons, scalar minima, local error/sensitivity
bounds, or a task-specific joint statistic can sometimes suffice. They do not
require preservation of every raw model detail, and information sufficiency is
not yet an efficiency result. The
[reconstruction note](foundations/01a_reconstruction_and_information_contracts.md)
sharpens the distinction between exact recovery and useful inference: covariance
can certify a tolerated bottleneck bound without determining its exact value;
fixed-cost changes can preserve bounded-regret choices; and local incompatibility
can have a precisely characterized approximate repair. Support, joint dependence,
error aggregation, endpoint attainment, and tail premises remain explicit.

## Result targets, not completed claims

After F01, F02-F04 compare concrete candidates and check their literature and
countermodels. Gate A chooses a justified development question. F05-F10 then
seek operational semantics, meaningful inference rules, a soundness proof, a
nontrivial characterization or constructive restricted result, and exact
fragment comparisons. Gates B and C additionally require executable reasoning,
adversarial review, and prospectively specified empirical evidence before paper
assembly. None of these later results is asserted by the present fixture suite.

The final paper is `paper_v2.md`, created only when the queue's evidence gates
permit it. The claim ledger distinguishes mathematical demonstrations, tests,
philosophical commitments, design choices, and deferred targets.

## Historical artifact development (current status is at the top)

The paragraphs below retain the sequence of earlier checkpoints; their former
'next task' statements are not the active pointer.

[Notation](notation.md), [claims](claim_ledger.md), the F01 derivation note,
[finite fixtures](checks/f01_examples.py), [fixture results](checks/F01_results.json),
and the [first session](work_logs/F01_2026-09-20_S1.md) bootstrap this phase.
The [continuation record](work_logs/F01_2026-09-21_S2.md),
[reconstruction fixtures](checks/f01_reconstruction.py), and their
[results](checks/F01_reconstruction_results.json) complete F01's evidence.
[Timing](time_ledger.csv) credits 60.243613 derivation minutes across the two
sessions. The full protected D60 obligation is met, without treating elapsed
time as evidence of mathematical soundness.

**F02 is complete.** The [candidate comparison](foundations/02_candidate_semantics.md)
retains four concrete proposals: fixed-task scalars (S), aligned profiles (P),
continuation-value transformers (T), and non-probabilistic guarantee fronts (G).
Each has multiple worked examples, a common comparison table, and explicit
information, units, scale and composition assumptions. The
[reconstruction supplement](foundations/02a_candidate_reconstruction.md) supplies
positive repairs and countermodels rather than choosing a winner. Dedicated
F02 discovery passes 124 checks. The [completion record](work_logs/F02_2026-09-22_S2.md)
and time ledger credit 61.118295 derivation minutes across S1 and S2.

**Next task: continue F03 — external foundations audit.** Its first recorded
session now supplies [eight core source checks and three targeted supplements](literature/01_foundations.md),
[worked mappings](literature/01a_import_boundaries.md), and a bibliography.
The L60 obligation is not yet satisfied. The earlier F02 source checks retain
their historical scope and are not retroactively counted as F03 time.
All gates remain unattempted; the repair queue is empty.

The completed F02 task did not implement the later reasoner, complete the F03 literature
audit, claim novelty, select a permanent value carrier, or run a frozen empirical
challenge. Contract inversion, a full scientific-model substitution theory,
inquiry policies, and neural interpretability remain deferred branches.

## F02 comparison implications, not new fixed commitments

A fixed-task scalar can remain sufficient for additive reasoning. Joint nonlinear
queries can require alignment; sequencing can require downstream-task responses;
hard multidimensional budgets can require attainable sets rather than all
weighted optimum values. The candidate note supplies exact scoped examples,
including an optimized response map that forgets a menu's mean-constraint
capability. None requires preserving every raw model detail.

Before selecting a core, compare extensional meanings with any extra witness or
syntax retained, identify permissible observations and shared uncertainty, and
check closure of admitted downstream tasks under composition. No universal
probability, bounded-value, scalarization, or policy-recovery axiom is adopted.

### Implications of the F02 reconstruction

Four closure questions remain distinct: algebraic closure, preservation of legal
implementation witnesses, closure of downstream task families, and robustness of
finite-precision encodings. A mathematical map can satisfy the first without
preserving the others. Fixed weighted scalar costs admit useful exact compressed
kernels; full hard-budget menus retain distinctions their weighted optima lose.
Observation timing and common latent choices remain part of the interpretation.

The finite T expression class has a scoped extensional characterization under
freely supplied finite stochastic affine primitives, not a claim about every
fixed physical library. G has unit-aware approximate substitution laws under
its declared independent-choice semantics. Bounded coordinate encodings can be
useful when operations and retained offsets match the query; naive absolute
squashing and rounding is not equivalent. These results are candidate-level
comparisons and inputs to F03/F04, not a replacement for their selection gate.

## F03 partial-audit implications

Existing quantitative, program-semantic, ordered and optimization theories supply
substantial antecedents. Reuse remains conditional: total versus substochastic
kernels, finite versus infinite max–min representations, complete versus finitary
semirings, possible-outcome versus feasible-budget polarity, and exact substitution
premises cannot be conflated. The 2024 generalized quantitative-algebra source
shows that amplifying operations are not ruled out merely by the 2016 framework's
max-metric rule, but it does not waive relation-preserving substitution or other
proof-system hypotheses. These findings constrain future imports without changing
the four candidates or selecting a permanent core.


### F03 S2: a numerical proof language is not the whole operational semantics

The [continued audit](literature/01b_proof_system_audit.md) adds Rational Lawvere
Logic (CSL 2026) as a fixed-arithmetic antecedent. Finite signed-polynomial and
budget-query adapters clarify what can be represented, without selecting that
logic as the project core. Finiteness, zero/infinity conventions, typed units,
nonempty compatible evidence, and a common available strategy witness remain
explicit obligations. Relational substitution and semiring algorithm imports
also retain their exact source conditions. The new numerical fixtures do not
establish a full proof checker or a new soundness/completeness theorem.

F03 remains partial. F04 and Gate A are not advanced by these source checks.


### F03 S3: the proposed Lawvere-to-value bridge

The [bridge audit](literature/01c_lawvere_value_bridge.md) separates three
questions: pragmatic interpretation of existing numerical semantics, encoding
signed values in that semantics, and changing the algebra itself. Finite signed
polynomial comparisons compile to guarded nonnegative polynomial sequents;
Abelian logic supplies an existing signed additive/lattice antecedent. These
are possible resources for later design, not an adopted calculus.

A further option keeps two-sided value profiles while grading replacement loss
nonnegatively. Its task-relative directed loss obeys a triangle bound, even
when absolute values are unbounded. It does not recover missing dependence,
certify unobserved performance, or supply a common implementation witness.
The finite polynomial import uses S12 Theorem 11 directly; a retrieved-text
normalization inconsistency is recorded rather than silently implemented.
F03's protected literature obligation remains incomplete. F04 and Gate A remain
unattempted, and the original project motivation and phase-one results survive.


### F03 S4R1: belief penalties and broader task value

The [belief/KL audit](literature/01d_belief_kl_objectives.md) checks the new
author-supplied lead against primary sources. A Bayesian KL functional is one
nonnegative belief object, not every imprecise belief. Proper lsc penalties on
a finite simplex generate monotone, shift-preserving continuation-cost maps;
finite signed costs need no universal bound. Combining beliefs retains shared
arguments, normalization offsets and source labels when the query needs them.
KL itself does not obey the prior replacement-distance triangle, and general
lsc beliefs are not closed under every pointwise RLL connective. No existing
RLL theorem is silently extended to logarithms or available-policy witnesses.

The source manifest now has8 core sources and 10 targeted supplements.
This session's33 checks bring F03 to135 passing local tests. The
[session record](work_logs/F03_2026-09-23_S4R1.md) credits 3.301479 additional L minutes;
cumulative L is 30.831357, leaving 29.168643 of L60. The interrupted unclosed
attempt receives no credit. **Continue F03; no core or gate has been selected.**


## S5 import-contract refinement (September 24, 2026)

The [context audit](literature/01e_belief_value_import_contracts.md) distinguishes
a belief penalty from the family of values obtained by optimizing against
linear costs. That family can forget nonconvex dependence assumptions needed
by later belief additions; a declared context family supplies a restricted
repair. Exact rational log/KL enclosures provide analytic side certificates
for numerical comparisons without adding an unproved logarithmic logic.

One S16 parameter-convexity statement is rejected as written, with an exact
finite witness and a joint-convexity replacement. The prior nonnegative KL and
signed-cost adapters remain valid at their scopes. No core or gate is selected;
F03 remains partial. The restored root README and prior research are preserved.


## F03 S6: consolidated source-use handoff

The [source-use note](literature/01f_consolidated_source_handoff.md) and
[register](literature/F03_import_contracts.json) state eligible finite interfaces,
required hypotheses and stronger inferences not obtained from each source.
The register is not an automatic proof checker. The four candidates remain
alternatives; source compatibility has not selected a winner.

The directed profile adapter now states the exact monotonicity/subhomogeneous
gain condition, including substochastic finite maps. The pointwise arithmetic
adapter distinguishes a valid numerical expression from an lsc belief and an
attained optimizer. These refine C41/C42 without weakening past claims.
F03 remains partial under its measured source-review requirement; F04 has not
started. Root motivation, phase-one results and existing source history remain
unchanged.

## S7 checked source-rule interface

The [source-rule audit](literature/01g_checked_source_derivations.md) separates
unconditional arithmetic residual chaining from guarded cancellation for finite
signed pairs. Its two finite certificates are derived in a subset of S12's rules;
the checker does not implement full RLL, source completeness, KL analysis or
policy synthesis. S10 substitution keeps all variable-relation premises, while
S13 signed sequents use a different polarity and structural rules. No candidate
is selected by these comparisons. The eighteen-source list remains unchanged.

[The S7 record](work_logs/F03_2026-09-24_S7.md) reports 207 passing F03 checks and
41.675988 cumulative L minutes; 18.324012 of L60 remain. Continue F03.


## S8: source context and witness boundaries

The [context/witness audit](literature/01h_context_and_witness_audit.md) adds a
finite context-elimination obstruction and an explicit extended-distance
optimality-certificate existence boundary. Positive extension and finite-coupling
constructions preserve useful restricted cases. These concern source use, not a
new candidate selection or an F04 gate review. There are 222 passing dedicated
F03 checks. [S8](work_logs/F03_2026-09-24_S8.md) records 46.253886 cumulative
L minutes; 13.746114 of L60 remain. Continue F03.


## S9: proposed calculus attributes and theorem portfolio

The author's request for a positive literature comparison is addressed in the
[agenda](literature/01i_calculus_desiderata_and_theorem_agenda.md). The proposed
priorities are operationally explicit, useful composition; sufficient information
for the admitted tolerance and contexts; faithful fragment translations;
auditable effective reasoning; and attainable witnesses for action claims.
Local precision repair and revision are additional practical goals.

The most attractive ambitious targets are an independently constructed,
resource-scoped characterization of observable value loss, or a constructive
minimal adequate abstraction. A belief/value representation preserving admitted
updates is a further target. Existing variational-preference and local-repair
results are antecedents, not completed project contributions. The proposed
[structured agenda](literature/F03_calculus_agenda.json) adds no fixed axioms.
F04 and GateA retain responsibility for selecting the actual development question.

There are21 registered sources (8core,13supplements), 236 passing F03 tests, and
51.058238 cumulative L minutes; 8.941762 remain. F03 stays partial and selected.
No core, gate, full repository verification or new CI outcome is asserted.


## F03 completion and continuity with phase one

The [closing comparison](literature/01j_phase_one_literature_and_novelty.md)
separates the original broad value-first program from its quantitative
licensing realization. It maps licensing to controlled I/O and assurance,
composition to graded program logics, and revision to dependency-based
computation. The exact synthesis is potentially useful; no priority claim is
proved. The region and joint-refutation adapters are elementary scoped results,
not replacements for the frozen phase-one profile semantics. The strongest
proposed next results concern useful value composition and non-definitional
characterizations of contextual loss or adequate-information repair.

F03 source-audit evidence and L60 are met. F04 is selected, not executed;
Gate A and all later gates remain unattempted. The earlier audit notes retain
their historical status. The root README receives only status/link updates;
phase-one mathematical and experimental artifacts are unchanged.


## F04 S1: loss-grounded discrimination and bounded self-feedback

The [new countermodels](derivations/01_candidate_countermodels.md) instantiate
DIR01 rather than freezing new primitives. Shared uncertainty can make a
comparison much more definite than individual losses. The precise finite affine
criterion is an established-pattern baseline, not by itself a novel calculus.
A calibrated proxy still needs a pairwise task-alignment warrant. Self-feedback
can be given a nonempty, computable bound semantics for a versioned controller,
while retaining uncertainty and distinguishing a changed policy from a newly
measured fixed one. Neural semantics must survive transported coordinate changes
and predict intervention effects; [the ordinary-training design](experiments/F04_neural_probe_design.md)
is prospective only.

The scalar/profile/transformer/front comparison is information-scoped: no
candidate is eliminated merely for not containing evidence that was never
provided, and a scalar concluded comparison is not conflated with separate
per-model scalar inputs. RLL-like comparisons and desirable-difference/lower-value
reasoning remain viable starting routes. Broader self-reference, nonlinear
source propagation and selection of a core remain research obligations.

[S1](work_logs/F04_2026-09-25_S1.md): 29 constructed tests pass, alongside unchanged
F02/F03 totals 124/256. F04 remains partial at D4.065999; 55.934001 D minutes
remain. The restored root README and phase-one results are untouched.


## F04 S2 scoped reconstruction — September 26, 2026

F01–F03 and DIR01 retain their completed scope; F04 remains partial.
The [S2 note](derivations/01a_nonlinear_and_reflective_reconstruction.md) establishes
F04-C09–C15, not an adopted calculus. It separates exact invariance, finite
boundedness and decision-useful precision for shared nonlinear costs. Both
viable routes get identical joint information. Reflection now permits two
fallible branches, joint uncertainty and one executable report; a finite
paired-deterioration constraint makes policy revision nonempty and quantitatively
controlled. Expected, robust, report and realized quantities remain distinct.

The prospective neural discriminator must compare observationally identical
input-dependent cost scalings before attributing absolute internal costs.
No network was trained. Cumulative F04 D is 7.592175 minutes; D60 is unmet.
No general complexity, proxy-calibration, source-validity, novelty, F05 or gate
result follows from these finite constructions. Next remains F04.


## F04 S3 checkpoint: compressed paired-revision evidence

[Derivation](derivations/01b_compressed_revision_certificates.md) and
[session](work_logs/F04_2026-09-26_S3.md). A fixed two-branch self-report family admits an
exact three-scalar report/deterioration check summary. It does not preserve
absolute optimization or every subsequent evidence/weight update. Retain sound
old certificates under genuine source restriction; selectively reopen a missing
directional bound when it blocks a useful comparison. Finite nonnegative linear
certificates give a checked arithmetic bridge, not a selected general calculus.
A target/proxy discrepancy can remain unbounded in level while its differences
support a useful policy comparison. Neural claims remain conditional structural
controls, not discovered trained mechanisms. Scope/units/version metadata are
not discarded by numerical compression. F04 remains partial (17.758820 D minutes);
Gate A and F05 are unstarted, and F03's completed scope remains unchanged.


## F04 S4 — certificate size, precision and reusable value functions

The [S4 derivation](derivations/01c_certificate_portfolios.md) treats the same
finite source information in the arithmetic and functional routes. Individual
proof sparsity does not imply numerical robustness, a small fixed proof library,
or a data-selected coverage guarantee. Case proofs establish a single deployed
policy across all admitted modes; they do not let the policy observe that mode.
A fixed finite CPWL map with concavity, positive homogeneity, monotonicity and
query-compatible translations is exactly a finite envelope of linear certificates.
This is a scoped structural result, not an adopted calculus or an identified
mechanism in a trained network. Runtime affine-piece checks are weaker and must
handle zero-activation conventions carefully. The numerical smoothing examples
are not exact arithmetic proof certificates.

F04 remains partial at **33.451225 measured D minutes**. The session meets its
requested D15 aim; **26.548775** of task D60 remain. Existing phase-one and
completed F03 conclusions are unchanged. Gate A and F05 remain unstarted.


## F04 S5 — source semantics versus numerical encoding

[The source-transport note](derivations/01d_source_transport_and_identifiability.md)
keeps the source matrix, input chart, target query and region assumptions explicit.
Invertible numbers do not justify subtracting upper-bound premises. A valid
network bound may have negative local derivatives while admitting a nonnegative
source/domain proof; a valid proof need not identify the actual computation.
The certificate and source-set routes agree on the fully specified finite-linear
fragment. Their practical differences depend on retained information and allowed
updates, not different access to the same source. The fixed-query assumption is
not dropped for input-dependent/bilinear policy objectives. No network is trained.
F04 remains partial at **48.782837 D minutes** with **11.217163** remaining;
Gate A and F05 are untouched. F01–F03 and the phase-one results retain their scope.


## F04 completion: two supported routes, no selected core

The [final reconstruction](derivations/01e_equal_information_completion.md) is
an equal-information comparison. Source-indexed arithmetic certificates and
lower-value/continuation formulations agree on the nonempty finite-polyhedral
linear fragment. Their natural closure, evidence-update interfaces and proof
costs differ; exact scalarization before composition can lose a useful guarantee.
A finite ReLU envelope can preserve an operational margin without reproducing
an entire nonlinear return function. Fixed-query representation results do not
automatically extend to varying queries and evidence together.

The common reflective example has two fallible branches, a fixed deployable
report-policy, uncertain proxy alignment, and explicit deterioration budgets.
The exact least-report map has a fragile degenerate corner. A denominator guard
or a declared positive self-prediction allowance supplies a restricted stability
alternative; an allowance is not automatically the exact report contract.
Empirical source adequacy and trained neural causal meaning remain unestablished.

F04 is complete; **Gate A is the next item and has not been attempted**. The
preferred *review proposal* is a small checked loss-comparison language with
source-preserving continuation semantics as an explicit alternative/reference.
Gate A, not this note, adjudicates foundation-selection readiness. No F05 syntax,
permanent calculus, full reflection principle or architecture has been adopted.


## Gate A disposition — current

Gate A passes only at foundation-selection readiness. F05 should investigate a
small checked loss-comparison language while retaining source-preserving
continuation semantics as an explicit alternative. Give nonempty, source-aware
semantics to a paired guarantee through composition and one specified update;
include the report-dependent policy and distinguish source uncertainty, proxy
alignment and approximation. The three required semantic interpretations and
rejection criteria are in [A_1](checkpoints/A_1.md). No F05 syntax, completed
soundness theorem, neural training or permanent carrier is introduced here.


## F05 provisional semantic choice — S1

The [source-aware loss core](foundations/03_provisional_core.md) is selected for
initial development, not frozen permanently. It uses finite rational CPWA syntax
with finite signed-real meanings at each model and potentially unbounded ranges
across models. Its basic query is new loss minus old loss <= a signed budget,
relative to nonempty, scoped, versioned joint source conditions. Nonnegative
residual shortfall is derived and does not replace strict improvement margins.

Keep unit conversions, shared-source identity, lexical binding, visible-policy
information, source-set validity and paired proxy discrepancy explicit. The
three principal interpretations are shared-source additive composition, the
versioned SELF-MIX controller with uncertainty and an evidence weakening, and a
source-parametric quadratic continuation with a component-local affine enclosure.
A direct absolute-error-plus-resource instance additionally connects the native
syntax to a conventional learning loss. These are modeled costs, not final utility.

Countermodels must be feasible in the declared source. Malformed contexts,
empty sources, stale versions and unavailable policy information are not truth
values or evidence of target-world failure. The executable audit only evaluates
rational hypothetical models in its documented subset; it does not decide global
validity or replace F06–F08. The richer continuation alternative and rejection
conditions remain explicit. Existing phase-one and F01–F04 results retain their
original scope. Gate A remains valid at readiness; F05 continuation is next.


## F05 completed semantic contract — S2

The current specification is [03_provisional_core.md](foundations/03_provisional_core.md),
with the [S2 reconstruction](foundations/03b_observation_and_revision_audit.md).
The following clarify its interpretation without replacing the selected language:

- A finite visible-policy table supplies one normalized rational lottery per
  available observation. The complete action-cost interpretation keeps hidden
  cases separate. An average over observations is a different question from a
  guarantee conditional on each observation; no hidden-case action oracle is added.
- Current equal-exposure loss comparisons may use relative costs. This is an
  optional exact query abstraction, not deletion of the evidence needed for
  future updates, absolute adequacy or changed use multiplicity. Convex compression
  is limited to its stated linear/static queries. A point map absorbs arbitrary
  evidence updates exactly only with the proved fibre-saturation condition.
- A randomized emitted self-report is evaluated on each positive-probability
  branch. A zero weighted positive shortfall enforces this; clipping after averaging
  can conceal an invalid emitted report. The interpreter retains the stated joint
  execution law, including random-seed dependencies.
- The reflective, shared-composition and nonlinear/enclosure examples remain
  nonempty with their explicit source/proxy assumptions. The native absolute-error
  loss and the component-level analytic log-loss enclosure illustrate distinct
  ML connections. No loss is declared ultimate utility and no logarithm primitive
  or training result is asserted.

The core, units and notation are synchronized. Finite value objects remain CPWA;
source interpretation and empirical warrant are not replaced by their scalar
summary. F05 D totals 60.320288 minutes. Ninety F05 checks pass, but universal
consequence still receives its mathematical meaning independently of testing.
The continuation alternative, all source/observation falsifiers and Gate A's
readiness scope remain unchanged. **Next: F06, unstarted**; F07 soundness and
later characterization/empirical tasks are not accomplished by this specification.
Older status paragraphs above are historical checkpoint records.


## F06 S1: first operational inference interface

The [rule register](derivations/02_inference_rules.md) introduces syntactic
comparisons `C;h |- new <=[b] old`, distinct from F05 semantic validity. The
same context, source meanings, live case and units must be retained. Negative
bounds express improvement; physical cost and resource aggregation still need
their stated plan interpretation. New relative comparisons can follow from
partial component contracts without complete component evaluation.

Implemented audit rules cover supplied finite traces, lattice/residual composition,
explicit conversions and same-schema RHS replay. Full source transports and
withdrawal repair remain mathematical obligations, not completed implementation.
A proof-budget CPWA function can be reified as a versioned numerical self-model;
its predicted output is distinct from the validity of its premises. The fixed
report-dependent controller remains uncertain and requires paired proxy evidence.
The continuation alternative, DIR01 objectives and Gate A conditions are unchanged.
No F07 soundness/complete-search/learning result is asserted by this checkpoint.


## F06 S2 — revisable arguments and numerical assumption loss

The [S2 reconstruction](derivations/02b_source_transport_and_withdrawal.md)
extends supplied-proof checking rather than changing F05's semantic meaning.
A useful consequence can survive even when the new source is not contained in
the entire old source: only the leaves used by its argument need current
replacements. Reconstructed proofs keep new contexts, actual source identities
and every live case. Numeric observation labels do not themselves certify a
transported policy's observation channel.

Removing a numerical premise a<=eta can instead produce an explicit allowance
res(eta,a). A single-case compiler carries such allowances through every local
S1 constructor using ordinary checked proof steps. This supplies a magnitude-
sensitive loss interface: an extra bound on the residual, or an independently
specified expectation model, can warrant a useful conclusion. It does not turn
an unknown premise into a fact, replace correlated signed evidence with an
optimal abstraction, or automatically preserve structural probability domains.

Same-query alternatives are retained for future withdrawal; a numeric snapshot
frontier does not promise exact response to every later evidence revision.
Six old instruction tags have explicit expansions into a ten-tag basis.
No automatic sign splitter, general optimizer, learned neural interpretation
or F07 result is claimed. F06 is partial, with 60.046135 recorded D minutes
and 29.953865 remaining. Gate A keeps its existing readiness scope.


## F06 completion: the derived-case interface

The [S3 reconstruction](derivations/02c_derived_cases_and_completion.md) extends
supplied finite proofs, not the meaning of F05's source/value objects. A numerical
sign partition is eliminated into the existing local instructions. A strict
infeasibility ray derives the surviving guard in a nonempty parent; it does not
create a live empty context. Incomplete coverage can retain a quantitative loss.
Policies remain fixed under their declared observation contract, and source
meaning, unit and evidence revisions are not interchanged.

The positive-weight coverage macro and the direct two-hinge construction have
explicit proofs, scope restrictions and sharpness witnesses for their stated
information class. Original signed source arguments can remain strictly more
precise than softened allowances. Fixed-trace replay is safe under its old
conditions but need not match fresh recompilation's bound. Both alternatives
are retained rather than deleting stronger historical information.

The S1 checker and F05 semantics are unchanged. F06 now meets its rule, example,
countermodel and D90 obligations; F07 remains the required general soundness
review. The continuation alternative, empirical proxy assumptions and learned-
neural interpretation remain provisional or untested as previously recorded.

## F07 reconstruction boundary

[The native soundness theorem](derivations/03_soundness.md) covers the sixteen
accepted F06 instruction tags on finite typed expressions and nonempty current
source cases, with finite real values at each assignment (unbounded domains are
allowed). The proof does not define validity as checker acceptance. It includes
lexically captured normalization, signed budgets and exhaustive case aggregation.

The [graded theorem](derivations/03b_graded_soundness_reconstruction.md) permits
numerical assumption violations to enter a proved cost allowance. Empirical
source validity, intended-loss meaning and observation-legal deployment remain
explicit premises. A new request receiver binds a valid returned root to its
requested pair, domain, unit and sufficient strength. No new inference tag or
permanent semantic choice is introduced. F07 remains partial; source-producer
and operational-contract reconstruction continue before D90/task completion.
