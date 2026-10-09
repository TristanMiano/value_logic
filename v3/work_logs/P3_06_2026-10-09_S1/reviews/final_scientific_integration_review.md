# P3-06 final scientific integration review

Contributor: **ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer**.
October 9, 2026 UTC. Signed review by `/root/p306_proof_review`.
Subagent effort is unmeasured and receives **zero principal Research90 credit**.
This review changes no clock, phase status, preserved source, production module
or gate. It does not start P3-07.

**Disposition:** the reviewed mathematics and saved numerical comparisons are
consistent at their stated scope. All scientific wording corrections listed
below have been repaired and reread, including normalized capital priors in
CF-16 and the explicit CF-17 exception to the general repricing warning.
No unresolved scientific defect was found in the reviewed statements. No new
learner or probe was run for this final review.

## 1. Scope and method

The principal review targets were
[the main derivation, especially section 8](../../../derivations/06_cost_forecast_refinement.md),
[the repricing companion](../../../derivations/06_price_replay.md), and
[the calibration companion](../../../derivations/06_calibration_scope.md).
The final pass also included the new
[CF-16 BRIA companion](../../../derivations/06_bria_boundary.md), CF-17's
coordinated unit transformation, the corresponding boundaries in
[the capital companion](../../../derivations/06_capital_comparison.md), and
the BRIA discussion in the [primary-source record](../../../literature/06_forecasting_sources.md).

The review reconstructed the identities, quantifiers, constants and scope
conditions from the earlier independent proofs. It inspected the saved JSON
results, source bindings and relevant driver code, checked reported decimal
values against the retained rational values, and compared existing numerical
fields across evidence versions. Reading and hashing existing evidence is
not a rerun of the scientific experiment. The separate
[final evidence audit](final_evidence_audit.json) records the broader
preservation and cross-version integrity checks; its counts are not added to
this review's own work.

## 2. Corrected findings retained as part of the review

| Finding during integration | Correct scientific statement | Disposition at this read |
|---|---|---|
| CF-13 attributed its sharp factor to a two-action crossing at a cell midpoint. | The factor is attained at a grid-endpoint crossing with the appropriate tie choice. A two-action midpoint crossing gives the smaller factor stated below. | Repaired and reread. |
| The smaller midpoint factor was initially unqualified for a general finite action table. | The claim requires a two-action table; an additional lower action can invalidate it. | Repaired and reread. |
| The new-action replay service listed retrospective losses without listing admitted answers among its scoring inputs. | New mixtures need the retained scalar and new rule; their retrospective realized losses additionally need admitted labels. | Repaired and reread. |
| A small numerical-allowance fraction risked being read as a causal claim about rerunning with tighter tolerance. | Holding the recorded forecasts and variance fixed makes the allowance contribution small; a different root tolerance may change the trajectory and variance. | Repaired and reread. |
| The sparse BRIA witness was described as having bounded unnormalized report-test residuals. | Those residuals can grow logarithmically; their time-normalized values vanish. The later summable-error witness has bounded unnormalized residuals. | Repaired and reread in the source record. |
| The repricing warning made the prospectively represented menu sound like the only possible weight-certificate transfer. | CF-17's coordinated common weight scaling is another exact transfer. An arbitrary new schedule is not automatically covered. | Repaired and reread. |
| CF-16's phrase about every positive-prior capital sum omitted its normalization. | The displayed bound holds when the nonnegative priors sum to one; strict positivity is the convention used by CF-12. | Repaired and reread. |

These corrections limit or repair actual claims. They do not remove an
unfavorable result or turn a finite check into an infinite theorem.

## 3. Saved comparisons and certificate applicability

The main four-case table agrees with the saved mathematical results. Its
ordered plain/decision/AA Brier-loss-per-weight triples are
`0.011165 / 0.110599 / 0.004223`,
`0.265712 / 0.308615 / 0.250303`,
`0.233969 / 0.282883 / 0.192746`, and
`0.266031 / 0.318507 / 0.251391`. The exact arithmetic comparator has zero
squared loss in each case. The delayed population is 120 admitted labels plus
eight pending labels, rather than 128 scored labels. The ordinary AA
implementation's floating-point measurements remain separate from its ideal
mixability antecedent; the main text makes no interval certificate for AA.

The two repricing rows agree with the saved rational scores:

| Decision-feature case | Old mixture at new prices | New mixture from old scalar | Full replay |
|---|---:|---:|---:|
| Varying stakes/actions | 167.820081 | 36.277236 | 163.266601 |
| Delayed cutoff | 317.981770 | 18.453982 | 272.141220 |

The varying-stakes Brier loss per weight changes from `0.318507` to
`0.361728` under row replay. Across the four cases, row changes alter
112–124 decision-feature forecasts and no plain forecasts; weight changes
alter 57–126 forecasts. These are counts on the fixed retained population.
They neither establish a universal sensitivity theorem nor claim that replay
improves the new objective.

