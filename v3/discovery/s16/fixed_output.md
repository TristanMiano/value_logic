# When the retained block covers every output direction

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass38.
Same-model derivation; regularized total least squares and scalar quadratic
duals are conventional comparisons. Exact formulation novelty is unassessed.

Write F(M;v)=v^T(I+MM^T)^(-1)v, ||v||=1. Earlier matching-source envelopes
allowed at least one output direction outside the retained target map W.
If the declared output dimension is n=k, W is square orthogonal and the
receipt C=W^T(I+MM^T)^(-1)W fixes the ENTIRE source Gram matrix:

    W^T MM^T W=C^(-1)-I.

All sources with this Gram matrix and the same input-column count are
equivalent under right orthogonal transformations, which preserve the edit
ball. Thus a canonical matrix with this Gram matrix supplies the exact
fixed-output problem. Hidden output dilations are no longer admissible.

## Exact edited maximum for a fixed source

Let B=MM^T, E=e^2>0, bmin=lambda_min(B). For0<=alpha<1 put

    A_alpha=alpha*B+[1-E*alpha/(1-alpha)]I.

There is a unique alphabar in(0,1) at which its least eigenvalue is zero:

    1+alphabar*bmin-E*alphabar/(1-alphabar)=0.

On[0,alphabar), define h(alpha)=v^T A_alpha^(-1)v. At alphabar use the
pseudoinverse value if v is orthogonal to the least-eigenvalue space, and
plus infinity otherwise. Then

    max_(||Delta||op<=e) F(M+Delta;v)
       = min_[0,alphabar] h(alpha).                 (1)

Derivation: the dual quadratic expression for F gives

    max_Delta F(M+Delta;v)
      = max_z [2v^Tz-||z||^2-(||M^Tz||-e||z||)_+^2].

For nonnegative q,

    (sqrt(q)-e)_+^2
       = sup_(0<=alpha<1)[alpha*q-E*alpha/(1-alpha)].

Every feasible A_alpha therefore supplies the upper bound h(alpha).
The function h is convex: A_alpha is matrix concave and inverse quadratic
forms are convex/decreasing on positive definite matrices.

At an interior minimum, z=A_alpha^(-1)v satisfies

    z^T[B-E/(1-alpha)^2 I]z=0.

Choose Delta=-e*(z/||z||)*(M^Tz/||M^Tz||)^T. Then direct multiplication
gives (I+(M+Delta)(M+Delta)^T)z=A_alpha z=v, so the bound is attained.

At alpha=0, the right derivative is E-v^TBv. If it is nonnegative, cancel
M^Tv with an edit of norm at most e, obtaining F=1. This covers M=0.

At a finite minimum at alphabar, let z0=A_alphabar^dagger v. The left
derivative is nonpositive, so z0^T A'_alphabar z0>=0. Add w in the least
eigenspace, orthogonal to z0, with

    ||w||^2 = [z0^T A'_alphabar z0]/
              [E/(1-alphabar)^2-bmin].

The denominator is strictly positive. Then z=z0+w solves A z=v and
z^T A' z=0, and the same rank-one edit attains the endpoint value. This
explicitly handles the singular quadratic endpoint; no minimax exchange
with an indefinite quadratic is being assumed.

## Edited minimum and degenerate shapes

The fixed-source lower formula in minrank_envelope.md also extends from
full-column-rank M to any M with at least one input column: use
B_in=M^T M>=0 and its actual least eigenvalue, possibly zero. The same
quadratic proof applies. At a singular endpoint g=M^Tv is automatically
orthogonal to a zero eigenspace; the null-vector construction is still
available. For M=0 this gives lower1/(1+E). Zero input columns permit no
edit and give F=1. For e=0 both endpoints are simply the retained value.

When n>=k+1, the earlier one-extra-output matching constructions remain
available subject to their input-column restrictions. When n=k, use the
fixed-source endpoints above. A shape claim must state both dimensions;
an arbitrary extra output direction is not free metadata.

## A visible difference from retaining output dimension

Take one target, one input column, C=1/10 and e=1. If the output dimension
is exactly one, M has magnitude3, so the exact edited interval is

    [1/17, 1/5],       width12/85.

If an additional output direction is allowed while preserving that same
scalar receipt and one-column restriction, the earlier cap constructions
attain

    [(3-sqrt(5))/20, (3+sqrt(5))/20],
    width sqrt(5)/10.

Thus knowing the output dimension cuts this constructed interval width by
the fraction1-24/(17*sqrt(5)), about36.86%, without another matrix-value
query. It is a capability/uncertainty metric under a declared information
contract, not an audit-fee or wall-clock saving. Ordinary methods given the
same dimensions and formulas tie. The example is developmental and does
not estimate how often this situation occurs in a real workload.

The bounded same-model screen in fixed_output_probe.py checks 100 constructed
maximizers: 44 cancellation, 51 interior and five singular-endpoint cases.
The scalar value1/5 and a two-output fixed-source hard-case value2/9 agree
with their explicit witnesses. This is finite developmental evidence only.
