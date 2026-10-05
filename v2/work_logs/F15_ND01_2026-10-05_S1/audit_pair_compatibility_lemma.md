# ND01: independent audit of the two-projector feasibility lemma

Reviewer: ChatGPT (GPT-6 Astra Pro), representation-analysis subagent.
Date: 2026-10-05. Concurrent review adds zero separate root-clock minutes.
Scope: the root's proposed supplementary lemma, before calculation of current
mask-pair feasibility. No models, populations, or mask feasibility values were
computed. This is neither ND02 nor F16.

**Verdict: the minimization formula is correct under the stated dimension
assumption.** The specialized sign assumptions and the claim that the nullspace
consists exactly of inactive coordinates require the qualifications below.

## Feasibility proof and boundaries

Put `w=v_N/2`, `t=||w||`, and
`rho_r=sqrt(delta_r+t^2)`. Completing the square gives
`||n_r-w||=rho_r`. For fixed `n0`, minimizing over the second sphere gives

\[
\min_{n_1} n_0^T n_1=n_0^T w-\rho_1\|n_0\|.
\]

Writing `x=||n0||` and using `||n0-w||^2=rho0^2` yields

\[
f(x)=\tfrac12(x^2+t^2-\rho_0^2)-\rho_1 x.
\]

When the nullspace dimension is at least two, every
`x in [|rho0-t|,rho0+t]` is attainable. This follows from the law of cosines
as the first sphere's direction rotates. The degenerate cases `t=0` or
`rho0=0` reduce to a singleton interval. The quadratic has derivative
`x-rho1`, so its minimum occurs at the proposed clamped value.

Maximization instead gives
`0.5*(x^2+t^2-rho0^2)+rho1*x`, which is nondecreasing for nonnegative
`x`. Its maximum is `(t+rho0)*(t+rho1)`. The product of the two spheres is
connected when the ambient nullspace dimension is at least two, including
zero-radius spheres, and the dot product is continuous. Every intermediate
dot product is therefore attainable.

The general exact criterion is

\[
f_{\min}\le -C\le f_{\max},
\]

provided both squared radii are nonnegative. Under `C>=0`, the upper
inequality is automatic and this reduces to `C<=-fmin`. At equality,
tangency is feasible. When `t=0`, the criterion becomes
`C<=sqrt(delta0*delta1)` under the nonnegative-sign assumptions. The
dimension-one case needs separate treatment because its two-point spheres
do not generally supply every intermediate value.

## Sign and rank qualifications

Positive fractional masks do not generally imply `delta_r>=0` or `C>=0`
after projection onto an arbitrary `D`. For example, let `v=(1,1)`, let
`D=span(1,-1)`, and use masks `(3/4,1/4)` and `(1/4,3/4)`. Their observable
coefficients are `(1/4,-1/4)` and its negative, giving
`delta0=delta1=C=-1/8`. This does not invalidate the general interval
criterion.

For the proposed specialization where `D` is the coordinate subspace of
noninactive units, the signs do follow:
`delta_r=sum_visible m_r*(1-m_r)*v^2>=0` and
`C=sum_visible m0*m1*v^2>=0`.

The kink argument correctly proves the needed rank formula under its
assumptions. If a constant linear combination of activations has a nonzero
coefficient on a variable ReLU, choose an interior point of its kink
hyperplane away from every other kink. Its unique derivative jump forces
that coefficient to vanish, a contradiction. Distinct affine hyperplanes
must be checked up to any nonzero proportionality, including negative
scaling. Strictly opposite-sign box extrema guarantee an interior cut.

After all variable coefficients vanish, a constant combination remains
exactly when the always-active weight columns annihilate its coefficient
vector; biases contribute only a constant. Consequently

\[
\dim D=\#\text{variable}+\operatorname{rank}(W_{\rm active}).
\]

Its complement contains inactive coordinates and the dependencies among
always-active columns. It consists **exactly** of inactive coordinates only
when `#always_active=rank(W_active)`. A reported rank of zero or one alone
is insufficient; the corresponding active-unit count must agree.

## Rank-eight extension and metric scope

Compatible nonzero orthogonal coefficients give rank-one projectors. They
can be enlarged using mutually orthogonal added directions from
`span(v,q0,q1)^perp`. In width 32 this common complement has dimension at
least 29, enough to add seven directions per nonzero rank-one projector.
Zero-coefficient cases also have enough room to reach two rank-eight
projectors. The additions preserve effective coefficients, mutual
orthogonality, and the structural assignment algebra. They do not establish
the semantic cost interpretation.

Feasibility is relative to the declared Euclidean metric. If the complement
is inactive coordinates and `v_N` is nonzero, positive rescaling of those
units can change `v_N` and `t` while preserving ordinary outputs and
transported coordinate masks.
For sufficiently large `t`, the minimizer is interior and
`fmin=-(t^2+delta0+delta1)/2`; compatibility can therefore be made feasible
by unrestricted positive rescaling. Report the stored-coordinate metric result, not an
invariant property of the learned input-output function. Floating evaluation
of an exact lemma should also report its numerical margin or a certified
bound near the feasibility boundary.
