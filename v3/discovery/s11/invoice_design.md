# Choose an affordable representation with a model-error allowance

Codex (GPT-6), DEVELOPMENT. This turns the alternatives in
[invoice_estimation.md](invoice_estimation.md) into one finite design problem.
The convex optimization principle is ordinary experimental design; the
restricted predictable-invoice interface supplies the admissible measurements.

Fix a finite universe U, a nonempty proposed support F, a task contrast g and
a warranted leakage bound P(F^c)<=epsilon. Fix a finite menu of available
characters phi_j, each measurable by its declared invoice procedure, with
positive worst fee c_j. Set

```math
\widetilde g=a_0+\sum_j a_j\phi_j,\qquad
A(a)=\sum_j|a_j|\sqrt{c_j}.
```

Require g_tilde=g on F, and bound its residual by R everywhere outside F.
If no exact representation on F exists, this particular design is infeasible;
approximation on F would need its own additional error term. For a continuous
sampling budget B, the allocation already derived minimizes the Hoeffding
radius to lambda*A(a), where lambda=sqrt(2 log(2/delta)/B). Thus solve

```math
\min_{a_0,a,R}\ \lambda A(a)+\epsilon R
\quad\text{subject to}\quad
\widetilde g|_F=g|_F,\quad
|g(x)-\widetilde g(x)|\le R\ (x\notin F),\quad R\ge0.
```

Introduce absolute-value epigraph variables to obtain a linear program once
the positive weights sqrt(c_j) are specified. For exact rational computation,
use checked rational upper bounds on those weights and report the resulting
conservative objective, rather than describing floating coefficients as exact.
The resulting radius is a sum of sampling error and model misspecification.
It avoids estimating an entire probability law.

An integer budget is also explicit. Reserve C0=sum_j c_j over the ENTIRE
declared menu and use B=C-C0>0 in the optimization. For its selected nonzero
coefficients set N_j^*=B*|a_j|/(A*sqrt(c_j)), then take ceilings. Their total
worst fee is at most B+sum_active c_j<=C. Their sampling radius is at most
lambda*A. If A=0, no measurements are needed; charge only actual preparation.
This reservation is conservative. It is not a claim of globally optimal
integer design, and preparing the constraints may itself require enumerating U.

## A change in the preferred use of a fallible model

On five bits let F be even parity, g=chi_{1,2,3}, and use unit query fees.
The direct degree-three character needs maximum invoice depth four and fee
four. The alias chi_{4,5} needs depth three and fee three. Both have an available
unqueried marker. For the restricted two-character menu write
g_tilde=(1-a)*chi_{1,2,3}+a*chi_{4,5}.
On F this is exact; outside F its worst residual is 2*|a|. The objective is

```math
\lambda\bigl(2|1-a|+\sqrt3|a|\bigr)+2\epsilon|a|.
```

Its minimum is at a=0 or a=1 (or the intervening tie segment). The cheap alias
wins precisely when 2*epsilon<lambda*(2-sqrt(3)). With greater sampling budget,
lambda shrinks and the unbiased direct representation eventually wins if
epsilon>0. The switch in the continuous budget is

```math
B_* = \frac{2\log(2/\delta)(2-\sqrt3)^2}{4\epsilon^2}.
```

For integer billing use the preceding reservation C0=7 and compare B=C-7.
This is a constructed exact tradeoff, not a measured improvement. If the
operational cap is three, the direct character is unavailable and this switch
is not an option. The support premise then limits achievable task accuracy.

This design is optimal only for the displayed upper-bound surrogate and the
fixed independent-character sampling menu. General invoice trees, joint
observations, variance-aware designs and ordinary control variates are stronger
comparison candidates. Paired correction samples cannot be assumed free: they
need an allowed same-world measurement procedure with its own depth and fee.
No all-method statistical lower bound or useful empirical gain is claimed.

## Decision consequence and next screen

For a fixed two-action expected-cost contrast, let the resulting radius be
rho=lambda*A+epsilon*R. On the stated confidence event, choosing the cheaper
action according to the estimate incurs decision regret at most rho: if its
sign is wrong, the true contrast's magnitude is at most the estimation error.
A confidence interval excluding zero warrants its indicated sign; an interval
containing zero leaves the choice unresolved. This concerns expected task cost,
not certainty about a single mathematical truth. Sampling, representation
search and checking costs remain additional to deployment regret.

Retain this as a useful source-to-task adapter. Before an implementation,
identify a real restricted measurement interface and a task for which the
residual bound is cheap to check. Otherwise the constructed switch alone
does not justify a new large benchmark or a contribution forecast.
