# Paid selective feedback for a bounded mathematical service

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.
Task: **R-P3-B-A**, the author-selected recurrence after P3-B.
Stage: **DEVELOPMENT**. P3-08 is not started by this construction.

## 1. The result and its question

The P3-B review left a specific gap: guarantees for all observed labels do not
automatically apply to every issued request when the reasoner pays for only
some answers. This construction supplies one restricted bridge. It combines
an exact purchase quota, ordinary product weights, a finite random-bit policy,
version-bound checked mathematical answers and an explicit resource bill.
The guarantee concerns every issued terminal decision, including decisions on
requests whose answers the learner never purchases.

There are two executable weight representations. Exact integer weights have
no update-rounding error, but their bit length can grow with the horizon. A
positive-integer fixed-mass representation has bounded storage and a separately
proved approximation allowance. Both keep predictions frozen within each
block and use one uniformly selected paid answer from it. Bought answers may
correct their own terminal actions. They do not revise earlier forecasts.

The learning machinery is ordinary. The closest comparison includes
Cesa-Bianchi, Mansour and Stoltz's product-weights analysis and Russo et al.'s
purchased best-action model; [the source contracts](../literature/07_selective_feedback_sources.md)
state the exact imports. The contribution assessed here is the restricted
finite/cost/feedback integration and its limitations, not a new name for
multiplicative weights or a priority claim for buying an answer before acting.

The source-bound implementation is [07_selective_feedback.py](../checks/07_selective_feedback.py).
The [service module](../checks/07_selective_feedback_service.py) reuses the
existing bounded modular adapter and implements ordinary exact controls.
The [prospective contract](../work_logs/R_P3_B_A_2026-10-09_S1/development/contract_v1.json),
[bounded-state design](../work_logs/R_P3_B_A_2026-10-09_S1/development/bounded_state_design.md)
and [planned development comparison](../work_logs/R_P3_B_A_2026-10-09_S1/development/run_plan_v1.json)
preserve what was selected before the corresponding runs.

## 2. Mathematical and information contract

Fix a deterministic exogenous tape of mathematical requests
$`q_1,\ldots,q_T`$ and their deterministic answers $`y_t=f(q_t)\in\{0,1\}`$.
The tape is fixed independently of the learner's random bits. The learner sees
the public mathematical input at each round, but receives its answer only
through a purchased successful receipt. Public inputs may admit other paid
exact computations; the ordinary controls below retain that capability.

Fix $`N\ge2`$ stateless expert functions $`a_i(q)\in\{0,1\}`$ before the run.
Their full loss table and comparator losses are

```math
\ell_{t,i}=\mathbf1\{a_i(q_t)\ne y_t\},\qquad
L_i=\sum_{t=1}^T\ell_{t,i},\qquad L_* = \min_{1\le i\le N} L_i.
```

The minimizer is one fixed expert on the entire tape. It does not change with
the request, and its loss contains every round. A purchased binary answer
allows the learner to compute all N expert losses for that one request.
This is selective full-vector feedback, rather than observing only the
loss of the action actually played. Computing that vector is charged.

Let $`T=mB`$, with equal blocks of size $`B\ge2`$. At the start of each
block, select one position uniformly, independently of the fixed tape and
earlier blocks. Write that position as $`J_k`$. The broker may hold the
selector privately, but the prediction operation does not receive it.
The mixture $`p_k`$ depends only on previously completed blocks and is
unchanged throughout the current block. The experts themselves do not adapt
inside the block.

| Stage | Available information and permitted action |
|---|---|
| Issue | Evaluate the fixed experts on the public request; issue the dyadic probability and prospective binary action using the frozen block weights. |
| Purchase | At the selected position, execute the cold checked service and pay its actual invoice. No other answer enters the learner. |
| Act | Use the correct purchased answer as the terminal action if this is the selected position; otherwise execute the prospective action. |
| Settle block | After all B actions close, update using only the selected request's expert predictions and checked answer. |
| Evaluate | After the learner transcript closes, a separate evaluator computes every label for scoring. These labels are not inputs to issue or update. |

The base theorem uses fresh independent fair action bits. The executable
development generator instead supplies a finite deterministic bit tape from a
recorded seed. Each saved trace is an illustrative realization of the finite
algorithm. Running a seed does not establish the independence premise of a
probability theorem.

## 3. Selected-loss product weights and the block bridge

Put $`X_{k,i}=\ell_{J_k,i}`$ and use uniform initial weights with the update

```math
w_{k+1,i}=w_{k,i}(1-\eta X_{k,i}),\qquad
p_{k,i}=\frac{w_{k,i}}{\sum_jw_{k,j}},\qquad 0<\eta\le\tfrac12.
```

### 3.1 The ordinary potential inequality

For each realized selected-loss sequence, let $`W_k=\sum_iw_{k,i}`$.
The upper and lower estimates for its logarithm are

```math
\begin{aligned}
\log(W_{m+1}/W_1)
&=\sum_k\log(1-\eta\langle p_k,X_k\rangle)
\le-\eta\sum_k\langle p_k,X_k\rangle,\\
\log(W_{m+1}/W_1)
&\ge-\log N+\sum_k\log(1-\eta X_{k,i})\\
&\ge-\log N-\eta\sum_k X_{k,i}-\eta^2\sum_kX_{k,i}^2.
\end{aligned}
```

The scalar inequalities are $`\log(1-z)\le-z`$ for $`z<1`$ and
$`\log(1-z)\ge-z-z^2`$ for $`0\le z\le1/2`$. The latter follows because
the derivative of $`z+z^2+\log(1-z)`$ is $`z(1-2z)/(1-z)\ge0`$ and its
value at zero is zero. Combining the estimates gives the established Prod
inequality in the loss convention:

