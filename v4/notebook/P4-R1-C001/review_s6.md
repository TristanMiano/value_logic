# S6 working review and derivations

Codex (GPT-6), resumed November 10, 2026. Review base: main `87d21941`.
Earlier results remain attributed to Claude (Fable 5.2). This is a fresh
cross-model reconstruction, not independent human review or formal proof.
Prospective aim and timing are in [record.md](record.md).

## Central reconstructions

- **Theorem 1:** the posterior second-moment proof works. Condition on the
  fine labels/outcomes in all but one history position. Equality of the four
  forecasts AA, AB, BA, BB forces the posterior squared difference to vanish;
  averaging those posteriors recovers the prior. Independence of assignment
  from skill is essential to the four positive-probability comparisons.
- **Theorem 5:** covariance is bilinear under independent assignment, so
  refinement preserves the existence of a nonzero covariance. On
  trait-tracking supports the map is extensive: a credited judge's own
  marginal variance supplies a witness within the full later panel.
  Monotonicity and extensivity give the finite closure iteration. State
  trait dependence on a positive-mass set of instances, not necessarily on
  almost every instance; finite panel-kernel classes make the scope explicit.
- **Theorem 13:** equality in two data-processing steps gives conditional
  independence of refined labels within a coarse label. The corresponding
  nonnegative Gram block has proportional rows, hence rank one; its
  likelihood vectors are proportional. Ignore zero-mass observations.
  The theorem concerns information about persistent state, not every
  distinction in marginal recurrence frequency.

These reconstructions support the central cores. Numerical checks and
source comparisons below are separate obligations, not substitutes for them.

## Repairs made at the first S6 checkpoint

1. **R1.6 / R1.1 bridge.** With independent task assignment and
   `W=(X,Y)`, the information of the pair labels is
   `I((c(X1),Y1);(c(X2),Y2)) = H(Y2|c(X2)) + V1(c)`.
   The baseline depends on c. Thus the objectives and their maximizers
   need not be identical. A world with no varying skill and task-dependent
   difficulty has positive difficulty-recovery gain but zero pairwise
   mutual information. Conditional proper scoring unifies the two games
   while retaining their different targets and side information. Also,
   task twins imply diagnostic twins of (task,result) under A1; arbitrary
   skill-dependent task choice needs proportional assignment likelihoods.
2. **R1.3 geometry.** Two shared causes can have N exemplars (N distinct
   points on a positive quarter-circle). Small counts need distributional
   conditions, as in the Gaussian construction. The arc-count formula
   requires a proper sector of angle at most pi and a nondegenerate hull;
   the full-plane cone gives E[V], not 1+E[V]. Preserve invariance and the
   Gaussian positive result. Added criteria preserve strict winners by
   giving the new criterion a sufficiently small positive weight, even
   when the old cone is lower-dimensional.
3. **R1.4 calibration.** The invariant quotient is under positive affine
   recalibration, including both means and sensitivity. Equal-difficulty
   tasks can have correlation one but different sensitivity to skill.
   Rank identifies linear span dimension; identifying a number of causal
   factors needs a full-rank factor model and further causal assumptions.
4. **R1.5 ties.** Disconnected components with equal maximal Perron roots
   can all survive. Connectedness gives a unique positive limit independent
   of initialization; it is not necessary for all judges to survive for a
   particular start. The count-update code adds M w, rather than w*(M w),
   so its normalized continuous analogue is linear reinforcement, not the
   ordinary replicator equation. Preserve and extend the convergence result.
5. **R1.7 boundary.** Centre the environmental vector when ratings are
   centred. At an invasion-payoff tie, beta>0 and distinct ratings produce
   second-order invasion; beta=0 or identical ratings can instead give a
   neutral face. Distinguish asymptotic stability from neutral stability.
   Preserve the consensus-adaptation construction and characterize all
   boundary cases rather than discarding it.
6. **Comparisons.** Equal population recovery targets do not identify an
   identical algorithm or objective. Keep the useful correspondence to
   co-clustering without asserting that all co-clustering is this score.

## Positive quantitative extensions, now written in R1.8

**Uniform-history transfer bound.** Theorem 16 now proves Theorem 2's bound for every
n >= 1 with the same constant. Condition on the remaining n-1 fine history
positions, apply the two disjoint pairwise quadratic comparisons, then use
Jensen on the posterior second moments. The coarse forecast may depend on
the coarsened remaining history; the pairwise lower bound holds for any
common reference forecast, so this does not assume it is posterior-optimal
after revealing the fine history. Nonmonotone actual gains do not obstruct
a uniform lower bound.

