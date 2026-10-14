# General graphs: a cut certificate can support cheap decision cover

**Prospective DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The anchor-cover construction extends to any nonempty undirected graph with
positive integral edge weights. Each original edge still has two independent
exactly-one Boolean components. Different edges can share cost coordinates,
so the cost uncertainty need not factor by logical component. Node costs lie
in [0,H], edge-weight sum is W, and common mandatory anchor is in{0,A}, A=10HW.
Replacement price equals A. One balanced repair chooses each endpoint once.

Its exact repair regret in a cost world z is sum_e w_e |z_u-z_v|. This is a
convex function of the cost vector, with maximum H MaxCut(G) on the box.
Suppose an independently checked certificate gives MaxCut(G)<=K<=W. Fix the
requested tolerance tau=HK. If anchor0 is observed, the balanced action is
warranted: regret<=tau and cost<=2HW<A. If anchorA is observed, replacement
has regret0. Thus either anchor response terminates, even when computing
the exact graph MaxCut would be expensive.

Without the anchor, replacement cannot meet tau: the lower optimum is at
most2HW, so its worst regret is at least A-2HW=8HW>tau. A repair's worst
combined regret is max(R,U), with U its star-free absolute upper cost. The
source optimum is nonnegative, so R<=U. Minimize U separately in every
original exactly-one component. If u_v is the observed cost or H, the result
is exactly2 sum_e w_e min(u_v,u_w), simultaneously attained at the compatible
coordinatewise upper world. Hence the full stopping predicate is

```math
g(s)=\min\left\{Q,\;2\sum_{vw\in E}w_{vw}\max(d_v,d_w)
                 +Q\,\mathbf{1}_{\text{anchor observed}}\right\}=Q,
\quad d_v=H-u_v,\quad Q=2HW-\tau.
```

This is the same ordinary stochastic submodular cover construction as for
stars, with quota changed by a checked graph bound. It is observable,
pointwise submodular, integer valued and always coverable. With an explicit
independent source law, expected-gain-per-fee greedy has the established
cover guarantee. Query safety does not assume the probability model is
correct: every terminal check uses all admitted compatible cost worlds.
The expected-fee comparison does depend on the stated distribution.

## A cheap, source-bound upper certificate

Supply cliques C with nonnegative integral multipliers lambda_C, such that
each edge's total allocated multiplier does not exceed its original weight.
Let r_e be the remaining weight after these allocations. Then

```math
\mathrm{MaxCut}(G)\le
K=\sum_C\lambda_C\left\lfloor |C|^2/4\right\rfloor+\sum_e r_e.
```

For every cut, a clique with t vertices on one side contributes exactly
t(|C|-t)<=floor(|C|^2/4) crossing edges; each residual edge contributes at
most its weight. Sum these inequalities. Checking every clique edge,
nonnegative multiplier, residual capacity and claimed scalar suffices. This
is an elementary ordinary cut upper bound, not a new graph optimization
theorem. The empty clique list always gives K=W. A unit-weight full clique
has K=floor(n^2/4); a triangle gives K2 rather than W3.

The certificate must bind the original source edges and feature scales.
It cannot replace source admission, mandatory-anchor resolution, or physical
cost receipts. Paid acquisition of a more expensive graph certificate needs
its own invoice. A proposer can fail to find a tight clique decomposition;
the empty-list fallback remains valid with its looser declared tolerance.

**Prospective gc01 finite screen:** H=4; n2..6 paths, cycles, cliques and
seeded sparse positive-weight graphs (8141690). Propose one full clique when
available, otherwise a deterministic greedy triangle packing. Check the
certificate against every cut and reject over-allocation, non-clique and
changed-source mutations. For n<=4 enumerate every receipt state with
unobserved/0/2/4 node outcomes and unknown/0/A anchor. Compare the cover
predicate with every original action count vector and every compatible box
corner. Check all terminal balanced/replacement/upper-minimizing witnesses.
For larger cases use all cost worlds in{0,2,4}^n and selected observation
sets (empty, each singleton, all); evaluate original actions directly.
No physical audits are acquired in this mathematical screen.
