# A sparse unbiased matching-cost estimate from execution alone

Codex (GPT-6), DEVELOPMENT. This constructive repair follows the adverse
no-extra-query controls in [ls01](local_service_results.md). It changes the
feedback duty: an unbiased estimate need not reconstruct every counterfactual
cost exactly on each request. The exposed streams remain developmental.

## Estimator

Keep the monotone, order-independent certificate and fixed-within-request
values/fees contract of [sparse feedback](sparse_feedback.md). The reference
identities are 0,...,n-1. A matching swaps disjoint adjacent pairs. For an edge
j let R_j be the reference prefix strictly before j. If Stop(R_j) is already
true, define A_j=B_j=0. Otherwise set

```math
A_j=\mathbf1\{\mathrm{Stop}(R_j\cup\{j\})\},\qquad
B_j=\mathbf1\{\mathrm{Stop}(R_j\cup\{j+1\})\},\qquad
\delta_j=c_{j+1}A_j-c_jB_j.
```

Sample a complete matching from a distribution P fixed before this request's
unknown values are observed; lazy generation is equivalent. Let e_j be the
probability that edge j is included, and s_j the probability that vertex j is
a singleton (neither adjacent edge is included). Require these to be positive
for the estimate below; explicit exploration will ensure this.

When execution first satisfies Stop, inspect the block containing the last
query. If it stopped on a singleton j<n-1, output only
delta_hat_j=c_{j+1}/s_j. If it stopped on the FIRST item j+1 of the swapped
pair (j,j+1), output only delta_hat_j=-c_j/e_j. If it stopped on the second
item of a swapped pair, the final singleton n-1, or never obtained a
certificate, output the zero vector. No extra truth query is bought.

For fixed current truth and fees, this vector is unbiased for the complete
delta vector. To see the positive term, on the event that j is a singleton,
all earlier matching blocks cover precisely R_j. If Stop(R_j) is false, no
earlier partial block could have stopped, by monotonicity, and querying j
reveals A_j. If Stop(R_j) is true, execution stopped earlier and both the
defined A_j and the estimator contribution are zero. The same argument for
the event that edge j is present reveals B_j by querying j+1 first. Divide
each event indicator by its own unconditional matching probability.

Only the first stopping observation contributes, so each estimate has at most
one nonzero coordinate. This is not a claim that each realized estimate equals
the true delta or that unqueried values have been learned. The exact feedback
lower bounds remain intact because they concern a stronger output duty.

## Computing the probabilities without completing the unseen suffix

For weighted matchings Q(M) proportional to product_{j in M} w_j, let Z[a,b)
be the partition function on the vertex interval [a,b). Then

```math
e_j^Q=\frac{w_j Z[0,j)Z[j+2,n)}{Z[0,n)},\qquad
s_j^Q=\frac{Z[0,j)Z[j+1,n)}{Z[0,n)}.
```

The same 2-by-2 transfer-product tree supplies each interval partition in
O(log n) matrix products. Only the stopping coordinate's event probability
is needed. Compute it from PRE-update weights and the actual sampling
distribution, not a newly updated policy or the probability conditional on
already having reached that prefix.

To ensure exploration, sample P=(1-gamma)Q+gamma U, where U is uniform over
all path matchings. Its edge/singleton probabilities mix linearly. Uniform
matching has e_j^U>=1/5: adding edge j while deleting at most its two adjacent
edges maps every matching to one containing j, with at most five preimages
(j itself, neither, left, right, or both neighbors). Similarly s_j^U>=1/3:
delete the at most one edge incident to vertex j; each singleton image has
at most three preimages. Boundary vertices only improve these bounds.

Thus the estimate magnitude is at most 5*c_max/gamma. Sampling a uniform
matching uses precomputed Fibonacci suffix counts and requires no extra
truth access. Weighted sampling remains lazy. There is at most one point
update, O(log n) extra matrix work for its event probability, and O(n) retained
tree state. Arithmetic precision, setup and the executed prefix are charged.

## A conservative ordinary exponential-weights guarantee

The construction is an importance-weighted partial-monitoring estimator.
Do not claim a new general online-learning principle. Here is a direct bound
for a fixed oblivious sequence, included to expose the variance tradeoff.

