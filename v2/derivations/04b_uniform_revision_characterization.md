# F08 optional extension: one finite proof can remain optimal under RHS revision

Research contributor: **Codex (GPT-6)**, September 30, 2026 UTC.
Status: accepted optional F08 result with fresh reconstruction and finite checks.
This is optional work within F08's protected derivation block, as requested by
the author. It is not an implementation of the F11 integrated reasoner.

## 1. Question and a failed shortcut

The pointwise theorem U1 says that each finite optimal bound has a native proof.
It does not, by itself, give a single proof that remains optimal when source
row bounds change. Infinitely many individually optimal proofs could in
principle be needed. F07 proves sound replay of a retained proof, which is
also weaker than optimal replay.

An initial attempted shortcut was to replay the affine-cell construction from
[04](04_characterization.md). It does not establish uniform optimality.
Discharging a guard internalizes current row budgets as term literals; later
envelope proofs and selected alternatives can retain choices made at that
particular parameter. Replaying their budgets is sound, but their sensitivity
envelope can exceed the newly optimal bound. Pointwise completeness is not an
argument that this compiler is uniformly optimal.

The alternative below uses a max-of-mins affine representation. Each inner
minimum has a linear optimization problem that is feasible whenever the
source is feasible. Its finite dual vertices give a complete retained set of
native arguments, without parameter-dependent empty sign-cell choices.

## 2. Fixed revision family

Fix the signature, positive conversion factors, interpretation and observation
contract, ordered hidden case names, source row directions and row units, and
one closed literal query pair t,s:u. Only the normalized rational row budgets
eta may change. Every context considered must still supply a feasible rational
witness for every original case. No claim is made about an inconsistent
context, changed observation policy, new source coordinate or altered matrix.

For the target u retain the rows whose units reach u. Convert each such row by
a chosen positive path to u. In case h write the resulting numerical system

    A_h*x <= theta_h,

where `theta_hi=k_hi*eta_hi` and `k_hi>0` is fixed. Inaccessible original rows
do not appear. These systems are nonempty on every admitted revision.

Let `f(x)=t(x)-s(x)`. The unit-directed optimum is

    B(eta) = max_h sup_(A_h*x<=theta_h) f(x).

The coefficients of f and every A_h are fixed. The theorem concerns this
native optimum; it equals the full-source optimum only under the separate
completeness conditions established in U7 or U10.

## 3. A finite max-min affine normal form

After certified retyping and finite lexical expansion, f is a same-unit CPWA
expression. It has a finite representation

    f(x) = max_(i in I) g_i(x),
    g_i(x) = min_(j in J_i) (a_ij*x+c_ij),           (N)

with nonempty finite I,J_i and rational affine pieces. This can be constructed
directly from syntax; it is not a representation guessed from sampled values.

An affine expression is one clause with one leaf. A maximum concatenates the
two lists of clauses. A minimum pairs each clause of the first expression
with each clause of the second and concatenates their inner leaf lists. An
addition pairs outer clauses and then pairs their leaves, adding the two
affine expressions. Positive scaling scales every leaf. For negative scaling,
negation interchanges min and max; distribute a finite min of maxima into a
max of minima by choosing one leaf from each maximum. Zero scaling becomes
the constant zero. Expand residual as `max(b-a,0)` before applying these steps.
These transformations may cause large expansion, but each is finite.

### Native equality is a separate obligation

Ordinary numerical equality of N is not enough to authorize a rewrite through
the checker's opaque nonlinear atoms. There are source-free native proofs of
the required algebraic identities:

* Translation: `max(a,b)+c=max(a+c,b+c)`, and the min version. One direction
  adds the same c to the two lattice injections/projections. For the reverse,
  subtract c in the two displayed bounds by exact difference rewrites, apply
  the appropriate common-bound rule, and add it back by another rewrite.
* Positive homogeneity: scale the two injections/projections for one direction;
  for the reverse divide those for the scaled terms by the fixed positive
  scalar, use the common-bound rule, and scale back. The zero case is an exact
  constant equality.
* Negation: reverse both injections/projections using native `negate`, then use
  the dual common-bound rule. This proves `-max(a,b)=min(-a,-b)` and its dual.
* Distributivity: F06 already emits a source-free proof of
  `min(ReLU(b),ReLU(c))<=ReLU(min(b,c))` via its fixed two-variable
  `positive_min` lemma. The reverse follows by the two min projections,
  monotone max congruence and min_common. Translate by a to obtain
  `min(max(a,b),max(a,c))=max(a,min(b,c))`; negation gives the dual law.

