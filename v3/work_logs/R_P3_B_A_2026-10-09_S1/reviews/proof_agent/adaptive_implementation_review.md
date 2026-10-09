# Independent review of the paid allocation implementation

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. Task R-P3-B-A.
Same-model, nonblind, independently assigned reconstruction. This review and
its probes receive **zero principal research-clock credit**. No policy source,
experiment, plan, ledger or publication was changed by this reviewer.

## Verdict and exact source boundary

**PASS for the successful, funded, trusted-local `execute()` service.** The
implemented propensities, delayed update, finite arithmetic, complete block
lookahead, exact bit consumption and exact purchase quota implement the
reviewed remaining-action estimator. The saved focused checks agree with an
independent `Fraction` reconstruction. A genuine failed provider invoice is
paid and retained before its unsuccessful answer is rejected.

The lower-level `prepare_block`/`issue`/`close` interface requires a truthful
broker to supply the actual selected position and ticket multiplicity. It is
not an independently enforced allocation protocol. This is a material API
precondition, **not a failure of the reviewed `execute()` path**. See §5.

| Source | Reviewed SHA-256 |
| --- | --- |
| `v3/checks/07_selective_feedback_allocation.py`, allocation v1 | `eaf79ecb0c4b297ffeec3de4026a025fabc23058ec3c119abe5fdd23434da070` |
| `v3/checks/07_selective_feedback.py`, core v1.2 | `f872ec2eb07df4722720763730932c33055e380f0ab76ddc3c848d79a5e70f48` |
| `v3/checks/07_selective_feedback_service.py`, service v1.2 | `68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32` |
| Preserved core v1.1 | `d103cfdf9356c7e977df53c27bd57c26adc8df59a954c7c4dac2a0d537ad3af4` |

The local source snapshots, `adaptive_review_start.json`, and
`core_v1_1_to_v1_2.diff` preserve the reviewed versions. This review also uses
the preserved `adaptive_quota_mathematics_reviewed.md`,
`allocation_exploration_reviewed.md`, and
`deployment_bound_design_reviewed.md`; later additions to the last design
receive a separate mathematical review.

## 1. Mathematical target and implemented factors

There is one fixed, deterministic, finite mathematical-query tape of
`T = mB` requests and a fixed source-defined library of four binary experts.
All full-tape loss rows are fixed independently of the supplied random bits.
The current block's public requests and public expert advice are available
before selection. The block distribution may depend on prior settled labels
and this public lookahead. It may not depend on current unpurchased labels.
Weights are held fixed for all `B` issued forecasts and prospective actions.
Exactly one selected label is bought, checked, and used as the terminal
action there. Its expert-loss update occurs only after the block closes.

Let `p` be the frozen expert mixture, `J` the sampled position, and
`pi_j = Pr(J=j | past, current public block)`. The estimator is

`X_i = (1/pi_J - 1) ell_{Ji}`, with `Z_i = X_i/H`.

When `pi_j >= 1/(H+1)`, `0 <= Z_i <= 1`. Conditional expectation gives

`E[p dot X] = sum_j (1-pi_j) (p dot ell_j)`,

which is the expected ideal mixture loss on the unbought positions.
The policy update uses `w_i (1 - Z_i/K)`, followed by the reviewed fixed-mass
normalization. With `K >= max(2,H)`, the usual quadratic Prod argument gives
the comparator coefficient

`1-pi_j + (1-pi_j)^2/(HK pi_j) <= 1`.

Indeed, subtracting the first term reduces this to
`((1-pi_j)/pi_j)^2 <= HK`; the left side is at most `H^2`.
The guarantee against any fixed expert, and hence the deterministic full-tape
best expert, is therefore

`E ideal_terminal_loss <= L* + HK log N + HKm/(2^s-1)`.

For dyadic action sampling add `(T-m) 2^-h`. This is an expectation under
fresh independent uniform supplied bits, not a pathwise regret claim or a
claim that one deterministic MT development seed is a random-bit proof.

