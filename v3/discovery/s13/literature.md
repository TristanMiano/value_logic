# s13 primary-source comparisons

Codex (GPT-6), DEVELOPMENT. Accessed October 20, 2026. Leads are distinguished
from read technical sections; no search snippet establishes an imported theorem.

## Initial boundary checks

- Johnstone and Cox, [Conformal Uncertainty Sets for Robust Optimization](https://proceedings.mlr.press/v152/johnstone21a/johnstone21a.pdf),
  PMLR152,2021, Introduction and start of Section2.1. Calibrating an uncertainty
  set for a downstream robust optimizer is established; no coverage theorem
  was imported beyond its stated exchangeability setting.
- Zhou and Zhu, [Calibrating Decision Robustness via Inverse Conformal Risk
  Control](https://arxiv.org/html/2510.07750), v3 June10,2026, Sections2–3.2,
  including Assumptions3.1–3.2, Theorem3.4 and Proposition3.5 statements.
  Their displayed expectation guarantee is distinct from a high-probability
  guarantee for a realized calibration set. Their miscoverage/regret frontier
  and selection-aware discussion are close antecedents; no theorem or
  reported numerical advantage is imported into calibrated_slack.md.
- Dronavajjala, [When Is Conformal Coverage Free? Switching Thresholds for
  Predict-then-Optimize](https://proceedings.mlr.press/v329/dronavajjala26a.html),
  PMLR329,2026, PDF pp2–10, especially Definition1 and Theorems2–3. The cost-gap
  versus perturbation comparison and exact directional switch point are
  established sensitivity tools. The paper studies cost uncertainty and
  decision neutrality; our candidate concerns failure of action constraints
  and a common warrant across repricing. No online quantile-fluctuation result
  is imported. Web PDF retrieval failed; the linked official raw GitHub PDF
  was read with urllib and pypdf instead, without saving it into the repository.
- NIST Dataplot, [Tolerance Limits](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/tolelimi.htm),
  Description and one-sided/percentile note. Confidence and population content
  are distinct; nonparametric tolerance limits are established. The page cites
  Wilks1941, whose Project Euclid page returned an iframe and whose original
  proof was not read. calibrated_slack.md supplies its elementary integer-score
  binomial argument directly rather than claiming a new statistics result.

- Kolmogorov and Zabih, [What Energy Functions Can Be Minimized via Graph
  Cuts?](https://www.robots.ox.ac.uk/~cvrg/trinity2005/kolmogorov_zabih_pami04.pdf),
  PAMI26(2),2004, Section3 graph representation, Section4 Theorems4.1–4.2
  and Section4.1 construction. The binary pairwise regularity condition and
  unary-cost offsets are established. signed_actions.md adapts coordinate
  reflection to the uncertain-threshold contract; it does not introduce a
  new cut algorithm. Failure of one renaming is not an instance hardness proof.

- Giles and Hajek, [An Information-Theoretic and Game-Theoretic Study of
  Timing Channels](https://hajek.ece.illinois.edu/Papers/GilesHajek02.pdf),
  IEEE Transactions on Information Theory48(9),2002, Introduction and SectionII
  problem formulation (pp2455–2457). The encoder selects packet-arrival
  waveforms and a constrained jammer delays them. Unlike our acquisition
  problem, this does not charge a private encoder for learning which message
  it has before choosing its waveform. Timing-channel capacity is therefore
  an antecedent/relaxation, not an imported attainable query rate. Equations
  in the extracted PDF were partially lost; no detailed capacity theorem was
  reconstructed. Searches for depth-only/private-query timing protocols did
  not identify an exact match; this is not evidence that none exists. An
  unrelated arXiv1902.00964 page was retrieved by mistake and is not a source.

- Stern and Juba, [Efficient, Safe, and Probably Approximately Complete
  Learning of Action Models](https://www.ijcai.org/proceedings/2017/0615.pdf),
  IJCAI2017, Sections2,3 and start of4 (Definitions1–4 and Theorem1 statement).
  Fully observed successful STRIPS trajectories support conservative action
  models and safe planning without complete model identification. Their exact
  action-effect premise and trajectory sampling contract differ from our
  fixed-task threshold warrant. The general motivation is established; no PAC
  bound was reconstructed or imported here.
- Srivastava, Russell and Pinto, [Metaphysics of Planning Domain
  Descriptions](https://aima.cs.berkeley.edu/~russell/papers/aaai16-abstraction.pdf),
  AAAI2016, Introduction and Section3.1 Definitions3–6/Theorems1–2. Dropping
  state predicates can destroy composition/Markov properties. This supports
  retaining an explicit boundary between a static action warrant and reusable
  sequential dynamics; no new sequential abstraction theorem is imported.
- Karimi, Schoelkopf and Valera, [Algorithmic Recourse: from Counterfactual
  Explanations to Interventions](https://arxiv.org/html/2002.06278), v4,
  Introduction and Sections3.1–3.2. The stated structural equations, intervention
  semantics and stationarity premise matter: changing observed features alone
  does not identify intervention effects. Our local threshold-response law is
  an explicit strong premise, not a causal conclusion from observational fit.

- Păsăreanu et al., [Assumption Generation for the Verification of
  Learning-Enabled Autonomous Systems](https://arxiv.org/html/2305.18372),
  Section II Definition1; Section III AlgorithmIII.1, Theorem2, Proposition3;
  Section III local-specification construction and Theorem4. The paper makes
  task-relative and observation-interface-relative weakest assumptions explicit,
  including estimation-only monitors when actual states are unavailable.
  **Comparison:** generic task adequacy, relaxed model accuracy and interface
  restriction are established. Its transition-system construction is not yet
  an imported theorem for our static projection service.
- Brawand et al., [Active Multiple-Prediction-Powered Inference,
  v1](https://arxiv.org/html/2605.08429), Introduction, Related Work and start of
  Section3.1 inspected. Predictor-subset costs, selective gold labels and
  cost-aware routing are explicit. **Comparison:** these features cannot alone
  support novelty for a generic paid-model estimator. Detailed optimality
  claims were not reconstructed and are not imported. An attempted OpenReview
  retrieval of Active Statistical Inference returned a browser challenge;
  that PDF was not read.
- Ji, Mascagni and Li, [Gaussian Variant of Freivalds' Algorithm](https://www.nist.gov/publications/gaussian-variant-freivalds-algorithm-efficient-and-reliable-matrix-product-verification),
  author/publication abstract inspected. Cheap verification of a fallible
  matrix product is established. No floating-point guarantee is imported.

Search-only leads, not read technical sources: Run2Survive (PMLR129),
online algorithm selection with censored feedback (arXiv2109.06234),
Künnemann's matrix-product correction (ESA2018), and goal-oriented residual
error estimates. The numerical-residual mechanism was already rejected as
new in s12/search.md, with its own literature record.

## Projection and invoice comparisons

- Fargier and Marquis, [Extending the Knowledge Compilation Map: Krom, Horn,
  Affine and Beyond](https://www.cril.univ-artois.fr/~marquis/fargier-marquis-aaai08.pdf),
  Introduction and stated fragment definitions inspected. The filename says
  aaai08 while the retrieved revised PDF carries2011 copyright; retain that
  version ambiguity rather than inventing a publication date. Krom disjunction
  closures and their operation tradeoffs are explicit prior machinery.
- Marquis, [Existential Closures for Knowledge
  Compilation](https://www.cril.univ-artois.fr/~marquis/marquis-ijcai11.pdf),
  Introduction and appendix discussion of expressiveness, PDFp9 (zero-based8),
  lines around the prime-implicate forgetting proof. Projection keeps precisely
  the prime consequences outside the forgotten variables; binary fragments
  remain binary. **Imported:** this standard projection fact. **Candidate
  adapter:** the common-Q/singleton-scope envelope and two-versus-three-model
  expanded-receipt boundary; no priority claim established by this search.
- Buhrman and de Wolf, [Complexity Measures and Decision Tree Complexity:
  A Survey](https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf), Introduction
  and Section2.1 inspected as a terminology/antecedent lead. The ordinary query
  reveals the queried bit, unlike our invoice interface. No quantum or
  randomized complexity theorem is imported from this survey. Sensitivity and
  edge-adversary methods are established; the proposed7/3 local charging
  inequality needs its own exact interface proof and close-prior assessment.

Exact-phrase timing/invoice searches did not identify the same acquisition
contract. That is an incomplete search result, not evidence of originality.

- Golia, Roy and Meel, [Manthan: A Data-Driven Approach for Boolean Function
  Synthesis](https://pmc.ncbi.nlm.nih.gov/articles/PMC7363189/), Introduction's
  functional-synthesis specification inspected. Producing hidden values that
  extend every admissible visible input is explicitly Skolem synthesis, with
  program-repair applications already named. No claim about a particular
  2-CNF synthesis algorithm or Manthan's performance is imported. This closes
  the generic novelty route for the third search question.
# Additional primary comparisons after the first context recovery

Read Aissi, Bazgan and Vanderpooten, *Complexity of the min-max (regret)
versions of cut problems*, ISAAC2005, abstract and section1:
https://www.lamsade.dauphine.fr/~bazgan/Papers/isaac05cut.pdf . First fetch
timed out; the unchanged retry was readable. Fixed-terminal and unrestricted
cuts have different robust-complexity results; interval min-max regret
fixed-terminal cut is stated hard. The full reduction was not reconstructed,
and the result is not automatically a hardness theorem for our unary-price
closure fragment. Read only the author abstract of Mastin, Jaillet and Chin,
*Randomized Minmax Regret for Combinatorial Optimization Under Uncertainty*,
arXiv1401.7043v2: https://arxiv.org/abs/1401.7043 . Mixed-strategy robust
optimization is an established alternative with different adversary timing;
no uninspected theorem is imported into the controller.

Revisited s05/frontier_sources.md's already-read AOLS/CMOVE comparison.
That record supplies the antecedent for small multiobjective action covers.
It is historical research, not a newly discovered contribution in s13.

Read Rashtchian and Raynaud, *Edge Isoperimetric Inequalities for Powers of
the Hypercube*, arXiv1909.10435v2(2022), introduction, theorem1 and its
following induced-edge corollary, PDFp2: https://arxiv.org/pdf/1909.10435 .
The bound E(W)<=|W|log2|W|/2 is classical and explicitly attributed there to
Harper, Bernstein, Lindsey and Hart. The short induction in vector_error.md
reconstructs that standard inequality; it is not a new isoperimetric result.

Read Suruga, *Zero-error expectation equals amortized query complexity*,
arXiv2608.04152v1(August4,2026), abstract, theorem1 and sections2.1-2.2:
https://arxiv.org/html/2608.04152v1 . Its ordinary decision-tree model already
has a general asymptotic1-epsilon factor for global-error expected randomized
query cost. Do not claim that factor as new. Our restricted private-invoice
interface does not directly inherit its zero-error single-instance constant;
the proposed delta is the channel-specific beta factor and finite edge bound.
The full proof and general-relation claims were not reconstructed here.

Read Ahuja, Hochbaum and Orlin, *A Cut-Based Algorithm for the Nonlinear Dual
of the Minimum Cost Network Flow Problem*, Algorithmica39(2004), abstract
and section1 formulation, pp189-190:
https://hochbaum.ieor.berkeley.edu/html/pub/AHO-cut-based-Algorithmica-2004.pdf .
Nonlinear separable objectives with ordered/difference constraints already
have cut-based methods, including pseudopolynomial constructions for arbitrary
nonlinear unary costs. Our explicit threshold expansion is ordinary machinery;
we do not import the paper's scaling guarantees for our more general profiles.

Read Hell and Rafiey, *Duality for Min-Max Orderings and Dichotomy for Min
Cost Homomorphisms*, arXiv0907.3016v1, abstract and section1, pp1-2:
https://arxiv.org/pdf/0907.3016 . Min/max-preserved ordered relations and
minimum-cost homomorphisms are established tractability subjects. Their
fixed-digraph classification is not applied as a theorem to our multi-sorted
profiles. The explicit reduction here supplies its own narrower argument.

Read Walsh, Hewlett and Morrison, *Blending Autonomous Exploration and
Apprenticeship Learning* (NeurIPS2011), sections1-2 and definitions1-2:
https://proceedings.neurips.cc/paper_files/paper/2011/file/e034fb6b66aacc1d48f445ddfb08da98-Paper.pdf .
The separation between knowing when a prediction is reliable and bounding
mistakes under supplied feedback is directly relevant. A small mistake bound
does not give free feedback, autonomous exploration or exact safe actions.
The earlier workshop PDF returned503. No reinforcement-learning theorem is
imported into the present permission service.

Re-read Brafman and Hoffmann, *Conformant Planning via Heuristic Forward
Search* (ICAPS2004), introduction and Planning Background, pp355-356:
https://cdn.aaai.org/ICAPS/2004/ICAPS04-042.pdf . This was already a prior
comparison in s12. Read Geffner, *Planning Graphs and Knowledge Compilation*
(KR2004), abstract, introduction and the planning-graph section, pp1-2:
https://icaps04.icaps-conference.org/icapspapers/KR04GeffnerH.pdf . The AAAI
mirror failed. Binary implicate compilation and planning from a set of
possible initial worlds are established. The latter paper's precise
prime-implicate correspondence theorem was not reconstructed here.

The s12 comparison also exposed an internal rediscovery: all coordinatewise
Boolean maps and the blind-reset baseline were already present in
s12/permission_compiler.md section7. s13/unary_actions.md now attributes that
first pass correctly. Proposed new work is the second maximal-warrant pass
and a priced overwrite minimum-cut fragment, not the availability of resets.

Codex (GPT-6). Read Akinsanya and Brennan, *Timing Channels in Adaptive Neural
Networks* (NDSS2024), abstract and introduction, PDF pp1-2:
https://www.ndss-symposium.org/wp-content/uploads/2024-125-paper.pdf .
Input-dependent inference effort can disclose input properties through timing;
this is an established phenomenon, not an invention of our invoice branch.
Their empirical inference setting does not supply our private-reset query
contract or its exact parity fee bound. No empirical numbers are imported.

Read Askarov, Zhang and Myers, *Predictive Black-Box Mitigation of Timing
Channels* (CCS2010), introduction, section2.1 and section3.5 theorem1:
https://www.cs.cornell.edu/andru/papers/ccs10.pdf .
The black-box source can encode information in event times; mitigation trades
delay for restricted leakage. Their separation bound uses joint storage/time
information. This supports explicitly accounting for all outputs, but is not
our adjacency-based acquisition lower bound. No theorem beyond that elementary
information separation is imported. Searches for query trees revealing only
stopping depth did not locate an exact contract; this is incomplete searching,
not evidence of novelty.

Read Gottwald and Braun, *Bounded rational decision-making from elementary
computations that reduce uncertainty*, arXiv1904.03964v1, abstract and
introduction (PDF pp1-2): https://arxiv.org/pdf/1904.03964 .
Its resource order is based on probability transfers and relative majorization,
with information costs as a special case. This is an established conceptual
antecedent for uncertainty-reduction costs. It does not, from the sections
read, price a concrete interpreter or give our restricted-observation bound.
The PMC mirror returned a browser challenge; a guessed arXiv HTML v3 returned
404. The original PDF was readable. Later mathematical sections are unread.

Read Nappo, Cangiotti and Sisti, *Confirming Mathematical Conjectures by
Analogy*, published online2023, Erkenntnis89(2024), abstract and introduction:
https://link.springer.com/article/10.1007/s10670-023-00683-6 .
They distinguish incremental evidential confirmation from analogy informing
prior credence. This is motivation for separating a proof-transport receipt
from an unverified analogy. No quantitative calibration guarantee is imported.
The university PDF returned403; publisher HTML was readable.


## Multivalued coding and proof-guidance checks (October20-21 UTC)

Read Golin and Rote, *A Dynamic Programming Algorithm for Constructing
Optimal Prefix-Free Codes with Unequal Letter Costs* (IEEE TIT1998),
introduction and start of sectionII, pp1770-1771:
https://www.cse.ust.hk/~golin/pubs/Huffman2.pdf . Unequal symbol costs and
weighted code trees are established. Later algorithm proofs were not read.
Read Golin and Young, *Prefix Codes: Equiprobable Words, Unequal Letter Costs*,
introduction and section2 through Lemma2.4 and its exchange argument, PDF
pp1-4: https://arxiv.org/pdf/cs/0205049 . Equiprobable messages with unequal
letter costs already have specialized algorithms. Our elementary O(q^2)
recurrence is not a preparation improvement. The invoice reduction in
multivalued.md inherits s12/cap_two.md and adds a product-target consequence.
No claim is made about the current best coding complexity.

Before the third context interruption, read Poesia, Broman, Haber and Goodman,
*Learning Formal Mathematics From Intrinsic Motivation* (NeurIPS2024),
introduction and related work, PDF pp1-4:
https://papers.neurips.cc/paper_files/paper/2024/file/4b8001fc75f0532827472ea5a16af9ca-Paper-Conference.pdf .
Conjecture generation, proof search and hindsight subgoal reuse are existing
research. The algorithm section and empirical results were not reconstructed;
no performance number or theorem is imported. Generic proof guidance alone
is not a new candidate. Search outputs interrupted at23:54-23:58 were not
credited as read; the coding sources above were reopened after recovery.

Read additional portions of Zhou and Zhu, arXiv2510.07750v3: section3.3
(selection and sample splitting) and AppendixF (known solver-gap correction).
Its main risk-estimator guarantee is in expectation; Proposition3.5 supplies
a separate pointwise high-probability offset. Neither is automatically a
simultaneous post-selection confidence band. Conservative treatment of
incomplete solves is established. No guarantee from this paper is imported
into the own finite integer tolerance proof.

Read Lin, Delage and Chan, *Conformal Inverse Optimization*, sections3.1 and
4.1 (problem, assumptions1-3, metrics and calibration construction):
https://arxiv.org/html/2402.01489v2 . It learns uncertain objective parameters
from observed decisions, requiring consistency with some parameter in the
set. This is different from our common event that every retained action is
safe, but it is a close decision-relevant calibration antecedent. Performance
theorems and empirical sections were not reconstructed here.

Read Abel et al., *Value Preserving State-Action Abstractions* (AISTATS2020),
introduction/background and section3 through Definition5, PDF pp1-5:
https://proceedings.mlr.press/v108/abel20a/abel20a.pdf . State aggregation and
options can preserve high-value behavior without retaining all predictions.
Its restricted options couple initiation/termination to an abstraction; an
arbitrary option needs additional execution state. The main quantitative
bounds and proofs were not imported. This is a strong antecedent against
calling generic task-sufficient dynamics a new mechanism.

Read Diwan, Hellerstein, Megow and Schloeter, *Optimal Verification of a
Minimum-Weight Basis in an Uncertainty Matroid* (STACS2026), introduction and
results discussion pp1-5 and section5.2 pp17-19, including Corollary32 and
the statement of Theorem33:
https://drops.dagstuhl.de/storage/00lipics/lipics-vol364-stacs2026/LIPIcs.STACS.2026.32/LIPIcs.STACS.2026.32.pdf .
Bipartite minimum-cost certificates and using a predicted certificate before
fallback are established. Their smooth basis-prediction guarantee depends on
circuit structure and two specified error terms. Its full-version proof was
not read or imported. The implication-audit adapter requires its own local
repair argument; generic prediction/checking is not a new contribution.

The Deshpande research-project page was used only to locate primary Boolean
function evaluation papers: https://www.cs.umd.edu/~amol/DBGroup/RobustPrDB.html .
Searches also surfaced CASP2607.14545 and general minimum-explanation work;
those search excerpts were not treated as read technical sources or as proof
that the exact implication-audit claim is novel.

Read Behrisch, Hermann, Mengel and Salzer, *Minimal Distance of Propositional
Models* (Theory of Computing Systems63,2019), introduction and section6.1,
Propositions32-33 and the proof of33:
https://link.springer.com/article/10.1007/s00224-018-9896-8 . Nearest arbitrary
assignments and nearest other satisfying assignments are distinct problems.
For bijunctive sources, a forced flip in a satisfying assignment propagates
further necessary flips. This is a close prior for the own unit-observation
least-error step. General classification proofs were not read. The earlier
CSR2016 author PDF returned403; the journal HTML was readable.

## Sequential calibration, numerical edits and binary experiments

Read Hultberg, Zachariah and Ribeiro, *Anytime-Valid Conformal Risk Control*
(2026), introduction, problem/related-work sections2-3 and section4.1 through
Proposition4.5: https://arxiv.org/html/2602.04364v1 . Nested bounded losses,
i.i.d. calibration and a safe endpoint support time-uniform risk control.
This is a direct antecedent for sequential_slack.md; its simple error-spending
adapter claims no statistical novelty or optimal constants. Distribution-
shift formulas and asymptotic proofs were not imported. The OpenReview page
for Xu et al.'s active anytime RCPS triggered browser verification; a guessed
arXiv HTMLv3 returned404, so its search excerpt is only a lead. Mineiro and
Howard2302.14248 was read only at abstract scope; guessed HTMLv3 also404.

Read Dörfler and Bullo, *Kron Reduction of Graphs with Applications to
Electrical Networks*, sectionIII.D, TheoremIII.14 and its proof, PDFp13:
https://motion.me.ucsb.edu/pdf/2011d-db.pdf . Schur-complement responses and
rank-one interior-edge perturbations are established. This blocks a novelty
claim for the basic numerical-edit identity. The own generic-SPD sign-cycle
construction is not silently specialized to all electrical networks.

Read the publisher abstract of Mayo and Antoulas, *A framework for the
solution of the generalized realization problem* (2007):
https://doi.org/10.1016/j.laa.2007.03.008 . Full algorithm not reconstructed.
Also read *A greedy data collection scheme for linear dynamical systems*,
section2, Problem2.1, Definition2.1 and Theorem1, plus the opening problem of
section3: https://www.cambridge.org/core/journals/data-centric-engineering/article/greedy-data-collection-scheme-for-linear-dynamical-systems/A333C8F25EF60FC73CE1A260D2AE85A7 .
The published Loewner realization uses transfer measurements and known
feed-through, with rank-dependent compression. Its adaptive point-selection
algorithm and empirical claims were not imported. These are strong ordinary
controls for generic value-only rational system identification.

Read Sason, *Entropy Bounds for Discrete Random Variables via Maximal
Coupling*, sectionI, Theorems1-2 and proofs, PDFpp1-3:
https://arxiv.org/pdf/1209.5259 . The common probability mass and residual
decomposition are established; no entropy theorem from later sections is
needed for experiment_frontier.md. Read Rauh et al., *Coarse-graining and
the Blackwell Order*, sectionI through Theorem1 and its decision discussion,
PDFpp1-2: https://arxiv.org/pdf/1701.07602 . Output garbling supplies the
ordinary decision comparison. The own prospective consequence is the priced
invoice frontier obtained by composing this comparison with the s13 edge
bound, not a new ordering of statistical experiments.

Read Valiant, *A Theory of the Learnable* (CACM1984), introduction and §5,
TheoremA and proof, printedpp1134-1135 and1138-1139:
https://courses.grainger.illinois.edu/ece544na/fa2014/valiant84.pdf . Bounded-
width CNF learning by deleting unsupported clauses, including partially
specified positive examples, is a direct antecedent. The original positive-
example/concept contract differs from the own population-coverage service;
the own finite-class calculation states its assumptions. No modern optimal
sample-complexity result is imported. The Belohlávek/Vychodil closure paper's
publisher page returned403 and its author publication page timed out; the
search abstract is a formal-concept comparison lead, not a completed read.

Read Zhou, Orfanoudaki and Zhu, *Conformalized Decision Risk Assessment*,
§§4.2.1-4.2.3, Algorithm1, and§5.1 Theorem5.1/Corollary5.2:
https://arxiv.org/html/2505.13243v3 . Its inverse feasible region concerns
one prescribed decision's near-optimality. The e-value result is an
expectation-wise risk bound; the p-value statement has an additional
post-selection TV term. These are not automatically the common high-
confidence action-menu guarantee needed here. Full proofs, consistency and
the optimizer implementation were not reconstructed. Generic task-relevant
conformal validation is already established.
# Additional online and incomplete-verification comparison

Codex (GPT-6), October21. Saha2019,
[dissertation](https://samsaha.com/files/learning-frameworks.pdf): read
§4.1,§5.3.2.2, and selected§3.2 passages through the CD-NPI/ICE reduction
and its illustrative example. Predicate elimination and property-directed
conjunctive learning directly anticipate online_clauses.md's basic rule.
Informative abstraction failures differ from mere timeouts. No experimental
performance or full convergence proof is imported from the thesis.

Zhang/Chaudhuri2016,
[Extended Littlestone dimension](https://proceedings.mlr.press/v49/zhang16a.pdf):
read introduction and§2 setup; their round reveals the label after either
prediction or abstention. Our paid world-fact audits require a separate
feedback/cost model; no abstention bound is imported.

Sridharan/Yoo2024,
[Online Learning with Unknown Constraints](https://arxiv.org/html/2403.04033v1):
read introduction, related work and§3 setup. Their unknown constraint model,
post-action signals and initially safe set differ from our pre-action exact
audit. No regret theorem is transferred. The attempted v2 HTML returned404;
v1 was available. Search results on feedback prices and reliable learning
remain leads only.
# Inspection, repair and correlated evaluation

Codex (GPT-6), October21. Read introduction and problem definition of
Stern/Kalech/Shinitzky2016, [Implementing Troubleshooting with Batch Repair](https://cdn.aaai.org/ojs/10075/10075-13-13603-1-2-20201228.pdf), pp769-771.
Guaranteed repair effects and repair overhead are explicit established
ingredients. Our additive implication-certificate optimization omits their
batch overhead and post-repair system-test channel; no performance transfers.
The2020 journal abstract and Langseth/Jensen2003 abstract/introduction were
also inspected as leads to stronger troubleshooting comparisons.

Zong/Lehtonen/Rintanen2026,
[Cost-Optimal Decision Diagrams](https://arxiv.org/html/2606.24672v1):
read introduction/related work and available§3 setup passages (the later
output was truncated, so no complete§3/proof read is claimed). Their exact
correlated evaluation algorithm is a stronger ordinary direction than a
fixed audit order; it evaluates a formula rather than modifying its input.

Ghuge/Moondra/Singh2026,
[Stochastic Function Certification with Correlations](https://arxiv.org/html/2604.02611v1):
read introduction and§1.1. Its certification task assumes support already
satisfies the target and distinguishes adaptive/nonadaptive benchmarks.
That supports careful comparison scope, not a theorem for our writes or
our off-support safety requirement. Later approximation proofs were not read.
# Scalar matrix-response and weak-intervention comparison

Codex (GPT-6), October21. Brunel/Urschel2024,
[Recovering a Magnitude-Symmetric Matrix from its Principal Minors](https://arxiv.org/html/2404.06302v2): read introduction,§5.1 opening algorithm
steps and§5.3 through Condition2, Theorem3 and the start of Example1. Recovery
up to diagonal sign changes, quadratic query schemes and quantitative
separation conditions are established. Our scalar resolvent oracle needs an
explicit interface reduction. No full noisy-recovery proof was imported.
Loewy1986 abstract and an author-hosted network review were orientation only.

Ma/Garnett/Schneider2013,
[Sigma-optimality](https://www.cs.cmu.edu/~schneide/nips13ma.pdf): read
introduction,§§2-4, Lemmas2,7,9 and the displayed Appendix A.1/A.2 passages;
not the complete submodularity appendix or experimental section. The2012
[preprint](https://arxiv.org/pdf/1209.3694) introduction and§§2-3.1 were also
read. Their nonnegative inverse and variance-reduction results are direct
antecedents. The continuous grounded-shunt omission bound is derived in
weak_ports.md; no empirical result or arbitrary edge-addition guarantee is
transferred from these sources.

# Additional application and generalization screens

Codex (GPT-6), October21. Livshits/Kimelfeld/Roy2018,
[Computing Optimal Repairs for Functional Dependencies](https://pmc.ncbi.nlm.nih.gov/articles/PMC6568326/):
abstract/introduction read. Minimum weighted repairs and their computational
complexity are established. Veltri et al.,
[Interactive Data Repairing: the FALCON Dive](https://ceur-ws.org/Vol-2037/paper_38.pdf):
introduction and displayed budget-repair formulation read; its user validates
update-rule semantics. No later approximation or empirical result is imported.
Application consequences are recorded in application_scope.md.

Searches for multi-target channel simulation and decision-tree influence
returned O'Donnell/Saks/Schramm/Servedio2005 and Jain/Zhang2011. Only abstracts
and introduction snippets were inspected; no influence theorem was imported.
The elementary OR example and direct simulation in multiple_targets.md are
derived separately. Renewed timing-channel searches returned the established
network timing literature and the already read adaptive-neural timing paper;
no exact-match acquisition theorem was found or inferred absent. These
additional search outputs are leads, not completed technical reads.

Esposito/Gastpar/Issa2019,
[A New Approach to Adaptive Data Analysis and Learning via Maximal Leakage](https://arxiv.org/pdf/1903.01777):
read introduction, finite-channel formula, Theorem1, Lemmas2-4, Appendix B
proof and the displayed opening of Appendix C. The selected-event bound,
post-processing and adaptive composition are established. The deployment
adapter in limited_adaptation.md derives its finite sums directly; it is
not a claimed new risk inequality or an import of a training algorithm.

Grabovsky2022,
[Reconstructing Stieltjes Functions from Their Approximate Values](https://arxiv.org/pdf/2101.02775):
read introduction, Theorems2.2-2.4 and the opening of§2.2 through the
admissible-value formulation. Positive spectral representations and sharp
interpolation regions are established. The paper explicitly distinguishes
upper-half-plane measurements from real-axis data; its algorithm is not
imported unchanged for our real edit strengths. The one-point real-axis
envelopes in one_value_bounds.md follow directly from Jensen/secants.
The NSF PDF request returned502 and author PDF web request timed out;
a separate urllib read yielded no recovered output. The arXiv text above
was available. No full reconstruction proof or implementation was read.

Impagliazzo/Williams2010,
[Communication Complexity With Synchronized Clocks](https://people.csail.mit.edu/rrw/cc-clocks-conf.pdf):
introduction, prior-work discussion,§III definitions and Theorem3.1's block
simulation read. Silence carries information, and time/message tradeoffs are
established. Their parties already possess their inputs and have unbounded
local computation; the invoice acquisition duty instead charges for learning
the hidden values. No synchronized-connection hierarchy theorem is imported.

Saha et al.2019,
[Incremental Adaptive Attack Synthesis](https://arxiv.org/html/1905.05322v1):
abstract/introduction, motivating setup and§3 through the observation-
constraint definition read. Adaptive cost observations, symbolic transcript
constraints and reuse of constraint-solving/model-counting work are established.
This is a strong conventional antecedent to invoice-controller synthesis;
the objective/interface differ from the proposed all-protocol acquisition
rate. No reported speedup is transferred. Bang et al.2018's direct PDF link
returned404; its search abstract remains a lead only.

The Fano packing example uses elementary finite linear algebra. Searches
found classical matroid-port and nonideal binary-clutter literature, including
Guenin's author overview and the2007 box-Mengerian characterization. Those
abstracts/overviews are orientation only; no classification theorem is used.

# Prediction-assisted inspection and repair

Erlebach/de Lima/Megow/Schloeter2022,
[Learning-Augmented Query Policies for Minimum Spanning Tree with Uncertainty](https://drops.dagstuhl.de/storage/00lipics/lipics-vol244-esa2022/LIPIcs.ESA.2022.49/LIPIcs.ESA.2022.49.pdf):
read introduction, section4 Theorems7-9, displayed algorithm and Theorem9
proof. Certificates, untrusted predictions, bipartite covers and robust
fallbacks are established ingredients. Their consistency/robustness benchmark
is an instance-optimal verifying query set. Our query/write adapter's blind
write and confirming-certificate denominators are different; no numerical
superiority over their algorithm follows. Later error-sensitive proofs were
not read or imported.

Diwan/Hellerstein/Megow/Schloeter2025 preprint (STACS2026),
[Optimal Verification of a Minimum-Weight Basis in an Uncertainty Matroid](https://ir.cwi.nl/pub/36038/36038.pdf):
read introduction and section5.2 through Observation23 and Theorem24 statement.
The paper makes the verification-versus-universal-certificate distinction
explicit and gives prediction-assisted uses of its verification algorithm.
No matroid theorem or approximation guarantee is imported into our editable
Boolean-input duty. General uncertainty areas and paid verification are
strong comparison requirements, not ingredients invented here.

The prior context's Eftang/Patera port-reduction publisher abstract was an
orientation lead. Numdam and IGPM PDFs returned truncated outputs and were
not read. spd_fallback.md uses elementary inverse order independently.

Horvitz/Klein, [Reasoning, Metareasoning, and Mathematical Truth](https://arxiv.org/pdf/1302.4960):
read displayed introduction and sections4-5, plus displayed6.2-6.3 and
opening7.1. The paper explicitly models search-progress likelihoods and
procedure-dependent evidence. It is a direct antecedent to acting before
theorem-prover completion. No source performance percentage or universal
truth-calibration theorem is imported. Callaway et al.,
[Learning to select computations](https://arxiv.org/pdf/1711.06892),
introduction, sections2.1-2.3 and opening3 were revisited; the repository's
07_paid_reasoning_sources.md retains its deeper earlier source comparison.
The current reread earns only its new observed interval, not earlier credit.

Beines/Kaibel/Mayer/Mutzel/Sauer2024 preprint,
[A Simpler Approach for Monotone Parametric Minimum Cut](https://arxiv.org/pdf/2410.15920):
read introduction and opening section2.1. Nested cuts, breakpoint compression
and efficient parametric algorithms are established; no empirical speedup or
unread algorithm proof is imported. The Gallo/Grigoriadis/Tarjan1987 technical
report appeared in search but its direct PDF returned403; the requested
arXiv v2 HTML returned404, while the v1 PDF above was available.

Allman/Lo/McCormick2022,
[Complexity of Source-Sink Monotone 2-Parameter Min Cut](https://arxiv.org/pdf/2107.09743):
read introduction through Theorem1.1 and opening construction. Two parameters
can expose exponentially many general min cuts. This is a scope warning;
no unproved reduction imports that lower bound into the narrower hard-closure
action system. price_ray.md gives its own elementary nesting proof and
derives the additional threshold-world warrant.

Final synthesis revisited Zhou/Zhu, [Calibrating Decision Robustness via
Inverse Conformal Risk Control](https://arxiv.org/html/2510.07750), v3,
sections2–3.3 (definitions, stated guarantees and selection algorithm).
The fixed-parameter expected guarantee, its i.i.d. high-probability adapter,
and split recalibration after selection are distinct. Our nested unsafe-cost
score instead uses an ordinary one-sided tolerance bound for a fixed risk
target. The potentially useful adapter is computing a conservative common
decision-warrant score from partial truthful receipts, then protecting a
specified price menu. Neither risk calibration nor post-selection protection
is new in itself. No superiority to CREME, new statistical theorem, or source
experiment result is imported. The earlier interrupted output remains excluded.

Gilewicz/Pindor/Telega/Tokarzewski2005,
[N-point Pade approximants and two-sided estimates of errors on the real axis
for Stieltjes functions](https://www.ippt.pan.pl/Repository/o596.pdf): read
introduction, definitions, section2 lemmas and Theorem4 proof. Bounds from
several real interpolation points, including changes of inequality direction,
are established numerical-analysis tools. Tokarzewski/Wajnryb2011,
[General inequalities for multipoint Pade approximants](https://files.ele-math.com/abstracts/mia-14-83-abs.pdf),
abstract only, explicitly describes best bounds relative to the given
coefficients. This is a close antecedent to two_value_sharp.md, whose elementary
dual proof is reconstructed locally. Treat the new note as a useful explicit
specialization, not a newly discovered class of sharp interpolation bounds.
The2005 source uses a compact spectral interval and continued fractions;
our unbounded-spectrum closure and partial-receipt statements have their own
stated proof obligations. No source numerical gains or unexamined2011 proof
are imported. Search-result leads to1973/1996 papers were not full-text read.
