# Complete ordinary construction and export on the parity family

Contributor: ChatGPT (GPT-6 Astra Pro), October 10, 2026 UTC.
Same-model, nonblind DEVELOPMENT review; zero principal-clock credit.

## 1. Conclusion and exact scope

The polynomial full-evidence size and fresh-checking result extends to
construction, full DAG export and one complete producer-state serialization
for the specified fresh parity family, under explicit arithmetic, map, text
and storage assumptions. The actual recording wrapper does not force an
unrecorded exponential computation before producing the polynomial packet.
The decisive count concerns **normalized operator/operand keys**, including
cache-hit invocations, and the text bound includes every complete retained
expression key. [Recorded producer][producer]; [inherited ADD][add].

This is an additive static argument for the cap-relaxed rule schema. No worker
was imported or run, no new dimension was tried, and no implementation cap,
source, invoice or earlier theorem was changed. It supplies no new measured
latency, common-tariff bill or finite crossover. The earlier complete size
proof and the independent fresh-verifier bound remain separately attributable.
[Size construction][size]; [fresh-verifier reconstruction][fresh].

The ordinary path considered here is a fresh `RecordingManager`, one successful
`export_dag(..., base=None)`, `to_wire`, and `state_bytes`, followed by a fresh
independent receipt. It does not use `export_tree`, the ordinary manager's
unrequested extrema service, or useful previously admitted portfolio domains.
The supplied incumbent and requested bound are still checked; this route does
not replace the receiving service with a trusted final ADD root.

## 2. Sizes and primitive conditions

Let $`S`$ count constructor occurrences in the **expanded** input forest:
the current hard and soft formulas and every loss expression validated in the
full request, including the selected difference. Physical sharing of Python
tuples does not reduce this size. Let $`A,N,E`$ count all
retained Apply facts, nodes and expression bindings after successful production,
including intermediate and subsequently unreachable facts. Write
$`F=A+N+E`$.

Let $`L`$ include the complete encoded full packet and independently supplied
current/source records, order, witness and identifiers. In particular, it
includes every full expression-key string, not only the number of bindings or
the last reachable graph. Let $`P`$ be the actual byte length of the installed
program closure, not the much shorter source digest record. Let $`B'`$ bound
the component widths of every exact rational intermediate used by the current
construction and validation, including temporary arithmetic and incumbent-rank
prefixes. An arbitrary soft-row sum cannot be bounded by the largest individual
input literal alone. Any variable-width numeric metadata other than the bounded
IDs, positions and counts is included in $`B'`$ too.

For a deliberately loose accounting parameter, set

```math
K=1+S+A+N+E+L+P,
\qquad
w=B'+\lceil\log_2(K+2)\rceil+1.
```

The extra logarithmic width covers IDs, positions, lengths and counters. The
following conditions are sufficient and match the conservative model used for
fresh checking:

1. Exact arithmetic, normalization, numeric hashing and decimal conversion on
   $`O(w)`$-bit operands cost at most $`O((w+1)^3)`$ bit work. Ordinary string
   and tuple operations pay for all examined characters, occurrences and
   scalar components. Fractions, complete expression keys and hash comparisons
   are not unbounded unit-cost primitives.
2. Across $`O(K)`$ ordinary map operations with at most $`O(K)`$ stored entries,
   allow $`O(K^2)`$ probes, including collision chains and rebuilding. Each key
   probe pays for the complete possible key comparison. This does not need
   expected constant-time hashing; a deterministic scan table satisfies a
   compatible conservative abstract contract.
3. Finite JSON parsing/encoding, copying, slicing, appending and canonical
   comparison sorting have their ordinary polynomial costs in the examined
   structure and text, with arithmetic charged separately. A quadratic
   allowance per parsed/encoded text, and a cubic overall allowance for key
   probes and sorting, suffices below. There are no input-supplied executable
   hooks or implicit decompression.
