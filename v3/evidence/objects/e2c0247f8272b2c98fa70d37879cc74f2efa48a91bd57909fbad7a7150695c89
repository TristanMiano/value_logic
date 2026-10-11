# A polynomial verification-work bound for the fresh parity receiver

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, integration reviewer,
October 10, 2026 UTC. **R-P3-B-B DEVELOPMENT; same-model, nonblind static
reconstruction. Zero principal or agent clock credit.**

This is additive reasoning after the existing parity proof-size result. It
executes no producer, receiver, experiment, analyzer or new parity dimension.
No existing source, proof, measured output, status or timing record is edited.

## 1. Conclusion

**A conservative polynomial upper bound is defensible for one complete fresh
verification of the existing parity packet, under an explicit ordinary
primitive-cost model.** The receiver does not unfold the diagram into a tree,
recursively recompute Apply, search all assignments, or expand a stored proof
dependency more than the input/lookup analysis below permits. Its repeated
expression-key processing is polynomial in the already expanded encoded input.
The retained-state serializer also preserves numeric child references.

One deliberately loose bound, allowing hash collisions, is

```math
T_{\rm fresh}(L,B)
=O\!\left((L+1)^3
  \bigl(B+\lceil\log_2(L+2)\rceil+1\bigr)^3\right).
```

Here $`L`$ counts the complete wire **and** the independently supplied current
and source inputs, and $`B`$ bounds rational component bit lengths as specified
below. The bound includes initialization/source-record validation, full receipt
checking, current-report construction and one complete retained-state
serialization. A fixed number of the wrapper's current-request/receipt
encoding passes has the same polynomial bound. Reading actual program files
for source enrollment is a separate term; for the fixed source closure it is
constant with respect to parity dimension, while a variable closure's bytes
must also be counted.

For the already proved parity construction,

```math
L=O(n^2\log(n+2)),\qquad B=O(1),
```

this gives the conservative consequence

```math
T_{\rm fresh}(n)=O(n^6\log^6(n+2)).
```

The exponents are upper bounds chosen for easy auditing, not predictions of
actual performance or claims of optimal verification. This strengthens the
certificate-size statement with a **conditional algorithmic work theorem**.
It does not establish a generic polynomial compiler or an arbitrary-dimension
runtime bound for the unchanged capped Python deployment. The measured primary
comparisons are unchanged.

## 2. Exact object and primitive model

### 2.1 The family and fresh state

The family is the one used by the inherited-tree obstruction: forward and
reverse XOR folds over the same $`n\ge2`$ Boolean coordinates, difference
$`D=A-B`$, no hard or soft rows, bound zero and a complete supplied incumbent.
There is one fixed complete variable order, a fresh receiver with no old
chunks, and one full packet from the recording construction. All required
facts are provided in dependency order. The previously proved bounds count
**all** node, Apply and expression facts, not only the final zero root.
[Existing proof and source-bound counts][size-proof].

The independent current Frame has ordinary finite tuple/tree syntax, exact
Fractions and the fixed family metadata. The expected source record, epoch,
order, current record, witness and request ID are supplied by the owner. The
optional diagnostic `work` object is a normal owned dictionary or `None`.
No input invokes attacker-defined Python callbacks through custom equality,
hash, container, Fraction or work objects. This is the same trusted owned-data
boundary as the current service; the theorem does not apply to arbitrary
mutated process objects.

### 2.2 What length and bit size include

Let $`L\ge2`$ be the total byte length of the full packet and the independently
supplied source/current records, together with ordinary explicit encodings of
the order, witness, epoch, bound and request ID. Counting duplicate material
more than once changes only constants here. The full input Frame's **expanded
syntax** is included through its current record; its number of distinct Python
objects is not the input-size measure.

Consequently the number of nodes, Apply rows, expression rows, coordinate
indices, syntax occurrences and supplied text bytes is each at most a constant
multiple of $`L`$. Every canonical expression key is a complete JSON string
inside that packet. Shared prefix syntax has already paid for its repeated
occurrences in $`L`$. Fixed source/metadata conventions are the same as in the
polynomial certificate-size theorem; arbitrary growing hidden payloads are
not omitted.

