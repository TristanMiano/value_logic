# F03 — External foundations audit

Research date: September 22, 2026. Source revision:
`65e91d9b46bf61566160de9dbdcb4a1a98b33f02`.
Status: **first audit pass; F03 remains in progress until the task record closes**.
No Gate A decision or permanent calculus selection is made here.

The objects compared are the four candidates in
[the F02 comparison](../foundations/02_candidate_semantics.md): evaluated scalars
(S), aligned value profiles (P), continuation-value transformers (T), and
achievable guarantee sets (G). The purpose is to identify usable antecedents and
hypothesis mismatches, not to find a citation for a predetermined design.
The [bibliography](../references.bib) records stable source identities; the
[source manifest](F03_sources.json) records inspected versions and locators.

## 1. What the audit changes

The four candidates have substantial established mathematical antecedents.
A familiar carrier or an elementary representation result should not itself be
advertised as a new logic. What still needs development is an explicit
operational consequence relation, justified composition under the declared
information access, and evidence that its retained structure is useful.

Three distinctions deserve particular attention in the next research work:

* A formula representing a function by infinitely many choices does not give a
  finite expression, an efficient algorithm, or an available policy witness.
* A theorem about all joins, complete lattices, or nonnegative costs does not
  automatically apply to finite menus of signed real costs.
* Numerical proximity, directional improvement, possible outcomes, and
  achievable guarantees use different orders and quantifiers. Their inference
  directions must be stated rather than transferred by analogy.

None of these is a refutation of F02's explicitly scoped constructions. The
comparison below classifies exact overlaps, restricted imports, and work still
owed before applying a general theorem. Original finite mapping arguments are
kept separately in [the mapping note](01a_import_boundaries.md).

## 2. Eight primary-source checks

The short source cards state only what is used. Page numbers are printed page
numbers unless a PDF index is expressly supplied. A theorem number belongs to
its inspected version, not automatically to a later publication.

### S01 — Cousot and Cousot: abstract interpretation

**Source.** Patrick Cousot and Radhia Cousot, *Abstract Interpretation: A Unified
Lattice Model for Static Analysis of Programs by Construction or Approximation
of Fixpoints* (POPL 1977, pp. 238–252). Inspected the authors' scan, especially
§6 (p. 242) and Appendix hypotheses H1–H3 and Theorems T1–T2 (pp. 251–252).

**Usable result.** For complete ordered domains and monotone transfer maps, an
abstraction/concretization pair satisfying the stated adjunction-style
conditions transports local simulation inequalities into fixed-point bounds.
The inspected presentation includes `alpha gamma = identity` and
`identity <= gamma alpha`.

**Project mapping.** This supplies a reference for distinguishing concrete
semantics from a sound summary. It does not turn ordinary averaging into a
universal abstraction, nor make a raw real vector domain complete. F02's acyclic
calculations need not adopt recursive fixed-point semantics. Explicit polarity
is required when moving from possible outcomes to achievable guarantees.

**Disposition:** foundational comparison; no fixed-point theorem imported for
an uncompleted F02 domain. See mapping M01.

### S02 — Mardare, Panangaden and Plotkin: quantitative equational reasoning

**Source.** Radu Mardare, Prakash Panangaden and Gordon Plotkin, *Quantitative
Algebraic Reasoning* (LICS 2016, pp. 700–709). Inspected the institutional accepted
manuscript, Definitions 2.1 and 3.1, Definition 4.1, and the §5 theorem statements.

**Usable interface.** Quantitative equations bound an extended symmetric metric.
Definition 2.1 has a triangle rule, a common-error nonexpansiveness rule, and an
infinitary Archimedean rule. The inspected basic theories use variable-premise axioms. Definition 3.1 requires each operation to be
nonexpansive for the maximum component distance.

**Project mapping.** This is a concrete antecedent for a tolerance-aware
calculus, not an automatic semantics for desirability. Minimum, maximum and
fixed convex mixtures fit familiar max-metric bounds; unscaled binary addition
does not. A one-sided guarantee is not automatically a metric equation.

**Disposition:** definitions and rule hypotheses verified. The strong
completeness theorem is not imported into a different signature, directed
relation, or purely finitary proof system. See M02 and supplement S09.

### S03 — Kozen: probabilistic programs as linear operators

