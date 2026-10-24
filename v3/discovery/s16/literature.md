# s16 primary-source comparisons

Codex (GPT-6), October 23, 2026. DEVELOPMENT. Record read scopes and limits.

## Essential variables and ridge correction

- Carlini, [Reducing the number of variables of a polynomial](https://arxiv.org/pdf/math/0507531),
  v1 July26,2005. Read abstract/introduction, remarks1–2, first catalecticant
  definition/Lemma2 and section4 Proposition1 proof. The derivative-annihilator
  characterization and minimal essential dimension directly precede our
  scalar correction reduction. The source works in characteristic zero;
  its positive-characteristic remark calls for different tools. Generic
  novelty of derivative-based variable reduction is rejected.
- Constantine, Eftekhari, Hokanson and Ward,
  [A near-stationary subspace for ridge approximation](https://arxiv.org/pdf/1606.01929),
  v2. Read abstract/introduction, section3 Assumption1, Theorems1–2 and
  AppendixA proof of Theorem1. Null gradient-covariance directions already
  characterize invariant directions. The Poincare error theorem is a
  distributional approximation bound, distinct from our uniform exact
  polynomial premise. The later near-stationarity proof and numerical
  experiments were not reconstructed or imported.
- Bhargava, Saraf and Volkovich,
  [Linear Independence, Alternants and Applications](https://eccc.weizmann.ac.il/report/2023/032/download/),
  read abstract and introduction opening. A search snippet mentioned a
  variable-reduction subsection, but the returned35-page version's text
  lookup did not locate it. Treat that specific subsection as an unresolved
  lead, not as a read proof. No algorithmic complexity claim is imported.

## Randomized proof purchase

- Csillag, Struchiner and Goedert, [Prediction-Powered E-Values](https://arxiv.org/pdf/2502.04294),
  v2 May26,2025. Read abstract/introduction, section2.1 construction,
  Theorems2.1–2.2 statements, Algorithm1 and confidence-set construction.
  Their prediction/correction factor specializes exactly to our linear
  loss factor. Their propensity floor is the same nonnegativity constraint
  after substitution. Updating future predictors and sampling rules is
  already covered. Generic novelty of the randomized-proof statistical
  mechanism is rejected. We independently gave the short conditional-mean
  proof for our special case; the source's general e-process proof and
  power theorem were not reconstructed or imported. The unresolved adapter
  concerns sound partial proofs and arbitrary completion order, with its
  own costs; it is not a new e-value principle.
- Zrnic and Candes, [Active Statistical Inference](https://arxiv.org/pdf/2403.03208),
  v3 April7,2026; first version2024. Read abstract/problem setting,
  mean-estimator equations1–2, oracle sampling objective and section7
  discussion of stabilizing fallible uncertainty scores. The estimator and
  variance expression directly precede our constant-propensity economic
  calculation. Adaptive acquisition itself is established. We did not
  reconstruct their asymptotic theorem or reproduce their experiments.
  The initial OpenReview PDF request returned a browser challenge; the
  arXiv copy supplied the actual source read.
- Brawand et al., [Active Multiple-Prediction-Powered Inference](https://arxiv.org/pdf/2605.08429v1),
  May8,2026. Read abstract, introduction/related work and the beginning of
  section3.1's model-subset setup. This is a close lead for priced multiple
  predictors. No optimization guarantee or empirical claim is imported;
  its global optimization statements require separate inspection if used.

## Constraint certificates and counterfactual bounds

- Harrison, [Verifying nonlinear real formulas via sums of squares](https://www.cl.cam.ac.uk/~jrh13/papers/sos.pdf),
  TPHOLs2007. Read abstract, sections1–2, the rational quadratic-form
  construction in section3, matrix interpretation in section4 and the
  Nullstellensatz/Positivstellensatz statements opening section5. Finding
  certificates numerically and checking them by elementary formal steps
  is established. Our bounded verifier must be compared with this actual
  symbolic-verification tradition, not an ordinary method forced to solve
  every task from scratch. Later implementation details were not audited.
- Li, Mordukhovich, Nghia and Pham,
  [Error Bounds for Parametric Polynomial Systems with Applications to Higher-Order Stability Analysis and Convergence Rates](https://arxiv.org/pdf/1509.03742),
  retrieved v1 with a2018 title-page date. Read abstract, Proposition3.1,
  marginal-qualification definition3.4, and Theorem4.2 statement with its
  compact-set extension. Holder error bounds and sensitivity of polynomial
  systems are established. Their local distance bounds have qualification
  and boundedness hypotheses; our elementary retained-identity substitution
  is not a replacement for their theorem. We did not reconstruct their
  subgradient proof or import their degree-dependent exponent.
- Parrilo, [Semidefinite programming relaxations for semialgebraic problems](https://doi.org/10.1007/s10107-003-0387-5),
  2003. Read the primary publisher abstract only. Bounded-degree
  Positivstellensatz search by semidefinite programming is direct prior
  machinery. Full algorithm and complexity claims remain unread here.

## Two-moment regularized-value transport

- El Ghaoui and Lebret,
  [Robust Solutions to Least-Squares Problems with Uncertain Data](https://people.eecs.berkeley.edu/~elghaoui/Pubs/rob-ls.pdf),
  SIAM J. Matrix Anal. Appl.18(4),1997. Read abstract/introduction,
  the unstructured min-max contract, Theorem3.1 and its rank-one
  perturbation proof, and Remark3.2's matrix-only edit case. The triangle
  envelope and aligned worst edit used in our rescaled-primal calculation
  are established robust least-squares machinery. Their displayed problem
  retains the full nominal matrix and chooses one robust action; ours asks
  for extrema of the reoptimized value over all source matrices consistent
  with two scalar receipts. This distinction identifies the comparison
  duty, but does not establish novelty. We did not reconstruct the later
  structured/rational-uncertainty results or reproduce their experiments.
  The alternate lowercase pdffiles URL was inaccessible; the author's
  Pubs copy was read successfully.

The short search did not locate an exact two-receipt theorem. That is an
unresolved literature question, not evidence of absence. Strong ordinary
controls include full-matrix robust least squares whenever that matrix is
retained and paid; do not artificially remove it from their information.

Repository-lineage correction: s14/second_receipt.md and
s14/two_scalar_upper.md already contain the exact lower and upper results
reconstructed in s16/two_moments.md; s14/partial_two_scalar.md already gives
the constant-size partial-receipt conic reduction. Read those derivations
at this correction. The new angle form and alternative witness are not a
new sharp-envelope contribution or independent confirmation. Preserve the
cross-target acquisition and explicit rational-checker deltas separately.

## Faulty models and self-correction

- Gemmell and Sudan,
  [Highly Resilient Correctors for Polynomials](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1992/Archive/CSD-92-661.pdf),
  1992 Berkeley report. Read abstract, introduction, definitions2.1–2.3
  and the section3 problem statement. Correcting a fallible polynomial
  computation through algebra and coding is established. Their premise
  concerns a program correct on a sufficient fraction of a finite domain;
  the program itself need not be a low-degree polynomial. Our registry
  test instead assumes bounded-degree residuals and pays exact truth
  access to validate a global fault budget. These are different contracts;
  the distinction alone proves neither novelty nor superiority. The
  randomized reduction and decoding proof were not reconstructed here.
- Blum, Luby and Rubinfeld,
  [Self-Testing/Correcting with Applications to Numerical Problems](https://people.csail.mit.edu/ronitt/papers/selftestcorrect.pdf).
  Read abstract/introduction and the opening self-testing/correcting
  definitions. Ordinary methods already address using fast fallible
  programs with simpler checks and corrections, including numerical
  functions. A narrative that conventional methods simply distrust or
  discard such models is false. The full algorithms and their quantitative
  guarantees are not imported from this initial comparison.

The generic claim that error correction makes several faulty computations
useful is rejected as novelty. The registry-level common-event interface
remains a possible adaptation only if a natural priced duty warrants it.

## Finite-scale moment acquisition

- Sharma, Devi, Kapoor, Ram and Barnett,
  [A brief note on some bounds connecting lower order moments for random variables defined on a finite interval](https://www.researchtrend.net/ijtas/tas12/20%20R%20SHARMA.pdf),
  2009. Read introduction, notation and Theorem1 statement. Its third-moment
  bounds specialize to the two inequalities applied to our normalized
  transformed measure. Those moment inequalities are prior machinery;
  the source states strict versions for at least three support values,
  while our matching two-point measures attain closure endpoints. We gave
  the short weighted Cauchy proof and did not rely on the source's later
  central-moment corollaries. PDF text extraction of formulas is imperfect;
  no stronger claim is imported from that extraction.
- Alahmadi, Pranic and Reichel,
  [Rational Gauss quadrature rules for the approximation of matrix functionals involving Stieltjes functions](https://www.math.kent.edu/~reichel/publications/stieltjes.pdf).
  Read abstract, Theorem3's rational Gauss-Radau remainder statement and
  the following bracketing discussion. Bounding quadratic matrix
  functionals by rational quadrature is established; derivative signs,
  spectral endpoint information and quadrature access matter. The full
  construction and proof dependencies were not reconstructed, and no
  complexity or exact two-value formula is imported. Rational interpolation
  remains a close comparison for the new finite-scale acquisition adapter.
# Additional comparison for the matrix-receipt route

* El Ghaoui and Lebret, [Robust Solutions to Least-Squares Problems with
  Uncertain Data](https://people.eecs.berkeley.edu/~elghaoui/Pubs/rob-ls.pdf),
  1997: extended the prior read to section3.3, equations19–20 and Theorem3.3.
  A scalar search after spectral decomposition is already established.
  Consequently neither rank-one worst edits nor reduction to one scalar
  search is the proposed delta. Our candidate concerns sharp revised-value
  ranges when only a compressed OLD inverse response is available.
* Becker, Kawas, Petrik and Ramamurthy,
  [Robust Partially-Compressed Least-Squares](https://arxiv.org/pdf/1510.04905),
  PDF title date September5,2018, arXiv identifier first posted2015: read
  abstract, introduction, section2 through Lemma1/Theorem1 and section3's
  scalar-search reduction. They robustify a sketched quadratic term while
  retaining an unsketched linear term. Robust compression and resource-aware
  ordinary methods are therefore direct prior concepts. This differs from
  conditioning all unknown source matrices on a retained inverse-response
  compression. Appendix algorithm proof and empirical results were not
  audited; no claimed speedup is imported into our service.
* Hansen and Pedersen, [Jensen's Operator Inequality](https://arxiv.org/pdf/math/0204049),
  2002 preprint: read introduction, Theorem2.1/Corollary2.3, and the displayed
  compression argument in its proof. Operator convexity, scalar convexity and
  their compression hypotheses must be distinguished. Our displayed Jensen
  comparisons need only a scalar spectral measure; they do not license the
  previously rejected pointwise edited-resolvent bound. General compression
  and dilation techniques are prior machinery.

This screen does not establish absence of an exact previous formulation.
The candidate delta is the specific information-conditioned sharp interval
and cheap receipt witnesses, with matching-source construction. Its useful
retention regime and closest complete ordinary comparison are still open.

## Joint unfinished-proof/ensemble screen

* Balsubramani and Freund,
  [Optimally Combining Classifiers Using Unlabeled Data](https://proceedings.mlr.press/v40/Balsubramani15.pdf),
  COLT2015: read setting, prediction game, Theorem2 statement and AppendixA
  Lemmas7–8 duality/clipped-prediction derivation. Unknown labels constrained
  by ensemble information and convex minimax aggregation are established.
  This rejects generic novelty for exploiting unresolved disagreements.
  Their transductive prediction game is a strong control, while our proposed
  contract retains anytime proof refinements and explicit program costs.
* The same authors,
  [PAC-Bayes with Minimax for Confidence-Rated Transduction](https://arxiv.org/pdf/1501.03838),
  2015: read abstract, introduction, setting and section4 Lemma3/Theorem4
  with the discussion separating PAC-Bayes from minimax aggregation.
  Combining those two frameworks is already prior work. The abstention
  extension was seen at its setup only; its detailed theorem/proof was
  not audited or imported. Future iid risk and a fixed unlabeled test set
  are different duties, not grounds for a superiority claim.
* Lacasse et al., [PAC-Bayes Bounds for the Risk of the Majority Vote and
  the Variance of the Gibbs Classifier](https://papers.neurips.cc/paper_files/paper/2006/file/779efbd24d5a7e37ce8dc93e7c04d572-Paper.pdf),
  2006: inspected Theorems1/6 statements and the section5 semi-supervised
  disagreement discussion. Label-free ensemble disagreement and preserving
  joint confidence information are old ideas. The paper also distinguishes
  Gibbs and majority-vote risk, which our delivery contract must preserve.
  No empirical improvement or finite-sample formula from that paper is
  substituted for the inherited anytime event.

Disposition: generic joint-ensemble novelty REJECTED. A useful bounded-
program/partial-proof/cost-selection adapter remains possible but unassessed.
Do not spend a large harness on the constructed18.18-versus1 illustration
before identifying a naturally paid evidence regime and these controls.

## Loss-range audit comparison

* Beygelzimer, Dasgupta and Langford,
  [Importance Weighted Active Learning](https://icml.cc/Conferences/2009/papers/392.pdf),
  ICML2009: read introduction, section4 loss-weighting/Algorithm2 and
  Theorem2's statement. They set query probability using the maximum
  loss difference across remaining hypotheses and labels, with a theorem
  that does not require a positive uniform query floor. Our range is
  instead across feasible labels for ONE policy's bounded unbiased score.
  Loss-sensitive querying and safe zero-query cases are not new generic
  capabilities. The paper's full label-complexity proof was not re-audited.
* Ashouritaklimi et al.,
  [Prediction-Powered Active Testing](https://arxiv.org/pdf/2607.08347),
  July9,2026 v1: read abstract, finite-pool setting and main-text
  Propositions3.1–3.3, with the formal E.11 oracle statement. Control-variate
  risk estimation and residual-sensitive acquisition are direct controls.
  Its loss-aware oracle uses unknown true losses and its implementable
  surrogate differs; no oracle price is treated as available evidence.
  Asymptotic coverage and experimental gains are not imported into our
  anytime proof-restricted construction. The61-page appendix was not audited.
* Contextual Active Model Selection, OpenReview id ZizwgYErtQ: PDF access
  returned a browser challenge. Search text is only a lead; no theorem
  from that source is counted as read or used.

The exact one-query bounded-score lower bound in range_audit.md remains
an elementary same-model derivation. Its natural interpretation is maximal
coupling of Bernoulli laws, not a new general active-learning algorithm.

## Retrospective decision comparison

* Chanialidis, Evers, Neocleous and Nobile,
  [Retrospective sampling in MCMC with an application to COM-Poisson
  regression](https://eprints.whiterose.ac.uk/id/eprint/100012/1/cmpstat.pdf),
  Stat2014: read accepted-version abstract and section3 equations5–6 with
  the three-way accept/refine/reject procedure. This is direct prior art
  for the interval acceptance mechanism. Both current and proposed target
  values can remain bounded rather than exact. Application-specific
  normalizer bounds, later experiments and their cost gains were not audited.
  Web retrieval exceeded its size limit; Python/fitz read the same publisher-
  repository PDF in memory, SHA256
  f92b049eea0b7e995e5f3823f07e2fd7fb08a3525a93c839d8cabdceda3cdd9b.
* Bardenet and Titsias, [Inference for determinantal point processes without
  spectral knowledge](https://mtitsias.github.io/files/dppnips.pdf), NIPS2015:
  read abstract/introduction and section3.2 on exact MCMC using progressively
  refined likelihood bounds. Cheap non-spectral evidence feeding exact
  retrospective decisions is already a demonstrated application pattern.
  We do not import its displayed likelihood formulas or claim our inverse-
  response receipt covers determinant terms. The author-hosted PDF was
  read with Python/fitz after web access failed; SHA256
  191ba204e0a75f569ac9660a96ce27012e339fc4fab64a1b90b5c2a2ea51b429.

The Glasgow landing page initially timed out; a later search retrieved its
abstract. The large thesis PDF was not read. These access outcomes do not
count as mathematical failures or independent confirmation. Generic exact
acceptance novelty is REJECTED; the possible adapter is a new paid source
of sharp bounds, if it proves useful in a real compatible objective.

## Structured changes and sampled model correction

* El Ghaoui/Lebret, previously cited: additional read of section4,
  Theorems4.1–4.2, structured Euclidean uncertainty and scalar/SDP
  formulations. Structure-aware robust least squares is established.
  These results have the original data, not just our old compression.
* Becker and Clancy, [Robust Least Squares for Quantized Data Matrices](https://arxiv.org/pdf/2003.12004),
  2020: read abstract, section2.1 Theorem1 and proof, Corollary1 and
  section2.3's regularized objective. Entrywise uncertainty has an explicit
  separable worst residual; quantization-aware robust regression is prior.
  This differs from interval uncertainty on a retained inverse-response
  matrix. Experiments and their gains were not audited or imported.
* Contino et al., [Weighted Procrustes problems](https://doi.org/10.1016/j.jmaa.2016.07.050),
  2017: primary search extraction supplied Definition3, Theorem2.6 and
  Proposition3.1. The shorted operator is the existing positive-operator
  lower envelope for weighted least squares. Full DOI opening failed and
  the repository PDF was restricted, so no full-paper read is claimed.
* Drmac and Gugercin, [A New Selection Operator for DEIM](https://arxiv.org/pdf/1505.00370),
  v2 October2015: read introduction/DEIM interface, Theorem2.1 statement,
  max-volume argument and remarks on construction cost. Sampling selected
  coordinates, basis-invariant selection and conditioning-controlled error
  are direct prior art. Maximum volume existence is not a free algorithm.
* Drmac and Saibaba, [DEIM: Canonical Structure and Weighted Inner Products](https://arxiv.org/pdf/1704.06606),
  v4 February2018: read sections1.1–1.2, Lemma2.1 and section3.1 setup.
  Oversampling, generalized measurements and background-model assimilation
  are already part of this literature. Weighted-space later proofs were
  not audited. PBDW is a close next primary-source comparison, not merely
  an unrelated application keyword.
* Sorensen and Embree, [A DEIM Induced CUR Factorization](https://arxiv.org/pdf/1407.5516),
  arXiv v2 September2015 (PDF title page June2018): read introduction,
  Lemma4.1 and Theorem4.1 proof with the approximate-SVD extension.
  Error-controlled interpolation and row/column reuse are prior. Our
  exact model-correction identity is its zero-residual specialization;
  any possible delta lies in validation, adaptive lifetime scope or a
  demonstrably useful paid service, not that identity alone.

* Binev, Cohen, Dahmen, DeVore, Petrova and Wojtaszczyk,
  [Data Assimilation in Reduced Modeling](https://people.tamu.edu/~gpetrova/BCDDPWdata_submit.pdf),
  June2015 manuscript: read introduction, Theorem2.8 and proof, and
  remarks2.9–2.12. Optimal recovery from a subspace-error tube and exact
  observations is prior; the fiber's radius can improve on a global bound.
  Multi-space intersections are described in the abstract, but their later
  algorithms were not audited here. Generic approximate-correction novelty
  is rejected.
* Smetana, Zahm and Patera, [Randomized Residual-Based Error Estimators](https://arxiv.org/pdf/1807.10489),
  v2 December2018: read introduction, Corollaries2.2/2.5, section2.3 and
  Remark2.7. High-probability many-query residual certification and its
  adaptive dependence problem are direct prior art. Their displayed scope
  is a finite parameter set; our polynomial-identity/SOS adapter instead
  has stronger algebraic premises and pays full validation evaluations.
  No superiority follows from that difference. Numerical sample-size
  formulas and empirical results were not imported.
* Barak and Steurer, [Sum-of-squares mathematical definitions](https://www.sumofsquares.org/public/lec01-2_definitions):
  read certificate definition, verification and finding-certificate sections.
  Polynomial identity verification and bit/degree costs are established
  parts of SOS proof systems. Their Boolean-cube completeness statement is
  not applied to our continuous-cube certificate form.

## Favorable matrix errors and regularized total least squares

* Golub, Hansen and O'Leary, [Tikhonov Regularization and Total Least Squares](https://drum.lib.umd.edu/bitstreams/1502d531-6ec5-4fd5-8eb1-779241ecc65e/download),
  1998 technical report / 1999 publication: read section2 Theorem2.1 and
  proof, section2.1 Theorem2.2, and section2.2's negative-regularization
  discussion. Scalar regularization and singular normal equations are
  established machinery. Their joint matrix/right-hand-side perturbation
  objective differs from our bounded matrix-only edit and retained-data
  optimization. Experimental sections were not audited.
* Xia, Wang and Yang, [A fast algorithm for globally solving Tikhonov
  regularized total least squares](https://arxiv.org/pdf/1810.11972),
  v1 October2018: read introduction equations1–5, section2 Theorem3's
  trust-region optimality conditions, Corollary1 and Theorem5 statements.
  Scalar parameterization and trust-region hard cases are direct prior art.
  Their fractional regularized objective is different; later branch-and-bound
  proofs and experiments were not audited. PMC4662500 returned a challenge,
  so its full text is not counted as read.
* Chandrasekaran, Golub, Gu and Sayed, [An Efficient Algorithm for a Bounded
  Errors-in-Variables Model](https://epubs.siam.org/doi/10.1137/S0895479896304678),
  1999: publisher abstract only. The [author-hosted PDF](https://asl.epfl.ch/wp-content/uploads/publications/journal_articles/simax_oct_1999.pdf)
  was retrieved but its text encoding was unreadable, and the screenshot tool
  did not return visible pixels. No theorem read is claimed from that copy.
* Chandrasekaran, Gu, Sayed and Schubert, [The Degenerate Bounded
  Errors-in-Variables Model](https://scg.ece.ucsb.edu/publications/papers/Chandrasekaran_2001_SIAM_DegenerateBoundedErrors.pdf),
  2001: read introduction, section4 proof outline, section5 algorithm,
  section6 rank-one error elimination and section7's degeneracy statement.
  Best-case norm-bounded matrix errors, scalar secular equations and singular
  boundary handling are established. Their unregularized residual/minimum-norm
  formulation differs from the ridge value and optimization over all sources
  consistent with a retained compression. No generic optimizer novelty is claimed.
  The 29-page proof and column-partition extension were not fully audited.

The bibliographic bridge was pages4 and11 of the 2021 optimization-online
[proton-CT algorithms manuscript](https://optimization-online.org/wp-content/uploads/2021/08/8560.pdf),
read in memory with Python/fitz after the web size limit. SHA256
4189c61c02101a9db4ac1854d00928a91c1f335d143e3d023a8fa19aaac1d1d1.
Only its bounded-data-uncertainty paragraph and references42–43 were used;
no medical or application-performance conclusion was imported. An EPFL link
to a 2002 regularized robust-design paper failed. These source-access limits
leave the exact closest-formulation comparison open.

## Decision invariance, derivative information and cheap certificate search

* Dvir, Kopparty, Saraf and Sudan, [Extensions to the Method of
  Multiplicities](https://arxiv.org/pdf/0901.2529): arXiv v2 metadata May2009,
  retrieved title page dated November2024. Read section2.4 Lemma8 and proof,
  Corollary9, and the preceding line-restriction Corollary7. The expected
  zero multiplicity is at most degree/grid-size. Derivative-batch identity
  checks therefore have an established stronger miss bound; the derivative
  acquisition bill is not supplied by that theorem. The author-hosted
  Princeton copy returned403. No Kakeya/extractor claim is imported.
* Adje, Garoche and Magron, [Property-based Polynomial Invariant Generation
  using Sums-of-Squares Optimization](https://arxiv.org/pdf/1503.07025),
  v1 March2015: read introduction, section3.2 setup, section4 equations12–13,
  Proposition1 and proof, and its computational-size discussion. Property-
  directed polynomial certificates are prior. Their forward reachable-set
  invariants differ from our order-preservation target; SOS feasibility and
  coefficient/degree costs remain substantive. Benchmarks were not audited.
* Gupta and Manoj, [An Optimal Algorithm for Certifying Monotone Functions](https://arxiv.org/pdf/2204.01224),
  April2022: read introduction, Definitions1.1–1.2 and Theorems1.3–1.5.
  The O(C(f) log n) result queries the whole Boolean function at chosen
  counterfactual inputs; it is not a bound on revealing unknown bits of one
  input. The exact input-specific shortest certificate can require far more
  queries. Algorithm1's setup was inspected, not its full proof. This is a
  strong relevant control when that function oracle is actually available.
* Ng, Harada and Russell, [Policy invariance under reward transformations](https://ai.stanford.edu/~ang/papers/shaping-icml99.pdf),
  ICML1999: primary indexed abstract only; direct PDF timed out. It identifies
  positive affine/potential transformations for sequential policy invariance.
  This supports treating sequential/expected objectives as a separate duty
  from ordinal pairwise choices, but no unread theorem is imported.

General ordinal-utility search results served as orientation only. The
polynomial-coordinate proof in ordinal_scope.md is explicit; its possible
contribution is the paid verification service, not monotone invariance itself.

## Posterior covariance as a natural value interface

* Attia, Leyffer and Munson, [Robust A-Optimal Experimental Design for
  Bayesian Inverse Problems](https://arxiv.org/pdf/2305.03855), v1 May2023:
  read introduction and section2.1 equation2.3, section2.2's design interface,
  and the beginning of section2.3 through its data-independent covariance
  observation. Robust design under prior/noise misspecification is already
  a direct application area. Their retained forward model and design search
  differ from our summary-only uncertainty question. Later algorithm proofs
  and experiments were not audited; no reported gain is imported.
* Spantini, Cui, Willcox, Tenorio and Marzouk, [Goal-oriented optimal
  approximations of Bayesian linear inverse problems](https://arxiv.org/pdf/1607.01881),
  v2 March2017: read abstract and introduction equations1.1–1.4 with the
  target-covariance/low-rank approximation interface. Avoiding a full
  posterior in favor of a quantity of interest is established. Their
  optimality theorem and later application were not audited at this screen.
* Attia, Alexanderian and Saibaba, [Goal-Oriented Optimal Design of
  Experiments for Large-Scale Bayesian Linear Inverse Problems](https://arxiv.org/abs/1802.06517),
  2018: primary abstract only. It establishes the relevance of targeted
  posterior uncertainty and is a necessary strong comparison; its actual
  algorithms have not yet been compared under our storage/edit contract.

Other robust-design search results are leads, not imported theorems.
The literature already makes task-relative posterior compression ordinary
practice. The possible added claim concerns sharp counterfactual envelopes
after only a small old response block and edit warrant remain.

## Closest perturbation sources for predictor reuse

* Chu, Lin, Tan and Wei, [Condition numbers and perturbation analysis for
  the Tikhonov regularization of discrete ill-posed problems](https://doi.org/10.1002/nla.702),
  online2010, journal2011: author-university metadata/abstract inspected.
  An indexed primary PDF extract exposed Theorem3 and its proof's initial
  normal-equation perturbation identity. Direct CiteSeer access returned403;
  a separate fetch redirected to404. This is an incomplete source screen,
  not a full theorem audit. It makes clear that normal-equation difference
  identities and componentwise regularized perturbation bounds are prior.
* Gulliksson, Wedin and Wei, [Perturbation Identities for Regularized
  Tikhonov Inverses and Weighted Pseudoinverses](https://doi.org/10.1023/A:1022319830134),
  BIT40,513–523,2000: primary indexed abstract only, full access failed.
  General weighted regularization identities are established; no unread
  formula is imported into the new derivation.
* Malyshev, [A Unified Theory of Conditioning for Linear Least Squares and
  Tikhonov Regularization Solutions](https://epubs.siam.org/doi/10.1137/S0895479801389564),
  volume24,1186–1196,2003: publisher abstract and bibliographic information
  read. Exact Frobenius-norm conditioning and close spectral-norm bounds are
  existing subjects. The full perturbation theorem remains unread.

A UCLA CAM89-04 PDF was fetched (27 image-only pages; SHA256
1bd9dddab745beb456445de0a551d0aa639954e011e8cad9a373a2f64df91121), but
text extraction yielded no substantive body. Its indexed right-hand-side
perturbation statement is only a lead. A2004 weighted-filter-matrix abstract
and a2016 structured-condition-number abstract likewise do not establish an
exact comparison. Access failure is not evidence of novelty. The candidate
must distinguish its retained-data/deployment conclusion from generic
perturbation algebra, not claim that algebra as a new mechanism.

## Relative reuse and classical efficiency inequalities

Rao, [Antieigenvalues and antisingularvalues of a matrix and applications
to problems in statistics](https://files.ele-math.com/articles/mia-10-45.pdf),
Mathematical Inequalities & Applications10,471–489,2007: read introduction,
section2.1–2.2 and section2.3's least-squares efficiency formulas, through
equation2.23. Kantorovich bounds already compare ordinary least squares with
an estimator using the correct covariance. Inverse compression and relative
efficiency are therefore direct conventional precedents. Later generalized
inequalities/genetics application were not inspected.

Householder and Bauer's1960 [Some inequalities involving the Euclidean
condition of a matrix](https://doi.org/10.1007/BF01386231) is a bibliographic
lead; the digital-library full-source request timed out. Huang and Zhou's2005
[A direct proof and a generalization for a Kantorovich type inequality](https://doi.org/10.1016/j.laa.2004.10.009)
was available only at primary abstract scope; full ScienceDirect access
returned403. These leads make a generic new-inequality claim inappropriate.
reuse_ratio.md supplies its own short proof and leaves exact formulation
novelty open. A useful application of an old inequality needs an explicit
access/deployment delta, not merely a new name.

## Private checking under adaptive feedback

Naor and Yogev, [Bloom Filters in Adversarial Environments](https://arxiv.org/pdf/1412.8356),
v5 January2019: read introduction, section2 definitions2.1–2.5 and the
adversarial challenge. Their target bounds a fresh adversarial false positive
after adaptive queries, potentially including earlier false positives. Our
first-error union bound is weaker and pays a multiplier for false proposals;
it supplies neither their sustained resilience nor a cryptographic result.
The comparison prevents treating private Boolean feedback as unlimited safe
reuse. Later attack/construction proofs were located but not fully audited.
The rank-bounded public-repair integration, rather than a generic adaptive
checking theorem, is the candidate requiring a useful exact comparison.

## Value queries and probability reconstruction

Marinelli, [On certain representations of pricing functionals](https://discovery.ucl.ac.uk/id/eprint/10189932/1/s10436-024-00438-5.pdf),
Annals of Finance2024: read introduction, Theorem4.3 and its integration
proof, Proposition5.1 and its first proof, and Corollary5.2. The paper directly
distinguishes recovering a measure from extending a value functional to
additional payoffs. Its call/put derivative and convex-payoff formulas are
close prior machinery for hinge_values.md; that note's elementary finite
grid error calculation is not a claim of a new general representation.

Breeden–Litzenberger1978 was checked at author-university bibliographic
scope only; the Stanford full-source request returned403. Boutsikas and
Vaggelatou2002, On the distance between convex-ordered random variables,
was located as an author-uploaded primary preprint, with an indexed
Proposition7 relating stop-loss and Wasserstein distances under a crossing
bound. That statement remains a lead; its full source was not audited or
used as a theorem premise in the finite-grid derivation.

## Approximate error-space growth is a reduced-basis problem

DeVore, Petrova and Wojtaszczyk, [Greedy Algorithms for Reduced Bases in
Banach Spaces](https://arxiv.org/pdf/1204.2290), arXivv1 April2012 (rendered
title page June2018): read Lemma2.1 and its Hadamard/AM–GM proof, Theorem3.2
and its proof, and Corollary3.3's statements. The determinant argument behind
approx_rank.md is direct prior machinery. Its application here is a finite
budget for above-tolerance correction witnesses, not a new greedy convergence
theorem. The paper's later Banach-space results were not audited.
Binev et al.2011 was located at primary abstract scope as the earlier
reduced-basis convergence comparison; its full proof was not reread here.

## Fixed-source robust least squares comparison

Chandrasekaran and Schubert, [Models for Robust Estimation and Identification](https://doi.org/10.1007/978-94-017-3552-0_18),
2002: inspected the author-uploaded text on ResearchGate, introduction and
sections2–5. Norm-bounded min–max and min–min regression, scalar secular
equations, degenerate cases and multi-column uncertainty are established.
The source does not by this reading settle equivalence to the specific
regularized max–min endpoint in fixed_output.md. Its printed formulas have
OCR defects, so no delicate formula is imported. A direct CiteSeer request
returned403. Generic scalar reduction and uncertainty-structure novelty are
rejected; the retained-information/shape contract still needs comparison.

## Fixed catalogues and sequential testing

Waudby-Smith and Ramdas, [Confidence sequences for sampling without replacement](https://proceedings.neurips.cc/paper_files/paper/2020/file/e96c7de8f6390b1e6c71556e4e0a4959-Paper.pdf),
NeurIPS2020: read section1.1, sections2.1–2.3 including Proposition2.1 and
Theorem2.1, and section4. The finite objects are explicitly fixed; only
sampling order is random. Hypergeometric likelihood/prior-posterior testing
is direct prior machinery. The supplementary proof referenced by
Proposition2.1 was not included in this11-page paper and was not audited.

Waudby-Smith, Stark and Ramdas, [RiLACS](https://arxiv.org/pdf/2107.11323),
v2 November2021: read introduction/SHANGRLA reduction and section3 through
the start of3.1, equations2–3. The remaining-population conditional mean
and predictable betting process are direct conventional comparisons.
Later tuning algorithms and experiments were not audited. Catalogue_proofs
adapts these ingredients to delayed aggregate certificates; it claims neither
a new finite-population inference principle nor demonstrated audit savings.

## Joint response contrasts and singular-value budgets

Mirsky, [Symmetric Gauge Functions and Unitarily Invariant Norms](https://doi.org/10.1093/qmath/11.1.50),
1960: publisher bibliographic page inspected; full access failed. Audenaert,
[A generalisation of Mirsky's singular value inequalities](https://arxiv.org/pdf/1410.4941),
v1 October2014: read introduction/Theorem1 and the stated connection to
Mirsky's original inequalities. Its later generalization proof is not used
or claimed audited. Joint_contrasts gives a direct trace proof for its
identity-source special case, so its certificate does not depend on an
unread singular-value theorem. Generic norm-budget coupling is conventional.

## Adaptive sketch reconstruction is a strong existing control

Krishnamurthy and Singh, [On the Power of Adaptivity in Matrix Completion and Approximation](https://arxiv.org/pdf/1407.3619),
arXivv1 July2014, rendered title date2018: read introduction, Algorithm1,
section3.1 and Theorem1. The algorithm already detects new column-space
directions from partial observations, buys an entire independent column,
and reconstructs later columns. Its coordinate-observation/coherence
conditions differ from arbitrary linear queries, so counts cannot be
compared as though the interfaces were equal. Later proof details were not
fully audited here.

Wagner and Zuk, [Low-Rank Matrix Recovery from Row-and-Column Affine Measurements](https://arxiv.org/pdf/1505.06292),
v1 May2015: read introduction, section4.1 Lemmas1–2 and Theorem1, and their
noiseless GRC proofs in section7.1. Rank-preserving row/column measurements
and exact reconstruction are direct prior machinery. Its noisy analysis was
not audited. These comparisons reject generic novelty for the sketch-and-
learn algorithm in sketched_correction.md. A residual/task-specific formal
adapter would still need a useful application and an exact incremental delta.

## Graph receipts and the gap metric

Kulkarni and Ramesh, [A formula for gap between two closed operators](https://doi.org/10.1016/j.laa.2010.01.004),
2010: read the author-uploaded ResearchGate text's introduction (including
Nakamoto's bounded-operator formula), Proposition2.1, Theorem3.1's block
projector, Theorem3.2 and its proof, and Theorem3.5's statement and proof
start. The remainder was not audited; OCR defects limit formula import.
An institutional copy at https://iitpkd.ac.in/sites/default/files/2020-02/LAA1Gap.pdf
was located but not read at this boundary. Nakamoto1995 is only a bibliography
and abstract lead, not a read source.

Horn, Li and Merino, [Distances between the graphs of matrices](https://doi.org/10.1016/0024-3795(94)00185-5),
1996: primary publisher abstract and metadata inspected. It explicitly studies
graph contraction/singular-value formulas and distance inequalities, making
it a close comparison for graph_receipt.md. Full text was not obtained.
The direct finite-dimensional derivation in that note is reconstructable,
but novelty of its sharp scalar modulus is UNASSESSED against this literature.

## Proof-directed catalogue sampling has a stratified-audit ancestor

Ottoboni et al., [SUITE](https://arxiv.org/pdf/1809.04235),
v1 September2018: read the abstract, introduction and section2 through the
start of2.1. Spertus and Stark, [Sweeter than SUITE](https://arxiv.org/pdf/2207.03379),
v3 July2022: read sections3.1–3.7, especially the conditional-factor proof
for predictable stratum selection, and the allocation-rule description at
the start of4.1. Their simulations and numerical claims were not reproduced.
These sources already combine heterogeneous evidence and adapt sampling
while controlling error. Proof_sampling.md therefore rejects generic novelty
for stratified or adaptive sequential testing. Its prospective delta is the
explicit sound-proof constraint and edit-transport interface, still without
a demonstrated economical application.

## Exact structured edits use standard matrix identities

Rasmussen and Williams, [Gaussian Processes for Machine Learning, Appendix A](https://gaussianprocess.org/gpml/chapters/RWA.pdf),
2006: read A.2–A.4, including Gaussian conditioning(A.6), inversion and
determinant lemmas(A.9–A.10), and Cholesky evaluation. These are direct
prior machinery for edit_kernel.md. That note handles a possibly singular
update coefficient through the inverse-free form and writes the precise
joint retained quantities. It makes no generic exact-update novelty claim.
The separate chapter2 request timed out; it was not counted as read.

## Joint response geometry and allocation

Bhatia, Jain and Lim, [On the Bures-Wasserstein distance between positive definite matrices](https://arxiv.org/pdf/1712.01504),
v1 December2017: read section2 Theorem1 and proof, the Procrustes discussion,
and Theorem2 with its block-PSD variational proof. These directly precede
reachable_covariance.md's Gram-factor distance formulation. Its response
substitution and explicit column-rank restriction are adaptations, not new
distance geometry. Later barycentre results were not audited.

Patriksson and Stromberg, [Algorithms for the continuous nonlinear resource allocation problem](https://arxiv.org/pdf/1501.07035),
v1 January2015 with rendered title date2018: read introduction and the
section3 dual-root/breakpoint discussion through3.1, including formula(5).
The common-multiplier algorithm is direct prior machinery. Its reported
large-scale numerical performance is not imported here. The specific signed
ridge-response reduction and sharp alpha<=2 concavity range in
joint_allocation.md remain to be compared more specifically; the generic
allocation algorithm is not a novelty claim. Patriksson's2006 survey was
located and read only at abstract/initial-problem-formulation scope.

## Mistake budgets and equivalence queries are established learning structure

Littlestone, [Learning Quickly When Irrelevant Attributes Abound](https://doi.org/10.1023/A:1022869011914),
1988: after two failed Stanford-copy fetches, read the publisher PDF's
sections3–4: mistake trees, Algorithm2, Theorem3/Lemmas1–2, the VC-dimension
counterexample, and the two equivalence-query transformations. This directly
precedes mistake_checks.md's learner potential and improper-proposal scope.
The later Winnow analysis was not audited.

Angluin, [Queries and Concept Learning](https://homepages.math.uic.edu/~lreyzin/papers/angluin88.pdf),
1988: read query definitions, sections2.1–2.4 including majority queries and
fresh-sampling stochastic equivalence. Generic conversion of counterexamples
to learning, and of samples to approximate equivalence, is not new.

Braverman et al., [Learning from Equivalence Queries, Revisited](https://arxiv.org/pdf/2604.04535),
v2 June2026: read introduction, symmetric-generator definition, random-
counterexample example and Theorem4 statement. It supplies a direct modern
comparison involving proper hypotheses and expected query counts. Its full
proof was not audited, so no numerical constant or complexity guarantee from
that theorem is imported into the present construction. The sealed-batch
adapter still needs a specific comparison to reusable validation literature.

## Adaptive validation and observable execution costs

Dwork, Feldman, Hardt, Pitassi, Reingold and Roth,
[Generalization in Adaptive Data Analysis and Holdout Reuse](https://arxiv.org/pdf/1506.02629),
v2 September2015: read introduction1.1; Theorem9 and its union-bound proof
and adaptive description-length composition; section4.2 SparseValidate,
Theorem27/proof and its discussion. On resumption also read definitions10–11,
Lemma12/proof and Theorem13's bad-event statement (not the later composition
proof). The finite-transcript multiplier in cost_leakage.md is direct prior
machinery. Perfect completeness plus independent public counterexamples
give our ideal-path restriction; statistical tolerance does not automatically
share that property. The paper's differential-privacy proofs were not audited.

Kocher, [Timing Attacks on Implementations of Diffie-Hellman, RSA, DSS, and
Other Systems](https://www.paulkocher.com/doc/TimingAttacks.pdf),1996:
read abstract/introduction, section2's simple exponentiator example, section9
on masking costs and section10's blinding discussion. Secret-dependent cost
disclosure and the difficulty of constant-time implementations are established
prior concerns. No cryptanalytic implementation or new side-channel principle
is claimed. The checker example is an explicit information-contract failure.

## Local response sensitivity and completion

Diao, Wei and Qiao, [Structured Condition Numbers of Structured Tikhonov
Regularization Problem and their Estimations](https://arxiv.org/pdf/1601.02333),
v1 January2016: read introduction, section2.1's definitions/information
inputs, Lemma3 and its derivative proof through equation(3.3) and the
solution perturbation expansion, and section3.2's adjoint formula(3.5),
Proposition2 and proof. This directly precedes task-sensitive derivative
calculations and paid condition estimation. It uses the source/solution
data, while local_contrasts.md optimizes over sources compatible with a
retained response block. That distinction is an information-contract delta,
not proof of literature novelty. No empirical performance numbers imported.

Davis, Kahan and Weinberger, [Norm-Preserving Dilations and Their Applications
to Optimal Error Bounds](https://epubs.siam.org/doi/10.1137/0719029),1982:
publisher abstract inspected; explicit block-completion formulas are the
stated subject. A related Davis ANU proceedings PDF timed out twice, so
its theorem text was not inspected. The Schur-complement completion in
local_contrasts.md is treated as classical machinery; no novelty claim
for completion or ordinary matrix differentiation is made.

## Completion-time selection has direct Monte Carlo ancestors

Murray, Singh and Lee, [Anytime Monte Carlo](https://arxiv.org/pdf/1612.03319),
v3 June2021 (first preprint2016): read introduction, section2's hold-time
assumptions, Proposition1/Corollaries2–3, and section2.1's multiple-chain
construction through Proposition5/Corollaries6–7 and their interpretation.
Appendix proofs and numerical experiments were not audited. The paper's
stationary Markov-chain length bias is distinct from completion_bias.md's
finite parallel-check selection, but directly precedes the general warning
that computation-time selection changes a sampling law. Its multiple-chain
repair is a strong conventional comparison, not a proof of our finite-slot
guarantee or a performance result imported into this repository.

## Nonquadratic geometry is established prior machinery

Hanner, [On the uniform convexity of Lp and lp](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/6920-11512_2007_Article_BF02589410.pdf),
1956: first PDF request timed out, second succeeded. Read Theorem1, its
two inequality proofs and equality discussion; Theorem2 and the final
small-e remark were inspected with imperfect formula extraction, so no
exact modulus constant from them is imported. The p-dependent geometry
and equality mechanisms have long-established precedents. The reuse note
derives its own elementary remainders and does not claim a new norm inequality.

Xu and Roach, [Characteristic inequalities of uniformly convex and uniformly
smooth Banach spaces](https://doi.org/10.1016/0022-247X(91)90144-O),1991,
is a precise comparison lead. DOI access failed and the publisher request
returned403; the full theorem text was not inspected. A secondary synopsis
was not used as a theorem. Exact comparison of the reuse adapter, including
its source-independent ratio and witness, remains open.

## Nesterov: coordinate descent, comparison for pass 58

Primary author manuscript: Y. Nesterov, February 1, 2010, *Efficiency of
coordinate descent methods on huge-scale optimization problems*, CORE
Discussion Paper (later SIAM Journal on Optimization 22(2),2012,341–362,
DOI10.1137/100802001).
[Author manuscript mirror](https://scispace.com/pdf/efficiency-of-coordinate-descent-methods-on-huge-scale-34woq9ez3l.pdf).
Read introduction's arithmetic-cost comparison, section2 definitions and
coordinate sampling/update equations2.2–2.7, Theorem1 proof equation2.13,
and section3 equations3.1–3.3 including Theorem2 and its proof. The
strong-convexity argument and Lipschitz-weighted randomized coordinate descent
rate already supply pass58's optimization machinery. Its special content is
only the quadratic scalar-value interface to the response-envelope witness,
including explicit acquisition and certificate costs. The introduction also
warns against treating full gradients as necessarily much dearer than values
for explicit programs. No claim of a new coordinate-descent method. Later
accelerated-method sections were not used. A LAMSADE PDF search lead returned
no extractable body and was not treated as verified evidence.

## Classical robust least squares: quantify the remaining scope carefully

El Ghaoui and Lebret,1997, [Robust Solutions to Least-Squares Problems with
Uncertain Data](https://people.eecs.berkeley.edu/~elghaoui/Pubs/rob-ls.pdf),
SIAM J. Matrix Anal. Appl.18(4),1035–1064. Read section3.1 Theorem3.1
and proof (unstructured worst residual, rank-one attainment and SOCP),
section3.2 Theorem3.2 and primal-dual proof through Remarks3.1–3.2, plus
section3.3's scalar reduction and Theorem3.3 statement. Structured and
rational-uncertainty appendix proofs were not inspected.
This is direct prior for robust least squares, rank-one perturbation
witnesses, conic formulations and one-dimensional reductions. Those
techniques are not new here. Its selected objective chooses one robust
solution before the uncertainty is realized. The s16 value-envelope target
instead bounds the reoptimized value after an edit, sometimes with only a
retained response block. These are different quantifier/information duties,
not a novelty proof. The fixed-source subproblems deserve particularly
close comparison before any claimed new theorem; generic conic machinery
or a scalar multiplier is insufficient as a contribution.

## Optimal recovery and quadratic-form access: narrow comparison scope

Simon Foucart, [Worst-Case-Optimal Estimation of a Quadratic Form by Quadratic
Functionals of its Linear Observations](https://foucart.github.io/publi/OR_QuadraticQ_v3.pdf),
author manuscript accessed October24,2026: read sections1–2's local/global
information definitions, assumptions, Theorem1 statement and proof through
its projected semidefinite upper formulation. The lower half and later
global/noisy theorems were not reconstructed. This directly precedes
information-fiber optimization and S-lemma endpoint certificates. Its
unknown object has an ellipsoidal model set and a quadratic target; our
unknown matrix has contraction constraints and an inverse quadratic target.
That difference is a comparison duty, not established novelty. The generic
optimal-recovery viewpoint is not new.

Ye and Chang, [Stochastic Diagonal Estimation Based on Matrix Quadratic
Form Oracles](https://arxiv.org/html/2506.15360v1), arXiv2506.15360: read
abstract, introduction1–1.3, equations1.1–1.3 and Proposition1's interface
statement. The page labels v1 June18,2025 but displays an August24,2026
manuscript date; no date inference beyond those displayed fields is made.
The scalar-quadratic versus matrix-vector access distinction and function-
value motivation are established comparison context. Statistical diagonal
estimators and their later sample-complexity proofs were not audited or
used as exact inverse-query lower bounds. Secondary summaries were leads
only. Neither source settles the source-local2*k-1 observation's novelty.
