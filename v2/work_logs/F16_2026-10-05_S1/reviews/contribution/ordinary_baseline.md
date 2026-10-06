# Ordinary exact baseline and a fresh stability objection

Contributor: **ChatGPT (GPT-6 Astra Pro)**, separate delegated F16 reviewer.
October 5, 2026 UTC. Derivation/read-only reconstruction; no experiment rerun.
Concurrent principal-clock credit: **zero**.

## 1. Equal-source construction

Let `p` denote a finite Boolean-world law. At a current source revision, the
ordinary competitor receives precisely the retained authorized measurements
`A p = y`, public restrictions `H p = h`, nonnegativity and normalization.
Its uncertainty set is

`P = {p >= 0 : 1^T p = 1, A p = y, H p = h}`.

An unavailable/withdrawn old measurement is not part of `A`, even if a hidden
scoring law continues to satisfy it. The competitor must not recover discarded
information from an uncharged archive, seed enumeration, a consistency witness
supplied by the scoring oracle, or arbitrary nonlinear source coding excluded
by the native information contract. Conversely, it may retain a full law or
an exact basis whenever the native route is granted that information.

Two measurement matrices with the same affine row span produce the same `P`
after their known values are correspondingly translated. Thus the five-field
tailored summary and six old means in F15 represent the same five-dimensional
information. The strongest ordinary method may use the identical five-field
representation; a different label cannot create a lower bound or advantage.

For the general signed piecewise-affine fragment, use the same finite source
cells and expression branch conditions. Access to a unit-restricted reduct
is a premise-eligibility policy: construct the ordinary admissible source from
the same reachable rows and conversions. An ordinary full-source solve and
an ordinary restricted-source solve are distinct services, just as native
warrant and full-source modeled validity are distinct in the project.

## 2. Exact revised queries and certificate scope

Let the current action/query cost be `C_a(p) = q_a^T p`. Define

`L_a = min_{p in P} q_a^T p`,
`U_a = max_{p in P} q_a^T p`.

With nonempty compact `P`, rational input, and finite dimension these extrema
are achieved and have exact finite LP descriptions. An equality answer has
`L_a = U_a`. The midpoint has sharp scalar worst error `(U_a-L_a)/2`; its
admission/refusal follows the same numerical tolerance as the native route.
The vector of coordinate midpoints minimizes worst error in the sup norm
without necessarily belonging to the image of one coherent law. Reusability
as a law is therefore a stronger output contract.

For a comparison `C_a-C_b <= beta`, a dual/Farkas certificate establishes
the bound on the same `P`. In the piecewise-affine case, certificates cover
each relevant branch, including branch infeasibility where required. The
ordinary producer may compile these certificates into the existing S1 proof
syntax and use the same receiving checker. This argument assumes the existing
fragment characterization; it is not a new proof of unrestricted compiler
correctness or completeness under a finite resource budget.

The reception wrapper includes the current source/context, allowed information
paths, target expressions, scope, unit, budget and proof-root statement.
Validation compares those exact objects with the consumer's actual request.
Hashing is a convenient implementation of a binding, not a theorem about
source honesty, intended units, or deployment transport. Revalidate the
mathematical witness and its current eligibility, not only a hash.

Cached proof trees, alternative witnesses, coefficient catalogues and dependency
graphs are available ordinary options. They can avoid search in favorable
cases, but their creation, retention, maintenance, failures, fallback solving
and current checks must all enter a practical comparison. No superiority
follows from a small checker alone.

## 3. Why the ordinary same-law regret solver is exact

For a finite action set `B` containing fallback, realized regret is

`r_a(p) = C_a(p) - min_{b in B} C_b(p)`
`       = max_{b in B} (C_a(p)-C_b(p))`.

Because `B` is finite,

`sup_{p in P} r_a(p) = max_{b in B} sup_{p in P}(C_a(p)-C_b(p))`.

For the upper bound, every term at every law is at most the right side. For
the reverse bound, each fixed competitor's supremum is bounded by the left
side, and taking the finite maximum preserves that inequality. The solver
therefore needs ordinary linear pairwise comparisons over one law, not a
distinct decision primitive.

Replacing `P` by independent cost intervals is a relaxation. It permits the
chosen action's upper extreme and a competing action's lower extreme to
arise at different laws. That can make regret too pessimistic, but the
strongest ordinary baseline never makes that information-losing relaxation
unless it is itself the declared contract or a deliberate cheap approximation.

A regret tolerance claim and a zero-budget fallback comparison differ. For
example, `sup(C_a-C_fallback)` may be small positive while `sup r_a` remains
below a positive tolerance. A received proof for a diagnostic action also
does not establish a regret claim for the action actually selected. Neither
distinction depends on special Value Logic arithmetic.

## 4. Exact retention and repair are observation-matrix problems

Write all old numeric queries as rows of `Q_old` and future queries as rows
of `Q_new`. If the source affine directions contain a relatively open set,
exact linear retention with arbitrary decoding must separate any direction
that changes a demanded numeric query. Equivalently, the required nullspace
inclusion is `ker A subseteq ker Q`, after removing source constraints and
known constants. A row-space basis attains the associated rank.

