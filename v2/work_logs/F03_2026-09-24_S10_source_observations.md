# Source-comparison notes — block 1

These are working source-comparison observations, not independent new calculus
results. Base: 48b11819230bb856ce03fed28a5161ff5e276e5b.

## I/O logic versus licensed use

Makinson–van der Torre (2000), author manuscript PDF index 4, §3.2,
Observation 1, was visually checked: simple-minded output is characterized by
SI, AND, WO. §5.1 adds cumulative transitivity only in the reusable variants.
Thus output production not being truth-preserving detachment, and requiring a
separate policy for output reuse, are established themes. The authors explicitly
frame their project as a way to use classical consequence around a transformation,
not simply a different assignment of truth values.

Phase-one `07_core_calculus.md` §§2–4 makes a different object central:
`Assess(s,e,q,P)`, where risk/task/fallback live in q and current evidence lives
in s. Its grant is not an unqualified object-language assertion. The proper
comparison is I/O operations versus the *licensed output* layer, not an identity
between `Assess` and `out_1`. Formula strengthening in SI cannot be mapped to
arbitrary domain restriction: restricting a domain can raise conditional risk.
Likewise CT cannot discharge the project's bridge/tube or new-root-certificate
conditions. A scope-erasing translation would not inherit the source theorem.
This is meaningful design differentiation, but not evidence that nonfactive
output or controlled reuse was first introduced by Value Logic.

## SPIBB versus the fallback atom

Laroche et al. (ICML2019), §2.3 Theorem 2, states a zeta-approximate improvement
bound with probability 1-delta under the baseline-constrained policy class.
The finite MDP, dataset, count threshold, discount and bounded-return conditions
are part of the guarantee. §2.5 expressly distinguishes the relaxed variant:
it retains the convergence statement, not the same SPI theorem. The PDF index 3
was visually inspected; the Theorem 2 statement was read in parsed index 2.

Phase-one `08_metatheory.md` Theorem 8 uses the certificate inequality
`sup(U_e)+Delta <= inf(U_F)` to preserve an improvement atom. This is not a new
principle of safe baseline improvement. It is a generic *consumer* of evidence,
whereas SPIBB specifies a producer of a particular kind of evidence and policy.
To specialize loss to minus return, the model, dataset, policy, common event and
confidence meaning must match; separately obtained confidence statements cannot
be turned into a simultaneous guarantee without a union bound or joint evidence.
Genericity buys representation of more certificate modes, not stronger statistics.
The paper does not imply that every fallback has low loss, just a comparison to
one explicitly specified baseline. Phase one's separate absolute adequacy atom
is therefore useful but not a contradiction of the source's relative objective.

## Actual phase-one arithmetic, rather than a strawman

`07_core_calculus.md` §2.2 already permits risk/value preorders and scalar or
vector acceptable regions. `08c_proof_carrying_plans.md` §§2–3 already composes
payloads, quantitative grades and certificates; its path-sensitivity rule is
not just a three-valued Boolean gate. Accordingly the accurate description is
*quantitative evidence and graded computation under a qualitative authorization
interface*, not “phase one contains no value semantics.” The next phase can
make value relations the inference interface without erasing these results.

`08_metatheory.md` Theorem 1 and Proposition 2 are a typing split plus finite
meet on a three-element chain. This is an algebraic identity with the conjunction
fragment of strong Kleene logic, not a novelty claim for the truth table or a
transfer of all of K3 proof theory. Its Theorem 3 is observable-relative
pigeonhole separation. Its Theorem 5 is conditional on change-completeness, with
necessity additionally assuming path realizability: the substantive question is
which of those premises the concrete evaluator satisfies, not just the abstract
iff. The finite independent-atom completeness claim should not be described as
completeness of quantitative risk inference.


---

# Source-comparison notes — block 2

## Revision locality is a concrete specialization, not a new general dependency theory

Acar–Blelloch–Harper, *Adaptive Functional Programming* (POPL2002), §§4 and6,
Theorems1/5: the source constructs dynamic dependency traces, gives a
change-propagation cost bound and states equality with from-scratch evaluation
up to a location renaming. Theorem5's statement and the discussion that its
full proof is in the companion report were visually checked at PDF11. Its
modifications concern input locations of the declared store; the source does
not certify an arbitrary external mutable evaluator or every value-logic update.

