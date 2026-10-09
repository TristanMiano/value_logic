# Independent reconstruction: exact-quota paid selective feedback

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC. Assignment:
**R-P3-B-A**. Review type: separate same-model, nonblind mathematical
reconstruction. Base: `6ce7391b6a41c6c19397b00ce7b6a2d9b228b9a4`.
Reviewer time is unmeasured and contributes **zero principal-clock credit**.
This review changes no earlier result, current plan, clock, ledger or publication.

**Verdict.** The proposed block protocol supports an all-issued expected
paid-decision inequality. It also supports a useful stronger cancellation:
the guaranteed improvement on purchased rounds can absorb the first-order
expert-loss term in linear multiplicative weights. The resulting constant
task-regret allowance is against a fixed expert acting without the paid
corrections. It is not a constant-regret theorem for the pre-issued forecasts
or a comparison with an expert given those same corrections.

The load-bearing restrictions are a fixed exogenous loss tape, one uniform
query in every block, the same prediction weights throughout a block, and
complete selected-query loss feedback at block end. Exact query count and
bounded random-bit execution are distinct: the latter needs an additional
sampling and arithmetic contract. The independent exact enumeration checks
272 selector paths and three separating examples; it does not establish the
general theorem by testing.

## 1. Objects and chronology

Fix integers $`N\geq1`$, $`m\geq1`$ and $`b\geq2`$, with $`T=mb`$.
The environment supplies a deterministic sequence of mathematical queries
and answers. For expert $`i`$ and round $`t`$, let $`\ell_{t,i}\in[0,1]`$
be its task loss. All these loss rows are fixed independently of the learner's
query and action randomization. The learner need not know the answers or loss
rows. A bought answer must suffice to evaluate **all** $`N`$ selected-query
expert losses. This is selective full-information feedback, not observation
of only the played expert's loss.

Experts may recommend different actions on different queries. A fixed
deterministic function of the public query, its exogenous features and its
position is permitted. The theorem does not require constant predictions.
It does require that the loss tape remain fixed: arbitrary expert changes
caused by the current block's purchased answer would violate that premise.

At the start of block $`k`$, compute weights $`p_k`$ using previously settled
blocks and choose $`J_k`$ uniformly among the block's $`b`$ positions,
independently of the previous history and the fixed tape. At every round,
issue the prediction before learning that round's answer. On $`J_k`$, buy
the answer and use a checked action of task loss zero. On other positions,
execute a mixture of the experts with marginal weights $`p_k`$. The mixture
may use fresh per-round randomness or one independent expert draw for the
whole block; only the expected-loss statement is asserted here. Settle the
queried loss vector and update weights **after the block**.

The bought answer can be used immediately to correct its own action. It
must not change subsequent predictions, expert features or query requests
inside that block. A separately checked exact-action override on another
round can only reduce task loss and hence preserves an upper bound, provided
it does not change the weights or the environment contract. It changes the
equality below into an inequality if such overrides are actually used.

Let $`\mathcal F_{k-1}`$ contain the completed-block history. Write

```math
X_{k,i}=\ell_{J_k,i},\qquad
\bar\ell_{k,i}=\frac1b\sum_{t\in B_k}\ell_{t,i},\qquad
L_i=\sum_{t=1}^T\ell_{t,i},\qquad L_* = \min_i L_i.
```

Let $`Q_k`$ be actual task loss on the block's unbought rounds. Conditional
on $`\mathcal F_{k-1}`$, the weights are fixed and uniform query selection
gives

```math
\mathbb E[Q_k\mid\mathcal F_{k-1}]
 =\sum_{t\in B_k}\left(1-\frac1b\right)
            \langle p_k,\ell_t\rangle
 =(b-1)\langle p_k,\bar\ell_k\rangle
 =(b-1)\mathbb E[\langle p_k,X_k\rangle\mid\mathcal F_{k-1}].
```

This is an expectation over the learner's controlled sampling. It assumes
no IID distribution of mathematical truths. Summing and applying the tower
property yields the central bridge

```math
\mathbb E\!\left[\sum_k Q_k\right]
  =(b-1)\mathbb E\!\left[\sum_k\langle p_k,X_k\rangle\right].
```

The factor is $`b-1`$, rather than $`b`$, because the purchased action has
already been corrected. For the unchanged **prospective predictions** on
all rounds, the corresponding factor is $`b`$.

## 2. Linear multiplicative weights: complete reconstruction

