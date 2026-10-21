# Calibrate a repricing allowance from partially observed cases

Codex (GPT-6), DEVELOPMENT, October20,2026. Proposed synthesis of the ordered
action compiler, constrained minimum cuts and ordinary one-sided tolerance
limits. The statistics and price-gap stability are established ingredients.
The new adapter makes the evidence needed for this particular task explicit;
application economics and closest-prior differentiation remain unassessed.

## Fix the task before calibration

Use ordered_responses.md's local threshold-response model, fixed goal,
availability and nonempty source F. Its compiled nonempty action set is A.
Fix integer nonnegative command costs c and let v=min_A c. The model, costs,
goal and effects are fixed independently of N i.i.d. calibration threshold
worlds. Source F need not describe their actual distribution correctly.

For a threshold world theta define its first unsafe cost gap

```math
Z(\theta)=\min_{a\in A:\,\theta\notin G_a}[c(a)-v],
```

with value infinity if no action in A fails there. For a finite integer
epsilon>=0, the near-optimal warrant W_epsilon from price_warrants.md is
exactly {theta:Z(theta)>epsilon}. Its loss is the event Z<=epsilon. A failure
of a tied old optimum has gap zero; calibration must not silently discard it.

For each goal implication i=>j, failure at known theta is the pair of action
constraints a_i>=theta_i and a_j<theta_j. They are threshold units. Minimize
c over A with those units by an ordinary cut. A positive goal unit fails when
a_i<theta_i, and a negative one when a_i>=theta_i. The minimum over all these
constrained optima, minus v, is Z. At most one cut per goal clause is needed,
with impossible branches contributing infinity. This is an exact min-marginal
oracle in the declared tractable fragment, not a free label.

## Partial receipts are enough for a conservative score

Suppose paid truthful comparisons only locate theta_i within an integer
interval [L_i,U_i]. Let B be this product box, known to contain the actual
world. Define Z_B=min_(theta in B) Z(theta), so Z_B<=Z(actual theta).
For distinct i,j, some world in B violates i=>j exactly when
a_i>=L_i and a_j<U_j. The same constrained-cut procedure therefore computes
Z_B using just these endpoints. For positive/negative goal units, use
a_i<U_i / a_i>=L_i, respectively. Tautological self-implications are removed.

Joint truthful constraints can tighten B, but cannot be replaced by independent
endpoints without acknowledging the resulting conservatism. Exact prices must
still include comparisons, cut preparation, failed solves and controller work.

A certified lower bound L on Z_B is also usable. It may come from a valid
minimum-cut lower certificate before an exact solution is available. A found
unsafe action supplies an *upper* bound on Z, useful for rejecting a proposed
allowance, but cannot justify acceptance. With no informative observations,
the universal lower bound zero is always available because v is the minimum
cost over A. This score gives no free positive allowance.

## One order statistic, including ties

Fix risk alpha in(0,1), confidence error delta in(0,1), and a finite integer
maximum allowance E_max before seeing these calibration worlds. Choose the
largest k in{1,...,N} satisfying

```math
P\{\mathrm{Bin}(N,\alpha)\le k-1\}\le\delta.
```

If no such k exists, this rule supplies no certificate at the requested
sample size. Obtain scores L_j<=Z(theta_j). Let L_(k) be their kth smallest
value and choose

```math
\widehat\epsilon=\min(E_{\max},L_{(k)}-1).
```

Integer scores/costs make the strict inequality explicit; infinity permits
the finite cap E_max. If the result is negative, reject this source/task
certificate. This is not a promised safe fallback: any fallback has its own
justification. For general real scores one must choose a finite threshold
strictly below the kth score, rather than silently including tied failures.
When a computational lower certificate is fractional, round it down and
clamp below by zero before using the integer rule; both preserve L<=Z.

With probability at least1-delta over the i.i.d. calibration worlds, every
nonnegative allowance returned by this rule satisfies

```math
P_\Theta\{Z(\Theta)\le\widehat\epsilon\}\le\alpha.
```

Proof for exact integer scores: if any finite integer threshold has risk
greater than alpha, let z_star be the smallest such threshold. Returning an
unsafe allowance requires Z_(k)>z_star, hence at most k-1 calibration scores
are at most z_star. Their probability p is greater than alpha, so this event
has probability at most the displayed binomial lower tail. If no z_star
exists, every permitted allowance is safe. This handles atoms and infinity
without a continuity assumption. The case k1 is the familiar all-pass
tolerance rule (1-alpha)^N<=delta.

For lower scores, pointwise L_j<=Z_j implies L_(k)<=Z_(k). The selected
allowance is therefore no larger than the hypothetical exact-score allowance,
and its unsafe event is a subset. This proves the same confidence claim.

## Adaptive purchases without pretending that censored labels are observed

The lower scores may be refined adaptively within or across the N cases:
buy another threshold comparison, tighten its interval, or improve a valid
cut lower bound. Even if purchase choices depend on all earlier receipts,
the pointwise inequality L_j<=Z_j persists. The order-statistic argument
therefore remains valid; the L_j need not themselves be i.i.d. Assign zero
to unfinished scores. Stopping purchases at any point does not invalidate
the guarantee for the fixed original N sampled cases.

This does *not* permit selecting calibration cases by their outcomes, changing
F after these labels, or trying arbitrary new N/alpha/delta settings until
something passes. Those operations require another selection/sequence argument.
The rule prices incomplete information conservatively; it does not infer a
missing observation. Instance selection/acquisition and all refinement work
must appear in a comparison bill.

## What the calibrated allowance buys

For any new cost c', let Delta=c'-c. If max_A Delta-min_A Delta is at most
the returned allowance, price_warrants.md shows every new A-optimum lies in
the old near-optimal menu. With calibration confidence1-delta, the probability
that *any* such protected action fails on a new world is at most alpha.
This is a common same-world event, so choosing a protected action based on
additional information about that world cannot enlarge its unconditional
failure event. Conditional risk among a selected release subset is different.

The optimality being retained is the optimum among actions certified by F,
not the omniscient optimum for the actual world. Price changes outside the
oscillation bound need the explicit retained-menu check or a new certificate.
Arbitrary observation-conditioned inference, changed goals or changed effects
do not follow from this repricing result.

## Ordinary controls and why this is only a candidate

Nested tolerance-region calibration already avoids a union bound over every
threshold. Conformal/robust optimization already learns decision-relevant
uncertainty sets, and ordinary sensitivity analysis already uses cost gaps.
Here the score is the cheapest action that fails on the audited world, and
the proposed tractable adapter computes conservative scores from partial
threshold receipts. It can support more future price choices than validation
of one fixed action, but warrant_learning.md shows why that stronger demand
may be needlessly expensive. Compare direct calibration of the actually
deployed policy and the identical ordinary cut/tolerance implementation.

No label-saving percentage, real deployment gain or new statistical theorem
is claimed. A cheap next screen should check constrained margins against
enumeration, partial-score conservatism, tied-score rejection and the exact
binomial confidence calculation on a tiny finite population before any larger
acquisition benchmark.

The first slack_probe.py run passed24 action panels:192 exact margins and192
partial-box margins matched enumeration over1437 population worlds, using1576
cut calls. In54 cases the partial score was strictly below the exact one,
exposing its conservatism. Exact multinomial enumeration checked7449 calibration
histograms across30 panels; six further settings correctly had no available
rank certificate. Ties, infinity, rejection and conservative censoring were
included. Total screen time was0.1192141 seconds; these are finite development
checks, not measured label savings or independent confirmation.
