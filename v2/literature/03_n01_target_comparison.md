# N01: closest comparisons for decision-preserving retention

Contributor: **Codex (GPT-6)**. Sources inspected October 2, 2026,
America/Los_Angeles. Target specification is in [the contribution plan](../contribution_plan.md).
This is a focused source check, not a comprehensive survey or a priority claim.
F10's audit is reused without assigning it new literature-time credit.

## N1. Shared certificates are already selected for coverage

Marc Fischer, Christian Sprecher, Dimitar I. Dimitrov, Gagandeep Singh and
Martin Vechev, *Shared Certificates for Neural Network Verification*, CAV 2022;
[inspected extended version, arXiv v4, November 23, 2023](https://arxiv.org/pdf/2109.00542v4).
Read §§3.2–4.1, Problems 2–3, Algorithm 1, Theorems 1–2 and equation (2).
The template-generation objective explicitly maximizes covered specifications
subject to a template-count limit and verified postconditions. Matching permits
reuse; unmatched cases fall back to verification. Soundness needs sound
templates and propagation; precision relative to the base verifier has its own
compositional condition. Its cost account includes template creation, matching
and fallback. **Impact:** neither small query-covering certificate portfolios
nor retention-versus-recomputation accounting is a new general contribution.
Our ordinary baseline must support both coverage-oriented retention and fallback.
Its neural abstractions are not automatically native rational proof objects.

## N2. Reusing a search tree does not mean trusting its old answer

Shubham Ugare, Debangshu Banerjee, Sasa Misailovic and Gagandeep Singh,
*Incremental Verification of Neural Networks*, PLDI 2023, article 185.
[Author copy](https://ggndpsngh.github.io/files/ivan.pdf),
[extended manuscript](https://arxiv.org/pdf/2304.01874).
Read §§3–4, §6.2 and the stated last-layer perturbation contract in §4.4;
consulted the extended appendix's relaxation construction. IVAN reuses/prunes
branching trees, rechecks the resulting subproblems and changes branching
priorities. Its specific quantitative perturbation claim fixes the analyzer,
property, architecture and permitted last-layer change. **Impact:** compare
selective fresh search as well as fixed replay. Do not import a bound for
arbitrary source withdrawal or treat a network-update speedup as a forecast
for this tiny rational workload. No IVAN implementation or general theorem
about its code is imported here.

## N3. Changing the input polyhedron is an established verification problem

Tianhao Wei and Changliu Liu, *Online Verification of Deep Neural Networks
under Domain Shift or Network Updates*;
[inspected arXiv v2, February 3, 2023](https://arxiv.org/pdf/2106.12732v2).
Read §§2.3, 3.2–3.3, Algorithm 2, equations (8)–(12), and §4's coverage
comparisons. The domain-shift formulation allows changing linear input
constraints, with fixed network/output requirement. It combines branch
management, enlarged verified sets, tolerance checks and recomputation.
**Impact:** relaxation is not a gap simply because monotone conflict reuse
alone cannot handle it. The source's distance/margin hypotheses and strict
output inequalities must be checked before transfer; our selected queries use
weak inequalities. A compiled CPWA loss comparison is directly relevant to
this class of problem. Speed, coverage and prior verification cost remain
distinct metrics. No published numeric speedup is adopted as our expectation.

## N4. An invalidated proof can be replaced without storing every proof

Boris Motik, Yavor Nenov, Robert Piro and Ian Horrocks, *Incremental Update
of Datalog Materialisation: The Backward/Forward Algorithm*, AAAI 2015.
[Publisher PDF](https://ojs.aaai.org/index.php/AAAI/article/view/9409/9268).
Rechecked §4, Theorem 1 and §5's work/runtime comparison. The algorithm
maintains materialisation after deletions and searches for surviving derivations;
the theorem states termination and bounded repetition of rule instances in its
Datalog setting. The evaluation compares rematerialisation as well as deletion
algorithms and exposes dependence on alternative-proof search order.
**Impact:** an invalid cached dependency set does not imply loss of the
decision. Include check-cache/search-replacement/fresh-solve as an ordinary
baseline. Its finite relational theorem does not prove termination or optimality
of arbitrary native budget search. The Oxford mirror opened initially but later
line reads failed; the publisher copy supplied the checked detail.

## N5. Approximate parametric optimization has a mature cost tradeoff

Colin N. Jones and Manfred Morari, *Polytopic Approximation of Explicit
Model Predictive Controllers*, IEEE TAC 55(11), 2010.
[Author manuscript](https://infoscience.epfl.ch/server/api/core/bitstreams/1cf0c9fe-7adf-4e30-af9b-56ce997d56a1/content).
Rechecked introduction, §V, Lemma 19 and Theorem 20. The method constructs
controlled approximations without first solving the complete explicit problem.
Its feasible-control and stability conclusions depend on the control problem's
convexity and Lyapunov conditions. **Impact:** allow a lazy approximation or
early-sufficient proof baseline, not only expensive full enumeration. A bound
on signed comparative loss is a different contract; do not import a stability
guarantee or a generic convex-epigraph method for a nonconvex outer combination.
This repeats a relevant F10 guard at the now-specific target, not a new source.

## N6. Revision sufficiency alone is not a safe contribution claim

Aevyra, *The Ledger of Will: Evidence, Revaluation, and the Preservation
of Revisable Agency*, research paper v4.0, September 25, 2026.
[Primary text](https://aevyra.github.io/ledger-of-will/).
Rechecked §§4–6 and §9. The finite factorization/revision-closure contracts
and budgeted retention proposal are close to the project's motivation.
Independent peer review and a completed behavioral study were not established.
**Impact:** retain this as a close proposal, while grounding the technical
baseline principally in optimization and verification literature. Neither a
quotient definition nor a generic decision-loss argument establishes the
project's distinctiveness. F10's cautious assessment remains appropriate.

## N7. The scientific primitives are classical

[NIST DLMF §3.5(i)–(ii)](https://dlmf.nist.gov/3.5) gives the trapezoidal
and Simpson rules, including equations 3.5.6–3.5.8 and their smoothness/error
conditions. It identifies Simpson's combination of two trapezoidal rules.
Our R=(4*T_2-T_1)/3 is that classical construction. The polynomial identities
in the derivation notebook are reconstructed directly; this work proposes no
new integration rule or general error bound for physical functions.
The later check also read §3.5(v), especially 3.5.19–3.5.21: n-point
Gaussian quadrature is exact through degree 2n-1. The independently reconstructed
moment calculations in derivation D19 show why admitting Gaussian actions
undercuts the seed's unrestricted application claim. This does not change
the frozen four-action interface fixture.

## N8. Accuracy/cost-based quadrature selection is not a new application idea

Naren Ramakrishnan, John R. Rice and Elias N. Houstis, *GAUSS: An Online
Algorithm Selection System for Numerical Quadrature*, Advances in Engineering
Software 33 (2002), 27–36.
[Author-hosted paper](https://people.cs.vt.edu/naren/papers/GAUSSAdvEng.pdf).
Read the ten rendered pages, especially §§2–3 and §§4.3–4.5; the PDF's extracted
text is corrupt. Its objective combines an accuracy requirement with few
function evaluations. It learns relational recommendation rules from recorded
performance, incorporates new observations and reports empirical selection
quality. Feature acquisition and repeated-run specialization enter its cost
discussion. **Impact:** neither quadrature selection, cost-sensitive comparison,
nor revisable explanations supply a fresh application claim here. Our supplied
coefficient-polytope guarantees differ from empirical recommendation, but that
is a contract distinction to investigate, not proof of novelty. Reimplementing
GAUSS is unnecessary for the first exact feasibility slice; comparing with a
cheap exact formula is essential. No GAUSS selection accuracy is a forecast
for this project, and its broad historical criticism of other learners is not
adopted as a current universal result.

## N9. A checked arithmetic interface is itself established

Alexis Fouilhé, David Monniaux and Michaël Périn, *Efficient Generation of
Correctness Certificates for the Abstract Domain of Polyhedra*, SAS 2013.
[Author manuscript dated April 5, 2013](https://www-verimag.imag.fr/~monniaux/biblio/Fouilhe_et_al_SAS_2013.pdf).
Read §§2–5, including the checker contract in §3.1, and §6's evaluation method.
An untrusted computation supplies nonnegative linear-combination witnesses to
a small Coq-certified checker. Bookkeeping during computation can avoid a
separate witness search. The checked inclusion guarantee is distinguished from
optimal precision, and the evaluation accounts for arithmetic representation
and compares replayed operations with established libraries. **Impact:** native
reception cannot be the remaining novelty claim merely because it independently
checks exact arithmetic, uses source identifiers or separates search from
checking. Strong baselines may generate certificates during computation and
reuse symbolic transformations. Our Python checks do not inherit this paper's
mechanized Coq guarantee. Its program-analysis workload and measured overhead
cannot be transferred to our tiny loss family. The 2014 frontend paper was
located through the authors, but the HAL full-text route was blocked; no theorem
from that unread paper is imported.

## N10. Alternatives need structured provenance, not just a union of supports

Todd J. Green, Grigoris Karvounarakis and Val Tannen, *Provenance Semirings*,
PODS 2007. [Author paper](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf).
Read §§3–5, in particular Proposition 3.5, Theorem 4.3 and Definition 5.1.
Symbolic annotations preserve how inputs combine, and evaluation through a
semiring homomorphism recovers the corresponding positive-query semantics.
The discussion explicitly separates alternative derivations that a plain
contributing-input set would conflate. Recursive Datalog needs additional
infinite-sum/continuity hypotheses. **Impact:** allow an ordinary baseline to
retain a structured circuit of alternatives and instantiate it after withdrawal;
do not force it to store every complete proof separately. This supports a
finite acyclic comparison, not a blanket import for negative-cost cycles,
arbitrary native inference or an unbounded proof search.

## N11. Exponentially many flat alternatives can be a representation artifact

Dan Olteanu and Jakub Závodný, *On Factorisation of Provenance Polynomials*,
TaPP 2011. [Author paper](https://www.cs.ox.ac.uk/dan.olteanu/papers/oz-tap11.pdf).
Read §§2–5. Distributive factorization can encode Cartesian combinations in
space proportional to the input alternatives instead of their product; the
paper also distinguishes storage size from enumeration and downstream-query
costs. **Impact:** count actual retained representations and certificate
generation work, not just the number of flat proof roots. This is especially
relevant to claims based on many alternative supports.

Their *Factorised Representations of Query Results: Size Bounds and Readability*,
ICDT 2012, [author paper](https://www.cs.ox.ac.uk/dan.olteanu/papers/oz-icdt12.pdf),
was checked at §§8–10, Theorems 3–7 and the definitions they use. Its size and
readability bounds have specified query/representation classes. They do not
establish a lower bound for every compressed native proof DAG. No claim about
all compression formats, or about a currently open complexity problem, is
imported from this historical source.

## N12. Decisions with incomplete values and reused witnesses are established

Craig Boutilier, Relu Patrascu, Pascal Poupart and Dale Schuurmans,
*Constraint-based optimization and utility elicitation using the minimax
decision criterion*, Artificial Intelligence 170 (2006), 686–713.
[Author copy](https://cs.uwaterloo.ca/~ppoupart/publications/elicConstraints/sdarticle.pdf).
Read §3.1 Definitions 1–3, §4.2's witness generation and computational
shortcuts, §4.4's coupled utility constraints, and §5's threshold stopping
contract. Pairwise worst-case regret, minimax choice, partial-value elicitation,
early sufficient decisions and seeding later computation with earlier
generated constraints are explicit. The reuse discussion concerns successive
elicitation problems; it does not license keeping obsolete coefficients after
arbitrary withdrawal. **Impact:** our fallback comparison, on setting
utility to negative loss, is a pairwise regret bound against F. Choosing the
first certified action is not minimax regret optimization. Generic decisions
without complete value information, coupled utility polytopes and incremental
witness reuse cannot be novelty claims. The paper's structured discrete
configuration domain differs from the declared quadrature family. Its utility
normalization and linearization assumptions must be checked before importing
an algorithm for signed losses. No source performance numbers are forecasts
for this project.

## N13. Necessary preferences already quantify over compatible value models

Salvatore Greco, Vincent Mousseau and Roman Słowiński, *Ordinal regression
revisited: multiple criteria ranking using a set of additive value functions*,
European Journal of Operational Research 191 (2008), 415–435.
[Author-hosted paper](https://www.lamsade.dauphine.fr/mcda/biblio/PDF/GMS-EJOR2008.pdf).
Read §§4.2–4.3, especially the universal/existential definitions and equations
(7)–(8), §4.4.2's removal of incompatible comparisons, and §5.1's nested
confidence levels. Necessary preference is checked across compatible additive
value functions using a minimum value difference; possible preference uses
a maximum. Weak comparisons require care at equality and are not simple
logical complements. **Impact:** robust value comparison and revisable
preference constraints already have direct decision-analysis precedents.
Our source constraints describe integration-error coefficients, not elicited
additive preferences; a faithful model translation is still needed. Neither
that change of interpretation nor explicit premise identifiers alone supplies
a project contribution. The paper does not settle our matched cost of retained
certificates, but its existence narrows what that cost study could claim.

## N14. Exact preservation of a chosen query language is established

Francesco Ranzato and Francesco Tapparo, *Generalized Strong Preservation by
Abstract Interpretation*, [author preprint v3, March 14, 2006](https://arxiv.org/pdf/cs/0401016v3).
Read §2.3, Definition 5.2, Lemma 5.3, Theorem 5.8 and §6.2's qualifications.
Strong preservation requires agreement of concrete and abstract truth for a
specified language. The most abstract preserving domain is characterized by
closure of formula denotations under intersections. The complete-shell
characterization has language-closure hypotheses; it is not an unrestricted
claim that all preservation is operator completeness. **Impact:** query-relative
information sufficiency and refinement to recover lost answers are established
ideas. For our finite queries, a threshold-answer abstraction is a natural
comparison, not a new general abstraction principle. These results concern
semantic precision in specified abstract domains, rather than the byte count,
construction cost or validity checking of retained proof objects. Do not turn
a semantic minimality theorem into a lower bound on arbitrary programs or
proof DAGs. The conference precursor could not be fetched; this comparison
uses the available full preprint, not an unread theorem from that precursor.

## N15. Rigorous adaptive quadrature already includes tolerance and cache choices

Fredrik Johansson, *Numerical integration in arbitrary-precision ball
arithmetic*, ICMS 2018.
[Primary preprint](https://arxiv.org/pdf/1802.07942v1).
Read §§2–3, including the callback contract, acceptance loop, tolerance
qualification, node caching and benchmark exclusions. The implementation
combines subdivision with variable-degree Gaussian quadrature using certified
complex-domain magnitude bounds. The integrand callback must enclose values
and, when requested, establish analyticity on the supplied region. Requested
tolerances are goals; the returned ball gives the achieved enclosure even
when evaluation limits intervene. Gaussian nodes are cached, and the reported
benchmarks omit their initial precomputation. **Impact:** rigorous adaptive
accuracy/resource decisions and numerical caching are established. A richer
scientific case must account for premise generation, numerical enclosures,
warm versus cold costs and achievable tolerance, rather than comparing only
to unchecked quadrature. The paper's historical timings and implementation
defaults are not current forecasts. Its complex analytic function interface
differs from our finite coefficient constraints; neither can be assumed to
provide the other's inputs for free. No implementation was installed or
benchmarked here. Petras's original article was located at its publisher
abstract only; its complexity theorems were not independently imported.

## Search and scope record

Search families covered parametric LP/explicit MPC approximation, incremental
neural verification, shared certificate coverage, threshold preservation,
and quadrature with correlated uncertainty. The last family mainly retrieved
distributional/Bayesian quadrature optimization and unrelated uses of the word
quadrature. Those search hits do not establish a missing literature niche.
[Nguyen et al., AISTATS 2020](https://proceedings.mlr.press/v108/nguyen20a.html)
was inspected only at the primary abstract: its distributionally robust
Bayesian optimization problem differs from our fixed coefficient polytope.
No theorem from it is imported. The more specific algorithm-selection search
then found GAUSS, checked above. Rice's 1974 Purdue report *The Algorithm
Selection Problem II* was checked only at its
[repository record](https://docs.lib.purdue.edu/cstech/69/); the download failed.
A recent accuracy/cost quadrature preprint was an inaccessible search lead,
not inspected evidence. Specialist rigorous quadrature and robust algorithm
selection still have incomplete coverage; this is not an absence claim.

## Consequence for ambition and the comparison

The generic retention/coverage mechanism, generic quadrature selection,
generic robust value comparison and generic independently checked polyhedral
certificates are displaced as novelty candidates. These established tools
remain appropriate to reuse. N01's own derivations further displace uniform
full-vector affine compression in the seed. Its optional nine-versus-twelve
policy distinction is a scoped lead, not a general innovation claim.
The narrower application question remains **NOT YET SUPPORTED**, not refuted:
can a precisely declared evidence-retention contract yield an informative
cost/decision tradeoff across scientific loss and later self-assessment cases?
Answering this needs an actual matched study and possibly a broader problem
than the two-coordinate feasibility family. An extra notation layer, duplicate
kernel checks or an example defeating only marginal intervals cannot support
the novelty claim. The next implementation should be small enough to discover
that the ordinary baseline already suffices without wasting a large budget.

No full-paper audit, replication of source experiments, comprehensive absence
claim or external priority claim is made by these targeted inspections.
