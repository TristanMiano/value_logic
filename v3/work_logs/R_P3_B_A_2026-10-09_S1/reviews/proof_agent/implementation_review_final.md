# Final v1.1 controller review

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Separate same-model, nonblind implementation reconstruction. Reviewer time is
unmeasured and adds zero principal credit. This review neither edits the root
controller nor consumes the separately planned development comparison batch.

**Verdict: PASS for the successfully completed, funded, trusted-local service
under the fixed-tape assumptions, with the zero-budget failure-metadata
qualification recorded below.** Both exact-state and fixed-state arithmetic
match their independently reconstructed theorems. No unresolved scientific
or successful-path implementation defect was found.

## 1. Exact source boundary

| Object | SHA-256 |
|---|---|
| Initial controller, preserved history | `2f718fdcc407994f0ab1d11e3ecc159e611ce724084170e8d5e7bc9fdd3353e1` |
| Reviewed controller `r-p3-b-a-blocked-prod-v1.1` | `d103cfdf9356c7e977df53c27bd57c26adc8df59a954c7c4dac2a0d537ad3af4` |
| Reviewed service `r-p3ba-euler-services-v1.2` | `68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32` |

The [final controller snapshot](implementation_source_final.py),
[final service snapshot](implementation_service_final.py), probe and manifest
bind this verdict. Earlier findings and their exact before-sources remain in
[the initial review](implementation_review_initial.md). A later exception-only
or documentation revision requires a distinct source binding; this review
does not silently relabel its evidence as that future version.

## 2. Initial findings disposition

| Initial finding | Reviewed disposition |
|---|---|
| Successful receipts used `success`, controller expected `answered` | Fixed. The controller accepts the exact local `ServiceResult`, successful status, checked integer answer, matching query/claim, named cold provider and source version. Complete runs succeed. |
| Missing `EXPERT_EVALUATION_CAP` in incomplete service module | Fixed in the reviewed service: the cap is $`64+9=73`$. |
| Invalid seed could follow paid startup without a meter-bearing exception | Fixed. Seed validation precedes meter creation or spending. The targeted diagnostic confirms no meter is created. |
| Bit-word initialization counted only one of validation and retention | Fixed. The initial envelope includes both word counts. |
| Sampler intermediates exceeded the broadly named numeric bound | Fixed. Prediction arithmetic, the separate 95-bit sampler bound and their maximum have distinct fields. |
| Final updated weights absent from the earlier working diagnostic | Fixed. Product and normalization intermediates update `peak_prediction_working_bits`; final persistent weights update `peak_weight_bits`. |
| Foreign meter accepted for the bit input | Fixed. The low-level constructor requires meter identity; rejection occurs before learner spending. |
| Issued record retains rounded probability | Correctly retained as an explicit scope condition. The supplied design/proof includes the issued-Brier allowance; the code has not silently relabeled $`q_t`$ as ideal $`p_t`$. |

The receipt checks bind trusted local data. They are not a cryptographic
authentication service for arbitrary external records, and no such stronger
requirement is imposed here.

## 3. State machine and exact arithmetic

The main broker owns the uniform selector and consumes it before a block.
It then calls a stateless public expert function and issues a dyadic forecast
and prospective action before making that query's purchase decision. The
selector flag is not supplied to the expert or prediction method. Within a
block, only the pending current action can be corrected by a purchased answer;
weights remain frozen until the last action closes.

The feedback slot contains the selected query's expert actions and checked
answer. It admits one receipt per block, and the broker's fixed loop provides
one selected position. A completed block requires that receipt. Successful
whole execution requires exactly $`m=T/b`$ admitted labels, consumed bit
capacity and no remaining query reservation. Receipts from failed calls are
charged before their lack of a checked answer rejects completion.

In exact-state mode, `_end_block` computes exactly
$`w'_i=w_i(K-\ell_i)`$. In fixed-state mode, it first computes those same
products, then uses the reviewed rule

```math
M=N2^s,\qquad
u_i=1+\left\lfloor\frac{(M-N)v_i}{\sum_jv_j}\right\rfloor,
\qquad R=M-\sum_iu_i,
```

adding one to each of the first $`R`$ indices. Its residual bound and positive
fixed mass agree with the [independent normalization proof](bounded_normalization_review.md).
The actual code was compared with a separate `Fraction`-based construction,
not only with its own output assertions.

The code admits the all-purchased singleton-block case as well. Its selector
uses zero bits, every current action is corrected, and there is no unbought
task loss; this is the trivial boundary of the theorem rather than a new
selective-learning claim. The executable broker fixes the service to its four
named experts. The lower-level arithmetic class has a broader bounded expert
count, still requiring its stated local API premises.

## 4. Both numeric and tariff bounds

Let $`z`$ be the declared prediction working-word bound. In exact-state mode,
individual weights are at most $`K^m`$. Their sum needs the additional
$`\lceil\log_2N\rceil`$ bits and the action numerator needs the additional
$`h`$ bits. The implemented formula includes these terms with slack.