Use uniform initial weights and an update

```math
w_{k+1,i}=w_{k,i}(1-\eta X_{k,i}),\qquad
p_{k,i}=\frac{w_{k,i}}{W_k},\qquad W_k=\sum_iw_{k,i},
```

with $`0<\eta\leq1/2`$. Every weight remains positive. The exact potential
identity and the elementary logarithm inequalities give

```math
\log\frac{W_{k+1}}{W_k}
 =\log(1-\eta\langle p_k,X_k\rangle)
 \leq-\eta\langle p_k,X_k\rangle,
```

and, for every fixed expert,

```math
\log\frac{W_{m+1}}{W_1}
 \geq-\log N+\sum_k\log(1-\eta X_{k,i})
 \geq-\log N-\eta\sum_kX_{k,i}-\eta^2\sum_kX_{k,i}^2.
```

The last step follows from $`\log(1-z)\geq-z-z^2`$ on $`[0,1/2]`$.
For completeness, the derivative of $`z+z^2+\log(1-z)`$ is
$`z(1-2z)/(1-z)\geq0`$, and the function is zero at zero. Combining the
upper and lower potential estimates proves the pathwise selected-loss bound

```math
\sum_k\langle p_k,X_k\rangle
 \leq\sum_kX_{k,i}
      +\frac{\log N}{\eta}
      +\eta\sum_kX_{k,i}^2. \tag{P}
```

This calculation supplies the needed theorem directly. The root's primary
literature review identifies the established Prod antecedent; this review
makes no novelty claim for the update or potential argument.

Since $`X_{k,i}^2\leq X_{k,i}`$ and uniform selection gives
$`\mathbb E\sum_kX_{k,i}=L_i/b`$, (P) and the block bridge imply

```math
\mathbb E\!\left[\sum_kQ_k\right]
 \leq\left(1-\frac1b\right)(1+\eta)L_i
     +(b-1)\frac{\log N}{\eta}. \tag{A}
```

Every $`L_i`$ is deterministic, so this holds with $`L_i=L_*`$.
For binary losses the square term equals the first-order term exactly;
bounded nonbinary losses need only the displayed inequality.

An alternative, sometimes sharper certificate is available for every
$`0<\eta<1`$. Concavity gives
$`\log(1-\eta x)\geq x\log(1-\eta)`$ on $`[0,1]`$, so

```math
\mathbb E\!\left[\sum_kQ_k\right]
 \leq \alpha(\eta)\left(1-\frac1b\right)L_*
       +(b-1)\frac{\log N}{\eta},\qquad
\alpha(\eta)=\frac{-\log(1-\eta)}{\eta}.
```

No logarithm is needed to execute the learner. A deployed numerical
certificate must bound a displayed logarithm in the safe direction.

### 2.1 Paid-action cancellation

Set $`K=\max(2,b-1)`$ and $`\eta=1/K`$. If $`b\geq3`$, then

```math
\left(1-\frac1b\right)\left(1+\frac1{b-1}\right)=1.
```

If $`b=2`$, the coefficient in (A) is $`3/4\leq1`$. Consequently,

```math
\mathbb E\!\left[\sum_kQ_k\right]-L_*
 \leq (b-1)K\log N
 =\begin{cases}
 2\log N,&b=2,\\
 (b-1)^2\log N,&b\geq3.
 \end{cases} \tag{C}
```

The allowance is independent of $`T`$ for fixed $`b,N`$. This is possible
because the learner gets an exact zero-loss action on one round in every
block while the comparator incurs its own loss on all rounds. It is not a
violation of a usual label-efficient regret lower bound. If the fixed expert
also receives exact corrections on the same sampled rounds, its expected
task loss is $`(1-1/b)L_i`$; the extra first-order term in (A) then remains.
The paid fees likewise remain in the actual bill.

The case $`b=1`$ is separate and trivial: buy every answer, incur no task
loss, and pay the full bill. If $`N=1`$, no learning update is necessary and
the basic identity gives exactly $`(1-1/b)L_1`$; the logarithmic allowance
is zero. A zero-query protocol is outside the block theorem.

## 3. The all-in bill and useful scope

Suppose every selected answer is successfully returned for fee $`f`$,
$`O_T`$ is the actual charged controller/evaluation/storage/execution cost,
and $`S`$ is setup. Include the cost of evaluating the experts, computing
their losses on the queried round, maintaining weights, generating random
bits and admitting the answer; none is supplied free by (P). Then