```math
\sum_k\langle p_k,X_k\rangle
\le\sum_kX_{k,i}+\frac{\log N}{\eta}
                    +\eta\sum_kX_{k,i}^2. \tag{1}
```

This statement is pathwise in the selected meta-rounds. The following
averaging step, rather than equation (1) alone, connects it to unbought
mathematical requests.

### 3.2 Why the factor is B minus one

Conditional on completed blocks, the current mixture is fixed. Uniform
selection and the frozen loss table give

```math
\begin{aligned}
\mathbb E\left[\sum_{t\in\mathcal B_k,\ t\ne J_k}
                    \langle p_k,\ell_t\rangle
                    \mid\mathcal F_{k-1}\right]
&=(B-1)\mathbb E[\langle p_k,X_k\rangle\mid\mathcal F_{k-1}],\\
\mathbb E\sum_k X_{k,i}&=L_i/B.
\end{aligned} \tag{2}
```

The purchased terminal decision has zero loss. For the ideal randomized
mixture, expected loss on each other request is its mixture loss. Binary
expert losses satisfy $`X_{k,i}^2=X_{k,i}`$. Taking expectations in (1),
applying (2), and minimizing over deterministic comparator totals yields

```math
\mathbb E L_{\rm terminal}^{\rm ideal}
\le \left(1-\frac1B\right)(1+\eta)L_*
                 +(B-1)\frac{\log N}{\eta}. \tag{3}
```

Choose $`K=\max(2,B-1)`$ and $`\eta=1/K`$. The coefficient of $`L_*`$
is at most one, and is exactly one when $`B\ge3`$. Thus

```math
\mathbb E L_{\rm terminal}^{\rm ideal}-L_*
\le (B-1)K\log N
=\begin{cases}2\log N,&B=2,\\(B-1)^2\log N,&B\ge3.\end{cases} \tag{4}
```

The allowance is constant in T when B is fixed. The comparator receives no
paid corrections, while the learner receives a perfect action on a fixed
fraction of rounds. If the comparator is corrected at the same selected
positions, its expected loss is $`(1-1/B)L_i`$ and the first-order difference
$`(1-1/B)L_i/K`$ remains. Equation (4) is not a constant-regret claim against
that stronger comparator, nor a statement that information is free.

### 3.3 A sharper certificate for the same executed algorithm

For binary selected losses,
$`\log(1-X_i/K)=X_i\log(1-1/K)`$ exactly. Using this identity in the
lower potential gives the coefficient

```math
\alpha_B=\frac{B-1}{B}K\log\frac{K}{K-1}
<\frac{B-1}{B}\left(1+\frac1K\right).
```

The conservative coefficient in (3), (8) can therefore be replaced by
$`\alpha_B`$, with the same logarithmic, fixed-state and action-rounding
allowances. Similarly the first-order Brier coefficient in (10) can be
replaced by $`K\log(K/(K-1))`$. A concave-log chord inequality supplies
the analogous potential bound for losses in `[0,1]`; the binary case makes
the comparator log term exact.

The initial independent review already gave the unrounded alternative.
The [separate rational refinement](../work_logs/R_P3_B_A_2026-10-09_S1/development/binary_potential_certificates.json)
now carries it through finite precision and all 20 existing uniform traces,
using positive-series logarithm enclosures. It does not change the policy,
any observed score or any invoice, and the original certificates remain
preserved. For the 3,968-round B=8 normalized trace, the retrospective
expected terminal upper bound tightens from approximately 1,924.352 to
1,820.737. Using only the source-known $`L_*\le T/2`$ gives approximately
1,941.591. These are expectation bounds, not per-seed acceptance limits.

Buying every answer ($`B=1`$) has zero terminal task loss and the complete
purchase bill. With one expert there is no need for a learning update. These
endpoints are mathematical checks, not the substantive learning result. The
current source-bound `execute()` fixes the four-expert library; it does not
execute a one-expert service.

## 4. Finite probabilities and bounded storage

### 4.1 Exact integer implementation

For binary losses, multiplying every weight by the same denominator leaves
the normalized distribution unchanged. Therefore the update

```math
w_{k+1,i}=w_{k,i}(K-X_{k,i}),\qquad w_{1,i}=1
```

implements (1) exactly. No floating-point exponential or exact-real oracle is
used. After at most m updates, each weight is at most $`K^m`$, so

```math
\mathrm{bits}(w_i)\le 1+m\lceil\log_2K\rceil.
```

The sum of weights and action-one mass require an additional
$`\lceil\log_2N\rceil`$ bits. Shifting the action numerator by h adds h
more. These intermediate capacities are explicit in `Contract`; a bound on
only the stored weights would be insufficient.

### 4.2 Fixed-mass representation

For a declared integer precision $`s\ge1`$, put $`M=N2^s`$ and initialize
each weight to $`2^s`$. After a purchased loss row, calculate

```math
v_i=w_i(K-X_i),\quad V=\sum_i v_i,\quad
u_i=1+\left\lfloor\frac{(M-N)v_i}{V}\right\rfloor,\quad
R=M-\sum_i u_i.
```

The residual R is an integer in $`[0,N-1]`$. Give one additional unit to the
first R experts in the fixed source order. The resulting weights are positive,
sum to M, and their normalized probabilities satisfy

```math
p_{k+1,i}\ge(1-2^{-s})
 \frac{p_{k,i}(1-X_{k,i}/K)}{1-\langle p_k,X_k\rangle/K}. \tag{5}
```

This is a one-sided multiplicative bound; the rounding is not assumed
unbiased. Taking logarithms, telescoping (5), and using $`p_{m+1,i}\le1`$
adds $`mK\log(1/(1-2^{-s}))`$ to equation (1). The resulting additional
terminal-loss allowance has the exact rational upper bound

```math
\Delta_s\le\frac{(B-1)mK}{2^s-1}. \tag{6}
```

