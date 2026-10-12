# Random audit order without a prior on costs

**DEVELOPMENT — ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC.**

This extends the conditional [homogeneous quotient family](quotient_closed_form.md).
It prices one randomized observation policy. It does not learn a source law,
prove randomized-policy optimality, or establish a full-cost advantage. The
source and logical premises still need their own paid admission.

## Fixed source, internal randomization

Let N remaining mandatory rows have M fixed high values and N minus M fixed
low values. Their locations are unknown but fixed independently of the
algorithm's random choices. Audit a uniform random permutation until R highs
or L lows appear. Buy the decision-bit audit only at the low-threshold repair
leaf. Assume positive thresholds with $`K=R+L-1\leq N`$, constant mandatory
audit tariff A and decision tariff D. All stopping conditions and returned
actions are checked on every realized path.

After k observations, the policy is still running exactly when the number h
of highs is below R and the number of lows is below L. Its expected mandatory
audit count is therefore a sum of hypergeometric survival probabilities:

```math
\mathbb E_M T=
\sum_{k=0}^{K-1}
\sum_{h=\max(0,k-L+1)}^{\min(k,R-1)}
\frac{\binom Mh\binom{N-M}{k-h}}{\binom Nk}.
```

Conceptually finish the permutation after the actual policy stops. At index K,
exactly one stopping threshold has been reached, so the probability of a
repair leaf is:

```math
P_M=
\sum_{h=0}^{R-1}
\frac{\binom Mh\binom{N-M}{K-h}}{\binom NK}.
```

Use zero for binomial coefficients outside their usual nonnegative index
range. Thus the policy's source-uniform expected observation quote is:

```math
J_{\mathrm{expected}}
=\max_{0\leq M\leq N}\{A\mathbb E_M T+DP_M\}.
```

This maximizes over fixed source configurations. The expectation is solely
over a specified internal random permutation; there is no prior on M or row
values. Every path still has the [proved realized cap](quotient_closed_form.md)
KA plus D. An adversary that assigns values after observing the random order
does not satisfy this fixed-source contract.

## A smaller exact maximization

If M is less than R, replacement cannot occur. The expected position of the
Lth low in a random permutation gives:

```math
P_M=1,\qquad \mathbb E_M T=\frac{L(N+1)}{N-M+1}.
```

This bill increases with M. If M exceeds N minus L, repair cannot occur:

```math
P_M=0,\qquad \mathbb E_M T=\frac{R(N+1)}{M+1},
```

which decreases with M. Only the counts from R minus one through N minus L
plus one need maximization: N minus K plus two counts. In particular, when
K equals N, the exact worst expected observation tariff of this policy is:

```math
\max\left\{
A\frac{L(N+1)}{L+1}+D,
A\frac{R(N+1)}{R+1}
\right\}.
```

The stopping-distribution calculation offers another exact evaluation. A
repair stop after L lows and h highs has probability:

```math
\rho_h=
\frac{\binom{L+h-1}{h}\binom{N-L-h}{M-h}}{\binom NM},
\qquad 0\leq h<R.
```

A replacement stop after R highs and j lows has probability:

```math
\sigma_j=
\frac{\binom{R+j-1}{j}\binom{N-R-j}{M-R}}{\binom NM},
\qquad 0\leq j<L.
```

Summing $`[A(L+h)+D]\rho_h`$ and $`A(R+j)\sigma_j`$ gives the same
expected bill with K terms per candidate count. Binomial arithmetic and
coefficient bit lengths still cost resources. The saved implementation
computes both formulas as a check; it is not an optimized acquisition service.

## Executed arithmetic evidence

[Source](random_order.py) and [raw results](random_order_results.json) preserve
546 exact comparisons against enumeration of all high-location sets for
N from one through seven and all legal positive thresholds and high counts.
The independent stopping-distribution formula agrees too. These are
conditional arithmetic checks with **zero new acquisitions**.

| N | R, L | Worst realized observation tariff | Worst expected tariff of this policy | High counts searched after reduction |
|---:|---|---:|---:|---:|
| 3 | 2, 2 | 4 | 11/3 | 2 |
| 127 | 64, 64 | 128 | 8257/65, approximately 127.031 | 2 |
| 128 | 64, 64 | 128 | 16449/130, approximately 126.531 | 3 |

All prices in the table are A equals D equals one. The modest gains in the
larger examples can readily be consumed by extra quote construction, random
order generation, checking or retention. None of those fees is declared zero.
Uniform random order is equally available to an ordinary threshold controller.
Unequal prices, correlated sources and additional sensors require a new quote.
Continuing past a valid repair threshold might sometimes reduce expected
decision-audit expense, so earliest stopping is not asserted to be optimal
for the expected-cost objective. This observation does not change the exact
worst-realized-tariff theorem or the current F01 forecast event.
