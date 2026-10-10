# ADD evidence wire contract v1

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
**R-P3-B-B DEVELOPMENT; zero overlapping principal-clock credit.**
Agreed with the independently assigned receiver implementer and accepted by
the principal before substantial implementation. Existing sources remain
unchanged. The parent owns the outer tariff, family, and delivery budgets.

## Current-bound service

The receiver independently receives the actual `Frame`, complete expected
frame record, complete feasible incumbent, and requested rational bound.
Evidence must establish that the current hard/rank-sublevel bad-set root is
zero. The supplied incumbent fixes the cutoff and establishes nonemptiness.
Both the incumbent and bound in the packet must equal the independently
supplied values; a packet may not choose a weaker request.

Producer implementation: `v3/checks/05_add_evidence.py`.
Independent receiver: `v3/checks/05_add_evidence_check.py`.

```python
receiver = Receiver(expected_source_record, epoch, bits, order)
report = receiver.receive(payload, current, expected_current_record,
                          witness, bound, work=work, request_id=request_id)
```

The producer offers full evidence or an incremental delta. A full packet needs
an empty receiver. A delta needs exact base counts and the same source record,
epoch, input count and order. Admission is atomic: no newly supplied fact gains
authority unless the complete current proof succeeds. Only the independent
caller's explicit reset may change the receiver epoch or source context.
The owner supplies a unique request ID for each attempt. Successfully admitted
IDs cannot be repeated within an epoch. `fork()` shares immutable prior facts
without changing the original receiver; the outer owner publishes the fork
only after the paid output/retention transaction succeeds. The current receipt
is exposed only for the matching successful attempt and caller request ID.

## Exact JSON object

The following are the only top-level fields. Arrays correspond to immutable
tuples in the producer object. Node IDs are implicit consecutive indices;
proof facts are listed in their actual postorder of insertion.

```json
{
  "schema": "rp3bb.add-evidence.v1",
  "mode": "full",
  "source_record": "complete canonical source-context JSON string",
  "epoch": "caller-selected-session-epoch",
  "bits": 1,
  "order": [0],
  "base": {"nodes": 0, "applies": 0, "expressions": 0},
  "nodes": [["T", 0, 1], ["T", 1, 1], ["N", 0, 0, 1]],
  "applies": [],
  "expressions": [],
  "current_record": "complete independently matched Frame.record() string",
  "witness": [0],
  "bound": [0, 1],
  "roots": {"guard": 1, "rank": 0, "difference": 0, "bad": 0}
}
```

This is a schema illustration, not by itself a valid current-request proof.
The real packet includes every needed expression binding and Apply fact.

| Field or record | Required meaning |
| --- | --- |
| `mode` | Exactly `full` or `delta`. Full uses three zero base counts. |
| `source_record` | Complete canonical JSON source context, compared with an independently supplied expected context. A digest is not an admission token. |
| `epoch`, `bits`, `order` | Fixed receiving session and complete variable order. No wire-directed reset. |
| `base` | Exact already admitted counts of nodes, Apply facts and expression bindings. |
| `nodes` | `['T', numerator, denominator]` or `['N', variable, low_id, high_id]`; IDs start at `base.nodes`. |
| `applies` | `[operator, left_id, right_id, result_id]`; unique keys, each justified by already checked facts. |
| `expressions` | `[canonical_expression_json_string, root_id]`; children already bound. Expression spelling is the inherited canonical `M._key` grammar. |
| `current_record` | Complete exact current `Frame.record()`, including source, scope, loss selection and units. |
| `witness` | Complete exact integer zero/one tuple, also supplied independently. |
| `bound` | Reduced signed-numerator/positive-denominator pair, also supplied independently. |
| `roots` | Exact guard, rank, selected difference and bad-set node IDs. Their current-request construction is independently rederived. |

Duplicate or unknown object keys, floats/nonfinite numbers, Boolean indices,
unreduced rational pairs, reassigned/duplicate proof keys, malformed expressions,
forward/cyclic node references, unordered or equal-child decisions, and stale
base/source/order/epoch data are rejected. Serialization uses exact canonical
JSON with ASCII escaping and no NaN/Infinity values.

## Source context

The producer helper constructs this exact-record shape from actual files:

```json
{
  "schema": "rp3bb.add-evidence-source.v1",
  "evidence_schema": "rp3bb.add-evidence.v1",
  "sources": [
    {"path": "v3/checks/example.py", "bytes": 123, "sha256": "64 lowercase hex characters"}
  ]
}
```

