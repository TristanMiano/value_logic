# Exact convex-value envelopes under uncertain witnesses

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT; same-model derivation.
This extends the [translated guaranteed core](translated_core.md) to a
reoptimized convex value. Ordinary convex duality is the principal comparator;
neither a new generic optimization algorithm nor moderate novelty is assumed.

## Information contract

Known centers a_1,...,a_n lie in R^d, P=conv{a_i}, and C is a known nonempty
compact convex uncertainty set. Unknown feasible witnesses x_i independently
satisfy x_i in a_i+C. Every witness is in one unknown compact convex F.
For upper-value statements it suffices to consider the minimal compatible
F=conv{x_i}; a larger F can only improve a minimized objective. For the exact
two-sided envelope below, the source itself is this hull. No unrelated global
constraints may silently restrict the allowed selectors or common shifts.

Let f:R^d->R be finite continuous convex, and define

    g(c) = min_(a in P) f(a+c).

Then the exact range of the reoptimized value over all independent witness
configurations is the same interval as under common translations:

    min_(x_i in a_i+C) min_(x in conv{x_i}) f(x) = min_(c in C) g(c),
    max_(x_i in a_i+C) min_(x in conv{x_i}) f(x) = max_(c in C) g(c). (V1)

Every intermediate value is attained by a common translation. Individual
hidden hulls need not be translates of P; this is a scalar envelope result.

### Lower endpoint

Every selected hull lies in P+C. Conversely every point a+c in P+C lies in
the common-shift hull P+c. Thus the lower endpoint is min_(P+C) f.

### Upper endpoint

Fix an arbitrary selected hull H and a minimizer z of f on H. Convex optimality
gives h in the subdifferential of f at z with h.(x-z)>=0 for every x in H.
This uses the usual convex sum rule, valid here because f is finite and
continuous on all R^d. Choose c* in C maximizing h.c. For every i,

    h.(a_i+c*) >= h.x_i >= h.z.

The same holds for all a in P. The subgradient inequality therefore yields
f(a+c*)>=f(z). Hence g(c*)>=min_H f. Common shifts are themselves allowed
independent configurations, which proves equality of the upper extrema.
The case h=0 is included: z is then a global minimizer of f.

The function g is convex (partial minimization over a convex set) and continuous
(continuous f over a fixed compact P). On connected C its image is an interval,
so common translations attain every value between their extrema. If C is a
polytope, max_C g is attained at one of its vertices. This replaces k^n
independent corner configurations by k common-corner convex optimizations for
this one scalar envelope. It does not promise an efficient maximum over an
arbitrary convex body C or uncharged construction of P.

The dual expression is equivalently

    max_H min_H f = sup_h [min_i max_(x in a_i+C) h.x - f*(h)].   (V2)

The constructive supporting-hyperplane proof avoids relying on an unjustified
max/min exchange. The max–min support representation and ordinary infimal
convolution already supply the ingredients.

## Useful qualifications

**Convexity matters.** In one dimension, take centers-1,+1, C=[-1,1] and
f(x)=(1-x^2)^2. Independent displacements can collapse both points to0,
giving minimum1. Every common-shift interval[c-1,c+1], c in[-1,1], contains
either-1 or+1, so its minimum is0. This nonconvex objective violates(V1).

**Marginal value envelopes are not a joint model.** With those same centers
and C, the collapsed hull{0} gives minima0 for both f_1(x)=x and f_2(x)=-x.
A common-shift interval gives(c-1,-c-1), whose components always sum to-2.
Each individual value has the correct possible range[-2,0], but no common
shift explains the valid joint observation(0,0). A reduced translation family
must not be conditioned on multiple truthful values as though it were a true
generative source. Future counterfactual objectives require the stated envelope
contract or additional retained information.

**A good reoptimized value need not return a uniformly good action.** Use the
four square regions of [the exact core example](translated_core.md), so
P={a:||a||_1<=1}, C=[-2/5,2/5]^2 and common feasible core K=(1/5)B_1.
For f(x)=||x-(1/2,0)||_2^2, the worst reoptimized value is

    max_(c in C) dist((1/2,0)-c,P)^2 = 9/200.

