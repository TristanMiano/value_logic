# F10 — external audit of the finite core

Research contributor: **Codex (GPT-6)**. Primary-source inspection: September
30, 2026. Status: **complete at F10 audit/calibration scope; L45 satisfied**. Base: `ed009e5` (F09). The work record is
[F10 S1](../work_logs/F10_2026-09-30_S1.md). This audit does not pass Gate B.

The author's novelty objective concerns the **project's contribution as a
whole**. Established tools, techniques and methods are intended building
blocks. The question is whether their use here supports a useful, specific
advance, rather than whether every local lemma is unprecedented.

## 1. Scope and classification

The object audited is the finite rational, signed, continuous piecewise-affine
(CPWA) language of F05, the F06/F07 kernel, F08's target-unit characterization
and revision constructions, and F09's fragment/presentation comparisons.
Finite nonempty polyhedral cases, admitted witnesses, fixed interpretations,
positive named conversions and literal request matching remain requirements.

Five checks organize the audit: (A) arithmetic and representation; (B) typed
consequence; (C) certificates and error bounds; (D) revision and retained
evidence; (E) abstraction and phase-one information. They are argument checks,
not a source-count target. F03 remains the wider survey; this note checks the
now-specific dependencies and follows the closest newly identified antecedents.

Classification vocabulary:

* **Established ingredient:** a checked external result or standard technique
  supplies the mathematical mechanism. A local reconstruction does not change
  its originality status.
* **Adaptation:** additional project assumptions or proof-format obligations
  must be discharged before that mechanism applies.
* **Independent local derivation:** describes how this repository obtained a
  result, not a claim of independent priority or external verification.
* **Contribution candidate:** a project-level question and discriminating
  comparison worth pursuing. Search coverage does not certify an open problem.

## 2. Check A — signed arithmetic, CPWA representation and Boolean fragments

