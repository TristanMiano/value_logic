# P3-09 broker adapter handoff

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated ordinary-control
reviewer. **PREPARATION and DEVELOPMENT**, October 11, 2026. Principal clock
credit: **zero**. Entry commit:
`f2a240b87d4df07ac91874b092db20b8c4378889`.

## Status and source binding

The new `v3/experiments/p309_broker.py` is ready for the root's common
prospective source freeze. Its SHA-256 is
`466546c583880575867dcfb827baede19d4905a9f28681213da27ccc22998ebd`
and its length is 56,461 bytes. No existing worker was edited. The source-only
inventory is `source_inventory.json`, SHA-256
`18e7fc636b22755530f7dde32584ee6a72fd4ccb107fac051f3323143221bdcb`.
It verifies the inspected inherited source bytes against the published entry.

The completed development snapshot is `development_v1/source`, with manifest
SHA-256 `78bcb45145ed69a0d4d2ae55cb19971512c96296baff583aefe869875dc06ede`.
The selfcheck passed all 143 named assertions. Its full result is
`development_v1/run/results.json`, SHA-256
`7a2d6d7eba3699008f6d31a05eeb07fa0a02518bf11601f0ae630382022585e7`.
All twelve frozen local source files remained unchanged after execution.
The canonical adapter still matches this snapshot at handoff.

No final population, query, private truth or final random stream was generated.
There were zero calls to the final generator and final group scheduler from
the selfcheck. Root preparation may enumerate opaque schedules independently;
that metadata operation constructs no queries and calls no random generator.

## Callable boundary

| API | Result and constraint |
| --- | --- |
| `source_paths()` | Complete twelve-file local import closure, relative to the repo root. Includes the adapter and optional reporter. |
| `default_config()` | Pure frozen metadata: recipes, literal seed labels, methods, caps, accounting and inference scope. No sampling. |
| `groups(config)` | Six group dictionaries with `id`, `arm='broker'`, and opaque `recipe`. It validates shape and scalar contracts without constructing a query. |
| `units(group, config)` | Full method configurations with complete unit IDs and full pairing target IDs. No population or solver calls. |
| `generate(group, config, *, exposure_token=None)` | Rejects before any population operation unless the exact P3-10 token is supplied. Returns only canonical public CNFs and group/segment metadata. Do not call during P3-09. |
| `run(unit, public_input, config)` | One paid public episode, separate common source bill, actual local bill and optional report bill. No private truth access. |
| `score(unit, result, public_input, config)` | Separate exact observer after the public seal. Retains incomplete costs and completed semantic failures. |
| `selfcheck()` | Development toy fixtures only; returns `status='PASS'` and raises on failed checks. On failure save `SelfcheckFailure.record`, which retains returned paid evidence. |

Unit identities include group, seed-free configuration and seed slot. The
`configuration_id` excludes both seed and population. `method_kind` is
`candidate`, `ordinary` or `mirror`; mirrors have `identity_duplicate=True`.
Each unit carries known stakes, native acquisition parameters, segments, and
pairing metadata. `base_id`, `cold_id`, `identity_of` and `stakes_reference`
always identify complete units. Same seed is explicitly insufficient to
equate the broker's and ordinary controller's feedback paths.

Public inputs contain only `query_id`, `variables`, canonical `clauses`,
`source_version` and `semantics_version` per query. Gate construction mode,
circuits, witnesses and private labels do not reach a policy. Each `run`
creates fresh scientific state. The source remains openly supplied to every
method under the declared installed platform; no confidential construction
recipe or hidden stronger oracle is assumed.

## Prospective catalogue and genuine transfer

There are two fixed public populations in each of three families. Mixed and
cheap-null episodes have horizon 64. Transfer episodes have a 64-request mixed
prefix followed by 64 new full-key gate-CNF requests. All episodes use blocks
of four and six stateless experts, including both constants. The finite
policy paths use three fixed seed slots; deterministic methods execute once
per public population. These are prespecified finite paths under the retained
`DEVELOPMENT_MT` implementation, with no IID or fair-bit inference.

