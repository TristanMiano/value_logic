# F08 bounded optional extension: faithful substitution and quantitative transfer

Research contributor: **Codex (GPT-6)**, September 30, 2026 UTC.
Status: accepted optional F08 proof, included in the final reconstruction audit.
This is the bounded final exploratory question selected at the S1 research
review. It does not implement an integrated image/LP/vertex searcher.

## 1. A computable image, rather than a definition by all queries

Let C and D be admitted old and new contexts. Their source lists can differ,
but their unit names, named positive conversions and interpretation/observation
contract are fixed as required for F07's substitution interface. A substitution
sigma replaces each old source by a closed, well-typed new term of the same
unit. New terms are finite rational CPWA syntax, with capture-avoiding lexical
substitution. This is a declared modeling map, not automatic operational
validation of changed programs or observations.

Fix target u. Let I be all old source coordinates whose units reach u and J
all new source coordinates whose units reach u. The dependency lemma says sigma(x), for
x in I, depends only on J. Define the rational CPWA coordinate map

    F_sigma : R^J -> R^I,
    (F_sigma(y))_x = value of sigma(x) at y.

Let P_u(C),P_u(D) be their projected reduct unions. Define

    Z_sigma(D) = F_sigma(P_u(D)).                    (I)

This image is an explicitly computable nonempty finite union of closed rational
polyhedra. To see this, simultaneously expand the finitely many coordinate
terms into affine cells, intersect those cells with each D-reduct case, and
write the affine graph of F on each resulting nonempty polyhedron. Project
the graph onto the old coordinates by rational elimination. There are finitely
many pieces and every individual projected polyhedron is closed. No compactness
assumption or claim that every continuous image of a closed set is closed is
being used. An empty piece is discarded with its infeasibility certificate.

For every old unit-u expression t, the ordinary closed-substitution lemma gives
`value(sigma(t),y)=value(t,F_sigma(y))`. The old sources outside I are irrelevant
to t; arbitrary values may be filled in there when writing a full old assignment.

## 2. Exact preservation and reflection (U16)

**Theorem U16.** With these fixed interfaces:

1. Every old native global unit-u consequence remains native after sigma in D
   iff `Z_sigma(D) subset P_u(C)`.
2. Every native consequence of a sigma-translated old query in D reflects back
   to an old native consequence in C iff `P_u(C) subset Z_sigma(D)`.
3. Both directions hold iff the two sets are equal.

Each statement ranges over matching rational budgets and literal old query
pairs, with their explicitly translated new pair. It concerns consequence
theories, not reuse of an old fingerprint or literal term pair.

For the forward implications from set inclusion, use the substitution lemma
and U1 on the old and new reducts. For necessity, if either inclusion fails,
use the finite CPWA separator of 04a C1 for the set on the right. All its
coordinates are old coordinates in I and can be expressed in unit u through
their chosen positive paths. The separator is a legitimate old query; its
translation evaluates it on the image I. It proves a bound on one set and
fails on the other. A rational separating point exists by 04a; where a point
in the image needs a preimage, choose its affine graph piece and use rational
back-substitution. Thus this is also an effective rational obstruction, not
only a noneffective equality of collections of answers.

The first inclusion has a single characteristic-query certificate:

    K_D(sigma(V_C,u),0_u;0).

This is equivalent to inclusion because V_C,u has exactly P_u(C) as its zero
set. The reverse inclusion can be checked using a characteristic term for the
explicit image Z. Its finite polyhedral construction is necessary; it is not
assumed available from a lossless serialization alone.

### Existing case-map transport has a narrower operational contract

U16 is not a claim that every faithful map is accepted by the current
`transport` adapter. Suppose C has the two cases x<=0 and x>=0, while D has
one unrestricted case and sigma is identity. Both global reduct unions are
the real line, so the consequence theories agree. But D's one case is not
contained in either individual old case; a supplied case map to just one
would lack that case's row proof. Native existence follows from U1, while
this specific adapter would need a refinement/reconstruction. Case identity
and global union information must not be conflated.

## 3. Affine coordinate changes give a sharper replay specialization

Suppose the relevant coordinate map is `x=M*z+d`, with rational M,d, and the
new cases contain exactly the substituted old rows (no extra restrictions).
Assume each full new case is admitted. If M is onto the old relevant coordinate
space, the new reduct is the preimage of the old reduct and its image is
exactly the old reduct. U16 gives faithfulness.

