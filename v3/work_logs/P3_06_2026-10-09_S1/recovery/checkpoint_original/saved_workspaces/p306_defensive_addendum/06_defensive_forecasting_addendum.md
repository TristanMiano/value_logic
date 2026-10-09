# P3-06 continuation — a common scalar forecast for expert regret and calibration

Contributor: **ChatGPT (GPT-6 Astra Pro)**. New supplementary derivation,
October 8, 2026. **Status: mathematical addendum; source comparison, integration,
current execution results and task closing records still require verification.**
This file is not a replacement for the interrupted P3-06 manuscripts or clocks.
The method is a reconstruction of a defensive-forecasting style construction;
no priority or general Logical Induction claim is made.

## 1. Exact question and input contract

Can the same scalar prediction, rather than a distribution over different
reports, support both finite-expert squared-loss regret and a specified finite
class of calibration tests? The earlier session reported a finite-grid branch
whose distributional calibration did not establish calibration of its mean.
The construction here addresses that distinction directly.

Round t presents a versioned deterministic mathematical query, N supplied
expert probabilities q(t,i) in [0,1], and a known nonnegative finite weight w(t).
The learner issues p(t) before its individual binary answer y(t) is received.
Expert calculations and the learner's arithmetic must be charged; an expert
already containing an arithmetic identity is not an identity discovered by
this update. Truth is not randomized by the forecast representation.

For now each copy of the learner waits for its outstanding answer before
issuing another prediction. Section 5 supplies a multi-copy delayed interface.
No outcome is fabricated when a query remains unresolved. The finite expert
library, score, calibration functions and scope are explicit inputs, not a
universal hypothesis class. The arithmetic implementation uses exact rationals;
that does not add a new inference rule to the inherited native proof language.

## 2. A vector potential

Fix positive feature scales alpha and beta. Let b(j,p), j=0,...,m, be continuous
triangular functions centered at j/m:

```math
b_j(p)=\max(0,1-m|p-j/m|).
```

They are nonnegative and sum to one on [0,1], so their squared sum is at most
one. At a prediction round use the feature vector

```math
\Phi_t(p)=w_t\bigl(
 \alpha(q_{t,1}-p),\ldots,\alpha(q_{t,N}-p),
 \beta b_0(p),\ldots,\beta b_m(p)\bigr).
```

All quantities entering this vector except its candidate p are available
before y(t). With only the earlier received outcomes, set

```math
R_{t-1}=\sum_{s<t}(y_s-p_s)\Phi_s(p_s),
\qquad
S_t(p)=\langle R_{t-1},\Phi_t(p)\rangle
       +\tfrac12(1-2p)\|\Phi_t(p)\|^2.
```

Use p=0 when S(0)<=0, and otherwise p=1 when S(1)>=0. Otherwise S(0)>0>S(1),
and continuity guarantees an interior zero. Exact root evaluation is not
assumed. The finite implementation bisects the sign bracket using rational
arithmetic, returning its actual residual when its work allowance expires.

For any issued p, define a nonnegative, outcome-independent allowance

```math
A_t=2\max\{0,(1-p_t)S_t(p_t),-p_tS_t(p_t)\}.
```

The endpoint choices have allowance zero. A residual bound |S(p)|<=delta
implies A<=2 delta. An unsuccessful root search does not acquire that bound by
being called successful: the actual rational A is stored with the report.

**Proposition DF-1 (pathwise potential).** For every received binary sequence,

```math
\|R_T\|^2\le
 \sum_{t\le T}p_t(1-p_t)\|\Phi_t(p_t)\|^2
 +\sum_{t\le T}A_t =: B_T.
```

**Proof.** Write e=y-p. For a binary y,

```math
e^2=p(1-p)+(1-2p)e.
```

Thus the increment in the squared residual norm minus the displayed variance
term is

```math
2e\langle R,\Phi\rangle+(e^2-p(1-p))\|\Phi\|^2
 =2eS(p)\le A_t.
```

The last inequality checks exactly the two possibilities y=0,1. Sum the
increments from the initial zero vector. This proof is algebraic and does not
require a stochastic outcome law, independence, or accurate experts.

The weight/feature bound gives

```math
B_T\le\tfrac14(N\alpha^2+\beta^2)\sum_{t\le T}w_t^2
       +\sum_{t\le T}A_t.
```

