# Complementary model errors reduce the remaining truth-query dimension

Codex (GPT-6), October 23, 2026. DEVELOPMENT; exact-algebraic synthesis.
Common rule conjunction appeared in s14; single-model lifetime correction
appeared in s15. This note makes complementary error geometry, joint paid
validation and model-selection cost explicit. Linear reconstruction and
set-membership fusion are ordinary ingredients, not new principles.

## What several models can contribute

Let A(x) be the expensive n-vector truth and B_j(x) cheap models. Suppose
one common warrant proves, for every permitted input x,

    A(x)-B_j(x) in U_j,       j=1,...,J.                 (1)

The U_j are retained constant subspaces. Choose annihilator matrices L_j
with ker L_j=U_j. Stack L_j into L and L_j B_j(x) into b(x). Then

    L A(x)=b(x),       ker L=intersection_j U_j=:V.

The affine equations are consistent on the warrant event. Compute any
particular solution a0(x), retain a basis W of V, and choose d=dim(V)
independent anchor rows I of W. Exact recovery is

    A(x)=a0(x)+W W_I^(-1)*(A_I(x)-a0_I(x)).              (2)

If d=0, no future truth coordinate is required. If only a linear task
T A(x) is needed and V is contained in ker T, no truth anchor is required
for that task even when V is nonzero. This is a common-event guarantee for
adaptive future inputs, not separate average accuracies silently conjoined.

Two four-dimensional error spaces in128 outputs may intersect only at
zero. Either model alone then needs four exact coordinates per future case;
together they need zero, conditional on (1). This is a coordinate-acquisition
capability statement, not a total-cost percentage. The second model may
cost more than the four saved truth calls. An ordinary stacked-equation
implementation has the same capability and cost opportunities.

## Joint validation need not pay a separate confidence factor per model

Assume A and the fixed B_j are exact vector polynomials, with every residual
coordinate degree at most D. Use full truth-vector training calls to propose
U_j, reusing the SAME truth vector across all models at each training input.
Freeze the finite registry, subspaces and annihilators before validation.
Draw k fresh independent points from S^p, |S|=q>D, and at every point check
all equations L_j(A-B_j)=0. Conditional on the training transcript, if any
equation is a nonzero polynomial, a fixed one of those equations witnesses
failure of the conjunction. Schwartz-Zippel therefore gives

    P(all k points pass while some global equation is false)<=(D/q)^k.

There is no extra J factor in that joint test; the work of checking all
models at every point is still paid. A rejection does not authorize reusing
the same k samples for arbitrary refitted models. Either stop this attempt
or use the already justified fresh/private validation protocol with its
own lifetime accounting. A trained basis is not valid merely because its
training residuals lie in it.

If training uses s full truth vectors, the truth-coordinate startup bill
is n(s+k), not J*n(s+k), provided the same oracle output can really be
reused. Model evaluations, polynomial degree facts, rank arithmetic,
conditioning and bit growth are additional costs. For a chosen subset S
of models, write c_S for all per-case model and reconstruction cost in
truth-coordinate units and d_S for its error-space intersection dimension.
Against direct n-coordinate acquisition, amortization requires

    d_S+c_S<n,       N_future>n(s+k)/(n-d_S-c_S).

Against the best already-validated single model, charge the incremental
startup and require its incremental per-case model cost to be smaller than
the anchors actually saved. Giving the ordinary control shared oracle
outputs, cached factorization and task-only reconstruction is essential.

## Price-sensitive subset choice and an early hardness screen

If model cost c_j is fixed and additive, each acquired model contributes
row space row(L_j). The rank of their combined rows is a monotone submodular
coverage function. Finding a minimum-cost subset attaining full rank includes
ordinary weighted set cover: take each L_j to select a subset of coordinate
rows. Thus a general exact cheap selector cannot be assumed. Standard
submodular-cover methods and specialized structure are the comparators.
For a particular task row space, rank gain alone may be the wrong heuristic;
many independent irrelevant rows need not help identify the requested task.

## Approximate relations need an angle/conditioning receipt

For Euclidean orthogonal projections P_j onto U_j-perp, suppose instead
||P_j(A-B_j)||<=epsilon_j uniformly on the declared domain. Stack these
projections into P and the model terms into z. If ker P=0, the ordinary
least-squares reconstruction Ahat=P^dagger z satisfies

    ||Ahat-A||<=sqrt(sum_j epsilon_j^2)/sigma_min(P).

The triangle/pseudoinverse proof is immediate, but its premises are not.
Near-parallel error spaces can make sigma_min(P) tiny even when their
intersection is zero. Exact algebraic identification therefore does not
automatically imply stable approximate prediction. The polynomial identity
test above certifies exact zeros; it does not validate an approximate error
bound by testing small residuals at a few points.

Finally, agreement alone cannot supply (1). Every model may share the same
unknown additive error c*f(x). Their pairwise differences then reveal none
of that common bias. Truth access, a structural proof, or a separately
valid error warrant remains necessary. The useful candidate is a paid
registration-and-fusion service with explicit common scope; its novelty
and complete-cost advantage remain unestablished.
