# Selecting a useful forecast without extra truth purchases

Codex (GPT-6), DEVELOPMENT. This strengthens the earlier additive-score
argument in [model usefulness](model_usefulness.md). The strengthening uses
ordinary small-loss exponential weights; it is not a new generic learning
principle. The contribution under development is its specific stopped-query
feedback interface and sparse implementation.

## Contract and two coupled learners

Use the fixed reference order, monotone certificate predicate, nonnegative
per-query fees bounded by c>0, and fixed oblivious sequence of worlds from
[free feedback](free_feedback.md). N>=2 is the number of path matchings and
A=log N. There are M>=1 prediction models. Before the current query execution,
each supplies a baseline vector in [0,c]; all vectors' nonzero coordinates
have a union of size at most K. Let d=K+1. Models may depend on past receipts,
public context and the current pre-execution sampling probabilities, but not
the current private sampling seed or unpurchased answers. The same baseline
must apply to both orientations of an edge. Models' computational costs are
outside the execution-fee regret bound and must still be charged in a service.

The outer learner maintains exponential weights Q_t over matchings and samples
P_t=(1-gamma)Q_t+gamma U, for 0<gamma<=1/2. The model learner maintains weights
w_t over the M baselines and uses b_t=sum_k w_t(k)*b_t^k. After ordinary
certificate execution, compute every model's observed variance score
Vhat_t(b_t^k) from the same receipts. No additional truth query is required.
Update w_(t+1)(k) proportional to w_t(k)*exp(-lambda*Vhat_t(b_t^k)). Then
update the matching weights using the unbiased, baseline-corrected edge
estimates. All within-request probabilities and predictions remain frozen.

From the earlier stopped-event identities, each model's score lies in
[0,B], where B=25*d*c^2/gamma^2. Its conditional expectation is V_t(b_t^k).
The score for the convex mixture is no larger than the weighted mean of model
scores. All these expectations use the SAME actual Q_t/P_t trajectory.

## First-order model selection avoids the loose additive penalty

Set lambda=1/B. For any nonnegative losses l_(tk)<=B, exponential weights
with initial weights 1/M obeys

```math
\sum_t\sum_k w_t(k)l_{tk}
\le 2\sum_t l_{tk_0}+2B\log M\quad\text{for every fixed }k_0.
```

Proof: exp(-u)<=1-u+u^2/2<=1-u/2 on [0,1]. Hence the log total-weight
decrease is at most -(lambda/2)*sum_t <w_t,l_t>. Retaining the single weight
k_0 lower-bounds it by -lambda*sum_t l_(t,k0)-log M. Combine the inequalities.
This is a pathwise statement even when the loss vectors depend on past
random observations. Convexity, conditional unbiasedness and expectation give

```math
\mathbb E\sum_t V_t(b_t)
\le 2\min_k\mathbb E\sum_t V_t(b_t^k)+2B\log M.
```

The minimum is outside expectation. This is not a comparison with the different
trajectory that would arise if model k controlled the whole process alone.

Let E_k denote expected cumulative weighted baseline error on that common
trajectory:

```math
E_k=\mathbb E\sum_{t,j}e_{tj}^{Q}\mathbf1\{\neg\mathrm{Stop}(R_{tj})\}
 (b_{tj}^k-b_{tj}^*)^2,
\qquad b_{tj}^*=\frac{e_{tj}a_{tj}+s_{tj}d_{tj}}{s_{tj}+e_{tj}}.
```

Here d_(tj) is the second potential response; scalar d=K+1 above is the support
bound. The completed-square calculation gives
E sum_t V_t(b_t^k)<=6*c^2*T+8*E_k/gamma. There are at most three nonzero
true local differences per world; e^Q/(s+e)<=1/(1-gamma),
e^Q/s<=3/gamma and e^Q/e<=1/(1-gamma) justify these constants.

## A conditional execution-regret consequence

For eta<=gamma/(5*d*c), every estimated matching loss has magnitude at most
1/eta. At most d edge estimates are nonzero on a request. Thus the matching
learner's second-moment term is at most d*Vhat_t(b_t), by Cauchy--Schwarz.
The same signed exponential-weights step as in free_feedback.md yields

```math
\mathbb E\mathrm{Regret}_T
\le \frac A\eta
 +\eta d\left(12c^2T+\frac{16\min_k E_k}{\gamma}
                  +\frac{50dc^2\log M}{\gamma^2}\right)
 +2\gamma cT.
```

Take eta=gamma/(5*d*c). Put G=A+2 log M and
gamma=5*sqrt(d*G/(22*T)), provided T>=(50/11)*d*G, which ensures gamma<=1/2.
Algebra gives the explicit bound

```math
\mathbb E\mathrm{Regret}_T
\le 2c\sqrt{22dG T}+\frac{16}{5c}\min_k E_k.
```

No error budget or identity of the best model is used to choose these parameters.
In the special case min_k E_k=0, this is a square-root bound while learning
which model supplies the useful baseline. More generally the bound remains
sublinear if that task-weighted cumulative error is o(T). It may be linear
for poor models; including a zero model does NOT by itself recover the earlier
T^(2/3) guarantee under this more aggressive exploration schedule. That missing
worst-case adaptation is an explicit limitation. Ordinary methods may attain
better rates or constants through other estimators and regularizers.

The ideal baseline uses two potential stopping responses. E_k=0 is a conditional
property a supplied model might have; it is not permission to give a deployable
predictor free access to those responses. Proving this bound does not show that
an inexpensive model exists, that the finite horizon is large enough for a
useful numerical bound, or that this learner beats the ordinary controls.

## Literature, implementation cost and next cheap screen

[Rakhlin and Sridharan (2013)](https://proceedings.mlr.press/v30/Rakhlin13.pdf),
section 4.1 Lemma 6 and its appendix proof, explicitly use a small-loss experts
bound to learn a predictable process. Section 4.2.1 Lemma 7 treats partial loss
feedback with all model predictions available. This is a close antecedent for
both the architecture and the proof strategy. Our baseline is a variance
control for stopped local-order contrasts, not their general predicted loss
vector; its score requires only purchased certificate receipts. The adapter
needs its own observability and sparsity proof, already developed in bp01.

Models require O(M*K) score arithmetic in a direct sparse implementation, plus
their own prediction/search cost. The transfer-tree action learner needs
O((K+1)*log n) additional probability/update work, beyond actual prefix sampling
and setup. Exact arithmetic bit growth and floating-point stability are further
implementation issues. The [declared small probe](model_probe_plan.md) now checks
the combined update. ms01 passes all three 512-request cases on first attempts,
including 480 finite conditional-mean checks over both arms, pathwise score and
estimated-loss inequalities, and zero extra feedback purchases. Fees for the
learned-model / same-tuning zero-baseline ablation are 2486/2476 on seeded bits,
670/664 on all-one worlds, and 6656/6656 on all-zero worlds. No observed fee
improvement is established; the latter two cases deliberately contain a correct
forecaster. Single-trajectory outcomes do not test the expected bound or prove
that selection is economically useful at this short horizon.

The probe's matrix counters include diagnostic enumeration calls. Its
`validation_world_reads` charges six disclosed bits per enumerated path, not
instrumented memory accesses. Named model counters omit some Python arithmetic,
including forecasts constructed before the ablation zeros them. They are
partial counters, not a total computation comparison. The exact earlier bp01
identities, rather than floating-point ms01 checks, support the estimator's
algebraic identity. No broad tuning sweep was added.
