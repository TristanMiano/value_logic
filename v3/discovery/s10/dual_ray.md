# Retaining a multiplier ray instead of one scale

**Working DEVELOPMENT derivation; Codex (GPT-6), October 14, 2026.**

A dual that is tight at the initial objective can be weak after receipts.
For the source x1 OR x2, a supplied one-copy action (1,1), initial [0,4]^2
and the cut multiplier 4, the initial regret upper is 4. Multiplier 1 gives
the weaker initial upper 7. After both costs are observed as 1, however, scale
4 supplies only the zero-clamped lower 0 and regret upper 2; scale 1 supplies
lower 1 and the exact regret 1. An initially tighter certificate is not a
pointwise stronger certificate over all later objectives.

Retain the checked aggregate b dot v >= K and allow any nonnegative scale t:

```math
L_t(q)=tK-\sum_i\max(tb_i-q_i,0).
```

For the nonnegative feature-cover cuts used here, b>=0 and a feasible original
action proves K<=sum b_i. Therefore L_t is concave and piecewise linear in t,
with breakpoints q_i/b_i for b_i>0. Its eventual slope K-sum b_i is nonpositive.
An optimum is attained at t=0 or one of those breakpoints (a final flat interval
causes no difficulty). Exact rational arithmetic checks the chosen scaled
multiplier through the original admitted cuts. No new logical acquisition is
required. This is the ordinary one-row LP/Lagrangian bound, equivalently a
fractional covering-knapsack calculation; it is not a new duality principle.

For q_i=a_i u_i+(m-a_i)l_i, define the ray regret upper as U-max_t L_t(q),
also allowing lower zero. It is at least as strong as any one retained scale.
Each fixed-scale bound is monotone under interval refinement, so their pointwise
minimum is monotone too. The audit reduction is no longer one fixed additive
score; do not reuse the single-certificate cover theorem without an additional
construction or restrict planning to a fixed scale.

For the finite exact-observation model {0,2,4} from initial [0,4], coordinate
q_i has only four possibilities: 4a_i, 0, 2m, 4m. Thus every future optimum on
one retained ray is among at most 4n+1 prospectively enumerable scales. This
provides a finite certificate portfolio before request outcomes. Common zeros
and repeated ratios shrink it. A prefix chosen for any one member retains the
same physical-fee upper guarantee if the runtime also checks the other members.
All scale enumeration, rational representation, planning and checking must be
paid; a large denominator can make integer-score convolution expensive.

This may remove some fallback proof calls caused only by a stale multiplier
scale. It cannot recover missing source cuts, fix an arbitrary weak aggregate,
or replace a full LP with a universal equal-quality guarantee. Compare with
the existing ordinary retained-cut LP and with the already strong threshold
controller before treating a numerical tightening as a resource improvement.
