# Independent block-sampling reconstruction

This is a same-model, nonblind derivation supplied by the literature reviewer
for the principal's reconciliation. It is not the project's final theorem and
reviews no implementation. The source of the multiplicative-weights inequality
is identified in [source_contracts.md](source_contracts.md), §2. The quota,
independence and decision bridges below are explicit additional steps.

## 1. Contract and the all-issued target

Let T=mB, with m≥1 and integer block length B≥1. A fixed table of expert losses
ℓ_{h,t}∈[0,1] covers N≥2 experts and all T issued rounds. It may be a deterministic
function of an externally fixed mathematical-query tape and fixed experts;
it does not depend on acquisition choices. There is no IID assumption on that
tape. Randomness is auxiliary algorithmic randomness.

Before block b, choose its mixture p_b from earlier purchased feedback. Keep
p_b and the expert loss table within that block independent of a fresh uniform
index J_b in its B positions. Purchase exactly that position. Delay learning
updates until the block ends. At unpurchased positions, use independent action
randomization with marginal p_b, or a realizable convex mixture with the stated
loss inequality. No unavailable label enters the learner.

One label per block gives exactly m purchases pathwise. This is a query-count
cap; variable fees still require a separate monetary bound. Exogenous mathematical
answers alone do not suffice if queries or within-block expert states change in
response to purchase choices. The loss-table independence condition is what the
proof uses.

Write r_t=min_h ℓ_{h,t} and d_{h,t}=ℓ_{h,t}−r_t. A purchased answer must make the
best action in this declared catalogue executable, with its task loss r_t.
A checked exact mathematical answer may enable an even better action; in that
case the decision bound becomes an inequality. The full loss vector needed for
an update must be computable from the single purchased answer and the public
expert predictions. This access is not valid for an arbitrary black-box loss
matrix merely because a best-action identifier is available.

## 2. Unbiased sampled block excess

Set z_{h,b}=d_{h,J_b} and update at block end by

```math
w_{h,b+1}=w_{h,b}(1-\eta z_{h,b}),\qquad 0<\eta\le 1/2.
```

Conditional on the information before the block,

```math
\mathbb E[z_{h,b}]=\frac1B\sum_{t\in b}d_{h,t},\qquad
\mathbb E[\langle p_b,z_b\rangle]
=\frac1B\sum_{t\in b}\langle p_b,d_t\rangle.
```

These are finite uniform-average identities. They do not treat the sampled
position as a random draw from a probability distribution over mathematical
truths. Let

```math
A=\mathbb E\sum_b\sum_{t\in b}\langle p_b,d_t\rangle,
\quad D_h=\sum_t d_{h,t},\quad D_h^{(2)}=\sum_t d_{h,t}^2.
```

Applying the source `prod` inequality to the realized sampled sequence, taking
expectations separately for each fixed h, and multiplying by B gives

```math
A\le D_h+\frac{B\ln N}{\eta}+\eta D_h^{(2)}
\le (1+\eta)D_h+\frac{B\ln N}{\eta}.
```

The comparator can be chosen as the best fixed expert on this deterministic
table. If the future expert rows instead depend on learner randomness, this
argument gives a minimum of expected fixed-expert bounds, not automatically an
expected random hindsight minimum or counterfactual policy regret.

## 3. Purchasing before acting can improve the bound

Let L_min=Σ_t r_t. Since the query index is uniform and the mixture is frozen
within its block, the expected excess task loss removed by correcting the
purchased action is exactly A/B. Thus

```math
\mathbb E[L_{\rm actual}]\le L_{\min}+(1-1/B)A.
```

For every fixed h, subtract L_h=L_min+D_h to obtain

```math
\mathbb E[L_{\rm actual}]-L_h
\le\left(\eta(1-1/B)-1/B\right)D_h
 +\frac{(B-1)\ln N}{\eta}.
```

For B≥3, the rational choice η=1/(B−1) cancels the D_h term and gives

```math
\mathbb E[L_{\rm actual}]-\min_hL_h\le (B-1)^2\ln N.
```

For B=2, η=1/2 yields a bound of 2 ln N with an additional nonpositive comparator
term. B=1 buys every answer. These are ordinary method consequences under this
interface. They are consistent with the improved large-query regime already
studied by the best-action-query literature; they establish no priority claim.

A looser but sometimes smaller allowance follows from D_h≤T and the uncorrected
bound: B ln N/η+ηT. The learning rate must be selected prospectively for the
chosen bound; choosing the best output retrospectively across different learners
would require another acquisition/selection contract.

With setup S, actual fee C=Σ_b c_{J_b}, and other resource bill O, add those terms:

```math
\mathbb E[J_T]\le\min_h L_h+(B-1)^2\ln N+S+\mathbb E[C+O]
\quad(B\ge3).
```

A fixed fee f gives C=fm. A known cap c_t≤c_max gives C≤mc_max. Neither form
counts arbitrary precision operations, exact random sampling, label verification
or expert evaluation as free. A deterministic seeded development trace verifies
that trace; it does not establish the auxiliary uniform-coin premise.

## 4. Two boundaries with finite witnesses

**Adaptive query tape.** For one two-position block, J is uniform in {1,2}.
Let the first loss be zero. Let the second loss be one if the first position was
purchased and zero otherwise. This environment uses only the earlier query
indicator, so it is nonanticipatory at the round level. Yet the sampled loss is
always zero, while the expected two-position loss total is 1/2. Therefore
B E[z]=0 differs from E[Σ_tℓ_t]=1/2. General round-wise adaptive adversaries
cannot be silently imported into the block proof.

**Within-block learning.** Let B=2 and both fixed outcome labels be zero, with
experts constantly predicting zero and one. Start with equal weights. Suppose
one uses the purchased label immediately and sets the future mixture to the
correct expert. If J=1, the issued losses are 1/2 then zero; if J=2, they are
1/2 then 1/2. The average all-issued forecast loss is 3/4. The sampled issued
forecast loss is always 1/2, so B E[z]=1. This example concerns the learner's
mixture loss, not the unchanged individual expert rows. Freezing the mixture
through the block is essential for the displayed mixture identity.

The second policy can perform better in a particular tape; the point is that
it is a different algorithm whose displayed unbiasedness proof is invalid.
Likewise, acquired-answer correction changes task loss but cannot retroactively
change a forecast already issued for forecasting evaluation.