The new weights require at most $`s+\lceil\log_2N\rceil+1`$ bits.
The normalization numerator can be as large as $`M^2K`$; its arithmetic is
bounded and charged as well. The [independent reconstruction](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/proof_agent/bounded_normalization_review.md)
proves these statements and preserves the finite checking evidence.

The approximation term is necessary. With two experts, $`s=1,K=2`$, and
only zero labels, weights evolve $`(2,2)\to(3,1)\to(3,1)\to\cdots`$.
The wrong expert retains positive mass despite a perfect alternative.
Keeping s fixed does not give asymptotically vanishing error on every such
sequence. For a finite horizon the allowance is explicit; increasing s with
the horizon can reduce it while using logarithmically growing storage.

### 4.3 Finite binary actions

Let $`U_t=\sum_iw_i a_i(q_t)`$, and let $`W=\sum_iw_i`$ be the frozen
block mass. The issued action-one probability is

```math
q_t=2^{-h}\left\lfloor\frac{2^h U_t}{W}\right\rfloor.
```

Exactly h fair bits sample this Bernoulli action. For either answer the
difference from ideal mixture loss is at most $`2^{-h}`$. Only unbought
actions retain that difference, giving

```math
\rho_h=(T-m)2^{-h}. \tag{7}
```

Power-of-two B requires exactly $`\log_2B`$ selector bits per block. Hence
the full service consumes exactly $`m\log_2B+Th`$ supplied bits. Exact
uniform rejection sampling for an arbitrary B has no finite worst-case bit
count; it is not silently used. The two-word extraction implementation has
a separate maximum 95-bit transient, included in the overall numeric bound.

For the four-expert fixed-mass service, $`M=2^{s+2}`$. If $`h\ge s+2`$,
the action probability is exactly representable and the action-rounding
allowance can be zero. The planned comparison uses $`s=h=16`$ and therefore
retains (7), rather than claiming that special case.

## 5. The all-in value and the actual hard budget

Let $`c\ge0`$ be a fixed price for one terminal mistake. Let a nonnegative
fixed vector price each declared primitive-resource category. Write S for
priced standalone setup, $`O_T`$ for actual controller, expert, random-bit,
storage and output costs, and $`f_t`$ for the priced cold checked completion
of request t. Its source-bound operation bill is deterministic given the
public request under the trusted local service. Actual expenditure is

```math
J_T=cL_{\rm terminal}+S+O_T+\sum_{k=1}^m f_{J_k}.
```

Setup is paid once for the actual dependency closure. A provider fee that
already includes computation must not be added again on top of the same
operation invoice. The implemented service uses actual category debits, with
no extra flat fee. Private evaluation and experiment orchestration are
separately reported research-procurement costs; they are unavailable to the
deployed policy and excluded from its task-value comparison.

**Uniform paid-feedback theorem.** Under the contract in §2, complete correct
selected receipts, and the finite policy in §4,

```math
\boxed{\quad
\mathbb E J_T\le
c\left[
 \left(1-\frac1B\right)\left(1+\frac1K\right)L_*
 +(B-1)K\log N+\Delta_s+\rho_h
\right]
 +S+\mathbb E O_T+\frac1B\sum_{t=1}^T f_t.
\quad} \tag{8}
```

Here $`\Delta_s=0`$ for exact weights; the fixed-state implementation uses
the safe rational value in (6). A simpler upper bound replaces the coefficient
of $`L_*`$ by one. Terminal loss is also at most $`T-m`$, so the minimum of
that trivial bound and the displayed task-loss bound is valid. This avoids
presenting a large logarithmic allowance as an informative numerical bound.

The expectation is over the controlled selectors and action bits. It is not
an IID-law assumption about mathematical truths. On a random exogenous tape
independent of those bits, conditioning on the whole tape extends the result
with the corresponding expected full-tape comparator and resource terms.

### 5.1 Exact quota is not an expected-budget statement

Every successful execution buys exactly m answers. The finite random input
also has a fixed bit count. To give the complete procedure a hard resource
limit, the broker reserves all m cold completions before execution, together
with the controller envelope and actual admitted setup.

For the checked service the inherited core cap is 1,024 units and the new
family-admission cap is 64, giving a safe reservation of **1,088 units per
purchase**. Actual successful debits are smaller. The controller's envelope
uses the admitted horizon, expert count, action/state precision and the largest
integer intermediate. It precharges each tariff operation and retains every
successful earlier charge if a later operation is denied. A child invoice
releases one reserved cap and debits the child's actual work. Its refund
cannot create another query position.

The resulting source-bound hard limit has the form

```math
C_{\rm setup}+C_{\rm controller}^{\max}
                 +1088m+C_{\rm development\ bit\ source}^{\max}.
```

The last term is explicitly charged for seeded development; the abstract
fair-bit input has its own supplied-bit/storage tariff. These are finite
abstract operation and 64-bit-word tariffs. They do not claim that a Python
integer operation takes one CPU cycle, or that a word tariff measures actual
heap allocation. Arithmetic involving large operands has its declared
operand-word charge, and the measurements report physical runtime separately.

A valid admitted run is funded to finish. An unavailable or unsuccessful
selected answer does not become a zero-loss update: the broker stops, records
its spending and does not issue the successful theorem. Omitting failed
labels from an otherwise purported successful sequence would generally change
the sampling law. An arbitrary timeout or fallback process therefore needs
its own guarantee.

### 5.2 What an economic gain would require

Against a checked always-BUY policy of cost
$`\sum_t f_t+S_{\rm BUY}+O_{\rm BUY}`$, a sufficient gain condition is

```math
c\left[L_*+(B-1)K\log N+\Delta_s+\rho_h\right]
 +S-S_{\rm BUY}+\mathbb E O_T-O_{\rm BUY}
 <\left(1-\frac1B\right)\sum_t f_t. \tag{9}
```