For a U11 dual point, substituted row and leaf data become

    A' = A*M,      theta' = theta-A*d,
    a'_j = a_j*M,  c'_j = c_j+a_j*d.

The new dual balance equation is the old equation multiplied by M^T. Since
M is onto, M^T is injective, so the old and new dual feasible sets in
(lambda,alpha) are identical. Their vertices and positive row supports agree.
The certificate budget is unchanged:

    lambda^T*(theta-A*d)+sum_j alpha_j*(c_j+a_j*d)
      = lambda^T*theta+sum_j alpha_j*c_j.

The cancellation uses the dual balance equation, not an unexplained dropping
of the offset. Thus a complete catalogue can be transferred while retaining
all its alternatives, preserving optimality for the corresponding RHS and
withdrawal families. The usual adapter that selects a single meet parent
still does not preserve that entire catalogue automatically.

Surjectivity is the right unrestricted affine condition here, not injectivity.
If M is not onto, choose a nonzero rational a with `a*M=0`. The old row-free
query a*x is unbounded above, while its substituted query is the constant a*d.
This gives a failure of reflection. For example, the injective map
`z -> (z,z)` makes x-y identically zero, adding a correlation absent from the
old unconstrained pair. Conversely `(z,w)->z` is onto and preserves every old
x-query despite the new nuisance coordinate w. For a particular constrained
domain, full row rank can be weakened to the exact image condition in U16.

These statements are about typed affine source representations; they are not
dimension-counting claims about arbitrary real encodings.

There is a related finite-CPWA lower bound. If an old projected reduct contains
an open subset of R^d, a representation with fewer than d real source coordinates
cannot be faithful through a finite CPWA map. Each of its finitely many affine
image pieces lies in an affine subspace of dimension at most the new coordinate
count. A finite union of proper affine subspaces cannot contain an open subset
of R^d: successively choose a small ball avoiding each of the finitely many
closed hyperplanes containing them. U16 then excludes faithfulness. This is
not a bound for arbitrary discontinuous real encodings or a task restricted
to only some queries. A constrained old domain can have a smaller required
dimension: if the old source already enforces x=y, the map z->(z,z) covers that
line and is faithful to its full query theory. The exact image condition, not
ambient coordinate count alone, is decisive.

## 4. A finite quantitative deduction coefficient exists (U17)

Let V=V_C,u be the converted-row violation term from U12. It is nonnegative
and zero precisely on the native reduct domain. For a rational b,

    K_C(t,s;b)
      iff there is rational K>=0 and a source-row-free native proof
             t <=[b] s+K*V.                        (Q)

Here source-row-free means the proof uses no source assumptions, although its
expressions can contain declared source coordinates. It therefore holds at
every finite assignment, in any admitted context with the fixed signature.
This is a quantitative deduction result, not a probability or confidence bound.

### Construct the forward direction

Use the certified max-min normal form `f=t-s=max_i min_j l_ij` and the converted
row system in each old case h. Since b is a valid native bound, every minimum
clause has a rational dual certificate of cost `B_hi<=b`. For example choose
one of its optimal vertices from U11. Let its row weights be lambda_hi.

For a converted row `a_r*x<=theta_r`, put
`delta_r=ReLU(a_r*x-theta_r)`. There is an unconditional native proof

    a_r*x <=[0] theta_r+delta_r

by max injection and an exact constant rewrite. Also `delta_r<=[0]V_h`, where
V_h is the maximum of the converted violations for case h. The row-free native
dual construction therefore proves

    g_i <=[0] B_hi + (sum_r lambda_hir)*V_h.

Take K_h as the maximum of these finite row-weight sums. Since V_h>=0, raising
each coefficient to K_h and its constant to b is justified by native arithmetic
and lattice inequalities. Max-common across i gives `f<=b+K_h*V_h` everywhere.
An empty row list has V_h=0 and K_h=0; the same constant/convex-leaf proof works.

Take K=max_h K_h. All these case-associated proofs are now unconditional,
with the same query f. Increase their gains to K, use min-common, and apply
the source-free min translation/homogeneity identities to obtain

    f <= b+min_h(K*V_h) = b+K*min_h V_h = b+K*V.

