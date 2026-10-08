# P3-05 — Reuse over coupled rank-weight regions

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 8, 2026 UTC.
Status: S3 completed exploratory derivation; finite linear ranking, fixed feasible cases
and fixed loss interpretation. No new learning task is started.

## 1. Why one current weight vector is not the whole edit contract

A stored certificate can cover a set G larger than the old winners. The
incumbent test checks one current ranking. Here the edit changes known ranking
weights, or declares uncertainty about them, while holding the case catalogue,
feasibility conditions, violation features and action-loss difference fixed.
This does not optimize over which unknown weight happens to be convenient.
Every admitted weight is covered separately.

Let F be a finite nonempty case family, $`G\subseteq F`$ a nonempty domain with
a checked bound $`d(x)\le B`$, and $`J=F\setminus G`$. Each case has a supplied
rational feature vector $`v_x\in\mathbb Q^k`$. Rank is
$`\rho_w(x)=w^Tv_x`$. Features can be failure indicators of the original soft
clauses. The mathematical reduction works for other linear features too;
that does not make arbitrary such features native to the soft-clause prototype.
The weight set W is a supplied nonempty compact rational polytope with explicit
box bounds and a feasible witness. The following are finite parameter results,
not a choice of a universal scalar value representation.

## 2. Exact all-winner coverage and the role of strict inequalities

**CT05-15 — coverage region.** If J is nonempty, every minimum-ranked case lies
in G exactly when

```math
\min_{g\in G}\rho_w(g)<\min_{j\in J}\rho_w(j).
```

If the inequality fails, a minimum outside G exists: either an outside case is
strictly better, or an outside minimum ties a best covered case. Thus equality
cannot be discarded. Equivalently the safe region is

```math
\bigcup_{g\in G}\bigcap_{j\in J}
   \{w:w^T(v_j-v_g)>0\}.
```

For a fixed covered incumbent g, its intersection is precisely the region
where the entire incumbent sublevel avoids J. Taking the union permits the
incumbent to vary with the observed weight. If the weights remain unknown,
this formula is instead a universal coverage obligation over all W; the acting
agent need not see a hidden weight or choose a different action. The action
pair is fixed. If J is empty, coverage is already complete and no margin LP
is necessary.

Failure of G-coverage does **not** alone refute the actual action comparison:
a case outside a saved certificate may nevertheless have low loss. The result
identifies exactly the information that the *given* certificate lacks.

## 3. A small family of exact rational margin problems

Define the worst coverage margin

```math
\gamma=\min_{w\in W}\left(
       \min_{j\in J} w^Tv_j-\min_{g\in G}w^Tv_g\right).
```

**CT05-16 — finite epigraph reduction.** For each outside case j, solve

```math
\gamma_j=\min_{w,t} t
\quad\text{subject to}\quad
 w\in W,\qquad w^T(v_j-v_g)\le t\quad(g\in G).
```

Then $`\gamma=\min_j\gamma_j`$. Indeed, finite minima over w and j can be
interchanged, and $`w^Tv_j-\min_g w^Tv_g=\max_g w^T(v_j-v_g)`$.
Compactness makes the outer minima attained. Consequently all-winner coverage
for every weight in W is equivalent to $`\gamma>0`$. If $`\gamma\le0`$, an
attaining weight witnesses an outside winner or tie. On a noncompact domain,
a zero infimum need not be attained and does not itself supply that witness;
that extension is not claimed.

This is an ordinary finite parametric linear-programming reduction. Its role
here is to certify the *selection coverage* component of proof reuse under
coupled rank changes, separately from the inherited loss inequality. A single
incumbent can fail uniformly even when the union is uniformly safe.

### Independently checked arithmetic certificates

Write one bounded epigraph system as $`Au\le b`$, with $`u=(w,t)`$ and
objective $`c^Tu=t`$. Given a feasible u and nonnegative multipliers lambda with

```math
 A^T\lambda=-c,\qquad c^Tu=-b^T\lambda,
```