4. Inputs and private state are owned canonical built-in data, and the abstract
   machine has sufficient polynomial stack/storage. Fixed module installation
   and actual program-file processing are either counted by $`P`$ under the
   declared byte/I/O/hash model or explicitly fixed infrastructure. Arbitrary
   operating-system delay, hostile Python subclasses or process mutation are
   outside this statement.

These are conditions for an algorithmic bound on the inspected source
structure, not a formal complexity theorem for CPython's allocator or every
standard-library primitive. They also differ from the deployed abstract
opcode/native-event and byte tariff. The [fresh-verifier note][fresh] gives
the elementary cubic arithmetic allowance and the same source-size distinction.

## 3. All recursive Apply calls are counted

In `Manager.apply`, a key is `(operator, left ID, right ID)`, with operand
normalization only for the declared commutative operators. A cache hit returns
immediately. A miss either uses a local identity/terminal rule or chooses the
earliest live variable and makes exactly two recursive cofactor calls before
storing its result. After cofactoring, the minimum live variable level strictly
increases. Therefore the same pending normalized key cannot recur among its
own descendants. Python's sequential argument evaluation completes and stores
the first child before starting the second. A later sibling occurrence is a
cache hit. [Inherited `Manager.apply`][add].

For one successful fresh construction, every distinct miss is consequently
stored once. Let $`T`$ count Apply entries initiated outside `apply` itself and
let $`R\le A`$ be the misses that actually recurse. Viewing all these entries
as a call forest gives

```math
\#\mathrm{ApplyCalls}=T+2R\le T+2A.
```

This includes every recursive cache hit. It does not infer runtime from a
counter that records only final cache size. The successful-run qualification
matters: a cap exception can interrupt an active computation before its key
is stored. The parity argument concerns the successful rule schema with
sufficient resources, not a fabricated all-budget completion claim.

For `compile`, the recursive `go` follows the input grammar, stopping at cached
expressions. A non-leaf expression miss initiates one Apply. If there are
$`h`$ hard and $`s`$ soft rows, `_current_goal` adds one Apply per hard row,
three per soft row, and four final rank/guard/loss operations. Thus

```math
T\le E+h+3s+4=O(S+1),
\qquad
\#\mathrm{ApplyCalls}=O(S+A+1).
```

Node or terminal interning is attempted a constant number of times per
relevant expression or Apply miss. The resulting unique-table operations are
also $`O(S+A+1)`$. `RecordingManager.apply` and `.compile` save and restore
only their work-counter context. `_RecordingDict.__setitem__` performs a
fresh-key test, the base insertion and one appended log record; it does not
scan or copy all prior facts. List growth and map rebuilding remain charged
by the primitive model. [Recording methods and `_current_goal`][producer].

Expression keys require separate care. `compile` validates and canonicalizes
the complete supplied expression even before its recursive cache lookups.
Tuple hashing or equality can reread an entire nested prefix. With expanded
size $`S`$, the largest such key has at most $`S`$ constructor occurrences,
and even a chain of prefixes can require quadratic aggregate occurrence work.
Neither pointer identity nor a compact final diagram licenses omitting it.
These traversals are covered below by the full syntax/key lengths.

## 4. Export and live state remain flat in graph references

The following operations are present in the inspected producer; their work is
part of the construction-to-delivery bound.

