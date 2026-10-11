# Independent service audit: v2 diagnostics and v5 resolution

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
Same-model, nonblind DEVELOPMENT review; zero principal-clock credit. This
reviewer wrote the separate ADD receiver and independently reviewed the
parent-owned orchestration and tariff. This is not independent verification
of every component by an unrelated implementation team.

## Disposition and exact sources

**No unresolved blocker was found for the declared finite v5 service.** Five
new enrollment-only diagnostic groups passed. They confirm prepaid source
capacity survives budget and validation failures, with a funded terminal
response and no successful enrollment. They do not execute certificate
deliveries or establish a comparative performance result. The scope and
accounting qualifications below are part of this disposition.

The [captured v5 service](source/v3/checks/05_certificate_delivery_service.py)
is 36,584 bytes, SHA-256
`b96cae82e0fe3f0f734671d57df81ac3a62350746f73228aef63c2f77bb1745f`.
The [manifest](source_manifest.json) records fifteen unchanged files: eight
worker files, the initial contract, four amendments, the plan and diagnostic.
Its SHA-256 is
`e3079edfa9b0564cbb985f0ccd2a414f05a577b6869ab0301ecb6bff46c601e0`.
Only the eight worker files enter the service's program-byte enrollment; the
review plan, diagnostic and contracts are observer evidence.

The [new results](run/results.json), SHA-256
`beda347c24283be71388bcf91398c265b040ca3dff3a205d01af6f6bb111c1a7`,
bind the executed diagnostic, exact runtime, all before/after source hashes
and each complete invoice. All fifteen source files remained unchanged. The
diagnostic source SHA-256 is
`6ddde2ae7803922655fbbbc79aea07519f8bd9fa0cd12d6f85b584258ea16955`.

| Revision | Evidence and permitted attribution |
| --- | --- |
| Initially read v1, `18d326e8…` | Static first reading while the parent was revising live-state accounting. No exact v1 snapshot is claimed by this review. |
| Captured v2, `b8929dc8…` | [Ten meter/boundary groups](../service_audit_v1/run/results.json) and a separate [postpaid-source defect reproduction](../service_audit_v1/source_fee_run_v1/results.json). All executions used this saved revision. |
| v4, `e1b037b5…` | Static inspection of native witness/bound binding, complete old inputs, disposal and the ordinary interval screen. The parent's preserved smoke has its own source and results; its executions are not credited here. |
| Captured v5, `b96cae82…` | Static review plus the five new enrollment groups reported here. The parent owns every primary-method execution. |

The original declarations and [amendments](source/v3/work_logs/R_P3_B_B_2026-10-10_S1/development/service_contract_amendment_4.json)
remain separate source-bound evidence. No earlier result is retrospectively
assigned to v5, and no prior artifact was repaired in place.

## Resolved defects

The v2 native wrapper checked the proof's incumbent but could advertise a
different supplied incumbent of equal rank. The saved one-bit diagnostic had
hard constraint `p`, a feasible proof witness `(1,)`, and an infeasible supplied
witness `(0,)`, both of rank zero. The actual receiving inequality remained
true; the defect was the advertised supplied-feasible-incumbent service. The
v5 `native_receipt` requires the received witness and exact rational bound to
equal the separately supplied request. `common_report` also directly checks
that supplied witness against every current hard constraint. These changes
were already present before the parent's v4 smoke.

The v2 old-input byte bill contained only the full Frame record. The focused
one-bit record was 251 bytes, while its complete request packet, including
witness, bound and request identity, was 387 bytes: an omitted **136 bytes**
under that encoding. V5 serializes, charges and decodes the complete old
packet at both endpoints, retains the complete old input specification, and
includes the current old request and proof packet in the additional bootstrap
live-state snapshot. V4 already corrected input transmission; v5 makes the
bootstrap snapshot convention literal.

The separate v2 source diagnostic completed all 194,270 source-byte reads and
hashes before its explicit hash-input byte bill was denied. The paid hash-byte
category was zero. That expected defect remains recorded at SHA-256
`8254ccf63182d30fb903b4e12a7f9b7f0aa306e7cf0f3f841bb0b77785bac440`.
V5 instead validates the externally supplied canonical manifest and exact
worker-path set, then prepays each file's declared program bytes, hash
capacity and one length-probe byte before opening it. It reads at most the
declared length plus one, rejects a length mismatch, and hashes only an
exact-length result. A failed or denied attempt retains previously paid
capacity. Those fees are not an assertion that every prepaid byte was actually
read or hashed.