every feasible z satisfies $`c^Tz=-\lambda^TAz\ge-\lambda^Tb=c^Tu`$.
Thus u is an exact minimizer. This direct inequality proves the receiving
check; no optimizer status is trusted. An explicit symmetric bound on t follows
from the weight box and the finitely many feature differences, making the
small search domain bounded without changing its minimum.

The prototype may search rational active bases for such a primal/dual pair.
Its cap can stop before finding one. In that event it returns an incomplete
search, not an infeasibility or robustness conclusion. Every outside case
needs a checked margin certificate for a complete positive report. Complete
input membership and nonempty weight/case families remain separate premises.

## 4. Two separating examples

Take three cases with features

```math
 v_{g_1}=(1,0,0),\qquad v_{g_2}=(0,1,0),\qquad v_j=(0,0,1),
```

and let $`G=\{g_1,g_2\}`$. Let $`w_1+w_2=1`$ with each in
$`[1/4,3/4]`$; hold $`w_3=a`$ fixed. The best covered rank is
$`\min(w_1,w_2)`$, so the exact worst margin is $`a-1/2`$.

At $`a=3/5`$, the margin is $`1/10`$: every winner is covered. Neither fixed
good incumbent beats the outside case throughout W, since its own rank reaches
$`3/4`$. Thus requiring **one common incumbent** loses a valid robust guarantee.
No hidden-state-dependent action is selected; only the proof of the fixed
comparison uses this coverage argument.

At $`a=2/5`$, both endpoints of W have positive gap $`3/20`$, but the midpoint
has gap $`-1/10`$. Checking only the vertices of the weight polytope therefore
misses an unsafe interior parameter. The object being minimized is a
piecewise-linear selection gap, not an affine expression whose minimum must
occur at a vertex of W. Its epigraph LP does have an appropriate attaining
point. At $`a=1/2`$, an outside tie at the midpoint defeats coverage exactly at
the boundary.

## 5. Connection to the actual finite certificate

For a fixed old Boolean frame with soft clauses, enumerate its admitted
finite cases and derive each feature as that clause's Boolean failure bit.
Recheck the old band proof. Its covered cases are exactly those at or below the
certified old cutoff; every such case has the old loss guarantee. The receiver
then recomputes this profile from the old frame and verifies all robust-margin
certificates. A positive result transports the old bound to all new minima
for every weight in W, without changing the loss or optimizing over weights.
This adapter is explicitly paid enumeration, not free access to a complete
logical model set. Scalar soft-clause weights and their formula identities are
held to the current supported interface. The executable soft-clause adapter
requires strictly positive box lower endpoints, preserving the old positive
weight contract. The abstract linear-profile theorem itself permits signed
weights; these two admission domains are not silently identified.

The three-case example can be encoded by two Boolean case bits, excluding 11.
Violation features identify 00, 01 and 10. Old weights $`(1/4,1/2,1)`$ and
cutoff $`1/2`$ certify 00 and 01; only 00 is an old winner. Give these two cases
loss difference minus one, and 10 difference three. At new weights
$`(3/4,1/4,3/5)`$, only 01 wins: the old winner disappears but the band and
positive robust-margin certificate still establish minus one. At midpoint
weights with $`a=2/5`$, 10 wins and the old loss bound really does fail.

## 6. Monotonicity applies to the correctly typed object

Restricting W while holding F, G, features and the loss fixed cannot decrease
this worst coverage margin, because it removes possible parameter scenarios
from the outer minimum. A robust certificate on W remains valid on its subset.
This differs from restricting F, which can eliminate all previous winners and
invalidate a selected-value bound, as P3-04 established. Conflating these two
uses of “narrowing uncertainty” would conceal the changed quantifier.

Changing feasibility, feature meanings or the actual loss requires a new
coverage/quantity bridge. Merely preserving the numerical weight intervals is
not enough. A positive margin is not a probability or a calibration statistic,
and these static sensitivity results do not learn which ranking is useful.
