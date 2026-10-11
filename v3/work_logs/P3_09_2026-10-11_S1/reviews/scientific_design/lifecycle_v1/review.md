# Independent lifecycle and preparation review

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 11, 2026 UTC.
**PREPARATION; same-model independent source review, nonblind to development.**
No final configuration, schedule, seed, population, case or outcome was read.
No adapter generator, final worker or private scorer was executed. The only new
execution was a disjoint lifecycle toy using integer bills and named statuses.
Agent work receives **zero principal clock credit**.

## Judgment and exact source scope

The captured implementation has **no identified blocker in preparation-before-
generation ordering, public-before-scoring ordering, fixed-root retry counting or
seal-based completion** under its declared trusted local process/filesystem
assumptions. It preserves a negative returned service result as an outcome and
does not rerun it merely because a later callback is interrupted.

The [source manifest](source_manifest.json) and complete relative-path snapshots
bind this review to:

| Source | SHA-256 |
|---|---|
| `p309_lifecycle.py` | `2cca63d82e684041b2b0c502dd396a6f0e82a8268d64a2d728076b84a1fcb1ee` |
| `p309_freeze.py` | `f5bdd254169cf8b88102ac300c448bee2d94c5ddd26a547663d08f56d8365729` |
| `p309_analyze.py` | `07f95128c4651388accca592eeb512e6df1c9e2681617f62957b071f07eeecc6` |

The analysis file is included for the seal/denominator/accounting interface. This
is not a duplicate full audit of the broker and certificate analyzers; their
owners are independently checking schema, price and coverage compatibility.
The initial scientific-design review remains the proposal, while the principal
owns the adopted protocol and final configuration.

## 1. Global preparation boundary

`prepare()` first validates the fixed code-defined configuration, group and unit
metadata. It assembles source paths from the driver, lifecycle, analyzer,
contracts, protocol and **every** selected arm. It snapshots those paths under
the same repository-relative layout and saves the runtime and prospective
schedule. Only the snapshot's `development-checks` subprocess is called during
preparation; this driver invokes each arm's expressly development-only selfcheck,
not `generate`, `run` or `score`.

The source and runtime records are compared again after those checks. A racing
source/runtime change invalidates preparation. A successful directory is renamed
into the freeze with its source, checks, method records and receipt intact; the
freeze verification checks both current and archived source bytes. This is a
whole-suite barrier, not a rule allowing the primary population to be generated
while a transfer or secondary method is still being selected.

Two useful corrections were made during this review and are present in the
captured driver:

- Every returned development-check record must explicitly report `status=PASS`;
  a nonthrowing negative status cannot be accepted merely because its process
  exited successfully. The overall child bundle must also pass and explicitly
  deny final generation.
- The preparation method receipt now distinguishes saved/hashed code and
  configuration, frozen schedule validation, arm-specific new development
  operations and inherited development evidence. It no longer asserts that
  every selected representation was executed on a toy. This distinction matters
  for the exact nine-fixture conformance worker: its new selfcheck exercises
  preadmission and the inherited full execution evidence remains separate.

These statements inspect the driver's call boundary. They depend on each
adapter's source contract that `groups` and `units` are metadata-only and that
`selfcheck` uses separate development inputs. This review directly established
that property for the new conformance adapter; the broker/certificate adapters
have their owners' corresponding reconstruction.

## 2. Source imports and environment

The driver checks the resolved path of each loaded adapter, the lifecycle and
analyzer. The preparation subprocess records loaded repository Python module
origins and rejects a loaded local file absent from the declared source list.
This corrects the earlier gap between hashing named files and identifying the
modules Python actually resolved. Dynamic inherited imports need their complete
relative paths preserved; flattening this source closure would be incorrect.

The runtime record binds the interpreter, supplied standard-library source and
extension bytes, ABI/integer representation and native loader dependencies. The
principal identified unavailable Tcl dependencies for an unused Tk extension;
the current driver records that optional absence rather than claiming every
shipped extension is runnable. The required CLI/native closure remains checked.
No relevant worker imports a GUI. This is an explicit environment contract,
not a claim to support arbitrary Python releases or arbitrary external modules.

The final driver executes under the restored repository layout after checking
that its current source matches the captured freeze. Its preparation subprocess
executes directly from the isolated copied layout. Therefore reproduction needs
the declared relative paths, current/frozen byte agreement and actual runtime
closure; an isolated loose file or an old saved source with a new dependency is
not the same experiment.

The lifecycle's file hashes and source-origin records are integrity checks for
trusted local execution. They do not authenticate a hostile remote process or
protect against an operator who deliberately rewrites every record and hash.
No stronger security claim is needed for the prospective research contract.

## 3. Exposure and scoring order

`final_stage` requires the explicit `P3-10` task argument and the repository task
pointer before it verifies the freeze. These are operational guards; the agent
must still obey the user's separately selected-task boundary. Closing P3-09 does
not itself authorize invoking the final execution path.

The driver publishes `exposure.json` durably, under the shared writer lock and
with the freeze binding, **before** calling any generator. Existing exposure
must match that binding. Input generation counts as exposure even before an
answer is scored. The exact four-stage dependency order is:

| Stage | Required authority before its callback |
|---|---|
| Inputs | Fully verified preparation and a durable global exposure record. |
| Public methods | Every scheduled input unit sealed complete. |
| Evaluation | Every scheduled public method unit sealed complete. |
| Analysis | Every scheduled evaluation unit sealed complete. |

