# Prospective structural certificate transfer design

Contributor: ChatGPT (GPT-6 Astra Pro), October 11, 2026 UTC.
Task: P3-09 preparation only. Principal-clock credit: zero.

## Recommendation and current implementation

Use the accepted Option B current-incumbent-sublevel certificate service for
the secondary structural comparison. Keep P3-08's full repair/action service
as a separately labeled regression endpoint. The two interfaces answer
different questions and use different tariffs. A certificate over a supplied
incumbent's sublevel does not itself compute every minimum repair or choose an
action across unresolved source cases.

The new adapter is
[p309_certificates.py](../../../../experiments/p309_certificates.py).
Its first source-bound development snapshot has SHA-256
`218cbde22309d3ec25c47611a2954fb19cdb68faf7680980f4b5b677c6c4eabc`.
The [complete eleven-file manifest](development_smoke_v1/source_manifest.json)
binds 257,523 application source bytes. Its SHA-256 is
`b421739001b4af7d0103d44f353dc9af7d2a0fb6fddc6bd5cb8a0d8fd5571a46`.
The earlier [inspection manifest](source_manifest.json) preserves the original
source, protocol, scope and development-evidence inputs to this design review.
No old worker, report, source snapshot, failed record or ledger was changed.

## Exact receiving obligation

Let the current public Frame give hard formulas, positive one-tier normality
weights, an exact rational difference, a full interpretation/scope record, a
complete feasible incumbent and a requested bound. The common obligation is:

```math
G_w=\left\{x:H(x)=1,\quad r(x)\le r(w)\right\},
\qquad w\in G_w,
\qquad \forall x\in G_w:\ D(x)\le B.
```

Every successful terminal receipt binds the complete current Frame record,
exact incumbent, exact cutoff and bound, loss unit, current request identifier
and full installed-source record. Coverage includes all current minimizers and
all other points below the supplied incumbent's cutoff. A nonoptimal incumbent
therefore creates a stronger requirement than checking only the minima.

The supplied incumbent must be feasible. An empty hard domain is not admitted
by inventing an arbitrary incumbent or by treating a vacuous bound as useful
current evidence. A missing old catalogue is allowed: fresh native proof and
direct ordinary checking can construct current evidence without old warrants.
An empty or insufficient reuse cover must use checked direct leaves or fail.
All tied current minima remain inside the bound's domain; there is no tie
selection shortcut. These obligations follow the unchanged
[service](../../../../checks/05_certificate_delivery_service.py),
[portfolio checker](../../../../checks/05_portfolio_transport.py),
[checked ADD receiver](../../../../checks/05_add_evidence_check.py) and
[independent scalar reference](../../../../checks/05_certificate_delivery_cases.py).

The native receiver checks its strict tree wire, current bindings, feasible
incumbent and every local proof obligation against admitted old domains. The
ADD receiver independently validates nodes, rational arithmetic, Apply facts,
expression bindings and a reconstructed current bad-set root. Shared facts are
unconditional expression denotations; old guard-scoped bounds do not become
unconditional Apply facts after an edit. Source authentication belongs to the
outer prepaid source enrollment, not to a hash string inside an untrusted
packet. Both receivers retain trusted caller-owned process state, not a
hostile-code security boundary.

## Two prospective structural constructions

The generator is deterministic. It accepts only the exact `P3-10-EXPOSED`
token before constructing any expression or Frame. Import, `default_config`,
`groups` and `units` create only source/configuration/schedule metadata.
No final group formula, case, witness, private truth or outcome was generated
in this review or its development check.

### Majority factorization

On each disjoint triple, compare the majority formula in disjunctive form with
its conjunctive form:

```math
U=(a\land b)\lor(a\land c)\lor(b\land c),
\qquad
V=(a\lor b)\land(a\lor c)\land(b\lor c).
```

The four-bit recipe uses one triple and one independent free coordinate. The
seven-bit recipe conjoins two disjoint triple identities and includes the free
coordinate. These change factorization and shared subfunction structure from
the published parity/cancellation streams; a variable rename or a new random
seed would not make this construction.

