# Independent exponential-capital implementation review

Contributor: **ChatGPT (GPT-6 Astra Pro), independent implementation reviewer**.
October 9, 2026 UTC. All executable evidence below is development. Reviewer
effort receives zero principal Research90 credit.

**Disposition:** the reviewed v1.1 implementation has valid rational
exponential enclosures, logarithmic upper bounds and additive capital
certificates. A pre-repair cache-validation defect is preserved and fixed.
No invalid numerical certificate was found. The capped search does not promise
to achieve its requested allowance on every valid input, and correctly retains
its actual allowance when it cannot do so.

The abstract construction is independently reconstructed in
[the capital comparison](exponential_capital_comparison.md). This review checks
the correspondence of [the executable implementation](../../../checks/06_capital_forecasting.py)
to that construction and its numerical/input boundary.

## 1. Preserved source and reproducible evidence

The first formal source snapshot has SHA-256
`376ad1c9b755845d3bce7e0d78ccfc281dad2091cfeb602dbe295b7a73583583`.
The repaired v1.1 snapshot has SHA-256
`2c04defb96a9a8f17ef5d32bacfeaadb70f5b981de3491f68eaba7461c1b5ecb`.
Both use the unchanged scalar action-table/rational-input dependency with
SHA-256
`b66af7ec64b7e690aaa15c0901b2ccb220f93f97962052607481ddd7ae240e07`.

The [review plan](../development/independent_capital_review_v1/review_plan.json),
[audit script](../development/independent_capital_review_v1/audit_capital_v1_1.py)
and [result](../development/independent_capital_review_v1/audit_capital_v1_1_result.json)
preserve **3,107 passing checks**:

| Probe family | Coverage |
| --- | --- |
| Exponential enclosure | 160 exact rational cases over four precisions, including signs, reduction boundaries, tiny inputs, and magnitude 1,024 |
| Logarithmic enclosure | 44 upper-bound and absolute-error checks using independently enclosed exponentials |
| Invalid inputs and public immutability | 76 rejected-call or immutable-assignment cases, with state fingerprints where applicable |
| Counterfactual capital updates | 16 length-four binary paths, 64 issues and 128 binary branches |
| Cap exhaustion | Two distinct failures to meet the request, with valid retained allowances |
| Common cost offsets | Four paired rounds with outcome-dependent common offsets of order $`10^{40}`$ |

All normal four-round paths met their requested per-round allowances. The
deliberate cap cases did not. No source, older evidence, principal clock,
phase status or gate decision was modified by this reviewer.

## 2. Exponential enclosure proof

For nonnegative $`z\le1`$, the Taylor sum through degree $`n`$ is a lower
bound. Its omitted positive terms obey

```math
\sum_{k=n+1}^{\infty}\frac{z^k}{k!}
\le\frac{1}{(n+1)!}
   \sum_{j=0}^{\infty}\frac{1}{(n+2)^j}
\le\frac{2}{(n+1)!}.
```

The implementation's factorial and next-index accounting match this bound.
It rounds the positive lower sum downward and the sum-plus-tail upward onto
its dyadic grid. Both endpoints are nonnegative, so squaring is monotone;
outward rounding after each square preserves containment. Before inversion,
the lower integer endpoint is at least the grid scale, so its division cannot
have a zero denominator. For a negative input, reciprocal endpoints reverse
order and are again rounded outward. The zero case is exactly $`[1,1]`$.

The independent reference uses a different reduction and arithmetic path:
divide by the integer ceiling of the input's absolute value, bound the omitted
Taylor tail by the actual next term and a geometric ratio, and raise the
resulting rational endpoints to an exact integer power. It performs no dyadic
squaring or intermediate rounding. Each production interval contains the
finer independent rational interval in every tested case.

The precision parameter controls the dyadic grid, not a fixed absolute width
after repeated squaring and not a hard total-bit bound. The probes include
$`\exp(-1024)`$ enclosed by $`[0,1/65536]`$ at 16 bits, while positive
large inputs require long integer numerators. The largest stored endpoint
numerator in these probes has 1,572 bits. These observations agree with the
implementation's explicit exclusion of a hard transient memory/CPU bound.

## 3. Logarithmic upper bound

