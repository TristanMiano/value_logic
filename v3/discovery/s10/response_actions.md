# Response-conditioned actions and worst-case query fees

**Codex (GPT-6), October 14, 2026. DEVELOPMENT derivation.**

cp02 showed little fee benefit from optimizing prefixes beyond the cheap fixed
threshold order. Its ordinary mirror ties; adaptive depth-three planning for a
fixed action has more compilation cost and a shorter horizon. A materially
different next direction is to precompute the feasible action returned after
each answer, so that an answer unfavorable for one action can favor another.

Let A be a finite source-checked set of feasible three-copy actions, not merely
the selected initial action. At a partial observation h define
U(h)=min_{a in A} max_{v in V} sum_i (a_i-3v_i)c_i^*(h,a,v), with c_i^* the
appropriate box endpoint. A source-complete V makes this exact for menu A;
a source-complete A makes it the global integral three-copy minimax value.
An action attaining U(h)<=tau is an executable no-more-audits response.

For a depth-limited policy, compute both ordinary expected-fee and worst-fee
values, allowing immediate relevance-aware fallback F(h):

```math
V_E(h)=\min\{F(h),\min_i[c_i+\sum_t p_i(t)V_E(h\cup(i,t))]\},
```

```math
V_W(h)=\min\{F(h),\min_i[c_i+\max_t V_W(h\cup(i,t))]\}.
```

At a certified closure both are zero; at the horizon use F. All query choices
must satisfy the same preliminary-spend cap. A worst-fee policy with V_W(root)
strictly below the initial full-information price supplies a distribution-free
fee improvement on the declared response alphabet. Continuous intermediate
costs need their own cover proof; checking only five sampled values is not
automatically a continuous guarantee.

The fixed-action obstruction explains why this may differ from cp02. If some
feasible competitor attains initial regret above tau, choose each coordinate
at that competitor's worst endpoint. Every observation leaves its pairwise
regret unchanged; the fixed action never closes even after all costs are known.
With a discounted full-information bundle, buying any preliminary coordinate
on that path can exceed the immediate-bundle fee. Choosing a different feasible
action after the observation can avoid that obstruction. This is ordinary
contingent decision making, not a new general stochastic-control principle.

For a precomputed policy, source/action optimization is paid once per retained
node rather than once per request. Memoize exact observation states and charge
that retention. This trades an upfront bill for smaller online bills; evidence
must include its amortization horizon. A cheap adaptive-action heuristic, a
complete ordinary action search and the compiled ordinary mirror remain controls.

For continuous cost answers, a fixed action's closure region for one queried
coordinate is an interval (from min-marginals). A finite menu gives a union of
such intervals. It is therefore possible to certify coverage of all answers
by sorting interval endpoints and checking no gaps, with a feasible action
attached to each interval. Such an interval policy can have a stronger scope
than a five-value response tree, but response partitions and conditional laws
must not be confused. Future queries may depend on actual observed values;
constant-action interval certificates safely cover whole cells without assuming
their centers or endpoints are representative for unproved objectives.

## A finite lifting criterion for one continuous query

For this integer three-copy duty, integer tolerance and integer unobserved box
endpoints, each fixed-action response interval has endpoints on the grid 1/6:
every active constraint has integer intercept and slope in {-3,-2,-1,0,1,2,3}.
Consequently the 48 cells of width 1/6 partitioning [-4,4] suffice. If an action
certifiably closes at a cell midpoint, its interval endpoints are grid points,
so that same action closes throughout the whole closed cell. Conversely a
universal cover must close at each midpoint. Thus universal one-query closure
is equivalent to a feasible closing action at those 48 midpoints. This is an
exact lifting argument for this arithmetic domain, not a generic grid test.

A guided compiler may query an exact robust-action proposer at the midpoint of
the leftmost currently uncovered cell, add the returned action's full interval,
and repeat. It either covers the whole domain in at most 48 proposals or finds
a midpoint whose exact optimal regret exceeds tolerance, proving that this
coordinate cannot universally close. With a smaller proposal cap, remaining
gaps are simply unresolved. The proposal is logical computation, not a purchased
cost observation. Pricing it is essential: source models and globally optimal
triple search can be much more expensive than executing the final one-query tree.

For m copies the analogous grid uses lcm(1,...,m), and rational tolerances or
box endpoints require a further denominator. The resulting grid can grow
rapidly; do not claim polynomial dependence on m or arbitrary numerical input.
This criterion uses the interval form and exact arithmetic proved above;
checking arbitrary endpoints or five response samples without it is insufficient.
