# Scalar-offset specialization: an inexpensive ordinary control

Codex (GPT-6), October26,2026. DEVELOPMENT. This is a specialization of
one-sided tropical linear equations, not a new general inference principle.
It supplies a strong control before running the exponential face machinery.

Let theta_i independently range over rational intervals [l_i,u_i]. Retain
k exact receipts min_i(a_ji+theta_i)=v_j. Define

    L_i=max(l_i, max_j(v_j-a_ji)),
    E_j={i: a_ji+L_i=v_j}.

The source is consistent exactly when every L_i<=u_i and every E_j is
nonempty. Necessity follows from the common lower bounds. Sufficiency is
the single vector theta=L. Every feasible theta lies above L, and for each
j at least one i in E_j stays at L_i. In particular the conditional source
is star-shaped about L: the straight segment from theta to L preserves
an attainer of each receipt and never violates its lower inequalities.

For a new offset row c, V_c(theta)=min_i(c_i+theta_i). Its exact attainable
set is the interval [ell_c,U_c], where

    ell_c=min_i(c_i+L_i),
    U_c=min( min_i(c_i+u_i),
             min_j max_(i in E_j)(c_i+L_i) ).

An empty receipt minimum is +infinity. To attain t between these endpoints,
set theta_i=max(L_i,t-c_i). The first upper restriction keeps theta_i<=u_i;
the second ensures each old receipt retains an attainer. The new value is
t: either an L coordinate already attains it or some raised coordinate does.
This is also a direct verification of the usual residuation calculation.
All feasibility and endpoint work is O(nk+n) scalar arithmetic with input
bit costs separate. General generator polytopes do not have this common
least point; their coupling can create the disconnected values in value_sets.

## Coupled contrast of two offset edits

For rows c,d, define F=min_i(c_i+theta_i), G=min_i(d_i+theta_i).
The identity F-G=max_a(F-d_a-theta_a) permits one anchor a. Reducing only
theta_a to L_a preserves feasibility and decreases F by no more than the
same amount. Thus an anchor's maximum is attained with theta_a=L_a.
With that coordinate fixed, its sharp maximum F is

    U_a(c)=min( c_a+L_a,
                min_(i!=a)(c_i+u_i),
                min_(j: a notin E_j) max_(i in E_j)(c_i+L_i) ).

Receipts containing a in E_j are already satisfied. The other receipts and
free coordinates use the same threshold construction as above. Therefore

    max(F-G)=max_a[U_a(c)-d_a-L_a].

Swap c,d and negate to obtain the sharp lower contrast. Continuous images
of this star-shaped source are intervals, so these endpoints describe the
entire contrast set. Precompute each receipt maximum and the two smallest
c_i+u_i; evaluating the n anchors takes O(nk+n) arithmetic. Repeated minima
and n=1 use their natural empty-set conventions. Witnesses are explicit.

This is a derived useful specialization; its formula has not yet been
compared theorem by theorem with tropical fractional optimization. No
moderate-novelty claim or readiness forecast attaches to it. A generic
mixed-integer formulation or the identical ordinary formula ties exactly.