```math
J_T=\sum_k Q_k+mf+O_T+S
```

and (C) yields

```math
\mathbb E[J_T]
 \leq L_*+(b-1)K\log N+mf+\mathbb E[O_T]+S. \tag{J}
```

This is the accepted target type. It compares with fixed experts' task
losses; a cost comparison against a deployable fixed-expert policy must
also use that policy's actual overhead. It does not compare with a policy
that counterfactually sees a different sequence of requests or labels.

For example, a sufficient declared break-even condition against a
zero-task-loss always-BUY baseline of total cost $`fT+O_B+S_B`$ is

```math
L_*+(b-1)K\log N+\mathbb E[O_T]-O_B+S-S_B
 < f(T-m).
```

This is a nonempty mathematical parameter region. Membership must be
justified for an application, and an ordinary analytic shortcut or cheaper
fixed predictor can still win. The theorem does not establish that a chosen
arithmetic family makes learning the cheapest service.

If fees $`f_t`$ are fixed independently of selection, the expected fee is
$`b^{-1}\sum_tf_t`$. A hard bound is $`\sum_k\max_{t\in B_k} f_t`$,
not the expected fee. For path-dependent actual service charges, retain
$`\mathbb E[\sum_k F_k]`$ unless a separate bound is justified. Choosing
only the cheapest position changes the sampling law and invalidates the
uniform bridge without a new estimator and action calculation.

If a bought action has a nonzero achievable minimum task loss $`c_t`$,
apply the analysis to residual losses $`\ell_{t,i}-c_t`$ and add
$`\sum_tc_t`$. The residuals must have a declared bound. For other units,
normalize by a fixed loss scale and multiply the task and regret terms back
into the common units before adding fees.

Exactly $`m`$ admitted queries is a hard count. Successful settlement,
solver runtime and a hard monetary or controller budget need their own
contract. Skipping a failed or unaffordable label generally breaks the
unbiased update; merely adding its immediate task loss does not repair the
learning argument. An actual abort/fallback protocol needs a separate bound.

## 4. Integer execution and finite action rounding

For binary expert recommendations $`a_{t,i}\in\{0,1\}`$ and answer
$`y_t\in\{0,1\}`$, use $`\ell_{t,i}=1\{a_{t,i}\ne y_t\}`$.
Integer weights initialized to one can update as

```math
w_{k+1,i}=w_{k,i}(K-\ell_{J_k,i}).
```

The common factor $`K`$ cancels on normalization, so this is exactly the
linear update with $`\eta=1/K`$. It requires no floating-point or
exponential approximation. Expert recommendations can vary with the query
under the fixed-tape premise.

At a prediction round put

```math
W=\sum_iw_i,\qquad U_t=\sum_iw_i a_{t,i},\qquad p_t=U_t/W.
```

With $`h`$ fair bits, sample action one with probability

```math
q_t=2^{-h}\left\lfloor 2^h U_t/W\right\rfloor.
```

Both $`p_t=0`$ and $`p_t=1`$ are represented exactly. Otherwise
$`0\leq p_t-q_t<2^{-h}`$. For either binary answer,

```math
\left|\mathbb E[\ell(q_t,y_t)]-\mathbb E[\ell(p_t,y_t)]\right|
 =|q_t-p_t|<2^{-h}.
```

Conditional fair action bits independent of the selected index and the
fixed answer therefore add at most

```math
\rho_T=(T-m)2^{-h}
```

to (J). This is an expected-loss allowance, not a pathwise bound on the
realized sampled errors. It includes only unbought rounds because queried
actions are corrected. If different fixed precisions are used, the safe
sum is over their admitted per-round allowances, with the sampling factor
included when justified. An actual high-probability regret theorem would
also need to control the random queried-loss estimates, not just action
sampling noise.

After at most $`m`$ updates, every individual weight is at most $`K^m`$,
so its unsigned bit length is at most

```math
B_w=m\lceil\log_2 K\rceil+1.
```

The total $`W`$ and the numerator $`U_t`$ need up to
$`B_w+\lceil\log_2 N\rceil`$ bits. The shifted division numerator
$`2^hU_t`$ needs an additional $`h`$ bits. Thus an individual-weight cap
alone is not a cap on every controller intermediate. Integer arithmetic,
division, expert evaluation, transient workspace and retained forecasts
must be included in the claimed controller bound or measured tariff.

