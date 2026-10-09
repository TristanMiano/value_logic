# R-P3-B-A: selective-label service and ordinary controls

Contributor: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-09 UTC.
Review: separate same-model, nonblind service-design assignment.
Base: `6ce7391b6a41c6c19397b00ce7b6a2d9b228b9a4`.
Stage: **DEVELOPMENT; proposed contract, no implementation or population run**.
Reviewer time is unmeasured and contributes zero to principal clocks.
The [source bindings](source_bindings.json) identify the inspected inputs.

## 1. Recommendation

**Reuse the existing finite modular-equality service for the first selective
feedback contract.** This isolates the new information and economic bridge
while retaining public exact computations, shortcuts and cache controls that
already limit the application claim. The recurrence can succeed by deriving
the requested guarantee and establishing a precise economic obstruction on
this scope. A favorable number against a deliberately expensive label provider
would not alone establish useful mathematical learning.

Use the 248 queries from P3-07:

```math
q=(p,a),\qquad p\in\{17,31,47,61,97\},\quad 1\le a<p,
\qquad y(q)=\mathbf1\{a^{(p-1)/2}\equiv1\pmod p\}.
```

The full mathematical inputs are public. The immutable adapter record also
contains the target residue 1, source and semantics versions, and a request
identifier. A new request identifier does not make an old mathematical key
fresh. A predetermined tape of these queries is adequate for the finite
selective-feedback theorem; no IID law is needed for that purpose. Any
population claim would need its separately stated law.

Avoid reusing P3-06's outcome-balanced generator as an unexplained natural
distribution. Its source explicitly computes a residue and chooses the target
to produce a selected label. That is legitimate saved development evidence,
but a new learning application should not inherit an unstated distributional
interpretation from it.

## 2. Concrete public/private boundary

| Boundary | Permitted contents and operation |
|---|---|
| Immutable contract | Mathematical/source versions; full fixed expert code; bounded action/loss rows; horizon and blocks; exact quota in each block; query and action randomness rules; price vector; initial retained state; receipt and numeric caps. |
| Public query | Complete modular claim and request identity. No evaluator-only label, diagnostic residue, answer-dependent generator metadata, or scoring record is passed to the learner. Public inputs may of course support paid exact inference. |
| `issue(query)` | Read public inputs, evaluate the fixed experts, and commit a prospective distribution/action and its block-weight identity before that round's purchase flag or answer is exposed. Every computation and retained record is priced. |
| Purchase broker | Hold a uniformly selected exact-size subset of the current block. Accept only selected immutable issue identities. Invoke a real solver/service, return a bound receipt only after its required work, and debit the actual resource bill. |
| Terminal action | Use the purchased answer on selected rounds when both correct binary actions are available. Otherwise use the previously committed prospective action. Log both actions; do not rewrite the issued forecast. |
| Block update | At block end, pass only purchased receipts, their public queries and already issued expert predictions to the update. Weights stay frozen within the block. |
| External evaluator | After the learner transcript is closed, compute all labels and all-issued scores privately. It cannot feed its unbought answers or diagnostics into the learner. |

The minimal fixed library can contain constant 0, constant 1 and explicitly
specified public-input heuristics. If an expert learns from history, that is a
different comparator contract: it is not automatically a fixed expert whose
losses are the same on the learner's and a counterfactual policy's histories.
The existing P3-06 residue-frequency expert updates from receipts, so it should
not be silently imported as a fixed public-input function.

Known same-scope residues can be reused after paying admission, lookup and
storage costs. For the simplest first implementation, new receipts may be
retained for the next block; all methods must nevertheless be allowed the
same public cache capability. If same-block receipt reuse corrects an
unselected duplicate, distinguish that licensed deduction from evaluator
feedback. It only improves actual nonnegative classification loss relative to
the uncorrected action, but its timing and resource charges still need a
stated extension. A first implementation may deliberately omit a cache; the
ordinary cached control must not then be excluded.

**Decision loss and forecast loss are different records.** Buying the answer
before acting can make terminal classification loss zero. It cannot erase the
Brier or log loss of an immutable forecast already issued before purchase.
The current-action improvement belongs in the decision theorem.

## 3. Exact quota, variable cost and hard limits

Let a block have length B and purchase exactly k positions, with
q = k/B. Draw a uniform k-subset independently of the tape and the block's
frozen expert mixture. Distinct positions in this sample are dependent; its
marginal inclusion probability is q. A proof using block-level unbiasedness
does not need to pretend those positions are independent Bernoulli draws.

The deployed development seed is a reproducibility device. It is not evidence
that the probability theorem's independent random sampling premise is true
of a deterministic pseudorandom trace. A tiny exhaustive subset calculation
can check finite algebra without being presented as a fresh population study.

Exactly k purchases is a hard **service-call count**, not a hard resource bill
and not a bound on all knowledge obtained through mathematical deductions.
If a checked completion is bounded by C_max under the fixed tariff, reserve
k C_max before opening the block and debit actual charges. A denial or timeout
must preserve its spent cost and emit the stated unresolved action. Do not
spend refunds on extra adaptively chosen labels under the original proof.

The existing adapter exposes a loose cold-completion bound of 1,024 units and
a warm bound of 2,048, exclusive of the controller's own work. These constants
are source-bound and are not physical-time estimates. Its actual arithmetic
cost varies with the public exponent and shortcut class. A uniform sample
with inclusion probability q has expected purchase cost q times the sum of
the fixed per-query completion costs; its realized cost must still be logged.

