# Ordinary ADD evidence bridge: initial design

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
Task: **R-P3-B-B, DEVELOPMENT**. Same-model, nonblind implementation assignment.
All overlapping reviewer time earns **zero principal research credit**. This
note changes no prior source, status, ledger, freeze, or contribution decision.
Base commit: `33c6d6795aac894bd3cf8575e44f1d6f38f6ae56`.

## Receiving service

The common conclusion should be a checked upper bound on the **entire current
incumbent sublevel**, with independently checked nonemptiness. Let the current
frame supply its Boolean hard rows, positive weighted soft rows, selected
rational loss difference, and full interpretation/source metadata. For the
supplied complete feasible incumbent $`w`$, define:

```math
X=\{x\in\{0,1\}^n:\text{every current hard row is true at }x\},
\qquad r(x)=\sum_j a_j(1-s_j(x)),\qquad \tau=r(w).
```

The requested conclusion is:

```math
w\in X,\qquad
\forall x\in X\;\bigl(r(x)\le\tau\Longrightarrow d(x)\le B\bigr).
```

This domain includes all current minimizers and all ties at the incumbent
cutoff. It need not equal the minimum-ranked subset. The common service need
not demand an exact lower extremum, exact optimal rank, selected-source
identity, or probability report. Those would be stronger outputs than the
existing portfolio receiver supplies.

The receiver obtains the current `Frame` and its complete `Frame.record()`
independently of the producer. A scope label or digest is not a substitute for
this record. It validates the request and chosen loss unit, checks the witness
against every current hard row, recomputes its rank, checks the supplied bound
and evidence, and reports the common current-bound conclusion. A refused or
resource-exhausted proof supplies no certified answer.

The implemented inherited scope is at most ten bits and one rank tier, with
the original Boolean/rational expression grammar and original input caps.
Computed rational components can be larger than input components; that work
and the chosen evidence caps must be explicit. This bridge is not a native-v2
compiler, causal discovery method, authenticated transport, or sandbox for
malicious Python code.

## What the current ordinary solver actually provides

`05_ordinary_add.Manager.query` already checks the complete frame record and a
feasible witness. It compiles hard rows, weighted rank and selected difference,
constructs the incumbent guard, and computes exact attained extrema using
memoized node-pair recursion. Its return value includes guard/rank/difference
roots. Its `export()` method explicitly describes the diagram as private
correctly constructed state, not a verified imported diagram.

The manager retains immutable mathematical nodes and maps for unique nodes,
Apply results, and compiled expressions. These tables give a concrete route
to proof export without editing the old manager. An exporter can subclass or
wrap the existing producer, retain its exact operations, and emit their
justifications. The producer remains untrusted at the receiving boundary.

`BandProof` accepts only exhaustive splits and hard, rank, or interval-loss
leaves. `PortfolioProof` additionally permits independently checked
nonnegative-multiplier witnesses and admitted older certificates. Neither
current receiver accepts an ADD terminal as a reason for a leaf.

## Legacy path export

Proposed producer API:

```python
export_tree(manager, frame, witness, bound, expected_record,
            *, symbolic=True, work=None) -> PortfolioProof
```

The proof has no old choices and uses the existing `hard`, `rank`, `direct`,
and `split` instructions. It is verified by the unchanged
`PortfolioCache.verify`. The ADD may determine a variable order, show the
producer that the requested bound is true, or guide which branches to inspect.
Every exported leaf must nevertheless satisfy the existing receiver's own
condition. When an ADD path ends at a terminal but that condition remains
unproved, the exporter must refine the remaining box, find an allowed symbolic
multiplier, or fail. Full assignment leaves provide the finite fallback when
the requested bound is valid and all inherited caps are met.

This is a real bridge into the old proof language. Its possible expansion is
a property of that language and its checking rules. It is not a lower bound
against ordinary shared proofs, alternative valid symbolic witnesses, or a
different receiver format. No ordinary shortcut or shared portfolio routine
will be prohibited to manufacture a comparison advantage.

## Shared DAG alternative

A second delivery format keeps shared nodes and Apply facts. Its bad-set root
represents:

```math
\mathrm{Bad}(x)
=\Bigl(\bigwedge_h h(x)\Bigr)
\land [r(x)\le\tau]\land[d(x)>B].
```

The receiver verifies that this root is the zero terminal after independently
binding it to the current frame, bound, and witness. Merely finding a zero
terminal in an imported graph is insufficient.

The proposed immutable evidence object has an exact JSON representation with
version, source record, epoch, input count/order, base admission counts,
topological node records, Apply claims, expression-root bindings, current
record, incumbent, requested bound, and the four roots. Node records are exact
rational terminals or ordered decisions. An Apply claim names its operation,
two operands, and result. A compiled-expression claim names the exact canonical
expression and its root. The final wire schema is being coordinated with the
independent receiver owner before hardening.

The independent checker must establish all of the following:

1. Every node has legal exact types, bounded components, older child references,
   and increasing variable levels. Zero/one values and Boolean node types are
   derived, not accepted from a producer's Boolean flag.
2. Every Apply claim follows from exact terminal arithmetic, a sound explicitly
   checked identity/controlling-value rule, or its two Shannon-cofactor claims.
   Child proof facts must already be admitted. The result must have the asserted
   children or the justified equal-child reduction.