| Operation | Required work included in the bound |
| --- | --- |
| Frame/current preparation | `Frame.__post_init__`, `record`, full expected-record comparison, witness feasibility, bound validation and `rank_bounds` traverse the supplied records and syntax. Exact rank-prefix arithmetic uses the declared intermediate-width parameter. |
| `export_dag` | Runs `_current_goal`, slices the retained node/fact logs, converts them to tuples, records each node and canonicalizes every retained expression key. Full mode exports all retained facts, not a claimed minimal reachable closure. |
| `AddEvidence.__post_init__` | Checks headers, counts, every node and Apply field, duplicate-key sets, and every expression binding. `_expression_key` scans UTF-8 text, parses JSON, recursively decodes the syntax, runs `K.validate`, and canonicalizes again for exact equality. These producer-side checks are paid work even though semantic authority belongs to the independent receiver. |
| `to_wire` | Performs the separate complete JSON and UTF-8 encoding, then checks the actual final byte length. `export_dag` itself returns the validated `AddEvidence` object. |
| `state_record` | Writes nodes and Boolean flags, node/ID unique entries, positions/order, Apply cache and proof log, and expression cache and proof log. Both expression tables canonicalize their full keys. The source context is included. |
| `state_bytes` | Serializes that complete state record, including the deliberately duplicated named tables and all temporary work required to form them. It does not substitute a child graph under every incoming edge. |

[Producer and validators][producer]; [Frame dependency][frame];
[syntax, interval and rational dependency][syntax].

Each expression-validation pass has a fixed number of structural traversals,
but duplicate sets and maps can add repeated full-key hashing/equality work.
The latter is covered by the map-probe allowance rather than described as free
or as a fixed number of character reads. Temporary slices, tuples, parsed keys
and complete encoded strings are included. The retained-state serialization
proxy has $`O(L)`$ length: it is a constant multiplicity of the packet's flat
facts, full keys and context. This is a serialized-state statement, not a claim
that its byte count equals physical Python heap usage.

Across construction and these complete passes there are $`O(K)`$ high-level
map operations. Under the stated model, allow $`O(K^2)`$ probes and charge the
loose maximum $`O(K(w+1)^3)`$ to each, including full tuple/key comparison.
This gives $`O(K^3(w+1)^3)`$ map work. If written key lengths are $`k_i`$,
then

```math
\sum_i k_i=O(L),
\qquad
\sum_i k_i^2\le\left(\sum_i k_i\right)^2=O(L^2).
```

Consequently the repeated key parsing and canonicalization, even with
quadratic text allowances per key, fit within the same conservative cubic
total. Full input passes, node/fact copying, numerical work and canonical
sorting do too. One sufficiently loose combined bound is

```math
T_{\rm producer}(K,B')=O\!\left(K^3(w+1)^3\right).
```

One charged period of serialized producer storage adds only its declared
$`O(L)`$ byte term. The bound is output-sensitive: $`F`$ and the complete
written keys can be exponentially large for other input families. For a warm
producer one must also count its retained historical expressions and context;
the small current request alone cannot bound previously accumulated state.

## 5. Substitution for the stipulated parity family

For the two forward/reverse parity folds in an empty manager, the established
construction supplies

```math
S=O(n),\qquad A,N=O(n^2),\qquad E=O(n),
\qquad L=O(n^2\log(n+2)).
```

This uses the full recorded construction, including intermediates and every
prefix key. Metadata has no unrelated growing payload, the program closure
is fixed, and the family has no hard/soft rows. All rational values involved
in the difference and goal are fixed small integers; the rank/cutoff is zero.
Thus $`B'=O(1)`$ and $`w=O(\log(n+2))`$. [Existing size and fact proof][size].

The loose producer bound therefore becomes

```math
T_{\rm producer}(n)=O\!\left(n^6\log^6(n+2)\right).
```

The exponent is neither tight nor measured. The independent fresh-verifier
bound has a compatible polynomial order when applied to the same complete
packet. Extra current-request transport, source enrollment, common reporting
and live-state delivery use the already identified full records and fixed
number of flat passes; they do not introduce an assignment search on this
family. Therefore the complete ordinary construction-to-fresh-receipt route
has a polynomial algorithmic upper bound under the named conditions.
[Fresh receiver and wrapper reconstruction][fresh].

