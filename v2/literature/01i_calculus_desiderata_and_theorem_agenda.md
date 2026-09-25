# F03 — Calculus desiderata and a theorem agenda

Session: 2026-09-24-S9 (America/Los_Angeles; observed UTC date September 25).
Base: `b722b22607ce3d051a84aaa08f00f073e9a99cc2`.
Status: literature-informed design recommendations and explicitly labelled targets.
This is **not** Gate A, a selected calculus, F04, or a novelty claim.

The author requested a positive account of what a good calculus should do and
which theorems are worth pursuing. This note complements the earlier import
checks; it does not replace the original motivation with a catalogue of reasons
not to build a calculus. Its recommendations concern the four F02 candidates:
scalars (S), aligned profiles (P), continuation transformers (T), and achievable
guarantee sets (G), with the later signed-value and belief-penalty bridges.

## 1. What the inspected literature actually rewards

The following are observations about this selected literature, not a survey of
all mathematical logic or a prediction of publication acceptance. Existing source
IDs refer to [the source manifest](F03_sources.json). Three new primary references address specific gaps in this request: contextual
distance, axiomatic value/ambiguity representation, and local abstraction repair.
The older abstraction-completeness work remains an author-abstract-only lead.

### 1.1 S12: expressive arithmetic, finite consequence, and a decision boundary

