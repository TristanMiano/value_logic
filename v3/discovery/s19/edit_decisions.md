# What sharp source-coupled edit contrasts decide

Codex (GPT-6), October26,2026. DEVELOPMENT; analytical consequence.

Let action a choose a stipulated edit with setup charge q_a and inner optimum
V_a(theta), all evaluated on the same retained conditional source F. The
loss is q_a+V_a(theta). For a finite list of actions, the exact worst-case
regret of a deterministic action is

    R(a)=max_b [q_a-q_b+max_(theta in F)(V_a(theta)-V_b(theta))].

The maximum with b=a includes0. Interchanging the two finite/supremum
maxima proves the formula. Thus the pair-contrast construction gives exact
deterministic minimax regret without identifying theta, absolute optima,
or a unique optimal action for every source. Pairwise conditional endpoints
are sufficient for this duty. The cost includes every pair query actually
performed, its face optimizations, subset work and source checking.

## Worked decision rather than just an interval

Use the earlier t in[0,1] example: original G=min(2t,1/2), edited
F=min(t,1/2). The improvement D=G-F ranges over[0,1/4]. For edit fee
q=3/20, the original action's worst regret is1/10 and the edited action's
is3/20. Exact deterministic minimax regret therefore selects the original.
A controller retaining only separate sharp value intervals plus monotonicity
has D in[0,1/2]; its analogous minimax rule selects the edit instead. On the
actual source its worst regret is3/20, versus1/10 for the coupled rule: a
1/3 reduction in this constructed worst-case criterion. This is not an
observed fee saving or superiority over ordinary source-aware case analysis,
which obtains exactly the same sharp interval and decision.

If randomization is allowed and the source does not react to the private
coin, choosing the edit with probability p has worst expected regret
max(p*q,(1-p)*(1/4-q)). Balancing gives p=2/5 and regret3/50. The marginal
interval controller instead uses p=7/10; its actual worst expected regret
is21/200. The relative reduction is3/7. The payoff units, source domain and
minimax criterion are stipulated; this tiny arithmetic is not a general
performance claim or new minimax theorem. Advice/computation charges would
have to be included before making a practical cost comparison.

For more than two actions, a matrix of sharp pairwise extrema need not
suffice for randomization. The adversary must select one common theta for
the entire mixture. Summing separately worst pairwise differences can be
strictly loose. A separate common-source separation problem is required;
the scalar bottleneck DP does not automatically solve it.

For a concrete information counterexample, take three actions with loss
vector either in A={(1,0,0),(0,1,0),(0,0,1)} or in
B={(1,1,0),(1,0,1),(0,1,1)}. Both sources have every individual interval
[0,1] and every distinct pair's sharp difference interval[-1,1]. Every pure
action has regret1 in both. In A, a mixture p has worst regret max_i p_i,
minimized at1/3. In B it has worst regret max_i(1-p_i), minimized at2/3.
Thus even all those sharp pairwise intervals lose a factor2 distinction in
the optimal mixed regret. This uses finite logical sources (exactly one or
exactly two true bits); it is not an impossibility for retaining their full
source constraint or joint payoff set.