**Source.** Dexter Kozen, *Semantics of Probabilistic Programs*, JCSS 22(3),
328–350 (1981). Inspected §3.3, clauses 3.3.1–3.3.5 (pp. 339–340), and Theorems
3.3.8–3.3.9 (p. 341), from the author's PDF.

**Usable result.** The distribution semantics assigns a positive linear
contraction to a program and composes these operators. It accounts for possible
nontermination; preservation of all probability mass is not automatic.

**Project mapping.** Finite backward evaluation is obtained by dualizing a
forward transition matrix. It provides the stochastic-linear fragment of T.
Immediate rewards make the backward map affine, and optimization or ambiguity
adds further structure. For a substochastic matrix, a common continuation shift
is multiplied by the surviving row mass; F02's exact shift law requires row sums
one.

**Disposition:** exact finite specialization plus an explicitly derived dual
mapping, not identification of all T with Kozen's linear program denotations.
See M03.

### S04 — Ovchinnikov: finite max–min representation

**Source.** Sergei Ovchinnikov, *Max-Min Representation of Piecewise Linear
Functions*, arXiv:math/0009026v1 (2000); journal version, Beiträge zur Algebra
und Geometrie 43(1), 297–302 (2002). Inspected preprint Definitions 2.1–2.2,
Lemma 4.1 and Theorem 4.1 with its proof.

**Usable result.** A continuous function given by finitely many affine pieces on
the stated convex domain has a finite maximum-of-minima representation using
its affine components. The converse is also established.

**Project mapping.** This is the load-bearing external result behind F02-C25.
For a global finite piecewise-affine map, monotonicity and common-shift
homogeneity separately constrain each essential affine slope to the probability
simplex. Those extra conditions come from the project's mapping argument, not
from the theorem alone.

**Disposition:** exact antecedent for the finite representation step. No
expression-size, learnability, restricted-primitive, or witness-preservation
claim follows. See M04.

### S05 — Akian, Gaubert and Hochart: monotone homogeneous maps

**Source.** Marianne Akian, Stéphane Gaubert and Antoine Hochart, *Minimax
Representation of Nonexpansive Functions and Application to Zero-Sum Recursive
Games*. Inspected arXiv:1605.04518v2 (2017), §2, Theorem 3.4, Corollary 3.8 and
§3.2. Journal publication: Journal of Convex Analysis 25(1), 225–240 (2018).

**Usable result.** Corollary 3.8 represents a monotone additively homogeneous
functional on an order-unit space by a minimax of affine expressions. In finite
dimension the inner linear coefficients lie in the simplex; the outer index
need not be finite. The separate no-instantaneous-payment representation also
requires positive homogeneity.

**Project mapping.** T's order/shift/nonexpansiveness interface is established
territory. This general minimax theorem must not replace S04's finite-piece
hypothesis, or silently remove immediate reward offsets.

**Disposition:** exact structural comparison and useful separation of finite
versus general representations; not a proof that every admitted map has a
finite operational realization. See M04.

### S06 — Bistarelli, Montanari and Rossi: semiring constraints

**Source.** Stefano Bistarelli, Ugo Montanari and Francesca Rossi,
*Semiring-Based Constraint Satisfaction and Optimization*, JACM 44(2), 201–236
(1997). Inspected the author-uploaded journal text: Definitions 2.1–2.2,
Theorem 2.9 and the idempotence condition in Theorem 4.16.

**Usable interface.** The paper's c-semiring has arbitrary, including infinite,
additive joins. Its multiplicative identity is additive top. The induced order
is a complete lattice. Order-independence of the cited local-consistency
algorithm additionally assumes idempotent multiplication.

**Project mapping.** G's finite union and Minkowski-sum algebra resembles the
framework, but finite-generated signed-cost upper sets do not meet those full
hypotheses. Nonnegative costs repair the unit/top mismatch, not arbitrary-join
closure; Minkowski addition remains nonidempotent.

**Disposition:** useful algebraic antecedent with three explicit import
barriers, not a turnkey c-semiring solver for G. A completion is described only
as a possible comparison construction. See M05.

### S07 — Boyd and Vandenberghe: vector optimization and scalarization

**Source.** Stephen Boyd and Lieven Vandenberghe, *Convex Optimization* (2004),
the coauthor's UCLA-hosted book. Inspected §§2.3.1 and 2.5.1, and §4.7.4,
pp. 178–180, including Figure 4.9 and equation 4.62.

