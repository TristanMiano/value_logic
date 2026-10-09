# Bounded-state extension and decision-policy boundary

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
Stage: DEVELOPMENT; prospective stronger construction before learner runs.
This extends contract_v1 within the same paid-feedback service. Exact product
weights remain a named control. No earlier exposure is relabeled as final.

## 1. Why consider fixed state?

Exact integer product weights can grow linearly in the number of purchased
labels. A negative cost result caused only by that avoidable representation
would be weak evidence about selective feedback. The following positive-integer
rounding rule trades a controlled regret term for state bounded independently
of the horizon. It is an ordinary numerical adaptation, not a novelty claim.

Let N be the number of experts, s>=1 a fixed precision, M=N*2^s, K>=2,
and eta=1/K. Initialize each weight to 2^s, so their sum is exactly M and
the initial distribution is exactly uniform even when N is not a power of two.
At the end of a block, given the purchased binary loss row x, form

```math
v_i=w_i(K-x_i),\qquad V=\sum_i v_i,
\qquad r_i=1+\left\lfloor\frac{(M-N)v_i}{V}\right\rfloor.
```

The residual R=M-sum_i r_i is an integer in [0,N-1]. Add one to the first R
weights according to the fixed expert order. The new weights are positive,
sum to M, and obey

```math
p_{k+1,i}\ge(1-2^{-s})\frac{p_{k,i}(1-\eta x_{k,i})}
                                  {1-\eta p_k\cdot x_k}.
```

The lower bound is componentwise. The extra fixed-index redistribution can
only increase a component relative to its floor-plus-one lower bound. It is
not described as unbiased rounding. Every arithmetic and retained word is paid.

## 2. Potential calculation

Write alpha=2^-s. Iterating the logarithm of the componentwise bound and using
p_{m+1,i}<=1 and p_{1,i}=1/N gives

```math
\eta\sum_k p_k\cdot x_k
\le \log N-\sum_k\log(1-\eta x_{k,i})
                     -m\log(1-\alpha).
```

The two scalar inequalities used are -log(1-z)>=z for 0<=z<1 and
-log(1-z)<=z+z^2 for 0<=z<=1/2. Thus

```math
\sum_k p_k\cdot x_k
\le\sum_k x_{k,i}+\eta\sum_k x_{k,i}^2
       +\frac{\log N+m\log(1/(1-\alpha))}{\eta}.
```

For the fixed-tape, one-purchase-per-block service, the same conditional
averaging bridge applies because the rounded weights also stay frozen inside
the block. Compared with exact product weights, the additional terminal-loss
allowance is

```math
\Delta_{\rm state}
 =(B-1)mK\log\frac1{1-2^{-s}}
 \le\frac{(B-1)mK}{2^s-1}.
```

The last expression is an exact rational upper bound. Binary action rounding
still adds (T-m)2^-h, independently of this state-rounding term. The pre-issued
Brier bound instead scales sampled-loss allowances by B, and its emitted
dyadic forecast needs a separate 2T*2^-h allowance.

Individual weights are at most M, requiring at most
s+ceil(log2 N)+1 bits. Updated products v_i are at most MK; the normalization
numerators are at most M^2 K. Prediction numerators are at most M*2^h.
These explicit intermediate bounds must enter the resource envelope: bounding
only retained weights does not bound the normalization computation. The fixed
bit-tape sampler has its own maximum 95-bit intermediate at a word crossing.

Initial planned development setting: s=16, h=16. All variants use the same
four fixed public experts and same purchase selectors for a given B/seed.
Retain exact-state results as a comparison. Choosing a later precision would
require a saved development amendment, not an invisible retuning.

## 3. Greedy optimization is a different action policy

The randomized prediction theorem does not license replacing its sampled
action by the deterministic argmin of the forecast's two estimated losses.
There is a concrete exogenous counterexample, even with perfect purchased
labels and all assumptions about blocks retained.

Use the two constant experts, B=4, K=3, and eight blocks. Every label in a
block is the same; the block labels alternate 1,0,1,0,1,0,1,0. With a tie
resolved as action 0, greedy prediction is wrong on every unpurchased round:
equal weights predict 0 before a label-1 block; weights in ratio 2:3 then
predict 1 before a label-0 block; the pair restores equal weights. Therefore
terminal loss is 8*(4-1)=24. The best fixed expert loses 16, so regret is 8,
exceeding the randomized bound 9*log(2), about 6.239 (before any bit allowance).

This tape can use two real queries from the same public modular service:
p=17,a=1 for label 1 and p=17,a=3 for label 0. The latter's residue is 16;
that fact will be privately verified in the finite check rather than passed
to the learner. Uniform purchase positions do not change the example because
all requests inside a block have the same answer.

For the ideal randomized two-expert policy the expected terminal loss per
two-block pair is 3*(1/2+3/5)=33/10, hence 66/5 over eight blocks. This is a
load-bearing P3-08 integration boundary: preserve the proved stochastic policy
or establish a new theorem for a greedy value optimizer. Knowing how to encode
a forecast in a valuation does not preserve every policy's regret guarantee.
