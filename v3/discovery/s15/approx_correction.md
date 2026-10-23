# Approximate correction with an explicit translation budget

Codex (GPT-6), October23,2026. DEVELOPMENT. Extends collision_corrector.md
to nonuniform sampling and approximate model errors. Classical approximate
self-correction, randomized smoothing and concentration are strong prior.

Let G be an additive group, let H be a real normed vector space, and let
f:G->H be a separately warranted additive function. Fix a model g before
calibration and write e=g-f. Draw U,V independently from a fixed source P.
The model-error distance has the observable mathematical representation

    M(U,V)=||e(U)-e(V)||
          =||g(U)-g(V)-f(U-V)||.                      (1)

One exact source difference and two model calls can acquire M; cheaper sound
upper bounds are also permitted. Neither f(U) nor f(V) must be resolved.

Suppose a retained calibration receipt says

    P[M(U,V)<=epsilon] >= beta.

By averaging over V, there exists a center c=e(v_star) such that
P[||e(U)-c||<=epsilon]>=beta (or arbitrarily close to beta if the
essential supremum is not attained; take the limit below). For a target x,
let P_x be the law of x+R with R~P, and independently warrant

    TV(P_x,P) <= rho.

Then both e(R) and e(x+R) lie in the same epsilon-ball with probability
at least2*beta-1-rho. On this event, the translated model answer

    Y_x=g(x+R)-g(R)

satisfies ||Y_x-f(x)||<=2*epsilon. Therefore

    P[||Y_x-f(x)||<=2*epsilon] >= (2*beta-1-rho)_+.    (2)

This is a conservative ball/union-bound consequence, not a sharp claim.
It permits additive real-valued sources without pretending that an infinite
group has a uniform probability distribution. A common model bias of any
size cancels. The translation-budget warrant is substantive; without it a
model can fail arbitrarily on translated inputs outside calibration support.

For P uniform on [-a,a]^d in R^d, a>0, an explicit budget is

    rho(x)=1-product_j (1-|x_j|/(2*a))_+.

This follows from the intersection volume of the cube and its translate.
For large changes the bound becomes1 and may provide no useful correction.
It is a sampling/functional-equation statement, not a learned causal law.

## Partial receipts and later selection of tolerance

Take a predeclared iid cohort of N pairs with latent distances M_i. Let
paid sound computation provide upper bounds U_i>=M_i; unresolved cases
may have U_i=+infinity. A simultaneous ordinary DKW event supplies

    F_M(epsilon) >= Fhat_M(epsilon)-alpha
                  >= Fhat_U(epsilon)-alpha

for every epsilon, with failure at most2*exp(-2*N*alpha^2). On this ONE
event, every truthful adaptive refinement of U and every subsequent choice
of epsilon is covered. Put beta_lo(epsilon)=(Fhat_U(epsilon)-alpha)_+.
The source/model and sampling law must remain those of the calibration.
New models or data-chosen sampling laws need their own valid uniform event.

When p=2*beta_lo-1-rho>1/2, odd k fresh independent translations and the
ordinary scalar median yield absolute error at most2*epsilon except with
probability P[Bin(k,p)<=floor(k/2)]. For vector outputs with the infinity
norm, take coordinatewise medians: the same majority of good full vectors
protects ALL coordinates, with no extra coordinatewise union bound.
Selecting a minimum predicted loss then has regret at most4*epsilon,
including any separately known additive action-cost vector.

Each new adaptive target uses fresh shifts. The calibration event can be
reused, but the fresh answer errors require a declared per-query/lifetime
budget. Randomized answer correctness is not automatically a simultaneous
confidence statement over every possible future query.

## A receipt-state illustration and an immediate cost screen

At N=5000, alpha=0.02 gives failure2*exp(-4)<0.05. If4600 distances have
sound upper bound epsilon and400 remain unresolved, beta_lo=0.90.
For any target with rho<=0.10, (2) gives p>=0.70. A binomial-tail
calculation can select k for a desired answer risk. Every trial costs two
model calls and a group subtraction, in addition to calibration and source
warrants. The candidate must beat those costs against direct source
evaluation, exact interpolation and ordinary self-correction; an assumed
cheap model is not itself measured evidence of a saving.

For a purely affine model g(z)=B*z+c and linear source f(z)=A*z,
Y_x=B*x for every R. Random shifts cannot repair the linear mismatch;
they only remove c. This rules out an attractive-looking but uninformative
low-rank benchmark. A useful approximate duty needs nonlinear/localized
model errors or a different independently justified structure.

The first correction_probe.py run checks6480 exact finite translation
cases and preserves a counterexample when rho is omitted. For p=0.70,
the smallest odd repetition count reaching the binomial error ceiling0.01
is31 (tail about0.00954), requiring62 model calls per answer. The full
calibration-plus-answer failure ceiling adds the calibration failure;
the1% number alone is not an unconditional end-to-end guarantee.
