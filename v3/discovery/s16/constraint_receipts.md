# Transporting model reliance through changed constraints

Codex (GPT-6), October 23, 2026. DEVELOPMENT; constructive extension.
This broadens the earlier graph-potential relation to polynomial feasible
sets. Algebraic ideals, real-radical certificates and error bounds are the
immediate conventional comparisons; generic novelty is not presumed.

## Affine tasks: only a quotient of the cost model matters

For a task with Hx=d, suppose true and cheap linear costs a,b obey
a-b=H^T phi. Then a^T x=b^T x+phi^T d on every feasible action. Their
optimizers agree even when individual coordinates of b are arbitrarily
wrong. If the constraints become H'x=d', H'=H+DeltaH, retain phi:

    a-b=H'^T phi+r,       r=-DeltaH^T phi.

On the revised feasible set, all ranking disagreement comes from r. If a
cheap-model optimum x_b has a certified gap gamma to every alternative,
and sup_{x,y feasible} r^T(x-y)<gamma, x_b remains truly optimal. More
generally its true regret is at most that oscillation. Computing its bound,
the gap and the new feasible solution costs work; they are not free inputs.

For a difference supported on a known coordinate set D, testing membership
in row(H) requires rank(K_D^T) independent scalar equations, where columns
of K span ker H. Rank-nullity gives

    rank(K_D^T)=|D|-rank(H)+rank(H_{complement D}).

This recovers the earlier graph cycle obligation count when H is an
incidence matrix. It is not a new rank theorem. The rule identifies the
relevant task equations instead of treating all coordinate errors equally.

## Polynomial tasks: exact agreement by an identity receipt

Let the old feasible set satisfy g_j(x)=0. Let e(x)=a(x)-b(x) be the
true-minus-cheap objective discrepancy. A retained identity

    e(x)=sum_j h_j(x)*g_j(x)                               (1)

proves exact agreement on that set. After g'_j=g_j+Delta g_j replaces the
constraints, every new feasible x obeys

    e(x)=-sum_j h_j(x)*Delta g_j(x).

Thus on a separately warranted common domain K,

    |e(x)|<=sum_j ||h_j||_K*||Delta g_j||_K.               (2)

If the old relation also has a known task-constant offset, subtract that
offset before applying these formulas; action rankings ignore it. Retained
symbolic multipliers can be expensive or large, and evaluating/range-bounding
them must be paid. An identity witness does not by itself establish a small
bound on an unbounded new domain.

Ideal membership is sufficient but not necessary for agreement on the real
feasible set. The example g=x^2,e=x has only x=0 feasible, so e vanishes,
but x is not a polynomial multiple of x^2. Reject an algorithm that treats
failure to find (1) as proof that the models disagree on feasible actions.

## Real-radical receipts give a different counterfactual rate

A more general sound certificate is a polynomial identity

    e(x)^(2k)+sum_l s_l(x)^2=sum_j q_j(x)*g_j(x), k>=1.   (3)

On the old real feasible set it implies e=0. On the new set, dropping the
nonnegative squares and bounding the remaining terms gives

    |e(x)| <= [sum_j ||q_j||_K*||Delta g_j||_K]^(1/(2k)). (4)

No feasibility, compactness or multiplier bound is inferred from the
identity alone. Supply those premises separately. Formula (4) follows by
substitution into (3), not by assuming smooth behavior of the feasible set.
If the new objective is also edited by Delta a-Delta b, add a warranted
bound on that discrepancy to (2) or (4).

For any revised feasible set, an epsilon bound on |a-b| gives true regret
at most 2epsilon for an exact cheap-model minimizer. If the cheap solver is
eta-suboptimal, the bound is eta+2epsilon. A strict cheap-objective margin
greater than 2epsilon preserves its unique optimal action. These familiar
optimization consequences need no probabilistic model calibration.

## The square-root rate is necessary in a small example

Take g(x)=x^2, e(x)=x, K=[-1,1]. Certificate (3) holds with k=1,q=1 and
no square terms. Replace g by g'(x)=x^2-t, with 0<t<=1. Old feasible actions
have e=0; new feasible actions x=+/-sqrt(t) have |e|=sqrt(t). Formula (4)
is exact. No uniform bound C*t works as t decreases to zero.

For true objective a=x and cheap objective b=0, choosing the positive root
has true regret 2sqrt(t), attaining the general regret bound. An arbitrary
choice among cheap-model ties therefore cannot be claimed robust merely
because the models agreed before the edit. This example prices no solver;
it establishes the necessary shape of a counterfactual guarantee.

## A bounded verification interface

For explicit rational polynomials, coefficient arithmetic can verify the
identities. A separately sound sum-of-squares decomposition uses exact
arithmetic or outward residual control; a floating optimizer's suggestion
is not a receipt. For exact polynomial evaluation oracles with a declared
degree bound, fixed candidate identities can also be checked by the earlier
private polynomial-identity protocol. Its one common failure event then
covers all later uses of that identity, including adaptive constraint edits
inside the certified domain. It does not grant new domain or degree facts.

This could retain a small proof of task-relative usefulness instead of a
fully accurate model. An ordinary symbolic optimizer given the same
certificate obtains the same bounds. Closest algebraic error-bound work,
natural priced examples, and the complete cost of acquiring certificates
remain necessary screens before asserting a contribution or economic gain.
