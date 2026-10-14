# An exact cheap cover for one replacement duty

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The expensive generic decision-region table can be avoided for a concrete
subfamily already exposed in op01: replacement price A, anchor in {0,A},
H=5, positive weighted exactly-one star, and tolerance tau=HW, W=sum weights.
Assume A>=2HW. All source node costs lie in [0,H]. Query fees are positive.

If the anchor is observed at A, replacement has regret0. If it is observed
at0, the balanced action (one copy per endpoint on every edge) has worst
repair regret HW and upper cost2HW<=A, hence meets the complete duty.
Thus **either anchor response completes the duty**.

If the anchor is unobserved, replacement cannot meet the tolerance when
A>HW, because the compatible all-zero node/anchor world has optimum0.
(Once some node costs are observed, the lower star optimum is at most2HW;
for the op01 value A=10HW it remains below A-HW at every state.) A repair's
combined bound is max(R,U), where U is its absolute star upper cost: the
unknown high anchor cancels the replacement price. Since the star optimum
is nonnegative, R<=U. Consequently the duty is feasible without the anchor
iff some source repair has upper cost at most HW.

Let u_v be the observed node cost, or H if unobserved. The minimum possible
upper cost is **exactly** 2 sum_i w_i min(u_0,u_i), realized by choosing the
smaller-upper endpoint in both components of each edge. Upper extrema are
simultaneously attained at the single Cartesian upper cost vector, so this
does not exchange incompatible maxima. Define an observed score d_v=H-u_v.
Then the exact terminal condition for A=10HW is

```math
g(s)=\min\left\{HW,\;2\sum_i w_i\max(d_0,d_i)
                 +HW\,\mathbf{1}_{\text{anchor observed}}\right\}=HW.
```

Each fixed world's item-state realization gives nonnegative node scores.
For each edge, the maximum acquired endpoint score is monotone submodular;
its second score can only add the excess above the current maximum. Sum,
positive scaling, and truncation at the quota preserve this property. The
anchor contributes the full quota regardless of its value. The function is
observable and all items guarantee coverage. Under the explicitly given
independent cost source, ordinary expected-gain-per-fee greedy therefore
falls under stochastic submodular cover. These are the hypotheses checked
locally; Hellerstein et al.'s [2021 cover theorem](https://arxiv.org/html/2102.01149)
is established prior art, not a new approximation claim.

The general replacement gap counterexample in observation_policy.md remains
valid. This specially constructed cover utility is different from that gap,
and applies to a specific price/tolerance/anchor relation. It does not justify
applying a submodular bound to all op01 duties or correlated cost models.

## ac01 finite screen and possible paid follow-up

First check the exact terminal equivalence on **every** partial state of the
four exposed op01 sources at price A/tolerance HW, using the full partial-star
action frontier as a comparison. Check every one-step pointwise diminishing
return inequality for distinct unobserved coordinates and all their supported
responses. Compare greedy's exact expected and worst fee by a finite decision
tree, with all policies checked against original source actions. No physical
queries in ac01. If this screen shows a useful computation/fee tradeoff,
declare and execute a paid service with fresh request identities and the
ordinary equal-interface mirror; otherwise preserve the negative screen.