Entries are sorted by complete repository-relative path, with unique paths.
The default scientific runtime closure includes the inherited rational
grammar, base and portfolio receivers, ordinary ADD implementation, new
producer, and new checker. The outer harness may add actual shared-service
sources. The receiver receives the expected full record from that harness;
the packet cannot define which source contract the receiver trusts.

## Local Apply rules

The commutative-key normalization sorts operand IDs only for `add`, `mul`,
`min`, `max`, `eq`, `and`, and `or`. It does not sort `sub`, `le`, or `gt`.
Boolean operators require operands whose Boolean type was derived from the
checked nodes.

The existing producer first handles equal operands: `min/max/and/or` return
the operand, `eq/le` return one, and `sub/gt` return zero. Two terminals use
exact rational arithmetic or comparison. Other controlling-value rules are
zero for multiplication/and, one for or, additive zero, multiplicative one,
Boolean and-one, and Boolean or-zero. Every such rule is checked locally.

Otherwise split on the earliest variable in either operand. Each operand is
cofactored only if it has that variable at its root. Both normalized child
Apply claims must already be checked. The asserted result is either their
common result, or the unique decision node with those child results. Reduced,
ordered, hash-consed nodes make those identity checks unambiguous.

The recorder preserves the original manager's postorder: recursive child Apply
entries precede the parent entry, and child compiled-expression entries precede
the parent binding. No receiver calls the ordinary `Manager` to validate these
facts.

## Finite caps

| Item | Cap or restriction |
| --- | --- |
| Bits | 1 through 10; zero-bit inherited requests are outside this ADD service. |
| Admitted nodes | 100,000. |
| Admitted Apply facts | 200,000. |
| Admitted expression bindings | 200,000. |
| Successful receiving chunks in one epoch | 256; no implicit eviction or reset. |
| Packet UTF-8 bytes | 32 MiB. |
| Source record | 1 MiB. |
| Source closure | One through 64 distinct sorted paths; each path at most 4,096 UTF-8 bytes, each source file one through 32 MiB. |
| Current record | 8 MiB. |
| One expression key | 256 KiB, plus inherited grammar caps of 1,024 nodes/depth 32. |
| Epoch text | 256 characters. |
| Outer wire nesting | 12; nested expression syntax is carried in a bounded JSON string. |
| Computed terminal rational | 4,096 bits per numerator/denominator component. |
| Requested input bound | Inherited 128-bit rational component cap. |

The 4,096-bit wire restriction is **narrower than the old ordinary manager's
16,384-bit computed cap**. It keeps canonical integer parsing and formatting
within the ordinary interpreter's decimal conversion limit. Exceeding the new
cap is a paid unsupported/resource failure, not mathematical falsity. Limits
apply to retained admitted state as well as a single delta.

## Charged state and delivery modes

The producer will expose a full serializable state record: node table, unique
keys, Boolean flags/order metadata, Apply cache and proof log, and expression
cache and proof log. The declared retention measure is the byte size of this
record, not physical heap consumption and not node JSON alone. Proof export,
JSON encoding/decoding, full record comparison, checking, admission and current
output remain charged work. Existing operation vectors and exact rational sizes
are retained separately from the parent's named scalar tariff.

After resident delta episodes, the same producer can export a full proof for a
fresh receiver. Earlier source or proof construction is reported separately
and included under the declared total-cost horizon. An unchanged conclusion
can be reused by either method only under the same actual consumer contract.
Any later checked-ADD-to-portfolio-domain admission is an explicit additional
adapter requiring its own verification boundary, not an unverified assignment
into the old portfolio's private cache.

## Explicit checked-ADD-to-portfolio adapter

The parent selected this additional ordinary control before the first bridge
execution. `admit_checked_add` takes an actual independent Receiver and the
unchanged native PortfolioCache, independently fixed source/current records,
incumbent, bound, request ID, and a fresh old-domain handle. It invokes receiving
verification on a fork, corroborates the newly committed receipt, checks the
exact source/current/cutoff/bound/nonempty/full-sublevel fields, then stages a
new PortfolioCache containing the verified domain. It returns both staged
objects; original authority is unchanged until the outer owner publishes them.

No caller report or arbitrary dictionary can be admitted. The adapter enforces
the exact independent Receiver class using the single canonical loader name
`_rp3bb_add_evidence_receiver`. It rejects class-identity mismatches rather than
silently trusting an object with a similarly named method. The checker imports
no producer module, preventing a circular dependency.

This new checked admission is the explicit boundary extension. Subsequent
choices, replacements, proof production and receiving use the old unmodified
portfolio kernel. The adapter's old-domain cutoff also obeys that kernel's
128-bit input-rational cap; exceeding it is a paid adapter-scope failure. The
original tree-bootstrap path remains a separate charged comparator.
