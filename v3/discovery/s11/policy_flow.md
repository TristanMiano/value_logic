# A compact realization flow for the full randomized policy class

Codex (GPT-6), DEVELOPMENT candidate. Extends the query/flip menu and its exact
regret oracle. General sequence-form/occupancy methods and matroid polytopes
are established; the combined finite interface and its transport are the scope.

## Histories as partial assignments

A state h is a partial assignment of the r queryable original signs, with j
queried coordinates and k=H-j remaining operations. The postponement lemma
permits all flips at the terminal leaf. Query order adds no hidden information:
for a fixed full query cell z compatible with h, the probability (over private
policy randomness) of reaching h depends only on h's already observed signs.
It does not depend on which compatible z is true or on its probability mass.

Use *conditional realization weights*, not unconditional state probabilities.
Let t_h be that reach probability, y_hj the weight assigned to querying j next,
and u_h0,u_h1 the weights stopping with terminal actions 0 and 1. They satisfy

```math
t_{\varnothing}=1,\qquad
t_h=\sum_{j\in\mathrm{dom}(h)}y_{h\setminus j,j},\qquad
u_{h0}+u_{h1}+\sum_{j\notin\mathrm{dom}(h)}y_{hj}=t_h.
```

Only histories with j<=min(r,H) are retained; queries require k>0. A query
weight feeds BOTH labelled outcome children. This is not an ordinary probability
flow with total mass one across a whole level. Each full z selects one child,
and its own compatible-history tree has probability conservation. Adding cell
probabilities to these equations would change their semantics.

Given feasible nonnegative weights, at positive t_h choose the outgoing option
with probability its weight/t_h. Use any stopping action at an unreachable h.
Induction for every fixed z recovers the stated weights on all compatible
histories, and its terminal weights sum to one. This supplies a single
implementable randomized controller, valid for every query-cell distribution.

Conversely, sum any finite policy's private-randomness path probabilities over
query orders leading to h. The constraints hold. Averaging its outgoing choices
at each h yields the same realization weights for every full z, because all
paths to h depend only on values specified by h. Thus this Markovization
preserves every cellwise expected fee and terminal coefficient simultaneously,
even when the cell probabilities are uncertain. It is stronger than merely
preserving occupancy at one nominal probability law.

## Compressing the terminal subsets

Let v_hi be the weight of stopping with action 1 and flipping coordinate i.
The exact convex hull of allowed subsets is

```math
0\le v_{hi}\le u_{h1},\qquad \sum_i v_{hi}\le k u_{h1}.
```

For u_h1>0 this is the uniform-matroid independence polytope. Its vertices
are indicators of subsets of size at most k: if a feasible vertex had two
fractional entries they could be perturbed against each other; if it had only
one, a tight integral sum could not coexist with that fractional entry, and
a slack sum would permit perturbation. Therefore every feasible vector is
realized by a mixture of legal subsets. u_h1=0 forces all v_hi=0.

An execution sampler can use ordinary pairwise dependent rounding. Move two
fractional entries in opposite directions until one reaches 0 or 1, choosing
the two boundary moves with probabilities preserving each expectation. Once
at most one fractional entry remains, round it by a Bernoulli draw. The final
number of flips never exceeds k, and each marginal is preserved. This needs
no enumeration of the sum_{j<=k} binomial(m,j) possible subsets.

## Cellwise cost rows and a robust master problem

For full z, sum only compatible histories. Its expected terminal coefficient
for coordinate i and expected fee are

```math
s_i(z)=\sum_{h\preceq z}(u_{h1}-2v_{hi}),\qquad
C(z)=\sum_{h\preceq z}\left(\sum_j a_j y_{hj}+\sum_i f_i v_{hi}\right).
```

These are linear in realization weights and satisfy the original paid menu.
For a supplied source (p,mu), aggregate each term using P_h=sum_{z extending h}p_z
and unnormalized moments M_hi=sum_z p_z E[X_i|z]. Policy cost is

```math
\sum_h\left[
 \sum_j a_j P_h y_{hj}
 +u_{h1}\sum_i w_i M_{hi}
 +\sum_i v_{hi}(f_iP_h-2w_iM_{hi})\right].
```

The resulting realization polytope has O((m+r)3^r) variables/constraints for
H>=r, with fewer histories at smaller H. It is independent of p and mu.
Minimize a regret bound over this polytope, adding one linear constraint for
each adversarial source: policy cost minus that source's optimum <= bound.
The exact regret oracle separates a proposed realization plan after converting
it to cell rows. Thus one need not generate a new policy column every iteration.
General correlated uncertainty in means remains outside the current oracle.

For known masses use the box oracle; for the lower-mass simplex use its 2^r
vertex calls. Source mixtures give the ordinary best response after averaging
both masses and unnormalized moments. This provides exact lower bounds from a
finite scenario distribution, just as in the earlier double-oracle method.
Neither a numerical LP optimum nor a stopped iteration cap proves convergence.

## Numerical advice can still yield a sound policy

Convert each numerical state's outgoing choice to a valid common-grid
probability vector. For terminal flip marginals, clamp numerical advice to
[0,1], round downward on the same grid, and if necessary scale downward until
their sum is <=k. Then recompute realization weights from these valid local
rules. This may worsen performance, but it defines an admissible controller.
Recompute its exact robust upper, and a lower from a valid rational scenario
mixture. Their gap is valid independently of numerical primal/dual residuals.
Preserve original advice and report any lost accuracy or stalling.

Prospective screen: reuse the four declared query/flip duties, at most forty
scenario-generation iterations and gap tolerance 1/100000. Compare exact bounds,
variables, support sizes and source calls with the earlier double-oracle runs.
Check realization conservation separately for every full cell; test terminal
subset feasibility and keep the iteration cap rather than extending it silently.
