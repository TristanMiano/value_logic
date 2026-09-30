# F09 optional reconstruction F — the information in a license fragment

Research contributor: **Codex (GPT-6)**. September 30, 2026 UTC.
This refines the exact phase-one relationship, without proposing that its full
calculus is only a status table or replacing its evidence consumers.

## 1. Fixed status encoding is not an internal assessment algorithm

B3 encodes already supplied diagnostics as constants. It does not implement
the diagnostic evaluator as one continuous native term of its numerical inputs.

**B11 (continuous-assessment obstruction).** No finite F05 term of a freely
varying tolerance can return an injective discrete encoding of the exact
phase-one assessment for every tolerance in a connected interval crossing a
decision boundary. It already fails for the point certificate [0,0], tolerance
tau in [−1,1], and the upper-bound consumer: tau<0 is refuted, while tau>=0 is
supported. A term is continuous. Along negative tolerances increasing to zero
its output would have the refuted code as limit, but at zero it must have the
different supported code. This contradicts continuity.

The obstruction persists with rational test inputs, by taking a rational
sequence approaching zero. It does not depend on how the third status is
encoded. It does not prohibit an external decoder, the existing discrete
phase-one evaluator, or a richer typed language with a separate predicate sort.
Nor does it prohibit finite tabulation for finitely many fixed requests.

A precise positive bridge uses continuous **margins** plus a separate consumer.
For an accepted interval certificate [l,u] and tolerance tau, retain u−tau and
l−tau. The consumer supports when the first is <=0, refutes when the second
is >0, and otherwise leaves the atom open. Native arithmetic represents the
margins exactly; the discrete observation belongs to the explicit consumer.
Missing certificates, invalid modes and malformed requests remain external
cases, not invented margins. The bridge is conditional on the same certificate
validity/provenance and interpretation assumptions on both sides; a feasible
modeled interval is not an empirical calibration theorem.

For arbitrary CPWA queries, the existence of a native certificate must also be
distinguished from a bounded producer finding it. B4's supplied endpoint rows
make its two directions directly constructible. Failure of a future bounded
search must not be reclassified as a semantic countercertificate or as proof
that a source interval actually crosses the threshold.

## 2. The exact quotient of the marginal interval consumer

Let D be a nonempty admitted finite polyhedral source union and f_1,...,f_n
fixed rational CPWA quantities in one accessible unit. For every rational
threshold tau observe each condition f_i<=tau as supported, refuted or open
using the universal/inclusive and universal/strict clauses from B4/B5.
Write l_i=inf_D f_i, u_i=sup_D f_i; finite endpoints are rational and attained.
Infinite endpoints here are metadata about unbounded ranges, not F05 literals.

**B12 (marginal observation quotient).** Two such source descriptions give the
same status for every individual rational threshold, and hence every finite
atomwise profile made from these thresholds, exactly when all their endpoint
pairs (l_i,u_i) agree.

The forward reconstruction is explicit: u_i is the infimum of rational
thresholds with supported status (or +infinity if none), and l_i is the
supremum of thresholds with refuted status (or −infinity if none). The strict
refutation boundary does not change the supremum. Rational density separates
any unequal endpoints. Conversely the clauses are simply u_i<=tau and l_i>tau,
so equal endpoints give equal status; profile meet adds no missing joint data.
The rectangular fallback comparison also depends only on the same endpoints.

Thus this specified consumer retains the coordinate interval hull of the joint
image (f_1,...,f_n)(D). It does not retain every correlation. Example: the line
x+y=1 in [0,1]^2 and the full square have the same coordinate endpoints and
all these marginal/profile observations, but native quantitative inference
proves x+y<=1 on the line and has optimum 2 on the square. Scaling the example
by M makes the lost sum allowance M, so the loss has no scope-independent
finite bound over arbitrary scales.

This is an exact quotient for the **marginal endpoint fragment**. Phase one's
more general region atoms, value spaces, compound certificate producers and
provenance interface are not restricted by this theorem. It would be incorrect
to describe the entire earlier calculus as unable to carry joint information.

There is a related distinction for B6: a connected domain has only two
intrinsic Boolean function classes, but the identities that make a particular
term constant can still encode rich source information. For example
max(x−1,0) is the constant zero on [0,1], but is not Boolean on [0,2]. Both
domains have a two-element Boolean algebra internally. The algebra's cardinality
alone is not the entire embedded native consequence theory.

## 3. The least extra profile information for joint rejection

