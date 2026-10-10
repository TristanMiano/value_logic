# Independent ADD receiver design v1

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.
Same-model independent implementation, DEVELOPMENT; zero principal-clock credit.
The parent assigned implementation after the initial
[receiver reconstruction](reconstruction.md). This is a new finite adapter;
the accepted historical sources remain unchanged.

## API and ownership

Implementation: [05_add_evidence_check.py](../../../../checks/05_add_evidence_check.py).
It imports the accepted finite `Frame` grammar. It imports neither the ordinary
ADD manager nor the new producer. The producer and exact schema are owned by
the independently assigned ordinary-controls agent; see the
[agreed wire contract](../ordinary_bridge/wire_contract_v1.md).

```python
receiver = Receiver(expected_source_record, epoch, bits, order, work=work)
candidate = receiver.fork(work=work)
report = candidate.receive(payload, current_frame, expected_current_record,
                           witness, bound, work=work,
                           request_id=owner_unique_request_id)
receipt = candidate.current_receipt(owner_unique_request_id)
state = candidate.state_record()
retention = candidate.storage(work=work)
# The outer owner publishes candidate only after charged terminal delivery.
```

The current frame, expected full frame record, complete witness and requested
bound are supplied independently. The producer cannot weaken any of them in
its packet. The owner supplies a complete expected source-closure record
containing the actual paths, lengths and SHA-256 values, including both new
producer/checker sources and the declared dependencies. Equality to that full
independent record is a binding check; the receiver does not discover the
dependency closure, reread its files or authenticate a digest as a certificate.
The outer service charges and verifies that source procurement separately.

`full` requires a fresh receiver and zero base counts. `delta` requires exact
resident counts and identical source, epoch, input count and variable order.
Neither mode may reset state through a wire field. `reset` is an explicit
trusted owner operation; fresh allocation is available. The initial common
scope is one through ten Boolean coordinates and one rank tier. Admitted
terminal rationals have at most 4,096 bits per component, a declared restriction
below the old manager's 16,384-bit computed-terminal cap. Input expressions
and requested bounds retain the inherited 128-bit component cap.

## What is checked

The verifier first bounds the UTF-8 wire, checks JSON nesting, rejects duplicate
keys and inexact numeric encodings, and validates exact object fields. Node
identifiers are exact integers, excluding Booleans. Terminal rationals must
have positive denominators and be reduced. Every decision node has unequal
already available children strictly later in the fixed variable order. Unique
table entries are reconstructed; duplicate nodes are rejected. Boolean type is
derived from the checked terminals and children, never from a producer flag.

Each pointwise Apply row is justified by an exact arithmetic identity, an
exact terminal equation, or a Shannon split whose two child Apply claims have
already been checked. Noncommutative operators retain operand order. Every
expression key is independently parsed against the fixed grammar, with child
bindings required before the parent. A root is accepted for an expression only
through those checked bindings. All facts admitted to the resident cache are
unconditional functions of the coordinate assignment. Hard-guard premises
are never admitted as unconditional equalities.

The receiver checks the incumbent directly against every current hard row,
computes its exact rank from the supplied current weights, and reconstructs
the complete current hard/rank guard and receiving difference using already
checked denotations. It then reconstructs the current bad-set function and
requires its root to be the unique rational-zero terminal. It never accepts a
producer's root name or `bad = 0` assertion without this derivation.

## Soundness reconstruction

Induct on node admission order. Each terminal denotes its stated exact rational;
each decision denotes its two children's values selected by the named bit.
Strict variable order and backward references give a total acyclic function.

Induct on Apply admission order. Exact terminal equations and listed identities
preserve pointwise semantics. In the remaining case, the checked child facts
give the required operation on both cofactors of the earliest variable. Their
reduced decision therefore denotes the pointwise operation everywhere. This
induction has no current-frame or hard-guard premise.

Induct on expression admission order. Literal and bit bindings are checked
directly. Each constructor is linked through its previously checked children
and the appropriate unconditional Apply fact. It therefore denotes the fixed
grammar expression on every Boolean assignment.

Finally, the independently evaluated feasible incumbent belongs to the current
guard. Every assignment in that guard belongs to the entire incumbent sublevel,
including all tied optima. If its receiving difference exceeded the independently
fixed bound, the correctly constructed bad function would be one there. A
checked constant-zero bad function rules that out. Thus the result is exactly
the nonempty uniform-bound service reconstructed from the native portfolio
receiver. It is not an optimal-incumbent, exact-minimizer-identity, calibration
or economic-value theorem.

## Persistent state and failure boundary

An admission chunk contains nodes, derived Boolean flags, unique keys, checked
Apply mappings and checked expression mappings. Private dictionaries cease to
be mutated when admitted. A new request stages new tables and validates the
whole claim before one state-pointer swap. Old tables are shared through
immutable chunks, avoiding a full copy of old proof tables for each delta.
Lookups explicitly traverse at most 256 admitted chunks. This is a real
algorithmic overhead, counted in the work vector and common event tariff.

There are at most 256 successful receipts in an epoch, with no implicit eviction
or reset. The total node, Apply and expression caps apply to cumulative state,
not just a packet. An empty delta still checks the full new claim and consumes
a receipt. A rejected attempt adds no denotation chunk. The independent
caller-owned request id prevents an old current receipt from becoming evidence
for a new request. Already admitted ids cannot be reused in the same epoch.
An invalid attempt invalidates retrieval of the previous current receipt.

There can be an interpreter interruption after the internal pointer swap and
before the caller receives the return value. The parent owns the resolution:
it performs work on `fork()`, serializes the complete retained state and current
receipt, and publishes that candidate receiver only after funded terminal
delivery succeeds. On any failure it discards the candidate. The previous
unconditional state can remain valid while its earlier request receipt is
inapplicable to the new unique id. This is distinct from pretending that an
internal successful proof check guarantees funded end-to-end delivery.

`state_record()` serializes every retained table, including unique keys and
Boolean flags even where they duplicate information derivable from nodes. It
also includes source/order binding, counts, admitted request ids, the immutable
committed receipt record and attempt metadata. `storage()` reports the exact
canonical byte size of this declared proxy. It does not measure Python heap
overhead. An exported state record is not an authenticated import facility;
a fresh receiver still needs a full proof checked through its normal API.

The raw counter dictionary counts parser characters, admitted rows, record
comparisons, rational checks, node/fact/chunk lookups, current feasibility/rank
checks and retained serialization bytes. These diagnostics do not purport to
be a complete resource tariff. The parent owns the common bounded event and
byte tariff, staged budget denials, protected terminal output and paid failure
receipt. No resource-success result is claimed from this design note alone.
