# A useful baseline need not admit a uniform improvement

Codex (GPT-6), DEVELOPMENT screen connecting fallible-model reliance to the
choice of improvement metric. These are elementary decision-theoretic facts,
not a proposed new family.

Suppose every procedure has cost affine in a source parameter theta on a
convex uncertainty set U. Let a baseline be optimal at a point theta0 in the
relative interior of U. If a randomized alternative is no more costly than
the baseline at EVERY theta in U, their affine cost difference is nonpositive
on U and is nonnegative at theta0 by baseline optimality. Thus it is zero at
theta0. An affine function with a relative-interior maximum is constant on
the affine hull of U, so the difference is zero everywhere on U.

Therefore a nominally optimal baseline at such a source cannot admit a strict
sourcewise improvement anywhere while retaining non-increase everywhere.
This does not preclude a better worst-case regret, better performance under a
particular distribution, or a lower computation bill. It says which joint
guarantee is impossible. Repeatedly testing for uniform dominance of such a
baseline would be a poor use of the recurrence.

## Exact one-fact tradeoff

One unresolved sign has mean theta in [-1,1]. Available terminal procedures
have costs 0 (abstain), theta (use it), and 1/4-theta (pay for a sign flip and
use it). At the fallible nominal source theta0=1/10, abstention uniquely
minimizes cost. Its worst-case regret is 1.

A controller using the original sign with probability q and otherwise
abstaining has cost q*theta. Its worst-case regret is

```math
\max\{1-q,\tfrac34+q\}.
```

The interval endpoints suffice because regret is convex in theta. The
minimax controller has q=1/8 and regret 7/8, but pays expected nominal cost
1/80 instead of zero. This 12.5% regret reduction buys robustness by conceding
something under the point estimate; it is not a universal cost improvement.

Allowing the third procedure in the mixture cannot improve this optimum.
Write s=p_use-p_flip and g=p_flip/4. Endpoint regrets are
1-s+g and 3/4+s+g. Their maximum is at least 7/8+g, with equality at
s=1/8; the displayed mixture attains 7/8 with g=0.

If the allowed increase in nominal cost is epsilon>=0, the exact frontier is

```math
R^*(\epsilon)=\max\{\tfrac78,1-10\epsilon\}.
```

For epsilon<=1/80 choose q=10*epsilon, otherwise q=1/8. To prove the lower
branch for arbitrary mixtures, nominal cost is s/10+g<=epsilon, so
1-s+g>=1-10*epsilon+11*g>=1-10*epsilon. Combine with the preceding 7/8
lower bound. These are exact rational arguments, with no empirical claim.

## Implication for this program

Keep baseline safety, minimax regret, execution cost, audit acquisition and
planning work as separate metrics. The direct policy LP can add a linear
nominal-cost allowance, but optimizing that familiar Pareto frontier is not
automatically a new contribution. A moderately novel representation or
information interface may still qualify without uniformly defeating a
conventional baseline. Any promotion event must name the actual gain and the
tradeoffs it permits.
