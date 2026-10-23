# Explicit rational certificates from partial scalar receipts

Codex (GPT-6), DEVELOPMENT, October 22, 2026. A constructive specialization
of classical rational interpolation for positive Stieltjes responses.
It strengthens the inexpensive single-receipt cover in receipt_cover.md;
it does not claim a new general interpolation principle.

For y(t)=E[1/(1+t*lambda)], lambda>=0 and y(0)=1, choose distinct positive
nodes t_1,...,t_m. Put

    D(t)=product_j(t+t_j), B(t)=product_j(t-t_j)/D(t),
    ell_i(t)=D(t_i)/D(t)*product_(j!=i)(t-t_j)/(t_i-t_j),
    I(t)=sum_i ell_i(t)*y(t_i).

These are explicit cardinal rational functions: ell_i(t_j) is the Kronecker
delta. No hidden spectrum or fitted model is needed to evaluate them.

## Pointwise residual, then a valid certificate

For every lambda>=0, polynomial multiplication gives

    1/(1+lambda*t)-sum_i ell_i(t)/(1+lambda*t_i)
      = B(t)/(1+lambda*t)*product_i(1-lambda*t_i)/(1+lambda*t_i).  (1)

One proof multiplies by (1+lambda*t)D(t). The numerator vanishes at every
t_i and has degree at most m, so it is a multiple of product_i(t-t_i).
Evaluating at t=-1/lambda determines the multiplier; lambda0 follows by
continuity or direct polynomial division. Thus |y(t)-I(t)|<=|B(t)| after
integrating (1) against the positive measure. This direct algebra avoids
importing an unread general analytic interpolation theorem.

For truthful value intervals [L_i,U_i], let I_lo/I_hi be the exact minimum
and maximum of sum ell_i(t)*v_i over their Cartesian product, choosing each
endpoint according to the coefficient's sign. Then

    I_lo(t)-|B(t)| <= y(t) <= I_hi(t)+|B(t)|.

This is conservative if receipts are correlated; treating a containing box
as independent samples is neither needed nor justified. Exact/outward
arithmetic must include the errors in coefficients and evaluation.

## A stronger even-node bound

Suppose m is even, every node lies in[A,B0], and
delta bounds |B(t)| on that interval. For z=1/lambda outside[A,B0], all
factors in B(z) have the same collective positive sign. Inside the interval,
B(z)>=-delta. Therefore the multiplier of B(t) in (1) lies in[-delta,1].
The endpoint lambda0 has multiplier1; the infinite-lambda limit is0.

It follows that a valid band is

    [I_lo+min(-delta*B(t),B(t)),
     I_hi+max(-delta*B(t),B(t))].

Its width is at most (1+delta)*|B(t)|+sum_i |ell_i(t)|*(U_i-L_i).
Clip with[0,1] and inherited monotonic bounds if useful. Every compatible
positive spectral model is protected; neither the spectrum nor a single
privileged fitted model is identified.

## Four concrete nodes and exact preparation targets

Take nodes1,2,8,16 and target interval[1,16]. With u=t+16/t in[8,17],

    B(t)=(u-17)(u-10)/[(u+17)(u+10)].

The exact uniform bound is |B(t)|<=1/25, attained positively at t4.
For the upper bound,25*N-D=6*(u-8)*(4u-85)<=0 on[8,17]. For the lower,
25*N+D=2*(13u^2-324u+2210)>0, since its discriminant is negative and
its leading coefficient is positive. Here N=u^2-27u+170, D=u^2+27u+170.

The four cardinal numerators over D(t) have constants
-306/35,180/7,-720/7,4896/35 multiplying the corresponding three factors
(t-t_j). A cheap exact Bernstein-polynomial certificate can establish
sum_i|ell_i(t)|<=9/4 on[1,16], splitting at the nodes and, if necessary,
subdividing intervals. This coefficient bound is a prospective check until
the accompanying certificate is executed and retained.

Conditional on that bound, receipts each of radius at most1/1000 yield
uniform band width at most

    26/625 + (9/2)/1000 = 461/10000 = 0.0461.

The upper-envelope decision service therefore has uniform regret at most
0.0461 plus certified optimization error, in normalized loss units, using
four partial responses over this whole interval. This improves the first
simple four-point covering guarantee, about0.0884, as a *guarantee on a
different specified placement/algorithm*, not as an observed workload gain.
Ordinary interval rational interpolation performs the same construction.

Point placement, original receipt purchases, numerical convergence, preparation,
interval evaluation and decision optimization remain charged operations.
No claim that this beats joint positive-moment optimization, multipoint Pade,
or direct target computation in complete cost is established. The useful
adapter is an explicit, checkable range-of-decisions receipt contract.

The executed `receipt_probe.py` now establishes the coefficient bound with
five exact rational Bernstein subinterval certificates, retained in
`receipt_probe.json`. All 488 kernel identities and 3,050 finite-law band
checks passed. Thus the conditional coefficient premise above is discharged
by a finite exact certificate; the broader ordinary-comparator and complete
cost limitations remain. The finite-law checks supplement the displayed
general identity rather than replace its proof.
