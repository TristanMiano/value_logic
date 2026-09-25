# F03 closing audit: phase-one objectives, literature, and novelty

Session: 2026-09-24-S10 (local session label; recorded UTC date September 25).
Source snapshot: `48b11819230bb856ce03fed28a5161ff5e276e5b`.
This is a literature and contribution audit, not F04, a core selection, or a gate.
The completion record separately checks the F03 evidence and timing obligations.

## 1. The broader program and the particular realization

The author's request concerns **value as primitive, licensing, open-ended
succession, model composition, and the broader phase-one objectives**, not only
whether the four public assessment outcomes are new. Two levels must therefore
remain visible.

At the program level, Value Logic asks what reasoning should preserve when a
bounded agent relies on useful but fallible models without possession of final
metaphysical truth. The intended primitives concern pragmatic value, adequate
error, available computation, and revisable reliance. This is a research
orientation; it does not identify a unique algebra by itself.

At the realization level, phase one constructs a definite interface:
`Assess(s,e,q,P)`, with a plan `e`, current evidence state `s`, task and reliance
context `q`, and requirements `P`. It checks well-formedness first; meaningful
requirements receive supported/open/refuted values. Required values meet to
produce authorization. Quantitative risk, cost, comparisons, and certificate
interpretations live below that public outcome. The paper and formalism also
include quantitative composition, revision locality, continuation semantics,
and a hybrid learned/exact implementation.

Thus **phase one is neither merely a new name for a three-valued truth table
nor a completed general value-term calculus**. Its most accurate description is
a quantitative, evidence-relative model-use calculus whose public consequence
is scoped permission. The next phase can move quantitative value relations into
the inference interface without discarding that achievement.

Primary project anchors: [paper §§1,3–7](../../paper.md),
[core §§2–7](../../formalism/07_core_calculus.md),
[metatheory](../../formalism/08_metatheory.md), and
[proof-carrying plans](../../formalism/08c_proof_carrying_plans.md).
The [original related-work audit](../../notes/literature_core_supplement.md)
already identified important antecedents. This note is a reassessment, not a
claim that phase one ignored them.

## 2. How the objectives relate to existing work

| Objective | What phase one actually does | Literature connection | Assessment and next opportunity |
|---|---|---|---|
| Value as primitive | `q` includes a risk/value preorder, task loss, acceptable region and resource conditions; quantitative plans have grades | S06 semiring preferences, S12 nonnegative arithmetic, S13 signed Abelian logic, S20 utility-plus-penalty representation | Neither numerical values nor an unbounded range is new. The opportunity is a useful consequence relation preserving task-relative value under composition and revision. |
| Use without metaphysical truth detachment | `USE` preserves plan/context/authorization labels; empirical support is not universally factive | S22 I/O logic; S26–S28 assurance arguments; phase-one justification-logic comparison | Nonfactive practical output and fallible assurance have strong antecedents. The exact model-use interface can still be a useful synthesis. |
| Licensing rather than mere ranking | Separate adequate, better-than-fallback, constraint, trace, and comparison atoms | S23 safe policy improvement; S26–S28 assurance and defeaters | Specific evidence producers and structured acceptance already exist. The project's cross-mode consumer interface and its integration with explicit open libraries are the differentiating scope. |
| Retention through succession | Losing comparative preference need not revoke absolute reliance; `AddDom` is profile-local | S22 controlled output reuse, S26–S28 revisable assurance; S20 preference representation | Retention and preference are genuinely different queries. Quantified continuation conditions and model-library changes make this explicit; the general finite-prefix proof pattern is not new. |
| Compose fallible models | Typed payload/grade/certificate transformers, tube-valid sensitivities and root licensing | S25 Graded Hoare Logic; phase-one Hoare/PCC references; S03/S05 transformers | Grading and erasure already have a general framework. A new contribution would identify exactly which value/evidence/update properties survive the actual composition. |
| Revise only affected conclusions | Current validity, negative collection reads, deterministic diagnostics and change-complete impact graph | S24 adaptive computation; S01/S21 abstraction and repair | Dependency locality is established. The concrete evaluator audit is useful; quantitative selective recomputation with certificates is a stronger target. |
| Learn reusable reasoning | Neural proposals feed exact decoding, masks, certificates and fallback; CPWL/ReLU representation is conditional | S04 max–min representation, S23 uncertainty-aware baseline methods, proof-carrying computation | Representation existence is not learnability or operational benefit. The frozen experiment supports some transfer claims but not general superiority. |
| Let models and frameworks remain revisable | Object-model results, internal derivations, metatheorems and evidence modes are kept distinct | S10/S12/S13 each provide precise source theories, not a privileged metaphysics | A framework-relative proof is usable without declaring a final universal theory. A value theory for choosing axioms or changing evaluators remains largely a program objective. |

