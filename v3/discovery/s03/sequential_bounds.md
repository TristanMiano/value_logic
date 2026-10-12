# S13S: restoring sequential acquisition constraints

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

The [matching obstruction](adaptive_bounds.md) shows that a common terminal
baseline cannot enforce every query-order constraint. It does not invalidate
the upper bound; it prevents treating that restricted family as complete.

## Local potentials

Let s=(A,v) be the actual partial assignment and f(s) the best conditional
terminal utility. For each unqueried bit j, write s+,s- for its children. The
ordinary finite Bellman equation is

    V(s)=max(f(s), max_j[-q_j+(V(s+)+V(s-))/2]).

Any function h with h(s)>=f(s) and
h(s)>=-q_j+(h(s+)+h(s-))/2 for every available j is an upper potential.
For a query, define Delta_h=h(child)-(h(s+)+h(s-))/2. Its conditional mean is
zero. Along any feasible query path, subtracting these increments from the
terminal utility and query charges gives, by telescoping, at most h(root):

    terminal - sum q - sum Delta_h
      <= h(root) + sum_queries[-q_j+E(h(child)|s)-h(s)]
      <= h(root).

The exact V gives equality on its own optimal choices. A local supersolution
can therefore provide an upper certificate that respects sequential state,
including the matching example. Finding a compact h is a substantive task;
writing down an exponential table is not an efficient general solution.

## Finite frontier composition

A valid pointwise bound H0(s)>=V(s), such as a conditional closure bound, need
not satisfy all Bellman supersolution inequalities. Do not infer the above
martingale certificate from admissibility alone. Instead compose a finite
proof graph with explicit frontier bounds. At a frontier use L=f(s), U=H0(s).
When expanding a state, compute

    L_new=max(f(s), max_j[-q_j+(L(s+)+L(s-))/2]),
    U_new=min(H0(s), max(f(s), max_j[-q_j+(U(s+)+U(s-))/2])).

Every available query must have children or an explicit valid child bound for
the upper rule. Any subset suffices for the lower rule. The upper Bellman
operator is monotone, so these remain sound. A lower-policy witness chooses
the maximizing query and eventually stops at the frontier. Increasing a
uniform depth monotonically raises L and lowers U; depth m is exact. A bound
U-L limits the loss of that concrete policy at the same start state.

This is conventional bounded dynamic programming. The potential contribution
is a useful compact closure/rank initializer and checked reuse in the value
service; it is not a new Bellman algorithm. McMahan, Likhachev and Gordon
(2005), *Bounded Real-Time Dynamic Programming*, already maintain upper/lower
values and focus work on relevant states with large gaps. Its
[author-hosted introduction](https://www.cs.cmu.edu/~ggordon/mcmahan-likhachev-gordon.brtdp.pdf)
and primary abstracts were inspected as comparison leads. Full implementation
and theorem comparison remain to be done before a material superiority claim.

## Costs and next development

The graph-bound computation, baseline proposal and each checked child expansion
are paid metacomputation. No source makes their expected future value free.
Cache canonical substituted value polynomials and query tariffs only when they
are bound to the same semantics; changed prices can reuse polynomials but need
updated Bellman inequalities. Side-effectful probes require the operational
state and transition charges of S11, not this pure-coordinate model.

Use the four-bit obstruction to confirm the local repair cheaply. Then compare
closure initialization with an ordinary perfect-information bound and a simple
coefficient bound under equal complete planning costs. A small frontier is only
useful if the savings exceed its more expensive initializer. Keep this economy
question separate from correctness of the finite recurrence.

## Targeted repair outcome

[frontier01.json](frontier01.json) explicitly reuses the matching fixture and
six earlier random cases. All depth bounds contained the exact oracle and
refined monotonically; full depth was exact. In the matching problem, the
closure initializer gives upper 0.97 at the root, versus 0.99 for ordinary
perfect information minus the cheapest first query, and 1 for a coefficient
bound. After three levels, closure and the perfect-information initializer both
reach the exact upper 387/400; their lower policy values remain 169/200 until
level four. Thus the sequential repair resolves the earlier unavoidable gap.

The complete cold-call timings favor the simple control in this tiny case:
full-depth coefficient initialization takes 7.769 ms, perfect information
18.303 ms, and closure 66.831 ms. At depth three closure takes 65.747 ms versus
16.839 ms for perfect information. The extra root tightness did not yield an
economic benefit in this uniform-depth prototype. This negative result argues
against using a costly closure initializer indiscriminately. Adaptive frontier
selection, reuse and larger sparse problems are different hypotheses that
require their own complete-cost development, not a reinterpretation of this run.

## Compact special-purpose flow advice

For a single closure no-gain certificate, an even simpler witness suffices:
nonnegative charges f_{e,i} on prerequisite incidences with
sum_{i in e}f_{e,i}=r_e and sum_{e containing i}f_{e,i}<=q_i. Every completed
term is fully charged to purchased prerequisites; hence every batch's reward
is at most its price, and the adaptive bound is zero. These are ordinary
bipartite-flow feasibility constraints. A partial feasible allocation of total
F gives an upper bound sum_e r_e-F, even without proving flow optimality.
An untrusted cheap allocator can therefore offer a useful certificate before
running full max flow. A repriced tariff preserves a witness if each capacity
still holds. Revealing bits and removing sunk prices generally does not; the
new conditional problem needs its own checked allocation.
