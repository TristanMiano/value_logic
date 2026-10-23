# Approximate error skeleton: conditioning is part of the receipt

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 32.

The [exact skeleton](error_skeleton.md) assumes the whole error vector lies
in a learned subspace. This extension explicitly pays for approximate membership
and anchor noise; it does not infer a uniform approximation from a few samples.

Let U be an n by d matrix with orthonormal columns, 0<d<n. Select distinct
coordinate rows J, with A=U_J full column rank and sigma=sigma_min(A)>0.
Write a true model error F=Uc+r with U^T r=0 and ||r||_2<=epsilon. The
observed exact-minus-model anchors are F_J+e, ||e||_2<=nu. Correct by

    Fhat = U A^dagger (F_J+e).

Then

    ||F-Fhat||_2 <= [epsilon^2 +
       (epsilon sqrt(sigma^(-2)-1) + nu/sigma)^2]^(1/2).       (1)

For noiseless anchors this is epsilon/sigma. It is not merely epsilon.
The bound is sharp over errors and anchor noise for these U,J whenever
the indicated complementary direction exists (in particular sigma<1).
For sigma=1 a nonzero orthogonal complement and available U-aligned anchor
noise give the corresponding sqrt(epsilon^2+nu^2) endpoint.

Proof: the residual is r-U A^dagger(R_J r+e), whose two terms are orthogonal.
Since R_J R_J^T=I and A^dagger A=I,

    [A^dagger R_J (I-UU^T)] [same]^T = (A^T A)^(-1)-I.

Its norm is sqrt(sigma^(-2)-1), and ||A^dagger||=1/sigma. The top
singular vectors can align the two coefficient errors. This proves (1)
and the stated sharpness. Rank deficiency admits an unobserved U direction
of arbitrarily large magnitude, so no analogous finite bound is possible.

If corrected action values have Euclidean error at most B from (1), choosing
their minimum has regret at most sqrt(2) B. A corrected margin exceeding
sqrt(2) B certifies the same unique minimizer. These are all-input claims
only when the subspace residual and anchor-noise bounds themselves are
all-input warrants; otherwise retain their exact probability/domain scope.

For rank one, selecting k equally priced anchors with the largest |U_i|
maximizes sigma. For uniform U_i=1/sqrt(n), sigma=sqrt(k/n), so noiseless
error amplification is sqrt(n/k). More anchors trade exact-output cost for
conditioning. With unequal costs this becomes a subset acquisition problem;
there is no free guarantee that a small convenient anchor set is adequate.

Acquiring U, proving epsilon, finding J, factoring A, checking anchor truth,
and applying the correction all belong in the invoice. Generic gappy POD,
interpolative approximation and oblique-projection bounds are direct ordinary
comparators. This is an extension candidate, not a novelty or measured-saving
claim. The exact polynomial membership certificate from pass 28 does not
automatically certify approximate membership from noisy observations.
Primary-source screen: Peherstorfer, Drmac and Gugercin (2020), section 4.1,
equation 17, directly matches the noiseless bound. See [read scopes](literature.md).
Reject generic interpolation/oversampling novelty at this stage.
