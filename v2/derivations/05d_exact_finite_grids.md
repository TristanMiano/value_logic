# F09 optional reconstruction D — exact grids and their failure boundary

Research contributor: **Codex (GPT-6)**. September 30, 2026 UTC.
This continues the protected optional derivation block. The result concerns
explicit small sublanguages on an independent cube, not arbitrary source
contexts or the future integrated F11 reasoner.

## 1. An exact optimization theorem for lattice/complement terms

Let M_Q contain atoms x_1,...,x_n, rational constants from a finite Q subset of
[0,1] containing 0 and 1, min, max, and complement 1−t. The source domain is
the **entire** cube [0,1]^n in one unit. Put

    G = {0,1/2,1} union Q union {1−q:q in Q}.

For n=0 use the single empty tuple. Complements can be pushed to leaves by
1−min(a,b)=max(1−a,1−b), the analogous maximum identity, and double-negation
cancellation. Thus every term is a lattice polynomial in literals x_i, 1−x_i
and constants in Q union (1−Q).

**B9 (exact finite-grid optimum).** For every pair t,s in M_Q,

    max_(x in [0,1]^n) (t(x)−s(x))
      = max_(x in G^n) (t(x)−s(x)).

This is also the exact optimal native budget in the cube context, by F08 U1/U4.
The statement includes signed budgets, not only zero-budget validity.

### 1.1 Common order cells

List all the finitely many literals occurring in both terms, including the
constants. For each ordering permutation, intersect the cube with the weak
inequalities saying these literals occur in that order. The resulting nonempty
sets are bounded closed rational polytopes; their union is the cube. On each
cell, every min/max chooses a fixed literal. Equality ties do not cause a
problem because the tied literal values agree. Consequently t−s is affine on
each cell, so its maximum occurs at a vertex of that cell.

### 1.2 Why all those vertices lie in the grid

At a cell vertex, each active nonconstant equality has one of the forms

    x_i=0, x_i=1, x_i=q, x_i=1−q,
    x_i=x_j, x_i=1−x_j.

The last form includes i=j, which fixes x_i=1/2. Ignore constant equalities
that impose no coordinate restriction. Make a graph of the coordinates, with
an ordinary edge for equality and a reversing edge for complementation.

In a component with a unary anchor q, every coordinate is q or 1−q, hence in G.
In an unanchored component, an odd number of reversing edges around a cycle
forces the root coordinate to equal its complement, so all coordinates in that
component equal 1/2. In the remaining case, the signed relations are consistent
and the component has one free root coordinate: every coordinate is either
z or 1−z. Perturb z slightly in both directions. All active equalities remain
true, and all finitely many inactive inequalities remain true for a sufficiently
small perturbation. An active cube boundary would have been an anchor, so it
cannot block this two-sided perturbation. The supposed point then lies strictly
between two distinct feasible points and is not a vertex. This contradiction
exhausts the unanchored case. Every actual vertex therefore belongs to G^n.

Combining this fact with affine optimization on each cell proves B9. No claim
that arbitrary piecewise-affine functions maximize at the cube's own vertices
has been made: vertices of the **order refinement** include 1/2 and the supplied
constants, and those are essential.

### 1.3 Two useful specializations

With Q={0,1}, three values {0,1/2,1} per atom suffice to find every exact optimal
budget for this min/max/complement sublanguage. Every value at a grid point is
one of those three values, so the optimum is in {−1,−1/2,0,1/2,1}. This finite
model property is about numerical term inequalities over the cube; it does
not import a phase-one negation operator or a provenance interpretation.

If complement is omitted, there are no reversing edges and no need for 1/2.
For Q={0,1}, the ordinary Boolean grid {0,1}^n already gives the exact optimum.
Thus the **positive** Boolean fragment extends exactly from Boolean sources to
the full continuous cube for zero-budget entailment. This refines B1/B2: the
failure of excluded middle on an interval concerns complement, not a failure
of every Boolean relationship on that interval.

For a second reconstruction of the positive zero-budget result, suppose a
min/max term t exceeds s at some cube point. Choose a threshold strictly between
their values. Thresholding each input to 0 or 1 is a lattice homomorphism and
fixes the constants 0,1, so it yields a Boolean valuation at which the same
inequality fails. This proves zero-budget reflection without the vertex
argument; the vertex reconstruction above supplies the stronger signed optimum.

## 2. The domain contract is essential

Adding a correlated source row can invalidate the grid theorem even when all
terms remain in the positive sublanguage. On

    x>=0, y>=0, x+y<=1/2,

the term min(x,y) has maximum 1/4 at x=y=1/4. The only points of
{0,1/2,1}^2 satisfying the source rows give minimum zero. To prove the exact
maximum, min(x,y)<= (x+y)/2 <=1/4, and the displayed point attains it. The
new source facet creates a vertex of the refined domain outside the old grid.

One may analyze a new grid for specially restricted sources, or use the general
affine-cell method from F08. One may not silently apply the independent-cube
result to an arbitrary admitted joint source context.

## 3. A primitive residual defeats every fixed finite scalar grid

Let x range over [0,1]. Set r_0(x)=1 and

    r_(n+1)(x)=res(x,r_n(x)),
    f_n(x)=min(x,r_n(x)),  n>=1.

These terms use only one atom, constants 0 and 1, min and the actual residual.
They can be read as the Boolean formulas `p or (p implies ... implies false)`
with n repeated antecedents; the parentheses are right-associative. Every one
is a classical tautology at Boolean inputs, with zero loss at x=0 and x=1.

On [0,1], induction gives r_n(x)=max(1−n*x,0). The step uses x>=0:
max(max(a,0)−x,0)=max(a−x,0). Hence f_n is zero at x=0 and at every x>=1/n,
is positive on (0,1/n), and has exact maximum

    max f_n = 1/(n+1), attained at x=1/(n+1).

On [0,1/n], compare the two affine branches x and 1−n*x. Their crossing is
the displayed point; the first increases and the second decreases. Outside
that interval the residual is zero, establishing the global maximum.

**B10 (no fixed finite test grid for the residual extension).** For any finite
S subset of [0,1], there exists an f_n which is zero on every point in S but
strictly positive somewhere in [0,1]. If S has a positive element let d be its
smallest positive element and choose n with 1/n<=d. Otherwise any n works.
All positive grid values lie in the zero tail, and x=0 is also a zero. The
rational attaining point still refutes a zero-budget claim.

In particular n=2 gives zero at 0,1/2,1 but maximum 1/3 at x=1/3. Thus the
three-value test from B9 is not valid once the Boolean implication is translated
with the primitive residual. This is not merely a bad choice of three points:
the quantified finite-grid obstruction rules out every fixed finite S for the
unbounded syntax family. A grid depending on a bounded expression class or
explicit affine pieces is a different, potentially valid contract.

This distinguishes exact finite model tests from sampling. All displayed
formulas are finite native terms, but native proof acceptance still checks an
actual derivation. A grid result is usable only with the theorem's syntax and
domain hypotheses; passing a sampled trace is not itself a native certificate.
