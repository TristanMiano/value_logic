# s17 primary-source comparison log

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT. Read scopes below are
positive records of inspection, not claims of an exhaustive literature search.
Full copyrighted source copies are temporary local scratch material, not
tracked evidence. The [claim](claim.md) fixes the comparison event.

## Initial closest-result screen

**El Ghaoui and Lebret (1997), [Robust Solutions to Least-Squares Problems
with Uncertain Data](https://people.eecs.berkeley.edu/~elghaoui/Pubs/rob-ls.pdf).**
Read the introduction's quantifiers, Lemmas 2.1–2.4 and the displayed proof
of 2.2, Theorems 3.1–3.3 with proofs through the scalar reduction, Remarks
3.1–3.2, Theorems 4.1–4.2 statements, and sections 5.1–5.2. The rank-one
worst residual, SOCP/SDP formulation, data-dependent regularization and
scalar search are established machinery. The specified objective chooses
x before its worst perturbation; section 5 also accommodates rational
matrix dependence and structured uncertainty. Thus merely saying N16 uses
a rational matrix function is not a novelty argument. The actual remaining
comparison is whether the compatibility constraint W^T(I+MM^T)^(-1)W=C,
unrestricted source dimensions, reoptimized value and attained scalar
endpoints follow by a routine reduction. That reduction is not supplied by
the inspected statements. The manuscript's full appendix/structured proof
audit has not been completed in this initial screen.

**Davis, [Dilations preserving a bound on the norm of an operator](https://maths.anu.edu.au/files/1-CMAProcVol5-Davis.pdf),
CMA volume 5, printed pp.3–14.** Read the full author exposition; visually
checked printed p.6's factorization and all-completions formula. The web
reader timed out, but direct download succeeded (942,433 bytes). Prescribed
block row/column norms characterize existence of a norm-bounded completion;
defect operators and a free contraction describe all completions. The final
application optimizes a linear numerical algorithm with prescribed
discretization/interpolation. This is strong prior for dilation and
information-limited algorithm design. N16 cannot claim either generic idea.
Whether its coupled nonlinear response/edit class collapses to that theorem
is a specific reduction obligation, not resolved by different terminology.
The original [Davis–Kahan–Weinberger 1982 journal paper](https://epubs.siam.org/doi/10.1137/0719029)
was inspected at abstract/reference scope only; its full PDF request timed
out. The exposition must not be represented as a complete audit of that
paper's eigenvalue applications. The [ANU catalogue](https://maths.anu.edu.au/research/cma-proceedings/miniconference-operator-theory-and-partial-differential-equations-0)
identifies volume 5 and the July 1983 meeting; its webpage metadata is mixed,
so no new precise publication-year claim is inferred from it.

**Hansen and Pedersen (2002 manuscript), [Jensen's Operator Inequality](https://arxiv.org/pdf/math/0204049).**
Read introduction, Theorem 2.1's isometry/compression equivalences and the
displayed averaging proof segment in section 3. Applying inverse compression
to the two rational maps is directly covered by classical operator convexity.
No novelty attaches to validity of the compressed inequalities alone. The
nontrivial assessment target is sharpness for the specified source/edit
information class, with its usefulness and implementation contract.

**Becker, Kawas, Petrik and Ramamurthy, [Robust Partially-Compressed
Least-Squares](https://arxiv.org/pdf/1510.04905), rendered September 2018.**
Read section 2 equations (5)–(10), Lemma 1 and Theorem 1 with proofs;
Theorem 2's approximation-guarantee statement only. Their retained objects
are a sketched design and an uncompressed linear term. They robustify the
chosen estimator against sketch errors and derive a conic/scalar-search
algorithm. This is a stronger concrete comparison than ordinary full
evaluation, but the stored information and decision order differ from N16.
Its empirical speedups are not N16 evidence, and its whole performance
analysis was not inspected here.

**Foucart, [Worst-Case-Optimal Estimation of a Quadratic Form by Quadratic
Functionals of its Linear Observations](https://foucart.github.io/publi/OR_QuadraticQ_v3.pdf).**
Read sections 1–2 through Theorem 1's upper-endpoint proof, including model,
observation and nondegeneracy assumptions. Ellipsoidal uncertainty plus
linear observations admits local endpoint SDPs by the S-lemma. The
information-conditioned interval and midpoint interpretation are therefore
established optimal-recovery concepts. Taking an unknown contraction matrix
as the object makes N16's information linear, but its perturbed inverse
target and factor-edit constraint do not immediately become this quadratic
ellipsoid problem. A different parametrization may still give a routine
reduction; that is a live novelty risk. Global and noisy-observation theorems
have not been audited in this initial screen.

## Search limits

Searches covered retained/partial information in robust least squares,
compressed resolvent perturbation, regularized optimal-value perturbation,
norm-preserving dilation and optimal recovery. Many hits concerned regression
outliers, learning regret or unrelated operator resolvents; these were not
treated as relevant evidence. Absence of an exact keyword match is not
evidence of novelty. The next mathematical screen should attempt the
strongest plausible reductions explicitly.

## Matrix uncertainty and data-consistent models

**Van Waarde, Camlibel and Mesbahi, [From noisy data to feedback controllers:
non-conservative design via a matrix S-lemma](https://arxiv.org/pdf/2006.00870),
v2 December 2020.** Read introduction and noise model, Theorems 9 and 11
with their displayed proofs, Corollaries 10 and 12, and Theorem 13's
statement. Visually checked PDF p.5 because text extraction confuses strict
and nonstrict matrix signs: Theorem 9 uses a strict generalized Slater
assumption, nonstrict conclusions, and a nonnegative scalar multiplier.
Theorem 11's strict conclusion additionally uses boundedness. This is direct
prior for exact robust certificates from a compatible-model class and for
eliminating matrix uncertainty with scalar multipliers. N16's general
philosophy therefore overlaps conventional methods completely. What still
requires assessment is the elimination of its nonlinear compressed-resolvent
and factor-edit constraints into the particular sharp interval. This source's
data-driven control applications were not audited in full. The failed web
screenshot request was replaced by a direct PDF download and local render.
The [explicit specialization](fixed_source.md) now recovers the exact
fixed-source upper family; the remaining delta concerns compressed information.

**Bisoffi, De Persis and Tesi (2022), [Data-driven control via Petersen's
lemma](https://pure.rug.nl/ws/portalfiles/portal/236636177/1_s2.0_S0005109822003983_main.pdf).**
Read introduction, Facts 1–2, Proposition 1 and its full proof (matrix
ellipsoid equals an affine image of a norm-bounded matrix), and Theorem 1's
statement and Schur-complement reduction. Their nonstrict Petersen version
requires additional nonzero/positive-definite assumptions for equivalence;
the sufficient direction has weaker hypotheses. This supplies a strong
conventional comparison using the full data-consistent set, rather than
recovering a unique model first. A changed representation can support a
useful adaptation, but using a scalar uncertainty multiplier is already
standard. N16 still owes its source-class reduction and exact sharpness;
merely producing an LMI or calling observations a receipt would add little.
The polynomial-system extension and all appendix proofs were not read.

**Jongeneel, Summers and Mohajerin Esfahani (2019), [Robust Linear Quadratic
Regulator: Exact Tractable Reformulation](https://wjongeneel.nl/pub/RLQR_CDC_2019.pdf).**
Read the problem definition, Examples II.4–II.5, Definition III.1 and
Proposition III.4's statement. The uncertainty set is tied to a discounted
state covariance and a weighted perturbation cost, rather than a generic
Euclidean ball. It illustrates why an exact uncertainty contract matters
and why model-specific reoptimization differs from one common controller.
It is contextual prior, less close to N16 than the matrix S-lemma or robust
least-squares sources. Its Riccati proof and performance theorem have not
been inspected, so no theorem import is made. An older author URL redirected
to an institutional administrative page; the author's current PDF succeeded.

**El Ghaoui, Oustry and Lebret (1998), [Robust Solutions to Uncertain
Semidefinite Programs](https://people.eecs.berkeley.edu/~elghaoui/Pubs/rob-sdp.pdf).**
Read sections 2-3, Lemma 2.1, Lemmas 3.1-3.2 and Theorems 3.1-3.2;
also the conclusion and Appendix B's representation/scaling setup, not
the full sensitivity appendix. Rational matrix dependence can be represented
using repeated scalar uncertainty blocks. Exactness for a full block must
not be transferred automatically to that structured representation. The
block-full extension in section 2.3 concerns independently perturbed output
blocks. It does not state that every coupled multiple-block uncertainty is
lossless. This is strong prior for rational robust certificates, with a
precise warning against claiming either automatic exactness or novelty merely
because a matrix fractional expression appears.

**Padoan, Coulson, van Waarde, Lygeros and Doerfler (2022), [Behavioral
uncertainty quantification for data-driven control](https://arxiv.org/pdf/2204.02671).**
Read introduction, section III through Theorem 1 and its proof, Corollary 2,
and Theorem 2's statement. Graph-subspace distances and projection-based
estimation errors are explicit prior. Theorem 1 relates the gap of two
known graph representations to their operator difference; it does not give
N16's endpoints from a retained compression of one projection. The control
case study and infinite-horizon proof were not audited. This is a geometric
comparison route; the matrix S-lemma remains the closer exact endpoint result.

**Bhatia, Jain and Lim (2017 manuscript; journal publication 2019), [On the
Bures-Wasserstein distance between positive definite matrices](https://arxiv.org/pdf/1712.01504).**
Read section 2 through Theorems 1-2 and proofs, and section 3's covariance
coupling reduction through equation (23). Distances between matrix factors,
block-PSD coupling descriptions and projection/principal-angle geometry
are established tools. Theorem 1 uses the Frobenius norm; importing its
polar-factor optimizer for the operator-norm edit would require a different
argument. The source does not, in these inspected sections, supply the
compressed ridge-response interval. Barycenter and iteration results were
not inspected and are not used.

**Bakonyi and Woerdeman (1993), [On the strong Parrott completion problem](https://www.researchgate.net/publication/238870299_On_the_strong_Parrott_completion_problem).**
Read the author-uploaded five-page text through Theorems 2.1, 2.2 and 2.4
and their displayed arguments. Theorem 2.1 treats contraction completion
subject to a prescribed linear interpolation equation; its proof reduces
existence to positive-semidefinite completion and Schur complements. This is
stronger prior than unconstrained dilation alone. The extracted formulas
have unreliable stars and inequality signs; no exact formula is imported
without our own reconstruction in completion.md. A web PDF opened, but its
screenshot returned no usable image; the direct download was access-restricted.
The publisher request also failed. These are retrieval limitations, not
mathematical evidence. The author's uploaded text is the inspected source.
The existence/parametrization argument makes a generic claim of novelty for
interpolating contractive completions untenable; the specific nonlinear
source/edit reduction remains the comparison obligation.

## Additional formulation screens

**Antezana, Corach and Stojanoff (2004 manuscript), [Spectral shorted
operators](https://arxiv.org/pdf/math/0410573).** Read the introduction and
section 2 through Proposition 2.4 and its proof. The extremal positive
operator supported on a subspace, its monotonicity and projection formula
are established structure. A compressed inverse can be related to a Schur
complement/shorted operator, but these inspected statements do not eliminate
the coupled factor edit. The later spectral-power and complexity results
were not audited and are not imported. The original Anderson–Trapp
[Shorted Operators II](https://epubs.siam.org/doi/10.1137/0128007) was read
at publisher-abstract scope only.

**Tian (2025 manuscript), [Shorting Dynamics and Structured Kernel
Regularization](https://arxiv.org/pdf/2512.04874).** Read the introduction,
section 4 through Theorem 4.3 and its displayed proof, and section 5's
rank-one energy-selection argument through Theorem 5.2. This describes
an operator/kernel trajectory and ridge predictors from its Gram matrices.
The inspected object is not an uncertainty class conditioned only on an
old compressed resolvent. It is a contextual application lead, not an exact
N16 reduction or an imported theorem. Its full convergence/invariance
analysis has not been audited here; no correctness or novelty endorsement
is inferred from the paper's own contribution language.

Additional searches for compressed-resolvent perturbation, retained inverse
quadratics, partial Gram information and regularized value sensitivity mostly
returned spectral scattering, robust common-action estimation, statistical
outliers, or approximation methods with different information. Such search
misses are not evidence that the pinned sharp theorem is new. The strongest
substantive comparisons remain the matrix S-lemma, operator Jensen and
constrained completion, for which explicit reductions were attempted.

**Bousselmi, Hendrickx and Glineur, [Interpolation Conditions for Linear
Operators and applications to Performance Estimation Problems](https://arxiv.org/pdf/2302.08781),
v3 March 2024.** Read sections 2–3 through Theorem 3.6, including Theorem
3.1's statement and main proof, the factorization/rotation Lemmas 3.4–3.5,
and Appendix B's displayed construction and norm-completion step. Appendix
C's zero-padding setup was inspected, not its entire rotation calculation.
Theorem 3.1 supplies exactly the bounded two-sided interpolation conditions
used in gram_sdp.md. Theorem 3.6 also handles an unbounded linear source
through additional Gram LMIs and an auxiliary scalar, preserving kernel
conditions. This is the closest general conventional framework found so far:
the N16 problem can be specialized into it. Neither a dimension-independent
SDP formulation nor the interpolation principle is a new contribution here.
The remaining possible delta is its explicit one-parameter endpoint solution,
attainment structure and useful conditional certificate. The algorithm-rate
applications in section 4 were not audited. Their absence of the words
"ridge" or "perturbation" is not evidence of novelty.

**Taylor, Hendrickx and Glineur, [Smooth Strongly Convex Interpolation and
Exact Worst-case Performance of First-order Methods](https://arxiv.org/pdf/1502.05666),
v6 October 2016, journal 2017.** Read the introduction and sections 3.1–3.3
through Theorem 5 and its proof. Gram matrices, dimension conditions,
primal worst-case instances and dual inequality certificates are established
performance-estimation methodology. Its function-interpolation theorem was
not reconstructed here and is not needed for the linear-operator reduction.
The newer operator paper provides the more direct import; this source
establishes the methodological background rather than the specific N16 formula.
## Follow-up comparison: extensions of the operator framework

**Bousselmi, Deng, Lu, Glineur and Hendrickx (2025),
[On the Convex Interpolation for Linear Operators](https://arxiv.org/pdf/2511.16360),
v1.** Read the introduction, the recalled bounded interpolation conditions,
the Gram representation setup, and Section 3 through Theorem 3.6 and its
polar-decomposition proof. Its conditions accommodate lower as well as upper
singular-value restrictions. This matters if a comparison gives the old source
extra spectral information: such information should strengthen the ordinary
control, rather than be ignored to preserve an N16 advantage. The present core
has no such extra restrictions. The inspected material does not supply its
one-parameter endpoint solution. Sections 2 and 4's full proofs and Section 5's
algorithmic applications were not audited. This is a comparison scope, not a
claim that the entire paper has been excluded as relevant prior art.

**Ranjan and Stellato (2025),
[Verification of First-Order Methods for Parametric Quadratic Optimization](https://arxiv.org/pdf/2403.03331),
v2.** Read Sections 1–2 and Section 3's comparison/setup through the
unconstrained-QP gradient iteration. They address finite-step algorithm
verification, explicitly including parameter and warm-start sets. Their
displayed PQP family fixes the quadratic matrix while varying linear terms
and bounds; their output is a convergence/residual guarantee. This supplies
an important conventional comparison for future solution-reuse claims, but
does not itself state the current sharp range of a reoptimized value over
unknown sources with a fixed compressed inverse. No claim about the correctness
of their full 58-page analysis is needed here.

**Avron, Clarkson and Woodruff (2017),
[Sharper Bounds for Regularized Data Fitting](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2017.27).**
Read the introduction and ridge-regression statement Theorem 2 (the condensed
version of Theorem 15), including its statistical-dimension and approximation
guarantee. It provides established resource-aware approximation of ridge
solutions using sketches, with a different retained object and guarantee.
N16 cannot claim that useful compressed ridge information is new. Its proposed
delta concerns the exact interval licensed by one specified response block
under arbitrary operator-norm edits. We did not reconstruct the sketching
theorem's omitted proof or compare implementation runtimes.

Searches for compressed resolvents, spectral-norm perturbations of ridge
values, and follow-ups to the operator-interpolation paper found no inspected
statement of the exact N16 endpoint theorem. Many leads concerned statistical
risk, solution perturbations, or spectral resolvents of different operators.
This limited search is not proof of novelty. The published 2024 operator-paper
PDF at the UCLouvain repository timed out; its arXiv version remains the
actually inspected source.

## General envelope leads

**Foucart, [Optimal Algorithms for Nonlinear Estimation with Convex
Models](https://foucart.github.io/publi/OR_NonlinearQ_v5.pdf), author version v5.**
Read the introduction/setup, Theorem 1's statement and opening proof reduction,
and Proposition 6's convex-program statement and explanation. These concern
optimal estimation of sup-linear functionals from linear observations on a
convex model set containing zero. They reinforce that information-conditioned
optimal estimation and convex computational constructions are established
goals. The inspected statements do not evaluate N16's specific endpoint
program. Its nonlinear source representation must first be converted to a
suitable convex information problem; the Gram reduction already does that
more directly for our comparison. The full proof and later examples were
not reconstructed, and no new theorem is imported from this lead.

**Davidson and Kennedy, [Noncommutative Choquet
Theory](https://www.math.uwaterloo.ca/~krdavids/Preprints/DavidsonKennedy_ncCh.pdf),
author manuscript.** Read the introduction, the multivalued-function setup
around Section 7.3, and statements/discussion of Proposition 7.4.5 and
Theorem 7.5.1. The convex-envelope description through representing completely
positive maps is relevant background for compression and dilation. It also
reinforces the need to distinguish scalar endpoint optimization from a
single greatest or least matrix bound. This is an abstract representation,
not an inspected explicit solution of the coupled ridge-source/edit problem.
The 79-page theory and its dependency chain were not audited. No claim of
novel matrix convexity, Jensen inequality, or envelope representation is made.

## Geometric and moment-problem leads

**Makarov and Seelmann (2010), [Metric properties of the set of orthogonal
projections and their applications to operator perturbation
theory](https://arxiv.org/pdf/1007.1575).** Read the introduction and Section 2
through Corollary 2.2 and its proof. Graph projections, inverse Gram blocks,
and the noncommutative angle-addition identity are established geometry.
The inspected statements retain the graph operators, rather than optimize
an edited ridge value from one compressed inverse. The later spectral-subspace
perturbation theorems were not audited. This comparison supplies no new
import beyond crediting the graph interpretation already used here.

**Fritzsche, Kirstein, Kley and Maedler (2021), [The Weyl matrix balls
corresponding to the matricial truncated Hamburger moment
problem](https://arxiv.org/pdf/2109.11900).** Read the introduction and
Theorem 8.7's statement and explanatory discussion. The theorem explicitly
parametrizes values of Stieltjes transforms under matrix moment constraints.
It reinforces that sharp matrix-information envelopes are established
objects. Its displayed problem does not include the coupled unknown source
and norm-bounded edit of N16. No reduction from N16 to that theorem has
been established here; its 68-page proof was not audited.

**Ballal, Suliman and Al-Naffouri (2017), [Bounded Perturbation Regularization
for Linear Least Squares Estimation](https://www.researchgate.net/publication/320482184_Bounded_Perturbation_Regularization_for_Linear_Least_Squares_Estimation),
author-uploaded text.** Read the introduction, the MSE setup in Section II,
and Section III through equations (19)--(25). The perturbation is used to
select a regularization parameter, with a known design matrix and one robust
action. The norm-plus-residual reduction and rank-one equality edit are
conventional ingredients, already credited in the closer robust-LS comparison.
The subsequent statistical parameter-selection approximations and experiments
were not audited. Direct access to the KAUST PDF returned 403; this author
copy is the text actually inspected.

Ito and Takeuchi's [The minimum value function for the Tikhonov regularization
and its applications](https://arxiv.org/abs/0910.4351) was screened at abstract
scope only. It concerns regularization-parameter selection. No theorem is
imported and the abstract is not treated as an exclusion of the full paper.

## Robust estimation under neighboring information contracts

**Loyka and Charalambous (2015), [Novel Matrix Singular Value Inequalities
and Their Applications to Uncertain MIMO
Channels](https://www.site.uottawa.ca/~sloyka/papers/2015/Loyka.Charalambous.T-IT.12-15.pdf).**
Read the introduction, Theorem 2 and its hypotheses/discussion, Section IV-A
through Proposition 2, and Section V through Proposition 3. The robust MMSE
result optimizes transmission for a known nominal channel and a sum-MSE
criterion. The text explicitly distinguishes singular-value bounds from
Loewner bounds for every fixed direction. It therefore does not justify
replacing a fixed-target ridge worst case by coordinatewise singular-value
shrinkage. The matrix-inequality proofs in the appendix were not reconstructed.
This is a useful strong neighboring comparison, not the same retained-C
information problem. The operator-interpolation SDP remains more direct.

**Vanli, Donmez and Kozat (2015), [Robust least squares methods under
bounded data uncertainties](https://repository.bilkent.edu.tr/bitstreams/91bc7e25-935d-41b2-b423-5ef507248b58/download).**
Read the introduction, Section 3.1's Taylor reduction and Lemma 1, and
Section 3.2 through Theorem 2. Their regret comparator includes the
reoptimized LS/ridge value, but the tractable displayed regret program uses
its first-order Taylor approximation around a known matrix and target.
This is relevant to later solution-reuse comparisons; it does not supply
the exact finite-edit compressed-information endpoints. No superiority over
their intended estimation application is claimed, and their simulations and
structured extension were not audited.

Wang, Bengtsson, Ottersten and Palomar's [Robust MIMO Precoding for Several
Classes of Channel Uncertainty](https://palomar.home.ece.ust.hk/papers/2013/WangBengtssonOtterstenPalomar_TST2013.pdf)
was screened at abstract/introduction scope. It concerns robust precoding
with a known nominal channel and is a lead for applications, not an imported
theorem or an exhaustive prior-art exclusion.

## Factor-distance and Harnack representations

**Peyre (2026), [Muon Dynamics as a Spectral Wasserstein
Flow](https://arxiv.org/pdf/2604.04891), v3 October 17.** Read the introduction,
Proposition 3.6, and Appendix D through Corollary D.2 and its proof. The
Gaussian reduction optimizes a covariance block and specializes to the
operator norm; commuting covariance matrices have a closed square-root
formula. This gives a conventional factor-distance representation relevant
to norm-bounded edits, but not the optimization of a fixed inverse-value
target under the additional compressed-inverse equality. The gradient-flow
and transport theory elsewhere in the paper were not audited. No result
about practical Muon performance is used in this assessment.

**Badea, Suciu and Timotin (2017), [Classes of contractions and Harnack
domination](https://ems.press/content/serial-article-files/38642?nt=1).** Read
the introduction, definitions and Section 2 through Theorem 2.7 and its
proof. Harnack domination compares positive operator functions via Poisson
kernels and yields resolvent estimates. These are useful background for
operator inequalities, but the premise is a domination relation between
contractions, rather than a norm bound between ridge factors with only C
retained. No exact reduction furnishing N16's endpoints has been established.
The paper's later spectral and ergodic results were not audited.

**Kretschmann, Schlingemann and Werner, [A Continuity Theorem for
Stinespring's Dilation](https://arxiv.org/pdf/0710.2495), v1 2007.** Read the
introduction and the Bures-distance definition. The infimum over common
dilations is relevant geometric background, while its completely bounded
map-distance comparison is a different specified object. No theorem from
the rest of the paper is imported, and the read scope does not exclude
every possible adaptation.

## Final targeted compressed-resolvent screen

**Arlinskii and Hassi (2015), [Compressed resolvents of selfadjoint
contractive extensions with exit and holomorphic operator-functions
associated with them](https://arxiv.org/pdf/1502.03239), v2.** Read the
introduction and Sections 2.1--2.3, including the Cayley-transform setup and
Schur--Frobenius resolvent formula. This treats extensions and their analytic
resolvents, not the stated norm-budgeted change between two ridge factors.
It credits the fractional/compression machinery. The later extension and
function-class theorems were not audited, and no exhaustive exclusion follows.

The publisher abstract/introduction preview for [Efficient estimates for
matrix-inverse quadratic forms](https://doi.org/10.1016/j.apnum.2024.01.013)
was screened: it describes estimates for a given positive definite matrix,
with condition-number and near-eigenvector regimes. Direct full-page access
returned 403. No theorem or proof from that paper is imported. The targeted
search also returned already inspected robust-LS parameter-selection work
and unrelated statistical-rate results. Search results are leads, not a
novelty certificate. This closes this particular search pass; the precise
operator-interpolation comparison remains the strongest identified control.

## Further exact-learning and robust-value comparisons

**Angluin and Dohrn (2017), [The Power of Random Counterexamples](https://proceedings.mlr.press/v76/angluin17a/angluin17a.pdf).**
Read Sections 1--3's query contract and Section 5, including Theorem 21's
induction and Theorem 23's high-probability argument. The elimination-graph
existence proof in Section 4 was not reconstructed. This strengthens the
existing comparison to public counterexample learning: a random witness is
an established information resource, and small query count does not imply
cheap hypothesis computation. It does not establish the private-check
service's complete economics or provide an all-input polynomial margin.

**Cherapanamjeri et al. (2023), [Robust Algorithms on Adaptive Inputs from
Bounded Adversaries](https://arxiv.org/pdf/2304.07413).** Read the introduction,
dynamic-regression contract and Theorems 1.1--1.2 statements; locate Section
5.1's unlimited-query KDE setting. The later algorithmic proofs were not
audited. This is relevant prior work on protecting reused randomness and
restricting adaptive interactions. Its approximate regression/KDE duties
differ from exact polynomial scope checks with independently bought public
repairs. No new adaptive-data principle or quantitative theorem is imported.
Hardt--Woodruff's adaptive-sketching abstract was also located; no proof from
that paper was read in this pass.

**Beck and Ben-Tal (2009), [Duality in robust optimization: Primal worst
equals dual best](https://www.tau.ac.il/~becka/25.pdf).** Read the introduction,
Section 2 through Example 2.2's robust and optimistic least-squares reduction,
and Theorem 4.1 with its proof and Example 4.2. The former reduces a fixed
matrix's favorable perturbation to a positive-part residual norm difference;
the latter explicitly requires concavity in uncertainty for its minimax
equality and exhibits failure without it. These are direct predecessors of
the scalar parameter and quantifier discussion. They do not justify applying
a minimax exchange to the N16 compatibility class. The separate
[fixed-source S-lemma reduction](fixed_source.md) remains the stronger exact
value comparison for this claim. Section 3's LP derivation was not audited.

**Golub, Hansen and O'Leary, [Tikhonov Regularization and Total Least
Squares](https://drum.lib.umd.edu/bitstreams/1502d531-6ec5-4fd5-8eb1-779241ecc65e/download),
1998 technical report.** Read the introduction, Section 2 formulations and
Theorem 2.2 with its proof; inspect Theorem 2.3's statement. The retrieved
text has poor mathematical character extraction. The source studies a
joint matrix/right-hand-side fitting error under a solution-norm constraint,
including positive and negative regularization parameters. Those established
connections caution against claiming novelty for optimistic quadratic
fitting or secular equations. No precise constant from this source is used,
and it is not identified as the compressed-response endpoint theorem.

Moazeni--Coleman--Li's [Regularized robust optimization: the optimal portfolio
execution case](https://cs.uwaterloo.ca/~yuying/papers/regularized_robust.pdf)
was a search lead. Its abstract and located stability-theorem context concern
a different uncertainty-set problem; the full portfolio analysis was not
read or imported. These additional screens refine attribution, not a proof
that the relevant literature contains no equivalent analytic result.

## Relative graphs, spectral subspaces and Poisson kernels

**Ryu, Hannah and Yin, [Scaled Relative Graphs](https://arxiv.org/pdf/1902.09788),
v4, June 2021.** Read Section 3.3's SRG-full definition and Theorem 2,
Theorems 3--4 and their proofs, Section 4.4's sum theorem and proof, and the
composition statement and failure example around Theorem 7. The inversion
theorem was located, but its whole proof was not reconstructed. Their exact
class calculus requires SRG-fullness and, for the stated equality for sums,
a chord property. Finite anchored observations of a particular resolvent
are not automatically such an operator class. This supplies a strong
geometric comparison and cautions against importing a scalar diagram as a
matrix theorem; the rest of the 49-page paper was not audited.

**Pates, [The Scaled Relative Graph of a Linear Operator](https://arxiv.org/pdf/2106.05650),
v2, August 2021.** Read the introduction, Beltrami--Klein setup, Theorem 1's
statement and the proof of equation (3.1), plus Theorem 2 and its proof for
real complexification. The graph isometry involving
`(I+T*T)^(-1/2)` connects the transformed SRG to a numerical range. The
real two-dimensional exception matters. The spectral/similarity portions
of Theorem 1 were not fully reconstructed. This establishes relevant
graph/resolvent geometry, not the particular constrained ridge-value
endpoint result under an additive factor budget.

**Quan, Bodard, Oikonomidis and Patrinos, [Scaled relative graphs for pairs
of operators beyond classical monotonicity](https://arxiv.org/pdf/2511.20209),
v2, August 2026.** Read the introduction, Definitions II.1--II.2,
Proposition II.3's statement, and the proofs of Propositions III.1--III.3
on transformed/warped resolvents and preconditioning. The appendix calculus
and circuit applications were not fully audited. Paired operator geometry
is established prior work; its whole-class incremental premises differ
from the finite anchored block C. No direct specialization giving N16's
scalar endpoints or finite witnesses was identified in the inspected parts.

**Motovilov and Selin, [Some Sharp Norm Estimates in the Subspace
Perturbation Problem](https://arxiv.org/pdf/math/0409558), v2, April 2006.**
Read the introduction, Theorem 1's hypotheses/statement, and Theorem 4.7
with its reduction to Theorem 1. Its selfadjoint spectral-gap and
off-diagonal-perturbation assumptions are material. The main proof of
Theorem 1 was not audited. This comparison does not turn a spectral
subspace norm bound into a sharp compressed-value information bound.

**Chalendar (2003), [The Operator-valued Poisson Kernel and its
Applications](https://www.irishmathsoc.org/bull51/S5101.pdf).** Read the
introduction and Section 2 through Proposition 2.5's proof. The kernel's
factorization proves positivity for contractions and supports the usual
polynomial norm inequality. Its premise concerns a contraction and disk
parameter, not two unknown ridge factors at a specified norm distance.
The later functional-calculus and invariant-subspace applications were
not audited. No direct N16 endpoint theorem is imported. The earlier
Harnack-domination comparison remains distinct from an additive edit bound.

The attempted PDF screenshot calls for the relative-graph sources returned
references without visible image pixels. Reading claims above concern the
retrieved text, not visual inspection. Searches also found local solution
stability and causal sensitivity work; search snippets alone do not settle
this theorem's novelty.

**Cui, Hoheisel, Nghia and Sun, [Lipschitz Stability of Least-Squares
Problems Regularized by Functions with C2-Cone Reducible Conjugates](https://arxiv.org/pdf/2409.13118),
v1, September 2024.** Read the introduction, Theorem 3.5 with its reduction
to earlier lemmas, and Theorem 3.8's equivalence statement and short proof.
The full prerequisite strong-regularity machinery was not reconstructed.
This concerns local single-valued/Lipschitz solution maps for general
regularizers. It is a relevant stability predecessor, but does not directly
give global worst edited values over sources sharing a compressed inverse.

**Christensen and Connault (2023), [Counterfactual Sensitivity and
Robustness](https://discovery.ucl.ac.uk/10160441/2/Christensen_Econometrica%20-%202023%20-%20Christensen%20-%20Counterfactual%20Sensitivity%20and%20Robustness.pdf).**
Read the introduction, Section 2.1's moment-constrained setup, Section
2.3's divergence assumptions and Proposition 2.1's dual formulation,
and Section 2.5's qualification definitions and Theorem 2.1 statement.
The supplemental proofs and empirical/statistical-inference analysis were
not audited. Sharp sensitivity bounds with unresolved model features and
finite dual programs are already conventional research goals. Its
distributional neighborhood and moment constraints differ from N16's
operator edit and resolvent information, so no theorem is imported as an
endpoint solution. The source supports conceptual attribution, not an
empirical claim for the present construction.

## Additional comparison for the shared-source follow-on

**Lin and Sinnamon (2012), [The Generalized Wielandt Inequality in Inner
Product Spaces](https://www.math.uwo.ca/faculty/sinnamon/pdf/wielandt.pdf).**
Read the introduction, the two-inner-product definitions and Lemma 2.1,
Theorem 2.4's two-dimensional proof and equality construction, Theorem
2.8 and Corollary 2.9 with proofs, and Theorems 3.1--3.2's matrix
formulation. The later statistical corollaries were not fully audited.
These results give sharp angle/cosine comparisons from norm-equivalence
constants. They are relevant to graph-shear and relative-condition
interpretations. They do not directly state the diameter of two ridge
resolvents normalized by their common old resolvent under separate additive
factor budgets. A reduction could still be possible; the inspected result
is not excluded merely because its notation differs.

The Hansen UCLA report [cam89-04](https://ww3.math.ucla.edu/camreport/cam89-04.pdf)
was located through an indexed Section 4 perturbation excerpt. Opening the
PDF returned zero extracted text lines, so no full theorem/proof audit is
claimed. The excerpt concerns perturbed regularized solutions rather than
the common-source relative value contrast. Further search results on
resolvent diameters were mostly spectral/PDE or statistical concentration
problems; no theorem is imported from those snippets. The earlier
Bousselmi--Hendrickx--Glineur interpolation result remains the strongest
identified constructive formulation for the new Gram certificate too.
# Late comparison: relative resolvent diameter and conditioning

The two-edit follow-on is separate from N16-C/v1. Searches for a sharp
relative resolvent diameter, regularized-inverse perturbation constants,
Tikhonov sensitivity and the unit-radius decimal coefficient did not locate
an exact matching theorem. Search failure is not novelty evidence. The
strongest comparison instead came from a direct combination of the already
credited Young bounds, giving [an exact analytic coefficient](pair_radius.md)
for every radius. It supersedes the apparent SDP coefficient advantage.

* Diao, Wei and Qiao, [Structured Condition Numbers of Structured Tikhonov
  Regularization Problem and their Estimations](https://arxiv.org/pdf/1601.02333),
  v1 January11,2016: read the introduction, the target map and limiting
  condition-number definitions in section2 (equation2.7), and section3.1's
  Lemma3 derivative proof and Theorem1 statement/proof. These concern local
  changes of a linear functional of the regularized solution, with known
  structured source and data. They establish conventional target-specific
  sensitivity machinery. The inspected result does not give the global
  common-center two-edit value diameter. Sections3.2 onward, nonlinear
  structure proofs and experiments were not audited. No theorem imported.
* Malyshev, [A Unified Theory of Conditioning for Linear Least Squares and
  Tikhonov Regularization Solutions](https://epubs.siam.org/doi/10.1137/S0895479801389564),
  2003: publisher abstract and references only. Exact Frobenius condition
  numbers and spectral-norm estimates are described; the full proof is
  subscription content and was not read. It remains a closer conditioning
  lead, not an excluded prior theorem.
* Gulliksson, Wedin and Wei, [Perturbation Identities for Regularized Tikhonov
  Inverses and Weighted Pseudoinverses](https://link.springer.com/article/10.1023/A:1022319830134),
  2000: publisher abstract and references only. It describes GSVD-based
  perturbation identities for the regularized inverse and weighted
  pseudoinverse; no full statement or proof was accessible. No result
  beyond this scope is inferred.
* Chu, Lin, Tan and Wei, [Condition numbers and perturbation analysis for the
  Tikhonov regularization of discrete ill-posed problems](https://research.manchester.ac.uk/en/publications/condition-numbers-and-perturbation-analysis-for-the-tikhonov-regu),
  2011: author-institution abstract only. The indexed CiteSeer PDF returned
  HTTP403. It describes normwise/componentwise conditioning, but was not
  inspected at theorem level.

The initial dblp and DOI tool opens failed; publisher URLs subsequently
provided the abstracts above. No paid access, inferred full reading or
hardware diagnosis is claimed. The new exact diameter has a short ordinary
derivation and remains unassessed for moderate novelty.

Sion, [On general minimax theorems](https://msp.org/pjm/1958/8-1/pjm-v8-n1-p14-p.pdf),
Pacific Journal of Mathematics8(1958),171--176: read the introduction,
definitions2.1--2.9, statements and displayed arguments3.1--3.3, and
Theorem3.4's proof and its compactness corollary. The external KKM/Helly
results used in those arguments were not independently reconstructed.
Section4 was inspected at statement level. The imported Theorem3.4 applies
to the separately continuous convex/concave objectives on compact convex
domains in partial_blocks.md; their spectral brackets give continuity at
the closed scalar endpoints. It does not apply to the two-point nonconvex
model set in the worked counterexample. This is a conventional theorem
application, not an N16 novelty claim.
# Late algebraic and analytic-solution comparison

Codex (GPT-6), October24. Same-model DEVELOPMENT.

- Nie, Ranestad and Sturmfels, [The Algebraic Degree of Semidefinite
  Programming](https://arxiv.org/pdf/math/0611562), v3 September8,2008;
  journal issue2010. Read introduction, section2 through Example4 and the
  genericity qualifications in section3. Their symbolic SDP analysis already
  supplies algebraic solutions through polynomial optimality systems. Their
  generic degree results are not a lower bound for our structured Gram SDP.
  No generic-SDP complexity or algebraic-degree superiority is claimed here.
  Later intersection-theoretic proofs were not reconstructed. Our elementary
  determinant argument gives the particular all-input degree bound in
  [algebraic_endpoints.md](algebraic_endpoints.md), conditional on N16's formula.
- Bousselmi--Hendrickx--Glineur [v3](https://arxiv.org/pdf/2302.08781):
  extended the earlier section3 audit to section4.1.2's Conjectures4.1--4.2,
  Theorem4.3 and Corollary4.4 statements/proof, section4.2.2's Theorem4.8
  proof, and section5's distinctions between analytical, conjectured and
  numerical guarantees. Analytic solutions and explicit extremizers can
  remain useful contributions after an exact SDP is available. This is a
  methodological precedent, not an endorsement of N16 or evidence that its
  formula is novel. The gradient-method scalar reduction is explicitly
  conjectural at its general stated scope in this version; it must not be
  imported as a universal scalar-extremizer theorem.

# Matrix-moment comparison and a localized source defect

Read Curto, Ech-charyfy, Idrissi and Zerouali,
[A Recursive Approach to the Matrix Moment Problem](https://link.springer.com/article/10.1007/s11785-026-02044-x),
published October5,2026; also checked the publisher PDF and arXiv2209.01630v3.
Inspected definitions in section2, Theorem3.8 and its displayed proof,
Proposition3.10, Theorem4.1's Lagrange-polynomial proof, and section4.3.1.
The two-atom weights in equation4.2 are the familiar elementary interval
completion underlying pair_block.md; no novelty is assigned to that step.

Do **not** import Remark4.10's positive-measure iff A>=0 statement as printed
(publisher PDF page16). For A=[-1], the positive measure delta_{-1} has
moments A^n. More generally a real symmetric A has its positive spectral
measure on R, irrespective of eigenvalue signs. The paper's own definition
of positive matrix measure permits support on R. Example3.9(3) also prints
an expression for A^n which gives A, not I, at n=0; reversing its displayed
negative-atom weight fixes that specific example. These are localized
counterexamples, not a judgment that every theorem in the paper fails.
Our new completion proof uses direct Schur identities, not these statements.

Kimsey--Woerdeman2013 was located through its institutional record and
conference abstract. The AMS full-text URL returned403; its theorem proofs
were not inspected and no theorem from it is imported. Searches did not
locate a correction to the above remark; this is not evidence that none exists.