### Selector multiplexer and disjoint arithmetic sum

A nested Boolean multiplexer is compared with the arithmetic sum of its
mutually exclusive guarded data leaves. The four-bit recipe has one address
bit, two data bits and one independent free coordinate. The seven-bit recipe
has two address bits, four data bits and that free coordinate. Each guarded
leaf is an admitted Boolean conjunction. Addition combines the disjoint
leaves, so no nonconstant multiplication operation is silently added to the
inherited grammar. The two sides have the same Boolean denotation even though
the sum retains its numeric expression type.

Both constructions use a free bit absent from hard and normality formulas:

```math
D=2z-1+(U-V)+c,
\qquad U=V,
\qquad B=1+c.
```

Thus the actual difference is nonconstant in the free bit. The two supplied
old domains fix that bit to zero and one, respectively, with old bounds minus
one and one. Their production and admission are paid. Both old domains are
needed to cover the current domain using only these identity-mapped old
lemmas. This is a restricted reuse-cover statement: ordinary direct checking
and direct proof leaves remain allowed. The generator's identity is not
passed to any method as an unpriced oracle or an admitted proof.

### Four edit slots

| Slot | Current change | Receiving obligation retained |
| --- | --- | --- |
| 1 | Initial unrestricted hard/rank domain | Nonempty full domain and every tied minimum |
| 2 | A hard disjunction and a one-row normality preference | Feasible supplied incumbent and both free-bit values |
| 3 | A feasible incumbent that violates the normality preference | Full larger incumbent sublevel, including points above the minimum |
| 4 | Repriced normality weight, known half-unit loss shift, and a new complete scope/version record | Rechecked current cutoff, bound, loss and full scope |

The fourth slot changes the full current problem record. It does not mutate
the frozen program source or claim that changing a display name invalidates a
mathematically reusable conditional lemma. Every new request withdraws the
previous terminal receipt as current authority. Resident expression facts may
be reused only through the unchanged source/order/epoch and current-goal
checks. A real program-source amendment would require a new source binding
and the parent lifecycle's explicit exposure disposition.

## Complete comparator catalogue and denominator

| Method | Classification | Fresh recipient | Resident recipient |
| --- | --- | --- | --- |
| `P-REUSE` | Candidate native portfolio reuse | Included | Included |
| `P-FRESH` | Ordinary fresh native-proof control | Included | Included |
| `O-ADD-COLD` | Ordinary fresh ADD construction | Included | Included; cold ADD still uses a fresh checker |
| `O-ADD-WARM` | Ordinary retained ADD construction | Full checked export | Owned checked delta state |
| `O-ENUM-RECEIVER` | Ordinary interval screen followed, when needed, by exhaustive current-domain checking | Included | Included |
| `O-ADD-PORTFOLIO` | Ordinary ADD construction of old domains, then native portfolio transport | Included | Included |
| `O-ADD-WARM-PRUNED` | Ordinary warm ADD with paid current full-proof pruning | Included | Ineligible; no resident pruning service was supplied |

Only `P-REUSE` receives `method_kind='candidate'`. Native proof syntax is
available to the ordinary fresh control. Enumeration remains eligible even
when it is expensive, and its sound global interval shortcut remains enabled.
The pruned control pays initial full export, closure computation, remapping,
its retained full producer state and fresh complete receiver admission. No
claim of minimum ordinary program size, optimal pruning or a generic optimal
compiler follows from this finite catalogue.

There are four complete streams, seven fresh configurations and six resident
configurations, each under two separately executed accounts and four edit
slots. That is 104 whole-history units and 416 delivery attempts. These are
not 416 independent trials. Matched descriptive comparisons occur within the
same stream, recipient condition and actual budget condition; the parent
analysis additionally combines the two prespecified size strata within each
family. Ties, differing covered-request sets, invalid delivery and unknown
costs are retained explicitly. No source-plurality learning or universal Q3
advantage is inferred from a finite resource ranking.

## Accounts, failed paths and retained state