All these equality proofs have budget zero. The generic positive-min lemma
has a finite native trace before arbitrary term substitution; it does not
require running a new affine sign split on a nonlinear substituted guard.
F07's checked closed-term substitution supplies that instantiation. Iterating
these identities therefore certifies N without using U1 as an equality oracle.
The source-free trace stays at zero budget throughout every RHS revision.

The finite-list notation also needs associativity, commutativity and repeated
leaf elimination; these are native equalities, not extra normalization rules.
For example, each of a,b,c has a zero-budget injection into
`max(a,max(b,c))` (compose injections for b,c). Two applications of max_common
then prove `max(max(a,b),c)<=max(a,max(b,c))`. Reverse the roles for the other
direction. Swapping two inputs uses the same two injections and max_common;
idempotence uses max_common on two identities and either injection. Min uses
the dual projections/min_common construction. Repeated applications justify
any chosen binary bracketing of the finite lists. No equality of differently
bracketed opaque min/max atoms is assumed by `_form`.

## 4. Each minimum clause has a parameter-independent dual

Fix h and i. The source is nonempty and each affine leaf is finite at every
point. Therefore the following lifted linear program is feasible:

    maximize z
    subject to A_h*x<=theta_h,
               z-a_ij*x<=c_ij for every j in J_i.   (P_hi)

Its supremum is exactly `sup g_i(x)`. The scalar z is a mathematical auxiliary
for deriving coefficients; it will not be introduced as an unsupported native
source. Applying the elementary affine-consequence construction in
[04a, A3](04a_characterization_reconstruction.md) gives the dual set

    D_hi = { (lambda,alpha):
               lambda>=0, alpha>=0,
               A_h^T*lambda=sum_j alpha_j*a_ij,
               sum_j alpha_j=1 }.                  (D)

Crucially, D depends on A and the query's affine leaves, not on theta. Each
point of D gives the upper bound

    lambda^T*theta_h + sum_j alpha_j*c_ij.           (V)

If D is empty, P_hi has no finite upper bound: it is feasible, and any finite
upper bound would give D's multipliers by A3. Thus that clause is unbounded
above for *every* admitted RHS revision. If D is nonempty, any one of its
points supplies a finite bound for every such revision. The primal's optimum
is attained, and A3 gives a dual point with that exact objective value.

### Why finitely many rational vertices suffice

D has the form `{w>=0:M*w=d}` with rational M,d. At an optimal point choose one
with the fewest positive coordinates. If its supported columns of M were
linearly dependent, a nonzero supported kernel direction permits a small move
in either sign while preserving nonnegativity. A nonzero objective change in
that direction would contradict optimality; otherwise move until a positive
coordinate becomes zero, contradicting minimal support. The supported columns
are consequently independent.

Such a point is a vertex: any feasible line through it has zero entries outside
its support and zero kernel direction on that independent support. Conversely
a dependent supported column set admits a two-sided feasible line and is not
a vertex. There are only finitely many column subsets. On an independent subset
the consistent solution is unique and rational, so all vertices are rational.
An optimal vertex exists by the preceding argument. Denote the finite,
nonempty vertex set by E_hi. This argument does not require a vertex of the
original source polyhedron or boundedness of its nuisance directions.

We have proved

    B(eta) = max_h max_i min_(v in E_hi)
               [lambda_v^T*theta_h + alpha_v^T*c_i] (B)

when every D_hi is nonempty. If any D_hi is empty, B is +infinity on every
admitted revision. No limiting infinite family of dual certificates is needed.

## 5. Emit the entire expression B as one native proof budget

For a vertex `(lambda,alpha)` and clause `g_i=min_j l_ij`, the native lattice
projections give `g_i<=[0]l_ij`. Multiply these inequalities by alpha_j and add.
Because the alpha weights sum to one, exact affine collection of the repeated
g_i atom rewrites their result as

    g_i <=[0] sum_j alpha_j*l_ij.

Separately, introduce the original retained rows, convert each along its fixed
path, multiply by lambda, and add. The coefficient equation in D identifies
this direction with `sum_j alpha_j*a_ij*x`. Adding the literal offset
`sum_j alpha_j*c_ij` proves

    sum_j alpha_j*l_ij <=[V] 0_u.

Transitivity produces a proof of the *same literal pair* `g_i,0_u` at budget V.
Zero weights need no row or leaf read. A singleton clause uses its identity
proof; an all-zero lambda vector needs only the constant offset.

