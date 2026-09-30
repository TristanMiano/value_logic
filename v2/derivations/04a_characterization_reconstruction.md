# F08 reconstruction: arithmetic, dependencies and observable source information

Research contributor: **Codex (GPT-6)**, September 30, 2026 UTC.
Status: accepted same-assistant reconstruction at F08 scope; not an independent
review. See [04](04_characterization.md) and the
[measured work record](../work_logs/F08_2026-09-30_S1.md).

This pass starts again from the finite syntax and source inequalities. It
checks three places where a plausible completeness outline could hide a gap:
the rational linear certificate, the direction of unit dependencies, and the
information retained by global queries across a union of hidden cases.

## A. An elementary constructive linear alternative

All vectors and matrices supplied as data are finite and rational. Variables
range over finite reals. Equalities are represented by their two opposite
nonstrict inequalities. A polyhedron may be unbounded or lower dimensional.

### A1. Eliminate one coordinate while retaining row certificates

Consider inequalities in coordinates `(z,r)`. Partition them according to
the coefficient of r. Keep every row with coefficient zero. For each pair

    p*r + a*z <= b,      p>0,
    n*r + c*z <= d,      n<0,

retain the consequence

    (-n*a+p*c)*z <= -n*b+p*d.                       (A1)

It is the nonnegative combination `(-n)` times the first row plus `p` times
the second. If every original row carries its vector of nonnegative rational
coefficients in the initial rows, this new row carries the same combination
of those vectors. No inequality is divided by a quantity of unknown sign.

The projected system is exact. Necessity follows by adding the inequalities.
For sufficiency, fix z satisfying the projected rows. Each positive row puts
an upper bound `(b-a*z)/p` on r; each negative row puts a lower bound
`(d-c*z)/n` on r. A1 says each lower bound is at most each upper bound. There
are finitely many bounds. If both types occur, their maximum lower endpoint
and minimum upper endpoint enclose a nonempty closed interval. If only one
type occurs, a closed ray remains; if neither occurs, r is unrestricted.
Choose an endpoint, or zero in the unrestricted case. For rational z the
chosen r is rational. The zero-coefficient rows already hold.

Repeated elimination therefore computes an exact finite rational projected
system and nonnegative row-combination certificates for every output row.
Redundant rows may be retained. This is a mathematical construction; F08
does not implement a general elimination or proof-search engine.

### A2. Feasible rational witnesses and strict infeasibility rays

Eliminate every variable. If all resulting scalar inequalities `0<=beta`
hold, back-substitute as in A1 to produce a rational feasible assignment.
If the system is infeasible, a final row has `beta<0`. Its retained coefficient
vector lambda proves

    lambda>=0, A^T*lambda=0, lambda^T*eta<0.          (A2)

Conversely A2 contradicts every supposed model by taking that nonnegative
combination of its inequalities. Thus exactly one of a rational feasible
assignment and a rational strict ray exists. This proof also covers no
variables, redundant equalities, empty row sets and unbounded feasible sets.

For a live parent plus one empty sign child, separate the last coefficient k
of the ray. The parent's known feasible assignment excludes k=0. Hence k>0,
which justifies the positive division in the native exclusion construction.
The fact that the child is closed is relevant: a strict parent/guard language
would require a different alternative and a different receiving contract.

### A3. Exact upper bounds with native affine multipliers

Let `P={x:A*x<=eta}` be nonempty and `q(x)=c+v*x`. Introduce a fresh mathematical
coordinate y with the two rows

    y-v*x<=c,       -y+v*x<=-c.                     (A3)

This coordinate is used to derive a certificate; it is not a new declared
source or a trusted native operation. Eliminate x, retaining y. By A1 the
result is exactly the set of attained values q(P), with finite rational rows
`alpha_j*y<=beta_j`. It is nonempty because P is nonempty.

If no row has positive alpha, that set is unbounded above: its negative-alpha
rows give only lower bounds, and its zero rows cannot contradict nonemptiness.
If a positive-alpha row occurs, the upper endpoint is

    B = min_(alpha_j>0) beta_j/alpha_j.

Every lower bound is at most B, again by nonemptiness. The endpoint B belongs
to the projected system. It is rational; back-substitution at y=B gives a
rational attaining assignment x. There is no appeal to a vertex of P, which
need not have one, or to compactness, which is not assumed.

Take an output row that attains this endpoint and write its retained weights
as lambda on the source rows, rho on the first A3 row, and sigma on the second.
All are nonnegative rational. Cancellation of x and the remaining y coefficient
give

    A^T*lambda=(rho-sigma)*v,
    alpha=rho-sigma>0,
    beta=lambda^T*eta+alpha*c.

Thus `mu=lambda/alpha` is rational and nonnegative, `A^T*mu=v`, and

    c+mu^T*eta=B.                                  (A4)