The allocation code assigns one ticket to every position and another `B`
tickets to the public favorite. Thus the favorite has `(B+1)/(2B)`
probability and every other position has `1/(2B)`. It sets `H=K=2B-1`.
The update factors are exactly:

| Selected position | Gamma in `1-gamma*ell` | Source integer multiplier |
| --- | --- | --- |
| Nonfavorite | `1/H` | `H-ell` |
| Favorite | `(B-1)/[(B+1)HK]` | `(B+1)HK-(B-1)ell` |

The source's reduced nonfavorite denominator and larger favorite denominator
therefore represent precisely the same rational update as the theorem.
Neither cost-proxy values nor realized invoices enter this probability
correction. Proxies guide selection; the actual child invoice is paid in full.

## 2. Chronology, scalar forecasts, actions and normalization

`execute()` calls `prepare_block()` once per complete block. That method
evaluates and charges all `B` public advice rows, computes each disagreement
score `positive_mass * negative_mass`, and compares score/proxy ratios by
exact integer cross-products. Strict improvement retains the first maximum.
Only after completing this lookahead does it consume a selector draw from
`0,...,2B-1`. Draws `0,...,B-1` select that position; the remaining draws select
the favorite. The resulting probabilities are exact because admitted `B`
is a power of two.

The immutable cached advice is then supplied to the inherited `issue()`.
No current receipt is available while its own forecast is issued. The source
does not pass a buy flag to `issue()`. Every round consumes its declared `h`
action bits, including a round whose prospective action is later corrected
by a purchased answer. Buying early in the block stores one feedback row;
it does not change any later forecast in that block. The inherited last-round
close dispatches to the allocation update only after all actions have issued.

The inherited scalar is the **emitted dyadic probability**
`q=floor(2^h * positive_mass / total_mass)/2^h`. The ideal mixture `p` is
used in the mathematical potential; the trace stores `q`. A fresh `h`-bit
integer sampled below its numerator implements a Bernoulli action with
parameter exactly `q`. The difference from ideal mixture loss is at most
`2^-h` per unbought position. Selected terminal actions use the checked label,
without changing the already-issued scalar or prospective action record.

The fixed mass is `M=N*2^s`. For integer positive update products `v_i`,
normalization forms `1+floor((M-N)*v_i/sum(v))` and gives the residual, which
is in `[0,N-1]`, to the first indices. It preserves positive weights and
total mass `M`, and satisfies the one-sided posterior inequality

`p'_i >= (1-2^-s) * v_i/sum(v)`.

The resulting potential allowance is
`HKm log(1/(1-2^-s)) <= HKm/(2^s-1)`. In particular, the fixed-state rounding
term remains necessary; exact integer execution does not remove it.

The 16-round native trace in `adaptive_implementation_probe.stdout.json`
independently reconstructs every favorite, selected position, ticket count,
emitted probability, action draw, paid answer, and final weight. The observed
call sequence contains all four public advice calls before the first issue
in every block. Weights recorded before every issue agree with the frozen
reference. Explicit supplied-bit cases separately exercise both ticket
branches, including a favorite at index 2 rather than index 0.

## 3. Arithmetic and complete lookahead capacity

Write `w = s + ceil(log2 N) + 1` and `D=(B+1)(2B-1)^2`.
The implemented persistent-weight bound is conservative: every weight is at
most `M`, so its bit length is at most `w`. The largest relevant positive
integer numerators are bounded by:

| Operation | Upper bound |
| --- | --- |
| Unnormalized update product | `MD` |
| Normalization numerator | `M^2 D` |
| Sum of update products | `MD` |
| Disagreement times proxy | `304 M^2` |
| Dyadic forecast numerator before division | `M 2^h` |