In fixed-state mode, persistent weights are at most $`M=N2^s`$; products
and their sum are at most $`MK`$; normalization numerators are at most
$`M^2K`$; and action numerators are at most $`M2^h`$. The code's maximum
of the two corresponding bit formulas safely dominates all of them. The
separate 95-bit word-crossing sampler limit covers its finite extraction
intermediates. Monetary and index counters stay within the stated 64-bit
range.

The initial review's direct sum of named successful-path charges remains
valid with one additional per-round type-check unit. For the fixed-state
normalization, a further direct upper sum is

```math
C_{\rm normalize}\leq N(4z^2+17z+7)+2z+5.
```

This counts mass/slack construction, reading and summing products, full
integer multiplication and division, floor-plus-one construction, subtotal
and residual computation, and the fixed-index redistribution. It is dominated
by the code's added per-block allowance

```math
N(16z^2+32z+32)
```

for every admitted $`N,z\geq1`$. The rest of the conservative controller
envelope already dominates prediction, action, feedback, bit storage and
ordinary product updates. Successful calls add the separately reserved cold
service cap; optional source setup and the labeled development RNG charge
remain separate.

These bounds describe the declared operand-word tariff. They do not claim
Python CPU cycles or actual heap allocation. Comparisons should use the
recorded actual debits, not treat the conservative funding cap as realized
cost. The focused successful tests below omit optional source procurement;
their caps and totals therefore exclude that setup invoice explicitly.

## 5. Focused executable evidence

The [saved final probe](implementation_final_probe.py) independently
reconstructs the development bit words as one evaluator-side bit string. It
checks selector positions, action-bit chronology, rounded probabilities,
prospective actions, purchased corrections, final weights, count invariants
and meter sums. Private modular `pow` checks occur only in the evaluator
after whole-service execution and do not supply labels to the policy.

| Successful case | Rounds | Purchases | Actual controller units | Controller envelope | Peak weight bits | Peak prediction bits |
|---|---:|---:|---:|---:|---:|---:|
| Exact state, $`b=4,h=16`$ | 32 | 8 | 7,087 | 31,426 | 11 | 27 |
| Fixed state, $`b=4,h=s=16`$ | 32 | 8 | 7,963 | 33,986 | 17 | 37 |
| Exact-state multiword case, $`b=2,h=32`$ | 256 | 128 | 72,949 | 399,924 | 129 | 161 |

All **320 rounds** matched the independent reference. The first two cases
used identical selector and action-bit streams, as required for a matched
development comparison. The multiword case specifically checks that exact
state can cross both one- and two-word boundaries without invalidating its
integer or tariff bounds. These are diagnostic cases, not evidence that one
method is economically preferable on a final challenge.

The actual normalization function matched the independent rational reference
on **640 state/loss pairs**: 560 small-precision cases, and 80 high-precision
cases exercising 78-bit normalization intermediates against an 82-bit bound.
All positive-mass and final-weight bounds held. This is targeted arithmetic
evidence in addition to the general proof, not a universal theorem inferred
from finite tests.

For the failed-invoice path, the probe temporarily called the actual trusted
provider with a 20-unit child limit. That provider returned `budget_exhausted`
with **19 spent service units** and no admitted answer. The controller charged
the invoice, rejected completion, and attached the whole **1,763-unit** meter.
One future 1,088-unit query reservation remained, and no successful result was
returned. The local reduced-budget fixture is labeled; repository source was
not modified. This verifies that a failed query does not manufacture a free
label or erase earlier spending.

All probe checks passed with exit code zero and empty stderr. The
[saved output](implementation_final_probe.stdout.json) retains the detailed
contracts, hashes, counts and totals.

## 6. Zero-budget metadata qualification

There is one small failure-interface qualification in the reviewed source.
For `unit_limit=0`, the first one-unit funding check is denied before the
whole-service error handler. The resulting `BudgetExceeded` has no attached
meter. **Zero units have been spent**, no label has been acquired, and no
completion or performance guarantee is emitted. Thus this does not revive
the initial lost-paid-startup defect and has no theorem effect.

The [exact diagnostic](zero_budget_metadata_probe.json) preserves this case.
It qualifies the current docstring's unconditional statement that a declared
cap failure carries a meter. The root has explicitly retained this source
while its separate development batch runs and will either qualify that API
wording or attach the zero snapshot afterward. Any changed source version and
source-registration setup price must retain their own disposition. A broad
successful-path rerun is not justified by an exception-only metadata change.

## 7. Integration disposition

Accept the reviewed successful service with its fixed exogenous tape, named
expert library, one-purchase-per-block chronology, actual bill, and applicable
state/action/issued-forecast allowances. The scalar forecast and executed
stochastic action remain distinct outputs. The independent
[greedy-policy check](greedy_boundary_review.md) explains why replacing this
action rule by a deterministic value optimizer requires a different policy
assessment. That next-stage implication does not start P3-08.
