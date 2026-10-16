# A finite-response lifting for randomized interval regret

Codex (GPT-6), DEVELOPMENT derivation. This records a general explanation of
the restricted query/flip LP. It uses ordinary convexification, endpoint support
and LP duality. It is a candidate synthesis, not a claim to invent randomized
minimax regret or polynomial robust optimization.

## Contract

Let X be a finite family of feasible deterministic procedures. Its member x has
known fixed cost g(x) and response v_i(x) in a finite numerical alphabet A_i for
each i=1,...,D. The source supplies coefficients theta_i independently within
declared intervals [l_i,u_i]. Independence here means a Cartesian uncertainty
set; no stochastic independence of truths is inferred. The expected cost is

```math
C(x,\theta)=g(x)+\sum_i\theta_i v_i(x).
```

The controller chooses a private mixture of feasible procedures before theta
is selected; the adversary sees the mixture, not its realized random seed.
The comparator may select the best feasible procedure knowing theta.

Assume an exact finite extended representation Q={z>=0:Bz=b} for the convex
hull of the following observable procedure features. For each i,a there is a
linear nonnegative coordinate q_ia(z) such that deterministic x gives the
indicator 1{v_i(x)=a}; mixed points give its marginal probability. Also g(z)
is affine, and every Q point has a feasible procedure-mixture realization with
these same features and cost. A mere relaxation does not satisfy this premise.
Bounds/inequalities can be represented using nonnegative slack variables.

## Exact oracle and compact LP

For controller z put s_i=sum_a a*q_ia(z). For fixed comparator x, interval
maximization gives

```math
g(z)-g(x)+\sum_i\max\{\ell_i(s_i-v_i(x)),u_i(s_i-v_i(x))\}.
```

The maximum over x is unchanged by replacing deterministic x with Q, because
the expression is linear in comparator label indicators after the endpoint
support values are fixed. Introduce d_ia with

```math
d_{ia}\ge\ell_i(s_i-a),\qquad d_{ia}\ge u_i(s_i-a).
```

Write sum_ia d_ia*q_ia(y)-g(y)=h(d)^T y+constant. Its maximum over Q has
the ordinary LP dual min b^T lambda+constant subject to B^T lambda>=h(d),
where lambda is unrestricted. Minimize g(z)+b^T lambda+constant subject to
z in Q, the endpoint inequalities and those dual inequalities.

Exactness follows in both directions. Choosing true supports d and an optimal
dual gives the true worst-case regret. Enlarging d cannot reduce the comparator
maximum because every q_ia(y) is nonnegative; weak duality makes every feasible
dual an upper bound. Thus minimizing over z cannot understate minimax regret.
Assume Q has finite relevant optimum; ordinary LP strong duality then supplies
attainment. An affine g constant cancels between controller and comparator.

The formulation has the size of Q plus O(sum_i |A_i|) support variables and
constraints, apart from the feature-map incidence representation. With rational
data this is a compact LP when that representation and label count are compact.
This does NOT assert that any polynomial nominal linear optimization problem
has a compact Q or a small finite-response alphabet.

## Relation to prior work and the query/flip instance

[Mastin, Jaillet and Chin (2015)](https://www.mit.edu/~jaillet/general/rand_mmr_final.pdf),
section 3.2, Theorem 4 and (LPI), establish polynomial randomized interval
minmax regret for polynomially solvable binary combinatorial optimization.
Their convex-hull and separation framework is a direct antecedent. Our lifting
allows finite response labels and an explicitly supplied exact extended
polytope; it should be presented as an adaptation of that framework. A missing
search hit is not evidence of novelty.

For binary labels a in {0,1}, s lies in [0,1], so the support branch is fixed by
a. For labels {-1,0,1}, the a=0 branch can change at s=0. Naively treating
the positive and negative indicator costs as unrelated intervals destroys their
shared theta. The finite-response lifting keeps that dependence exactly.

In the paid query/flip instance, the response coordinate is (query cell z,
original sign i), its label is {-1,0,1}, and its coefficient includes p_z*w_i.
The realization flow supplies the exact procedure mixture and known fee row.
Terminal zero mass gives label 0; terminal-one mass minus flip mass gives +1;
flip mass gives -1. Conditional first-moment boxes are the uncertainty set.
This explains why the direct formulation is compact in m for fixed query
dimension r even though there are many feasible procedures and source corners.

The special top-k/Bellman epigraph in [direct_lp.md](direct_lp.md) is an explicit
dual construction of this idea for the operation menu. No general MDP hardness
result is contradicted: a policy's state visitation coefficient can take an
enormous set of values, and an exact response-label polytope may be intractable.
The small ternary alphabet and source-independent query flow do real work.

## Unknown query-cell masses

If p_z>=L_z>=0, sum L<=1 and sum p=1, the allowed mass vectors are the convex
hull of p^(j)=L+(1-sum L)*e_j. For a fixed controller, worst-case regret after
maximizing conditional interval means is convex in p: it is the supremum of
linear functions indexed by comparator and mean choice. Hence its maximum
is attained at one of these mass vertices.

Use one shared private-reach controller z and a separate support/dual block
for each mass vertex, with an upper variable dominating all block objectives.
This optimizes over mass uncertainty as well as conditional mean intervals.
The controller flow is independent of p; only cost/response coefficient maps
change. Zero-mass cells pose no conditional-probability division problem.
This extension is derivation only; the earlier mass probe checked a fixed
controller, not this optimization. It can multiply LP size by up to 2^r.

Acquiring justified lower masses and mean intervals still has a separate bill.
Neither the lifting nor the LP creates reliability for an arbitrary fallible
model. It enables useful conservative decisions conditional on those premises.
