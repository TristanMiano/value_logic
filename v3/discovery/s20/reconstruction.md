# Reconstruction of V19-R/v1 from the input contract

Codex (GPT-6), October 28, 2026. DEVELOPMENT; same-model reconstruction.
This is not a claim of independent confirmation. The event remains the one
specified in [s19/claim.md](../s19/claim.md).

## 1. Translate observations without choosing a fitted model

Write K={1,...,k}. The j-th observation is equivalent to the conjunction
of g_ji(x_i)>=a_j for EVERY i and the disjunction of g_ji(x_i)<=b_j over i.
There is no requirement that its upper-bound witness attain the exact
minimum, and ties do not need to be broken consistently across observations.
Any witness suffices. Let

    Q_i(T) = {x_i in B_i : all g_ji(x_i)>=a_j,
                            and g_ji(x_i)<=b_j for j in T}.

For every disjoint labeled partition (T_1,...,T_n) of K, take the product
of these slices, omitting products with an empty factor. The union of the
remaining products is EXACTLY the admitted source set X. One direction
uses the assigned upper-bound witness; the other chooses one witness for
each observation. This reduction is ordinary disjunctive programming.

Every nonempty local slice is compact and convex. If its affine image under
f_i has extrema ell_i(T),u_i(T), then that image is exactly the closed
interval [ell_i(T),u_i(T)]. This follows by interpolating the extremizers,
not by assuming the nonconvex admitted source X has a convex image.

## 2. An anchor eliminates the need to enumerate product branches

Temporarily choose a generator i as the witness of the new minimum, and
assign it exactly the old-witness subset T. Its potential value q must lie
in its local interval. Every other generator need only attain a value at
least q. For a fixed outside partition (T_l) of K minus T this is equivalent
to q<=min_(l!=i) u_l(T_l). Local maxima can be chosen simultaneously because
the original source prior is a Cartesian product. Cross-generator coupling
would invalidate precisely this step.

Take the largest such outside threshold:

    C_i(S) = max_(outside partitions of S) min_(l!=i) u_l(T_l).

Use C_i(S)=-infinity when no feasible outside partition exists; if n=1,
C_i(empty)=+infinity and C_i(nonempty)=-infinity. There are finitely many
partitions. Every finite maximum is attained. All outside partition ranges
in q are downward rays with a common lower end at -infinity. Their union
is therefore just the ray ending at C_i(S), even if X is disconnected.
This nested-ray fact is the key compression step.

The attainable values with this anchor/subset are exactly

    J_iT = [ell_i(T), min(u_i(T), C_i(K minus T))],

when Q_i(T) is nonempty and the displayed lower endpoint does not exceed
the upper. In the forward direction, any admitted x with i attaining its
new minimum supplies the needed partition and inequalities. In the reverse
direction, choose a maximizing outside partition, choose each outside local
maximizer, and interpolate the anchor's extremizers to q. The old lower
inequalities and all assigned upper inequalities hold, and the new minimum
is q. A degenerate local interval uses its recorded extremizer directly.

Every admitted source has a new minimizing generator because n is finite
and positive. Taking the union of the J_iT therefore proves completeness,
not merely a sound outer bound. If this union is empty, X is empty: a
nonempty X would supply a finite minimum in some anchor interval.

## 3. Compute all outside thresholds by subset partitions

For a sequence of generators I define U_I(S) as the best minimum of local
upper extrema over all disjoint labeled partitions of S among I. Unavailable
slices and impossible partitions are absent. Empty I has the conventions
above. For a new generator i,

    U_(I,i)(S) = max_(T subset S) min(U_I(S minus T), u_i(T)).

The induction is exact because the subset assigned to i is unique for each
partition, and all other assigned subsets form a partition of its complement.
With the infinity conventions the induction also covers no old observations,
no outside generators, and slices receiving the empty subset.

Store all prefix and suffix tables and attaining splits. For each i combine
its preceding and following tables by the same subset split. This yields
C_i(S) for all S. For one layer the number of pairs (S,T subset S) is 3^k:
each observation is outside S, in T, or in S minus T. There are O(n) layers.
An entry requires only selection and comparison of local rational extrema;
no sums of LP optima grow with the number of layers.

At most 2*n*2^k local LP calls compute all extrema or detect empty slices.
The later construction uses O(n*3^k) comparisons. Sorting and merging at
most n*2^k candidate intervals uses O(n*2^k*log(n*2^k)) comparisons.
Prefix/suffix/anchor tables and split indices use O(n*2^k) entries; a split
index costs O(k) bits. This statement is about entries and comparisons,
not unit-cost access to unbounded integers or free copies of constraint rows.

## 4. Rational certificates and bit costs

For rows Ax<=b and affine objective c dot x+d, a bounded slice is certified
by feasible x_lo,x_hi and nonnegative multipliers lambda_lo,lambda_hi with

    A^T lambda_lo = -c,  d-b dot lambda_lo = ell,
    A^T lambda_hi =  c,  d+b dot lambda_hi = u,
    c dot x_lo+d=ell,    c dot x_hi+d=u.

Weak duality proves no feasible value lies outside [ell,u]; the two points
prove both bounds attained. An empty slice uses lambda>=0,
A^T lambda=0, b dot lambda<0. This contradicts feasibility after multiplying
the original rows. Rational LP duality/Farkas supplies these certificates
when the theorem's hypotheses hold. Their existence is imported machinery.

Check EVERY pair (i,T), reconstructing its rows from the caller's problem
rather than trusting rows supplied in the certificate. Missing entries are
errors, not emptiness proofs. Recompute the subset tables and normalized
interval union from the certified extrema. A hash binds the advertised
certificate to those input bytes but is not authentication of the model.
In fact the verified extrema/witness argument remains sound for inputs
outside the compact-polytope promise whenever all required exact certificates
exist; the verifier does not need to prove that promise separately.

Rational LP extrema and primal/dual witnesses have polynomial encoding length
in their rational LP input size. The combination step selects extrema rather
than adding them, so it does not amplify their bit length. Source recovery
uses the recorded outside split and local maximizers. In the anchor it uses

    x(q) = x_lo + ((q-ell)/(u-ell))*(x_hi-x_lo),

unless u=ell, in which case q=ell. Its bit length is polynomial in the LP
certificates and the rational query q. Walking the stored splits is O(n)
table accesses, plus mask operations, writing all local vectors and doing
the anchor's exact arithmetic. Retaining or verifying all local certificates
can dominate the small final interval list; those costs must be reported.

## 5. Output size and the exact scope of the resource improvement

For k=2r, take n=2 and B_i={x in [0,1]^k : sum x_j=r}; observe
min(x_1j,x_2j)=0 for every j. The supports are disjoint and each has at least
r members, so each has exactly r, all its members equal one, and the supports
are complementary. Let f_1=sum_j 2^j x_1j and f_2=2^k. Every r-subset then
gives a different new minimum. Thus binom(k,r) isolated values occur.

An explicit interval list needs that many components. This is an unconditional
output-length obstruction, with coefficients of O(k) bits and growing local
dimension. It does not lower-bound the time of a succinct representation,
one-band feasibility, approximate prediction, or every possible ordinary
solver. The upper bound replaces n^k old-witness assignment enumeration by
a fixed-parameter construction in k, while permitting n to be large. It is
not a lower bound against conventional mathematics: conventional LPs and
subset dynamic programming constitute the construction itself.
