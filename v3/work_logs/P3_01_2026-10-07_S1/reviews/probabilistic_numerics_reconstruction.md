# P3-01 probabilistic numerics: bounded reconstruction

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal sub-agent**.
Date: 2026-10-07 UTC. Nonblind internal review, not external validation.
Own resource time is unmeasured; zero concurrent principal-clock credit.
Scope: [probabilistic_numerics_boundary.md](probabilistic_numerics_boundary.md),
its Gaussian scale argument, two-action decision diagnostic and local integral
calculation. No canonical edits, experiment, new algorithm or P3-02 execution.

**Finding:** the calculations are correct under the stated model. One small
missing qualification matters to the nontrivial decision example: its Schur
complement must be positive. The general scale identity also permits zero
posterior variance, which cannot be changed by scaling.

## Gaussian reconstruction and observation scope

Put `r = k-q^T K^-1 q`. Positive definiteness of `K` makes its inverse
well-defined, and positive semidefiniteness of the full block implies `r>=0`.
For `s>0`, `(s^2 K)^-1=s^-2 K^-1`. Substituting this into the usual finite
Gaussian conditional gives the note's unchanged mean and variance `s^2 r`.
The covariance term subtracted from `s^2 k` has scale `s^2`, not `s^4`.
These are elementary conditioning and matrix identities.

Exact conditioning on a continuous `Y=y` uses the Gaussian regular conditional
distribution, not division by the probability of a singleton event. With
positive-definite `K`, its usual density formula supplies the claimed
conditional for every finite `y`. This is an idealized mathematical information
contract, not a claim that arbitrary real numbers can be observed or computed
exactly by finite code for free.

**Recommended clarification:** require `r>0` when using scaling to obtain the
distinct variances in the paid-decision example. A concrete consistency witness
is `K=1`, `q=1`, `k=2` and zero means. Equivalently, under each model let
`Y` and `E` be independent centered Gaussians with variance `s^2`, and set
`Z=Y+E`. Observing the same `Y=y` yields mean `y` and variance `s^2`;
`s=1/10` and `s=1` supply exactly the two variances in the note.

The crucial scope is common scaling of the **whole** joint covariance with
fixed means, shape, locations and data. With independent observation noise
of fixed covariance `R`, the mean generally instead contains
`s^2 q^T (s^2 K+R)^-1`, whose scale need not cancel. Conversely, noisy models
whose entire joint covariance, including the noise, shares the scale may
retain the identity. Thus noiseless observation is a sufficient setup here,
not a theorem that every noisy model destroys invariance. The note correctly
allows marginal likelihoods and scale-selection procedures to differ.

## Paid squared-error choice

For posterior mean `mu` and variance `v`, reporting any scalar `a` has modeled
expected squared loss `v+(a-mu)^2`. Therefore reporting `mu` costs `v` under
that model. Buying the stipulated exact result and then reporting it costs
`1/10` and leaves zero squared error. Hence `1/100<1/10<1` gives the two
claimed preferences. No clipping, bounded-loss theorem or empirical result
is needed for that finite comparison.

The comparison assumes the exact result arrives before the final decision,
its purchase price is in the same additive total-loss units, and other costs
are common, sunk or included. It compares the two stated options; it does not
prove optimality over unlisted computations. Different scales describe
different epistemic models, not different actual errors of the same point
estimate on one fixed target. The draft already labels model adequacy and
real availability of the exact action as unestablished; preserve that scope.

## Integral normalization check

Reopened the primary [arXiv v1 PDF](https://arxiv.org/pdf/1506.01326v1) and
[version-pinned HTML](https://arxiv.org/html/1506.01326v1). Visually inspected
PDF page 4 (zero-based page 3), equations (2.1), (2.3)–(2.5). The displayed
target is the unnormalized integral over `[-3,3]`; the kernel and scalar
constant are as transcribed in the principal note.

Directly, symmetry gives

$$
\int_{-3}^{3}\int_{-3}^{3}|x-x'|\,dx'\,dx
=2\int_{-3}^{3}\int_{-3}^{x}(x-x')\,dx'\,dx
=\int_{-3}^{3}(x+3)^2\,dx=72.
$$

The square's area is 36, so integrating the stated kernel gives
`36c(1+b)-(b/3)c*72 = 36c(1+b/3)`. Dividing the target by six divides its
variance by 36 and yields the smaller displayed constant. This independently
confirms the **local normalization discrepancy under the inspected conventions**.
It is not evidence of an acknowledged publication erratum or of an effect on
the paper's code, experiments or other results. No such further claim was
investigated or is needed.

## Warrant boundary

The current CB03 already requires jointly applicable bounds and preserves
population, probability and selection scope. This review exposes no new
defect in it. A positive Gaussian posterior variance is a model-conditional
expected squared error, not a deterministic absolute-error bound or automatic
coverage over arbitrary fixed integrands. The principal note's four-way typing
already records the needed distinction. Substituting posterior standard
deviation for CB03's justified `epsilon` would require a separate justified
bridge, but the present draft makes no such substitution.

Verification consists of direct reconstruction and selected primary-page
inspection. No test suite was run, no assertion count increased, and no
scientific-support or task-completion disposition changed.