Use Q exponential weights over matchings and update by the sparse estimate.
For eta<=gamma/(5*c_max), the elementary bound
exp(-eta*x)<=1-eta*x+eta^2*x^2 applies to every estimated matching loss.
For a fixed world there is at most one nonzero A_j and at most two nonzero
B_j. Therefore

```math
\mathbb E\,\mathbb E_{M\sim Q}
 \left(\sum_{j\in M}\widehat\delta_j\right)^2
\le c_{\max}^2\left(\frac3\gamma+\frac2{1-\gamma}\right).
```

For the negative contribution use e_j^Q/e_j^P<=1/(1-gamma); for the positive
one use e_j^Q/s_j^P<=3/gamma. The terms add because the estimator never has
two nonzero coordinates on one execution. Standard exponential-weights
telescoping and unbiasedness then bound expected execution regret by

```math
\frac{\log N}{\eta}
+\eta T c_{\max}^2\left(\frac3\gamma+\frac2{1-\gamma}\right)
+2\gamma c_{\max}T.
```

The last term is the cost of mixing exploration: the full matching family's
within-request cost range is at most 2*c_max. There are no added feedback
purchase fees, but computation is still outside this execution-regret bound.
This conservative tuning gives a T^(2/3)-type rate; it does not beat existing
general bandit/partial-monitoring rates. Better local-observability algorithms
may use the same information more efficiently and remain relevant controls.

Next cheap screen: enumerate small matching families, several positive
rational weight systems and binary worlds; verify the estimate's exact mean,
one-coordinate support, event probabilities and variance bound. Then compare
a fixed declared tuning on the four exposed ls01 streams, keeping the adverse
older results. No new confirmation exposure or F01 forecast is implied.

## First exact screen and exposed service comparison

[ff01](ff01/attempts.jsonl) passes all four cases on first attempts: 720
world/weight panels, 11,568 execution events, 3792 exact mean-coordinate
identities, 720 variance checks and 108 numerical event-probability checks.
The three weight systems and monotone threshold, two-sided and DNF stopping
rules include both signs of the local cost difference. These checks support
the specified identity, not an unrestricted statistical claim.

[fs01](fs01/attempts.jsonl) then reuses the four already exposed 2000-request
streams, with one prospective formula each for gamma and eta. All first
attempts pass; the saved world hashes match ls01. Query bills are 32,139;
164,806; 145,646; and 596,153. Feedback purchases are zero. Pooled fees are
**938,744**, versus **940,053** for the earlier local-audit learner, a reduction
of 1309 units (about 0.1393%). The ordinary bandit-0 control still costs only
**937,656**; the new learner is about **0.1160% more expensive**. It beats both
fixed-pair bandits on case 0 but not on the other three cases. Retain all
outcomes; no sweep was added to seek a better headline.

The 1,658,916 log-domain matrix products are fewer than the earlier local
learner's 2,008,402, partly because uniform exploration samples through
precomputed Fibonacci counts instead of tree queries. The new learner also
uses 8000 mixture coins, uniform-branch choices and more weight updates.
These are separate operation categories, not a complete 17.4% computation
or monetary advantage. Executed truth reads total 189,131. Exact-estimate
acquisition and noisy-estimate learning are different output duties.

The mathematical gain survives the adverse economic comparison: the full
matching family can receive sparse unbiased difference estimates from its
own certificate execution, without buying full counterfactual labels. That
is useful structure to retain, but its learning rule has not demonstrated a
material advantage over strong ordinary controls on this panel.

## Literature boundary

[Lattimore and Szepesvari (2019)](https://proceedings.mlr.press/v99/lattimore19a/lattimore19a.pdf),
sections 1–2, place arbitrary loss/signal maps in finite-action partial
monitoring and distinguish the learning-rate classes from their game-dependent
constants. Our finite matching game fits that framework. The compact
stopping-event estimator and its implementation are the proposed adapter;
the general possibility of learning with partial feedback is established.
[Kirschner, Lattimore and Krause (2023)](https://jmlr.org/papers/v24/22-1248.html)
is a further comparison lead on structured linear partial monitoring; only
its abstract has been read at this point, so no detailed equivalence or
rate comparison is claimed from that lead.