Phase-one `08b_audit_repairs.md` §1.1 explicitly separates current provenance
from read dependencies. §§2–4 give concrete finite read sets, including empty
collection-index reads, and the event-write obligations; Theorem1 then proves
same projection gives same complete diagnostics, with current validity and
normalization included. These do real work for this evaluator, but the proof
pattern is deterministic dependency locality. Phase-one `08_metatheory.md`
Theorem5's graph equivalence adds path realizability for the exact chosen
observable. It does not imply every conservative edge can change a grant, or
that the existing implementation already attains Acar's runtime bound.

One promising extension therefore has to add something genuinely discriminating:
quantitative approximate recomputation plus preserved certificate modes, or an
effective least dependency abstraction for an explicitly restricted language.
Merely adding another dependency graph would not constitute that extension.

## Proof-carrying plans already have a graded layer

Phase-one `08c_proof_carrying_plans.md` §1.2 itself identifies Hoare logic,
proof-carrying code, certifying algorithms and quantitative types as antecedents.
Its Theorem1 assumes typed edges, total deterministic transformers, accepted
primitive evidence, sound local constructor rules and canonical certificate
construction. A topological induction establishes erasure and a checked root.
Its Corollary3 grants a request only after that *root* claim and all other
required atoms pass. This is stronger than blindly conjoining leaf grants, but
not a new general proof-erasure theorem. The local sound-rule hypothesis does
not automatically produce target-world validity for empirical leaves.

The source-defined bundle is useful heritage for phase two: keep payload,
quantitative grades and evidence distinct even if a richer value relation
becomes central. A source numerical theorem can be placed in G_c/C_c only with
its hypotheses; the old WF/profile adapter can remain a consumer. This is an
explicit architectural connection, not a proposal to freeze phase-one carriers.

## Completeness and minimality need their original query scope

Phase-one Theorem3's four-way observable separation is a deterministic-decoder
counting argument. The diagnostic quotient concerns the allowed profile queries;
singletons distinguish realizable atom vectors, and ternary independence is
needed for the 3^n worst case. Likewise the profile completeness theorem concerns
a finite independent-atom preorder in a fixed instantiation fiber, not the
completeness of risk inequalities or an optimization procedure.

These are useful internal correctness results. A stronger future characterization
must identify a representation or metric *independently* and prove equality with
what permitted compositions/updates distinguish, or give an effective construction
of a sufficient abstraction. Defining equivalence as equality on all queries is
not by itself a new full-abstraction theorem. The prior S19/S21 comparisons make
this distinction material rather than merely terminological.

## Keep the two orders distinct

Source abstract-interpretation precision is an information order, not automatically
the phase-one refusal/open/support chain used for requirement conjunction.
Narrowing an uncertainty set can resolve open either to supported or to refuted.
Consequently loss of current support after new evidence is not automatically a
violation of abstract-interpretation monotonicity. A nonempty region's set of
possible Boolean threshold outcomes has the natural reverse-inclusion information
order; truth-order meet remains a different operation. A joint profile may
exclude simultaneous satisfaction even though no individual requirement is
uniformly refuted. That observation motivates a small scoped bridge calculation,
not a silent redefinition of the frozen phase-one `Refused` outcome.


---

# S10 source observations: graded program judgments and checked evidence

PCC, inspected original POPL 1997 scan, printed 106/108/109 (PDF 0/2/3):
its trusted consumer validates a supplied proof for the consumer's safety policy.
That policy and the implementation of checking are part of the trust boundary;
the producer need not be trusted. This is an exact antecedent for separately
checked root certificates, not a theorem about statistical adequacy or future
survival of a certificate. Phase one 08c section 1 already names PCC, Hoare,
refinements, and quantitative types; the audit should not present this connection
as absent from its original design. The separate y/g/K bundle is a deliberate
integration choice. Induction over a DAG and erasure of annotation are standard
patterns. Interesting further work is what the checked annotation preserves
across defeasible evidence updates, scopes and estimator assumptions, rather
than proving an erasure identity again under a renamed notation.

