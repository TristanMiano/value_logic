# F09 optional reconstruction C — which Boolean observations exist?

Research contributor: **Codex (GPT-6)**. September 30, 2026 UTC.
Optional ambition selected while the protected D60 block remained open. This
develops the elementary Boolean interpretation beyond the required example;
it does not change the native language or attempt a later implementation task.

## 1. Boolean observations are controlled by source geometry

Fix target unit u. Let P=P_u(C) be F08's projected union of unit-reduct source
models, in coordinates of the declared sources whose units can reach u. P is
a nonempty finite union of nonempty rational closed polyhedra. Every u-valued
term is a continuous rational CPWA function of these coordinates; syntactically
present but unused foreign bindings have no denotational dependence.

These coordinates can be used in u-valued arithmetic: for each source choose
one positive conversion path into u and divide its result by that path's
rational factor. This yields its numerical coordinate in u. Thus a rational
affine expression in the chosen coordinates is an available u-valued term.
This is the same explicit retyping contract as F08, not an inverse conversion
rule or a claim of coherent conversion cycles.

Say t is **natively Boolean in C at u** when a native zero-budget proof of

    d(t)=min(abs(t),abs(t−1_u)) <=[0] 0_u

exists. Since d is nonnegative and vanishes exactly at 0 and 1, U1 says this
is equivalent to t taking only these two values on P. Identify two such terms
when both native zero-budget comparison directions exist; by U1 this is exactly
equality of their functions on P. Interpret a term's zero set as its true event.

**B6 (all native Boolean observations).** If P has c connected components, its
native Boolean observations modulo this equivalence form exactly the powerset
Boolean algebra on those c components. In particular there are 2^c classes.
The operations are max for intersection, min for union and 1−t for complement.

### 1.1 Necessity and the finite component description

A continuous function from a connected set into {0,1} is constant. One proof
uses preimages: the preimages of neighborhoods of 0 and 1 would be disjoint,
nonempty, relatively open sets partitioning the connected domain. Hence a
Boolean term is constant on every component of P.

To see that there are finitely many components, write P=union_h P_h and draw
an edge between h and k when P_h intersects P_k. Every P_h is convex, hence
connected. A graph-connected cluster has connected union, by adding sets along
a spanning tree with nonempty intersections. Different graph clusters have
disjoint unions. Each cluster union and its complement in P are closed because
they are finite unions of closed sets, so each is also relatively open. These
clusters are exactly the connected components. This argument does not identify
different hidden case labels when their numeric domains merely share a name;
it checks actual intersections and covers duplicate or overlapping cases.

### 1.2 Sufficiency by an explicit rational CPWA separator

Choose any union A of components to be true and put B=P\A. Empty A or B uses
the constant 1 or 0. Otherwise describe each polyhedron in A by rational affine
rows a_hj*x<=b_hj and form its nonnegative violation term

    V_h(x)=max(0, max_j(a_hj*x−b_hj)),
    V_A(x)=min_(h in A) V_h(x).

For an empty row list use V_h=0. Then V_A=0 exactly on A. On B it is strictly
positive. Crucially, in this fragment there is a rational delta>0 with
V_A>=delta everywhere on B. To reconstruct that step, refine each polyhedron
in B by the finitely many affine cells of V_A. On every nonempty resulting
closed rational polyhedron V_A is affine and bounded below by zero. Its image
is a closed rational polyhedron on the line (rational polyhedral projection),
so its finite infimum is attained and rational. No cell can have minimum zero,
since A and B are disjoint. There are finitely many cells, so the least of
their positive minima is a positive rational delta. This is also an application
of F08's attained finite-bound theorem, not an assumption of compactness.

Now set

    b_A(x)=min(1, V_A(x)/delta).

It is a finite rational native term, equals 0 on A and 1 on B, and is Boolean
on P. U1 gives its Boolean-defect certificate and the native identities for
the Boolean operations. This proves sufficiency and the exact algebra claim.
There may be many global CPWA extensions of the same Boolean function on P;
the theorem identifies their relative equivalence classes, not their syntax.

### 1.3 Unit access and observation limits

The theorem uses P_u(C), not automatically the full source projection. For
example let x:U, with one conversion U->V of factor 1 and no return path.
Put two V-valued source cases x<=−1 and x>=1, written through that conversion.
The full numerical source is two separated rays. The U-reduct has no rows,
so its projection is all of R, connected. The term

    min(1,max((x+1)/2,0))

is Boolean on the full two-ray domain but takes 1/2 at the reduct point x=0.
It therefore has no native U-valued Boolean-defect certificate. A usable return
path restores access to the premises and the two-component distinction.

