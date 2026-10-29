# An observation bound must name its baseline

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT clarification/extension.
The frozen observation_value.md theorem and first result remain unchanged.
Its B(J)-Q(J) compares the **best constant action** with the best contingent
policy. The informal advice to reject a costly observation using that bound
requires that the incumbent is already optimal, or that this ideal baseline
is explicitly the intended comparison. The formula is correct at its stated
baseline; using it for an arbitrary current action would be a scope error.

## A concrete failure of the broader interpretation

Let two possible cells have losses(fast,fallback)=(0,1) and(10,1). No cell
is yet known attainable, and at least one is possible. A truthful signal
distinguishes the cells. For every nonempty support J, B(J)-Q(J)=0:
if the hazardous cell is present, both best constant and contingent worst
losses are1; otherwise both are0. Thus the sharp ideal-baseline value is0.

The current fallback action nevertheless has loss1 even when the true
support contains only the safe cell. A contingent fast-if-safe policy then
has loss0. Hence zero ideal-baseline information value cannot justify
rejecting every positive-fee observation relative to this incumbent.
Computing that the hazardous cell is impossible would also allow the fast
action, and may be cheaper. The two routes require their own costs.

## Exact incumbent upper value

Fix an incumbent a. Define

    U_a = max_(K subset J subset P, J nonempty) [W_a(J)-Q(J)].  (I1)

This is the largest total improvement from replacing that incumbent by an
optimal contingent policy, over signature-compatible supports. It includes
any improvement obtainable just by choosing a better constant action;
it is not the observation's pure incremental value. A safe coarse bound is

    U_a <= Gamma_a + U,                                      (I2)

where Gamma_a is the sharp computational gap from refinement_gap.md and U
is the ideal-baseline observation bound. This follows by adding
W_a-B and B-Q pointwise in J. Their separate maxima need not occur at the
same J, so(I2) can be strict. If Gamma_a=0, U alone is a valid upper bound.

There is an exact calculation without the full-action cover DP. For each
candidate post-observation threshold t in the finite set of loss entries,
form every signal's legal branch actions h as in observation_value.md:
all known cells in that signal must have v_jh<=t. The option's allowed cells
are A_sh(t)={j in P_s:v_jh<=t}. If any signal has no legal option, discard t.
Otherwise let

    M_a(t)=max_(s,h legal,j in A_sh(t)) v_ja,

omitting thresholds for which this collection is empty. Then

    U_a = max_t [M_a(t)-t].                                  (I3)

For an upper bound, take any J, let t=Q(J), and choose an optimal action in
each nonempty branch (arbitrary legal actions in empty branches). Every cell
of J is allowed, so W_a(J)<=M_a(t). Conversely choose an option and cell
attaining M_a(t), use that option in its signal and any legal option elsewhere,
and take J to be the union of the allowed sets. It contains K and that cell;
W_a(J)>=M_a(t) and Q(J)<=t. These two directions prove(I3), including its
attaining signature support. It is nonnegative because an observation policy
can ignore the signal and retain the incumbent.

For one incumbent, direct evaluation takes O(|V|*c*m) scalar work, where c
is the number of possible cells, m the action count and |V| the number of
distinct loss entries; membership/known-cell checks are charged too. Evaluating
all m incumbents adds at most a factor m. No report-parameter resource claim
or standalone novelty claim is made. This is elementary finite robust
optimization using the established information contract already cited.

## Sound decision use

If a proposed observation plus its policy computation costs a fixed fee at
least U_a, it cannot strictly improve the current action's true worst loss
net of that fee under the declared contract. It can have other benefits
outside this single-use calculation; those were excluded explicitly.
An implementable policy optimized on P has loss at most Q(P), so when K
is nonempty, max(0,W_a(K)-Q(P)) is a guaranteed lower bound on its robust
improvement before fees. With K empty use0. A large upper value alone does
not recommend acquisition, and a signature support is not an original-source
witness. The scalar problem's source premises and signal accuracy remain
upstream requirements. Use this incumbent-aware wrapper for cost decisions;
retain the ideal-baseline calculation as a separate benchmark.
