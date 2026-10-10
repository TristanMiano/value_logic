# Predictable hard snapshots followed by live correction

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
**P3-08 DEVELOPMENT extension**, proposed after the first 114 common runs.
Those runs, their source closure and the first live-report construction are
retained. This note changes a reporting service, not the executed learning
or purchase policy, and does not select an optional external-certificate task.

## 1. Why a second reference process helps

The [first live correction theorem](08_live_hard_performance.md) translates
the cache-free base statistics by exactly observable removed losses. Its
sampling widths still include forecasts for queries already known at block
entry. The [accepted frozen-hard construction](07_observable_performance.md#10-a-sufficient-predictable-hard-answer-interface)
allows those positions to be removed from the unknown sampling residual.
The two constructions can be composed, without recomputing a concentration
proof on the nonpredictable live forecast vector.

Let H^0_kt indicate a current hard answer present **at block entry**, and
H^1_kt indicate a current hard answer before the particular live issuance.
The source-matched hard broker has H^0<=H^1 within one successful epoch.
For its hard-disabled counterpart use both masks zero. These definitions
are a counterfactual reference inside the report, not a rewrite of any
historically issued forecast.

The intermediate snapshot forecast is q^s=y on H^0=1 and q otherwise.
Its vector is predictable given the past selected feedback. Its actual
propensities are still those of the **executed** selector, which can use
the raw base forecasts and paid public cost proxies. No different selector
is substituted into the report.

## 2. Snapshot centers and the shared residual

For the raw q define d=q+(1-2q)y. Put

```math
a^s_t=(1-H^0_t)/2,\qquad
r^s_t=(1-H^0_t)(d_t-1/2),\qquad
v^s_t=(1-H^0_t)q_t(1-q_t).
```

The snapshot conditional error is a^s+r^s and its Brier loss is a^s+r^s-v^s.
The observable centers are

```math
U_s=\sum_{t\notin\{J_k\}}a^s_t
        +\sum_k(\pi_{kJ_k}^{-1}-1)r^s_{kJ_k},
\qquad
A_s=\sum_t(a^s_t-v^s_t)+\sum_k r^s_{kJ_k}/\pi_{kJ_k}.
```

Direct subtraction gives

```math
V_s-U_s=F_s-A_s
=\sum_k\left(\sum_t r^s_{kt}-r^s_{kJ_k}/\pi_{kJ_k}\right). \tag{1}
```

For each block the right-hand increment has conditional mean zero. Its
conditional range width is bounded by the predictable public quantity

```math
C^s_k=\max_t\frac{(1-H^0_{kt})|1-2q_{kt}|}{\pi_{kt}}
\le C^0_k,\qquad Q_s=\sum_k(C^s_k)^2. \tag{2}
```

This is precisely the inherited predictable-mask proof. The masks can be
reconstructed retrospectively from **earlier-block** checked receipts;
retrospective computation does not change their predictability. Its actual
reads, reconstruction, arithmetic and output must be paid.

## 3. Translate only the additional within-block corrections

Let Delta^new_F and Delta^new_V be the first theorem's corrections restricted
to H^1=1 and H^0=0. Then the live targets satisfy

```math
F_1=F_s-\Delta^{new}_F,\qquad
V_1=V_s-\Delta^{new}_V.
```

Consequently U_s-Delta^new_V and A_s-Delta^new_F again have exactly the same
unknown residual (1). Applying the fixed-rate two-sided radius
Q_s/R+5R/8 with the old prospectively chosen R is valid. The action-error
allowance still uses the number n_1 of unselected positions with H^1=0.
Neither a changed live mask nor a changed propensity enters (2).

Q_s<=Q_0 holds pathwise for this same underlying policy. This does **not**
order the complete endpoints: the centers changed as well. The first raw
base report and this snapshot report are separate declared confidence
constructions unless their error budgets are jointly allocated.

## 4. A finite, predeclared rate grid

The original fixed R can be conservative after most coordinates become
hard-known. Optimizing a rate after observing Q without an error correction
is still invalid. A finite predetermined grid gives a simple paid remedy.

Let S=B or 2B as appropriate and R_*=S ceil(sqrt(2m)). Before any labels,
form a set of rates

```math
\mathcal R=\{S,2S,4S,\ldots,2^jS\}\cup\{R_*\},
\quad j=\min\{j\ge0:2^jS\ge R_*\}.
```

Remove a duplicate R_* if present; let J be the resulting size. Fix
c=ceil(log_2(80J)), an exactly computable integer. Since e>2,
exp(c)>2^c>=80J. For **each** R in this fixed set use lambda_R=8/R.
The conditional moment/stopped-exponential argument applied to each sign
has failure probability at most exp(-c)<=1/(80J) for radius

```math
\rho_R(Q_s)=Q_s/R+cR/8.
```

A union bound over both signs and all J rates has failure probability at
most 1/40. Thus all these inequalities hold on the same sampling event,
and the reporter may validly choose

```math
\rho_{grid}(Q_s)=\min_{R\in\mathcal R}\rho_R(Q_s). \tag{3}
```

This is a finite union correction, not an unpenalized optimization over
observed variance. It may be worse than the single-rate rule when that
rate was already well matched. No universal endpoint improvement is claimed.
The exact choice of R attaining the minimum is itself public and reported.

Combining the common sampling event with the same conditional action tails
as the first theorem gives a per-episode, fixed-end **19/20** joint interval
for live F,V,Z. All-path execution and reporting completion, current sound
receipts, the unchanged base/selector path and independent fair supplied
bits remain premises. Seeded development agreement is not coverage evidence.
The confidence statement is not conditional on a budget-selected success.

## 5. Planned finite implementation and comparison

The reporter will expose explicit `basis=base|snapshot` and
`radius=fixed|grid` choices. For the confidence theorem, both must be fixed
before inspecting that episode's outcomes, or receive their own valid
selection/error-budget argument. Selection just before a retrospective
report call is insufficient. The DEVELOPMENT extension uses snapshot/grid;
its reanalysis of already seen seeded traces checks formulas and costs,
not prospective confidence coverage. It will retain the raw-base exact
corrections separately from the corrections relative to its chosen reference,
so private audit can still check the actual hard/base pathwise differences.
The report's reference centers and widths will be named explicitly.

The grid is tiny under T<=8192, B>=2 and the existing precision limits.
Compare its unreduced rational radii by paid bounded integer cross-products.
A conservative exponent calculation using T<2^14, m<2^13, D<=2^32,
M=B+1<2^11, S<=2^11 and R<2^15 keeps the radius-comparison intermediates
below 256 bits. The existing 2^48 reporting-completion envelope remains
loose; an independent code/cost check must confirm the implemented bound.

Recompute from the same sealed public traces before any new private-score
comparison. Preserve the first report and any failures. The comparison is
about purchased-information performance accountability and its cost; an
ordinary representation mirror can provide the identical service. It does
not establish a special economic advantage of value notation.
