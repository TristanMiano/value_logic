# Frozen hard answers: independent composition review

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. R-P3-B-A.
Same-model, nonblind analytic review. **Zero principal clock credit.**
No policy, service, cache, calculator or experimental probe was executed.

## Verdict and binding

**PASS; no mathematical blocker under the stated premises.** The note supplies
a sufficient predictable interface for new direct performance certificates,
while retaining the separate pointwise transfer of base upper bounds. It does
not implement or select a P3-08 policy, establish complete hard-state behavior,
or price a new reporting service.

Target: `development/frozen_hard_answer_composition.md` under this recurrence.
Reviewed SHA-256:
**`21b2420d0b61176ffea258c7bcd56b6ab3d23bf9e3abd30722ca40c08d45fcc8`**.
The exact 6,222-byte target is preserved in
`frozen_hard_answer_composition_reviewed.md`; its capture receipt and this
review's manifest retain the source binding.

## 1. Predictability and pointwise composition

The necessary sufficient conditions are stated: the mask H and every answer
it licenses are available in the pre-selection information, remain sound for
the block's declared version/epoch, and do not depend on sampled action values.
The actual positive selection probabilities are defined conditional on that
same information. A new answer bought inside the block is excluded from the
frozen reporting mask until a later block. That exclusion is what preserves
the present whole-block proof; a complete reasoner's broader hard-information
duties remain a separate integration question.

With `q'=(1-H)q+Hy`, known coordinates emit the correct degenerate probability,
while unknown coordinates retain the base forecast. Consequently

`d'=(1-H)d`, `g'=(1-H)g`, and `v'=(1-H)v`.

Under the same action-bit coupling, known-position errors become zero and all
other prospective actions are unchanged. The same purchases and base updates
therefore give pointwise upper-loss domination, including actual terminal
errors. Keeping the complete supplied-bit schedule, even for degenerate
actions, preserves the stated coupling instead of shifting later draws.

Soundness, version matching and payment for snapshot work are substantive
premises. Lower bounds cannot transfer by domination. Changing the acquisition
law to avoid already-known purchases or feeding overridden outputs into the
base weight update would be a different process.

## 2. General public-center identity

For any finite predictable public center `a_t`, set `r'_t=d'_t-a_t`.
In a block with selected position J,

`sum_{t!=J} d'_t - [sum_{t!=J} a_t+(1/pi_J-1)r'_J]`

`=sum_t r'_t-r'_J/pi_J`.

Because `g'=d'-v'`, subtraction from the proposed Brier estimator gives the
same expression:

`sum_t g'_t - [sum_t(a_t-v'_t)+r'_J/pi_J]`

`=sum_t r'_t-r'_J/pi_J`.

The random omission of the selected coordinate from the public center sum
is therefore accounted exactly. That center sum need not be constant across
selectors. Conditional expectation of `r'_J/pi_J` is `sum_t r'_t`, so each
block residual is mean zero under the actual conditional selection law.
Summing blocks proves the proposed shared identity for `V'-Ua` and `F'-Aa`.

## 3. Mask-specific range and its comparison

Choosing `a_t=(1-H_t)/2` gives

`r'_t=(1-H_t)(1-2q_t)(y_t-1/2)`.

Thus `r'_t/pi_t` lies in `[-C'_k/2,C'_k/2]`, where

`C'_k=max_t (1-H_t)|1-2q_t|/pi_t`.

The residual's conditional range width is at most `C'_k`. Known coordinates
contribute exactly zero, which is stronger than putting the usual half-center
around their already-known zero error. One must use this mask-specific range,
not blindly substitute the extreme `q'` into the old half-centered formula.

For the **same raw forecast vector and actual propensities**, every coordinate
in this maximum is at most its old counterpart. Hence `C'_k<=C_k` and
`Q'=sum(C'_k)^2<=Q`. These comparisons are pathwise on the coupled base
trajectory; they say nothing about a separately rerun acquisition policy.

The original fixed `lambda=8/R` is still legitimate. The one-sided radius
`Q'/R+R/2` and two-sided radius `Q'/R+5R/8` follow from the same exponential
argument and log bounds. Both performance targets share the resulting event.
The radii weakly decrease relative to the base calculation, but complete
endpoints need not be ordered because their estimators and targets differ.
No rate is retrospectively optimized using the realized mask or Q'.

## 4. Conditional action count and degenerate cases

Let the complete selector/snapshot history be fixed. Under the expressly
action-independent history and unchanged bit schedule, all unknown unbought
forecast parameters are then fixed and their action bits remain independent.
Their count n' may be random before this conditioning, but it is fixed within
each conditional calculation. For `n'>0`, Hoeffding gives

`Pr(±(Z'-V')>a | history) <= exp(-2a^2/n')`.

The radius `ceil_sqrt(2n')` makes each selected one-sided tail below `1/40`.
The two-sided radius `ceil_sqrt(ceil(5n'/2))` makes each sign below `1/80`.
Because those conditional tail bounds hold for every admitted history, they
also hold after averaging over histories. This is not the unjustified use of
random Q in a rate optimized after observing it. The action result remains
fixed-end, with no new anytime or multi-arm coverage.

If `n'=0`, there is no action tail to estimate: every unbought output is
correct under its snapshot, while every purchased terminal output is correct
under its receipt. Therefore `Z'=V'=0` exactly. The deterministic terminal
cap can more generally be tightened to `n'`.

The Brier distinction in the note is correct. `n'=0` does not imply that a
purchased forecast was already correct when issued. One can have a single
uncovered selected forecast at `q'=1/2`, with all unbought positions covered;
terminal loss is zero while that purchased forecast contributes Brier `1/4`.
If **all issued positions are covered by the sound frozen snapshots**, then
every issued Brier loss is zero.

There is a useful exact consequence within the same premises: when `n'=0`,
the possibly nonzero `F'` is nevertheless publicly computable exactly as

`F'=sum_purchased (q'_t-y_t)^2`.

Every unbought Brier loss is zero, and every selected label has been paid for.
Thus this case needs no sampling uncertainty for F', although F' need not
equal zero. This is an analytic observation, not another executed calculator.

The stated public deterministic-envelope tightening is also valid: set known
coordinates' losses to zero using their checked warrants rather than taking
a generic maximum over both hypothetical labels. Exact identities may replace
the loose generic fixed-rate radii in their respective degenerate cases.

## Conclusion within scope

The note correctly separates retaining base statistics for upper-bound
transfer, freezing a sound block-entry mask for new direct certificates, and
using current-block feedback to change later forecasts under a replacement
selection argument. Only the first two interfaces have been justified here.
Nothing in this review licenses stale answers, a changed purchase quota or
law, action-dependent histories, unpaid snapshot work, or a claim that the
new interface has been implemented or selected.
