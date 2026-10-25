# s18 primary-source comparison log

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT. Inspection scopes are
limited to those stated; absence of an exact search hit is not novelty evidence.

## Capped N16 comparison

**Bousselmi, Hendrickx and Glineur, [Interpolation Conditions for Linear
Operators and Applications to Performance Estimation Problems](https://arxiv.org/html/2302.08781v3).**
Read the two-sided bounded interpolation and self-adjoint interpolation
statements/proof portions (HTML Theorems6 and8), plus the numerical
conjecture discussion in section4.1.2. The exact SDP specialization is
already in s17; no new exactness claim is earned by repeating it. The
framework does not automatically supply a closed scalar solution for every
interpolation problem. Our additional comparison instead eliminates a
hidden second-moment block by standard minimax.

**Bousselmi, Deng, Lu, Glineur and Hendrickx,
[arXiv2511.16360](https://arxiv.org/pdf/2511.16360).** Read the introductory
operator-class setup and Theorem2.4's statement. Convex Gram-interpolation
classes constrain spectral sets, rather than arbitrary spectral multiplicities.
This limits what a convex information representation can preserve. The
full polar-decomposition proof was inspected in s17, not newly re-audited
here. It does not separately supply N16's analytic endpoints.

**Sion (1958), [On general minimax theorems](https://msp.org/pjm/1958/8-1/pjm-v8-n1-p14-p.pdf).**
Read the definitions and section3 through Theorem3.4 and its following
one-compact-set corollary (printed as3.3). Convexity/concavity and the stated
semicontinuity conditions permit the exchanges used in
[n16_reduction.md](n16_reduction.md). The compact set is the matrix moment
interval, or the scalar q interval; the other variable need not be compact.
This theorem supplies minimax exchange, not compatibility with a finite
ridge source or endpoint attainment. Those are checked separately.

**El Ghaoui and Lebret (1997), [Robust Solutions to Least-Squares Problems
with Uncertain Data](https://people.eecs.berkeley.edu/~elghaoui/Pubs/rob-ls.pdf).**
Revisited section3.1's rank-one worst-residual proof, Theorem3.2's
normal-equation derivation, Remark3.2 with fixed right-hand side and
section3.3's one-dimensional reduction. These directly account for the
norm-sum and scalar-parameter machinery. Their action-before-perturbation
problem must still be related to N16's reoptimized value, which the selected
rank-one edit and normal equation accomplish. The source's generic robust
least-squares method is credited; our retained-information specialization
is a candidate synthesis, not a new robust least-squares algorithm.

**Fritzsche, Kirstein and Maedler,
[On the structure of Hausdorff moment sequences of complex matrices](https://arxiv.org/pdf/1701.04246).**
Read the introduction, Notation4.1, Definition4.2, Theorem4.3 and the
finite-measure existence statements5.2–5.4 at statement scope. With
interval[0,1] and moments(I,C,Q), their conditions reduce to
[[I,C],[C,Q]]>=0 and C-Q>=0, hence C^2<=Q<=C. Thus this closed
moment interval is classical. The general referenced moment theorem and
all later canonical-measure proofs were not reconstructed here. Strict
finite ridge-source realization and the selected scalar equality moment
are supplied by explicit elementary constructions in our comparison.

**Zhen, Kuhn and Wiesemann, [A Unified Theory of Robust and
Distributionally Robust Optimization via the Primal-Worst-Equals-Dual-Best
Principle](https://arxiv.org/pdf/2105.00760).** Read the introductory setup,
Slater definitions and the section3 weak-duality/reformulation diagram at
statement scope. This is relevant generic duality background, but Sion
already suffices for the particular compact moment problem. No new N16
formula is attributed to this paper, and its74-page proof/companion is
not claimed as audited.

**[Perturbation Duality for Robust and Distributionally Robust Optimization:
Short and General Proofs](https://arxiv.org/html/2603.20503v1).** Inspected the
Theorem1 hypotheses and nearby interchange/attainment discussion only.
Its transport/moment formulation is not needed for the present finite
reduction. This is a screened lead, not a theorem imported into N16.

Access limits: Beck–Ben-Tal's author PDF timed out on two follow-up opens;
s17's recorded inspection is inherited, not newly claimed. Two International
Press URLs for Zagorodnyuk's truncated matrix Hausdorff paper returned403.
Dette–Studden's Dortmund PDF loaded with garbled text; its proof was not
read. The readable Fritzsche–Kirstein–Maedler source replaced that lead.
Searches also returned unrelated compressed resolvents, sketching, and
low-rank matrix completion. Those keyword matches provide no novelty verdict.

## Broad discovery sources

**Diwan, Hellerstein, Megow and Schloeter,
[Optimal Verification of a Minimum-Weight Basis in an Uncertainty Matroid](https://arxiv.org/html/2512.17116v1).**
Read abstract and contents only. The paper claims polynomial minimum-cost
verification with known full weights for general uncertainty areas, including
closed intervals and finite sets. It is a strong lead for a certificate-query
candidate, not a fully inspected theorem or an imported approximation guarantee.

**Akshay, Bansal and Mahla,
[Certifying Almost-Sure Reachability in Unknown MDPs](https://arxiv.org/html/2610.18119v1).**
Read section2 definitions and impossibility statements, section3 Lemma1 and
proof, section4 definitions, Theorems4/5 proof sketches and Theorem6 statement.
Their reset/step sampling contract and size-only budget are stronger demands
than our possibly abstaining generative-row, margin-dependent drift check.
A known lower bound on positive transition probabilities supports their
model-learning route; Theorem6 transfers a bounded ranking supermartingale
through a controlled model error. No contradiction to their lower bound or
complete proof audit is claimed here.

**Bowers and Waggoner,
[Matching with Nested and Bundled Pandora Boxes](https://arxiv.org/pdf/2406.08711).**
Read introduction, section2.1, reservation and exposure definitions in2.2,
Lemma1 and its following optimal-search argument; also inspected Definition4's
backward nested-index recursion and the nearby section4 optimality argument.
Reservation/capped values account for paid independent inspection, including
more general rewards than our Bernoulli specialization. The expected maximum
capped value makes the outer retention objective submodular immediately.
The full matching analysis and every nested proof were not reconstructed.
Weitzman's Harvard PDF timed out; MIT's1978 working-paper metadata loaded
but two download attempts failed. We do not claim to have read those PDFs.

**Berger, Ezra, Feldman and Fusco,
[Pandora's Problem with Combinatorial Cost](https://arxiv.org/pdf/2303.01078).**
Read introduction, Examples1/2, Theorems1–3 statements and the reservation
discussion. Shared setup costs can make individually unprofitable boxes jointly
useful. The stated submodular-cost fixed-order result does not give an efficient
general value-oracle algorithm; their hardness result is directly relevant.
This defeats importing independent-box indices into shared proof-cost banks.
No full proof audit or new shared-cost algorithm is claimed.

**Chattopadhyay, Dahiya and Mahajan,
[Query Complexity of Search Problems](https://drops.dagstuhl.de/storage/00lipics/lipics-vol272-mfcs2023/LIPIcs.MFCS.2023.34/LIPIcs.MFCS.2023.34.pdf).**
Read introduction, section2 definitions and propositions, Theorem3.2's short
proof and Proposition4.1's sketch. Finding any valid output, finding a canonical
output and deciding a Boolean function have different query requirements.
The PromiseFIND1 discussion is relevant to our existential-receipt extraction;
its imported separation theorems were not independently proved here. Our fee
formula is an elementary weighted promise-search specialization, not a new
general randomized-versus-deterministic separation. The paper's randomized
depth/error convention differs from our zero-error expected-fee examples.

**Ahmed and Guan,
[The Inverse Optimal Value Problem](https://optimization-online.org/wp-content/uploads/2002/07/510.pdf).**
Read introduction, section2 assumptions and value/duality propositions, and
the section3 reduction statement. Observing only an optimum value is an
established inverse-optimization interface. Their unknown object is the cost
vector of a known linear program, rather than our unknown feasible subset;
their complexity result is not automatically a lower bound for our finite
contact-set formula. The full hardness reduction and later algorithms were
not audited. This comparison rules out claiming value-only inference itself
as new.

**Beckert, Bormer and Klebanov,
[Reusing Proofs when Program Verification Systems are Modified](https://formal.kastel.kit.edu/~klebanov/pubs/reuse2.pdf).**
Read the five-page position paper. Its KeY workflow reuses rule applications
under changed programs and discusses recertification after changes to the
verification system, including a corrected semantic rule. Similarity suggests
steps; the current prover still checks applicability. This is direct precedent
for using a fallible reuse heuristic without treating old proof authority as
permanent. It is not a complete semantics of genuine counterpossibles or a
quantified cost guarantee for our proposed retention controller.

Other leads: the Google research page for *Randomized query complexity can beat
certificate complexity* was inspected only for title/authors; no theorem was
imported. Freivalds-related arXiv search abstracts and general inverse-feasible-
region search hits were leads only. A repository about revision-impact
certificates was not used as a vetted scientific comparison.

## Value-equivalent models and policy reuse

**Barreto et al., [Successor Features for Transfer in Reinforcement Learning](https://me.net.nz/files/publications/barreto2017sf.pdf).**
Read introduction/background, Theorem1 and its supplement proof on pages12–13.
Uniform action-value error gives generalized policy improvement with the
usual discounted error term; Bellman monotonicity and contraction prove it.
Read Lemma1's reward-mismatch statement and beginning of its proof only.
Our minimum-potential switching construction is an undiscounted cost-side
specialization with its own termination premise, not a new GPI principle.
Experiments and the remaining supplement were not audited.

**Nemecek and Parr, [Policy Caches with Successor Features](https://proceedings.mlr.press/v139/nemecek21a/nemecek21a.pdf).**
Read introduction/background, Theorem1 statement, section5 Algorithms1/2 and
the conical-task LP bound, and section7 comparison. This directly addresses
using a retained policy cache and performance-gap bounds to decide whether to
reuse or learn another policy, for changed rewards with shared dynamics.
The supplement proof was not located/read in the inspected nine-page main
PDF; experiment text returned by search was not an empirical audit.

**Thakoor et al., [Generalised Policy Improvement with Geometric Policy Composition](https://proceedings.mlr.press/v162/thakoor22a/thakoor22a.pdf).**
Read introduction, section2.1, Definition4.1's suffix closure, Theorem4.2 and
its B.4 proof, and Proposition5.1's proof. Bellman improvement over the
appropriate closed switching-policy class is established prior work. Closure
is a real hypothesis. The mentioned nonclosed counterexample, full sampling
argument and training experiments were not audited.

**Grimm et al., [The Value Equivalence Principle for Model-Based Reinforcement Learning](https://proceedings.neurips.cc/paper/2020/file/3bb585ea00014b0e3ebe4c6dd165a358-Paper.pdf).**
Read introduction, definitions1/2, section3 properties including Proposition1's
span statement and nearby text, Proposition2's dimension statement, Remark2
and section7. Generic decision-sufficient model equivalence is already
credited in s11. Our [affine-anchor note](affine_anchor.md) flags the role of
unknown rewards in linear-span reasoning; it is not a claim to correct this
paper because shared-reward conventions and the supplement were not resolved.

**Grimm et al., [Proper Value Equivalence](https://arxiv.org/pdf/2106.10316).**
Read introduction, sections2/3, Definition1, Propositions1/2, and Proposition4
and Corollary1 planning statements. Preserving the required policy values can
suffice for optimal planning while multiple models remain. A finite bank is
not automatically coverage of all policies. Appendix proofs were not audited.
Metadata identifies NeurIPS2021 andv2.

**Nikulski et al., [Robust Successor Features](https://arxiv.org/html/2609.31016v1).**
Read introduction, section2.3, section3's linear transition/reward setup and
Theorem1 statement. Its discounted linear-MDP comparison includes reward,
transition and approximation terms. This is a relevant stronger control for
policy reuse under changed dynamics, not an imported proof for our
undiscounted drift contract. Appendix proofs and empirical results were not
audited; the stated parameter normalization was not independently validated.

Arumugam and Van Roy's
[value-equivalent sampling paper](https://proceedings.neurips.cc/paper_files/paper/2022/hash/3b18d368150474ac6fc9bb665d3eb3da-Abstract-Conference.html)
was an abstract/search lead only. No rate-distortion theorem is imported.

## Calibration across batches

**Ling and Strohmer, [Self-Calibration and Bilinear Inverse Problems via Linear Least Squares](https://math.ucdavis.edu/~strohmer/papers/2016/Blind-Cali.pdf).**
Read introduction, section2.1's three models, section2.2 equations2.5/2.6 and
the inverse-gain linearization/normalization discussion through its block
matrix. Inverting unknown gains to obtain linear equations is direct prior
work for our lifted batch constraints. The stability results and full
forty-two-page proof development were not audited. Our additional scope is
the interval/offset probability interface and specified decision/query costs.

**Hendrickx, Olshevsky and Saligrama,
[Minimax Rank-1 Factorization](https://perso.uclouvain.be/julien.hendrickx/availablepublications/HOS_19_rank1.pdf).**
Read introduction/motivation, sections2/3, section4.1's weighted log least
squares derivation and Theorem1/Corollary1 statements. Positive connected
observation graphs and ratio information are established mechanisms. Small
entries and lost connectivity matter to noisy recovery. No full minimax
proof audit. The separate MIT rank-one-completion PDF failed with502;
its search snippet is only a lead, as is the2026 LAA completion article.

## Guaranteed feasible cores from uncertain witnesses

**Davari, Edalat and Lieutier,
[The convex hull of finitely generable subsets and its predicate transformer](https://www.doc.ic.ac.uk/~ae/papers/lics19.pdf).**
Read introduction/related work, Definition1 and the rectangular-corner
construction, Algorithm1, section4's pre-inner support definition, Lemmas2–4
and Theorem1 with their arguments. Their max–min support expression is the
direct prior for(K2); the earlier rectangular construction already reduces
the required corner hulls drastically. The paper distinguishes interiors and
closed sets; our finite compact proof states its boundary convention directly.
Later domain-theoretic continuity, infinite-generation and predicate-transformer
results were not audited. Our translated-shape erosion formula is a direct
specialization, not a new general hull method.

**Lindner et al., [Learning Safety Constraints from Demonstrations with Unknown Rewards](https://proceedings.mlr.press/v238/lindner24a/lindner24a.pdf).**
Read abstract, AppendixB's guaranteed-hull construction and associated source
references. This already uses uncertain witness regions to obtain guaranteed
feasible decisions in a learning setting. The nearby AppendixA text returned
by the tool was not a reconstruction of its safety/convergence proofs. No
experiment audit. This is a stronger conceptual comparator than full model
identification.

**Lee and Abbas,
[A Geometric Approach to Resilient Distributed Consensus Accounting for State Imprecision and Adversarial Agents](https://arxiv.org/pdf/2403.09009v1).**
Read definitions4.1/4.2, Lemmas4.1/4.3 and Theorem4.5 with their proofs,
sectionIV-B's construction and nearby application/setup. The alternate
[six-page author-hosted version](https://nebula.wsimg.com/131afb0b104df29f1b943888a77c50fa?AccessKeyId=DC23973FEA94075ABCF3&alloworigin=1&disposition=0)
states the same subset identity as Theorem4.4 and refers to the preprint for
proof. ArXiv history showed onlyv1. Our rational square example contradicts
that identity and Lemma4.3; this is not an audit of all consensus claims.

**[LazySets Pontryagin-difference documentation](https://juliareach.github.io/LazySets.jl/v1.44/lib/binary_functions/#Minkowski-difference).**
Read the polyhedral support-offset formula and its stated attribution to
Kolmanovsky–Gilbert Theorem2.3. This confirms a standard implemented ordinary
operation for(T2). The original1997/1998 paper was not independently read.

Sember's thesis was a primary search lead; its library-hosted PDF failed to
fetch. Edalat–Lieutier–Kashefi's2001 author PDF opened with garbled extraction
and its requested screenshot failed. Do not claim their original proof was
read: the2019 paper's account supplies the comparison used here.
# Additional bounded screens during s18

- **Geometric acquisition screen:**
  [Bruce/Hoffmann/Krizanc/Raman2005](https://link.springer.com/article/10.1007/s00224-004-1180-4)
  publisher abstract and author publication record inspected; full proof access
  was unavailable. It reports a three-update comparison for full boundary-point
  identification. This cannot be imported for the smaller fixed-point decision
  in query_scope.md. The EATCS survey endpoint returned403; its search excerpt
  was only a lead to the original. The strong ordinary sorting comparison
  [Halldorsson/de Lima2021](https://doi.org/10.1016/j.tcs.2021.03.021)
  was inspected in the search-returned abstract and witness-set/Theorems11-12
  text. No new geometric acquisition guarantee is asserted from these sources.
- [Agarwal et al., Convex Hulls under Uncertainty](https://users.cs.duke.edu/~pankaj/publications/papers/prob-ch.pdf)
  abstract only: its supplied probability distributions make it a different
  contract from deterministic guaranteed-hull information. No membership
  probability algorithm or stochastic independence assumption was imported.

- **Approximate inverse constraint learning:**
  [Chou/Ozay/Berenson2020, cost uncertainty](https://arxiv.org/pdf/2001.09336),
  abstract, Problem3, cost-uncertainty discussion and Remark1 inspected.
  They already infer safe/unsafe sets under unknown cost parameters; the
  suboptimal KKT-residual variant has an explicitly qualified conservativeness
  guarantee. The s18 relative-demo claim instead assumes a bound on global
  value regret and an unrestricted convex feasible set. This is a narrower
  information contract, not general superiority over their method.
  [Their parametric-constraint paper](https://proceedings.mlr.press/v100/chou20a/chou20a.pdf)
  was read at the problem setup and sections4.2-4.3: consistency across all
  admissible constraints and possible-action feasibility tests are already
  ordinary methods. Its supplied-cost interface differs from ours.
- **Relative suboptimality normalization:** the search-returned section4.2.2
  of [Chan/Mahmood/Zhu's inverse-optimization survey](https://pubsonline.informs.org/doi/10.1287/opre.2022.0382)
  identifies established scaling reductions and earlier joint objective/
  constraint estimation. The direct page fetch timed out. Troutt et al.2005
  and2008 are leads only; their original proofs were not accessed. Do not
  claim positive-scale normalization as a new idea.
- **Geometric comparison:**
  [Brandenberg/Koenig, arXiv1310.4368v4](https://arxiv.org/pdf/1310.4368),
  Definition3.1, Proposition3.4, Lemma3.5 and its proof inspected. Classical
  Minkowski asymmetry has a sharp dimension bound and a polyhedral LP
  formulation. This is a close comparison obligation for the proposed1/d
  threshold, not yet a proved equivalence or an independent new bound.
- Lindner et al.'s section4.2 and Assumption3 use a Boltzmann demonstration
  model for convergence. This does not directly supply the deterministic
  relative-regret contract in relative_demo.md. Their main guarantees and
  our possible specialization should remain separate.
- [CF-KKT2026](https://arxiv.org/html/2610.09350v1) was screened at the abstract,
  introduction and control formulation only. Its learned-dynamics/KKT approach
  is a current adjacent source, not a reconstructed comparator theorem.

- Revisited Lee/Abbas's exact definitions, Lemmas4.1/4.3 and Theorem4.5;
  the four-square example uses their stated independent point-selection
  semantics. Revisited Davari/Edalat/Lieutier Algorithm1: its retained
  common-direction hull family is a strong ordinary control for the proposed
  scalar convex-value envelope, not merely for the final intersection.
- Extended inspection of Lindner et al.2024 to Appendix C, Assumption4,
  Theorem8 and the start of Theorem9's proof. Their guaranteed-unsafe cone
  uses optimal demonstrations, unknown linear rewards and a nondegeneracy
  condition. This motivates a separately derived relative-error variant;
  the paper's complete maximality and approximate-demonstration results have
  not yet been audited for that variant.

- **van Ackooij and Sagastizabal, Constrained Bundle Methods for Upper
  Inexact Oracles with Application to Joint Chance Constrained Energy
  Problems**, [author manuscript](https://optimization-online.org/wp-content/uploads/2012/12/3711.pdf).
  Inspected abstract, the Slater-point interpolation steps in section6.1,
  section6.3's starting-point comparison, and the nearby warning about the
  cost of obtaining the Slater point. This supports treating feasible
  interpolation as an ordinary control. It does not establish the exact
  uncertain-witness common-core formula in interior_repair.md. The full
  convergence proofs and numerical experiments were not reconstructed.
- The previously inspected [Davari/Edalat/Lieutier2019 manuscript](https://www.doc.ic.ac.uk/~ae/papers/lics19.pdf)
  was revisited only for its pre-inner-support formula and occurrences of
  ball regions. Its general support machinery is already a direct control;
  no additional specialized interior-ball theorem was located in this pass.
- A cheap search for convex-value envelopes also surfaced
  [Norton/Takeda/Mafusalov2017](https://arxiv.org/abs/1711.07511), optimistic
  robust optimization; [Sheikhi/de Berg/Mehrabi2017](https://pure.tue.nl/ws/portalfiles/portal/52366453/sheisepa2017.pdf),
  separability of imprecise points; and
  [Loffler/van Kreveld](https://members.loria.fr/Sylvain.Lazard/BellairsWorkshops/Bellairs-2009/background/hulls-loffler-vanKreveld.pdf),
  extremal uncertain convex hulls. Only search abstracts/snippets were
  inspected, not their proofs. These remain comparison leads, not imported
  theorems or evidence that a matching result does not exist.

# Coupled search screen (s18)

- Lawler, Lenstra, Rinnooy Kan and Shmoys, *Minmax criteria*,
  [author-hosted chapter](https://people.orie.cornell.edu/shmoys/or6335/ch3.pdf),
  section3.1, Theorem3.1 and its exchange proof inspected. Jackson's1955
  earliest-due-date rule minimizes maximum lateness. Setting due dates to
  minus returned-action losses gives exactly the queried-action order in
  total_search.md. The ordering algorithm is established machinery. The
  least-cost-last generalization is also stated/proved there; no novelty is
  claimed for rearranging these scalar jobs.
- Vayanos, Georghiou and Yu, *Robust Optimization with Decision-Dependent
  Information Discovery*, [arXiv2004.08490v3](https://arxiv.org/pdf/2004.08490),
  abstract, introduction contributions and section7.4 formulation inspected.
  It explicitly couples sequential paid discovery with worst-case eventual
  reward, including a robust Pandora example. Its general formulation and
  K-adaptability methods are strong ordinary controls. The inspected example
  has correlated uncertain prizes and allows keeping opened boxes; s18 has
  binary feasibility, known terminal losses, upward-closed contact promises
  and logically inferred unqueried outputs. Those restrictions support our
  short exact reduction but do not make joint query/decision optimization a
  new principle. The full general equivalence proof and computational study
  were not reconstructed in this cheap screen.

# Boolean closure and incomplete witnesses

- Kautz, Kearns and Selman, *Reasoning With Characteristic Models*, AAAI1993,
  [author-hosted paper](https://www.cs.virginia.edu/~rmw7my/papers/kc-models.pdf).
  Abstract and section2 definitions inspected. Complete models, intersection
  closure and Horn representation are established ingredients; the paper
  explicitly studies representation-dependent reasoning benefits. Our contact
  interface does not justify claiming that conventional logics ignore models.
- Khardon, *Translating between Horn Representations and their Characteristic
  Models*, JAIR1995,[primary paper](https://arxiv.org/pdf/cs/9512105).
  Abstract, section2.1/Theorem1 and the membership-query simulation on printed
  page361 inspected. The latter tests closure membership by intersecting all
  supplied generators above the target. That is the exact fixed-generator
  antecedent of meet_receipts.md; our extra universal-selector step is a
  specialization of this ordinary operation. No general translation algorithm
  or historical open-complexity claim is imported as a current result.
- Eiter, Ibaraki and Makino, *Computing Intersections of Horn Theories for
  Reasoning with Models*, AAAI1998,
  [proceedings paper](https://cdn.aaai.org/AAAI/1998/AAAI98-041.pdf).
  Abstract, preliminaries and returned algorithm/theorem text inspected.
  It already studies least/common models of intersections represented by
  characteristic-model lists, plus enumeration and optimization-related limits.
  Several formulas were lost by text extraction; the exact running-time
  proof was not reconstructed. A list of every selector-generated theory
  would be an exponential expansion of our contact input, so a direct
  polynomial reduction is not established by this screen alone.
- Brandts and Zivny, *Beyond PCSP(1-in-3,NAE)*,
  [2022 author preprint](https://www.cs.ox.ac.uk/standa.zivny/publications/bz22ic-preprint.pdf),
  introduction and Theorem4 inspected. The authors explicitly state positive
  one-in-three hardness and the Boolean polymorphism form of Schaefer's
  classification. This supports the source problem and the distinction from
  ordinary affine CSP feasibility. Our incomplete-witness problem has a
  different quantifier/input contract. Original Schaefer1978 PDF attempts at
  ACM and a Northeastern-hosted copy returned403; only its search excerpt
  was visible, so its original proof is not claimed read.

# Abstract convexity control for fallible reports

- Nowak and Rybicki, *Byzantine Approximate Agreement on Graphs*, DISC2019,
  [proceedings](https://drops.dagstuhl.de/storage/00lipics/lipics-vol146-disc2019/LIPIcs.DISC.2019.29/LIPIcs.DISC.2019.29.pdf).
  Sections2.1,2.4,3.1.1 and displayed resilience theorems inspected. Their
  safe area is explicitly an intersection of hulls after deleting possible
  faulty inputs. Semilattice height/Helly numbers and resilience thresholds
  are already part of this abstract-convexity framework. Our centralized
  receipt core has no distributed agreement or communication duty; its
  threshold must not be compared directly with their extra asynchronous
  requirements. The generic safe-area idea and meet-height principle are
  established prior, leaving only the particular incomplete-input algorithms
  and decision interface as possible increments.
- Abbasizanjani and Kullmann, *The classification of minimally unsatisfiable
  2-CNFs -- a fundamental study*,[arXiv2003.03639v3](https://arxiv.org/pdf/2003.03639),
  April2026 version. Abstract and section6's unit-clause facts, including
  Lemma6.4 and Corollary6.5, inspected; the full74-page classification was
  not audited. The at-most-two-unit fact supports the short standard clause
  bound used in fallible_contacts.md. Earlier search hits giving a4d bound
  were loose leads, not evidence against the reconstructed2d argument.

# Modular computation screen

- Dumas, Gautier and Roch, *Generic design of Chinese remaindering schemes*,
  [2010 paper](https://arxiv.org/pdf/1005.0830), abstract, sections3 and4,
  especially4.1–4.3 and Algorithms8–9 inspected. A controller already separates
  modular computation, reconstruction and stopping; deterministic bounds,
  randomized stabilization and full computation costs are explicit. Our
  threshold-specific stopping predicate could fit this ordinary interface.
  It is not a new generic early-termination architecture. The Verimag copy
  timed out; the arXiv version was accessible.
- Kaltofen and Villard, *Computing the sign or the value of the determinant
  of an integer matrix, a complexity survey*,
  [author copy, published2004](https://kaltofen.math.ncsu.edu/bibliography/02/KaVi02.pdf).
  Introduction, section2 Remark1 and returned portions of sections3–4 inspected
  as a literature map. Random-prime nonzero tests and certified arithmetic
  filters are already explicit. This survey is not used as a new primary
  proof of an improved determinant bound, nor are its historical asymptotic
  records described as current. Follow its original references if a concrete
  determinant application becomes worth pursuing.

# Additional incomplete-information screen

Chen/Dalmau, *Looking Algebraically at Tractable Quantified Boolean Formulas*
(SAT2004), abstract and sections1--2:
https://www.satisfiability.org/SAT04/programme/91.pdf . The primary text gives
an algebraic proof of quantified2-SAT tractability and discusses semilattice
models for quantified Horn formulas. These are strong antecedents for using
closure operations to compress universal duties. They begin with a supplied
constraint formula; our contact interface instead leaves the closed source
unknown. That input distinction is an obligation to compare, not evidence
that the resulting algorithm is novel.

Bubeck/Kleine Buening, *Models and Quantifier Elimination for Quantified Horn
Formulas* (2008), abstract and introduction:
https://www.ub-net.de/cms/fileadmin/upb/doc/bubeck-qhorn-dam-2008.pdf . The
paper gives quadratic-size elimination and model construction using restricted
universal assignments. Only the opening statements were inspected here; no
claim that our unknown-source contact problem improves those results.

Xue/Li/Janardan, *On the Separability of Stochastic Geometric Objects, with
Applications* (SoCG2016), primary abstract:
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2016.62 . This
addresses probabilities and margins under stochastic point models. It is a
related uncertain-geometry lead, not a proof of the deterministic closure
receipt claims. No complete literature-absence claim follows from this screen.

# Uniform counterfactual proof-bank screen

Diochnos, Sloan and Turan, *On Multiple-Instance Learning of Halfspaces*,
[2011 author preprint](https://www.diochnos.com/research/publications/dst-MIL-Halfspaces.pdf),
abstract, sections2--3 and Theorems1--2 inspected. The paper provides the
bag-VC upper bound and a matching-order lower bound through cyclic polytopes.
Our halfspace-feasibility predicate is exactly the OR bag predicate; taking
the convex hull changes no halfspace-intersection answer. This directly
subsumes the proposed complexity obstruction and supplies the stronger
comparison for bounded witness banks. No full algorithmic-learning audit.

Sabato/Tishby, *Multi-Instance Learning with Any Hypothesis Class* (JMLR2012),
[primary paper](https://www.jmlr.org/papers/volume13/sabato12a/sabato12a.pdf),
abstract/introduction and the section3 result as exposed by the source search.
The general theory studies bag classes with logarithmic dependence on maximal
bag size; it does not require independent instances within each bag for that
setting. This is established machinery for the proposed proof-bank adapter,
not a new statistical result of this recurrence. Detailed learning algorithms
and constants were not reconstructed.

# Affine report-stream screen

Pavel Patak, *Tverberg type theorems for matroids*,
[arXiv1702.08170v2 primary PDF](https://arxiv.org/pdf/1702.08170), header2021,
arXiv version marker2019. Introduction, Lemmas1--2, Proposition5 and the
start of section3 inspected. Its affine-hull and matroid statements already
give the same threshold and stronger nested-closure conclusion; the colored
extension has a polynomial algorithm. This is a direct antecedent to our
full-point affine robust-action construction. The source distinguishes
affine-hull intersection from the conventional name "affine Tverberg",
which refers to convex hulls under an affine simplex map. We do not claim
an improvement to that stronger convex theorem or distributed consensus.

# Conditional optimum-receipt screen

Ahmed/Guan, *The Inverse Optimal Value Problem*,
[primary preprint](https://optimization-online.org/wp-content/uploads/2002/07/510.pdf),
abstract, sections1--2 and start of section3 inspected. It already treats
values rather than optimal solutions as inverse data, including hardness
and tractable special cases when cost coefficients vary over a compact convex
set. Our source has independently uncertain hull generators and several
retained directional minima; its possible increment is the face/subset
algorithm for that structure, not inverse inference from values itself.
The closest broader interval-parameter results still need a full comparison.

Cerny/Hladik, *Inverse optimization: towards the optimal parameter set of
inverse LP with interval coefficients* (2016),
[author abstract](https://kam.mff.cuni.cz/~hladik/publ/b2hd-CerHla2016a.html).
It studies parameter sets inducing a prescribed optimum and reports hardness
and parametric methods. The linked rdcu PDF was inaccessible. This is an
explicit remaining comparison lead, not a paper whose proofs were inspected.
The Chan/Mahmood/Zhu survey section3.5.2 was used only to locate these primary
works, not as evidence of absence of the present specialization.

Agarwal/Har-Peled/Suri/Yildiz/Zhang, *Convex Hulls under Uncertainty*,
[primary arXiv PDF](https://arxiv.org/pdf/1406.6599), abstract, input models
and introduction inspected (PDF header2018, arXivv1 marker2014). It treats
probabilistic sites, hull membership and compact representations, with
potentially exponential output distributions. Our deterministic conditional
value problem has a different declared input, but the broad uncertain-hull
representation theme is established. The Duke PDF fetch failed403; the
arXiv copy was available. No full probabilistic algorithm comparison made.
# Further inverse-value and ordinal-feedback comparison

Codex (GPT-6), s18 DEVELOPMENT; primary-source screening, not confirmation.

- Li and Cui, [Variational Theory and Algorithms for a Class of
  Asymptotically Approachable Nonconvex Problems](https://arxiv.org/pdf/2307.00780),
  November21,2024 version: inspected Example1.1, formulation(1)--(2), and
  Section5 formulations/termination discussion. Multiple scalar optimum
  observations with shared unknown parameters are explicitly established.
  Their general numerical stationary-point framework is not an exact
  small-receipt global endpoint algorithm. The s18 simplex specialization
  and conditional-value distinction must be stated as adaptations, not a
  new inverse-observation principle.
- Dostert and Jochemko, [Learning polytopes with fixed facet directions](https://arxiv.org/pdf/2201.03419),
  v4 February2023: inspected introduction and its precise statement of
  Theorem3.1/Corollary3.5. Support-value reconstruction and max-affine
  regression are established. Their fixed-normal-fan quadratic formulation
  is a mandatory comparison to supplied generator regions and unknown
  attainer assignments; the parameterizations differ. No general claim of
  new reconstruction from optimum values is warranted.
- The Cerny--Hladik2016 full text remains inaccessible through both the
  author's rdcu link and the Springer PDF endpoint. Preserve that gap.
- Oki and Sakaue, [Finite and Corruption-Robust Regret Bounds in Online
  Inverse Linear Optimization under M-Convex Action Sets](https://arxiv.org/pdf/2602.01682),
  v2 May11,2026: inspected Sections2--5 and AppendixD. The exact
  distinct-component assumption in the corrupted theorem motivates
  [tied_feedback.md](tied_feedback.md); AppendixD explains why an honest
  cycle can instead express equal utility. This is a narrower adaptation
  question, not a claim that preference learning or corruption robustness
  is new. The paper's regret normalizes the per-round utility range.
- Cohen, Schapire and Singer, [Learning to Order Things](https://arxiv.org/pdf/1105.5464),
  JAIR1999: inspected abstract, introduction and start of the preference
  formulation; also the readable NIPS1997 version. Learning pairwise
  preferences and maximizing ordering agreement are already explicit.
  Thus the ordering step in tied_feedback.md is conventional; a contribution
  would require its specific tie-insensitive finite mistake guarantee.
- Yasutake et al., [Online Rank Aggregation](https://proceedings.mlr.press/v25/yasutake12/yasutake12.pdf),
  2012: inspected introduction and online protocol. It reveals a full
  permutation and evaluates Kendall loss, rather than one best available
  choice with genuine ties and a hard count of bad responses.
- Helmbold and Warmuth, [Learning Permutations with Exponential Weights](https://jmlr.org/papers/volume10/helmbold09a/helmbold09a.pdf),
  2009: inspected abstract/introduction and the loss-matrix contract.
  Their linear assignment loss supports a doubly stochastic summary.
  Pairwise ordering disagreement is a different loss; do not import the
  compact representation without a reduction.

These are bounded screens. They do not establish absence of an equivalent
result in noisy sorting, partial-label learning or contextual recommendation.

## Late primary comparisons and inspected scope

- [Cai et al., September2026](https://arxiv.org/pdf/2609.13440): model,
  reduction and Section3.2/Theorem3.6 proof inspected. General O(d) regret
  and known-budget O(d+C) robustness materially strengthen the comparator.
  Budget-agnostic tuning remains an explicit question. No independent audit
  of the complete paper was performed.
- [Sakaue, September2026](https://arxiv.org/pdf/2609.26978): abstract and
  opening theorem scope inspected, including expected O(sqrt(d)) regret and
  the polynomial-time question. Full proof not inspected.
- [Kitaoka, October2026 v2](https://arxiv.org/pdf/2609.09809): Assumption3.1
  and opening guarantees inspected; uniqueness and a uniform witness margin
  restrict the finite-mistake contract.
- [Bubboloni and Gori](https://arxiv.org/pdf/1606.03898): Propositions1–2,
  Theorems3/55 and the flow/Schulze comparison inspected. Strict transitivity
  and these ranking kernels are established. [Gori2024](https://doi.org/10.1016/j.mathsocsci.2024.05.003),
  readable Sections4–5, explicitly interprets disjoint paths as independent
  arguments; this is not a novel interpretation supplied by s18.
- [Shivaswamy and Joachims2015](https://www.cs.cornell.edu/~tj/publications/shivaswamy_joachims_15a.pdf):
  Sections3.1/4 and the movie-feedback description inspected. Improving
  feedback and the finite-context caveat are already established.
- [Ailon2012](https://jmlr.org/papers/volume13/ailon12a/ailon12a.pdf): abstract
  and introduction inspected. Adaptive queries to a fixed, possibly
  inconsistent pair-label matrix optimize ordering disagreement; this is
  not the same loss/interface as round-corrupted truthful choices.
- [Zhang et al., label cut](https://pages.cs.wisc.edu/~jyc/papers/label-cut.pdf):
  abstract, introduction and the set-cover connection inspected. The grouped
  report hardness construction adapts this conventional labeled-cut problem.
- [Björklund, Husfeldt and Koivisto2009](https://www.cs.helsinki.fi/u/mkhkoivi/publications/sicomp-2009.pdf):
  primary search-extracted opening/equation1 inspected; a direct fetch later
  timed out. The full paper was not read. The s18 sieve is a reconstructed
  inclusion-exclusion adaptation, not a claimed new covering algorithm.
- [Mostafaee, Hladik and Cerny2015](https://nb.vse.cz/~cernym/invp.pdf):
  introduction, model and Theorem1/2 scope through roughly page4 inspected.
  This accessible prescribed-optimal-value interval-LP report is distinct
  from the still-inaccessible Cerny/Hladik2016 article above.
- [Ren, Mohajerin Esfahani and Georghiou2025](https://arxiv.org/pdf/2505.15025):
  Section3's affine-image hypothesis class, simplex unknown vertices and
  Theorem3.3 reformulation inspected. It uses optimizer observations and
  bilinear/block-coordinate machinery; the underlying source parameterization
  is a strong conventional antecedent.
- [Corrente et al.2013](https://link.springer.com/article/10.1007/s10994-013-5365-4):
  abstract, Section4.1 necessary/possible preferences and Section6
  inconsistency treatment inspected. Robust ordinal inference is established.

The [published ICML Oki–Sakaue entry](https://proceedings.mlr.press/v306/oki26a.html)
was located, but its published PDF has not yet been compared. The version
actually inspected is the May arXivv2 specified above. These access/scope
limits remain part of the contribution uncertainty, not evidence of absence.
