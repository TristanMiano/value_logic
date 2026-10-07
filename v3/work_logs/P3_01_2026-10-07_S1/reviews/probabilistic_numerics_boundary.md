# P3-01: probabilistic numerics as an ordinary comparison

Researcher: **ChatGPT (GPT-6 Astra Pro)**, principal agent.
Date: October 7, 2026 UTC. Scope: optional primary comparison and elementary
reconstruction within P3-01; no numerical learner or P3-02 result is selected.

## 1. Inspected primary contract

Philipp Hennig, Michael A. Osborne and Mark Girolami,
[*Probabilistic Numerics and Uncertainty in Computations*](https://arxiv.org/pdf/1506.01326v1),
arXiv v1, June 3, 2015, 17-page author postprint; corresponding Proceedings A
471(2179), 20150142 (2015), DOI `10.1098/rspa.2015.0142`.
[Version-pinned HTML](https://arxiv.org/html/1506.01326v1) was also inspected.
The PDF uses section letters and numbered equations such as (2.5); the HTML
uses subsection numbers and renumbers that equation (5). This note uses PDF
locators when an equation number matters.

Selected definitions/arguments: §1, §2(a)–(c), equation (2.5), and §3(a)–(d).
The framework places a joint model on a deterministic target and results of
accessible computations, then supplies a rule choosing further computations.
The quadrature example conditions a Gaussian-process prior on function values.
Its posterior mean can reproduce a classical rule while uncertainty still
depends on model parameters. The paper discusses acquisition, prior mismatch,
model-selection overhead and propagating uncertainty through computational
pipelines. These are existing comparison ideas, not value-logic novelties.

No empirical performance result, convergence theorem, universal runtime bound
or claim about the whole field in 2026 is imported. The source's views about
probability being uniquely suited to uncertainty are not adopted as a premise
of this open-carrier project.

## 2. Direct scale reconstruction, independent of a particular integrand

Consider a finite, jointly Gaussian model for an unknown scalar `Z` and an
observation vector `Y`. Fix their means `m_z,m_y`. For each positive `s`, let
the covariance be

$$
s^2\begin{pmatrix}k&q^\mathsf{T}\\q&K\end{pmatrix},
$$

where `K` is positive definite and the whole block is positive semidefinite.
Condition on the same exact observation `Y=y`. The Gaussian conditional has

$$
m_{Z|y}=m_z+(s^2q^\mathsf{T})(s^2K)^{-1}(y-m_y)
=m_z+q^\mathsf{T}K^{-1}(y-m_y),
$$

and

$$
v_{Z|y}=s^2k-(s^2q^\mathsf{T})(s^2K)^{-1}(s^2q)
=s^2\bigl(k-q^\mathsf{T}K^{-1}q\bigr).
$$

Thus changing this common covariance scale leaves the posterior mean unchanged
while scaling its variance. The assumptions are essential: input locations,
mean, covariance shape and exact observation model are fixed; a separate
unscaled observation-noise covariance or changed hyperparameter-selection rule
can alter the mean. This is a standard Gaussian-conditioning identity, not
a new probabilistic-numerics result.

The two posteriors need not have equal marginal likelihoods for `y`. We are
not claiming that their evidence is statistically indistinguishable under
every analysis. A method can estimate or select the scale, with its procedure,
data and cost specified. The narrower statement is that identical point
estimates do not determine a unique uncertainty model or validate its scale.

## 3. Same estimate, different modeled value of computation

Under squared-error task loss with real-valued reports, reporting the posterior mean has modeled
expected loss equal to the posterior variance. For the following two distinct
positive variances, assume `k-q^T K^-1 q > 0`; the scale identity still holds
when this quantity is zero, but then every scaled conditional variance is
zero and the decision separator is absent. Suppose a guaranteed exact
computation, available to both methods, costs `1/10` in the same total-loss
unit. If the posterior variance is `1/100`, retaining the approximate result
has smaller modeled cost; if it is one, buying the exact computation has
smaller modeled cost. The report, observed data and available action can be
the same while the assumed uncertainty scale changes the decision.

This is an explicitly stipulated decision diagnostic. It does not establish
which posterior is adequate for a fixed mathematical instance or that the
exact computation is available at this cost in any real problem. Gaussian
squared loss is unbounded, although its expectation is finite here. No bounded
online-learning or LI loss theorem is inferred from this example. A clipped
or bounded variant would need its own payoff calculation.

The lesson for Q1/Q4 is concrete: an implementation must identify which of
the following it has produced:

- A point estimate.
- A probability distribution or error estimate under a declared model.
- A proved bound under named analytic assumptions.
- A statistical coverage statement for a specified population and selection
  process.

These can support different decisions and transport rules. A value expression
can represent each, but its type and evidence are still necessary. An ordinary
probabilistic or verified numerical method can represent them too.

## 4. Source code and selection remain information, not free truth

The paper explicitly notes in §2(c) that source code may reveal assumptions
useful for tailoring a numerical method. A black-box evaluation model and a
model with inspectable source code therefore have different access contracts.
P3-01 requires the same legitimate access terms for its methods, including
cheap source inspection. A prior over functions need not use all information
in a supplied program; omitting that information is a modeling choice, not a
proof that the deterministic answer is intrinsically random.

The model's acquisition rule also uses its assumed uncertainty. More informative
computations are valuable according to a joint model and objective, and their
selection has overhead. The source's §3(c) flags adaptive-selection and
exploration issues. Its §3(d) already proposes communicating uncertainty across
computational pipelines to control numerical effort. P3-N01 therefore cannot
claim that generic idea as its delta. A useful restricted connection to checked
logical evidence and revision could still be a formal adaptation or application,
provided its added service and assumptions are supported.

## 5. An illustrative normalization is not imported

The inspected PDF's equation (2.3) uses
`k(x,x')=c(1+b-(b/3)|x-x'|)` on `[-3,3]`; equation (2.4) displays the double
integral of this kernel as `c(1+b/3)`, for the unnormalized integral defined
in (2.1). Direct integration instead gives

$$
\int_{-3}^{3}\!\int_{-3}^{3}|x-x'|\,dx\,dx'=72,
$$

so the covariance integral under those displayed conventions is

$$
36c(1+b)-24cb=36c(1+b/3).
$$

The smaller expression would be the variance of the average integral `F/6`.
This is a local normalization discrepancy in the inspected version, not an
independently established publication erratum or a novelty claim. We do not
use its printed scalar constant. The general conditioning formula and the
scale identity above suffice for our comparison. No source equation or external
repository was edited, and no claim is made that this affects the paper's
experiments or broader results.

## 6. Retrieval and verification limits

PMC returned a browser-check page; an MPI author-PDF route returned HTTP 403.
The arXiv v1 HTML and PDF supplied the inspected content. The PDF equation was
also requested as a page screenshot; the reconstruction does not rely on a
numerical experiment or on importing the illustrative normalization.

The scale and integration calculations are principal derivations, separately
reconstructed in the same-model internal
[review](probabilistic_numerics_reconstruction.md). They are not entries
in `finite_checks_1.json` and are not independent external validation. Their
resource time belongs only to the observed principal mode segments; no new
time credit is created by this note.
