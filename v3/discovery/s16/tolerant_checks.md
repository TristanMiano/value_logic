# Why exact private checks do not automatically verify approximation tubes

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass36.

The bounded-false-proposal argument in private_repairs.md requires perfect
completeness and a uniform fixed-false-claim error bound. A numerical test of
|f(x)|<=epsilon on private points does not acquire those properties simply
because f is a polynomial of small degree.

## Degree two already defeats a finite-grid tolerance test

Let G be any finite grid in [0,1]. Choose a outside G and let
rho=min_(g in G)|g-a|>0. Fix epsilon>0, choose0<c<epsilon/2 and
0<eta<c*rho^2, and put

    f(x)=epsilon+eta-c*(x-a)^2.

The polynomial is positive throughout [0,1], is at most epsilon at every
grid point, but f(a)>epsilon. Every sampled grid check passes with certainty,
although the all-input tube claim is false. Repetition on that grid does not
fix the problem. Under continuous uniform sampling the violating interval
can have arbitrarily small measure as eta tends to zero, so degree alone
still gives no uniform detection probability. Exact identity testing has a
different zero-set guarantee.

A known Lipschitz constant and a positive violation margin give a detectable
ball, at a dimension-dependent price. But a gap test with accept threshold
epsilon and desired conclusion epsilon+gamma has an intermediate band.
Proposals in that band can generate sample-dependent feedback even when the
relaxed conclusion is true. The deterministic ideal-transcript proof does
not simply ignore these proposals. Their information leakage or their number
must be controlled separately.

## Small false rejections can completely change reuse

For a hidden a uniform in a q-element set, imagine true claims T_b which the
checker rejects exactly when a=b, and false claims F_b accepted exactly when
a=b. Each fixed true claim has false-reject probability1/q and each fixed
false claim false-accept probability1/q. Querying all T_b reveals a after
one rejection, then F_a is accepted falsely with certainty. Thus approximate
completeness cannot be substituted into the earlier unlimited-true-query
claim without an additional error/leakage budget.

## What the existing SOS route does and does not repair

approx_correction.md proposes an exact polynomial identity expressing a
nonnegative tube slack as sums of squares and domain constraints. Private
PIT checks the identity; exact syntax/checking warrants nonnegativity.
This recovers a one-sided statement about CERTIFICATE validity, even though
the desired semantic conclusion is an approximate error tube.

However, an invalid proposed SOS identity may correspond to a perfectly
adequate model/error space. Its rejection does not necessarily reveal a new
error direction. The rank bound from private_repairs.md therefore cannot
pay for arbitrarily many bad certificate proposals. One must separately
bound invalid certificate attempts, use the explicit rejection/error budget,
or provide a sound complete certificate-generation mechanism for the claimed
class. Existence and acquisition of such certificates remain real costs.

This screen preserves the exact private-repair result while preventing an
unjustified extension to noisy numerical models. No large harness is needed
to establish these elementary counterexamples.
