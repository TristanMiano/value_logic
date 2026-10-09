# Independent finite-menu repricing reconstruction

Contributor: **ChatGPT (GPT-6 Astra Pro), independent implementation reviewer**.
October 9, 2026 UTC. This is a separate extension experiment; the principal
scalar implementation has one issue-time weight profile.

## Result

The announced-menu version of CF-7 is valid. The
[`independent probe`](../development/independent_audit_v1/menu_extension_probe.py)
and its [`result`](../development/independent_audit_v1/menu_extension_result.json)
pass **63,127 exact checks**. The main menu run contains 64 binary-sequence
episodes, split between two and three profile blocks, and 2,624 retrospective
mixture evaluations, including choices selected after inspecting outcomes.
Every profile block uses the **same issued scalar forecast**.

The checks independently reconstruct both possible next potential increments,
profile-specific regret identities, direct rescoring from full tapes, and
rescoring from per-profile summaries alone. They verify both the manuscript's
nonnegative-coefficient bound and the sharper norm bound below. These finite
checks support the implementation correspondence; the general statement follows
from the displayed algebra, not from enumerating the coefficient grid.

## A sharper statement, including a larger valid coefficient domain

Let $`R_{r,i}`$ be the expert coordinate for profile $`r`$, and
$`C_{r,j}`$ its calibration coordinate. For any retrospectively chosen fixed
real coefficient vector $`\lambda`$, the exact identities are

```math
L(\lambda)-L_i(\lambda)
=2\sum_r\frac{\lambda_rR_{r,i}}{\alpha_r}
 -\sum_t w_t(\lambda)(q_{t,i}-p_t)^2,
\qquad
E_j(\lambda)=\sum_r\frac{\lambda_rC_{r,j}}{\beta_r}.
```

Here $`w_t(\lambda)=\sum_r\lambda_rw_{t,r}`$. Since these coordinates are
distinct coordinates of the common residual vector, Cauchy--Schwarz gives

```math
|E_j(\lambda)|\le\sqrt{B_T}
 \sqrt{\sum_r(\lambda_r/\beta_r)^2}.
```

This calibration inequality permits signed coefficients. If every resulting
weight on the evaluated tape is nonnegative, the distance term in the regret
identity is nonnegative, giving

```math
L(\lambda)-L_i(\lambda)\le2\sqrt{B_T}
 \sqrt{\sum_r(\lambda_r/\alpha_r)^2}.
```

Nonnegative coefficients are sufficient for this condition but are not
necessary. The valid domain can include the span of the declared profiles
intersected with nonnegative resulting weights. This does not cover arbitrary
unrepresented new weights. The coefficient vector stays fixed across rounds;
it is not a freely chosen separate coefficient vector for each outcome.

## Three distinct obstructions

**An original cumulative score loses information.** Two tapes with squared
errors $`(1,0)`$ and $`(0,1)`$ both have unit-weight score one. Under prices
$`(2,0)`$, their scores are two and zero. These tapes are information witnesses,
not claimed trajectories of the learning algorithm. Retaining the relevant
per-profile summaries resolves this ambiguity for the announced menu.

**Signed coefficients invalidate a naive signed sum in the original bound.**
An actual two-round, two-profile probe uses profiles $`(1,1)`$ and $`(1,0)`$,
then chooses $`\lambda=(1,-1)`$. The resulting weights $`(0,1)`$ are still
nonnegative. The sum of signed coefficients is zero, but regret to the zero
expert is $`7569/262144>0`$, and calibration residuals are nonzero. The correct
coefficient-norm bound passes. Signed coefficients themselves are therefore
not an impossibility witness; the false step is using a canceling signed sum
as an upper-bound factor.

**Negative resulting weights break the one-sided regret deduction.** On an
actual 64-round all-zero trace, taking the negative of the unit-weight profile
produces regret $`8349697/131072`$ against the constant-one expert, while
$`B_T=11754672229/8589934592`$. Its square exceeds $`4B_T`$. The originally
large negative regret reverses sign, and the distance term can no longer be
dropped. The signed calibration norm inequality remains valid.

The theorem snapshot, prospective probe plan, exact traces, chosen coefficient
vectors, interpreter, execution duration and source hashes are preserved in
[`independent_audit_v1`](../development/independent_audit_v1/). All are development
evidence with zero principal Research90 credit. No change to the main module is
implied by this independent extension.
