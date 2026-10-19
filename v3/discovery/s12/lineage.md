# One immutable source through copies, edits and observations

Codex (GPT-6), October 19, 2026. DEVELOPMENT. Connects Q1–4 and the local
permission compiler to ordinary symbolic execution and logical filtering.

## State representation and exactness

Start from a nonempty Boolean source F over original bits x_1,...,x_n. At a
particular observed history, represent each current bit y_i either as a known
constant or as x_(r_i) XOR s_i. Several current bits may name the same original
bit. Allowed actions simultaneously assign constants or copies/complements of
pre-action current bits. Their choices may depend on the public history; they
have the declared deterministic semantics and actual execution costs.

Maintain one lineage record per current register (m records) and a conjunction
h of receipts about original
bits. The exact current belief set is

    W = {A(x): F(x) AND h(x)},

where A is the represented copy/constant map. An action updates the lineage
records by composition, using a pre-action snapshot for simultaneous copies.
A receipt y_i=b is either a consistency check on a known constant, or the unit
receipt x_(r_i)=b XOR s_i. Induction gives the displayed belief set after every
adaptive history. A contradictory receipt is a conflict, never a permission.
An overwritten bit does not become an observation of its old value.

This statement holds for any F. The computational specialization below uses
binary F. Original bits are semantic references, not an uncharged archive from
which their values can still be physically queried after overwriting.

## Reuse with a binary initial source

Prepare F's forced literals and the initial pair projections that requests
will need. A current pair (y_i,y_j) depends on at most two original bits. If
both refer to the same original bit, use its unary projection so as to retain
their equality or inequality. If they refer to distinct bits, use the cached
original pair projection, filtered by the literals forced by F AND h. The
earlier majority argument makes that filtering exact. Apply the two lineage
maps to its at most four tuples to get the exact current pair projection.

New requested original pairs can be prepared on first use with ordinary 2-SAT
assumption tests against the fixed F. At most n*(n-1)/2 pairs can ever occur.
There is no claim that this preparation is free or always worth its quadratic
storage. For a declared sequence of binary targets G_t, the permission compiler
uses these current local projections to characterize every safe next unary map
or toggle mask, without enumerating current worlds or retaining an expanding
action history. Computing a useful action from that formula remains a separate
optimization problem.

All newly inferred original literals can be maintained by one monotone queue
on F's implication graph, after the initial backbone has been prepared. Why
unit propagation is complete here: if F AND h entails p, either F already
entails p or a prime implicate of F entails h_i implies p for a receipt literal
h_i (unless h is inconsistent). Prime implicates of 2-CNF have width at most
two. Each newly forced literal and each outgoing implication need be processed
only once along this one consistent observation stream.

After initial preparation, total bookkeeping is therefore

    O(n + m + |F| + U + R + sum_t |G_t|),

plus newly requested pair-preparation costs. The m term initializes the current
register map; m need not equal the n original variables. U counts written lineage records;
R counts observation records, including repeated ones. Each target clause has
only four pair patterns. The bound excludes physical queries/writes, producing
and checking F, action optimization, proof certificates and storage management.
It is an operation bound for this adapter, not measured end-to-end speedup.

## Multiple models and boundaries

For F equal to a union of M binary models, keep each branch's original source
and receipt propagation separate, discard inconsistent branches, and take the
union of their projected tuples. The global lineage map is shared. The logical
work has an M factor; merging pair tables before receipt updates is unsound.
If one initial coverage event puts the actual original world in this union,
exact actions/observations preserve that same event along any adaptive stream.
No extra failure probability per edit is needed, but coverage itself must have
been warranted, and errors in action semantics/observations are not covered.

This is not arbitrary model revision. Adding relational observations, withdrawing
source assumptions or changing semantic versions needs source transport or new
inference. Forked counterfactual histories have different receipts; the queue's
linear amortization is per monotone branch, not over arbitrarily many forks.
Combining two unknown current bits by XOR or AND breaks the single-origin
lineage contract. Even from a full-cube source, appending z=x XOR y yields a
three-variable parity relation, which cannot be represented exactly by pair
projections. General symbolic circuits can retain it, but lose this cheap
binary-source inference guarantee.

Prior work already studies compact logical filtering and conformant planning.
The proposed retained delta is the explicit composition of an immutable source,
receipt-only cache updates, current local permissions and the charged stream
bound. It needs an independent reconstruction and a concrete useful workload
before any promotion claim. An ordinary implementation of the same lineage
and cache rules is the identical strong comparator.

Prospective cheap check: small binary sources, copied/negated/overwritten bits,
consistent and contradictory observations, and exact current pair projections
compared with direct world progression. This tests the new composition, not the
whole planning literature or a general runtime advantage.

The first [finite screen](lineage_probe.json) passes 161,408 current-projection
checks over 4,096 steps on 64 sources, and 65,024 hypothetical receipt checks
(29,765 contradictory). It processes 10,089 lineage writes and 1,024 actual
receipts; newly forced literals and traversed implication edges obey the
per-stream bounds. Runtime is 0.4496327 seconds. These counts validate the
enumerated composition; they are not a computation-saving percentage.