No hidden case is supplied to a deployed action: f is fixed throughout, and
the minimum combines globally valid allowance bounds. Convert the constant b
back to the external budget and compose the zero-budget normal-form equalities.
Every instruction is native, and no original source row remains.

Moving a signed literal between the expression and the external budget is
not a rewrite that changes its parent's budget. Explicitly, a zero-budget
proof `t<=s+b+K*V` rewrites to `t-b<=s+K*V`. Add the native constant comparison
`b<=[b]0` and rewrite the sum to `t<=[b]s+K*V`. Negative b works by the same
constant rule. This accounts for the external budget in Q without weakening
it to zero or introducing a new inference rule.

For the converse, U12 proves V<=0 in C. Scale by K>=0, add the identity on s,
and compose with Q. This yields the original requested bound. In particular,
a full-source semantic bound that is not native cannot have a finite Q
coefficient for the *reduct* characteristic term: its reduct countermodel has
V=0 and violates the bound regardless of K.

## 5. The least coefficient is rational and has a native certificate

The construction above gives a finite sufficient coefficient, not necessarily
the least one. An exact minimum can also be characterized without assuming
that a ratio attains its supremum.

Partition the finitely many terms f=t-s-b and V into common affine cells.
On each nonempty cell `A_j*x<=eta_j`, write

    f=a_j*x+c_j,       V=d_j*x+e_j.

The inequality f<=K*V on that cell is equivalent by affine consequence to

    lambda_j>=0,
    A_j^T*lambda_j=a_j-K*d_j,
    lambda_j^T*eta_j<=K*e_j-c_j.

Together with K>=0 these are a finite rational **linear** system in K and the
lambda_j. Its projection onto K is nonempty by section 4, closed and rational
by elimination, and bounded below by zero. It therefore has a rational least
element K_*. Native U1 on the row-free source emits Q at K_*. This proves that
the least semantic coefficient and the least coefficient admitting a native
row-free certificate coincide in this fragment. It does not implement the
coefficient optimizer or assert that a producer's default cap will accept it.

The ratio need not attain its extremum. With old source x<=0, V=ReLU(x),
f=ReLU(x-1) and b=0, the least K is 1. For x>1 the ratio is `1-1/x`, approaching
1 without reaching it. K=1 is nevertheless a feasible, attained coefficient:
`ReLU(x-1)<=ReLU(x)` everywhere. Every K<1 fails at a sufficiently large rational
x. This does not contradict U4, which concerns the optimum of a fixed CPWA
query, not this ratio on a varying-parameter domain.

## 6. Approximate source substitution now has a checked transfer rule

Suppose Q has been emitted for an old request, and D supplies a current native
certificate

    sigma(V_C,u) <=[epsilon] 0_u.

Closed typed substitution of the row-free Q proof and native composition give

    sigma(t) <=[b+K*epsilon] sigma(s).                (T)

The epsilon certificate must be checked against precisely this current context,
domain, characteristic expression, zero and unit; an unrelated successful proof
or an unchecked metadata field does not suffice. On an admitted nonempty
domain its nonnegative expression cannot have a negative valid upper budget.
For epsilon=0 this gives a concrete exact transfer from one characteristic
inclusion proof, without requiring every new case to map to just one old case.
Source-free substitution can use the old single unrestricted case for every
new case; it has no old row assumptions to graft.

There is no query-independent fixed error tolerance for the entire unbounded
language. Old source x<=0 and new source x<=epsilon permit the query M*x to
lose M*epsilon for any positive rational M. Q's coefficient must retain the
query's sensitivity. V is a declared row-violation measure with a characteristic
zero set, not a canonical metric or an empirical probability of invalidity.
The F07 operational/interpretation bridge is still needed when these numerical
terms are claimed to describe an actual changed model or controller.

Even the least global coefficient need not give the tightest bound in one new
context. In the `ReLU(x-1)` example K_*=1. A new source x<=1/2 proves
V<=1/2, so T transfers the valid budget 1/2, whereas fresh reasoning gives the
exact bound 0. Optimality of a universal linear penalty coefficient and
optimality of a particular transferred request are separate claims. U16's
image equality preserves exact optima; mere inclusion or a positive violation
allowance generally preserves only the stated warrant.