When $`b=2^r`$, one exactly uniform block index uses exactly $`r`$ fair
bits; the query schedule then has a bounded random-bit implementation.
For non-power-of-two $`b`$, exact uniform rejection sampling terminates
almost surely but has no finite worst-case number of draws. A fixed
deterministic pseudorandom seed is a development realization; it does not
by itself verify the fair-bit probability premise. Similar care is needed
if sampling an arbitrary exact rational expert mixture instead of using
the dyadic binary-action rule.

## 5. The pre-issued forecast remains a different object

The forecast $`p_t`$ is issued before paid resolution. Replacing its value
by the corrected answer for scoring would change the forecast record.
Since binary expert losses also equal their Brier scores, convexity gives

```math
(p_t-y_t)^2
 \leq\sum_i p_{k,i}(a_{t,i}-y_t)^2
 =\langle p_k,\ell_t\rangle.
```

The all-round prospective mixture uses the factor $`b`$ and (P), hence

```math
\mathbb E\!\left[\sum_{t=1}^T(p_t-y_t)^2\right]
 \leq (1+1/K)L_*+bK\log N. \tag{F}
```

There is no paid-correction cancellation in (F). In particular, fixed
$`b,K`$ does not establish vanishing forecast regret per round whenever
$`L_*`$ itself is linear in $`T`$. A horizon-tuned learning rate gives the
usual different trade-off; the current constant paid-action allowance
cannot be attached to the all-issued Brier record.

If the issued scalar itself is $`q_t`$ rather than $`p_t`$, Brier score
is 2-Lipschitz on $`[0,1]`$, so add at most $`2T2^{-h}`$ to (F).
If $`q_t`$ is only an execution probability and $`p_t`$ is the retained
forecast, that extra forecasting allowance is unnecessary. The comparison
here is to the given binary experts, not an arbitrary continuous forecast
class, calibration criterion or unrestricted logical inductor.

## 6. Fixed experts, random hindsight and adaptation

For the fixed tape, the minimizing fixed expert is an ordinary deterministic
hindsight comparison. The theorem does not select a different expert for
each query or each block. If the whole tape is randomly drawn independently
of the learner's coins, conditioning on that entire tape proves the bound
with an expected hindsight minimum as well.

A weaker extension allows each block's full loss matrix to be committed
from the preceding history **before** its own index is drawn. The block
bridge still holds conditionally. Applying (P) to every fixed expert and
taking expectations yields a bound with
$`\min_i\mathbb E[L_i]`$. It does not directly yield the smaller quantity
$`\mathbb E[\min_i L_i]`$. The two values can be 1 and 0 respectively:
with probability one-half let the expert totals be $`(0,2)`$, and otherwise
$`(2,0)`$. The selected trajectory is not a different policy's counterfactual
trajectory either.

For completeness, a qualified adaptive-block hindsight extension is
possible, but it needs an extra sampling term. Put
$`A_i=\sum_k\bar\ell_{k,i}`$. Each
$`X_{k,i}-\bar\ell_{k,i}`$ is a conditional mean-zero increment of range
width at most one. The elementary bounded-range moment-generating-function
bound, followed by a union over the fixed experts, gives

```math
\mathbb E\max_i\sum_k(X_{k,i}-\bar\ell_{k,i})
 \leq\sqrt{m\log N/2}.
```

One way to verify the MGF step is to differentiate its log twice: the
tilted variance of a variable in an interval of width one is at most
$`1/4`$, while its initial value and derivative are zero. Integrating twice
gives $`\log\mathbb E e^{\lambda Z}\leq\lambda^2/8`$; conditional
iteration and minimizing $`\log N/\lambda+m\lambda/8`$ give the result.
Using $`X^2\leq1`$ in (P), this supplies the valid but weaker bound

```math
\mathbb E\!\left[\sum_kQ_k\right]
 \leq\left(1-\frac1b\right)\mathbb E[\min_iL_i]
 +(b-1)\left(\frac{\log N}{\eta}+\eta m
                    +\sqrt{m\log N/2}\right).
```

This optional extension has not been implemented or selected as the main
service. It still excludes adaptation within a block after its query
schedule begins to be exposed.

### Two direct failures of the block bridge

**Premature update.** Take one block of two fixed labels $`(0,1)`$, two
constant experts, initially equal weights and $`\eta=1/2`$. If the first
round is bought and the weights update immediately, the second round's
mistake probability is $`2/3`$. If the second round is bought, the first
round's mistake probability is $`1/2`$. Expected unbought loss is therefore
$`7/12`$, while the queried pre-update mixture loss is always $`1/2`$.
Freezing weights only in the bookkeeping, while allowing updated expert
features to change predictions, has the same structural problem.