GHL, arXiv:2007.11235v2, sections 1-2: the paper already gives a unified
parameterized system combining program assertions, a preordered monoidal grade,
and underlying effectful computations, with an erasing map. It is a closer
antecedent to phase one's quantitative composition layer than a list of isolated
cost-analysis precedents. Its examples include probability-of-postcondition-
failure bounds. That quantity must not be identified with a tolerance on mean
loss or with the failure probability of a procedure that estimates mean loss.
Phase one's q and Modes_q can distinguish all three; importing a source requires
choosing which has been placed in the grade.

The bounded-loop language is not a solution to arbitrary cyclic self-endorsement.
Its loop counter is evaluated once, and the displayed quantitative loop rule
requires a statically justified number of repetitions. Open-ended model/library
succession is a change of evidence state between requests, not an execution loop
inside the object language. The paper's future work on dependent grades/partiality
must not be treated as a proved generalization. Likewise, phase one's dependence
of G_c on context and input is not automatically an instance of one fixed grading
monoid; a translation must fix a suitable fragment or provide the richer typing.

The visible GHL overview displays an apparent disjunction in the precondition
of a max-assignment example. That isolated rendered line is not needed here and
is not imported. The parameterization and later formal rules, once inspected,
are the relevant evidence; no broad theorem is rejected on this rendering alone.

Concrete research consequences for phase one: an evidence-relative outer
assessment can consume a checked graded judgment, while preserving distinct
status/trace/requirement queries. A richer grade need not redefine Granted as a
scalar. Conversely, categorical denotation and generic grade syntax do not by
themselves supply the phase-one current-validity and correction normalization.
The distinction is one of mathematical interface and assumptions, not a claim
that existing program logics assume metaphysical access to reality.

## Exact formal-interface reinspection

GHL 3.4 Table 1 specifies a preordered monoid, sound primitive command and
procedure specifications, and a consequence rule with stronger precondition,
weaker postcondition, and larger grade. Sequential grades combine in program
order. Definition 9 requires an erasing map that preserves identity, composition,
grade coercion, effect embedding and relevant coproduct structure. Theorem 5.1
asserts that a denoted derivation erases to the denoted program. Thus even the
combination of grading, proof denotation and erasure is an existing general
construction, not merely several independent precedents. The comparison with
08c Theorem 1 is exact at the interface level but not an established translation
of the full stateful license system into a GHL structure.

A source soundness theorem is conditional on correctly interpreted primitive
specifications. Phase-one 08_metatheory Theorem 15 is similarly explicitly a
schema: Support_m implies Target_w only on C_m, or in the probability sense of
the particular statistical mode. Its one-line instantiation is not itself a new
statistical guarantee. SPIBB can supply a nontrivial candidate generator and
specific high-probability return bound inside such a mode; it does not establish
arbitrary risk estimators, unknown objectives or future library completeness.

Phase-one Thm 10 is the finite unary-preorder entailment characterization:
P entails Q exactly when each requirement of Q follows from some requirement
of P, assuming every downward-closed supported set is realizable in the fixed
address fiber. Its separation witness is the closure of P. This has a standard
order-theoretic proof and excludes genuine conjunctive interactions by assumption.
It is not comparable in scope to complete equational deduction for arbitrary
quantitative terms. Thm 11's coarsest quotient similarly follows from equality of
all selected observations by definition. The instantiated finite query family is
useful; a new full-abstraction result must identify an independently described
semantic distance or representation rather than rename this quotient.

Two restrictions survive any purported phase-two refinement: validity/evidence
mode must remain distinguishable from an arithmetic bound, and absence of a
constructor's failed assumptions must not be inferred from a small numeric grade.
A wider numeric carrier alone does not recover either missing distinction.


---

# S10 source observations: assurance is a much closer neighbor

The targeted Assurance 2.0 check is important enough to qualify the novelty
assessment, not merely add another citation. The 2021 manifesto already separates
plausible evidence from deductive argument steps, records residual doubts, and
calls for updates and explicit defeaters. The 2024 defeater report gives a concrete
true/false/unsupported assessment system. The separately inspected 2024 semantic-
automation paper checks object/property/environment consistency, adequacy and
predeclared-domain completeness using an ASP translation. These comparisons
undercut any broad claim that structured, typed, defeasible, evidence-grounded
assessment is peculiar to this project.

