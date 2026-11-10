# R1.5 Reinforcing judges by weighted vindication: convergence and concentration

**Author:** Claude (Fable 5.2). **Date:** November 10, 2026. **Cycle:**
[P4-R1-C001](../notebook/P4-R1-C001/record.md), session 3 (cycle unfinished).
**Theses:** C5, C2. **Builds on:** [R1.2](R1_judges_without_oracle.md),
[R1.4](R1_transfer_geometry.md). **Status:** a short proof from the
Perron-Frobenius theorem and exact computations on small worlds, by one
model; not independently reviewed.

## What this shows

R1.2 described which *sets* of judges are self-consistent. Here judges carry
graded weights, and a judge gains weight when its judgments are borne out by
judges who themselves carry weight. This is the essay's "good judgers have
more valuable judgements," and its question of why assigning value to values
does not "go absolutely wild."

- **It does not go wild: the weights converge** (Theorem 12(i)). Judges
  whose approvals are never borne out across performances, the random, the
  fashion followers and the pure conventions, drop to zero in one step.
- **When the traits that judges track are connected in the population, the
  limit is unique, does not depend on the starting weights, and keeps every
  trait-tracking judge** (Theorem 12(iii)). Connected means: one can pass
  from any such judge to any other through pairs whose approvals of
  different performances of a performer are dependent. By R1.4 this is a
  statement about the transfer geometry of the domain.
- **When they are not connected, weight concentrates on one family and the
  rest go to zero** (Theorem 12(ii)). The winner is the family whose members
  bear each other out most strongly, not the one that is most right. In the
  example with a reputation judge beside two outcome trackers, the
  reputation judge takes all the weight when it is consistent enough and
  none when it is not.

So the essay's remark that the dimensions of excellence "are connected" is
not only an observation about trees. It is the condition under which a
society that reinforces its judges recursively keeps all of its competent
judges instead of collapsing onto its most self-consistent family.

## 1. Setting and result

Assume B1 and B2 of R1.2 and fix a delineation $`c`$. The **vindication
matrix** is

```math
M_c[j,l]=I\bigl(A_{j,1};A_{l,0}\mid c_1,c_0\bigr),
```

the information that judge $`j`$'s approval of one performance carries
about judge $`l`$'s approval of another performance of the same performer,
given both labels. It is symmetric, because the two performances are
exchangeable, and non-negative. $`M_c[j,j]>0`$ exactly when $`j`$'s own
approvals are dependent across performances. The **vindication graph**
joins $`j`$ and $`l`$ when $`M_c[j,l]>0`$. Weights are updated by

```math
w\;\mapsto\;\frac{M_c\,w}{\|M_c\,w\|_1}.
```

**Theorem 12. Evidence: proved; computed in eight worlds.**

- **(i)** From any starting weights with $`M_cw\ne0`$ the iteration
  converges, provided that among the components of the vindication graph
  that carry starting weight one has a strictly largest Perron root. A judge
  with a zero row has weight zero from the first step.
- **(ii)** The limit is the Perron vector of that component and is zero
  outside it.
- **(iii)** If the vindication graph on the judges with nonzero rows is
  connected, the limit is the same for all starting weights that touch it,
  and is strictly positive on every such judge.

*Proof.* A symmetric non-negative matrix is block diagonal over the
components of its graph, and each block is irreducible. Under B1 and B2 a
judge whose approvals depend on any other judge's across performances also
depends on its own, so each block has a positive diagonal entry and is
primitive. By the Perron-Frobenius theorem the powers of a primitive block,
normalised, converge to its positive Perron vector, at the rate of its
Perron root; across blocks the largest root dominates. $`\square`$

The step "depends on another's, hence on its own" holds because a nonzero
covariance between $`\tilde k_{j,\kappa}`$ and another kernel forces
$`\tilde k_{j,\kappa}`$ to vary with the traits, and then its variance, the
covariance with itself on the same cell, is positive.

A count-based version, in which each judge accumulates credit earned from
the current shares, was run alongside and approached the same limits in every
world (it is a replicator dynamic with the same rest points; no proof is
given here).

## 2. Computations

[weights_dynamics.py](../notebook/P4-R1-C001/weights_dynamics.py), at each
world's true delineation, from uniform starting weights. Roots in nats.

| World (from R1.2) | Components and Perron roots | Limit weights |
|---|---|---|
| A. Trackers, fashion pair, random | trackers 0.054 | trackers one half each; others 0 |
| C. Two domains on independent abilities | domain 1: 0.004; domain 2: 0.013 | domain-2 judges one half each; domain-1 judges 0 |
| C with abilities weakly correlated | one component | domain 1: 0.016 each; domain 2: 0.484 each |
| C with abilities more correlated | one component | domain 1: 0.107 each; domain 2: 0.393 each |
| F. Trackers and a reputation judge approving at 0.9 / 0.1 | trackers 0.054; reputation 0.222 | reputation 1; trackers 0 |
| F with reputation at 0.7 / 0.3 | trackers 0.054; reputation 0.013 | trackers one half each; reputation 0 |

In world C the judges of domain 1 are accurate and are still driven to zero,
because the two domains' abilities are independent and domain 2's judges
bear each other out more strongly. A modest correlation between the
abilities joins the components and both families survive, with weights that
grow with the strength of the connection.

## 3. Limits and named obligations

- **Fixed delineation.** The delineation is held at the true one. When it is
  instead set by the weighted judges, concentration feeds back: judges at
  zero weight stop contributing distinctions, which under pure
  specialisation removes the labels that would vindicate them (R1.2). The
  coupled dynamics are not analysed.
- **One update rule.** Rules in which credit does not depend on the
  creditors' weights (plain vindication, as in R1.2) do not concentrate.
  Which rule a real community follows is an empirical matter. The result
  says what recursion on weights adds: convergence, and concentration when
  the domain is disconnected.
- **Predictability is not validity,** as in R1.2: the winning family is the
  most mutually predictable one.
- **C5.** This is a convergence statement for one linear rule of recursive
  valuation. It is not a general theorem on value drift and says nothing on
  self-trust in the Löb sense.

## 4. Closest established work

The update is eigenvector centrality on a weighted graph, as in PageRank and
related ranking methods, and the proof is the Perron-Frobenius theorem; both
are quoted from memory. What is added is the choice of matrix, vindication
across a performer's reappearances instead of agreement or endorsement, the
identification of its components with independent families of tracked
traits, and the reading of connectedness as the condition for pluralism.
