# P3-01 — what a cost-space learning criterion would need to say

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Status: **exploratory contract probes**, within P3-01. No learning algorithm
or phase-three theorem programme is selected by this note.

The [main contract](01_problem_contract.md) separates predictive and decision
duties. The following elementary arguments make that separation sharper. They
are comparison diagnostics, not claims of mathematical novelty.

## 1. A change from truth-payoffs to failure costs can be exact recoding

Fix Boolean sentence-payoffs `y_phi(W)` and quotes `p_t(phi)` in `[0,1]`.
For this diagnostic define failure-cost payoffs and corresponding quotes by

$$
c_\varphi(W)=1-y_\varphi(W),\qquad
v_t(\varphi)=1-p_t(\varphi).
$$

A signed position `a` in the original payoff has marked-to-world gain
`a(y_phi-p_t(phi))`. A position `b=-a` in the cost payoff has gain

$$
b(c_\varphi-v_t(\varphi))
=(-a)((1-y_\varphi)-(1-p_t(\varphi)))
=a(y_\varphi-p_t(\varphi)).
$$

The equality holds term by term, hence for every finite portfolio, every date
and every world in the same assessment set. It preserves lower and upper
wealth bounds. The inverse is the same sign reversal. This is a transformation
of payoff functions on the **original Boolean worlds**, not a claim that
complementing every truth coordinate preserves the original connective rules.
The constructed quote `v_t(phi)` need not equal the original market's separate
quote `p_t(not phi)` at finite times.

Transport the operational contract as well: allow signed positions, or carry
each original constraint through `b=-a`; transport cash/collateral requirements;
and preserve price access and computational restrictions. The expression
language must permit constant subtraction and sign reversal with their stated
computational cost. Under those conditions the no-exploitation property is
the same property in this cost notation. The underlying selected definitions
are S01 §§3.4–3.5, not a newly imported learning theorem. If original belief
states use finite support and default zero, the encoded cost states use default
one; demanding default zero on both sides changes the representation contract.

This is stronger than observing that a scalar expected cost encodes one
probability: it identifies the additional operational conditions needed to
call the *criterion* equivalent. If positions cannot be shorted, the cost
payoff is not tradeable, the assessment worlds change, or the representation
requires an expensive new decoder, the stated correspondence no longer follows.
Signed coefficients here describe contracts; they are not a claim that an
agent can freely execute every negative-cost physical action.

The marked-gain identity is an external mathematical comparison of criteria,
not an implementation of every expressible trader or the LI construction in
the inherited native verifier. Core §3 permits negative rational scaling and
subtraction. Products between jointly variable quantities have the separate
[representation boundary](01_representation_boundaries.md); this recoding
does not bypass it.

The pure coordinate change supplies no improvement by itself. It can still
be useful as a transparent interface to a value-first presentation. A future
advance must identify another duty, construction, guarantee or application.

## 2. Charging costs changes the criterion, sometimes dramatically

Consider a different, explicitly defined market diagnostic. Each elementary
claim pays either zero or one, every quote is `1/2`, and a trade of signed size
`a` incurs a fee `s|a|`, with fixed `s>=1/2`. Its gain is

$$
a(y-1/2)-s|a|\le |a|/2-s|a|\le0
\qquad (y\in\{0,1\}).
$$

Summing shows that every portfolio's marked net gain is nonpositive at every
world and every time. No trader obtains unbounded positive wealth, even if
every provable sentence keeps its quote `1/2` forever. The argument covers
arbitrary signed position sizes, not merely one-unit trades.

Constant-half quotes on every sentence constitute a computable market, but not
a zero-default, finitely supported belief state in S01's narrower terminology.
If that representation is mandatory, use the separate fee variant `s>=1`:
for any quote `p` in `[0,1]`, `a(y-p)-s|a|<=0`. In particular the always-zero
quote sequence, or any computable finite-support sequence that leaves one
theorem at zero forever, has the same failure of eventual correctness. This
variant uses a different explicitly stated fee; it does not silently change
the half-quote example.

The fee is per unit of the normalized elementary payoff position. If a new
unbounded bundle is traded for one fixed fee, that is another action/price
contract; it is not a counterexample to this calculation. A fixed per-*order*
fee can be amortized by increasing the order size, so it cannot silently replace
the proportional fee used in the proof.

