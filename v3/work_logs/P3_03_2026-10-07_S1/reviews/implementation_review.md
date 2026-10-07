# P3-03 internal review — executable bounded kernel

Contributor: **ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction
reviewer**. October 7, 2026 UTC. Same-model, nonblind review; zero additional
concurrent time credit.

## 1. Scope and evidence binding

This review statically inspects
[the implemented kernel](../../../checks/03_bounded_logic.py), following the
[mathematical reconstruction](bounded_reconstruction.md). It distinguishes
actual APIs from broader mathematical extensions. The reviewed revision was
observed at `2026-10-07T15:36:35.103131+00:00`:

| Field | Recorded value |
|---|---|
| File | `v3/checks/03_bounded_logic.py` |
| Bytes | 30,011 |
| SHA-256 | `c6dae8bfddcb748c15d3d50bc812ce01c7c7c7ec858b4b3b050ca30b0b1aa386` |
| Static syntax checks | `ast.parse` and `compile(..., 'exec', dont_inherit=True)` succeeded. |
| Module imported or executed by this reviewer | **No.** |
| Scientific cases run by this reviewer | **None.** Root was preparing the prospective development plan and independent harness. |

An earlier draft was inspected first and concrete findings were sent to the
principal before its scientific executions. The revised source above was then
read again. The finding table records repairs visible in those reviewed bytes;
it does not pretend the original draft already included them. Syntax success
is an administrative check and supplies no experimental correctness evidence.

## 2. What is actually implemented

The kernel holds at most twelve active Boolean coordinates in a fixed query
list. It implements two query types: opaque statement records with no executable
producer, and bounded runs of a small natural-number register machine. The
machine instructions are `INC`, `DECJZ`, `JUMP`, and Boolean `HALT`; programs,
initial register magnitudes, register count, and the proposition's execution
horizon have declared finite caps. Query IDs and versions are retained in the
original input and receipt binding.

The source uses cubes, an explicit processing agenda, Strong-Kleene checks of
finite Boolean expressions, and a configurable committed-cell cap. Its losses
use exact rational literals, variables, fixed rational scaling, addition,
minimum, maximum, and positive residual. Reports contain conditional outer
bounds, source filtering and feasibility status, checked coordinate answers,
producer/checker process status, and resource diagnostics. There is no point
probability default.

External Boolean constraints are accepted only as explicitly labeled
`conditional_assumption` records. Callers cannot submit a hard checked fact
through that API or use the reserved `vm:` evidence namespace. Actual checked
VM literals are generated only after the kernel's producer/checker process.
The `depends_on` field supports conservative withdrawal closure; it is not a
general proof language or a certificate validating the conditional premise.

## 3. Static soundness assessment

### Cover transitions and budget boundaries

The initial all-star cube covers every finite assignment. A source transaction
removes a cube only after one active Boolean constraint evaluates false over
that whole cube. A split prepares both children and then replaces the parent.
At a capacity stop, the parent remains in the source and is requeued. These
operations preserve the mathematical outer-cover invariant.

The implementation's interruption guarantee is **between completed
transactions or calls**. It explicitly excludes a Python process crash inside
a transaction. Temporary split workspace includes the old parent and both
children; the committed frontier still respects its configured cap. Neither
the code nor this review supplies a durable transactional restore mechanism.

The interval evaluator has the needed sign reversal for negative rational
scales. Its addition, min/max, and residual operations enclose all concrete
values and are inclusion-isotone. On a singleton every admitted operation has
an exact mathematical endpoint. A numerical report remains conditional on
successful bounded arithmetic: expression admission alone does not guarantee
that every intermediate rational calculation fits its separate bit cap.

### Producer and replay checker

Producing a candidate and checking it are separate phases. The checker starts
from the original query's initial machine state and replays its instructions.
No candidate answer becomes a `known` coordinate until replay has finished,
the original-query and VM-version checks pass, and the canonical candidate
equals the independently replayed terminal receipt. Using canonical JSON
comparison also prevents Python's Boolean/integer equality from accepting a
typed alteration such as integer one being replaced by Boolean true.

The internal execution horizon and the outer transaction allowance have
different roles. Exhausting the latter retains a partial job. Completing the
former determines whether the machine halted with the requested output
within that horizon. A zero horizon has no executed instruction and therefore
does not witness the requested termination. A halt instruction completed as
the final allowed instruction counts within the horizon. These are readings
of the code, not claims of executed test coverage.

