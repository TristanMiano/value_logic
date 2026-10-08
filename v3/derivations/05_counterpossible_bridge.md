# P3-05 — Applying transport to the retained counterpossible semantics

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 8, 2026 UTC.
S3 finite integration. This uses the completed P3-04 paired-support semantics;
it does not silently replace a logical counterpossible by ordinary conditioning.

## 1. Two different Boolean levels

The original quoted antecedent is $`\theta=p\land\neg p`$. Its ordinary
interpretation remains the ordinary Boolean one, under which no valuation
satisfies it. P3-04's explicitly exceptional hypothetical evaluation uses
independent support flags $`p^+,p^-,q^+,q^-`$. These flags are ordinary bits,
but the hypothetical positive support of the quoted negation of p is p-minus,
**not** one minus p-plus. The positive support of theta is
$`p^+\land p^-`$. Ordinary numerical evaluation of these flags therefore does
not make theta classically satisfiable or replace its original syntax.

The hypothetical source compiler receives the exact quoted formula, reference
valuation, permitted consistency exceptions, frame preferences, hypothetical
background and loss expression. It constructs the actual hard/soft conditions
using the unchanged P3-04 implementation. The receiving wrapper reconstructs
that source from the independently supplied request before checking the
portfolio proof. A changed quoted antecedent or exception policy is a changed
request, even when a display name or numerical answer stays unchanged.

**CT05-18 — typed hypothetical-source bridge.** Under the stated P3-04
paired-support interpretation and exact source compiler, acceptance of the
recompiled current request by CT05-8 establishes the reported fixed loss
comparison on every selected hypothetical support state of that request.
The proof is composition of the source construction with the receiver's
all-minimizer guarantee. It imports no correctness of the chosen relevance
policy, no probability of a contradiction, and no metaphysical truth claim.

The code supports P3-04's default single rank tier only. It does not adopt
its additional lexicographic baseline-preservation tier or a general rule
for transporting arbitrary arithmetic semantics. Explicit limits are part
of the finite input contract, not a restriction on future value representations.

## 2. Withdraw a frame without losing the original question

Take ordinary reference $`p=q=0`$, allow a consistency exception only for p,
and initially frame q at zero. Positive support of theta is hard; normal q
complementarity is hard; normal p complementarity has one unit of soft penalty.
There is one selected hypothetical state, $`(1,1,0,1)`$, of rank one.
For the fixed action-loss difference

```math
d=4q^+-1,
```

an old band at cutoff one certifies minus one. The antecedent remains genuinely
impossible under the ordinary reference interpretation.

Withdraw only the q frame. The hypothetical source now contains two equally
preferred states, with q-plus zero and one respectively. Keep both. Map the
current flags to the old certificate's flags by
$`\pi(p^+,p^-,q^+,q^-)=(p^+,p^-,0,1)`$.
The mapped old hard and rank constraints hold, but the exact loss correction
is $`4q^+`$. Its upper bound four changes the justified report to three.
Copying the old minus-one report is unsound; the q-plus-one state is an actual
counterexample under the stipulated hypothetical semantics.

This map is an **auxiliary proof map** used with its explicitly checked loss
correction. It is not an assertion that the current counterpossible actually
causes the old framed state or that the old relevance preference still applies.
An ordinary direct evaluation obtains the same new interval. Transport gives
an audited conditional derivation, not evidence of a universal performance gain.

Adding the hypothetical background q instead selects the other q state and
eliminates every old selected state literally. Adding both q and not-q while
permitting q's consistency exception yields a second localized conflict.
The same numeric proof discipline applies with a new request and correction;
no rule of arbitrary explosion is introduced.

## 3. Limits and separating checks

Disallowing p's consistency exception makes the theta request infeasible. A
vacuous old band may exist as a universal empty-domain inequality, but no current
feasible incumbent can be supplied. The receiver must reject any attempt to
turn it into a useful action guarantee.

Simultaneously renaming atoms, their support positions, quoted formulas, frame
entries and loss coefficients preserves the named finite denotations. Merely
renaming a formula label while keeping a stale proof record does not. Duplicated
hard assumptions can preserve the selected set while increasing validation
work; that is not resource-preserving operational equivalence by itself.

The accompanying development checks enumerate all ordinary valuations and all
sixteen hypothetical support assignments for their fixed request family. They
compare direct paired evaluation with the receiver and include stale antecedent,
frame, exception and advertised-bound rejections. Their semantic target is the
P3-04 declared model, not a independently identified uniquely correct theory of
counterpossibles. This is a concrete bridge for C04/R01/I01, not a new answer to
the general philosophical selection problem.