| Group kind | Stochastic configurations times three slots | Deterministic configurations | Executions per population |
| --- | --- | --- | --- |
| Mixed | 18 times 3 | 10 | 64 |
| Gate transfer | 14 times 3 | 10 | 52 |
| Cheap null | 14 times 3 | 10 | 52 |

Two populations of each kind give 336 executions and 28,160 scheduled request
positions. Eighteen executions, or 1,536 request positions, are explicit
identity mirrors. The other 318 are named `non_mirror_episode_executions`;
this does not call them distinct mathematical trajectories or independent
observations, since base/live/provider variants are also coupled.

The stochastic symmetric catalogue contains six broker variants: both
uniform and positive-ticket selection, each with hard-disabled cold, live
hard cold, and live hard hashed selected-receipt cache. It also contains
ordinary probability-to-cost, ordinary combo with linear or hashed caches at
three supplied prices, and the exact ordinary kernel mirror. The deterministic
catalogue retains bounded enumeration and bounded DPLL with both fallback
bits, full charged enumeration, exact DPLL, linear and hashed exact caches,
and both no-compute endpoints. Mixed groups add normalized stake pairs
`(1/2, 3/2)` and `(3/2, 1/2)` for probability-to-cost and the hashed combo at
the fixed raw price `1/10000`.

The gate suffix changes the program construction class while preserving the
same CNF receiving service and fixed code. It uses three primary variables,
two four-gate AND/OR/XOR circuits and an asserted XOR output miter: twelve
variables, clause width at most three. The second circuit is copied, mutated
at one gate, or independently constructed. No solver filters final instances.
A bounded canonical-key redraw rule enforces new full keys relative to the
prefix and earlier suffix positions. The fixed learner's paid online state
continues across the boundary; report prefix and suffix separately. This is
not an offline fitting or circuit-optimality claim. The full DPLL and cheap
visible shortcuts remain ordinary competitors. The null family deliberately
retains formulas with very cheap exact visible answers.

## Common information, feedback and output service

All methods receive the same canonical CNFs, same original six-expert library,
same prices, provider limits and current exact-answer service. Bounded proof
timeouts remain unresolved and use the supplied fallback; they may still
complete the common forecast/action service. `full_horizon` means all required
forecast/action positions were delivered, not that every position received a
checked proof. The certificate arm has its own stronger receiving service.

The broker buys one logical checked receipt per block and records the actual
selected propensity. Hard state may upgrade only a previously paid current
full-key answer; its learned component continues on the original selected
feedback. The cached provider preserves those logical selections and updates
while replacing repeated physical provider work by paid cache reuse. The
ordinary methods may choose a different acquisition history using equal
initial access and prices. Their different use of selector and action bits
means passing the same integer seed does not equate their paths.

The ordinary combo remains a credible fallible controller with an explicit
exploration floor: designated unknown selected queries force a full purchase.
Its optional purchases use public shape proxies and its own successful paid
cost history; that history is not an oracle and does not turn failed calls
into free observations. It is neither an optimal value-of-computation policy
nor a claim to enumerate all ordinary algorithms. Both zero-compute endpoints
remain available to expose that floor at large prices. The mandatory mirror
is the identical kernel and invoice, so ordinary attainability always
includes the candidate's own computation; no exclusive algorithmic novelty
follows from a favorable finite comparison against the distinct catalogue.

## Accounting and score semantics

The actual common installed source charge for this source revision is 65,114
word units per episode: the preserved core's 50,115 plus 14,999 for the whole
new adapter. The optional reporter has a separate 6,380-unit source charge
plus actual reporting execution. Its source is included in the complete
snapshot, while its extra invoice is excluded from terminal-only rankings.
Python import/orchestration, supplier generation, audit JSON and private
scoring execution are explicitly outside the inherited word tariff. The
adapter is installed in full for all methods even though it co-locates the
observer and supplier code. These are declared service units, not physical
CPU time, process memory or minimum possible deployment overhead.

