# Partial response blocks and disjunctive model information

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; separate application of
N16-C, conventional convex minimax and disjunctive robust optimization.
No standalone novelty or promotion claim is made.

## Convex partial information has a scalar saddle formulation

Instead of retaining one full C, suppose truthful linear observations and
spectral brackets restrict it to a nonempty compact convex set K satisfying
epsilon I<=C<=(1-epsilon)I for a fixed epsilon>0. Fix c and E>0.
The unknown source may have any compression in K. Its exact upper endpoint is

    sup_(C in K) inf_(0<=r<=E/h) tr(V U_(E/r)(C)),      (P1)

with value1 at r=0, V=cc^T and ||c||=1. For each fixed r the objective
is concave in C by operator concavity of U; for each fixed C it is convex
in r by [the perspective representation](parameters.md). It is continuous
on the two compact domains, including r=0 because of the uniform spectral
brackets. [Sion's Theorem3.4](https://msp.org/pjm/1958/8-1/pjm-v8-n1-p14-p.pdf)
therefore exchanges sup and inf.
The resulting outer scalar objective sup_C tr(V U_(E/r)(C)) is convex.

Similarly, write the lower parameter as t=1/r-1 on 0<=r<=1/(1+h),
with value0 at r=0. The lower objective is convex in C, concave in r
and continuous on the compact domains. Hence

    inf_(C in K) sup_r tr(V L_(1/r-1)(C))
      =sup_r inf_(C in K) tr(V L_(1/r-1)(C)).          (P2)

The exactness over sources follows by applying N16-C to each C and then
optimizing C. Compactness supplies an optimizing C, and its finite endpoint
witness supplies a finite source. This imports ordinary minimax; it is not
a new theorem about arbitrary partial or nonconvex information sets.

At a fixed positive d, the inner problems also have familiar Schur forms:
U_t(C)=(a/d)[I-(I+dC)^(-1)] and
L_t(C)=(a/d)(aI-dC)^(-1)-I/d. Their inverse quadratic epigraphs are small
LMIs. At d=0 the objectives are linear. Thus partial-block acquisition can
be analyzed with ordinary convex optimization without pretending every
entry was purchased. The scalar-only closed formula is no longer free of
an inner optimization over K.

## Convexifying two warranted hypotheses can lose a decision

Take E=1/2, so h=1, c=(1,1)/sqrt(2), and let a source warrant state
that its retained block is one of

    C_1=diag(1/100,61/100),  C_2=(3/10)I.

There need be no belief about which is true. The warrant that one is true
is essential; two fallible guesses without it give no universal guarantee.
For C_1, the feasible upper parameter t=2 gives

    tr(V U_2(C_1))=3388/6345<3/5.

For C_2, the cap parameter t=1 gives the sharp upper endpoint3/5.
Therefore the disjunction certifies F(N;Wc)<=3/5 for every warranted
edit. In particular it certifies the strict threshold F<603/1000.
The same certificate need not use the same t for both hypotheses.

Now replace the two-point information set by its convex hull. It includes

    C_bar=(1/4)C_1+(3/4)C_2=diag(91/400,151/400).

Here s=c^T C_bar c=121/400 and m=c^T C_bar^2 c=15541/160000.
Since m<s/3, the N16 upper cap condition holds strictly. Its exact,
finitely attained upper value is therefore

    2s=121/200=0.605>0.603.

The convexified information class cannot certify the same threshold. This
is an explicit counterexample to exchanging the optimizations in P1 for
an arbitrary nonconvex K: its convex hull has an upper endpoint at least
0.005 greater than that of the two-point set. The unit here is the ridge
objective, not a probability, computation count or fee.

## Relation to the broader program

The example uses several possible models through a warranted disjunction,
without selecting a single fully trusted model or assigning probabilities.
It shows exactly which model information a computational relaxation discards.
Ordinary disjunctive robust optimization preserves that information and
ties the resulting guarantee. There is no philosophical separation from
ordinary methods, no learning advantage and no new economic comparison.
Its value is a small, explicit decision consequence and a warning against
silently changing the information class while applying a minimax theorem.

[partial_check.py](partial_check.py) and [partial_result.json](partial_result.json)
verify all three rational certificate calculations using the unchanged s16
checker, plus the strict cap condition for C_bar. The first two verdicts
are `below`; the convex-hull receipt is `unresolved`. The latter verdict
alone is not an impossibility proof: the finite adverse source comes from
the proved cap attainment and its checked premise. Runtime was665,300 ns
on Python3.12.14. No comparison of solver times is claimed.
