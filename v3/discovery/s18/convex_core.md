# Constructing a feasible action from value-only receipts

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT; broad constructive branch.
This revisits [value receipts](value_receipts.md). Unknown feasibility and
unknown optimizer coordinates are different from impossibility of constructing
an action. Convexity can turn existential value receipts into an explicit
feasible point even when no individual witness was retained.

## General core and the role of convexity

Let A be a known compact convex set. An unknown nonempty compact convex
F subset A intersects each known nonempty compact contact set T_i subset A.
The T_i arise, for example, from truthful upper bounds on old linear minima,
after all old lower bounds have been imposed on A. No retained incumbent is
assumed here. Every selector tuple x_i in T_i gives a compatible minimal set
conv{x_1,...,x_m}. The actions feasible in every compatible source are exactly

    K = intersection_(x_i in T_i) conv{x_1,...,x_m}.                 (K1)

Equivalently, by separation of a point from a compact convex set,

    y in K iff h.y <= max_i min_(x in T_i) h.x for every h.        (K2)

Indeed, the least possible support of a selector hull in direction h is
min_(x_i) max_i h.x_i = max_i min_(x_i in T_i) h.x_i. Finite independent
choices and compactness justify both minimizers and the exchange. This is
also the earlier sharp new-value upper envelope with the sign of h reversed.
The right side need not itself be a support function; K can be empty.

Convexity changes the action question. In one dimension, contacts in[-1,-1/2]
and[1/2,1] force every compatible convex F to contain[-1/2,1/2]. Without
convexity the two endpoint witnesses need not imply any intermediate action.
The old finite example with contacts at(0,2),(2,0),(1,1) does not demonstrate
failure after convexification: the segment between the first two points
already contains(1,1). Keep the sharp value formula, but use a genuine
convex counterexample when claiming that a common action is absent.

## Exact symmetric coordinate construction

Assume dimension d>=2, a known Euclidean radius R>0 and0<=gamma<=R.
The unknown F is nonempty compact convex and contained in the ball||x||_2<=R.
For every coordinate i, truthful value receipts say

    min_(x in F) x_i <= -gamma,   max_(x in F) x_i >= gamma.       (K3)

They provide2d existential contacts, not2d disclosed optimizers. Set

    sigma = sqrt(R^2-gamma^2),
    lambda = gamma - sqrt(d-1)*sigma.

The exact common feasible core is

    K = {y: ||y||_1<=lambda}, if lambda>=0;
    K = empty,               if lambda<0.                        (K4)

Thus a nonempty guaranteed-action core appears precisely at
gamma>=R*sqrt((d-1)/d). At equality the zero vector is guaranteed feasible;
above it, an explicit cross-polytope of actions is available. This does not
identify F, its complete values, or any of the old optimizing witnesses.

### Containment proof

Fix h and choose i with|h_i|=||h||_infinity, with its matching sign.
The corresponding contact cap has sign(h_i)*x_i>=gamma. For gamma at or
above the threshold, minimizing h.x on that cap gives

    gamma*|h_i| - sigma*sqrt(||h||_2^2-h_i^2)
       >= [gamma-sqrt(d-1)*sigma]*||h||_infinity
       = lambda*||h||_infinity.

The cap minimum occurs on its coordinate boundary: the unconstrained
ball minimizer points opposite h and cannot lie in this positive cap.
Since F contains a cap witness, its support in direction h is at least
this value. Support-function containment then gives lambda times the unit
l1 ball subset F. This is ordinary convex geometry and Cauchy–Schwarz.

### Sharpness and the empty-core regime

For any sign vector s in{-1,+1}^d, put b=sigma/sqrt(d-1). For each i choose
two witnesses with coordinate i equal to+gamma*s_i or-gamma*s_i and every
other coordinate j equal to-b*s_j. Each has norm R; their convex hull is a
compatible F because it reaches both coordinate thresholds. All of them obey

    s.x <= gamma-(d-1)*b = lambda.

If lambda>=0 and||y||_1>lambda, choose s matching y. This compatible F excludes
y, proving the reverse inclusion in(K4). If lambda<0, the all-positive and
all-negative sign constructions force opposite strict halfspaces. Their
intersection is empty, proving that no common feasible action exists.
The information class itself remains consistent, for example via the full
radius-R ball. Empty core is not inconsistent evidence.

## Explicit cases and decision use

For d=2,R=1,gamma=4/5, sigma=3/5 and lambda=1/5. Every compatible F contains
the diamond||y||_1<=1/5. The four coordinate value receipts can therefore
deliver the action(1/5,0) without recovering a single old optimizer. A sharp
source for the first-quadrant separating direction is the hull of
(4/5,-3/5),(-4/5,-3/5),(-3/5,4/5),(-3/5,-4/5), all with x_1+x_2<=1/5.
For gamma=3/5 instead, lambda=-1/5 and no action is guaranteed feasible.

An integer three-dimensional case is R=19,gamma=17,b=6,lambda=5:
17^2+2*6^2=19^2. Six scalar contacts force the complete5-radius l1 ball.
The extremal witnesses have one coordinate+/-17 and the other two equal
to signed-6. No floating-point optimizer is needed for these certificates.

For a new known linear cost c.y, minimizing over the guaranteed core gives
-lambda*||c||_infinity, with an explicit signed coordinate action. This is
a robust feasible action, not necessarily an optimizer of the unknown F.
The radius-R bound also gives the separate crude regret upper bound
R*||c||_2-lambda*||c||_infinity. Stronger old value constraints may improve it.

A known affine image c_0+A*z transports the construction when A is invertible
and the stated coordinate receipts concern z=A^{-1}(x-c_0). Source binding,
convexity and the radius warrant must actually be supplied or checked.
Randomizing between infeasible physical actions is not a substitute for a
convex feasible action space.

## Comparison duties

The mechanism is an explicit integration of support receipts, a norm bound and
convexity. It uses standard support-function containment; novelty is unassessed.
Natural interfaces might disclose scalar optimization bounds while withholding
optimizers or private constraints. That possible motivation is not measured
evidence. A retained feasible incumbent or a direct feasibility query at the
proposed action is a strong ordinary control whenever available. Do not claim
that acquiring these2d reports is cheaper than asking that direct question.
The constructive point is what already retained values can warrant and output.

The first literature screen found a direct general framework: guaranteed
hulls, including the pre-inner support formula of Davari–Edalat–Lieutier2019.
Credit(K1)/(K2) to this established geometry. The closed coordinate/radius
formula(K4) is a specialization derived here, not evidence of novelty by
itself. The related [translated-region construction](translated_core.md)
includes a concrete obstruction to replacing a collective core with fixed
small-subset cores, checked by exact rational enumeration.
