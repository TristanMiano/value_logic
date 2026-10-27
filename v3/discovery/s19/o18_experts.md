# A stronger mistake-count comparator with a costly representation

Codex (GPT-6), s19 DEVELOPMENT. This is a specialization of existing
reward-class learning, not a new algorithm claimed by this project.

[Joshi et al., Learning to Answer from Correct Demonstrations,
Algorithm1 and Sections4.3--4.4](https://arxiv.org/html/2510.15464)
provide a mistake-unaware update for arbitrary demonstrations. Its reward
class may have several optimal responses. Thus the strict-refinement
obstacle in o18_reductions.md does NOT rule out this stronger method.
We reconstruct the binary specialization with a fixed parameter, avoiding
any need to know C or to tune a regret bound after seeing it.

## Exact potential calculation

Maintain positive weights w_h, initially1. Choose the feasible response B
maximizing the total weight of reward hypotheses accepting B. After report
A, multiply each weight by

    (3/2)^[h rejects B] * (1/2)^[h rejects A].

Partition weights by acceptance of B and A. The increase in total weight is

    (W_rejectB_acceptA - W_acceptB_rejectA)/2
      - W_rejectB_rejectA/4 <= 0,

because B maximizes accepted weight. For any fixed h, its final weight is
(3/2)^M_h * (1/2)^C_h. Since the total is at most N, this gives

    M_h <= (ln N + C_h ln2)/ln(3/2).                 (E1)

This holds pathwise for arbitrary contexts and reports. There is no mistake
bit, corruption ceiling or stochastic noise assumption in this calculation.

## Instantiation on O18's domain

Let H contain every weak order of d named elements. For a matroid context M,
h accepts exactly its utility-optimal bases. This set depends only on the
weak order, by matroid greedy optimality. Every actual real utility vector,
including ties, is represented. Each weak order can be encoded by its
canonical consecutive ranks in {0,...,d-1}, so N<=d^d. Every context has a
feasible optimal basis and its maximal binary reward is1. The actual h has
C_h<=C; M_h is exactly the number of truly suboptimal choices. Therefore

    M <= 2.466304... * d ln d + 1.709511... * C.

For d=1 there are no mistakes. This is an ordinary, budget-agnostic,
tie-compatible, horizon-independent polynomial mistake bound, with better
asymptotic dependence on C than O18's stated count. It substantially narrows
any claimed delta. The useful question is computational implementation.

## Resource boundary

Directly listing weak orders takes exponentially many hypotheses. Even
restricting to strict orders already gives d! possibilities. Evaluating one
hypothesis on one proposed base is possible with a forward greedy solve and
an exact comparison; this does not make the weighted acceptance maximization
over all feasible bases an ordinary *linear* matroid optimization problem.
Its objective is a weighted sum of optimal-base indicator functions.

An explicit exhaustive implementation can enumerate bases and hypotheses;
that is a valid but expensive comparator. We have not established a hardness
result for a better implementation, nor proved that no compressed algorithm
can attain E1 efficiently. O18's cubic path work, quadratic oracle calls,
and logarithmic-in-T counter storage remain its plausible useful distinction.
The general existence of finite polynomial mistake bounds with ties and
unknown C is already supplied by E1 and must not be presented as O18 novelty.

A serious next novelty question is whether the reward-class update admits
an efficient implementation or a known efficient relaxation for these
matroid-optimal-base indicator rewards. Generic weighted-majority terminology
alone does not answer that representation question.

## A concrete obstacle for the generic acceptance oracle

The generic weighted acceptance maximization is NP-hard even on a uniform
matroid with a polynomial list of two-level weak orders. Given a simple
graph G=(V,E) and k>=2, take rank-k bases on V. For each edge e={i,j}, put
both endpoints in the high utility group and all other vertices in the low
group. A rank-k base is optimal for this weak order exactly when it contains
both endpoints. Unit weights therefore make accepted weight equal to the
number of edges induced by the chosen k vertices. Its maximum is
k*(k-1)/2 exactly when G contains a k-clique. This is the ordinary densest
k-subgraph objective, not a new complexity problem.

This proves a limitation of a *generic* weighted-reward optimization oracle.
It does not prove that the particular weights reachable from a uniform prior
over every weak order are hard, and it does not exclude other algorithms.
That reachable-state question remains separate. Even linearity already fails:
with rank2 and two rewards whose high groups are {1,2} and {3,4}, the
acceptance scores of bases12 and34 sum to2, while scores13 and24 sum to0.
A linear element-weight objective would give equal sums for those pairs.