This identifies the required relationship between accuracy, avoided
completions and overhead. It is a nonempty abstract parameter region, not
evidence that the selected modular family occupies it. Direct exact actions,
ordinary caches and analytic tables can be better controls than checked
always-BUY. Their prices and output contracts matter independently of (9).

In the uniform implementation, changing only a fixed price vector can rescore
retained resource coordinates without changing the query or learning path,
provided the new resource contract remains funded. Changing the action rule,
expert library, admitted feedback, or a price-dependent acquisition policy is
a different procedure. The [earlier repricing boundary](06_price_replay.md)
continues to apply.

## 6. A pre-issued forecast keeps its own score

For ideal action-one mass $`p_t=U_t/W`$, convexity gives

```math
(p_t-y_t)^2\le\sum_i p_{k,i}(a_i(q_t)-y_t)^2
                         =\langle p_k,\ell_t\rangle.
```

Every issued forecast is scored, including those followed by a purchase.
The conditional sampling factor is therefore B, rather than B minus one.
For the emitted dyadic forecast $`q_t`$,

```math
\mathbb E\sum_{t=1}^T(q_t-y_t)^2
\le\left(1+\frac1K\right)L_*+BK\log N
 +\begin{cases}0,&\text{exact weights},\\
 BmK/(2^s-1),&\text{fixed state},\end{cases}
 +2T2^{-h}. \tag{10}
```

The last term uses the 2-Lipschitz bound for binary Brier loss on $`[0,1]`$.
It can be removed when the probability is represented exactly. The right
side may again be replaced by its minimum with T.

The bound compares with the source-fixed binary experts. It does not establish
calibration, a joint probability law over mathematical statements, coherence
under every logical implication, or a general logical-induction property.
In particular, a constant paid-action allowance in (4) does not transfer to
the original forecast score. The record contains both quantities so later
integration can choose the right one.

## 7. Choosing the purchased position from learned disagreement

The [separately versioned allocation extension](../checks/07_selective_feedback_allocation.py)
allows the settled learning state to influence the next purchase. It grants a
stronger public input: **the current block's B public requests are available
before the selector is drawn**. Public expert advice, buffering and selection
are charged. The current block's unpurchased answers remain unavailable.

Conditional on the completed past and that public block, choose probabilities
$`\pi_{k,t}>0`$ summing to one, with $`\pi_{k,t}\ge1/(H+1)`$ for fixed
$`H\ge1`$. They may depend on the frozen mixture and prior purchased labels.
Draw one position J and keep the same mixture throughout the block. Define

```math
X_{k,i}=(\pi_{k,J}^{-1}-1)\ell_{J,i},\qquad Z_{k,i}=X_{k,i}/H\in[0,1].
```

The subtraction of one removes the purchased action, whose terminal loss is
corrected to zero. Conditional averaging gives

```math
\begin{aligned}
\mathbb E[X_{k,i}\mid G_k]
 &=\sum_t(1-\pi_{k,t})\ell_{t,i},\\
\mathbb E[X_{k,i}^2\mid G_k]
 &=\sum_t\frac{(1-\pi_{k,t})^2}{\pi_{k,t}}\ell_{t,i},\\
\mathbb E[L^{\rm ideal}_{{\rm terminal},k}\mid G_k]
 &=\mathbb E[\langle p_k,X_k\rangle\mid G_k].
\end{aligned} \tag{11}
```

G includes the completed past, current public block, frozen weights and chosen
propensities, but precedes the current selector. Apply (1) to Z with
$`\eta=1/K`$, where $`K\ge\max(2,H)`$, and multiply by H. Each deterministic
comparator loss then receives coefficient

```math
1-\pi+\frac{(1-\pi)^2}{HK\pi}\le1,
```

because $`(1/\pi-1)^2\le H^2\le HK`$. The fixed-mass normalizer retains
(5) with X replaced by Z. The resulting bound is

```math
\boxed{\quad
\mathbb E L_{\rm terminal}
\le L_*+HK\log N+\frac{HmK}{2^s-1}+(T-m)2^{-h}.
\quad} \tag{12}
```

The minimum with $`T-m`$ is again valid. This is not a statement that an
adaptive selector has a better worst-case bound than the uniform rule.
The probability floor can increase H substantially.

### 7.1 Finite tickets and the actual update

For power-of-two B, give one ticket to every position and B additional tickets
to a favored position. Drawing exactly $`\log_2(2B)`$ bits produces

```math
\pi_f=\frac{B+1}{2B},\qquad \pi_t=\frac1{2B}\ (t\ne f),\qquad H=K=2B-1.
```

The source-fixed favorite maximizes
$`U_t(M-U_t)/\widehat c_t`$, breaking ties at the earliest position.
$`U_t`$ is the frozen weight mass predicting one. The public cost proxy is
128 for the elementary inputs $`a=1`$ or $`a=p-1`$, and 304 otherwise.
It is an inexpensive heuristic based on public structure. It is neither the
actual provider invoice nor a proved value-of-information calculation.

The correct loss multiplier is $`1-\gamma_J\ell_{J,i}`$, where

```math
\gamma_J=\frac{\pi_J^{-1}-1}{HK}
=\begin{cases}
\dfrac{B-1}{(B+1)H^2},&J=f,\\
\dfrac1H,&J\ne f.
\end{cases}
```

Integer numerators and denominators implement these factors before fixed-mass
normalization. The largest denominator is
$`D=(B+1)(2B-1)^2<2^{32}`$ for the admitted $`B\le1024`$.
The normalization numerator is at most $`M^2D`$. The allocation comparison is
bounded by $`304M^2`$, and forecast shifts by $`M2^h`$. All three quantities,
the public block buffer and the separate 95-bit sampler transient appear in
the declared capacities and charged implementation. Total supplied bits are
$`m\log_2(2B)+Th`$.