This demonstrates a failure of the proposed implication

```
no profitable exploitation after these fees
    => accurate theorem beliefs or convergence to theorem certainty.
```

It does not show that resource-aware learning is impossible or undesirable.
Avoiding computations whose benefit is below their cost can be the right
decision policy. It shows that this economic objective and a logical-belief
learning duty are different targets. To claim both, the later algorithm needs
separate evidence for both. A high-fee criterion cannot obtain the belief
guarantee merely by retaining the word “induction.”

## 3. Bounded decision usefulness can rationally leave questions unresolved

Suppose the only current action choice has expected wrong-answer cost `1/2`,
and a guaranteed resolving computation costs `2`. Under the stipulated model,
buying certainty worsens the task objective. The useful policy can abstain from
that computation even though it remains uncertain. If a later request changes
the stakes to `10`, the same resolving computation can become valuable.

That change is not a contradiction in the mathematical proposition. It changes
which information is worth obtaining for the task. A useful cost-based learner
may consequently prioritize some logical questions over others. This is a
natural research ambition, but ordinary metareasoning can make the same
distinction. The comparison needs the same future-task information, options,
belief estimates and computation costs.

These probes suggest three separate commitments for P3-06/07:

1. Specify the statistical/logical duty of the forecast, if any.
2. Specify the decision duty and the permitted resource tradeoff.
3. Prove or test the connection under stated stakes, feedback and information
   assumptions; do not infer it from a shared numerical scale.

The current P3-N01 obligation remains open. This note narrows the meaning of a
possible “value/cost-space analogue” before a later task chooses an algorithm.

Independent same-model reconstruction and remaining assumptions are recorded in
[the cost-criterion review](../work_logs/P3_01_2026-10-07_S1/reviews/cost_criterion_review.md).

## 4. Refinement has several non-equivalent meanings

The author's phrase “refines those estimates over time” needs a declared
quantifier. Four possible services are:

| Service | Quantifier and assumptions | What does not follow |
|---|---|---|
| Narrower certified bounds | Fixed loss and interpretation; nonempty sound case sets satisfy `W_(t+1) subset W_t`; exact extrema or a proved nested enclosure | Better mean prediction, a cheap computation, or narrowing after evidence withdrawal |
| Lower expected prediction loss after information | Correct conditional probability model, nested information, and the corresponding Bayes report; expectation taken before the new observation | Improvement on every observed branch or adequacy of an arbitrary learned uncertainty model |
| Lower realized forecast error | A particular report and later resolved label, or a specified aggregate/cohort | Calibration, uniform future accuracy or a correct counterfactual model |
| Better paid decisions | The announced task loss, available policy class, information access, resource costs and comparator | More accurate answers to every logical question |

For the first row, nonempty `W_(t+1) subset W_t` gives

$$
\inf_{W_t}\ell\le\inf_{W_{t+1}}\ell
\le\sup_{W_{t+1}}\ell\le\sup_{W_t}\ell.
$$

This is pathwise narrowing of the exact loss range. It uses the same payoff
and a justified restriction; it does not apply after changing the objective
or restoring previously excluded cases. Independently recomputed loose outer
bounds may fail to nest even when the true extrema do. A claimed monotonic
certificate service needs the actual enclosure/transport rule as well.

### A finite signal can increase uncertainty on the branch that occurs

Let `Y` be a Boolean answer and `S` a possible acquired signal under this
explicitly stipulated joint model:

| | `S=0` | `S=1` |
|---|---:|---:|
| `Y=0` | `4/5` | `1/10` |
| `Y=1` | `0` | `1/10` |

Before seeing `S`, the probability of `Y=1` is `1/10`. The posterior is zero
on `S=0`, and `1/2` on `S=1`. The latter observation raises posterior variance
from `9/100` to `1/4`. On the particular branch `Y=0,S=1`, squared forecast
error rises from `1/100` to `1/4`. This is correct conditioning under the
stipulated model, not evidence of a defective update.

Before purchasing the signal, expected squared loss after conditioning is

$$
\frac45\,0+\frac15\,\frac14=\frac1{20}<\frac9{100}.
$$

