# P3-11-A1: resource and witness accounting

Codex (GPT-6), October 28, 2026. Same-model mathematical confirmation unit;
the overall stage remains open. The resource statement is an algorithmic
bound, not a measured speedup or a bound on every detail of the Python runtime.

## Local work and exact subset recurrence

There are n*2^k indexed local slices. Minimize f_i on each one. If it is
infeasible, retain that disposition; otherwise maximize f_i as well.
Compactness supplies finite attained extrema. Thus at most 2*n*2^k LP calls
suffice, including infeasibility detection. The number and size of rows and
coordinates in each LP remain charged input, not a constant-time oracle.

For a consecutive sequence J of blocks, let U_J(S) be the largest possible
minimum of their local upper extrema over feasible partitions of S among J.
The empty sequence admits only S=empty, with value +infinity. Unavailable
states are absent, not zero. Appending block i gives

    U_(J,i)(S)=max_(T subset S) min(U_J(S minus T),u_i(T)),

where only two available operands are used. This recurrence follows by
partitioning all feasible assignments according to the subset T assigned
to the new block. It preserves a maximizing split, since every candidate
set is finite. It does not assume that a missing local slice is infeasible
without an LP answer or certificate.

For a single layer there are exactly 3^k pairs (S,T subset S): for each
observation choose outside S, in T, or in S minus T. Prefix and suffix
construction takes 2*n layers. For each possible anchor i and T, combining
the prefix/suffix partitions of K minus T examines at most
2^(k-|T|) splits. Summing over T gives another 3^k per block. Therefore
there are at most 3*n*3^k candidate combinations, each using a bounded
number of endpoint comparisons. Infeasible states can reduce this count.

At most n*2^k candidate intervals remain. Sorting and merging them uses
O(n*2^k*log(n*2^k)) additional endpoint comparisons. An interval entirely
contained in a previous one is harmless, and touching closed endpoints
are merged. There is no scan over n^k witness assignments in this method.

This comparison is with explicit branch enumeration, not a lower bound
against all ordinary solvers. A conventional implementation of the same
recurrence has the same bound; generic MIP may win on individual instances.
For example n=100,k=6 gives at most12,800 local LP calls and218,700 candidate
combinations before interval sorting, versus10^12 labelled witness functions
in complete branch enumeration. These are exact operation-count illustrations,
not observed elapsed-time, fee or energy reductions.

## Storage, bit operations and the implementation boundary

Prefix/suffix values and attaining splits, local extrema and anchor records
need O(n*2^k) entries. Each mask/split uses O(k) bits and each block index
uses O(log(n+1)) bits. Dense arrays indexed by masks give a direct theoretical
implementation; initialization and integer/index operations must also be
charged. The Python checker uses sparse dictionaries. Its functional
correctness does not establish an adversarial worst-case hash-table runtime
bound, and no such Python benchmark claim is part of the event.

Every finite DP value is selected from a local upper endpoint; min and max
do not add these endpoints or increase their encoding length. The final
endpoints are likewise selected from local endpoints. Exact rational
comparison pays for integer arithmetic at their actual bit lengths. A
unit-cost real-arithmetic interpretation would hide work and is not used.

For rational LP input, ordinary rational LP theory supplies polynomial-size
basic primal/dual or infeasibility witnesses. One can see the relevant
encoding control by clearing row denominators and applying Cramer's rule
to a nonsingular basic system: determinant numerator and denominator lengths
are bounded polynomially in the original rational matrix encoding. A compact
nonempty polytope has a vertex optimum, including lower-dimensional cases;
strong LP duality and Farkas supply the matching dual alternatives. This
is established LP machinery, not an additional V19 theorem or a claim that
the floating-point proposal generator always finds those certificates.

Retaining witnesses can cost much more than the final answer list. For
block dimension d_i and m_i original inequality rows, each slice contains
at most m_i+2k rows. A bounded certificate stores two d_i-dimensional points
and two multiplier vectors of that row length; an empty certificate stores
one multiplier vector. Verification rebuilds and checks these rows and
performs exact dot products. Those coordinates, multipliers, input bytes,
temporary constraints and their bit lengths are additional costs.

The development LP producer uses numerical proposals followed by exact
acceptance checks. It may fail to produce a certificate on some valid input.
The mathematical LP-oracle algorithm's completeness is not a claim of total
completeness for that numerical producer. The verifier and source-query
service have a separate conditional contract: if the supplied complete
certificate passes, its returned range and sources obey the original input.

## Rational source recovery and queries

For q in an anchor interval, stored prefix/suffix splits identify a feasible
outside partition with every local upper value at least q. Recover those
splits in O(n) table accesses, plus mask operations. Use the recorded local
maximizers outside the anchor. For anchor endpoints ell<u use

    x_lo + ((q-ell)/(u-ell))*(x_hi-x_lo).

The coefficient lies in[0,1], so this point remains in its convex slice and
has value q. If ell=u, use the recorded endpoint directly. Rational input
and q give a rational source. Its encoding length is polynomial in the
endpoint certificates and q's encoding; a very long rational query is not
free. All n vectors must be written, and the anchor's coordinates require
their exact arithmetic. The query bound is not O(n) independent of output
dimension or number length.

The implemented stabbing index sorts anchor lower endpoints and records
the greatest upper endpoint in every prefix. For a query q, a binary search
finds the last lower endpoint <=q; its prefix maximum reaches q if and only
if an anchor interval contains q. This takes O(log(n*2^k+1)) endpoint
comparisons. Band intersection in the sorted disjoint merged list uses
O(log(m+1)) comparisons for m output intervals. Source recovery then pays
the larger costs above. Changing the future readout generally requires
new LP extrema, even though the old observation slices stay the same.

## Explicit-output limitation

The fixed claim's two-hypersimplex example has k=2r, two local vectors in
[0,1]^k of coordinate sum r, and min(x_1j,x_2j)=0 for each coordinate.
Their supports are disjoint and each has at least r members. Since there
are only2r coordinates, both supports have r members and every positive
coordinate is one. They are complementary Boolean vectors. Binary weights
on the first block, with a sufficiently large constant second readout,
give binom(k,r) distinct scalar values. Each is an isolated interval component.

Therefore explicit enumeration can require exponentially many components
in k. This does not prove a lower bound on one-band feasibility, approximation,
symbolic compression or every ordinary inference algorithm. The new sharper
component theorem is unnecessary to this fixed example and is not used here.

This reconstruction finds the fixed asymptotic claim supported when entries,
endpoint comparisons and additional LP/bit/certificate work are distinguished
as above. It does not establish a practical break-even query count.
