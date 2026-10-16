# Fallible forecasts as sparse variance baselines

Codex (GPT-6), DEVELOPMENT derivation, not an executed new learner. This links
the [execution-only estimate](free_feedback.md) to model usefulness without
requiring an approximate model to certify truth. It is an application of
ordinary control variates, with a sparse stopping-query interface.

For edge j write e and s for its sampling edge/singleton probabilities and
a=c_{j+1}*A_j, d=c_j*B_j. On a request whose reference prefix R_j has not
already certified the answer, introduce a common baseline b_j. If the
executed matching visits j as a singleton, contribute (a-b_j)/s. If it visits
the swapped pair beginning with j+1, contribute (b_j-d)/e. Otherwise contribute
zero. Record the first-item Stop indicator whether or not execution stops
there; its truth is observed by the ordinary checker.

The baseline terms cancel in expectation, leaving a-d=delta_j. If R_j already
certifies the answer, neither event is reached and the estimate is zero, as
required. Hence a wrong forecast can increase variance but does not introduce
bias into this estimate. This conclusion requires the SAME b_j for the two
counterfactual orientations. It may be fixed from past rounds and current
public context, or be a canonical function of R_j's received values. It must
not depend on the sampled orientation, a differently ordered transcript, or
the current random seed. Keep weights frozen throughout one request and apply
all collected updates afterward.

The per-coordinate second moment, before multiplying by the weighted learner's
edge marginal, has the exact decomposition

```math
V_j(b)=\frac{(a-b)^2}{s}+\frac{(b-d)^2}{e}
=\frac{(a-d)^2}{s+e}
 +\left(\frac1s+\frac1e\right)(b-b_j^*)^2,
\qquad b_j^*=\frac{ea+sd}{e+s}.
```

This is second moment, not variance; subtracting the fixed delta_j squared
gives variance. The identity applies when Stop(R_j) is false; the whole
expression is multiplied by that indicator otherwise. The forecast target
is a particular weighted stopping response. Generic truth accuracy need
not be the relevant model-quality measure.

For example, if both possible first queries immediately certify, and both
fees equal c, then delta_j=0. The zero baseline still generates opposite
importance-weighted noise, while b_j=c makes both observed contributions
zero. Conversely, predicting b_j=c when neither query could certify creates
noise where the zero baseline produced none. No universal improvement follows
from adding a model. The ideal b_j^* is a diagnostic depending on unobserved
counterfactuals, not a free deployable oracle.

An advice model can propose at most K active baseline edges before a request;
use b_j=0 elsewhere and clip active values into [0,c_max]. There are at most
K+1 nonzero estimate coordinates, so the sparse transfer-tree implementation
needs O((K+1)*log n) extra event-probability and update work, beyond executed
prefix sampling and the model's own charged cost. Each coordinate magnitude
is at most 5*c_max/gamma. Taking eta<=gamma/(5*(K+1)*c_max) gives the same
elementary exponential-weights step bound. By Cauchy--Schwarz, its conditional
second-moment term is at most

```math
(K+1)\sum_j e_j^Q\mathbf1\{\neg\mathrm{Stop}(R_j)\}
\left[\frac{\delta_j^2}{s_j^P+e_j^P}
 +\left(\frac1{s_j^P}+\frac1{e_j^P}\right)(b_j-b_j^*)^2\right].
```

This exposes a model-error quantity which could pay for prediction, but does
not yet show that any available cheap model makes it small. An observed
positive contribution would need model preparation/evaluation prices and
ordinary no-model controls, with selection costs retained. Do not run a broad
tuning sweep solely because an oracle baseline looks favorable.

[Greensmith, Bartlett and Baxter (2004)](https://jmlr.org/papers/volume5/greensmith04a/greensmith04a.pdf),
Theorem 16 and section 7.1, already express baseline-induced excess variance
as weighted squared error and study learning a useful baseline. Their
controlled-POMDP gradient setting differs from this matching difference
estimate. The elementary completed-square identity is inherited control-variate
algebra, not a new principle of Value Logic. [Rakhlin and Sridharan (2013)](https://proceedings.mlr.press/v30/Rakhlin13.html)
is a further lead on exploiting and selecting predictable processes; only its
abstract and introductory feedback discussion have been read here. The
proposed delta, if useful, would be the paid sparse implementation and its
task-specific feedback contract.