The `full` condition supplies total budget 134,217,728 per delivery without an
independent consumer cap. The `capped` condition supplies the same total
account plus consumer cap 1,048,576. The label `full` is not an all-path success
bound. The consumer cap was fixed from the previous development engineering
regime before these new populations existed; no new pilot population was
generated to choose it.

The published prior [cap-history extraction](prior_cap_history.json) records
why actual execution matters. At the same consumer cap, native reuse and the
hybrid delivered 32 of 48 requests despite 37 retrospective full-path bills
fitting the displayed threshold; warm ADD delivered 43 despite 41 such
retrospective fits. A paid failure can evict state, change later bootstrap
requirements and change later bills. The adapter consequently allocates a new
owner for every method/recipient/budget history and continues its fixed four
edit slots after every callback-returned resource or validation failure. It
does not simulate cap histories by thresholding uncapped bills.

The application closure is the six core grammar/transport/portfolio/ADD files,
the v5 service and independent reference, the pruner and pruned service, and
the new adapter. Every method pays the same full eleven-file installation.
The independent reference is not called in `run`; its historical inclusion in
the shared installed service does not supply unpriced truth. Source bytes,
hash capacity and sentinel length checks are prepaid before each bounded
source read. Previously spent source enrollment survives a failure invoice;
prepaid capacity remains billed even if the subsequent read fails.

Current JSON-to-Frame conversion runs in the new paid
`request_materialization` stage. Old input conversion runs in
`producer_old_materialization` only for methods retaining old recipes.
Conversion replaces the whole old-input tuple atomically. The producer-state
serializer supports both raw caller records and fully materialized Frames,
including after denial before old proof construction. Raw input is not an
admitted warrant. Unused old recipes are not retained by the direct, fresh or
plain ADD controls.

The unchanged worker pays proof search, checking, current and old wire bytes,
full serialized live-state periods and terminal output before publication.
The cold/fresh disposal convention remains the v5 convention: charge actual
live producer/receiver state at delivery, then dispose of the declared cold
state. Post-disposal sizes are observer-only diagnostics. On failure the owner
evicts scientific caches, emits the protected 111-byte receipt plus two
ownership events, and retains the 113-unit terminal bill and all paid work
before it. No current certificate is published on that path.

The tariff is exactly the inherited CPython 3.12.14 observed worker `opcode`
trace events, bounded native-call profile events and declared serialized byte
periods. Interpreter bootstrap/frame bookkeeping, instrumentation and archive
writing are outside this operational event model. The model does not price
physical CPU time, allocator work, whole-process peak heap or elapsed
byte-time. It is separate from `STRUCTURAL-VM-v1`; no cross-tariff total is
defined. Fixed module/class endpoint binding belongs to source installation;
all input-dependent decoding and worker orchestration is traced.

## Arithmetic and Q2/Q5 limits

These prospective recipes use small fixed coefficients, one rank tier and at
most seven bits. Their inputs stay inside the shared grammar and arithmetic
fragment. Direct constructor counting gives fewer than 64 expanded expression
nodes and depth below 12 for either largest shifted difference; the hard row
has three nodes and the only soft row is a coordinate. This is a static size
bound on the fixed grammar recipes, not an executed final fixture check.
The inherited caps remain unchanged: 128-bit input components,
128-bit native context/cutoff components, 16,384-bit old ADD terminals,
4,096-bit checked ADD terminals, 2,047 native proof-tree nodes and the checked
ADD's finite wire/state/history caps.

Those arithmetic domains are not nested. The source-bound prior reciprocal
sum witness has a 7,914-bit reduced denominator and is outside the checked
ADD wire while remaining within the older ADD cap. Conversely, two admitted
128-bit soft weights can produce a 254-bit cutoff that direct checked ADD and
enumeration accept but the native cutoff interface rejects. Increasing a
resource account does not remove either fixed representation cap. The
published rational retry and retained integrity discrepancy remain historical
evidence; these final structural recipes do not purport to cover that larger
union of fragments. See the preserved
[equal-delivery derivation](source/v3/derivations/05_equal_certificate_delivery.md)
and [retry summary](source/v3/work_logs/R_P3_B_B_2026-10-10_S1/development/rational_service_v1_retry1/summary.json).

