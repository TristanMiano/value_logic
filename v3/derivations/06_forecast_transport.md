# P3-06 — Changing a report changes its guarantee

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
New reconstruction in P3-06-R1. The lost earlier projection/grid learner is
still unverified; these examples do not purport to recover its execution.
Read with the [scalar construction](06_cost_forecast_refinement.md).

## 1. A calibrated randomized report can have a miscalibrated mean

Consider two equally frequent contexts. The answer is deterministically zero
in A and one in B. The announced distributions over reports are:

| Context | Answer | Mass on report 1/4 | Mass on report 3/4 | Mean report |
|---|---:|---:|---:|---:|
| A | 0 | 3/4 | 1/4 | 3/8 |
| B | 1 | 1/4 | 3/4 | 5/8 |

The distribution-weighted frequency of answer one among reports of 1/4 is
1/4; among reports of 3/4 it is 3/4. Equivalently both grid-coordinate
calibration residuals are exactly zero. A finite eight-observation realization
with A's report counts 3:1 and B's counts 1:3 also has zero grid residuals.

Replacing each report distribution by its mean changes the object being
scored. Every mean report of 3/8 now precedes answer zero, and every mean
report of 5/8 precedes answer one. Their respective conditional errors are
$`-3/8`$ and $`3/8`$. Repetition preserves this failure. This is **CF-8**:
calibration of a distribution over reports does not imply calibration of its
round-by-round mean. Jensen's inequality for squared loss is a different
statement and does not repair the calibration implication.

This explains why the main construction solves for one actual scalar $`p_t`$
and uses that same scalar in its expert losses and tent residuals. Its optional
randomized *action* is a different consumer: the probability report itself
is not sampled from several calibrated reports and then replaced by a mean.

## 2. A quantitative output-transport lemma

Let $`p_t,p'_t\in[0,1]`$ be the original and changed issued numbers, with
the same answers, expert tape and nonnegative weights. Put
$`D_T=\sum_t w_t|p'_t-p_t|`$. A reported scalar can be changed by projection,
rounding or another postprocessing rule. The following statements compare
these **two fixed report tapes**; they do not assert that rerunning a stateful
learner under a different internal rule generates either tape.

Squared loss is 2-Lipschitz on the binary forecast interval. Therefore

```math
L'_T-L_{T,i}\le L_T-L_{T,i}+2D_T.
```

For a calibration test $`b:[0,1]\to[0,1]`$ with Lipschitz constant $`m`$,

```math
\begin{aligned}
|b(p')(y-p')-b(p)(y-p)|
&\le |b(p')-b(p)|\,|y-p'|+b(p)|p'-p|\\
&\le(m+1)|p'-p|.
\end{aligned}
```

Thus **CF-9** is the transport bound

```math
|E'_b|\le |E_b|+(m+1)D_T.
```

For the main tents, this uses their actual resolution $`m`$. If
$`D_T=o(W_T)`$, the normalized expert upper bound and these calibration
residuals survive. If a display rounds every probability to a fixed grid of
width $`h`$, nearest rounding has $`D_T\le hW_T/2`$, giving an explicit
worst-case upper allowance that need not vanish. This is not a lower bound
on actual error: reports already on the grid have zero displacement.
A shrinking display error can preserve the
normalized result; a hard decision applied to the display still needs its
own consumer analysis.

This lemma also shows what has to be paid when an estimated coherence repair
alters an issued scalar. A different proof may give a better bridge, but
neither an unexplained projection nor a changed scalar inherits calibration
by name. Projecting every report to zero already defeats that assertion on
an all-one answer tape.

## 3. Forecast coherence and checked information

One scalar in $`[0,1]`$ is a coherent probability adapter for one binary
coordinate and its known affine loss rows. It does not automatically provide
a jointly coherent law over several unresolved mathematical claims. For
example, knowledge that two claims are equivalent constrains a simultaneous
joint-probability report to give them the same probability. Independent scalar
calls with unrelated experts have no mechanism enforcing that equality.

The hard-evidence service remains separate. A received, checked, same-scope
answer gives an exact current response for that canonical query; a new request
identifier does not make the same already-resolved claim unknown again.
The mathematical adapter must route a cached repeated claim through that
known-answer channel. Old pre-answer forecasts remain immutable for scoring.
Withdrawn or changed evidence belongs to a new version or proved transport.

These are precise U03/U04 limits, not a reopening of P3-03. The scalar learner
does not replace the earlier finite cover, propagate all represented Boolean
constraints, or introduce a probability law over unfinished cover cells.
Adding a joint coherent learner would need its own report space, resource
account and calibration/regret proof.

## 4. Absolute costs and relative decision quality

Suppose a common outcome-dependent cost $`M_ty`$ is added to both actions.
Their slope difference, smooth action selection and relative decision
features are unchanged. Their absolute estimated losses change by
$`M_tp_t`$, while their realized losses change by $`M_ty_t`$. The signed
error in the absolute loss estimate therefore gains $`M_t(p_t-y_t)`$.
The magnitude of that error can increase or decrease.

The smooth decision-regret theorem cannot independently bound that new
absolute error merely because it still bounds relative action quality.
To estimate absolute loss accurately, use the relevant probability/absolute
exposure guarantee and its actual scale, or include an appropriate extra
continuous feature. Costs, cost differences, forecast accuracy and good
decisions are different requested services.

## 5. What the examples establish

| Operation | Preserved conclusion under stated conditions |
|---|---|
| Rescore exactly the same issued scalar | Its own coordinate bounds remain applicable at their original weights and scope. |
| Replace a randomized report by its mean | No general calibration transfer; CF-8 gives an exact counterexample. |
| Change a scalar report slightly | CF-9 charges the weighted displacement and the test's Lipschitz constant. |
| Change training or expert behavior and rerun | Requires a new run; fixed-tape transport alone does not identify its predictions. |
| Answer a known repeated claim | Use its version-matched checked answer; retain its historical forecast separately. |
| Add a common outcome-dependent action cost | Relative decision regret is unchanged; absolute cost error can change substantially. |

The executable transport probe is new development evidence. None of these
results supplies a full Logical Induction criterion, a paid reasoning policy,
or an advantage over ordinary prediction and scoped evidence management.
