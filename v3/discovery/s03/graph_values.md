# S20: observation graphs and robust value

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.
Extends S18's alternative-observation question while preserving S13Q's
weighted coordinate-prediction objective. No source or runtime superiority claim.

## A physical query interface with alternatives

There are n Boolean facts x_v. A node query reveals x_v at nonnegative fixed
cost a_v (it may be unavailable). An edge query reveals x_u XOR x_v at
nonnegative fixed cost c_e. Each query is pure, exact, and charges once. Terminal
actions guess each fact independently, earning sum_v w_v 1[guess_v=x_v], w_v>=0.
Normalize sum w<=1 when a bounded score is needed. Query availability and prices
are supplied, not inferred for free from a logical problem.

Under the uniform law on all bit assignments, an observed edge graph has one
fair flip per connected component without a node observation. A component with
an observed node is fully known. Thus a terminal query set has optimal utility
base + sum of r_v over anchored vertices, where base=sum w/2 and r_v=w_v/2.
This is independent of the observed labels. An adaptive policy's expected net
utility is the expectation of that set function minus purchased-query costs;
it cannot exceed its largest fixed-set value. The maximizing fixed query set
attains that value. Nonuniform beliefs generally invalidate this argument.

The same number is the **minimax expected utility over arbitrary fixed truth
assignments**, if terminal randomization is permitted. Upper bound: any policy's
worst-world expected utility is at most its average under the uniform law, hence
at most the preceding optimum. Lower bound: buy an optimal fixed set, predict
anchored facts exactly and use a fair random flip for each unanchored component.
Every world's expected score is exactly base+covered prizes. Randomization is
operational; this is not a proof that the agent believes all worlds equally.
Known additional logical constraints can make this conservative uncertainty
set loose. Optimality for a smaller constrained set is not asserted.

Cycles carry redundant parity information and can be deleted at no loss when
costs are nonnegative. Multiple anchors in the same selected component are also
redundant. For general physical graphs, add a supersource with edges of cost a_v
to the anchorable vertices. A purchased anchored forest becomes a connected
rooted subgraph with node prizes r_v. This is the ordinary rooted
prize-collecting Steiner-tree objective (equivalently charge penalties for
uncovered vertices). This identifies a strong comparison, not a new optimizer.

## Exact dynamic program for a physical tree

Root the physical tree arbitrarily. For each subtree keep three values:

- N: its root is uncovered, and all covered components are internally anchored.
- U: its root component is tentatively covered but has no internal anchor;
  it must be connected to an anchor above. Its prizes are already included.
- A: its root component is covered and internally anchored; all other covered
  components are also anchored.

Initialize N=0, U=r_v, A=r_v-a_v (A invalid if no anchor). For each child with
edge price c, write C=max(N_child,A_child). Simultaneous updates are

```
N' = N + C
U' = U + max(C, U_child-c)
A' = max(A + C, A + U_child-c, A + A_child-c, U + A_child-c).
```

Invalid states are omitted. The root answer is max(N,A), not U. The N state
can omit all edges in its uncovered component because they have no terminal
value and nonnegative cost. Every other option either separates a closed child
subtree or connects its root component, whose anchor status gives the recurrence.
Conversely every recurrence option constructs the stated type, proving exactness
by induction. Multiple-anchor options are harmless, though some are dominated.
Backpointer records for constant many choices per child give O(n) arithmetic
operations/storage and a selected plan in O(n). Bit complexity of rational
arithmetic is separate; copying sets at every node would spoil the stated bound.

An independent plan check uses connected components and purchased anchors to
recompute prizes and all query costs. It checks feasibility/value, not global
optimality by itself. Optimality comes from the recurrence/proof or a checked DP
certificate, which remains a possible development.

## Cheap development probe, before exposure

Build an exact-rational implementation and save its source hashes. Fresh seed
64283: 32 trees with n=2..6, nonnegative prices, absent anchors and varying
weights. Compare all edge/anchor subsets and (on the smaller first 12 cases)
explicit uniform-world belief Bellman planning. Check truth-dependent guesses.
Then time source construction, tree DP and plan checking separately for path,
star and random trees of 4096 nodes. Use the identical ordinary tree algorithm
as the strongest named control: no false speedup against a huge Bellman table.
Costs are supplied synthetic query prices; this does not measure real proof
acquisition. These are developmental sanity checks, not final confirmation.