Fix one nonempty domain D, finitely many margins f_i and their **fixed**
threshold-zero requirements. Put A_i={x in D:f_i(x)<=0}. The following is an
optional *new joint consumer*, not a silent change to phase one's atomwise meet.

Let S={i:A_i=D}, and let F be the family of inclusion-minimal nonempty sets I
with intersection_(i in I) A_i empty. The family F is an antichain of conflicting
requirement sets. No member of F contains an index in S: removing such an
index could not restore feasibility. The original individually refuted atoms
are exactly the singleton members of F.

**B13 (exact fixed-profile interface).** For any nonempty required set R,
the joint observation of max_(i in R) f_i is

    supported iff R subset S;
    refuted iff some I in F is a subset of R;
    open otherwise.

Support commutes with universal conjunction. Joint refutation means the accepted
sets have empty intersection; finiteness of R supplies a minimal nonempty
infeasible subset. The remaining case has both an accepted source point and
a point violating some requirement, hence is open. This proves the three clauses.

Conversely, the answers for all profiles recover S from supported singletons
and F from minimal refuted profiles. Consequently (S,F) is a necessary and
sufficient **canonical observation summary** for this fixed query family.
This is not a claim about minimum bit storage under arbitrary encodings.
Phase one's atomwise summary keeps S and the singleton conflicts but can omit
all larger conflicts, exactly the gap exposed by B5.

Every finite pair (S,F) satisfying the stated disjointness/antichain conditions
has a rational point-case realization. For each subset J of the non-S indices
containing no member of F, make one Boolean source point at which the accepted
requirements are S union J. There is always at least the J=empty point. Use
loss 0 for accepted requirements and 1 for rejected ones, with the requirement
loss<=0. Every non-S index can fail at the empty point. A requested set is
jointly feasible exactly when it contains no forbidden member, and the indices
supported everywhere are exactly S. This realizes the interface in the finite
F05 fragment, without hiding an infeasible source case.

The antichain can be large. This theorem gives an exact explanation of missing
information; it does not promise that explicitly storing all conflicts is an
efficient replacement for source constraints.

### 3.1 A bounded-arity control for affine requirements on a convex source

If D is one feasible polyhedron in R^d and every f_i is affine, every minimal
conflict contains at most d+1 requirements. Here is a reconstruction using the
rational infeasibility certificate from F08, not an unexamined appeal to a
named convexity theorem.

An infeasible family consists of the fixed source rows plus the requirement
rows. There are nonnegative rational multipliers whose weighted normal vectors
sum to zero and whose weighted right-hand sides sum to −1 after normalization.
View each row as its (normal,right-hand-side) column in R^(d+1). If more than
d+1 columns have positive coefficients, they are linearly dependent. Choose
a rational dependence, reverse its sign if necessary to have a positive entry,
and subtract the largest nonnegative multiple that keeps all coefficients
nonnegative. At least one positive coefficient vanishes while the represented
column (0,−1) is unchanged. Iteration leaves at most d+1 rows in total, including
source rows. Their requirement subset is already infeasible with D. Minimality
of the conflict therefore bounds its size by d+1.

The sum of its requirement multipliers is positive, since the source polyhedron
is feasible. Normalize those multipliers to a convex combination. The same
certificate then gives a positive rational lower bound on that convex combination
of requirement margins, and hence on their maximum. Native weighted source
inference and maximum injections supply a joint-refutation certificate.

The dimension can be the affine dimension r of D, rather than its ambient d.
Parameterize its rational affine hull by x=x_0+B*z with rational x_0,B and
r free coordinates, then apply the same argument there. A rational hull basis
can be reconstructed by successively selecting rational feasible points outside
the current rational affine span. If the span is too small, one of its rational
defining equations is violated by some feasible point; choose a smaller rational
positive violation margin and use F08's rational feasibility reconstruction to
get a rational point outside the span. This terminates at the affine dimension.

For a union of k feasible polyhedra of affine dimensions r_h, choose such a
requirement subset separately for each case and take their union. Every
minimal conflict then has size at most sum_h(r_h+1), and hence at most k(d+1).
No sharp bound for every fixed dimension profile is claimed. For a finite
k-point source this gives k, attained by the family below. Arbitrary CPWA
requirements require a common affine refinement first, which can greatly
increase the number of cells.

The single-convex-case d+1 bound is also sharp. On R^d use requirements
−x_i<=0 for i=1,...,d and sum_i x_i+1<=0. All together are impossible, while
omitting the last permits x=0 and omitting any coordinate requirement permits
that coordinate to be −2 with the others zero. Their joint maximum is at least
1/(d+1), because the average of the d+1 margins is that constant, and equality
is attained when every x_i=−1/(d+1). The d=2 instance has a saved native
certificate, constructed from weighted maximum injections.

