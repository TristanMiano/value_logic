# F08 optional extension: characteristic probes and complete withdrawal support

Research contributor: **Codex (GPT-6)**, September 30, 2026 UTC.
Status: accepted reconstruction within the protected F08 block. This note uses
the explicitly scoped U1 and U11 arguments; it is not a later gate or an
automatic reasoner. Current timing and acceptance remain in the work record.

## 1. A finite characteristic query for the native source domain

Fix a target unit u and the signature/observation conditions of U1. In each
source case h retain exactly its rows whose units reach u. For such a row
`l_hi<=r_hi:v`, choose a positive path Phi_v:v->u and define

    e_hi = ReLU(Phi_v(l_hi-r_hi)),
    V_h = max_i e_hi,               with V_h=0_u for no retained rows,
    V_C,u = min_h V_h.                                      (C)

The case list is nonempty. All extrema are finite binary syntax. Positive
conversion factors preserve the signs of row violations. Therefore V_C,u is
nonnegative everywhere, and its zero set is precisely the union of the reduct
cases, ignoring only numerical coordinates on which it cannot depend.

This expression has a native global proof `V_C,u<=[0]0_u` in the original C.
In case h, introduce each retained row, apply its named conversion path, and
restore the normalized intercept by adding its constant. This proves
`Phi_v(l_hi-r_hi)<=[0]0_u`. Max-common with `0<=[0]0` proves e_hi<=0; repeated
max-common proves V_h<=0. A min projection proves V_C,u<=V_h. Aggregate these
local proofs, all with the literal same V_C,u and zero, using all_cases.
An empty row list uses the constant zero identity. No inaccessible row is used.

**Corollary U12 (finite characteristic probes).** For two admitted contexts
C,D with the same signature and interpretation, write P_u(C),P_u(D) for the
projected reduct unions of U9. Then

    P_u(C) subset P_u(D)
       iff K_C(V_D,u,0_u;0),

and equality of their entire global unit-u native consequence theories is
equivalent to these two characteristic queries being provable in opposite
directions. This follows from C's exact zero set and U1, not from a definition
that identifies contexts merely when every queried answer happens to agree.

The construction produces a mathematical characteristic term and a proof.
It does not erase the original source/provenance record or define a new value
carrier. Equivalent zero sets can have different rows, witnesses, update
histories and proof sizes. Operational applicability and the ability to observe
a coordinate are still separate from its occurrence in a modeled loss term.
Positive path choices change violation magnitudes; their zero sets agree.

## 2. Why affine probes alone do not provide this representation

The two-ray example in 04a has source `x<=-1 or x>=1`. Every nonconstant affine
upper-bound query is unbounded, just as on the whole line. Its characteristic
CPWA term `min(ReLU(x+1),ReLU(1-x))` nevertheless separates x=0.

There is also a useful unbounded two-dimensional example. Let

    Q = {(0,0)} union {(x,y):x>=1}.

This is a finite union of closed rational polyhedra. Its convex hull is
`{x>0, arbitrary y} union {(0,0)}`, which is not closed; its closed convex hull
is `{x>=0}`. To check the convex-hull formula, for x>0 choose
`lambda=min(1,x)` and write `(x,y)=lambda*(x/lambda,y/lambda)+(1-lambda)*(0,0)`.
The nonzero point lies in the halfspace case. No convex combination with
first coordinate zero can put positive weight on that case.

For an affine objective a*x+b*y+c, boundedness above on Q requires b=0 and
a<=0; then its optimum is c, attained at the origin. These are exactly the
same affine upper bounds as on `{x>=0}`. But

    V(x,y)=min(max(|x|,|y|), ReLU(1-x))

is zero exactly on Q and equals 1 at (0,1). It is admitted finite CPWA syntax.
Thus even closure of the convex hull loses source information that the full
query language can use. This does not invalidate the closed-image argument in
U4: a linear projection of each individual polyhedron is closed, and a finite
union of those projections is closed. Taking a convex hull is a different
operation and was not used in that proof.

## 3. A complete retained dual catalogue survives arbitrary row withdrawals

Use the fixed query, row directions and unit meanings from U11. Its clause
dual is

    D_hi={lambda>=0, alpha>=0:
          A_h^T*lambda=sum_j alpha_j*a_ij, sum_j alpha_j=1}.

Withdraw any subset W_h of the original rows in each case. Removing rows
cannot invalidate the old feasibility witness. In the converted numerical
system, the new dual is naturally identified with

    D_hi(W_h)=D_hi intersect {lambda_r=0 for every r in W_h}.  (F)

Inaccessible original rows had no coordinate in this dual and have no effect.
F is a face: a convex combination of nonnegative coordinate vectors has a zero
coordinate only if each positively weighted endpoint has that coordinate zero.

