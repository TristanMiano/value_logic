# Independent review of the certificate-delivery synthesis

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
Same-model, nonblind, additive DEVELOPMENT review. **Zero principal-clock
credit.** No worker, policy, proof checker or root analyzer was executed. The
small readback programs only read captured Markdown and existing CSV/JSON.

**Disposition:** the primary and secondary numerical comparisons, receiving
service and fixed-invoice price conclusions are supported. One material
rational-run integrity discrepancy requires disposition, and three wording or
history corrections are recommended. Pending consumer-cap results are outside
this review.

The [captured synthesis](source/v3/experiments/certificate_delivery.md) is
SHA-256 `712d0c3c23c610b3e6fa495bcd0cc43309511e14383efba21e883e6c98832878`.
The [captured derivation](source/v3/derivations/05_equal_certificate_delivery.md)
is `fda0dd2a76a654bb235d2a885a2a9a0d879bf6858427d670a54f20729b062898`.
These are in-progress document snapshots, not a declaration that their live
originals will remain fixed. The known analysis-link typo was already repaired
before this capture.

## 1. Material evidence discrepancy

The observed `development/rational_service_v1/completed_units.jsonl` has
**29 complete records and 143,295 bytes**, with SHA-256
`df3e500eac31c649b9afa3fc285b3d5428ed157ced94e2a63c462ff6bc92f69f`.
Its final record is the ordinary hybrid's `zero_work_capacity` failure.
The existing summary instead declares thirty records, thirteen deliveries,
seventeen failures, 302 assertions, and completed-stream digest
`82f71da539ad3231764b54e9652635b5c4eded73805b8f2f08a81e6d521d28e4`.
The manifest itself still matches its declared digest.

The [integrity observation](rational_integrity_observation_v1.json) preserves
the actual stream and summary separately. Root independently observed the same
discrepancy and reported no known mutation or active rational process. This
review does not explain its cause or reconstruct the absent record.

All six records for each of the first four rational inputs are present. Their
format outcomes and six reserve-only failures at 113 units match the synthesis.
Five recovery deliveries are present; the ordinary hybrid's final recovery is
absent. The available stream therefore contains twelve deliveries and seventeen
failures. **The synthesis's complete thirty-unit and all-six-recoveries claim
cannot presently be corroborated from that stream.** Report the discrepancy
and resolve its lineage before treating the summary as a complete reproducible
run. The independent arithmetic arguments and the recorded first four input
groups are separate evidence; the missing recovery does not refute them.

The [three-run integrity readback](run_integrity_readback.json) found matching
row counts, completed-stream hashes and manifest hashes for primary v5
(317 records) and secondary pruning v1 (148 records). Their source-integrity
status is unaffected by this rational-run finding.

The first transcription reader stopped at its thirty-row assertion. Its initial
provisional diagnosis of a reader-schema error was incorrect: invoices are
top-level, and the source stream actually has twenty-nine records. That initial
record and program remain preserved; the integrity observation explicitly
supersedes the diagnosis. The revised readback consumes the preserved observed
stream and labels its incomplete status rather than reporting a global PASS.

## 2. Three specific text corrections

**Section 4, final paragraph:** replace “producer and consumer coordinates” with
“nonconsumer and consumer coordinates.” The fixed intercept is total minus
consumer, which includes coordination and current-request preparation as well
as stages named producer. The claimed strict two-coordinate domination is
numerically correct with this definition.

**Section 5.2, first paragraph:** replace “has exact negative denominator size
7,914 bits” with “has an exact negative value whose reduced denominator has
7,914 bits.” The normalized denominator is positive; the value is negative.

**Section 6, repair chronology:** native exact incumbent/bound binding was
already present in the frozen v4 smoke source. So were the common incumbent
feasibility check and complete old-request transmission. The paragraph should
not assign their discovery or repair to the post-v4-smoke interval. The actual
amendments establish this chronology:

