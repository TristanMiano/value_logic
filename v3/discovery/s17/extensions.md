# Separate extension register

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT. None of these extensions
is necessary for the [bounded contribution event](claim.md).

## Smaller endpoint witnesses (new derivation, not a novelty assertion)

The 2k-dimensional dilation in [the reconstructed proof](proof.md) suffices
for the core event. For a single target, a one-coordinate extension already
adjusts its second moment. Let H=I-C, Q=c^T C H c>0 and
tau=(m_star-c^T C^2c)/Q in [0,1). Define

    b=sqrt(tau) C H c/sqrt(Q),
    S=[[C,b],[b^T,1-b^T H^(-1)b]].                    (E1)

Then b^T(CH)^(-1)b=tau, so the Schur complement of C in S is
1-tau>0. Also

    I-S = [I;-b^T H^(-1)] H [I,-H^(-1)b] >= 0,        (E2)

of rank k. Thus 0<S<=I, its compression is C and its target second moment
is c^T C^2c+(c^T b)^2=m_star. A finite n=k+1 by p=k source exists:
factor S^(-1)-I, which has rank k. The endpoint normal-equation arguments
depend only on that second moment and remain valid. Canonical interior and
zero-endpoint sources use n=p=k. Padding with zero rows/columns and rotating
the target basis preserves the construction.

Consequently the same scalar endpoint theorem appears to hold for every
fixed n>=k+1 and p>=k, with any specified isometry W. The case n=k can
differ, as the scalar M=3 example shows. This improves the witness size
and the interpretation of the dimension-unrestricted contract. It is an
elementary rank-one completion consequence, not separately forecast as a
moderately novel contribution. Direct substitution checks E1–E2: because
C and H commute, H^(-1)+C^(-1)=(CH)^(-1), and
b^T(CH)^(-1)b=tau. Also (c^T b)^2=tau Q. Thus both Schur complements,
the rank and the required moment follow without a numerical square root.
This is a same-model algebraic check. The core assessment continues to use
the reconstructed 2k witness instead.

### Resulting fixed-shape classification (separate development claim)

For any specified n>=k and p, strict C<I forces p>=k: the rank of
W^T(I-S)W=I-C is k, whereas rank(I-S)=rank(M)<=p. Conversely p>=k
permits compatible sources by padding the canonical k-by-k source.

If n>=k+1 and p>=k, E1 realizes every needed cap moment; the interior
and cancellation constructions also fit after padding. Orthogonal output
rotation carries the canonical target subspace to any specified isometry W.
Therefore both core endpoints are attained at every such fixed shape.

If n=k and p>=k, W is square orthogonal and C determines the full S up
to that known basis change. The [fixed-source formulas](fixed_source.md)
apply, including t below the cap when its denominator permits it. Those
endpoints can differ from the unrestricted-information endpoints. The
M=3, e=1 example explicitly shows the difference at k=n=p=1.

This resolves a useful shape ambiguity without claiming that generic
completion, rank arguments or the fully known-source formulas are novel.
It is not added as a prerequisite to N16-C/v1's readiness event, and has
not received independent confirmation.

## Other preserved routes

Fixed smaller shapes, boundary eigenvalues, simultaneous matrix extrema,
shared edit budgets, task-specific value queries, quadratic/nonquadratic
solution reuse and private-check/public-repair mechanisms retain their s16
development records. They will be compared in the 40-hour portfolio review.
Their metrics and unassessed forecasts do not inflate the core N16 estimate.
