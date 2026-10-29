# Strong controls that remove the apparent gap advantage

Codex (GPT-6), October 28, 2026. DEVELOPMENT. These are ordinary special-case
derivations used to delimit the intended contribution, not separate novelty
claims or new prerequisites for V19-R/v1.

## Known slopes, independently bounded intercepts

Suppose the response is h(z)=max_i(c_i(z)+theta_i), with known c_i and unknown
scalar intercepts theta_i in [L_i,U_i]. Measurements are
a_j<=max_i(c_ji+theta_i)<=b_j. Absorb every universal upper inequality:

    U_i' = min(U_i, min_j(b_j-c_ji)).

If any U_i'<L_i, the source is empty. Otherwise its remaining conditions are
that for each j at least one theta_i is at least a_j-c_ji. The source is
upward closed inside the box [L,U']; if feasible, its top corner U' is
feasible. The segment from any feasible point to U' remains feasible, so
the source is star-shaped and every continuous scalar image is an interval.
Thus a disconnected future range is unavailable in this important special
case. Unknown slopes or more general local coefficient coupling matter.

There is also a direct O(n*k) formula for the future max at fixed z_star.
Let d_i=c_i(z_star), E_j={i:a_j-c_ji<=U_i'}, and

    q_0 = max_i(d_i+L_i),
    q_min = max(q_0, max_j min_(i in E_j)
                           (d_i+max(L_i,a_j-c_ji))),
    q_max = max_i(d_i+U_i').

An empty E_j means inconsistency. With k=0 the max over j is absent and
q_min=q_0. Necessity follows from the baseline lower bounds and the witness
needed for each observation. For sufficiency choose, for each j, a minimizing
i in E_j, and set each theta_i to the maximum of L_i and the requirements
assigned to it. Each assigned requirement is <=U_i'; the resulting future
maximum is <=q_min and all observations hold. Necessity then gives equality.
The top corner realizes q_max. Connectedness supplies every intermediate
value. This is a mathematical derivation of a strong cheap control, not a
measured speed comparison.

[Maragos and Theodosis, arXiv:1912.03891](https://arxiv.org/pdf/1912.03891),
section 7.3, equations (68)--(71) and its known-slope discussion, solves a
related tropical fitting problem by fixing the slope vectors and estimating
intercepts through max-plus residuation. Their slopes may first be selected
from gradients; that selection does not preserve every uncertain slope model.
The above bounded-error prediction calculation is our explicit special-case
control, with its elementary monotonicity fully stated. It does not purport
to improve their fitting method.

## A model-count revision can remove the worked gap

In prediction_duty.md, add a third independently uncertain affine piece with
endpoint responses (u_3,v_3) in [0,1]^2, without either calibrated sum strip.
The old envelope observations permit u_3,v_3<=1. Any compatible model has
some v_i>=99/100. Since every u_i<=1, its future maximum is at least
(-1+3*99/100)/2=197/200. All pieces have future value at most3/2.
Both bounds and every intermediate value are attainable. Fix
(u_1,v_1)=(3/5,3/5) and (u_2,v_2)=(1,4/5). Their future values are3/5
and7/10; piece2 supplies the old u witness. For q in[197/200,1], choose
(u_3,v_3)=(1,(2q+1)/3). For q in[1,3/2], choose
(u_3,v_3)=(3-2q,1). Piece3 supplies the old v witness and has future value q.
The expanded model therefore has the full interval[197/200,3/2] as its
prediction set. In
particular 5/4 becomes attainable, and the old reciprocal bound disappears.
The earlier gap certificate is still correct for its original two-piece
model; it is stale for this revised source version.

This is a substantive limit of the intended use. Known physical architecture
or defensible model-specific bounds can justify the original contract.
A fitted two-piece surrogate cannot silently assume away an unobserved third
piece. When a report contradicts the original prediction set, revising the
model class is one live explanation. The exact method supports that diagnosis
without identifying the faulty premise or manufacturing a probability that
the original model is true.

An initial derivation incorrectly retained43/40 as the expanded lower bound.
That bound relied on the old pair jointly satisfying both receipts; adding a
third witness relaxes that condition on the pair. The mistake was found in
the immediate analytic reconstruction, before execution or a frozen claim.
The explicit construction and bound above replace it. This is precisely why
changing the source version requires redoing the inference, not just adding
a new response to an old conditional prediction interval.
