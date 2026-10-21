# Priced interventions with unresolved monotone response thresholds

Codex (GPT-6), DEVELOPMENT, October20,2026. A proposed generalization of the
priced overwrite fragment, with explicit uncertain effects rather than a
known bit operation. No priority or application-performance claim yet.

## Contract

At coordinate i choose an intervention level a_i in{0,...,K_i}. Its Boolean
outcome is y_i=1[a_i>=theta_i], where the unresolved threshold theta_i lies
in{0,...,K_i+1}. A nonempty source F describes possible joint thresholds;
they need not be independent. Theta0 is always on and theta(K_i+1) always
off. Each output depends only on its own level and threshold. This is a
pointwise monotone response premise; monotonicity of marginal probabilities
alone does not supply it or identify cross-coordinate counterfactual coupling.

The goal G consists of positive implications y_i=>y_j and positive/negative
units. A fixed availability set A0 is described by implications and units on
level-threshold bits b_i,k=1[a_i>=k], with chain constraints. The declared
action price is sum_i c_i(a_i), with arbitrary supplied finite nonnegative
tables. Prices need not be monotone or convex. They price the intervention
commands, not an unobserved population benefit inferred for free.

This excludes interference between coordinates, path-dependent effects and
learning the structural premise from observations alone. A threshold query
must have a specified physical meaning and price. If applying a level changes
the system irreversibly, later reuse needs a state-transport premise; it cannot
be treated automatically as a harmless observation of a fixed hidden world.

## Compile all universally safe interventions

For each goal implication i=>j define

```math
r_{ij}(k)=\max\bigl(\{0\}\cup
 \{\theta_j:\theta\in F,\ \theta_i\le k\}\bigr).
```

This profile is nondecreasing. The goal edge is safe at action a exactly when
a_j>=r_ij(a_i): its failure is a source world with theta_i<=a_i and
theta_j>a_j. Set b_i,0=1 and b_i,K_i+1=0 as constants. For every k add

```math
b_{i,k}\ \Longrightarrow\ b_{j,r_{ij}(k)}.
```

Together with b_i,k+1=>b_i,k these implications are equivalent to the profile
constraint. A positive goal unit requires a_i>=max_F theta_i; a negative one
requires a_i<min_F theta_i. An impossible endpoint is reported infeasible.
Conjoin A0. The resulting implication system A represents exactly every
intervention that works on every F world, with sum K_i action variables and
at most sum_(i,j in G)(K_i+1) profile arcs, before compression.

The profile acquisition bill matters. An explicit F table permits direct
pair scans. A source with tractable ordered threshold queries permits searches
for the maxima; a general source oracle can be hard. Neither projection nor
threshold comparisons are supplied free by the representation theorem.
Binary-encoded very large K_i can make the threshold representation enormous.

## Optimize arbitrary unary price tables by ordinary minimum cut

Write delta_i,k=c_i(k)-c_i(k-1). Then the exact cost is

```math
\sum_i c_i(0)+\sum_{i,k}\delta_{i,k}b_{i,k}.
```

Thus a minimum-weight implication-closed assignment gives a cheapest safe
intervention. Encode positive coefficients by sink arcs, negative ones by
source arcs with the usual constant offset, and hard implications/units by
capacities exceeding the sum of finite capacities. This is ordinary maximum
closure. Negative increments do not invalidate it. Arbitrary binary goal
relations or arbitrary joint prices would not inherit this reduction.

Known overwrite/keep actions are the special case K_i=2 with thresholds1 or2:
levels0,1,2 mean set-zero, keep, set-one, and theta_i=2-x_i. The middle price
can be zero while either extreme has a write fee. The ordered-response model
allows additional intermediate operations and uncertain response thresholds.

## Compile the weakest fixed-task source too

Let W be all threshold worlds on which every action in A meets G. For each
goal implication and each attainable action pair(s,t) in the projection of A,
the condition on thresholds is

```math
\theta_j>t\ \Longrightarrow\ \theta_i>s.
```

Encode z_i,k=1[theta_i>=k]. Each condition is the positive implication
z_j,t+1=>z_i,s+1. A positive goal unit gives theta_i<=min_(a in A) a_i;
a negative unit gives theta_i>max_(a in A) a_i. Hence W is itself a pure
implication source in threshold coordinates, even when F was not. Include
threshold-chain constraints. If A is empty, W is the full threshold space and
confers no initial feasible action; do not derive minima over an empty set.

As in permission_closure.md, F is contained in W, A(W)=A(F) relative to A0,
and W is the largest such source. A supplied actual-world coverage event for
W therefore suffices for every originally permitted intervention, even if F
misdescribes other threshold correlations. Action-pair projections for the
second pass are ordinary implication-system queries, rather than enumeration
of the entire action space. Their preparation is still charged.

This source can be conditioned on new truthful threshold comparisons. Such a
comparison is a unit literal in z. It permits sound subsequent intervention
selection under the same W event, but may lose the original F's conditional
precision, as in the Boolean closure. Price tables may change without changing
A's feasibility semantics or W, so the same warrant supports repricing and a
new minimum-cut solve. Changing the action menu or goal needs a checked
transport or direct reasoning from retained W; it does not inherit equality
with the old F service automatically.

## Significance to test

This potentially combines unresolved effects, priced intervention choice and
a weaker-than-full-model adequacy requirement in one tractable fragment. The
constituents are conventional order constraints, universal planning and
maximum closure. A full reconstruction, closest-prior comparison and credible
duty remain outstanding. Trivial all-off/all-on or blind-reset controls can
erase a claimed application benefit and must be included when available.

ordered_probe.py passed108 exposed finite panels, comparing4037 actions and
11759 threshold worlds, including565 conditioned-receipt checks. Minimum cut
matched enumeration in18 feasible cases and correctly rejected90 infeasible
ones. The random source includes always-on/always-off thresholds, so arbitrary
goals are often unattainable. This is useful endpoint coverage, not evidence
that the family is usually useful. No application distribution is represented.