The declared `max(2w+max(bit_length(D),bit_length(304))+2, w+h+2)` therefore
covers each such operand. Its word count `z` bounds the operands appearing
in the controller's integer tariff. At `B=1024`,
`D=4B^3-3B+1=4,294,964,225`, which has 32 bits and fits the single-word
factor premise. The source's separate 95-bit bit-extraction bound is still
needed: a cross-word extraction can temporarily hold more bits than the
forecast arithmetic. Counter and resource indices remain below 64 bits in
the admitted finite execution.

The six deliberately selected valid arithmetic states at `B=1024`, `s=h=32`
include both propensities and concentrated as well as uniform weights.
Every update matches an independent exact-rational posterior normalization.
The observed largest operand is 100 bits, within the declared 104 bits.
This is an arithmetic diagnostic, not a claim to have run an additional
1024-round scientific arm.

All admitted source queries have `key_words=9`. The actively retained
lookahead accounting is `B*(9+N+words(score)+5)` in the worst case, which is
within the declared `B*(128+N+4z)`. Cached advice is computed once per position
and reused; the cap still pays for all `B` evaluations. The native probe's
peak active block buffer is 76 words, below its 544-word cap.

This buffer bound concerns the declared abstract charged policy buffer.
Preloaded input bits, the public tape supplied to `execute()`, and the saved
audit/output records are distinct objects and scale with horizon. A fixed
weight precision does not establish constant total memory in `T`. This
review does not identify the word tariff with Python object bytes or physical
processor cycles.

## 4. Sufficient charged cap and error spending

The cap can be checked symbolically, rather than inferred from the small
probe. Let `n=N`, `z>=1` be the declared working-word bound, `r=log2(2B)`,
`q=9`, and `I=ceil(random_bits/64)`. Summing the source's named charges gives
the following conservative upper envelopes for successful trusted execution.
Move the block output's `3B` term and the active buffer release into the
per-round envelope; charge public advice once at its admitted cap 73.

| Portion | Upper envelope for actual controller debits | Source allowance |
| --- | --- | --- |
| Initialization, including first funding check and both bit-word charges | `49+n+2I` | `2048+4nz+2I` |
| Per round: public lookahead/advice, issue/close, proportional output and buffer release | `111+4q+73+9n+6nz+20z+4z^2+h` | `1024+73+80nz+40z^2+8h` |
| Per block: selector, block mass, one successful receipt admission, update, fixed-mass normalization and remaining output | `98+q+3z+4nz^2+24nz+15n+r` | `1024+16nz^2+64nz+32n+8r` |

For `n,z>=1`, every source allowance dominates its corresponding actual
envelope. This includes the denominator-dependent arithmetic through `z`,
the full public lookahead, residual normalization work, and the one receipt's
extra propensity admission. Thus no provider bill or lookahead cost is
silently assumed to be part of a free side channel.

The controller cap is separate from any trusted setup invoice, the full
`1088m` purchase reservation, and the development generator allowance
`1248+I`. Actual receipts redeem one cap at a time; refunds do not create
new positions. On successful completion the reservation is empty, exactly
`m` labels have been accepted, and bit consumption is exactly
`m log2(2B)+Th`. These are hard finite resource/count properties under the
declared tariff. The loss guarantee remains an expectation.

The native 16-round diagnostic spent 5,523 controller units against a 33,418
controller allowance. Its four actual service invoices total 888 units; the
development generator costs 1,253 units. Total spending is 7,664 against the
funded 39,023-unit cap. Operation sums, category sums and invoice sums agree.

For a deliberately underfunded *child* call, the test invokes the real trusted
provider with limit 20. It returns a `budget_exhausted` invoice for 19 units.
The outer broker absorbs all 19 before core receipt validation rejects it.
The attached outer meter retains 2,151 total units, zero accepted labels,
and the remaining future 1,088-unit reservation. No success result or
successful-learning guarantee is returned. This is a focused error-accounting
check, not an externally forged-record test.

## 5. Low-level allocation API qualification

