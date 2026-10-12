# S11C: values sufficient for choosing computations

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; Q2/Q3/Q4/Q5, S04/S11 lineage.
The [mutable-cache example](stateful_cf.md) motivates a constructive repair.
This is an elementary finite control/abstraction construction. Material utility
and novelty are unestablished; P3-POS01 remains outstanding.

## Retain relative values and the cost of changing their baseline

Let X be a covered finite set of hidden program states. Terminal actions A
have known rational costs c(x,a). Diagnostic e has known cost q(x,e), observed
symbol o(x,e), and deterministic successor t(x,e). Include every observation
available to the controller, such as an observed execution bill, in o. The
controller otherwise observes neither x nor its following normalization.
Use a stipulated prior and at most H diagnostics before a mandatory terminal
action. Unknown real program semantics or prior calibration are outside this
conditional construction.

Define b(x)=min_a c(x,a), r(x,a)=c(x,a)−b(x), and

    q*(x,e)=q(x,e)+b(t(x,e))−b(x).

For every diagnostic path x0,...,xk and final action a, telescoping gives

    sum_i q(xi,ei)+c(xk,a)
      = b(x0)+sum_i q*(xi,ei)+r(xk,a).

This equality is pathwise, including adaptively selected diagnostics and
stopping. Averaging under any fixed initial prior subtracts the same E[b(x0)]
from every policy. Hence minimizing transformed expected cost preserves all
policy rankings. The controller must keep the original observation function;
revealing the model-dependent transformed charge would change its information.
Transformed charges may be negative. The finite horizon makes this harmless
for the recursion, but no unbounded termination claim follows.

For the uniform cache example, initial E[b]=−1/3. The first raw probe changes
cached's baseline by 9, so its expected transformed charge is 3. The resulting
partial-information terminal regret is 1/3. Their sum, with initial baseline,
is the actual cost 3. A second observation removes that regret but leaves the
baseline harm, giving 8/3. A complete restoration removes the harm and permits
zero terminal regret, giving −1/3 before its price. The information and state
effects are thus represented separately without treating either as free.

## A finite continuation partition

Partition X initially by identical terminal regret vectors r(x,·). To refine
one level, key each state by its existing block together with, for every
available diagnostic e,

    (q*(x,e), o(x,e), block(t(x,e))).

All diagnostics are assumed available everywhere; a varying action menu must
also be part of the key. Repeat to stability, retaining exact rational values.
There are at most |X|−1 strict increases in block count. At stability, r and
q* are constant on each block, and each diagnostic has a well-defined
observation and successor block. This is an observation-preserving deterministic
bisimulation construction after a potential transformation, not a newly
claimed control principle.

Aggregate the prior mass of each block. For a chosen diagnostic, sum masses by
the block's observation, then move each mass to its successor block and
normalize within the observed branch. This agrees with aggregating the original
Bayesian successor belief: states in the same block have the same observation
and destination block. Immediate transformed expected charges also agree.
Induct on remaining horizon: terminal costs agree at zero; for every diagnostic,
the immediate charge and each observation branch's recursively optimal expected
cost agree. Taking the minimum over terminal actions and diagnostics preserves
the optimal value and the full set of tied first choices at every H.

The untransformed optimal expected cost is E[b(initial)]+the quotient value.
This constant need not be identifiable to choose the policy, but it is needed
to report absolute cost. Thus values can discard some belief information while
preserving choices only if the retained object is closed under the contemplated
computations. Equal current value vectors alone are insufficient.

At finite H, H refinements already supply sufficient depth-indexed blocks;
the implementation will use the stable partition for simplicity. Refinement
requires the paid transition/observation table. It can leave every state
distinct, and the quotient still has a continuous belief space and branching
planning cost. No generic compression or computational speedup follows.

## Antecedents and next development

Ng, Harada and Russell, [ICML 1999, §3 Theorem 1 and Corollary 2](https://people.eecs.berkeley.edu/~russell/papers/icml99-shaping.pdf),
establish policy-preserving potential-based reward transformations in their
MDP setting, with discounted or proper absorbing undiscounted assumptions.
The terminal-normalized cost identity here is a finite pathwise use of the
same telescoping algebra; it does not import their learning-speed findings.
The hidden-state observation restriction and quotient need the separate
argument above. Ordinary state abstraction is the closest remaining comparison.

Next cheap development: implement exact belief recursion and the partition;
compare original and transformed quotient values on generated finite systems
and the cache example. Include a family with removable nuisance offsets and
a family where terminal-only merging fails. Charge construction as well as
request cost before suggesting that retained values buy a resource benefit.

## Developmental prototype outcome

[continuation.py](continuation.py) implements exact rational belief recursion,
potential normalization and the stable partition. [continuation01.json](continuation01.json)
matches original, normalized and quotient optimal values and tied first choices
on 120 generated finite systems with horizons 0–3. This is a cheap finite check,
not independent reconstruction of the argument or empirical transfer evidence.

On a deliberately duplicated nuisance-offset family, 512 states reduce to two.
Construction took 2.3689 ms and the quotient request including belief aggregation
0.2696 ms, versus 7.4211 ms for the explicit original-state request. Both visited
seven beliefs; only their state-vector width changed. This supplied finite
table excludes semantic acquisition and is exactly the redundancy that ordinary
potential normalization and aggregation can remove. It is not a new superiority
claim. General random systems usually retain all states.

The cache system has five states (live, empty cache, cache 0, cache 1, frozen).
Two current-regret classes split to four continuation classes. Cache 0 and
frozen can merge for the stated diagnostic menu; live and empty cache cannot.
The expanded menu adds a zero-binding probe, beyond the first toy's fixed
one/two/restoration alternatives. The optimal two-probe policy first binds 0,
making the empty cache hold 0; next it binds 1. That second observation separates
live (return 1) from cache/frozen (return 0). Choose terminal 0 for live and 1
otherwise. Under the uniform initial prior its cost is −2/3, better than the
paid restoration policy. The first probe has no immediate information gain;
its value comes from beneficial state preparation and later discrimination.

This is a changed, explicitly specified action menu. It neither contradicts
the earlier menu's optimum nor establishes how to discover real predictor
semantics. The stronger ordinary belief planner discovers the same sequence.
The useful research direction is a representation that preserves this
complementarity while retaining less than the full hidden-state probability
vector. A stable state partition is only one candidate; linear value-directed
belief compression is a stronger conventional comparator to inspect next.
