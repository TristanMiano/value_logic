# s12 primary-source comparisons

Codex (GPT-6), DEVELOPMENT. Accessed October 18/19, 2026. These entries record
what was actually read; search leads do not establish a theorem or priority.

## Task-specific reliance is already a substantial ordinary research area

- Bao et al., [Optimal Model Selection for Conformalized Robust Optimization,
  v1](https://arxiv.org/html/2507.04716v1), Sections 3.1–3.2, Algorithm 2,
  Theorems 3.1–3.4, Section 4.1. F-CROMS symmetrizes model selection over an
  augmented calibration/test sample; Theorem 3.3 gives finite-sample marginal
  robustness under exchangeability. Its efficiency result also assumes
  quantile regularity, bounded loss, local loss continuity and a model gap.
  Conditional results are distinct and require more structure. **Use:** closes
  the novelty route “choose a conformal model for downstream decision quality.”
  No theorem is yet imported into the invoice or repair setting.
- Cortes-Gomez et al., [Utility-Directed Conformal Prediction,
  v2](https://arxiv.org/html/2410.01767v2), abstract and Introduction. Constructing
  prediction sets for a supplied decision cost, rather than only their size,
  is established. The v2 title differs from the initial search record's v1
  title. Only introductory scope inspected; no efficiency theorem imported.
- Bai and Jin, [Conformal Selective Prediction with General Risk Control,
  v1](https://arxiv.org/html/2603.24704v1), abstract, Introduction and start of
  Section 2.1. Distinguishes marginal and selective deployment risk and treats
  bounded continuous risks with risk-adjusted e-values under exchangeability.
  **Use:** selective trust for a user-specified risk is not itself a new claim.
  Its guarantees must not be relabelled pointwise logical certification.
- Qu, [Active Epistemic Control for Query-Efficient Verified Planning,
  v1](https://arxiv.org/html/2602.03974v1), Introduction and Section 3.2. Separates
  grounded facts used for commitment from model beliefs used to prune plans.
  **Use:** “fallible simulation guides search; evidence certifies release” is
  an existing proposal. No empirical or correctness claim is imported from
  this paper; its detailed verifier assumptions remain to be inspected.

## Partial monitoring supplies the right task-level comparison

- Bartok, Pal and Szepesvari, [Minimax Regret of Finite Partial-Monitoring
  Games in Stochastic Environments](https://proceedings.mlr.press/v19/bartok11a/bartok11a.pdf),
  COLT 2011, pp. 135–137, Definitions 1–3 and Theorem 4. A signal matrix maps
  outcome laws to feedback laws; observability concerns **loss differences**,
  not recovery of the whole outcome distribution. In finite known games with
  iid outcomes, strongly Pareto-optimal actions and their neighborhood signal
  spans determine the trivial, square-root, two-thirds or linear regret cases.
  **Use:** this is a stronger and more relevant baseline for invoice-limited
  learning than full-law identification. Any consequence below must identify
  the invoice interface's contribution separately from this established theory.
  Adversarial guarantees require the later theorem, not this iid result.

## Leads retained without theorem import

- Zrnic and Candes, [Active Statistical Inference,
  v3](https://arxiv.org/html/2403.03208v3): retrieved; detailed assumptions next.
- Brawand et al., [Active Multiple-Prediction-Powered Inference](https://arxiv.org/abs/2605.08429):
  abstract lead only. Predictor selection, routing and residual-based label
  allocation are already studied jointly under a deployment budget.
- Lee, [A robust optimization approach with probe-able uncertainty](https://www.sciencedirect.com/science/article/pii/S0377221721005956),
  EJOR 2022: publisher abstract/introduction inspected. Querying to establish
  optimality against remaining uncertainty is established; full text not read.

## Additional inexpensive comparisons

- Zrnic and Candes, Active Statistical Inference v3 (link above), Sections 4–6,
  equations (1)–(2), Proposition 1 and sequential estimator. Read the AIPW
  residual correction, variance formula, adaptive propensity contract and
  distinction between their stated asymptotic intervals and time-uniform
  extensions. **Use:** task-specific residual sampling with fallible predictions
  and paid labels is established. We cannot call a generic correction sampler
  new; paired measurements and positivity still require an operational contract.
- Yano, [A Reduced Basis Method for Coercive Equations with an Exact Solution
  Certificate and Spatio-Parameter Adaptivity](https://epubs.siam.org/doi/10.1137/16M1071341),
  publisher abstract inspected. Certified output error and parameter/spatial
  adaptivity are established. The publisher search result for
  [Efficient reduced models and a posteriori error estimation for parametrized
  dynamical systems by offline/online decomposition](https://www.tandfonline.com/doi/full/10.1080/13873954.2010.514703)
  also identifies affine-parameter primal/dual residual reuse; full-page
  retrieval failed, so authors and detailed theorem hypotheses need checking
  before any theorem import. These suffice to deprioritize a generic numerical
  certificate-library proposal, not to establish exact priority for an extension.

## Noise and paid information

- Feige, Raghavan, Peleg and Upfal, [Computing with Noisy
  Information](https://cadmo.ethz.ch/education/lectures/HS18/SAADS/papers/computing_noisy_information.pdf),
  SIAM J. Computing 23(5), 1994. Read Sections 1.1–1.3, pp. 1001–1003, and
  start of Section 2. Independent constant-probability query errors and
  per-instance correctness are explicit. Repeating queries and aggregating
  them already gives a logarithmic overhead; parity has a matching order in
  their model. **Use:** the noisy-reset construction adapts this standard
  principle to cost-only group measurements. Its O(k log k) repetition factor
  is not a novel general phenomenon. Their lower bound is not automatically
  a lower bound for Gaussian invoice observations or arbitrary marker bundles.
- Verdu, [On Channel Capacity per Unit Cost](https://collaborate.princeton.edu/en/publications/on-channel-capacity-per-unit-cost/),
  IEEE Information Theory 1990. Primary institutional abstract and the
  first-page search extraction from the MIT-hosted paper inspected; full PDF
  retrieval failed. It studies communication under symbol costs. **Use:**
  information per unit cost is established. No capacity theorem is imported
  into the population-estimation calculation, whose task and accounting differ.
- Yakowitz and Spragins, [On the Identifiability of Finite
  Mixtures](https://doi.org/10.1214/aoms/1177698520), 1968, pp. 209–214:
  bibliographic record located; primary full-text retrieval returned no usable
  text. Secondary search leads identify translation-family identifiability as
  an antecedent. The note provides its own finite-support proof, explicitly as
  an elementary argument; exact primary theorem locator remains unchecked.

## Permission compilation and ordinary antecedents

- Aspvall, Plass and Tarjan, [A Linear-Time Algorithm for Testing the Truth
  of Certain Quantified Boolean Formulas](https://www.math.ucsd.edu/~sbuss/CourseWeb/Math268_2007WS/2SAT.pdf),
  IPL 8(3), 1979, pp. 121–123. Read the implication graph construction and
  Theorem 1's SCC satisfiability criterion and constructive proof, pp. 121–122.
  **Imported machinery:** 2-SAT graph semantics and extension of consistent
  implication-closed literals. The receipt-to-action compiler is an adaptation;
  it is not a new linear-time satisfiability algorithm. A first mirror failed;
  the linked primary-paper copy was readable.
- Bohler, Hemaspaandra, Reith and Vollmer, [The Complexity of Boolean Constraint
  Isomorphism, v2](https://arxiv.org/pdf/cs/0306134), Appendix E, Lemma 21,
  printed p. 20. Read its statement attributing the equivalence between
  bijunctive relations and majority closure to Schaefer. The elementary
  majority argument is reproduced specifically for the receipt update; the
  closure property is established prior work, not a new theorem here.
- Hoffmann and Brafman, [Conformant Planning via Heuristic Forward Search:
  A New Approach](https://cdn.aaai.org/ICAPS/2004/ICAPS04-042.pdf), ICAPS 2004,
  pp. 355–357, Planning Background and Search Space, Theorem 1 and Proposition 1.
  CNF belief states, universal action applicability, and SAT-based knowledge
  tests already support planning under initial uncertainty. Their 2-CNF
  relaxation is also a direct conceptual comparator. **Scope distinction:**
  the current adapter compiles all allowed coordinatewise atomic maps exactly
  for local target clauses and reuses projections under receipts. These sources
  do not establish priority for that narrower statement; the comparison remains
  open. General conformant planning capability is not a new claim.
- Picard, [Maximal Closure of a Graph and Applications to Combinatorial
  Problems](https://doi.org/10.1287/mnsc.22.11.1268), 1976: publisher abstract
  inspected. Weighted closure is established. The reduction to minimum cut
  will be given explicitly if used in an implementation; full original text
  and exact theorem locator have not yet been read.

- Bulatov and Jeavons, [An Algebraic Approach to Multi-sorted Constraints](https://www.cs.ox.ac.uk/activities/constraints/publications/CP03multisorted.pdf),
  Sections 2–3, Definitions 1–2 and 6–9, especially Definition 8 on printed
  p. 7. Read the distinct-sort operation definition and its preservation
  condition. **Use:** coordinate-dependent constraint-preserving functions
  are established objects. The proposed all-map compiler is a concrete Boolean
  homomorphism encoding, not a new notion of transformation. Their tractability
  theorems concern constraint languages and do not themselves establish a new
  receipt-update or paid acquisition result for this session.
- Fandinno et al., [Planning with Incomplete Information in Quantified Answer
  Set Programming](https://arxiv.org/pdf/2108.06405), v1, 2021. Read Section 3's
  state, sensing, conditional-plan and universal-success definitions, and
  Section 6's conformant encoding/Theorem 6.1, printed pp. 9–10; inspected
  Section 8's pointers. **Use:** the general quantified planning formulation
  already includes the semantics motivating our safe edits. Our narrow case
  eliminates the universal world quantifier through small local projections;
  no superiority to QASP or existing planning compilers has been measured.

## Redundant proof supports and partial probability information

- Song, Der Kiureghian and Sackman, [Seismic Response and Reliability of
  Electrical Substation Equipment and Systems](https://peer.berkeley.edu/sites/default/files/peer516_j._song_a._kiureghian_j._sackman_.pdf),
  PEER Report 2005/16, April 2006. Read Section 6.2.2, printed pp. 133–137,
  equations (6.12)–(6.16) and the following sharpness argument. It formulates
  arbitrary Boolean failure probabilities with partial marginal/joint bounds
  as LPs over basic events, crediting Hailperin and earlier work. **Use:** the
  proof-support risk LP is established machinery specialized to a logical
  support hypergraph. The 2003 AMAS PDF failed to open; the 2020 Byun–Song
  delayed-column paper was accessible only as a publisher search extract,
  with direct access forbidden. No theorem from that newer paper is imported.
- Michels, Hommersom, Lucas, Velikova and Koopman, [Inference for a New
  Probabilistic Constraint Logic](https://www.cs.ru.nl/~peterl/ijcai13.pdf),
  IJCAI 2013. Read Sections 3.1–3.2 and 4.1–4.2, especially equation (7):
  proof constraints are disjoined and then used for inference. Their defined
  random variables are independent; their specific probability formulas are
  not imported for arbitrary dependent premise errors. **Use:** collecting
  alternative logical supports is also established. The shared adaptive-action
  certificate must be judged on its concrete interface and costs.
- Hansen/Jaumard/Aragao 1995 PSAT paper: primary-host search extraction located
  the LP formulation and analytical-dual discussion; direct PDF fetch timed
  out. Retain as a lead, not a fully read theorem source.

## Affine operation menus and coding theory

- Randriambololona, [On products and powers of linear codes under componentwise
  multiplication](https://arxiv.org/pdf/1312.0022), inspected Section 2,
  Definitions 2.6/2.8, Proposition 2.11 and Corollaries 2.41/2.42 with their
  proofs (printed pp. 16–17 and 27 in the accessed version). Stabilizing
  algebras decompose into support-block indicators and have a Schur-product
  dual description. **Imported:** the algebra/decomposition structure. The
  receipt and operation interpretation, affine offset and explicit circulation
  example are developed here; no originality is claimed for the underlying
  code algebra. The paper itself identifies earlier decomposition results.
- Barelli and Couvreur, [An efficient structural attack on NIST submission
  DAGS](https://asiacrypt.iacr.org/2018/files/SLIDES/MONDAY/421/1110-1225/dagsCouvreur.pdf),
  Asiacrypt 2018 author slides, slide labelled 18/28, Definition 4 (PDF page
  index 28). Read the code-conductor definition. **Use:** the homogeneous
  safe-map condition is exactly an established conductor. No cryptanalytic
  result or complexity bound is imported. The general dual identity is also
  shown directly by the inner-product calculation in affine_edits.md.

## Exact priced parity and observable computation cost

- Nisan and Szegedy, [On the degree of Boolean functions as real polynomials](https://web.vu.lt/mif/s.jukna/boolean/Nisan-Szegedy.pdf),
  1994, Section 1.3.2 and Theorem 1.3, printed pp. 303–304; inspected the
  introductory multilinear representation and degree/decision-tree discussion.
  **Imported:** polynomial and Fourier lower bounds for query trees are
  established. The present maximum-invoice-path price argument uses those
  elementary tools for a different observation interface; the paper is not
  evidence of priority for our exact formula.
- Tizpaz-Niari, Cerny and Trivedi, [Quantitative Mitigation of Timing Side
  Channels](https://arxiv.org/pdf/1906.08957), v1, 2019. Read Introduction,
  Section 4/Definition 2 and Section 5's optimization formulation. Their task
  trades information leakage against added performance cost, including
  stochastic mitigation. **Use:** observation through execution cost and
  cost/information tradeoffs are established; neither is claimed as new here.
  The exact reset/parity price result has a different objective and interface.
- Phan et al., [Synthesis of Adaptive Side-Channel Attacks](https://eprint.iacr.org/2017/401.pdf),
  2017: the primary-host search extraction exposed Section II's adaptive
  history-to-public-input attacker and cost-observation model. Direct PDF open
  returned an internal error. Bang's 2018 dissertation search extraction also
  described Chapter 5's treatment, but direct eScholarship access hit a
  verification page. **Limited use:** these are clear primary leads for the
  established multi-run adaptive cost-observation setting; no theorem has been
  imported from unseen full text. A complete priority search remains open.

One unrelated arXiv PDF was opened from an incorrect identifier during this
search; no content from it is used. Broad phrase searches did not locate the
specific price formula, which is not evidence that it is new.

## Unfinished verification and random truncation

- Rhee and Glynn, [Unbiased Estimation with Square Root Convergence for SDE
  Models](https://web.stanford.edu/~glynn/papers/2015/RheeG15.pdf), 2015,
  Section 2/Theorem 1 and its proof, Section 3/Proposition 1 and Theorem 3,
  printed pp. 1028–1033. Read the coupled estimator, variance conditions and
  work/variance optimization. The paper explicitly credits McLeish's prior
  construction. **Use:** the generic roulette proposal is established;
  arbitrary mathematical verification does not inherit their convergence rates.
- Bengs and Hullermeier, [Multi-armed bandits with censored consumption of
  resources](https://link.springer.com/article/10.1007/s10994-022-06271-z),
  published 2022, volume 2023. Read Sections 2.3–2.4 and 3.2, equations
  (8)–(10), and the smaller-limit feedback update. **Use:** choosing resource
  caps and learning from censored observations is already a developed setting.
  Its stochastic arm hypotheses are not asserted for arbitrary proof streams.
- Tornede, Bengs and Hullermeier, [Machine Learning for Online Algorithm
  Selection under Censored Feedback](https://arxiv.org/pdf/2109.06234),
  arXiv source opened; publisher abstract inspected. Retain as a direct
  comparison lead. No theorem was imported from sections not yet read.

## Graphic inference and local repair

- Gopalan, Huang, Simitci and Yekhanin, [On the Locality of Codeword
  Symbols](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/r-d-codes.pdf),
  accessed author PDF, Section 2/Definition 2 and the following dual-codeword
  hypergraph on printed p. 4. Read the recovery-by-linear-dependence definition.
  **Use:** cheap recovery of a coordinate through other code coordinates is
  established local repair. The current invoice-weight substitution is an
  adapter; no new locality theorem or storage-code construction is claimed.
- Bruck and Naor, [The hardness of decoding linear codes with
  preprocessing](https://www.wisdom.weizmann.ac.il/~naor/PAPERS/hardness_of_decoding_ieee_paper.pdf),
  IEEE Transactions on Information Theory 36(2), March 1990, Section II,
  printed pp. 382–383, Facts 1–2, Lemma 1 and Proposition 1. Read the incidence
  row/cut-space facts and all-ones maximum-cut reduction. **Use:** the general
  graphic-target hardness is exactly an established decoding connection.
  Their signed-cut formulation must not be confused with the positive-capacity
  single-edge min-cut instance in graph_invoices.md. No new hardness or
  preprocessing theorem is claimed here.

## Paying for relation calibration

- Angelopoulos, Bates, Candes, Jordan and Lei, [Learn then Test](https://arxiv.org/pdf/2110.01052),
  arXiv v5, 2022. Read Section 1.1/Definition 1, Section 2.1/Theorem 1 and
  Sections 2.2–2.3.1, pp. 2–5. Their fixed-model calibration, valid tests and
  familywise selection control directly subsume the confidence-style relation
  admission step. The zero-observed-error rule here is an elementary binomial
  special case. Arbitrarily selecting a certified member is allowed only after
  simultaneous control; fixed-sequence order must be chosen independently of
  calibration. No new calibration principle is claimed. The Berkeley-hosted
  PDF returned 403; the arXiv PDF was read instead.
- Angelopoulos, Bates, Fisch, Lei and Schuster, [Conformal Risk Control](https://arxiv.org/pdf/2208.02814),
  arXiv v4, June 2025. Read Sections 1.1–1.2, Section 2.1/Theorem 1 and its
  exchangeability proof, and Section 2.4/Proposition 1, pp. 2–5. Their guarantee
  averages over calibration and test data; it requires the specified monotone
  loss family, boundedness and endpoint conditions. This supports keeping
  marginal risk distinct from high-probability control of a fitted rule's risk.
  The current fixed binary admission rule has a direct elementary proof; its
  sharper iid constant is not asserted under exchangeability alone.

## Outcome-dependent query prices

- Saettler, Laber and Cicalese, [Trading off Worst and Expected Cost in
  Decision Tree Problems and a Value Dependent Model](https://arxiv.org/pdf/1406.3655),
  arXiv v1, 2014. Read Section 1.1's finite objects/classes/tests contract and
  Section 3's branch-dependent cost formulation, DividePairs rule and lower
  bound setup, pp. 3 and 6–7. Outcome-dependent testing costs and separate
  expected/worst objectives are established. The cap-two reduction fits this
  framework with two oriented tests for each coordinate. Its contribution is
  the exact translation from a private invoice interface; no new general
  decision-tree optimization principle is asserted. Constructing an explicit
  hypothesis universe may itself be exponential, and is charged if used.

## Variable-cost invoice coding

- Golin and Rote, [A Dynamic Programming Algorithm for Constructing Optimal
  Prefix-Free Codes with Unequal Letter Costs](https://www.cse.ust.hk/~golin/pubs/Huffman2.pdf),
  IEEE Transactions on Information Theory, 1998. Read Sections I–II, printed
  pp. 1770–1772: unequal letter costs, run-length application and the tree
  representation. Variable-cost and run-length coding are established. Their
  encoder chooses codewords for supplied messages; our private encoder must
  acquire hidden coordinates within each paid reset episode. That restriction
  is an additional obligation, not resolved by importing a code tree.
- Shannon, [A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf),
  1948 reprint. Read Part I, Section 1, PDF pp. 3–4: unequal symbol durations,
  the counting recurrence and capacity root. This is the ordinary coding
  antecedent for treating invoice amounts as symbols with costs. Such a
  communication relaxation does not establish realizability by bounded private
  query programs. No new general channel-capacity result is claimed.

Anantharam–Verdu's Bits through queues was located through its university
abstract, but no queue theorem is imported: that stochastic service channel
is a different interface from exact deterministic invoices.

- Yao, [Probabilistic computations: Toward a unified measure of complexity](https://doi.org/10.1109/SFCS.1977.24),
  FOCS 1977: bibliographic original located; publisher access returned a
  JavaScript verification page, so no original internal theorem was read.
  Ben-David and Blais, [A New Minimax Theorem for Randomized Algorithms](https://arxiv.org/pdf/2002.10802),
  arXiv v2, 2020, Section 1, pp. 3–5, was read as a primary follow-on comparison.
  Its introduction explicitly attributes randomized/distributional minimax to
  Yao and distinguishes fixed worst cost, expected scores and low-bias claims.
  The invoice note uses only a directly proved averaging inequality plus
  transitive masking; it imports neither the newer ratio theorem nor a
  forecasting amplification theorem. The paper's forecasting-algorithm
  sections are a relevant separate lead for bounded truth forecasts.

The later forecasting screen read Sections 3.1, 3.3–3.5, particularly
Definitions 3.1–3.2 and Lemmas 3.9–3.10, pp. 19–24. It uses the hs score and
independent-repeat identity with explicit fixed-input scope. The conditional
process calculation and repeated-model counterexample in forecast_scores.md
are worked here; no new scoring or amplification principle is claimed.

## Adaptive observation constraints and implementation costs

- Saha, Eiers, Kadron, Bang and Bultan, [Incremental Adaptive Attack
  Synthesis](https://arxiv.org/pdf/1905.05322), arXiv v1, 2019. Read Sections
  2–4, especially Algorithms 2–4 and the prefix-comparison example, pp. 2–10.
  Adaptive inference from execution costs, grouping indistinguishable paths,
  and reusing observation constraints are established. Their objective is
  information gain for a supplied program; the present private-query interface
  additionally constrains and prices the encoder. Its exact target-specific
  prices are not supplied by their entropy heuristic. Model counting and
  synthesis costs remain real in both approaches. The prefix-stopping idea is
  closely related to familiar segment oracles; no novelty is claimed for
  learning a prefix from stopping time. This comparison narrows the candidate
  delta to the explicit query/reset/readout contract and its guarantees.
- Phan et al., *Synthesis of Adaptive Side-Channel Attacks*, 2017, primary
  ePrint 2017/401 PDF was located again but direct access returned 403. The
  search extract was only a lead; no additional internal theorem is imported.

## Symmetry and conservative changes

- Anders, [SAT Preprocessors and Symmetry](https://drops.dagstuhl.de/opus/volltexte/2022/16675/pdf/LIPIcs-SAT-2022-1.pdf),
  SAT 2022. Read Section 2/Lemma 1 and the transformation definitions in
  Section 3, pp. 1:4–1:7. Semantic symmetries form a group, and syntactic
  preservation is a different condition. Our universally safe XOR masks are
  a special semantic symmetry subgroup; receipt-conditioned maps into the
  original target are not generally symmetries of the remaining source.
- Vorel and Roman, [Complexity of Road Coloring with Prescribed Reset
  Words](https://ktiml.mff.cuni.cz/~vorel/bib/VO4.pdf), author preprint dated
  May 11, 2016. Read Definition 3.3/Theorem 3.4, p. 7, explicitly attributing
  the change-set intersection characterization of bijunctivity to Schaefer.
  This is an exact antecedent of the core edit-consensus observation, so that
  observation is retained as imported machinery, not a new result. Schaefer's
  original STOC 1978 PDF was indexed with the same statement, but both university
  mirrors and the ACM PDF returned 403 on direct access; its proof was not read.

## Priced choices and multiple objectives

- Aaronson, [Quantum Certificate Complexity](https://www.scottaaronson.com/papers/qcc.pdf),
  author manuscript, Definition 3 and Section 3/Lemma 5 (PDF pp. 2–4).
  Read the randomized verifier's reference-input completeness and arbitrary
  behavior on other same-value inputs, and the independent-query comparison.
  This is a direct antecedent of fixed-premise randomized auditing. The adapter
  does not improve general randomized certificate complexity.
- Hu et al., *Exact Finite-Population Sequential Auditing for Selective Release
  from Model-Proposed Candidate Sets*, Mathematics 2026: publisher HTML and
  PDF access failed (429/internal error). Search metadata suggests a close
  application comparison, but its technical derivation was not read or imported.

- Callaway et al., [Learning to select computations](https://cocosci.princeton.edu/papers/callawayLearningToSelect.pdf),
  UAI 2018, Sections 2–3 (PDF pp. 2–4). Read the metalevel-MDP and value-of-
  computation definitions, the myopic failure under complementary computations,
  and the learned mixture of value-of-information features. Generic learned
  computation selection would repeat this established direction; no new BMPS
  comparison or result is inferred from its abstract.
- Marquis, [Existential Closures for Knowledge Compilation](https://www.cril.univ-artois.fr/~marquis/marquis-ijcai11.pdf),
  IJCAI 2011, Sections 1–3, Definitions 3,7,8 and the beginning of Section 3.
  KROM-C[OR] and its conditioning/forgetting context are explicit antecedents
  of the model-union representation. The local permission adapter is not a new
  compilation language. The paper also points to Fargier–Marquis 2008.
- Waudby-Smith and Ramdas, [Confidence sequences for sampling without
  replacement](https://proceedings.neurips.cc/paper_files/paper/2020/file/e96c7de8f6390b1e6c71556e4e0a4959-Paper.pdf),
  NeurIPS 2020, Sections 1.1–2.3 (PDF pp. 2–4). Read the fixed nonrandom
  population model and binary prior/posterior-ratio construction. A working
  prior is not a prior distribution over mathematical truths. The audit note's
  zero-failure crossing argument is separately derived; no new confidence-
  sequence principle is claimed.
- Rajaraman et al., *Learning to Reason with Curriculum I*, COLT 2026: the
  proceedings landing page was accessible, but the direct proceedings PDF
  returned an internal error. Only a lead, with no technical theorem imported.

- Freund and Schapire, [A Decision-Theoretic Generalization of On-Line Learning
  and an Application to Boosting](https://www.schapire.net/papers/FreundSc95.pdf),
  JCSS 1997, author manuscript dated December 19, 1996. Read Figure 1 and
  Sections 2–2.2 (PDF pp. 4–7). Exponential weighting and its log-potential
  comparison are established machinery; only the invoice-loss interpretation
  is adapted here. A first output was truncated by context refresh and was not
  counted as read; the complete relevant output was obtained after recovery.

- Aissi, Mahjoub and Ravi, [Randomized Contractions for Multiobjective Minimum
  Cuts](https://www.contrib.andrew.cmu.edu/~ravi/mcmc-esa17.pdf), ESA 2017.
  Read Section 1's definitions and prior-work distinctions, pp. 6:2–6:4.
  Budgeted/global cuts, node restrictions and fixed terminal separation have
  different complexity claims. No algorithmic bound for their global-cut
  setting is imported into the present terminal-specific model-choice problem.
  The risk-cut note uses only a directly derived Lagrangian separator and a
  matching finite mixture certificate, not a new multiobjective-cut method.
- Drygala, Nagarajan and Svensson, [Online Algorithms with Costly
  Predictions](https://proceedings.mlr.press/v206/drygala23a/drygala23a.pdf),
  AISTATS 2023. Read Sections 1–2.1, pp. 1–4, including Theorems 2.1–2.2.
  They explicitly price prediction acquisition and distinguish when, whether
  and how often to ask. The basic value-of-prediction theorem uses a paid
  correct prediction; robust extensions are separately identified. Our proposed
  invoice orientation is a different adapter: a bad prediction increases the
  fee but does not make the decoded answer wrong. No general learning-augmented
  or prediction-purchase novelty is claimed.

- Brešar, Klavžar and Škrekovski, [The cube polynomial and its derivatives:
  the case of median graphs](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v10i1r3/pdf/),
  Electronic Journal of Combinatorics 2003. Read Sections 2–3, Propositions 1–3,
  pp. 3–5: cube-polynomial definition, product identity and expansions. These
  identify existing combinatorial machinery behind the proposed face potential;
  they do not establish its Bellman inequality, which the finite screen rejects.

- Efraimidis, [(alpha,beta) Fibonacci Search](https://arxiv.org/pdf/1012.0259),
  2010, Sections 2–5, Definitions 1–6 and Propositions 3–6 (pp. 3–7).
  Read the positive integer outcome prices, weighted decision-tree capacity,
  lower bound and matching search. This is the exact ordinary antecedent of
  the ordered-source invoice example. The adapter does not claim a new search
  principle or a gain over this method.
- Henshall, Schachte, Søndergaard and Whiting, [Binary Decision Diagrams for
  Affine Approximation](https://arxiv.org/pdf/0804.0066), 2008, Section 2.2,
  Definition 1 and Proposition 1 (p. 4). Read affine envelopes and translation
  of affine relations to vector spaces. General affine approximation is prior
  work. The present binary-source block argument is a local specialization.
- Nordh and Zanuttini, [Propositional Abduction is Almost Always
  Hard](https://www.ijcai.org/Proceedings/05/Papers/0524.pdf), IJCAI 2005,
  Section 2 and beginning of Section 3, Proposition 5. Read the width-two
  affine definition and polynomial abduction argument. Do not infer that
  arbitrary binary-source abduction or query selection is easy.
- The indexed ECAI 2002 Zanuttini PDF at frontiersinai.com redirected to an
  unrelated gambling page when opened. That content was discarded; the
  indexed snippet remains a bibliographic lead, not a paper read.

- Amir and Russell, [Logical Filtering](https://cdn.aaai.org/Symposia/Spring/2003/SS-03-05/SS03-05-001.pdf),
  AAAI Spring Symposium 2003. Read Section 2, Definition 2.1, Sections 4.2–4.4,
  especially Corollaries 4.7, 4.10–4.12. Compact state representations and
  tractable action/observation filtering are established. The lineage adapter
  uses a narrower action class and explicit original-pair reuse; it must not
  claim to invent indefinitely compact logical belief tracking.
- Palacios and Geffner, [Compiling Uncertainty Away in Conformant Planning
  Problems with Bounded Width](https://arxiv.org/pdf/1401.3468), JAIR 2009,
  Sections 2–4, Definitions 1,4–6 and Theorem 7. Read deterministic uncertain-
  initial-state semantics and conditional-knowledge compilation. Their
  conformant width is not our target-clause or invoice width. No planner
  performance number is imported into the present finite adapter.
- Brafman and Shani, [Replanning in Domains with Partial Information and
  Sensing Actions](https://arxiv.org/pdf/1401.6048), Sections 5.3.1–5.3.3,
  pp. 583–584. Read regression of observations to the initial source and the
  partially specified state cache. This is a particularly close antecedent:
  immutable-source reasoning and cached regression are already explicit.
  Our proposed delta is the restricted lineage/pair-cache amortization, not
  the general idea of reusing an initial logical model.
- Dietterich and Bakiri, [Solving Multiclass Learning Problems via
  Error-Correcting Output Codes](https://arxiv.org/pdf/cs/9501101), JAIR 1995,
  Section 1's coding explanation (p. 266) and Section 2.3 (p. 269). Read the
  minimum-distance correction principle and row/column separation discussion.
  Coherence guards are an error-detection adapter; the present marginal-only
  bound does not assume independent classifier errors.
- Lei, Song and Luo, [A new re-encoding ECOC using reject
  option](https://link.springer.com/article/10.1007/s10489-020-01642-2), 2020:
  publisher abstract/introduction only. This establishes a reject-option
  antecedent, not verification of an exact theorem matching our bound.
- Georgiadis, Kipouridis, Kosinas, Papadopoulos and Parotsidis,
  [Computing the (k+2)-Edge-Connected Components in k-Edge-Connected Digraphs
  in Subquadratic Time](https://drops.dagstuhl.de/storage/00lipics/lipics-vol374-icalp2026/html/LIPIcs.ICALP.2026.95/LIPIcs.ICALP.2026.95.html),
  ICALP 2026, Section 4.1, Definition 20 and Proposition 21. Read the residual
  graph and closed-set characterization of all minimum terminal cuts, which
  the authors explicitly attribute to Picard and Queyranne (1980), Theorem 1.
  The original full text was not read. This is the exact established machinery
  in the all-optimal-repair source adapter, not merely a loosely similar idea.
- Kohli and Torr, [Measuring uncertainty in graph cut solutions](https://www.microsoft.com/en-us/research/wp-content/uploads/2008/01/kt_cviu08.pdf),
  CVIU 2008, Section 2.1 equations 5–6, Sections 3.1–3.2 (pp. 31–33).
  Read unary/pair min-marginal definitions, residual capacities and submodular
  energy reduction. Exact constrained minima and dynamic cut reuse are prior
  work; the new repair-margin note supplies no comparative solver gain.
- Tarlow and Adams, Revisiting Uncertainty in Graph Cut Solutions, CVPR 2012:
  publisher abstract read as a lead; Princeton PDF returned an internal error.
  The Toronto-hosted PDF opened, but its technical sections have not yet been
  read. Do not import its calibrated marginal interpretation into repair fees.
- Lin and Reiter, [Forget It!](https://cdn.aaai.org/Symposia/Fall/1994/FS-94-02/FS94-02-037.pdf),
  AAAI Fall Symposium 1994, Definition 1, Propositions 2–3, Theorem 4 and
  Proposition 6 (pp. 141–143). Read model agreement outside forgotten atoms,
  preservation of retained consequences, substitution construction and
  commutation. These are the exact projection primitives of task adequacy.
- [On Forgetting in Tractable Propositional Fragments](https://arxiv.org/pdf/1502.02799),
  2015, introduction and Section 4.1 Corollary 14 / Section 4.2 Theorem 15.
  Read Krom closure/uniform interpolation and the strongest-necessary/
  weakest-sufficient condition connection. No new forgetting theorem is
  claimed by the binary task-envelope adapter.
- Feature-model slicing is a close application antecedent. The 2016 Krieter
  technical-report PDF at isf.cs.tu-bs.de returned an internal access error;
  the 2024 projected-d-DNNF slicing paper's ACM DOI returned HTTP 403. Their
  indexed abstracts identify projection with preservation of transitive hidden
  dependencies, but the technical texts were not read. They remain priority
  leads; do not claim configuration slicing as a new application principle.
- Shannon, [A Mathematical Theory of Communication](https://web.mit.edu/6.976/www/handout/shannon.pdf),
  1948 corrected reprint, Section 1 (pp. 3–4), Section 8 Theorem 8 and
  Section 9 Theorem 9 (p. 16). Read unequal symbol durations, the capacity
  characteristic equation and the noiseless coding converse. The invoice
  entropy bound adapts this existing result, with a direct finite-tree proof.
  It does not assert that the constrained private-query interface attains
  the ordinary cost alphabet's capacity.
- Giacobazzi, Ranzato and Scozzari, [Making Abstract Interpretations Complete](https://www.sci.unich.it/~scozzari/paper/JACM00.pdf),
  JACM 2000, Sections 1.1–1.2 (pp. 362–364). Read Galois abstraction,
  best approximations, soundness and exact preservation of selected semantic
  operations. Task-scoped preservation is an established abstract-interpretation
  objective. The present envelope's direct finite projection proof is a
  specialization, not a new general theory of abstraction completeness.
- Bodirsky and Mamino, [A polynomial-time algorithm for median-closed
  semilinear constraints](https://arxiv.org/pdf/1808.10068), 2018,
  Section 2.2, Theorem 2.1, and Section 3, Theorem 3.2 (pp. 3–4). Read
  majority/median preservation, binary decomposition and the TVPI/bijunctive
  representation. These are direct antecedents of the ordered-source adapter.
- Hunsberger, [Algorithms for a Temporal Decoupling Problem in Multi-Agent
  Planning](https://cdn.aaai.org/AAAI/2002/AAAI02-071.pdf), AAAI 2002,
  Definitions 2–4, Facts 2–3 and Theorem 4 (pp. 468–469). Read distance
  graphs/matrices, cubic generic closure and tight feasible difference ranges,
  attributed there to Dechter, Meiri and Pearl (1991). The original 1991 PDF
  at cse.unl.edu returned HTTP 502; do not claim it was read. No dynamic
  controllability or decoupling result is imported into the interval adapter.
- Gulwani and Tiwari, [Combining Abstract Interpreters](https://www.csl.sri.com/~tiwari/pldi06.pdf),
  PLDI 2006, Introduction (PDF pp. 1–2), Definition 1 (p. 4) and Section 6
  (p. 9). Read the distinctions between componentwise, reduced and logical
  combinations, and the separate role of disjunctive completion. Their exact
  combination results have convexity, stable-infiniteness and disjointness
  hypotheses; these are not imported into the finite Boolean adapter. This
  reinforces that combining task abstractions is established machinery.
- Patrick Cousot's [author overview of abstract interpretation](https://www.di.ens.fr/~cousot/AI/),
  Sections 1 and 3.14–3.17, read for the explicit task-preservation and domain
  combination interpretation. This overview supports the methodological
  comparison, not priority for the present restricted receipt bound. The
  separate MDP-abstraction search returned leads only; no MDP theorem is used.
