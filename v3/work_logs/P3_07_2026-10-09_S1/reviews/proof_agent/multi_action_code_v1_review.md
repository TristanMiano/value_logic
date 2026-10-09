# P3-07 — frozen multi-action code and saved-run v1 review

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal subagent**.  
Date: October 9, 2026 UTC. Review is read-only with respect to root artifacts.
All targeted probes are **DEVELOPMENT**, with **zero principal credit** and
unmeasured agent research time.

## 1. Versions and disposition

| Frozen source | SHA256 |
|---|---|
| `07_multi_action_forecasting.py` | `4d52fb20d2ebd70cf7b4cf049ecdbf596cc49b353470d3a3782be2b095bb7a9f` |
| `07_multi_action_development.py` | `e71951eec94f481c7a621df3f3c82c67708be309ed161838db155e282a8470c5` |
| Run's recorded computation adapter | `06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615` |

The two requested source hashes were verified before review. Exact copies
are retained as
[forecasting snapshot](multi_action_code_v1_07_multi_action_forecasting.py)
and [development snapshot](multi_action_code_v1_07_multi_action_development.py),
with the [snapshot manifest](multi_action_code_v1_snapshot_manifest.json).
The original run remains at
[multi_action_run_v1](../../development/multi_action_run_v1/manifest.json).

**Disposition:** the saved ordinary-size numerical evidence passes the
independent reconstruction described below. Its original results and scope
remain valid. The frozen v1 source has **one demonstrated transactional
numeric-cap error and two concrete sampling-boundary issues** that should
be repaired in a new version before claiming the corresponding public cap
and failure contract. This is not an invalidation of the mathematical
multi-action bound or the successfully completed saved trajectories.

The root has been informed and plans a new source version and a fresh labeled
development stream. No repair was applied by this reviewer.

## 2. What was independently checked

The [prospective targeted plan](multi_action_code_v1_targeted_plan.json),
[probe script](multi_action_code_v1_targeted_probe.py), and
[saved results](multi_action_code_v1_targeted_result.json) preserve the
review. No prior three-case experiment was rerun.

### 2.1 All 96 stored rows reconstruct correctly

For each of the three 32-row cases, the probe reads the saved pre-service
issuance record and completed row, checks agreement of all common fields,
and reconstructs the enlarged feature vector from the stored mixture,
forecast, weight and cost rows. It independently recomputes:

- The score and actual endpoint/interior allowance.
- The residual, variance, cumulative allowance and `B`.
- Every fixed-action loss, predicted gap and exact residual decomposition.
- Ideal and rounded mixture costs, the actual selected action and sampled
  action cost.
- Checked-service fees, later-feedback fees, non-BUY task loss, controller
  fees and the all-in identity.
- Per-category service totals and equality between the work counter, its
  category counts, the summed row operation counts and the 64-unit setup.

Every reconstructed value agrees with the saved result, and every enlarged
potential inequality holds. This audits the saved arithmetic and account
composition. It does not repeat the adapter's modular-arithmetic audit or
infer statistical performance from the chosen seeds.

The saved cases have these relevant outcomes, before the separately reported
one-time setup fee of `2/3125`:

| Case | Root-tolerance misses | All-in weighted cost | Always-BUY fee cost |
|---|---:|---:|---:|
| Full root, eight bits | 0 | `13869277/25000` | `368` |
| Capped root, eight bits | 31 | `1729334/3125` | `368` |
| Full root, one bit | 0 | `2777833/5000` | `368` |

`root_cap=0` means no additional bracket updates after the initial endpoint
and midpoint evaluations. It does not mean zero forecasting work. The 31
misses correctly retain their actual positive allowances, and the saved
potential uses them. No zero-residual certificate was fabricated on cap
exhaustion.

### 2.2 Issuance precedes the truth service

Source order places `issue`, rounding and action selection before the
`issued_file.write(...); flush()` pair, and places the checked-service call
after that pair. The pre-service record contains no label.

A targeted one-call interception replaces the service entry with a review
sentinel. At that first call, the issuance file is already readable with one
complete flushed row, its query matches the service request, and no label
field exists. The probe stops there and performs **zero** real truth
computations. This directly verifies the relevant call-order boundary
without rerunning the 32-row solver experiment. The intercepted record is
retained in [the order probe](multi_action_code_v1_order_probe/audit_order_only_issued.jsonl).

The record does not by itself provide a separate receipt timestamp for every
historical service. Its evidential basis is the frozen executed source,
consistent saved records and this narrowly instrumented ordering check.

## 3. Demonstrated issue: report rejection occurs after settlement commits

`Forecaster.settle` computes local candidate state and validates several
components, then assigns it to the object, clears `pending`, increments
`settled`, and calls `report()`. The validated values include `variance`
and `allowances` separately, but not their sum `B`. `report()` subsequently
passes `B` to `sqrt_upper`, which calls the 8,192-bit validator.

This permits an apparently failed settlement that has actually committed.
The targeted probe uses only valid public inputs and the existing cap:

- Two constant-zero action rows, four calibration bins, `eta=1`.
- Constant expert `1/2`, `root_cap=0`, and weight `2^4093`, which has only
  4,094 bits and is within the accepted input range.
- Sixteen synthetic stress-test labels equal to one; these are controlled
  unit-level inputs, not purported checked modular-query results.