The last column is a research assessment, not a theorem about priority. Generic
encodability in a powerful existing logic would not automatically make a useful
specialized interface redundant. Conversely, different terminology or the absence
of an exact title match would not establish novelty.

### 2.1 Value-first is a stronger ambition than changing the numeric range

Phase one already allows scalar, vector, and partially ordered risk/value
spaces in `07_core_calculus.md` §2.2. Its annotated computation in `08c` carries
more than Boolean truth. But its central completed rules answer questions such
as whether an already specified requirement is supported, whether a stricter
profile licenses a weaker one, or which evidence update changes a judgment.
They do not yet form a general calculus deriving values of arbitrary new
combinations from value premises.

S12 and S13 show why replacing a Boolean range by `[0,infinity]` or the real line
is not by itself the missing contribution. S20 is an even closer comparison to
the belief/value intuition: under its stated preference axioms it represents
choices through utility and a nonnegative penalty. Its full weak-order and
mixture assumptions are not forced by this project. In particular, a fixed
scalar tradeoff need not preserve phase one's hard constraints or partial orders.

A productive bridge would keep signed or structured values, specify the
nonnegative loss of a permitted substitution, and connect those judgments to
licensed use. It would explain **which operations preserve pragmatic adequacy**,
not merely attach a cost to propositions. S19's independently defined behavioral
and contextual distances and S21's constructive abstraction repair suggest the
kind of characterization that could make such a bridge substantial. Their
existing theorems do not already prove the proposed project adaptation.

### 2.2 Licensing has close predecessors, but the exact output matters

S22's simple-minded I/O operation has SI, AND and WO rules; its reusable variants
add further conditions. Output need not include input, and controlled output
reuse is an explicit choice. Its natural comparison is phase one's `MayRely` or
labelled output layer, not an identity with `Assess`.

For example, logical input strengthening must not be translated as unrestricted
restriction of an evaluation domain. Phase-one `08a`, Theorem 1 and Counterexample
3, show that a small mean risk on a population can hide a bad subpopulation.
Likewise, composing two licensed outputs does not discharge frame matching,
reachable-tube validity, or root-certificate obligations. These are precise
mismatches to retain in a translation, not reasons to ignore the I/O antecedent.

S23's SPIBB theorem supplies a specific high-probability baseline-improvement
bound in a finite discounted MDP and constrained policy class. In return
orientation it gives advantage at least `A-B`, estimated advantage minus an
uncertainty penalty. To satisfy a positive phase-one margin `Delta`, one needs
`A-B >= Delta`, together with all source assumptions. An approximate improvement
bound with positive allowed degradation does not alone prove this.

Phase one's generic improvement atom is principally an **evidence consumer**.
It does not improve SPIBB's statistics. A bound on a joint return difference is
not automatically two marginal risk intervals for the frozen scalar endpoint
comparator; use requires a faithful adapter or a separately declared mode.
Absolute adequacy and relative improvement must also stay distinct: beating a
poor fallback does not show the candidate meets the task's absolute requirement.

### 2.3 Assurance 2.0 materially narrows broad originality claims

S26–S28 are especially close to the evidence-and-licensing objectives. They
already discuss fallible evidence, explicit doubts and counterevidence,
structured claims, residual risks, and semantic analysis. Their recognition of
fallible human judgment means they must not be portrayed as requiring access to
metaphysical certainty. Their practical goal of justified confidence is not the
same as a theorem that no possible future discovery could change an assessment.

