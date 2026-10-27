# Exact receipts admit a second parameterization

Codex (GPT-6), October 26, 2026. DEVELOPMENT. Constructive ordinary-control
screen motivated by [local dimension](local_dimension.md). No novelty
claim is assigned to branching on affine equalities.

## Many exact receipts, few uncertain directions

Permit even a jointly constrained source x in a nonempty compact rational
polytope B in R^D. There are k exact observations

    min_(i=1,...,n) g_ji(x) = v_j,

where every g_ji is affine. First intersect B with all universal lower
inequalities g_ji>=v_j, obtaining the convex polytope Q. The remaining
condition for each j is the union of n affine hyperplanes g_ji=v_j.

Maintain a list of affine subspaces, initially {R^D}. For each observation,
inspect every current subspace L. If any one of its n affine equations is
identically zero on L, this observation already holds throughout L: keep
L. Otherwise replace L by its nonempty intersections with the n equations.
Each surviving child has strictly smaller dimension. Empty intersections
are discarded. Duplicate subspaces may be merged, but merging is optional
for correctness and for the following tree bound.

Every branching node has at most n children and a root-to-leaf path has at
most D strict dimension decreases. Therefore at every stage there are at
most n^D subspaces; more precisely n^min(k,D) before optional merging.
Zero-dimensional subspaces either survive unchanged or are discarded.
Induction on processed observations proves that their union is exactly the
intersection of the observed equality disjunctions. A simple implementation
uses O(k*n^(D+1)) affine containment/intersection operations, with their
rational linear-algebra cost explicit. Input scanning is not omitted.

If the coefficient normals of all g_ji span rank r<D, every dimension
drop increments the rank of equations from that span, giving n^r instead.
This rank can be computed by Gaussian elimination. Arbitrary coupling in B
does not invalidate the argument. The construction is exponential in this
rank and number of alternatives, rather than in the number of receipts.

For each final L, intersect it with Q and compute the full range of a new
minimum V(x)=min_i f_i(x). The lower endpoint is min_i min_(Q intersect L)
f_i; the upper endpoint is one epigraph LP maximizing z subject to
z<=f_i(x). Nonempty Q intersect L is compact and convex, hence its
continuous scalar image is the entire interval between those endpoints.
The union has at most n^r intervals and uses at most (n+1)*n^r LP solves,
including feasibility detection. Source witnesses follow from the LP
optimizers and continuity along their joining segment; because V is a
minimum of affine functions, a requested value can be located exactly on
that segment by its finitely many affine pieces. These are ordinary LP
and affine-arrangement operations, with no unit-cost large arithmetic.

This is a useful alternative to AR1 when k is large and r small. AR1
instead allows interval receipts and has its stronger dependence on n
under independent blocks. Neither algorithm dominates the other on every
input, and neither is compared with an identical implementation as if it
were a weaker competitor.

For completeness, the segment witness needs no numerical root finder.
Let x^- attain the lower endpoint a and x^+ attain the upper endpoint b.
For a requested q in[a,b], take t=0 if q=a. Otherwise set

    t = max_{i: f_i(x^-)<q}
        (q-f_i(x^-))/(f_i(x^+)-f_i(x^-)).

The index set is nonempty, each denominator is positive, and t is in[0,1].
At x=(1-t)x^-+t*x^+, every affine f_i is at least q and at least one is
exactly q. Thus V(x)=q, using rational arithmetic and O(n) evaluations
after the endpoint values are known.

## Exact conflict certificates from ordinary algebra and convexity

There is also a finite conflict bound independent of k. Express all old
normals in r independent coordinates y, and project B to the compact
convex set K in those coordinates. Define

    p_j(y) = product_(i=1,...,n) (g_ji(y)-v_j).

Each polynomial has degree at most n. Select a linear basis of their
coefficient vectors; at most h=binom(r+n,n) receipt polynomials suffice.
Their common zero set is the zero set of every p_j, since every omitted
polynomial is their linear combination. This is the standard polynomial
coefficient-space argument of De Loera--Petrovic--Stasi, Theorem4.11.
The branching argument above writes this zero set as a union of at most
n^r affine subspaces L (including the whole space when appropriate).

Suppose all receipts together are inconsistent. On each such L, the
intersection of K with all lower halfspaces g_ji>=v_j is empty. Apply
ordinary Helly in L: at most dim(L)+1 of these halfspaces, with K fixed
as background, suffice to make that intersection empty. If K already
misses L, none are needed. Select the receipts supplying these halfspaces.
Together with the coefficient-basis receipts, they form an inconsistent
subcollection of size at most

    binom(r+n,n) + (r+1)*n^r.

Indeed, their equality polynomials already force a point into one of the
listed L, and their selected lower inequalities exclude it there. Taking
an entire receipt only adds constraints, so grouping inequalities by
receipt does not invalidate the certificate. This bound is deliberately
loose. It is an existence and constructive-algebra result, not a small
bit-size or efficient minimal-core guarantee. Computing the projected K
explicitly is unnecessary: feasibility and separating subsets can use
the original B with linear equalities. Rational certificates must still
pay their representation and linear-algebra costs.

General finite-Helly consequences for uniformly bounded unions of convex
sets already appear in Alon--Kalai1995. No new generic Helly principle is
claimed. This explicit specialization helps distinguish exact receipts
from the following noisy example.

A small conflict certificate does not mean the entire feasible source has
a bounded receipt basis. For n=2, min(0,h_j(x))=0 simply imposes h_j(x)>=0.
In two dimensions these can describe polygons with arbitrarily many
essential facets. Nor does the certificate remove the cost of inspecting
the k input observations.

## Interval receipts can have arbitrarily long minimal conflicts

The dimension-drop argument genuinely uses exact equality. Here is a
two-variable construction showing why a small universal conflict basis
cannot simply be carried to interval receipts.

Take x,y in[0,1], an integer N>=1, and epsilon=1/(4N). For i=0,...,N-1
require the two disjunctions

    A_i: x <= i/N-epsilon OR y <= 1-(i+1)/N,
    B_i: x >= (i+1)/N+epsilon OR y >= 1-i/N.

They are interval-minimum observations [-2,0] on the two displayed
affine residuals (use x-threshold and y-threshold for A_i, and the
negated residuals for B_i). The lower endpoint -2 is automatic throughout
the source square. Thus each configuration has only one uncertain scalar.

For every x in[0,1], some i has
i/N-epsilon < x < (i+1)/N+epsilon. That pair forces simultaneously
y<=1-(i+1)/N and y>=1-i/N, so all2N observations are inconsistent.
If A_i alone is removed, x=(i+1/2)/N and y=1-i/N satisfy every remaining
observation. If B_i alone is removed, use the same x and y=1-(i+1)/N.
The neighboring thresholds are separated because epsilon<1/(2N).
Hence all2N observations are essential to the contradiction.

This is an elementary constructed lower bound for minimal conflict size,
not a time-complexity lower bound. It does not imply that checking these
particular two-dimensional instances is difficult. It rules out a bound
depending only on the number and dimensions of configurations for general
interval-receipt conflict certificates.

## Finite algorithm screen

The precommitted exact_flat_probe.py passed54 one/two-dimensional rational
cases against2,448 complete witness assignments, including coupled source
inequalities and constant affine responses. Six cases were inconsistent;
162 source witnesses passed. This particular seeded panel had no
disconnected output ranges. The same run checked92 deletion witnesses for
six explicit noisy-conflict families. It took147,689,200ns. The shared
Gaussian-elimination/vertex helper limits independence; this is a small
implementation screen, not confirmation of the general theorem or the
Helly certificate bound. Source, input and outcome hashes are retained.
