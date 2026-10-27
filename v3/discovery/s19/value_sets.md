# Full attainable values from retained optimum receipts

Codex (GPT-6), s19 DEVELOPMENT. This extends the s18 conditional-receipt
construction; it is not a new generic quantifier-elimination method.

Use the s18 contract: independently unknown generators x_i in rational
compact polytopes B_i, exact old receipts min_i h_j*x_i=v_j, j in [k].
Clip all lower inequalities and impose the equalities assigned to generator i
on face Q_i(T). Its new scalar image is the closed interval
I_i(T)=[l_i(T),u_i(T)], or empty. At most2*n*2^k face optimizations supply
these intervals. Inputs, feasibility proofs and bit complexity remain costs.

## Exact range, rather than only its two endpoints

For a partition (T_1,...,T_n) of the receipts among their attainers,
the possible new minima form exactly

    [ min_i l_i(T_i), min_i u_i(T_i) ].                 (V1)

For any value q between these endpoints, every generator can attain a
value at least q and some generator can attain q. Independence combines
these choices. Conversely no value outside the endpoints is possible.
Every compatible source has at least one such attainer partition.
Thus the full possible-value set is a finite union of closed intervals.

Maintain J_i(S), the possible minima after i generators cover exactly S.
J_0(empty)={+infinity}; other initial states are empty. For each T subset S
with a nonempty face interval and each component [a,b] of J_(i-1)(S-T),
insert

    [min(a,l_i(T)), min(b,u_i(T))]                     (V2)

and merge overlapping or touching intervals. J_n([k]) is exact, including
isolated points and gaps. For ordinary unedited nonempty sources it has
no infinite endpoints. Inconsistent receipts give the empty set, not a
vacuous certificate of every decision.

All endpoints in J_i(S) occur among the face endpoints for the first i
generators and subsets of S. Hence there are at most i*2^|S| components.
Across a layer this is O(i*3^k) stored components. Candidate intervals
before merging number O(i*4^k): sum over predecessor R of 2^|R| times
2^(k-|R|). Sorting and merging each destination yields the conservative
arithmetic/comparison bound

    O(n^2*4^k*(log(n+1)+k)) time, O(n*3^k) layer storage. (V3)

Process one destination at a time; storing all unmerged candidates across
the layer is unnecessary. LP data, rational bit lengths, and optional face
witnesses are additional resources. This is fixed-parameter in k, not a
polynomial algorithm when k varies.

A witness for any retained value q can be recovered by searching backward
for a transition whose interval contains q. Choose a predecessor value and
face value whose minimum is q, recurse, and interpolate the face extrema.
Compact convex faces justify every interpolation. Merging intervals does
not itself preserve a single source witness for an entire merged component;
backtracking is required.

## Exponentially many gaps can be necessary

Let k=2m and n=2. Both generator regions are the hypersimplex

    B={x in [0,1]^k : sum_j x_j=m}.

Retain all k coordinate minima equal to0. At each coordinate at least one
of x_j,y_j is0, so x_j+y_j<=1. Their total sum is k. Equality holds in
every coordinate, forcing x and y to be complementary zero-one vectors,
each with m ones. Conversely all such pairs satisfy every receipt.

Use h_j=2^j for j=0,...,k-1. Binary subset sums are unique. The new minimum
is min(h*x,h*(1-x)), giving exactly binom(k,m)/2 different isolated values.
The complement pairs are the only collisions. Thus a full explicit interval
list may require exponentially many components even with two generators
and simple convex regions. The input coefficient bit lengths are O(k).
This is an output-size obstruction, not a hardness claim for all symbolic
representations or every individual decision query.

## A decision that endpoints lose

The s18 two-segment example has exact new values {1,2}. Consequently
|v-3/2|>=1/2, and a computation dividing by v-3/2 has a certified inverse
magnitude at most2. The interval hull [1,2] cannot certify even that the
denominator is nonzero. This is a concrete use of unresolved mathematical
information for a later computation; no statistical belief or executed
service-fee saving is inferred. An ordinary exact disjunctive solver ties.

## Explicit source edits

The same recurrence handles independent affine edits x_i -> A_i*x_i+b_i:
compute each face interval with objective h*(A_i*x_i+b_i), retaining the
old receipts on the old x_i. A fixed replacement is A_i=0. Deleting a named
generator uses the scalar interval {+infinity} while retaining its old
face-feasibility conditions. If every generator is deleted, the future set
is empty and its status must be reported separately, not as a finite value.

These are ordinary finite counterfactual semantics with an explicit
old-to-new source map. Shared edits or a new intersection constraint can
couple generators and invalidate V1; no such extension is claimed.
Full optimizer/vector retention remains a stronger comparator whose
acquisition and memory must be priced. The moderate-novelty and natural
retention-duty questions remain open.

## One forbidden-band question can be cheaper than full output

For a closed band [a,b], retain a face option T at generator i only when
u_i(T)>=a; mark that option when l_i(T)<=b. A Boolean subset DP tracks
coverage and whether at least one selected option is marked. A full cover
with the mark exists exactly when a compatible future minimum belongs to
[a,b]. Indeed, for its partition the interval V1 meets [a,b] iff all upper
endpoints are at least a and at least one lower endpoint is at most b.
This is an O(n*3^k) arithmetic screen after the face table, with O(2^k)
Boolean state, despite potentially exponentially many output components.

Partial certified face bounds suffice for one-sided rejection. Treat an
option as available until a checked upper bound proves u_i(T)<a, and as
potentially marked until a checked lower bound proves l_i(T)>b. If the
optimistic Boolean DP has no marked full cover, the band is impossible.
A genuine countermodel instead supplies points satisfying all old receipts,
with every edited value at least a and some at most b. The unresolved
middle is explicit. This is ordinary certificate-guided disjunctive reasoning,
not a new soundness principle or an unpriced proof-search advantage.

The bounded probe value_set_result.json passes180 seeded rational segment
cases against independent parameter-cell enumeration, with321 checked source
witnesses and29 inconsistent cases. It separately recovers {1,2} and
1,3,10,35,126 singleton components for the hypersimplex family k=2,4,6,8,10.
The band DP and partial-proof acquisition rule are derivations only.