At the two corners with c_1=-2/5, the target relative to P has absolute
coordinates(9/10,2/5). Its excess l1 norm is3/10, and projection onto the
diagonal facet gives squared distance(3/10)^2/2=9/200. At the other two
corners the target is inside P. Convexity of g proves the corner maximum.
Yet the best single action known feasible in every source is(1/5,0), costing
9/100. Thus an existential reoptimized bound can be a factor two below the
best uniformly feasible action cost. Source-specific witness acquisition can
still be necessary to implement the better bound. A randomized action whose
support must be feasible for every source cannot improve the convex objective
over its mean in K. This is an information/output distinction, not a fee gain.

## Counterfactual uncertainty updates

If every uncertainty region changes from a_i+C to a_i+C+D with a supplied
compact convex D, the new common feasible core is exactly

    K_new = (P minus_Pontryagin (-C)) minus_Pontryagin (-D)
          = K_old minus_Pontryagin (-D).                         (V3)

This is standard associativity of erosion. It gives a precise reuse contract
for a known enlargement of uncertainty; arbitrary source revisions, reduced
uncertainty or unknown changes do not inherit it. For fixed known translation
d instead, the core translates by d. These are explicit ordinary geometric
counterfactuals, not a semantics for arbitrary inconsistent mathematical worlds.

## Next comparison

Check close robust-optimization/uncertain-hull results before expanding this
into a contribution event. The current positive delta is a transparent scalar
optimization envelope and its executable-action boundary. The old
same-corner hull method and support formulas may already make it routine.
No readiness forecast is assigned to this branch yet.

## General polytopal regions: a finite exact envelope

For arbitrary nonempty compact convex regions B_i, let f again be finite,
continuous and convex. The upper-envelope proof still works: at a minimizing
point z of any selected hull, choose its supporting subgradient h, then replace
each selected point by an h-maximizer of its own B_i. Every replaced point
has h-value at least h.z, so the new hull's minimized f cannot be smaller.
Therefore a worst configuration can be chosen with all its vertices exposed
by a common direction. This is stronger than enumerating arbitrary independent
vertex choices, and it does not require the regions to be translates.

For finitely many polytopal B_i, refine their normal fans. On each full-
dimensional cone, select the unique support vertex of each region; retain the
resulting hull. Directions on fan boundaries also admit an attaining such
configuration: perturb within an adjacent full-dimensional cone, and its
vertices still maximize the original boundary direction. If h=0, any selected
configuration has value at least the global minimum f(z), so it causes no
exception. The maximum of min_H f over this finite family is the exact upper
envelope. The lower envelope is min f over conv(union_i B_i).

For axis-aligned boxes, the fan has only2^d coordinate sign cones, so2^d
same-corner hulls suffice for the upper envelope. The established inner-hull
algorithm already retains exactly this kind of family. Our additional
interpretation keeps the family for convex reoptimization, rather than retaining
only its intersection: min_(intersection H) f can strictly exceed
max_H min_H f, as the9/100 versus9/200 example shows. The information lost
by retaining only the common feasible core is consequential for value bounds.
This is a direct duality-based adaptation of prior geometry; novelty still
requires a close comparison.

## Prospective finite arithmetic check

Before execution: use the same four rational squares as the core probe and
the squared Euclidean losses centered at(0,0),(1/2,0),(2,1). Compute exact
point-to-polygon minima on all256 corner hulls and the four ordinary
same-corner hulls. Compare their maxima, and separately evaluate the common
core. Expected second-target values are9/200 and9/100. No random sampling,
floating optimizer, new source purchase or full model recovery. Reusing the
same rational hull routine is explicitly not independent implementation.
One execution; preserve failed source versions. This checks the finite
calculation and ordinary reduction, not the general theorem or fee economics.

[The exact probe](convex_value_check.py) passed; [result](convex_value_result.json).
Its three targets agree between256 independent corner hulls and four ordinary
same-corner hulls. The middle target gives9/200 versus9/100 exactly. Python
3.12.14,31,000,000ns measured execution, source SHA256
237d39ba9450ce637a5751c83c60558c09f69b7b86082072508244b6e07817f1.
This is a reproduction of the finite consequence using the strong ordinary
reduction, not a64-fold practical speed or fee claim.
