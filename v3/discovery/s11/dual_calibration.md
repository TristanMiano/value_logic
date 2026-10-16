# Calibrating the task certificate instead of every marginal

Codex (GPT-6), DEVELOPMENT candidate, not an executed learner or novelty claim.
This combines the invoice-flow dual with ordinary importance sampling and
martingale concentration. It opens a source-acquisition question distinct from
merely optimizing a supplied probability table.

## A pathwise certificate supplies a scalar target

Fix a checked invoice certificate (h,lambda). It establishes, for every full
score vector x, B(x)<=h_0(0)+sum_i lambda_i(x_i). Put

```math
a_i=\min_x\lambda_i(x),\quad
g_i(x)=\lambda_i(x)-a_i,\quad
R_i=\max_x g_i(x),\quad b=h_0(0)+\sum_i a_i.
```

Then 0<=g_i<=R_i and B(x)<=b+sum_i g_i(x_i). Marginal distributions are
not required to check this inequality. A fallible model may propose useful
prices; the exact arc checks determine validity for every score vector.
Model quality affects how tight the certificate is, not its pointwise soundness.

Before observing the current vector, sample a coordinate I with known
probability q_i>0 wherever R_i>0. Observe X_I and return Z=g_I(X_I)/q_I.
Conditionally on the entire vector, E_I[Z]=sum_i g_i(X_i). Consequently this
one-coordinate score estimates the certificate's expectation even with arbitrary
within-vector dependence. Choosing q_i=R_i/R, where R=sum_i R_i, gives Z in
[0,R] and minimizes the worst possible bound max_i R_i/q_i. This is the
standard importance-sampling calculation, not a new unbiasedness theorem.
Coordinates with R_i=0 require no measurement; R=0 makes the bound deterministic.

## What can be guaranteed under changing sources

For request t, let the certificate, its policy and q_t be fixed using the
past. The current vector must not respond to the private draw I_t. Normalize
by a deterministic/past-known bound R_t. Given the current vector, the
importance score is unbiased. A bounded martingale argument can therefore
control the difference between sum_t Z_t and sum_t sum_i g_ti(X_ti), even if
the full vectors are mutually dependent or chosen adaptively before I_t.
Together with the pathwise invoice inequality, this yields a high-probability
upper bound on the actual cumulative policy invoice from partial measurements.
It does not forecast the next request under an unconstrained distribution
change, and it does not turn past calibration into a stationary marginal law.

For deterministic R_t, Hoeffding-Azuma gives the simple fixed-horizon form

```math
\sum_{t=1}^T B_t(X_t)
\le \sum_{t=1}^T (b_t+Z_t)
 +\sqrt{\tfrac12\log(1/\delta)\sum_{t=1}^T R_t^2}
```

with probability at least 1-delta over the private sampling draws, provided
the required predictable/conditional assumptions hold. For random predictable
ranges, use a valid self-normalized bound or a deterministic envelope; do not
silently substitute a realized sum of ranges into this displayed fixed-bound
formula. Time-uniform stopping needs a confidence sequence or an explicit
union-bound schedule, not an unmodified fixed-T bound.

## The measurement bill cannot disappear

The randomly chosen coordinate generally is not the fixed policy's first
query. If it is bought as an extra calibration query, its actual fee must be
added to the service invoice. Reusing its answer may reduce later fees only
under a separately specified interface. Assuming that an arbitrary coordinate
is free because the controller would sometimes inspect it is invalid.

If the calibration purchase itself changes the tested policy, certify that
augmented policy. Alternatively calibrate on separate paid requests or reserve
a fixed pre-observation sampling decision. Choosing the coordinate after seeing
correlated outcomes invalidates the simple estimator. Choosing a new certificate
after seeing the same calibration samples also needs simultaneous coverage,
sample separation or a genuinely predictable online analysis.

## Cheap screen to decide usefulness

First inspect R and the number of positive R_i in the existing exact invoice
certificates. Large dual ranges can make one-coordinate calibration statistically
expensive despite reducing the number of distinct marginals estimated. Compare
its sample-fee requirement with full-law histograms, an ordinary fixed-policy
evaluation baseline, and simply paying the fallback. Reject the practical claim
quickly if range and measurement fees dominate; retain only the valid reduction.

## First range screen and a possible repair

`dual_ranges.json` records a cheap analytical screen, with no newly drawn
samples. Only three of fourteen already selected invoice cases have a checked
upper below immediate fallback. To estimate their certificate means to half
that predicted margin with delta=0.05, the elementary bounded-range calculation
requires 9,273, 1,256 and 493 samples respectively. Expected additional
calibration fees are about 17,267, 1,902 and 935. These are sufficient-count
forecasts, not empirical lower bounds or guaranteed adoption times. The small
case with an approximately one-unit predicted improvement looks unattractive
under this estimator. The 80-coordinate case is less immediately implausible,
but no source-learning gain has yet been demonstrated.

