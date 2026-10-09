# Predictable hard answers and public centering

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
R-P3-B-A, final D/R assumption analysis. This is a mathematical interface
result. No cache, policy, reporting calculator or P3-08 integration is executed.

## 1. The remaining composition question

The observable-performance proof fails if a bought label changes later
forecasts inside its current block in a selector-dependent way. That does
not exclude every use of earlier hard answers. The sufficient condition is
predictability of the current block's entire forecast vector and actual
purchase law before its selection, together with the action-independent
state and random-bit schedule already assumed by the base service.

Freeze a version-matched hard-answer snapshot at block entry. Write
$`H_{kt}\in\{0,1\}`$ for whether that snapshot supplies the correct answer
to current query $`t`$. The mask and each available answer must be measurable
in the pre-selection information. They remain sound for this block's declared
epoch; a premise withdrawal or scope change cannot silently retain that
warrant. A label purchased in this block may still correct its own terminal
action, but becomes eligible for this snapshot only in a later block.

Keep the base purchase and weight-update path, with its actual positive
propensities. Replace the emitted forecast only where a snapshot answer was
available before issuance:

```math
q'_{kt}=(1-H_{kt})q_{kt}+H_{kt}y_{kt}.
```

This expression does not grant an unbought answer: the second term is
permitted only through the already checked snapshot. Retain the original
supplied-bit schedule, including action draws on known-answer positions,
and let the output use the degenerate probability zero or one there. Hard
answers and snapshot construction/checking/storage remain paid resources.
No old forecast is retroactively rescored as the replacement.

The new prospective losses satisfy

```math
d'_{kt}=(1-H_{kt})d_{kt},\qquad
g'_{kt}=(1-H_{kt})g_{kt},\qquad
v'_{kt}=q'_{kt}(1-q'_{kt})=(1-H_{kt})v_{kt}.
```

Thus the base expectation and upper loss bounds transfer by pointwise
domination on the unchanged purchase/update path. Lower loss bounds do not
transfer by domination. Direct new certificates are nevertheless available
because the snapshot and current forecasts are predictable. This is the
specific safe alternative to the selector-dependent within-block change.

## 2. Public centering handles known zero losses exactly

Naively retaining the center one-half at hard-answer coordinates is valid but
needlessly treats their known zero loss as uncertain. For any predictable
public center $`a_{kt}`$, let $`r'_{kt}=d'_{kt}-a_{kt}`$ and define

```math
U_a=\sum_{k,t\ne J_k}a_{kt}
       +\sum_k(\pi_{kJ_k}^{-1}-1)r'_{kJ_k},
\qquad
A_a=\sum_{k,t}(a_{kt}-v'_{kt})
       +\sum_k r'_{kJ_k}/\pi_{kJ_k}.
```

For $`V'=\sum_{k,t\ne J_k}d'_{kt}`$ and $`F'=\sum_{k,t}g'_{kt}`$,
direct subtraction gives

```math
V'-U_a=F'-A_a
 =\sum_k\left(\sum_t r'_{kt}-r'_{kJ_k}/\pi_{kJ_k}\right).
```

Each block residual has conditional mean zero. The removed position in the
first public sum is known after selection and is accounted exactly; that
sum need not be constant to make the identity hold. The center is public
control information, not a newly learned truth probability.

Choose $`a_{kt}=(1-H_{kt})/2`$. Then

```math
r'_{kt}=(1-H_{kt})(d_{kt}-1/2),\qquad
C'_k=\max_t\frac{(1-H_{kt})|1-2q_{kt}|}{\pi_{kt}}
\le C_k.
```

The conditional residual range is at most $`C'_k`$. The same fixed-rate
exponential proof therefore uses $`Q' = \sum_k(C'_k)^2`$ and the original
predeclared $`\lambda=8/R`$. Its one-sided radius is $`Q'/R+R/2`$ and its
two-sided radius is $`Q'/R+5R/8`$. Both targets share that event. The term
based on known hard coordinates is removed analytically, without sampling
it or using privately evaluated unknown answers.

The inequality $`Q'\le Q`$ assumes the **same base forecast path and actual
propensities**. It does not compare newly rerun acquisition policies. Even
under those conditions, it compares concentration radii, not necessarily
the complete realized endpoints, because their centers and targets change.

## 3. Action tails and exact special cases

Let $`n'`$ count unpurchased positions not covered by the frozen snapshots.
Conditional on the complete selector/snapshot history, that count and the
remaining forecast parameters are fixed, and the relevant action draws remain
independent. Thus one may use $`\lceil\sqrt{2n'}\rceil`$ for the one-sided
action radius or $`\lceil\sqrt{\lceil5n'/2\rceil}\rceil`$ for its two-sided
analogue. This is a conditional action argument; it is not the invalid
substitution of random $`Q`$ into an optimized martingale square-root bound.
The history and its cost must not depend on sampled action values.

If $`n'=0`$, terminal loss and the remaining-action mean are exactly zero.
If every position, bought or unbought, was already hard-known at issuance,
all issued Brier loss is also exactly zero. These exact identities replace
loose generic radii in their respective special cases. If only unbought
positions are hard-known, bought pre-purchase forecasts can still have Brier
loss, so the latter conclusion does not follow merely from $`n'=0`$.

Public deterministic envelopes may also set each hard coordinate's loss to
zero rather than taking the generic maximum over both hypothetical answers.
That tightening uses the checked source premise. Wrong or stale hard answers,
action-dependent snapshots, changed purchase paths, or current-label changes
to later current-block forecasts fall outside this result unless separately
justified. The base implementation and saved development traces are unchanged.

## 4. Consequence

There are now three explicit interfaces: retain base statistics and transfer
upper bounds by sound pointwise improvement; freeze valid hard answers before
selection and compute new direct certificates; or change forecasts from
within-block observations and provide a replacement selection argument.
Only the first two have been justified here. Implementing or choosing among
them remains P3-08 work, not an additional selected task in this recurrence.