P3-08's paired-support compiler preserves a classically inconsistent quoted
formula under its fixed interpretation; it returns all optimal repairs per
external source and chooses one receiving action across every source and
every tied optimum. Its resource-failure guarantee is restricted to nine
published fixtures, its fixed routing table and CPython 3.12.14. Its paired
normality example uses multiple tiers, while this certificate Frame admits
one. Applying `run_method` unchanged to arbitrary new final cases, or silently
flattening those tiers, would overstate the accepted contract. The original
full repair and genuine counterpossible obligations therefore remain the
separate P3-09 conformance/regression arm's responsibility.

Q5's finite exact information audit and verifier can provide source-bound
identifiability, witness-law and additional-query conformance checks. They do
not establish that supplied inputs are true expected losses, discover an
agent's beliefs, price information acquisition, or prove an end-to-end
learning/action theorem. The same mathematical audit is available to ordinary
methods. This certificate adapter supplies no replacement Q5 semantics.

## Development evidence and remaining gates

The first [development selfcheck](development_smoke_v1/results.json) passed
13 method/recipient histories, each with a valid constant bound, a false bound,
recovery and another valid bound. Its separate two-bit toy has two tied
minimizers and four points in the deliberately nonoptimal incumbent sublevel.
The additional success/reserve-only-failure/recovery probe passed; the failure
cost 113 units and no stale receipt was current. Total: 55 development delivery
attempts. These are API checks, not new transfer results or final evidence.

The results SHA-256 is
`819dce1ed0e4f44f43a062ae683c1a4f56e2263bc567b951e839692e3eaf5c0c`.
The [receipt](development_smoke_v1/receipt.json) confirms all eleven captured
source files remained unchanged. A subsequent
[observer-only check](development_smoke_v1/observer_boundary_v1/results.json)
changed a successful toy receipt's bound and malformed its terminal JSON.
Both became completed private-score failures, excluded the invalid request
from delivered coverage, and retained all 2,105,829 paid units from that
history. No method ran in that observer check. Its result SHA-256 is
`ca7ee88d3c54bcd9da515b989979b31c9b4ba6581df1c5b0e59047f6f2d4c1d8`.

Root still owns independent source review, the complete prospective freeze,
the final-population exposure decision, unit seals, aggregate analysis and
publication. P3-09 stops before final generation and execution. These toy
checks create no permission to proceed to P3-10.

## Additive prospective v1.1 scorer correction

Before the parent freeze, an exact-type review found that v1's Python terminal
dictionary comparison could equate boolean witness entries with integer zero
or one. The worker's strict input/checking service already excludes those
entries, so the 55 honest v1 development attempts remain valid. A separately
preserved forged-receipt observer test reproduced the weaker independent
score gate. The [prospective amendment](scorer_v1_1_amendment.md) records the
issue and its disposition without changing any v1 source or outcome.

The current `p309-certificates-v1.1` adapter has SHA-256
`14db182d5ace8f8670cd298c3dad456e54e72a3e1ecdbfe36d5238fca6f1126c`.
Its [eleven-file source manifest](scorer_v1_1/source_manifest.json), SHA-256
`5190f98dc88b094ec8df1116cfbab2b4e8af1ee2c3db8112727483a7917ff327`,
binds 257,549 source bytes. Canonical JSON comparison now distinguishes the
exact terminal types. Recipes, methods, caps and resource governor remain the
same; the new source and adapter-version bytes must be charged on new runs.

The [focused v1.1 observer result](scorer_v1_1/results.json), SHA-256
`477909709d3661c49bc177f2df728ee9cf1bbe0485c65b9021c1595b11c06d7c`,
rejects the boolean witness, wrong bound and malformed terminal JSON as
completed invalid scores. It retains the old history's 2,105,829 paid units
and excludes each invalid request from delivered coverage. This check makes
no new paid-worker performance claim: it re-audits preserved old receipts,
and zero workers or final recipes ran. The source-bound v1.1 receipt confirms
unchanged files. The parent frozen-source development gate remains required
before final freeze completion.