## 3. The two duties apply to the same p

Define L= sum w(p-y)^2 and L(i)= sum w(q(i)-y)^2. The expert coordinate obeys

```math
L_T-L_{T,i}
 =\frac{2}{\alpha}R_{T,i}
  -\sum_{t\le T}w_t(q_{t,i}-p_t)^2
 \le\frac{2\sqrt{B_T}}{\alpha}.
```

This follows by expanding the two squares, retaining their shared outcome.
It is a comparison to each fixed supplied expert, hence also to the best
fixed member of that library. It is not a comparison to a free per-round
oracle or every computationally bounded strategy.

The calibration coordinate simultaneously gives

```math
\left|\sum_{t\le T} w_t b_j(p_t)(y_t-p_t)\right|
 \le\frac{\sqrt{B_T}}{\beta}.
```

These are finite continuous-bin calibration residuals for the issued scalar
p itself. No independent random report is sampled and no mean-of-reports
substitution is involved. A conditional-bin error divides by
sum w b(j,p), not automatically by the total number of rounds. Rarely occupied
bins can therefore have weak conditional bounds. The result does not imply
calibration for arbitrary discontinuous/adaptive selections or every context.
Extra predictable continuous context features can be added, with their norms
included in the same potential; no such extension is silently assumed here.

For W=sum w>0, a sufficient condition for both displayed residuals divided by
W to vanish is sum w^2=o(W^2) and sum A=o(W^2). Bounded weights with a
nonvanishing average and bounded per-round absolute root residual satisfy
these conditions. Finite weights need not be uniformly bounded, but a single
dominating stake can prevent the normalized conclusion.

**Do not confuse two approximation allowances.** An additive per-round
*loss* error in a projection-based regret proof typically needs a sublinear
cumulative loss allowance. Here A is an increment of a *squared vector
potential*, followed by a square root. Its sufficient asymptotic condition is
sum A=o(W^2), not automatically sum A=o(W). A fixed root-search work budget,
however, does not ensure bounded absolute residual as R grows. The recorded
allowance, not the step count alone, decides whether the bound is useful.

## 4. Finite computation of the report

With the triangular features, S is continuous and piecewise cubic. It can be
evaluated exactly at rational p. Bisection does not require monotonicity:
retaining opposite endpoint signs preserves an interval containing a root.
For a requested positive residual tolerance, continuity ensures eventual
success if work is allowed to increase.

A quantitative bound is available without an exact algebraic-root primitive.
If each feature coordinate is bounded by M(k) and has Lipschitz constant
D(k), then a valid score Lipschitz constant is

```math
L_S=\sum_k\bigl(|R_k|D_k+M_k^2+M_kD_k\bigr).
```

Apply the product rule inside each linear-feature piece and then join the
pieces by continuity. After k bisections the midpoint is within
2^(-k-1) of some root, so a score residual at most L(S)2^(-k-1) suffices.
Expert coordinates allow M=D=alpha w; calibration coordinates allow
M=beta w, D=m beta w. All these bounds are available before the outcome.
This is a rational-operation bound, not a fixed-bit-cost CPU or RAM theorem.
Exact numerator/denominator growth and retained histories must be accounted
for separately. The supplementary implementation records score evaluations,
bisection count and actual allowance, not a total resource guarantee.

## 5. Delayed and missing proof feedback

Allocate each new query to an idle copy. A copy cannot issue another forecast
until its outstanding label is admitted. Create a new copy only when none is
idle. Each copy runs exactly the preceding algorithm on its own subsequence.
Expert forecasts may use any information legitimately available at issue;
copy-local updates do not receive another copy's unreturned labels.

For K used copies, summing residual vectors and applying Cauchy--Schwarz gives

```math
\left\|\sum_{k=1}^K R^{(k)}\right\|^2
 \le K\sum_{k=1}^K B^{(k)}.
```

Consequently the same global expert and calibration bounds hold with B
replaced by K sum B(k). Each fixed expert keeps the same index across copies.
The number of copies is bounded by one plus the maximum number of already
outstanding queries at an issuance, but K and their memory/work are costs,
not free parallel performance.