Use either a provider fee covering solve/check/acquisition/storage or the
priced primitive resource vector. Do not charge both for the same work, and
do not treat controller computation as included in a provider's fee unless
the service contract actually includes it. Input admission, random sampling,
expert evaluation, numerical updates, receipt checking, retained state and
terminal output require declared prices. Harness-only final scoring remains
separate and unavailable to the policy.

## 4. Ordinary controls that matter

| Control | Required service and fair comparison |
|---|---|
| Ordinary label-efficient weighting | Same experts, selective receipts, quota, information histories and charged computation. Identical outputs are an expected ordinary equivalence, not a defect. |
| Fixed actions and public shortcuts | Constants 0 and 1, any specified fallback, and the actual elementary modular identities. Prefix and output costs are included. |
| Fast direct exact action | Public efficient binary modular exponentiation, including input, arithmetic and action emission. For an action-only endpoint it need not buy the learner's second independent check. P3-06 already admits this control. |
| Checked always-BUY | The existing P3-07 efficient producer plus independent checker, admission and acquisition. This is an equal checked-receipt service comparison. |
| Exact semantic cache | Retain a residue under its mathematical/source key, then answer changed targets or repeated request identities by paid lookup and comparison. Allow the same capability to every controller. |
| Ordinary analytic label table | Construct quadratic-residue membership tables directly from public mathematics, then pay lookup costs. This is stronger for repeated use than only comparing against P3-07's general catalogue-profile construction. |

For the last control, build the set of residues j squared modulo p for
1 <= j <= (p-1)/2 for each of the five primes. This needs **124 square/reduce
evaluations in total**, plus prime/source checks, initialization, storage and
per-query lookup. No claim about total charged units or runtime follows from
that arithmetic count alone.

Here is the source-specific proof. Multiplication by a nonzero residue
permutes the nonzero residues, so cancellation of their product gives
x^(p-1) = 1. Each nonzero square is therefore a root of
z^((p-1)/2) - 1. There are exactly (p-1)/2 distinct nonzero squares:
x squared equals z squared in a prime field precisely when x = z or x = -z.
A degree-(p-1)/2 nonzero polynomial has at most that many roots. Thus the
square table contains every positive answer and no negative answer. Restricting
j to the indicated half-range lists exactly one representative of each pair.
The root-count and prime assumptions agree with P3-07's existing analytic
companion; the implementation must pay or explicitly inherit their admission.

This table's answers are inferred from public structure, not leaked private
labels. A budget that forbids the table merely because it finds many answers
would change the task from computation-cost comparison to a constrained
oracle game. Either game can be defined, but they answer different questions.

## 5. Honest positive or negative evidence target

For classification with a block-frozen prospective mixture, fixed tape and
fixed per-query checked cost c_t, selected answers correct terminal loss to
zero. Conditional on earlier blocks, sampling is independent of the current
prospective losses. In the no-cache-correction case the expected total is

```math
\mathbb E[J_T]
=(1-q)\mathbb E[L_T^{\rm prospective}]
 +q\sum_{t=1}^{T}c_t+\mathbb E[O_T]+S.
```

This identity is a proposed integration target; the principal's final theorem
must bind the actual chronology and any rounding allowances. A valid
expert-relative upper bound can be substituted for the prospective-loss
term. Variable blocks require their own q_b factors instead of pulling out
one common q. Correcting additional cache-known rounds gives an upper bound
unless their improvement is included explicitly.

Against the same checked always-BUY service, the expected gap is

```math
(1-q)\left(\mathbb E[L_T^{\rm prospective}]
                  -\sum_t c_t\right)
 +\mathbb E[O_T]-O_T^{\rm BUY}+S-S^{\rm BUY}.
```

This exhibits both mechanisms: labels saved can repay imperfect decisions,
while learning overhead can erase the saving. A sufficient dominance
obstruction, independent of the labels, is that excess controller/setup cost
already exceeds the cost of all skipped completions; nonnegative task loss
then cannot rescue the learner. An exact table control can produce a much
stronger obstruction on this particular public finite family.

A positive development finding should identify the named baseline and price
region, include every setup/ongoing cost, and survive the cheap exact and
analytic controls. A useful theorem whose positive region is displaced by
the ordinary table still supplies the selected-feedback bridge; it does not
establish an economical application gain on these 248 queries. Retain that
negative conclusion rather than increasing provider prices or slowing a
solver to manufacture a win.

## 6. Why not introduce a combinatorial family now?

A bounded SAT or subset-sum service is a legitimate mathematical question,
but it adds solver trust, input distribution, pre-processing, repeated-query
compilation and heuristic comparison to the selective-feedback recurrence.
At small bounds, brute-force tables, bitsets, dynamic programming, unit
propagation or cached symbolic compilation may remove its apparent difficulty.
P3-05's ordinary ADD results already show why this is a substantive comparison
problem. Merely moving to a combinatorial name would not resolve it.

If the derived bound identifies a credible regime requiring expensive
resolution and useful cross-query predictive structure, a separate later
application can select such a family prospectively and audit the ordinary
solver before choosing instances. No such family or new population is selected
by this review. The present recommendation is to complete the contracted
learning/cost bridge on the existing service and report its actual scope.