Open: uncertain runtimes, fallible/missing query results, constrained truth
sets, nonuniform forecast improvements, general graphs, paid source validation,
and a useful mathematical-workload instance. An exact toy interface alone does
not meet P3-POS01. Keep the minimax and Bayesian interpretations separate.

## Observed development and comparison

The initial Python probe and its one unchanged retry failed before a result
artifact was written: native exit -1073741819, then an unexplained generator
TypeError. [Versioned amendment](graph_amend.md) preserves these outcomes and
ports the same input draws and methods to Node. [Amended result](graph02.json):
32 trees, 6,216 subset checks, 12 Bellman cases with 3,986 states, and 744
world-specific expected-score checks agree exactly. The 4,096-node path/star/
random examples attain normalized gains 0.1447/0.1842/0.1645 over baseline.
Construction took 3.36/3.47/3.92 ms, DP 10.55/7.88/11.66 ms and feasible-plan
checking 0.29/0.56/0.80 ms. Prices and labels are synthetic; no external proof
acquisition was timed. This supports the implementation at exposed scope only.

[Goemans and Williamson (1995)](https://math.mit.edu/~goemans/PAPERS/GoemansWilliamson-1995-AGeneralApproximationTechniqueForConstrainedForestProblems.pdf),
sections 4.3 and 4.3.1, defines the rooted edge-cost-plus-uncovered-penalty
objective and gives a primal-dual algorithm. I read the formulation, dual,
algorithm and theorem statement on pp. 310–313, not its entire proof. This is
the relevant general-graph comparison. The tree recurrence here is reconstructed;
no algorithmic novelty is assigned to ordinary dynamic programming.

Own consequence: writing R=sum r and minimum penalty objective C*, graph gain
is G*=R-C*. A multiplicative approximation C<=alpha*C* only gives
G>=alpha*G*-(alpha-1)*R. It need not ensure any positive gain when G* is small;
the empty acquisition gives gain zero. For profitable-computation stopping,
use an instance-specific lower bound on C* to upper-bound G*, not a bare
cost approximation ratio.

## General-graph upper certificates, reconstructed

Use the augmented graph with root 0 and anchor edges. For subsets S excluding
0, choose finitely supported y_S>=0. Require sum_{S: edge crosses S} y_S<=c_e
for every physical or anchor edge. Also supply allocations z_{S,v}>=0 for v in S
with sum_v z_{S,v}=y_S and sum_S z_{S,v}<=r_v. These allocations imply
sum_{S subset T} y_S<=sum_{v in T} r_v for every T; all constraints can be checked
from the supplied finite support. Therefore LB=sum_S y_S is a lower bound on
C*, and R-LB is an upper bound on the value of further acquisition.

Direct proof: split supported cuts into those whose S lies entirely in the
uncovered set T and all others. For every other S, a covered vertex in S has a
path to the root, so a purchased edge crosses S. Edge constraints pay at most
the tree's edge bill. The first group is paid by the allocated prizes in T.
Together LB<=cost+uncovered prizes for every feasible plan. This requires no
trust in a proposed optimizer. Feasible acquisition supplies a lower gain;
their difference bounds decision regret under the declared model.

The allocation condition is also complete for the finite-support penalty
constraints: a bipartite flow sends y_S from each set node to its members,
whose capacities are r_v. Any set-node family has union T and demand at most
sum_{S subset T}y_S<=sum_{v in T}r_v, so the max-flow cut conditions hold.
This is a standard transport feasibility argument, not a new duality theorem.
Membership size and checking costs must be paid; a dense certificate can be
larger than the graph. No implementation or speedup for this certificate yet.

## Prices that are forecasts rather than exact runtimes

For a fixed selected batch with authenticated per-query bounds l<=cost<=u,
using u in the tree DP gives an achieved worst-world lower guarantee. This
does not require a runtime probability law. At l, the DP gives an optimistic
upper bound for the fixed-batch class. The same upper bound covers adaptive
policies only if their observation interface supplies no extra information
beyond purchased labels. Timing, failures or partial progress can reveal other
facts and invalidate that upper-bound argument. Conservative price bounds
alone do not erase information leaked by cost observations.

Fallible model forecasts can guide choice inside a separately certified cost
box or between guaranteed plans. Learning narrow bounds and charging actual
query execution remain outstanding; a freely supplied cost interval is not
an answer to the self-modeling question.