Let $`B\ge1`$ bound numerator and denominator bit lengths in the input
rationals and node terminals. In this no-rank family, the cutoff is zero.
One checked terminal equation adds, subtracts, multiplies or compares only two
already represented rationals. Before reduction its integer components require
at most $`2B+O(1)`$ bits. The verifier does not accumulate an unrepresented chain
of enormous rational values while checking an Apply row: the result must be
looked up as an already admitted terminal. The parity terminals are the fixed
small integers already documented in the proof-size review, so $`B=O(1)`$.

This argument is **not** a bound on arbitrary incumbent-rank accumulation.
For another Frame, successive soft-weight additions and intermediate
`K.interval` values can grow beyond the largest individual input component.
The present family has no hard/soft rows: both loops in `receive` are empty,
the cutoff remains exactly zero, and the corresponding `common_report` loops
are also empty. A generalization would have to bound those prefix arithmetic
values separately or define its bit-size parameter to include every exact
intermediate. No such generalization is claimed here.

Set

```math
w=B+\lceil\log_2(L+2)\rceil+1.
```

This accounts for rational operands and ordinary row IDs, table counts,
positions, lengths and diagnostic counters. Fixed source-size fields do not
grow with $`n`$. If other variable-width metadata integers are admitted, their
bit lengths must be included in $`w`$ as well.

### 2.3 Explicit cost assumptions

The bound is for the source-level rule schema under these ordinary algorithmic
conditions:

1. Exact integer/Fraction comparison, addition, multiplication, reduction,
   decimal conversion and numeric hashing of $`O(w)`$-bit operands take at most
   $`A(w)=O((w+1)^3)`$ bit work. This deliberately generous allowance is
   compatible with schoolbook arithmetic and Euclidean reduction. String
   hashing, equality, copying and scanning pay for the examined bytes. No
   unbounded rational primitive is assigned unit physical cost.
2. Arrays, tuples and ordinary maps have polynomial bookkeeping costs. Across
   $`O(L)`$ map operations with at most $`O(L)`$ entries, allow
   $`O(L^2)`$ key probes, including geometrically sized rebuilds. This permits
   worst-case collisions and does **not** assume expected constant-time lookup.
   Comparing or hashing an entire key of up to $`O(L)`$ bytes is charged.
   A deterministic linear-scan map satisfies a compatible conservative
   abstract contract; no map implementation is changed here.
3. JSON decoding walks the supplied finite text/container structure, with
   charged decimal conversion and duplicate-key map work. Encoding walks the
   supplied finite structure and pays for its emitted text. Comparison sorting,
   if used for canonical object keys, is polynomial in key count and examined
   characters. A conservative quadratic allowance in each parsed/serialized
   text length suffices below. No executable decompression or custom object
   hook is supplied by the packet.
4. The abstract machine supplies sufficient polynomial stack/storage for
   these finite traversals. Source loading and interpreter setup are fixed
   infrastructure for the named closure, or are charged separately by their
   actual size. Arbitrary I/O latency, scheduling and physical heap/runtime
   behavior are outside this model.

These are stated conditions, not a formal complexity audit of CPython's C
implementation, allocator or operating system. They are enough for a theorem
about the actual verification structure. Without such primitive conditions,
the earlier encoded-size theorem should not be described as a proved physical
runtime theorem.

### 2.4 Why the cubic arithmetic allowance suffices

For reduced operands $`a/b`$ and $`c/d`$ whose components have at most $`B`$
bits, comparison uses the cross products $`ad`$ and $`cb`$. Each product has
at most $`2B`$ bits. Addition/subtraction uses numerator $`ad\pm cb`$ and
denominator $`bd`$, with at most $`2B+1`$ and $`2B`$ bits respectively.
Multiplication uses $`ac`$ and $`bd`$, again at most $`2B`$ bits. Equality,
ordering, minimum/maximum and Boolean terminal tests require no longer chain
than these comparisons. Multiplication by a fixed Boolean or the unit/zero
terminals is included in the same upper bound.

Grade-school multiplication and long division on $`u`$-bit nonnegative integers
use $`O(u^2)`$ bit work. A deliberately coarse Euclidean-gcd bound is
$`O(u)`$ divisions: after at most two remainder steps the larger relevant
argument drops by at least a factor of two. Assigning every division the
maximum $`O(u^2)`$ cost therefore gives $`O(u^3)`$ for reduction. Dividing
the numerator and denominator by the gcd costs no more. Sign normalization,
bit-length checks and comparison are covered as well. Decimal parsing by
repeated multiply/add and printing by repeated division also fit this cubic
allowance. Thus the use of $`A(w)=O((w+1)^3)`$ pays explicitly for exact
Fraction normalization; it does not silently replace gcd by a unit primitive
or assume all rational operations cost only $`O(B^2)`$.

