# Two-line source-complete response certificates

Codex (GPT-6), DEVELOPMENT, 2026-10-14.

The complete-model loops in rr01 are unnecessary for positive response intervals.
Use the already checked source diagram and signed min-marginals instead. This
is ordinary weighted decision-diagram dynamic programming, specialized to the
existing induced minimax-regret objective (Mastin et al.; Gilbert/Spanjaard).

For m-copy counts a and a box [l,u], write q_j=a_j u_j+(m-a_j)l_j.
When query i has affine endpoints l_i(t)=l0+l1 t, u_i(t)=u0+u1 t,
set q_i=0 and compute r_z=min_{v feasible, v_i=z} sum_{j!=i}q_j v_j.
Let A=sum_{j!=i}a_j u_j. The exact regret after answer t is the maximum
of the following two lines, omitting an infeasible z branch:

```math
R_a(t)=\max\{A+a_i(u_0+u_1t)-r_0,\quad
A-(m-a_i)(l_0+l_1t)-r_1\}.
```

Proof: for each fixed competitor bit z, separate its coordinate i from the
ordinary induced objective. Every remaining term is independent of t, so its
minimum is exactly r_z. Maximize over the two possible bits. This is valid for
all real answers in the declared query domain and any current box on the other
coordinates. It requires a source-complete minimization representation, not a
list of all source models. The initial diagram compilation and every marginal
evaluation still cost money/computation; neither is inherited for free.

Intersect the at-most-two halfspaces R_a(t)<=tau with the query domain.
For m=3 and latent queries of slope +1 or -1, nonzero slopes are integers of
magnitude at most three, so six-scaled integer endpoints suffice. This replaces
O(number of models * features) interval construction by O(diagram nodes +
features). The interval's cached source identity, prior observations, and query
map remain necessary. A negative interval still needs only two feasible models.

An action proposal can also use a bounded witness pool rather than a complete
list. Start with ordinary nominal extrema, propose a three-copy action by local
search on the pool, query the exact diagram for its worst competitor, add that
feasible competitor, and repeat under a fixed round/pool cap. Retain the best
exactly checked candidate across rounds. This is a bounded ordinary separation
heuristic. Its restricted-pool objective is not a global lower bound on the
full action problem; source completeness applies to the final upper check only.
No optimality claim follows from failure to discover another improving action.

Use the pool only as a proposal device and negative-certificate witness set.
Source completeness for a positive result comes from the diagram. This removes
the previous 64-model enumeration admission restriction, while retaining the
diagram-state cap and its possible exponential compilation cost. The next
transfer test should preserve capped admissions as failures, not silently drop
them from the claimed source denominator.