The saved v2 replay manifest reports 15,368 checks. Its public projection
uses issue descriptions and admitted evidence; the expert policy is
reconstructed from admitted residue counts and public shortcut computations.
The original reports, private pending results and exact-baseline answers are
excluded. The stated full-policy replay is therefore justified for this
particular policy and fixed admission schedule. A different policy depending
on old learner reports would require its own reconstruction.

Row-only rescoring retains the old scalar Brier and tent certificate at the
old weights, but does not automatically transfer the old action-feature
certificate to the new action rule. A genuinely new weight metric requires
an explicit transfer or its own certificate. Known-cache records have exact
reports and zero forecast residual, so including them in the scored
denominator while omitting them from a learning-copy residual does not add
uncontrolled forecast error. Their exact cost-minimizing choice also adds
nonpositive regret to a fixed action comparator.

The saved capital comparison uses a different 32-issue prefix population.
Its Brier-loss-per-weight column is `0.026581`, `0.257374`, `0.224023`,
`0.258997`; it improves both polynomial variants on those four prefixes and
improves AA on two. At its delayed cutoff only 29 labels are scored and three
remain pending. All 128 capital issues in the four cases have zero actual
capital allowance. The stated expert bounds of approximately `1.242454`,
`9.939627` and `39.758507` are valid displayed approximations; the delayed
number sums four copy bounds. The first and last displayed values round
upward. The issue-call ranges of 0.47–1.13 seconds and 6,528–11,936
exponential enclosure calls agree with the saved records. They do not form
a matched timing comparison with the earlier 128-query experiment.

The bound-usefulness analysis is also reported accurately: eight raw expert
bounds improve the coarse unknown-weight bound, none improves the elementary
envelope for its particular retrospectively best expert, and keeping the
negative expert-distance term improves two plain-variant comparisons. The
shortcut decision case has actual mixed regret about `-97.398460` and the
retained forecast-gap certificate about `-78.314344`. That certificate
concerns the two fixed action identities. The numerical allowance fraction
of the summed polynomial budgets ranges from about `0.000092896%` to
`0.155103135%`. This supports the corrected fixed-record statement, not a
prediction about a tighter-tolerance rerun.

The saved v1/v2/v3 mathematical query populations, forecast metrics and core
audit fields agree. The defects and repairs concern instrumentation and
receipt/interface validation and are retained as versions. Repeated equality
of those saved metrics is not independent evidence of predictive quality.

## 4. CF-13 through CF-15: action and calibration claims

For CF-13, the selected optimal endpoint slopes are nonincreasing. At a point
$`p=(j+r)/m`$, the chord through the optimal endpoint costs lower-bounds
every affine action cost. Subtracting it from the adjacent-center mixture
gives the exact upper estimate

```math
\mathrm{gap}(p)\le\frac{r(1-r)(d_j-d_{j+1})}{m}\le\frac{D}{4m}.
```

The repaired witness with rows $`Dy`$ and $`D/m`$ attains the last bound at
$`p=1/(2m)`$, when the second action is selected at the tied right endpoint.
For two rows crossing at the cell midpoint, maximization on either half-cell
instead gives $`D/(16m)`$. This qualification is necessary: adding a third
lower row can change the gap to the best action even when the two selected
endpoint rows cross at the midpoint. The fixed-table comparator identity
has coefficients $`d_j-d_a`$ outside the time sum; changing tables generally
destroys that factorization. The preserved two-round obstruction verifies
why zero fixed tent residuals need not control those changing coefficients.

CF-14 correctly assumes unit weights, immediate full feedback, fixed expert
scales, bounded action slope differences and successful root certification.
The constant $`C`$ is independent of the grid dimension. The interpolant
error is at most $`L/(2m)`$, and the prefix residual has the stated joint
coordinate bound. In the unfinished epoch, its announced length obeys
$`H\le T+1`$, so summing the geometric bounds yields the displayed uniform
$`O((1+L)T^{2/3})`$ result without a failure at the start of a large epoch.
The action slack uses the global dyadic schedule; resetting that schedule
inside epochs would produce an additional logarithmic factor. The result is
for each fixed bounded Lipschitz class and, by approximation, each fixed
continuous test. It is not uniform over all continuous functions of
unbounded complexity or arbitrary discontinuous selectors.

The CF-14 resource claims inherit the fixed-denominator rational input
contract and keep epoch summary terms separate where necessary. The active
numeric-state and literal full-feature-history bounds have the stated
orders. The production grid cap of 64 is explicit; there is no claim that
this increasing-grid extension has been implemented. Delayed feedback
requires separate copy accounting.