Every vertex of this face is a vertex of D_hi. If it were a nontrivial convex
combination of two points in D_hi, the zero-coordinate property would put both
points in the face, contradicting extremality there. Conversely a vertex of
D_hi lying in the face remains extreme in it. Consequently its vertex set is
exactly the old vertices whose positive row support avoids W_h.

If the face is nonempty, it has an optimal vertex for every feasible current
RHS by the same standard-form argument as U11. If it is empty, the lifted
minimum-clause primal is still feasible but has no finite upper bound.

**Corollary U13 (complete finite retention under withdrawal).** A U11 trace
retaining every dual vertex supplies an exact finite native optimum after any
subset of row withdrawals and any simultaneous admitted RHS changes whenever
each clause in each remaining case has at least one surviving vertex. The
exact budget is U11's max/min expression with the unavailable vertices removed.
If a clause has no surviving vertex, the native optimum is +infinity.

For nonempty surviving portfolios, F06 source transport can produce a current
optimal proof: each vertex proof uses only its positive-support rows; each
meet chooses the best available current argument; every outer max clause and
every live case is still required. It may collapse the returned portfolio.
Retain the original complete catalogue separately for future withdrawals or
revisions; do not assume the newly selected witness remains complete.

The qualification about complete catalogues is essential. A missing supplied
certificate in an arbitrary retained proof does **not** establish an empty
dual face, and a generic `UnavailableProof` result is not an unboundedness
certificate. The present fixture's catalogue is proved complete explicitly;
there is no generic catalogue-completeness receiver implemented in F08.

Deleting a hidden case instead of a row removes its outer maximum, provided a
nonempty case family remains. A complete local catalogue for every retained
case again gives the exact new global optimum. Declaring that an empirical
case no longer belongs to the source still requires the ordinary applicability
and current-context checks; the algebra does not decide that evidence question.

## 4. Withdrawal as a finite relaxation path

Increase each withdrawn original row budget by a common R>=0 while fixing the
others. An old dual vertex's budget is

    a_v+c_v*R,  where c_v=sum_(r in W_h) k_r*lambda_vr>=0.

The vertices surviving actual withdrawal are exactly those with c_v=0. If
each clause has a survivor, let M_hi be its best survivor budget at the kept
row values. Every nonsurviving vertex eventually has `a_v+c_v*R>=M_hi`.
A sufficient threshold is the maximum of zero and the finitely many ratios
`(M_hi-a_v)/c_v` with c_v>0, taken over all cases and clauses. Beyond it,
the relaxed-source optimum equals the actual-withdrawal optimum **exactly**.

If some clause has no survivor, its finitely many c_v are all positive; its
minimum budget grows without bound as R grows. This agrees with its unbounded
post-withdrawal optimum. The discussion assumes an initially finite native
optimum; if one clause's dual was already empty, it remains unbounded after
weakening. Infinity is a metatheoretic status here, not a permitted budget
literal or an arithmetic value inserted into a checked proof.

This result concerns the complete finite max/min budget expression. It does
not assert that any particular historical proof's allowance becomes sharp
under relaxation. The threshold follows from the explicitly retained slopes.

## 5. Assumption failures and a smallest exact fixture

Adding a genuinely new row is different from withdrawing an old one. The new
dual can have vertices using that new row, absent from the old catalogue.
For old rows x<=1 and y<=1, the exact old proof of x+y<=2 adds the two rows.
Add the new joint row x+y<=0. The new optimum is 0, attained at (0,0).
Even optimal replacements for the old individual row leaves still have bounds
1: (1,-1) attains the x bound and (-1,1) attains the y bound in the new source.
The old addition skeleton therefore retains budget 2. The new joint row gives
the stronger certificate, which requires adding a new argument. Merely
recomputing optimal marginal row allowances cannot recover the correlation.
Changed matrix coefficients, conversion factors, source meanings or query
expressions likewise need new analysis. This is not a blanket completeness
claim for arbitrary revisions or a replacement for F06's receiving conditions.

In U11's executable family, the first clause is min(x,y), with source rows
`x<=a`, `y<=b`, `x+y<=e`. Its dual equations reduce to

    lambda_1+lambda_2+2*lambda_3=1, lambda>=0,
    alpha_1=lambda_1+lambda_3, alpha_2=lambda_2+lambda_3.

Its only vertices are `(1,0,0)`, `(0,1,0)` and `(0,0,1/2)`, giving budgets
a, b and e/2. The second clause `min(x-y-1,y-x-1)` has only the zero-row
certificate with leaf weights (1/2,1/2), giving -1. Thus all eight withdrawal
masks are characterized: with any of the three rows retained, the optimum is
`max(min(retained entries from a,b,e/2),-1)`; with none retained it is unbounded.
For the finite cases choose x=y equal to the retained minimum to attain it.
For the empty retained set, x=y=N exhibits arbitrarily large values.