The precise operator still matters. In an ordinary assurance implication block,
a false subclaim generally leaves the parent unsupported; denying an antecedent
does not refute its consequence. In phase one, a profile consists of actual
required conditions, so one refuted condition refutes the authorization. The
common three-element carrier does not identify these two operations. Section 6
below records the small separating witness.

S28's completeness analysis ranges over a declared inventory of objects,
properties and environments. It is not completeness of arithmetic proof search
or exhaustion of all future models. This is a useful comparison to `CertUndom`
over an exact finite evaluated set. Both can support a rigorous scoped statement
without thereby producing an unscoped statement about every possible candidate.

### 2.4 Open-ended succession is an explicit scope, not a universal impossibility

Phase-one `06_open_endedness.md` distinguishes current assessment, pathwise
stabilization, permanent current stability, certification, and finality.
Theorem 1 uses two continuations indistinguishable at the current finite state
but differing later. It is a valid finite-information separation argument;
its proof method alone is not a novel theory of induction or knowledge.

The more specific integration is that a library can grow while an old plan
retains its adequacy certificate yet loses comparative status under another
profile. Positive freeze and statistical-margin conditions show that useful
stability need not wait for finality. `AddDom` is a hypothesis about allowed
continuations, not a theorem that science must always discover a better model.

The opportunity is not another unrestricted claim that final truth is
unavailable. It is a constructive description of **what can remain licensed
under a specified class of changes**, with quantitative sensitivity or cost of
revalidation. S24 already gives correctness and cost results for incremental
computation in its own language; a Value Logic result must address the additional
certificate, scope, and allowed-update conditions rather than import it wholesale.

### 2.5 Model composition has more existing structure than a new vocabulary suggests

S25 combines program assertions, preordered-monoid grades, effectful computation
and an erasing interpretation. Its Definition 9 and Theorem 5.1 make erasure part
of a general semantic framework. Phase-one `08c` proves a particular finite-DAG
payload/grade/certificate construction, followed by root licensing. This is a
valuable instance-level obligation, not a first general grading or erasure result.

The analogy is conditional. Phase-one context/input-dependent grades need a
suitable instance of the source grading structure; source assertions, effects,
and loop hypotheses cannot simply be omitted. A postcondition's failure
probability, expected task loss, and the confidence-failure probability of a
risk estimator are different quantities even when all use nonnegative numbers.
The existing context and mode fields are an asset for keeping them separate.

The quantitative path-sum proof in `08a` also depends on full reachable-tube
bounds. A small grade outside the tube, or a frame mismatch, cannot be repaired
by calling a component licensed. This points toward a theorem connecting
quantitative substitutions, checked evidence and allowed contexts—not a mere
new notation for sum/product error propagation.

### 2.6 Learning is still an open objective, not a consequence of representation

Phase one's [representation note](../../ml/03_representation_theorems.md) states
its boundary carefully: suitable finite continuous piecewise-affine statistics
can have exact ReLU realizations, while current evidence, proof checking and
inclusive boundary decisions remain external. Its kernel/factorization theorem
is an exact observational-sufficiency result; without precision restrictions,
its finite code counts do not give real-valued neural-width lower bounds.

The [frozen results](../../experiments/02_results.md) and paper report mixed
outcomes, including poor usable coverage. Therefore the evidence does not show
that a value-first architecture generally outperforms alternatives. It does
leave a concrete research question: can a compact learned representation retain
just enough quantitative, contextual and evidential information to derive useful
new guarantees? Success needs a proof interface plus a discriminating experiment,
not another unrestricted universal-approximation statement.

## 3. Degree of novelty: distinguish ingredients, integration, and results

This is my literature-grounded assessment, not an exhaustive priority search.
The exact combination has not been shown to be unprecedented, but neither has
an equivalence reducing the complete phase-one system to a cited system been
established. The new Assurance and GHL comparisons materially narrow broad
originality claims without refuting phase one's explicit theorems.