There is nevertheless no identity of the complete operations. In the 2024
report sections 2.2-2.4, an ordinary reasoning block represents an implication
from subclaims and sideclaims to a parent. A false antecedent does not refute
that parent; its propagated assessment is unsupported. A phase-one required
profile is a conjunction of actual authorization requirements. Its meet can
therefore be refuted when one required condition is refuted. Treating the latter
as a rule for rejecting arbitrary consequences would deny the antecedent; treating
the former as the phase-one meet would suppress a required authorization failure.
The two interfaces share a ternary carrier but differ on a two-input witness.
Exact versus ordinary defeaters likewise must remain explicit. The analogy to
lapse versus rebuttal is strong, not a free transfer of every rule.

The manifesto's 'indefeasibility' is a practical judgment about examined doubts
and consciously accepted residual risks. It expressly does not claim certainty.
It must not be caricatured as metaphysical infallibility merely to make phase
one's non-finality look novel. The project's stronger universal StableNow over a
specified continuation class is a different, explicit quantified property. Its
finite-prefix theorem says when a state-only certificate cannot establish that
property. This is a standard indistinguishability argument instantiated to the
model-use setting, not a refutation of practical assurance confidence.

The ASP paper's completeness check concerns the author's declared object/domain
inventory. This is neither completeness of a numerical proof system nor a theorem
that the inventory exhausts future possible models. That distinction maps cleanly
to phase-one CertUndom(g,Eval_s(q)): a scoped claim can be rigorously supported
without making an unscoped global claim. The missing step is not solved by merely
renaming inventory completeness as finality.

The strongest defensible characterization of phase one is thus a particular
formal synthesis, with concrete instantiated proofs and an implemented witness,
not a new family of truth algebras and not the first general framework to track
fallible assurance. Its explicit request factorization, comparison profiles,
negative-read footprints, certificate-mode boundary, and open-library continuation
semantics remain a coherent combination worth comparing. Whether the exact
combination was previously published has not been established by this search.
A broad logic's ability to encode it would not alone negate the usefulness of its
abstractions; conversely, lack of an exact name match would not establish novelty.

## Direct source-to-phase-one theorem consequences

GHL's refinement map already erases annotated derivations to their underlying
program. Therefore an erasure theorem for the phase-one y/g/K product is primarily
an instance-level verification obligation. The genuinely new work would need to
characterize scope/evidence/update preservation for the actual new representation
or show a useful computational consequence, rather than add another empty grade.

SPIBB's approximate baseline theorem has a slack parameter zeta. In loss
orientation it gives R(candidate)-R(baseline)<=zeta, on the stated probability
event. This does not satisfy a requested positive improvement Delta merely by
calling it 'safe improvement'. The algorithm's estimated advantage must dominate
its uncertainty penalty plus Delta, or an appropriate separate improvement
certificate must be supplied. A joint difference guarantee does not by itself
supply separate marginal intervals for the frozen endpoint comparator. Candidate,
baseline, sampling and policy-class scopes must survive the certificate adapter.

The same caution applies to certainty parameters: a failure probability for a
program's postcondition, an upper bound on expected task loss, and a confidence
failure probability for an estimator of that loss are three different claims.
All can be written with nonnegative numbers; their common range does not make
them substitutable. The phase-one context and mode fields already provide places
to preserve this distinction. A value-first phase should exploit, not erase it.


---

# Post-interruption source comparison — broad objectives

This closes a literature-comparison block, not a new calculus selection.

Phase one's q already includes a risk/value preorder, acceptable region, explicit
fallback, resource conditions and evidence modes. Its 08c bundle separates
payload, quantitative grade and certificate. Calling it merely a truth table
would overlook much of its value-related semantics. Its public inference target,
however, is a finite-stage permission, not yet arbitrary value-term consequence.

The I/O source (Makinson–van der Torre 2000, author PDF §3.2, Observation 1,
PDF4) explicitly supplies SI/AND/WO for one output operation and keeps reusable
variants separate. This precedes non-truth-detaching output. It does not license
strengthening a population domain, which can raise conditional risk (phase-one
08a Theorem1/Counterexample3). No scope-erasing I/O encoding is imported.

