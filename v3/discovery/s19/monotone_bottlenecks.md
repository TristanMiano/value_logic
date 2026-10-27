# Monotone bottlenecks need only the ordinary covering transform

Codex (GPT-6), October26,2026. DEVELOPMENT. A refinement using established
covering products and Stoian's threshold-chunk idea; no priority claim for
the general transform or square-root decomposition.

For the receipt tables, T subset S implies u_i(T)>=u_i(S), with an empty
slice represented by minus infinity. Prefix, suffix and omitted-block
bottleneck tables inherit this decreasing property: remove obligations
from a feasible partition and each local upper endpoint can only improve.

Let f,g be two such decreasing tables on k elements, N=2^k, and let

    h(S)=max_(A subset S) min(f(A),g(S minus A)).

For downward-closed Boolean tables F,G, a cover A union B=S with F(A)=G(B)=1
exists exactly when a disjoint such cover exists. Remove A from B; downward
closure preserves G(B minus A). Thus Boolean subset feasibility can be
computed by the ordinary unranked covering product:

    C = Mobius( zeta(F) * zeta(G) ),

where multiplication is pointwise over integers. C(S) counts covering
pairs, is nonnegative, and is positive exactly at feasible partitions.
Each transform costs O(k*N) integer operations and O(N) temporary entries.
Counts and intermediate sums have O(k) bits; bit complexity is charged
separately from operation counts. This is the existing covering-product
identity, not a new transform.

## Preserve downward closure even when a chunk cuts through a tie

Sort the 2N tagged entries of f and g by decreasing value, then increasing
subset cardinality, then side and mask. At every prefix, each side's active
Boolean table is downward closed. A proper subset has either a larger value
or the same value and smaller cardinality, so it was activated earlier.
Arbitrary tie order would not give this property.

Process chunks of B tags. After activating a chunk, use the covering
product to find outputs S that become feasible for the first time. For each
such S, scan the chunk. A new f(A) tag with A subset S proposes partition
(A,S minus A) if the complementary g entry is active; a new g(B) tag
proposes the symmetric partition. Take the largest actual min-value among
these proposals, and retain its split witness.

At least one proposal exists: there is an active partition now, none before
the chunk, so a member of that partition is new. Every active partition
uses at least one new tag, so the scan finds their best value. Any partition
using a future tag has bottleneck no larger than the last value of this
chunk; a currently feasible partition has bottleneck at least that value.
Thus the result is already the exact global h(S), including ties. The
plus/minus infinity sentinels are ordered symbols; minus-infinity outputs
do not warrant a feasible source witness.

There are O(N/B) transforms and each output scans one chunk, giving

    O(k*N^2/B + N*B + k*N)

operations after including tag sorting and scans. For k>=1, choose
B=ceil(sqrt(k*N)), capped by2N, giving

    O(sqrt(k)*2^(3k/2) + k*2^k)

integer/arithmetic/comparison operations and O(2^k) temporary entries.
Handle k=0 directly. Monotonicity can be checked on the k*2^(k-1) cover
relations before using this implementation. Ordinary ranked subset
convolution remains available for arbitrary nonmonotone input tables.

Consequently AR1 can use this refinement for its O(n) prefix, suffix and
omitted-block convolutions. After its local LP table is obtained, its
combination work becomes

    O(n*sqrt(k)*2^(3k/2) + n*2^k*log(n*2^k)),

with O(n*2^k) stored scalars and O(2^k) temporary transform entries, plus
the separately charged local certificates and exact-number bit costs.
This improves a polynomial factor in the earlier conservative bound, not
the exponential base. It is not an end-to-end measured speedup or a
replacement for strong direct solvers on individual requests.

## Small development check

The prospectively hashed monotone_subset.py and monotone_subset_probe.py
passed400 exhaustive monotone ternary k=2 pairs and240 seeded cases through
k=8, with14,949 exact value/split checks. The adapter also matched all180
previously exposed polygon cases and reconstructed472 valid source
witnesses. Nonmonotone input is rejected. The saved run took1,379,273,000ns;
its7,274 covering calls,1,917,882 transform additions,207,056 products and
622,296 tag scans describe this panel only. They are not a matched
end-to-end saving against the earlier different panel or a production solver.
The plan binds every imported helper and exposed input/result. This is
same-model DEVELOPMENT, with shared helpers and no independent confirmation.