**Ingredient level: mostly established.** Three-valued meet, interval tests,
unary preorder closure, deterministic-decoder quotients, DAG induction,
Lipschitz propagation, append-only histories, and checked program annotations
are not strong standalone novelty claims. Several phase-one proofs correctly
identify these as standard patterns or elementary consequences. Theorem 15 of
`08_metatheory.md` is explicitly a mode-soundness schema: its statistical
substance lies in establishing its premise for a particular evidence producer.
Likewise, `ml/03`'s representation theorem does not prove a learner finds the code.

**Integration level: meaningful but priority remains open.** The particular
combination of task-relative adequacy, fallback advantage, requested versus
reported comparisons, evidence modes, complete diagnostics, negative reads,
open-library continuation classes, typed composition and learned/exact boundaries
is coherent. Its formal details rule out real mistakes. But S25 and S26–S28
already combine several nearby ideas, so “the first logic for fallible evidence”
or “the first way to combine grades and proofs” would be indefensible. A focused
comparison of concrete translations is stronger than a claim that no similar
framework was found under the same name.

**Theorem level: the concrete instantiations are stronger than the generic
schemas.** Deriving every actual evaluator footprint, including negative reads,
is more informative than assuming a change-complete graph and restating its
consequence. A path-realizability hypothesis must still accompany a necessary
condition. Characterizing a finite independently realizable profile fragment is
useful, but not completeness of arbitrary quantitative reasoning. Defining the
coarsest observation quotient is a baseline for, not a replacement for, an
independently characterized semantics or effective abstraction procedure.

**Program level: there is substantial room for a distinctive result.** A
value-first calculus can investigate how representations preserve pragmatic
consequences across use, composition, budgets and changes of evidence. Existing
mathematics supplies much of the vocabulary. The remaining opportunity is to
prove a useful relationship among those notions that is not stipulated by a
semantic definition, and to demonstrate consequences the simpler baseline
cannot obtain at comparable cost.

A defensible concise positioning of phase one is:

> A particular typed, revisable model-use assurance calculus, combining
> quantitative certificates, profile-relative authorization, explicit
> open-library scope, and an experimentally tested learned/exact interface.

This describes its realized contribution without claiming the program ends
there. It is not a recommendation to rename the project or abandon value as
primitive.

## 4. The strongest theorem opportunities, anchored to phase one

These refine the existing [T0–T4 agenda](01i_calculus_desiderata_and_theorem_agenda.md)
without choosing a carrier, executing F04, or rewriting the task sequence.
They are **unproved project targets**, not new claims of this audit.

### P1 — Recover the old calculus and prove a strict, useful extension

Start with the phase-one region/composition interface, not merely four labels.
Give an independently specified value domain and rules, a typed translation of
a named phase-one fragment, and a decoder back to its required observations.
Prove sound preservation of those observations and characterize where equality
holds. Preserve evidence-mode and request-scope premises. Then give an inference
about a composite or joint requirement that the old summary cannot determine
but the new semantics can, with a finite checkable derivation.

**Anchor:** `08_metatheory` Theorems 8–14 and `08c` root-certificate lifting.
**Precedents:** S01/S10 abstraction and source translations; S25 grading.
**What makes it more than recoding:** independently defined rules plus a strict
separation and a useful composition, not defining the new decoder to return the
old assessment. Section 6 gives a small explanatory seed, not this full theorem.

### P2 — Characterize practical substitution under bounded permitted uses

Phase one's source scopes, frames and reachable tubes already state what makes
reuse legitimate. Define a nontrivial context grammar respecting those
conditions and an execution/resource budget. Seek an independently defined
compositional distance or grade equal to, or sharply bounding, the worst
pragmatic loss visible to those contexts. Include a constructive separating
context or an arbitrarily close one for the reverse direction.

**Anchor:** `08a` path-sensitivity bounds and `ml/03` observation factorization.
**Precedents:** S05/S19 operator and contextual-distance characterizations.
**New work still needed:** signed/directed observations, evidence assumptions,
resource-indexed composition and a non-definitional reverse theorem. Absolute
values may remain unbounded; limiting amplification is not clipping all values.