| Amendment | Timing and substantive change |
| --- | --- |
| [1](../../../development/service_contract_amendment_1.json) | Before service smoke or scalar execution: charge live scientific state before cold/fresh disposal and distinguish later retained-size diagnostics. |
| [2](../../../development/service_contract_amendment_2.json) | Before the first root service execution, v3: exact native incumbent/bound binding, common feasibility, complete old inputs, unused-manager avoidance, disposal and failure/setup scope. |
| [3](../../../development/service_contract_amendment_3.json) | Before the first root service or scalar execution, v4: the generic paid global interval screen before exact receiving enumeration. |
| [4](../../../development/service_contract_amendment_4.json) | After the v4 smoke and before primary v5: add current old-input/packet copies to bootstrap live snapshots and prepay source capacities before reads/hashes. |

This distinction is also preserved in the earlier
[source-bound service review](../service_audit_v5/review.md).

## 3. Numerical and service checks that agree

The [transcription readback](transcription_readback_v2.json) compared all
48 primary cost-table entries, twelve displayed cumulative differences and
thirty secondary table values without discrepancy. Every consumer threshold
row agrees with the observed bill plus the 1,024-unit reserve: at the smallest
threshold the counts are 37, 42, 44, 41, 46 and 37 in the report's method order;
all methods have 48 at each larger threshold. All 48 first primary requests
have the stated 430,041 source charge. The four unchanged first pruned packets
each add three consumer units; the other twenty packets and their consumer
bills shrink, while all twenty-four total bills grow. The finite-obstruction
and standalone-pruner counts are transcribed consistently with their existing
reviews; they remain those authors' executions.

The direct ordinary receiver first validates the actual feasible incumbent and
computes its rank. A sound upper enclosure over the whole Boolean cube is
sufficient for the narrower current incumbent sublevel. If that screen does
not prove the bound, the code visits every assignment, checking all hard rows,
the rank cutoff and the actual loss. The common receipt independently binds
the complete current record, supplied incumbent, bound, rank, source and unit.
It certifies every point in the incumbent sublevel, including all minimizing
ties; it neither finds the incumbent nor returns minimizing identities.

The saved primary work counters show **twelve screen completions**, exactly the
constant requests in both recipient conditions, and **thirty-six enumeration
completions**, all parity and complementary requests. Thus the generic screen
is correctly described, and the nonconstant direct-method results did not come
from that shortcut or a supplied observer answer. The synthesis correctly
distinguishes lower direct cost on every request *against P-REUSE* from its
minimum *among all six methods on complete six-request cells*.

The consumer-price result matches the
[independent exact economic audit](../economic_robustness_v1/review.md): seven
primary cells have direct checking as their unique minimum for every
$`\rho\ge0`$; k5 resident changes from direct checking to warm ADD at exactly
$`2556095/1236394`$. P-REUSE never reaches the envelope, including ties. Every
secondary cell has a direct-method line strictly smaller in both coordinates
than every alternative. These are fixed-path, finite-catalogue results.
The report correctly retains the three request-level native-event exceptions
to pooled-category domination and the difference between a completed bill and
an enforced account with a protected failure reserve.

The arithmetic-fragment explanation agrees with the independent witnesses:
valid 128-bit input components can generate the exact 7,914-bit denominator
required at the ADD difference root, while the converse incumbent cutoff has
a reduced 254-bit denominator that native preparation rejects. Neither claim
implies semantic impossibility or a total bridge over all inherited inputs.
The receiving service and the finite comparisons therefore support an ordinary
checked-proof interface without an affirmative general plurality advantage.

## 4. Closure

The [input inventory](input_manifest.json) identifies the actual sources and
evidence read. The initial reader failure, corrected interpretation, captured
drafts, observed rational bytes and both reader versions are retained.
The [focused style receipt](focused_style_receipt.json) concerns only this new
review and its plan; it is not a global style or live-rendering claim.
No root report, worker, original invoice, source snapshot, ledger or clock was
edited. Final consumer-cap results and any later rational-lineage resolution
require their own clearly identified disposition.
