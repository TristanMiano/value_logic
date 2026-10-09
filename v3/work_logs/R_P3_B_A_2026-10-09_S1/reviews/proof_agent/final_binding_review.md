# Final binding review: observable §§7–8 and acquisition objective

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. R-P3-B-A.
Same-model, nonblind independent analytic review. **Zero principal clock
credit. No policy, service, calculator or experimental probe was run.**

## Verdict and precise extent

**PASS; no blocker in the reviewed material.** Observable-performance §§7–8
faithfully integrate the reviewed two-sided concentration and hard-answer
boundaries. The supplied-model last-block ratio-versus-net witness is exact.
Neither text claims a new executed policy or established acquisition optimality.

| Reviewed source | Binding |
| --- | --- |
| `v3/derivations/07_observable_performance.md`, full file when captured | `6e7e0a7c5f52ec61a101f0f91777071851fec8b0782512bd2c33d924240bdabf` |
| **Only §§7–8** of that captured file | `c6f40445a34d99b6c2361dd1848eb35d3b5f6a3e9b94f84cdb724a3c390b1386` |
| `development/selection_objective_boundary.md` | `47a02c22248c3bd61bb18245ecf35071be67c48dbc634a3140b44429496a34dd` |

The full snapshot and separately extracted §§7–8 are preserved. The full
hash identifies captured bytes, **not a review of other sections**. The new
§9 evidence section and the checkpoint synthesis are expressly outside this
receipt. No science, status or clock file was edited by this reviewer.

During final binding, the root appended §9 and added one separator newline
after §8. The exact diff contains no substantive change to §§7–8. The
post-append section extraction is also retained, with SHA-256
`3d165ae78df13583a7bdef4eb568556b3bc4c7ef6292176a8cb561ee775978a8`.
`final_binding_append_receipt.json` records that boundary change and the
then-current full-file hash without extending this review to §9.

## 1. Two-sided and override integration

Section 7's equations (10)–(11) retain the correct constants:
`rho_pm=Q_m/R+5R/8`, action radius `ceil_sqrt(ceil(5(T-m)/2))`, and the exact
`exp(5)>1097/12>80` witness. Two sampling signs share the V/F residual and cost
`1/40`; two action signs cost another `1/40`. Joint fixed-end per-episode
coverage is at least `19/20` under the original fair-bit premises.

The section explicitly distinguishes the new `rho_pm<=9R/8` envelope from
the earlier one-sided `rho<=R`. It preserves the fixed-rate sampling prefix
scope while denying an automatic anytime terminal or simultaneous multi-arm
claim. Public deterministic lower and upper envelopes may be intersected
with the confidence intervals, and empty intersections are retained without
ordinary better/worse labels. These are precisely the reviewed safeguards.

Section 8 correctly distinguishes three facts:

- A sound prospective correction can weakly reduce base loss, so an unchanged
  purchase/update process with retained base statistics supports transfer of
  base **upper** loss bounds. The extra correction work remains payable.
- Pointwise improvement does not transfer a base **lower** loss bound.
- Consistent recomputation from changed forecasts preserves the algebraic
  shared-residual identity, but selector-dependent changes inside a block may
  destroy the mean-zero and predictable-width premises. Retained base
  statistics generally do not share that identity with the new targets.

The new text therefore resolves the earlier algebra-versus-concentration
ambiguity without modifying the original design. The public-stage protocol
binds the original two-sided design hash
`41a1c9538d0ae697f52cf242be53faa1fe2219892004d77cc707ffb9964a0659`.
The additive clarification expresses the two-sided-radius, empty-interval and
override distinctions incorporated here. I inspected these bindings and the
public stage's completion metadata, not its 23-row evidence analysis.

Equation (12) is a valid pathwise implication: for `c>=0`, the event
`Z<=Z_upper` also implies
`cZ+lambda dot r <= c Z_upper+lambda dot r`. The same observed resource bill
may be correlated with selection; adding it requires no independence. The
section correctly refuses to rename a conditional task mean plus a realized
bill as an unconditional expected policy cost or a future-episode forecast.
It also keeps the reporting calculator's own deployment cost explicit.

The constant-half information example is properly conditional on the admitted
received-information source containing distinct answer assignments. Its exact
V/F performance identities do not undo identification already supplied by
sound singleton evidence. This is not an assertion that an arbitrary sampled
terminal-error record carries no information.

## 2. Fixed-quota objective

For a last block with frozen prospective error probabilities `d_t`, a required
single selected correction, and supplied fees measured in units priced by
lambda, the displayed objective is exactly

`J(pi)=c sum_t d_t + sum_t pi_t(lambda f_t-c d_t)`.

The first term does not depend on pi. For a feasible common floor
`0<=epsilon<=1/B`, write `pi_t=epsilon+x_t`, where `x_t>=0` and
`sum x_t=1-B epsilon`. A minimizing distribution places the residual mass on
a maximizer of `c d_t-lambda f_t`; ties may split that mass. This is the stated
ordinary simplex linear program. It is conditional on the supplied errors
and fees and excludes later learning benefits and any omitted choice-dependent
controller work. The note does not claim those unknown quantities for free.

For an independent lottery with action-one probability q and supplied truth
belief p, expected error is `q+(1-2q)p`. Under the additional model equality
`p=q`, it becomes `2q(1-q)`. Thus the disagreement interpretation needs that
extra belief premise. The witness's dyadic probabilities are exactly
representable, so no rounding discrepancy affects its arithmetic. The
executed expert mixture has not been established as such a truth belief.

## 3. Exact ratio-versus-net witness

For the supplied parameters `B=2`, `c=1`, `lambda=1/10`,
`q=p=(1/2,1/4)`, `f=(2,1)`, and `epsilon=1/4`:

| Position | Variance `q(1-q)` | Variance/fee | Model error `d=2q(1-q)` | Net correction `d-lambda*f` |
| --- | --- | --- | --- | --- |
| 1 | `1/4` | `1/8` | `1/2` | `3/10` |
| 2 | `3/16` | `3/16` | `3/8` | `11/40` |

The ratio selects position 2, whereas the fixed-quota net criterion selects
position 1 because `3/10-11/40=1/40`. The favored position receives `3/4`
probability and the other `1/4`. Shifting that extra `1/2` probability to the
better net position improves the expected objective by

`(1/2)(1/40)=1/80`.

The complete expected objectives independently confirm the difference:

`J(favor 1)=7/8-[(3/4)(3/10)+(1/4)(11/40)]=93/160`,

`J(favor 2)=7/8-[(1/4)(3/10)+(3/4)(11/40)]=95/160`.

Their difference is `2/160=1/80`, exactly as reported. These are supplied
model parameters, not measured service fees, empirical truth probabilities,
new labels or a selected replacement policy. A benefit/cost ratio can solve
other allocation problems; this witness suffices to separate it from the
stated fixed-count net objective.

The conclusion is appropriately limited: immediate correction, information
for later learning, and narrower performance intervals are distinct possible
acquisition goals. The quota-regret theorem guarantees neither the fee-proxy
heuristic's optimality nor learned value of computation. The note starts no
P3-08 integration or further recurrence.