The numeric-hash condition is explicit too: a hash computation must take
polynomial work in its examined integer/rational representation. This review
does not import constant-time unbounded Fraction hashing. Any relevant
numeric-hash work is included in $`A(w)`$ before the collision/probe allowance.

## 3. Source-level reconstruction

All locations below refer to the preserved source bytes linked in §6. A fresh
packet makes the apparent historical-store loops particularly simple.

| Path | Actual work and why it does not expand exponentially |
| --- | --- |
| `_wire`, `_depth_scan`, `_json`, `_pairs`, `_json_integer` | The outer wire is scanned and parsed. Strings that contain expression keys remain strings at this stage. Duplicate object fields are checked through finite maps; decimal integers are parsed with the bit cost above. No diagram traversal occurs. |
| `_source_record`; `Receiver.reset` | Source fields, sorted paths, digest syntax and canonical JSON are checked. The order is validated and a position map is later built. The receiver checks a supplied source record; it does not execute the named source programs or read every file here. |
| `Receiver.receive` current-input preamble | `Frame.__post_init__`, `Frame.record`, current-record comparisons, witness/type checks and requested-bound checks traverse ordinary current syntax and supplied metadata. In this exact family the hard/soft loops are empty and the rank is zero. There is no enumeration of Boolean assignments. |
| `_View.node` and `_View.lookup` | During the complete admission pass, `self.state` is the empty pre-receipt state. New nodes and facts are in pending arrays/maps. The `reversed(self.state.chunks)` loops therefore make **zero** old-chunk iterations. The pass does not publish one chunk per row. |
| `_View.admit_nodes` | Each node row checks a fixed number of prior child IDs, their order levels and Boolean flags. A unique-table lookup uses the constant-arity node tuple. It never recursively follows a child's descendants. |
| `_View.admit_applies`; `_operation_result` | Each Apply row checks a fixed number of node/table references. A terminal case performs one bounded rational operation. A nonterminal case determines the earliest variable and checks the **two already admitted cofactor Apply results**. The methods `operation` and `lookup` retrieve facts; they do not call `_operation_result` recursively or recompute Apply. |
| `_expression`; `_syntax_key`; `admit_expressions` | Each written expression key is parsed into its full syntax tree, recursively type-checked and re-encoded once for canonical comparison. The row then re-encodes at most two immediate child subexpressions to look up their already checked bindings. It does not recursively admit or verify all descendant bindings afresh. |
| Current root reconstruction | The difference binding is retrieved from the current expression. The no-hard/no-soft guard/rank and zero bound need a fixed number of Apply/terminal lookups. A checked zero bad root discharges the claim; there is no cube search. |
| `next_state`; receipt construction | Pending arrays become tuples and a **single** chunk is attached. The first receipt ID tuple has one element. The report and canonical receipt contain the current record and scalar counts, not an expanded diagram. The final pointer swap does not initiate another proof pass. |
| `state_record`; `storage` | Nodes are serialized with numeric child IDs. The unique table adds a constant number of copies of those node records; Apply rows remain tuples of IDs, and expression entries remain already written key strings. The serializer never substitutes a child graph under each parent. The one current receipt/source/order record adds only the declared text. |

The decisive absence of recursion is in `_operation_result`, lines 413–454 of
the receiver. Its two Shannon dependencies are calls to `self.operation`,
which normalizes two IDs and performs a map lookup. A hypothetical recursive
recomputation of those dependencies could duplicate work, but that is not the
implemented receiving rule. [Frozen receiver][receiver].

Expression syntax recursion needs a different argument. It really does reread
the parity prefixes, and `_syntax_key` is not a memoized encoder. Nevertheless,
each of those prefixes is fully present as text in the packet. If row $`i`$
has key length $`k_i`$, its child encodings are no larger than a constant
multiple of $`k_i`$, and

```math
\sum_i k_i=O(L).
```

Even assigning quadratic parse/encode cost per such text gives
$`\sum_i O(k_i^2 A(w))=O(L^2 A(w))`$. The final current-difference encoding
adds a constant number of traversals of the separately counted current syntax.
Counting only distinct expression objects and omitting those full keys would
invalidate this accounting; the existing certificate-size proof does not make
that omission. [Frozen expression admission][receiver]; [prefix-size proof][size-proof].