## New source-enrollment probes

The exact worker closure has eight files totalling 197,956 bytes. Its canonical
source record occupies 1,199 ASCII bytes. The successful fee reconstruction
is program capacity 197,956, hash capacity 197,956, eight length-probe bytes
and 1,199 source-record input bytes, plus the actual observed worker events.
The small diagnostics below call only `_enroll` through the unmodified meter.
They do not patch file access, hashing, tracing or worker source.

| Probe | Program capacity | Hash capacity | Probe bytes | Total units | Outcome |
| --- | ---: | ---: | ---: | ---: | --- |
| Exact source, ample account | 197,956 | 197,956 | 8 | 431,014 | Enrolled |
| Account 396,935 | 173,404 | 173,404 | 7 | 381,306 | Denied before the last file's 24,552-byte program fee; no enrollment |
| First expected length one byte short | 22,822 | 22,822 | 1 | 75,654 | Length mismatch; no enrollment |
| First expected length one byte long | 22,824 | 22,824 | 1 | 75,658 | Length mismatch; no enrollment |
| Last expected hash changed | 197,956 | 197,956 | 8 | 431,122 | Hash mismatch; no enrollment |

Every failed group includes the same 113-unit failure response and retains its
paid work and capacity prefix. The low account is the prospectively declared
diagnostic rule `reserve + 2 * source_bytes - 1`. The mismatch groups change
only the independently supplied expected metadata; the actual worker files
remain unchanged. Both a shorter and longer declared first file pay their
declared capacities before rejection. The last-file hash case pays all prior
files and the current file's capacity before rejecting.

The evidence that reads and hashes follow prepayment is the captured source's
control flow, corroborated by exact invoices and rejection boundaries. No
unrecorded I/O trace or physical byte-time measurement is claimed. A missing
file would fail at the same already-prepaid `open` boundary; that consequence
is static analysis, not an additional executed probe.

## Event and byte accounting

The tariff is the exact named CPython 3.12.14 event model: each observed worker
`opcode` trace event and each bounded native `c_call` profile event costs one.
Nested `Meter.run` calls relabel the active stage and preserve tracing of the
outer worker. Only the meter's own exact code objects are excluded as
apparatus. The serialization callbacks still execute as priced worker code.
The outer call primes opcode tracing before invoking even a previously
unexecuted worker code object and restores the earlier trace/profile hooks.

The saved v2 meter diagnostics independently reconstructed a first-call
`RETURN_CONST` event, twelve outer plus one inner opcode events in a nested
example, and four opcodes plus one native call for `len`. The relevant meter
trace/profile logic is unchanged in the inspected v5 diff. V5's new execution
tests source enrollment; it does not silently repeat or reattribute those
earlier meter executions.

This model does not price every interpreter instruction, physical arithmetic
bit operation, heap allocation or wall-clock unit. Interpreter bootstrap,
the measuring apparatus, fixed module import and endpoint field binding have
the stated installation/governor convention. Bounded rational arithmetic,
hashing, equality and native calls are covered by the named observed events
and explicit input capacities, not an assertion of constant physical cost.
The finite grammar, rational, wire, node, receipt and source caps in the
captured dependencies remain necessary limitations. The raw legacy work
counters are separate diagnostics, not a substitute complete tariff.

Within `_execute`, query routing, request encoding, old bootstrap, producer
search, export, receiver decoding/checking, current report construction and
live-state serialization run under the meter. Source input is charged before
manifest parsing. Current requests are charged at each applicable endpoint;
each proof's output and receiver input bytes are both charged. The ordinary
direct receiver has no redundant proof producer. Its global interval screen
is a sound whole-cube upper bound; when that fails, charged exact enumeration
checks the requested incumbent sublevel.

The complete worker bundle is a declared common installation convention. It
includes capabilities that a separately minimized ordinary deployment could
omit. Likewise, the common wrapper retains small endpoint metadata. Report
the actual total and consumer components, and do not call these the minimum
possible ordinary costs. Consumer units are exactly the declared stage subset:
`receiver_*`, `terminal`, `failure_terminal` and `common_source`; other charged
coordination/producer stages remain in the total bill.