### P3 — Preserve useful judgments through quantitative, selective revision

Strengthen the existing exact disjoint-write rule: allow relevant inputs to
change, quantify their effect on values and inference bounds, and decide which
certificates must be recomputed for the requested tolerance. An effective
refinement procedure could either produce an adequate updated certificate or a
witness that the retained summary is insufficient. Include scope changes,
newly populated collections and changed evidence validity, not only numerical
perturbations of a fixed vector.

**Anchor:** `08b` derived read/write footprints, `06` continuation classes,
and the existing phase-two contextual-update counterexample.
**Precedents:** S21 local abstraction repair and S24 adaptive computation.
**New work still needed:** a meaningful optimality or error/cost guarantee for
the declared fragment, not just another dependency graph. An information-minimal
refinement need not minimize runtime or storage.

### P4 — Characterize belief-as-a-component-of-value under admitted updates

Use the phase-one distinction between task criterion, risk estimator, training
objective and evidence mode. Specify when a belief penalty plus other value
terms is an adequate semantics for those uses, and which combinations or updates
commute with a compressed representation. The broad penalty/KL connection has
an antecedent in S20; the sharper opportunity is update-sensitive preservation.

**Anchor:** phase-one `q`, estimator nesting and non-factive certificate modes;
F03's signed-value and belief/context adapters.
**Precedents:** S15/S20 and the audited S12/S13 fragments.
**New work still needed:** stated update class and witness/information access;
static equality of all current scalar evaluations alone is insufficient.

My preferred eventual portfolio remains **sound operational composition plus
one of P2 or P3**, with P1 as a carefully scoped compatibility/separation result.
P4 is the strongest direct bridge to the author's belief/value intuition. These
are alternatives and supporting directions, not a demand that one phase prove
all four.

## 5. Exact source records added for this comparison

The existing twenty-one sources remain intact. Seven targeted records are
added because the requested phase-one comparison introduces specific neighboring
systems. They are not seven additional full-paper verifications. Bibliographic
and inspection details are in [F03_sources.json](F03_sources.json); their uses
are recorded in [F03_import_contracts.json](F03_import_contracts.json).

- **S22, Makinson–van der Torre (2000), Input/Output Logics.** Author manuscript,
  §3.2 Observation 1 and §5.1. The first identifies SI/AND/WO with simple-minded
  output; reusable output is a separate construction. PDF index 4 was viewed.
  Comparison-only for phase-one labelled use; no full translation is claimed.
- **S23, Laroche–Trichelair–Tachet des Combes (2019), SPIBB.** PMLR 97,
  §2.3 Theorem 2 and §2.5; theorem at PDF index 2 visually checked. The baseline,
  policy class and uncertainty terms are part of the guarantee. No theorem for
  a generic phase-one risk estimator is imported.
- **S24, Acar–Blelloch–Harper (2002), Adaptive Functional Programming.**
  Author-hosted POPL article, §§4/6, Theorems 1/5; PDF index 11 viewed.
  Change-propagation correctness is relative to its language/store conditions;
  the full correctness proof is delegated to a companion report not audited here.
- **S25, Gaboardi–Katsumata–Orchard–Sato, Graded Hoare Logic.**
  `arXiv:2007.11235v2`, January 2021: §3.4 Table 1, Definitions 1/9,
  Theorem 5.1. Grading and erasure are explicit existing structures. The whole
  categorical model is not imported for arbitrary phase-one context dependence.
- **S26, Bloomfield–Rushby, Assurance 2.0: A Manifesto.**
  `arXiv:2004.10474v3`, January 2021, §§II–III. Read the distinction between
  plausible premises, deductive steps and residual doubts. Used as a broad
  methodological comparison, not a source of an absolute finality theorem.
- **S27, Bloomfield–Netkachova–Rushby, Defeaters and Eliminative Argumentation.**
  `arXiv:2405.15800v1`, May 2024, §§1–2.4. Read ordinary and exact defeater
  propagation; false antecedents do not generally refute parents. These are
  assessment rules, not phase one's requirement meet under a new name.
