## 7. Two-sided reports can diagnose poor usefulness

An upper certificate can establish an acceptable performance ceiling. A lower
certificate can expose a procedure whose loss exceeds a declared reference.
The same centered construction supplies both, with an explicit larger error
allowance. Keep the fixed rate $`\lambda=8/R`$ and apply the conditional moment
argument to both signs with error $`1/80`$ per tail. Since
$`e^5>1097/12>80`$, define

```math
\rho_{\pm}=Q_m/R+5R/8,\qquad
 r_{a,\pm}=\left\lceil\sqrt{\left\lceil5(T-m)/2\right\rceil}\right\rceil.
 \tag{10}
```

The two sampling tails have total error at most $`1/40`$. The same event
bounds both $`V-U_c`$ and $`F-A_c`$ by absolute value, because they are equal.
The two conditional action tails also have total error at most $`1/40`$.
Thus, per declared episode at the fixed end,

```math
\Pr\!\left[
 |V-U_c|\le\rho_{\pm},\quad
 |F-A_c|\le\rho_{\pm},\quad
 |Z-U_c|\le\rho_{\pm}+r_{a,\pm}
\right]\ge19/20. \tag{11}
```

Here $`\rho_{\pm}\le9R/8`$, not necessarily $`R`$. This is a different
reporting rule from (8), not a free two-sided interpretation of that formula.
The shared sampling part has its fixed-rate prefix property; the complete
terminal statement remains fixed-end. A union over different arms, different
post-selected rates or additional procedures needs a separate allocation.

Intersect each interval with its public deterministic envelope. Besides (9),
use the corresponding minima of the two possible binary losses for $`V`$
and $`F`$, and zero for $`Z`$. If an intersection is empty, retain a confidence
conflict. Do not erase that row or attach ordinary valid better/worse labels
to the empty interval. The coverage statement permits failure paths.

Against the exact constant-half reference, a Brier lower endpoint greater
than $`T/4`$ indicates poorer forecast loss, while an action-mean upper
endpoint below $`(T-m)/2`$ indicates better remaining-action mean. These are
current-episode performance statements under the sampling theorem's premises.
They do not establish generalization to a future tape or a profitable change
of purchase policy. The [two-sided design](../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/two_sided_design.md)
and its [additive clarification](../work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/two_sided_design_clarification.json)
precede the corresponding public-statistics calculation. The original design
and all earlier outputs remain unchanged.

## 8. Integration and value boundaries

### Hard answers and changed forecasts

A later hard-answer mechanism may improve a current action or a forecast for
which the sound answer is available before issuance. If the underlying
purchase and learner-update path remains unchanged, the base process's
upper loss bounds transfer to the improved outputs by pointwise domination,
provided its original statistics remain available and the extra work is paid.

That domination does not transfer lower bounds. Nor does it license inserting
selection-dependent overridden forecasts into the original conditional-moment
proof. If a label bought early in a block changes a later forecast in that
block, the whole forecast vector may no longer be fixed before the selector.
The algebraic identity (5) still holds if **all** targets and statistics are
consistently recomputed, but its zero-mean and predictable-width proof need
not hold. Old base statistics generally do not share (5) with the changed
targets. This is a substantive P3-08 interface obligation, not a retroactive
change to the reviewed cache-free policy.

### Actual cost and a future decision

Let the observed resource vector be $`\mathbf r`$, with declared prices
$`\boldsymbol\lambda`$ and terminal-error price $`c\ge0`$. The event bounding
$`Z`$ immediately also bounds the **same episode's realized all-in cost**:

```math
cZ+\boldsymbol\lambda\cdot\mathbf r
\le c\,\overline Z+\boldsymbol\lambda\cdot\mathbf r. \tag{12}
```

The realized bill can be random and correlated with the selector; adding
that same known bill pathwise requires no independence assumption. It is not
an estimate of the bill on a new episode, and conditional task mean plus a
realized resource bill must not be silently renamed an unconditional expected
policy cost. Repricing this fixed record also does not rerun a price-sensitive
selector. The new reporting calculator's own cost must be included if deployed.

A good current-episode estimate can therefore support accountability or a
specified stopping rule, while a forecast of future usefulness still needs
its own stability/model assumptions. The one-sided prefix sampling bound
licenses exactly its declared statistic, not arbitrary adaptive stopping of
the complete terminal-cost service. P3-07's independently scoped policy-profile
and acquisition results remain separate ways to address a future decision.

The constant-half example in §5 concerns information contributed by the
performance record. Where the received-information source admits two distinct
answer assignments, those assignments have identical constant-half performance.
If sound prior information already leaves a singleton, truth is identified
by that source; this example does not undo the identification.
