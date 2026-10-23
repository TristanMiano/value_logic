# s14 primary-source comparisons

## Interactive algebraic certificates

Dumas, Kaltofen, Thome and Villard, [Linear Time Interactive Certificates
for the Minimal Polynomial and the Determinant of a Sparse Matrix](https://arxiv.org/pdf/1602.00810),
v2December2019: introduction, Section3 definitions, Section4/Figure2 and
soundness/complexity proof through Theorem5 and Corollary6 (PDF pp7–10).
The committed rational function, random resolvent challenge and checked
linear-system response directly anticipate parametric_witness.md. This is
a strong rejection of a new verification-principle claim. Minimality and
general singular-field handling are stronger duties in the source; the SPD
adapter only needs rational-function equality. No determinant preconditioner
or implementation was imported. The author-host ISSAC2016 PDF introduction
was read first; a later deeper fetch timed out, so the substantive proof
reading used the explicitly different2019 arXiv version.

## Lossy acquisition and causal coding

- Kaspi and Merhav, [Zero-Delay and Causal Single-User and Multi-User Lossy
  Source Coding with Decoder Side Information](https://arxiv.org/pdf/1301.0079),
  displayed October29,2018 version: Section3 setup, Theorem1 and the discussion
  around Theorem3 (PDF pp7–12). Their encoder observes the current source
  symbol, retains causal history and sends an instantaneous code. This is a
  strong causal-coding comparator, but it does not directly impose paid
  private coordinate acquisition followed by answer erasure. The scalar
  time-sharing theorem is not imported as a proof for our high-reset gap.
- Permuter and Weissman, [Source Coding with a Side Information Vending
  Machine](https://arxiv.org/pdf/0904.2311), v2April2009: abstract and initial
  introduction/setup, PDF p1. Paid actions affecting information availability
  and rate/distortion/cost tradeoffs are established; the encoder initially
  has its source block. The journal-host retrieval timed out, so only this
  preprint's displayed introduction was read.
- Ahmadi and Simeone, [Robust Coding for Lossy Computing with Receiver-Side
  Observation Costs](https://arxiv.org/pdf/1108.1535): abstract and introduction,
  PDF p1. Computing a function, paid noisy measurements and measurement
  failures are established combinations. No later rate theorem imported.
  The earlier1105.4910 PDF URL returned404; the distinct1108.1535 paper is
  recorded explicitly rather than treated as the same full text.

## Finite perturbation comparison

El Ghaoui and Lebret, [Robust Solutions to Least-Squares Problems with
Uncertain Data](https://people.eecs.berkeley.edu/~elghaoui/Pubs/rob-ls.pdf),
SIAM J. Matrix Analysis and Applications18(4),1997: introduction and displayed
Theorem3.1, Theorem3.2/Remark3.2 and Theorem6.1 statements. Bounded matrix
uncertainty, robust least squares, regularization and continuity are well
established. Their optimization retains the nominal matrix and minimizes a
worst-case residual; the present receipt interface retains only one scalar
regularized value and a distance warrant. Later proofs were not reconstructed.
This identifies a close comparison class, not proof that the exact scalar
envelope is new. Search also returned Tikhonov sensitivity and ridge-leverage
work; only the previously recorded Diao/Wei/Qiao passages have been read.
Later reading added Theorem3.1's displayed proof and Section3.3 through
Theorem3.3: rank-one worst residuals and one-dimensional convex reductions
are already explicit. The possible delta is therefore the optimal envelope
conditioned on one/two retained scalars, not robust least squares or scalar
optimization itself. No full-matrix minimax theorem is silently imported.

Boyd and Vandenberghe, [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf),
Section6.4.2, printed pp319–322, especially the norm-bound-error derivation
pp321–322: the residual-plus-solution-norm objective and rank-one perturbation
are textbook machinery. Our receipt characterization must be assessed as a
specialization with a different retained-information contract. Other sections
returned by the PDF search were not treated as read proofs.

## Coding comparison for the full-recovery menu

- Aviran, Siegel and Wolf, [Optimal Parsing Trees for Run-Length Coding of
  Biased Data](https://cmrr-star.ucsd.edu/static/pubs/optimal_parsing_trees.pdf),
  ISIT2006 version, pp1495–1498: introduction, II-B, III-A and III-B including
  the displayed tree-search comparison. Source-word parsing, mean cost per
  source length and ordered leaf assignments directly precede the menu.
  The additional paid-acquisition feasibility condition t>=leaf depth is
  explicit here. The source supports narrowing the possible novelty to that
  constraint and general-policy results. No journal-version proof read.
- Drmota, Reznik, Savari and Szpankowski, [Tunstall Code, Khodak Variations,
  and Random Walks](https://www.dmg.tuwien.ac.at/drmota/tunstall08.pdf),
  dated February5,2008: abstract and introductory construction, pp1–3.
  Maximal-probability leaf expansion and complete parsing trees are standard.
  No later asymptotic theorem imported.
- MIT6.441 [supplementary Tunstall notes](https://web.mit.edu/6.441/spring06/handout/sup/Tunstall_codes_-_Notes_1.pdf),
  dated February10,1994, pp1–4: parser/coder distinction, complete dictionary
  and expected phrase-length objective. Amjad and Bocherer,
  [Fixed-to-Variable Length Distribution Matching](https://arxiv.org/pdf/1302.0019),
  v2July2013, introduction and SectionI definitions: prefix-tree distribution
  matching is another close existing formulation. Later algorithm not read.

## Additional numerical comparison

Sion, [On General Minimax Theorems](https://msp.org/pjm/1958/8-1/pjm-v8-n1-p14-p.pdf),
Pacific Journal of Mathematics8(1),1958, printed pp171–174: introduction,
Section2 definitions and Theorem3.4 with its displayed proof read. The
compact continuous convex-concave special case licenses the interchange in
partial_two_scalar.md. Its hypotheses are checked there for the moment
region and alpha interval; no analogous interchange is assumed for an
arbitrary full-matrix uncertainty problem.

Braess and Hackbusch, [On the approximation of Stieltjes functions by
exponential sums and rational functions with applications to partial
differential equations](https://link.springer.com/article/10.1007/s00211-025-01523-1),
published December2025, volume2026: introduction, displayed interpolation
discussion in Remark3.2, section4.2.1/Theorem4.3 proof and section4.3.1 through
Theorem4.6 and its comparison discussion read. Rational interpolation,
Blaschke products and exponential approximation rates are strong existing
machinery. A simple logarithmic nearest-receipt cover cannot support a claim
of optimal general sampling. The local rational_receipts.md derives its
fixed-pole residual directly and adds interval accounting; it does not import
the paper's best-approximation algorithm or unread convergence proofs.
The IWOTA2024 session-abstract PDF returned502 and was not read.

Codex (GPT-6), DEVELOPMENT. Accessed October 22, 2026. Read scope below is
limited to displayed material; search leads are not treated as read proofs.

- Arunachalam and Podder, [Communication Memento: Memoryless Communication
  Complexity](https://drops.dagstuhl.de/storage/00lipics/lipics-vol185-itcs2021/LIPIcs.ITCS.2021.61/LIPIcs.ITCS.2021.61.pdf),
  ITCS2021: abstract, introduction and beginning of background, pp1-3.
  Parties already possess their inputs; the principal measure is maximum
  message size per round. Forgetting is established, but this interface does
  not charge an encoder to acquire hidden coordinates before producing a
  count-only response. Later equivalences and lower-bound proofs not read.
- Sabato, Sarwate and Srebro, [Auditing: Active Learning with Outcome-Dependent
  Query Costs](https://proceedings.neurips.cc/paper_files/paper/2013/file/40008b9a5380fcacce3976bf7c08af5b-Paper.pdf),
  NeurIPS2013: introduction/setup and beginning of section2, pp1-3. Labels
  are observed after purchase and negative labels incur the audit fee.
  This is a close cost-dependent acquisition antecedent; it differs from
  observing only the count of hidden private queries. No sample-complexity
  theorem is imported into the invoice construction.
- Mutny and Krause, [Experimental Design for Linear Functionals in RKHSs](https://papers.nips.cc/paper_files/paper/2022/file/7f2223201858b6ff4cc1832d8856459b-Paper-Conference.pdf),
  NeurIPS2022: introduction and opening background, pp1-2. Directly estimating
  a requested functional, controlled approximation bias and adaptive designs
  are established. The bounded RKHS/noise premises differ from a positive
  spectral measure with deterministic solver intervals. No later confidence
  theorem or empirical gain is imported. This blocks generic task-directed
  querying as a novelty claim by itself.

Search leads to robust model aggregation and Stieltjes experimental design
remain orientation only. No conclusion that an exact prior match is absent.

- Durr, Erlebach, Megow and Meissner, [An Adversarial Model for Scheduling
  with Testing](https://arxiv.org/pdf/1709.02592), displayed2020 version:
  introduction and section6, Lemma20/Theorems21-23 with their proofs,
  pp31-32. Testing versus guaranteed execution and the sharp randomized
  one-job4/3 comparison directly anticipate the one-bit reliance primitive.
  The paper's offline-optimum denominator is stronger than blind correction;
  the parameterized prediction/budget adapter here uses a different contract.
  No sum-of-completion-times proof or experiment was imported.
- Albers and Eckl, [Explorable Uncertainty in Scheduling with Non-Uniform
  Testing Times](https://arxiv.org/pdf/2009.13316): abstract, section4,
  Theorem6 and Appendix D.7 proof. The nonuniform test-time result supports
  the normalized test/fallback comparison. Other scheduling bounds not
  imported. The random_reliance note records the concrete reduction and
  limits the possible contribution to a certificate/risk-budget adaptation.
# Budget-dependent model reliance

* Mehlhorn and Michail, *Minimum Cycle Bases: Faster and Simpler*,
  https://www.mpi-inf.mpg.de/~mehlhorn/ftp/MinCycleBasisFasterSimpler.pdf.
  Read abstract, introduction and Section 2/2.1 (PDF pp1–4). The cycle-space
  vector matroid, greedy extraction and polynomial candidate sets are direct
  antecedents. The threshold-span argument in budget_warrants.md is an
  elementary matroid consequence, not a new basis algorithm. Horton’s
  1984 repository record was also located, but its PDF was not read.
* Jeavons and Petke, *Local Consistency and SAT-Solvers* (JAIR2012),
  https://arxiv.org/pdf/1401.4613. Read introduction and Section2.1,
  Definitions1–2 and Lemma1 (printed pp329–331). Local-consistency methods
  are a strong bounded-inference comparison. Our cap is the number/price
  of physical receipts in a final inference, not width of intermediate
  constraints; no later simulation proof or experiment is imported.

# Matrix-response transport comparison

* Massei and Robol, *Rational Krylov for Stieltjes matrix functions:
  convergence and pole selection*, BIT2021 (online2020),
  https://link.springer.com/article/10.1007/s10543-020-00826-z.
  Read introduction, Section3.3 Theorem3/Remark2, Lemma4 and its proof,
  Corollary1, and Section3.5 discussion. The symmetric rational product and
  optimal pole placement are direct classical antecedents of receipt_design.md.
  Matrix-access rational Krylov is a strong control; scalar interval receipts
  have a weaker interface. No new Zolotarev principle is claimed.
* Chu, Lin, Tan and Wei, *Condition numbers and perturbation analysis for
  the Tikhonov regularization of discrete ill-posed problems*,
  https://doi.org/10.1002/nla.702, located as a relevant older comparator.
  The CiteSeer PDF retrieval returned403; indexed excerpts exposed a
  solution-vector unrestricted perturbation theorem, but no substantive
  full-text read or independently checked import is claimed. The specific
  sharp scalar-only finite response envelope remains a literature question.

* Kolmogorov and Zabih, *What Energy Functions Can Be Minimized via Graph
  Cuts?* (PAMI2004), https://www.cs.cornell.edu/~rdz/Papers/KZ-PAMI04.pdf.
  Read Theorem4.1 and constructive Section4.1, pp150–151. Binary pairwise
  submodularity permits an explicit cut representation. The defect-score
  model is an elementary directed-arc special case; its minimization is
  established machinery. No general higher-order claim is imported.
* Ge, Juba, Nilsson and Shao, UAI2026 proceedings page
  https://proceedings.mlr.press/v337/ge26a.html and its preliminary arXivv1
  https://arxiv.org/pdf/2602.14890, *Lifted Relational Probabilistic Inference
  via Implicit Learning*. Read preprint introduction, Sections2–4 and Section5
  limitations (PDF pp1–8). Query-directed reasoning from partial examples
  without a complete learned model is a strong established comparison.
  Its bounded-degree/quantifier-rank, explicit boundedness, sampling and
  witnessing hypotheses matter. In particular, the introduction separates
  a fixed grounding across examples from selecting a favorable grounding on
  each example. No theorem or bit-complexity guarantee is imported as
  independently verified here. The final proceedings PDF could not be parsed
  by the web tool (application/octet-stream), so this reading is explicitly
  the preliminary version. Nilsson1986 was also located, but its substantive
  PDF retrieval timed out; no new full-text read claim is made.


The following acquisition-model lead was also screened: Aspnes, Blais,
Demirbas, O'Donnell, Rudra and Uurtamo, *k+ Decision Trees*,
https://www.cs.cmu.edu/~eblais/papers/k-plus-dts.pdf. Read abstract,
introduction and Section2.1 definitions (PDF pp0–3). A query returns the
number of true selected literals, capped at k, for one query charge.
Our invoice reveals how many individually paid queries a private adaptive
tree executed. These are different observations and tariffs. The paper is
a relevant aggregate-query comparator, not a direct proof of the invoice
rate or a demonstrated absence of prior work. No later theorem is imported.


* Diao, Wei and Qiao, *Structured Condition Numbers of Structured Tikhonov
  Regularization Problem and their Estimations* (2016 preprint),
  https://arxiv.org/pdf/1601.02333. Read introduction pp1–3 and Section3.1,
  Lemma3 and its proof pp8–9 (PDF indices7–8). Structured perturbations and
  sensitivity of selected functionals are established; the proof expands the
  regularized inverse and derives its Frechet derivative. This is a direct
  ancestor of response-focused perturbation analysis. The current adapter
  derives a global bound for a different scalar value and then integrates a
  value-dependent derivative bound. Neither that difference nor a failed
  keyword search establishes novelty. No statistical condition estimator or
  numerical benchmark is imported here.
* Chung, Kilmer and O'Leary, *A Framework for Regularization via Operator
  Approximation* (2015), https://doi.org/10.1137/130945363. Read publisher
  abstract only: nearby structured operators support cheaper parameter
  selection, with solution/residual perturbation bounds. This supplies an
  established use-case comparator. Full proof not accessed; no bound from
  this paper is claimed as verified or used in receipt_transport.md.

## Further breadth and target-warrant comparisons

- Diwan, Hellerstein, Megow and Schloeter, *Optimal Verification of a
  Minimum-Weight Basis in an Uncertainty Matroid*, STACS 2026,
  https://drops.dagstuhl.de/storage/00lipics/lipics-vol364-stacs2026/LIPIcs.STACS.2026.32/LIPIcs.STACS.2026.32.pdf.
  Read introduction pp32:1-3 and Section 5.2, pp32:17-19, including
  Corollary 32's proof and Theorem 33's statement; the latter proof is
  deferred to the full version and was not read. This is a close paid-query
  comparison, explicitly separating a good predicted basis from a cheaply
  verifiable one. No new matroid benchmark or generic prediction-plus-
  verification claim is selected from this pass.
- Kleinberg, Leyton-Brown, Lucier and Graham, *Procrastinating with
  Confidence: Near-Optimal, Anytime, Adaptive Algorithm Configuration*,
  NeurIPS 2019, https://openreview.net/pdf?id=SJlzR4rg8H.
  Read introduction through Section 1.2 and Section 3's controller,
  lower-confidence construction and Example 3.1 (PDF pp4-6); not the
  complete theorem proof. The method already allocates capped runs and
  preserves unfinished evidence while pursuing useful configurations.
  Generic censored solver selection is therefore not a fresh mechanism.
- Hanselle, Tornede, Wever and Huellermeier, *Algorithm Selection as
  Superset Learning: Constructing Algorithm Selectors from Imprecise
  Performance Data*,
  https://epub.ub.uni-muenchen.de/91670/1/_PAKDD__Superset_Learning_for_Algorithm_Selection_with_Right_Censored_Data.pdf.
  Read abstract/introduction and Sections 2.2-3 through the optimistic
  superset-loss definition, printed pp4-6. This is a direct ancestor of
  learning from truthful interval-valued runtime labels. Its optimistic
  fitting loss is not by itself a worst-case deployment certificate.
- Eppstein, McCarthy and Parrish, *Rooted Cycle Bases*, arXiv1504.04931v1,
  April 20, 2015, https://arxiv.org/pdf/1504.04931 (journal version 2017).
  Read introduction, Section 2, Theorem 1's statement, Sections 4.1-4.4
  displayed lemmas/proofs and Theorem 2's proof, printed pp1-11.
  The polynomial positive-weight rooted-basis algorithm is imported.
  Appendix B's full tie-breaking construction was not reconstructed.
  Our target/price adapter uses a union of these ordinary bases and the
  matroid threshold property; it does not claim a new rooted-basis solver.
- Juettner, Kiraly, Mendoza-Cadena, Pap, Schlotter and Yamaguchi,
  *Shortest odd paths in undirected graphs with conservative weight
  functions*, arXiv2308.12653v1, https://arxiv.org/pdf/2308.12653.
  Read abstract and introduction pp1-3. Nonnegative shortest simple odd
  paths have established polynomial methods; unrestricted conservative
  weights have a different hardness boundary. Only this algorithmic
  orientation is used. No theorem proof or implementation is imported.
- Mehlhorn and Michail, *Minimum Cycle Bases: Faster and Simpler*,
  https://www.mpi-inf.mpg.de/~mehlhorn/ftp/MinCycleBasisFasterSimpler.pdf.
  Additional read: Section 2.1's support-vector description, printed pp3-4.
  It is the ordinary basis framework behind weighted_cycles.md; the
  nonadditive price oracle is supplied separately in that note.

Search-result leads concerning cycle edge participation and non-additive
costs were not used as verified theorems. Search absence is not novelty
evidence. The interrupted earlier broad-search output has no read claim.

- Nordh and Zanuttini, *What makes propositional abduction tractable*,
  https://gustavnordh.com/abductionAIsub.pdf. Read Section 6.2, Definition 36
  and Lemma 37, printed p29, plus the displayed related-work complexity
  statements on pp16-17. The prime-implicate characterization is a direct
  ancestor; those cited complexity results were not independently proved.
- Dechter and Pearl, *Structure identification in relational data*,
  Artificial Intelligence 58 (1992) 237-270,
  https://ftp.cs.ucla.edu/pub/stat_ser/r172-reprint.pdf. Read Section 3.2's
  Definitions 3.14/3.16 and Theorems 3.19-3.23 with displayed proofs,
  printed pp247-250, and the preceding projection-network construction.
  Restricted-scope logical approximations are established machinery.
  Historical conjectures elsewhere in the paper are not used as theorems.
- O'Sullivan and Provan, *Approximate Compilation for Embedded Model-based
  Reasoning* (AAAI 2006),
  https://www.cs.ucc.ie/ccsl/GP-papers/2006/AAAI06-compile-Final.pdf.
  Abstract and introduction only. Preference-aware incomplete compilation
  is an additional established direction; no algorithm or guarantee is
  imported from this limited read.

- Hanneke and Kontorovich, *Stable Sample Compression Schemes* (2021),
  https://proceedings.mlr.press/v132/hanneke21a/hanneke21a.pdf.
  Read introduction, Theorem 9's statement, Theorem 10 and Corollary 11
  with their displayed proofs, and Appendix A's Theorem 9 proof (p25).
  Their data-dependent compression bounds are imported unchanged. The
  partial-receipt wrapper bounds the rank of hidden sampled syndromes;
  it does not introduce a new concentration inequality.
- Ye, Amin and Ozdaglar, *Learning Decision-Sufficient Representations for
  Linear Optimization*, arXiv2603.18551v2 (May 22, 2026),
  https://arxiv.org/pdf/2603.18551. Read introduction pp1-3; Section 3's
  Corollary 4; Section 4.2 Definition 6, Remarks 7/8 and Property 9 proof;
  Section 5.3 Lemmas 19/20, Theorem 21 and Property 22 with displayed
  proofs; Section 6 Algorithm 2, displayed Lemmas 23-25, and Theorem 26's
  statement and displayed proof portion, pp13-14. Definition 6 requires
  a common optimal decision on each fiber; global Definition 1 recovers
  the full optimal set. Algorithm 2 uses a LINEAR QUERY ORACLE on iid
  sampled cost vectors, not free full vectors. This is a close ancestor
  of decision-relevant compression and its learning. No complete theorem
  reconstruction, complete price comparison or imported hardness claim.
- Welsh, *Transversal Theory and Matroids* (1969),
  https://doi.org/10.4153/CJM-1969-145-0. Read Sections 1-2, especially
  Rado's theorem and Perfect's partial-transversal corollary on p1324.
  The hidden-rank min-max formula is a direct import of this corollary.
  The interrupted earlier PDF request receives no read credit; this is
  a fresh bounded read of the relevant primary statement.

Juba's AAAI2019 endpoint was inaccessible; an attempted alternate PDF
and the Campi-Garatti wait-and-judge repository page were truncated during
context refresh. They remain leads, not read evidence. Edmonds's 1979
publisher page was only an abstract/metadata read. No theorem is imported
from those limited or unavailable outputs.

- Bousselmi, Hendrickx and Glineur, *Interpolation Conditions for Linear
  Operators and Applications to Performance Estimation Problems*, SIAM
  J. Optim.34(3),3033-3063 (2024), https://arxiv.org/pdf/2302.08781.
  Read Sections 2.1-2.2, Theorem 3.1, the main-text Lemmas 3.4/3.5 and
  their proof route, the displayed proof of Theorem 3.1, and Section 3.3
  including Theorem 3.6 and its displayed proof. Appendix B/C's full
  constructive proofs were not reconstructed. Theorem 3.1 is imported
  directly in counterfactual_sdp.md; Gram interpolation is not new here.
- Boyd and Vandenberghe, *Convex Optimization*, approximation/fitting
  lecture, revised slides with Parth Nobel,
  https://web.stanford.edu/class/ee364a/lectures/approx.pdf.
  Read slides6.19-6.23, especially6.22's stochastic least-squares expansion.
  Mean-zero matrix noise becoming a quadratic regularizer is a direct
  ancestor of balanced_edits.md. The latter bounds the expectation of
  the reoptimized value, not just the optimum of the expected objective.

Rubbens et al.'s2023 interpolation overview and Bousselmi et al.'s2025
convex-interpolation extension were search/abstract leads only. Juba's
AAAI2019 NSF-hosted PDF also returned502; its abstract is read, but no
theorem proof is claimed from that failed access.

Later successful access and follow-up reads:

- Juba, arXiv1806.11204v1 (2018; AAAI2019 version may renumber),
  https://arxiv.org/pdf/1806.11204. Read abstract, introduction/related work,
  partial-example weakness discussion, Definitions5-7, the associated
  construction, Theorem9 and its complete displayed proof, and future work.
  This is a close ancestor for using fallible/partially observed information
  in bounded reasoning. Its bounded-degree SOS and sample assumptions are
  not replaced by the affine adapter. The earlier access failures remain.
- Juba and Michael, draft book dated August6,2026,
  https://www.cse.wustl.edu/~bjuba/lrbook/L_R_Book-ch10.pdf.
  Read Chapter10 introduction, Section10.1 Definitions10.1-10.5 and examples;
  displayed excerpts of Theorems10.16/10.17 and Section10.4. Full algorithms
  and proofs were not read/imported. Chapter11 access returned502. This is
  a scope screen against claiming generic provisional reasoning as new.
- Acharya, Jafarpour and Orlitsky, *Expected Query Complexity of Symmetric
  Boolean Functions* (Allerton2011),
  https://people.csail.mit.edu/jayadev/papers/exp_qry_cmp.pdf.
  Read abstract, SectionsI-IV, Theorem1 proof and complete Theorem2 proof.
  Optimal threshold evaluation is established; invoice-only output is the
  additional interface in majority_stopping.md. Later sections were only
  displayed incidentally, not imported.
- Wu, *Entropy of Bernoulli Measures Conditioned on Affine Subspaces and
  a Problem of Ancheta-Massey*, arXiv2608.22837v1 (August2026),
  https://arxiv.org/pdf/2608.22837. Read introduction, Theorem1 and proof,
  Lemma1 and its proof through Lemmas2-4. The proof's key chain is completed
  on page8. Section4 was displayed but is not independently reconstructed.
  Import Lemma1 in biased_affine_invoice.md. The fair linear-lossy bound is
  attributed there to Ancheta1978; that older paper has not been read directly.
  Nonlinear nearest-codeword encoding must be distinguished from a linear
  encoder, even when the reconstruction code itself is linear.
- Ferguson, *Optimal Stopping and Applications*, Chapter2,
  https://www.math.ucla.edu/~tom/Stopping/sr2.pdf. Read the opening finite-
  horizon backward recursion, equation(1), and its explanation on page2.1.
  This is the ordinary Bellman ancestor of stopped_summary.md. The displayed
  secretary examples were not imported. Dinkelbach1967's publisher abstract
  and metadata were read at https://doi.org/10.1287/mnsc.13.7.492; the PDF
  link redirected to the abstract. No full-paper read is claimed. The finite
  ratio update is reconstructed directly in stopped_summary.md.
- Hamming1950, *Error Detecting and Error Correcting Codes*,
  https://doi.org/10.1002/j.1538-7305.1950.tb00463.x. Read publisher metadata.
  The Yale PDF timed out twice and the NPS copy returned403/inaccessible.
  The elementary perfect-code construction is reconstructed explicitly in
  perfect_code_invoice.md and attributed to the established code family;
  no full-text read is claimed.
- Garatti, Care and Campi, *Complexity Is an Effective Observable to Tune
  Early Stopping in Scenario Optimization*, IEEE TAC68(2),2023,
  https://marco-campi.unibs.it/pdf-pszip/2023-TAC-tune%20N%20.pdf.
  Read abstract/introduction, SectionII assumptions/definitions and
  Algorithm1, and the displayed Theorem1 conclusion. Full theorem proof
  was not read/imported. Adaptive sample size based on retained complexity
  is established; convex/nondegenerate scenario assumptions are substantive.
- Bazinet, Zantedeschi and Germain, *Sample Compression Unleashed*,
  https://arxiv.org/pdf/2409.17932, v3March2025. Abstract/introduction only.
  This is a comparison lead for compression with general losses; no theorem
  imported. The search aggregator's reference to anytime results is not
  treated as a statement proved by this paper.
- Howard, Ramdas, McAuliffe and Sekhon, *Time-uniform Chernoff bounds via
  nonnegative supermartingales*, https://arxiv.org/pdf/1808.03204,
  displayed v8December2025. Read abstract, Lemma1 (Ville) and its complete
  Section6.1 proof, plus the displayed Section4.6 SPRT connection. The
  classical maximal inequality is imported in fingerprint_learning.md.
  The paper's broader martingale results are not reconstructed or imported.
- Halko, Martinsson and Tropp, *Finding Structure with Randomness*,
  https://arxiv.org/pdf/0909.4061, v2December2010. Read Sections4.3-4.4,
  Lemma4.1 statement and Algorithm4.2. Random probes, incremental range
  construction and residual-based stopping are strong ordinary ancestors.
  Their Gaussian operator-norm theorem is not a finite-field risk theorem.
- Makarov and Seelmann, *Metric Properties of the Set of Orthogonal
  Projections and Their Applications to Operator Perturbation Theory*,
  https://arxiv.org/pdf/1007.1575. Read introduction and Section2, including
  projection representation(2.1), Lemma2.1, Corollary2.2 and its proof.
  Graph-subspace geometry is established. No claim that the later scalar
  receipt envelopes are absent from the full operator literature follows
  from this limited screen. A separate Tamkang graph-gap article returned502.
- Kulkarni and Ramesh, *A Formula for Gap Between Two Closed Operators*,
  Linear Algebra and its Applications432(2010),3012-3017,
  https://iitpkd.ac.in/sites/default/files/2020-02/LAA1Gap.pdf. Read the
  introduction, bounded-operator formula attributed to Nakamoto, preliminaries
  and Theorem3.1 projection representation. The unbounded extension's full
  proof was not read. It confirms graph-gap geometry as an established
  comparison. A requested page screenshot timed out.
- Sayed, *A Framework for State-Space Estimation with Uncertain Models*,
  IEEE TAC46(7),2001,
  https://asl.epfl.ch/wp-content/uploads/publications/journal_articles/tac_jul_2001.pdf.
  Read abstract, introduction and SectionII's surrounding discussion through
  Theorem1 and SectionII-A opening. Extracted equations were largely missing;
  two screenshot requests timed out. Therefore no formula or theorem is
  imported from this read. Its min-max regularized-estimation duty is a
  close general ancestor; it differs from bounding the reoptimized value
  across models consistent with only scalar receipts.

Two fresh requests for El Ghaoui/Lebret's Berkeley rob-ls.pdf returned tool
access errors. The search excerpt and publisher metadata were available;
they do not establish a new full-text read. Broad searches of sharp ridge-
value perturbation and graph-gap bounds did not settle the novelty question.
- Yang, Hanneke and Carbonell, *Bayesian Active Learning Using Arbitrary
  Binary Valued Queries*,
  https://www.cs.cmu.edu/~./jgc/publication/Bayesian%20Active%20Learning.pdf.
  Read Section2's query/code equivalence and Definitions1-5, Theorem1,
  and the complete Huffman upper-bound proof in Section4. The lower proof
  was only partially displayed, not reconstructed. Arbitrary binary queries
  make lossy coding directly available; our paid coordinate-read/private-
  reset interface does not supply such arbitrary queries at unit price.
- Makhdoumi, Huang, Medard and Polyanskiy, *On Locally Decodable Source
  Coding*, https://arxiv.org/pdf/1308.5239, v2August2013. Read abstract,
  introduction and related-work definitions; no converse proof imported.
  Also read Makhdoumi's2013 thesis Section2.2 opening definition at
  https://people.lids.mit.edu/yp/homepage/data/theses/2013_MS_Makhdoumi.pdf.
  Its local encoding bounds each SOURCE coordinate's number of affected
  output symbols, whereas local decoding bounds access to compressed data.
  Neither equals our adaptive episode's bounded source-query depth. The
  referenced Montanari/Mossel smooth-compression paper remains a lead.

- Garatti and Campi, *Non-convex scenario optimization*, online2024,
  issue2025, https://marco-campi.unibs.it/pdf-pszip/2023-Nonconvex-MP.pdf.
  Read introduction, equations(5)-(6), Section2 Property1, Definitions2-3,
  Theorems3-4 and Section2.1 discussion. Theorem4 is explicitly imported;
  its Section5.2 proof has not been reconstructed. No nondegeneracy or
  convexity assumption is needed in this theorem. scenario_baseline.md
  checks the map to span learning and the closer numerical comparator.
- Balcan, Blum, Fragkia, Li and Sharma, *Verify to Amplify: Improving
  Reasoning via Learned Chain-of-Thought Verification*,
  https://arxiv.org/pdf/2603.03538, v5September9,2026. An older search title
  referred to online learnability; use the title actually displayed in v5.
  Read abstract/introduction, Section2.1 setup and Remark2.1, Section2.3
  Definitions2.9-2.12 and Remark2.11. No theorem proof imported. Feedback
  supplies the true first erroneous step after predictions, with a
  realizable verifier and a separate generator-progress premise. These are
  substantive resources, not free verification of unresolved mathematics.
  The OpenReview endpoint was inaccessible; the arXiv PDF was readable.

Fresh query-driven-PAC Juba PDF access returned502; no full-text read.
A wait-and-judge repository page supplied metadata, then failed to open;
it does not replace the directly read scenario source above.

- Epperly, Govindarajan and Chandrasekaran, *Minimal Rank Completions for
  Overlapping Blocks*, https://arxiv.org/pdf/2106.11267,2021. Read the
  introduction/field convention, Section2 Proposition2, Construction1,
  Theorem4 statement and its attainment proof; the complete-solution
  converse was only partially displayed. Their warm-up explicitly
  attributes block completion to earlier Kaashoek/Woerdeman work.
  joint_receipts.md uses elementary block elimination over F2, not a
  claim to a new completion theorem. The DOI endpoint failed, arXiv worked.
- Javanmardi, Sale, Hofman and Hullermeier, *Conformal Prediction with
  Partially Labeled Data*, PMLR204,2023,
  https://proceedings.mlr.press/v204/javanmardi23a/javanmardi23a.pdf.
  Read Section2.2 and Section3, Theorems1-3 with their displayed proofs.
  Pessimistic latent-score domination with truthful candidate labels is
  already an explicit guarantee-preserving device. Their fixed trained
  predictor/calibration split and marginal prediction-set coverage differ
  from our jointly learned equation scope and latent-rank certificate.
  Theorem1 is a particularly close antecedent for the containment argument;
  no new general incomplete-data validity principle is claimed here.
- Garatti and Campi, *On Conditional Risk Assessments in Scenario
  Optimization*, SIAM J. Optimization33(2),2023,
  https://marco-campi.unibs.it/pdf-pszip/2023-SIOPT.pdf. Read introduction,
  Assumptions1.1/1.4, Definitions1.2/1.3, Example1.5 and Remark1.6, plus
  the opening Bayesian setup. The example and distinction between a
  distribution-free confidence procedure and conditional risk are directly
  relevant; no later Bayesian theorem imported. The publisher supplied
  abstract only, followed by a readable author manuscript.
- Campi, *Inductive knowledge under dominance*, Synthese201:184,2023,
  https://marco-campi.unibs.it/pdf-pszip/2023-Synthese.pdf. Read abstract,
  opening introduction, Definitions1-2, Proposition1 statement, Remark2,
  and Section3 opening through the explanation of complexity-based model
  rejection. No proposition proof imported. Conventional scenario theory
  already explicitly concerns useful idealized models, surrogative
  reasoning and fallible domain knowledge; those concerns do not separate
  this project from ordinary methods.

- Cousot and Cousot,1977 POPL abstract-interpretation paper: read the
  authors' detailed summary at
  https://cs.nyu.edu/~pcousot/COUSOTpapers/POPL77.shtml; no new full-paper
  proof read in this final screen. It directly describes using sound partial
  execution information to settle selected questions. Karr1976 affine-
  relationship analysis is a close lead; the Texas PDF returned404 and
  the indexed excerpt is not counted as a full-text read. The affine
  pullback in counterfactual_rules.md is elementary and claimed as an
  adapter, not a new abstract-interpretation algorithm.