- **S28, Murugesan et al., Semantic Analysis of Assurance Cases.**
  `arXiv:2408.11699v3`, §5 adequacy/completeness discussions. Its declared-domain
  semantic checks strengthen the comparison but do not exhaust future models
  or establish arithmetic proof-system completeness. Diagram interpretation is
  not needed for the used textual scope statements.

The PCC background remains explicitly cited by phase one. A fresh publisher
abstract was located, but this continuation's attempted full-PDF URLs failed;
no new full-proof audit of PCC is claimed. No external papers are redistributed.

## 6. A worked bridge to the actual phase-one calculus

The following elementary arguments make the comparison operational. They do not
claim new priority, change phase one's frozen rules, or choose the next core.
They use the region clauses of `07_core_calculus.md` and `08b_audit_repairs.md`,
and isolate exactly where a richer value representation can add information.

### 6.1 Recovering a meaningful region atom

Fix one meaningful requirement, a **nonempty** certified possible-value region
`U`, and its acceptable set `A`. Assume the evidence is current, scope-correct,
conflict-free, and accepted by the relevant mode. Define

\[
\alpha_A(U)=\begin{cases}
+&U\subseteq A,\\
-&U\cap A=\varnothing,\\
?&\text{otherwise.}
\end{cases}
\]

This is precisely the region-test part of the phase-one evaluator. It is not
an encoding of all diagnostics, trace modes, missing evidence, or well-formedness.
An empty region is not silently accepted by vacuous subset inclusion: the
present definition excludes it. Missing or conflicting evidence has its own
phase-one handling before this restricted test is used.

There are **two different orders**. Required statuses meet along
`- < ? < +`. By contrast, information refinement uses `? <=info +` and
`? <=info -`, with the resolved outcomes incomparable. If
`empty != U' subseteq U`, then

