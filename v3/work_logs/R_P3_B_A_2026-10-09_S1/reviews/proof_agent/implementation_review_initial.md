# Initial controller audit against the selective-feedback theorem

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Separate same-model, nonblind review; unmeasured reviewer time adds zero
principal-clock credit. This preserves the initial implementation assessment
and does not overwrite the independent [proof review](review.md).

Reviewed controller: `v3/checks/07_selective_feedback.py`, SHA-256
`2f718fdcc407994f0ab1d11e3ecc159e611ce724084170e8d5e7bc9fdd3353e1`.
The exact source is retained in [the initial snapshot](implementation_source_initial.py).
The dependency at the executable diagnostic had SHA-256
`68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32`.

**Initial verdict: BLOCKED pending the concrete interface and error-reporting
repairs below.** The mathematical state transition is otherwise consistent
with the reviewed theorem under the trusted local provider, fixed public
expert and exogenous-tape scope. Successful integration has not been inferred
from an in-memory diagnostic shim.

## 1. Findings that require disposition

| Finding | Initial evidence | Required disposition |
|---|---|---|
| Successful receipt rejected | `close` requires status `answered`; the checked service returns `success`. An actual checked receipt is rejected after its invoice is charged. | Align the source-bound status contract and rerun one complete service path. |
| Missing expert evaluation cap at first inspection | `execute` reads `S.EXPERT_EVALUATION_CAP`; the concurrently written initial dependency did not define it. | The dependency had added it by the saved executable diagnostic. Bind the completed source closure, not the earlier partial module. |
| Startup spending omitted from invalid-seed exception | Seed validation occurs in `BitTape.seeded`, after funding and optional setup, outside the `execute` error handler. The focused diagnostic incurred 1,001 units and raised `Rejected` without an attached meter. | Validate the seed before spending, or include all paid startup in the error handler. |
| Bit storage initialization understated locally | `BitTape` pays one word for validation and another for retention; the named initial cap includes only one word count. | Include both counts explicitly. The root had identified this correction before this review. |
| Numeric bound named too broadly | A two-round, two-position, 32-action-bit contract has `working_bits=38`, while a permitted cross-word extraction transient is 95 bits. | Name the bound as prediction/weight arithmetic and give the sampler's separate constant bound, or take their maximum. |
| Issued forecast is rounded | `Issued.numerator/denominator` stores dyadic $`q_t`$, not ideal $`p_t=U_t/W`$. | Include $`2T2^{-h}`$ in the all-issued Brier bound, or separately retain and price the exact ideal forecast. |

The low-level `FrozenProd` constructor also accepts a `BitTape` owned by a
different meter. The main `execute` path constructs the correct shared meter,
so this is not a demonstrated defect of successful whole-service execution.
Either explicitly restrict the theorem to that broker or reject mismatched
meter ownership in the low-level constructor. No authentication of arbitrary
external or maliciously forged Python records is requested by this review.

## 2. Correct state and randomness structure

`execute` admits a complete tuple whose length matches an equal-block
contract. The contract restricts block size to a power of two. At block start,
the broker consumes exactly $`\log_2b`$ selector bits before issuing any
request. It does not pass the selector flag to `issue` or to the stateless
expert function. Each round computes public expert actions, issues the
rounded probability and its prospective sampled action, and only then calls
the paid service if that position was selected.

`FrozenProd.close` replaces the current terminal action by the checked answer
on the bought round. It retains only that round's expert actions and label.
Weights are changed by `_end_block` after the last round closes; no current
block prediction depends on the bought label. The sampled query provides
the full selected loss vector, and the multiplication factor is exactly
$`K-1\{a_i\ne y\}`$. `block_mass` is computed before the block and remains
valid because the weights are frozen.

The focused diagnostic adapted only the receipt status spelling in memory
to examine transitions after the separately detected interface error. The
weights stayed unchanged after buying the first of two rounds, changed to
the predicted product weights only after closing the second, and the
feedback slot was cleared. This supports the chronology; the shim does not
make the initial source a successfully integrated implementation.

The feedback slot rejects a second receipt in one block. Finishing a block
without a receipt raises, and overall successful completion requires exactly
the contract quota. The broker's fixed nested loops cannot create additional
query positions from a refunded reservation. A duplicate close cannot operate
on a different object: it requires the exact pending issued record.

Distinct selector and action reads consume disjoint ranges of the supplied
bit tape. The total is

```math
m\log_2 b+Th.
```