In particular, parsing a long key does not generate one new table admission
per descendant. The key grammar consists of tagged arrays, rational strings
and indices; `_expression.read` traverses those array occurrences and updates
a one-element count list. It returns one parsed expression. `admit_expressions`
then performs a fixed number of ledger operations for that row: duplicate
lookup, at most two child-binding lookups, the applicable operation/terminal
lookup and the final insertion, plus fixed-size work-counter updates. Across
all rows these are $`O(L)`$ map operations, not the product of row count and
all prefix lengths. The much larger reread/re-encode work is the separate
$`\sum_i k_i^2`$ allowance above. Outer/source/metadata duplicate-key maps
are bounded by their separately counted written structure.

## 4. Combining the bounds

There are $`O(L)`$ fixed-row checks and high-level table operations for the
nodes, Apply facts, expression bindings, source/order metadata and current
claim. Per-row node and Apply keys have constant arity and $`O(w)`$-bit
components. Expression keys can contain $`O(L)`$ bytes, but their construction
is separately bounded above. The maximum map size is $`O(L)`$.

Under the collision-tolerant map condition, there are at most $`O(L^2)`$
key probes overall. Charging the excessively conservative bound
$`O(L A(w))`$ to every probe, including any full-key comparison and numerical
work, gives

```math
T_{\rm maps}=O(L^3 A(w)).
```

Node/Apply arithmetic outside those lookups is $`O(L A(w))`$. Outer JSON,
source/current validation, expression parsing and canonical re-encoding are
bounded by $`O(L^2 A(w))`$ under the stated text model. Any canonical
comparison sorting can be covered by the same conservative cubic total,
even without using a tight sorting bound. Exact work counters add only
polynomial-width integer updates; they do not change the order.

The complete freshly retained state has $`O(L)`$ encoded length for this
family: a constant multiplicity of flat node/fact rows, the full expression
strings already counted in $`L`$, one source/order record and one current
receipt. The JSON quoting layers have fixed multiplicity. The retained state
has no recursively materialized copy of a diagram below each incoming edge.
Its construction and one serialization are therefore covered by the same
polynomial allowance. Taking $`A(w)=O((w+1)^3)`$ gives the bound in §1.

This proof does not need a favorable average distribution of hashes. Tighter
bounds may follow from the aggregate key lengths and more specific parser/map
algorithms, but this note does not claim them. A loose polynomial is sufficient
to rule out a hidden forced exponential traversal on the stipulated fresh
family under the named model.

### 4.1 The service wrapper and source enrollment

The current wrapper's ADD receiving path decodes and reconstructs the complete
current request, initializes or forks the receiver, calls `receive`, constructs
the common report, serializes the receiving live state and delivers it. For a
fresh parity packet those extra receiving operations are a fixed number of
passes over the same current record, packet and flat receiver state. The
`common_report` hard/rank loops are empty here. They add no tree search.
The producer's compilation/export work and producer-state serialization are
different costs and are not credited to this verification theorem. [Frozen
service, `request_from_wire`, `_execute`, `common_report`, `_receiver_state`][service].

`Receiver.reset` validates the **source-record text**. Actual program-file
enrollment is `Session._enroll`: it prepays capacities, reads each admitted
file and checks its SHA-256. If their combined length is $`P`$, those bytes
cannot be charged only by the much shorter digest record. For the fixed current
source closure $`P`$ is constant in $`n`$. Under a byte-linear I/O/hash model its
file-processing term is $`O(P)`$, with the record bookkeeping already counted.
For a claim allowing a varying source closure, a safe formulation counts
$`L+P`$ and the corresponding integer widths instead. No exponential amount
of source text may be hidden behind a binary length field or digest.

This is an algorithmic accounting statement. It supplies no new common-tariff
invoice, low-budget execution, paid-success envelope or proof of physical
latency. The wrapper's terminal reserve and failure-publication contract keep
their separate source-bound arguments.

## 5. Scope of the strengthened theorem

The earlier result may accurately be strengthened to:

> For the stated parity family and fixed order, the uncapped recording/checking
> rule schema has polynomial-size full shared evidence and a polynomial-work
> fresh verification procedure under the stated exact arithmetic, map and text
> cost model. The inherited empty-history tree rules still require exponential
> visited trees. The receiver verifies input linkage, the complete current
> bad-set obligation and nonemptiness; the comparison is not based only on a
> compact final root.

