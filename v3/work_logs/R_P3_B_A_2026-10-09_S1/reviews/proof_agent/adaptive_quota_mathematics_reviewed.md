# Adaptive exact-quota selector: independent derivation check

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Task: **R-P3-B-A**; same-model, nonblind review; **zero principal clock credit**.
This is a separate exploration within the selected recurrence. It changes no
stable core, planned experiment, status, ledger or later task. The parent supplied
the candidate theorem and the numerical witness before this review's probe.

**Finding:** the proposed bound is valid under the information contract below.
History-dependent sampling probabilities are permitted. The purchased
propensity must enter the update. A finite, exactly enumerated example refutes
the same claimed guarantee for an update that omits it.

## 1. Information and parameter contract

Fix an exogenous deterministic loss table `ell[t,i]` in `[0,1]`, `N>=2`, and
`T=mB` with `B>=2`. For the mathematical service, fixed stateless binary experts
and deterministic answers induce this table. Each purchased answer exposes the
expert-loss column and permits a zero-loss terminal action at that position.

At each block, the learner has its past transcript and **all public requests
and expert advice for the current block before selecting a position**. It has
no new unpurchased labels. Freeze the actual mixture `p_k` for the entire block.
Select a probability vector `pi_k` using this past and public block, with

```math
\sum_{t\in\mathcal B_k}\pi_{k,t}=1,\qquad
\pi_{k,t}\ge\frac1{H+1}>0.
```

Use one fixed `H` throughout and `K>=max(2,H)`. Feasibility implies `H>=B−1`.
Draw exactly one `J_k` from this vector with fresh selector randomness. On each
unbought position, the action has the frozen mixture's distribution, using
randomness independent of the selector conditional on the block state.
Update only after the block. The whole loss table is fixed independently of
these fresh random bits; it is not required to be IID.

The requirement to have the whole public block is an additional interface
relative to an input stream revealed only one request at a time. It requires
buffering or an explicitly granted lookahead window. That interface, and the
work to evaluate its advice, must also be available to ordinary controls.

## 2. Conditional identity and the comparator coefficient

Let `G_k` contain the past and the public block, after `p_k` and `pi_k` are
fixed and before the selector is drawn. Define

```math
X_{k,i}=\left(\frac1{\pi_{k,J_k}}-1\right)\ell_{J_k,i},
\qquad Z_{k,i}=X_{k,i}/H.
```

Then `0<=Z_{k,i}<=1`. Directly conditioning on `G_k` gives

```math
\begin{aligned}
\mathbb E[X_{k,i}\mid G_k]
 &=\sum_{t\in\mathcal B_k}(1-\pi_{k,t})\ell_{t,i},\\
\mathbb E[X_{k,i}^2\mid G_k]
 &=\sum_{t\in\mathcal B_k}\frac{(1-\pi_{k,t})^2}{\pi_{k,t}}\ell_{t,i}^2,\\
\mathbb E[L^{\rm ideal}_{{\rm terminal},k}\mid G_k]
 &=\mathbb E[\langle p_k,X_k\rangle\mid G_k].
\end{aligned}
```

The last identity includes zero purchased loss and all unbought positions.
It does not require `pi_k` to be independent of `p_k` or of the past. It does
require the same frozen mixture on those positions and the specified
conditional action randomization. These are evaluator-side identities for a
fixed table; they do not expose unpurchased columns as learner inputs.

Apply ordinary product weights to `Z` with `eta=1/K`:

```math
w_{k+1,i}=w_{k,i}(1-Z_{k,i}/K).
```

The standard pathwise inequality, multiplied by `H`, is

```math
\sum_k\langle p_k,X_k\rangle
\le\sum_kX_{k,i}+HK\ln N+\frac1{HK}\sum_kX_{k,i}^2.
```