For any rational requested b>=B, the same multiplier plus nonnegative slack
proves the request. Conversely any such multiplier proves an upper bound by
ordinary addition of the source inequalities. This establishes, constructively,

    (forall x in P, c+v*x<=b)
      iff (exists mu>=0, A^T*mu=v, c+mu^T*eta<=b).

The native emitter uses only row introduction, nonnegative rational scale,
addition, a constant comparison for c, exact affine rewrite and optional slack.
The mathematical y coordinate and its two defining rows disappear from A4.
They are never admitted as unsupported source premises to the returned proof.

### A4. Rational countermodels for a failed bound

If B is finite and B>b, its rational attaining assignment is a countermodel.
If q(P) is unbounded above, choose a rational y>b satisfying its finitely many
lower bounds and back-substitute. Thus a real countermodel always has a
rational counterpart here. An implementation timeout or unsuccessful search
does not exhibit either one.

These arguments reconstruct the precise finite linear facts required by F08.
They are standard elimination/linear-consequence facts, not a novelty claim.

## B. Unit dependence is semantic and directional

Let A(u) be the units with a path to u, including u itself. For every conversion
`v->u`, A(v) is a subset of A(u). An expression's arithmetic children otherwise
have its own unit, except for the bound expression of a let.

The useful induction statement is stronger than a statement about closed terms:
for any typed local environment, two source assignments and two local-value
environments that agree on all source/local coordinates whose units are in
A(u) give the same denotation to every well-typed expression of unit u.

Constants, sources and local references satisfy this directly. Same-unit
arithmetic and min/max apply the induction hypothesis to their children.
For conversion from v to u, agreement on A(u) implies agreement on A(v), and
the declared fixed factor preserves equality of the child denotations.

For `let z=a in b:u`, let a's unit be v. If v is in A(u), every unit in A(v)
is in A(u). Applying the induction hypothesis to a shows equal bound values;
the extended environments agree at all relevant locals, including z, so b has
the same denotation. If v is outside A(u), the possibly different new values
of z are irrelevant to the induction hypothesis for b. Shadowed locals are
overwritten in both environments, with the same typing. The right-hand side
of the binding is evaluated in the old environments.

This proof uses total, pure finite-real term semantics. It would fail for an
effectful language in which an unused binding changed a store or raised an
observable exception. F05 is not that language. Originally malformed children
are still rejected even if their value would subsequently be unused or
multiplied by zero.

For an affine expression, the same result implies that the collected
coefficient of every outside source is zero: vary that coordinate while fixing
the others. Hence a retained source row contains no numerical constraint on
outside coordinates, even if a dead lexical binding mentions one syntactically.

### B1. Ancestry is about premises, not arbitrary stored instructions

The native `same_difference` check requires all four compared expressions to
have the same unit before examining collected forms. The fact that `_form`
erases unit labels numerically therefore does not authorize a mixed-unit
rewrite. The sixteen constructor checks preserve premise units, except that
`convert` follows its named directed edge. Tracing the designated root backward
then puts every *used* row unit in A(u).

Unused checked steps can have other units. They do not enter the root induction.
Likewise a foreign value in the supplied feasibility witness supplies no rule
premise. Checking the entire original trace before pruning is necessary for
the receiving contract, but it does not turn unused evidence into a derivation.

### B2. Local extension is not hidden-case reassignment

The sign macros operate on a single-case context. Before aggregating their
outputs, localize the checked trace to its existing case h. All remaining
steps have case h and no `all_cases` constructor remains. If a larger context
has the same signature, observation and exact h rows, this trace can be
extended to it by updating the context fingerprint and rechecking every step.
Every row index still denotes the same h row. The added cases are not used.
The proof is still **local to h**; only the later all_cases rule makes a global
claim. Moving it to a differently constrained case, or relabeling its root
global directly, is not this lemma.

Conversely U1's necessity induction is domain-indexed, as in F07: each local
premise holds in its own reduct case; a global premise holds in their union.
One must not assume that an assignment in a union satisfies all case rows at
once. The written first outline has been tightened to state this explicitly.

## C. Global source information has a finite CPWA separator

Fix a signature and observation contract and a target u. Let I_u be the finite
list of declared source coordinates whose units reach u, and let pi_u project
onto them. Write

    P_u(C) = union_h pi_u(models of (C|u)_h),
    Q_u(C) = union_h pi_u(models of C_h).

Both are nonempty finite unions of closed rational polyhedra. For P, the
retained rows already depend only on I_u by section B. For Q, exact projection
follows from A1. Always `Q_u(C) subset P_u(C)`. These sets contain numerical
source coordinates; they are not declared policy observations.

For each source x:v in I_u choose a positive path of factor k_v to u. The term
`(1/k_v)*Phi_v(x)` has unit u and numerical value x. Consequently every rational
affine expression in the projected coordinates can be written in unit u.
This is an expression construction, not an inverse inference from a u premise
back to v. Finite min/max combinations remain in the existing syntax.