The statement remains **receiver- and family-relative**. Its uncapped schema
parameterizes the relevant bit, row, text and expression-depth allowances and
assumes sufficient algorithmic stack space. The actual source retains its
ten-bit restriction, node/Apply/expression and receipt caps, JSON/key/source
size and integer-digit limits, 4,096-bit terminal limit, inherited expression
limits and canonical-record depth limit. Python/JSON recursion limits also
remain real implementation constraints. No source cap was changed and no
large-dimension acceptance was attempted.

The polynomial work statement does not prove that an arbitrary expression has
a small ADD or a small recording trace. It does not make the exact-root bridge
total over all inherited rational inputs: the preserved 7,914-bit denominator
witness remains outside its 4,096-bit exported-terminal fragment. It does not
cover unbounded resident histories by pretending their old store is empty,
or give untrusted process mutation and custom callbacks this input-length
bound. It establishes no physical speed advantage at the small tested sizes.

The original source-bound theorem and the primary adverse comparisons remain
intact. The new implication is specifically that, after making the text,
arithmetic and dictionary assumptions explicit, complete fresh checking of
the already constructed parity evidence also admits a polynomial bound.

### 5.1 Repeated empty deltas are a different case

An empty delta need not add any node, Apply or expression fact. Nevertheless,
each successful `receive` calls `next_state`, appends a new `_Chunk` and adds
the new request ID. With one initial nonempty chunk followed by empty chunks,
looking up an old terminal can inspect every newer chunk before reaching its
original unique-table entry. The cost of that lookup grows linearly in the
number of successful receipts; `state_record` also walks and serializes the
empty-chunk and request-ID history. Constant scientific-fact counts therefore
do **not** imply constant incremental checking, retained state or serialized
cost. The deployed 256-receipt cap bounds that history but does not erase it.

This is consistent with the present proof. During a single fresh admission
the `_View` continues to reference the empty old `_State`; all imported rows
stay in its pending containers until one final `next_state` creates exactly
one new chunk. No old receipt history is omitted from this fresh input because
there is none. A history-dependent verification theorem would need an explicit
history/chunk-size parameter, and the repeated serialization bill would need
its own summation. No constant-cost delta claim follows here.

## 6. Source binding and method

This review read the following current files and compared each byte-for-byte
with its `primary_v5` preserved copy. All four matched. The links point to those
preserved copies, not to a future changed implementation.

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| [Independent ADD receiver][receiver] | 33,036 | `1f396bbb625614c87d48fa5fece438851999a7afeb58d5af6933812b4038c2bf` |
| [Frame/canonical-record dependency][frame] | 16,360 | `48422eb4b23ab38d2b755de76000edaa38231dce6064c2f9cb71e45702c9ae35` |
| [Inherited syntax/rational dependency][syntax] | 22,823 | `c71692e2e84c52f915dd1d09048344bf1d6c53e7d0362fe82a598d8f3d0ab896` |
| [Paid service wrapper][service] | 36,584 | `b96cae82e0fe3f0f734671d57df81ac3a62350746f73228aef63c2f77bb1745f` |
| [Earlier complete size/count proof][size-proof] | 22,114 | `614b0b02d578cd2eb2848155adccfff7a70bca14a788eb52b611f838e1c4d6e0` |

The source inspection also followed `Frame.__post_init__`, `Frame.record`,
`Request.__post_init__`, `Request.record`, `canonical`, `validate` and
`interval`. The fresh no-hard/no-soft family reaches no inherited search,
band construction, portfolio proof traversal or ordinary ADD manager call
through this receiving path. Fixed module installation is not mistaken for
input-dependent proof work.

The review consists of source reading, complexity reconstruction and source
hash comparison. No worker import or execution, experimental measurement,
new $`n=9`$ or $`n=10`$ exposure, source edit or clock credit occurred. A
focused Markdown-source check does not constitute a live rendering or
formal implementation-verification claim.

[receiver]: ../../development/primary_v5/sources/v3/checks/05_add_evidence_check.py
[frame]: ../../development/primary_v5/sources/v3/checks/05_counterfactual_transport.py
[syntax]: ../../development/primary_v5/sources/v3/checks/04_counterfactual_repair.py
[service]: ../../development/primary_v5/sources/v3/checks/05_certificate_delivery_service.py
[size-proof]: finite_obstruction_v1/proof_and_results.md
