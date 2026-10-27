# s19 scoped primary literature notes

Codex (GPT-6), DEVELOPMENT. Search snippets are leads, not proof evidence.
Sections named below were inspected; no claim of a complete literature survey.

## Reserved ordinal-feedback screen

- [Oki--Sakaue, ICML2026](https://proceedings.mlr.press/v306/oki26a.html):
  published Assumption2.2 and AppendixD retain distinct coordinates for
  corrupted reports. The May arXiv tie extension is still uncorrupted.
  Published PDF was obtained from the PMLR-linked mlresearch repository.
- [Joshi et al., ICLR2026](https://proceedings.iclr.cc/paper_files/paper/2026/file/4975dfc24b3fd21d069842c90dd07c91-Paper-Conference.pdf):
  Algorithm1, section4.3/Theorem4 and tractability discussion read; the
  arXiv version's AppendixD.1 potential proof was inspected. Reward-class
  learning directly supplies the stronger ordinary error control in
  o18_experts.md. Large class representation is acknowledged in the paper.
- [Leme--Podimata--Schneider](https://arxiv.org/pdf/2206.07528): model,
  Theorem3.1/algorithm/proof and convex-optimization opening read. Unknown-C
  density methods are strong controls; varying convex objectives can share
  a minimizer. Zero inverse loss does not alone imply true-utility correctness.
- [Gupta et al.](https://www.renatoppl.com/papers/robust_contextual_pricing.pdf):
  model and Theorems3.1/4.1 read. The reduction uses pricing-specific sale
  structure; unknown-C layers retain a known upper bound and logarithmic
  factors. It is not automatically an O18 winner-feedback algorithm.
- [Raman--Subedi--Tewari2024](https://proceedings.mlr.press/v247/raman24b/raman24b.pdf):
  opening/model and relevance-ranking definition inspected; set-valued
  feedback differs from seeing just one optimum.
- [Pour--Mansouri--Ben-David2026v2](https://arxiv.org/html/2602.09402v2):
  models, finite-class result and linear-regret example inspected. Their
  agnostic changing-target comparison is not the fixed-true-order plus
  corrupted-report contract here.
- [Gelfand et al., NeurIPS2010](https://proceedings.neurips.cc/paper/2010/file/019d385eb67632a7e958e23f24bd07d7-Paper.pdf):
  introduction and perceptron cycling theorem in section2 read. Finite update
  sets under nonpositive inner products already give qualitative boundedness.
- [Harks2026](https://arxiv.org/html/2609.18342): introduction, Definition1,
  Theorem1 and related-work discussion read. Explicit quantitative antecedent
  [Amaldi--Hauser2005](https://pubsonline.informs.org/doi/abs/10.1287/moor.1050.0164)
  was reached only as an abstract. Do not call all prior bounds nonconstructive.
- [Daume et al.2015](https://arxiv.org/pdf/1510.03130): opening definitions,
  section6 Algorithm1/Theorem1 read, not the appendix proof. Margin-based
  inverse structured prediction is an ordinary antecedent; no tie/unknown-C
  quantitative result was extracted from those inspected sections.
- [Hopkins--McConville--Propp](https://arxiv.org/pdf/1612.06816):
  abstract and Lemma12/Theorem13 surroundings inspected. Equal-position
  chip splitting has the same familiar stable position pattern.
- [Galashin et al., Interval-Firing](https://www.math.ucla.edu/~galashin/papers/interval_firing.pdf):
  section4 process definitions and Lemma8.2 including proof read. Its
  non-escaping permutahedra give a close known explanation of the perceptron
  invariant. The central-firing sequel was also inspected at its
  permutohedron definition and Propositions6.4/6.6; it is not the main lemma.

## Conditional values and source changes

- [Mostafaee--Hladik--Cerny, 2015 manuscript](https://nb.vse.cz/~cernym/invp.pdf):
  introduction, section2 setup, Theorem3/Corollary1 and Example1 read.
  Prescribed optimal-value inversion and disconnected optimal-value images
  are established subjects. Their box-coefficient model and continuity
  assumptions differ from our source family conditioned on several shared
  observations. The new claim must concern the particular attainer algorithm,
  not discovery that possible values may have gaps.
- [Li--Cui2024v3](https://arxiv.org/html/2307.00780v3): opening and the s18
  Example1.1 comparison retained. Shared-parameter inverse-optimal-value
  inference is established. Our forward simplex program is its special case.
- [Hladik2018 tutorial](https://kam.mff.cuni.cz/~hladik/doc/2018-conf-ROBUST-IlpTutorial-talk.pdf):
  opening interval-image/verification discussion inspected as a primary
  exposition. It motivates exact images versus interval enclosures; no
  new theorem claim is based on a search snippet about its hardness slide.
- [Berger--Sankaranarayanan2024](https://guberger.github.io/assets/papers/template-based-piecewise-affine-regression.pdf):
  published pages5--6 and8 read via the author PDF; also the
  [L4DC2023 version](https://proceedings.mlr.press/v211/berger23a/berger23a.pdf),
  sections3--4. Compatible affine fits, infeasibility cores, subset search,
  set covers and optimistic/pessimistic cover stopping are already combined
  explicitly. This is a strong antecedent for our generic partial-proof
  acquisition mechanism. Our possible delta is conditional future-value
  images/contrasts with generator-specific constraints, not the cover loop.
- [Kim--Lee2023/2024](https://arxiv.org/abs/2308.08070): abstract and initial
  model text inspected through the primary NSF manuscript search result.
  Random-design max-affine estimation is a direct model antecedent. Full
  first-order convergence proof was not inspected; failed web fetches do
  not count as a comparison of its detailed guarantees.

## Broader cost-learning and uncertainty screens

- [Constantin--Doering2020](https://arxiv.org/pdf/2006.03139), section3.5,
  PDF pages19--20: the binary-root/sum/majority reconstruction argument is
  an exact antecedent of binary_risks.md. The candidate core is reproduced,
  not moderately novel. Quantum rotated contexts exceed our classical-event
  interface and are not imported as available measurements.
- [Tornede--Bengs--Huellermeier2021](https://arxiv.org/pdf/2109.06234):
  introduction, section2 and the section4/5 transition inspected. Online
  algorithm selection with right-censored runtimes already uses contextual
  bandits. The capped-policy bill and uncapped runtime are distinct learning
  targets; our note is an ordinary reduction, not a new censoring method.
- [Callaway et al.2018](https://cocosci.princeton.edu/papers/callawayLearningToSelect.pdf):
  opening and metalevel-MDP definition read. Learning computation choice
  from value/cost features is established. No new metareasoning principle
  is inferred from relabelling a capped proof policy.
- Matroid union is imported as classical Edmonds--Fulkerson machinery.
  [Berczi-Kovacs--Frank2026](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70668),
  section2 Theorems2.4--2.5, provides the exact rank-cover statement and
  cites the original Theorem1c; this is a modern exposition, not an audit
  of the original proof. The polynomial consequence is conventional.

## Additional broad comparisons

- Espindola-Winck, Hardouin and Lhommeau, *On the Set-Estimation of Uncertain
  Max-Plus Linear Systems*, [author PDF](https://perso-laris.univ-angers.fr/~hardouin/Set_estimation_Automatica_2024.pdf).
  Read the model in section3.1, the conditional-reach definition/equation6,
  and theorem1/complexity discussion. Exact inverse images and state sets
  already have disjunctive and tropical-polyhedral algorithms. This is a
  direct control for scalar-offset observations. General ordinary-linear
  coupling inside each generator polytope is not automatically a tropical
  polyhedron. The complete proofs and implementations were not audited.
- Jianwang and Ramirez-Mendoza2020, [paper](https://doi.org/10.1080/21642583.2020.1737845).
  Read introduction and feasible-set definitions/algorithm description.
  Mode classification followed by zonotope outer approximation is an
  established bounded-error approach; it does not by itself give sharp
  extrema over all latent assignments. No full theorem comparison here.
- Butkovic2019, [paper](https://doi.org/10.1007/s10957-018-1429-8).
  Read the primary publication's introduction, not its full proof. It
  identifies low-order polynomial one-sided tropical systems and uses
  residuation for optimization. Thus scalar-offset receipt inversion is
  established machinery; the derived contrast formula needs a closer
  tropical-fractional comparison before any novelty claim.
- Bemporad et al.2005 bounded-error piecewise-affine identification:
  bibliographic/search lead only; the requested PDF fetch failed. Do not
  claim its full results have been compared.

- Schmidhuber2004, *Optimal Ordered Problem Solver*,
  [author manuscript](https://sferics.idsia.ch/pub/juergen/oops2.pdf).
  The retrieved section2.1/2.2 text defines bias-optimality and gives
  probability-weighted generation/run/check budgets with doubling. This
  directly precedes the proof-investment weighted-search term. The journal
  PDF open failed; no full OOPS implementation/proof audit is claimed.
- Shah and Rajkumar2021, [Sequential Ski Rental](https://arxiv.org/pdf/2104.06050),
  read introduction, section3 and section4.1. Unknown buy cost is predicted
  across repeated seasons with stochastic buy-expert assumptions; this is
  distinct from paying resumable proof work until a checked certificate.
- Angelopoulos et al.2020, [Online Computation with Untrusted Advice](https://drops.dagstuhl.de/storage/00lipics/lipics-vol151-itcs2020/LIPIcs.ITCS.2020.52/LIPIcs.ITCS.2020.52.pdf),
  read introductory problem descriptions and contribution summary only.
  Rental/bidding consistency-robustness guarantees are direct conceptual
  controls; no full theorem reduction was established in this screen.

- Azar, Chiplunkar, Kutten and Touitou2020,
  [Set Cover with Delay](https://drops.dagstuhl.de/storage/00lipics/lipics-vol173-esa2020/LIPIcs.ESA.2020.8/LIPIcs.ESA.2020.8.pdf).
  Read model section2 and section6, Theorem14 and Lemmas15--17. Its
  frequency-plus-one counter/dual argument is the closest structural
  antecedent of shared_proofs. Prices are known, delay is revealed as it
  accrues, and purchased sets serve current requests. The proposed adapter
  uses unknown persistent proof-completion costs and charges unfinished
  progress. This is an interface distinction, not established novelty.
- Levy, Touitou and Rosenberg2024,
  [Online Weighted Paging with Unknown Weights](https://arxiv.org/abs/2410.21266):
  abstract only. It learns page weights from samples, a different observation
  mechanism from interruptible completion-threshold search. Retain as a
  literature lead rather than claim a theorem-level comparison.

- Additional searches for hidden buying prices and nonclairvoyant covering
  returned no directly matching completion-threshold theorem in the sources
  inspected. This is an incomplete search, not evidence of priority.
  Buchbinder--Naor's online primal-dual survey
  [primary manuscript](https://users.ece.northwestern.edu/~nickle/randAlg/BuchbinderN07.pdf)
  is a lead for the generic covering argument; its ski-rental excerpt assumes
  a known purchase price. No complete proof audit was done here.

- Additional Berger--Sankaranarayanan reading: published pages2--5,
  Problems1--3 and Theorem2. Their domains come from a supplied template;
  their fitted PWA pieces are not required to be the pointwise minimum of
  all affine pieces. This strengthens the generic covering antecedent but
  is not a direct theorem for our entire conditional source-image task.
- Anderson, Pfrommer and Sojoudi2023,
  [Tight Certified Robustness via Min-Max Representations](https://brendon-anderson.github.io/files/publications/anderson2023tight.pdf).
  Read Definition1, Assumptions1--3, Theorem2 and its proof dependency.
  Exact convex reformulations use a supplied finite min-max representation
  and a convex attack set. Old optimum receipts can make our conditional
  parameter source nonconvex; their theorem cannot be imported by replacing
  that source with its hull. Generic disjunctive convex optimization remains
  a strong comparator. No complete audit of their representation conversion
  or experiments was performed.

- Hoffman1952, [original NBS paper](https://nvlpubs.nist.gov/nistpubs/jres/049/4/v49.n04.a05.pdf):
  read section2 theorem and proof outline, plus section3's computational
  qualification. The linear inequality residual-to-distance theorem is
  imported, not rediscovered. OCR obscures some displayed norm formulas;
  no claim depends on transcribing those special-case constants.
- Pena, Vera and Zuluaga2020/2021,
  [author preprint](https://arxiv.org/pdf/1905.02894), introduction equations1--3
  and computational discussion on page3. The relative-polyhedron bound
  applies directly to fixed B_i. Their paper emphasizes the difficulty of
  obtaining upper constants; our stability consequence does not treat those
  constants as costless or already computed.

## Additional cheap screen: unknown-work search and covering

Im, Moseley, Xu and Zhang2023, Online State Exploration,
https://par.nsf.gov/servlets/purl/10479863 (publisher DOI
https://doi.org/10.1007/978-3-031-43421-1_20): read pp333-338, definitions,
applications and algorithm1, plus references; no full proof audit. The hidden
target is a vector to dominate; moves and incorrect-state penalties are
priced under monotonicity/submodularity assumptions. It imports a strong
ordinary exploration baseline but does not directly state our repeated CNF
proof-bank duty with fallback and persistent unknown completion lengths.
A reduction would need to preserve the changing request relation and cost.
Web retrieval failed502; the primary NSF-hosted PDF was retrieved directly.

Online Covering with Maximum Delay under Subadditive Service Costs2026,
https://arxiv.org/html/2609.32675: read introduction, section2 model and
section3 offline form. Known-cost instantaneous services explicitly have no
persistent acquisition or effect on future requests; maximum batch delay is
a different bill. Its covering terminology alone does not establish the
unknown-proof-work guarantee. No novelty conclusion follows from these
scope differences. The closer Azar et al. counter/dual comparison remains.

Searches for nonclairvoyant covering and unknown buying costs also returned
known-price ski rental, joint replenishment and online bidding. Those search
results are leads, not evidence that no hidden-completion theorem exists.

Shahaf and Horvitz2009, Investigations of Continual Computation,
https://erichorvitz.com/continual_computation_IJCAI_2009.pdf: read sections2
and3.1, including proposition3.1 and precedence-hardness sketch. Shared
subtasks, cached partial work and expected computation value are established
metareasoning machinery. Their greedy result uses future-task probabilities
and expected time saved; our proposed bound uses adversarial requests and
unknown completion-only progress. That distinction may support an adapter,
not an invention of continual computation or reuse. No full paper audit.

Wei et al.2026, Serve Now or Improve Later?,
https://arxiv.org/html/2610.06212: read introduction only. The contribution
uses state-aware one-step rollout and prices checkpoint/recovery/publication
for reusable capability construction. This supplies a practical cost warning:
our abstract resumable instruction stream cannot imply wall-clock or GPU
savings without those costs. The paper's stronger model and measurements
have not been reproduced here; its empirical gains are not ours.

Bamas, Maggiori and Svensson2020, The Primal-Dual Method for Learning
Augmented Algorithms,
https://proceedings.neurips.cc/paper/2020/file/e834cb114d33f729dbc9c7fb0c6bb607-Paper.pdf:
read sections1-3, algorithms1-4 and theorem1 proof sketch. Advising a covering
solution, accelerating its variables and charging to both advice and OPT
are explicit prior machinery. Their set costs are supplied and their main
cover construction is fractional with a separate rounding cost. Our(PA2)
is a proposed adaptation to paid hidden completion and finite certificate
clauses, not a new robust-advice paradigm. Full supplemental proofs unread.

Lu, Ren and Liu2026v2, Learning-Augmented Algorithms for Online Vertex Cover,
https://arxiv.org/html/2606.22831: read introduction, advice model, general-
graph algorithm2 and theorem2 proof. Equal endpoint loads with advice-
dependent known-weight thresholds give(1+lambda)consistency and(1+1/lambda)
robustness. Only purchased vertices are charged; our unused/unfinished
progress is paid. Their guarantee must not be numerically compared to ours
as if the bills and advice interfaces were identical. No reproduction of
their experiments or bipartite proof audit was performed.

Simchowitz, Jamieson, Suchow and Griffiths2018, Adaptive Sampling for Convex
Regression, https://arxiv.org/pdf/1808.04523: read model/introduction,
lemma2.1, algorithm1, proposition4.2 and its counting argument. The exact
midpoint-defect certificate and adaptive secant construction in risk_curve.md
are already present, with a stronger function-specific/noisy framework.
Park a generic new-algorithm claim. No stochastic theorem reproduction.
Siem et al.2007/2012 was an additional primary abstract lead; the institutional
PDF returned403 and its detailed theorem was not inspected.

Reid and Williamson2011, Information, Divergence and Risk for Binary
Experiments, https://www.jmlr.org/papers/volume12/reid11a/reid11a.pdf:
read introduction, section6.3 theorem21, proposition20 context and
lemma23/corollary24. Risk curves and experiment comparison/realizability
are established. No full87-page audit, and the worked two-experiment example
and query-count derivation above are our reconstruction, not attributed as
new results in that source.

## Completion-estimator screen (s19, October26)

- McLeish, *A general method for debiasing a Monte Carlo estimator*,
  [arXivv2](https://arxiv.org/pdf/1005.2228), sections1-2, equation1 and the
  variance/budget discussion through page5. The truncated inverse-survival
  sum directly contains the one-jump completion estimator: set the increment
  at the first success to its discounted payoff. Finite variance and useful
  error control require additional tail information. This is a direct
  antecedent, not merely a neighboring use of randomization. Examples were
  not reproduced.
- Cui, Fu, Peng and Zhu, *Optimal Unbiased Estimation for Expected Cumulative
  Discounted Cost*, [2020 version](https://arxiv.org/pdf/1804.04215),
  introduction pages1-2. Their objective is variance versus expected work
  for randomized truncation of cumulative cost, including comparisons with
  fixed truncation. Only the model, objectives and stated results were read;
  the optimal-control proof was not reconstructed. This does not establish
  the bounded-output envelope result here, but makes a generic novelty claim
  for discounted random truncation untenable.

## Max-affine identification comparison (additional s19 screen)

- Toriello and Vielma, *Fitting Piecewise Linear Continuous Functions*,
  [author manuscript](https://juan-pablo-vielma.github.io/publications/Fitting-Piecewise-Linear.pdf),
  section3.2, equations3.6-3.12, Proposition3.2 and model size discussion.
  The max-affine fitting model uses binary selectors for active pieces;
  negating it gives the same basic minimum/attainer disjunction as the
  receipt problem. Fixing fitted observations and bounding each piece's
  coefficients gives a direct ordinary mixed-integer control. The studied
  objective is fitting, not enumeration of all future attainable values.
  No solver-performance comparison was reproduced.
- Teichrib and Schulze Darup2024,
  [*Piecewise regression via mixed-integer programming for MPC*](https://proceedings.mlr.press/v242/teichrib24a/teichrib24a.pdf),
  sections2-3, equations2 and4-8, Theorem1 and its proof. Their difference
  of two max-affine models handles a larger fitted-function class using
  active-piece selectors. A bounded-coefficient specialization is a valid
  generic exact control here; no claim is made that the receipt algorithm
  subsumes their nonconvex regression problem. Theorem2's separate weight
  discussion and the empirical section were not used.

## Unknown-cost acquisition: a closer primary antecedent

Nadimpalli, Qiao and Rubinfeld,
[*No Price Tags? No Problem: Query Strategies for Unpriced Information*](https://arxiv.org/pdf/2511.06170),
November2025 v1. Read the model and result overview, section3.2 Definition11,
section2's round-robin overview, and Proposition39's proof in section6.1.
Cumulative investment reveals a variable at an unknown cost threshold, and
all investment is charged. Thus this acquisition interface is established.
Their average-case guarantees use uniformly random Boolean inputs and a
cost-aware query benchmark; Proposition39 separates zero-error acquisition
from known-cost querying. The full general algorithm and its martingale
analysis were not reconstructed.

For s19, the remaining candidate is a specific persistent monotone-proof
service with changing requests, possible noncompletion and paid fallback.
Neither uniform input bits nor a finite observation of nontermination is
available in that service. The source does not directly supply the stated
width-plus-one bound, but sharply narrows any novelty claim when combined
with the known cover counter/dual and advice machinery. Do not advertise
unknown completion costs alone as a new model or result.

## Robust fusion: direct antecedent found

De Oliveira, Ishii and Lin, [Robust Merging of Information](https://www.econ.cuhk.edu.hk/wp-content/uploads/2025/04/Henrique.pdf), February13,2021.
Read section4.1 Lemma1/Proposition1 and AppendixA.1 proof, plus the start of
section4.2. The compatible joint channel obtained by independently garbling
the binary Blackwell supremum is exactly our generic construction. Robust
value equals its Bayes value; an arbitrary Bayes-optimal policy need not be
robust on cells the least-informative channel makes null. Park generic novelty.
The same authors' [2025 revision](https://www.aeaweb.org/conference/2026/preliminary/paper/kfyaeTzE)
was inspected in its introduction only; its broader decomposition theorems
were not independently reconstructed. Neither source was needed to certify
the explicit four-cell example's elementary minimax calculation.

## Faster bottleneck primitive and bounded-error identification

- Stoian, [Approximate Min-Sum Subset Convolution](https://arxiv.org/pdf/2404.11364),
  v3 August9,2024, section3 Theorem3 and its chunk/Boolean-convolution proof.
  Exact min-max subset convolution is an established soft-O(2^(3k/2))
  primitive. Negation imports it into our max-min prefix/suffix tables.
  fast_bottlenecks.md reconstructs an explicitly tagged, entry-prefix
  implementation to cover asymmetry and ties; no new convolution theorem
  is claimed. The approximation results in section4 are not used.
- Bemporad, Garulli, Paoletti and Vicino,
  [Set Membership Identification of Piecewise Affine Models](https://cse.lab.imtlucca.it/~bemporad/publications/papers/sysid-03.pdf),
  2003, section2 Problem1 and section3 Problem2, equations4-5 and section3.1.
  Bounded-error data classification becomes partition into feasible linear
  subsystems; their initialization uses a greedy randomized method and need
  not find the minimum partition. This directly precedes the broad idea of
  retaining feasible affine parameter sets. The read sections do not state
  AR1's entire future-minimum image, its interval count or the parameterized
  reconstruction bound. That absence from these sections is not a global
  novelty finding. Their unknown region partition and model-count fitting
  duty also differs from our fixed labelled product of coefficient regions.

## Receipt components: greedy recoloring antecedent

Bonamy and Bousquet, [Recoloring graphs via tree decompositions](https://doi.org/10.1016/j.ejc.2017.10.010),
European Journal of Combinatorics69,2018. The indexed primary full text
provides Lemma6 and its proof: processing existing color classes in order
reaches a greedy coloring with at most one recoloring per vertex. A direct
publisher open returned403; the [arXiv manuscript](https://arxiv.org/pdf/1403.6386)
was accessible, and the same normalization occurs inside its Lemma6 proof
on page5 (the numbering and surrounding statement differ). This is a close
antecedent to our component proof. The receipt adaptation uses bin-specific
hereditary feasibility plus convex assignment cells and obtains the scalar
image consequence. The broader graph-mixing/treewidth theorems are not
imported. The separate feasibility-type cap has not received a complete
reconfiguration-literature comparison; it remains exploratory.

## Broader computation-policy reading

- Antipov and Doerr, [When Switching Algorithms Helps](https://arxiv.org/pdf/2604.07473),
  GECCO2026 author version. Read sections2.2,4 and the opening of5:
  the OneMax comparison uses a specified two-algorithm portfolio with
  static parameters. Section2.2 explicitly notes that a dynamic-parameter
  variant has a stronger linear bound and is outside that portfolio.
  The switch can use observed fitness stagnation instead of true distance.
  We did not reconstruct the full section5 probability analysis or run
  experiments. This is a comparison/inspiration source, not a new s19 gain.
- Gupta and Roughgarden, [A PAC Approach to Application-Specific Algorithm Selection](https://arxiv.org/pdf/1511.07147),
  v2 September2016. Read the introduction and section4.2 Theorem4.2 proof:
  a nested-interval MWIS construction defeats worst-case online learning
  over their continuous heuristic class. Section4.3's smoothing assumptions
  and finite-net strategy were inspected, not its full proof. This does
  not negate finite-expert guarantees and does not give policy regret for
  unobserved counterfactual cache states. No general learner is imported.

## Matroid receipt connectivity: established sufficient theorem

- Wdowinski, [Hall's theorem for reconfigurations and higher dimensional topological connectedness](https://arxiv.org/pdf/2511.04863),
  November2025. Read definitions, Theorem2.2, Proposition2.8 and the statements
  in section5.1. Excess topological connectivity of every union of color
  classes connects colorful simplices; matroid rank supplies that excess.
  The direct-sum copy construction in matroid_components.md makes this an
  antecedent to the strict-slack conjecture. Full topological proofs were
  not independently reconstructed; this is an import, not a new theorem.
- Hanaka, Iwamasa, Kobayashi, Okada and Saito,
  [Basis Sequence Reconfiguration in the Union of Matroids](https://drops.dagstuhl.de/storage/00lipics/lipics-vol322-isaac2024/LIPIcs.ISAAC.2024.38/LIPIcs.ISAAC.2024.38.pdf),
  ISAAC2024, definitions and section3 Theorem3/Lemmas4-6. Their fixed-size
  disjoint bases are reconfigurable exactly when coloop ownership agrees;
  exchangeability paths identify the invariant. Our variable-size assignment
  partitions use different moves. No direct equivalence or shortest-path
  algorithm is claimed from this source.

## Score correction and computational effort

- Predd, Osherson, Kulkarni and Poor,
  [Aggregating Probabilistic Forecasts from Incoherent and Abstaining Experts](https://www.princeton.edu/~kulkarni/Papers/Journals/j065_2008_PreOshKulPoo_DecisionAnalysis.pdf),
  Decision Analysis2008. Read sections4.2-4.5, Table5, Theorem1 and the
  appendix projection statement. Successive local coherence projections
  already give stepwise Brier improvement while trading constraint scope
  against computation. No empirical results from that paper are s19 results.
- Predd, Seiringer, Lieb, Osherson, Poor and Kulkarni,
  [Probabilistic Coherence and Proper Scoring Rules](https://www.princeton.edu/~kulkarni/Papers/Journals/j071_2009_PreSeirLieOshKulPoo_TransIT.pdf),
  IEEE Transactions on Information Theory2009. Read Theorem1,
  Proposition3/proof and sectionVII.A. Coherence domination and Bregman
  projection support the score-budget screen. We use only the elementary
  weighted quadratic specialization; no new general scoring theorem.

## Randomized proof scheduling comparison

Nadimpalli--Qiao--Rubinfeld2025 Proposition39 was revisited specifically for
the hidden-cost obstruction. Its uniform Boolean inputs and random cost
permutation differ from random_proofs.md's one successful proof machine;
only the information-barrier comparison is claimed. Gomes and Selman,
[Algorithm Portfolio Design: Theory vs. Practice](https://arxiv.org/pdf/1302.1541),
introduction and section3 opening, already frame interleaved and restarted
search using runtime profiles. No distributional guarantee from that paper
is imported into the fixed unknown-threshold model.

## Set estimation as a stronger contextual control

- Espindola-Winck, Hardouin and Lhommeau,
  [On the Set-Estimation of Uncertain Max-Plus Linear Systems](https://perso-laris.univ-angers.fr/~hardouin/Set_estimation_Automatica_2024.pdf),
  July4,2024 author version. Read section2 representations/complexity,
  section3 setup and section4 Definition3/equation6. It already computes
  conditional sets by prediction and measurement inverse images, using
  tropical-polyhedral representations. This is a direct antecedent to
  generic set-valued inference, though its max-plus state and interval-matrix
  hypotheses do not include arbitrary ordinary coefficient polytopes.
  No performance result or probability law is imported into s19.
- Tabatabaeipour and Stoustrup,
  [Set-membership state estimation for discrete time piecewise affine systems using zonotopes](https://orbit.dtu.dk/files/59450970/ECC.pdf).
  The indexed primary text exposes equations8-14 and Algorithms1-2:
  propagate and intersect unions of feasible sets, then use a zonotope
  implementation with overapproximated intersections. Direct PDF access
  returned403. This is a scoped comparison from the visible primary text,
  not a reconstructed theorem or an exact full-output complexity result.

## Inverse values, disjunctions and low-dimensional controls

- Ahmed and Guan, [The Inverse Optimal Value Problem](https://www.isye.gatech.edu/~sahmed/invlp.pdf),
  author version leading to the2005 paper. Read introduction, section2
  Propositions2.1-2.3, section3 Theorem3.1/reduction, and section4
  Propositions4.1-4.2. Inferring parameters from an optimum value is already
  established and can be hard. Their convex cost-set, single prescribed-value
  problem differs from retaining multiple nonlinear receipts, but rules out
  claiming generic value-only inverse optimization as new.
- Huchette and Vielma, [A mixed-integer branching approach for very small formulations of disjunctive constraints](https://optimization-online.org/wp-content/uploads/2017/09/6230.pdf),
  2017. Read sections1-2, Definitions1-5, Propositions1-2 and Theorem1;
  inspected the later formulation summary. General disjunctive formulations
  are mandatory controls. Two integer control variables over a domain with
  holes do not supply an ordinary fixed-dimensional integer-programming
  algorithm for free; alternatives and their representation remain inputs.
- Alon and Kalai, [Bounding the piercing number](https://web.math.princeton.edu/~nalon/PDFS/pierce4.pdf),
  1995, Theorem1.1, Corollary1.2 and its proof. Uniformly bounded numbers
  of convex pieces in every intersection yield finite Helly consequences.
  This is an antecedent to the exact-flat conflict discussion; no sharp
  constant or algorithmic cost is imported.
- De Loera, Petrovic and Stasi,
  [Random Sampling in Computational Algebra: Helly Numbers and Violator Spaces](https://arxiv.org/pdf/1503.08804),
  v3, December2015, published2016. Read section2 examples, Definition4.10
  and Theorem4.11 with its coefficient-space proof. A linear basis of
  polynomial coefficients preserves the common zero set. The explicit
  receipt-conflict bound combines this existing argument with ordinary
  Helly and affine branching. The paper's sampling algorithms were not
  reconstructed or assigned a free oracle cost here.

## Robust fusion: direct antecedents and an early rejection

- de Oliveira, Ishii and Lin,
  [Robust Aggregation of Correlated Information](https://arxiv.org/pdf/2106.00088),
  September2026 version posted October4. Read sections3.2-3.3, Corollary1,
  section4 Theorem2/Corollary2, AppendixA.2-A.4 and section7.1.1-7.2.
  Binary decision decomposition gives a sum of source-wise maxima and
  constructive dominating maps. Thus known-channel acquisition has the
  familiar submodular form, and a large game LP is not always required.
  Their discussion of overlapping marginals motivated, but does not itself
  prove, our separate tree screen. An October21 accepted-publication
  listing was visible; the accessible arXiv text is the version compared.
- Krause, McMahan, Guestrin and Gupta,
  [Selecting Observations against Adversarial Objectives](https://proceedings.neurips.cc/paper/2007/file/eae27d77ca20db309e056e3d2dcd7d69-Paper.pdf),
  2007, section2, equations2.1-2.2. Worst-case combinations of submodular
  objectives need not be submodular. Our certified-channel-type example
  specializes this established limitation; no new robust acquisition
  principle is claimed.
- Eban, Mezuman and Globerson,
  [Discrete Chebyshev Classifiers](https://proceedings.mlr.press/v32/eban14.pdf),
  ICML2014. Read sections2.1-2.4, Theorem2.1/proof, Corollary2.2,
  Theorem2.3, section4 Lemma4.1 and section5 scope. Their tree-marginal
  hinge formulation directly covers the proposed binary overlap LP after
  clipping the score difference and dividing hinge loss by two. The paper's
  deterministic-classifier approximation does not leave a missing factor
  in the randomized policy problem. PARK generic tree-fusion tractability.
- Farnia and Tse, [A Minimax Approach to Supervised Learning](https://proceedings.neurips.cc/paper_files/paper/2016/file/7b1ce3d73b70f1a7246e7b76a35fb552-Paper.pdf),
  2016. Read introduction, section2.2.2, section3 Theorem2/equation11 and
  section3.3.2. The empirical-input-marginal and cross-moment contract is
  different, but minimax classification itself is a strong established
  alternative. No new general robust-classification claim is retained.
- Malvestuto, [2010 marginal-extension paper](https://www.kybernetika.cz/content/2010/4/621/paper.pdf),
  introduction only. Its domination terminology concerns support inclusion,
  not pointwise submeasure domination. It was not used to justify the
  common-submeasure construction.

## Acquisition and reconstruction controls

- Wang and Boutilier,
  [Incremental Utility Elicitation with the Minimax Regret Decision Criterion](https://www.cs.toronto.edu/kr/publications/minimax.pdf),
  sections2-3, especially pairwise LP regret and Theorem1's piecewise-linear
  query-response characterization. Task-directed query selection and
  termination based on regret reduction are established. Their axis-parallel
  utility bounds and standard-gamble queries differ from anonymous minimum
  observations; a general relabelled acquisition rule is parked.
- Boutilier, Patrascu, Poupart and Schuurmans,
  [Regret-based Utility Elicitation in Constraint-based Decision Problems](https://cs.uwaterloo.ca/~ppoupart/publications/elicitationIJCAI05/elicitationIJCAI05.pdf),
  IJCAI2005, sections3.1-3.2, Propositions1-2, and the incremental-solver
  discussion. Midpoint bound queries give a worst-case regret-reduction
  guarantee; retained constraints and anytime solver bounds are already
  explicit. No empirical query savings from that paper are s19 evidence.
- Balcan, Daniely, Mehta, Urner and Vazirani,
  [Learning Economic Parameters from Revealed Preferences](https://www.cs.cmu.edu/~ninamf/papers/revealed-pref-optimal.pdf),
  July2014 version. Read definitions of the utility/query contracts and
  AppendixE, Theorem35 with the linear, separable-concave and Leontief
  constructions. Rich chosen value queries can identify these classes
  efficiently, using bounded parameter bit lengths. This is a stronger
  interface than a fixed retained scalar history and limits generic
  learning claims based on that history.
- Filmus, Moran and Nesterova,
  [Optimal Reconstruction from Linear Queries](https://arxiv.org/pdf/2605.19625),
  May2026. Read sections1-2 main theorem statements and section3's feasible
  region/radius setup. Proper versus query-specific reconstruction already
  separates attainable worst-case errors under bounded adversarial noise.
  We did not reconstruct the robust Jung theorem or import its rates as a
  new result; the distinction is a comparison lead, not a s19 contribution.

## Subset transforms and sparse receipt inference

- Bjorklund, Husfeldt, Kaski and Koivisto,
  [Fourier meets Mobius: fast subset convolution](https://kam.mff.cuni.cz/~matousek/cla/bjorklund-al-subsetconvolution.pdf),
  sections2.5 and4.1.2. Covering convolution via zeta/Mobius transforms and
  the use of monotonicity to avoid ranked convolution are explicit prior
  machinery. Our threshold-block adaptation does not originate either
  insight. Exact integer counts have O(k)-bit lengths; unit arithmetic
  counts must not be relabelled bit complexity.
- Stoian, [October2026 min-sum subset-convolution result](https://arxiv.org/pdf/2610.10282),
  introduction, Theorem1 and Corollary2 only. Its sub-3^k bounds concern
  min-sum, not the imported min-max primitive's2^(3k/2) bound. No full proof
  was reconstructed. Claims that3^k is still the best generic min-sum
  bound would be stale; none is needed here.
- Dechter, [Tractable structures for constraint satisfaction](https://ics.uci.edu/~csp/r139.pdf),
  sections2.1-2.2 and3.1, Theorems1 and13. Tree consistency and cutset
  conditioning are direct algorithmic antecedents. Their finite-domain
  input costs do not by themselves establish compact continuous-polytope
  messages, a connected full source or the claimed scalar-image bound.
- Jefferson, Moore, Nightingale and Petrie,
  [Implementing logical connectives in constraint programming](https://www-users.york.ac.uk/peter.nightingale/aij-watchedor-reify-paper.pdf),
  2010, DOI10.1016/j.artint.2010.07.001. Indexed primary abstract/body
  describes generalized arc consistency for OR when child constraints
  have no shared variables. Direct PDF retrieval failed, so the full OR
  proof was not reviewed. This is a mandatory comparison, not an absence
  finding or a reconstructed theorem in this session.
- Dabrowski, Jonsson, Ordyniak and Osipov,
  [Disjunctive temporal problem study](https://ojs.aaai.org/index.php/AAAI/article/download/16489/16296),
  AAAI2021, problem definition, Theorem3 and Lemma2. Incidence width and
  numeric magnitude enter their bounded-domain algorithm. Binary difference
  predicates differ from the disjunctions of unary block halfspaces here.
  The hardness gadget overview was read without full reconstruction; no
  lower bound is transferred to our more restricted contract.
- Shapiro, Feldman and Dechter,
  [On the Complexity of Interval-Based Constraint Networks](https://ics.uci.edu/~csp/r76-complexityinterval_based.pdf),
  1998, section2.1, Theorems1-3 and section5. Exact interval unions and their
  possible exponential growth are established. Acyclic arithmetic networks
  can still create gaps, so forest_receipts.md depends on its special OR
  predicates and convex local blocks, not acyclicity alone.
- Beringer and de Backer,
  [Satisfiability of Boolean formulas over linear constraints](https://www.ijcai.org/Proceedings/93-1/Papers/042.pdf),
  IJCAI1993, sections5.2-6.2. Disjunctive LP relaxations, propagation and
  conflicts are strong ordinary controls. The paper explicitly distinguishes
  local convex-hull relaxations from the global convex hull. No generic
  model-repair or LP-conflict novelty is claimed by our adapters.

## Topological scope

- Bauer, Kerber, Roll and Rolle,
  [A Unified View on the Functorial Nerve Theorem and its Variations](https://arxiv.org/pdf/2203.03571),
  June2025 arXiv version: TheoremC/4.8, Lemma4.9, Theorem4.10 and its
  triangulation proof. These supply the closed semi-algebraic good-cover
  implication used in forest_topology.md. The entire abstract-homotopy
  development was not reconstructed. Our work must establish its own
  contractible intersections before applying the imported theorem.
- Schnider and Weber,
  [A Topological Version of Schaefer's Dichotomy Theorem](https://drops.dagstuhl.de/storage/00lipics/lipics-vol293-socg2024/LIPIcs.SoCG.2024.77/LIPIcs.SoCG.2024.77.pdf),
  SoCG2024. Read Definitions3-4, Lemmas13-16, section3.1's setup and
  Corollary26. Cubical solution-space topology and its relation to CSP
  complexity already have substantial theory. The elementary sphere
  example is a scope counterexample, not a new generic topology result.
  The full universality proof and appendix were not audited.

## Probability information and inverse risk controls

- Artzner, Delbaen, Eber and Heath,
  [Coherent Measures of Risk](https://people.math.ethz.ch/~delbaen/ftp/preprints/CoherentMF.pdf),
  July1998 manuscript, published1999. Read Proposition4.1 and remarks,
  section4.2 Conditions4.1-4.2, Propositions4.2-4.4 and their proofs.
  Risk envelopes and extending partial risk measurements are established.
  Their largest coherent extension is a strong control for unrestricted
  envelopes; a fixed number of model-specific bounded generators adds
  constraints that cannot be silently discarded. Actual-risk guarantees
  still require a truth-to-envelope warrant.
- Chen, Wang, Zhao and Zhao,
  [Active Learning for Risk-Sensitive Inverse Reinforcement Learning](https://arxiv.org/pdf/1909.07843),
  2019, sectionsII-III.A, Theorems1-2 and equations6-9. Optimal demonstrated
  actions yield halfspace restrictions on a risk envelope through KKT
  conditions. The input is richer and different from scalar risk reports.
  Risk-envelope learning and active query selection are not new here;
  their experimental gains were not reproduced or used as our evidence.
- Ueta, Tanaka, Kobayashi and Nakata,
  [Inverse-Optimization-Based Uncertainty Set for Robust Linear Optimization](https://arxiv.org/pdf/2312.00391),
  2023, sections1-3 and Theorem1. Known optimal decisions supply an
  inverse-feasible cone, normalized to a polytope for robust optimization.
  This differs from unlabelled optimum values but is a strong source-aware
  comparator. No statistical or empirical gain is imported.
- Caprio, Sultana, Elia and Cuzzolin,
  [Credal Learning Theory](https://papers.nips.cc/paper_files/paper/2024/file/442443dbe8c4c7e1df7eda140921de36-Paper-Conference.pdf),
  NeurIPS2024, section3.1. Its data-derived credal sets and explicit
  true-process containment assumption reinforce the distinction between
  identifying a service's model collection and warranting actual loss.
  The generalization theorems were not audited or claimed for our example.

Further scoped leads: Krivulin's
[tropical polynomial optimization](https://arxiv.org/pdf/2002.03168),
2021 version, introduction only, concerns box-constrained tropical
polynomial minimization and elimination, not the same multiple retained
value contract. The Arizona
[partial inverse-optimization note](https://inverseopt.cs.arizona.edu/writeup.pdf)
describes partially specified optimal outputs and discrepancy fitting,
not a complete scalar predictive set. Neither lead constitutes a novelty
clearance. Failed primary PDF retrievals for some convex-CSP papers are
not negative evidence about their contents.

## Final multiclass comparison

Mazuelas, Romero and Grunwald, [Minimax Risk Classifiers with 0-1 Loss](https://jmlr.org/papers/volume24/22-0339/22-0339.pdf),
JMLR24(208),2023: read sections2.1--2.2, Theorem2, equations6--11 and
AppendixB. The precise specialization and PARK disposition are in
multiclass_fusion.md. The general-loss2022 reference is a lead, not a
completed proof comparison. One PDF hostname timed out; the primary
no-www JMLR copy was accessible. No experiments were reproduced.
