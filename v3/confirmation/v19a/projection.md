# P3-11-A1: reconstruction by product-cell projection

Codex (GPT-6), October 28, 2026. Same-model mathematical confirmation work,
under the prospective plan. This unit is a proof reconstruction, not a claim
that the whole confirmation stage or its protected floor is complete.

## Start with the ordinary exact disjunction

Let K={1,...,k}, I={1,...,n}, n>=1. Write g_ji(x_i)=c_ji dot x_i+d_ji.
The observation a_j<=min_i g_ji(x_i)<=b_j is equivalent to

    (for every i, g_ji(x_i)>=a_j)
    and (there exists i, g_ji(x_i)<=b_j).

The existential witness need not be the minimizing block. That distinction
matters when the observation has positive width. Ties impose no consistency
requirement on the choice of witness across different observations.

Define Q_i(T) by retaining the original B_i, every lower inequality and the
upper inequalities indexed by T. For every function alpha:K->I let
T_i=alpha^(-1)(i) and P_alpha=product_i Q_i(T_i). Empty factors give an empty
product cell. The conditioned source X is the union of P_alpha over all
alpha. To prove X subset union, choose one upper witness separately for
each observation at the given source. To prove the reverse inclusion,
use the assigned witness for each j and all lower inequalities. This is
an exact ordinary disjunctive formulation with at most n^k branches.

For a nonempty Q_i(T), compactness gives attained finite extrema ell_i(T)
and u_i(T) of f_i. Convexity and affinity give every value between them:
interpolate the two extremizers. Thus the local image is exactly
[ell_i(T),u_i(T)]. This step is local; X itself need not be convex or connected.

## Project each branch before compressing the disjunction

On a feasible product branch, local scalar choices are independent and range
over intervals A_i=[ell_i,u_i]. Their minimum has the exact image

    [min_i ell_i, min_i u_i].                                  (P1)

Necessity is immediate: each coordinate is at least the smallest ell_i,
and a coordinate attaining the smallest u_i bounds the minimum above.
For sufficiency, choose q in this interval and choose i with ell_i<=q.
The upper inequality q<=min_j u_j gives q<=u_i. Set the anchor coordinate
to q and every other coordinate to its available upper extremum u_j.
The minimum is q. Local extremizers and interpolation lift these scalar
choices to an actual source. No assumed global continuity fills a gap.

Consequently the completely explicit ordinary answer is the union of the
intervals (P1) over all feasible alpha. This route already solves the problem,
but enumerates the observation-to-block functions. The proposed compression
can now be verified as a rearrangement of this exact finite formula.

For a fixed q, membership is equivalent to

    exists a feasible partition (T_1,...,T_n):
       (exists i: ell_i(T_i)<=q) and (for every j: q<=u_j(T_j)).

Choose the existential i first and then its assigned subset T. Its own
conditions are q in [ell_i(T),u_i(T)]. Outside, the remaining condition is
that some feasible partition of K minus T has all upper extrema at least q.
If there is at least one such outside partition, the finite collection of
its bottleneck upper values has an attained largest element C_i(K minus T).
Existence of an outside value at least q is equivalent to q<=C_i(K minus T).
If there is no feasible outside partition the existential is false.

Thus the complete answer is precisely the union of

    [ell_i(T), min(u_i(T), C_i(K minus T))]                     (P2)

over nonempty local slices with nonempty displayed interval. This proves
AR1 by finite logical rearrangement of the independently derived branch
projection, rather than assuming the anchor formula as a starting point.

## Boundary conventions checked explicitly

- With one block, only T=K has an available outside partition. Its outside
  value is +infinity, the neutral value of a minimum over zero operands.
  Any nonempty remaining observation set is impossible to assign outside.
  Formula(P2) returns precisely the image of Q_1(K).
- With no observations, each block has only its empty-subset slice. Formula
  (P1) gives one interval [min_i ell_i(empty),min_i u_i(empty)]. Formula(P2)
  has the same union, including the one-block/no-observation case.
- Degenerate local intervals require no division. The only admissible
  anchor value is its shared endpoint, attained by the supplied point.
- A globally inconsistent source can have many nonempty local slices.
  It has no feasible full partition. Its branch union and AR1 union are
  both empty; no single omitted or empty slice is used as a shortcut.
- All comparisons are non-strict. Tied extrema, shared endpoints of output
  intervals, and tied old-observation witnesses are included exactly.

## Premises that carry the proof

The product premise is necessary for the simultaneous choice of outside
maximizers. For example, impose x_1+x_2=1 with each marginal in [0,1], no
observations and f_i(x_i)=x_i. The true minimum range is [0,1/2]; applying
the independent-marginal construction would return [0,1]. Arbitrary
cross-block correlations cannot be silently absorbed into local bounds.
The observation correlations themselves are retained by the disjunction.

Exact local scalar images are also necessary. With one block whose scalar
image is {0,1}, replacing it by [0,1] creates unattainable interior values.
Convexity and affinity are sufficient conditions for the local image
property, not a claim about general fallible-model parameter sets.

Attainment is used in the reverse implication. An open local interval
(0,1) has neither endpoint source, so reporting [0,1] would be wrong.
The compact rational-polytope premise supplies attainment. The exact
certificate checker can sometimes establish bounded attained images
without checking compactness, but that does not weaken the theorem's
stated domain or establish a new general-domain contribution.

## Ordinary equivalence and the surviving distinction

The branch union, the anchor formula, and the set-semiring inside-outside
reconstruction compute the same set under the same information. An ordinary
implementation of(P2) ties exactly. The meaningful algorithmic distinction
is how the full finite disjunction is evaluated and represented, with the
resource proof still to be checked; it is not that classical reasoning
cannot preserve model uncertainty or detect inconsistent observations.

This unit finds no substantive defect in the fixed projection claim. Its
conclusion is a mathematical reconstruction at the declared assumptions,
not a final novelty decision or an empirical performance result.