Producer and checker deliberately share the same transition function. Replay
can detect a wrong or corrupted candidate; it is not an independent validation
of the transition function's operational semantics. The independent development
reference must check that separate bridge.

### Immediate uptake and conflict

Accepted checked literals immediately enter the active source and the report's
literal overlay. Thus they affect the next report before all old cubes have
been physically pruned. Conditional literal assumptions can also tighten a
conditional interval, but they do not receive `CHECKED_TRUE` or `CHECKED_FALSE`
truth status. This preserves the distinction between a premise and a checked
VM answer.

An empty effective frontier or a contradictory literal overlay yields
`FINITE_CONFLICT` and no numeric bound. A nonempty frontier without a checked
satisfying singleton yields unresolved feasibility. A witness is initially
available when there are no constraints, is cleared when constraints change,
and is subsequently set only after all active constraints accept a singleton.
That witness establishes finite Boolean-assessment feasibility; it is not a
complete model of arithmetic or a forecast of the actual answer vector.

The `source_exactly_filtered` flag requires an empty agenda and only singleton
cells. It is a claim about finite source processing. It must not be presented
as full-theory coherence or as a numeric success when a report instead returns
`ARITHMETIC_LIMIT`.

## 4. Findings and visible repairs

| ID | Initial finding and consequence | Disposition in the reviewed revision |
|---|---|---|
| IR01 | Original-input hash plus local epoch counters did not identify an active source. Two kernels from the same input could reach equal epochs with different premises and accept one another's conditional reports as current. | **Repaired statically.** Reports bind the canonical full active source, including query records, VM version and exact constraints. `report_is_current` checks this identity along with the original input, scope, kernel/VM versions, epochs and current loss. |
| IR02 | A short string such as `1e1000000000` could reach `Fraction` before the rational bit cap, requesting a huge power allocation. The reviewer did not execute that witness. | **Repaired statically.** A bounded integer or integer/positive-integer grammar with bounded digit counts is checked before constructing a fraction. Scientific notation is not admitted. |
| IR03 | Checking the encoded input byte cap only after canonical serialization left the admission procedure without a preceding traversal envelope. | **Repaired statically.** `admitted_data` checks container traversal, depth, scalar sizes and integer bits before JSON encoding/deepcopy. It explicitly does not account for how the caller originally constructed the object. |
| IR04 | A receipt blocked by full evidence capacity became permanently unscheduled even when later withdrawal freed a slot. | **Repaired statically.** Capacity-blocked jobs remain eligible. A subsequent scheduled checker transaction can revalidate and admit the candidate when space exists. |
| IR05 | Report coordinates collapsed pending, rejected and capacity-blocked computations into one unresolved status; failure reasons could disappear when `last_event` changed. | **Repaired statically.** Truth status remains unresolved when appropriate, while a separate process record retains the phase and persistent disposition. |
| IR06 | Capped source dimensions and rational calculations did not cap growing event IDs, scheduling counters or cumulative cost integers. A uniform CPU or fixed-total-RAM interpretation would be unsupported. | **Scope corrected.** The coarse transaction model is explicit, control operand bit lengths are exposed, and no fixed-total-memory or constant-CPU theorem is asserted. |
| IR07 | A report's embedded resource account preceded its own serialization charge, and snapshots had the analogous boundary. | **Label corrected.** Each object states where its resource snapshot ends; its current serialization charge is outside that embedded snapshot. |
| IR08 | `peak_cells` is first initialized by a source transaction, although the initial frontier already contains one cell. An initial or evidence-only report can therefore omit that peak. | **Minor accounting correction requested.** Initialize the committed-cell peak to one. This does not affect mathematical bounds. |

One wording correction was also requested: the input traversal docstring says
repeated/cyclic containers are rejected, while small repeated containers are
counted per occurrence and can be accepted. Cycles eventually exceed the
depth/node envelope. This discrepancy does not invalidate the accepted-input
soundness argument or require rejecting harmless repeated containers.

The source-identity check is an identity/current-warrant service, not
authentication of arbitrary externally fabricated report JSON. The code
states that limit explicitly. It can continue to recognize an older, looser
warrant after further cover refinement when the underlying source and loss
remain applicable; it does not claim that the older report is the latest or
tightest report.

## 5. Revision and reuse

Adding an assumption increases the source epoch, clears the old feasibility
witness and requeues every retained cube for the stronger source. This cannot
restore a previously pruned alternative, but none is needed for a mere
addition: the new compatible set is a subset of the old one.

