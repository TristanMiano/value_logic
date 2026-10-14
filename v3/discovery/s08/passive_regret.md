# Compulsory calibration changes the exploration question

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
New derivation; not a novelty or complete-cost superiority claim.
This examines the repeated-request consequence of the compulsory-pair lemma,
separately from a finite confidence-set experiment.

For every nontrivial path request, conditional on all prior requests and the
predictable first query, the first indicator is middle with probability 1/2.
When it is middle, the next adjacent compulsory query repeats with probability
rho. Thus eligible arrivals and their repeat bits have the same joint law on
each fresh row, irrespective of which prepared interval policy is selected.
They supply passive statistical feedback at an action-independent rate.
They are not physically free requests: all service and compulsory audit costs
remain. The incremental physical cost of **using this particular statistic**
is zero. Its computation and storage cost are not zero.

## Greedy statistical use need not buy exploratory actions

Let a fixed finite bank have continuous expected physical fees V_pi(rho),
and choose at request t a minimizing bank policy at the empirical repeat
fraction from eligible pairs in requests before t. Use any fixed estimate
when no sample has arrived. Every chosen policy still produces an exact
receipt-based action certificate.

Fix the true rho and one minimizing policy pi*. For a nonoptimal policy pi,
write its positive gap as Delta_pi=V_pi(rho)-V_pi*(rho). Let L_pi be a valid
Lipschitz constant of V_pi-V_pi* on [0,1]. For a degree-d Bernstein difference
with coefficients c_s, one valid constant is

```math
L_\pi=d\max_{0\le s<d}|c_{s+1}-c_s|.
```

If L_pi=0 and Delta_pi>0, pi can never minimize at another parameter.
Otherwise selection of pi implies an estimation error of at least
gamma_pi=Delta_pi/L_pi; if gamma_pi>1, selection is impossible. Conditional
on N prior eligible pairs, Hoeffding bounds that event by
2 exp(-2 N gamma_pi^2), including the vacuous N=0 bound of two.
Because N is Binomial(t-1,1/2), averaging gives

```math
\Pr(\pi_t=\pi)\le
2\left(\frac{1+e^{-2\gamma_\pi^2}}2\right)^{t-1}.
```

Summing expected physical-fee regret over any horizon therefore gives the
finite, gap-dependent bound

```math
\mathbb E\sum_{t=1}^T[V_{\pi_t}(\rho)-V_{\pi^*}(\rho)]
\le\sum_{\pi:\Delta_\pi>0}
\frac{2\Delta_\pi}{1-(1+e^{-2\gamma_\pi^2})/2}.
```

The argument tolerates ties: policies tied at the true parameter contribute
zero, and only strictly suboptimal policies enter the sum. The constants can
be huge near a crossing. It is a pointwise bound for a fixed finite bank,
not a uniform fast-rate claim or a global optimal-policy result.

This is the familiar advantage of informative passive feedback over bandit
feedback, instantiated by a logical action duty. It does not prove a new
general learning principle. The useful structural obligation is to show that
feedback remains informative under **every deployed policy**, without adding
queries solely for exploration or accidentally using selection-biased pairs.

## The computation bill prevents an automatic full-cost conclusion

Updating counts and choosing a policy every request costs additional work.
Even bounded cumulative physical-fee regret can coexist with linearly growing
additional computation relative to a prepared oracle. A permanent finite-data
commitment is a different tradeoff: with noisy overlapping source laws it has
a positive chance of choosing the wrong policy, which can cause linear future
fee regret on an unbounded horizon. An all-time confidence guarantee bounds
that chance; it does not turn it into zero.

One prospective repair is sparse statistical maintenance. At deterministic
service epochs of length 2^k, obtain only enough compulsory-pair samples to
reach a cumulative target on the order of k^2, then ignore later eligible
samples until the next epoch. A predictable decision to retain a pair, made
before its repeat bit is revealed, preserves the Bernoulli law. Eventually,
for any fixed positive decision gap, the epoch length grows slower than the
inverse error probability: 2^k exp(-constant*k^2) is summable. This suggests
finite physical-fee regret with only polylogarithmically many statistical
updates, but the arrival delay, selection timing, source admission, bit costs
and numerical policy comparisons still need a complete derivation. It is
not yet an implemented or verified theorem. Horizon-dependent targets could
be much sharper when a supported decision margin is available.

The next question is whether a checked decision region can schedule useful
future maintenance under an explicit horizon or workload contract. Do not
charge every mandatory receipt to learning, or omit the maintenance schedule
from the comparison. Ordinary passive-learning and parametric-verification
controllers receive the same receipts and source assumptions.