Drawing a prospective action on a bought round is deliberate: its output is
issued before the answer and then superseded for execution. The seed source
is labeled deterministic development; the code does not establish independent
fair bits by running one seed. No private evaluator answer is passed into
the learner. The service's four experts are fixed functions of public input.

## 3. Integer widths and the conservative tariff envelope

After $`m`$ updates, individual weights are at most $`K^m`$. A bound
$`1+m\lceil\log_2K\rceil`$ is therefore sufficient. Their sum and the
numerator selected by current expert actions need the additional
$`\lceil\log_2N\rceil`$ allowance. Shifting by the action precision adds
$`h`$ bits. The controller's arithmetic formula includes these terms and two
extra bits. The integer division is exact, with no floating-point exponential
or probability approximation hidden in the update.

For the admitted Euler family, the semantic key occupies nine declared
64-bit words. Let $`z`$ be the controller's prediction working-word bound,
$`n=N`$, $`h`$ the action precision, $`r=\log_2b`$, and $`I`$ the supplied
bit-word count. A direct sum of the named successful-path charges is bounded
as follows, keeping the feature function's separately supplied cap:

```math
\begin{aligned}
C_{\rm initial}&\leq33+n+2I,\\
C_{\rm round}&\leq85+5n+3nz+6z+2z^2+h+18+C_{\rm feature},\\
C_{\rm block}&\leq49+9+6n+7nz+z+r.
\end{aligned}
```

The initial expression includes the whole-service funding check, bit
validation and retention, and learner initialization. The development MT
state and generated-word charges are separate. Round charges cover issuing,
prediction, dyadic execution, output and ordinary close; block charges cover
mass construction, one feedback receipt, final weight updates and selector
extraction. These are tariff bounds, not CPU or Python-heap bounds.

After correcting the missing second $`I`$ in its initial term, the proposed
controller envelope

```math
\begin{aligned}
1024+4nz+2I
&+T(512+C_{\rm feature}+16nz+8z^2+8h)\\
&+m(512+32nz+8r)
\end{aligned}
```

dominates those expressions for the admitted $`n,z,h\geq1`$. It is quite
conservative; an oversized cap must not be substituted for actual debits
when reporting observed economic performance. The separately reserved cold
purchase cap and source-registry setup are additional components.

`peak_working_bits` currently observes the block mass and shifted prediction
numerator. It does not observe the last block's updated weights or the
sampler's transient concatenation. Keep that diagnostic's meaning precise;
the independently bounded weight and sampler fields can cover those other
objects. The cap derivation does not quantify harness transcript retention,
JSON serialization or physical memory outside the stated tariff model.

## 4. Reservations, failures and retained spending

The broker reserves the complete cold-service quota before running the
learner. A completed child invoice must have matching operation/category
totals and fit one funded call cap. Redemption releases one call's cap and
debits its actual work. A smaller actual invoice leaves funds available but
does not create another selector or query slot.

Underfunding the total declared service is rejected before query execution,
after one explicitly charged funding check. A failed checked service still
has its actual invoice absorbed before `close` rejects its unsuccessful
answer. In the saved receipt-status diagnostic, the valid service invoice
cost 114 units; the controller then spent another 65 units admitting and
rejecting the mismatched receipt. The pending issue remained present and no
completion was claimed. These costs were not refunded.

The existing loop error handler retains a meter snapshot, closed-round count
and purchase count. Its placement misses paid startup errors. The invalid
seed diagnostic isolates this defect using a labeled conservative feature-cap
fixture and an observing meter constructor: the rejection occurs after a
1,000-unit supplied setup invoice and one funding unit, without preserving
the resulting meter on the exception. No mathematical label was acquired in
that diagnostic.

A denied `_end_block` can leave some tariff charges and audit peak updates
while the new weight tuple is still uncommitted; the whole-service broker
then stops and records failure. The theorem is for successfully completed,
funded executions. It is not a claim that a failed arbitrary prefix retains
the successful learner's regret guarantee.

## 5. Evidence and next review boundary

[The diagnostic source](implementation_initial_probe.py) and
[its saved output](implementation_initial_probe.stdout.json) preserve the
observed failures and the explicitly labeled status and cap fixtures.
The original controller is unchanged. No final experiment or broad
regression rerun was performed.

Re-review the final controller/service source closure after the concrete
repairs and any bounded-state update have been integrated. At that point,
one successful complete path, a metered failure path, the actual final
arithmetic update and its corresponding theorem should determine acceptance.
The initial evidence remains historical evidence of what was found and fixed.
