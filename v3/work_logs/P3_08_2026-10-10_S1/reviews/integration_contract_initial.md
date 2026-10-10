# P3-08 initial integration-contract reconstruction

Contributor: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.
Same-model, nonblind independent reconstruction by the integration-review agent.
Source inventory captured at `2026-10-10T16:06:54.068342+00:00`; repository HEAD
was `a818baf5b8838ac452ee77aa3d2ffd4d4fce0aad`.

**Zero principal research-clock credit.** Agent work was concurrent; its resource
cost is unmeasured. No policy experiment, new executable implementation, final
freeze, evaluation population, commit, or push was performed for this initial
review. The only repository addition is this review. The algebra below was
reconstructed from the stated contract and inspected code; earlier reviews were
visible and are explicitly not treated as blinded replication.

## 1. Initial verdict and selected route

The accepted mathematical interface is sufficient for a small combined broker.
I found no new mathematical flaw in the frozen-hard-answer theorem under its
stated predictability, soundness, and unchanged-path premises. I found concrete
integration hazards in using the existing lower-level APIs without their trusted
broker and in confusing a frozen report with current hard truth. Those hazards
do not reopen the accepted trusted `execute()` results.

The smallest route that makes U04 operational is:

1. Keep an unchanged numerical base learner as a shadow process, with the same
   expert advice, purchases, selected labels, block updates, and bit schedule.
2. Maintain a separately typed, versioned live hard-answer state. A successfully
   checked receipt fixes the matching current truth coordinate immediately at
   the next eligible transaction. Dependent current estimates become stale or
   are replaced, while historical issued forecasts remain untouched.
3. Before a new forecast or action is issued, a current sound hard answer can
   replace the base output by the correct value. Retain both original base and
   actually emitted forecasts as immutable records.
4. Transfer **only upper bounds** from the base output by sound pointwise
   improvement. Do not recompute the base centered confidence formulas using
   selection-dependent live forecasts or transfer base lower bounds.

The principal explicitly selected this live-hard-state/shadow-base route while
this review was being prepared. The proposed generic bounded-CNF port is a new
source-bound implementation, not a monkeypatch of the Euler service. A direct
certificate for a separate predictable snapshot remains a mathematically
available extension; it is not necessary to call the first broker complete.

## 2. Reconstructed objects and event order

The following distinctions are load-bearing, not merely naming conventions.

| Object | Meaning and permitted change |
|---|---|
| Semantic claim | Complete public mathematical input plus interpretation/source versions. Repeated request IDs may refer to the same semantic claim. |
| Request identity | Exact issued request occurrence. Its purchased receipt must bind this occurrence as well as the semantic claim. |
| Live hard coordinate | Checked true, checked false, unresolved/pending, failed, conflicted, or stale. A learned score is not a hard answer. |
| Base forecast | Dyadic number produced from fixed public experts and the block's frozen weights. Preserved even when an emitted output is improved. |
| Emitted forecast | The actual prospective output, fixed before the corresponding receipt. Its eventual Brier score uses this number forever. |
| Prospective action | Paid randomized action coupled to the base bit draw, or its sound hard-answer correction. |
| Terminal action | Action after any licensed current-answer correction. A purchased successful answer makes its own terminal error zero. |
| Feedback | Exactly one checked selected expert-loss row per completed block, with its actual positive propensity. |
| Performance report | A named target, source/epoch, method version, confidence scope, and paid reporting procedure. It is not a truth-law declaration. |
| Resource invoice | Actual debits, including failed work, distinct from reservations and private evaluator work. |

For the primary route, freeze the base weights at block entry. The broker owns
one selector draw and its positive law. On each round it computes public advice,
issues and records the base forecast/action, checks the already available hard
state, and issues the actual forecast/action. Only then may it run the selected
provider. Receipt admission updates live hard state, but selected expert feedback
is settled only at block end. A newly checked answer can improve later same-block
emitted forecasts, without affecting later base forecasts or learning updates.

Neither the tape, receipt eligibility, source epoch schedule, nor any branch that
controls future selection, expert state, or bit consumption may depend on sampled
action values under the inherited sampling/action proof. Action values may be
recorded and output. Their conditional-independence premise is otherwise lost.

Keep the exact number and order of action-bit draws even at known zero/one
coordinates. Drawing fewer bits there changes later selectors/actions in a shared
bit tape and defeats the straightforward path coupling. A separately designed
stream split could work, but it would need its own version and argument.

