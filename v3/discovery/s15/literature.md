# s15 primary-source comparisons

Codex (GPT-6), October 23, 2026. DEVELOPMENT.
Record exact read scope, imported versus adapted claims and access failures.

## Opening numerical comparison

- Beck, Drori and Teboulle, [A new semidefinite programming relaxation
  scheme for a class of quadratic matrix problems](https://www.tau.ac.il/~becka/SDP_QMP.pdf),
  Operations Research Letters 40 (2012), 298–302: read introduction,
  formulation (1.1), Example 1.1 and the paragraph describing the main
  constraint-count result (PDF pp. 1–2). Robust least squares with several
  Frobenius uncertainty constraints and specialized rank reduction already
  belong to this literature. This is a close comparison, not an imported
  proof of the scalar-receipt envelope; later proofs were not read.
- Bousselmi, Hendrickx and Glineur's [operator interpolation paper](https://arxiv.org/pdf/2302.08781),
  v3 March 15, 2024: re-read abstract and introductory motivating examples;
  s14 retains the earlier exact theorem-read scope. Its SDP machinery is
  inherited prior art, not a fresh s15 development or independent review.
- Suh et al., [Peppy](https://arxiv.org/abs/2609.35762), September 28, 2026:
  abstract and metadata only. Structured analytic proof discovery with
  symbolic checking is an established contemporary comparator for any
  proposed generic proof-search workflow. No claimed results or code have
  been independently checked here.

Searches for sharp resolvent-value, Tikhonov and graph-gap perturbation
contracts did not identify an exact one-/two-receipt match. That limited
negative search is not evidence of priority. Secondary summaries were
treated only as leads and supplied no mathematical claim.

The follow-up Banach-space screen found Zolezzi,
[Well-Posedness and Conditioning of Optimization Problems](https://www.math.bas.bg/pliska/Pliska-12/Pliska-12-1998-267-280.pdf),
Pliska 12 (1998), 267–280. Only the displayed abstract/opening scope was
read: stability and conditioning of abstract optimization under data
perturbations already have a broad theory. No theorem or condition-number
bound was imported. Searches also returned residual-method stability and
generalized-discrepancy literature; incomplete equation extraction was not
used to claim a close quantitative match. The specific finite-distance,
one-value envelope in norm_transport.md remains a comparison question.

## Costed product and rank certificates

- Dumas, Kaltofen, Lucas and Pernet, [Elimination-based certificates for
  triangular equivalence and rank profiles](https://arxiv.org/pdf/1909.05692),
  v1 September 2019: read introduction and Sections 2.1–2.2, Protocols 1–2,
  Lemma 1 and Theorem 1 with their displayed proofs. Freivalds product
  checks and low-rank factorization verification with matrix-vector costs
  are explicit prior. Section 3's later protocols were not reconstructed.
- Dumas and Kaltofen, [Essentially Optimal Interactive Certificates in
  Linear Algebra](https://arxiv.org/pdf/1401.4567), v4 January 2020: read
  abstract, introduction, and the displayed Section 4.2 rank-upper protocol,
  Lemma 1, Theorem 4 and its main probability argument, plus Corollary 3.
  Black-box rank certificates are strong antecedents. Their field-size and
  interactive assumptions must not be erased when comparing to F2 probes.
- Oseledets and Tyrtyshnikov, [TT-cross approximation for multidimensional
  arrays](https://doi.org/10.1016/j.laa.2009.07.024), 2010: publisher
  abstract only. Exact cross/skeleton recovery is explicitly established.
  The CiteSeer full text returned 403 and the Rome PDF timed out; the
  indexed formula is a lead, not a claimed full-text proof read.

These comparisons reject any new generic product-verification or matrix-
factorization principle. The potential project contribution is the paid
acquisition and common-event model-use adapter, if it proves nonredundant.

- Salmond, Grant, Grivell and Chan, [On the rank of random matrices over
  finite fields](https://arxiv.org/pdf/1404.3250), v2 August 2016: read
  introduction and Lemma 1, equation (4), which explicitly labels the
  uniform full-rank product formula as established. It supplies the exact
  distribution used after the stopping-event reduction; neither that
  product formula nor the general random-rank method is new here.
- Fulman and Goldstein, [Stein's method and the rank distribution of
  random matrices over finite fields](https://arxiv.org/pdf/1211.0504),
  2015: read opening formula (1), Theorem 1.1 and introduction. This is
  further context for the established rank-distribution literature; its
  total-variation results are not needed for this construction.

The limited stopping-rule search did not establish priority. The Calabi–Wilf
implementation page concerned generation of random subspaces of a specified
dimension, not this unknown-rank stopping contract; only that page was read.

## Joint model and target changes

- El Ghaoui and Lebret, [Robust Solutions to Least-Squares Problems with
  Uncertain Data](https://people.eecs.berkeley.edu/~elghaoui/Pubs/rob-ls.pdf),
  SIAM J. Matrix Analysis and Applications18(4),1997: read introduction,
  Sections3.1–3.3, Theorems3.1–3.3 and displayed proofs. Joint matrix/vector
  uncertainty, exact worst-residual formulas, SOCP, and scalar reductions
  after SVD are established. Their stated duty selects a robust decision
  using nominal data; ours bounds reoptimized values over old models sharing
  one receipt. That quantifier/information distinction is a comparison
  obligation, not by itself proof of novelty. Later structured proofs were
  not reconstructed.
- Ito and Takeuchi, [The minimum value function for the Tikhonov
  regularization and its applications](https://arxiv.org/pdf/0910.4351),
  2009: read introduction, Definition1/Lemma1 and Section3's model function,
  equations9–12. Reusing a few value/derivative evaluations through rational
  approximation to select regularization parameters is direct prior art.
  This strengthens the comparison for the inherited rational-receipt route.
  No numerical findings were reproduced and later tests are not new evidence.
  Some extracted inequality signs in the opening proof appear inconsistent;
  no theorem from that extraction is imported without reconstruction.

## Partial failure margins and distributional change

- Chen, Kuhn and Wiesemann, [Data-Driven Chance Constrained Programs over
  Wasserstein Balls](https://optimization-online.org/wp-content/uploads/2018/06/6671-1.pdf),
  version dated May9,2022: read introduction and Sections2.1–2.2,
  Theorems1–3, Lemma1 and the displayed Theorem2/Lemma1/Theorem3 proofs.
  The nearest-failure fractional-transport formula and smallest-margin
  criterion are prior art. Their positive-radius restriction matters;
  Remark1 explicitly rejects the zero-radius equivalence. The finite-case
  adapter reconstructs its pointwise bound and preserves that boundary.
- Yang, Jiang and Lyu, [Contextual Distributionally Robust Chance-Constrained
  Programs](https://arxiv.org/pdf/2609.23739), September20,2026: abstract,
  introduction and formulation(1)–(2) only. Conditional risk adds a
  context-mass constraint and coupled transport duties. No later theorem,
  empirical result or code was reproduced; do not import conditional safety
  into the simpler unconditional margin adapter.
- Reeve, [A short proof of the Dvoretzky–Kiefer–Wolfowitz–Massart
  inequality](https://arxiv.org/pdf/2403.16651), March25,2024: opening iid
  definition, Theorem1, Corollaries1–2 and comparison with Massart were read.
  The adapter uses the conventional conservative two-sided DKW ceiling,
  not the paper's local refinements. Massart's original DOI endpoint was
  inaccessible to the web tool; its author-uploaded abstract and the primary
  Reeve statement corroborate the bound, but the original proof was not read.

## Reusing a private randomized checker

- Dumas and Zucca, [Prover efficient public verification of dense or
  sparse/structured matrix-vector multiplication](https://arxiv.org/pdf/1704.02768),
  displayed version dated September13,2018: read introduction, Section2's
  definitions, Section3's opening comparison and AppendixB.1. The private
  preprocessed fingerprint and linear verification cost are explicitly
  established. AppendixB.1 treats several vectors with one fingerprint.
  Later public-verification cryptographic proofs were not reconstructed.
- Tramer and Boneh, [Slalom: Fast, Verifiable and Private Execution of Neural
  Networks in Trusted Hardware](https://arxiv.org/pdf/1806.03287), v2/ICLR2019:
  read Sections2.1,2.3,3.2, Lemmas2.1/3.1, Theorem3.2 and AppendixB's
  definitions and displayed integrity proof. Secret-state reuse is explicit
  prior. The paper states a number-of-checks union bound. The proposed
  lifetime first-false-claim argument imposes permanent retirement on the
  first rejection. This limited reading does not establish its novelty or
  show an improvement to the full Slalom system. The appendix switches
  conditional/unconditional probability notation; this project retains an
  unconditional failure event and does not import a conditional guarantee.
- Merbaum et al., [Maverick: Private and Verifiable LLM Inference Made
  Practical via Matrix-Vector Multiplication Delegation](https://arxiv.org/pdf/2609.10264),
  v1 September9,2026: read abstract, Section1.1 and the Slalom comparison
  in Section2. Transparent code-based preprocessing is a distinct stronger
  service contract; its later security arguments and empirical claims were
  not reproduced. It warns of leakage from reusable private state, which
  makes rejection handling and the private-observation boundary essential.
- Hofmeister et al., [Secure Private and Adaptive Matrix Multiplication
  Beyond the Singleton Bound](https://arxiv.org/pdf/2108.05742), v2 February2022:
  abstract and opening introduction only. This is a lead for adaptive coded
  verification, not a theorem imported into the local construction.

Disposition: generic private matrix-vector verification is rejected as a
novel mechanism. Keep only a possible explicit lifetime/repair adapter and
its cost question; do not start a large implementation based on this overlap.

## Approximate residual verification and adaptive sketches

- Hardt and Woodruff, [How Robust are Linear Sketches to Adaptive Inputs?](https://arxiv.org/pdf/1211.1056),
  displayed version dated October29,2018: read introduction, the for-each
  versus for-all distinction, the adaptive oracle model and informal
  Theorem1.1/GapNorm definition. This rules out an unrestricted robustness
  claim for ordinary low-dimensional sketches. The local service stops
  on a rejection and exposes no numerical sketch value; it does not solve
  their continuing oracle duty. Later attack proofs were not reconstructed.
- Balabanov and Nouy, [Randomized linear algebra for model reduction,
  PartI](https://arxiv.org/pdf/1803.02602), v4 October31,2019: read abstract,
  introduction, Section4.2, Proposition4.4 and Corollary4.5. Residual-sketch
  error estimation and subspace-based simultaneous guarantees are direct
  prior. Their appendix proofs and numerical experiments were not rerun.
- The same authors, [PartII](https://arxiv.org/pdf/1910.14378), v2 July22,2020:
  read introduction, displayed Proposition5.4 and Section5.2's applications,
  including its adaptive-size paragraph. Independent verification sketches
  and refreshing after a quality-driven update are explicit antecedents.
  No new residual-estimation or generic adaptive-certification principle
  is claimed by the local adapter.
- Shinkar and Singh, [A Simplified Reduction for Error Correcting Matrix
  Multiplication Algorithms](https://drops.dagstuhl.de/storage/00lipics/lipics-vol353-approx-random2025/html/LIPIcs.APPROX-RANDOM.2025.29/LIPIcs.APPROX-RANDOM.2025.29.html),
  RANDOM2025: read abstract, introduction, Lemmas9--10 and their stated
  verification interfaces. Average-to-worst-case correction of fallible
  algorithms is a promising broader lead, already an established research
  area. The new code/reduction proofs were not read and are not imported.

## Self-correction and residual collisions

- Blum, Luby and Rubinfeld, [Self-Testing/Correcting with Applications to
  Numerical Problems](https://people.csail.mit.edu/ronitt/papers/selftestcorrect.pdf),
  JCSS1993: read abstract, introduction, the distinction between result
  checking and correction, and incremental versus total time. The original
  publisher endpoint returned403; the author-hosted PDF was accessible,
  though many mathematical symbols extracted poorly. Later numerical
  application proofs were not reconstructed. The basic goal of using a
  fallible fast program to answer arbitrary inputs is already explicit.
- Rubinfeld and Shapira, [Sublinear Time Algorithms](https://eccc.weizmann.ac.il/report/2011/013/download/),
  ECCC2011/013: read Section4.1, Theorem2, Claims4.1--4.2 and their displayed
  proofs, plus the self-correction paragraph. Collision-to-largest-atom
  reasoning and translated differences with majority decoding are already
  central to the established proof. The local5/8 threshold concerns a
  different, true-source-bound residual collision statistic; this alone
  does not establish a novel correction principle. Calibration calls and
  the source homomorphism warrant are extra premises, not free advantages.
- Rubinfeld, [Robust Functional Equations with Applications to
  Self-Testing/Correcting](https://ecommons.cornell.edu/entities/publication/75a2196c-403c-47b0-a847-2d79deb5ab17),
  Cornell TR94-1435: repository abstract only. Functional-equation methods
  already extend beyond linear/polynomial functions. The scanned PDF had
  no extracted text and its proofs were not read.
- Ar, Blum, Codenotti and Gemmell, [Checking approximate computations over
  the reals](https://iris.cnr.it/handle/20.500.14243/364580),1993: institutional
  abstract only; full text was access-restricted. Approximate arithmetic,
  changed sampling distributions and conditioning are established issues,
  so a real-valued extension must compare with this literature.

Disposition: translated-difference correction and collision concentration
are rejected as new generic ideas. Retain the explicit partial-calibration
adapter and sharp information boundary as developmental consequences;
complete-cost usefulness and nonredundant synthesis remain unresolved.

## Conditional margin transport: closer screen

Yang, Jiang and Lyu, [Contextual Distributionally Robust Chance-Constrained
Programs](https://arxiv.org/pdf/2609.23739), arXiv2609.23739v1,
September20,2026: read Sections2.1--2.2 assumptions/geometry and
Section3.1 Theorems1--2 with their mass-allocation interpretation, beyond
the earlier abstract/introduction read. They already linearize the
conditional probability inequality and couple numerator and denominator
through one transport budget. Their product-space model has additive
context/outcome costs, empirical source atoms and a conditioning-mass
constraint; strict transport slack handles nonattained projections.
The local finite-space two-distance envelope uses an arbitrary fixed
release partition and only a population mass receipt. Its incomplete
calibration adapter and closed scalar branch remain comparison targets,
not evidence that conditional transport itself is new. Appendix proofs,
MIP implementation and reported experiments were not reconstructed.
Reject a generic priority claim for joint conditional optimization.

## Randomized summaries and expectation queries

Kaniewski, Lee and de Wolf, [Query complexity in expectation](https://arxiv.org/pdf/1411.7280),
arXiv1411.7280v1,November26,2014: read abstract/introduction and
Sections3.1--3.2, Definition8, Theorem9 and both proof directions. Their
classical model permits nonnegative real outputs with a prescribed mean;
nonnegative literal degree exactly characterizes its worst-case queries.
The local invoice channel has bounded binary output and a full distribution
depending only on Q(x); for a binary output that distribution is determined
by its mean. Sampling polynomial terms is established, not a new query
principle. Signed Fourier sampling plus a binary offset supplies the local
explicit channel, while the literal cone is a closer route to a stronger
finite control. Quantum and extension-complexity claims are not imported.

Gopalan, Servedio, Tal and Wigderson, [Degree and Sensitivity: tails of two
distributions](https://arxiv.org/pdf/1604.07432), displayed September3,2018
version: read the Section7 Hamming-code construction and its displayed
Fourier transform before Lemma7.4. This explicitly uses the simplex-dual
support at the middle weight; that ingredient is established. Their
indicator/composition construction is not the local quantizer-constant
function class. No general priority conclusion follows from this difference.
Searches for local decoding/private decoding mostly returned privacy of
the requested coordinate or encoding randomness, different protected objects.
Those snippets are leads, not a completed comparison of the present
transcript-privacy contract. The broad sensitivity results are not imported.

## Open proposals and incomplete empirical losses

Catoni, [PAC-Bayesian Supervised Classification](https://arxiv.org/pdf/0712.0248),
2007, Section1.2.4, Theorem1.2.6 and the immediately following Gibbs-posterior
discussion: the exact exponential risk bound and fixed-temperature optimizer
used in open_model_receipts.md are already present. Read also the adjacent
distinction between per-case posterior resampling and one persistent model,
and the Section1.2.8 lead-in's union-budget treatment of temperature choice.
The broader monograph was not reconstructed. Truthful upper-loss substitution
is a monotone adapter, not a new statistical inequality. Partial-label/active-
feedback searches returned leads but were not a completed comparison.

## Randomized program relations

Gulwani and Necula, [Discovering Affine Equalities Using Random
Interpretation](https://people.eecs.berkeley.edu/~necula/Papers/rand_popl03.pdf),
POPL2003: read abstract/introduction, Section2's language/sampling contract,
Section6's polynomial-testing explanation and Section7's nonlinear/basic-
block discussion. Random executions used to infer reusable program relations
are established, including explicit comparison with symbolic expansion.
Their branch blending and equality adjustments are not imported here; the
local source remains a fixed polynomial residual program. The present
rank-stage stop and unresolved-membership interface require their own stated
scope, but do not establish a new general relation-discovery principle.
The Schwartz1980 course-hosted PDF endpoint returned404; its text was not
read. The degree/grid identity-testing bound was read in this primary paper.
# Gaussian availability constants, October 23 continuation

Davidson and Szarek, *Local operator theory, random matrices and Banach
spaces*, author PDF <https://case.edu/artsci/math/szarek/TeX/DavSzaHB.pdf>:
read printed p.42, Theorem II.13 and the proof opening, from a local rendered
page because the web extraction was garbled and the web screenshot tool
returned only a reference. For an n-by-m Gaussian matrix with variance1/n,
m<=n, the upper singular-value tail at1+sqrt(m/n)+t is less than
exp(-n*t*t/2). Rescale and transpose if needed to obtain the constant used
in checker_availability.md. No claim to have reconstructed the full proof.

Laurent and Massart (2000), *Adaptive estimation of a quadratic functional
by model selection*, publisher PDF and CERN record were blocked by access
checks. The Orsay 1998 preprint metadata was accessible. Search snippets
are not counted as reading Lemma1. The elementary chi-square lower-tail
argument is supplied directly in checker_availability.md; the original
lemma remains unread here.

# Anytime partial receipts

Waudby-Smith and Ramdas, *Estimating means of bounded random variables by
betting*, <https://arxiv.org/html/2010.09686v7>: read Section4's capital
process(23), Propositions2--3, Section4.3, and Section4.4 through Theorem3
and its running-intersection statement; also the displayed Ville statement
near Theorem1. Predictable bounded bets and inversion of capital processes
are established machinery. The source explicitly permits dominated processes
in its use of Ville. Our pending-proof lower envelope is therefore a direct
interface adaptation, not a new generic confidence-sequence theorem.

Lindon and Kallus, *Anytime-Valid Inference Under Outcome Delay: A Design-Based
Approach*, <https://arxiv.org/html/2603.25971v1>, March26,2026: read abstract
and introduction only. It targets sample cumulative reward under randomized
treatment assignment with fixed potential outcome values and times; that
differs from our iid-case risk and sound upper receipts. No theorem or proof
from this paper is imported. Its full technical delayed-feedback comparison
remains open. Searches on coarsened observations also found filtration-lifting
work, but those leads were not read and do not establish novelty here.

# Time-uniform PAC-Bayes comparator

Chugg, Wang and Ramdas, JMLR24(372),2023,
<https://www.jmlr.org/papers/volume24/23-0401/23-0401.pdf>: read introduction
and setting, Lemma3, Theorem4 and proof opening, Corollary15 and its short
proof, and Section4.2.5 through Corollary16. Their master theorem already
combines mixtures, change of measure, dominated processes and Ville, with
simultaneity over time and posteriors. This is a direct strong antecedent
for anytime_programs.md. The local upper-receipt substitution and finite
program-enumeration interface cannot support a generic statistical novelty
claim. The appendix proofs and experiments were not read or reproduced.

# Graph potential comparison

Johnson(1977), *Efficient Algorithms for Shortest Paths in Sparse Networks*,
<https://bohr.wlu.ca/hfan/cp412/references/p1-johnson.pdf>: read basic path
definitions and Section5, Lemma2 and the all-pairs construction around it.
The potential reweighting preserves shortest paths and is explicitly
attributed there to Edmonds and Karp, with related earlier sources. Thus
potential cancellation in potential_edits.md is established machinery.

Ng, Harada and Russell(1999), author PDF
<https://ai.stanford.edu/~ang/papers/shaping-icml99.pdf>, timed out twice.
The Toronto search result proved to be Toryn Klassen's2016 presentation,
not the original paper; it is not used as a primary theorem source. No
discounted-policy theorem from that unread paper is imported here.

# Randomized-encoding interface comparison

Applebaum(2017), *Garbled Circuits as Randomized Encodings of Functions:
a Primer*, <https://eccc.weizmann.ac.il/report/2017/067/download>: read
introduction through Example1.3 and the stated efficiency/decoder tradeoff.
Perfect privacy is equality of output laws for equal function values;
perfect correctness uses disjoint supports and a decoder. Those principles
already cover the motivation for our averaged count disclosure. The local
restrictions are count-only output, bounded episode queries, fresh resets
and separately paid repetition. Output locality in a randomized encoding
is not automatically a bound on total encoder queries. The IACR copy was
forbidden; ECCC opened once, then timed out when fetching Section2. No later
definition, lower-bound proof or construction is counted as read here.

# Additional source scopes after the balanced-summary construction

- Cullen, Montague and Rubinstein (June 26, 2026), [Halt Fast!](https://arxiv.org/html/2606.27694v1): abstract/introduction, Section 3 Theorem 1, Section 4 learned mixtures through equations (7)–(10), including the fixed safety anchor, inspected. This directly precedes the generic idea of learned certification bets insured by an ordinary component. The local forecast-range proposal must claim only its algebraic/partial-receipt contract and explicit resource bounds. Reported application speedups are not reproduced or transferred here.
- Csillag, Struchiner and Goedert (2025), [Prediction-Powered E-Values](https://arxiv.org/html/2502.04294v2): abstract/introduction and Section 2.1 through Theorem 2.1's opening statement inspected. The predictable randomized collection and inverse-probability correction are explicit prior art. Remaining theorem clauses and proof were not yet read in this screen. Our lower-receipt products do not silently instantiate this mechanism: missingness, positivity and acquisition contracts differ.
- Lee, Han and Kim (October 18, 2026), [Calibration-Free Early Stopping for Chain-of-Thought Reasoning via E-processes](https://arxiv.org/html/2610.25212v1): abstract/introduction, Sections 3.1–3.5, limitations, and Appendix C's null definition and scope paragraph inspected. Its guarantee concerns signal drift, explicitly not answer correctness. The polynomial-range null has a separate mathematical link to false completion; a model-confidence signal alone cannot replace that premise.
- Learning-Augmented Perfectly Secure Collaborative Matrix Multiplication (January 14, 2026), [arXiv record](https://arxiv.org/abs/2601.09916): abstract only. Its privacy/tensor-multiplication duty is not a completed comparator for range certification.

- Kayal (April 21, 2010), [Algorithms for Arithmetic Circuits](https://eccc.weizmann.ac.il/report/2010/073/download): abstract, introduction, Section 3 definitions 5–6, Lemma 8 and proof through the statement/start of Claim 8.1 inspected. Computing all linear dependencies by a small random evaluation matrix is an explicit antecedent. The remaining proof of Claim 8.1 was not retrieved (timeout), so no uninspected constants are imported. The earlier Shpilka–Yehudayoff survey link was a different work, not this source.
- Saunders, Storjohann and Villard (2004), [Matrix rank certification](https://journals.uwyo.edu/index.php/ela/article/download/237/237/237): Sections 1–3, both certificate algorithms and the conclusion inspected. Their Las Vegas certificates use characteristic-zero positivity, trace information and black-box matrix products; the paper explicitly distinguishes the finite-field limitation. This is a strong exact-certification comparator, not a source for applying positivity over arbitrary fields.
- Cade's Section 4.1 proof and Section 4.4 Lemma 6 were subsequently retrieved and inspected. The zero-error certificate equivalence and the nonnegative-literal representation are established antecedents; no claim is made that the local support argument discovers them.
- Dumas–Villard's CASC 2002 author PDF was indexed but returned 404 when opened. Only its search-index abstract and early-termination excerpt were inspected. Shpilka–Yehudayoff and Bhargava–Saraf–Volkovich PDFs were located but targeted section retrieval failed; they are leads, not completed theorem comparisons.

- Kaufmann, Cappe and Garivier, JMLR 17 (2016), [author paper](https://www.jmlr.org/papers/volume17/kaufman16a/kaufman16a.pdf): Lemma 1, Appendix A.1 Lemma 19, its proof and Wald identity (18) inspected. Sequential change of measure is prior art. Their mutual absolute continuity premise is stronger than the one-way support relation of the folded laws here; use the local truncation argument rather than importing the lemma without qualification.
- Kaniewski, Lee and de Wolf, [query complexity in expectation](https://homepages.cwi.nl/~rdewolf/publ/qc/query_expectation-arxiv.pdf): in addition to the earlier definition and theorem scopes, Section 5's opening example `(abs(x)-1)^2` inspected. The all-zero versus weight-one support obstruction is a close antecedent. No new generic gap between ordinary and nonnegative degree is claimed, and no quantum proof was imported.
- Cade (2018), [postselected classical query complexity](https://arxiv.org/html/1804.10010v2): abstract, introduction, Sections 2.1.1–2.1.2, 2.4 definitions 3–4 and lemmas 1–4, corollary 1, Section 3 theorems 1–4 and the symmetric near-balanced discussion inspected; Section 4.1.1's initial bullets only. The full Section 4.1 proof remains unread after an overflowing tool response. Exact postselection/certificate complexity and positivity restrictions are established topics. Paid repeated pure count laws have a different accounting contract; rejected runs cannot become free postselection.

# Additional numerical sensitivity screen

Codex (GPT-6), October 23. Diao, Wei and Qiao (2016),
[arXiv:1601.02333v1](https://arxiv.org/pdf/1601.02333), abstract and introduction
through equations 1.1–1.4, section 2 opening perturbed-optimizer equations 2.1,
and references 12/20 were inspected. These concern condition numbers for
linear functions of the optimizer using matrix/solution data. No completed
match to the local scalar optimal-value information contract was established.
Theorem 3 extraction was garbled and is not imported.

Chu, Lin, Tan and Wei (2011), *Condition numbers and perturbation analysis for
the Tikhonov regularization of discrete ill-posed problems*, NLAA 18:87–103,
and Gulliksson, Wedin and Wei (2000), *Perturbation identities for regularized
Tikhonov inverses and weighted pseudoinverses*, BIT 40:513–523, remain leads.
A Citeseer copy of the former returned 403. Its indexed theorem excerpt was
insufficient for a primary-source comparison. Unread search output at the
context boundary earns no literature credit; see dispositions.

# Approximate skeleton comparison

[Peherstorfer, Drmac and Gugercin, arXiv:1808.10473v4](https://arxiv.org/pdf/1808.10473)
(May 2020): read abstract/introduction, section 2.1 equations 3–5,
section 4.1 equation 17, section 4.2 opening/Lemma 4.1 statement, and
Theorem 4.6 statement/proof through its noise covariance calculation.
Equation 17 directly supplies the noiseless gappy-POD residual amplification
used in pass 32. The noisy result studies randomized oversampling and expected
errors under a noise model; our note states a deterministic bounded-noise
version. This distinction does not establish novelty. No sampling theorem is
imported to certify the local residual premise. Generic approximate skeleton
reconstruction is known; acquisition and task-specific evidence reuse remain
the possible synthesis, not a claimed new projection method.

# PAC synthesis comparison for private scope checks

[Chen et al., ICSE 2016](https://homepage.iis.sinica.edu.tw/~bywang/papers/icse16.pdf),
*PAC Learning-Based Verification and Model Synthesis*: read abstract,
introduction, sections 4.1–4.3, equation 2, sections 5.1–5.2 through Lemma 2,
and Theorem 1 statement. Their approximate equivalence queries use increasing
sample budgets across adaptive candidates; the reported guarantee concerns
probability of program paths under the specified sampling distribution.
Our polynomial-scope note uses a degree promise to turn a false universal
identity into a bounded probability of passing a private check, then applies
retirement to repeated proposals. Neither sample reuse nor algebraic identity
testing is claimed new. Their guarantees do not directly supply this local
all-input conclusion. The older private-verification sources already recorded
above remain closer comparators for the reuse lemma. Search found no completed
primary-source match for the entire correction/epoch contract; this is an
unresolved comparison, not evidence of novelty.

# Multinomial and selective-program comparison

[Lindon and Malek, NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/file/12f3bd5d2b7d93eadc1bf508a0872dc2-Paper-Conference.pdf):
read abstract/introduction, section 2.1 opening, equation 3, Theorems 2.1–2.4
statements and the confidence-region projection through equation 12.
The Dirichlet likelihood-mixture martingale is a direct antecedent. Appendix
proofs were not read; a requested line lookup instead returned the conclusion.
The local derivation states its own finite-mixture calculation and uses the
previously read general anytime PAC-Bayes construction. No generic novelty.

[Wu et al., arXiv:2405.14681v3](https://arxiv.org/pdf/2405.14681): abstract,
introduction, section 3.1 Theorem 3 and proof, and section 3.2 setup were read.
This supplies a close discrete-loss PAC-Bayes comparison lead; the recursive
prior theorem and its implementation were not imported or fully assessed.

[Akter et al., arXiv:2509.12527v2](https://arxiv.org/pdf/2509.12527v2): abstract,
introductory definitions, Theorem 2.6 with its continuation, and Appendix C.3
were inspected. The local [information note](information_coverage.md) gives
counterexamples to a displayed KL/MI inequality and to base-rate-free coverage
reasoning. These exclude that argument as support here. Other results and
reported experiments were not audited or reproduced. The paper's “skeleton”
means a language-model baseline distribution, unlike the linear error space
in our correction notes.

# Information and computation comparisons

[Shannon (1959)](https://gwern.net/doc/cs/algorithm/information/1959-shannon.pdf):
abstract and opening single-letter distortion definitions/examples were read.
The Queen's-hosted copy returned 404. This is a general antecedent for
value-weighted information constraints, not a completed comparison of our
specific binary frontier.

[Xu, arXiv:2604.11204v1](https://arxiv.org/pdf/2604.11204): abstract,
section II assumptions/core definition, derivation-depth definitions,
Theorem 3.5 construction, equation 3.13, depth-constrained distortion and
redundancy definitions/Lemma 4.1, Theorem 4.5 statement and Remark 4.10 read.
The source explicitly includes a communication/computation tradeoff, measured
in immediate-consequence iterations. Its distortion replaces one stored fact
relative to a fixed reference base. This is a relevant comparator for the
broader program, not the same primitive-query/count-observation contract.
The complete rate theorem and experiments were not independently checked or
imported. No claim that conventional information theory excludes reasoning
costs should be inferred from our terminology.

[Guo and Li, arXiv:2602.00906v7](https://arxiv.org/pdf/2602.00906): abstract,
introductory membership-testing setup, Assumption 2.5, Theorems 3.1–3.3
statements, and section 3.1 through Lemma 3.5 were read. It gives sparse-limit
memory/error characterizations for random key sets and generic output losses.
Memory size and query-observation budgets differ; its asymptotic result is
not a direct improvement over or refutation of our finite pure-query claims.
Proofs and reported empirical results were not imported or reproduced.