For a complete scored prefix whose outcomes have all eventually arrived,
this proves the stated prefix guarantee. At an intermediate cutoff it covers
only the settled subsequences. Pending predictions stay immutable and have
no fictitious losses. No statistical claim about the unresolved population
follows from their omission. Action-dependent proof acquisition may still
satisfy the algebra on settled rounds, but does not itself bound K, ensure
coverage, or establish a useful paid-discovery policy. An adversarially growing
number of copies can erase the desired sublinear rate. Such policy questions
remain P3-07, not a consequence of this wrapper.

## 6. From weighted forecasts to decisions

Suppose the supplied action losses on one binary outcome are
c(a,y)=b(a)+d(a)y, with known coefficients in a common unit. Select a minimizer
of b(a)+d(a)p using an announced tie rule. Put D=max d(a)-min d(a).
For an outcome-optimal action a*,

```math
0\le c(\widehat a,y)-c(a^*,y)
 \le(d_{\widehat a}-d_{a^*})(y-p)
 \le D|y-p|.
```

The first upper bound subtracts the nonpositive difference of the two forecast
costs. It respects shared cost components instead of separately bounding every
action. With weights w=D across rounds, Cauchy--Schwarz gives

```math
\sum_t\mathrm{regret}_t\le
 \sqrt{\left(\sum_t D_t\right)
             \left(\sum_t D_t(p_t-y_t)^2\right)}.
```

If a supplied expert has weighted squared loss o(sum D), and the preceding
weighted expert-regret bound is also o(sum D), the learner has normalized
vanishing outcome-oracle decision regret. This conditional result needs good
predictive structure; expert regret alone does not supply it. It also does
not include the cost of running the expert library, obtaining labels or solving
the finite minimization. Costs independent of which action is compared cancel
from this terminal comparison but remain relevant to a paid policy.

Unbounded known stakes may be treated through the displayed sums; no universal
rate follows when stakes concentrate. Unknown semantic loss coefficients,
uncertain payoff interpretations and multi-event correlations need the
separate P3-02/P3-04 information contracts. The scalar binary fragment is not
a universal value carrier.

## 7. Repricing and scope boundaries

A regret theorem proved for the issue-time weights is not a regret theorem
for arbitrary retrospective weights. For example two rounds with learner
squared errors (1,0) and expert errors (0,1) have zero unweighted regret;
weights (2,0) give regret two. Repeating the pattern makes the discrepancy
linear. This is an obstruction to the implication, not a trace asserted to
be produced by this algorithm.

Retaining old scalar cumulative regret alone cannot generally support a new
price schedule. Retaining immutable issue forecasts, expert values, resolved
answers, original weights and scoped loss coefficients permits honest
rescoring. It does not turn those old forecasts into the different forecasts
a retrained online algorithm would have issued under the new weights.
A changed interpretation or corrected answer must be separately versioned;
old scored records must not be silently edited.

## 8. Project disposition

This is a concrete candidate for U06 (learning which supplied predictor to
trust), U07 (finite continuous-bin calibration), U08 (finite-expert weighted
regret), U09 (explicit delayed copies and pending labels), and V03 (a
conditional terminal decision bridge). The proofs have the exact limited
quantifiers above. They do not establish universal LI inexploitability,
self-trust, non-dogmatism, arbitrary-language logical prediction, discovery of
new identities, a bounded value-of-computation policy, or a performance
advantage over ordinary defensive forecasting.

The important empirical comparison remains a strong ordinary implementation
on identical information/resources. The source/priority reconciliation should
include defensive forecasting, BRIA, delayed online learning, the interrupted
projection learner, and the finite-grid calibration branch. No newness is
inferred from giving the common scalar prediction a cost interpretation.
P3-N01 remains NOT YET SUPPORTED. P3-07 and all later gates are unstarted.

## 9. Evidence status of this addendum

`defensive_forecasting.py` is new supplementary code. Its checker writes full
new finite traces, exact invariant checks, source hashes, outcome coverage and
actual execution duration to `development_result.json`, retaining failures.
These are neither recovered earlier runs nor a final challenge. The current
conversation has not exposed its tool-returned results for inspection; an
unseen status is not reported as an observed pass. Research-time credit for
this addendum is zero pending any separately verified accounting. The earlier
P3-06 files and raw clocks must be inspected before task closure, without
inventing the interruption interval or replacing the original forecast.