GHL (arXiv:2007.11235v2, §§3.4,4,5, Definition1/9, Theorem5.1) precedes the
combination of program semantics, assertions, preordered-monoid grades and
erasure. Its grade can denote resource use or a postcondition failure bound;
those are not estimator confidence or task-risk tolerance. Phase-one 08c is a
specific certificate/assessment integration, not a new generic erasure theorem.
Context-dependent grades require an actual instantiation of the source model.

SPIBB (PMLR97, §2.3 Theorem2, PDF2) gives return improvement at least A-B,
where A is estimated advantage and B its uncertainty penalty. Requested positive
advantage Delta needs A-B>=Delta; merely describing the result as safe improvement
is insufficient. Direct difference evidence is not automatically the pair of
marginal intervals expected by the frozen phase-one scalar comparator. The
source's policy class, finite MDP, confidence event and bounded-return hypotheses
must be carried by the evidence mode. Generic licensing is a consumer, not a
replacement proof of the producer's statistical guarantee.

Assurance 2.0 (arXiv:2405.15800v1 §§1,2.1-2.4) already treats evidence, assumptions,
defeaters, counterevidence, residual risks and ternary assessment. For ordinary
implication blocks, a false premise leaves the parent unsupported, not false;
for a conjunction of actual requirements, one failed requirement defeats the
whole authorization. Phase one's meet and assurance's implication propagation
therefore are different operators even on relabeled identical carriers. This
is an important exact mismatch, not proof that a whole family cannot encode
phase one. The source explicitly discusses fallible human judgment, so it must
not be caricatured as assuming metaphysical certainty. Its practical assurance
indefeasibility differs from phase one's universal StableNow quantification.

Novelty should therefore be evaluated at two levels: the broad fallibilist,
value-oriented research program, and its particular implemented license calculus.
Nonnegative or signed value ranges, grade composition, evidence-labelled inference,
and dependency locality have precedents. The exact integration remains a
possible synthesis contribution; this targeted search neither certifies priority
nor shows it is redundant. Stronger future targets should construct an independently
defined quantitative/contextual relation or effective abstraction and prove its
behavior, rather than repeat a query-quotient definition.


---

# Final source-transfer check (S10)

The freshly retrieved S27 sections 2.1–2.4 distinguish propagation through an
ordinary implication block from exact negation/refutation. Section 4 additionally
discusses conjunctive/disjunctive decompositions; the comparison must not imply
that the source lacks them. The finite check proposed in the appendix compares
one explicitly identified ordinary-block rule with phase one's required-condition
meet. It is not a proposed semantics for every Assurance 2.0 node. Section 2.2's
implementation note describes the inspected 2024 version, not a verified current
tool capability.

S25 Theorem 5.1 explicitly erases a graded derivation to its underlying program.
This closely matches 08c's erasure result at the structural level. The source's
assertion-indexed arrow carries pre/postconditions as well as a pomonoid grade;
its assertions can provide context-sensitive premises. We therefore cannot claim
that phase one's context dependence by itself lies outside all existing graded
logics. What remains is constructing a faithful instance and validating empirical
certificate modes and revision behavior, not renaming the source grades.

S22 Observation 1 was checked in the rendered author manuscript, PDF index 4.
SI, AND and WO characterize its simple-minded output, with compactness used in
the proof. This licenses no blanket claim about finite proof search for all
value operations and no statistical conditioning rule. Phase one's restriction
counterexample and grade-sensitive composition must be explicitly translated.

S23's guarantee remains a return comparison under its policy/data/MDP assumptions;
phase one's four-way interface does not strengthen that guarantee. A positive
required fallback margin needs a bound of the correct sign and magnitude. The
new correlated-loss example below illustrates a difference between joint and
marginal evidence, not an undocumented claim about a specific SPIBB experiment.

No source is treated as a proof that earlier frameworks require metaphysical
certainty, that Value Logic is globally novel, or that a formal signature has
already been chosen. Source-based comparison supports a useful synthesis claim
and identifies non-definitional characterization targets.