### C1. A separating expression

Suppose `Q=union_(h=1..m) Q_h`, with each polyhedron given as
`Q_h={y:a_hj*y<=b_hj for all j}`. Define

    V_h(y) = max(0, max_j(a_hj*y-b_hj)),
    V_Q(y) = min_h V_h(y).                           (C1)

For an empty row list set V_h=0. Every expression is finite rational CPWA;
binary min/max syntax implements the finite extrema. Each V_h is nonnegative
and vanishes exactly on Q_h. Thus V_Q is nonnegative and vanishes exactly on
the union Q. In particular, at any point outside Q, *every* V_h is positive
and their finite minimum is positive. Finiteness matters in this last step.

C1 is expressed using the same fixed expression in every hidden case. It
does not inspect the hidden case tag, and it does not select a different
deployed action according to that tag. It is a mathematical probe in the
admitted term language, not a claim that all these coordinates are observable
to a running policy.

If a nonempty rational polyhedral set P contains a real point outside Q, it
also contains a rational point outside Q. Pick a violated row in each Q_h at
that real point. The finite list of strict violations has a positive margin.
Choose a positive rational epsilon below all those margins and add the closed
constraints `a_hj*y-b_hj>=epsilon` to P. The resulting rational system is
nonempty, so A2 supplies a rational point. For a finite union P, use its case
containing the original point. This proves the rational qualification without
assuming that P has interior in the whole ambient space.

### C2. Exact global-theory characterization (U9)

For two admitted contexts C,D with the same signature and interpretation,
their entire native global unit-u consequence theories are equal if and only
if `P_u(C)=P_u(D)`. Context fingerprints and concrete proof objects can still
differ; theory equality compares matching expression-pair/budget requests.

If the sets agree, section B makes every unit-u query a function of these
coordinates, and U1 gives the same provable budgets. If the sets differ, take
a point of one outside the other (reverse C,D if necessary). The expression
V for the latter set satisfies `V<=[0]0` there and fails at the selected point.
U1 proves that request in one context and proves its nonderivability in the
other. A rational separating point exists by C1.

For local requests the corresponding statement uses each named case's
projected reduct, not their union. Global queries cannot distinguish a change
in the hidden partition that leaves this union unchanged.

### C3. Exact completeness criterion for one context (U10)

All semantically valid global unit-u comparisons in C have native proofs if
and only if `Q_u(C)=P_u(C)`.

Equality suffices by U1. If it fails, Q is a proper subset of P. Use V_Q from
C1. It satisfies `V_Q<=[0]0` throughout the original source, yet is positive
at a point of the reduct. U1's necessity direction excludes a native proof.
This is sharper than the graph criterion U7, which concerns *every* context
over a fixed signature. A particular inaccessible row can be redundant, so
failure of the graph criterion does not make every particular context lose
precision. No criterion is inferred from a bounded search failure.

### C4. A hidden-case gap invisible to all affine queries

Take x:U, one factor-one conversion U->V and no return path. Case `left`
has only `convert(x)<=-1_V`, witnessed by x=-1. Case `right` has only
`-convert(x)<=-1_V`, witnessed by x=1. The full projected source is

    Q=(-infinity,-1] union [1,infinity),

whereas its U-reduct is the entire line. Every nonconstant affine objective
`a*x+c` is unbounded above on both sets; a constant objective has the same
bound on both. Thus *all affine upper-bound queries* fail to distinguish them.

The admitted common expression

    V(x)=min(max(x+1,0), max(1-x,0))

vanishes on Q and equals 1 at x=0. Its full semantic optimum is 0 and its native
U optimum is 1. Indeed V<=1 everywhere: for x<=0 the first branch is at most 1;
for x>=0 the second is at most 1. This example shows why replacing the global
finite-union information by its convex hull is insufficient for the actual
CPWA query language. It is not merely another failure of a numerical budget.

If the same source inequalities are supplied in U, each case directly proves
its own hinge is <=0; min projection then proves V<=0 with the literal same
pair. `all_cases` joins those local proofs. The missing ingredient in the
original example is directed access to evidence, not a missing hidden-case
axiom or an inability of the expression language to represent the query.

## D. What this reconstruction does and does not establish

A1–A4 supply the rational certificates, countermodels and attaining endpoints
used by U1/U4/U5/U6 without a compactness or full-dimensionality assumption.
B checks lexical dependence and the precise native unit boundary. C adds an
exact information-preservation characterization, including a nonlinear probe
that affine comparisons alone would miss.

The reasoning concerns finite mathematical syntax and exact rational
certificates with sufficiently large resources. It does not assert that every
input finishes under the Python process's recursion/memory limits or a
producer's declared cap. Finite executable examples check the connection to
the current implementation; they do not formally verify Python or establish
an unrestricted theorem from testing. The F11 integrated reasoner, practical
complexity, full contribution audit and empirical interpretation remain open.
