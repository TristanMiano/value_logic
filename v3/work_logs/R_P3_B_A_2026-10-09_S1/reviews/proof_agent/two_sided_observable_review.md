# Two-sided observable certificates: independent analytic review

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. R-P3-B-A.
Same-model, nonblind independent review. **Zero principal clock credit.**
No policy, label service, calculator, experimental probe or private-score
comparison was executed for this review.

## Verdict and source boundary

**PASS for the base-policy interval theorem and its stated per-arm, fixed-end
coverage.** The four-tail constants are sufficient. The clipping and retained
empty-interval requirements are sound. The hard-answer override permits
transfer of upper loss bounds under the stated coupling, but does not transfer
lower bounds or justify a new concentration calculation from changed forecasts.
The exact algebra-versus-centering distinction is explained in §5.

Initial reviewed `development/observable_certificate/two_sided_design.md`:
SHA-256 `41a1c9538d0ae697f52cf242be53faa1fe2219892004d77cc707ffb9964a0659`.
Underlying `development/centered_certificate_design.md`:
SHA-256 `2d1b432a851df6076402de1aa3eef10b081243f28f11a77c7992d5ca758ab1ae`.
Both exact documents are retained beside this note. This is an analytic
design review, not certification of a later two-sided calculator or its output.

## 1. Common centered residual

For the emitted base forecast q and binary label y, define

`d=q+(1-2q)y=1/2+r`, `r=(1-2q)(y-1/2)`, and `v=q(1-q)`.

Then Brier loss is `g=d-v`. Put `n=T-m`, let V be the unbought conditional
action-error sum and F the immutable all-issued Brier sum. The centered
estimators are

`Uc=n/2+sum_k (1/pi_J-1)r_J`,

`Ac=T/2-sum_t v_t+sum_k r_J/pi_J`.

For each base-policy path,

`V-Uc = F-Ac = D = sum_k [sum_{t in block k} r_t-r_J/pi_J]`.

The base forecast vector and propensities are fixed before that block's fresh
selector. Each bracket therefore has conditional mean zero. Its conditional
range has width at most
`C_k=max_t |1-2q_t|/pi_t`, since `r_t/pi_t` lies in `[-C_k/2,C_k/2]`.
This C is predictable in the source-bound fixed-tape/frozen-block proof;
the offline calculator may reconstruct it later from the retained public
forecast records. Let `Q=sum_k C_k^2`.

One event bounding D gives simultaneous bounds for V and F. Treating these
as separate independent residuals would spend error probability needlessly.

## 2. Two signs, constants and probability budget

The conditional bounded-range exponential inequality gives nonnegative
supermartingales for both signs:

`exp(±lambda D_k-lambda^2 Q_k/8)`.

Fix `R=S*ceil_sqrt(2m)>0`, using only the declared m and S, and set
`lambda=8/R` before observing the realized Q. Here `S=B` for uniform selection
or `S=2B` for the ticket rule. For either sign, probability at most `1/80`
is assigned to exceeding

`lambda Q/8+log(80)/lambda`.

The exact partial sum `sum_{j=0}^5 5^j/j! = 1097/12 > 80` proves
`log(80)<5`. Consequently the proposed radius

`rho_two = Q/R+5R/8`

is sufficient for each sign. The event `|D|<=rho_two` has probability at
least `1-2/80=39/40` and supports both V and F.

The previous one-sided assertion `rho<=R` must **not** be reused. Since
`Q<=mS^2<=R^2/2`, the new two-sided radius satisfies `rho_two<=9R/8`; it can
exceed R. No numerical optimization of lambda using the realized Q is allowed
under this particular exponential proof.

Conditional on the full selector/feedback path, the source's unbought action
bits remain independent and do not influence future selectors or weights.
The actual terminal error count L is a sum of n independent Bernoulli losses
with conditional mean V. Hoeffding's two signs each have tail at most
`exp(-2a^2/n)`. With

`a = ceil_sqrt(ceil(5n/2))`,

we have `a^2>=5n/2`, so each tail is below `exp(-5)<1/80`. The two action tails
cost another `1/40`. A union bound gives joint probability at least **19/20**
for both sampling signs and both action signs. Independence between sampling
and action deviation events is unnecessary for this union bound.