The guarantee belongs to the trusted `execute` broker, which supplies the
selected position's actual ticket multiplicity. The low-level methods are
not an authentication layer for arbitrary external propensity claims. A
future independently exposed receipt/selection API must bind that state.

### 7.2 Actual fees and forecasts under adaptive selection

For fixed cold request bills $`f_t`$, expected purchase expenditure is

```math
\mathbb E\sum_k f_{J_k}
=\mathbb E\sum_k\sum_{t\in\mathcal B_k}\pi_{k,t}f_t. \tag{13}
```

For a given block this is half its uniform mean fee plus half the favorite's
fee. Across adaptive histories, the outer expectation remains. Summing the
conditional fees along one realized history does not integrate all histories.
The full value bound adds S and expected actual allocation/controller costs
to c times (12) and (13); its hard resource budget reserves 1,088 units for
each of the exactly m purchases. Looking up an already computed invoice is
not a free way to discover an unresolved mathematical answer's cost.

The uniform all-issued Brier identity in (10) cannot be reused. A safe adaptive
bound adds at most m ideal mixture losses for the purchased positions, then
uses convexity and probability rounding:

```math
\mathbb E\sum_t(q_t-y_t)^2
\le\min\left\{T,\ L_*+HK\log N+\frac{HmK}{2^s-1}+m+2T2^{-h}\right\}. \tag{14}
```

No additional binary-action rounding allowance is needed in (14): its
$`2T2^{-h}`$ term already covers the emitted forecast. The independent
[adaptive reconstruction](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/literature_agent/adaptive_quota_review.md)
checks the selection proof and preserves an exact failure witness for omitting
propensity.

## 8. Numerical guarantees available before private evaluation

The theorem's $`L_*`$ is defined by the complete deterministic tape. It can
be evaluated retrospectively after a private evaluator computes all answers,
but the live learner has not acquired that information. A valid numerical
admission certificate must use a bound available under its own information
contract.

The four-expert library contains both constant guesses. Their losses sum to
T on every binary tape, so **$`L_*\le T/2`$ is known from the source alone**.
Substituting this value into (8) or (12), then clipping at $`T-m`$, gives a
label-free expected terminal-loss envelope. In the uniform B=2 case the
first-order contribution is $`3T/8`$; for B at least four it is $`T/2`$.
The logarithmic and finite-representation allowances still have to be added.

If G is that expected task-loss envelope and the common resource price is
lambda, an all-in expectation cap is `c G + lambda C_funded`. For different
nonnegative category prices, the safe scalar replacement is
`c G + max_j(lambda_j) C_funded`, or a tighter priced categorywise envelope
when one is available. Resource units are not added directly to task-loss
units. This avoids running every candidate answer service to price it and is
conservative:
reservations can substantially exceed actual debits. A private evaluator's
smaller $`L_*`$ and potential invoice table can tighten a retrospective
comparison, but they are not inputs to the deployed purchase decision. A
fallible prediction of comparator quality cannot replace a certified upper
bound without an additional error argument.
The corresponding pathwise cap uses `c(T−m)`, not the smaller expectation
envelope `c G`. A hard resource budget and an expected decision-loss guarantee
are different parts of the result.

### 8.1 Choosing precision from a declared allowance

Write $`A=(B-1)mK`$ for uniform selection, or $`A=HmK`$ for the ticket
extension. For positive target allowances $`\varepsilon_s,\varepsilon_h`$,
choose integers satisfying

```math
2^s\ge 1+A/\varepsilon_s,
\qquad
2^h\ge (T-m)/\varepsilon_h,
\qquad s,h\ge1.
```

Then the state and action approximation terms are at most their targets.
Integer comparison can choose the ceilings exactly, without a floating-point
rounding decision. The executable limits $`s,h\le32`$ must still be met.
For a four-expert state, the alternative $`h\ge s+2`$ makes the action
probability exact, at the price of more supplied and consumed random bits.

At fixed B and a fixed desired *total* approximation allowance, state precision
need grow only logarithmically with T; it need not follow the linear exact
weight-bit growth. At fixed s, only the **weight state** has size independent
of T. The preloaded random-bit tape, emitted records and the supplied request
tape still scale with the admitted horizon. No constant-total-memory or
physical-heap theorem follows from the fixed-mass construction.

### 8.2 Previously proved answers and the hard-information interface

A learned forecast is a fallible score. It is not a replacement for a
version-matched proved answer already retained by the larger reasoner.
The current standalone learner deliberately has no answer cache, so it must
not be described as a complete implementation of the phase's hard-evidence
update duty U04. The checked receipts and pre-issued forecasts remain distinct.

There is a simple safe composition fact. Keep the exact same purchase/update
process and raw forecasts, and let an additional sound, paid mechanism replace
an action by the known correct answer, or issue a 0/1 forecast from a
version-matched answer **already available before that forecast is issued**.
The latter is an alternative prospective output; an earlier issued forecast
is never overwritten for scoring. Each such replacement weakly reduces its 0–1 or Brier loss
pointwise. Therefore the corresponding task-loss upper bounds survive; the
additional mechanism's actual resource costs must be added to the bill.
No new truth need be inferred from a forecast for this argument.

This fact does **not** authorize skipping a scheduled purchase and assigning
its budget elsewhere under the old sampling proof. Nor does it authorize
changing the expert weights, the loss objective or the public tape using
current feedback. Those changes can alter the comparator or conditional
selection law. The full cache/hard-state/portfolio integration remains P3-08
work and is not executed by this recurrence.

## 9. Concrete failures that the integration must avoid

The following are mathematical separators, not hypothetical objections or
extra random-seed evidence. The [independent block review](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/proof_agent/review.md),
[greedy-action review](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/proof_agent/greedy_boundary_review.md)
and [propensity witness](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/literature_agent/adaptive_quota_review.md)
retain their exact constructions.