The cold episode account is `2**38`; optional report execution is capped at
`2**48`. Source reads, selected receipt calls, provider/check work, advice,
selector/action bits, finite numerical updates, cache operations, output and
retention are charged by the preserved implementations. Source and local
invoices remain separate and also sum to `cold_units`. Neither failed
prefixes nor denied optional reports erase an already returned paid record.

The standardized score includes `status`, `validity_pass`, `full_horizon`,
`horizon`, exact rational pairs `brier_mean`, `base_brier_mean`,
`uniform_brier_mean` and `action_loss_mean`, integer `cold_units`, `local_units`
and `optional_reporting_units`, and raw/normalized native prices. Brier uses
the immutable pre-current-computation forecast; terminal loss uses the actual
terminal bit. They are separate services and diagnostics. Raw task loss and
raw acquisition price both divide by the declared maximum task loss. Thus
raw combo price `1/10000` becomes normalized `1/15000` under either asymmetric
pair. Readout comparisons at fixed forecast history are separated from
changed acquisition under the combo, and retrospective repricing is separate
from a price-supplied policy execution.

Private evaluation independently enumerates assignments using bit masks. A
bad forecast encoding, nonbinary action, wrong bound receipt or unsupported
hard claim produces `validity_pass=False`, `status='FAIL'`, null complete
metrics, diagnostics and all paid costs. It is a completed adverse outcome,
not a retry license. Changed outer unit/input binding or inconsistent
accounting remains an integrity error. Unexpected programming errors are not
broadly swallowed. Incomplete service has missing IDs, paid costs and clearly
labelled closed-prefix diagnostics; it has no positive complete-denominator
ranking.

Top-level `base_path_sha256`, `delivered_path_sha256` and
`action_path_sha256` bind the recorded mathematical paths. They exclude fees
and provider identity; the base digest also excludes live-hard changes.
Scores retain all six original experts, constant-half, exact and dyadic
equal-weight mixture, and chronological same-hard-mask static readouts, plus
the exact first-occurrence full-key indices and denominator. These are
evaluator-only diagnostics on that policy's recorded paid history, not new
deployed controllers or regret against adaptively upgraded experts. Optional
paid interval endpoints, widths and conflict flags remain descriptive; no
empirical coverage claim is inferred from the seeded development source.

The root analyzer can average each whole fixed configuration over seed slots
within population and then equally over the two populations before taking
any catalogue minimum. Deterministic reuse creates no new replication.
Asymmetric deployed arms are intentionally limited to probability-to-cost
and combo; they do not constitute a complete asymmetric best-ordinary
catalogue. The symmetric experiment retains all strong ordinary controls.

## Development evidence and reproduction

The saved plan predates execution. There were 28 normal toy episodes, one
paid provider-denial episode and one optional-report-denial episode. All 28
normal episodes completed; all seven normal broker/mirror reports succeeded.
The provider denial retained 70,635 cold units, including 5,521 local units,
and withheld complete-horizon metrics. Its rejected report separately retained
6,636 units. The optional-source denial left the exact completed core episode
unchanged and returned a failed optional report. The separate source-version
and withdrawal boundary account retained 3,458 units. Three observer-only
malformed copies were graded as semantic failures with their paid costs.
These numbers document implementation behavior on the fixed toy, not final
performance evidence or a tuning criterion.

The completed invocation was:

```bash
python v3/work_logs/P3_09_2026-10-11_S1/reviews/broker_design/development_v1/development_observer_v1.py v3/work_logs/P3_09_2026-10-11_S1/reviews/broker_design/development_v1
```

The observer refuses to overwrite its saved `run` directory. For a new
development reproduction, use a new versioned destination containing the
same frozen closure, observer and manifest. Do not reuse a completed result
directory or edit its records. The root preparation suite may call the
unchanged adapter selfcheck in its own freshly source-bound preparation
attempt and must preserve a returned failure record if it raises.

Canonical ownership is returned to the root at this handoff. No further
policy executions, final generation, clock changes or shared-source edits are
planned by this reviewer.