**Explicit diagnostic bound.** Let A,B be disjoint sets in one c-cell,
with masses alpha,beta, and let
`d = E[(L(A|theta)/alpha - L(B|theta)/beta)^2]`.
Put `k = alpha*beta/(alpha+beta)`. Theorem 17 proves:

```math
I(W_1;W_2)-I(c(W_1);c(W_2))\;\ge\;2k^3d^2.
```

Derivation: retain the one-sided loss `I(W1;W2|c(W1))`. Weighted Pinsker
and the triangle inequality give at least `k/2 * ||r_A-r_B||_1^2`, where
r_A and r_B predict the original next observation given A and B. Their
difference t has zero sum and `t(A)/alpha-t(B)/beta=d`. The range of the
test function `1_A/alpha-1_B/beta` is `1/k`, so `||t||_1 >= 2kd`.
In the balanced binary model with normalized likelihoods 1 +/- epsilon,
the bound and actual mutual information both start at epsilon^4/2, so
the constant is asymptotically sharp there.

## Coupled kinds and actions: routes to compare

- Score forecasts on a common external event space, keeping a decoder or
  within-kind baseline explicit. Otherwise changing kinds changes the
  prediction question and can reward trivial categories.
- Compare raw self-fulfilling recurrence with observation under a declared
  intervention/reference policy. Seek a joint update of partitions and
  forecasts with independent environmental exposure, and characterize
  regimes in which informative exploration or an audit channel is needed.
- Treat the future distribution as affected by ratings/actions. A useful
  fixed point must state whether it is predictively calibrated in its own
  induced world, optimal under deployment, or grounded in a common external
  comparison. These can be connected by conditions, but are distinct.

## Source observations (bounded read scopes)

- Shalizi and Crutchfield, [arXiv cond-mat/9907176v2](https://arxiv.org/abs/cond-mat/9907176v2):
  section V, especially Theorem 1, Corollary 1, Lemma 7 and Appendix E.
  Their sufficient predictive states and refinement proof are the direct
  enabling comparison. Our finite episode models require no infinite-past
  construction; equivalence of one-step prediction and latent sufficiency
  uses the additional shared-likelihood Gram structure.
- Kong and Schoenebeck, [1605.01021v2](https://arxiv.org/abs/1605.01021v2)
  and [1802.08887v3](https://arxiv.org/abs/1802.08887v3): abstracts verified;
  the latter's conditional-independence and elicitation claims concern a
  mechanism-design target not yet proved by our vindication operator.
- Borgs, Chayes and Lovasz, [0803.1244v2](https://arxiv.org/abs/0803.1244v2):
  abstract and reduction framework checked; a symmetric graphon is not
  literally the nonsymmetric performer/task kernel. Twin reduction is the
  relevant analogy, not an already verified transfer of the full theorem.
- Keribin et al., [categorical latent block model](https://link.springer.com/article/10.1007/s11222-014-9472-2):
  publisher abstract confirms the cited identification/estimation topic.
  Full hypotheses have not yet been reconstructed.
- Perdomo et al., [Performative Prediction](https://proceedings.mlr.press/v119/perdomo20a.html):
  definitions and Theorem 3.5 / section 4 checked. Stable retraining and
  deployment optimality are distinct; contractive feedback plus smoothness
  and strong convexity supplies one positive convergence route. This is a
  closer comparison for R1.7 than preference evolution alone.

## First S6 checkpoint

The central proofs survived reconstruction. The seven result files now have
dated corrections; earlier notebooks and output bytes are preserved. R1.8
states and proves the two bounds. The independent rational checker reports
65 partition/history checks, 44 history-bound comparisons, 360 diagnostic
partition comparisons, 660 diagnostic-bound comparisons and four support
worlds, with no violation.

R1.9 gives a simultaneous population construction for forecast calibration
and concept influence under agent-caused recurrence. A positive environmental
share, a finite catalogue including the finest representation, and persistent
learning imply recovery. A fixed total budget can fund the needed learning
reserve. A matched example proves that allocating learning only in proportion
to current influence can permanently suppress an initially mistaken useful
model. The numerical work retained slow near-twin convergence and repaired
integration coordinates after normalization checks exposed numerical drift.

The review also characterized individual vindication as self-repeatability,
showed why longer own-approval histories do not enlarge its support under
B1--B2, and supplied coalition credit for joint-only signals. R1.5 now includes
the tied-Perron-root limit and a proof for its actual discrete count update.

The remaining research time will investigate finite observations, known
self-caused recurrence corrections, and practical costs, while retaining
the broader W1 questions. This is a checkpoint, not cycle completion or the
final aim-balance self-review.