| Changed contract | Finite witness | Consequence |
|---|---|---|
| Update immediately after the selected label inside a block | Two constant experts; B=2; labels `(0,1)`; learning rate 1/2. Expected unbought loss is 7/12, while the proposed frozen-block selected-loss expression is 1/2. | The frozen-mixture identity cannot price later predictions changed by that block's purchase. |
| Let current requests depend on the already revealed selector history | One constant-zero expert; first label 0; second label 1 exactly when the first position was bought. Selected loss is always zero; expected unbought loss is 1/2. | The exogenous-table assumption is substantive even when updates are delayed. |
| Move a hindsight minimum through expectation | Random comparator losses `(Z,1−Z)` with fair Z have minimum zero, but each expected loss is 1/2. | A fixed-expert bound against `min_i E L_i` is not a random-hindsight bound against `E min_i L_i`. |
| Ignore purchase propensities | B=4, selection probabilities `(5/8,1/8,1/8,1/8)`, repeated labels `(0,1,1,1)`, 64 blocks. | Unweighted updates give expected regret above 64.26179846, violating the proposed `49 log 2 < 34.3` allowance; the corrected update gives regret near −9.16553353. |
| Replace randomized action by a greedy threshold | Sixteen B=4 blocks alternate the real queries `(p=17,a=2)` and `(p=17,a=6)`. Both have expert row `(0,1,0,1)`, but opposite answers. | Greedy makes 48 unbought errors; every fixed expert loses 32 on the full tape. Regret 16 exceeds the complete fixed-state/action allowance below 12.603. |

The last example concerns the actual four-expert advice family. A tie chooses
zero; after a true block the mixture favors one, so the next false block is
also wrong. The proved randomized action avoids this deterministic pattern.
Encoding a forecast as two estimated action losses does not transfer the
randomized regret theorem to their pointwise minimizer. A well-specified
subjective probability model would pose a different decision problem; this
separator does not claim that greedy Bayes actions are generally irrational.

### 9.1 Finite precision also has a lower boundary

On a repeated true query, the constantly wrong zero expert retains positive
weight at every finite time. Consequently the raw action-one probability is
less than one. Downward h-bit rounding gives $`q_t\le1-2^{-h}`$, so

```math
\mathbb E L_{\rm terminal}\ge (T-m)2^{-h}
```

on this tape, even though a fixed expert has zero loss. With positive
fixed-mass weights, the wrong expert has at least $`1/M`$ mass and the stronger
lower bound is $`(T-m)\max\{1/M,2^{-h}\}`$. The admitted query
$`p=17,a=1`$ realizes the true label and expert row `(0,1,1,1)`.
This is a direct analytic construction; no selection of a lucky error trace
is needed.

Therefore fixed action precision, as well as fixed state precision, limits
an unqualified asymptotic claim. The current executable admits only a finite
horizon up to 8,192; the construction explains what would happen if a family
of larger horizons retained the same precision. Raising precision or using a
sound known-answer override changes that conclusion through an explicit
mechanism. The existing finite upper bounds already charge these errors.

### 9.2 An action lottery's value need not identify truth probability

If an additional coherent subjective law assigns truth probability p, an
independent binary action lottery with probability q of action one has
expected zero–one loss

```math
q(1-p)+(1-q)p=q+(1-2q)p.
```

With known q and this exact payoff model, the scalar can distinguish arbitrary
admitted p values when $`q\ne1/2`$. At q=1/2 its value is always one-half,
so any two distinct admitted p values collide. Independent correction
with probability pi and known stake c multiplies the variable term by
$`c(1-\pi)`$; zero stakes or certain correction also remove identification.
Known additional resource costs must first be separated. In general the
coefficient $`c(1-\pi)(1-2q)`$ must be nonzero for this scalar to add
identification on a nontrivial source. If hard evidence already fixes p,
that evidence still identifies it even when the scalar is constant.

This conditional identity applies the earlier probability-information
contract to the new randomized service. It does not assign a new probability
law to deterministic mathematics. In particular, the learner's action
probability, a forecast scored by Brier loss, an upper regret envelope and a
checked mathematical answer are different objects. A scalar all-in bill
cannot simply be inverted as though it were the expected loss of relying on
one uncorrected proposition.

## 10. What the development evidence actually shows

The public mathematical family has 248 queries: each nonzero residue a for
$`p\in\{17,31,47,61,97\}`$, asking whether
$`a^{(p-1)/2}\bmod p=1`$. Four cheap source-fixed experts predict zero, one,
the low bit of a, and whether $`2a<p`$. The public tape follows index
$`(73t+19)\bmod248`$ in the ordered family; its generator computes no labels.
The main horizons, 992 and 3,968, cover four and sixteen complete domain cycles.

The [uniform comparison](../work_logs/R_P3_B_A_2026-10-09_S1/development/service_comparison/analysis.md)
completed 16 planned main arms and four planned variation arms, plus eight
ordinary exact-control runs. The [adaptive comparison](../work_logs/R_P3_B_A_2026-10-09_S1/development/allocation_comparison/analysis.md)
completed its three separately specified arms. All are DEVELOPMENT. Complete
source snapshots, failed preliminary probes, actual invoices, immutable public
transcripts and subsequent private evaluator records are retained.

The uniform batch executed core v1.1. Core v1.2 only adds an initial funding
failure annotation and changes its version marker. Independent comparison
verifies identical successful-path operations; its source registry costs 26
more units. The following uniform **v1.2** costs are explicit setup-only
transfers of those observations, not relabelled reruns. The adaptive rows
were actually executed under current v1.2.

