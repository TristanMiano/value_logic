# Shared edits constrain action contrasts more than separate value intervals

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass40.
Matrix interval optimization, singular-value inequalities and robust control
are conventional ingredients. Exact application novelty remains unassessed.

## A certificate for a whole response block

Let X=W^T(I+NN^T)^(-1)W. The operator receipt gives simultaneous L<=X<=U,
where L=L_t(C), U=U_q(C) may use separately chosen admissible parameters.
Let H be any symmetric action-contrast matrix, e.g. cc^T-dd^T. Put D=U-L.
The maximum over this matrix interval is

    max_(L<=X<=U) tr(HX)
       = tr(HL)+tr((D^(1/2) H D^(1/2))_+).           (1)

Indeed X=L+D^(1/2) K D^(1/2),0<=K<=I, on the support of D; choose K to
project onto the positive eigenspace. The analogous minimum uses the negative
part. A certified semidefinite upper bound can replace exact eigensolving.
This interval optimization can be loose for the set of actually edited
sources; it is not a general sharpness claim for that smaller set.

For L=lI,U=uI and unit targets with c^T d=cos(theta), H has eigenvalues
plus/minus sin(theta). Hence the difference is in

    [-(u-l)*sin(theta), (u-l)*sin(theta)].           (2)

Independent subtraction of the two [l,u] intervals instead gives plus/minus
(u-l). This corrects the artificial uncertainty that remains even when the
two targets are identical. The targets, source and paid receipt are shared;
an ordinary joint matrix calculation obtains exactly the same improvement.

## Frobenius budgets also couple orthogonal targets

Here is a different, finite-shape example where the angle in(2) is90degrees.
The full retained response is C=I_2/2 and the source has two output and two
input coordinates. A right orthogonal change makes M=I_2. The warranted
edit budget is ||N-M||_F<=e, with0<e<=1/10. Each individual target still has
the sharp interval

    [f(1+e),f(1-e)],       f(x)=1/(1+x^2),

because a rank-one edit attains either endpoint. But the two opposing
rank-one edits cannot both spend the full Frobenius budget.

For any N with singular values sigma1<=sigma2, the contrast is at most
f(sigma1)-f(sigma2). The singular-value distance inequality gives

    (sigma1-1)^2+(sigma2-1)^2 <= ||N-I||_F^2.

In this identity-source case no general perturbation theorem is needed:
write N=U diag(sigma_i)V^T, so tr(N)<=sum_i sigma_i, and expand
||N-I||_F^2=sum_i sigma_i^2+2-2tr(N). This proves the displayed bound.

Both bounds are attained by a positive diagonal N aligned with the two
contrast targets. An optimum has sigma1<=1<=sigma2, since moving either
singular value toward1 otherwise improves the objective and reduces cost.
Thus the exact positive endpoint is the one-variable problem

    max_(a,b>=0, a^2+b^2<=e^2)
        f(1-a)-f(1+b),                            (3)

or a=e*cos(phi),b=e*sin(phi),0<=phi<=pi/2. The negative endpoint is its
opposite by exchanging targets. Formula(3), rather than two independent
scalar envelopes, accounts for the shared paid edit warrant.

An inexpensive analytic upper certificate already separates the interfaces.
On[.9,1.1],0<f''(x)<=1/2: differentiating gives
f''=2(3x^2-1)/(1+x^2)^3, whose maximum on this interval is1/2 at1.
Taylor's theorem and convexity therefore imply

    f(1-a)-f(1+b)
       <= (a+b)/2+a^2/4
       <= e/sqrt(2)+e^2/4.                       (4)

For e=.1, independent sharp intervals give contrast radius

    100/181-100/221 =4000/40001 =.09999750006...,

whereas(4) gives radius.07321067812... . Thus the same Frobenius information
certifies over26.78% less contrast uncertainty using even this nonoptimal
joint bound. This is an uncertainty/capability gain, not a measured fee or
CPU saving. Source acquisition, matrix storage and edit-norm verification
are paid. The ordinary joint robust calculation ties.

Under an operator-norm budget, the diagonal edit diag(-e,+e) is allowed;
then the independently subtracted endpoint IS attained. Replacing an
operator bound with a Frobenius bound without a warrant would fabricate
this improvement. Nor is(3) automatically a concave optimization: its
first term is convex in a on the displayed interval. A numerical local
optimum alone is not a certificate for its global value.
