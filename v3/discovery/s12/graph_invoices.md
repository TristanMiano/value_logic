# A cut certificate turns the parity price theorem into a graph service

Codex (GPT-6), s12 DEVELOPMENT derivation and finite graph probe.
This uses ordinary cut/cycle duality and max-flow/min-cut, with the private
invoice price from [parity_price.md](parity_price.md). It is distinct from
s05's T-join bound for calibrated vertex-prediction errors.

## Capacity two makes character prices additive

With episode cap H=2, positive coordinate fees c_i and reset overhead f>=0,
the exact full-source parity price is

```math
\Phi(T)=\sum_{i\in T} w_i,
\qquad w_i=c_i+\min_{j\ne i}c_j+f.
```

This includes the empty and singleton targets. Thus on a checked affine source,
the exact optimum is a weighted minimum representative in the target's dual
coset. This is still hard in general; the formula is not an optimization oracle.

## One unknown edge in an affine circulation source

Let hidden Boolean edge labels x obey A*x=b over GF(2), where A is the vertex
incidence matrix of a known undirected graph and the affine source is nonempty.
Fix a non-loop edge e=(u,v). For every vertex set U,

```math
\bigoplus_{i\in\delta(U)}x_i=\bigoplus_{z\in U}b_z.
```

The dual space is the cut space. Representatives of the edge target are
T={e} symmetric-difference delta(U). If the cut does not contain e, T contains
e and has weight at least w_e. If it contains e, U separates u from v and
T=delta(U)\{e}. Therefore the exact optimal invoice price is

```math
\min\{w_e,\ \text{minimum weighted u-v cut in G-e, with weights }w_i\}.
```

A selected cut is a short algebraic witness for the alternative parity; its
offset is the known parity of b on U. A feasible u-v flow with the same value
as that cut certifies minimum cost. A loop is independent of the incidence
equations and must be queried directly. A bridge is already determined by b;
the corresponding cut in G-e has value zero.

Known edge receipts can be incorporated by giving already observed edges zero
capacity and moving their values into the offset. They remain available as
paid marker purchases in private episodes, so the original c_i still determine
the weights of unknown coordinates. Equivalently remove their columns and
update b, while remembering all marker options. The min-cut price describes
remaining acquisition from that public receipt; it does not refund earlier
purchases or pay for source admission, optimization and checking.

## A constructed nontrivial representative

Take vertices u,v,z_1,z_2,z_3, a direct edge e=(u,v) with fee 100, and three
two-edge u-z_j-v paths, all with fee one. Let b=0. The three path bits are free,
while x_e is their parity. With H=2 and f=0, direct recovery costs 101.
A cut next to u in G-e has three edges of weight two; three disjoint paths
each support flow two, proving minimum cut six. Querying those three path
bits through separate private invoices recovers x_e with worst invoice six.
This is 95 fewer fee units in a constructed example. An ordinary controller
using the same graph and invoice interface obtains the same six.

The graph relation does substantive work here: it replaces an expensive
unresolved bit with a parity of three independent cheaper bits. Its acquisition
or verification is not included in those six units. No application runtime or
population-level economic benefit is established by this example.

## General targets retain a computational obstruction

For target S=all edges, a representative is E\delta(U). With unit original
fees and f=0, its price is twice the number of uncut edges. Computing the exact
invoice optimum would therefore compute a maximum cut. This is the familiar
weighted coset-decoding obstruction in a concrete graphic instance. The
single-edge task is polynomial because it reduces to an ordinary separating
cut; arbitrary parity tasks do not inherit that tractability.

## Rely on one relation when the graph model is fallible

Now suppose A*x=b is a model assumption and let e_z=(A*x-b)_z be its Boolean
violation at vertex z. For a proposed cut U, the decoded edge answer is wrong
exactly when the parity of (e_z)_(z in U) is one. On a connected graph with a
feasible b, every violation vector has even total parity. If justified marginal
bounds Pr(e_z=1)<=epsilon_z are all that is known, the sharp worst failure
probability of that cut relation is

```math
R(U)=\min\{1,\ \sum_{z\in U}\epsilon_z,
                 \sum_{z\notin U}\epsilon_z\}.
```

Both sums are upper bounds because an odd cut-side violation requires at
least one violation on each side. Sharpness: put total mass R(U) on patterns
with exactly one bad vertex on either side, using a transportation coupling
that respects the marginal capacities; put remaining mass on no violations.
Each even violation pattern is realized by some edge assignment on a connected
graph. Degenerate empty sides have zero risk. This is ordinary reliability
optimization, not an independence assumption.

For a cut chosen before the current instance is seen, this task-specific risk
may be far below the bound for the entire graph model being correct. Choosing
cuts after current-instance observations requires more care: separately small
marginal cut risks do not give a simultaneous selection guarantee.

One conservative adaptive option fixes a vertex region W in advance with
sum_(z in W)epsilon_z<=alpha and permits only cut certificates with U subset W.
Every erroneous accepted cut then entails some violation in W, regardless of
adaptive cut selection or stopping. The unconditional error probability is at
most alpha. Minimum acquisition cost within that proof region is an ordinary
u-v cut with vertices outside W forced to the opposite side. This is a
restriction, not the unrestricted cheapest risk-constrained cut. Calibrating
epsilon, selecting W from current data, conditioning the error claim and
paying for graph/source verification remain separate obligations.

## Next cheap screen

Compare cut prices with exhaustive affine-character representatives on small
graphs, including loops, bridges, unequal fees, offsets and known receipts.
Check the proposed cut/flow certificates independently of the optimizer, then
execute invoice decoding on a small set of exact circulation worlds. Inspect
coding/graph inference and reliability antecedents before assigning novelty.
This is development of a concrete tractable adapter, not another large learner
sweep or a claim that max-flow is a new value-logic algorithm.

## Finite screen and closest conventional methods

[graph_probe.py](graph_probe.py) passed on 37 graphs, 289 consistent receipts
and 1,655 target requests, including loops, bridges, parallel edges, affine
offsets, unequal fees and known coordinates. Cut/flow feasibility and equality
were checked separately from the augmenting-path optimizer. Direct enumeration
checked 7,969 candidate representatives and 9,547 world/decoding pairs. The
constructed six-unit alternative was attained. [The saved output](graph_probe.json)
reports 470 cut routes, 729 already-known targets and 456 direct routes;
0.1847186 seconds is only the small probe's runtime, not a service speedup.
The marginal-risk and trusted-region extensions have not been executed.

Gopalan et al.'s [locality paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/r-d-codes.pdf),
Section 2/Definition 2 and the following dual-codeword hypergraph, supplies
the conventional local-recovery viewpoint. Bruck and Naor's
[1990 paper](https://www.wisdom.weizmann.ac.il/~naor/PAPERS/hardness_of_decoding_ieee_paper.pdf),
Section II/Facts 1–2, Lemma 1 and Proposition 1, explicitly connects cut codes
to decoding and gives the same all-ones/MaxCut reduction. Neither local repair
nor that hardness argument is new. The present adapter uses the derived
invoice weights and prices its restricted observation interface; priority and
usefulness of the complete package remain open.

For an implementation seeking a safe saving rather than a proof of global
optimality, any checked cheaper cut suffices. Conversely a feasible flow with
value at least the direct price certifies that direct recovery is optimal,
without finishing a larger max-flow computation. Finding and checking those
certificates still costs work. This is ordinary primal/dual early termination.
