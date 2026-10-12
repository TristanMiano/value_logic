# Paid calibration: sources and constructive implications

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; source reading and proposed integration, not confirmation.
Parent scope: [s05 session](session.md), [S25](../s03/robust_tree.md),
[S23](../s03/censored_values.md), and [S12](../s03/policy_bank.md).
Parallel work receives no added principal-clock credit.

## Primary sources actually read

1. **Maurer and Pontil (2009), Empirical Bernstein Bounds and Sample Variance
   Penalization.** [COLT paper](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf).
   Read introduction, PDF pp. 1–2, especially Theorem 4 and the following
   finite-class discussion. Theorem 4 bounds the mean of iid bounded values
   using their observed sample variance. Applying its one-sided statement to
   each member of a fixed finite class gives simultaneous coverage; independence
   between policies evaluated on the same task is unnecessary. The confidence
   construction is imported. Paired policy contrasts and receipt-level costing
   below are our application choices, not a new concentration result.

2. **Dudik, Langford and Li (2011), Doubly Robust Policy Evaluation and
   Learning.** [ICML paper](https://icml.cc/2011/papers/554_icmlpaper.pdf).
   Read PDF pp. 2–4: problem definition, section 2.2 equation (1), section 3
   bias derivation/Theorem 1, and section 4 variance statement/Theorem 2.
   The estimator combines a predicted reward with an inverse-propensity
   correction on observed outcomes. Correct selection probabilities can
   remove bias despite an inaccurate reward model. The paper's analysis
   separates nuisance-model estimation from its evaluation data. Its estimator
   is a conventional comparison for model-assisted paid audits; this reading
   does not establish an economic advantage for our service.

3. **Howard, Ramdas, McAuliffe and Sekhon (2021), Time-uniform,
   nonparametric, nonasymptotic confidence sequences.**
   [Author manuscript](https://arxiv.org/pdf/1810.08240).
   Read manuscript section 4.1, Theorem 4/equation (23), and section 4.2,
   equations (25)–(27), PDF pp. 13–15. A bounded observation sequence and
   predictable forecasts yield an empirical-Bernstein confidence sequence
   using accumulated squared prediction errors. The target is the average
   conditional expectation, not automatically a constant population mean.
   Their randomized-treatment example combines forecasts and known assignment
   probabilities. This supplies an anytime conventional construction when
   audit decisions adapt; neither optional stopping nor changing forecasts
   requires treating forecasts as authoritative truth. The paper's two-sided
   statement has error allowance twice the one-sided boundary allowance.

No full-paper or exhaustive novelty review was performed.

## Additional primary reading: exact T-join closure

The principal's subsequent construction asks whether pairwise upper error
bounds imply a *sharp* parity-error bound through minimum-weight T-joins.

- **Edmonds and Johnson (1973), Matching, Euler tours and the Chinese
  postman**, Mathematical Programming 5, 88–124.
  [Paper](https://web.eecs.umich.edu/~pettie/matching/Edmonds-Johnson-chinese-postman.pdf),
  [publisher record](https://doi.org/10.1007/BF01580113).
  Read retrieved indexed paper passages for journal pp. 91 and 94: equation
  (3.5), elimination of the auxiliary parity variables, the convex-hull
  statement, and dual equations (3.7)–(3.9). The original paper supplies the
  integral parity polyhedron and its fractional odd-cut packing dual. Direct
  PDF requests returned gateway errors; the full paper and algorithm proof
  were not inspected. The paper's postman setup uses its degree-odd nodes.

- **Cornaz, Grappe and Lacroix, Trader Multiflow and Box-TDI Systems in
  Series-Parallel Graphs**, author manuscript dated March 5, 2018.
  [Author PDF](https://www-lipn.univ-paris13.fr/~lacroix/research/publications/boxTDIMF.pdf).
  Read definitions on PDF p. 4, section 2.1 on p. 5, and the subsequent
  distinction from total dual integrality. Section 2.1 states the T-join
  dominant description for an arbitrary undirected graph and even vertex set
  T, referring to Schrijver's Corollary 29.2b. The series-parallel restriction
  concerns the later TDI/box-TDI result, not the dominant description itself.

The imported graph statement is

```text
conv{incidence(J): J is a T-join} + nonnegative_orthant
  = {x >= 0: x(delta(S)) >= 1 for every S with |S intersect T| odd}.
```

Thus for nonnegative edge weights p, linear programming over this dominant
has the minimum T-join value, and its dual is a nonnegative *fractional*
packing of T-odd cuts with edge capacities p. Integer dual packing is not
needed and is not claimed for arbitrary graphs.

The proposed probability application requires common vertex bits whose pair
errors are their XORs, or a consistent change of vertex signs. Each outcome
then identifies a cut, and odd parity on T identifies a T-odd cut. Arbitrary
independently selected edge forecasts need not have that consistency.
Restricting the cut-packing mass to at most one and adding empty-cut mass
converts a feasible packing into a probability law; this is the proposed
application step, not a theorem attributed to either graph paper. It motivates
the sharp candidate value `min(1, minimum_T_join_weight)`. The principal's
derivation and finite checks must establish the exact probabilistic scope.

## Strong direct comparison from the same receipts

Fix K normalized policy scores f_k in [0,1] before iid task draws, and fix
n >= 2. A conservative direct use of Maurer–Pontil Theorem 4, with error
allowance alpha/K per score, gives simultaneous lower endpoints

```text
L_k = mean(f_k) - sqrt(2 * sample_variance(f_k) * log(2K/alpha) / n)
                 - 7 * log(2K/alpha) / (3 * (n-1)).
```

Evaluate all computable policies from each task's shared receipts. The
statistical multiplicity is logarithmic in K; paid label cost is the union
of necessary receipts, not K separate populations. Retain computation costs
for scoring every policy. If the decision concerns a contrast in [-1,1],
apply the bound to its rescaling into [0,1], then undo that rescaling.
Shared components cancel before both acquisition and variance estimation.
Known constant costs can be subtracted afterward without adding variance.
These statements do not cover newly selected score functions or repeated
fixed-n peeking; use an appropriate common event or an anytime construction.

The useful comparison therefore includes a paired, receipt-sharing policy
bank. A marginal source must demonstrate reuse beyond what that bank already
receives, or a cheaper representation of a larger decision family.

## Proposed middle route: selected block calibration

S25 bounds prediction error along a path by adding edge-error bounds. Keep a
small, prospectively declared library of contiguous path blocks, including
single edges. For fixed edge forecasts, a block's error is the parity of its
edge errors. Obtain simultaneous upper bounds u_B for these block errors
from checked sampled tasks. No independence between edges is assumed.

For any fixed acquisition set S, split the unqueried edges on a target path
into contiguous gaps. Cover each gap by disjoint library blocks. The node
prediction is wrong only if at least one chosen block has odd error, hence

```text
node_error(S) <= min(1, sum_over_cover u_B).
excess_score_lower(S) = max(0, 1 - 2 * min_over_covers sum_over_cover u_B).
```

The second line permits the same explicit fair-guess fallback as S25. Find
the minimum additive bound for each gap by a shortest-cover dynamic program:
for a gap beginning at i, initialize b[i-1]=0 and set
`b[j]=min(b[k-1]+u_[k..j])` over available ending blocks. A shared confidence
event covers later choices among these covers and fixed query sets. This is
still nonadaptive acquisition with respect to deployment labels.

Singleton fallback preserves the original bound when the supplied edge bounds
are unchanged. Actual calibration must account for allocating confidence
across the enlarged library. This is a proposed bridge between sparse moments
and S25's marginal guarantee, using ordinary union bounds and dynamic
programming. Its possible benefit comes from cancellations inside blocks and
reuse across policies; no new statistical principle is claimed.

One checked edge receipt can update every completed block and every evaluable
policy on that same task. Charge each primitive computation once, plus all
checking and update work. A directly checked block parity may be cheaper than
its separate edges only when the actual verifier offers that operation.

## Residual audits as a subsequent construction

For a fixed bounded target Y, forecast h before observing its label and audit
with known probability q > 0. If an audit obtains the exact label, the usual
correction `Z=h+A*(Y-h)/q` satisfies `E[Z | Y,h,q]=Y`. Its added audit variance
is `(Y-h)^2*(1/q-1)`. This identity is an imported residual-estimation principle,
already present in S23; it suggests adapting paid acquisition to the residuals
of useful blocks or contrasts, rather than fitting an entire joint law.

Predictable models, positive probability floors and correctly bounded Z allow
the Howard framework to support sequential acquisition. For a population-mean
claim, choose the filtration so each fresh task retains the declared sampling
law; otherwise report its average conditional target. Model fitting, cheap
features, audits, and inverse-probability range costs all enter the comparison.
An attempted audit that times out has not supplied Y. Keep its unresolved
interval or the existing partial-receipt bound, rather than silently treating
it as a completed residual observation.

The next inexpensive constructive check is a correlated path source with
paid shared receipts: compare edge bounds, a small block library, and paired
policy contrasts at equal total acquisition cost. Follow with adaptive
residual acquisition only if that simpler comparison identifies useful reuse.
