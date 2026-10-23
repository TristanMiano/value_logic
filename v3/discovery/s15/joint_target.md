# A retained value can also survive a changed target

Codex (GPT-6), October23,2026. DEVELOPMENT. Extends norm_transport.md;
not independently reconstructed, and close-prior novelty is unassessed.

Let X,Y be finite-dimensional real normed spaces, 1<p<infinity,
q=p/(p-1), and

    F(M;v)=min_x (||v-Mx||_Y^p+||x||_X^p).

The old target satisfies ||v||=1 and its paid value receipt is F(M;v)=s,
0<s<=1. The new model and target satisfy independently justified bounds

    ||N-M|| <= e,    ||w-v|| <= eta.

The structural bounds are paid premises, not consequences of the scalar
receipt. Both changes may be adversarial and coordinated. Put

    a=s^(1/p), b(k)=(1+k^q)^(1/q),
    t=(s^(-1/(p-1))-1)^(1/q), A(k)=a*b(k).

Then the proposed dimension-unrestricted sharp envelopes are

    L = min_(0<=k<=t) [(A(k)-eta)_+ / b(k+e)]^p,
    U = max_(0<=k<=t) [(A(k)+eta) / b((k-e)_+)]^p.       (1)

They require two one-dimensional optimizations and no new operator
application after the old receipt and edit warrants have been acquired.
That is a mathematical information contract, not a complete-cost saving.

## Lower bound from the old optimal dual witness

The quotient norm identity is

    F(M;v)^(1/p) = sup_(y!=0) <y,v> /
                  (||y||_*^q+||M*y||_*^q)^(1/q).

At an old maximizing witness y, let k=||M*y||_*/||y||_*.
The numerator divided by ||y||_* equals a*b(k)=A(k). The unit norm of v
forces A(k)<=1, hence k<=t. The edit inequalities give

    <y,w>/||y||_* >= A(k)-eta,
    ||N*y||_*/||y||_* <= k+e.

Evaluating the new dual quotient at y proves the lower expression in(1)
for this unknown k, and minimizing over its allowed interval proves L.
If the numerator is negative, the trivial nonnegative value gives the
positive part. Finite dimensionality supplies a maximizing witness; this
argument does not require differentiable or strictly convex norms.

## Upper bound from every new dual direction

For any nonzero y, again set k=||M*y||_*/||y||_*.
The old value and target norm jointly give

    <y,v>/||y||_* <= min(1,a*b(k)).

Meanwhile <y,w> <= <y,v>+eta*||y||_* and
||N*y||_*/||y||_* >= (k-e)_+. Thus the new dual quotient is at most

    [min(1,A(k))+eta] / b((k-e)_+).

For k>=t the numerator is constant and the denominator is nondecreasing,
so its supremum is already attained somewhere in[0,t]. Taking the
supremum over y proves U. This step is essential: simply reusing the old
primal minimizer generally supplies a looser upper bound.

## Sharpness in two-dimensional l_p spaces, as a limit

Fix k in[0,t]. For K large, let M=diag(k,K) and

    v_K=(c_K,(1-c_K^p)^(1/p)),
    c_K^p=(s-ell(K))/(ell(k)-ell(K)),
    ell(u)=(1+u^q)^(1-p).

Then ||v_K||_p=1, F(M;v_K)=s exactly, and c_K tends to A(k).
For the lower construction use N=diag(k+e,K), and reduce the first
target coordinate by min(eta,c_K). For the upper construction use
N=diag((k-e)_+,K), and increase that coordinate by eta.
Both edits obey their bounds. The second coordinate's optimized cost
vanishes as K tends to infinity, while the first converges to the two
expressions in(1). Therefore every value optimized in(1) is approached
by an admissible sequence. No blanket finite-attainment claim is made.

When k=t, A(k)=1 and the scalar construction already attains the endpoint.
For e=0, the envelopes reduce to

    (s^(1/p)-eta)_+^p <= F(M;w) <= (s^(1/p)+eta)^p,

with limiting diagonal witnesses. For eta=0, recover norm_transport.md.
For s=1, t=0 gives L=(1-eta)_+^p/(1+e^q)^(p-1) and U=(1+eta)^p.

## Monotone scalar root reductions when e>0

If eta>=a then L=0. Otherwise the unconstrained lower minimizer k_L is
the unique nonnegative solution, before the eta=0 minimizer, of

    [1-e*k^(q-1)-(k/(k+e))^(q-1)] /
       (1+k^q)^((q-1)/q) = eta/a.                    (2)

The numerator decreases strictly from1 to zero on this interval and
the positive denominator increases. The objective derivative has the
sign of eta/a minus the left side, so clip k_L at t.

For the upper bound, the objective increases on[0,e]. On k>e, its
derivative has the sign of the following left side minus eta/a:

    [(k/(k-e))^(q-1)-1-e*k^(q-1)] /
       (1+k^q)^((q-1)/q) = eta/a.                    (3)

The positive part of the left side decreases from infinity to zero.
Thus there is one root k_U>e, and the constrained maximizer is
min(k_U,t). At eta=0 these roots coincide with the earlier lower and
upper shear optima; e=0 is handled by the separate exact formula.
These derivative reductions need a cheap implementation check before
they are used as certified numerical procedures. Floating bisection is
not outward arithmetic.

## Why this is related to the original objective

A changed scientific or mathematical task can change both the evaluator
and its target. Retaining only the old scalar value leaves most of the
model unresolved, yet(1) states exactly which new values it can exclude
under explicit change semantics. This is task-relative reuse of paid
reasoning, not a claim that a counterfactual changes mathematical truth.
Robust optimization, dual quotient norms and perturbation theory are
ordinary ancestors and an identical conventional implementation ties.
The potentially useful contribution is the sharp small-information
contract and a warranted decision adapter. A source comparison and a
specific paid application remain necessary before a novelty claim.

The first joint_probe.py run passes240 small parameter cases, their scalar
grid checks and diagonal limiting witnesses, plus20 nonsymmetric matrices
with separately calculated primal/dual intervals (maximum gap<4.49e-11).
At p2,s0.1,e1,eta0.05 the approximate interval is
[0.02835137938,0.30793598104]. These are floating checks, not outward
certification. Sharpness is uniform over the class of spaces/dimensions;
an individually fixed space can admit a stronger contract.