**Public-history-adaptive future request.** There is one expert that always
predicts zero. In a two-round block the first requested answer is zero.
The second requested answer is one if the public first-round action was
BUY, and zero otherwise. A uniform bought index has selected loss zero on
both paths, but the expected unbought task loss is $`1/2`$. The expected
all-issued expert loss is $`1/2`$, whose nominal discounted value is only
$`1/4`$. No access to future random bits is needed: reacting to the observed
first-round purchase already invalidates the fixed-tape bridge. A concrete
mathematical-query environment can implement these answers by selecting
between two predetermined true/false statements.

## 7. Uneven blocks require weighted updates

Let block sizes be $`b_k`$, put $`c_k=b_k-1`$ and $`B=\max_kc_k`$,
and keep one uniform query per block. The actual objective is now

```math
\mathbb E[\text{task loss}]
 =\mathbb E\sum_k c_k\langle p_k,X_k\rangle.
```

An unweighted selected-loss regret bound does not by itself control this
weighted objective. If $`B>0`$, update using
$`Z_{k,i}=c_kX_{k,i}/B\in[0,1]`$. Applying (P) to $`Z`$ and multiplying
by $`B`$ proves

```math
\sum_kc_k\langle p_k,X_k\rangle
 \leq\sum_kc_kX_{k,i}
       +B\frac{\log N}{\eta}
       +\frac{\eta}{B}\sum_kc_k^2X_{k,i}^2.
```

With $`L_{k,i}=\sum_{t\in B_k}\ell_{t,i}`$ and $`X^2\leq X`$,

```math
\mathbb E[\text{task loss}]
 \leq\sum_k\frac{c_k}{b_k}
          \left(1+\frac{\eta c_k}{B}\right)L_{k,i}
       +B\frac{\log N}{\eta}.
```

Choosing $`\eta=1/\max(2,B)`$ makes every coefficient at most one, so
the constant full-expert comparison extends with allowance
$`B\max(2,B)\log N`$. For binary losses a common-factor integer update is
$`w_i\leftarrow w_i(KB-c_kX_{k,i})`$, with $`K=\max(2,B)`$.
Singleton blocks have no unbought loss and do not change relative weights.
If all blocks are singletons, every answer is bought and no update theorem
is needed. The actual implementation has been scoped by the root to equal
power-of-two blocks; this appendix is a derivation, not an implemented claim.

## 8. Finite evidence and integration recommendation

[The independent probe](finite_bridge_probe.py) uses exact fractions and
exhaustive selector averages, with no pseudorandom seeds. Its
[saved result](finite_bridge_probe.stdout.json) checks:

- 16 binary tapes with two blocks of size two: 64 selector paths.
- 32 binary tapes with block sizes two and three and the weighted update:
  192 selector paths.
- Eight binary tapes with a singleton and a size-two block: 16 paths.
- The premature-update, public-history-adaptation and random-hindsight
  examples above.

The equalities hold after averaging for every enumerated fixed tape. They
often fail on individual paths, as expected: 32 equal-block paths and 144
uneven-block paths have different realized unbought and sampled-target
losses. This is useful evidence against a mistaken pathwise interpretation.
The process exited zero; stderr is empty. It does not execute the root's
candidate or certify its API, tariffs, source closure or finite arithmetic
limits. Those require the assigned implementation review.

**Accept for integration** the fixed-tape, fixed-library, equal-power-of-two
block service if the implementation preserves the chronology, settles every
selected label, bounds the complete integer workspace, prices the complete
bill and retains the rounding allowance. Preserve (F) separately from (J).
Keep ordinary exact computation, caches, analytic shortcuts and ordinary
label-efficient expert algorithms in the comparison set. The useful delta
here is an explicit paid-action/learning and hard-query-count bridge with
finite implementation duties; this review does not award a contribution
status or start P3-08.

### Read provenance

The source manifest records the prospective recurrence forecast and protocol,
the earlier optional-recurrence dossier, and the previously published P3-07
full-feedback and dyadic-sampling boundaries. The reviewer read the relevant
passages of those earlier documents, not their entire transitive source
closure. The mathematical reconstruction above is new work in this owned
review directory. External literature attribution belongs to the root's
separate primary-source audit; no third-party paper is copied here.