The improvement is `1/25` in this score's units. It is an ex ante expectation,
not a statement that every acquisition reduces uncertainty or actual error.
For a squared-loss decision with report/action domain `[0,1]`, an acquisition
price below `1/25` can be worth
paying under this model; a higher price exceeds the expected benefit.

For zero-one action loss with action domain `{0,1}`, the optimal prior action
is zero with error `1/10`.
After `S=0` it remains zero; after `S=1` either action has conditional error
`1/2`. The optimal expected action error is still `1/10`. Thus the same
information strictly improves expected squared prediction loss while yielding
no reduction in the optimal zero-one action loss. Any strictly positive
acquisition price worsens that latter task. Ties and prices are explicit.

The action domains matter. If squared loss were restricted to Boolean actions,
it would equal zero-one loss, so the `1/25` value-of-information calculation
would not describe that restricted decision problem.

The arithmetic can describe an epistemic model or a distribution over a
declared deterministic query family. It does not make a fixed mathematical
answer physically random. A finite lookup implementation is not being
introduced, and no test from the earlier `finite_checks_1.json` is credited
with validating this later calculation.

### Why the expected-score statement is conditional

For nested information `F_t subset F_(t+1)`, let
`p_t=E[Y|F_t]` and `p_(t+1)=E[Y|F_(t+1)]` under one fixed probability model.
For bounded `Y`, expanding the square and conditioning gives

$$
E[(Y-p_t)^2\mid F_t]
=E[(Y-p_{t+1})^2\mid F_t]
+E[(p_{t+1}-p_t)^2\mid F_t].
$$

The cross term vanishes because
`E[Y-p_(t+1)|F_(t+1)]=0` and the report difference is measurable there.
This proves the expected improvement for that model without claiming that
the conditional expectations are cheaply computable. An arbitrary learned
forecast need not equal these conditional expectations, and a changed model
or interpretation need not preserve their joint probability space.

This is elementary decision/probability reasoning, consistent with S02/S03,
not a P3-06 learning theorem. Its contract consequence is to name the exact
notion of refinement before testing an update. In particular, the future
challenge must not label a sound update failed merely because a surprising
observation increases a legitimate uncertainty estimate.

## 5. Vanishing probability error needs a stakes bridge

Even convergence to the correct probability does not by itself control costs
when the stakes grow. This elementary sequence tests that particular
implication; it is not a proposed learner or a claim that every P3-01 duty
is simultaneously satisfied.

Take a fixed Boolean outcome `Y=0` and numerical forecasts `p_n=1/n`.
Their squared prediction loss is `1/n^2`, which tends to zero. Its cumulative
sum is bounded by two: the first term is one and the remaining sum is bounded
by the integral of `x^(-2)` from one to infinity.

On request `n`, allow an action with loss `nY` and a fallback with loss
`1/2`. The first action has actual cost zero, but its estimated expected cost
is `n p_n=1`. Minimizing these estimates therefore takes the fallback on
every request and incurs regret `1/2` per request relative to always taking
the zero-cost action. The cumulative decision regret grows as `N/2`,
despite vanishing probability error and bounded cumulative squared score.

The large stake is a known rational coefficient at each request, so this
example does not rely on a forbidden product of two unknown native
coordinates. It concerns the interpretation of a cross-request guarantee.
For an absolute probability error `epsilon_n` and a binary loss gap
`kappa_n`, the corresponding absolute cost error is
`|kappa_n| epsilon_n`. An appropriate rate or bounded-stakes assumption is
needed before using a probability-error result as a cost-error result.

The sequence is deliberately elementary. If a version-matched sound resolution
has been admitted, the project's separate U04 hard-evidence rule would require
an exact eligible correction; this example does not dispute that requirement
or claim that an LI generates these prices. It refutes only the implication
from normalized predictive convergence alone to the stated unbounded-stakes
decision guarantee. A strong ordinary method may use any legitimate proof or
shortcut as usual.

This direct written calculation was added after the eleven-group development
run and is not part of its assertion count. It supplies a useful boundary for
P3-06's later theorem choice, without beginning that algorithm or theorem task.
The [independent same-model reconstruction](../work_logs/P3_01_2026-10-07_S1/reviews/growing_stakes_review.md)
confirms the bound, decision calculation and these scope limits.