At that fixed end, valid raw intervals are

`V in [Uc-rho_two, Uc+rho_two]`,

`F in [Ac-rho_two, Ac+rho_two]`,

`L in [Uc-rho_two-a, Uc+rho_two+a]`.

The sampling part also has a bounded-prefix first-crossing guarantee for the
**same fixed lambda**, using each prefix's `D_k,Q_k`. This does not authorize
recomputing R from each prefix without an additional argument. The conditional
action calculation is fixed-end; the full joint terminal certificate is not
an anytime statement. Nor is it simultaneous 95% coverage for all 23 arms.

## 3. Deterministic clipping and empty intervals

Public pathwise bounds are

`Vmin=sum_unbought min(q,1-q)`, `Vmax=sum_unbought max(q,1-q)`,

`Fmin=sum_all min(q^2,(1-q)^2)`, `Fmax=sum_all max(q^2,(1-q)^2)`.

Intersect the raw V and F intervals with these bounds and L with `[0,n]`.
Because these envelopes contain the true targets pathwise, they need no
additional probability allocation. The centered public sufficient statistics
already recover the lower envelopes from
`Vmin=n-Vmax` and `Fmin=T-2*sum(v)-Fmax`; unbought labels are unnecessary.
One may additionally use the clipped V interval plus the action radius before
intersecting with `[0,n]`. Integer rounding of L's endpoints is also safe.

If an intersection has lower endpoint above its upper endpoint, retain an
explicit **empty interval** and the row. Do not reverse endpoints, manufacture
a point interval or silently drop the row. Empty intervals should not receive
ordinary valid interval-diagnostic labels; any saved raw threshold predicates
must be distinguished from valid interval conclusions. Such an empty result
is outside the claimed confidence event under the theorem premises.

For a nonempty valid interval, `F_lower>T/4` supports the stated worse-than-half
Brier conclusion; `V_upper<n/2` and `V_lower>n/2` support the corresponding
conditional-action comparisons. These are episode-performance statements,
not a prediction about future requests, an economic comparison with changed
costs, or evidence that deterministic MT seeds satisfy a confidence premise.

## 4. Diagnostic and data scope

The design correctly preserves all 23 already selected arms, uses sealed
public statistics to form intervals, and keeps private evaluation outside
that formation and retention decision. It explicitly acknowledges that this
is post-run DEVELOPMENT analysis after earlier scores were exposed, not a
new confirmatory experiment. A formula valid under fresh fair bits does not
turn the saved deterministic seeds into demonstrated frequentist coverage.
Calculator work remains separately accounted offline analysis.

## 5. Hard-answer overrides: what transfers

Keep the raw base policy's purchases, updates, forecasts, action coupling and
statistics. A sound additional mechanism that replaces an output by the
correct answer weakly decreases its loss pointwise. Therefore the same event
that upper-bounds base F or actual base terminal errors also upper-bounds the
corresponding overridden losses. For conditional V, retain the same
conditioning and base-action coupling. Additional override resource costs
still require their own bill. Lower bounds do not transfer: an override can
reduce a previously large base loss to zero.

Two different issues must be kept separate:

1. Base estimators `Uc,Ac` generally do **not** have the same shared residual
   with the new overridden targets.
2. If *all* statistics and targets are consistently recomputed from a changed
   q, the algebraic identity `V-Uc=F-Ac` still holds. What can fail is the
   conditional mean-zero and predictable-range premise needed for the
   concentration theorem.

A two-position example establishes the distinction without a code probe.
Let both requests be the same true query and the raw forecasts be `(1/2,1/2)`.
Select uniformly. If the first answer is bought, override the later forecast
to one; otherwise leave both forecasts at one-half. With consistent recomputed
statistics, `D=-1/2` when the first position is selected and `D=0` when the
second is selected. The algebraic shared identity holds in both cases, but
`E D=-1/4`, not zero. The current selector has changed a later forecast vector
inside its own block.

Thus the design's intended **base-upper-only transfer** is sound. A new
two-sided confidence calculation from overridden forecasts needs its own
information and timing proof; pointwise improvement alone supplies neither
that proof nor a transferred lower bound. This identifies a P3-08 interface
requirement without starting its implementation.
