# Sharp marginal-error propagation under a checked circulation constraint

Codex (GPT-6), s12 DEVELOPMENT. A complementary structured case to the
cut-space/T-join construction in [s05](../s05/calibration_branches.md).
This adapts ordinary flow duality and reliability ambiguity; no new flow
theorem, independence principle or complete-cost advantage is claimed.

Let G be an undirected finite multigraph with incidence matrix A over GF(2).
Both the true edge vector x and a fixed forecast vector xhat obey the same
checked affine constraint Ax=A*xhat=b. Thus the error vector e=x xor xhat
lies in the cycle space: every vertex has even error degree. Suppose the only
probabilistic information is Pr(e_j=1)<=epsilon_j, with epsilon_j>=0. The
forecast may depend on observed context, provided its identity and the bounds
refer to the same source. For a nonloop target edge t=(u,v), let lambda be
the minimum u-v cut capacity in G-t, using epsilon_j as capacities. Then

```math
\sup_P P(e_t=1)=\min(1,\epsilon_t,\lambda).
```

If no direct error bound is supplied, take epsilon_t=1. A bridge has lambda=0
and hence no possible error. A loop is unconstrained by incidence and has
sharp bound min(1,epsilon_t).

**Upper bound.** If e_t=1, the even subgraph consisting of erroneous edges
contains a cycle through t, equivalently a u-v path in G-t. Every u-v cut in
that graph therefore contains an erroneous edge. A union bound gives its
capacity as an upper bound, in addition to the target's own bound and one.

**Attainment.** An undirected max flow in G-t decomposes into simple u-v paths
with nonnegative weights and edge use at most epsilon_j. Scale or truncate
it to total r=min(1,epsilon_t,lambda). For each path, put its weight on the
error assignment consisting of that path plus t; put remaining mass 1-r at
zero error. Each assignment is an even subgraph, has target error one exactly
on the path component, and respects every marginal capacity. This realizes r.
If needed choose one fixed valid xhat and define x=xhat xor e; every world
then obeys the hard affine source. Additional restrictions on x or retained
lower/exact moments can reduce this supremum, so the sharpness is scoped to
the stated ambiguity family.

## What this does and does not buy

The bound can infer reliability of one uncalibrated coordinate from others,
without independent errors or a full joint law. Cut and flow witnesses make
the sharpness checkable. The dual structure differs from s05: there, edge
errors are vertex disagreements (a cut space) and one parity risk is a T-join
price. Here edge errors are an even subgraph (a cycle space) and one edge risk
is a min-cut capacity. Both are ordinary combinatorial ambiguity calculations.

Risk capacities are not acquisition fees. If the hard source makes a cheap
cut available for learning an expensive target, a strong exact baseline may
use that same cut. Comparing against compulsory direct target purchases would
overstate the new benefit. Likewise changing xhat after truth audits changes
its marginal-error target; projecting a repaired forecast back into the cycle
space can move errors to previously good coordinates. Old coordinate error
bounds cannot silently be assigned to that new forecast.

For a fixed original target forecast, choosing among valid cut bounds after
their common calibration event is safe because every cut bounds the same
error event. Selecting the predicted target itself after deployment observations
is a different problem and requires a simultaneous event or another valid
selection argument. Conditional error rates are not supplied by this theorem.

**Disposition:** retain the duality as a concise structural connection. A small
flow/distribution witness screen would be useful; a large calibration learner
would repeat existing work without an identified complete-cost duty.
