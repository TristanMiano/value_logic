# Greatest-point shortcut for a restricted receipt class

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT control/extension.
Established greatest-element and max-closure machinery is credited below.
This does not change the frozen V19 claim or assert standalone novelty.

## Contract and the structural premise

Use the sign-reversed report convention

    a_j <= max_i h_ji(x_i) <= b_j,

where x_i lies in a nonempty compact rational ordinary polytope B_i and h_ji
is affine with nonnegative coefficients. The future readout is
q=min_i f_i(x_i), with affine f_i also having nonnegative coefficients.
The original minimum-report format is recovered by g_ji=-h_ji and bands
[-b_j,-a_j]. No monotonicity of that negated g is assumed.

Absorb every upper report inequality into each block:

    P_i = B_i intersect {h_ji(x_i)<=b_j for every j}.

The key premise is that every nonempty P_i has a **greatest point** p_i:
x_i<=p_i componentwise for every x_i in P_i. This premise is stronger than
having some maximizer of the sum of coordinates. It may be supplied with
coordinatewise dual bounds and a matching feasible point, with all those
certificates charged.

A cheap sufficient syntactic class has at most one positive coefficient in
each row of B_i, and at most one nonzero coefficient in each nonnegative
form h_ji. Constant forms are allowed. Then every row of P_i has at most one
positive coefficient. Such a half-space is closed under coordinatewise max:
if the row has a positive coefficient, select the input point attaining that
coordinate's maximum; every other coefficient is nonpositive, so increasing
those coordinates preserves the inequality. An all-nonpositive row is even
more direct. Intersections preserve max-closure.

A nonempty compact max-closed set has a greatest point. For each coordinate
take a point attaining its maximum and take the coordinatewise maximum of
these finitely many points. The result is feasible and dominates the set.
It is the unique maximizer of the sum of coordinates. Thus **one LP per
block**, maximizing that sum over P_i, finds p_i in the syntactic class.
An empty P_i is detected by an actual infeasibility certificate.

Max-closure and the sum-objective construction are established results,
not discoveries here. The receipt-specific consequence follows next.

## Exact projections without receipt-subset enumeration

Let p=(p_i)_i. The source set S is nonempty if and only if all P_i are
nonempty and max_i h_ji(p_i)>=a_j for every receipt j. Necessity follows
from monotonicity and x_i<=p_i. Sufficiency follows by using p itself.

For a chosen block i, define its forced receipts

    J_i = {j: max_{r!=i} h_jr(p_r) < a_j},

using max over an empty set=-infinity when n=1. Then the exact projection
of S onto block i is the ordinary polytope

    Z_i = P_i intersect {h_ji(x_i)>=a_j for every j in J_i}.     (G1)

To prove necessity, a receipt in J_i cannot be witnessed by any other block,
since its greatest point already misses a_j. To prove sufficiency, pair any
x_i in Z_i with p_r in every other block. Each forced receipt is witnessed
by block i; every other receipt has an outside greatest-point witness.
All upper inequalities remain satisfied. This is an exact projection claim,
not an assertion that independent choices from all Z_i jointly satisfy S.

The lower endpoint of the future range is consequently

    L = min_i min_{x_i in Z_i} f_i(x_i).                       (G2)

This takes at most one additional LP per block. Pick an attaining block i
and point z_i, and pair it with all outside p_r to obtain a source z. Its
future minimum equals L: it is at most f_i(z_i)=L and cannot be below the
global minimum in(G2).

Since every f_i is nondecreasing, p attains the upper endpoint

    U = min_i f_i(p_i).                                      (G3)

## Why there are no holes, and how to give a rational source

For every x in S, the segment x(t)=(1-t)x+t*p stays in S. It stays in the
ordinary convex product P; each coordinate only increases, so every retained
lower max-report remains true. Thus S is star-shaped with center p. In
particular it is path-connected, and any continuous scalar readout has an
interval image. Compactness makes that image closed and bounded.

For the present readout, S therefore has exact image[L,U]. More explicitly,
on the segment from the lower source z to p write

    f_i(z_i+t*(p_i-z_i)) = A_i+t*D_i,  with D_i>=0.

For rational q in[L,U], take

    t=max(0, max_{i:D_i>0} (q-A_i)/D_i).

Every zero-slope line has A_i>=q because q<=U. Also0<=t<=1. If q>L,
one positive-slope line attains the maximum and equals q while all other
lines are at least q. If q=L, t=0 works. Hence the segment source has
minimum exactly q and is rational. No search over winner assignments is used.

## Costs, certificates, and limits

In the syntactic class, a consistent input needs **2n local LP optimizations**:
n greatest-point LPs and n lower-endpoint LPs. Forming all P_i and forced
constraints costs input-linear work plus O(nk) scalar comparisons, using
largest/second-largest outside report values with ties handled. Input reading,
LP bit complexity, dual checking and source output are charged. The output
has one interval; rational witness reconstruction uses the retained lower
source, greatest source and O(n+sum_i d_i) arithmetic work.

An exact LP oracle can supply a primal optimum and matching nonnegative dual,
or Farkas infeasibility. A numerical proposal implementation can refuse.
The existing producer sometimes makes a second numerical call to obtain a
Farkas vector; count that extra call explicitly on inconsistent inputs.
The2n statement is the mathematical optimization-query bound and, for this
producer, the intended count on successful feasible inputs. It is not a
machine-time or fee percentage, and the ordinary shortcut is identical.

Without the syntactic condition, a sum maximizer need not be greatest.
For the triangle x,y>=0, x+y<=1, both(1,0) and(0,1) maximize the sum;
neither dominates the other. Without monotone observations, p can miss a
receipt that a smaller point satisfies: max(-x_1,-x_2)=0 is feasible on[0,1]^2
although it fails at p=(1,1). Without monotone future readouts, p need not
maximize the future minimum: with max(x_1,x_2)=1 and future min(-x_1,2),
the true range is[-1,0] but the value at p is-1.

The noisy-envelope example has a two-positive-coefficient upper sum row
and a nonmonotone future form. It is outside this shortcut's contract.
Its disconnected image therefore does not conflict with the connectedness
argument. More generally, the row test is sufficient, not necessary for a
greatest point; failure of the test does not prove that holes exist.

## Closest established structure

[Dlask2024](https://link.springer.com/article/10.1007/s10479-024-05980-z),
section1.1, Remark2/equation1 and Theorem4, explicitly gives greatest-element
existence for bounded closed max-closed sets, recovery by a strictly increasing
objective, and the one-positive-coefficient row characterization, crediting
earlier work. Proposition1's proof was also read. Those facts fully account
for the shortcut's base machinery; its projection and segment consequences
are the elementary adaptation written above. No projection convergence-rate
claim is imported, and this is not a general solution of max-closed semilinear
constraint satisfaction.

Disposition: a stronger ordinary structural control and an implementable
restricted service branch. Standalone contribution novelty UNASSESSED.
It helps state precisely when the general exponential receipt method is
unnecessary and when coupling that defeats the greatest point can matter.
