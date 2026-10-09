# Independent acquisition-boundary derivation

## Scope and provenance

This is a same-model subagent review, not a cross-model review. The task prompt disclosed the candidate answer `n = 45`, cost `0.5 n`, horizon `H = 128`, and gross-benefit ceiling `0.05 H`. Consequently this is **not a blind review**. The derivation and initial exact calculation below were completed **before reading** `v3/checks/07_acquisition_boundary.py` or its saved results. Source comparison follows in a separate report. All activity is unmeasured and receives zero principal-time credit.

The experiment is precisely a fixed, predetermined number `n` of independent Bernoulli observations, with equally likely hypotheses `theta = 0.45` and `theta = 0.55`. Conclusions here do not establish a sample-cost lower bound for arbitrary adaptive or sequential experiments.

## Optimal fixed-sample accuracy

Let `K` be the number of successes. The likelihood ratio of the positive hypothesis to the negative hypothesis is

`L = (0.55/0.45)^K (0.45/0.55)^(n-K) = (11/9)^(2K-n)`.

With equal priors and symmetric zero-one loss, the Bayes-optimal rule selects the positive sign for `K > n/2`, the negative sign for `K < n/2`, and can break ties arbitrarily. A fair random tie-break makes the two conditional accuracies identical. The resulting average accuracy is

`A_n = P_{0.55}(K > n/2) + (1/2) P_{0.55}(K = n/2)`.

An exact rational expression, with the tie term included only for even `n`, is

`A_n = [2 sum_{k=floor(n/2)+1}^n C(n,k) 11^k 9^(n-k) + 1_{n even} C(n,n/2) 11^(n/2) 9^(n/2)] / (2 * 20^n)`.

For `m >= 1`, `A_(2m) = A_(2m-1)`. For `m >= 0`,

`A_(2m+1) - A_(2m) = (0.55 - 0.5) C(2m,m) (0.55 * 0.45)^m > 0`.

For the second identity, only a tie after `2m` observations can change the conditional correctness probability upon adding one observation: its value rises from `1/2` to `0.55`. For the plateau identity, the changes from the two central bins after `2m-1` observations cancel, since the relevant central probabilities have ratio `0.55/0.45`. These identities also establish monotonicity for every nonnegative integer `n`.

Exact integer arithmetic gives

| n | Optimal accuracy |
|---:|---:|
| 43 | 0.74576699993528800232173186960976531162933254758061113489020499401 |
| 44 | 0.74576699993528800232173186960976531162933254758061113489020499401 |
| 45 | 0.75056091835019342028805339998700102361472478271436338569969848322 |
| 46 | 0.75056091835019342028805339998700102361472478271436338569969848322 |

The comparisons with `3/4` use exact fractions, not these rounded decimal representations. Hence the smallest fixed sample count attaining accuracy at least `3/4` is **45**.

## Total variation and chi-square bound

For probability distributions `P,Q`, with `P` absolutely continuous with respect to `Q`, write `L = dP/dQ`. Then

`TV(P,Q) = (1/2) E_Q |L-1| <= (1/2) sqrt(E_Q[(L-1)^2]) = (1/2) sqrt(chi²(P||Q))`.

This is Cauchy-Schwarz applied to `|L-1|` and the constant function `1`, whose squared `L²(Q)` norm is one. Also `TV <= 1`.

For `P = Bernoulli(0.55)` and `Q = Bernoulli(0.45)`,

`chi²(P||Q) = (0.55-0.45)^2 / [0.45*(1-0.45)] = 4/99`.

For independent product measures, `L_n = product_i L_i`, and independence gives

`1 + chi²(P^n||Q^n) = E_{Q^n}[L_n²] = [E_Q(L²)]^n = (1+4/99)^n = (103/99)^n`.

Thus

`TV(P^n,Q^n) <= min(1, (1/2) sqrt((103/99)^n - 1))`.

With equal priors the optimal classification accuracy is `(1+TV)/2`, so accuracy at least `3/4` requires `TV >= 1/2`, which in turn requires `(103/99)^n >= 2`. Exact integer comparisons give a necessary condition **n >= 18**: the product chi-square is below one at `n = 17` and above one at `n = 18`. This bound is valid but loose. It does **not** establish the exact threshold `n = 45`; that threshold comes from the binomial calculation.

## Economics of the stipulated experiment

Given profiling cost `0.5 n`, the smallest fixed experiment attaining accuracy `3/4` costs `0.5 * 45 = 22.5`. The stipulated maximum exploitation gain over `H = 128` decisions is `0.05 * 128 = 6.4`, even if the sign becomes perfectly known. Therefore every qualifying fixed-`n` experiment has net gain at most `6.4 - 22.5 = -16.1` relative to the stated baseline.

Even the weaker chi-square necessary count `n >= 18` costs at least `9`, already exceeding `6.4`; it suffices for this economic exclusion. The exact threshold strengthens the sample-count statement.

If the exploitation rule receives the full `H` rounds and gains `0.05` per round when its sign is correct but loses `0.05` when its sign is wrong, its expected gross gain at accuracy `A_n` is `0.1 H (A_n-1/2)`. At `n = 45` this is approximately `3.20717975488247578`, below the universal gross ceiling `6.4`.

These statements concern this binary hypothesis pair, equal prior, IID observations, symmetric sign-identification objective, fixed sample count, observation charge, horizon, and gain baseline. They do not by themselves rule out all lower-accuracy fixed experiments, nor establish anything about expected sample size under arbitrary stopping rules or adaptive acquisition models. Separate arguments are needed for such extensions.
