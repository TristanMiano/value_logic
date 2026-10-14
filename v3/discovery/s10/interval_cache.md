# Reusing positive and negative decision certificates across answers

**Codex (GPT-6), October 14, 2026. DEVELOPMENT derivation.**

The [s07 ambiguity floor](../s07/ambiguity_theory.md) already establishes
adversarial-mixture lower bounds and their acquisition meaning. The present
direction is a cheaper two-witness relaxation and response-interval reuse;
the minimax/Jensen principle is inherited ordinary mathematics.

Let v,w be two checked feasible binary repairs, a any feasible m-copy counts,
and [l,u] the current contrast box. Their two pairwise-regret inequalities
imply that any action's worst regret is at least their average. Relaxing the
action coordinates independently to [0,m] gives the valid lower bound

```math
2R^*\;\geq\;m\sum_i h_i(l_i,u_i;v_i,w_i),
```

where h_i=2 min(0,u_i) for v_i=w_i=0,
h_i=-2 max(0,l_i) for v_i=w_i=1, and
h_i=min(u_i,-l_i) when v_i differs from w_i. Clamp the final lower bound at
zero if desired. This bound needs only two original-source feasible witnesses;
it does not need a complete model list, a mean-objective oracle, or knowledge
that the action relaxation is feasible. Relaxing can only weaken the lower.
It applies to every integer m-copy action and its convex relaxation, but not
automatically to an outside replacement option with a different cost function.

For a symmetric box [-H,H], it becomes mH/2 times the witnesses' Hamming
distance. After one latent true-cost query t, while other coordinates remain
symmetric, a differing queried coordinate contributes (m/2) min(t,H-t).
For m=3,H=4 and a distance-12 pair, querying a differing coordinate gives
66+(3/2)min(t,4-t). It exceeds tolerance 66 for every interior t. Thus many
source-action searches after that first observation are provably unable to
close, even though further observations can help.

Each h_i is nonincreasing when its cost interval shrinks. Precompute a bank of
witness pairs and update only changed coordinates; stop looking for a new
action when any pair's lower exceeds tolerance. This does not prove the chosen
next audit is cheapest. Pair selection and updates are priced computations.

For a single prospective affine interval query, each changed h_i is the minimum
of two affine functions of its answer. Therefore the set where this fixed pair
proves R*>tau is an interval given by two strict inequalities. Retain that
negative interval with the pair, source identity, exact prior observation state
and query map. A positive interval similarly retains a feasible action and its
two endpoint regret checks. On a later request with exactly the same prior
state, an answer lying inside a retained positive interval closes; one lying
inside a negative interval skips further action search and continues acquiring
information. Observed values outside both intervals remain unresolved.

For positive certificates, derive the affine inequalities against the complete
source model set or an admitted source upper cover. For negative certificates,
two feasible witnesses suffice. Strictness at negative endpoints matters;
equality at tau cannot rule out a valid action. A cache keyed only by the last
answer, ignoring preceding observations or source identity, is unsound.

In lp02, exact state caching had only four hits on 2,886 opportunities. Interval
reuse can generalize a paid computation to many distinct values, but only after
the actual proof is constructed and checked. Unlike an offline universal policy,
it need not pay for hypothetical branches never encountered. This is ordinary
proof/region caching and must face that explicit comparator with equal evidence.