## 3. U04 and the two valid composition arguments

### 3.1 Live hard state and pointwise upper transfer

Let the base forecast be `q_t`, the fixed interpreted answer `y_t`, and the live
forecast be `q^L_t`. Whenever a checked current answer is available before issue,
set `q^L_t=y_t`; otherwise set `q^L_t=q_t`. Keep the base purchase/update path.
Then, on every admitted path,

```text
(q^L_t-y_t)^2 <= (q_t-y_t)^2.
```

Use the same base prospective action at unknown positions and the known correct
answer at corrected positions. Every corrected terminal error becomes zero and
other terminal errors are unchanged. Thus `F_live <= F_base` and
`Z_live <= Z_base` pointwise. Under the action-independent history premise, the
corresponding realized-history conditional action means are also ordered.

Every base simultaneous upper event therefore remains an upper event for its
matching live target. Base two-sided intervals provide their upper endpoints
for this purpose, but their lower endpoints do not bound the improved target.
The inherited expectation theorem transfers in the same direction. Add the
actual extra hard-state, output, and reporting costs to the same episode's bill;
this pathwise addition does not assume the bill is independent of the selector.

The transferred upper is calculated from **base statistics** and must say so.
It need not equal a directly calculated estimate of live loss. The fixed-expert
comparator and the unchanged base path remain part of its contract.

U04 expressly permits dependent estimates to be marked stale. Consequently a
block-snapshot output can remain as a historical/snapshot forecast after hard
resolution, provided the live truth coordinate updates and the old output is
not advertised as a contradictory current truth estimate. The primary route
avoids that ambiguity by also hardening newly emitted current forecasts.

### 3.2 Predictable snapshots and direct reports

For completeness, reconstruct the alternative accepted theorem. Freeze at block
entry a sound answer mask `H_kt` and its version-matched answers, measurable before
selection. Put `q'_kt=(1-H_kt)q_kt+H_kt*y_kt`. New labels bought in this block are
not added to this reporting mask until a later block. With binary answers,

```text
d' = (1-H)d;   g' = (1-H)g;   v' = q'(1-q') = (1-H)v.
```

For a predictable public center `a_kt`, write `r'_kt=d'_kt-a_kt`. Define

```text
U_a = sum_k sum_(t != J_k) a_kt
      + sum_k (1/pi_kJ_k - 1) r'_kJ_k,

A_a = sum_(k,t) (a_kt-v'_kt) + sum_k r'_kJ_k/pi_kJ_k.
```

Subtracting from `V'=sum_(k,t!=J_k)d'_kt` and `F'=sum_(k,t)g'_kt` gives

```text
V'-U_a = F'-A_a
       = sum_k [sum_t r'_kt-r'_kJ_k/pi_kJ_k].
```

The random omission of `J_k` from the first center sum is handled exactly.
Conditional on pre-selection information, inverse-propensity sampling makes each
bracket's mean zero. With `a_kt=(1-H_kt)/2`, its range width is at most

```text
C'_k = max_t (1-H_kt)*abs(1-2q_kt)/pi_kt.
```

This is not the old half-centered width blindly evaluated at extreme `q'`.
Known zero-loss positions contribute no unknown residual. On the same base
trajectory and actual propensities, `C'_k<=C_k` and `Q'=sum_k (C'_k)^2<=Q`.
These inequalities compare widths/radii, not complete realized interval endpoints.

Retain the predeclared `R=S*ceil(sqrt(2m))` and `lambda=8/R`. The inherited
one-sided radius is `Q'/R+R/2`, and the two-sided radius is `Q'/R+5R/8`.
Optimizing the rate after seeing random `Q'` is not licensed. Conditional on the
complete action-independent selector/snapshot history, use only the `n'`
unbought, uncovered positions for the action tail. If `n'=0`, terminal error and
its mean are exactly zero; the all-issued Brier loss is exactly the purchased
issued Brier sum, which need not be zero. If all issued positions were covered,
all three losses are zero.

### 3.3 New finite witness: sound immediate hard answers do not make the mask predictable

Take one block of size two, with both positions the same false claim and base
forecasts `(1/4,1/4)`. Let `J` be uniform on the two positions. Begin with no hard
answer. A label bought at position one immediately hardens position two's newly
issued forecast to zero. Naively use the live mask in the preceding direct
snapshot formulas with `a=(1-H)/2`.

