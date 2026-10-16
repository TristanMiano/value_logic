# Invoice identification with a fallible logical support

Codex (GPT-6), DEVELOPMENT. The exact support consequences in
[invoice information](invoice_information.md) do not justify treating a
high-confidence model as a proved logical constraint. Here is a quantified
boundary, followed by a task-relative repair.

## A sharp amplification example

Let n=2d+1 be odd, and let F be the even-parity worlds. At invoice cap H=d+1,
the measured characters of degrees <=d form a basis on F. If their population
moments are mu_S, the unique signed reconstruction on the assumed support is

```math
p^*(x)=2^{-(n-1)}\sum_{|S|\le d}\mu_S\chi_S(x),\qquad x\in F.
```

For an arbitrary true law P, define for each odd world z the interpolation
kernel on F

```math
K_z(x)=2^{-(n-1)}\sum_{|S|\le d}\chi_S(z)\chi_S(x).
```

Character orthogonality on F gives
p^*=P restricted to F + sum_(z outside F) P(z) K_z. Each K_z has total mass
one but can have negative entries. All odd z have the same L1 norm L_d by
translation symmetry. If P(F^c)<=epsilon, then

```math
\frac12\|P-p^*\|_1\le\frac{1+L_d}{2}\epsilon,
```

where p^* is embedded as zero outside F. It may be signed; call this total
variation distance only when p^* is a probability law. The inequality follows
by adding the outside mass to the L1 norm of its interpolated image.

The bound is sharp with a nonnegative reconstructed law whenever
epsilon<=(2/(1+L_d)). Put mass epsilon at one odd z. On F put at least
epsilon*max(0,-K_z(x)) at every negative kernel coordinate, then distribute
the remaining probability mass arbitrarily on F. This is possible because
the negative part sums to (L_d-1)/2. Then Q=p^* is nonnegative, supported
entirely on F, and has the same measured moments and therefore the same
invoice distributions for every cap-(d+1) policy as P. Their total variation
distance is exactly epsilon*(1+L_d)/2. Thus a support violation can be
amplified even when observed invoices are perfectly consistent with an exact
support model. This is an information obstruction, not solver error.

For explicit calculation, K_z(x) depends only on the odd Hamming distance
j=2r+1. The elementary coefficient identity

```math
\sum_{k=0}^d [t^k](1-t)^j(1+t)^{n-j}
=[t^d](1-t)^{j-1}(1+t)^{n-j}
```

gives the finite expression

```math
L_d=2^{-2d}\sum_{\substack{j=1\\j\text{ odd}}}^{2d+1}
 {2d+1\choose j}
 \left|[t^d](1-t)^{j-1}(1+t)^{2d+1-j}\right|.
```

No asymptotic estimate is needed for the proposed screen. Check this
combinatorial expression against explicit kernels for n=3,5,7 and preserve
one exact pair P,Q at each size, choosing epsilon small enough to keep both
nonnegative. A larger n=21 or 41 uses only the formula, with no fictitious
enumeration of all worlds. This formula is ordinary finite Fourier and
Krawtchouk-polynomial algebra; no coding-theory priority claim is made.

sp01 passes all six cases on first attempts. The exact L1 kernel norms for
n=3,5,7 are 2,7/2,6, with explicit nonnegative P,Q witnesses and 84 moment
equalities in total. For n=21,41,101 the combinatorial formula is evaluated
without world enumeration. At n=41, support leakage
131072/70861149213 (about 0.00000185) can coexist with total variation 1/4
between a true law and an invoice-indistinguishable exact-support law under
cap 21. This is a constructed possibility, not a measured application risk.

## Stable value information can survive unstable law recovery

For a desired cost g on all worlds, choose any invoice-measurable degree-d
function g_tilde which equals g on F. Its expectation is identified by the
invoice moments. With r=g-g_tilde and support leakage <=epsilon,

```math
\epsilon\min(0,\min_{x\notin F}r(x))
\le\mathbb E g-\mathbb E\widetilde g
\le\epsilon\max(0,\max_{x\notin F}r(x)).
```

This is a valid outer bound, not necessarily sharp after all observed-moment
constraints are imposed. It can be much smaller than a full-law error bound.
In particular, every allowed query-invoice cost already lies in the measured
space, so choose g_tilde=g and obtain zero identification error even if full
law recovery is unstable. A new terminal payoff or enlarged operation menu
can require new information. For choosing among actions, control differences
g_a-g_b; a shared unidentified offset need not matter.

Optimizing a useful extension and checking its residual on a large logical
source have costs. The generic task-relative principle already belongs to
P3-02. The explicit contribution of this branch is the invoice-depth/source
calculation and its sharp failure mode under approximate support. It guides
what to estimate and what not to claim, rather than requiring complete
probability identification for bounded reasoning to be useful.