Withdrawal computes the transitive dependency closure, removes those premises,
and rebuilds the frontier from a new all-star root. If a removed record was a
checked VM answer, its known coordinate is removed and its producer/checker
job is restarted. Unaffected checked answers remain supported. Rebuilding is
the implemented sound policy; retaining valid excluded branches and repairing
only affected exclusions is not implemented.

Changing a loss validates a new expression and unit/version record and advances
the objective epoch. Current-warrant checks bind the exact new loss. A report
is returned as a deep copy, so later source mutations do not edit the returned
historical object. Historical storage and a complete event journal remain the
caller's responsibility; the kernel stores only the latest event internally.

There is no public in-place query, program, checker or theory replacement API.
A changed semantic query requires a fresh configuration/kernel instance in
this prototype. The broader version-transport/reuse analysis is a mathematical
interface obligation, not an implemented arbitrary transport service.

## 6. Resource and capacity scope

The allowance is an upper bound on complete declared kernel transactions.
A report transaction can visit the entire bounded frontier and expression;
a source transaction can scan every current constraint; a withdrawal can
compute a finite dependency closure. These are intentionally heterogeneous
operations. Input admission, identity checks, serialization, allocation and
host execution do not become identical-cost CPU instructions because the
transaction counter increments once.

The input, program, cell, expression and rational caps supply a concrete finite
instance. Exact rational arithmetic checks a conservative result-size envelope
before its admitted multiplication/addition/subtraction. Register values can
grow beyond their initial input bit cap through `INC`, but their growth within
a bounded run is limited by the declared finite instruction horizon; there is
no unbounded multiplication instruction hidden in that VM.

A one-cell cap can stall splitting forever while preserving a sound outer
cover. Full evidence capacity can block acceptance until capacity becomes
available. A fixed syntactic loss can meet an arithmetic limit. Therefore the
unrestricted mathematical eventual-resolution or exactness statements require
their explicit service, capacity, retention and arithmetic assumptions. They
are not unconditional guarantees of every configuration admitted by the
finite prototype.

No value-of-computation policy, learning rate, universal proof-search fairness,
physical RAM cap, or superiority from heterogeneous transaction counts follows
from this implementation.

## 7. Priority development checks

The principal's saved prospective plan should include independent checks of
the implemented claims, especially the following cases. This reviewer has not
executed them.

1. Compare every covered finite assignment with an independently evaluated
   Boolean source and loss on small cases, including after each partial budget.
2. Test true, false and unresolved VM cases against an independent instruction
   interpretation; include zero horizon and termination at the last allowed
   instruction.
3. Preserve an unvisited branch through a budget stop and a cell-cap stop.
4. Verify that conditional literals can change conditional bounds without
   becoming checked semantic answers, while accepted VM literals update the
   next report even before full frontier pruning.
5. Exercise branch-divergent equal-epoch source reports, wrong-request receipts,
   and canonically distinct Boolean/integer receipt fields.
6. Withdraw a dependency root, preserve unrelated support, reopen the full
   unknown cube, and detect stale loss/source reports.
7. Reach evidence capacity, free a slot, and confirm scheduled retry; retain
   persistent failure/process status in ordinary reports.
8. Reject oversized/exponent-form rational literals at admission without
   constructing their implied giant integers. Distinguish arithmetic failure
   from a false or empty-source conclusion.

## 8. Present disposition

After the visible repairs, this static review finds no remaining mathematical
soundness blocker in the declared finite, conditional, transaction-boundary
scope. IR08 and the small traversal-docstring discrepancy remain identified
administrative corrections in the bound source revision. Executable correctness
still requires the separately planned development evidence.

This is an implementation review of the restricted VM/cube process. It does
not validate arbitrary arithmetic proof search, growing active-query APIs,
crash restoration, a learned prior, anticipatory logical induction, or a new
counterfactual method. Those are not silently imported from the mathematical
proposal or from the successful static syntax check.

## 9. Subsequent development revision

The executed attempt-1 kernel has SHA-256
`ae757bee58089b1229cdd2e123e4650be704f04729b2fff081238c988a916247`.
Static inspection confirms that it initializes the committed-cell peak to
one and corrects the repeated-container wording. **IR08 and the docstring
correction are therefore closed in that later revision.** The earlier source
binding and finding table remain as the historical record of what this review
actually inspected at that point.

The separately saved [harness review](harness_review.md) checks the current
method/evaluator hashes against the attempt's manifest and summary, explains
the independent evaluator scope, and assesses the twelve passing development
suites without rerunning them. That evidence supplements this static review;
it does not convert its finite tested scope into a universal implementation
proof.
