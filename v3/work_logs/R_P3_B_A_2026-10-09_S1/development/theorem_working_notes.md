# Selective feedback: prospective working derivation

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
Stage: DEVELOPMENT; this record precedes new implementation experiments.

## Contract and intended ordinary import

There are T=mB fixed mathematical requests. Their correct answers and the
losses of N stateless binary experts are fixed independently of the learner's
randomness. One request J in each equal block is uniformly purchased. The
expert mixture is frozen for that entire block. A checked label may correct
the terminal decision on J, but cannot alter an already issued forecast.

The first proof target uses product weights with learning rate eta=1/K,
K=max(2,B-1). With binary expert losses the common denominator cancels: each
integer weight is multiplied by K or K-1. This avoids exact-real arithmetic.
The primary source under examination is Cesa-Bianchi, Mansour and Stoltz
(2007), section 3, Lemmas 1–2. Its product-weights inequality specializes to

```math
\sum_{k=1}^m p_k\cdot x_k
\le \sum_{k=1}^m x_{k,i}
 +\frac{\log N}{\eta}
 +\eta\sum_{k=1}^m x_{k,i}^2.
```

Here x is the expert-loss row at the purchased request, rather than an
importance-weighted loss estimate at each original round. Each block is one
ordinary full-information meta-round. This is an ordinary adaptation, with
source attribution to be checked directly by the principal.

## Block bridge to be reconstructed

Conditional on earlier blocks, uniform J and frozen p give

```math
\mathbb E\left[\sum_{t\ne J}p_k\cdot\ell_t\right]
=(B-1)\mathbb E[p_k\cdot\ell_J],
\qquad
\mathbb E\sum_k\ell_{J_k,i}=L_i/B.
```

For binary losses x squared equals x. Consequently the candidate terminal
decision bound is

```math
\mathbb E L_{\rm terminal}
\le (1-B^{-1})(1+\eta)L_i
 +(B-1)\log N/\eta.
```

For B>=3, eta=1/(B-1) cancels the coefficient in regret to a fixed expert:
the upper bound becomes L_i+(B-1)^2 log N. For B=2 the admitted eta=1/2
gives a sharper negative comparator coefficient and regret at most 2 log N.
B=1 is always-buy and should be handled explicitly. The source check found
Russo et al., NeurIPS 2024, studying purchased current best-action advice;
therefore the action-correction capability is not a novelty claim.

For a finite binary sampler, round the ideal action-one mass down to h bits.
At each unbought request the expected decision-loss change is at most 2^-h.
This suggests adding (T-m)2^-h, subject to independent reconstruction.
One uniform selector needs exactly log2(B) fair bits when B is a power of two.
The deterministic seeded development trace does not certify independence;
the probability theorem is a distinct randomized-service contract.

## Costs, comparators and boundaries

Fixed per-query checked resource cost c_t gives expected purchase cost
sum_t c_t/B. Actual cost on each trace is the sum at its selected positions;
the exact m-call cap is not a bound on all computation. Add setup, controller,
randomness, storage and output costs explicitly. A cap must fund m times the
admitted completion bound plus the controller bound before opening service.

The existing finite public modular family has cheap ordinary structure.
Include direct fast exact actions and a paid quadratic-residue table, as well
as checked always-BUY and an ordinary semantic cache. A direct action need not
buy an independent checking receipt merely to match the learner's provider.
Any unfavorable cost result is a scoped implementation/application result,
not a lower bound on every selective learner.

Outstanding proof duties include the exact integer bit bound, the emitted
forecast's separate all-issued score, fixed versus adaptive comparator
quantifiers, and concrete failures of updating within a block or choosing
later requests after observing the current block's purchase history.