**Claims checked:** F08 U1/U11's finite normalization and F09 B1/B2 and
presentation comparisons. Read [A01](#a01-abelian-and-lukasiewicz-calculi),
[A02](#a02-max-min-representation), [A03](#a03-rational-lawvere-logic), and
the closer scalar proof theory [A15](#a15-riesz-space-proof-theory).

Signed addition, subtraction and lattice extrema sit naturally in established
ordered-group/vector-lattice mathematics. Rational scaling is an additional
divisible/vector-space operation; it must not be attributed wholesale to an
integer-coefficient source calculus. F08's numerical normal form is established
CPWA machinery. Its zero-budget native equality traces are the project-specific
adaptation: a semantic identity cannot silently become a rewrite rule in the
kernel's opaque nonlinear normalizer.

A15 supplies a still closer established account of the scalar/lattice part:
Riesz-space hypersequents, completeness, cut elimination and rational-scalar
conservativity. HR's base signature has zero, not all native affine constants;
the paper separately adds a positive unit in its modal extension. This narrows
the originality boundary further. The typed source interface and checked
replay still require a translation; differing notation is not itself novelty.

The source max-min theorem uses a convex domain. Our terms are globally defined
on real coordinate space before restriction to a finite union of source cases;
therefore no extension of that theorem to arbitrary nonconvex domains is needed.
The direct syntax construction in F08 is sufficient and preserves rational
coefficients. Neither source representation nor native completeness bounds the
size of the expanded expression or supplies a competitive producer.

F09's Boolean losses reverse the conventional truth orientation: loss 0 is
true, loss 1 false. The bounded Boolean subalgebra and ordinary propositional
entailment reduction are reusable foundations. They do not identify the full
signed calculus with Boolean logic or with a logic using an infinite truth
value. The positive-affine presentation results likewise concern a specified
budget interface; changing coordinates alone is not a novel value theory.

**Decision:** retain the carrier and proofs, describe them as established
arithmetic with checked native adaptations. No competing paper examined here
automatically replaces the typed kernel or proves its operational guarantees.

## 3. Check B — exactly which completeness theorem applies

**Claim checked:** [F08 U1](../derivations/04_characterization.md),
`K_C(t,s;b) iff C|u satisfies t-s <= b`, with finite rational b. Compare
[A03](#a03-rational-lawvere-logic), [A04](#a04-quantitative-algebraic-reasoning)
and [A05](#a05-generalised-quantitative-algebra).

These are three different completeness contracts. Native bounds are signed,
directed and unit-indexed. Symmetric nonnegative metric equations do not supply
that contract. Addition accumulates two error allowances, and scaling may have
gain greater than one, so max-metric nonexpansiveness cannot be assumed. The
generalised quantitative-algebra framework is a closer comparison, but its
model class, syntax and potentially infinitary rules still have to be matched.
RLL's nonnegative extended carrier and rational operations also differ from
finite signed CPWA terms. Its finite-sequent result is not an unrestricted
compactness or native certificate theorem.
These comparisons do not establish that an existing framework cannot encode
K. Such an encoding would need to preserve the selected model, premise,
unit-access and proof-reception contracts; a notation change is insufficient.
In particular, A05 does not impose symmetry or a zero diagonal: its [0,1]
relation range alone does not rule out recoding directed signed comparisons.
The difficult comparison is the whole consequence and reception contract,
not merely the numerical range of a relation.

The local construction earns the exact U1 statement through an ancestor-unit
invariant plus a native converse. With `U -> V` and the sole row
`convert(x:U) <= -1:V`, the full real source implies `x <= -1:U`; the U-reduct
does not. This obstruction survives the existence of a complete untyped
arithmetic calculus. Positivity makes numerical conversion invertible; the
proof interface deliberately need not expose an inverse conversion rule.

The unit restriction should be evaluated as a useful evidence-access policy,
not mistaken for an arithmetic discovery. If applications require full-source
consequence, an explicitly scoped policy change or a semantic backend is a
real alternative. Adding reverse rules merely to remove the counterexample
would change the intended interface. F10 selects neither change.

**Decision:** no external completeness theorem is imported as a substitute for
U1. Preserve the target reduct, graph criterion, fixed-signature assumptions
and distinction between a reduct countermodel and a full-source countermodel.

## 4. Check C — exact certificates and geometry-controlled transfer

**Claims checked:** F06/F07 affine leaves, F08's uniform replay construction,
and [U18](../derivations/04h_geometry_and_transfer.md). Compare
[A06](#a06-certified-polyhedral-minimization),
[A07](#a07-hoffmans-error-bound) and
[A08](#a08-neural-verification-proof-production). For reception of proofs
under changing authority, also compare [A16](#a16-proof-reception-and-revocation).

Nonnegative multiplier certificates, rational checking, case splits for
piecewise-affine constraints, and separating search from checking are strong
established precedents. The repository contributes its own typed request,
case-coverage, source-revision and provenance obligations. An external solver
answer without an accepted native certificate is not evidence for those extra
obligations. Conversely, a standalone Python checker is not thereby a proof
assistant verification of its implementation.

A16 also prevents treating current-context reception as a new architectural
idea. Its proof-derived capabilities retain dependencies that are checked for
revocation at use time. Native signed bounds and unit reachability differ,
but versioning, request binding and dependency checking are adaptations of
established proof-carrying patterns, not independent novelty claims.

U18 is an explicit Hoffman-style construction: with fixed matrices and every
case feasible, a finite matrix-dependent coefficient bounds distance by row
violation; a loss sensitivity bound then transfers a quantitative judgment.
The original theorem's definiteness assumptions must not be applied directly
to a seminorm with zero-cost directions. F08's coordinatewise refinement has
its own LP argument. Scaling the rows, changing conversions or changing the
coordinate gauge changes the relevant coefficient. A coefficient uniform in
the RHS is not uniform over all matrices or all unnormalised loss expressions.

**Decision:** credit this as a local reconstruction and native realization of
classical error-bound/duality methods. The useful future question is whether
this certificate interface gives sharper or cheaper revision handling in a
declared workload. ReLU verification papers establish verification methods;
they supply no evidence that an ordinarily trained network has learned this
project's logic or its task-relative meaning.

## 5. Check D — revision, minimization and alternative supports

**Claims checked:** F08 U11/U13, F07 alternative supports and F09's affine
transport opportunity. The close sources are [A09](#a09-parametric-polyhedra),
[A10](#a10-proof-minimization), [A11](#a11-incremental-conflict-reuse),
[A12](#a12-assumption-based-truth-maintenance) and
[A13](#a13-provenance-semirings).

The mathematical budget in U11 is a finite max of minima of affine functions
of the source RHS. Fixed dual feasible sets and their optimality regions are
parametric linear programming. Retaining all relevant alternatives is a sound
baseline, not itself a new optimization principle. A09's normalized projection
problem is not identical to U11's query problem: its irredundancy theorem has
normalization hypotheses, and irredundant projected inequalities are not
automatically a smallest shared native proof DAG.

There are at least four different retention objectives:

| Objective | Appropriate baseline | Extra obligation in this project |
|---|---|---|
| Justify today's conclusion cheaply | Current-proof dependency minimization | Preserve the exact signed bound and literal request |
| Reuse an old conflict after strengthening | Refinement-based conflict inheritance | Check refinement; relaxation cannot inherit a conflict for free |
| Keep derivability after assumptions disappear | Alternative-support labels | Distinguish a known support family from all semantic proofs |
| Keep optimal quantitative bounds throughout a declared revision family | Parametric LP envelopes plus support restrictions | Compile/check the full retained alternatives and current context |

These mechanisms can be combined. A11 is not a competitor to be dismissed
because it studies networks; its monotone cases belong in our baseline suite.
Nor does failure of monotone inheritance under relaxation make safe handling
of relaxation unprecedented: ordinary incremental solving, truth maintenance
and rechecking already provide approaches. A13 is another precedent for
symbolic dependency information evaluated under changed annotations. Its
semiring factorization is not automatically a theorem for a circuit containing
all of K's min, max, additive and scaling budget operators.

A current smallest proof can discard tomorrow's best alternative. U11's
worked family already witnesses this. Conversely, preserving every possible
future optimum can be much more expensive than solving today's query. The
useful research question is the **workload-dependent tradeoff** among retained
information, achieved loss bounds, new search and exact checking. It should
include total construction cost and the number of updates needed to recover
that cost. Merely counting smaller proof files would miss the intended gain.

**Decision:** classify U11/U13 as independently reconstructed adaptations of
parametric optimization and support maintenance to the native calculus. A
compact, checked revision experiment is a plausible project-level contribution
candidate, with low-to-medium confidence about distinctiveness and no verified
priority claim. The close combined proposal in
[calibration C09](02a_research_calibration.md#c09-the-combined-retention-aim-also-has-a-close-proposal)
makes the actual application result essential. Generic envelope pruning, support antichains or proof
dependency deletion alone are insufficient grounds for originality.

### Import caution: strict refutations versus weak upper bounds

The inspected A10 Algorithm 2 permits removal cost `delta <= abs(Delta)`.
For a refutation that specifically requires `Delta < 0`, the boundary
`Delta = -1, delta = 1` leaves zero and no longer gives a strict contradiction.
A weak bound may legitimately permit equality. Any adaptation here must
recheck the residual inequality at the correct strictness, rather than copy a
comparison sign from pseudocode. This is a local import caution, not a claim
that the published implementation is unsound; its code was not audited. No
A10 algorithm has been imported into this repository.

## 6. Check E — information and abstraction

**Claims checked:** F08 characteristic probes and source substitution;
F09 phase-one consumers, joint conflicts and source refinement. Compare
[A14](#a14-abstract-interpretation-repair), with the broader phase-one antecedents
already checked in [F03's project comparison](01j_phase_one_literature_and_novelty.md).

Local completeness and abstraction repair supply a better vocabulary than
claiming a new general theory of retained information. Our fixed query
language matters: affine probes recover less information than all CPWA probes,
and a three-state assessment tag does not reconstruct the evidence that
produced it. Loss of joint information under marginal summaries is a standard
relational-abstraction issue. F09's exact adapters and witnesses state where
that issue occurs in this project's interfaces.

The target-unit reduct adds a distinct policy check. Equal full source sets
need not have equal target reducts after a row/case transformation. A source
refinement justified with inaccessible rows may expose information that the
original target-unit proof could not use. A14's concrete/abstract transformer
contract does not prove that such a transformation preserves this evidence
policy. A safe adaptation must compare the projected target reducts, not just
full-source semantics, or explicitly authorize the stronger evidence access.

F09's finite conflict/Boolean-component results remain useful exact boundary
lemmas. They are not evidence of a new global Boolean semantics, and adding
more elementary variants is unlikely to be the best next use of research time.
The larger opportunity is a worked loss-grounded task whose answer depends on
joint evidence, survives declared updates, and respects the requested access
policy. F13's scientific and bounded self-assessment cases provide places to
test that benefit without changing the phase's scope.

**Decision:** no source theorem inspected here repairs or replaces U1 merely
by being more general. Retain the local results at their stated scope and
compare an access-aware refinement adapter with an ordinary full-information
semantic baseline. Neither is automatically the right application policy.

## 7. Source-use register

All entries were accessed September 30, 2026. PDF page numbers below are the
paper's printed numbers where clear; explicit PDF-page locators are one-based.
Short paraphrases record only the checked dependency. Search snippets and
secondary summaries are not used as theorem evidence.

### A01. Abelian and Lukasiewicz calculi

George Metcalfe, Nicola Olivetti and Dov Gabbay, *Sequent and Hypersequent
Calculi for Abelian and Lukasiewicz Logics*, arXiv cs/0211021v1, November 2002.
[Primary preprint](https://arxiv.org/pdf/cs/0211021).
Read §2.3, Theorem 12; §3; §5, Theorems 62, 63 and 66; and §6's labelled
alternative to explicit hypersequent expansion.
The real ordered additive group is a characteristic model for Abelian
tautologies; the paper supplies proof calculi and relates the bounded logic to
the ordered-group setting. This licenses the arithmetic comparison, not an
import of its proof-search or complexity guarantees into K. The result is not
a theorem about named directed units or changing source fingerprints.

### A02. Max-min representation

Sergei Ovchinnikov, *Max-Min Representation of Piecewise Linear Functions*,
arXiv math/0009026v1, September 2000.
[Primary text](https://arxiv.org/html/math/0009026).
Read Definition 2.1 and Theorem 4.1. A continuous finite piecewise-linear
function on the specified convex domain has a lattice representation using
its affine components. The paper's terminology includes affine offsets.
The web rendering's later title-block date is not used as the version date.
Our application uses globally defined terms, then restricts their inputs.

### A03. Rational Lawvere Logic

Giorgio Bacci, Radu Mardare, Prakash Panangaden and Gordon Plotkin,
*Rational Lawvere Logic*, CSL 2026, DOI 10.4230/LIPIcs.CSL.2026.3.
[Published primary text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol363-csl2026/html/LIPIcs.CSL.2026.3/LIPIcs.CSL.2026.3.html).
Read syntax/semantics, Theorems 9, 11 and 17, and the quantitative-equational
embedding discussion. The carrier is extended nonnegative reals; rational
operations include multiplication and division. Finite completeness and the
polynomial fragment have explicit restrictions, including finitising premises
in the latter. Its infinity-based Boolean encoding differs from F09's finite
continuous Boolean-loss fragment. Complexity classifications are not copied
without an encoding and input-size analysis.

### A04. Quantitative Algebraic Reasoning

Radu Mardare, Prakash Panangaden and Gordon Plotkin, *Quantitative Algebraic
Reasoning*, LICS 2016.
[Author manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/25269544/LICS2016.pdf).
Read Definition 2.1 and Theorem 5.2. Quantitative equations have nonnegative
tolerances and metric rules, including symmetry, nonexpansiveness and an
infinitary Archimedean rule. Completeness is for that theory/model contract.
It is an antecedent for quantitative algebraic consequence, not a finite
signed, directed, unit-indexed native proof theorem.

### A05. Generalised quantitative algebra

Matteo Mio, Ralph Sarkis and Valeria Vignudelli, *Universal Quantitative
Algebra for Fuzzy Relations and Generalised Metric Spaces*, LMCS 2024.
[Published primary PDF](https://lmcs.episciences.org/14876/pdf).
Read Definitions 2.27 and 3.1, Remark 3.7, and the free-model construction through
Theorem 5.13/Corollary 5.14. The fuzzy relation takes values in [0,1], without
requiring metric axioms or nonexpansive operations. Interpretations are
nonexpansive, however, and the quantified relational variable space can be
infinite even for finite terms. This broader completeness contract does not
automatically yield finite native CPWA certificates or the unit graph policy.

### A06. Certified polyhedral minimization

Alexandre Marechal and Michael Perin, *Efficient Elimination of Redundancies
in Polyhedra by Raytracing*, VMCAI 2017.
[Author PDF](https://www-verimag.imag.fr/~perin/research/paper/17/marechal_perin_VMCAI_2017.pdf).
Read §3, Theorem 1/Algorithm 1, and §4.4. Constraint redundancy can be certified
by nonnegative combinations, and nonredundancy by a separating point. Search
may use floating point while candidates are checked rationally, with exact
fallback. Correctness, precision and minimality certificates are distinct.
These are direct antecedents for certificate checking and later pruning
baselines; future-revision completeness is an additional specification.

### A07. Hoffman's error bound

Alan J. Hoffman, *On Approximate Solutions of Systems of Linear Inequalities*,
Journal of Research of the NBS 49(4), 263–265, October 1952.
[Original scan, mirror](https://upload.wikimedia.org/wikipedia/commons/0/07/On_approximate_solutions_of_systems_of_linear_inequalities_%28IA_jresv49n4p263%29.pdf).
Read §2's theorem and proof, and §3's norm discussion. Consistent inequalities
admit a distance bound in terms of positive residuals. The proof chooses over
finitely many row subsets: its constant depends on the matrix and measuring
functions, not the feasible RHS. Those functions are continuous, positively
homogeneous and definite. The NIST endpoint failed; the linked file is the
original paper, not a summary from the hosting site's encyclopedia.

### A08. Neural verification proof production

Omri Isac, Clark Barrett, Min Zhang and Guy Katz, *Neural Network Verification
with Proof Production*, FMCAD 2022.
[Author PDF](https://theory.stanford.edu/~barrett/pubs/IBZ%2B22.pdf).
Read §§III–V. A proof tree records case splits and linear refutations, with
justifications for bound-tightening lemmas. This is a close established
producer/checker architecture for piecewise-linear verification. Its network
verification scope is separate from discovering interpretable reasoning in
trained networks. No performance result from that system is attributed to K.

### A09. Parametric polyhedra

Alexandre Marechal, David Monniaux and Michael Perin, *Scalable
Minimizing-Operators on Polyhedra via Parametric Linear Programming*, SAS 2017.
[Author PDF](https://www-verimag.imag.fr/~perin/research/paper/17/marechal_monniaux_perin_SAS_2017.pdf).
Read §§3–6, especially §5's optimality-region exploration and §6.2 Theorem 1;
§7's experiments and §8's degeneracy limitation.
Projection is expressed through parametric objectives; rational computation
and certificate generation are integrated. The irredundancy result concerns
the nonconstant pieces of a normalized parametric problem. It is a close
algorithmic starting point, not a smallest-proof or arbitrary-revision theorem
for our unnormalized native traces.

### A10. Proof minimization

Omri Isac, Idan Refaeli, Haoze Wu, Clark Barrett and Guy Katz, *Proof
Minimization in Neural Network Verification*, VMCAI 2026, pp. 99–124.
[Published version on author site](https://www.katz-lab.com/_files/ugd/e8497d_31deeb9d38cd4dcdaed789997ad93209.pdf);
[preprint](https://arxiv.org/abs/2511.08198), November 2025.
Read §3.1 dependency extraction, §3.2 Algorithms 2–3 and Theorem 2, and the
global-sharing discussion. The cardinality result fixes a proof vector and its
dependency choices; the global procedure is heuristic. It is not a theorem of
globally smallest proofs across future contexts. Both inspected versions have
the comparison sign noted in the import caution above. The published version,
not the preprint's date, determines the venue citation.

### A11. Incremental conflict reuse

Raya Elsaleh, Liam Davis, Haoze Wu and Guy Katz, *Incremental Neural Network
Verification via Learned Conflicts*, arXiv 2603.12232v1, March 12, 2026.
[Primary preprint](https://arxiv.org/html/2603.12232v1).
Read Definition 2, Lemma 1, Theorem 3.1, Algorithms 1–2, §6 and Appendix B.
Reuse is sound for a fixed network when both input and output query regions
shrink. The implementation stores activation-phase conflicts and uses SAT for
pruning/propagation. The paper explicitly leaves conflict minimization and
richer reusable information for further work. Its evaluated benefit is
workload-dependent; we import neither its speedups nor a guarantee that
arbitrary withdrawals satisfy refinement.

### A12. Assumption-based truth maintenance

Johan de Kleer, *An Assumption-based TMS*, Artificial Intelligence 28 (1986),
127–162. [Author-hosted original scan](https://www.dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf).
Read §§4.1–4.7 and §4.9. Labels collect consistent minimal assumption
environments sufficient for a datum, relative to the supplied justifications.
Subset tests determine support in a context; alternative derivations and
nogoods are maintained. This substantially predates generic claims about
retaining multiple supports or changing contexts. Label completeness is
relative to known justifications, not an independent completeness theorem for
the problem solver's arithmetic. Retraction is represented with assumptions.

### A13. Provenance semirings

Todd J. Green, Grigoris Karvounarakis and Val Tannen, *Provenance Semirings*,
PODS 2007. [Author PDF](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf).
Read Proposition 3.5 and Theorem 4.3; §5 distinguishes recursive queries.
For positive relational algebra, symbolic provenance can be evaluated in a
commutative semiring, and appropriate homomorphisms commute with query
evaluation. This is a precise precedent for reusable symbolic annotations.
The positive query language and algebraic laws are hypotheses; signed native
budgets with both lattice extrema are not identified with that interface.

### A14. Abstract interpretation repair

Roberto Bruni, Roberto Giacobazzi, Roberta Gori and Francesco Ranzato,
*Abstract Interpretation Repair*, PLDI 2022, pp. 426–441,
DOI 10.1145/3519939.3523453.
[Author manuscript](https://iris.univr.it/bitstream/11562/1153347/1/pldi22.pdf).
Read Definition 4.8, Theorem 4.9, Theorem 4.11 and §5. Pointed shells concern
optimal local-completeness repair; their existence has explicit conditions,
including the additive-transformer characterization. Boolean guards have a
constructive case. This is not unconditional existence of a finite best
abstraction, and it does not enforce the native unit-access restriction.

### A15. Riesz-space proof theory

Christophe Lucas and Matteo Mio, *Proof Theory of Riesz Spaces and Modal Riesz
Spaces*, LMCS 18(1), article 32, February 17, 2022,
DOI 10.46298/lmcs-18(1:32)2022.
[Published primary PDF](https://lmcs.episciences.org/9100/pdf).
Read §2.1's signature, §3.1 Theorems 3.10–3.18, and §3.2 Propositions 3.19–3.20.
HR extends ordered-group proof theory with scalars; rational conclusions are
conservative over rational Riesz-space axioms. Cut elimination and decidability
are established for its specified proof system. The paper reports a separate
Coq formalization, which this audit has not built or checked. These results
are not complexity or formal-verification guarantees for the Python kernel.

### A16. Proof reception and revocation

Jamie Morgenstern, Deepak Garg and Frank Pfenning, *A Proof-Carrying File
System with Revocable and Use-Once Certificates*, STM 2011; revised proceedings
LNCS 7170, 40–55, 2012, DOI 10.1007/978-3-642-29963-6_5.
[Author manuscript](https://people.mpi-sws.org/~dg/papers/stm11-lpcfs.pdf).
Read §§2–4, especially proof verification and file access. The system separates
proof checking from runtime capability checks and tracks certificate
dependencies through revocation and consumption. Revocation is enforced by
the surrounding architecture, while time and linear resource use also appear
in its logic. This is a close interface precedent, not a numerical completeness
theorem or a security guarantee for this repository. No implementation was run.

## 8. Contribution statement and dispositions

**Current defensible statement.** The project supplies a finite operational
calculus for task-relative quantitative judgments, with directed units, joint
source cases, explicit assumptions and versioned proof reception. It gives
local soundness and target-unit completeness arguments, exact fixed-family
revision constructions, and scoped interfaces to Boolean and earlier project
reasoning. Its arithmetic, geometry and dependency mechanisms have substantial
established antecedents. Local reconstruction and a working Python checker
are useful evidence, but establish neither research priority nor independent
formal verification.

**Candidate project advance.** Use those ingredients to answer a concrete
question about what checked evidence must be retained for useful loss-based
decisions after specified revisions, including a bounded self-assessment case.
Show where joint evidence matters and compare precision, storage and total
work with strong existing combinations. This is a plausible modest contribution
direction, not a verified open problem. The neural track asks an additional
empirical question and currently has a design, not a positive learned-structure
result. Component originality is not an acceptance quota.

| Item | Audit disposition | Effect on future work |
|---|---|---|
| Signed lattice/scalar identities and finite normalization | Established ingredients; A15 sharpens the closest proof-theory comparison | Reuse them and keep native compilation obligations explicit |
| U1 target-reduct characterization | Locally derived adaptation with a deliberate evidence-access boundary | Preserve exact scope; review usefulness of the policy in the case studies |
| U11/U13 and U18 | Native adaptations of parametric duality, support maintenance and error bounds | Compare construction/reuse cost; do not claim new general geometry |
| F09 Boolean, affine and phase-one boundaries | Exact project interface results using established structures | Carry witnesses into the reference tests; avoid more equivalent toy variants |
| A10 strictness caution | No imported algorithm; no repository semantic repair required | Any future import must check the final strict/weak inequality |
| Claimed practical or neural advantage | Unestablished | Requires the separate frozen empirical work |

**Simpler alternative.** A direct LP/CPWA semantic solver, with ordinary support
tracking where needed, is a serious baseline. If an application does not need
portable native traces, restricted evidence access or safe versioned reception,
it may be the simpler sufficient solution. The audited literature does not
force replacement of the current kernel, because those interfaces are part of
its stated purpose. It does remove any presumption that a new arithmetic
formalism is needed. Gate B and the later cases must assess the remaining
interface benefit; this audit does not pass the gate or settle that comparison.

No load-bearing external theorem was found to have been misapplied in a way
requiring a change to the selected semantics or existing local proofs. This is
a targeted source audit, not a fresh independent reconstruction of every proof.
The contribution language is narrowed and the import caution is recorded.
[The calibration note](02a_research_calibration.md) gives prospective hours,
staged stopping points, floor assessment and v2/v3 implications.

## 9. Search and inspection limits

A targeted soft-constraint lead was also checked: Stefano Bistarelli and Fabio
Gadducci, *Enhancing constraints manipulation in semiring-based formalisms*,
ECAI 2006, pp. 63–67 ([author manuscript](https://bista.sites.dmi.unipg.it/papers/papers-download/BistarelliGadducci.pdf);
publication details checked against the author's bibliography). Read §3's
Definitions 2–5 and §4.3, Definition 6 and Proposition 10. Residuation supplies
a weak division operation; paired local-consistency updates preserve the
combined solution under the stated absorptive/invertibility assumptions.
This is a useful cost-redistribution antecedent, but not a theorem that removes
an arbitrary versioned source from a retained native proof. The signed finite
carrier also cannot silently inherit the required complete semiring structure.
The existing F03 semiring import boundary remains in force. This rejected
direct import narrows the comparison without claiming that constraint
retraction as a whole is new.

The search followed the current claims under several adjacent descriptions:
ordered-group and Riesz-space proof theory; quantitative algebra; CPWA lattice
representation; certified polyhedral minimization; parametric LP and explicit
MPC approximation; proof minimization, conflict reuse, ATMS and provenance;
local abstraction repair; causal abstraction, subspace patching and calibrated
surrogate losses. The linked calibration also checks preference revision,
revision-sufficient memory and successor features under reward changes.
The register records the statements actually used, not a
claim to have independently verified every theorem in each paper.

Access failures were retained as limits: the original NIST Hoffman endpoint
failed, so an original-paper scan on a mirror was inspected; a Penn provenance
endpoint was replaced with an author PDF; earlier abstraction-repair endpoints
failed before an institutional manuscript succeeded. Some author links for
abstract non-interference failed; the accessible abstract remains a lead, not
theorem evidence here. A search hit labelled as a 2005 follow-up resolved to
*Transforming Semantics by Abstract Interpretation*, a different paper, and
was not used as evidence about non-interference. A later A10 author-PDF retrieval
failed after its text had already been inspected. No unavailable text is
treated as checked merely because a search result describes it.

Priority remains uncertain, especially for the combined revision workflow and
the future learned-cost experiment. No systematic citation-graph review,
implementation replication, or exhaustive survey was performed. A result
absent from this search is not thereby new. Before a publication-level claim,
repeat the closest-baseline search around the actual demonstrated result,
including its application terminology and more recent work.