`prepare_block()` returns the selected index and its ticket multiplicity but
does not bind them into an internal allocation state. `close()` checks only
that a supplied multiplicity is an integer in `{1,B+1}`. Also, no prepared
flag prevents a caller from preparing the same unopened block more than
once. Consequently, arbitrary direct callers must not claim the execution
theorem merely because the low-level methods returned successfully.

The saved diagnostic makes this boundary concrete. A valid all-ones selector
chooses favorite index 2 with five tickets at `B=4`. Supplying one ticket
instead of five is accepted by low-level close. It produces final weights
`[58255,67963,67963,67963]`, rather than the correctly corrected weights
`[64933,65737,65737,65737]`. This demonstrates that actual ticket truth is a
caller precondition; shape validation is insufficient to establish it.

The reviewed `execute()` supplies exactly the returned multiplicity to the
one returned selected index and prepares each block once. It therefore
satisfies that precondition. If an independently safe public allocation API
is later promised, store and enforce the prepared block, selected position,
actual tickets and one-use lifecycle. That extension is unnecessary to
certify the present trusted broker. Arbitrary forged Python records and
authenticated remote services are outside this local-service claim.

## 6. Core v1.2 guard disposition

The preserved diff from core v1.1 contains only the version string and a
`try/except BudgetExceeded` around the first one-unit funding charge. The
handler attaches the meter snapshot before re-raising. Every successful
operation, action, check, invoice, update and tariff formula is unchanged.

An independently loaded 16-round, fixed-state native case at seed 23 produces
identical complete returned structures after normalizing only the core
version strings. Both spend 6,140 operational units. The canonical trace
digest is `159405288da7c7f4fe7151fdacfe53769d58f9aa639ec067a9f4fd35e8670304`.
At zero funding, v1.1 lacks the snapshot and v1.2 supplies it with total zero
and one denied charge. This resolves the prior metadata limitation without
changing any successful trace or theorem.

Source-registry setup is deliberately excluded from that operational trace
comparison. The implementation bytes differ and a registry that prices bytes
must invoice each real version's source. Version metadata also differs.
Earlier v1.1 evidence remains evidence for its preserved source; it must not
be silently relabeled as a newly priced v1.2 experiment.

## 7. All-issued forecast bridge and source-known deployment envelope

The old uniform identity multiplying selected loss by `B` does not transfer
to a nonuniform selected position. There is, however, a valid direct bound.
For every selector realization, the full ideal mixture loss is its ideal
unbought loss plus the `m` selected ideal losses, each at most one. Binary
Brier loss of the ideal scalar is at most its mixture classification loss.
The Brier function is 2-Lipschitz on `[0,1]`, so the emitted dyadic scalars
satisfy

`E sum Brier(q_t,y_t) <= min(T, L*+HK log N+HKm/(2^s-1)+m+2T 2^-h)`.

Here the ideal unbought loss means the sum of mixture losses, equivalently
conditional expected prospective action loss; it is not the sampled mistake
count on one development trace. The bound does not need a second action
rounding term: the `2T 2^-h` term already treats the scored scalar.
Purchased forecasts remain their original pre-receipt records.

The source contains both constant binary experts. Their full-tape losses sum
to `T`, so `L*<=T/2` is available from source alone without evaluating a
single mathematical label. Substituting this upper bound gives a valid
prospective numerical expectation certificate; exact private-evaluator
`L*` remains a retrospective refinement. The resource cap is pathwise;
source-known loss bounds remain expectations and can additionally be clipped
at the hard maxima `T-m` for terminal mistakes and `T` for all-issued Brier.

## Evidence and completion

`adaptive_implementation_probe.py` and its saved JSON/stdout and empty stderr
are the focused supporting evidence. They do not create new comparison arms
or select parameters using outcome search. The accompanying manifest binds
this report, exact source snapshots, diff and probe results. No P3-08 work,
historical-clock inference, repository publication or broad experimental
rerun was performed by this reviewer.
