# Retaining scalar values without incorrectly conditioning a surrogate

Codex (GPT-6), s18 DEVELOPMENT. Extends convex_values.md. Ordinary robust
optimization, disjunctive programming and abstraction completeness are strong
controls; no generic new Bayesian or counterfactual semantics is claimed.

## A query-adequate family need not be an update-adequate model

Independently choose x_i in compact convex regions B_i and let the actual
source be H=conv{x_i}. For translates B_i=a_i+C, common translations P+c
give the exact lower and upper values of every single finite continuous
convex objective. They also give the same universally feasible core. They
need not include the actual hull and need not preserve joint value reports.

In one dimension let a1=-1,a2=1,C=[-1,1]. Observe the truthful scalar
min_H x=0. Actual compatible sources include every interval[0,t],0<=t<=2.
In particular the collapsed hull{0} is possible. Conditioning the common-
translation surrogate instead forces c=1 and keeps only[0,2]. It would
report min_H(-x)=-2 with certainty, although the correct range is[-2,0].
For f(x)=(x-1)^2 it would report value0 with certainty; the correct range
is[0,1]. A second truthful observation min_H(-x)=0 would falsely make the
conditioned surrogate empty. This is loss of joint information, not a
contradiction in the actual mathematical source.

## Exact conditioning on a bounded number of linear optimum receipts

Suppose k retained exact values are

    min_H h_j dot x = v_j, j=1,...,k.

Let P_v={x:h_j dot x>=v_j for every j}, and put B_i'=B_i intersect P_v.
Every generating point must lie in B_i'. Each minimum is attained by at
least one generating point, so choose an attainer assignment
a:{1,...,k}->{1,...,n}. In that branch replace region i by

    B_i^a = B_i' intersect {x:h_j dot x=v_j for all j with a(j)=i}. (C1)

Discard a branch if any region is empty. The original compatible source
family is exactly the union of the independent-selector families given by
these at most n^k branches. Every actual source supplies an assignment of
its attaining indices; every selector in a surviving branch has all values
at least v_j and at least one equality for each j, so has exactly the
observed values. Shared attainers and degenerate regions are allowed.

For a new finite continuous convex objective f, take the minimum of the
branch lower endpoints and maximum of the branch upper endpoints. The lower
endpoint in each branch is min f over conv(union_i B_i^a): convexity of each
region lets several convex-combination points from the same region merge
into one allowed generator. The upper endpoint uses the common-exposed-
direction construction in convex_values.md. For polytopal regions this gives
a finite exact procedure using their refined normal fans, including lower-
dimensional faces. It is not generally the old same-corner family after the
clipping in(C1).

With fixed k this separates the discrete attainer ambiguity from each
independent-region problem. It does not establish a generally cheap algorithm:
n^k can be large, normal fans can be complex, and exact arithmetic/optimization
must be paid. For k=1 there are at most n branches. No extra branch is needed
for a merely lower bound on a linear minimum; that just clips every region.
An upper bound requires at least one attainer below the bound and similarly
introduces an existential branch. Exact equality is stronger than an interval.

The hull-equality source contract is essential. If the unknown F merely
contains the generating hull and may contain arbitrary additional points,
an optimum need not be attained by any x_i. Then(C1) is unsound unless those
additional feasible points or witnesses are explicitly represented.

## Joint linear value envelopes have an ordinary compact formulation

For linear objectives h_1,...,h_k and nonnegative weights lambda_j, the
largest compatible weighted sum of their separately reoptimized values is
the convex optimization problem

    maximize sum_j lambda_j t_j
    subject to x_i in B_i, t_j<=h_j dot x_i for every i,j.    (C2)

For polytopal regions this is an ordinary linear program. Each selector
makes its largest admissible t equal to the componentwise minimum over
generators. Conversely every feasible t is componentwise below such a value
vector, so a nonnegative weighted maximum is unchanged. Thus(C2) describes
the downward closure of the attainable joint value vectors, not necessarily
their exact set or arbitrary signed scalarizations.

The potential useful contribution is a precise distinction between
query-adequate retained models and sound update rules, together with an
explicit bounded-attainer repair. The machinery is conventional and its
novelty/materiality remains open. A new name for conditioning or an incorrect
surrogate update is not the intended outcome.

## A small piece of retained witness metadata removes the attainer branching

If an acquired linear optimum receipt also names one attaining generator
index a(j), then(C1) has one specified branch rather than n^k possibilities.
Retaining k such identities uses at most k ceil(log2 n) bits in addition to
the scalar values and source binding. It preserves independent convex regions
after clipping, without retaining the full coordinate vectors of the
attainers. Multiple receipts can name the same generator.

The identity is part of the receipt's mathematical assertion. It must be
checked while the attaining point/source is available, or supplied by an
appropriately trusted value service. A guessed index from a fallible model
cannot remove all other branches. A conventional optimizer often returns
the full attaining point anyway; retaining it is a mandatory stronger
control, with its actual storage and subsequent-use costs. The comparison
is therefore a retention tradeoff, not an automatic solve-time or audit gain.

This gives a concrete design choice: retain values alone and pay for
attainer ambiguity later, retain the small certified incidence metadata,
or retain complete attaining vectors when their broader future value is
worth the storage. The ordinary attainer-aware method is the mechanism;
calling it value logic does not create an additional algorithmic advantage.
