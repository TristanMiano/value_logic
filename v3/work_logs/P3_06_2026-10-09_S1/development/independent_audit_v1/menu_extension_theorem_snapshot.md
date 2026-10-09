# CF-7 theorem snapshot before independent extension probe



Retaining $`p_t`$ permits new known affine loss estimates for that same binary
answer. Retaining only an old cumulative weighted score generally does not
permit retrospective rescoring. For example, error vectors $`(1,0)`$ and
$`(0,1)`$ have equal unweighted sum and different scores under weights
$`(2,0)`$. Repeating the pair gives a linear discrepancy. This refutes the
implication from an old-weight regret guarantee to an arbitrary new-weight
guarantee; it is not asserted to be an algorithm-generated trace.

The general audit record retains immutable query/version, issued forecast,
expert vector, old weight, semantic loss rows, issue order and any checked
answer/receipt. It supports three different operations:

| Operation | Information and conclusion |
|---|---|
| Answer a newly priced affine loss query | Use the retained scalar forecast and new known row; it remains an estimate. |
| Rescore old issued predictions | Use their retained answers and new weights; report exactly that retrospective metric. |
| Rerun the learning procedure under new weights | Replay issue/feedback order, expert-input policy and parameter versions; this may issue different forecasts. |

No rescoring operation retroactively changes the forecasts or their proven
issue-time guarantee. A replay supplied with old expert vectors is only a
fixed-expert-tape replay if those experts originally depended on changed
learner outputs; full-policy replay needs their computations too. A changed
semantic interpretation or withdrawn answer requires a new episode or a
separately proved transport, not silent editing of settled history.

### A restricted positive transfer result

Suppose a finite menu of nonnegative weight profiles $`w_{t,r}`$ is declared
before each answer, and the feature vector includes expert/calibration blocks
for each profile with positive scales $`\alpha_r,\beta_r`$. The same
potential proof gives each profile its own coordinate regret/calibration
bound. For any fixed retrospectively selected $`\lambda_r\ge0`$, define
$`w_t(\lambda)=\sum_r\lambda_r w_{t,r}`$. Linearity gives, simultaneously,

```math
L(\lambda)-L_i(\lambda)
\le2\sqrt{B_T}\sum_r\frac{\lambda_r}{\alpha_r},\qquad
\left|E_j(\lambda)\right|
\le\sqrt{B_T}\sum_r\frac{\lambda_r}{\beta_r}.
```

This is **CF-7**, a finite-menu extension of the general feature theorem;
it does not cover arbitrary new per-round weights outside the predeclared
cone. For scoring alone, retaining per-profile losses and bin residuals is
sufficient for this menu, even if full history is absent. The kernel and
finite-menu information arguments are ordinary linear algebra; whether the
extra features are worth their time, memory and looser norm bound is separate.
The main executable prototype initially uses one weight profile; an independent
finite check will distinguish this theorem extension from that implementation.

