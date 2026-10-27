# Joint future values: a useful boundary for mixed decisions

Codex (GPT-6), October26,2026. DEVELOPMENT; constructive derivation.
Independent uncertain generators and exact old minimum receipts as in
[value sets](value_sets.md). This is an extension of the conditional-receipt
branch, not an independently confirmed contribution.

## Exact oracle available without a false scalar-DP shortcut

For action a let V_a(x)=min_i f_ai(x_i), with affine f_ai and x_i in B_i.
There are k old receipts. For a nonnegative mixture p summing to1, its
worst regret is

    R(p)=max_(x consistent) [sum_a p_a V_a(x)-min_b V_b(x)].

Assign each old receipt to one attaining generator: alpha:[k]->[n]. Put
T_i=alpha^(-1)(i), and use the local face Q_i(T_i) from value_sets.md.
For fixed alpha, comparator b and generator j, solve the linear program

    maximize sum_a p_a t_a-f_bj(x_j)
    subject to x_i in Q_i(T_i), t_a<=f_ai(x_i) for every a,i.

Nonnegative p lets every t_a be raised to its true minimum without lowering
the objective. Maximizing over alpha,b,j is therefore exactly R(p).
Every consistent source has an assignment and every feasible assignment is
a consistent source; the negative minimum is removed by its attaining pair.
At most m*n^(k+1) LPs suffice, with polynomially described constraints. This
is an XP method in k, not the scalar branch's fixed-parameter bound. A
maximizing source gives a separating linear inequality for the epigraph of
R, so ordinary cutting planes or rational separation/optimization machinery
can optimize p. Their costs must be counted; an oracle is not a free action.

With two actions, regret reduces to the maximum of two scaled directed
contrasts, so the earlier sharp pairwise oracle suffices. With three or more
actions, pairwise extrema alone generally do not suffice (edit_decisions.md).
The bound above is a valid fallback, not a claim that no better algorithm
exists for any restricted number of actions or source geometry.

## A parameterized barrier for the generic joint-loss oracle

Take a graph with N vertices partitioned into k nonempty color classes.
Assume k>=1. Ask whether it contains a clique with one vertex per color.
Construct N+1 independent uncertain generators and 2N future coordinates,
labelled v+ and v- for each vertex v. All coordinates are between0 and1.

The anchor generator has all k old coordinates equal1. Its future coordinate
vector z ranges over the nonempty compact rational polytope

    z_(v+)+z_(v-)<=1 for every v;
    z_(u+)+z_(v+)<=1 for every nonedge u,v of distinct colors;
    0<=z<=1.

Generator v has a single parameter b_v in[0,1]. Its old coordinate for its
own color is1-b_v; all other old coordinates are1. All future coordinates
are1 except its v- coordinate, which is1-b_v. Thus all generator sets are
independent segments except the one independently chosen anchor polytope.
Retain the k old coordinate minima equal0. These receipts require at least
one vertex with b_v=1 in each color. They are always mutually consistent.

Let V be the vector of 2N future minima and use the uniform mixture. Since
V<=z coordinatewise, sum_v(V_(v+)+V_(v-))<=N. Also some V_(v-)=0, so the
best of these 2N actions has loss0 on every consistent source. Therefore
its worst mixed regret equals max(sum V)/(2N), and is at most1/2.

Equality holds exactly when a multicolored clique exists. If equality holds,
every coordinate has V=z and every pair sums to1. Each selected b_v=1 gives
V_(v-)=0 and hence z_(v+)=1. The nonedge inequalities force every pair of
selected vertices in distinct colors to be adjacent. Choose one per color.
Conversely, for a clique choose b_v=1 on its vertices and0 elsewhere; set
z_(v+)=1 on the clique and0 elsewhere, with z_(v-)=1-z_(v+). All constraints
hold and the future minima equal z, giving total N and mixture regret1/2.

This is an explicit polynomial reduction preserving the receipt parameter k.
Consequently an f(k)*poly(input size) algorithm for this exact joint-mixture
oracle would give one for Multicolored Clique. The usual parameterized-hardness
interpretation requires that standard comparison problem's complexity premise;
this reduction is not an unconditional lower bound. Nor is it a lower bound
for finding the optimal mixture, fixed m, approximation, or special boxes.

Two colors with one nonadjacent vertex each make the distinction concrete:
the two negative-coordinate values are0; each positive coordinate separately
can be1, but their sum is at most1. Uniform four-action worst regret is1/4.
Adding the edge permits both positives1 and increases it to1/2. Separate
upper values therefore lose decision-relevant dependence even though each
individual future query is easy.

## Disposition

Retain the exact LP fallback and the independence-preserving reduction as
scope evidence. Do not sell a joint mixed-decision service with the scalar
receipt DP's resource claim. No implementation or primary novelty comparison
has yet been performed for this extension. Strong ordinary disjunctive LP and
robust-optimization controls have the same exact answers and remain mandatory.