CF-15 is the stronger existing calibration antecedent. In
[Vovk's Working Paper 13](https://www.probabilityandfinance.com/articles/13.pdf),
section 3 equations (7)–(10) and the K29-star theorem supply the stated
Fermi–Sobolev norm and kernel. For the fixed Lipschitz ball,
$`\|f\|_{\mathrm{FS}}^2\le1+L^2`$. Its diagonal is
$`4/3-p(1-p)`$, and maximizing the variance product gives $`13/48`$.
The bare exact square-root residual constant, the direct-sum feature terms
and the scaling by $`1/\beta`$ are therefore correct.

The feature map is one-half Hölder in Hilbert norm, rather than Lipschitz;
the finite-history scalar score still has the stated Lipschitz estimate.
The prefix identity and its $`11/6`$ correction bound agree with the
[independent FS review](fs_kernel_comparison_review.md) and its saved
2,692-check probe. The conditional balanced-tree operation count remains
an unimplemented data-structure statement, not a complete bit or CPU bound.

## 5. CF-16: independent BRIA reconstruction

For $`k=\lceil\log_2(t+1)\rceil`$, there are $`2^{k-1}`$ rounds in
block $`k`$. Multiplying the block size by its error and squared error gives

```math
\sum_{t\ge1}\epsilon_t
=\sum_{k\ge1}2^{-k-4}=\frac1{16},\qquad
\sum_{t\ge1}\epsilon_t^2
=\sum_{k\ge1}2^{-3k-7}=\frac1{896}.
```

The dyadic report and cumulative-error denominators have logarithmic bit
length. The perfect expert one has zero loss, so regret to it is at most
$`1/896`$, and regret to any other expert is no larger. Every coefficient
sequence bounded in absolute value by one has total forecast residual at
most $`1/16`$ on this particular tape.

The constant chosen action zero is forecast-optimal for the displayed cost
rows. Both realized costs are zero because $`y_t=1`$, while the chosen
reward estimate is $`1-\epsilon_t/2<1`$. The constant hypothesis
recommending that same action and promising one is always testable and
always strictly outpromises. Every action-matching test set has empirical
record zero. It therefore fails the negative divergence required by BRIA
coverage, while no-overestimation holds.

I independently reopened the primary
[BRIA paper](https://arxiv.org/pdf/2307.05068), Definitions 2–7 and section
4.5, printed pages 424–426. Its test-set condition is action matching, not
membership in the outpromise set. Its always-kept-promise example already
states the finite-rejections implication. CF-16 correctly attributes that
antecedent. The added calculation is compatibility with the constant metric
bounds and small dyadic representation.

For every real coefficient and rate, completing the square gives

```math
\lambda a_t\epsilon_t-\frac{(\lambda a_t)^2}{8}
=2\epsilon_t^2-\frac{(\lambda a_t-4\epsilon_t)^2}{8}
\le2\epsilon_t^2.
```

Every calibration or action component is therefore at most
$`\exp(1/448)`$ along the actual tape, as is every unit-weight expert
component with $`0<\kappa\le2`$. A prior sum with priors summing to one
inherits the bound, and $`\exp(1/448)<448/447`$ follows from the
exponential/geometric series comparison. For the constant chosen action,
the action coefficients are zero and one-half and forecast slack is zero.
The general coefficient inequality also covers the production mixture's
exposure sequence evaluated on this tape.

This is not a proof of $`K_T\le1`$, an outcome-uniform next-step
certificate, a bound on issued allowance sums, or a production trajectory.
The new companion states those distinctions. The earlier exact report one
with reward estimate one covers the singleton hypothesis; the summably
perturbed report does not. Thus the report-transport observation is valid:
summable output displacement alone does not preserve exact BRIA coverage.
The witness has optimal realized decisions, so its criterion failure is not
evidence of poor realized decision performance.

The saved fixed 127-round probe reports PASS on 20,588 checks. I read its
source and result and verified the plan/source hash bindings, without running
it. Its finite enumeration supports the arithmetic fixture; the infinite
statement follows from the proof above.

## 6. CF-17: independent unit-covariance reconstruction

With $`w'=uw`$, $`c'_i=vc_i+g`$, $`\eta'=v\eta`$ and
$`\gamma'=\gamma/v`$, the common affine offset cancels from both the
forecast cost difference and action exposure. The mixture is unchanged.
Every feature and every coordinate magnitude/Lipschitz bound scales by
$`u`$. Assuming the same previously admitted labels gives
$`R'=uR`$, so the implemented score and its Lipschitz estimate scale by
$`u^2`$. With $`\delta'=u^2\delta`$, all endpoint tests, midpoint
tests and sufficient-bisection comparisons agree exactly. This proves the
same output and copy assignment inductively, including an explicit cap.

Per-copy variance, actual allowance and budget scale by $`u^2`$.
Weighted squared losses and calibration residuals scale by $`u`$; weighted
relative action regret and smoothing slack scale by $`uv`$. The exact
sum of square-root copy budgets scales by $`u`$. A separately rounded,
fixed-grid rational upper enclosure need not satisfy exact covariance.
Absolute action costs additionally acquire the common weighted offset;
relative regrets cancel it.

For the capital implementation, transforming its envelopes by
$`w'_{\max}=uw_{\max}`$ and $`D'_{\max}=vD_{\max}`$ makes its rates
$`\kappa/u`$, $`\lambda/u`$ and $`\rho/(uv)`$. Every log increment
for both possible labels is identical, so the exact enclosure inputs and
search branches are identical. Its Brier/calibration certificates scale by
$`u`$ and its action certificates by $`uv`$. Fixed expert values, the
same issue/admission schedule, stable action identities, unchanged horizon,
priors and dimensionless capital numerical controls are needed. Arithmetic
bit costs are not invariant.

The saved 16-tick public-prefix probe uses the existing null and delayed
cases with three declared transformations and reports PASS on 3,522 checks.
Its six case/profile records have 16 issues each, with 16 admissions for the
null case and 13 admissions plus three pending for the delayed case. I read
its source and verified its input/plan/source bindings without rerunning it.
This is representation transport, not a new predictive population or a claim
that arbitrary repricing is harmless.

## 7. Remaining scientific boundaries

The newly added finite-domain qualification in the main text is sound.
With finitely many possible residue keys, permanent exact caching and eventual
admission for every encountered key, the finite set of first admission times
has a finite maximum. Only finitely many indexed requests can precede it.
Thus eventual exact prediction can follow from caching alone, without an
unbounded-language induction theorem or a uniform bound on how long the
finite pre-admission period lasts.

The duty table also retains the necessary distinctions: supplied-expert
regret does not imply low loss without a good expert; rare-bin mass and
pending weight have their own denominators; mixed action cost is separate
from a sampled action path; common offsets can preserve relative regret
while changing absolute cost error; and arbitrary input denominators do not
meet CF-11's restricted bit premise. The residue-frequency expert's growing
denominator is expressly excluded from that premise.

The resulting evidence supports the restricted scalar, action, delay,
repricing and finite-resource contracts documented here. It does not support
P3-N01, full Logical Induction, full BRIA coverage, an implemented paid
acquisition policy, a universal contribution claim or a final-test pass.

## 8. Evidence identifiers for this final pass

The reviewed document snapshots have these SHA-256 hashes. The disposition
applies to their stated mathematical and empirical claims; later source-only
additions require their own review attribution.

| Document | SHA-256 |
|---|---|
| `v3/derivations/06_cost_forecast_refinement.md` | `b79eecdea706c59aa5d003075c5ca1d620e5d14264d010529f9b4c7410c2eb4b` |
| `v3/derivations/06_price_replay.md` | `563cca0d66a8f9f2e34728d1eabcf3e9fe6f39eac1431c18529285fa325130d5` |
| `v3/derivations/06_calibration_scope.md` | `299d9dd1b2209a5f3f06e6ee4ddf714745377aa03e4557b0762bd81994716861` |
| `v3/derivations/06_bria_boundary.md` | `ff7c4be05de6296f096e6d87cfec7533fd8dc5e6f28ded00918fd2119b163597` |
| `v3/derivations/06_capital_comparison.md` | `8791ca2e3d587b10562ccef3fe7dffd9c5e08ce8640bc0a6972ffeabbedf0a18` |
| `v3/literature/06_forecasting_sources.md` | `25cda0be11236ec9e249f2e9d64b129949f7861cdaf966a907ecf2955facfb43` |

The following retained result hashes were checked without executing either
probe:

| Artifact | SHA-256 |
|---|---|
| `development/bria_constant_bound_v1/result.json` | `3fa74aba49fb0c4e8e08845273e0d9bb5416b3d1f30fb4f6e35e6f52ede27ea5` |
| `development/bria_constant_bound_v1/probe.py` | `2244782fa3d3bc2f8aa7d18caae1677f7330bc982c7ae403131cd867b2ff91c2` |
| `development/unit_covariance_v1/result.json` | `70dd26c4205892cc23e59770efcac2c4a1f97005c70828d0bf7569c8f5235a42` |
| `development/unit_covariance_v1/probe.py` | `0a6a6b996ead751a01a4d7b8641269b2d153a6255a65e03840d85a83a2e64fc2` |

The unit-covariance probe's production source bindings remain polynomial core
`b66af7ec64b7e690aaa15c0901b2ccb220f93f97962052607481ddd7ae240e07`
and capital core
`2c04defb96a9a8f17ef5d32bacfeaadb70f5b981de3491f68eaba7461c1b5ecb`.
The substantive earlier reconstructions remain in the independently authored
reviews linked above; their work and finite checks are not counted a second
time by this final integration review.