In [Rational Lawvere Logic](https://drops.dagstuhl.de/storage/00lipics/lipics-vol363-csl2026/html/LIPIcs.CSL.2026.3/LIPIcs.CSL.2026.3.html),
Theorems 9 and 11 separate finite-theory completeness from its finite-valued
polynomial specialization. Section 6's reduction has two obligations: semantic
validity passes to every branch, and proofs of the branches reconstruct a proof
of the original request. Theorem 15 rules out unrestricted finitary completeness
for infinite theories; Theorem 17 gives complexity bounds for rationally encoded
inputs. Section 5 distinguishes encoding distance names plus axioms from
obtaining their meaning automatically, and restricts the QEL embedding's
completeness claim to the stated compact theories.

**Design reading:** expressing an objective, proving a consequence, finding a
proof, and explaining its runtime are separate achievements. For Value Logic,
a useful finite or tolerance-relative completeness result is a better target
than silently demanding all of them for an unrestricted language. The actual
numeric interpretation still has to mean something for a task.

### 1.2 S13: proof structure can be a contribution, not just semantic validity

In [Metcalfe, Olivetti and Gabbay's inspected 2002 preprint](https://arxiv.org/abs/cs/0211021v1),
Section 4 establishes analytic hypersequent systems and cut admissibility;
Sections 5–6 develop different terminating and labelled calculi. In particular,
Theorem 62 uses a lexicographically decreasing tuple of formula complexity,
variable count, a focused occurrence imbalance, and symbol count. Theorems 63
and 66 separately establish soundness and completeness of that terminating
version. Theorem 88 concerns the labelled calculus's complexity. These are
properties of the specified systems, not every extension of signed arithmetic.

**Design reading:** a rule set may be sound yet unsuitable for search. An
analytic or terminating reformulation, an effective normal form, or a faithful
certificate translation can be a substantial result. We should distinguish
proof discovery from checking a supplied proof. Arbitrary multiplication, new
constants, contextual updates, and policy witnesses do not inherit those
results just because our values are signed.

### 1.3 S10: a universal property explains why a semantic representation fits

In [Mio, Sarkis and Vignudelli, LMCS 2024](https://lmcs.episciences.org/14876/pdf),
Theorem 5.1 constructs free quantitative algebras. Section 5 proves that a
permitted generator interpretation extends uniquely to an appropriate
homomorphism; Lemma 5.12 then connects the term construction back to derivability,
and Theorem 5.13 gives completeness. Definition 7.6 and its generalized-metric
counterpart (equation 8.9) require an extension not to alter the old ordinary
equations. The complete variable relation and the infinitary rule system remain
part of the source interface.

**Design reading:** an attractive representation theorem is not merely a
bijection between two encodings. It explains the operations, identifies which
models it covers, and preserves the intended comparisons. Conservativity is
also an explicit property to establish, not something that follows from reusing
old symbols. None of this makes a free-algebra theorem a finite implementation.

### 1.4 S19: compare an independently defined semantics with actual observations

[Crubille and Dal Lago, arXiv:1701.05521v1](https://arxiv.org/abs/1701.05521v1),
*Metric Reasoning About lambda-Terms: The General Case*, defines contextual
distance using observations of program contexts. Sections 4–5 study amplification
by copying and a tuple-based behavioural distance. Theorem 4 bounds contextual
distance by the behavioural one; Theorem 5 proves equality in the specified
calculus without parallel disjunction. The trace-to-context construction in section 5.5 and Lemma 14 obtain the
reverse direction by realizing discriminating traces as contexts. This is a characterization,
not a definition that declares the two distances equal. Copying does not
trivialize every fragment considered in the paper.

**Design reading:** a strong Value Logic theorem would connect a tractable
semantic construction to the value losses that permitted consumers can actually
observe. Restricting information access and resource use is then part of the
meaning of the theorem. The source concerns probabilistic higher-order programs;
our directed signed-value version remains a proposed adaptation, not an import.

### 1.5 An abstraction-completeness lead, kept at its actual evidence level

The [authors' abstract for Giacobazzi, Ranzato and Scozzari (JACM 2000)](https://profs.scienze.univr.it/~giaco/abstracts/jacm.abstract.html)
frames completeness as avoiding additional precision loss in abstract
computations and discusses least refinements and greatest restrictions under
specific assumptions. The abstract also distinguishes limits of fixed-point
completion. A full proof text was not obtained in this session: the author page
links an old PostScript endpoint and the author-uploaded PDF retrieval failed.
No numbered theorem, universal existence result, or algorithm from this work
is imported. It is a clearly identified lead, not another fully audited source.

**Design reading:** this motivates asking for the smallest task-sufficient
representation or a justified refinement procedure, instead of retaining all
information by default. The existing S01 abstract-interpretation comparison
supplies the broader sound-abstraction background. The constructive target below
states its own fragment rather than borrowing unverified completion guarantees.

### 1.6 S20: axiomatize a value/belief combination, then characterize it

[Maccheroni, Marinacci and Rustichini](https://www.carloalberto.org/wp-content/uploads/2018/11/no.12.pdf),
*Ambiguity Aversion, Robustness, and the Variational Representation of Preferences*,
is inspected in its March 2006 revision (Carlo Alberto Notebook 12, May 2006).
Printed pages 6–7 give A1–A6. Theorem 3 (p. 9) characterizes preferences by

$$V(f)=\min_p\left\{\int u(f)\,dp+c(p)\right\},$$

with affine $u$ and grounded, convex, lower-semicontinuous $c\geq0$.
Equation (2) includes a KL penalty. Proposition 6 (p. 10) gives fixed-$u$ penalty
uniqueness in that class when $u(X)$ is unbounded; Theorem 3 otherwise specifies
a minimal penalty. Appendix Lemma 26 and the proof on pp. 32–33 explain the
conjugacy route. This is not a uniqueness result for arbitrary nonconvex beliefs.

**Design reading:** representation should be earned from explicit properties,
not postulated because two quantities can be added. Complete preferences,
mixture continuity and uncertainty aversion are possible fragment assumptions,
not mandatory commitments of Value Logic. This provides a mathematical precedent
for the author's intuition, without selecting a calculus or granting a hidden
parameter the status of uniquely true belief.

### 1.7 S21: repair only the precision needed by a particular use

[Bruni, Giacobazzi, Gori and Ranzato, *Abstract Interpretation Repair*](https://iris.univr.it/retrieve/f3391e11-abdd-46fb-b90b-dd68816496e8/pldi22.pdf)
(PLDI 2022), Definition 4.8 and Theorem 4.9, characterize pointed locally
complete refinements of an abstract domain. The additive case has an explicit
existence criterion; Theorem 4.11 gives a constructive Boolean-guard case.
Section 5 develops forward/backward repair strategies. Section 8 separates
these results from scalable symbolic implementation.

**Design reading:** seek just enough precision for the particular use, not
universal exactness in advance. Refinement optimal in an information order is
not automatically cheapest to represent or compute. The source assumes complete
lattice/closure-operator semantics and its stated transfer-function conditions;
these require a mapping before use in a value calculus. This is a stronger
primary antecedent for T2 than the abstract-only lead above, not a proof of our
proposed tolerance- and resource-sensitive extension.

## 2. Recommendations and theorem targets

The following sections are the project's proposed agenda, not statements that
the preceding papers prove these properties of Value Logic.

### 2.1 Attributes I would prioritize

These are proposed acceptance questions for later design, not additional fixed
philosophical premises. The source column identifies the motivating type of
result; it does not assert that the source already proves it for this project.

| Priority | Attribute | A useful acceptance question | Literature connection |
|---|---|---|---|
| Essential | **Operationally explicit meaning** | Does a judgment identify a task, units, available information, and the use whose value it bounds? Can one state when it is meaningful, not just evaluate a formula? | S03 and S08 make operational/uncertainty assumptions matter; S12 separates interpretation from syntactic arithmetic. |
| Essential | **Sound, nontrivial composition** | Can premises about components derive a useful new guarantee for their joint or sequential use, without reevaluating the whole composite? Are sensitivity, duplication and resource costs charged correctly? | S02/S10 organize compositional quantitative reasoning; S19 tests preservation under actual contexts. |
| Essential in an admitted fragment | **Sufficient information at the requested tolerance** | Does the representation keep the distinctions needed by permitted consumers, including declared later updates, without storing everything? Can it provide a bound when an exact answer is unnecessary? | S01 supplies sound abstraction; S19 supplies an observational comparison; S07/S20 explain what some scalar summaries identify. |
| Strongly desirable | **Faithful interfaces between fragments** | Do translations preserve and reflect the particular judgments claimed, including guards, units and premise multiplicity? Does adding structure avoid changing the old fragment's conclusions unintentionally? | S10's extension condition; S12's qualified embeddings; S13's translations. |
| Strongly desirable | **Auditable and effective reasoning** | Can a small independent checker validate a derivation? Is there a terminating or otherwise controlled search procedure for a useful fragment, with a stated complexity measure? | S13's distinct analytic and terminating systems; S12's finite-theory and rational-input results. |
| Required when a judgment promises an action | **Attainable witnesses** | Does a derived claim yield a feasible plan available at the right observation time, rather than only a numerical optimum or a different action in each hidden model? | S03/S08 operational semantics and S12's example encodings motivate checking existence separately. |
| Strong practical desideratum | **Adaptive precision** | Can a failed adequacy proof trigger a targeted information refinement rather than a complete redesign or a demand for all model details? | S21 provides exact local-repair antecedents; a tolerance/resource-sensitive version is still a project target. |
| Useful engineering goal | **Local revision and explicit dependency** | When a premise or interpretation changes, can invalidated claims be located and unaffected derivations retained? | The project's existing phase-one locality/proof-carrying work is an available precedent, not a new contribution of F03. |

The second and third attributes are the center of the proposal. A calculus that
is sound because it always answers “unknown” has not achieved the intended
capability. A calculus that computes an exact aggregate from a complete supplied
world table may have useful semantics, but still owes an account of *inference*
and a reason to prefer its representation to the original table.

I would not require every desirable attribute in the most general language.
A small fragment with a sharp characterization and useful composition is a
better first result than a grand signature with no demonstrated inference.
The unrestricted mathematical range can remain unbounded while a particular
query supplies a finite sensitivity, resource budget, or tail condition.

### 2.2 Properties to choose deliberately, not assume universally

Several attractive laws describe a particular evaluation regime, not all value:

* **Complete preference order, uncertainty aversion and convexity.** These are
  legitimate choices for a variational fragment, as S20 makes explicit. They
  would exclude some partially ordered guarantees or preserve only a convexified
  view of a nonconvex belief description. That is a scope decision, not an axiom
  forced by fallibilism.
* **Additive shifts, scaling and structural rules.** A shared payoff shift,
  multiplying a payoff, repeating a resource, and copying a model are different
  operations. Choose the admissible laws by their operational meaning. A
  translated finite signed quantity is not permission to cancel infinity.
* **Unrestricted exact completeness.** A useful finite or approximate fragment
  can be complete even when a stronger infinitary ambition is not available.
  Noncompactness is a reason to formulate the claim accurately, not a reason to
  give up on proof theory.

Similarly, numerical `[0,1]` output, a total order, probability semantics,
commutative sequencing, universal contraction, and a single scalar objective
are not entrance requirements. Neither are elegant category-theoretic language
or neural implementability substitutes for a worked operational example.

### 2.3 Four different claims often called “complete”

The following terminology distinguishes possible project claims. It is not an
assertion that every cited author uses identical conventions.

| Claim | What it compares | What it does not automatically give |
|---|---|---|
| **Proof-system completeness** | Independent semantic consequence versus derivability in specified rules. | A terminating search, feasible proof size, or a policy witness. |
| **Representation/expressiveness theorem** | Objects satisfying stated structural assumptions versus a concrete mathematical representation. | Preservation of every future update, a unique hidden interpretation, or efficient construction. |
| **Exactness of an abstraction** | Evaluating an admitted operation before versus after summarizing it. | Exactness for a larger operation/context language or for recursive limits. |
| **Contextual full abstraction** | Distinctions or quantitative distances in an independently constructed semantics versus permitted observations of use. | Decidability, bounded search, or the same result after enlarging the consumer language. |

All four can be worth proving. They answer different questions. In particular,
calling a semantic quotient “complete” because it is defined to identify exactly
what the chosen observations identify is not yet a constructive characterization.

## 3. Ranked theorem targets for this project

The ranking below is my provisional research preference. It selects **result
shapes**, not S, P, T, G, or a permanent logical core. All targets are unproved
for an eventual Value Logic calculus. The small examples in section 4 illustrate
what would and would not count as meeting them.

### T0 — Necessary foundation: sound operational composition

First require a soundness theorem for the chosen rules and a nonvacuous
composition result. A typical target judgment says that replacement preserves
value to a specified allowance, with evidence/context/resource premises made
explicit. The rules should derive at least one useful composite conclusion from
strictly less than a complete reevaluation of its outcome model.

A proof by induction is entirely appropriate. But “every rule was defined as a
semantically valid inference” is not a sufficient contribution: the rule family
and semantics should be independently described, and an actual derivation
should demonstrate why this formulation is useful. Treat this as the necessary
base, not the phase's only ambitious theorem. S02/S10/S12 provide distinct
examples of organizing such metatheory.

### T1 — First choice: characterize resource-scoped observable value loss

Fix an evidence interpretation, observation unit, information schedule and
admitted context family `C_b`. For finite signed observations, potentially
unbounded across contexts, define the *benchmark* quantity

$$
D_{C_b}(M,N)=\sup_{C\in C_b}[V(C[M])-V(C[N])]_+.
$$

Seek an independently defined algebraic, compositional, or algorithmic quantity
`d_b` satisfying `d_b = D_{C_b}` in a useful fragment, or a precise two-sided
approximation if exact equality is too strong. The sound direction bounds every
allowed consumer's loss. The converse constructs a separating consumer, or an
arbitrarily close one when the supremum is not attained. S19's proof structure
is the precedent; its probabilistic symmetric theorem is not the desired signed,
directed theorem verbatim.

**Why this would be interesting:** it says that the value semantics preserves
exactly the distinctions that the declared uses can exploit. It connects the
calculus to pragmatic adequacy rather than an arbitrary numerical algebra.

**First tractable scope:** finite typed acyclic expressions, a finite primitive
library with independently justified grades, rational finite inputs, and an
explicit context grammar with a resource budget. This is a proposed starting
scope, not a theorem that such a fragment has the target property. Source tests
may require a different fragment.

**Non-goal:** defining `d_b` by the same supremum and calling the equality a new
result. Context composition must also respect the budget indexing: with an
additive cost convention, composing budget-b and budget-c contexts may require
`C_{b+c}`, not closure inside `C_b`. Replacing a zero-loss preorder with equality
requires zero loss in both directions.

### T2 — Second choice: minimal adequate information, with constructive repair

For a fixed operation/context language, characterize which summaries are
sufficient for its exact or tolerance-relative conclusions. A strong version
constructs a least exact refinement of a proposed summary, up to the declared
information order. A quantitative version provides a sharp information/error
tradeoff or a finite refinement procedure that either certifies the requested
bound or supplies a distinguishing example.

**Why this would be interesting:** F01/F02 show that “a scalar is insufficient”
is usually too broad, while “retain the whole model” is often unnecessary.
This target would explain which extra structure pays for which inference.
The exactness question is motivated by S01, S21 and the explicitly limited
abstraction-completeness lead. S21 makes a local target particularly attractive:
refine only where the current use needs it. No general existence or runtime
theorem is imported for our tolerance-sensitive setting.

**First tractable scope:** a finite value-table universe with a declared finite
query set and finitely represented operations. Then investigate what survives
when tables or contexts are symbolic and unbounded. Exact equivalence can be a
congruence; approximate indistinguishability at a fixed positive tolerance need
not be transitive. A smallest approximate *quotient* must not be promised simply
by copying the exact construction.

T1 and T2 are related but not the same. T1 identifies an observational loss;
T2 identifies the information sufficient to determine or bound it.

### T3 — Third choice: a representation that survives belief/value composition

S20 gives an especially relevant existing representation pattern: expected
utility plus a nonnegative penalty, characterized by explicit properties. The
project should reuse such a result where it applies, not present adding a KL
term or taking a variational infimum as a new theorem.

A more distinctive target is to characterize when a belief-to-value translation
preserves **the admitted combinations and updates**, as well as current
comparisons. For example, identify a class of penalties and update contexts
where translating and then updating agrees with updating and then translating,
or derive the sharp loss caused by using a smaller representation. The earlier
independence/uniform-marginal witness makes this an actual question, not an
automatic consequence of a static conjugacy theorem.

**Why this would be interesting:** it would show in what operational sense
belief is contained in, recoverable from, or usable inside value. It avoids
claiming that all beliefs are KL, that all value is belief, or that one
normalization uniquely identifies a metaphysical utility.

**First tractable scope:** finite outcome spaces, fixed comparison units,
proper declared penalty classes, and explicitly listed update operations.
Complete-order/convexity assumptions can be examined as one fragment while
nonconvex or partially ordered alternatives remain live. General min–max T and
hard-budget G should not be silently replaced by a concave scalar fragment.

### T4 — Fourth choice: robust finite certification with usable witnesses

Seek a fragment where a tolerance-relative semantic conclusion yields a finite,
checkable derivation and, whenever the judgment promises action, a feasible
plan available under the declared information schedule. Prove what the checker
certifies; separately bound search cost or give a terminating search procedure.
A normal-form or cut-elimination result can be valuable if it yields this
concrete improvement. S12/S13 motivate these different proof-theoretic targets;
phase one's proof-carrying-plan work is an explicitly reusable baseline.

**Why this would be interesting:** the intended user needs a justified action
or adequacy claim now, not just existence of an infinitary semantic argument.
A particularly relevant extension asks when positive practical slack lets a
finite portion of improving evidence certify an adequate result. The elementary
example in section 4.4 does not establish that for an unrestricted language.

**First tractable scope:** rational finite arithmetic and guarded operations;
known finite action menus or finite typed plan derivations; no implicit hidden
information or infinite optimizer assumption. A source arithmetic proof can
supply part of the certificate, but operational witness extraction remains its
own obligation. A hard logical task may still admit a fast checker for supplied
certificates; this is not the same as fast search or short certificates for all
instances.

### Useful supporting results, not another unlimited agenda

A conservative embedding of a Boolean, signed arithmetic, or phase-one fragment
could make any of T1–T4 stronger, provided both directions are actually proved
under the appropriate guards. Sharp separation theorems, lower bounds, and
counterexamples are also useful when they identify the smallest necessary
additional assumption and a surviving constructive alternative. Interpolation,
normalization, categorical universal properties, and learning bounds should be
pursued when they solve a concrete interface problem, not as an obligatory list
of fashionable theorem names.

I would plan the eventual phase around **T0 plus one of T1 or T2**, with a modest
fragment-translation or certificate result. T3 is the strongest bridge suggested
by the author's belief/value intuition. Proving all four ambitious targets in
one phase is neither required nor the present recommendation.

## 4. Small worked anchors for the proposed targets

These elementary reconstructions explain the agenda; they do not fulfill its
ambitious targets for a chosen calculus. Their general arguments are below;
finite fixtures only check the displayed cases. None is claimed novel.

### 4.1 An independently specified observational characterization

Let `n>=1`, `x,y in R^n`, and

$$d_+(x,y)=\max(0,\max_i(x_i-y_i)).$$

Let `C` be all real-valued maps on `R^n` which are coordinatewise monotone and
satisfy `F(z+t1)=F(z)+t` for every real `t`. These properties describe consumers
independently of the proposed formula for `d_+`. Then

$$d_+(x,y)=\sup_{F\in C}[F(x)-F(y)]_+.$$

For the upper bound put `r=d_+(x,y)`. Coordinatewise, `x<=y+r1`. Monotonicity
and the shift law give `F(x)<=F(y)+r`. For the reverse bound, if `r>0`, choose
a coordinate `j` attaining the largest difference. The projection `F(z)=z_j`
belongs to `C` and attains `r`. If `r=0`, all shortfalls are zero, so equality
holds as well. The family is nonempty because it contains the projections.

For `x=(5,-2)` and `y=(4,1)`, the two replacement directions have losses one
and three. Nothing bounds absolute value: adding any common real offset
preserves these losses. This gives a small complete two-sided argument of the
*shape* sought in T1. It is only an elementary profile result, following the
same monotonicity/shift reasoning already used in F03-C41; arbitrary models,
evidence updates, and resource-sensitive programs are not covered by it.

### 4.2 Why the context budget belongs in the theorem

For scalar finite signed `x,y`, suppose a permitted use is `C_k(z)=kz` and costs
`k` work units, for integer `0<=k<=b`. Direct calculation gives

$$\sup_{0\leq k\leq b}[C_k(x)-C_k(y)]_+=b[x-y]_+.$$

For `x=1,y=0`, finite budget `b` gives loss `b`. Permitting every integer `k`
instead gives infinite loss. This example limits *amplification*, not the
carrier of values. It explains why “small difference in every conceivable
future use” may be the wrong task question. It does not assert that copying
trivializes all contextual metrics; S19 explicitly distinguishes fragments.

### 4.3 Approximate indistinguishability is not an exact quotient

With symmetric distance `|x-y|` and tolerance one, `0` is close to `3/4` and
`3/4` is close to `3/2`, but `0` is not close to `3/2`. Equivalence classes cannot
be obtained merely by declaring every pair within tolerance equivalent. Taking
a transitive closure changes the meaning and can merge arbitrarily distant
points. This leaves graded chaining intact: the allowances add rather than
staying fixed. T2 should therefore specify an exact congruence, a cover, a
one-sided approximation relation, or another suitable object, not assume that
one construction answers all four questions.

### 4.4 Finite adequate evidence despite a failure of exact compactness

For a nonnegative extended quantity `P`, consider the source-inspired premises
`2^(-n) |- P`, meaning `P<=2^(-n)`, for every integer `n>=1`. All premises force
`P=0`, but any finite prefix through `N` permits `P=2^(-N)>0`.

For any declared positive tolerance `delta`, choose `N` with `2^(-N)<=delta`.
That single premise already gives `P<=delta`. A strict target uses a strictly
smaller dyadic bound. Thus in this example finite adequate certification is
possible even when exact zero needs the infinite information. This reinterprets
S12's known noncompactness witness, not a general approximate-completeness
result. Extending it to a language with discontinuous tests, hard constraints,
noncompact model classes, or unbounded observations needs new assumptions and
proof. Positive slack by itself has not been proved sufficient in all of those
settings.

## 5. A focused handoff, not a premature selection

For the next foundation-selection work, I would bring a short list of result
questions rather than a large list of desired theorems:

1. Which admitted consumer or composition has a useful conclusion that a scalar
   baseline cannot derive, and what minimal extra information makes it possible?
2. Can the chosen representation support an independently defined, sharp
   operational loss characterization, or a constructive adequate abstraction?
3. Can a meaningful fragment be translated to a known calculus with the right
   guards, and can its proofs or witnesses be checked without trusting a score?

For S, the positive baseline is cheap inference in a genuinely summary-sufficient
fragment. For P, it is retaining just the relevant joint/context structure.
For T, it is compositional reasoning across downstream purposes. For G, it is
preserving feasible tradeoffs and witnesses without assuming scalarization
recovers them. These are assessment questions, not evidence that all candidates
already solve the same problem.

The literature comparisons make **T0 plus one independently meaningful
characterization** a stronger aim than merely extending the numeric range of
truth values. Signed arithmetic, nonnegative penalties, and familiar Boolean
fragments are useful building blocks. What would make this project distinctive
is a justified connection between that calculus, permissible uses, and preserved
pragmatic value. F04 and Gate A still decide the actual development question.

## 6. Evidence and inspection boundary

The work is a same-agent source audit and research proposal. S19–S21 are
added for the exact new questions above; the original eighteen references remain.
The Giacobazzi–Ranzato–Scozzari abstract is a lead, not a numbered imported
result. No new theorem of a final calculus, independent review, or publication
novelty is asserted. The candidate/input assumptions in existing notes are not
silently changed.

The [agenda register](F03_calculus_agenda.json) records attributes and target
status for later tasks. It is a human-readable research plan in structured form,
not a new proof oracle. The [small checks](../checks/f03_theorem_agenda.py) validate
finite illustrations and metadata only. The [session record](../work_logs/F03_2026-09-24_S9.md)
records source locators, actual measured time and the still-binding F03 minimum.