On round 16, `settle()` raises `Rejected: Bounded rational primitive component
cap exceeded.` Its state nevertheless changes from 15 to 16 settled rows,
and the pending record is cleared. The separate variance and allowance
components have 8,189 and 8,192 bits, while their sum has 8,193 bits. The
work ledger correctly retains the 312-unit settlement charge, but its peak
observed component field still reports 8,192.

This is a real committed-state/exception inconsistency. A caller seeing the
exception cannot safely retry that settlement, because the object has
already consumed it. It also defeats the intended rejection-before-invalid-
state-publication interpretation of the bit cap.

**Recommended repair:** compute and validate every derived report target and
prepare the return payload before committing the candidate state. In
particular, cover `B`, square-root enclosures, scale divisions and reported
bound values, not merely the separate summands. Alternatively, any postcommit
report operation must be total under previously checked invariants. Preserve
the legitimate paid work on rejection while leaving the semantic state and
pending record uncommitted.

## 4. Sampling-boundary issues

### 4.1 `choose_slots` does not validate its own bit cap

The rounder restricts `bits` to an exact integer in `0..32`, but the separate
sampling helper performs `1 << bits` without that validation. A direct call

```python
choose_slots((1 << 33, 0), 33, 0, work)
```

is accepted and charged 39 units. This exceeds the stated rounder/sampler
bit domain. Ordinary saved calls all originate in the valid rounder, so
their categorical probabilities and costs are unaffected.

**Recommended repair:** validate type and range before shifting, and validate
the bounded slot shape before unbounded traversal if the helper is intended
as a public bounded API. No large allocation was used in this probe.

### 4.2 The harness obtains random bits before paying for them

The frozen harness calls `ar.getrandbits(bits)` and only afterward calls
`choose_slots`, whose first successful payment includes the fair-bit charge.
On an unfunded call, the draw has already advanced the random generator
although `choose_slots` raises `Exhausted` and charges zero units.

The targeted probe reproduces that exact three-line order with eight bits
and a zero work budget. The generator state changes before the denied charge.
This is inconsistent with the advertised prepaid resource model on failed
paths, even though the successful saved runs charge the correct eventual
amount.

**Recommended repair:** pay for admitted random-bit acquisition before
generating the bits, or move generation inside a helper that performs its
funding check first. Keep selection and bit-acquisition charges explicit
and avoid charging the same bits twice.

## 5. Other cap behavior and scope

A zero-budget issue raises `Exhausted` without installing a pending record
or consuming a query identity. With a budget exactly sufficient to issue,
an unfunded settlement raises `Exhausted` before modifying the residual or
pending state, and the earlier paid issuance work remains recorded. These
targeted ordinary operation-cap paths behave correctly.

The component has no general cancellation/fallback controller for a pending
forecast whose settlement cannot be funded. A caller must supply its own
declared abort/fallback protocol or sufficient reserve. The successful
development run has ample work budget and settles every row; it does not
demonstrate graceful end-to-end operation under every smaller budget.

The 8,192-bit instrumentation observes selected values, not every temporary
inside rational expressions or every diagnostic return value. Intermediate
exact arithmetic and private reporting should be scoped accordingly until
their full bound/validation contract is explicit. The demonstrated `B`
failure above is the concrete stored/returned-state problem requiring repair;
this review does not claim a separate measured CPU or temporary-memory breach.

## 6. Resource, feedback and all-in interpretation

The work ledger is a declared bounded rational-operation bundle model. Its
fee is exactly the charged operation count divided by 100,000, followed by
the announced round weight. It is not Python instruction count or elapsed
CPU time. Query generation, the exhaustive categorical frequency diagnostic,
and private audit serialization are harness services at the stated scope.
Their outputs are not used by the policy before action selection.

Every round performs a real checked solver call after the action record has
been emitted. If BUY was selected, its label is reused for settlement. If
another action was selected, the same declared service fee is paid for later
full feedback. Thus all rows belong to the fully supervised cohort; the
action-selected settled-subset martingale error identified in the theoretical
review does not occur in this run.

The provider's flat fee is a **stipulated actual tariff**, not its raw
operation count or an empirical upper estimate. It includes the solve,
check, acquisition and storage service. Raw adapter units are reported
separately and correctly are not billed a second time. The saved rows imply
the exact pathwise identity

```math
\text{learner all-in cost}
 =\sum_t w_t\,\text{BUY fee}_t
  +\sum_t w_t\,\text{non-BUY task loss}_t
  +\sum_t w_t\,\text{controller fee}_t.
```

Both added terms are nonnegative for these tables. The learner therefore
exceeds the always-BUY **fee-cost comparator** on each saved trajectory,
before even adding its one-time setup. This is a useful negative finding:
the lower sampled or mixed action-only cost does not imply an all-in win
when every unbought label is later purchased anyway. Any further claim about
a separately implemented always-BUY controller's overhead needs that
controller's corresponding accounting; the displayed identity itself is
exact under the declared tariff convention.

The dyadic rounding uses the sharp fixed-dimension TV bound and exact integer
cumulative lookup. The saved eight-bit/one-bit traces do not establish an
independent-fair-bit probability theorem. The source and result correctly
label that theorem as an additional stochastic sampling assumption rather
than a fact inferred from three seeded development trajectories.

## Final review recommendation

Retain the original run and its sources as successful ordinary-size
development evidence. Version and repair the transactional report boundary,
sampling input cap, and draw-before-payment order, then evaluate the repaired
version on the prospectively declared fresh stream. The original cap failure
and probe must remain preserved. No later gate, contribution status or
P3-07 completion determination is made by this review.
