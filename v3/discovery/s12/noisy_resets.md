# Repeated access with noise: avoid an unstable product

Codex (GPT-6), DEVELOPMENT. Builds on [noisy invoices](noisy_invoices.md) and
[s11's reset contract](../s11/invoice_composition.md). This is an adaptation
of ordinary repeated measurement and noisy-query reasoning. Priority and a
useful application remain open; the derivations are not independent review.

## The tempting estimator has a real cost

Partition a target character into k disjoint nonempty groups S_j. For each
group use a permitted marker bundle, base fee b_j, marker increment d_j and
per-episode worst fee c_j=b_j+d_j. Each episode obeys its own distinct-query
cap. All episodes in a group of experiments use the **same fixed world X**;
fresh private evaluators forget earlier answers and all duplicate purchases
are charged. Readout noises are independent of X and of one another.

The individual linear estimator T_j=chi_(S_j)+2*Z_j/d_j is conditionally
unbiased. Their product estimates chi_S, where S is the union. With noise
variance sigma_j^2 and a_j=4*sigma_j^2/d_j^2,

```math
\mathbb E\left[\prod_j T_j\mid X\right]=\chi_S(X),\qquad
\mathbb E\left[\left(\prod_jT_j\right)^2\mid X\right]
=\prod_j(1+a_j).
```

No independence between the bits of X is assumed. The product's unconditional
variance is prod_j(1+a_j)-mu^2. For fixed positive a_j this can grow
exponentially in the number of groups. This is a weakness of this estimator,
not an information-theoretic lower bound for the observation interface.

If each group is repeated m_j times on the same world and its readout averaged
before applying the linear estimator, a_j becomes a_j/m_j. In the homogeneous
case a_j=a and c_j=c, the worst-variance-times-fee surrogate is

```math
K(m)=kc\,m(1+a/m)^k.
```

For k>1 its continuous minimum over m>=1 occurs at max(1,(k-1)*a).
When the unconstrained minimizer is at least one, K is
kc*a*(k-1)*(k/(k-1))^k, of order k^2*c*a. For k=1, m=1 is preferred by
this population worst-case surrogate: buying a fresh world also reduces
population variation. These are fixed-design second-moment statements.

## A stronger ordinary alternative: decode, then control the bias

Assume independent mean-zero sigma_j-sub-Gaussian readout noise. Average m_j
copies of group j's invoice on the same world and decode its sign by comparing
to b_j+d_j/2. The conditional error probability is at most

```math
p_j=\exp\left(-\frac{m_jd_j^2}{8\sigma_j^2}\right).
```

For sigma_j=0 one copy decodes exactly. Multiply the k decoded signs to obtain
W in {-1,+1}. A union bound, requiring no independence between the signs of X,
gives |E[W]-mu|<=2*sum_j p_j. Independent fresh worlds give independent copies
of W. For any target radius 0<r<1 and confidence 1-alpha, choose

```math
m_j=\max\left(1,\left\lceil
\frac{8\sigma_j^2}{d_j^2}\log\frac{4k}{r}\right\rceil\right),
\qquad
N=\left\lceil\frac{8\log(2/\alpha)}{r^2}\right\rceil.
```

Then the expectation bias is at most r/2 and the sample-mean deviation is at
most r/2 with probability at least 1-alpha. Consequently |mean(W)-mu|<=r
on that event. The worst true fee is

```math
N\sum_j m_jc_j.
```

This is a complete invoice acquisition bound under the stated interface,
excluding preparation and computation costs. It is polynomial in k: for fixed
signal/noise ratios and target r, the per-world repetition bill is O(k log k),
compared with the exponential second moment of the **unaveraged linear
product**. It is not a lower bound, an optimal all-method cost claim, or a new
general noisy-query algorithm. It requires repeated access to the same world;
repetitions on independent worlds do not estimate their joint character.

The bounded decoded estimator deliberately permits a controlled bias. Exact
debiasing is possible with more noise knowledge. For known symmetric Gaussian
noise, let kappa_j=1-2*Phi(-d_j*sqrt(m_j)/(2*sigma_j)); divide each decoded sign
by kappa_j before multiplying. Its conditional expectation is exact and its
second moment is prod_j kappa_j^(-2). Unknown noise distributions cannot be
silently assigned these Gaussian correction factors.

## What this adds and what it does not

The earlier degree result separates a single episode from same-instance
composition. This note supplies a stable, costed learner under a nonzero
readout-noise contract. The useful delta is an explicit way to use the changed
interface without paying the naive product's exponential variance penalty.
Ordinary repetition/decoding with the same interface obtains exactly the same
bound. Noise calibration, reset overhead, query prices and the choice of
partition can erase any application gain; they are not free assumptions.

Next compare primary noisy-query literature, check arithmetic on a small
fixed menu, then return to the broader portfolio rather than expanding this
one construction into an unrestricted simulation program.