| T=3,968 method | Cold resource units | Terminal errors in saved trace | Interpretation |
|---|---:|---:|---|
| Uniform B=8, exact integer weights | 2,935,924, derived | 1,703 | Exact weights; growing integer cost. |
| Uniform B=8, fixed state s=16 | 1,039,136, derived | 1,702 | Smaller representation cost; explicit rounding allowance. |
| Adaptive tickets B=8, fixed state s=16 | 1,382,703, observed | 1,754 | Pays for lookahead and allocation; different learning rate and bit schedule. |
| Direct fast exact action | 355,613, observed | 0 | Ordinary public mathematical shortcut. |
| Initially empty semantic cache | 178,636, observed | 0 | Pays for cold exact entries and later reuse. |
| Quadratic-residue table | **171,880, observed** | **0** | Pays for exact construction and all lookups. |
| Checked always-BUY | 1,134,013, observed | 0 | Pays for every cold checked answer. |

At B=8, bounded weights reduce the observed uniform resource bill by about
64.6%; peak retained weight width falls from 1,342 to 18 bits. This is a
representation result. It does not establish better forecasts, equal weight
trajectories or identical actions. The source-fixed numerical error allowance
is what licenses the bounded implementation.

The adaptive selector buys 8,227 fewer fee units on the longer saved path, but
raises total cost by 343,567 units against the current uniform counterpart.
Its other two paths show the same qualitative fee/overhead difference.
These are realized comparisons, not estimates of unconditional savings caused
by allocation. The learning factors and bit schedules change together.
No tuning, new seeds or hidden retries were used to find a favorable path.

### 10.1 Forecast quality is a separate comparison

A constant forecast of one-half has Brier loss exactly one-quarter on every
binary question, regardless of its answer. A post-run analytic diagnostic
therefore supplies a strong label-free reference, without executing another
method or using hindsight to select a parameter.

| T=3,968, B=8 | All-issued Brier score | Conditional expected terminal errors |
|---|---:|---:|
| Analytic q=1/2 reference | **992** | 1,736 with the same purchase count |
| Uniform fixed-state trace | 1,418.954973 | 1,676.901886 |
| Adaptive fixed-state trace | 1,134.448268 | 1,727.731979 |

The learner rows' conditional action means integrate only the action bits
along each realized selector/feedback path. Their state and invoice do not
depend on sampled actions. Those quantities are not the unconditional theorem
expectation over all selector histories. The null action comparison can retain
the exact same complete invoice as an output-substitution diagnostic; a
separately optimized cheap null policy was not executed or priced here.

All six adaptive/matching-uniform Brier scores inspected in that diagnostic
exceed T/4. Lower adaptive Brier relative to uniform therefore supplies no
forecast-superiority claim. Both longer-tape conditional terminal means are
below the fair-coin reference, but this does not establish a general or
causal decision advantage. The exact table remains the strongest completed
ordinary economic control.

## 11. A cost obstruction beyond the recorded seeds

The table computes the same deterministic answer on every admitted input.
For an odd prime p, the nonzero squares are exactly the solutions of
$`x^{(p-1)/2}=1`$: Fermat's identity makes every square a solution; the
$`(p-1)/2`$ distinct squares exhaust the roots of that nonzero polynomial
in the field. Enumerating $`j=1,\ldots,(p-1)/2`$ gives one representative
of each square. The implementation verifies the listed primes by paid trial
division and uses six 64-bit table words. Construction costs 1,611 units;
its finite-domain correctness argument is in the
[service design](../work_logs/R_P3_B_A_2026-10-09_S1/reviews/service_agent/design.md),
and the construction charge and complete actual invoices are preserved in the
[executed comparison](../work_logs/R_P3_B_A_2026-10-09_S1/development/service_comparison/run_001/result.json)
and its [analysis](../work_logs/R_P3_B_A_2026-10-09_S1/development/service_comparison/analysis.md).

Let A(q) be the family-admission cost shared by the expert evaluator and table
lookup. The implemented expert call costs A(q)+9 and table lookup A(q)+10.
Every learner round also pays 12 close/identity units. Dropping all other
nonnegative learner costs therefore gives

```math
R_{\rm learner,ongoing}-R_{\rm table,lookups}
\ge11T+R_{\rm purchases}. \tag{15}
```

This is a source-level inequality on every successfully completed admitted
tape, independent of favorable seeds. Current uniform registry cost is 18,996;
table registry is 12,477. Including table construction gives

```math
R_{\rm uniform,cold}-R_{\rm table,cold}
\ge4908+11T+R_{\rm purchases}. \tag{16}
```

The adaptive registry costs 22,897, so its corresponding constant is 8,809.
Its extra allocation work is nonnegative and (15) still applies. The table's
source-reconstructed event and unit envelopes fit its existing finite meter
through the admitted horizon 8,192; it is an available control, not an
unfunded mathematical oracle.

For any fixed common primitive price $`\lambda\ge0`$ and terminal-error
price $`c\ge0`$, the table has zero task loss and no larger all-in cost;
its resource inequality is strict when $`\lambda>0`$. This rejects this
particular learner deployment for this terminal-answer service and tariff.
It does not reject selective learning for every mathematical family.

### 11.1 Setup, prices and equal outputs

There are two distinct setup sensitivities. If both source registries are
already available or excluded, (15)'s 11T term alone covers the table's 1,611
construction units at $`T\ge147`$; the first legal even horizon is 148.
If all learner setup is waived while the table pays its full registry and
construction, the table owes 14,088 units. The same 11T-only argument then
requires $`T\ge1281`$, with first legal even horizon 1,282. Actual purchases
make both inequalities stronger. At the observed 992-round arms, the minimum
uniform purchased bill is already 17,510, so even that asymmetric comparison
has a lower positive margin of 14,334 units. That last number is a saved-path
calculation, not a minimum proved over every possible selector history.

An earlier review wording conflated construction-only sensitivity with the
full standalone bill. Its additive correction and the clarified analysis
preserve the original evidence. Equations (15)–(16) and all measured costs
are unchanged.