This principle also gives the incremental rank requirement

`rank([H; Q_old; Q_new]) - rank([H; Q_old])`,

with normalization included in `H` and rank measured on the same ambient
space. It does not itself evaluate the special reset-price matrix. That
evaluation, its explicit actual-mean repair construction and its sharp
radius/witnesses are the possible small application delta in C4.

If rank shows a missing coordinate, the ordinary method can keep the full
feasible fiber and answer partially. It need not reconstruct all of `p` or
return nothing. If acquisition is allowed, it may request exactly the same
actual order means and update `A,y`; if the consumer only needs a decision,
it may stop before numeric completeness. Query counts are not prices, bytes,
sample sizes or source-execution counts.

## 5. Simultaneous source coverage and selected-query guarantees

Assume the true state is included in a data-dependent source `C(D)` with
probability at least `1-delta`. A current accepted certificate establishes
its selected inequality for every state in that same `C(D)`. On the event
that the true state is included, the selected inequality is true even if
the query, bound and acceptance decision depend arbitrarily on `D`. Hence

`P(accepted AND selected bound false) <= delta`.

This is event inclusion. It is available to any ordinary solver producing
valid uniform source statements. It does not imply the same probability
conditional on acceptance, validate a misspecified model, or license optional
stopping under pointwise coverage. For a repeated guarantee use a joint
event, a justified time-uniform construction, or an explicit error budget.

The exact finite laws in F15 are stipulated model information. The strong
exact-old-summary assumption in C4-A3 is likewise a mathematical premise;
it is not a demonstrated empirical calibration result. Replacing exact old
measurements by intervals enlarges the consistency set in the already
established optimal-recovery framework. A future contribution would need to
evaluate the particular observation design, noise, and useful decisions.

## 6. Fresh small-edit baseline

Consider one unchanged full-order reset family with fixed terminal penalty
and one price edit `c_j -> c_j+epsilon`, preserving positivity. For each
world and action, the cost difference is exactly

`d_a(world) = epsilon * 1{action a reaches j}`.

An unchanged fixed fallback has difference zero. Thus, for every action and
law, the new-minus-old cost is in the common interval `[l,u]`, where
`l=min(0,epsilon)`, `u=max(0,epsilon)`, and `u-l=|epsilon|`.

### Numeric consequence

If the exact old mean `C_a^0` is known, use the estimator

`hat C_a^1 = C_a^0 + (l+u)/2`.

Its maximum absolute error is at most `(u-l)/2=|epsilon|/2`. When the action
reaches the edited procedure deterministically, its exact shift may be used
instead. The generic estimator remains valid regardless of dependencies
among procedure outcomes, the old-summary fiber's dimension, or the size
of a nonzero price edit. Positivity is needed for the stated task model;
the pointwise inequality itself is elementary.

### Action consequence

Let `a0` minimize the old means over the same actions including fallback.
Every compatible law gives the same retained old means, so the chosen old
optimizer is common to the fiber. Let `a1(p)` be a new optimizer at law `p`.
Then

`C_a0^1(p) <= C_a0^0 + u`
`           <= C_a1(p)^0 + u`
`           <= C_a1(p)^1(p) + u-l`.

Therefore the unchanged old optimizer has same-law regret at most
`|epsilon|` uniformly over `P`. This proof makes no assertion for changed
programs, outcome laws, source authority, or an action family different from
the one whose old means were retained.

### F15 numerical substitution and its limit

For each small-price variant, `|epsilon|=1/40`. Numeric tolerance and regret
tolerance both equal `1/20`. The two generic guarantees are respectively
`1/80 < 1/20` and `1/40 < 1/20`. So exact old means alone suffice for these
two service dimensions in those arms, without the specialized radius.

The additional useful-native requirements are not implied: a received
comparison at budget zero with margin `1/20` may require stronger information,
the selected action may differ, and the proof must meet its explicit premise
criterion. Do not infer all useful counts or timing from this derivation.

For `M=4`, C4-A1's uniform radius is `|epsilon|/4`; that factor-of-two
improvement over the generic midpoint bound could matter when
`|epsilon|/4 <= tau < |epsilon|/2`. F15's small-edit tolerance lies above
both bounds. A prospective numerical-discrimination study could select a
different tolerance/price combination, but even then a generic exact
optimal-recovery solver has access to the same sharp interval. The potential
contribution remains the explicit consequence and evaluated application,
not an inability of established mathematics to produce it.

## 7. Load-bearing interpretation

The ordinary reduction defeats generic inference-power, primitive novelty,
cheap-checker-as-speed, discarded-joint-information and broad acquisition
claims. It also demonstrates why the useful results are technically
conservative. Under the author's criterion, these facts leave room for a
modest application whose additional content is explicit, correct and useful.
If those concrete consequences disappear under a closest-source reduction
or proof repair, the word "synthesis" cannot preserve a positive disposition
on its own. This is why the main review's support is tied to the exact
price results and bounded operational examples.