**Usable result.** Positive dual weights yield Pareto optima; nonconvex fronts
can contain unsupported efficient points. In the convex case the converse uses
nonzero nonnegative weights, whose arbitrary minimizers need not all be Pareto
optimal. The relevant upper image is achievable objectives plus the ordering
cone.

**Project mapping.** This directly contextualizes F02-C12, C17 and C18.
Weighted optimum values retain a convexified upper-image description, not every
deterministic feasible budget. The project's finite hull-recovery and lottery
calculations remain explicit specialization arguments.

**Disposition:** standard antecedent. Neither existence of an optimizer nor
permission to randomize follows merely from a scalarization formula. See M06.

### S08 — Iyengar: robust dynamic programming

**Source.** Garud Iyengar, *Robust Dynamic Programming*, Mathematics of Operations
Research 30(2), 257–280 (2005). The inspected full text is the author's CORC
TR-2002-07 revision of May 4, 2004: §2, Assumption 1, equations 9–11 and Theorem 1.
The locators refer to that report, not an assumed identical journal layout.

**Usable result.** Under rectangularity of admissible history-conditioned
transition choices, finite-horizon robust values obey a Bellman recursion. The
finite state/action/uncertainty specialization avoids the report's general
supremum and integrability subtleties.

**Project mapping.** This supports T's carefully scoped sequential robust
interpretation. Rectangularity is freedom to paste allowed conditional choices,
not probabilistic independence of all variables. A shared unknown parameter
across stages generally prevents this pasting.

**Disposition:** restricted import with an explicit information/uncertainty
contract. Preserve F02's shared-parameter counterexample and do not silently
reveal a hidden parameter to the decision maker. See M07.

## 3. Targeted supplementary check

### S09 — A known route beyond the common-error metric rule

Matteo Mio, Ralph Sarkis and Valeria Vignudelli, *Beyond Nonexpansive Operations
in Quantitative Algebraic Reasoning*, arXiv:2201.09087v1 (2022), was checked
specifically because S02's baseline rule excludes ordinary addition. Sections
2.3 and 3.1 admit selected generalized distance axioms and operation-specific
liftings preserving isometric embeddings; Definition 3.11 and Theorem 3.14 give
the corresponding rule interface and soundness statement.

The inspected version uses distances in `[0,1]`. That bounds a distance, not the
underlying set of values. It is not an unrestricted-real-error or universal
regret-calculus theorem. The mapping note gives a separate elementary capped-sum
example; proving that an eventual Value Logic signature meets the complete
lifting hypotheses is still an obligation. This is a checked alternative, not
an assertion that failed max-metric nonexpansiveness forces abandonment of
quantitative algebra.

### S10 — The 2024 generalization removes operation nonexpansiveness

Matteo Mio, Ralph Sarkis and Valeria Vignudelli, *Universal Quantitative Algebra
for Fuzzy Relations and Generalised Metric Spaces*, LMCS 20(4:19), 19:1–19:56
(2024), was checked in the journal PDF: Definitions 3.1–3.6, the substitution
scheme in Definition 4.1, Theorems 4.4 and 5.13, and the comparison in §9.1.

Unlike S02, its algebra operations can be arbitrary functions. Variable
interpretations remain nonexpansive for an explicitly supplied `[0,1]`-valued
relation, and substitution must prove preservation of all the required variable
relations. Soundness and completeness concern that full equation language and
proof system; the infimum/Archimedean scheme is not a finite search algorithm.

This changes the follow-up priority: addition's failure under S02 is not a
barrier to expressing an addition-based theory. The price is explicit relational
premises, operation laws, and substitution obligations. The paper's distinction
between equations and zero-distance judgments also matters when separation is
not assumed. See M08 for a simple failed unrestricted substitution. We have not
checked every free-algebra or monadicity proof or imported their entire metatheory.

### S11 — Relational-algebra variety results are not a ready deduction engine

Jan Jurka, Stefan Milius and Henning Urbat, *Algebraic Reasoning over Relational
Structures*, arXiv:2401.08445v2 (June 9, 2024), was checked in §§3–6. The HTML's
broken automatic theorem numbering is not used as an invented locator.

Its relational carriers satisfy a declared infinitary Horn theory; operations
use liftings that preserve embeddings. The §4.2 variety result concerns closure
under products, subalgebras and the stated **c-reflexive** quotients, not all
surjective images. The §5 exactness result adds a preservation condition for
relation-reflecting surjections. Section 6 explicitly leaves derivation of a
complete concrete deduction system to further work.