3. Every expression binding follows from the original expression grammar and
   already checked child bindings/Apply facts. A producer-supplied root cannot
   replace a missing compile justification.
4. The current hard conjunction, every soft weight, the selected difference,
   incumbent rank cutoff, and requested bound appear in the final guard/bad
   construction. The receiver independently checks the incumbent's feasibility.
5. The imported current record equals the independently supplied full record,
   the declared source/order/epoch contract matches, and the verified bad root
   is identically zero.

These local rules allow sharing in both construction and checking. Resource
statements must depend on the actual constructed/visited Apply states and
exported facts, not just final root size. A tiny zero root can follow large
intermediate diagrams or costly rational operations.

### Cold and resident delivery

Cold delivery contains the complete proof closure needed by a new receiver.
Resident delivery can reference unconditional node, expression, and Apply
facts admitted earlier by that same receiver. A delta has explicit base counts
and a fixed source record, variable order, and epoch. The current frame,
incumbent and bound are rebound and checked for every request.

A caller-authorized epoch reset discards old authority; evidence cannot reset
its own receiving epoch. Persisted JSON or a digest does not recreate admitted
state without checking the chain. Semantics of retained diagram functions are
independent of whether an earlier scoped loss warrant still applies, which is
why changed hard rows and ranks can reuse functions while requiring fresh
current-request conclusions.

Both methods receive the same permission to retain verified evidence. Charging
a fresh ordinary admission on every request while granting the portfolio a
free resident cache would change the requested service.

## Work and bytes to account for

The parent owns the common tariff, outer budget, and comparison runner. The
producer/checker should expose actual work vectors and storage/transfer sizes
for these categories, with setup and current-request costs kept observable:

| Phase | Necessary work and retained state |
| --- | --- |
| Input and setup | Full source closure procurement; request validation and serialization; witness acquisition if not commonly supplied; exact record comparison; source/order/epoch enrollment. |
| Initial and edited construction | Expression visits/validation; Apply calls, hits and misses; unique-table operations; exact rational operations and component sizes; guard/rank/loss assembly; any producer-only extrema/search. |
| Proof export | Closure selection and graph traversal; dependency lookup; node/Apply/expression record production; copying and canonical serialization; legacy path unfolding and symbolic multiplier search. |
| Delivery and checking | Actual wire bytes sent/read; JSON and grammar validation; reference/order checks; exact terminal arithmetic; Shannon/shortcut checks; current request and witness checks; root binding; full or incremental admission. |
| Retention and cleanup | Producer nodes and every cache, including key material; receiver admitted nodes/facts/keys; proof/receipt bytes retained; evictions/reset work and dependent authority invalidation. |
| Output | Current certified conclusion and its bound, full record binding, status, and actual output bytes; failure/timeout reporting and its incurred invoice. |

Raw operation counts and rational sizes should remain available even when a
declared common tariff produces scalar units. A dictionary lookup is not a
physical unit of arbitrary-precision arithmetic. Retained serialized bytes are
not automatically total Python heap size; report the exact accounting scope.
Producer-only timings do not settle the end-to-end comparison.

## Allowed controls and first implementation step

The ordinary controller may use exact recomputation, a fully checked finite
table, constant shortcuts, warm ADD functions, earlier checked proof facts,
the same portfolio procedure, and any valid legacy symbolic witness. In
particular, sharing the same evidence kernel preserves an ordinary equality
control. Cold ADD and fresh tree production are ablations, not the strongest
ordinary comparator by definition.

The first end-to-end implementation should use one constant/nonempty frame and
one changed current record. It should establish a cold proof and resident
delta accepted by the independently implemented receiver, then check a wrong
root, changed bound, stale frame, missing hypothesis, and epoch mismatch. This
initial focused check does not establish the later comparison family or budget;
the parent will declare those separately. Before any run is published, preserve
the actual producer version and source closure. Corrections retain the earlier
version and failures.

## Source binding

The accompanying `initial_sources.json` records the selection, forecast, style,
Option B advice, and six current implementation/derivation inputs. The main
interfaces read for this design have these SHA-256 hashes:

| Source | SHA-256 |
| --- | --- |
| `05_ordinary_add.py` | `9263992673a815b15b489272aa827ea27066a0af264a85bbf905875f632abef7` |
| `05_counterfactual_transport.py` | `48422eb4b23ab38d2b755de76000edaa38231dce6064c2f9cb71e45702c9ae35` |
| `05_portfolio_transport.py` | `9bf64849eae1072c9da6a2e754858af6f2f15c2c4f7e7ac55ffb556f2064b821` |
| `04_counterfactual_repair.py` | `c71692e2e84c52f915dd1d09048344bf1d6c53e7d0362fe82a598d8f3d0ab896` |
| `05_resource_comparison_check.py` | `3865f82aa6d8c75949aba6af0963160b8b18093bbc05e531443c754a61f68ac8` |
| `05_resource_comparison.md` | `cbb69a5aefcd62a83ee45dfc3bd3b95eec747a8c41f044670a866ec6c3980028` |

No substantive implementation or experiment preceded this initial design.