The reduction writes the positive input as $`2^k r`$, with
$`1\le r\le2`$. For $`z=(r-1)/(r+1)`$, the logarithm is
$`2\sum_{j\ge0}z^{2j+1}/(2j+1)`$, with nonnegative terms. After
$`n`$ terms, replacing all subsequent odd denominators by $`2n+1`$
and summing their geometric numerator series gives the stated tail bound.

The local tolerance is $`2^{-b}/(k+1)`$. Thus the sum of the $`k`$
copies of the logarithm-of-two error and the reduced-input error is at most
$`2^{-b}`$. For the returned value $`U`$,

```math
0\le U-\log x\le2^{-b}.
```

The numerical audit does not reproduce this logarithm routine as its oracle.
It proves, with the separate exponential enclosures, that
$`\exp(U)\ge x`$ and $`\exp(U-2^{-b})\le x`$. Monotonicity of the
real exponential then establishes both sides. Inputs include values around
one and two, non-dyadic rationals and $`2^{200}`$.

The original public logarithm routine was directly decorated with
`lru_cache`. Python's equality between certain numeric types let a warmed
cache admit a floating input, Boolean input or floating precision without
running the intended validation. The
[negative reproduction](../development/independent_capital_review_v1/reproduce_cache_alias_v1.py)
and [failure result](../development/independent_capital_review_v1/cache_alias_reproduction.json)
preserve three examples. The returned numeric value was not an invalid
enclosure; the defect was a cache-dependent breach of the exact-input
contract. Version 1.1 validates and normalizes inputs in a public wrapper
before calling a private cached helper. The warmed-cache aliases and the
ordinary malformed inputs now all reject.

## 4. Capital certificate and search limits

Let $`K`$ denote the true old prior-weighted capital, with maintained bound
$`K\le C`$. If the old enclosure lower endpoint is $`L`$ and the two
new enclosure upper endpoints are $`U_0,U_1`$, the implementation records

```math
A=\max(0,U_0-L,U_1-L).
```

For either answer,

```math
K'_y\le U_y\le L+A\le K+A\le C+A.
```

This is an inductive certificate for every chosen forecast. Its validity
does not depend on establishing a sign bracket, finding a root, or meeting
the requested allowance. The search can therefore return its best evaluated
candidate after exhausting a numerical cap while retaining a valid larger
capital bound. A missing sign-bracket verification can matter for a promised
root-success theorem; this implementation makes no such universal promise.

Two preserved cases distinguish different reasons for a positive allowance:

| Case | Forecast | Retained allowance | Independent finding |
| --- | ---: | ---: | --- |
| Horizon $`10^{12}`$, fixed 16-bit enclosures | $`0`$ | $`1/1179648`$ | Both true outcome capitals strictly decrease; enclosure width prevents meeting the much smaller request |
| Zero bisection cap | $`1/2`$ | $`8007563/100663296`$ | One outcome genuinely increases capital, and the increase is covered |

Both cases report `allowance_met=False`. Hence the numerical budget must
remain conditional on achieving the requested allowances. The unconditional
finite certificate uses $`C_T=1+\sum_t A_t`$ and the actual reported
logarithmic correction $`\log(C_T/\pi)`$.

## 5. Update algebra and state integrity

Independent history reconstruction checks all three component families.
Expert logs equal their fixed rate times cumulative weighted Brier regret.
The positive and negative calibration logs equal the signed weighted tent
residual minus the quadratic-variation correction. Action logs use the
centered residual $`Z_i`$, not full mixed-action regret. The separately
verified transport is $`G_i\le Q+Z_i`$, so the audit's action bound adds
the retained smoothing slack $`Q`$.

Every tested counterfactual branch has enclosed capital below the maintained
bound plus the recorded allowance. A separate rational computation verifies
the capital supermartingale average on the nonzero-weight branches. The
zero-weight round preserves exact scores. Large common outcome-dependent
cost offsets leave forecast selection and capital logs identical and cancel
exactly from relative mixed-action regret.

The current public configuration, rates and priors are read-only properties;
their records and all returned predictions/history elements are immutable.
Mutable caller name lists, expert mappings and action-row lists do not alias
retained state. Audit dictionaries are detached. Invalid issue/reveal calls,
scope mismatches, noninteger binary aliases, duplicate settlements and the
announced horizon boundary leave the tested complete learner state unchanged.

These are finite development probes and an implementation proof review. They
do not turn the saved query population into a statistical generalization
experiment or certify a realized randomly sampled action loss as equal to
its scored mixture loss.
