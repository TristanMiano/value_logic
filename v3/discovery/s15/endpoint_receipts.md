# Absolute and maximum losses need only a simple receipt envelope

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 25.
This extends the numerical information contract to two nonsmooth endpoints.
It is a small mathematical capability result, not a measured speedup.

For finite-dimensional normed spaces X,Y and ||v||=1, define

    A(M;v)=min_x (||v-Mx||+||x||),
    B(M;v)=min_x max(||v-Mx||,||x||).

Let C denote either A or B, with old scalar receipt C(M;v)=s in (0,1].
Suppose ||N-M||<=e and ||w-v||<=eta. Then the sharp, space-unrestricted
infimum and supremum compatible with these receipts are

    (s-eta)_+/(1+e) <= C(N;w)
                   <= min(1+eta, (1+e)*s+eta).               (1)

For eta=0 both endpoints are attained in finite dimension, including when
s<1. This differs from the limiting l_p witnesses used for 1<p<infinity.
The word sharp refers to the declared information across allowed spaces;
it need not describe a particular fixed Euclidean geometry.

## Bounds

For either product norm, replacing M by N changes any fixed x's objective
by at most e*||x||, which is at most e times its old objective. Minimization
and exchange of M,N give

    C(M;u)/(1+e) <= C(N;u) <= (1+e)*C(M;u)

for every u. Each C(M;.) is a norm bounded above by the Y norm and is
therefore 1-Lipschitz with respect to that norm. The lower bound follows
by applying the same-target inequality to w and then
C(M;w)>=(s-eta)_+. The upper bound follows by first editing M at v and
then the target, together with C(N;w)<=||w||<=1+eta.

Coercivity supplies minimizers; positive definiteness follows from the
bounded linear map M and the product norm. No differentiability is used.

## Explicit sharpness in X=Y=l_infinity^2

For nonnegative diagonal entries a_i,

    B(diag(a_i);u)=max_i |u_i|/(1+a_i).

For a_i>=1,

    A(diag(a_i);u)=max_i |u_i|/a_i.

The second equality follows because x=M^-1 u attains that value and
||u||_(weighted infinity) <= ||u-Mx||_infinity+||x||_infinity.

For B's lower bound with s>eta, take v=(s,1), w=(s-eta,1),
M=diag(0,K), N=diag(e,K), choosing finite K large enough that the second
coordinate is below both desired values. This attains (s-eta)/(1+e).
For A use the same targets and M=diag(1,K), N=diag(1+e,K).
When eta>=s, set the first coordinate of w to zero and let K increase;
the lower endpoint zero is an infimum. If eta>=1, w=0 attains it.

For B's upper linear branch, (1+e)*s<=1, take
v=((1+e)*s,1), w=((1+e)*s+eta,1), M=diag(e,K), N=diag(0,K).
For A replace the first diagonals by 1+e and 1. Again finite large K
attains the endpoint. On the capped branch use v=(1,1), w=(1+eta,1),
with B's first diagonal changing from 1/s-1 to zero, or A's from 1/s
to one. The edit is permitted since 1/s-1<=e. These constructions also
cover equality at the join and eta=0.

## Contribution screen

Ordinary quotient norms, infimal convolution and robust optimization supply
the ingredients. Retain the sharp receipt-conditioned endpoint formula
as a useful extension alongside the p-power family, but do not count it
as another independent mechanism or claim priority without a closer source
comparison. A=absolute-residual regularization and B=balanced worst-component
regularization support different application choices. Neither formula
acquires its scalar receipt, norm warrant or target-edit bound for free.

The endpoint formula also exposes a distinction between old optimizer
reuse and reoptimization: it certifies the new optimum; it does not supply
an optimizer at that value or its computation cost.
