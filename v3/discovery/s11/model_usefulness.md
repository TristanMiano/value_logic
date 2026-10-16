# Learning which fallible baseline is useful

Codex (GPT-6), DEVELOPMENT derivation. This extends
[prediction baselines](prediction_baseline.md); it does not assert a new
general control-variate or optimistic-learning principle.

Keep each request's matching distribution P=(1-gamma)Q+gamma U fixed before
current unknown values. For edge j use its singleton/edge probabilities s_j,e_j,
weighted-learner edge marginal e_j^Q, and the original a_j,d_j notation.
Baseline forecasts b_j in [0,c_max] are fixed from past information/public
context before sampling. The same b_j must apply under both orientations.
Do not fit a baseline using the current orientation and then treat it as fixed.

## An observable score for useful prediction

Let I_j^s indicate that execution reaches reference prefix R_j and samples
singleton j; let I_j^e indicate that it reaches R_j and samples edge (j,j+1).
Only the corresponding a_j or d_j is needed, and it is observed after the
first query in that block whether or not the checker stops. Define

```math
\widehat V(b)=\sum_j e_j^Q\left[
 I_j^s\frac{(a_j-b_j)^2}{s_j^2}
 +I_j^e\frac{(d_j-b_j)^2}{e_j^2}\right].
```

Conditioning on past history and the current fixed original world gives

```math
\mathbb E[\widehat V(b)]
=\sum_j e_j^Q\mathbf1\{\neg\mathrm{Stop}(R_j)\}
\left[\frac{(a_j-b_j)^2}{s_j}+\frac{(d_j-b_j)^2}{e_j}\right]
=:V(b).
```

Thus the variance-relevant score can itself be estimated without buying
counterfactual labels. A received score is noisy; it is not a deterministic
certificate that a model's predictions are correct or that a future request
will benefit. Every model can be scored on the SAME executed receipts.

Suppose M forecasters collectively use a fixed union of at most K active
baseline edges per request, with zero predictions elsewhere. Zero-baseline
terms outside that union are nonzero at at most one realized stopping event.
Hence each observed score lies in [0,B], where
B=25*(K+1)*c_max^2/gamma^2 is a conservative bound. Model computation,
retention and score evaluation are additional costs, not free observations.

Apply ordinary exponential weights to the M observed scores with rate lambda,
and predict the convex mixture of their baseline vectors before the request.
Squared error is convex, so its observed score is at most the weighted average
of model scores. Hoeffding's bounded-loss argument and conditional unbiasedness
give, for every FIXED comparator model k,

```math
\mathbb E\sum_{t=1}^T V_t(b_t)
\le \mathbb E\sum_{t=1}^T V_t(b_t^k)
 +\frac{\log M}{\lambda}+\frac{\lambda T B^2}{8}.
```

The comparator is evaluated under the same realized sequence of sampling
distributions Q_t/P_t. This is not a comparison with the different trajectory
that would result from running model k's entire controller from scratch.
The minimum over fixed k can be taken OUTSIDE the expectation. A hindsight
choice depending on the random trajectory needs an additional uniform bound;
do not silently move that minimum inside the expectation. Include the zero
baseline among the forecasters, but do not mistake this variance-score bound
for a no-harm guarantee on complete monetary cost.

## How prediction error enters execution regret

Write d=K+1, A=log N for N matchings, and

```math
E=\sum_{t,j} e_{tj}^Q\mathbf1\{\neg\mathrm{Stop}(R_{tj})\}
 (b_{tj}-b_{tj}^*)^2,
\qquad b_{tj}^*=\frac{e_{tj}a_{tj}+s_{tj}d_{tj}}{s_{tj}+e_{tj}}.
```

For adaptive past-dependent predictions, replace E by its expectation in the
bound below. At most three true local differences are nonzero, each bounded
by c_max. Using e^Q/(s+e)<=1/(1-gamma), s>=gamma/3 and e>=gamma/5, the previous
second-moment bound becomes, for 0<gamma<=1/2 and eta<=gamma/(5*d*c_max),

```math
\mathbb E\mathrm{Regret}_T
\le \frac A\eta
 +\eta\left(6d c_{\max}^2T+\frac{8d\mathbb E E}{\gamma}\right)
 +2\gamma c_{\max}T.
```

This is a direct ordinary exponential-weights consequence, not a new general
regret rate. It isolates the forecast error that actually matters to this
stopping-cost task. The ideal baseline is a diagnostic using both potential
outcomes; it is not a deployable oracle without further evidence.

For the special conditional claim E=0, choose
eta=sqrt(A)/(4*c_max*sqrt(d*T)) and gamma=5*sqrt(d*A)/(4*sqrt(T)), provided
gamma<=1/2. The displayed bound is then at most
8*c_max*sqrt(d*A*T). Bad baselines retain unbiasedness but can destroy that
rate; the estimator alone does not automatically adapt to an unknown E.
The observable model-score mechanism is a route to selection, with its own
often loose gamma-dependent overhead. No inexpensive end-to-end adaptive
rate or service advantage is yet established.

## Cheap screen and prior art

Before any service extension, check exact finite expectation, second-moment
decomposition, model-score expectation and convexity on the existing four
small ff01 fixtures, with baselines zero, half the maximum fee, maximum fee,
and the nondeployable optimal diagnostic. Include a deliberately
orientation-dependent baseline to show the bias failure. Preserve all
outcomes; this is mathematical development on exposed fixtures.

bp01 completes all four declared cases on their first attempts. The saved
outputs retain the exact score sums for all four baselines, including adverse
fixed predictions, and the orientation-dependent bias counterexample. No
learned model or service benchmark was run. Executed baseline_probe.py and
its dependency hashes are recorded in each result; preserve those bytes.

[Rakhlin and Sridharan (2013)](https://proceedings.mlr.press/v30/Rakhlin13.html)
already studies predictable processes and selection among models under
different feedback contracts. Its abstract/introduction supports that broad
comparison; exact theorem import requires further reading. Here the proposed
adapter is the observable sparse stopping-cost score and its explicit purchase
boundary. [Greensmith, Bartlett and Baxter (2004)](https://jmlr.org/papers/volume5/greensmith04a/greensmith04a.pdf)
already identifies weighted baseline error as excess variance (Theorem 16).
Several fallible models helping is not unique to Value Logic: this construction
uses conventional machinery to pursue the program's value/cost-centered goal.