This is a useful comparison for genuinely ordered or relational candidates,
including possibilities beyond one symmetric metric. It is not a result that
our finite G carrier automatically satisfies those closure hypotheses, and it
does not supply an implemented sound-and-complete Value Logic reasoner. A full
translation of a candidate signature remains future work; this is a targeted
hypothesis check rather than adoption of the categorical framework.

## 4. Candidate-to-literature disposition

| Candidate | Closest checked antecedents | Surviving distinction to investigate |
|---|---|---|
| S: evaluated scalars | S02, S07, S09–S10; S03 for linear expectations | Fix task, scale and operation before treating a number as sufficient. Numerical order is not every possible contextual decoder. |
| P: aligned profiles | S01 and S02; S03's joint-distribution semantics | Preserve shared indexing or an explicitly adequate joint abstraction. Averaging is not a homomorphism for every nonlinear composition. |
| T: continuation maps | S03–S05, S08 | Separate total from partial kernels, finite syntax from infinite representation, and extensional values from permitted information and witnesses. |
| G: achievable budgets | S06–S07; S01 and S11 as order/polarity comparisons | Distinguish finite algebra from complete c-semiring, signed from nonnegative costs, and underapproximated guarantees from optimistic outer approximations. |

The source mappings do not rank these candidates. F04 still needs adversarial
comparison of their actual representations, and Gate A still needs the complete
research evidence and timing record. Literature familiarity is not the criterion
for choosing a winner.

## 5. Direct source navigation and remaining checks