Its source is Cesa-Bianchi, Mansour and Stoltz, *Improved second-order bounds
for prediction with expert advice*, Machine Learning 66 (2007),
[author-hosted paper](https://cesa-bianchi.di.unimi.it/Pubblicazioni/J28.pdf),
§3, printed pp. 327–328, Lemmas 1–2, with gains replaced by negative losses.
The conditional block identity and the following coefficient calculation
are this review's reconstruction, not a quoted source theorem.

Using `ell^2<=ell`, the coefficient of each comparator loss is at most

```math
c(\pi)=1-\pi+\frac{(1-\pi)^2}{HK\pi}\le1.
```

Indeed, `c(pi)<=1` is equivalent to
`(1/pi−1)^2<=HK`, and the probability floor gives
`(1/pi−1)^2<=H^2<=HK`. Taking expectations and then minimizing over the
**deterministic** comparator totals therefore gives

```math
\mathbb E L^{\rm ideal}_{\rm terminal}
\le L_*+HK\ln N,
\qquad L_*:=\min_i\sum_t\ell_{t,i}.
```

This comparator receives no purchased correction. If the comparator receives
the same correction at `J_k`, its expected loss is the first term of the
conditional comparator identity; the nonnegative second-order term remains.
The displayed result does not establish the same constant regret against
that stronger comparator.

### Fixed versus random hindsight

For the selected deterministic tape, moving the final minimum outside
expectation is harmless. For adaptive between-block loss tables that are
fixed only before their respective selectors, this fixed-expert argument
would yield `E L_terminal <= min_i E L_i + HK ln N`; it would not by itself
yield `E[L_terminal−min_i L_i] <= HK ln N`.

An exogenous random tape independent of all learner random bits is different:
one could condition on that entire tape, apply the deterministic-tape theorem,
then average. That extra argument can retain random-hindsight regret in that
more specific model. No such stochastic extension is needed for this task,
and random tapes coupled to learner history cannot be covered by silently
using this conditioning argument.

## 3. Fixed mass, finite actions and exact tickets

Let `delta=2^(−s)`. The fixed-mass rounding scheme is sufficient whenever the
next normalized weights satisfy

```math
p_{k+1,i}\ge(1-\delta)
\frac{p_{k,i}(1-Z_{k,i}/K)}{1-\langle p_k,Z_k\rangle/K}.
```

Following any fixed expert through the usual logarithmic potential adds at
most `m log(1/(1−delta))` before multiplying by `HK`. This remains valid when
the next selector depends on these rounded weights. The resulting allowance is

```math
HKm\ln\frac1{1-2^{-s}}
\le\frac{HKm}{2^s-1}.
```

The bound conservatively counts an update after every block, including the
last. Dyadic rounding of the binary action probability changes expected loss
by at most `2^(−h)` on each unbought position. There are exactly `T−m` such
positions, so the additional action allowance is `(T−m)2^(−h)`.

For `B` a power of two, give one ticket to every position and `B` additional
tickets to a public-information favorite `f_k`. Draw one uniform integer
from `0,...,2B−1`. This consumes exactly `log2(2B)` fair bits and gives

```math
\pi_{k,f_k}=\frac{B+1}{2B},\qquad
\pi_{k,t}=\frac1{2B}\ (t\ne f_k),\qquad H=2B-1.
```

The expert-loss multiplier must be `1−gamma_J ell[J,i]`, where

```math
\gamma_J=\frac{1/\pi_J-1}{HK}
=\begin{cases}
\dfrac{B-1}{(B+1)HK},&J=f_k,\\
1/K,&J\ne f_k.
\end{cases}
```

For integer `H,K`, a common exact denominator is `D=(B+1)HK`.
Multiplying each weight by `D−(B−1)ell[J,i]` at a favored purchase, or by
`D−(B+1)H ell[J,i]` otherwise, implements the update for binary losses.
Integer intermediates and their arithmetic cost need a new declared bound;
they are not the stable core's old `K−ell` update. Exact weights are at most
`D^m`; fixed-mass pre-rounding sums are at most `MD`, and the rounding
numerators `(M−N)v_i` are at most `M^2 D`.

Uniform `pi=1/B`, `H=B−1` gives `gamma=1/K` and recovers the core. Nonuniform
selection increases the required `H`: it can help actual fees or useful label
placement, but this worst-case learning allowance does not prove an advantage
over uniform selection.

## 4. Mathematical fees and the closest adaptive ordinary method

If `c_{k,t}` is the actual potential invoice for position `t`, determined
before the draw from the current service state, then

```math
\mathbb E\sum_k c_{k,J_k}
=\mathbb E\sum_k\sum_{t\in\mathcal B_k}\pi_{k,t}c_{k,t}.
```

The same identity applies to known fixed request prices. A public quote or
proxy used to choose the favorite is not automatically the actual invoice.
With service randomness or selector-dependent costs, use the actual
conditional invoice `E[C_k | G_k,J_k=t]` instead. Costs of obtaining all public
block advice, evaluating disagreement/cost scores, buffering, sampling,
updating, checking and setup remain part of the bill. Running every exact
service to discover its cost would itself incur the work of those runs.

For fixed public prices, the ticket policy's block fee is
`(sum_t c_t+B c_f)/(2B)`: half the uniform mean plus half the favored price.
Choosing the cheapest position lowers this fee term, but may increase actual
task loss, and increases the worst-case allowance through `H`. Selection by
disagreement also needs an actual cost comparison before being called useful.
The full bound adds expected actual query/controller/setup costs to the
task-loss and approximation allowances; a query-count cap is not a monetary cap.

The closest inspected adaptive expert source is Castro, Hellström and van
Erven, *Adaptive Selective Sampling for Online Prediction with Experts*,
NeurIPS 2023, [published PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/00b67df24009747e8bbed4c2c6f9c825-Paper-Conference.pdf),
§2, pp. 2–3; §4, Theorem 2 and Lemma 2, pp. 5–6; §5. It uses current weighted
expert disagreement to choose a Bernoulli label-query probability, and updates
with importance-weighted losses `ell_i,t Z_t/q_t`. Its sufficient rule is
`q_t=min{4A_t(1−A_t)+eta/3,1}`. The displayed expected-regret bound is
`ln N/eta+n eta/8`; reduced expected label complexity additionally uses a
conditional positive-gap premise. The prediction incurs its loss even when
the label is purchased. This is not an exact one-per-block quota or a
purchase-corrected terminal-action theorem, and it does not price mathematical
implementation. Its proof has not been imported to supply our block bridge.

The present selector is an ordinary importance-weighting adaptation, not a
novelty claim. A matched ordinary control can use the same public lookahead,
disagreement, fees, exact quota, propensity update and current-answer
correction. Source methods with different information or correction services
should be labeled as scoped comparisons.

## 5. Finite witness against ignoring propensity

The parent proposed this candidate; it was recorded **before probing** in
`adaptive_propensity_witness_target_v1.json`. Parameters are `B=4`, `m=64`,
`H=K=7`, two constant experts `0,1`, repeated labels `(0,1,1,1)`, and
`pi=(5/8,1/8,1/8,1/8)`. The best full-tape expert is constant 1, with loss 64.

Already on one block,

```math
\mathbb E[\ell_{J,\cdot}]=(3/8,5/8),\qquad
\mathbb E[X_{\cdot}]=(21/8,3/8).
```

Ignoring propensity learns toward the expert favored by the purchased-label
distribution, which is opposite to the expert preferred by the unbought
terminal-loss target.

Before block `k+1`, the number `z` of purchased zeros has distribution
`Binomial(k,5/8)`. With the naive multiplier `6/7` for every purchased loss,
the action-zero probability is

```math
a^{\rm naive}_{k,z}
=\frac{7^z6^{k-z}}{7^z6^{k-z}+7^{k-z}6^z}.
```

With the correct multipliers `242/245` after a purchased zero and `6/7`
after a purchased one, it is

```math
a^{\rm aware}_{k,z}
=\frac{245^z210^{k-z}}{245^z210^{k-z}+245^{k-z}242^z}.
```

For either variant, conditional expected terminal block loss is
`3/8+(9/4)a`. The calculator sums this expression exactly over the binomial
statistic and then all 64 blocks. No Monte Carlo, service calls or hindsight
parameter search are used.

| Update | Exact rational expectation enclosed by these decimals: regret to full-tape best expert |
| --- | --- |
| Naive, ignores propensity | `[64.261798460036, 64.261798460037]` |
| Propensity-aware | `[−9.165533525572, −9.165533525571]` |

The naive result strictly exceeds the proposed `49 ln 2` allowance:
`ln 2<7/10`, since the first four nonnegative terms of `exp(7/10)` already
sum to `12013/6000>2`; hence `49 ln 2<34.3`. The correct update's negative
regret is consistent with purchased correction. This one example does not
substitute for its theorem proof.

The exact algorithm, target and digest-bound results are
`check_adaptive_propensity_witness.py`, `adaptive_propensity_witness_target_v1.json`
and `adaptive_propensity_witness_result_v1.json`. The result file stores rigorous
rational decimal enclosures and digests of the full exact fractions. Re-running
the calculator checks the existing result without overwriting it.

This is an algebraic failure witness, not evidence that a repeated mathematical
query family beats cheap analytic or cached exact controls. No service-price
claim is attached to it.