| Selector | Live forecasts | Live mask | `V_live` | Naive `U_a` | Residual |
|---|---|---|---:|---:|---:|
| `J=1` | `(1/4,0)` | `(0,1)` | `0` | `-1/4` | `1/4` |
| `J=2` | `(1/4,1/4)` | `(0,0)` | `1/4` | `1/4` | `0` |

The residual mean is `1/8`, not zero. Every hard answer is correct, the tape is
exogenous, and the loss identity still holds pathwise, but the new mask depends
on the current selector. This breaks the martingale premise of the naively
recomputed direct certificate. It does not break sound base upper-bound transfer.
This is an analytic counterexample, not a newly executed random experiment.

## 4. Receipt and selector binding in the inspected APIs

`FrozenProd.issue()`/`close()` in `v3/checks/07_selective_feedback.py` bind an
issued record by exact local object identity and validate a `ServiceResult`'s
request ID, full claim key, checked boolean, exact integer answer, successful
status, provider name, and provider version. A repeated semantic query with a
fresh request ID can reuse hard knowledge, but a purchase still binds its own
issued request. Do not conflate those two identity tests.

There are deliberately weaker lower-level boundaries:

- `FrozenProd.close()` admits the first valid receipt in a block, without
  independently proving that its position was the broker's sampled position.
  The trusted `execute()` supplies that missing condition.
- `AllocatedProd.close()` validates that tickets are `1` or `B+1`, but does not
  bind the supplied multiplicity to an internally retained sampled ticket.
  Again, its trusted `execute()` passes the actual result from `prepare_block()`.
- `prepare_block()` is not itself a capability that prohibits another selection
  before a first round issues. Its trusted caller invokes it exactly once.

These are documented trust premises, not defects in the accepted executions.
The new composed broker should own a single-use block selection record containing
the block/index, exact law, selected position, selected multiplicity, and epoch.
Close/update/report should consume this record rather than accept an independent
caller-supplied propensity. Reject a second prepare, unscheduled receipt, reused
receipt, duplicate close, false ticket value, or selector record from another
block. Do not silently resample on a malformed/failed receipt.

The adaptive update objective uses `(1/pi-1)` because bought actions are corrected.
The all-issued forecast objective uses all positions. Replacing one by the other
changes the bound even when the same selected answer is used.

The old services are trusted local code, not external receipt authentication.
The generic port must state the same boundary or implement an actual checker.
Testing forged local dataclasses establishes rejection behavior only; it cannot
prove a cryptographic or hostile-provider security claim.

## 5. Scope withdrawal, conflicts, and failure

### Versions and current warrants

Use complete semantic records as exact identity, with hashes as audit references.
The old modular `claim_key` includes semantics version, source version, public
arithmetic input, and target residue. A bounded-CNF key analogously needs its full
canonical input/semantics; request ID alone and a digest alone are insufficient.
Each hard entry also needs its receipt provenance and active warrant/epoch.

On withdrawal or source/interpretation change, make affected entries unusable at
the next current read and mark dependent current reports stale. Lazy rechecking
is permitted. A global epoch with exact read-time comparisons is simpler than
an uncharged eager scan. Historical forecasts, receipts, invoices, and their old
conditional claims remain historical records. They are not relabelled as evidence
for the new interpretation. A stakes-only objective change need not withdraw an
independently checked mathematical answer, but it changes dependent cost reports.

A withdrawal during a block invalidates the use of an old snapshot for the new
scope. The minimal contract stops the successful-episode route and starts a new
epoch/episode after re-admission. It must not drop the affected records and keep
claiming a successful complete-block theorem. If an invalidation cannot be funded,
the safe result is stopped/stale service, not continuation under the withdrawn
warrant. Conflicting admissible hard records produce a conflict status, not a
last-writer-wins boolean or a default false answer.

### Failed resources and receipts

The accepted success theorem requires exactly one **successful checked** purchase
per block. A failed provider call is not an observed label, not zero loss, and not
permission for a replacement sample. Stop or expose a separately modeled fallback;
do not condition the original theorem on an arbitrary subset of successes.

Reserve provider completion caps before invoking providers, absorb their actual
invoices even on failure, and charge binding/checking/output work separately when
it is not already included. Reservations are neither spent units nor additional
flat fees. Releasing unused funds does not create an extra query position.