## Receiver authority, live state and publication

The native codec rejects duplicate or unknown object fields, inexact JSON
numbers and out-of-cap input. Full Frame records are independently bound and
reconstructed canonically. Native proof validity still comes from the actual
old `PortfolioCache.verify`, now with explicit supplied witness/bound binding.
The independently coded DAG receiver checks unconditional nodes, Apply facts
and expression bindings; each current request reconstructs its own guard,
rank and bad-set obligation. Source, current record, order, epoch and delta
base must agree with caller-owned state. Neither a root ID nor an arbitrary
report creates authority.

Source admission checks the sealed files on disk against the independently
provided complete expected record. The owned process must have loaded that
same closure and keep it fixed. This is not protection against mutation of
`sys.modules`, private Python state or files after enrollment. The source
record itself is not a remotely authenticated identity. A fresh process and
before/after closure preservation support the actual source-bound runs.

The common receiving obligation is the entire current feasible incumbent
sublevel, including every tied minimizer, for the fixed supplied receiving
loss, unit, bound and feasible witness. It does not enumerate optimum
identities. Old conditional domains can be reused only through checked
current maps and cover obligations. The ordinary hybrid obtains its old
domains through the independent ADD receiver and then uses the same native
portfolio receiving kernel. Empty old domains do not establish a nonempty
current request by themselves.

The declared storage unit is one serialized live-state period at successful
old-domain admission and current delivery, **before disposal**. It includes
the applicable manager tables/logs, independently checked receiver state,
portfolio domains, current request and evidence packets, and current receipt.
V5 also includes current bootstrap request/packet copies. This is a named
serialized-state proxy, not a heap peak or elapsed byte-time estimate.

Cold ADD's manager and checked graph are charged while needed, then discarded.
Warm resident ADD retains checked immutable chunks and advances only from the
acknowledged cursor. A fresh recipient receives a full proof and begins with
empty verified facts, although source/interpreter installation is shared.
Resident portfolio endpoints discard old replay packets after successful
delivery; fresh recipients retain and recheck them. Post-disposal sizes are
observer-only diagnostics, with no second paid period at the same boundary
and no fictitious period after the last request.

Current graph admission occurs on a fork. The parent wrapper publishes a
receiver only after validation, full live serialization, output bytes and
delivery/publication events are paid and the outer worker returns. Denial
after an internal graph commit discards that candidate. Every new attempt
withdraws the previous current payload under a new caller-owned identity.
The failure policy conservatively clears producer and verified recipient
caches; it does not claim preservation of an uncharged old receiver. A later
attempt rebuilds as required, while a previously completed source installation
may remain enrolled.

## Reserved failure and threshold interpretation

Accounts below 1,024 units are rejected externally before an admitted paid
attempt. Every nonfailure charge protects that reserve in both applicable
accounts. The failure terminal uses the 111-byte fixed payload, one delivery
event and one eviction event:

```math
111+1+1=113<1024.
```

Consequently any admitted denial reached through the guarded worker leaves
enough capacity for this declared failure response, preserving its paid
prefix. This is a failure-response argument, not an all-path success bound
for arbitrary fixture inputs or an unrestricted Python API.

The published threshold fields test observed consumer bill $`u\le T`$.
They are descriptive affordability statistics. For the same deterministic
successful path to execute with this reserve, its consumer account instead
needs $`u+1024\le T`$; the analogous total-account condition also applies.
Actual low-budget executions must remain separately labelled. The v2 meter
diagnostic exhibited this distinction, and amendment four states it directly.

## Reproduction and stopping point

Run from the repository root with the pinned CPython 3.12.14 runtime. Choose
a fresh output directory; the diagnostic refuses to overwrite its run.

```bash
python v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/service_audit_v5/source/v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/service_audit_v5/enrollment_probe_v5.py \
  --source-root v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/service_audit_v5/source \
  --manifest v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/service_audit_v5/source_manifest.json \
  --out /tmp/rp3bb_service_v5_enrollment_reproduction
```

There were five enrollment groups, zero `Session.deliver` calls, zero policy
runs, no worker edits and no research-clock credit. The focused Markdown
source guard is recorded separately; no live renderer or global historical
style pass is claimed. No further experiment is needed for this bounded
review. Comparative claims belong to the parent's separately sealed complete
service runs and must retain their finite horizons, setup costs and ordinary
controls.