\[
\alpha_A(U)\leq_{\rm info}\alpha_A(U').
\]

**Proof.** Containment in `A` and disjointness from `A` are each preserved by
nonempty restriction. A mixed region can remain mixed or resolve either way.
For example, at tolerance one, `{0,2}` is open, `{0}` supported and `{2}` refuted.
Thus genuine information gain need not move upward in the conjunction chain.
Evidence invalidation is not generally region narrowing, so the result does
not contradict phase one's nonmonotonic state updates.

This gives a precise compatibility target: a new value semantics may recover
this decoder on an admitted fragment while retaining richer information for
other queries. Merely using the same three output names proves less.

### 6.2 Exactly when separate statuses lose joint refutation

Let `B` be a nonempty subset of `{0,1}^n`, `n>=1`, representing jointly possible
satisfaction patterns of `n` requirements. This is a semantic uncertainty set,
not an assumption that the phase-one evidence store already contains it.
Let `a_i` be `+` if every pattern has coordinate `i` equal to one, `-` if every
pattern has coordinate `i` equal to zero, and `?` otherwise. Compare

\[
K(B)=\min_i a_i
\quad\text{and}\quad
J(B)=\begin{cases}
+&\forall b\in B,\ b=(1,\ldots,1),\\
-& (1,\ldots,1)\notin B,\\
?&\text{otherwise.}
\end{cases}
\]

`K` is the phase-one required-status meet of the individual region summaries.
`J` is the three-way abstraction of the **joint conjunction claim**.

**Proposition.** `K(B) != J(B)` holds exactly when

\[
(1,\ldots,1)\notin B
\quad\text{and}\quad
\forall i\ \exists b\in B:\ b_i=1.
\]

In this case `K(B)=?` and `J(B)=-`; there is no opposite discrepancy.

**Proof.** `K=+` means every coordinate is one in every pattern, exactly the
condition for `J=+`. `K=-` means some coordinate is always zero, which makes
the all-ones pattern impossible and hence `J=-`. If neither happens then
`K=?`. It differs from `J` only when `J=-`, namely when the all-ones pattern is
missing although no single coordinate is always zero. This is the displayed
condition. The cases exhaust all nonempty `B`. ∎

For a Cartesian product of nonempty marginal possibilities,
`B=B_1 x ... x B_n`, the discrepancy is impossible: if each `B_i` contains one,
then the product contains the all-ones pattern. **Thus the separate-status
meet agrees with the joint abstraction on that explicit product fragment.**

The smallest separating example is

\[
B=\{(1,0),(0,1)\}.
\]

Each condition is individually unresolved, while their simultaneous satisfaction
is impossible. In loss coordinates use two jointly possible vectors `(0,2)`
and `(2,0)` with each tolerance one. Both marginal regions are `{0,2}`, but
`max(loss_1-1, loss_2-1)=1` in every possibility.

The gap is useful but is **not an error in phase one's declared interface**.
A phase-one profile is refused when a required atom has an accepted refutation;
it need not materialize the whole joint uncertainty set. A new joint atom or
separate joint-query interface could expose the additional refutation without
changing the old profile's meaning. The independent-atom premise of phase-one
Theorem 10 explicitly excludes unrepresented conjunctive entailments; our
construction therefore does not refute its relative-completeness theorem.

The finite tests enumerate all 15 nonempty binary two-coordinate sets and all
255 three-coordinate sets. They check the exact characterization, not a
sampling conjecture. The general proposition is established by the proof above.

### 6.3 Why the assurance comparison is not a relabeling

For an ordinary implication argument block with no relevant defeater, S27
§§2.1–2.2 assesses the parent as supported when every premise is supported;
otherwise the ordinary block alone does not establish that parent. For example,
a supported first premise and refuted second premise need not refute the parent:
the implication could have a true consequent for another reason.

A phase-one **required-condition conjunction** instead is refuted when one
required condition is refuted. Its top claim includes that condition, rather
than merely being one consequence of it. The two operations differ on `(+,-)`.
This is legitimate in both cases because their judgments have different meanings.
S27's exact-defeater and conjunctive/disjunctive decomposition cases require
separate rules; this comparison does not assert that every assurance block uses
one ordinary-implication operation. The fixture validates only the displayed
fragment of the comparison.

### 6.4 A loss-difference certificate can be stronger than marginal intervals

Suppose the jointly certified candidate/fallback losses are

\[
U=\{(0,1),(1,2)\},\qquad \Delta=1.
\]

Every joint possibility satisfies `loss_candidate + Delta <= loss_fallback`.
But marginal projection gives candidate interval `[0,1]` and fallback interval
`[1,2]`. Phase one's conservative scalar endpoint test requires `1+1<=1`,
which fails. It does not refute improvement; it withholds that support because
the marginal test has discarded dependence.

This is why a source result about the **difference** in performance cannot be
silently substituted for two separate interval certificates. A faithful adapter
can expose a valid joint-difference mode, or preserve enough structure for the
comparison. The example supplies neither new SPIBB data nor a stronger general
statistical guarantee. It is a finite semantic comparison of two evidence forms.

## 7. Closing assessment and remaining scientific work

F03 has now connected the original pragmatic motivation, its finite licensing
realization, quantitative composition, revision machinery, and learned interface
to concrete primary-source results. The appended source records state what was
inspected, and the existing register distinguishes usable fragments from unused
stronger statements. The scoped source gaps and the rejected S16 convexity
claim remain recorded; none is silently imported into the project.

Completion of **this literature task** is not completion of the calculus.
No universal novelty theorem is established, no entire external proof system is
independently verified, and no readiness gate is passed here. The eight broad
objective comparisons and P1–P4 are evidence for future choices, not replacements
for F04's hostile examples or Gate A's candidate decision. Phase-one results and
negative experimental outcomes remain unchanged.

The most promising continuity is this: **phase one made practical reliance
explicit; a later value-based calculus can explain, compositionally and with
less unnecessary information, what warrants that reliance.** A rigorous result
connecting those two levels would address the original ambition more directly
than either abandoning the phase-one interface or treating it as immutable.
