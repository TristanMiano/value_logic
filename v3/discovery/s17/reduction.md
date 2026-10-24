# What a routine reduction would have to establish

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; mathematical comparison.
This is our analysis of the [claim](claim.md), not an assertion that no
uninspected theorem covers it. Source scopes are in [literature](literature.md).

## Known full source versus a retained compression

The [explicit matrix S-lemma reduction](fixed_source.md) is the strongest
fixed-source comparison developed here. It gives the exact reoptimized
upper endpoint, so the common-action/reoptimized-value distinction below
must not be used to dismiss all existing robust optimization results.

The later [Gram SDP reduction](gram_sdp.md) is stronger still: the exact
compressed source/edit problem specializes to known linear-operator
interpolation machinery. The prospective delta is now the explicit scalar
solution and finite attainment/certificate synthesis, not the existence of
an exact tractable formulation or a distinct general reasoning principle.

If W=I and S=C, then M M^T=C^(-1)-I is known. Up to right orthogonal
transformations and zero padding, the norm-bounded perturbation problem is
a conventional fully specified ridge perturbation problem. N16's interior
attainment constructions deliberately use this canonical source. Therefore
their scalar search and rank-one perturbation are especially close to
classical robust least squares; neither is a plausible novelty claim alone.

The compatibility class also contains sources where S does not leave
range(W) invariant. At the parameter boundary, a different compressed
second moment can be essential. The block C fixes W^T S W but only implies

    C^2 <= W^T S^2 W <= C.

The proof must establish that its chosen second moment is realizable without
altering ANY entry of C, and that the same realizable source supports an
edit attaining the optimized value. A generic completion theorem can supply
the realizability ingredient. It does not alone identify the scalar
optimizer or prove the edited ridge normal equation. Whether the combination
is sufficiently substantive for a useful, moderately novel adaptation is
the live contribution judgment; several elementary steps are not automatically
a new contribution.

## Why exchanging min and max is not an acceptable shortcut

For a scalar source M=3, target v=1 and edit radius e=1, N lies in [2,4].
The worst reoptimized value is

    max_N min_x [(1-Nx)^2+x^2]=1/5.

The robust-action problem instead has objective

    min_x [(|1-3x|+|x|)^2+x^2]=2/9,

attained at x=1/3. To verify the latter, on 0<=x<=1/3 the quadratic is
(1-2x)^2+x^2, decreasing up to that boundary; on x>=1/3 it is
(4x-1)^2+x^2, increasing from the boundary; x<0 cannot improve it.
The inequality between these two quantifier orders is strict.

If only the old value C=1/10 is retained and extra output coordinates are
allowed, the proposed upper endpoint becomes (3+sqrt(5))/20, larger than
either number. This further change comes from the source information class,
not a different optimizer for the same scalar data. The proof's boundary
construction, rather than a generic minimax assertion, carries that duty.

## Mapping to quadratic optimal recovery

Treating the unknown object as S makes the observations W^T S W linear,
but the desired quantity after a factor edit is not a fixed quadratic
functional of S. Treating the unknown as M retains an elementary norm ball
for its edit, but the observation constraint becomes nonlinear and the
source is not bounded by one declared ellipsoid. Treating a ridge primal
or dual vector as the unknown yields quadratic functionals, but compatibility
with one common M and its edited N then needs elimination.

These are obstacles to a literal substitution into the inspected quadratic
optimal-recovery theorem. They are not impossibility proofs for a clever
reparameterization. An audit should attempt the coupled source/edit
elimination rather than counting these differing surface forms as novelty.

## What would undermine the bounded contribution

A pre-existing theorem giving the same extrema from C,c,e, including the
hidden-source completion and endpoint attainability, would remove the main
mathematical delta even if its terminology differs. A standard theorem whose
immediate specialization does all that would substantially weaken novelty.
Conversely, merely observing that Young, Jensen and completion are standard
does not establish that the resulting exact information theorem was already
available or valueless. The assessment must explain the explicit remaining
delta and keep its uncertainty in the numerical forecast.