Public and scoring records additionally bind the relevant upstream result hashes.
The separate evaluator is not called until all public methods finish, including
other arms. The analyzer imports no policy/generator. A callback may use its
ordinary paid expert/provider service; that is different from access to the
external evaluator's completed truth table.

The code does not regenerate inputs during `prepare` to estimate costs or choose
an arm. It enumerates pure group/unit recipe records, which is the allowed means
of binding all methods and denominators before exposure. This review did not
read the resulting final schedule or any selected seed values.

## 4. Durable completion and retry

`publish_bytes` writes an exclusive temporary file, flushes and fsyncs it,
publishes with a nonoverwriting hard link, and fsyncs its directory. Pending
files remain evidence if interrupted. A writer lock prevents concurrent stage
writers. Exact schedule IDs are checked for uniqueness and safe paths.

A completed unit requires exactly one immutable seal with matching
source/configuration/schedule identity, unit hash, exact result-file hash and
start-receipt hash. The result content must agree with its unit and attempt.
An orphan result without its seal has no completion authority. The stage's
`complete.json` is a derived index; if its creation is interrupted after every
unit seal exists, it can be reconstructed without replaying any method.
Conversely, a summary cannot make a missing or altered unit complete. This is
the relevant safeguard against repeating the old rational-stream mistake of
accepting a thirty-row summary after observing only twenty-nine rows.

One stage has at most two execution attempts. The second requires a nonempty
reason and the explicit `unexplained_infrastructure` classification. All sealed
units are preserved and skipped. The fixed output root, source/configuration
binding and unit schedule cannot change to obtain another attempt. A completed
stage rejects a retry; a third attempt is refused. A deterministic defect needs
its separate versioned amendment and data-exposure disposition, not a false
infrastructure label.

Callback-returned no-answer, resource failure or failed semantic validation is a
completed scientific result. It is sealed like a success. An exception before a
returned value leaves the unit unsealed and records the exception and failed
unit ID, without automatically retrying. The principal also authorized a narrow
conformance amendment so a named invalid inner mathematical certificate becomes
an explicit completed `FAIL` score; an outer hash or unit mismatch remains a
hard integrity exception. The [conformance note](../conformance_v1_1/review.md)
records that separate source change and its development witness.

## 5. Incomplete costs: qualification sent to the principal

The lifecycle correctly labels an interrupted callback's unmeasured prefix as
**unknown**, not zero. A returned service's actual invoice can include all its
internal failed proof/purchase requests. After a permitted outer infrastructure
retry, however, the sealed replacement episode does not reconstruct the lost
first callback's bill.

At the captured source, `analyze(config, schedule, scored)` receives only sealed
completed scores, so a final aggregate does not itself display outer attempt
history. The failure/interruption artifacts are preserved elsewhere. I asked the
principal to carry a compact, source-bound outer-attempt audit into the aggregate:
which stages retried, which units had unsealed attempts, known measured prefixes
where available, and unknown overhead. This is an accounting qualification to
resolve in the final report/driver, not a reason to invent missing charges.

The important distinction is:

- **Complete owned-history bill:** every paid internal service attempt of the
  completed scientific policy/history, including its modeled failures.
- **All infrastructure attempts' expenditure:** that bill plus any extra
  unreturned or interrupted outer attempt; potentially unknown.

The former remains a valid exact completed-path endpoint. It must not be called
the latter when an unknown prefix exists. Wall/process measurements remain
separate from the declared scientific tariffs. No cross-tariff universal total
is inferred.

The captured analyzer retains scheduled denominators, marks unknown scored costs
and withholds positive full-denominator catalogue comparisons if relevant scores
are incomplete. Its certificate comparison uses exact delivered-ID inclusion,
not equal success counts, and requires nonempty service before a practical
economic-dominance claim. Those safeguards address missing *scored* service
outcomes; the outer interruption qualification is a distinct layer.

## 6. Independent development witness

[independent_toy.py](independent_toy.py) imports only the captured lifecycle
source. It creates a new development root, never a final directory. Its first
callback returns an explicit failed scientific result with toy bill seven. Its
second callback is deliberately interrupted. One unchanged retry then returns
toy bill eleven for only that missing unit.

The [saved result](run/results.json), SHA-256
`09d9b88d312d6275957ea34376b62322546e40ffe31e5b1c9b70ee10360f5e0b`,
passes six focused checks:

1. The returned negative result is a sealed completed outcome.
2. The interrupted callback records unknown cost and no automatic retry.
3. Missing completion blocks a downstream completeness check.
4. The single retry preserves the negative result byte-for-byte and runs only
   the missing unit.
5. The complete-path toy bill is eighteen, including the negative outcome, while
   the all-infrastructure-attempts total remains unknown.
6. A completed-stage replay is rejected.

The toy bills are explicit illustrative integers, not measurements of a policy
or a physical machine. All attempt/start/result/seal/failure artifacts from this
development witness are retained. No final generator, input, seed or worker is
involved, and no principal research time is credited.

## Remaining boundary

This review supports the recorded lifecycle mechanics at the captured hashes.
It is not a final freeze-verification receipt: the principal is still completing
the protocol, aggregate audit and source preparation. Later source amendments
need their own bounded readback. No additional policy competition or final
exposure is needed to resolve the remaining administrative/accounting record.