The relevant use is partial *counterfactual evaluation* of a policy that has
not been run on the full vector. If the policy is already executed, its invoice
is directly observed and this estimator adds no value merely by estimating it.
Stationary evaluation across requests can turn the sample mean into a future
expectation bound; the changing-source martingale statement above only controls
the chosen sequence of counterfactual invoices. Keep those two duties separate.

A dual optimized solely for the sharp model-based bound need not have a small
calibration range. A candidate repair chooses prices to minimize U+eta R,
where U=h_0+sum p_i lambda_i and R=sum_i(max lambda_i-min lambda_i). This is a
linear program after introducing lower/upper price bounds for each coordinate.
The penalty coefficient can reflect a prospectively fixed statistical precision
budget. It trades certificate tightness against the range of the sparse
measurement. Pointwise validity still follows from the same arc inequalities.
This is conventional regularized robust optimization applied to the certificate,
not a claim that generic regularization or importance sampling is new. Compare
with a range-minimal certificate among sharp dual optima before crediting any
benefit to sacrificing bound tightness.

Under uncertain marginal probabilities, an oscillation penalty also gives the
elementary upper bound E_p'[lambda_i]<=E_p[lambda_i]+TV(p_i,p_i') R_i.
Equality is not guaranteed when the source lacks sufficient mass at a minimizer
or a probability-simplex boundary binds. Thus U+eta R is a valid TV-robust
upper bound, but it is not automatically the exact worst-case expectation over
probability balls. This limits the stronger DRO identification.

## Range-regularization screen

The prospectively chosen penalty grid is 0, 1/100, 1/20, 1/10, 1/4, 1/2,
plus a range-minimization solve constrained to the previous sharp upper value.
`range_dual.py` and `rd01` record three reused duties, exact repaired arc checks,
and all outcomes. These are obtained feasible certificates, not an independently
certified globally optimal frontier. The range-minimizing sharp solutions match
the original ranges in these cases, so the observed improvements do not merely
remove gratuitous solver degeneracy.

On the five-coordinate case, eta=1/20 changes the upper bill from 417/55 to
2621/330 and the sampling range from 35 to 53/2. The displayed sufficient
sample count falls from 1,256 to 994, with lower average measurement fee.
On the eighty-coordinate case, eta=1/10 changes the checked upper bill from
about 104.836 to about 108.307 and range from about 472.933 to about 405.178.
The same sufficient-count calculation falls from 493 to 415. This is a useful
bound/measurement tradeoff to investigate, but no samples were drawn and no
deployment savings were measured. The six-coordinate case remains unattractive:
even its improved bound/range pair requires 8,584 samples under the simple rule.
Large penalties can collapse the certificate to a zero-range worst-path bound
that exceeds fallback; eliminating sampling alone is not the objective.

## A fixed mathematical source needs no random truth assumption

The same pointwise certificate can concern one fixed vector x of unresolved
computable mathematical scores. Repeated independent draws I_t from q sample
coordinates of that fixed vector. Then Z_t=g_I(x_I)/q_I has mean sum_i g_i(x_i)
over the reasoner's own randomization. The finite-sample bound therefore
certifies the counterfactual invoice B(x), without positing a stochastic law
for mathematical truth or training on unresolved outcomes as labels. Actual
checked evaluation of sampled coordinates is still required. This connects
the new invoice certificate to the existing S08 finite-population mechanism;
the random-sampling principle itself is inherited, not a new contribution.

Repeated draws can reuse paid receipts for the same deterministic coordinate,
but the draw sequence and estimator must retain their declared sampling law.
Sampling without replacement admits different, potentially tighter inference.
If running the target policy directly is cheaper than calibrating its surrogate,
the meta-evaluation has no practical purpose. The present range screen is not
evidence that it repays its own cost. It warrants a targeted acquisition study
only for a duty where avoiding expensive policy execution has actual value.

## Sampling cost depends on which statistical bound is optimized

For one independent sampled coordinate per draw, let M(q)=max_i R_i/q_i and
average fee c(q)=sum_i q_i c_i. The elementary Hoeffding sufficient sample
fee is proportional to M(q)^2 c(q). Among positive q on informative coordinates,
q_i=R_i/R minimizes this product even with heterogeneous nonnegative fees.
For fixed M>=R, every q_i>=R_i/M; put any residual mass on a cheapest coordinate.
Then c(q)>=c_min+sum_i R_i(c_i-c_min)/M, so M^2 c(q) is bounded below by a
nondecreasing function of M, minimized at R. Equality there gives the proposed q.
Zero-range coordinates can absorb residual mass but cannot improve this bound.

This does not make fee-blind allocation universally optimal. For a second-moment
bound using sum_i R_i^2/q_i, Cauchy-Schwarz gives

```math
\left(\sum_i q_i c_i\right)
\left(\sum_i R_i^2/q_i\right)
\ge \left(\sum_i R_i\sqrt{c_i}\right)^2,
```

with q_i proportional to R_i/sqrt(c_i) when all relevant fees are positive.
That is the familiar cost-adjusted allocation. Variance-sensitive confidence
methods may therefore favor different prices. The zero-fee limit needs separate
treatment. Do not describe the earlier range-optimal design as a globally
optimal acquisition rule.