New hard-state acceptance/eviction/withdrawal and public report construction are
real controller operations. Precharge complete mutation bundles before publishing
new state. A failed commit cannot leave a partly updated hard coordinate or emit
an uncharged corrected answer. If a receipt was acquired but state retention fails,
record that distinction and stop the promised combined service without erasing
the acquired receipt or costs.

Current `execute()` failures attach aggregate meter, round-count, and purchase
metadata, but do not expose their full local partial transcript/invoice list.
The new broker should retain each completed public unit and failed receipt in
durable failure output. Do not claim interruption recovery from only a final
exception counter. The principal's experiment harness still needs its own stage
and attempt records.

The existing observable-performance calculators are offline analysis. Reusing
their formulas in a live output needs priced public reads, receipt validation,
wide integer/rational arithmetic, storage, and emission. Under the old largest
admitted precision, accumulators exceed a 64-bit word. Either bound the new
reporting scope more narrowly with a justified cap or pay operand-word tariffs.

## 6. Smallest sound implementation and port boundary

The selected architecture requires only a generic typed query/receipt layer, a
hard-state store, a broker that owns the selector, and a retained base numerical
learner. It should not import all of `Kernel` merely to store a binary answer.

`Kernel` in `03_bounded_logic.py` already supplies a useful reference for U04:
checked VM acceptance stores signed evidence, reports overlay direct literals,
withdrawal removes dependencies and restores an outer cover, and current-warrant
checks compare complete source/loss records. Its public `add_assumption()` accepts
**conditional assumptions**, not arbitrary checked external receipts. Mutating
its `known` or `constraints` internals, or relabelling an imported receipt as a
conditional assumption and then claiming unconditional checked truth, is not a
sound direct reuse of that interface. A new small store can state its narrower
checked-binary scope while existing finite-source/repair services retain their
own separately implemented semantics.

For the generic CNF port, the old `FrozenProd.issue()` and `close()` are explicitly
Euler-type/provider-bound. Preserve the numerical Prod recurrence and fixed-mass
rounding, but version the port and new generic validation boundary. A small
equivalence check on identical expert rows, selected labels, contract, and bit
tape can establish exact numerical agreement with the old implementation. It
does not by itself validate the new query checker or resource charges.

Recommended result fields include stage, method/source/checker versions, epoch,
block/index, exact semantic and request identities, base/emitted forecast,
prospective/terminal actions, hard-state status/provenance, actual selector law,
receipt disposition, paid invoice, and the named guarantee route. A live output
using inherited statistics should explicitly record
`base_upper_transferred_by_sound_correction`; a direct live lower certificate is
absent. Current truth and historical forecasts remain separate typed fields.

Ordinary controls must receive the same source, fees, cache rights, outputs, and
hard-state operations. The exact-table obstruction on the Euler family remains
accepted. A new family can yield a different comparison, but source-visible exact
or analytic shortcuts cannot be removed after they succeed. The same composition
can be implemented as an ordinary learner plus ordinary checked cache; no numerical
difference is presumed from the value-language description.

## 7. Suggested focused verification before broad development

These are proposed tests, not a claim that they have been executed.

| Check | Concrete decisive evidence |
|---|---|
| Numerical port | Same finite expert rows/selected labels and bits give identical base dyadic forecasts, weight tuples, and rounding to the old numeric path. Include `state_bits=1` and a nonzero floor residual. |
| Coupling | Empty hard store reproduces the base transcript exactly. Adding sound hard entries changes only permitted emitted outputs, hard-state work, and reporting costs; selector positions, bit count/order, purchased rows, and final weights match. |
| Immediate U04 | Buy an early occurrence and repeat the same semantic claim later in the block with a fresh request ID. Current hard status and later emitted forecast become exact; earlier emitted/base forecasts remain byte-identical. |
| Hard mask boundary | Retain the analytic `B=2` witness above. The broker labels such outputs upper-transfer only and never claims the failed direct predictable-mask argument. |
| Receipt identity | Reject wrong request ID, semantic key, source/checker version, block, status, answer type/value, unchecked answer, duplicate receipt, and a receipt for a nonselected occurrence. Preserve spent costs. |
| Selector ownership | Reject a second selection/preparation, forged ticket multiplicity, position substitution, and repeated closure. Exact selected propensity equals the internal draw's declared law. |
| Failure | Exercise one debit boundary before solve, checking, hard-store commit, and corrected output. No partial hard fact or successful completed-episode theorem appears; already spent costs and completed records remain. |
| Withdrawal | Withdraw a retained warrant, then query the same semantic input. It is stale/unresolved until rechecked; previous historical forecast and invoice bytes stay fixed. Changing semantics cannot hit the old cache. |
| Conflict | Contradictory admitted records produce typed conflict and stop unconditional hard correction. A failed/unchecked record cannot manufacture conflict or overwrite a checked coordinate. |
| State capacity | Declared eviction or admission rejection remains paid and explicit; expired/evicted entries are never fetched through an audit-log or evaluator backdoor. |
| Scoring boundary | Evaluator labels are unavailable until public trace closes. Bought corrected actions score zero terminal loss; their pre-purchase forecast retains its actual Brier loss. No missing label is scored as false. |
| Public reporting | Reconstruct any certificate from public issued records and bought labels only. Transfer base upper endpoints, add the exact actual invoice, and deny live lower/anytime/multi-arm interpretations not proved. |
| Ordinary control | Matched information/output/cache/checking service and source closure; retain adverse cost and forecast comparisons. Free-oracle output is clearly a diagnostic, never a paid contender. |