Emit these proofs for **every** vertex in E_hi and join them with `meet_proofs`.
The result has exactly the inner minimum budget in B. Use `max_common` across
the clauses, then compose N's zero-budget equality and rewrite the difference
back to the original literal pair t,s. Do this in every h and apply `all_cases`.
Its budget is precisely B, with negative values preserved.

The entire trace is finite. Its conversion paths, affine leaf expressions,
dual weights, rule tags and zero-budget algebraic identities are independent
of eta. Only row budgets change. Consequently the F06 `replay` operation,
which recalculates **all** retained native min/max budgets, gives B at every
admitted RHS revision.

**Theorem U11 (uniform optimal replay).** For this fixed finite revision family,
either the native optimum is infinite at every admitted revision, or there is
one finite native trace, based at any one admitted revision, whose RHS replay
attains the native optimum at every admitted rational revision. Construction
requires retaining the complete finite dual-vertex alternatives in B (or a
separately justified equally complete set).

This also provides an alternative constructive proof of U1: the source-free
normal-form identities plus rational lifted affine consequence produce each
finite valid bound. It does not depend on generic query-specific sign-cell
enumeration. The original sign-cell reconstruction remains useful independent
evidence about the F06 branch producers and exact exclusion treatment.

## 6. A crucial implementation distinction: retain the alternatives

U11 is not a claim about every sound transport adapter. The existing
`f06_source_transport.transport` deliberately chooses one currently best
available parent of a `meet_proofs` node. The transported trace is sound and
may be optimal at that current context, but it can discard alternatives needed
after a later revision. The F08 `receive_converted` adapter uses that transport
and therefore has its stated **current-request** guarantee only.

For U11's construction, emit each original row/path proof directly into the
final context and retain every dual alternative. Do not pass the completed
portfolio through a pruning operation that selects only one meet parent.
Ordinary reachability pruning retains both referenced meet parents; F06's
RHS `replay` also retains both. Request reception still needs the new context
fingerprint. Uniform optimality does not make a stale proof object acceptable.

## 7. Consequences for sensitivity and scope

Formula B extends to a monotone continuous rational CPWA function of all
formal row budgets. Its numerical values outside the admitted feasible-context
domain are not asserted as source optima. In the admitted domain, it is the
exact native optimum, not merely one retained proof's upper envelope.

For original row coordinate r let L_r be the maximum of its nonnegative
coefficient over B's finitely many affine pieces, including the fixed positive
conversion factor. Use zero for inaccessible rows and for rows absent from
all these certificates. Finite min and max preserve a common coordinate
Lipschitz envelope, so

    |B(eta')-B(eta)| <= sum_r L_r*|eta'_r-eta_r|,
    B(eta') <= B(eta)+sum_r L_r*max(eta'_r-eta_r,0).

The second inequality also uses monotonicity. The coefficients need not be
minimal: a dual vertex that is never optimal in the allowed revision region
can enlarge this envelope. Source coefficients, units, conversion factors,
the query or hidden case schema changing are outside this theorem. In
particular, it does not justify moving a reflective report while pretending
that its controlled policy and source equations stayed fixed.

The finite construction may be very large. Normal-form expansion and vertex
enumeration are candidates for F11's producer design, not a promise that the
default F06 expansion limits suffice or that the procedure is computationally
competitive. No claim of global novelty is attached before F10's comparison.

## 8. Worked family for the executable audit

In one unit let the source rows be

    x<=a, y<=b, x+y<=e,

with unbounded nuisance z, and compare `z+f(x,y)` against z, where

    f=max(min(x,y), min(x-y,y-x)-1).

For the first clause, three dual vertices give a, b and e/2: the first two
project onto a single coordinate; the third averages the two min projections
and uses half the sum row. For the second clause, equal weights on `x-y-1`
and `y-x-1` cancel every source coefficient and give -1. Hence

    B(a,b,e)=max(min(a,b,e/2),-1).

Put `r=min(a,b,e/2)` and choose x=y=r, with any z. All source rows hold and
f equals B. This is an independent sharpness witness for the supplied finite
portfolio at every rational a,b,e, including negative optimal budgets.

Keeping only the currently best first-clause proof can lose future optimality.
At `(a,b,e)=(0,10,20)` the x-row proof is best. If it alone survives, replaying
at `(10,0,20)` yields 10 although the exact bound is 0. Retaining all three
alternatives and replaying their native minimum yields 0. Successful reception
at the first context would not have certified future portfolio completeness.
