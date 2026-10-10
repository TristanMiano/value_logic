> **Portable display copy — notation only.**
>
> Original: [v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/u08_comparator_qualification.md](../../../reviews/forecast_benchmarks_independent/u08_comparator_qualification.md)  
> Original SHA-256: `c92a810356cab9a210c71889d4984c9133a0bf2634a130d32e44594e3d6f9530`.
>
> Generated with the unchanged math guard's `transform(protect=True)`,
> plus relocation of relative links to their original destinations.
> The original scientific document remains unchanged. This is a source-notation
> check, with no live-render or new mathematical validation claim.

# U08: the comparator preserved by sound hard correction

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.
Same-model, nonblind scientific review; **zero principal time credit**.
Additive review only: no code, existing evidence, main artifact or ledger
changes; no policy runs, new empirical tests or additional private-data reads.

**The proposed qualification is correct and should be explicit.** Sound
correction transfers applicable base upper bounds against the **original
fixed-expert loss table**. It does not, by itself, transfer the same regret
bound against the best expert after giving every expert the learner's
realized hard mask. The existing main U08 row is defensible under its original
scope, but its phrase “transfer its applicable bounds” leaves this comparator
distinction implicit next to the newly displayed hard-matched benchmarks.

The main forecast section and the principal assumption audit already call
those benchmarks descriptive and separate them from terminal economics.
They should also state explicitly that the inherited fixed-expert theorem
does not certify regret against the retrospectively hard-matched benchmark.
This is a scope clarification, not a defect in the score calculation or the
accepted exact live-loss identities.

## 1. What transfers

The original selective-feedback contract fixes stateless expert functions and
an exogenous truth tape. Its comparator losses
$`L_i=\sum_t\ell_{t,i}`$ are the losses of those unchanged experts on the
declared full tape; they do not acquire the learner's random hard mask.
The accepted theorem retains its exact scored output, expectation, quota,
propensity, rounding, funding and other premises. It must not be paraphrased
as a stronger Brier-regret theorem if its particular bound concerns terminal
lottery loss.

Let $`L`$ denote the same typed base loss appearing in an applicable bound.
Sound correction gives $`L^H=L-D`$ with $`D\ge0`$ pathwise. Consequently, if

```math
\mathbb E L\le G(L_1,\ldots,L_N),
```

then

```math
\mathbb E L^H\le\mathbb E L\le G(L_1,\ldots,L_N).
```

The right-hand comparator is unchanged. Here $`G`$ stands for the actually
proved envelope, including any first-order coefficient and approximation
allowances. In a scope where it has the form $`\min_iL_i+R`$, the same
$`\min_iL_i+R`$ upper bound transfers. Added hard-state resource costs still
need their own bill; this inequality transfers task loss only.

## 2. Why the matched comparator needs another argument

For Brier scoring, put

```math
\ell_t=(q_t-y_t)^2,\qquad
\ell_{t,i}=(a_{t,i}-y_t)^2,
```

and let $`H_t`$ mark a current sound answer available before issue. Giving every
expert the same hard answer removes its own error at those positions:

```math
D=\sum_tH_t\ell_t,\quad D_i=\sum_tH_t\ell_{t,i},\qquad
L^H=L-D,\quad L_i^H=L_i-D_i.
```

The exact comparator identity is

```math
L^H-L_i^H=(L-L_i)+(D_i-D).
```

Both corrections are nonnegative, but **their difference has no fixed
sign**. The same information can improve an expert more than it improves
the learner. Even a bound against each original $`L_i`$ therefore cannot
simply replace it with the smaller $`L_i^H`$.

For the hindsight best matched expert, write $`L_*=\min_iL_i`$. Then

```math
L^H-\min_iL_i^H
=(L-L_*)+
\left[L_*-\min_i(L_i-D_i)\right]-D.
```

The bracketed improvement of the comparator can exceed the learner's
improvement $`D`$. A generic estimate adds as much as $`\max_iD_i-D`$ to the
original regret, potentially a quantity linear in the horizon. Soundness
alone supplies no smaller bound.

### Finite causal separator for the inference

The following is a mathematical separator for the purported implication,
**not an executed P3-08 policy or a counterexample to the Prod recurrence**.
Use three distinct claims A, B and C, all with truth zero. Expert 1 predicts
one exactly on A; expert 2 predicts one exactly on B. A base forecaster follows
expert 2. Arrange three two-position blocks as follows, with one checked
purchase in each block and an initially empty hard store:

| Position | Claim | Selected for purchase | Hard before issue | Expert 1 | Base / expert 2 |
| --- | --- | --- | ---: | ---: | ---: |
| 1 | A | Yes | 0 | 1 | 0 |
| 2 | A | No | 1 | 1 | 0 |
| 3 | A | Yes | 1 | 1 | 0 |
| 4 | B | No | 0 | 0 | 1 |
| 5 | B | No | 0 | 0 | 1 |
| 6 | C | Yes | 0 | 0 | 0 |

The first receipt makes positions 2 and 3 hard before issue. Repeating its
scheduled purchase at position 3 is permitted. Neither B position has an
earlier receipt. These are stateless expert predictions with a causal,
sound preissue mask; a current purchase never revises its own Brier score.

The original losses are $`L=2`$, $`L_1=3`$, $`L_2=2`$: regret against the original
best expert is zero. Hard correction removes no learner error, so $`D=0`$ and
$`L^H=2`$. It removes two errors from expert 1, giving $`L_1^H=1`$ and
$`L_2^H=2`$. Regret against the best matched expert is therefore **one**.
Repeating this array with fresh A/B/C claims makes the gap linear. This
illustrates the absence of a general domination-to-matched-regret inference;
it does not purport to run the implemented learner with different weights.

## 3. Selection history and the location of the minimum

The algebraic problem exists even for a fixed mask. In P3-08 there is a
further issue: $`H`$ follows the learner's selected receipts and is random under
the theorem's selection model. The transformed comparator loss $`L_i^H`$ is
therefore a function of that history, even though $`a_i`$ itself was fixed.
The identity of the best matched expert can change across histories.

Even a separately proved bound against every fixed expert in expectation
would naturally involve $`\min_i\mathbb E L_i^H`$. A guarantee against the
best expert on each realized history instead involves
$`\mathbb E\min_iL_i^H`$. These are different:

```math
\mathbb E\min_iL_i^H\le\min_i\mathbb E L_i^H.
```

For instance, random losses $`(Z,1-Z)`$ with a fair bit $`Z`$ have expected
hindsight minimum zero, while the minimum expected loss is one half. The
original derivation already records this separator. One cannot move the
minimum through expectation when importing its fixed-expert bound.

Moreover, availability before each issue is weaker than availability before
the block selector: an earlier purchase inside the same block can change a
later $`H_t`$. The broker also continues to update from the **original** selected
expert losses. Replacing them by hard-masked losses would change the update
and the conditional sampling argument. Neither predictability at issue time
nor the exact live reporting identity alone proves the desired new regret
claim. The snapshot/reporting theorem estimates actual live losses; it is not
a regret theorem against a new masked comparator class.

## 4. Static and matched-history scores remain valid diagnostics

The saved static-mixture and fixed-expert benchmarks replay the learner's
actual historical hard answers. They do not execute an autonomous static
policy's own selector, purchase schedule, state or resource bill. In
particular, replacing the forecast by a static mixture can change the ticket
selector's favorite and hence future available labels. That counterfactual
history was not generated by the benchmark audit.

Thus the measured 18-configuration comparisons remain correct descriptive
scores. Their favorable and adverse outcomes establish neither the new
matched-comparator regret theorem nor a separately deployed static policy's
performance. This qualification also leaves the original fixed-expert
expected bounds, exact hard-loss translations and public report coverage
claims intact within their own assumptions.

## 5. Suggested additions for the principal

**U08 row:** “The accepted base selective-feedback path is retained. Sound
corrections transfer applicable base expected upper bounds against the
original fixed experts. They do not establish regret against a hindsight
best expert given the learner's realized hard mask; adaptive-policy regret
and greedy-action guarantees are not imported.”

**Forecast comparison / principal assumption audit:** “The matched-history
benchmarks replay the learner's acquired answers. They neither run each
benchmark's own selector nor inherit the original fixed-expert regret bound:
the common hard mask can remove different amounts of loss from the learner
and each expert, and its hindsight minimizer can depend on the selection
history.”

## Source binding

The reviewed copies are retained in `u08_source/`, with the complete inventory
in `u08_source/manifest.json`. Main artifact SHA-256:
`a12435b9ed07a6f8b130e5f48b7e92c4a42fd0a7f055130748bad1e5a49c3cfc`.
Principal assumption audit SHA-256:
`4a22e06e3707eccca0df9d07e29731fc9c6374748d08d263390191155c34c22a`.

The controlling internal sources are `01_desiderata.md` U08;
`07_selective_feedback.md` §§2–3, 8.2 and 9; and
`08_live_hard_performance.md` §§1–4. The current additive P3-08 overlay is
included for disposition context. No external theorem or additional
experiment is imported by this review.