Even with all rows accessible, a connected source interval has only the two
constant Boolean classes. The Boolean-cube point-case construction in B1/B2
has 2^n components, hence realizes every Boolean truth function on n loss bits.
For a case family with overlaps, the number of case labels can exceed c; a
hidden case label is not an observable Boolean input.

This is a denotational expressibility theorem. It does not grant a deployed
policy access to an unknown source quantity or permit it to choose an action
by hidden case. Every native global proof still has one fixed literal query.

## 2. Approximate Boolean values have a sharp rounding boundary

Let 0<=epsilon<1/2 be rational. Suppose a native proof establishes

    d(t) <=[epsilon] 0.

Equivalently, on the reduct domain each value of t lies in
[-epsilon,epsilon] or [1−epsilon,1+epsilon]. The two intervals are disjoint.
Define the continuous native term

    R_epsilon(t)=min(1,max((t−epsilon)/(1−2*epsilon),0)).

**B7 (relative exact rounding).** R_epsilon(t) is natively Boolean and
abs(t−R_epsilon(t))<=epsilon has a native certificate on the same domain.
Moreover each connected component has one unique nearby Boolean value.

On the first interval the inner affine expression is <=0 and R is 0; on the
second it is >=1 and R is 1. The absolute error is at most epsilon in both
cases. U1 supplies both stated certificates. Continuity cannot cross from one
interval to the other along a connected component, which proves uniqueness.
There is no discontinuous threshold primitive: the term interpolates over the
gap, and the **source premise** says that its input avoids that gap.

The denominator is substantive. At epsilon=1/2, t=x on [0,1] meets the defect
bound but a connected domain cannot support a nonconstant exact Boolean term.
Thus no continuous rounding that maps the two endpoints to different bits can
have the same unrestricted guarantee at this threshold. The interpolating
rounder's global Lipschitz constant is 1/(1−2*epsilon); its divergence expresses
the loss of a separating gap, not a floating-point implementation accident.

The literal 0/1 encoding is a declared numerical presentation. For anchors
l<h use min(abs(t−l),abs(t−h)) and require epsilon<(h−l)/2. The corresponding
rounder interpolates between the two anchors over [l+epsilon,h−epsilon].
Affine changes of unit transport anchors and epsilon together as in S2; an
unchanged ordinary 0/1 test is not invariant under arbitrary unit rescaling.

## 3. Boolean-equivalent expressions can have very different stability

Let M be the sublanguage with constants 0,1, atoms, min, max and complement
1−t. Its implication abbreviation is min(1−a,b). This is one available
interpretation of Boolean syntax, distinct from the primitive residual away
from Boolean inputs.

**B8a.** Every M term is 1-Lipschitz in the maximum norm on its source vector.
Atoms have this bound, constants have zero bound, complement preserves it, and
min/max of two such functions also have it. The last step follows from
min(a,b)<=min(c,d)+max(|a−c|,|b−d|), and the analogous maximum inequality,
with the reverse comparison obtained by exchange. Induction introduces no
factor depending on depth or repeated occurrences of an atom.

Therefore, if x is within epsilon of a Boolean vector e, the value of any M
formula is within epsilon of its Boolean value at e. If x is in [0,1]^n and
two M formulas are Boolean-equivalent, their outputs differ by at most epsilon:
both lie in [0,epsilon] when the common Boolean loss is 0, or both in
[1−epsilon,1] when it is 1. Without the cube range, the triangle bound is
2*epsilon. The cube bound is sharp: excluded middle at x=epsilon versus the
constant true formula differs by epsilon for epsilon<=1/2.

**B8b (residual amplification).** For the equally Boolean-correct residual
interpretation define

    S(t)=res(1−t,t)=max(2*t−1,0).

It is Boolean-equivalent to t, since `not A implies A` is equivalent to A.
Its k-fold iterate for k>=1 is

    S^k(t)=max(2^k*t−(2^k−1),0).

Induction uses max(2*max(a,0)−1,0)=max(2*a−1,0). At t=1−epsilon in [0,1],
its deviation from the Boolean loss 1 is min(2^k*epsilon,1). Thus no common
positive input-error allowance gives a formula-independent small output error
for this class, even among formulas equivalent to the same single atom.
For k large enough the encoded false input near 1 receives output 0.

This is an exact analytic stability comparison, not an empirical training
claim and not a reason to delete the residual from the loss calculus. Residual
arithmetic has its own compositional purpose. It means the chosen extension
of Boolean syntax and the admitted input domain must be declared when using
Boolean interpretations as numerical or neural controls.
