# Further boundaries of conditioned optimum receipts

Codex (GPT-6), s18 DEVELOPMENT. These are bounded consequences of the
attainer construction, assessed separately from its linear endpoint claim.

## Endpoints need not describe every possible value

Let B1 be the segment from(0,1) to(2,0), and B2 the segment from(0,2)
to(1,0). Choose one hidden point from each and take their exact convex hull.
Retain min x=0 and min y=0. Every interior point of either segment has both
coordinates positive, so the two receipts force either the pair
{(0,1),(1,0)} or the pair{(2,0),(0,2)}. The new minimum of x+y is therefore
either1 or2, with no intermediate value. The sharp endpoint interval[1,2]
is useful for monotone threshold decisions but is not the exact value set.
For example, the smallest possible (v-3/2)^2 is1/4, whereas replacing the
value set by its interval would give0. This is a limit on later nonlinear
use of a summary, not a failure of the endpoint algorithm.

## Concave new objectives preserve the generator reduction

For a concave function f on the relevant compact hulls,

    min_(x in conv{x_i}) f(x) = min_i f(x_i).

One inequality holds because each generator is feasible; the other follows
from concavity on every convex combination. Thus the same attainer DP and
covering sieve apply if each face table can supply l_i(T)=min f and
u_i(T)=max f. These subproblems are not automatically easy: minimizing a
general concave function over a polytope can be hard.

For the concrete piecewise-linear form f(x)=min_q(a_q dot x+b_q), with m
supplied pieces, each upper face value is one LP using an auxiliary scalar
z<=a_q dot x+b_q. Each lower face value is the minimum of m linear-program
values. At most n*2^k*(m+1) such optimizations therefore suffice before the
same finite covering calculations. This extends the exact computational
contract without assuming an efficient general concave minimization oracle.

For a convex f, the generator reduction fails: on the segment between-1
and1, f(x)=x^2 has minimum0 while both generator values are1. The earlier
convex-envelope results require their own proof and must not be imported
into this DP by merely replacing the face objective.

## Explicit inverse-optimal-value specialization

The unknown parameter is theta=(x_1,...,x_n), with each x_i in B_i. For
observation j, use the forward simplex program

    min_(lambda>=0, sum lambda=1) sum_i lambda_i*(h_j dot x_i).

Its value is exactly min_i h_j dot x_i. Hence this observation model is a
direct special case of the established inverse-optimal-value model in
Li--Cui, Example1.1; learning from scalar optima is not a new idea here.
The prospective contribution is the structured exact conditional endpoint
algorithm, its information-retention consequences and its limits. The
covering computation is likewise an application of established sieves.