The common-unit-price result is not a claim of coordinatewise dominance.
The [signed resource audit](../work_logs/R_P3_B_A_2026-10-09_S1/development/price_and_precision_audit.json)
finds that the reference uniform learner uses 11,408 fewer units in the
`cache` category than the table, while its total bill is much larger. Some
B=16 rows also use fewer `solve` units. Different category prices can change
the ordering and require the actual signed scalar product. Repricing a fixed
transcript does not simulate a changed price-dependent acquisition rule.
These tariffs are declared accounting units, not measured hardware prices.

The measured controls deliver correct terminal answers. Their service does
not promise an independent checked proof object on every request. If that
becomes a deployment requirement, every method needs the same certificate
contract and its own revised cost. That is the retained optional equal-delivery
comparison, not a reason to remove the current legitimate terminal control.

Merely requiring the table also to emit an exact forecast and its terminal
action does not explain the learner's gap. As a source-derived sensitivity,
charge the table an extra 24 output units per query, matching the learner's
16 forecast/action words and eight terminal words. Reintroducing that
previously dropped 24T learner output debit into (15) cancels this surcharge,
leaving the same 11T-plus-purchases margin. This is an algebraic equal-emission
comparison, not an executed proof-certificate service or a hardware claim.
Both sides still require the same interpretation of the emitted output fields.

## 12. A stronger learning-rate option, without a new experiment

The performed runs retain their prospectively fixed learning rates. There is
also an analytic option for a future source-bound configuration. For
$`0\le u\le\eta<1`$,

```math
-\log(1-u)\le u+\frac{u^2}{2(1-\eta)}.
```

Expand the positive logarithm series; every coefficient from the quadratic
term onward is at most one-half. Apply this inequality to
$`u=\eta Z_i`$, with $`Z_i=X_i/H`$ from §7. The selected-loss potential
becomes

```math
\sum_k\langle p_k,X_k\rangle
\le\sum_kX_{k,i}+\frac{H\log N}{\eta}
 +\frac{\eta}{2H(1-\eta)}\sum_kX_{k,i}^2.
```

The conditional comparator coefficient is at most one when
$`\eta H\le2(1-\eta)`$. Choosing $`\eta=2/(H+2)`$ therefore gives an
ideal terminal allowance $`H(H+2)\log N/2`$ and fixed-state allowance
$`H(H+2)m/[2(2^s-1)]`$. Uniform sampling has $`H=B-1`$, giving
$`(B^2-1)\log N/2`$ in place of the simpler conservative allowance.
For B=2, a smaller first-order coefficient from the performed rate can still
be better for a particular certified comparator bound.

This is a mathematical parameter option, **not a selected improved policy**.
No tape, seed, forecast or cost observation is relabelled to use it. Its
integer factors and arithmetic envelope must be checked before execution:
for the adaptive ticket version, a straightforward common denominator already
exceeds $`2^{32}`$ at B=1,024. The existing denominator cap cannot be copied.
The [refinement record](../work_logs/R_P3_B_A_2026-10-09_S1/development/binary_potential_refinement.md)
separates this option from the tighter certificate for the unchanged algorithm.

## 13. Consequences for the five questions and the next boundary

| Primary question | What this recurrence adds | What remains open |
|---|---|---|
| Q1: reasoning about unresolved mathematics | A finite procedure issues forecasts and decisions on true and false mathematical queries while learning only from purchased answers; its feedback, bit, precision and budget assumptions are explicit. | General logical induction, coherent joint beliefs, and a complete hard-evidence update system are not supplied by this standalone forecaster. |
| Q2: logical counterfactuals | The new service gives a precise policy and value interface that a later hypothetical comparison must preserve. | No new counterpossible semantics, policy robustness or discovery of relevant assumptions is established. |
| Q3: several useful models | Multiple fixed experts can be combined with a paid-feedback guarantee; fixed state reduces the cost of that particular combination. | The strongest ordinary exact method wins the selected service. No affirmative practical advantage for these fallible models over that method is shown. |
| Q4: improving usefulness estimates and choosing reasoning | The all-issued paid-feedback gap has a proved restricted bridge, with exact quota, adaptive propensity repair, a complete resource bill and explicit forecast/action distinctions. | The tested forecasts do not beat the half-probability Brier reference; learned acquisition value and broader deployment benefit need stronger evidence. |
| Q5: probability information in values | The emitted action probability, forecast score, task-loss envelope, exact receipt and resource bill retain separate meanings; a randomized value can erase truth-probability information. | No scalar aggregate value universally identifies a mathematical belief law. |

The supported object is a **bounded formal adaptation and implementation
synthesis**: a complete selective-feedback/terminal-decision/resource contract,
a finite-state guarantee, a propensity-corrected allocation extension and
consequential integration/cost boundaries. Ordinary learning, decision theory
and exact computation can implement the same construction. Its contribution
is neither a new generic algorithm nor an economic superiority claim. The
separate contribution assessment applies the author's broad criterion and
leaves the later author gate intact.

For P3-08, the resulting interface should retain the immutable issued forecast,
actual randomized action, selected propensity, quota, settled feedback,
precision allowance and complete invoice. Version-matched hard facts can
supply prospectively timed corrections; alternate greedy actions, changed
loss prices or adaptive experts need their own guarantees. The exact table,
cache and a proper forecast null remain legitimate comparison components.
Binding a prepared allocation to a reusable public low-level API is additional
integration work, not a guarantee supplied by the current trusted broker.

**Recommended next item: P3-08 after this recurrence's boundary. It remains
unstarted.** If the intended final service requires equivalent independently
checked certificates, the existing optional equal-delivery recurrence is
useful before the P3-09 freeze. Further tuning on this easy 248-query table is
unlikely to answer Q3 better than selecting a genuinely discriminating service
and preserving its strongest public shortcuts. Neither that further recurrence
nor the next task is selected by this document.