- **S01** — [Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints](https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml). Exact inspected copy and locators: `F03_sources.json`.
- **S02** — [Quantitative Algebraic Reasoning](https://strathprints.strath.ac.uk/70265/). Exact inspected copy and locators: `F03_sources.json`.
- **S03** — [Semantics of Probabilistic Programs](https://www.cs.cornell.edu/kozen/Papers/ProbSem.pdf). Exact inspected copy and locators: `F03_sources.json`.
- **S04** — [Max-Min Representation of Piecewise Linear Functions](https://arxiv.org/abs/math/0009026). Exact inspected copy and locators: `F03_sources.json`.
- **S05** — [Minimax Representation of Nonexpansive Functions and Application to Zero-Sum Recursive Games](https://arxiv.org/abs/1605.04518). Exact inspected copy and locators: `F03_sources.json`.
- **S06** — [Semiring-Based Constraint Satisfaction and Optimization](https://bista.sites.dmi.unipg.it/papers/index-old.html). Exact inspected copy and locators: `F03_sources.json`.
- **S07** — [Convex Optimization](https://www.seas.ucla.edu/~vandenbe/cvxbook.html). Exact inspected copy and locators: `F03_sources.json`.
- **S08** — [Robust Dynamic Programming](https://pubsonline.informs.org/doi/abs/10.1287/moor.1040.0129). Exact inspected copy and locators: `F03_sources.json`.
- **S09** — [Beyond Nonexpansive Operations in Quantitative Algebraic Reasoning](https://arxiv.org/abs/2201.09087). Exact inspected copy and locators: `F03_sources.json`.

- **S10** — [Universal Quantitative Algebra for Fuzzy Relations and Generalised Metric Spaces](https://lmcs.episciences.org/14876). The journal PDF is the inspected version.
- **S11** — [Algebraic Reasoning over Relational Structures](https://arxiv.org/html/2401.08445v2). The version and section locators are explicit.

The two 2024 leads initially found only as abstracts were subsequently promoted
to targeted supplementary checks S10–S11 after reading the relevant full-text
sections. That does not mean every proof in those articles has been verified.
The eight core cards remain the main audit; the three supplements answer specific
obstacles raised by those cards rather than expanding this into an exhaustive survey.

The remaining source review should recheck the basic-premise/Archimedean
conditions and the free-algebra argument for any contemplated completeness
import, construct the exact proposed signature-to-source translation, and distinguish a
source's representation theorem from an information-legal operational witness.
The current cards do not claim a page-by-page verification of entire papers.

## 6. Publication and task boundaries

These checks establish relevant antecedents and explicit conditions for reuse.
They do not establish novelty, an adopted calculus's completeness, a practical
speed advantage, or a readiness-gate pass. In particular, there is no claim that
a representation theorem automatically gives an efficient or information-legal
procedure.

The session record must determine whether F03's L60 floor has been reached.
Until then the F03 checkbox remains unchecked and the next pointer remains F03,
even when the present notes are useful for later work. Mathematical proofs,
source-access limits and executable checks have different evidence roles.


## 7. Continuation: proof-system and solver checks

[S2's focused audit](01b_proof_system_audit.md) rechecks the source hypotheses,
adds S12 (*Rational Lawvere Logic*, CSL 2026), and works explicit adapters for
substitution, signed arithmetic, finite budget queries, factor elimination and
robust action coupling. The source manifest preserves S1 entries and adds dated
reinspection records rather than silently replacing what was originally checked.
There are still eight core sources; the targeted supplement count is now four.
Task status and exact measured literature time are in the
[S2 record](../work_logs/F03_2026-09-22_S2.md). No whole-paper independent
verification, adopted calculus, or readiness gate is claimed.


## 6. S3 continuation: the author's range bridge

The [Lawvere/value bridge audit](01c_lawvere_value_bridge.md) distinguishes
reinterpretation, finite signed encoding, a restricted negative-cone translation,
and signed values with nonnegative loss grades. S13 is a targeted Abelian-logic
comparison motivated by the author's request for a two-sided range; S01-S12
remain unchanged as source identities. The manifest records the actual inspected
2002 version and source-specific locators, not a claim that the whole paper is
verified. S12's finite-polynomial theorem is the explicit import target, with
finitising premises covering both hypotheses and conclusion. A retrieved
normalization-paragraph inconsistency remains documented. This continuation
adds evidence without completing L60 or choosing the phase's calculus.


## September 23 continuation: belief and KL lead

[The S4R1 audit](01d_belief_kl_objectives.md) records five targeted primary
supplements, precise finite belief/cost/transformer adapters, and their limits.
The broad blog embeddings are not imported from an incomplete math rendering.
Logarithmic identities and RLL's arithmetic theorem have distinct premises.
F03 remains partial; see [actuals](../work_logs/F03_2026-09-23_S4R1_actuals.json).


## S5 consolidation — context preservation and convexity (September 24, 2026)

[The new import-contract note](01e_belief_value_import_contracts.md) compares
belief/value duality with S07's conjugacy and partial-minimization hypotheses,
adds exact rational logarithm/KL enclosures for the S12 arithmetic boundary,
and records a scoped counterexample to S16 Proposition 1. No new bibliography
entry is added. A targeted retry of the earlier S02 rule-page inspection
succeeded on PDF page1 but again failed on page2; the stronger parsed reflection
sentence remains unused. F03 is still partial; no whole-paper independent
verification, fixed core, or readiness-gate pass is claimed.


## S6 consolidated handoff (September 24, 2026)

[The source-use handoff](01f_consolidated_source_handoff.md) and
[structured import register](F03_import_contracts.json) consolidate the existing
18 references without adding a source. They distinguish conditional theorem
interfaces from comparisons, unreadable leads and rejected stronger claims.
Two finite adapters clarify directed gains for signed profiles and the boundary
between pointwise arithmetic, uniform witnesses and lsc belief types. The
[session record](../work_logs/F03_2026-09-24_S6.md) keeps this checkpoint partial;
189 combined F03 checks are not a substitute for L60 or a later soundness gate.

## S7: concrete source-rule derivations

The [source-rule note](01g_checked_source_derivations.md) supplies two small
conditional RLL derivations and their complete syntax certificates, alongside
S10's explicit substitution premises and S13's signed cancellation boundary.
No source is added and no permanent calculus is selected. Its validator handles
only the listed source-rule subset; it does not establish source completeness,
operational witnesses, or calibration of the assumptions. The latest timing and
partial status are recorded in [S7](../work_logs/F03_2026-09-24_S7.md).


## S8: full contexts and existing witnesses

[The context/witness audit](01h_context_and_witness_audit.md) sharpens two uses
of existing sources, without adding references. Related-variable elimination
needs an extension argument; optimality equations need a satisfiability witness.
Finite countermodels and positive constructions are separated from source
theorems. The updated register records these as scoped adapter boundaries, not
new mandatory primitives. [S8](../work_logs/F03_2026-09-24_S8.md) records the
still-partial task status and actual source-review credit.