The convexity restriction cannot be dropped while keeping the d+1 bound.
For any k>=2 let D consist of the k rational points (j,j^2), j=1,...,k, in R^2.
For each i impose

    f_i(x,y)=1/2−y+2*i*x−i^2 <=0.

At point j this is 1/2−(j−i)^2: positive only when j=i. Every proper family
of requirements admits the point corresponding to an omitted index, while
all k together are infeasible. Thus the sole minimal conflict is the full
k-element family, with fixed ambient dimension 2. Every individual atom is
open, but the joint maximum is exactly 1/2 on the source. This is a precise
family where recording only singleton failures loses arbitrarily high-order
joint rejection information.

### 3.2 A separate bound for natively Boolean requirements

If each requirement is already a natively Boolean loss and P_u(C) has c
connected components, every accepted set is a union of components by B6.
In a minimal conflict I, omitting each i must admit some component C_i that
all other requirements accept. Requirement i must reject C_i, or the whole
family would be feasible. These components are distinct: if C_i=C_j for i!=j,
one condition says i rejects it and the other says i accepts it. Hence |I|<=c.

In particular a connected accessible domain supports no higher-order conflict
among native Boolean requirements. This does not rule out open phase-one
assessments on a connected interval: their threshold predicates are external
observations of continuous margins, not generally native {0,1}-valued terms.

### 3.3 Exponentially many conflicts, including on a convex source

For integers 2<=m<=n, consider the single rational polyhedron

    D={x in [0,1]^n : sum_i x_i=m-1}

and affine requirement margins f_i=1-x_i. It is feasible, compact and convex;
its affine dimension is n-1. Each individual requirement is open: its margin
attains both 0 and 1. A set R of requirements is jointly accepted exactly when
|R|<=m-1. Necessity follows because acceptance forces x_i=1 for every i in R;
sufficiency follows by filling the remaining coordinates to total m-1.
Consequently the minimal conflict antichain consists of **all m-subsets**, of
size binomial(n,m). Convexity bounds each conflict's arity, but not the number
of different conflicts by a polynomial in n.

For a nonempty R of size r, its joint margin V_R=max_{i in R}(1-x_i) has exact
minimum

    min_D V_R = max(0,1-(m-1)/r).

The lower bound follows from maximum >= average and sum_{i in R} x_i<=m-1.
For r>=m-1, equality is attained by x_i=(m-1)/r on R and zero elsewhere.
For r<m-1, put every coordinate of R at 1 and fill the other coordinates.
The maximum of V_R is 1: at least one chosen coordinate can be zero while the
other n-1 coordinates accommodate m-1. Hence all nonempty profiles below the
conflict size are open, while r>=m has the sharp joint-refutation margin
`(r-m+1)/r`. The average argument gives a native certificate recipe using the
source sum and nonnegativity rows plus weighted maximum injections. This
general recipe is a paper extension, not an additional saved certificate.

There is no contradiction with the connected-component bound for Boolean
requirements: these f_i vary continuously through [0,1] and are not native
bits on D. If one instead insists on Boolean losses with the same profile
answers, at least binomial(n,m-1) accessible components are needed. Each
(m-1)-subset must be accepted somewhere, and its accepting component can
accept no additional index, since every m-subset is a conflict. Distinct
(m-1)-subsets therefore need distinct components. Boolean point cases for all
such subsets attain this bound.

An explicit antichain list is not necessarily a minimal representation. The
example just given has the short rule "refute exactly when |R|>=m". A separate
worst-case information argument follows from B13's general realization: fix
n>=4 and m=floor(n/2), and choose **any** subfamily F of the m-subsets. Every
choice is an antichain, realizable with S empty and every singleton open.
Different choices have different answers on an m-element profile R: it is
refuted precisely when R is in F. There are therefore

    2^(binomial(n,m))

different joint-profile interfaces with the same individual statuses. A
self-contained finite binary summary, interpreted by one fixed decoder that
must answer every profile exactly and has no access to other source data,
must use at least binomial(n,m) bits in the worst case. This is simple counting:
there are only 2^N-1 binary strings of length less than N. It is not a bound on
the cost of one query, a claim that all source families need that much storage,
or an objection to retaining a compact constraint system and computing answers
on demand. It identifies how much information singleton statuses can omit.