By contrast, the inherited empty-history tree rules require $`2^n`$ leaves
and $`2^{n+1}-1`$ visited nodes on this family. `export_tree` deliberately
targets that older vocabulary: a zero ADD root does not authorize one of its
leaves, so it refines until those rules can discharge the bound. A fixed
positive charge per visited or explicitly serialized tree node therefore
gives an exponential traversal/output lower bound for that particular route.
The full DAG-export path never calls this tree exporter. The successful parity
goal also does not enter the `NoBoundProof` counterexample branch.
[Actual legacy exporter][producer]; [tree-size proof][size].

All finite deployed restrictions remain in force: ten bits, row/cache limits,
the 4,096-bit terminal fragment, inherited syntax/depth limits, packet/key and
record limits, JSON/Python stack limits, and the fixed experiment's resource
budget. The theorem only relaxes those guards in the named abstract rule
schema and assumes resources sufficient to complete it. It does not assert
that arbitrary-dimensional Python calls are admitted, arbitrary ADD
compilation is polynomial in input alone, repeated resident histories have
constant cost, or a native portfolio with useful prior lemmas has the fresh
tree lower bound. The finite primary ordinary-direct cost advantage and the
non-nested rational-fragment witnesses are unaffected.

## 6. Review of principal section 3.3 and source preservation

The captured principal derivation, SHA-256
`1533eae8ae59254e090bdd1f5324d27456b55a3889c5d6dfda9f2459b1ecadfb`,
contains the correctly qualified normalized operator/operand-key argument and
separates `export_dag` from `to_wire`. I find no material omitted
superpolynomial path or unsupported generic-compilation claim in its section
3.3 under its stated primitive, source, owned-data and parity assumptions.
Its fixed-pass validation sentence should be read as structural passes;
full-key map comparisons remain separately charged as explained above.
[Exact principal text reviewed][principal].

The principal subsequently added the explicit cubic accounting in section
3.3. Its separately captured revision, SHA-256
`4e4dbfb7edeea4350810caf139acf25bf5e63ab86f45b4ce0603c38e0d908e6b`,
agrees with the derivation above: it includes the complete written/source
lengths, actual intermediate widths, collision/key work and parity-only
substitution. I found no additional material objection in that revision.
The [new capture][principal-v2] and its [additive manifest][inputs-v2] preserve
the earlier captured text and source binding rather than replacing them.

The [initial source manifest][manifest] binds the two implementation sources,
their inspected syntax/Frame dependencies and the prior size proof to actual
preserved copies. All five originals still matched those copies byte-for-byte
at final source capture. The [additional review-input manifest][inputs] binds
the principal derivation and independent fresh-verifier note to their captured
bytes. The latter note has SHA-256
`e2c0247f8272b2c98fa70d37879cc74f2efa48a91bd57909fbad7a7150695c89`.
These are inspected-source records, not a replacement for the complete common
service's paid installation closure.

| Inspected implementation | SHA-256 |
| --- | --- |
| `05_add_evidence.py` | `1e40f1bf7a3cb2dc9cfe46beff9a3548392e99e7ff0fa81a6c79c2f53508bbdc` |
| `05_ordinary_add.py` | `9263992673a815b15b489272aa827ea27066a0af264a85bbf905875f632abef7` |

The method was source reading, independent call-count/size reconstruction and
read-only hashing/copying. A focused Markdown-source check of this new note
and its prospective plan is recorded separately. It does not establish live
rendering, mathematical formal verification, worker execution or clock credit.

[producer]: source/v3/checks/05_add_evidence.py
[add]: source/v3/checks/05_ordinary_add.py
[frame]: source/v3/checks/05_counterfactual_transport.py
[syntax]: source/v3/checks/04_counterfactual_repair.py
[size]: source/v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/literature_and_obstruction/finite_obstruction_v1/proof_and_results.md
[fresh]: review_inputs/fresh_receiver_work_bound.md
[principal]: review_inputs/derivation_reviewed.md
[principal-v2]: review_inputs/derivation_reviewed_v2.md
[manifest]: source_manifest.json
[inputs]: review_input_manifest.json
[inputs-v2]: review_input_amendment_v2.json
