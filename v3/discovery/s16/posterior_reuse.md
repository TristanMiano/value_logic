# Retained uncertainty and a warrant to keep using an old predictor

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass29.
Same-model derivation. Bayesian conditioning, ridge perturbation and
goal-oriented covariance approximation are existing subjects.

## A natural interface for the numerical receipts

In a finite linear-Gaussian model, theta~N(0,I), y=M^T theta+noise with
independent noise~N(0,I). Conditional on a fixed M and observed y,

    S_M=(I+MM^T)^-1,    mu_M=S_M M y.

For an orthonormal target map W, the retained block C=W^T S_M W is the
posterior covariance of W^T theta. This is precisely the response receipt
already studied. Goal-oriented Bayesian inversion already works with such
blocks; retaining only relevant uncertainty is not new. The new mathematical
question is what follows after only that block, small scalar metadata and a
justified design-change bound ||N-M||op<=e remain available.

The existing envelopes apply to the covariance under each specified N.
They do not alone describe a posterior that mixes over uncertain N.
For a sharp failure example, take scalar M=0 and equiprobable alternatives
N=+e and N=-e. Their likelihoods of y are equal and each conditional variance
is1/(1+e^2), but their posterior means are opposite. The mixture variance is

    1/(1+e^2) + e^2*y^2/(1+e^2)^2,

which is unbounded as |y| grows. A covariance-only bound of1 would therefore
fail for model-mixture uncertainty. Actual model adequacy is also not supplied
by Gaussian algebra or an old numerical receipt.

## A data-specific mean transport bound

Retain one additional old value

    r_M = min_x [||y-M^T x||^2+||x||^2]
        = y^T(I+M^T M)^-1 y.

Let r=y-M^T mu_M, so ||r||^2+||mu_M||^2=r_M. Write Delta=N-M.
The normal equations give the exact identity

    mu_N-mu_M = S_N [Delta*r - N*Delta^T*mu_M].        (1)

The block row S_N^(1/2)[I,-N] has operator norm1, since its product with
its transpose is I. Hence

    ||mu_N-mu_M||_(S_N^-1)^2
       <= ||Delta*r||^2+||Delta^T*mu_M||^2
       <= e^2*r_M.                                  (2)

Equivalently,

    (mu_N-mu_M)(mu_N-mu_M)^T <= e^2*r_M*S_N.          (3)

This is a deterministic least-squares statement. In particular, the excess
new ridge objective of the OLD optimizer is at most e^2 times the old optimal
objective. It addresses a deployment duty omitted by merely bounding the
new optimum's value. It does not identify the new optimizer for free.

The coefficient1 in (2) cannot be uniformly reduced. With scalar M=t,
N=t+e and y=1, the ratio of the left side to e^2*r_M is

    (1-t^2-t*e)^2 / [(1+t^2)*(1+(t+e)^2)] -> 1

as t tends to infinity, for every fixed e>0. This is sharpness of this
uniform inequality, not a new claim about the closest perturbation literature.

## Consequences for continued reliance and model mixtures

For any unit target v, let f_N=v^T S_N v and a^2=e^2*r_M. Conditional on
the specified Gaussian model N and y,

    E[(v^T theta-v^T mu_M)^2 | y,N] <= (1+a^2)*f_N.    (4)

The optimal conditional mean has risk f_N. Thus the retained predictor's
conditional squared-error risk is at most1+a^2 times that optimum. For
example, the premises e=.1 and r_M=4 imply at most4% excess risk. This is
an analytic conditional guarantee, not a measured forecast or audit saving.

More generally, suppose N is itself latent, every conditional model uses
the stated common prior/noise law, and its posterior support is contained
in the edit ball. The law of total covariance and (3) imply

    Cov(theta | y) <= (1+a^2)*E[S_N | y].              (5)

Indeed covariance of the conditional means is bounded by their squared
deviations from the common anchor mu_M. No probability distribution over N
is needed to evaluate this upper bound; its support premise is needed.

For any valid simultaneous upper matrix U(C) from operator_receipt.md,
W^T S_N W<=U(C) for every allowed N. Thus the mixture covariance is at most
(1+a^2)U(C), and the old projected mean can be retained using only

    (C, W^T mu_M, r_M, source shape, edit warrant).

This is k(k+1)/2+k+1 numerical scalars beyond the target map and metadata.
Acquiring/checking those scalars, the target map and the edit warrant is paid.
If a dense W is necessary its n*k storage must be counted; coordinate or
otherwise implicit targets are the favorable case. An ordinary method using
the same receipts implements the same result and ties.

## A uniform conditional credible region

Let C_N=W^T S_N W and d_N=W^T(mu_N-mu_M). Equation(3) implies
d_N^T C_N^-1 d_N<=a^2. With U>=C_N positive definite, a component's
U-standardized prediction error can be coupled as A^(1/2)(g+h), where
||A^(1/2)||op<=1, g is standard k-dimensional Gaussian and ||h||<=a.
Therefore a conservative region with conditional probability at least1-delta is

    ||U^-1/2 (W^T theta-W^T mu_M)||
        <= a + sqrt(chi_square_quantile(k,1-delta)).   (6)

The noncentral chi-square quantile with noncentrality a^2 gives a tighter
radius by the same coupling. The same coverage holds for every mixture over
allowed N because it holds componentwise. This is a Bayesian conditional
model statement, not distribution-free coverage for arbitrary real systems.
It covers adaptive linear target choices within W through one common region.
Different values of the envelope parameter may be chosen from retained data
before evaluating (6); every valid U is pointwise uniform over the edit ball.

## An unfinished old solve can still be used

For an approximate old vector x, define its actual objective
r_x=||y-M^T x||^2+||x||^2 and normal-equation residual
g_M=(I+MM^T)x-My. If ||g_M||<=beta is checked, the same block-row argument,
with the extra term -S_N g_M, gives

    ||mu_N-x||_(S_N^-1) <= beta+e*sqrt(r_x).           (7)

Use a=beta+e*sqrt(r_x) in (3)–(6). Thus a stopped computation has an explicit
remaining-error price; it need not be misreported as an exact solution.
Sharper residual metrics can replace the Euclidean beta when independently
warranted. Rounded covariance receipts require their own outward bounds.

This candidate links bounded numerical work, a fallible retained predictor,
counterfactual design changes and typed probabilistic conclusions. Its generic
ingredients are conventional. The particular retained-information guarantee,
sharp uniform coefficient, acquisition economics and closest existing
perturbation formulations need comparison before a novelty or promotion claim.