The load-bearing first set is numerical/coupling/U04, selector-receipt identity,
one genuine failure, and version withdrawal. Broad repetitions should resolve a
specific remaining risk rather than substitute for these witnesses.

## 8. Source binding

Hashes cover complete files. Some longer derivations were inspected at their
relevant sections, not line-by-line in unrelated theorem sections. This review
does not claim a fresh audit of the entire historical phase.

| Source path | SHA-256 |
|---|---|
| `v3/RESEARCH_PROTOCOL.md` | `ef57593ce23cbe06b1683fc3609526f700b6ab5c395befacbbcd01bd48f3aa52` |
| `v3/foundations/01_desiderata.md` | `0c1b250e1e22640c1a965015e009ed18a2661415af83f5086b893f0182376774` |
| `v3/checkpoints/B_1.v1.json` | `f91918d661b0ae74068b46d2103822adfe9a5d507666885571e94c2a89ea2a8f` |
| `v3/checkpoints/B_1_R_P3_B_A.md` | `4425c19ad9f64dbdee2b6cff4307594472c22534c20e26dcb4c2bdb26e19c2c9` |
| `v3/checkpoints/B_1_R_P3_B_A.v1.json` | `de2f77122e1e213d972934be520ffaac22520d38a04348d03866f11e8cc7aea5` |
| `v3/derivations/03_logical_uncertainty.md` | `8c5938d98f0605a833eefec90fd9c45901cc7096589cffd0d933f1e7b6440e8c` |
| `v3/derivations/07_selective_feedback.md` | `b8b79d95fcfde60f749fc4e872e38ae20d608a786462002660b97658597103cd` |
| `v3/derivations/07_observable_performance.md` | `178ed397b699c06da1056e0e660dd6e35c498def127dc6b54d4dc876e44f7a8f` |
| `v3/work_logs/R_P3_B_A_2026-10-09_S1/development/frozen_hard_answer_composition.md` | `21b2420d0b61176ffea258c7bcd56b6ab3d23bf9e3abd30722ca40c08d45fcc8` |
| `v3/work_logs/R_P3_B_A_2026-10-09_S1/reviews/proof_agent/frozen_hard_composition_review.md` | `c68c7ed9bb98d759ff4d70ab4536418c1b60dcb4be46eee24da8398cfd2a5dec` |
| `v3/checks/03_bounded_logic.py` | `841df6c5223844d2131642adcbb136855e054aa8833036506bb32c91aaf8afe6` |
| `v3/checks/07_computation_adapter.py` | `06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615` |
| `v3/checks/07_selective_feedback.py` | `f872ec2eb07df4722720763730932c33055e380f0ab76ddc3c848d79a5e70f48` |
| `v3/checks/07_selective_feedback_service.py` | `68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32` |
| `v3/checks/07_selective_feedback_allocation.py` | `eaf79ecb0c4b297ffeec3de4026a025fabc23058ec3c119abe5fdd23434da070` |
| `v3/work_logs/P3_08_2026-10-10_S1/forecast.json` | `cce049260f0d9245ffa211403b1d57397794510d849456459b4930e02ed3bd3a` |

**Disposition:** initial contract reconstruction complete. No inherited theorem
blocker found. Implementation correctness, actual resource bounds, generic source
checking, and the proposed tests await the new P3-08 files and execution.
