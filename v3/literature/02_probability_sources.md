# P3-02 — probability, expectation and information comparisons

Contributor: **ChatGPT (GPT-6 Astra Pro)**, with internal same-model, nonblind
source reconstruction. Accessed October 7, 2026 UTC. This is a targeted import
record for [the probability-information derivation](../derivations/02_probability_information.md),
not a worldwide priority review. The P3-01 source record is preserved.

## P02-S1 — finite coherent expectations (inherited S13, reopened)

Halpern and Pucella, **Characterizing and Reasoning about Probabilistic and
Non-Probabilistic Expectation**, 2007 author manuscript,
[PDF](https://www.cs.cornell.edu/home/halpern/papers/expectation.pdf).
Inspected §§2.1–2.2, Proposition 2.1, Theorems 2.2/2.4, and their finite-domain
qualification; P3-01 already records Example 2.11 and the expressiveness result.

The finite all-gamble functional determines a law when it is additive,
affinely homogeneous and monotone. Super/subadditive, positively affinely
homogeneous and monotone analogues instead represent lower/upper expectations.
The affine condition includes correct treatment of constant translations. Their canonical
closed convex probability set is determined by all such gamble bounds;
an arbitrary generating family is not unique. A restricted list of gamble
values is less information than the whole functional. The principal note's
indicator and convex-hull proofs reconstruct the finite case, while its
retained-query criteria also use phase-two information-recovery arguments.
No infinite-domain theorem without continuity hypotheses is imported.

## P02-S2 — proper scoring (inherited S02, reopened)

Gneiting and Raftery, **Strictly Proper Scoring Rules, Prediction, and
Estimation**, JASA 102(477), 359–378, 2007,
[author PDF](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf).
Inspected §1 definition, §2.1 equation (2), §3.1 Definition 2/Theorem 2 (McCarthy–Savage
representation), and Examples 1–3 on printed pp.362–363.

The paper uses rewards; the principal note negates them to obtain losses.
Strict propriety identifies the unique optimal **report** under one fixed
outcome law. It does not by itself guarantee law recovery from one scalar risk,
learned accuracy, or validity under a report-induced outcome law. Brier
and logarithmic examples are reconstructed directly. The finite
score-difference span lemma is an elementary consequence of strict propriety
and finite linear algebra; no separate numbered antecedent was located in
the selected reading, and that does not establish novelty. Boundary log
reports can have infinite losses; only finite positive-report probes enter
the finite matrix argument.

## P02-S3 — dimension and identifiable elicitation

Frongillo and Kash, **On Elicitation Complexity**, 2015,
[author PDF](https://raf.prof/media/papers/elic-complex.pdf).
Inspected §2 Definitions 1–7, §2.1 Proposition 2/Lemma 1, and the corresponding
appendix construction. The source assumes a convex distribution family.

The paper distinguishes a scalar property from the dimension of an
elicitable/identifiable intermediate report. For a linear expectation
property, Lemma 1 gives the affine dimension of its range under the stated
identifiable-elicitation class. Definition 7 explains why unrestricted real
encodings defeat unqualified coordinate-count lower bounds. This is an
established strong comparator for recovering task information without an
entire law. Its elicitation complexity is not automatically our fixed
measurement-menu cost, bit count, statistical sample size or decoder runtime.
The principal note proves its own finite retained-measurement statements.

## P02-S4 — scoring linear properties directly

Abernethy and Frongillo, **A Characterization of Scoring Rules for Linear
Properties**, COLT/PMLR 23, 27.1–27.13, 2012,
[primary proceedings PDF](https://proceedings.mlr.press/v23/abernethy12/abernethy12.pdf).
Inspected §3's outcome/report domains and §4 equations (6)–(7), Lemma 7.

The Bregman construction scores an expected vector-valued feature directly.
Thus a strong ordinary method need not reconstruct all probabilities before
predicting task losses. The inspected PDF's Definition 2 is in minimization
orientation, whereas (6)–(7) and the following text maximize their displayed
score. We use the explicit formula, reverse its sign consistently when
needed, and prove the squared-loss specialization independently. This is a
local reading qualification, not a claim to have established a published
erratum or audited the paper's entire characterization theorem.

## P02-S5 — ordinary convex geometry and LP certificates

Boyd and Vandenberghe, **Convex Optimization**, original author lecture
[slides](https://web.stanford.edu/~boyd/cvxbook/bv_cvxslides_original.pdf), linked
from the [book page](https://web.stanford.edu/~boyd/cvxbook/).
Inspected slides 2–19 (PDF p.34), 5–9 through 5–12 (PDF pp.125–128): separating
hyperplanes, the standard-form LP dual, weak/strong duality, and linear-constraint
refinement of strict feasibility.

The finite polyhedral fibers used for our LP certificates are nonempty and
compact, so linear
objectives attain finite extrema and ordinary LP duality supplies matching
certificates. The note proves certificate soundness directly by multiplying
the constraints, and labels sharpness as the standard LP consequence. No
generic Slater interior assumption is imposed on a boundary-only law fiber.
The full book PDF failed twice (initial open and the book page's actual link);
the linked original slides succeeded. The book itself is not claimed read.

## P02-S6 — calibrated decisions and nonlinear report dimension

Ramaswamy and Agarwal, **Convex Calibration Dimension for Multiclass Loss
Matrices**, JMLR 17, 2016,
[primary PDF](https://jmlr.org/papers/volume17/14-316/14-316.pdf).
Inspected §2.3, Definitions 1/4/5, Theorems 6/12, Example 8 and §4.3.

Their matrices use outcome rows and action columns; ours transpose that
orientation. The source removes actions never uniquely optimal. Its trigger
sets are Bayes-action regions; calibration requires each surrogate optimality
set to fit inside a region. For quadratic expectation reports, those sets
are precisely our observation fibers. This directly anticipates the
common-optimum criterion. Our essential-row iff is a finite reconstruction,
not an imported general calibration lower bound. Ordinal absolute loss has
a one-dimensional convex surrogate despite requiring more fixed linear
expectation coordinates in our service. The optimized median is a nonlinear
property of the law. Neither report dimension nor exact recovery alone is a
complete computational or statistical comparison.

## P02-S7 — ordinary low-rank expectation codes

Ramaswamy, Agarwal and Tewari, **Convex Calibrated Surrogates for Low-Rank
Loss Matrices with Applications to Subset Ranking Losses**, NeurIPS 2013,
[primary proceedings PDF](https://proceedings.neurips.cc/paper_files/paper/2013/file/a5cdd4aa0048b187f7182f1b9ce7a6a7-Paper.pdf).
Inspected Theorem 3 and its proof, printed pp.3–4.

The source factors an action loss through a low-dimensional outcome-feature
vector, learns its expectation by squared loss, and decodes by linear action
scores. This is a direct strong ordinary comparator for task-specific value
prediction. The principal note reconstructs a finite decoder-regret inequality
and allows a common state-dependent baseline to cancel in expected-cost
comparisons. No learner, convergence rate, sample access or resource budget is
supplied merely by this algebraic factorization.

## P02-S8 — ordinary linear-fractional optimization

Charnes and Cooper, **Programming with Linear Fractional Functionals**,
Naval Research Logistics Quarterly 9, 181–186, 1962,
[author-archive scan](https://iiif.library.cmu.edu/file/Cooper_box00010_fld00009_bdl0001_doc0001/Cooper_box00010_fld00009_bdl0001_doc0001.pdf),
[publisher record](https://onlinelibrary.wiley.com/doi/10.1002/nav.3800090303).
Inspected the introduction and “General Linear Fractional Models,” printed
pp.182–184: equations (2.1)–(3), Lemma 1, Theorem 1 and the positive-denominator
branch of (4.1). The archived scan has imperfect OCR.

The reciprocal-denominator substitution gives an ordinary LP. Our note
reconstructs a positive-margin probability-polytope specialization and its
inverse explicitly. It does not import the source's complete treatment of
sign-changing or vanishing denominators, nor infer a uniform stability bound
from exact fractional-program equivalence. The threshold form is directly
an affine inequality when its denominator is known positive.

## P02-S9 — information-based complexity and noisy optimal recovery

Foucart and Liao, **Radius of Information for Two Intersected Centered
Hyperellipsoids and Implications in Optimal Recovery from Inaccurate Data**,
2024 author manuscript,
[PDF](https://foucart.github.io/publi/OR_L1Noise_v3.pdf),
[arXiv record](https://arxiv.org/abs/2401.11112).
Inspected §1 (printed pp.1–3), the premises and statement of §2.1 Theorem 1,
and §3.2 equations (22)–(25), printed pp.11–12.

The source explicitly separates model set, observation map, target quantity,
recovery map and global worst-case information radius. Computational feasibility
is not assumed merely by defining a recovery map. Noisy observations use a
joint object/error representation. These are strong ordinary antecedents for
our information contract. Its main linear-recovery theorem concerns Hilbert
spaces and two centered hyperellipsoids; we do not apply that theorem to an
arbitrary probability simplex or vector norm. Our scalar polytope/affine
comparison is reconstructed directly with LP duality. No Gaussian risk or
statistical learning guarantee is imported.

## P02-S10 — local radius and multivalued observation relations

Osipenko, **Optimal Recovery of Linear Functionals and Operators**,
Communication on Applied Mathematics and Computation 30(4), 459–482, 2016,
[primary paper](https://www.rstu.ru/proc/pdf/paperOs.pdf).
Inspected the introduction's exact-information definitions and stated
Smolyak Theorem 1 (printed p.461), plus §3 (pp.466–468): multivalued
observations, feasible inverse images and local/global information radii.

The compact-convex affine comparator has a direct route from that stated
symmetric-source scalar theorem, using the homogenization shown in principal
§15. The principal also proves it by finite LP duality and compactness.
The original 1965 work is not claimed read. We do not import §3's more general
symmetric-hull criterion or the analytic-function examples. This is ordinary
optimal-recovery ancestry, not a new general estimation theory.

An additional lead, Donoho's **Statistical Estimation and Optimal Recovery**,
was opened at its Stanford author PDF, but that retrieval supplied no text
lines. No theorem from that paper is claimed inspected or imported here.
The accessible deterministic sources above suffice for this scoped comparison.

## P02-I1 — phase-two retention and coherent recovery

The primary inherited record is [paper §7](../../paper_v2.md#7-what-must-survive-a-cost-revision),
with [price revision §§3–8](../../v2/derivations/09_c4_price_revision.md) and
[coherent recovery §§1–7,10](../../v2/derivations/10_f16_coherent_recovery.md).
The normalized-simplex kernel argument, rank-based repair, small-edit stability
and compatible-estimate distinction are already explicit there. The generic
midpoint/compatible-center solver is also explicit in
[F16 reconstruction §15](../../v2/work_logs/F16_2026-10-05_S1/root_reconstruction.md)
and [ordinary comparison §6](../../v2/derivations/07_adversarial_review.md).
The [noisy-source boundary](../../v2/work_logs/F16_2026-10-05_S1/source_uncertainty_boundary.md)
already supplies related simplex coherence gaps. Their reset
procedure hypotheses and equal-price envelope result remain unchanged.
P3-02 generalizes the *presentation of the service contract* and reconstructs
the generic finite algebra; it does not rename those inherited proofs as new
results. Its generic coherence counterexample explains why F16's special
equality cannot be inferred merely from convexity or a full observation fiber.

## Internal reconstruction and disposition

The [scoring review](../work_logs/P3_02_2026-10-07_S1/reviews/scoring_sources.md),
[finite proof review](../work_logs/P3_02_2026-10-07_S1/reviews/finite_recovery.md)
and [retention review](../work_logs/P3_02_2026-10-07_S1/reviews/retention_bridge.md)
contain longer mathematical reconstructions, selected examples and original
reading boundaries. The principal reopened the new external sources used in
the canonical comparison. Reviewers and principal share one model family;
this is internal checking, not external peer review. Their overlapping work
does not add principal-clock research credit.

The later [score-span review](../work_logs/P3_02_2026-10-07_S1/reviews/scoring_span_review.md),
[decision comparison](../work_logs/P3_02_2026-10-07_S1/reviews/decision_source_comparison.md),
[payoff projection](../work_logs/P3_02_2026-10-07_S1/reviews/payoff_uncertainty_projection.md)
and [source audit](../work_logs/P3_02_2026-10-07_S1/reviews/principal_source_audit.md)
record additional qualifications and the snapshots actually reviewed.

The final same-task refinements use direct finite arguments, with explicit
internal reviews of [calibrated target repair](../work_logs/P3_02_2026-10-07_S1/reviews/calibrated_repair_review.md),
[bounded and restricted queries](../work_logs/P3_02_2026-10-07_S1/reviews/calibrated_repair_scope.md),
[calibrated one-action information](../work_logs/P3_02_2026-10-07_S1/reviews/calibrated_decision_review.md),
[coefficient alphabets and approximation](../work_logs/P3_02_2026-10-07_S1/reviews/coefficient_alphabet_boundary.md),
and [nonlinear units/outcome stakes](../work_logs/P3_02_2026-10-07_S1/reviews/nonlinear_unit_boundaries.md).
Their row-space, quotient, interpolation and positive-cone arguments are
proved in the principal note. No separately numbered external antecedent,
new primary-source inspection or priority finding is claimed for those
combined formulations. The [final comparison review](../work_logs/P3_02_2026-10-07_S1/reviews/final_comparison_scope.md)
and [principal mathematical reconciliation](../work_logs/P3_02_2026-10-07_S1/reviews/principal_final_mathematics_review.md)
separate that content from the inherited methods and from the narrower
implemented certificate service.

The sources provide strong ordinary implementations of the finite expectation,
property and decision services studied here. P3-02 records a scoped reconstruction
and synthesis of their information requirements, including explicit calibration,
conditional-target and payoff-uncertainty cases. No exclusive capability,
learning duty or resource advantage over that combination has been established.
The finite information-audit interface is a narrower candidate for assessment
under the author's synthesis/adaptation criterion. Ordinary antecedents do not
by themselves rule out such a useful adaptation; merely listing those ingredients
would not establish it either. This source record supplies no change to the
existing phase-wide P3-N01 disposition, **NOT YET SUPPORTED**, or to any gate.
